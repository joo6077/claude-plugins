---
feature: "사용자 훅 · 핸드오프 스킬 (레포 밖) — US-1 ~ US-5"
slug: after-0926-user-hooks
created: "2026-09-27 11:09"
complexity: "복잡"
conditions: 21
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:92961b02c19bb6a0
locked_at: "2026-09-27 11:22"
---

## 배경

- 출처: 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md` 「## user」 절 US-1 ~ US-5. 원 출처는 부모 목록 `followups.md` 셋째(FU-3) · 아홉째(FU-9) 줄, `.harness/.meta/after-kaizen-0926/b-user-setup-notes.md` 「다음에 합칠 것」 세 줄, `c4d-notes.md:33`(user-setup:P6 판단).
- 합의: 사용자 위임으로 받았다 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72`, 2026-09-26T10:09:00.557Z 「123다실행해 …」 와 결정 답 2026-09-26T10:30:16.222Z, 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 …」. 결정 파일 `decisions.md` PD-1 에 US-5 를 맞춘다.
- 이 묶음만 레포 밖 파일을 고친다. 레포에는 계약 · 사본 · 시험 도구 · 결과만 들어간다.
- 복잡도 4 축: 레이어 — 훅 셸 세 개 · 스킬 문서 한 개 (여럿) / 공개 형식 변경 — 예 (핸드오프 틀의 폐기 칸 형식과 세션 마감 훅 안내 형식이 바뀐다) / 소비면 — 예 (다음 세션이 핸드오프 파일과 복붙 블록을 읽는다) / 회귀 위험 — 예 (병렬 세션 훅의 커밋 판별이 바뀌면 놓침 · 헛경고가 생긴다). 넷 다 예라 「복잡」.
- 고치기 전 실측 (`us-result-before.txt`, 61 줄): 작업 알림 원문을 넣으면 세션 마감 안내가 뜬다(`N1 empty=0`), 따옴표 안 「git commit」 에 경고 · 커밋 뒤 알림이 뜬다(`Q1-pre empty=0` · `Q1-post landed=1`), `GIT_INDEX_FILE=` 을 `git add` 에만 붙이면 개인 인덱스 목록을 보인다(`I1-pre mine=1 private=1`), 폐기 칸이 원문 자리를 안 가리킨다(`H1 pline_prd=0`), 핸드오프 커밋에 옛 모델 이름이 실린다(`SK5 coauthor_old=1`).
- 실제 세션에서도 재현했다 (`us-e2e-before.txt`): 백그라운드 명령 설명에 「다음 세션」 이 든 작업 알림 하나에 세션 마감 안내 1 건(`handoff_ctx=1`, 사용자 프롬프트에는 그 낱말 없음 `prompt_kw=0`), 따옴표 안 「git commit」 명령 하나에 커밋 전 경고 1 · 커밋 뒤 알림 1 (실제 커밋은 없음 `head_subject=init`).
- 작업 알림의 실제 입력 모양은 `claude -p` 세션에 입력을 받아 적는 훅을 `--settings` 로 붙여 받았다. `prompt` 값이 `<task-notification>` 으로 시작하고 `</task-notification>` 으로 끝나며, 알림 전용 칸은 없다 (키: `cwd` · `hook_event_name` · `permission_mode` · `prompt` · `prompt_id` · `scratchpad_dir` · `session_id` · `transcript_path`). 받은 원문은 `us-fixtures/task-notification.json`.

## 범위 경계

- 아래에서 `T` 는 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-us/.harness/.meta/after-kaizen-0926b` 다.
- 고칠 파일 넷: `~/.claude/hooks/next-session-handoff.sh` (US-1 · US-5) / `~/.claude/hooks/parallel-session-guard.sh` (US-2) / `~/.claude/hooks/enforce-codex-stdin.sh` (US-3) / `~/.claude/skills/handoff/SKILL.md` (US-4 · US-5). 공용 도우미 `~/.claude/hooks/_lib-hook-payload.sh` 는 사본만 두고 **고치지 않는다** — US-3 이 쓸 함수 `strip_heredoc_bodies` 가 이미 있고, 따옴표 제거(US-2)는 병렬 세션 훅 한 곳에서만 쓰므로 도우미를 바꿀 까닭이 없다. 도우미를 쓰는 훅 일곱(`block-dirwide-autofixer.sh` · `enforce-codex-stdin.sh` · `qa-pending-check.sh` · `check-plain-korean.sh` · `remind-plain-korean.sh` · `parallel-session-guard.sh` · `lint-contract-oracle.sh`)이 그대로 도는 것은 도우미 지문이 같다는 것으로 잰다(AR-01).
- 고치기 전 사본: `T/us-backup/` — 위 다섯 파일(핸드오프는 `handoff-SKILL.md`), `hooks.sha256`(훅 폴더 15 파일 지문), `settings.sha256`.
- 시험: `T/us-test.sh <훅 폴더> <SKILL.md>` 가 한 줄에 한 경우(`<경우> <잰 값>`)를 찍는다. 「고친 뒤 결과」 는 `bash T/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md 2>/dev/null` 의 표준출력, 「고치기 전 결과」 는 `T/us-result-before.txt` 다. 실제 세션 시험은 `T/us-e2e.sh <라벨> <notify|quoted>`, 고치기 전 출력은 `T/us-e2e-before.txt`. 픽스처 저장소는 scratchpad `us-fx` · `us-e2e-<라벨>` 에 만들고 매번 지운다.
- 작성 시점 sha256 앞 16 자: `us-test.sh` = `0eb9d22f5406c8f2`, `us-e2e.sh` = `4fb0f5fe11a58712`, `us-result-before.txt` = `217861efdbc082ab`, `us-e2e-before.txt` = `12d6e50095afec8a`, `us-fixtures/task-notification.json` = `3ba977806cbb4975`. 평가 때 값이 다르면 시험이 바뀐 것이다.
- US-1 해석: 알림 전용 칸이 없으므로 `prompt` 안의 `<task-notification>` ~ `</task-notification>` 구간을 판정에서 뺀다. 구간 밖 사용자 글은 그대로 판정한다(N2). 알림만 온 입력은 조용히 지나간다.
- US-2 해석: (가) 작은따옴표 · 큰따옴표 안 글자는 커밋 판별에서 명령 위치로 보지 않는다. 따옴표 밖에 진짜 `git commit` 이 있으면 그대로 잡는다(Q4 · Q5). `bash -c '<명령>'` 처럼 따옴표 안에서 실제로 도는 커밋은 고치기 전에도 못 잡았고 이번에도 잡지 않는다. (나) `GIT_INDEX_FILE=<값> <명령>` 앞말은 그 명령 하나에만 붙는다. 커밋 명령에 붙었거나 앞에서 `export` 했을 때만 개인 인덱스로 본다.
- US-3 해석: 인라인 awk 를 공용 함수 호출로 바꾼다. 판정(C01 ~ C12)은 한 글자도 바뀌지 않아야 한다.
- US-4: 공동 작성자 줄은 지금 세션 모델 `Claude Opus 5.5 (1M context)`. 근거는 이 세션(구현 세션 `bda55d45…`)의 시스템 첨부 안내가 커밋 끝에 붙이라고 준 줄 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이다. 교차 진단 세션이 본 `Claude Sonnet 5` 는 그 진단 세션 자신의 모델이라 기준이 아니다. 모델 이름을 틀에 박는 방식은 그대로 두므로 다음 모델 교체 때 이 줄을 다시 바꿔야 한다 — 틀을 「세션 안내의 첨부 줄을 쓴다」 로 바꾸는 일은 이번 범위 밖이고 「남은 것」 에 적는다.
- US-5 (PD-1): 핸드오프 틀 폐기 칸과 세션 마감 훅 복붙 블록의 폐기 줄은 결정을 옮겨 적지 않고 원문 자리 경로를 적게 한다. 원문 자리 순서 — 그 기능 PRD 의 비범위 표, 없으면 작업 계약 「범위 경계」, 둘 다 없으면 승인 기록. `planning-kit/skills/plan-prd/SKILL.md:28` (Gotcha 14 「핸드오프는 이 PRD 경로를 가리키고 결정을 다시 쓰지 않는다」) 와 `harness/skills/sprint-contract/SKILL.md:641` 와 같은 방향이다. 핸드오프 폐기 칸을 기계로 읽는 곳은 레포에 없다 (`grep -rn -e '폐기한 결정' -e '폐기·거절' .` 결과에 핸드오프 틀을 읽는 코드 0 개) — 소비면은 다음 세션의 사람 · 모델뿐이다.
- AR-01 전제: `~/.claude/hooks/` · `~/.claude/settings.json` 은 이 기계의 모든 세션이 같이 쓴다. 평가 때 대상 밖 파일 지문이 달라졌으면 그 파일의 변경 시각과 내용을 적고, 이 계약의 대상 넷과 무관한 다른 세션 변경인지부터 가른다.
- `project.yaml` 금지 패턴 4 종은 레포 릴리스 · 플러그인 파일 전용이라 이번 변경 파일(레포 밖 셸 · 문서)에 걸릴 것이 없다 → `AP-00: N/A`.
- 폐기한 결정: 없음 (이 묶음에서 사용자가 버린 항목 없음).
- 봉인 전 교차 진단(qa-evaluator) 반영: (1) `PATH=/bin` 이 grep 까지 숨기던 것을 jq 만 숨기는 폴더로 바꾸고 ER-01 에 표준오류 칸을 더했다 — 시험 도구 지문과 고치기 전 결과(61 줄)를 다시 떴다. (2) US-4 목표 문자열의 근거를 적었다. (3) `project.yaml` AP-04 정규식이 닫는 `---` 에도 걸리는 문제는 이 계약 범위 밖이라 「남은 것」 으로 넘긴다.
- 커버리지 해소: SC-01 ~ SC-07 · ER-01 · SK-02 — 경우 이름은 `us-test.sh` 출력 줄 이름과 같은 표기이고, 측정은 그 줄을 그대로 읽는다.
- 커버리지 해소: AR-01 — 대상 경로는 측정의 `cmp` · `shasum -c` · `find` 가 직접 연다 대상 셋 · 도우미 · 핸드오프 폴더 · 설정 파일 이름이 측정 줄에 명령 인자로 들어 있다 (검출기는 공백 든 명령 토큰을 대상으로 안 센다).
- 커버리지 해소: SC-05 — `shared.txt` · `mine.txt` 는 시험 준비물 이름이고, 측정은 `us-test.sh` 출력의 `shared=` · `mine=` 칸(해당 이름이 안내문에 있는지)으로 읽는다.
- 오라클 해소: SK-01 — 산출물이 틀 문서의 줄 자체라 그 줄의 문구 · 위치를 재는 것이 곧 결과다. 틀을 실제로 쓰는 동작(5 단계 커밋)은 SK-02 가 코드 블록을 뽑아 실행해 잰다.
- 오라클 해소: SK-03 — 바뀐 줄 수를 `diff` 로 재서, 문구만 어딘가에 넣고 다른 줄을 건드린 경우를 FAIL 로 잡는다. 마크다운 경고는 검사기를 실제로 돌린 출력이다.
- 오라클 해소: AR-02 — 산출물이 커밋 기록이라 `git log` 출력이 곧 결과다.

## 회귀 게이트

- 고치기 전 결과 `us-result-before.txt` 61 줄, 실제 세션 `us-e2e-before.txt` (세션 `3c6a15e1-92e4-43b7-adfb-874fe5bce143` · `4baedc61-bd39-4203-b01e-b91c67bdfc7e`).
- 음성 대조 실측 (봉인 전): 옛 codex 훅에서 heredoc 제거를 빼고 `cmd="$raw"` 로 바꾼 사본은 `C03 deny` · `C05 deny` · `C11 deny` · `C12 deny` 를 낸다 (고치기 전은 넷 다 `none`).
- 양성 대조 (훅 오류 0 기대 측정): DG-04 의 오류 첨부 jq 식을 `/Users/jackson/.claude/projects/-private-tmp-claude-501--Users-jackson-Hub-10-Dev-claude-plugins-e8a3c269-60ff-4f5a-8bb3-8703bb91d8cf-scratchpad-fail-probe-work/0379b5a8-f988-4cd7-a742-f03bb6b71309.jsonl` 에 `probe-fail-hook` 이름으로 돌리면 1.
- 마크다운 경고 기준: 옛 `handoff-SKILL.md` 를 markdownlint-cli2 0.23.2 · `{ "config": { "MD013": false } }` 로 재면 0 건. 양성 대조: 같은 파일을 `MD013: true` 로 재면 `MD013` 8 건.
- shellcheck 0.11.0 `-f gcc` 모든 등급: 사본 네 셸 파일 모두 0 줄.

## Skill
- [ ] SK-01: 핸드오프 틀의 `## 폐기·거절한 결정 (되살리기 전에 사용자에게 묻기)` 절 바로 다음 절은 여전히 `## Known Issues / Blockers` 이고, 두 제목 사이의 목록 줄이 정확히 1 개이며 그 줄에 `원문 자리` · `PRD 비범위 표` · `범위 경계` · `승인 기록` 이 이 순서로 있고 `없음` 이 있으며 `<이유>` · `<날짜>` 는 없다 [exact]
  - 측정: `n=$(grep -nx '## 폐기·거절한 결정 (되살리기 전에 사용자에게 묻기)' ~/.claude/skills/handoff/SKILL.md | cut -d: -f1)` 가 한 줄. `awk -v n=$n 'FNR>n && /^## /{print; exit}'` 가 `## Known Issues / Blockers`. 두 줄 사이 `^- ` 줄 수 1. 그 줄에 `grep -c '원문 자리.*PRD 비범위 표.*범위 경계.*승인 기록'` = 1 · `grep -c '없음'` = 1 · `grep -cE '<이유>|<날짜>'` = 0
  - 음성 대조: 고치기 전 사본은 그 줄이 `- <항목> · <날짜> · <이유> (없으면 "없음")` 라 순서 검사 0 · `<이유>` 1
- [ ] SK-02: Given 남의 파일 `other.txt` 가 올려진 저장소. When 핸드오프 5 단계 코드 블록을 그대로 실행한다. Then 새 커밋이 정확히 1 개, 제목에 `시험`, 파일은 핸드오프 파일 1 개, `other.txt` 는 커밋에 없고 여전히 올려져 있으며, 커밋 본문에 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 줄이 정확히 있고 `Opus 4` 는 없다 [exact]
  - 측정: 고친 뒤 결과 `SK5 new_commits=1 subject=1 files=1 other_in_commit=0 other_still_staged=1 coauthor_now=1 coauthor_old=0`
  - 음성 대조: 고치기 전 결과 `coauthor_now=0 coauthor_old=1`
- [ ] SK-03: 핸드오프 스킬 파일은 두 줄만 바뀐다 — 폐기 칸 목록 줄과 공동 작성자 줄. 마크다운 경고는 0 건이다 [exact]
  - 측정: `diff T/us-backup/handoff-SKILL.md ~/.claude/skills/handoff/SKILL.md | grep -cE '^<'` = 2 · `grep -cE '^>'` = 2, `^<` 두 줄의 `< ` 뒤가 `- <항목> · <날짜> · <이유> (없으면 "없음")` 와 `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"` 이다. scratchpad `mdlint/node_modules/.bin/markdownlint-cli2 --config mdlint/cfg.markdownlint-cli2.jsonc` 로 그 파일 사본을 재어 `Summary: 0 issues`

## Script
- [ ] SC-01: Given 세션 마감 훅. When 받은 작업 알림 원문만 넣으면(`N1`) 또는 알림 뒤에 사용자 글 「안녕」 을 붙이면(`N3`) Then 출력이 없다. When 알림 뒤에 「다음 세션에 이어가자」 를 붙이면(`N2`) · 「오늘 여기까지」 만 넣으면(`H1`) Then 세션 마감 안내가 나온다. 「안녕」 만이면(`H2`) 출력이 없다 [exact, enumerated]
  - 측정: 고친 뒤 결과 `N1 noti_has_kw=1 empty=1` · `N2 detect=1` · `N3 empty=1` · `H1 json=1 detect=1 …` · `H2 empty=1`
  - 음성 대조: 고치기 전 결과 `N1 … empty=0` · `N3 empty=0`
- [ ] SC-02: 세션 마감 안내의 복붙 블록에 `폐기한 결정:` 으로 시작하는 줄이 정확히 1 개이고, 그 줄에 `PRD 비범위 표` · `범위 경계` · `승인 기록` 이 이 순서로 있고 `없으면 없음` 이 있으며 `이유` 는 없다 [exact]
  - 측정: 고친 뒤 결과 `H1 json=1 detect=1 pline_count=1 pline_prd=1 pline_scope=1 pline_approval=1 pline_order=1 pline_none=1 pline_reason=0`
  - 음성 대조: 고치기 전 결과 `pline_prd=0 pline_scope=0 pline_approval=0 pline_order=0`
- [ ] SC-03: 따옴표 안 「git commit」 — `Q1-pre`(작은따옴표 안 `;`) · `Q2-pre`(큰따옴표 안 줄바꿈 뒤 줄머리) · `Q3-pre`(큰따옴표 안 `&&`)는 커밋 전 출력이 없고, `Q1-post` · `Q2-post` 는 커밋 뒤 알림이 없다 [exact, enumerated]
  - 측정: 고친 뒤 결과 `Q1-pre empty=1` · `Q2-pre empty=1` · `Q3-pre empty=1` · `Q1-post landed=0` · `Q2-post landed=0`
  - 음성 대조: 고치기 전 결과 셋 다 `empty=0 shared=1`, 둘 다 `landed=1`
- [ ] SC-04: 따옴표 밖 진짜 커밋은 그대로 잡는다 — `Q4-pre`(메시지 안에 `; git commit` 이 든 커밋) · `Q5-pre`(따옴표 인자 뒤 `&& git commit`)는 경고에 `shared.txt` 가 있고, `Q4-post` 는 커밋 뒤 알림이 있다 [exact, enumerated]
  - 측정: 고친 뒤 결과 `Q4-pre empty=0 shared=1` · `Q5-pre empty=0 shared=1` · `Q4-post landed=1`
  - 음성 대조: 따옴표 안뿐 아니라 모든 명령을 커밋 아님으로 보는 사본이면 `empty=1` · `landed=0` 이 되어 FAIL 한다
- [ ] SC-05: `GIT_INDEX_FILE=` 이 붙은 자리 — `I1-pre`(`git add` 에만 붙음)는 공용 인덱스 경고라 `shared.txt` 가 있고 `mine.txt` · `개인 인덱스` 는 없다. `I2-pre`(커밋에도 붙음) · `I3-pre`(`export`)는 `mine.txt` 와 `개인 인덱스` 가 있고 `shared.txt` 는 없다 [exact, enumerated]
  - 측정: 고친 뒤 결과 `I1-pre empty=0 shared=1 mine=0 private=0` · `I2-pre empty=0 shared=0 mine=1 private=1` · `I3-pre empty=0 shared=0 mine=1 private=1`
  - 음성 대조: 고치기 전 결과 `I1-pre empty=0 shared=0 mine=1 private=1`
- [ ] SC-06: 병렬 세션 훅의 기존 판정은 그대로다 — `SC02a` ~ `SC02d` · `SC03a` ~ `SC03f` · `SC05a` ~ `SC05d` · `ER02` · `SC04a` ~ `SC04c` 줄이 고치기 전 결과와 글자까지 같다 [exact, enumerated]
  - 측정: `diff <(grep -E '^(SC0[2-5][a-f]|ER02) ' T/us-result-before.txt) <(고친 뒤 결과 | grep -E '^(SC0[2-5][a-f]|ER02) ')` 빈 출력, 그리고 그 줄 수 = 18 (고치기 전 결과에서 실측)
- [ ] SC-07: codex stdin 훅은 heredoc 본문 제거를 공용 함수로 하고 판정은 그대로다 — 훅 파일에 인라인 awk 상태 변수(`inhd`)가 없고 `strip_heredoc_bodies` 로 넘기는 줄이 있으며, `C01` ~ `C12` 판정이 고치기 전과 같다 [exact, enumerated]
  - 측정: `grep -c 'inhd' ~/.claude/hooks/enforce-codex-stdin.sh` = 0, `grep -cE '\|[[:space:]]*strip_heredoc_bodies' ~/.claude/hooks/enforce-codex-stdin.sh` >= 1, `grep -c 'strip_heredoc_bodies()' ~/.claude/hooks/enforce-codex-stdin.sh` = 0, `diff <(grep -E '^C[0-9]{2} ' T/us-result-before.txt) <(고친 뒤 결과 | grep -E '^C[0-9]{2} ')` 빈 출력이고 그 줄 수 = 12
  - 음성 대조: heredoc 제거를 빼고 원문을 그대로 쓰는 사본은 `C03` · `C05` · `C11` · `C12` 가 `deny` 가 된다 (봉인 전 실측, 회귀 게이트)

## Error
- [ ] ER-01: 조용히 지나가야 하는 13 경우 — `ER01-pre-empty` · `ER01-pre-broken` · `ER01-pre-nojq` · `ER01-post-empty` · `ER01-post-broken` · `ER01-post-nojq` · `ER01-handoff-empty` · `ER01-handoff-broken` · `ER01-handoff-nojq` · `CX-empty` · `CX-broken` · `CX-nojq` · `CX-nolib` (빈 입력 · 깨진 JSON `{` · jq 만 숨긴 PATH · 없는 도우미 경로) 모두 종료 코드 0 · 표준출력 없음 · 표준오류 없음 [exact, enumerated]
  - 측정: 고친 뒤 결과에서 `grep -cE '^(ER01-|CX-)'` = 13 이고 `grep -E '^(ER01-|CX-)' | grep -vc 'rc=0 empty=1 stderr_empty=1$'` = 0, 그리고 준비 줄 `NOJQ-env jq=0 grep=1` 이 있다. 준비: 이 맥은 `/bin/jq` · `/bin/grep` 둘 다 없고 `/usr/bin` 에만 있어 `PATH=/bin` 은 grep 까지 숨긴다. 그래서 `us-test.sh` 가 scratchpad `us-fx/nojq-bin` 에 `/usr/bin` 의 jq 를 뺀 도구마다 exec 감싸개(새 일반 파일, 바로가기 아님)를 만들고 `PATH=<그 폴더>:/bin` 으로 돌린다. 고치기 전 결과도 13 줄 모두 `rc=0 empty=1 stderr_empty=1`
  - 음성 대조: 고치기 전 세션 마감 훅을 `PATH=/bin` 으로 돌리면 종료 코드 0 인데 표준오류에 `grep: command not found` 가 샌다(봉인 전 실측) — 표준출력만 보는 옛 측정은 이것을 못 잡았고 `stderr_empty` 칸이 잡는다

## Architecture
- [ ] AR-01: 범위 밖은 그대로 — 공용 도우미 `~/.claude/hooks/_lib-hook-payload.sh` 가 사본과 바이트까지 같고, 훅 폴더 파일은 15 개 그대로이며 대상 셋(`next-session-handoff.sh` · `parallel-session-guard.sh` · `enforce-codex-stdin.sh`)을 뺀 12 개 지문이 사본 지문과 같고, `~/.claude/skills/handoff/` 에는 파일이 1 개, `~/.claude/settings.json` 지문이 사본과 같으며, 대상 셋과 도우미가 `bash -n` 을 통과한다 [exact, enumerated]
  - 측정: `cmp ~/.claude/hooks/_lib-hook-payload.sh T/us-backup/_lib-hook-payload.sh` 종료 코드 0. `grep -vE ' \./(next-session-handoff|parallel-session-guard|enforce-codex-stdin)\.sh$' T/us-backup/hooks.sha256 | (cd ~/.claude/hooks && shasum -a 256 -c -) | grep -c ': OK$'` = 12. `find ~/.claude/hooks -maxdepth 1 -type f | wc -l` = 15. `find ~/.claude/skills/handoff -type f | wc -l` = 1. `shasum -a 256 ~/.claude/settings.json | cut -d' ' -f1` 이 `T/us-backup/settings.sha256` 과 같다. 네 파일 각각 `bash -n` 종료 코드 0
- [ ] AR-02: Given 이 계약의 봉인 커밋과 결과 커밋이 모두 끝난 뒤, 가지 `chore/ak2-us` 의 구간 `6378948..chore/ak2-us` 커밋이 건드린 경로는 전부 `.harness/` 아래다 (하한은 워크트리를 만든 origin/main 고정값, 상한은 가지 끝, 경로 한정 없이 전부 보고 `.harness/` 밖이 0 개인지 잰다, 생성물 없음) [exact]
  - 측정: `git -C /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-us log --format= --name-only 6378948..chore/ak2-us | grep -v '^$' | grep -vc '^\.harness/'` = 0
- [ ] AR-03: 고치기 전 사본은 한 번만 커밋되고 그 뒤 바뀌지 않는다 — `T/us-backup/` 아래 파일을 건드린 커밋이 정확히 1 개다 [exact]
  - 측정: `git -C /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-us log --format=%H 6378948..chore/ak2-us -- .harness/.meta/after-kaizen-0926b/us-backup | grep -c .` = 1

## Anti-patterns
- [ ] AP-00: N/A (대상이 `~/.claude` 셸 훅 · 스킬 문서 — `project.yaml` 금지 패턴 4 종은 레포 릴리스 · 플러그인 파일 전용이라 이번 변경 파일에 걸릴 수 없다)

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
  - 측정: heredoc 본문 제거 함수는 훅 파일이 아니라 공용 도우미에 있다 — `bash -c '. ~/.claude/hooks/_lib-hook-payload.sh; declare -F strip_heredoc_bodies'` 종료 코드 0, 대상 훅 셋 각각 `grep -c 'strip_heredoc_bodies()'` = 0
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  - 측정: codex stdin 훅이 heredoc 제거를 새로 짜지 않고 공용 함수를 부른다 — SC-07 의 `inhd` 0 · 호출 줄 1 이상

## Diagnostics
- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 레포 파일만 잰다 — 이번 변경 파일 넷은 전부 `~/.claude` 아래라 교집합 0 개. 실제 문법 검사는 AR-01 의 `bash -n`)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 없음 — `diagnostics.ide_exclude: []`)
  - 측정: shellcheck 0.11.0 `-f gcc` 모든 등급으로 `next-session-handoff.sh` · `parallel-session-guard.sh` · `enforce-codex-stdin.sh` · `_lib-hook-payload.sh` 각각 0 줄 (고치기 전 모두 0 줄). 스킬 문서 마크다운 경고는 SK-03
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 는 레포 릴리스 스크립트다 — 이번 변경 파일과 교집합 0 개)
- [ ] DG-04: 실제 Claude Code 실행 — (a) `bash T/us-e2e.sh post-notify notify` 출력이 `prompt_kw=0 noti_kw=1 handoff_ctx=0` 이고 (b) `bash T/us-e2e.sh post-quoted quoted` 출력이 `pre_ctx=0 post_ctx=0 head_subject=init` 이며 (c) 두 실행 모두 `hook_errors=0` 이다 [exact, enumerated]
  - 측정: `us-e2e.sh` 출력 두 벌
  - 음성 대조: 고치기 전 `us-e2e-before.txt` 는 `handoff_ctx=1` · `pre_ctx=1 post_ctx=1`. 양성 대조: (c) 의 jq 식을 회귀 게이트의 대조 기록에 `probe-fail-hook` 이름으로 돌리면 1
