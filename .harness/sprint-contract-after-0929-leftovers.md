---
feature: "남은 작은 결함 모음 — nr · fs2 검토가 넘긴 것"
slug: after-0929-leftovers
created: "2026-09-29 18:40"
complexity: "복잡"
conditions: 28
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: "sha256:22e89d143f5d6cdc"
measurement_digest: "sha256:8b6f09f5db78ab5d"
locked_at: "2026-09-29 18:54"
---

## 배경

- 묶음 rest. 출처는 `.harness/.meta/after-kaizen-0928/nr-notes.md` 「남긴 것」 · 「독립 검토가 짚은 작은 결함 셋」 과 `.harness/.meta/after-kaizen-0928/fs2-notes.md` 「이 묶음 밖으로 남긴 것」 · 「QA 3 회차 APPROVE 뒤 남은 것」 이다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`(A10). 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rest`, 가지 `chore/ak3-rest`, 시작 판 `BASE` = `ab637374` (가지 `chore/after-kaizen-0928` 끝 — fs1 `a29ef6c9` · fs2 `dd7a9313` · nr `ab637374` 이 모두 합쳐진 판). 드리프트 다시 보기 기준 `DRIFT_SINCE` = `cacd9da3` (fs2 가 쪽을 맞춘 기준 판).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-rest` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력일 때 W 맨 위 폴더에서 잰다. 이 가지는 이 스프린트만 커밋하므로 HEAD 는 이 스프린트 끝과 같다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. 브라우저 측정은 W 의 `node_modules`(`npm ci`) 의 playwright 를 쓰고, `TMPDIR` 는 scratch 아래 폴더로 둔다.

항목별 처리 방침 (결정):

- **(1) prd-patterns 날짜** — nr 이 `d6fe28e3`(2026-09-29)에 새 절과 출처 셋을 더했는데 원본 `last_updated` 와 쪽 머리 · 꼬리 날짜가 `2026-09-25` 그대로다. 셋 다 `2026-09-29` 로 고친다(구조-01). `version` 은 그대로 둔다.
- **(2) Gotcha 10 번호 겹침** — `onboarding-kit/skills/setup-guide/SKILL.md` Gotcha 10 의 `1. ①` ~ `5. ⑤` 를 `- ①` ~ `- ⑤` 로 바꾼다. 쪽(`docs/onboarding-kit/setup-guide.html` Gotcha 10 칸)은 이미 ①~⑤ 만 쓴다(스킬-02).
- **(3) Phase 4 두 확인 단계** — 원본 Phase 4 에 두 단계를 더한다: 출처 줄의 조회일과 원문 Last updated 를 따로 적었는지, 서비스 계정 키는 대안이 없을 때만 안내했는지(Gotcha 10). 쪽 Phase 4 목록도 같은 수 · 같은 확인으로 맞춘다. 쪽 끝 체크리스트(`final-title`)의 두 항목은 이미 있다(스킬-03).
- **(4) A10 둘째 몫** — `docs/planning/flows.md` 61 줄 「최신 안정판」 문장을 `ex/A10.md` §3 교체안대로 쓴다: 공식 flowchart 문법 · Mermaid core 12.0.0 이 2026-09-10 공개된 비시험판(출처 GitHub 릴리스 `releases/tag/mermaid%4012.0.0`) · 2026-09-28 에 가져온 npm `latest` 도 12.0.0(`registry.npmjs.org/mermaid/latest`) · 이 예시는 12 에서 렌더해 확인하지 않았다. 쪽 `docs/planning-kit/flows.html` 의 머리 줄 · 알림 상자 · 표 두 줄 · 비교 카드 문장(「최신 안정판」 여섯 자리)도 같게 맞추고, 원본 · 쪽 날짜를 그 커밋 날로 올린다(구조-02). `docs/planning/research-log.md:45` 의 「최신 안정판」 은 그때의 기록이라 그대로 둔다.
- **(5) 공통 CSS 검사 media 속성** — `scripts/check-docs-common-css.py` 가 `<style media="(prefers-reduced-motion…)">` 와 `<link … media="(prefers-reduced-motion…)">` 도 쪽 안 움직임 규칙으로 잡는다. `media="print"` 같은 다른 조건은 잡지 않는다. 시험 경우 7 을 더한다(스크립트-01). 봉인 전 실측: 지금 검사는 두 모양 모두 종료 코드 0(결함 재현).
- **(6) api-kit 문서 검사 연결 규칙** — `scripts/check-api-kit-docs.py` 의 공통 CSS 연결 판정이 `rel` 에 `stylesheet` 가 있고 주소가 `assets/site.css` 로 끝나는(닫는 따옴표 · 공백 · `>` 가 바로 뒤) `<link>` 만 센다. 시험 파일 `scripts/test-check-api-kit-docs.py` 를 새로 만들어 CI 에 등록한다(스크립트-02). 봉인 전 실측: 지금 정규식은 `rel="preload"` 와 `site.css.bak` 을 연결로 센다.
- **(7) 테마 단추** — 두 테마인데 단추가 없는 쪽은 접근성 검사기 `btn=none` 여섯 줄, 모두 `docs/howto-kit/` 의 `branch-catalog` · `changelog-feeds` · `deep-links` · `deprecation-policy` · `procedure-standards` · `ui-anchoring` 이다. 여섯 쪽 모두 `.theme-toggle` 스타일과 `toggleTheme()` · `dk-theme` 저장 스크립트는 있고 단추 요소만 없다 — 같은 폴더 `overview.html` 의 단추 모양대로 `id="theme-btn"` 단추를 넣는다(구조-03 · 구조-04).
- **(8) 스크립트 움직임** — 공통 스크립트 파일이 없다(`docs/assets/` 에는 `site.css` 하나). 그래서 쪽에서 `matchMedia('(prefers-reduced-motion: reduce)')` 로 멈춘다. 대상은 추적 쪽 `<script>` 를 전부 훑어(`behavior:'smooth'` · 스스로 다시 부르는 `requestAnimationFrame` · `setInterval`) 줄이기 확인이 없는 되풀이 움직임 셋이다: `docs/design-kit/animation.html` 스프링 공(`#springBall` 위치를 프레임마다 바꿈) · 같은 쪽 깜빡임 상자(`#flashBox` 투명도를 타이머로 바꿈) · `docs/design-kit/data-display.html` 진행 막대(`#progressBar` 폭을 타이머로 바꿈). 이미 막은 것: `docs/process/kaizen-flow.html` 부드러운 스크롤 · `animation.html` Rive 표본 · `microinteraction.html` 진행 표본. 대상 밖(이유): `docs/index.html` 의 `scrollIntoView({block:'nearest'})` 는 부드러운 스크롤이 아니고, `iconography.html` 타이머는 숫자를 세는 글자라 움직임이 아니며, 한 번만 도는 `setTimeout` · 한 번짜리 `requestAnimationFrame` 은 CSS 전환을 켜는 것이라 공통 파일이 0.01ms 로 줄인다. 줄이기 설정에서는 끝 상태를 바로 보이고, 허용 설정의 움직임은 그대로다(오류-01 · 오류-02).
- **(9) 쪽 없는 원본 둘** — `reflect-kit/references/memory-grounding.md` → `docs/reflect-kit/memory-grounding.html`, `reflect-kit/skills/reflect-kaizen/SKILL.md` → `docs/reflect-kit/reflect-kaizen.html`. 드리프트 매핑은 이미 접두 `reflect-kit/skills/` · `reflect-kit/references/` 로 두 원본을 잡고(`[NEW` 표지로 나옴), docs-site Step 1 표에도 두 접두가 있다 — 연결표는 이미 됨. 쪽을 만들고 `docs/index.html` 에 올린다(구조-05).
- **(10) 드리프트 다시 보기** — `python3 scripts/detect-docs-drift.py --since cacd9da3` 의 짝 가운데 원본이 새로 얻은 낱말을 쪽이 못 싣는 짝이 둘이다: `docs/planning-kit/prd-patterns.html`(낱말 24/94 빠짐) · `docs/onboarding-kit/setup-guide.html`(낱말 76/152 빠짐). nr 은 인용 · 새 표지만 쟀다. 이 두 쪽을 맞추고, 이번 묶음이 바꾸는 `docs/planning/flows.md` 짝과 `harness/docs/guides/contract-design-guide.md` 짝(12)이 더해져 짝은 열하나가 된다(구조-06).
- **(11) 계약 스킬 Gotcha** — `harness/skills/sprint-contract/SKILL.md` Gotchas 끝에 한 줄: 여러 파일을 한꺼번에 바꾸는 조건이면 봉인 전에 그 글자 · 파일을 읽는 기존 검사 스크립트를 `grep` 으로 찾아 구현 뒤 모양의 사본에서 돌려 보고, 「더하라」 조건과 「그대로」 조건이 겨누는 파일 겹침을 뽑는다(스킬-01). 이 원본에는 대응 쪽이 없다(드리프트 매핑 `None`).
- **(12) 범위 목록 × CI 전용 단계 점검** — 교차 진단이 짚은 빠진 항목. fs2 QA 2 · 3 회차 리포트가 같은 제안을 두 번 했다(`.harness/sprint-feedback-after-0929-final-sweep-docs.md:170`): 「CI 에만 있는 단계 목록과 `# sprint-scope` 목록 교차 대조를 `harness/docs/guides/contract-design-guide.md` 에 체크리스트 항목으로 명시」. (11) 은 바뀌는 글자를 읽는 검사를 찾는 규칙이고, 이 항목은 CI 파일에만 있는 단계가 부르는 스크립트가 범위 목록 밖이라 고칠 길이 없는 경우를 막는 점검이다 — 다른 규칙이다. 가이드 `### 스코프 범위 인라인 명시` 절 뒤에 `### 범위 목록과 CI 전용 단계 맞대기 (2026-09-29 추가)` 절을 새로 두고(번호 점검 단계 · fs2 실측 · `contract_ambiguity_notes` 승격 근거), 쪽 `docs/harness/contract-design-guide.html` 같은 자리에 같은 절을 싣는다(구조-11). 가이드 `version` · `last_updated` 는 올리지 않는다 — 올리면 `qa-evaluation-guide.md` §버전 정보 Parity 도 같이 올려야 해서 범위가 커진다. 다른 추가 절과 같이 제목의 `(2026-09-29 추가)` 표시로 남긴다. `contract_ambiguity_notes` 에 적는 것은 평가자 피드백의 몫이라 이번 변경이 아니다.

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 스킬 원본(setup-guide · sprint-contract) · 계약 설계 가이드, 연구 문서(`docs/planning/`), 문서 쪽 HTML · 쪽 스크립트 · 목차, CI 검사 스크립트 · CI 파일 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 두 검사 스크립트의 판정 규칙이 바뀌고, 계약 스킬 · setup-guide 스킬이 사용자에게 새 확인을 요구한다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 원본마다 짝 쪽(드리프트 매핑), 검사마다 시험 파일 · CI 단계, nr · fs2 의 봉인된 측정(오류-03) |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 검사를 조이면 추적 쪽이 걸릴 수 있고, 스크립트 움직임을 막다 허용 설정의 표본까지 멈출 수 있으며, Gotcha 10 · Phase 4 를 고치면 nr 측정이 깨질 수 있다 |

기능 조건 20 개는 스킬-01 ~ 스킬-03 · 스크립트-01 · 스크립트-02 · 오류-01 ~ 오류-03 · 구조-01 ~ 구조-11 · 진단-05 다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절 · 자동 포함 여섯 줄 · `N/A (` 줄을 빼고 센 값이다. 복잡 가이드 9 ~ 20 안이다.

Step 2.5 짝 조건: 원본을 바꾸는 조건(스킬-02 · 스킬-03 · 구조-01 · 구조-02 · 구조-11)은 짝 쪽을 같은 조건 안에서 따로 재고, 드리프트 전체를 구조-06 이 잰다. 검사를 바꾸는 조건(스크립트-01 · 스크립트-02)은 시험 파일 · CI 등록 · 추적 쪽 전부 통과를 함께 잰다. 쓰는 쪽인 nr · fs2 측정은 오류-03, CI 는 진단-05 가 잰다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | 진단-01 N/A (대상 파일이 이번 변경 밖) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 진단-03 N/A (같은 이유) |
| `diagnostics.ide_exclude` | `[]` | 진단-02 `[]` |
| `contract_categories[].id` / `prefix` | Skill/스킬 · Script/스크립트 · Error/오류 · Architecture/구조 | 같음 |
| `anti_patterns[].id` / `message` | 금지-01 버전 하드코딩 · 금지-02 force push · 금지-03 bare code fence · 금지-04 frontmatter name | 금지-02 · 금지-03 |

## GAP 분석 (Pre-Edit Audit)

모두 W 시작 판(`ab637374`)에서 연 값이다.

| 대상 | 읽은 증거 (`파일:줄` · 명령 출력) | 발견한 갭 | 조건 |
| --- | --- | --- | --- |
| `docs/planning/prd-patterns.md` · `docs/planning-kit/prd-patterns.html` | `prd-patterns.md:4` `last_updated: 2026-09-25`, 쪽 `:311` `last_updated 2026-09-25` · `:1011` `last updated 2026-09-25`. `git log -- docs/planning/prd-patterns.md` 끝 `d6fe28e3 2026-09-29` | 내용을 바꾼 날과 머리 날짜가 어긋남 | 구조-01 |
| `onboarding-kit/skills/setup-guide/SKILL.md` Gotcha 10 | `:283-287` `1. ①` ~ `5. ⑤`. `m 스킬-02` → `doubled=5 marks=` | 번호와 ①~⑤ 이 겹쳐 「1. ①」 로 그려짐 | 스킬-02 |
| 같은 파일 Phase 4 · 쪽 Phase 4 | 원본 `:345-353` 단계 7 개, 쪽 `:505-515` `<ol>` 7 개 · 끝 체크리스트 `:595` · `:603` 에 두 확인. `m 스킬-03` → `skill_steps=7 page_steps=7 skill_date=0 skill_sa=0 page_date=0 page_sa=0` | 원본 · 쪽 Phase 4 에 두 확인 없음 | 스킬-03 |
| `docs/planning/flows.md` · 쪽 | `flows.md:61` 「2026-09-24 에 확인한 Mermaid 최신 안정판은 12.0.0 …」, 쪽 `:297` · `:458` · `:462` · `:472` · `:473` · `:923` 「최신 안정판」 여섯 자리. `ex/A10.md` §3 교체안. `m 구조-02` → `md_lines=0 … stale_md=1 stale_page=6` | 원문 인용이 아닌 「최신 안정판」 | 구조-02 |
| `scripts/check-docs-common-css.py` · 시험 | `:34` `STYLE_RE` 가 `<style>` 안 글만 보고 `:57-60` 태그 속성은 안 봄. scratch 쪽 `style-media.html` · `link-media.html` → 둘 다 종료 코드 0. 시험 `경우 6 개 중 통과 6` | media 속성 모양을 못 잡음 | 스크립트-01 |
| `scripts/check-api-kit-docs.py` | `:49` `SITE_CSS_LINK` — `rel` 을 안 보고 끝이 `\b`. 봉인 전 실측: `rel="preload"` → 셈, `site.css.bak` → 셈, `site.cssx` → 안 셈. 시험 파일 없음. `12/12 PASS` | 느슨한 연결 판정, 시험 없음 | 스크립트-02 |
| howto-kit 여섯 쪽 | 접근성 검사기 전체 실행 `btn=none` 6 줄. `docs/howto-kit/branch-catalog.html:47-55` `.theme-toggle` 스타일, `:387-407` `applyTheme` · `toggleTheme` · `dk-theme`, 단추 요소 0. `overview.html` 은 단추 1. `m 구조-03` → `theme_ok=0/6` (모두 `click=none btn=none`) | 단추만 없음 | 구조-03 · 구조-04 |
| 쪽 스크립트 움직임 | 추적 쪽 `<script>` 훑기(주석 뺌): `behavior` smooth 1 곳(`docs/process/kaizen-flow.html`, 줄이기 확인 있음) · `requestAnimationFrame` 3 쪽 · `setInterval` 5 쪽. 확인 없는 되풀이 셋 — `docs/design-kit/animation.html:889-904` 스프링 · `:1063` 깜빡임 · `docs/design-kit/data-display.html:859` 진행 막대. `m 오류-01` → 셋 모두 `changes` 2 ~ 4 | 줄이기 설정에서도 움직임 | 오류-01 · 오류-02 |
| reflect-kit 쪽 없는 원본 | `detect-docs-drift.py --since ca2181b2 --include-format-only` 에 `[NEW` 2 줄. `docs/reflect-kit/` 쪽 7 개, 목차 `docs/index.html:537-543` 에 두 쪽 없음. 원본 106 줄 · 210 줄 | 쪽 · 목차 없음 | 구조-05 |
| 드리프트 `--since cacd9da3` | 짝 9 개 · 종료 코드 0 (flows · 계약 설계 가이드는 이번에 바뀌어 짝에 들어온다). `m 구조-06` → GAP 2 (`prd-patterns.html` 낱말 24/94 · `setup-guide.html` 76/152) | 두 쪽이 원본 새 낱말을 못 실음 | 구조-06 |
| `harness/skills/sprint-contract/SKILL.md` | `:32-79` Gotchas 46 줄, 기존 검사 대조 줄 없음. `m 스킬-01` → `line_hits=0` | 규칙 없음 | 스킬-01 |
| `harness/docs/guides/contract-design-guide.md` · 쪽 | `grep -c 'sprint-scope' harness/docs/guides/contract-design-guide.md` → 0, `### 스코프 범위 인라인 명시` 절 `:484-519`, 쪽 같은 절 `:750-775`. fs2 피드백 `:170` 이 2 · 3 회차 연속 같은 제안. `m 구조-11` → `md_heads=0 … page_keys_ok=0` | 범위 목록 × CI 전용 단계 점검이 가이드에 없음 | 구조-11 |
| 앞 묶음 측정 | nr 열 개 · fs2 `오류-01` 모두 종료 코드 0 (`m 오류-03` → `runs=11 bad=0`) | 통과 중 — 지켜야 함 | 오류-03 |
| 로컬 CI · CI 전용 단계 | `## 회귀 게이트` 봉인 전 실측 | 통과 중 | 진단-05 |

## Skill

- [ ] 스킬-01: 계약 스킬 Gotchas 에 봉인 전 기존 검사 대조 규칙이 한 줄 있다 — `harness/skills/sprint-contract/SKILL.md` 의 `## Gotchas` 절(다음 두 단계 제목 앞까지)에서 대시 목록 항목 줄 가운데 `봉인 전` · `grep` · `사본` · `「더하라」` · `「그대로」` · `겹침` 여섯 글자를 모두 담은 줄이 정확히 하나다. Given 공통 전제 G, When `m 스킬-01`, Then `line_hits=1 hit_count=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-01`. 시작 판 `line_hits=0 hit_count=0 keys=6` · 종료 코드 1. 봉인 전 사본 대조: 이 줄을 더한 scratch 사본에서 `m 스킬-01` 종료 코드 0, `python3 scripts/validate-plugin.py harness` 종료 코드 0(`$` + 숫자 검사 포함), `python3 scripts/run-kaizen-assertions.py` `14 passed, 0 failed`
- [ ] 스킬-02: Gotcha 10 목록에 번호와 ①~⑤ 가 겹치지 않는다 — `onboarding-kit/skills/setup-guide/SKILL.md` 의 `### Gotcha 10:` 절에서 숫자 번호 뒤에 ①~⑤ 가 붙은 줄이 0 이고, `- ①` ~ `- ⑤` 로 시작하는 줄이 그 차례로 다섯이다. 쪽 `docs/onboarding-kit/setup-guide.html` Gotcha 10 칸은 시작 판에서 이미 ①~⑤ 만 쓴다(`:383`). Given 공통 전제 G, When `m 스킬-02`, Then `doubled_zero=1 doubled=0 bullet_marks_in_order=1 marks=①②③④⑤` · 종료 코드 0 [exact]
  측정: `m 스킬-02`. 시작 판 `doubled_zero=0 doubled=5 bullet_marks_in_order=0 marks=` · 종료 코드 1 (양성 대조 겸함 — 0 기대 값이 시작 판에서 5 를 낸다)
- [ ] 스킬-03: setup-guide 완료 단계가 두 규칙을 확인한다 — 원본 `onboarding-kit/skills/setup-guide/SKILL.md` 의 `### Phase 4:` 번호 단계 가운데 `조회일` 과 `Last updated` 를 함께 담은 단계가 정확히 하나, `서비스 계정 키` · `대안` · `Gotcha 10` 을 함께 담은 단계가 정확히 하나이고, 쪽 `docs/onboarding-kit/setup-guide.html` 의 Phase 4 `<ol>` 항목도 같은 수이며 같은 두 조건을 만족하는 항목이 각각 하나다. Given 공통 전제 G, When `m 스킬-03`, Then `same_count=1 skill_date=1 skill_sa=1 page_date=1 page_sa=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-03`. 시작 판 `skill_steps=7 page_steps=7 same_count=1 skill_date=0 skill_sa=0 page_date=0 page_sa=0` · 종료 코드 1. 봉인 전 사본 대조: 두 단계를 원본 · 쪽에 넣은 scratch 사본 → `skill_steps=9 page_steps=9 … page_sa=1` · 종료 코드 0

## Script

- [ ] 스크립트-01: 공통 CSS 검사가 태그 media 속성의 움직임 줄이기도 잡는다 — `scripts/check-docs-common-css.py` 가 `<style media="(prefers-reduced-motion: reduce)">` 인 쪽과 `<link rel="stylesheet" media="(prefers-reduced-motion: reduce)" href="…">` 인 쪽을 어긋난 쪽으로 적고, `media="print"` 인 `<style>` · `<link>` 만 있는 쪽은 통과시킨다. 이 세 쪽이 `scripts/test-check-docs-common-css.py` 의 새 경우 7 이다: ① style media 쪽 → 종료 코드 1 · 그 쪽 이름 적힘 ② link media 쪽 → 종료 코드 1 · 그 쪽 이름 적힘 ③ print media 쪽 → 종료 코드 0. Given 공통 전제 G, When 아래 측정, Then 시험 종료 코드 0 · 끝 줄 `경우 7 개 중 통과 7`, 검사 종료 코드 0 · 끝 줄 `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0` [exact, enumerated]
  측정: `python3 scripts/test-check-docs-common-css.py; echo $?` 와 `python3 scripts/check-docs-common-css.py; echo $?`, 그리고 `grep -c 'scripts/test-check-docs-common-css.py' .github/workflows/ci.yml` 이 1 이상(이미 등록됨). 시작 판: 시험 `경우 6 개 중 통과 6`, 검사 `검사한 쪽 204 · 어긋난 쪽 0 · 못 읽은 쪽 0`, 결함 재현 — scratch 쪽 `style-media.html` · `link-media.html` · `print-media.html` 을 지금 검사로 부르면 셋 다 종료 코드 0 (봉인 전 실측). 추적 쪽 가운데 `<style` · `<link` 에 `media=` 가 있는 쪽 0 (`git grep -nE '<(style|link)[^>]*media=' -- 'docs/*.html'` 빈 출력) — 조인 검사에 걸릴 기존 쪽이 없다
  음성 대조(준비 단계 봉인 전 실측 — 사본 추출 · 지금 시험에 `--check <사본>` 이 `경우 6 개 중 통과 6`): 시작 판 검사 사본(`git show ab637374:scripts/check-docs-common-css.py`)을 `python3 scripts/test-check-docs-common-css.py --check <사본>` 으로 부르면 경우 7 ① ② 가 실패해 종료 코드가 0 이 아니다. 새 검사에서 media 속성 보기만 지운 사본도 같다
- [ ] 스크립트-02: api-kit 문서 검사가 공통 CSS 연결을 정확히 센다 — `scripts/check-api-kit-docs.py` 는 `rel` 값에 `stylesheet` 가 있고 `href` 가 `assets/site.css` 에서 끝나는(바로 뒤가 닫는 따옴표 · 공백 · `>`) `<link>` 만 연결로 센다. 새 시험 `scripts/test-check-api-kit-docs.py` 가 검사 파일을 불러 임시 폴더의 원본 · 쪽 짝으로 다섯 경우를 돌린다: ① `<link rel="stylesheet" href="../assets/site.css">` → 연결 있음 ② `<link href='../assets/site.css' rel=stylesheet>` → 연결 있음 ③ `<link rel="preload" as="style" href="../assets/site.css">` 만 → 연결 없음 ④ `<link rel="stylesheet" href="../assets/site.css.bak">` 만 → 연결 없음 ⑤ 연결이 HTML 주석 안에만 → 연결 없음. 시험은 `--check <검사 사본>` 을 받고, `.github/workflows/ci.yml` 에 `run: python3 scripts/test-check-api-kit-docs.py` 줄이 정확히 하나다. Given 공통 전제 G, When 아래 측정, Then 시험 종료 코드 0 · 끝 줄 `경우 5 개 중 통과 5`, 검사 종료 코드 0 · 끝 줄 `12/12 PASS`, CI 줄 수 1 [exact, enumerated]
  측정: `python3 scripts/test-check-api-kit-docs.py; echo $?` · `python3 scripts/check-api-kit-docs.py; echo $?` · `grep -c 'run: python3 scripts/test-check-api-kit-docs.py' .github/workflows/ci.yml`. 시작 판: 시험 파일 없음, 검사 `12/12 PASS` · 종료 코드 0, CI 줄 0. 결함 재현(봉인 전 실측): 지금 `SITE_CSS_LINK` 에 ① ② ③ ④ 를 대면 `True True True True`, `site.cssx` 는 `False`. api-kit 쪽 12 개의 연결은 모두 `<link rel="stylesheet" href="../assets/site.css">` 13 줄 — 조인 규칙에 걸릴 기존 쪽이 없다
  음성 대조: 시작 판 검사 사본(`git show ab637374:scripts/check-api-kit-docs.py`)을 `--check <사본>` 으로 주면 ③ ④ 가 실패해 종료 코드가 0 이 아니다. 알려진 답: 다섯 경우의 기대는 손으로 정한 위 값이다

## Error

- [ ] 오류-01: 움직임 줄이기 설정에서 스크립트 움직임 셋이 멈춘다 — 브라우저 움직임 줄이기 설정(`reducedMotion: 'reduce'`)으로 표본을 켠 뒤 60 · 150 · 300 · 450 · 600 · 800 · 1000 · 1200ms 에 잰 값이 모두 같다: `docs/design-kit/animation.html` 재생 단추를 누른 뒤 `#springBall` 의 `left`, 같은 쪽 `#flashSlider` 를 2 로 바꾼 뒤 `#flashBox` 의 `opacity`, `docs/design-kit/data-display.html` 진행 막대 단추를 누른 뒤 `#progressBar` 의 `width`. Given 공통 전제 G, When `m 오류-01`, Then 세 줄 `changes=0` · `targets=3 moving=0 jsm_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01` (`node .harness/.meta/after-0929-leftovers/jsmotion.js reduce`). 시작 판 `spring changes=2 ~ 3 · flash changes=4 · progress changes=4` · `targets=3 moving=3` · 종료 코드 1 (같은 측정을 세 번 돌려 셋 모두 매번 움직임을 냈다. 스프링 값은 브라우저 시각에 따라 2 와 3 으로 갈린다 — 판정은 0 인지만 본다)
  알려진 답: 시작 판 scratch 사본에서 스프링을 목표 위치로 바로 옮기고 · 깜빡임 타이머를 켜지 않고 · 진행 막대를 100% 로 바로 채운 사본(`JSM_ROOT=<사본>`)은 세 줄 모두 `changes=0` (봉인 전 실측 — 측정이 0 을 낼 수 있다)
- [ ] 오류-02: 움직임 허용 설정의 표본은 그대로 움직인다 — 오류-01 과 같은 셋을 허용 설정(`reducedMotion: 'no-preference'`)으로 재면 셋 모두 `changes` 가 1 이상이다. Given 공통 전제 G, When `m 오류-02`, Then `targets=3 moving=3 jsm_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02`. 시작 판 `targets=3 moving=3 jsm_rc=0` · 종료 코드 0. 양성 대조: 오류-01 의 알려진 답 사본(줄이기 확인 없이 멈춘 사본)은 허용 설정에서도 `changes=0` 이라 이 조건이 FAIL 한다 — 조건 없이 움직임을 지운 구현을 잡는다 (봉인 전 실측: 세 줄 `changes=0`)
- [ ] 오류-03: 앞 묶음 측정이 이 판에서도 통과한다 — nr 측정 `.harness/.meta/after-0929-four-new-rules/measure.py` 의 `스킬-01` · `스킬-02` · `스킬-03` · `스킬-04` · `구조-01` · `구조-02` · `구조-03` · `구조-04` · `오류-01` · `오류-02` 열 개와 fs2 측정 `.harness/.meta/after-0929-final-sweep-docs/measure.py` 의 `오류-01`(추적 쪽 전부 움직임 줄이기) 하나가 모두 종료 코드 0 이다. Given 공통 전제 G, When `m 오류-03`, Then 열한 줄 `OK` · `runs=11 bad=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-03`. 시작 판 `runs=11 bad=0` · 종료 코드 0. 봉인 전 사본 대조: 스킬-02 · 스킬-03 · 구조-01 모양으로 고친 scratch 사본에서 nr 열 개 모두 종료 코드 0 (「더하라」 조건 스킬-02 · 스킬-03 · 구조-01 · 구조-06 과 「그대로」 조건 오류-03 이 함께 겨누는 파일 `onboarding-kit/skills/setup-guide/SKILL.md` · `docs/onboarding-kit/setup-guide.html` · `docs/planning/prd-patterns.md` · `docs/planning-kit/prd-patterns.html` 에서 부딪히지 않는다)

## Architecture

- [ ] 구조-01: prd-patterns 날짜 — `docs/planning/prd-patterns.md` 머리 `last_updated` 와 `docs/planning-kit/prd-patterns.html` 의 `last_updated …` · `last updated …` 날짜가 모두 `2026-09-29` 하나씩이다. Given 공통 전제 G, When `m 구조-01`, Then `md=2026-09-29 page_meta=2026-09-29 page_foot=2026-09-29 ok=1` · 종료 코드 0 [exact]
  측정: `m 구조-01`. 시작 판 `md=2026-09-25 page_meta=2026-09-25 page_foot=2026-09-25 ok=0` · 종료 코드 1
- [ ] 구조-02: flows Mermaid 문장 — `docs/planning/flows.md` 에 `아래 예시는 Mermaid 공식 flowchart 문법을 따른다` 로 시작하는 줄이 정확히 하나이고 그 줄에 `12.0.0` · `2026-09-10` · `비시험판` · `2026-09-28` · `registry.npmjs.org/mermaid/latest` · `releases/tag/mermaid%4012.0.0` · `렌더해 확인하지 않았다` 가 모두 있으며, `docs/planning-kit/flows.html` 의 보이는 글과 링크 주소에도 일곱이 모두 있고, 원본 · 쪽 모두 `최신 안정판` 이 0 이며, 원본 `last_updated` 와 쪽 두 날짜가 `docs/planning/flows.md` 를 마지막으로 바꾼 커밋 날(`git log -1 --format=%ad --date=short -- docs/planning/flows.md`)과 같다. Given 공통 전제 G, When `m 구조-02`, Then `md_keys_ok=1 page_keys_ok=1 stale_md=0 stale_page=0 no_stale=1 dates_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02`. 시작 판 `md_lines=0 md_keys_ok=0 … page_miss=['비시험판', '렌더해 확인하지 않았다'] stale_md=1 stale_page=6 no_stale=0 dates=2026-09-28/2026-09-28/2026-09-28/2026-09-28 dates_ok=1` · 종료 코드 1
- [ ] 구조-03: howto-kit 여섯 쪽 테마 단추 — `docs/howto-kit/branch-catalog.html` · `docs/howto-kit/changelog-feeds.html` · `docs/howto-kit/deep-links.html` · `docs/howto-kit/deprecation-policy.html` · `docs/howto-kit/procedure-standards.html` · `docs/howto-kit/ui-anchoring.html` 마다: 저장값 없이 밝은 색 설정으로 열면 `<html data-theme>` 이 `light`, 어두운 설정이면 `dark`, 어두운 설정에서 단추(`#theme-btn` 또는 `#themeToggle`)를 누르면 `light` 로 바뀌고 `localStorage` 의 `dk-theme` 이 `light` 이며 다시 열어도 `light`, 누르기 전후 본문 배경색이 다르고, 단추 가로 · 세로가 44 이상이다. Given 공통 전제 G, When `m 구조-03`, Then 여섯 줄 `OK` · `theme_ok=6/6 br_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03` (fs2 `br.js theme`). 시작 판 여섯 쪽 모두 `first_light=light first_dark=dark click=none stored=none reload=none bg_differs=0 btn=none` · `theme_ok=0/6 br_rc=0` · 종료 코드 1
- [ ] 구조-04: 접근성 검사기를 docs 전체에 돌리면 모든 줄이 `OK` 이고 `theme=both` 이며 `btn=none` 줄이 0 이고 끝 줄이 `206/206 PASS` 다. Given 공통 전제 G, When `m 구조-04`, Then `rows=206 fail=0 theme_both=206 btn_none=0 tracked=206 tail=[206/206 PASS] rc=0` · 종료 코드 0 [exact]
  측정: `m 구조-04` (`node scripts/check-docs-a11y.js` 인자 없이). 시작 판 `rows=204 fail=0 theme_both=204 btn_none=6 tracked=204 tail=[204/204 PASS] rc=0` · 종료 코드 1 (양성 대조 겸함 — `btn_none` 0 기대가 시작 판에서 6 을 낸다)
- [ ] 구조-05: reflect-kit 새 쪽 둘 — `docs/reflect-kit/memory-grounding.html`(원본 `reflect-kit/references/memory-grounding.md`) · `docs/reflect-kit/reflect-kaizen.html`(원본 `reflect-kit/skills/reflect-kaizen/SKILL.md`)마다 쪽 줄 수(`\n` 수) 400 이상(docs-site Gotcha 8), `docs/index.html` 에 그 쪽 `file:` 항목이 정확히 하나이고 그 id 가 목차 전체에서 하나뿐이며 `getIcon` 에 같은 id 아이콘이 있고, `assets/site.css` 링크가 하나다. 원본 담김은 낱말 비율 0.95 이상 · 인라인 코드 전부 · 코드 블록 줄(공백 뺀 8 글자 이상) 전부다. 그리고 `python3 scripts/detect-docs-drift.py --since ca2181b2 --include-format-only` 출력에 `[NEW` 줄이 0 이다. Given 공통 전제 G, When `m 구조-05`, Then 두 줄 `OK` · `new_pages_ok=2/2 nopage=0 drift_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-05` (원본 담김 세기는 fs2 도우미 `cov` 그대로). 시작 판 두 쪽 `MISSING` · `NOPAGE reflect-kit/references/memory-grounding.md` · `NOPAGE reflect-kit/skills/reflect-kaizen/SKILL.md` · `new_pages_ok=0/2 nopage=2 drift_rc=0` · 종료 코드 1 (양성 대조 겸함)
- [ ] 구조-06: 드리프트 다시 보기 — `python3 scripts/detect-docs-drift.py --since cacd9da3` 기본 출력의 원본이 정확히 열한 개 `bambu-kit/skills/bambu-print-profile/SKILL.md` · `design-kit/skills/design-mockup/SKILL.md` · `docs/backend/fundamentals/database.md` · `docs/planning/flows.md` · `docs/planning/prd-patterns.md` · `harness/docs/guides/skill-design-guide.md` · `harness/references/contract-schema.md` · `onboarding-kit/skills/setup-guide/SKILL.md` · `onboarding-kit/skills/setup-guide/references/format-checklist.md` · `onboarding-kit/skills/setup-guide/references/search-strategy.md` · `harness/docs/guides/contract-design-guide.md` 이고, 짝마다 쪽이 있고 `[NEW` 표지가 없으며, 원본이 `cacd9da3` 뒤에 새로 얻은 인라인 코드 · 낱말(fs2 도우미 `codes` · `words` 와 같은 세기)이 모두 쪽의 보이는 글이나 링크 주소에 있다. Given 공통 전제 G, When `m 구조-06`, Then `pairs=11 bad=0 same_set=1 extra=[] lack=[] drift_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-06`. 시작 판 `pairs=9 bad=2 same_set=0 extra=[] lack=['docs/planning/flows.md', 'harness/docs/guides/contract-design-guide.md'] drift_rc=0` · 종료 코드 1 (GAP 두 줄: `docs/planning-kit/prd-patterns.html word_miss=24/94` · `docs/onboarding-kit/setup-guide.html word_miss=76/152` — 양성 대조 겸함)
- [ ] 구조-07: 이번에 바뀌거나 새로 생긴 docs 쪽(`git diff --name-only ab637374..HEAD -- docs` 의 `.html`)이 두 테마(`dark` · `light`) 각각 320 · 375 · 1280 폭에서 가로 넘침 0 이다. Given 공통 전제 G, When `m 구조-07`, Then `pages` 1 이상 · `bad=0 br_rc=0,0` · 종료 코드 0 [exact]
  측정: `m 구조-07` (fs2 `br.js paint`). 시작 판 `pages=0 themes=2 bad=0 br_rc=0,0` · 종료 코드 1 (바뀐 쪽 없음). 양성 대조: `docs/howto-kit/branch-catalog.html` 의 `<body>` 바로 뒤에 폭 2000px 상자를 넣은 scratch 사본 → 두 테마 모두 `of=1680/1625/720`, 원본은 `0/0/0` (봉인 전 실측)
- [ ] 구조-08: 기록 — `.harness/.meta/after-kaizen-0928/rest-notes.md` 에 열한 항목 낱말 `prd-patterns` · `Gotcha 10` · `Phase 4` · `flows.md` · `check-docs-common-css` · `check-api-kit-docs` · `테마 단추` · `matchMedia` · `memory-grounding` · `reflect-kaizen` · `드리프트` · `sprint-contract` 와 `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 6 개 이상이 있다. Given 공통 전제 G, When `m 구조-08`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-08`. 시작 판 파일 없음 · 종료 코드 1
- [ ] 구조-09: 바뀌거나 새로 생긴 docs 파일(`.html` · `.css` · `.js`)이 레포 밖 자원을 부르지 않는다 — fs2 구조-10 과 같은 식(`<script>` · `<img>` · `<iframe>` 의 `src`, `<link>` 의 `href`, CSS `@import` · `url()` 에서 `http://` · `https://` · `//` 로 시작하는 주소, 따옴표 세 모양 모두). Given 공통 전제 G, When `m 구조-09`, Then `checked` 1 이상 · `ext_files=0` · 종료 코드 0 [exact]
  측정: `m 구조-09`. 시작 판 `checked=0 ext_files=0 git_rc=0` · 종료 코드 1. 양성 대조는 같은 함수로 fs2 가 봉인 전에 쟀다(`EXT` 세 줄 · `ext_files=3`)
- [ ] 구조-10: 커밋 규칙 — `ab637374..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(문서 사이트는 `docs/<폴더>` 하나 — `docs/planning` 과 `docs/planning-kit` 은 다른 폴더다 — 에 `docs/index.html` 을 더해도 된다)이며, `.harness/` 파일은 구현 파일과 다른 커밋이고, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이며, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-10`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-10` (fs2 `m_commits` 를 이 계약 · 이 기준 판으로). 시작 판 `commits=0` · 종료 코드 1
- [ ] 구조-11: 계약 설계 가이드에 범위 목록 × CI 전용 단계 점검이 있다 — `harness/docs/guides/contract-design-guide.md` 에 `### 범위 목록과 CI 전용 단계 맞대기` 로 시작하는 제목이 정확히 하나이고, 그 절(다음 `## ` · `### ` 제목 앞까지)에 `# sprint-scope` · `.github/workflows/ci.yml` · `run:` · `check-api-kit-docs.py` · `contract_ambiguity_notes` · `봉인 전` 여섯 글자가 모두 있으며 번호 단계 줄(`1. ` 모양)이 3 이상이다. 쪽 `docs/harness/contract-design-guide.html` 의 보이는 글과 링크 주소에 제목 글 `범위 목록과 CI 전용 단계 맞대기` 와 여섯 글자가 모두 있다. Given 공통 전제 G, When `m 구조-11`, Then `md_heads=1 md_head_ok=1 md_miss=[] md_keys_ok=1 md_steps_ok=1 page_miss=[] page_keys_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-11`. 시작 판 `md_heads=0 md_head_ok=0 md_miss=[여섯 모두] md_keys_ok=0 md_steps=0 md_steps_ok=0 page_miss=[제목 글 · 여섯 가운데 봉인 전 뺀 다섯] page_keys_ok=0` · 종료 코드 1 (양성 대조 겸함 — 쪽은 `봉인 전` 을 이미 다른 절에 싣고 있어 제목 글이 가른다). 원본 · 쪽 짝의 새 낱말 전부는 구조-06 이 잰다

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-rest` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 바뀐 `.md` 여섯 파일에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 코드는 시험 파일 하나(`scripts/test-check-api-kit-docs.py`)와 쪽 안 스크립트 몇 줄이다. 시험은 CI 에 등록해 누구나 부른다 — 스크립트-02)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 단추는 같은 쪽의 `.theme-toggle` 스타일 · `toggleTheme()` 과 `overview.html` 단추 모양을 쓰고 — 구조-03, media 모양은 기존 검사 · 기존 시험에 경우를 더하며 — 스크립트-01, 새 시험은 `scripts/test-check-docs-common-css.py` 의 `--check` · 경우 표 모양을 따르고 — 스크립트-02, 측정은 fs2 · nr 도우미를 불러 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only ab637374..chore/ak3-rest | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.md` 여섯 파일(`docs/planning/prd-patterns.md` · `docs/planning/flows.md` · `onboarding-kit/skills/setup-guide/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/docs/guides/contract-design-guide.md` · `.harness/.meta/after-kaizen-0928/rest-notes.md`)은 markdownlint-cli2(MD013 끔)로 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`, 바뀐 `.py` 는 `python3 -m py_compile` 종료 코드 0, 바뀐 `.js` 는 `node --check` 종료 코드 0
  측정: 파일마다 `<scratch>/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/rest/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(설정 파일 내용 `{ "config": { "MD013": false } }`). 시작 판 앞 다섯 파일 모두 `warn=0 ran=1`. 양성 대조: `#bad` 제목과 빈 줄 셋이 든 사본 `pos.md` → 경고 4 (봉인 전 실측)
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 정적 문서 쪽 · 스킬 글 · 검사 스크립트 · CI 파일 · 기록. 측정: git diff --name-only ab637374..HEAD -- . ':(exclude).harness' | grep -cvE '^(docs/|scripts/|\.github/|onboarding-kit/skills/setup-guide/|harness/skills/sprint-contract/|harness/docs/guides/)' 이 0. 쪽을 브라우저로 여는 확인은 구조-03 · 구조-04 · 구조-07 · 오류-01 · 오류-02 · 오류-03 이 한다)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` (TMPDIR 은 scratch 아래 새 폴더)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외)이고 `docs-a11y` 로그 끝이 `206/206 PASS`, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/test-check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-check-docs-common-css.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/check-install-docs-guidance.py` · `python3 scripts/test-check-cause-table-copies.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` 의 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 `grep -c 'rc=0' <TMPDIR>/ci-local/summary.txt`. 시작 판 ci-local 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `204/204 PASS`, CI 전용 단계 모두 종료 코드 0 (`12/12 PASS` · `어긋남 0` · `경우 3 개 중 통과 3` · `검사한 쪽 204 · 어긋난 쪽 0 · 못 읽은 쪽 0` · `경우 6 개 중 통과 6` · `checked=2 violations=0 infra_errors=0` · `need=0` · `실패 0 건` 넷 · `checked=6 violations=0` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0`), `npx playwright test` `174 passed` (봉인 전 실측. `test-check-api-kit-docs.py` 는 구현이 만든다)

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
docs/planning/prd-patterns.md
docs/planning-kit/prd-patterns.html
docs/planning/flows.md
docs/planning-kit/flows.html
onboarding-kit/skills/setup-guide/SKILL.md
docs/onboarding-kit/setup-guide.html
scripts/check-docs-common-css.py
scripts/test-check-docs-common-css.py
scripts/check-api-kit-docs.py
scripts/test-check-api-kit-docs.py
.github/workflows/ci.yml
docs/howto-kit/*.html
docs/design-kit/animation.html
docs/design-kit/data-display.html
docs/reflect-kit/memory-grounding.html
docs/reflect-kit/reflect-kaizen.html
docs/index.html
harness/skills/sprint-contract/SKILL.md
harness/docs/guides/contract-design-guide.md
docs/harness/contract-design-guide.html
```

- 하지 않는 것: 옛 기록(`docs/planning/research-log.md:45` 의 「최신 안정판」 · `docs/backend/research-log.md` · `docs/planning/research-log.md:22`) 고치기 — 그때의 기록이다. `scripts/check-docs-common-css.py` 의 `site.css` 링크 세기(`rel` 을 안 봄)는 fs2 가 남긴 두 항목 밖이라 두고 기록 「남긴 것」 에 적는다. 한 번만 도는 `setTimeout` 움직임(`accessibility.html` 누름 튀김 · `animation.html` 찌그러짐 · 안무 표본 등)은 CSS 전환이라 공통 파일 몫이다. 킷 버전 올리기 · 릴리스 · 합치기 · push, 로컬 CI 도구 `ci-local.sh`(레포 밖) 고치기, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일 고치기.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` 와 `.github/` 는 따로, docs 는 `docs/<폴더>` 별로(`docs/index.html` 은 새 쪽 커밋에 곁들여도 된다). 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0929-leftovers/`)은 따로다.
- 교차 대조(봉인 전): 여러 파일을 한꺼번에 바꾸는 조건(스킬-02 · 스킬-03 · 구조-01 · 구조-02 · 구조-03 · 구조-06)이 건드리는 글자 · 파일을 읽는 기존 검사를 `grep` 으로 찾았다 — `scripts/` · `.github/` 에서 `setup-guide/SKILL.md` · `Gotcha 10` · `Phase 4` · `①` · `last_updated` · `최신 안정판` · `media=` 를 읽는 CI 검사는 없고(`check-stale-values.py` · `check-docs-links.py` 도 해당 글자 0), 봉인된 nr 측정이 같은 두 파일을 읽는다. 구현 뒤 모양의 scratch 사본(`git clone --shared` 뒤 스킬-02 · 스킬-03 · 구조-01 · 스킬-01 모양 편집)에서 nr 열 개 · `validate-plugin.py harness` · `run-kaizen-assertions.py` 모두 종료 코드 0 이었다(오류-03 측정 줄). CI 에만 있는 단계 목록과 이 범위 목록을 맞대면, 이 계약이 바꾸는 검사 둘(`check-docs-common-css.py` · `check-api-kit-docs.py`)과 새 시험 하나가 모두 진단-05 의 CI 전용 목록에 있다. 구조-11 이 바꾸는 가이드를 읽는 검사는 `scripts/check-install-docs-guidance.py`(이 가이드를 면제 목록에 둠)와 `harness/evals/kaizen/contract-kaizen/assertions.json`(`적절히|충분히|잘` 글자 있음) 둘이고, 새 절을 넣은 scratch 사본에서 둘 다 종료 코드 0 이다(아래 봉인 전 실측). CI 단계 가운데 `scripts/` 밖 스크립트(킷 `evals/` 시험들 · `harness/scripts/check-superseded.sh` · `bambu-kit/evals/` 둘)는 이번 변경 파일 이름을 읽지 않는다(`grep` 0). 예외는 `npx playwright test` 가 부르는 `design-kit/evals/visuals.spec.js` 로, `animation.html` 을 연다 — 그 시험은 브라우저 기본 설정(움직임 허용)이라 오류-01 의 줄이기 분기에 닿지 않고, 진단-05 가 통과를 잰다. 범위 밖 스크립트를 고쳐야 하는 경우는 없다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0929-leftovers/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 스크립트 움직임은 같은 폴더 `jsmotion.js`, 테마 · 넘침은 fs2 의 `.harness/.meta/after-0929-final-sweep-docs/br.js` 를 fs2 도우미를 거쳐 부른다.
- 도우미가 쓰는 판: 시작 판 `ab637374` · 드리프트 기준 `cacd9da3` · 쪽 없는 원본 찾기 `ca2181b2`(레포 첫 커밋). 봉인 전 파일 지문(`shasum -a 256 <파일> | cut -c1-16`): `measure.py` `9174c7de7b5cc09f` · `jsmotion.js` `3b69d76a369dae8e` · fs2 `measure.py` `1d53c015d309e924` · fs2 `br.js` `01c706e939a85586` · nr `measure.py` `dbb0a808d4963633`. 봉인 뒤 도우미가 바뀌면 지문이 드러난다.
- 봉인 전 사본 대조(구조-11): 시작 판 scratch 사본에 새 절을 원본 · 쪽에 넣고 커밋하니 `m 구조-11` → `md_heads=1 … md_steps=4 … page_keys_ok=1` · 종료 코드 0, `m 구조-06` 의 가이드 짝 `OK … code_miss=0/6 word_miss=0/58`, `python3 scripts/validate-plugin.py harness` · `python3 scripts/check-install-docs-guidance.py` · `python3 scripts/run-kaizen-assertions.py` · `python3 scripts/check-docs-links.py` · `python3 scripts/check-stale-values.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-docs-common-css.py` 모두 종료 코드 0.
- 수 206 은 시작 판 추적 쪽 204 개에 새 쪽 둘(구조-05)을 더한 값이다. 쪽을 더 만들거나 지우면 스크립트-01 · 구조-04 · 진단-05 의 수가 달라진다.
- 봉인 전 실측(2026-09-29, W 시작 판): 스킬-01 · 스킬-02 · 스킬-03 · 구조-01 · 구조-02 · 구조-03 · 구조-04 · 구조-05 · 구조-06 · 구조-07 · 구조-08 · 구조-09 · 구조-10 · 구조-11 · 오류-01 종료 코드 1(결함 재현 · 산출물 없음), 오류-02 · 오류-03 종료 코드 0(지킬 동작). 값은 각 조건 측정 줄과 `## GAP 분석` 에 있다.
- 커버리지 해소: 스킬-01 — 파일 경로와 여섯 낱말은 도우미 `m_sc_gotcha` 의 `SC_SKILL` · `keys` 에 글자 그대로 있고 `m 스킬-01` 이 잰다. 검출기는 측정 줄의 백틱만 본다.
- 커버리지 해소: 스킬-03 · 구조-03 · 구조-05 · 구조-06 — 파일 · 원본 목록은 도우미 `SKILL` · `SETUP_PAGE` · `BTN_PAGES` · `NEW_PAGES` · `DRIFT_PAIRS` 한 곳에 두고 `m <조건>` 이 줄마다 이름을 찍는다(목록을 두 번 적지 않는다).
- 커버리지 해소: 구조-02 — 두 파일 경로와 일곱 낱말은 도우미 `m_flows` · `FLOW_KEYS` 에 글자 그대로 있고 `m 구조-02` 가 빠진 낱말을 `md_miss` · `page_miss` 로 찍는다.
- 커버리지 해소: 스크립트-01 · 스크립트-02 — 스크립트 · CI 파일은 측정 명령의 인자 자체이고, `<style media=…>` · `assets/site.css` 같은 모양은 시험 경우의 내용 설명이지 따로 재는 파일이 아니다.
- 커버리지 해소: 오류-01 · 오류-02 · 오류-03 — 쪽 · 요소 · 측정 파일 이름은 `jsmotion.js` 의 `TARGETS` 와 도우미 `m_prior` 의 `runs` 에 글자 그대로 있다.
- 커버리지 해소: 구조-11 — 두 파일 경로 · 제목 · 여섯 글자는 도우미 `GUIDE` · `GUIDE_PAGE` · `CI_SCOPE_HEAD` · `CI_SCOPE_KEYS` 에 글자 그대로 있고 `m 구조-11` 이 빠진 글자를 `md_miss` · `page_miss` 로 찍는다.
- 커버리지 해소: 구조-08 — 기록 파일 경로와 낱말 목록은 도우미 `NOTES` · `m_notes` 의 `keys` 에 있다.
- 커버리지 해소: 진단-02 · 진단-05 — 파일 · 명령 목록이 조건 줄 안에 백틱으로 있다. 검출기는 빈칸 든 백틱 덩어리를 건너뛴다.
- 오라클 해소: 스킬-01 · 스킬-02 · 스킬-03 · 구조-08 — 스킬 문서 · 기록에 적는 것 자체가 요구다. 스킬-03 은 원본과 쪽을 함께 재고, 적은 규칙이 실제 동작으로 이어지는지는 onboarding 게이트 시험(`onboarding-gate-evals`, 진단-05)과 nr 측정(오류-03)이 본다.
- 오라클 해소: 스크립트-01 · 스크립트-02 · 진단-05 — 글자 찾기가 아니라 시험 · 검사를 실제로 돌린 종료 코드 · 끝 줄로 판정하고 음성 대조가 붙어 있다. `grep -c … ci.yml` 은 CI 등록 확인일 뿐이다.
- 오라클 해소: 진단-02 — 글자 찾기가 아니라 markdownlint · `py_compile` · `node --check` 를 실행해 그 출력으로 판정하고, 양성 대조(경고 4)를 봉인 전에 쟀다.
- 오라클 해소: 구조-01 · 구조-02 · 구조-11 — 원본 · 쪽 글을 고치는 것 자체가 요구다. 날짜는 커밋 기록에서 뽑은 값과 맞댄다.
