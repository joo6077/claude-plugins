---
feature: "기존 마크다운 경고 정리 — design-kit 폴더 (l1)"
slug: after-0926-mdlint-l1
created: "2026-09-27 13:39"
complexity: "중간"
conditions: 17
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:c6273ee9b186048f
measurement_digest: sha256:e760f50a17c2d6c9
locked_at: "2026-09-27 13:48"
---

## 배경

공통 전제 (모든 조건): Given 구현 커밋 · notes 커밋이 가지 `chore/ak2-l1` 에 다 올라갔고, 작업 폴더 `R=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l1` 의
HEAD 가 그 가지 끝(`H`)이며 `git -C "$R" status --porcelain -- . ':(exclude).harness'` 가 빈 출력이다.
측정은 `TMPDIR=<빈 임시 폴더> bash "$R/.harness/.meta/after-0926-mdlint-l1/m.sh" <ID>` 로 돌리고, 출력이 조건에 적은 기대와 글자 그대로 같으면 PASS 다.
`m.sh` 는 시작 판 `B=90d07163b675cd4222b41c11d3a58b28c968976a`(목록 파일을 담은 커밋)와 가지 끝 `H`(`git rev-parse refs/heads/chore/ak2-l1`)를 각각 `git archive` 로 풀어 잰다.
`UNRESOLVED` · `STOP` 이 나오면 판정하지 않고 멈춘다.
측정 도구 지문(`shasum -a 256 <파일> | cut -c1-16`)이 아래와 다르면 어떤 조건도 판정하지 않는다:
`m.sh` `0c0d4d2e77e261bf` · `norm.py` `6a8aa9e9f075850e` (둘 다 `.harness/.meta/after-0926-mdlint-l1/`, 커밋 `16a890d`) ·
편집기와 같은 설정의 린트 실행기 `run.sh` `e1c237a6a876ad33` · 설정 `cfg.jsonc` `dfe13e2d516b31e5`
(둘 다 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint/`, markdownlint-cli2 0.23.2 · markdownlint 0.41.1 · MD013 끔) ·
로컬 CI 묶음 `ci-local.sh` `59fe55125c0dbc77` (`/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/`).

- 위임과 합의: 사용자 결정 UD-7 「범위 밖 기존 markdownlint 경고를 전부 고친다」(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`).
  위임 원문 시각 2026-09-26T10:30:16.222Z 「전부 고친다」 · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」(세션 `bda55d45-296c-491f-89ba-b52042d58e72`).
  이 계약의 합의는 이 위임으로 받은 것으로 적는다. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다 — 부모가 사용자에게 따로 묻는다
- 이 묶음(l1)의 대상: 작업 폴더에서 `git ls-files '*.md' | grep '^design-kit/'` 50 개 가운데 「고치지 않는 파일」 1 개를 뺀 49 개.
  목록은 `.harness/.meta/after-kaizen-0926b/l1-files.txt`(커밋 `90d0716`) 한 곳에만 있다. 조건은 이 파일을 가리키고 목록을 다시 적지 않는다
- 고치지 않는 파일과 까닭:
  - `design-kit/references/visual-change-protocol.md` — 시험 `design-kit/evals/decision-gate-test.sh:8` 이 `DOC=${DECISION_GATE_DOC:-$HERE/../references/visual-change-protocol.md}` 로 열어 §6 검사 코드를 떼어 돌린다
  - `.harness/` 아래 기존 파일 전부 — 봉인된 계약 기록이다. 이 계약이 새로 더하는 파일(계약 · 피드백 · 개정 · 측정 묶음 · notes)만 생긴다
  - 경로에 `evals/` 와 `fixture` 가 함께 든 design-kit md 는 0 개다(`git ls-files '*.md' | grep '^design-kit/' | grep -c fixture` = 0)
  - 이런 파일에는 경고를 끄는 주석도 넣지 않는다
- 판단 둘(위임으로 계약 작성자가 정했다)
  - 제목 단계를 바꿀지(MD025 · MD024 · MD036 · MD041 · MD001), 그 자리에만 좁혀 끌지는 구현자가 자리마다 정한다. 바꾸는 파일은 읽는 도구 grep 결과를 notes 에 남긴다(SK-04).
    레포 SKILL.md 가 `# Gotchas` · `# Process` · `# References` 를 맨 윗단계로 쓰는 관례(`grep -rnE "^#+ (Gotchas|Process|References)" --include=SKILL.md .` 실측: `# ` 215 줄 · `## ` 137 줄)라 둘 다 뜻을 해치지 않는다
  - 뜻 불변 판정은 「모양 표식을 떼고 낱말 순서가 같다」 로 기계가 잰다(SK-02). 떼는 표식은 `norm.py` 머리 설명에 있는 것뿐이다 — 빈 줄 · 줄 앞뒤 공백 · 코드 블록 언어 이름 · 줄 머리 번호 목록 숫자 · `#` `*` `|` `<` `>` · `-` 와 `:` 로만 된 낱말 · 좁힌 끄기 주석 한 줄

## GAP 분석 — 복잡도 · 설정 대조 · 편집 전 감사 · 시작 판 값

복잡도 네 축:

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 아니오 — md 문서 한 층(스킬 본문 · 참조 · 리서치 문서 · 틀) |
| 공개 판정 · 계약 변경 | 외부에 노출된 형태가 바뀌는가 | 아니오 — 모양만 고치고 문장 · 판정값을 바꾸지 않는다 |
| 소비면 존재 | 이 파일을 읽는 반대편이 있는가 | 예 — 스킬 로더(설치본), 사본 대조 `scripts/check-reviewer-protocol-copies.py:39`, 문서 사이트 드리프트 `scripts/detect-docs-drift.py:48`, 표 · 제목을 읽는 검사 스크립트 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 제목 단계 · 표 칸을 바꾸면 사본 대조 · 드리프트 · 평가 단언이 깨질 수 있다 |

→ 두 축이 예 — **중간**. 기능 조건은 9 개로 중간 가이드(4~8)를 하나 넘는다. 과제가 요구한 다섯 항목(경고 0 · 고치지 않는 파일 · 뜻 불변 · 검사 통과 · 끄기 주석 기록)에
범위 · 커밋 규칙 둘과 제목 · 끄기 효력 둘이 붙어서다. 스프린트를 나누면 같은 49 파일을 두 번 훑어야 해 나누지 않는다.

설정 리터럴 대조 (`.harness/project.yaml`):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 같은 값 (DG-03 N/A 사유) |
| `diagnostics.ide_exclude` | `[]` | `[]` — 편집기 맞춤법 검사(cSpell) 항목은 사용자 전역 규칙으로 뺀다 |
| `contract_categories` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns` | AP-01 · AP-02 · AP-03(`python3 scripts/validate-plugin.py --check=code-fence`) · AP-04(`python3 scripts/validate-plugin.py --check=frontmatter`) | AP-03 · AP-04 선별 — 코드 블록 언어를 넣고 SKILL.md 머리 근처를 고친다. AP-01(버전 하드코딩) · AP-02(force push)는 판 올림 · 푸시를 안 해 걸릴 자리가 없다 |

편집 전 감사 (읽은 파일과 줄):

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭 | 조건화 |
| --------- | ---------------------------- | -------------- | ------ |
| `design-kit/docs/design/**` 26 개 | `foundations/color.md:1-7` 머리에 `title: 컬러` 와 `# 컬러` 가 함께 있다 · `color.md:283-287` 맨 URL 다섯 | 머리 `title` 때문에 `:7` 이 MD025 (23 파일), MD034 5 | SK-01 · SK-04 |
| `design-kit/skills/*/SKILL.md` 8 개 | `design-audit/SKILL.md:13` `# Gotchas` · `:52` `# Process` · `:142` `# References` | 맨 윗단계 제목 셋이라 MD025 (7 파일 14 곳) | SK-01 · SK-04 |
| `design-kit/skills/design-test/SKILL.md` | `:1-14` 머리 뒤 첫 제목이 `## Gotchas` | MD041 1 | SK-01 · SK-04 |
| `design-kit/skills/design-concept/SKILL.md` | `:86` 번호 11 로 시작하는 목록 | MD029 1 | SK-02 (번호 숫자는 떼고 잰다) |
| `design-kit/skills/design-audit/templates/audit-report.md` | `:37` · `:48` 같은 제목 `[카테고리] 항목 제목` — 틀의 반복 자리 | MD024 2, 일부러 두 번 쓴 제목 | SK-03 · ER-01 |
| `design-kit/agents/design-reviewer.md` | 사본 대조 기준 `scripts/check-reviewer-protocol-copies.py:14-15` — 줄 앞 공백 · `>` · 빈 줄은 무시, 글자는 같아야 한다 | 경고 23 (MD022 · MD032 등) | SC-01 |
| `design-kit/README.md` | `:9-54` `<!-- AUTO:* -->` 블록 다섯 | 경고 0 (블록 안 0 · 밖 0) — 생성기 줄은 손대지 않는다 | SK-01 · SC-01 |
| `design-kit/references/visual-change-protocol.md` | `design-kit/evals/decision-gate-test.sh:8` 이 연다 | 고치지 않는 파일 | AR-01 |
| `scripts/run-evals.py` | `:52-56` SKILL.md · agent md 는 있는지만 본다 | 없음 — 내용 파싱 안 함 | SC-01 |
| `scripts/detect-docs-drift.py` | `:48` `design-kit/references/visual-change-protocol.md` · `:87` `spacing-layout.md` → 문서 페이지 매핑 | 원본이 바뀌면 드리프트 후보로 나온다 — 모양만 고쳐 페이지를 다시 만들 일은 없다 | 범위 경계 |

시작 판 값 (봉인 전, `B` = 가지 끝이던 때 실측 2026-09-27 13:3x):

```text
SK-01: list=49 list_diff=0 linted=49 warn=1966
  규칙별: MD060 1554 · MD032 160 · MD036 97 · MD022 50 · MD040 45 · MD025 37 · MD024 10 · MD031 6 · MD034 5 · MD041 1 · MD029 1
DG-02: list=49 list_diff=0 linted=49 warn=1966
SK-02: files=49 changed=0 mismatch=0 disables=0 missing=0 / rc=0 / lint_comments_added=0 narrow_added=0 wide_added=0
SK-03: disables=0 stated=NONE listed=0
SK-04: heading_changed_files=0 noted_with_grep=0
ER-01: disables=0 rule_pairs=0 effective=0
AR-01: excluded=1 excluded_touched=0 harness_modified=0
AR-02: changed=0 outside=0 harness_outside=0
AR-03: commits=2 multi_top=0 merges=0
SC-01: validate-plugin=0 sync-docs=0 sync-orchestrator=0 sync-evals=0 run-evals=0 run-kaizen-assertions=0 check-reviewer-protocol-copies=0 check-cause-table-copies=0 | ci_rc=0 ci_steps=25 ci_bad=0
AP-03: rc=0 bare=0 · AP-04: rc=0
```

대조 실측 (봉인 전, 세션 스크래치의 버리는 복제본 `l1-clone` — 작업 폴더와 다른 저장소):

- 자동 고침 탐침 — 복제본에서 목록 49 개에 `markdownlint-cli2 --fix` 만 돌려 커밋하면 `SK-01 warn=298`(MD060 108 · MD036 97 · MD040 45 · MD025 37 · MD024 10 · MD041 1) ·
  `SK-02 changed=46 mismatch=0 rc=0` · `AR-02 changed=46 outside=0`. 자동 고침은 뜻 검사를 통과하고, 남은 298 은 손으로 고칠 몫이다
- SK-01 음성 대조 — 시작 판 `warn=1966`. 아무것도 안 고치면 FAIL 한다
- SK-02 음성 대조 — 복제본에서 `color.md` 한 낱말(「심리학」→「철학」)을 바꾸면 `MISMATCH design-kit/docs/design/foundations/color.md at=9` · `mismatch=3`(아래 둘 포함) · `rc=1`.
  파일 전체 끄기 `<!-- markdownlint-disable MD060 -->` 를 넣으면 `wide_added=1` 과 `MISMATCH … motion.md`, 빈 HTML 주석 `<!-- -->` 를 더하면 `MISMATCH design-kit/README.md`
- SK-03 음성 대조 — 좁힌 끄기 주석 1 개를 넣고 notes 가 없으면 `disables=1 stated=NONE listed=0`, notes 의 줄 번호가 틀리면 `stated=1 listed=0`. 맞게 적으면 `disables=1 stated=1 listed=1`
- SK-04 음성 대조 — `# Process` 를 `## Process` 로 바꾸고 notes 가 없으면 `heading_changed_files=1 noted_with_grep=0`, 경로와 grep 결과를 적으면 `noted_with_grep=1`
- ER-01 음성 대조 — 경고가 없는 줄(`## Process`) 앞의 MD025 끄기는 `disables=1 rule_pairs=1 effective=0`, 진짜 MD025 줄(`# References`) 앞에 하나 더하면 `disables=2 rule_pairs=2 effective=1`
- AR-01 · AR-02 · AR-03 음성 대조 — `visual-change-protocol.md` 끝에 한 줄, `.harness/project.yaml` 끝에 한 줄, `scripts/` 새 파일과 `design-kit/README.md` 를 한 커밋에 넣으면
  `excluded_touched=1 harness_modified=1` · `outside=2 harness_outside=1` · `multi_top=2`
- SC-01 음성 대조 — 복제본에서 `design-kit/agents/design-reviewer.md:32` 사본 줄의 「마커는」 을 「표식은」 으로 바꾸면(적용 확인 `1 file changed`)
  `check-reviewer-protocol-copies.py` 종료 코드 1 · `violations=1`. 같은 검사가 `ci-local.sh` 의 `reviewer-copies` 단계에도 있어 `ci_bad` 가 1 이 된다
- 도구 준비 — `python3` = pyenv 3.14.3, markdownlint-cli2 0.23.2, `ci-local.sh` 는 `TMPDIR` 아래 `ci-local/summary.txt` 에 단계마다 `rc=` 를 적는다.
  yq 가 없어 `feedback-agg-test SKIP (yq 없음)` 한 줄이 늘 나오고, 그 줄 때문에 스크립트 끝 `grep -v 'rc=0'` 가 성공해 종료 코드가 0 이 된다 — 그래서 `ci_rc` 와 함께 `ci_bad`(SKIP 한 줄을 뺀 rc≠0 줄 수)를 잰다.
  `SC-01` 한 번에 약 5 분(실측 5:01)
- 세션 전용 도구 — 편집기와 같은 설정의 린트 실행기 `run.sh` · `cfg.jsonc` 는 이 세션 스크래치(`bda55d45-…/scratchpad/mdlint/`)에만 있다.
  `m.sh` 에서 이것을 부르는 조건은 `SK-01` · `DG-02` · `ER-01` 셋이다(`SC-01` 은 레포 검사 여덟과 커밋된 `ci-local.sh` 만 부른다).
  그래서 SK-01 · DG-02 · ER-01 은 이 기계 · 이 세션 스크래치가 남아 있을 때만 잴 수 있고, 스크래치가 없으면 공통 전제의 도구 지문 검사에서 멈춘다

## 범위 경계

```text
# sprint-scope
design-kit/*.md
```

- 위 블록은 커밋 직전 훅용이다. `design-kit/*.md` 는 고치지 않는 파일 `visual-change-protocol.md` 도 덮지만 AR-01 이 따로 막는다. 허용 경로의 정본은 목록 파일이다(AR-02)
- 이 계약은 모양만 고친다. 문장을 새로 쓰지 않으므로 톤 규칙(tone-kit)은 notes 의 새 문장에만 적용된다
- 킷 판 올림(`plugin.json`) · marketplace · 릴리스 · 푸시는 하지 않는다 — 부모가 합친 뒤 한다
- 문서 페이지(`docs/design-kit/*.html`)는 다시 만들지 않는다 — 원본의 모양만 바뀌어 페이지 내용이 달라지지 않는다. `detect-docs-drift.py` 가 후보로 내면 notes 「남은 것」 에 적는다
- 다른 묶음(l2 · l3a …)의 파일은 건드리지 않는다. 같은 폴더를 다른 가지(`chore/ak2-k2`)가 고친 것은 이미 기준 판에 합쳐져 있다(`git branch --contains` 로 확인)
- notes 경로는 `.harness/.meta/after-kaizen-0926b/l1-notes.md` 다. 여기에 `좁힌 끄기 주석: <수>` 한 줄, 끄기 주석마다 `경로:줄 규칙 까닭` 한 줄, 제목을 바꾼 파일마다 경로와 읽는 도구 grep 명령 · 결과를 적는다
- 커버리지 해소: SK-01 · SK-02 · SK-03 · SK-04 · ER-01 · AR-01 · AR-02 — 대상 49 경로는 `m.sh` 가 목록 파일(`.harness/.meta/after-kaizen-0926b/l1-files.txt`)을 읽어 돈다. 목록을 조건에 다시 적지 않는 것은 두 곳에 두지 않으려는 것이다
- 커버리지 해소: AR-01 — `m.sh AR-01` 이 `B..H` 구간을 쓰고, 제외 집합을 `H` 의 design-kit md 전체에서 목록 파일을 뺀 것으로 계산한다(지금 `design-kit/references/visual-change-protocol.md` 하나 — 출력 `excluded=1`).
  `.harness/` 는 `git diff --name-status B H -- .harness` 의 `A` 아닌 줄을 센다
- 커버리지 해소: SC-01 — 검사 여덟과 `ci-local.sh` 는 `m.sh` 의 `SC-01` 한 곳에 열거되고 출력에 이름이 그대로 나온다
- 느슨하게 하는 개정(대상 줄이기 · 뜻 검사의 떼는 표식 늘리기 · 문턱 낮추기)이 필요해지면 개정 파일에 동의 칸을 비워 적고 멈춘다

## 회귀 게이트

- 구현 중: 파일 몇 개를 고칠 때마다 `bash run.sh "$R" <그 파일 목록>` 과 `m.sh SK-02` 를 돌려 뜻 불변을 먼저 본다
- 커밋 전: `m.sh SK-01` · `SK-02` · `ER-01`
- 최종: 아래 조건 전부를 가지 끝에서

## Skill

- [ ] SK-01: Given 공통 전제, When 목록 파일의 49 개를 편집기와 같은 설정으로 잴 때, Then 경고가 0 건이고 목록 파일은 시작 판 그대로다 [exact, collective]
    측정: `bash m.sh SK-01` → `list=49 list_diff=0 linted=49 warn=0`
    뜻: list = 목록 줄 수, list_diff = `B..H` 에서 목록 파일이 바뀐 수, linted = markdownlint-cli2 의 `Linting: N file(s)` 수(검사기가 실제로 돌았다는 줄), warn = `run.sh <H 사본> <목록>` 출력 줄 수
    음성 대조: 시작 판 `warn=1966` — 고치지 않으면 FAIL
- [ ] SK-02: Given 공통 전제, When 목록 49 개의 시작 판과 가지 끝 판을 모양 표식을 떼고 비교할 때, Then 모든 파일의 낱말 순서가 같고, 새로 더한 markdownlint 주석은 모두 한 줄짜리 좁힌 끄기(`<!-- markdownlint-disable-next-line MDnnn -->`)다 [exact, collective]
    측정: `bash m.sh SK-02` → 끝 두 줄 `files=49 changed=<수> mismatch=0 disables=<수> missing=0` · `rc=0`, 셋째 줄 `lint_comments_added=<a> narrow_added=<a> wide_added=0` (a 는 두 칸이 같은 값)
    뜻: `MISMATCH` 줄이 하나라도 나오면 FAIL. 떼는 표식은 `norm.py` 머리 설명에 있는 것뿐이다
    음성 대조: 한 낱말 바꾸기 → `mismatch≥1 rc=1`, 파일 전체 끄기 주석 → `wide_added=1`, 빈 HTML 주석 → `MISMATCH`
- [ ] SK-03: Given 공통 전제, When 가지 끝의 좁힌 끄기 주석을 세고 notes 와 맞댈 때, Then notes 에 적힌 수가 실제 수와 같고 주석마다 `경로:줄` 과 규칙 번호와 까닭이 한 줄에 있다 [exact, enumerated]
    측정: `bash m.sh SK-03` → `disables=<n> stated=<n> listed=<n>` (세 값이 같다. 주석이 0 개면 `disables=0 stated=0 listed=0`)
    뜻: disables = 목록 파일 안 좁힌 끄기 줄 수, stated = notes 의 `좁힌 끄기 주석: N` 값, listed = `경로:줄`(가지 끝 판의 주석 줄 번호) 이 든 notes 줄 가운데 `MDnnn` 뒤에 까닭 글자가 있는 수
    음성 대조: notes 없음 → `stated=NONE`, 줄 번호 틀림 → `listed` 가 모자람
- [ ] SK-04: Given 공통 전제, When 코드 블록 밖 제목 줄이 시작 판과 달라진 파일을 셀 때, Then 그 파일마다 notes 에 경로와 제목을 읽는 도구를 찾은 grep 명령 · 결과가 있다 [exact, collective]
    측정: `bash m.sh SK-04` → `heading_changed_files=<k> noted_with_grep=<k>` (두 값이 같다)
    음성 대조: `# Process` → `## Process` 를 notes 없이 바꾸면 `noted_with_grep=0`

## Script

- [ ] SC-01: Given 공통 전제, When 레포 검사 여덟과 로컬 CI 묶음을 가지 끝 작업 폴더에서 돌릴 때, Then 모두 종료 코드 0 이고 CI 묶음 25 단계 가운데 rc≠0 단계가 없다 [exact, enumerated]
    측정: `bash m.sh SC-01` → ` validate-plugin=0 sync-docs=0 sync-orchestrator=0 sync-evals=0 run-evals=0 run-kaizen-assertions=0 check-reviewer-protocol-copies=0 check-cause-table-copies=0 | ci_rc=0 ci_steps=25 ci_bad=0`
    뜻: 차례대로 `python3 scripts/validate-plugin.py` · `scripts/sync-docs.py --check-only` · `scripts/sync-orchestrator.py --check-only` · `scripts/sync-evals.py --check-only` · `scripts/run-evals.py` ·
    `scripts/run-kaizen-assertions.py` · `scripts/check-reviewer-protocol-copies.py` · `scripts/check-cause-table-copies.py` 의 종료 코드, 그리고 `bash ci-local.sh <R>` 의 종료 코드 · 단계 수 · SKIP 한 줄을 뺀 실패 단계 수
    음성 대조: `design-reviewer.md:32` 사본 줄 한 낱말을 바꾸면 `check-reviewer-protocol-copies=1` · `ci_bad=1`

## Error

- [ ] ER-01: Given 공통 전제, When 좁힌 끄기 주석을 모두 지운 사본을 다시 잴 때, Then 주석마다 적힌 규칙의 경고가 바로 다음 줄에 실제로 나온다 — 쓸모없는 끄기 주석이 없다 [exact, collective]
    측정: `bash m.sh ER-01` → `disables=<n> rule_pairs=<p> effective=<p>` (rule_pairs 와 effective 가 같다)
    음성 대조: 경고 없는 줄 앞 끄기 → `rule_pairs=1 effective=0`

## Architecture

- [ ] AR-01: Given 공통 전제, When `B..H` 차이를 볼 때, Then 고치지 않는 파일(design-kit md 가운데 목록 밖 것 — 지금 `design-kit/references/visual-change-protocol.md` 하나)이 한 줄도 안 바뀌고, `.harness/` 아래 기존 파일은 수정 · 삭제 0 개다 [exact, enumerated]
    측정: `bash m.sh AR-01` → `excluded=1 excluded_touched=0 harness_modified=0`
    음성 대조: 제외 파일에 한 줄 · `.harness/project.yaml` 에 한 줄 → `excluded_touched=1 harness_modified=1`
- [ ] AR-02: Given 공통 전제, When `B..H` 에서 바뀐 경로를 모을 때, Then `.harness/` 밖 경로는 모두 목록 파일 안에 있고, `.harness/` 안 경로는 이 계약의 계약 · 피드백 · 개정 파일, `.harness/.meta/after-0926-mdlint-l1/` 아래, `.harness/.meta/after-kaizen-0926b/l1-notes.md` 뿐이다 [exact, collective]
    측정: `bash m.sh AR-02` → `changed=<수> outside=0 harness_outside=0`
    음성 대조: `scripts/` 새 파일 · 제외 파일 편집 → `outside=2`, `.harness/project.yaml` 편집 → `harness_outside=1`
- [ ] AR-03: Given 공통 전제, When `B..H` 의 병합 아닌 커밋을 하나씩 볼 때, Then 한 커밋이 맨 위 폴더를 둘 이상 싣지 않고 병합 커밋이 없다 [exact, collective]
    측정: `bash m.sh AR-03` → `commits=<수> multi_top=0 merges=0`
    음성 대조: `scripts/` 와 `design-kit/` 를 한 커밋에 → `multi_top=1`

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다
    측정: `bash m.sh AP-03` → `rc=0 bare=0` (가지 끝 사본에서 `python3 scripts/validate-plugin.py design-kit --check=code-fence`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
    측정: `bash m.sh AP-04` → `rc=0` (가지 끝 사본에서 `python3 scripts/validate-plugin.py design-kit --check=frontmatter`)

## Reusability

- [ ] RE-01: N/A (산출물이 md 문서 모양 고침뿐이라 재사용 단위 코드가 없다. 측정: `bash m.sh AR-02` 의 `outside=0` — 바뀐 경로가 목록의 md 뿐)
- [ ] RE-02: N/A (새로 만드는 컴포넌트 · 함수 · 모듈이 없다. 측정은 RE-01 과 같다)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git -C "$R" diff --name-only B H | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외, 맞춤법 검사 항목 제외) — 편집기 markdownlint 와 같은 설정으로 목록 49 개를 잰다
    측정: `bash m.sh DG-02` → `list=49 list_diff=0 linted=49 warn=0` (AUTO 블록이 있는 `design-kit/README.md` 는 시작 판에서 블록 안 0 · 밖 0)
- [ ] DG-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: DG-01 과 같은 명령)
- [ ] DG-04: N/A (산출물이 문서뿐이라 구동할 앱 · 서버가 없다. 측정: 바뀐 경로가 모두 `.md` — `m.sh AR-02` 의 `outside=0`)
