# Sprint Feedback
Feature: Codex 감독 판정 막힘 미리 알리기 · 되돌려 쓰기 신호 빈틈
Evaluated: 2026-10-08 17:51
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-codex-audit-judge-guard.md
- sha256: 430ac7600d036813fe7c381d16fdc588b79df02001f3cad4ba9d0b4ae5d1b717 (status done 반영 뒤)
- slug: codex-audit-judge-guard
- seal_status: SEAL_OK · measure_status: MEASURE_OK
- 봉인 커밋 대조: seal_commit=71376849(계약 파일 1개), 측정 묶음 9a905963 이후 차이 0
- status_transition: active -> done

## Amendments
- amendments: 0

## Deletions
- deletions_range: 452ca7b8..49c5d6cd, 삭제 0

## Results

판정 방식: Codex 를 부르지 않았다(감독 mode: off). 측정은 가짜 codex 측정 묶음.

| 조건 | 판정 | 측정 |
|---|---|---|
| 스크립트-01 | PASS | /tmp · /private/tmp 아래 impl 종료 2 · 설정-오류 · exec 0 · 로그인 확인 0, draft 는 돈다, 밖 · TMPDIR 만 /tmp 인 impl 종료 0 |
| 스크립트-02 | PASS (3 회) | (a) SIGTERM → 그 차례 토큰 · 종료 143 (b) SIGINT · 잠금 못 잡음 → original · 종료 130, 둘 다 중단됨 · Traceback 0 · 새 항목 0 · 임시 0 |
| 스크립트-03 | PASS | auth.json · 잠금 파일 600, 쓰다 만 파일 0 |
| 스크립트-04 | PASS | 앞 측정 묶음 세 가지 종료 0 |
| 스킬-01 · 구조-01 · 재사용-01 | PASS | README /tmp 안내, 바뀐 경로 2 개, pthread_sigmask 0 · write_back 1 |
| 금지-03 · 금지-04 | PASS | validate-plugin 종료 0 |
| 재사용-02 · 진단-01 · 진단-03 | N/A | 계약 사유 |
| 진단-02 | PASS | 더한 줄 경고 0, 양성 대조 35 · 27 |
| 진단-04 | PASS | 측정 전체 PASS · 로컬 CI 34 개 실패 0 |

음성 대조: 스크립트-01 --base 종료 1, 스크립트-02 --base 3 회 모두 종료 1.
변이 시험: 신호 삼킴 → 02(a) FAIL, 되돌리기를 try 끝에 → 02(b) FAIL, /tmp 판정을 TMPDIR 로 → 01 FAIL, realpath 없이 /tmp 만 → 01 FAIL, 현재 폴더 기준 → PASS(못 잡음).

## 개선 제안 (판정 영향 없음)
1. [스크립트-01] 측정-판별력-미기재 — 감독을 저장소가 아닌 폴더에서 부르는 경우를 넣으면 현재 폴더 기준 구현을 거른다.
2. 코드 — 원래 처리기가 파이썬 밖에서 설정된 경우(signal.signal 이 None) 복원에서 TypeError 가능. 지금 실행 경로에는 해당 없음.

## Cross-Diagnosis
- 상태: done (부모가 새 에이전트로 실행)
- 1. 뜻을 잘못 읽어 판정이 틀린 조건: 없음. 낮음 — measure.py script_01 주석이 「현재 폴더로 판정하는 구현을 가려낸다」고 과장(감독을 늘 저장소에서 부른다). 판정은 맞다
- 2. 0 건으로 거저 통과: 없음. 임시 파일 지우기 갈래는 실행되지 않지만 계약이 코드 검토로 밝혔다
- 3. TypeError 걱정: 생기지 않는다. main() 이 처음에 세 신호에 on_signal 을 걸고 write_back 은 그 뒤 메인 스레드에서만 불린다(실측: 시작 값 default_int_handler · SIG_DFL, nohup 으로 SIG_IGN 도 다시 걸린다)
- 덧붙임(낮음): 처리기를 바꿔 끼우고 되돌리는 짧은 순간에 다른 신호가 오면 끝마무리 중 Ctrl-C 하나가 묻힐 수 있다. 갱신은 버려지지 않는다. 코드 검토 대상
