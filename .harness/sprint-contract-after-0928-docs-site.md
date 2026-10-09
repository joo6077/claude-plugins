---
feature: "문서 사이트 약점 — 짝 없는 원본 · 밝은 테마 · 옛 값 · 모양만 바뀐 원본 거르기"
slug: after-0928-docs-site
created: "2026-09-28 12:15"
complexity: "복잡"
conditions: 31
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:496b4785f3dd5d39
measurement_digest: sha256:48cdc97f09055aac
locked_at: "2026-09-28 12:26"
---

## 배경

- 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md` 의 A2 · A3 · B12 · B13 · B14 · B15 · B16 · B17 · D3 · D5 를 한 묶음(d1)으로 처리한다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-d1`, 가지 `chore/ak3-d1`, 시작 판 `BASE` = `e500a63` (가지 `chore/after-kaizen-0928` 끝). 드리프트 비교 기준 `SINCE` = `6378948` (목록 D3 이 쓴 판).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-d1` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력일 때 W 맨 위 폴더에서 잰다. 이 가지는 이 스프린트만 커밋하므로 HEAD 는 이 스프린트 끝과 같다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 ID>` 다.

항목별 처리 방침 (결정):

- **A2 · D5** — 드리프트 도구가 `--since 6378948` 로 「대응 쪽 없음(NEW)」 을 내는 원본 19 개를 결정표(`.harness/.meta/after-kaizen-0926b/dca-notes.md` 「DC-9 매핑 규칙 결정」)대로 처리한다. 짝 다섯(tone core 넷 · codex-kaizen search-sources)은 도구의 덮어쓰기 매핑으로 기존 쪽에 잇고, `tone-kit/references/project-detection.md` 는 「페이지 없음」 으로 도구가 건너뛰게 하고, 새 페이지 아홉(bambu 참고 셋 · figma-parity · cross-kit-principles · react 참고 셋 · reflect-promote)을 만든다. research-log 넷(flutter · planning · rust · tone)은 결정표가 「페이지 없음」 이라 적었지만 사용자 결정 DC-1(2026-09-26T10:30:16.222Z 「일곱 다 · 설계도 현행화」)이 같은 종류인 api 연구 기록을 새 쪽으로 만들게 했고 그 뒤 backend · infra · react 도 쪽이 생겼으므로, 킷마다 다르지 않게 **새 쪽으로 만든다**. 새 쪽은 모두 열셋이다.
  - 교차 진단 반영(방향 근거): 결정표 DC-9 는 dca 서브에이전트가 정한 것이고(커밋 `4bee454`, 2026-09-26 21:10 KST), research-log 행의 근거 「다른 킷도 조사 기록 페이지가 없다」 는 같은 날 앞서 나온 **사용자** 결정 DC-1(2026-09-26T10:30:16.222Z = 19:30 KST)이 api 연구 기록을 새 쪽으로 정한 것과 부딪힌다. 실제로 `docs/api-kit/research-log.html` 은 DC-9 16 분 뒤(`e9b5fc1`, 21:26 KST) DC-1 대로 만들어졌고 backend · infra · react 도 뒤따랐다(`31942a4` · `c95c5fa` · `1fa06a2`). 사용자 결정이 서브에이전트 결정보다 앞서므로 DC-9 의 research-log 행을 틀린 행으로 보고, 이미 있는 넷을 지우는 쪽(내용을 잃음)이 아니라 남은 넷을 만드는 쪽으로 맞춘다. DC-1 의 범위를 노트마다 다르게 적은 것(`decisions.md:17` 은 일곱, 다른 기록은 api 연구 기록 포함)도 D5 표 근거 칸에 적는다. D5 는 결정표가 지금 사실과 어긋난 행(research-log 여덟 · tone adapter 둘 · locale-korean · sources)과 A2 의 열아홉을 한 표로 다시 적어 바로잡는다.
- **D3** — 도구가 「모양만 바뀐 원본」 을 기본으로 빼게 한다. 모양만 바뀜의 정의: 두 판에서 HTML 주석(`<!-- … -->`)을 지우고, 코드 울타리 여는 · 닫는 줄(울타리 뒤 언어 표시 포함)은 한 표지로 바꾼 뒤 낱말(`\w+`) 순서가 같다. 기준 커밋을 기록하는 방식은 쓰지 않는다 — 원본마다 기록 파일을 관리해야 하고, 모양만 바뀐 새 변경이 올 때마다 기록을 다시 적어야 하기 때문이다. 이 정의로 가리면 어느 기준 판으로 불러도 같은 판정이 나온다. 모든 짝을 보고 싶으면 새 선택지 `--include-format-only` 를 준다. 원본 내용이 실제로 바뀐 짝 가운데 쪽이 따라가지 못한 여덟(`## GAP 분석` 표)은 쪽을 다시 맞춘다.
- **A3** — 일곱 쪽에 공통 틀 규칙(`.claude/skills/docs-site/references/page-template.html` · docs-site Gotcha 13)대로 밝은 테마를 넣는다. 단추 id 는 레포 검사기가 재는 `theme-btn` 을 쓴다(dca DC-12 와 같은 선택. 틀의 `themeToggle` 을 검사기가 못 재는 것은 목록 B7 몫이라 여기서 고치지 않는다).
- **B17** — 글자 참조를 지우고 원래 글자로 적는다. 대신 「공통 CSS 링크 하나」 를 글자 수가 아니라 구조로 재는 검사 `scripts/check-docs-common-css.py` 를 새로 두고 CI 에 넣는다: `<link>` 요소 가운데 `assets/site.css` 를 가리키는 것의 수(주석 안 링크는 세지 않음)와, `site.css` · `prefers-reduced-motion` 을 숫자 글자 참조로 쪼갠 자리의 수를 잰다. 본문에 원래 글자로 이름을 적어도 검사는 통과하고, 쪼개 적으면 실패한다. 쪽 `<style>` 안의 움직임 줄이기 규칙은 이 검사가 막지 않는다 — 지금 105 쪽에 남아 있어(`## GAP 분석`) 걸면 CI 가 떨어지고, 그 정리는 이 묶음의 항목이 아니다.
- **B15** — `.feat-card:hover` 의 들뜸을 움직임 줄이기 설정이 아닐 때만 준다.
- **B16** — dr2 가 다시 쓴 쪽 열에 옛 판(`38cccd1`)이 걸던 형제 쪽 링크를 되살리고, react 다섯 쪽에 옛 손 글 절(Bad vs Good · 공통 주의사항)을 지금 스킬에 맞춰 다시 넣는다.

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 정적 문서 화면(HTML · CSS · 쪽 스크립트), 목차(`docs/index.html`), 원본과 쪽을 짝짓는 도구, CI 검사 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 드리프트 도구의 기본 출력이 줄고 선택지가 하나 늘며, 짝이 다섯 바뀐다. 새 CI 검사가 생긴다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 카이젠 Step F2(`.claude/skills/kaizen-orchestrator/SKILL.md:627` · `:632`), `.claude/skills/tone-research/SKILL.md:80`, `--check-table` CI 단계, 목차 화면, 링크 · 고아 검사 `scripts/check-docs-links.py` |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 필터가 내용 바뀐 원본까지 빼면 다시 맞출 쪽을 놓친다. 쪽을 다시 쓰면 원본 내용 · 대비 · 넘침이 깨질 수 있다 |

기능 조건 22 개는 SK-01 · SC-01 ~ SC-06 · ER-01 ~ ER-05 · AR-01 ~ AR-09 · DG-05 다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절 · 자동 포함 여섯 줄 · `N/A (` 줄을 빼고 센 값이다. 복잡 가이드 상한 20 을 둘 넘는다. 나누지 않은 까닭: 부모가 이 열 항목을 한 묶음(d1)으로 맡겼고, 드리프트 도구 · 새 쪽 · 결정 기록(A2 · D3 · D5)이 같은 매핑을 공유해 따로 봉인하면 한쪽 계약의 기대 수(SC-02 · SC-03 · AR-04)가 다른 쪽 커밋에 흔들린다.

Step 2.5 짝 조건: 만드는 쪽은 드리프트 도구(SC-01 ~ SC-04)와 새 검사(SC-05 · SC-06)다. 쓰는 쪽은 docs-site 스킬 표 · 설명(SK-01), CI 파일(SC-04 · SC-05), 목차(AR-01), 기록 표(AR-05)다. 카이젠 Step F2 와 `tone-research` 는 같은 명령을 부르기만 하고 출력 줄 모양(`원본 → 쪽 [표지]`)이 그대로라 고칠 것이 없다 — SC-03 이 `--json` 키와 줄 모양을 함께 잰다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A (대상 파일이 이번 변경 밖) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A (같은 이유) |
| `diagnostics.ide_exclude` | `[]` | DG-02 `[]` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같음 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name | AP-01 · AP-02 · AP-03 |

## GAP 분석 (Pre-Edit Audit)

모두 BASE(`e500a63`) 작업 폴더에서 연 값이다.

| 대상 | 읽은 증거 (`파일:줄` · 명령 출력) | 발견한 갭 | 조건 |
| --- | --- | --- | --- |
| `scripts/detect-docs-drift.py` | `:35-76` 접두 매핑 · `:81-121` 덮어쓰기 매핑 · `:126` `SOURCE_EXCLUDES` · `:224` `changed_files` 가 `git diff --name-only` 만 봄 · `:318-358` 선택지 | 모양만 바뀐 원본을 가르지 못한다. `--since 6378948` → 191 줄 · 종료 코드 0 · NEW 19 (도움 스크립트 `m AR-04` 시작 판 `pairs=191 bad=27`) | SC-01 ~ SC-04 · AR-04 |
| 모양/내용 가름 (도우미 `classify`) | 191 짝의 원본 189 개 가운데 모양만 134 · 내용 55 → 짝으로 모양만 135 · 내용 56. 알려진 답 `m KA` → `caching=SHAPE tone_overview=REAL` (표 구분 줄 · HTML 주석만 바뀐 `docs/rust/data/caching.md` 와 `(_, __)`→`(_, _)` 낱말이 바뀐 `docs/tone/overview.md`) | — | SC-03 |
| 내용 바뀐 짝의 쪽 따라감 (`m AR-04`) | GAP 8: `docs/process/kaizen-flow.html` 낱말 10/120 빠짐 · `docs/bambu-kit/bambu-print-profile.html` 3/48 · `docs/bambu-kit/bambu-fields-baseline.html` 1/9 · `docs/api-kit/multi-sample-pagination-variance.html` 코드 1/1 · 낱말 4/6 · `docs/harness/agent-design-guide.html` 3/64 · `docs/harness/plugin-validation.html` 4/88 · `docs/harness/skill-design-guide.html` 1/163 · `docs/infra-kit/infra-test.html` 1/27. NOPAGE 19 | 쪽이 원본 새 문장을 안 싣는다 | AR-04 |
| `docs/index.html` | `:403` · `:453` · `:499` · `:574` research-log 넷의 id 가 `<킷>-research-log` · `:630` `getIcon` | 새 쪽 열셋 미등록. `research-log` 는 id 가 겹치면 다른 쪽이 열린다 | AR-01 |
| A3 일곱 쪽 | `m AR-02` 시작 판: 일곱 모두 검사기 `theme=dark-only btn=none`, 테마 측정 `first_light=null`(design-test 만 `dark`) `click=none`. 좋은 예 `docs/onboarding-kit/setup-guide.html` 은 `first_light=light first_dark=dark click=light stored=light reload=light bg_differs=1` · `btn=49x44 theme=both` | 밝은 테마 · 단추 · 저장 키 없음 | AR-02 |
| 사이트 전체 테마 | 로컬 CI `docs-a11y` 로그: 189 쪽 가운데 `theme=dark-only` 125 | A3 일곱 밖 118 쪽도 어두운 테마뿐 — 이 묶음의 항목이 아니라 기록(AR-09)에 남은 일로 적는다 | AR-09 |
| B12 `docs/onboarding-kit/search-strategy.html:513` | `guide_gate G1~G4` · 원본 `onboarding-kit/skills/setup-guide/SKILL.md:308` 은 G1 ~ G5 | `m ER-03` → `G1~G4=1 G1~G5=0` | ER-03 |
| B13 bambu 세 쪽 | `failure-recipes.html:164` 머리 표지 `Bambu Studio 2.6.0 (v02.06.00.51)` · `:718` · `:764`, `materials.html:127` 부제 「2.6.0 (v02.06.00.51) 기준」 · `:130` 「Studio 버전은 실행 때 조회한다」 · `:280` · `:463` · `:706`. 원본 `references/failure-recipes.md:5-9` 「런타임에 조회한다 — 하드코딩하지 마라 · Info.plist · BBL.json · 최초 앱 02.06.00.51 / 번들 02.06.00.05 · 2026-09-05 앱 02.08.02.61 / 번들 02.08.00.06」 (세 원본 같은 머리) | `m ER-04` 시작 판: failure-recipes 토큰 여섯 모두 0 · 떠 있는 판 번호 줄 `[164, 718, 764]`, materials `실행 때 조회=1 Info.plist=0 BBL.json=0 02.06.00.05=0 02.08.00.06=0 02.08.02.61=2` · `[127, 280, 463, 706]`, baseline `실행 때 조회=0 Info.plist=0 BBL.json=0 02.06.00.05=0 02.08.00.06=1 02.08.02.61=5` | ER-04 |
| B14 `docs/onboarding-kit/setup-guide.html` | 원본 `SKILL.md:255` 「만들 수 없다고 결론 낼 때도 §3.7 네 칸」 | `m ER-05` → `code=74/82 rule_sentence=0`, 빠진 8: `**출처:**` · `.env.local` · `.env.production` · `/insights` · `/setup-guide firebase analytics` · `com.<앱이름>.app` · `harness/docs/guides/skill-design-guide.md` · `references/project-detection.md` | ER-05 |
| B15 `docs/design-kit/design-test.html:156` | `.feat-card:hover{…transform:translateY(-2px)}` · 공통 파일 `docs/assets/site.css:6-13` 은 전환 시간만 줄인다 | 측정 `node .harness/.meta/after-0928-docs-site/theme.js hover` → `reduce cards=9 transform=matrix(1, 0, 0, 1, 0, -2)` · `no-preference cards=9 transform=matrix(1, 0, 0, 1, 0, -2)` | ER-02 |
| B16 dr2 다시 쓴 쪽 열 | `m AR-03` 시작 판: integration 형제 링크 8 개 · state-data 5 · quality 6 · animation 4 · build-audit 4 · performance 1 · howto overview 6 · feedback-system 3 이 옛 판(`38cccd1`)보다 빠짐. 옛 손 글 절 아홉 없음 | 쪽끼리 길이 끊겼다 | AR-03 |
| B17 세 쪽 | `m ER-01`: `kaizen-flow.html` `charref=1` · `animation.html` 4 · `build-audit.html` 2, 세 쪽 모두 `style_motion=0 site_css_links=1` | 글자 참조로 측정을 비켜 갔다 | ER-01 · SC-05 |
| 공통 CSS 구조 검사 (새로 둘 것) | 도우미 탐침: 추적 쪽 189 개 모두 `assets/site.css` 링크 1 개, 숫자 글자 참조 쪼갬 3 쪽(위 B17), `<style>` 안 `prefers-reduced-motion` 105 쪽 | 링크 수를 글자로 재면 본문 언급이 섞인다 | SC-05 · SC-06 |
| `.claude/skills/docs-site/SKILL.md` | `:45-70` Step 1 표 · 초안 폴더 줄 `:70`. `--include-format-only` · `check-docs-common-css.py` · `글자 참조` · `tone-kit/references/project-detection.md` 모두 0 회. markdownlint(MD013 끔) 0 건 | 새 동작 · 새 검사 · 페이지 없는 원본이 스킬에 없다 | SK-01 |
| `.harness/.meta/after-kaizen-0926b/dca-notes.md` | `:109-162` DC-9 결정표 · `:143-145` · `:147-148` · `:157-159` research-log 「페이지 없음이 맞음」 · `:161` adapter-contract 「페이지 없음」 · `:163` adapter-dart-flutter 「짝」 · `:167` locale-korean 「짝」 · `:169` sources 「페이지 없음」 | 지금 파일과 다르다(D5) | AR-05 |
| 로컬 CI | `ci-local.sh` 시작 판(W) 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `189/189 PASS`. CI 파일에만 있는 단계: `check-api-kit-docs.py` 0 · `detect-docs-drift.py --check-table` 0(「스크립트 45 짝 · 표 34 짝 · 어긋남 0」) · `check-cause-table-copies.py` 0 · `measure-helpers-test.sh` 0 · `run-gate-fixtures.sh` 0(「24 경우 중 불일치 0」) · `makerworld-fetch-test.sh` 0(「5 경우 중 불일치 0」) · `npx playwright test` 0(「164 passed」) | 통과 중 | DG-05 |

커버리지 해소 (Step 6.5 (4) 검출기가 낸 일곱 건):

- 커버리지 해소: SK-01 — 네 글자는 측정 명령의 작은따옴표 인자로 모두 들어 있다(검출기는 백틱만 본다). 파일 경로 `.claude/skills/docs-site/SKILL.md` 도 같은 명령의 인자다.
- 커버리지 해소: SC-06 — 경우 다섯은 새 시험이 돌리고, 측정은 그 시험의 종료 코드와 CI 등록 줄이다. 백틱 토큰(`<code>…</code>` · `scripts/`)은 사본 내용 설명이지 따로 재는 대상이 아니다.
- 커버리지 해소: ER-04 — 토큰 여섯과 판 번호 두 꼴 · 쪽 세 개는 도우미 `m ER-04` 가 그대로 센다(`measure.py` 의 `m_er04` · `ver_lines`).
- 커버리지 해소: AR-01 — 목차 항목 · 아이콘 · `assets/site.css` 링크 수는 `m AR-01` 이 쪽마다 `reg` · `icon` · `site_css` 로 찍는다. 쪽 목록은 측정 줄에 열셋을 모두 적었다.
- 커버리지 해소: AR-02 — `0/0/0/0` · `ok=20/20` 은 기대 출력 값이지 대상이 아니다. 대상 20 쪽은 측정 줄(일곱)과 AR-01 측정 줄(열셋)에 있다.
- 커버리지 해소: AR-03 — `react-kit/skills/` · `docs/react/kit-design/` 는 사람이 대조할 기준이라 기계 측정이 없고, 그 결과는 AR-09 (c) 기록으로 잰다(`## 범위 경계` 셋째 항목).
- 커버리지 해소: AR-05 — `d1-notes.md` 는 `m AR-05` 가, `dca-notes.md` 는 같은 줄의 `grep -c` 가 읽는다(경로가 측정 앞 산문에만 백틱으로 있을 뿐이다). 원본 27 개 목록은 도우미 `NEW_PAGES` · `PAIRS` · `D5_EXTRA` · `NO_PAGE` 한 곳에 둔다(목록을 두 번 적지 않는다). SC-01 의 짝 다섯도 같은 이유로 도우미 `PAIRS` 에 둔다.

## Skill

- [ ] SK-01: docs-site 스킬이 이번 동작을 적는다 — `.claude/skills/docs-site/SKILL.md` 에 (a) 페이지를 만들지 않는 원본 `tone-kit/references/project-detection.md`, (b) 드리프트 도구가 모양만 바뀐 원본을 기본으로 빼고 `--include-format-only` 로 모두 보인다는 설명, (c) 공통 CSS 링크 수를 `scripts/check-docs-common-css.py` 로 잰다는 것과 쪽 글에서 낱말을 숫자 글자 참조로 쪼개 적지 않는다는 규칙이 있고, 표와 스크립트 매핑 맞대기가 어긋남 0 이다. Given 공통 전제 G, When 아래 측정, Then 네 글자 각 1 회 이상 · 맞대기 종료 코드 0 [exact, enumerated]
  측정: `for s in 'tone-kit/references/project-detection.md' '--include-format-only' 'check-docs-common-css.py' '글자 참조'; do grep -cF -- "$s" .claude/skills/docs-site/SKILL.md; done` 가 네 줄 모두 1 이상, `python3 scripts/detect-docs-drift.py --check-table` 종료 코드 0 · 마지막 줄 「어긋남 0」. 시작 판 네 값 `0 0 0 0` · 맞대기 0

## Script

- [ ] SC-01: 짝 다섯이 기존 쪽을 가리킨다 — 결정표가 「짝」 으로 정한 원본 다섯(도우미 `PAIRS`)을 드리프트 도구가 `--since 6378948 --include-format-only` 에서 정해진 기존 쪽으로 낸다. Given 공통 전제 G, When `m SC-01`, Then `pairs_ok=5/5 drift_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m SC-01` 의 다섯 줄 `tone-kit/references/core-antipatterns.md → docs/tone-kit/antipattern-catalog.html OK` · `core-comment.md → docs/tone-kit/comment-economy.html` · `core-naming.md → docs/tone-kit/naming-taxonomy.html` · `core-structure.md → docs/tone-kit/extraction-thresholds.html` · `reflect-kit/skills/codex-kaizen/references/search-sources.md → docs/reflect-kit/codex-kaizen.html`. 시작 판 `pairs_ok=0/5 drift_rc=2` (선택지 없음)
- [ ] SC-02: NEW 표지가 0 이 된다 — `--since 6378948 --include-format-only` 출력에 `[NEW` 표지 줄이 0, 「페이지 없음」 원본 `tone-kit/references/project-detection.md` 줄이 0, 출력 줄이 1 이상이다. Given 공통 전제 G, When `m SC-02`, Then `new_marks=0 no_page_lines=0 lines=190 drift_rc=0` · 종료 코드 0 [exact]
  측정: `m SC-02`. 양성 대조: 시작 판에서 선택지 없이 `python3 scripts/detect-docs-drift.py --since 6378948 | grep -c '\[NEW'` → 19 (봉인 전 실측)
- [ ] SC-03: 기본 출력이 모양만 바뀐 원본을 뺀다 — `--since 6378948` 기본 출력의 짝 집합이, `--include-format-only` 출력 가운데 `## 배경` 의 정의로 「내용이 바뀐」 원본의 짝 집합과 같다. 모두 190 · 기본 56 이고, 도구는 뺀 짝 수 134 와 선택지 이름 `--include-format-only` 를 표준 오류 한 줄에 적으며, `--json` 출력은 56 개 항목에 키가 `source` · `target` · `registered` · `exists` 넷이다. Given 공통 전제 G, When `m SC-03` 과 JSON 측정, Then `all=190 default=56 expect_real=56 only_tool=0 only_ref=0 rc=0,0` · 표준 오류에 `134` 와 `--include-format-only` · JSON `56 ['exists', 'registered', 'source', 'target']` [exact]
  측정: `m SC-03` (참조 분류는 도우미 `classify` — 도구 코드를 부르지 않는 따로 짠 식), JSON: `python3 scripts/detect-docs-drift.py --since 6378948 --json | python3 -c 'import json,sys;d=json.load(sys.stdin);print(len(d),sorted({k for e in d for k in e}))'`. 알려진 답: `m KA` → `caching=SHAPE tone_overview=REAL` · 종료 코드 0 (봉인 전 실측). 시작 판 `all=0 default=191 … rc=2,0`
- [ ] SC-04: 새 시험 `scripts/test-detect-docs-drift.py` 가 임시 git 저장소 사본으로 세 경우를 돌린다 — (1) 매핑된 원본에 표 구분 줄 · 빈 줄 · 울타리 언어 표시 · HTML 주석 · 목록 기호만 바꾼 커밋은 기본 출력 「no docs drift」 · `--include-format-only` 출력 1 줄, (2) 낱말 하나를 바꾼 커밋은 기본 출력 1 줄, (3) 기준 판에 없던 매핑된 원본을 더한 커밋은 기본 출력 1 줄. `.github/workflows/ci.yml` 에 이 시험을 부르는 `run:` 줄이 있다. Given 공통 전제 G, When `python3 scripts/test-detect-docs-drift.py`, Then 종료 코드 0 · 출력에 경우 3 개 통과 [exact]
  측정: `python3 scripts/test-detect-docs-drift.py; echo $?` 와 `grep -c 'scripts/test-detect-docs-drift.py' .github/workflows/ci.yml` 이 1 이상
  음성 대조: 도구 사본에서 모양/내용 가름을 「늘 내용 바뀜」 으로 바꾸면(임시 사본, 원본은 건드리지 않는다) 경우 (1) 이 실패해 종료 코드가 0 이 아니다
- [ ] SC-05: 새 검사 `scripts/check-docs-common-css.py` 가 추적 쪽 전부를 재고 통과한다 — 인자 없이 부르면 `git ls-files` 로 `docs/` 아래 HTML 을 모두 읽어, 쪽마다 `assets/site.css` 를 가리키는 `<link>` 수(HTML 주석 안은 세지 않고, 큰따옴표 · 작은따옴표 · 따옴표 없는 속성 모두 센다)가 1 이 아니거나 `site.css` · `prefers-reduced-motion` 을 숫자 글자 참조(`&#46;` · `&#45;` · `&#x2e;` · `&#x2d;` 꼴)로 쪼갠 자리가 있으면 그 쪽을 한 줄로 적는다. 끝 줄에 검사한 쪽 수와 어긋난 쪽 수를 함께 적고, 종료 코드는 `harness/evals/gate-exit-codes.md` 의 네 값(0 통과 · 1 위반 · 2 못 읽음 · 3 대상 없음)을 쓴다. `.github/workflows/ci.yml` 에 이 검사를 부르는 `run:` 줄이 있다. Given 공통 전제 G, When `python3 scripts/check-docs-common-css.py`, Then 종료 코드 0 · 검사한 쪽 202 · 어긋난 쪽 0 [exact]
  측정: `python3 scripts/check-docs-common-css.py; echo $?` 의 끝 줄에 `202` 와 `0`, `git ls-files 'docs/*.html' | wc -l` 이 202, `grep -c 'scripts/check-docs-common-css.py' .github/workflows/ci.yml` 1 이상. 시작 판에는 파일 없음
- [ ] SC-06: 새 검사를 임시 사본으로 돌리면 기대대로 떨어진다 — scratch 폴더에 만든 사본(레포 파일은 건드리지 않는다)을 인자로 줘서: ① 첫 파일은 정상 · 둘째 파일에만 링크 둘 → 종료 코드 1, 둘째 파일 이름만 적힘, 검사한 쪽 2. ② 본문 `site&#46;css` 쪽 · `prefers&#45;reduced-motion` 쪽 → 각각 종료 코드 1. ③ 링크 하나 + 본문 `<code>site.css</code>` · `<code>prefers-reduced-motion</code>` 원래 글자 + 주석 안 링크 하나 + 작은따옴표 링크 쪽 → 종료 코드 0. ④ 링크 둘 쪽과 UTF-8 아닌 바이트 쪽을 함께 → 종료 코드 2, 두 파일 이름이 모두 적힘. ⑤ 검사 사본을 `scripts/` 에 넣은, 추적 HTML 이 0 개인 임시 git 저장소에서 인자 없이 부르기 → 종료 코드 3. 셸 대조는 해당 없음 (고정 해석기 python3). 이 다섯 경우가 새 시험 `scripts/test-check-docs-common-css.py` 에 들어 있고 CI 에 등록돼 있다. Given 공통 전제 G, When `python3 scripts/test-check-docs-common-css.py`, Then 종료 코드 0 · 경우 5 개 통과 [exact, enumerated]
  측정: `python3 scripts/test-check-docs-common-css.py; echo $?` 와 `grep -c 'scripts/test-check-docs-common-css.py' .github/workflows/ci.yml` 1 이상
  음성 대조: 검사 사본에서 글자 참조 세기를 지우면 경우 ② 가, 주석 빼기를 지우면 경우 ③ 이 실패해 시험 종료 코드가 0 이 아니다

## Error

- [ ] ER-01: B17 세 쪽이 글자 참조 없이 원래 글자로 적고 측정도 맞는다 — `docs/process/kaizen-flow.html` · `docs/react-kit/animation.html` · `docs/react-kit/build-audit.html` 에 숫자 글자 참조 쪼갬 0, `<style>` 안 `prefers-reduced-motion` 0, `assets/site.css` 링크 1, 보이는 글에 원래 글자 `site.css`(kaizen-flow 1 회 이상) · `prefers-reduced-motion`(animation 4 회 이상 · build-audit 2 회 이상). Given 공통 전제 G, When `m ER-01`, Then 세 줄 모두 `OK` · 종료 코드 0 [exact, enumerated]
  측정: `m ER-01`. 시작 판 `charref=1` · `4` · `2` 로 세 줄 `BAD`
- [ ] ER-02: 움직임 줄이기 설정에서 기능 카드가 들뜨지 않는다 — `docs/design-kit/design-test.html` 의 첫 기능 카드를 가리켰을 때 계산된 `transform` 이 줄이기 설정에서는 `none`, 보통 설정에서는 지금처럼 위로 2px. Given 공통 전제 G, When `node .harness/.meta/after-0928-docs-site/theme.js hover`, Then `reduce cards=9 transform=none` 과 `no-preference cards=9 transform=matrix(1, 0, 0, 1, 0, -2)` 두 줄 · 종료 코드 0 [exact]
  측정: 위 명령. 시작 판 `reduce cards=9 transform=matrix(1, 0, 0, 1, 0, -2)` (결함 재현, 봉인 전 실측)
- [ ] ER-03: B12 — `docs/onboarding-kit/search-strategy.html` 보이는 글에 `G1~G4` 0 회 · `G1~G5` 1 회 이상. Given 공통 전제 G, When `m ER-03`, Then `G1~G4=0 G1~G5=1` 이상 · 종료 코드 0 [exact]
  측정: `m ER-03`. 시작 판 `G1~G4=1 G1~G5=0`
- [ ] ER-04: B13 — bambu 세 쪽이 원본 머리처럼 판 번호를 「실행 때 조회」 로 안내한다. `docs/bambu-kit/failure-recipes.html` · `docs/bambu-kit/materials.html` · `docs/bambu-kit/bambu-fields-baseline.html` 보이는 글에 `실행 때 조회` · `Info.plist` · `BBL.json` · `02.06.00.05` · `02.08.00.06` · `02.08.02.61` 가 각 1 회 이상, 그리고 failure-recipes · materials 에서 `2.6.0` 이나 `02.06.00.51` 이 보이는 줄마다 같은 줄에 `처음` · `최초` · `실측` 가운데 하나가 있다. Given 공통 전제 G, When `m ER-04`, Then 세 줄 `OK` · `loose_version_lines=[]` · 종료 코드 0 [exact, enumerated]
  측정: `m ER-04`. 시작 판 세 줄 `BAD` (값은 `## GAP 분석`)
- [ ] ER-05: B14 — `docs/onboarding-kit/setup-guide.html` 이 원본 `onboarding-kit/skills/setup-guide/SKILL.md` 의 인라인 코드 82 개를 모두 싣고, 「만들 수 없다고 결론 낼 때도 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)」 규칙 문장을 싣는다. Given 공통 전제 G, When `m ER-05`, Then `code=82/82 rule_sentence=1 miss=[]` · 종료 코드 0 [exact]
  측정: `m ER-05`. 시작 판 `code=74/82 rule_sentence=0`

## Architecture

- [ ] AR-01: 새 쪽 열셋 — 도우미 `NEW_PAGES` 의 원본 13 개마다 쪽이 있고, 쪽이 `wc -l` 기준 400 줄 이상, `docs/index.html` 에 그 쪽 `file:` 항목이 정확히 하나이며 그 id 가 목차 전체에서 하나뿐이고 `getIcon` 에 같은 id 아이콘이 있으며, `assets/site.css` 링크가 하나다. 원본 담김은 낱말 비율 0.95 이상 · 인라인 코드 전부 · 코드 블록 줄(공백 뺀 8 글자 이상) 전부다. Given 공통 전제 G, When `m AR-01`, Then `new_pages_ok=13/13` · 종료 코드 0 [exact, enumerated]
  측정: `m AR-01` 열세 줄 — `docs/bambu-kit/comment-analysis.html` · `docs/bambu-kit/tolerance.html` · `docs/bambu-kit/user-preferences.html` · `docs/flutter-toolkit/figma-parity-self-verify.html` · `docs/harness/cross-kit-principles.html` · `docs/react-kit/clean-arch-layout.html` · `docs/react-kit/common-gotchas.html` · `docs/react-kit/result-patterns.html` · `docs/reflect-kit/reflect-promote.html` · `docs/flutter-toolkit/research-log.html` · `docs/planning-kit/research-log.html` · `docs/rust-kit/research-log.html` · `docs/tone-kit/research-log.html`. 시작 판 열셋 모두 `MISSING`
- [ ] AR-02: 밝은 테마가 공통 틀 규칙대로 돈다 — A3 일곱 쪽과 새 쪽 열셋(20 쪽)마다: 저장값 없이 밝은 색 설정 브라우저로 열면 `light`, 어두운 색 설정이면 `dark`, 단추 `#theme-btn` 을 누르면 `light` 로 바뀌고 `dk-theme` 에 `light` 가 저장되며 다시 열어도 `light`, 누르기 전후 본문 배경색이 다르다. 접근성 검사기 줄은 `OK` · 넘침 `0/0/0/0`(320 · 375 · 768 · 1280) · `theme=both` · 단추 가로 · 세로 44 이상. Given 공통 전제 G, When `m AR-02`, Then `ok=20/20` · 종료 코드 0 [exact, enumerated]
  측정: `m AR-02` (검사기 `node scripts/check-docs-a11y.js` 와 `node .harness/.meta/after-0928-docs-site/theme.js theme`). A3 일곱: `docs/design-kit/visual-change-protocol.html` · `docs/design-kit/design-test.html` · `docs/flutter-toolkit/visual-evidence-protocol.html` · `docs/infra-kit/cicd.html` · `docs/infra-kit/infra-test.html` · `docs/onboarding-kit/format-checklist.html` · `docs/react-kit/render-evidence-protocol.html`. 양성 대조: 시작 판 `ok=0/20` (일곱 쪽 `dark-only` · `click=none`), 좋은 예 `docs/onboarding-kit/setup-guide.html` 은 같은 두 측정에서 기대 줄과 같다 (봉인 전 실측)
- [ ] AR-03: B16 — dr2 가 다시 쓴 쪽 열(도우미 `B16_PAGES`)마다 옛 판 `38cccd1` 이 걸던 같은 폴더 · 형제 폴더 쪽 링크가 모두 있고, react 다섯 쪽에 옛 손 글 절 아홉이 같은 제목의 `<h2>` 로 있으며 절 본문 보이는 글이 200 자 이상이다 — `Bad vs Good — 통합 설계 실수 패턴` · `21 스킬 교차 공통 주의사항` (integration), `Bad vs Good — G1 핵심 실수 패턴` · `Scaffolding 핵심 Gotchas` (scaffolding), `Bad vs Good — G3 핵심 실수 패턴` (performance), `Bad vs Good — G5 핵심 실수 패턴` · `G5 스킬 공통 주의사항` (ui-patterns), `감사 실패를 유발하는 패턴 vs 올바른 패턴` · `빌드·감사 스킬 공통 주의사항` (build-audit). 되살린 절의 스킬 이름 · 규칙 · 수치는 지금 `react-kit/skills/` 와 `docs/react/kit-design/` 에 맞추고, 옛 판과 달라진 곳은 기록(AR-09)에 적는다. Given 공통 전제 G, When `m AR-03`, Then 열 줄 모두 `OK` · 종료 코드 0 [exact, enumerated]
  측정: `m AR-03`. 시작 판 열 줄 모두 `BAD`
- [ ] AR-04: D3 — 원본 내용이 실제로 바뀐 짝의 쪽이 따라간다. `--since 6378948` 기본 출력의 짝마다 쪽이 있고, 원본이 `6378948` 뒤에 새로 얻은 인라인 코드 · 낱말(HTML 주석 · 울타리 줄 · 표 구분 줄 뺌)이 모두 쪽의 보이는 글이나 링크 주소에 있다. Given 공통 전제 G, When `m AR-04`, Then `pairs=56 bad=0 drift_rc=0` · 종료 코드 0 [exact]
  측정: `m AR-04`. 양성 대조: 시작 판 `pairs=191 bad=27` (GAP 8 · NOPAGE 19, 봉인 전 실측)
- [ ] AR-05: D5 — 기록 `.harness/.meta/after-kaizen-0928/d1-notes.md` 에 `| 원본 | 결정 | 근거 |` 표가 있고, 원본 27 개(도우미 `NEW_PAGES` 13 · `PAIRS` 5 · `D5_EXTRA` 8 · 「페이지 없음」 1)가 각각 한 행이며, 결정 칸이 `새 페이지: \`<쪽>\`` · `짝: \`<쪽>\`` · `페이지 없음` 가운데 하나로 지금 파일 · 목차 · 도구 출력과 맞는다. 그리고 `.harness/.meta/after-kaizen-0926b/dca-notes.md` 의 「DC-9 매핑 규칙 결정」 절에 이 기록을 가리키는 정정 한 줄이 있다(옛 표 행은 그날 기록이라 고치지 않는다). Given 공통 전제 G, When `m AR-05` 와 `grep -c 'after-kaizen-0928/d1-notes.md' .harness/.meta/after-kaizen-0926b/dca-notes.md`, Then `rows_ok=27/27` · 종료 코드 0 · 정정 줄 1 이상 [exact, enumerated]
  측정: 위 두 명령. 시작 판 `notes 없음` · 0
- [ ] AR-06: 바뀌거나 새로 생긴 docs 쪽 전부(목차 `docs/index.html` 뺌)가 접근성 검사기에서 `OK` · 넘침 `0/0/0/0` · 콘솔 에러 0 · 대비 실패 0 이다. Given 공통 전제 G, When `m PAGES`, Then `bad=0` · 종료 코드 0 [exact]
  측정: `m PAGES` (대상은 `git diff --name-only e500a63..HEAD -- docs` 의 HTML — 이름이 겹치는 쪽은 도우미가 따로 돌려 경로로 되짚는다). 양성 대조: `docs/onboarding-kit/setup-guide.html` 의 `<body>` 바로 뒤에 폭 2000px 상자를 넣은 scratch 사본을 검사기에 주면 `FAIL wide.html of=1680/1625/1232/720` (봉인 전 실측)
- [ ] AR-07: 바뀌거나 새로 생긴 docs 쪽이 레포 밖 자원을 부르지 않는다 — `<script>` · `<img>` · `<iframe>` 의 `src`, `<link>` 의 `href`, CSS `@import` · `url()` 에서 `http://` · `https://` · `//` 로 시작하는 주소를 큰따옴표 · 작은따옴표 · 따옴표 없음 모두 센다(본문 `<a href>` 는 세지 않는다). Given 공통 전제 G, When `m EXT`, Then `ext_pages=0` · `checked` 1 이상 · 종료 코드 0 [exact]
  측정: `m EXT`. 양성 대조: scratch 사본 `bad.html`(따옴표 없는 `//` 링크 · 작은따옴표 `@import url('https://…')` · 작은따옴표 `//` 이미지)과 `good.html` 을 인자로 주면 `EXT …bad.html 3` · `checked=2 ext_pages=1` · 종료 코드 1, `good.html` 만 주면 종료 코드 0 (봉인 전 실측)
- [ ] AR-08: 커밋 규칙 — `e500a63..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(문서 사이트는 `docs/<킷>/` 하나에 `docs/index.html` 을 더해도 된다)이며, `.harness/` 파일은 구현 파일과 다른 커밋이고, 메시지에 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」 가 있으며, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m COMMITS`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m COMMITS`
- [ ] AR-09: 기록 — `.harness/.meta/after-kaizen-0928/d1-notes.md` 에 (a) 항목 열 개(A2 · A3 · B12 · B13 · B14 · B15 · B16 · B17 · D3 · D5)마다 처리 커밋 해시, (b) `tone-kit:tone-guide` 1 단계와 5 단계를 돌린 결과(새로 쓴 한국어 글 · 스크립트 주석 · 기록이 대상), (c) 이 묶음 밖으로 남긴 것 — 어두운 테마만 있는 118 쪽, `<style>` 에 움직임 줄이기를 다시 적은 쪽 수, AR-03 에서 옛 판과 달라진 곳 — 이 있다. Given 공통 전제 G, When 아래 측정, Then 열 ID 모두 1 회 이상 · `tone-guide` 1 회 이상 · `118` 1 회 이상 [exact, enumerated]
  측정: `for k in A2 A3 B12 B13 B14 B15 B16 B17 D3 D5 tone-guide 118; do printf '%s=%s\n' $k "$(grep -cw -- "$k" .harness/.meta/after-kaizen-0928/d1-notes.md)"; done` 가 모두 1 이상

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다 (이 묶음에서는 bambu 쪽이 Studio 판을 기준값처럼 박아 두지 않는 것으로 잰다 — ER-04 와 같은 측정 `m ER-04`)
- [ ] AP-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-d1` 에 `forced-update` 0 줄)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 바뀐 `.md` 파일(`.claude/skills/docs-site/SKILL.md` · `.harness/.meta/after-kaizen-0928/d1-notes.md` · `.harness/.meta/after-kaizen-0926b/dca-notes.md`)에 markdownlint MD040 0 건 — DG-02 와 같은 명령)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 검사 · 시험은 `scripts/` 에 두고 인자 없이도 · 파일 인자로도 부를 수 있다 — SC-05 · SC-06 명령)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 짝 다섯은 새 쪽을 만들지 않고 기존 쪽에 잇는다 — SC-01. 새 쪽은 틀 `.claude/skills/docs-site/references/page-template.html` 과 공통 파일 `docs/assets/site.css` 를 쓴다 — AR-01 · AR-02. 접근성 · 링크 검사는 기존 `scripts/check-docs-a11y.js` · `scripts/check-docs-links.py` 를 쓴다)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only e500a63..chore/ak3-d1 | grep -c '^scripts/release.sh$' 이 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.md` 세 파일은 markdownlint-cli2 0.23.2(MD013 끔)로 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`, 새 · 바뀐 `.py` 는 `python3 -m py_compile` 종료 코드 0
  측정: 파일마다 `<scratch>/mdlint/node_modules/.bin/markdownlint-cli2 --config <scratch>/d1/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(설정 파일 내용 `{ "config": { "MD013": false } }`). 양성 대조: `#bad` 제목과 빈 줄 셋이 든 사본 `pos.md` → 경고 4 · 종료 코드 1 (봉인 전 실측). 시작 판 `.claude/skills/docs-site/SKILL.md` 0 건 · `dca-notes.md` 0 건
- [ ] DG-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: DG-01 과 같은 명령)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 정적 문서 쪽 · 검사 스크립트 · 기록. 쪽을 브라우저로 여는 확인은 AR-02 · AR-06 · ER-02 가 한다)
- [ ] DG-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` (TMPDIR 은 scratch 아래 새 폴더)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외)이고 `docs-a11y` 로그 끝이 `202/202 PASS`, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/test-check-docs-common-css.py` · `npx playwright test` 의 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 `grep -c 'rc=0' <TMPDIR>/ci-local/summary.txt`. 시작 판 ci-local 25 단계 `rc=0` · `docs-a11y` `189/189 PASS`, CI 전용 여섯 단계 0 · `npx playwright test` `164 passed` (봉인 전 실측, 새 셋은 아직 없음)

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다. 원본 문서(드리프트 매핑이 잡는 `.md` · `.yaml`)는 고치지 않는다 — 고치면 SC-02 · SC-03 · AR-04 의 기대 수가 흔들린다. 원본이 틀렸다고 보이면 기록에 남긴다.

```text
# sprint-scope
scripts/detect-docs-drift.py
scripts/test-detect-docs-drift.py
scripts/check-docs-common-css.py
scripts/test-check-docs-common-css.py
.github/workflows/ci.yml
.claude/skills/docs-site/SKILL.md
docs/index.html
docs/bambu-kit/comment-analysis.html
docs/bambu-kit/tolerance.html
docs/bambu-kit/user-preferences.html
docs/bambu-kit/failure-recipes.html
docs/bambu-kit/materials.html
docs/bambu-kit/bambu-fields-baseline.html
docs/bambu-kit/bambu-print-profile.html
docs/flutter-toolkit/figma-parity-self-verify.html
docs/flutter-toolkit/research-log.html
docs/flutter-toolkit/visual-evidence-protocol.html
docs/harness/cross-kit-principles.html
docs/harness/feedback-system.html
docs/harness/agent-design-guide.html
docs/harness/plugin-validation.html
docs/harness/skill-design-guide.html
docs/react-kit/clean-arch-layout.html
docs/react-kit/common-gotchas.html
docs/react-kit/result-patterns.html
docs/react-kit/render-evidence-protocol.html
docs/react-kit/integration.html
docs/react-kit/scaffolding.html
docs/react-kit/state-data.html
docs/react-kit/performance.html
docs/react-kit/quality.html
docs/react-kit/ui-patterns.html
docs/react-kit/animation.html
docs/react-kit/build-audit.html
docs/reflect-kit/reflect-promote.html
docs/planning-kit/research-log.html
docs/rust-kit/research-log.html
docs/tone-kit/research-log.html
docs/design-kit/visual-change-protocol.html
docs/design-kit/design-test.html
docs/infra-kit/cicd.html
docs/infra-kit/infra-test.html
docs/onboarding-kit/format-checklist.html
docs/onboarding-kit/search-strategy.html
docs/onboarding-kit/setup-guide.html
docs/howto-kit/overview.html
docs/process/kaizen-flow.html
docs/api-kit/multi-sample-pagination-variance.html
```

- 하지 않는 것: 어두운 테마만 있는 A3 밖 118 쪽의 밝은 테마, 쪽 `<style>` 에 남은 움직임 줄이기 105 쪽 정리, 접근성 검사기의 `themeToggle` 인식(목록 B7), 변환 스크립트를 레포에 들이기(목록 D4), 로컬 CI 도구 `ci-local.sh` 고치기(목록 D2 · 레포 밖 파일). 다른 ak3 묶음이 `chore/after-kaizen-0928` 에 더하는 원본 변경은 이 가지에 없으므로 이 계약이 재지 않는다 — 합친 뒤 드리프트는 그 판에서 다시 본다.
- 되살린 react 손 글(AR-03)은 옛 판 문장을 그대로 붙이지 말고 지금 스킬 · 설계 기록에 맞춘다. 옛 판 코드 표본 41 개 가운데 지금 `react-kit/` · `docs/react/` 에 글자 그대로 없는 것이 많다(봉인 전 탐침 87 개 중 41 개) — 스킬 이름 · 규칙 번호 · 수치가 지금과 어긋나지 않는지 사람이 대조하고 결과를 기록에 적는다. 이 대조는 기계로 재지 못해 AR-09 (c) 의 기록으로 남긴다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0928-docs-site/`)은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <ID>` = `python3 .harness/.meta/after-0928-docs-site/measure.py <ID>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 테마 · 카드 측정은 `node .harness/.meta/after-0928-docs-site/theme.js theme <쪽...>` · `node .harness/.meta/after-0928-docs-site/theme.js hover`. 둘 다 W 의 `node_modules`(`npm ci`)의 playwright 를 쓴다.
- 도우미가 쓰는 판: 시작 판 `e500a63` · 드리프트 기준 `6378948` · 옛 쪽 `38cccd1`. 파일 지문은 봉인 커밋 직전에 `shasum -a 256 .harness/.meta/after-0928-docs-site/measure.py .harness/.meta/after-0928-docs-site/theme.js | cut -c1-16` 로 뽑아 봉인 커밋 메시지에 적는다 — 봉인 뒤 도우미가 바뀌면 드러난다.
- 봉인 전 실측(2026-09-28, W 시작 판): SC-01 ~ SC-03 · AR-01 ~ AR-05 · AR-07 · ER-01 · ER-03 ~ ER-05 모두 종료 코드 1(결함 재현), `m KA` 0, EXT 양성 대조 1 · 좋은 예 0, 테마 좋은 예(setup-guide) 기대 줄과 같음, 카드 측정 결함 재현, markdownlint 양성 대조 경고 4. 값은 `## GAP 분석` 과 각 조건 측정 줄에 있다.
- 오라클 해소: SK-01 — 스킬 문서에 적는 것 자체가 요구다. 적은 동작이 실제로 도는지는 SC-01 ~ SC-06 이 도구 · 검사를 불러 잰다.
- 오라클 해소: DG-02 — 글자 찾기가 아니라 markdownlint · `py_compile` 를 실행해 그 출력으로 판정하고, 양성 대조(경고 4)를 봉인 전에 쟀다.
- SC-03 의 190 · 56 · 134 는 시작 판 191 짝에서 「페이지 없음」 원본 하나(모양만 바뀐 원본이라 기본 출력 수는 그대로)를 뺀 값이다. 원본 문서를 고치지 않는다는 `## 범위 경계` 전제가 깨지면 이 수가 달라진다.
