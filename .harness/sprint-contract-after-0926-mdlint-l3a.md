---
feature: "기존 마크다운 경고 정리 — bambu · reflect · rust · react · flutter · api 킷 (l3a)"
slug: after-0926-mdlint-l3a
created: "2026-09-27 13:49"
complexity: "복잡"
conditions: 20
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:d36d549d292f6e1e
measurement_digest: sha256:42aa4443e2a8a4be
locked_at: "2026-09-27 13:57"
---

## 배경

- 사용자 결정 UD-7(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`): 범위 밖 기존 markdownlint 경고를 전부 고친다. 위임 기록: 2026-09-26T10:30:16.222Z 「전부 고친다」 · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l3a` (가지 `chore/ak2-l3a`, 기준 `chore/after-kaizen-0926b` 의 c3e45f3). 모든 측정은 W 맨 위에서 돈다.
- 대상 목록 L = `.harness/.meta/after-kaizen-0926b/l3a-files.txt` (120 줄, 커밋 c08f56f). 만든 식: `git ls-files '*.md' | grep -E '^(bambu-kit|reflect-kit|rust-kit|react-kit|flutter-toolkit|api-kit)/'` 124 개에서 고치지 않는 파일 4 개를 뺐다.
- 고치지 않는 파일 4 개와 근거 (grep 으로 찾음):
  - `api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md` — 경로에 evals/ 와 fixture 가 함께 든다
  - `api-kit/skills/api-ui/SKILL.md` — `api-kit/evals/api-ui.spec.js:7` 이 열어 `## 7.` 절의 js 블록을 뽑는다
  - `bambu-kit/skills/bambu-print-profile/SKILL.md` — `bambu-kit/evals/run-gate-fixtures.sh:10` · `bambu-kit/evals/makerworld-fetch-test.sh:9` 가 열어 표와 실행 줄 · `### JSON 주소` 블록을 뽑는다
  - `flutter-toolkit/skills/flutter-scenario-report/references/record-format.md` — `flutter-toolkit/evals/scenario-report/test_build_report.py:22` 가 연다
  - 킷 안 다른 시험 스크립트 가운데 md 를 여는 것(`reflect-kit/evals/hooks/collect-status-test.sh` · `reflect-kit/evals/hooks/log-reflection-test.sh` · `flutter-toolkit/evals/hooks/format-edited-dart-test.sh`, `grep -ln '\.md'` 로 찾음)은 임시 폴더에 새로 만든 md 만 열어 목록과 겹치지 않는다
  - `.harness/` 아래는 전부 고치지 않는다(봉인된 계약 기록). 목록 식이 킷 폴더만 잡으므로 목록에 들지 않는다
- 공통 기호 (모든 조건이 이 뜻으로 쓴다. 명령은 `cd $W` 뒤에 돈다):
  - `W` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l3a`
  - `L` = `.harness/.meta/after-kaizen-0926b/l3a-files.txt`
  - `B` = `90685b9` (측정 묶음 커밋. 킷 폴더 파일은 c3e45f3 · c08f56f 와 같다)
  - `U` = `$(git rev-parse --verify -q chore/ak2-l3a) || exit 2` — 이 묶음 가지 끝. `HEAD` 를 상한으로 쓰지 않는다
  - `M` = `.harness/.meta/after-0926-mdlint-l3a` (측정 묶음: `lint.sh` · `meaning.py` · `ci.sh`, 커밋 90685b9)
  - `N` = `.harness/.meta/after-kaizen-0926b/l3a-notes.md` (구현이 만든다 — 끄기 주석과 제목 단계 변경의 자리와 이유)
  - `R` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint/run.sh`
- 공통 전제 (Given, 모든 조건에 한 번에 건다): 이 묶음의 커밋이 전부 끝났고, `git status --porcelain --untracked-files=all` 이 계약 자신의 `status:` 줄 말고 0 줄이다 (contract-schema.md 의 `dirty_except_status` 로 잰다). 뜻 · 범위 조건은 `B..U` 커밋 구간으로 재고, 경고 수는 작업 트리로 잰다.
- 측정 도구: markdownlint-cli2 0.23.2 (markdownlint 0.41.1), 설정 `cfg.jsonc` = `{ "config": { "MD013": false } }` (sha256 앞 16 자리 `dfe13e2d516b31e5`, 편집기 확장 기본값과 같음).
- 「뜻이 안 바뀜」 의 허용 모양 (meaning.py 가 떼는 것): 공백 · 빈 줄 · 표 구분 줄 · 코드 블록 여는 줄의 언어 · 제목 표식 `#` · 줄 전체를 감싼 강조 `**` · 빈 인용 줄 `>` · http(s)/ftp URL 꺾쇠 `<>` · `<!-- markdownlint-… -->` 주석. 이것 말고 한 글자라도 다르면 MISMATCH 다. 앞머리(frontmatter) 블록과 코드 블록 속 줄은 공백까지 같아야 한다.

## 리서치 소스

- 봉인 전 실측 (2026-09-27, 판 90685b9 작업 트리):
  - `bash $M/lint.sh $W $W/$L | tail -1` → `LINTED=120 WARNINGS=2241`. `bash $R $W $W/$L | grep -c .` → `2241`
  - 규칙별: MD060 1552 · MD032 260 · MD034 142 · MD031 53 · MD025 52 · MD022 49 · MD041 35 · MD033 30 · MD027 20 · MD036 17 · MD024 16 · MD038 8 · MD058 3 · MD028 2 · MD037 1 · MD012 1
  - 경고가 있는 파일 103 개 / 120 개. 고치지 않는 파일 4 개의 경고는 145 건(이 묶음 밖)
  - AUTO 블록 안 · 밖 (contract-schema §4 Diagnostics v5.7): README 5 개(`api-kit/README.md` · `flutter-toolkit/README.md` · `react-kit/README.md` · `reflect-kit/README.md` · `rust-kit/README.md`)에 AUTO 블록이 있다. 경고 2241 건 중 블록 안 0 · 밖 2241. 나눈 스크립트의 양성 대조: `api-kit/README.md:25`(블록 안) · `:53`(밖) 두 줄을 넣으면 `in_auto=1 out_auto=1`
  - 시험 사본(`git archive` 로 푼 판 + `--fix` 만 돌림): 경고 2241 → 220, `meaning.py` → `MISMATCH=1` (`rust-kit/skills/rust-auth/SKILL.md` — 따옴표 안 예시 전자우편 주소를 꺾쇠로 감쌌다. 뜻이 바뀌는 자동 고침이다), `ci.sh` → `CI_OK=28 CI_BAD=0 CI_SKIP=1`
  - `bash $M/ci.sh $W | tail -1` → `CI_OK=28 CI_BAD=0 CI_SKIP=1`
  - `python3 $M/meaning.py --selftest` → 11 경우 전부 OK, `SELFTEST PASS`
  - `python3 $M/meaning.py $W $B $B $W/$L | tail -1` → `CHECKED=120 MISMATCH=0 FRONTMATTER=0 CODEBLOCK=0 HEADING=0 DISABLE=0 BADDISABLE=0 NOTES_MISSING=0`

## GAP 분석

- 제목 단계를 읽는 도구 (grep 으로 찾음 — 목록 파일 제목을 바꿀 때 먼저 볼 곳): `scripts/check-cause-table-copies.py` 가 `## 실패 원인 가르기` 를 `flutter-toolkit/skills/flutter-preflight/SKILL.md` · `react-kit/skills/react-preflight/SKILL.md` 에서 읽는다. `scripts/check-reviewer-protocol-copies.py` 가 `## Canonical Unverified…` 사본을 `api-kit/agents/api-reviewer.md` · `react-kit/agents/react-reviewer.md` · `rust-kit/agents/rust-reviewer.md` · `flutter-toolkit/skills/flutter-audit/SKILL.md` 에서 대조한다. `scripts/detect-docs-drift.py` 가 `reflect-kit/docs/DESIGN.md` · `SCHEMA.md` · `RESEARCH.md` 를 본다. `scripts/run-evals.py` 가 각 킷 `evals/evals.json` 의 문구를 SKILL.md 에서 찾는다. `scripts/sync-docs.py` 가 SKILL.md 앞머리와 README AUTO 블록을 쓴다
- `validate-plugin.py` 는 `## Gotchas` → `# Gotchas` 같은 단계 변경을 못 잡는다 (시험 사본에서 rust-api SKILL.md 를 그렇게 바꿔도 rc=0). 그래서 SK-03 이 제목 변경을 따로 잰다
- MD041 35 건은 앞머리 뒤 첫 제목이 `## Gotchas` 인 SKILL.md 다. H1 을 새로 넣으면 낱말이 늘어 SK-02 가 막고, `# Gotchas` 로 올리면 제목을 읽는 도구가 깨질 수 있다 — 그 자리는 좁힌 끄기 주석이 맞는 모양이다
- MD033 30 건은 표 칸 속 `<br>` 다. 표 줄 사이에 `disable-next-line` 을 넣으면 표가 끊긴다 — 표 앞뒤를 `disable MD033` · `enable MD033` 짝으로 감싸는 것을 허용한다(파일 전체가 아니라 그 표만)
- ci-local.sh 의 종료 코드는 판정에 못 쓴다: 마지막 줄이 `grep -v 'rc=0' summary.txt` 라, yq 가 없는 이 맥에서는 SKIP 줄 때문에 늘 0 이고 모든 단계가 통과한 yq 설치 기계에서는 1 이다. 시작 판 실측 종료 코드 0. 그래서 SC-01 은 요약 줄로 잰다

## 범위 경계

```text
# sprint-scope
bambu-kit/
reflect-kit/
rust-kit/
react-kit/
flutter-toolkit/
api-kit/
```

- 위 블록은 커밋 직전 훅용이다. 폴더 안에서도 고칠 수 있는 파일은 목록 L 의 120 개뿐이고(AR-01), 고치지 않는 파일 4 개는 ER-01 이 잰다
- `.harness/` 아래에서 이 묶음이 바꿀 수 있는 경로: 이 계약 · `sprint-amendments-after-0926-mdlint-l3a.md` · `sprint-feedback-after-0926-mdlint-l3a.md` · `N`. 그 밖 `.harness/` 경로는 AR-02 가 막는다
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. 한 커밋에 맨 위 폴더 하나(킷 하나, 또는 `.harness` 하나). 메시지는 한국어, 끝 줄은 빈 줄 뒤 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` — 봉인 커밋도 같다. `git add -A` · `git stash` · push · 가지 바꾸기 금지
- 자동 고침은 `markdownlint-cli2 --config <cfg.jsonc> --fix` 를 목록 L 의 파일에만 돌린다(폴더 통째 금지). 자동 고침이 URL 이 아닌 것(전자우편 주소 등)을 꺾쇠로 감싸면 뜻이 바뀐다 — 되돌리고 그 줄에 `disable-next-line MD034` 를 쓴다
- 규칙을 지키면 뜻이 깨지는 자리(일부러 두 번 쓴 제목 · 원문 인용 · 첫 줄 `## Gotchas` · 표 칸 `<br>` 등)만 좁혀 끈다. 꼴은 ER-02, 기록은 ER-03
- 문장을 새로 쓰지 않는다. 톤 규칙은 문장을 새로 쓰는 자리에만 걸리므로 이 묶음에는 걸릴 자리가 없다 (notes 문장은 예외 — notes 는 설명 문장이다)
- 측정 묶음(`M` 의 세 파일)과 목록 L 은 봉인 뒤 바꾸지 않는다(SC-02). 바꿔야 하면 개정 파일에 쓴다
- `meaning.py` 는 notes `N` 이 없으면 안내 없이 파일 없음 오류로 멈춘다. 구현 중간에 SK-02 · SK-03 · ER-02 · ER-03 측정을 돌리기 전에 `N` 을 빈 파일로라도 먼저 만들어 둔다
- 커버리지 해소: ER-01 — 산문의 네 경로를 측정 절 끝 「대상:」 에 같은 표기로 다시 적었다
- 커버리지 해소: SC-02 — 네 파일 이름이 측정 절에 경로째 적혀 있다
- 오라클 해소: SK-03 — grep 은 문서 서술을 찾는 것이 아니라 `meaning.py` 를 실행해 나온 HEADING 자리를 notes 와 맞대는 것이다. 판정은 실행 출력으로 한다
- 오라클 해소: AR-04 — 커밋 메시지는 산출물 그 자체라 `git log` 로 실제 기록을 읽어 잰다

## 회귀 게이트

- 기존 검사 28 단계는 시작 판에서 전부 rc=0 이다(리서치 소스 실측). 이 묶음이 끝난 뒤에도 같아야 한다(SC-01)
- 이 계약이 안 보는 것: 목록 밖 md(harness · design-kit 등 다른 묶음)의 경고, 고치지 않는 파일 4 개의 경고 145 건

## Skill

- [ ] SK-01: 목록 L 의 120 개 파일에서 편집기와 같은 설정의 markdownlint 경고가 0 건이다 [exact]
    측정: `bash $M/lint.sh $W $W/$L | tail -1` 이 정확히 `LINTED=120 WARNINGS=0` 이고, `bash $R $W $W/$L | grep -c .` 이 `0`
    음성 대조: 시작 판(90685b9)에서 같은 두 명령이 `LINTED=120 WARNINGS=2241` · `2241` (봉인 전 실측). 검사기가 돌지 않으면 lint.sh 가 `STOP` 과 종료 코드 2 를 내므로 0 으로 새지 않는다
- [ ] SK-02: 목록 L 의 120 개 파일의 뜻이 시작 판과 같다 — 허용 모양(배경 절)을 떼고 공백을 지운 글자열이 같고, 앞머리 블록과 코드 블록 속 줄은 공백까지 같다 [exact]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 에서 `CHECKED=120` · `MISMATCH=0` · `FRONTMATTER=0` · `CODEBLOCK=0`
    음성 대조: 시험 사본에 `--fix` 만 돌린 판은 `MISMATCH=1` (rust-auth SKILL.md 의 전자우편 꺾쇠, 봉인 전 실측). `python3 $M/meaning.py --selftest` 의 낱말 바꿈 · 순서 바꿈 · 앞머리 들여쓰기 · 코드 속 들여쓰기 경우가 각각 1 을 낸다
- [ ] SK-03: 단계가 바뀌었거나 새로 생긴 제목마다 notes `N` 에 `- <경로>:<줄> … — <이유>` 줄이 있고, 그 줄에 제목 낱말을 찾은 grep 명령이 적혀 있다 [exact, enumerated]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N` 의 `HEADING <경로>:<줄>` 줄마다 같은 `경로:줄` 의 `NOTES_MISSING` 줄이 없고, `python3 $M/meaning.py $W $B $U $W/$L $W/$N | awk '/^HEADING /{print $2}' | while read -r k; do awk -v p="- $k " 'index($0,p)==1 && /grep/{f=1} END{exit !f}' $W/$N || echo "NOGREP $k"; done | grep -c .` 이 `0`. HEADING 이 0 줄이면 이 조건은 notes 없이 통과한다
    음성 대조: selftest 의 「notes 이유 없음」 · 「notes 다른 줄」 경우가 `NOTES_MISSING=1`

## Script

- [ ] SC-01: 검사 28 단계 `validate-plugin` · `sync-evals` · `sync-docs` · `sync-orchestrator` · `run-evals` · `contrast-claims` · `docs-links` · `stale-values` · `collector-test` · `react-detect-test` · `reflect-log-test` · `reflect-projid-test` · `reflect-collect-test` · `onboarding-gate-evals` · `howto-gate-evals` · `feedback-save-test` · `commit-guard-test` · `dart-format-hook-test` · `playwright-visuals` · `docs-a11y` · `scenario-report-ut` · `decision-gate-test` · `kaizen-assertions` · `reviewer-copies` · `api-ui-viewer` · `cause-table-copies` · `docs-drift-table` · `measure-helpers` 가 전부 rc=0 이다. `feedback-agg-test SKIP (yq 없음)` 줄은 허용한다 [exact, enumerated]
    측정: `bash $M/ci.sh $W | tail -1` 이 `CI_OK=28 CI_BAD=0 CI_SKIP=1` (yq 가 설치된 기계면 `CI_OK=29 CI_BAD=0 CI_SKIP=0`). 단계 이름 28 개는 같은 실행의 요약 줄(`ci.sh` 출력 앞부분)에 각각 `rc=0` 으로 나온다. ci-local.sh 자체의 종료 코드는 쓰지 않는다(GAP 분석 절)
    음성 대조: 시험 사본에서 `api-kit/README.md` 의 AUTO 블록 줄 하나(24 줄)를 고치면 `sync-docs --check-only` 가 rc=1 (봉인 전 실측) — 그 줄이 `CI_BAD` 로 잡힌다
- [ ] SC-02: 측정 묶음과 목록 파일이 봉인 뒤 바뀌지 않았다 — `.harness/.meta/after-0926-mdlint-l3a/lint.sh` · `.harness/.meta/after-0926-mdlint-l3a/meaning.py` · `.harness/.meta/after-0926-mdlint-l3a/ci.sh` · `.harness/.meta/after-kaizen-0926b/l3a-files.txt` [exact, enumerated]
    측정: `shasum -a 256 <파일> | cut -c1-16` 이 차례로 `.harness/.meta/after-0926-mdlint-l3a/lint.sh` `241f16dba9687ed9` · `.harness/.meta/after-0926-mdlint-l3a/meaning.py` `03347080caf6f1d7` · `.harness/.meta/after-0926-mdlint-l3a/ci.sh` `e647283b66f8df0c` · `.harness/.meta/after-kaizen-0926b/l3a-files.txt` `79abd647261d8e33`, 그리고 `wc -l < $W/$L` 이 `120`

## Error

- [ ] ER-01: 고치지 않는 파일 4 개 `api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md` · `api-kit/skills/api-ui/SKILL.md` · `bambu-kit/skills/bambu-print-profile/SKILL.md` · `flutter-toolkit/skills/flutter-scenario-report/references/record-format.md` 가 한 줄도 바뀌지 않았다 — 끄기 주석도 없다 [exact, enumerated]
    측정: `git diff --name-only $B $U -- api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md api-kit/skills/api-ui/SKILL.md bambu-kit/skills/bambu-print-profile/SKILL.md flutter-toolkit/skills/flutter-scenario-report/references/record-format.md | grep -c .` 이 `0` 이고, 같은 네 경로에 `git status --porcelain --` 가 0 줄 (대상: `api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md` · `api-kit/skills/api-ui/SKILL.md` · `bambu-kit/skills/bambu-print-profile/SKILL.md` · `flutter-toolkit/skills/flutter-scenario-report/references/record-format.md`)
    양성 대조: 시험 사본에서 `bambu-kit/skills/bambu-print-profile/SKILL.md` 끝에 빈 줄 하나를 더해 커밋하면 같은 diff 명령이 `1` (봉인 전 실측)
- [ ] ER-02: 새로 넣은 markdownlint 주석은 전부 규칙 번호가 적힌 `disable-next-line` 이거나, 같은 규칙의 `enable` 이 뒤에 오는 `disable` · 그 짝 `enable` 이다 — `disable-file` · `configure-file` · 규칙 없는 끄기 · 짝 없는 `disable` 은 0 개 [exact]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 의 `BADDISABLE=0`
    양성 대조: selftest 의 「짝 없는 disable」 · 「파일 전체 끄기」 경우가 각각 `BADDISABLE=1`
- [ ] ER-03: notes `N` 에 `끄기 주석 수: <n>` 줄이 정확히 하나 있고 n 이 새로 넣은 주석 수와 같으며, 새 주석마다 `- <경로>:<줄> <규칙> — <이유>` 줄이 있다 [exact]
    측정: `grep -cE '^끄기 주석 수: [0-9]+$' $W/$N` 이 `1` · 그 수가 `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 의 `DISABLE=` 값과 같음 · 같은 끝 줄의 `NOTES_MISSING=0`
    음성 대조: selftest 의 「notes 이유 없음」 · 「notes 다른 줄」 경우가 `NOTES_MISSING=1`

## Architecture

- [ ] AR-01: 킷 폴더에서 바뀐 파일은 전부 목록 L 안에 있다 — 목록 밖 파일 변경 0 개 [exact]
    측정: (Given 공통 전제 · 경로 `.` 에서 `.harness` 제외 · 생성물 없음(md 만 고친다) · 「포함」 관계 · 상한 `U`) `git diff --name-only $B $U -- . ':(exclude).harness' | grep -vxFf $W/$L | grep -c .` 이 `0`, 그리고 `git status --porcelain --untracked-files=all -- . ':(exclude).harness' | grep -c .` 이 `0`. 봉인 전 기준값 `0`
    양성 대조: 같은 명령을 `6378948 c3e45f3` 구간에 돌리면 `177` (봉인 전 실측)
- [ ] AR-02: `.harness/` 아래에서 바뀐 경로는 이 계약 · 개정 · 피드백 · notes 네 가지 뿐이다 — 다른 계약 · 개정 · 기록 파일 변경 0 개 [exact]
    측정: `git diff --name-only $B $U -- .harness | grep -vE '^\.harness/(sprint-(contract|amendments|feedback)-after-0926-mdlint-l3a\.md|\.meta/after-kaizen-0926b/l3a-notes\.md)$' | grep -c .` 이 `0`
    양성 대조: 같은 명령을 `c3e45f3 90685b9` 구간에 돌리면 `4` (봉인 전 실측)
- [ ] AR-03: `B..U` 구간의 커밋마다 담긴 파일의 맨 위 폴더가 정확히 하나다 [exact]
    측정: `for c in $(git log --format=%H $B..$U); do git show --name-only --format= $c | cut -d/ -f1 | sort -u | grep -c .; done | grep -vxc 1` 이 `0` 이고, `git log --format=%H $B..$U | grep -c .` 이 `1` 이상(커밋이 있다)
    양성 대조: 커밋 `7038841` 에 같은 셈을 하면 `16` (봉인 전 실측)
- [ ] AR-04: `B..U` 구간의 커밋 메시지는 빈 줄을 뺀 마지막 줄이 정확히 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이다 [exact]
    측정: `for c in $(git log --format=%H $B..$U); do git log -1 --format=%B $c | sed '/^$/d' | tail -1; done | grep -vxFc 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>'` 이 `0`
    양성 대조: 커밋 `6378948` 의 마지막 줄은 `release: 13 킷 (카이젠 뒤 이어질 것 2026-09-26)` 이라 같은 셈이 `1` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
    측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
    측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0 (앞머리 자체의 불변은 SK-02 의 `FRONTMATTER=0` 이 잰다)

## Reusability

- [ ] RE-01: N/A (산출물이 md 모양 고침과 notes 뿐이라 재사용 단위 코드가 없다. 측정: `git diff --name-only $B $U -- . ':(exclude)*.md' ':(exclude).harness' | grep -c .` 이 0)
- [ ] RE-02: N/A (RE-01 과 같은 사유 — 새로 만든 컴포넌트 · 함수 · 모듈이 없다. 측정: RE-01 과 같은 명령이 0)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 대상이 이번 변경 파일에 없다. 측정: `git diff --name-only $B $U | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 목록 L 의 md 에 편집기 markdownlint 경고 0 건
    측정: SK-01 과 같은 명령 (`bash $M/lint.sh $W $W/$L | tail -1` 이 `LINTED=120 WARNINGS=0`). AUTO 블록 안 · 밖은 시작 판 0 · 2241 (리서치 소스)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 대상도 같은 파일이라 이번 변경 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (산출물이 md 문서뿐이라 구동할 앱 · 서버가 없다. 측정: RE-01 과 같은 명령이 0 — md · .harness 밖 변경 파일 0 개)
