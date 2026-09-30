---
feature: "병렬 세션 훅이 못 잡는 커밋 모양 (h2 · B10)"
slug: after-0928-parallel-guard
created: "2026-09-28 10:47"
complexity: "복잡"
conditions: 23
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:44b7000a48c52ae6
measurement_digest: sha256:05e740133d2ff998
locked_at: "2026-09-28 10:56"
---

## 배경

남은 일 목록(통합 폴더 `.harness/.meta/after-kaizen-0928/remaining.md`) B10 을 고친다. 레포 밖 `~/.claude/hooks/parallel-session-guard.sh` 가 다음 모양의 진짜 커밋을 못 잡는다: 큰따옴표 안 역따옴표 치환 · 치환 안에서 도는 `git commit` · `git -c k=v commit` · 서브셸 `( … )` · `{ …; }` · `then` / `time` / `command` 뒤 · `bash -c '…'`. 그리고 `git -C $W …` 처럼 풀 수 없는 경로를 가리키는 커밋 뒤 알림이 세션 폴더의 HEAD 를 보여 준다.
사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).

- `W` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h2` (작업 폴더 · 계약 뿌리, 가지 `chore/ak3-h2`)
- `M` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0926b` (통합 폴더의 지난 묶음 시험, 읽기만)
- `T` = `$W/.harness/.meta/after-kaizen-0928/h2-tools` (봉인 전에 만든 측정 도구와 고치기 전 출력) · `B` = `$W/.harness/.meta/after-kaizen-0928/h2-backup` (고치기 전 설치본 사본)
- 기준 커밋 `95508d9` (가지 시작점). 구간 상한은 `chore/ak3-h2` 가지 끝 — `git -C $W rev-parse --verify chore/ak3-h2` 로 풀고, 못 풀면 `UNRESOLVED` 로 멈춘다. `HEAD` 를 상한으로 쓰지 않는다. 이 가지는 이 계약만 커밋하므로 누적 차이로 잰다
- 「고친 뒤」 는 설치본 훅 편집과 구현 커밋을 모두 마친 상태다. 측정은 이 맥(zsh · BSD sed · ugrep)에서 `bash <스크립트>` 로 부른다. 도구는 해석기가 bash 로 정해져 있다

측정 도구 (`$T` 아래, 봉인 커밋 전에 커밋 `a4fbb26` · `f8b599d` 로 따로 커밋함):

- `h2-cases.sh <훅 폴더>` — 잡을 것 K01~K19 · 글자일 뿐인 것 N01~N13 · 대상 저장소 D01~D05 · 닫히지 않은 입력 E01~E03(이벤트 둘씩). 기대 출력 `h2-expected.txt`, 고치기 전 출력 `h2-before.txt`
- `h2-truth.sh` — K · N 명령을 진짜 bash 와 scratch 의 가짜 git 으로 돌려 커밋이 실제로 불리는지 센다(시험 입력 정답 확인). 봉인 전 출력 `h2-truth.txt`
- `h2-random.sh <기준 훅 폴더> <새 훅 폴더> <시드>` — cx3 `guard-random.sh` 와 같은 재료 · 같은 시드의 무작위 명령 40 개에서 두 판 안내문 맞대기. 공용 도우미는 각 폴더 것을 읽는다
- `h2-speed.sh <훅 폴더>` — 20415 글자 명령을 커밋 전 이벤트로 5 번 돌려 가장 느린 밀리초
- `h2-naive.sh <폴더>` — 양성 대조용으로 따옴표 덮기를 끄고 커밋 찾기를 넓힌 백업 사본을 만든다
- `hooks-before.sha256` — 고치기 전 `~/.claude/hooks` 맨 위 파일 15 개 지문. `guard-before.txt` · `us-before.txt` — 고치기 전 설치본의 cx3 · us 시험 출력

## GAP 분석

- Pre-Edit 감사 (파일:줄 증거, 고치기 전 설치본 sha256 `25b4dae61864b8ca…`):
  - `~/.claude/hooks/parallel-session-guard.sh:52-75` 따옴표 덮기 awk — 큰따옴표 안에서 `$(` 만 치환으로 알고 역따옴표는 모른다(K01). 치환 안 글자는 `_` 로 덮어 안에서 도는 커밋을 못 본다(K02 · K03 · K05). 따옴표 밖 `$(` 는 깊이를 올리지 않는다(`:61-62` 는 깊이 > 0 에서만 괄호를 센다)
  - `:76-80` `-C <값>` 만 지운다(`-c` 는 대소문자가 달라 안 지운다 — K06 · K07). `:82` 명령 위치를 `^` 또는 `[;&|]` 뒤로만 본다 — `(` · `{` · `then` · `do` · `else` · `time` · `command` 뒤와 `bash -c` · `sh -c` 인자(작은따옴표로 덮임)를 못 본다(K08~K17)
  - `:94-99` 대상 폴더 — `cd` 는 `^` · `[;&|]` 뒤만 보고(`(cd` 놓침 — D04), `/` 로 시작하는 글자만 경로로 받아 `"$W"` · `"$X"` 는 버리고 세션 폴더로 남는다(D01 · D02 가 세션 저장소 인덱스와 HEAD 를 보여 준다)
  - `:137` 경로 한정(`-o`) 판별은 원문 `$cmd` 에서 찾는다 — K18 · K19 는 모양이 바뀌어도 커밋 전 경고가 없어야 한다
  - `:153` 이미 「값을 못 풀면 조용히 지나간다」 는 선례가 있다(`GIT_INDEX_FILE` 값에 `$` · 역따옴표). D01 · D02 도 같은 원칙으로 조용히 둔다 — 「잘못된 대상을 짚는 경고는 침묵보다 나쁘다」(`:89-90`)
  - `~/.claude/hooks/_lib-hook-payload.sh` (sha256 `dff1e68e…`) 함수 여섯: `hook_field` · `strip_heredoc_bodies` · `hook_deny` · `hook_stop_block` · `hook_stop_context` · `hook_notice`. 따옴표 판별 함수는 없다
  - 쓰는 쪽: `~/.claude/settings.json:14` · `:152` 이 이 훅을 PreToolUse · PostToolUse 로 부른다. 안내문 모양은 바꾸지 않는다
- 시험 입력 정답: `h2-truth.txt` 에서 K01~K19 는 모두 `ran=1`, N01~N13 은 모두 `ran=0` (봉인 전 실측) — 잡을 것은 진짜 커밋이고 글자일 뿐인 것은 커밋이 안 돈다
- 고치기 전 실측: `h2-cases.sh ~/.claude/hooks` 가 K 19 줄 모두 `pre=0 post=0`, D01 · D02 · D04 가 세션 저장소를 가리킨다(`r=1 r2=0`). 기대와 다른 줄 22 개(diff 44 줄)

## 범위 경계

```text
# sprint-scope
```

- 레포 밖: `~/.claude/hooks/parallel-session-guard.sh` 만 고친다. 따옴표 · 명령 위치 판별을 다른 훅도 쓸 공용으로 빼면 같은 폴더 `_lib-hook-payload.sh` 까지. 고치기 전 사본은 `$B` 에 커밋돼 있다(`a4fbb26`). `~/.claude/settings.json` 과 다른 훅 13 개는 건드리지 않는다
- 레포 안: `.harness/` 아래만 — 이 계약 · 개정 · 피드백, `$T` · `$B`, 결과 노트 `.harness/.meta/after-kaizen-0928/h2-notes.md`. 위 범위 목록 블록이 비어 있는 것은 `.harness/` 밖 레포 경로를 하나도 고치지 않는다는 뜻이다
- 하지 않는 것: 상대 경로 `cd ..` · `git -C sub` 의 대상 풀기(B10 에 없다), `eval` · `xargs` · `nohup` · `exec` 뒤 커밋, 여러 겹 `bash -c "sh -c '…'"`. 통합 폴더 · 본 체크아웃 · 다른 워크트리 · 봉인된 `.harness` 파일. 킷 버전 올리기 · 릴리스 · 푸시
- CI 등록: 대상 훅이 레포 밖(`~/.claude/hooks`)이라 GitHub CI 기계에는 없다. 새 시험을 CI 에 올릴 수 없고, 측정 도구는 `$T` 에 두어 평가자가 그대로 돌린다
- 오라클 해소: SC-01 · SC-02 · SC-03 · ER-02 의 기대값은 `h2-truth.sh` 가 진짜 bash 로 확인한 정답과 GAP 분석의 「조용히 둔다」 원칙에서 나왔다. RE-01 은 평가자가 새 함수를 읽어 판정한다
- 오라클 해소: DG-05 — 글자 찾기가 아니라 로컬 CI 와 여덟 명령을 실제로 돌려 요약 줄과 종료 코드로 판정한다
- 커버리지 해소: SC-01 — `~/.claude/hooks` 와 `h2-expected.txt` 는 측정 줄의 빈칸 든 명령(`bash $T/h2-cases.sh ~/.claude/hooks | … $T/h2-expected.txt`) 안에 있어 검출기가 못 본다
- 교차 진단 반영: AR-02 서명 문구가 세션 규칙과 어긋날 수 있다는 지적 — 구현 세션(bda55d45…)에 주어진 커밋 서명 규칙이 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이라 조건 문구와 같다. 조건은 그대로 둔다
- 커버리지 해소: AR-03 — `$B` 의 두 사본 · 설치본 두 파일 · `hooks-before.sha256` · `~/.claude/settings.json` 은 모두 측정 줄의 빈칸 든 명령(`shasum -a 256 $B/…` · `stat -f %m ~/.claude/hooks/…` · `grep -cF … ~/.claude/settings.json`) 안에 있다. `~/.claude/hooks` 의 다른 13 개는 `hooks-before.sha256` 을 거른 `shasum -c` 가 덮는다. AR-05 — 도구 여섯은 조건 아래 측정 줄에 이름마다 적혀 있다. DG-05 — CI 파일에만 있는 단계 여덟은 측정 줄에 명령마다 적혀 있다

## 회귀 게이트

- cx3 시험 `$M/cx3-tools/guard-cases.sh ~/.claude/hooks` 는 고치기 전 설치본에서 `guard-expected.txt` 와 차이 0 줄(10 줄). us 시험 `$M/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md` 는 `us-result-after.txt` 와 차이 0 줄(68 줄), 표준오류 0 줄
- 로컬 CI: `TMPDIR=<scratch>/…/tmp bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W`. 봉인 전 기준(2026-09-28 10:4x): 요약 26 줄 가운데 `rc=0` 25 줄, `feedback-agg-test SKIP (yq 없음)` 1 줄. CI 파일에만 있는 단계 여덟도 봉인 전 모두 종료 코드 0

## Skill

- [ ] SK-00: N/A (스킬 · 에이전트 파일을 만들거나 고치지 않는다 — 대상은 레포 밖 셸 훅이다. 측정: `git -C $W diff --name-only 95508d9 chore/ak3-h2 | grep -cE '(^|/)(SKILL|agents/[^/]+)\.md$'` 이 0)

## Script

- [ ] SC-01: 진짜로 커밋이 도는 새 모양 19 가지를 커밋 전 경고와 커밋 뒤 알림으로 잡는다 — Given 고친 뒤 설치본 `~/.claude/hooks`, When `h2-cases.sh ~/.claude/hooks` 를 돌리면, Then `K` 로 시작하는 19 줄이 `h2-expected.txt` 의 `K` 줄과 같다 — K01 큰따옴표 안 역따옴표 뒤 커밋 · K02~K05 치환(`$( )` · 역따옴표, 따옴표 밖과 큰따옴표 안) 안 커밋 · K06 · K07 `git -c k=v commit` · K08 · K09 서브셸 · K10 `{ …; }` · K11 `then` · K12 `time` · K13 `command` · K14 `bash -c '…'` · K15 `sh -c "…"` · K16 `do` · K17 `else` 는 `pre=1 post=1`, 경로를 한정한 K18 서브셸 · K19 `bash -c` 는 `pre=0 post=1` [exact, enumerated]
  측정: `bash $T/h2-cases.sh ~/.claude/hooks | grep -E '^K' | diff - <(grep -E '^K' $T/h2-expected.txt) | grep -cE '^[<>]'` 이 0 이고 `bash $T/h2-cases.sh ~/.claude/hooks | grep -cE '^K[0-9]{2} '` 가 19
  음성 대조: 고치기 전 설치본(`$T/h2-before.txt`)은 19 줄 모두 `pre=0 post=0` 이라 같은 측정이 38 (봉인 전 실측). 명령 위치 판별을 고치기 전으로 되돌리면 FAIL 한다
  알려진 답: `bash $T/h2-truth.sh | grep -E '^K' | grep -c 'ran=1'` 이 19 (봉인 전 실제값 19, 종료 코드 0) — 19 가지 모두 진짜 bash 에서 커밋이 불린다
- [ ] SC-02: 글자일 뿐인 13 가지는 계속 조용하다 — Given 고친 뒤, When 같은 도구를 돌리면, Then `N` 으로 시작하는 13 줄이 모두 `pre=0 post=0` 이다 — N01 작은따옴표 안 역따옴표 · N02 큰따옴표 안 `\`` · N03 작은따옴표 안 `$( )` · N04 큰따옴표 안 `\$( )` · N05 큰따옴표 안 `( … )` · N06 작은따옴표 안 `{ …; }` · N07 큰따옴표 안 `then` · N08 `echo` 인자 `time` · N09 `printf` 인자 `command` · N10 `echo` 인자 `bash -c` · N11 큰따옴표 안 `git -c x commit` · N12 작은따옴표 안 `bash -c "…"` · N13 `bash -c` 안 큰따옴표 글자 [exact, enumerated]
  측정: `bash $T/h2-cases.sh ~/.claude/hooks | grep -E '^N' | diff - <(grep -E '^N' $T/h2-expected.txt) | grep -cE '^[<>]'` 이 0 이고 `N` 줄이 13
  양성 대조: `bash $T/h2-naive.sh <scratch 새 폴더>` 로 만든 넓힌 사본에 같은 측정을 돌리면 24 (N11 을 뺀 12 줄이 `pre=1 post=1`, 봉인 전 실측). 고치기 전 설치본은 0
  알려진 답: `bash $T/h2-truth.sh | grep -E '^N' | grep -c 'ran=0'` 이 13 (봉인 전 실제값 13)
- [ ] SC-03: 풀 수 있는 대상 저장소는 그쪽 HEAD 를 보여 준다 — Given 고친 뒤, When 같은 도구를 돌리면, Then D03 `git -C <다른 저장소 절대경로> commit` 은 `pre=0 post=1 r=0 r2=1`, D04 `(cd <다른 저장소 절대경로> && git commit …)` 은 `pre=0 post=1 r=0 r2=1`, D05 평범한 `git commit` 은 `pre=6 post=1 r=1 r2=0` 이다 [exact, enumerated]
  측정: `bash $T/h2-cases.sh ~/.claude/hooks | grep -E '^D0[345] ' | diff - <(grep -E '^D0[345] ' $T/h2-expected.txt) | grep -cE '^[<>]'` 이 0
  음성 대조: 고치기 전 설치본은 D04 가 `pre=6 post=1 r=1 r2=0` 이라 같은 측정이 2 (봉인 전 실측). 서브셸 안 `cd` 를 대상으로 안 보면 FAIL 한다
- [ ] SC-04: 고치기 전에 잡던 것은 계속 잡고 조용하던 것은 계속 조용하다 (cx3 시험) — Given 고친 뒤, When `$M/cx3-tools/guard-cases.sh ~/.claude/hooks` 를 돌리면, Then 출력이 `$M/cx3-tools/guard-expected.txt` 와 줄까지 같다 — X1~X5 `pre=1 post=1`, T1~T3 `pre=0 post=0`, E1 두 줄 `rc=0 out=0 err=0` [exact]
  측정: `bash $M/cx3-tools/guard-cases.sh ~/.claude/hooks | diff - $M/cx3-tools/guard-expected.txt | grep -cE '^[<>]'` 이 0
  음성 대조: us 백업 판(`$M/us-backup`)은 같은 측정이 6 (봉인 전 실측) — 큰따옴표 안 치환 판별이 빠지면 FAIL 한다
- [ ] SC-05: us 시험이 고치기 전과 줄까지 같다 — Given 고친 뒤, When `bash $M/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md` 를 돌리면, Then 표준출력이 `$M/us-result-after.txt` (68 줄)와 같고 표준오류가 빈다 [exact]
  측정: `bash $M/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md 2>$E | diff - $M/us-result-after.txt | grep -cE '^[<>]'` 이 0, `grep -c . $E` 가 0 (`$E` 는 scratch 아래 새 파일)
  음성 대조: 같은 시험을 us 백업 판(`$M/us-backup`, `$M/us-backup/handoff-SKILL.md`)에 돌리면 22 (봉인 전 실측) — 따옴표 · 개인 인덱스 판별이 빠지면 FAIL 한다
- [ ] SC-06: 새 모양이 없는 무작위 명령에서는 안내문이 한 글자도 안 바뀐다 — Given 고친 뒤, When `h2-random.sh $B ~/.claude/hooks <시드>` 를 시드 11 · 22 · 33 으로 돌리면, Then 세 마지막 줄이 모두 `cases=40 has_dq_subst=0` 이고 `diff=0` 이다 [exact, enumerated]
  측정: `for s in 11 22 33; do bash $T/h2-random.sh $B ~/.claude/hooks $s | tail -1; done`
  양성 대조: 같은 도구로 `$M/us-backup` 과 고치기 전 설치본을 시드 11 로 맞대면 `diff=19`, `$B` 와 `h2-naive.sh` 사본을 맞대면 `diff=25` (둘 다 봉인 전 실측). 고치기 전 `$B` 와 설치본끼리는 세 시드 모두 `diff=0` (`$T/h2-random-before.txt`)
- [ ] SC-07: 긴 명령에서도 훅이 빨리 끝난다 — Given 고친 뒤, When `h2-speed.sh ~/.claude/hooks` 를 돌리면, Then 출력이 `chars=20415 warned=1` 을 담고 `max_ms` 가 1000 이하다 [exact]
  측정: `bash $T/h2-speed.sh ~/.claude/hooks` 한 줄에서 `max_ms=` 뒤 수 ≤ 1000. 봉인 전 기준 110 · 115 · 264 (세 번 실측)
  음성 대조: `warned=0` 이면 끝의 진짜 커밋을 놓친 것이라 FAIL 한다

## Error

- [ ] ER-01: 망가진 입력과 닫히지 않은 새 모양에서도 조용히 끝난다 — Given 고친 뒤, Then (a) `h2-cases.sh` 의 `E01-` · `E02-` · `E03-` 여섯 줄(닫히지 않은 `bash -c '…` · 큰따옴표 안 닫히지 않은 역따옴표 · 닫히지 않은 `(`)이 모두 `rc=0 out=0 err=0` 이고 (b) us 시험의 `ER01-pre-` · `ER01-post-` 여섯 줄(빈 입력 · 깨진 JSON · jq 없음)이 모두 `rc=0 empty=1 stderr_empty=1` 이며 (c) `bash -n ~/.claude/hooks/parallel-session-guard.sh` 종료 코드가 0 이다 [exact, enumerated]
  측정: `bash $T/h2-cases.sh ~/.claude/hooks | grep -cE '^E0[123]-(Pre|Post)ToolUse rc=0 out=0 err=0$'` 이 6, `bash $M/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md | grep -E '^ER01-(pre|post)-' | grep -c 'rc=0 empty=1 stderr_empty=1'` 이 6, `bash -n` 종료 코드 0
- [ ] ER-02: 풀 수 없는 대상 폴더를 가리키는 커밋에는 경고도 알림도 내지 않는다 — Given 고친 뒤, When 같은 도구를 돌리면, Then D01 `git -C "$W" commit -m x` 와 D02 `cd "$X" && git commit -m x` (세션 폴더는 워크트리 둘 · 스테이징 있는 저장소) 가 둘 다 `pre=0 post=0 r=0 r2=0` 이다 [exact, enumerated]
  측정: `bash $T/h2-cases.sh ~/.claude/hooks | grep -E '^D0[12] ' | diff - <(grep -E '^D0[12] ' $T/h2-expected.txt) | grep -cE '^[<>]'` 이 0
  음성 대조: 고치기 전 설치본은 둘 다 `pre=6 post=1 r=1 r2=0` (세션 저장소를 잘못 짚음)이라 같은 측정이 4 (봉인 전 실측)

## Architecture

- [ ] AR-01: 레포 안 변경이 `.harness/` 밖에 없다 — Given 구현 커밋 완료, When `git -C $W diff --name-only 95508d9 chore/ak3-h2 -- . ':(exclude).harness/'` 를 돌리면, Then 출력 0 줄이다 (범위 목록 블록이 비어 있는 것과 같은 뜻) [exact]
  측정: 위 명령 `| grep -c .` 이 0. 상한은 `git -C $W rev-parse --verify chore/ak3-h2`, 못 풀면 `UNRESOLVED`. 봉인 전 기준값 0 (`95508d9..f8b599d`)
  양성 대조: 같은 명령을 구간 `3517826 a5152c5` 로 돌리면 17 (봉인 전 실측) — 명령이 `.harness/` 밖 레포 경로 변경을 센다
- [ ] AR-02: 커밋 규칙을 지켰다 — Given 구현 커밋 완료, Then `95508d9..chore/ak3-h2` 의 커밋마다 (a) 담은 경로의 맨 위 폴더가 하나다 (b) 메시지에서 끝 빈 줄을 걷어낸 마지막 줄이 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이고 그 앞 줄이 빈 줄이다 (c) 병합 커밋이 0 개다 [exact]
  측정: `git -C $W rev-list 95508d9..chore/ak3-h2` 의 커밋 `c` 마다 `git -C $W show --name-only --format= $c | awk -F/ 'NF{print $1}' | LC_ALL=C sort -u | grep -c .` 이 1, `git -C $W log -1 --format=%B $c | awk -v S='Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>' '{a[NR]=$0} END{n=NR; while (n>0 && a[n]=="") n--; print ((a[n]==S && a[n-1]=="") ? "sig=ok" : "sig=bad")}'` 이 `sig=ok`, `git -C $W rev-list --merges 95508d9..chore/ak3-h2 | grep -c .` 이 0
  양성 대조: 서명 측정은 `a4fbb26` 에서 `sig=ok`, 서명 줄이 없는 `01b1cac` 에서 `sig=bad` (봉인 전 실측)
- [ ] AR-03: 백업을 먼저 커밋했고 다른 훅과 설정은 그대로다 — Given 구현 완료, Then (a) `$B/parallel-session-guard.sh` sha256 이 `25b4dae61864b8cae928ea198d2a97f6cbca71f3fc4c0af2cdd7175449627d6c` 이고 `$B/_lib-hook-payload.sh` 가 `dff1e68e020a502805c9de034d21b8a18abd857d45302fe54686c71089b625d3` 이다 (b) 백업을 처음 담은 커밋 시각(`%ct`)이 설치본 `parallel-session-guard.sh` 수정 시각(`stat -f %m`)보다 이르다 (c) 설치본 `_lib-hook-payload.sh` 를 고쳤으면 같은 순서 조건을 지키고, 안 고쳤으면 지문이 (a) 값 그대로다 (d) `~/.claude/hooks` 맨 위 파일이 15 개이고 두 대상을 뺀 13 개 지문이 `$T/hooks-before.sha256` 과 같다 (e) `~/.claude/settings.json` 에 `parallel-session-guard.sh PreToolUse` · `parallel-session-guard.sh PostToolUse` 가 각각 한 번 든다 [exact, enumerated]
  측정: `shasum -a 256 $B/parallel-session-guard.sh $B/_lib-hook-payload.sh`, `git -C $W log --diff-filter=A --format=%ct -- .harness/.meta/after-kaizen-0928/h2-backup/parallel-session-guard.sh | tail -1` 과 `stat -f %m ~/.claude/hooks/parallel-session-guard.sh` 비교(봉인 전 1790559669 대 1790505686 — 아직 안 고쳐 거꾸로다), `cd ~/.claude/hooks && grep -vE ' \./(parallel-session-guard|_lib-hook-payload)\.sh$' $T/hooks-before.sha256 | shasum -a 256 -c - | grep -vc ': OK$'` 이 0, `find ~/.claude/hooks -maxdepth 1 -type f | grep -c .` 이 15, `grep -cF 'parallel-session-guard.sh PreToolUse' ~/.claude/settings.json` 과 `grep -cF 'parallel-session-guard.sh PostToolUse' ~/.claude/settings.json` 이 각각 1
- [ ] AR-04: 결과 노트가 남아 있다 — Given 구현 완료, Then `$W/.harness/.meta/after-kaizen-0928/h2-notes.md` 가 커밋돼 있고 (a) B10 의 모양 여덟(큰따옴표 안 역따옴표 · 치환 안 커밋 · `git -c` · 서브셸 · `{ …; }` · `then`/`time`/`command` · `bash -c` · 풀 수 없는 대상 폴더)마다 결과와 해당 측정값 (b) `tone-kit:tone-guide` 5 단계 대조 표(규칙 · 건수 · 판정, 대상은 훅에 더한 줄) (c) 로컬 CI 요약 줄과 CI 파일에만 있는 단계 여덟의 종료 코드 를 담는다 [structural, enumerated]
  측정: `git -C $W ls-files --error-unmatch .harness/.meta/after-kaizen-0928/h2-notes.md` 종료 코드 0, 평가자가 파일을 읽어 (a)~(c) 를 확인
- [ ] AR-05: 측정 도구가 봉인 뒤 바뀌지 않았다 — Given 구현 완료, Then `$T` 의 `h2-cases.sh` · `h2-truth.sh` · `h2-random.sh` · `h2-speed.sh` · `h2-naive.sh` · `h2-expected.txt` 의 sha256 앞 16 자리가 차례로 `8483be1e695a157f` · `17ce1709e994270b` · `9931a3cc1f762e40` · `09acd39cc44261b2` · `f0c36298f4cc9a44` · `236f259254040a51` 이다 [exact, enumerated]
  측정: `cd $T && shasum -a 256 h2-cases.sh h2-truth.sh h2-random.sh h2-speed.sh h2-naive.sh h2-expected.txt | cut -c1-16` 이 위 여섯 값과 차례로 같다

## Anti-patterns

- [ ] AP-00: N/A (대상이 레포 밖 `~/.claude/hooks` 셸 훅과 `.harness/` 기록뿐 — project.yaml 패턴 넷은 레포 플러그인 파일 전용: AP-01 버전 하드코딩 · AP-02 force push · AP-03 · AP-04 는 validate-plugin 이 킷 폴더만 잰다)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
  측정: 훅에 새 셸 함수를 정의했으면 따옴표 · 명령 위치 판별처럼 다른 훅(`enforce-codex-stdin.sh` 등)도 쓸 일인지 평가자가 읽어 판정하고, 그렇다면 `_lib-hook-payload.sh` 에 있어야 PASS. 새 함수 0 개면 PASS (`grep -cE '^[a-z_]+\(\) *\{' ~/.claude/hooks/parallel-session-guard.sh` 를 `$B` 사본의 1 과 비교)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  측정: heredoc 본문 제거는 공용 `strip_heredoc_bodies` 를 계속 쓴다 — `grep -c 'strip_heredoc_bodies' ~/.claude/hooks/parallel-session-guard.sh` ≥ 1 (봉인 전 2)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git -C $W diff --name-only 95508d9 chore/ak3-h2 | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 셸 진단 경고 0 — Given 고친 뒤, Then `shellcheck -f gcc ~/.claude/hooks/parallel-session-guard.sh` 와 `shellcheck -f gcc ~/.claude/hooks/_lib-hook-payload.sh` 출력이 각각 0 줄이다 [exact, enumerated]
  측정: 두 명령 `| grep -c .` 이 각각 0 (봉인 전 0 · 0, `/opt/homebrew/bin/shellcheck`)
  양성 대조: `printf 'x=$1\necho $x\n' > <scratch>/sc.sh; shellcheck -f gcc <scratch>/sc.sh | grep -c .` 이 1 이상 — 세는 식이 경고를 잡는다
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh` 로 릴리스 스크립트만 돈다 — 이번 변경 파일과 교집합 0 개. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경은 셸 훅이다. 훅의 실제 동작은 SC-01 ~ SC-07 · ER-01 · ER-02 가 잰다)
- [ ] DG-05: 로컬 CI 와 CI 파일에만 있는 단계가 기준과 같게 통과한다 — Given 고친 뒤, Then (a) `TMPDIR=<scratch 새 폴더>/tmp bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W` 요약에서 `rc=0` 이 아닌 줄이 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐이고 (b) `$W` 에서 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test design-kit/evals/visuals.spec.js` · `npx playwright test api-kit/evals/` 여덟의 종료 코드가 모두 0 이다 [exact, enumerated]
  측정: `<TMPDIR>/ci-local/summary.txt` 에서 `grep -vc 'rc=0'` 이 1 이고 그 줄이 `feedback-agg-test SKIP (yq 없음)`. 여덟 명령은 하나씩 `bash -c '<명령>'` 으로 돌려 종료 코드를 본다(zsh 는 변수 속 명령을 낱말로 안 쪼갠다). 봉인 전 기준: 요약 `rc=0` 25 줄 + SKIP 1 줄, 여덟 모두 0

사용자가 할 일: 없음
