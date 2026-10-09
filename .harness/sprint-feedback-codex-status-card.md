# Sprint Feedback
Feature: Codex 진행 상황 — 리서치 작업 카드 줄 · 짧은 상태 표시줄 · 표시 결함 고치기
Evaluated: 2026-10-09 13:02
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-codex-status-card.md
- sha256: a6484a467d5ae9f80ec245ed0b0be551da349f7a59759348601a4fb047aa3fb6 (status done 반영 뒤)
- slug: codex-status-card
- seal_status: SEAL_OK · measure_status: MEASURE_OK
- 봉인 커밋 대조: seal_commit=535a21fe(계약 파일 1개), 측정 묶음 4abbf59a 이후 차이 0
- status_transition: active -> done

## Amendments
- amendments: 0

## Deletions
- deletions_range: afbb36f2..9d5ddfe6, 삭제 0

## Results

판정 방식: Codex 를 부르지 않았다(감독 mode: off). 감독은 가짜 codex, 리서치 실행기는 가짜 codex 를 PATH 앞에, 확장은 가짜 vscode 모듈.

| 조건 | 판정 | 측정 |
|---|---|---|
| 스크립트-01 | PASS | Goal 셋째 줄 주제, 1 초 간격 진행 줄 2 개 이상(stderr 만), 20 초 간격 5 초 안 1 개 이하, 40 글자 자르기(보통 · LC_ALL=C), Goal 없으면 첫 줄 |
| 스크립트-02 | PASS | 바로가기 폴더 → 실제 경로 |
| 스크립트-03 | PASS | 작업별 줄 · 요약(감독 1 · 리서치 1 / 리서치 1 / null / 감독 2 · 리서치 1) · 풀이 일반 글자 |
| 스크립트-04 | PASS | 항목 1 개 · 글자 · 풀이, 하나 지우면 감독 1, 살아 있는 채 deactivate 만으로 정리, ID 하나 |
| 스크립트-05 | PASS | 상태 폴더 못 써도 APPROVE · Traceback 없음 · 사용 기록 1 줄, BEAT=1 갱신 |
| 스크립트-06 · 07 · 08 | PASS | 리서치 갱신, 규칙 문장, 앞 묶음 7 개 |
| 스킬-01 · 구조-01 · 재사용-01 | PASS | README 낱말, 바뀐 경로 6 개, extension.js 판단 없음 |
| 금지-03 · 금지-04 | PASS | validate-plugin 종료 0 |
| 재사용-02 · 진단-01 · 진단-03 | N/A | 계약 사유 |
| 진단-02 · 진단-04 | PASS | 더한 줄 경고 0 · 로컬 CI 34 개 실패 0 |

음성 대조: 스크립트-01 · 02 · 05 --base 종료 1.
변이 시험: stdout 진행 줄 → 01(b1 · b3), 끝에 한 번 → 01(b1), 첫 줄 주제 → 01(a), record_usage 보호 안 함 → 05(a), 작업마다 항목 → 04(a) 모두 FAIL 로 잡힘. CLAUDE.md 「앞에서 기다리며」 를 래퍼 앞에 되살림 → 못 잡음(측정 구멍).

## 개선 제안 (판정 영향 없음)
1. [스크립트-07] 측정-방식-불일치 — 「직접 부를 때는」 앞쪽에 「앞에서 기다리며」 가 0 번인지도 재야 한다.
2. 참고 — 경과를 시도마다 다시 세는 변이는 CODEX_TRIES=1 측정으로 못 가린다(구현은 실행기 시작부터 세어 맞다).

## Cross-Diagnosis
- 상태: done (부모가 새 에이전트로 실행)
- 1. 뜻과 다르게 읽힌 조건: 판정을 뒤집는 것 없음. 중 — 스크립트-07 이 앞쪽 「앞에서 기다리며」 를 안 잰다(지금 파일은 1 개뿐이라 결과는 맞음). 하 — 경과 기준을 CODEX_TRIES=1 로 못 가림, (c) 보통 로캘이 측정 환경을 물려받음
- 2. 헛통과: 없음(빈 목록 참이 되는 자리는 다른 확인이 받침). 하 — BEAT 기본 · 상한, 큰따옴표 낱말, 메모 예외 문장은 측정 없음
- 3. 계약 밖: 중 — 작업 카드에 stderr 진행 줄이 실제로 뜨는지 측정 없음(실제 세션에서 확인 필요). 중 — MEMORY.md 목차 줄이 옛 문구(부모가 고침). 하 — 출력 섞임 없음 · 로그 길이 작음 · TERM 정상 · set -u 문제없음 · 세션 없으면 ---- · 진행 줄 사용량은 늦은 값일 수 있음 · run_tag 의 남은 한도가 가장 최근 세션 파일을 짐작(범위 밖) · 작업 폴더 밖에서 부르면 상태 표시줄에 안 뜸
