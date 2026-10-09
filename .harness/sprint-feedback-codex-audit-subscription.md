# Sprint Feedback
Feature: Codex 감독 구독 로그인 · 역할별 모델
Evaluated: 2026-10-08 14:28
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-codex-audit-subscription.md
- sha256: 6c43130aa38a0f2ad3770de69584eefe252635a0b8a47bf7dc45b40fe7b93d83
- status: active
- slug: codex-audit-subscription
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (부모가 절대경로로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (bash · zsh 둘 다)
- contract_seal_broken: n/a
- measure_status: MEASURE_OK
- 봉인 커밋 대조: seal_commit=875b6703(계약 파일 1개만), 지금 판과 차이 0줄 — 재봉인 없음
- status_transition: active -> done

## Amendments
- amendments: 0 (개정 파일 없음)

## Deletions
- deletions_range: da5cf49a..fe7fae75
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: done (부모가 새 에이전트로 실행, 아래 Cross-Diagnosis)

## Results

판정 방식: Codex 를 부르지 않았다(감독 mode: off). 측정은 가짜 codex 측정 묶음, 스크립트-03 만 진짜 `codex sandbox`(codex 0.160.1).

| 조건 | 판정 | 측정 |
|---|---|---|
| 스크립트-01 | PASS | impl · draft · revise 모두 `CODEX_HOME` = 감독 폴더(로그인 확인 포함), 토큰은 마지막 차례 `refreshed-N` |
| 스크립트-02 | PASS | 정상 끝 · SIGTERM 둘 다 프로필 파일 0 개, `config.toml` 바이트 동일, `enabled = false`, `-s` 0 개 |
| 스크립트-03 | PASS | copy-write=ok · input-read=ok · input-write=no · ssh-read=no · auth-read=no (5 칸 모두 잼) |
| 스크립트-04 | PASS | API 키 두 모양 모두 사본, TMPDIR 항목 0, auth.json 동일, plan apikey |
| 스크립트-05 | PASS | 역할별 모델 네 조합 + `CODEX_AUDIT_MODEL`, 판정 인자에 `model_reasoning_effort="max"` |
| 스크립트-06 | PASS | 구독 문구 · usd null · plan chatgpt · 상한 건너뜀. API 키는 종료 2 `한도-예산`, 차례 줄 `0.49달러` |
| 스크립트-07 | PASS | 두 감독 `-p` 이름 다름, 한쪽 끝나도 다른 쪽 파일 남음, 새 항목 · 사라진 항목 없음 |
| 스크립트-08 | PASS | 로그인 확인 `CODEX_HOME` = 감독 폴더, 실패면 종료 2 `로그인-없음` · exec 0 |
| 스킬-01 | PASS | README · 템플릿 · SKILL.md 에 낱말 있음 |
| 구조-01 | PASS | 바뀐 경로 4 개 모두 범위 안, `codex-audit.sh` 포함 |
| 금지-03 · 금지-04 | PASS | validate-plugin 두 검사 종료 0 |
| 재사용-01 | PASS | `def judge_profile(` 1 개, `'[' + table + ']'` 1 곳, `[permissions.` 0 개 |
| 재사용-02 · 진단-01 · 진단-03 | N/A | 계약 사유 사실 확인 |
| 진단-02 | PASS | 더한 줄 경고 0, 양성 대조 35 · 132 · 31 |
| 진단-04 | PASS | bash -n 0 · validate-plugin 0 · 측정 묶음 PASS 12 · FAIL 0 · Traceback 0 · 로컬 CI 명령 34 개 실패 0 |

음성 대조: `--base` 로 스크립트-01~08 · 스킬-01 모두 종료 1.
변이 실험 8 개(늘 감독 폴더 사용 · 프로필 안 지움 · 구독 금액 · 상한 늘 건너뜀 · model_draft 무시 · 로그인 확인 사본 · 끝낼 때 사본 처리 · 판정 인터넷 허용) 전부 해당 조건이 FAIL 로 잡음.
[미검증] 0 건, env_gaps 0 건, 커버리지 18/18.

## 개선 제안 (판정 영향 없음)
1. [스크립트-02] 측정-환경-오염 — `cleanup()` 의 파일 분기를 지워도 PASS. 정상 경로 `finally` 가 먼저 지우기 때문. 계약은 정상 끝 · SIGTERM 만 요구하고 둘 다 잰다.
2. [스크립트-04] 측정-방식-불일치(약함) — 「감독 폴더가 아님」만 확인하고 임시 뿌리 아래 사본인지는 안 본다.
3. [측정 묶음] 측정-환경-오염 — 스크립트-07 이 FAIL 로 끝나면 `cji-measure-*` 임시 폴더가 약 10MB 씩 남는다(PASS 때는 안 남음).

## Cross-Diagnosis
- 1. 뜻을 잘못 읽어 판정이 틀린 조건: 없음
- 2. 0 건으로 통과했을 측정: 판정을 뒤집는 것 없음. 좁게 재는 곳 둘(낮음) — 스크립트-04 는 exec 호출만 보고 로그인 확인은 안 본다(measure.py 341행), 스크립트-02 SIGTERM 칸은 cleanup() 파일 분기를 실행하지 않는다
- 계약 밖 구현 결함:
  - (중간) 구독 경로는 감독 폴더를 지우지 않아 codex 부산물(logs · state · thread_history · memories sqlite, shell_snapshots)이 쌓이고 키 가리기를 안 거친다. 기억 기능이 켜져 있으면 앞 판정이 다음 판정에 섞일 수 있다. `~/.codex-qa` 에 `memories_1.sqlite` · `thread_history_1.sqlite` 가 이미 있다(10-06 생성)
  - (중간) 차례 번호를 못 받은 차례의 세션 기록이 감독 폴더 sessions 에 남는다
  - (중간, 미실측) 동시 감독이 갱신 열쇠를 함께 쓴다 — 한 번 쓰면 버려지는 열쇠면 한쪽 로그인이 끊길 수 있다
  - (낮음) `subscription()` 을 여러 번 다시 읽어, 다른 감독이 auth.json 을 쓰는 순간 한 차례가 API 키 경로로 빠질 수 있다
  - (낮음) SIGKILL · 전원 차단 때 `codex-audit-*.config.toml` 이 남는다
- 측정 묶음 결함(중간): 스크립트-07 이 FAIL 로 끝나면 따로 뜬 가짜 codex 가 release 파일을 기다리며 남는다. 7 개 남은 것을 부모가 kill 로 정리했다
