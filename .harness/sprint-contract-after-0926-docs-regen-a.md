---
feature: "문서 페이지 다시 맞추기 A (harness · process · api · backend · bambu)"
slug: after-0926-docs-regen-a
created: "2026-09-27 16:09"
complexity: "복잡"
conditions: 25
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:2f0ef9185160f3ff
measurement_digest: sha256:600de837d4e77b33
locked_at: "2026-09-27 16:17"
---

## 배경

묶음 dr1a. 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dr1a`, 가지 `chore/ak2-dr1a`, 가지를 딴 판(기준 판) `38cccd1`.
짝 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/docs-pairs.txt`
(경고 정리 전 판 `c3e45f3` 기준 46 짝) 가운데 NEW 가 아니고 페이지가 `docs/harness/` · `docs/process/` · `docs/api-kit/` ·
`docs/backend-kit/` · `docs/bambu-kit/` 아래인 짝 17 개(페이지 16 쪽)를 원본에 맞춰 다시 만든다. 함께 하는 일 둘:

- 설계 가이드 `harness/docs/guides/contract-design-guide.md:775` 「작성 시점 패턴(조건 패턴 5 종)」 을 스킬 표의 실제 수 8 종으로 고치고
  페이지에도 반영한다(`cx-notes.md` 「끝 판 독립 검토가 찾은 것」 셋째 줄).
- `scripts/check-api-kit-docs.py` 의 외부 리소스 판정이 `url(//…)` · `<img src="https…">` · 빈칸 없는 `@import` 를 잡게 하고,
  이 검사를 `.github/workflows/ci.yml` 첫 작업에 한 단계로 넣는다(`cx-notes.md` 「판단 기록」 첫 줄 · 「끝 판 독립 검토」 첫 줄).

`docs/harness/feedback-schema.html` 은 NEW 라 이 묶음 밖이다.

이어작업이 아니다. 9/24 계약 `sprint-contract-after-0924-docs-regen.md` 와 대상 짝이 겹치지 않는 새 묶음이라, 앞 회차의 무엇을 좁힌 계약이 아니다(교차 진단 확인).

사용자 위임: 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 2026-09-26T10:09:00.557Z · 10:30:16.222Z · 2026-09-27T01:22:01.089Z
「자동으로 다 진행해 나한테 묻지 말고 …」. 결정 기록은
`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`.
조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다.

### 공통 전제

- 모든 측정은 W 에서 `bash .harness/.meta/after-0926-docs-regen-a/measure.sh <조건 번호>` 로 부른다(아래 조건의 「`m <번호>`」 가 이것이다).
  환경 `SCR` 은 세션 스크래치 아래 폴더다(이 계약 작성 때는 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/dr1a`).
- 끝 판 U 는 `git rev-parse --verify -q chore/ak2-dr1a` 로 푼다. 풀리지 않으면 측정이 `UNRESOLVED` 로 멈춘다 — `HEAD` 로 떨어지지 않는다.
- 「구현 커밋 뒤」 는 W 의 작업 트리가 U 와 같다는 뜻이다(`git -C W status --porcelain -- docs scripts .github harness` 가 빈 출력).
- 옛 판(담김 비교 기준)은 기준 판 `38cccd1` 의 페이지다. 봉인 전에 잰 값은 `baseline.tsv` 에 있다.
- 원본 담김 도구 둘은 레포 밖 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/` 의 `coverage.py` · `fence2.py` 다.
  그 폴더 안에서 python3 를 돌리지 않는다(표준 모듈이 가려진다). 측정 묶음이 절대 경로로 부른다.

### 측정 묶음

`.harness/.meta/after-0926-docs-regen-a/` 에 둔다. 봉인 커밋과 따로 커밋한다. 봉인 전 지문(sha256 앞 16 자리)은 AR-03 에 적는다.

| 파일 | 하는 일 |
| --- | --- |
| `measure.sh` | 조건 번호마다 측정 한 벌 |
| `pairs.txt` | 짝 17 개 (원본 · 페이지) |
| `baseline.tsv` | 짝마다 옛 판 값 — 코드 표시 담김 수 · 낱말 비율 · 코드 블록 줄 담김 수 |
| `heads.tsv` | 페이지 머리에 있어야 할 판 번호 · 날짜 (원본 머리에서 옮김) |
| `drift.py` | 페이지가 마지막으로 고쳐진 뒤 원본에 새로 생긴 코드 표시가 페이지에 들었는지 |
| `layout.js` | 세 폭 × 두 테마 넘침 · 글 잘림 · 콘솔 오류 |
| `ext_cases.py` | 외부 리소스 판정식 사례 30 · 기준 판과 200 입력 맞대기 |

### 복잡도 네 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 지나는가 | 셋 — 문서 페이지 · 검사 스크립트 · CI 설정 |
| 공개 API·계약 변경 | 밖에 보이는 판정이 바뀌는가 | 예 — `check-api-kit-docs.py` 의 외부 리소스 판정이 넓어진다 |
| 소비면 존재 | 그 변경을 받아 쓰는 쪽이 있는가 | 예 — CI 단계 · 종료 코드 표 · api-kit 12 쪽 |
| 회귀 위험 | 기존 동작이 깨질 길이 있는가 | 예 — 페이지를 다시 만들며 원본 내용을 덜 담을 수 있고, 판정식이 옛 18 사례를 다르게 볼 수 있다 |

네 축 모두 예 → 복잡. Step 2.5 짝 조건: 만드는 쪽은 SC-01(판정식), 받는 쪽은 SC-02(CI 단계 · 종료 코드 표) · SC-03(api-kit 12 쪽이 새 판정으로 통과) · ER-01(쪽이 없을 때의 기존 동작).
설계 가이드 한 줄의 받는 쪽은 페이지 `docs/harness/contract-design-guide.html` 이고 SK-06 이 함께 잰다.

### 설정 값 대조

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀔 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-02 · AP-03. AP-01 은 `plugin.json` 판을 건드리지 않아서, AP-04 는 SKILL.md · agents 를 건드리지 않아서 뺐다 |

## 리서치 소스

- 문서 페이지 규칙: 레포 `.claude/skills/docs-site/SKILL.md` Gotcha 1 · 8 · 10 · 11 · 13 과 Step 7 의 담김 조건 둘
- 페이지 맞추기 계약 다섯 가지 · 산출물이 검사인 조건 · 기존 동작 유지 조건: `harness/references/contract-schema.md` v5.7 해당 절
- 짝 목록 · 남은 일: `after-kaizen-0926b/docs-pairs.txt` · `cx-notes.md` · `hs-notes.md:104` · `vsa-notes.md:53` · `vsb-notes.md:79` · `leftovers.md` DC-3 · DC-4 · DC-6 · DC-15

## GAP 분석 (Pre-Edit Audit)

기준 판 `38cccd1` 에서 읽기만 했다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `docs/harness/contract-schema.html` | 머리 「Sprint Contract 스키마 v5.6 · 2026-09-26」 · `with_two` · `dirty_except_status` · 「페이지 맞추기 계약」 0 건 | 원본은 v5.7(`harness/references/contract-schema.md:6`). 원본에 새로 생긴 코드 표시 62 개 중 50 개가 없다 | SK-03 · SK-04 · SK-05 |
| `docs/harness/qa-evaluation-guide.html` | `:748` 「커밋 훅은 50 개를 넘는 삭제만 막는다」 · 머리 「v5.1 · 2026-09-24」 | 원본 머리는 2026-09-26(`qa-evaluation-guide.md:4`), 범위 목록 블록(`sprint-scope`) 0 건 | SK-03 · SK-04 · SK-05 |
| `docs/harness/contract-design-guide.html` | `:1013` 「조건 패턴 5 종」 · `measurement_digest` 0 건 | 원본도 `:775` 에 옛 수 | SK-04 · SK-06 |
| `docs/harness/plugin-validation.html` | 머리 「v1.4.1 · 2026-09-26」 · `:372` · `:924` 「V2 전체 SKIP」 | 원본 1.5.0 은 `no templates/ — OK`(`plugin-validation-guide.md` V2 절) | SK-03 · SK-04 · SK-05 |
| `docs/harness/agent-design-guide.html` · `skill-design-guide.html` | 머리 판 번호 맞음 | 원본에 새로 생긴 코드 표시 4 · 14 개 중 0 · 1 개만 있다(`cacheTtl` · `# sprint-scope` 등) | SK-04 |
| `docs/process/kaizen-flow.html` | `:198` 범위 표 · `:257` | 원본 범위 줄의 `scripts/` · `templates/` 가 없다(`.claude/skills/kaizen-orchestrator/SKILL.md:420` 등) | SK-04 · SK-05 |
| `docs/process/phase-research-templates.html` | 머리 「판 1.2.0」 | 원본 `last_updated: 2026-09-05` 가 머리에 없다, 새 코드 표시 2 개 없음 | SK-03 · SK-04 |
| `docs/api-kit/static-evidence-viewer-contract.html` · `multi-sample-pagination-variance.html` · `contract-extraction-modes.html` | 머리 「v0.1.1 · 2026-09-24」 · 「v0.1.0 · 2026-09-04」 · 「v0.1.1 · 2026-09-24」 | 머리는 맞다. api-ui 스킬 · 설계 기록에서 새 코드 표시 3 개가 없다 | SK-04 |
| `docs/backend-kit/api-design.html` | 머리 「v0.1.1 · 2026-09-25」 | 새 코드 표시 0 — 이미 맞춰져 있을 수 있다 | SK-01 ~ SK-04 로만 잰다 |
| `docs/bambu-kit/bambu-print-profile.html` | 미검증 표(`leftovers.md` DC-6 가 짚은 `:1647` 근처) | 「종류 줄만 빠진 목록」 행이 없다, 새 코드 표시 10 개 중 9 개 없음 | SK-04 · SK-05 |
| `docs/bambu-kit/bambu-fields-baseline.html` · `materials.html` · `failure-recipes.html` | 머리 텍스트 | fields-baseline 머리에 `2026-05-15` · `v02.08.04.57` · `v02.08.02.61` 없음, materials 머리에 `2026-05-15` 없음 | SK-03 · SK-04 |
| `harness/docs/guides/contract-design-guide.md` | `:775` 「(조건 패턴 5 종)」 | 스킬 표는 8 행(`harness/skills/sprint-contract/SKILL.md:477` 「조건 패턴 8 종 (v5.7)」) | SK-06 |
| `scripts/check-api-kit-docs.py` | `:36-39` `EXTERNAL` · `:74` 적용 · `:87-90` 쪽 순회 | `url(` 쪽은 `https?://` 만, `<img src>` 없음, `@import\s` 는 빈칸이 있어야 잡는다. 사례 30 중 Q1 ~ Q6 여섯을 틀린다 | SC-01 |
| `.github/workflows/ci.yml` · `harness/evals/gate-exit-codes.md` | ci `:16` 첫 작업 `validate:` · `:82-83` 판정 표 사본 단계 · 종료 코드 표 `:62-73` | 이 검사가 CI 에도 표에도 없다 | SC-02 |

구현 방향 한 가지(판정식) — `<img\b … src=` 는 `data:` 를 빼고 스킴 · `//` · `\\` 로 시작하면 외부, `url(` 은 `https?:` 와 `//` 로 시작하면 외부,
`@import` 는 뒤 빈칸과 상관없이 외부. 봉인 전에 이 모양의 흉내 판정식(세션 스크래치 `dr1a/mock-check.py`)으로 사례 30 · 200 입력 · 12 쪽 · 두 사본을 모두 쟀다(아래 회귀 게이트).
조건은 판정만 재므로 식의 모양은 구현이 고른다.

## 범위 경계

```text
# sprint-scope
docs/process/kaizen-flow.html
docs/process/phase-research-templates.html
docs/api-kit/static-evidence-viewer-contract.html
docs/api-kit/multi-sample-pagination-variance.html
docs/api-kit/contract-extraction-modes.html
docs/backend-kit/api-design.html
docs/bambu-kit/bambu-print-profile.html
docs/bambu-kit/bambu-fields-baseline.html
docs/bambu-kit/failure-recipes.html
docs/bambu-kit/materials.html
docs/harness/agent-design-guide.html
docs/harness/contract-design-guide.html
docs/harness/plugin-validation.html
docs/harness/qa-evaluation-guide.html
docs/harness/skill-design-guide.html
docs/harness/contract-schema.html
docs/index.html
harness/docs/guides/contract-design-guide.md
scripts/check-api-kit-docs.py
.github/workflows/ci.yml
harness/evals/gate-exit-codes.md
```

- 페이지 16 쪽은 원본에 이미 맞으면 바꾸지 않아도 된다 — SK-01 ~ SK-08 이 판정한다. 꼭 바뀌어야 하는 것은 아래 넷(AR-01).
- `docs/index.html` 은 목차 제목에 판 번호가 붙은 줄을 맞출 때만 고친다(지금 `contract-schema` 줄은 이미 v5.7).
- 원본 md 가운데 고치는 것은 설계 가이드 한 줄뿐이다. 다른 원본의 판 번호 · 날짜는 그대로 두고 페이지를 원본에 맞춘다.
- api-kit 12 쪽 본문에 `@import` · `url(//` · `<img src="https…">` 글자가 산문으로 들어가면 새 판정식이 외부 리소스로 잡는다 — 그런 글을 쓸 때는 코드 표시 안에서 `&lt;`·`&#64;` 로 옮기거나 산문 표현을 바꾼다.
- 이 묶음 밖: `docs/harness/feedback-schema.html`(NEW) · 짝 목록의 나머지 킷 페이지 · 편집기 경고 정리 · 검사기 단추 id 문제(cx-notes) · 킷 판 올림.
- `.harness/` 아래(계약 · 측정 묶음 · notes)는 범위 목록에 적지 않아도 된다.
- 커버리지 해소: SK-01 — 측정 `m SK-01` 이 `pairs.txt` · `baseline.tsv` 의 17 짝을 모두 돌고 짝마다 페이지 · 원본 이름을 한 줄씩 낸다(봉인 전 출력 17 줄 + `pairs=17`). 목록을 측정 절에 다시 적지 않는다
- 커버리지 해소: SK-03 — `m SK-03` 이 `heads.tsv` 14 줄을 돌며 쪽마다 한 줄을 내고, 낱말은 `heads.tsv` 에 조건 산문과 같은 글자로 있다(봉인 전 `pages=14`)
- 커버리지 해소: SK-05 — `m SK-05` 가 산문의 여섯 (쪽 · 글자) 짝을 글자 그대로 `chk` 여섯 줄로 잰다(`items=6`)
- 커버리지 해소: SK-07 — `../assets/site.css` · `assets/site.css` 는 대상이 아니라 세는 글자다. `m SK-07` 이 SK-01 의 16 쪽을 `pairs.txt` 에서 읽어 쪽마다 한 줄을 낸다(`pages=16`)
- 커버리지 해소: AR-01 — `m AR-01` 의 `required=` 가 산문의 네 경로를 글자 그대로 담은 목록으로 센다(`required=0/4` 의 분모 4)

## 회귀 게이트

봉인 전 실측(기준 판 `38cccd1`, U = `38cccd1`, 2026-09-27). 모든 값은 위 측정 묶음으로 냈다.

- `m SK-01` · `m SK-02` → `pairs=17 bad=0` (옛 판 = 지금 판이라 같다). 양성 대조: W 를 `git clone --shared` 한 스크래치 복제본에서 `docs/harness/contract-schema.html` 을 반으로 자른 뒤 `REPO=<복제본>` 로 재면 SK-01 `new=200/316 lost=116 wr=0.63/0.89 BAD` · SK-02 `in_new=128/259 lost=47 BAD`, 둘 다 `pairs=17 bad=1` · 종료 코드 1.
- `m SK-03` → `pages=14 bad=6` (phase-research-templates `2026-09-05` · fields-baseline 셋 · materials `2026-05-15` · plugin-validation `1.5.0` · qa-evaluation-guide `2026-09-26` · contract-schema `v5.7` 빠짐).
- `m SK-04` → `pairs=17 total_missing=135` · 종료 코드 1. 알려진 답: 스크래치 저장소(`dr1a/ka`) — 커밋 1 원본 `` `a` `` · 페이지 `a`, 커밋 2 원본에 `` `b c` `` · `` `d` `` 더하고 페이지에 `b c` 더함(페이지 마지막 커밋 1) → 기대 `added=2 in_page=1 missing=1` · 종료 코드 1, 실제 같음.
- `m SK-05` → `items=6 bad=6`. `m SK-06` → `skill_rows=8 guide5=1 guide8=0 page5=1 page8=0`.
- `m SK-07` → `pages=16 bad=0`. 양성 대조: 복제본의 `docs/bambu-kit/materials.html` 에 같은 링크 한 줄을 더하면 `link=2 mentions=2 BAD` · `pages=16 bad=1` · 종료 코드 1.
- `m SK-08` → `cells=96 bad=0`. 양성 대조: 스크래치 `dr1a/bad.html`(900px 상자 · 100px 폭 `overflow:hidden` 글 · `console.error`) 6 칸 모두 `BAD` (320 에서 `overflow=588 clipped=1 errors=1`), `dr1a/clip-only.html`(잘린 글만) 6 칸 모두 `clipped=1 BAD`, 종료 코드 1. 두 테마 확인: 16 쪽 가운데 api-kit 셋 · process 둘은 테마마다 `body` 배경이 다르고(밝음 `rgb(246, 247, 243)` 등 · 어두움 `rgb(13, 13, 20)`), 나머지 열한 쪽은 어두운 단일 테마라 두 칸이 같게 그려진다 — 조건은 두 테마 모두에서 넘침 · 잘림 0 만 요구한다.
- `m SC-01` → `cases=30 wrong=6 Q1,Q2,Q3,Q4,Q5,Q6 | compare n=200 diff=0 seed=20260927 | tree=[12/12 PASS] rc0=0 | last=static-evidence-viewer-contract applied1=1 rc1=0 fail1=0 fail1_last=0 | first=contract-extraction-modes applied2=1 rc2=0 fail2=0 fail2_first=0`. 흉내 판정식으로는 `cases=30 wrong=0` · `diff=0` · `tree=[12/12 PASS]` · 마지막 쪽 사본 종료 코드 1 · `FAIL` 1 줄 · 그 쪽 이름. 음성 대조: 흉내 판에서 `re.IGNORECASE` 를 뺀 판정식은 `compare n=200 diff=50` · 종료 코드 1.
- `m SC-02` → `ci_steps=0 job=[] first_job=[validate:] exitdoc=0`.
- `m SC-03` → `a11y=rc0/[16/16 PASS] links=rc0/[1] contrast=rc0/[1] api=rc0/[12/12 PASS] table=rc0/[1]`.
- `m SC-04` → `tool=59fe55125c0dbc77` · `ci_local_ok=25 other=[feedback-agg-test SKIP (yq 없음)] cause_copies=rc0 measure_helpers=rc0`.
- `m ER-01` → `rc=1 rows=12 missing_named=1 summary=[11/12 PASS]` (지금 판정식에서도 같다 — 지켜야 할 기존 동작).
- `m AR-01` → `scope=0 changed=0 extra=[] required=0/4` (범위 블록은 이 파일에 방금 썼고 구현 커밋이 아직 없다). `m AR-02` → `commits=0 bad=0`. `m AR-04` → `notes=0`.
- `m AP-02` → `remote_heads=0`. `m AP-03` → `rc=0 v6=[V6 code-fence        0 bare — OK]`.
- `m DG-02` → `md=rc0/[1]/[Summary: 0 issues in 0 files] py=rc0`. 양성 대조: 같은 파일에 MD013 을 켜면 `contract-design-guide.md:1328:81 error MD013/line-length` 가 나온다. 설정 파일 `dr1a/mdlint/cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }`.
  `contract-design-guide.md` 에 `<!-- AUTO:* -->` 블록 0 개(`grep -c 'AUTO:'` 0) — 블록 안 · 밖으로 나눌 것이 없다.

준비 단계(봉인 전에 돌림):

- `REPO` 를 바꿔 잴 때(양성 대조 복제본 등)는 항상 절대 경로로 준다. `layout.js` 는 `REPO/node_modules/playwright-core` 를 `require` 하는데, 상대 경로면 Node 가 패키지 이름으로 읽어 `MODULE_NOT_FOUND` 로 죽는다(교차 진단이 재현). 기본값은 `measure.sh` 가 절대 경로로 준다.
- 교차 진단 뒤 `m SC-01` 을 다시 돌려 같은 값(`wrong=6 … rc1=0 fail1=0`)을, 흉내 판정식으로 `cases=30 wrong=0` · `compare n=200 diff=0` 을 다시 받았다(2026-09-27).
- W 에 `npm ci` (종료 코드 0, `node_modules/playwright-core` 있음). `node` 는 v24.14.1.
- markdownlint: `cd $SCR/mdlint && npm install --no-save markdownlint-cli2@0.23.2` (종료 코드 0), `--help` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. `measure.sh` 는 `ML`(기본 `$SCR/mdlint`) 아래 이 설치본을 쓴다.
- `ci-local.sh` 지문 `59fe55125c0dbc77`. `TMPDIR` 은 `m SC-04` 가 `$SCR` 아래 새 폴더로 준다.
- zsh 에서 목록 변수를 따옴표 없이 넘기면 쪼개지지 않는다 — 측정 묶음은 bash 로 돌고, 페이지 목록은 `xargs` 로 넘긴다(봉인 전 `node scripts/check-docs-a11y.js $P` 가 zsh 에서 16 쪽을 한 경로로 붙여 실패한 것을 보고 고쳤다).

## Skill

- [ ] SK-01: 다시 만든 16 쪽이 원본을 옛 판(`38cccd1`)보다 덜 담지 않는다 — Given 구현 커밋 뒤, When 17 짝마다 `coverage.py <W> <원본> <페이지> 38cccd1` 를 돌리면, Then 짝마다 원본 코드 표시가 페이지에 든 수(`new`)가 `baseline.tsv` 의 옛 값 이상이고, 옛 페이지에 있던 코드 표시가 빠진 수(`lost`)가 0 이고, 원본 낱말 비율(`wr` 화살표 뒤)이 옛 값 이상이다 [exact, enumerated]
  대상 17 짝: `docs/process/kaizen-flow.html` · `docs/process/phase-research-templates.html` · `docs/api-kit/static-evidence-viewer-contract.html`(원본 둘 — `api-kit/skills/api-ui/SKILL.md` · `docs/api/verification/static-evidence-viewer-contract.md`) · `docs/api-kit/multi-sample-pagination-variance.html` · `docs/api-kit/contract-extraction-modes.html`(둘 다 원본 `docs/superpowers/specs/2026-09-02-api-kit-design.md`) · `docs/backend-kit/api-design.html` · `docs/bambu-kit/bambu-print-profile.html` · `docs/bambu-kit/bambu-fields-baseline.html` · `docs/bambu-kit/failure-recipes.html` · `docs/bambu-kit/materials.html` · `docs/harness/agent-design-guide.html` · `docs/harness/contract-design-guide.html` · `docs/harness/plugin-validation.html` · `docs/harness/qa-evaluation-guide.html` · `docs/harness/skill-design-guide.html` · `docs/harness/contract-schema.html`
  측정: `m SK-01` 이 `pairs=17 bad=0` · 종료 코드 0 (옛 값은 `baseline.tsv` 둘째 · 넷째 칸. 봉인 전 실측은 회귀 게이트 첫 줄)
  양성 대조: 반으로 자른 페이지를 둔 복제본에서 `bad=1` · 종료 코드 1 (봉인 전 실측)
- [ ] SK-02: 원본 코드 블록 줄이 페이지에 든 수가 옛 판보다 줄지 않는다 — Given 구현 커밋 뒤, When SK-01 의 17 짝마다 `fence2.py <W> <원본> <페이지>` 를 돌리면, Then 짝마다 `in_new` 가 `baseline.tsv` 다섯째 칸 이상이고 `lost` 가 0 이다 [exact, enumerated]
  측정: `m SK-02` 가 `pairs=17 bad=0` · 종료 코드 0
  양성 대조: SK-01 과 같은 복제본에서 `in_new=128/259 lost=47 BAD` · `bad=1` (봉인 전 실측)
- [ ] SK-03: 페이지 머리의 판 번호 · 날짜가 원본 머리와 같다 — Given 구현 커밋 뒤, When `heads.tsv` 의 14 쪽마다 본문 글(스크립트 · 스타일을 빼고 태그를 벗긴 글)의 첫 700 글자를 보면, Then 그 쪽에 적힌 낱말이 모두 들어 있다 [exact, enumerated]
  대상과 낱말: `docs/process/phase-research-templates.html` `1.2.0` `2026-09-05` · `docs/api-kit/static-evidence-viewer-contract.html` `0.1.1` `2026-09-24` · `docs/api-kit/multi-sample-pagination-variance.html` `0.1.0` `2026-09-04` · `docs/api-kit/contract-extraction-modes.html` `0.1.1` `2026-09-24` · `docs/backend-kit/api-design.html` `0.1.1` `2026-09-25` · `docs/bambu-kit/bambu-fields-baseline.html` `2026-05-15` `v02.08.04.57` `v02.08.02.61` · `docs/bambu-kit/failure-recipes.html` `2026-08-13` · `docs/bambu-kit/materials.html` `2026-05-15` · `docs/harness/agent-design-guide.html` `1.7.0` `2026-09-24` · `docs/harness/contract-design-guide.html` `v5.1` `2026-09-24` · `docs/harness/plugin-validation.html` `1.5.0` `2026-09-26` · `docs/harness/qa-evaluation-guide.html` `v5.1` `2026-09-26` · `docs/harness/skill-design-guide.html` `1.6.0` `2026-09-24` · `docs/harness/contract-schema.html` `v5.7` `2026-09-26`. 예외: `docs/process/kaizen-flow.html` · `docs/bambu-kit/bambu-print-profile.html` — 원본 머리에 판 번호 · 날짜가 없다
  측정: `m SK-03` 이 `pages=14 bad=0` · 종료 코드 0 (봉인 전 `bad=6`)
- [ ] SK-04: 페이지가 마지막으로 고쳐진 뒤 원본에 새로 생긴 코드 표시가 모두 페이지에 든다 — Given 구현 커밋 뒤, When 17 짝마다 기준 판 `38cccd1` 에서 그 페이지를 마지막으로 고친 커밋의 원본과 지금 원본의 코드 표시(백틱 글, 빈칸은 하나로)를 견줘 새로 생긴 것을 모으면, Then 그 가운데 페이지 글(스크립트 · 스타일 뺌, 태그 벗김, 빈칸 하나로)에 없는 것이 0 개다 [exact, enumerated]
  측정: `m SK-04` 가 끝 줄 `pairs=17` · `total_missing=0` (두 값은 탭으로 나뉜다) · 종료 코드 0 (봉인 전 `total_missing=135` · 종료 코드 1)
  알려진 답: 스크래치 저장소 `dr1a/ka` 에서 기대 `added=2 in_page=1 missing=1` · 종료 코드 1, 실제 같음 (봉인 전 실측)
- [ ] SK-05: notes 가 짚은 산문 어긋남 여섯이 풀렸다 — Given 구현 커밋 뒤, When 아래 글자를 페이지에서 `grep -cF` 로 세면, Then `docs/harness/qa-evaluation-guide.html` 의 「50 개를 넘는 삭제만」 0 · 「sprint-scope」 1 이상, `docs/harness/contract-schema.html` 의 「페이지 맞추기 계약」 1 이상, `docs/bambu-kit/bambu-print-profile.html` 의 「종류 줄만 빠진」 1 이상, `docs/process/kaizen-flow.html` 의 「templates/」 1 이상, `docs/harness/plugin-validation.html` 의 「no templates/ — OK」 1 이상이다 [exact, enumerated]
  측정: `m SK-05` 가 `items=6 bad=0` · 종료 코드 0 (봉인 전 `bad=6`)
- [ ] SK-06: 설계 가이드와 그 페이지의 조건 패턴 수가 스킬 표의 실제 행 수와 같다 — Given 구현 커밋 뒤, When `harness/skills/sprint-contract/SKILL.md` 의 「**조건 패턴 8 종」 표 행과 두 파일의 글자를 세면, Then 표 행 8 · `harness/docs/guides/contract-design-guide.md` 의 「조건 패턴 5 종」 0 · 「조건 패턴 8 종」 1 · `docs/harness/contract-design-guide.html` 의 「조건 패턴 5 종」 0 · 「조건 패턴 8 종」 1 이상이다 [exact]
  측정: `m SK-06` 이 `skill_rows=8 guide5=0 guide8=1 page5=0 page8=` 1 이상 · 종료 코드 0 (봉인 전 `skill_rows=8 guide5=1 guide8=0 page5=1 page8=0`)
  알려진 답: 표 행을 손으로 세면 측정 커버리지 표기 · 인자 매트릭스 · 음성 대조 · 양성 대조 · 알려진 답 대조 · 산출물이 검사인 조건 · 기존 동작 유지 조건 · 페이지 맞추기 계약 8 개, 측정 `skill_rows=8` (봉인 전 실측)
- [ ] SK-07: 16 쪽이 공통 링크 `../assets/site.css` 를 정확히 하나 가진다 — Given 구현 커밋 뒤, When 쪽마다 그 주소를 `href` 로 가진 `<link` 태그 수와 `assets/site.css` 글자 수를 세면, Then 둘 다 1 이다 [exact, enumerated]
  대상: SK-01 의 16 쪽
  측정: `m SK-07` 이 `pages=16 bad=0` · 종료 코드 0
  양성 대조: 링크 한 줄을 더한 복제본에서 `link=2 mentions=2 BAD` · 종료 코드 1 (봉인 전 실측)
- [ ] SK-08: 16 쪽이 세 폭 · 두 테마에서 가로로 넘치지 않고 글이 잘리지 않고 콘솔 오류가 없다 — Given 구현 커밋 뒤 W 에 `npm ci` 가 된 상태, When `layout.js` 가 쪽마다 폭 320 · 375 · 1280 과 테마 light · dark(prefers-color-scheme 흉내 · `localStorage` `dk-theme` · `html[data-theme]` 셋 다 맞춤) 여섯 칸을 열면, Then 96 칸 모두 `overflow=0`(문서 폭 − 보이는 폭) · `clipped=0`(자기 글을 가진 요소 중 `overflow` 가 hidden · clip 이거나 `text-overflow` 가 ellipsis 인데 내용 폭이 상자보다 1px 넘게 큰 것) · `errors=0` 이다 [exact, enumerated]
  측정: `m SK-08` 이 `cells=96 bad=0` · 종료 코드 0. 캡처는 `$SCR` 아래에만 둔다(커밋하지 않는다)
  양성 대조: `dr1a/bad.html` · `dr1a/clip-only.html` 12 칸 모두 `BAD` · 종료 코드 1 (봉인 전 실측)

## Script

- [ ] SC-01: api-kit 문서 검사가 `url(//…)` · `<img src="https…">` · 빈칸 없는 `@import` 를 외부 리소스로 잡고, 옛 18 사례와 그 밖 입력의 판정은 그대로다 — Given 구현 커밋 뒤, When 끝 판 `scripts/check-api-kit-docs.py` 의 `EXTERNAL` 에 `ext_cases.py` 사례 30 을 넣고, 기준 판 판정식과 시드 20260927 입력 200 개로 맞대고, 끝 판 트리(`git archive` 로 푼 `scripts` · `docs`)에서 검사를 (가) 그대로 (나) 마지막 쪽 `docs/api-kit/static-evidence-viewer-contract.html` 의 `</body>` 앞에 `<img src="https://x.test/a.png" alt="">` 를 넣은 사본 (다) 첫 쪽 `docs/api-kit/contract-extraction-modes.html` 의 `</style>` 앞에 `.x{background:url(//cdn.x.test/a.png)}` 를 넣은 사본으로 돌리면, Then 사례 틀림 0 · 맞대기 차이 0 · (가) 요약 `12/12 PASS` 종료 코드 0 · (나) 변이 1 줄 들어감 · 종료 코드 1 · `FAIL` 1 줄 · 그 줄이 마지막 쪽 · (다) 변이 1 줄 · 종료 코드 1 · `FAIL` 1 줄 · 그 줄이 첫 쪽이다 [exact]
  사례(1 = 외부, 0 = 외부 아님 — `ext_cases.py` 가 글자 그대로 담는다): 옛 18 P1 ~ P10 · N1 ~ N6 · U1 · U2(앞 계약 `after-0926-codex-and-leftover-fixes` SC-01 그대로) · 새 Q1 1 `url(//cdn…)` · Q2 1 `url( '//cdn…')` · Q3 1 `<img src="https://…">` · Q4 1 `<IMG ALT='' SRC='//…'>` · Q5 1 `@import"https://…"` · Q6 1 `@import'//…'` · Q7 1 `@import url(https://…)` · R1 0 `<img src="../assets/a.png">` · R2 0 `<img src="data:…">` · R3 0 `url(data:…)` · R4 0 `<img alt="https://…" src="a.png">` · R5 0 `fill="url(#grad)"`
  측정: `m SC-01` 이 `cases=30 wrong=0 | compare n=200 diff=0 seed=20260927 | tree=[12/12 PASS] rc0=0 | last=static-evidence-viewer-contract applied1=1 rc1=1 fail1=1 fail1_last=1 | first=contract-extraction-modes applied2=1 rc2=1 fail2=1 fail2_first=1`
  음성 대조: 기준 판 판정식은 `wrong=6 Q1,Q2,Q3,Q4,Q5,Q6` · (나) (다) 모두 `rc=0 fail=0` — 옛 구현을 두면 실패한다. 흉내 판에서 대소문자 무시를 빼면 `diff=50` — 맞대기가 판정 차이를 잡는다 (봉인 전 실측)
  기존 동작 유지 조건: 하위 문장 「옛 18 사례의 판정이 같다」 는 사례 P · N · U, 「이번에 뜻을 바꾸지 않는 모양(`<link href>` · `<script src>` · `<a href>` · 산문 · 빈칸 있는 `@import` · `//` 로 시작하지 않는 `url(`)의 판정이 같다」 는 시드 20260927 무작위 입력 200 개로 잰다
  산출물이 검사인 조건: ① 첫 칸만 읽기 — (나) 가 위반을 마지막 쪽에만 둔 사본이고 요약 줄이 12 쪽을 센다 ② 실행 목록 등록은 SC-02 ③ ER-01 ④ 해당 없음 (고정 해석기 python3)
- [ ] SC-02: api-kit 문서 검사가 CI 첫 작업의 한 단계이고 종료 코드 표에 한 행이다 — Given 구현 커밋 뒤, When 끝 판 `.github/workflows/ci.yml` 과 `harness/evals/gate-exit-codes.md` 를 읽으면, Then `run: python3 scripts/check-api-kit-docs.py` 줄이 1 개이고 그 줄이 든 작업이 `jobs:` 의 첫 작업이며, 소비처 표에 `` | `scripts/check-api-kit-docs.py` | 0 · 1 | `` 행이 1 개다 [exact]
  측정: `m SC-02` 가 `ci_steps=1 job=[validate:] first_job=[validate:] exitdoc=1` (봉인 전 `ci_steps=0 job=[] first_job=[validate:] exitdoc=0`)
- [ ] SC-03: 문서 검사 다섯이 끝 판에서 통과하고 검사한 수가 맞다 — Given 구현 커밋 뒤, When W 에서 `node scripts/check-docs-a11y.js <16 쪽>` · `python3 scripts/check-docs-links.py` · `python3 scripts/check-contrast-claims.py` · `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` 를 돌리면, Then 다섯 모두 종료 코드 0 이고, a11y 끝 줄 `16/16 PASS` · links 에 「고아 · 유령 · 아이콘 누락 없음」 1 줄 · contrast 에 「어긋난 것: 0」 1 줄 · api-kit 끝 줄 `12/12 PASS` · 표 맞대기에 「어긋남 0」 1 줄이다 [exact, enumerated]
  측정: `m SC-03` 이 `a11y=rc0/[16/16 PASS] links=rc0/[1] contrast=rc0/[1] api=rc0/[12/12 PASS] table=rc0/[1]` (봉인 전 같은 값 — 다시 만든 뒤에도 지켜야 한다)
  양성 대조: api-kit 검사는 SC-01 (나) (다), a11y 넘침은 SK-08 의 `bad.html` 과 같은 모양(검사기 자체 판정 `of>2px` FAIL)으로 확인한다. 검사한 수(16 · 12)를 함께 재어 검사가 멈춘 0 을 통과로 읽지 않는다
- [ ] SC-04: 로컬 CI 전체와 그 스크립트 밖의 CI 단계가 통과한다 — Given 구현 커밋 뒤, When `ci-local.sh`(지문 `59fe55125c0dbc77`)를 `TMPDIR=$SCR/<새 폴더>` 로 W 에 돌리고 `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` 를 돌리면, Then 요약의 `rc=0` 줄이 25 개이고 나머지 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이며 두 스크립트 종료 코드가 0 이다 [exact]
  측정: `m SC-04` 가 `tool=59fe55125c0dbc77` 과 `ci_local_ok=25 other=[feedback-agg-test SKIP (yq 없음)] cause_copies=rc0 measure_helpers=rc0` (봉인 전 같은 값). api-kit 검사 · 표 맞대기는 SC-03 이 잰다

## Error

- [ ] ER-01: api-kit 쪽 하나가 없어도 검사가 나머지를 다 재고 없는 쪽을 이름으로 댄다 (기존 동작 유지) — Given 구현 커밋 뒤, When 끝 판 트리에서 `docs/api-kit/multi-sample-pagination-variance.html` 을 지운 사본으로 `python3 scripts/check-api-kit-docs.py` 를 돌리면, Then 종료 코드 1 · 쪽 줄(`OK  ` · `FAIL` 로 시작) 12 개 · 그 쪽의 `FAIL` 줄 바로 아래에 「HTML 없음」 · 요약 `11/12 PASS` 다 [exact]
  측정: `m ER-01` 이 `rc=1 rows=12 missing_named=1 summary=[11/12 PASS]` (봉인 전 같은 값 — 판정식을 바꾸며 쪽 순회를 건드리지 않았다는 확인)

## Architecture

- [ ] AR-01: 바뀐 경로가 범위 목록 안이고 꼭 바뀌어야 할 넷이 바뀌었다 — Given 구현 커밋 뒤, When `git diff --name-only 38cccd1..<U> -- . ':(exclude).harness'` 를 이 계약 「범위 경계」 의 `# sprint-scope` 블록과 견주면, Then 블록 밖 경로가 0 개이고 `harness/docs/guides/contract-design-guide.md` · `scripts/check-api-kit-docs.py` · `.github/workflows/ci.yml` · `harness/evals/gate-exit-codes.md` 넷이 모두 바뀐 목록에 있다 [exact, enumerated]
  측정: `m AR-01` 이 `scope=21 changed=<수> extra=[] required=4/4` (U 는 공통 전제대로 가지 끝. 봉인 전 `changed=0 required=0/4` — 구현 전이라 0)
  생성물 제외: 이 레포에 생성 코드가 없다. `.harness/` 는 계약 · 측정 묶음 · notes 자리라 뺀다
- [ ] AR-02: 커밋마다 맨 위 단위가 하나이고 메시지가 한국어이며 끝에 서명 줄이 있다 — Given 구현 커밋 뒤, When `38cccd1..<U>` 의 병합 아닌 커밋마다 바뀐 파일의 단위(`docs/<킷>/…` 는 `docs/<킷>`, `docs/` 바로 아래 파일은 `docs`, 그 밖은 맨 위 폴더)를 세고 메시지를 보면, Then 커밋이 1 개 이상이고 모든 커밋이 단위 1 개 · 첫 줄에 한글 · 빈 줄 없는 마지막 줄이 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` · 그 바로 앞 줄이 빈 줄이다 [exact]
  측정: `m AR-02` 가 `commits=<1 이상> bad=0` · 종료 코드 0
- [ ] AR-03: 계약이 봉인된 채이고 봉인 커밋이 구현보다 먼저이며 측정 묶음이 봉인 뒤 바뀌지 않았다 — Given 구현 커밋 뒤, When 끝 판의 이 계약과 측정 묶음을 보면, Then 구간에서 이 계약을 처음 담은 커밋의 파일이 1 개 · 그 커밋이 `.harness` 밖을 처음 고친 커밋의 조상 · `conditions_digest` · `measurement_digest` 가 다시 계산한 값과 같고, 묶음 지문이 아래와 같다 [exact]
  측정: `m AR-03` 이 `seal_commit_files=1 seal_before_impl=1 seal=OK measure=OK` 와 `bundle measure.sh=73f51c990ff750a2 pairs.txt=0dc11a65862edc3f baseline.tsv=b65107220c8e742d heads.tsv=23760ae2eb2baafb drift.py=b858aaf9d9bb2eff layout.js=806bb9c641ea5103 ext_cases.py=352a43fec341215d`
- [ ] AR-04: 묶음 기록에 커밋 목록 · tone-guide 5 단계 대조 · 조건별 자기 측정이 있다 — Given 구현 커밋 뒤, When 끝 판 `.harness/.meta/after-kaizen-0926b/dr1a-notes.md` 를 읽으면, Then 파일이 있고 `## 커밋 목록` · `## tone-guide 5 단계 대조` · `## 조건별 자기 측정` 머리가 각 1 개이며 tone-guide 절에 표 줄(`| ` 로 시작)이 3 줄 이상이다 [exact]
  측정: `m AR-04` 가 `notes=1 commits_h=1 tone_h=1 self_h=1 tone_rows=<3 이상>` (봉인 전 `notes=0`)

## Anti-patterns

- [ ] AP-02: force push 금지 — 이 가지를 원격에 밀지 않았다
  측정: `m AP-02` 가 `remote_heads=0` (봉인 전 같은 값)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: `m AP-03` 이 `rc=0 v6=[V6 code-fence        0 bare — OK]` (봉인 전 같은 값. 바뀌는 md 는 harness 킷의 설계 가이드 하나)

## Reusability

- [ ] RE-01: N/A (산출물이 문서 페이지 · 판정식 · CI 한 단계 · 문서 한 줄이라 재사용 단위 코드가 새로 생기지 않는다. 측정: `git diff --name-only --diff-filter=A 38cccd1..<U> -- . ':(exclude).harness'` 가 0 줄)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 페이지는 공통 파일 `docs/assets/site.css` 와 기존 검사 `scripts/check-api-kit-docs.py` 를 다시 쓰고 새 CSS · JS · 검사 파일을 만들지 않았다
  측정: `git diff --name-only --diff-filter=A 38cccd1..<U> -- docs scripts` 가 0 줄, 공통 링크는 SK-07

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only 38cccd1..<U> | grep -c '^scripts/release.sh$' 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 md 는 markdownlint-cli2 0.23.2(MD013 끔)로 0 건, 바뀐 py 는 컴파일 종료 코드 0
  측정: `m DG-02` 가 `md=rc0/[1]/[Summary: 0 issues in 0 files] py=rc0` (봉인 전 같은 값, `Linting: 1 file` 줄로 검사기가 돌았는지 함께 본다)
  양성 대조: MD013 을 켜면 같은 파일에서 `:1328:81 error MD013` 이 나온다 (봉인 전 실측)
- [ ] DG-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: DG-01 과 같은 명령)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 산출물이 정적 페이지 · 검사 스크립트 · CI 설정이다. 페이지를 브라우저로 열 때의 콘솔 오류는 SK-08 이 잰다. 측정: 바뀐 파일 가운데 서버 · 앱 시작 파일 0 개)
