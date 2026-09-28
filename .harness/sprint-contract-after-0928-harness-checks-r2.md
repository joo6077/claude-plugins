---
feature: "harness 계약 규칙 · 검사 도구 약점 2 회차 (h1 — B1 · B2 · B3 · B4 · B7 · B8 · B9 · B22 · D2 · D4, 독립 검토 뒤 남은 자리 포함)"
slug: after-0928-harness-checks-r2
created: "2026-09-28 14:00"
complexity: "복잡"
conditions: 44
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:925cf12b1330ffe9
measurement_digest: sha256:ff2e15044cb81057
locked_at: "2026-09-28 14:09"
---

## 배경

- 1 회차 계약 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1/.harness/sprint-contract-after-0928-harness-checks.md` (봉인 `455c55aaa06642fa`, QA APPROVE 뒤 `status: superseded` · `superseded_by: after-0928-harness-checks-r2`, 커밋 `0fbb27d`). 이 계약이 그 새 판이다. 1 회차 QA 리포트는 커밋 `6228a0c` 에 그대로 남겼다.
- 1 회차 독립 검토가 막는 결함을 짚었다 — 계약 머리의 줄 끝 주석을 값으로 읽는 결함(B1)이 `harness/scripts/commit-guard.sh` 의 범위 검사 읽개 `val()` 에도 있어, `status: active   # …` 계약이면 커밋 범위 검사가 꺼진다. 고친 커밋 `76b6cc5` 가 `harness/scripts/commit-guard.sh` · `harness/evals/hooks/commit-guard-test.sh` 두 파일을 바꿨다.
- 1 회차에서 틀린 측정과 바로잡은 까닭 (조건의 뜻은 1 회차와 같다):
  - AR-05 — `.harness` 밖 바꿀 경로를 18 개로 못 박았다. 막는 결함을 고치려면 위 두 파일이 들어가야 하므로 20 개로 적는다. 목록을 넓히는 것은 느슨해지는 쪽이라 개정 파일이 아니라 새 판으로 다시 쓴다 (결정 파일 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md` 의 길).
  - DG-02 — 끝 줄 `files=18` 도 같은 목록을 센다. `files=20` 으로 적는다.
  - SC-01 — `REPO` 줄 `checked=3` 은 1 회차 계약 자신이 superseded 가 되면서 4 가 된다. `checked=4` 로 적는다.
  - 새 조건 — commit-guard 줄 끝 주석 시험(SC-14, 고치기 전 FAIL · 고친 뒤 PASS). 검토가 남긴 막지 않는 것 셋(B9 평가 파일 없는 킷 이름 알림 · B8 자료 절 고르기 · B3 스크립트 폴더 찾기 차례, SC-18 ~ SC-20)과 레포 밖 훅 `~/.claude/hooks/qa-pending-check.sh` 의 같은 결함(SC-15 ~ SC-17 · AR-07)을 이 판에서 함께 잰다.
- 사용자 위임: 2026-09-26T10:09:00.557Z · 10:30:16.222Z · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1` (가지 `chore/ak3-h1`, 시작 판 `95508d9`). 아래 모든 명령은 W 에서, `<W>` 자리에 이 절대경로를 넣어 돌린다.
- 측정 묶음 둘. M = `.harness/.meta/after-0928-harness-checks/` (1 회차 그대로, 커밋 `3686f92`): `m-a11y.sh 122c08cbc8bbe637` · `m-cause.sh 5aefaab98b0a0f2d` · `m-cilocal.sh e122eb1e69fc0f17` · `m-d4.sh 0801617955ff9ef2` · `m-diag.sh 08291bb42d36311f` · `m-docs.sh 958dad8b72e0e34a` · `m-evals.sh 1112f1a97ed09d4f` · `m-exit.sh e2958ad063a6e231` · `m-fm.sh ce143f0d2dcff488` · `m-helpers.sh 3faa29f90e73f542` · `m-phase.sh 56908fa40348449c` · `m-scope.sh a5b343e119307246` · `m-superseded.sh 3439a8de3d72f295` · `m-tests.sh fe763da2f2c9931d`. M2 = `.harness/.meta/after-0928-harness-checks-r2/` (이 판에서 새로): `m-evals-absent.sh 6ae0b0b177d8872c` · `m-guard.sh 2dbbbb11bb37527d` · `m-hookdiff.sh 2788790ceb2246b1` · `m-hs.sh b8a32921c2c2223a` · `m-phase-sec.sh 831f9dd8d189d87c` · `m-qapending-run.sh 95eb1ffcd1879e65` · `m-qapending.sh a52c15e4f631d064`. sha256 앞 16 자리다. 평가 전에 `shasum -a 256` 로 대조한다 — 다르면 그 파일을 부르는 조건은 FAIL.
- 모든 측정은 임시 폴더를 `mktemp -d "${TMPDIR:-/tmp}/…XXXXXX"` 로 만들고 끝나면 지운다. 레포 파일과 레포 밖 훅을 고치지 않는다 (읽기만).
- 브라우저가 필요한 측정(m-a11y · SC-07 · AR-03)은 W 에 `node_modules` 가 없으면 `NODE_PATH=/Users/jackson/Hub/10_Dev/claude-plugins/node_modules` 를 준다.
- 공통 전제 G: 조건에 「(커밋 뒤)」 가 붙은 것은 이 스프린트의 구현 커밋이 모두 `chore/ak3-h1` 에 들어간 뒤에 잰다. 그 밖의 조건은 작업 폴더 상태로 잰다. 레포 밖 훅 조건(SC-15 ~ SC-17 · AR-07)은 훅을 고친 뒤의 `~/.claude/hooks/qa-pending-check.sh` 를 잰다.

## 리서치 소스

- 바깥 근거가 필요한 항목이 없다. 모든 결함은 레포 파일 · 레포 밖 훅과 봉인 전 실측으로 확인했다.
- YAML 줄 끝 주석은 값 앞에 빈칸이 있어야 주석으로 읽힌다 — `abc#def` 는 값 그대로다 (YAML 1.2 §6.6 Comments, <https://yaml.org/spec/1.2.2/#66-comments>). SK-01 · SC-15 의 네 번째 입력이 이 규칙을 잰다.

## GAP 분석

- 1 회차 조건 28 개(기능)의 측정을 가지 끝(`3f9ebb6` 뒤 `0fbb27d`)에서 다시 돌렸다. AR-05 · DG-02 · SC-01 `REPO` 줄 말고는 1 회차 기대값과 글자까지 같다: `m-fm ng=0 total=42` · `m-docs` 세 절 모두 1 이상 · `fm_same=1 md_lines=17 html_lines=17` · `m-cause` 다섯 줄 · `m-exit rows=14 cite=14 only_rows=[] only_cite=[]` · `m-helpers current rc=0 pass_F=7 fail_F=0 swapped=0` · `m-tests` 세 쌍 · `m-phase` · `m-evals` 네 줄 · `m-cilocal` 다섯 줄 · `m-a11y` 여섯 줄(visual-styles `btn=63x48`) · 전체 쪽 `189/189 PASS` · AR-01 사라진 명령 0 · 새 명령 넷 · AR-06 셋.
- 바로잡은 측정의 두 판 값:
  - AR-05 `m-scope.sh <W> 95508d9 chore/ak3-h1` — 가지 끝 `changed=` 20 경로(아래 목록), `commits=<n> bad=0 dirty=0` (측정 묶음 커밋 `e6399c7` 뒤 실측 n=14 — 커밋이 더해질 때마다 늘어나므로 조건은 n ≥ 1 만 본다). 1 회차 기대 18 경로와 다르다(두 경로 많음).
  - DG-02 `m-diag.sh` — 가지 끝 `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=20`.
  - SC-01 `m-superseded.sh` — 가지 끝 `REPO rc=0 checked=4 violations=0 states=` (1 회차 판 `0fbb27d` 이전 `checked=3`).
  - SC-14 `m-guard.sh` — 시작 판 `6378948` (지시가 준 판): `guard 6378948 rc=1 fails=16 s24=FAIL s25=FAIL s26=FAIL`. 가지 시작 판 `95508d9`: `guard 95508d9 rc=1 fails=2 s24=FAIL s25=FAIL s26=PASS`. 가지 끝: `guard chore/ak3-h1 rc=0 fails=0 s24=PASS s25=PASS s26=PASS`. `95508d9..chore/ak3-h1` 에서 `commit-guard.sh` 를 바꾼 커밋은 `76b6cc5` 하나라, `95508d9` 판 훅이 곧 「구현을 되돌린 사본」 이다.
- B1 레포 밖 — `~/.claude/hooks/qa-pending-check.sh:52` `function value(line)` 이 따옴표 · 끝 빈칸만 벗긴다 (sha256 앞 16 자리 `bdf5f8cc581a32d7`, 고치기 전). 실측 `bash M2/m-qapending.sh ~/.claude/hooks/qa-pending-check.sh` → 1 · 2 · 6 · 7 이 NG, `ng=4 total=7`. 훅 통째로: `bash M2/m-qapending-run.sh ~/.claude/hooks/qa-pending-check.sh` → `plain rc=0 caught=1` · `cmt rc=0 caught=0` — 줄 끝 주석이 붙은 이 세션 계약의 QA 빠짐을 못 붙잡는다. 같은 규칙으로 고친 scratch 사본에서 두 측정이 `ng=0 total=7` · `cmt rc=0 caught=1` 로 바뀌는 것을 봉인 전 확인했다.
- B9 남은 자리 — `bash M2/m-evals-absent.sh <W> <판>`: `0bf2dad`(1 회차 구현 끝) 과 `95508d9` 에서 run · sync 모두 `absent=[]`, 가지 끝에서 둘 다 `absent=[planning-kit, reflect-kit, bambu-kit, onboarding-kit]` (`dd60755`).
- B8 남은 자리 — `bash M2/m-phase-sec.sh <W> <판>`: `0bf2dad` 에서 `mid s2=aaa-kit,infra-kit,reflect-kit s3=rust-kit bad_rc=0`, `95508d9` 에서 같은 s2 · s3 에 `bad_rc=1`(상한 17), 가지 끝에서 `same` · `mid` 모두 `s2=flutter-toolkit,rust-kit,bambu-kit s3=react-kit bad_rc=0` (`dd60755`).
- B3 남은 자리 — `bash M2/m-hs.sh <W> <판>`: `0bf2dad` 에서 bash · zsh 모두 `repo=0 plugin=127 market=127` · `feedback_repo_rel=2`, 가지 끝에서 모두 `repo=0 plugin=0 market=0` · `feedback_repo_rel=0` (`df5adaf`). `95508d9` 에는 Step 0.5 superseded 절이 없어 `STOP` 이다 — 비교 판은 `0bf2dad`.

## 범위 경계

- 이 계약이 고치는 것: 1 회차의 열 항목(B1 · B2 · B3 · B4 · B7 · B8 · B9 · B22 · D2 · D4)과 독립 검토 뒤 남은 자리(commit-guard 읽개 · B9 · B8 · B3 · 레포 밖 훅 읽개). 남은 일 목록의 다른 B · D 항목과 A · C 는 다른 묶음이거나 사람 몫이다.
- 봉인된 계약 · QA 리포트 · 개정 파일(`.harness/sprint-contract-*.md` · `sprint-feedback-*.md` · `sprint-amendments-*.md` 가운데 `95508d9` 에 이미 있는 것)은 고치지 않는다. 옛 로컬 CI 도구 파일도 그대로 둔다.
- 변경 허용 경로(.harness 밖)는 20 개이며 목록 원문은 AR-05 다. 1 회차 18 개에 `harness/evals/hooks/commit-guard-test.sh` · `harness/scripts/commit-guard.sh` 를 더했다.
- 레포 밖 예외: `~/.claude/hooks/qa-pending-check.sh` 한 파일, 그 안의 `value()` 함수만 고친다. 고치기 전에 원본을 `.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh` 로 복사해 커밋하고, 시험 `.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-value-test.sh` 를 둔다. `~/.claude/hooks/` 의 다른 파일은 고치지 않는다.
- `.harness/` 안에서 더하는 것: 이 계약 · 측정 묶음 M2 · notes `.harness/.meta/after-kaizen-0928/h1-notes.md` 보강 · 위 백업 폴더 · QA 산출물.
- 대응 쪽: 원본 `harness/references/contract-schema.md` 의 쪽은 `docs/harness/contract-schema.html` 하나다. `harness/agents/` · `harness/skills/` · `harness/scripts/` · `harness/evals/` 는 짝이 없다.
- 오라클 해소: SC-11 — 동작은 `--list` 실행 출력 두 벌로 판정하고, 글자 검사는 단계 목록을 손으로 적지 않았는지만 본다.
- 오라클 해소: AR-04 — 산출물이 결정 기록 글이라 글 검사가 맞다. 「들이지 않는다」 는 (4) 의 커밋 구간 파일 검사로 잰다.
- 커버리지 해소: SK-01 — `m-fm.sh` 가 읽개 세 파일을 직접 열어 함수를 뗀다. commit-guard 의 읽개는 SC-14, 레포 밖 훅의 읽개는 SC-15 가 잰다.
- 커버리지 해소: SC-04 — `m-cause.sh` 가 원문 `harness/skills/sprint/SKILL.md` 와 검사 `scripts/check-cause-table-copies.py` 를 사본으로 떠서 돌린다.
- 커버리지 해소: AR-02 — `m-exit.sh` 가 표 파일의 모든 행과 인용 파일 전체를 맞대고, 두 새 스크립트 이름은 같은 조건의 grep 식에 들어 있다.
- 커버리지 해소: AR-03 — `m-docs.sh` 가 쪽 `docs/harness/contract-schema.html` 을 열어 낱말 셋과 공통 스타일 링크를 세고 `fm_get` 을 맞댄다.
- 커버리지 해소: AR-05 — `m-scope.sh` 의 `changed=` 줄이 20 경로 전체를 한 번에 맞댄다 (`.harness` 는 제외 경로 표기).
- 커버리지 해소: SC-18 — `m-evals-absent.sh` 가 `scripts/run-evals.py` · `scripts/sync-evals.py` 두 파일을 모두 돌린다. SC-19 — `m-phase-sec.sh` 가 `scripts/spawn-kaizen-phase.sh` 를 두 사본에서 돈다. SC-20 — `m-hs.sh` 가 `harness/skills/sprint-contract/SKILL.md` 의 Step 0.5 덩어리와 Step 9 · 10 줄을 잰다.
- 커버리지 해소: SC-20 — `m-hs.sh` 가 세 환경을 모두 만들어 돈다: 레포(`harness/scripts/` 가 있는 W) · 임시 플러그인 폴더 · 임시 HOME 아래 `.claude/plugins/marketplaces/m/harness/scripts/` (마켓 설치본 모양).
- 커버리지 해소: AR-07 — (1) 이 `.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh` 를 `git show chore/ak3-h1:<경로>` 로 잰다. 검출기는 `chore/ak3-h1:` · `<W>/` 접두가 붙은 글자를 다른 토큰으로 본다.
- 오라클 해소: SC-13 — 로컬 CI 전체를 실제로 돌리고, grep 은 그 실행 출력에서 단계 이름을 찾을 뿐이다.
- 교차 진단 반영(1 회차 봉인 전): 서명 판정은 `Claude <이름> <noreply@anthropic.com>` 모양 한 줄(`m-scope.sh`)이다 — 이 판도 같은 파일을 쓴다.
- 조건 수: 기능 조건 36 개로 복잡 난이도 가이드 상한 20 을 넘는다. 1 회차와 같은 까닭(같은 CI 파일 · 종료 코드 표 · 계약 형식 문서를 나누면 부딪힌다)에, 새로 더한 여덟은 모두 1 회차 항목의 남은 자리라 따로 떼지 않는다 (사용자 위임 범위 안의 판단).
- 범위 목록 (커밋 직전 훅이 읽는다, AR-05 의 20 경로와 같다):

```text
# sprint-scope
.github/workflows/ci.yml
docs/design-kit/visual-styles.html
docs/harness/contract-schema.html
harness/agents/qa-evaluator.md
harness/evals/gate-exit-codes.md
harness/evals/hooks/commit-guard-test.sh
harness/evals/measure/measure-helpers-test.sh
harness/evals/superseded/check-superseded-test.sh
harness/references/contract-schema.md
harness/scripts/check-superseded.sh
harness/scripts/commit-guard.sh
harness/skills/sprint-contract/SKILL.md
scripts/check-cause-table-copies.py
scripts/check-docs-a11y.js
scripts/ci-local.sh
scripts/run-evals.py
scripts/spawn-kaizen-phase.sh
scripts/sync-evals.py
scripts/test-check-cause-table-copies.py
scripts/test-ci-local.sh
```

## 회귀 게이트

- 로컬 CI 전체 — SC-13 이 새 도구로 CI 파일의 모든 `run:` 단계를 돈다 (commit-guard 시험 단계 `Commit guard hook test` 포함).
- 봉인 전 가지 끝 값: 위 GAP 분석 첫 두 항목. 1 회차 봉인 전 기준값(`m-fm ng=24` 등)은 1 회차 계약에 있다.

## Skill

- [ ] SK-01: Given 계약 머리에 줄 끝 주석이 붙은 계약, When 머리 읽개 셋(`harness/agents/qa-evaluator.md` 의 `fm_get` · `harness/references/contract-schema.md` 의 `fm_get` · `harness/skills/sprint-contract/SKILL.md` 의 `read_fm`)이 bash 와 zsh 에서 값을 읽으면, Then 일곱 입력 모두 주석을 뺀 값을 낸다 — 1 `status: superseded   # 새 판 있음`→`superseded` · 2 `status: "active" # 주석`→`active` · 3 `status: active`→`active` · 4 `owner_session: abc#def`→`abc#def` · 5 `feature: "a # b"`→`a # b` · 6 `status: 'done'<탭># 탭 앞 주석`→`done` · 7 `status: active #`→`active` [exact, enumerated]
  측정: `bash M/m-fm.sh <W>` 끝 줄이 `ng=0 total=42` 이고 종료 코드 0. 세 함수의 첫 줄은 지금 모양(`fm_get() {` · `fm_get() { # fm_get <file> <key>` · `read_fm() {`)을 지킨다 — 못 떼면 `STOP` 과 종료 코드 2 로 FAIL.
  알려진 답: 1 회차 봉인 전 실측 `ng=24 total=42`, 가지 끝 `ng=0 total=42`.
- [ ] SK-02: Given 같은 일을 새 판 계약으로 다시 쓸 때, When sprint-contract SKILL.md Step 0.5 절을 읽으면, Then 옛 판에 `status: superseded` 와 `superseded_by: <새 슬러그>` 를 적는 절차, 조건 줄은 건드리지 않아 봉인이 그대로라는 설명, 적은 뒤 `check-superseded.sh` 를 돌려 종료 코드 0 을 확인하는 단계가 있다 [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `skill-0.5 status: superseded=` · `skill-0.5 superseded_by=` · `skill-0.5 check-superseded.sh=` 세 값이 모두 1 이상. 절 = `### 0.5. ` 줄부터 `### 1. ` 줄 앞까지. 1 회차 봉인 전 셋 다 0, 가지 끝 1 · 2 · 5.
- [ ] SK-03: sprint-contract SKILL.md `## Gotchas` 절에 계약 형식 문서 `§측정 관례` 를 가리키며 측정 명령 함정(`git log --format=%B` 끝 빈 줄)을 짚는 항목이 하나 이상 있다 [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `skill-gotchas 측정 관례=` 와 `skill-gotchas --format=%B=` 가 모두 1 이상. 1 회차 봉인 전 둘 다 0.
- [ ] SK-04: 계약 형식 문서 `#### 측정 관례` 절에 지난 계약 넷의 측정 결함을 다음 계약이 되풀이하지 않게 하는 규칙 다섯이 있다 — (1) 린트 끄기 주석을 읽는 측정은 `disable-next-line` · `disable-line` 과 구간 `disable` 을 가른다 (`meaning.py`) (2) 파일마다 차이를 셀 때 첫 차이 하나가 아니라 모두 낸다 (`meaning.py` SPACING) (3) 커밋 메시지 끝 줄을 `git log --format=%B | tail` 로 재지 않는다 — 끝 빈 줄 때문에 헛 FAIL 이 난다 (cx3 `AR-02`) (4) 기대 출력 글자는 봉인 전 실제 실행 출력에서 옮긴다 — 빈칸 수가 달라 헛 FAIL 이 난다 (dr1a `SC-01`) (5) 정렬은 `LC_ALL=C sort` 로 하고 로캘 없는 `sort -u` 를 쓰지 않는다 (k4 `DG-02`) [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `schema-측정관례` 일곱 줄(`disable-next-line` · `meaning.py` · `AR-02` · `SC-01` · `DG-02` · `--format=%B` · `sort -u`)이 모두 1 이상. 절 = `#### 측정 관례` 줄부터 다음 `#### ` 줄 앞까지. 1 회차 봉인 전 일곱 모두 0.
- [ ] SK-05: 계약 형식 문서가 `superseded_by` 규칙을 기계로 확인하는 명령으로 `harness/scripts/check-superseded.sh` 를 적는다 [exact]
  측정: `bash M/m-docs.sh <W>` 의 `schema-전체 harness/scripts/check-superseded.sh=` 가 1 이상. 1 회차 봉인 전 0.

## Script

- [ ] SC-01: Given 손으로 답을 아는 계약 폴더 둘과 W 의 `.harness`, When `bash harness/scripts/check-superseded.sh <폴더>` 를 돌리면, Then superseded 계약마다 `<상태> <경로>` 한 줄(상태는 `OK` · `MISSING_BY`(가리킴 없음) · `MISSING_TARGET`(가리킨 계약 없음) · `CHAIN`(가리킨 계약도 superseded))과 끝 줄 `checked=<N> violations=<V>` 를 내고, 위반이 있으면 1 · 없으면 0 으로 끝난다. 줄 끝 주석이 붙은 `status: superseded   # …` 도 superseded 로 센다 [exact, enumerated]
  측정: `bash M/m-superseded.sh <W>` 의 세 줄이 정확히 `A rc=1 checked=4 violations=3 states=a:OK,c:MISSING_BY,d:MISSING_TARGET,e:CHAIN` · `B rc=0 checked=1 violations=0 states=x:OK` · `REPO rc=0 checked=4 violations=0 states=` 이다 (REPO 의 넷은 `after-0926-kits-api-onboarding-howto` · `after-0926-kits-reflect-bambu-tone` · `after-0926-mdlint-l2` · `after-0928-harness-checks`, states 는 한 글자 슬러그만 뽑으므로 빈 값이 맞다).
  알려진 답: 폴더 A 는 superseded 넷(a · c · d · e) 가운데 a 만 옳다 — 손으로 셈. 가지 끝 실측이 위 세 줄과 같다.
- [ ] SC-02: superseded 확인 스크립트의 시험 `harness/evals/superseded/check-superseded-test.sh` 가 SC-01 의 폴더 A · B 와 같은 경우를 스스로 만들어 기대 출력과 맞대고 통과하면 0 으로 끝난다 [exact]
  측정: `bash M/m-tests.sh <W> 95508d9` 의 `superseded 그대로 rc=0 broken=0`.
  음성 대조: 같은 출력의 `superseded 망가뜨림` 줄 — 대상 스크립트를 늘 `checked=0 violations=0` 과 0 으로 끝나는 가짜로 바꾼 사본에서 `rc=` 가 0 이 아니고 `broken=1` (가지 끝 `rc=1 broken=1`).
- [ ] SC-03: 공용 측정 시험 `harness/evals/measure/measure-helpers-test.sh` 가 SK-01 의 일곱 입력을 계약 형식 문서의 `fm_get` 에 돌리는 확인 일곱을 `F1-` ~ `F7-` 이름으로 더하고 모두 통과한다 [exact, enumerated]
  측정: `bash M/m-helpers.sh <W> 95508d9` 의 첫 줄이 `current rc=0 pass_F=7 fail_F=0 swapped=0`.
  음성 대조: 같은 출력 둘째 줄 — 계약 형식 문서의 `fm_get` 만 판 `95508d9` 것으로 되돌린 사본에서 `old-fm_get rc=1 pass_F=3 fail_F=4 swapped=1`.
- [ ] SC-04: Given 판정 표 원문(`harness/skills/sprint/SKILL.md`), When 사본 검사 `scripts/check-cause-table-copies.py` 가 원문 덩어리를 뗄 때, Then 덩어리는 `| 공용 작업 폴더 |` 줄부터 사본 위치를 알리는 `판정 표와 두 경우는` 으로 시작하는 줄 바로 앞까지다 — 그 사이에 원문에만 더한 줄은 사본 둘을 모두 MISMATCH 로 만든다 [exact, enumerated]
  측정: `bash M/m-cause.sh <W>` 의 네 줄이 정확히 `a-unchanged rc=0 checked=2 violations=0 infra_errors=0 mismatch=0 applied=1` · `b-bullet-after-last rc=1 checked=2 violations=2 infra_errors=0 mismatch=2 applied=1` · `c-para-before-note rc=1 checked=2 violations=2 infra_errors=0 mismatch=2 applied=1` · `d-note-edited rc=0 checked=2 violations=0 infra_errors=0 mismatch=0 applied=1`. `applied=` 는 원문 사본에 바꿈이 실제로 들어갔는지다 — 0 이면 그 경우는 잰 것이 아니다.
  양성 대조: 1 회차 봉인 전 b · c 가 `rc=0 … mismatch=0 applied=1` 이었다 — 결함이 이 측정에 잡힌다.
- [ ] SC-05: 판정 표 사본 검사의 시험 `scripts/test-check-cause-table-copies.py` 가 SC-04 의 a · b · c · d 와 ER-03 의 e 다섯 경우를 임시 사본으로 돌려 기대 종료 코드와 맞대고 통과하면 0 으로 끝난다 [exact]
  측정: `bash M/m-tests.sh <W> 95508d9` 의 `cause 그대로 rc=0 broken=0`.
  음성 대조: `cause 망가뜨림` 줄 — 검사 스크립트를 판 `95508d9` 것으로 되돌린 사본에서 `rc=` 가 0 이 아니고 `broken=1`.
- [ ] SC-06: Given 테마 단추 id 가 `theme-btn` 이 아닌 `themeToggle` 인 쪽, When `node scripts/check-docs-a11y.js` 가 그 쪽을 재면, Then 단추 크기를 재어 `btn=<가로>x<세로>` 로 적고 44 미만이면 그 쪽을 FAIL 로 센다 [exact, enumerated]
  측정: `NODE_PATH=… bash M/m-a11y.sh <W>` 의 여섯 줄 — `color-palette.html OK btn=87x48` · `visual-styles.html OK btn=<가로>x<세로>` (둘 다 44 이상) · `korean-technical-writing.html OK btn=80x44` · `research-log.html OK btn=66x44` · `small-toggle.html FAIL btn=60x30` · `big-toggle.html OK btn=60x48` · 끝 줄 `rc=1` (small-toggle 때문).
  양성 대조: 1 회차 봉인 전 여섯 쪽 모두 `OK`, 앞 셋과 임시 둘이 `btn=none`, `rc=0` 이었다.
- [ ] SC-07: `docs/design-kit/visual-styles.html` 의 테마 단추가 375 너비에서 가로 · 세로 모두 44 이상이고, 문서 사이트 전체 접근성 검사가 모든 쪽을 통과한다 [exact]
  측정: SC-06 의 `visual-styles.html` 줄의 두 수가 모두 44 이상. 그리고 W 에서 `node scripts/check-docs-a11y.js` 의 끝 줄이 `<N>/<N> PASS` 이고 N 은 `find docs -name '*.html' | grep -c .` 와 같으며 종료 코드 0. 가지 끝 실측 `189/189 PASS` · 단추 63x48. 기본 작업 폴더가 아니라 W 에서 잰다.
- [ ] SC-08: Given 마켓 목록의 킷 수, When `bash scripts/spawn-kaizen-phase.sh <n>` 을 부르면, Then 받는 번호 상한은 4 + (harness 를 뺀 킷 수) 이고 킷 Phase 의 이름 · 슬러그는 마켓 목록 차례에서 뽑힌다 — 킷 이름 끝의 `-kit` · `-toolkit` 을 뗀 것이 슬러그 끝이다 [exact, enumerated]
  측정: `bash M/m-phase.sh <W>` 에서 (1) `same` 사본 n=1~17 의 슬러그가: `design-guides` · `contract` · `evaluator` · `harness` · `flutter` · `design` · `backend` · `infra` · `rust` · `react` · `planning` · `reflect` · `bambu` · `onboarding` · `tone` · `api` · `howto` (`kaizen-phase<n>-<이것>`, 모두 `rc=0`) (2) `same n=0` · `same n=18` · `same n=19` 가 `rc=1` (3) `foo` 사본 n=1~17 이 같은 슬러그 · `rc=0` 이고 `foo n=18 rc=0 slug=kaizen-phase18-foo` (4) `foo n=0` · `foo n=19` 가 `rc=1` (5) `same help_1_17=0` · `foo help_1_17=0`.
  알려진 답: 1 회차 봉인 전 `foo n=18 rc=1 slug=` · `help_1_17=1`. 가지 끝 실측이 (1)~(5) 와 같다.
- [ ] SC-09: Given 마켓 목록, When `python3 scripts/run-evals.py` 를 돌리면, Then 평가 대상은 마켓 목록의 킷 가운데 `evals/evals.json` 이 있는 것이고, 형식이 달라 빼는 킷은 `SKIP <킷> (<사유>)` 줄로 이유를 댄다 — 지금 빼는 것은 `howto-kit` 하나다 [exact, enumerated]
  측정: `bash M/m-evals.sh <W>` 의 `same run-evals` 줄이 `rc=0 kits=api-kit,backend-kit,design-kit,flutter-toolkit,harness,infra-kit,react-kit,rust-kit,tone-kit skip=howto-kit bar_missing=0 total=[Total: 122 passed, 0 failed]`, `foo run-evals` 줄이 `rc=0 kits=api-kit,backend-kit,design-kit,flutter-toolkit,foo-kit,harness,infra-kit,react-kit,rust-kit,tone-kit skip=howto-kit bar_missing=0 total=[Total: 123 passed, 0 failed]`.
  알려진 답: 1 회차 봉인 전 `foo` 줄에 `foo-kit` 없음 · `skip=` 비어 있음 · `122 passed`.
- [ ] SC-10: Given 마켓 목록, When `python3 scripts/sync-evals.py --check-only` 를 돌리면, Then 대상은 마켓 목록의 킷 가운데 `evals/evals.json` 이 있는 것이고 빼는 킷은 `SKIP <킷> (<사유>)` 줄로 이유를 댄다 — 지금 빼는 것은 `harness` · `howto-kit` 둘이다. 새 킷의 사례 없는 스킬은 MISSING 으로 잡혀 1 로 끝난다 [exact, enumerated]
  측정: `bash M/m-evals.sh <W>` 의 `same sync-evals` 줄이 `rc=0 kits=api-kit,backend-kit,design-kit,flutter-toolkit,infra-kit,react-kit,rust-kit,tone-kit skip=harness,howto-kit bar_missing=0 total=[Total: 0 added, 0 orphans, 0 missing (preview)]`, `foo sync-evals` 줄이 `rc=1 kits=api-kit,backend-kit,design-kit,flutter-toolkit,foo-kit,infra-kit,react-kit,rust-kit,tone-kit skip=harness,howto-kit bar_missing=1 total=[Total: 0 added, 0 orphans, 1 missing (preview)]`.
  알려진 답: 1 회차 봉인 전 `foo sync-evals rc=0 … bar_missing=0`.
- [ ] SC-11: Given CI 파일 `.github/workflows/ci.yml`, When `bash scripts/ci-local.sh --list <폴더>` 를 부르면, Then CI 파일에서 `run:` 을 가진 단계를 모두 읽어 한 줄씩 `RUN <job> <단계 이름>` 또는 `SKIP <job> <단계 이름> (<사유>)` 로 적고 끝 줄 `steps=<N> run=<R> skip=<S> unsupported=<U>` 를 낸다. SKIP 은 준비 단계 다섯(`Install Python dependencies` · `Install dependencies` · `Install Playwright browsers` · `Install zsh (셸 대조 시험용)` · `Install zsh (공용 측정 파일 시험용)`)뿐이다. 단계 목록을 스크립트 안에 손으로 적지 않는다 [exact, enumerated]
  측정: `bash M/m-cilocal.sh <W>` 의 `repo-list rc=0 last=[steps=40 run=35 skip=5 unsupported=0] yaml_steps=40 skip_names=[Install Playwright browsers|Install Python dependencies|Install dependencies|Install zsh (공용 측정 파일 시험용)|Install zsh (셸 대조 시험용)]` 와 `extra-list rc=0 last=[steps=41 run=36 skip=5 unsupported=0] extra_run=1`. 그리고 `grep -cE 'validate-plugin|check-docs-a11y|run-evals' scripts/ci-local.sh` 이 0.
  알려진 답: `yaml_steps` 는 1 회차 봉인 전 36, AR-01 의 네 단계를 더해 40.
- [ ] SC-12: Given 작은 CI 파일(통과 단계 `Good` · 7 로 끝나는 단계 `Bad`), When `bash scripts/ci-local.sh <폴더>` 로 실제로 돌리면, Then 단계마다 `PASS <job> <이름> rc=0` / `FAIL <job> <이름> rc=<n>` 한 줄, 끝 줄 `steps=2 run=2 skip=0 unsupported=0 failed=1`, 종료 코드 1 이다. 도구의 시험 `scripts/test-ci-local.sh` 가 이 경우와 SC-11 · ER-02 의 경우를 맞대고 통과한다 [exact]
  측정: `bash M/m-cilocal.sh <W>` 의 `two-run rc=1 last=[steps=2 run=2 skip=0 unsupported=0 failed=1] fail_line=1 pass_line=1`. 그리고 `bash M/m-tests.sh <W> 95508d9` 의 `cilocal 그대로 rc=0 broken=0`.
  음성 대조: `cilocal 망가뜨림` 줄 — 도구를 아무것도 안 하고 0 으로 끝나는 가짜로 바꾼 사본에서 `rc=` 가 0 이 아니고 `broken=1`.
- [ ] SC-13: (커밋 뒤) 새 로컬 CI 도구로 W 의 CI 전체를 돌리면 모든 단계가 통과한다 — 옛 도구가 빠뜨린 다섯 단계(`python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · bambu 시험 두 명령 · `bash harness/evals/measure/measure-helpers-test.sh`)와 AR-01 의 새 네 단계, commit-guard 시험 단계를 포함한다 [exact, enumerated]
  측정: `TMPDIR=<scratch 아래 폴더> bash scripts/ci-local.sh <W>` 의 끝 줄이 `steps=40 run=35 skip=5 unsupported=0 failed=0` 이고 종료 코드 0. 여섯 단계 이름이 각각 `PASS ` 로 시작하는 줄에 있다: `api-kit docs check` · `Docs drift mapping check` · `Cause table copy check` · `Bambu-kit gate fixtures · MakerWorld fetch test` · `Measure helpers test` · `Commit guard hook test` (`grep '^PASS ' | grep -cF '<이름>'` 이 1 이상). 봉인 전 가지 끝 실측 `steps=40 run=35 skip=5 unsupported=0 failed=0` · 종료 코드 0 · 여섯 이름 모두 1 이상.
- [ ] SC-14: Given 계약 머리 `status` · `owner_session` 값 뒤에 줄 끝 주석이 붙은 이 세션의 진행 중 계약(`status: active   # 진행 중` · `"active"<탭># 탭 뒤 주석` 과 `'S'`), When 커밋 직전 훅 `harness/scripts/commit-guard.sh` 가 범위 목록 밖 파일의 커밋을 재면, Then 계약을 살아 있는 것으로 읽어 그 커밋을 2 로 막는다. 값 가운데 `#`(`S#1`)은 주석이 아니라 값이다 [exact, enumerated]
  측정: `bash M2/m-guard.sh <W> chore/ak3-h1` 이 정확히 `guard chore/ak3-h1 rc=0 fails=0 s24=PASS s25=PASS s26=PASS` (가지 끝의 시험 `harness/evals/hooks/commit-guard-test.sh` 를 그 판의 훅에 돌린다). 봉인 전 실측이 이와 같다.
  음성 대조: 같은 시험을 구현 전 훅에 돌린 `bash M2/m-guard.sh <W> 95508d9` 가 정확히 `guard 95508d9 rc=1 fails=2 s24=FAIL s25=FAIL s26=PASS` — `val()` 만 되돌리면 s24 · s25 가 FAIL 한다. 지시가 준 시작 판 `6378948` 에서는 `guard 6378948 rc=1 fails=16 s24=FAIL s25=FAIL s26=FAIL` (그 판 훅은 다른 기능도 없다).
- [ ] SC-15: Given 줄 끝 주석이 붙은 계약 머리, When 레포 밖 훅 `~/.claude/hooks/qa-pending-check.sh` 의 머리 값 읽개 `value()` 가 읽으면, Then SK-01 의 일곱 입력(1 `status: superseded   # 새 판 있음`→`superseded` · 2 `status: "active" # 주석`→`active` · 3 `status: active`→`active` · 4 `owner_session: abc#def`→`abc#def` · 5 `feature: "a # b"`→`a # b` · 6 `status: 'done'<탭># 탭 앞 주석`→`done` · 7 `status: active #`→`active`) 모두 주석을 뺀 값을 낸다 [exact, enumerated]
  측정: `bash M2/m-qapending.sh /Users/jackson/.claude/hooks/qa-pending-check.sh` 끝 줄이 `ng=0 total=7` 이고 종료 코드 0. 함수 첫 줄은 `function value(line…) {` 모양을 지킨다 — 못 떼면 `STOP` 과 2 로 FAIL.
  알려진 답: 봉인 전 실측(고치기 전 훅) `ng=4 total=7`, NG 는 1 · 2 · 6 · 7.
  음성 대조: 고치기 전 사본 `.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh` 에 같은 측정을 돌리면 `ng=4 total=7` 과 종료 코드 1.
- [ ] SC-16: Given 머리 값 뒤에 줄 끝 주석이 붙은 이 세션 소유 진행 중 계약(QA 결과 파일 없음), When 레포 밖 훅 `~/.claude/hooks/qa-pending-check.sh` 를 통째로 돌리면, Then 주석 없는 계약과 똑같이 그 계약을 QA 빠짐으로 붙잡는다 [exact, enumerated]
  측정: `bash M2/m-qapending-run.sh /Users/jackson/.claude/hooks/qa-pending-check.sh` 의 두 줄이 정확히 `plain rc=0 caught=1` · `cmt rc=0 caught=1`.
  알려진 답: 봉인 전 실측(고치기 전 훅) `plain rc=0 caught=1` · `cmt rc=0 caught=0`.
  음성 대조: 고치기 전 사본 `.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh` 에 같은 측정을 돌리면 `cmt rc=0 caught=0`.
- [ ] SC-17: 레포 밖 훅 읽개의 시험 `.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-value-test.sh <훅 파일>` 이 SC-15 의 일곱 입력을 인자로 받은 훅의 `value()` 에 돌려 기대값과 맞대고, 모두 맞으면 0 · 아니면 0 이 아닌 값으로 끝난다 [exact]
  측정: `bash .harness/.meta/after-kaizen-0928/h1-backup/qa-pending-value-test.sh /Users/jackson/.claude/hooks/qa-pending-check.sh` 종료 코드 0.
  음성 대조: `bash .harness/.meta/after-kaizen-0928/h1-backup/qa-pending-value-test.sh .harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh` 종료 코드가 0 이 아니다 (고치기 전 사본).
- [ ] SC-18: Given 마켓 목록에 `evals/evals.json` 이 없는 킷, When `python3 scripts/run-evals.py` 와 `python3 scripts/sync-evals.py --check-only` 를 돌리면, Then 둘 다 그 킷들을 `없는 킷 <N> 개 — 대상 아님: <이름들>` 한 줄로 알린다 — 지금 그 킷은 `planning-kit` · `reflect-kit` · `bambu-kit` · `onboarding-kit` 넷이다 [exact, enumerated]
  측정: `bash M2/m-evals-absent.sh <W> chore/ak3-h1` 의 두 줄이 정확히 `run chore/ak3-h1 rc=0 absent=[planning-kit, reflect-kit, bambu-kit, onboarding-kit]` · `sync chore/ak3-h1 rc=0 absent=[planning-kit, reflect-kit, bambu-kit, onboarding-kit]`. 봉인 전 실측이 이와 같다.
  양성 대조: `bash M2/m-evals-absent.sh <W> 0bf2dad` 가 `run 0bf2dad rc=0 absent=[]` · `sync 0bf2dad rc=0 absent=[]` — 알림 없이 건너뛰던 판이 이 측정에 잡힌다.
- [ ] SC-19: Given 마켓 목록 중간(harness 바로 뒤)에 킷 하나가 끼어 Phase 번호가 밀린 경우, When `bash scripts/spawn-kaizen-phase.sh <n>` 이 Phase 마다 자료 절을 고르면, Then 자료 절 §2 는 `flutter-toolkit` · `rust-kit` · `bambu-kit`, §3 은 `react-kit` 이 받는다 — 번호가 아니라 킷 이름으로 고른다 [exact, enumerated]
  측정: `bash M2/m-phase-sec.sh <W> chore/ak3-h1` 의 두 줄이 정확히 `same s2=flutter-toolkit,rust-kit,bambu-kit s3=react-kit bad_rc=0` · `mid s2=flutter-toolkit,rust-kit,bambu-kit s3=react-kit bad_rc=0`. 봉인 전 실측이 이와 같다.
  알려진 답: `bash M2/m-phase-sec.sh <W> 0bf2dad` 의 `mid` 줄이 `mid s2=aaa-kit,infra-kit,reflect-kit s3=rust-kit bad_rc=0` — 끼운 킷 때문에 번호가 밀려 엉뚱한 킷이 절을 받는다 (손으로 셈: 5 aaa · 9 infra · 10 rust · 13 reflect).
- [ ] SC-20: Given harness 플러그인을 설치해 쓰는 다른 프로젝트(레포 상대 경로 `harness/scripts/` 가 없다), When sprint-contract SKILL.md Step 0.5 의 superseded 확인 부르기를 bash 와 zsh 로 돌리면, Then 레포 · 설치된 플러그인 폴더(`CLAUDE_PLUGIN_ROOT`) · 마켓 설치본(`~/.claude/plugins/marketplaces/…`) 세 환경 모두 스크립트를 찾아 0 으로 끝나고, Step 9 · 10 은 피드백 스크립트를 레포 상대 경로로 부르지 않는다 [exact, enumerated]
  측정: `bash M2/m-hs.sh <W> chore/ak3-h1` 의 세 줄이 정확히 `hs chore/ak3-h1 bash repo=0 plugin=0 market=0` · `hs chore/ak3-h1 zsh repo=0 plugin=0 market=0` · `hs chore/ak3-h1 feedback_repo_rel=0`. 봉인 전 실측이 이와 같다.
  양성 대조: `bash M2/m-hs.sh <W> 0bf2dad` 가 bash · zsh 모두 `repo=0 plugin=127 market=127` 과 `feedback_repo_rel=2` — 설치 환경에서 파일이 없어 127 로 끝나던 판이 이 측정에 잡힌다.

## Error

- [ ] ER-01: superseded 확인 스크립트에 없는 폴더를 주면 위반 0 으로 통과하지 않고 2 로 끝난다 [exact]
  측정: `bash M/m-superseded.sh <W>` 의 `MISSING rc=2` 로 시작하는 줄.
- [ ] ER-02: 로컬 CI 도구는 (a) CI 파일이 없는 폴더에서 2 로 끝나고 (b) `name` · `run` 밖의 열쇠(`working-directory` 등)가 있는 단계를 돌리지 않고 `UNSUPPORTED <job> <이름> (<사유>)` 로 알린 뒤 1 로 끝난다 [exact, enumerated]
  측정: `bash M/m-cilocal.sh <W>` 의 `none-list rc=2` 와 `wd-list rc=1 last=[steps=2 run=1 skip=0 unsupported=1] unsupported_line=1`.
- [ ] ER-03: 판정 표 사본 검사는 원문 덩어리의 끝 표지(`판정 표와 두 경우는` 으로 시작하는 줄)가 없으면 통과시키지 않고 `CANON_MISSING` 과 2 로 끝난다 [exact]
  측정: `bash M/m-cause.sh <W>` 의 `e-note-removed rc=2` 로 시작하고 `applied=0` 으로 끝나는 줄.
- [ ] ER-04: Phase 부트스트랩은 범위 밖 번호에서 태그를 만들기 전에 1 로 끝난다 [exact, enumerated]
  측정: SC-08 측정의 `same n=0` · `same n=18` · `same n=19` · `foo n=0` · `foo n=19` 다섯 줄이 `rc=1 slug=` (슬러그 빈 값).

## Architecture

- [ ] AR-01: CI 파일에 run 단계 넷이 더해지고 기존 36 단계의 명령은 그대로다 — 더하는 넷의 명령: `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `python3 scripts/test-check-cause-table-copies.py` · `bash scripts/test-ci-local.sh` [exact, enumerated]
  측정: `python3 -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[1])); [print(s["run"].strip()) for j in d["jobs"].values() for s in j["steps"] if "run" in s]' <파일>` 을 `git show 95508d9:.github/workflows/ci.yml` 과 W 의 파일에 각각 돌려 `LC_ALL=C sort` 후 `LC_ALL=C comm` — 사라진 명령 0 줄, 새 명령이 정확히 위 넷. 가지 끝 실측이 이와 같다.
- [ ] AR-02: 종료 코드 표 `harness/evals/gate-exit-codes.md` 에 새 스크립트 둘(`harness/scripts/check-superseded.sh` · `scripts/ci-local.sh`)의 행이 있고, 표의 행과 그 표를 인용하는 스크립트가 서로 빠짐없이 맞는다 [exact, enumerated]
  측정: `bash M/m-exit.sh <W>` 가 `rows=<k> cite=<k> only_rows=[] only_cite=[]` (두 k 가 같고 14 이상). 그리고 ``grep -cE '^\| `(harness/scripts/check-superseded.sh|scripts/ci-local.sh)` \|' harness/evals/gate-exit-codes.md`` 가 2. 가지 끝 실측 `rows=14 cite=14 only_rows=[] only_cite=[]`.
- [ ] AR-03: 대응 쪽 `docs/harness/contract-schema.html` 이 원본 변경을 싣는다 — `fm_get` 코드가 원본과 글자까지 같고, `check-superseded.sh` · `disable-next-line` · `meaning.py` 가 쪽에 있고, 공통 스타일 링크가 하나이며, 320 · 375 · 1280 너비 가로 넘침이 2 px 이하다 [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `html check-superseded.sh=` · `html disable-next-line=` · `html meaning.py=` 가 1 이상, `html assets/site.css=1`, 끝 줄이 `fm_same=1 md_lines=<k> html_lines=<k>` (두 k 가 같고 1 이상). 넘침은 `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` 줄의 `of=<320>/<375>/<768>/<1280>` 에서 첫째 · 둘째 · 넷째가 2 이하이고 줄이 `OK` 로 시작. 가지 끝 실측 `fm_same=1 md_lines=17 html_lines=17` · `of=0/0/0/0`.
  양성 대조: `fm_same` 은 원본만 고치고 쪽을 안 고치면 0 이 된다 (1 회차 봉인 전 확인).
- [ ] AR-04: D4 결정이 notes `.harness/.meta/after-kaizen-0928/h1-notes.md` 에 근거와 함께 있고, 변환 스크립트는 레포에 들이지 않는다 [exact, enumerated]
  측정: (1) notes 파일에 `D4` 와 `두지 않는다` 가 같은 줄에 있는 줄 1 개 이상 (2) notes 에 `same=6 total=21` 과 `m-d4.sh` 가 각각 1 번 이상 (3) notes 에 다시 만드는 길로 `docs-site` 와 `detect-docs-drift.py` 가 각각 1 번 이상 (4) (커밋 뒤) `git diff --name-only 95508d9 chore/ak3-h1 -- . ':(exclude).harness' | grep -cE '(^|/)(gen|pages|gen_yaml)\.py$|page\.css$'` 이 0.
- [ ] AR-05: (커밋 뒤) 이 가지가 `.harness` 밖에서 바꾼 경로가 정확히 아래 20 개이고, 커밋마다 맨 위 폴더가 하나 · 서명 줄이 하나이며, 커밋 안 된 `.harness` 밖 변경이 없다 — `.github/workflows/ci.yml` · `docs/design-kit/visual-styles.html` · `docs/harness/contract-schema.html` · `harness/agents/qa-evaluator.md` · `harness/evals/gate-exit-codes.md` · `harness/evals/hooks/commit-guard-test.sh` · `harness/evals/measure/measure-helpers-test.sh` · `harness/evals/superseded/check-superseded-test.sh` · `harness/references/contract-schema.md` · `harness/scripts/check-superseded.sh` · `harness/scripts/commit-guard.sh` · `harness/skills/sprint-contract/SKILL.md` · `scripts/check-cause-table-copies.py` · `scripts/check-docs-a11y.js` · `scripts/ci-local.sh` · `scripts/run-evals.py` · `scripts/spawn-kaizen-phase.sh` · `scripts/sync-evals.py` · `scripts/test-check-cause-table-copies.py` · `scripts/test-ci-local.sh` [exact, enumerated]
  측정: `bash M/m-scope.sh <W> 95508d9 chore/ak3-h1` — 상한은 가지 `chore/ak3-h1` 를 풀어 쓴다(HEAD 아님, 풀리지 않으면 `STOP` · 2 로 FAIL). 첫 줄 `changed=` 뒤가 위 20 경로를 글자 차례로 쉼표로 이은 것과 정확히 같고, 끝 줄이 `commits=<n> bad=0 dirty=0` (n ≥ 1). 서명 줄은 `%(trailers:key=Co-Authored-By,valueonly)` 로 잰다.
  알려진 답: 봉인 전 가지 끝 실측 `changed=` 가 위 20 경로와 같고 `commits=14 bad=0 dirty=0` (측정 묶음 커밋 `e6399c7` 뒤). n 은 봉인 커밋 · 백업 커밋 · notes 커밋이 더해질 때마다 늘어나므로 이 수와 다르다고 FAIL 이 아니다 — 판정은 조건문의 n ≥ 1 이다. 1 회차 기대 18 경로와는 `harness/evals/hooks/commit-guard-test.sh` · `harness/scripts/commit-guard.sh` 두 경로가 다르다.
- [ ] AR-06: (커밋 뒤) 옛 로컬 CI 도구와 봉인된 계약 · QA 리포트 · 개정 파일이 그대로이고, 새 도구는 레포에 추적된다 [exact, enumerated]
  측정: (1) `shasum -a 256 /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh | cut -c1-16` 이 `59fe55125c0dbc77` (2) `git -C <W> diff --name-only --diff-filter=MD 95508d9 chore/ak3-h1 -- '.harness/sprint-contract-*.md' '.harness/sprint-feedback-*.md' '.harness/sprint-amendments-*.md' | grep -c .` 이 0 (3) `git -C <W> ls-files --error-unmatch scripts/ci-local.sh` 종료 코드 0. 가지 끝 실측 셋 다 맞다 (1 회차 계약은 `95508d9` 뒤에 생겨 (2) 의 대상이 아니다).
  양성 대조: (2) 의 명령을 `fb5374b~1 fb5374b` 구간에 돌리면 1 — 계약 수정이 잡힌다 (1 회차 봉인 전 실측).
- [ ] AR-07: (커밋 뒤) 레포 밖 훅의 고치기 전 원본이 `.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh` 로 `chore/ak3-h1` 에 커밋돼 있고, 지금 훅은 `value()` 함수 밖을 바꾸지 않았으며 문법이 맞다 [exact, enumerated]
  측정: (1) `git -C <W> show chore/ak3-h1:.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh | shasum -a 256 | cut -c1-16` 이 `bdf5f8cc581a32d7` (봉인 전 실측한 고치기 전 훅의 값) (2) `git -C <W> ls-files --error-unmatch .harness/.meta/after-kaizen-0928/h1-backup/qa-pending-value-test.sh` 종료 코드 0 (3) `bash M2/m-hookdiff.sh <W>/.harness/.meta/after-kaizen-0928/h1-backup/qa-pending-check.sh /Users/jackson/.claude/hooks/qa-pending-check.sh` 가 정확히 `outside_diff=0 fn=1 syntax=0` (4) `shasum -a 256 /Users/jackson/.claude/hooks/qa-pending-check.sh | cut -c1-16` 이 `bdf5f8cc581a32d7` 가 아니다.
  양성 대조: (3) 은 고친 scratch 사본 끝에 한 줄을 더하면 `outside_diff=2` 가 된다 — 함수 밖 변경이 잡힌다 (봉인 전 실측).

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 (고치는 SKILL.md · 계약 형식 문서 · qa-evaluator.md 에 코드 블록이 있다)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지. 측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0 (sprint-contract SKILL.md · qa-evaluator.md 를 고친다)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — superseded 확인은 폴더를 인자로 받는 독립 스크립트이고 로컬 CI 도구는 폴더를 인자로 받는다. 측정: SC-01 · SC-11 이 임시 폴더 인자로 돈다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — superseded 확인은 머리 값을 공용 측정 파일의 `fm_get` 으로 읽고 자기 읽개를 새로 두지 않는다. 측정: `grep -cE '^[[:space:]]*(fm_get|read_fm)\(\)' harness/scripts/check-superseded.sh` 이 0 이고 `grep -c 'measure-common.sh' harness/scripts/check-superseded.sh` 가 1 이상

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: (커밋 뒤) `git diff --name-only 95508d9 chore/ak3-h1 | grep -c '^scripts/release.sh$'` 이 0. 실제 오라클은 DG-02 · SC-13)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude 는 빈 목록) — 이번에 바꾸거나 더한 `.md` 의 더한 줄에 markdownlint 경고 0 · `.sh` 새 파일 전체와 고친 파일의 더한 줄에 shellcheck 경고 0 · `.py` 컴파일 실패 0 · `.js` 문법 실패 0, 그리고 레포 밖 훅 `~/.claude/hooks/qa-pending-check.sh` 에 shellcheck 경고 0. 측정: `bash M/m-diag.sh <W> 95508d9 /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl` 끝 줄이 정확히 `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=20` (files 는 AR-05 의 20 경로) 이고 `shellcheck /Users/jackson/.claude/hooks/qa-pending-check.sh` 종료 코드 0. markdownlint-cli2 0.23.2 · MD013 끔. 봉인 전 가지 끝 실측 `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=20` · 훅 shellcheck 0. 양성 대조: 1 회차 봉인 전 md 한 줄 · sh 한 줄 · 깨진 py 한 파일을 넣어 `md_new=1 sh_new=2 py_bad=1` 로 잡힘을 확인했다
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` 로 릴리스 스크립트만 돈다 — 이번 변경 파일과 교집합 0 개. 실제 오라클은 SC-13 의 로컬 CI 전체)
- [ ] DG-04: N/A (산출물에 구동할 앱 · 서버가 없다 — 변경은 문서 · 검사 스크립트 · CI 파일 · 문서 쪽 · 레포 밖 셸 훅. 실제 오라클은 SC-13 · SC-07 의 브라우저 측정 · SC-16 의 훅 통째 실행)

사용자가 할 일: 없음
