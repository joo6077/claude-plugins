# Sprint Feedback
Feature: Codex 감독 구독 사용량 상한 · API 키 로그인 막기 · 금액 코드 지우기
Evaluated: 2026-10-08 19:19
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-codex-audit-usage-cap.md
- sha256: 630cba5024602824d4381d21f8c945c542529aef0ccd135be342542402c753e2 (status done 반영 뒤)
- slug: codex-audit-usage-cap
- seal_status: SEAL_OK · measure_status: MEASURE_OK
- 봉인 커밋 대조: seal_commit=3c41c6e0(계약 파일 1개), 차이 0
- status_transition: active -> done

## Amendments
- amendments: 1 (AM-01 relaxing · 스크립트-03 revise 보고서 폴더 draft-r*, consent anchored 2026-10-08T10:10:50.823Z)

## Deletions
- deletions_range: b699b17e..dd3d40e5, 삭제 1 — harness/templates/codex-audit/prices.json (sprint-scope 안)

## Results

판정 방식: Codex 를 부르지 않았다(감독 mode: off). 측정은 가짜 codex 측정 묶음.

| 조건 | 판정 | 측정 |
|---|---|---|
| 스크립트-01 | PASS | (a)~(l) 전부 — 창별 resets_at > 지금 · used >= 상한, 못 읽는 줄 건너뜀, 실패 원인에 창 · % · 상한 · 풀리는 시각 |
| 스크립트-02 | PASS | limits 5시간 12 · 주간 3, usd · plan 없음, ## 사용량 · follow 차례 끝 줄, 시간 초과 차례도 기록 |
| 스크립트-03 | PASS | API 키 2 종 × impl · draft · revise 와 auth.json 없음 — 종료 2 · 로그인-없음 · exec 0 · 모델 확인 절 없음 |
| 스크립트-04 | PASS | 오늘 차례 1 · 5시간 12% · 주간 3% · 풀리는 시각, 달러 없음 |
| 스크립트-05 | PASS | 앞 측정 묶음 8 개 종료 0 |
| 스크립트-06 | PASS | draft m-draft · judge m-impl |
| 스킬-01 · 구조-01 · 재사용-01 | PASS | 낱말 · 옛 낱말 0, 바뀐 경로 6 개, 금지 낱말 0 · subscription( 2 곳 · prices.json 없음 |
| 금지-03 · 금지-04 | PASS | validate-plugin 종료 0 |
| 재사용-02 · 진단-01 · 진단-03 | N/A | 계약 사유 |
| 진단-02 · 진단-04 | PASS | 더한 줄 경고 0 · 측정 전체 · 로컬 CI 34 개 실패 0 |

음성 대조: 스크립트-01 · 02 · 03 · 04 --base 모두 종료 1.
변이 시험: 첫 값 · null 포함 마지막 값 → 02 · 04, 마지막 줄만 → 01, > 비교 → 01, 한 창 풀리면 줄 무시 → 01, 구독 확인을 모델 확인 뒤로 → 03, follow 사용량 비움 → 02, 시간 초과 기록 생략 → 02, 못 읽는 줄 건너뛰기 제거 → 01. 전부 FAIL 로 잡힘.

## 개선 제안 (판정 영향 없음)
1. [스크립트-04] 측정-방식-불일치 — 어제 줄까지 센 변이도 저장소별 줄이 차례 1\b 에 맞아 통과. 헤더 줄만 ^오늘 \(\S+\) 차례 1$ 로 재면 좁혀진다.
2. [스크립트-01] 측정-방식-불일치 — 상한 100 경계, used 가 null 인 창 빼기는 측정 없음(구현은 맞음).

## Cross-Diagnosis
- 상태: done (부모가 새 에이전트로 실행)
- 1. 뜻과 다르게 읽힌 조건: 판정을 뒤집는 것은 없음. 중간 — 스크립트-04 측정이 저장소별 줄에도 맞아 어제 줄까지 센 변이가 통과(재현함). 구현은 맞다
- 2. 0 건으로 거저 통과: 없음. 낮음 — (j) 는 사용 · 상한이 둘 다 70 이라 상한 표기 검사가 겹친다. 측정 안 된 상한 100 경계 · null 창은 직접 넣어 계약대로 동작함을 확인
- 3. 실제 세션 기록: 구독 기록 3 개에서 limits 가 5시간 57/60/63% · 주간 17/17/18% 로 정상 판독. plan_type 이 "plus" 로 찍힘(계약 배경은 Pro). 낮음 — 줄에 시각이 없어 늦게 붙은 낮은 값이 최신으로 읽힐 수 있음, 사용 기록 파일 정리 없음, 동시 덧붙이기는 안전
