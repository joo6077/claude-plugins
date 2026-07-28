# Evals 정합성 점검 — 2026-07-27 카이젠 사이클

`scripts/sync-evals.py --check-only` 실행 결과: **0 added / 0 orphans / 0 missing**.
각 플러그인의 `skills/` 디렉토리와 `evals/evals.json` 의 `id` 집합이 일치한다.

점검 대상: flutter-toolkit · rust-kit · react-kit · design-kit · backend-kit · infra-kit

## 이번 사이클 evals 내용 변경 (id 집합 변경 없음 — assertion/케이스 품질 개선)

| 킷 | 변경 | Phase |
| -- | ---- | ----- |
| flutter-toolkit | id 5·8·12·16 assertion 보강 + id 20 신규 (flutter-provider 비트리거 조건) | 5 |
| design-kit | 20 → 27 케이스 (시각변경 protocol·승인기록·Evidence Validity 관련 7건 신규) | 6 |
| onboarding-kit | v0.1.0 → v0.2.0. `flutter-fcm-ios` 를 Flutter 실측 API 로 교체(네이티브 호출 negative assertion), `deprecated-api-warning` → `deprecation-claim-fidelity` 재정의, 신규 2건(`source-ledger-per-step` · `no-invented-paths`), 각 케이스에 `source` 필드 | 14 |

## 특기 사항

onboarding-kit 의 `flutter-fcm-ios` 케이스는 **사용자 피드백 메모리와 정면 모순**하는 상태였다.
메모리(`feedback_setup_guide_stack_first`)가 "스택별 절차가 다르니 스택부터 확정하라"는 사고를
기록하고 있는데, 정작 eval 이 Flutter 가이드에 Flutter 에 존재하지 않는 네이티브 Swift
`FirebaseApp.configure()` 를 요구하고 있었다 — 테스트가 그 사고를 되레 강제하던 셈.
1차 출처(firebase.google.com/docs/flutter/setup)로 확인 후 교체했다.

**교훈**: eval 도 카이젠 대상이다. 스킬 본문만 고치고 eval 을 방치하면 테스트가 결함을 고정한다.
