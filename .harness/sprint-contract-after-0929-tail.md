---
feature: "마지막 꼬리 — 연결 판정 · 전환 효과 · Mermaid 그려짐"
slug: after-0929-tail
created: "2026-09-29 20:25"
complexity: "복잡"
conditions: 26
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: "sha256:fe19cd7e88a8a978"
measurement_digest: "sha256:7237599f49dbe4b5"
locked_at: "2026-09-29 20:43"
---

## 배경

- 묶음 tail. 출처는 `.harness/.meta/after-kaizen-0928/rest-notes.md` 「남긴 것」 절이다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-tail`, 가지 `chore/ak3-tail`, 시작 판 `BASE` = `c6cfcd09` (가지 `chore/after-kaizen-0928` 끝 — rest 가 합쳐진 판).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-tail` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 다시 돌린 뒤 W 맨 위 폴더에서 잰다. 이 가지는 이 스프린트만 커밋한다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. 브라우저 측정은 W 의 `node_modules` 의 playwright 를 쓰고, `TMPDIR` 는 scratch 아래 폴더로 둔다.

항목별 처리 방침 (결정):

- **(1) 가짜 연결 넷** — `scripts/check-api-kit-docs.py` 의 공통 CSS 연결 판정이 `data-rel="stylesheet" rel="preload"` · `rel="stylesheet" data-href="../assets/site.css" href="x.css"` · `rel="alternate stylesheet"` · `media="print"` 넷을 연결로 친다(봉인 전 실측, 아래 GAP). 속성 이름 앞에 다른 글자 · `-` 가 붙은 것(`data-rel` · `data-href`)은 그 속성으로 보지 않고, `rel` 낱말에 `alternate` 가 있거나 `media` 가 화면용이 아니면 연결이 아니다. 넷을 시험 `scripts/test-check-api-kit-docs.py` 경우 6 ~ 9 로 더한다(스크립트-01).
- **(2) 물음표 값** — `href="../assets/site.css?v=2"` 는 브라우저가 같은 파일을 불러오므로 연결로 친다. 지금 api-kit 검사는 이를 연결 없음으로 본다(실측). 시험 경우 10 으로 못박는다(스크립트-01).
- **(3) 공통 CSS 검사** — `scripts/check-docs-common-css.py` 의 `site.css` 연결 세기도 같은 기준(rel 낱말에 `stylesheet` · `alternate` 아님 · `media` 없음 또는 `all` · `screen` · `data-` 속성은 rel · href 로 보지 않음 · 주소는 물음표 값을 떼고 `assets/site.css` 로 끝남)으로 센다. 지금은 `rel` 을 아예 안 봐서 `preload` · `site.css.bak` 까지 센다(실측). 시험 경우 8 을 더한다(스크립트-02). 두 검사가 같은 판정을 쓰도록 판정은 한 곳에 두고 두 검사가 불러 쓴다. 자리는 `scripts/plugin_utils.py` — 이 레포 `scripts/` 에서 두 검사 이상이 함께 쓰는 판정은 그 모듈에 두고 `from plugin_utils import …` 로 부른다(선례 `check-cause-table-copies.py:24` · `check-reviewer-protocol-copies.py:29`, 모듈 머리 설명 「사본 검사 둘이 공유하는 헬퍼」). 판정 열두 경우의 결과는 스크립트-03, 한 곳에 있음은 구조-01 이 잰다.
- **(4) 본문 배경 전환** — 기록은 40 쪽이라 적었지만 브라우저로 다시 재니(움직임 허용 설정에서 `body` 의 `transition-property` 에 `all` · `background` · `background-color` 가 있고 길이가 0 초 넘는 쪽) 47 쪽이다: api-kit 13 · tone-kit 14 · react-kit 10 · design-kit 3 · backend-kit · harness · howto-kit(`overview.html`) · infra-kit · process · reflect-kit · rust-kit 각 1. 목록은 도우미 `BODY_PAGES`. 움직임 줄이기 설정에서 공통 파일은 전환을 0.01ms 로 줄이지만, 테마 단추를 누른 직후 같은 작업 안에서 읽은 본문 배경은 47 쪽 모두 옛 색이다(0.01ms 전환도 한 번은 그려야 끝난다). 공통 파일 `docs/assets/site.css` 의 움직임 줄이기 블록에서 `html` · `body` 의 전환을 없애 해결한다 — 쪽 47 개는 건드리지 않는다(오류-01). 움직임 허용 설정의 전환은 그대로 둔다(오류-02).
- **(5) Mermaid 그려짐** — 추적 쪽 가운데 Mermaid 예시(아래 정의)가 있는 쪽은 `docs/planning-kit/data-modeling.html`(2) · `docs/planning-kit/flows.html`(4) · `docs/planning-kit/reference.html`(3), 예시 9 개다. 원본 울타리 수(`docs/planning/data-modeling.md` 2 · `docs/planning/flows.md` 4 · `docs/planning/reference.md` 3)와 같다. 새 검사 `scripts/check-docs-mermaid.js` 가 브라우저 빈 쪽에 레포가 못박은 Mermaid 를 넣고 예시마다 그려, 그림(`svg`)과 도형이 있고 오류 그림 · 오류 글이 없는지 잰다. Mermaid 는 npm `latest` 인 12.0.0(`npm view mermaid dist-tags` → `latest: '12.0.0'`, 2026-09-29 조회)을 `devDependencies` 에 정확한 판으로 넣는다. 봉인 전 실측으로 아홉 예시 모두 12.0.0 에서 그려진다 — 고칠 쪽은 없다. 검사 · 시험을 CI `playwright` 묶음(`npm ci` 뒤)에 등록한다(스크립트-04 · 스크립트-05 · 구조-02). 종료 코드 표 `harness/evals/gate-exit-codes.md` 소비처에 줄을 더한다(구조-03).
- **(5 딸림) flows 문장** — `docs/planning/flows.md` 61 줄과 쪽 `docs/planning-kit/flows.html` 은 「이 예시 자체는 Mermaid 12 에서 렌더해 확인하지 않았다」 고 적는다. 검사가 생기면 거짓이 되므로 원본 문장과 쪽의 머리 · 굵은 글 · 표 한 줄(「12 에서 렌더해 봤나 / 해 보지 않았다」) · 비교 카드를 검사 이름(`scripts/check-docs-mermaid.js`)과 12.0.0 으로 바꾼다. 나머지 여섯 사실(12.0.0 · 2026-09-10 · 비시험판 · 2026-09-28 · 두 출처 주소)은 그대로다(구조-04). `docs/planning/research-log.md:45` 「12 에서 렌더해 보지는 않았다」 는 그때의 기록이라 그대로 둔다.

용어 — **Mermaid 예시**: 쪽의 `<pre>` 가운데, 빈 줄과 `%%` 로 시작하는 줄을 건넌 첫 줄이 Mermaid 그림 종류 낱말(`flowchart` · `graph` · `sequenceDiagram` · `classDiagram` · `stateDiagram` · `stateDiagram-v2` · `erDiagram` · `journey` · `gantt` · `pie` · `mindmap` · `timeline` 등, 도우미 `mmrender.js` 의 `KW`)로 시작하는 것. **그려짐**: `mermaid.render` 가 예외 없이 돌려준 그림에 `svg` 요소가 있고 도형(`rect` · `path` · `circle` · `ellipse` · `polygon` · `line` · `text`)이 1 개 이상이며, `aria-roledescription="error"` 요소와 `Syntax error` · `Parse error` 글이 없는 것.

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 검사 스크립트 · 공용 모듈 · 시험, 공통 CSS · 문서 쪽 · 연구 원본, CI 파일 · npm 의존성, 종료 코드 표(harness) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 두 검사의 판정 규칙이 바뀌고, 새 검사가 종료 코드 네 값을 약속한다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 추적 쪽 206 개, CI 두 묶음, 공용 모듈을 부르는 다른 스크립트 일곱(`validate-plugin.py` 등), 앞 묶음 봉인 측정(오류-03) |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 판정을 조이면 추적 쪽이 걸릴 수 있고, 공통 CSS 를 바꾸면 움직임 허용 설정의 전환까지 멈출 수 있으며, 새 의존성이 CI `npm ci` · `npx playwright test` 를 바꿀 수 있다 |

기능 조건 17 개는 스크립트-01 ~ 스크립트-05 · 오류-01 ~ 오류-03 · 구조-01 ~ 구조-08 · 진단-05 다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절 · 자동 포함 여섯 줄 · `N/A (` 줄을 빼고 센 값이다. 복잡 가이드 9 ~ 20 안이다.

Step 2.5 짝 조건: 판정을 바꾸는 쪽(스크립트-01 · 스크립트-02 · 구조-01)과 판정 결과를 받는 쪽(추적 쪽 206 개 전부 통과 — 스크립트-01 · 스크립트-02 의 검사 끝 줄, CI 등록 — 스크립트-01 · 스크립트-02 · 구조-02, 공용 모듈을 부르는 다른 스크립트 — 진단-05 의 `validate-plugin` · `sync-docs` · `sync-orchestrator` · `run-evals` · `check-cause-table-copies` · `reviewer-copies`)을 따로 잰다. 새 검사를 만드는 쪽(스크립트-04 · 스크립트-05)과 받는 쪽(CI 등록 · 의존성 — 구조-02, 종료 코드 표 — 구조-03, 거짓이 된 문장 — 구조-04)을 따로 잰다. 공통 CSS 를 바꾸는 쪽(오류-01)과 그 파일을 읽는 앞 묶음 측정(오류-02 · 오류-03)을 따로 잰다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | 진단-01 N/A (대상 파일이 이번 변경 밖) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 진단-03 N/A (같은 이유) |
| `diagnostics.ide_exclude` | `[]` | 진단-02 `[]` |
| `contract_categories[].id` / `prefix` | Skill/스킬 · Script/스크립트 · Error/오류 · Architecture/구조 | 같음 |
| `anti_patterns[].id` / `message` | 금지-01 버전 하드코딩 · 금지-02 force push · 금지-03 bare code fence · 금지-04 frontmatter name | 금지-02 · 금지-03 |

## GAP 분석 (Pre-Edit Audit)

모두 W 시작 판(`c6cfcd09`)에서 연 값이다.

| 대상 | 읽은 증거 (`파일:줄` · 명령 출력) | 발견한 갭 | 조건 |
| --- | --- | --- | --- |
| `scripts/check-api-kit-docs.py` | `:52-53` `REL_ATTR = re.compile(r"\brel" …)` · `HREF_ATTR` 가 `\b` 로 시작해 `data-rel` · `data-href` 에 먼저 걸림, `:56-62` `links_site_css` 가 `alternate` · `media` 를 안 보고 주소 끝을 `endswith("assets/site.css")` 로 봄. `m 스크립트-03` → api 열이 `data-rel` · `data-href` · `alternate` · `print` 를 1, `query` 를 0 으로 냄 | 가짜 연결 넷을 셈 · 물음표 값 주소를 못 셈 | 스크립트-01 · 스크립트-03 |
| `scripts/test-check-api-kit-docs.py` | `:28-34` 경우 다섯, docstring `:2` 「짝 다섯 경우로」, `--check` 받음. 시험 `경우 5 개 중 통과 5` | 네 가짜 · 물음표 값 경우 없음 | 스크립트-01 |
| `scripts/check-docs-common-css.py` | `:34` `SITE_CSS_HREF_RE` 가 `\bhref` 로 `assets/site.css` 가 든 주소만 봄(`rel` 안 봄), `:57-58` `site_css_links`. `m 스크립트-03` → common 열이 `preload` · `bak` · `data-rel` · `data-href` · `alternate` · `print` 를 1 로 냄. 검사 `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0` | rel · media · data- 를 안 봄 | 스크립트-02 · 스크립트-03 |
| `scripts/test-check-docs-common-css.py` | `:1-17` 경우 일곱, `:94` 경우 5 가 검사 파일만 임시 저장소 `scripts/` 에 복사. 시험 `경우 7 개 중 통과 7` | 가짜 연결 경우 없음. 검사가 공용 모듈을 부르면 경우 5 가 모듈도 복사해야 한다 | 스크립트-02 |
| `scripts/plugin_utils.py` | `:1-6` 「사본 검사 둘이 공유하는 헬퍼」, `grep -c stylesheet` 0. 부르는 곳 `check-cause-table-copies.py:24` 등 7 파일. `m 구조-01` → `imports_ok=0 replaced=0` | 공용 판정 없음 | 구조-01 |
| 추적 쪽의 `site.css` 연결 모양 | 추적 쪽 206 개 주석 밖 `<link>` 가운데 `site.css` 든 것: `<link rel="stylesheet" href="../assets/site.css">` 204 · `../../assets/site.css` 1 · `assets/site.css` 1 | 조인 판정에 걸릴 쪽 없음(봉인 전 사본에서 206/206) | 스크립트-02 |
| `docs/assets/site.css` | `:6-17` 움직임 줄이기 블록 — `*` 에 `transition-duration:0.01ms !important`. `body.js list` → 47 쪽, `m 오류-01` → `bad=47` (누른 직후 옛 색), `m 오류-02` → `moving=47` | 누른 직후 본문 배경이 옛 색 | 오류-01 · 오류-02 |
| Mermaid 예시 쪽 · 원본 | `docs/planning-kit/flows.html:483` · `:579` · `:636` · `:697` `<pre class="code-block" aria-label="Mermaid … 예시">`, data-modeling `:501` · `:581`, reference 셋. `mmrender.js` (Mermaid 12.0.0 scratch 설치본) → `pages=3 examples=9 bad=0`. 추적 쪽 어디에도 Mermaid 라이브러리를 부르는 곳 없음 | 그려지는지 재는 검사 없음 | 스크립트-04 · 스크립트-05 |
| `package.json` · `package-lock.json` | `package.json:26-28` devDependencies `@playwright/test ^1.58.2` 하나. `m 구조-02` → `pkg=None` | Mermaid 없음 | 구조-02 |
| `.github/workflows/ci.yml` | `:68-71` api-kit 검사 · 시험(이름 「다섯 경우」), `:91-93` 공통 CSS 검사 · 시험(이름 「일곱 경우」), `:160-197` playwright 묶음(`npm ci` 뒤 시각 시험 · api-kit 뷰어 · 접근성) | Mermaid 단계 없음 · 경우 수 이름이 바뀔 값 | 스크립트-01 · 스크립트-02 · 스크립트-05 |
| `harness/evals/gate-exit-codes.md` | 소비처 표 `:71` `check-docs-a11y.js` · `:72` `check-api-kit-docs.py` 줄 있음. `m 구조-03` → `rows=0` | 새 검사 줄 없음 | 구조-03 |
| `docs/planning/flows.md` · 쪽 | `flows.md:61` 「이 예시 자체는 Mermaid 12 에서 렌더해 확인하지 않았다.」, 쪽 `:459` 머리 · `:464` 굵은 글 · `:475` 표 줄 · `:922-923` 비교 카드. `m 구조-04` → `old_md=1 old_page=5 name_ok=0` | 검사가 생기면 거짓이 될 문장 | 구조-04 |
| 앞 묶음 측정 | fs2 `오류-01` · `오류-02` · `구조-06`, rest `오류-01` · `오류-02` 모두 종료 코드 0 (`m 오류-03` → `runs=5 bad=0`) | 통과 중 — 지켜야 함 | 오류-03 |
| 로컬 CI · CI 전용 단계 | `## 회귀 게이트` 봉인 전 실측 | 통과 중 | 진단-05 |

## Skill

- [ ] 스킬-00: N/A (이번 변경 파일에 스킬 · 에이전트 파일이 없다. 측정: git diff --name-only c6cfcd09..chore/ak3-tail | grep -cE '(SKILL|agents/[^/]+)\.md$' 이 0)

## Script

- [ ] 스크립트-01: api-kit 문서 검사가 가짜 연결 넷을 세지 않고 물음표 값 주소는 센다 — `scripts/test-check-api-kit-docs.py` 가 열 경우를 돌린다: 기존 ① ~ ⑤ 에 더해 ⑥ `<link data-rel="stylesheet" rel="preload" href="../assets/site.css">` 만 → 연결 없음 ⑦ `<link rel="stylesheet" data-href="../assets/site.css" href="x.css">` 만 → 연결 없음 ⑧ `<link rel="alternate stylesheet" href="../assets/site.css">` 만 → 연결 없음 ⑨ `<link rel="stylesheet" media="print" href="../assets/site.css">` 만 → 연결 없음 ⑩ `<link rel="stylesheet" href="../assets/site.css?v=2">` → 연결 있음. 시험 파일 머리 설명과 CI 단계 이름이 「열 경우」 를 적는다. Given 공통 전제 G, When `m 스크립트-01`, Then `count_words_ok=1 test_ok=1 check_ok=1 tags_ok=1 base_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` — `python3 scripts/test-check-api-kit-docs.py` 종료 코드 0 · 끝 줄 `경우 10 개 중 통과 10`, `python3 scripts/check-api-kit-docs.py` 종료 코드 0 · 끝 줄 `12/12 PASS`, 시험 파일에 ⑥ ~ ⑩ 의 태그 글 다섯(`data-rel="stylesheet"` · `data-href="../assets/site.css"` · `rel="alternate stylesheet"` · `media="print"` · `site.css?v=2`), `.github/workflows/ci.yml` 의 `validate` 묶음에 `run: python3 scripts/test-check-api-kit-docs.py` 정확히 1 줄. 시작 판 `count_words_ok=0 test_tail=[경우 5 개 중 통과 5] … base_rc=0 base_fails=0 … ci=1` · 종료 코드 1
  음성 대조: 시작 판 검사 사본(`git show c6cfcd09:scripts/check-api-kit-docs.py`)을 `--check <사본>` 으로 주면 ⑥ ~ ⑩ 다섯이 실패해 종료 코드 1 · `FAIL` 줄 5 (`base_ok`). 준비 단계 봉인 전 실측: 사본 꺼내기와 지금 시험의 `--check <사본>` 이 `경우 5 개 중 통과 5` 로 돈다. 구현 뒤 모양 사본에서 `base_rc=1 base_fails=5`
- [ ] 스크립트-02: 공통 CSS 검사가 같은 기준으로 연결을 센다 — `scripts/test-check-docs-common-css.py` 의 새 경우 8: ① 가짜 연결 넷(스크립트-01 ⑥ ~ ⑨ 과 같은 태그) 하나씩만 있는 쪽 넷 → 각각 종료 코드 1 · 그 쪽 이름 · `site_css_links=0` 이 적힘 ② `<link rel="stylesheet" href="../assets/site.css?v=2">` 쪽 → 종료 코드 0 ③ 진짜 연결 하나와 가짜 넷이 함께 있는 쪽 → 종료 코드 0. 경우 5(추적 쪽 0 개 임시 저장소)는 검사가 공용 모듈을 불러도 종료 코드 3 을 낸다. 시험 머리 설명과 CI 단계 이름이 「여덟 경우」 를 적는다. Given 공통 전제 G, When `m 스크립트-02`, Then `count_words_ok=1 test_ok=1 check_ok=1 tags_ok=1 base_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02` — 시험 종료 코드 0 · 끝 줄 `경우 8 개 중 통과 8`, `python3 scripts/check-docs-common-css.py` 종료 코드 0 · 끝 줄 `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0`, 시험 파일에 태그 글 넷(`data-rel="stylesheet"` · `data-href="../assets/site.css"` · `rel="alternate stylesheet"` · `site.css?v=2`), `validate` 묶음에 `run: python3 scripts/test-check-docs-common-css.py` 정확히 1 줄. 시작 판 `count_words_ok=0 test_tail=[경우 7 개 중 통과 7] … base_ok=0` · 종료 코드 1
  음성 대조: 시작 판 검사 사본(`git show c6cfcd09:scripts/check-docs-common-css.py`)을 `--check <사본>` 으로 주면 `FAIL 경우 8` 한 줄만 나오고 종료 코드 1 (`base_ok`). 준비 단계 봉인 전 실측: 지금 시험 `--check <사본>` → `경우 7 개 중 통과 7`. 구현 뒤 모양 사본에서 `base_ok=1`
- [ ] 스크립트-03: 두 검사의 연결 판정이 열두 경우에서 기대와 같고 서로 같다 — 도우미 `LINK_CASES` 열두 경우(`stylesheet` · `quote-mix` · `preload` · `bak` · `comment` · `data-rel` · `data-href` · `alternate` · `print` · `query` · `media-all` · `media-screen`, 기대 연결 1 · 1 · 0 · 0 · 0 · 0 · 0 · 0 · 0 · 1 · 1 · 1)를 `<head>` 에 넣은 임시 쪽으로 api-kit 검사의 `check(원본, 쪽)` 판정과 공통 CSS 검사 명령 판정(종료 코드 0 = 연결, 1 과 `site_css_links=0` = 연결 없음)을 받는다. Given 공통 전제 G, When `m 스크립트-03`, Then `cases=12 right=12 agree=12 all_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03`. 시작 판 `BAD` 일곱 줄(`preload` · `bak` · `data-rel` · `data-href` · `alternate` · `print` · `query`) · `cases=12 right=5 agree=9 all_ok=0` · 종료 코드 1 (양성 대조 겸함). 알려진 답: 열두 기대값은 손으로 정한 위 값이고, 구현 뒤 모양 사본에서 `right=12 agree=12`
- [ ] 스크립트-04: Mermaid 검사가 레포 쪽 예시를 모두 그리고 깨진 예시를 잡는다 — `node scripts/check-docs-mermaid.js`(인자 없이 = git 이 추적하는 `docs/*.html` 전부)가 예시마다 한 줄을 적고 끝 줄 `쪽 3 · 예시 9 · 안 그려진 예시 0` · 종료 코드 0 을 내며, 출력에 `docs/planning-kit/data-modeling.html` · `docs/planning-kit/flows.html` · `docs/planning-kit/reference.html` 이 모두 있다. 따로 짠 그리기(도우미 `mmrender.js`)도 추적 쪽 전부에서 `pages=3 examples=9 bad=0` 이다. `flows.html` 첫 예시의 `A["Visitor lands on pricing"]` 닫는 괄호를 지운 사본을 인자로 주면 종료 코드 1 이고 그 사본 이름이 적힌다. Given 공통 전제 G, When `m 스크립트-04`, Then `ok=1 pages_named_ok=1 ref_ok=1 broken_applied=1 broken_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04`. 시작 판 검사 없음 → `rc=1 … ok=0 pages_named_ok=0 ref=[pages=3 examples=9 bad=0] ref_ok=1 broken_applied=1 broken_rc=1 broken_ok=0` · 종료 코드 1. `mmrender.js` 는 봉인 전 Mermaid 12.0.0 scratch 설치본(`MM_LIB=<scratch>/mm/node_modules/mermaid/dist/mermaid.min.js`)으로 쟀고, 구현 뒤에는 W `node_modules` 의 같은 판을 쓴다
  알려진 답: 예시 수 9 는 원본 울타리 수 2 + 4 + 3 을 손으로 센 값이다. 음성 대조: 깨진 사본을 `mmrender.js` 에 주면 `BAD …#1 svg=0 … err=1 msg=Parse error on line 2:` · 종료 코드 1 (봉인 전 실측) — 검사도 같은 사본에서 1 을 내야 한다(`broken_ok`)
- [ ] 스크립트-05: Mermaid 검사 시험 네 경우가 통과하고 CI 에 등록된다 — `node scripts/test-check-docs-mermaid.js` 가 임시 폴더에서 ① 그려지는 예시 하나 쪽 → 검사 종료 코드 0 ② 깨진 예시 쪽 → 1 과 그 쪽 이름 ③ 예시 없는 쪽 → 3 ④ `node_modules` 를 찾을 수 없는 임시 폴더로 옮긴 검사 사본 → 2 를 확인하고 끝 줄 `경우 4 개 중 통과 4` · 종료 코드 0 을 낸다. 시험은 `--check <검사 사본>` 을 받는다. `.github/workflows/ci.yml` 의 `playwright` 묶음에 `run: node scripts/check-docs-mermaid.js` · `run: node scripts/test-check-docs-mermaid.js` 가 각각 정확히 1 줄이고 둘 다 `run: npm ci` 뒤이며, 시험 단계 이름이 「네 경우」 를 적는다. Given 공통 전제 G, When `m 스크립트-05`, Then `test_ok=1 stub_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-05`. 시작 판 시험 없음 → `test_rc=1 … test_ok=0 … ci_ok=0` · 종료 코드 1
  음성 대조: 늘 `쪽 0 · 예시 0 · 안 그려진 예시 0` 과 종료 코드 0 을 내는 가짜 검사(도우미가 임시 폴더에 새로 쓰는 `stub-check.js`)를 `--check` 로 주면 경우 ② ③ ④ 가 실패해 시험 종료 코드 1 (`stub_ok`). 구현 뒤 모양 사본에서 `stub_rc=1`

## Error

- [ ] 오류-01: 움직임 줄이기 설정에서 테마 단추를 누른 직후 본문 배경이 끝 색이다 — 움직임 허용 설정에서 본문 배경 전환이 걸린 쪽(도우미 `body.js list` 를 추적 쪽 전부에 돌린 결과)이 도우미 `BODY_PAGES` 47 쪽과 같고, 그 47 쪽마다 움직임 줄이기 · 어두운 설정으로 열어 단추(`#theme-btn` · `#themeToggle` · `.dk-theme-btn`)를 누른 같은 작업 안에서 읽은 본문 배경이 800ms 뒤 값과 같으며 누르기 전과 다르다. 세 번 재어 세 번 모두다. Given 공통 전제 G, When `m 오류-01`, Then `listed=47 same_set=1 pages=47 bad=0 rcs=0,0,0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01`. 시작 판 `listed=47 same_set=1 pages=47 bad=47 rcs=0,0,0 ok=0` · 종료 코드 1 (양성 대조 겸함 — 0 기대 `bad` 가 시작 판에서 47). 구현 뒤 모양 사본(`docs/assets/site.css` 움직임 줄이기 블록에 `html,body{transition-duration:0s !important}` 한 줄)에서 `bad=0` (봉인 전 실측, 두 번)
- [ ] 오류-02: 움직임 허용 설정에서는 47 쪽의 본문 배경 전환이 그대로 돈다 — 오류-01 과 같은 47 쪽을 움직임 허용 · 어두운 설정으로 열어 단추를 누르면 누르기 전과 800ms 뒤가 다르고, 누른 직후 · 16 · 50 · 100 · 200 · 400 · 800ms 에 읽은 값이 서로 다른 것 셋 이상이다. Given 공통 전제 G, When `m 오류-02`, Then `pages=47 moving=47 rc=0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02`. 시작 판 `pages=47 moving=47 rc=0 ok=1` · 종료 코드 0. 양성 대조: 공통 파일이 아니라 쪽마다 본문 전환을 지운 모양(전환 자체를 없앤 구현)이면 `distinct` 가 1 ~ 2 라 이 조건이 FAIL 한다 — 봉인 전 실측: 움직임 줄이기 설정의 시작 판이 `distinct` 1 ~ 2 로 같은 모양을 낸다(오류-01 측정 줄 `mid=2`)
- [ ] 오류-03: 앞 묶음 측정 다섯이 이 판에서도 통과한다 — fs2 측정 `.harness/.meta/after-0929-final-sweep-docs/measure.py` 의 `오류-01`(추적 쪽 전부 움직임 줄이기) · `오류-02`(움직임 허용 설정이 fs2 시작 판과 같음) · `구조-06`(쪽 `<style>` 에 움직임 줄이기 규칙 0 · 공통 파일에 1 블록)과 rest 측정 `.harness/.meta/after-0929-leftovers/measure.py` 의 `오류-01` · `오류-02`(스크립트 움직임 셋)가 모두 종료 코드 0 이다. Given 공통 전제 G, When `m 오류-03`, Then 다섯 줄 `OK` · `runs=5 bad=0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-03`. 시작 판 `runs=5 bad=0 ok=1` · 종료 코드 0. 봉인 전 사본 대조: 구현 뒤 모양 사본에서 다섯 모두 종료 코드 0 (「더하라」 조건 오류-01 과 「그대로」 조건 오류-03 이 함께 겨누는 파일 `docs/assets/site.css` 에서 부딪히지 않는다)

## Architecture

- [ ] 구조-01: 연결 판정이 공용 모듈 한 곳에 있다 — `scripts/check-api-kit-docs.py` · `scripts/check-docs-common-css.py` 가 모두 `from plugin_utils import` 또는 `import plugin_utils` 줄을 갖고, W 를 `git clone --shared` 한 사본(작업 폴더의 세 파일을 얹음)에서 `scripts/plugin_utils.py` 의 문자열 값 안 `stylesheet` 만 다른 낱말로 바꾸면 스크립트-03 열두 경우 가운데 연결 기대 다섯 경우를 두 검사 모두 0 개 연결로 본다(두 검사가 각자 판정을 따로 들고 있으면 이 값이 0 이 아니다). Given 공통 전제 G, When `m 구조-01`, Then `imports_ok=1 replaced` 1 이상 · `api_pos_after=0 common_pos_after=0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-01`. 시작 판 `imports=check-api-kit-docs.py:0,check-docs-common-css.py:0 imports_ok=0 replaced=0 api_pos_after=4 common_pos_after=5 ok=0` · 종료 코드 1. 구현 뒤 모양 사본에서 `imports_ok=1 replaced=1 api_pos_after=0 common_pos_after=0` (봉인 전 실측 — 바꿈은 문자열 토큰만 건드려 함수 이름은 그대로다)
- [ ] 구조-02: Mermaid 를 12.0.0 으로 못박았다 — `package.json` 의 `devDependencies.mermaid` 가 `12.0.0`(범위 기호 없음)이고 `@playwright/test` 는 `^1.58.2` 그대로이며, `package-lock.json` 의 `packages["node_modules/mermaid"].version` 과 `packages[""].devDependencies.mermaid` 가 `12.0.0`, `npm ci` 뒤 `node_modules/mermaid/package.json` 의 `version` 이 `12.0.0` 이다. Given 공통 전제 G, When `m 구조-02`, Then `pkg=12.0.0 pw=^1.58.2 lock=12.0.0 lock_root=12.0.0 installed=12.0.0 ok=1` · 종료 코드 0 [exact]
  측정: `m 구조-02`. 시작 판 `pkg=None pw=^1.58.2 lock=None lock_root=None installed=None ok=0` · 종료 코드 1. 구현 뒤 모양 사본(`npm install --save-dev --save-exact mermaid@12.0.0`)에서 `ok=1`
- [ ] 구조-03: 종료 코드 표에 새 검사가 있다 — `harness/evals/gate-exit-codes.md` 소비처 표에서 첫 칸이 `scripts/check-docs-mermaid.js` 인 줄이 정확히 하나이고 둘째 칸이 `0 · 1 · 2 · 3` 이다(빈칸을 빼고 맞댄다). Given 공통 전제 G, When `m 구조-03`, Then `rows=1 ok=1` · 종료 코드 0 [exact]
  측정: `m 구조-03`. 시작 판 `rows=0 row=[] ok=0` · 종료 코드 1
- [ ] 구조-04: flows 원본 · 쪽이 거짓이 된 문장을 버리고 검사 이름을 적는다 — `docs/planning/flows.md` 에 `아래 예시는 Mermaid 공식 flowchart 문법을 따른다` 로 시작하는 줄이 정확히 하나이고, 그 줄과 `docs/planning-kit/flows.html` 의 보이는 글 · 링크 주소에 `12.0.0` · `2026-09-10` · `비시험판` · `2026-09-28` · `registry.npmjs.org/mermaid/latest` · `releases/tag/mermaid%4012.0.0` 여섯이 모두 있으며, 원본과 쪽 보이는 글에 `렌더해 확인하지 않았다` · `렌더해 봤나` · `해 보지 않았다` 가 0 이고, 그 줄과 쪽 보이는 글에 `check-docs-mermaid.js` 가 있으며, 그 줄의 낱말 · 인라인 코드(fs2 도우미 `words` · `codes` 세기)가 모두 쪽 보이는 글에 있고, 원본 `last_updated` 와 쪽 두 날짜가 `docs/planning/flows.md` 를 마지막으로 바꾼 커밋 날과 같다. Given 공통 전제 G, When `m 구조-04`, Then `keep_ok=1 old_ok=1 name_ok=1 line_in_page_ok=1 dates_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-04`. 시작 판 `md_lines=1 keep_md=[] keep_page=[] keep_ok=1 old_md=1 old_page=5 old_ok=0 name_ok=0 line_in_page_ok=1 miss=[] dates=2026-09-29/2026-09-29/2026-09-29/2026-09-29 dates_ok=1` · 종료 코드 1 (양성 대조 겸함 — 0 기대 `old_page` 가 시작 판에서 5). 구현 뒤 모양 사본에서 `old_md=0 old_page=0 name_ok=1` · 종료 코드 0
- [ ] 구조-05: 기록 — `.harness/.meta/after-kaizen-0928/tail-notes.md` 에 낱말 `check-api-kit-docs` · `check-docs-common-css` · `plugin_utils` · `data-rel` · `site.css?v=2` · `prefers-reduced-motion` · `check-docs-mermaid` · `12.0.0` · `flows.md` · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 5 개 이상이 있다. Given 공통 전제 G, When `m 구조-05`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-05`. 시작 판 파일 없음 · 종료 코드 1
- [ ] 구조-06: 이번에 바뀐 docs 쪽(`git diff --name-only c6cfcd09..HEAD -- docs` 의 `.html`)이 두 테마(`dark` · `light`) 각각 320 · 375 · 1280 폭에서 가로 넘침 0 이다. Given 공통 전제 G, When `m 구조-06`, Then `pages` 1 이상 · `bad=0 br_rc=0,0` · 종료 코드 0 [exact]
  측정: `m 구조-06` (rest `m_overflow` 를 이 기준 판으로). 시작 판 `pages=0 themes=2 bad=0 br_rc=0,0` · 종료 코드 1 (바뀐 쪽 없음). 양성 대조는 같은 함수로 rest 가 봉인 전에 쟀다(폭 2000px 상자 사본 → `of=1680/1625/720`)
- [ ] 구조-07: 바뀐 docs 파일(`.html` · `.css` · `.js`)이 레포 밖 자원을 부르지 않는다 — fs2 구조-10 과 같은 식. Given 공통 전제 G, When `m 구조-07`, Then `checked` 1 이상 · `ext_files=0` · 종료 코드 0 [exact]
  측정: `m 구조-07`. 시작 판 `checked=0 ext_files=0 git_rc=0` · 종료 코드 1. 양성 대조는 같은 함수로 fs2 가 봉인 전에 쟀다(`ext_files=3`)
- [ ] 구조-08: 커밋 규칙 — `c6cfcd09..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(레포 맨 위 바로 아래 파일 `package.json` · `package-lock.json` 은 한 묶음 `(root)`, docs 는 `docs/<폴더>` 하나 — `docs/assets` · `docs/planning` · `docs/planning-kit` 은 서로 다른 폴더)이며, `.harness/` 파일은 구현 파일과 다른 커밋이고, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이며, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-08`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-08`. 시작 판 `commits=0` · 종료 코드 1

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-tail` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 바뀐 `.md` 세 파일에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 공통 CSS 연결 판정은 `scripts/plugin_utils.py` 에 두어 두 검사가 부르고 — 구조-01, 새 Mermaid 검사 · 시험은 CI 에 등록해 누구나 부른다 — 스크립트-05)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 판정 자리는 기존 공용 모듈 `scripts/plugin_utils.py` — 구조-01, 새 경우는 기존 두 시험의 경우 표에 더하고 — 스크립트-01 · 스크립트-02, 새 시험은 기존 시험의 `--check <검사 사본>` · 끝 줄 `경우 N 개 중 통과 M` 모양을 따르며 — 스크립트-05, 전환 문제는 쪽 47 개가 아니라 공통 파일 한 곳에서 푼다 — 오류-01)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only c6cfcd09..chore/ak3-tail | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.md` 세 파일(`docs/planning/flows.md` · `harness/evals/gate-exit-codes.md` · `.harness/.meta/after-kaizen-0928/tail-notes.md`)은 markdownlint-cli2(MD013 끔)로 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`, 바뀐 `.py` 는 `python3 -m py_compile` 종료 코드 0, 바뀐 `.js` 는 `node --check` 종료 코드 0
  측정: 파일마다 `<scratch>/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/rest/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(설정 파일 내용 `{ "config": { "MD013": false } }`). 시작 판 앞 두 파일 `warn=0 ran=1`, 구현 뒤 모양 사본 두 파일 `warn=0`. 양성 대조: `#bad` 제목과 빈 줄 셋이 든 사본 `pos.md` → 경고 4 (봉인 전 실측)
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 검사 스크립트 · 시험 · 공통 CSS · 문서 쪽 · 연구 원본 · CI 파일 · npm 의존성 · 기록. 측정: git diff --name-only c6cfcd09..HEAD -- . ':(exclude).harness' | grep -cvE '^(docs/|scripts/|\.github/|harness/evals/gate-exit-codes\.md$|package(-lock)?\.json$)' 이 0. 쪽을 브라우저로 여는 확인은 스크립트-04 · 오류-01 · 오류-02 · 오류-03 · 구조-06 이 한다)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` (TMPDIR 은 scratch 아래 새 폴더)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외)이고 `docs-a11y` 로그 끝이 `206/206 PASS`, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/test-check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-check-docs-common-css.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/check-install-docs-guidance.py` · `python3 scripts/test-check-cause-table-copies.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `node scripts/check-docs-mermaid.js` · `node scripts/test-check-docs-mermaid.js` 의 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 `grep -c 'rc=0' <TMPDIR>/ci-local/summary.txt`. 시작 판 ci-local 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `206/206 PASS`, CI 전용 단계 모두 종료 코드 0 (`12/12 PASS` · `경우 5 개 중 통과 5` · `어긋남 0` · `경우 3 개 중 통과 3` · `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0` · `경우 7 개 중 통과 7` · `checked=2 violations=0 infra_errors=0` · `need=0` · `실패 0 건` 넷 · `checked=6 violations=0` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0`), `npx playwright test` `174 passed` (봉인 전 실측. 끝 두 명령은 구현이 만든다 — 구현 뒤 모양 사본에서 둘 다 종료 코드 0)

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
scripts/plugin_utils.py
scripts/check-api-kit-docs.py
scripts/test-check-api-kit-docs.py
scripts/check-docs-common-css.py
scripts/test-check-docs-common-css.py
scripts/check-docs-mermaid.js
scripts/test-check-docs-mermaid.js
.github/workflows/ci.yml
package.json
package-lock.json
docs/assets/site.css
docs/planning/flows.md
docs/planning-kit/flows.html
harness/evals/gate-exit-codes.md
```

- 하지 않는 것: 쪽 47 개의 본문 전환 줄 지우기(공통 파일 한 곳에서 푼다), 원본 `.md` · 스킬의 `mermaid` 코드 울타리를 그려 보기(이번 대상은 문서 쪽 예시다 — `docs/planning/ideation.md` 의 `mindmap` 셋 · `planning-kit/skills/` 의 울타리 아홉은 쪽에 예시로 실려 있지 않다), 옛 기록(`docs/planning/research-log.md:45` · 쪽 `docs/planning-kit/research-log.html:249`) 고치기, 킷 버전 올리기 · 릴리스 · 합치기 · push, 로컬 CI 도구 `ci-local.sh`(레포 밖) 고치기, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일 고치기.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약은 `status: done` 이고 이 계약의 조건을 느슨하게 하지 않는다): rest 계약 `스크립트-01` · `스크립트-02` · `진단-05` 측정 줄이 적은 시험 끝 줄 `경우 7 개 중 통과 7` · `경우 5 개 중 통과 5` 는 여덟 · 열로 는다(경우를 더하는 쪽이라 더 엄격하다). rest `m 구조-02` 의 `FLOW_KEYS` 일곱째 `렌더해 확인하지 않았다` 는 구조-04 가 지우는 문장이라 그 측정은 이 판에서 `md_keys_ok=0` 이 된다 — 나머지 여섯 낱말 · 날짜 · 「최신 안정판」 0 은 구조-04 가 그대로 잰다. 그래서 오류-03 은 이 둘을 빼고 공통 파일 · 스크립트 움직임 측정 다섯만 지킨다.
- 교차 진단(봉인 전, qa-evaluator 새 에이전트): 조건을 고칠 지적은 없었다. 관찰 둘은 구현이 지킨다 — 구조-05 의 8 자리 16 진수 세기는 해시가 아닌 글자도 셀 수 있으므로 기록에는 실제 커밋 해시만 적는다. 스크립트-03 은 `scripts/check-api-kit-docs.py` 의 모듈 이름 `REPO` · `check` 를 불러 쓰므로 구현은 이 두 이름을 바꾸지 않는다(바뀌면 스크립트-01 의 실행 측정이 먼저 걸린다).
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` · `.github/` · `(root)`(`package.json` · `package-lock.json`) · `harness/` 는 따로, docs 는 `docs/assets` · `docs/planning` · `docs/planning-kit` 따로. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0929-tail/`)은 따로다.
- 교차 대조(봉인 전): 여러 파일을 한꺼번에 바꾸는 조건(스크립트-01 · 스크립트-02 · 구조-01 · 구조-04 · 오류-01)이 건드리는 글자 · 파일을 읽는 기존 검사를 `grep` 으로 찾았다 — `scripts/` · `.github/` · `harness/evals/` 에서 `check-api-kit-docs` · `check-docs-common-css` · `site.css` · `package.json` · `flows` · `Mermaid` · `12.0.0` 을 읽는 것은 `scripts/check-docs-a11y.js`(본문 전환을 기다린 뒤 색을 잰다 — 움직임 허용 설정이라 오류-01 의 변경에 닿지 않는다), `harness/evals/gate-exit-codes.md`(소비처 표 — 구조-03 이 고친다), `.github/workflows/ci.yml`(단계 이름의 경우 수 — 스크립트-01 · 스크립트-02 가 고친다), `scripts/test-check-docs-common-css.py` 경우 5(검사 파일만 복사 — 스크립트-02 가 공용 모듈도 복사하게 고친다)다. `scripts/plugin_utils.py` 를 부르는 다른 스크립트 일곱(`validate-plugin.py` · `sync-docs.py` · `sync-orchestrator.py` · `run-evals.py` · `run-kaizen-assertions.py` · `check-cause-table-copies.py` · `check-reviewer-protocol-copies.py`)은 함수 하나가 늘어도 그대로 돈다. 구현 뒤 모양 scratch 사본(`git clone --shared` 뒤 공용 판정 · 두 검사 · 두 시험 · 공통 CSS 한 줄 · Mermaid 검사 · 시험 · CI 네 줄 · `npm install --save-dev --save-exact mermaid@12.0.0` · 종료 코드 표 한 줄 · flows 원본 한 문장 · 쪽 네 자리)에서, 폴더별 서명 커밋 아홉 개로 나눠 담은 뒤 이 계약 측정 열다섯 개(스크립트-01 ~ 05 · 오류-01 ~ 03 · 구조-01 ~ 04 · 구조-06 ~ 08 — 구조-05 는 기록 파일이 구현 몫이라 뺐다)가 모두 종료 코드 0 이었고, `## 회귀 게이트` 의 사본 대조 줄에 적은 검사들도 모두 종료 코드 0 이었다. CI 에만 있는 단계와 이 범위 목록을 맞대면, 이 계약이 바꾸는 검사 둘 · 시험 둘과 새 검사 · 시험이 모두 진단-05 의 목록에 있고, 범위 밖 스크립트를 고쳐야 하는 경우는 없다. `npx playwright test` 는 `testDir: '.'` 이지만 기본 시험 파일 모양(`*.spec.js` · `*.test.js`)만 읽고 `node_modules` 는 건너뛰므로 새 파일 이름(`test-check-docs-mermaid.js`)과 Mermaid 설치본을 읽지 않는다 — 사본에서 `174 passed` 로 같았다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0929-tail/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 본문 배경 전환은 같은 폴더 `body.js`, Mermaid 대조 그리기는 `mmrender.js`, 넘침 · 밖 자원 · 커밋 범위 목록 읽기는 rest · fs2 도우미를 불러 쓴다. `MM_LIB` 환경 변수를 주지 않으면 `mmrender.js` 는 W `node_modules/mermaid/dist/mermaid.min.js` 를 쓴다.
- 도우미가 쓰는 판: 시작 판 `c6cfcd09`. 봉인 전 파일 지문(`shasum -a 256 <파일> | cut -c1-16`): 이 계약 커밋 직전에 다시 찍어 아래 줄에 적는다 — `body.js` `e4d30bb7c06df5b1` · `mmrender.js` `79a7d960292e5337` · rest `measure.py` `9174c7de7b5cc09f` · fs2 `measure.py` `1d53c015d309e924` · fs2 `br.js` `01c706e939a85586`. `measure.py` 지문은 이 절 끝 줄에 있다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본, 2026-09-29): 이 계약 측정 스크립트-01 ~ 05 · 오류-01 ~ 03 · 구조-01 ~ 04 · 구조-06 ~ 08 종료 코드 0 (구조-06 `pages=1` · 구조-07 `checked=2 ext_files=0` · 구조-08 `commits=9 bad=0`). 같은 사본에서 로컬 CI 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `206/206 PASS`, 진단-05 의 CI 전용 명령 열여덟 모두 종료 코드 0 (`npx playwright test` `174 passed`), `python3 scripts/detect-docs-drift.py --since c6cfcd09` 짝은 `docs/planning/flows.md → docs/planning-kit/flows.html` 하나(구조-04 가 맞춘다), `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0. 같은 사본에서 `python3 scripts/check-api-kit-docs.py` `12/12 PASS` · 시험 `경우 10 개 중 통과 10` · `python3 scripts/check-docs-common-css.py` `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0` · 시험 `경우 8 개 중 통과 8` · `node scripts/check-docs-mermaid.js` `쪽 3 · 예시 9 · 안 그려진 예시 0` · 시험 `경우 4 개 중 통과 4`.
- 수 206 은 시작 판 추적 쪽 수다. 쪽을 더하거나 지우면 스크립트-02 · 진단-05 의 수가 달라진다. 47 은 시작 판 `body.js list` 결과이고, 기록(rest-notes)의 40 은 다른 셈이다.
- 봉인 전 실측(2026-09-29, W 시작 판): 스크립트-01 · 스크립트-02 · 스크립트-03 · 스크립트-04 · 스크립트-05 · 오류-01 · 구조-01 · 구조-02 · 구조-03 · 구조-04 · 구조-05 · 구조-06 · 구조-07 · 구조-08 종료 코드 1(결함 재현 · 산출물 없음), 오류-02 · 오류-03 종료 코드 0(지킬 동작). 값은 각 조건 측정 줄과 `## GAP 분석` 에 있다.
- 커버리지 해소: 스크립트-01 · 스크립트-02 — 검사 · 시험 · CI 파일은 측정 명령의 인자이고, `<link …>` 모양은 시험 경우의 내용이다. 태그 글은 도우미 `m_api_test` · `m_css_test` 의 `tags` 에 글자 그대로 있다.
- 커버리지 해소: 스크립트-03 — 열두 경우의 이름 · 태그 · 기대값은 도우미 `LINK_CASES` 한 곳에 있고 `m 스크립트-03` 이 틀린 경우를 이름으로 찍는다.
- 커버리지 해소: 스크립트-04 · 스크립트-05 — 쪽 세 개는 도우미 `MM_PAGES`, 깨진 사본을 만드는 글은 `m_mm_check` 의 `old` 에 글자 그대로 있다.
- 커버리지 해소: 오류-01 · 오류-02 — 47 쪽은 도우미 `BODY_PAGES` 한 곳에 두고 `m 오류-01` 이 실측 목록과 맞대며 어긋난 쪽을 `BAD` 로 찍는다(목록을 두 번 적지 않는다).
- 커버리지 해소: 오류-03 — 측정 파일 두 개와 조건 다섯은 도우미 `m_prior` 의 `runs` 에 글자 그대로 있다.
- 커버리지 해소: 구조-01 · 구조-02 · 구조-03 · 구조-04 · 구조-05 — 파일 경로와 낱말은 도우미 `API_CHECK` · `CSS_CHECK` · `SHARED` · `EXIT_TABLE` · `FLOWS_MD` · `FLOWS_PAGE` · `FLOW_KEEP` · `NOTES` 와 `m_notes` 의 `keys` 에 글자 그대로 있다.
- 커버리지 해소: 진단-02 · 진단-05 — 파일 · 명령 목록이 조건 줄 안에 백틱으로 있다. 검출기는 빈칸 든 백틱 덩어리를 건너뛴다.
- 오라클 해소: 스크립트-01 ~ 05 · 진단-05 — 글자 찾기가 아니라 시험 · 검사를 실제로 돌린 종료 코드 · 끝 줄로 판정하고 음성 대조가 붙어 있다. `ci.yml` · 시험 파일 글자 확인은 등록 · 경우 존재 확인일 뿐이다.
- 오라클 해소: 구조-01 — 글자 찾기(`import` 줄)만으로는 각 검사가 판정을 따로 들고 있어도 통과하므로, 사본에서 공용 모듈의 판정 값만 망가뜨려 두 검사의 판정이 함께 바뀌는지 실제로 돌려 잰다.
- 오라클 해소: 오류-01 · 오류-02 — 브라우저에서 단추를 실제로 눌러 읽은 계산된 색으로 판정한다. 오류-01 은 같은 작업 안에서 읽으므로 그림이 한 번 그려지기 전의 값을 잰다.
- 오라클 해소: 진단-02 — 글자 찾기가 아니라 markdownlint · `py_compile` · `node --check` 를 실행해 그 출력으로 판정하고, 양성 대조(경고 4)를 봉인 전에 쟀다.
- 오라클 해소: 구조-04 · 구조-05 — 원본 · 쪽 · 기록 글을 고치는 것 자체가 요구다. 날짜는 커밋 기록에서 뽑은 값과 맞댄다.
- 도우미 `measure.py` 지문(봉인 전): `3d920fd41c46e7f6`.
