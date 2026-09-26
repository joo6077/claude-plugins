---
feature: "문서 사이트 고침 · 320px 기준 폭 (dca) — DC-2 · DC-5 · DC-7 ~ DC-14"
slug: after-0926-docs-fixes
created: "2026-09-26 20:16"
complexity: "복잡"
conditions: 29
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:a1f762a2866454db
measurement_digest: sha256:57f76c23521e7bc2
locked_at: "2026-09-26 20:31"
---

## 배경

남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md`(읽기만, 기준 판 `6378948`)의 「## docs」 절 가운데 DC-2 · DC-5 ~ DC-14 를 한 묶음으로 처리한다. DC-1(새 페이지) · DC-3 · DC-4 · DC-15(다른 묶음이 원본을 고친 뒤 부모가 함)는 뺐다. DC-6 도 같은 까닭으로 뺐다 — 표 행이 따라야 할 원본 판정 동작을 다른 묶음(KBa-1)이 바꾼다(`## 범위 경계`).

- 사용자 결정: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`(읽기만) — DC-2 「문서 사이트 좁은 화면 기준 폭에 320 을 넣는다」. 위임: 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 사용자 말 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」(앞서 여쭌 세 가지를 실행하고 다음 카이젠으로 넘긴 것도 지금 처리하라는 뜻), 결정 답 2026-09-26T10:30:16.222Z, 그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(2026-09-24T04:04:16.964Z).
- 사용자 합의(Step 5): 위 위임으로 받은 것으로 적는다. 판단이 갈린 곳은 저장소 안 근거로 정해 `## GAP 분석` 과 `## 범위 경계` 에 적었다. 봉인된 조건을 느슨하게 하는 개정(허용 파일 늘리기 · 측정 대상 줄이기 · 문턱 낮추기)은 이 위임으로 동의 처리하지 않는다 — 개정 파일에 동의 칸을 비워 두고 부모가 사용자에게 묻는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dca`, 가지 `chore/ak2-dca`(`origin/main` `6378948` 에서 갈라짐). 범위 구간의 아래 끝은 이 계약의 봉인 커밋(이 계약 파일을 처음 담은 커밋)의 부모다 — 해시를 박지 않고 측정 도우미가 git 기록에서 푼다. 봉인 전 실측 때 그 자리는 `6378948` 이었다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 킷 하나 · `git add -A` · `git stash` · push · 가지 바꾸기 금지. 본 체크아웃과 다른 워크트리는 건드리지 않는다. `.harness/` 파일은 구현 파일과 다른 커밋에 싣는다(AR-09). 이 묶음에서 킷 폴더에 드는 파일은 `design-kit/evals/visuals.spec.js` 하나다.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 스킬 안내 글 · 쪽 스크립트 주석 · notes 가 대상이다. 결과는 notes 에 남긴다(AR-10).
- 기록 파일(notes): `.harness/.meta/after-kaizen-0926b/dca-notes.md` (W 안, 이 가지에 커밋).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · notes 커밋이 가지 `chore/ak2-dca` 에 모두 들어간 뒤, 가지를 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 한다. 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(봉인 커밋의 부모)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다(DG-05 만 작업 폴더를 쓴다).
`HEAD` 를 상한으로 쓰지 않는다. `BASE` · `TIP` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.
「177 쪽」 은 `BASE` 트리의 `find docs -name '*.html'` 결과다(도우미 `PAGES`). 폭을 재는 브라우저는 어두운 색 설정 · 움직임 줄이기 설정으로 `file://` 로 연다.
「글 잘림」 과 「삐져나감」 은 도우미 `pw.js w` 의 정의다 — 글 조각이 스크롤 안 되는 숨김 조상(`overflow` 가 `hidden` · `clip`) 밖으로 2px 넘게 나가면 잘림, 가장 가까운 테두리나 배경이 있는 블록 상자 밖으로 2px 넘게 나가면 삐져나감이다. 같은 쪽을 1280 폭에서도 재서 1280 에서 이미 그런 조각(설계로 잘라 둔 것)은 빼고 좁은 폭에서만 생긴 것을 센다. 화면 밖으로 밀어 둔 서랍 메뉴(글 조각 전체가 화면 왼쪽 밖이거나 오른쪽 밖)는 숨긴 UI 로 보고 뺀다.

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.
기능 조건 20 개는 SK-01 ~ SK-04 · ER-01 ~ ER-04 · AR-01 ~ AR-11 · DG-05 이다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절(AP-03 · AP-04) · 자동 포함 여섯 줄(RE-01 · RE-02 · DG-01 ~ DG-04) · `N/A (` 줄(SC-00 · DG-01 · DG-03)을 빼고 센 값이다.
Step 2.5 짝 조건: 만드는 쪽은 검사 두 곳에 더하는 320 폭(`scripts/check-docs-a11y.js` · `design-kit/evals/visuals.spec.js`, AR-01)과 새 쪽의 틀(`page-template.html`, SK-04) · 스킬 안내(SK-01 ~ SK-03)다. 쓰는 쪽은 그 검사를 부르는 CI(`.github/workflows/ci.yml:131` · `:142`)와 `ci-local.sh`(DG-04 · DG-05 가 끝점에서 실제로 돌려 잰다), 검사를 통과해야 하는 177 쪽(ER-01 · ER-02), 스킬 Step 6 의 검사 호출(`SKILL.md:131`)이다. 쓰는 쪽 파일(`ci.yml` · `ci-local.sh`)은 부르는 명령이 그대로라 고치지 않는다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 정적 문서 화면(HTML · CSS · 쪽 스크립트), 그 화면을 재는 검사 도구, 새 쪽을 만드는 스킬 안내와 틀 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — CI 가 부르는 두 검사의 합격선이 320 폭까지 넓어진다. 새 쪽 틀의 색 값과 스킬 안내가 바뀐다 |
| 소비면 존재 | 반대편이 있는가 | 예 — CI · `ci-local.sh`, 177 쪽, 틀을 쓰는 새 쪽(DC-1 묶음) |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 44 쪽을 고치면서 375 · 768 · 1280 화면과 대비가 깨질 수 있고, 움직임 설정을 따르게 바꾸면 보통 설정의 움직임이 사라질 수 있다 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 (새 notes 와 고치는 `SKILL.md` · `css-tokens.md`) · AP-04 (`SKILL.md` 를 고친다). AP-01 은 더하는 줄에 판 번호가 들어갈 자리가 없어서(폭 숫자 · 안내 글 · 쪽 CSS · 스크립트), AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 실제로 읽고 잰 값이다(시작 판 `6378948`). 측정은 도우미와 같은 식이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `scripts/check-docs-a11y.js` | `:5` 머리 주석 「가로 오버플로(375/768/1280px)」 · `:62` `for (const w of [375, 768, 1280])` · `:142` `const ok = of[375] <= 2 && …` · `:144` `of=${of[375]}/${of[768]}/${of[1280]}` · `:133` 테마 단추를 `#theme-btn` 으로만 찾음 | 기준 폭에 320 이 없다. 틀의 단추 id 는 `themeToggle` 이라 이 검사가 틀로 만든 쪽의 단추 크기를 못 잰다(쪽 22 개가 `theme-btn`, 3 개가 `themeToggle`) | AR-01 · DG-04. 단추 id 는 넘김 |
| `design-kit/evals/visuals.spec.js` | `:11-13` 넘침 허용 쪽 넷(375 이하에서 80px) · `:15-25` `expectNoOverflow` · `:54-56` 등 13 개 `describe` 마다 375 · 768 시험 | 320 시험이 없다. 시작 판 `143 passed` | AR-01 · DG-04 |
| `playwright.config.js` | `:1-16` 전체 — `testDir` · `timeout` · `headless` · `chromium` 뿐 | 폭이 적힌 자리가 없다 — 고칠 것 없음 | 범위 경계 |
| `.claude/skills/docs-site/SKILL.md` | `:5` 「standalone HTML로 변환하고」 · `:16` 「페이지는 반드시 standalone HTML이어야 한다」 · `:104` 「line-height 1.2~1.6배」 · `:109` 「prefers-reduced-motion 대응」 · `:134` 「가로 오버플로(375/768/1280px」 · `:161-165` Step 7 세 항목 · `:25` Gotcha 10 | `:5` · `:16` 이 공통 파일 링크(`:16` 같은 줄)와 어긋나는 옛 원칙을 적는다. `:104` 가 사이트 값 1.7 과 어긋나고, `:109` 는 공통 파일이 맡는 일을 쪽마다 하라고 읽힌다. `:134` 에 320 이 없다. Step 7 에 옛 페이지 대비 담김 조건이 없다. 편집기 경고 9(MD025 2 · MD031 2 · MD032 5, 기존) | SK-01 ~ SK-03 · AP-04 · DG-02 |
| `.claude/skills/docs-site/references/page-template.html` | `:12` `--text3:#7A6F64` · `:19-22` 밝은 테마 덮어쓰기 `--text3:#8a8078` · `:113-122` 테마 단추(`aria-label="테마 전환"`) · `:136-151` `dk-theme` 저장 · 브라우저 색 설정 따라가기 | 어두운 `--text3` 는 `css-tokens.md:51-52` 가 기준으로 적은 `#948779` 가 아니라 대비 미달 옛 값(표면 위 3.34), 밝은 `--text3` 는 밝은 배경 네 곳 위 최소 3.39 로 AA 미달 — 이 틀을 그대로 따르면 DC-12 의 열한 쪽이 밝은 테마 대비에서 떨어진다 | SK-04 · ER-04 |
| `.claude/skills/docs-site/references/css-tokens.md` | `:15` 공통 토큰 코드 블록 `--text3:#7A6F64` · `:51-52` 「`#948779` 가 정본이다」 | 한 파일 안에서 두 값이 어긋난다 | SK-04 · AP-03 |
| DC-12 열한 쪽 (도우미 `THEME_PAGES`) | 열한 쪽 모두 `[data-theme="light"]` 0 · 테마 단추 0 · `dk-theme` 0 (`grep -c`). `check-docs-a11y.js` 시작 판 줄이 모두 `theme=dark-only`, 도우미 `theme` 이 `follow=null/null` 아홉 · `dark/dark` 둘(`design-concept` · `design-mockup` 은 `<html data-theme="dark">`) | 밝은 테마가 없다 | ER-04 · RE-01 |
| 177 쪽 320 폭 | 도우미 `w` 로 전수: 글자 간격 그대로 `doc_ok=165 clip_ok=163 esc_ok=164`(모자란 쪽 32), 글자 간격 +0.06em `doc_ok=155 clip_ok=160 esc_ok=155`(모자란 쪽 44, 앞의 32 를 모두 포함). 예: `docs/design-kit/typography-scale.html` `doc=9 clip=20`(`.type-preview`), `docs/flutter-toolkit/theming.html` 은 +0.06em 에서만 `clip=1`(`ColorScheme.fromSeed(see…` 코드 줄), `docs/flutter-toolkit/widget-composition.html` `doc=40`, `docs/infra-kit/cost-optimization.html` 표 칸 `clip=6` | 목록이 적은 두 쪽 말고도 44 쪽이 320 에서 넘치거나 글이 잘린다. 375 · +0.06em 문서 넘침은 177 쪽 모두 0 (`doc_ok=177`) | ER-01 · ER-02 |
| `docs/assets/site.css` | `:1-11` 본문 행간 1.7 · 움직임 줄이기 두 규칙 | 줄바꿈처럼 사이트 전체에 같아야 하는 규칙을 더할 자리. 있는 두 규칙은 그대로 둬야 한다 | AR-07 |
| 스크립트 움직임 (DC-11 전수) | 177 쪽 `<script>` · `on…=` 속성을 훑음: 부드러운 스크롤 `docs/design-kit/design-template.html:1048` · `grid-alignment.html:689` · `ratio-proportion.html:964` · `visual-hierarchy.html:820`(맨 위로 단추) · `docs/process/kaizen-flow.html:866`(`scrollIntoView`, 시뮬레이터). 스스로 도는 표본 `docs/design-kit/animation.html:887` `riveInterval` · `docs/design-kit/microinteraction.html:975` 진행 막대. `docs/design-kit/motion.html` 은 이미 설정을 확인한다. 도우미 `motion reduce` 가 `motion_ok=170` 과 위 일곱 쪽을 낸다 | 목록의 `docs/flutter-toolkit/animation.html` `.animate(` 는 `:398` Dart 코드 표본 글이라 움직임이 아니다. backend-kit 셋 등 「더 있음」 은 CSS `scroll-behavior` 라 공통 파일이 이미 끈다 | ER-03 |
| `docs/tone-kit/dart-flutter-idioms.html` | `:1287` 「…정본이다(표 칸에 옮기면 대안 기호가 깨진다). 처리는…」 | HTML 표 칸에서는 틀린 말 (원본 `docs/tone/dart-flutter-idioms.md:633` 은 마크다운이라 맞는 말) | AR-02 |
| `docs/api-kit/multi-sample-pagination-variance.html` | `:430` 「정본은 <span class="mono">docs/api/research-log.md</span>」 | 쉬운 말 목록 낱말 | AR-03 |
| DC-10 원문 넷 | `docs/api/verification/static-evidence-viewer-contract.md:9` · `:82` · `:86` `api-ui-v7.html`, `:85` 「56 개 중 24 미만 0 · 44 미만 39」(2026-09-25) · `docs/superpowers/specs/2026-09-02-api-kit-design.md:483` · `:595` · `docs/api-kit/static-evidence-viewer-contract.html:270` · `:352` · `:542` · `:566` · `:640` v7, `:286` · `:559-560` · `:608` · `:618-637` 56 · 39 · 17 수치. 기준: `api-kit/skills/api-ui/SKILL.md:136` · `:249` 확정 시안 v8, `:177` · `:221` v8 실측 `targets 57 · under44 40`(2026-09-26) | 원문 셋이 옛 시안 v7 과 v7 수치를 적는다. 시안 이름만 바꾸면 수치가 틀린 말이 된다 — 수치도 v8 값으로 옮긴다. `docs/api/research-log.md:179` 는 v7 사본을 연 그날의 기록(sha 앞자리까지)이라 그대로 둔다 | AR-04 |
| DC-9 매핑 | `.claude/skills/docs-site/SKILL.md:45-64` 매핑 표 · `scripts/detect-docs-drift.py:33-99` `SOURCE_TO_HTML` · `SOURCE_OVERRIDES`. 도우미 `maplist` 가 시작 판에서 짝 원본 없는 등록 페이지 23 · 없는 페이지를 가리키는 원본 43 을 낸다(목록 당시 21 에서 둘 늘었다) | 규칙이 정해지지 않았다. 스크립트 매핑은 VS-13(다른 묶음)이 같은 파일을 고친다 | AR-05 |
| `docs/harness/contract-schema.html` (DC-13) | 흔들림 재현: 옛 판(`33fec27^`, 높이 31894)과 새 판을 번갈아 캡처하면 옛 판끼리 비교에서 네 번에 한 번 `diff=1118`, 다른 픽셀 상자 `81,29743-1198,29743` 한 줄. 그 줄은 `code.code-block`(`top=29692.297 bottom=29744.703`) 아래 1px 테두리 — 소수 자리 y 에 걸친 가는 선의 번짐이 캡처마다 달라진 것. 높이는 여덟 번 모두 같았다. 지금 판(높이 32927)은 같은 판 여섯 번 · 번갈아 여섯 번 모두 0 | 쪽 레이아웃이 흔들리는 것이 아니라 가는 선 번짐이다. 레포 안 검사 중 픽셀 비교를 하는 것은 없다 | AR-06 |
| `docs/bambu-kit/bambu-print-profile.html` (DC-6) | `:1648` 「목록 파일이 비었거나 깨짐 → 같음」 · 원본 `bambu-kit/skills/bambu-print-profile/SKILL.md:1604-1612` | 표 행이 따라야 할 원본 동작을 KBa-1(다른 묶음)이 바꾼다 | 범위 경계 (뺌) |
| `design-kit/skills/design-audit/references/audit-criteria.md` | `:97` 「최소 지원 뷰포트(375px) … 375px 와 2px 허용치는 이 킷의 판정값이다」 | 킷의 감사 판정값이지 문서 사이트 검사가 아니다 | 범위 경계 (넘김) |

구현 후보가 갈린 곳 — 저장소 안 근거로 하나씩 정했다.

| 갈린 곳 | 고른 것 | 버린 것 | 근거 |
| --- | --- | --- | --- |
| 320 에서 글자 간격 +0.06em 도 볼지 | 본다(ER-02) | 글자 간격 그대로만 | CI 는 리눅스에서 돌고 맥보다 글자를 넓게 그린다. `check-docs-a11y.js` 가 320 을 재기 시작하면 맥에서 아슬아슬하게 맞춘 쪽이 CI 에서 떨어진다. 목록이 짚은 theming 코드 줄 잘림도 +0.06em 에서만 나온다 |
| 글 잘림을 무엇으로 셀지 | 잘림 · 삐져나감 둘 다, 1280 에서 이미 그런 것은 빼고 | 문서 넘침만 | 문서 넘침 0 이어도 표 칸 · 카드 안에서 글이 잘린다(`cost-optimization` 표 칸). 1280 에서도 잘린 것은 설계로 잘라 둔 것이라 좁은 폭 결함이 아니다 |
| 밝은 테마 규칙을 둘 곳 | 열한 쪽마다 틀과 같은 방식(`[data-theme="light"]` 덮어쓰기 · 테마 단추 · `dk-theme` 저장 · 브라우저 색 설정 따라가기) | 공통 파일에 밝은 토큰 | 쪽마다 자기 색을 직접 적은 곳이 있어 공통 토큰만 바꾸면 대비가 쪽마다 다르게 깨진다. 공통 파일에 두면 이미 밝은 테마가 있는 33 쪽의 규칙과 겹친다 |
| 틀의 `--text3` | 어두운 값은 `css-tokens.md` 가 기준으로 적은 `#948779`, 밝은 값은 밝은 배경 네 곳 위 4.5 이상인 값 | 틀 그대로 | 틀 그대로 따르면 열한 쪽이 밝은 테마 대비에서 떨어지고, 새 쪽(DC-1)도 따라 떨어진다 |
| DC-9 적용 자리 | 결정은 notes 에만 적는다. 매핑 표 · 스크립트는 고치지 않는다 | 매핑 표를 같이 고치기 | `SKILL.md:45-46` 이 「표를 고치면 스크립트의 매핑도 같은 커밋에서 고친다」 인데 스크립트는 VS-13(다른 묶음, 목록의 다른 절)이 고친다. 과제도 「notes 에 적는다」 다 |

## Skill

- [ ] SK-01: docs-site `SKILL.md` 가 공통 파일 규칙과 어긋나는 옛 안내를 더는 적지 않는다 (DC-5) — Given 공통 전제 G, When `m SK-01`, Then `standalone=0`(설명 `:5` · Gotcha 1 `:16` 의 「standalone」 이 사라짐) · `lh_old=0`(「1.2~1.6」 없음) · `typo_ok=1`(`- **Typography**` 줄이 하나이고 그 줄에 `site.css` 와 `1.7` 이 함께 있음) · `motion_ok=1`(`- **Motion**` 줄이 하나이고 그 줄에 `site.css` 와 `matchMedia` 가 함께 있음 — CSS 움직임은 공통 파일이 맡고 스크립트 움직임은 쪽이 설정을 확인한다) · `fm_same=1`(머리 설정은 설명 둘째 줄 말고 글자 그대로 — 부르는 낱말이 그대로다) · `gotcha10_same=1` [exact]
  측정: `m SK-01` 의 한 줄. 시작 판 `standalone=2 lh_old=1 typo_ok=0 motion_ok=0 fm_same=1 gotcha10_same=1`, 모의 좋은 판 `0 0 1 1 1 1`
  양성 대조: 나쁜 판(설명에 「standalone」 을 되살리고 `argument-hint` 를 바꿈) → `fm_same=0 standalone=1` (봉인 전 실측). `gotcha10_same` 은 `# Gotchas` 절 안의 `10. ` 줄만 견준다 — 절 밖에 `10. ` 줄을 더한 판 → `1`, Gotcha 10 첫 줄을 바꾼 판 → `0` (봉인 전 실측)
- [ ] SK-02: 문서 사이트 QA 절(`## Step 7`)이 있던 페이지를 다시 만들 때 담김 조건을 넣으라고 적는다 (DC-14) — Given 공통 전제 G, When `m SK-02`, Then Step 7 의 번호 항목이 시작 판보다 1 개 이상 늘고(`s7_items=3->4` 이상), 그 절에 「옛 페이지」 가 1 번 이상, 글자 그대로 「빠진 수 0」 이 1 번 이상(옛 페이지에 있던 원본 코드 표시가 새 페이지에서 빠진 수), 「낱말 비율이 옛 페이지 이상」 이 1 번 이상 있다 — `s7_old>=1 s7_lost>=1 s7_ratio_rule>=1` [exact]
  측정: `m SK-02`(`m SK-01` 과 같은 줄). 시작 판 `s7_items=3->3 s7_old=0 s7_lost=0 s7_ratio_rule=0`, 모의 좋은 판 `3->4 2 1 1`
  양성 대조: 시작 판이 곧 나쁜 판이다 — 세 값 모두 0 (봉인 전 실측). Step 7 절은 다음 `#` · `##` 제목에서 끝난다 — Step 7 과 `# References` 사이에 `## 덧붙임` 절(번호 줄 · 「빠진 수 0」 · 「낱말 비율이 옛 페이지 이상」)을 끼운 나쁜 판 → `s7_items=3->3 s7_lost=0 s7_ratio_rule=0` (고치기 전 식은 `3->4 1 1` 로 잘못 셌다, 봉인 전 실측)
- [ ] SK-03: 스킬의 자가 검증 안내가 320 폭을 적는다 (DC-2) — Given 공통 전제 G, When `m SK-03`, Then 글 `320/375/768/1280px` 가 든 줄이 정확히 1 개다 — `w320_line=1` [exact]
  측정: `m SK-03`(`m SK-01` 과 같은 줄). 시작 판 `w320_line=0`, 모의 좋은 판 `1`
  양성 대조: 나쁜 판 셋 — 빈칸을 넣은 `320 / 375 / 768 / 1280px` → `w320_line=0`, 순서를 바꾼 `375/768/1280/320px` → `0`, 같은 글을 두 줄에 적은 판 → `2` (봉인 전 실측)
- [ ] SK-04: 새 쪽의 틀과 토큰 문서의 `--text3` 가 대비 기준을 넘는다 (DC-12 공통 틀) — Given 공통 전제 G, When `m SK-04` 가 `page-template.html` 의 `:root` 와 `[data-theme="light"]` 블록, `css-tokens.md` 의 첫 `css` 코드 블록에서 `--text3` 를 읽어 WCAG 대비를 계산하면, Then `tpl_dark_text3=#948779` 이고 `tpl_dark_min`(어두운 bg · bg2 · surface · surface2 위 최솟값) 4.5 이상, `tpl_light_min`(밝은 네 배경 위 최솟값) 4.5 이상, `tokens_block_text3=#948779` [exact]
  측정: `m SK-04`. 시작 판 `tpl_dark_text3=#7A6F64 tpl_dark_min=3.34 tpl_light_text3=#8a8078 tpl_light_min=3.39 tokens_block_text3=#7A6F64`, 모의 좋은 판(밝은 값 `#6b6259`) `#948779 4.68 #6b6259 5.25 #948779`
  양성 대조: 시작 판이 곧 나쁜 판이다 (봉인 전 실측). 틀의 `[data-theme="light"] {` 처럼 중괄호 앞에 빈칸을 넣은 판도 `tpl_light_text3=#8a8078` 로 읽는다(고치기 전 식은 `None`, 봉인 전 실측)

## Script

- [ ] SC-00: N/A (릴리스 스크립트 · 판 올리기 · `marketplace.json` 은 이 계약이 건드리지 않는다 — 킷 폴더에 드는 파일은 `design-kit/evals/visuals.spec.js` 하나이고 판 올림 판단은 notes 에 적는다(AR-10). 측정: `m SC-00` 이 `release_paths=0`. 양성 대조: 나쁜 판(`scripts/release.sh` 를 고쳐 커밋) → `release_paths=1`, 봉인 전 실측) [exact]

## Error

- [ ] ER-01: 177 쪽이 320 폭에서 가로로 넘치지 않고 글이 잘리거나 삐져나가지 않는다 (DC-2) — Given 공통 전제 G, When `m ER-01` 이 쪽마다 1280 폭에서 글 조각을 훑은 뒤 320 폭으로 줄여 다시 훑으면, Then 끝줄이 `doc_ok=177 clip_ok=177 esc_ok=177` 이고(문서 넘침 2px 이하 · 320 에서만 생긴 잘림 0 · 삐져나감 0 인 쪽 수), 같은 도우미가 시작 판과 견준 `wide_worse=0`(1280 에서의 잘림 · 삐져나감 수가 시작 판보다 늘어난 쪽 0) [exact, collective]
  측정: `m ER-01`. 시작 판 끝줄 `w=320 ls=0 pages=177 doc_ok=165 clip_ok=163 esc_ok=164`(두 번 재 같은 값), 모자란 쪽 32 가 `BAD` 줄로 나온다
  양성 대조: 시작 판의 `BAD docs/design-kit/typography-scale.html doc=9 clip=20` · `BAD docs/flutter-toolkit/widget-composition.html doc=40` · `BAD docs/infra-kit/cost-optimization.html … clip=6` (봉인 전 실측)
- [ ] ER-02: 글자 간격이 넓어져도(CI 리눅스가 글자를 더 넓게 그리는 것을 맥에서 흉내) 320 폭에서 같은 결과이고 375 폭 넘침도 그대로 0 이다 (DC-2) — Given 공통 전제 G, When `m ER-02` 가 `*{letter-spacing:0.06em !important}` 를 넣고 ER-01 과 같이 재면, Then 첫 끝줄이 `doc_ok=177 clip_ok=177 esc_ok=177` · `wide_worse=0` 이고, 같은 조건 375 폭 끝줄의 `doc_ok=177` [exact, collective]
  측정: `m ER-02`. 시작 판 `w=320 ls=1 pages=177 doc_ok=155 clip_ok=160 esc_ok=155`(모자란 쪽 44), 375 `doc_ok=177`
  양성 대조: 시작 판의 `BAD docs/flutter-toolkit/theming.html doc=0 clip=1 esc=0`(`ColorScheme.fromSeed(see…`) — 글자 간격 그대로에서는 `OK` 인 쪽이다 (봉인 전 실측)
- [ ] ER-03: 움직임 줄이기 설정에서 스크립트가 주는 움직임도 멈추고, 보통 설정의 움직임은 그대로다 (DC-11) — Given 공통 전제 G, When `m ER-03` 이 177 쪽을 움직임 줄이기 설정으로 열어 손대지 않은 2 초 동안 `style` · `class` 가 바뀌는 요소를 세고, `onclick` 에 `scroll` 이 든 요소를 모두 누르고, `#simStart` 가 있으면 눌러 2.5 초 기다린 뒤 부드러운 스크롤 호출(`scrollTo` · `scrollBy` · `scrollIntoView` 의 `behavior:'smooth'`)과 길이 있는 `animate()` 호출을 세면, Then 모두 0 인 쪽이 177 — `pref=reduce … motion_ok=177`. 그리고 같은 재기를 보통 설정(`no-preference`)으로 도우미 `SMOOTH_PAGES` 다섯 쪽과 `AUTO_PAGES` 두 쪽에 하면 일곱 줄 모두 `BAD` 이고 앞 다섯은 `smooth=` 1 이상, 뒤 둘은 `automut=` 1 이상이다 — `pref=no-preference pages=7 motion_ok=0` [exact, enumerated]
  측정: `m ER-03`. 시작 판 `pref=reduce pages=177 motion_ok=170`(`BAD` 일곱: `docs/design-kit/animation.html` `automut=1` · `docs/design-kit/microinteraction.html` `automut=2` · `docs/design-kit/design-template.html` · `docs/design-kit/grid-alignment.html` · `docs/design-kit/ratio-proportion.html` · `docs/design-kit/visual-hierarchy.html` `smooth=1` · `docs/process/kaizen-flow.html` `smooth=5`), 보통 설정 `motion_ok=0`
  음성 대조: 부드러운 스크롤을 모든 설정에서 `auto` 로 바꾸거나 표본 타이머를 지우면 둘째 끝줄이 `motion_ok=` 1 이상이 되어 FAIL 한다 — 움직임을 없애는 것이 아니라 설정을 따르게 하는 것을 잰다
- [ ] ER-04: 어두운 테마 전용이던 열한 쪽에 밝은 테마가 생기고 틀과 같은 방식으로 바뀐다 (DC-12) — Given 공통 전제 G, When `m ER-04` 가 도우미 `THEME_PAGES` 의 열한 쪽(`docs/backend-kit/api-lifecycle.html` · `docs/design-kit/design-concept.html` · `docs/design-kit/design-mockup.html` · `docs/design-kit/typography-scale.html` · `docs/flutter-toolkit/theming.html` · `docs/onboarding-kit/setup-guide.html` · `docs/process/kaizen-flow.html` · `docs/rust-kit/grpc-tonic.html` · `docs/rust-kit/observability.html` · `docs/rust-kit/ownership-borrowing.html` · `docs/rust-kit/project-structure.html`)을 레포 검사기로 재고 도우미 `theme` 로 열면, Then 검사기 줄이 열하나 모두 `OK` · `theme=both`(밝은 테마의 글자 대비도 잰다) · 끝줄 `11/11 PASS` 이고, 도우미 끝줄이 `pages=11 theme_ok=11` — 쪽마다 저장값이 없을 때 브라우저 색 설정을 따르고(`follow=light/dark`), 접근 이름에 「테마」 가 든 단추가 정확히 하나이며 375 폭에서 44×44 이상이고, 누르면 `data-theme` 이 바뀌고 `dk-theme` 에 저장되며 다시 열어도 유지되고, 저장소 키가 `dk-theme` 하나다 [exact, enumerated]
  측정: `m ER-04`. 시작 판 검사기 줄 열하나 모두 `theme=dark-only` · `11/11 PASS`, 도우미 `pages=11 theme_ok=0`(`follow=null/null` 아홉 · `dark/dark` 둘 · `btn=0`)
  양성 대조: 시작 판이 곧 나쁜 판이다 (봉인 전 실측)

## Architecture

- [ ] AR-01: 문서 사이트를 재는 두 검사가 320 폭을 잰다 (DC-2) — `scripts/check-docs-a11y.js` 는 폭 목록 `for (const w of [320, 375, 768, 1280])` 한 줄, 합격 식 `of[320] <= 2 && of[375] <= 2` 한 줄, 출력 `of=${of[320]}/${of[375]}/${of[768]}/${of[1280]}` 한 줄, 머리 주석 「가로 오버플로(320/375/768/1280px)」 한 줄을 갖고, `design-kit/evals/visuals.spec.js` 는 13 개 `describe` 마다 `test('no horizontal overflow at 320px'` 와 `expectNoOverflow(page, url, 320)` 을 하나씩 갖는다. Given 공통 전제 G, When `m AR-01`, Then `a11y_widths=1 a11y_ok320=1 a11y_print=1 a11y_head=1` · `vis_tests320=13 vis_call320=13 vis_describe=13` [exact]
  측정: `m AR-01`. 시작 판 `a11y_widths=0 a11y_ok320=0 a11y_print=0 a11y_head=0` · `vis_tests320=0 vis_call320=0 vis_describe=13`, 모의 좋은 판 모두 기대값. 두 검사가 실제로 320 을 재는지는 DG-04 가 끝점에서 돌려 본다(모의 판에서 쪽을 안 고치면 `165/177 PASS` · `5 failed`)
- [ ] AR-02: tone-kit 쪽에서 괄호 한 토막만 뺀다 (DC-7) — `docs/tone-kit/dart-flutter-idioms.html` 에서 바뀐 줄이 정확히 한 줄이고, 그 줄은 시작 판 줄에서 「(표 칸에 옮기면 대안 기호가 깨진다)」 만 지운 것과 글자까지 같다. Given 공통 전제 G, When `m AR-02`, Then `changed=1/1 old_left=0 exact=1` [exact]
  측정: `m AR-02`. 시작 판 `changed=0/0 old_left=1 exact=0`, 모의 좋은 판 `1/1 0 1`
  양성 대조: 나쁜 판(같은 쪽 `<title>` 도 바꿈) → `changed=2/2 exact=0` (봉인 전 실측)
- [ ] AR-03: api-kit 쪽의 「정본은」 을 「기준 기록은」 으로 바꾼다 (DC-8) — `docs/api-kit/multi-sample-pagination-variance.html` 에서 바뀐 줄이 정확히 한 줄이고, 그 줄은 시작 판 줄의 「정본은」 을 「기준 기록은」 으로 바꾼 것과 글자까지 같다. Given 공통 전제 G, When `m AR-03`, Then `changed=1/1 old_left=0 new_n=1 exact=1` [exact]
  측정: `m AR-03`. 시작 판 `changed=0/0 old_left=1 new_n=0 exact=0`, 모의 좋은 판 `1/1 0 1 1`
  양성 대조: 나쁜 판(바꾼 뒤 공백 하나를 더 넣음) → `exact=0` (봉인 전 실측)
- [ ] AR-04: 옛 시안 v7 기재를 v8 로 고치고 인용 수치도 v8 실측으로 옮긴다 (DC-10) — Given 공통 전제 G, When `m AR-04`, Then `docs/api/verification/static-evidence-viewer-contract.md` 가 `md_v7=0 md_v8=3 md_row=1`(누르는 자리 행이 「57 개 중 24 미만 0 · 44 미만 40」 과 `2026-09-26` 을 담음), `docs/superpowers/specs/2026-09-02-api-kit-design.md` 가 `spec_v7=0 spec_v8=2 spec_hist=1`(「사용자 확정 2026-09-03」 이력은 남김), `docs/api-kit/static-evidence-viewer-contract.html` 이 `page_v7=0 page_v8=5 page_old=0`(옛 수치 글 여덟 가지 `56 개` · `/ 56` · `56 에서` · `미만 39` · `39 /` · `39 개` · `39 를` · `(2026-09-25)` 모두 0) · `page_40of57=1 page_17of57=1 page_0of57=1` · `page_57` 3 이상이고, 그날의 기록 `docs/api/research-log.md` 는 그대로 `rlog_v7=1` [exact]
  측정: `m AR-04`. 시작 판 `md_v7=3 md_v8=0 md_row=0 spec_v7=2 spec_v8=0 spec_hist=1 page_v7=5 page_v8=0 page_old=17 page_57=0 page_40of57=0 page_17of57=0 page_0of57=0 rlog_v7=1`, 모의 좋은 판 `0 3 1 0 2 1 0 5 0 4 1 1 1 1`
  양성 대조: 시작 판이 곧 나쁜 판이다 (봉인 전 실측)
- [ ] AR-05: 매핑 규칙을 저장소 안 근거로 정해 notes 에 표로 적는다 (DC-9) — notes 의 `## DC-9` 로 시작하는 절에 표가 있고, 도우미 `maplist` 가 시작 판에서 뽑은 짝 원본 없는 등록 페이지 23 개와 없는 페이지를 가리키는 원본 43 개가 각각 첫 칸에 백틱으로 든 행을 갖는다. 행의 둘째 칸(결정)은 `원본:` · `원본 없음` · `새 페이지` · `짝:` · `페이지 없음이 맞음` 가운데 하나로 시작하고, 셋째 칸(근거)은 한글 10 자 이상이다. 같은 절에 `docs/howto/design-brief.md` 와 `docs/howto-kit/overview.html` 을 함께 담은 행, `process (공유)` 와 `.claude/skills/kaizen-orchestrator/SKILL.md` 를 함께 담은 행이 있다. Given 공통 전제 G, When `m AR-05`, Then `list_orphan=23 list_missing=43` · `section=1 orphan=23/23 missing=43/43 howto_pair=1 process_row=1` [exact, collective]
  측정: `m AR-05`. 시작 판 `list_orphan=23 list_missing=43` · `section=0 orphan=0/23 missing=0/43 howto_pair=0 process_row=0`, 모의 notes `section=1 orphan=23/23 missing=43/43 howto_pair=1 process_row=1`
  양성 대조: 나쁜 notes(한 행의 결정 칸을 비움) → `orphan=22/23` (봉인 전 실측)
- [ ] AR-06: 긴 쪽 캡처 흔들림의 원인과 재현을 notes 에 남긴다 (DC-13) — notes 에 토큰 `contract-schema.html` · `29743` · `code-block` · `1118` · `소수` · `pixalt` 가 각각 한글 15 자 이상인 줄에 1 번 이상 든다(원인: 옛 판 `code.code-block` 아래 1px 테두리가 소수 자리 y 에 걸쳐 캡처마다 한 줄 1118 픽셀 번짐이 달라짐, 재현: 도우미 `pw.js pixalt` 명령과 잰 값, 지금 판의 반복 캡처 값). 원인이 쪽 결함이 아니라 가는 선 번짐이면 쪽은 고치지 않는다. Given 공통 전제 G, When `m AR-06`, Then 끝줄의 여섯 토큰 값이 모두 1 이상 [exact, enumerated]
  측정: `m AR-06`. 시작 판 `notes=absent`. 같은 도우미가 찍는 `pix` · `pixalt` 두 줄은 보고용이다(판정에 쓰지 않음 — 흔들림이 간헐이라 봉인 전 번갈아 재기 두 번에서 옛 판 `diffs=0,1118,0,0` 과 `0,0,0,0,0` 이 나왔다). 봉인 전 지금 판 `pix … zero=5/5` · `pixalt … zero=5/5`
  양성 대조: 모의 notes(원인 설명 한 줄만, 재현 명령 줄 없음) → `contract-schema.html=1 29743=1 code-block=1 1118=1 소수=1 pixalt=0` (봉인 전 실측)
- [ ] AR-07: 넘침을 가리지 않고 공통 파일의 두 규칙을 지킨다 — 177 쪽과 `docs/assets/site.css` 에서 `overflow(-x|-y)?:hidden|clip` · `text-overflow:ellipsis` · `display:none` · `visibility:hidden` 선언 수가 시작 판보다 늘어난 파일이 0 이고, `site.css` 에 `body{line-height:1.7}` 줄과 `@media (prefers-reduced-motion: reduce){` 줄이 그대로 1 번씩 있다. Given 공통 전제 G, When `m AR-07`, Then `hide_added=0` · `site_lh=1 site_rm=1` [exact]
  측정: `m AR-07`. 시작 판 `hide_added=0` · `site_lh=1 site_rm=1`
  양성 대조: 나쁜 판(`docs/backend-kit/api-design.html` 에 `overflow-x:hidden` 한 줄) → `hide_added=1` (봉인 전 실측)
- [ ] AR-08: 바뀐 파일이 허용 집합 안이고 반드시 바뀔 열 파일이 모두 바뀌며 계약 봉인이 깨지지 않는다 — `git diff --name-only BASE TIP -- . ':(exclude).harness'` 의 경로가 모두 허용 집합(도우미 `FIXED` 열 파일 · `docs/assets/site.css` · `docs/` 아래 `.html`) 안이고 `FIXED` 열 파일은 모두 들어 있으며, PNG 0 · `docs/` 안 수정 아닌 변경(추가 · 삭제 · 이름 바꿈) 0 이다. `.harness/` 는 이름을 열거하지 않고 끝점 트리의 `sprint-contract*.md` 모두에 봉인 검사를 돌려 `SEAL_BROKEN` 이 0 이다. Given 공통 전제 G, When `m AR-08`, Then `extra=0 missing=0 png=0` · `docs_not_modify=0` · `seal_broken=0` [exact, collective]
  측정: `m AR-08`. 시작 판 `changed=0 extra=0 missing=10 png=0` · `docs_not_modify=0` · `seal_broken=0`, 모의 좋은 판 `changed=10 extra=0 missing=0 png=0`
  양성 대조: 나쁜 판 → `extra=4 png=1`(`api-kit/evals/api-ui.spec.js` · `docs/cap.png` · `scripts/new-check.py` · `scripts/release.sh`) · `docs_not_modify=1` · 앞 계약 조건 줄 한 글자를 바꾼 판 `seal_broken=1` (봉인 전 실측)
- [ ] AR-09: 커밋이 킷 둘을 섞지 않고 `.harness/` 와 구현 파일을 섞지 않는다 — `BASE` 부터 `TIP` 까지 병합 아닌 커밋 가운데 최상위 킷 폴더(시작 판에서 `*/.claude-plugin/plugin.json` 을 가진 폴더) 둘 이상을 담은 커밋 0, `.harness/` 파일과 그 밖의 파일을 함께 담은 커밋 0. Given 공통 전제 G, When `m AR-09`, Then `multi_kit=0 mixed=0` 이고 `impl_commits` 1 이상 [exact]
  측정: `m AR-09`. 시작 판 `impl_commits=0 multi_kit=0 mixed=0`, 모의 좋은 판 `impl_commits=2 multi_kit=0 mixed=0`
  양성 대조: 나쁜 판(`design-kit` · `api-kit` · notes · 쪽을 한 커밋에) → `multi_kit=1 mixed=1` (봉인 전 실측)
- [ ] AR-10: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 가 커밋돼 있고 열두 토큰 `DC-2` · `site.css` · `tone-guide` · `DC-6` · `KBa-1` · `.animate(` · `theme-btn` · `audit-criteria` · `--text3` · `design-kit/evals` · `playwright.config.js` · `DC-10` 이 각각 한글 15 자 이상인 줄에 1 번 이상 든다. 담을 내용: 320 에서 고친 쪽과 수단(공통 파일로 푼 것 · 쪽에서 푼 것), `tone-guide` 1 · 5 단계 결과, DC-6 을 KBa-1 뒤로 뺀 까닭, `.animate(` 가 Dart 코드 표본이라 움직임이 아닌 것, 검사기가 `theme-btn` 만 찾아 틀의 단추를 못 재는 것, `audit-criteria` 의 375 가 킷 판정값이라 그대로 둔 것, 틀 `--text3` 를 바꾼 까닭, `design-kit/evals` 를 고친 킷의 판 올림 판단, `playwright.config.js` 에 폭이 없어 고칠 것이 없는 것, DC-10 에서 수치까지 옮긴 까닭과 그대로 둔 기록. Given 공통 전제 G, When `m AR-10`, Then `committed=1` 이고 열두 값 모두 1 이상 [exact, enumerated]
  측정: `m AR-10`. 시작 판 `committed=0` · `notes=absent`, 모의 notes `committed=1` 과 열두 값 1
  양성 대조: 토큰만 남기고 설명을 지운 줄이 있는 나쁜 notes → `tone-guide=0` (봉인 전 실측). 평가자는 셈이 잡은 줄마다 그 줄이 실제로 그 결정이나 넘김을 설명하는지 한 번 눈으로 읽는다 — 토큰을 끼워 넣은 빈말 줄이면 그 값은 0 으로 본다
- [ ] AR-11: 바뀐 쪽을 브라우저로 캡처해 확인했고 캡처는 커밋하지 않았다 — notes 에 `캡처 폴더: \`<절대 경로>\`` 한 줄이 있고, 그 폴더에 바뀐 `docs/` 쪽마다 `320` · `375` · `1280` 세 폭 × 어두운 테마(끝점에서 `[data-theme="light"]` 규칙이 있는 쪽은 밝은 테마까지) 캡처가 이름 규칙 `<폴더>__<쪽 이름>-<폭>-<dark|light>.png`(하위 폴더는 `-` 로 잇는다)로 모두 있고 비어 있지 않으며, 규칙 밖 이름의 PNG 가 0 이다. PNG 가 커밋되지 않은 것은 AR-08 `png=0` 이 잰다. Given 공통 전제 G, When `m AR-11`, Then `cap_need` 와 `cap_have` 가 같고 `cap_badname=0` [exact, collective]
  측정: `m AR-11`. 시작 판 `cap_dir=absent`, 모의 판(세 쪽 · 18 장 중 한 장을 빼고 이름 틀린 한 장을 넣음) `cap_need=18 cap_have=17 cap_badname=1`
  양성 대조: 위 모의 판 (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  이 계약에 적용: 새 notes 와 고치는 `SKILL.md` · `css-tokens.md`. V6 는 킷 폴더만 읽어 이 셋을 보지 않으므로 도우미 `bare` 가 V6 와 같은 셈(줄 앞 공백을 벗긴 뒤 백틱 셋으로 시작하면 열고 닫기를 번갈아 셈)을 돌린다. 측정: `m AP-03` 이 `dca-notes.md=absent->0 SKILL.md=0->0 css-tokens.md=0->0` (시작 판 `absent->absent 0->0 0->0`)
  양성 대조: 나쁜 notes(언어 없는 울타리) → `dca-notes.md=absent->1` (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  이 계약에 적용: 고치는 `.claude/skills/docs-site/SKILL.md` 의 첫 머리 설정 블록에 `name` 이 그대로 있다. 측정: `m AP-04` 가 `fm_name=docs-site` (시작 판 같은 값). 설명 둘째 줄 말고 머리 설정이 바뀌면 SK-01 `fm_same=0` 이 잡는다

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
  이 계약에 적용: 테마 전환은 틀과 기존 쪽이 쓰는 저장 키 `dk-theme` 를 그대로 쓰고 새 키를 만들지 않는다(`SKILL.md:32` Gotcha 13). 측정: `m RE-01` 이 `docs/` 더한 줄의 `localStorage.getItem`/`setItem` 키를 세어 `key[dk-theme]=<1 이상>` 만 찍고 다른 키 0 (시작 판 빈 출력)
  양성 대조: 나쁜 판(`localStorage.setItem('theme', …)` 한 줄) → `key[theme]=1` (봉인 전 실측)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  이 계약에 적용: 320 폭은 새 검사 도구를 만들지 않고 있는 두 검사에 더한다. 측정: `m RE-02` 가 `new_files_scripts=0 new_checker=0`(`scripts/` · `design-kit/evals/` 새 파일 0, `.harness/` 밖 새 `.js` · `.py` · `.sh` 0) (시작 판 같은 값)
  양성 대조: 나쁜 판(`scripts/new-check.py`) → `new_files_scripts=1 new_checker=1` (봉인 전 실측)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_paths=0`. 양성 대조: 나쁜 판 → `release_paths=1`) [exact]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외)
  편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 바뀐 `docs/` 쪽과 틀 가운데 짝 안 맞는 태그 수가 시작 판보다 늘어난 파일 0, notes 의 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0, 고치는 마크다운 넷의 경고 수가 시작 판 이하(시작 판 `SKILL.md` 9 · `css-tokens.md` 0 · `static-evidence-viewer-contract.md` 11 · `2026-09-02-api-kit-design.md` 70 — 범위 밖 기존 경고), 고치는 두 스크립트의 `node --check` 출력 0 줄. 측정: `m DG-02` 가 `tag_worse=0 md_notes=0 md_skill=9-><9 이하> md_tokens=0->0 md_evmd=11-><11 이하> md_spec=70-><70 이하>` · `js_syntax=0/0` (시작 판 `tag_worse=0 md_notes=absent md_skill=9->9 md_tokens=0->0 md_evmd=11->11 md_spec=70->70` · `js_syntax=0/0`). 설치가 안 되면(망 끊김 등) 도우미가 `md=ENV_FAIL` 을 찍는다 — 그 칸만 `[미검증:ENV]` 로 적고 나머지 칸은 그대로 판정한다
  양성 대조: 나쁜 notes(언어 없는 울타리 · 토큰만 남긴 줄) → `md_notes=3` (AP-03 나쁜 notes 와 같은 판, 봉인 전 실측). 모의 notes 는 `md_notes=0`
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 `m DG-01` 이 `release_paths=0`) [exact]
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
  이 계약에 적용: 끝점 트리에서 레포 검사기 `node scripts/check-docs-a11y.js`(인자 없이 — `docs/` 177 쪽 전부의 넘침 320 · 375 · 768 · 1280 · 콘솔 오류 · 글자 대비 · 누르는 자리 크기)와 `npx playwright test design-kit/evals/visuals.spec.js` 를 돌린다. 측정: `m DG-04` 가 `a11y_rc=0 177/177 PASS` · `visuals_rc=0 156 passed`(실패 수 표시 없음) (시작 판 `a11y_rc=0 177/177 PASS` · `visuals_rc=0 143 passed`)
  음성 대조: 검사에 320 만 더하고 쪽을 고치지 않은 모의 판 → `a11y_rc=1 165/177 PASS` · `visuals_rc=1 5 failed 151 passed` (봉인 전 실측) — 두 검사가 320 을 실제로 재고, 쪽 고침을 지우면 이 조건이 떨어진다
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력 — 아니면 도우미가 `W_NOT_TIP` 을 찍고 멈춘다), When `m DG-05` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌려 그 요약 파일을 읽으면, Then `tool_same=1 rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` 이고 `outside=` 칸이 설치 단계 넷(`pip install pyyaml` · `zsh` 설치 · `npm ci` · `npx playwright install --with-deps chromium`)과 여러 줄 `run: |` 한 줄뿐이다 [exact]
  측정: `m DG-05`. 도구 파일은 이 가지 밖(본 체크아웃)에 있어 커밋으로 고정되지 않으므로 도우미가 그 내용 지문(`git hash-object`)을 봉인 때 값 `TOOL_BLOB` 과 대조한다. 시작 판 `tool_same=1 rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` · 같은 `outside`. `tool_same=0` 이거나 요약 파일이 없으면(`ci_summary=absent`) 그 회차는 `[미검증:ENV]` 로 적는다
  음성 대조: 이 계약이 기대는 `docs-a11y` · `playwright-visuals` 단계는 DG-04 의 음성 대조대로 쪽 고침을 지우면 `rc=1` 이 된다

## 범위 경계

항목별 처리 — 입력은 목록 「## docs」 절의 DC-2 · DC-5 ~ DC-14 와 Pre-Edit 감사에서 나온 것이다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| DC-2 320 기준 폭 | 계약에 넣음 | AR-01 · SK-03 · ER-01 · ER-02 · DG-04. 기준 폭이 적힌 자리는 `scripts/check-docs-a11y.js` 넷(`:5` · `:62` · `:142` · `:144`) · `design-kit/evals/visuals.spec.js` 13 곳 · `SKILL.md:134` 이다. `playwright.config.js` · `docs/assets/site.css` 에는 폭이 없다. `check-docs-a11y.js:54` 의 첫 창 크기 375 는 기준 폭 목록이 아니라 창을 여는 크기라 그대로 둔다. `visuals.spec.js:13` 의 넘침 허용 80px 쪽 넷은 375 이하에 걸려 320 에도 걸린다 — 그대로 둔다(ER-01 이 177 쪽을 2px 로 따로 잰다) |
| DC-5 스킬 안 어긋난 안내 | 계약에 넣음 | SK-01. `:16` 의 공통 파일 문장은 앞 묶음이 이미 넣었다 — 남은 것은 「standalone」 두 곳 · `:104` · `:109` 다 |
| DC-6 bambu 미검증 표 | 뺌 — 다른 묶음 원본 뒤 | 목록 비고가 「KBa-1 뒤」 다. KBa-1 이 「종류 줄만 빠진 목록」 의 판정 동작을 바꾸고 「enum 값 검사 미실행」 을 더하므로 지금 원본(`SKILL.md:1604-1612`)에 맞춰 행을 쓰면 KBa-1 뒤에 다시 틀린다. DC-3 · DC-4 · DC-15 와 같은 부류로 부모에게 돌린다 |
| DC-7 · DC-8 | 계약에 넣음 | AR-02 · AR-03 |
| DC-9 매핑 규칙 | 계약에 넣음 (notes 결정만) | AR-05. 매핑 표(`SKILL.md:45-64`) · `scripts/detect-docs-drift.py` 는 고치지 않는다 — 스크립트는 VS-13 이 고치고 표는 스크립트와 같은 커밋에서 고친다는 규칙(`SKILL.md:45-46`)이 있다. notes 의 결정 표를 VS-13 이 옮겨 쓴다 |
| DC-10 옛 시안 v7 | 계약에 넣음 | AR-04. 페이지 `static-evidence-viewer-contract.html` 은 DC-3(부모) 도 다시 맞춘다 — 이 묶음은 v7 다섯 곳과 그 카드의 수치만 고친다. `docs/api/research-log.md:179` 는 그날 v7 사본을 연 기록이라 그대로 둔다 |
| DC-11 스크립트 움직임 | 계약에 넣음 | ER-03. 목록의 `.animate(` 한 쪽은 Dart 코드 표본이라 할 일 없음 — notes 에 적는다(AR-10) |
| DC-12 밝은 테마 열한 쪽 | 계약에 넣음 | ER-04 · SK-04 · RE-01. 틀의 대비 미달 `--text3` 를 같이 고친다(갈린 곳 표). 검사기 단추 id 불일치(`#theme-btn` · `themeToggle`)는 검사 도구를 고치는 일이라 넘김 — notes 에 적는다 |
| DC-13 긴 쪽 흔들림 | 계약에 넣음 (원인 · 재현 notes) | AR-06. 쪽을 고칠 결함이 아니다(높이 불변 · 가는 선 번짐) |
| DC-14 담김 조건 | 계약에 넣음 | SK-02 |
| 320 에서 넘치는 44 쪽 고치기 | 계약에 넣음 | ER-01 · ER-02 · AR-07 · AR-11. 공통 파일로 풀 수 있는 것(줄바꿈 규칙 등)은 `site.css` 에 더하고, 쪽마다 다른 구조는 쪽에서 푼다. 넘침을 가리는 선언은 쓰지 않는다(`SKILL.md:30` Gotcha 11) · 폭 숫자를 아슬아슬하게 맞추지 않는다(Gotcha 12) |
| KD-2 감사 기준 행간 1.2~1.6 (`design-kit/skills/design-audit/references/audit-criteria.md:10`) | 뺌 — 다른 묶음 | 목록 「## kit-design-kit」 절 항목이라 design-kit 묶음 몫이다. 이 묶음은 킷 폴더에 `design-kit/evals/visuals.spec.js` 하나만 들이고(AR-08) 감사 기준 파일은 허용 집합 밖이다. DC-5 쪽(`SKILL.md` 의 1.2~1.6)은 SK-01 이 고치고, 두 값이 어긋난다는 사실을 notes 에 적어 design-kit 묶음에 넘긴다 |
| VS-18 오케스트레이터 F2 의 「standalone」 (`.claude/skills/kaizen-orchestrator/SKILL.md:620`) | 뺌 — 다른 묶음 | 목록 「## vs」 절 항목이다. 이 묶음 허용 집합 밖이라 notes 에만 적는다 |
| `design-kit/skills/design-audit/references/audit-criteria.md:97` 의 375 | 넘김 | 킷의 감사 판정값이다. 문서 사이트 검사와 다른 일이고 킷 폴더라 범위 밖 — notes 에 적는다 |
| 고치는 마크다운의 기존 편집기 경고(`SKILL.md` 9 · `static-evidence-viewer-contract.md` 11 · 설계 기록 70) | 넘김 (늘리지만 않음) | 사용자 결정 UD-7 「범위 밖 기존 경고를 전부 고친다」 는 VS-26 묶음 몫이다. 같은 파일을 두 묶음이 줄 단위로 크게 고치면 합칠 때 부딪힌다 — 이 묶음은 DG-02 로 늘지 않음만 잰다 |
| 다른 묶음과 같은 파일 | 주의 | `SKILL.md`(DC-1 묶음이 매핑 표를 고칠 수 있다) · `docs/process/kaizen-flow.html`(DC-15 가 카드 범위 칸을 고친다) · `static-evidence-viewer-contract.html`(DC-3). 바꿀 줄을 최소로 하고 표에 없는 절은 건드리지 않는다 |
| 쪽 본문 내용 · 킷 폴더(`design-kit/evals/visuals.spec.js` 말고) · `scripts/`(`check-docs-a11y.js` 말고) | 범위 밖 | AR-08 이 막는다 |

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 목록을 한 곳에만 둔 조건:

- 커버리지 해소: ER-04 — 검출기가 산문의 열한 쪽 경로와 출력 글 `follow=light/dark` 를 냈다. 열한 쪽은 산문에 도우미 `THEME_PAGES` 와 같은 글자로 있고 `m ER-04` 가 그 목록을 잰다(목록을 측정 절에 두 번 적지 않는다). `follow=light/dark` 는 대상이 아니라 기대 출력이다
- 커버리지 해소: AR-10 — 검출기가 `site.css` · `design-kit/evals` · `playwright.config.js` 를 냈다. 셋은 notes 가 담아야 할 토큰이고 `m AR-10` 의 토큰 목록에 같은 글자로 있다

교차 진단 반영(qa-evaluator, 봉인 전): Step 7 절 끝 식을 `#` · `##` 둘 다에서 끊게 고쳤다(평가자 권고 `(?=^## |\Z)` 는 이 파일의 Step 7 뒤가 `# References` 라 절 끝을 못 찾아 파일 끝까지 읽으므로 둘 다 받는 식으로 했다) · `gotcha10_same` 을 Gotcha 절로 좁혔다 · 틀 CSS 식에 중괄호 앞 빈칸을 허용했다 · SK-03 양성 대조를 더했다 · GAP 표 「42 쪽」 을 「44 쪽」 으로 바로잡았다 · KD-2 · VS-18 을 이 표에 올렸다. AR-06 의 `33fec27^` 은 보고용 값이라 그대로 둔다(얕은 복제본에서는 그 두 줄만 못 돈다). DG-05 의 로컬 CI 도구에 `run-kaizen-assertions.py` 단계가 없는 것(VS-24)은 notes 에 적는다.

교차 진단(qa-evaluator) 때 주의:

- ER-01 · ER-02 의 잘림 · 삐져나감 정의는 공통 전제 G 와 도우미 `pw.js` 의 `SCAN` 한 곳에 있다. 평가자는 `BAD` 줄 몇 개를 브라우저로 열어 실제로 글이 잘렸는지 눈으로 한 번 본다
- DC-6 은 뺐다 — 부모가 KBa-1 뒤에 처리한다

계약 파일의 편집기 경고(첫 줄 제목 없음 · 코드 표시 안 공백 등)는 계약 형식에서 나온다. 계약 · QA 리포트 · 개정 파일은 DG-02 대상에서 뺀다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 그 밖의 입력은 지우지 마라.
브라우저 도구는 작업 폴더 W 의 `node_modules`(추적 안 되는 폴더, `npm ci` 로 설치)를 `NODE_PATH` 로 빌려 쓰고, 푼 트리마다 그 폴더를 가리키는 `node_modules` 연결을 만든다(`npx playwright test` 가 설정 파일 옆에서 찾는다).

준비 단계 실측(봉인 전, 이 기계): `command -v node` → fnm 경로 · 종료 코드 0 (`v24.14.1`), `python3` · `git` · `shasum` 종료 코드 0, W 의 `node_modules/playwright-core` 판 `1.58.2`(`npm ci` 종료 코드 0), 브라우저 실행 파일은 `~/Library/Caches/ms-playwright/chromium_headless_shell-1208`. 브라우저가 없으면 `Executable doesn't exist` 로 멈춘다 — 복구: `cd W && node_modules/.bin/playwright-core install chromium-headless-shell` 뒤 다시 잰다. 브라우저가 없어 못 잰 조건은 FAIL 이 아니라 환경 실패로 보고한다.
`markdownlint-cli2@0.23.2` 임시 설치 종료 코드 0. `ci-local.sh` 지문 `git hash-object` → `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`.
Playwright 쓰임(`newContext` 의 `viewport` · `colorScheme` · `reducedMotion`, `addInitScript`, `addStyleTag`, `$$` · `boundingBox`, `reload`, `screenshot({ fullPage, animations: 'disabled' })`)은 Context7 `/microsoft/playwright/v1.58.2` 문서와 맞춰 봤다.
봉인 전 실측은 `BASE_REF=6378948` · `TIP=6378948` 로 잰 시작 판 값과, 임시 복제본(`W=<복제본>`)에 모의 좋은 판 · 나쁜 판을 커밋해 잰 값이다. ER-01 · ER-02 는 한 번에 5 분 남짓 걸린다(끝점과 시작 판을 모두 재므로 두 배).
도우미는 zsh 에서 부르지 마라 — zsh 는 따옴표 없는 변수를 낱말로 나누지 않아 쪽 목록이 한 덩어리가 된다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/dca-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/dca-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 봉인 커밋이 아직 없을 때: BASE_REF=<커밋> 을 준다. 시작 판을 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>
# === 측정 도우미 시작 (after-0926-docs-fixes) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라(따옴표 없는 변수를 낱말로 나누지 않아 쪽 목록이 한 덩어리가 된다).
# 끝점 TIP = 가지 끝. 시작점 BASE = 이 계약을 처음 담은 커밋(봉인 커밋)의 부모 — 해시를 박지 않고 git 기록에서 푼다.
# 봉인 커밋이 아직 없으면 BASE_REF=<커밋> 을 준다. 시작 판 자체를 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dca}
BR=${BR:-chore/ak2-dca}
SLUG=after-0926-docs-fixes
CF_REL=.harness/sprint-contract-$SLUG.md
NOTES=.harness/.meta/after-kaizen-0926b/dca-notes.md
TIP=$(git -C "$W" rev-parse --verify -q "$BR^{commit}") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
if [ -n "${BASE_REF:-}" ]; then
  BASE=$(git -C "$W" rev-parse --verify -q "$BASE_REF^{commit}") || { echo "UNRESOLVED BASE_REF"; return 2 2>/dev/null || exit 2; }
else
  SEAL=$(git -C "$W" log --diff-filter=A --format=%H "$TIP" -- "$CF_REL" | tail -1)
  [ -n "$SEAL" ] || { echo "UNRESOLVED SEAL (봉인 커밋 없음)"; return 2 2>/dev/null || exit 2; }
  BASE=$(git -C "$W" rev-parse --verify -q "$SEAL^") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
fi
T=$(mktemp -d "${TMPDIR:-/tmp}/dca.XXXXXX")
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
TOOL_BLOB=01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860
# DC-12 — 어두운 테마 전용이던 열한 쪽 (c3b 묶음이 손본 쪽)
THEME_PAGES='docs/backend-kit/api-lifecycle.html
docs/design-kit/design-concept.html
docs/design-kit/design-mockup.html
docs/design-kit/typography-scale.html
docs/flutter-toolkit/theming.html
docs/onboarding-kit/setup-guide.html
docs/process/kaizen-flow.html
docs/rust-kit/grpc-tonic.html
docs/rust-kit/observability.html
docs/rust-kit/ownership-borrowing.html
docs/rust-kit/project-structure.html'
# DC-11 — 스크립트로 부드럽게 움직이는 쪽: 맨 위로 단추 넷 · 시뮬레이터 하나 (움직임 줄이기가 아닐 때는 그대로 부드럽게 움직여야 한다)
SMOOTH_PAGES='docs/design-kit/design-template.html
docs/design-kit/grid-alignment.html
docs/design-kit/ratio-proportion.html
docs/design-kit/visual-hierarchy.html
docs/process/kaizen-flow.html'
# DC-11 — 손대지 않아도 스스로 움직이는 표본 쪽 (움직임 줄이기가 아닐 때는 그대로 움직여야 한다)
AUTO_PAGES='docs/design-kit/animation.html
docs/design-kit/microinteraction.html'
KITS=$(cd "$EB" && find . -mindepth 3 -maxdepth 3 -path './*/.claude-plugin/plugin.json' | cut -d/ -f2 | LC_ALL=C sort)
PAGES=$(cd "$EB" && find docs -name '*.html' | LC_ALL=C sort)
CAP_RE='^[a-z0-9-]+__[a-z0-9-]+-(320|375|1280)-(dark|light)\.png$'

cat > "$T/pg.py" <<'PY'
import sys, re, os, subprocess, importlib.util, html as H
from html.parser import HTMLParser
rd = lambda p: open(p, encoding='utf-8').read()
def ex(p):
    return os.path.exists(p)
def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def cr(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x + 0.05) / (y + 0.05)
def var(block, k):
    m = re.search(r'--' + k + r'\s*:\s*(#[0-9A-Fa-f]{6})', block); return m.group(1) if m else None
cmd = sys.argv[1]
SK = '.claude/skills/docs-site/SKILL.md'
if cmd == 'skill':   # skill <옛 트리> <새 트리> — docs-site SKILL.md 의 안내 글 (DC-5 · DC-14 · DC-2)
    b, t = sys.argv[2:4]; bs, ts = rd(os.path.join(b, SK)), rd(os.path.join(t, SK))
    fm = lambda x: x.split('\n---', 1)[0]
    fmk = lambda x: [l for l in fm(x).splitlines() if not l.startswith('  .md ')]   # 설명 둘째 줄(:5) 말고는 머리 설정이 그대로
    L = ts.splitlines()
    typo = [l for l in L if l.lstrip().startswith('- **Typography**')]; mot = [l for l in L if l.lstrip().startswith('- **Motion**')]
    s7 = re.search(r'(?ms)^## Step 7[^\n]*\n(.*?)(?=^#{1,2} |\Z)', ts); s7 = s7.group(1) if s7 else ''
    s7b = re.search(r'(?ms)^## Step 7[^\n]*\n(.*?)(?=^#{1,2} |\Z)', bs); s7b = s7b.group(1) if s7b else ''
    num = lambda s: len(re.findall(r'(?m)^\d+\. ', s))
    gsec = lambda x: (lambda m: m.group(1) if m else '')(re.search(r'(?ms)^# Gotchas[^\n]*\n(.*?)(?=^#{1,2} |\Z)', x))   # Gotcha 절 안에서만
    g10 = lambda x: [l for l in gsec(x).splitlines() if l.startswith('10. ')]
    w320 = sum(1 for l in L if '320/375/768/1280px' in l)
    print(f"fm_same={int(fmk(bs) == fmk(ts))} fm_name={'docs-site' if re.search(r'(?m)^name: docs-site$', fm(ts)) else ''} standalone={ts.count('standalone')} lh_old={ts.count('1.2~1.6')} "
          f"typo_ok={int(len(typo) == 1 and 'site.css' in typo[0] and '1.7' in typo[0])} "
          f"motion_ok={int(len(mot) == 1 and 'site.css' in mot[0] and 'matchMedia' in mot[0])} "
          f"s7_items={num(s7b)}->{num(s7)} s7_old={s7.count('옛 페이지')} s7_code={s7.count('코드 표시')} s7_ratio={s7.count('낱말 비율')} s7_lost={s7.count('빠진 수 0')} s7_ratio_rule={s7.count('낱말 비율이 옛 페이지 이상')} "
          f"w320_line={w320} gotcha10_same={int(g10(bs) == g10(ts))}")
elif cmd == 'tpl':   # tpl <새 트리> — 새 쪽의 틀과 토큰 문서의 --text3 (DC-12 공통 틀)
    t = sys.argv[2]; tp = rd(os.path.join(t, '.claude/skills/docs-site/references/page-template.html'))
    root = re.search(r'(?s):root\s*\{(.*?)\}', tp).group(1); lt = re.search(r'(?s)\[data-theme="light"\]\s*\{(.*?)\}', tp)
    lt = lt.group(1) if lt else ''
    d3 = var(root, 'text3'); l3 = var(lt, 'text3')
    lr = min(cr(l3, var(lt, k) or var(root, k)) for k in ('bg', 'bg2', 'surface', 'surface2')) if l3 else 0
    dr = min(cr(d3, var(root, k)) for k in ('bg', 'bg2', 'surface', 'surface2')) if d3 else 0
    tk = rd(os.path.join(t, '.claude/skills/docs-site/references/css-tokens.md'))
    blk = re.search(r'(?s)```css\n(.*?)```', tk).group(1)
    print(f'tpl_dark_text3={d3} tpl_dark_min={dr:.2f} tpl_light_text3={l3} tpl_light_min={lr:.2f} tokens_block_text3={var(blk, "text3")}')
elif cmd == 'line1':  # line1 <옛 트리> <새 트리> <파일> <옛 글> <새 글> — 한 줄만 바뀌었고 그 줄이 옛 줄에서 옛 글을 새 글로 바꾼 것과 같은지
    b, t, f, old, new = sys.argv[2:7]; B, N = rd(os.path.join(b, f)).splitlines(), rd(os.path.join(t, f)).splitlines()
    import difflib
    ch = [x for x in difflib.unified_diff(B, N, lineterm='', n=0) if x[:1] in '+-' and not x.startswith(('+++', '---'))]
    minus = [x[1:] for x in ch if x[0] == '-']; plus = [x[1:] for x in ch if x[0] == '+']
    ok = len(minus) == 1 and len(plus) == 1 and old in minus[0] and minus[0].replace(old, new, 1) == plus[0]
    nn = rd(os.path.join(t, f)).count(new) if new else '-'
    print(f'{os.path.basename(f)}: changed={len(minus)}/{len(plus)} old_left={rd(os.path.join(t, f)).count(old)} new_n={nn} exact={int(ok)}')
elif cmd == 'dc10':  # dc10 <새 트리> — 옛 시안 v7 기재와 v8 실측 수치
    t = sys.argv[2]
    md = rd(os.path.join(t, 'docs/api/verification/static-evidence-viewer-contract.md')); sp = rd(os.path.join(t, 'docs/superpowers/specs/2026-09-02-api-kit-design.md'))
    pg = rd(os.path.join(t, 'docs/api-kit/static-evidence-viewer-contract.html')); rl = rd(os.path.join(t, 'docs/api/research-log.md'))
    row85 = [l for l in md.splitlines() if l.startswith('| 누르는 자리 최소 크기 |')]
    print(f"md_v7={md.count('api-ui-v7')} md_v8={md.count('api-ui-v8.html')} md_row={int(len(row85) == 1 and '57 개 중 24 미만 0 · 44 미만 40' in row85[0] and '2026-09-26' in row85[0])} "
          f"spec_v7={sp.count('api-ui-v7.html')} spec_v8={sp.count('api-ui-v8.html')} spec_hist={sp.count('사용자 확정 2026-09-03')} "
          f"page_v7={pg.count('api-ui-v7')} page_v8={pg.count('api-ui-v8.html')} "
          f"page_old={sum(pg.count(x) for x in ('56 개', '/ 56', '56 에서', '미만 39', '39 /', '39 개', '39 를', '(2026-09-25)'))} "
          f"page_57={pg.count('57 개')} page_of57={pg.count('/ 57')} page_u40={pg.count('미만 40')} page_40of57={pg.count('40 / 57')} page_17of57={pg.count('17 / 57')} page_0of57={len(re.findall(r'(?<![0-9])0 / 57', pg))} page_0926={pg.count('(2026-09-26)')} "
          f"rlog_v7={rl.count('api-ui-v7.html')}")
elif cmd == 'maplist':  # maplist <트리> — 드리프트 도구 매핑으로 짝 원본이 없는 등록 페이지 · 없는 페이지를 가리키는 원본
    t = os.path.abspath(sys.argv[2]); spec = importlib.util.spec_from_file_location('dd', os.path.join(t, 'scripts/detect-docs-drift.py'))
    dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
    dd.REPO_ROOT = __import__('pathlib').Path(t); dd.INDEX_HTML = dd.REPO_ROOT / 'docs/index.html'
    files = sorted(os.path.relpath(os.path.join(d, f), t) for d, ds, fs in os.walk(t) if '/node_modules' not in d and '/.git' not in d for f in fs)
    reg = dd.load_registry(); tg = set(); miss = []
    for s in files:
        c = dd.SOURCE_OVERRIDES.get(s) or ([dd.map_source_to_html(s)] if dd.map_source_to_html(s) else [])
        for x in c:
            tt, r_, e_ = dd.resolve_target(x, reg); tg.add(tt)
            if not e_: miss.append(s)
    for p in sorted(p for p in reg if p not in tg): print('ORPHAN', p)
    for s in sorted(set(miss)): print('MISSING', s)
elif cmd == 'dc9':   # dc9 <목록 파일> <notes> — DC-9 절 표에 목록의 경로마다 결정 칸이 찬 행이 있는지
    items = [l.split(' ', 1) for l in open(sys.argv[2]).read().splitlines() if l.strip()]
    n = rd(sys.argv[3]) if ex(sys.argv[3]) else ''
    sec = re.search(r'(?ms)^## DC-9[^\n]*\n(.*?)(?=^## |\Z)', n); sec = sec.group(1) if sec else ''
    rows = [l for l in sec.splitlines() if l.startswith('|') and not re.match(r'^\|\s*-', l)]
    OK = ('원본:', '원본 없음', '새 페이지', '짝:', '페이지 없음이 맞음')
    def dec(path):
        for r in rows:
            c = [x.strip() for x in r.strip('|').split('|')]
            if len(c) >= 3 and f'`{path}`' in c[0]:
                return any(c[1].startswith(o) for o in OK) and len(re.sub(r'[^가-힣]', '', c[2])) >= 10
        return False
    o = [p for k, p in items if k == 'ORPHAN']; mi = [p for k, p in items if k == 'MISSING']
    od = sum(dec(p) for p in o); md_ = sum(dec(p) for p in mi)
    howto = int(any('`docs/howto/design-brief.md`' in r and '`docs/howto-kit/overview.html`' in r for r in rows))
    proc = int(any('`process (공유)`' in r and '`.claude/skills/kaizen-orchestrator/SKILL.md`' in r for r in rows))
    print(f'section={int(bool(sec))} orphan={od}/{len(o)} missing={md_}/{len(mi)} howto_pair={howto} process_row={proc}')
elif cmd == 'tokens':  # tokens <notes> <토큰...> — 토큰마다 그 토큰이 든 줄 가운데 한글 15 자 이상인 줄 수
    n = rd(sys.argv[2]) if ex(sys.argv[2]) else None
    if n is None: print('notes=absent'); sys.exit(0)
    L = n.splitlines(); out = []
    for k in sys.argv[3:]:
        out.append(f'{k}={sum(1 for l in L if k in l and len(re.sub(r"[^가-힣]", "", l)) >= 15)}')
    print(' '.join(out))
elif cmd == 'hide':  # hide <옛 트리> <새 트리> <쪽 목록> — 쪽 · 공통 파일에 새로 들어간 넘침 가리기 선언
    b, t = sys.argv[2:4]; P = open(sys.argv[4]).read().split() + ['docs/assets/site.css']
    import difflib
    pat = re.compile(r'overflow(-x|-y)?\s*:\s*(hidden|clip)|text-overflow\s*:\s*ellipsis|display\s*:\s*none|visibility\s*:\s*hidden')
    hits = []
    for p in P:
        B = rd(os.path.join(b, p)).splitlines() if ex(os.path.join(b, p)) else []
        N = rd(os.path.join(t, p)).splitlines() if ex(os.path.join(t, p)) else []
        bc = sum(len(pat.findall(l)) for l in B); nc = sum(len(pat.findall(l)) for l in N)
        if nc > bc: hits.append(f'{p}:{bc}->{nc}')
    print(f'hide_added={len(hits)} {hits[:5]}')
elif cmd == 'wide':  # wide <옛 w 출력> <새 w 출력> — 1280 에서의 잘림 · 삐져나감이 쪽마다 늘지 않았는지
    g = lambda f: {m.group(1): int(m.group(2)) for m in re.finditer(r'^\S+ (\S+) .*? wide=(\d+)', open(f).read(), re.M)}
    B, N = g(sys.argv[2]), g(sys.argv[3]); worse = [k for k in N if N[k] > B.get(k, 0)]
    print(f'wide_worse={len(worse)} {worse[:5]}')
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
elif cmd == 'commits':  # commits <W> <BASE> <TIP> <킷 목록> — 킷 둘 이상을 한 커밋에 · .harness 와 섞인 커밋
    w, base, tip, kits = sys.argv[2], sys.argv[3], sys.argv[4], set(open(sys.argv[5]).read().split())
    g = lambda *a: subprocess.run(['git', '-C', w, *a], capture_output=True, text=True).stdout
    multi = mixed = impl = 0
    for c in g('rev-list', '--no-merges', f'{base}..{tip}').split():
        fs = [f for f in g('show', '--name-only', '--format=', c).splitlines() if f.strip()]
        h = [f for f in fs if f.startswith('.harness/')]; o = [f for f in fs if not f.startswith('.harness/')]
        if h and o: mixed += 1
        if o: impl += 1
        if len({f.split('/')[0] for f in o if f.split('/')[0] in kits}) > 1: multi += 1
    print(f'impl_commits={impl} multi_kit={multi} mixed={mixed}')
elif cmd == 'bare':  # bare <파일> — 줄 앞 공백을 벗긴 뒤 백틱 셋으로 시작하는 줄을 열고 닫기로 번갈아 세어 언어 없는 여는 울타리 수
    p = sys.argv[2]
    if not ex(p): print('absent'); sys.exit(0)
    n = 0; op = False
    for l in rd(p).splitlines():
        s = l.lstrip()
        if s.startswith('```'):
            if not op:
                op = True
                if s.rstrip() == '```': n += 1
            else: op = False
    print(n)
PY

cat > "$T/pw.js" <<'JS'
// w <트리> <폭> <ls:0|1> <쪽...>  — 1280 과 <폭> 에서 글 조각을 모두 훑어 <폭> 에서만 생기는 잘림 · 삐져나감과 문서 가로 넘침
// motion <트리> <reduce|no-preference> <쪽...> — 손대지 않은 2 초 동안 style · class 가 바뀌는 요소 수, 스크롤 단추 · 시뮬레이터를 누른 뒤 부드러운 스크롤 · animate() 호출 수
// theme <트리> <쪽...> — 테마 단추 · 저장 키 dk-theme · 브라우저 색 설정 따라가기
// pix <트리> <쪽> <횟수> — 같은 판을 여러 번 전체 캡처해 첫 판과 다른 픽셀 수
const path = require('path'); const { chromium } = require('playwright-core');
const SCAN = () => {
  const out = { clip: [], esc: [] }; let i = -1;
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  const INLINE = /^(inline|inline-block|contents)$/;
  while ((n = tw.nextNode())) {
    i++;
    if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (!el || el.closest('script,style,noscript,template,[aria-hidden="true"]')) continue;
    const cs0 = getComputedStyle(el); if (cs0.display === 'none' || cs0.visibility === 'hidden') continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const rs = [...r.getClientRects()].filter(x => x.width > 0 && x.height > 0); if (!rs.length) continue;
    const R = Math.max(...rs.map(x => x.right)), L = Math.min(...rs.map(x => x.left));
    if (R <= 0 || L >= document.documentElement.clientWidth) continue; // 화면 밖으로 밀어 둔 서랍 · 메뉴는 숨긴 UI 다
    const tag = `${i}:${el.tagName.toLowerCase()}.${String(el.className || '').split(' ')[0]}:${n.textContent.trim().slice(0, 24)}`;
    let a = el, box = false;
    while (a && a !== document.documentElement) {
      const cs = getComputedStyle(a), ar = a.getBoundingClientRect(), ox = cs.overflowX;
      if (ox === 'auto' || ox === 'scroll') break; // 스크롤로 닿는다
      if ((ox === 'hidden' || ox === 'clip') && (R > ar.right + 2 || L < ar.left - 2)) { out.clip.push(tag); break; }
      if (!box && !INLINE.test(cs.display) && ((parseFloat(cs.borderRightWidth) > 0 && cs.borderRightStyle !== 'none') || !/rgba\(0, 0, 0, 0\)|transparent/.test(cs.backgroundColor))) {
        box = true; if (R > ar.right + 2 || L < ar.left - 2) out.esc.push(tag);
      }
      a = a.parentElement;
    }
  }
  return out;
};
const OVER = () => document.documentElement.scrollWidth - document.documentElement.clientWidth;
(async () => {
  const [mode, tree0, ...rest] = process.argv.slice(2); const tree = path.resolve(tree0);
  const b = await chromium.launch();
  if (mode === 'w') {
    const [w, ls, ...P] = rest; const sum = { doc: 0, clip: 0, esc: 0 };
    for (const rel of P) {
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark', reducedMotion: 'reduce' });
      const p = await ctx.newPage(); await p.goto('file://' + path.join(tree, rel), { waitUntil: 'load' });
      if (ls === '1') await p.addStyleTag({ content: '*{letter-spacing:0.06em !important}' });
      await p.waitForTimeout(100); const wide = await p.evaluate(SCAN);
      await p.setViewportSize({ width: +w, height: 900 }); await p.waitForTimeout(150);
      const doc = await p.evaluate(OVER); const nar = await p.evaluate(SCAN);
      const clip = nar.clip.filter(x => !wide.clip.includes(x)), esc = nar.esc.filter(x => !wide.esc.includes(x) && !wide.clip.includes(x));
      const ok = doc <= 2 && !clip.length && !esc.length;
      sum.doc += doc <= 2; sum.clip += !clip.length; sum.esc += !esc.length;
      console.log(`${ok ? 'OK ' : 'BAD'} ${rel} doc=${doc} clip=${clip.length} esc=${esc.length} wide=${wide.clip.length + wide.esc.length}${ok ? '' : ' ' + JSON.stringify([...clip.slice(0, 3), ...esc.slice(0, 3)])}`);
      await ctx.close();
    }
    console.log(`w=${rest[0]} ls=${rest[1]} pages=${P.length} doc_ok=${sum.doc} clip_ok=${sum.clip} esc_ok=${sum.esc}`);
  } else if (mode === 'motion') {
    const [pref, ...P] = rest; let clean = 0;
    for (const rel of P) {
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark', reducedMotion: pref });
      await ctx.addInitScript(() => {
        window.__smooth = 0; window.__anim = 0;
        const wrap = (o, k) => { const f = o[k]; o[k] = function (a, ...r) { if (a && typeof a === 'object' && a.behavior === 'smooth') window.__smooth++; return f.call(this, a, ...r); }; };
        wrap(window, 'scrollTo'); wrap(window, 'scrollBy'); wrap(Element.prototype, 'scrollIntoView'); wrap(Element.prototype, 'scrollTo');
        const an = Element.prototype.animate; Element.prototype.animate = function (k, o) { const d = typeof o === 'number' ? o : (o && o.duration) || 0; if (d > 0.01) window.__anim++; return an.call(this, k, o); };
      });
      const p = await ctx.newPage(); await p.goto('file://' + path.join(tree, rel), { waitUntil: 'load' }); await p.waitForTimeout(500);
      const muts = await p.evaluate(() => new Promise(res => { const s = new Set();
        const mo = new MutationObserver(ms => ms.forEach(m => s.add(m.target))); mo.observe(document.body, { attributes: true, attributeFilter: ['style', 'class'], subtree: true, childList: true });
        setTimeout(() => { mo.disconnect(); res(s.size); }, 2000); }));
      const clicked = await p.evaluate(() => { let n = 0; for (const el of document.querySelectorAll('[onclick]')) if (/scroll/.test(el.getAttribute('onclick'))) { el.click(); n++; } return n; });
      const sim = await p.$('#simStart'); if (sim) { await sim.click(); await p.waitForTimeout(2500); }
      await p.waitForTimeout(200);
      const sm = await p.evaluate(() => window.__smooth), an = await p.evaluate(() => window.__anim);
      const ok = muts === 0 && sm === 0 && an === 0; clean += ok;
      console.log(`${ok ? 'OK ' : 'BAD'} ${rel} automut=${muts} smooth=${sm} anim=${an} clicked=${clicked}${sim ? '+sim' : ''}`);
      await ctx.close();
    }
    console.log(`pref=${pref} pages=${P.length} motion_ok=${clean}`);
  } else if (mode === 'theme') {
    const P = rest; let ok = 0;
    for (const rel of P) {
      const url = 'file://' + path.join(tree, rel); const r = {};
      for (const cs of ['light', 'dark']) {  // 저장값이 없으면 브라우저 색 설정을 따른다
        const ctx = await b.newContext({ viewport: { width: 375, height: 812 }, colorScheme: cs }); const p = await ctx.newPage();
        await p.goto(url, { waitUntil: 'load' }); r[cs] = await p.evaluate(() => document.documentElement.getAttribute('data-theme')); await ctx.close();
      }
      const ctx = await b.newContext({ viewport: { width: 375, height: 812 }, colorScheme: 'light' }); const p = await ctx.newPage();
      await p.goto(url, { waitUntil: 'load' });
      const btns = await p.$$('button[aria-label*="테마"]'); r.btn = btns.length;
      if (btns.length === 1) {
        const bb = await btns[0].boundingBox(); r.size = `${Math.round(bb.width)}x${Math.round(bb.height)}`; r.big = bb.width >= 44 && bb.height >= 44;
        await btns[0].click(); r.after = await p.evaluate(() => document.documentElement.getAttribute('data-theme'));
        r.key = await p.evaluate(() => localStorage.getItem('dk-theme'));
        await p.reload({ waitUntil: 'load' }); r.kept = await p.evaluate(() => document.documentElement.getAttribute('data-theme'));
        r.keys = await p.evaluate(() => Object.keys(localStorage).sort().join(','));
      }
      await ctx.close();
      const good = r.light === 'light' && r.dark === 'dark' && r.btn === 1 && r.big && r.after === 'dark' && r.key === 'dark' && r.kept === 'dark' && r.keys === 'dk-theme';
      ok += good;
      console.log(`${good ? 'OK ' : 'BAD'} ${rel} follow=${r.light}/${r.dark} btn=${r.btn} size=${r.size || '-'} toggled=${r.after || '-'} key=${r.key || '-'} kept=${r.kept || '-'} keys=${r.keys || '-'}`);
    }
    console.log(`pages=${P.length} theme_ok=${ok}`);
  } else if (mode === 'pix' || mode === 'pixalt') {
    // pixalt <트리 A> <트리 B> <쪽> <횟수> — A 와 B 를 번갈아 캡처하고 A 의 캡처끼리만 비교한다 (DC-13 재현)
    const alt = mode === 'pixalt'; const treeB = alt ? path.resolve(rest[0]) : null;
    const [rel, n] = alt ? rest.slice(1) : rest; const shots = [];
    for (let i = 0; i < +n * (alt ? 2 : 1); i++) {
      const tr = alt && i % 2 ? treeB : tree;
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark', reducedMotion: 'no-preference' });
      const p = await ctx.newPage(); await p.goto('file://' + path.join(tr, rel), { waitUntil: 'load' }); await p.waitForTimeout(300);
      if (alt && i % 2) { await ctx.close(); continue; }
      shots.push(await p.screenshot({ fullPage: true, animations: 'disabled' })); await ctx.close();
    }
    const cmp = await (await b.newContext()).newPage(); const out = [];
    for (let i = 1; i < shots.length; i++) {
      out.push(await cmp.evaluate(async ([u, v]) => {
        const load = s => new Promise(res => { const im = new Image(); im.onload = () => res(im); im.src = s; });
        const [a, c] = [await load(u), await load(v)];
        if (a.width !== c.width || a.height !== c.height) return -1;
        const px = im => { const cv = document.createElement('canvas'); cv.width = im.width; cv.height = im.height; const g = cv.getContext('2d'); g.drawImage(im, 0, 0); return g.getImageData(0, 0, im.width, im.height).data; };
        const [d, e] = [px(a), px(c)]; let k = 0;
        for (let q = 0; q < d.length; q += 4) if (d[q] !== e[q] || d[q + 1] !== e[q + 1] || d[q + 2] !== e[q + 2]) k++;
        return k;
      }, ['data:image/png;base64,' + shots[0].toString('base64'), 'data:image/png;base64,' + shots[i].toString('base64')]));
    }
    console.log(`${mode} ${rel} runs=${n} diffs=${out.join(',')} zero=${out.filter(x => x === 0).length}/${out.length}`);
  }
  await b.close();
})();
JS

m() {
  case "$1" in
    SK-01|SK-02|SK-03|AP-04) python3 "$T/pg.py" skill "$EB" "$E" ;;
    SK-04) python3 "$T/pg.py" tpl "$E" ;;
    ER-01) node "$T/pw.js" w "$E" 320 0 $PAGES > "$T/w0.txt"; grep -v '^OK' "$T/w0.txt" | tail -40
           [ "$E" = "$EB" ] || { node "$T/pw.js" w "$EB" 320 0 $PAGES > "$T/w0b.txt"; python3 "$T/pg.py" wide "$T/w0b.txt" "$T/w0.txt"; } ;;
    ER-02) node "$T/pw.js" w "$E" 320 1 $PAGES > "$T/w1.txt"; grep -v '^OK' "$T/w1.txt" | tail -50
           [ "$E" = "$EB" ] || { node "$T/pw.js" w "$EB" 320 1 $PAGES > "$T/w1b.txt"; python3 "$T/pg.py" wide "$T/w1b.txt" "$T/w1.txt"; }
           node "$T/pw.js" w "$E" 375 1 $PAGES | tail -1 ;;
    ER-03) node "$T/pw.js" motion "$E" reduce $PAGES | grep -v '^OK'
           node "$T/pw.js" motion "$E" no-preference $SMOOTH_PAGES $AUTO_PAGES ;;
    ER-04) (cd "$E" && node scripts/check-docs-a11y.js $THEME_PAGES) | grep -E 'theme=|PASS$'; node "$T/pw.js" theme "$E" $THEME_PAGES ;;
    AR-01) echo "a11y_widths=$(grep -cE 'for \(const w of \[320, 375, 768, 1280\]\)' "$E/scripts/check-docs-a11y.js") a11y_ok320=$(grep -cE 'of\[320\] <= 2 && of\[375\] <= 2' "$E/scripts/check-docs-a11y.js") a11y_print=$(grep -cF 'of=${of[320]}/${of[375]}/${of[768]}/${of[1280]}' "$E/scripts/check-docs-a11y.js") a11y_head=$(grep -cF '가로 오버플로(320/375/768/1280px)' "$E/scripts/check-docs-a11y.js")"
           echo "vis_tests320=$(grep -cF "test('no horizontal overflow at 320px'" "$E/design-kit/evals/visuals.spec.js") vis_call320=$(grep -cF 'expectNoOverflow(page, url, 320)' "$E/design-kit/evals/visuals.spec.js") vis_describe=$(grep -cE "^test\.describe\('" "$E/design-kit/evals/visuals.spec.js")" ;;
    AR-02) python3 "$T/pg.py" line1 "$EB" "$E" docs/tone-kit/dart-flutter-idioms.html '(표 칸에 옮기면 대안 기호가 깨진다)' '' ;;
    AR-03) python3 "$T/pg.py" line1 "$EB" "$E" docs/api-kit/multi-sample-pagination-variance.html '정본은' '기준 기록은' ;;
    AR-04) python3 "$T/pg.py" dc10 "$E" ;;
    AR-05) python3 "$T/pg.py" maplist "$EB" > "$T/maplist.txt"; echo "list_orphan=$(grep -c '^ORPHAN' "$T/maplist.txt") list_missing=$(grep -c '^MISSING' "$T/maplist.txt")"
           python3 "$T/pg.py" dc9 "$T/maplist.txt" "$E/$NOTES" ;;
    AR-06) node "$T/pw.js" pix "$E" docs/harness/contract-schema.html 6
           [ -f "$T/old/docs/harness/contract-schema.html" ] || { mkdir -p "$T/old" && git -C "$W" archive 33fec27^ docs | tar -x -C "$T/old"; }
           node "$T/pw.js" pixalt "$E" "$T/old" docs/harness/contract-schema.html 6
           python3 "$T/pg.py" tokens "$E/$NOTES" 'contract-schema.html' '29743' 'code-block' '1118' '소수' 'pixalt' ;;
    AR-07) printf '%s\n' $PAGES > "$T/pages.txt"; python3 "$T/pg.py" hide "$EB" "$E" "$T/pages.txt"
           echo "site_lh=$(grep -c '^body{line-height:1.7}$' "$E/docs/assets/site.css") site_rm=$(grep -c '^@media (prefers-reduced-motion: reduce){$' "$E/docs/assets/site.css")" ;;
    AR-08) CH=$(git -C "$W" diff --name-only "$BASE" "$R" -- . ':(exclude).harness'); printf '%s\n' "$CH" > "$T/changed.txt"
           python3 - "$T/changed.txt" <<'PY2'
import sys, re
ch = [l for l in open(sys.argv[1]).read().splitlines() if l.strip()]
FIXED = ['.claude/skills/docs-site/SKILL.md', '.claude/skills/docs-site/references/css-tokens.md', '.claude/skills/docs-site/references/page-template.html',
         'scripts/check-docs-a11y.js', 'design-kit/evals/visuals.spec.js', 'docs/api/verification/static-evidence-viewer-contract.md',
         'docs/superpowers/specs/2026-09-02-api-kit-design.md', 'docs/tone-kit/dart-flutter-idioms.html', 'docs/api-kit/multi-sample-pagination-variance.html',
         'docs/api-kit/static-evidence-viewer-contract.html']
ok = lambda f: f in FIXED or f == 'docs/assets/site.css' or (re.match(r'^docs/.+\.html$', f) is not None)
extra = [f for f in ch if not ok(f)]; missing = [f for f in FIXED if f not in ch]
print(f'changed={len(ch)} extra={len(extra)} missing={len(missing)} png={sum(f.endswith(".png") for f in ch)} {extra[:5]} {missing[:5]}')
PY2
           git -C "$W" diff --name-status "$BASE" "$R" -- docs ':(exclude).harness' | awk '$1 != "M" {n++} END {print "docs_not_modify=" n+0}'
           sb=0; for c in $(cd "$E" && find .harness -maxdepth 1 -name 'sprint-contract*.md' | LC_ALL=C sort); do
             rec=$(awk '/^---$/{f++; next} f==1 && /^conditions_digest:/{sub(/^conditions_digest:[ ]*sha256:/,""); print; exit}' "$E/$c")
             [ -n "$rec" ] || continue
             act=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$E/$c" | sed -E 's/^- \[[ x]\]/- [ ]/' | shasum -a 256 | cut -c1-16)
             [ "$rec" = "$act" ] || { sb=$((sb+1)); echo "SEAL_BROKEN $c"; }
           done; echo "seal_broken=$sb" ;;
    AR-09) printf '%s\n' $KITS > "$T/kits.txt"; python3 "$T/pg.py" commits "$W" "$BASE" "$R" "$T/kits.txt" ;;
    AR-10) echo "committed=$(git -C "$W" cat-file -e "$R:$NOTES" 2>/dev/null && echo 1 || echo 0)"
           python3 "$T/pg.py" tokens "$E/$NOTES" 'DC-2' 'site.css' 'tone-guide' 'DC-6' 'KBa-1' '.animate(' 'theme-btn' 'audit-criteria' '--text3' 'design-kit/evals' 'playwright.config.js' 'DC-10' ;;
    AR-11) CAP=$(sed -n 's/^캡처 폴더: `\(.*\)`$/\1/p' "$E/$NOTES" 2>/dev/null | head -1); echo "cap_dir=${CAP:-absent}"
           [ -n "$CAP" ] && [ -d "$CAP" ] || { echo "cap_ok=0"; return 0; }
           need=0; have=0; for p in $(git -C "$W" diff --name-only "$BASE" "$R" -- 'docs/*.html' 'docs/**/*.html'); do
             base=$(echo "$p" | sed -E 's#^docs/##; s#\.html$##; s#/#__#; s#/#-#g')
             th=dark; grep -qF '[data-theme="light"]' "$E/$p" && th='dark light'
             for w in 320 375 1280; do for t in $th; do need=$((need+1)); [ -s "$CAP/$base-$w-$t.png" ] && have=$((have+1)); done; done
           done; echo "cap_need=$need cap_have=$have cap_badname=$(find "$CAP" -maxdepth 1 -name '*.png' | xargs -n1 basename 2>/dev/null | grep -cvE "$CAP_RE")" ;;
    RE-01) git -C "$W" diff -U0 "$BASE" "$R" -- docs | grep -E '^\+' | grep -oE "localStorage\.(get|set)Item\(['\"][^'\"]+['\"]" | sed -E "s/.*\(['\"]//; s/['\"]$//" | sort | uniq -c | awk '{printf "key[%s]=%s ", $2, $1} END {print ""}' ;;
    RE-02) echo "new_files_scripts=$(git -C "$W" diff --name-status "$BASE" "$R" -- scripts design-kit/evals | awk '$1 == "A"' | wc -l | tr -d ' ') new_checker=$(git -C "$W" diff --name-status "$BASE" "$R" -- . ':(exclude).harness' | awk '$1 == "A" && $2 ~ /\.(js|py|sh)$/' | wc -l | tr -d ' ')" ;;
    AP-03) for f in "$NOTES" .claude/skills/docs-site/SKILL.md .claude/skills/docs-site/references/css-tokens.md; do printf '%s=%s->%s ' "$(basename "$f")" "$(python3 "$T/pg.py" bare "$EB/$f")" "$(python3 "$T/pg.py" bare "$E/$f")"; done; echo ;;
    DG-01|DG-03|SC-00) echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$R" -- scripts/release.sh .claude-plugin | wc -l | tr -d ' ')" ;;
    DG-02) tw=0; for p in $(git -C "$W" diff --name-only "$BASE" "$R" -- 'docs/*.html' 'docs/**/*.html' .claude/skills/docs-site/references/page-template.html); do
             a=$(python3 "$T/pg.py" html "$E/$p"); bb=0; [ -f "$EB/$p" ] && bb=$(python3 "$T/pg.py" html "$EB/$p"); [ "$a" -gt "$bb" ] && { tw=$((tw+1)); echo "TAG_WORSE $p $bb->$a"; }; done
           (cd "$T" && npm i --silent --no-save markdownlint-cli2@0.23.2 >/dev/null 2>&1) || { echo "md=ENV_FAIL"; }
           printf '{"config":{"MD013":false}}\n' > "$T/.markdownlint-cli2.jsonc"
           mdc() { [ -f "$1" ] || { echo absent; return; }; (cd "$T" && node_modules/.bin/markdownlint-cli2 "$1" 2>&1 | grep -cE ':[0-9]+(:[0-9]+)? (error|warning)? ?MD[0-9]+' ); }
           echo "tag_worse=$tw md_notes=$(mdc "$E/$NOTES") md_skill=$(mdc "$EB/.claude/skills/docs-site/SKILL.md")->$(mdc "$E/.claude/skills/docs-site/SKILL.md") md_tokens=$(mdc "$EB/.claude/skills/docs-site/references/css-tokens.md")->$(mdc "$E/.claude/skills/docs-site/references/css-tokens.md") md_evmd=$(mdc "$EB/docs/api/verification/static-evidence-viewer-contract.md")->$(mdc "$E/docs/api/verification/static-evidence-viewer-contract.md") md_spec=$(mdc "$EB/docs/superpowers/specs/2026-09-02-api-kit-design.md")->$(mdc "$E/docs/superpowers/specs/2026-09-02-api-kit-design.md")"
           echo "js_syntax=$(node --check "$E/scripts/check-docs-a11y.js" 2>&1 | wc -l | tr -d ' ')/$(node --check "$E/design-kit/evals/visuals.spec.js" 2>&1 | wc -l | tr -d ' ')" ;;
    DG-04) (cd "$E" && node scripts/check-docs-a11y.js > "$T/a11y.txt" 2>&1; echo "a11y_rc=$? $(tail -1 "$T/a11y.txt")"; grep -E '^FAIL' "$T/a11y.txt" | head -5)
           (cd "$E" && npx playwright test design-kit/evals/visuals.spec.js --reporter=line > "$T/vis.txt" 2>&1; echo "visuals_rc=$? $(grep -oE '[0-9]+ (passed|failed|flaky)' "$T/vis.txt" | tr '\n' ' ')") ;;
    DG-05) [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] && [ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "W_NOT_TIP"; return 0; }
           echo "tool_same=$([ "$(git hash-object "$CI_LOCAL" 2>/dev/null)" = "$TOOL_BLOB" ] && echo 1 || echo 0)"
           (cd "$W" && TMPDIR="$T" bash "$CI_LOCAL" "$W" > "$T/ci.txt" 2>&1); SUM=$T/ci-local/summary.txt
           [ -s "$SUM" ] || { echo "ci_summary=absent"; return 0; }
           echo "rc0=$(grep -c 'rc=0' "$SUM") other=[$(grep -v 'rc=0' "$SUM" | sed -E 's/[[:space:]]+/ /g' | tr '\n' ';')] outside=[$(sed -n '/이 스크립트 밖의 것:/,/^[0-9]*$/p' "$T/ci.txt" | sed '1d;$d' | tr '\n' ';')]" ;;
    *) echo "UNKNOWN $1" ;;
  esac
}
# === 측정 도우미 끝 ===
```
