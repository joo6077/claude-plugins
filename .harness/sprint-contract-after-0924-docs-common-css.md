---
feature: "문서 사이트 177 쪽을 공통 스타일 파일로 (d2) — 움직임 줄이기 · 본문 행간 1.7"
slug: after-0924-docs-common-css
created: "2026-09-26 17:42"
complexity: "복잡"
conditions: 26
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:11225a00534b06ba
locked_at: "2026-09-26 17:49"
---

## 배경

문서 사이트(`docs/`)의 HTML 177 쪽은 모두 자기 `<style>` 을 품고 있고 공용 스타일 파일은 0 개다. 그래서 사이트 전체에 같아야 하는 규칙 둘 — 움직임 줄이기(`prefers-reduced-motion: reduce` 일 때 애니메이션 · 전환 · 부드러운 스크롤을 끔)와 본문 행간 1.7 — 이 쪽마다 들쭉날쭉하다.
봉인 전 실측(시작 판 `4d1de5f`): 움직임 줄이기 규칙을 품은 쪽 119 · 없는 쪽 58, 움직임 줄이기를 흉내 냈을 때 계산값 기준으로 다 꺼지는 쪽 97 · 안 꺼지는 쪽 80, body 행간 선언 1.7 이 151 쪽 · 1.6 이 21 쪽 · 1.65 가 4 쪽 · 없음 1 쪽(`docs/index.html`).
같은 규칙 글자가 100 쪽 넘게 겹치는 것이 2 개뿐이라 「겹치는 규칙을 떼어 내는」 방식은 성립하지 않는다(과제 실측).
이 계약은 공통 파일 `docs/assets/site.css` 를 만들어 두 규칙만 담고, 177 쪽 모두에 그 파일을 거는 링크 한 줄을 넣고, 행간이 1.7 이 아닌 쪽의 body 행간 선언을 지워 공통 값을 따르게 하고, 새 쪽도 따르도록 docs-site 스킬의 틀과 안내를 고친다. 쪽마다 다른 스타일은 쪽에 그대로 둔다.

- 사용자 결정: AskUserQuestion(2026-09-26, 이 세션 `bda55d45-296c-491f-89ba-b52042d58e72`)에서 문서 사이트를 「공통 스타일 파일로」 — 가장 큰 변경인 줄 알고 골랐다. 근거 원문은 핸드오프 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-0110.md` §C4 5 번 「문서 사이트 공통 틀 177 쪽에 `prefers-reduced-motion` · 행간 1.7 — 큰 변경」(본 체크아웃, 읽기만)과 이 가지의 `.harness/.meta/after-kaizen-0926/d1-notes.md` 「넘긴 것과 사유」 마지막 행이다.
- 사용자 합의(Step 5): 사용자 위임으로 받은 것으로 적는다 — user 2026-09-26T01:04:21.505Z 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」
  (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`),
  그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(2026-09-24T04:04:16.964Z). 판단이 갈린 곳은 저장소 안 근거로 정했고 `## 범위 경계` 에 적었다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-docs`, 가지 `chore/ak-docs`. 이 가지는 통합 가지 `chore/after-kaizen-0926` 의 `39ddc12` 에서 갈라졌고 앞 묶음(d1)이 커밋을 더했다. 범위 구간의 아래 끝은 이 계약의 봉인 커밋(이 계약 파일을 처음 담은 커밋)의 부모다 — 해시를 박지 않고 측정 도우미가 git 기록에서 푼다. 봉인 전 실측 때 그 자리는 `4d1de5f` 였다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · `git add -A` · `git stash` · push · 가지 바꾸기 금지 · 본 체크아웃과 다른 워크트리는 건드리지 않는다. 구현 커밋은 셋이고 차례가 정해져 있다 — (1) 공통 파일 + 템플릿 · 스킬 안내 네 파일, (2) 177 쪽 링크, (3) 행간 고친 스물다섯 쪽. `.harness/` 파일은 구현 파일과 다른 커밋에 싣는다(AR-06).
- `scripts/` · 킷 폴더 · 쪽 본문 내용 · 쪽마다 다른 디자인은 고치지 않는다. 검사 도구가 새 링크를 못 다루면 도구를 고치지 말고 notes 에 적는다 — 이미 하나가 걸린다(AR-09, `## 범위 경계` 첫 행).
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 공통 파일의 주석과 스킬 안내 글도 한국어 기술 문체 규칙 대상이다. 결과는 notes 에 남긴다(AR-08).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · notes 커밋이 가지 `chore/ak-docs` 에 모두 들어간 뒤, 가지를 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 한다. 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(봉인 커밋의 부모)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다(DG-05 만 작업 폴더를 쓴다).
`HEAD` 를 상한으로 쓰지 않는다. `BASE` · `TIP` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.
「배포 흉내」 는 Playwright 가 `http://pages.test/claude-plugins/` 아래 요청을 가로채 트리의 `docs/` 파일을 경로 조각마다 대소문자를 가려 내주는 것이다 — GitHub Pages 가 `docs/` 를 그대로, 저장소 이름 아래 경로로 내보내는 모양을 흉내 낸다(`docs/.nojekyll` 이 있어 폴더를 가공하지 않는다).

복잡도 4 축 — 셋이 「예」 이고 「공개 약속 변경」 과 「쓰는 쪽」 이 둘 다 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.
기능 조건 17 개는 SK-01 ~ SK-04 · ER-01 · ER-02 · AR-01 ~ AR-10 · DG-05 이다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절(AP-03 · AP-04) · 자동 포함 여섯 줄(RE-01 · RE-02 · DG-01 ~ DG-04) · `N/A (` 줄(SC-00 · DG-01 · DG-03)을 빼고 센 값이다.
Step 2.5 짝 조건: 만드는 쪽은 공통 파일과 docs-site 스킬의 틀 · 안내(SK-01 ~ SK-04), 쓰는 쪽은 그 파일을 거는 177 쪽(AR-01 ~ AR-05 · ER-01 · ER-02)과 쪽을 읽는 검사 도구 넷 — `scripts/check-docs-links.py`(AR-10) · `scripts/check-api-kit-docs.py`(AR-09) · `scripts/check-docs-a11y.js` · `design-kit/evals/visuals.spec.js`(DG-04) — 이다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 하나 — 정적 문서 화면(HTML · CSS)과 그 틀을 만드는 스킬 안내 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 「쪽은 스타일을 모두 `<style>` 안에 둔다」(docs-site `SKILL.md:16`)가 「공통 파일 한 개 + `<style>`」 로 바뀌고, 177 쪽이 새 경로 `docs/assets/site.css` 에 기댄다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 177 쪽, 새 쪽을 만드는 템플릿, 쪽을 읽는 검사 도구 넷 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 행간이 바뀌는 스물여섯 쪽의 화면, 보통 모드에서 그대로여야 하는 151 쪽, 링크 경로가 배포에서 안 풀리면 177 쪽 모두 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 (새 notes 와 고치는 스킬 문서 둘) · AP-04 (docs-site `SKILL.md` 를 고친다). AP-01 은 더하는 줄에 판 번호가 들어갈 자리가 없어서(링크 줄 · CSS 규칙 · 안내 한 줄), AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 실제로 읽고 잰 값이다(시작 판 `4d1de5f`). 측정은 도우미와 같은 식이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `docs/**/*.html` 177 쪽 | `find docs -name '*.html'` 177 (깊이: `docs/index.html` 1 · `docs/<폴더>/` 175 · `docs/design-kit/examples/moodboard-taskflow.html` 1). 177 쪽 모두 `<head>` 안에 `<style>` 이 하나 있고 그 여는 줄이 자기 줄로 시작한다. `docs/design-kit/accessibility.html:299-339` 은 body 안에 `<style>` 여덟 개, `docs/design-kit/animation.html:562` · `docs/design-kit/feedback.html:337` 은 하나 더 | 공용 스타일 파일 0 개 · `docs/assets/` 없음. 움직임 줄이기 계산값 기준 안 꺼지는 쪽 80 (전환 · 부드러운 스크롤 36, 부드러운 스크롤만 16, 애니메이션 · 전환 · 반복 · 스크롤 14, 전환만 13, 애니메이션 · 반복 · 스크롤 1) | AR-01 · AR-04 |
| body 행간이 1.7 이 아닌 스물여섯 쪽 | `docs/reflect-kit/design.html:33` `line-height:1.6;` · `docs/backend-kit/caching.html:33` `html,body{…line-height:1.65;…}` · `docs/design-kit/examples/moodboard-taskflow.html:54` `line-height: 1.6;` · `docs/index.html:7-8` `<link rel="icon" href="data:,">` 다음 `<style>`, body 행간 선언 없음 | 1.6 스물하나 · 1.65 넷 · 없음 하나. 스물다섯 가운데 여덟(`caching` · `error-handling` · flutter-toolkit 여섯 `animation` · `performance` · `testing` · `state-management` · `flutter-ai-rules` · `primitive-substitution-gate`)은 `html,body` 를 한 규칙에 묶어 둬서 선언을 지우면 html 쪽 행간도 함께 빠진다 | AR-02 · AR-03 |
| `docs/design-kit/design-template.html` | `:7-9` CDN `preconnect` · Pretendard 외부 스타일 링크 다음 `<style>` | 177 쪽 가운데 이미 스타일 링크가 있는 유일한 쪽(외부 글꼴). 그대로 둔다 — 공통 파일 링크는 첫 `<style>` 앞에 따로 넣는다 | AR-01 · AR-02 |
| 스크립트로 부드럽게 움직이는 쪽 | `docs/design-kit/design-template.html:1047` · `grid-alignment.html:688` · `ratio-proportion.html:963` · `visual-hierarchy.html:819` `scrollTo({top:0,behavior:'smooth'}` · `docs/process/kaizen-flow.html:864` `scrollIntoView({ behavior: 'smooth' …` · `docs/flutter-toolkit/animation.html:397` `.animate(` | CSS 는 스크립트가 직접 준 움직임을 끄지 못한다 | 넘김 (`## 범위 경계`) |
| `.claude/skills/docs-site/SKILL.md` | `:5` description 「standalone HTML로 변환」, `:16` Gotcha 1 「외부 CSS/JS/font CDN 링크를 절대 추가하지 마라. 모든 스타일은 `<style>` 내 인라인.」, `:104` 「line-height 1.2~1.6배」, `:109` 「Motion: … prefers-reduced-motion 대응」 | `:16` 이 공통 파일 링크를 금지하는 글이다 — 안 고치면 스킬이 스스로 어긋난다. `:104` 는 킷 감사 기준을 옮긴 줄이라 사이트 값 1.7 과 어긋나지만 기준 문서가 킷 폴더에 있다 | SK-02 · AP-04. `:104` 는 넘김 |
| `.claude/skills/docs-site/references/page-template.html` | `:6-7` `<title>` 다음 `<style>`, `:22` `html{font-size:16px;scroll-behavior:smooth}`, `:25` body 의 `line-height:1.7`, `:26-27` 자리표시자 `{{ACCENT_R}}` 가 CSS 안에 있다 | 공통 파일 링크 없음. body 에 공통 파일이 맡을 행간이 적혀 있다 | SK-01 |
| `.claude/skills/docs-site/references/css-tokens.md` | `:56-72` 「사용 규칙」 1 ~ 6 | 공통 파일 안내 없음 | SK-03 · AP-03 |
| `scripts/check-api-kit-docs.py` | `:34` `EXTERNAL = re.compile(r'<link\s\|<script[^>]+src=\|@import\s\|…')` · `:69-70` 걸리면 「외부 리소스 참조」 | 어떤 `<link` 든 외부 리소스로 센다 — 공통 파일 링크를 넣으면 api-kit 열두 쪽이 모두 FAIL. CI(`.github/workflows/ci.yml`)와 `ci-local.sh` 에는 이 도구 단계가 없고, 부르는 스킬 · 스크립트도 없다(`grep -rn check-api-kit-docs` 가 `.harness/` 옛 계약에서만 나온다). 시작 판 `12/12 PASS` | AR-09 · 넘김 |
| `scripts/check-docs-links.py` | `:53-56` 태그의 `href` · `src` 를 모은다, `:77` 쪽 폴더 기준으로 풀어 존재를 본다, `:91` 쪽 수는 `*.html` 만 센다 | 새 링크를 내부 링크로 세고 존재를 본다 — 고칠 것 없음. 시작 판 `내부 상대링크 507 개` · `깨진 링크 없음` · `페이지 176 · 등록 176` | AR-10 |
| `scripts/check-docs-a11y.js` | `:40-47` `docs/` 아래 `*.html` 만 걷는다, `:123-127` 스타일 규칙을 읽다 막히면 `try/catch` 로 넘긴다 | 새 파일 · 새 링크로 깨질 자리 없음. 시작 판 `177/177 PASS` | DG-04 |
| `design-kit/evals/visuals.spec.js` | `:4-8` `docs/design-kit` 쪽을 `file://` 로 연다, `:13` 넘침 허용 쪽 넷, 화면 비교 기준 이미지 없음(`toHaveScreenshot` 0 건) | 보통 모드만 잰다. 시작 판 `143 passed` | DG-04 |
| `design-kit/skills/design-audit/references/audit-criteria.md` · `.claude/skills/kaizen-orchestrator/SKILL.md` | 앞 `:10` 「line-height가 font-size의 1.2~1.6배」 · 뒤 `:620` 「docs-site 스킬 원칙 (standalone, …)」 | 새 규칙과 어긋나는 글이 두 곳 더 있다. 둘 다 이 묶음 범위 밖 폴더다 | 넘김 |
| `docs/.nojekyll` | `git ls-files docs/.nojekyll` 1 줄 (`ef41bdd` 부터) | 배포가 폴더를 가공하지 않는다는 저장소 안 근거. Pages 원본 설정(가지 · 폴더)은 저장소 밖이라 확인할 수 없다 | ER-02 의 배포 흉내 |

구현 후보가 갈린 곳 — 저장소 안 근거로 하나씩 정했다.

| 갈린 곳 | 고른 것 | 버린 것 | 근거 |
| --- | --- | --- | --- |
| `SKILL.md:16` 「모든 스타일은 `<style>` 내 인라인」 | 그 문장을 「공통 파일 링크 한 줄 + `<style>` 인라인」 으로 바꾸고 같은 줄에 「공통 파일이 맡는 규칙은 쪽에 다시 적지 않는다」 를 둔다. CDN 금지 문장은 그대로 | 안내 줄만 더하고 `:16` 을 두기 | 두면 한 파일 안에서 「링크 금지」 와 「링크를 건다」 가 부딪힌다 |
| 템플릿 body 의 `line-height:1.7` | 지운다 | 두기 | 새 안내 줄이 「다시 적지 않는다」 이다 — 틀이 그 규칙을 어기면 새 쪽이 따라 어긴다. 177 쪽의 기존 1.7 선언과 기존 움직임 줄이기 규칙은 과제대로 그대로 둔다 |
| 공통 파일의 움직임 줄이기 내용 | 애니메이션 길이 · 전환 길이 0.01ms, 애니메이션 반복 1 회, 스크롤 `auto`, 모두 `!important` | 반복 횟수를 빼기 | 길이만 줄이고 반복을 두면 무한 반복 애니메이션이 0.01ms 마다 깜빡인다 — 「끈다」 가 아니다. 시작 판에 반복이 남는 쪽이 15 |
| 두 단계 아래 쪽의 경로 | `docs/design-kit/examples/moodboard-taskflow.html` 은 `../../assets/site.css` | 과제 문구대로 `../assets/site.css` | 과제는 「한 단계 아래는 `../`」 라고만 적었다. 쪽 폴더에서 `docs/assets/site.css` 까지의 상대 경로를 계산한 값을 쓴다 |

## Skill

- [ ] SK-01: 새 쪽의 틀 `.claude/skills/docs-site/references/page-template.html` 이 공통 파일을 건다 — `<head>` 안 첫 `<style>` 앞에 `<link rel="stylesheet" href="../assets/site.css">` 한 줄이 정확히 1 번 있고, body 규칙의 `line-height` 선언이 빠지며(공통 파일이 맡는 규칙을 다시 적지 않는다), 그 두 곳 말고는 바뀌지 않는다(공백 · 세미콜론만 다른 것은 같다고 본다). Given 공통 전제 G, When `m SK-01`, Then `tpl_link=1 tpl_before_style=1 tpl_body_lh=none tpl_shape=1` (시작 판 `tpl_link=0 tpl_before_style=0 tpl_body_lh=1.7 tpl_shape=0`). 양성 대조: 나쁜 판(템플릿 body 행간을 되살림) → `tpl_body_lh=1.7 tpl_shape=0` (봉인 전 실측) [exact]
- [ ] SK-02: docs-site `SKILL.md` 가 새 규칙을 한 곳에 적고 스스로 어긋나지 않는다 — 외부 CDN 금지 문장 「외부 CSS/JS/font CDN 링크를 절대 추가하지 마라」 가 정확히 1 번 남고, 옛 문장 「모든 스타일은 `<style>` 내 인라인」 은 0 번, 「공통 파일이 맡는 규칙은 쪽에 다시 적지 않는다」 가 정확히 1 번이며 그 줄에 `assets/site.css` 가 함께 있다. 머리 설정(첫 `---` 블록)은 글자 그대로이고, 이 파일의 더한 줄은 2 이하 · 뺀 줄은 1 이하다. Given 공통 전제 G, When `m SK-02`, Then `skill_fm_same=1 skill_cdn=1 skill_old_inline=0 skill_phrase=1 skill_phrase_line=1` · `numstat SKILL.md=<더한>/<뺀>` 이 더한 ≤ 2 · 뺀 ≤ 1 (시작 판 `skill_fm_same=1 skill_cdn=1 skill_old_inline=1 skill_phrase=0 skill_phrase_line=0` · 빈 값). 양성 대조: 나쁜 판 2(머리 설정의 `name` 줄을 지우고 description 글을 바꿈) → `skill_fm_same=0` · `numstat SKILL.md=2/3` (봉인 전 실측) [exact]
- [ ] SK-03: `.claude/skills/docs-site/references/css-tokens.md` 에 안내 한 줄만 더해진다 — 더한 줄 1 · 뺀 줄 0 이고, 「공통 파일이 맡는 규칙은 쪽에 다시 적지 않는다」 가 정확히 1 번이며 그 줄에 `assets/site.css` 가 함께 있다. Given 공통 전제 G, When `m SK-03`, Then `tokens_phrase=1 tokens_phrase_line=1` · `numstat css-tokens.md=1/0` (시작 판 `0` · `0` · 빈 값). 양성 대조: 나쁜 판 2(코드 울타리 세 줄을 더 붙임) → `numstat css-tokens.md=5/0` (봉인 전 실측) [exact]
- [ ] SK-04: 공통 파일 `docs/assets/site.css` 가 사이트 전체에 같아야 하는 두 규칙만 담고, `docs/` 아래 CSS 파일은 그 하나뿐이다 — 브라우저가 읽은 규칙 목록(주석은 빠진다)이 글자 그대로 `rule[body]{line-height:1.7} | media[(prefers-reduced-motion: reduce)]{rule[*, ::before, ::after]{animation-duration:0.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:0.01ms!important}}` 이다(`*::before` 는 브라우저가 `::before` 로 적는다 — 선택자는 `*, *::before, *::after` 로 쓰면 된다). Given 공통 전제 G, When `m SK-04` 가 배포 흉내로 `index.html` 을 열어 그 파일의 규칙을 찍으면, Then 첫 줄이 위 글과 같고 둘째 줄이 `css_files=docs/assets/site.css ` (시작 판 `sheet=absent` · `css_files=` 빈 값). 양성 대조: 나쁜 판(body 에 `color:red` 를 더하고 `docs/assets/extra.css` 를 만듦) → 첫 줄이 `rule[body]{color:red;line-height:1.7} | …` · `css_files=docs/assets/extra.css docs/assets/site.css ` (봉인 전 실측) [exact]

## Script

- [ ] SC-00: N/A (릴리스 스크립트 · 판 올리기 · `marketplace.json` 은 이 계약이 건드리지 않는다 — `docs/` 와 `.claude/skills/docs-site/` 는 어느 킷 폴더에도 속하지 않아 올릴 판이 없다. 측정: `m SC-00` 이 `release_paths=0` — 바뀐 경로 가운데 `scripts/` · `.claude-plugin/` 0 개. 양성 대조: 나쁜 판(`scripts/release.sh` 를 고쳐 커밋) → `release_paths=1`, 봉인 전 실측) [exact]

## Error

- [ ] ER-01: 177 쪽이 좁은 화면 · 넓은 화면 · 글자 간격이 넓어진 좁은 화면(CI 리눅스가 글자를 더 넓게 그리는 것을 맥에서 흉내)에서 가로로 넘치지 않는다 — Given 공통 전제 G, When `m ER-01` 이 배포 흉내로 쪽마다 어두운 색 설정 1280 폭으로 열고 375 폭으로 줄인 뒤, 마지막에 `*{letter-spacing:0.06em !important}` 를 넣어 375 폭에서 다시 재면, Then 세 경우 모두 `scrollWidth - clientWidth` 가 2 이하인 쪽이 177 이다 — 끝줄 `of_ok=177 ls_ok=177` (시작 판 `of_ok=177 ls_ok=177`). 양성 대조: 900px 폭 요소를 담은 임시 쪽 → `w375=` 2 초과로 `BAD`, 375 에서는 맞고 글자 간격에서만 넘치는 임시 쪽 → `w375=0 … ls375=` 2 초과로 `BAD` (봉인 전 실측) [exact, collective]
- [ ] ER-02: 177 쪽 모두 배포에서 공통 파일을 받아 읽고 오류가 없다 — Given 공통 전제 G, When `m ER-02` 가 배포 흉내(경로 조각마다 대소문자를 가림)로 쪽을 열면, Then 쪽마다 주 프레임이 요청한 공통 파일의 응답이 200 이고 그 파일의 규칙이 1 개 이상 읽히며(첫 화면 `index.html` 은 iframe 에 다른 쪽을 띄우므로 iframe 의 요청은 세지 않는다), 콘솔 오류 · 페이지 오류가 0 이다 — 끝줄 `css_ok=177 err_ok=177` (시작 판 `css_ok=0 err_ok=177`). 양성 대조: 나쁜 판(`docs/backend-kit/api-design.html` 의 href 를 `../Assets/site.css` 로 — 맥 파일 시스템은 대소문자를 무시해 `file://` 로는 풀린다) → 끝줄 `css_ok=176 … err_ok=176` (그 쪽 `css=404 err=1`), 링크 한 줄을 뺀 음성 대조 판 → `css_ok=175` (봉인 전 실측) [exact, collective]

## Architecture

- [ ] AR-01: 177 쪽 모두 공통 파일을 정확히 한 번, 정해진 자리와 글자로 건다 — 쪽마다 `docs/assets/site.css` 로 풀리는 스타일 링크가 정확히 1 개이고, 그 링크가 `<head>` 안 첫 `<style>` 보다 앞에 있으며, `href` 가 쪽 폴더에서 `docs/assets/site.css` 까지의 상대 경로(`docs/index.html` 은 `assets/site.css`, `docs/<폴더>/` 는 `../assets/site.css`, `docs/design-kit/examples/` 는 `../../assets/site.css`)와 글자 그대로 같고, 그 줄이 `<link rel="stylesheet" href="<그 경로>">` 한 줄뿐이다. 가리키는 파일은 끝점 git 트리에 대소문자까지 같은 이름으로 있다. Given 공통 전제 G, When `m AR-01`, Then `pages=177 one=177 before_style=177 href_exact=177 line_exact=177` · `css_tracked=1` (시작 판 `one=0 before_style=0 href_exact=0 line_exact=0` · `css_tracked=0`). 양성 대조: 나쁜 판(한 쪽에 링크 두 번 · 한 쪽은 `<style>` 뒤 · 한 쪽은 `../Assets/`) → `one=176 before_style=175 href_exact=175 line_exact=175` 와 세 쪽 이름 (봉인 전 실측) [exact, collective]
- [ ] AR-02: 쪽에서 바뀐 것은 링크 한 줄과 body 행간 선언뿐이다 — 도우미 `LH_PAGES` 의 스물다섯 쪽(1.6 스물하나 · 1.65 넷)은 끝점에서 링크 줄을 빼면 시작 판의 첫 `<style>` 안 body 규칙에서 `line-height` 선언만 지운 것과 같고(공백 · 세미콜론만 다른 것은 같다고 본다) body 규칙에 행간 선언이 남지 않으며, 나머지 152 쪽(`docs/index.html` 포함)은 링크 줄을 빼면 시작 판과 바이트까지 같다. Given 공통 전제 G, When `m AR-02`, Then `pages=177 same=177 lh_removed=25/25` (시작 판 `same=152 lh_removed=0/25`). 양성 대조: 나쁜 판(행간 쪽 `reflect-kit/design.html` 의 색 선언까지 바꿈 등) → `same=170 lh_removed=24/25` (봉인 전 실측) [exact, enumerated]
- [ ] AR-03: 보통 모드에서 177 쪽 모두 본문 행간이 1.7 이다 — Given 공통 전제 G, When `m AR-03` 이 움직임 줄이기 설정 없이(`no-preference`) 1280 폭으로 쪽을 열어 body 의 계산된 행간 ÷ 계산된 글자 크기를 소수 둘째 자리로 재면(배포 흉내와 `file://` 두 경로 모두), Then 둘 다 `1.70` 인 쪽이 177 — 끝줄 `lh_ok=177 lhf_ok=177` (시작 판 `lh_ok=151 lhf_ok=151` — 1.6 · 1.65 쪽과 `docs/index.html` 의 `normal`). 음성 대조: 모의 좋은 판에서 `docs/index.html` · `docs/reflect-kit/design.html` 의 링크 한 줄만 뺀 사본 → `lh_ok=175 lhf_ok=175`, 두 쪽 모두 `lh=normal` (봉인 전 실측) [exact, collective]
- [ ] AR-04: 움직임 줄이기 설정에서 177 쪽 모두 CSS 움직임이 꺼진다 — Given 공통 전제 G, When `m AR-04` 가 쪽을 연 뒤 `emulateMedia({ reducedMotion: 'reduce' })` 로 바꿔 모든 요소와 그 `::before` · `::after` 의 계산값을 재면, Then 애니메이션 길이 · 전환 길이의 가장 큰 값이 0.01ms 이하, 애니메이션 이름이 `none` 이 아닌데 반복 횟수가 1 이 아닌 요소 0, 스크롤이 `smooth` 인 요소 0 인 쪽이 177 — 끝줄 `rm_ok=177` (시작 판 `rm_ok=97`). 이 조건은 CSS 계산값만 잰다 — 스크립트가 직접 준 움직임(`scrollTo`/`scrollIntoView` 의 `smooth` 다섯 쪽, `.animate(` 한 쪽)은 재지 않고 `## 범위 경계` 로 넘긴다. 음성 대조: AR-03 의 링크를 뺀 사본 → `rm_ok=176` (`docs/index.html` 이 `trans=0.25` 로 잡힌다. `reflect-kit/design.html` 은 쪽 자체 규칙이 이미 전환을 꺼서 행간에서만 잡힌다) (봉인 전 실측) [exact, collective]
- [ ] AR-05: 행간 1.7 이 이미였고 움직임 줄이기도 있던 쪽은 보통 모드 화면이 그대로다 — 도우미 `PIX_PAGES` 의 다섯 쪽(`docs/api-kit/snapshot-sealing-canonicalization.html` · `docs/harness/feedback-system.html` · `docs/infra-kit/deployment-strategies.html` · `docs/planning-kit/prioritization.html` · `docs/tone-kit/comment-economy.html`)을 시작 판과 끝점에서 배포 흉내 · 어두운 색 설정 · 1280 폭 · 전체 높이로 캡처해(애니메이션은 끝난 상태로) 픽셀을 비교하면 크기가 같고 다른 픽셀이 0 이다. Given 공통 전제 G, When `m AR-05`, Then 다섯 줄 모두 `diff_px=0` · 끝줄 `pix_zero=5/5` (시작 판끼리 세 번 모두 `pix_zero=5/5`). 양성 대조: 나쁜 판 4(`feedback-system.html` 의 body 행간을 1.6 으로) → 그 줄이 `diff_px=-1`(높이가 달라짐) 또는 0 보다 큰 값 · `pix_zero=4/5` (봉인 전 실측) [exact, enumerated]
- [ ] AR-06: 구현 커밋은 정해진 셋이 정해진 차례로 들어가고 `.harness/` 와 섞이지 않는다 — `BASE` 부터 `TIP` 까지 병합 아닌 커밋 가운데 `.harness/` 밖 파일을 담은 커밋이 정확히 3 개이고, 차례대로 첫째는 도우미 `C1SET` 의 네 파일(공통 파일 · 템플릿 · `SKILL.md` · `css-tokens.md`)과 같고, 둘째는 시작 판의 177 쪽과 같으며 쪽마다 더한 줄 1 · 뺀 줄 0 이고, 셋째는 `LH_PAGES` 스물다섯 쪽과 같다. `.harness/` 파일과 그 밖의 파일을 한 커밋에 담은 것은 0 이다. Given 공통 전제 G, When `m AR-06`, Then `impl=3 c1=1 c2=1 c3=1 c2_plus1=177/177 mixed=0` (시작 판 `impl=0 c1=0 c2=0 c3=0 c2_plus1=0/177 mixed=0`). 양성 대조: 나쁜 판(모의 좋은 판 위에 쪽 · 공통 파일 · `scripts/release.sh` · notes 를 한 커밋에) → `impl=4 … mixed=1` (봉인 전 실측) [exact, enumerated]
- [ ] AR-07: 바뀐 파일이 기대 집합과 정확히 같고 계약 봉인이 깨지지 않는다 — `git diff --name-only BASE TIP -- . ':(exclude).harness'` 의 경로가 시작 판의 177 쪽과 `C1SET` 네 파일을 합친 181 경로와 같다(더 있는 것 0 · 빠진 것 0 — `scripts/` · 킷 폴더 · 다른 파일 없음, 생성물 없음). `.harness/` 는 이름을 열거하지 않고, 끝점 트리의 `sprint-contract*.md` 모두에 봉인 검사를 돌려 `SEAL_BROKEN` 이 0 이다. Given 공통 전제 G, When `m AR-07`, Then `changed=181 extra=0 missing=0` · `seal_broken=0` (시작 판 `changed=0 extra=0 missing=181` · `seal_broken=0`). 양성 대조: 나쁜 판 → `changed=183 extra=2` 와 `docs/assets/extra.css` · `scripts/release.sh`, 나쁜 판 3(앞 계약 `sprint-contract-after-0924-docs-regen.md` 의 조건 줄 한 글자를 바꿈) → `seal_broken=1` (봉인 전 실측) [exact, collective]
- [ ] AR-08: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926/d2-notes.md` 가 커밋돼 있고 열 토큰 `check-api-kit-docs` · `moodboard-taskflow` · `index.html` · `caching.html` · `audit-criteria` · `kaizen-orchestrator` · `scrollIntoView` · `.nojekyll` · `320px` · `tone-guide` 가 각각 한글 15 자 이상인 줄에 1 번 이상 든다(토큰만 늘어놓은 줄은 세지 않는다). 담을 내용: 새 링크를 외부 리소스로 세는 검사 도구와 그 결과(AR-09), 두 단계 아래 쪽의 경로, 행간 선언이 없던 첫 화면, `html,body` 를 묶은 여덟 쪽, 사이트 값과 어긋나는 행간 기준 · standalone 글 두 곳, 스크립트가 직접 준 움직임 여섯 쪽, 배포 판단 근거(`docs/.nojekyll` · 배포 흉내), 320px 넘침 넘김, `tone-guide` 1 · 5 단계 결과. 측정: `m AR-08` 이 `committed=1` 과 열 값 모두 1 이상 (시작 판 `committed=0` 과 0 열). 양성 대조: 토큰마다 한글 설명 줄을 담은 모의 notes → `committed=1` 과 1 열, 열 토큰을 한 줄에 늘어놓기만 한 notes → `committed=1` 과 0 열 (봉인 전 실측) [exact, enumerated]
- [ ] AR-09: 새 링크를 못 다루는 검사 도구 `scripts/check-api-kit-docs.py` 의 결과 변화는 「외부 리소스 참조」 한 가지뿐이다 — 도구는 고치지 않는다(AR-07 이 `scripts/` 변경 0 을 잰다). Given 공통 전제 G, When `m AR-09` 가 시작 판과 끝점에서 `python3 scripts/check-api-kit-docs.py --json` 을 돌려 쪽마다 FAIL 사유 집합을 비교하면, Then 끝점에서 새로 생긴 사유가 정확히 「외부 리소스 참조」 하나인 쪽이 12 이고, 그 밖의 사유가 새로 생기거나 사라진 쪽이 0 — `pages=12 base_fail=0 ext_only_new=12 other_change=0` (시작 판 `pages=12 base_fail=0 ext_only_new=0 other_change=0`, 텍스트 출력 끝줄 `12/12 PASS`). 양성 대조: 나쁜 판(api-kit 한 쪽에서 `prefers-reduced-motion` 글을 지움) → `ext_only_new=11 other_change=1` (봉인 전 실측) [exact]
- [ ] AR-10: 링크 검사 도구가 새 링크 177 개를 내부 링크로 세고 깨진 것이 없으며 쪽 등록은 그대로다 — Given 공통 전제 G, When `m AR-10` 이 시작 판과 끝점에서 `python3 scripts/check-docs-links.py` 를 돌리면, Then 두 줄 모두 `rc=0` · `broken0=1` · `페이지 176 · 등록 176` 이고 끝점의 `내부 상대링크` 개수가 시작 판보다 정확히 177 많다 (봉인 전 실측: 시작 판 `507 개`, 모의 좋은 판 `684 개`). 양성 대조: 나쁜 판(없는 쪽으로 가는 링크 하나 · 링크 하나 더) → 끝점 줄 `rc=1 내부 상대링크 686 개 broken0=0` (봉인 전 실측) [exact]

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이 계약에 적용: 새 notes 와 고치는 `SKILL.md` · `css-tokens.md`. V6 는 킷 폴더만 읽어 이 셋을 보지 않으므로 도우미 `bare` 가 V6 와 같은 셈(줄 앞 공백을 벗긴 뒤 백틱 셋으로 시작하면 열고 닫기를 번갈아 센다)을 돌린다. 측정: `m AP-03` 이 `bare: d2-notes.md=absent->0 SKILL.md=0->0 css-tokens.md=0->0` (시작 판 `absent->absent 0->0 0->0`). 양성 대조: 나쁜 판 notes → `d2-notes.md=absent->1`, 나쁜 판 2 → `css-tokens.md=0->1` (봉인 전 실측) [exact]
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이 계약에 적용: 고치는 `.claude/skills/docs-site/SKILL.md` 의 첫 머리 설정 블록에 `name` 이 그대로 있다. 측정: `m AP-04` 가 `fm_name=docs-site` (시작 판 같은 값). 양성 대조: 나쁜 판 2(`name` 줄을 지움) → `fm_name=` 빈 값 (봉인 전 실측) [exact]

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 이 계약에 적용: 사이트 전체 규칙을 쪽 폴더마다 두지 않고 `docs/` 아래 CSS 파일 하나에 두며 177 쪽이 모두 그 하나를 건다. 측정: `m RE-01` 이 `css_files=1 link_pages=177` (시작 판 `css_files=0 link_pages=0`). 양성 대조: 나쁜 판 → `css_files=2 link_pages=176` (봉인 전 실측) [exact]
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 이 계약에 적용: 공통 파일이 맡는 규칙을 쪽에 새로 적지 않는다 — 177 쪽의 더한 줄에 `prefers-reduced-motion` · `line-height` 가 0 줄. 측정: `m RE-02` 가 `added_rm=0 added_lh=0` (시작 판 같은 값). 양성 대조: 나쁜 판(한 쪽에 움직임 줄이기 규칙 · 한 쪽에 행간 선언을 새로 적음) → `added_rm=1 added_lh=1` (봉인 전 실측) [exact]

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_sh=0`. 양성 대조: 나쁜 판 → `release_sh=1`) [exact]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 177 쪽 가운데 짝 안 맞는 태그 수가 시작 판보다 늘어난 쪽 0 · 공통 파일의 중괄호 짝이 맞음 · notes 의 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0 · `SKILL.md` · `css-tokens.md` 경고 수가 시작 판 이하(시작 판 `SKILL.md` 9 — MD025 2 · MD031 2 · MD032 5, 이번 범위 밖 기존 경고). 측정: `m DG-02` 가 `tag_worse=0 css_bad=0 md_notes=0 md_skill=9->9` 이하 `md_tokens=0->0` (시작 판 `tag_worse=0 css_bad=1 md_notes=absent md_skill=9->9 md_tokens=0->0` — 공통 파일이 아직 없어 `css_bad=1`). 양성 대조: 닫히지 않은 `div` 를 담은 임시 쪽 → 태그 셈 1, 나쁜 판 notes(언어 없는 코드 울타리) → `md_notes=1` (봉인 전 실측). 설치가 안 되면(망 끊김 등) 도우미가 `md=ENV_FAIL` 을 찍는다 — 그 칸만 FAIL 이 아니라 `[미검증:ENV]` 로 적고, 나머지 칸은 그대로 판정한다 [exact]
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 `m DG-01` 이 `release_sh=0`) [exact]
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이 계약에 적용: 끝점 트리에서 레포 검사기 `node scripts/check-docs-a11y.js`(인자 없이 — `docs/` 177 쪽 전부의 넘침 375 · 768 · 1280 · 콘솔 오류 · 글자 대비 · 누르는 자리 크기)와 `npx playwright test design-kit/evals/visuals.spec.js` 를 돌린다. 측정: `m DG-04` 가 `a11y_rc=0 177/177 PASS` · `visuals_rc=0 143 passed` (실패 수 표시 없음) (시작 판 같은 값, 모의 좋은 판 같은 값). 음성 대조: 900px 로 넘치고 오류를 던지는 임시 쪽 → `check-docs-a11y.js` 가 `0/1 PASS` · 종료 코드 1 (봉인 전 실측). visuals 는 이 계약의 구현 지점(링크 · 행간 삭제)을 무력화해도 FAIL 하지 않는 기존 회귀 검사다 — 구현의 효과는 AR-03 · AR-04 가 잰다 [exact]
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력 — 아니면 도우미가 `W_NOT_TIP` 을 찍고 멈춘다), When `m DG-05` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌리고 그 도구 밖 CI 단계 `python3 scripts/run-kaizen-assertions.py` 도 따로 돌리면, Then 요약에 `rc=0` 줄이 22 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이며 kaizen 줄이 `Total: 14 passed, 0 failed` 다. 도구 파일은 이 가지 밖(본 체크아웃)에 있어 커밋으로 고정되지 않으므로 도우미가 그 내용 지문(`git hash-object`)을 봉인 때 값 `TOOL_BLOB` 과 대조해 `tool_same` 을 찍는다. 측정: `m DG-05` 가 `tool_same=1 rc0=22 other=[feedback-agg-test SKIP (yq 없음);] kaizen=[Total: 14 passed, 0 failed]` (시작 판 · 모의 좋은 판 봉인 전 실측: 같은 값). `tool_same=0`(도구 파일이 봉인 뒤 바뀜)이거나 요약 파일이 없으면(도우미가 `ci_summary=absent` 를 찍음) 그 회차는 PASS 도 FAIL 도 아니라 `[미검증:ENV]` 로 적는다. 음성 대조: 이 계약이 기대는 `docs-a11y` · `docs-links` · `playwright-visuals` 단계는 보통 모드 · 원래 글자 간격에서 재므로 링크를 빼도 통과한다 — 링크 · 행간 · 움직임은 AR-01 · AR-03 · AR-04 가, 글자 간격 넘침은 ER-01 이 잡는다 [exact]

## 범위 경계

항목별 처리 — 입력은 과제 목록 (1) ~ (4) 와 합격선, 그리고 Pre-Edit 감사에서 나온 것이다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| `scripts/check-api-kit-docs.py` 가 새 링크를 외부 리소스로 센다 (`:34` `<link\s`) | 계약에 넣음 (결과 변화만 잠금) · 도구 고치기는 넘김 | AR-09 · AR-08. 과제가 「검사 도구가 새 링크를 못 다루면 고치지 말고 notes 에 적고 멈춰라」 라 했다. 봉인 전 결정(교차 진단 지적 반영): 「멈춰라」 는 합격선을 이루는 도구 — CI 와 `ci-local.sh` 가 부르는 `check-docs-a11y.js` · `check-docs-links.py` · `visuals.spec.js` — 에 걸린다고 읽는다. 셋 모두 새 링크를 다룬다(DG-04 · AR-10 · DG-05 모의 판 실측). 이 도구는 CI(`.github/workflows/ci.yml`) · `ci-local.sh` 에 없고 부르는 스킬 · 스크립트도 없어(`grep -rn check-api-kit-docs` 가 `.harness/` 옛 계약에서만 나온다) 합격선 밖이다 — 그래서 구현을 멈추지 않고, 「고치지 말고」 를 지켜 `scripts/` 는 건드리지 않으며(AR-07), 변화가 「외부 리소스 참조」 한 가지로만 나는지 잠근 뒤(AR-09) notes 에 적는다(AR-08). 도구 한 줄 고치기를 범위에 넣는 안은 과제의 `scripts/` 범위 밖 지시와 부딪혀 버렸다. 고칠 자리는 `:34` 의 `<link\s` 가 같은 사이트 안 `assets/site.css` 를 빼게 하는 것이다(다음 scripts 묶음 후보) |
| (1) 공통 파일 `docs/assets/site.css` — 움직임 줄이기 · 본문 행간 1.7 만 | 계약에 넣음 | SK-04 · RE-01. 반복 횟수 1 을 더한 까닭은 `## GAP 분석` 의 갈린 곳 표 |
| (2) 177 쪽 `<head>` 안, 자기 `<style>` 앞에 상대 경로 링크 한 줄 | 계약에 넣음 | AR-01 · AR-02 · AR-10 · ER-02. 두 단계 아래 쪽은 `../../assets/site.css` |
| (3) 행간이 1.7 이 아닌 쪽의 body 행간 선언 지우기 | 계약에 넣음 | AR-02 · AR-03. 지울 선언이 있는 쪽은 스물다섯(도우미 `LH_PAGES`). `docs/index.html` 은 선언이 없어 지울 것이 없고 공통 파일로 1.7 을 받는다. `html,body` 를 묶은 여덟 쪽은 html 쪽 행간도 함께 빠지지만 글이 body 안에만 있어 화면에 드러나는 차이는 body 행간뿐이다 |
| (4) 템플릿 · `SKILL.md` · `css-tokens.md` 안내 | 계약에 넣음 | SK-01 ~ SK-03 · AP-03 · AP-04. `SKILL.md:16` 의 「모든 스타일은 `<style>` 내 인라인」 을 바꾸는 것과 템플릿 body 의 행간을 지우는 것은 안내 줄과 어긋나지 않게 하려는 것이다(갈린 곳 표) |
| 배포에서 상대 경로가 풀리는지 | 계약에 넣음 | ER-02 (배포 흉내 · 대소문자 가림) · AR-01 (`css_tracked` · `href_exact`). Pages 원본 설정(가지 · 폴더)은 저장소 밖이라 확인하지 않는다 — `docs/.nojekyll` 이 저장소 안 근거다 |
| 합격선 — 보통 모드 행간 · 움직임 줄이기 · 375 · 1280 · 글자 간격 넘침 · 접근성 · 링크 · visuals · 음성 대조 · 다섯 쪽 픽셀 비교 | 계약에 넣음 | AR-03 · AR-04 · ER-01 · DG-04 · AR-10 · AR-05. 음성 대조(링크를 뺀 사본)는 AR-03 · AR-04 · ER-02 에 있다 |
| 커밋 셋 · 차례 · 범위 | 계약에 넣음 | AR-06 · AR-07 |
| 스크립트가 직접 준 움직임 — `scrollTo`/`scrollIntoView` `smooth` 다섯 쪽(`design-template` · `grid-alignment` · `ratio-proportion` · `visual-hierarchy` · `kaizen-flow`)과 `.animate(` 한 쪽(`flutter-toolkit/animation`) | 넘김 | CSS 로 끌 수 없고 쪽 스크립트는 쪽 본문이라 범위 밖이다. notes 에 적는다(AR-08 `scrollIntoView`) |
| 움직임을 보여 주는 표본 쪽(`design-kit/motion` · `animation` · `microinteraction` · `react-kit/animation` 등) | 계약에 넣음 (그대로 적용) | 움직임 줄이기 설정의 사용자에게는 표본의 CSS 움직임도 꺼진다. 보통 모드 화면은 그대로다(AR-02 가 쪽 글을 잠근다). 사용자 결정 「사이트 전체에 같아야 하는 규칙」 을 따른다 |
| 기존 쪽의 `body{line-height:1.7}` 151 쪽과 쪽 자체 움직임 줄이기 규칙 119 쪽 | 넘김 (그대로 둔다) | 과제 「그 밖에 쪽마다 다른 스타일은 쪽에 그대로 둔다」 · 「그 밖의 선언은 건드리지 않는다」. 새 안내 줄은 새 쪽을 향한다 |
| `SKILL.md:104` · `design-kit/skills/design-audit/references/audit-criteria.md:10` 의 행간 1.2 ~ 1.6 기준 | 넘김 | 기준 문서가 킷 폴더라 범위 밖이다. 사이트 값 1.7 은 사용자 결정이며 시작 판에서도 151 쪽이 1.7 이다. notes 에 적는다(AR-08 `audit-criteria`) |
| `SKILL.md:5` description 의 「standalone」 · `.claude/skills/kaizen-orchestrator/SKILL.md:620` 의 「standalone」 | 넘김 | description 은 스킬을 부르는 낱말이라 이번 규칙 한 줄과 다른 일이고, 오케스트레이터는 범위 밖 폴더다. notes 에 적는다(AR-08 `kaizen-orchestrator`) |
| 320px 넘침 (시작 판 `docs/design-kit/typography-scale.html` 이 320 폭에서 9px 넘침) | 넘김 | 과제 합격선은 375 · 1280 이다. d1 notes 가 이 묶음으로 넘겼지만 과제 항목에 없다. notes 에 적는다(AR-08 `320px`) |
| 핸드오프가 적은 「글자 간격 +0.06em 에서 넘치는 옛 쪽 일곱」 | 할 일 없음 | 시작 판에서 일곱 쪽 모두 375 · 글자 간격 넘침 0 이다(새로 연 창마다 재도 0). 177 쪽 전체가 `ls_ok=177` |
| 쪽 본문 내용 · 쪽마다 다른 디자인 · 킷 폴더 · `scripts/` | 범위 밖 | AR-02 · AR-07 이 막는다 |

AR-05 의 다섯 쪽은 킷이 서로 다르고 높이가 16384px 이하인 쪽에서 골랐다 — 후보였던 `docs/harness/contract-schema.html`(31894px)은 시작 판 대 모의 좋은 판 다섯 번 가운데 두 번 1118 px 가 달랐고(시작 판끼리 세 번은 0), 원인을 확정하지 못해 뺐다. 고른 다섯 쪽은 여섯 번 모두 0 이었다(`## 회귀 게이트` 실측).

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 목록을 한 곳에만 둔 조건:

- 커버리지 해소: AR-02 — 검출기가 산문의 `reflect-kit/design.html` · `docs/index.html` 을 냈다. 앞은 양성 대조의 예이고 뒤는 「나머지 152 쪽」 에 드는 예외 설명이다. 잴 대상은 도우미 `LH_PAGES` 스물다섯 쪽과 시작 판 트리의 177 쪽이며 `m AR-02` 가 그 둘을 센다. 스물다섯 쪽 목록은 도우미 한 곳에만 적는다(목록을 두 번 적지 않는다) — 시작 판 `lhscan` 결과와 같다(`[1.6]=21 [1.65]=4 [1.7]=151 [none]=1`)
- 커버리지 해소: AR-05 — 검출기가 다섯 쪽 경로와 출력 글(`pix_zero=5/5` · `pix_zero=4/5` · `feedback-system.html`)을 냈다. 조건 문장에 「측정」 낱말이 없어 검출기가 산문만 본 것이다. 다섯 쪽은 조건 산문과 도우미 `PIX_PAGES` 에 같은 글자로 있고 `m AR-05` 가 그 목록을 잰다
- 커버리지 해소: AR-06 — 검출기가 `scripts/release.sh` · `.harness/` · `SKILL.md` · `css-tokens.md` 를 냈다. 앞 둘은 양성 대조 설명과 섞임 판정 대상 폴더 이름이고, 뒤 둘은 도우미 `C1SET` 의 네 파일 가운데 둘이다. 177 쪽은 시작 판 트리에서 `find docs -name '*.html'` 로 뽑는다
- 커버리지 해소: AR-08 — 검출기가 `docs/.nojekyll` · notes 경로 · `caching.html` · `index.html` · `.nojekyll` 을 냈다. notes 경로는 도우미 `NOTES` 가 읽고, `caching.html` · `index.html` · `.nojekyll` 은 `m AR-08` 의 열 토큰 목록에 같은 글자로 있다. `docs/.nojekyll` 은 「담을 내용」 설명이다

교차 진단(qa-evaluator) 지적을 반영한 평가 때 주의:

- AR-02 · AR-05 · AR-06 · AR-08 의 대상 목록은 `## 회귀 게이트` 도우미의 `LH_PAGES` · `PIX_PAGES` · `C1SET` · `NOTES` 와 `m AR-08` 열 토큰에 있다. 조건 문장만 보고 「목록이 없다」 로 읽지 말고 도우미 블록을 함께 읽어 전수로 잰다
- AR-08 의 셈은 열 토큰이 든 줄의 한글 글자 수만 본다. 평가자는 셈이 잡은 줄마다 그 줄이 실제로 그 결정이나 넘김을 설명하는지 한 번 눈으로 읽는다 — 토큰을 끼워 넣은 빈말 줄이면 그 열은 0 으로 본다
- AR-05 에서 뺀 `docs/harness/contract-schema.html` 의 흔들림(두 번 1118 px) 원인은 확정하지 못했다. 다른 긴 쪽에서도 나올 수 있어 다음 묶음의 재조사 후보로 notes 에 남긴다
- DG-05 는 가지 밖 도구 파일에 기댄다. 지문이 달라지거나 파일이 없어지면 그 회차는 `[미검증:ENV]` 이고, 그때는 CI 단계를 도구 없이 하나씩 돌린 결과로 대신 보고하지 않는다

계약 파일의 편집기 경고(MD041 첫 줄 제목 1 · MD038 코드 표시 안 공백 5)는 계약 형식에서 나온다 — 허용 헤더 목록에 1 단계 제목이 없고, AP-03 문구는 `project.yaml` 글자 그대로이며, 도우미 출력 `css_files=… ` 은 끝 공백까지 글자 그대로 옮겼다(판정이 그 글자와 대조한다). 계약 · QA 리포트 · 개정 파일은 DG-02 대상에서 뺀다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 그 밖의 입력은 지우지 마라.
브라우저 도구는 작업 폴더 W 의 `node_modules`(추적 안 되는 폴더, `npm ci` 로 설치)를 `NODE_PATH` 로 빌려 쓰고, 푼 트리마다 그 폴더를 가리키는 `node_modules` 연결을 만든다(`npx playwright test` 가 설정 파일 옆에서 찾는다).

준비 단계 실측(봉인 전, 이 기계): `command -v node` → fnm 경로 · 종료 코드 0 (`v24.14.1`), `command -v python3` · `command -v git` · `command -v shasum` 종료 코드 0,
W 의 `node_modules/playwright-core` 판 `1.58.2`, 브라우저 실행 파일은 사용자 폴더 `~/Library/Caches/ms-playwright/chromium_headless_shell-1208` 에서 온다(d1 계약과 같은 판).
그 폴더에 브라우저가 없으면 `pw2.js` 가 `Executable doesn't exist` 로 종료 코드 2 를 낸다. 복구: `cd W && node_modules/.bin/playwright-core install chromium-headless-shell` 뒤 다시 잰다 — 브라우저가 없어 못 잰 조건은 FAIL 이 아니라 환경 실패로 보고한다.
`markdownlint-cli2@0.23.2` 임시 설치 종료 코드 0. `ci-local.sh` 지문 `git hash-object` → `b15dcdf8f6d2bb1b9c5f152c949f8c29f70e61e1`.
Playwright 쓰임(`newContext` 의 `reducedMotion` · `colorScheme`, `emulateMedia({ reducedMotion })`, `context.route` + `route.fulfill({ path })`, `response.frame()` · `page.mainFrame()`, `screenshot({ fullPage, animations: 'disabled' })`, `addStyleTag`)은 Context7 `/microsoft/playwright/v1.58.2` 문서와 맞춰 봤다.
도우미는 zsh 에서 부르지 마라 — zsh 는 따옴표 없는 변수를 낱말로 나누지 않아 쪽 목록이 한 덩어리가 된다(봉인 전에 한 번 그렇게 죽었다).

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/d2-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/d2-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 봉인 커밋이 아직 없을 때: BASE_REF=<커밋> 을 준다. 시작 판을 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>
# === 측정 도우미 시작 (after-0924-docs-common-css) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라(단어 나누기가 달라 쪽 목록이 한 덩어리가 된다).
# 끝점 TIP = 가지 끝. 시작점 BASE = 이 계약을 처음 담은 커밋(봉인 커밋)의 부모 — 해시를 박지 않고 git 기록에서 푼다.
# 봉인 전 실측처럼 봉인 커밋이 아직 없으면 BASE_REF=<커밋> 을 준다. 시작 판 자체를 재려면 E_REF=BASE.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-docs}
BR=${BR:-chore/ak-docs}
SLUG=after-0924-docs-common-css
CF_REL=.harness/sprint-contract-$SLUG.md
NOTES=.harness/.meta/after-kaizen-0926/d2-notes.md
TIP=$(git -C "$W" rev-parse --verify -q "$BR^{commit}") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
if [ -n "${BASE_REF:-}" ]; then
  BASE=$(git -C "$W" rev-parse --verify -q "$BASE_REF^{commit}") || { echo "UNRESOLVED BASE_REF"; return 2 2>/dev/null || exit 2; }
else
  SEAL=$(git -C "$W" log --diff-filter=A --format=%H "$TIP" -- "$CF_REL" | tail -1)
  [ -n "$SEAL" ] || { echo "UNRESOLVED SEAL (봉인 커밋 없음)"; return 2 2>/dev/null || exit 2; }
  BASE=$(git -C "$W" rev-parse --verify -q "$SEAL^") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
fi
T=$(mktemp -d "${TMPDIR:-/tmp}/d2.XXXXXX")
NM=${NM:-$W/node_modules}
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2" && ln -s "$NM" "$2/node_modules"; }
EB=$T/base; snap "$BASE" "$EB"
case "${E_REF:-TIP}" in
  BASE) E=$EB; R=$BASE ;;
  *)    E=$T/tip; snap "$TIP" "$E"; R=$TIP ;;
esac
[ -d "$NM/playwright-core" ] || (cd "$W" && npm ci >/dev/null 2>&1)
[ -d "$NM/playwright-core" ] || { echo "NO_PLAYWRIGHT"; return 2 2>/dev/null || exit 2; }
export NODE_PATH=$NM
CI_LOCAL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
TOOL_BLOB=b15dcdf8f6d2bb1b9c5f152c949f8c29f70e61e1
C1SET='.claude/skills/docs-site/SKILL.md
.claude/skills/docs-site/references/css-tokens.md
.claude/skills/docs-site/references/page-template.html
docs/assets/site.css'
# 본문 행간이 1.7 이 아닌 쪽 가운데 지울 선언이 있는 스물다섯 (1.6 스물하나 · 1.65 넷). docs/index.html 은 선언이 없어 지울 것이 없다
LH_PAGES='docs/backend-kit/caching.html
docs/backend-kit/error-handling.html
docs/design-kit/examples/moodboard-taskflow.html
docs/flutter-toolkit/animation.html
docs/flutter-toolkit/async-patterns.html
docs/flutter-toolkit/flutter-ai-rules.html
docs/flutter-toolkit/hooks.html
docs/flutter-toolkit/performance.html
docs/flutter-toolkit/primitive-substitution-gate.html
docs/flutter-toolkit/responsive.html
docs/flutter-toolkit/state-management.html
docs/flutter-toolkit/testing.html
docs/flutter-toolkit/theming.html
docs/flutter-toolkit/widget-composition.html
docs/react-kit/build-audit.html
docs/react-kit/integration.html
docs/react-kit/performance.html
docs/react-kit/scaffolding.html
docs/react-kit/ui-patterns.html
docs/react-kit/wasm-catalog.html
docs/reflect-kit/codex-kaizen.html
docs/reflect-kit/design.html
docs/reflect-kit/research.html
docs/reflect-kit/schema.html
docs/reflect-kit/tag-canonicalization.html'
# 행간 1.7 이 이미였고 움직임 줄이기도 있던 쪽 가운데 킷이 서로 다른 다섯 — 보통 모드 화면이 그대로여야 한다.
# 높이 16384px 를 넘는 쪽은 뺐다 — contract-schema(31894px)는 같은 판끼리도 네 번에 한 번 1118 px 가 달랐다
PIX_PAGES='docs/api-kit/snapshot-sealing-canonicalization.html
docs/harness/feedback-system.html
docs/infra-kit/deployment-strategies.html
docs/planning-kit/prioritization.html
docs/tone-kit/comment-economy.html'
printf '%s\n' "$LH_PAGES" > "$T/lh.txt"
PAGES=$(cd "$EB" && find docs -name '*.html' | LC_ALL=C sort)

cat > "$T/pg2.py" <<'PY'
import sys, re, os, posixpath, json, subprocess
from html.parser import HTMLParser
rd = lambda p: open(p, encoding='utf-8').read()
CSS = 'docs/assets/site.css'
PHRASE = '공통 파일이 맡는 규칙은 쪽에 다시 적지 않는다'
def pages(tree):
    out = []
    for d, _, fs in os.walk(os.path.join(tree, 'docs')):
        out += [os.path.relpath(os.path.join(d, f), tree) for f in fs if f.endswith('.html')]
    return sorted(out)
def want_href(p): return posixpath.relpath(CSS, posixpath.dirname(p))
class H(HTMLParser):
    def __init__(s, page):
        super().__init__(convert_charrefs=True); s.page = page; s.inhead = False; s.style0 = None; s.links = []
    def handle_starttag(s, t, a):
        a = dict(a); pos = s.getpos()
        if t == 'head': s.inhead = True
        if t == 'style' and s.style0 is None: s.style0 = pos
        if t == 'link' and 'stylesheet' in (a.get('rel') or '').lower().split():
            h = a.get('href') or ''
            tgt = posixpath.normpath(posixpath.join(posixpath.dirname(s.page), h.split('#')[0].split('?')[0]))
            if tgt.lower() == CSS: s.links.append((pos, h, s.inhead, s.style0 is None))
    def handle_endtag(s, t):
        if t == 'head': s.inhead = False
BODY = re.compile(r'(?s)((?:^|(?<=[{};]))\s*)([^{};@]*?)\{([^{}]*)\}')
def body_rules(css):
    for m in BODY.finditer(css):
        if 'body' in [x.strip() for x in m.group(2).split(',')]: yield m
def strip_body_lh(h):
    def fix_style(sm):
        css = sm.group(2); out = []; last = 0
        for m in body_rules(css):
            out += [css[last:m.start()], m.group(1) + m.group(2) + '{' + re.sub(r'line-height\s*:\s*[^;}]+;?', '', m.group(3)) + '}']; last = m.end()
        return sm.group(1) + ''.join(out + [css[last:]]) + sm.group(3)
    return re.sub(r'(?is)(<style[^>]*>)(.*?)(</style>)', fix_style, h, count=1)
def norm(h):
    h = re.sub(r'\s+', '', h); h = re.sub(r';+', ';', h); return h.replace('{;', '{').replace(';}', '}')
def body_lh(h):
    css = '\n'.join(re.findall(r'(?is)<style[^>]*>(.*?)</style>', h)); vals = []
    for m in body_rules(css): vals += [v.strip() for v in re.findall(r'line-height\s*:\s*([^;}]+)', m.group(3))]
    return ','.join(vals) or 'none'
def drop_line(h, w):
    L = h.splitlines(True); idx = [i for i, l in enumerate(L) if l.strip() == w]
    if len(idx) == 1: del L[idx[0]]
    return ''.join(L), len(idx)
cmd = sys.argv[1]
if cmd == 'links':   # links <트리> — 쪽마다 공통 파일 링크 수 · 자리 · href 글자 · 줄 모양
    tree = sys.argv[2]; P = pages(tree); c = dict(one=0, before=0, href=0, line=0); bad = []
    for p in P:
        h = rd(os.path.join(tree, p)); x = H(p); x.feed(h); L = x.links; w = want_href(p)
        ok1 = len(L) == 1; ok2 = ok1 and L[0][2] and L[0][3]; ok3 = ok1 and L[0][1] == w
        ok4 = ok1 and h.splitlines()[L[0][0][0] - 1].strip() == f'<link rel="stylesheet" href="{w}">'
        for k, v in zip(('one', 'before', 'href', 'line'), (ok1, ok2, ok3, ok4)): c[k] += v
        if not (ok1 and ok2 and ok3 and ok4): bad.append(f'{p}:n={len(L)}')
    print(f"pages={len(P)} one={c['one']} before_style={c['before']} href_exact={c['href']} line_exact={c['line']} bad={bad[:5]}")
elif cmd == 'lhscan':  # lhscan <트리> — body 규칙의 행간 선언 값별 쪽 수
    from collections import Counter; C = Counter(); tree = sys.argv[2]; L = []
    for p in pages(tree):
        v = body_lh(rd(os.path.join(tree, p))); C[v] += 1
        if v != '1.7': L.append(f'{p}={v}')
    print(' '.join(f'[{k}]={v}' for k, v in sorted(C.items()))); [print(l) for l in L]
elif cmd == 'shape':  # shape <옛 트리> <새 트리> <행간 목록> — 링크 한 줄 · 행간 선언 말고 바뀐 게 없는지
    b, t, lf = sys.argv[2:5]; LH = set(open(lf).read().split()); same = lhdone = 0; bad = []; P = pages(b)
    for p in P:
        tp = os.path.join(t, p)
        if not os.path.exists(tp): bad.append(p + ':gone'); continue
        th = rd(tp); th2, _ = drop_line(th, f'<link rel="stylesheet" href="{want_href(p)}">'); bh = rd(os.path.join(b, p))
        if p in LH:
            ok = norm(th2) == norm(strip_body_lh(bh)) and body_lh(th) == 'none'; lhdone += ok
        else:
            ok = th2 == bh
        same += ok
        if not ok: bad.append(p)
    print(f'pages={len(P)} same={same} lh_removed={lhdone}/{len(LH)} bad={bad[:5]}')
elif cmd == 'tpl':  # tpl <옛 트리> <새 트리> — 템플릿의 링크 한 줄 · body 행간 삭제 말고 바뀐 게 없는지
    f = '.claude/skills/docs-site/references/page-template.html'; w = '<link rel="stylesheet" href="../assets/site.css">'
    ph = lambda x: re.sub(r'\{\{(\w+)\}\}', r'__\1__', x)  # 템플릿 자리표시자 {{X}} 가 CSS 중괄호로 읽히지 않게
    bh, th = ph(rd(os.path.join(sys.argv[2], f))), ph(rd(os.path.join(sys.argv[3], f))); L = th.splitlines()
    n = sum(1 for l in L if l.strip() == w)
    li = next((i for i, l in enumerate(L) if l.strip() == w), -1); si = next((i for i, l in enumerate(L) if '<style' in l), -1)
    hi = next((i for i, l in enumerate(L) if '<head' in l), -1)
    th2, _ = drop_line(th, w)
    print(f'tpl_link={n} tpl_before_style={int(hi < li < si)} tpl_body_lh={body_lh(th)} tpl_shape={int(norm(th2) == norm(strip_body_lh(bh)))}')
elif cmd == 'skill':  # skill <옛 트리> <새 트리> — docs-site SKILL.md · css-tokens.md 안내 줄
    b, t = sys.argv[2:4]; s = '.claude/skills/docs-site/SKILL.md'; k = '.claude/skills/docs-site/references/css-tokens.md'
    fm = lambda x: x.split('\n---', 1)[0]
    bs, ts, tk = rd(os.path.join(b, s)), rd(os.path.join(t, s)), rd(os.path.join(t, k))
    both = lambda x: sum(1 for l in x.splitlines() if PHRASE in l and 'assets/site.css' in l)
    print(f"skill_fm_same={int(fm(bs) == fm(ts))} skill_cdn={ts.count('외부 CSS/JS/font CDN 링크를 절대 추가하지 마라')} "
          f"skill_old_inline={ts.count('모든 스타일은 `<style>` 내 인라인')} skill_phrase={ts.count(PHRASE)} skill_phrase_line={both(ts)} "
          f"tokens_phrase={tk.count(PHRASE)} tokens_phrase_line={both(tk)}")
elif cmd == 'apikit':  # apikit <옛 json> <새 json> — FAIL 사유가 「외부 리소스 참조」 말고 바뀌었는지
    ld = lambda f: {r['html']: set(r['fail']) for r in json.JSONDecoder().raw_decode(open(f).read())[0]}  # 끝의 「N/M PASS」 줄은 버린다
    B, T = ld(sys.argv[2]), ld(sys.argv[3])
    ext = sum(1 for k in T if (T[k] - B.get(k, set())) == {'외부 리소스 참조'})
    other = sum(1 for k in T if ((T[k] - B.get(k, set())) - {'외부 리소스 참조'}) or (B.get(k, set()) - T[k]))
    print(f'pages={len(T)} base_fail={sum(1 for k in B if B[k])} ext_only_new={ext} other_change={other}')
elif cmd == 'commits':  # commits <W> <BASE> <TIP> <C1 목록> <행간 목록> <쪽 목록> — 구현 커밋 셋의 파일 집합 · 순서
    w, base, tip = sys.argv[2:5]; C1 = set(open(sys.argv[5]).read().split()); LH = set(open(sys.argv[6]).read().split()); PG = set(open(sys.argv[7]).read().split())
    g = lambda *a: subprocess.run(['git', '-C', w, *a], capture_output=True, text=True).stdout
    impl = []; mixed = 0
    for c in g('rev-list', '--reverse', '--no-merges', f'{base}..{tip}').split():
        ns = [l.split('\t') for l in g('show', '--numstat', '--format=', c).splitlines() if l.strip()]
        fs = {x[2] for x in ns}; h = {f for f in fs if f.startswith('.harness/')}
        if h and fs - h: mixed += 1
        if fs - h: impl.append((c, fs, {x[2]: (x[0], x[1]) for x in ns}))
    want = [C1, PG, LH]
    eq = [int(i < len(impl) and impl[i][1] == want[i]) for i in range(3)]
    plus1 = sum(1 for f, v in impl[1][2].items() if v == ('1', '0')) if len(impl) > 1 else 0
    print(f'impl={len(impl)} c1={eq[0]} c2={eq[1]} c3={eq[2]} c2_plus1={plus1}/{len(PG)} mixed={mixed}')
elif cmd == 'html':  # html <파일> — 짝 안 맞는 태그 수 (편집기 진단 대용)
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr','path','circle','rect','line','polyline','polygon','ellipse','stop','use'}
    class P(HTMLParser):
        def __init__(s): super().__init__(); s.st = []; s.bad = 0
        def handle_starttag(s, tag, a):
            if tag not in VOID: s.st.append(tag)
        def handle_startendtag(s, tag, a): pass
        def handle_endtag(s, tag):
            if tag in VOID: return
            if tag in s.st:
                while s.st and s.st[-1] != tag: s.st.pop(); s.bad += 1
                s.st.pop()
            else: s.bad += 1
    x = P(); x.feed(rd(sys.argv[2])); x.close(); print(x.bad + len(x.st))
PY

cat > "$T/pw2.js" <<'JS'
// render <트리> <쪽>... — 배포 흉내(http 하위 경로)로 열어 행간 · 공통 파일 응답 · 움직임 줄이기 · 넘침을 잰다
// pix <옛 트리> <새 트리> <쪽>... — 1280 폭 전체 화면 캡처를 픽셀로 비교한다
// cssom <트리> — 공통 파일의 규칙을 브라우저가 읽은 그대로 찍는다
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright-core');
const ORIGIN = 'http://pages.test/claude-plugins/';
const EPS = 1e-5 + 1e-9;
async function serve(ctx, tree) {
  await ctx.route(ORIGIN + '**', async r => {
    const rel = decodeURIComponent(new URL(r.request().url()).pathname.replace('/claude-plugins/', ''));
    const f = path.join(tree, 'docs', rel);
    // 배포 서버는 대소문자를 가린다 — 맥 파일 시스템이 대소문자를 무시해도 경로 조각마다 글자 그대로 있어야 내준다
    let d = path.join(tree, 'docs'), exact = true;
    for (const part of rel.split('/').filter(Boolean)) { if (!fs.existsSync(d) || !fs.readdirSync(d).includes(part)) { exact = false; break; } d = path.join(d, part); }
    if (exact && fs.statSync(f).isFile()) await r.fulfill({ path: f });
    else await r.fulfill({ status: 404, body: 'not found' });
  });
}
const OVER = () => document.documentElement.scrollWidth - document.documentElement.clientWidth;
const LH = () => { const s = getComputedStyle(document.body); const lh = parseFloat(s.lineHeight), fz = parseFloat(s.fontSize);
  return isNaN(lh) ? s.lineHeight : (lh / fz).toFixed(2); };
const MOTION = () => {
  const sec = v => v.split(',').map(x => x.trim()).map(x => x.endsWith('ms') ? parseFloat(x) / 1000 : parseFloat(x));
  let a = 0, t = 0, iter = 0, smooth = 0;
  for (const el of document.querySelectorAll('*')) for (const ps of [null, '::before', '::after']) {
    const s = getComputedStyle(el, ps);
    a = Math.max(a, ...sec(s.animationDuration)); t = Math.max(t, ...sec(s.transitionDuration));
    if (s.animationName.split(',').some(x => x.trim() !== 'none') && s.animationIterationCount.split(',').some(x => x.trim() !== '1')) iter++;
    if (ps === null && s.scrollBehavior === 'smooth') smooth++;
  }
  return { a, t, iter, smooth };
};
(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const b = await chromium.launch();
  if (mode === 'render') {
    const tree = path.resolve(args[0]); const P = args.slice(1); const sum = { lh: 0, lhf: 0, css: 0, rm: 0, of: 0, ls: 0, err: 0 };
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark', reducedMotion: 'no-preference' });
    await serve(ctx, tree);
    const fctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark' });
    for (const rel of P) {
      const p = await ctx.newPage(); let errs = 0, css = 'none';
      p.on('console', m => m.type() === 'error' && errs++); p.on('pageerror', () => errs++);
      // 첫 화면(index.html)은 iframe 에 다른 쪽을 띄운다 — 그 쪽의 요청을 이 쪽 것으로 세지 않게 주 프레임 응답만 본다
      p.on('response', r => { try { if (r.frame() === p.mainFrame() && r.url().toLowerCase().endsWith('/assets/site.css')) css = r.status(); } catch {} });
      await p.goto(ORIGIN + rel.replace(/^docs\//, ''), { waitUntil: 'load' });
      const rules = await p.evaluate(() => { const ss = [...document.styleSheets].find(s => (s.href || '').toLowerCase().endsWith('/assets/site.css'));
        try { return ss ? ss.cssRules.length : 0; } catch { return -1; } });
      if (css === 200 && rules < 1) css = 'empty';
      const lh = await p.evaluate(LH); const w1280 = await p.evaluate(OVER);
      await p.setViewportSize({ width: 375, height: 900 }); const w375 = await p.evaluate(OVER);
      await p.emulateMedia({ reducedMotion: 'reduce' }); const m = await p.evaluate(MOTION);
      await p.emulateMedia({ reducedMotion: 'no-preference' });
      await p.addStyleTag({ content: '*{letter-spacing:0.06em !important}' }); await p.waitForTimeout(100);
      const ls375 = await p.evaluate(OVER); await p.close();
      const fp = await fctx.newPage(); await fp.goto('file://' + path.join(tree, rel)); const lhf = await fp.evaluate(LH); await fp.close();
      const ok = { lh: lh === '1.70', lhf: lhf === '1.70', css: css === 200, rm: m.a <= EPS && m.t <= EPS && m.iter === 0 && m.smooth === 0,
                   of: w375 <= 2 && w1280 <= 2, ls: ls375 <= 2, err: errs === 0 };
      for (const k in ok) sum[k] += ok[k];
      console.log(`${Object.values(ok).every(Boolean) ? 'OK ' : 'BAD'} ${rel} lh=${lh} lhf=${lhf} css=${css} anim=${m.a} trans=${m.t} iter=${m.iter} smooth=${m.smooth} w375=${w375} w1280=${w1280} ls375=${ls375} err=${errs}`);
    }
    console.log(`pages=${P.length} lh_ok=${sum.lh} lhf_ok=${sum.lhf} css_ok=${sum.css} rm_ok=${sum.rm} of_ok=${sum.of} ls_ok=${sum.ls} err_ok=${sum.err}`);
  } else if (mode === 'pix') {
    const [A, B] = [path.resolve(args[0]), path.resolve(args[1])]; const P = args.slice(2); let zero = 0;
    const shot = async (tree, rel) => {
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark', reducedMotion: 'no-preference' });
      await serve(ctx, tree); const p = await ctx.newPage();
      await p.goto(ORIGIN + rel.replace(/^docs\//, ''), { waitUntil: 'load' }); await p.waitForTimeout(300);
      const buf = await p.screenshot({ fullPage: true, animations: 'disabled' }); await ctx.close(); return buf;
    };
    const cmp = await (await b.newContext()).newPage();
    for (const rel of P) {
      const x = await shot(A, rel), y = await shot(B, rel);
      const r = await cmp.evaluate(async ([u, v]) => {
        const load = s => new Promise(res => { const i = new Image(); i.onload = () => res(i); i.src = s; });
        const [i, j] = [await load(u), await load(v)];
        if (i.width !== j.width || i.height !== j.height) return { size: `${i.width}x${i.height}/${j.width}x${j.height}`, diff: -1 };
        const px = im => { const c = document.createElement('canvas'); c.width = im.width; c.height = im.height;
          const g = c.getContext('2d'); g.drawImage(im, 0, 0); return g.getImageData(0, 0, im.width, im.height).data; };
        const [d, e] = [px(i), px(j)]; let n = 0;
        for (let k = 0; k < d.length; k += 4) if (d[k] !== e[k] || d[k + 1] !== e[k + 1] || d[k + 2] !== e[k + 2] || d[k + 3] !== e[k + 3]) n++;
        return { size: `${i.width}x${i.height}`, diff: n };
      }, ['data:image/png;base64,' + x.toString('base64'), 'data:image/png;base64,' + y.toString('base64')]);
      if (r.diff === 0) zero++;
      console.log(`${rel} size=${r.size} diff_px=${r.diff}`);
    }
    console.log(`pix_zero=${zero}/${P.length}`);
  } else if (mode === 'cssom') {
    const ctx = await b.newContext(); await serve(ctx, path.resolve(args[0])); const p = await ctx.newPage();
    await p.goto(ORIGIN + 'index.html', { waitUntil: 'load' });
    console.log(await p.evaluate(() => {
      const ss = [...document.styleSheets].find(s => (s.href || '').endsWith('/assets/site.css'));
      if (!ss) return 'sheet=absent';
      const decl = st => [...st].map(k => `${k}:${st.getPropertyValue(k)}${st.getPropertyPriority(k) ? '!' + st.getPropertyPriority(k) : ''}`).sort().join(';');
      return [...ss.cssRules].map(r => r.type === 1 ? `rule[${r.selectorText}]{${decl(r.style)}}`
        : r.type === 4 ? `media[${r.media.mediaText}]{${[...r.cssRules].map(q => q.type === 1 ? `rule[${q.selectorText}]{${decl(q.style)}}` : `other${q.type}`).join(' ')}}`
        : `other${r.type}`).join(' | ');
    }));
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(2); });
JS

# 봉인 검사 함수 — harness/references/contract-schema.md §계약 봉인 · §값 따옴표 규약 과 같은 정의
fm_get() { awk -v k="$2" -v q="\"'" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit }
  fm && index($0, k ":") == 1 { v = substr($0, length(k) + 2); sub(/^[[:space:]]+/, "", v); sub(/[[:space:]]+$/, "", v)
  c = substr(v, 1, 1); if (length(v) > 1 && index(q, c) > 0 && substr(v, length(v), 1) == c) v = substr(v, 2, length(v) - 2); print v; exit }' "$1"; }
sha256_16() {
  if   command -v sha256sum >/dev/null 2>&1; then sha256sum
  elif command -v shasum    >/dev/null 2>&1; then shasum -a 256
  elif command -v python3   >/dev/null 2>&1; then python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'
  else openssl dgst -sha256 | sed 's/.*= //'
  fi | cut -c1-16
}
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}
  if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); [ "$rec" = "$act" ] && echo "SEAL_OK $1" || echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; }

# 언어 없는 여는 코드 울타리 수 — validate-plugin V6 과 같은 셈(줄 앞 공백을 벗기고 백틱 셋으로 시작하면 열고 닫기를 번갈아 센다)
bare() { [ -f "$1" ] || { echo absent; return; }; awk '{s=$0; sub(/^[ \t]+/,"",s)} s ~ /^```/ { if (!inb) { h=substr(s,4); gsub(/[ \t]/,"",h); if (h=="") n++; inb=1 } else inb=0 } END{print n+0}' "$1"; }
render() { [ -s "$T/render.txt" ] || (cd "$E" && node "$T/pw2.js" render "$E" $PAGES > "$T/render.txt" 2>&1); tail -1 "$T/render.txt"; }
m() {
  case "$1" in
  SK-01) python3 "$T/pg2.py" tpl "$EB" "$E" ;;
  SK-02|SK-03) python3 "$T/pg2.py" skill "$EB" "$E"
    for f in .claude/skills/docs-site/SKILL.md .claude/skills/docs-site/references/css-tokens.md; do
      echo "numstat $(basename "$f")=$(git -C "$W" diff --numstat "$BASE" "$R" -- "$f" | awk '{print $1"/"$2}')"; done ;;
  SK-04) node "$T/pw2.js" cssom "$E"
    echo "css_files=$(cd "$E" && find docs -name '*.css' | LC_ALL=C sort | tr '\n' ' ')" ;;
  AR-01) python3 "$T/pg2.py" links "$E"; echo "css_tracked=$(git -C "$W" ls-tree -r --name-only "$R" -- docs/assets/site.css | grep -cx 'docs/assets/site.css')" ;;
  AR-02) python3 "$T/pg2.py" shape "$EB" "$E" "$T/lh.txt" ;;
  AR-03|AR-04|ER-01|ER-02) render ;;
  AR-05) (cd "$E" && node "$T/pw2.js" pix "$EB" "$E" $PIX_PAGES) ;;
  AR-06) printf '%s\n' "$C1SET" > "$T/c1.txt"; printf '%s\n' "$PAGES" > "$T/pages.txt"
    python3 "$T/pg2.py" commits "$W" "$BASE" "$R" "$T/c1.txt" "$T/lh.txt" "$T/pages.txt" ;;
  AR-07) git -C "$W" diff --name-only "$BASE" "$R" -- . ':(exclude).harness' | LC_ALL=C sort > "$T/changed.txt"
    printf '%s\n%s\n' "$PAGES" "$C1SET" | LC_ALL=C sort > "$T/allowed.txt"
    echo "changed=$(grep -c . "$T/changed.txt") extra=$(comm -23 "$T/changed.txt" "$T/allowed.txt" | grep -c .) missing=$(comm -13 "$T/changed.txt" "$T/allowed.txt" | grep -c .)"
    comm -23 "$T/changed.txt" "$T/allowed.txt" | head -3
    echo "seal_broken=$(cd "$E" && find .harness -type f -name 'sprint-contract*.md' | while read -r f; do verify_seal "$f"; done | grep -c '^SEAL_BROKEN')" ;;
  AR-08) b=$(git -C "$W" show "$R:$NOTES" 2>/dev/null); out="committed=$([ -n "$b" ] && echo 1 || echo 0)"
    for k in check-api-kit-docs moodboard-taskflow index.html caching.html audit-criteria kaizen-orchestrator scrollIntoView .nojekyll 320px tone-guide; do
      out="$out $k=$(printf '%s\n' "$b" | python3 -c 'import sys, re; k = sys.argv[1]; print(sum(1 for l in sys.stdin if k in l and len(re.findall(r"[가-힣]", l)) >= 15))' "$k")"; done; echo "$out" ;;
  AR-09) (cd "$EB" && python3 scripts/check-api-kit-docs.py --json > "$T/ak-base.json" 2>/dev/null); (cd "$E" && python3 scripts/check-api-kit-docs.py --json > "$T/ak-tip.json" 2>/dev/null)
    python3 "$T/pg2.py" apikit "$T/ak-base.json" "$T/ak-tip.json" ;;
  AR-10) for x in "$EB" "$E"; do (cd "$x" && python3 scripts/check-docs-links.py > "$T/links.txt" 2>&1; echo "rc=$? $(grep -oE '내부 상대링크 [0-9]+ 개' "$T/links.txt") broken0=$(grep -c '깨진 링크 없음' "$T/links.txt") $(grep -oE '페이지 [0-9]+ · 등록 [0-9]+' "$T/links.txt")"); done ;;
  RE-01) echo "css_files=$(cd "$E" && find docs -name '*.css' | grep -c .) link_pages=$(python3 "$T/pg2.py" links "$E" | sed -E 's/.* one=([0-9]+).*/\1/')" ;;
  RE-02) a=$(git -C "$W" diff "$BASE" "$R" -- $PAGES | grep '^+' | grep -v '^+++')
    echo "added_rm=$(printf '%s\n' "$a" | grep -c 'prefers-reduced-motion') added_lh=$(printf '%s\n' "$a" | grep -c 'line-height')" ;;
  AP-03) out="bare:"; for f in "$NOTES" .claude/skills/docs-site/SKILL.md .claude/skills/docs-site/references/css-tokens.md; do
      out="$out $(basename "$f")=$(bare "$EB/$f")->$(bare "$E/$f")"; done; echo "$out" ;;
  AP-04) echo "fm_name=$(fm_get "$E/.claude/skills/docs-site/SKILL.md" name)" ;;
  SC-00) echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$R" | grep -cE '^(scripts/|\.claude-plugin/)|/\.claude-plugin/')" ;;
  DG-01|DG-03) echo "release_sh=$(git -C "$W" diff --name-only "$BASE" "$R" | grep -cx 'scripts/release.sh')" ;;
  DG-02) tb=0; for pg in $PAGES; do a=$(python3 "$T/pg2.py" html "$EB/$pg"); b2=$(python3 "$T/pg2.py" html "$E/$pg"); [ "$b2" -gt "$a" ] && tb=$((tb+1)); done
    css=$(cat "$E/docs/assets/site.css" 2>/dev/null); cb=$([ -n "$css" ] && [ "$(printf '%s' "$css" | tr -cd '{' | wc -c)" = "$(printf '%s' "$css" | tr -cd '}' | wc -c)" ] && echo 0 || echo 1)
    MDL=${MDL:-$T/mdl}
    [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
    printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
    ml() { [ -f "$1" ] || { echo absent; return; }; (cd "$(dirname "$1")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$(basename "$1")" 2>&1) | grep -cE '^[^ ]+:[0-9]+'; }
    if [ ! -x "$MDL/node_modules/.bin/markdownlint-cli2" ]; then echo "tag_worse=$tb css_bad=$cb md=ENV_FAIL"
    else echo "tag_worse=$tb css_bad=$cb md_notes=$(ml "$E/$NOTES") md_skill=$(ml "$EB/.claude/skills/docs-site/SKILL.md")->$(ml "$E/.claude/skills/docs-site/SKILL.md") md_tokens=$(ml "$EB/.claude/skills/docs-site/references/css-tokens.md")->$(ml "$E/.claude/skills/docs-site/references/css-tokens.md")"; fi ;;
  DG-04) (cd "$E" && node scripts/check-docs-a11y.js > "$T/a11y.txt" 2>&1; echo "a11y_rc=$? $(tail -1 "$T/a11y.txt")")
    (cd "$E" && npx playwright test design-kit/evals/visuals.spec.js --reporter=line --output="$T/pw-out" > "$T/vis.txt" 2>&1; echo "visuals_rc=$? $(grep -oE '[0-9]+ passed' "$T/vis.txt" | tail -1) $(grep -oE '[0-9]+ failed' "$T/vis.txt" | tail -1)") ;;
  DG-05) [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] && [ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "W_NOT_TIP"; return 2; }
    ts=$([ "$(git hash-object "$CI_LOCAL" 2>/dev/null)" = "$TOOL_BLOB" ] && echo 1 || echo 0)
    mkdir -p "$T/ci"; TMPDIR=$T/ci bash "$CI_LOCAL" "$W" > "$T/ci/run.log" 2>&1
    [ -f "$T/ci/ci-local/summary.txt" ] || { echo "tool_same=$ts ci_summary=absent"; return 2; }
    kz=$(cd "$W" && python3 scripts/run-kaizen-assertions.py 2>&1 | grep -oE 'Total: [0-9]+ passed, [0-9]+ failed' | tail -1)
    echo "tool_same=$ts rc0=$(grep -c 'rc=0' "$T/ci/ci-local/summary.txt") other=[$(grep -v 'rc=0' "$T/ci/ci-local/summary.txt" | tr '\n' ';')] kaizen=[$kz]" ;;
  *) echo "unknown $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측 — 시작 판(`BASE_REF=4d1de5f E_REF=BASE`, 구현 전)에서 도우미로 잰 값과 대조 결과. 모의 판은 세션 임시 폴더에서 W 를 `git clone --no-hardlinks` 해 만들었다.

- 시작 판: 각 조건의 괄호 안 값 그대로. `lhscan` → `[1.6]=21 [1.65]=4 [1.7]=151 [none]=1`, 스물다섯 쪽 목록이 도우미 `LH_PAGES` 와 같다
- 모의 좋은 판(시작 판 위에 봉인 커밋 대역 → 공통 파일 · 템플릿 · `SKILL.md` · `css-tokens.md` 한 커밋 → 177 쪽 링크 한 커밋 → 스물다섯 쪽 행간 선언 지우기 한 커밋 → notes 한 커밋): SK-01 `tpl_link=1 tpl_before_style=1 tpl_body_lh=none tpl_shape=1`, SK-02 · SK-03 `skill_fm_same=1 skill_cdn=1 skill_old_inline=0 skill_phrase=1 skill_phrase_line=1 tokens_phrase=1 tokens_phrase_line=1` · `numstat SKILL.md=1/1` · `numstat css-tokens.md=1/0`, SK-04 조건의 글과 같은 줄 · `css_files=docs/assets/site.css `, ER · AR-03 · AR-04 `pages=177 lh_ok=177 lhf_ok=177 css_ok=177 rm_ok=177 of_ok=177 ls_ok=177 err_ok=177`, AR-01 `one=177 before_style=177 href_exact=177 line_exact=177` · `css_tracked=1`, AR-02 `same=177 lh_removed=25/25`, AR-05 `pix_zero=5/5`, AR-06 `impl=3 c1=1 c2=1 c3=1 c2_plus1=177/177 mixed=0`, AR-07 `changed=181 extra=0 missing=0` · `seal_broken=0`, AR-08 `committed=1` 과 1 열, AR-09 `pages=12 base_fail=0 ext_only_new=12 other_change=0`, AR-10 `rc=0 내부 상대링크 684 개 broken0=1 페이지 176 · 등록 176`, RE-01 `css_files=1 link_pages=177`, RE-02 `added_rm=0 added_lh=0`, AP-03 `absent->0 0->0 0->0`, AP-04 `fm_name=docs-site`, DG-02 `tag_worse=0 css_bad=0 md_notes=0 md_skill=9->9 md_tokens=0->0`, DG-04 `a11y_rc=0 177/177 PASS` · `visuals_rc=0 143 passed`, DG-05 `tool_same=1 rc0=22 other=[feedback-agg-test SKIP (yq 없음);] kaizen=[Total: 14 passed, 0 failed]` — 모든 기대값이 도달 가능하다
- 음성 대조 판(모의 좋은 판에서 `docs/index.html` · `docs/reflect-kit/design.html` 의 링크 한 줄만 뺌): 끝줄 `lh_ok=175 lhf_ok=175 css_ok=175 rm_ok=176`, `index.html` 은 `lh=normal css=none trans=0.25`, `reflect-kit/design.html` 은 `lh=normal css=none trans=0.00001`(쪽 자체 규칙이 전환을 이미 끈다)
- 나쁜 판(모의 좋은 판 위 한 커밋 — 한 쪽 링크 두 번 · 한 쪽 링크를 `<style>` 뒤로 · 한 쪽 `../Assets/` · 행간 쪽의 색 선언 · 다섯 쪽 밖 한 쪽의 행간 · 한 쪽에 움직임 줄이기 규칙 · api-kit 한 쪽의 `prefers-reduced-motion` 글 지움 · 깨진 링크 · 공통 파일에 `color:red` · 템플릿 행간 되살림 · `scripts/release.sh` · 새 `docs/assets/extra.css` · 언어 없는 코드 울타리와 토큰을 한 줄에 늘어놓은 notes, `.harness/` 와 섞어서): AR-01 `one=176 before_style=175 href_exact=175 line_exact=175`, AR-02 `same=170 lh_removed=24/25`, ER-02 끝줄 `css_ok=176 … err_ok=176`(`api-design.html` 이 `css=404 err=1` — `file://` 로는 `lhf=1.70` 이라 맥에서만 재면 못 잡는다), SK-01 `tpl_body_lh=1.7 tpl_shape=0`, SK-04 첫 줄 `rule[body]{color:red;line-height:1.7} | …` · `css_files=docs/assets/extra.css docs/assets/site.css `, AR-06 `impl=4 c1=1 c2=1 c3=1 c2_plus1=177/177 mixed=1`, AR-07 `changed=183 extra=2` 와 두 경로, AR-08 `committed=1` 과 0 열, AR-09 `ext_only_new=11 other_change=1`, AR-10 끝점 줄 `rc=1 내부 상대링크 686 개 broken0=0`, RE-01 `css_files=2 link_pages=176`, RE-02 `added_rm=1 added_lh=1`, AP-03 `d2-notes.md=absent->1`, SC-00 `release_paths=1`, DG-01 `release_sh=1`, DG-02 `md_notes=1`
- 나쁜 판 2(모의 좋은 판 위에 `SKILL.md` 머리 설정의 `name` 줄을 지우고 description 글을 바꾸고, `css-tokens.md` 에 언어 없는 코드 울타리 세 줄): SK-02 `skill_fm_same=0` · `numstat SKILL.md=2/3`, SK-03 `numstat css-tokens.md=5/0`, AP-03 `css-tokens.md=0->1`, AP-04 `fm_name=` 빈 값
- 나쁜 판 3(모의 좋은 판 위에 앞 계약 `sprint-contract-after-0924-docs-regen.md` 의 SK-01 조건 줄 한 글자를 바꿈): AR-07 `seal_broken=1`
- 나쁜 판 4(모의 좋은 판 위에 `docs/harness/feedback-system.html` 의 body 행간을 1.6 으로): AR-05 `feedback-system.html size=1280x7075/1280x7019 diff_px=-1` · `pix_zero=4/5`
- 임시 쪽: 900px 폭 요소와 오류를 던지는 스크립트 → `pw2.js render` `BAD … w375=525 w1280=0 ls375=525 err=1`, `check-docs-a11y.js` `0/1 PASS` 종료 코드 1. 고정폭 글자 36 개 한 줄 → `w375=0 w1280=0 ls375=5` 로 `BAD`. 닫히지 않은 `div` → 도우미 태그 셈 1
- 알려진 답(새로 짠 셈 `links`): 나쁜 판의 링크 결함 셋을 손으로 세면 — 두 번 건 쪽은 넷 모두 실패, `<style>` 뒤로 옮긴 쪽은 자리만 실패, `../Assets/` 쪽은 글자 둘(href · 줄)만 실패 — `one=176 before_style=175 href_exact=175 line_exact=175` 이고 도우미 값과 같다
- 픽셀 비교의 흔들림: 시작 판끼리 세 번, 시작 판 대 모의 좋은 판 세 번을 다섯 쪽을 포함한 여덟 쪽에 돌려 다섯 쪽은 여섯 번 모두 `diff_px=0` 이었다. 뺀 `docs/harness/contract-schema.html`(31894px)은 시작 판 대 모의 좋은 판 다섯 번 가운데 두 번 `diff_px=1118` 이었고 시작 판끼리는 세 번 모두 0 이었다 — 원인은 확정하지 못했고 흔들린 쪽을 빼는 쪽으로 정했다(16384px 를 넘는 다른 두 쪽 `agent-design-guide` · `plugin-validation` 은 흔들리지 않았다)
- 시작 판 DG-05: `tool_same=1 rc0=22 other=[feedback-agg-test SKIP (yq 없음);] kaizen=[Total: 14 passed, 0 failed]` (`ci-local.sh` 종료 코드 0, W 가 `4d1de5f` 이고 추적 파일 변경 0)
- 계약에서 뗀 도우미가 작성 원본과 바이트까지 같다(`cmp` 종료 코드 0). 뗀 도우미로 시작 판 · 모의 좋은 판 · 나쁜 판의 브라우저 없는 조건을 다시 재어 위 값과 같았다

## 리서치 소스

- 저장소 안: 핸드오프 `.harness/handoff/2026-09-26-0110.md` §C4 5 번 · §운영 요령(본 체크아웃, 읽기만), 이 가지의 `.harness/.meta/after-kaizen-0926/d1-notes.md` 「넘긴 것과 사유」 · 「다음 사이클 메모」 R3(로컬 CI 도구 밖 단계), `.harness/.meta/after-kaizen-0926/c3b-notes.md:77-85` · `:140`, `.harness/sprint-contract-after-0924-docs-regen.md`(같은 꼴의 측정 도우미), `.claude/skills/docs-site/SKILL.md` · `references/page-template.html` · `references/css-tokens.md`, `harness/references/contract-schema.md` §계약 봉인 · §`.harness/` 범위 조건 · §커밋 구간 상한 · §여러 주체가 한 가지에 커밋할 때
- `.harness/.meta/kaizen-0924/` 의 `final-notes.md` · `f1-harness-followups-notes.md` · `f1-kit-followups-notes.md` · `f2-review-fixes-notes.md` — 움직임 줄이기 · 행간 · 공통 틀을 다룬 줄 0 건(`grep -n 'reduced-motion\|행간\|line-height\|공통 틀'`). 이 묶음의 근거는 위 핸드오프 §C4 와 d1 · c3b notes 다
- 측정 도구 원본: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` (DG-05). `coverage.py` · `fence2.py` 는 쪽 본문을 다시 만드는 묶음용이라 쓰지 않았다 — 이 묶음은 쪽 본문을 바꾸지 않고 AR-02 가 링크 줄 · 행간 선언 말고는 바이트까지 같음을 잰다
- 라이브러리 문서: Context7 `/microsoft/playwright/v1.58.2` (`emulateMedia` · `reducedMotion` · `route.fulfill({ path })` · `response.frame()` · `page.mainFrame()` · `screenshot({ fullPage, animations })`)
- 메모리: 「CI 리눅스는 내 맥보다 화면을 더 나쁘게 그린다」 · 「변이는 검사가 읽는 자리에 넣어라」(api-kit 변이를 처음에 `prefers-reduced-motionX` 로 넣어 도구가 못 잡는 자리였다 — 고쳐 다시 쟀다) · 「zsh 변수 함정 둘」 · 「검사 결과 "0건"을 통과로 읽기 전에」
- 저장소 밖 원문은 쓰지 않았다
