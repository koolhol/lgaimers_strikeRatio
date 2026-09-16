# Strike Ratio

LG Aimers Phase 2 야구 제구 성공 확률 예측 프로젝트입니다. 각 투구 직전까지 확인할 수 있는 정보만으로 `control_success=1`의 확률을 예측합니다.

- 프로젝트 기간: **2026.08.05 ~ 2026.09.02**
- 평가 지표: Brier Skill Score
- 공식 확인 최고 점수: **1046.2789329284** (`s11_fixed.zip`)
- 최종 모델: `final_model/`의 472 rank-only same/opposite-hand ensemble

> 공식 최고점과 최종 연구 후보는 다릅니다. 472는 로컬 rolling-origin 검증 후 최종화했지만, 최초 제출 패키지의 자산 압축 해제 오류 때문에 리더보드 점수는 확인하지 못했습니다. 저장소의 최종 패키지는 POSIX 경로 ZIP으로 다시 구성하고 자산 무결성 검사를 추가했습니다.

## 문제와 평가식

예측값 `p_i`와 정답 `y_i`에 대해:

```text
Brier Score = mean((p_i - y_i)^2)
Reference Brier = r * (1 - r),  r = mean(y_i)
Score = max(0, 100000 * (1 - Brier Score / Reference Brier))
```

확률의 순위뿐 아니라 calibration이 직접 점수에 영향을 줍니다.

## 최종 모델 구조

1. 현재 시즌 투수 상태를 반영한 LightGBM 2개와 CatBoost
2. 타자 현재 시즌 및 타자 ID CatBoost
3. count 상태별 CatBoost 전문가 3개
4. 경기 phase 보정
5. 동일 손/반대 손 CatBoost 전문가 2개
6. 마지막 두 전문가는 확률 수준을 직접 섞지 않고 기존 모델과 직교화한 **rank residual**만 결합

마지막 설계는 동일/반대 손 전문가의 AUC 개선은 유지하면서, 연도별 평균 확률과 타깃 편향을 줄이기 위해 선택했습니다.

## 주요 시도와 결론

| 방향 | 결과/판단 |
|---|---|
| LightGBM, XGBoost, CatBoost 기본 모델 | 강한 tabular 기준선 구축 |
| 현재 시즌 투수·타자 통계, ID 모델 | 최종 앙상블의 핵심 신호로 채택 |
| TabM, FT-Transformer, Wide&Deep, SSL | 검증상 안정적인 우위가 없어 미채택 |
| 전역 affine/polynomial calibration | 가장 큰 리더보드 상승을 만든 핵심 단계 |
| TrackMan 투수 매핑 및 파생 피처 | 약 80% 수준의 매핑 coverage를 확보했으나 2025 전이 불안정으로 최종 제외 |
| 동적 Beta/상태공간, residual 보정 | pooled Brier는 개선했지만 시즌 또는 타깃 균형 실패 |
| count/hand 세그먼트 보정 | 일부 개선했으나 세밀한 lookup은 과적합 위험으로 중단 |
| 동일 손/반대 손 전문가 | 모든 연도 AUC 개선, 확률 자체는 타깃 편향 발생 |
| rank-only 결합 | 2022~2024 Brier와 AUC가 모두 개선되어 최종 연구 후보로 채택 |

상세 실험 이력은 [`docs/EXPERIMENT_LOG.md`](docs/EXPERIMENT_LOG.md), 수치 테이블은 [`docs/results.csv`](docs/results.csv)에 있습니다.

## 해결한 핵심 문제

- 시간 누수 방지: 모든 누적 통계는 strict-past/as-of 방식으로 구성했습니다.
- 배포 이동: pooled 검증보다 2023·2024 rolling-origin 결과와 타깃별 Brier를 우선했습니다.
- 확률 보정: Brier 기준으로 전역 calibration을 별도 최적화했습니다.
- 전문가 편향: 새 전문가의 확률을 그대로 섞지 않고 기존 예측 logit에 직교한 순위 잔차만 사용했습니다.
- TrackMan ID 불일치: 시즌×월 활동 fingerprint, 손잡이, mutual-best, 후보 margin을 이용해 매핑을 감사했습니다.
- 제출 재현성: Windows 절대경로를 제거하고 `Path(__file__)` 기준 상대경로만 사용합니다.
- ZIP 경로 오류: PowerShell `Compress-Archive` 대신 POSIX 엔트리를 생성하는 `tar` 패키징으로 고정했습니다.
- 자산 누락: 패키징 전후 SHA-256과 ZIP 내부 필수 파일 목록을 검사합니다.

## 실행

평가 서버와 같은 구조로 데이터를 둡니다. 대회 데이터는 라이선스와 용량 문제로 저장소에 포함하지 않습니다.

```text
final_model/
├── model/
├── data/
│   ├── test.csv
│   └── sample_submission.csv
├── output/
├── script.py
└── requirements.txt
```

```bash
pip install -r final_model/requirements.txt
python final_model/script.py
```

결과는 `final_model/output/submission.csv`에 생성됩니다.

## 제출 ZIP 생성 및 검증

Windows PowerShell에서:

```powershell
./tools/build_submission.ps1
```

생성물은 `dist/submit.zip`입니다. ZIP 최상위에는 정확히 `model/`, `script.py`, `requirements.txt`만 들어갑니다. 내부 경로 구분자는 `/`입니다.

## 저장소 구성

```text
Strike_Ratio/
├── final_model/             # 최종 추론 코드와 모델 자산
├── tools/                   # 제출 패키징·무결성 검사
├── docs/                    # 전체 실험 기록과 사전등록 설정
├── README.md
└── .gitignore
```

## 재현성과 규칙 준수

- 공식 제공 Train 데이터와 허용된 보조 데이터만 사용했습니다.
- 테스트 정답 또는 정답에 준하는 정보는 사용하지 않았습니다.
- 행별·ID별 리더보드 탐색이나 특정 테스트 행 후처리는 하지 않았습니다.
- 최종 추론은 네트워크 연결 없이 동작합니다.
- 데이터와 생성 결과는 Git에서 제외합니다.

## 한계

- 2025 평가 분포가 과거 시즌과 달라 로컬 개선이 리더보드로 그대로 전이되지 않는 사례가 있었습니다.
- 최종 472 모델은 타깃별 안정성 게이트를 엄격하게는 통과하지 못한 공격적 후보입니다.
- 공식적으로 점수가 확인된 가장 안전한 모델은 `s11_fixed.zip`의 1046.2789329284입니다.

