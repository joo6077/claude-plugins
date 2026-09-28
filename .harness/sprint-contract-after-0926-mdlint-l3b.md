---
feature: "기존 마크다운 경고 정리 — backend · infra · planning · tone · howto · onboarding 킷과 루트 밖 기타 (l3b)"
slug: after-0926-mdlint-l3b
created: "2026-09-27 14:49"
complexity: "복잡"
conditions: 21
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:a83801884f4bbe77
measurement_digest: sha256:2dcf946ef53a46d5
locked_at: "2026-09-27 14:57"
---

## 배경

- 사용자 결정 UD-7(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`): 범위 밖 기존 markdownlint 경고를 전부 고친다. 위임 기록: 2026-09-26T10:30:16.222Z 「전부 고친다」 · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 (세션 bda55d45-296c-491f-89ba-b52042d58e72). 사용자에게 묻지 않는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l3b` (가지 `chore/ak2-l3b`, 기준 `chore/after-kaizen-0926b` 의 c3e45f3). 모든 측정은 W 맨 위에서 돈다.
- 대상 목록 L = `.harness/.meta/after-kaizen-0926b/l3b-files.txt` (67 줄, 커밋 de8c8cd). 만든 식: `git ls-files '*.md' | grep -v '^\.harness/' | grep -vE '^(design-kit|docs|bambu-kit|reflect-kit|rust-kit|react-kit|flutter-toolkit|api-kit|harness|\.claude|scripts)/' | grep -vE '^(README|CLAUDE)\.md$'` 95 개에서 고치지 않는 파일 28 개를 뺐다. 95 개는 전부 여섯 킷 안이다(backend-kit 10 · howto-kit 25 · infra-kit 13 · onboarding-kit 14 · planning-kit 14 · tone-kit 19) — 루트 밖 기타 md 는 이 식에 0 개다.
- 고치지 않는 파일 28 개와 근거 (grep 으로 찾음):
  - 경로에 evals/ 와 fixture 가 함께 든 24 개: `howto-kit/evals/fixtures/` 아래 15 개(`edge-empty.md` · `edge-zero-steps.md` · `fail-g3-domainmix.md` · `fail-g4-deprecation-ko.md` · `fail-g4-korean-abolish-unsourced.md` · `fail-g4-korean-delete-unsourced.md` · `fail-g4-korean-shutdown-unsourced.md` · `fail-g5-nonterminal.md` · `fail-g6-granularity.md` · `pass-fcm-ios.md` · `pass-g4-completion-phrase-not-deprecation.md` · `pass-g4-delete-action-not-deprecation.md` · `pass-g4-korean-delete-sourced.md` · `pass-g4-korean-sourced.md` · `pass-g4-retention-notice-not-deprecation.md`)와 `onboarding-kit/skills/setup-guide/evals/fixtures/` 아래 9 개(`gate-blocking-ok.md` · `gate-fail-blocking-empty.md` · `gate-fail-blocking-nourl.md` · `gate-fail-ledger-double-source.md` · `gate-fail-ledger-marker-swift.md` · `gate-fail-ledger-misplaced.md` · `gate-g4-ko-sourced.md` · `gate-g4-ko-unsourced.md` · `gate-ok-flutter.md`). 두 폴더에는 md 말고 파일이 없다(`git ls-files … | grep -vc '\.md$'` → 0)
  - `onboarding-kit/skills/setup-guide/SKILL.md` — `onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh:10` 이 열어 `guide_gate() {` 함수를 뽑아 돌린다
  - `howto-kit/README.md` · `howto-kit/skills/howto-audit/SKILL.md` · `howto-kit/skills/howto-doc/SKILL.md` — `howto-kit/evals/run-evals.sh:131~160` 이 킷 안 md 의 `bash` 울타리 가운데 `howto_gate` 를 부르는 블록을 뽑아 zsh · bash 로 돌리고, 수를 `howto-kit/evals/evals.json` 의 `gate_blocks`(`{'README.md': 1, 'skills/howto-audit/SKILL.md': 1, 'skills/howto-doc/SKILL.md': 2}`)와 맞댄다. `grep -rlE 'howto_gate' howto-kit --include='*.md' | grep -v evals/` 이 이 세 파일을 낸다
  - 킷 안 나머지 시험 스크립트: `howto-kit/scripts/howto-gate.sh` 는 `step-contract.md` 를 주석으로만 가리키고 열지 않는다. `scripts/check-reviewer-protocol-copies.py` 가 `backend-kit/agents/backend-reviewer.md` · `howto-kit/agents/howto-reviewer.md` · `infra-kit/agents/infra-reviewer.md` · `planning-kit/agents/planning-reviewer.md` 를 열지만 공백 · 인용 표식 · 빈 줄을 떼고 맞대므로(그 파일 머리말) 모양 고침과 부딪히지 않는다 — 목록에 남기고 SC-01 의 `reviewer-copies` 단계가 잰다
  - `.harness/` 아래는 전부 고치지 않는다(봉인된 계약 기록). 목록 식이 `.harness/` 를 빼므로 목록에 들지 않는다
- 공통 기호 (모든 조건이 이 뜻으로 쓴다. 명령은 `cd $W` 뒤에 돈다):
  - `W` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l3b`
  - `L` = `.harness/.meta/after-kaizen-0926b/l3b-files.txt`
  - `B` = `de8c8cd` (측정 묶음 · 목록 커밋. 킷 폴더 파일은 c3e45f3 과 같다)
  - `U` = `$(git rev-parse --verify -q chore/ak2-l3b) || exit 2` — 이 묶음 가지 끝. `HEAD` 를 상한으로 쓰지 않는다
  - `M` = `.harness/.meta/after-0926-mdlint-l3b` (측정 묶음: `lint.sh` · `meaning.py` · `ci.sh`, 커밋 de8c8cd)
  - `N` = `.harness/.meta/after-kaizen-0926b/l3b-notes.md` (구현이 만든다 — 끄기 주석과 제목 단계 변경의 자리와 이유)
  - `R` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint/run.sh`
  - `CL` = `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`
- 공통 전제 (Given, 모든 조건에 한 번에 건다): 이 묶음의 커밋이 전부 끝났고, `git status --porcelain --untracked-files=all` 이 계약 자신의 `status:` 줄 말고 0 줄이다 (contract-schema.md 의 `dirty_except_status` 로 잰다). 뜻 · 범위 조건은 `B..U` 커밋 구간으로 재고, 경고 수는 작업 트리로 잰다.
- 측정 도구: markdownlint-cli2 0.23.2, 설정 `cfg.jsonc` = `{ "config": { "MD013": false } }` (편집기 확장 기본값과 같음). `lint.sh` 와 `ci.sh` 는 l3a 묶음을 옮겨 왔다(`ci.sh` 는 임시 폴더 이름 `l3a-ci` → `l3b-ci` 한 줄만 다르다).
- `meaning.py` 는 l3a 판에 네 가지를 더했다 — l3a 독립 검토가 찾은 자동 고침 뜻 바뀜을 옛 판이 못 잡았기 때문이다:
  - `SPACING` — 공백을 다 지우면 같아도, 줄 안 공백을 한 칸으로 줄이고 `|` `[` `]` 옆 공백만 뗀 글줄이 다르면 잡는다 (코드 조각 속 공백 `` `^## ` `` → `` `^##` `` · 강조 표식 옆 공백 `modules/* + shared/*`)
  - `QUOTEJOIN` — 코드 블록 밖 인용 덩어리 수가 줄면 잡는다 (빈 줄을 `>` 로 채워 따로이던 인용 둘이 하나가 됨)
  - `BADANGLE` — 새로 감싼 URL 꺾쇠 안에 주소가 아닌 글자(한글 · 짝 없는 닫는 괄호 · 끝 문장부호)가 들면 잡는다 (`(<https://…/)을>`)
  - 끄기 주석 종류를 긴 이름부터 맞춘다 — l3a 판은 `disable-next-line` 을 `disable` 로 읽어 「규칙 번호 없음」 으로 잘못 잡았다(l3a-notes 「측정 도구 결함」)
- 「뜻이 안 바뀜」 의 허용 모양 (meaning.py 가 떼는 것): 공백 · 빈 줄 · 표 구분 줄 · 코드 블록 여는 줄의 언어 · 제목 표식 `#` · 줄 전체를 감싼 강조 `**` · 빈 인용 줄 `>` · http(s)/ftp URL 꺾쇠 `<>` · `<!-- markdownlint-… -->` 주석. 이것 말고 한 글자라도 다르면 MISMATCH 다. 앞머리 블록과 코드 블록 속 줄은 공백까지 같아야 한다. 목록 번호(MD029 자동 고침의 `4.` → `1.`)는 허용 모양이 아니다.

## 리서치 소스

- 봉인 전 실측 (2026-09-27, 판 de8c8cd 작업 트리):
  - `bash $M/lint.sh $W $W/$L | tail -1` → `LINTED=67 WARNINGS=965`. `bash $R $W $W/$L | grep -c .` → `965`
  - 규칙별: MD060 818 · MD032 46 · MD025 42 · MD022 27 · MD034 9 · MD058 8 · MD031 4 · MD041 3 · MD037 2 · MD036 2 · MD028 2 · MD038 1 · MD029 1
  - 경고가 있는 파일 52 개 / 67 개. 고치지 않는 파일 28 개의 경고는 45 건(`bash $R $W <28 개 목록>`, 이 묶음 밖)
  - AUTO 블록 안 · 밖 (contract-schema §4 Diagnostics): 목록 안 README 3 개(`onboarding-kit/README.md` · `planning-kit/README.md` · `tone-kit/README.md`)에 AUTO 블록이 있다. 경고 965 건 중 블록 안 0 · 밖 965. 나눈 스크립트의 양성 대조: `tone-kit/README.md:35`(블록 안) · `:14`(밖) 두 줄을 넣으면 `in_auto=1 out_auto=1`
  - 시험 사본(`git archive de8c8cd` 로 푼 판 + 목록 L 에만 `--fix`): 경고 965 → 95, `meaning.py` → `MISMATCH=1 SPACING=1` — `tone-kit/skills/tone-guide/SKILL.md` 의 목록 번호 `4.` → `1.`(MD029, 뜻이 바뀌는 자동 고침), `infra-kit/skills/infra-audit/SKILL.md` 의 `*.yml, *.yaml` → `*.yml,*.yaml`(MD037, 공백이 뜻의 일부). 목록 밖 파일 변경 0. `ci.sh` → `CI_OK=28 CI_BAD=0 CI_SKIP=1`
  - `bash $M/ci.sh $W | tail -1` → `CI_OK=28 CI_BAD=0 CI_SKIP=1` (약 5 분)
  - `TMPDIR=<임시> bash $CL $W; echo $?` → `0`
  - `python3 $M/meaning.py --selftest` → 19 경우 전부 OK, `SELFTEST PASS`
  - `python3 $M/meaning.py $W $B $B $W/$L <빈 notes> | tail -1` → `CHECKED=67 MISMATCH=0 SPACING=0 QUOTEJOIN=0 BADANGLE=0 FRONTMATTER=0 CODEBLOCK=0 HEADING=0 DISABLE=0 BADDISABLE=0 NOTES_MISSING=0`
  - 알려진 답 (새 검사 셋): l3a 작업 폴더에서 `python3 $M/meaning.py . 90685b9 7a57927 .harness/.meta/after-kaizen-0926b/l3a-files.txt` (독립 검토 전 판) → `SPACING=5 QUOTEJOIN=2 BADANGLE=1` — l3a 가 뒤 커밋 31ab876 · 440fe5e · 36c191d · 2d2a7ff 로 되돌린 자리(api-probe · api-verify `Bearer ` · react-audit `^export default ` · codex-kaizen · rust-init `modules/*` · bambu user-preferences 인용 · flutter-error 인용 · react-animation APG 꺾쇠)와 파일이 맞는다. 되돌린 뒤 판 e46e280 → `SPACING=0 QUOTEJOIN=0 BADANGLE=0`, 그리고 120 파일에서 새 검사가 잘못 잡은 것 0
  - 봉인 전 측정 묶음 지문(`shasum -a 256 | cut -c1-16`): `lint.sh` `241f16dba9687ed9` · `meaning.py` `c86f51a872340f16` · `ci.sh` `5db585eaf378130c` · `l3b-files.txt` `cfb155b0a09756fe`

## GAP 분석

- 제목 단계를 읽는 도구 (grep 으로 찾음 — 목록 파일 제목을 바꿀 때 먼저 볼 곳): `scripts/sync-docs.py:215~222` 가 각 킷 `references/*.md` 의 첫 `# ` 줄을 README AUTO:references 표 설명으로 옮긴다 — `tone-kit/references/*.md` 의 첫 H1 을 바꾸면 README 가 어긋나 `sync-docs --check-only` 가 실패한다. `scripts/check-reviewer-protocol-copies.py` 가 reviewer 사본 네 개(배경 절)에서 `1. **마커는` 조항 덩어리와 4 요건 덩어리를 찾는다. `scripts/detect-docs-drift.py` 가 `infra-kit/skills/infra-test/SKILL.md` · `onboarding-kit/…` 와 docs 페이지 짝을 본다. `scripts/run-evals.py` 는 SKILL.md 가 있는지만 본다. `scripts/validate-plugin.py` 는 앞머리를 읽는다
- MD025 42 건은 planning-kit SKILL.md 12 개 · planning-reviewer 가 `# Gotchas` · `# Process` · `# References` 를 H1 으로 여럿 쓰고, 일부(plan-prd 64 · 97 · 124 줄)는 코드 블록이 아닌 본문에 산출물 틀의 H1 을 싣는다. 단계를 바꾸려면 먼저 그 제목 낱말을 grep 으로 찾고 notes 에 적는다(SK-03). 틀 예시처럼 H1 이어야 뜻이 사는 자리는 좁혀 끈다
- MD041 3 건은 앞머리 뒤 첫 줄이 `## Gotchas` 이거나 본문 문장인 SKILL.md 다(backend-test · infra-test · howto). H1 을 새로 넣으면 낱말이 늘어 SK-02 가 막는다 — 좁힌 끄기 주석이 맞는 모양이다
- MD029 1 건(`tone-kit/skills/tone-guide/SKILL.md:89`)은 자동 고침이 번호를 바꿔 뜻이 바뀐다 — 번호를 그대로 두고 좁혀 끈다. MD037 2 건 · MD038 1 건 · MD028 2 건은 자동 고침이 공백 · 인용 경계를 바꿀 수 있다 — `meaning.py` 의 SPACING · QUOTEJOIN 이 잡는다
- MD033 은 이 목록에 0 건이다. 표 안에 끄기 주석을 넣어야 하면 표 줄 사이에 `disable-next-line` 을 넣지 말고(표가 끊긴다) 표 앞뒤를 같은 규칙의 `disable` · `enable` 짝으로 감싼다
- ci-local.sh 의 종료 코드는 판정력이 약하다: 마지막 줄이 `grep -v 'rc=0' summary.txt` 라, yq 가 없는 이 맥에서는 SKIP 줄 때문에 늘 0 이다(l3a GAP 분석과 같다). 사용자 전달 조건이라 SC-03 으로 두되 판정은 SC-01 의 요약 줄로 한다
- `validate-plugin.py` 는 `## Gotchas` → `# Gotchas` 같은 단계 변경을 못 잡는다(l3a 실측). 그래서 SK-03 이 제목 변경을 따로 잰다
- 봉인 전 교차 진단(qa-evaluator, 2026-09-27): 막을 결함 0 건. `check-reviewer-protocol-copies.py` · `check-cause-table-copies.py` 가 맞대는 덩어리는 조항 본문 목록 줄부터라 `planning-reviewer.md` 의 H1 을 H2 로 낮춰도 부딪히지 않는다고 실측했다. 그 제목 단계 변경은 SK-03 절차(grep 먼저 · notes 기록)로 다룬다

## 범위 경계

```text
# sprint-scope
backend-kit/
infra-kit/
planning-kit/
tone-kit/
howto-kit/
onboarding-kit/
```

- 위 블록은 커밋 직전 훅용이다. 폴더 안에서도 고칠 수 있는 파일은 목록 L 의 67 개뿐이고(AR-01), 고치지 않는 파일 28 개는 ER-01 이 잰다
- `.harness/` 아래에서 이 묶음이 바꿀 수 있는 경로: 이 계약 · `sprint-amendments-after-0926-mdlint-l3b.md` · `sprint-feedback-after-0926-mdlint-l3b.md` · `N`. 그 밖 `.harness/` 경로는 AR-02 가 막는다
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. 한 커밋에 맨 위 폴더 하나(킷 하나, 또는 `.harness` 하나). 메시지는 한국어, 끝 줄은 빈 줄 뒤 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` — 봉인 커밋도 같다. `git add -A` · `git stash` · push · 가지 바꾸기 금지
- 자동 고침은 `markdownlint-cli2 --config <cfg.jsonc> --fix` 를 목록 L 의 파일에만 돌린다(폴더 통째 금지). 자동 고침 뒤 `meaning.py` 를 돌려 MISMATCH · SPACING · QUOTEJOIN · BADANGLE 자리를 시작 판 글자로 되돌리고 그 줄만 좁혀 끈다
- 규칙을 지키면 뜻이 깨지는 자리(일부러 두 번 쓴 제목 · 원문 인용 · 첫 줄 `## Gotchas` · 목록 번호 · 코드 조각 속 공백 등)만 좁혀 끈다. 꼴은 ER-02, 기록은 ER-03. 파일 전체를 끄는 주석 금지
- 문장을 새로 쓰지 않는다. 톤 규칙은 문장을 새로 쓰는 자리에만 걸리므로 이 묶음의 md 에는 걸릴 자리가 없다 (notes 문장은 예외 — notes 는 설명 문장이다)
- 측정 묶음(`M` 의 세 파일)과 목록 L 은 봉인 뒤 바꾸지 않는다(SC-02). 바꿔야 하면 개정 파일에 쓴다
- `meaning.py` 는 notes `N` 이 없으면 파일 없음 오류로 멈춘다. 구현 중간에 SK-02 · SK-03 · ER-02 · ER-03 측정을 돌리기 전에 `N` 을 빈 파일로라도 먼저 만들어 둔다
- 가짜 도구가 필요하면 scratch 에 새 일반 파일로만 만든다. `~/.pyenv` · `/opt/homebrew` · `/usr` · `~/.local` 아래에 쓰지 않는다
- 커버리지 해소: ER-01 — 측정 pathspec 의 두 폴더(`howto-kit/evals/fixtures` · `onboarding-kit/skills/setup-guide/evals/fixtures`)를 펼친 24 개 이름을 조건 산문과 배경 절에 같은 표기로 적었다
- 커버리지 해소: SC-02 — 네 파일 이름이 측정 절에 경로째 적혀 있다
- 오라클 해소: SK-03 — `meaning.py` 를 실행해 나온 HEADING 자리를 notes 와 맞댄다. 판정은 실행 출력으로 한다
- 오라클 해소: AR-04 — 커밋 메시지는 산출물 그 자체라 `git log` 로 실제 기록을 읽어 잰다

## 회귀 게이트

- 기존 검사 28 단계는 시작 판에서 전부 rc=0 이다(리서치 소스 실측). 이 묶음이 끝난 뒤에도 같아야 한다(SC-01)
- 이 계약이 안 보는 것: 목록 밖 md(harness · design-kit · docs 등 다른 묶음)의 경고, 고치지 않는 파일 28 개의 경고 45 건

## Skill

- [ ] SK-01: 목록 L 의 67 개 파일에서 편집기와 같은 설정의 markdownlint 경고가 0 건이다 [exact]
    측정: `bash $M/lint.sh $W $W/$L | tail -1` 이 정확히 `LINTED=67 WARNINGS=0` 이고, `bash $R $W $W/$L | grep -c .` 이 `0`
    음성 대조: 시작 판(de8c8cd)에서 같은 두 명령이 `LINTED=67 WARNINGS=965` · `965` (봉인 전 실측). 검사기가 돌지 않으면 lint.sh 가 `STOP` 과 종료 코드 2 를 내므로 0 으로 새지 않는다
- [ ] SK-02: 목록 L 의 67 개 파일의 뜻이 시작 판과 같다 — 허용 모양(배경 절)을 떼고 공백을 지운 글자열이 같고, 줄 안 공백의 뜻(코드 조각 · 강조 옆)과 인용 덩어리 수가 같고, 새 URL 꺾쇠 안에 주소 밖 글자가 없고, 앞머리 블록과 코드 블록 속 줄은 공백까지 같다 [exact]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 에서 `CHECKED=67` · `MISMATCH=0` · `SPACING=0` · `QUOTEJOIN=0` · `BADANGLE=0` · `FRONTMATTER=0` · `CODEBLOCK=0`
    음성 대조: 시험 사본에 `--fix` 만 돌린 판은 `MISMATCH=1 SPACING=1` (tone-guide 목록 번호 · infra-audit `*.yml, *.yaml`, 봉인 전 실측). l3a 독립 검토 전 판(90685b9..7a57927)은 `SPACING=5 QUOTEJOIN=2 BADANGLE=1`. `python3 $M/meaning.py --selftest` 의 낱말 바꿈 · 순서 바꿈 · 앞머리 들여쓰기 · 코드 속 들여쓰기 · 코드 조각 속 공백 · 강조 표식 옆 공백 · 인용 둘 합침 · 꺾쇠가 조사까지 감쌈 경우가 각각 1 을 낸다
- [ ] SK-03: 단계가 바뀌었거나 새로 생긴 제목마다 notes `N` 에 `- <경로>:<줄> … — <이유>` 줄이 있고, 그 줄에 제목 낱말을 찾은 grep 명령이 적혀 있다 [exact, enumerated]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N` 의 `HEADING <경로>:<줄>` 줄마다 같은 `경로:줄` 의 `NOTES_MISSING` 줄이 없고, `python3 $M/meaning.py $W $B $U $W/$L $W/$N | awk '/^HEADING /{print $2}' | while read -r k; do awk -v p="- $k " 'index($0,p)==1 && /grep/{f=1} END{exit !f}' $W/$N || echo "NOGREP $k"; done | grep -c .` 이 `0`. HEADING 이 0 줄이면 이 조건은 notes 없이 통과한다
    음성 대조: selftest 의 「notes 이유 없음」 · 「notes 다른 줄」 경우가 `NOTES_MISSING=1`

## Script

- [ ] SC-01: 검사 28 단계 `validate-plugin` · `sync-evals` · `sync-docs` · `sync-orchestrator` · `run-evals` · `contrast-claims` · `docs-links` · `stale-values` · `collector-test` · `react-detect-test` · `reflect-log-test` · `reflect-projid-test` · `reflect-collect-test` · `onboarding-gate-evals` · `howto-gate-evals` · `feedback-save-test` · `commit-guard-test` · `dart-format-hook-test` · `playwright-visuals` · `docs-a11y` · `scenario-report-ut` · `decision-gate-test` · `kaizen-assertions` · `reviewer-copies` · `api-ui-viewer` · `cause-table-copies` · `docs-drift-table` · `measure-helpers` 가 전부 rc=0 이다 (`validate-plugin` = `python3 scripts/validate-plugin.py`, `sync-docs` · `sync-orchestrator` · `sync-evals` = 각 `--check-only`, `run-evals` = `scripts/run-evals.py`, `kaizen-assertions` = `scripts/run-kaizen-assertions.py`, `reviewer-copies` = `scripts/check-reviewer-protocol-copies.py`, `cause-table-copies` = `scripts/check-cause-table-copies.py`). `feedback-agg-test SKIP (yq 없음)` 줄은 허용한다 [exact, enumerated]
    측정: `bash $M/ci.sh $W | tail -1` 이 `CI_OK=28 CI_BAD=0 CI_SKIP=1` (yq 가 설치된 기계면 `CI_OK=29 CI_BAD=0 CI_SKIP=0`). 단계 이름 28 개는 같은 실행의 요약 줄(`ci.sh` 출력 앞부분)에 각각 `rc=0` 으로 나온다 (단계 명령: `python3 scripts/validate-plugin.py` · `scripts/run-evals.py` · `scripts/run-kaizen-assertions.py` · `scripts/check-reviewer-protocol-copies.py` · `scripts/check-cause-table-copies.py` — ci-local.sh 와 ci.sh 가 부른다)
    음성 대조: 시험 사본에서 `tone-kit/README.md` 의 AUTO 블록 줄 하나(35 줄)를 고치면 `python3 scripts/sync-docs.py --check-only` 가 rc=1, 되돌리면 rc=0 (봉인 전 실측) — 그 단계가 `CI_BAD` 로 잡힌다
- [ ] SC-02: 측정 묶음과 목록 파일이 봉인 뒤 바뀌지 않았다 — `.harness/.meta/after-0926-mdlint-l3b/lint.sh` · `.harness/.meta/after-0926-mdlint-l3b/meaning.py` · `.harness/.meta/after-0926-mdlint-l3b/ci.sh` · `.harness/.meta/after-kaizen-0926b/l3b-files.txt` [exact, enumerated]
    측정: `shasum -a 256 <파일> | cut -c1-16` 이 차례로 `.harness/.meta/after-0926-mdlint-l3b/lint.sh` `241f16dba9687ed9` · `.harness/.meta/after-0926-mdlint-l3b/meaning.py` `c86f51a872340f16` · `.harness/.meta/after-0926-mdlint-l3b/ci.sh` `5db585eaf378130c` · `.harness/.meta/after-kaizen-0926b/l3b-files.txt` `cfb155b0a09756fe`, 그리고 `wc -l < $W/$L` 이 `67`
- [ ] SC-03: `bash $CL $W` 의 종료 코드가 0 이다 (사용자 전달 조건. 판정력은 SC-01 이 진다 — GAP 분석 절) [exact]
    측정: `T=$(mktemp -d); TMPDIR=$T bash $CL $W > $T/out 2>&1; echo $?` 이 `0`
    음성 대조: 해당 없음 (이 종료 코드는 yq 없는 기계에서 실패 단계가 있어도 0 이다. 실패 단계 검출은 SC-01 의 음성 대조가 맡는다). 시작 판 실측 `0`

## Error

- [ ] ER-01: 고치지 않는 파일 28 개가 한 줄도 바뀌지 않았다 — 끄기 주석도 없다. 대상: `howto-kit/README.md` · `howto-kit/skills/howto-audit/SKILL.md` · `howto-kit/skills/howto-doc/SKILL.md` · `onboarding-kit/skills/setup-guide/SKILL.md` · `howto-kit/evals/fixtures/` 의 `edge-empty.md` · `edge-zero-steps.md` · `fail-g3-domainmix.md` · `fail-g4-deprecation-ko.md` · `fail-g4-korean-abolish-unsourced.md` · `fail-g4-korean-delete-unsourced.md` · `fail-g4-korean-shutdown-unsourced.md` · `fail-g5-nonterminal.md` · `fail-g6-granularity.md` · `pass-fcm-ios.md` · `pass-g4-completion-phrase-not-deprecation.md` · `pass-g4-delete-action-not-deprecation.md` · `pass-g4-korean-delete-sourced.md` · `pass-g4-korean-sourced.md` · `pass-g4-retention-notice-not-deprecation.md` · `onboarding-kit/skills/setup-guide/evals/fixtures/` 의 `gate-blocking-ok.md` · `gate-fail-blocking-empty.md` · `gate-fail-blocking-nourl.md` · `gate-fail-ledger-double-source.md` · `gate-fail-ledger-marker-swift.md` · `gate-fail-ledger-misplaced.md` · `gate-g4-ko-sourced.md` · `gate-g4-ko-unsourced.md` · `gate-ok-flutter.md` [exact, enumerated]
    측정: `git diff --name-only $B $U -- howto-kit/README.md howto-kit/skills/howto-audit/SKILL.md howto-kit/skills/howto-doc/SKILL.md onboarding-kit/skills/setup-guide/SKILL.md howto-kit/evals/fixtures onboarding-kit/skills/setup-guide/evals/fixtures | grep -c .` 이 `0` 이고, 같은 여섯 경로에 `git status --porcelain --untracked-files=all --` 가 0 줄. 두 폴더는 `git ls-files` 로 펼치면 위 24 개 md 뿐이다(봉인 전 실측 24 개 · md 밖 0 개) (대상: `howto-kit/README.md` · `howto-kit/skills/howto-audit/SKILL.md` · `howto-kit/skills/howto-doc/SKILL.md` · `onboarding-kit/skills/setup-guide/SKILL.md` · `howto-kit/evals/fixtures/` 의 `edge-empty.md` · `edge-zero-steps.md` · `fail-g3-domainmix.md` · `fail-g4-deprecation-ko.md` · `fail-g4-korean-abolish-unsourced.md` · `fail-g4-korean-delete-unsourced.md` · `fail-g4-korean-shutdown-unsourced.md` · `fail-g5-nonterminal.md` · `fail-g6-granularity.md` · `pass-fcm-ios.md` · `pass-g4-completion-phrase-not-deprecation.md` · `pass-g4-delete-action-not-deprecation.md` · `pass-g4-korean-delete-sourced.md` · `pass-g4-korean-sourced.md` · `pass-g4-retention-notice-not-deprecation.md` · `onboarding-kit/skills/setup-guide/evals/fixtures/` 의 `gate-blocking-ok.md` · `gate-fail-blocking-empty.md` · `gate-fail-blocking-nourl.md` · `gate-fail-ledger-double-source.md` · `gate-fail-ledger-marker-swift.md` · `gate-fail-ledger-misplaced.md` · `gate-g4-ko-sourced.md` · `gate-g4-ko-unsourced.md` · `gate-ok-flutter.md`)
    양성 대조: 시험 사본에서 `howto-kit/skills/howto-doc/SKILL.md` 끝에 빈 줄 하나를 더해 커밋하면 같은 diff 셈이 `1` (봉인 전 실측)
- [ ] ER-02: 새로 넣은 markdownlint 주석은 전부 규칙 번호가 적힌 `disable-next-line` 이거나, 같은 규칙의 `enable` 이 뒤에 오는 `disable` · 그 짝 `enable` 이다 — `disable-file` · `configure-file` · 규칙 없는 끄기 · 짝 없는 `disable` 은 0 개 [exact]
    측정: `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 의 `BADDISABLE=0`
    양성 대조: selftest 의 「짝 없는 disable」 · 「파일 전체 끄기」 경우가 각각 `BADDISABLE=1`, 「한 줄 끄기 꼴」 은 `BADDISABLE=0`
- [ ] ER-03: notes `N` 에 `끄기 주석 수: <n>` 줄이 정확히 하나 있고 n 이 새로 넣은 주석 수와 같으며, 새 주석마다 `- <경로>:<줄> <규칙> — <이유>` 줄이 있다 [exact]
    측정: `grep -cE '^끄기 주석 수: [0-9]+$' $W/$N` 이 `1` · 그 수가 `python3 $M/meaning.py $W $B $U $W/$L $W/$N | tail -1` 의 `DISABLE=` 값과 같음 · 같은 끝 줄의 `NOTES_MISSING=0`
    음성 대조: selftest 의 「notes 이유 없음」 · 「notes 다른 줄」 경우가 `NOTES_MISSING=1`

## Architecture

- [ ] AR-01: 킷 폴더에서 바뀐 파일은 전부 목록 L 안에 있다 — 목록 밖 파일 변경 0 개 [exact]
    측정: (Given 공통 전제 · 경로 `.` 에서 `.harness` 제외 · 생성물 없음(md 만 고친다) · 「포함」 관계 · 상한 `U`) `git diff --name-only $B $U -- . ':(exclude).harness' | grep -vxFf $W/$L | grep -c .` 이 `0`, 그리고 `git status --porcelain --untracked-files=all -- . ':(exclude).harness' | grep -c .` 이 `0`. 봉인 전 기준값 `0`
    양성 대조: 같은 명령을 `6378948 c3e45f3` 구간에 돌리면 `187` (봉인 전 실측)
- [ ] AR-02: `.harness/` 아래에서 바뀐 경로는 이 계약 · 개정 · 피드백 · notes 네 가지 뿐이다 — 다른 계약 · 개정 · 기록 파일 변경 0 개 [exact]
    측정: `git diff --name-only $B $U -- .harness | grep -vE '^\.harness/(sprint-(contract|amendments|feedback)-after-0926-mdlint-l3b\.md|\.meta/after-kaizen-0926b/l3b-notes\.md)$' | grep -c .` 이 `0`
    양성 대조: 같은 명령을 `c3e45f3 de8c8cd` 구간에 돌리면 `4` (봉인 전 실측)
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
    측정: SK-01 과 같은 명령 (`bash $M/lint.sh $W $W/$L | tail -1` 이 `LINTED=67 WARNINGS=0`). AUTO 블록 안 · 밖은 시작 판 0 · 965 (리서치 소스)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 대상도 같은 파일이라 이번 변경 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (산출물이 md 문서뿐이라 구동할 앱 · 서버가 없다. 측정: RE-01 과 같은 명령이 0 — md · .harness 밖 변경 파일 0 개)
