---
feature: "기존 마크다운 경고 정리 — harness · .claude · 루트 README · CLAUDE.md · docs/superpowers (l4)"
slug: after-0926-mdlint-l4
created: "2026-09-27 14:58"
complexity: "복잡"
conditions: 21
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:72cdc70fdb63b31c
measurement_digest: sha256:6de3290ef0c03e2a
locked_at: "2026-09-27 15:10"
---

## 배경

- 사용자 결정 UD-7(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`): 범위 밖 기존 markdownlint 경고를 전부 고친다. 위임 기록: 2026-09-26T10:30:16.222Z 「전부 고친다」 · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l4` (가지 `chore/ak2-l4`, 기준 `chore/after-kaizen-0926b` 의 c3e45f3). 모든 측정은 W 맨 위에서 돈다.
- 대상 목록 L = `.harness/.meta/after-kaizen-0926b/l4-files.txt` (109 줄, 커밋 98a7f9c). 만든 식: `git ls-files '*.md' | grep -E '^(harness|\.claude|scripts|docs/superpowers)/|^(README|CLAUDE)\.md$' | grep -v '^\.harness/'` 116 개에서 고치지 않는 파일 7 개를 뺐다. `scripts/` 아래에는 추적되는 md 가 없어 목록에 한 줄도 없다.
- 고치지 않는 파일 7 개와 근거 (grep 으로 찾음):
  - `harness/evals/test-fixtures/README.md` · `harness/evals/test-fixtures/fixture-a/contract.md` · `harness/evals/test-fixtures/fixture-b/contract.md` · `harness/evals/test-fixtures/fixture-c/contract.md` · `harness/evals/test-fixtures/fixture-d/contract.md` · `harness/evals/test-fixtures/fixture-e/contract.md` — 경로에 evals/ 와 fixture 가 함께 든다
  - `harness/references/contract-schema.md` — 시험 스크립트 `harness/evals/measure/measure-helpers-test.sh:11` 이 열어 bash 블록에서 측정 도우미를 뽑는다
  - 목록 파일 경로를 적은 md 밖 파일은 전부 찾았다(`git grep -l -F -- <경로> -- ':(exclude)*.md' ':(exclude)*.html' ':(exclude).harness'`, 17 개 경로가 걸림). 그 가운데 시험이 여는 것: `harness/evals/kaizen/*/assertions.json` 이 `harness/skills/sprint-contract/SKILL.md` · `harness/docs/guides/contract-design-guide.md` · `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md` 에서 낱말 패턴을 찾는다 — 내용을 뽑아 돌리는 시험이 아니라 문구 검사라, l3a 가 run-evals 의 문구 검사를 다룬 방식대로 고칠 대상에 두고 SC-01 의 `kaizen-assertions` 단계가 지킨다. 나머지는 주석 속 언급이거나(`gate-exit-codes.md` 를 부르는 스크립트들) 검사 도구가 읽는 것(`sync-docs.py` · `sync-orchestrator.py` · `detect-docs-drift.py` · `check-*-copies.py`)이라 SC-01 이 잰다
  - `.harness/` 아래는 전부 고치지 않는다(봉인된 계약 기록). 목록 식이 `.harness/` 를 뺀다
- 공통 기호 (모든 조건이 이 뜻으로 쓴다. 명령은 `cd $W` 뒤에 돈다):
  - `W` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l4`
  - `L` = `.harness/.meta/after-kaizen-0926b/l4-files.txt`
  - `B` = `275e4fb` (측정 묶음 마지막 커밋 — 교차 진단 지적을 반영한 canon.sh · meaning.py 판. `.harness` 밖 파일은 c3e45f3 · e5333b7 과 같다)
  - `U` = `$(git rev-parse --verify -q chore/ak2-l4) || exit 2` — 이 묶음 가지 끝. `HEAD` 를 상한으로 쓰지 않는다
  - `M` = `.harness/.meta/after-0926-mdlint-l4` (측정 묶음: `lint.sh` · `meaning.py` · `ci.sh` · `auto.py` · `canon.sh`. lint.sh · meaning.py 는 l3b 판 그대로, ci.sh 는 l3b 판에 ci-local 종료 코드 줄을 더했다)
  - `N` = `.harness/.meta/after-kaizen-0926b/l4-notes.md` (구현이 만든다 — 끄기 주석과 제목 단계 변경의 자리와 이유)
  - `R` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint/run.sh`
- 공통 전제 (Given, 모든 조건에 한 번에 건다): 이 묶음의 커밋이 전부 끝났고, `git status --porcelain --untracked-files=all` 이 계약 자신의 `status:` 줄 말고 0 줄이다 (contract-schema.md 의 `dirty_except_status` 로 잰다). 뜻 · 범위 조건은 `B..U` 커밋 구간으로 재고, 경고 수는 작업 트리로 잰다.
- 측정 도구: markdownlint-cli2 0.23.2, 설정 `cfg.jsonc` = `{ "config": { "MD013": false } }` (sha256 앞 16 자리 `dfe13e2d516b31e5`, 편집기 확장 기본값과 같음).
- 「뜻이 안 바뀜」 의 허용 모양 (meaning.py 가 떼는 것): 공백 · 빈 줄 · 표 구분 줄 · 코드 블록 여는 줄의 언어 · 제목 표식 `#` · 줄 전체를 감싼 강조 `**` · 빈 인용 줄 `>` · http(s)/ftp URL 꺾쇠 `<>` · `<!-- markdownlint-… -->` 주석. 이것 말고 한 글자라도 다르면 MISMATCH 다. 앞머리(frontmatter) 블록과 코드 블록 속 줄은 공백까지 같아야 한다. 공백을 지우면 같아도 코드 조각 · 강조 표식 옆 공백이 바뀌면 SPACING, 따로이던 인용이 합쳐지면 QUOTEJOIN, 꺾쇠 안에 주소 아닌 글자가 들면 BADANGLE 이다. 목록 번호 숫자를 바꾸는 것(MD029 고침)은 허용 모양이 아니다.

## 리서치 소스

- 봉인 전 실측 (2026-09-27, 판 e5333b7 작업 트리):
  - `bash $M/lint.sh $W $W/$L | tail -1` → `LINTED=109 WARNINGS=1661`. `bash $R $W $W/$L | grep -c .` → `1661`
  - 규칙별: MD060 764 · MD032 336 · MD031 164 · MD040 97 · MD022 84 · MD036 66 · MD025 63 · MD024 38 · MD034 12 · MD041 7 · MD058 5 · MD038 5 · MD029 5 · MD001 5 · MD056 2 · MD033 2 · MD012 2 · MD047 1 · MD037 1 · MD028 1 · MD003 1
  - 경고가 있는 파일 89 개 / 109 개. 고치지 않는 파일 7 개의 경고는 75 건(`bash $M/lint.sh $W <7 개 목록>` → `LINTED=7 WARNINGS=75`, 이 묶음 밖)
  - AUTO 블록 안 · 밖 (contract-schema §4 Diagnostics): 줄 첫머리 `<!-- AUTO:` 블록이 있는 목록 파일은 `README.md` · `harness/README.md` · `CLAUDE.md` · `.claude/skills/kaizen-orchestrator/SKILL.md` (표식 줄 44 개). `python3 $M/auto.py $W <lint 출력>` → `in_auto=0 out_auto=1661`. 양성 대조: `README.md:8`(블록 안) · `README.md:30`(밖) 두 줄을 넣으면 `in_auto=1 out_auto=1`
  - `python3 $M/meaning.py --selftest` → 20 경우 전부 OK, `SELFTEST PASS` (판 275e4fb — 교차 진단 지적대로 「제목 단계만」(`# 제목` → `## 제목`) 경우를 더했고 `mismatch=0 heading=1` 이 실행으로 나왔다)
  - `python3 $M/meaning.py $W HEAD HEAD $W/$L | tail -1` → `CHECKED=109 MISMATCH=0 SPACING=0 QUOTEJOIN=0 BADANGLE=0 FRONTMATTER=0 CODEBLOCK=0 HEADING=0 DISABLE=0 BADDISABLE=0 NOTES_MISSING=0`
  - `bash $M/ci.sh $W | tail -2` (판 b90f348, `.harness` 밖은 B 와 같음) → `CI_LOCAL_RC=0` · `CI_OK=28 CI_BAD=0 CI_SKIP=1`
  - `bash $M/canon.sh $W $B` → `CANON_LINES=157 CANON_SHA=c9e099aee5ca5df7` (판 275e4fb. e5333b7 판 canon.sh 는 `## Canonical` 절 밖의 4 요건 덩어리(892 줄 제목 아래)를 빠뜨려 150 줄이었다 — 교차 진단 지적. 지금 판은 `scripts/check-reviewer-protocol-copies.py` 의 `canonical_blocks()` 를 그대로 불러 그 덩어리를 뽑는다)
  - 시험 사본(`git archive b90f348` 를 scratch 에 풀어 git 저장소로 만들고 목록 파일에만 `--fix`): 경고 1661 → 326 (MD040 97 · MD036 66 · MD025 63 · MD060 44 · MD024 38 · MD041 7 · MD001 5 · MD056 2 · MD033 2 · MD028 1 · MD003 1). `meaning.py` → `MISMATCH=1 SPACING=4 CODEBLOCK=5` — 자동 고침만으로는 뜻이 바뀐다(`docs/superpowers/plans/2026-03-29-harness-kaizen.md` 등 코드 블록 속 줄 5 파일, 코드 조각 속 공백 4 자리). `canon.sh`(e5333b7 판) → `CANON_SHA=23723dd04e912627` 로 시작 판과 같았다 (자동 고침은 정본 덩어리를 건드리지 않는다. 4 요건 덩어리는 시작 판 경고가 0 건이라 자동 고침이 닿지 않는다). `ci.sh` → `CI_LOCAL_RC=0` · `CI_OK=28 CI_BAD=0 CI_SKIP=1` (자동 고침만으로 깨지는 검사 단계는 없다 — 뜻 검사 SK-02 가 막는 자리가 따로 있다)

## GAP 분석

- Pre-Edit 확인 (실제로 연 자리):
  - `harness/evals/measure/measure-helpers-test.sh:11` — `schema=$root/harness/references/contract-schema.md` 를 열어 도우미를 뽑는다 → 고치지 않는 파일
  - `scripts/check-cause-table-copies.py:24-27` — `CANON = "harness/skills/sprint/SKILL.md"`, 덩어리는 `| 공용 작업 폴더 |` 줄부터 `- **미확정**` 줄까지. 목록 파일 가운데 이 파일은 시작 판 경고 0 건
  - `scripts/check-reviewer-protocol-copies.py:31-34` — `harness/docs/guides/qa-evaluation-guide.md` 의 `## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)` 절과 `#### \`UNVERIFIED_ENV\` 남용 방지 4 요건` 제목(892 줄, `## Canonical` 절 밖)을 읽는다. 두 Canonical 절(1251 · 1322 줄에서 시작)과 4 요건 덩어리에는 시작 판 경고가 없다
  - `harness/evals/kaizen/evaluator-kaizen/assertions.json:17-18` — `## Check Artifacts` 제목 바로 뒤 빈 줄 모양과 `### 산출물이 검사일 때` 제목을 정규식으로 찾는다. 제목 단계 · 빈 줄 모양을 바꾸면 깨질 수 있다
  - `scripts/sync-orchestrator.py:28,87` — `.claude/skills/kaizen-orchestrator/SKILL.md` 에 `### Step N: Phase …` 제목을 쓴다(AUTO 블록)
- 정본 덩어리 합치기 위험: 두 사본 대조 검사는 다른 킷 사본과 줄 단위로 맞댄다(`scripts/plugin_utils.py:132` `normalized` 는 줄 앞 공백 · `>` · 끝 공백과 빈 줄만 버린다). 다른 묶음(l2 · l3a)이 사본을 고치는 가지가 따로 있어, 이 묶음이 정본 줄 모양을 바꾸면 가지마다는 통과해도 합친 뒤 깨질 수 있다 → ER-04 로 정본 덩어리를 한 글자도 안 바꾸게 막는다. 시작 판에서 그 덩어리에 경고가 없어 막아도 SK-01 과 부딪히지 않는다
- 제목 경고: MD025 63 · MD041 7 · MD001 5 · MD003 1 · MD036 66 · MD024 38. `.claude/skills/*-kaizen` · `*-research` SKILL.md 의 MD025 가 많다. H1 을 새로 넣으면 낱말이 늘어 SK-02 가 막고, 단계를 바꾸면 SK-03 의 notes 기록과 grep 확인이 필요하다
- MD029 5 건은 목록 번호 숫자를 바꾸면 SK-02 MISMATCH 다 — 좁힌 끄기가 맞는 모양이다. MD056 2 건(표 칸 수)도 칸을 더하면 낱말이 늘 수 있다
- ci-local.sh 의 종료 코드: 마지막 줄이 `grep -v 'rc=0' summary.txt` 라 yq 가 없는 이 맥에서는 SKIP 줄 때문에 0 이다. 과제가 종료 코드 0 을 요구해 `CI_LOCAL_RC` 로 따로 재되, 실패 단계를 놓치지 않게 요약 줄 `CI_BAD=0` 을 함께 본다 (SC-01)

## 범위 경계

```text
# sprint-scope
harness/
.claude/
docs/superpowers/
README.md
CLAUDE.md
```

- 위 블록은 커밋 직전 훅용이다. 폴더 안에서도 고칠 수 있는 파일은 목록 L 의 109 개뿐이고(AR-01), 고치지 않는 파일 7 개는 ER-01 이 잰다
- `.harness/` 아래에서 이 묶음이 바꿀 수 있는 경로: 이 계약 · `sprint-amendments-after-0926-mdlint-l4.md` · `sprint-feedback-after-0926-mdlint-l4.md` · `N`. 그 밖 `.harness/` 경로는 AR-02 가 막는다
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. 한 커밋에 맨 위 폴더 하나(`harness` · `.claude` · `docs` · `README.md` · `CLAUDE.md` · `.harness` 가운데 하나 — 루트 파일 둘은 각각 따로). 메시지는 한국어, 끝 줄은 빈 줄 뒤 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` — 봉인 커밋도 같다. `git add -A` · `git stash` · push · 가지 바꾸기 금지
- 자동 고침은 `markdownlint-cli2 --config <cfg.jsonc> --fix` 를 목록 L 의 파일에만 돌린다(폴더 통째 금지). 자동 고침이 코드 블록 속 줄 · 코드 조각 속 공백 · 주소 아닌 글자를 바꾸면 되돌리고 그 자리를 좁혀 끈다
- 규칙을 지키면 뜻이 깨지는 자리(일부러 두 번 쓴 제목 · 원문 인용 · 목록 번호 · 표 칸 `<br>` 등)만 좁혀 끈다. 꼴은 `<!-- markdownlint-disable-next-line 규칙 -->` 또는 같은 규칙의 `disable` · `enable` 짝(표처럼 한 줄 끄기를 넣으면 모양이 끊기는 자리). 파일 전체 끄기 금지. 꼴은 ER-02, 기록은 ER-03
- 문장을 새로 쓰지 않는다. 톤 규칙은 문장을 새로 쓰는 자리에만 걸리므로 이 묶음에는 걸릴 자리가 없다 (notes 문장은 예외 — notes 는 설명 문장이다)
- 측정 묶음(`M` 의 다섯 파일)과 목록 L 은 봉인 뒤 바꾸지 않는다(SC-02). 바꿔야 하면 개정 파일에 쓴다
- `meaning.py` 는 notes `N` 이 없으면 파일 없음 오류로 멈춘다. 구현 중간에 SK-02 · SK-03 · ER-02 · ER-03 측정을 돌리기 전에 `N` 을 빈 파일로라도 먼저 만들어 둔다
- 커버리지 해소: ER-01 — 산문의 일곱 경로를 측정 절 끝 「대상:」 에 같은 표기로 다시 적었다
- 커버리지 해소: SC-02 — 여섯 파일 이름이 측정 절에 경로째 적혀 있다
- 커버리지 해소: SC-01 — 과제가 이름을 댄 검사 여덟(`validate-plugin` · `sync-docs` · `sync-orchestrator` · `sync-evals` · `run-evals` · `kaizen-assertions` · `reviewer-copies` · `cause-table-copies`)이 28 단계 이름 목록 안에 같은 표기로 있다
- 오라클 해소: SK-03 — grep 은 문서 서술을 찾는 것이 아니라 `meaning.py` 를 실행해 나온 HEADING 자리를 notes 와 맞대는 것이다. 판정은 실행 출력으로 한다
- 오라클 해소: AR-04 — 커밋 메시지는 산출물 그 자체라 `git log` 로 실제 기록을 읽어 잰다

## 회귀 게이트

- 기존 검사 28 단계는 시작 판에서 전부 rc=0 이고 ci-local.sh 종료 코드도 0 이다(리서치 소스 실측). 이 묶음이 끝난 뒤에도 같아야 한다(SC-01)
- 이 계약이 안 보는 것: 목록 밖 md(다른 킷 묶음 l1 · l2 · l3a · l3b)의 경고, 고치지 않는 파일 7 개의 경고 75 건

## Skill

- [ ] SK-01: 목록 L 의 109 개 파일에서 편집기와 같은 설정의 markdownlint 경고가 0 건이다 [exact]
    측정: `bash $M/lint.sh $W $W/$L | tail -1` 이 정확히 `LINTED=109 WARNINGS=0` 이고, `bash $R $W $W/$L | grep -c .` 이 `0`
    음성 대조: 시작 판(e5333b7)에서 같은 두 명령이 `LINTED=109 WARNINGS=1661` · `1661` (봉인 전 실측). 검사기가 돌지 않으면 lint.sh 가 `STOP` 과 종료 코드 2 를 내므로 0 으로 새지 않는다
- [ ] SK-02: 목록 L 의 109 개 파일의 뜻이 시작 판과 같다 — 허용 모양(배경 절)을 떼고 공백을 지운 글자열이 같고, 코드 조각 · 강조 표식 옆 공백과 인용 덩어리 수가 같고, 새 꺾쇠 안은 주소 글자뿐이며, 앞머리 블록과 코드 블록 속 줄은 공백까지 같다 [exact]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 에서 `CHECKED=109` · `MISMATCH=0` · `SPACING=0` · `QUOTEJOIN=0` · `BADANGLE=0` · `FRONTMATTER=0` · `CODEBLOCK=0`
    음성 대조: 시험 사본에 `--fix` 만 돌린 판은 `MISMATCH=1 SPACING=4 CODEBLOCK=5` (봉인 전 실측). `python3 $M/meaning.py --selftest` 의 낱말 바꿈 · 순서 바꿈 · 앞머리 들여쓰기 · 코드 속 들여쓰기 · 코드 조각 속 공백 · 인용 둘 합침 · 꺾쇠가 조사까지 감쌈 경우가 각각 1 을 낸다
- [ ] SK-03: 단계가 바뀌었거나 새로 생긴 제목마다 notes `N` 에 `- <경로>:<줄> … — <이유>` 줄이 있고, 그 줄에 제목 낱말을 찾은 grep 명령이 적혀 있다 [exact, enumerated]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N` 의 `HEADING <경로>:<줄>` 줄마다 같은 `경로:줄` 의 `NOTES_MISSING` 줄이 없고, `python3 $M/meaning.py $W $B $U $W/$L $W/$N | awk '/^HEADING /{print $2}' | while read -r k; do awk -v p="- $k " 'index($0,p)==1 && /grep/{f=1} END{exit !f}' $W/$N || echo "NOGREP $k"; done | grep -c .` 이 `0`. HEADING 이 0 줄이면 이 조건은 notes 없이 통과한다
    음성 대조: selftest 의 「notes 이유 없음」 · 「notes 다른 줄」 경우가 `NOTES_MISSING=1`. 「제목 단계만」(`# 제목` → `## 제목`, 글자 같고 단계만 다름) 경우가 `mismatch=0 heading=1` 이라 HEADING 자리로 잡힌다 (판 275e4fb, 봉인 전 실측)

## Script

- [ ] SC-01: 검사 28 단계 `validate-plugin` · `sync-evals` · `sync-docs` · `sync-orchestrator` · `run-evals` · `contrast-claims` · `docs-links` · `stale-values` · `collector-test` · `react-detect-test` · `reflect-log-test` · `reflect-projid-test` · `reflect-collect-test` · `onboarding-gate-evals` · `howto-gate-evals` · `feedback-save-test` · `commit-guard-test` · `dart-format-hook-test` · `playwright-visuals` · `docs-a11y` · `scenario-report-ut` · `decision-gate-test` · `kaizen-assertions` · `reviewer-copies` · `api-ui-viewer` · `cause-table-copies` · `docs-drift-table` · `measure-helpers` 가 전부 rc=0 이고, `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` 의 종료 코드가 0 이다. `feedback-agg-test SKIP (yq 없음)` 줄은 허용한다 [exact, enumerated]
    측정: `bash $M/ci.sh $W | tail -2` 가 `CI_LOCAL_RC=0` 과 `CI_OK=28 CI_BAD=0 CI_SKIP=1` 두 줄 (yq 가 설치된 기계면 끝 줄 `CI_OK=29 CI_BAD=0 CI_SKIP=0`). 단계 이름 28 개는 같은 실행의 요약 줄(`ci.sh` 출력 앞부분)에 각각 `rc=0` 으로 나온다
    음성 대조: 시험 사본에서 `README.md` 의 AUTO 블록 줄 하나(8 줄)를 고치면 `python3 scripts/sync-docs.py --check-only` 가 rc=1, 고치기 전 rc=0 (봉인 전 실측) — 그 단계가 `CI_BAD` 로 잡힌다
- [ ] SC-02: 측정 묶음과 목록 파일이 봉인 뒤 바뀌지 않았다 — `.harness/.meta/after-0926-mdlint-l4/lint.sh` · `.harness/.meta/after-0926-mdlint-l4/meaning.py` · `.harness/.meta/after-0926-mdlint-l4/ci.sh` · `.harness/.meta/after-0926-mdlint-l4/auto.py` · `.harness/.meta/after-0926-mdlint-l4/canon.sh` · `.harness/.meta/after-kaizen-0926b/l4-files.txt` [exact, enumerated]
    측정: `shasum -a 256 <파일> | cut -c1-16` 이 차례로 `.harness/.meta/after-0926-mdlint-l4/lint.sh` `241f16dba9687ed9` · `.harness/.meta/after-0926-mdlint-l4/meaning.py` `b357357dd14ab08d` · `.harness/.meta/after-0926-mdlint-l4/ci.sh` `592e8a77d0dd807b` · `.harness/.meta/after-0926-mdlint-l4/auto.py` `7b64340cb05bd679` · `.harness/.meta/after-0926-mdlint-l4/canon.sh` `6442e910fa0589e1` · `.harness/.meta/after-kaizen-0926b/l4-files.txt` `674a1f5615f2644d`, 그리고 `wc -l < $W/$L | tr -d ' '` 이 `109` (이 맥의 `wc` 는 앞에 공백을 붙인다)

## Error

- [ ] ER-01: 고치지 않는 파일 7 개 `harness/references/contract-schema.md` · `harness/evals/test-fixtures/README.md` · `harness/evals/test-fixtures/fixture-a/contract.md` · `harness/evals/test-fixtures/fixture-b/contract.md` · `harness/evals/test-fixtures/fixture-c/contract.md` · `harness/evals/test-fixtures/fixture-d/contract.md` · `harness/evals/test-fixtures/fixture-e/contract.md` 가 한 줄도 바뀌지 않았다 — 끄기 주석도 없다 [exact, enumerated]
    측정: `git diff --name-only $B $U -- harness/references/contract-schema.md harness/evals/test-fixtures/README.md harness/evals/test-fixtures/fixture-a/contract.md harness/evals/test-fixtures/fixture-b/contract.md harness/evals/test-fixtures/fixture-c/contract.md harness/evals/test-fixtures/fixture-d/contract.md harness/evals/test-fixtures/fixture-e/contract.md | grep -c .` 이 `0` 이고, 같은 일곱 경로에 `git status --porcelain --` 가 0 줄 (대상: `harness/references/contract-schema.md` · `harness/evals/test-fixtures/README.md` · `harness/evals/test-fixtures/fixture-a/contract.md` · `harness/evals/test-fixtures/fixture-b/contract.md` · `harness/evals/test-fixtures/fixture-c/contract.md` · `harness/evals/test-fixtures/fixture-d/contract.md` · `harness/evals/test-fixtures/fixture-e/contract.md`)
    양성 대조: 시험 사본에서 `harness/references/contract-schema.md` 끝에 빈 줄 하나를 더해 커밋하면 같은 diff 명령이 `1`, 더하기 전 `0` (봉인 전 실측)
- [ ] ER-02: 새로 넣은 markdownlint 주석은 전부 규칙 번호가 적힌 `disable-next-line` 이거나, 같은 규칙의 `enable` 이 뒤에 오는 `disable` · 그 짝 `enable` 이다 — `disable-file` · `configure-file` · 규칙 없는 끄기 · 짝 없는 `disable` 은 0 개 [exact]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 의 `BADDISABLE=0`
    양성 대조: selftest 의 「짝 없는 disable」 · 「파일 전체 끄기」 경우가 각각 `BADDISABLE=1`, 「한 줄 끄기 꼴」 이 `BADDISABLE=0`
- [ ] ER-03: notes `N` 에 `끄기 주석 수: <n>` 줄이 정확히 하나 있고 n 이 새로 넣은 주석 수와 같으며, 새 주석마다 `- <경로>:<줄> <규칙> — <이유>` 줄이 있다 [exact]
    측정: `grep -cE '^끄기 주석 수: [0-9]+$' $W/$N` 이 `1` · 그 수가 `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 의 `DISABLE=` 값과 같음 · 같은 끝 줄의 `NOTES_MISSING=0`
    음성 대조: selftest 의 「notes 이유 없음」 · 「notes 다른 줄」 경우가 `NOTES_MISSING=1`
- [ ] ER-04: 다른 킷 사본과 맞대는 정본 덩어리(`harness/docs/guides/qa-evaluation-guide.md` 의 `## Canonical ` 절 둘과 `#### \`UNVERIFIED_ENV\` 남용 방지 4 요건` 덩어리, `harness/skills/sprint/SKILL.md` 의 `| 공용 작업 폴더 |` ~ `- **미확정**` 덩어리)가 한 글자도 바뀌지 않았다 [exact]
    측정: `bash $M/canon.sh $W $U` 가 정확히 `CANON_LINES=157 CANON_SHA=c9e099aee5ca5df7` (시작 판 `bash $M/canon.sh $W $B` 와 같은 값, 봉인 전 실측). 판을 못 읽거나 4 요건 덩어리가 비면 `STOP` 과 종료 코드 2
    양성 대조: 시험 사본에서 `qa-evaluation-guide.md` 1260 줄 끝에 ` x` 를 붙여 커밋하면 `CANON_SHA=a0ce2330b3dde9c5` (e5333b7 판 canon.sh) · `CANON_SHA=ffe48414020e9638` (275e4fb 판 canon.sh) 로 달라진다 (봉인 전 실측). 4 요건 덩어리 895 줄 끝에 ` x` 를 붙여 커밋하면 `CANON_LINES=157 CANON_SHA=9511ba2e1c0acb5a` 로 달라진다 (275e4fb 판 canon.sh, 봉인 전 실측 — e5333b7 판은 이 변경을 못 잡았다)

## Architecture

- [ ] AR-01: `.harness` 밖에서 바뀐 파일은 전부 목록 L 안에 있다 — 목록 밖 파일 변경 0 개 [exact]
    측정: (Given 공통 전제 · 경로 `.` 에서 `.harness` 제외 · 생성물 없음(md 만 고친다) · 「포함」 관계 · 상한 `U`) `git diff --name-only $B $U -- . ':(exclude).harness' | grep -vxFf $W/$L | grep -c .` 이 `0`, 그리고 `git status --porcelain --untracked-files=all -- . ':(exclude).harness' | grep -c .` 이 `0`. 봉인 전 기준값 `0`
    양성 대조: 같은 명령을 `6378948 c3e45f3` 구간에 돌리면 `182` (봉인 전 실측)
- [ ] AR-02: `.harness/` 아래에서 바뀐 경로는 이 계약 · 개정 · 피드백 · notes 네 가지 뿐이다 — 다른 계약 · 개정 · 기록 파일 변경 0 개 [exact]
    측정: `git diff --name-only $B $U -- .harness | grep -vE '^\.harness/(sprint-(contract|amendments|feedback)-after-0926-mdlint-l4\.md|\.meta/after-kaizen-0926b/l4-notes\.md)$' | grep -c .` 이 `0`
    양성 대조: 같은 명령을 `c3e45f3 b90f348` 구간에 돌리면 `5` (봉인 전 실측)
- [ ] AR-03: `B..U` 구간의 커밋마다 담긴 파일의 맨 위 폴더가 정확히 하나다 (루트 파일 `README.md` · `CLAUDE.md` 는 각각 제 이름이 맨 위 폴더다) [exact]
    측정: `for c in $(git log --format=%H $B..$U); do git show --name-only --format= $c | cut -d/ -f1 | sort -u | grep -c .; done | grep -vxc 1` 이 `0` 이고, `git log --format=%H $B..$U | grep -c .` 이 `1` 이상(커밋이 있다)
    양성 대조: 커밋 `7038841` 에 같은 셈을 하면 `16` (봉인 전 실측)
- [ ] AR-04: `B..U` 구간의 커밋 메시지는 빈 줄을 뺀 마지막 줄이 정확히 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이다 [exact]
    측정: `for c in $(git log --format=%H $B..$U); do git log -1 --format=%B $c | sed '/^$/d' | tail -1; done | grep -vxFc 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>'` 이 `0`
    양성 대조: 커밋 `6378948` 의 마지막 줄은 서명 줄이 아니라 같은 셈이 `1` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
    측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0. 킷 밖 목록 파일(`.claude/` · `docs/superpowers/` · 루트 md)의 언어 없는 fence 는 SK-01 의 MD040 이 잰다 (시작 판 97 건)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
    측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0 (앞머리 자체의 불변은 SK-02 의 `FRONTMATTER=0` 이 잰다)

## Reusability

- [ ] RE-01: N/A (산출물이 md 모양 고침과 notes 뿐이라 재사용 단위 코드가 없다. 측정: `git diff --name-only $B $U -- . ':(exclude)*.md' ':(exclude).harness' | grep -c .` 이 0)
- [ ] RE-02: N/A (RE-01 과 같은 사유 — 새로 만든 컴포넌트 · 함수 · 모듈이 없다. 측정: RE-01 과 같은 명령이 0)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 대상이 이번 변경 파일에 없다. 측정: `git diff --name-only $B $U | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 목록 L 의 md 에 편집기 markdownlint 경고 0 건
    측정: SK-01 과 같은 명령 (`bash $M/lint.sh $W $W/$L | tail -1` 이 `LINTED=109 WARNINGS=0`). AUTO 블록 안 · 밖은 시작 판 0 · 1661 (리서치 소스)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 대상도 같은 파일이라 이번 변경 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (산출물이 md 문서뿐이라 구동할 앱 · 서버가 없다. 측정: RE-01 과 같은 명령이 0 — md · .harness 밖 변경 파일 0 개)
