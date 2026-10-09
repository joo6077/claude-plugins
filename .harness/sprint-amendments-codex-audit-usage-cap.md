# Sprint Amendments — codex-audit-usage-cap / 개정 1

봉인 기준은 원 계약 `.harness/sprint-contract-codex-audit-usage-cap.md` 의 봉인 커밋 `3c41c6e0` 이다. 조건 줄 · 측정 줄 · 봉인 필드는 고치지 않는다. 아래 한 건은 측정 묶음(`.harness/.meta/codex-audit-usage-cap/measure/measure.py`)만 고쳐, 측정이 조건 문구를 그대로 재게 바로잡은 것이다.

## 동의

- 질문: AskUserQuestion 「봉인한 뒤 측정 하나를 고쳤습니다. 이 고침을 개정으로 인정할까요?」(고친 내용과 이전 · 이후 동작을 질문에 적었다). 답: 「동의 (추천)」.
- 앵커: `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/35b5945f-4957-4359-9b18-2d22b3bafeb0.jsonl` 5012 행 응답(**동의 시각** `2026-10-08T10:10:50.823Z`, uuid `1344d686-710b-4ed1-9dd7-3d007f0e0bff`), cwd `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-usage-cap`.
- consent: anchored. 선후: 측정 수정은 구현 커밋 `dd3d40e5` 뒤 · 동의 전에 작업 폴더에서 고쳤고, 이 파일과 함께 동의 뒤에 커밋한다.

## AM-01 — relaxing · 스크립트-03 revise 경우의 보고서 폴더

- 변경: revise 경우의 `report.md` 를 `revise-r*` 대신 `draft-r*` 폴더에서 읽는다(`case.report('draft' if verb == 'revise' else verb)`).
- 이유: 감독은 revise 기록을 draft 와 같은 `draft-r<번호>` 폴더에 남긴다(`allocate(meta, slug, 'impl' if verb == 'impl' else 'draft')`). 옛 측정은 없는 폴더를 찾아 어떤 구현에도 「감독 폴더 없음: revise」 로 FAIL 했다 — 통과 집합이 공집합이었다. 조건이 재는 내용(종료 2 · 갈래 `로그인-없음` · 실패 원인 `구독` · exec 0 번 · 로그인 확인 0 번 · TMPDIR 0 · `## 모델 확인` 없음)은 그대로다.
- direction 계산(측정 집합, `amend_direction_oracle`): 원 측정 대상 {`revise-r*` 폴더}, 개정 측정 대상 {`draft-r*` 폴더}. removed={`revise-r*`} added={`draft-r*`} → `relaxing measured_removed=1 measured_added=1`.
- 확인: 고친 뒤 `measure.sh 스크립트-03` PASS, `measure.sh 스크립트-03 --base` FAIL(`plain impl: 종료 0`).
