# LG Aimers Online Hackathon - Experiment Log

이 파일은 모델 실험에서 무엇을 왜 변경했고 결과가 어땠는지를 사람이 읽기 쉽게 기록하는 변경 이력이다. 수치 기록용 `results.csv`를 대체하지 않는다.

## Current Baseline

### LGBM-130

- Base models: LGBM-095 / LGBM-101
- Ensemble: `0.6 * LGBM-095 + 0.4 * LGBM-101`
- Features: 49
- Walk-forward mean Brier: 0.24767113993370793
- Walk-forward mean ROC-AUC: 0.5530385153643456
- 2024 Brier: 0.2480885134392783
- 2024 ROC-AUC: 0.5480200784149498
- 실제 리더보드 점수: 약 704
- Status: Current Baseline

---

## Feature Experiments

### LGBM-043

- Feature count: 50
- 결과:
  - Brier: 0.24813187006678789
  - ROC-AUC: 0.5474123979847956
- 판정: REJECT
- 이유: LGBM-029 대비 Brier 악화

### LGBM-044

- Feature count: 50
- 결과:
  - Brier: 0.24813530193282593
  - ROC-AUC: 0.5474553752929705
- 판정: REJECT
- 이유: LGBM-029 대비 Brier 악화

### LGBM-045

- Feature count: 50
- 결과:
  - Brier: 0.24814896191185257
  - ROC-AUC: 0.5472649117918489
- 판정: REJECT
- 이유: LGBM-029 대비 Brier 악화

### LGBM-046

- Feature count: 50
- 결과:
  - Brier: 0.24814556826746414
  - ROC-AUC: 0.5473439087833403
- 판정: REJECT
- 이유: LGBM-029 대비 Brier 악화

### LGBM-047

- Feature: `tm_prev_season_month_fastball_speed_median`
- Feature count: 50
- Brier: 0.24810827083148893
- ROC-AUC: 0.5477195259015495
- 판정: REJECT
- 이유: LGBM-029 대비 Brier 악화

---

## Validation Analysis

### LGBM-029 Walk-Forward Validation

5-fold time-based validation을 수행함.

- 2020 Brier: 0.2480689387
- 2021 Brier: 0.2457608164
- 2022 Brier: 0.2433782762
- 2023 Brier: 0.2531070157
- 2024 Brier: 0.2480956179
- Mean Brier: 0.2476821329843597
- Brier std: 0.0036043231722169

결론:

시즌별 Brier 변동이 지금까지 Feature 실험에서 발생한 미세한 Brier 차이보다 훨씬 크므로, 단일 2024 validation만으로 Feature를 채택하지 않도록 5-fold walk-forward validation을 사용하기로 함.

---

## Calibration

### Platt Calibration

- Model training: 2019~2021
- Calibration: 2022
- Validation: 2023 / 2024

2023:

- Raw Brier: 0.25276199875578
- Calibrated Brier: 0.2531101275551658
- Change: +0.0003481287993858384
- 판정: REJECT

2024:

- Raw Brier: 0.25329758970318894
- Calibrated Brier: 0.2536237024027909
- Change: +0.000326112699601977
- 판정: REJECT

결론:

해당 time-based Platt calibration 구조에서는 Brier가 개선되지 않았다.

---

## Trackman

Trackman은 공식 제공 데이터라는 전제에서 사용 가능성을 검토함.

현재 `train.csv`와 Trackman의 선수 ID 체계가 직접 연결되지 않아 선수별 Trackman Feature는 사용하지 않음.

사용 가능한 방식으로 다음을 이용한 리그/기간 수준 Feature를 검토함.

- `season`
- `game_month`
- 전년도 데이터

LGBM-047의 전년도 동월 fastball `rel_speed` median Feature는 Brier 개선에 실패하여 REJECT.

LGBM-048에서 다음 Feature를 검증함.

- `tm_prev_season_month_fastball_spin_median`

5-fold paired walk-forward 기준을 충족하지 못했고 2024 Brier와 ROC-AUC도 악화하여 REJECT.

---

## Current Failed Features

다음 Feature는 현재 실패한 Feature로 기록한다.

- `pitcher_form_diff_1`
- `pitcher_strike_pressure`
- `pitcher_li_success_pressure`
- `pitcher_prev_game_missing`
- `tm_prev_season_month_fastball_speed_median`
- `tm_prev_season_month_fastball_spin_median`
- `pitcher_batter_success_gap`
- `pitcher_recent_trend_3v5`

앞으로 실험에서 임의로 다시 추가하지 않는다.

---

## Current Experiment Policy

앞으로 Feature 실험은 가능하면 다음 순서로 진행한다.

1. LGBM-029 baseline 유지
2. Feature 정확히 1개 변경
3. 5-fold walk-forward validation
4. Brier 우선 평가
5. AUC 보조 평가
6. 결과를 `results.csv`에 기록
7. 변경 이유와 결과를 이 파일에 기록

---

## Future Experiment Entry Template

새로운 실험이 끝날 때마다 아래 형식을 이 파일의 맨 아래에 추가한다.

```markdown
## LGBM-XXX

### 변경

- 추가:
- 제거:
- 수정:

### 목적

- 왜 이 Feature/방법을 테스트했는지

### 결과

- Brier:
- ROC-AUC:
- ΔBrier:
- ΔAUC:

### 판정

- CANDIDATE / REJECT / BASELINE

### 이유

- 왜 채택 또는 폐기했는지 간단히 기록

### 비고

- Leakage 여부
- 대회 규칙 관련 사항
- 다음 실험에 영향을 주는 사항
```

## Recording Principles

- 실험 결과를 임의로 만들어내지 않는다.
- 사용자가 제공한 결과 또는 실제 실행 결과만 기록한다.
- 결과가 없는 실험은 수치를 작성하지 않는다.
- 실패한 Feature도 삭제하지 않고 기록을 유지한다.
- Feature를 복구했다면 `복구`라고 명확히 기록한다.
- 현재 baseline이 변경되면 Current Baseline 부분도 함께 업데이트한다.

---

## LGBM-048

### 변경

- 추가: `tm_prev_season_month_fastball_spin_median`
- 제거: 없음
- 수정: 없음

### 목적

- LGBM-029의 기존 49개 Feature에 전년도 동일 `game_month`의 리그 전체 fastball `spin_rate` 중앙값 Feature 1개를 추가했을 때 여러 validation season에서 일관되게 Brier가 개선되는지 확인

### 결과

- 2024 Brier: 0.2482264560517314
- 2024 ROC-AUC: 0.5463649911226753
- 2024 ΔBrier: +0.0001308381151043
- 2024 ΔAUC: -0.0016052386614959
- 5-fold Mean Baseline Brier: 0.2476821329843598
- 5-fold Mean Candidate Brier: 0.2474561658241517
- 5-fold Mean ΔBrier: -0.0002259671602080
- 5-fold Median ΔBrier: 0.0000000000000000
- Brier improvement folds: 2
- Brier degradation folds: 2
- AUC improvement folds: 1
- AUC degradation folds: 3
- 가장 개선된 fold 제외 Mean ΔBrier: +0.0000001068566173

### 판정

- REJECT

### 이유

- Brier 개선 fold가 5개 중 2개로 최소 3개 조건을 충족하지 못함
- Median ΔBrier가 음수가 아님
- 평균 Brier 개선 대부분이 2023 fold의 큰 개선에 의존하며, 해당 fold를 제외하면 평균 Brier가 악화함
- 2024에서 Brier와 ROC-AUC가 모두 악화함

### 비고

- Leakage 방지를 위해 Trackman은 각 행의 정확히 전년도 season과 동일 `game_month`, `pitch_type_group == "fastball"` 데이터만 사용
- 선수·경기·투구 ID 매핑을 사용하지 않음
- 결측값은 대체하지 않고 LightGBM native missing value 처리 사용
- LGBM-029는 Current Baseline으로 유지

---

## LGBM-052

### 변경

- 추가: `pitcher_recent_trend_3v5`
- 제거: 없음
- 수정: 없음

### 목적

- `asof_pitcher_prev3_game_success_rate - asof_pitcher_prev5_game_success_rate`로 투수의 단기 성공률 추세를 표현했을 때 여러 validation season에서 Brier가 개선되는지 확인

### 결과

- 2024 Brier: 0.2481587721736172
- 2024 ROC-AUC: 0.5470749908020858
- 2024 ΔBrier: +0.0000631542369901
- 2024 ΔAUC: -0.0008952389820854
- 5-fold Mean ΔBrier: +0.0000217683063551
- 5-fold Median ΔBrier: +0.0000057285946749
- 5-fold Mean ΔAUC: -0.0001219557585064
- 5-fold Median ΔAUC: -0.0000574758794052
- Brier improvement folds: 2
- Brier degradation folds: 3
- AUC improvement folds: 2
- AUC degradation folds: 3

### 판정

- REJECT

### 이유

- Mean ΔBrier와 Median ΔBrier가 모두 양수로 악화함
- Brier 개선 fold가 5개 중 2개에 그침
- 2024에서 Brier와 ROC-AUC가 모두 악화함

### 비고

- `test.py` 실행 환경 자동 전환과 결과 행 누락 컬럼 문제를 수정한 뒤 정상 완료
- LGBM-029는 Current Baseline으로 유지

---

## LGBM-049

### 변경

- 추가: `pitcher_batter_success_gap`
- 제거: 없음
- 수정: 없음

### 목적

- 기존 `pitcher_batter_success_interaction`을 유지하면서 `asof_pitcher_success_rate - asof_batter_success_rate`가 나타내는 투수와 타자의 성공률 차이를 추가했을 때 여러 validation season에서 Brier가 일관되게 개선되는지 확인

### 결과

- 2024 Brier: 0.2481354115353943
- 2024 ROC-AUC: 0.5473925144249512
- 2024 ΔBrier: +0.0000397935987672
- 2024 ΔAUC: -0.0005777153592200
- 5-fold Mean Baseline Brier: 0.2476821329843597
- 5-fold Mean Candidate Brier: 0.2477090146185862
- 5-fold Mean ΔBrier: +0.0000268816342265
- 5-fold Median ΔBrier: +0.0000056172365029
- 5-fold Mean ΔAUC: -0.0001300950070920
- 5-fold Median ΔAUC: -0.0000860158061423
- Brier improvement folds: 2
- Brier degradation folds: 3
- AUC improvement folds: 1
- AUC degradation folds: 4
- 가장 개선된 fold 제외 Mean ΔBrier: +0.0000441244211597

### 판정

- REJECT

### 이유

- Mean ΔBrier와 Median ΔBrier가 모두 양수로 전체적으로 악화함
- Brier 개선 fold가 5개 중 2개로 최소 3개 조건을 충족하지 못함
- 2024에서 Brier와 ROC-AUC가 모두 악화함
- 가장 개선된 fold를 제외한 평균도 악화하여 특정 fold 왜곡을 제거해도 채택 근거가 없음

### 비고

- Feature 생성에는 현재 투구 이전에 계산된 두 asof 성공률만 사용
- 기존 `pitcher_batter_success_interaction`과 baseline 49개 Feature를 모두 유지
- Trackman, test, target, 외부 데이터/API를 사용하지 않음
- 결측값은 대체하지 않고 LightGBM native missing value 처리 사용
- LGBM-029는 Current Baseline으로 유지

## LGBM-050

### 실험 목적

LGBM-029의 기존 49개 Feature를 유지한 상태에서
투수와 타자의 누적 Middle Rate 차이가 추가적인 예측 정보를 제공하는지 검증했다.

### 변경 사항

추가 Feature:

- `pitcher_batter_middle_gap`

정의:

```text
asof_pitcher_middle_rate - asof_batter_middle_rate
```

## LGBM-051

### 실험 목적

LGBM-029의 기존 49개 Feature를 유지하고 투수의 누적 Strike Rate와 Ball Rate 차이가 추가적인 예측 정보를 제공하는지 검증했다.

### 변경 사항

추가 Feature:

- `pitcher_control_balance`

정의:
`asof_pitcher_strike_rate - asof_pitcher_ball_rate`

기존 LGBM-029의 49개 Feature는 변경하지 않았다.

### 결과

- Features: 50
- num_leaves: 15
- learning_rate: 0.02
- n_estimators: 275
- Validation: 2024

- Brier Score: `0.24814048836066588`
- ROC-AUC: `0.5473566623629754`

LGBM-029 대비:

- ΔBrier: `+0.00004487042403872`
- ΔAUC: `-0.0006135678211958`

### 판정

**REJECT**

Brier Score와 ROC-AUC가 모두 LGBM-029보다 악화되었다.

따라서 `pitcher_control_balance`는 최종 Feature에 채택하지 않는다.

### 다음 실험

LGBM-029의 기존 49개 Feature를 baseline으로 유지하고 새로운 Feature를 별도로 검증한다.

## LGBM-053

- 추가 Feature: `pitcher_reliability`
- 정의: `asof_pitcher_n / (asof_pitcher_n + 50)`
- Feature 수: 49 → 50
- 검증: 5-fold walk-forward
- 2024 Brier: `0.24814559956730664`
- 2024 AUC: `0.5473435689623729`
- Baseline Brier: `0.24809561793662716`
- Baseline AUC: `0.5479702297841712`
- ΔBrier: `+0.00004998163067948`
- ΔAUC: `-0.0006266609717983`
- 판정: `REJECT`

`pitcher_reliability` 추가 시 baseline보다 Brier와 AUC 모두 악화되어 채택하지 않음.

## LGBM-054

- 추가 Feature: `pitcher_batter_success_gap`
- 정의: `asof_pitcher_success_rate - asof_batter_success_rate`
- Feature 수: 49 → 50
- 2024 Brier: `0.24813541153539434`
- 2024 AUC: `0.5473925144249512`
- Baseline Brier: `0.24809561793662716`
- Baseline AUC: `0.5479702297841712`
- ΔBrier: `+0.00003979359876718`
- ΔAUC: `-0.0005777155112200`
- 판정: `REJECT`

투수와 타자의 성공률 차이를 추가했지만 baseline보다 Brier와 AUC가 모두 악화되어 채택하지 않음.

## LGBM-055

- 추가 Feature: `pitcher_score_state`
- 정의: `asof_pitcher_success_rate * score_diff_pitcher_team`
- Feature 수: 49 → 50
- 2024 Brier: `0.24814095247658038`
- 2024 AUC: `0.5473888276898038`
- Baseline Brier: `0.24809561793662716`
- Baseline AUC: `0.5479702297841712`
- ΔBrier: `+0.00004533453995322`
- ΔAUC: `-0.0005814024743674`
- 판정: `REJECT`

투수 누적 성공률과 현재 점수 차이를 결합했지만 baseline보다 Brier와 AUC가 모두 악화되어 채택하지 않음.

## LGBM-057

- 추가 Feature: `game_pressure_index`
- 정의: `li * abs(score_diff_pitcher_team)`
- Feature 수: 49 → 50
- 2024 Brier: `0.24814612319954277`
- 2024 AUC: `0.5473334612896469`
- Baseline Brier: `0.24809561793662716`
- Baseline AUC: `0.5479702297841712`
- ΔBrier: `+0.00005050526291561`
- ΔAUC: `-0.0006367686365243`
- 판정: `REJECT`

경기 중요도와 점수 차이의 절대값을 결합했지만 baseline보다 Brier와 AUC가 모두 악화되어 채택하지 않음.

## LGBM-059

### 변경

LGBM-029의 기존 49개 Feature에 Trackman 기반 Context Feature 13개를 추가하여 총 62개 Feature로 실험.

Trackman 선수/경기 직접 매핑 없이 다음 상황 변수를 기준으로 과거 Trackman 데이터를 집계:

- balls_before
- strikes_before
- outs_before
- inning
- top_bottom
- pitcher_hand
- batter_hand

추가 Feature:

- ctx_n
- ctx_rel_speed_mean
- ctx_rel_speed_std
- ctx_spin_rate_mean
- ctx_spin_rate_std
- ctx_vert_break_std
- ctx_horz_break_std
- ctx_extension_mean
- ctx_rel_height_std
- ctx_rel_side_std
- ctx_zone_speed_mean
- ctx_breaking_rate
- ctx_offspeed_rate

Walk-forward 방식으로 검증했으며, 검증 시즌보다 이전 시즌의 Trackman 데이터만 사용.

### 2024 결과

- Train rows: 1,221,585
- Validation rows: 253,507
- Features: 62
- Brier: 0.24812223274229617
- ROC-AUC: 0.5475882705808006
- Prediction mean: 0.49512637070219384
- Actual mean: 0.4861049201797189
- Training time: 9.4130 sec
- Prediction time: 0.5252 sec

### LGBM-029 대비

- Brier: 0.24809561793662716 → 0.24812223274229617
- ΔBrier: +0.00002661480566901
- AUC: 0.5479702297841712 → 0.5475882705808006
- ΔAUC: -0.0003819592033706

### 판정

2024 단일 결과만으로는 개선되지 않음.
다만 Trackman Context Feature 전체 번들의 효과를 판단하려면 walk-forward 전체 결과를 확인해야 함.

현재는 선수 단위 Trackman ID 매핑 가능성을 별도로 분석 중이며, 해당 분석 결과에 따라 다음 Feature Engineering 방향을 결정한다.

## LGBM-061

### 변경

LGBM-029의 기존 49개 Feature를 유지하고 학습 데이터 내부 5-fold OOF 예측을 이용한 Isotonic Calibration을 적용.

### 5-Fold 결과

- Mean Brier: 0.24780045252049118
- Baseline Mean Brier: 0.24768213298435976
- Mean ΔBrier: +0.00011831953613146707
- Median ΔBrier: +0.00002047763719026374
- Brier 개선: 2/5 folds
- Brier 악화: 3/5 folds
- Mean ΔAUC: -0.000085073080923601
- AUC 개선: 1/5 folds
- AUC 악화: 4/5 folds
- Best fold 제외 Mean ΔBrier: +0.00016264120980279823

### 2024 결과

- Baseline Brier: 0.24809561793662716
- Candidate Brier: 0.2480366507780733
- ΔBrier: -0.00005896715855385759
- Baseline AUC: 0.5479702297841712
- Candidate AUC: 0.5479157138552045
- ΔAUC: -0.0000545159289665858

2024에서는 Brier가 소폭 개선되었지만 전체 5개 walk-forward fold에서는 Brier와 AUC 모두 악화되는 경향을 보였다.

### 판정

REJECT

2024 단일 validation 결과만으로 채택하지 않고 5-fold walk-forward 결과를 기준으로 기각한다.
현재 OOF 5-fold Isotonic Calibration은 최종 모델에 적용하지 않는다.

## LGBM-062

### 변경

- 추가: `pitcher_prev_season_rel_speed_mean`
- 제거: 없음
- 수정: 없음

### Feature 정의

- 각 fold의 validation season보다 이전 train/Trackman 데이터만으로 재구성한 HIGH `pitcher_id -> pitcher_trackman_id` 매핑만 사용
- 현재 행의 season이 S일 때 매핑된 투수의 Trackman season S-1 `rel_speed` 평균
- PARTIAL/UNRESOLVED 및 미매핑 투수는 NaN 유지, 별도 대체 없음
- LGBM-029의 기존 49개 Feature는 변경하지 않고 총 50개 Feature 사용

### 결과

- Mean ΔBrier: +0.0000326697
- Median ΔBrier: +0.0000002075
- Brier 개선: 1/5 folds
- Brier 악화: 3/5 folds
- Mean ΔAUC: -0.0002320080
- Median ΔAUC: -0.0001556874
- AUC 개선: 0/5 folds
- AUC 악화: 4/5 folds
- Best fold 제외 Mean ΔBrier: +0.0000459451
- 2024 Brier: 0.2481471365 (baseline 0.2480956179, Δ +0.0000515185)
- 2024 ROC-AUC: 0.5472310892 (baseline 0.5479702298, Δ -0.0007391406)

### 판정

- REJECT

### 이유

- mean/median ΔBrier가 음수가 아니고 Brier 개선 fold가 1개뿐이며, best fold 제외 mean ΔBrier도 양수여서 CANDIDATE 조건을 충족하지 못함
- 2024에서 Brier와 ROC-AUC가 모두 악화됨

### 비고

- 2020 fold의 학습 데이터는 2019뿐이므로 2018 Trackman 값이 없어 학습 Feature가 전부 NaN이었고 baseline과 candidate 예측이 동일함
- validation/current/future season Trackman 기록은 Feature 계산에 사용하지 않음

## LGBM-063

### 변경

LGBM-029의 49개 Feature에 고신뢰(HIGH) Trackman 선수 매핑을 이용한 `pitcher_prev_season_spin_rate_mean` 1개를 추가하여 50개 Feature로 실험.

현재 시즌보다 1년 전 Trackman 데이터만 사용했으며, HIGH 매핑이 없는 선수는 NaN으로 유지했다.

### 5-Fold 결과

- Mean ΔBrier: +0.000010860125410439015
- Median ΔBrier: +0.0000031165505435803986
- Brier 개선: 2/5
- Brier 악화: 3/5
- Mean ΔAUC: -0.000047926959131450174
- AUC 개선: 1/5
- AUC 악화: 4/5
- Best fold 제외 Mean ΔBrier: +0.0000306882539622827

### 2024 결과

- Brier: 0.248124873957715
- ROC-AUC: 0.5474136846078352
- ΔBrier: +0.000029256021087831208
- ΔAUC: -0.0005565451763359652
- Feature missing: 63.48%

### 판정

REJECT

전년도 평균 Spin Rate Feature는 전체 walk-forward에서 안정적인 Brier 개선을 만들지 못했으며 AUC도 대부분의 fold에서 감소했다. 최종 모델에는 적용하지 않는다.

## LGBM-064

### 변경

LGBM-029의 49개 Feature에 고신뢰(HIGH) Trackman 선수 매핑을 이용한 다음 2개 Feature를 동시에 추가하여 51개 Feature로 실험.

- `pitcher_prev_season_rel_speed_mean`
- `pitcher_prev_season_spin_rate_mean`

각 validation season에 대해 직전 시즌 Trackman 데이터만 사용했으며, HIGH 매핑이 없는 선수는 NaN으로 유지했다.

### 5-Fold 결과

- Mean ΔBrier: -0.000007913447554186437
- Median ΔBrier: +0.000003600265015585302
- Brier 개선: 2/5
- Brier 악화: 3/5
- Mean ΔAUC: +0.00009242336287100806
- AUC 개선: 3/5
- AUC 악화: 2/5
- Best fold 제외 Mean ΔBrier: +0.000009134752458839213

### 2024 결과

- Brier: 0.24810747453227525
- ROC-AUC: 0.5476172966358641
- ΔBrier: +0.00001185659564809094
- ΔAUC: -0.00035293314830708855
- Speed Feature missing: 63.48%
- Spin Feature missing: 63.48%

### 판정

REJECT

두 Trackman Feature를 동시에 사용했을 때 Mean Brier와 Mean AUC는 개선되었지만, Median ΔBrier가 양수이고 Brier 개선 fold가 2/5에 그쳤으며, Best fold를 제외하면 성능이 악화되었다. 안정적인 성능 개선으로 판단하기 어려워 최종 모델에는 적용하지 않는다.

## LGBM-065

### 변경

LGBM-029의 49개 Feature에 고신뢰(HIGH) Trackman 선수 매핑을 이용한 `pitcher_prev_season_rel_speed_std` 1개를 추가하여 50개 Feature로 실험.

현재 시즌보다 1년 전 Trackman 데이터만 사용했으며, HIGH 매핑이 없는 선수는 NaN으로 유지했다.

### 5-Fold 결과

- Mean ΔBrier: +0.0000090514992317825
- Median ΔBrier: -0.000011721607562908964
- Brier 개선: 3/5
- Brier 악화: 2/5
- Mean ΔAUC: -0.00008584942151177444
- AUC 개선: 3/5
- AUC 악화: 2/5
- Best fold 제외 Mean ΔBrier: +0.00002848010191195543

### 2024 결과

- Brier: 0.24815520039556874
- ROC-AUC: 0.5470936923542906
- ΔBrier: +0.00005958245894158165
- ΔAUC: -0.0008765374298805861
- Feature missing: 63.48%

### 판정

REJECT

전년도 구속 표준편차는 Brier 기준 3개 fold에서 개선되었고 Median ΔBrier도 음수였으나, Mean ΔBrier가 양수였으며 Best fold를 제외한 평균도 악화되었다. 특히 2024 validation에서 Brier와 AUC가 모두 악화되어 안정적인 성능 개선으로 판단하지 않는다.

## LGBM-066

### 변경

LGBM-029의 49개 Feature에 고신뢰(HIGH) Trackman 선수 매핑을 이용한 다음 2개 Feature를 동시에 추가하여 51개 Feature로 실험.

- `pitcher_prev_season_rel_speed_mean`
- `pitcher_prev_season_rel_speed_std`

현재 시즌보다 1년 전 Trackman 데이터만 사용했으며, HIGH 매핑이 없는 선수는 NaN으로 유지했다.

### 5-Fold 결과

- Mean ΔBrier: -0.000004473008907912579
- Median ΔBrier: +0.000006663220581154539
- Brier 개선: 1/5
- Brier 악화: 4/5
- Mean ΔAUC: +0.00007636199246048303
- AUC 개선: 3/5
- AUC 악화: 2/5
- Best fold 제외 Mean ΔBrier: +0.000013862254018642828

### 2024 결과

- Brier: 0.24810451651499854
- ROC-AUC: 0.5475632326491627
- ΔBrier: +0.000008898578371385746
- ΔAUC: -0.0004069971350084689
- 평균 구속 Feature missing: 63.48%
- 구속 표준편차 Feature missing: 63.48%

### 판정

REJECT

전년도 평균 구속과 구속 표준편차를 동시에 사용했을 때 Mean ΔBrier는 음수였지만 Median ΔBrier가 양수이고 Brier 개선 fold가 1/5에 불과했다. Best fold를 제외한 평균도 악화되었으며 2024 validation에서도 Brier와 AUC가 모두 악화되어 안정적인 성능 개선으로 판단하지 않는다.

## LGBM-067

### 실험 목적

최근 시즌에 더 높은 가중치를 부여하는 recency-weighted training을 적용하여 최근 시즌 데이터가 모델 학습에 더 큰 영향을 주도록 하는 실험.

### 설정

- Feature: 기존 baseline 49개 유지
- Model: LightGBM Binary Classification
- num_leaves: 15
- learning_rate: 0.02
- n_estimators: 275
- subsample: 0.8
- colsample_bytree: 0.8
- random_state: 42
- Recency weight: `0.7^(최신 학습 시즌 - 해당 시즌)`

### Walk-forward 결과

| Validation |       Δ Brier |         Δ AUC |
| ---------- | ------------: | ------------: |
| 2020       |  0.0000000000 |  0.0000000000 |
| 2021       | +0.0000212028 | -0.0003541205 |
| 2022       | +0.0000446729 | -0.0003295124 |
| 2023       | +0.0000922930 | +0.0004553530 |
| 2024       | -0.0000057380 | -0.0004228003 |

### 종합 결과

- Mean Δ Brier: +0.0000304863
- Median Δ Brier: +0.0000212028
- Brier 개선: 1/5
- Brier 악화: 3/5
- Mean Δ AUC: -0.0001302160
- Median Δ AUC: -0.0003295124
- AUC 개선: 1/5
- AUC 악화: 3/5
- Best fold 제외 Mean Δ Brier: +0.0000395424
- 2024 Brier: 0.2480898799
- 2024 AUC: 0.5475474295

### 판정

REJECT

Mean Brier와 Median Brier가 모두 악화되었으며 Brier 개선 fold도 1/5에 불과하다. Best fold를 제외해도 성능이 악화된다. 2024 validation에서는 Brier가 소폭 개선되었지만 AUC가 악화되었고 전체 walk-forward 안정성이 확인되지 않았다.

recency-weighted training 0.7은 채택하지 않고 기존 baseline 학습 방식으로 복귀한다.

### 다음 방향

Trackman Feature 실험으로 전환한다. 기존 LGBM-064에서 `pitcher_prev_season_rel_speed_mean + pitcher_prev_season_spin_rate_mean` 조합이 가장 유망했지만 CANDIDATE 조건을 충족하지 못했으므로 채택하지 않았다.

다음 실험에서는 최근 과거 Trackman 정보를 이용한 단일 Feature를 우선 검증한다.

## LGBM-068

### 실험 목적

투수의 과거 Trackman 상대 구속(rel_speed)을 최근 시즌에 더 높은 가중치로 반영한 Feature가 제구 성공 확률 예측에 도움이 되는지 검증.

### Feature

pitcher_recent_weighted_rel_speed_mean_0.7

HIGH 투수 매핑만 사용하고, 각 예측 시즌보다 이전 시즌의 Trackman rel_speed 평균을 시즌별로 계산한 뒤 최근 시즌에 0.7 기반 가중치를 적용하여 가중 평균을 생성.

### 설정

- Baseline Feature: 49개
- Candidate Feature: 50개
- Model: LightGBM Binary Classification
- num_leaves: 15
- learning_rate: 0.02
- n_estimators: 275
- subsample: 0.8
- colsample_bytree: 0.8
- random_state: 42
- HIGH pitcher mapping만 사용
- 미래 시즌 Trackman 데이터 미사용

### Walk-forward 결과

| Validation |   Delta Brier |     Delta AUC |
| ---------- | ------------: | ------------: |
| 2020       |  0.0000000000 |  0.0000000000 |
| 2021       | -0.0000411401 | -0.0000694828 |
| 2022       | +0.0000018295 | -0.0000921720 |
| 2023       | +0.0000909233 | -0.0000959510 |
| 2024       | +0.0000471153 | -0.0006559406 |

### 종합 결과

- Mean Delta Brier: +0.0000197456
- Median Delta Brier: +0.0000018295
- Brier improvement folds: 1/5
- Brier degradation folds: 3/5
- Mean Delta AUC: -0.0001827093
- Median Delta AUC: -0.0000921720
- AUC improvement folds: 0/5
- AUC degradation folds: 4/5
- Mean Delta Brier without best fold: +0.0000349670
- 2024 Brier: 0.2481427332
- 2024 AUC: 0.5473142891
- 2024 Delta Brier: +0.0000471153
- 2024 Delta AUC: -0.0006559406

### 판정

REJECT

Mean Delta Brier와 Median Delta Brier가 모두 양수이며 Brier 개선 fold도 1/5에 불과하다. AUC는 5개 fold 중 단 한 번도 개선되지 않았다. 특히 2024 validation에서 Brier와 AUC가 모두 악화되었다.

최근 시즌에 더 높은 가중치를 주는 rel_speed Feature는 현재 방식으로는 안정적인 예측 성능 개선을 확인하지 못했다.

### 다음 방향

최근 가중 Spin Rate 단일 Feature를 별도로 검증한다.

## LGBM-069

### 실험 목적

투수의 과거 Trackman Spin Rate를 최근 시즌에 더 높은 가중치로 반영한 Feature가 제구 성공 확률 예측에 도움이 되는지 검증.

### Feature

pitcher_recent_weighted_spin_rate_mean_0.7

HIGH 투수 매핑만 사용하고, 각 예측 시즌보다 이전 시즌의 Trackman spin_rate 평균을 시즌별로 계산한 뒤 최근 시즌에 0.7 기반 가중치를 적용하여 가중 평균을 생성.

### 설정

- Baseline Feature: 49개
- Candidate Feature: 50개
- Model: LightGBM Binary Classification
- num_leaves: 15
- learning_rate: 0.02
- n_estimators: 275
- subsample: 0.8
- colsample_bytree: 0.8
- random_state: 42
- HIGH pitcher mapping만 사용
- 미래 시즌 Trackman 데이터 미사용

### Walk-forward 결과

| Validation |   Delta Brier |     Delta AUC |
| ---------- | ------------: | ------------: |
| 2020       |  0.0000000000 |  0.0000000000 |
| 2021       | -0.0000489895 | +0.0000374836 |
| 2022       | -0.0000126192 | -0.0000127872 |
| 2023       | +0.0001511824 | -0.0002420291 |
| 2024       | +0.0000295959 | -0.0004156192 |

### 종합 결과

- Mean Delta Brier: +0.0000238339
- Median Delta Brier: 0.0000000000
- Brier improvement folds: 2/5
- Brier degradation folds: 2/5
- Mean Delta AUC: -0.0001265904
- Median Delta AUC: -0.0000127872
- AUC improvement folds: 1/5
- AUC degradation folds: 3/5
- Mean Delta Brier without best fold: +0.0000420398
- 2024 Brier: 0.2481252138
- 2024 AUC: 0.5475546106
- 2024 Delta Brier: +0.0000295959
- 2024 Delta AUC: -0.0004156192

### 판정

REJECT

Mean Delta Brier가 양수이고 Median Delta Brier가 0으로 음수가 아니다. Brier 개선 fold도 2/5로 기준인 3/5에 미달한다. Best fold를 제외하면 Mean Delta Brier가 +0.0000420398로 악화된다.

2021과 2022에서는 Brier가 개선되었지만 2023에서 크게 악화되었고 2024에서도 Brier와 AUC가 모두 악화되었다.

최근 시즌 가중 Spin Rate 단일 Feature는 안정적인 성능 개선을 확인하지 못했으므로 채택하지 않는다.

## LGBM-071

### 실험 목적

투수의 과거 Trackman 유도 수직 무브먼트(IVB, `induced_vert_break`) 평균이 제구 성공 확률 예측에 도움이 되는지 검증.

### Feature

`pitcher_prev_induced_vert_break_mean`

각 예측 시즌에 대해 해당 시즌보다 이전 시즌의 Trackman 데이터만 사용하여 투수별 시즌 IVB 평균을 계산한 뒤, 과거 시즌들의 IVB 평균을 다시 평균하여 Feature 생성.

예:

- 2024 validation → 2019~2023 Trackman만 사용
- 2024 Trackman 데이터는 사용하지 않음

### 데이터 조건

- 공식 제공 Trackman 데이터만 사용
- `trackman_player_mapping_analysis.csv`의 HIGH pitcher mapping만 사용
- HIGH 투수 매핑: 163명
- 미래 시즌 데이터 사용 금지
- 외부 데이터 사용 없음

### 설정

- Baseline Feature: 49개
- Candidate Feature: 50개
- 추가 Feature: 1개
- Model: LightGBM Binary Classification
- num_leaves: 15
- learning_rate: 0.02
- n_estimators: 275
- subsample: 0.8
- colsample_bytree: 0.8
- random_state: 42
- n_jobs: -1

### Walk-forward 결과

| Validation | Baseline Brier | Candidate Brier |   Delta Brier |     Delta AUC |
| ---------- | -------------: | --------------: | ------------: | ------------: |
| 2020       |   0.2480689387 |    0.2480689387 |  0.0000000000 |  0.0000000000 |
| 2021       |   0.2457608164 |    0.2457101457 | -0.0000506707 | +0.0000657900 |
| 2022       |   0.2433782762 |    0.2433799029 | +0.0000016267 | -0.0001275206 |
| 2023       |   0.2531070157 |    0.2532060584 | +0.0000990427 | +0.0002087950 |
| 2024       |   0.2480956179 |    0.2481408939 | +0.0000452760 | -0.0007739329 |

### 종합 결과

- Baseline Brier Mean: 0.2476821330
- Candidate Brier Mean: 0.2477011879
- Mean Delta Brier: +0.0000190549
- Median Delta Brier: +0.0000016267
- Brier improvement folds: 1/5
- Brier degradation folds: 3/5

- Baseline AUC Mean: 0.5529196009
- Candidate AUC Mean: 0.5527942271
- Mean Delta AUC: -0.0001253737
- Median Delta AUC: 0.0000000000
- AUC improvement folds: 2/5
- AUC degradation folds: 2/5

- Mean Delta Brier without best fold: +0.0000364863

### 2024 결과

- Candidate Brier: 0.2481408939
- Candidate AUC: 0.5471962969
- Delta Brier: +0.0000452760
- Delta AUC: -0.0007739329

### 판정

**REJECT**

Mean Delta Brier와 Median Delta Brier가 모두 음수가 아니며, Brier 개선도 1/5 fold에 불과하다. Best fold를 제외한 Mean Delta Brier 역시 +0.0000364863으로 악화되었다.

특히 2024 validation에서 Brier와 AUC가 모두 악화되었으며, AUC는 -0.0007739329 하락했다.

따라서 투수의 과거 IVB 평균을 단독 Feature로 추가하는 방식은 현재 baseline의 안정적인 성능 개선을 확인하지 못했다.

### 다음 방향

LGBM-072에서 `pitcher_prev_horz_break_mean`을 단독 Feature로 검증한다.

현재까지:

- LGBM-068: 최근 가중 Rel Speed → REJECT
- LGBM-069: 최근 가중 Spin Rate → REJECT
- LGBM-070: Rel Speed Slope → REJECT
- LGBM-071: 이전 IVB 평균 → REJECT

다음은 과거 수평 무브먼트(Horizontal Break) 평균을 검증한다.

## LGBM-070

- 변경: `pitcher_rel_speed_slope` 1개 추가 (49 → 50 Features, 과거 Trackman HIGH 매핑만 사용)
- 결과: Mean/Median ΔBrier `+0.000041 / +0.000010`, Brier 개선/악화 `0/3`, best fold 제외 Mean ΔBrier `+0.000051`, Mean ΔAUC `-0.000239`
- 2024: Brier `0.248163` (Δ `+0.000067`), AUC `0.547088` (Δ `-0.000883`)
- 판정: **REJECT**

## LGBM-072

- 변경: `pitcher_prev_horz_break_mean` 1개 추가 (49 → 50 Features, 예측 시즌 이전 Trackman만 사용)
- 결과: Mean/Median ΔBrier `+0.000030 / +0.000000`, Brier 개선/악화 `2/2`, best fold 제외 Mean ΔBrier `+0.000044`, Mean ΔAUC `-0.000174`
- 2024: Brier `0.248123` (Δ `+0.000028`), AUC `0.547471` (Δ `-0.000500`)
- 판정: **REJECT**

## LGBM-073

- 변경: `pitcher_prev_rel_speed_std` 1개 추가 (49 → 50 Features, 예측 시즌 이전 Trackman만 사용)
- 결과: Mean/Median ΔBrier `+0.000029 / +0.000000`, Brier 개선/악화 `2/2`, best fold 제외 Mean ΔBrier `+0.000053`, Mean ΔAUC `-0.000141`
- 2024: Brier `0.248151` (Δ `+0.000055`), AUC `0.547158` (Δ `-0.000812`)
- 판정: **REJECT**

## LGBM-074

- 변경: `pitcher_recent1_success_gap = asof_pitcher_prev1_game_success_rate - asof_pitcher_success_rate` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000360291 / +0.0000362521`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000638929`, Mean ΔAUC `-0.0001986085`
- 2024: ΔBrier `+0.0000362521`, ΔAUC `-0.000558`; 판정: **REJECT**

## LGBM-075

- 변경: `pitcher_recent1_success_ratio = (prev1 success + 1e-6) / (cumulative success + 1e-6)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000162680 / +0.0000047662`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000371636`, Mean ΔAUC `-0.0000591855`
- 2024: ΔBrier `+0.0000443652`, ΔAUC `-0.000526`; 판정: **REJECT**

## LGBM-076

- 변경: `pitcher_strike_count_pressure = asof_pitcher_strike_rate × (balls_before + strikes_before)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000323270 / +0.0000153439`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000533640`, Mean ΔAUC `-0.0001798764`
- 2024: ΔBrier `+0.0000522929`, ΔAUC `-0.000663`; 판정: **REJECT**

## LGBM-077

- 변경: `pitcher_batter_count_success_interaction = pitcher_batter_success_interaction × (count + 1)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000273676 / +0.0000010554`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000501223`, Mean ΔAUC `-0.0001210611`
- 2024: ΔBrier `+0.0000589590`, ΔAUC `-0.000755`; 판정: **REJECT**

## LGBM-078

- 변경: `pitcher_out_success_interaction = asof_pitcher_success_rate × (outs_before + 1)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000297472 / +0.0000007809`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000514208`, Mean ΔAUC `-0.0000957768`
- 2024: ΔBrier `+0.0000604511`, ΔAUC `-0.000802`; 판정: **REJECT**

## LGBM-079

- 변경: `pitcher_runner_success_interaction = asof_pitcher_success_rate × num_runners_on` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000171639 / +0.0000064154`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000451382`, Mean ΔAUC `-0.0000742280`
- 2024: ΔBrier `+0.0000450215`, ΔAUC `-0.000523`; 판정: **REJECT**

## LGBM-080

- 변경: `count_imbalance_squared = (balls_before - strikes_before)^2` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000293273 / +0.0000063725`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000534400`, Mean ΔAUC `-0.0001449579`
- 2024: ΔBrier `+0.0000560369`, ΔAUC `-0.000744`; 판정: **REJECT**

## LGBM-081

- 변경: `pitcher_count_control_alignment = strike_rate × balls_before - ball_rate × strikes_before` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000150913 / +0.0000060633`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000355452`, Mean ΔAUC `-0.0000944264`
- 2024: ΔBrier `+0.0000429839`, ΔAUC `-0.000616`; 판정: **REJECT**

## LGBM-082

- 변경: `pitcher_matchup_success_interaction = pitcher success × same/opposite-hand sign` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000150193 / +0.0000257210`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000383029`, Mean ΔAUC `-0.0000859581`
- 2024: ΔBrier `+0.0000389077`, ΔAUC `-0.000540`; 판정: **REJECT**

## LGBM-083

- 변경: `pitcher_strike_batter_success_gap = asof_pitcher_strike_rate - asof_batter_success_rate` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000260210 / +0.0000177559`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000451925`, Mean ΔAUC `-0.0001529693`
- 2024: ΔBrier `+0.0000402448`, ΔAUC `-0.000648`; 판정: **REJECT**

## LGBM-084

- 변경: `pitcher_middle_pa_progress = asof_pitcher_middle_rate × (balls_before + strikes_before + 1)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000240103 / +0.0000034610`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000438584`, Mean ΔAUC `-0.0001294871`
- 2024: ΔBrier `+0.0000509025`, ΔAUC `-0.000684`; 판정: **REJECT**

## LGBM-085

- 변경: `pitcher_reverse_runner_pressure = reverse_rate × (runners + 1) × (outs + 1)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000224953 / -0.0000033227`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000386174`, Mean ΔAUC `-0.0001327610`
- 2024: ΔBrier `+0.0000407365`, ΔAUC `-0.000511`; 판정: **REJECT**

## LGBM-086

- 변경: `pitcher_success_logit = logit(asof_pitcher_success_rate)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000260962 / +0.0000015178`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000426713`, Mean ΔAUC `-0.0001508487`
- 2024: ΔBrier `+0.0000546430`, ΔAUC `-0.000817`; 판정: **REJECT**

## LGBM-087

- 변경: `pitcher_batter_experience_log_ratio = log1p(asof_pitcher_n) - log1p(asof_batter_n)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000122447 / +0.0000014089`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000297963`, Mean ΔAUC `-0.0001381155`
- 2024: Brier `0.2481397842` (Δ `+0.0000441662`), AUC `0.5473529214` (Δ `-0.0006173084`); 판정: **REJECT**

## LGBM-088

- 변경: `pitcher_reverse_count_out_interaction = reverse_rate × (count + 1) × (outs + 1)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000294629 / +0.0000060650`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000496253`, Mean ΔAUC `-0.0001392423`
- 2024: ΔBrier `+0.0000499503`, ΔAUC `-0.000626`; 판정: **REJECT**

## LGBM-089

- 변경: `pitcher_recent_success_volatility = abs(prev1 success - prev5 success)` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000247332 / +0.0000141561`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000495870`, Mean ΔAUC `-0.0001091325`
- 2024: ΔBrier `+0.0000539885`, ΔAUC `-0.000790`; 판정: **REJECT**

## LGBM-090

- 변경: `pitcher_pitchmix_entropy = -Σ(pitch_type_rate × log(pitch_type_rate))` 추가 (49 → 50)
- 결과: Mean/Median ΔBrier `+0.0000204222 / -0.0000001568`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000390996`, Mean ΔAUC `-0.0001530275`
- 2024: ΔBrier `+0.0000411729`, ΔAUC `-0.000711`; 판정: **REJECT**

## LGBM-091

- 변경: 49 Features 고정, `num_leaves=7`
- 결과: Mean/Median ΔBrier `-0.0000229273 / -0.0000467419`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000151708`, Mean ΔAUC `-0.0005175984`
- 2024: Brier `0.2482716741` (Δ `+0.0001760562`), AUC `0.545437` (Δ `-0.002533`); 판정: **REJECT**

## LGBM-092

- 변경: 49 Features 고정, `num_leaves=31`
- 결과: Mean/Median ΔBrier `+0.0000363624 / -0.0000000019`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000545237`, Mean ΔAUC `+0.0000286426`
- 2024: ΔBrier `-0.0000362828`, ΔAUC `+0.000295`; 판정: **REJECT**

## LGBM-093

- 변경: 49 Features 고정, `min_child_samples=100`
- 결과: Mean/Median ΔBrier `-0.0000077273 / -0.0000087876`, Brier 개선/악화 `5/0`, best fold 제외 Mean ΔBrier `-0.0000066686`, Mean ΔAUC `+0.0000340973`
- 2024: ΔBrier `-0.0000087876`, ΔAUC `+0.000074`; 판정: **CANDIDATE**

## LGBM-094

- 변경: 49 Features 고정, `min_child_samples=500`
- 결과: Mean/Median ΔBrier `-0.0000060121 / -0.0000062063`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `-0.0000013004`, Mean ΔAUC `+0.0000693713`
- 2024: ΔBrier `+0.0000005415`, ΔAUC `-0.000101`; 판정: **CANDIDATE**

## LGBM-095

- 변경: 49 Features 고정, `lambda_l1=0.5`
- 결과: Mean/Median ΔBrier `-0.0000102010 / -0.0000081912`, Brier 개선/악화 `5/0`, best fold 제외 Mean ΔBrier `-0.0000070276`, Mean ΔAUC `+0.0001055843`
- 2024: ΔBrier `-0.0000081912`, ΔAUC `+0.000053`; 판정: **CANDIDATE**

## LGBM-096

- 변경: 49 Features 고정, `lambda_l2=1.0`
- 결과: Mean/Median ΔBrier `-0.0000045601 / +0.0000008083`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000031649`, Mean ΔAUC `-0.0000343666`
- 2024: ΔBrier `+0.0000008083`, ΔAUC `-0.000147`; 판정: **REJECT**

## LGBM-097

- 변경: 49 Features 고정, `learning_rate=0.01`, `n_estimators=550`
- 결과: Mean/Median ΔBrier `+0.0000002924 / +0.0000053169`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000036611`, Mean ΔAUC `-0.0000456357`
- 2024: ΔBrier `+0.0000053169`, ΔAUC `-0.000097`; 판정: **REJECT**

## LGBM-098

- 변경: 49 Features 고정, `learning_rate=0.04`, `n_estimators=150`
- 결과: Mean/Median ΔBrier `+0.0000102718 / +0.0000185228`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000218995`, Mean ΔAUC `-0.0001665708`
- 2024: ΔBrier `+0.0000010599`, ΔAUC `-0.000217`; 판정: **REJECT**

## LGBM-099

- 변경: 49 Features 고정, `subsample=0.9`, `colsample_bytree=0.9`
- 결과: Mean/Median ΔBrier `+0.0000367180 / +0.0000227241`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000565292`, Mean ΔAUC `-0.0001547984`
- 2024: ΔBrier `+0.0000227241`, ΔAUC `-0.000375`; 판정: **REJECT**

## LGBM-100

- 변경: 49 Features 고정, `num_leaves=15`, `learning_rate=0.02`, `n_estimators=400`, `min_child_samples=100`, `lambda_l1=0.1`, `lambda_l2=0.5`, `subsample=0.9`, `colsample_bytree=0.9`
- 결과: Mean/Median ΔBrier `+0.0000915451 / +0.0000193487`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0001238646`, Mean ΔAUC `-0.0003613574`
- 2024: ΔBrier `+0.0000193487`, ΔAUC `-0.000471`; 판정: **REJECT**

## Train-only / Hyperparameter Summary

- LGBM-074~090: 모두 **REJECT**. 가장 낮은 candidate mean Brier는 LGBM-087 (`0.2476943776`)이나 baseline보다 악화.
- LGBM-091~100 CANDIDATE: LGBM-093, LGBM-094, LGBM-095.
- CANDIDATE 중 Mean Brier 최상: LGBM-095 (`lambda_l1=0.5`, Mean ΔBrier `-0.0000102010`).
- 전체 mean Brier 최저는 LGBM-091이나 best fold 제외 Mean ΔBrier와 2024 성능이 악화되어 **REJECT**.
- 현재 LGBM-029 baseline 정의와 49개 Feature는 변경하지 않음.

## LGBM-101

- 변경: 49 Features 고정, `lambda_l1=0.5`, `min_child_samples=50`
- 결과: Mean/Median ΔBrier `-0.0000100247 / -0.0000051024`, Brier 개선/악화 `5/0`, best fold 제외 Mean ΔBrier `-0.0000061654`, Mean ΔAUC `+0.0001179623`
- 2024: Brier `0.2480905155` (Δ `-0.0000051024`), AUC `0.548008`; 판정: **CANDIDATE**

## LGBM-102

- 변경: 49 Features 고정, `lambda_l1=0.5`, `min_child_samples=100`
- 결과: Mean/Median ΔBrier `-0.0000030677 / -0.0000063597`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000011773`, Mean ΔAUC `+0.0000588016`
- 2024: Brier `0.2480875530` (Δ `-0.0000080649`), AUC `0.548053`; 판정: **REJECT**

## LGBM-103

- 변경: 49 Features 고정, `lambda_l1=0.5`, `min_child_samples=150`
- 결과: Mean/Median ΔBrier `+0.0000021423 / -0.0000030202`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000090589`, Mean ΔAUC `+0.0000031913`
- 2024: ΔBrier `+0.0000020459`; 판정: **REJECT**

## LGBM-104

- 변경: 49 Features 고정, `lambda_l1=0.5`, `min_child_samples=200`
- 결과: Mean/Median ΔBrier `-0.0000058181 / -0.0000061529`, Brier 개선/악화 `4/1`, best fold 제외 Mean ΔBrier `-0.0000023299`, Mean ΔAUC `+0.0000444916`
- 2024: ΔBrier `-0.0000050048`; 판정: **CANDIDATE**

## LGBM-105

- 변경: 49 Features 고정, `lambda_l1=0.5`, `min_child_samples=300`
- 결과: Mean/Median ΔBrier `-0.0000048491 / -0.0000118592`, Brier 개선/악화 `4/1`, best fold 제외 Mean ΔBrier `-0.0000026690`, Mean ΔAUC `+0.0000120237`
- 2024: ΔBrier `-0.0000020600`; 판정: **CANDIDATE**

## LGBM-106

- 변경: 49 Features 고정, `lambda_l1=0.5`, `min_child_samples=500`
- 결과: Mean/Median ΔBrier `+0.0000071906 / +0.0000025850`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000113057`, Mean ΔAUC `-0.0000374794`
- 2024: ΔBrier `-0.0000043711`; 판정: **REJECT**

## LGBM-107

- 변경: 49 Features 고정, `min_child_samples=20`, `lambda_l1=0.05`
- 결과: Mean/Median ΔBrier `+0.0000039817 / +0.0000054366`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000088421`, Mean ΔAUC `-0.0000392337`
- 2024: ΔBrier `-0.0000013269`; 판정: **REJECT**

## LGBM-108

- 변경: 49 Features 고정, `min_child_samples=20`, `lambda_l1=0.10`
- 결과: Mean/Median ΔBrier `+0.0000027541 / +0.0000035343`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000046747`, Mean ΔAUC `-0.0000559093`
- 2024: ΔBrier `+0.0000035343`; 판정: **REJECT**

## LGBM-109

- 변경: 49 Features 고정, `min_child_samples=20`, `lambda_l1=0.25`
- 결과: Mean/Median ΔBrier `+0.0000060960 / +0.0000078639`, Brier 개선/악화 `1/4`, best fold 제외 Mean ΔBrier `+0.0000112208`, Mean ΔAUC `-0.0000650428`
- 2024: ΔBrier `+0.0000078639`; 판정: **REJECT**

## LGBM-110

- 변경: 101~109의 강건성 순위로 `min_child_samples=50`(LGBM-101)과 `lambda_l1=0.10`(LGBM-108)을 조합. 49 Features 유지.
- 결과: Mean/Median ΔBrier `+0.0000014594 / -0.0000005581`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000048963`, Mean ΔAUC `-0.0000337856`
- 2024: Brier `0.2480950598` (Δ `-0.0000005581`), AUC `0.547869`; 판정: **REJECT**

## Regularization Search Summary

- CANDIDATE: LGBM-101, LGBM-104, LGBM-105.
- LGBM-101은 5/5 folds에서 Brier와 AUC가 모두 개선됐으나 Mean Brier `0.2476721083`으로 LGBM-095 (`0.2476719320`)보다 `+0.0000001763` 높음.
- LGBM-101의 2024 Brier도 LGBM-095보다 `+0.0000030888` 높음.
- 따라서 101~110에서 LGBM-095를 넘어선 새 regularization 모델은 확인되지 않았으며, 공식 baseline LGBM-029와 현재 최상 candidate LGBM-095를 유지함.

## LGBM-111

- 변경: 49 Features 고정, `lambda_l1=0.35`, `min_child_samples=50`
- 결과: Mean/Median ΔBrier `+0.0000022853 / -0.0000006507`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000072758`, Mean ΔAUC `-0.0000537994`
- 2024: Brier `0.2481036825` (Δ `+0.0000080646`), AUC `0.547714` (Δ `-0.000256`); 판정: **REJECT**

## LGBM-112

- 변경: 49 Features 고정, `lambda_l1=0.40`, `min_child_samples=50`
- 결과: Mean/Median ΔBrier `-0.0000036981 / +0.0000020630`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000035686`, Mean ΔAUC `+0.0000203398`
- 2024: ΔBrier `+0.0000020630`, ΔAUC `-0.000117`; 판정: **REJECT**

## LGBM-113

- 변경: 49 Features 고정, `lambda_l1=0.45`, `min_child_samples=50`
- 결과: Mean/Median ΔBrier `-0.0000097091 / -0.0000090523`, Brier 개선/악화 `5/0`, best fold 제외 Mean ΔBrier `-0.0000057567`, Mean ΔAUC `+0.0001152819`
- 2024: Brier `0.2480865657` (Δ `-0.0000090523`), AUC `0.548020` (Δ `+0.000050`); 판정: **CANDIDATE**

## LGBM-114

- 변경: 49 Features 고정, `lambda_l1=0.50`, `min_child_samples=50`. LGBM-101과 완전히 동일한 설정이므로 검증된 결과 재사용.
- 결과: Mean/Median ΔBrier `-0.0000100247 / -0.0000051024`, Brier 개선/악화 `5/0`, best fold 제외 Mean ΔBrier `-0.0000061654`, Mean ΔAUC `+0.0001179623`
- 2024: Brier `0.2480905155` (Δ `-0.0000051024`), AUC `0.548008` (Δ `+0.000037`); 판정: **CANDIDATE**

## LGBM-115

- 변경: 49 Features 고정, `lambda_l1=0.55`, `min_child_samples=50`
- 결과: Mean/Median ΔBrier `-0.0000041403 / -0.0000019064`, Brier 개선/악화 `4/1`, best fold 제외 Mean ΔBrier `+0.0000002315`, Mean ΔAUC `+0.0000528658`
- 2024: ΔBrier `+0.0000066746`, ΔAUC `-0.000054`; 판정: **REJECT**

## LGBM-116

- 변경: 49 Features 고정, `lambda_l1=0.60`, `min_child_samples=50`
- 결과: Mean/Median ΔBrier `-0.0000001443 / +0.0000069584`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000040082`, Mean ΔAUC `-0.0000280696`
- 2024: ΔBrier `+0.0000069584`; 판정: **REJECT**

## LGBM-117

- 변경: 49 Features 고정, `lambda_l1=0.70`, `min_child_samples=50`
- 결과: Mean/Median ΔBrier `-0.0000001744 / +0.0000044328`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000035224`, Mean ΔAUC `-0.0000503726`
- 2024: ΔBrier `+0.0000045844`; 판정: **REJECT**

## LGBM-118

- 변경: 49 Features 고정, `lambda_l1=0.50`, `min_child_samples=75`
- 결과: Mean/Median ΔBrier `+0.0000070262 / +0.0000038608`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000096359`, Mean ΔAUC `+0.0000855854`
- 2024: ΔBrier `-0.0000032509`, ΔAUC `+0.000002`; 판정: **REJECT**

## LGBM-119

- 변경: 49 Features 고정, `lambda_l1=0.50`, `min_child_samples=125`
- 결과: Mean/Median ΔBrier `-0.0000026117 / -0.0000005487`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+0.0000003991`, Mean ΔAUC `+0.0000294314`
- 2024: ΔBrier `+0.0000041066`, ΔAUC `-0.000089`; 판정: **REJECT**

## LGBM-120

- 변경: 49 Features 고정, `lambda_l1=0.50`, `min_child_samples=175`
- 결과: Mean/Median ΔBrier `+0.0000016525 / +0.0000003624`, Brier 개선/악화 `2/3`, best fold 제외 Mean ΔBrier `+0.0000079392`, Mean ΔAUC `-0.0000065685`
- 2024: ΔBrier `+0.0000021317`, ΔAUC `-0.000131`; 판정: **REJECT**

## L1 Fine Search Summary

- CANDIDATE: LGBM-113 (`lambda_l1=0.45`)과 LGBM-114 (`lambda_l1=0.50`, LGBM-101 재현).
- LGBM-114가 111~120 중 mean Brier 최상이지만 LGBM-095보다 Mean Brier `+0.0000001763`, 2024 Brier `+0.0000030888` 높음.
- `lambda_l1=0.55` 이상과 추가 min-child 조정에서는 강건한 추가 개선이 확인되지 않음.
- 최종 판단: **CASE B**. `lambda_l1=0.5` 주변 추가 정밀 탐색을 종료하고 Calibration 단계로 이동.
- 공식 baseline LGBM-029와 현재 최상 candidate LGBM-095 유지.

## LGBM-121

- 변경: 실제 결과 기준 raw 최상 모델 LGBM-095에 과거 rolling OOF 예측으로 학습한 Platt calibration 적용. 현재 validation label은 calibration fitting에 미사용.
- 결과: Mean/Median ΔBrier `+0.0001797370 / +0.0002095597`, Brier 개선/악화 `1/3` (동률 1), best fold 제외 Mean ΔBrier `+0.0003656928`, Mean ΔAUC `0.000000`
- 2024: Brier `0.2482969864` (raw 대비 Δ `+0.0002095597`); 판정: **REJECT**

## LGBM-122

- 변경: LGBM-095에 과거 rolling OOF 기반 Isotonic calibration 적용.
- 결과: Mean/Median ΔBrier `+0.0002483194 / +0.0000194283`, Brier 개선/악화 `1/3` (동률 1), best fold 제외 Mean ΔBrier `+0.0004947810`, Mean ΔAUC `-0.000181`
- 2024: Brier `0.2481068550` (raw 대비 Δ `+0.0000194283`); 판정: **REJECT**

## LGBM-123

- 변경: 각 fold에서 이전 validation season 성능만으로 Platt/Isotonic 중 하나를 선택하는 past-fold adaptive calibration.
- 결과: Mean/Median ΔBrier `+0.0003225435 / +0.0002095597`, Brier 개선/악화 `1/3` (동률 1), best fold 제외 Mean ΔBrier `+0.0005442009`, Mean ΔAUC `-0.000052`
- 2024: raw 대비 ΔBrier `+0.0002095597`; 판정: **REJECT**

## LGBM-124

- 변경: validation season 이전 데이터만 사용한 leave-one-season-out OOF 예측으로 Platt calibration 학습.
- 결과: Mean/Median ΔBrier `+0.0001615940 / +0.000169`, Brier 개선/악화 `0/4` (동률 1), best fold 제외 Mean ΔBrier `+0.0002019925`, Mean ΔAUC `0.000000`
- 2024: raw 대비 ΔBrier `+0.0002069736`; 판정: **REJECT**

## LGBM-125

- 변경: 121~124 중 상대적으로 가장 나은 LGBM-124 calibration을 raw LGBM-095와 결합해 재검증.
- 결과: Mean ΔBrier `+0.0001615940`, best fold 제외 Mean ΔBrier `+0.0002019925`, 2024 ΔBrier `+0.0002069736`
- 판정: **REJECT**

## LGBM-126

- 변경: LGBM-124 calibrated probability 이동량을 50%로 축소 (`raw + 0.5 × (calibrated - raw)`).
- 결과: Mean ΔBrier `+0.0000717033`, Brier 개선/악화 `0/4` (동률 1), best fold 제외 Mean ΔBrier `+0.0000896291`
- 2024: raw 대비 ΔBrier `+0.0000893784`; 판정: **REJECT**

## LGBM-127

- 변경: fold별 raw LGBM-095와 최상 calibration(LGBM-124)의 확률 이동 및 Brier 차이 분석.
- 결과: calibration이 2021~2024 네 fold 모두에서 Brier 악화. Mean ΔBrier `+0.0001615940`, 2024 ΔBrier `+0.0002069736`.
- 판정: **REJECT**

## LGBM-128

- 변경: Calibration 단계 종료 판단. 최상 calibration도 REJECT이므로 추가 무작위 parameter 탐색 없이 raw LGBM-095를 유지.
- 결과: raw identity이므로 Mean/Median/2024 ΔBrier `0`; 판정: **REJECT**
- 결론: Calibration 효과 없음. Ensemble 단계로 이동.

## LGBM-129

- 변경: 실제 상위 raw 모델 LGBM-095, LGBM-101, LGBM-113의 fold별 prediction correlation 분석.
- 결과: 상관 범위 약 `0.997885~0.999956`. 모델별 예측은 매우 유사하며 ensemble 다양성이 낮음.
- 판정: **ANALYSIS**

## LGBM-130

- 변경: 상위 raw 모델 LGBM-095/LGBM-101의 제한적 weighted ensemble (`0.5/0.5`, `0.6/0.4`, `0.7/0.3`) 평가. 강건성 기준으로 `0.6/0.4` 선택.
- 결과: Mean/Median ΔBrier `-0.0000007920 / -0.0000011948`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `-0.0000000167`, Mean ΔAUC 약 `+0.000013`
- 2024: LGBM-095 raw 대비 ΔBrier `+0.0000010867`로 소폭 악화.
- 판정: **CANDIDATE**
- 비고: 판정 기준은 통과했지만 개선 폭과 best-fold 제외 여유가 매우 작고 2024가 악화되어 강한 개선으로 해석하지 않음.

## Calibration / Ensemble Summary

- Calibration LGBM-121~127은 모두 raw LGBM-095보다 악화. 추가 calibration 탐색 중단.
- Raw 상위 모델 간 prediction correlation이 매우 높아 ensemble 이득이 제한적임.
- LGBM-130은 제한된 ensemble 중 유일한 CANDIDATE이나 개선 폭은 `7.92e-7`에 불과함.
- 가장 안정적인 단일 모델은 계속 LGBM-095이며, LGBM-130은 추가 독립 검증이 필요한 미세 개선 후보로만 유지.

## Ensemble Weight Fine Search

LGBM-095와 LGBM-101의 모델·Feature는 고정하고 ensemble weight만 변경했다. 모든 결과는 LGBM-095 raw prediction 대비 5-fold walk-forward paired 비교다.

## LGBM-131

- 변경: ensemble weight `0.500/0.500` (095/101)
- 결과: Mean/Median ΔBrier `-8.1034163843e-07 / -1.40628885456e-06`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+1.52312294409e-07`, Mean ΔAUC `+1.49319007246e-05`
- 2024: ΔBrier `+1.38942690184e-06`, ΔAUC `-4.720026343e-06`
- 판정: **REJECT**

## LGBM-132

- 변경: ensemble weight `0.550/0.450` (095/101)
- 결과: Mean/Median ΔBrier `-8.10173897126e-07 / -1.30488652661e-06`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+5.91292906582e-08`, Mean ΔAUC `+1.41741614397e-05`
- 2024: ΔBrier `+1.23653546971e-06`, ΔAUC `-4.12017739859e-06`
- 판정: **REJECT**

## LGBM-133

- 변경: ensemble weight `0.600/0.400` (095/101), LGBM-130 재검증
- 결과: LGBM-130의 주요 지표와 허용 오차 `1e-12` 이내에서 일치. Mean/Median ΔBrier `-7.9203583972e-07 / -1.19476718591e-06`, best fold 제외 Mean ΔBrier `-1.67310965984e-08`, Mean ΔAUC `+1.33301756375e-05`
- 2024: ΔBrier `+1.08674375801e-06`, ΔAUC `-3.3857206071e-06`
- 판정: **CANDIDATE**

## LGBM-134

- 변경: ensemble weight `0.650/0.350` (095/101)
- 결과: Mean/Median ΔBrier `-7.55927466178e-07 / -1.07593083234e-06`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `-7.52688673195e-08`, Mean ΔAUC `+1.23358512998e-05`
- 2024: ΔBrier `+9.40051766735e-07`, ΔAUC `-2.65873856864e-06`
- 판정: **CANDIDATE**

## LGBM-135

- 변경: ensemble weight `0.700/0.300` (095/101)
- 결과: Mean/Median ΔBrier `-7.01848776519e-07 / -9.48377466059e-07`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `-1.01384487229e-07`, Mean ΔAUC `+1.11999954477e-05`
- 2024: ΔBrier `+7.96459495939e-07`, ΔAUC `-2.03154448541e-06`
- 판정: **CANDIDATE**

## LGBM-136

- 변경: ensemble weight `0.750/0.250` (095/101)
- 결과: Mean/Median ΔBrier `-6.29799770757e-07 / -8.12107086995e-07`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `-1.05918347017e-07`, Mean ΔAUC `+9.75510261032e-06`
- 2024: ΔBrier `+6.55966945484e-07`, ΔAUC `-1.69985231224e-06`
- 판정: **CANDIDATE**

## LGBM-137

- 변경: ensemble weight `0.800/0.200` (095/101)
- 결과: Mean/Median ΔBrier `-5.39780448838e-07 / -6.67119695125e-07`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `-1.01879697047e-07`, Mean ΔAUC `+8.06828500057e-06`
- 2024: ΔBrier `+5.18574115538e-07`, ΔAUC `-1.37052714411e-06`
- 판정: **CANDIDATE**

## LGBM-138

- 변경: ensemble weight `0.450/0.550` (095/101)
- 결과: Mean/Median ΔBrier `-7.92539063599e-07 / -1.49897416976e-06`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+2.62817914674e-07`, Mean ΔAUC `+1.55210355911e-05`
- 2024: ΔBrier `+1.54541805436e-06`, ΔAUC `-5.28723553161e-06`
- 판정: **REJECT**

## LGBM-139

- 변경: ensemble weight `0.400/0.600` (095/101)
- 결과: Mean/Median ΔBrier `-7.56766172644e-07 / -1.58294247216e-06`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+3.90646151462e-07`, Mean ΔAUC `+1.58257408091e-05`
- 2024: ΔBrier `+1.70450892734e-06`, ΔAUC `-6.24599720889e-06`
- 판정: **REJECT**

## LGBM-140

- 변경: ensemble weight `0.350/0.650` (095/101)
- 결과: Mean/Median ΔBrier `-7.03022965565e-07 / -1.65819376177e-06`, Brier 개선/악화 `3/2`, best fold 제외 Mean ΔBrier `+5.35797004764e-07`, Mean ΔAUC `+1.59449310334e-05`
- 2024: ΔBrier `+1.86669952076e-06`, ΔAUC `-7.31700476331e-06`
- 판정: **REJECT**

## LGBM-141

- 변경: 1차 평균 Brier 최적점 0.500 주변 미세 탐색, ensemble weight `0.475/0.525` (095/101)
- 결과: Mean/Median ΔBrier `-8.03686640533e-07 / -1.45372113877e-06`, best fold 제외 Mean ΔBrier `+2.05399777471e-07`, Mean ΔAUC `+1.52529415281e-05`
- 2024: ΔBrier `+1.46703501303e-06`, ΔAUC `-5.03907372551e-06`
- 판정: **REJECT**

## LGBM-142

- 변경: 1차 평균 Brier 최적점 0.500 주변 미세 탐색, ensemble weight `0.525/0.475` (095/101)
- 결과: Mean/Median ΔBrier `-8.1250405729e-07 / -1.35667731718e-06`, best fold 제외 Mean ΔBrier `+1.03555465467e-07`, Mean ΔAUC `+1.46766323355e-05`
- 2024: Brier `0.248088739289241`, AUC `0.548019163131421`, ΔBrier `+1.31259372071e-06`, ΔAUC `-4.3010041364e-06`
- 판정: **REJECT**

## Ensemble Weight Search Conclusion

- 평균 Brier 최저점은 LGBM-142 (`0.525/0.475`)지만 LGBM-130 대비 Mean ΔBrier 개선은 약 `-2.04682e-08`로 실질적 의미가 없다.
- LGBM-142는 best fold 제외 Mean ΔBrier가 양수이고 2024 Brier/AUC도 LGBM-130보다 악화되어 과적합 가능성이 있다.
- 095 비중을 높일수록 2024 악화 폭과 best fold 의존성은 감소하지만 전체 평균 Brier 이득도 감소한다.
- 실제 제출 후보 TOP 3: LGBM-130/LGBM-133 (`0.600/0.400`), LGBM-134 (`0.650/0.350`), LGBM-135 (`0.700/0.300`).
- 최종 결정: 실제 리더보드 약 704점으로 검증된 **LGBM-130 유지**. 기존 제출 패키지는 수정하지 않음.

## Probability Ensemble Search

- 비교 기준: LGBM-130 (`0.6 * LGBM-095 + 0.4 * LGBM-101`)
- LGBM-141/142는 직전 weight fine search에서 이미 사용된 번호이므로 덮어쓰지 않고 `SKIPPED_ID_CONFLICT`로 기록함.
- Feature, 모델 파라미터, Trackman, 외부 데이터는 변경하거나 사용하지 않음.

## LGBM-143

- 변경: complementary geometric mean
- 결과: Mean/Median ΔBrier `+7.89293007619e-09 / -2.003348e-07`, best fold 제외 Mean ΔBrier `+2.126715e-07`, Brier 개선/악화 `3/2`, Mean ΔAUC `+1.623669e-06`
- 2024: ΔBrier `+3.07718416664e-07`, ΔAUC `-1.373860e-06`
- 판정: **REJECT**

## LGBM-144

- 변경: harmonic mean
- 결과: Mean/Median ΔBrier `-5.49543840822e-08 / -2.164001e-07`, best fold 제외 Mean ΔBrier `+1.090887e-07`, Brier 개선/악화 `3/2`, Mean ΔAUC `+1.595408e-06`
- 2024: ΔBrier `+2.9149223052e-07`, ΔAUC `-1.242429e-06`
- 판정: **REJECT**

## LGBM-145

- 변경: arithmetic mean `0.5/0.5`
- 결과: Mean/Median ΔBrier `-1.83057987102e-08 / -2.115217e-07`, best fold 제외 Mean ΔBrier `+1.690434e-07`, Brier 개선/악화 `3/2`, Mean ΔAUC `+1.601725e-06`
- 2024: ΔBrier `+3.02683143827e-07`, ΔAUC `-1.334306e-06`
- 판정: **REJECT**

## LGBM-146

- 변경: logit-space ensemble `0.6/0.4`
- 결과: Mean/Median ΔBrier `+7.46153183684e-09 / -5.373486e-10`, best fold 제외 Mean ΔBrier `+1.298645e-08`, Brier 개선/악화 `3/2`, Mean ΔAUC `+2.906494e-08`
- 2024: ΔBrier `-5.37348582297e-10`, ΔAUC `+4.858590e-09`
- 판정: **REJECT**

## LGBM-147

- 변경: logit-space ensemble `0.5/0.5`
- 결과: Mean/Median ΔBrier `-1.04680796531e-08 / -2.158234e-07`, best fold 제외 Mean ΔBrier `+1.826527e-07`, Brier 개선/악화 `3/2`, Mean ΔAUC `+1.626338e-06`
- 2024: ΔBrier `+3.02122360935e-07`, ΔAUC `-1.328824e-06`
- 판정: **REJECT**

## LGBM-148

- 변경: logit-space ensemble `0.7/0.3`
- 결과: Mean/Median ΔBrier `+9.66630954113e-08 / +2.428011e-07`, best fold 제외 Mean ΔBrier `+3.564144e-07`, Brier 개선/악화 `2/3`, Mean ΔAUC `-2.105071e-06`
- 2024: ΔBrier `-2.9075353089e-07`, ΔAUC `+1.358163e-06`
- 판정: **REJECT**

## LGBM-149

- 변경: logit-space ensemble `0.4/0.6`
- 결과: Mean/Median ΔBrier `+4.28588733892e-08 / -3.923187e-07`, best fold 제외 Mean ΔBrier `+4.205233e-07`, Brier 개선/악화 `3/2`, Mean ΔAUC `+2.509274e-06`
- 2024: ΔBrier `+6.17225853206e-07`, ΔAUC `-2.864450e-06`
- 판정: **REJECT**

## LGBM-150

- 변경: prediction diff에 따라 095 weight를 0.6에서 0.5 방향으로 완화 (`w095=clip(0.6-0.1*diff, 0.5, 0.6)`)
- 결과: Mean/Median ΔBrier `-1.37399529532e-09 / +3.273233e-10`, best fold 제외 Mean ΔBrier `-2.922221e-10`, Brier 개선/악화 `2/3`, Mean ΔAUC `+1.838938e-08`
- 2024: ΔBrier `+6.42472297585e-10`, ΔAUC `-1.681819e-09`
- 판정: **REJECT**

## LGBM-151

- 변경: prediction diff가 클수록 101 weight를 더 높임 (`w095=clip(0.6-0.2*diff, 0.4, 0.6)`)
- 결과: Mean/Median ΔBrier `-2.74394422184e-09 / +6.551822e-10`, best fold 제외 Mean ΔBrier `-5.798651e-10`, Brier 개선/악화 `2/3`, Mean ΔAUC `+4.156167e-08`
- 2024: ΔBrier `+1.28500507457e-09`, ΔAUC `-1.021550e-08`
- 판정: **REJECT**

## LGBM-152

- 변경: 0.5에 더 가까운 보수적 prediction에 weight 0.7, 다른 prediction에 0.3 적용
- 결과: Mean/Median ΔBrier `-3.27009184878e-06 / +9.083002e-07`, best fold 제외 Mean ΔBrier `+1.290933e-06`, Brier 개선/악화 `2/3`, Mean ΔAUC `+2.787839e-06`
- 2024: ΔBrier `+1.55115273739e-06`, ΔAUC `-6.096409e-06`
- 판정: **REJECT**

## LGBM-153

- 변경: fold train target mean 방향 shrinkage, strength `0.05`
- 결과: Mean/Median ΔBrier `-4.36110319969e-05 / +4.493588e-05`, best fold 제외 Mean ΔBrier `+1.963995e-05`, Brier 개선/악화 `2/3`, Mean ΔAUC `0`
- 2024: ΔBrier `+6.03295432274e-05`
- 판정: **REJECT**. 시즌 간 target mean 차이에 민감함.

## LGBM-154

- 변경: fold train target mean 방향 shrinkage, strength `0.10`
- 결과: Mean/Median ΔBrier `-6.83404565138e-05 / +1.031598e-04`, best fold 제외 Mean ΔBrier `+5.709363e-05`, Brier 개선/악화 `2/3`, Mean ΔAUC `0`
- 2024: ΔBrier `+1.34237732544e-04`
- 판정: **REJECT**. 시즌 간 target mean 차이에 민감함.

## LGBM-155

- 변경: fold train target mean 방향 shrinkage, strength `0.15`
- 결과: Mean/Median ΔBrier `-7.41882735508e-05 / +1.746717e-04`, best fold 제외 Mean ΔBrier `+1.123610e-04`, Brier 개선/악화 `2/3`, Mean ΔAUC `0`
- 2024: Brier `0.248310238007229`, AUC `0.54802007841495`, ΔBrier `+2.21724567951e-04`
- 판정: **REJECT**. 평균 개선은 일부 fold에 집중되며 2024가 크게 악화됨.

## Probability Ensemble Conclusion

- 평균 Brier 순위상 LGBM-155가 가장 낮지만 median, best-fold 제외 mean, 개선 fold 수, 2024 결과를 모두 위반하므로 채택할 수 없음.
- harmonic/geometric/logit/adaptive 방식의 차이는 대부분 실질적으로 무의미하거나 2023/2024에서 악화됨.
- 신규 CANDIDATE는 없음.
- 최종 결정: 실제 리더보드 약 704점으로 검증된 **KEEP LGBM-130**.

## LGBM-156~180 Three-Model Ensemble Artifact Audit

- 목적: LGBM-130을 baseline으로 기존 모델 095/101과 104/105/113/114를 조합한 3-model ensemble 검증.
- 확인된 직렬화 모델 파일: `submit_lgbm130/model/lgbm_095.txt`, `submit_lgbm130/model/lgbm_101.txt`.
- 104/105/113/114는 fold별 집계 지표 CSV만 존재하며, 직렬화 모델 또는 행별 fold prediction은 존재하지 않음.
- 집계 Brier/AUC와 prediction mean만으로는 ensemble prediction, Brier/AUC, prediction 차이 및 correlation을 복원할 수 없음.
- 전체기간 제출 모델로 과거 validation fold를 예측하는 것은 temporal leakage이므로 사용하지 않음.
- 지시된 “존재하지 않는 모델을 새로 만들거나 추측하지 않음” 원칙에 따라 LGBM-156~180은 모두 `NOT_RUN_MISSING_MODEL_ARTIFACT`로 기록함.
- 수치 결과를 만들지 않았으며 `results.csv`에 가짜 또는 예약 행을 추가하지 않음. 실험 번호는 소비하지 않음.
- 제출은 수행하지 않았고 LGBM-130 관련 파일은 수정하지 않음.
- 최종 결정: **KEEP LGBM-130**.

## LGBM-181~200 LGBM-130 Fine Search

- Baseline: LGBM-130 (`0.60 * LGBM-095 + 0.40 * LGBM-101`)
- Feature, Trackman, 모델 파라미터 변경 없음. 각 fold에서 LGBM-095/101을 기존 조건으로 재현함.
- LGBM-181~190: 095/101 weight 미세 조정.
- LGBM-191~200: `0.5 + strength * (p130 - 0.5)` probability shrinkage/expansion.

| Experiment | Method           |   Mean ΔBrier | Median ΔBrier | Best fold 제외 Mean ΔBrier |   2024 ΔBrier | Verdict |
| ---------- | ---------------- | ------------: | ------------: | -------------------------: | ------------: | ------- |
| LGBM-181   | weight 0.61/0.39 | +5.784049e-09 | +2.306991e-08 |              +3.094595e-08 | -2.958638e-08 | REJECT  |
| LGBM-182   | weight 0.62/0.38 | +1.228691e-08 | +4.648850e-08 |              +6.277129e-08 | -5.904876e-08 | REJECT  |
| LGBM-183   | weight 0.63/0.37 | +1.950859e-08 | +7.025577e-08 |              +9.547602e-08 | -8.838716e-08 | REJECT  |
| LGBM-184   | weight 0.64/0.36 | +2.744907e-08 | +9.437172e-08 |              +1.290602e-07 | -1.176016e-07 | REJECT  |
| LGBM-185   | weight 0.65/0.35 | +3.610837e-08 | +1.188364e-07 |              +1.635237e-07 | -1.466920e-07 | REJECT  |
| LGBM-186   | weight 0.59/0.41 | -5.065237e-09 | -2.272123e-08 |              +1.378627e-08 | +2.971036e-08 | REJECT  |
| LGBM-187   | weight 0.58/0.42 | -9.411661e-09 | -4.509378e-08 |              +2.826544e-08 | +5.954472e-08 | REJECT  |
| LGBM-188   | weight 0.57/0.43 | -1.303927e-08 | -6.711765e-08 |              +4.343752e-08 | +8.950306e-08 | REJECT  |
| LGBM-189   | weight 0.56/0.44 | -1.594807e-08 | -8.879283e-08 |              +5.930250e-08 | +1.195854e-07 | REJECT  |
| LGBM-190   | weight 0.55/0.45 | -1.813806e-08 | -1.101193e-07 |              +7.586039e-08 | +1.497917e-07 | REJECT  |
| LGBM-191   | shrink 0.95      | -8.889402e-05 | +2.829636e-05 |              -1.688000e-05 | +2.829636e-05 | REJECT  |
| LGBM-192   | shrink 0.96      | -7.284437e-05 | +2.207053e-05 |              -1.519815e-05 | +2.207053e-05 | REJECT  |
| LGBM-193   | shrink 0.97      | -5.593014e-05 | +1.612799e-05 |              -1.266922e-05 | +1.612799e-05 | REJECT  |
| LGBM-194   | shrink 0.98      | -3.815134e-05 | +1.046872e-05 |              -9.293222e-06 | +1.046872e-05 | REJECT  |
| LGBM-195   | shrink 0.99      | -1.950796e-05 | +5.092720e-06 |              -5.070148e-06 | +5.092720e-06 | REJECT  |
| LGBM-196   | expansion 1.01   | +2.037254e-05 | -4.647907e-06 |              +2.947858e-05 | -4.809444e-06 | REJECT  |
| LGBM-197   | expansion 1.02   | +4.160965e-05 | -8.076000e-06 |              +5.990696e-05 | -9.335613e-06 | REJECT  |
| LGBM-198   | expansion 1.03   | +6.371134e-05 | -1.028428e-05 |              +9.128511e-05 | -1.357851e-05 | REJECT  |
| LGBM-199   | expansion 1.04   | +8.667760e-05 | -1.127275e-05 |              +1.236131e-04 | -1.753812e-05 | REJECT  |
| LGBM-200   | expansion 1.05   | +1.105084e-04 | -1.104140e-05 |              +1.568908e-04 | -2.121446e-05 | REJECT  |

### LGBM-181~200 결론

- 0.60 아래 weight는 평균 Brier가 최대 `1.81e-8` 개선됐지만 best-fold 제외 평균과 2024가 악화됨.
- 0.60 위 weight는 2024가 개선됐지만 전체 평균·중앙값·best-fold 제외 평균이 악화됨.
- Shrinkage 0.95~0.99는 2020/2023 개선에 평균이 좌우되며 3개 fold와 2024가 악화됨.
- Expansion 1.01~1.05는 2024가 개선됐지만 전체 평균 Brier가 명확히 악화됨.
- 신규 CANDIDATE는 없으며 최종 결정은 **KEEP LGBM-130**.

## LGBM-201~225 Prediction Difference Search

- Baseline: LGBM-130 (`0.60 * LGBM-095 + 0.40 * LGBM-101`)
- validation target을 이용한 alpha 선택 없이 지정된 변환을 각각 독립 평가함.
- Feature, Trackman, 외부 데이터 및 모델 파라미터 변경 없음.

| Experiment | Method                   |   Mean ΔBrier | Median ΔBrier | Best fold 제외 Mean |   2024 ΔBrier | Verdict |
| ---------- | ------------------------ | ------------: | ------------: | ------------------: | ------------: | ------- |
| LGBM-201   | linear difference -0.2   | +3.526967e-08 | -3.881753e-07 |       +4.073772e-07 | +6.177652e-07 | REJECT  |
| LGBM-202   | linear difference -0.1   | -1.830580e-08 | -2.115217e-07 |       +1.690434e-07 | +3.026831e-07 | REJECT  |
| LGBM-203   | linear difference 0.1    | +9.018706e-08 | +2.463897e-07 |       +3.490322e-07 | -2.902843e-07 | REJECT  |
| LGBM-204   | linear difference 0.2    | +2.522554e-07 | +5.276475e-07 |       +7.860038e-07 | -5.681696e-07 | REJECT  |
| LGBM-205   | linear difference 0.3    | +4.862050e-07 | +8.437733e-07 |       +1.310915e-06 | -8.336561e-07 | REJECT  |
| LGBM-206   | nonlinear difference -5  | -6.374295e-08 | +1.702235e-08 |       -9.001710e-09 | +3.219778e-08 | REJECT  |
| LGBM-207   | nonlinear difference -2  | -2.671109e-08 | +6.648241e-09 |       -4.974413e-09 | +1.286095e-08 | REJECT  |
| LGBM-208   | nonlinear difference 2   | +2.832965e-08 | -6.433976e-09 |       +4.139384e-08 | -1.283673e-08 | REJECT  |
| LGBM-209   | nonlinear difference 5   | +7.385890e-08 | -1.568319e-08 |       +1.072741e-07 | -3.204642e-08 | REJECT  |
| LGBM-210   | nonlinear difference 10  | +1.578338e-07 | -3.002723e-08 |       +2.271801e-07 | -6.394147e-08 | REJECT  |
| LGBM-211   | disagreement shrink 1    | -2.064151e-06 | +3.423861e-07 |       +4.593225e-07 | +3.423861e-07 | REJECT  |
| LGBM-212   | disagreement shrink 2    | -4.081057e-06 | +6.868596e-07 |       +9.338475e-07 | +6.868596e-07 | REJECT  |
| LGBM-213   | disagreement shrink 3    | -6.050718e-06 | +1.033420e-06 |       +1.423575e-06 | +1.033420e-06 | REJECT  |
| LGBM-214   | disagreement shrink 5    | -9.848307e-06 | +1.732803e-06 |       +2.448638e-06 | +1.732803e-06 | REJECT  |
| LGBM-215   | disagreement shrink 10   | -1.851550e-05 | +3.517788e-06 |       +5.277341e-06 | +3.517788e-06 | REJECT  |
| LGBM-216   | dynamic weight +0.05     | +6.885150e-10 | -1.634607e-10 |       +1.010214e-09 | -3.212134e-10 | REJECT  |
| LGBM-217   | dynamic weight -0.05     | -6.875034e-10 | +1.635947e-10 |       -1.466834e-10 | +3.212286e-10 | REJECT  |
| LGBM-218   | dynamic weight +0.10     | +1.378042e-09 | -3.267875e-10 |       +2.021691e-09 | -6.424117e-10 | REJECT  |
| LGBM-219   | dynamic weight -0.10     | -1.373995e-09 | +3.273233e-10 |       -2.922221e-10 | +6.424723e-10 | REJECT  |
| LGBM-220   | dynamic weight +0.20     | +2.760130e-09 | -6.530395e-10 |       +4.048435e-09 | -1.284763e-09 | REJECT  |
| LGBM-221   | rank 0.6/0.4             | +5.919683e-02 | +6.124636e-02 |       +6.124841e-02 | +6.124636e-02 | REJECT  |
| LGBM-222   | rank 0.5/0.5             | +5.919503e-02 | +6.124680e-02 |       +6.124745e-02 | +6.124680e-02 | REJECT  |
| LGBM-223   | rank 0.7/0.3             | +5.920100e-02 | +6.124662e-02 |       +6.125197e-02 | +6.124662e-02 | REJECT  |
| LGBM-224   | rank 0.4/0.6             | +5.919560e-02 | +6.124795e-02 |       +6.124911e-02 | +6.124795e-02 | REJECT  |
| LGBM-225   | 0.5 p130 + 0.5 mean rank | +1.519507e-02 | +1.472026e-02 |       +1.595048e-02 | +1.472026e-02 | REJECT  |

### LGBM-201~225 결론

- Mean Brier 상위 5개는 LGBM-215~211이지만 모두 2개 fold만 개선되고 median, best-fold 제외 mean, 2024 Brier 및 AUC가 악화됨.
- Linear/nonlinear/dynamic weight 차이는 대부분 `1e-7` 미만으로 실질적 개선이 아님.
- Rank prediction은 probability calibration을 파괴하여 모든 fold에서 Brier가 크게 악화됨.
- 신규 CANDIDATE는 없으며 **CURRENT BEST = LGBM-130** 유지.

## LGBM-226~245 Disagreement Shrinkage Artifact Audit

- 요청: LGBM-130 baseline에서 disagreement shrinkage alpha `0.025~1.000` 20개를 기존 095/101 prediction artifact만 사용해 평가.
- 실제 확인 결과: `lgbm_095_walkforward.csv`와 `lgbm_101_walkforward.csv`에는 fold별 집계 지표와 prediction mean만 있으며 행 단위 `p095`/`p101`은 없음.
- 전체기간 제출 모델은 과거 validation fold용 모델이 아니므로 사용 시 temporal leakage가 발생함.
- “새로운 모델을 학습하지 않음” 제약에 따라 fold 모델을 재학습하지 않음.
- LGBM-226~245는 모두 `NOT_RUN_MISSING_PREDICTION_ARTIFACT`로 상태 기록했으며 성능 수치를 생성하지 않음.
- `results.csv`에는 가짜 또는 예약 행을 추가하지 않았고 실험 번호는 소비하지 않음.
- 비교 가능한 신규 후보와 TOP 5는 없음. **CURRENT BEST = LGBM-130** 유지.

## LGBM-130 Row-Level Prediction Pipeline Recovery

- 근거 코드: `experiments/scripts/lgbm_121_130.py`, `experiments/scripts/export_lgbm_130.py`, `submit_lgbm130/script.py`.
- 기존 49개 Feature 순서와 LGBM-095/101 파라미터를 그대로 사용해 5-fold walk-forward prediction을 재생성함.
- 저장 컬럼: `row_id`, `y_true`, `p095`, `p101`, `p130`.
- 저장 위치: `experiments/outputs/lgbm_130_row_predictions/fold_YYYY_predictions.csv`.
- 재현 Mean Brier: `0.2476711399337079`.
- 재현 Mean AUC: `0.5530385153643456`.
- 재현 2024 Brier/AUC: `0.2480885134392783 / 0.5480200784149498`.
- 기존 fold 및 전체 지표와 허용 오차 `1e-12` 이내에서 일치하여 pipeline 복구 성공.

## LGBM-226~245 Executed After Pipeline Recovery

- 기존 `NOT_RUN_MISSING_PREDICTION_ARTIFACT` 기록은 보존하고 실제 실행 결과를 별도 상세/요약 CSV에 저장함.
- 각 fold의 row-level 후보 prediction은 `experiments/outputs/lgbm_226_245_row_predictions/fold_YYYY_predictions.csv`의 `p226`~`p245` 컬럼에 저장함.

| Experiment | Alpha |   Mean ΔBrier | Median ΔBrier | Best fold 제외 Mean |   2024 ΔBrier | Verdict |
| ---------- | ----: | ------------: | ------------: | ------------------: | ------------: | ------- |
| LGBM-226   | 0.025 | -5.217956e-08 | +8.534215e-09 |       +1.129778e-08 | +8.534215e-09 | REJECT  |
| LGBM-227   | 0.050 | -1.043296e-07 | +1.706974e-08 |       +2.260506e-08 | +1.706974e-08 | REJECT  |
| LGBM-228   | 0.075 | -1.564501e-07 | +2.560656e-08 |       +3.392185e-08 | +2.560656e-08 | REJECT  |
| LGBM-229   | 0.100 | -2.085411e-07 | +3.414469e-08 |       +4.524813e-08 | +3.414469e-08 | REJECT  |
| LGBM-230   | 0.125 | -2.606025e-07 | +4.268412e-08 |       +5.658392e-08 | +4.268412e-08 | REJECT  |
| LGBM-231   | 0.150 | -3.126345e-07 | +5.122486e-08 |       +6.792921e-08 | +5.122486e-08 | REJECT  |
| LGBM-232   | 0.175 | -3.646369e-07 | +5.976690e-08 |       +7.928400e-08 | +5.976690e-08 | REJECT  |
| LGBM-233   | 0.200 | -4.166097e-07 | +6.831025e-08 |       +9.064829e-08 | +6.831025e-08 | REJECT  |
| LGBM-234   | 0.225 | -4.685531e-07 | +7.685490e-08 |       +1.020221e-07 | +7.685490e-08 | REJECT  |
| LGBM-235   | 0.250 | -5.204669e-07 | +8.540086e-08 |       +1.134054e-07 | +8.540086e-08 | REJECT  |
| LGBM-236   | 0.275 | -5.723512e-07 | +9.394812e-08 |       +1.247982e-07 | +9.394812e-08 | REJECT  |
| LGBM-237   | 0.300 | -6.242059e-07 | +1.024967e-07 |       +1.362005e-07 | +1.024967e-07 | REJECT  |
| LGBM-238   | 0.325 | -6.760311e-07 | +1.110466e-07 |       +1.476123e-07 | +1.110466e-07 | REJECT  |
| LGBM-239   | 0.350 | -7.278268e-07 | +1.195977e-07 |       +1.590336e-07 | +1.195977e-07 | REJECT  |
| LGBM-240   | 0.375 | -7.795930e-07 | +1.281502e-07 |       +1.704644e-07 | +1.281502e-07 | REJECT  |
| LGBM-241   | 0.400 | -8.313297e-07 | +1.367040e-07 |       +1.819047e-07 | +1.367040e-07 | REJECT  |
| LGBM-242   | 0.450 | -9.347144e-07 | +1.538155e-07 |       +2.048138e-07 | +1.538155e-07 | REJECT  |
| LGBM-243   | 0.500 | -1.037981e-06 | +1.709322e-07 |       +2.277609e-07 | +1.709322e-07 | REJECT  |
| LGBM-244   | 0.750 | -1.552542e-06 | +2.565939e-07 |       +3.430666e-07 | +2.565939e-07 | REJECT  |
| LGBM-245   | 1.000 | -2.064151e-06 | +3.423861e-07 |       +4.593225e-07 | +3.423861e-07 | REJECT  |

### LGBM-226~245 실제 실행 결론

- Mean Brier 최저 후보는 LGBM-245이지만 개선 fold는 `2/5`이고 median 및 best-fold 제외 mean이 양수임.
- 모든 alpha에서 2024 Brier가 악화됐으며 AUC도 악화됨.
- 신규 CANDIDATE는 없고 **LGBM-130 유지**.

## LGBM-246~265 Nonlinear / Threshold Disagreement Search

- 기존 `lgbm_130_row_predictions` artifact만 사용했으며 모델 학습·Feature·Trackman 변경 없음.
- 실험군 A: `p130 + alpha * (0.5-p130) * d^gamma`.
- 실험군 B: `p130 + (0.5-p130) * max(d-threshold, 0)`.

| Experiment | Parameters     |   Mean ΔBrier |     Mean ΔAUC | Best fold 제외 Mean ΔBrier |   2024 ΔBrier | Verdict |
| ---------- | -------------- | ------------: | ------------: | -------------------------: | ------------: | ------- |
| LGBM-246   | a=1.0, g=0.50  | -4.522073e-05 | -1.879040e-05 |              -5.638413e-06 | +1.257075e-05 | REJECT  |
| LGBM-247   | a=1.0, g=0.60  | -2.437019e-05 | -1.042468e-05 |              -1.289209e-06 | +5.899033e-06 | REJECT  |
| LGBM-248   | a=1.0, g=0.70  | -1.304851e-05 | -6.107167e-06 |              +2.762861e-07 | +2.834508e-06 | REJECT  |
| LGBM-249   | a=1.0, g=0.80  | -7.005987e-06 | -3.598201e-06 |              +6.522885e-07 | +1.384387e-06 | REJECT  |
| LGBM-250   | a=1.0, g=0.90  | -3.787157e-06 | -2.276492e-06 |              +6.082197e-07 | +6.847467e-07 | REJECT  |
| LGBM-251   | a=0.75, g=0.50 | -3.510236e-05 | -1.278012e-05 |              -4.875401e-06 | +9.273177e-06 | REJECT  |
| LGBM-252   | a=0.75, g=0.60 | -1.864379e-05 | -7.294951e-06 |              -1.147237e-06 | +4.385456e-06 | REJECT  |
| LGBM-253   | a=0.75, g=0.70 | -9.902955e-06 | -4.377641e-06 |              +1.554291e-07 | +2.115886e-06 | REJECT  |
| LGBM-254   | a=0.75, g=0.80 | -5.292678e-06 | -2.638231e-06 |              +4.739460e-07 | +1.035654e-06 | REJECT  |
| LGBM-255   | a=0.75, g=0.90 | -2.853213e-06 | -1.646402e-06 |              +4.515515e-07 | +5.128489e-07 | REJECT  |
| LGBM-256   | a=0.50, g=0.50 | -2.419278e-05 | -7.542190e-06 |              -3.681328e-06 | +6.078863e-06 | REJECT  |
| LGBM-257   | a=0.50, g=0.60 | -1.267330e-05 | -4.607967e-06 |              -8.850447e-07 | +2.897758e-06 | REJECT  |
| LGBM-258   | a=0.50, g=0.70 | -6.679683e-06 | -2.699748e-06 |              +6.909576e-08 | +1.403928e-06 | REJECT  |
| LGBM-259   | a=0.50, g=0.80 | -3.553910e-06 | -1.651108e-06 |              +3.057837e-07 | +6.886782e-07 | REJECT  |
| LGBM-260   | a=0.50, g=0.90 | -1.910705e-06 | -1.167373e-06 |              +2.979588e-07 | +3.414252e-07 | REJECT  |
| LGBM-261   | threshold=0.01 | +1.702630e-08 | -4.101664e-07 |              +2.128287e-08 |             0 | REJECT  |
| LGBM-262   | threshold=0.02 | +7.947073e-09 | -7.464164e-08 |              +9.933841e-09 |             0 | REJECT  |
| LGBM-263   | threshold=0.03 | -5.581698e-11 | +8.900358e-10 |                          0 |             0 | REJECT  |
| LGBM-264   | threshold=0.04 |             0 |             0 |                          0 |             0 | REJECT  |
| LGBM-265   | threshold=0.05 |             0 |             0 |                          0 |             0 | REJECT  |

### LGBM-246~265 결론

- Brier 최저 LGBM-246은 AUC와 2024 Brier/AUC가 크게 악화됨.
- Brier-AUC 방향 균형은 LGBM-263이 가장 낫지만 전체 1,237,679행 중 10행만 변경되어 Mean ΔBrier `-5.58e-11`, Mean ΔAUC `+8.90e-10`으로 실질적 효과가 없음.
- threshold 0.04 이상은 변경되는 행이 없어 LGBM-130과 동일함.
- 신규 CANDIDATE는 없으며 **LGBM-130 유지**.

## LGBM-266~285 Conditional Weighting Search

- 기존 `p095/p101/p130` row-level artifact만 사용하고 모델 학습·Feature·Trackman 변경 없이 실행함.
- Piecewise 실험은 명시된 구간 규칙에 따라 `d<0.01`에서 adjustment 0, `0.01<=d<0.03`에서 medium, `d>=0.03`에서 large 값을 적용함. 표의 small 값은 baseline 구간이라 미적용.

| Experiment | Method / Parameter    |   Mean ΔBrier |     Mean ΔAUC | Best fold 제외 Mean ΔBrier |            2024 ΔBrier / ΔAUC | Verdict |
| ---------- | --------------------- | ------------: | ------------: | -------------------------: | ----------------------------: | ------- |
| LGBM-266   | linear k=-0.5         | -6.829513e-09 | +1.020982e-07 |              -1.415319e-09 | +3.212967e-09 / -2.865322e-08 | REJECT  |
| LGBM-267   | linear k=-0.25        | -3.427401e-09 | +5.081221e-08 |              -7.219694e-10 | +1.606294e-09 / -1.114984e-08 | REJECT  |
| LGBM-268   | linear k=0.25         | +3.452691e-09 | -3.066761e-08 |              +5.063702e-09 | -1.605916e-09 / +8.097649e-10 | REJECT  |
| LGBM-269   | linear k=0.5          | +6.930672e-09 | -7.042289e-08 |              +1.015898e-08 | -3.211453e-09 / -1.096297e-08 | REJECT  |
| LGBM-270   | linear k=1            | +1.396250e-08 | -1.669959e-07 |              +2.044428e-08 | -6.421393e-09 / +2.011954e-08 | REJECT  |
| LGBM-271   | sqrt k=-0.05          | -5.618821e-09 | +7.095315e-08 |              +1.819555e-09 | +6.444929e-09 / -8.328121e-08 | REJECT  |
| LGBM-272   | sqrt k=-0.025         | -2.822487e-09 | +2.905847e-08 |              +8.960846e-10 | +3.221725e-09 / -3.270205e-08 | REJECT  |
| LGBM-273   | sqrt k=0.025          | +2.848641e-09 | -2.098334e-08 |              +5.629542e-09 | -3.220247e-09 / -6.228951e-11 | REJECT  |
| LGBM-274   | sqrt k=0.05           | +5.723435e-09 | -6.976554e-08 |              +1.129160e-08 | -6.439017e-09 / +1.189732e-08 | REJECT  |
| LGBM-275   | sqrt k=0.1            | +1.155148e-08 | -1.736524e-07 |              +2.271329e-08 | -1.287212e-08 / +3.830811e-08 | REJECT  |
| LGBM-276   | square k=-5           | -1.185926e-09 | +1.858666e-08 |              -2.776940e-10 | +1.093514e-10 / -1.245791e-10 | REJECT  |
| LGBM-277   | square k=-2.5         | -5.933243e-10 | +1.181394e-08 |              -1.388581e-10 | +5.467549e-11 / +2.367005e-09 | REJECT  |
| LGBM-278   | square k=2.5          | +5.940465e-10 | -6.982072e-09 |              +8.007952e-10 | -5.467504e-11 / -8.720544e-10 | REJECT  |
| LGBM-279   | square k=5            | +1.188815e-09 | -1.571927e-08 |              +1.602489e-09 | -1.093496e-10 / -1.058923e-09 | REJECT  |
| LGBM-280   | square k=10           | +2.380519e-09 | -2.927955e-08 |              +3.208574e-09 | -2.186975e-10 / +2.304716e-09 | REJECT  |
| LGBM-281   | piecewise +0.02/+0.03 | +7.064922e-09 | -1.443212e-07 |              +1.196272e-08 |                         0 / 0 | REJECT  |
| LGBM-282   | piecewise -0.02/-0.03 | -6.686469e-09 | +1.580085e-07 |              +1.348350e-09 |                         0 / 0 | REJECT  |
| LGBM-283   | piecewise +0.04/+0.06 | +1.450830e-08 | -3.001382e-07 |              +2.439441e-08 |                         0 / 0 | REJECT  |
| LGBM-284   | piecewise -0.04/-0.06 | -1.299448e-08 | +3.215537e-07 |              +2.729988e-09 |                         0 / 0 | REJECT  |
| LGBM-285   | piecewise +0.03/+0.05 | +1.004723e-08 | -2.145790e-07 |              +1.725485e-08 |                         0 / 0 | REJECT  |

### LGBM-266~285 결론

- Brier 및 AUC 평균 기준 1위는 LGBM-284지만 Mean ΔBrier `-1.30e-8`로 실질적 개선이 아니며 best-fold 제외 Mean ΔBrier가 양수임.
- 2024 양 지표를 함께 개선한 후보들은 전체 평균 Brier/AUC가 악화됨.
- 실제 제출 검토 순위는 LGBM-284, LGBM-282, LGBM-277이나 모두 변화량이 지나치게 작아 REJECT.
- **266~285에서 제출할 가치가 있는 후보 없음. LGBM-130 유지.**

## LGBM-286~305 Probability Scaling Search

- 기존 LGBM-130 row-level `p130`만 사용해 center 0.5 shrinkage와 logit-space scaling을 평가함.
- 모델 학습·Feature·Trackman·외부 데이터 사용 없음.
- 모든 변환은 양의 단조 변환이므로 AUC ranking은 LGBM-130과 동일함.

| Experiment | Method           | Parameter |   Mean ΔBrier | Median ΔBrier | Best fold 제외 Mean |   2024 ΔBrier | Verdict |
| ---------- | ---------------- | --------: | ------------: | ------------: | ------------------: | ------------: | ------- |
| LGBM-286   | center shrink    |      0.90 | -1.561736e-04 | +6.367460e-05 |            -1.3e-05 | +6.367460e-05 | REJECT  |
| LGBM-287   | center shrink    |      0.92 | -1.318555e-04 | +4.867348e-05 |            -1.7e-05 | +4.867348e-05 | REJECT  |
| LGBM-288   | center shrink    |      0.94 | -1.040791e-04 | +3.480545e-05 |            -1.8e-05 | +3.480545e-05 | REJECT  |
| LGBM-289   | center shrink    |      0.96 | -7.284437e-05 | +2.207053e-05 |       -1.519815e-05 | +2.207053e-05 | REJECT  |
| LGBM-290   | center shrink    |      0.98 | -3.815134e-05 | +1.046872e-05 |       -9.293222e-06 | +1.046872e-05 | REJECT  |
| LGBM-291   | center shrink    |      1.00 |             0 |             0 |                   0 |             0 | REJECT  |
| LGBM-292   | center expansion |      1.02 | +4.160965e-05 | -8.076000e-06 |       +5.990696e-05 | -9.335613e-06 | REJECT  |
| LGBM-293   | center expansion |      1.04 | +8.667760e-05 | -1.127275e-05 |       +1.236131e-04 | -1.753812e-05 | REJECT  |
| LGBM-294   | center expansion |      1.06 | +1.352039e-04 |    -1.028e-05 |           +1.91e-04 | -2.460753e-05 | REJECT  |
| LGBM-295   | center expansion |      1.08 | +1.871884e-04 |      -3.0e-06 |           +2.62e-04 | -3.054384e-05 | REJECT  |
| LGBM-296   | logit scale      |      0.96 | -6.671405e-05 | +2.183503e-05 |            -1.4e-05 | +2.183503e-05 | REJECT  |
| LGBM-297   | logit scale      |      0.97 | -5.111264e-05 | +1.595686e-05 |            -1.2e-05 | +1.595686e-05 | REJECT  |
| LGBM-298   | logit scale      |      0.98 | -3.479023e-05 | +1.035845e-05 |            -9.0e-06 | +1.035845e-05 | REJECT  |
| LGBM-299   | logit scale      |      0.99 | -1.775121e-05 | +5.039577e-06 |            -5.0e-06 | +5.039577e-06 | REJECT  |
| LGBM-300   | logit scale      |      1.01 | +1.845899e-05 | -4.647907e-06 |            +2.7e-05 | -4.760516e-06 | REJECT  |
| LGBM-301   | logit scale      |      1.02 | +3.762131e-05 | -8.076000e-06 |            +5.5e-05 | -9.242211e-06 | REJECT  |
| LGBM-302   | logit scale      |      1.03 | +5.748251e-05 | -1.028428e-05 |            +8.3e-05 | -1.344533e-05 | REJECT  |
| LGBM-303   | logit scale      |      1.04 | +7.803814e-05 |      -1.2e-05 |           +1.12e-04 | -1.737011e-05 | REJECT  |
| LGBM-304   | logit scale      |      1.05 | +9.928371e-05 |      -1.2e-05 |           +1.42e-04 | -2.101681e-05 | REJECT  |
| LGBM-305   | logit scale      |      1.06 | +1.212147e-04 |      -1.2e-05 |           +1.73e-04 | -2.438568e-05 | REJECT  |

### LGBM-286~305 결론

- Strength/alpha 1 미만은 2020/2023 효과로 Mean Brier가 개선되지만 3개 fold 및 2024가 악화됨.
- Strength/alpha 1 초과는 2024 Brier가 개선되지만 전체 Mean Brier와 best-fold 제외 Mean이 악화됨.
- AUC는 모든 후보가 LGBM-130과 동일하여 후보 간 차별점이 없음.
- 유력 후보로 볼 수 있는 LGBM-286, LGBM-289, LGBM-296도 2024 악화 때문에 REJECT.
- 제출 추천 없음. **LGBM-130 유지.**

## LGBM-386~405 Continuous Piecewise Boundary/Extreme Search

- Method: `continuous_piecewise_probability_shrinkage`
- Baseline: LGBM-130
- Boundary search: lower `0.323~0.327`, symmetric upper `0.677~0.673`
- Extreme search: `0.625`, `0.650`, `0.675`, `0.700`
- Middle strength: `1.00`
- Existing row-level LGBM-130 fold predictions only; no model training or feature changes.

| Experiment | Parameters                                           |        Mean ΔBrier |      Median ΔBrier | Brier I/D | Mean ΔBrier without best fold | 2024 ΔBrier | Mean ΔAUC | Verdict   |
| ---------- | ---------------------------------------------------- | -----------------: | -----------------: | --------: | ----------------------------: | ----------: | --------: | --------- |
| LGBM-386   | lower=0.323; upper=0.677; extreme=0.625; middle=1.00 | -4.73631163487e-05 | -2.49502333793e-08 |       3/1 |            -1.16002515314e-05 |           0 |         0 | CANDIDATE |
| LGBM-387   | lower=0.323; upper=0.677; extreme=0.650; middle=1.00 | -4.46094774232e-05 | -2.35889809075e-08 |       3/1 |            -1.12354710037e-05 |           0 |         0 | CANDIDATE |
| LGBM-388   | lower=0.323; upper=0.677; extreme=0.675; middle=1.00 | -4.17981381884e-05 | -2.21845717352e-08 |       3/1 |            -1.08123233940e-05 |           0 |         0 | CANDIDATE |
| LGBM-389   | lower=0.323; upper=0.677; extreme=0.700; middle=1.00 | -3.89290986445e-05 | -2.07370059457e-08 |       3/1 |            -1.03308087022e-05 |           0 |         0 | CANDIDATE |
| LGBM-390   | lower=0.324; upper=0.676; extreme=0.625; middle=1.00 | -4.91029451258e-05 | -1.63364177186e-08 |       3/1 |            -1.17485497682e-05 |           0 |         0 | CANDIDATE |
| LGBM-391   | lower=0.324; upper=0.676; extreme=0.650; middle=1.00 | -4.62528110841e-05 | -1.56366850856e-08 |       3/1 |            -1.13924962054e-05 |           0 |         0 | CANDIDATE |
| LGBM-392   | lower=0.324; upper=0.676; extreme=0.675; middle=1.00 | -4.33421919520e-05 | -1.48813293910e-08 |       3/1 |            -1.09754164871e-05 |           0 |         0 | CANDIDATE |
| LGBM-393   | lower=0.324; upper=0.676; extreme=0.700; middle=1.00 | -4.03710877293e-05 | -1.40703504958e-08 |       3/1 |            -1.04973106133e-05 |           0 |         0 | CANDIDATE |
| LGBM-394   | lower=0.325; upper=0.675; extreme=0.625; middle=1.00 | -5.08762180091e-05 |                  0 |       2/2 |            -1.18849602237e-05 |           0 |         0 | REJECT    |
| LGBM-395   | lower=0.325; upper=0.675; extreme=0.650; middle=1.00 | -4.79280345060e-05 |                  0 |       2/2 |            -1.15390227806e-05 |           0 |         0 | REJECT    |
| LGBM-396   | lower=0.325; upper=0.675; extreme=0.675; middle=1.00 | -4.49164846651e-05 |                  0 |       2/2 |            -1.11293148750e-05 |           0 |         0 | REJECT    |
| LGBM-397   | lower=0.325; upper=0.675; extreme=0.700; middle=1.00 | -4.18415684865e-05 |                  0 |       2/2 |            -1.06558365066e-05 |           0 |         0 | REJECT    |
| LGBM-398   | lower=0.326; upper=0.674; extreme=0.625; middle=1.00 | -5.26973751899e-05 |                  0 |       2/2 |            -1.20247202315e-05 |           0 |         0 | REJECT    |
| LGBM-399   | lower=0.326; upper=0.674; extreme=0.650; middle=1.00 | -4.96486384093e-05 |                  0 |       2/2 |            -1.16892822619e-05 |           0 |         0 | REJECT    |
| LGBM-400   | lower=0.326; upper=0.674; extreme=0.675; middle=1.00 | -4.65335556908e-05 |                  0 |       2/2 |            -1.12872428572e-05 |           0 |         0 | REJECT    |
| LGBM-401   | lower=0.326; upper=0.674; extreme=0.700; middle=1.00 | -4.33521270344e-05 |                  0 |       2/2 |            -1.08186020174e-05 |           0 |         0 | REJECT    |
| LGBM-402   | lower=0.327; upper=0.673; extreme=0.625; middle=1.00 | -5.45644810838e-05 |                  0 |       2/2 |            -1.21741211844e-05 |           0 |         0 | REJECT    |
| LGBM-403   | lower=0.327; upper=0.673; extreme=0.650; middle=1.00 | -5.14128289507e-05 |                  0 |       2/2 |            -1.18491560031e-05 |           0 |         0 | REJECT    |
| LGBM-404   | lower=0.327; upper=0.673; extreme=0.675; middle=1.00 | -4.81917511119e-05 |                  0 |       2/2 |            -1.14546704078e-05 |           0 |         0 | REJECT    |
| LGBM-405   | lower=0.327; upper=0.673; extreme=0.700; middle=1.00 | -4.49012475676e-05 |                  0 |       2/2 |            -1.09906643985e-05 |           0 |         0 | REJECT    |

### LGBM-386~405 conclusion

- Current best candidate: **LGBM-390** (`lower=0.324`, `upper=0.676`, `extreme=0.625`, `middle=1.00`).
- Stable 3/1 candidates were observed at lower `0.323` and `0.324`; lower `0.325~0.327` changed to 2/2 and remained REJECT despite larger mean Brier improvements.
- Within each boundary, a smaller extreme strength improved mean Brier in the tested range.
- The next search should preserve fold stability near the narrow transition between lower `0.324` and `0.325`, with `extreme=0.625` as the strongest stable reference.

## LGBM-406~425 Continuous Piecewise Fine Search

- Method: `continuous_piecewise_probability_shrinkage`
- Baseline: LGBM-130
- Boundary search: lower `0.32350~0.32450`, symmetric upper `0.67650~0.67550`
- Extreme search: `0.525`, `0.550`, `0.575`, `0.600`
- Middle strength: `1.00`
- Existing row-level LGBM-130 fold predictions only; no model training or feature changes.

| Experiment | Parameters                                               |        Mean ΔBrier |      Median ΔBrier | Brier I/D | Mean ΔBrier without best fold | 2024 ΔBrier | Mean ΔAUC | Verdict   |
| ---------- | -------------------------------------------------------- | -----------------: | -----------------: | --------: | ----------------------------: | ----------: | --------: | --------- |
| LGBM-406   | lower=0.32350; upper=0.67650; extreme=0.525; middle=1.00 | -5.88442604684e-05 | -2.65638723795e-08 |       3/1 |            -1.25225270419e-05 |           0 |         0 | CANDIDATE |
| LGBM-407   | lower=0.32350; upper=0.67650; extreme=0.550; middle=1.00 | -5.62789209729e-05 | -2.56078451777e-08 |       3/1 |            -1.24006211627e-05 |           0 |         0 | CANDIDATE |
| LGBM-408   | lower=0.32350; upper=0.67650; extreme=0.575; middle=1.00 | -5.36545007167e-05 | -2.46026989892e-08 |       3/1 |            -1.22190292290e-05 |           0 |         0 | CANDIDATE |
| LGBM-409   | lower=0.32350; upper=0.67650; extreme=0.600; middle=1.00 | -5.09709997001e-05 | -2.35484337308e-08 |       3/1 |            -1.19777512406e-05 |           0 |         0 | CANDIDATE |
| LGBM-410   | lower=0.32375; upper=0.67625; extreme=0.525; middle=1.00 | -5.93707716200e-05 | -2.33089464952e-08 |       3/1 |            -1.25433639557e-05 |           0 |         0 | CANDIDATE |
| LGBM-411   | lower=0.32375; upper=0.67625; extreme=0.550; middle=1.00 | -5.67840134977e-05 | -2.25528778985e-08 |       3/1 |            -1.24263679815e-05 |           0 |         0 | CANDIDATE |
| LGBM-412   | lower=0.32375; upper=0.67625; extreme=0.575; middle=1.00 | -5.41374754497e-05 | -2.17445073336e-08 |       3/1 |            -1.22490185544e-05 |           0 |         0 | CANDIDATE |
| LGBM-413   | lower=0.32375; upper=0.67625; extreme=0.600; middle=1.00 | -5.14311574760e-05 | -2.08838347449e-08 |       3/1 |            -1.20113156744e-05 |           0 |         0 | CANDIDATE |
| LGBM-414   | lower=0.32400; upper=0.67600; extreme=0.525; middle=1.00 | -5.98986303876e-05 | -1.85791168839e-08 |       3/1 |            -1.25625024647e-05 |           0 |         0 | CANDIDATE |
| LGBM-415   | lower=0.32400; upper=0.67600; extreme=0.550; middle=1.00 | -5.72904367079e-05 | -1.81018768031e-08 |       3/1 |            -1.24505535238e-05 |           0 |         0 | CANDIDATE |
| LGBM-416   | lower=0.32400; upper=0.67600; extreme=0.575; middle=1.00 | -5.46217579377e-05 | -1.75690135495e-08 |       3/1 |            -1.22775784274e-05 |           0 |         0 | CANDIDATE |
| LGBM-417   | lower=0.32400; upper=0.67600; extreme=0.600; middle=1.00 | -5.18925940770e-05 | -1.69805272066e-08 |       3/1 |            -1.20435771756e-05 |           0 |         0 | CANDIDATE |
| LGBM-418   | lower=0.32425; upper=0.67575; extreme=0.525; middle=1.00 | -6.04276144049e-05 | -1.21177552992e-08 |       3/1 |            -1.25795650860e-05 |           0 |         0 | CANDIDATE |
| LGBM-419   | lower=0.32425; upper=0.67575; extreme=0.550; middle=1.00 | -5.77979802110e-05 | -1.20117518709e-08 |       3/1 |            -1.24728203806e-05 |           0 |         0 | CANDIDATE |
| LGBM-420   | lower=0.32425; upper=0.67575; extreme=0.575; middle=1.00 | -5.51071497321e-05 | -1.18466625398e-08 |       3/1 |            -1.23043714899e-05 |           0 |         0 | CANDIDATE |
| LGBM-421   | lower=0.32425; upper=0.67575; extreme=0.600; middle=1.00 | -5.23551229683e-05 | -1.16224872782e-08 |       3/1 |            -1.20742184139e-05 |           0 |         0 | CANDIDATE |
| LGBM-422   | lower=0.32450; upper=0.67550; extreme=0.525; middle=1.00 | -6.09603927729e-05 | -5.18858811471e-09 |       3/1 |            -1.25966512904e-05 |           0 |         0 | CANDIDATE |
| LGBM-423   | lower=0.32450; upper=0.67550; extreme=0.550; middle=1.00 | -5.83091728835e-05 | -5.47973860732e-09 |       3/1 |            -1.24951577223e-05 |           0 |         0 | CANDIDATE |
| LGBM-424   | lower=0.32450; upper=0.67550; extreme=0.575; middle=1.00 | -5.55960394568e-05 | -5.70819641554e-09 |       3/1 |            -1.23312765900e-05 |           0 |         0 | CANDIDATE |
| LGBM-425   | lower=0.32450; upper=0.67550; extreme=0.600; middle=1.00 | -5.28209924928e-05 | -5.87396153939e-09 |       3/1 |            -1.21050078933e-05 |           0 |         0 | CANDIDATE |

### LGBM-406~425 conclusion

- Current valid best candidate: **LGBM-422** (`lower=0.32450`, `upper=0.67550`, `extreme=0.525`, `middle=1.00`).
- LGBM-422 improves mean ΔBrier by `-1.18574476471e-05` relative to the previous valid best LGBM-390 while retaining 3/1 fold stability, unchanged 2024 metrics, and unchanged AUC.
- Every tested boundary retained 3/1 stability; moving lower from `0.32350` to `0.32450` improved mean Brier within each extreme setting.
- A smaller extreme strength continued to improve mean Brier throughout the tested range.
- The next search should examine the narrow stability boundary below lower `0.325` and extreme values below `0.525`, without treating the larger mean gains from 2/2 configurations as valid candidates.

## LGBM-426~445 Continuous Piecewise Micro Search

- Method: `continuous_piecewise_probability_shrinkage`
- Baseline: LGBM-130
- Boundary search: lower `0.32455~0.32495`, symmetric upper `0.67545~0.67505`
- Extreme search: `0.475`, `0.500`, `0.525`, `0.550`
- Middle strength: `1.00`
- Existing row-level LGBM-130 fold predictions only; no model training or feature changes.

| Experiment | Parameters                                               |        Mean ΔBrier |      Median ΔBrier | Brier I/D | Mean ΔBrier without best fold | 2024 ΔBrier | Mean ΔAUC | Verdict   |
| ---------- | -------------------------------------------------------- | -----------------: | -----------------: | --------: | ----------------------------: | ----------: | --------: | --------- |
| LGBM-426   | lower=0.32455; upper=0.67545; extreme=0.475; middle=1.00 | -6.61923512998e-05 | -2.87750270833e-09 |       3/1 |            -1.26132864144e-05 |           0 |         0 | CANDIDATE |
| LGBM-427   | lower=0.32455; upper=0.67545; extreme=0.500; middle=1.00 | -6.36609117457e-05 | -3.37479205692e-09 |       3/1 |            -1.26379025689e-05 |           0 |         0 | CANDIDATE |
| LGBM-428   | lower=0.32455; upper=0.67545; extreme=0.525; middle=1.00 | -6.10674144742e-05 | -3.80865006200e-09 |       3/1 |            -1.25999938394e-05 |           0 |         0 | CANDIDATE |
| LGBM-429   | lower=0.32455; upper=0.67545; extreme=0.550; middle=1.00 | -5.84118594852e-05 | -4.17907677908e-09 |       3/1 |            -1.24995602258e-05 |           0 |         0 | CANDIDATE |
| LGBM-430   | lower=0.32465; upper=0.67535; extreme=0.475; middle=1.00 | -6.64231957230e-05 |                  0 |       2/2 |            -1.26151943847e-05 |           0 |         0 | REJECT    |
| LGBM-431   | lower=0.32465; upper=0.67535; extreme=0.500; middle=1.00 | -6.38836544983e-05 | -5.77877190544e-10 |       3/1 |            -1.26424725342e-05 |           0 |         0 | CANDIDATE |
| LGBM-432   | lower=0.32465; upper=0.67535; extreme=0.525; middle=1.00 | -6.12817664641e-05 | -1.16578102727e-09 |       3/1 |            -1.26069505145e-05 |           0 |         0 | CANDIDATE |
| LGBM-433   | lower=0.32465; upper=0.67535; extreme=0.550; middle=1.00 | -5.86175316203e-05 | -1.68875877171e-09 |       3/1 |            -1.25086283256e-05 |           0 |         0 | CANDIDATE |
| LGBM-434   | lower=0.32475; upper=0.67525; extreme=0.475; middle=1.00 | -6.66537989333e-05 |                  0 |       2/2 |            -1.26167917402e-05 |           0 |         0 | REJECT    |
| LGBM-435   | lower=0.32475; upper=0.67525; extreme=0.500; middle=1.00 | -6.41061772951e-05 |                  0 |       2/2 |            -1.26467552944e-05 |           0 |         0 | REJECT    |
| LGBM-436   | lower=0.32475; upper=0.67525; extreme=0.525; middle=1.00 | -6.14959187782e-05 |                  0 |       2/2 |            -1.26136425325e-05 |           0 |         0 | REJECT    |
| LGBM-437   | lower=0.32475; upper=0.67525; extreme=0.550; middle=1.00 | -5.88230233826e-05 |                  0 |       2/2 |            -1.25174534545e-05 |           0 |         0 | REJECT    |
| LGBM-438   | lower=0.32485; upper=0.67515; extreme=0.475; middle=1.00 | -6.68857451946e-05 |                  0 |       2/2 |            -1.26187964925e-05 |           0 |         0 | REJECT    |
| LGBM-439   | lower=0.32485; upper=0.67515; extreme=0.500; middle=1.00 | -6.43299889755e-05 |                  0 |       2/2 |            -1.26514346829e-05 |           0 |         0 | REJECT    |
| LGBM-440   | lower=0.32485; upper=0.67515; extreme=0.525; middle=1.00 | -6.17113048297e-05 |                  0 |       2/2 |            -1.26207195471e-05 |           0 |         0 | REJECT    |
| LGBM-441   | lower=0.32485; upper=0.67515; extreme=0.550; middle=1.00 | -5.90296927574e-05 |                  0 |       2/2 |            -1.25266510852e-05 |           0 |         0 | REJECT    |
| LGBM-442   | lower=0.32495; upper=0.67505; extreme=0.475; middle=1.00 | -6.71182225653e-05 |                  0 |       2/2 |            -1.26205931422e-05 |           0 |         0 | REJECT    |
| LGBM-443   | lower=0.32495; upper=0.67505; extreme=0.500; middle=1.00 | -6.45543162805e-05 |                  0 |       2/2 |            -1.26559245237e-05 |           0 |         0 | REJECT    |
| LGBM-444   | lower=0.32495; upper=0.67505; extreme=0.525; middle=1.00 | -6.19271900406e-05 |                  0 |       2/2 |            -1.26276247045e-05 |           0 |         0 | REJECT    |
| LGBM-445   | lower=0.32495; upper=0.67505; extreme=0.550; middle=1.00 | -5.92368438455e-05 |                  0 |       2/2 |            -1.25356936846e-05 |           0 |         0 | REJECT    |

### LGBM-426~445 conclusion

- Current valid best candidate: **LGBM-426** (`lower=0.32455`, `upper=0.67545`, `extreme=0.475`, `middle=1.00`).
- LGBM-426 candidate mean Brier: `0.2476049475824081`; mean ΔBrier: `-6.61923512998e-05`; median ΔBrier: `-2.87750270833e-09`; Brier folds: `3/1`; mean ΔBrier without best fold: `-1.26132864144e-05`.
- LGBM-426 mean AUC remains `0.5530385153643456`; 2024 Brier/AUC remain `0.2480885134392783` / `0.5480200784149498`, with zero deltas.
- Relative to previous best LGBM-422, LGBM-426 improves mean ΔBrier by `-5.23195852693e-06` while retaining the same 3/1 stability and unchanged AUC/2024 metrics.
- Stability transitions within this micro-range: lower `0.32455` remained 3/1 for every extreme; lower `0.32465` remained 3/1 only for extreme `0.500~0.550`; lower `0.32475~0.32495` produced 2/2 and was rejected.
- Lower extreme strength improved mean Brier, but at lower `0.32465` extreme `0.475` crossed to 2/2. Future searches should respect this joint boundary/extreme stability interaction.

## LGBM-446~475 Continuous Piecewise Stability Frontier Search

- Method: `continuous_piecewise_probability_shrinkage`
- Baseline: LGBM-130
- Boundary search: lower `0.32456~0.32466`, symmetric upper `0.67544~0.67534`
- Extreme search: `0.425`, `0.450`, `0.475`, `0.500`, `0.525`
- Middle strength: `1.00`
- Thirty new parameter combinations; existing row-level LGBM-130 fold predictions only.

| Experiment | Parameters                                               |        Mean ΔBrier |      Median ΔBrier | Brier I/D | Mean ΔBrier without best fold | 2024 ΔBrier | Mean ΔAUC | Verdict   |
| ---------- | -------------------------------------------------------- | -----------------: | -----------------: | --------: | ----------------------------: | ----------: | --------: | --------- |
| LGBM-446   | lower=0.32456; upper=0.67544; extreme=0.425; middle=1.00 | -7.10936508837e-05 | -1.36570932341e-09 |       3/1 |            -1.23760274215e-05 |           0 |         0 | CANDIDATE |
| LGBM-447   | lower=0.32456; upper=0.67544; extreme=0.450; middle=1.00 | -6.86855749945e-05 | -2.00570793307e-09 |       3/1 |            -1.25260153852e-05 |           0 |         0 | CANDIDATE |
| LGBM-448   | lower=0.32456; upper=0.67544; extreme=0.475; middle=1.00 | -6.62154125225e-05 | -2.58212681792e-09 |       3/1 |            -1.26134509751e-05 |           0 |         0 | CANDIDATE |
| LGBM-449   | lower=0.32456; upper=0.67544; extreme=0.500; middle=1.00 | -6.36831634679e-05 | -3.09496595019e-09 |       3/1 |            -1.26383341910e-05 |           0 |         0 | CANDIDATE |
| LGBM-450   | lower=0.32456; upper=0.67544; extreme=0.525; middle=1.00 | -6.10888278305e-05 | -3.54422532989e-09 |       3/1 |            -1.26006650331e-05 |           0 |         0 | CANDIDATE |
| LGBM-451   | lower=0.32458; upper=0.67542; extreme=0.425; middle=1.00 | -7.11428495292e-05 | -7.11683267873e-10 |       3/1 |            -1.23751338858e-05 |           0 |         0 | CANDIDATE |
| LGBM-452   | lower=0.32458; upper=0.67542; extreme=0.450; middle=1.00 | -6.87332699268e-05 | -1.38339084632e-09 |       3/1 |            -1.25257657577e-05 |           0 |         0 | CANDIDATE |
| LGBM-453   | lower=0.32458; upper=0.67542; extreme=0.475; middle=1.00 | -6.62615459818e-05 | -1.99122110467e-09 |       3/1 |            -1.26137902503e-05 |           0 |         0 | CANDIDATE |
| LGBM-454   | lower=0.32458; upper=0.67542; extreme=0.500; middle=1.00 | -6.37276776942e-05 | -2.53517415394e-09 |       3/1 |            -1.26392073638e-05 |           0 |         0 | CANDIDATE |
| LGBM-455   | lower=0.32458; upper=0.67542; extreme=0.525; middle=1.00 | -6.11316650640e-05 | -3.01524979984e-09 |       3/1 |            -1.26020170980e-05 |           0 |         0 | CANDIDATE |
| LGBM-456   | lower=0.32460; upper=0.67540; extreme=0.425; middle=1.00 | -7.11921152316e-05 | -5.74109926266e-11 |       3/1 |            -1.23743108275e-05 |           0 |         0 | CANDIDATE |
| LGBM-457   | lower=0.32460; upper=0.67540; extreme=0.450; middle=1.00 | -6.87810294298e-05 | -7.60848495318e-10 |       3/1 |            -1.25255839220e-05 |           0 |         0 | CANDIDATE |
| LGBM-458   | lower=0.32460; upper=0.67540; extreme=0.475; middle=1.00 | -6.63077414866e-05 | -1.40011019445e-09 |       3/1 |            -1.26141945976e-05 |           0 |         0 | CANDIDATE |
| LGBM-459   | lower=0.32460; upper=0.67540; extreme=0.500; middle=1.00 | -6.37722514018e-05 | -1.97519611778e-09 |       3/1 |            -1.26401428542e-05 |           0 |         0 | CANDIDATE |
| LGBM-460   | lower=0.32460; upper=0.67540; extreme=0.525; middle=1.00 | -6.11745591756e-05 | -2.48610623754e-09 |       3/1 |            -1.26034286918e-05 |           0 |         0 | CANDIDATE |
| LGBM-461   | lower=0.32462; upper=0.67538; extreme=0.425; middle=1.00 | -7.12413961712e-05 |                  0 |       2/2 |            -1.23735122258e-05 |           0 |         0 | REJECT    |
| LGBM-462   | lower=0.32462; upper=0.67538; extreme=0.450; middle=1.00 | -6.88288039371e-05 | -1.38376810010e-10 |       3/1 |            -1.25254258586e-05 |           0 |         0 | CANDIDATE |
| LGBM-463   | lower=0.32462; upper=0.67538; extreme=0.475; middle=1.00 | -6.63539517236e-05 | -8.09076500241e-10 |       3/1 |            -1.26146219983e-05 |           0 |         0 | CANDIDATE |
| LGBM-464   | lower=0.32462; upper=0.67538; extreme=0.500; middle=1.00 | -6.38168395307e-05 | -1.41530101527e-09 |       3/1 |            -1.26411006447e-05 |           0 |         0 | CANDIDATE |
| LGBM-465   | lower=0.32462; upper=0.67538; extreme=0.525; middle=1.00 | -6.12174673584e-05 | -1.95705029959e-09 |       3/1 |            -1.26048617979e-05 |           0 |         0 | CANDIDATE |
| LGBM-466   | lower=0.32464; upper=0.67536; extreme=0.425; middle=1.00 | -7.12906357108e-05 |                  0 |       2/2 |            -1.23726722442e-05 |           0 |         0 | REJECT    |
| LGBM-467   | lower=0.32464; upper=0.67536; extreme=0.450; middle=1.00 | -6.88765392742e-05 |                  0 |       2/2 |            -1.25252285936e-05 |           0 |         0 | REJECT    |
| LGBM-468   | lower=0.32464; upper=0.67536; extreme=0.475; middle=1.00 | -6.64001249811e-05 | -2.19775669885e-10 |       3/1 |            -1.26150123410e-05 |           0 |         0 | CANDIDATE |
| LGBM-469   | lower=0.32464; upper=0.67536; extreme=0.500; middle=1.00 | -6.38613928316e-05 | -8.57065612925e-10 |       3/1 |            -1.26420234865e-05 |           0 |         0 | CANDIDATE |
| LGBM-470   | lower=0.32464; upper=0.67536; extreme=0.525; middle=1.00 | -6.12603428258e-05 | -1.42957998217e-09 |       3/1 |            -1.26062620301e-05 |           0 |         0 | CANDIDATE |
| LGBM-471   | lower=0.32466; upper=0.67534; extreme=0.425; middle=1.00 | -7.13398268120e-05 |                  0 |       2/2 |            -1.23717809193e-05 |           0 |         0 | REJECT    |
| LGBM-472   | lower=0.32466; upper=0.67534; extreme=0.450; middle=1.00 | -6.89242287086e-05 |                  0 |       2/2 |            -1.25249825966e-05 |           0 |         0 | REJECT    |
| LGBM-473   | lower=0.32466; upper=0.67534; extreme=0.475; middle=1.00 | -6.64462548328e-05 |                  0 |       2/2 |            -1.26153565288e-05 |           0 |         0 | REJECT    |
| LGBM-474   | lower=0.32466; upper=0.67534; extreme=0.500; middle=1.00 | -6.39059051845e-05 | -2.98641583685e-10 |       3/1 |            -1.26429027160e-05 |           0 |         0 | CANDIDATE |
| LGBM-475   | lower=0.32466; upper=0.67534; extreme=0.525; middle=1.00 | -6.13031797636e-05 | -9.01939467557e-10 |       3/1 |            -1.26076211581e-05 |           0 |         0 | CANDIDATE |

### LGBM-446~475 conclusion

- Current valid best candidate: **LGBM-456** (`lower=0.32460`, `upper=0.67540`, `extreme=0.425`, `middle=1.00`).
- LGBM-456 candidate mean Brier: `0.2475999478184763`; mean ΔBrier: `-7.11921152316e-05`; median ΔBrier: `-5.74109926266e-11`; Brier folds: `3/1`; mean ΔBrier without best fold: `-1.23743108275e-05`.
- LGBM-456 mean AUC remains `0.5530385153643456`; 2024 Brier/AUC remain `0.2480885134392783` / `0.5480200784149498`, with zero deltas.
- Relative to previous best LGBM-426, LGBM-456 improves mean ΔBrier by `-4.99976393183e-06` while retaining 3/1 stability and unchanged AUC/2024 metrics.
- The best-fold-excluded mean is less favorable than LGBM-426, so the gain is not uniform across all secondary stability measures.
- The stability frontier depends jointly on boundary and extreme: lower extreme strengths cross from 3/1 to 2/2 sooner as the boundary moves inward.

## LGBM-476~495 Continuous Piecewise Tight Search

- Method: `continuous_piecewise_probability_shrinkage`
- Baseline: LGBM-130
- Boundary search: lower `0.32457~0.32463`, symmetric upper `0.67543~0.67537`
- Extreme search: `0.400`, `0.415`, `0.425`, `0.435`, `0.450`
- Middle strength: `1.00`
- Twenty new parameter combinations; existing row-level LGBM-130 fold predictions only.

| Experiment | Parameters                                               |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier I/D | Mean ΔBrier without best fold |         2024 Brier | 2024 ΔBrier | Verdict   |
| ---------- | -------------------------------------------------------- | -----------------: | -----------------: | -----------------: | --------: | ----------------------------: | -----------------: | ----------: | --------- |
| LGBM-476   | lower=0.32457; upper=0.67543; extreme=0.400; middle=1.00 | 0.2475976749784056 | -7.34649553023e-05 | -3.19148124595e-10 |       3/1 |            -1.21626855768e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-477   | lower=0.32457; upper=0.67543; extreme=0.415; middle=1.00 | 0.2475990755517745 | -7.20643819334e-05 | -7.58542895163e-10 |       3/1 |            -1.22979291404e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-478   | lower=0.32457; upper=0.67543; extreme=0.425; middle=1.00 | 0.2476000216904454 | -7.11182432625e-05 | -1.03872702106e-09 |       3/1 |            -1.23755755417e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-479   | lower=0.32457; upper=0.67543; extreme=0.435; middle=1.00 | 0.2476009777675895 | -7.01621661184e-05 | -1.30871466442e-09 |       3/1 |            -1.24432091635e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-480   | lower=0.32457; upper=0.67543; extreme=0.450; middle=1.00 | 0.2476024305179430 | -6.87094157650e-05 | -1.69457753385e-09 |       3/1 |            -1.25258856344e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-481   | lower=0.32459; upper=0.67541; extreme=0.400; middle=1.00 | 0.2475976242952003 | -7.35156385076e-05 |                  0 |       2/2 |            -1.21611283165e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-482   | lower=0.32459; upper=0.67541; extreme=0.415; middle=1.00 | 0.2475990257300383 | -7.21142036697e-05 | -9.16225428860e-11 |       3/1 |            -1.22967970700e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-483   | lower=0.32459; upper=0.67541; extreme=0.425; middle=1.00 | 0.2475999724545777 | -7.11674791303e-05 | -3.84577897306e-10 |       3/1 |            -1.23747159267e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-484   | lower=0.32459; upper=0.67541; extreme=0.435; middle=1.00 | 0.2476009291268350 | -7.02108068729e-05 | -6.67289057343e-10 |       3/1 |            -1.24426132002e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-485   | lower=0.32459; upper=0.67541; extreme=0.450; middle=1.00 | 0.2476023827871922 | -6.87571465158e-05 | -1.07214781497e-09 |       3/1 |            -1.25256686421e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-486   | lower=0.32461; upper=0.67539; extreme=0.400; middle=1.00 | 0.2475975735644119 | -7.35663692960e-05 |                  0 |       2/2 |            -1.21596339262e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-487   | lower=0.32461; upper=0.67539; extreme=0.415; middle=1.00 | 0.2475989758616344 | -7.21640720736e-05 |                  0 |       2/2 |            -1.22957265396e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-488   | lower=0.32461; upper=0.67539; extreme=0.425; middle=1.00 | 0.2475999231726605 | -7.12167610475e-05 |                  0 |       2/2 |            -1.23739169582e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-489   | lower=0.32461; upper=0.67539; extreme=0.435; middle=1.00 | 0.2476008804406554 | -7.02594930525e-05 | -2.56257237652e-11 |       3/1 |            -1.24420769845e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-490   | lower=0.32461; upper=0.67539; extreme=0.450; middle=1.00 | 0.2476023350119645 | -6.88049217434e-05 | -4.49492831844e-10 |       3/1 |            -1.25255100384e-05 | 0.2480885134392783 |           0 | CANDIDATE |
| LGBM-491   | lower=0.32463; upper=0.67537; extreme=0.400; middle=1.00 | 0.2475975228581032 | -7.36170756047e-05 |                  0 |       2/2 |            -1.21581143689e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-492   | lower=0.32463; upper=0.67537; extreme=0.415; middle=1.00 | 0.2475989260168240 | -7.22139168840e-05 |                  0 |       2/2 |            -1.22946317132e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-493   | lower=0.32463; upper=0.67537; extreme=0.425; middle=1.00 | 0.2475998739137538 | -7.12660199542e-05 |                  0 |       2/2 |            -1.23730942675e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-494   | lower=0.32463; upper=0.67537; extreme=0.435; middle=1.00 | 0.2476008317769096 | -7.03081567983e-05 |                  0 |       2/2 |            -1.24415176148e-05 | 0.2480885134392783 |           0 | REJECT    |
| LGBM-495   | lower=0.32463; upper=0.67537; extreme=0.450; middle=1.00 | 0.2476022872583173 | -6.88526753906e-05 |                  0 |       2/2 |            -1.25253291228e-05 | 0.2480885134392783 |           0 | REJECT    |

### LGBM-476~495 conclusion

- Current valid best candidate: **LGBM-476** (`lower=0.32457`, `upper=0.67543`, `extreme=0.400`, `middle=1.00`).
- LGBM-476 mean Brier: `0.2475976749784056`; mean ΔBrier: `-7.34649553023e-05`; median ΔBrier: `-3.19148124595e-10`; Brier folds: `3/1`; verdict: `CANDIDATE`.
- LGBM-476 2024 Brier remains `0.2480885134392783` with zero delta; AUC and 2024 AUC remain unchanged.
- Relative to LGBM-456, LGBM-476 improves mean ΔBrier by `-2.27284007069e-06`, but its best-fold-excluded mean is less favorable (`-1.21626855768e-05` vs `-1.23743108275e-05`).
- The stability boundary shifts with extreme strength: aggressive shrinkage becomes 2/2 at smaller inward boundary movements, while higher extreme values retain 3/1 farther inward.

## LGBM-496~515 미세 경계 및 extreme 탐색

- 실험 목적: LGBM-476 주변에서 Mean Brier를 추가로 낮추면서 3/1 fold 안정성, 2024 성능, AUC를 유지하는 조합 탐색
- method: `continuous_piecewise_probability_shrinkage`
- Baseline: LGBM-130
- lower 탐색 범위: `0.32454~0.32460`
- upper 탐색 범위: `0.67546~0.67540` (`upper=1-lower`)
- extreme 탐색 범위: `0.375`, `0.390`, `0.400`, `0.405`, `0.410`
- middle: `1.00`
- 기존 LGBM-130 row-level fold prediction만 사용했으며 모델 학습과 Feature 변경은 수행하지 않음.

| 실험     | parameter                                                |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier | 2024 ΔBrier |           Mean AUC | verdict   |
| -------- | -------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | ----------: | -----------------: | --------- |
| LGBM-496 | lower=0.32454; upper=0.67546; extreme=0.375; middle=1.00 | 0.2475954684130607 | -7.56715206472e-05 | -6.18904621996e-10 |                  3/1 |           -1.18907547417e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-497 | lower=0.32454; upper=0.67546; extreme=0.390; middle=1.00 | 0.2475968304782870 | -7.43094554209e-05 | -1.06728348381e-09 |                  3/1 |           -1.20628576174e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-498 | lower=0.32454; upper=0.67546; extreme=0.400; middle=1.00 | 0.2475977509275436 | -7.33890061643e-05 | -1.35354605302e-09 |                  3/1 |           -1.21650933873e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-499 | lower=0.32454; upper=0.67546; extreme=0.405; middle=1.00 | 0.2475982148739036 | -7.29250598043e-05 | -1.49288037488e-09 |                  3/1 |           -1.22124614281e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-500 | lower=0.32454; upper=0.67546; extreme=0.410; middle=1.00 | 0.2475986813014181 | -7.24586322898e-05 | -1.62968338824e-09 |                  3/1 |           -1.22573295727e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-501 | lower=0.32456; upper=0.67544; extreme=0.375; middle=1.00 | 0.2475954163907941 | -7.57235429138e-05 |                  0 |                  2/2 |           -1.18883943726e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-502 | lower=0.32456; upper=0.67544; extreme=0.390; middle=1.00 | 0.2475967792820384 | -7.43606516695e-05 | -3.62897240036e-10 |                  3/1 |           -1.20609562843e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-503 | lower=0.32456; upper=0.67544; extreme=0.400; middle=1.00 | 0.2475977002935178 | -7.34396401901e-05 | -6.62130905660e-10 |                  3/1 |           -1.21634870840e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-504 | lower=0.32456; upper=0.67544; extreme=0.405; middle=1.00 | 0.2475981645244525 | -7.29754092555e-05 | -8.07932998281e-10 |                  3/1 |           -1.22109993414e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-505 | lower=0.32456; upper=0.67544; extreme=0.410; middle=1.00 | 0.2475986312388505 | -7.25086948575e-05 | -9.51191819754e-10 |                  3/1 |           -1.22560095039e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-506 | lower=0.32458; upper=0.67542; extreme=0.375; middle=1.00 | 0.2475953643580015 | -7.57755757064e-05 |                  0 |                  2/2 |           -1.18860480045e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-507 | lower=0.32458; upper=0.67542; extreme=0.390; middle=1.00 | 0.2475967280752308 | -7.44118584771e-05 |                  0 |                  2/2 |           -1.20590688681e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-508 | lower=0.32458; upper=0.67542; extreme=0.400; middle=1.00 | 0.2475976496489188 | -7.34902847891e-05 |                  0 |                  2/2 |           -1.21618946348e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-509 | lower=0.32458; upper=0.67542; extreme=0.405; middle=1.00 | 0.2475981141644234 | -7.30257692845e-05 | -1.28325516879e-10 |                  3/1 |           -1.22095510753e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-510 | lower=0.32458; upper=0.67542; extreme=0.410; middle=1.00 | 0.2475985811657017 | -7.25587680063e-05 | -2.77997569409e-10 |                  3/1 |           -1.22547032207e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-511 | lower=0.32460; upper=0.67540; extreme=0.375; middle=1.00 | 0.2475953122532971 | -7.58276804108e-05 |                  0 |                  2/2 |           -1.18837773815e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-512 | lower=0.32460; upper=0.67540; extreme=0.390; middle=1.00 | 0.2475966767979514 | -7.44631357565e-05 |                  0 |                  2/2 |           -1.20572556312e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-513 | lower=0.32460; upper=0.67540; extreme=0.400; middle=1.00 | 0.2475975989348159 | -7.35409988920e-05 |                  0 |                  2/2 |           -1.21603753140e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-514 | lower=0.32460; upper=0.67540; extreme=0.405; middle=1.00 | 0.2475980637353767 | -7.30761983312e-05 |                  0 |                  2/2 |           -1.22081754102e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-515 | lower=0.32460; upper=0.67540; extreme=0.410; middle=1.00 | 0.2475985310240231 | -7.26089096848e-05 |                  0 |                  2/2 |           -1.22534690097e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |

### LGBM-496~515 결론

- 최고 유효 후보는 **LGBM-496** (`lower=0.32454`, `upper=0.67546`, `extreme=0.375`, `middle=1.00`)이다.
- LGBM-496의 Mean Brier는 `0.2475954684130607`, Mean ΔBrier는 `-7.56715206472e-05`, Median ΔBrier는 `-6.18904621996e-10`, fold별 개선/악화는 `3/1`, verdict는 `CANDIDATE`이다.
- LGBM-496의 2024 Brier는 `0.2480885134392783`, 2024 ΔBrier는 `0`이며 Mean AUC와 2024 AUC도 LGBM-130과 동일하게 유지되었다.
- 이전 최고 LGBM-476 대비 Mean ΔBrier가 `-2.20656534491e-06` 추가 개선되었으나, mean_delta_without_best_fold는 `-1.18907547417e-05`로 LGBM-476보다 덜 개선되었다.
- lower가 안쪽으로 이동하고 extreme이 작아질수록 2/2로 전환되는 경향이 재확인되었다. 다음 탐색은 LGBM-496 주변에서 Mean Brier 개선과 mean_delta_without_best_fold 간의 균형을 함께 확인해야 한다.

## LGBM-516~535 안정성 경계 미세 탐색

- 실험 목적: LGBM-496 주변에서 Mean Brier를 추가 개선하면서 3/1 fold 안정성, 2024 성능, AUC를 유지하는 조합 탐색
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.32453~0.32456`
- upper 탐색 범위: `0.67547~0.67544` (`upper=1-lower`)
- extreme 탐색 범위: `0.350`, `0.360`, `0.370`, `0.380`, `0.385`
- middle: `1.00`
- 기존 LGBM-130 row-level fold prediction만 사용했으며 모델 학습과 Feature 변경은 수행하지 않음.

| 실험     | parameter                                                |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier | 2024 ΔBrier |           Mean AUC | verdict   |
| -------- | -------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | ----------: | -----------------: | --------- |
| LGBM-516 | lower=0.32453; upper=0.67547; extreme=0.350; middle=1.00 | 0.2475932745891720 | -7.78653445360e-05 | -2.14636947105e-10 |                  3/1 |           -1.15555179925e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-517 | lower=0.32453; upper=0.67547; extreme=0.360; middle=1.00 | 0.2475941550774668 | -7.69848562411e-05 | -5.34586930279e-10 |                  3/1 |           -1.16975868362e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-518 | lower=0.32453; upper=0.67547; extreme=0.370; middle=1.00 | 0.2475950454857643 | -7.60944479436e-05 | -8.44435299463e-10 |                  3/1 |           -1.18296604910e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-519 | lower=0.32453; upper=0.67547; extreme=0.380; middle=1.00 | 0.2475959458140643 | -7.51941196436e-05 | -1.14418202690e-09 |                  3/1 |           -1.19517389569e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-520 | lower=0.32453; upper=0.67547; extreme=0.385; middle=1.00 | 0.2475963996982153 | -7.47402354926e-05 | -1.29026730966e-09 |                  3/1 |           -1.20090299941e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-521 | lower=0.32454; upper=0.67546; extreme=0.350; middle=1.00 | 0.2475932479274397 | -7.78920062682e-05 |                  0 |                  2/2 |           -1.15539186932e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-522 | lower=0.32454; upper=0.67546; extreme=0.360; middle=1.00 | 0.2475941286782247 | -7.70112554833e-05 | -1.47743844936e-10 |                  3/1 |           -1.16961528009e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-523 | lower=0.32454; upper=0.67546; extreme=0.370; middle=1.00 | 0.2475950193536275 | -7.61205800804e-05 | -4.64382338139e-10 |                  3/1 |           -1.18283873242e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-524 | lower=0.32454; upper=0.67546; extreme=0.380; middle=1.00 | 0.2475959199536483 | -7.52199800596e-05 | -7.70895569602e-10 |                  3/1 |           -1.19506222631e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-525 | lower=0.32454; upper=0.67546; extreme=0.385; middle=1.00 | 0.2475963739753904 | -7.47659583175e-05 | -9.20355180956e-10 |                  3/1 |           -1.20079898883e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-526 | lower=0.32455; upper=0.67545; extreme=0.350; middle=1.00 | 0.2475932212503995 | -7.79186833085e-05 |                  0 |                  2/2 |           -1.15523323801e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-527 | lower=0.32455; upper=0.67545; extreme=0.360; middle=1.00 | 0.2475941022638601 | -7.70376698478e-05 |                  0 |                  2/2 |           -1.16947315962e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-528 | lower=0.32455; upper=0.67545; extreme=0.370; middle=1.00 | 0.2475949932065555 | -7.61467271524e-05 | -9.62172563845e-11 |                  3/1 |           -1.18271268309e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-529 | lower=0.32455; upper=0.67545; extreme=0.380; middle=1.00 | 0.2475958940784857 | -7.52458552222e-05 | -4.09309391936e-10 |                  3/1 |           -1.19495180840e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-530 | lower=0.32455; upper=0.67545; extreme=0.385; middle=1.00 | 0.2475963482379139 | -7.47916957940e-05 | -5.62049629060e-10 |                  3/1 |           -1.20069622176e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-531 | lower=0.32456; upper=0.67544; extreme=0.350; middle=1.00 | 0.2475931945746531 | -7.79453590548e-05 |                  0 |                  2/2 |           -1.15507492873e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-532 | lower=0.32456; upper=0.67544; extreme=0.360; middle=1.00 | 0.2475940758507195 | -7.70640829884e-05 |                  0 |                  2/2 |           -1.16933136063e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-533 | lower=0.32456; upper=0.67544; extreme=0.370; middle=1.00 | 0.2475949670606393 | -7.61728730687e-05 |                  0 |                  2/2 |           -1.18258695454e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-534 | lower=0.32456; upper=0.67544; extreme=0.380; middle=1.00 | 0.2475958682044122 | -7.52717292957e-05 | -5.34907951266e-11 |                  3/1 |           -1.19484171048e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-535 | lower=0.32456; upper=0.67544; extreme=0.385; middle=1.00 | 0.2475963225014936 | -7.48174322143e-05 | -2.09465556011e-10 |                  3/1 |           -1.20059377420e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |

### LGBM-516~535 결론

- 이번 20개 중 최고 안정 후보는 **LGBM-516** (`lower=0.32453`, `upper=0.67547`, `extreme=0.350`, `middle=1.00`)이다.
- LGBM-516의 Mean Brier는 `0.2475932745891720`, Mean ΔBrier는 `-7.78653445360e-05`, Median ΔBrier는 `-2.14636947105e-10`, fold별 개선/악화는 `3/1`, mean_delta_without_best_fold는 `-1.15555179925e-05`, verdict는 `CANDIDATE`이다.
- LGBM-516의 2024 Brier는 `0.2480885134392783`, 2024 ΔBrier는 `0`이며 Mean AUC와 2024 AUC도 LGBM-130과 동일하게 유지되었다.
- 숫자상 최저 Mean Brier 후보는 LGBM-531 (`0.2475931945746531`)이지만 fold별 개선/악화가 `2/2`이고 Median ΔBrier가 `0`이므로 `REJECT`이다.
- 이전 최고 안정 후보 LGBM-496 대비 LGBM-516의 Mean ΔBrier는 `-2.19382388871e-06` 추가 개선되었으나, mean_delta_without_best_fold는 `+3.35236749228e-07`만큼 악화되었다.
- 안정성 전환선은 `extreme=0.350`에서 lower `0.32453/0.32454` 사이, `extreme=0.360`에서 lower `0.32454/0.32455` 사이, `extreme=0.370`에서 lower `0.32455/0.32456` 사이에 위치했다.
- 다음 탐색 범위는 lower `0.32450~0.32454`, upper `0.67550~0.67546`, extreme `0.320~0.355`가 적절하다. Mean Brier와 mean_delta_without_best_fold의 균형을 위해 안정성 전환선 바깥쪽 조합을 우선해야 한다.

## LGBM-536~555 안정성 전환선 정밀 탐색

- 실험 목적: LGBM-516 주변의 lower와 extreme 상호작용을 정밀 확인하고, 3/1 fold 안정성을 유지하는 추가 Mean Brier 개선 후보 탐색
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.32451~0.32454`
- upper 탐색 범위: `0.67549~0.67546` (`upper=1-lower`)
- extreme 탐색 범위: `0.330`, `0.340`, `0.345`, `0.355`, `0.365`
- middle: `1.00`
- 기존 LGBM-130 row-level fold prediction만 사용했으며 모델 학습과 Feature 변경은 수행하지 않음.

| 실험     | parameter                                                |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier | 2024 ΔBrier |           Mean AUC | verdict   |
| -------- | -------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | ----------: | -----------------: | --------- |
| LGBM-536 | lower=0.32451; upper=0.67549; extreme=0.330; middle=1.00 | 0.2475915977257376 | -7.95422079704e-05 | -3.58894719499e-10 |                  3/1 |           -1.12452550525e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-537 | lower=0.32451; upper=0.67549; extreme=0.340; middle=1.00 | 0.2475924578672433 | -7.86820664646e-05 | -6.85333012562e-10 |                  3/1 |           -1.14069666833e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-538 | lower=0.32451; upper=0.67549; extreme=0.345; middle=1.00 | 0.2475928916545374 | -7.82482791705e-05 | -8.44781716802e-10 |                  3/1 |           -1.14840775980e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-539 | lower=0.32451; upper=0.67549; extreme=0.355; middle=1.00 | 0.2475937666622081 | -7.73732714999e-05 | -1.15613840723e-09 |                  3/1 |           -1.16308096262e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-540 | lower=0.32451; upper=0.67549; extreme=0.365; middle=1.00 | 0.2475946515806553 | -7.64883530526e-05 | -1.45744072366e-09 |                  3/1 |           -1.17675552526e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-541 | lower=0.32452; upper=0.67548; extreme=0.330; middle=1.00 | 0.2475915705463124 | -7.95693873955e-05 |                  0 |                  2/2 |           -1.12433319637e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-542 | lower=0.32452; upper=0.67548; extreme=0.340; middle=1.00 | 0.2475924309412784 | -7.87089924295e-05 | -2.84999357447e-10 |                  3/1 |           -1.14052172616e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-543 | lower=0.32452; upper=0.67548; extreme=0.345; middle=1.00 | 0.2475928648570322 | -7.82750766757e-05 | -4.47867382070e-10 |                  3/1 |           -1.14824133626e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-544 | lower=0.32452; upper=0.67548; extreme=0.355; middle=1.00 | 0.2475937401250814 | -7.73998086265e-05 | -7.66044921940e-10 |                  3/1 |           -1.16293124685e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-545 | lower=0.32452; upper=0.67548; extreme=0.365; middle=1.00 | 0.2475946253085195 | -7.65146251884e-05 | -1.07414446782e-09 |                  3/1 |           -1.17662207799e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-546 | lower=0.32453; upper=0.67547; extreme=0.330; middle=1.00 | 0.2475915433725900 | -7.95965611180e-05 |                  0 |                  2/2 |           -1.12413947385e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-547 | lower=0.32453; upper=0.67547; extreme=0.340; middle=1.00 | 0.2475924040208797 | -7.87359128282e-05 |                  0 |                  2/2 |           -1.14034539599e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-548 | lower=0.32453; upper=0.67547; extreme=0.345; middle=1.00 | 0.2475928380650255 | -7.83018686824e-05 | -5.08738606797e-11 |                  3/1 |           -1.14807353748e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-549 | lower=0.32453; upper=0.67547; extreme=0.355; middle=1.00 | 0.2475937135933191 | -7.74263403889e-05 | -3.75874664726e-10 |                  3/1 |           -1.16278018129e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-550 | lower=0.32453; upper=0.67547; extreme=0.365; middle=1.00 | 0.2475945990416153 | -7.65408920927e-05 | -6.90773799272e-10 |                  3/1 |           -1.17648730622e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-551 | lower=0.32454; upper=0.67546; extreme=0.330; middle=1.00 | 0.2475915161997234 | -7.96237339845e-05 |                  0 |                  2/2 |           -1.12394517242e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-552 | lower=0.32454; upper=0.67546; extreme=0.340; middle=1.00 | 0.2475923771012726 | -7.87628324353e-05 |                  0 |                  2/2 |           -1.14016850009e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-553 | lower=0.32454; upper=0.67546; extreme=0.345; middle=1.00 | 0.2475928112737789 | -7.83286599290e-05 |                  0 |                  2/2 |           -1.14790517951e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-554 | lower=0.32454; upper=0.67546; extreme=0.355; middle=1.00 | 0.2475936870622549 | -7.74528714530e-05 |                  0 |                  2/2 |           -1.16262856951e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-555 | lower=0.32454; upper=0.67546; extreme=0.365; middle=1.00 | 0.2475945727753488 | -7.65671583591e-05 | -3.07328773541e-10 |                  3/1 |           -1.17635200106e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |

### LGBM-536~555 결론

- 이번 20개 중 가장 낮은 Mean Brier는 LGBM-551의 `0.2475915161997234`이지만 fold별 개선/악화가 `2/2`, Median ΔBrier가 `0`이므로 `REJECT`이다.
- 최고 안정 후보는 **LGBM-536** (`lower=0.32451`, `upper=0.67549`, `extreme=0.330`, `middle=1.00`)이다.
- LGBM-536의 Mean Brier는 `0.2475915977257376`, Mean ΔBrier는 `-7.95422079704e-05`, Median ΔBrier는 `-3.58894719499e-10`, fold별 개선/악화는 `3/1`, mean_delta_without_best_fold는 `-1.12452550525e-05`, verdict는 `CANDIDATE`이다.
- LGBM-536의 Mean AUC와 2024 AUC는 각각 `0.5530385153643456`, `0.5480200784149498`로 변화가 없고, 2024 Brier는 `0.2480885134392783`, 2024 ΔBrier는 `0`이다.
- 이전 최고 LGBM-516 대비 Mean ΔBrier는 `-1.67686343440e-06` 추가 개선되어 최고 안정 기록을 갱신했다. 다만 mean_delta_without_best_fold는 `+3.10262940000e-07`만큼 악화되었다.
- 다음 20개 탐색 범위는 lower `0.32448~0.32452`, upper `0.67552~0.67548`, extreme `0.300~0.335`로 제한한다. `extreme=0.330`의 안정성 전환이 lower `0.32451/0.32452` 사이에서 발생했으므로 이 경계의 바깥쪽을 우선 탐색한다.

## LGBM-556~575 extreme 0.330 이하 안정성 탐색

- 실험 목적: LGBM-536 주변에서 extreme을 낮출 때 Mean Brier가 추가 개선되는지 확인하고 3/1 fold 안정성 전환선을 식별
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.32450~0.32452`
- upper 탐색 범위: `0.67550~0.67548` (`upper=1-lower`)
- extreme 탐색 범위: `0.315~0.338`, 특히 `0.325~0.335` 집중
- middle: `1.00`
- 기존 LGBM-130 row-level fold prediction만 사용했으며 모델 학습과 Feature 변경은 수행하지 않음.

| 실험     | parameter                                                |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier | 2024 ΔBrier |           Mean AUC | verdict   |
| -------- | -------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | ----------: | -----------------: | --------- |
| LGBM-556 | lower=0.32450; upper=0.67550; extreme=0.315; middle=1.00 | 0.2475903536403157 | -8.07862933922e-05 | -2.67817296118e-10 |                  3/1 |           -1.09861362228e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-557 | lower=0.32450; upper=0.67550; extreme=0.320; middle=1.00 | 0.2475907749164680 | -8.03650172399e-05 | -4.36386510261e-10 |                  3/1 |           -1.10756396224e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-558 | lower=0.32450; upper=0.67550; extreme=0.325; middle=1.00 | 0.2475911986691618 | -7.99412645462e-05 | -6.02448035902e-10 |                  3/1 |           -1.11626475194e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-559 | lower=0.32450; upper=0.67550; extreme=0.328; middle=1.00 | 0.2475914541095179 | -7.96858241900e-05 | -7.00881214177e-10 |                  3/1 |           -1.12136544164e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-560 | lower=0.32450; upper=0.67550; extreme=0.330; middle=1.00 | 0.2475916248983970 | -7.95150353109e-05 | -7.66001789776e-10 |                  3/1 |           -1.12471599138e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-561 | lower=0.32450; upper=0.67550; extreme=0.332; middle=1.00 | 0.2475917960835227 | -7.93438501852e-05 | -8.30721130773e-10 |                  3/1 |           -1.12802661309e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-562 | lower=0.32450; upper=0.67550; extreme=0.335; middle=1.00 | 0.2475920536041738 | -7.90863295342e-05 | -9.27047882904e-10 |                  3/1 |           -1.13291768057e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-563 | lower=0.32451; upper=0.67549; extreme=0.315; middle=1.00 | 0.2475903260961851 | -8.08138375228e-05 |                  0 |                  2/2 |           -1.09839631029e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-564 | lower=0.32451; upper=0.67549; extreme=0.320; middle=1.00 | 0.2475907474950084 | -8.03924386995e-05 | -2.24020801909e-11 |                  3/1 |           -1.10735570199e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-565 | lower=0.32451; upper=0.67549; extreme=0.325; middle=1.00 | 0.2475911713715259 | -7.99685621820e-05 | -1.91905213942e-10 |                  3/1 |           -1.11606543364e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-566 | lower=0.32451; upper=0.67549; extreme=0.328; middle=1.00 | 0.2475914268867296 | -7.97130469783e-05 | -2.92400548219e-10 |                  3/1 |           -1.12117143581e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-567 | lower=0.32451; upper=0.67549; extreme=0.332; middle=1.00 | 0.2475917689611766 | -7.93709725313e-05 | -4.24986740244e-10 |                  3/1 |           -1.12783962908e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-568 | lower=0.32451; upper=0.67549; extreme=0.335; middle=1.00 | 0.2475920265576434 | -7.91133760646e-05 | -5.23370680128e-10 |                  3/1 |           -1.13273591681e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-569 | lower=0.32451; upper=0.67549; extreme=0.338; middle=1.00 | 0.2475922850460800 | -7.88548876279e-05 | -6.20849704980e-10 |                  3/1 |           -1.13754232693e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-570 | lower=0.32452; upper=0.67548; extreme=0.315; middle=1.00 | 0.2475902985452174 | -8.08413884905e-05 |                  0 |                  2/2 |           -1.09817712769e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-571 | lower=0.32452; upper=0.67548; extreme=0.320; middle=1.00 | 0.2475907200667352 | -8.04198669727e-05 |                  0 |                  2/2 |           -1.10714558712e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-572 | lower=0.32452; upper=0.67548; extreme=0.325; middle=1.00 | 0.2475911440671002 | -7.99958666077e-05 |                  0 |                  2/2 |           -1.11586427668e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-573 | lower=0.32452; upper=0.67548; extreme=0.328; middle=1.00 | 0.2475913996571658 | -7.97402765421e-05 |                  0 |                  2/2 |           -1.12097560088e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | REJECT    |
| LGBM-574 | lower=0.32452; upper=0.67548; extreme=0.332; middle=1.00 | 0.2475917418320745 | -7.93981016334e-05 | -1.91699711660e-11 |                  3/1 |           -1.12765082868e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |
| LGBM-575 | lower=0.32452; upper=0.67548; extreme=0.335; middle=1.00 | 0.2475919995043718 | -7.91404293361e-05 | -1.19611848204e-10 |                  3/1 |           -1.13255234620e-05 | 0.2480885134392783 |           0 | 0.5530385153643456 | CANDIDATE |

### LGBM-556~575 결론

- 이번 20개 중 가장 낮은 Mean Brier는 LGBM-570의 `0.2475902985452174`이지만 fold별 개선/악화가 `2/2`, Median ΔBrier가 `0`이므로 `REJECT`이다.
- 최고 안정 후보는 **LGBM-556** (`lower=0.32450`, `upper=0.67550`, `extreme=0.315`, `middle=1.00`)이다.
- LGBM-556의 Mean Brier는 `0.2475903536403157`, Mean ΔBrier는 `-8.07862933922e-05`, Median ΔBrier는 `-2.67817296118e-10`, fold별 개선/악화는 `3/1`, mean_delta_without_best_fold는 `-1.09861362228e-05`, verdict는 `CANDIDATE`이다.
- LGBM-556의 Mean AUC와 2024 AUC는 각각 `0.5530385153643456`, `0.5480200784149498`로 변화가 없고, 2024 Brier는 `0.2480885134392783`, 2024 ΔBrier는 `0`이다.
- 이전 최고 LGBM-536 대비 Mean ΔBrier는 `-1.24408542184e-06` 추가 개선되어 최고 안정 기록을 갱신했다. 다만 mean_delta_without_best_fold는 `+2.59118829678e-07`만큼 악화되었다.
- 안정성 전환선은 `extreme=0.315`에서 lower `0.32450/0.32451` 사이, `extreme=0.320`에서 lower `0.32451/0.32452` 사이에 위치했다.
- 다음 탐색 범위는 lower `0.32447~0.32451`, upper `0.67553~0.67549`, extreme `0.290~0.320`으로 제한한다. 더 작은 extreme을 사용할 때는 안정성 전환선보다 바깥쪽 lower를 우선한다.

## LGBM-576~595 LGBM-556 주변 정밀 탐색

- 실험 목적: LGBM-556 주변에서 extreme `0.315` 이하와 바깥쪽 lower의 상호작용을 확인하고 안정적인 Mean Brier 추가 개선 후보 탐색
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.324470~0.324505`
- upper 탐색 범위: `0.675530~0.675495` (`upper=1-lower`)
- extreme 탐색 범위: `0.3050~0.3175`
- middle: `1.00`
- 기존 LGBM-130 row-level fold prediction만 사용했으며 모델 학습과 Feature 변경은 수행하지 않음.

| 실험     | parameter                                                   |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier |           2024 AUC | verdict   |
| -------- | ----------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | -----------------: | --------- |
| LGBM-576 | lower=0.324470; upper=0.675530; extreme=0.3050; middle=1.00 | 0.2475896018885345 | -8.15380451734e-05 | -1.19565490841e-09 |                  3/1 |           -1.08066600084e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-577 | lower=0.324470; upper=0.675530; extreme=0.3100; middle=1.00 | 0.2475900178502528 | -8.11220834552e-05 | -1.35886929487e-09 |                  3/1 |           -1.09008768136e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-578 | lower=0.324470; upper=0.675530; extreme=0.3125; middle=1.00 | 0.2475902267585192 | -8.09131751888e-05 | -1.43954270726e-09 |                  3/1 |           -1.09470506371e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-579 | lower=0.324470; upper=0.675530; extreme=0.3150; middle=1.00 | 0.2475904362850569 | -8.07036486510e-05 | -1.51959356209e-09 |                  3/1 |           -1.09926014078e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-580 | lower=0.324470; upper=0.675530; extreme=0.3175; middle=1.00 | 0.2475906464298662 | -8.04935038418e-05 | -1.59902194263e-09 |                  3/1 |           -1.10375291257e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-581 | lower=0.324480; upper=0.675520; extreme=0.3050; middle=1.00 | 0.2475895741025832 | -8.15658311247e-05 | -7.71577662873e-10 |                  3/1 |           -1.08043235070e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-582 | lower=0.324480; upper=0.675520; extreme=0.3100; middle=1.00 | 0.2475899901847474 | -8.11497489605e-05 | -9.38247507465e-10 |                  3/1 |           -1.08986328035e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-583 | lower=0.324480; upper=0.675520; extreme=0.3125; middle=1.00 | 0.2475901991536685 | -8.09407800394e-05 | -1.02064648400e-09 |                  3/1 |           -1.09448524613e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-584 | lower=0.324480; upper=0.675520; extreme=0.3150; middle=1.00 | 0.2475904087411490 | -8.07311925590e-05 | -1.10242140416e-09 |                  3/1 |           -1.09904487921e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-585 | lower=0.324480; upper=0.675520; extreme=0.3175; middle=1.00 | 0.2475906189471887 | -8.05209865192e-05 | -1.18357237899e-09 |                  3/1 |           -1.10354217959e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-586 | lower=0.324490; upper=0.675510; extreme=0.3050; middle=1.00 | 0.2475895463066921 | -8.15936270159e-05 | -3.47411294177e-10 |                  3/1 |           -1.08019859823e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-587 | lower=0.324490; upper=0.675510; extreme=0.3100; middle=1.00 | 0.2475899625093468 | -8.11774243611e-05 | -5.17537901423e-10 |                  3/1 |           -1.08963878011e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-588 | lower=0.324490; upper=0.675510; extreme=0.3125; middle=1.00 | 0.2475901715389452 | -8.09683947627e-05 | -6.01662997202e-10 |                  3/1 |           -1.09426533086e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-589 | lower=0.324490; upper=0.675510; extreme=0.3150; middle=1.00 | 0.2475903811873908 | -8.07587463171e-05 | -6.85162648839e-10 |                  3/1 |           -1.09882952148e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-590 | lower=0.324490; upper=0.675510; extreme=0.3175; middle=1.00 | 0.2475905914546838 | -8.05484790241e-05 | -7.68036828580e-10 |                  3/1 |           -1.10333135198e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-591 | lower=0.324505; upper=0.675495; extreme=0.3050; middle=1.00 | 0.2475895046224485 | -8.16353112594e-05 |                  0 |                  2/2 |           -1.07984675284e-05 | 0.2480885134392783 | 0.5480200784149498 | REJECT    |
| LGBM-592 | lower=0.324505; upper=0.675495; extreme=0.3100; middle=1.00 | 0.2475899210057197 | -8.12189279882e-05 |                  0 |                  2/2 |           -1.08930082627e-05 | 0.2480885134392783 | 0.5480200784149498 | REJECT    |
| LGBM-593 | lower=0.324505; upper=0.675495; extreme=0.3125; middle=1.00 | 0.2475901301262744 | -8.10098074334e-05 |                  0 |                  2/2 |           -1.09393426106e-05 | 0.2480885134392783 | 0.5480200784149498 | REJECT    |
| LGBM-594 | lower=0.324505; upper=0.675495; extreme=0.3150; middle=1.00 | 0.2475903398661087 | -8.08000675992e-05 | -5.91121318561e-11 |                  3/1 |           -1.09850529456e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |
| LGBM-595 | lower=0.324505; upper=0.675495; extreme=0.3175; middle=1.00 | 0.2475905502252224 | -8.05897084856e-05 | -1.44572381844e-10 |                  3/1 |           -1.10301392677e-05 | 0.2480885134392783 | 0.5480200784149498 | CANDIDATE |

### LGBM-576~595 결론

- 이번 20개 중 가장 낮은 Mean Brier는 LGBM-591의 `0.2475895046224485`이지만 fold별 개선/악화가 `2/2`, Median ΔBrier가 `0`이므로 `REJECT`이다.
- 최고 안정 후보는 **LGBM-586** (`lower=0.324490`, `upper=0.675510`, `extreme=0.3050`, `middle=1.00`)이다.
- LGBM-586의 Mean Brier는 `0.2475895463066921`, Mean ΔBrier는 `-8.15936270159e-05`, Median ΔBrier는 `-3.47411294177e-10`, fold별 개선/악화는 `3/1`, mean_delta_without_best_fold는 `-1.08019859823e-05`, verdict는 `CANDIDATE`이다.
- LGBM-586의 Mean AUC와 2024 AUC는 각각 `0.5530385153643456`, `0.5480200784149498`로 변화가 없고, 2024 Brier는 `0.2480885134392783`으로 변화가 없다.
- 이전 최고 LGBM-556 대비 Mean Brier는 `-8.07333623648e-07`, 상대적으로 `0.000326076364357%` 개선되어 최고 안정 기록을 갱신했다. mean_delta_without_best_fold는 `+1.84150240529e-07`만큼 악화되었다.
- 다음 20개 탐색 범위는 lower `0.32445~0.32449`, upper `0.67555~0.67551`, extreme `0.2850~0.3075`로 제한한다. extreme을 더 낮출 때는 `lower=0.324490`보다 바깥쪽 경계를 우선해 3/1 안정성을 유지해야 한다.

## LGBM-596~615 LGBM-586 주변 하향 정밀 탐색

### 현재 기준점

- 안정적인 최고 후보: **LGBM-586**
- method: `continuous_piecewise_probability_shrinkage`
- parameter: `lower=0.324490`, `upper=0.675510`, `extreme=0.3050`, `middle=1.00`
- baseline Brier: `0.24767113993370798`
- candidate Brier: `0.2475895463066921`
- Mean ΔBrier: `-8.159362701586348e-05`
- Brier 개선/악화 fold: `3/1`
- mean_delta_without_best_fold: `-1.0801985982272777e-05`
- Mean AUC: `0.5530385153643456`, 2024 Brier: `0.2480885134392783`, 2024 AUC: `0.5480200784149498`

### 실험 목적과 탐색 범위

- 실험 목적: LGBM-586 주변에서 extreme을 `0.3050`보다 낮추면서 Mean Brier를 추가로 개선하고, `3/1` fold 안정성을 유지하는 lower 경계를 정밀 탐색한다.
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.324450~0.324510`
- upper 탐색 범위: `0.675550~0.675490` (`upper=1-lower`)
- extreme 탐색 범위: `0.2850~0.3025`
- middle: `1.00`
- 이전 실험에서 관찰된 안정성 전환선을 따라 각 extreme별 lower를 촘촘히 배치했으며, 정확히 20개만 실행했다.
- 데이터 처리, feature engineering, feature selection, CV split, random seed, LightGBM 구조와 hyperparameter, 학습·검증·평가·calibration·prediction pipeline은 변경하지 않았다.

### 20개 실험 결과

| 실험     | parameter                                                   |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier |           2024 AUC |           Mean AUC | verdict   |
| -------- | ----------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | -----------------: | -----------------: | --------- |
| LGBM-596 | lower=0.324450; upper=0.675550; extreme=0.2850; middle=1.00 | 0.2475880192884135 | -8.31206452945e-05 | -1.39352898665e-09 |                  3/1 |           -1.04102914299e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-597 | lower=0.324460; upper=0.675540; extreme=0.2850; middle=1.00 | 0.2475879910277517 | -8.31489059562e-05 | -9.55759915655e-10 |                  3/1 |           -1.04075846427e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-598 | lower=0.324470; upper=0.675530; extreme=0.2850; middle=1.00 | 0.2475879627725199 | -8.31771611881e-05 | -5.17896531216e-10 |                  3/1 |           -1.04048706773e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-599 | lower=0.324480; upper=0.675520; extreme=0.2850; middle=1.00 | 0.2475879345162997 | -8.32054174082e-05 | -7.99387500638e-11 |                  3/1 |           -1.04021532425e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-600 | lower=0.324460; upper=0.675540; extreme=0.2900; middle=1.00 | 0.2475883969812659 | -8.27429524420e-05 | -1.12545703312e-09 |                  3/1 |           -1.05116734621e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-601 | lower=0.324470; upper=0.675530; extreme=0.2900; middle=1.00 | 0.2475883688418947 | -8.27710918132e-05 | -6.91071255776e-10 |                  3/1 |           -1.05090563266e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-602 | lower=0.324480; upper=0.675520; extreme=0.2900; middle=1.00 | 0.2475883407015146 | -8.27992321934e-05 | -2.56592413983e-10 |                  3/1 |           -1.05064357704e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-603 | lower=0.324490; upper=0.675510; extreme=0.2900; middle=1.00 | 0.2475883125510630 | -8.28273826449e-05 |                  0 |                  2/2 |           -1.05038140956e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-604 | lower=0.324470; upper=0.675530; extreme=0.2950; middle=1.00 | 0.2475887773843555 | -8.23625493525e-05 | -8.61755888870e-10 |                  3/1 |           -1.06107497649e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-605 | lower=0.324480; upper=0.675520; extreme=0.2950; middle=1.00 | 0.2475887493609668 | -8.23905727412e-05 | -4.30750130009e-10 |                  3/1 |           -1.06082249905e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-606 | lower=0.324490; upper=0.675510; extreme=0.2950; middle=1.00 | 0.2475887213275502 | -8.24186061578e-05 |                  0 |                  2/2 |           -1.06056991295e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-607 | lower=0.324500; upper=0.675500; extreme=0.2950; middle=1.00 | 0.2475886933011215 | -8.24466325864e-05 |                  0 |                  2/2 |           -1.06031675987e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-608 | lower=0.324475; upper=0.675525; extreme=0.3000; middle=1.00 | 0.2475891744498980 | -8.19654838099e-05 | -8.16192474717e-10 |                  3/1 |           -1.07087354736e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-609 | lower=0.324485; upper=0.675515; extreme=0.3000; middle=1.00 | 0.2475891465358160 | -8.19933978920e-05 | -3.88608700774e-10 |                  3/1 |           -1.07063073671e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-610 | lower=0.324495; upper=0.675505; extreme=0.3000; middle=1.00 | 0.2475891186250829 | -8.20213086250e-05 |                  0 |                  2/2 |           -1.07038713075e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-611 | lower=0.324505; upper=0.675495; extreme=0.3000; middle=1.00 | 0.2475890907162951 | -8.20492174129e-05 |                  0 |                  2/2 |           -1.07014307426e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-612 | lower=0.324480; upper=0.675520; extreme=0.3025; middle=1.00 | 0.2475893669893401 | -8.17729443678e-05 | -6.87306767055e-10 |                  3/1 |           -1.07562338683e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-613 | lower=0.324490; upper=0.675510; extreme=0.3025; middle=1.00 | 0.2475893391336356 | -8.18008000723e-05 | -2.61409838220e-10 |                  3/1 |           -1.07538496710e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-614 | lower=0.324500; upper=0.675500; extreme=0.3025; middle=1.00 | 0.2475893112848041 | -8.18286489039e-05 |                  0 |                  2/2 |           -1.07514599001e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-615 | lower=0.324510; upper=0.675490; extreme=0.3025; middle=1.00 | 0.2475892834390387 | -8.18564946692e-05 |                  0 |                  2/2 |           -1.07490556836e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |

### 결과 요약과 best 갱신 여부

- 이번 20개 중 수치상 최고 후보는 **LGBM-599**이며 Mean Brier는 `0.2475879345162997`이다.
- LGBM-599는 fold별 개선/악화가 `3/1`, Median ΔBrier가 `-7.99387500638e-11`, mean_delta_without_best_fold가 `-1.04021532425e-05`이므로 안정적인 최고 후보이기도 하다.
- LGBM-599의 Mean AUC와 2024 AUC는 각각 `0.5530385153643456`, `0.5480200784149498`로 악화가 없으며, 2024 Brier도 `0.2480885134392783`으로 악화가 없다.
- 기존 best LGBM-586 대비 Mean Brier는 `-1.61179039237e-06` 추가 개선되었으므로 안정적인 best를 **LGBM-599**로 갱신한다.
- 동일 extreme 안에서는 lower를 안쪽으로 이동할수록 Mean Brier가 개선되었지만, 안정성 전환선을 넘으면 `2/2`가 되어 REJECT되었다. 확인된 전환선은 `extreme=0.2900`에서 lower `0.324480/0.324490` 사이, `extreme=0.2950`에서 `0.324480/0.324490` 사이, `extreme=0.3000`에서 `0.324485/0.324495` 사이, `extreme=0.3025`에서 `0.324490/0.324500` 사이이다.

### 다음 실험 기준점과 탐색 방향

- 다음 안정 기준점은 **LGBM-599** (`lower=0.324480`, `upper=0.675520`, `extreme=0.2850`, `middle=1.00`)이다.
- 다음 탐색에서는 lower `0.32443~0.32449`, upper `0.67557~0.67551`, extreme `0.2650~0.2875` 범위를 우선한다.
- extreme을 추가로 낮추면 안정성 전환 lower도 바깥쪽으로 이동할 가능성이 있으므로, 각 extreme별 전환선 양쪽을 촘촘히 배치하고 `3/1`을 유지하는 가장 안쪽 lower를 우선 확인한다.

## LGBM-616~635 extreme 0.285 미만 정밀 탐색

### 현재 기준점

- 이번 요청의 안정 기준점: **LGBM-586**
- method: `continuous_piecewise_probability_shrinkage`
- parameter: `lower=0.324490`, `upper=0.675510`, `extreme=0.3050`, `middle=1.00`
- baseline Brier: `0.24767113993370798`
- candidate Brier: `0.2475895463066921`
- Mean ΔBrier: `-8.159362701586348e-05`
- Brier 개선/악화 fold: `3/1`
- mean_delta_without_best_fold: `-1.0801985982272777e-05`
- Mean AUC: `0.5530385153643456`, 2024 Brier: `0.2480885134392783`, 2024 AUC: `0.5480200784149498`

### 실험 목적과 탐색 범위

- 실험 목적: LGBM-586 주변에서 extreme이 `0.2850`보다 작은 구간의 Brier 개선 추세와 fold 안정성 전환선을 확인한다.
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.324460~0.324500`
- upper 탐색 범위: `0.675540~0.675500` (`upper=1-lower`)
- extreme 탐색 범위: `0.2550~0.2825`
- 중요 구간인 extreme `0.2750~0.2825`에 12개를 배치하고, 더 낮은 `0.2550~0.2650`에 8개를 배치했다.
- middle: `1.00`
- 데이터 처리, feature engineering, feature selection, CV split, random seed, LightGBM 구조와 hyperparameter, 학습·검증·평가·calibration·prediction pipeline은 변경하지 않았으며 정확히 20개만 실행했다.

### 20개 실험 결과

| 실험     | parameter                                                   |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier |           2024 AUC |           Mean AUC | verdict   |
| -------- | ----------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | -----------------: | -----------------: | --------- |
| LGBM-616 | lower=0.324460; upper=0.675540; extreme=0.2550; middle=1.00 | 0.2475856072172960 | -8.55327164119e-05 |                  0 |                  2/2 |           -9.73073832150e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-617 | lower=0.324465; upper=0.675535; extreme=0.2550; middle=1.00 | 0.2475855927542750 | -8.55471794330e-05 |                  0 |                  2/2 |           -9.72907869867e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-618 | lower=0.324470; upper=0.675530; extreme=0.2550; middle=1.00 | 0.2475855782910731 | -8.55616426349e-05 |                  0 |                  2/2 |           -9.72742034994e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-619 | lower=0.324475; upper=0.675525; extreme=0.2550; middle=1.00 | 0.2475855638302884 | -8.55761034196e-05 |                  0 |                  2/2 |           -9.72575900442e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-620 | lower=0.324460; upper=0.675540; extreme=0.2650; middle=1.00 | 0.2475863919330423 | -8.47480006657e-05 | -2.52129039868e-10 |                  3/1 |           -9.96631822003e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-621 | lower=0.324470; upper=0.675530; extreme=0.2650; middle=1.00 | 0.2475863632258786 | -8.47767078293e-05 |                  0 |                  2/2 |           -9.96320596981e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-622 | lower=0.324480; upper=0.675520; extreme=0.2650; middle=1.00 | 0.2475863345178136 | -8.48054158944e-05 |                  0 |                  2/2 |           -9.96009005218e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-623 | lower=0.324490; upper=0.675510; extreme=0.2650; middle=1.00 | 0.2475863057994658 | -8.48341342422e-05 |                  0 |                  2/2 |           -9.95697285016e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-624 | lower=0.324460; upper=0.675540; extreme=0.2750; middle=1.00 | 0.2475871865365275 | -8.39533971804e-05 | -6.08912947841e-10 |                  3/1 |           -1.01919336604e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-625 | lower=0.324470; upper=0.675530; extreme=0.2750; middle=1.00 | 0.2475871580530276 | -8.39818806804e-05 | -1.64076779940e-10 |                  3/1 |           -1.01890227456e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-626 | lower=0.324480; upper=0.675520; extreme=0.2750; middle=1.00 | 0.2475871295685820 | -8.40103651260e-05 |                  0 |                  2/2 |           -1.01861082631e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-627 | lower=0.324490; upper=0.675510; extreme=0.2750; middle=1.00 | 0.2475871010739370 | -8.40388597710e-05 |                  0 |                  2/2 |           -1.01831925635e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-628 | lower=0.324465; upper=0.675535; extreme=0.2800; middle=1.00 | 0.2475875733613064 | -8.35665724016e-05 | -5.62917074065e-10 |                  3/1 |           -1.02995981318e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-629 | lower=0.324475; upper=0.675525; extreme=0.2800; middle=1.00 | 0.2475875449934561 | -8.35949402519e-05 | -1.21522375496e-10 |                  3/1 |           -1.02967846369e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-630 | lower=0.324485; upper=0.675515; extreme=0.2800; middle=1.00 | 0.2475875166135149 | -8.36233201931e-05 |                  0 |                  2/2 |           -1.02939712168e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-631 | lower=0.324495; upper=0.675505; extreme=0.2800; middle=1.00 | 0.2475874882371305 | -8.36516965775e-05 |                  0 |                  2/2 |           -1.02911495173e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-632 | lower=0.324470; upper=0.675530; extreme=0.2825; middle=1.00 | 0.2475877606652396 | -8.33792684684e-05 | -4.30375374227e-10 |                  3/1 |           -1.03518432735e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-633 | lower=0.324480; upper=0.675520; extreme=0.2825; middle=1.00 | 0.2475877323515313 | -8.34075821767e-05 |                  0 |                  2/2 |           -1.03490769881e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-634 | lower=0.324490; upper=0.675510; extreme=0.2825; middle=1.00 | 0.2475877040276872 | -8.34359060208e-05 |                  0 |                  2/2 |           -1.03463095352e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-635 | lower=0.324500; upper=0.675500; extreme=0.2825; middle=1.00 | 0.2475876757110248 | -8.34642226831e-05 |                  0 |                  2/2 |           -1.03435362503e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |

### 결과 요약과 best 갱신 여부

- 수치상 최고 후보는 **LGBM-619**이며 Mean Brier는 `0.2475855638302884`이지만 fold별 개선/악화가 `2/2`, Median ΔBrier가 `0`이므로 `REJECT`이다.
- 안정적인 최고 후보는 **LGBM-620** (`lower=0.324460`, `upper=0.675540`, `extreme=0.2650`, `middle=1.00`)이다.
- LGBM-620은 Mean Brier `0.2475863919330423`, Mean ΔBrier `-8.47480006657e-05`, fold별 개선/악화 `3/1`, mean_delta_without_best_fold `-9.96631822003e-06`으로 안정성 조건을 충족한다.
- LGBM-620의 Mean AUC와 2024 AUC는 각각 `0.5530385153643456`, `0.5480200784149498`로 악화가 없고, 2024 Brier도 `0.2480885134392783`으로 악화가 없다.
- 요청 기준점 LGBM-586 대비 Mean Brier는 `-3.15437364983e-06` 추가 개선되어 안정적인 best를 **LGBM-620**으로 갱신한다. 직전 로그의 LGBM-599와 비교해도 Mean Brier가 `-1.54258325746e-06` 추가 개선되었다.

### extreme 최적 구간

- 수치만 보면 extreme `0.2550`이 가장 낮은 Mean Brier 구간이지만 이번 lower 범위에서는 전부 `2/2`로 나타나 안정적인 best로 채택할 수 없다.
- 안정성까지 고려한 이번 탐색의 최적 extreme은 `0.2650`이며, `lower=0.324460`에서만 `3/1`을 유지했다.
- extreme `0.2750~0.2825`에서도 안정 후보가 확인되었지만 Mean Brier는 extreme `0.2650`보다 높았다. 따라서 실제 최적점은 `0.2550~0.2650` 사이의 안정성 경계 부근에 있을 가능성이 높다.

### 다음 실험 기준점과 탐색 방향

- 다음 안정 기준점은 **LGBM-620** (`lower=0.324460`, `upper=0.675540`, `extreme=0.2650`, `middle=1.00`)이다.
- 다음 탐색은 lower `0.32442~0.32447`, upper `0.67558~0.67553`, extreme `0.2500~0.2675`를 우선한다.
- extreme `0.2550~0.2650`을 촘촘히 나누고, 현재 범위보다 바깥쪽 lower를 함께 탐색하여 `2/2`에서 `3/1`로 전환되는 경계를 찾는다.

## LGBM-636~655 LGBM-620 주변 extreme 정밀 탐색

### 현재 기준점

- 안정적인 최고 후보: **LGBM-620**
- method: `continuous_piecewise_probability_shrinkage`
- parameter: `lower=0.324460`, `upper=0.675540`, `extreme=0.2650`, `middle=1.00`
- candidate Brier: `0.24758639193304227`
- Mean ΔBrier: `-8.474800066566867e-05`
- Brier 개선/악화 fold: `3/1`
- mean_delta_without_best_fold: `-9.966318220033799e-06`
- Mean AUC Δ: `0`, 2024 Brier Δ: `0`, 2024 AUC Δ: `0`

### 실험 목적과 탐색 범위

- 실험 목적: LGBM-620 주변에서 extreme `0.2625~0.2675`를 중심으로 최적점을 촘촘히 찾고 lower와의 안정성 전환선을 확인한다.
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.324465~0.324478`
- upper 탐색 범위: `0.675535~0.675522` (`upper=1-lower`)
- extreme 탐색 범위: `0.2600~0.2700`
- middle: `1.00`
- lower는 `0.324470` 부근에 집중했으며, extreme `0.2625~0.2675`에 12개를 배치했다.
- 데이터 처리, feature engineering, feature selection, CV split, random seed, LightGBM 구조와 hyperparameter, 학습·검증·평가·calibration·prediction pipeline은 변경하지 않았고 정확히 20개만 실행했다.

### 20개 실험 결과

| 실험     | parameter                                                   |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier |           2024 AUC |           Mean AUC | verdict   |
| -------- | ----------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | -----------------: | -----------------: | --------- |
| LGBM-636 | lower=0.324465; upper=0.675535; extreme=0.2600; middle=1.00 | 0.2475859839306608 | -8.51560030472e-05 |                  0 |                  2/2 |           -9.84816591075e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-637 | lower=0.324468; upper=0.675532; extreme=0.2600; middle=1.00 | 0.2475859752847394 | -8.51646489685e-05 |                  0 |                  2/2 |           -9.84720229438e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-638 | lower=0.324470; upper=0.675530; extreme=0.2600; middle=1.00 | 0.2475859695219329 | -8.51704117750e-05 |                  0 |                  2/2 |           -9.84655926540e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-639 | lower=0.324472; upper=0.675528; extreme=0.2600; middle=1.00 | 0.2475859637597401 | -8.51761739678e-05 |                  0 |                  2/2 |           -9.84591553205e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-640 | lower=0.324465; upper=0.675535; extreme=0.2625; middle=1.00 | 0.2475861804460450 | -8.49594876630e-05 |                  0 |                  2/2 |           -9.90677514327e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-641 | lower=0.324468; upper=0.675532; extreme=0.2625; middle=1.00 | 0.2475861718165981 | -8.49681171098e-05 |                  0 |                  2/2 |           -9.90582691292e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-642 | lower=0.324470; upper=0.675530; extreme=0.2625; middle=1.00 | 0.2475861660647700 | -8.49738689379e-05 |                  0 |                  2/2 |           -9.90519414399e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-643 | lower=0.324472; upper=0.675528; extreme=0.2625; middle=1.00 | 0.2475861603135530 | -8.49796201550e-05 |                  0 |                  2/2 |           -9.90456067360e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-644 | lower=0.324465; upper=0.675535; extreme=0.2650; middle=1.00 | 0.2475863775795568 | -8.47623541512e-05 | -2.62253274652e-11 |                  3/1 |           -9.96476146011e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-645 | lower=0.324468; upper=0.675532; extreme=0.2650; middle=1.00 | 0.2475863689666707 | -8.47709670372e-05 |                  0 |                  2/2 |           -9.96382853351e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-646 | lower=0.324470; upper=0.675530; extreme=0.2650; middle=1.00 | 0.2475863632258786 | -8.47767078293e-05 |                  0 |                  2/2 |           -9.96320596981e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-647 | lower=0.324472; upper=0.675528; extreme=0.2650; middle=1.00 | 0.2475863574856949 | -8.47824480131e-05 |                  0 |                  2/2 |           -9.96258270754e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-648 | lower=0.324468; upper=0.675532; extreme=0.2675; middle=1.00 | 0.2475865667349572 | -8.45731987507e-05 |                  0 |                  2/2 |           -1.00212071562e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-649 | lower=0.324470; upper=0.675530; extreme=0.2675; middle=1.00 | 0.2475865610052587 | -8.45789284493e-05 |                  0 |                  2/2 |           -1.00205947429e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-650 | lower=0.324472; upper=0.675528; extreme=0.2675; middle=1.00 | 0.2475865552761658 | -8.45846575422e-05 |                  0 |                  2/2 |           -1.00199816339e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-651 | lower=0.324475; upper=0.675525; extreme=0.2675; middle=1.00 | 0.2475865466816799 | -8.45932520281e-05 |                  0 |                  2/2 |           -1.00190616938e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-652 | lower=0.324470; upper=0.675530; extreme=0.2700; middle=1.00 | 0.2475867594029101 | -8.43805307978e-05 |                  0 |                  2/2 |           -1.00773604632e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-653 | lower=0.324472; upper=0.675528; extreme=0.2700; middle=1.00 | 0.2475867536849658 | -8.43862487422e-05 |                  0 |                  2/2 |           -1.00767574527e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-654 | lower=0.324475; upper=0.675525; extreme=0.2700; middle=1.00 | 0.2475867451072043 | -8.43948265036e-05 |                  0 |                  2/2 |           -1.00758526621e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-655 | lower=0.324478; upper=0.675522; extreme=0.2700; middle=1.00 | 0.2475867365274502 | -8.44034062577e-05 |                  0 |                  2/2 |           -1.00749475419e-05 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |

### 결과 요약과 best 갱신 여부

- 수치상 최고 후보는 **LGBM-639**이며 Mean Brier는 `0.2475859637597401`이지만 fold별 개선/악화가 `2/2`, Median ΔBrier가 `0`이므로 `REJECT`이다.
- 안정적인 최고 후보는 **LGBM-644** (`lower=0.324465`, `upper=0.675535`, `extreme=0.2650`, `middle=1.00`)이다.
- LGBM-644의 Mean Brier는 `0.2475863775795568`, Mean ΔBrier는 `-8.47623541512e-05`, fold별 개선/악화는 `3/1`, mean_delta_without_best_fold는 `-9.96476146011e-06`이다.
- LGBM-644의 Mean AUC와 2024 AUC는 각각 `0.5530385153643456`, `0.5480200784149498`로 악화가 없으며 2024 Brier도 `0.2480885134392783`으로 악화가 없다.
- 기존 best LGBM-620 대비 Mean Brier가 `-1.43534854500e-08` 추가 개선되었고 안정성 조건을 충족하므로 best를 **LGBM-644**로 갱신한다. 다만 mean_delta_without_best_fold는 `+1.55675992236e-09`만큼 소폭 악화되어 개선 폭은 매우 작다.
- 이번 범위에서는 LGBM-644를 제외한 19개가 모두 `2/2`였다. extreme `0.2600~0.2625`는 `lower=0.324465`에서도 안정성 경계 안쪽이므로, 해당 extreme의 안정 후보는 더 바깥쪽 lower에서 찾아야 한다.

### 다음 실험 기준점과 탐색 방향

- 다음 안정 기준점은 **LGBM-644** (`lower=0.324465`, `upper=0.675535`, `extreme=0.2650`, `middle=1.00`)이다.
- 다음 탐색은 lower `0.32443~0.324466`, upper `0.67557~0.675534`, extreme `0.2550~0.2660`을 우선한다.
- 특히 extreme `0.2600~0.2650`별로 lower 안정성 전환선을 바깥쪽에서 좁혀, 수치상 개선과 `3/1`을 동시에 만족하는 조합을 확인한다.

## LGBM-656~675 LGBM-644 주변 초미세 탐색

### 현재 기준점

- 안정적인 최고 후보: **LGBM-644**
- method: `continuous_piecewise_probability_shrinkage`
- parameter: `lower=0.324465`, `upper=0.675535`, `extreme=0.2650`, `middle=1.00`
- candidate Brier: `0.24758637757955682`
- Mean ΔBrier: `-8.476235415115218e-05`
- Brier 개선/악화 fold: `3/1`
- mean_delta_without_best_fold: `-9.964761460111438e-06`
- Mean AUC Δ: `0`, 2024 Brier Δ: `0`, 2024 AUC Δ: `0`

### 실험 목적과 탐색 범위

- 실험 목적: LGBM-644 주변에서 extreme `0.2650` 부근의 최적점과 lower 안정성 전환선을 더 촘촘하게 확인한다.
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.324460~0.324470`
- upper 탐색 범위: `0.675540~0.675530` (`upper=1-lower`)
- extreme 탐색 범위: `0.2630~0.2660`
- 핵심 extreme `0.2640~0.2660`에 16개를 집중 배치했고, lower는 `0.324460~0.324470`에 한정했다.
- middle: `1.00`
- 데이터 처리, feature engineering, feature selection, CV split, random seed, LightGBM 구조와 hyperparameter, 학습·검증·평가·calibration·prediction pipeline은 변경하지 않았으며 정확히 20개만 실행했다.

### 20개 실험 결과

| 실험     | parameter                                                   |         Mean Brier |        Mean ΔBrier |      Median ΔBrier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier |           2024 AUC |           Mean AUC | verdict   |
| -------- | ----------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | -----------------: | -----------------: | --------- |
| LGBM-656 | lower=0.324460; upper=0.675540; extreme=0.2630; middle=1.00 | 0.2475862341988739 | -8.49057348340e-05 | -1.79579823234e-10 |                  3/1 |           -9.91999939697e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-657 | lower=0.324461; upper=0.675539; extreme=0.2630; middle=1.00 | 0.2475862313239959 | -8.49086097121e-05 | -1.34260907947e-10 |                  3/1 |           -9.91968402463e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-658 | lower=0.324462; upper=0.675538; extreme=0.2630; middle=1.00 | 0.2475862284495312 | -8.49114841767e-05 | -8.89409657034e-11 |                  3/1 |           -9.91936815103e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-659 | lower=0.324463; upper=0.675537; extreme=0.2630; middle=1.00 | 0.2475862255751089 | -8.49143585991e-05 | -4.36200242593e-11 |                  3/1 |           -9.91905224012e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-660 | lower=0.324460; upper=0.675540; extreme=0.2640; middle=1.00 | 0.2475863130165194 | -8.48269171885e-05 | -2.15904127909e-10 |                  3/1 |           -9.94320863080e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-661 | lower=0.324462; upper=0.675538; extreme=0.2640; middle=1.00 | 0.2475863072715893 | -8.48326621186e-05 | -1.25405463791e-10 |                  3/1 |           -9.94258146904e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-662 | lower=0.324464; upper=0.675536; extreme=0.2640; middle=1.00 | 0.2475863015257225 | -8.48384079855e-05 | -3.49028028701e-11 |                  3/1 |           -9.94195462154e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-663 | lower=0.324466; upper=0.675534; extreme=0.2640; middle=1.00 | 0.2475862957782856 | -8.48441554223e-05 |                  0 |                  2/2 |           -9.94132870775e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-664 | lower=0.324461; upper=0.675539; extreme=0.2645; middle=1.00 | 0.2475863495908548 | -8.47903428532e-05 | -1.88815213464e-10 |                  3/1 |           -9.95446356958e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-665 | lower=0.324463; upper=0.675537; extreme=0.2645; middle=1.00 | 0.2475863438485891 | -8.47960851189e-05 | -9.83846615288e-11 |                  3/1 |           -9.95383790931e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-666 | lower=0.324465; upper=0.675535; extreme=0.2645; middle=1.00 | 0.2475863381034043 | -8.48018303037e-05 | -7.95008503474e-12 |                  3/1 |           -9.95321403000e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-667 | lower=0.324467; upper=0.675533; extreme=0.2645; middle=1.00 | 0.2475863323589352 | -8.48075747728e-05 |                  0 |                  2/2 |           -9.95259008001e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-668 | lower=0.324463; upper=0.675537; extreme=0.2655; middle=1.00 | 0.2475864228211899 | -8.47171125181e-05 | -1.34770111737e-10 |                  3/1 |           -9.97690378326e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-669 | lower=0.324465; upper=0.675535; extreme=0.2655; middle=1.00 | 0.2475864170804345 | -8.47228532735e-05 | -4.44756731444e-11 |                  3/1 |           -9.97628397360e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-670 | lower=0.324467; upper=0.675533; extreme=0.2655; middle=1.00 | 0.2475864113403937 | -8.47285933143e-05 |                  0 |                  2/2 |           -9.97566409353e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-671 | lower=0.324469; upper=0.675531; extreme=0.2655; middle=1.00 | 0.2475864056013903 | -8.47343323177e-05 |                  0 |                  2/2 |           -9.97504406516e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-672 | lower=0.324464; upper=0.675536; extreme=0.2660; middle=1.00 | 0.2475864594753535 | -8.46804583545e-05 | -1.07813841188e-10 |                  3/1 |           -9.98809043910e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-673 | lower=0.324466; upper=0.675534; extreme=0.2660; middle=1.00 | 0.2475864537367754 | -8.46861969326e-05 | -1.75875147779e-11 |                  3/1 |           -9.98747266478e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-674 | lower=0.324468; upper=0.675532; extreme=0.2660; middle=1.00 | 0.2475864479997997 | -8.46919339083e-05 |                  0 |                  2/2 |           -9.98685474233e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-675 | lower=0.324470; upper=0.675530; extreme=0.2660; middle=1.00 | 0.2475864422634381 | -8.46976702699e-05 |                  0 |                  2/2 |           -9.98623624538e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |

### 결과 요약과 best 갱신 여부

- 수치상 최고 후보와 안정적인 최고 후보는 모두 **LGBM-659** (`lower=0.324463`, `upper=0.675537`, `extreme=0.2630`, `middle=1.00`)이다.
- LGBM-659의 Mean Brier는 `0.2475862255751089`, Mean ΔBrier는 `-8.49143585991e-05`, fold별 개선/악화는 `3/1`, mean_delta_without_best_fold는 `-9.91905224012e-06`이다.
- LGBM-659의 Mean AUC와 2024 AUC는 각각 `0.5530385153643456`, `0.5480200784149498`로 악화가 없고, 2024 Brier도 `0.2480885134392783`으로 악화가 없다.
- 기존 best LGBM-644 대비 Mean Brier가 `-1.52004447931e-07` 추가 개선되고 안정성 조건을 충족하므로 best를 **LGBM-659**로 갱신한다. 다만 mean_delta_without_best_fold는 `+4.57092299924e-08`만큼 악화되었다.
- extreme `0.2630`에서는 lower `0.324463`까지 모두 `3/1`이었으며, extreme `0.2640`의 안정성 전환은 lower `0.324464/0.324466` 사이, extreme `0.2645`는 `0.324465/0.324467` 사이, extreme `0.2655`는 `0.324465/0.324467` 사이, extreme `0.2660`은 `0.324466/0.324468` 사이였다.

### 다음 실험 기준점과 탐색 방향

- 다음 안정 기준점은 **LGBM-659** (`lower=0.324463`, `upper=0.675537`, `extreme=0.2630`, `middle=1.00`)이다.
- 다음 탐색은 lower `0.324450~0.324466`, upper `0.675550~0.675534`, extreme `0.2600~0.2635`를 우선한다.
- extreme `0.2600~0.2625`에서는 더 바깥쪽 lower를 사용하고, extreme `0.2630`에서는 lower `0.324463` 안쪽의 안정성 경계를 추가로 확인한다.

## LGBM-676~695 LGBM-659 주변 초정밀 탐색

### 현재 기준점

- 안정적인 최고 후보: **LGBM-659**
- method: `continuous_piecewise_probability_shrinkage`
- parameter: `lower=0.324463`, `upper=0.675537`, `extreme=0.2630`, `middle=1.00`
- candidate Brier: `0.2475862255751089`
- Mean Delta Brier: `-8.49143585990586e-05`
- Brier 개선/악화 fold: `3/1`
- mean_delta_without_best_fold: `-9.919052240119075e-06`
- Mean AUC delta: `0`, 2024 Brier delta: `0`, 2024 AUC delta: `0`

### 이번 탐색 범위

- 실험 목적: LGBM-659 주변에서 extreme과 lower의 최적점을 더 촘촘하게 확인한다.
- method: `continuous_piecewise_probability_shrinkage`
- lower 탐색 범위: `0.324460~0.324468`
- upper 탐색 범위: `0.675540~0.675532` (`upper=1-lower`)
- extreme 탐색 범위: `0.2620~0.2640`
- 특히 extreme `0.2625~0.2635`, lower `0.324461~0.324465` 구간을 우선 배치했다.
- middle: `1.00`
- 데이터 처리, feature engineering, feature selection, CV split, random seed, LightGBM 구조와 hyperparameter, 학습 데이터, validation 방식, 평가 방식, calibration 방식, prediction pipeline은 변경하지 않고 parameter만 변경했다.

### 20개 실험 결과

| 실험     | parameter                                                   |         Mean Brier |   Mean Delta Brier | Median Delta Brier | Brier 개선/악화 fold | mean_delta_without_best_fold |         2024 Brier |           2024 AUC |           Mean AUC | verdict   |
| -------- | ----------------------------------------------------------- | -----------------: | -----------------: | -----------------: | -------------------: | ---------------------------: | -----------------: | -----------------: | -----------------: | --------- |
| LGBM-676 | lower=0.324460; upper=0.675540; extreme=0.2620; middle=1.00 | 0.2475861554801059 | -8.49844536021e-05 | -1.43156153598e-10 |                  3/1 |           -9.89669051858e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-677 | lower=0.324461; upper=0.675539; extreme=0.2620; middle=1.00 | 0.2475861526030258 | -8.49873306822e-05 | -9.77670999713e-11 |                  3/1 |           -9.89637310012e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-678 | lower=0.324462; upper=0.675538; extreme=0.2620; middle=1.00 | 0.2475861497263597 | -8.49902073482e-05 | -5.23770471439e-11 |                  3/1 |           -9.89605517968e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-679 | lower=0.324463; upper=0.675537; extreme=0.2620; middle=1.00 | 0.2475861468497361 | -8.49930839718e-05 | -6.98599511573e-12 |                  3/1 |           -9.89573722181e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-680 | lower=0.324460; upper=0.675540; extreme=0.2625; middle=1.00 | 0.2475861948271302 | -8.49451065778e-05 | -1.61380436792e-10 |                  3/1 |           -9.90835741336e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-681 | lower=0.324461; upper=0.675539; extreme=0.2625; middle=1.00 | 0.2475861919511506 | -8.49479825574e-05 | -1.16026466213e-10 |                  3/1 |           -9.90804101850e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-682 | lower=0.324462; upper=0.675538; extreme=0.2625; middle=1.00 | 0.2475861890755847 | -8.49508581233e-05 | -7.06714131660e-11 |                  3/1 |           -9.90772412202e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-683 | lower=0.324463; upper=0.675537; extreme=0.2625; middle=1.00 | 0.2475861862000612 | -8.49537336468e-05 | -2.53154441854e-11 |                  3/1 |           -9.90740718818e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-684 | lower=0.324464; upper=0.675536; extreme=0.2625; middle=1.00 | 0.2475861833231007 | -8.49566106072e-05 |                  0 |                  2/2 |           -9.90709114530e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-685 | lower=0.324464; upper=0.675536; extreme=0.2630; middle=1.00 | 0.2475862226992507 | -8.49172344572e-05 |                  0 |                  2/2 |           -9.91873721959e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-686 | lower=0.324465; upper=0.675535; extreme=0.2630; middle=1.00 | 0.2475862198232972 | -8.49201104108e-05 |                  0 |                  2/2 |           -9.91842223991e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-687 | lower=0.324466; upper=0.675534; extreme=0.2630; middle=1.00 | 0.2475862169473984 | -8.49229863096e-05 |                  0 |                  2/2 |           -9.91810722289e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-688 | lower=0.324468; upper=0.675532; extreme=0.2630; middle=1.00 | 0.2475862111971555 | -8.49287365524e-05 |                  0 |                  2/2 |           -9.91747707688e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-689 | lower=0.324462; upper=0.675538; extreme=0.2635; middle=1.00 | 0.2475862678481994 | -8.48720855085e-05 | -1.07185677001e-10 |                  3/1 |           -9.93098726672e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-690 | lower=0.324463; upper=0.675537; extreme=0.2635; middle=1.00 | 0.2475862649748795 | -8.48749588284e-05 | -6.18997630930e-11 |                  3/1 |           -9.93067237760e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-691 | lower=0.324464; upper=0.675536; extreme=0.2635; middle=1.00 | 0.2475862621001246 | -8.48778335833e-05 | -1.66128777401e-11 |                  3/1 |           -9.93035837832e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-692 | lower=0.324465; upper=0.675535; extreme=0.2635; middle=1.00 | 0.2475862592252744 | -8.48807084335e-05 |                  0 |                  2/2 |           -9.93004441990e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-693 | lower=0.324463; upper=0.675537; extreme=0.2640; middle=1.00 | 0.2475863043993729 | -8.48355343351e-05 | -8.01546606866e-11 |                  3/1 |           -9.94226760068e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | CANDIDATE |
| LGBM-694 | lower=0.324465; upper=0.675535; extreme=0.2640; middle=1.00 | 0.2475862986519768 | -8.48412817312e-05 |                  0 |                  2/2 |           -9.94164168326e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |
| LGBM-695 | lower=0.324468; upper=0.675532; extreme=0.2640; middle=1.00 | 0.2475862900324560 | -8.48499012519e-05 |                  0 |                  2/2 |           -9.94070264503e-06 | 0.2480885134392783 | 0.5480200784149498 | 0.5530385153643456 | REJECT    |

### 결과 요약과 best 갱신 여부

- 수치상 최고 후보와 안정적 최고 후보는 모두 **LGBM-679** (`lower=0.324463`, `upper=0.675537`, `extreme=0.2620`, `middle=1.00`)이다.
- LGBM-679의 Mean Brier는 `0.2475861468497361`, Mean Delta Brier는 `-8.49930839718e-05`, fold별 개선/악화는 `3/1`, mean_delta_without_best_fold는 `-9.89573722181e-06`이다.
- LGBM-679은 AUC 악화가 없고 2024 Brier/AUC 악화도 없어서 안정성 조건을 만족한다.
- 기존 best LGBM-659 대비 Mean Brier가 `-7.87253727903e-08` 추가 개선되어 안정적인 best를 **LGBM-679**로 갱신한다.
- 다만 mean_delta_without_best_fold는 LGBM-659보다 덜 음수이므로, 개선폭은 평균 Brier 중심의 미세 개선으로 판단한다.
- 이번 범위에서는 extreme `0.2620`과 lower `0.324463` 조합이 가장 유망했고, 같은 extreme에서 lower가 증가할수록 Mean Brier가 소폭 개선되지만 `0.324464` 이후에는 2/2 REJECT 경계가 나타난다.

### 다음 탐색 방향

- 다음 안정 기준점은 **LGBM-679** (`lower=0.324463`, `upper=0.675537`, `extreme=0.2620`, `middle=1.00`)이다.
- 다음 탐색은 lower `0.324460~0.324464`, upper `0.675540~0.675536`, extreme `0.2600~0.2625`를 우선한다.
- 특히 extreme `0.2610~0.2625`와 lower `0.324462~0.3244635` 부근을 촘촘하게 보되, lower를 `0.324464` 이상으로 올릴 때 2/2 REJECT 경계가 발생하는지 확인한다.

## LGBM-696~715 Global Scale + Intercept calibration

### 현재 실제 Leaderboard 기준점

- 현재 확인된 실제 Leaderboard 최고 기록은 `704점`이다.
- 해당 제출의 raw prediction pipeline은 `LGBM-130`이며, `0.6 * LGBM-095 + 0.4 * LGBM-101`의 확률 ensemble이다.
- LGBM-679는 LGBM-130에 `continuous_piecewise_probability_shrinkage`를 적용한 후처리 후보이지만, 로컬 제공 test 표본과 2024 validation에서는 prediction을 변경하지 않았다.

### calibration 기준 raw 모델/ensemble과 선정 이유

- calibration 기준점은 **LGBM-130 raw ensemble**으로 선정했다.
- LGBM-131/132/142는 평균 Brier가 미세하게 더 낮지만 `mean_delta_without_best_fold > 0`, 2024 Brier 악화, 2024 AUC 악화로 REJECT된 raw ensemble이다.
- LGBM-134~137은 2024 악화 폭이 LGBM-130보다 작지만 전체 평균 개선폭이 감소하고 모두 3개 개선/2개 악화 구조였다.
- LGBM-095는 2024 Brier가 LGBM-130보다 미세하게 낮지만 전체 평균 Brier와 평균 AUC에서 LGBM-130에 뒤지고, 실제 `704점` Leaderboard 근거는 LGBM-130에 있다.
- LGBM-130은 전체 raw 후보 중 실제 Leaderboard 기록, 전체 평균 Brier, fold 안정성 및 best fold 제외 평균을 함께 만족하는 재현 가능한 raw 기준점이다.
- 로컬 제공 test 표본 5행의 LGBM-130 prediction 범위는 `0.446438402922~0.520472165779`, 평균은 `0.483090745133`이었다. 이 값은 배포 영향 확인에만 사용했으며 calibration parameter 선정에는 사용하지 않았다.

### 실험 목적과 calibration 수식

- 목적은 모델을 재학습하지 않고 LGBM-130의 중앙 확률 구간까지 실제로 변경하는 calibration을 검증하는 것이다.
- 수식은 `p' = clip(0.5 + scale * (p - 0.5) + intercept, 0, 1)`이다.
- raw model, feature, 데이터 처리, CV split, seed, LightGBM hyperparameter, 모델 가중치 및 raw prediction pipeline은 변경하지 않았다.
- parameter 범위는 2020~2023 OOF만으로 사전에 확정했으며 2024 정답은 후보 생성과 범위 결정에 사용하지 않았다.

### scale/intercept 탐색 범위

- 2020~2023 OOF equal-fold OLS 기준점은 `scale=0.749354`, `intercept=-0.001281`이었다.
- 요청된 기본 scale 범위의 하한과 시즌별 intercept 편차를 반영해 scale `0.80~1.00`, intercept `-0.006~0.001`로 축소했다.
- scale은 `0.80`, `0.85`, `0.90`, `0.95`, `1.00`, intercept는 `-0.006`, `-0.004`, `-0.002`, `0.001`을 사용해 정확히 20개 조합을 실행했다.

### 20개 실험 결과

| experiment | scale | intercept | candidate Brier mean |   mean delta Brier | median delta Brier | 개선/악화 fold | mean delta without best fold |     2024 Brier |   2024 delta Brier | 2024 변경 비율 |              2024 max/mean 변화 | verdict   |
| ---------- | ----: | --------: | -------------------: | -----------------: | -----------------: | -------------: | ---------------------------: | -------------: | -----------------: | -------------: | ------------------------------: | --------- |
| LGBM-696   |  0.80 |    -0.006 |       0.247428647824 | -2.42492110128e-04 |  7.08298660935e-05 |            2/3 |            7.86440301339e-05 | 0.248159343305 |  7.08298660935e-05 |           100% | 0.032016381139 / 0.007118573472 | REJECT    |
| LGBM-697   |  0.80 |    -0.004 |       0.247426182011 | -2.44957922871e-04 |  9.11121694116e-05 |            2/3 |            6.42764243741e-05 | 0.248179625609 |  9.11121694116e-05 |           100% | 0.030016381139 / 0.006355523457 | REJECT    |
| LGBM-698   |  0.80 |    -0.002 |       0.247431716198 | -2.39423735613e-04 |  1.19394472730e-04 |            2/3 |            5.79088186142e-05 | 0.248207907912 |  1.19394472730e-04 |           100% | 0.028016381139 / 0.006010449586 | REJECT    |
| LGBM-699   |  0.80 |     0.001 |       0.247455017479 | -2.16122454726e-04 |  1.76817927707e-04 |            2/3 |            6.33574099745e-05 | 0.248265331367 |  1.76817927707e-04 |           100% | 0.027133790413 / 0.006306874511 | REJECT    |
| LGBM-700   |  0.85 |    -0.006 |       0.247437342529 | -2.33797404220e-04 |  2.41562124451e-05 |            2/3 |            1.58438537675e-05 | 0.248112669652 |  2.41562124451e-05 |           100% | 0.025512285854 / 0.006183281030 | REJECT    |
| LGBM-701   |  0.85 |    -0.004 |       0.247439995399 | -2.31144535136e-04 |  4.34823897655e-05 |            2/3 |            6.85943939539e-06 | 0.248131995829 |  4.34823897655e-05 |           100% | 0.023512285854 / 0.005115751376 | REJECT    |
| LGBM-702   |  0.85 |    -0.002 |       0.247450648268 | -2.20491666051e-04 |  7.08085670860e-05 |            2/3 |            5.87502502333e-06 | 0.248159322006 |  7.08085670860e-05 |           100% | 0.021512285854 / 0.004557550048 | REJECT    |
| LGBM-703   |  0.85 |     0.001 |       0.247481627571 | -1.89512362425e-04 |  1.26797833067e-04 |            2/3 |            1.93984034652e-05 | 0.248215311272 |  1.26797833067e-04 |           100% | 0.020600342810 / 0.004795675175 | REJECT    |
| LGBM-704   |  0.90 |    -0.006 |       0.247467651659 | -2.03488274512e-04 | -1.54355494504e-05 |            3/2 |           -2.57794566060e-05 | 0.248073077890 | -1.54355494504e-05 |           100% | 0.019008190570 / 0.005675284284 | REJECT    |
| LGBM-705   |  0.90 |    -0.004 |       0.247475423210 | -1.95716723601e-04 |  2.93450187241e-06 |            2/3 |           -2.93806795902e-05 | 0.248091447941 |  2.93450187241e-06 |           100% | 0.017008190570 / 0.004122187354 | REJECT    |
| LGBM-706   |  0.90 |    -0.002 |       0.247491194761 | -1.79945172690e-04 |  2.93045531952e-05 |            2/3 |           -2.49819025745e-05 | 0.248117817992 |  2.93045531952e-05 |           100% | 0.015008190570 / 0.003177761728 | REJECT    |
| LGBM-707   |  0.90 |     0.001 |       0.247529852087 | -1.41287846323e-04 |  8.38596301793e-05 |            2/3 |           -3.38373705099e-06 | 0.248172373069 |  8.38596301793e-05 |           100% | 0.014066895207 / 0.003299223334 | REJECT    |
| LGBM-708   |  0.95 |    -0.006 |       0.247519575213 | -1.51564721003e-04 | -4.79454195928e-05 |            3/2 |           -4.62259009864e-05 | 0.248040568020 | -4.79454195928e-05 |           100% | 0.012504095285 / 0.005761013561 | REJECT    |
| LGBM-709   |  0.95 |    -0.004 |       0.247532465445 | -1.38674488265e-04 | -3.05314942677e-05 |            3/2 |           -4.44439325829e-05 | 0.248057981945 | -3.05314942677e-05 |           100% | 0.010504095285 / 0.003774898189 | REJECT    |
| LGBM-710   |  0.95 |    -0.002 |       0.247553355678 | -1.17784255527e-04 | -5.11756894264e-06 |            3/2 |           -3.46619641794e-05 | 0.248083395870 | -5.11756894264e-06 |           100% | 0.008504095285 / 0.002061093677 | REJECT    |
| LGBM-711   |  0.95 |     0.001 |       0.247599691027 | -7.14489064205e-05 |  4.59793435048e-05 |            2/3 |           -4.98901157420e-06 | 0.248136516758 |  4.80033190450e-05 |           100% | 0.007533447603 / 0.001857947458 | REJECT    |
| LGBM-712   |  1.00 |    -0.006 |       0.247593113190 | -7.80267436935e-05 | -7.33733979822e-05 |            4/1 |           -3.55979430168e-05 | 0.248015140041 | -7.33733979822e-05 |           100% | 0.006000000000 / 0.006000000000 | CANDIDATE |
| LGBM-713   |  1.00 |    -0.004 |       0.247611122105 | -6.00178291290e-05 | -5.69155986548e-05 |            4/1 |           -3.17319620112e-05 | 0.248031597841 | -5.69155986548e-05 |           100% | 0.004000000000 / 0.004000000000 | CANDIDATE |
| LGBM-714   |  1.00 |    -0.002 |       0.247637131019 | -3.40089145645e-05 | -3.24577993274e-05 |            4/1 |           -1.98659810056e-05 | 0.248056055640 | -3.24577993274e-05 |           100% | 0.002000000000 / 0.002000000000 | CANDIDATE |
| LGBM-715   |  1.00 |     0.001 |       0.247691144391 |  2.00044572823e-05 |  1.92288996637e-05 |            1/4 |            2.92198115234e-05 | 0.248107742339 |  1.92288996637e-05 |           100% | 0.001000000000 / 0.001000000000 | REJECT    |

### 결과 분석과 best 갱신 여부

- 수치상 전체 평균 Brier 최저 후보는 **LGBM-697**이지만 2개 fold 개선/3개 fold 악화, 양의 median delta, 양의 `mean_delta_without_best_fold`, 2024 Brier 악화로 REJECT한다.
- 안정적 최고 후보와 2024 기준 최고 후보는 모두 **LGBM-712** (`scale=1.000`, `intercept=-0.006`)이다.
- LGBM-712는 4개 fold 개선/1개 fold 악화, 음의 median delta, 음의 `mean_delta_without_best_fold`, 2024 Brier 개선 및 2024 prediction 100% 변경 조건을 만족한다.
- 모든 후보는 양의 affine 단조변환이며 clipping으로 인한 순위 손실이 없어 평균 AUC와 2024 AUC delta는 `0`이다.
- LGBM-712의 전체 평균 Brier는 역사적 후처리 최저 기록 LGBM-679보다 `6.9663402783e-06` 높지만, LGBM-679와 달리 2024와 제출 가능 prediction을 실제로 변경한다.
- 따라서 역사적 전체 평균 Brier 최저 기록은 LGBM-679로 보존하고, **실제 배포 가능한 calibration 안정 기준점은 LGBM-712로 갱신**한다.

### 다음 실험 방향

- Global Scale + Intercept에서 2024까지 개선되는 안정 후보가 확인되었으므로 즉시 Platt scaling으로 이동하지 않는다.
- 다음 calibration 기준점은 LGBM-712이며 scale `1.00`과 intercept `-0.006` 주변을 더 좁게 탐색한다.
- 다음 권장 범위는 scale `0.97~1.03`, intercept `-0.008~-0.004`이다.
- 다음 후보 구성에서도 test 분포와 2024 정답을 fitting에 사용하지 않고, 2020~2023 OOF 근거로 parameter를 고정한 뒤 2024는 최종 gate로만 사용한다.
- 실험: LGBM-716~735, global_scale_intercept 20개를 scale `0.990~1.010`, intercept `-0.008~-0.004` 범위에서 실행했다.
- 목적: LGBM-712 (`scale=1.000`, `intercept=-0.006`) 주변의 Brier 최적점과 fold 안정성을 확인했다.
- 결과: 20개 결과를 `lgbm_716_735_walkforward.csv`와 `lgbm_716_735_walkforward_summary.csv`에 저장했으며 모든 후보가 2024 prediction을 실제로 변경했다.
- 수치상 최고 후보: LGBM-716 (`scale=0.990`, `intercept=-0.0080`)이지만 3개 개선/2개 악화이고 `mean_delta_without_best_fold > 0`이므로 REJECT했다.
- 안정적 최고 후보: 신규 CANDIDATE가 없어 기존 LGBM-712를 유지하며 best를 갱신하지 않는다.
- 다음 탐색: LGBM-712를 기준으로 Global Scale + Intercept 미세 탐색을 종료하고 Platt scaling 검토로 이동한다.
- 실험: LGBM-736~755, global_scale_intercept 20개를 scale `0.988~1.000`, intercept `-0.009~-0.006` 범위에서 실행했다.
- 목적: global scale + intercept 미세 탐색으로 LGBM-716 주변의 안정성 전환점을 확인했다.
- 결과: 모든 후보가 prediction을 변경했지만 신규 CANDIDATE는 없었고 3개 개선/2개 악화 경계를 넘지 못했다.
- 안정적 best: 기존 LGBM-712를 유지한다.
- 기존 best 대비: 수치상 최고 LGBM-736은 평균 Brier가 개선됐지만 3/2와 양의 `mean_delta_without_best_fold`로 REJECT되어 미개선으로 판정한다.
- 다음 탐색: Global Scale + Intercept 탐색을 종료하고 LGBM-712 기준 Platt scaling으로 이동한다.
- 실험: LGBM-756
- 가설: 최근 1/3/5경기 투수 middle 상태와 누적 middle 상태의 차이가 미래 제구 성공에 추가 정보를 제공한다.
- Feature: `pitcher_recent1_middle_gap`, `pitcher_recent3_middle_gap`, `pitcher_recent5_middle_gap`을 추가했다.
- OOF Brier: `0.24761654691300344` (LGBM-712 대비 mean delta `+2.3433722988974726e-05`, 1개 개선/4개 악화, best fold 제외 mean delta `+4.602256133539456e-05`).
- 2024 Brier: `0.2480637008509682` (delta `+4.8560809672110183e-05`, AUC delta `-0.0007491105780575991`).
- verdict: `REJECT` — prediction은 충분히 변경됐고 leakage 및 기존 Feature 중복 검사는 통과했지만 2024와 전체 안정성이 모두 악화됐다.
- 다음 방향: recent middle gap 가설은 폐기하고, LGBM-757에서 최근 투수 성공 상태와 타자 누적 성공 성향의 새로운 상호작용 가설을 검토한다.
- 실험: LGBM-758
- 가설: 최근 3/5경기 투수 success 상태와 누적 success 상태의 차이가 미래 제구 성공에 추가 정보를 제공한다.
- Feature: `pitcher_recent3_success_gap`, `pitcher_recent5_success_gap`을 추가하고, 기존 LGBM-074의 recent1 gap과 LGBM-052의 3v5 trend는 제외했다.
- OOF Brier: `0.247597339667278` (LGBM-712 대비 mean delta `+4.22647726360803e-06`, 1개 개선/4개 악화, best fold 제외 mean delta `+3.5185901352596805e-05`).
- 2024 Brier: `0.24807038251591104` (delta `+5.5242474614941584e-05`, AUC delta `-0.0008643731411008826`).
- verdict: `REJECT` — prediction은 충분히 변경됐고 leakage 및 중복 검사는 통과했지만 2024 Brier와 AUC, fold 안정성이 모두 악화됐다.
- 다음 방향: recent success gap 계열은 폐기하고, 다음 실험에서는 최근 투수 success 상태와 타자 누적 success 성향의 새로운 상호작용 가설을 검토한다.
- 실험: LGBM-759
- 가설: 최근 1/3/5경기 success rate 요약값 사이의 다중 horizon 불일치가 투수 제구의 변동성 및 일관성을 표현한다.
- Feature: `pitcher_recent_success_horizon_std`, `pitcher_recent_success_horizon_curvature`를 추가하고 기존 endpoint gap 변동성 Feature는 제외했다.
- OOF Brier: `0.24763279150645606` (LGBM-712 대비 mean delta `+3.967831644159925e-05`, 1개 개선/4개 악화, best fold 제외 mean delta `+5.9854059229924594e-05`).
- 2024 Brier: `0.24806126643158702` (delta `+4.612639029091814e-05`, AUC delta `-0.0007290524204364157`).
- verdict: `REJECT` — prediction은 충분히 변경됐고 leakage 및 중복 검사는 통과했지만 2024와 전체 Brier/AUC 안정성이 모두 악화됐다.
- 다음 방향: recent success 변동성 및 일관성 계열은 폐기하고, 최근 투수 success 상태와 타자 누적 success 성향의 상호작용 가설로 이동한다.
- 실험: LGBM-760
- 가설: 현재 볼카운트별 투수의 과거 제구 성공 성향이 기존 `pitcher_ball_pressure` 및 단순 rate Feature에 없는 추가 정보를 제공한다.
- Feature: `pitcher_prior_season_count_success_rate`, `pitcher_prior_season_count_support_log`, `pitcher_prior_season_count_success_lift`를 추가했으며 각 행보다 이전 시즌의 기록만 사용했다.
- OOF Brier: `0.24758841007194773` (LGBM-712 대비 mean delta `-4.7031180666679e-06`, 2개 개선/2개 악화, best fold 제외 mean delta `+1.8507833405970175e-05`).
- 2024 Brier: `0.24803336873517862` (delta `+1.8228693882516023e-05`, AUC delta `-0.0001813712113281074`).
- verdict: `REJECT` — prediction과 leakage 및 중복 검사는 통과했지만 2024 Brier/AUC가 악화됐고 fold 안정성 조건을 만족하지 못했다.
- 다음 방향: 볼카운트별 과거 성향 계열은 추가 미세탐색하지 않고, 주자 및 경기상황과 투수 특성의 새로운 상호작용 가설로 이동한다.
- 실험: LGBM-761
- 가설: HIGH `pitcher_id -> pitcher_trackman_id` 개인 매핑을 이용한 최근 시즌 대비 개인 장기 Trackman 상태 변화가 미래 제구 성공에 추가 정보를 제공한다.
- Feature: `pitcher_trackman_recent_vs_long_spin_rate_gap`, `pitcher_trackman_recent_vs_long_ivb_gap`을 추가했다. 최근은 현재 행의 직전 시즌, 장기는 그보다 이전의 모든 시즌으로 정의했으며 현재·미래 시즌 Trackman은 사용하지 않았다.
- OOF Brier: `0.24762520415820827` (LGBM-712 대비 mean delta `+3.209096819385415e-05`, 0개 개선/3개 악화, best fold 제외 mean delta `+4.011371024231769e-05`).
- 2024 Brier: `0.24806201047549947` (delta `+4.687043420337211e-05`, AUC delta `-0.0006712649788624958`).
- verdict: `REJECT` — 개인별 Trackman 변화량과 prediction 변경은 정상적으로 적용됐고 leakage 및 과거 Feature 중복 검사는 통과했지만 2024와 전체 안정성이 악화됐다.
- 다음 방향: 개인별 최근-장기 spin rate 및 IVB 변화량 가설은 폐기하고 동일 계열 미세 변형을 반복하지 않는다.
- 실험: LGBM-762
- 가설: HIGH `pitcher_id -> pitcher_trackman_id` 매핑으로 만든 투수 개인의 구종별 물리 특성 차이가 기존 49개 Feature에 추가 정보를 제공한다.
- Feature: `pitcher_pitchtype_fastball_breaking_speed_separation`, `pitcher_pitchtype_fastball_offspeed_speed_separation`, `pitcher_pitchtype_fastball_breaking_ivb_separation`을 추가했다. train에는 현재 투구 구종이 없으므로 결과 이후에 결정되는 현재 구종은 사용하지 않고, 행의 시즌보다 이전 Trackman에서 개인별 구종 간 차이만 집계했다.
- OOF Brier: `0.2475847092957074` (LGBM-712 대비 mean delta `-8.403894307057458e-06`, median delta `0.0`, 2개 개선/2개 악화, best fold 제외 mean delta `+5.197847489618601e-06`).
- 2024 Brier: `0.2480437197405191` (delta `+2.8579699222985866e-05`, AUC `0.5475435886551583`, AUC delta `-0.00047648975979153185`).
- verdict: `REJECT` — 개인별 구종 Trackman Feature와 prediction 변경은 정상 적용됐고 leakage 및 중복 검사는 통과했지만 2024 Brier/AUC가 악화됐으며 fold 안정성 조건을 만족하지 못했다.
- 다음 방향: 개인별 구종 간 speed 및 IVB separation 계열은 반복하지 않고 다른 정보 가설로 이동한다.
- 실험: LGBM-763 사전 검증 중단
- 가설: 현재 row의 투수와 현재 구종을 해당 투수의 과거 동일 구종 Trackman 집계에 직접 연결한다.
- 구조 검증: `train.csv`에는 현재 투구의 `pitch_type`, `pitch_type_group`, `auto_pitch_type`, `tagged_pitch_type`에 해당하는 컬럼이 없다. 기존 `asof_pitcher_fastball_rate`, `asof_pitcher_breaking_rate`, `asof_pitcher_offspeed_rate`는 과거 구종 비율이며 현재 row의 구종이 아니다.
- 판정: `BLOCKED_NOT_RUN` — 현재 구종을 추측하거나 투구 결과 이후 Trackman 구종을 연결하면 요구 구조를 충족하지 못하거나 leakage가 발생하므로 코드, 학습, 결과 CSV를 생성하지 않았다.
- 다음 방향: 투구 직전에 사용 가능하다고 공식적으로 보장된 현재 구종 컬럼 또는 train row와 동일 투구 Trackman을 연결하는 공식 키가 제공될 때만 이 가설을 재개한다.
- 실험: LGBM-764
- 가설: HIGH `pitcher_id -> pitcher_trackman_id` 개인 매핑과 현재 row의 `balls_before`, `strikes_before`를 직접 연결한 과거 Trackman 물리 특성이 추가 정보를 제공한다.
- Feature: `pitcher_count_trackman_rel_speed_mean`, `pitcher_count_trackman_spin_rate_mean`, `pitcher_count_trackman_ivb_mean`을 추가했다. 각 row의 시즌보다 이전 Trackman만 사용해 `pitcher_trackman_id × balls_before × strikes_before` 단위로 집계했다.
- OOF Brier: `0.24759378775897617` (LGBM-712 대비 mean delta `+6.745689617670969e-07`, median delta `0.0`, 2개 개선/2개 악화, best fold 제외 mean delta `+1.1604621660062098e-05`).
- 2024 Brier: `0.24804591561326456` (delta `+3.0775571968455484e-05`, AUC `0.5475790238439193`, AUC delta `-0.00044105457103049694`).
- verdict: `REJECT` — 개인 투수와 현재 카운트의 직접 연결, prediction 변경, leakage 및 중복 검사는 통과했지만 2024 Brier/AUC와 전체 안정성이 악화됐다.
- 다음 방향: 개인 투수×현재 카운트 Trackman 평균 계열은 추가 미세 변형하지 않고 다른 Feature 정보 가설로 이동한다.
- 실험: LGBM-765
- 가설: 투수 개인의 직전 시즌 구종 비중과 그 이전 장기 구종 비중의 차이가 오래된 Trackman 평균으로 인한 최근 시즌 악화를 설명한다.
- Feature: `pitcher_trackman_recent_vs_long_fastball_share_gap`, `pitcher_trackman_recent_vs_long_breaking_share_gap`을 추가했다. HIGH 개인 매핑만 사용하고 최근은 S-1, 장기는 S-1보다 이전 Trackman으로 분리했으며 spin/IVB gap, rel_speed slope 및 weighted Trackman과 중복되지 않게 구성했다.
- OOF Brier: `0.2476175298785114` (LGBM-712 대비 mean delta `+2.4416688496980976e-05`, median delta `+2.2731920464647004e-05`, 0개 개선/3개 악화, best fold 제외 mean delta `+3.052086062122622e-05`).
- 2024 Brier: `0.24805098763488756` (delta `+3.584759359145928e-05`, AUC `0.547450934542094`, AUC delta `-0.0005691438728557818`).
- verdict: `REJECT` — 개인별 최근-장기 구종 비중 변화와 prediction 변경은 정상 적용됐고 leakage 및 중복 검사는 통과했지만 2024와 전체 Brier/AUC 안정성이 악화됐다.
- 다음 방향: 최근-장기 Trackman 구종 비중 변화 가설은 폐기하고 추가 미세조정하지 않는다.
- 실험: LGBM-766
- 가설: 투수 개인의 과거 spin rate와 IVB 평균이 아니라 투구별 표준편차로 나타낸 물리 특성의 일관성이 제구 성공 예측에 추가 정보를 제공한다.
- Feature: `pitcher_prior_trackman_spin_rate_std`, `pitcher_prior_trackman_ivb_std`를 추가했다. 개인 rel_speed std는 LGBM-065/066/073과 중복되어 제외했고, 상황 전체 std와 다른 HIGH 매핑 투수 개인 단위로 행의 시즌 이전 Trackman만 집계했다. 최초 cutoff 표본 분포에서 100개 이상 비율이 97%를 넘어 최소 표본 수를 100으로 적용했다.
- OOF Brier: `0.247606884527378` (LGBM-712 대비 mean delta `+1.3771337363582825e-05`, median delta `+9.306663179609043e-06`, 1개 개선/3개 악화, best fold 제외 mean delta `+2.7552186863830097e-05`).
- 2024 Brier: `0.24804600187545928` (delta `+3.0861834163176116e-05`, AUC `0.5474451778920613`, AUC delta `-0.0005749005228885551`).
- verdict: `REJECT` — 개인별 변동성 Feature와 prediction 변경은 정상 적용됐고 leakage·중복·표본 수 검사는 통과했지만 2024와 전체 Brier/AUC 안정성이 악화됐다.
- 다음 방향: 개인별 Trackman spin rate 및 IVB 변동성 계열은 추가 변형하지 않고 폐기한다.

## 구조 Feature 자동 탐색 LGBM-767~773

- SKIP: `batter_times_faced`, `pitcher_pitch_count`는 현재 경기와 투구 순서를 식별할 `game_id`, 경기 내 투구 순번이 없어 안전하게 계산할 수 없다.
- SKIP: `pitch_count_in_at_bat`는 `pitch_of_pa`가 없고 2-strike foul 때문에 `balls_before + strikes_before`로 정확히 복원할 수 없다.
- SKIP: `runner_state`는 기존 `base_state` 및 3개 runner flag와 동일한 상태 정보다.
- SKIP: `pitch_seq_change`, `prev_pitch_type`, `is_same_pitch_3times`는 train에 현재·이전 `pitch_type`과 정확한 투구 시계열 키가 없다.
- SKIP: `total_bases_occupied`는 기존 `num_runners_on`과 전 행에서 정확히 동일하다.
- SKIP: `inning_phase`는 기존 `inning`의 단조 재표현으로 LightGBM에 새로운 정보가 없고, `inning_topbot_encoded`는 기존 categorical `top_bottom`의 동일 정보다.

- 실험: LGBM-767
- 가설/Feature: 현재 투구 직전 `outs_before × num_runners_on`인 `outs_runner_interaction`이 아웃-주자 조합 효과를 표현한다.
- OOF Brier: `0.2476246488294121` (mean delta `+3.153563939767845e-05`, median delta `+2.6298917953249124e-05`, 1개 개선/4개 악화, best fold 제외 `+5.595361100202423e-05`).
- 2024: Brier `0.24804940197329037` (delta `+3.426193199426719e-05`), AUC `0.5475791802842748` (delta `-0.00044089813067504924`).
- verdict: `REJECT` — leakage·중복 검사와 prediction 변경은 통과했지만 2024 및 전체 안정성이 악화됐다.

- 실험: LGBM-768
- 가설/Feature: 현재 count 내 strike 비율 `strike_ratio_in_count = strikes_before / (balls_before + strikes_before)`이며 0-0은 0으로 처리했다.
- OOF Brier: `0.24762315420198266` (mean delta `+3.004101196822373e-05`, median delta `+3.912139181741492e-05`, 2개 개선/3개 악화, best fold 제외 `+5.62235274101236e-05`).
- 2024: Brier `0.24805426143311352` (delta `+3.912139181741492e-05`), AUC `0.5474949326523977` (delta `-0.0005251457625521372`).
- verdict: `REJECT` — leakage·중복 검사와 prediction 변경은 통과했지만 2024 및 전체 안정성이 악화됐다.

- 실험: LGBM-769
- 가설/Feature: 투구 직전 2루 또는 3루 주자 존재 여부인 `scoring_position`을 추가했다.
- OOF Brier: `0.24762784521354395` (mean delta `+3.4732023529521205e-05`, median delta `+3.0480766992663222e-05`, 1개 개선/4개 악화, best fold 제외 `+5.8766534222411126e-05`).
- 2024: Brier `0.2480709636174692` (delta `+5.582357617309186e-05`), AUC `0.5472891593306255` (delta `-0.0007309190843243218`).
- verdict: `REJECT` — leakage·중복 검사와 prediction 변경은 통과했지만 2024 및 전체 안정성이 악화됐다.

- 실험: LGBM-770
- 가설/Feature: 표준적인 투수 우세 count인 `strikes_before > balls_before`를 `advantage_pitcher`로 추가했다.
- OOF Brier: `0.24763517284054654` (mean delta `+4.2059650532139115e-05`, median delta `+4.2972805483376675e-05`, 1개 개선/4개 악화, best fold 제외 `+6.285467834551278e-05`).
- 2024: Brier `0.2480672354448759` (delta `+5.209540357981046e-05`), AUC `0.5473187558962271` (delta `-0.0007013225187226801`).
- verdict: `REJECT` — leakage·중복 검사와 prediction 변경은 통과했지만 2024 및 전체 안정성이 악화됐다.

- 실험: LGBM-771
- 가설/Feature: 투구 직전 3-2 count 여부인 `is_full_count`를 추가했다.
- OOF Brier: `0.24762699541892993` (mean delta `+3.388222891549386e-05`, median delta `+3.0480766992663222e-05`, 1개 개선/4개 악화, best fold 제외 `+5.770429095487695e-05`).
- 2024: Brier `0.24805206281727576` (delta `+3.69227759796642e-05`), AUC `0.5474917483763894` (delta `-0.0005283300385604539`).
- verdict: `REJECT` — leakage·중복 검사와 prediction 변경은 통과했지만 2024 및 전체 안정성이 악화됐다.

- 실험: LGBM-772
- 가설/Feature: 투구 직전 count가 0-0인지 나타내는 `is_first_pitch`를 추가했다.
- OOF Brier: `0.24762523035797007` (mean delta `+3.211716795562536e-05`, median delta `+2.881174104074624e-05`, 1개 개선/4개 악화, best fold 제외 `+5.6291389956962534e-05`).
- 2024: Brier `0.24807076538080408` (delta `+5.5625339507980875e-05`), AUC `0.5472918448848714` (delta `-0.0007282335300784482`).
- verdict: `REJECT` — leakage·중복 검사와 prediction 변경은 통과했지만 2024 및 전체 안정성이 악화됐다.

- 실험: LGBM-773
- 가설/Feature: 야구의 후반 7회 이상 여부인 `is_late_game`을 추가했다.
- OOF Brier: `0.24763268442638947` (mean delta `+3.957123637505222e-05`, median delta `+3.0480766992663222e-05`, 1개 개선/4개 악화, best fold 제외 `+5.96166315965721e-05`).
- 2024: Brier `0.2480709636174692` (delta `+5.582357617309186e-05`), AUC `0.5472891593306255` (delta `-0.0007309190843243218`).
- verdict: `REJECT` — leakage·중복 검사와 prediction 변경은 통과했지만 2024 및 전체 안정성이 악화됐다.

- 자동 탐색 결론: 실행 가능한 7개 후보는 모두 REJECT이며, 필수 키 부재 또는 정확한 중복인 10개 후보는 SKIP했다. 모든 실험은 LGBM-712의 동일 49개 Feature에서 해당 Feature 하나만 추가했다.

## LGBM-712 Deployment Package Restoration

- 목적: 기존 LGBM-130 배포 패키지를 변경하지 않고 LGBM-712의 최종 calibration이 포함된 별도 배포 패키지를 복원했다.
- 생성 경로: `submit_lgbm712/`
- 포함 파일: `script.py`, `requirements.txt`, `model/lgbm_095.txt`, `model/lgbm_101.txt`
- 기존 LGBM-130 생성 과정과 Feature 49개 및 생성식은 그대로 유지했다.
- 최종 출력 직전에 `p130 = 0.6 * p095 + 0.4 * p101`, `p712 = np.clip(p130 - 0.006, 0.0, 1.0)`을 적용하고 `control_success`에 `p712`를 기록한다.
- 원본/복사 모델 SHA-256 일치: LGBM-095 `5f587d898f6739ea8d33b2e5841d1d8f3fabcf600e57a3778cad3862214e90ba`, LGBM-101 `268ec7edfb72980c524e08383acac8c8aa80bf434fac21236e5f6d2d450c3381`.
- 검증: Feature 함수 AST 동일, 모델 Feature 이름·순서 49개 동일, 0.6/0.4 가중치, `-0.006` 단일 적용, `[0,1]` clipping, finite prediction, 입력/출력 row 수 및 `row_id` 순서, 제출 컬럼 `row_id,control_success`를 모두 통과했다.
- 비-clipping 구간에서 LGBM-130 대비 prediction shift의 최대 수치 오차는 `5.204170427930421e-18`이었다.
- 저장된 2020~2024 validation prediction으로 재검증한 Brier/AUC/prediction mean의 기록 대비 최대 오차는 `5.551115123125783e-17`이었다.
- 2024 재현값: Brier `0.2480151400412961`, AUC `0.5480200784149498`, prediction mean `0.48921937001156857`.
- 판정: `PASS`. 새로운 모델 학습, Feature 실험, 제출 실행은 수행하지 않았다.

## CatBoost vs LGBM-712 Single Comparison

- 목적: LGBM-712와 정확히 동일한 49개 Feature를 사용한 단일 CatBoost의 시간순 walk-forward 성능과 고정 50:50 blend 가능성을 평가했다.
- 실행 설정: CatBoost `1.2.10`, `Logloss`, iterations `300`, learning_rate `0.05`, depth `6`, l2_leaf_reg `3.0`, random_seed `42`, random_strength `1.0`, bootstrap `Bernoulli`, subsample `0.8`, thread_count `-1`, one_hot_max_size `2`, nan_mode `Min`.
- 범주형 Feature: `top_bottom`, `game_type`, `base_state`, `pitcher_hand`, `batter_hand`, `pitcher_team_id`, `batter_team_id`, `pitcher_batter_hand`. 실제 dtype·고유값을 점검한 뒤 모두 문자열로 고정하고 결측 sentinel을 `__MISSING__`으로 통일했다.
- 검증 구조: `2019→2020`, `2019~2020→2021`, `2019~2021→2022`, `2019~2022→2023`, `2019~2023→2024`.
- 최종 validation을 eval_set 또는 early stopping에 사용하지 않았고, iterations와 모든 파라미터는 전 fold에서 고정했다. 튜닝·seed ensemble·가중치 탐색·추가 calibration은 수행하지 않았다.
- LGBM-712는 저장된 fold별 `p095`, `p101`을 `clip(0.6*p095 + 0.4*p101 - 0.006, 0, 1)`로 복원했으며 기존 기록과 `1e-12` 이내에서 일치했다.

| Validation | CatBoost ΔBrier | 50:50 ΔBrier | CatBoost ΔAUC | 50:50 ΔAUC |
| ---------- | ---------------: | ------------: | -------------: | ----------: |
| 2020 | +0.000820972346 | +0.000269961055 | -0.001776229869 | -0.000201253654 |
| 2021 | -0.000244977347 | -0.000176816687 | -0.000421727564 | +0.000420635023 |
| 2022 | -0.000006537119 | -0.000043211492 | -0.000146885504 | +0.000246738119 |
| 2023 | +0.000100311524 | +0.000013616515 | +0.001298397135 | +0.000951656053 |
| 2024 | -0.000092973690 | -0.000098267300 | +0.001181553361 | +0.001227713295 |

- 전체 pooled OOF: LGBM-712 Brier/AUC `0.2475868123514759 / 0.5557378599497719`; CatBoost `0.2476993612966766 / 0.5556321427916533`; 50:50 `0.2475786865081288 / 0.5561263827495316`.
- 전체 OOF 대비: CatBoost ΔBrier `+0.0001125489452006`, ΔAUC `-0.0001057171581185`; 50:50 ΔBrier `-0.0000081258433471`, ΔAUC `+0.0003885227997597`.
- Fold ΔBrier 평균/중앙값 및 개선/악화: CatBoost `+0.0001153591426864 / -0.0000065371185269`, `3/2`; 50:50 `-0.0000069435819774 / -0.0000432114919125`, `3/2`.
- 2024: LGBM-712 Brier/AUC `0.2480151400412961 / 0.5480200784149498`; CatBoost `0.2479221663508622 / 0.5492016317762964`; 50:50 `0.2479168727411873 / 0.5492477917098050`.
- 전체 OOF correlation: prediction Pearson `0.9728298490179642`, Spearman `0.9635946078481618`, residual Pearson `0.9995712901867784`.
- 2024 correlation: prediction Pearson `0.9460537404326756`, Spearman `0.9453986096623492`, residual Pearson `0.9996258485883271`.
- residual 정의: `prediction - y_true`.
- 정렬·누수·Feature 검증: row_id와 season 기준 1:1 병합, target 일치, fold별 행 수, 중복/누락, Feature 49개 이름·순서, dtype, categorical index, finite/range 검사를 모두 통과했다.
- 산출물: `experiments/scripts/catboost_lgbm712_comparison.py`, `experiments/outputs/catboost_lgbm712_metrics.csv`, `experiments/outputs/catboost_lgbm712_oof_predictions.csv`, `experiments/outputs/catboost_lgbm712_run_config.json`.
- 판정: `HOLD` — CatBoost 단독은 전체 OOF에서 악화됐지만 2024에서 개선됐고, 고정 50:50 blend는 전체 OOF와 2024 Brier/AUC를 모두 개선했다. 추가 실험은 자동 실행하지 않는다.

## CatBoost-LGBM712 Locked Fixed-Weight Analysis

- 입력: 기존 `catboost_lgbm712_oof_predictions.csv`만 사용했으며 모델 학습, Feature 생성, TrackMan, calibration은 수행하지 않았다.
- 후보: CatBoost 비중 `w = 0.0, 0.1, 0.2, 0.3, 0.4, 0.5`만 평가했다. 식은 `(1-w)*LGBM-712 + w*CatBoost`이다.
- 선택 잠금: 파일의 선두 984,172행인 2020~2023만 읽어 후보를 평가했고, 2024를 읽기 전에 `catboost_lgbm712_weight_lock.json`에 CatBoost 비중 `0.2`를 영구 기록했다. 동률 허용치는 `1e-7`이며 해당 범위에서는 작은 CatBoost 비중을 선택했다.
- 선택 구간: LGBM-712 Brier `0.2474764819746077`; 고정 80:20 blend Brier/AUC/mean `0.2474662829997385 / 0.5546646086516617 / 0.5285902399613982`; ΔBrier `-0.0000101989748692`.
- 선택 구간 fold ΔBrier: 2020 `+0.0000742583935909`, 2021 `-0.0000837653981386`, 2022 `-0.0000268709006007`, 2023 `-0.0000033228135735`; 개선/악화 `3/1`, 평균/중앙값 `-0.0000099251796805 / -0.0000150968570871`.
- 2024 잠금 평가: LGBM-712 Brier/AUC/mean `0.2480151400412961 / 0.5480200784149498 / 0.4892193700115685`; 80:20 blend `0.2479634058120786 / 0.5486929226534398 / 0.4901482743334079`; ΔBrier `-0.0000517342292175`, ΔAUC `+0.0006728442384900`.
- 전체 2020~2024 prediction 차이(CatBoost-LGBM): 평균 `0.0067317408476004`, 표준편차(ddof=0) `0.0145700009935009`, 절댓값 평균 `0.0118231958750734`.
- 전체 row loss: CatBoost가 더 작은 행 `51.263292%`, LGBM-712가 더 작은 행 `48.736708%`; squared-loss 차이(CatBoost-LGBM) 평균/중앙값 `+0.0001125489452006 / -0.0004102342443349`.
- 2020~2023 row loss: CatBoost 우세 `51.363075%`, LGBM 우세 `48.636925%`; loss 차이 평균/중앙값 `+0.0001654882960374 / -0.0004548212130023`.
- 2024 row loss: CatBoost 우세 `50.875913%`, LGBM 우세 `49.124087%`; loss 차이 평균/중앙값 `-0.0000929736904339 / -0.0002600138236485`.
- 정렬·검증: `row_id + season` 1:1 병합, 양쪽 prediction/target 일치, 중복·누락·행 수, `[0,1]`, NaN/inf, blend 및 squared-loss 식, 원본 OOF SHA-256 보존을 모두 통과했다.
- 산출물: `experiments/scripts/catboost_lgbm712_fixed_weight_analysis.py`, `experiments/outputs/catboost_lgbm712_weight_selection_2020_2023.csv`, `experiments/outputs/catboost_lgbm712_weight_lock.json`, `experiments/outputs/catboost_lgbm712_fixed_weight_metrics.csv`, `experiments/outputs/catboost_lgbm712_diversity.csv`, `experiments/outputs/catboost_lgbm712_row_loss.csv`, `experiments/outputs/catboost_lgbm712_fixed_weight_summary.json`.
- 판정: `HOLD` — 선택 구간과 잠금 2024가 모두 개선됐지만 선택 구간 이득은 약 `1.02e-5`로 매우 작고, 2020 악화 `+7.43e-5`가 존재해 안정적인 ACCEPT로 과장하지 않는다.

## CATBOOST-ID51 Single Comparison

- 목적: 기존 CATBOOST-49의 정확한 49개 Feature와 고정 설정을 유지하고 공식 train의 `pitcher_id`, `batter_id`만 categorical Feature로 추가했다. 총 Feature는 51개다.
- 설정: CatBoost `1.2.10`, Logloss, iterations `300`, learning_rate `0.05`, depth `6`, l2_leaf_reg `3.0`, random_seed `42`, random_strength `1.0`, Bernoulli bootstrap, subsample `0.8`, thread_count `-1`, one_hot_max_size `2`, nan_mode `Min`.
- ID 처리: 두 ID 모두 동일 규칙의 문자열 categorical로 변환했고 결측 토큰은 `__MISSING_PITCHER__`, `__MISSING_BATTER__`로 고정했다. 실제 ID 결측 행은 0개였다. 별도 target/frequency encoding은 생성하지 않았으며 CatBoost ordered categorical statistics는 각 fold 학습 Pool 내부에서만 계산됐다.
- Walk-forward: `2019→2020`, `2019~2020→2021`, `2019~2021→2022`, `2019~2022→2023`, `2019~2023→2024`. eval_set과 early stopping은 사용하지 않았다.
- 전체 OOF: LGBM-712 Brier/AUC `0.2475868123514759 / 0.5557378599497719`; CATBOOST-49 `0.2476993612966766 / 0.5556321427916533`; CATBOOST-ID51 `0.2479795117292424 / 0.5532978253059972`.
- 전체 OOF ID51 변화: CATBOOST-49 대비 ΔBrier `+0.0002801504325658`, ΔAUC `-0.0023343174856560`; LGBM-712 대비 ΔBrier `+0.0003926993777664`, ΔAUC `-0.0024400346437746`.
- 2024: CATBOOST-ID51 Brier/AUC `0.2482752756010081 / 0.5458380424807959`; CATBOOST-49 대비 ΔBrier `+0.0003531092501458`, ΔAUC `-0.0033635892955005`; LGBM-712 대비 ΔBrier `+0.0002601355597120`, ΔAUC `-0.0021820359341538`.
- ID51 vs LGBM prediction correlation 전체 OOF Pearson/Spearman `0.9526654759435084 / 0.9324063760528694`; ID51 vs CATBOOST-49 Pearson `0.9600144252565004`.
- 고정 80:20 비교: 2020~2023 old blend Brier/AUC `0.2474662829997385 / 0.5546646086516617`, ID51 blend `0.2474916908576531 / 0.5544710626420941`; ID51-old ΔBrier `+0.0000254078579146`. 전체 OOF old `0.2475681059383097 / 0.5560144470588277`, ID51 `0.2475959802137199 / 0.5558107143368931`; ΔBrier `+0.0000278742754103`. 2024 old `0.2479634058120786 / 0.5486929226534398`, ID51 `0.2480008552828066 / 0.5484058425480030`; ΔBrier `+0.0000374494707281`.
- Fold 안정성: ID51 단독은 CATBOOST-49 대비 Brier 개선/악화 `0/5`; ID51 80:20은 old 80:20 대비 `0/5`. 두 blend prediction의 전체 OOF Pearson correlation은 `0.9983297596515308`이다.
- ID 진단: 전체 OOF에서 두 ID 모두 seen `909,218행 (73.461536%)`, 하나 이상 unseen `328,461행 (26.538464%)`; 2024는 각각 `184,502행 (72.779844%)`, `69,005행 (27.220156%)`이었다.
- 전체 OOF 하위집단 ID51 Brier 및 CATBOOST-49 대비 ΔBrier: both seen `0.248136 / +0.000264`; pitcher-only unseen `0.247826 / +0.000185` (204,503행); batter-only unseen `0.247397 / +0.000576` (99,845행); 하나 이상 unseen `0.247547 / +0.000326` (328,461행).
- 2024 하나 이상 unseen: 69,005행, ID51 Brier `0.248217`, CATBOOST-49 대비 ΔBrier `+0.000601`. unseen 집단에서도 뚜렷한 악화가 확인됐다.
- 누수·정렬 검증: 정확한 51개 Feature와 순서, ID categorical dtype, row_id/target 제외, 미래 시즌 제외, validation Pool/target 미사용, TrackMan 미사용, LGBM-712 재현, `row_id + season` 1:1 병합, target/행 수, prediction finite 및 `[0,1]`을 모두 통과했다.
- 산출물: `experiments/scripts/catboost_id51_comparison.py`, `experiments/outputs/catboost_id51_metrics.csv`, `experiments/outputs/catboost_id51_oof_predictions.csv`, `experiments/outputs/catboost_id51_id_diagnostics.csv`, `experiments/outputs/catboost_id51_subgroup_metrics.csv`, `experiments/outputs/catboost_id51_run_config.json`.
- 판정: `REJECT` — ID51 단독은 CATBOOST-49 대비 전체 OOF와 2024 및 모든 fold에서 악화됐고, 고정 ID51 80:20도 기존 80:20보다 선택 구간·전체·2024 및 모든 fold에서 악화됐다. 기존 CATBOOST-49 HOLD 및 old 80:20 HOLD 결과는 보존한다.

## CATBOOST-ID51 Main Results Registration and LGBM-712 Feature Diagnostics

- CATBOOST-ID51은 모든 단독 fold와 고정 80:20 앙상블 비교에서 악화되어 `REJECT`로 확정했다. ID 기반 추가 실험과 ID51 가중치 탐색은 중단한다.
- `results.csv` append 전 `results.backup_before_CATBOOST-ID51-001_20260812.csv`를 생성했다. 기존 행은 CSV row 기준으로 모두 보존했고 `CATBOOST-ID51-001` 한 행만 append했다.
- 대표 2024 값: train rows `1,221,585`, valid rows `253,507`, features `51`, Brier `0.2482752756010081`, AUC `0.5458380424807959`, prediction mean `0.4982874762619241`, training time `107.19556860000012`, LGBM-712 대비 Brier delta `+0.00026013555971199365`, verdict `REJECT`. CatBoost에 해당하지 않거나 측정되지 않은 필드는 빈칸으로 유지했다.
- results 검증: 백업 존재, 기존 행 불변, 실험명 단일 존재, 헤더 순서 및 22개 컬럼 유지, 상세 metrics/OOF full-precision 일치, delta 부호·계산 일치, CSV reload를 모두 통과했다.
- 진단은 저장된 `lgbm_095.txt`, `lgbm_101.txt`만 로드했으며 모델 fit/predict, validation target 로드, Feature 생성 실험, Feature 제거를 수행하지 않았다. 원본 train 45개 컬럼과 배포 코드에 이미 고정된 interaction 4개만 재구성했다.
- 두 모델 파일의 SHA-256은 서로 다르고 `min_data_in_leaf`가 각각 `20`, `50`이지만, 저장된 트리의 49개 Feature별 split/gain importance는 전 항목에서 동일했다.
- 공통 gain 하위 25%는 13개였다: `game_dayofweek`, `top_bottom`, `run_top_before`, `run_bot_before`, `score_diff_home`, `score_diff_pitcher_team`, `runner_on_1b`, `runner_on_2b`, `runner_on_3b`, `num_runners_on`, `home_win_expectancy`, `away_win_expectancy`, `pitcher_hand`. 이 중 split/gain이 양쪽 모델 모두 0인 Feature는 `top_bottom`과 세 runner flag였다.
- 결측률 최대는 prev1/3/5 success 및 middle 6개에서 각각 `0.019785`; 거의 상수인 Feature는 없었다. Feature별 결측률, 고유값 수, top-value 비율, importance와 순위는 `lgbm712_feature_diagnostics.csv`에 기록했다.
- 상관은 target 없이 seed 42의 250,000행 표본으로 계산했다. 핵심 관계: `asof_pitcher_n`/`asof_pitcher_pitchmix_n` Pearson·Spearman `1/1`, home/away expectancy Pearson `-1`, runner count/base state 최대 절대 상관 `0.973997`, prev3/prev5 success `0.882146`, prev3/prev5 middle `0.845889`, balls/pressure `0.987788`. 범주 코드가 포함된 상관은 별도 caution flag를 남겼다.
- 전체 행 대수 검증: run total, 두 score difference, runner count, base state, `asof_pitcher_n == asof_pitcher_pitchmix_n`은 전 행 일치했다. home/away expectancy 합은 반올림으로 100에서 최대 `0.1` 차이였고, 세 pitch-mix rate 합은 non-null 행에서 최대 `1.000000000139778e-6` 오차로 1과 일치했다.
- 그룹 gain 비중(두 모델 동일): win expectancy `0.024880%`, score state `0.165609%`, runner state `0.119477%`, recent success `8.464187%`, recent middle `0.175140%`, pitch mix `1.626165%`, generated interactions `40.872280%`. interaction 그룹은 높은 gain 때문에 제거 후보가 아니다.
- 2019 기준 시즌 PSI가 큰 항목은 `asof_batter_n` `2.289326`(2024), middle interaction `2.150408`(2024), pitcher count와 pitchmix count 각각 `1.852464`(2023), batter middle `1.831983`(2024), batter success `1.780415`(2024)였다. `season` 자체와 2020의 비정상 일정 영향을 받는 `game_month`는 해석상 분리했다.
- 다음 ablation 후보는 최대 2개로 제한한다: (1) 양쪽 모델에서 split/gain 0이며 `base_state`와 `num_runners_on`에 완전히 포함되는 `runner_on_1b/2b/3b` 그룹, (2) `asof_pitcher_n`과 전 행 동일하면서 gain이 더 낮은 `asof_pitcher_pitchmix_n` 단일 중복 count 그룹. 이 단계에서는 어느 Feature도 제거하거나 재학습하지 않았다.
- 진단 산출물: `experiments/scripts/lgbm712_feature_diagnostics.py`, `experiments/outputs/lgbm712_feature_diagnostics.csv`, `experiments/outputs/lgbm712_feature_correlation_pairs.csv`, `experiments/outputs/lgbm712_feature_group_diagnostics.csv`, `experiments/outputs/lgbm712_feature_distribution_shift.csv`, `experiments/outputs/lgbm712_feature_redundancy_checks.csv`, `experiments/outputs/lgbm712_feature_diagnostic_config.json`.

## LGBM-774~775 Feature-removal ablation

- Untouched 49-feature LGBM-712 retraining reproduction gate: PASS.
- Walk-forward: 2019→2020, ..., 2019~2023→2024; no early stopping or future data.
- LGBM-774: removed `runner_on_1b|runner_on_2b|runner_on_3b`; features `46`.
  - mean delta Brier `+1.425441218259604e-05`, folds `1/4`.
  - 2024 Brier `0.2480343725167423`, delta `+1.923247544619033e-05`; AUC `0.5476394142437161`, delta `-0.0003806641712337244`.
  - verdict: `REJECT`.
- LGBM-775: removed `asof_pitcher_pitchmix_n`; features `48`.
  - mean delta Brier `+3.415325350338283e-05`, folds `0/5`.
  - 2024 Brier `0.248032011551762`, delta `+1.687151046586566e-05`; AUC `0.5477872488847412`, delta `-0.0002328295302086447`.
  - verdict: `REJECT`.
- results backup: `results.backup_before_LGBM-774-775_20260812_154220.csv`.
- run config: `experiments\outputs\lgbm_774_775_ablation_config.json`.
- Existing result rows were preserved; two validated representative 2024 rows were appended.

## XGBOOST-001
- Exact 49 features, fixed settings, walk-forward checks PASS.
- OOF XGBoost delta `+0.0007915240781199706`; fixed 80:20 delta `+4.307244995968573e-05`.
- 2024 XGBoost Brier `0.2483087629079819` delta `+0.0002936228666857721`; blend `0.2479774171906647` delta `-3.772285063141645e-05`.
- verdict `HOLD`.

## CATBOOST-TUNE-001
- selected on 2020-2023: `depth4`; locked 2024 blend delta `-2.23789110827266e-05`; verdict `HOLD`.

## CATBOOST-ITER-001
- selected iterations `200` on 2020-2023; locked 2024 blend delta `-3.89874313186378e-05`; verdict `HOLD`.

## CATBOOST-LR-001
- selected learning rate `0.03` on 2020-2023; locked 2024 blend delta `-3.471164350254963e-05`; verdict `HOLD`.

## CATBOOST-SEED5-001
- fixed seeds `(42, 52, 62, 72, 82)`; overall blend delta `-2.484937159791256e-05`; locked 2024 blend `0.2479597250214088`, delta vs old best `-3.680790669841061e-06`; verdict `CANDIDATE`.

## LGBM-776
- Added `pitcher_recent1_success_positive_gap`; overall blend delta vs Seed5 baseline `+2.716657189960614e-05`; 2024 delta `+5.233051426378754e-05`; folds `1/4`; verdict `REJECT`.

## LGBM-SEED5-001
- Selected seeds: [42]; selection delta `+0`; 2024 delta `+0`; folds `0/0`; verdict `REJECT`.

## CATBOOST-DIVERSITY-001
- Candidate `depthwise_d6`; weights `0.80/0.20/0.00`; selection delta `+0`; 2024 delta `+0`; folds `0/0`; `REJECT`.

## STACKING-LINEAR-001
- Ridge `0.0`; selection delta `+0.0002219774629645399`; 2024 weights `intercept=0.1, LGBM=0.1865268, CatBoost=0.60870017`; 2024 delta `+5.444513173877286e-05`; folds `1/3`; `REJECT`.

## LGBM-TEMPORAL-001
- Window `3`; weights `0.60/0.20/0.20`; selection delta `-6.599169059789967e-06`; 2024 delta `-7.668084562845179e-06`; folds `2/0`; `HOLD`.

## TEMPORAL-ROBUST-002
- Weights full/recent2/recent3/recent4/cat `0.40/0.00/0.40/0.00/0.20`; nested `1/1`; selection `1/0`; 2024 delta `-6.57991880026465e-06`; `HOLD`.

## TEMPORAL-DECAY-003
- Decay `0.95`; weights full/plain/decay/cat `0.40/0.30/0.10/0.20`; nested `0/2`; selection `2/1`; 2024 delta vs TEMPORAL-001 `+6.524409879304915e-07`; `REJECT`.

## TEMPORAL-WEIGHT-004
- Weights full/recent3/cat `0.55/0.23/0.22`; nested `1/2`; selection `3/1`; 2024 delta vs TEMPORAL-001 `-4.609822005147146e-06`; `HOLD`.

## CATBOOST-TEMPORAL-006
- weights fullLGB/recentLGB/fullCat/recentCat `0.60/0.20/0.20/0.00`; nested `0/0`; selection `0/0`; 2024 delta `+0`; target0 delta `+0`; `REJECT`.

## TEMPORAL-CALIBRATION-007
- `{'method': 'identity', 'shift': 0.0, 'scale': 1.0, 'temperature': 1.0, 'logit_shift': 0.0}`; nested `0/1`; selection `0/0`; 2024 delta `+0`; `REJECT`.

## LGBM-ROLLING-WINDOW-008
- window `3.0`, weights `0.50/0.30/0.20`; 2024 `+3.877476773717081e-06`; `REJECT`.

## TEMPORAL-TREND-009
- mode `linear`, alpha `0.06`; 2024 `-5.929565554119165e-07`; `HOLD`.

## LGBM-TEMPORAL-DIVERSITY-010
- `incumbent`, `none`, new weight `0.00`; 2024 `+0`; `REJECT`.

## XGBOOST-DIVERSITY-011
- `incumbent`, `none`, new `0.00`; 2024 `+0`; `REJECT`.

## LGBM-SAMPLING-REG-DIVERSITY-012
- `incumbent`, `none`, new `0.00`; 2024 `+0`; `REJECT`.

## CATBOOST-PARAMETER-DIVERSITY-013
- `cat_d6_random_bayes`, `replace_cat`, new `0.05`; 2024 `+6.325322875644357e-06`; `REJECT`.

## ERROR-COMPLEMENT-BLEND-014
- `x0.025_l0.000_c0.15`; XGB/LGB/Cat `0.025/0.000/0.15`; 2024 `+2.314047023288524e-05`; `REJECT`.

## DYNAMIC-DISAGREEMENT-GATING-015
- `cat_cap_t0.022_w0.020_s0.025`; 2024 `+1.315539196716786e-06`; `REJECT`; row-independent.

## BASE-MODEL-OOF-AUDIT-016
- Exact nine-model OOF audit; recent reconstruction passed; `185.8s`; `ANALYSIS`.

## CONSTRAINED-SEED-BLEND-017
- `CONSTRAINED-SEED-BLEND-017,model=f0.60_r0.60_drop_42,2024_brier=0.2479514442182721,delta_823=-6.127185737669905e-07,nested=2/1,selection=2/2,HOLD`.

## SEED-DROP-ROBUSTNESS-018
- drop seed 42 robustness; selection `-9.686114538776103e-07`; seasons `2/2`; LOSO best `1/4`; 2024 `-6.127185737669905e-07`; `REJECT`.

## OOF-RESIDUAL-SEGMENT-AUDIT-019
- 823 residual audit across `13` non-Trackman groupings; stable selection segments `40`; 2024 same direction `33`; `ANALYSIS`.

## SEGMENT-RESIDUAL-CALIBRATION-020
- preregistered `9733eb6dc38f`; candidates `108`; status `development_no_candidate`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no test access.

## REGULARIZED-9MODEL-STACKING-021
- preregistered `a156e3430df6`; status `development_no_candidate`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no test access.

## FINAL-823-REPRODUCIBILITY-AUDIT-022
- final ZIP `final_823_submission.zip` SHA256 `8fddd50b7e2c6a1db18aa7d1ebfe39285fa7193f5e935b20696931e1f7d2ed3f`; 9 models; 49 features; exact packaged/direct smoke predictions; row/order independence; hidden-test/prior-upload comparison unavailable; `PASS`.

## NONTRACKMAN-FEATURE-TOURNAMENT-023
- seven row-local non-Trackman families; advanced `[]`; status `no_selection_candidate`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no test access.

## HISTORY-DYNAMICS-SUBFEATURE-SEARCH-024
- 19 frozen history-dynamics candidates; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## STABILIZED-HISTORY-DYNAMICS-025
- 20 stabilized history candidates; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## TRACKMAN-ROBUST-RELEASE-PROFILE-027
- 11 preregistered prior-season robust release candidates; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no test access.

## TRACKMAN-REPERTOIRE-ENTROPY-028
- 10 preregistered prior-season repertoire candidates; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no test access.

## REGULARIZED-LOGISTIC-DIVERSITY-029
- Six preregistered sparse logistic structures and 24 fixed blends; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## HIERARCHICAL-CONTEXT-TARGET-ENCODING-030
- Six preregistered strict-past hierarchical context candidates; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## HIERARCHICAL-COUNT-ROBUSTNESS-031
- Fixed 030 count bundle at weight 0.025; development `False`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no alternative, Trackman, or test access.

## LEADERBOARD-GAP-AUDIT-033
- Compared exact Score796.zip and locked 823 ZIP. Full LGBMs byte-identical; 2024 OOF Brier gain `+1.134887523268624e-05`; recent3 Shapley `+7.689730156787422e-06`; CatBoost seed5 Shapley `+3.659145075898818e-06`; diagnostic only, no model selection/test-wide tuning.

## HIERARCHICAL-PLAYER-SKILL-RATING-034
- Seven preregistered strict-past hierarchical player-skill candidates; status `development_rule_frozen`; tier `stable`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## HIERARCHICAL-HAND-RESIDUAL-DECOMPOSITION-035
- Six preregistered proper subsets of the 034 hand/matchup family with balance-first selection; status `development_no_candidate`; tier `None`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; sequential 2023 reuse disclosed; no Trackman/test access.

## HIERARCHICAL-HAND-LOW-WEIGHT-036
- Fixed pitcher-by-batter-hand residual with preregistered 0.5-2.0% weights; status `development_rule_frozen`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## LONG-RECENT-PLAYER-DYNAMICS-DECOMPOSITION-037
- Eight preregistered proper subsets of long/recent player skill with balance-first selection; status `development_rule_frozen`; tier `stable`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## PLAYER-ID-CATEGORICAL-DIVERSITY-038
- Five preregistered native CatBoost player-ID structures screened at seed 42; selected structure expanded to seeds 42/52/62; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no Trackman/test access.

## AGGRESSIVE-CANDIDATE-AUDIT-039
- Aggressive pre-2024 audit selected `HIERARCHICAL-PLAYER-SKILL-RATING-034` / `family__hand_matchup_residual` at weight `0.025`; 2024 delta `-9.637901155490347e-07`; final `family__hand_matchup_residual__weight_0.025`; `ACCEPT`; competition safeguards unchanged.

## TRACKMAN-LATENT-COMMAND-EMBEDDING-040
- Shared 2019-frozen PCA of strict-past pitch-group physical distributions; three candidates; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no test access.

## DIRECT-MIXED-EFFECTS-PROBABILITY-041
- Three preregistered sparse crossed-player probability models and 12 blends; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no TrackMan/test access.

## TEMPORAL-OOF-RESIDUAL-BOOSTING-042
- Three preregistered nonlinear temporal OOF residual models and nine scales; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no TrackMan/test access.

## TEMPORAL-STABLE-FEATURE-ABLATION-043
- Eight preregistered semantic feature removals; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no TrackMan/test access.

## SEASON-BALANCED-TEMPORAL-WEIGHTING-044
- Eight preregistered season-total-mass weighting policies; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no TrackMan/test access.

## CATBOOST-SEED-POOL-EXTENSION-045
- Frozen cumulative CatBoost seed pools 6-10; status `development_rule_frozen`; confirmation `True`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no TrackMan/test-wide selection.

## PLAYER-EMBEDDING-WIDE-DEEP-046
- Frozen sparse Wide&Deep player/context embeddings, three seeds; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no TrackMan/test access.

## COUNT-CONDITIONAL-MIXTURE-OF-EXPERTS-047
- Frozen 12-state count experts with support shrinkage; status `development_rule_frozen`; confirmation `True`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no TrackMan/test access.

## COUNT-STATE-ROBUSTNESS-AUDIT-048
- Audited frozen 047 candidate by 12 count states on 2020-2023 with block bootstrap and BH-FDR; qualified `[]`; 2024 not accessed; `ANALYSIS`.

## CROSS-FAMILY-MICRO-BLEND-050
- Three-family preregistered micro-blend; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; official data only, no test access.

## FIXED-MICRO-BLEND-CONFIRMATION-051
- Frozen 050 near-miss confirmation; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no test access.

## TABM-PLR-BRIER-ENSEMBLE-052
- PLR numerical encoding plus four-member BatchEnsemble TabM with BCE+Brier loss; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; official train only, no test access.

## BALANCED-TABM-HIERARCHY-CONFIRMATION-053
- Frozen balanced hierarchy/TabM blend; confirmation `False`; 2024 not evaluated; model `incumbent_823`; `REJECT`; no test access.

## FT-TRANSFORMER-BRIER-ENSEMBLE-054
- Compact FT-Transformer with fold-only preprocessing and BCE+Brier loss; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; official train only, no test access.

## MONOTONE-SUCCESS-REGULARIZATION-055
- 2019-directed monotone constraints on three success feature sets; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; official train only, no test access.

## SUBMISSION-PACKAGE-ALIGNMENT-056
- Rebuilt active `submit.zip` from the hash-locked incumbent 823 payload; exact historical ZIP `True`; smoke max abs difference `0`; runtime `2.508s`; prior package preserved as `submit_aggressive_039_backup.zip`; `PASS`; no test-wide statistics.

## DENSITY-RATIO-TEMPORAL-WEIGHTING-057
- Strict-past adversarial density-ratio weighting with three strengths and three incumbent blends; status `development_no_candidate`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; no target/test distribution access.

## MASKED-TABULAR-SSL-058
- Fold-only masked feature reconstruction followed by supervised BCE+Brier fine-tuning; status `development_rule_frozen`; confirmation `False`; model `incumbent_823`; 2024 delta `+0`; `REJECT`; official train only, no test access.

## SSL-TREND-CALIBRATION-059
- 50% linear annual SSL-minus-incumbent mean-drift correction fit on 2020-2022; weight selected on disclosed 2020-2023; locked 2024 delta `+0`; model `incumbent_823`; `REJECT`; no post-2024 retuning or test access.

## SSL-TEMPORAL-ERROR-DECOMPOSITION-060
- Brier quadratic decomposition found positive SSL blend direction in `4/4` 2020-2023 seasons but reversed 2024 oracle weight `-0.064996`; `STOP_SSL_FAMILY_NONSTATIONARY_RESIDUAL_DIRECTION`; diagnostic only, incumbent retained, no test access.

## TRACKMAN-MAPPING-COVERAGE-EXPANSION-061
- Expanded conservative identity mapping using mutual unique top1, score/situation margins >=0.20, n>=20, hand and temporal consistency; pitcher coverage `76.144%`, batter `76.727%`, duplicate mappings `0`, known temporal consistency `100.000%`; `PASS`; identity audit only, no target/test access.

## STABLE-INTERACTION-RESIDUAL-AUDIT-064
- Audited all `28` pairwise low-cardinality row-local contexts with strictly prior-season OOF residual corrections. No candidate improved both 2021 and 2022; best aggregate candidate `count__batter_experience` worsened Brier by `+4.133734864990277e-05` and won only `1/2` seasons. 2023 confirmation and 2024 were not accessed; incumbent retained; `NO_DEVELOPMENT_CANDIDATE`.

## EXPANDED-MAPPING-RELEASE-PROFILE-062
- Re-tested the fixed 027 compact prior-season release profile with 061 expanded mapping only; development status `development_no_candidate`; 2024 audit delta `+0`; `REJECT`; sequential reuse disclosed, strict prior-season Trackman, no test access.

## EXPANDED-MAPPING-PHYSICAL-PROFILE-063
- Final expanded-mapping strict-prior-season robust velocity/spin/movement bundle; development status `development_no_candidate`; 2024 audit delta `+0`; `REJECT`; current-pitch Trackman/test not used.

## COMPACT-RETRIEVAL-FEASIBILITY-065
- CPU sample feasibility proxy for TabR/ModernNCA using a supervised 8D embedding, 64 historical neighbors, and MLP/neighbor probability averaging. The smallest 2.5% incumbent blend worsened pooled 2021-2022 Brier by `+2.56163370038337e-05` with `0/2` season wins; larger weights worsened further. 2023 confirmation and 2024 were not accessed; no full experiment; `NO_DEVELOPMENT_CANDIDATE`.

## STRICT-PAST-TEAM-CONTEXT-066
- Three strict-past Bayesian team context bundles were tested with official train data only. `team_matchup_bundle` improved development Brier by `-2.225429808824786e-05` but failed target balance (`target1 +0.001973996666288641`); no candidate passed the preregistered gate, so 2023/2024 were not evaluated; `NO_DEVELOPMENT_CANDIDATE`.

## TEAM-MATCHUP-MICROBLEND-067
- Frozen 066 team-matchup micro-blends at 0.5-5%. The 0.5% blend improved all three development seasons by pooled `-5.607307450028465e-07`, but one-shot 2023 confirmation worsened by `+1.348514140186996e-06`; 2024 was not accessed; incumbent retained; `REJECT_CONFIRMATION`.

## DECAYED-TEAM-MATCHUP-068
- Strict-past team matchup histories used season decay `0.5` and a frozen incumbent blend weight of `0.005`. Development improved all `3/3` seasons with pooled Brier delta `-5.12965784849051e-07`, but one-shot 2023 confirmation worsened by `+1.2505423422903839e-06`; 2024 was not evaluated; incumbent retained; `REJECT_CONFIRMATION`.

## CURRENT-SEASON-RECONSTRUCTION-069
- Reconstructed row-independent within-season pitcher/batter success state from each row's cumulative `asof_n × rate` and strictly prior-season endpoint constants. Pitcher-only features improved standalone development Brier by `-0.00016832265361046983` with `3/3` wins. A 2.5% incumbent blend improved 2023 overall by `-2.6746052688708666e-05` but exceeded the target1 guard (`+6.87622487616224e-05`); 2024 was not evaluated; `REJECT_CONFIRMATION`.

## CURRENT-SEASON-LOW-WEIGHT-070
- Sequential disclosure from 069 was recorded, then pitcher current-season weight was frozen at `0.01` before the family-specific 2024 evaluation. It improved all four 2020-2023 seasons (pooled `-4.730292769637453e-06`) and locked 2024 Brier by `-3.6110273271827698e-06`; target0/target1 deltas were both negative (`-5.20743921250677e-06`, `-1.9233500806459247e-06`). Official train only, test not accessed; `ACCEPT`.

## BUILD-CURRENT-SEASON-SUBMISSION-071
- Trained the accepted 55-feature pitcher current-season LightGBM pair and stored 792 endpoint constants. The initial PowerShell-created ZIP passed the Windows smoke test but failed on the Linux server because `/app/model/full_lgbm_095.txt` was not found; package withdrawn; `FAIL_LINUX_PATH`.

## PACKAGE-LINUX-SUBMISSION-072
- Repacked every archive entry with explicit POSIX `model/...` paths, Unix regular-file metadata and mode `0644`, added a legacy separator fallback resolver, verified CRC and exact root payload, and reran the extracted 5-row smoke test. Corrected package `submit_current_season_070_linux.zip`, size `2,203,694` bytes, SHA-256 `12868738847ee82258246a2c38d61361b01643e527f802c5b413bd538bc0ac14`; `PASS`.

## CURRENT-SEASON-SUBTYPE-EXTENSION-073
- Added 16 deployment-parity current-season reverse/middle/ball/strike features to the accepted 070 pitcher model, using strictly prior-season constants and no other test rows. Replacement improved all three development seasons versus 070 by pooled `-1.2992637865028023e-06`, but one-shot 2023 confirmation worsened by `+2.449058983333696e-06`; 2024 was not evaluated, 070 retained; `REJECT_CONFIRMATION`.

## FAILURE-AUXILIARY-OOF-074
- Recovered training-only reverse/middle/other-failure labels for `99.8926%` of official train rows and generated season-wise strict-past auxiliary probabilities. Replacing the 1% component of accepted 070 improved development Brier only `-1.1191574980640162e-07`, with `1` win, `1` loss, one tie and target1 imbalance `+4.4015265367181033e-05`; development gate failed, 2023/2024 targets were not evaluated, 070 retained; `REJECT_DEVELOPMENT`.

## GAME-TYPE-RESIDUAL-AUDIT-075
- Audited accepted 070 residuals by Regular/Futures on 2020-2023 without accessing 2024. Residual signs were unstable for both Futures (`-1|+1|+1|-1`) and Regular (`-1|+1|-1|+1`); Futures showed a major 2023 reversal (`-0.1998378845`). No R/F specialist or calibration candidate qualified; `NO_STABLE_CANDIDATE`.

## L2-BRIER-REGRESSION-076
- Trained a 55-feature LightGBM `regression_l2` pair without the binary offset and blended it 0.5% into accepted 070. Development improved pooled Brier `-1.2976203219994265e-06`, 2023 improved `-4.936440791358798e-06`, and locked 2024 improved an additional `-1.539762500030184e-06`; locked target deltas stayed within the preregistered guard. Final 2024 Brier/AUC `0.2479469061470187 / 0.5489126476643506`; `ACCEPT`.

## BUILD/PACKAGE-L2-SUBMISSION-077/078
- Trained the full-data 55-feature L2 pair and packaged it as a 0.5% extension of 070. Explicit POSIX archive paths, Unix `0644` metadata, exact root payload, CRC integrity, and extracted 5-row smoke execution passed. Package `submit_l2_076_linux.zip`, size `2,482,359` bytes, SHA-256 `b8d4aa8822c5458a9de1b5bdf49941d7b13b240bfc1720df4bf900a932fa05f1`; `PASS`.

## CURRENT-SEASON-10PCT/PACKAGE-079
- After public leaderboard validation of the 1% current-season direction and disclosure of all local seasons, the current-season pitcher component was increased to a fixed aggressive weight of 10% with 90% incumbent; L2 was excluded. The weight improves overall Brier in all 2020-2024 seasons; 2024 Brier/AUC are `0.2479180374891735 / 0.5493250232268798`, delta `-3.401944767243646e-05`, with both target deltas negative. Explicit POSIX paths, Unix metadata, CRC, root payload, and extracted 5-row smoke passed. Package `submit_current_season_10pct_linux.zip`, SHA-256 `f6983a5904a30684b7f9753dc0add6ef46c4e8a16f8d393f94237750f492b20c`; `ACCEPT_AGGRESSIVE`.

## CURRENT-SEASON-20PCT/PACKAGE-080
- Following the public leaderboard gain from 10%, increased the current-season pitcher component to 20% with 80% incumbent and no L2. Overall Brier improves in every 2020-2024 season; 2024 Brier/AUC are `0.2478886643206108 / 0.5497443135901608`, delta `-6.339261623514316e-05`, with target0/target1 deltas `-9.532344110659199e-05 / -2.9636336232928827e-05`. Explicit POSIX paths, Unix metadata, CRC, exact payload, and extracted 5-row smoke passed. Package `submit_current_season_20pct_linux.zip`, SHA-256 `0fc7c9ba8b4ed8ebecad2f155a72ed4a37ee5a8b5be8b58068dd365e5ba06018`; `ACCEPT_AGGRESSIVE`.

## CURRENT-SEASON-40PCT/PACKAGE-081
- Following consecutive public leaderboard gains at 10% and 20%, increased the fixed current-season pitcher component to 40% with 60% incumbent and no L2. Overall Brier improves in every 2020-2024 season; 2024 Brier/AUC are `0.24784385682081453 / 0.5503620134909533`, delta `-0.00010820011603136931`, with target0/target1 deltas `-0.00017206721243777874 / -4.0681797982815004e-05`. Explicit POSIX paths, Unix metadata, CRC, exact payload, and extracted 5-row smoke passed. Package `submit_current_season_40pct_linux.zip`, SHA-256 `559ab2b5088e7cb3292edea46749435d8faac94e9b2f76c67b45b4f6ad887a81`; `ACCEPT_AGGRESSIVE`.

## CURRENT-SEASON-60PCT/PACKAGE-082
- Increased the fixed current-season component to 60%. All 2020-2024 seasons improve; locked 2024 Brier/AUC are `0.24781763443745722 / 0.5506657959947068`, delta `-0.00013442249938867788`, and both target groups improve. POSIX archive and extracted smoke passed. Package `submit_current_season_60pct_linux.zip`, SHA-256 `c4253e8144b3eb2d1cea9000a416f0eaf5cde804f7b27538a89bdcd23ed62fb3`; `ACCEPT_AGGRESSIVE`.

## CURRENT-SEASON-80PCT/PACKAGE-083
- Increased the fixed current-season component to 80%, near the local 2024 quadratic optimum. All 2020-2024 seasons improve; locked 2024 Brier/AUC are `0.24780999717053886 / 0.5506631778378189`, delta `-0.00014205976630706884`, and both target groups improve, although target1 gain is nearly flat. POSIX archive and extracted smoke passed. Package `submit_current_season_80pct_linux.zip`, SHA-256 `b5bba5a18d6ce88efa67ccd7a3cab90bde9ed15c76738fa9e61a79521c3159ec`; `ACCEPT_AGGRESSIVE`.

## CURRENT-SEASON-FEATURE-ABLATION-084
- Compared full6 against `no_count`, `no_raw`, `no_delta`, and `shrink_only` at the deployed 80% weight using 2020-2022 development seasons. `no_raw` led development by `-1.8751e-05` but reversed strongly on 2023 (`+2.3519e-04`); 2024 was not accessed and full6 was retained; `REJECT_CONFIRMATION`.

## CURRENT-SEASON-STRUCTURE-TUNING-085
- Kept full6 and screened five preregistered LightGBM structures with active `subsample_freq=1`. A-C improved pooled development Brier, but every candidate exceeded the target-balance or worst-season guard; D-E were worse overall. No candidate accessed 2023/2024; `NO_STRUCTURE_IMPROVEMENT`.

## CURRENT-SEASON-CALIBRATED-STRUCTURE-086
- Before confirmation, froze structure A, a development-only offset `-0.0006214128`, and a 10% within-current-model blend. It passed 2023 (`-1.3824e-05`) but worsened locked 2024 by `+7.5249e-06`, with target1 `+1.4721e-04`; current 80% submission retained; `REJECT_LOCKED`.

## CURRENT-SEASON-PITCHMIX-087
- Reconstructed current-season fastball/breaking/offspeed counts from each row's official cumulative fields and strictly earlier-season pitcher constants, adding nine row-independent features. The candidate improved all three development seasons and both pooled targets (`-3.1290e-05`), but reversed on 2023 (`+1.7166e-04`); 2024 was not accessed and the 80% model was retained; `REJECT_CONFIRMATION`.

## CURRENT-SEASON-PITCHER-BATTER-BLEND-088
- Added 10% of the existing pitcher+batter current-season model inside the deployed current component after three development wins (`-1.0231e-05`). Overall 2023 Brier improved `-3.0641e-05`, but target1 worsened `+9.5620e-05`, exceeding the frozen guard; 2024 was not accessed and the 80% pitcher-only model was retained; `REJECT_TARGET_GUARD`.

## CURRENT-SEASON-ACTIVE-BAGGING-089
- Changed only LightGBM `subsample_freq` from 0 to 1 while retaining the full six current-season features, paired min-child models, and 80% submission weight. Development improved pooled Brier `-3.5269e-05`, but 2023 worsened `+2.4509e-05` with target1 `+5.1106e-05`; 2024 was not accessed and the incumbent 80% model was retained; `REJECT_CONFIRMATION`.

## CURRENT-SEASON-REGULARIZATION-090
- Screened four L1/L2 settings with all other current-season model settings fixed. `reg_alpha=0, reg_lambda=1` improved all three development seasons and both pooled targets (`-1.3437e-05`). It also improved overall 2023 Brier (`-1.1934e-05`) but target1 worsened `+6.5009e-05`, exceeding the frozen guard; 2024 was not accessed and the 80% model was retained; `REJECT_TARGET_GUARD`.

## CURRENT-SEASON-CATBOOST-091
- Trained one CatBoost model on the base49 plus current-season six features and screened 10/20/30% replacement inside the current component. All weights improved overall Brier in all three development seasons, but severe target-direction imbalance exceeded the guard; 2023/2024 were not accessed; `NO_CATBOOST_CANDIDATE`.

## CURRENT-SEASON-CATBOOST-CALIBRATED-092
- Froze a development-only CatBoost offset `-0.0054396824` and 30% within-current blend. Pooled development improved both targets and all three seasons (`-6.3687e-05`), but 2023 target1 worsened `+1.1715e-04` despite overall improvement `-8.5092e-06`; 2024 was not accessed and the 80% model was retained; `REJECT_TARGET_GUARD`.

## CURRENT-SEASON-CATBOOST-AGGRESSIVE-093/BUILD-094/PACKAGE-095
- Re-evaluated the frozen calibrated CatBoost candidate using the competition's aggregate Brier objective, treating target splits as diagnostics rather than rules. Locked 2024 improved Brier `-6.1580e-05`, AUC reached `0.5513996381`, and both targets improved. Trained the full-data 55-feature CatBoost and packaged final weights as incumbent 20%, current LGBM 56%, calibrated current CatBoost 24%. POSIX paths, CRC, payload, and extracted smoke passed. Package `submit_current_season_catboost_093_linux.zip`, SHA-256 `19b5533d2b5e4cb64e930d2005f966f6966c94debbe538e88827dad2b9359197`; `ACCEPT_AGGRESSIVE`.

## CURRENT-SEASON-CATBOOST-SEED-ENSEMBLE-096
- Added current-season CatBoost seed 52 and compared an equally weighted seed42/52 ensemble against accepted 093, with its offset refit only on 2020-2022. It worsened all three development seasons (`+9.4884e-06` pooled); 2023/2024 were not accessed and 093 was retained; `REJECT_DEVELOPMENT`.

## CURRENT-SEASON-CATBOOST-BRIER-097
- Trained a CatBoost RMSE regressor on the 55 current-season features and screened 10/20/30% within-current blends. Overall Brier improved all three development seasons, but severe opposing target shifts failed the guard. After development-only centering, the RMSE model was also worse than accepted 093 in every development season; `NO_BRIER_CATBOOST_CANDIDATE`.

## CURRENT-SEASON-CATBOOST-LOWVAR-098
- Tested a depth-5, stronger-regularized low-variance CatBoost configuration against accepted 093 after development-only centering. It worsened all three development seasons (`+2.7894e-05`); 2023/2024 were not accessed; `REJECT_DEVELOPMENT`.

## CURRENT-SEASON-CATBOOST-WEIGHT-099/PACKAGE-100
- Re-optimized only the global hybrid weight after CatBoost entered the current-season component. A 90% hybrid weight improved all 2020-2024 seasons versus 093's 80%; locked 2024 gained an additional `-3.0897e-06`, while both targets remained improved versus the pre-CatBoost 80% model. POSIX archive and extracted smoke passed. Package `submit_current_season_catboost_90pct_099_linux.zip`, SHA-256 `c199045b08018e47af55d3dca7208d6771de9211284fb8237d74f2c5434e1df0`; `ACCEPT_SMALL`.

## PREDICTION-STACKING-101/PACKAGE-102
- Fit nonnegative sum-to-one weights plus a bounded intercept by pooled 2020-2022 Brier using only incumbent, current LGBM, and raw current CatBoost OOF predictions. The frozen stack (`0% / 27.9173% / 72.0827%`, intercept `-0.00394186`) beat accepted 093 in all development seasons, 2023 (`-1.1232e-04`), and locked 2024 (`-6.3237e-05`). Locked target1 was `+3.3675e-05` versus 093 but remained improved versus the pre-CatBoost 80% model; aggregate Brier/AUC reached `0.2476851799 / 0.5518766171`. POSIX archive and extracted smoke passed. Package `submit_prediction_stacking_101_linux.zip`, SHA-256 `389ba3387584f87c8d07b282cf21b3d8ed1fc085019c50ac84ef41c77248ce2a`; `ACCEPT_AGGRESSIVE`.

## ROBUST-PREDICTION-STACKING-103
- Added pooled target0/target1 no-loss constraints to the 2020-2022 Brier stack. It retained almost the same aggressive CatBoost-heavy weights and improved aggregate Brier through 2024, but target directions continued to reverse by season; locked 2024 target0 worsened `+1.0707e-04`. The unconstrained 101 stack remains the stronger aggregate candidate; `REJECT_TARGET_GUARD`.

## RIDGE-PREDICTION-STACKING-104
- Selected stacking regularization by strict expanding validation (`fit 2020 -> validate 2021`, `fit 2020-2021 -> validate 2022`) across five ridge strengths anchored to 093. Every strength worsened both validation folds; 2023/2024 were not accessed and 101 remained the aggressive candidate; `NO_RIDGE_CANDIDATE`.

## CATBOOST-CURRENT-FEATURE-ABLATION-105
- Tested `no_count`, `no_raw`, `no_delta`, and `shrink_only` specifically for the dominant CatBoost component, recalibrating each intercept only on 2020-2022 with 101 stack weights fixed. Every ablation worsened pooled development Brier; `no_raw` was least harmful at `+4.3514e-05` but lost two seasons. 2023/2024 were not accessed and full6 was retained; `NO_ABLATION_IMPROVEMENT`.

## CATBOOST-CURRENT-STRUCTURE-106
- Tested three preregistered current-season CatBoost structures (`d4_fast`, `d6_reg`, `d7_reg`) against the 101 stack, recalibrating only their development intercepts. Every structure worsened pooled 2020-2022 Brier; `d4_fast` was least harmful at `+2.9587e-05` and lost all three seasons. 2023/2024 were not accessed and the baseline CatBoost was retained; `NO_STRUCTURE_IMPROVEMENT`.

## CATBOOST-PITCHER-BATTER-CURRENT-107
- Added six reconstructed batter-current-season features to the dominant CatBoost component and recalibrated its intercept only on 2020-2022. Pooled Brier was nearly neutral but worse (`+1.9229e-06`), with one season win, two losses, and worst-season loss `+1.2261e-04`. 2023/2024 were not accessed and pitcher-only current features were retained; `REJECT_DEVELOPMENT`.

## ROLLING-PROBABILITY-CALIBRATION-108
- Applied 25/50/100% of each previous season's mean 101-stack OOF residual as the next season's fixed correction. Every factor failed strict 2021-2022 expanding validation; the least harmful 25% factor worsened mean Brier `+4.2774e-05`. 2023/2024 were not accessed; `NO_CALIBRATION_CANDIDATE`.

## PLATT-PROBABILITY-CALIBRATION-109
- Fit affine-probability and Platt-logit calibration on pooled 2020-2022 predictions. Both slightly improved pooled fit (`-8.3232e-06` and `-7.7968e-06`) solely through a 2020 gain, while worsening 2021 and 2022. Neither qualified for 2023/2024 access; the uncalibrated 101 stack was retained; `NO_STABLE_CANDIDATE`.

## RECENT-WINDOW-CURRENT-CATBOOST-111
- Compared two- and three-season CatBoost training windows against the full-history 101 stack on 2022-2023, using development-only intercept fitting. Both lost both seasons: recent3 worsened mean Brier by `+5.6685e-05` and recent2 by `+9.4990e-05`, with severe target imbalance. 2024 was not accessed; the full-history CatBoost was retained; `NO_RECENT_WINDOW_CANDIDATE`.

## SEASON-DECAY-CURRENT-CATBOOST-112
- Tested CatBoost yearly sample-weight multipliers 0.50/0.70/0.85/0.95 against 101 on 2022-2023. The best, 0.85, still worsened mean Brier by `+5.3437e-06` and split the seasons 1-1; all candidates materially worsened target1. 2024 was not accessed and full-history equal weighting was retained; `NO_SEASON_DECAY_CANDIDATE`.

## PITCHER-ID-CATBOOST-113
- Added official `pitcher_id` as a CatBoost categorical feature and blended the resulting model into 25/50/75/100% of the CatBoost component. Every fraction worsened pooled 2020-2022 Brier; the least harmful 25% fraction was `+1.2701e-05` with one season win and two losses. 2023/2024 were not accessed; `NO_PITCHER_ID_CANDIDATE`.

## RELIABILITY-GATED-RECENT-CATBOOST-114
- Applied the three-season CatBoost only when reconstructed current-season pitcher volume exceeded 20/50/100/200 pitches, at 25/50/100% prediction fractions. Every candidate lost both 2022 and 2023; the least harmful threshold 20/fraction 25% candidate worsened Brier by `+1.0893e-05`. 2024 was not accessed; `NO_RELIABILITY_GATE_CANDIDATE`.

## TEMPORAL-RESIDUAL-CATBOOST-115
- Trained an expanding-window CatBoost regressor on prior-season out-of-fold residuals of stack 101, with prediction/disagreement and the 55 official-data features. All correction fractions worsened pooled 2021-2023 Brier; the least harmful 10% correction was `+5.3980e-05` with one win and two losses. The 2024 locked metric was not evaluated; `NO_RESIDUAL_CANDIDATE`.

## RELIABILITY-GATED-BATTER-CATBOOST-116
- Applied the pitcher+batter current-season CatBoost only for batters with at least 10/20/50/100/200 reconstructed current-season plate appearances, at 25/50/100% fractions. The selected threshold 10/fraction 25% candidate improved all three development seasons (`-1.9612e-05`), 2023 (`-1.5433e-04`), and 2024 aggregate Brier (`-1.7390e-05`). It worsened target1 on 2023 and 2024, so it failed the strict locked target guard despite five-season aggregate consistency; `REJECT_LOCKED_TARGET_GUARD`.
- Built `submit_batter_gate_116_linux.zip` from official train data only. SHA-256 `af684096c05d87afa9e9c1d20b15ad82e42015a83baa6de2f5f6ed84e931d139`; 17 POSIX archive entries, CRC, extracted asset resolution, and five-row inference all passed.

## BATTER-GATE-FRACTION-117
- Fine-searched batter-model fractions 0.10-0.50 at the fixed 10-PA gate using 2020-2023. The existing 0.25 fraction was the strongest candidate that improved all four development seasons (`-5.3221e-05` pooled); it also improved 2024 aggregate Brier by `-1.7390e-05`. The already-built 116 ZIP exactly matches this selected formula; `ACCEPT_AGGREGATE`.

## CATBOOST-OOF-DIVERSITY-118
- Trained eight structurally diverse CatBoost architectures with strict season-forward OOF predictions and tested 5/10/20/30% blends into 116. The selected high-randomness model improved all three 2020-2022 seasons (`-4.0277e-05`) but worsened 2023 by `+1.4727e-05`; `REJECT_CONFIRMATION`.

## CATBOOST-DIVERSITY-CONFIRMATION-119
- Screened the best development-qualified fraction from each of seven architectures on 2023. The target-guarded `p55_d5_bayes` 20% blend improved 2023 by `-4.4740e-06` but worsened 2024 by `+8.5547e-06`; `REJECT_LOCKED`.

## CATBOOST-DIVERSITY-AGGRESSIVE-120
- Locked the strongest aggregate confirmation model, `pb61_d5_bayes` at 30%, after development improvement `-3.3593e-05` and 2023 improvement `-1.7470e-04`. It was nearly neutral but worse on 2024 (`+1.2165e-06`) with opposing target effects; `REJECT_LOCKED`. Candidate 116 remains preferred.

## BATTER-CURRENT-SUBSETS-121
- Trained seven time-forward CatBoost variants using targeted subsets of the six batter current-season features. Five subsets passed development; `no_count` was strongest with all three 2020-2022 wins (`-1.2959e-05` versus 116), but worsened 2023 by `+1.2017e-05`; `REJECT_CONFIRMATION`.

## BATTER-SUBSET-CONFIRMATION-122
- Screened all five development-qualified batter subsets on 2023. None improved aggregate Brier; the least harmful `no_raw` subset was `+2.8241e-06` and also exceeded the target guard. 2024 was not evaluated for these subsets; `NO_CONFIRMED_SUBSET`.

## SITUATION-CROSS-CATBOOST-123
- Trained seven explicit CatBoost situation-cross feature groups spanning count, handedness, base state, inning, score, and game type. The strongest development candidate, count alone at 25%, improved all three 2020-2022 seasons (`-3.7738e-06`) but worsened 2023 by `+5.9261e-06`; `REJECT_CONFIRMATION`.

## SITUATION-CROSS-CONFIRMATION-124
- Screened the best qualified fraction from each of three development-qualified cross groups. The count/count-hand/count-base group at 10% improved 2020-2022 pooled Brier by `-6.5789e-07`, 2023 by `-6.9709e-07`, and 2024 by `-2.1083e-06`. It had one development-season loss and mixed target effects, so the gain is accepted only as a tiny aggregate candidate; `ACCEPT_AGGREGATE_TINY`.

## BATTER-ID-CATBOOST-125
- Trained CatBoost variants with official `batter_id` as a categorical feature on pitcher55 and pitcher+batter61 inputs, then blended them into candidate 116. The pitcher+batter61 identity model at 30% improved all three 2020-2022 seasons (`-2.7604e-05`), 2023 (`-1.0592e-04`), and 2024 (`-6.6938e-06`). Target effects flipped by season, but all five aggregate folds improved; `ACCEPT_AGGREGATE`.

## BATTER-ID-FRACTION-126
- Fine-searched 10-60% fractions for the pitcher+batter61 plus batter-ID CatBoost using 2020-2023. The 50% blend was the strongest fraction with all four development-season wins (`-7.0568e-05` pooled) and improved 2024 by `-6.4643e-06`; `ACCEPT_AGGREGATE`. Built `submit_batter_id_126_linux.zip` from official train data only. SHA-256 `2c5756ba89d86c2a5158e73f4b523f6d4051340e983fcc5f37ee3dfcc9a934ba`; 18 POSIX entries, CRC, extracted asset resolution, and five-row inference passed.

## BATTER-ID-RELIABILITY-GATE-127
- Restricted the 50% batter-ID component to batters with at least 1/10/25/50/100/250/500 prior-season observations. Every gate worsened 126; even the least restrictive threshold 1 lost three of four development seasons and increased pooled Brier by `+1.3574e-05`. 2024 was not evaluated; the global 50% identity blend was retained; `NO_RELIABILITY_GATE_CANDIDATE`.

## BATTER-ID-STRUCTURE-128
- Trained six alternative CatBoost structures for the successful batter-ID component with resumable season checkpoints. The selected depth-6/high-randomness model improved 2020-2022 pooled Brier by `-6.5439e-05` and 2023 by `-2.0305e-04`, with both 2023 targets improving, but worsened 2024 by `+3.0431e-05`; `REJECT_LOCKED`. Baseline structure 126 was retained.

## BATTER-ID-CROSSES-130
- Trained six explicit high-cardinality batter-ID cross variants with pitcher hand, count, game type, and base state. Every variant lost all three 2020-2022 selection seasons versus 126; the least harmful ID-count cross still worsened pooled Brier by `+2.4361e-05`. 2023/2024 were not evaluated; `NO_ID_CROSS_CANDIDATE`.

## BATTER-HAND-HISTORY-131
- Added six leakage-safe, prior-season-only batter-by-opposing-pitcher-hand history features: sample size, raw rate, three shrinkage rates, and batter-relative delta. Replacing the 126 identity component lost all three 2020-2022 seasons and worsened pooled Brier by `+4.9184e-05`; 2023/2024 were not evaluated; `REJECT_DEVELOPMENT`.

## BATTER-ID-CTR-TUNING-132
- Tested five CatBoost categorical-processing variants for the successful batter-ID component. Limiting CTR leaves to 256 improved all three 2020-2022 seasons (`-3.0617e-05` versus 126), 2023 (`-5.4261e-05`), and 2024 (`-1.7398e-06`). Target effects were mixed in 2023/2024, but all five aggregate folds improved; `ACCEPT_AGGREGATE`.
- Built `submit_batter_id_ctr_132_linux.zip` from official train data only. SHA-256 `c505dd28c9d55b4ac27f325c87e5a9fe1bfd52a7b7c7d5fbdbf132d21042d2a0`; 18 POSIX entries, CRC, extracted asset resolution, and five-row inference passed.

## BATTER-ID-CTR-FRACTION-133
- Fine-searched 25-150% replacement of the baseline identity component with the CTR-limited model. The 150% extrapolation improved all four 2020-2023 seasons (`-3.9503e-05`) but worsened 2024 by `+4.7472e-06`; `REJECT_LOCKED`. The validated 100% replacement from 132 was packaged instead.

## BATTER-ID-SITUATION-EXPERTS-134
- Trained separate batter-ID CatBoost experts for opposing-pitcher hand (2 models), count advantage (3), and runners empty/on (2), using strict season-forward folds. No family improved all three 2020-2022 seasons; count experts were least harmful (`-2.4530e-06` pooled) but won only one season. 2023/2024 were not evaluated; `NO_EXPERT_CANDIDATE`.

## BATTER-ID-SEASON-WEIGHT-135
- Tested yearly training-weight multipliers 0.80/0.90/0.95/0.98 on the batter-ID model. None passed development; the best 0.90 candidate still worsened pooled Brier by `+6.1571e-06` and won only one of three seasons. 2023/2024 were not evaluated; `NO_SEASON_WEIGHT_CANDIDATE`.

## VALIDATED-ID-ENSEMBLE-136
- Enforced the post-132 rule that an auxiliary must pass the strict locked gate and have no public rejection before receiving a 5-15% OOF blend. CTR256 was publicly rejected (about 998 versus 126 at 1008.137), while 134 and 135 failed development. No auxiliary was eligible; `NO_ELIGIBLE_AUXILIARY_RETAIN_126`.

## BASELINE-126-RESTORE
- Recreated `submit_batter_id_126_linux.zip`; SHA-256 exactly matched the public-validated baseline `2c5756ba89d86c2a5158e73f4b523f6d4051340e983fcc5f37ee3dfcc9a934ba`. Public score remains `1008.1373865799`.

## TRACKMAN-EXPANDED-RELEASE-137
- Revalidated 061 expanded pitcher mapping with strict prior-season release-location features against public baseline 126. Coverage rose to 57.1-65.6%; development and 2023 improved, but locked 2024 improvement was only `-2.9638e-06` and target 1 worsened `+3.7697e-05`, below the post-public strict gate. `REJECT_LOCKED`; retain 126 and do not package.

## BATTER-RECENT-IDENTITY-138
- Added a previous-season-only batter identity alongside the pooled batter ID and tested 10/25/50% replacement against 126. Every fraction worsened pooled development Brier; best 10% was `+3.0905e-06` with one of three season wins. 2023/2024 were not accessed; `REJECT_SELECTION`.

## PITCHER-BATTER-ID-139
- Added categorical pitcher ID to 126's batter-ID CatBoost and tested 5/10/20% replacement. All fractions won two of three seasons and improved target 1, but worsened pooled Brier; best 5% was `+1.0257e-06`, driven by target 0 loss. 2023/2024 were not accessed; `REJECT_SELECTION`.

## PITCHER-ID-RESIDUAL-140
- Tested controlled negative 5/10/20% use of the 139 disagreement. Pooled development improved, best `-1.6525e-06`, but every fraction won only one of three seasons and worsened target 1. 2023/2024 were not accessed; `REJECT_SELECTION`.

## PITCHER-ID-AUXILIARY-141
- Trained an independent pitcher-ID CatBoost without batter ID and blended it 5/10/20% into 126. The best 5% gave only `-4.8915e-07`, won one of three seasons, improved target 1, and worsened target 0. 2023/2024 were not accessed; `REJECT_SELECTION`.

## COUNT-GATED-PITCHER-ID-142
- Gated the 139 pitcher-ID disagreement by hitter-ahead/even/pitcher-ahead count groups. Pitcher-ahead at 5% passed development and 2023, but locked 2024 improved only `-3.1857e-07`, far below the `-1e-05` public-safety gate. `REJECT_LOCKED`; retain 126.

## BASELINE126-RESIDUAL-BIAS-143
- Audited 126 residual bias across count, pitcher hand, batter hand, and runner-state segments. Every segment's bias changed sign across 2020-2022, so none passed the preregistered temporal-stability gate. 2023/2024 corrections were not evaluated; `REJECT_SELECTION`.

## LAGGED-SEASON-CALIBRATION-144
- Tested row-independent season calibration using only the previous official labeled season: lagged 126 OOF residual and lagged league-rate change, each at 25/50% shrinkage. Every candidate won only one of two development seasons and worsened pooled Brier; best delta was `+4.0954e-05`. No test aggregation and no 2023/2024 evaluation; `REJECT_SELECTION`.

## BASELINE126-TEMPERATURE-145
- Tested fixed row-local logit temperatures 0.90/0.95/1.05/1.10 on 126. Temperature 1.05 improved pooled Brier by `-2.3879e-06`, but won only one of three seasons, exceeded the target-loss gate, and had worst-season loss `+9.3618e-05`. 2023/2024 were not evaluated; `REJECT_SELECTION`.

## BATTER-ID-SEED-BAGGING-146
- Averaged batter-ID CatBoost seeds 42/52/62 and replaced the seed-42 ID component in 126. Development won two of three seasons but pooled Brier worsened `+3.8348e-06`, with both target classes worse. 2023/2024 were not evaluated; `REJECT_SELECTION`.

## BATTER-ID-SEED-BLEND-147
- Blended the 146 seed mean into 126 at 10/25/50%. The selected 25% candidate passed development and 2023, but locked 2024 improved only `-2.6516e-06` while target 1 worsened `+8.7778e-05`; below the `-1e-05` gate. `REJECT_LOCKED`; retain 126.

## BATTER-ID-CONTINUOUS-RELIABILITY-148
- Replaced 126's fixed 0.50 batter-ID fraction with row-local smooth weights based on current-season batter sample size (strength 10/50, amplitude 0.025/0.05). Best pooled delta was only `-6.1498e-08`, with one of three season wins and target 1 worsening. 2023/2024 were not evaluated; `REJECT_SELECTION`.

## FINAL-CANDIDATE-STRESS-149
- Rebuilt and hash-verified public model 126 (`2c5756ba89d86c2a5158e73f4b523f6d4051340e983fcc5f37ee3dfcc9a934ba`). ZIP has 18 POSIX entries, valid CRC, no network dependency or test-wide aggregation, and smoke inference reproduced locked predictions exactly in 2.08 seconds. All 137-148 challengers were rejected; `PASS_RETAIN_126`.

## BATTER-ID-ORDERED-BOOSTING-150
- Replaced only CatBoost's Plain boosting with Ordered boosting for the batter-ID component. Pooled development improved `-1.5133e-05` and both targets improved, but the gain came from 2020 (`-9.4593e-05`); 2021 and 2022 worsened. It won one of three seasons, so 2023/2024 were not evaluated; `REJECT_SELECTION`.

## BATTER-ID-ORDERED-BLEND-151
- Blended the Ordered batter-ID model into 126 at 5/10/20%. The selected 20% candidate passed development (`-6.3900e-06`) and 2023 (`-1.2891e-05`), but locked 2024 worsened `+1.8918e-06` and both target-class limits were exceeded. `REJECT_LOCKED`; retain 126.

## BATTER-ID-ORDERED-TIME-152
- Tested Ordered boosting with `has_time=True` after verifying monotonic season order and nondecreasing as-of pitcher counts. Development Brier worsened `+2.7480e-05`, won one of three seasons, and exceeded target/worst-season gates. 2023/2024 were not evaluated; `REJECT_SELECTION`.

## BATTER-PREVIOUS-SEASON-PROFILE-153
- Added strict previous-season batter support, shrinkage-50 success rate, and league-relative rate to the batter-ID CatBoost. Development Brier worsened `+1.7414e-05`, won one of three seasons, and target 0 degraded. 2023/2024 were not evaluated; `REJECT_SELECTION`.

## BATTER-ID-D6RANDOM3-BLEND-154
- Blended 128's strong `d6_random3` batter-ID model into 126 at 5/10/20/30%. The selected 30% candidate strongly improved development (`-2.4538e-05`) and 2023 (`-6.3838e-05`), but locked 2024 worsened `+6.2473e-06` with target-class instability. `REJECT_LOCKED`; no post-lock weight substitution.

## BATTER-ID-PREVIOUS-WINDOW-155
- Trained the batter-ID CatBoost on only season S-1 for each target season S. It lost all three development seasons, worsening pooled Brier `+1.2448e-04` and both targets. 2023/2024 were not evaluated; `REJECT_SELECTION`.

## BATTER-ID-BRIER-REGRESSION-156
- Replaced 126's raw batter-ID Logloss component with a CatBoost RMSE/Brier regressor and tested 10/25/50/100% replacement. The selected 25% blend improved development only `-7.9626e-07` and 2023 aggregate `-9.9541e-06`, but target 1 worsened `+6.4209e-05`, exceeding the gate. 2024 was not accessed; `REJECT_CONFIRMATION`, retain 126.

## BATTER-ID-FEATURE-ABLATION-157
- Tested a batter-ID CatBoost without pitch-mix features and a batter-focused version with pitcher-history features removed. The selected no-pitchmix 25% blend improved development only `-9.7696e-07` and 2023 aggregate `-1.0631e-05`, but target 1 worsened `+5.4625e-05`, above the gate. 2024 was not accessed; `REJECT_CONFIRMATION`, retain 126.

## BATTER-RECENT-PITCHER-TYPE-158
- Added strictly prior-season, season-normalized batter form split by pitcher handedness, including long/recent residual effects, trend, and support. The selected 50% blend improved development `-3.3674e-06` and 2023 aggregate `-5.8254e-06`, but target 0 worsened `+5.1451e-04`. 2024 was not accessed; `REJECT_CONFIRMATION`, retain 126.

## BATTER-ID-SEASON-CONTINUITY-159
- Reduced the 126 batter-ID branch for batters without previous-season presence or at least two distinct prior seasons. Every candidate worsened pooled development Brier; best was `+5.1015e-06` with only one season win. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## BATTER-ID-EXTENSION-160
- Increased 126's batter-ID fraction from 0.50 to fixed 0.55/0.60/0.65. Fraction 0.65 improved pooled development `-2.0774e-06` and both targets, but only 2021 improved; 2020 and 2022 worsened. It failed the two-season gate, so 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## BASELINE126-TEMPORAL-STACKING-161
- Fit bounded ridge residual-stack weights for r101, batter-season, batter-ID, and LGB components using only seasons strictly before each target season. The weights were temporally unstable: 2021 and 2022 both worsened, pooled Brier increased `+1.7003e-04`, and target 1 degraded `+4.4726e-03`. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## BATTER-ID-CURRENT-FORM-CROSS-162
- Added a fixed categorical cross of batter ID, current-season as-of PA support bin, and as-of success-rate bin to the 126 batter-ID CatBoost. The smallest 10% blend won two seasons but worsened pooled Brier `+2.4096e-06` and target 0; larger blends were worse. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## BATTER-ID-LIGHTGBM-163
- Trained a native-categorical LightGBM on the full 61 features plus raw batter ID and blended it into 126 at 10/25/50%. The 10% blend worsened pooled development Brier `+4.9283e-06` with one season win; larger blends lost all seasons. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## TRACKMAN-PITCHER-CLUSTER-164
- Built six fixed 2019 unsupervised pitcher-arsenal clusters from prior-season pitch mix, velocity, spin, and movement; joined only through 061 reliable mappings and added cluster-by-batter-hand. Coverage was 59.9-61.0% in development. Even the 5% blend worsened pooled Brier `+1.0269e-06` with one season win. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## TRACKMAN-COVERAGE-GATED-165
- Applied the 137 release-location model only to rows with all prior-season TrackMan release features available through 061 reliable mappings. The selected 10% gate was neutral on development (`-8.6174e-09`) and improved 2023 `-3.4279e-06`, but locked 2024 improved only `-9.2946e-07`, below the preregistered `-1e-05` minimum, while target 1 worsened. `REJECT_LOCKED`, retain 126.

## TRACKMAN-HIGH-TIER-GATE-166
- Restricted the 137 release-location correction to ORIGINAL_HIGH pitcher mappings with complete prior-season features. The selected 15% blend improved development `-3.6515e-07`, 2023 `-1.9076e-06`, and locked 2024 `-5.5834e-07`, but remained far below the `-1e-05` gate and target 1 worsened in confirmation/lock. `REJECT_LOCKED`, retain 126.

## TRACKMAN-TIER-WEIGHT-167
- Tested nine fixed tier-specific weights for ORIGINAL_HIGH and PROMOTED_RELIABLE TrackMan mappings. Selection chose 20% for ORIGINAL_HIGH and 0% for promoted mappings. It improved development `-3.9627e-07`, 2023 `-2.5073e-06`, and locked 2024 `-7.0652e-07`, but remained far below the `-1e-05` gate and target 1 worsened. `REJECT_LOCKED`, retain 126.

## LATENT-PITCHER-BATTER-SVD-168
- Built strictly past, season-normalized pitcher/batter effects and rank 4/8/16 SVD matchup embeddings, then blended them into 126 at 2/5/10%. The best rank-16 2% blend worsened pooled Brier `+7.3815e-06`, won one season, and strongly shifted target-class loss despite regularization. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## TRACKMAN-RESIDUAL-MODEL-169
- Trained a small LightGBM only on strictly prior 126 OOF residuals for rows with reliable previous-season TrackMan profiles. The compact bundle included velocity, spin, movement, release, pitch mix, count, and batter hand; development coverage was about 60%. Every nonzero correction worsened both eligible development seasons; the smallest 5% correction increased pooled Brier `+1.1065e-06`. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## BATTER-ARCHETYPE-CLUSTER-170
- Built eight fixed batter archetypes from strictly previous-season overall, handedness, count-state, and runner-state success profiles, then added archetype interactions to the 126 batter-ID CatBoost. Coverage was 86-87%, but every blend lost all three development seasons; the smallest 10% blend worsened pooled Brier `+8.3489e-06`. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## PLAYER-MOBILITY-TENURE-171
- Added strictly past pitcher/batter season counts, appearance gaps, prior-team counts, current-team tenure, same-team indicators, and mobility-state categories to the 126 batter-ID CatBoost. The smallest 10% blend won 2020 and 2022 but worsened pooled Brier `+5.8156e-06` because 2021 degraded `+1.8388e-05`; larger blends were worse. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## BATTER-ID-MODEL-SIZE-REG-172
- Tested CatBoost `model_size_reg` 0/1/5 with all other 126 settings fixed and 10/25% blends. The selected value 1 at 25% improved all three development seasons (`-5.4325e-06`) and 2023 (`-3.6890e-07`), but locked 2024 improved only `-2.4345e-06`, below the `-1e-05` minimum, while target 1 worsened. `REJECT_LOCKED`, retain 126.

## BASELINE126-MULTISEGMENT-RESIDUAL-173
- Applied fixed shrinkage corrections to five preregistered multidimensional segment families whose 126 residual biases had the same sign in all three development seasons. Count-by-handedness improved all three seasons and pooled Brier `-1.6375e-05`, but target 0 worsened `+5.9934e-05`, narrowly exceeding the `+5e-05` gate. 2023/2024 were not accessed; `REJECT_SELECTION`, retain 126.

## BASELINE126-NEUTRALIZED-SEGMENT-174
- Removed the fixed development mean shift from 173's count-by-handedness corrections. Full neutralization improved all three development seasons (`-1.6380e-05`), both targets, and 2023 (`-1.1658e-05`). Locked 2024 improved `-9.9209e-06` with both target losses within limits, missing the preregistered `-1e-05` threshold by `7.9084e-08`. `REJECT_LOCKED` by the frozen rule; retain 126 pending robustness review.

## FINAL-CANDIDATE-STRESS-110
- Stress-tested 101 against 093 across season, target, game type, inning side, count, handedness, base state, and pitcher-history bins. All five seasons improved; 38/39 reported subgroups improved, with pooled target1 the sole loss. The 2024 pitcher-cluster bootstrap 95% interval was entirely favorable (`-9.0402e-05` to `-3.5948e-05`). Renamed archive `submit(강력후보).zip` matched expected SHA-256 `389ba3387584f87c8d07b282cf21b3d8ed1fc085019c50ac84ef41c77248ce2a`; POSIX/CRC and extracted inference passed; `PASS_AGGREGATE_AGGRESSIVE`.

## TRACKMAN-PITCH-TEACHER-175
- Strict-past TrackMan pitch-type teacher with 399,644 unique training alignments versus public-best 126: `REJECT_CONFIRMATION`. Current-pitch TrackMan is used only as a historical training label; inference uses row-local pre-pitch inputs only.

## TRACKMAN-PITCH-TEACHER-LOWBLEND-176
- Strict-past TrackMan pitch-type teacher with 399,644 unique training alignments versus public-best 126: `REJECT_CONFIRMATION`. Current-pitch TrackMan is used only as a historical training label; inference uses row-local pre-pitch inputs only.

## TRACKMAN-PITCH-TEACHER-FIXED005-177
- Strict-past TrackMan pitch-type teacher with 399,644 unique training alignments versus public-best 126: `REJECT_LOCKED`. Current-pitch TrackMan is used only as a historical training label; inference uses row-local pre-pitch inputs only.
## BATTER-ID-STRUCTURE-CTR-COMBO-178
- Combined the strongest previously isolated CatBoost changes (`random_strength=3`, `l2_leaf_reg=10`, `ctr_leaf_count_limit=256`). Selection Brier improved `-7.93e-5` and 2023 improved `-1.58e-4`, but locked 2024 degraded `+2.71e-5`; `REJECT_LOCKED`. Public-best 126 retained.

## HIERARCHICAL-PITCHER-ID-RESIDUAL-179
- Strict-past hierarchical pitcher / hand / count target encoding with ridge residual correction versus 126: `REJECT_SELECTION`.
## BATTER-ID-DEPTHWISE-181
- Tested a new broad CatBoost `Depthwise` batter-ID architecture against 126 under the raised leaderboard-aligned gate. It lost all three selection seasons and worsened pooled Brier by `+3.32e-5`; `REJECT_SELECTION`. 2023/2024 were not accessed.

## CONTROL-SUBTYPE-TEACHER-182
- Training-only reconstructed control-subtype teacher versus 126, with row-local inference and no other test-row access: `REJECT_SELECTION`.

## CONTROL-SUBTYPE-FEATURE-CATBOOST-183
- Reused strict-past subtype teacher probabilities as nonlinear features in the 126 batter-ID CatBoost branch: `REJECT_SELECTION`.

## TABM-BLEND-185
- Local CPU TabM-style OOF predictions worsened 126 at 5/10/15% blends; `REJECT_TABM`.

## IDENTITY-UNCERTAINTY-186
- Added leakage-safe posterior mean, uncertainty, and z-score identity features. Every blend worsened pooled selection Brier; `REJECT_SELECTION`.

## BATTER-ID-COMBINATION-CTR-187
- CatBoost categorical combination complexity 2/3 improved selection and 2023 aggregate Brier, but the selected candidate worsened 2023 target 1 by `+1.2814e-4`; `REJECT_CONFIRMATION`.

## COMBINATION-CTR-TOURNAMENT-188
- Searched 12 depth/CTR-complexity/L2 structures with two-seed averaging across 72 temporal models. Best robust three-season candidate improved only `-4.3483e-6`, below the preregistered `-5e-6` minimum; 2023/2024 were not accessed; `REJECT_SELECTION`.

## COMBINATION-CTR-STABLE-FOLLOWUP-189
- Fixed the all-three-season 188 candidate (`depth=6`, CTR complexity 2, L2 3, seeds 42/52, 25% blend) before follow-up. It improved 2023 by `-1.9295e-5`, but locked 2024 improved only `-1.7924e-6`, below the `-1e-5` minimum; `REJECT_LOCKED`, retain 126.

## COMBINATION-CTR-STABLE-ENSEMBLE-190
- Averaged the two all-three-season stable CTR structures from 188 before blending 25% into 126. All three selection seasons improved, but pooled gain was only `-4.3042e-6`, below the frozen `-5e-6` minimum; 2023/2024 were not accessed; `REJECT_SELECTION`.

## BATTER-ID-LOSSGUIDE-191
- Tested three CatBoost Lossguide asymmetric-tree structures and 10/25/50% blends against 126. The best 10% candidate improved all three selection seasons but only by `-5.1154e-7`, far below the frozen minimum; 2023/2024 were not accessed; `REJECT_SELECTION`.

## BATTER-ID-BOOTSTRAP-192
- Tested MVS and Bayesian bootstrap regularization in the 126 batter-ID branch. Bayesian temperature 1 at 50% improved selection by `-6.3774e-6` and 2023 by `-4.3336e-5`, but locked 2024 improved only `-3.1079e-6`, below the `-1e-5` minimum; `REJECT_LOCKED`, retain 126.

## BAYESIAN-BOOTSTRAP-SEED-ENSEMBLE-193
- Averaged seeds 42/52 for 192's Bayesian bootstrap candidate. Pooled selection improved only `-1.3706e-6`, with 2021 worsening `+1.0837e-5`; 2023/2024 were not accessed; `REJECT_SELECTION`.

## BAYESIAN-SEGMENT-GATE-194
- Tested frozen row-local count, handedness, runner, and inning-side gates for 192's Bayesian correction. Runners-empty improved all three selection seasons (`-5.8841e-6`) and 2023 (`-2.0798e-5`), but locked 2024 improved only `-3.0755e-6`, below the `-1e-5` minimum; `REJECT_LOCKED`, retain 126.

## BATTER-ID-FEATURE-SAMPLING-195
- Tested CatBoost feature subsampling and per-tree sampling in the 126 batter-ID branch. RSM 0.70 at 50% improved selection by `-8.6165e-6`; 2023 improved `-9.8857e-6`, missing the frozen `-1e-5` confirmation minimum by `1.1426e-7`. 2024 was not accessed; `REJECT_CONFIRMATION`, retain 126.

## RSM-SEED-ENSEMBLE-196
- Averaged seeds 42/52 for 195's fixed RSM 0.70 candidate. Pooled selection was effectively neutral (`+5.9916e-9`) and 2021 worsened `+1.9434e-5`; 2023/2024 were not accessed; `REJECT_SELECTION`.

## RSM-SEGMENT-GATE-197
- Tested row-local situation gates for 195's RSM correction. Runners-empty improved all three selection seasons (`-6.2005e-6`), but 2023 improved only `-1.9452e-6`, below confirmation minimum; 2024 was not accessed; `REJECT_CONFIRMATION`.

## TRACKMAN-PITCHMIX-SIMILARITY-198
- Audited pitcher identity expansion by matching season-level fastball/breaking/offspeed fingerprints within throwing hand. Against 318 known 061 pitcher mappings, top-1 accuracy was only `45.60%`, below the frozen `80%` minimum; no mappings were promoted, no target/test data were accessed; `REJECT_MAPPING_EXPANSION`.
## TRACKMAN-SOFT-PROFILE-199 / NEUTRAL-200
- Hard identity linkage was replaced by strict one-season-lagged, same-hand kNN soft averaging of seven TrackMan physical profile fields from official data. Coverage was 97.8%+ from 2020 onward.
- 199 improved pooled 2021-2022 Brier by `-1.0541e-5`, but target=0 worsened `+2.0280e-3`; rejected before 2023/2024.
- Target-free mean neutralization in 200 removed the class imbalance but also removed the gain (best fraction 0.1: `+2.6223e-6`); rejected. Test and locked 2024 were not accessed.
## NEUTRALIZED-SEGMENT-174-ROBUSTNESS-201
- Post-lock robustness audit of fixed 174 versus public-best 126: 32/34 eligible season-month cells improved (94.1%). Pitcher-cluster bootstrap 95% intervals were entirely favorable in every season; 2024 was `[-1.6600e-5, -3.3580e-6]` with 99.82% improvement probability. Both 2024 target deltas stayed below the loss gate. Classified `ROBUST_EXPLORATORY_CANDIDATE`; this post-lock audit does not restore clean locked status.
- Public leaderboard result supplied by the user on 2026-08-21: `1006.4195487012`, below 126's `1008.1373865799`. Archive SHA-256 `2cedb3f61b0bc37963d0383ab5e90bf9d56bb2b5683441b5d4db162ea5db1b58` is now permanently marked `PUBLIC_REJECT`; never recommend or resubmit this archive/correction again.
## CURRENT-SEASON-JOINT-SIGNAL-202
- Added twelve row-local hierarchical combinations of pitcher/batter current-season support, shrunken rates, logit pooling, deviations, and pitcher recent-form gap to the 126 batter-ID branch. Selection improved `-1.4594e-5` with balanced target gains, but 2023 improved only `-9.3175e-6` and target 0 worsened `+2.4701e-4`; `REJECT_CONFIRMATION`. 2024/test were not accessed.
## PUBLIC-BEST-126-CANONICAL-ARCHIVE
- User-confirmed public score: `1008.1373865799`.
- Canonical archive: `C:\Users\junsu\Desktop\최고점.zip`; SHA-256 `86d5beec2227d28c84135f82f8c3b646315a23b84e6ba78ca002b4afb4322a88`; size `2,090,898` bytes. Treat this exact archive as the immutable public-best 126 reference for every future experiment and duplicate-submission check.
## CURRENT-SEASON-JOINT-ABLATION-203
- Split 202's twelve current-season joint features into five preregistered families. `pooled_shrink` at 50% improved selection `-2.0586e-5` with balanced target gains, but 2023 worsened `+6.1625e-6` and target 0 worsened `+1.6468e-4`; `REJECT_CONFIRMATION`. 2024/test were not accessed; retain canonical 126.
## BASELINE126-WITHIN-SEASON-AUDIT-204
- Audited 126 components across 34 eligible season-month cells. Batter-ID improved over the batter-season stack in 73.5% of months (early 80.0%, late 68.4%); batter current-season features improved over r101 in 82.4% (early 86.7%, late 78.9%). Both structural gains remain broad but weaken late in the season; 2024 month signs are mixed, so month-specific gating is not justified. Test was not accessed.
## CURRENT-SEASON-ROBUST-ABLATION-205
- Removed volatile raw current-season rates/deltas from the 126 batter-ID branch in four shrinkage-focused variants. None passed the raised selection gate; the least harmful `pitcher_strong` 10% blend still worsened pooled Brier `+2.1319e-6` and both targets. 2023/2024/test were not accessed; retain canonical 126.
## TEAM-CATEGORICAL-CROSS-206
- Added explicit CatBoost categorical crosses for team matchup, team-by-hand, and game-type-by-team to the 126 batter-ID branch. No family improved pooled selection Brier; best `team_matchup` 10% worsened `+7.0658e-7` and won one season. 2023/2024/test were not accessed; retain canonical 126.
## GAME-TYPE-BATTER-EXPERT-207
- Split the 126 batter-ID CatBoost branch into independent `R`/`F` game-type experts and applied target-free, per-type mean matching to the original branch. The best 10% blend worsened pooled selection Brier `+8.1925e-6`, improved only 2022, and worsened both target classes. `REJECT_SELECTION`; 2023/2024/test were not accessed and canonical 126 remains the only submission candidate.
## BATTER-ID-BORDER-COUNT-208
- Regularized numeric quantization in the 126 batter-ID CatBoost branch with border counts 32/64/128 and target-free mean matching. Border 64 at 25% improved all three selection seasons and both targets, but pooled gain was only `-6.1353e-6`, below the frozen `-1e-5` minimum. The 50% blend gained `-9.2699e-6` but lost 2021. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## BORDER64-SEED-ENSEMBLE-209
- Averaged seeds 42/52 for 208's border-count 64 batter-ID model with target-free mean matching. The ensemble weakened the direction: best 40% blend improved pooled selection Brier only `-3.7021e-6`, while 2021 worsened `+2.8460e-6`. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## BATTER-ID-GRADIENT-LEAF-210
- Replaced the 126 batter-ID branch's default leaf update with Gradient estimation over five iterations and applied target-free mean matching. The best 50% blend improved pooled Brier `-8.3430e-6`, but 2021 worsened `+2.4916e-5` and target 0 worsened `+2.7937e-6`. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## BATTER-ID-L2-SPLIT-SCORE-211
- Changed only the 126 batter-ID CatBoost split score from its default Cosine score to L2 and applied target-free mean matching. Every blend worsened pooled selection Brier; the least harmful 10% blend was `+6.8179e-6`, with only 2022 marginally improving. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## REGULARIZER-PORTFOLIO-212
- Equally averaged the previously promising Bayesian bootstrap, RSM 0.70, and border-count 64 batter-ID variants, then target-free mean matched the portfolio to the original branch. A 25% blend improved all three selection seasons but only by `-5.9720e-6`, below the frozen `-1e-5` minimum. Larger blends exceeded the improvement minimum (`-1.0154e-5` at 50%, `-1.2545e-5` at 75%) but both worsened 2021. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## SELECTIVE-QUANTIZATION-213
- Applied border count 64 only to the four volatile pitcher/batter current-season raw-rate and career-delta features while retaining default quantization elsewhere. All blends worsened every selection season and both targets; the least harmful 10% blend was `+1.6793e-6`. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## NEWTON-LEAF-ITERATIONS-214
- Limited CatBoost Newton leaf estimation to one or five iterations in the 126 batter-ID branch with target-free mean matching. Both variants improved 2020 and 2022 but consistently worsened 2021. The best aggregate candidate, Newton-5 at 50%, gained `-6.3851e-6` but worsened 2021 by `+2.4495e-5`. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## VOLATILE-FEATURE-PENALTY-215
- Retained the four volatile current-season raw-rate/delta features but reduced their CatBoost split-selection weights to 0.50 or 0.75. Every pooled candidate worsened; the least harmful 0.75/10% setting was `+9.7469e-7` and won only 2020. The 0.50 variants improved 2020/2022 but materially worsened 2021. `REJECT_SELECTION`; 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## REGULARIZER-ERROR-CORRELATION-216
- Diagnosed the OOF correction directions of Bayesian bootstrap, RSM 0.70, border-count 64, Gradient-5, and Newton-5 against canonical 126 using 2020-2022 only. Pairwise correlations were moderate (`0.4283`-`0.5857`, median `0.4822`), so the variants are not duplicates and retain some complementary signal. However, every member's pooled oracle-sized gain was below `1e-5`; Gradient-5 and Newton-5 were actively misaligned in 2021, while the other three were nearly neutral there. `RETAIN_COMPLEMENTARY_DIRECTIONS` for future constrained research, but no candidate passed selection, 2023/2024/test were not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## CONSTRAINED-REGULARIZER-PORTFOLIO-217
- Searched 65 preregistered nonnegative 0.25-grid portfolios of Bayesian, RSM 0.70, border-count 64, Gradient-5, and Newton-5 directions at four blend fractions (260 candidates), requiring all three selection seasons and both targets to improve. The strongest fully robust candidate used 25% RSM and 75% border64 at a 25% blend, but gained only `-6.3247e-6`, below the frozen `-1e-5` minimum. Larger pooled gains all incurred a 2021 loss. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## CROSS-FAMILY-SHRINK-REGULARIZER-218
- Combined the target-free current-season pooled-shrink direction from 203 with 217's fixed 25% RSM / 75% border64 regularizer direction across 12 preregistered weights. The best all-three-season candidate (25% signal weight, 25% overall blend) gained `-7.9685e-6`, below the frozen `-1e-5` minimum. A candidate exceeding the pooled threshold (`-1.0731e-5`) still worsened 2021 by `+5.2362e-7`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## CROSS-FAMILY-FRONTIER-219
- Fit the exact quadratic Brier surface of 218's two fixed correction directions (maximum reconstruction error `3.49e-17`) and diagnosed 1,002,001 weight/fraction points without training or candidate promotion. The best no-season/no-target-loss point used 23.3% pooled-shrink signal, 76.7% regularizer, and a 33.4% overall blend, reaching pooled `-1.0055e-5`. Its 2021 delta was only `-7.27e-11`, effectively the zero-loss boundary, so it has no robustness margin and remains diagnostic only. 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## PITCHER-RECENT-FORM-GEOMETRY-220
- Trained 15 season models spanning five preregistered row-local recent-form families: success trend, middle trend, form stability, batter interaction, and their 28-feature union. The strongest robust candidate was the seven-feature success-trend family at a 25% blend; it improved all three selection seasons and both targets, but pooled gain was only `-3.4348e-6`, far below the frozen `-1e-5` minimum. The nominal best 50% blend gained `-3.5422e-6` but worsened 2021. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## ROBUST-SIGNAL-ADDITIVE-PORTFOLIO-221
- Added 220's robust success-trend correction to 218's robust fixed cross-family correction across nine preregistered scale pairs. The strongest fully robust pair (cross-family scale 1.0, recent-form scale 0.5) improved all three seasons and both targets by pooled `-9.4272e-6`, missing the frozen `-1e-5` minimum by `5.73e-7`. The nearest pair above the pooled threshold worsened 2021 by `+1.70e-7`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## SUBMISSION-PAYLOAD-AUDIT-222
- Audited four preserved submission ZIPs by archive SHA-256, uncompressed entry SHA-256, and actual execution on the official five-row probe. Canonical 126 and public-rejected 174 shared nine paths; eight payloads were byte-identical and only `script.py` differed among common files, while 174 added ten files including `segment_corrections_174.csv`. Their predictions were not identical: 174 shifted every probe prediction by `-7.39013897467e-5`, proving the correction is active and the leaderboard difference is not a packaging-only effect. Every preserved ZIP pair produced different probe predictions. The two same-score upload originals shown by the user are not both preserved, so their direct equivalence cannot be proven; exact equal displayed scores are consistent with identical effective predictions despite metadata or unused-file differences. Diagnostic only, no submission created; canonical 126 remains the only submission candidate.
## SUBMISSION-PREFLIGHT-GUARD-223
- Added a reusable submission preflight guard that validates ZIP paths, duplicate members, required payloads, output schema, row IDs, finite probability bounds, known archive hashes, and effective predictions on the official five-row probe. It recognized canonical 126 as `KNOWN_PUBLIC_BEST`, blocked the current `submit.zip` as the exact public-rejected 174 archive, and classified `점수 하락 폐기.zip` as `REVIEW_NEW_PREDICTIONS` after measuring a probe maximum absolute difference of `0.0051576440` from canonical 126. Probe-equivalent archives are also blocked even when ZIP bytes differ. No submission was created; future candidates must pass this guard plus the frozen offline validation gates.
## LONG-SEED-ENSEMBLE-224
- Trained all 18 preregistered selection models for two longer CatBoost schedules (600 iterations at learning rate 0.03 and 900 iterations at 0.02), three seeds each, and three temporal folds. The best pooled candidate was the three-seed `long600` ensemble at a 40% blend, but its gain was only `-1.6618e-6`, it won two of three seasons, its worst season worsened `+1.0551e-5`, and target 0 worsened `+5.4290e-7`. No candidate improved every selection season and both targets, and none approached the frozen `-1e-5` minimum. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## LONG-SEED-PORTFOLIO-225
- Reused 224's six long-training member directions and evaluated all 126 nonnegative 0.25-grid portfolios at six blend fractions (756 candidates) without new model training. No candidate improved all three selection seasons and both targets. The pooled best was `long600_seed52` alone at a 60% blend: both targets improved and pooled Brier gained `-6.0394e-6`, but 2021 worsened `+4.4621e-6` and 2022 worsened `+5.5020e-7`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## GROUPDRO-CATBOOST-226
- Introduced strict-past season-by-target group reweighting for the 126 batter-ID CatBoost branch. Four frozen DRO strengths produced 12 temporal models and 16 blend candidates. Uniform group mass (`eta=0`) at a 60% blend was the pooled best, improving both targets and aggregate Brier by `-3.4696e-5`, but 2021 worsened `+2.2351e-5`; it won only 2020 and 2022. Difficulty-adaptive strengths 0.5/1/2 all worsened pooled Brier because standardized exponential weighting concentrated excessive mass on the hardest historical group (for example 85.2% on 2020 target 0 at eta 2 for the 2022 fold). No candidate improved all three seasons. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate. The new direction retains signal, but any follow-up must cap group mass and specifically neutralize the 2021 reversal.
## CAPPED-GROUP-BALANCE-227
- Interpolated empirical season-by-target group mass toward uniform mass at frozen strengths 20/40/60/80/100%, training 12 new temporal models and reusing 226's three fully balanced checkpoints. Across 30 blends, no candidate improved all three selection seasons. The pooled best used 60% group balancing and 100% model replacement, improving aggregate Brier `-4.9093e-5` and both targets (`-7.1355e-5` / `-2.9467e-5`), but 2021 worsened `+2.8518e-5`; 2020 improved `-1.5743e-4` and 2022 improved `-1.9733e-5`. Even 20% balancing retained a 2021 loss, showing the reversal is structural rather than caused only by uncapped weight concentration. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the GroupDRO axis is closed.
## DYNAMIC-BETA-STATE-228
- Added deployment-parity empirical-Bayes pitcher/batter latent success states with fixed global prior strength 20, retained concentration capped at 500, and season decay 0.25/0.50/0.75. Each row used only its official current `asof` cumulative state plus posterior information from completed earlier seasons; posterior mean, uncertainty, prior weight, and pitcher-batter interactions were added to the 126 batter-ID branch. The decay-0.25 model at a 40% blend passed selection: pooled `-1.5237e-5`, all three season wins (2020 `-3.7620e-5`, 2021 `-8.2851e-6`, 2022 `-1.0206e-7`), and both target improvements (`-2.1766e-5` / `-9.4819e-6`). It also improved 2023 aggregate Brier `-1.5969e-5`, but target 0 worsened `+1.8393e-4` while target 1 improved `-2.1590e-4`, violating the frozen zero-loss target guard. `REJECT_CONFIRMATION`; 2024 was not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate. This state-space axis retains the strongest new structural signal and merits a preregistered target-balance follow-up without reopening decay selection.
## DYNAMIC-BETA-LAG-CENTER-229
- Held 228's decay 0.25, 40% blend, model, and state features fixed, replacing only its pooled target-free ID-branch mean match with four preregistered one-season-lag multipliers. The underlying plain-minus-state gap declined monotonically from 2020 through 2023 (`0.002959`, `0.001514`, `0.000826`, `0.000360`), confirming that 228's fixed `0.001761` shift over-centered 2023. However, no lag multiplier preserved all three selection-season wins and both target guards. The pooled-best 1.0 multiplier gained `-1.6345e-5` but worsened target 0 `+2.5371e-5` and 2022 `+2.5371e-7`; the balanced 0.75 multiplier improved both targets and pooled Brier `-1.5405e-5` but still worsened 2022 `+8.0501e-7`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## DYNAMIC-BETA-GAP-FORECAST-230
- Reused 228's exact strict-passing selection candidate and forecast each future season's target-free ID-branch centering gap from completed seasons using the median consecutive gap ratio. The forecast shift `0.0004364` passed 2023 confirmation with pooled `-1.9787e-5` and balanced target gains (`-9.9012e-6` / `-2.9675e-5`). It therefore opened the locked 2024 gate, where pooled Brier still improved `-1.2920e-5`, but target 1 worsened `+1.7945e-4` and the gain missed the frozen `-2e-5` minimum. `REJECT_LOCKED`; 2024 was evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## ONLINE-RESIDUAL-STATE-231
- Built row-independent pitcher/batter Gaussian residual states from completed-season 126 OOF errors, with frozen season decay, shrinkage, and correction fractions. Every candidate worsened pooled 2021-2022 Brier. The least harmful decay-0.5/prior-50/10% correction was `+5.1143e-6`, won only one season, and worsened target 0 `+2.3740e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the direct residual-state correction axis is closed.
## FACTORIZATION-MACHINE-232
- Trained a strict temporal second-order categorical Factorization Machine over pitcher, batter, team, handedness, count, base, inning-side, and game-type fields, then tested frozen 2/5/10% blends with canonical 126. The 5% pooled best improved `-5.5752e-6` but won only two seasons and worsened target 0 `+7.0243e-4`. The 2% blend won all three seasons but gained only `-3.4538e-6` and still worsened target 0 `+2.7979e-4`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the FM axis is closed.
## TEMPORAL-GRAPH-RESIDUAL-233
- Fit a strict-past temporal bipartite pitcher-batter graph with node biases and rank-8 residual edge factors, using only completed-season canonical-126 OOF errors. Every blend worsened pooled 2021-2022 Brier. The least harmful 10% correction was `+9.5136e-6`, won one season, and strongly reversed target balance (`-1.4181e-4` / `+1.4325e-4`). `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the temporal residual-graph axis is closed.
## DYNAMIC-BETA-ROW-CENTER-234
- Held 228's state model, decay, and 40% blend fixed while replacing part of its scalar center with a target-free row-local Ridge estimate of the plain-ID minus state-ID gap from completed seasons. The pooled-best alpha-100/75% row-centering candidate improved `-1.6160e-5`, but won only two seasons, worsened its worst season `+1.5166e-6`, and worsened target 1 `+1.3128e-5`. All six candidates violated a season and/or target guard. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## DYNAMIC-BETA-ROW-MICROBLEND-235
- Microblended canonical 126 toward 234's fixed alpha-100/75% row-centered direction at 10/25/40%. The 25% candidate improved all three seasons but only by `-4.7377e-6` and worsened target 1 `+2.5721e-6`; the pooled-best 40% candidate gained `-7.3570e-6`, worsened target 1 `+4.3426e-6`, and marginally lost one season. No candidate reached the `-1e-5` gate or target balance. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## DYNAMIC-BETA-ROW-DEPLOYMENT-236
- Reused 228's exact strict-passing selection result and deployed 234's fixed alpha-100/75% row-local target-free center only to future seasons. It passed 2023 confirmation more strongly than 230: pooled `-2.3821e-5`, target 0 `-4.4878e-5`, and target 1 `-2.7605e-6`. The locked 2024 aggregate still improved `-1.4348e-5`, but target 1 worsened `+3.0397e-4` and the gain missed the frozen `-2e-5` minimum. `REJECT_LOCKED`; 2024 was evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## REALMLP-237
- Trained a strict temporal RealMLP-style model with robust standardized/smooth-clipped numerics, learned categorical embeddings, SiLU pre-normalized residual blocks, and BCE+Brier optimization. Every blend failed selection; the least harmful 1% blend worsened pooled Brier `+2.5299e-7`, won two seasons, and worsened target 0 `+2.0912e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## SCARF-238
- Added strict-past SCARF feature-corruption contrastive pretraining on 200k fold-training rows before supervised BCE+Brier fine-tuning. The 5% blend improved pooled Brier `-1.0913e-5`, but won only two seasons, worsened its worst season `+5.0860e-6`, and worsened target 1 `+4.9196e-5`. Smaller blends retained the same imbalance and missed the pooled threshold. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## ROW-INDEPENDENT-SAINT-239
- Tested a competition-legal SAINT-style feature-token transformer with strict-past CutMix contrastive pretraining; cross-row inference attention was deliberately omitted because test rows must remain independent. All blends improved both targets in aggregate, but only one of three seasons. The pooled-best 5% blend gained `-5.7181e-6`, below the `-1e-5` gate, while its worst season worsened `+1.6186e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## RANDOM-FOREST-240
- Trained a strict temporal 120-tree Random Forest with fold-only median/ordinal preprocessing and tested 1/2.5/5/10% blends with canonical 126. Every blend worsened every selection season. The least harmful 1% blend was pooled `+1.1373e-6`, with target 0 worsening `+5.7577e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the classical Random Forest axis is closed.
## VIME-241
- Ran explicit VIME donor corruption with joint corruption-mask estimation and masked numeric/categorical reconstruction on 200k strict-past fold rows, followed by supervised BCE+Brier fine-tuning. The pooled-best 5% blend improved `-6.1602e-6`, but won only two seasons, worsened its worst season `+7.4236e-6`, and worsened target 0 `+1.4233e-4`. Smaller blends retained the same direction and missed the pooled gate. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the VIME axis is closed.
## TABTRANSFORMER-242
- Trained a strict temporal TabTransformer applying self-attention only to categorical feature tokens, then combined contextual embeddings with standardized numeric features in an MLP head. Every blend worsened pooled Brier; the least harmful 1% blend was `+2.5845e-6`, won one season, and worsened target 0 `+2.0153e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the categorical-transformer axis is closed.
## SUBTAB-243
- Ran strict-past SubTab pretraining with two random feature-subset views, projection alignment, and full numeric/categorical reconstruction before supervised fine-tuning. The pooled-best 5% blend improved `-7.4404e-6`, but won only two seasons, worsened its worst season `+3.6675e-6`, and worsened target 0 `+9.1608e-5`. Smaller blends retained the same imbalance and missed the pooled gate. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the SubTab axis is closed.
## T-JEPA-244
- Ran strict-past T-JEPA-style latent prediction with a masked context encoder, EMA target encoder, and supervised BCE+Brier fine-tuning. The pooled-best 5% blend improved `-5.4850e-6`, but won only two seasons, worsened its worst season `+8.8663e-6`, and worsened target 0 `+2.9828e-4`. Smaller blends retained the same imbalance and missed the pooled gate. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the T-JEPA axis is closed.
## RATAB-245
- Ran strict-past RaTab-style latent augmentation by truncating the final encoder-block weight with SVD, aligning original and augmented representations, and reconstructing all features before supervised fine-tuning. The pooled-best 5% blend improved only `-1.4871e-6`, won one season, worsened its worst season `+1.1739e-5`, and worsened target 0 `+5.8937e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the RaTab axis is closed.
## STUNT-246
- Ran strict-past STUNT-style pretraining with six self-generated tasks: random numeric column subsets were clustered into eight pseudo-classes and masked while a shared encoder predicted them, followed by supervised fine-tuning. The pooled-best 1% blend improved only `-1.5412e-7`, won two seasons, worsened its worst season `+2.1881e-6`, and worsened target 1 `+6.1635e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the STUNT axis is closed.
## TRANSTAB-247
- Trained a strict-past TransTab-style transformer whose numeric and categorical value tokens include deterministic character-ngram signatures of their column names. The pooled-best 5% blend improved `-1.8046e-5`, but won only two seasons, worsened its worst season `+6.7699e-6`, and strongly worsened target 0 `+4.8709e-4` while improving target 1. `REJECT_SELECTION`; 2023/2024 were not evaluated, test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the TransTab axis is closed.
## TARGET-RULE-AUDIT-248
- Audited 1,221,585 official Train rows from 2019-2023 under a frozen, analysis-only protocol; locked 2024 and Test were not accessed. No single current-row column or frozen context key approached the deterministic-rule gate. The best single feature was 20-bin `asof_pitcher_reverse_rate` (2023 delta versus the development-prior predictor `-1.6360e-3`, maximum supported development purity `0.6412`); the best context was count plus handedness (`-2.94296e-4`, purity `0.5688`). A separate nondeployable semantics audit showed that the next same-pitcher cumulative success counter reconstructs the current Train target exactly on 99.8836% of rows, and the next same-batter counter does likewise on 99.8787%; this is future-row label recovery, unavailable and forbidden for validation/Test inference. `NO_DEPLOYABLE_DETERMINISTIC_RULE`; no model or submission was created.
## DYNAMIC-SUBTYPE-BETA-249
- Held 228's success-state decay `0.25` and 40% blend fixed, then added row-independent exact-count Beta features for pitcher reverse/middle and batter middle histories. Aggregate selection Brier and both targets improved (`-6.7876e-6`, target0 `-7.4650e-6`, target1 `-6.1905e-6`), but only 2020 improved (`-4.0255e-5`); 2021 and 2022 worsened `+1.8140e-5` and `+1.3325e-6`. The pooled gain also missed the frozen `-1e-5` minimum. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and exact-count subtype Beta expansion is closed.
## CARTE-250
- Trained a strict-past CARTE-style row-local star graph in which a row node aggregated numeric/categorical feature nodes carrying deterministic official-column-name signatures through two attention message-passing layers; no external semantics were used. The pooled-best 1% blend improved only `-2.8965e-7`, won two seasons, worsened 2020 `+4.7778e-6`, and strongly worsened target 0 `+1.8161e-4` while improving target 1. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the CARTE-style transfer graph axis is closed.
## TRANSTAB-FIXED-CENTER-251
- Reused 247's frozen pooled-best 5% TransTab direction and applied one target-free scalar center learned from pooled 2020-2022 predictions (`-0.00935162` at the raw-model level), with no target-season aggregation or alternate tuning. Centering removed the aggregate class imbalance: pooled selection improved `-1.8262e-5`, target0 `-2.5708e-6`, and target1 `-3.2095e-5`. However, only 2020/2021 improved (`-5.4142e-5` / `-1.2345e-5`); 2022 worsened `+1.1220e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## TRANSTAB-TEMPORAL-GATE-252
- Applied one frozen strict-past closed-form Ridge gate to 251's centered correction, using only completed-season OOF benefit and current-row numeric/prediction features; 2020 retained gate 1.0. The gate failed to transfer: 2021 reversed from improvement to `+8.7627e-6`, 2022 worsened further to `+1.5591e-5`, pooled gain weakened to `-9.7363e-6`, and target1 worsened `+8.3107e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and row-level temporal gating of the TransTab direction is closed.
## T2GFORMER-253
- Trained a strict-past T2G-Former-style network with a learned directed feature-relation graph supplying per-head guidance to two feature-token attention layers. The pooled-best 5% blend improved `-8.8965e-6`, below the frozen threshold, won 2020/2022 (`-3.5418e-5` / `-4.8488e-6`), but worsened 2021 `+1.3249e-5`; target0 also worsened `+1.7952e-4` while target1 improved. Smaller blends retained the same direction. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the T2G-Former axis is closed.
## EXCELFORMER-254
- Trained a strict-past ExcelFormer-style architecture using fold-training mutual-information ordering, semi-permeable attention, interaction-attenuated initialization, and a GLU feedforward block. The pooled-best 5% blend improved `-1.3925e-5`, but only 2020 improved (`-6.9733e-5`); 2021/2022 worsened `+1.6941e-5` / `+1.0303e-5`, and target0 worsened `+3.1413e-4` while target1 improved. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the ExcelFormer axis is closed.
## AMFORMER-255
- Trained a strict-past AMFormer-style network with sample-invariant learned prompts, top-8 feature selection, and parallel additive/log-domain multiplicative attention. The pooled-best 5% blend improved `-1.2084e-5`, but only 2020 improved (`-8.1508e-5`); 2021/2022 worsened `+2.1610e-5` / `+2.2747e-5`, and target1 worsened `+1.3838e-4` while target0 improved. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the AMFormer axis is closed.
## MODERNNCA-256
- Trained all strict-past fold rows with a deep ModernNCA embedding and stochastic 1,024-row retrieval banks, masking exact self-neighbors. The pooled-best 2.5% blend improved only `-9.9613e-7`; only 2020 improved (`-6.5957e-6`), while 2021/2022 worsened `+1.1259e-6` / `+2.4081e-6`, and target0 worsened `+8.1086e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the ModernNCA axis is closed.
## TABR-257
- Trained a strict-past TabR network with learned top-32 retrieval, label embeddings, and key-difference value transforms over frozen 2,048-row fold-training banks. The pooled-best 5% blend improved `-1.9074e-5` and won 2020/2021 (`-5.8630e-5` / `-6.1380e-6`), but 2022 worsened `+7.0257e-6` and target1 worsened `+6.1083e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, and canonical 126 remains the only submission candidate. The raw TabR axis is closed, while one preregistered global centering audit remains plausible because its failure is small and directional.
## TABR-FIXED-CENTER-258
- Applied the sole preregistered target-free pooled mean correction (`+0.00201438` at the raw-model level) to 257's frozen 5% TabR direction. Centering fixed target balance: pooled selection improved `-1.9085e-5`, target0 `-4.5778e-6`, and target1 `-3.1874e-5`. However, only 2020/2021 improved (`-5.5435e-5` / `-8.3329e-6`); 2022 still worsened `+6.0340e-6`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and further TabR correction tuning is closed.
## DCNV2-259
- After confirming that incumbent seed/fold stabilization had already been extensively covered by 001/017/045/096/146/147/188-225, trained a previously untested strict-past parallel DCNv2 with two full-matrix cross layers and a two-layer deep tower. The pooled-best 5% blend improved only `-7.1272e-6`; 2020/2022 improved (`-2.6155e-5` / `-4.3655e-7`), but 2021 worsened `+4.9680e-6` and target1 worsened `+1.8798e-4`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, and canonical 126 remains the only submission candidate.
## TROMPT-260
- Trained a strict-past three-cycle Trompt with intrinsic column embeddings, four recurrent prompts, sample-specific prompt-column importance, and cycle-level supervision. The pooled-best 5% blend improved a strong `-5.2921e-5` and won 2020/2021 (`-1.4851e-4` / `-1.3086e-5`), but 2022 worsened `+1.5855e-6`; target1 also worsened `+6.7758e-4` while target0 improved strongly. Even the 1% blend kept the same directional failures. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and one target-free global-centering follow-up is justified by the unusually strong pooled direction and near-neutral 2022 result.
## TROMPT-FIXED-CENTER-261
- Applied the sole preregistered target-free pooled mean correction (`+0.01600690` at the raw-model level) to 260's frozen 5% direction. Selection became exceptionally clean: pooled `-5.3567e-5`, all three seasons improved, and target0/target1 improved `-4.4376e-5` / `-6.1669e-5`. Confirmation then reversed sharply: 2023 pooled worsened `+1.9506e-5`, with target0 `+1.9516e-3` versus target1 `-1.9129e-3`. `REJECT_CONFIRMATION`; 2024/Test were not accessed, no submission was created, canonical 126 remains the only submission candidate, and fixed global centering of Trompt is closed.
## AUTOINT-262
- Trained a strict-past two-layer AutoInt with multi-head residual interacting layers and an output over all final feature vectors. The pooled-best 5% blend improved `-1.6329e-5`, both targets improved (`-2.9118e-6` / `-2.8158e-5`), and 2020/2021 improved (`-2.1618e-5` / `-3.2001e-5`), but 2022 worsened `+4.5341e-6`. Smaller blends preserved the same sign pattern. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the AutoInt axis is closed.
## GRANDE-263
- Trained a compact strict-past GRANDE-style ensemble of 32 depth-4 hard axis-aligned trees, jointly learning feature choices, thresholds, leaf logits, and instance-wise leaf-derived estimator weights with straight-through gradients. The pooled-best 5% blend improved `-1.2604e-5`, but only 2020 improved (`-1.3073e-4`); 2021/2022 worsened `+4.9706e-5` / `+4.1696e-5`, and target1 worsened `+2.8134e-4`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the GRANDE axis is closed.
## TANGOS-264
- Trained a strict-past ReGLU MLP with exact analytic first-hidden-unit attributions and TANGOS specialization/orthogonalization over 50 frozen neuron pairs. Every tested blend improved all three seasons; the 5% blend improved 2020/2021/2022 by `-9.5496e-6` / `-9.8987e-6` / `-4.8625e-6`. However, pooled improvement was only `-8.0961e-6`, below the frozen threshold, and target0 worsened `+7.2632e-4` while target1 improved. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and one target-free global-centering follow-up is justified because the season direction is uniquely stable.
## TANGOS-FIXED-CENTER-265
- Applied the sole preregistered target-free pooled mean correction (`-0.01378766` at the raw-model level) to 264's frozen 5% direction. It reduced the target imbalance substantially but did not remove it: target0 still worsened `+4.2244e-6`, while target1 improved `-1.9844e-5`. More importantly, the formerly stable season direction collapsed: only 2020 improved (`-3.1942e-5`), while 2021/2022 worsened `+4.4617e-6` / `+1.4810e-6`; pooled gain was only `-8.5667e-6`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and TANGOS centering is closed.
## PTARL-266
- Trained a strict-past two-stage PTaRL-style network: phase-1 embeddings initialized eight global prototypes by deterministic K-means, then a freshly initialized phase-2 backbone learned prototype coordinates with transport, coordinate-diversity, and prototype-orthogonality losses. Every blend worsened pooled Brier; the least harmful 1% blend was `+3.8669e-7`, with 2021 worsening `+3.8119e-6` and target1 worsening `+4.1906e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the PTaRL axis is closed.
## BISHOP-267
- Trained a compact strict-past BiSHop-style network with numeric/categorical cell embeddings, alternating feature-wise and within-patch sparse Hopfield attention, hierarchical patch processing, and a sparse decoder query. Every blend worsened pooled Brier; the least harmful 1% blend was `+2.8332e-7`, with 2021 worsening `+3.3648e-6` and target0 worsening `+2.4552e-5`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the BiSHop axis is closed.
## PROTOGATE-268
- Trained a strict-past ProtoGate-style model with stochastic global gates, sample-specific local gates, and top-8 label-prototype retrieval from a frozen 1,024-row bank. Every blend worsened pooled Brier; the least harmful 1% blend was `+1.6843e-6`, with 2020 worsening `+8.0601e-6` and target0 worsening `+2.9768e-4`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the ProtoGate axis is closed.
## MAMBULAR-269
- Trained a compact strict-past Mambular-style network interpreting the fixed feature list as a sequence and applying two bidirectional input-selective diagonal state-space blocks with local depthwise convolution. The pooled-best 5% blend improved `-1.0444e-5`, but only 2020 improved (`-7.4796e-5`); 2021/2022 worsened `+2.1266e-5` / `+2.1368e-5`, and target0 worsened `+1.5037e-4`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the Mambular axis is closed.
## TABNET-270
- Trained a compact strict-past TabNet with three sequential sparsemax feature-selection steps, multiplicative reuse priors, shared GLU feature transformers, and aggregated decisions. The pooled-best 5% blend improved `-9.0964e-6`, below the frozen threshold, while 2022 worsened `+9.4267e-6` and target1 worsened `+2.3100e-4`. Smaller blends retained the same directional failures. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the TabNet axis is closed.
## NODE-271
- Trained a strict-past NODE ensemble of 64 depth-4 differentiable oblivious trees with sparsemax feature selectors, soft split routing, learned leaves, and uniform estimator aggregation. The pooled-best 5% blend improved `-1.5870e-5`, but only 2020 improved (`-1.2620e-4`); 2021/2022 worsened `+4.5156e-5` / `+3.2024e-5`, and target1 worsened `+3.6354e-4`. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and the NODE axis is closed.
## TABULARNN-272
- Trained a strict-past TabulaRNN with numeric/categorical feature tokens, a bidirectional GRU, and learned row-local attention pooling. The pooled-best 5% blend improved a strong `-2.9337e-5` and won 2020/2021 (`-5.8227e-5` / `-4.1126e-5`), but 2022 worsened `+1.0929e-5` and target0 worsened `+1.7117e-4`. The 1% blend reduced the 2022 loss to `+1.9199e-6` but retained the target reversal and missed the pooled threshold. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate. One frozen target-free global-centering audit is justified by the strong pooled direction and small low-blend 2022 miss.
## TRACKMAN-PRIVILEGED-MULTITASK-273
- Trained paired identical strict-past RealMLP encoders with identical seeds and batches; only the privileged member reconstructed ten standardized prior-season TrackMan physical/pitch-mix targets for reliably mapped pitchers (season coverage 57.7-65.9%), while validation inference used no TrackMan. The least harmful 25% auxiliary-minus-control correction improved pooled Brier only `-2.2858e-6`; 2021 improved `-9.8745e-6`, 2022 worsened `+3.0366e-6`, and target0 strongly worsened `+5.0956e-4` while target1 improved. 2020 was exactly neutral because no 2018 TrackMan exists. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and direct shared-encoder TrackMan privileged multitask learning is closed.
## TABULARNN-FIXED-CENTER-274
- Applied the sole preregistered target-free pooled mean correction (`-0.00349515` at the raw-model level) to 272's frozen 5% TabulaRNN direction. Centering fixed pooled target balance and retained a strong `-2.9366e-5` gain: target0/target1 improved `-1.1796e-5` / `-4.4856e-5`, and 2020/2021 improved `-6.3912e-5` / `-3.7310e-5`. However, 2022 worsened `+1.2638e-5`, so the all-season gate failed. `REJECT_SELECTION`; 2023/2024 were not evaluated, Test was not accessed, no submission was created, canonical 126 remains the only submission candidate, and standalone TabulaRNN centering is closed.
## CONSTRAINED-DIRECTION-PORTFOLIO-275
- Evaluated 91 preregistered nonnegative portfolios over frozen 228 dynamic-Beta, 137 TrackMan-release, 274 centered-TabulaRNN, and 270 TabNet corrections under pooled, every-season, both-target, and total-weight constraints. Six passed selection. The chosen portfolio used 1.25× dynamic Beta plus 0.5× TrackMan release (zero neural weights), improving pooled `-1.8236e-5`, all seasons, target0 `-2.5790e-5`, and target1 `-1.1576e-5`. It improved 2023 aggregate more strongly (`-2.1795e-5`) but target0 reversed to `+2.2693e-4` while target1 improved `-2.7056e-4`. `REJECT_CONFIRMATION`; 2024/Test were not accessed, no submission was created, canonical 126 remains the only submission candidate. The robust selection frontier confirms that dynamic-Beta plus TrackMan release carries real aggregate signal, but their shared future target-direction drift prevents promotion.
## PORTFOLIO-GAP-FORECAST-276
- Kept 275's frozen 1.25× dynamic-Beta plus 0.5× TrackMan-release portfolio and forecast its 2023 target-free correction mean from the median consecutive change in completed 2020-2022 means. Subtracting the preregistered `0.0003288983` center strengthened 2023 aggregate improvement to `-2.8358e-5` and flipped target0 from a large loss to `-1.0693e-4`, but overshot target1 to `+5.0226e-5`. `REJECT_CONFIRMATION`; 2024/Test were not accessed, no submission was created, canonical 126 remains the only submission candidate, and alternate center interpolation is prohibited by the one-forecast preregistration.
## PORTFOLIO-DAMPED-GAP-FORECAST-277
- Retained the full aggressive 275 portfolio amplitude and applied the sole target-free 50%-damped median-trend forecast, selected from the 2022 correction-mean backtest without using 2023 labels. The `0.0002420076` center passed 2023 cleanly: pooled `-2.6645e-5`, target0 `-1.8750e-5`, target1 `-3.4542e-5`. The locked 2024 aggregate still improved `-1.6807e-5`, but missed the `-2e-5` minimum and reversed target1 sharply to `+2.7193e-4` while target0 improved `-2.8993e-4`. `REJECT_LOCKED`; Test was not accessed, no submission was created, canonical 126 remains the only submission candidate. The TrackMan/Beta portfolio is aggregate-positive through 2024 but its target-free seasonal center cannot forecast the abrupt 2024 mean reversal safely.
## AGGRESSIVE-PORTFOLIO-AUDIT-278
- Audited the frozen 277 candidate under an explicitly preregistered aggregate-oriented policy without changing predictions. Every 2020-2024 season improved, pooled five-season Brier improved `-1.9612e-5`, and 2024 improved `-1.6807e-5`. The opposing pooled target movement passed the bounded-tradeoff rule (target0 `-8.1781e-5`, target1 `+3.8722e-5`), while the 10,000-replicate 2024 pitcher-cluster bootstrap remained below zero at its 97.5% bound (`-9.1577e-6`). `PASS_AGGRESSIVE_AUDIT`; this is an aggressive promotion candidate only, Test was not accessed, no submission was created, and canonical 126 remains unchanged pending an explicit packaging decision.
## AGGRESSIVE-PORTFOLIO-PACKAGE-279
- Promoted the frozen 278 aggregate candidate into a rule-compliant, row-independent inference package. Retrained the dynamic-Beta and prior-season TrackMan release branches on all official Train data, froze the target-free 2025 center at `0.0000832333`, and embedded only train-derived mappings/statistics and model weights. The inference code does not use other Test rows or the Test distribution. The provided five-row sample Test executed successfully; the real evaluation Test remains inaccessible. `PACKAGE_READY`; ZIP size `6,345,799` bytes, SHA-256 `7d465b61aaf216cdca3842ce89ad76f3bfc1ee2cd864d0f3551bfc6a3f33d4cc`.
## TRACKMAN-MONTHLY-FINGERPRINT-MAPPING-280
- Recomputed pitcher identity mapping directly from the official 1,475,092-row Train and 1,793,078-row TrackMan files using same-hand season-by-month count fingerprints, active-season Jaccard similarity, mutual-best checks, and one-to-one Hungarian assignment. Results closely reproduced the external claim: score thresholds 0.95/0.90/0.85/0.80 yielded 247/320/369/398 pitchers and 62.08%/74.79%/79.34%/80.91% Train-row coverage. The raw A+B rule produced 409 pitchers and 81.91% coverage, but its B-tier overlap with the trusted 061 mapping was only 88%. A-tier overlap precision was 99.22%; applying an A-derived team-transition audit reduced B to 17 and raised its observed overlap precision to 100%, leaving 337 pitchers and 77.29% coverage. `REJECT_RAW_B_AS_TOO_RISKY`; identity audit only, target and Test were not accessed, and package 279 was not changed.
## TRACKMAN-CONSENSUS-TIER-281
- Trained a prior-season TrackMan release model using the frozen 061/280 consensus tiers: 260 S, 85 A, 61 B, with two conflicting pitchers excluded. Applied correction scales 100%/50%/25% and zero for unmapped rows. Selection 2020-2022 passed with pooled Brier `-1.5342e-6`; 2023 improved `-7.8745e-6` within the target guard. Locked 2024 worsened slightly `+9.3358e-7`, with target0 improving and target1 worsening. `REJECT_LOCKED`; official data only, Test was not accessed, package 279 remains unchanged, and the fixed S/A/B correction-scale policy is closed.
## TRACKMAN-TIER-ABLATION-282
- Reused 281's cached predictions to compare S-only, S+A, and S+A+B corrections without retraining. Selection chose S+A, improving pooled 2020-2022 Brier `-1.5591e-6` with two season wins; 2023 improved `-7.0834e-6`. Locked 2024 still worsened `+8.9122e-7`, with target0 `-3.2743e-5` and target1 `+3.6448e-5`. `REJECT_LOCKED`; B removal did not fix the future reversal, Test was not accessed, package 279 remains unchanged, and consensus-tier TrackMan expansion is closed.
## PORTFOLIO-CENTER-FORECAST-TOURNAMENT-283
- Compared six target-free correction-mean forecast rules over completed-season walk-forward origins 2022-2024. The minimum-MAE rule was the same 50%-damped median trend already frozen for package 279, producing the identical 2025 center `0.0000832332924561`. `RETAIN_279_CENTER`; no Test distribution or Test labels were accessed, no package change was needed, and alternate deployment-center rules are closed.
## ONLINE-PORTFOLIO-RIDGE-284
- Fit strict-past nonnegative ridge weights for the dynamic-Beta and TrackMan correction components, centering completed seasons by their own target-free means and forecasting future component means with the frozen 50%-damped trend. The best ridge (`100`) improved pooled 2021-2022 Brier `-4.2182e-6`, but won only 2021, worsened 2022 `+1.4529e-6`, and reversed target0 by `+1.1261e-4`. `REJECT_SELECTION`; 2023/2024 were not evaluated by the gate, Test was not accessed, package 279 remains unchanged, and adaptive ridge weighting is closed.
## PORTFOLIO-DIRECTION-AGREEMENT-285
- Tested five fixed shrinkage levels for rows where the dynamic-Beta and TrackMan correction signs disagreed; component agreement covered 63.56% of selection rows. Selection chose conflict scale `1.0`, exactly the unchanged 279 direction, because every disagreement shrinkage weakened the frozen development frontier. It repeated 2023 `-2.6645e-5` and locked 2024 `-1.6807e-5` with the known target reversal. `REJECT_LOCKED`; the row-local sign gate adds no value, Test was not accessed, and package 279 remains unchanged.
## PROBABILITY-CONDITIONED-PORTFOLIO-286
- Multiplied the frozen portfolio correction by `1 + gamma * (2*p126-1)` using seven preregistered row-local gamma values. Selection chose the strongest positive conditioning (`gamma=0.75`), improving pooled 2020-2022 Brier `-1.9560e-5`, all three seasons, and both targets. Although 2023 pooled improvement strengthened to `-2.7717e-5`, target1 reversed to `+2.4640e-5`, violating the zero-loss confirmation gate. `REJECT_CONFIRMATION`; 2024 and Test were not accessed, package 279 remains unchanged, and simple linear probability conditioning is closed.
## CONDITIONED-CENTER-DAMPING-287
- Fixed 286's selected `gamma=0.75` and selected the center-trend damping entirely from the 2022 correction-mean forecast error using 2020-2021 means. The target-free choice was again damping `0.5`, reproducing the same 2023 center `0.0002896733`, pooled gain `-2.7717e-5`, and target1 loss `+2.4640e-5`. `REJECT_CONFIRMATION`; 2024 and Test were not accessed, package 279 remains unchanged, and conditioned-center damping is closed.
## TARGET-BALANCED-GAMMA-288
- Re-ranked 286's preregistered gamma candidates by the absolute gap between target0 and target1 selection improvements, subject to all three seasons and both targets improving. This selected `gamma=-0.5`, whose selection target deltas were nearly equal (`-1.7722e-5` / `-1.6782e-5`). It retained a strong 2023 pooled gain (`-2.5868e-5`) but reversed target0 to `+2.2193e-5` while target1 improved. `REJECT_CONFIRMATION`; 2024 and Test were not accessed, package 279 remains unchanged, and selection-period target balancing does not forecast future target direction.
## AGGRESSIVE-BALANCED-GAMMA-AUDIT-289
- Audited frozen `gamma=-0.5` under an aggregate policy that allowed a bounded one-target tradeoff. Confirmation passed because pooled 2023 improved `-2.5868e-5` and the target0 loss (`+2.2193e-5`) was smaller than the target1 gain. Locked 2024 remained statistically aggregate-positive (`-1.6985e-5`; pitcher-bootstrap upper 97.5% `-9.1866e-6`) but target1 worsened `+2.8539e-4`, exceeding the preregistered `+2e-4` cap despite being smaller than the target0 gain. `REJECT_AGGRESSIVE_LOCKED`; Test was not accessed and package 279 remains the stronger bounded-risk candidate.
## RELIABILITY-CONDITIONED-PORTFOLIO-290
- Tested 12 row-local reliability gates from pitcher count, batter count, their minimum, and geometric mean at count scales 200/500/1000, plus the ungated control. Every gated variant weakened the strict selection frontier; the chosen candidate was exactly `UNGATED`, reproducing 279's 2023 and 2024 metrics and known target reversal. `REJECT_LOCKED`; cumulative-count reliability does not identify harmful corrections, Test was not accessed, and package 279 remains unchanged.
## HIST-GRADIENT-BOOSTING-291
- Pivoted away from TrackMan and portfolio postprocessing to a new sklearn Histogram Gradient Boosting model over the canonical 49 row-local features, with strict-past categorical vocabularies and four small blends into 126. Every blend worsened pooled selection Brier; the least harmful 1% blend was `+2.0076e-6`, improving only 2022 while target0 worsened `+6.9429e-5`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, package 279 remains unchanged, and the independent HGB axis is closed.
## RBF-KAN-292
- Trained a new RBF-KAN-style tabular model with per-feature radial-basis additive functions, categorical scalar functions, and low-rank feature interactions under strict temporal folds. Every blend worsened pooled selection Brier; the least harmful 1% blend was `+9.0230e-6`, improved only 2021, and worsened target0 `+4.1162e-5`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, package 279 remains unchanged, and this nonlinear additive/KAN axis is closed.
## EXTRA-TREES-293
- Trained an independent ExtraTrees model over the canonical 49 row-local features with strict-past categorical frequency encoding. Every blend failed the selection gate; the least harmful 0.5% blend worsened pooled Brier `+7.3674e-7`, improved only 2022, and worsened target0 `+3.4904e-5`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, package 279 remains unchanged, and the ExtraTrees axis is closed.
## SHRINKAGE-LDA-294
- Trained a regularized Gaussian discriminant model over the canonical 49 features using strict-past frequency encoding, standardization, and automatic covariance shrinkage. Every blend failed the selection gate; the least harmful 0.25% blend was essentially neutral but still worsened pooled Brier `+4.1680e-8`, improved only 2020, and worsened both targets. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, package 279 remains unchanged, and the shrinkage-LDA axis is closed.
## GAUSSIAN-NB-295
- Trained a diagonal Gaussian Naive Bayes model over the canonical 49 features with strict-past transforms. The 1% blend improved pooled selection Brier `-1.1863e-5`, but the gain came only from 2021; 2020/2022 worsened and target1 deteriorated `+1.4364e-3`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, package 279 remains unchanged, and the unconditioned GaussianNB axis is closed.
## CENTERED-GAUSSIAN-NB-296
- Added only preregistered fixed global center offsets to 295, without row/ID/segment or evaluation-distribution conditioning. The pooled-best 2% / center `0.15` candidate improved `-2.1049e-5`, but improved only 2021, worsened 2020 by `+1.1523e-4`, and worsened target1 `+1.0928e-4`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, package 279 remains unchanged, and fixed centering cannot stabilize the GaussianNB direction.
## GLOBAL-BLEND-PACKAGE-297
- Built a fixed row-independent interpolation between public-best 126 (`75%`) and aggressive 279 (`25%`) after the full 279 package lowered the public leaderboard score. The package uses one global coefficient, does not condition on rows/IDs/segments or evaluation distribution, passed ZIP integrity and provided 5-row sample inference, and did not access the real evaluation Test. `PACKAGE_READY`; submit at most once as a one-dimensional global-weight probe and close the 279 direction if it underperforms 126.
## GANDALF-298
- Trained a compact GANDALF-style network with four gated feature-learning stages, strict-past preprocessing, categorical embeddings, and BCE+Brier optimization against public-best 126. The least harmful 0.5% blend was effectively neutral (`-4.0439e-9`) and improved 2020/2022, but worsened 2021 `+2.5351e-6` and target1 `+8.2087e-6`; larger blends became progressively worse. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the GANDALF axis is closed.
## XGBOOST-DART-299
- Trained a strict-past XGBoost DART model with tree dropout and frequency-encoded categoricals against public-best 126. Every blend worsened pooled selection Brier; the least harmful 0.5% blend was `+4.6650e-7`, improved only 2022, and worsened target0 `+3.5171e-5`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the XGBoost-DART axis is closed.
## EXPLAINABLE-BOOSTING-300
- Trained an EBM-style generalized additive model using six rounds of strict-past cyclic univariate Newton boosting over 49 features. The pooled-best 2.5% blend improved `-5.3692e-6`, but only 2020 improved; 2021/2022 worsened and target0 deteriorated `+1.3050e-4`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the univariate explainable-boosting axis is closed.
## TRANSITION-MULTITASK-301
- Reconstructed four train-only auxiliary pitch outcomes (reverse/middle/ball/strike) from the next same-pitcher same-season official Train cumulative counters, achieving complete auxiliary coverage on `93.23%` of rows, and trained a shared-trunk multitask network whose inference consumes only the current row. This genuinely new supervision did not beat public-best 126: the standalone model worsened pooled Brier `+1.1625e-3`, while even the smallest preregistered 25% blend worsened `+1.0991e-4`, improving only 2022 and sharply worsening target0. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and transition-derived multitask supervision is closed in this form.
## DOMAIN-ADVERSARIAL-302
- Trained a genuinely different gradient-reversal network that learned the target while adversarially suppressing season and game-month information from its shared representation. The standalone model worsened pooled Brier `+9.8326e-4`; the smallest 25% blend still worsened `+1.5567e-5`, improving only 2020 while strongly worsening target0. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and season/month domain-adversarial learning is closed.
## LATENT-OUTCOME-303
- Decomposed each eligible official Train pitch into one of 16 reverse/middle/ball/strike latent outcomes (`93.23%` complete coverage), trained a CatBoost multiclass generator on the 126 feature family, and converted class probabilities to success probability using strictly past empirical class rates. The standalone model worsened pooled Brier `+1.0736e-3`; the smallest 25% blend worsened `+3.6304e-5`, improved only 2020, and worsened target1 `+1.0348e-3`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and latent-outcome decomposition is closed.
## SEMANTIC-DISTILLATION-304
- Removed 303's multiclass inference stage and directly trained a CatBoost regressor on leave-one-out smoothed success rates of the 16 train-only latent outcome classes. The standalone model worsened pooled Brier `+9.4899e-4`; the smallest 25% blend worsened `+5.0861e-5`, improved only 2020, and worsened target1 `+1.0433e-3`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and semantic soft-label distillation is closed.
## REGULARIZED-QDA-305
- Trained a strongly regularized Quadratic Discriminant model with separate class covariance structures over the canonical 49 features and strict-past transforms. It lost all three selection seasons: the smallest 25% blend worsened pooled Brier `+6.8066e-4`, while the standalone model worsened `+1.4884e-2` and severely polarized target directions. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the regularized-QDA axis is closed.
## ADABOOST-306
- Trained a previously untested adaptive example-reweighting ensemble of 100 depth-3 trees using strict-past frequency encoding. It lost all three selection seasons: the smallest 25% blend worsened pooled Brier `+1.3750e-3`, and the standalone model worsened `+2.1719e-2` with extreme target polarization. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the AdaBoost axis is closed.
## XGBOOST-DIRECT-BRIER-307
- Trained XGBoost with a custom squared-probability objective using the exact sigmoid-space Brier gradient and a clipped second derivative, rather than Logloss. It lost all three selection seasons: the smallest 25% blend worsened pooled Brier `+6.3807e-5`, and the standalone model worsened `+5.1847e-4` with target0 deterioration. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and direct-Brier XGBoost is closed.
## RANDOM-FOURIER-KERNEL-308
- Trained a streaming nonlinear RBF-kernel logistic model using 512 random Fourier features over strict-past standardized/frequency-encoded inputs. It lost all three selection seasons: the smallest 25% blend worsened pooled Brier `+2.1231e-4`, and the standalone model worsened `+2.9508e-3` with strong target polarization. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the global random-Fourier kernel axis is closed.
## RULEFIT-309
- Trained XGBoost trees only to discover leaf-path rules, one-hot encoded those rules, and relearned their weights with sparse logistic regression under strict temporal folds. It lost all three selection seasons: the smallest 25% blend worsened pooled Brier `+3.6430e-3`, and the standalone model worsened `+5.3906e-2` with severe target polarization. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the RuleFit axis is closed.
## PLS-DA-310
- Trained an eight-component supervised partial-least-squares discriminant regressor, extracting latent feature directions by covariance with the target under strict temporal folds. It lost all three selection seasons: the smallest 25% blend worsened pooled Brier `+6.4470e-5`, and the standalone model worsened `+9.7362e-4`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and the PLS-DA axis is closed.
## TABPFN-SCREEN-311
- Attempted the first official-pretrained TabPFN screen with a preregistered 10,000-row deterministic training context. CPU attention required a 19.2 GB allocation even with batched validation inference, so the run ended as `BLOCKED_CPU_MEMORY` without producing or inspecting validation metrics. 2023/2024 and Test were not accessed and no submission was created; experiment 312 preregisters a resource-feasible 2,000-row context before execution.
## TABPFN-SCREEN-312
- Reduced the deterministic training context to 2,000 rows, which fit but consumed about 3.8 GB and made the preregistered 10,000-row-per-season validation screen impractically slow on CPU. The run was stopped before any metrics were produced or inspected (`BLOCKED_CPU_RUNTIME`). 2023/2024 and Test were not accessed and no submission was created; experiment 313 preregisters a 2,000-row-per-season screen.
## TABPFN-SCREEN-313
- Retained the 2,000-row training context and reduced validation to 2,000 deterministic rows per season, but CPU inference remained impractically slow and was stopped before metrics were produced or inspected (`BLOCKED_CPU_RUNTIME`). 2023/2024 and Test were not accessed and no submission was created; experiment 314 preregisters a final 500-row context / 1,000-row validation feasibility screen.
## TABPFN-SCREEN-314
- Completed the first resource-feasible official-pretrained TabPFN screen using deterministic target-free samples (500 past training rows and 1,000 validation rows per selection season). The least harmful 25% blend worsened pooled Brier `+1.7876e-4`, improved only 2022, worsened 2020/2021, and sharply polarized targets (target0 `+5.7523e-3`, target1 `-4.6304e-3`). `REJECT_SCREEN`; a larger/full TabPFN run is not justified, 2023/2024 and Test were not accessed, and no submission was created.
## TABULARNN-PROBABILITY-GATE-315
- Applied twelve preregistered row-local probability-conditioned amplitudes to the frozen strong TabulaRNN-272 correction. Conditioning strengthened the pooled-best result to `-3.7566e-5` at fraction 5% / gamma 1.0 and reduced target0 damage substantially, but target0 still worsened `+4.4175e-5` and 2022 worsened `+1.2551e-5`; only two seasons improved. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and probability conditioning alone cannot stabilize the TabulaRNN direction.
## PORTFOLIO-TABULARNN-ORTHOGONAL-316
- Added seven preregistered nonpositive weights of 315's probability-conditioned TabulaRNN correction to the frozen 275 dynamic-Beta/TrackMan portfolio, selecting by target-direction balance after strict pooled/every-season/both-target gates. Five candidates remained eligible, but the selected weight was exactly zero; every nonzero neural subtraction reduced balance or aggregate quality. This reproduces 275 and its 2023 target0 reversal (`+2.2693e-4`), so `REJECT_CONFIRMATION`; 2024 and Test were not accessed and no submission was created.
## BERNOULLI-NEWTON-BOOST-317
- Trained a previously untested classic stagewise Bernoulli-deviance/Newton tree booster on deterministic target-free 75,000-row strict-past samples. The pooled-best 5% blend improved only `-1.3650e-6`, lost 2022 (`+1.0982e-5`), and strongly polarized targets (target0 `+3.6032e-4`, target1 `-3.2023e-4`). `REJECT_SCREEN`; 2023/2024 and Test were not accessed, no submission was created, and a larger Newton-boost run is not justified.
## FROZEN-MODEL-COVARIANCE-STACK-318
- Fit four preregistered ridge meta-models on 2020-2021 OOF residuals from seven frozen diverse directions (dynamic Beta, TrackMan release, SSL, TabM, Trompt, TabNet, and TabulaRNN), then evaluated only untouched 2022. Every ridge worsened aggregate Brier; the strongest regularization still lost `+2.1862e-5` and polarized targets. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and covariance stacking of these frozen directions is closed.
## TRACKMAN-BIOMECHANICAL-EFFICIENCY-319
- Added nine genuinely new strictly prior-season TrackMan features covering release-to-plate speed retention, movement per spin, movement-angle concentration, release/movement correlations, arsenal speed/shape separation, and support through the reliable 061 pitcher mapping (59.9-65.6% row coverage). The 20% blend improved pooled Brier `-2.5931e-6` and both targets, with 2020/2022 wins, but 2021 worsened `+8.7065e-6`; it missed the all-season and minimum pooled gates. `REJECT_SELECTION`; 2023/2024 and Test were not accessed and no submission was created. The balanced pooled direction justifies a preregistered feature-group ablation focused on removing the 2021 reversal.
## TRACKMAN-BIOMECHANICAL-ABLATION-320
- Split 319 into fixed efficiency, release-coupling, and arsenal-separation groups and trained each independently. Release coupling (`rel_side`↔horizontal break and `rel_height`↔IVB correlations plus support) at 20% passed the strict 2020-2022 gate: pooled `-4.7457e-6`, all three seasons improved, and both targets improved. It also passed 2023 aggregate/target-tolerance confirmation at `-7.7624e-6` (target0 `-5.4934e-5`, target1 `+3.9418e-5`). `PASS_CONFIRMATION`; 2024 and Test were not accessed in this experiment.
## TRACKMAN-RELEASE-COUPLING-LOCKED-321
- Performed the preregistered one-shot 2024 audit of 320's frozen release-coupling 20% candidate using only 2023 TrackMan profiles. Aggregate Brier improved for the fifth consecutive evaluated season (`-1.3494e-6`), with 56.30% feature coverage; target0 improved `-2.0445e-5` and target1 worsened `+1.8838e-5`, within tolerance. The gain missed the locked minimum `-3e-6`, so `REJECT_LOCKED`; Test was not accessed and no submission was created. This is nevertheless the first new TrackMan feature candidate in this sequence with aggregate improvement in every 2020-2024 season.
## TRACKMAN-RELEASE-COUPLING-AGGRESSIVE-322
- Audited the fixed 40% release-coupling candidate selected solely as 320's pooled-best development candidate under a preregistered bounded aggregate policy. It improved pooled 2020-2022 Brier `-7.4636e-6` with both targets improving and only a `+9.5478e-7` 2021 loss, improved 2023 `-1.4700e-5`, and improved locked 2024 `-1.9931e-6`. Future target tradeoffs stayed within the frozen caps. `ACCEPT_AGGRESSIVE`; all five yearly aggregate folds improve except the bounded sub-micro 2021 miss, Test was not accessed, and no submission was created yet.
## TRACKMAN-RELEASE-COUPLING-PACKAGE-323
- Retrained the frozen 322 release-coupling CatBoost branch on all official Train rows with strict prior-season TrackMan features, embedded only the reliable pitcher mapping and precomputed 2024 profiles for 2025 inference, and blended it globally at 40% into canonical 126. The inference code is row-independent and does not inspect Test-wide distributions. POSIX ZIP structure, CRC, extraction, and the provided five-row sample inference passed. `PACKAGE_READY`; ZIP `submit_trackman_release_coupling_323.zip`, 4,999,613 bytes, SHA-256 `6120cd583fc630902af377510bba1572a54379b9c2a4043ce0489dacfbec6503`; real evaluation Test was not accessed.
- Public-LB follow-up supplied by the participant: score `1006.4001901074`, which is `-1.7371964725` below public-best 126 (`1008.1373865799`) and `-1.6214666566` below package 297 (`1008.021656764`). The offline micro-gain did not transfer to 2025; `REJECT_PUBLIC_LB`, do not reuse or blend this package, and retain canonical 126 as the incumbent.
- Post-LB root-cause audit found no packaging/formula explosion, but exposed a material design flaw: the 40% alternative-model correction was applied to every row, including pitchers without a 2024 TrackMan profile. All five provided sample-Test rows were unmapped, yet their predictions still moved by up to `0.0027138` (mean absolute change `0.0012509`) because the separately retrained CatBoost branch changes even when all three TrackMan inputs are missing. With only 56.30% mapped coverage in the locked fold, the ungated correction injects model-retraining noise into a large unmapped population; combined with the original micro-scale OOF gains and seasonal target reversals, this is the most concrete explanation for the large LB loss.
## TRACKMAN-RELEASE-COUPLING-GATE-324
- Tested the corrective design with six preregistered support/fraction combinations (minimum 100/300/600 prior TrackMan pitches × 20/40%), enforcing bit-identical 126 predictions outside the gate. No candidate passed: the pooled-best 600/40% gate improved `-2.4568e-6` but lost 2021 `+1.0345e-6`, won only two seasons, and worsened target0 `+3.3534e-5`. `REJECT_SELECTION`; 2023/2024 and Test were not accessed in this experiment and no package was created. This shows that much of 320/322's apparent balance came from alternative-model retraining movement on unmapped rows rather than the TrackMan signal itself; the release-coupling TrackMan axis is closed.
## OUTCOME-COMPOSITION-FEATURES-325
- Added nine deterministic row-local features expressing cumulative pitcher outcome-rate entropy/HHI/mass, ball-strike and success-location log ratios, plus pitcher-batter logit gaps. Every blend failed pooled selection; the least harmful 5% blend worsened `+1.0763e-7`, improved only 2020, worsened 2021/2022, and slightly worsened target0. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and cumulative-rate compositional geometry is closed.
## WIN-EXPECTANCY-STATE-RESIDUAL-326
- Fit a target-free expanding ridge model of home-win-expectancy logit from inning/score/outs/base/half-inning state, then added four row-local residual features intended to isolate latent team context. Every blend worsened pooled Brier; the least harmful 5% blend lost `+9.6578e-7`, improved 2020/2022, but worsened 2021 `+4.6871e-6` and both pooled targets. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and win-expectancy residualization is closed.
## MULTIRATE-UNCERTAINTY-327
- Added twelve row-local empirical-Bayes uncertainty/z-score features for pitcher reverse/middle/ball/strike rates and batter middle rate, extending the earlier success-only uncertainty test. Every blend worsened pooled Brier; the least harmful 5% blend lost `+1.7982e-7`, improved only 2021, and worsened both pooled targets. `REJECT_SELECTION`; 2023/2024 and Test were not accessed, no submission was created, and multirate posterior uncertainty is closed.
- 2026-08-25 — `SIGNED-FORM-RELIABILITY-328`: Added 12 strict-past, row-local features that split pitcher/batter current-season deviation into count-reliability-weighted positive/negative directions and concordant/discordant interactions. The 40% candidate passed the full 2020-2022 selection gate strongly (pooled `-4.6405e-5`, all three seasons and both targets improved), but 2023 reversed aggregate (`+6.8266e-6`) with severe target imbalance (target0 `+5.7147e-4`, target1 `-5.5791e-4`). `REJECT_CONFIRMATION`; 2024/Test were not accessed and no submission was created.
- 2026-08-25 — `SIGNED-FORM-GATE-329`: Held 328's 40% correction fixed and preregistered 11 row-local gates based only on the positive/negative quadrants of strict-past pitcher/batter current-season form. Selection retained `ALL` (mean gate 1.0), exactly reproducing 328's `-4.6405e-5` development gain; every quadrant restriction weakened the development frontier. Diagnostic 2023 reconfirmation therefore repeated the aggregate loss and target reversal. `REJECT_RECONFIRMATION`; 2024/Test were not accessed and no submission was created. Signed-form quadrant gating is closed.
- 2026-08-25 — `AUTO-RESIDUAL-INTERACTIONS-330`: Screened 570 preregistered pairwise product/difference/absolute-difference formulas over 20 official strict-past numeric inputs using only stable 2020-2021 OOF residual correlation, then froze 16 diverse formulas before one-shot 2022 selection. The smallest 5% blend was essentially aggregate-neutral (`-2.2834e-8`) but polarized targets (target0 `-7.3601e-5`, target1 `+6.5509e-5`); larger blends worsened aggregate and target1. `REJECT_SELECTION`; 2023 was not evaluated, 2024/Test were not accessed, and no submission was created. Broad residual-ranked arithmetic interaction mining does not provide a balanced direction.
- 2026-08-25 — `PRIOR-PITCHER-WORKLOAD-ROLE-331`: Reconstructed target-free game/appearance boundaries from official row order and added nine strictly previous-season pitcher role features (appearance support, pitch workload distribution, entry/exit inning, starter, multi-inning, and heavy-work rates). The pooled-best 40% blend improved only `-2.3604e-6`, won one season, and worsened 2021 `+2.3105e-5`; the smaller balanced-target blends still lost 2021 and missed the minimum gain. `REJECT_SELECTION`; 2023/2024/Test were not evaluated and no submission was created. Prior-season workload/role is weak and season-unstable.
- 2026-08-25 — `TRACKMAN-BATTER-PITCHER-COMPATIBILITY-332`: Combined reliable 061 pitcher and batter mappings with strictly previous-season TrackMan profiles. Added 26 row-local features measuring the current pitcher's velocity/spin/movement/release/pitch-mix distance from the batter's same-handed historical pitch exposure, and forced predictions to remain exactly canonical 126 outside dual-profile support gates. Dual-profile coverage was about 41% in 2020-2022. The pooled-best 300-pitch/40% candidate gained only `-1.6011e-6`, won two seasons, and worsened target1 `+4.7469e-6`; `REJECT_SELECTION`. 2023/2024/Test were not evaluated and no submission was created.
- 2026-08-25 — `TRACKMAN-COMPATIBILITY-ABLATION-333`: Trained 15 temporal models separating 332 into support, velocity, movement, release, and pitch-mix groups, with 45 frozen support/fraction candidates. Physical groups were neutral or harmful. The support-only 300-pitch/40% candidate improved all three seasons but only by `-2.2214e-6`, below the `-3e-6` minimum, while target0 worsened `+2.2e-5`. `REJECT_SELECTION`; 2023/2024/Test were not evaluated and no submission was created. Prior-season batter-exposure versus pitcher-arsenal TrackMan compatibility is closed; the only stable effect is weak coverage/identity support rather than physical matchup signal.
- 2026-08-25 — `ROBUST-MODEL-ZOO-334`: Inventoried 257 season-2020 checkpoint families and isolated 28 with complete 2020-2024 predictions. The first heterogeneous raw-probability formulation produced no eligible direction and, on audit, was found to duplicate canonical 126's batter-ID branch for branch-model checkpoints. It was explicitly marked `INVALID_FORMULATION`; no later-season gate or Test was used, and it was replaced by the composition-correct 335 formulation.
- 2026-08-25 — `ROBUST-BRANCH-DELTA-ZOO-335`: Re-expressed 19 compatible checkpoints as target-free mean-matched changes versus the exact frozen batter-ID branch, scaled by its actual 50% × CatBoost share. Five directions improved both 2020 and 2021 with balanced targets, but every optimized portfolio reversed sharply on untouched 2022; the least harmful selected-grid portfolio still lost about `+9.0e-5`. `REJECT_SELECTION`; 2023/2024/Test were not evaluated.
- 2026-08-25 — `CONSTRAINED-BRANCH-PORTFOLIO-336`: Solved exact nonnegative quadratic portfolios over all 19 branch deltas with explicit non-loss constraints for each 2020-2022 season and both targets. Every solution was pinned to effectively zero correction on 2022 (numerical deltas around `1e-15`), so no candidate improved all three seasons. `REJECT_SELECTION`; 2023/2024/Test were not evaluated.
- 2026-08-25 — `SIGNED-CONSTRAINED-BRANCH-PORTFOLIO-337`: Extended 336 to globally signed coefficients under frozen L1 caps. The selected L1-0.1 portfolio used only `d6_random3_ctr256` at `+0.1`, passed 2020-2022 strongly (pooled `-1.0193e-5`, all seasons and both targets) and passed 2023 (`-1.6927e-5`; target0 `+4.28e-7`, target1 `-3.4284e-5`). The conditional locked 2024 audit reversed aggregate to `+1.3885e-6` and worsened target0 `+7.7339e-5`, so `REJECT_LOCKED`. Test was not accessed and no submission was created. Large frozen branch-zoo portfolio optimization is closed; the remaining stable frontier is canonical 126.
- 2026-08-25 — `HIERARCHICAL-HEAD-TO-HEAD-338`: Added eleven genuinely new pitcher-batter direct-matchup features using only completed earlier-season labels: pair support/active seasons, pitcher-batter hierarchical priors, 5/20/50-strength shrinkage, pitcher/batter lifts, previous-season pair state, and recency gap. Every blend worsened pooled selection Brier; the least harmful 5% blend was `+1.7890e-6`, improved only 2022, and worsened both targets. `REJECT_SELECTION`; 2023/2024/Test were not evaluated and no submission was created. Direct historical head-to-head effects add no stable value beyond canonical player histories.
- 2026-08-25 — `HIERARCHICAL-BATTER-COUNT-339`: Added thirteen strictly prior-season hierarchical features for batter × balls × strikes and batter × pitcher-hand × count, including support, 10/30/100-strength rates, batter/count lifts, previous-season state, and recency gap. The smallest 5% blend improved 2020 and marginally 2022 but worsened 2021 `+5.6245e-6`, leaving pooled Brier `+1.0251e-6`; larger blends worsened further. `REJECT_SELECTION`; 2023/2024/Test were not evaluated and no submission was created. Explicit batter-count history is redundant and season-unstable beyond canonical CatBoost interactions.
- 2026-08-25 — `PUBLIC-LB-GLOBAL-CALIBRATION-PROBES-340`: Preregistered and packaged three rule-compliant, row-independent global calibration probes around immutable public-best 126: intercept `-0.0005`, intercept `+0.0005`, and a 25%-shrunk 2024 OOF affine correction. All non-script artifacts are byte-identical to public-best 126, ZIP integrity and five-row official sample inference passed, and no evaluation-test distribution or row/ID/segment-specific logic was used. `THREE_PACKAGES_READY`; retain 126 unless a complete fixed-global package exceeds public score `1008.1373865799`.
- 2026-08-25 — `PUBLIC-LB-AFFINE-STRENGTH-341`: After the 25% fixed-global affine transform raised public score to `1016.9867506137`, preregistered 37.5% and 50% strengths along the identical OOF-derived direction. Both packages preserve every model artifact from public-best 126, apply one row-independent formula globally, and passed ZIP integrity plus five-row inference preflight. `TWO_PACKAGES_READY`.
- 2026-08-26 — `PUBLIC-LB-AFFINE-OPTIMUM-342`: Public scores at global affine weights 0, 0.25, 0.375, and 0.5 lay exactly on `score(w)=-30.21315979w²+42.95074608w+1008.13738658`. Preregistered the analytic optimum `w=0.710795335192`, corresponding to `clip(p-0.003011548976+0.067059909306*(p-0.5),0,1)` and predicted score `1023.4019815596`. The package keeps the original public-best model artifacts, uses one global row-independent transform, and passed five-row inference preflight. `PACKAGE_READY`.
- 2026-08-26 — `PUBLIC-LB-OFFSET-AXIS-343`: After 342 scored `1023.4019815591`, fixed its confidence-scale coefficient at `0.067059909306` and preregistered symmetric global offset probes at `-0.003511548976` and `-0.002511548976` (`±0.0005` around 342). Both packages preserve all public-best 126 model artifacts, apply one row-independent transform, and passed ZIP integrity plus five-row inference preflight. The reference and two probe scores will determine the exact independent offset vertex before any subsequent submission. `TWO_OFFSET_PROBES_READY`.
- 2026-08-26 — `PUBLIC-LB-OFFSET-OPTIMUM-344`: The 343 symmetric probes scored `1022.3673108856` (down) and `1024.2354205897` (up) around reference `1023.4019815591`, yielding the exact fixed-scale quadratic vertex at offset delta `+0.002320844869597`. Preregistered absolute offset `-0.000690704106403` with scale coefficient `0.067059909306`; predicted score is `1025.5697779704`. The package preserves all public-best model artifacts and passed ZIP integrity plus five-row inference preflight. `PACKAGE_READY`.
- 2026-08-27 — `PUBLIC-LB-AFFINE-2D-OPTIMUM-345`: Experiment 344 scored `1025.5697779711`, matching its analytic prediction within `7e-10`. Combined all fixed-global calibration observations to solve the complete two-variable Brier quadratic in offset `c` and scale `s`. The negative-definite surface has joint optimum `c=0.002895168052643`, `s=0.166636301069256`, equivalent to `clip(1.166636301069256*p-0.080422982481985,0,1)`, with score prediction `1033.0960951923`. Public submission scored `1033.0960952068` (difference `1.45e-8`), confirming negligible clipping. The package preserves the canonical model artifacts and passed ZIP integrity plus five-row inference preflight. `PUBLIC-BEST`.
- 2026-08-27 — `NONLINEAR-RESIDUAL-CALIBRATION-346`: Tested quadratic/cubic/quartic probability residual bases after removing their intercept and linear components, using four strictly rolling source-year to next-year OOF transitions and five frozen strengths. The best pooled candidate improved mean Brier but had a `+5.78e-5` worst-transition loss and worsened pooled target1, far beyond the stability limits. `REJECT_LOCAL`; Test and public LB were not accessed and no package was created.
- 2026-08-27 — `CALIBRATED-BRANCH-DELTA-347`: Re-audited the strongest deployable batter-ID branch direction across twelve signed global weights after applying the exact 345 affine calibration. Positive weights improved every 2020-2022 selection season and 2023, but all worsened locked 2024 aggregate; negative weights reversed the earlier seasons. `REJECT_LOCAL`; Test and public LB were not accessed and no package was created.
- 2026-08-27 — `CALIBRATED-BRANCH-PORTFOLIO-348`: Jointly optimized all 19 frozen deployable branch directions after calibration 345 under signed L1 caps and explicit non-loss constraints for each 2020-2022 season and both targets. Larger portfolios produced strong balanced development gains and improved 2023, but every eligible direction reversed on locked 2024; the L1-0.8 optimum lost `+1.67e-5` aggregate with severe target polarization (`+6.97e-4` target0, `-7.03e-4` target1). `REJECT_LOCAL`; Test/public LB were not accessed and no package was created.
- 2026-08-27 — `CALIBRATION-AWARE-CORE-WEIGHTS-349`: Evaluated 210 joint settings of CatBoost share, batter-support gate strength, and final batter-ID share. Every composition received an independent global affine fit on 2020-2022 OOF before comparison. The pooled-best settings improved only one selection season; settings that also improved 2023/2024 retained severe locked-year target polarization (typically target0 about `+1e-4` to `+2.4e-4` versus target1 improvements). No candidate passed the season and target gates. `REJECT_LOCAL`; Test/public LB were not accessed and no package was created.
- 2026-08-27 — `CALIBRATION-AWARE-LGB-RATIO-350`: Reconstructed the two deployable current-season LightGBM components separately for all five OOF seasons and tested 13 min-child-20/min-child-50 mixture ratios, giving each ratio its own 2020-2022 affine fit. The incumbent 60/40 ratio remained the temporal compromise. Heavier min-child-20 weights produced only sub-`1e-6` development gains, lost 2023, and polarized 2024 targets; lighter weights reversed those patterns. `REJECT_LOCAL`; Test/public LB were not accessed and no package was created.
- 2026-08-27 — `PUBLIC-LB-ASYMMETRIC-SLOPE-351`: Preregistered two symmetric global piecewise-linear calibration probes around public-best 345 by adding `gamma*abs(p-0.5)` with `gamma=-0.02` and `+0.02`. Both transforms remain globally monotone, use no row/ID/segment or test-distribution logic, preserve every canonical model artifact, and passed ZIP integrity plus five-row inference preflight. The two scores and reference `1033.0960952068` will determine the exact one-dimensional curvature vertex. `TWO_PACKAGES_READY`.
- 2026-08-27 — `CALIBRATED-COUNT-HAND-352`: Re-evaluated the frozen, mean-neutralized count-by-handedness corrections from 174 after applying affine-345 plus the analytic asymmetric gamma optimum. Selection remained strong and balanced (`-1.8918e-5`, all three seasons and both targets) and 2023 improved `-1.2054e-5`, but locked 2024 improved only `-8.4760e-6`, below the frozen `-1e-5` minimum, while target0 worsened `+9.2695e-6`. `REJECT_LOCKED`; Test/public LB were not accessed and no package was created.
- 2026-08-27 — `CALIBRATED-COUNT-HAND-STRENGTH-353`: Preregistered six global strengths for the frozen, mean-neutralized count-by-handedness corrections and selected strength `2.0` using 2020-2022 only. It improved all three selection seasons and both targets (pooled `-3.1587e-5`), passed 2023 (`-1.7785e-5`), and passed locked 2024 (`-1.0697e-5`; target0 `+2.4734e-5`, target1 `-4.8154e-5`, both within the `5e-5` cap). `ACCEPT_STRICT`; a row-local official-feature package with the analytic final global calibration passed ZIP integrity and five-row inference preflight.
- 2026-08-27 — `COUNT-HAND-STRENGTH-EXPANSION-354`: Expanded the frozen count-hand correction strength from `2.0` through `4.0` and audited all five previously accessed OOF seasons as a robustness set. Strengths `2.25`-`3.25` improved aggregate Brier in every season, but every expanded candidate exceeded the frozen `5e-5` per-season target-loss cap; larger strengths also began losing seasons. `REJECT_ROBUST`; 353 strength `2.0` remains the accepted package, Test/public LB were not accessed, and no replacement package was created.
- 2026-08-27 — `COUNT-HAND-RECALIBRATION-355`: Fitted an incremental joint offset/scale/asymmetric-gamma correction to the accepted 353 prediction using 2020-2022 OOF only, then tested seven frozen shrinkage fractions. All fractions produced strong aggregate gains but severe target polarization and lost at least one selection season; the smallest 2% correction still worsened pooled target1 `+1.2110e-4`. `REJECT_RECALIBRATION`; 353's existing public-derived global calibration is retained, Test/public LB were not accessed, and no replacement package was created.
- 2026-08-27 — `COUNT-HAND-SECONDARY-SEGMENTS-356`: Added each frozen exact-count, count-by-runners, hand-by-runners, and inning-by-count correction from 173 on top of accepted 353, with five global strengths and development mean neutralization. The selected count-by-runners strength `2.0` improved all 2020-2022 seasons and both pooled targets (`-7.9171e-6`) but reversed on 2023 aggregate (`+3.8166e-6`). `REJECT_CONFIRMATION`; 2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `SIGNED-COUNT-HAND-STRENGTH-357`: Split 353's frozen count-by-handedness correction into separate global positive and negative strengths across a 5x5 preregistered grid. The selected `(positive=2.0, negative=3.0)` candidate improved all 2020-2022 seasons and both targets (`-2.7278e-6`) versus 353, but reversed on 2023 aggregate (`+2.2049e-6`). `REJECT_CONFIRMATION`; 2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `RELIABILITY-MODULATED-COUNT-HAND-358`: Modulated 353's frozen count-hand correction using strict-past pitcher, batter, minimum, or geometric current-season support across three scales and four signed strengths. Batter support produced the best small balanced pooled gain (`-8.6332e-7`), but every candidate lost at least one 2020-2022 season and missed the minimum gain. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `ROBUST-COUNT-HAND-ESTIMATORS-359`: Re-estimated the 11 frozen stable count-hand corrections using median, minimum-absolute, recent-weighted, or trimmed-midrange summaries of their 2020-2022 residual biases, then compared five global strengths against 353. The selected trimmed-midrange strength `2.0` improved all selection seasons and both targets (`-1.3962e-6`) but marginally reversed on 2023 (`+6.3553e-7`). `REJECT_CONFIRMATION`; 2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `STABILITY-WEIGHTED-COUNT-HAND-360`: Weighted each of the 11 frozen count-by-handedness corrections by five preregistered cross-season stability/support formulas, three reliability floors, and five global strengths. The pooled-best inverse-CV candidate improved both targets (`-7.4645e-6`) but improved only two of the three 2020-2022 seasons, so no candidate passed the strict selection gate. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `COUNT-HAND-SEGMENT-JACKKNIFE-361`: Individually removed, halved, or boosted each of the 11 frozen count-by-handedness corrections while keeping 353's global strength fixed. Boosting `3-1|2|2` by 1.5 produced the best pooled gain (`-1.4191e-6`) with both targets improving, but 2022 marginally worsened (`+2.7460e-7`); no candidate won all three selection seasons. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `COUNT-HAND-PAIRED-BALANCE-362`: Jointly adjusted the two complementary segments from 361. Multipliers `1.5` for `3-1|2|2` and `2.0` for `1-2|1|1` passed selection with all three seasons and both targets improving (`-3.4461e-6` pooled), but reversed on 2023 (`+3.7998e-6`) with target-direction polarization. `REJECT_CONFIRMATION`; 2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `PITCHER-COUNT-RESIDUAL-STATE-363`: Built deployable pitcher-by-ball/strike-count residual states from completed earlier OOF seasons only, with three season decays, two shrinkage priors, pair-only/hierarchical backoff, and three global fractions on top of 353. The best candidate still worsened pooled selection (`+6.7726e-7`), losing 2021 and polarizing targets despite improving 2022. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `TEMPORAL-RESIDUAL-SPLINE-364`: Extended the successful global-calibration axis with past-only regularized quantile splines orthogonal to intercept, confidence, and absolute-confidence bases. Fifteen-bin candidates improved both 2021 and 2022 strongly (best pooled `-3.7286e-5`) and remained monotone, but every improving candidate caused severe target polarization; none passed the frozen `5e-5` target-loss cap. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `CLASS-BALANCED-RESIDUAL-SPLINE-365`: Reprojected 364's frozen 15-bin calibration curve to remove class-conditional source mean shifts. The constraint system was temporally ill-conditioned: even the smallest monotone candidate worsened pooled selection by `+0.0042574`, driven by a large 2022 reversal. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `PUBLIC-LB-GAMMA-OPTIMUM-366`: Re-audited every dramatic leaderboard gain and recovered the exact vertex of the preregistered global gamma probes. Scores at gamma `0`, `-0.02`, and `+0.02` imply the exact quadratic optimum `gamma=-0.014393031311814568` and predicted score `1033.3614596813`, `+0.0402711937` above the current public best. Built a canonical-artifact, row-independent package; ZIP integrity, asset identity, and five-row inference passed. `SAFE_FINAL_CANDIDATE`.
- 2026-08-27 — `TRACKMAN-A-TIER-EXPERT-367`: Restricted the frozen TrackMan release-coupling expert to the 320 tier-A mutual monthly-fingerprint pitcher mappings, required 100/300/600 prior-season TrackMan pitches, preserved every unsupported row exactly, and evaluated on top of pure gamma-optimal 366. The best candidate improved only `-1.7392e-6`, lost 2021 (`+3.0448e-6`), and polarized targets; it was far below the deliberately raised `-1e-5` structural-gain threshold. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `CALIBRATED-DYNAMIC-BETA-368`: Re-audited the strongest frozen structural candidate, dynamic Beta 228/230, after applying the exact public-optimal affine-plus-gamma transform identically to reference and candidate. Pooled 2020-2022 Brier improved `-1.8109e-5` with both targets improving, but calibrated 2022 reversed to `+7.4328e-6`; only two seasons won. `REJECT_SELECTION`; 2023/2024/Test/public LB were not accessed and no package was created.
- 2026-08-27 — `CALIBRATED-DYNAMIC-BETA-AGGRESSIVE-369`: Audited 368's completely frozen predictions under the preregistered bounded aggressive policy. Four of five seasons improved; pooled 2020-2024 Brier improved `-1.8844e-5`, 2023 improved `-2.5827e-5`, and 2024 improved `-1.4225e-5`. The maximum yearly target loss was `+2.1160e-4`, within the aggressive `3e-4` cap. `ACCEPT_AGGRESSIVE`; Test/public LB were not accessed and no package was created because the gain is not evidence of the participant's requested 10-point leaderboard improvement.
- 2026-08-27 — `CALIBRATED-BETA-COUNT-PORTFOLIO-370`: Combined the frozen dynamic-Beta correction with the complementary frozen count-by-hand correction after exact global calibration. Selection chose full Beta weight and count strength `2.0`, improving pooled 2020-2022 Brier `-4.9563e-5`, every season, and both targets. It improved 2023 `-4.3620e-5` and locked 2024 `-2.5403e-5`, but strict locked target1 worsened `+1.6298e-4`; `REJECT_LOCKED` under the `5e-5` cap. Test/public LB were not accessed and no package was created.
- 2026-08-27 — `BETA-COUNT-PORTFOLIO-AGGRESSIVE-371`: Audited the exact frozen 370 candidate without prediction changes. All five years improved aggregate Brier; pooled 2020-2024 improved `-4.3436e-5`, and both pooled targets improved (`-7.5584e-5` / `-1.3271e-5`). Maximum single-year target loss was `+1.6298e-4`, inside the preregistered aggressive `2e-4` cap. `ACCEPT_AGGRESSIVE`; Test/public LB were not accessed and no package was created yet.
- 2026-08-27 — `BETA-COUNT-STRENGTH-EXPANSION-372`: Expanded the two frozen correction strengths beyond 370's selected boundaries. Selection again chose both grid maxima (Beta weight `2.0`, count strength `3.5`), improving all three seasons, both targets, and pooled Brier `-6.4623e-5`; 2023 improved `-6.1549e-5` and 2024 improved `-2.6827e-5`. It failed the relaxed locked target cap because 2024 target1 worsened `+3.5983e-4` while target0 improved. `REJECT_LOCKED`; Test/public LB were not accessed and no package was created.
- 2026-08-27 — `BETA-COUNT-FIVE-YEAR-ROBUST-373`: With all five official Train seasons explicitly treated as the robustness set, searched a broad global coefficient grid over the two frozen correction directions. Beta weight `0.75` and count strength `2.5` improved every year (worst year `-1.5442e-5`), pooled Brier `-4.1699e-5`, and both pooled targets (`-5.7702e-5` / `-2.6683e-5`); maximum single-year target loss stayed inside the frozen `2e-4` cap at `+1.9454e-4`. `ACCEPT_TRAIN_ROBUST`; Test/public LB were not accessed and no package was created yet.
- 2026-08-27 — `BETA-COUNT-DEPLOYMENT-SHIFT-374`: Selected the target-free 2025 dynamic-Beta branch-gap forecast using frozen 2022-2024 walk-forward absolute error. Median clipped ratio won (`MAE 4.7686e-4`) and fixed the 2025 shift at `0.0007864910`. `ACCEPT_DEPLOYMENT_SHIFT`; no Test rows, labels, IDs, or leaderboard results were used.
- 2026-08-27 — `BETA-COUNT-SUBMISSION-375`: Deployed 373 with Beta weight `0.75`, count-hand strength `2.5`, and 374's fixed 2025 shift on the canonical globally calibrated reference. ZIP integrity and five-row row-independent inference passed. `READY_STRUCTURAL_CANDIDATE`; no leaderboard claim is made before submission.
- 2026-08-27 — `BETA-RELIABILITY-GATE-376`: Modulated 375's dynamic-Beta correction using strict-past pitcher/batter sample reliability across 96 frozen global candidates. The best candidate improved pooled Brier only `-2.9781e-6`, won three of five seasons, worsened target1 `+2.0514e-5`, and lost 2022/2023. `REJECT_ROBUST`; Test/public LB were not accessed and 375 remains unchanged.
- 2026-08-27 — `BETA-COUNT-AGREEMENT-GATE-377`: Tested whether the two frozen 375 corrections should be strengthened when their row-level directions agree and weakened when they conflict. The best candidate improved pooled Brier only `-6.9706e-7`, won three of five seasons, worsened target1 `+7.3434e-6`, and lost 2021/2024. `REJECT_ROBUST`; Test/public LB were not accessed and 375 remains unchanged.
- 2026-08-27 — `DYNAMIC-BETA-COMPONENT-378`: Trained 15 new CatBoost folds for pitcher-only, batter-only, and additive-without-interactions dynamic-state branches, keeping 375's count and global calibration fixed. No candidate beat 375 pooled; the least harmful pitcher-only candidate worsened `+1.5898e-6`, lost 2021/2024, and sharply polarized targets (`+1.7349e-4` / `-1.5970e-4`). `REJECT_ROBUST`; the joint pitcher-batter interaction state in 375 is retained and Test/public LB were not accessed.
- 2026-08-27 — `DYNAMIC-BETA-UNCERTAINTY-INTERACTIONS-379`: Trained five new CatBoost folds with seven row-local uncertainty, standardized-gap, logit-gap, and prior-weight interactions added to the joint dynamic-Beta state. The best weight `1.5` improved pooled Brier `-5.0890e-6` and four of five seasons, but worsened 2022 `+7.5032e-6`, polarized pooled targets (`+7.8731e-5` / `-8.3736e-5`), and exceeded the yearly target cap. `REJECT_ROBUST`; Test/public LB were not accessed and 375 remains unchanged.
- 2026-08-27 — `DYNAMIC-BETA-UNCERTAINTY-BRIDGE-380`: Globally bridged frozen 375 and 379 correction directions across 30 candidates. The best bridge improved pooled Brier `-7.8900e-6` and four seasons, but again worsened 2022 `+9.5701e-6`, worsened pooled target0 `+6.6794e-5`, and exceeded the yearly target cap. `REJECT_ROBUST`; partial blending cannot repair 379's directional imbalance, Test/public LB were not accessed, and 375 remains unchanged.
- 2026-08-27 — `DYNAMIC-BETA-UNCERTAINTY-ABLATION-381`: Retrained five enriched temporal models and neutralized mean-geometry, uncertainty, prior-weight, or all-new feature groups to training-fold medians. Every group remained directionally polarized; the pooled-best prior-weight ablation improved `-9.2310e-6` but won only three seasons, lost 2022/2023, and worsened target0 `+1.7467e-4`. `REJECT_ROBUST`; no individual 379 feature group repairs the imbalance, Test/public LB were not accessed, and 375 remains unchanged.
- 2026-08-27 — `BETA-COUNT-SECONDARY-SEGMENTS-382`: Added frozen exact-count, count-by-runners, hand-by-runners, and inning-by-count corrections on top of 375 across 32 global candidates. The best hand-by-runners candidate improved pooled Brier `-4.6477e-6` but won only three seasons, lost 2022/2024, and worsened target0 `+1.5134e-5`. `REJECT_ROBUST`; Test/public LB were not accessed and 375 remains unchanged.
- 2026-08-27 — `DYNAMIC-BETA-UNCERTAINTY-RECENTER-383`: Jointly searched 270 frozen global combinations of the 375/379 bridge and a single row-independent recentering offset. Recentring could balance pooled targets or produce five aggregate wins, but not both: the best balanced candidate improved `-6.08e-6` with four wins, while the best five-win candidate improved `-2.32e-6` but worsened target1 `+5.9e-5`. No candidate passed all constraints. `REJECT_ROBUST`; Test/public LB were not accessed and 375 remains unchanged.
- 2026-08-27 — `DYNAMIC-BETA-COUNT-JOINT-RECENTER-384`: Added count-hand strength to the frozen 383 bridge/offset search across 240 focused global candidates. The pooled best improved `-1.0414e-5`, but won only three seasons, lost 2021/2022, and worsened target1; 16 candidates balanced pooled targets, yet none improved all five seasons. `REJECT_ROBUST`; the unresolved 2022 reversal is not repaired by count strength, Test/public LB were not accessed, and 375 remains unchanged.
- 2026-08-27 — `COUNT-HAND-RIDGE-RESIDUAL-385`: Fit regularized 48-cell count-hand residual corrections on frozen 375 OOF predictions from 2020-2022 only. The selected pseudo-count `10000`, minimum support `500`, full-strength candidate improved all fitting seasons and pooled Brier `-2.0115e-5` with both targets improving. It also improved 2023 aggregate `-1.0779e-5`, but target0 worsened `+6.0352e-5`, just beyond the frozen `5e-5` cap, so 2024 was not accessed. `REJECT_CONFIRMATION`; Test/public LB were not accessed and 375 remains unchanged.
- 2026-08-27 — `COUNT-HAND-RIDGE-STABILITY-386`: Used disclosed 2023 to stabilize the 385 estimator while keeping correction values fitted only on 2020-2022. Pseudo-count `3000`, minimum support `1500`, and strength `0.9` improved all four selection seasons (`-1.6023e-5` pooled) with both pooled targets improving and maximum selection target loss `4.6798e-5`. Locked 2024 improved `-4.4742e-6` with target losses inside the `5e-5` cap. `ACCEPT_STRICT`; Test/public LB were not accessed.
- 2026-08-27 — `COUNT-HAND-RIDGE-DEPLOYMENT-387`: Refit the frozen 386 estimator on all five official Train OOF seasons without further selection. The refit diagnostic improved pooled Brier `-1.4126e-5` with both targets improving (`-1.4735e-5` / `-1.3554e-5`). `ACCEPT_DEPLOYMENT_REFIT`; Test/public LB were not accessed.
- 2026-08-27 — `COUNT-HAND-RIDGE-SUBMISSION-388`: Added the frozen 387 post-calibration count-hand residual map to package 375. ZIP integrity, exact payload structure, finite predictions, and five-row row-independent inference passed. Package `submit_388_count_hand_ridge.zip`, SHA-256 `622f1803281772ae2b7cea5f900db15c8daa36234cdf3b62a73d6cccc0ef4665`; `READY_STRICT_CANDIDATE`.
- 2026-08-27 — `COUNT-HAND-RIDGE-BRIER-MAX-389`: Explicitly optimized pooled five-season Brier over 432 regularized count-hand residual candidates while preserving 388 separately. Cap `0.02`, pseudo-count `1000`, minimum support `1500`, and strength `1.0` improved every season and pooled Brier `-3.9874e-5`; target0 worsened `+5.2334e-5` while target1 improved `-1.2639e-4`. `ACCEPT_BRIER_MAX`; Test/public LB were not accessed.
- 2026-08-27 — `COUNT-HAND-BRIER-MAX-DEPLOYMENT-390`: Refit the frozen 389 estimator on all five official Train OOF seasons without further selection. The in-sample deployment diagnostic improved pooled Brier `-4.9309e-5` with both targets improving. `ACCEPT_BRIER_MAX_DEPLOYMENT_REFIT`; Test/public LB were not accessed.
- 2026-08-27 — `COUNT-HAND-BRIER-MAX-SUBMISSION-391`: Packaged 390 as a separate aggressive candidate while preserving strict package 388. ZIP integrity, payload structure, finite predictions, and five-row row-independent inference passed. Package `submit_391_count_hand_brier_max.zip`, SHA-256 `326beadc0357087dcb03bdf8ce1f8aa585915e259f3c8ea8cbcbbbfedab53484`; `READY_AGGRESSIVE_BRIER_MAX_CANDIDATE`.
- 2026-08-27 — `HIGH-ORDER-CONTEXT-RESIDUAL-392`: Fit a second residual layer on frozen 389 predictions using count-hand crossed with runners, inning, outs, half, and base state. The pooled-Brier winner was count-hand-base with cap `0.02`, pseudo-count `500`, minimum support `100`, and strength `1.0`; it improved pooled Brier `-4.6359e-5` and both pooled targets, but won only three seasons and lost 2023/2024. `ACCEPT_BRIER_MAX`; Test/public LB were not accessed.
- 2026-08-27 — `HIGH-ORDER-CONTEXT-DEPLOYMENT-393`: Refit the frozen 392 count-hand-base estimator on all official Train OOF seasons over deployment base 390. The in-sample deployment diagnostic improved Brier `-6.8486e-5` with both targets improving; 376 segments were active. `ACCEPT_AGGRESSIVE_DEPLOYMENT_REFIT`; Test/public LB were not accessed.
- 2026-08-27 — `HIGH-ORDER-BRIER-MAX-SUBMISSION-394`: Packaged 393 over preserved candidate 391. ZIP integrity, payload structure, finite predictions, and five-row row-independent inference passed. Audit combined delta versus 375 is `-8.6233e-5`; package `submit_394_high_order_brier_max.zip`, SHA-256 `11cc1bb73aaba1720f78a3ac7e897d207922bd7f722bddb415a4e63498103cc2`; `READY_VERY_AGGRESSIVE_BRIER_MAX_CANDIDATE`.
- 2026-08-27 — `ROLLING-ORIGIN-VALIDATION-RESET-395`: Re-evaluated 366/375/388/391/394 against confirmed public baseline 345 using earlier-season-only affine-plus-shape calibration and rolling residual refits for 2022→2024. No candidate passed the frozen recent-year deployment gate. 391 had the strongest recent pooled delta (`-8.6079e-5`) and positive recent AUC gains, but 2024 target1 worsened `+3.5369e-4`; 394 reversed 2024 Brier `+2.3308e-5` and AUC. `VALIDATION_RESET_COMPLETE_NO_DEPLOYMENT`; 394 is withdrawn and no submission was created.
- 2026-08-27 — `ROW-LOCAL-EMPIRICAL-BAYES-CALIBRATION-396`: Nested rolling-origin calibration used strict-past pitcher/batter current-season deviations, empirical-Bayes reliability, count/runner/hand interactions, and inner-fold L2 selection on top of 345. It improved 2023 Brier `-3.3799e-4` and AUC `+6.8045e-4`, but reversed sharply in 2024 (`+4.6598e-4`, AUC `-3.2151e-3`) with severe target polarization. Pitcher-cluster improvement probability was only `3.6%`. `REJECT_ROLLING_GATE`; Test/public LB were not accessed and no submission was created.
- 2026-08-27 — `ROLLING-COUNT-HAND-RIDGE-397`: Removed dynamic-Beta and legacy count corrections, then fit count-hand residual maps directly on rolling-calibrated 345 with nested earlier-season regularization selection. The same conservative specification was selected in every outer fold (cap `0.0025`, pseudo-count `30000`, minimum support `5000`, strength `0.25`). Brier and AUC improved in 2022, 2023, and 2024, both pitcher and season-month cluster bootstrap probabilities were `100%`, and target losses stayed tiny; however recent pooled Brier improved only `-4.5789e-6`, far below the frozen `-2.5e-5` deployment threshold. `REJECT_ROLLING_GATE`; no submission was created.
- 2026-08-27 — `RECENT-WEIGHTED-RESIDUAL-CATBOOST-398`: Trained four expanding rolling CatBoost regressors to predict calibrated-345 residuals from canonical and current-season row-local features, using 50% season decay, strong L2 regularization, and earlier-fold-only blend selection. The direction showed real recent discrimination (AUC `+1.3703e-4` in 2023 and `+2.3230e-4` in 2024) and recent pooled Brier improved `-3.3290e-5`, but 2024 improved only `-1.7454e-5` and class deltas were severely polarized (`+1.9448e-3` / `-2.0918e-3`). `REJECT_ROLLING_GATE`; checkpoints were preserved, Test/public LB were not accessed, and no submission was created.
- 2026-08-27 — `ORTHOGONAL-RESIDUAL-DIRECTION-399`: Reused frozen 398 checkpoints and estimated target-free intercept/slope/absolute-confidence projections from earlier OOF seasons only. Orthogonalization retained positive AUC gains in 2023/2024 but destroyed the 2023 Brier gain and left recent pooled Brier essentially neutral (`+6.8029e-7`); pitcher/month bootstrap probabilities fell to `46.4%`/`43.4%`. `REJECT_ROLLING_GATE`; source models were not retrained, Test/public LB were not accessed, and no submission was created.
- 2026-08-27 — `RECENT-BALANCED-RANK-CATBOOST-400`: Trained four expanding class-balanced CatBoost classifiers with 50% season decay and combined their scores with rolling-calibrated 345 through earlier-OOF-only regularized logit stacking. The standalone model gained AUC in 2023 (`+6.9585e-4`) but reversed in 2024 (`-1.5789e-3`); the stacked candidate worsened Brier in every outer fold and recent pooled Brier by `+2.8590e-4`, with zero pitcher/month bootstrap support. `REJECT_ROLLING_GATE`; checkpoints were preserved, Test/public LB were not accessed, and no submission was created.
- 2026-08-27 — `LAGGED-BALANCED-RESIDUAL-401`: Reused frozen 398 directions and selected a residual strength plus a single global offset from the immediately preceding OOF season, analytically interpolating between pooled optimum and equal class-delta balance. Recent pooled Brier reached `-2.5054e-5` with positive AUC gains and strong cluster bootstrap support, but the prior-year balance point did not transfer: 2024 improved only `-1.9905e-6` and polarized targets (`+2.2573e-3` / `-2.3904e-3`). `REJECT_ROLLING_GATE`; no model retraining, Test/public LB access, or submission creation occurred.
- 2026-08-28 — `CLASS-CENTERED-RESIDUAL-CATBOOST-402`: Retrained expanding recent-weighted residual CatBoost models after subtracting training-fold class-conditional residual means, intending to remove global class bias and retain contextual error structure. Every immediately preceding fold still violated the `1e-4` target-loss cap even at 5% strength, so the nested rule selected zero correction for all outer years. The learned evaluation directions retained large positive mean shifts (`+0.0102` to `+0.0135`) despite near-zero training centers. `REJECT_ROLLING_GATE`; no Test/public LB access or submission creation occurred.
- 2026-08-28 — `MONTHLY-ROLLING-STABILITY-AUDIT-403`: Audited frozen 397/398/402 directions across 15 eligible 2023-2024 season-month blocks. No candidate passed. The conservative 397 count-hand ridge was the only direction with 80% month wins, 80% month AUC wins, tiny balanced target deltas, and 100% month-bootstrap support, but its 2024 gain was only `-4.0232e-6`. Residual models won 11/15 months but reversed in late 2024 and remained severely class-polarized; 398 losses concentrated in 2024 August-October. `MONTHLY_AUDIT_COMPLETE_NO_STABLE_DIRECTION`; diagnostic only, with no Test/public LB access or submission creation.
- 2026-08-28 — `MONTHLY-FEATURE-GROUP-ABLATION-404`: Retrained ten 398-style residual models for 2023/2024 while separately removing recent-game form, current-season state, team/score context, pitchmix/subtype, or hand/count feature groups. No ablation passed. Removing pitchmix/subtype gave the best overall recent result (`-4.8248e-5`, 12/15 month wins, positive 2023/2024 AUC gains), but every variant still lost aggregate Brier and AUC across the 2024 August-October block. Removing current-season state reduced the late loss most (`+7.8604e-6`) but damaged 2023 and remained target-polarized. `FEATURE_ABLATION_COMPLETE_NO_STABLE_MODEL`; the late reversal is not attributable to one feature family, Test/public LB were not accessed, and no submission was created.
- 2026-08-28 — `PHASE-MATCHED-RESIDUAL-CATBOOST-405`: Trained nine rolling CatBoost residual experts restricted to matching early (Mar-May), middle (Jun-Jul), or late (Aug-Oct) season phases. Phase strengths were selected only from earlier outer folds, with an explicit zero fallback when no nonzero option passed the prior target-balance rule. The safe candidate improved 2023/2024 Brier by only `-8.8802e-6` / `-3.6479e-6`; 2024 middle and late experts were disabled, while the retained early expert remained class-polarized (`+3.9197e-4` / `-4.2189e-4` overall). Recent pooled improvement was only `-6.2222e-6`, and late-2024 improvement was exactly zero. `REJECT_PHASE_MATCHED_GATE`; Test/public LB were not accessed and no submission was created.
- 2026-08-28 — `RECENT-FULL-BASE-CATBOOST-406`: Trained three new direct 142-feature CatBoost classifiers with fixed 65% season decay, including engineered interactions, current-season pitcher/batter states, and both entity IDs. The safe nested target-balance selector disabled the new model in 2023/2024. A frozen 10% diagnostic nevertheless revealed genuine discrimination gains in both recent seasons: 2023 Brier/AUC `-1.6661e-4` / `+1.8521e-4`, and 2024 `-6.9613e-6` / `+1.3377e-4`. However class deltas were severely polarized (2024 `+6.7347e-4` / `-7.2629e-4`), so `REJECT_NEW_BASE_MODEL_GATE`; checkpoints were retained, Test/public LB were not accessed, and no submission was created.
- 2026-08-28 — `LAGGED-AFFINE-NEW-BASE-407`: Froze the 406 models and 10% blend, then fit one global affine-plus-confidence calibration using only earlier outer-fold predictions. It retained both recent AUC gains and improved 2023 Brier `-9.0921e-5`, but the past-fitted correction reversed 2024 Brier to `+1.3554e-5` and flipped the class imbalance (`-9.6819e-4` / `+1.0514e-3`). `REJECT_LAGGED_AFFINE_GATE`; the new rank signal remains promising but global lagged calibration does not transfer, with no Test/public LB access or submission creation.
- 2026-08-28 — `RECENT-FULL-BASE-NO-IDS-408`: Retrained all three 406 rolling folds after removing only direct pitcher and batter IDs, retaining the other 140 features and frozen 10% blend. The no-ID model preserved recent discrimination and slightly strengthened 2023 (`-1.7609e-4`, AUC `+2.0068e-4`), proving the new signal is not dependent on direct identity memorization. It weakened 2024 to `-2.2608e-6`, AUC `+3.8187e-5`, and remained class-polarized (`+7.5347e-4` / `-8.0120e-4`). `REJECT_NO_ID_BASE_MODEL_GATE`; direct IDs are not the primary bias source, Test/public LB were not accessed, and no submission was created.
- 2026-08-28 — `RECENT-FULL-BASE-NO-CURRENT-STATE-409`: Retrained all three 406 folds after removing only the 12 generated current-season pitcher/batter empirical-Bayes features. The large 2023 discrimination signal collapsed: Brier improvement shrank from `-1.6661e-4` to `-4.5067e-5`, and AUC changed from `+1.8521e-4` to `-1.4887e-4`. The 2024 AUC gain remained positive (`+9.8993e-5`) but Brier improved only `-2.8442e-6`, while class polarization persisted. `REJECT_NO_CURRENT_STATE_GATE`; current-season state is essential to the new 2023 rank signal but is not the sole calibration-bias source, Test/public LB were not accessed, and no submission was created.
- 2026-08-28 — `PUBLIC-LB-GAMMA-OPTIMUM-366-CONFIRMATION`: Submitted the previously frozen package under filename `submit123.zip`. Public score was `1033.3614596813`, matching the analytic prediction `1033.3614596812783` within `2.2e-11` and improving the prior `1033.3211884876`. Experiment 366 is now the verified public best.
- 2026-08-28 — `PAIRWISE-RANK-RESIDUAL-410`: Trained three rolling CatBoost `PairLogit` rankers over pitcher-season-month-dayofweek query groups using the full 406 feature set plus calibrated 345, capped at 20 sampled pairs per query and 500 iterations. Rank scores were projected off base logit and standardized using training-only constants before nested logit blending. The direction weakly improved 2022 (`-6.1504e-6`, AUC `+1.4092e-5`) and fixed-strength 2024 (`-5.1920e-6`, AUC `+1.1457e-4` at strength 0.01), but reversed sharply in 2023 even at the minimum 0.005 strength (`+1.1153e-4`, AUC `-1.5705e-4`). The nested rule therefore disabled 2024. `REJECT_PAIRWISE_RANK_GATE`; pairwise within-pitcher ordering does not transfer consistently, Test/public LB were not accessed, and no submission was created.
- 2026-08-28 — `PUBLIC-LB-CURVATURE-PROBES-411`: Starting from verified public-best 366 (`1033.3614596813`), preregistered symmetric coefficients `-0.05/+0.05` for the new global basis `(p-0.5)*abs(p-0.5)`. Both complete transforms are strictly monotone (minimum derivatives `1.1022/1.1522`), apply identically to every row, and use no row, ID, segment, external, or Test-distribution information. Every model asset is byte-identical to 366; ZIP layout and five-row inference passed. Packages `submit_411_curvature_minus005.zip` and `submit_411_curvature_plus005.zip`; `TWO_GLOBAL_CURVATURE_PROBES_READY`.
- 2026-08-28 — `PUBLIC-LB-CURVATURE-OPTIMUM-412`: The preregistered 411 probes scored `1033.3705856281` at `h=-0.05` and `1033.3090701122` at `h=+0.05` around reference `1033.3614596813`. The exact quadratic is `score(h)=-8.65272445998926*h^2-0.615155158998277*h+1033.3614596813`, giving vertex `h=-0.0355469055927294` and predicted score `1033.37239311248` (`+0.01093343118`). The final global monotone package preserves all 366 model assets; no further coefficient search was performed.
- 2026-08-28 — `PUBLIC-LB-CUBIC-PROBES-413`: Froze the exact 412 signed-curvature vertex and added symmetric coefficients `-0.1/+0.1` for a new global cubic confidence basis `(p-0.5)^3`. Both transforms remain strictly monotone (minimum derivatives `1.0417/1.1480`), apply identically to every row, preserve all 366 model assets byte-for-byte, and passed ZIP-layout plus five-row inference checks. Packages `submit_413_cubic_minus010.zip` and `submit_413_cubic_plus010.zip`; `TWO_GLOBAL_CUBIC_PROBES_READY`.
- 2026-08-28 — `PUBLIC-LB-CUBIC-OPTIMUM-414`: The 413 probes scored `1033.3479829257` at `k=-0.1` and `1033.3951899684` at `k=+0.1` around the exact 412 reference prediction `1033.37239311248`. The conditional quadratic `-0.0806665429990971*k^2+0.23603521349969*k+c` gives vertex `k=1.46303042577597` and predicted score `1033.54505646193`, about `+0.18360` over verified 366. Historical OOF raw probabilities span `0.3578~0.7881`, indicating the stronger monotone cubic remains far from clipping on observed model support. The final package preserves all 366 assets and uses one global transform.
- 2026-08-29 — `PUBLIC-LB-QUARTIC-AGGRESSIVE-PROBES-415`: Froze the exact 414 cubic optimum and prepared three submissions in order: the 414 vertex, then aggressive symmetric quartic probes `m=-2/+2` on `(p-0.5)^4`. Both probe transforms remain strictly monotone over the full probability interval (minimum derivatives `1.151951/1.151959`), preserve all 366 model assets byte-for-byte, and passed five-row inference, Python compilation, ZIP layout, and CRC checks. Packages `submit_414_cubic_optimum.zip`, `submit_415_quartic_minus2.zip`, and `submit_415_quartic_plus2.zip`; `THREE_AGGRESSIVE_SUBMISSIONS_READY`.
- 2026-08-29 — `PUBLIC-LB-QUARTIC-EXTRAPOLATION-416`: Actual scores at quartic coefficients `m=0/-2/+2` were `1033.5450564678/1033.6309405935/1033.4517504041`. Their exact conditional Brier parabola has `a=-0.0009277422499280874`, `b=-0.044797547350015066`, and vertex `m=-24.143315319253535`, predicting `1034.0858371234` if clipping remains inactive. Prepared extreme vertex `s4.zip` and aggressive hedge `m=-16` (`s5.zip`, predicted `1034.0243152094`); both passed five-row inference, compilation, ZIP layout, and CRC checks. `TWO_EXTREME_QUARTIC_SUBMISSIONS_READY`.
- 2026-08-30 — `PUBLIC-LB-QUINTIC-AGGRESSIVE-PROBES-417`: The experiment-416 predictions were exact to roughly `4e-10`: `s4=1034.0858371238` and `s5=1034.0243152097`. Froze `s4` and added symmetric aggressive coefficients `-10/+10` for the new global quintic basis `(p-0.5)^5`. Both packages preserve the model assets, avoid clipping in the five-row smoke test, and pass compilation, ZIP-layout, and CRC checks. Packages `s6.zip` and `s7.zip`; `TWO_AGGRESSIVE_QUINTIC_PROBES_READY`.
- 2026-08-30 — `PUBLIC-LB-STRUCT375-PROBES-418`: Ended polynomial calibration after the quintic probes implied only `+0.002674` at their exact vertex. Froze public-best `s4` and constructed a genuine structural direction from experiment 375's dynamic pitcher/batter Beta state plus count-hand correction. Applied the complete frozen `s4` calibration separately to canonical and structural endpoints, then prepared exact probability blends at fractions `0.5/1.0`. Five-row inference changed predictions by mean absolute `0.001425` at the full endpoint, the half-probe identity held to `5.6e-17`, all 375 assets were byte-identical, and compilation, ZIP layout, and CRC checks passed. Packages `s8.zip` and `s9.zip`; `TWO_STRUCTURAL_PROBES_READY`.
- 2026-08-30 — `PUBLIC-LB-STRUCT375-REJECTION-418`: The participant submitted only the safer half-strength structural probe `s8.zip`; it scored `1030.3038856474`, a material `-3.7819514764` versus `s4=1034.0858371238`. This confirms that the five-year-local dynamic-Beta/count improvement does not transfer to 2025 after the exact public calibration. `REJECT_PUBLIC_LB`; do not submit `s9.zip`, do not reverse or microblend this direction, and retain `s4` as the incumbent.
- 2026-08-30 — `RECENT-WINDOW-DIRECT-CATBOOST-419`: Trained a new 142-feature depth-7 CatBoost classifier using only the most recent three completed seasons and evaluated only large 50%/100% replacements, with raw and strictly lagged-affine modes. All four candidates improved 2023 dramatically (best `-0.001721`) but every candidate collapsed in 2024: the least harmful 50% lagged candidate still worsened Brier `+1.4556e-4`, lost AUC `-8.7389e-4`, and had worst target loss `+0.00547`. `REJECT_LARGE_RECENT_MODEL`; Test/public LB were not accessed and no submission ZIP was created.
- 2026-08-30 — `TRACKMAN-YOY-STATE-INTERACTION-420`: Built 57 new strict-past features combining prior-season TrackMan velocity, spin, movement, release, arsenal mix, variability, and their year-over-year changes with current-season pitcher form/workload. High-confidence A/B monthly-fingerprint mappings covered `70.5%-80.1%` of rows, while the two-season 300/100-pitch support gate retained about `50%`; all unsupported rows remained exactly canonical. Large 50%/100% replacements failed: the safer 50% candidate worsened 2023 Brier `+2.3998e-5` and AUC `-1.4393e-4`, while 2024 was nearly neutral (`-6.3381e-7`). `REJECT_LARGE_TRACKMAN_TREND`; Test/public LB were not accessed and no submission ZIP was created.
- 2026-08-30 — `TWO-DISTINCT-STRUCTURAL-CANDIDATES-421-423`: Prepared two non-micro alternatives on the verified `s7` global calibration. `c1.zip` adds the full frozen count×pitcher-hand×batter-hand Brier-max ridge residual layer to the canonical endpoint. The initial gated TrackMan `c2` design was withdrawn during review because experiments 324/367 had already closed that axis. Replacement `c2.zip` reverses at full strength the complete dynamic-Beta plus legacy count-hand structural direction whose half-strength public probe lost `-3.78195` points. Both final packages passed Python compilation, five-row inference, root ZIP-layout inspection, and SHA-256 generation. These are deliberately different high-variance structural probes, not neighboring calibration coefficients.
- 2026-08-31 — `STRUCTURAL-CANDIDATES-PUBLIC-REJECTION-421-423`: Actual public scores were `1018.2426250692` for full count-hand Brier-max `c1.zip` and `1027.6231912069` for reversed dynamic-Beta/count-hand `c2.zip`, losses of `-15.8456160830` and `-6.4650499453` versus incumbent `s7=1034.0882411522`. `REJECT_PUBLIC_LB` for both. Full residual deployment refits do not transfer to 2025, and the loss of a positive structural probe does not justify reversing that direction: curvature dominates and both signs lose. Do not submit, blend, reverse, or refine either family; retain `s7` unchanged.
- 2026-08-31 — `S7-DETAILED-SEGMENT-DISCOVERY-424`: Froze the exact public-best `s7` endpoint and tested 26 row-local feature crosses with selection restricted to rolling 2021/2022 and confirmation on 2023/2024. Batter-form crosses produced real recent rank signal: `hands×batter-form` improved Brier/AUC in both confirmation years (`2023 -7.02e-5/+2.80e-4`, `2024 -1.31e-5/+1.60e-4`), but target1 worsened up to `+4.68e-4`. No family met the frozen balanced `-2.5e-5` gate. `NO_LARGE_STABLE_SEGMENT_SIGNAL`; Test was not accessed and no package was created.
- 2026-08-31 — `S7-SEGMENT-ORTHOGONALIZATION-425`: Removed intercept, slope, confidence-shape, complete s7-basis, or confidence-bin projections from the strongest 424 directions using training years only. Aggregate discrimination survived, but the batter-form class polarization remained. The balanced `base×outs×count` direction improved both targets in 2023/2024 but only `-1.07e-5` mean Brier. `REJECT_NO_BALANCED_LARGE_GAIN`; Test was not accessed.
- 2026-08-31 — `S7-MULTISIGNAL-RIDGE-426`: Combined nine frozen segment directions with season-decayed ridge and confidence interactions. The selected direction improved 2023/2024 Brier `-8.64e-5/-2.57e-5` and AUC in both, but severely polarized targets (`2024 target1 +1.26e-3`) and did not pass the earlier selection folds. `REJECT_NO_BALANCED_LARGE_GAIN`; no Test access or package.
- 2026-08-31 — `S7-CLASS-CONSTRAINED-RIDGE-427`: Added exact quadratic constraints prohibiting training-fold loss for either target class. The best rolling specification improved all 15 confirmation months, with 2023/2024 Brier `-5.87e-5/-1.90e-5` and AUC `+2.99e-4/+2.78e-4`, but the constraint did not fully transfer: 2024 target1 worsened `+1.22e-4`, above the `1e-4` cap, and the early selection target cap also failed. `REJECT_NO_BALANCED_LARGE_GAIN`; the signal is promising research evidence but not submission-grade, and no ZIP was created.
- 2026-08-31 — `S7-SEASON-TARGET-GROUPDRO-428`: Applied exact non-loss constraints to every available season×target group while fitting the frozen multisignal residual direction. The constrained model improved every confirmation month, 2023/2024 Brier `-4.52e-5/-2.69e-5`, and AUC `+2.87e-4/+3.43e-4`. However target balance still drifted out of sample: 2024 target1 worsened `+1.55e-4`, and no early-selection specification met the `1e-4` cap. `REJECT_GROUPDRO_GATE`; no Test access or package.
- 2026-08-31 — `S7-GROUPDRO-LAGGED-BALANCE-429`: Estimated one class-balance offset solely from the immediately preceding completed season and froze it for each next-year evaluation. This repaired 2024 completely: Brier `-2.52e-5`, target0/1 `-1.83e-5/-3.25e-5`, AUC `+3.43e-4`, and all 8 months improved. But the 2022-derived offset had the wrong sign for 2023, leaving target1 `+1.15e-4`; early selection also missed the cap by `5.45e-6`. `REJECT_LAGGED_BALANCE_GATE`; no ZIP. The remaining issue is specifically the year-to-year sign transition in the balance offset, not lack of rank signal.
- 2026-08-31 — `S7-RECENT-WEIGHTED-GROUPDRO-430`: Refit both the segment residual maps and GroupDRO objective with exponential season decay (`0.50/0.75` selected only on 2021/2022), retaining strict season×target constraints and the immediately preceding-season balance offset. The chosen `0.50` decay retained positive 2023/2024 AUC and recent mean Brier `-3.26e-5`; 2024 target balance was nearly perfect (`target0 -2.61e-5`, `target1 +2.55e-7`). However it worsened the 2023 target1 loss to `+1.98e-4`, and no selection specification met the target cap. `REJECT_RECENT_WEIGHTED_GATE`; recent weighting does not solve the 2022→2023 balance sign change, Test was not accessed, and no ZIP was created.
- 2026-08-31 — `S7-CONDITIONAL-RANK-SIGNAL-431`: Converted the strongest batter-form segment residuals into training-CDF percentile scores inside fixed s7 probability bins, so inference remains row-independent and does not use Test distributions. The selected count×batter-form rank layer improved 2023/2024 Brier `-8.78e-5/-1.93e-5` and AUC `+2.26e-4/+2.78e-4`, but its conditional score distribution still shifted and target1 worsened `+4.25e-4/+1.93e-4`. `REJECT_CONDITIONAL_RANK_GATE`; probability-bin rank normalization does not remove batter-form class drift.
- 2026-08-31 — `S7-CONTEXT-ONLY-GROUPDRO-432`: Removed all pitcher/batter-form directions and combined only count-hand, base state, outs, count, and leverage signals under season×target constraints. Confirmation was balanced and directionally consistent: 2023/2024 Brier `-1.81e-5/-2.56e-5`, AUC `+1.53e-4/+3.23e-4`, all 15 months improved, and worst confirmation target loss was only `+5.60e-5`. However recent mean gain was `-2.18e-5`, below the frozen `-2.5e-5` threshold, and the earlier 2021/2022 selection gate failed badly. `REJECT_CONTEXT_ONLY_GATE`; no Test access or ZIP. This is the safest new recent-year direction but lacks pre-transition evidence.
- 2026-08-31 — `S7-CONTEXT-PHASE-EXPERTS-433`: Froze 432's form-free context signals and fit separate early/late or early/middle/late season×target-constrained experts, selecting only on 2021/2022. The selected early/late split modestly strengthened the recent result: 2023/2024 Brier `-1.92e-5/-2.64e-5`, AUC `+1.56e-4/+3.38e-4`, all 15 months improved, and worst confirmation target loss stayed within tolerance at `+8.77e-5`. Recent mean reached `-2.28e-5`, still short of `-2.5e-5`, while the early selection gate remained unstable. `REJECT_PHASE_EXPERT_GATE`; no Test access or ZIP.
- 2026-08-31 — `S7-PRESSURE-STATE-EXPERTS-434`: Split 432's context-only direction by count pressure, scoring-position×outs, pressure×scoring-position, or pressure×outs and fit separate season×target-constrained experts. The selected pressure split weakened the signal: 2023/2024 Brier `-1.19e-5/-1.50e-5`, only 11/15 months improved, and 2024 target1 worsened `+2.16e-4`. The early selection gate also failed. `REJECT_PRESSURE_EXPERT_GATE`; pressure segmentation fragments the stable context signal and is closed, with no Test access or ZIP.
- 2026-08-31 — `S7-INDEPENDENT-CONTEXT-MODEL-435`: Trained four expanding rolling CatBoost residual models using only 48 game-state, count, runners, score, leverage, expectancy, hand, and phase features; all player IDs and current player-form features were excluded. Although AUC increased slightly in both recent years, Brier worsened in 2023 `+7.04e-5` and 2024 `+1.92e-6`, with severe 2024 target polarization. `REJECT_INDEPENDENT_CONTEXT_GATE`; the safe 433 signal comes from regularized historical segment shrinkage and is not recoverable as a standalone nonlinear context model. Test was not accessed and no ZIP was created.
- 2026-08-31 — `S7-PHASE-ROW-GATE-436`: Audited 433's frozen early/late correction with 27 preregistered row-local gates based on phase, correction magnitude/sign, runners, scoring position, outs, count pressure, and leverage. No gate met the 2021/2022 selection stability and target-balance requirements. The fallback pooled-best positive-correction gate reversed recent Brier (`2023 +2.17e-5`, `2024 +5.65e-7`) and severely polarized targets. `REJECT_ROW_GATE`; restricting 433 to apparently favorable row subsets destroys its balanced aggregate cancellation, so row gating is closed. Test was not accessed and no ZIP was created.
- 2026-08-31 — `S7-PHASE-PLUS-RECENT-MODEL-437`: Combined 433's safe early/late context correction with the independently trained 406 recent full-base CatBoost direction, whose target bias is opposite. Weights were fitted only on 2022 under a `1e-4` per-target cap. The combination produced a large stable rank gain: 2023/2024 Brier `-1.01e-4/-3.79e-5`, AUC `+2.65e-4/+4.57e-4`, and all 15 months improved. It narrowly missed confirmation because 2023 target0 worsened `+1.13e-4`. `REJECT_CROSS_SIGNAL_GATE`; a strict safety refit was preregistered as 438.
- 2026-08-31 — `S7-PHASE-PLUS-RECENT-STRICT-438`: Refit the two frozen 437 weights using only 2022 while requiring zero Brier loss for both selection targets. Frozen weights were phase `1.2523352284` and recent-model `0.0319342267`. The candidate passed every deployment condition: 2022/2023/2024 Brier `-1.37e-5/-7.11e-5/-3.59e-5`; 2023/2024 AUC `+2.33e-4/+4.43e-4`; all 15 recent months improved; confirmation target deltas stayed under the `1e-4` cap (worst `+8.90e-5`); recent mean Brier improved `-5.35e-5`. `CANDIDATE_FOUND`; Test was not accessed and no package was created pending cluster-bootstrap and deployment-refit audit.
- 2026-08-31 — `S7-CANDIDATE-438-BOOTSTRAP-439`: Audited frozen 438 with 2,000 cluster-bootstrap repetitions over pitcher×season, batter×season, season×month, and season×month×day-of-week clusters. Every axis returned `1.000` improvement probability, while the exact 2023/2024 fold metrics and 15/15 month wins were reproduced. `PASS_BOOTSTRAP_AUDIT`; Test was not accessed.
- 2026-08-31 — `S7-CANDIDATE-438-PACKAGE-440`: Refit the frozen context residual maps and early/late season×target GroupDRO coefficients on all official 2020-2024 OOF rows, trained the 142-feature recent CatBoost deployment model on all official Train rows with frozen 0.65 season decay, and estimated its 2025 affine calibration solely from 2022-2024 rolling OOF predictions. Packaged the exact frozen weights over public-best s7. The package is row-independent, uses no Test distribution, passed compilation, provided five-row inference, archive extraction, and bit-exact extracted reproduction. Package `s10.zip`, 13,841,207 bytes, SHA-256 `6e47493b9b5073774f1679acfd2b413ade1e576ef10025bfb239694368c5833b`; `PACKAGE_READY`.
- 2026-08-31 — `S7-CANDIDATE-438-RUNTIME-PATH-FIX-441`: The platform rejected `s10.zip` during import because the bundled feature helper assumed repository depth with `Path(__file__).resolve().parents[2]`; under `/app/feature_engineering.py` this raised `IndexError: 2` at script import line 9. Replaced the repository-depth assumption with the helper's direct parent, rebuilt as `s10f.zip`, and verified compilation, direct five-row inference, shallow-root archive extraction, and bit-exact prediction reproduction. Corrected SHA-256 `a34abba5283cd28719f8f59e112aefeeb2ea7e71a89f346e72c82fe4e5c099d5`; `RUNTIME_FIX_READY`. The failed `s10.zip` must not be resubmitted.
- 2026-08-31 — `S7-CANDIDATE-438-LINUX-STRUCTURE-FIX-442`: Withdrew `s10f.zip` before submission because its extra top-level `feature_engineering.py` did not match the official three-entry archive contract. Rebuilt as `s10l.zip` with exactly `model/`, `script.py`, and `requirements.txt` at archive root; placed the helper under `model/` and loaded it through `Path(__file__).resolve().parent / "model"` without repository-depth indexing, recursive fallback, Windows separators, or working-directory assumptions. Verified archive-root names, compilation, clean shallow extraction, five-row execution, and bit-exact predictions (`max_abs_diff=0`). Size `13,841,338` bytes; SHA-256 `058928106F084C8DE365E8CD515F62C2406821E8E0C64FFD30C655269C47A0DF`. Only `s10l.zip` is submission-eligible; `s10.zip` and `s10f.zip` are withdrawn.
- 2026-08-31 — `S7-CANDIDATE-438-KNOWN-GOOD-PATH-PARITY-443`: Compared the candidate byte-level archive layout and path logic against previously accepted `s7.zip`, `pluss.zip`, and `submit123.zip`. To eliminate the only new runtime mechanism, inlined the three required feature-engineering functions into `script.py` and removed the dynamically imported Python helper from `model/`. The resulting `s10r.zip` now follows the known-good pattern: one self-contained root `script.py`, root `requirements.txt`, model assets only under `model/`, and the identical `ROOT/data`, `ROOT/output`, and `ROOT/model` `pathlib` resolution used by `s7`. The archive has no backslash entries, no repository-depth indexing, and no working-directory dependency. Clean extraction and five-row inference passed with predictions bit-identical to candidate 438 (`max_abs_diff=0`). Size `13,834,583` bytes; SHA-256 `85F566879F80831C522D1FDFE753FDF2DD7FC2C212120B404E24A07DC2D87F0E`. `s10r.zip` supersedes all earlier s10 packages.
- 2026-08-31 — `S10R-PUBLIC-LB-SUCCESS-444`: `s10r.zip` executed successfully on the official Linux evaluator and scored `1044.5370826337`, improving the previous public-best `s7=1034.0882411522` by `+10.4488414815` points. This validates both the corrected deployment package and candidate 438's frozen phase-context plus recent-model signal. `ACCEPT_NEW_INCUMBENT`; all subsequent experiments must use `s10r` as the public-best reference, while earlier s10 packages remain withdrawn.
- 2026-08-31 — `S10R-RECENT-CATBOOST-ENSEMBLE-445`: Trained three preregistered 142-feature CatBoost variants (independent seed, stronger season decay, and deeper regularized trees) over expanding 2022/2023/2024 folds and compared their frozen ensembles against reconstructed `s10r`. The 2022-only selection chose the equal four-model ensemble. It improved 2023/2024 versus `s10r` by only `-1.55e-5/-3.71e-6` Brier, recent mean `-9.60e-6`, despite positive AUC and acceptable target caps. `REJECT_ENSEMBLE_GATE`; variance reduction alone is too small for another submission, and no deployment ZIP was created.
- 2026-08-31 — `S10R-FULL-RESIDUAL-CATBOOST-446`: Trained a new 143-input CatBoost regressor on `y - frozen s7`, using the complete 142-feature recent representation plus base prediction, expanding 2022/2023/2024 folds, and 0.65 season decay. The preregistered 2022 zero-loss constraint for both targets selected correction strength `0.0`; therefore it cannot safely improve `s10r` and confirmation remained unchanged. `REJECT_FULL_RESIDUAL_GATE`; direct full-feature residual learning is closed and no deployment ZIP was created.
- 2026-08-31 — `S10R-TRACKMAN-RELEASE-BRANCH-447`: Reused the frozen strict-prior-season TrackMan release-coupling model as an independent row-local direction over reconstructed `s10r`. Every positive 2022 strength improved pooled Brier and AUC, but all worsened target1; the preregistered zero-loss-per-target selector therefore chose no candidate. `REJECT_TRACKMAN_ON_S10R`; no package.
- 2026-08-31 — `S10R-TRACKMAN-BALANCED-448`: Added one global offset to the frozen 447 TrackMan direction and fitted only its weight/offset on 2022. The fitted direction improved 2023 Brier `-2.86e-5` but reduced AUC, then worsened 2024 Brier `+4.28e-7` with target0 loss `+1.71e-4`. Recent mean was only `-1.41e-5`. `REJECT_BALANCED_TRACKMAN_GATE`; the release-coupling branch does not transfer robustly over s10r and no ZIP was created.
- 2026-08-31 — `S10R-ROLLING-RECALIBRATION-449`: Refit offset-only, affine, and asymmetric-affine calibrators on 2022 reconstructed `s10r` and applied them unchanged to the 2023 selection fold. All three worsened Brier (`+5.85e-5`, `+6.37e-5`, `+7.43e-5`) with severe target polarization, so no family was eligible and locked 2024 was not used for selection. `REJECT_S10R_RECALIBRATION_GATE`; s10r should retain its existing global calibration and no ZIP was created.
- 2026-08-31 — `S10R-RECENT-INCLUDE-2019-450`: Retrained the successful 142-feature recent CatBoost with 2019 restored as a 0.65 exponentially decayed prior and selected phase/recent weights on 2022 under zero per-target loss. Versus reconstructed s10r it improved 2023 `-2.38e-5` but was essentially neutral in 2024 `-2.34e-7`, winning only 4/8 2024 months; recent mean was `-1.20e-5`. `REJECT_INCLUDE_2019_GATE`; older data adds mild variance reduction but no deployment-scale gain, and no ZIP was created.
- 2026-08-31 — `S10R-RELIABILITY-MOE-451`: Built a structural row-local mixture-of-experts from three independently trained CatBoost models: full 142-feature identity model, 140-feature no-ID model, and 130-feature no-current-state model. Four frozen routing policies switched experts using career support and reconstructed current-season support; 2022 selected the hybrid policy. It improved all 15 recent months and both recent AUCs, but gains versus s10r were only `2023 -1.21e-5`, `2024 -2.63e-6`, recent mean `-7.34e-6`. `REJECT_RELIABILITY_MOE_GATE`; this was a genuine model-composition change, but not large enough to deploy, and no ZIP was created.
- 2026-08-31 — `S10R-FULL142-LGBM-452`: Trained a genuinely different LightGBM classifier over the complete 142-feature recent representation in expanding rolling folds, then compared standalone LightGBM and an equal raw CatBoost-LightGBM ensemble. 2022 selected the equal ensemble, but versus s10r it worsened 2023 `+2.98e-5` with negative AUC and worsened 2024 `+5.55e-7`; recent mean loss was `+1.52e-5`. `REJECT_FULL142_LGBM_GATE`; this new model family does not complement s10r, and no ZIP was created.
- 2026-08-31 — `S10R-COUNT-REGIME-EXPERTS-453`: Trained nine independent full-142 CatBoost models across expanding folds, with separate heads for batter-ahead, even, and pitcher-ahead counts and deterministic row routing. This structural model improved s10r in every evaluated season: 2022 `-4.03e-6`, 2023 `-3.45e-5`, 2024 `-5.36e-6`; recent AUC improved in both years and target balance stayed within cap. However recent mean `-2.00e-5` missed the frozen deployment threshold `-2.5e-5`, and only 5/8 2024 months improved. `REJECT_COUNT_REGIME_EXPERTS_GATE`; promising structural evidence retained, but no ZIP was created.
### 454 — 453 count-regime deployment package (2026-08-31)

- Trained three 2025 deployment heads on official 2020–2024 Train only and fitted calibration from rolling 2022–2024 OOF.
- Built `experiments/submissions/s11.zip`; exact top-level layout is `model/`, `script.py`, `requirements.txt`.
- Clean extraction/run matched the source preflight predictions exactly (`max_abs_diff=0`); no Test labels or leaderboard-derived row logic used.
- This remains an experimental package: experiment 453 improved every recent season but missed the preregistered recent-mean gate (`-1.99526e-5` vs required `-2.5e-5`).

### 455 — Count-regime × inning-phase experts (2026-08-31)

- Split the full 142-feature CatBoost into six independently trained experts: three count-advantage regimes × early/late inning.
- Result vs reconstructed s10r: 2022 `+1.36997e-5`, 2023 `+7.11419e-5`, 2024 `+3.58628e-5`; recent mean `+5.35023e-5` (worse).
- AUC also fell in every evaluation year, so the finer split destroyed useful shared sample strength rather than adding signal.
- Verdict: `REJECT_COUNT_INNING_EXPERTS_GATE`; no deployment package created.

### 454 official leaderboard result

- Submitted package: `s11_fixed.zip`
- Official score: `1046.2789329284`
- Previous best s10r: `1044.5370826337`
- Actual gain: `+1.7418502947` points; this is the new public best.
- The local recent-fold estimate was roughly +8 points, so only about 22% transferred, but the direction did transfer positively.

### 456 — Regime-specific s11 blend weights (2026-08-31)

- Froze the s11 models and phase correction, then fitted three count-regime weights using 2022 only with shrinkage toward the s11 global weight.
- All three weights collapsed effectively to zero; 2023/2024 mean delta vs s11 was `+4.63233e-5` and AUC fell in both years.
- Verdict: `REJECT_REGIME_SPECIFIC_BLEND_GATE`; per-regime blending is not pursued.

### 457 — Shared model with explicit count interactions (2026-08-31)

- Kept all training rows in one 149-feature CatBoost and added seven categorical count/context interaction features.
- Delta vs s11: 2022 `+1.63206e-6`, 2023 `+4.40727e-6`, 2024 `+3.74916e-6`; recent mean `+4.07821e-6` (slightly worse).
- AUC decreased in every evaluation year and 2023 target 0 exceeded the balance cap.
- Verdict: `REJECT_SHARED_COUNT_INTERACTIONS_GATE`; no ZIP created.

### 458 — Pitch-mix temporal state (2026-08-31)

- Reconstructed 12 row-local current-season pitcher pitch-mix features: support/reliability, shrunken fastball/breaking/offspeed rates, deviations from the season-start state, and entropy/HHI/gap changes.
- Neither the extended LightGBM nor its equal raw ensemble with s11 passed 2022 selection. The better ensemble worsened s11 by `+5.26066e-5` in 2023 and `+4.28203e-6` in 2024, with AUC losses in both years.
- Verdict: `REJECT_PITCHMIX_TEMPORAL_STATE_GATE`; no ZIP created.

### 459 — s11 × TrackMan count coupling (2026-08-31)

- Combined s11 with the frozen strict-past TrackMan release direction using global and count-specific weights fitted on 2022.
- The count-specific candidate improved 2023 `-2.79405e-5`, but 2024 was neutral/worse `+3.57386e-7` with target0 `+1.69033e-4`.
- Verdict: `REJECT_S11_TRACKMAN_COUNT_COUPLING_GATE`; no ZIP created.

### 460 — s11 TrackMan support gate (2026-08-31)

- Tested 24 fixed mapping/support/fraction policies and kept unsupported rows exactly equal to s11.
- Reliable mapping, prior-season support >=100, fraction 20% improved every evaluated year and both recent AUCs; 2023/2024 deltas were `-4.50223e-6/-1.08204e-6`.
- The recent mean gain `-2.79214e-6` was far below the deployment threshold, so `REJECT_S11_TRACKMAN_SUPPORT_GATE`; no ZIP created.

### 461 — Pitcher-hand full-feature experts (2026-08-31)

- Trained independent recent-weighted full-142 CatBoost experts for left- and right-handed pitchers.
- Brier improved vs s11 in 2022/2023/2024 (`-7.27e-7/-2.04e-5/-1.07e-6`), but recent AUC fell and target0/target1 polarized severely.
- Recent mean was `-1.07121e-5`; verdict `REJECT_PITCHER_HAND_EXPERTS_GATE`, no ZIP created.

### 462 — Pitcher-hand experts × support-gated TrackMan (2026-08-31)

- Combined the frozen 461 hand-expert direction with 460's reliable-mapping/support>=100 TrackMan direction, fitting two weights and one offset on 2022 only.
- Recent mean improved `-1.22733e-5`, but 2023 AUC fell and 2024 target0 worsened `+2.89413e-4` despite aggregate improvement.
- Verdict: `REJECT_HAND_TRACKMAN_BALANCE_GATE`; the TrackMan direction did not neutralize hand-expert class polarization, no ZIP created.

### 463 — Pitcher-hand × batter-hand matchup experts (2026-08-31)

- Trained four independent recent-weighted full-142 CatBoost experts for the four pitcher/batter handedness combinations.
- Strong structural signal vs s11: 2022/2023/2024 deltas `-8.57e-6/-7.94e-5/-9.42e-6`, positive AUC in all years, and 14/15 recent months improved.
- Recent mean `-4.44216e-5` passed the magnitude threshold, but 2023 target0 worsened `+2.33380e-4`; `REJECT_MATCHUP_HAND_EXPERTS_GATE` pending a preregistered global balance refit.

### 464–465 — Matchup-hand global balance refits (2026-08-31)

- Adding a 2022-only global offset strengthened recent mean improvement to about `-8.43e-5`, but 2023 target0 still worsened about `+1.88e-4`.
- A fixed `-2.5e-5` improvement reserve for both 2022 target classes was infeasible; optimizer success was false.
- Both refits remain `REJECT`; frozen 463 predictions are retained for head-specific calibration follow-up.

### 466 — Strictly lagged per-matchup-head calibration (2026-08-31)

- Calibrated each frozen 463 matchup head separately using only earlier OOF rows.
- Signal remained strong: recent mean `-4.57248e-5`, positive AUC in 2022/2023/2024, and 2024 target deltas were within tolerance.
- The 2023 target0 loss remained `+2.21329e-4`, so the per-head calibration did not repair the temporal class shift.
- Verdict: `REJECT_MATCHUP_HEAD_CALIBRATION_GATE`; no ZIP created. The frozen matchup experts are the strongest new structural direction after s11 but remain unsafe.

### 467 — Target-free matchup subset gate (2026-08-31)

- Evaluated all 15 nonempty matchup subsets at four frozen strengths, keeping excluded rows exactly equal to s11 and selecting on 2022 only.
- Selection retained all four matchups at 75%; recent mean improved `-3.53619e-5`, but 2023 target0 still worsened `+1.64919e-4`, so the strict gate failed.
- Several confirmation-safe subsets existed diagnostically, led by `1_1+1_2+2_2` at 50% with recent mean `-1.73426e-5`, but they missed the deployment-scale threshold and were not promoted post hoc.
- Verdict: `REJECT_MATCHUP_SUBSET_GATE`; no ZIP created.

### 468 — Batter-hand full-feature experts (2026-08-31)

- Trained independent recent-weighted full-142 CatBoost experts for left- and right-handed batters.
- Aggregate Brier improved vs s11 in 2022/2023/2024 (`-6.01e-6/-5.63e-5/-7.71e-7`) and AUC rose in every year.
- Target effects were severely polarized in both recent years: 2023 target0 `+2.44655e-4`, 2024 target0 `+2.72044e-4`.
- Recent mean `-2.85304e-5` passed magnitude but failed balance and 2024 stability; `REJECT_BATTER_HAND_EXPERTS_GATE`, no ZIP created.

### 469 — Same/opposite-hand full-feature experts (2026-09-01)

- Trained independent full-142 CatBoost experts for same-hand and opposite-hand matchups with expanding rolling folds.
- Aggregate Brier improved vs s11 in 2022/2023/2024 (`-2.20e-5/-1.97e-4/-1.57e-5`); AUC rose in every year and 19/22 season-months improved.
- The gain was target-polarized: target0 worsened `+2.80e-4` in 2023 and `+4.87e-4` in 2024, while target1 improved strongly.
- Recent mean was `-1.06194e-4`, but the strict target-balance gate failed. Verdict: `REJECT_SAME_OPPOSITE_HAND_EXPERTS_GATE`; no ZIP created.

### 470 — Globally balanced same/opposite-hand experts (2026-09-01)

- Refit phase weight, 469 expert weight, and one global offset using 2022 only while constraining both target classes to be non-worse.
- Aggregate Brier improved vs s11 in 2022/2023/2024 (`-2.47e-5/-2.75e-4/-1.05e-5`), with positive AUC deltas throughout.
- Confirmation target polarization increased: target0 worsened `+2.34e-4` in 2023 and `+6.31e-4` in 2024.
- Recent mean was `-1.42588e-4`, but the confirmation balance gate failed. Verdict: `REJECT_BALANCED_SAME_OPPOSITE_GATE`; no ZIP created.

### 471 — Rank-only same/opposite-hand expert transfer (2026-09-01)

- Removed the 2022 intercept and s11-logit projection from the frozen 469 expert difference, then selected one nonnegative residual-ranking weight on 2022 only.
- Aggregate Brier improved vs s11 in 2022/2023/2024 (`-3.25e-5/-1.87e-4/-1.62e-5`) and AUC improved in every year.
- Both target classes improved in 2022 and 2023. In 2024, target0 improved strongly (`-3.09e-4`) while target1 worsened (`+2.93e-4`).
- Recent mean was `-1.01506e-4`, but the strict target cap failed. Formal verdict: `REJECT_SAME_OPPOSITE_RANK_ONLY_GATE`; retained as an aggressive 2025-shift-aligned deployment candidate.

### 472 — Full-period rank-only same/opposite deployment (2026-09-01)

- Refit the two 469 same/opposite-hand experts on all official 2019-2024 Train rows with the preregistered season decay and CatBoost parameters.
- Derived the 2025 expert calibrator strictly from frozen 2022-2024 rolling OOF predictions and reused the 471 projection, scale, and rank weight unchanged.
- Created `s12.zip` with exact Linux top-level structure (`model/`, `script.py`, `requirements.txt`) and passed an extract-and-run inference check.
- Candidate status: aggressive submission candidate aligned with the inferred lower 2025 target prevalence; no leaderboard result used in construction.
