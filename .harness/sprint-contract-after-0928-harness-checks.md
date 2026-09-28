---
feature: "harness 계약 규칙 · 검사 도구 약점 (남은 일 3 차 h1 — B1 · B2 · B3 · B4 · B7 · B8 · B9 · B22 · D2 · D4)"
slug: after-0928-harness-checks
created: "2026-09-28 10:49"
complexity: "복잡"
conditions: 36
status: superseded
superseded_by: after-0928-harness-checks-r2
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:455c55aaa06642fa
measurement_digest: sha256:d6e75fb37b35d6bd
locked_at: "2026-09-28 10:58"
---

## 배경

- 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/remaining.md` 의 B1 · B2 · B3 · B4 · B7 · B8 · B9 · B22 · D2 · D4 를 한 묶음으로 처리한다. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1` (가지 `chore/ak3-h1`, 시작 판 `95508d9`). 아래 모든 명령은 W 에서, `<W>` 자리에 이 절대경로를 넣어 돌린다.
- 측정 묶음은 `.harness/.meta/after-0928-harness-checks/` (아래 M) 에 있다. 조건이 부르는 파일과 sha256 앞 16 자리: `m-a11y.sh 122c08cbc8bbe637` · `m-cause.sh 5aefaab98b0a0f2d` · `m-cilocal.sh e122eb1e69fc0f17` · `m-d4.sh 0801617955ff9ef2` · `m-diag.sh 08291bb42d36311f` · `m-docs.sh 958dad8b72e0e34a` · `m-evals.sh 1112f1a97ed09d4f` · `m-exit.sh e2958ad063a6e231` · `m-fm.sh ce143f0d2dcff488` · `m-helpers.sh 3faa29f90e73f542` · `m-phase.sh 56908fa40348449c` · `m-scope.sh a5b343e119307246` · `m-superseded.sh 3439a8de3d72f295` · `m-tests.sh fe763da2f2c9931d`. 평가 전에 `shasum -a 256` 로 대조한다 — 다르면 그 조건은 FAIL.
- 모든 측정은 임시 폴더를 `mktemp -d "${TMPDIR:-/tmp}/…XXXXXX"` 로 만들고 끝나면 지운다. 레포 파일을 고치지 않는다 (m-scope · m-diag 는 읽기만).
- 브라우저가 필요한 측정(m-a11y · SC-07 · AR-03)은 W 에 `node_modules` 가 없으면 `NODE_PATH=/Users/jackson/Hub/10_Dev/claude-plugins/node_modules` 를 준다.
- 공통 전제 G: 조건에 「(커밋 뒤)」 가 붙은 것은 이 스프린트의 구현 커밋이 모두 `chore/ak3-h1` 에 들어간 뒤에 잰다. 그 밖의 조건은 작업 폴더 상태로 잰다.

## 리서치 소스

- 바깥 근거가 필요한 항목이 없다. 모든 결함은 레포 파일과 봉인 전 실측으로 확인했다 (아래 GAP 분석).
- YAML 줄 끝 주석은 값 앞에 빈칸이 있어야 주석으로 읽힌다 — `abc#def` 는 값 그대로다 (YAML 1.2 §6.6 Comments, <https://yaml.org/spec/1.2.2/#66-comments>). SK-01 의 네 번째 입력이 이 규칙을 잰다.

## GAP 분석

- B1 — 머리 읽개 셋(`harness/agents/qa-evaluator.md:235` `fm_get` · `harness/references/contract-schema.md:242` `fm_get` · `harness/skills/sprint-contract/SKILL.md:281` `read_fm`)이 줄 끝 주석을 값으로 읽는다. 실측 `bash M/m-fm.sh <W>` → `ng=24 total=42`, 틀린 경우 1 · 2 · 6 · 7 (주석 · 따옴표 뒤 주석 · 탭 뒤 주석 · 빈 주석). 공용 측정 파일 `harness/scripts/measure-common.sh` 는 계약 형식 문서의 `fm_get` 을 떼어 쓰므로 거기서 고치면 따라온다.
- B2 — `superseded_by` 를 기계로 보는 곳 0 곳. W 의 `.harness` 에 superseded 계약 셋(`after-0926-kits-api-onboarding-howto` · `after-0926-kits-reflect-bambu-tone` · `after-0926-mdlint-l2`)이 있고 셋 다 가리킨 새 판이 있으며 새 판은 `done` 이다 (봉인 전 손으로 확인).
- B3 — sprint-contract SKILL.md Step 0.5 절(`### 0.5.` ~ `### 1.`)에 `superseded` 낱말 0 건 (`bash M/m-docs.sh <W>` 의 `skill-0.5` 줄).
- B4 — `scripts/check-cause-table-copies.py:12` `BLOCK_END = "- **미확정**"`. 원문에 줄을 더한 사본 셋(b · c · d)에서도 모두 `rc=0` (`bash M/m-cause.sh <W>`).
- B7 — `scripts/check-docs-a11y.js:133` 이 `theme-btn` 만 찾는다. 테마 단추 id 가 `themeToggle` 인 쪽 셋(`docs/design-kit/color-palette.html` · `docs/design-kit/visual-styles.html` · `docs/tone-kit/korean-technical-writing.html`)이 `btn=none`. 따로 잰 실제 크기 87x48 · 63x33 · 80x44 — visual-styles 만 44 미만이다. 전체 쪽 실측 `189/189 PASS`.
- B8 — `scripts/spawn-kaizen-phase.sh:71` 상한 `17` 손 적기, 도움말 `1 ~ 17`. 마켓 목록에 킷 하나를 더한 사본에서도 `n=18 rc=1` (`bash M/m-phase.sh <W>`).
- B9 — `scripts/run-evals.py:32` · `scripts/sync-evals.py:32` 손 목록. `howto-kit/evals/evals.json` 은 있지만 두 목록 모두에 없다 — 그 파일은 게이트 픽스처 형식이라 run-evals 로 돌리면 16 건 FAIL 이고 CI 는 `sh howto-kit/evals/run-evals.sh` 로 따로 돈다. sync-evals 는 `harness` 도 뺀다 — 넣으면 `sprint` · `refactor-checklist` 두 스킬이 사례 없음으로 나온다. 새 킷을 더한 사본에서 두 스크립트 모두 그 킷을 모른다 (`bash M/m-evals.sh <W>`).
- B22 — 계약 형식 문서 `#### 측정 관례` 절(44 줄)에 `disable-next-line` · `meaning.py` · `AR-02` · `SC-01` · `DG-02` · `--format=%B` · `sort -u` 모두 0 건. SKILL.md Gotchas 절에 `측정 관례` · `--format=%B` 0 건.
- D2 — 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` (sha256 앞 16 자리 `59fe55125c0dbc77`) 는 레포 밖 · 추적 안 됨이고, CI 파일 `run:` 단계 36 개 가운데 26 개만 손으로 적어 다섯 단계(`check-api-kit-docs.py` · `detect-docs-drift.py --check-table` · `check-cause-table-copies.py` · bambu 시험 두 명령 한 단계 · `measure-helpers-test.sh`)를 안 돌린다. 나머지 다섯은 준비 단계(`pip install pyyaml` · `npm ci` · `npx playwright install --with-deps chromium` · zsh 설치 둘)다.
- D4 — 변환 스크립트 두 벌(`dcb/gen` · `dr2/gen`, 세션 scratch)을 판 `95508d9` 원본에 다시 돌린 결과 `same=6 total=21` (`bash M/m-d4.sh <W> 95508d9 <scratch>/dcb/gen <scratch>/dr2/gen`, scratch = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`). 나머지 15 쪽은 뒤에 원본이 바뀌었거나(코드 울타리 언어 표기) 스크립트가 원본의 `<!-- markdownlint-disable … -->` 주석을 본문 글로 옮기는 결함(`docs/tone-kit/locale-korean.html` 차이 2 줄)이 드러났다. 그래서 이 계약은 「레포에 두지 않는다」 로 정하고 근거를 notes 에 남기게 한다 — 쪽을 다시 만드는 길은 docs-site 스킬과 `detect-docs-drift.py` 다.
- 종료 코드 표 `harness/evals/gate-exit-codes.md` 는 지금 행 12 · 인용 스크립트 12 로 맞다 (`bash M/m-exit.sh <W>` → `rows=12 cite=12 only_rows=[] only_cite=[]`, 인용만 하는 가짜 파일을 넣으면 `only_cite=[scripts/zz-probe.sh]` 로 잡힘을 봉인 전 확인).

## 범위 경계

- 이 계약이 고치는 것: 위 GAP 의 열 항목. 남은 일 목록의 다른 B · D 항목(B5 · B6 · B10~B21 · D1 · D3 · D5~D8)과 A · C 는 다른 묶음이거나 사람 몫이다.
- 봉인된 계약 · QA 리포트 · 개정 파일(`.harness/sprint-contract-*.md` · `sprint-feedback-*.md` · `sprint-amendments-*.md` 가운데 `95508d9` 에 이미 있는 것)은 고치지 않는다. 옛 로컬 CI 도구 파일도 그대로 둔다 — 그 경로를 적은 봉인 계약이 있다.
- 변경 허용 경로(.harness 밖)는 18 개이며 정본 목록은 AR-05 다. 새 파일은 그 가운데 다섯(`harness/scripts/check-superseded.sh` · `harness/evals/superseded/check-superseded-test.sh` · `scripts/ci-local.sh` · `scripts/test-ci-local.sh` · `scripts/test-check-cause-table-copies.py`)이다.
- `.harness/` 안에서 더하는 것: 이 계약 · 측정 묶음 `.harness/.meta/after-0928-harness-checks/` · notes `.harness/.meta/after-kaizen-0928/h1-notes.md` · QA 산출물.
- 대응 쪽: 원본 `harness/references/contract-schema.md` 의 쪽은 `docs/harness/contract-schema.html` 하나다 (`scripts/detect-docs-drift.py` 의 `harness/references/` → `docs/harness/` 짝). `harness/agents/` · `harness/skills/` 는 짝이 없다.
- 오라클 해소: SC-11 — 동작은 `--list` 실행 출력 두 벌(레포 CI 파일 · 단계를 더한 사본)로 판정하고, 글자 검사는 단계 목록을 손으로 적지 않았는지만 본다.
- 오라클 해소: AR-04 — 산출물이 결정 기록 글이라 글 검사가 맞다. 「들이지 않는다」 는 (4) 의 커밋 구간 파일 검사로 잰다.
- 커버리지 해소: SK-01 — `m-fm.sh` 가 읽개 세 파일(`harness/agents/qa-evaluator.md` · `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md`)을 직접 열어 함수를 뗀다.
- 커버리지 해소: SC-04 — `m-cause.sh` 가 원문 `harness/skills/sprint/SKILL.md` 와 검사 `scripts/check-cause-table-copies.py` 를 사본으로 떠서 돌린다.
- 커버리지 해소: AR-02 — `m-exit.sh` 가 표 파일 `harness/evals/gate-exit-codes.md` 의 모든 행과 인용 파일 전체를 맞대고, 두 새 스크립트 이름은 같은 조건의 grep 식에 들어 있다.
- 커버리지 해소: AR-03 — `m-docs.sh` 가 쪽 `docs/harness/contract-schema.html` 을 열어 낱말 셋과 공통 스타일 링크를 세고 `fm_get` 을 맞댄다.
- 커버리지 해소: AR-05 — `m-scope.sh` 의 `changed=` 줄이 18 경로 전체를 한 번에 맞댄다 (`.harness` 는 제외 경로 표기).
- 교차 진단 반영(봉인 전): `m-scope.sh` 가 서명 줄을 특정 모델 이름 한 벌과 맞대고 있어, 모델이 바뀌면 구현이 옳아도 AR-05 가 늘 FAIL 한다는 지적을 받았다. 서명 판정을 `Claude <이름> <noreply@anthropic.com>` 모양 한 줄(`grep -cxE 'Claude [^<>]+ <noreply@anthropic\.com>'`)로 바꿨다. 임시 저장소 실측 — 지금 모델 서명 1 · 다른 모델 서명 1 · 사람 서명 0 · 서명 두 줄 2.
- 조건 수: 기능 조건 28 개로 복잡 난이도 가이드 상한 20 을 넘는다. 열 항목이 모두 harness 검사 도구 약점이라 한 묶음으로 간다 — 나누면 같은 CI 파일 · 종료 코드 표 · 계약 형식 문서를 두 가지에서 따로 고쳐 서로 부딪힌다 (사용자 위임 범위 안의 판단).
- 범위 목록 (커밋 직전 훅이 읽는다, AR-05 의 18 경로와 같다):

```text
# sprint-scope
.github/workflows/ci.yml
docs/design-kit/visual-styles.html
docs/harness/contract-schema.html
harness/agents/qa-evaluator.md
harness/evals/gate-exit-codes.md
harness/evals/measure/measure-helpers-test.sh
harness/evals/superseded/check-superseded-test.sh
harness/references/contract-schema.md
harness/scripts/check-superseded.sh
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

- 로컬 CI 전체 — SC-13 이 새 도구로 CI 파일의 모든 `run:` 단계를 돈다 (옛 도구가 빠뜨린 다섯 단계 포함).
- 봉인 전 기준값: `m-fm ng=24` · `m-cause` 다섯 경우 모두 `rc=0` · `m-phase same n=18 rc=1` · `m-evals` 두 사본 모두 foo-kit 0 · 전체 쪽 접근성 `189/189 PASS` · `m-exit rows=12 cite=12` · 공용 측정 시험 `rc=0 pass_F=0`.

## Skill

- [ ] SK-01: Given 계약 머리에 줄 끝 주석이 붙은 계약, When 머리 읽개 셋(`harness/agents/qa-evaluator.md` 의 `fm_get` · `harness/references/contract-schema.md` 의 `fm_get` · `harness/skills/sprint-contract/SKILL.md` 의 `read_fm`)이 bash 와 zsh 에서 값을 읽으면, Then 일곱 입력 모두 주석을 뺀 값을 낸다 — 1 `status: superseded   # 새 판 있음`→`superseded` · 2 `status: "active" # 주석`→`active` · 3 `status: active`→`active` · 4 `owner_session: abc#def`→`abc#def` · 5 `feature: "a # b"`→`a # b` · 6 `status: 'done'<탭># 탭 앞 주석`→`done` · 7 `status: active #`→`active` [exact, enumerated]
  측정: `bash M/m-fm.sh <W>` 끝 줄이 `ng=0 total=42` 이고 종료 코드 0. 세 함수의 첫 줄은 지금 모양(`fm_get() {` · `fm_get() { # fm_get <file> <key>` · `read_fm() {`)을 지킨다 — 못 떼면 `STOP` 과 종료 코드 2 로 FAIL.
  알려진 답: 봉인 전 실측 `ng=24 total=42` (경우 1 · 2 · 6 · 7 이 읽개 셋 × 셸 둘에서 틀림).
- [ ] SK-02: Given 같은 일을 새 판 계약으로 다시 쓸 때, When sprint-contract SKILL.md Step 0.5 절을 읽으면, Then 옛 판에 `status: superseded` 와 `superseded_by: <새 슬러그>` 를 적는 절차, 조건 줄은 건드리지 않아 봉인이 그대로라는 설명, 적은 뒤 `harness/scripts/check-superseded.sh` 를 돌려 종료 코드 0 을 확인하는 단계가 있다 [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `skill-0.5 status: superseded=` · `skill-0.5 superseded_by=` · `skill-0.5 check-superseded.sh=` 세 값이 모두 1 이상. 절 = `### 0.5. ` 줄부터 `### 1. ` 줄 앞까지. 봉인 전 셋 다 0.
- [ ] SK-03: sprint-contract SKILL.md `## Gotchas` 절에 계약 형식 문서 `§측정 관례` 를 가리키며 측정 명령 함정(`git log --format=%B` 끝 빈 줄)을 짚는 항목이 하나 이상 있다 [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `skill-gotchas 측정 관례=` 와 `skill-gotchas --format=%B=` 가 모두 1 이상. 봉인 전 둘 다 0.
- [ ] SK-04: 계약 형식 문서 `#### 측정 관례` 절에 지난 계약 넷의 측정 결함을 다음 계약이 되풀이하지 않게 하는 규칙 다섯이 있다 — (1) 린트 끄기 주석을 읽는 측정은 `disable-next-line` · `disable-line` 과 구간 `disable` 을 가른다 (`meaning.py`) (2) 파일마다 차이를 셀 때 첫 차이 하나가 아니라 모두 낸다 (`meaning.py` SPACING) (3) 커밋 메시지 끝 줄을 `git log --format=%B | tail` 로 재지 않는다 — 끝 빈 줄 때문에 헛 FAIL 이 난다 (cx3 `AR-02`) (4) 기대 출력 글자는 봉인 전 실제 실행 출력에서 옮긴다 — 빈칸 수가 달라 헛 FAIL 이 난다 (dr1a `SC-01`) (5) 정렬은 `LC_ALL=C sort` 로 하고 로캘 없는 `sort -u` 를 쓰지 않는다 (k4 `DG-02`) [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `schema-측정관례` 일곱 줄(`disable-next-line` · `meaning.py` · `AR-02` · `SC-01` · `DG-02` · `--format=%B` · `sort -u`)이 모두 1 이상. 절 = `#### 측정 관례` 줄부터 다음 `#### ` 줄 앞까지. 봉인 전 일곱 모두 0.
- [ ] SK-05: 계약 형식 문서가 `superseded_by` 규칙을 기계로 확인하는 명령으로 `harness/scripts/check-superseded.sh` 를 적는다 [exact]
  측정: `bash M/m-docs.sh <W>` 의 `schema-전체 harness/scripts/check-superseded.sh=` 가 1 이상. 봉인 전 0.

## Script

- [ ] SC-01: Given 손으로 답을 아는 계약 폴더 둘과 W 의 `.harness`, When `bash harness/scripts/check-superseded.sh <폴더>` 를 돌리면, Then superseded 계약마다 `<상태> <경로>` 한 줄(상태는 `OK` · `MISSING_BY`(가리킴 없음) · `MISSING_TARGET`(가리킨 계약 없음) · `CHAIN`(가리킨 계약도 superseded))과 끝 줄 `checked=<N> violations=<V>` 를 내고, 위반이 있으면 1 · 없으면 0 으로 끝난다. 줄 끝 주석이 붙은 `status: superseded   # …` 도 superseded 로 센다 [exact, enumerated]
  측정: `bash M/m-superseded.sh <W>` 의 세 줄이 정확히 `A rc=1 checked=4 violations=3 states=a:OK,c:MISSING_BY,d:MISSING_TARGET,e:CHAIN` · `B rc=0 checked=1 violations=0 states=x:OK` · `REPO rc=0 checked=3 violations=0 states=` 이다 (REPO 의 states 는 m-superseded 가 한 글자 슬러그만 뽑으므로 빈 값이 맞다).
  알려진 답: 폴더 A 는 superseded 넷(a · c · d · e) 가운데 a 만 옳다 — 손으로 셈. 봉인 전 스크립트가 없어 네 줄 모두 `rc=127`.
- [ ] SC-02: superseded 확인 스크립트의 시험 `harness/evals/superseded/check-superseded-test.sh` 가 SC-01 의 폴더 A · B 와 같은 경우를 스스로 만들어 기대 출력과 맞대고 통과하면 0 으로 끝난다 [exact]
  측정: `bash M/m-tests.sh <W> 95508d9` 의 `superseded 그대로 rc=0 broken=0`.
  음성 대조: 같은 출력의 `superseded 망가뜨림` 줄 — 대상 스크립트를 늘 `checked=0 violations=0` 과 0 으로 끝나는 가짜로 바꾼 사본에서 `rc=` 가 0 이 아니고 `broken=1`.
- [ ] SC-03: 공용 측정 시험 `harness/evals/measure/measure-helpers-test.sh` 가 SK-01 의 일곱 입력을 계약 형식 문서의 `fm_get` 에 돌리는 확인 일곱을 `F1-` ~ `F7-` 이름으로 더하고 모두 통과한다 [exact, enumerated]
  측정: `bash M/m-helpers.sh <W> 95508d9` 의 첫 줄이 `current rc=0 pass_F=7 fail_F=0 swapped=0`.
  음성 대조: 같은 출력 둘째 줄 — 계약 형식 문서의 `fm_get` 만 판 `95508d9` 것으로 되돌린 사본에서 `old-fm_get rc=1 pass_F=3 fail_F=4 swapped=1`. 봉인 전 두 줄 모두 `pass_F=0 fail_F=0` (확인 일곱이 아직 없음).
- [ ] SC-04: Given 판정 표 원문(`harness/skills/sprint/SKILL.md`), When 사본 검사 `scripts/check-cause-table-copies.py` 가 원문 덩어리를 뗄 때, Then 덩어리는 `| 공용 작업 폴더 |` 줄부터 사본 위치를 알리는 `판정 표와 두 경우는` 으로 시작하는 줄 바로 앞까지다 — 그 사이에 원문에만 더한 줄은 사본 둘을 모두 MISMATCH 로 만든다 [exact, enumerated]
  측정: `bash M/m-cause.sh <W>` 의 네 줄이 정확히 `a-unchanged rc=0 checked=2 violations=0 infra_errors=0 mismatch=0 applied=1` · `b-bullet-after-last rc=1 checked=2 violations=2 infra_errors=0 mismatch=2 applied=1` · `c-para-before-note rc=1 checked=2 violations=2 infra_errors=0 mismatch=2 applied=1` · `d-note-edited rc=0 checked=2 violations=0 infra_errors=0 mismatch=0 applied=1`. `applied=` 는 원문 사본에 바꿈이 실제로 들어갔는지다 — 0 이면 그 경우는 잰 것이 아니다.
  양성 대조: 봉인 전 b · c 가 `rc=0 … mismatch=0 applied=1` 이다 — 결함이 지금 측정에 잡힌다.
- [ ] SC-05: 판정 표 사본 검사의 시험 `scripts/test-check-cause-table-copies.py` 가 SC-04 의 a · b · c · d 와 ER-03 의 e 다섯 경우를 임시 사본으로 돌려 기대 종료 코드와 맞대고 통과하면 0 으로 끝난다 [exact]
  측정: `bash M/m-tests.sh <W> 95508d9` 의 `cause 그대로 rc=0 broken=0`.
  음성 대조: `cause 망가뜨림` 줄 — 검사 스크립트를 판 `95508d9` 것으로 되돌린 사본에서 `rc=` 가 0 이 아니고 `broken=1`.
- [ ] SC-06: Given 테마 단추 id 가 `theme-btn` 이 아닌 `themeToggle` 인 쪽, When `node scripts/check-docs-a11y.js` 가 그 쪽을 재면, Then 단추 크기를 재어 `btn=<가로>x<세로>` 로 적고 44 미만이면 그 쪽을 FAIL 로 센다 [exact, enumerated]
  측정: `NODE_PATH=… bash M/m-a11y.sh <W>` 의 여섯 줄 — `color-palette.html OK btn=87x48` · `visual-styles.html OK btn=<가로>x<세로>` (둘 다 44 이상) · `korean-technical-writing.html OK btn=80x44` · `research-log.html OK btn=66x44` · `small-toggle.html FAIL btn=60x30` · `big-toggle.html OK btn=60x48` · 끝 줄 `rc=1` (small-toggle 때문).
  양성 대조: 봉인 전 실측 여섯 쪽 모두 `OK`, 앞 셋과 임시 둘이 `btn=none`, `rc=0` — 작은 단추를 못 잡는 결함이 지금 측정에 잡힌다.
- [ ] SC-07: `docs/design-kit/visual-styles.html` 의 테마 단추가 375 너비에서 가로 · 세로 모두 44 이상이고, 문서 사이트 전체 접근성 검사가 모든 쪽을 통과한다 [exact]
  측정: SC-06 의 `visual-styles.html` 줄의 두 수가 모두 44 이상. 그리고 W 에서 `node scripts/check-docs-a11y.js` 의 끝 줄이 `<N>/<N> PASS` 이고 N 은 `find docs -name '*.html' | grep -c .` 와 같으며 종료 코드 0. 봉인 전 실측 `189/189 PASS` · 단추 63x33.
- [ ] SC-08: Given 마켓 목록의 킷 수, When `bash scripts/spawn-kaizen-phase.sh <n>` 을 부르면, Then 받는 번호 상한은 4 + (harness 를 뺀 킷 수) 이고 킷 Phase 의 이름 · 슬러그는 마켓 목록 차례에서 뽑힌다 — 킷 이름 끝의 `-kit` · `-toolkit` 을 뗀 것이 슬러그 끝이다 [exact, enumerated]
  측정: `bash M/m-phase.sh <W>` 에서 (1) `same` 사본 n=1~17 의 슬러그가 봉인 전과 같다: `design-guides` · `contract` · `evaluator` · `harness` · `flutter` · `design` · `backend` · `infra` · `rust` · `react` · `planning` · `reflect` · `bambu` · `onboarding` · `tone` · `api` · `howto` (`kaizen-phase<n>-<이것>`, 모두 `rc=0`) (2) `same n=0` · `same n=18` · `same n=19` 가 `rc=1` (3) `foo` 사본 n=1~17 이 같은 슬러그 · `rc=0` 이고 `foo n=18 rc=0 slug=kaizen-phase18-foo` (4) `foo n=0` · `foo n=19` 가 `rc=1` (5) `same help_1_17=0` · `foo help_1_17=0`.
  알려진 답: 봉인 전 `foo n=18 rc=1 slug=` · `help_1_17=1`.
- [ ] SC-09: Given 마켓 목록, When `python3 scripts/run-evals.py` 를 돌리면, Then 평가 대상은 마켓 목록의 킷 가운데 `evals/evals.json` 이 있는 것이고, 형식이 달라 빼는 킷은 `SKIP <킷> (<사유>)` 줄로 이유를 댄다 — 지금 빼는 것은 `howto-kit` 하나다 [exact, enumerated]
  측정: `bash M/m-evals.sh <W>` 의 `same run-evals` 줄이 `rc=0 kits=api-kit,backend-kit,design-kit,flutter-toolkit,harness,infra-kit,react-kit,rust-kit,tone-kit skip=howto-kit bar_missing=0 total=[Total: 122 passed, 0 failed]`, `foo run-evals` 줄이 `rc=0 kits=api-kit,backend-kit,design-kit,flutter-toolkit,foo-kit,harness,infra-kit,react-kit,rust-kit,tone-kit skip=howto-kit bar_missing=0 total=[Total: 123 passed, 0 failed]`.
  알려진 답: 봉인 전 `foo` 줄에 `foo-kit` 없음 · `skip=` 비어 있음 · `122 passed`.
- [ ] SC-10: Given 마켓 목록, When `python3 scripts/sync-evals.py --check-only` 를 돌리면, Then 대상은 마켓 목록의 킷 가운데 `evals/evals.json` 이 있는 것이고 빼는 킷은 `SKIP <킷> (<사유>)` 줄로 이유를 댄다 — 지금 빼는 것은 `harness` · `howto-kit` 둘이다. 새 킷의 사례 없는 스킬은 MISSING 으로 잡혀 1 로 끝난다 [exact, enumerated]
  측정: `bash M/m-evals.sh <W>` 의 `same sync-evals` 줄이 `rc=0 kits=api-kit,backend-kit,design-kit,flutter-toolkit,infra-kit,react-kit,rust-kit,tone-kit skip=harness,howto-kit bar_missing=0 total=[Total: 0 added, 0 orphans, 0 missing (preview)]`, `foo sync-evals` 줄이 `rc=1 kits=api-kit,backend-kit,design-kit,flutter-toolkit,foo-kit,infra-kit,react-kit,rust-kit,tone-kit skip=harness,howto-kit bar_missing=1 total=[Total: 0 added, 0 orphans, 1 missing (preview)]`.
  알려진 답: 봉인 전 `foo sync-evals rc=0 … bar_missing=0`.
- [ ] SC-11: Given CI 파일 `.github/workflows/ci.yml`, When `bash scripts/ci-local.sh --list <폴더>` 를 부르면, Then CI 파일에서 `run:` 을 가진 단계를 모두 읽어 한 줄씩 `RUN <job> <단계 이름>` 또는 `SKIP <job> <단계 이름> (<사유>)` 로 적고 끝 줄 `steps=<N> run=<R> skip=<S> unsupported=<U>` 를 낸다. SKIP 은 준비 단계 다섯(`Install Python dependencies` · `Install dependencies` · `Install Playwright browsers` · `Install zsh (셸 대조 시험용)` · `Install zsh (공용 측정 파일 시험용)`)뿐이다. 단계 목록을 스크립트 안에 손으로 적지 않는다 [exact, enumerated]
  측정: `bash M/m-cilocal.sh <W>` 의 `repo-list rc=0 last=[steps=40 run=35 skip=5 unsupported=0] yaml_steps=40 skip_names=[Install Playwright browsers|Install Python dependencies|Install dependencies|Install zsh (공용 측정 파일 시험용)|Install zsh (셸 대조 시험용)]` 와 `extra-list rc=0 last=[steps=41 run=36 skip=5 unsupported=0] extra_run=1` (CI 파일에 단계 하나를 더한 사본 — 도구를 안 고쳐도 새 단계를 돈다). 그리고 `grep -cE 'validate-plugin|check-docs-a11y|run-evals' scripts/ci-local.sh` 이 0.
  알려진 답: `yaml_steps` 는 봉인 전 36, AR-01 의 네 단계를 더해 40. 봉인 전 도구가 없어 `rc=127`.
- [ ] SC-12: Given 작은 CI 파일(통과 단계 `Good` · 7 로 끝나는 단계 `Bad`), When `bash scripts/ci-local.sh <폴더>` 로 실제로 돌리면, Then 단계마다 `PASS <job> <이름> rc=0` / `FAIL <job> <이름> rc=<n>` 한 줄, 끝 줄 `steps=2 run=2 skip=0 unsupported=0 failed=1`, 종료 코드 1 이다. 도구의 시험 `scripts/test-ci-local.sh` 가 이 경우와 SC-11 · ER-02 의 경우를 맞대고 통과한다 [exact]
  측정: `bash M/m-cilocal.sh <W>` 의 `two-run rc=1 last=[steps=2 run=2 skip=0 unsupported=0 failed=1] fail_line=1 pass_line=1`. 그리고 `bash M/m-tests.sh <W> 95508d9` 의 `cilocal 그대로 rc=0 broken=0`.
  음성 대조: `cilocal 망가뜨림` 줄 — 도구를 아무것도 안 하고 0 으로 끝나는 가짜로 바꾼 사본에서 `rc=` 가 0 이 아니고 `broken=1`.
- [ ] SC-13: (커밋 뒤) 새 로컬 CI 도구로 W 의 CI 전체를 돌리면 모든 단계가 통과한다 — 옛 도구가 빠뜨린 다섯 단계(`python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · bambu 시험 두 명령 · `bash harness/evals/measure/measure-helpers-test.sh`)와 AR-01 의 새 네 단계를 포함한다 [exact, enumerated]
  측정: `TMPDIR=<scratch 아래 폴더> bash scripts/ci-local.sh <W>` 의 끝 줄이 `steps=40 run=35 skip=5 unsupported=0 failed=0` 이고 종료 코드 0. 다섯 단계 이름이 각각 `PASS ` 로 시작하는 줄에 있다: `api-kit docs check` · `Docs drift mapping check` · `Cause table copy check` · `Bambu-kit gate fixtures · MakerWorld fetch test` · `Measure helpers test`.

## Error

- [ ] ER-01: superseded 확인 스크립트에 없는 폴더를 주면 위반 0 으로 통과하지 않고 2 로 끝난다 [exact]
  측정: `bash M/m-superseded.sh <W>` 의 `MISSING rc=2` 로 시작하는 줄.
- [ ] ER-02: 로컬 CI 도구는 (a) CI 파일이 없는 폴더에서 2 로 끝나고 (b) `name` · `run` 밖의 열쇠(`working-directory` 등)가 있는 단계를 돌리지 않고 `UNSUPPORTED <job> <이름> (<사유>)` 로 알린 뒤 1 로 끝난다 [exact, enumerated]
  측정: `bash M/m-cilocal.sh <W>` 의 `none-list rc=2` 와 `wd-list rc=1 last=[steps=2 run=1 skip=0 unsupported=1] unsupported_line=1`.
- [ ] ER-03: 판정 표 사본 검사는 원문 덩어리의 끝 표지(`판정 표와 두 경우는` 으로 시작하는 줄)가 없으면 통과시키지 않고 `CANON_MISSING` 과 2 로 끝난다 [exact]
  측정: `bash M/m-cause.sh <W>` 의 `e-note-removed rc=2` 로 시작하고 `applied=0` 으로 끝나는 줄 (applied 는 원문에서 표지 줄을 지운 뒤 남은 수라 0 이 맞다).
- [ ] ER-04: Phase 부트스트랩은 범위 밖 번호에서 태그를 만들기 전에 1 로 끝난다 [exact, enumerated]
  측정: SC-08 측정의 `same n=0` · `same n=18` · `same n=19` · `foo n=0` · `foo n=19` 다섯 줄이 `rc=1 slug=` (슬러그 빈 값).

## Architecture

- [ ] AR-01: CI 파일에 run 단계 넷이 더해지고 기존 36 단계의 명령은 그대로다 — 더하는 넷의 명령: `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `python3 scripts/test-check-cause-table-copies.py` · `bash scripts/test-ci-local.sh` [exact, enumerated]
  측정: `python3 -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[1])); [print(s["run"].strip()) for j in d["jobs"].values() for s in j["steps"] if "run" in s]' <파일>` 을 `git show 95508d9:.github/workflows/ci.yml` 과 W 의 파일에 각각 돌려 `LC_ALL=C sort` 후 `comm` — 사라진 명령 0 줄, 새 명령이 정확히 위 넷.
- [ ] AR-02: 종료 코드 표 `harness/evals/gate-exit-codes.md` 에 새 스크립트 둘(`harness/scripts/check-superseded.sh` · `scripts/ci-local.sh`)의 행이 있고, 표의 행과 그 표를 인용하는 스크립트가 서로 빠짐없이 맞는다 [exact, enumerated]
  측정: `bash M/m-exit.sh <W>` 가 `rows=<k> cite=<k> only_rows=[] only_cite=[]` (두 k 가 같고 14 이상 — 새 시험 파일이 표를 인용하면 그 행도 있어야 한다). 그리고 ``grep -cE '^\| `(harness/scripts/check-superseded.sh|scripts/ci-local.sh)` \|' harness/evals/gate-exit-codes.md`` 가 2. 봉인 전 `rows=12 cite=12`, 인용만 하는 가짜 파일을 넣으면 `only_cite` 에 잡힘을 확인했다.
- [ ] AR-03: 대응 쪽 `docs/harness/contract-schema.html` 이 원본 변경을 싣는다 — `fm_get` 코드가 원본과 글자까지 같고, `check-superseded.sh` · `disable-next-line` · `meaning.py` 가 쪽에 있고, 공통 스타일 링크가 하나이며, 320 · 375 · 1280 너비 가로 넘침이 2 px 이하다 [exact, enumerated]
  측정: `bash M/m-docs.sh <W>` 의 `html check-superseded.sh=` · `html disable-next-line=` · `html meaning.py=` 가 1 이상, `html assets/site.css=1`, 끝 줄이 `fm_same=1 md_lines=<k> html_lines=<k>` (두 k 가 같고 1 이상). 넘침은 `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` 줄의 `of=<320>/<375>/<768>/<1280>` 에서 첫째 · 둘째 · 넷째가 2 이하이고 줄이 `OK` 로 시작.
  양성 대조: 봉인 전 세 낱말 0 건. `fm_same` 은 원본만 고치고 쪽을 안 고치면 0 이 된다.
- [ ] AR-04: D4 결정이 notes `.harness/.meta/after-kaizen-0928/h1-notes.md` 에 근거와 함께 있고, 변환 스크립트는 레포에 들이지 않는다 [exact, enumerated]
  측정: (1) notes 파일에 `D4` 와 `두지 않는다` 가 같은 줄에 있는 줄 1 개 이상 (2) notes 에 `same=6 total=21` 과 `m-d4.sh` 가 각각 1 번 이상 (3) notes 에 다시 만드는 길로 `docs-site` 와 `detect-docs-drift.py` 가 각각 1 번 이상 (4) (커밋 뒤) `git diff --name-only 95508d9 chore/ak3-h1 -- . ':(exclude).harness' | grep -cE '(^|/)(gen|pages|gen_yaml)\.py$|page\.css$'` 이 0.
- [ ] AR-05: (커밋 뒤) 이 가지가 `.harness` 밖에서 바꾼 경로가 정확히 아래 18 개이고, 커밋마다 맨 위 폴더가 하나 · 서명 줄이 하나이며, 커밋 안 된 `.harness` 밖 변경이 없다 — `.github/workflows/ci.yml` · `docs/design-kit/visual-styles.html` · `docs/harness/contract-schema.html` · `harness/agents/qa-evaluator.md` · `harness/evals/gate-exit-codes.md` · `harness/evals/measure/measure-helpers-test.sh` · `harness/evals/superseded/check-superseded-test.sh` · `harness/references/contract-schema.md` · `harness/scripts/check-superseded.sh` · `harness/skills/sprint-contract/SKILL.md` · `scripts/check-cause-table-copies.py` · `scripts/check-docs-a11y.js` · `scripts/ci-local.sh` · `scripts/run-evals.py` · `scripts/spawn-kaizen-phase.sh` · `scripts/sync-evals.py` · `scripts/test-check-cause-table-copies.py` · `scripts/test-ci-local.sh` [exact, enumerated]
  측정: `bash M/m-scope.sh <W> 95508d9 chore/ak3-h1` — 상한은 가지 `chore/ak3-h1` 를 풀어 쓴다(HEAD 아님, 풀리지 않으면 `STOP` · 2 로 FAIL). 첫 줄 `changed=` 뒤가 위 18 경로를 글자 차례로 쉼표로 이은 것과 정확히 같고, 끝 줄이 `commits=<n> bad=0 dirty=0` (n ≥ 1). 서명 줄은 `%(trailers:key=Co-Authored-By,valueonly)` 로 재므로 `%B` 끝 빈 줄 함정이 없다. 봉인 전 `changed=` 빈 값 · `commits=0`.
- [ ] AR-06: (커밋 뒤) 옛 로컬 CI 도구와 봉인된 계약 · QA 리포트 · 개정 파일이 그대로이고, 새 도구는 레포에 추적된다 [exact, enumerated]
  측정: (1) `shasum -a 256 /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh | cut -c1-16` 이 `59fe55125c0dbc77` (2) `git -C <W> diff --name-only --diff-filter=MD 95508d9 chore/ak3-h1 -- '.harness/sprint-contract-*.md' '.harness/sprint-feedback-*.md' '.harness/sprint-amendments-*.md' | grep -c .` 이 0 (3) `git -C <W> ls-files --error-unmatch scripts/ci-local.sh` 종료 코드 0.
  양성 대조: (2) 의 명령을 `fb5374b~1 fb5374b` 구간에 돌리면 1 — 계약 수정이 잡힌다 (봉인 전 실측).

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 (고치는 SKILL.md · 계약 형식 문서 · qa-evaluator.md 에 새 코드 블록이 들어간다)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지. 측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0 (sprint-contract SKILL.md · qa-evaluator.md 를 고친다)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — superseded 확인은 폴더를 인자로 받는 독립 스크립트이고 로컬 CI 도구는 폴더를 인자로 받는다. 측정: SC-01 · SC-11 이 임시 폴더 인자로 돈다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — superseded 확인은 머리 값을 공용 측정 파일의 `fm_get` 으로 읽고 자기 읽개를 새로 두지 않는다. 측정: `grep -cE '^[[:space:]]*(fm_get|read_fm)\(\)' harness/scripts/check-superseded.sh` 이 0 이고 `grep -c 'measure-common.sh' harness/scripts/check-superseded.sh` 가 1 이상

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: (커밋 뒤) `git diff --name-only 95508d9 chore/ak3-h1 | grep -c '^scripts/release.sh$'` 이 0. 실제 오라클은 DG-02 · SC-13)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude 는 빈 목록) — 이번에 바꾸거나 더한 `.md` 의 더한 줄에 markdownlint 경고 0 · `.sh` 새 파일 전체와 고친 파일의 더한 줄에 shellcheck 경고 0 · `.py` 컴파일 실패 0 · `.js` 문법 실패 0. 측정: `bash M/m-diag.sh <W> 95508d9 /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl` 끝 줄이 정확히 `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=18` (files 는 AR-05 의 18 경로 — 종류 밖 파일도 센다). markdownlint-cli2 0.23.2 · MD013 끔(편집기 확장과 같음). 양성 대조: 봉인 전 md 한 줄 · sh 한 줄 · 깨진 py 한 파일을 넣어 `md_new=1 sh_new=2 py_bad=1` 로 잡힘을 확인했다
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` 로 릴리스 스크립트만 돈다 — 이번 변경 파일과 교집합 0 개. 실제 오라클은 SC-13 의 로컬 CI 전체)
- [ ] DG-04: N/A (산출물에 구동할 앱 · 서버가 없다 — 변경은 문서 · 검사 스크립트 · CI 파일 · 문서 쪽. 실제 오라클은 SC-13 과 SC-07 의 브라우저 측정)

사용자가 할 일: 없음
