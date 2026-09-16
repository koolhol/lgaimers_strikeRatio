# Final model card

- Candidate: 472
- Stable official reference: s11, 1046.2789329284
- Training seasons: 2019~2024
- Validation: expanding rolling-origin evaluation on 2022, 2023, 2024
- Output: probability of `control_success=1`
- Libraries: LightGBM 4.6.0, CatBoost 1.2.10

The final candidate extends s11 with two full-feature CatBoost experts split by same-hand versus opposite-hand matchups. Only the component of their logit difference orthogonal to the incumbent prediction is transferred. The blend strength and projection were frozen from 2022, then checked unchanged on 2023 and 2024.

Validation deltas versus s11 for experiment 471:

| Season | Brier delta | AUC delta |
|---|---:|---:|
| 2022 | -0.00003250 | +0.00030838 |
| 2023 | -0.00018680 | +0.00045012 |
| 2024 | -0.00001621 | +0.00018615 |

Risk: 2024 target 1 worsened while target 0 improved, so this is an aggressive distribution-shift candidate rather than the verified stable leaderboard model.
