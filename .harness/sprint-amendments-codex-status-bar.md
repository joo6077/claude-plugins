# Sprint Amendments — codex-status-bar / 개정 1

봉인 기준은 원 계약 `.harness/sprint-contract-codex-status-bar.md` 의 봉인 커밋 `92c262d3` 이다. 조건 줄 · 측정 줄 · 봉인 필드는 고치지 않는다. 아래 한 건은 측정 묶음(`.harness/.meta/codex-status-bar/measure/measure.py`)의 실패 문구만 고친 것이다.

## 동의

- 질문: AskUserQuestion 「봉인 뒤 측정 스크립트의 실패 문구 두 줄을 고쳤습니다. 개정으로 인정할까요?」(고친 내용과 이전 · 이후 동작을 질문에 적었다). 답: 「동의 (추천)」.
- 앵커: `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/35b5945f-4957-4359-9b18-2d22b3bafeb0.jsonl` 5728 행 응답(**동의 시각** `2026-10-09T02:38:21.988Z`, uuid `93d63441-27b4-4850-917e-cab622fd4d56`), cwd `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-status-bar`.
- consent: anchored. 선후: 측정 수정은 구현 커밋 `6310b0e7` 뒤 · 동의 전에 작업 폴더에서 고쳤고, 이 파일과 함께 동의 뒤에 커밋한다.

## AM-01 — relaxing · 스크립트-03 (f) · (j) 실패 문구의 `%`

- 변경: `'(f) 사용량 없으면 % 없이: %s' % f` 와 `'(j) 풀린 창은 % 를 빼야 한다: %s' % j` 의 낱 `%` 를 `%%` 로 바꿨다. 판정식(`check(...)` 의 첫 인자)은 그대로다.
- 이유: 파이썬 `%` 서식은 판정 전에 문구를 먼저 만든다. 낱 `%` 뒤 한글을 서식 문자로 읽어 `ValueError: unsupported format character` 를 냈다 — 어떤 구현에도 스크립트-03 이 FAIL 하는 통과 집합 공집합 상태였다.
- direction 계산(측정 집합, `amend_direction_oracle`): 원 측정 대상 {(f) · (j) 판정 전에 서식 오류로 끝나는 측정}, 개정 측정 대상 {(f) · (j) 판정식}. removed=1 added=1 → `relaxing measured_removed=1 measured_added=1`.
- 확인: 고친 뒤 `measure.sh 스크립트-03` PASS, `measure.sh 스크립트-03 --base` FAIL(`check_status.js 종료 1`).
