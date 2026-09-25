---
feature: "카이젠 2026-09-24 Phase 6 계약 — 편집 전 확정(대상 · 되말하기 · 관례 표) · 비교 반복과 반영 확인 · 캡처 점검 목록 · 승인 기록 폐기 칸 · 같은 역할 관례 감사 · 형제 규약 숫자와 정본 · 시안 개수 정합 · DTCG · 버전 · WCAG 사실 정정"
slug: kaizen-0924-p06-design-kit
created: "2026-09-25 05:27"
complexity: "복잡"
conditions: 30
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:2e3e2f264632e340
locked_at: "2026-09-25 06:16"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase6.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 6` 인 행은 아홉이다(`F01` · `F04` · `design:P1` ~ `design:P7`). 러닝북 Phase 6 추가 과제가 하나(flutter 규약과 숫자 맞추기 · 세 규약 정본
한 줄 결정), 근거 파일 §3 현행화 표가 열 줄, 카이젠 스킬(`.claude/skills/design-kaizen/SKILL.md`) Gotcha 6 형제 대조와 Step 4(evals)에서 넷을 더 봤다.
앞 Phase notes(`phase1-notes.md` ~ `phase4-notes.md`)에는 design-kit 로 넘긴 줄이 없다(`grep -n 'design-kit\|Phase 6'` 0 건).

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `F01` | UI 의도가 샘 — 평평한 줄 대신 카드, 화면 대신 그리로 가는 칩, 고정 범위를 뒤집음. 남은 것 design:P3 | 반영 — SK-01 (규약 §0 대상 · 되말하기 · 화면 자체) · SK-05 (design-mockup Step 1). 리액트 규약 쪽은 Phase 10 몫 |
| `F04` | 글자 넘침 · 깨진 글리프를 사용자가 잡음, 넘침 재현을 데이터 수정으로 시도. 남은 것 design:P4 | 반영 — SK-03 · SK-07 인용 |
| `design:P1` | 시안 · 컴포넌트 전에 재사용 부품 목록과 구조 관례 목록을 기존 화면 근거로. 기존 화면 3 개(이 제안) 대 2 개 | 반영 — SK-01 (관례 표) · SK-05 (design-mockup Step 2 · design-component Step 0 · design-guide Step 1). 수는 **2 개 이상**으로 정했다 (아래 결정 1) |
| `design:P2` | 시안 개수 규칙을 파일마다 맞춤 (미지정 3 · 지정 N · 승인 시 최대 5). 한 프로젝트 기억과 방향이 반대라 사용자 확인 필요 | 부분 반영 — SK-09. 규칙 방향은 바꾸지 않고, 규칙과 어긋난 두 자리(`mockup-guidelines.md:7` 「5개 시안」 · `evals.json` id 19 「정확히 5개」)만 이미 정한 규칙에 맞춘다. 방향 질문은 사용자 확인 목록으로 넘긴다(ER-04 `design:P2 방향`) |
| `design:P3` | design-mockup Step 1 에 대상 화면 경로와 한 문장 되말하기, 요소 하나 지목 요청까지 §2 를 넓힘 | 반영 — SK-01 (§0 · §2) · SK-05 |
| `design:P4` | 렌더 산출물 캡처 점검 목록 4 줄과 가장 큰 글자 크기로 한 번 더. 같은 점검 항목이 규약 · audit-criteria · design-reviewer 세 자리 | 반영 — SK-03 (규약에만 정의) · SK-07 (design-audit Gotcha 12 · design-reviewer 규칙 9 는 인용만) · RE-01 (정의가 한 곳) |
| `design:P5` | 승인 기록에 확정 구성과 폐기 항목 칸. 폐기 결정 기록 자리가 네 곳 | 반영 — SK-04 · SK-06. 기록 자리는 아래 결정 3 |
| `design:P6` | 비교 반복 순서와 새로 그려졌는지 확인, 스스로 고치기 최대 5 회. 플러터 규약 3 회 대 5 회 | 반영 — SK-02 · SK-08. 상한은 **3 회**로 정했다 (아래 결정 1) |
| `design:P7` | 감사 기준에 기존 화면 관례 일치 행. 2 개 대 3 개 | 반영 — SK-07 · ER-03. 행 이름을 「같은 역할 관례 일치」 로 좁혔다(근거 파일 §2 P7) — 모자랄 때의 처리는 결정 4 |
| 러닝북 Phase 6 | flutter 규약과 숫자(기존 화면 2 개 이상 · 스스로 고치기 3 회)를 맞추고, 세 규약 정본 자리를 한 줄로 결정 | 반영 — SK-08 (결정 2) |
| 근거 파일 §3 · §4-9 · §4-10 | DTCG 예시가 규격과 충돌 · Style Dictionary v4 표기 · Tailwind 날짜 · WCAG 「2026 법적 타겟」 · `size` 쿼리 전면 금지 · 375px 를 WCAG 수치로 표기 · 44×44 를 AA 로 읽힐 표기 | 반영 — SK-11 · SK-12 · ER-01 |
| 카이젠 스킬 Step 4 | 개선에 맞춰 `evals/evals.json` assertion 추가 · 수정 | 반영 — SK-10 (id 28 · 29 · 30 신설, id 25 에 한 줄, id 19 수정) |
| 카이젠 Gotcha 6 형제 대조 ① | `design-audit` · `design-reviewer` 가 옮겨 둔 미검증 정본이 2026-08-13 개정(카운터 `UNVERIFIED_ENV` / `UNVERIFIED_INVALID_EVIDENCE` 분리 · `N/A (사유)` 예외) 전 판이다 — `design-reviewer.md` 의 `UNVERIFIED_ENV` 0 건(backend-reviewer 7 건 · backend-audit 3 건, `grep -o` 로 셌다) | 미반영 — 처리 배정표 밖이고 판정 규칙(REJECT 문턱) 자체를 바꾸는 별도 관심사다. design-reviewer 규칙 8 · 최종 판정, design-audit Gotcha 11 · Step 4 · Step 5, evals id 21 다섯 자리를 함께 바꿔야 해 이 계약 기능 조건이 20 을 넘는다. 다음 사이클 Phase 6 으로 넘긴다(ER-04 `UNVERIFIED_ENV`). 이번 변경은 그 차이에 걸리지 않게 `N/A` 를 쓰지 않고 design-reviewer 규칙 7 의 기존 말(「대상 코드에 해당 요소 부재」)을 쓴다 — ER-03 |
| 카이젠 Gotcha 6 형제 대조 ② | 형제 스킬 셋은 `## Step 0: 자동 감지 및 로드` 인데 design-mockup 만 `## Step 2` 다 | 미반영 — 단계 번호를 옮기면 Gotcha 13 의 「Step 6」 · evals 가 함께 바뀐다. 이번 관심사와 별개라 다음 사이클로(ER-04 `design-mockup Step 0`). AR-02 가 이번에 단계 제목을 바꾸지 않았음을 잰다 |
| 카이젠 Gotcha 8 (Phase 1 새 원칙) | skill-design-guide §3.7 의 `[미검증]` 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) | 미반영 — design-kit 에는 옛 「사유 한 줄」 문구가 없다(`grep -rn '사유 한 줄' design-kit` 에서 docs/design 을 뺀 0 건). phase1-notes 넘김 표에도 design-kit 는 없다. 규약 §3 의 「캡처 실패 → `[미검증]`」 줄에 네 칸을 붙이는 것은 위 ①과 함께 다음 사이클에 본다(ER-04 `§3.7 네 칸`). Phase 1 이 agent 가이드 §10 을 `[미검증:ENV]` · `[미검증:INVALID]` 분류로 다시 썼는데 design-reviewer 에는 접미 없는 `[미검증]` 이 15 줄 남았다 — ① 과 같은 일이라 함께 넘긴다 |
| 관련 행 (다른 Phase 배정) | `F02`(Phase 5 · design 쪽은 P1 · P7) · `F03`(Phase 10 · design 쪽은 P6) · `F20`(Phase 11 · 폐기 결정 자리) · `F25`(Phase 5 · design 쪽은 P2) · `F26`(이번 스프린트 · design 쪽은 P6) | 디자인 쪽 몫은 위 줄에서 다룬다. `F20` 의 제품 수준 기록 자리는 Phase 11 이 정한다 — design-kit 은 경로만 가리킨다(결정 3 · ER-04 `F20`) |

### 결정 넷

1. **숫자 — 같은 역할의 서로 다른 기존 화면 2 개 이상 · 스스로 고치기 최대 3 회.** flutter 규약(`flutter-toolkit/references/visual-evidence-protocol.md:52` ·
   `:91`)이 이미 이 값으로 돈다. 근거 파일 §5 는 「정확히 2 개/3 개」 · 「정확히 3 회/5 회」 를 정하는 외부 표준을 찾지 못했다고 적었다 — 숫자는 형제 규약
   정합과 운영 비용으로 고른 레포 결정이다(근거 파일 §2 P1 · P6 추론). 세 번째 화면이 있으면 더 읽어도 되지만 필수로 두지 않는다
2. **세 규약의 정본 — 세 규약(design-kit visual-change-protocol · flutter-toolkit visual-evidence-protocol · react-kit render-evidence-protocol)이 같이 쓰는
   규칙의 정본은 harness `skill-design-guide.md` 한 절에 두고, 세 규약에는 스택마다 다른 채널 · 도구 · 명령만 남긴다.** 세 규약이 이미 등급(§3.7) ·
   미검증 정본(qa-evaluation-guide)을 harness 에서 가져오고, 시안 개수 정본도 harness §5.6 이다(근거 파일 §2 P2 추론). design-kit 을 정본으로 두면
   flutter-toolkit · react-kit 이 지금 없는 design-kit 의존을 새로 갖게 된다. 그 절은 이 사이클 Phase 1 이 끝난 뒤라 다음 사이클 Phase 1 이 만든다 —
   그때까지 design-kit 규약 머리에 이 결정 한 줄과 「한쪽 값을 바꾸면 다른 쪽도 같이 바꾼다」 를 둔다(결정 줄은 SK-08 (a) 가 잰다. 같이 바꾼다는 줄은
   재지 않는다 — `mock.py` 가 글자 그대로 넣는다). flutter · react 규약이 그 절을 가리키게
   바꾸는 것은 Phase 5 · 10 몫이다(ER-04)
3. **폐기 결정 기록 자리 — design-kit 승인 기록은 디자인 범위(버린 안 · 요소와 이유)만 적고, 제품 요구 수준의 폐기 결정은 새로 정하지 않고 그 결정이 적힌
   파일 경로만 적는다.** 네 후보(design:P5 · backend-family:P1 · user-setup:P2 · user-setup:P6) 가운데 제품 수준 자리는 처리 배정표가 Phase 11(`F20`)에
   맡겼다. 결정 원문을 두 곳에 두면 한쪽만 고쳐진다(근거 파일 §2 P5 추론). 기록만 두면 아무도 안 읽으므로 design-mockup Step 2 가 같은 화면의 승인 기록을,
   design-concept Step 0 이 컨셉 승인 기록을 읽어 폐기한 대안을 다시 넣지 않게 한다(SK-06)
4. **같은 역할 기존 화면이 모자라거나 관례 표가 없을 때 — `[미검증]` 이 아니라 design-reviewer 규칙 7 의 「대상 코드에 해당 요소 부재」 로 적는다.**
   근거 파일 §2 P7 · §4-1 · §4-8 은 `[미검증]` 을 권했다. 그러나 이 킷의 design-reviewer 규칙 8.2 는 `[미검증]` 을 검증 도구·환경이 없을 때만 쓰고,
   규칙 8.3 은 2 건이면 FAIL 이 없어도 REJECT 다. 비교할 기존 화면이 모자란 것은 도구가 없는 것도, 감사 대상의 결함도 아니라 대조할 관례가 없는 것이다.
   `[미검증]` 으로 두면 화면이 적은 앱이 이 항목 하나로 REJECT 문턱에 다가간다(ER-03)

## 리서치 소스

근거 파일 `.harness/.meta/evidence/phase6.md` 의 출처만 쓴다. 새로 찾은 자료는 없다.

- [WCAG 2.2 — Recommendation 2024-12-12](https://www.w3.org/TR/WCAG22/) — SC 3.2.4(같은 기능의 일관된 식별 → 같은 역할 한정 관례) · SC 1.4.4(텍스트 200%) ·
  SC 1.4.10(320 CSS px Reflow) · SC 2.5.8(AA 24×24) · SC 2.5.5(AAA 44×44). 「2026 법적 타겟」 근거는 없음
- [W3C DTCG Format Module 2025.10 Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) — 이름에 `{` `}` `.` 금지 · `$` 시작 금지,
  color `$value` = `colorSpace` · `components` (+ 선택 `alpha` · `hex`) 객체, dimension `$value` = `{ value, unit(px|rem) }`, 그룹 속성 목록에 `$schema` 없음
- [Tailwind CSS v4.0 발표 2025-01-22](https://tailwindcss.com/blog/tailwindcss-v4) · [v4.3.3 (2026-07-16)](https://github.com/tailwindlabs/tailwindcss/releases/tag/v4.3.3) — 기본 팔레트 `rgb` → `oklch`
- [Style Dictionary v5.0.0](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.0.0) · [v5.5.5 (2026-09-20)](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.5.5) ·
  [v5 Migration](https://styledictionary.com/versions/v5/migration/) — Node.js 22 이상, 비토큰 leaf 참조 · `.value` 접미 참조 · 참조 구문 바꾸기 제거, `convertTokenData` 취약점 수정
- [MDN Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries) ·
  [MDN 호환 데이터 container-type](https://github.com/mdn/browser-compat-data/blob/main/css/properties/container-type.json) — `size` 는 유효한 값, 크기 쿼리 Chrome 105 · Firefox 110 · Safari 16
- 조회하지 않은 것(근거 파일 §5): Material 3 Expressive · Apple HIG 2026. DTCG `$schema` URL · Figma Variables 의 OKLCH 지원은 확인하지 않았으므로 강하게 쓰지 않는다

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하는가 | 넷 — 공유 규약(`references/visual-change-protocol.md`) · 생성 스킬(design-mockup · design-component · design-guide · design-concept · design-system) · 감사(design-audit · audit-criteria · design-reviewer) · 평가 사례(`evals/evals.json`) |
| 공개 API·계약 변경 | 밖에 드러난 형태가 바뀌는가 | 예 — 규약에 §0 이 새로 생기고, 승인 기록 최소 필드가 두 칸 늘고, 감사 Authenticity 에 행이 하나 는다 |
| 소비면 존재 | 받아 쓰는 반대편이 있는가 | 예 — 규약 절을 인용하는 스킬 · 에이전트 여섯, 승인 기록을 읽는 design-mockup Step 2, 감사 판정을 받는 design-audit Step 5 |
| 회귀 위험 | 기존 동작이 깨질 경로가 있는가 | 예 — eval 기대값 변경(id 19), 감사 행 추가, 규약 절 번호를 인용하는 기존 문장 |

네 축 모두 「예」 — **복잡**. Step 2.5 양면 조건이 필수다(아래 Counterpart).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 `N/A` 사유에 같은 문자열 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 `N/A` 사유에 같은 문자열 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 `[]` |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 네 절 그대로. `Script` 는 `SC-00: N/A (사유)` |
| `anti_patterns[].id` / `message` | `AP-01` 버전 하드코딩 · `AP-02` force push · `AP-03` bare code fence · `AP-04` frontmatter name 누락 | `AP-01` · `AP-03` · `AP-04` 를 쓴다. `AP-02` 는 이 Phase 가 push 하지 않아(러닝북 — push · PR 은 Final F4) 걸릴 자리가 없어 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `7925890` 판)

| 대상 파일 | 읽은 줄 | 기존 갭 · 위반 | 조건 |
| --------- | ------- | -------------- | ---- |
| `design-kit/references/visual-change-protocol.md` | `:3-4` 적용 스킬 목록 · `:45` §2 첫 문장 · `:54` Change Manifest 틀 보존 줄 · `:97-103` 렌더 산출물 특칙 · `:121-133` 최소 필드 · `:171-176` 개수 계약 | 편집 전 대상 · 되말하기 · 관례 표 없음(F01 · P1 · P3), §2 와 그 틀의 보존 줄이 「속성 하나」 만 다룸(P3 — F01 은 칩 하나를 옮기라는 말에 이웃 칩까지 옮겼다), 반영 확인 · 반복 순서 · 상한 없음(P6), 캡처 점검 목록 없음(P4 · F04), 확정 구성 · 폐기 칸 없음(P5), 적용 스킬 목록에 design-component · design-concept 빠짐. 개수 계약은 이미 3 · N · 5 | SK-01 ~ SK-04 · SK-08 · AR-02 |
| `design-kit/skills/design-mockup/SKILL.md` | `:26` Gotcha 10 · `:37-44` Step 1 · `:46-59` Step 2 · `:123-131` Step 5 · `:135-157` Step 6 | Step 1 에 대상 경로 · 되말하기 없음, Step 2 가 앱 코드 · 승인 기록을 안 읽음, Step 5 가 속성 지목만이고 틀 보존 줄도 「같은 요소」 만, 「§2」 가 어느 문서의 절인지 그 줄에 없음, Step 6 에 확정 구성 · 폐기 칸 없음, Gotcha 10 「2026 Baseline 기준 모든 주요 브라우저 지원」 | SK-05 · SK-06 · SK-12 |
| `design-kit/skills/design-mockup/references/mockup-guidelines.md` | `:7` · `:67` | 「5개 시안」(P2 규칙과 어긋남 — 개수를 여기 또 적으면 숫자가 어긋날 자리가 하나 는다) · 「44×44pt 이상」 을 AA 와 구분 안 함 | SK-09 · SK-12 |
| `design-kit/skills/design-component/SKILL.md` | `:32-47` Step 0 | 앱 코드의 기존 부품을 찾지 않음(P1) | SK-05 |
| `design-kit/skills/design-guide/SKILL.md` | `:24` Gotcha 10 · `:27` Gotcha 13 · `:34-50` Step 1 | Gotcha 13 이 Step 1 에서 토큰 · 기존 컴포넌트를 Grep/Read 한다고 적었는데 Step 1 본문엔 카테고리 표뿐, 「법적 표준」 | SK-05 · SK-12 |
| `design-kit/skills/design-concept/SKILL.md` | `:90-103` Step 0 · `:204-224` Step 7 | 승인 기록 틀에 폐기 칸 없음(형제 design-mockup 과 짝), Step 0 이 승인 기록을 읽지 않음 | SK-06 |
| `design-kit/skills/design-audit/SKILL.md` | `:45` Gotcha 12 렌더 산출물 특칙 · `:72` Color 행 · `:78` Layout 행 · `:80` Authenticity 행 | 캡처 점검 목록 인용 없음, 「현재 법적 표준」 · 「2026 Baseline」, 관례 행 없음 | SK-07 · SK-12 |
| `design-kit/skills/design-audit/references/audit-criteria.md` | `:41` · `:59` · `:96` · `:97` · `:110-118` | 「2023-10 권고안, 2026 AA 컴플라이언스 타겟」 · 「2026 법적 컴플라이언스 타겟」 · `size` 쿼리 전면 금지 · 375px 를 SC 1.4.10 근거로만 표기 · 관례 행 없음 | SK-07 · SK-12 · ER-03 |
| `design-kit/agents/design-reviewer.md` | `:25` 규칙 7 · `:28` 규칙 8.1 · `:47` 규칙 9 렌더 특칙 · `:109-113` Authenticity | 캡처 점검 인용 없음, 관례 항목 없음. 규칙 8.1 이 `N/A` 를 동의어로 막는다(개정 전 정본) → 새 항목은 규칙 7 의 말을 쓴다 | SK-07 · ER-03 |
| `design-kit/skills/design-test/SKILL.md` | `:24` Gotcha 9 | 「법적 기준」 | SK-12 |
| `design-kit/skills/design-system/SKILL.md` | `:23` Gotcha 8 · `:27` Gotcha 12 · `:29` Gotcha 14 · `:141` Step 5 | `.` 를 금지한 뒤 경로 구분에 `.` 허용, 「2026 Production Ready」 · 「HSL→OKLCH」, 「`$schema`는 validation 용」, Style Dictionary v4 | SK-11 · SK-12 |
| `design-kit/skills/design-system/references/token-principles.md` | `:76` · `:81` · `:94` · `:103` | `$schema` · color 문자열 · dimension 문자열(DTCG 위반 셋 — `dtcg.py` 가 3 을 낸다), 「DTCG 토큰에 `oklch()` 를 쓰고」 | SK-11 |
| `design-kit/evals/evals.json` | `:388` · `:391` (id 19) · `:521` (id 25) | 「시안 5개」 · 「정확히 5개」, 승인 기록 새 칸 사례 없음, 새 절차의 사례 없음 | SK-09 · SK-10 |
| `flutter-toolkit/references/visual-evidence-protocol.md` (읽기만) | `:52` Step 0 관례 표 · `:91` 최대 3 회 · `:106-119` 캡처 점검 목록 | 비교 기준값 — 2 개 이상 · 3 회. 고치지 않는다(Phase 5 범위) | SK-08 |
| `harness/docs/guides/qa-evaluation-guide.md` (읽기만) | `:1223-1294` Canonical Unverified-Evidence Protocol | design-reviewer 복제본과 어긋남 — 미반영 근거 | 배경 표 ① |

구현 후보는 하나다(규약에 정의 · 스킬은 인용). 「세 자리에 같은 목록을 복사」 하는 안은 카이젠 Gotcha 4(audit-criteria 와 Gotcha 중복 금지)와
근거 파일 §2 P4 비고에 어긋나 버렸다.

### Counterpart — 규약을 받아 쓰는 반대편

생산 면(규약)과 소비 면(스킬 · 감사)을 따로 조건으로 둔다.

- 생산: `visual-change-protocol.md` §0 · §2 → SK-01, §3 비교 반복 순서 → SK-02, §3 캡처 점검 목록 → SK-03, §4 승인 기록 → SK-04
- 소비 — 생성 스킬: design-mockup Step 1 · 2 · 5, design-component Step 0, design-guide Step 1 → SK-05
- 소비 — 승인 기록: design-mockup Step 2(읽기) · Step 6(쓰기 틀과 확인 명령), design-concept Step 0(읽기) · Step 7(쓰기 틀과 확인 명령) → SK-06
- 소비 — 감사: audit-criteria Authenticity 행, design-audit Step 2 표 · Gotcha 12, design-reviewer Authenticity · 규칙 9 → SK-07
- 규약 절 번호를 인용하던 기존 문장(§1 · §2 · §4 · §5 · §6 · §7)은 번호가 그대로라 바뀌지 않는다 — 새 절을 §0 으로 앞에 두어 번호를 밀지 않았다(AR-02 가 기존 제목이 하나도 안 빠졌음을 잰다)
- 소비자 없음으로 판정한 것: design-reference · design-test 는 §0 · §3 새 절을 부르지 않는다 — 시각 산출물을 고치는 단계가 없거나(design-reference) 시험을 만드는 스킬이다(design-test). design-test 는 사실 정정 한 줄만 바뀐다(SK-12)

### 개선안 초안

적용할 편집은 전부 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p6b/mock.py`
(sha256 앞 16 자리 `aed436d274a907a1` — 2 회차 검토가 권한 evals id 28 프롬프트 한 줄을 BUILD 가 봉인 전에 고친 판. 1 회차 검토 반영판 `0ec137c2ed0469bb` 은
`p6d/mock.py`, 검토 전 판 `8e34f2eff74a478e` 은 `p6d/mock.v1.py`)에 글자 그대로 있다. 옛 문자열이 정확히 한 번 있어야 치환하고 아니면 `MOCK_FAIL` 로 멈춘다. BUILD 는
`python3 <mock.py> <작업 폴더>` 로 이 치환을 그대로 적용한 뒤 커밋한다. 편집 전 판 사본에 적용한 결과가 아래 `회귀 게이트` 의 「모의본」 이다. 요지:

- 규약 머리: 적용 스킬 목록에 design-component · design-concept 추가, 형제 규약 숫자 문단과 정본 결정 한 줄(결정 2), 그 절이 아직 없다는 한 줄
- 규약 §0 신설 `## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표` — 대상(화면 파일 · 라우트, 화면 자체) · 되말하기(두 갈래면 묻기) · 관례 표(같은 역할 서로 다른 기존
  화면 2 개 이상, 네 칸, 없는 부품 이름 금지, 같은 역할 한정, constants 에 관례, 관례 없음 두 경우)
- 규약 §2 에 요소 하나 지목 문단과 Change Manifest 틀 보존 줄의 이웃 요소 구절, §3 에 `### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한`(다섯 단계 · 표식 · 최대 3 회)과 `### 캡처 점검 목록`(네 항목 ·
  텍스트 200% · 320 CSS px · 실제 글꼴), §4 최소 필드에 `확정 구성` · `폐기한 대안·이유` 와 규칙 두 줄(다시 넣지 않기 · 제품 수준은 경로만)
- design-mockup: Step 1 대상 · 되말하기 한 단락, Step 2 감지 목록에 승인 기록 · 관례 표 두 줄, Step 5 지목 범위(규약 경로 한 번) · 틀 보존 줄의 이웃 요소
  구절 · §3 순서 인용, Step 6 틀 두 칸과 확인 명령 한 줄, Gotcha 10 크기 쿼리 지원 문장
- design-component Step 0 · design-guide Step 1 각 한 단락, design-concept Step 7 틀 폐기 칸과 확인 명령 한 줄 · Step 0 감지 목록에 컨셉 승인 기록 한 줄과
  폐기 안을 다시 제안하지 않는다는 한 줄
- 감사: audit-criteria Authenticity 행 하나, design-audit Step 2 Authenticity 칸 · Gotcha 12 인용 한 문장, design-reviewer Authenticity 한 줄 · 규칙 9 인용 한 문장
- 사실 정정: design-system Gotcha 8 · 12 · 14 · Step 5, token-principles 예시 · 주의 사항, audit-criteria `:41` · `:59` · `:96` · `:97`, design-audit `:72` · `:78`,
  design-guide `:24`, design-test `:24`, mockup-guidelines `:7`(개수 숫자는 적지 않고 Step 3-a 를 가리킨다) · `:67`(44×44 CSS px · Apple HIG 44pt 를 가른다)
- evals: id 19 기대값 3 개, id 25 에 한 줄, id 28 · 29 · 30 신설

## 범위 경계

- 이 Phase 시작 HEAD: `79258900de00e621412e4c436b44028a77d7fb64`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p06-design-kit.md` 의 `end_sha:`
  마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열셋이다 — `design-kit/references/visual-change-protocol.md` · `design-kit/skills/design-mockup/SKILL.md` ·
  `design-kit/skills/design-mockup/references/mockup-guidelines.md` · `design-kit/skills/design-component/SKILL.md` · `design-kit/skills/design-guide/SKILL.md` ·
  `design-kit/skills/design-concept/SKILL.md` · `design-kit/skills/design-audit/SKILL.md` · `design-kit/skills/design-audit/references/audit-criteria.md` ·
  `design-kit/agents/design-reviewer.md` · `design-kit/skills/design-test/SKILL.md` · `design-kit/skills/design-system/SKILL.md` ·
  `design-kit/skills/design-system/references/token-principles.md` · `design-kit/evals/evals.json`. 새 파일은 없다. `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase6-notes.md` · `.harness/.meta/kaizen-0924/phase6-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 `broken` 으로 잰다
- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p06-design-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · DG-01 · DG-04 · ER-04 가 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 은 `design-kit/` 을 건드린 커밋을 경로로 직접 센다(`unsigned`). FIX 가 커밋을 더할 때도 서명을 넣고,
  개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로 `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 **`git add -- <파일…> && git commit -o -- <파일…>` 로 열세 파일만** 싣는다. `.harness/` 파일은 따로 커밋한다(한 커밋에 킷 하나 —
  `validate-post-kaizen.py` scope-isolation). `git add -A` · `git commit -a` · `git stash` 는 쓰지 않는다
- 측정이 기대는 제목은 이름을 바꾸지 않는다: 규약 `## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표` · `## 2. Partial Visual Change Isolation` ·
  `## 3. Before/After Evidence Block` · `### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한` · `### 캡처 점검 목록` · `## 4. Design Approval Record`,
  design-mockup `## Step 1: 화면 요구사항 파악` · `## Step 2: 자동 감지 및 로드` · `### Step 3-a` · `## Step 5: 사용자 선택 및 수정` · `## Step 6: 승인 기록 생성`,
  design-component `## Step 0: 자동 감지 및 로드`, design-guide `## Step 1: 맥락 파악`, design-concept `## Step 0: 자동 감지 및 로드` · `## Step 7: 승인 기록 생성`, design-audit `# Gotchas` ·
  `## Step 2: 감사 카테고리 확인`, audit-criteria `## Authenticity`, design-reviewer `## 핵심 규칙` · `### 10. Authenticity`, design-system `# Gotchas`,
  token-principles `### 최소 예시`
- 공유 파일(`.claude-plugin/marketplace.json` · `design-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 ·
  감사 로그 · 실패 횟수 파일)과 다른 Phase 소관 파일(flutter-toolkit · react-kit 규약, harness 가이드 · 스키마)은 건드리지 않는다 — AR-01 `shared` · `outside`.
  `docs/design/research-log.md` 도 이번에는 고치지 않는다 — 킷 로그 단락은 notes 에 적어 Final 이 옮긴다(ER-04). design-kit README 의 AUTO 구간은 스킬
  frontmatter 를 읽는데 frontmatter 를 바꾸지 않는다(SK-09 `keep` 이 design-mockup description 을 잰다). 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서
  `docs-site-regen` 을 뺀다
- 넘기는 것 — BUILD 가 notes(`.harness/.meta/kaizen-0924/phase6-notes.md`)에 아래 문자열을 **각각 한 번 이상** 적는다(ER-04 가 글자 그대로 센다):
  `skill-design-guide.md` (다음 사이클 Phase 1 — 세 규약이 같이 쓰는 규칙의 정본 절 신설, 결정 2) ·
  `visual-evidence-protocol.md` (다음 사이클 Phase 5 — 그 절을 가리키고 스택 몫만 남긴다) ·
  `render-evidence-protocol.md` (Phase 10 — 리액트 규약에 되말하기 · 관례 표 · 반영 확인 · 캡처 점검 · 3 회 상한이 없다, 다음 사이클엔 정본 절 인용) ·
  `UNVERIFIED_ENV` (다음 사이클 Phase 6 — 배경 표 ①, 다섯 자리) · `design:P2 방향` (사용자 확인 목록 — 한 프로젝트 기억 「여러 개 다 만들어 나란히」 ·
  「시안 추가는 승인 대기 말고 바로 구현」 과 design-mockup 개수 계약 · 매트릭스 사전 합의가 반대 방향) · `F20` (Phase 11 — 제품 수준 폐기 결정 자리를
  정하면 design-kit 승인 기록 폐기 칸이 그 경로를 적는다) · `design-mockup Step 0` (다음 사이클 Phase 6 — 배경 표 ②) · ``버전: `0.1.0` `` (Final — design-kit
  README 의 버전 줄이 plugin.json `0.4.0` 과 다르다) · `docs/design/research-log.md` (Final — 킷 로그 단락을 옮긴다) · `Material 3` (다음 사이클 — 근거 파일 §5 에서
  조회하지 않은 Material 3 Expressive · Apple HIG) · `임계값 다시 정의` (다음 사이클 — 규약 머리는 임계값을 자기 문서에서 다시 정의하지 말라는데
  「2 개 이상」 · 「3 회」 가 스킬 · 감사 다섯 자리에 다시 적혔다. SK-08 은 이번 한 번만 맞춰 보고 다음 변경 때 막을 장치는 없다) ·
  `§3.7 네 칸` (다음 사이클 Phase 6 — 배경 표 Gotcha 8 행, 규약 §3 캡처 실패 줄과 design-reviewer 접미 없는 `[미검증]` 15 줄). 처리 배정표 키 아홉(`F01` · `F04` · `design:P1` ~ `design:P7`)도 notes 에 적는다. 러닝북이 적게 한
  나머지(바꾼 파일 · changelog 한 단락 · 킷 로그 한 단락 · 다음 사이클 메모)도 notes 에. `.github/workflows/ci.yml` 에 넣을 줄은 없다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 harness 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase6-review.md` — 1 회차 `VERDICT: CHANGES`, 마지막 판정은
  2 회차(2026-09-25 06:10) `VERDICT: APPROVE`
- 2 회차 검토 「봉인 전에 넣을 것」 셋은 조건 줄과 측정 값을 바꾸지 않아 BUILD 가 봉인 전에 넣었다 — evals id 28 프롬프트의 기존 화면을 같은 역할(설정 화면 둘)로
  바꾼 `mock.py`(지문은 `개선안 초안` 절), `회귀 게이트` 설명 문단의 줄 끝 공백 문장, 결정 2 의 「(SK-08)」 을 SK-08 이 실제로 재는 범위로 좁힌 문장.
  「notes 다음 사이클 메모로 넘길 것」 둘(SK08 정규식이 「기존 화면이 N 개」 꼴을 세지 않음 · token-principles 가 가리키는 design-system Gotcha 12 의 Figma OKLCH 단정)은 notes 에 적는다
- 검토 결과(`VERDICT: CHANGES`) 반영: 막는 이유 다섯(공통 정의 없이 · zsh 로 돌린 0 · SK-08 붙여 쓴 숫자 · DG-05 저장소 전체 종료 코드 · 결정 4 · 틀 보존 줄)과
  ER-01 FAIL 문장 · 배경 표 ① 사실 정정을 모두 넣었다. 막지 않는 것 일곱도 넣었다 — 넷째(규약 머리의 「그 절은 아직 없다」)만 「다음 사이클 Phase 1 이
  만든다」 를 빼고 넣었다. 규약은 다른 프로젝트에서 읽히는 킷 파일이라 이 레포의 카이젠 차례 이름이 뜻을 갖지 않는다. 바뀐 측정은 반영판 모의본으로 다시 쟀다(`회귀 게이트` 절)
- 오라클 해소: SK-01 ~ SK-09 · SK-12 · ER-03 — 산출물이 스킬 · 문서 문장 자체라 정해진 절 구간에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을
  잘라 재며, 편집 전 파일에서 새 문장 0 · 옛 문장 1 을 봉인 전에 확인했다. 새 문장이 있는 줄을 하나씩 지운 사본 76 개 가운데 그 조건이 읽는 파일을 지운 74 개에서 해당 조건 출력이 모두 바뀌었다
  (`회귀 게이트` 절 문장 삭제 대조)
- 오라클 해소: SK-06 `ka` · SK-10 · SK-11 — 스킬이 가르치는 확인 명령 · JSON 구조 · DTCG 형태를 실제로 돌린 출력이다. 알려진 답: DTCG 옛 예시 위반 3(근거 파일 §3 이
  짚은 세 줄) · 새 예시 0, 승인 기록 틀에서 확인 명령 2
- 오라클 해소: SK-08 — 두 파일에서 숫자를 뽑아 맞대는 계산이다. 양성 대조: 규약의 2 를 3 으로, 3 회를 5 회로 바꾼 사본에서 값 집합이 둘로 갈라진다
- 오라클 해소: ER-01 · ER-02 · AP-01 · RE-01 · RE-02 · AR-02 — 더한 줄 · 제목 · 경로를 세는 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: AR-01 · ER-04 · DG-01 · DG-04 — 커밋 기록(`git log`)과 notes 문자열 · 봉인 검증 함수를 실제로 돌린 출력이다
- 오라클 해소: DG-02 · DG-05 · DG-06 — 린터 · 검사 스크립트를 실제로 돌린 출력이다
- 커버리지 해소: SK-10 — `evals.json` 은 `SK10` 이 읽는 `$EV` 이고, `run-evals.py` 는 이 조건이 재지 않고 DG-05 가 잰다고 적은 참조다
- 커버리지 해소: ER-04 — notes 경로는 공통 정의의 `$NOTES`, 나머지 문자열 스물하나는 `ER04` 함수 안 `for t in …` 인자다(검출기는 함수 이름만 적힌 측정 절의 인자를 읽지 못한다)
- 커버리지 해소: AR-02 — `../` · `.md` 는 대상 경로가 아니라 `AR03` 이 더한 줄에서 찾는 경로꼴의 조각이다
- 커버리지 해소: 조건 산문의 파일 이름은 측정 함수 안의 변수(`$P` · `$MU` · `$MG` · `$CM` · `$GD` · `$CO` · `$DA` · `$AC` · `$DR` · `$DT` · `$DS` · `$TP` · `$EV` · `$FL`)다.
  공통 정의가 그 이름으로 `$END` 판(또는 시작 커밋 판)을 가리킨다. 검출기는 함수 이름만 적힌 측정 절의 인자를 읽지 못한다 — 위 해소가 전부 그 경우다
- 편집 전부터 있던 마크다운 경고는 범위 밖이다 — DG-02 는 더한 줄에 새로 걸린 경고만 잰다
- 기능 조건 20 (Step 6.2 둘째 명령) · 전체 조건 줄 30 — 처음 초안은 21 이라 참조 경로 조건을 AR-02 에 합쳤다

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 도우미 다섯(`common.sh` · `conds.sh` · `dtcg.py` · `fence.py` · `new-warnings.sh`)을 한 폴더 `K` 에 저장한 뒤 **bash** 에서 돈다.
각 도우미 블록은 첫 `#` 주석 줄(셔뱅이 있으면 그 다음 줄)에 파일 이름이 적혀 있다. 아래 명령으로 이 계약에서 그대로 떼어 낸다 — 블록 본문을 한 글자도 바꾸지 않아야
AR-01 의 도우미 지문이 맞는다.

```bash
# 도우미 떼어 내기 — 계약 파일에서 이름 붙은 bash · python 블록을 K 에 저장한다
K=$(mktemp -d); CF=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924/.harness/sprint-contract-kaizen-0924-p06-design-kit.md
awk -v K="$K" '
  /^```(bash|python)$/ { inb = 1; n = 0; name = ""; buf = ""; next }
  inb && /^```$/ { if (name != "") { printf "%s", buf > (K "/" name); close(K "/" name) } inb = 0; next }
  inb { n++; if (name == "" && n <= 2 && match($0, /^# [A-Za-z0-9._-]+\.(sh|py) /)) name = substr($0, 3, RLENGTH - 3); buf = buf $0 "\n" }
' "$CF"
ln -s /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules "$K/node_modules"
printf '%s\n' '{ "config": { "MD013": false } }' > "$K/cfg.markdownlint-cli2.jsonc"
ls "$K"   # cfg.markdownlint-cli2.jsonc common.sh conds.sh dtcg.py fence.py new-warnings.sh node_modules
K="$K" bash -c '. "$K/common.sh"; . "$K/conds.sh"; run_all'   # 또는 조건 하나씩: SK01 · AR01 …
```

`new-warnings.sh` 옆 `node_modules` 는 markdownlint-cli2 가 설치된 폴더다 — 준비 단계 실측(2026-09-25): `.bin/markdownlint-cli2 --version` 첫 줄
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다. 설정은 편집기 마크다운 확장과 같게
MD013(줄 길이)만 끈다. 준비 단계 실측(2026-09-25): `command -v python3` → `/Users/jackson/.pyenv/versions/3.14.3/bin/python3` (3.14.3) · `command -v bash` → `/opt/homebrew/bin/bash` 5.3.9 (측정은 이 bash 로 돌렸다. `/bin/bash` 는 3.2.57) · `git --version` 2.53.0 ·
`command -v sha256sum` → `/sbin/sha256sum`. `common.sh` 는 `W` 가 비어 있으면 작업 폴더로 들어간다 — `W` 는 봉인 전 예행에서만 바꿨다. `END_UNRESOLVED` 가 찍히면
종료 코드 2 로 멈춘다(상한을 못 구하면 `HEAD` 로 재지 않는다). 셸 함수에 기대는 측정(`AR01` · `DG01` · `DG04`)은 함수 정의가 없으면 `DEFS_MISSING` 과 종료 코드 2 를 낸다.
`conds.sh` 는 공통 정의가 없으면 함수를 하나도 만들지 않고 `DEFS_MISSING` 을 낸다 — 공통 정의 없이 `AP-03` 이 `bare_open_total=0 unclosed_total=0` 을 그대로 냈다(검토 실측).
`common.sh` 는 bash 가 아니면 `NOT_BASH` 로 멈춘다 — zsh 에서 SK-12 `old` 가 옛 표현 열 개를 0 으로 냈다(검토 실측).
출력 줄 끝의 공백은 비교하지 않는다 — `toks` 가 값마다 뒤에 공백을 붙인다(SK-01 `b=` · SK-04 · SK-05 · SK-07 · SK-11 · SK-12). AR-01 ② 는 끝 공백까지 적었다.

```bash
# common.sh — 측정 공통 정의 — bash 로 실행한다 (zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash 로 돌린다 (zsh 는 따옴표 없는 변수를 쪼개지 않아 0 이 조용히 나온다)"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다 — C 로케일이면 덜 잡힌다
cd "${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2   # W 는 봉인 전 예행에서만 바꾼다
B=79258900de00e621412e4c436b44028a77d7fb64                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p06-design-kit'
CF=.harness/sprint-contract-kaizen-0924-p06-design-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p06-design-kit.md
NOTES=.harness/.meta/kaizen-0924/phase6-notes.md
EVID=.harness/.meta/evidence/phase6.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
FILES=(design-kit/references/visual-change-protocol.md design-kit/skills/design-mockup/SKILL.md
  design-kit/skills/design-mockup/references/mockup-guidelines.md design-kit/skills/design-component/SKILL.md
  design-kit/skills/design-guide/SKILL.md design-kit/skills/design-concept/SKILL.md design-kit/skills/design-audit/SKILL.md
  design-kit/skills/design-audit/references/audit-criteria.md design-kit/agents/design-reviewer.md
  design-kit/skills/design-test/SKILL.md design-kit/skills/design-system/SKILL.md
  design-kit/skills/design-system/references/token-principles.md design-kit/evals/evals.json)
MDS=("${FILES[@]:0:12}")   # 앞 열둘이 마크다운 — evals.json 만 뺀다
FRE='design-kit/(references/visual-change-protocol\.md|skills/design-mockup/(SKILL|references/mockup-guidelines)\.md|skills/design-(component|guide|concept|test)/SKILL\.md|skills/design-audit/(SKILL|references/audit-criteria)\.md|agents/design-reviewer\.md|skills/design-system/(SKILL|references/token-principles)\.md|evals/evals\.json)'
T=$(mktemp -d); mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" design-kit flutter-toolkit/references/visual-evidence-protocol.md | tar -x -C "$T/B"
git archive "$END" design-kit | tar -x -C "$T/E"
R=$T/E
P=$R/design-kit/references/visual-change-protocol.md
MU=$R/design-kit/skills/design-mockup/SKILL.md;      MG=$R/design-kit/skills/design-mockup/references/mockup-guidelines.md
CM=$R/design-kit/skills/design-component/SKILL.md;   GD=$R/design-kit/skills/design-guide/SKILL.md
CO=$R/design-kit/skills/design-concept/SKILL.md;     DA=$R/design-kit/skills/design-audit/SKILL.md
AC=$R/design-kit/skills/design-audit/references/audit-criteria.md; DR=$R/design-kit/agents/design-reviewer.md
DT=$R/design-kit/skills/design-test/SKILL.md;        DS=$R/design-kit/skills/design-system/SKILL.md
TP=$R/design-kit/skills/design-system/references/token-principles.md; EV=$R/design-kit/evals/evals.json
FL=$T/B/flutter-toolkit/references/visual-evidence-protocol.md   # 형제 규약은 시작 커밋 판으로 잰다 — Phase 5 가 같은 가지에서 고칠 수 있다
RT="$R/design-kit/skills $R/design-kit/agents $R/design-kit/references"   # 스킬이 실제로 읽는 자리 (docs/design 리서치 문서는 뺀다)
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
toks()  { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
labels() { printf '%s\n' "$1" | grep -oE '^[0-9]\. \*\*[^*]+\*\*' | sed -E 's/^[0-9]\. \*\*//; s/\*\*$//' | tr '\n' '|'; echo; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$R/$f"; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

```bash
# conds.sh — 조건마다 측정 함수 하나. common.sh 를 먼저 source 한 bash 에서 부른다 (예: `SK01`)
# 출력 한 줄이 조건 줄에 적힌 기대 문자열과 같아야 PASS 다. 함수는 판정하지 않고 값만 낸다 — 판정은 조건 줄이 한다
type sect toks added url my >/dev/null 2>&1 && [ -n "${END:-}" ] && [ -n "${T:-}" ] || { echo "DEFS_MISSING — common.sh 를 먼저 source 한다"; return 2; }
SK01() {
  local s0; s0=$(sect "$P" '## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표')
  echo "SK-01 a=$(toks "$s0" '1. **대상** — 바꿀 화면의 파일 경로와 라우트' '화면을 가리키는 요청이면 대상은 그 화면 자체다' '2. **되말하기** — 요청을 대상 요소 이름과 배치까지 넣어 한 문장으로 되말한다. 두 갈래로 읽히면 묻고 시작한다' '3. **관례 표** — 앱 코드가 있으면 같은 역할의 서로 다른 기존 화면 **2 개 이상**을 Read 해서' '줄 모양(카드인지 평평한 줄인지) · 칩·뱃지 모양 · 아이콘 뜻(닫기·끝내기·접기) · 재사용 부품(실제' '**코드 검색에서 나오지 않은 부품 이름은 시안·스펙에 쓰지 않는다**' '관례 일치는 **같은 역할**에만 적용한다' '관례를 벗어나는 안은 사용자가 요청하거나')| first=[$(grep -m1 '^## ' "$P")]"
  echo "SK-01 b=$(toks "$(sect "$P" '## 2. Partial Visual Change Isolation')" '**요소 하나를 지목한 요청**(「이 칩만」, 「추가 버튼만 오른쪽으로」)도 같은 규칙을 따른다' '같은 줄·같은 영역의 이웃 요소는 보존 목록에 올린다' '요소 하나를 지목했으면 같은 줄·같은 영역의 이웃 요소와 그 자리')"
}
SK02() {
  local s; s=$(sect "$P" '### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한')
  echo "SK-02 $(toks "$s" '3. **반영 확인** — 새로 찍은 캡처에서 1 의 표식이 바뀌었는지로 판정한다' '판정하지 않는다. 표식이 그대로면 「반영 안 됨」 이다' '반영이 확인되기 전에는 「갱신했다」 고 말하지 않는다' '**스스로 고치기는 최대 3 회**다. 3 회째도 실패하면')| $(labels "$s") in3=$(sect "$P" '## 3. Before/After Evidence Block' | grep -cx '### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한')"
}
SK03() {
  local s; s=$(sect "$P" '### 캡처 점검 목록')
  echo "SK-03 $(toks "$s" '하나라도 걸리면 그 캡처로 PASS 를 주지 않는다' '실제 서비스 글꼴로 그리지 않은 캡처로는 글자 모양을' '넘침은 데이터를 고쳐 재현하지 말고 글자를 키운 상태로 한 장 더 찍는다.' '웹은 텍스트 200% 확대(WCAG 2.2 SC 1.4.4), 앱은 기기 글자 크기 최대다.' '320 CSS px 폭에서 내용·기능이 사라지거나 양방향 스크롤이 생기는지(SC 1.4.10 Reflow)는 따로 판정한다.')| $(labels "$s") in3=$(sect "$P" '## 3. Before/After Evidence Block' | grep -cx '### 캡처 점검 목록')"
}
SK04() {
  echo "SK-04 $(toks "$(sect "$P" '## 4. Design Approval Record')" '- 확정 구성: {화면에 남는 요소와 배치 — 무엇이 어디에 있는가}' '- 폐기한 대안·이유: {이번 결정에서 버린 안·요소와 이유 — 없으면 `없음`}' '**폐기한 대안은 다시 넣지 않는다.**' '제품 요구 수준의 폐기 결정(기능·설정 항목을 없앤다는 결정)은 이 기록에서 새로 정하지 않는다')"
}
SK05() {
  local s1; s1=$(sect "$MU" '## Step 1: 화면 요구사항 파악')
  local a b; a=$(printf '%s\n' "$s1" | grep -nF '§0 의 대상과 되말하기를 응답에 남긴다' | head -1 | cut -d: -f1); b=$(printf '%s\n' "$s1" | grep -nF '불명확하면 사용자에게 확인한다.' | head -1 | cut -d: -f1)
  echo "SK-05 $(toks "$s1" '§0 의 대상과 되말하기를 응답에 남긴다')before=$([ -n "$a" ] && [ -n "$b" ] && [ "$a" -lt "$b" ] && echo 1 || echo 0) | $(toks "$(sect "$MU" '## Step 2: 자동 감지 및 로드')" '- 앱 코드 존재 → §0 관례 표를 만든다. 같은 역할의 서로 다른 기존 화면 2 개 이상을 읽고, 재사용 부품은 grep 으로' '확인한 실제 이름만 쓴다. 관례는 Step 3-a 매트릭스의 `constants` 에 넣는다')| $(toks "$(sect "$MU" '## Step 5: 사용자 선택 및 수정')" '**속성 하나나 요소 하나를 지목한 경우**(보더만·색만·간격만, 이 칩만)' '§3 비교 반복 순서를 따르고, 캡처마다 §3 캡처 점검 목록을 본다' '**특정 속성만 지목한 경우**' '요소 하나를 지목했으면 같은 줄·같은 영역의 이웃 요소와 그 자리')| $(toks "$(sect "$CM" '## Step 0: 자동 감지 및 로드')" '§0 관례 표의 재사용 부품 칸' '이미 있는 부품은 새 컴포넌트로 다시 정의하지 않고 스펙에서' '그 부품을 가리킨다. 코드 검색에서 나오지 않은 부품 이름은 쓰지 않는다')| $(toks "$(sect "$GD" '## Step 1: 맥락 파악')" '그 코드가 쓰는 토큰과 기존 컴포넌트를 Grep/Read 로 찾아' '§0 관례 표 — 같은 역할의 서로 다른 기존 화면 2 개 이상 — 를 근거로 쓴다.')"
}
SK06() {
  local s6; s6=$(sect "$MU" '## Step 6: 승인 기록 생성')
  printf '%s\n' "$s6" | awk '/^```markdown$/{b=1;next} b&&/^```$/{b=0} b' > "$T/appr.md"
  local s7; s7=$(sect "$CO" '## Step 7: 승인 기록 생성')
  printf '%s\n' "$s7" | awk '/^```markdown$/{b=1;next} b&&/^```$/{b=0} b' > "$T/apprc.md"
  echo "SK-06 $(toks "$s6" '- 확정 구성: {화면에 남는 요소와 배치}' '- 폐기한 대안·이유: {이번 결정에서 버린 안·요소와 이유 — 없으면 `없음`}' "grep -cE '^- (확정 구성|폐기한 대안·이유):' .design/approvals/{파일명}.md   # → 2")| $(toks "$s7" '- 폐기한 대안·이유: {이번에 버린 컨셉 안과 이유 — 없으면 `없음`}' "grep -c '^- 폐기한 대안·이유:' .design/approvals/{YYYYMMDD}-concept.md")$(toks "$(sect "$CO" '## Step 0: 자동 감지 및 로드')" '.design/approvals/*-concept.md → 폐기한 컨셉 안 로드' '- 컨셉 승인 기록 존재 → 폐기한 대안·이유 칸의 안은 사용자가 되살리라고 하지 않는 한 다시 제안하지 않는다')| $(toks "$(sect "$MU" '## Step 2: 자동 감지 및 로드')" '.design/approvals/*.md      → 같은 화면의 확정 구성 · 폐기한 대안 로드' '폐기한 대안·요소는 사용자가 되살리라고 하지 않는 한 시안에 다시 넣지 않는다')| ka=$(grep -cE '^- (확정 구성|폐기한 대안·이유):' "$T/appr.md") kc=$(grep -c '^- 폐기한 대안·이유:' "$T/apprc.md")"
}
SK07() {
  local row; row=$(sect "$AC" '## Authenticity' | grep -F '| 같은 역할 관례 일치 |')
  echo "SK-07 rows=$(printf '%s\n' "$row" | grep -c .) $(toks "$row" '같은 역할의 기존 화면 2 개 이상과 줄 모양(카드/평평한 줄) · 칩·뱃지 모양 · 아이콘 뜻이 같다' '역할이 다른 화면은 대조하지 않는다' '[WCAG 2.2 SC 3.2.4](https://www.w3.org/TR/WCAG22/)')| da=$(sect "$DA" '## Step 2: 감사 카테고리 확인' | grep -F '| **Authenticity** |' | grep -cF '같은 역할 기존 화면과 관례 불일치') dr=$(toks "$(sect "$DR" '### 10. Authenticity')" '- 같은 역할 관례 일치 (같은 역할의 기존 화면 2 개 이상과 줄 모양 · 칩·뱃지 모양 · 아이콘 뜻이 같은가 — 역할이 다른 화면은 대조하지 않는다.')| cats=$(grep -cE '^### [0-9]+\. ' "$DR") $(sect "$DA" '## Step 2: 감사 카테고리 확인' | grep -cE '^\| \*\*[A-Z]') $(grep -c '^## ' "$AC") | cite=$(toks "$(sect "$DA" '# Gotchas')" '§3 캡처 점검 목록(넘침 · 깨진 글리프 · 칩·뱃지와 줄 모양 · 디버그 겹침)을 보고, 하나라도 걸린 캡처는 PASS 근거로 쓰지 않는다')$(toks "$(sect "$DR" '## 핵심 규칙')" '§3 캡처 점검 목록(넘침 · 깨진 글리프 · 칩·뱃지와 줄 모양 · 디버그 겹침)을 보고, 하나라도 걸린 캡처는 PASS 근거로 쓰지 않는다')"
}
SK08() {
  local ds dr fs fr
  ds=$(grep -rhoE '기존 화면 \**[0-9]+ ?개' $RT | grep -oE '[0-9]+' | sort -u | tr '\n' ' ')
  fs=$(grep -oE '서로 다른 기존 화면 [0-9]+ 개 이상' "$FL" | grep -oE '[0-9]+' | sort -u | tr '\n' ' ')
  dr=$(grep -rhoE '스스로 고치기(는)? 최대 [0-9]+ ?회' $RT | grep -oE '[0-9]+' | sort -u | tr '\n' ' ')
  fr=$(grep -oE '최대 [0-9]+ 회, 이후 사용자' "$FL" | grep -oE '[0-9]+' | sort -u | tr '\n' ' ')
  echo "SK-08 line=$(grep -cxF '> **세 규약(이 문서 · flutter-toolkit visual-evidence-protocol · react-kit render-evidence-protocol)이 같이 쓰는 규칙의 정본은 harness `skill-design-guide.md` 한 절에 두고, 세 규약에는 스택마다 다른 채널 · 도구 · 명령만 남긴다.**' "$P") screens=[$ds|$fs] retry=[$dr|$fr]"
}
SK09() {
  echo "SK-09 old=$(grep -rnE '시안 ?5 ?개|5 ?개 시안|정확히 5 ?개' $RT "$EV" | grep -c .) $(toks "$(cat "$MG")" '시안은 개수와 무관하게 서로 다른 레이아웃/구성 접근을 사용한다 (개수는 `SKILL.md` Step 3-a 를 따른다):')| e19=$(python3 -c 'import json,sys; e={x["id"]:x for x in json.load(open(sys.argv[1],encoding="utf-8"))["evals"]}[19]; print(int(e["expected_output"]=="하이파이 HTML 시안 3개(개수 미지정) + 각 UI 요소에 유니크 ID 부여"), int(e["assertions"][0]["text"]=="개수를 지정하지 않았으므로 HTML 시안을 정확히 3개 생성한다"))' "$EV") | keep=$(toks "$(sect "$MU" '### Step 3-a')" '| 미지정 | **3** |' '승인받으면 **최대 5**')$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f' "$MU" | grep -cF '(미지정 3 · 사용자 지정 N · 승인 상한 5)')"
}
SK10() {
  echo "SK-10 $(python3 -c '
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))["evals"]; by={e["id"]:e for e in d}
ids=[e["id"] for e in d]
new=[(i,by[i]["skill"],len(by[i]["assertions"]),all(a.get("type") in ("behavior","output") and a.get("text") for a in by[i]["assertions"])) for i in (28,29,30) if i in by]
print("ids_ok=%d" % (ids==list(range(1,31))), "new=%s" % ";".join("%d:%s:%d:%d" % t for t in new), "e25=%d" % sum(a["text"]=="승인 기록에 확정 구성과 폐기한 대안·이유 칸을 포함한다" for a in by[25]["assertions"]))
' "$EV")"
}
SK11() {
  local tp ds tprc dsrc
  tp=$(python3 "$K/dtcg.py" "$TP" '### 최소 예시'); tprc=$?
  ds=$(python3 "$K/dtcg.py" "$DS" '14. **DTCG v1'); dsrc=$?
  echo "SK-11 tp=[$(printf '%s\n' "$tp" | tail -1) rc=$tprc] ds=[$(printf '%s\n' "$ds" | tail -1) rc=$dsrc] | $(toks "$(sect "$DS" '# Gotchas')" '경로 구분은 `/` 또는 `.`만 사용' '토큰·그룹 이름에는 `{` `}` `.` 를 쓰지 않고, 이름을 `$` 로 시작하지 않는다' '`$schema`는 validation 용이다' '`$schema` 는 2025.10 Final Report 의 그룹 속성 목록에 없다')| $(toks "$(cat "$TP")" '`oklch()`를 쓰고 Figma 쪽에는 hex 근사치를 병기' 'color `$value` 는 `oklch()` 같은 CSS 문자열이 아니라 `colorSpace` · `components` 객체다' 'dimension `$value` 도 `"16px"` 문자열이 아니라' '`$schema` 는 2025.10 Final Report 의 그룹 속성 목록에 없다. 도구가 요구하면')"
}
SK12() {
  local o=""; for t in '2026 Production Ready' 'HSL→OKLCH' 'Style Dictionary v4' '2026 Baseline' '법적 표준' '법적 기준' '법적 컴플라이언스' '2026 AA 컴플라이언스 타겟' '`block-size`/`size` 쿼리 금지' '44×44pt 이상'; do o="$o$(grep -rF -- "$t" $RT | grep -c .) "; done
  echo "SK-12 old=[$o] ds=$(toks "$(cat "$DS")" 'Tailwind CSS v4(2025-01-22 발표 · 최신 안정판 v4.3.3, 2026-07-16)가 기본 팔레트를 `rgb` 에서 `oklch` 로 바꿨고' 'Style Dictionary v5 파이프라인 안내' 'v5 는 Node.js 22 이상이 필요하고' 'v5.5.5(2026-09-20)가 고쳤으니')ac=$(grep -cxF '## WCAG 2.2 신규 성공 기준 (W3C 권고안 — 현재 게시본 2024-12-12)' "$AC") $(toks "$(cat "$AC")" '375px 와 2px 허용치는 이 킷의 판정값이다' '`size` 도 유효한 값이며 금지 대상이 아니다' '법적 의무인지는 관할 법령마다 달라 여기서 단정하지 않는다')mg=$(toks "$(cat "$MG")" 'AA 최소는 SC 2.5.8 24×24 CSS px')mu=$(toks "$(cat "$MU")" '크기 쿼리는 Chrome 105 · Firefox 110 · Safari 16 부터 지원한다')da=$(toks "$(cat "$DA")" '(크기 쿼리 지원: Chrome 105 · Firefox 110 · Safari 16)' '판정 기준은 WCAG 2.2 AA이며')gd=$(toks "$(cat "$GD")" '판정 기준은 WCAG 2.2 AA이며')dt=$(toks "$(cat "$DT")" 'WCAG 2.2 AA(4.5:1 WCAG2 공식)가 판정 기준.')"
}
ER01() {
  local n=0 miss=0 f u
  for f in "${FILES[@]}"; do
    while read -r u; do [ -n "$u" ] || continue; n=$((n+1)); grep -qF -- "$u" "$EVID" || { miss=$((miss+1)); echo "  MISS $f $u" >&2; }; done < <(comm -13 <(url < "$T/B/$f") <(url < "$R/$f"))
  done
  local vs vmiss=0 v
  vs=$(added | grep -oE '\bv?[0-9]+\.[0-9]+\.[0-9]+\b' | sed 's/^v//' | sort -u | tr '\n' ' ')
  for v in $vs; do grep -qF -- "$v" "$EVID" || vmiss=$((vmiss+1)); done
  local ds dmiss=0 d
  ds=$(added | grep -oE '\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b' | sort -u | tr '\n' ' ')
  for d in $ds; do [ "$d" = 2026-09-24 ] && continue; grep -qF -- "$d" "$EVID" || dmiss=$((dmiss+1)); done
  echo "ER-01 new_urls=$n miss=$miss versions=[$vs] vmiss=$vmiss dates=[$ds] dmiss=$dmiss"
}
ER02() {
  echo "ER-02 lines=$(added | grep -c .) k02=$(added | grep -cE "$K02") formal=$(added | grep -cE '합니다|됩니다|습니다') names=$(added | grep -ciE 'fit-?pal|mcp__')"
}
ER03() {
  echo "ER-03 $(toks "$(sect "$P" '## 0. 편집 전 확정')" '`관례 없음 — 같은 역할 기존 화면 N 개`' '`관례 없음 — 앱 코드 없음`')| $(toks "$(sect "$AC" '## Authenticity')" '`대상 코드에 해당 요소 부재 — 같은 역할 기존 화면 N 개`')$(toks "$(sect "$DR" '### 10. Authenticity')" '`대상 코드에 해당 요소 부재 — 같은 역할 기존 화면 N 개`')| na=$(grep -rF 'N/A (같은 역할' $RT | grep -c .) rule7=$(grep -cF '"대상 코드에 해당 요소 부재"' "$DR")"
}
AR02() {
  local f d=0 x
  for f in skills/design-mockup/SKILL.md skills/design-component/SKILL.md skills/design-guide/SKILL.md skills/design-concept/SKILL.md skills/design-audit/SKILL.md skills/design-test/SKILL.md skills/design-system/SKILL.md; do
    x=$(diff <(grep -E '^# |^##+ Step' "$T/B/design-kit/$f") <(grep -E '^# |^##+ Step' "$R/design-kit/$f") | grep -c '^[<>]'); d=$((d+x)); done
  for f in agents/design-reviewer.md skills/design-mockup/references/mockup-guidelines.md skills/design-system/references/token-principles.md; do
    x=$(diff <(grep -E '^#+ ' "$T/B/design-kit/$f") <(grep -E '^#+ ' "$R/design-kit/$f") | grep -c '^[<>]'); d=$((d+x)); done
  local ac pa pr
  ac=$(diff <(grep -E '^#+ ' "$T/B/design-kit/skills/design-audit/references/audit-criteria.md") <(grep -E '^#+ ' "$AC") | grep '^[<>]' | tr '\n' '|')
  pa=$(comm -13 <(grep -E '^#+ ' "$T/B/design-kit/references/visual-change-protocol.md" | sort) <(grep -E '^#+ ' "$P" | sort) | tr '\n' '|')
  pr=$(comm -23 <(grep -E '^#+ ' "$T/B/design-kit/references/visual-change-protocol.md" | sort) <(grep -E '^#+ ' "$P" | sort) | grep -c .)
  echo "AR-02 same=$d ac=[$ac] p_added=[$pa] p_removed=$pr"
}
AR03() {
  local f l p n=0 bad=0
  for f in "${MDS[@]}"; do
    while IFS= read -r p; do n=$((n+1)); [ -f "$(dirname "$R/$f")/$p" ] || { bad=$((bad+1)); echo "  BAD $f $p" >&2; }; done < <(git diff --no-index -U0 "$T/B/$f" "$R/$f" | grep '^+' | grep -v '^+++' | grep -oE '`(\.\./)+[^` ]+\.md`' | tr -d '`')
  done
  echo "AR-03 checked=$n unresolved=$bad"
}
RE01() {
  local t o=""; for t in '3. **관례 표** — ' '3. **반영 확인** — ' '4. **디버그 겹침** — '; do o="$o$(grep -rlF -- "$t" $RT | sed "s#^$R/##" | tr '\n' ',') "; done
  echo "RE-01 [$o]"
}
RE02() {
  echo "RE-02 manifest=$(grep -rhcE '^[[:space:]]*## Change Manifest' "$T/B/design-kit/skills" "$T/B/design-kit/agents" "$T/B/design-kit/references" | awk '{s+=$1} END{print s+0}')/$(grep -rhcE '^[[:space:]]*## Change Manifest' $RT | awk '{s+=$1} END{print s+0}') dirs=$(diff <(grep -rhoE '\.design/[a-z]+/' "$T/B/design-kit/skills" "$T/B/design-kit/agents" "$T/B/design-kit/references" | sort -u) <(grep -rhoE '\.design/[a-z]+/' $RT | sort -u) | grep -c '^[<>]')"
}
AP01() {
  echo "AP-01 $(added | grep -oE '\bv?[0-9]+\.[0-9]+\.[0-9]+\b' | sed 's/^v//' | sort -u | tr '\n' ' ')| own=$(added | grep -cF '0.4.0')"
}
AP03() { echo "AP-03 $( (cd "$R" && python3 "$K/fence.py" "${MDS[@]}") | tail -1)"; }
AP04() {
  local s o=""; for s in design-mockup design-component design-guide design-concept design-audit design-test design-system; do o="$o$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f' "$R/design-kit/skills/$s/SKILL.md" | grep -cx "name: $s") "; done
  echo "AP-04 [$o] agent=$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f' "$DR" | grep -cx 'name: design-reviewer')"
}
DG02() {
  local f k o=""
  for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$R/$f" "$T/$k.md"; o="$o$(bash "$K/new-warnings.sh" "$T/$k.0.md" "$T/$k.md" | grep -oE 'new_warnings=[0-9]+|LINT_NOT_RUN' | sed 's/new_warnings=//') "; done
  echo "DG-02 md=[$o] json=$(python3 -c 'import json,sys; json.load(open(sys.argv[1],encoding="utf-8")); print(0)' "$EV" 2>/dev/null || echo 1)"
}
AR01() {
  type unsigned_on >/dev/null && type my >/dev/null && type verify_seal >/dev/null && type sha256_16 >/dev/null || { echo "AR-01 DEFS_MISSING"; return 2; }
  local u a b c s shared own h
  u=$(unsigned_on "$B" "$END" "$SIG" design-kit | grep -c .)
  a=$(my | grep -vE "^(\.harness/|($FRE)$)" | grep -c .); b=$(my | grep -cxE "$FRE")
  c=$(git diff --name-only --diff-filter=A "$B" "$END" -- design-kit | grep -c .)
  shared=$(git log --oneline "$B..$END" -- .claude-plugin/marketplace.json design-kit/.claude-plugin/plugin.json README.md CLAUDE.md .claude/kaizen-input/insights-report.md .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml docs/design | wc -l | tr -d ' ')
  s=$(find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .)
  own=$(verify_seal "$CF" | cut -d' ' -f1)
  h=""; for f in common.sh conds.sh dtcg.py fence.py new-warnings.sh; do h="$h$f:$(sha256_16 < "$K/$f") "; done
  echo "AR-01 unsigned=$u outside=$a mine=$b added_files=$c shared=$shared broken=$s own=$own"
  echo "AR-01 helpers $h"
}
ER04() {
  local t o="" n
  for t in 'skill-design-guide.md' 'visual-evidence-protocol.md' 'render-evidence-protocol.md' 'UNVERIFIED_ENV' 'design:P2 방향' 'F20' 'design-mockup Step 0' '버전: `0.1.0`' 'docs/design/research-log.md' 'Material 3' '임계값 다시 정의' '§3.7 네 칸' 'F01' 'F04' 'design:P1' 'design:P2' 'design:P3' 'design:P4' 'design:P5' 'design:P6' 'design:P7'; do
    n=$(git show "$END:$NOTES" 2>/dev/null | grep -cF -- "$t"); o="$o$([ "$n" -ge 1 ] && echo 1 || echo 0)"; done
  echo "ER-04 $o"
}
DG01() { type my >/dev/null || { echo "DG-01 DEFS_MISSING"; return 2; }; echo "DG-01 $(my | grep -c '^scripts/release.sh$')"; }
DG04() { type my >/dev/null || { echo "DG-04 DEFS_MISSING"; return 2; }; echo "DG-04 $(my | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$')"; }
DG05() {
  git diff --quiet "$END" -- "${FILES[@]}" || { echo "DG-05 GIVEN_NOT_MET 작업 트리가 END 와 다르다"; return 2; }
  local vp fa rc o="" c x r
  vp=$(python3 scripts/validate-plugin.py design-kit 2>&1)
  fa=$(python3 scripts/validate-plugin.py --check=table-integrity,code-fence 2>&1 | grep -E '^ +FAIL ' | grep -cE "$FRE")
  for c in 'sync-docs.py design-kit --check-only' 'run-evals.py design-kit'; do python3 scripts/$c >/dev/null 2>&1; o="$o$? "; done
  # 저장소 전체를 보는 두 검사는 종료 코드와 design-kit 을 가리키는 줄 수를 함께 낸다 — 다른 Phase 가 같은 가지에서 동시에 움직인다
  for c in 'sync-evals.py --check-only' 'validate-doc-contracts.py'; do x=$(python3 scripts/$c 2>&1); r=$?; o="$o$r:$(printf '%s\n' "$x" | grep -cE '\[design-kit\]|design-kit/') "; done
  python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1; rc=$?
  echo "DG-05 v=$(printf '%s\n' "$vp" | grep -cE '^  V([1-9]|10) ') bad=$(printf '%s\n' "$vp" | grep -E '^  V([1-9]|10) ' | grep -cE 'ERROR|FAIL') kitfail=$fa rc=[$o] evals=[$(python3 scripts/run-evals.py design-kit 2>&1 | tail -1)] stale_rc=$rc stale_mine=$(grep -cE "$FRE" "$T/sv.txt")"
}
DG06() {
  local out; out=$(python3 scripts/validate-post-kaizen.py --since "$B" 2>&1)
  echo "DG-06 $(printf '%s\n' "$out" | grep -E ' (scope-isolation|doc-contracts): ' | sed -E 's/^ *//' | cut -c1-60 | tr '\n' '|')"
}
run_all() { AR01; ER04; DG01; DG04; SK01; SK02; SK03; SK04; SK05; SK06; SK07; SK08; SK09; SK10; SK11; SK12; ER01; ER02; ER03; AR02; AR03; RE01; RE02; AP01; AP03; AP04; DG02; }
```

```python
#!/usr/bin/env python3
# dtcg.py <파일> <제목 앞부분> — 그 제목 뒤 첫 json 코드 블록을 DTCG 2025.10 형태로 잰다 (근거: .harness/.meta/evidence/phase6.md §3)
# 블록을 못 찾거나 JSON 이 깨지면 종료 코드 2 — 「위반 0」 으로 조용히 끝나지 않게 한다
import json, re, sys

path, head = sys.argv[1], sys.argv[2]
lines = open(path, encoding="utf-8").read().split("\n")
start = next((i for i, l in enumerate(lines) if l.lstrip().startswith(head)), None)
if start is None:
    print(f"NO_HEADING {head}"); sys.exit(2)
body, inside, indent = [], False, 0
for l in lines[start + 1:]:
    s = l.lstrip()
    if not inside and s.startswith("```json"):
        inside, indent = True, len(l) - len(s); continue
    if inside and s == "```":
        break
    if inside:
        body.append(l[indent:])
if not body:
    print("NO_JSON_BLOCK"); sys.exit(2)
try:
    doc = json.loads("\n".join(body))
except json.JSONDecodeError as e:
    print(f"JSON_ERROR {e}"); sys.exit(2)

viol, tokens = [], 0
ALIAS = re.compile(r"^\{[^{}]+\}$")


def walk(node, path_, inherited):
    global tokens
    for k in node:
        if k == "$schema":
            viol.append(f"{path_ or '/'} $schema")
    t = node.get("$type", inherited)
    if "$value" in node:
        tokens += 1
        v = node["$value"]
        if isinstance(v, str):
            if not ALIAS.match(v):
                viol.append(f"{path_} {t} 문자열 값 {v!r}")
        elif t == "color":
            ok = isinstance(v, dict) and isinstance(v.get("colorSpace"), str) \
                and isinstance(v.get("components"), list) and len(v["components"]) == 3 \
                and all(isinstance(c, (int, float)) for c in v["components"]) \
                and ("hex" not in v or re.fullmatch(r"#[0-9a-fA-F]{6}", str(v["hex"])))
            if not ok:
                viol.append(f"{path_} color 객체 형태 {v!r}")
        elif t == "dimension":
            ok = isinstance(v, dict) and isinstance(v.get("value"), (int, float)) and v.get("unit") in ("px", "rem")
            if not ok:
                viol.append(f"{path_} dimension 객체 형태 {v!r}")
        return
    for k, child in node.items():
        if k.startswith("$"):
            continue
        if any(c in k for c in "{}."):
            viol.append(f"{path_}/{k} 이름에 금지 문자")
        if isinstance(child, dict):
            walk(child, f"{path_}/{k}", t)


walk(doc, "", None)
for v in viol:
    print(f"V {v}")
print(f"tokens={tokens} violations={len(viol)}")
```

```python
# fence.py <파일>… — 여는 펜스에 언어 힌트가 없으면 bare. 4-백틱 바깥 펜스 안의 ``` 는 내용으로 본다
import re, sys
tot_bare = tot_unclosed = 0
for path in sys.argv[1:]:
    open_len = 0; open_ch = ''; bare = []
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line.rstrip('\n'))
        if not m:
            continue
        run, rest = m.group(1), m.group(2).strip()
        if open_len == 0:
            open_len, open_ch = len(run), run[0]
            if not rest:
                bare.append(n)
        elif run[0] == open_ch and len(run) >= open_len and not rest:
            open_len = 0
    tot_bare += len(bare); tot_unclosed += 1 if open_len else 0
    print(f"{path}: bare_open={len(bare)} {bare} unclosed={1 if open_len else 0}")
print(f"bare_open_total={tot_bare} unclosed_total={tot_unclosed}")
```

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

### 봉인 전 실측 — 편집 전 판과 모의본

「편집 전」 은 시작 커밋 판(`end_sha` 를 `7925890` 으로 둔 예행 저장소), 「모의본」 은 같은 판에 `mock.py` 를 적용해 서명 커밋으로 올린 예행 저장소에서
`run_all` 을 돌린 값이다(2026-09-25, 검토 반영 뒤 다시 잼 — 예행 저장소 `p6d2/rh` · `p6d2/rh0`). 조건 줄의 요구값과 한 글자씩 같은지는 각 조건에 적었다.

| 조건 | 편집 전 | 모의본 |
| --- | --- | --- |
| SK-01 | `a=0 0 0 0 0 0 0 0` · `first=[## 1. …]` · `b=0 0 0` | `a=1 1 1 1 1 1 1 1` · `first=[## 0. …]` · `b=1 1 1` |
| SK-02 · SK-03 · SK-04 | 전부 0 · `in3=0` | 전부 1 · 단계 이름 순서 요구값 · `in3=1` |
| SK-05 · SK-06 · SK-07 | 새 문장 0 · 옛 문구 1 (SK-05 `\| 0 0 1 0 \|`) · `ka=0 kc=0` · `cats=10 10 12` | 새 문장 1 · 옛 문구 0 (SK-05 `\| 1 1 0 1 \|`) · `ka=2 kc=1` · `cats=10 10 12` |
| SK-08 | `line=0` · design-kit 쪽 숫자 없음 · flutter 쪽 `2` · `3` (붙여 쓴 꼴까지 읽는 측정으로) | `line=1` · 양쪽 `2` · 양쪽 `3` |
| SK-09 | `old=3 0` · `e19=0 0` · `keep=1 1 1` | `old=0 1` · `e19=1 1` · `keep=1 1 1` |
| SK-10 | `ids_ok=0 new= e25=0` | 요구값 |
| SK-11 | `tp=[tokens=3 violations=3 rc=0]` · 옛 문장 1 · 새 문장 0 | `violations=0` · 옛 문장 0 · 새 문장 1 |
| SK-12 | `old=[1 1 1 3 2 1 1 1 1 1 ]` · 새 문장 0 | `old` 전부 0 · 새 문장 전부 1 |
| ER-01 · ER-02 | 더한 줄 없음 | `new_urls=7 miss=0 dmiss=0` · `lines=212 k02=0 formal=0 names=0` |
| ER-03 | 새 문장 넷 0 · `na=0 rule7=1` | 새 문장 넷 1 · `na=0 rule7=1` |
| AR-02 | 바뀐 제목 없음 · `checked=0` | 요구값 · `checked=9 unresolved=0` |
| RE-01 · RE-02 | `[   ]` · `manifest=2/2 dirs=0` | 세 칸 모두 규약 하나 · `manifest=2/2 dirs=0` |
| AP-01 · AP-03 · AP-04 | `own=0` · `0 0` · `[1 1 1 1 1 1 1 ] agent=1` | `own=0` · `bare_open_total=0 unclosed_total=0` · 같음 |
| DG-02 | 더한 줄 없음 | 열두 칸 0 · `json=0` |

### 문장 삭제 대조

러닝북 규칙(「특정 문장이 있어야 한다는 조건은 그 문장만 지운 사본에서 FAIL 이 나는지」)대로, 조건 함수 `SK01` ~ `SK09` · `SK11` · `SK12` · `ER03` 이 재는
새 문장마다 그 문장이 있는 줄 하나만 지운 사본을 만들어 그 조건 함수를 다시 돌렸다(검토 반영 뒤 다시 돌림 — 줄 번호는 반영판 모의본 기준, `p6d2/dt3.tsv`).
사본 76 개 가운데 74 개가 출력이 바뀌었다. 나머지 2 개는 같은 문장이 그 조건이 읽지 않는 파일에도 있어 그 파일을 지운 사본이다: 틀 줄 `- 폐기한 대안·이유: …` 가
규약 §4 와 design-mockup Step 6 에 함께 있다. 각 조건이 읽는 파일 쪽 삭제는 둘 다 바뀌었다. 아래 수는 조건마다 출력이 바뀐 사본 수다(절 제목 줄 포함).

| 조건 | SK-01 | SK-02 | SK-03 | SK-04 | SK-05 | SK-06 | SK-07 | SK-08 | SK-09 | SK-11 | SK-12 | ER-03 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 출력이 바뀐 사본 | 12 | 5 | 6 | 4 | 10 | 8 | 5 | 1 | 1 | 5 | 12 | 5 |

SK-10 은 JSON 이라 줄 삭제 대신 항목을 뺐다(SK-10 양성 대조). 삭제 대조를 처음 돌렸을 때 SK-11 의 token-principles `$schema` 줄을 지워도 출력이 그대로였다 —
그 문장을 재는 토큰이 design-system 에만 있었다. 그래서 SK-11 (c) 에 `$schema` 문장을 더했고 다시 돌려 바뀌었다.

### 양성 · 음성 대조 (모의본 사본에 알려진 나쁜 변경 하나씩)

각 조건 줄의 `양성 대조:` 에 적은 값이 전부 실제로 나왔다 — SK-08 `screens=[2 3 |2 ]` · `retry=[3 5 |3 ]`(띄어 쓴 꼴 · 붙여 쓴 꼴 둘 다), SK-09 `old=1 1 | e19=1 0`, SK-10 `ids_ok=0` · `e25=0`,
SK-11 `violations=1`, ER-01 `miss=1` · `vmiss=1` · `dmiss=1`, ER-02 `k02=1 formal=1 names=1`, ER-03 `na=1`, AR-02 `same=1` · `unresolved=1`,
RE-01 셋째 칸 두 파일, RE-02 `manifest=2/3 dirs=1`, AP-01 `own=1`, AP-03 `bare_open_total=1`, AP-04 `[1 1 0 1 1 1 1 ]`, DG-02 첫 칸 `1`,
DG-05 셋째 칸 `1:1` · 첫 칸 `1`. 검토 반영 뒤 바뀐 측정(SK-08 · DG-05 · DG-02)은 반영판 모의본에서 다시 돌렸다.

### 예행 — 커밋 기록을 재는 조건

`git clone --shared` 로 만든 예행 저장소에서 시작 커밋 `7925890` 위에 이 Phase 가 할 커밋을 차례로 올렸다 — 봉인 커밋(이 계약 사본을 봉인해 싣기) → 구현 커밋(열세 파일) →
`end_sha` 커밋 → notes 커밋(스물한 문자열을 담은 모의 notes) → `end_sha` 덧붙임 커밋. 모두 서명 줄을 달았다. 그 저장소에 `W` 를 두고 떼어 낸 도우미로 돌린 값:

```text
AR-01 unsigned=0 outside=0 mine=13 added_files=0 shared=0 broken=0 own=SEAL_OK
AR-01 helpers common.sh:64f32d049a33c4a8 conds.sh:5fe82e178530b978 dtcg.py:ab7473168fd8f9c7 fence.py:dae506ed24cc7822 new-warnings.sh:e485430011be3e1a
ER-04 111111111111111111111
DG-01 0
DG-04 0
DG-05 v=10 bad=0 kitfail=0 rc=[0 0 0:0 0:0 ] evals=[Total: 30 passed, 0 failed] stale_rc=0 stale_mine=0
DG-06 [ PASS  ] ✓ scope-isolation: no cross-phase commits (5 commi|[ PASS  ] ✓ doc-contracts: doc-contracts: 1 블록 검사 · violatio|
```

같은 예행 저장소에서 SK-01 ~ AP-04 · DG-02 값도 위 「모의본」 열과 한 글자도 다르지 않았다. 음성 대조(예행 사본마다 하나씩):

- 서명 없이 `design-kit/README.md` 를 고친 커밋을 얹고 `end_sha` 를 옮긴 사본 — `unsigned=1 outside=0` (서명 줄 목록에는 안 보이고 경로 직접 세기에만 걸린다)
- 서명을 달고 루트 `README.md` 를 고친 커밋을 얹은 사본 — `outside=1 shared=1`
- 봉인 뒤 SK-04 조건 줄 한 글자를 고친 사본 — `broken=1 own=SEAL_BROKEN`
- notes 커밋 없이 `end_sha` 가 구현 커밋인 사본 — `ER-04 000000000000000000000`
- 개정 파일이 없는 지금 작업 폴더 — `common.sh` 가 `END_UNRESOLVED` 를 찍고 종료 코드 2
- zsh 로 source — `NOT_BASH` · 종료 코드 2 (같은 zsh 에서 DG-05 식 `python3 scripts/$c` 는 `$c` 가 안 쪼개져 `sync-evals` 칸이 `2:0` 이 된다 — 봉인 전 실측)
- `conds.sh` 만 source 한 bash — `DEFS_MISSING` 과 source 종료 코드 2 뒤 `AP03` · `AP01` · `ER01` · `run_all` 이 `command not found`, PASS 줄 없음
- 다른 킷(`backend-kit`) `evals.json` 한 항목의 `skill` 을 없는 이름으로 바꾼 사본 — DG-05 셋째 칸 `1:0` (남의 킷 어긋남은 이 조건을 떨어뜨리지 않는다)
- 봉인 전인 지금 작업 폴더의 이 계약은 `SEAL_ABSENT` 다 — 봉인을 빠뜨리면 `own` 이 떨어진다

## Skill

- [ ] SK-01: 공유 규약이 편집 전에 대상 · 되말하기 · 관례 표를 남기게 하고 요소 하나 지목까지 부분 변경 규칙을 넓힌다 (F01 · design:P1 · design:P3 — 규약 쪽) — `design-kit/references/visual-change-protocol.md` 의 첫 `## ` 제목이 `## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표` 이고, 그 절에 여덟 문장(대상 = 화면 파일 경로와 라우트 · 화면을 가리키면 그 화면 자체 · 되말하기 한 문장과 두 갈래면 묻기 · 같은 역할의 서로 다른 기존 화면 **2 개 이상** · 관례 표 네 칸 · 코드 검색에 없는 부품 이름 금지 · 같은 역할에만 적용 · 관례 이탈은 요청 · 승인 때만)이 각 1 건, `## 2. Partial Visual Change Isolation` 절에 요소 하나 지목 문장과 이웃 요소 보존 문장, Change Manifest 틀 보존 줄의 이웃 요소 구절이 각 1 건이다 [exact, enumerated]
      (측정: `SK01` 두 줄 — `SK-01 a=` 뒤 여덟 값이 모두 1 이고 `first=[## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표]`, `SK-01 b=` 뒤 세 값이 모두 1.
       봉인 전 실측: 편집 전 `a=0 0 0 0 0 0 0 0 | first=[## 1. Visual Source of Truth Precedence — 무엇이 진실인가]` · `b=0 0 0`. 모의본 요구값.
       문장 삭제 대조: 이 조건이 재는 문장 12 개(절 제목 포함) 각각의 줄만 지운 사본에서 출력이 12 개 모두 바뀐다)
- [ ] SK-02: 공유 규약 §3 에 비교 반복 순서가 있고 반영 확인과 스스로 고치기 상한 3 회를 적는다 (design:P6 · F03 · F26 디자인 쪽) — `## 3. Before/After Evidence Block` 절 안에 `### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한` 이 1 건이고, 그 절의 번호 단계 굵은 이름이 순서대로 `기준 캡처|한 번에 한 의도|반영 확인|재캡처|대조|` 이며, 네 문장(표식이 바뀌었는지로 반영 판정 · 성공 메시지만으로 판정하지 않고 표식이 그대로면 반영 안 됨 · 반영 확인 전에 갱신했다고 말하지 않음 · 스스로 고치기 최대 3 회와 3 회째 실패 뒤 사용자에게 넘김)이 각 1 건이다 [exact, enumerated]
      (측정: `SK02` 한 줄이 `SK-02 1 1 1 1 | 기준 캡처|한 번에 한 의도|반영 확인|재캡처|대조| in3=1`.
       봉인 전 실측: 편집 전 `SK-02 0 0 0 0 |  in3=0`. 모의본 요구값. 문장 삭제 대조: 5 개 모두 출력이 바뀐다)
- [ ] SK-03: 공유 규약 §3 에 캡처 점검 목록 넷과 큰 글자 캡처 · Reflow 판정을 적는다 (design:P4 · F04 — 규약 쪽) — `## 3. Before/After Evidence Block` 절 안에 `### 캡처 점검 목록` 이 1 건이고, 굵은 항목 이름이 순서대로 `글자 넘침|깨진 글리프|칩·뱃지와 줄 모양|디버그 겹침|` 이며, 다섯 문장(하나라도 걸리면 PASS 를 주지 않음 · 실제 글꼴이 아닌 캡처로 글자 모양 판정 금지 · 넘침을 데이터로 재현하지 말고 글자를 키워 한 장 더 · 웹은 텍스트 200% 확대(WCAG 2.2 SC 1.4.4) · 320 CSS px Reflow(SC 1.4.10) 따로 판정)이 각 1 건이다 [exact, enumerated]
      (측정: `SK03` 한 줄이 `SK-03 1 1 1 1 1 | 글자 넘침|깨진 글리프|칩·뱃지와 줄 모양|디버그 겹침| in3=1`.
       봉인 전 실측: 편집 전 `SK-03 0 0 0 0 0 |  in3=0`. 모의본 요구값. 문장 삭제 대조: 6 개 모두 출력이 바뀐다)
- [ ] SK-04: 공유 규약 §4 승인 기록 최소 필드에 확정 구성 · 폐기한 대안 칸이 있고 폐기 규칙 두 줄이 있다 (design:P5 — 규약 쪽 · 결정 3) — `## 4. Design Approval Record` 절에 `- 확정 구성:` 틀 줄 · `- 폐기한 대안·이유:` 틀 줄 · `**폐기한 대안은 다시 넣지 않는다.**` · 제품 요구 수준 폐기 결정은 새로 정하지 않는다는 문장이 각 1 건이다 [exact, enumerated]
      (측정: `SK04` 한 줄이 `SK-04 1 1 1 1`. 봉인 전 실측: 편집 전 `SK-04 0 0 0 0`. 모의본 요구값. 문장 삭제 대조: 4 개 모두 출력이 바뀐다)
- [ ] SK-05: 생성 스킬 셋이 규약 §0 · §2 · §3 을 부른다 (F01 · design:P1 · design:P3 — 소비 쪽) — (a) design-mockup `## Step 1: 화면 요구사항 파악` 에 §0 대상 · 되말하기를 남기라는 문장이 1 건이고 그 줄이 `불명확하면 사용자에게 확인한다.` 보다 앞선다 (b) `## Step 2: 자동 감지 및 로드` 에 앱 코드 → §0 관례 표 두 줄이 각 1 건 (c) `## Step 5: 사용자 선택 및 수정` 에 속성 하나나 요소 하나 지목 문장 1 · §3 순서와 점검 목록 인용 1 · 옛 문구 `**특정 속성만 지목한 경우**` 0 · Change Manifest 틀 보존 줄의 이웃 요소 구절 1 (d) design-component `## Step 0: 자동 감지 및 로드` 에 재사용 부품 칸 세 문장 각 1 (e) design-guide `## Step 1: 맥락 파악` 에 토큰 · 기존 컴포넌트 탐색 문장과 §0 관례 표 근거 문장 각 1 [exact, enumerated]
      (측정: `SK05` 한 줄이 `SK-05 1 before=1 | 1 1 | 1 1 0 1 | 1 1 1 | 1 1`.
       봉인 전 실측: 편집 전 `SK-05 0 before=0 | 0 0 | 0 0 1 0 | 0 0 0 | 0 0` — 옛 문구가 편집 전 1 이라 (c) 셋째 값이 살아 있다. 모의본 요구값. 문장 삭제 대조: 10 개 모두 출력이 바뀐다)
- [ ] SK-06: 승인 기록을 쓰고 읽는 스킬이 새 칸을 쓴다 (design:P5 — 소비 쪽 · 결정 3) — (a) design-mockup `## Step 6: 승인 기록 생성` 틀에 `- 확정 구성:` · `- 폐기한 대안·이유:` 줄과 확인 명령 `grep -cE '^- (확정 구성|폐기한 대안·이유):' .design/approvals/{파일명}.md   # → 2` 가 각 1 건 (b) design-concept `## Step 7: 승인 기록 생성` 틀에 `- 폐기한 대안·이유:` 줄과 확인 명령 `grep -c '^- 폐기한 대안·이유:' .design/approvals/{YYYYMMDD}-concept.md` 가 각 1 건, `## Step 0: 자동 감지 및 로드` 에 컨셉 승인 기록 로드 줄과 폐기한 안을 다시 제안하지 않는다는 줄이 각 1 건 (c) design-mockup `## Step 2: 자동 감지 및 로드` 에 승인 기록 로드 줄과 폐기한 대안을 다시 넣지 않는다는 줄이 각 1 건 (d) 알려진 답 — design-mockup Step 6 의 `markdown` 틀 블록을 파일로 떼어 (a) 의 확인 명령을 돌리면 2, design-concept Step 7 틀 블록에 (b) 의 확인 명령을 돌리면 1 [exact, enumerated]
      (측정: `SK06` 한 줄이 `SK-06 1 1 1 | 1 1 1 1 | 1 1 | ka=2 kc=1`.
       봉인 전 실측: 편집 전 `SK-06 0 0 0 | 0 0 0 0 | 0 0 | ka=0 kc=0` — 편집 전 틀에서 같은 확인 명령이 0 이라 (d) 가 틀의 칸을 실제로 잰다. 모의본 요구값. 문장 삭제 대조: 8 개 모두 출력이 바뀐다)
- [ ] SK-07: 감사 쪽 세 자리가 같은 역할 관례 항목을 갖고 캡처 점검 목록을 인용한다 (design:P7 · design:P4 — 소비 쪽) — (a) audit-criteria `## Authenticity` 절에 `| 같은 역할 관례 일치 |` 로 시작하는 행이 1 개이고 그 행에 세 토큰(같은 역할 기존 화면 2 개 이상과 줄 모양 · 칩·뱃지 모양 · 아이콘 뜻 대조 · 역할이 다른 화면은 대조하지 않음 · WCAG 2.2 SC 3.2.4 링크)이 각 1 (b) design-audit Step 2 표 Authenticity 행에 `같은 역할 기존 화면과 관례 불일치` 1 (c) design-reviewer `### 10. Authenticity` 에 같은 역할 관례 일치 항목 1 (d) 카테고리 수가 그대로 — design-reviewer `### N.` 10 · design-audit Step 2 표 굵은 행 10 · audit-criteria `## ` 12 (e) design-audit `# Gotchas` · design-reviewer `## 핵심 규칙` 에 §3 캡처 점검 목록 인용 문장이 각 1 [exact, enumerated]
      (측정: `SK07` 한 줄이 `SK-07 rows=1 1 1 1 | da=1 dr=1 | cats=10 10 12 | cite=1 1`.
       봉인 전 실측: 편집 전 `SK-07 rows=0 0 0 0 | da=0 dr=0 | cats=10 10 12 | cite=0 0`. 모의본 요구값. 문장 삭제 대조: 5 개 모두 출력이 바뀐다)
- [ ] SK-08: 형제 규약과 숫자가 같고 세 규약 정본 결정이 한 줄로 있다 (러닝북 Phase 6 · 결정 1 · 결정 2) — (a) 규약에 정본 결정 줄 `> **세 규약(이 문서 · flutter-toolkit visual-evidence-protocol · react-kit render-evidence-protocol)이 같이 쓰는 규칙의 정본은 harness `skill-design-guide.md` 한 절에 두고, 세 규약에는 스택마다 다른 채널 · 도구 · 명령만 남긴다.**` 가 줄 전체로 1 건 (b) design-kit 이 스킬로 읽는 자리(`skills` · `agents` · `references`)의 「기존 화면 N 개」(붙여 쓴 「N개」 포함) 숫자 집합이 flutter 규약(시작 커밋 판)의 「서로 다른 기존 화면 N 개 이상」 집합과 같고 값이 하나(`2`) (c) 「스스로 고치기 최대 N 회」(붙여 쓴 「N회」 포함) 숫자 집합이 flutter 규약의 「최대 N 회, 이후 사용자」 집합과 같고 값이 하나(`3`) [exact, enumerated]
      (측정: `SK08` 한 줄이 `SK-08 line=1 screens=[2 |2 ] retry=[3 |3 ]`.
       봉인 전 실측: 편집 전 `SK-08 line=0 screens=[|2 ] retry=[|3 ]`. 모의본 요구값. 양성 대조: 규약의 `**2 개 이상**` 을 `**3 개 이상**` 으로 바꾼 사본 `screens=[2 3 |2 ]`, `최대 3 회` 를 `최대 5 회` 로 바꾼 사본 `retry=[3 5 |3 ]`, audit-criteria 새 행을 「기존 화면 3개 이상」 · design-mockup Step 5 를 「스스로 고치기 최대 5회」 로 바꾼 사본 `screens=[2 3 |2 ]` · `retry=[3 5 |3 ]` (띄어쓰기 없는 꼴을 못 읽던 검토 전 측정은 이 사본에서 `screens=[2 ]` · `retry=[3 ]` 로 요구값 쪽 값만 냈다). 문장 삭제 대조: 정본 결정 줄을 지운 사본 `line=0`)
- [ ] SK-09: 시안 개수 규칙이 파일마다 같다 — 방향은 바꾸지 않는다 (design:P2 부분) — (a) design-kit 이 스킬로 읽는 자리와 `evals.json` 에 `시안 5개` · `5개 시안` · `정확히 5개` 꼴이 0 줄 (b) mockup-guidelines 에 개수 참조 문장 1 (c) evals id 19 의 `expected_output` 이 `하이파이 HTML 시안 3개(개수 미지정) + 각 UI 요소에 유니크 ID 부여` 이고 첫 assertion 이 `개수를 지정하지 않았으므로 HTML 시안을 정확히 3개 생성한다` (d) 규칙 자체는 그대로 — design-mockup `### Step 3-a` 의 `| 미지정 | **3** |` · `승인받으면 **최대 5**` 와 frontmatter description 의 `(미지정 3 · 사용자 지정 N · 승인 상한 5)` 가 각 1 [exact, enumerated]
      (측정: `SK09` 한 줄이 `SK-09 old=0 1 | e19=1 1 | keep=1 1 1`.
       봉인 전 실측: 편집 전 `SK-09 old=3 0 | e19=0 0 | keep=1 1 1` (3 = `evals.json:388` · `:391` · `mockup-guidelines.md:7`). 모의본 요구값. 양성 대조: id 19 첫 assertion 을 옛 문구로 되돌린 사본 `old=1 1 | e19=1 0`)
- [ ] SK-10: evals 가 새 절차의 사례를 갖는다 (카이젠 스킬 Step 4) — `evals.json` 의 id 가 1 ~ 30 이 빠짐없이 차례로 있고, id 28 · 29 는 `design-mockup` · id 30 은 `design-audit` 이며 각각 assertion 이 3 개 이상이고 모든 assertion 의 `type` 이 `behavior` 또는 `output` 이며 `text` 가 비어 있지 않고, id 25 에 `승인 기록에 확정 구성과 폐기한 대안·이유 칸을 포함한다` assertion 이 1 개다. `run-evals.py` 통과는 DG-05 가 잰다 [exact, enumerated]
      (측정: `SK10` 한 줄이 `SK-10 ids_ok=1 new=28:design-mockup:4:1;29:design-mockup:4:1;30:design-audit:3:1 e25=1`.
       봉인 전 실측: 편집 전 `SK-10 ids_ok=0 new= e25=0`. 모의본 요구값. 양성 대조: id 30 을 뺀 사본 `ids_ok=0`, id 25 의 새 assertion 을 뺀 사본 `e25=0`)
- [ ] SK-11: DTCG 예시와 이름 규칙이 2025.10 규격과 맞는다 (근거 파일 §3 · §4-9) — (a) `dtcg.py` 가 token-principles `### 최소 예시` 의 json 블록에서 `violations=0` · 종료 코드 0, design-system Gotcha 14 블록에서도 `violations=0` · 종료 코드 0 (b) design-system `# Gotchas` 에서 옛 문장 `경로 구분은 `/` 또는 `.`만 사용` · `` `$schema`는 validation 용이다 `` 0, 새 문장(이름에 `{` `}` `.` 금지와 `$` 시작 금지 · `$schema` 는 그룹 속성 목록에 없음) 각 1 (c) token-principles 에서 옛 문장(`` `oklch()`를 쓰고 Figma 쪽에는 hex 근사치를 병기 ``) 0, 새 문장 셋(color 객체 · dimension 객체 · `$schema`) 각 1 [exact, enumerated]
      (측정: `SK11` 한 줄이 `SK-11 tp=[tokens=3 violations=0 rc=0] ds=[tokens=2 violations=0 rc=0] | 0 1 0 1 | 0 1 1 1`.
       봉인 전 실측 — 알려진 답: 편집 전 `tp=[tokens=3 violations=3 rc=0]` (근거 파일 §3 이 짚은 `$schema` · color 문자열 · dimension 문자열 셋) · `ds=[tokens=2 violations=0 rc=0]` · `1 0 1 0` · `1 0 0 0`. 모의본 요구값. 양성 대조: 모의본 dimension 을 `"16px"` 로 되돌린 사본 `violations=1`. 제목을 못 찾으면 `NO_HEADING` 과 종료 코드 2 — rc 값이 이를 잡는다)
- [ ] SK-12: 버전 · 날짜 · WCAG · CSS 사실을 근거 파일 값으로 고친다 (근거 파일 §3 · §4-10) — (a) design-kit 이 스킬로 읽는 자리에서 옛 표현 열(`2026 Production Ready` · `HSL→OKLCH` · `Style Dictionary v4` · `2026 Baseline` · `법적 표준` · `법적 기준` · `법적 컴플라이언스` · `2026 AA 컴플라이언스 타겟` · `` `block-size`/`size` 쿼리 금지 `` · `44×44pt 이상`)이 모두 0 줄 (b) 새 문장 — design-system 넷(Tailwind 발표일 · 최신판 · `rgb` → `oklch` / Style Dictionary v5 / Node.js 22 / v5.5.5) · audit-criteria 제목 줄 `## WCAG 2.2 신규 성공 기준 (W3C 권고안 — 현재 게시본 2024-12-12)` 과 세 문장(375px 는 킷 판정값 · `size` 는 금지 대상 아님 · 법적 의무 단정하지 않음) · mockup-guidelines AA 24×24 · design-mockup 크기 쿼리 지원 · design-audit 둘 · design-guide 하나 · design-test 하나가 각 1 [exact, enumerated]
      (측정: `SK12` 한 줄이 `SK-12 old=[0 0 0 0 0 0 0 0 0 0 ] ds=1 1 1 1 ac=1 1 1 1 mg=1 mu=1 da=1 1 gd=1 dt=1`.
       봉인 전 실측: 편집 전 `old=[1 1 1 3 2 1 1 1 1 1 ]` · 새 문장 전부 0. 모의본 요구값. 문장 삭제 대조: 새 문장 12 개(제목 줄 포함) 모두 출력이 바뀐다)

## Script

- [ ] SC-00: N/A (이 Phase 는 `scripts/release.sh` · 버전 올리기 · `marketplace.json` 을 건드리지 않는다 — 공유 파일이라 Final 몫이다. 측정: AR01 의 `shared=0` 과 `outside=0`)

## Error

- [ ] ER-01: 더한 URL · 날짜가 근거 파일에 있다 — 러닝북 「근거 파일에 없는 URL · 버전 · 수치를 지어내지 마라」 — 열세 파일을 파일마다 시작 커밋 판과 비교해 새로 생긴 URL 이 모두 합쳐 1 개 이상이고(측정이 살아 있다) 그 가운데 근거 파일에 없는 것이 0, 더한 줄의 날짜(`20YY-MM-DD`) 가운데 `/insights` 보고서 날짜 `2026-09-24` 말고 근거 파일에 없는 것이 0 이다. 비교는 파일마다 한다 [exact]
      (측정: `ER01` 한 줄에서 `new_urls` 가 1 이상 · `miss=0` · `dmiss=0`.
       봉인 전 실측: 모의본 `new_urls=7 miss=0 … dates=[2024-12-12 2025-01-22 2026-07-16 2026-09-20 2026-09-24 ] dmiss=0`. 양성 대조: 모의본 규약 끝에 `<https://example.com/not-in-evidence>` · `2031-01-01` 을 더한 사본 `miss=1` · `dmiss=1`)
- [ ] ER-02: 더한 줄의 말투가 레포 규칙을 지킨다 (러닝북 말투 · 문서 규칙, tone-kit `locale-korean.md` K-02 · K-04) — 열세 파일의 더한 줄에서 번역투 여섯 꼴(K-02 치환표 grep) 0 · `합니다` · `됩니다` · `습니다` 0 · 특정 앱 이름(`fit-pal` · `fitpal`)과 MCP 도구 이름꼴(`mcp__`) 0 이고, 더한 줄이 1 개 이상이다 [exact]
      (측정: `ER02` 한 줄에서 `lines` 가 1 이상 · `k02=0 formal=0 names=0`. 봉인 전 실측: 모의본 `lines=212 k02=0 formal=0 names=0`. 양성 대조: `이 값은 배경에 적용됩니다. fit-pal 에서 보았다.` 한 줄을 더한 사본 `k02=1 formal=1 names=1`)
- [ ] ER-03: 같은 역할 기존 화면이 모자라거나 앱 코드가 없을 때의 처리를 적는다 (design:P1 · design:P7 경계 · 결정 4) — (a) 규약 §0 에 `` `관례 없음 — 같은 역할 기존 화면 N 개` `` · `` `관례 없음 — 앱 코드 없음` `` 각 1 (b) audit-criteria Authenticity · design-reviewer Authenticity 에 `` `대상 코드에 해당 요소 부재 — 같은 역할 기존 화면 N 개` `` 각 1 (c) design-kit 이 스킬로 읽는 자리에 `N/A (같은 역할` 0 줄 — design-reviewer 규칙 8.1 이 아직 `N/A` 를 동의어로 막으므로(배경 표 ①) 규칙 7 의 말을 쓴다 (d) design-reviewer 에 규칙 7 의 `"대상 코드에 해당 요소 부재"` 가 1 [exact, enumerated]
      (측정: `ER03` 한 줄이 `ER-03 1 1 | 1 1 | na=0 rule7=1`. 봉인 전 실측: 편집 전 `ER-03 0 0 | 0 0 | na=0 rule7=1`. 모의본 요구값. 양성 대조: audit-criteria 에 `N/A (같은 역할 기존 화면 1 개)` 행을 더한 사본 `na=1`. 문장 삭제 대조: 5 개(절 제목 줄 포함) 모두 출력이 바뀐다)
- [ ] ER-04: notes 가 넘기는 것과 처리 배정표 키를 적는다 — `$END` 판 `.harness/.meta/kaizen-0924/phase6-notes.md` 에 스물한 문자열(`skill-design-guide.md` · `visual-evidence-protocol.md` · `render-evidence-protocol.md` · `UNVERIFIED_ENV` · `design:P2 방향` · `F20` · `design-mockup Step 0` · ``버전: `0.1.0` `` · `docs/design/research-log.md` · `Material 3` · `임계값 다시 정의` · `§3.7 네 칸` · `F01` · `F04` · `design:P1` ~ `design:P7`)이 각각 1 줄 이상 있다 [exact, enumerated]
      (Given: BUILD 가 notes 를 커밋하고 그 sha 로 `end_sha:` 를 덧붙인 뒤 · 측정: `ER04` 한 줄이 `ER-04 111111111111111111111`.
       봉인 전 실측: `회귀 게이트` 절 예행 — 모의 notes 를 커밋한 예행 저장소에서 요구값, notes 가 없는 상한(`end_sha` = 구현 커밋)에서 `ER-04 000000000000000000000`)

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 공유 파일을 건드리지 않고, 이 계약이 봉인돼 있고, 측정 도우미가 이 계약에 적힌 그대로다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p06-design-kit` · 측정: `AR01` 두 줄 —
       ① `AR-01 unsigned=0 outside=0 mine=13 added_files=0 shared=0 broken=0 own=SEAL_OK` — `unsigned` 는 구간 안에서 `design-kit/` 을 건드렸는데 서명이 없는 커밋 수(이 구간에 design-kit 을 고칠 Phase 는 6 하나다), `outside` · `mine` 은 서명 커밋이 건드린 파일 중 `.harness/` 와 열세 파일 밖의 수 · 열세 파일 수, `added_files` 는 구간에 새로 생긴 `design-kit/` 파일 수, `shared` 는 공유 파일(`.claude-plugin/marketplace.json` · `design-kit/.claude-plugin/plugin.json` · `README.md` · `CLAUDE.md` · `.claude/kaizen-input/insights-report.md` · `.harness/.meta/orchestrator-audit-log.md` · `.harness/.meta/kaizen-failure-count.yaml` · `docs/design`)을 건드린 구간 커밋 수를 `git log … | wc -l` 로 직접 센 값, `broken` 은 이 Phase 몫 계약 가운데 `SEAL_BROKEN` 수(`harness/references/contract-schema.md` §`.harness/` 범위 조건 권장 형태), `own` 은 이 계약의 `verify_seal` 결과(`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL). `shared` 가 0 이 아니면 그 커밋의 서명 줄부터 본다 — 다른 Phase 서명이면 이 Phase 몫이 아니다(근거에 적고 PASS)
       ② `AR-01 helpers common.sh:64f32d049a33c4a8 conds.sh:5fe82e178530b978 dtcg.py:ab7473168fd8f9c7 fence.py:dae506ed24cc7822 new-warnings.sh:e485430011be3e1a ` — `회귀 게이트` 절 명령으로 떼어 낸 도우미 다섯의 sha256 앞 16 자리. 도우미를 봉인 뒤에 고치면 여기서 드러난다.
       봉인 전 실측: `회귀 게이트` 절 예행 — ① 요구값. 음성 대조: 예행 사본에 서명 없이 `design-kit/README.md` 를 고친 커밋을 얹고 `end_sha` 를 옮기면 `unsigned=1` · `outside=0`(서명 줄 목록에는 안 보인다), 서명을 달고 `README.md`(루트)를 고친 커밋을 얹으면 `outside=1` · `shared=1`, 봉인 뒤 조건 줄 한 글자를 고치면 `broken=1` · `own=SEAL_BROKEN`. 봉인 전인 지금 작업 폴더의 이 계약은 `SEAL_ABSENT` — 봉인을 빠뜨리면 `own` 이 떨어진다)
- [ ] AR-02: 스킬 · 문서 구조를 유지하고 더한 참조 경로가 실제 파일을 가리킨다 (카이젠 스킬 Gotcha 3 — 섹션 구조를 바꾸지 말고 내용만) — (a) 바꾼 SKILL.md 일곱의 `# ` 제목과 Step 제목, design-reviewer · mockup-guidelines · token-principles 의 모든 제목이 시작 커밋 판과 같고, audit-criteria 는 제목 한 줄(`:41` WCAG 절)만 바뀌며, 규약은 제목이 하나도 빠지지 않고 셋(`## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표` · `### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한` · `### 캡처 점검 목록`)만 는다 (b) 마크다운 열두 파일의 더한 줄에서 백틱으로 감싼 `../` 로 시작하는 `.md` 경로가 1 개 이상이고, 그 파일 자리에서 풀었을 때 없는 경로가 0 이다 [exact, enumerated]
      (측정: (a) `AR02` 한 줄이 `AR-02 same=0 ac=[< ## WCAG 2.2 신규 성공 기준 (2023-10 권고안, 2026 AA 컴플라이언스 타겟)|> ## WCAG 2.2 신규 성공 기준 (W3C 권고안 — 현재 게시본 2024-12-12)|] p_added=[## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표|### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한|### 캡처 점검 목록|] p_removed=0`
       (b) `AR03` 한 줄에서 `checked` 가 1 이상 · `unresolved=0`.
       봉인 전 실측: 모의본 (a) 요구값 (b) `checked=9 unresolved=0`. 양성 대조: design-guide 에 `## Step 9: 새 단계` 를 더한 사본 `same=1`, audit-criteria 의 `../../../references/visual-change-protocol.md` 를 `../../references/…` 로 바꾼 사본 `unresolved=1`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 더한 줄의 버전꼴 문자열(`x.y.z`)은 근거 파일에 있는 바깥 도구 판 · WCAG 성공 기준 번호뿐이고, 킷 자신의 버전 `0.4.0` 은 0 이다 [exact]
      (측정: `ER01` 의 `vmiss=0` · `AP01` 의 `own=0`. 봉인 전 실측: 모의본 버전꼴 `1.4.10 1.4.4 2.5.5 2.5.8 3.2.4 4.3.3 5.0.0 5.5.5` 모두 근거 파일에 있다 · `own=0`. 양성 대조: `버전 0.4.0 기준` 한 줄을 더한 사본 `own=1`, `v9.9.9` 를 더한 사본 `vmiss=1`)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 마크다운 열두 파일을 같은 판정에 펜스 길이를 더한 검출기로도 잰다 [exact]
      (측정: `AP03` 한 줄이 `AP-03 bare_open_total=0 unclosed_total=0`. V6 쪽은 DG-05. 봉인 전 실측: 모의본 요구값. 양성 대조: 규약 끝에 언어 힌트 없는 펜스를 더한 사본 `bare_open_total=1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 일곱과 design-reviewer 의 첫 frontmatter 블록에 `name: <이름>` 줄이 1 개씩 그대로다 [exact]
      (측정: `AP04` 한 줄이 `AP-04 [1 1 1 1 1 1 1 ] agent=1`. V1 쪽은 DG-05. 봉인 전 실측: 편집 전 · 모의본 요구값. 양성 대조: design-guide 의 `name:` 줄을 지운 사본 `[1 1 0 1 1 1 1 ]`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 새 절차 셋(관례 표 · 반영 확인 · 캡처 점검 목록)의 정의는 공유 규약 한 곳에만 있고 스킬 · 에이전트는 절 번호로 인용한다 — 정의 줄(`3. **관례 표** — ` · `3. **반영 확인** — ` · `4. **디버그 겹침** — `)을 가진 파일이 design-kit 이 스킬로 읽는 자리에서 각각 `design-kit/references/visual-change-protocol.md` 하나뿐이다 [exact, enumerated]
      (측정: `RE01` 한 줄이 `RE-01 [design-kit/references/visual-change-protocol.md, design-kit/references/visual-change-protocol.md, design-kit/references/visual-change-protocol.md, ]`.
       봉인 전 실측: 편집 전 `RE-01 [   ]`. 모의본 요구값. 양성 대조: design-reviewer 에 디버그 겹침 정의 줄을 복사한 사본에서 셋째 칸이 두 파일)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 요소 지목 요청은 기존 Change Manifest 형식을 그대로 쓰고(`## Change Manifest` 블록 수가 시작 커밋 판과 같다) 승인 기록은 기존 `.design/` 하위 폴더만 쓴다(새 `.design/<폴더>/` 이름 0) [exact]
      (측정: `RE02` 한 줄이 `RE-02 manifest=2/2 dirs=0`. 봉인 전 실측: 편집 전 · 모의본 요구값. 양성 대조: design-guide 에 `## Change Manifest` 블록과 `.design/newdir/` 를 더한 사본 `manifest=2/3 dirs=1`)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `DG01` 이 `DG-01 0`. 함수 정의가 없으면 `DEFS_MISSING` · 종료 코드 2. 실제 분석은 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: (a) 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 열두 파일의 **더한 줄**에 걸린 경고가 0 (b) `evals.json` 이 JSON 으로 읽힌다. 편집 전부터 있던 경고는 `범위 경계` 절대로 범위 밖이다 [exact]
      (측정: `DG02` 한 줄이 `DG-02 md=[0 0 0 0 0 0 0 0 0 0 0 0 ] json=0` — 린터가 안 돌면 그 칸이 `LINT_NOT_RUN` 이 된다.
       봉인 전 실측: 모의본 요구값(더한 줄 84 · 16 · 2 · 3 · 5 · 5 · 4 · 5 · 2 · 1 · 4 · 7). 양성 대조: 규약의 `관례 표의 규칙:` 줄 끝에 공백 둘을 붙이고 그 아래 빈 줄을 목록 한 줄로 바꾼 사본에서 첫 칸 `1`)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `DG01` 이 `DG-01 0`. 실제 시험은 SK-10 · DG-05 의 `run-evals.py`)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바꾼 파일은 마크다운 열둘과 JSON 하나다. 측정: `DG04` 가 `DG-04 0` (서명 커밋이 건드린 파일 가운데 `.dart` · `.ts` · `.tsx` · `.js` · `.rs` · `.go` · `.py` · `.sh` 수). 양성 대조: 같은 `grep -cE` 에 `a/b.dart` · `c.sh` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사가 이 Phase 파일을 문제로 가리키지 않는다 — (a) `python3 scripts/validate-plugin.py design-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 하나도 `ERROR` · `FAIL` 이 아니다 (b) 전체 킷 `--check=table-integrity,code-fence` 의 `FAIL` 줄 가운데 이 Phase 파일을 가리키는 줄 0 (c) `sync-docs.py design-kit --check-only` · `run-evals.py design-kit` 가 종료 코드 0 이고 `run-evals.py design-kit` 끝 줄이 `Total: 30 passed, 0 failed`, 저장소 전체를 보는 `sync-evals.py --check-only` · `validate-doc-contracts.py` 는 종료 코드가 0 이거나, 0 이 아니면 출력에서 design-kit 을 가리키는 줄(`[design-kit]` 또는 `design-kit/`)이 0 — 다른 Phase 가 같은 가지에서 동시에 움직이므로 남의 킷 어긋남은 이 조건 몫이 아니다(그 출력을 근거에 붙인다) (d) `check-stale-values.py` 가 0 또는 1 이고 출력에 이 Phase 파일 0 건 [exact]
      (Given: 작업 트리의 열세 파일이 `$END` 와 같다 — 아니면 `DG05` 가 `GIVEN_NOT_MET` · 종료 코드 2 · 측정: `DG05` 한 줄이 `DG-05 v=10 bad=0 kitfail=0 rc=[0 0 0:0 0:0 ] evals=[Total: 30 passed, 0 failed] stale_rc=0 stale_mine=0` — `stale_rc` 는 1 이어도 되고, `rc` 셋째 · 넷째 칸은 `:` 뒤가 0 이면 앞 숫자와 무관하게 통과.
       봉인 전 실측: `회귀 게이트` 절 예행 값. 편집 전 사본은 `evals=[Total: 27 passed, 0 failed]`. 양성 대조: design-kit `evals.json` 한 항목의 `skill` 을 없는 이름으로 바꾼 사본 셋째 칸 `1:1`, design-guide description 을 바꾼 사본 `sync-docs.py design-kit --check-only` 종료 코드 1(첫 칸 `1`). 음성 대조: backend-kit `evals.json` 을 같은 식으로 바꾼 사본 셋째 칸 `1:0`)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 79258900de00e621412e4c436b44028a77d7fb64` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록에 서명 줄 커밋이 없을 때 이 조건은 PASS 다 [exact]
      (측정: `DG06` 한 줄의 두 칸이 `[ PASS` 또는 `[ SKIP` 으로 시작한다. `scope-isolation` 이 `FAIL` 일 때만 — `python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1` 뒤
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | grep -c .` 이 1 이상(위반 목록을 실제로 읽었다) ·
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done | grep -c .` 0.
       봉인 전 실측: `회귀 게이트` 절 예행 값)
