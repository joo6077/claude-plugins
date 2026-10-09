# Sprint Feedback
Feature: Codex 감독 구독 로그인 — 사본 쓰고 갱신만 되돌려 쓰기
Evaluated: 2026-10-08 16:13
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-codex-audit-auth-writeback.md
- sha256: 856eea7c28d6cb24ad00d63e5ab3b3be9afec383f07a6613278688329ab4d1d1 (status done 반영 뒤)
- slug: codex-audit-auth-writeback
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation
- seal_status: SEAL_OK · measure_status: MEASURE_OK
- 봉인 커밋 대조: seal_commit=2264299f(계약 파일 1개), 측정 묶음 143c84ed 이후 차이 0
- status_transition: active -> done

## Amendments
- amendments: 0

## Deletions
- deletions_range: 2f98abee..a18a996f, 삭제 0

## Results

판정 방식: Codex 를 부르지 않았다(감독 mode: off). 측정은 가짜 codex 측정 묶음, 스크립트-07 만 진짜 `codex sandbox`.

| 조건 | 판정 | 측정 |
|---|---|---|
| 스크립트-01 | PASS | impl · draft · revise 모두 사본, 마지막 차례 토큰 되돌려 씀, 권한 600, 임시 0. 로그인 확인 갱신 · 시간 초과 차례 갱신도 되돌려 씀 |
| 스크립트-02 | PASS | 정상 · SIGTERM 둘 다 새 항목은 허용 3 개 밖 0, `-p` · `-s` 0, 사본 config 에 격리 설정 1 번, SIGTERM 뒤 그 차례 토큰 · 임시 0 |
| 스크립트-03 | PASS | (a) 바깥 변경 보존 (b) 나중 감독이 덮지 않음 (c) 잠금 잡은 3 초 동안 그대로 (d) 잠금 중 SIGTERM 뒤 그 차례 토큰 |
| 스크립트-04 | PASS | 갱신 없으면 바이트 · 수정 시각 동일, 깨진 사본 안 씀, API 키 두 모양 사본 · 잠금 파일 없음 · plan apikey |
| 스크립트-05 | PASS | 차례 번호 없는 차례의 세션 기록이 감독 폴더에 0 |
| 스크립트-06 | PASS | 도중 auth.json 이 깨져도 두 줄 모두 plan chatgpt · 구독 문구, `{` 덮지 않음 |
| 스크립트-07 | PASS | 6 칸 모두 기대대로(사본 auth.json 읽기 막힘 포함) |
| 스크립트-08 | PASS | 앞 묶음 스크립트-05 · 06 종료 0, 로그인 실패 종료 2 · 로그인-없음 · exec 0 · 임시 0 |
| 스킬-01 · 구조-01 · 재사용-01 | PASS | README 낱말 · 옛 문구 넷 없음, 바뀐 경로 2 개, `subscription(` 2 곳 |
| 금지-03 · 금지-04 | PASS | validate-plugin 종료 0 |
| 재사용-02 · 진단-01 · 진단-03 | N/A | 계약 사유 |
| 진단-02 | PASS | 더한 줄 경고 0, 양성 대조 1 이상 |
| 진단-04 | PASS | 측정 전체 PASS · Traceback 0 · 로컬 CI 명령 34 개 실패 0 |

음성 대조: `--base` 로 스크립트-01 · 02 · 04 · 05 · 06 종료 1, 스크립트-03 3 회 모두 종료 1.
변이 시험(임시 복제본): 잠금 제거 → (c) FAIL, 비교 제거 → (a) FAIL, 신호 미루기 제거 → (d) FAIL, 잠금+비교 제거 → (a) FAIL, 임시 파일+os.replace 를 제자리 쓰기로 → PASS(조건에 없음).

## 개선 제안 (판정 영향 없음)
1. [스크립트-03] 측정-방식-불일치 — 임시 파일 + `os.replace` 와 잠금 파일 권한 600 은 배경 서술에만 있고 조건이 재지 않는다. 다음 계약에 넣을 것.
2. [스크립트-08] 갈래 `로그인-없음` 을 report.md 전체에서 찾는다 — 갈래 줄을 짚는 것보다 느슨.
3. 구현 위험 — `write_back` 의 `pthread_sigmask` 는 메인 스레드만 막는다. copier 데몬 스레드가 살아 있으면 미루기가 뚫릴 수 있다(지금 증상 없음).

## Cross-Diagnosis
- 상태: done (부모가 새 에이전트로 실행)
- 1. 뜻을 잘못 읽어 판정이 틀린 조건: 없음. 스크립트-08 · 03(c) 측정이 문장보다 조금 느슨하지만 같은 줄의 다른 확인이 받쳐 준다(낮음)
- 2. 0 건으로 거저 통과한 조건: 없음. 변이 — 신호 미루기 제거는 03(d) FAIL, 제자리 쓰기 교체는 01~04 PASS(조건 밖, 낮음)
- 3. 신호 미루기 빈틈 재현(낮음~중간): 파이썬 신호 처리기는 늘 메인 스레드에서 돌고 `pthread_sigmask` 는 부른 스레드만 막는다. 파이프를 읽는 데몬 스레드가 살아 있으면 막은 구간 안에서 Interrupted 가 터진다(파이썬 3.14.3, 3/3). SIGTERM 경로는 copier.join 을 건너뛰어 생길 수 있다. 결과: 갱신이 버려지거나 `.codex-audit-auth-*` 임시 파일이 남는다. 고칠 안: 쓰는 동안 signal.signal 처리기를 「받은 신호를 적어 두기만」으로 바꿔 끼우고 끝나면 되돌린 뒤 다시 보낸다 — 다음 스프린트 후보
- 덧붙임(낮음): os.replace 가 OSError 로 실패하면 임시 파일이 남는다
