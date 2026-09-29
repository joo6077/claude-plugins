---
feature: "마지막 정리 — 문서 사이트 밝은 테마 · 움직임 규칙 · 드리프트"
slug: after-0929-final-sweep-docs
created: "2026-09-29 10:24"
complexity: "복잡"
conditions: 25
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:34da4f58f14e406f
measurement_digest: sha256:e2e8c0f8d4737f10
locked_at: "2026-09-29 11:31"
---

## 배경

- 마지막 정리 목록 `.harness/.meta/after-kaizen-0928/final-sweep.md` 의 「d1 남은 것 / d1 검토 3」 네 행(묶음 fs2)을 처리한다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 앞 묶음 기록 `.harness/.meta/after-kaizen-0928/d1-notes.md` 「이 묶음 밖으로 남긴 것」. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-fs2`, 가지 `chore/ak3-fs2`, 시작 판 `BASE` = `cacd9da3` (가지 `chore/after-kaizen-0928` 끝 — ak3 열두 묶음 d1 · dz · ex · ex2 · h1 · h2 · id · k1 · lt · rec · orca3 · gd 가 합쳐진 판). 드리프트 다시 보기 기준 `DRIFT_SINCE` = `e500a63` (d1 이 쪽을 맞춘 기준 판. d1 은 `6378948` → `e500a63` 사이 원본 변경을 맞췄다).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-fs2` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력일 때 W 맨 위 폴더에서 잰다. 이 가지는 이 스프린트만 커밋하므로 HEAD 는 이 스프린트 끝과 같다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. 브라우저 측정은 W 의 `node_modules`(`npm ci`) 의 playwright 를 쓰고, `TMPDIR` 는 scratch 아래 폴더로 둔다.

항목별 처리 방침 (결정):

- **(1) 밝은 테마 118 쪽** — 대상은 시작 판에서 쪽 `<style>` 에 `[data-theme="light"]` 규칙이 없는 쪽이다(도우미 `dark_only()`, `docs/index.html` · `docs/design-kit/examples/moodboard-taskflow.html` 포함 118 개. 접근성 검사기 `theme=dark-only` 118 줄과 같다). 118 쪽의 색은 모두 같은 이름의 색 변수(`--bg` · `--bg2` · `--surface` · `--surface2` · `--border` · `--text` · `--text2` · `--text3` · `--accent` 등, `:root` 에 선언)로 쓰여 있어, 밝은 테마 색은 공통 파일 `docs/assets/site.css` 에서 이 변수들을 밝은 값으로 바꾸는 규칙으로 준다. 쪽마다 밝은 테마 CSS 를 새로 쓰지 않는다 — 쪽 `<style>` 에 새 선택자를 더하지 않는다(값만 변수로 바꾸는 것은 된다). 쪽에 더하는 것은 테마 단추 요소와 단추 · 저장 · 복원 스크립트뿐이고, 규칙은 docs-site Gotcha 13 과 틀 `.claude/skills/docs-site/references/page-template.html` 을 따른다 — 저장 키 `dk-theme`, 저장값이 없으면 브라우저 색 설정, `<html data-theme>` 로 테마를 건다. 단추 id 는 검사기가 재는 `theme-btn` 또는 `themeToggle`. 이미 밝은 테마가 있는 84 쪽은 자기 밝은 규칙을 그대로 쓰므로, 공통 파일의 밝은 규칙이 그 쪽들의 색을 덮지 않아야 한다(구조-03). 84 쪽의 밝은 규칙도 모두 `[data-theme="light"]` 이고 두 쪽 무리 모두 공통 파일 링크가 `<style>` 앞이라 같은 세기 선택자로는 가를 수 없다 — 그래서 공통 파일의 밝은 규칙은 새 단추가 있는 쪽에만 걸리게 단추 표지(`:root:has(.dk-theme-btn)`)로 좁힌다. 쪽 `<style>` 에 박힌 색 값이 밝은 배경에서 대비가 모자라면 값을 `var(--이름, 원래 값)` 꼴로 바꾼다 — 어두운 테마에서는 원래 값이 그대로 계산된다(구조-03 이 잰다).
- **(1-2) 접근성 검사기 고침** — 봉인 전 시험(scratch 사본에 공통 파일 밝은 규칙과 단추를 넣은 118 쪽)에서 검사기가 118 줄 모두 `theme=dark-only` 를 냈다. `file://` 로 연 쪽은 링크한 `docs/assets/site.css` 의 `cssRules` 를 읽으면 `SecurityError` 가 나 검사기가 공통 파일의 밝은 규칙을 못 본다(실측 `…/site.css ERR SecurityError`). 이대로면 밝은 테마 대비를 아무도 재지 않으므로 검사기를 고친다 — 규칙 목록을 뒤지는 대신 두 테마로 칠한 `html` · `body` 의 배경 · 글자색이 다르면 두 테마로 본다. 같은 시험에서 0.5 초 전환(`docs/design-kit/visual-hierarchy.html` `.td-cta` · `ratio-proportion.html`)이 끝나기 전에 재 어두운 대비가 틀리게 나왔으므로, 테마를 바꾼 뒤 도는 유한 애니메이션이 끝날 때까지 기다린다. 고친 검사기를 시작 판에 돌린 값은 옛 검사기와 같다(`202/202 PASS` · `theme=both` 84).
- **(2) 움직임 줄이기 106 쪽** — 시작 판에서 쪽 `<style>` 에 `prefers-reduced-motion` 을 다시 적은 쪽 106 개(도우미 `motion_pages()`, `reduce` 블록 105 · `no-preference` 블록 1 = `docs/design-kit/design-test.html`)의 쪽 안 규칙을 지우고 공통 파일이 맡는다. 그 가운데 31 쪽 안팎은 가리킬 때 들뜨는 카드(`.card:hover{transform:…}`)를 줄이기 설정에서 `transform:none` 으로 막고 있어, 공통 파일이 지금처럼 전환 시간만 줄이면 지운 뒤 카드가 다시 들뜬다(양성 대조: `docs/backend-kit/database.html` 에서 쪽 규칙만 지운 사본은 줄이기 설정에서 `hover_lifts=2`). 그래서 공통 파일이 줄이기 설정에서 가리킬 때의 움직임도 멈춰야 한다. 모든 `:hover` 의 `transform` 을 공통 파일이 `none` 으로 덮으면 안 된다 — 가리킨 요소의 조상도 `:hover` 라서, 가만히 있을 때 `transform` 을 가진 요소(봉인 전 실측: 11 쪽 89 개, 예 `docs/design-kit/image-illustration.html` `.focal-point` 가운데 맞춤)가 가리키는 순간 제자리를 잃는다. 그래서 쪽의 가리킬 때 `transform` 값(추적 쪽 74 쪽 130 곳)을 `var(--dk-hover-move, 원래 값)` 으로 바꾸고 공통 파일이 줄이기 설정에서 `--dk-hover-move` 를 `none` 으로 둔다. 움직임을 허용한 설정의 들뜸 · 애니메이션은 그대로 둔다(오류-02). 새 쪽이 규칙을 다시 적지 않게 공통 CSS 검사가 쪽 `<style>` 의 `prefers-reduced-motion` 을 위반으로 잡는다(스크립트-01). 스크립트로 주는 움직임(`behavior:'smooth'` 스크롤 등)은 공통 파일이 멈출 수 없어 이 계약 밖이다(docs-site Motion 규칙 그대로).
- **(3) 디자인 연구 기록** — `docs/design` 폴더에서 이름이 `-log.md` 로 끝나는 파일은 `docs/design/research-log.md` 하나다(`find docs/design -name '*-log.md'`). 드리프트 도구 매핑과 docs-site Step 1 표에 `docs/design/` → `docs/design-kit/` 을 넣고, 새 쪽 `docs/design-kit/research-log.html` 을 만들어 목차에 올린다. d1 결정표(`d1-notes.md` D5)의 다른 킷 연구 기록 여덟과 같은 처리다.
- **(4) 드리프트 다시 보기** — 시작 판에서 `python3 scripts/detect-docs-drift.py --since e500a63` (모양만 바뀐 원본은 도구가 기본으로 뺀다 — 뺀 짝 4 개) 가 내는 내용 바뀐 짝 31 개마다, 원본이 `e500a63` 뒤에 새로 얻은 인라인 코드 · 낱말을 쪽이 싣게 맞춘다. 그중 `react-kit/references/style-guide.md` 는 쪽이 없어(`[NEW`) d1 결정표의 react 참고 폴더 원칙(참고 문서마다 쪽 하나)대로 새 쪽 `docs/react-kit/style-guide.html` 을 만든다. 같은 마지막 정리의 다른 묶음(fs1)은 이 계약을 쓰는 지금 합쳐지지 않았다 — 그 묶음이 바꾸는 원본과 쪽은 그 묶음 계약 몫이다(`## 범위 경계`).

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 공통 CSS · 쪽 HTML · 쪽 스크립트, 목차(`docs/index.html`), 드리프트 도구, CI 검사(공통 CSS 검사 · 접근성 검사기) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 공통 파일이 모든 쪽의 밝은 테마 색과 움직임 줄이기를 맡는다. 공통 CSS 검사가 새 위반을 잡는다. 드리프트 매핑이 하나 는다 |
| 소비면 존재 | 반대편이 있는가 | 예 — `docs/assets/site.css` 를 링크한 추적 쪽 202 개 전부(밝은 테마가 이미 있는 84 쪽 포함), docs-site 스킬 글(Gotcha 1 · 13 · Motion 줄 · Step 1 표), `--check-table` CI 단계, 접근성 검사기 `scripts/check-docs-a11y.js`(공통 파일에 밝은 규칙이 생기면 모든 쪽을 두 테마로 잰다) |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 공통 밝은 규칙이 84 쪽의 밝은 색을 덮을 수 있고, 쪽 규칙을 지우면 줄이기 설정에서 카드가 다시 들뜨며, 공통 규칙을 넓게 잡으면 움직임 허용 설정의 들뜸까지 죽는다 |

기능 조건 17 개는 스킬-01 · 스크립트-01 · 스크립트-02 · 오류-01 · 오류-02 · 구조-01 ~ 구조-11 · 진단-05 다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절 · 자동 포함 여섯 줄 · `N/A (` 줄을 빼고 센 값이다. 복잡 가이드 9 ~ 20 안이다.

Step 2.5 짝 조건: 만드는 쪽은 공통 파일(구조-02 · 구조-06 · 오류-01)과 공통 CSS 검사(스크립트-01) · 드리프트 매핑(스크립트-02)이다. 쓰는 쪽은 추적 쪽 전부(구조-03 · 구조-04 · 구조-05 · 오류-02 — 이미 두 테마인 84 쪽을 따로 잰다), docs-site 스킬 글(스킬-01), CI 의 `--check-table` · 공통 CSS 검사 · 접근성 검사 단계(진단-05)다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | 진단-01 N/A (대상 파일이 이번 변경 밖) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 진단-03 N/A (같은 이유) |
| `diagnostics.ide_exclude` | `[]` | 진단-02 `[]` |
| `contract_categories[].id` / `prefix` | Skill/스킬 · Script/스크립트 · Error/오류 · Architecture/구조 | 같음 |
| `anti_patterns[].id` / `message` | 금지-01 버전 하드코딩 · 금지-02 force push · 금지-03 bare code fence · 금지-04 frontmatter name | 금지-02 · 금지-03 |

## GAP 분석 (Pre-Edit Audit)

모두 W 시작 판(`cacd9da3`)에서 연 값이다.

| 대상 | 읽은 증거 (`파일:줄` · 명령 출력) | 발견한 갭 | 조건 |
| --- | --- | --- | --- |
| `docs/assets/site.css` | `:1-14` — 행간 · 좁은 폭 줄바꿈 · `@media (prefers-reduced-motion: reduce)` 전환 · 애니메이션 시간만 줄임. `[data-theme="light"]` 0 | 밝은 테마 규칙 없음. 가리킬 때 `transform` 을 멈추지 않음 | 구조-02 · 구조-06 · 오류-01 |
| 어두운 테마만 있는 쪽 | 도우미 `m LISTS` → `pages=202 dark_only=118 motion_in_style=106`. 접근성 검사기 전체 실행 `theme=dark-only btn=none` 118 줄 · `theme=both` 84 줄 · `202/202 PASS` · 모든 줄 `of=0/0/0/0`. 118 쪽 `:root` 변수: `--bg` 118 · `--border` 118 · `--bg2` `--surface` `--surface2` `--text` `--text2` `--text3` `--accent` 117 (값도 `#0d0d14` · `#F5F0E8` 등 거의 하나) · `<html lang="ko">` 115 · `<html lang="ko" data-theme="dark">` 3 | 밝은 테마 · 단추 · 저장 없음 | 구조-01 · 구조-02 · 구조-05 |
| 이미 두 테마인 84 쪽 | 같은 검사기 줄 `theme=both`, 단추 없는 쪽 6 (`btn=none`) | 공통 밝은 규칙이 이 쪽들의 밝은 색을 덮으면 안 된다. 단추 없는 6 쪽은 이 계약 대상 밖 | 구조-03 |
| 쪽 안 움직임 줄이기 | 106 쪽의 규칙 모양 26 가지 — 가장 흔한 것 `*,*::before,*::after{transition:none!important;animation:none!important}html{scroll-behavior:auto}` 27 쪽, `.card:hover,.checklist li:hover{transform:none}` 을 곁들인 쪽 10 (예 `docs/backend-kit/database.html`), `docs/design-kit/design-test.html` 만 `no-preference` 안 `.feat-card:hover{transform:translateY(-2px)}` | 공통 파일과 겹치고, 가리킬 때 들뜸 멈춤은 쪽마다 따로 | 구조-06 · 오류-01 · 오류-02 |
| `scripts/check-docs-common-css.py` | `:1-108` — 링크 수 · 쪼갠 이름만 잰다. `python3 scripts/check-docs-common-css.py docs/backend-kit/database.html` → `검사한 쪽 1 · 어긋난 쪽 0` · 종료 코드 0 | 쪽 `<style>` 의 움직임 규칙을 못 잡는다 | 스크립트-01 |
| `scripts/test-check-docs-common-css.py` | `:1-16` 경우 다섯 · `--check <사본>` 음성 대조 선택지. 실행 `경우 5 개 중 통과 5` · 종료 코드 0 | 새 위반의 경우 없음 | 스크립트-01 |
| `scripts/check-docs-a11y.js` | `:123-127` 밝은 테마 판정이 `document.styleSheets` 의 `cssRules` 를 뒤진다 · `:71` 테마를 바꾼 뒤 0.5 초만 기다린다. scratch 시험 `…/site.css ERR SecurityError` · 118 줄 `theme=dark-only` | 공통 파일이 주는 밝은 테마를 못 재고, 0.5 초 넘는 전환 중에 잰다 | 구조-05 |
| `scripts/detect-docs-drift.py` | `:44-92` 접두 매핑에 `docs/design/` 없음. `--since 6378948 --include-format-only` 출력에 `docs/design/` 줄 0. `--check-table` → `매핑 맞대기: 스크립트 50 짝 · 표 34 짝 · 어긋남 0` | 연구 기록이 드리프트 밖 | 스크립트-02 |
| `docs/design/research-log.md` | 531 줄. `git diff --stat 6378948 HEAD` 11 줄 바뀜, `e500a63..HEAD` 0. `docs/design-kit/` 에 `research-log.html` 없음, 목차에 `design-research-log` 0 | 쪽 · 목차 없음 | 구조-07 |
| 드리프트 `--since e500a63` | 기본 출력 31 줄 · 표준 오류 「모양만 바뀐 원본의 짝 4 개를 뺐다」 · 종료 코드 0. `m 구조-08` → `pairs=31 bad=16`: GAP 15(`docs/api-kit/static-evidence-viewer-contract.html` 코드 4/4 · `docs/bambu-kit/bambu-print-profile.html` 코드 25/34 · 낱말 135/229 · `bambu-fields-baseline.html` 코드 1/25 · `failure-recipes.html` 낱말 3 · `seam-recipes.html` 2 · `docs/design-kit/material-design.html` 21/52 · `visual-change-protocol.html` 2 · `design-mockup.html` 1 · `docs/flutter-toolkit/research-log.html` 코드 2/2 · `docs/harness/contract-schema.html` 코드 1 · 낱말 4 · react 참고 다섯 쪽(`clean-arch-layout` · `common-gotchas` · `project-detection` · `result-patterns` · `wasm-catalog`) 설치본 안내 문장) · NOPAGE 1(`react-kit/references/style-guide.md`) | 다른 묶음이 바꾼 원본을 쪽이 못 따라감 | 구조-07 · 구조-08 |
| `.claude/skills/docs-site/SKILL.md` | `:16` Gotcha 1 이 「`transform` 움직임은 쪽이 `@media (prefers-reduced-motion: no-preference)` 안에서만 준다」 · `:32` Gotcha 13 에 `docs/assets/site.css` 0 · `:119` Motion 줄에 `transform` 0 · `:56` design-kit 표 줄에 `docs/design/` 0. `m 스킬-01` → `g1_checker=1 g1_no_preference_gone=0 g13_site_css=0 motion_transform=0 table_design_log=0`. markdownlint(MD013 끔) 0 건 | 새 규칙이 스킬에 없다 | 스킬-01 |
| 로컬 CI · CI 전용 단계 | `## 회귀 게이트` 봉인 전 실측 | 통과 중 | 진단-05 |

커버리지 해소 (Step 6.5 (4) 검출기가 낸 건): 아래 `## 회귀 게이트` 에 적는다.

## Skill

- [ ] 스킬-01: docs-site 스킬 글이 이번 규칙을 적는다 — `.claude/skills/docs-site/SKILL.md` 의 (a) Gotcha 1 줄이 `check-docs-common-css.py` · `prefers-reduced-motion` 을 말하고 옛 권고 `no-preference` 가 그 줄에 없고, (b) Gotcha 13 줄이 밝은 테마 색을 주는 `docs/assets/site.css` 를 말하고, (c) Motion 줄(`- **Motion**:`)이 `docs/assets/site.css` 와 `transform` 을 말하고, (d) Step 1 표 design-kit 줄에 `` `docs/design/` `` 가 있다. Given 공통 전제 G, When `m 스킬-01`, Then `g1_checker=1 g1_no_preference_gone=1 g13_site_css=1 motion_transform=1 table_design_log=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-01` (없어야 할 `no-preference` 는 글자 참조를 풀어서 찾는다. 줄 머리 `1. **외부 리소스 금지**` · `13. **테마 토글을 넣으면 영속화까지**` · `- **Motion**:` · `| design-kit |` 로 줄을 골라 글자를 찾는다). 시작 판 `g1_checker=1 g1_no_preference_gone=0 g13_site_css=0 motion_transform=0 table_design_log=0` · 종료 코드 1

## Script

- [ ] 스크립트-01: 공통 CSS 검사가 쪽 `<style>` 의 움직임 줄이기 규칙을 잡는다 — `scripts/check-docs-common-css.py` 가 쪽 `<style>` 안(HTML 주석 · CSS 주석 뺌)에 `prefers-reduced-motion` 이 있는 쪽을 어긋난 쪽으로 한 줄에 적고, 본문 글 · `<code>` · `<script>` 의 `matchMedia('(prefers-reduced-motion: reduce)')` 는 잡지 않는다. 새 경우 6 이 `scripts/test-check-docs-common-css.py` 에 있다: ① `<style>` 에 `@media (prefers-reduced-motion: reduce){…}` 인 쪽과 정상 쪽을 함께 → 종료 코드 1, 앞 쪽 이름만 적힘 ② 본문 `<code>prefers-reduced-motion</code>` · `<script>` 의 `matchMedia` · `<style>` 안 CSS 주석에만 이름이 있는 쪽 → 종료 코드 0. 레포에서 인자 없이 부르면 통과한다. Given 공통 전제 G, When 아래 측정, Then 시험 종료 코드 0 · 끝 줄 `경우 6 개 중 통과 6`, 검사 종료 코드 0 · 끝 줄 `검사한 쪽 204 · 어긋난 쪽 0 · 못 읽은 쪽 0` [exact, enumerated]
  측정: `python3 scripts/test-check-docs-common-css.py; echo $?` 와 `python3 scripts/check-docs-common-css.py; echo $?`, `grep -c 'scripts/test-check-docs-common-css.py' .github/workflows/ci.yml` 1 이상(이미 등록됨). 시작 판: 시험 `경우 5 개 중 통과 5`, 검사 `검사한 쪽 202 · 어긋난 쪽 0 · 못 읽은 쪽 0`, 결함 재현 `python3 scripts/check-docs-common-css.py docs/backend-kit/database.html` → 종료 코드 0 (봉인 전 실측)
  음성 대조: 검사 사본에서 새 움직임 규칙 세기를 지우고 `python3 scripts/test-check-docs-common-css.py --check <사본>` 로 부르면 경우 6 ① 이 실패해 종료 코드가 0 이 아니다. 주석 빼기를 지운 사본은 경우 6 ② 가 실패한다
- [ ] 스크립트-02: 디자인 연구 기록이 드리프트 매핑에 있다 — `python3 scripts/detect-docs-drift.py --since 6378948 --include-format-only` 출력에서 `docs/design/` 로 시작하는 줄이 정확히 `docs/design/research-log.md → docs/design-kit/research-log.html` 하나(`[NEW` 표지 없음)이고, `--check-table` 이 종료 코드 0 · 끝 줄에 `어긋남 0` 이다(스크립트 매핑과 스킬 표를 함께 고친다). Given 공통 전제 G, When `m 스크립트-02`, Then `lines=['docs/design/research-log.md → docs/design-kit/research-log.html'] drift_rc=0 check_table_rc=0` · 종료 코드 0 [exact]
  측정: `m 스크립트-02`. 시작 판 `lines=[] drift_rc=0 check_table_rc=0 check_table_tail=[매핑 맞대기: 스크립트 50 짝 · 표 34 짝 · 어긋남 0]` · 종료 코드 1
  양성 대조: 스크립트 매핑에만 `("docs/design/", "docs/design-kit/")` 를 넣은 scratch 사본 → `표에 없는 짝 (스크립트에만): docs/design/ → docs/design-kit/` · `어긋남 1` · `check_table_rc=1`, 쪽이 없어 `[NEW` 표지가 붙은 줄 → 도우미 종료 코드 1 (봉인 전 실측)

## Error

- [ ] 오류-01: 움직임 줄이기 설정에서 움직임이 실제로 멈춘다 — 추적 쪽 전부(204 개)를 브라우저 움직임 줄이기 설정(`reducedMotion: 'reduce'`)으로 열어 0.5 초 뒤: 한 번 도는 길이(`getComputedTiming().activeDuration`)가 0.02ms 를 넘는 애니메이션 0 (`document.getAnimations()` 전부 — 재는 때에 따라 갈리지 않게 상태가 아니라 길이로 센다), 모든 요소의 가장 긴 전환 시간 0.01ms 이하, 이름 있는 애니메이션의 가장 긴 시간 0.01ms 이하, 맨 위 요소 `scroll-behavior` 가 `auto`, 그리고 지금 적용되는 규칙 가운데 `:hover` 에서 `transform` · `translate` · `scale` · `rotate` 를 주는 선택자마다 첫 대상 요소를 가리켜도 그 값이 바뀌지 않는다(`hover_lifts=0`). Given 공통 전제 G, When `m 오류-01`, Then `pages=204 bad=0 br_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01` (`node .harness/.meta/after-0929-final-sweep-docs/br.js motion reduce <쪽...>`). 시작 판 `pages=202 bad=41 br_rc=0` · 종료 코드 1 (41 쪽이 줄이기 설정에서도 가리키면 들뜬다 — 예 `docs/backend-kit/api-design.html` `hover_lifts=2`. 같은 측정을 두 번 돌려 출력이 글자까지 같았다). 양성 대조: `docs/backend-kit/database.html` 에서 쪽 `reduce` 블록만 지운 scratch 사본(공통 파일은 시작 판 그대로)은 `hover_lifts=2`, 원본은 `hover_lifts=0` (봉인 전 실측)
- [ ] 오류-02: 움직임을 허용한 설정의 움직임은 그대로다 — 시작 판 202 쪽을 움직임 허용 설정(`reducedMotion: 'no-preference'`)으로 열어 잰 `hover_lifts`(가리킬 때 들뜨는 요소 수) · `endless`(끝없이 도는 애니메이션 수) · `transition_ms`(가장 긴 전환) 세 값이 쪽마다 시작 판과 같다(시작 판은 `git archive cacd9da3 docs` 를 임시 폴더에 풀어 같은 명령으로 잰다). Given 공통 전제 G, When `m 오류-02`, Then `pages=202 changed=0` · `br_rc=0,0` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02`. 시작 판 자기 대조(시작 판 대 시작 판) `pages=202 changed=0 base_hover_lifts=127 br_rc=0,0` · 종료 코드 0 (봉인 전 실측 — 측정이 재는 때마다 흔들리지 않는다). 양성 대조: 오류-01 의 사본처럼 공통 파일에 `*:hover{transform:none!important}` 를 줄이기 조건 없이 넣은 scratch 사본은 `docs/design-kit/design-test.html` 의 `hover_lifts` 가 1 → 0 으로 바뀐다 (봉인 전 실측)

## Architecture

- [ ] 구조-01: 테마 단추 규약이 돈다 — 어두운 테마만 있던 118 쪽(도우미 `dark_only()`)과 새 쪽 둘(`docs/design-kit/research-log.html` · `docs/react-kit/style-guide.html`), 모두 120 쪽마다: 저장값 없이 밝은 색 설정 브라우저로 열면 `<html data-theme>` 이 `light`, 어두운 색 설정이면 `dark`, 어두운 설정에서 단추(`#theme-btn` 또는 `#themeToggle`)를 누르면 `light` 로 바뀌고 `localStorage` 의 `dk-theme` 이 `light` 이며 다시 열어도 `light`, 누르기 전후 본문 배경색이 다르고, 단추 가로 · 세로가 44 이상이다. Given 공통 전제 G, When `m 구조-01`, Then `theme_ok=120/120 br_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-01` (`node .harness/.meta/after-0929-final-sweep-docs/br.js theme <쪽...>`). 시작 판 `theme_ok=0/120 br_rc=0` · 종료 코드 1 (118 쪽 모두 `first_light=null first_dark=null click=none`, 새 쪽 둘은 파일 없음). 좋은 예 `docs/onboarding-kit/setup-guide.html` → `first_light=light first_dark=dark click=light stored=light reload=light bg_differs=1 btn=60x44` (봉인 전 실측)
  양성 대조(일부만 깨진 사본, 시작 판 scratch 복제본): 단추에 `style="min-height:0;height:30px"` 를 붙인 사본 → `btn=60x30`(44 미만이라 도우미가 BAD), 저장 줄을 지운 사본 → `stored=null reload=dark`(BAD) (봉인 전 실측)
- [ ] 구조-02: 밝은 테마 색은 공통 파일이 준다 — 어두운 테마만 있던 118 쪽마다 쪽 `<style>`(주석 뺌)에 시작 판에 없던 선택자가 0 개이고, `data-theme` · `prefers-color-scheme` · `theme-btn` · `themeToggle` 글자가 0 이며, `style=` 속성 수가 시작 판보다 늘지 않는다. 그리고 `docs/assets/site.css`(주석 뺌)에 `[data-theme="light"]` 가 1 회 이상 있다. Given 공통 전제 G, When `m 구조-02`, Then `pages=118 bad=0 site_css_light_rules=` 1 이상 · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02`. 시작 판 `pages=118 bad=0 site_css_light_rules=0` · 종료 코드 1. 양성 대조: 도우미 `selectors()` 로 `.card{color:red}` 쪽과 `.card{color:var(--x)}.theme-new{color:red}` 쪽을 맞대면 새 선택자 `{'.theme-new'}`, 값만 바꾼 쪽은 빈 집합. 도우미 전체 흐름도 시작 판 scratch 복제본에서 `docs/backend-kit/database.html` `<style>` 에 `.theme-new{color:red}`, `docs/backend-kit/api-design.html` `<body>` 에 `style=` 를 넣으면 `BAD … new_selectors=['.theme-new']` · `BAD … style_attrs=0->1` · `pages=118 bad=2` · 종료 코드 1 (봉인 전 실측). `<style>` 글은 글자 참조를 풀어서 잰다(`prefers&#45;reduced-motion` 같은 우회를 잡는다)
- [ ] 구조-03: 이미 있던 색은 그대로다 — 시작 판 202 쪽 모두의 어두운 테마 색 지문, 시작 판에서 밝은 테마가 있던 84 쪽의 밝은 테마 색 지문이 시작 판과 같다. 색 지문은 테마를 브라우저 색 설정 · `dk-theme` 저장값 · `<html data-theme>` 셋 다 같은 값으로 고정하고 색 전환이 도는 중에 재지 않도록 움직임 줄이기 설정으로 1280 폭에서 연 뒤 0.3 초 기다려, 글자를 직접 가진 요소마다(테마 단추 `#theme-btn` · `#themeToggle` 안은 뺌) 태그 · 글자색 · 배경색과 body 배경 · 글자색을 모은 목록의 sha256 앞 16 자리다. Given 공통 전제 G, When `m 구조-03`, Then `dark_pages=202 light_pages=84 changed=0 br_rc=0,0,0,0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03`. 시작 판 자기 대조(시작 판 대 시작 판) `dark_pages=202 light_pages=84 changed=0 br_rc=0,0,0,0` · 종료 코드 0 (봉인 전 실측. 움직임 허용 · 0.05 초 기다림으로 쟀던 첫 판은 색 전환 중에 재 3 쪽이 스스로와 달랐다 — 그래서 위 고정 방법을 쓴다). 양성 대조: `docs/onboarding-kit/setup-guide.html` 의 `--text:` 값 하나를 바꾼 scratch 사본은 지문 `8989806b9b7432a2` → `ca0ba1621c3e1290`, 바꾸지 않은 사본은 다른 폴더에서도 `8989806b9b7432a2` (봉인 전 실측)
- [ ] 구조-04: 추적 쪽 전부(204 개)가 두 테마(`dark` · `light`, 구조-03 과 같은 고정 방법) 각각 320 · 375 · 1280 폭에서 가로 넘침(`scrollWidth - clientWidth`, 폭을 바꾼 뒤 0.2 초 기다려 잰다) 0 이다. Given 공통 전제 G, When `m 구조-04`, Then `pages=204 themes=2 bad=0 br_rc=0,0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-04`. 시작 판 `pages=202 themes=2 bad=0 br_rc=0,0` · 종료 코드 0 (어두운 테마만 있던 쪽은 밝은 테마로 고정해도 어두운 모양 그대로라 지금은 한 테마만 잰 셈이다). 양성 대조: `docs/onboarding-kit/setup-guide.html` 의 `<body>` 바로 뒤에 폭 2000px 상자를 넣은 scratch 사본 → `of=1680/1625/720` (봉인 전 실측)
- [ ] 구조-05: 접근성 검사기를 docs 전체에 돌리면 모든 줄이 `OK` 이고 `theme=both` 이며(대비는 어두운 · 밝은 두 번 잰다 — 검사기가 밝은 규칙이 있는 쪽만 밝은 테마로 재므로 `theme=both` 가 곧 두 테마 대비 측정이다) 끝 줄이 `204/204 PASS` 다. 넘침 기준은 검사기 것(768 포함 네 폭 2px 이하)이고, 두 테마 넘침 0 은 구조-04 가 잰다. Given 공통 전제 G, When `m 구조-05`, Then `rows=204 fail=0 theme_both=204 tracked=204 tail=[204/204 PASS] rc=0` · 종료 코드 0 [exact]
  측정: `m 구조-05` (`node scripts/check-docs-a11y.js` 인자 없이). 시작 판 `rows=202 fail=0 theme_both=84 tracked=202 tail=[202/202 PASS] rc=0` · 종료 코드 1. 단추 크기도 이 검사기가 `theme-btn` · `themeToggle` 둘 다 잰다(B7 은 앞 묶음에서 풀림) — 단추 규약 전체는 구조-01 이 잰다
  양성 대조: 공통 파일 밝은 규칙과 단추를 넣은 scratch 사본 118 쪽 — 옛 검사기 `theme=dark-only` 118 줄(결함 재현), 고친 검사기 `theme=both` 118 줄. 음성 대조: 같은 사본에서 단추와 스크립트만 지운 `ctl-nobtn.html` → 고친 검사기 `btn=none theme=dark-only` (봉인 전 실측)
- [ ] 구조-06: 쪽 안 움직임 줄이기 규칙이 없다 — 추적 쪽 204 개 모두 `<style>`(HTML · CSS 주석 뺌)에 `prefers-reduced-motion` 0 쪽이고, `docs/assets/site.css` 에 `@media (prefers-reduced-motion: reduce)` 블록이 1 개 이상 있다. Given 공통 전제 G, When `m 구조-06`, Then `pages=204 style_motion_pages=0 base_motion_pages=106 site_reduce_blocks=` 1 이상 · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-06` (`<style>` 글은 글자 참조를 풀어서 잰다 — 글자 참조로 적은 규칙은 브라우저가 풀지 않아 규칙으로 돌지도 않는다). 시작 판 `pages=202 style_motion_pages=106 base_motion_pages=106 site_reduce_blocks=1` · 종료 코드 1
- [ ] 구조-07: 새 쪽 둘 — `docs/design-kit/research-log.html`(원본 `docs/design/research-log.md`) · `docs/react-kit/style-guide.html`(원본 `react-kit/references/style-guide.md`)마다 쪽이 `wc -l` 기준 400 줄 이상, `docs/index.html` 에 그 쪽 `file:` 항목이 정확히 하나이고 그 id 가 목차 전체에서 하나뿐이며 `getIcon` 에 같은 id 아이콘이 있고, `assets/site.css` 링크가 하나다. 원본 담김은 낱말 비율 0.95 이상 · 인라인 코드 전부 · 코드 블록 줄(공백 뺀 8 글자 이상) 전부다. Given 공통 전제 G, When `m 구조-07`, Then 두 줄 `OK` · `new_pages_ok=2/2` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-07`. 시작 판 두 쪽 `MISSING` · `new_pages_ok=0/2` · 종료 코드 1
  양성 대조: 시작 판 scratch 복제본에 원본 앞 절반만 `<pre>` 로 실은 400 줄 넘는 쪽 → `BAD … wr=0.55 code=58/138 fence=6/6`, 원본 전부를 실었지만 목차에 안 올린 쪽 → `BAD … reg=0 … wr=1.00 code=37/37 fence=20/20` · `new_pages_ok=0/2` (봉인 전 실측)
- [ ] 구조-08: 드리프트 다시 보기 — `python3 scripts/detect-docs-drift.py --since e500a63` 기본 출력(모양만 바뀐 원본 뺌)의 짝마다 쪽이 있고 `[NEW` 표지가 없으며, 원본이 `e500a63` 뒤에 새로 얻은 인라인 코드 · 낱말(HTML 주석 · 울타리 줄 · 표 구분 줄 뺌, 낱말 앞뒤 `.` · `-` 뺌)이 모두 쪽의 보이는 글이나 링크 주소에 있다. Given 공통 전제 G, When `m 구조-08`, Then `pairs=31 bad=0 drift_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-08` (짝 31 개는 `## GAP 분석` 의 드리프트 행과 도구 출력 그대로다). 시작 판 `pairs=31 bad=16 drift_rc=0` · 종료 코드 1
  양성 대조: 시작 판에서 `OK` 인 짝 `docs/bambu-kit/surface-recipes.html` 에서 원본이 새로 얻은 낱말 `0.001728` 하나를 지운 scratch 사본 → 그 짝 `GAP … word_miss=1/137` · `pairs=31 bad=17` (봉인 전 실측 — `OK` 짝이 못 읽어서 통과한 것이 아니다)
- [ ] 구조-09: 기록 — `.harness/.meta/after-kaizen-0928/fs2-notes.md` 에 (a) 네 항목(`밝은 테마` · `움직임 줄이기` · `research-log` · `드리프트`)마다 처리 커밋 해시, (b) `tone-kit:tone-guide` 1 단계와 5 단계를 돌린 결과(새로 쓴 한국어 글 · 스크립트 주석 · 쪽 스크립트가 대상), (c) 이 묶음 밖으로 남긴 것 — 단추 없는 두 테마 쪽 6 개, 스크립트로 주는 움직임, 합쳐지지 않은 묶음 fs1 — 과 (d) 단추 · 규칙 · 새 쪽을 만든 도구 폴더 `.harness/.meta/after-0929-final-sweep-docs/tools/` 가 있다. Given 공통 전제 G, When 아래 측정, Then 모든 값 1 이상 [exact, enumerated]
  측정: `for k in '밝은 테마' '움직임 줄이기' 'research-log' '드리프트' 'tone-guide' 'fs1' '6 개' 'after-0929-final-sweep-docs/tools/'; do printf '%s=%s\n' "$k" "$(grep -cF -- "$k" .harness/.meta/after-kaizen-0928/fs2-notes.md)"; done` 가 모두 1 이상, 그리고 `grep -cE '[0-9a-f]{8}' .harness/.meta/after-kaizen-0928/fs2-notes.md` 4 이상. 시작 판 파일 없음
- [ ] 구조-10: 바뀌거나 새로 생긴 docs 파일(`.html` · `.css` · `.js`)이 레포 밖 자원을 부르지 않는다 — `<script>` · `<img>` · `<iframe>` 의 `src`, `<link>` 의 `href`, CSS `@import` · `url()` 에서 `http://` · `https://` · `//` 로 시작하는 주소를 큰따옴표 · 작은따옴표 · 따옴표 없음 모두 센다(본문 `<a href>` 는 세지 않는다). Given 공통 전제 G, When `m 구조-10`, Then `checked` 1 이상 · `ext_files=0` · 종료 코드 0 [exact]
  측정: `m 구조-10`. 시작 판 `checked=0 ext_files=0` · 종료 코드 1 (바뀐 파일 없음)
  양성 대조: 시작 판 scratch 복제본에 `<script src='https://…'>` (작은따옴표) · `<img src=//…>` (따옴표 없음) · 공통 파일 `@import url("https://…")` 를 넣어 커밋한 뒤 → `EXT` 세 줄 · `checked=3 ext_files=3` · 종료 코드 1 (봉인 전 실측)
- [ ] 구조-11: 커밋 규칙 — `cacd9da3..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(문서 사이트는 `docs/<폴더>` 하나 — `docs/assets` 도 한 폴더 — 에 `docs/index.html` 을 더해도 된다)이며, `.harness/` 파일은 구현 파일과 다른 커밋이고, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이며, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-11`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-11`. 시작 판 `commits=0` · 종료 코드 1

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-fs2` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 바뀐 `.md` 두 파일(`.claude/skills/docs-site/SKILL.md` · `.harness/.meta/after-kaizen-0928/fs2-notes.md`)에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 밝은 테마 색 · 움직임 줄이기는 모든 쪽이 링크하는 `docs/assets/site.css` 한 곳에 둔다 — 구조-02 · 구조-06)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 테마 규약은 틀 `.claude/skills/docs-site/references/page-template.html` 의 `dk-theme` 규약을 따르고 — 구조-01, 새 검사를 만들지 않고 기존 `scripts/check-docs-common-css.py` 에 더하며 — 스크립트-01, 새 쪽은 공통 파일을 쓴다 — 구조-07)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only cacd9da3..chore/ak3-fs2 | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.md` 두 파일은 markdownlint-cli2 0.23.2(MD013 끔)로 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`, 바뀐 `.py` 는 `python3 -m py_compile` 종료 코드 0, 바뀐 `.js` 는 `node --check` 종료 코드 0
  측정: 파일마다 `<scratch>/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/fs2/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(설정 파일 내용 `{ "config": { "MD013": false } }`). 양성 대조: `#bad` 제목과 빈 줄 셋이 든 사본 `pos.md` → 경고 4 (봉인 전 실측). 시작 판 `.claude/skills/docs-site/SKILL.md` 0 건 · `Linting: 1 file`
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 정적 문서 쪽 · 공통 CSS · 검사 스크립트 · 기록. 측정: git diff --name-only cacd9da3..HEAD -- . ':(exclude).harness' | grep -cvE '^(docs/|scripts/|\.claude/skills/docs-site/)' 이 0. 쪽을 브라우저로 여는 확인은 구조-01 · 구조-03 · 구조-04 · 구조-05 · 오류-01 · 오류-02 가 한다)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` (TMPDIR 은 scratch 아래 새 폴더)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외)이고 `docs-a11y` 로그 끝이 `204/204 PASS`, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/test-check-docs-common-css.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `npx playwright test` 의 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 `grep -c 'rc=0' <TMPDIR>/ci-local/summary.txt`. 시작 판 ci-local 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `202/202 PASS`, CI 전용 단계 모두 0 (`12/12 PASS` · `어긋남 0` · `violations=0` · `실패 0 건` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `검사한 쪽 202` · `경우 3 개 중 통과 3` · `경우 5 개 중 통과 5` · `실패 0 건` · `실패 0 건` · `checked=6 violations=0`), `npx playwright test` `172 passed` (봉인 전 실측)

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다. 원본 문서(드리프트 매핑이 잡는 `.md` · `.yaml`)는 고치지 않는다 — 고치면 구조-08 의 짝 31 개와 새로 얻은 낱말이 흔들린다. 원본이 틀렸다고 보이면 기록에 남긴다. `docs/*.html` 은 docs 아래 HTML 전부다(원본 `.md` 는 들지 않는다).

```text
# sprint-scope
docs/*.html
docs/assets/
scripts/check-docs-a11y.js
scripts/check-docs-common-css.py
scripts/test-check-docs-common-css.py
scripts/detect-docs-drift.py
.claude/skills/docs-site/SKILL.md
.claude/skills/docs-site/references/page-template.html
```

- 하지 않는 것: 이미 두 테마인 84 쪽 가운데 단추가 없는 6 쪽에 단추 달기(대상이 어두운 테마만 있는 쪽이다), 스크립트로 주는 움직임 멈추기, 로컬 CI 도구 `ci-local.sh` 고치기(레포 밖 파일). 같은 마지막 정리의 fs1 묶음이 바꾸는 원본 · 쪽(목록 ex2 · dz · k1 · h1 · lt 행)은 이 가지에 없으므로 이 계약이 재지 않는다 — fs1 을 합친 뒤 드리프트는 그 판에서 다시 본다.
- 교차 진단 대조(봉인 전): 목록 A3 의 일곱 쪽은 모두 시작 판에서 이미 두 테마라 118 쪽에 없다(`dark_only()` 에 이름 0). 목록 A2 의 `[NEW` 는 기준 판 뒤에 바뀐 원본에만 붙는다 — 레포 첫 커밋부터 보면(`--since <첫 커밋> --include-format-only`) 쪽 없는 원본은 `react-kit/references/style-guide.md` (이 계약이 만든다) · `reflect-kit/references/memory-grounding.md` · `reflect-kit/skills/reflect-kaizen/SKILL.md` 셋이다. 뒤 둘은 네 항목 밖이라 기록 「남은 것」 에 적는다. 목록 D4 처럼 다시 만들 수단이 없어지지 않게 단추 넣기 · 움직임 블록 지우기 · 새 쪽 만들기 도구는 `.harness/.meta/after-0929-final-sweep-docs/tools/` 에 둔다(구조-09 (d)).
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. docs 는 `docs/<폴더>` 별로 커밋한다. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0929-final-sweep-docs/`)은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0929-final-sweep-docs/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 브라우저 측정은 같은 폴더의 `br.js`(`theme` · `paint` · `motion` 세 모드)를 부른다. 목록 `m LISTS` → `base=cacd9da3 pages=202 dark_only=118 motion_in_style=106`.
- 도우미가 쓰는 판: 시작 판 `cacd9da3` · 드리프트 다시 보기 기준 `e500a63` · 연구 기록 매핑 확인 `6378948`. 파일 지문은 봉인 커밋 직전에 `shasum -a 256 .harness/.meta/after-0929-final-sweep-docs/measure.py .harness/.meta/after-0929-final-sweep-docs/br.js | cut -c1-16` 로 뽑아 봉인 커밋 메시지에 적는다 — 봉인 뒤 도우미가 바뀌면 드러난다.
- 수 204 는 시작 판 추적 쪽 202 개에 새 쪽 둘(구조-07)을 더한 값이다. 쪽을 더 만들거나 지우면 스크립트-01 · 구조-04 · 구조-05 · 구조-06 · 오류-01 · 진단-05 의 수가 달라진다.
- 봉인 전 실측(2026-09-29, W 시작 판): 스킬-01 · 스크립트-02 · 구조-01 · 구조-02 · 구조-06 · 구조-07 · 구조-08 · 구조-10 모두 종료 코드 1(결함 재현). 값은 각 조건 측정 줄과 `## GAP 분석` 에 있다.
- 커버리지 해소: 스킬-01 — 네 경로 · 이름은 `m 스킬-01` 이 `.claude/skills/docs-site/SKILL.md` 에서 줄 머리로 고른 줄마다 글자 그대로 찾는다(`measure.py` 의 `m_skill`). 검출기는 측정 줄의 백틱만 본다.
- 커버리지 해소: 스크립트-01 — 두 스크립트는 측정 명령의 인자 자체다(`python3 scripts/…`). `<code>prefers-reduced-motion</code>` 는 경우 6 ② 의 사본 내용 설명이지 따로 재는 대상이 아니다.
- 커버리지 해소: 구조-01 — 새 쪽 둘은 도우미 `NEW_PAGES` 에 있고 `m 구조-01` 이 `dark_only()` 118 쪽과 함께 잰다(목록을 두 번 적지 않는다).
- 커버리지 해소: 구조-07 — 원본 · 쪽 짝 둘은 도우미 `NEW_PAGES` 한 곳에 두고 `m 구조-07` 이 쪽마다 `docs/index.html` 항목 · 아이콘 · `assets/site.css` 링크 수를 찍는다. `new_pages_ok=2/2` 는 기대 출력이다.
- 커버리지 해소: 구조-09 — 기록 파일 경로와 도구 폴더 이름은 측정 줄의 `for` 명령 안에 글자 그대로 있다(`grep -cF … .harness/.meta/after-kaizen-0928/fs2-notes.md`, 찾는 낱말 목록의 `after-0929-final-sweep-docs/tools/`). 검출기는 빈칸 든 백틱 덩어리를 건너뛴다.
- 오라클 해소: 스킬-01 — 스킬 문서에 적는 것 자체가 요구다. 적은 동작이 실제로 도는지는 스크립트-01 · 스크립트-02 · 구조-01 ~ 구조-06 · 오류-01 · 오류-02 가 도구 · 브라우저로 잰다.
- 오라클 해소: 스크립트-01 — 글자 찾기가 아니다. 시험 스크립트와 검사를 실제로 돌린 종료 코드 · 끝 줄로 판정하고, 음성 대조(움직임 규칙 세기 · 주석 빼기를 지운 사본)가 붙어 있다. `grep -c … ci.yml` 은 CI 등록 확인일 뿐이다.
- 오라클 해소: 구조-09 — 기록 파일을 남기는 것 자체가 요구다. 기록이 가리키는 동작은 다른 조건이 잰다.
- 오라클 해소: 진단-05 — 명령을 실제로 돌린 종료 코드와 요약 파일 `rc=0` 줄 수로 판정한다. 글자 찾기가 아니다.
- 오라클 해소: 진단-02 — 글자 찾기가 아니라 markdownlint · `py_compile` · `node --check` 를 실행해 그 출력으로 판정하고, 양성 대조(경고 4)를 봉인 전에 쟀다.
