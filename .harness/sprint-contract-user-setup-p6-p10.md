---
feature: "사용자 설정 P6~P10 — 핸드오프 폐기 결정 절 · 병렬 세션 훅 구멍 둘과 삭제 수 · 플러터 규칙 반 문장 · 전역 규칙 두 줄 · fit-pal 기억 둘"
slug: user-setup-p6-p10
created: "2026-09-26 11:23"
complexity: "복잡"
conditions: 22
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:af6ae6ab308af2bf
locked_at: "2026-09-26 11:37"
---

## 배경

- 출처: 핸드오프 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-0110.md` §B 표(P6~P10), 원래 배정은 `.claude/kaizen-input/insights-report.md` 의 `user-setup:P6`~`P10` 행. 전부 레포 밖(`~/.claude/`) 파일이라 이 레포 PR 에 코드 변경은 없다. 계약 · 결과 파일만 이 가지(`chore/after-kaizen-0926`)에 커밋한다.
- 동의 근거: P9 · P10 에 붙어 있던 「사용자 확인 필요」 는 user `2026-09-26T01:04:21.505Z` 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」 로 받은 것으로 본다 (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`).
- 복잡도 4 축: 레이어 — 훅 코드 · 공용 도우미 · 규칙 문서 · 기억 파일 (여럿) / 공개 계약 변경 — 예 (공용 도우미에 함수가 옮겨 오고, 핸드오프 틀과 훅 안내 형식이 바뀐다) / 소비면 — 예 (`block-dirwide-autofixer.sh` 가 옮긴 함수를 쓰고, 다음 세션이 핸드오프 틀을 읽는다) / 회귀 위험 — 예 (커밋 판별식이 바뀌면 오탐 · 누락이 생긴다). 넷 다 예라 「복잡」.
- 고치기 전 실측(`b-result-before.txt`): 변수 앞말 두 형태를 못 잡고(SC02b · SC02c 빈 출력), heredoc 본문 속 글자에 반응하고(SC02d 경고), 커밋 뒤 알림에 지운 수가 없고(SC04a `del2=0`), 핸드오프 5 단계가 남이 올려둔 파일을 싣는다(SK02 `files=2`). 실제 세션(`b-e2e.sh pre0`, 세션 `47eb1faf-f954-46f3-a091-91f7c06e8761`)에서도 공용 인덱스의 `shared.txt` 가 커밋에 실렸다. 이 세션 도중에도 heredoc 본문 속 `git commit` 글자에 커밋 뒤 알림이 떠서 다른 세션의 커밋 `8b63360` 을 보여줬다.

## 범위 경계

- 대상 파일 9 개: `~/.claude/skills/handoff/SKILL.md` · `~/.claude/hooks/next-session-handoff.sh` (P6) / `~/.claude/hooks/parallel-session-guard.sh` · `~/.claude/hooks/block-dirwide-autofixer.sh` · `~/.claude/hooks/_lib-hook-payload.sh` (P7) / `~/.claude/rules/flutter-playwright-verification.md` (P8) / `~/.claude/CLAUDE.md` (P9) / `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_timezone_country_ui.md` · 같은 폴더 `MEMORY.md` (P10). 고치기 전 사본은 scratchpad `b-before/` (위 9 개 · `settings.json` · `hooks.sha256` 15 줄).
- scratchpad 는 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad` 다. 시험은 그 안의 `b-test.sh <훅 폴더> <SKILL.md>`(한 줄에 한 경우, `<경우> <잰 값>`)와 `b-e2e.sh <라벨> <commit|handoff> [명령]`(실제 `claude -p` 세션). 봉인 시점 sha256 앞 16 자: `b-test.sh` = `ae7a6a71d22a0daa`, `b-e2e.sh` = `3e065eda0e41caa3`. 평가 때 값이 다르면 시험이 바뀐 것이다.
- 「고친 뒤 결과」 는 `bash b-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md 2>/dev/null` 의 표준출력이다. 조건의 `경우=값` 은 그 출력에서 해당 줄의 낱말을 뜻한다.
- P7 개인 인덱스 해석: 명령 안 어디든(앞말 · `env` 뒤 · `export`) `GIT_INDEX_FILE=<값>` 이 보이면 마지막 것을 쓴다. 값의 따옴표를 벗겨 `$` 나 역따옴표가 남으면 풀 수 없는 값이다. 상대 경로는 커밋이 돌 폴더 기준이다. 풀 수 없거나 파일이 없으면 공용 인덱스로 떨어지지 않고 조용히 지나간다 — 개인 인덱스를 쓰는 커밋에 공용 인덱스 목록을 보여주는 것은 틀린 경고이고, 커밋 뒤 알림이 실제로 들어간 것을 보여준다.
- 세 번째 사본: `~/.claude/hooks/enforce-codex-stdin.sh` 에도 같은 heredoc 제거 awk 가 인라인으로 있다. 핸드오프 지시 범위(자동 수정 훅의 함수를 공용으로 옮겨 병렬 세션 훅과 같이 쓰기) 밖이라 이번에 건드리지 않는다. 다음에 합칠 후보로 결과 파일에 적는다.
- AR-06 전제: `~/.claude/hooks/` 는 이 기계의 모든 세션이 같이 쓰는 폴더다. 평가 때 대상 밖 파일의 지문이 달라졌으면 그 파일의 변경 시각과 내용을 리포트에 적고, 이 계약의 대상 파일 넷과 무관한 다른 세션 변경인지부터 가른다.
- 킷 훅과 겹침: 킷 `harness/scripts/commit-guard.sh post` 는 삭제 51 개 이상에서만 알린다. 이 사용자 훅의 커밋 뒤 알림은 고치기 전부터 모든 커밋에 떴으므로, 51 개 이상 삭제 커밋에서 알림 둘은 이번 변경이 새로 만든 겹침이 아니다. 관찰 줄 `OBS-dup` 으로 재고 결과 파일에 적는다 (조건 아님).
- `project.yaml` 금지 패턴 4 종은 레포 릴리스 · 플러그인 파일 전용이라 이번 변경 파일(레포 밖 셸 · 문서)에 걸릴 것이 없다 → `AP-00: N/A`.
- 커버리지 해소: SC-02 · SC-03 · SC-05 · ER-01 · ER-02 · SK-02 · AR-02 — 경우 이름은 `b-test.sh` 출력 줄 이름과 같은 표기이고, 측정은 그 줄을 그대로 읽는다.
- 커버리지 해소: AR-06 — 대상 경로는 측정의 `shasum` 비교와 `git log`/`git show` 가 직접 연다.
- 커버리지 해소: SC-02 · SC-05 · DG-04 — `shared.txt` · `mine.txt` · `../private.idx` 는 시험 준비물 이름이고, 측정은 `b-test.sh` · `b-e2e.sh` 출력의 `shared=` · `mine=` 칸(해당 파일 이름이 안내문에 있는지)으로 읽는다. DG-04 는 `b-e2e.sh` 가 안내문 첫 160 자를 찍으므로 두 이름을 눈으로도 본다.
- 커버리지 해소: AR-01 — 측정의 「두 훅 각각」 은 `block-dirwide-autofixer.sh` · `parallel-session-guard.sh`, 「네 파일 각각」 은 조건 산문에 열거한 네 파일이며 모두 `~/.claude/hooks/` 아래다.
- 커버리지 해소: AR-05 — 측정의 `grep -c` · `wc -l` 대상은 위 대상 파일 목록의 fit-pal 두 파일(절대 경로)이다.
- 오라클 해소: SK-01 — 산출물이 틀 문서의 절 자체라 그 절의 위치 · 문구를 재는 것이 곧 결과다. 틀을 실제로 쓰는 동작(5 단계 커밋)은 SK-02 가 코드 블록을 추출해 실행해 잰다.
- 오라클 해소: AR-03 · AR-04 — 산출물이 규칙 문장 자체다(실행할 코드가 없다). 대신 `diff` 로 바뀐 줄 수까지 재서, 문구만 어딘가에 넣고 다른 줄을 건드린 경우를 FAIL 로 잡는다.

## 회귀 게이트

- 고치기 전 결과: scratchpad `b-result-before.txt` 37 줄 (`bash b-test.sh b-before b-before/handoff-SKILL.md 2>/dev/null`).
- 대조 기록: 옛 훅으로 돌린 실제 세션 `47eb1faf-f954-46f3-a091-91f7c06e8761` — `PreToolUse:Bash` 안내에 `shared.txt`, 커밋에 `shared.txt`. 훅 오류 양성 대조: `/Users/jackson/.claude/projects/-private-tmp-claude-501--Users-jackson-Hub-10-Dev-claude-plugins-e8a3c269-60ff-4f5a-8bb3-8703bb91d8cf-scratchpad-fail-probe-work/0379b5a8-f988-4cd7-a742-f03bb6b71309.jsonl` 에 DG-04 명령을 `probe-fail-hook` 이름으로 돌리면 1.
- 기준 줄 수: `~/.claude/CLAUDE.md` 266 · `flutter-playwright-verification.md` 70 · fit-pal `MEMORY.md` 280. 공용 도우미 함수 5 개(`bash -c '. ~/.claude/hooks/_lib-hook-payload.sh; declare -F' | wc -l`).

## Skill
- [ ] SK-01: 핸드오프 틀의 `## Known Issues / Blockers` 바로 앞 절이 `## 폐기·거절한 결정 (되살리기 전에 사용자에게 묻기)` 이고, 그 절 본문에 표가 아닌 한 줄 형식 안내가 있어 `항목` · `날짜` · `이유` 세 낱말을 모두 담는다 [exact] (측정: `n=$(grep -nx '## 폐기·거절한 결정 (되살리기 전에 사용자에게 묻기)' ~/.claude/skills/handoff/SKILL.md | cut -d: -f1)` 가 한 줄; `awk -v n=$n 'FNR>n && /^## /{print; exit}'` 가 `## Known Issues / Blockers`; 두 줄 사이에서 `항목` · `날짜` · `이유` 를 모두 담고 `|` 로 시작하지 않는 줄 1 개 이상)
- [ ] SK-02: Given 남의 파일 `other.txt` 가 올려진 저장소. When 핸드오프 5 단계 코드 블록을 그대로 실행한다. Then 새 커밋이 정확히 1 개 생기고 그 제목에 치환된 요약(`시험`)이 있으며, 그 커밋에 파일이 정확히 1 개(핸드오프 파일)이고 `other.txt` 는 커밋에 없고 여전히 올려진 상태다 [exact] (측정: 고친 뒤 결과 `SK02 new_commits=1 subject=1 files=1 other_in_commit=0 other_still_staged=1`. 음성 대조: 고치기 전 결과는 `files=2 other_in_commit=1 other_still_staged=0`; 5 단계 제목을 지워 코드 블록을 못 뽑은 사본(`### 5. 커밋` → `### 커밋`)은 `new_commits=0 subject=0` — 봉인 전 실측)

## Script
- [ ] SC-01: 세션 마감 문장 「오늘 여기까지」 를 넣으면 훅 출력이 올바른 JSON 이고 안내문에 `폐기` 가 정확히 한 줄, 그 줄이 `폐기한 결정: <없으면 없음>` 이다. 마감 문장이 아니면 출력이 없다 [exact] (측정: 고친 뒤 결과 `SC01a json=1 pye=1 line=1` · `SC01b empty=1`. 음성 대조: 고치기 전 `SC01a json=1 pye=0 line=0`)
- [ ] SC-02: 네 형태 — `SC02a`(접두 없음)는 경고에 `shared.txt`, `SC02b`(`GIT_INDEX_FILE=` 앞말) · `SC02c`(`env GIT_INDEX_FILE=`)는 경고에 `mine.txt` 가 있고 `shared.txt` 는 없으며, `SC02d`(heredoc 본문 속 `git commit`)는 출력이 없다 [exact, enumerated] (측정: 고친 뒤 결과 `SC02a empty=0 shared=1` · `SC02b empty=0 shared=0 mine=1` · `SC02c empty=0 shared=0 mine=1` · `SC02d empty=1`. 음성 대조: 고치기 전 `SC02b empty=1` · `SC02c empty=1` · `SC02d empty=0`)
- [ ] SC-03: 기존 동작 유지 — `SC03a`(`git -C <저장소>`) · `SC03b`(`cd <저장소> &&`) · `SC03f`(`git commit -F - <<'EOF'`)는 경고에 `shared.txt`, `SC03c`(`-o` 경로 한정) · `SC03d`(워크트리 1 개) · `SC03e`(`git status`)는 출력 없음 [exact, enumerated] (측정: 고친 뒤 결과 여섯 줄이 고치기 전 결과의 같은 이름 줄과 글자까지 같다 — `diff <(grep '^SC03' 전) <(grep '^SC03' 후)` 빈 출력)
- [ ] SC-04: 커밋 뒤 알림 — 두 파일을 지운 커밋이면 `지운 파일 2 개` 가 있고(`SC04a`), 지운 파일이 없는 커밋이면 `지운 파일` 낱말이 없고 기존 「방금 커밋에 실제로 들어간 것」 은 그대로 있으며(`SC04b`), `GIT_INDEX_FILE=` 앞말이 붙은 커밋에도 알림이 뜬다(`SC04c`) [exact, enumerated] (측정: 고친 뒤 결과 `SC04a landed=1 del2=1` · `SC04b landed=1 delword=0` · `SC04c landed=1`. 음성 대조: 고치기 전 `SC04a del2=0` · `SC04c landed=0`)
- [ ] SC-05: 개인 인덱스 해석 — `SC05a`(값이 `"$T"`) · `SC05b`(없는 파일)는 출력 없음, `SC05c`(`export GIT_INDEX_FILE=<파일>; git commit`) · `SC05d`(상대 경로 `../private.idx`)는 경고에 `mine.txt` 가 있고 `shared.txt` 는 없다 [exact, enumerated] (측정: 고친 뒤 결과 `SC05a empty=1` · `SC05b empty=1` · `SC05c empty=0 shared=0 mine=1` · `SC05d empty=0 shared=0 mine=1`. 음성 대조: 고치기 전 `SC05c shared=1 mine=0` · `SC05d empty=1`)

## Error
- [ ] ER-01: 조용히 지나가야 하는 9 경우 — `ER01-pre-empty` · `ER01-pre-broken` · `ER01-pre-nojq` · `ER01-post-empty` · `ER01-post-broken` · `ER01-post-nojq` · `ER01-handoff-empty` · `ER01-handoff-broken` · `ER01-handoff-nojq` (빈 입력 · 깨진 JSON `{` · `env PATH=/bin` 으로 jq 를 숨김) 모두 종료 코드 0, 표준출력 없음 [exact, enumerated] (측정: 고친 뒤 결과에서 `^ER01-` 줄이 9 개이고 전부 `rc=0 empty=1` — `grep '^ER01-' 후 | grep -vc 'rc=0 empty=1$'` = 0 이고 `grep -c '^ER01-'` = 9. 준비 실측: `/bin/jq` 없음, `/usr/bin/jq` 있음 → `PATH=/bin` 이면 jq 가 숨는다)
- [ ] ER-02: 공용 도우미를 읽지 못해도(`CLAUDE_HOOK_LIB` 가 없는 파일) 병렬 세션 훅의 커밋 전 검사는 계속 돌아 `SC02a` 와 같은 경고를 낸다 — 도우미가 깨지면 훅이 조용히 꺼지는 경로가 없다 [exact] (측정: 고친 뒤 결과 `ER02 empty=0 shared=1`)

## Architecture
- [ ] AR-01: heredoc 본문 제거 함수 `strip_heredoc_bodies` 가 공용 도우미 `~/.claude/hooks/_lib-hook-payload.sh` 에 정의돼 있고, `block-dirwide-autofixer.sh` · `parallel-session-guard.sh` 에는 정의가 없고 부르는 줄만 있다. 도우미의 기존 함수 5 개는 바뀌지 않고, 네 셸 파일(`_lib-hook-payload.sh` · `block-dirwide-autofixer.sh` · `parallel-session-guard.sh` · `next-session-handoff.sh`)은 문법 검사를 통과한다 [exact, enumerated] (측정: `grep -c '^strip_heredoc_bodies()' ~/.claude/hooks/_lib-hook-payload.sh` = 1; 두 훅 각각 `grep -c 'strip_heredoc_bodies()'` = 0 · `grep -c 'strip_heredoc_bodies'` >= 1; `bash -c '. ~/.claude/hooks/_lib-hook-payload.sh; declare -F' | wc -l` = 6; `diff b-before/_lib-hook-payload.sh ~/.claude/hooks/_lib-hook-payload.sh | grep -c '^<'` = 0; 네 파일 각각 `bash -n` 종료 코드 0)
- [ ] AR-02: 자동 수정 훅은 함수를 옮긴 뒤에도 같은 판정을 낸다 — `AF-a` · `AF-b` · `AF-c` · `AF-d` · `AF-e` · `AF-f` 여섯 경우의 결과가 고치기 전과 같다 [exact, enumerated] (측정: `diff <(grep '^AF-' 전) <(grep '^AF-' 후)` 빈 출력. 고치기 전 값: `deny none none deny deny deny`)
- [ ] AR-03: 플러터 규칙 — 「relaunch 하지 마라」 줄 끝에 반 문장이 붙고 새 줄은 없다 [exact] (측정: `grep -c '반영이 안 된' ~/.claude/rules/flutter-playwright-verification.md` = 1; `wc -l` = 70; `diff b-before/flutter-playwright-verification.md ~/.claude/rules/flutter-playwright-verification.md` 의 `^<` 1 줄 · `^>` 1 줄이고 `^>` 줄에 `relaunch 하지 마라` 와 `restart_app 을 되풀이하지 말고` 가 있다)
- [ ] AR-04: 전역 규칙 두 줄 — `~/.claude/CLAUDE.md` 가 새 줄 없이 두 줄만 바뀐다. (1) 「올바른 파일/컴포넌트를 먼저 식별」 줄에 `무엇이 막는지와 우회 방법` 이 붙고 (2) 「건너뛰기 금지」 줄에서 `작은 변경이니까` 문장이 빠지고 `예외 목록에 든 수정` 문장이 들어간다 [exact, enumerated] (측정: `wc -l` = 266; `diff b-before/CLAUDE.md ~/.claude/CLAUDE.md | grep -c '^>'` = 2 · `grep -c '^<'` = 2; `grep -c '무엇이 막는지와 우회 방법'` = 1 이고 그 줄에 `올바른 파일/컴포넌트를 먼저 식별` 이 있다; `grep -c '예외 목록에 든 수정'` = 1 이고 그 줄에 `건너뛰기 금지` 가 있다; `grep -c '작은 변경이니까'` = 0)
- [ ] AR-05: fit-pal 기억 — (1) `feedback_no_timezone_country_ui.md` 에 `한국·한국어 우선으로 추론하지 마라` 가 1 번 있고 (2) `MEMORY.md` 는 280 줄에서 275 줄이 되며, 여섯 이름 `feedback_shared_index_use_private_index_file` · `feedback_private_index_leaves_shared_index_stale` · `feedback_shared_index_snapshot_reverts_commits` · `feedback_shared_index_steals_staged_files` · `feedback_shared_worktree_stage_hunks` · `feedback_shared_index_reset_paths_only` 가 각각 정확히 한 번, 모두 같은 한 줄에 있고 그 줄에 `feedback_own_worktree_not_shared_dev` 와 `지키면 필요 없음` 이 있다. 여섯 파일은 그대로 있다 [exact, enumerated] (측정: `grep -c` 1; `wc -l` = 275; 이름마다 `grep -c` = 1 이고 여섯의 `grep -n` 줄 번호가 하나; 그 줄에서 두 낱말 `grep -c` 각 1; `diff b-before/MEMORY.md 후 | grep -c '^<'` = 6 · `'^>'` = 1; 여섯 파일 각각 `test -f`)
- [ ] AR-06: 범위 밖은 그대로 — `~/.claude/settings.json` sha256 이 `b-before/settings.json` 과 같고, `~/.claude/hooks/` 파일은 15 개 그대로이며 그중 `_lib-hook-payload.sh` · `block-dirwide-autofixer.sh` · `parallel-session-guard.sh` · `next-session-handoff.sh` 를 뺀 11 개의 sha256 이 `b-before/hooks.sha256` 과 같다. Given 이 계약의 봉인 커밋과 결과 커밋이 끝난 뒤, 제목에 `user-setup-p6-p10` 이 든 이 가지의 커밋이 건드린 경로는 전부 `.harness/` 아래다 (구간 `f81568d..chore/after-kaizen-0926` — 하한은 작성 시점 origin/main 고정값, 상한은 가지 끝, 경로 한정 없이 전부 보고 `.harness/` 밖이 0 개인지 잰다, 생성물 없음) [exact, enumerated] (측정: `shasum -a 256` 비교; `find ~/.claude/hooks -maxdepth 1 -type f | wc -l` = 15; `git log --format=%H --grep=user-setup-p6-p10 f81568d..chore/after-kaizen-0926` 의 커밋마다 `git show --name-only --format=` 을 모아 `grep -vc '^\.harness/'` = 0)

## Anti-patterns
- [ ] AP-00: N/A (대상이 `~/.claude` 셸 훅 · 규칙 문서 · 기억 파일 — `project.yaml` 금지 패턴 4 종은 레포 릴리스 · 플러그인 파일 전용이라 이번 변경 파일에 걸릴 수 없다)

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: heredoc 제거 함수가 훅 파일이 아니라 공용 도우미에 있다 — AR-01 의 `declare -F` 6)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 병렬 세션 훅이 heredoc 제거를 새로 짜지 않고 공용 함수를 부른다 — `grep -c 'strip_heredoc_bodies()' ~/.claude/hooks/parallel-session-guard.sh` = 0 이고 `grep -c 'strip_heredoc_bodies' …` >= 1)

## Diagnostics
- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 레포 파일만 잰다 — 이번 변경 파일 9 개는 전부 `~/.claude` 아래라 교집합 0 개. 실제 문법 검사는 AR-01 의 `bash -n` 네 파일)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 없음 — `diagnostics.ide_exclude: []`. 측정: `shellcheck -f gcc` 모든 등급으로 네 셸 파일 각각 0 줄. 고치기 전 네 파일 모두 0 줄)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 는 레포 릴리스 스크립트다 — 이번 변경 파일과 교집합 0 개)
- [ ] DG-04: 실제 Claude Code 실행 — (a) `b-e2e.sh post1 commit 'GIT_INDEX_FILE=@IDX@ git commit -m e2e1'` 의 세션 기록에 `PreToolUse:Bash` 의 `hook_additional_context` 중 `mine.txt` 가 있고 `shared.txt` 가 없는 것 1 건 이상, `PostToolUse:Bash` 의 `hook_additional_context` 중 `방금 커밋에 실제로 들어간 것` 이 든 것 1 건 이상, 저장소 마지막 커밋의 파일이 `mine.txt` 하나 (b) `b-e2e.sh post2 handoff` 의 세션 기록에 `UserPromptSubmit` 의 `hook_additional_context` 중 `폐기한 결정` 이 든 것 1 건 이상 (c) 두 기록 모두 네 훅 이름이 든 `hook_non_blocking_error` · `hook_blocking_error` · `hook_cancelled` 첨부 0 건 [exact, enumerated] (측정: `b-e2e.sh` 출력. 양성 대조: (c) 의 같은 jq 식을 회귀 게이트의 대조 기록에 `probe-fail-hook` 이름으로 돌리면 1)
