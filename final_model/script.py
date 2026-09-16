"""Lightweight inference package reproducing public-best model 126."""
from pathlib import Path
import json
import math
import lightgbm as lgb
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

ROOT = Path(__file__).resolve().parent
TEST, SAMPLE = ROOT/"data"/"test.csv", ROOT/"data"/"sample_submission.csv"
OUTPUT = ROOT/"output"/"submission.csv"
ID, TARGET = "row_id", "control_success"
CATS = ["top_bottom", "game_type", "pitcher_hand", "batter_hand", "pitcher_team_id", "batter_team_id", "base_state", "pitcher_batter_hand"]
CHUNK_SIZE = 200_000
CSR = ["csr_pitcher_season_n_log", "csr_pitcher_season_success_rate", "csr_pitcher_season_success_shrink20", "csr_pitcher_season_success_shrink50", "csr_pitcher_season_success_shrink100", "csr_pitcher_season_minus_career"]
BCSR = ["csr_batter_season_n_log", "csr_batter_season_success_rate", "csr_batter_season_success_shrink20", "csr_batter_season_success_shrink50", "csr_batter_season_success_shrink100", "csr_batter_season_minus_career"]

def safe_numeric(frame, column):
    return pd.to_numeric(frame[column], errors="coerce")

def add_feature(frame, name, value):
    if name in frame.columns:
        raise RuntimeError(f"feature collision: {name}")
    array = np.asarray(value, dtype=np.float64).copy()
    array[~np.isfinite(array)] = np.nan
    frame[name] = array.astype(np.float32)

def engineer_features(base):
    frame = base.copy()
    families = {key: [] for key in ["history_dynamics", "sample_reliability", "pitcher_batter_matchup", "pitchmix_geometry", "game_state_interactions", "expectancy_context", "history_missingness"]}
    def put(family, name, value):
        add_feature(frame, name, value); families[family].append(name)

    pitcher_success = safe_numeric(frame, "asof_pitcher_success_rate"); batter_success = safe_numeric(frame, "asof_batter_success_rate")
    pitcher_middle = safe_numeric(frame, "asof_pitcher_middle_rate"); batter_middle = safe_numeric(frame, "asof_batter_middle_rate")
    success_recent = [safe_numeric(frame, f"asof_pitcher_prev{window}_game_success_rate") for window in [1, 3, 5]]
    middle_recent = [safe_numeric(frame, f"asof_pitcher_prev{window}_game_middle_rate") for window in [1, 3, 5]]
    for window, value in zip([1, 3, 5], success_recent): put("history_dynamics", f"dyn_success_gap_prev{window}", value-pitcher_success)
    for window, value in zip([1, 3, 5], middle_recent): put("history_dynamics", f"dyn_middle_gap_prev{window}", value-pitcher_middle)
    put("history_dynamics", "dyn_success_prev1_minus_prev3", success_recent[0]-success_recent[1]); put("history_dynamics", "dyn_success_prev3_minus_prev5", success_recent[1]-success_recent[2]); put("history_dynamics", "dyn_success_prev1_minus_prev5", success_recent[0]-success_recent[2])
    put("history_dynamics", "dyn_middle_prev1_minus_prev3", middle_recent[0]-middle_recent[1]); put("history_dynamics", "dyn_middle_prev3_minus_prev5", middle_recent[1]-middle_recent[2]); put("history_dynamics", "dyn_middle_prev1_minus_prev5", middle_recent[0]-middle_recent[2])
    put("history_dynamics", "dyn_success_recent_spread", pd.concat(success_recent, axis=1).max(axis=1)-pd.concat(success_recent, axis=1).min(axis=1)); put("history_dynamics", "dyn_middle_recent_spread", pd.concat(middle_recent, axis=1).max(axis=1)-pd.concat(middle_recent, axis=1).min(axis=1))

    pitcher_n = safe_numeric(frame, "asof_pitcher_n").clip(lower=0); batter_n = safe_numeric(frame, "asof_batter_n").clip(lower=0); mix_n = safe_numeric(frame, "asof_pitcher_pitchmix_n").clip(lower=0)
    put("sample_reliability", "rel_log1p_pitcher_n", np.log1p(pitcher_n)); put("sample_reliability", "rel_log1p_batter_n", np.log1p(batter_n)); put("sample_reliability", "rel_log1p_pitchmix_n", np.log1p(mix_n))
    for scale in [25., 200., 1000.]:
        put("sample_reliability", f"rel_pitcher_n_{int(scale)}", pitcher_n/(pitcher_n+scale)); put("sample_reliability", f"rel_batter_n_{int(scale)}", batter_n/(batter_n+scale))
    put("sample_reliability", "rel_effective_matchup_n", 2*pitcher_n*batter_n/(pitcher_n+batter_n+1.)); put("sample_reliability", "rel_pitcher_success_x_n200", pitcher_success*pitcher_n/(pitcher_n+200.)); put("sample_reliability", "rel_batter_success_x_n200", batter_success*batter_n/(batter_n+200.))

    put("pitcher_batter_matchup", "match_success_difference", pitcher_success-batter_success); put("pitcher_batter_matchup", "match_success_abs_difference", (pitcher_success-batter_success).abs()); put("pitcher_batter_matchup", "match_success_ratio", (pitcher_success+.01)/(batter_success+.01))
    p_logit = np.log(pitcher_success.clip(1e-4, 1-1e-4)/(1-pitcher_success.clip(1e-4, 1-1e-4))); b_logit = np.log(batter_success.clip(1e-4, 1-1e-4)/(1-batter_success.clip(1e-4, 1-1e-4)))
    put("pitcher_batter_matchup", "match_success_logit_difference", p_logit-b_logit); put("pitcher_batter_matchup", "match_middle_difference", pitcher_middle-batter_middle); put("pitcher_batter_matchup", "match_middle_abs_difference", (pitcher_middle-batter_middle).abs()); put("pitcher_batter_matchup", "match_log_sample_ratio", np.log1p(pitcher_n)-np.log1p(batter_n))
    put("pitcher_batter_matchup", "match_same_hand", safe_numeric(frame, "pitcher_hand").eq(safe_numeric(frame, "batter_hand")).astype(float)); put("pitcher_batter_matchup", "match_pitcher_success_minus_batter_middle", pitcher_success-batter_middle); put("pitcher_batter_matchup", "match_pitcher_middle_minus_batter_success", pitcher_middle-batter_success)

    mix_columns = ["asof_pitcher_fastball_rate", "asof_pitcher_breaking_rate", "asof_pitcher_offspeed_rate"]
    mix = frame[mix_columns].apply(pd.to_numeric, errors="coerce"); mix_sum = mix.sum(axis=1, min_count=1); normalized = mix.div(mix_sum.replace(0, np.nan), axis=0); entropy = -(normalized.clip(lower=1e-12)*np.log(normalized.clip(lower=1e-12))).sum(axis=1, min_count=1)
    put("pitchmix_geometry", "mix_entropy", entropy); put("pitchmix_geometry", "mix_hhi", (normalized**2).sum(axis=1, min_count=1)); put("pitchmix_geometry", "mix_max_share", normalized.max(axis=1)); put("pitchmix_geometry", "mix_min_share", normalized.min(axis=1)); put("pitchmix_geometry", "mix_share_spread", normalized.max(axis=1)-normalized.min(axis=1))
    put("pitchmix_geometry", "mix_fastball_minus_breaking", normalized.iloc[:, 0]-normalized.iloc[:, 1]); put("pitchmix_geometry", "mix_fastball_minus_offspeed", normalized.iloc[:, 0]-normalized.iloc[:, 2]); put("pitchmix_geometry", "mix_breaking_minus_offspeed", normalized.iloc[:, 1]-normalized.iloc[:, 2]); put("pitchmix_geometry", "mix_missing_count", mix.isna().sum(axis=1)); put("pitchmix_geometry", "mix_available_count", mix.notna().sum(axis=1))

    balls = safe_numeric(frame, "balls_before"); strikes = safe_numeric(frame, "strikes_before"); outs = safe_numeric(frame, "outs_before"); runners = safe_numeric(frame, "num_runners_on"); inning = safe_numeric(frame, "inning"); score = safe_numeric(frame, "score_diff_pitcher_team"); leverage = safe_numeric(frame, "li")
    put("game_state_interactions", "state_count_balance", balls-strikes); put("game_state_interactions", "state_count_total", balls+strikes); put("game_state_interactions", "state_three_ball", balls.eq(3).astype(float)); put("game_state_interactions", "state_two_strike", strikes.eq(2).astype(float)); put("game_state_interactions", "state_full_count", (balls.eq(3)&strikes.eq(2)).astype(float))
    put("game_state_interactions", "state_runners_x_outs", runners*outs); put("game_state_interactions", "state_balls_x_outs", balls*outs); put("game_state_interactions", "state_strikes_x_outs", strikes*outs); put("game_state_interactions", "state_abs_pitcher_score_diff", score.abs()); put("game_state_interactions", "state_close_game", score.abs().le(1).astype(float)); put("game_state_interactions", "state_late_inning", inning.ge(7).astype(float)); put("game_state_interactions", "state_leverage_x_count_total", leverage*(balls+strikes)); put("game_state_interactions", "state_leverage_x_runners", leverage*runners)
    scoring_position = safe_numeric(frame, "runner_on_2b").fillna(0)+safe_numeric(frame, "runner_on_3b").fillna(0)
    put("game_state_interactions", "state_scoring_position_runners", scoring_position); put("game_state_interactions", "state_bases_loaded", runners.eq(3).astype(float))

    home_we = safe_numeric(frame, "home_win_expectancy")/100.; away_we = safe_numeric(frame, "away_win_expectancy")/100.; top = frame["top_bottom"].astype(str).eq("T")
    pitcher_we = pd.Series(np.where(top, home_we, away_we), index=frame.index); batter_we = pd.Series(np.where(top, away_we, home_we), index=frame.index)
    put("expectancy_context", "exp_home_minus_away", home_we-away_we); put("expectancy_context", "exp_abs_home_minus_away", (home_we-away_we).abs()); put("expectancy_context", "exp_pitcher_team", pitcher_we); put("expectancy_context", "exp_batter_team", batter_we); put("expectancy_context", "exp_pitcher_minus_batter", pitcher_we-batter_we); put("expectancy_context", "exp_pitcher_uncertainty", 1-(pitcher_we-.5).abs()*2); put("expectancy_context", "exp_leverage_x_pitcher_gap", leverage*(pitcher_we-batter_we)); put("expectancy_context", "exp_score_x_home_gap", safe_numeric(frame, "score_diff_home")*(home_we-away_we))
    home_clip = home_we.clip(1e-4, 1-1e-4); put("expectancy_context", "exp_home_logit", np.log(home_clip/(1-home_clip)))

    historical = ["asof_pitcher_success_rate", "asof_pitcher_reverse_rate", "asof_pitcher_middle_rate", "asof_pitcher_ball_rate", "asof_pitcher_strike_rate", *[f"asof_pitcher_prev{window}_game_success_rate" for window in [1, 3, 5]], *[f"asof_pitcher_prev{window}_game_middle_rate" for window in [1, 3, 5]], "asof_batter_success_rate", "asof_batter_middle_rate", *mix_columns]
    historical_frame = frame[historical]
    put("history_missingness", "miss_history_count", historical_frame.isna().sum(axis=1)); put("history_missingness", "miss_history_any", historical_frame.isna().any(axis=1).astype(float)); put("history_missingness", "miss_recent_success_count", pd.concat(success_recent, axis=1).isna().sum(axis=1)); put("history_missingness", "miss_recent_middle_count", pd.concat(middle_recent, axis=1).isna().sum(axis=1)); put("history_missingness", "miss_pitchmix_count", mix.isna().sum(axis=1)); put("history_missingness", "miss_pitcher_cold_start", pitcher_n.eq(0).astype(float)); put("history_missingness", "miss_batter_cold_start", batter_n.eq(0).astype(float)); put("history_missingness", "miss_both_cold_start", (pitcher_n.eq(0)&batter_n.eq(0)).astype(float)); put("history_missingness", "miss_pitchmix_cold_start", mix_n.eq(0).astype(float)); put("history_missingness", "miss_core_rate_count", frame[["asof_pitcher_success_rate", "asof_batter_success_rate"]].isna().sum(axis=1))
    all_names = [name for values in families.values() for name in values]
    if len(all_names) != len(set(all_names)) or any(name not in frame for name in all_names): raise RuntimeError("invalid engineered feature manifest")
    return frame, families

def s7_calibrate(values):
    x = np.asarray(values, float)-.5
    return np.clip(values + .002895168052643 + .166636301069256*x - .014393031311814568*np.abs(x) - .0355469055927294*x*np.abs(x) + 1.46303042577597*x**3 - 24.143315319253535*x**4 + 10.*x**5, 0, 1)

def fixed_bin(values, edges, labels):
    return pd.cut(pd.to_numeric(values,errors="coerce"),[-np.inf,*edges,np.inf],labels=labels,include_lowest=True).astype("string").fillna("NA").astype(str)

def phase_adjustment(raw, base, artifact):
    count=raw["balls_before"].astype(str)+"-"+raw["strikes_before"].astype(str);hands=raw["pitcher_hand"].astype(str)+"-"+raw["batter_hand"].astype(str);base_state=raw["base_state"].astype("string").fillna("NA").astype(str);outs=raw["outs_before"].astype(str);lev=fixed_bin(raw["li"],[.7,1.3,2.0],["low","mid","high","extreme"])
    labels={"count_hands":count+"|"+hands,"base_outs_count":base_state+"|"+outs+"|"+count,"count_base":count+"|"+base_state,"lev_count":lev+"|"+count,"base_outs":base_state+"|"+outs}
    columns=[]
    for family in artifact["families"]:columns.append(labels[family].map(artifact["maps"][family]).fillna(0).to_numpy(float)-float(artifact["centers"][family]))
    values=np.column_stack(columns);z=np.asarray(base)-.5;expanded=np.column_stack([values,values*z[:,None],values*np.abs(z)[:,None]]);standard=(expanded-np.asarray(artifact["mean"]))/np.asarray(artifact["std"]);design=np.column_stack([np.ones(len(raw)),standard]);late=(pd.to_numeric(raw["inning"],errors="coerce").fillna(0).to_numpy()>=7).astype(int);out=np.zeros(len(raw))
    for group in [0,1]:
        mask=late==group;out[mask]=np.clip(design[mask]@np.asarray(artifact["coefs"][str(group)]),-.003,.003)
    return out

def recent_matrix(raw, xbid, artifact):
    frame=raw.copy();frame["pitcher_batter_hand"]=frame["pitcher_hand"].astype(str)+"_"+frame["batter_hand"].astype(str);frame["pitcher_batter_success_interaction"]=frame["asof_pitcher_success_rate"]*frame["asof_batter_success_rate"];frame["pitcher_batter_middle_interaction"]=frame["asof_pitcher_middle_rate"]*frame["asof_batter_middle_rate"];frame["pitcher_ball_pressure"]=frame["asof_pitcher_ball_rate"]*frame["balls_before"];frame,_=engineer_features(frame)
    for c in CSR+BCSR:frame[c]=xbid[c].to_numpy()
    names=artifact["recent_feature_names"];x=frame[names].copy()
    for c in artifact["recent_categorical_features"]:x[c]=x[c].astype("string").fillna("__MISSING__").astype(str)
    return x

def asset(name):
    """Resolve an asset from the required model/ directory."""
    path = ROOT / "model" / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing model asset: {path}")
    return path

def build(raw, names, catboost=False):
    x = raw.drop(columns=[ID, "pitcher_id", "batter_id"]).copy()
    x["pitcher_batter_hand"] = x["pitcher_hand"].astype(str)+"_"+x["batter_hand"].astype(str)
    x["pitcher_batter_success_interaction"] = x["asof_pitcher_success_rate"]*x["asof_batter_success_rate"]
    x["pitcher_batter_middle_interaction"] = x["asof_pitcher_middle_rate"]*x["asof_batter_middle_rate"]
    x["pitcher_ball_pressure"] = x["asof_pitcher_ball_rate"]*x["balls_before"]
    if list(x.columns) != names or len(names) != 49:
        raise RuntimeError("feature count/name/order mismatch")
    for column in CATS:
        x[column] = x[column].astype("string").fillna("__MISSING__").astype(str) if catboost else x[column].astype("category")
    return x

def add_current_season(x, raw, baseline, names):
    ids = raw["pitcher_id"].astype(str)
    base_n = ids.map(baseline["base_n"]).fillna(0).to_numpy(float)
    base_success = ids.map(baseline["base_success"]).fillna(0).to_numpy(float)
    total_n = pd.to_numeric(raw["asof_pitcher_n"], errors="coerce").fillna(0).to_numpy(float)
    total_success = np.rint(total_n*pd.to_numeric(raw["asof_pitcher_success_rate"], errors="coerce").fillna(0).to_numpy(float))
    season_n = np.maximum(total_n-base_n, 0.0)
    season_success = np.clip(total_success-base_success, 0.0, season_n)
    rate = np.divide(season_success, season_n, out=np.full(len(raw), np.nan), where=season_n>0)
    career = np.divide(base_success, base_n, out=np.full(len(raw), np.nan), where=base_n>0)
    prior = np.where(np.isfinite(career), career, 0.5238)
    x[CSR[0]], x[CSR[1]] = np.log1p(season_n), rate
    for column, strength in zip(CSR[2:5], [20.0, 50.0, 100.0]):
        x[column] = (season_success+strength*prior)/(season_n+strength)
    x[CSR[5]] = rate-prior
    if list(x.columns) != names or len(names) != 55:
        raise RuntimeError("current-season feature mismatch")
    return x

def add_batter_current_season(x, raw, baseline, names):
    ids = raw["batter_id"].astype(str)
    base_n = ids.map(baseline["base_n"]).fillna(0).to_numpy(float)
    base_success = ids.map(baseline["base_success"]).fillna(0).to_numpy(float)
    total_n = pd.to_numeric(raw["asof_batter_n"], errors="coerce").fillna(0).to_numpy(float)
    total_success = np.rint(total_n*pd.to_numeric(raw["asof_batter_success_rate"], errors="coerce").fillna(0).to_numpy(float))
    season_n = np.maximum(total_n-base_n, 0.0)
    season_success = np.clip(total_success-base_success, 0.0, season_n)
    rate = np.divide(season_success, season_n, out=np.full(len(raw), np.nan), where=season_n>0)
    career = np.divide(base_success, base_n, out=np.full(len(raw), np.nan), where=base_n>0)
    prior = np.where(np.isfinite(career), career, 0.5238)
    x[BCSR[0]], x[BCSR[1]] = np.log1p(season_n), rate
    for column, strength in zip(BCSR[2:5], [20.0, 50.0, 100.0]):
        x[column] = (season_success+strength*prior)/(season_n+strength)
    x[BCSR[5]] = rate-prior
    if list(x.columns) != names or len(names) != 61:
        raise RuntimeError("batter current-season feature mismatch")
    return x, season_n

def main():
    current95 = lgb.Booster(model_file=str(asset("current_season_lgbm_095.txt"))); current101 = lgb.Booster(model_file=str(asset("current_season_lgbm_101.txt")))
    current_cat = CatBoostClassifier(); current_cat.load_model(str(asset("current_season_catboost.cbm")))
    batter_cat = CatBoostClassifier(); batter_cat.load_model(str(asset("current_batter_catboost.cbm")))
    batter_id_cat = CatBoostClassifier(); batter_id_cat.load_model(str(asset("current_batter_id_catboost.cbm")))
    regime_models = {}
    for regime in ["batter_ahead", "even", "pitcher_ahead"]:
        model = CatBoostClassifier(); model.load_model(str(asset(f"count_regime_{regime}.cbm"))); regime_models[regime] = model
    artifact = json.loads(asset("candidate_453.json").read_text(encoding="utf-8"))
    relation_models = {}
    for relation in ["same", "opposite"]:
        model = CatBoostClassifier(); model.load_model(str(asset(f"hand_relation_{relation}.cbm"))); relation_models[relation] = model
    relation_artifact = json.loads(asset("candidate_472.json").read_text(encoding="utf-8"))
    baseline_frame = pd.read_csv(asset("pitcher_season_baseline.csv"), dtype={"pitcher_id": str})
    if baseline_frame.pitcher_id.duplicated().any(): raise RuntimeError("duplicate pitcher baseline")
    baseline = baseline_frame.set_index("pitcher_id")
    batter_baseline_frame = pd.read_csv(asset("batter_season_baseline.csv"), dtype={"batter_id": str})
    if batter_baseline_frame.batter_id.duplicated().any(): raise RuntimeError("duplicate batter baseline")
    batter_baseline = batter_baseline_frame.set_index("batter_id")
    current_names = current95.feature_name(); names = current_names[:49]
    if current101.feature_name()!=current_names or len(current_names)!=55 or len(names)!=49: raise RuntimeError("current model metadata mismatch")
    if current_cat.feature_names_ != current_names: raise RuntimeError("current CatBoost metadata mismatch")
    batter_names = batter_cat.feature_names_
    if len(batter_names)!=61 or batter_names[:55]!=current_names: raise RuntimeError("batter CatBoost metadata mismatch")
    batter_id_names = batter_id_cat.feature_names_
    if len(batter_id_names)!=62 or batter_id_names[:61]!=batter_names or batter_id_names[-1]!="batter_id": raise RuntimeError("batter-id CatBoost metadata mismatch")
    if any(model.feature_names_ != artifact["recent_feature_names"] for model in regime_models.values()): raise RuntimeError("regime model metadata mismatch")
    if any(model.feature_names_ != relation_artifact["recent_feature_names"] for model in relation_models.values()): raise RuntimeError("relation model metadata mismatch")
    submission = pd.read_csv(SAMPLE, encoding="utf-8-sig"); parts, offset = [], 0
    for raw in pd.read_csv(TEST, encoding="utf-8-sig", chunksize=CHUNK_SIZE):
        end = offset+len(raw)
        if not raw[ID].reset_index(drop=True).equals(submission[ID].iloc[offset:end].reset_index(drop=True)): raise RuntimeError("row_id order mismatch")
        xl, xc = build(raw, names, False), build(raw, names, True)
        xs = add_current_season(xl.copy(), raw, baseline, current_names)
        xsc = add_current_season(xc.copy(), raw, baseline, current_names)
        p_current = np.clip(.6*current95.predict(xs)+.4*current101.predict(xs)-.006, 0, 1)
        p_current_cat = current_cat.predict_proba(xsc)[:, 1]
        prediction = np.clip(.2791734961563579*p_current+.7208265038436421*p_current_cat-.00394185533843516, 0, 1)
        xbsc, batter_season_n = add_batter_current_season(xsc.copy(), raw, batter_baseline, batter_names)
        p_batter_cat = batter_cat.predict_proba(xbsc)[:, 1]
        batter_prediction = np.clip(.2791734961563579*p_current+.7208265038436421*p_batter_cat-.004722230724360439, 0, 1)
        prediction = np.clip(prediction+(batter_season_n>=10.0)*.25*(batter_prediction-prediction), 0, 1)
        xbid = xbsc.copy(); xbid["batter_id"] = raw["batter_id"].astype("string").fillna("__MISSING__").astype(str)
        if list(xbid.columns) != batter_id_names: raise RuntimeError("batter-id feature mismatch")
        p_batter_id = batter_id_cat.predict_proba(xbid)[:, 1]
        batter_id_prediction = np.clip(.2791734961563579*p_current+.7208265038436421*p_batter_id-.004562541132185068, 0, 1)
        prediction = np.clip(.5*prediction+.5*batter_id_prediction, 0, 1)
        base_s7 = s7_calibrate(prediction)
        phase_correction = phase_adjustment(raw, base_s7, artifact)
        xr = recent_matrix(raw, xbid, artifact)
        if list(xr.columns) != artifact["recent_feature_names"]: raise RuntimeError("recent feature mismatch")
        balls = pd.to_numeric(raw["balls_before"], errors="coerce").fillna(0).to_numpy(); strikes = pd.to_numeric(raw["strikes_before"], errors="coerce").fillna(0).to_numpy()
        row_regime = np.where(balls>strikes, "batter_ahead", np.where(balls<strikes, "pitcher_ahead", "even")); regime_raw = np.empty(len(raw), dtype=float)
        for regime, model in regime_models.items():
            positions = np.flatnonzero(row_regime==regime)
            if len(positions): regime_raw[positions] = model.predict_proba(xr.iloc[positions])[:,1]
        rc=np.asarray(artifact["recent_calibration"],float);rx=regime_raw-.5;regime_prediction=np.clip(regime_raw+rc[0]+rc[1]*rx+rc[2]*np.abs(rx),0,1)
        prediction = np.clip(base_s7 + float(artifact["phase_weight"])*phase_correction + float(artifact["regime_weight"])*(regime_prediction-base_s7),0,1)
        same = pd.to_numeric(raw["pitcher_hand"], errors="coerce").to_numpy() == pd.to_numeric(raw["batter_hand"], errors="coerce").to_numpy()
        relation_raw = np.empty(len(raw), dtype=float)
        for relation, model in relation_models.items():
            positions = np.flatnonzero(same if relation == "same" else ~same)
            if len(positions): relation_raw[positions] = model.predict_proba(xr.iloc[positions])[:, 1]
        rc = np.asarray(relation_artifact["relation_calibration"], float); rx = relation_raw-.5
        relation_prediction = np.clip(relation_raw+rc[0]+rc[1]*rx+rc[2]*np.abs(rx),1e-6,1-1e-6)
        incumbent = np.clip(prediction,1e-6,1-1e-6); incumbent_logit = np.log(incumbent/(1-incumbent))
        difference = np.log(relation_prediction/(1-relation_prediction))-incumbent_logit
        residual = (difference-(float(relation_artifact["projection_intercept"])+float(relation_artifact["projection_slope"])*incumbent_logit))/float(relation_artifact["residual_scale"])
        prediction = 1/(1+np.exp(-np.clip(incumbent_logit+float(relation_artifact["rank_weight"])*residual,-30,30)))
        if not np.isfinite(prediction).all() or np.any((prediction<0)|(prediction>1)): raise RuntimeError("invalid prediction")
        parts.append(pd.Series(prediction)); offset = end
    if offset != len(submission): raise RuntimeError("row count mismatch")
    prediction = pd.concat(parts, ignore_index=True)
    if prediction.isna().any() or not prediction.map(math.isfinite).all(): raise RuntimeError("NaN/inf")
    submission[TARGET] = prediction; OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(OUTPUT, index=False, encoding="utf-8"); print(f"Saved {len(submission):,} rows to {OUTPUT}")

if __name__ == "__main__": main()
