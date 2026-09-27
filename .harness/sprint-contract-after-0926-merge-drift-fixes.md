---
feature: "합친 뒤 어긋남 고침 — design-mockup 단계 번호 · 종료 코드 표 · 병렬 세션 훅 따옴표 · superseded 상태 (cx3)"
slug: after-0926-merge-drift-fixes
created: "2026-09-27 19:20"
complexity: "복잡"
conditions: 25
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:6c4191696be56f14
measurement_digest: sha256:eac93e473d1b60da
locked_at: "2026-09-27 19:31"
---

## 배경

부모 교차 진단(통합 폴더 `.harness/.meta/after-kaizen-0926b/parent-xdiag.md` 5~10 줄)이 짚은 「합친 뒤 생긴 어긋남」 넷을 고친다.
사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 코덱스로 점검 …」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).

- (1) k2 가 design-mockup 단계를 다시 매겨(0cfcb03) 자동 감지가 Step 0 이 됐는데, `design-kit/skills/design-mockup/SKILL.md:171` 과 `docs/design-kit/design-mockup.html:665` 가 아직 「Step 2 가 폐기 칸의 경로를 따라 원문을 읽는다」 라고 한다. 폐기 칸 경로를 따라 읽는 일은 Step 0 본문(SKILL.md 57 줄)에 있다.
- (2) `harness/evals/gate-exit-codes.md` 머리 설명은 「게이트 스크립트는 … 인용만 한다」 이고 「소비처」 표는 이 파일을 인용하는 스크립트 목록이다. dr1a(92377e0)가 `scripts/check-api-kit-docs.py` 행을 더했는데 그 스크립트는 이 파일을 인용하지 않는다(인용 11 · 행 12).
- (3) us 묶음이 `~/.claude/hooks/parallel-session-guard.sh` 에 따옴표 판별을 넣은 뒤, 큰따옴표 안 `$( … )` 속 큰따옴표를 바깥 따옴표의 닫힘으로 읽는다. `echo "$(echo "it's")"; git commit -m x` 에서 `it's` 의 작은따옴표가 따옴표를 새로 열어 뒤의 진짜 커밋까지 덮는다. 고치기 전 us 백업 판은 이 커밋을 잡는다.
- (4) 이 세션이 1 회차 계약 셋(k3 · k4 · l2)에 쓴 `status: superseded` 가 `harness/references/contract-schema.md` 의 허용 값(`active | done`) 밖이고 새 판을 가리키는 칸이 없다. 계약 고르기(qa-evaluator Step 1-c · 스키마 ladder)는 `active` · `done` 이 아닌 값을 레거시로 센다 — superseded 계약 하나만 남으면 3.5b 가 그것을 고르고, 레거시 계약 하나와 함께 있으면 레거시를 둘로 세어 BLOCKED 가 된다(봉인 전 실측, 아래 SC-01).

공통 이름 (측정 줄에서 쓴다):

- `W` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cx3` (이 계약의 작업 폴더 · 계약 뿌리)
- `M` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b` (통합 폴더, 읽기만)
- `T` = `$W/.harness/.meta/after-kaizen-0926b/cx3-tools` (이 계약이 봉인 전에 만든 측정 도구와 고치기 전 출력)
- 기준 커밋 `a314ecc` (가지 `chore/ak2-cx3` 의 시작점). 구간 상한은 `chore/ak2-cx3` 가지 끝이다 — `git -C $W rev-parse --verify chore/ak2-cx3` 로 풀고, 못 풀면 `UNRESOLVED` 로 멈춘다. `HEAD` 를 상한으로 쓰지 않는다
- 「고친 뒤」 는 구현 커밋을 모두 마친 상태다. 측정은 이 맥(zsh · BSD sed · ugrep)에서 `bash <스크립트>` 로 부른다

측정 도구 (`$T` 아래, 봉인 커밋 전에 따로 커밋한다 — 봉인 커밋은 계약 파일 하나만 담는다):

- `step-refs.py <판 뿌리>` — (1) 두 파일의 「Step N」 인용 하나마다 가리킨 절 제목과 문장 뜻을 대조. 마지막 줄 `refs= ok= bad= unclassified=`
- `table-cite.sh <판 뿌리>` — (2) hs 묶음 도우미 `hs5.sh` 사본. 첫 줄 `cite= rows= missing= extra=`
- `guard-cases.sh <훅 폴더>` — (3) 재현 넷 · 글자로만 남아야 하는 것 셋 · 산술 확장 하나 · 닫히지 않은 입력. 기대 출력 `guard-expected.txt`
- `guard-random.sh <기준 훅 폴더> <새 훅 폴더> <시드>` — (3) 큰따옴표 안 `$(` 가 없는 무작위 명령 40 개에서 두 판 안내문 맞대기
- `ladder-cases.sh <판 뿌리>` — (4) qa-evaluator Step 1-b · 1-c 블록과 스키마 ladder 블록을 떼어 입력 넷에 돌린다. 기대 출력 `ladder-expected.txt`
- `supersede-check.sh <계약 뿌리>` — (4) `status: superseded` 계약마다 새 판 칸 · 대상 존재 · 대상 상태 · 대상 슬러그 · 봉인
- 고치기 전 출력: `step-refs-before.txt` · `table-cite-before.txt` · `guard-before-backup.txt` · `guard-before-current.txt` · `ladder-before.txt` · `supersede-before.txt`, 훅 폴더 지문 `hooks-before.sha256`

## GAP 분석

- Pre-Edit 감사 (파일:줄 증거):
  - `design-kit/skills/design-mockup/SKILL.md:38` `## Step 0: 자동 감지 및 로드` · `:57` 「승인 기록 폐기 칸이 경로를 가리킴 → 그 파일을 열어 원문을 읽는다」 · `:171` 「다음 시안 전에는 Step 2 가 폐기 칸의 경로를 따라 원문을 읽는다」 — 어긋남 1 곳. 같은 파일의 다른 인용 `:29` Step 5 · `:58` Step 1 · `:59` Step 2-a 는 맞다
  - `docs/design-kit/design-mockup.html:460` Step 0 제목 · `:665` 같은 옛 문장 · `:485` Step 1 / Step 2-a · `:756` Step 5 는 맞다. 옛 문장이 든 파일은 `.harness` 밖에서 이 둘뿐(`grep -rlF '폐기 칸의 경로를 따라'`)
  - `harness/evals/gate-exit-codes.md:3-4` 「게이트 스크립트 … 인용만 한다」 · `:72` `scripts/check-api-kit-docs.py` 행. `scripts/check-api-kit-docs.py:1-15` 머리 설명에 종료 코드 인용 없음 · `:111` `return 1 if bad else 0`. 같은 표의 `scripts/check-docs-a11y.js:31` 은 「종료 코드 의미: harness/evals/gate-exit-codes.md」 로 인용한다
  - `~/.claude/hooks/parallel-session-guard.sh` 따옴표 덮기 awk 블록(`cmd_unquoted=` 줄부터) 이 `$(` 를 모른다. 설치본은 `$M/us-after/parallel-session-guard.sh` 와 바이트까지 같고(`cmp` 0), `_lib-hook-payload.sh` 는 `$M/us-backup/` 사본과 같다
  - `harness/references/contract-schema.md:215` `status: active  # v5 — active | done` · `:262` 필드 표 `active | done` · `:392-399` status 해석 규칙 · `:456-460` ladder 블록 `case` 가 `active` · `"done"` 외를 레거시로 센다. `harness/agents/qa-evaluator.md:259-264` status 표 · `:293-305` 1-c 블록이 `active` · `done` 외를 `LEGACY` 에 넣는다. `harness/docs/guides/qa-evaluation-guide.md:224-230` 같은 표. `docs/harness/contract-schema.html:445` · `docs/harness/qa-evaluation-guide.html:365` 가 그 표의 페이지 판
  - 쓰는 쪽: `~/.claude/hooks/qa-pending-check.sh:70` 은 `active` 만 본다 — superseded 를 새로 알 필요 없음. 커밋 범위 훅도 `status: active` 만 본다(스키마 §범위 목록 블록)
- (2) 방향 결정: 표 머리 설명이 「게이트 스크립트는 인용만 한다」 이고 표 이름이 「소비처」 라서, 행을 빼지 않고 스크립트가 표를 인용하게 한다. `check-api-kit-docs.py` 는 0(전부 통과) · 1(하나라도 실패)을 이 표의 뜻대로 쓰는 문서 검사다
- (4) 이름 결정: 새 판을 가리키는 칸은 `superseded_by` 다. design-kit 결정 전파 규칙(`design-kit/references/visual-change-protocol.md` §6)이 같은 뜻으로 `superseded` · `superseded_by` 를 쓴다. 값은 새 판 계약의 슬러그(따옴표 없이)이고 사슬은 금지(가리킨 계약이 다시 superseded 면 안 된다)

## 범위 경계

```text
# sprint-scope
design-kit/skills/design-mockup/SKILL.md
docs/design-kit/design-mockup.html
harness/evals/gate-exit-codes.md
scripts/check-api-kit-docs.py
harness/references/contract-schema.md
harness/agents/qa-evaluator.md
harness/docs/guides/qa-evaluation-guide.md
docs/harness/contract-schema.html
docs/harness/qa-evaluation-guide.html
```

- 레포 밖: `~/.claude/hooks/parallel-session-guard.sh` 만 고친다. 따옴표 판별을 공용으로 빼야 하면 같은 폴더 `_lib-hook-payload.sh` 까지. 고치기 전에 `$W/.harness/.meta/after-kaizen-0926b/cx3-backup/` 에 복사해 커밋한다
- `.harness/` 아래: 이 계약 · 개정 · 피드백, `cx3-tools/` · `cx3-backup/` · 결과 노트 `cx3-notes.md`, 그리고 superseded 계약 셋(`sprint-contract-after-0926-kits-reflect-bambu-tone.md` · `sprint-contract-after-0926-kits-api-onboarding-howto.md` · `sprint-contract-after-0926-mdlint-l2.md`)의 앞머리 한 줄(`superseded_by:`)만. 셋의 조건 줄 · 측정 줄 · 서술 절은 건드리지 않는다
- 하지 않는 것: user-hooks 훅이 고치기 전에도 못 잡던 모양(`git -c k=v commit` · 서브셸 · `{ …; }` · `then` · `time` · `command` · `bash -c`)과 큰따옴표 안 `$( git commit … )` 처럼 치환 안에서 도는 진짜 커밋 — 고치기 전 백업도 못 잡았다(`(` 뒤라 명령 위치로 안 본다). 킷 버전 올리기 · 릴리스 · 푸시. qa-evaluator Step 1-e 봉인 대조의 `status: (active|done)` 거르기(superseded 계약은 평가 대상이 아니다). sprint-contract 스킬 본문(작성 스킬은 superseded 를 쓰지 않는다)
- 오라클 해소: SK-02 · SK-03 — 고칠 대상이 문서 문장 자체라 글자 확인이 곧 결과다. superseded 의 실제 동작은 SC-01(블록을 떼어 실행) · ER-02(실행) 가 잰다. SC-06 · DG-02 · DG-05 는 명령을 실행해 그 출력으로 판정한다
- 커버리지 해소: SK-02 — `.harness/` 는 측정의 `--exclude-dir=.harness` 로 덮는다. SK-02 · SK-04 · AR-03 의 나머지 경로는 조건 아래 들여쓴 측정 줄에 그대로 적혀 있다(검출기는 조건 줄만 본다) — SK-04 의 두 HTML 은 세 `grep -cE … docs/harness/…html` 명령이 덮는다. AR-03 — `~/.claude/hooks` 폴더는 `find ~/.claude/hooks -maxdepth 1` 과 `cd ~/.claude/hooks && … shasum -c` 로, `_lib-hook-payload.sh` 는 (c) 의 `shasum -a 256` 과 지문 목록 거르기로 덮는다
- T1(`echo "$(echo "a; git commit -m y")"`)은 고치기 전 두 판 모두 경고를 냈지만 안쪽 큰따옴표 안 글자라 진짜 커밋이 아니다. 치환 안을 제대로 읽으면 조용해지는 것이 맞으므로 기대값을 `pre=0 post=0` 으로 둔다

## 회귀 게이트

- 로컬 CI: `TMPDIR=<scratch>/tmp bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W`. 봉인 전 기준(2026-09-27 19:2x, 고치기 전 판): `rc=0` 25 줄, `feedback-agg-test SKIP (yq 없음)` 1 줄, 그 밖 0 줄. ci.yml 의 `measure-helpers-test.sh` 등은 이 스크립트 밖이라 재지 않는다
- us 묶음 시험 `$M/us-test.sh` 출력은 고치기 전 설치본에서 `$M/us-result-after.txt` 와 줄까지 같다(68 줄, 봉인 전 실측 `diff` 0 줄). 백업 판 출력과는 22 줄 다르다

## Skill

- [ ] SK-01: design-mockup 의 「Step N」 인용이 모두 가리키는 절의 뜻과 맞는다 — Given 고친 뒤, When `step-refs.py` 를 작업 폴더에 돌리면, Then 마지막 줄이 정확히 `refs=8 ok=8 bad=0 unclassified=0` 이고 종료 코드 0 이다 [exact]
  측정: `python3 $T/step-refs.py $W | tail -1; echo rc=$?`
  음성 대조: 고치기 전 판(봉인 전 실측 `$T/step-refs-before.txt`)은 `refs=8 ok=6 bad=2 unclassified=0` — SKILL.md:171 · design-mockup.html:665 두 곳이 `bad(want '자동 감지')`. 둘 중 하나만 고치면 `bad=1` 로 FAIL 한다
  알려진 답: 손으로 센 인용 8 개 = SKILL.md 29 · 58 · 59 · 171 줄 + HTML 485 줄 둘 · 665 · 756 줄 (봉인 전 실제값 8, 종료 코드 0)
- [ ] SK-02: 옛 문장이 레포 어디에도 남지 않는다 — Given 고친 뒤, Then `.harness/` 밖에서 「Step 2 가 폐기 칸의 경로를 따라」 가 든 파일 0 개이고, 「폐기 칸의 경로를 따라 원문을 읽는다」 는 `design-kit/skills/design-mockup/SKILL.md` 와 `docs/design-kit/design-mockup.html` 에 각각 정확히 1 번 든다 [exact, enumerated]
  측정: `cd $W && grep -rlF 'Step 2 가 폐기 칸의 경로를 따라' . --exclude-dir=.harness --exclude-dir=node_modules | grep -c .` 이 0, `grep -cF '폐기 칸의 경로를 따라 원문을 읽는다' design-kit/skills/design-mockup/SKILL.md docs/design-kit/design-mockup.html` 이 파일마다 1
  양성 대조: 고치기 전 첫 명령이 2 (두 파일)
- [ ] SK-03: 계약 형식 문서가 `superseded` 상태와 새 판 칸을 정의한다 — Given 고친 뒤 `harness/references/contract-schema.md` 에서, Then (a) `### v5 신규 필드` 표의 `status` 행 값 칸에 `active` · `done` · `superseded` 가 모두 들고 (b) 같은 표에 `superseded_by` 행이 있어 그 규칙 칸에 「슬러그」 · 「superseded」 가 들며 사슬 금지(가리킨 계약이 superseded 가 아님)를 적고 (c) `### status 해석 규칙` 절 목록에 `superseded` 를 active 후보와 레거시 양쪽에서 빼는 줄이 있고 (d) `## 메타데이터` 의 frontmatter 예시 `status:` 줄 주석에 `superseded` 가 든다 [exact, enumerated]
  측정: `awk '/^### v5 신규 필드/{f=1;next} f&&/^#/{exit} f' harness/references/contract-schema.md` 출력에서 `^\| \`status\`` 줄의 `superseded` 수 ≥1 · `^\| \`superseded_by\`` 줄 1 개(그 줄에 `슬러그` · `superseded` 가 든다), `awk '/^### status 해석 규칙/{f=1;next} f&&/^#/{exit} f' … | grep -c 'superseded'` ≥1, `awk '/^## 메타데이터/{f=1;next} f&&/^## /{exit} f' … | grep -E '^status:' | grep -c superseded` 이 1. 사슬 금지 뜻은 평가자가 `superseded_by` 행을 직접 읽어 판정
  양성 대조: 고치기 전 네 측정 모두 0 (봉인 전 실측: 파일 안 `superseded` 0 번)
- [ ] SK-04: 상태 표를 옮겨 적은 쪽 넷이 `superseded` 를 제외 행으로 안다 — Given 고친 뒤, Then 다음 네 파일의 status 표에 `superseded` 가 든 행이 있고 그 행의 active 후보 칸이 「제외」 다: `harness/agents/qa-evaluator.md` (`#### 1-b` 절 표) · `harness/docs/guides/qa-evaluation-guide.md` (`### 판정 근거는 파일 개수가 아니라` 절 표) · `docs/harness/qa-evaluation-guide.html` (`<code>status: done</code>` 행이 든 표). 그리고 `docs/harness/contract-schema.html` 의 필드 표 `status` 행에 `superseded` 가 들고 `superseded_by` 행이 있다 [exact, enumerated]
  측정: md 둘(`harness/agents/qa-evaluator.md` 은 `awk '/^#### 1-b/{f=1;next} f&&/^####/{exit} f'`, `harness/docs/guides/qa-evaluation-guide.md` 는 `awk '/^### 판정 근거는 파일 개수가 아니라/{f=1;next} f&&/^###/{exit} f'` 로 절을 자른다)에서 `grep -cE '^\|.*superseded.*제외'` 가 1 이상 (같은 식으로 `done.*제외` 를 세면 고치기 전 판에서 둘 다 1 — 절 자르기가 표를 잡는다), HTML 은 `grep -cE '<tr><td><code>status: superseded</code>.*제외' docs/harness/qa-evaluation-guide.html` ≥1 · `grep -cE '<tr><td><code>status</code></td>.*superseded' docs/harness/contract-schema.html` ≥1 · `grep -cE '<tr><td><code>superseded_by</code>' docs/harness/contract-schema.html` ≥1
  양성 대조: 고치기 전 네 파일 모두 `superseded` 0 번 (봉인 전 실측)

## Script

- [ ] SC-01: 계약 고르기가 superseded 계약을 active 도 레거시도 아닌 것으로 뺀다 — Given 고친 뒤, When `ladder-cases.sh $W` 를 돌리면(입력 넷: c1 superseded 하나 · c2 superseded + 레거시 하나 · c3 superseded + active 하나 · c4 done + 레거시 하나, 구현 둘: qa-evaluator 1-b · 1-c 블록과 스키마 ladder 블록), Then 출력이 `$T/ladder-expected.txt` 와 줄까지 같다 [exact]
  측정: `bash $T/ladder-cases.sh $W | diff - $T/ladder-expected.txt | grep -cE '^[<>]'` 이 0, 스크립트 종료 코드 0
  음성 대조: 고치기 전 판 출력(`$T/ladder-before.txt`, 봉인 전 실측)과 기대의 차이는 8 줄 — c1 이 두 구현 모두 superseded 계약 `sprint-contract-old.md` 를 3.5b 로 고르고, c2 가 레거시를 둘로 세어 BLOCKED 다. qa-evaluator 쪽 한 곳만 고치면 SCHEMA 두 줄이 남아 FAIL 한다
  알려진 답: c1 은 후보가 있으나 active 0 · 레거시 0 이라 BLOCKED(QA `4 <none>`, 스키마 `BLOCKED active=0`), c2 · c4 는 레거시 하나라 3.5b 로 `sprint-contract-leg.md`, c3 은 active 하나라 3 으로 `sprint-contract-new.md` — 두 규약 문서의 ladder 표에서 손으로 정했다
- [ ] SC-02: 병렬 세션 훅이 큰따옴표 안 `$( … )` 뒤의 진짜 커밋을 다시 잡는다 — Given 고친 뒤 설치본 `~/.claude/hooks`, When `guard-cases.sh ~/.claude/hooks` 를 돌리면, Then 출력이 `$T/guard-expected.txt` 와 줄까지 같다 — 재현 X1(`echo "$(echo "it's")"; git commit -m x`) · X2~X5 는 `pre=1 post=1`, 치환 안 · 바깥 큰따옴표 안 글자 T1~T3 은 `pre=0 post=0`, 닫히지 않은 입력 E1 은 두 이벤트 모두 `rc=0 out=0 err=0` [exact]
  측정: `bash $T/guard-cases.sh ~/.claude/hooks | diff - $T/guard-expected.txt | grep -cE '^[<>]'` 이 0
  음성 대조: 고치기 전 설치본(`$T/guard-before-current.txt`)은 기대와 4 줄 다르다 — X1 `pre=0 post=0`, T1 `pre=1 post=1`. 고치기 전 us 백업(`$T/guard-before-backup.txt`)은 X1 을 `pre=1 post=1` 로 잡되 T1~T3 을 잡아 6 줄 다르다. 따옴표 판별을 통째로 빼 백업처럼 돌아가면 T2 · T3 에서 FAIL 한다
- [ ] SC-03: us 묶음 시험이 고치기 전과 줄까지 같다 — Given 고친 뒤, When `bash $M/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md` 를 돌리면, Then 표준출력이 `$M/us-result-after.txt`(68 줄)와 같고 표준오류가 빈다 [exact]
  측정: `bash $M/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md 2>$E | diff - $M/us-result-after.txt | grep -cE '^[<>]'` 이 0, `grep -c . $E` 가 0 (`$E` 는 scratch 아래 새 파일)
  음성 대조: 같은 시험을 us 백업 판(`$M/us-backup`, 백업 SKILL)에 돌린 출력은 `us-result-after.txt` 와 22 줄 다르다(봉인 전 실측) — 따옴표 · 인덱스 판별이 빠지면 이 측정이 FAIL 한다
- [ ] SC-04: 큰따옴표 안 `$(` 가 없는 명령에서는 안내문이 한 글자도 안 바뀐다 — Given 고친 뒤, When `guard-random.sh $M/us-after ~/.claude/hooks <시드>` 를 시드 11 · 22 · 33 으로 돌리면, Then 세 줄 모두 `cases=40 has_dq_subst=0` 이고 `diff=0` 이다 [exact, enumerated]
  측정: `for s in 11 22 33; do bash $T/guard-random.sh $M/us-after ~/.claude/hooks $s | tail -1; done`
  양성 대조: 같은 도구로 `$M/us-backup` 과 `$M/us-after` 를 시드 11 로 맞대면 `diff=19` (봉인 전 실측) — 맞대기가 차이를 잡는다. 고치기 전 설치본끼리는 세 시드 모두 `diff=0`, 새 판이 경고를 낸 경우 `warned=1 · 4 · 1`
- [ ] SC-05: 종료 코드 표의 행과 그 표를 인용하는 스크립트가 같은 집합이다 — Given 고친 뒤, When `table-cite.sh $W` 를 돌리면, Then 첫 줄이 정확히 `cite=12 rows=12 missing=0 extra=0` 이다 [exact]
  측정: `bash $T/table-cite.sh $W | head -1`
  음성 대조: 고치기 전(`$T/table-cite-before.txt`, 봉인 전 실측) `cite=11 rows=12 missing=0 extra=1` — 행을 빼는 쪽으로 가면 `cite=11 rows=11` 이라 FAIL 한다(GAP 분석 방향 결정)
- [ ] SC-06: `scripts/check-api-kit-docs.py` 가 표를 인용하되 동작은 그대로다 — Given 고친 뒤, Then (a) 파일 첫 20 줄(머리 설명)에 `harness/evals/gate-exit-codes.md` 가 들고 같은 줄 또는 바로 앞뒤 줄에 0 과 1 의 뜻이 적혀 있고 (b) `python3 scripts/check-api-kit-docs.py` 의 표준출력 · 종료 코드와 `--json` 출력이 고치기 전과 같다 [exact]
  측정: `head -20 scripts/check-api-kit-docs.py | grep -c 'gate-exit-codes.md'` ≥1 (뜻 문구는 평가자가 그 줄을 읽어 판정). `python3 scripts/check-api-kit-docs.py | shasum -a 256` 이 `46d7e0adf3e6fed0…` 로 시작하고 종료 코드 0, `python3 scripts/check-api-kit-docs.py --json | shasum -a 256` 이 `28297b8c9f8b5da2…` 로 시작 (둘 다 봉인 전 실측)

## Error

- [ ] ER-01: 병렬 세션 훅이 망가진 입력에서도 조용히 끝난다 — Given 고친 뒤, Then SC-03 출력 가운데 `ER01-` 로 시작하는 여섯 줄이 모두 `rc=0 empty=1 stderr_empty=1` 이고, `guard-cases.sh` 의 `E1-PreToolUse` · `E1-PostToolUse` 두 줄이 `rc=0 out=0 err=0` 이며, `bash -n ~/.claude/hooks/parallel-session-guard.sh` 종료 코드가 0 이다 [exact, enumerated]
  측정: `bash $M/us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md | grep -E '^ER01-(pre|post)-' | grep -vc 'rc=0 empty=1 stderr_empty=1'` 이 0 이고 그 여섯 줄이 있다, `bash $T/guard-cases.sh ~/.claude/hooks | grep -c '^E1-.* rc=0 out=0 err=0$'` 이 2, `bash -n` 종료 코드 0
- [ ] ER-02: superseded 계약 셋이 새 판을 가리키고 봉인은 그대로다 — Given 고친 뒤, When `supersede-check.sh $W` 를 돌리면, Then 마지막 줄이 `superseded=3 valid=3` 이고 셋의 `by=` 가 각각 `after-0926-kits-api-onboarding-howto-r2` · `after-0926-kits-reflect-bambu-tone-r2` · `after-0926-mdlint-l2-r2` 이며 모두 `seal=OK` 다. 그리고 셋의 기준 커밋 대비 차이는 앞머리 안에 더한 `superseded_by:` 한 줄씩뿐이다 [exact, enumerated]
  측정: `bash $T/supersede-check.sh $W`. `git -C $W diff a314ecc chore/ak2-cx3 -- .harness/sprint-contract-after-0926-kits-reflect-bambu-tone.md .harness/sprint-contract-after-0926-kits-api-onboarding-howto.md .harness/sprint-contract-after-0926-mdlint-l2.md | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)[[:space:]]'` 가 정확히 세 줄이고 셋 다 `+superseded_by:` 에 빈칸 하나가 이어진 꼴로 시작 (Given: 구현 커밋 완료, 상한 `chore/ak2-cx3`)
  음성 대조: 고치기 전(`$T/supersede-before.txt`, 봉인 전 실측) `superseded=3 valid=0`, 셋 다 `by=<none>`. 새 판이 superseded 인 계약을 가리키거나 조건 줄을 건드리면 `valid` 가 3 보다 작아 FAIL 한다

## Architecture

- [ ] AR-01: 레포 안 변경이 범위 목록 안에 있다 — Given 구현 커밋 완료, When `git -C $W diff --name-only a314ecc chore/ak2-cx3 -- . ':(exclude).harness/'` 를 `## 범위 경계` 의 `# sprint-scope` 블록과 맞대면, Then 블록 밖 경로 0 개다(포함 관계 — 블록의 모든 경로를 바꿀 필요는 없다) [exact]
  측정: 블록을 `awk '/^# sprint-scope/{f=1;next} f&&/^```/{exit} f' $W/.harness/sprint-contract-after-0926-merge-drift-fixes.md | LC_ALL=C sort` 로 뽑아 `LC_ALL=C comm -23 <(diff 목록 | LC_ALL=C sort) <(블록)` 이 0 줄. 상한은 `git rev-parse --verify chore/ak2-cx3`, 못 풀면 `UNRESOLVED`. 봉인 전 기준값: `a314ecc..a314ecc` 0 줄
- [ ] AR-02: 커밋 규칙을 지켰다 — Given 구현 커밋 완료, Then `a314ecc..chore/ak2-cx3` 의 커밋마다 (a) 킷 하나만 담는다 — 경로를 `design-kit/` · `docs/design-kit/` → design-kit, `harness/` · `docs/harness/` → harness, `scripts/` → scripts 로 묶고 `.harness/` 는 세지 않을 때 묶음 수 ≤ 1 (b) 메시지 마지막 줄이 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이고 그 앞 줄이 빈 줄 (c) 병합 커밋 0 개 [exact]
  측정: `git -C $W rev-list a314ecc..chore/ak2-cx3` 의 커밋마다 `git show --name-only --format= <c>` 를 위 규칙으로 묶어 센 최댓값 ≤1, `git log -1 --format=%B <c> | tail -2` 가 빈 줄 + 그 한 줄, `git rev-list --merges a314ecc..chore/ak2-cx3 | grep -c .` 이 0
- [ ] AR-03: 훅을 고치기 전에 백업을 커밋했고 다른 훅은 그대로다 — Given 구현 완료, Then (a) `$W/.harness/.meta/after-kaizen-0926b/cx3-backup/parallel-session-guard.sh` 의 sha256 이 `5bf30dd50557ba86520487bb86cc0b3f9e2d1e446d645daf860b272e2f9d8194` 다 (b) 그 파일을 처음 담은 커밋의 커밋 시각(`%ct`)이 설치본 훅의 수정 시각(`stat -f %m`)보다 이르다 (c) `_lib-hook-payload.sh` 를 고쳤다면 같은 폴더 백업이 sha256 `dff1e68e020a502805c9de034d21b8a18abd857d45302fe54686c71089b625d3` 이고 같은 순서 조건을 지킨다(안 고쳤으면 설치본 지문이 그 값 그대로) (d) `~/.claude/hooks` 맨 위 파일 15 개 가운데 두 대상을 뺀 13 개 지문이 `$T/hooks-before.sha256` 과 같고 파일 수가 15 다 [exact, enumerated]
  측정: `shasum -a 256`, `git -C $W log --diff-filter=A --format=%ct -- .harness/.meta/after-kaizen-0926b/cx3-backup/parallel-session-guard.sh | tail -1` 과 `stat -f %m ~/.claude/hooks/parallel-session-guard.sh` 비교, `cd ~/.claude/hooks && grep -vE ' \./(parallel-session-guard|_lib-hook-payload)\.sh$' $T/hooks-before.sha256 | shasum -a 256 -c - | grep -vc ': OK$'` 이 0, `find ~/.claude/hooks -maxdepth 1 -type f | grep -c .` 이 15
- [ ] AR-04: 결과 노트가 남아 있다 — Given 구현 완료, Then `$W/.harness/.meta/after-kaizen-0926b/cx3-notes.md` 가 커밋돼 있고 (a) 항목 (1)~(4) 마다 결과와 자기 측정값 (b) `tone-kit:tone-guide` 5 단계 대조 표(규칙 · 건수 · 판정, 대상은 이번에 더한 줄) (c) 로컬 CI 요약 줄 을 담는다 [structural, enumerated]
  측정: `git -C $W ls-files --error-unmatch .harness/.meta/after-kaizen-0926b/cx3-notes.md` 종료 코드 0, 평가자가 파일을 읽어 (a)~(c) 세 부분을 확인

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 판정은 `python3 scripts/validate-plugin.py --check=code-fence` (고친 md: design-mockup SKILL.md · contract-schema.md · qa-evaluator.md · qa-evaluation-guide.md · gate-exit-codes.md)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 — 판정은 `python3 scripts/validate-plugin.py --check=frontmatter` (design-mockup SKILL.md · qa-evaluator.md 를 고친다)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
  측정: 훅에 새 셸 함수를 정의했으면 그것이 따옴표 판별처럼 다른 훅도 쓸 일이면 `_lib-hook-payload.sh` 에 두었는지 평가자가 읽어 판정. 새 함수 0 개면 PASS (`grep -cE '^[a-z_]+\(\) *\{' ~/.claude/hooks/parallel-session-guard.sh` 를 백업과 비교)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  측정: 훅의 heredoc 본문 제거는 기존 공용 함수 `strip_heredoc_bodies` 를 계속 쓴다(`grep -c 'strip_heredoc_bodies' ~/.claude/hooks/parallel-session-guard.sh` ≥1). 스키마 · 평가자의 ladder 는 기존 `fm_get` 을 쓴다

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git -C $W diff --name-only a314ecc chore/ak2-cx3 | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 편집기 진단 새 경고 0 — Given 고친 뒤, Then (a) markdownlint-cli2 0.23.2(`MD013` 끔 설정 `{ "config": { "MD013": false } }`)로 잰 경고 수가 `design-kit/skills/design-mockup/SKILL.md` 0 · `harness/evals/gate-exit-codes.md` 0 · `harness/references/contract-schema.md` ≤8 · `harness/agents/qa-evaluator.md` 0 · `harness/docs/guides/qa-evaluation-guide.md` 0 이고 (b) `shellcheck -f gcc ~/.claude/hooks/parallel-session-guard.sh` 출력 0 줄 (c) `python3 -m py_compile scripts/check-api-kit-docs.py` 종료 코드 0 [exact, enumerated]
  측정: scratch `mdlint/node_modules/.bin/markdownlint-cli2 --config mdlint/cfg.markdownlint-cli2.jsonc <파일> 2>&1 | grep -cE '^[^ ]+:[0-9]+'` 를 `design-kit/skills/design-mockup/SKILL.md` · `harness/evals/gate-exit-codes.md` · `harness/references/contract-schema.md` · `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md` 다섯에 하나씩 돌린다. 봉인 전 기준 0 · 0 · 8 · 0 · 0, shellcheck 0 줄
  양성 대조: 같은 명령이 contract-schema.md 에서 8 을 낸다(525 줄 MD060 등) — 세는 식이 경고를 잡는다
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh` 로 릴리스 스크립트만 돈다 — 이번 변경 파일과 교집합 0 개. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경은 문서 · 검사 스크립트 · 셸 훅이다. 훅의 실제 동작은 SC-02 ~ SC-04 · ER-01 이 잰다)
- [ ] DG-05: 로컬 CI 가 기준과 같게 통과한다 — Given 고친 뒤, When `TMPDIR=<scratch>/ci-cx3-after/tmp bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W` 를 돌리면, Then 요약의 모든 단계가 `rc=0` 이고 yq 없는 `feedback-agg-test` 만 `SKIP` 이다 [exact]
  측정: `<TMPDIR>/ci-local/summary.txt` 에서 `grep -vc 'rc=0'` 이 1 이고 그 한 줄이 `feedback-agg-test SKIP (yq 없음)`
