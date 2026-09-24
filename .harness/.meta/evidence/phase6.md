---
phase: 6
title: "Phase 6 design-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 6 행 · phase-research-templates.md Phase 6 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용으로 조사했으며 워크트리 변경은 없습니다.

## 1. 출처 목록

실제로 `curl` 또는 `gh`로 가져온 출처만 적었습니다.

1. [Tailwind CSS v4.0 발표 — 2025-01-22](https://tailwindcss.com/blog/tailwindcss-v4)
2. [Tailwind CSS 최신 릴리스 v4.3.3 — 2026-07-16](https://github.com/tailwindlabs/tailwindcss/releases/tag/v4.3.3)
3. [W3C DTCG Design Tokens Format Module 2025.10 Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/)
4. [W3C WCAG 2.2 — Recommendation 2024-12-12](https://www.w3.org/TR/WCAG22/)
5. [MDN CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries)
6. [MDN Browser Compat Data — `@container`](https://github.com/mdn/browser-compat-data/blob/main/css/at-rules/container.json)
7. [MDN Browser Compat Data — `container-type`](https://github.com/mdn/browser-compat-data/blob/main/css/properties/container-type.json)
8. [Style Dictionary 최신 릴리스 v5.5.5 — 2026-09-20](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.5.5)
9. [Style Dictionary v5.0.0 릴리스와 breaking changes](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.0.0)
10. [Style Dictionary v5 Migration Guidelines](https://styledictionary.com/versions/v5/migration/)
11. [Bootstrap 최신 릴리스 v5.3.8](https://github.com/twbs/bootstrap/releases/tag/v5.3.8)
12. [Playwright 최신 릴리스 v1.63.0](https://github.com/microsoft/playwright/releases/tag/v1.63.0)
13. [shadcn CLI 최신 릴리스 4.21.0](https://github.com/shadcn-ui/ui/releases/tag/shadcn%404.21.0)

필수 소스 중 Tailwind, DTCG, WCAG, MDN 네 건을 실제 조회했습니다.

## 2. 항목별 관찰 사실

### design:P1 — 재사용 부품·구조 관례 선탐색

- WCAG 2.2 SC 3.2.4는 여러 페이지에서 같은 기능을 하는 컴포넌트가 일관되게 식별되어야 한다고 요구합니다. 아이콘이 뜻하는 동작이나 동일 기능의 이름을 기존 화면과 맞추는 근거가 됩니다. SC 3.2.3도 반복되는 내비게이션의 상대적 순서를 일관되게 유지하되 사용자가 변화를 시작한 경우를 예외로 둡니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- DTCG는 디자인 토큰의 목적을 조직 전반의 공통 어휘와 의미 관계·일관성 확립으로 설명합니다. 기존 토큰·의미 이름을 먼저 조사하고 재사용한다는 방향은 이 목적과 맞습니다. [DTCG Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/)
- 반대/제한 근거: WCAG는 “같은 기능의 일관된 식별”을 요구하지 모든 화면의 시각 구조를 같게 만들라고 요구하지는 않습니다. 따라서 줄/카드 관례는 같은 의미·역할에 한해 적용해야 합니다. 레포의 Authenticity 규칙은 연속 동일 구조 3회 이상 반복을 문제로 삼고 있어, 무차별 복제와 충돌합니다: [audit-criteria.md:110](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/references/audit-criteria.md:110).
- 기존 화면을 정확히 2개 또는 3개 읽어야 한다는 외부 표준은 찾지 못했습니다.
- 추론: 계약값은 **서로 다른 기존 화면 최소 2개**가 적합합니다. 반복 관례인지 판단할 최소 대조군이고, 이미 Flutter 규약과 P7이 2개를 사용합니다. 세 번째 화면이 있으면 추가 근거로 읽되 필수값으로 만들 필요는 없습니다.
- 현재 삽입 지점은 요청과 일치합니다.
  - design-mockup: [SKILL.md:46](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-mockup/SKILL.md:46) 뒤
  - design-component: [SKILL.md:32](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-component/SKILL.md:32)
  - design-guide: Gotcha 13은 탐색을 요구하지만 Step 1 본문에는 토큰·컴포넌트 탐색이 없습니다: [SKILL.md:27](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-guide/SKILL.md:27), [SKILL.md:34](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-guide/SKILL.md:34)
  - 우선순위 표 순위 3: [visual-change-protocol.md:23](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/references/visual-change-protocol.md:23)
  - Variant constants 예시: [visual-change-protocol.md:195](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/references/visual-change-protocol.md:195)

### design:P2 — 시안 개수 계약

- 외부 표준은 기본 시안 수나 상한을 정하지 않습니다.
- 현행 design-kit은 이미 핵심 위치에서 `미지정 3 · 사용자 지정 N · 승인 시 최대 5`로 맞아 있습니다: [design-mockup/SKILL.md:4](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-mockup/SKILL.md:4), [SKILL.md:68](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-mockup/SKILL.md:68), [visual-change-protocol.md:171](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/references/visual-change-protocol.md:171), [README.md:16](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/README.md:16).
- 추론: 현행 값을 유지하되 숫자의 SSOT는 harness §5.6으로 두고 design-kit에는 참조만 남기는 편이 드리프트를 줄입니다.

### design:P3 / F01 — 대상 화면·되말하기

- WCAG의 “사용자가 시작한 변경” 예외는 사용자의 실제 의도를 먼저 확정하는 방향과 양립하지만, 작업 전 되말하기 형식이나 파일 경로 표기를 요구하는 표준은 아닙니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 현재 Step 1은 페이지 종류·기능·사용자만 묻고 대상 화면 파일/라우트나 한 문장 되말하기가 없습니다: [design-mockup/SKILL.md:37](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-mockup/SKILL.md:37).
- 추론: `대상 화면 파일·라우트`와 `요청을 배치까지 포함해 한 문장으로 되말하기`를 Step 1의 필수 출력으로 두는 것이 F01에 직접 대응합니다.
- 부분 변경 규약은 현재 “보더만·색만·간격만” 같은 속성 단위입니다: [visual-change-protocol.md:43](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/references/visual-change-protocol.md:43). 요소 하나를 지목한 요청도 같은 Change Manifest를 적용하도록 범위를 넓힐 근거가 있습니다.

### design:P4 / F04 — 캡처 점검 목록과 큰 글자

- WCAG 2.2 SC 1.4.4는 텍스트를 200%까지 키워도 콘텐츠나 기능 손실이 없어야 한다고 요구합니다. “가장 큰 글자 크기”보다 **200% 텍스트 확대**가 웹 계약으로 더 정확합니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- SC 1.4.10은 320 CSS px 상당 폭에서 콘텐츠·기능 손실과 양방향 스크롤이 없어야 한다고 규정합니다. 넘침 점검의 직접 근거입니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 반대/제한 근거: WCAG는 스크린샷 횟수나 네 줄 체크리스트를 정하지 않습니다. 캡처는 준수 결과를 확인하는 레포 자체 절차입니다.
- 현재 protocol은 빈 캡처 유효성만 확인하고 글자 넘침·깨진 글리프·관례·디버그 겹침의 네 항목은 없습니다: [visual-change-protocol.md:97](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/references/visual-change-protocol.md:97).
- 추론: Flutter의 네 항목을 옮기되 웹 산출물은 기본 캡처와 **텍스트 200% 캡처**를 요구해야 합니다. 실제 앱 글꼴을 쓰지 않은 artifact snapshot으로 글리프 PASS를 주면 안 됩니다.

### design:P5 — 확정 구성·폐기 항목 기록

- 현재 승인 기록에는 선택된 안, 확정 시각 값, 미확정/후속은 있지만 “확정 구성”과 “명시적으로 폐기한 항목”은 없습니다: [visual-change-protocol.md:121](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/references/visual-change-protocol.md:121), [design-mockup/SKILL.md:140](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-mockup/SKILL.md:140).
- 가져온 외부 출처에서는 승인 기록의 필드나 폐기 결정 저장 위치에 관한 직접 근거를 찾지 못했습니다.
- 추론: design-kit 승인 파일에는 디자인 범위의 `확정 구성`과 `폐기한 대안·이유`만 기록하고, 제품 요구 수준의 폐기 결정은 공용 결정 기록을 참조해야 중복 정본을 피할 수 있습니다.

### design:P6 — 비교 반복·반영 확인

- 외부 표준은 자기 수정 반복을 3회 또는 5회로 정하지 않습니다.
- 현재 design-kit EVIDENCE는 before/after/proof만 요구하고, 새 결과가 실제로 다시 그려졌는지를 가시적 표식으로 확인하는 단계가 없습니다: [visual-change-protocol.md:72](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/references/visual-change-protocol.md:72).
- 추론: Flutter 규약과 맞춰 **자기 수정 최대 3회 후 사용자 에스컬레이션**을 계약값으로 삼는 것이 적합합니다. 5회를 지지하는 외부 근거는 없고, 3회는 이미 운영 중인 sibling 계약과 일치합니다.
- 순서는 `기준 캡처 → 한 의도 변경 → 달라져야 할 표식 확인 → 재캡처 → 보존 영역 대조 → 실패 시 self-reject`로 고정하는 것이 좋습니다.

### design:P7 — 기존 화면 관례 감사

- WCAG 2.2 SC 3.2.4는 같은 기능의 일관된 식별을 요구하므로 아이콘 의미·같은 기능의 컴포넌트 표현을 대조하는 근거가 됩니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 반대/제한 근거: 동일 기능이 아닌 화면까지 같은 줄/카드 구조로 강제하면 현행 Authenticity의 레이아웃 변주 규칙과 충돌합니다: [audit-criteria.md:114](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/references/audit-criteria.md:114).
- 추론: 행 이름은 `같은 역할의 기존 화면 관례 일치`로 좁혀야 합니다. P1 목록이 있으면 그 목록에 기록된 **동일한 기존 화면 최소 2개**를 사용하고, 목록 부재나 비교 가능한 화면 부족은 `[미검증]`으로 둡니다.
- 세 동기화 위치:
  - [audit-criteria.md:110](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/references/audit-criteria.md:110)
  - [design-reviewer.md:109](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/agents/design-reviewer.md:109)
  - [design-audit/SKILL.md:80](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/SKILL.md:80)

## 3. 현행화 — 낡거나 잘못된 곳

| 파일:줄 | 현재 값 | 최신 값·판정 |
|---|---|---|
| [design-system/SKILL.md:23](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-system/SKILL.md:23) | `.`은 금지 문자라고 한 뒤 경로 구분에 `.` 사용 가능이라고 함 | DTCG 2025.10은 토큰·그룹 이름에 `{`, `}`, `.`을 어디에도 쓸 수 없고 `$`로 시작할 수 없다고 명시합니다. 점은 참조 경로 문법이지 이름 문자가 아닙니다. [DTCG Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) |
| [design-system/SKILL.md:27](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-system/SKILL.md:27) | `Tailwind CSS v4(2026 Production Ready)`, `HSL→OKLCH` | v4 발표일은 2025-01-22이고, 공식 표현은 기본 팔레트를 `rgb`에서 `oklch`로 바꿨다는 것입니다. 최신 안정판은 v4.3.3(2026-07-16)입니다. [v4 발표](https://tailwindcss.com/blog/tailwindcss-v4), [v4.3.3](https://github.com/tailwindlabs/tailwindcss/releases/tag/v4.3.3) |
| [design-system/SKILL.md:141](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-system/SKILL.md:141) | Style Dictionary v4 파이프라인 | 최신 안정판은 v5.5.5(2026-09-20)입니다. v5는 Node.js 22 이상, 비토큰 leaf 참조 제거, `.value` suffix 참조 제거, 참조 구문 사용자 변경 제거라는 breaking change가 있습니다. v5.5.5는 `convertTokenData` object 출력의 prototype-pollution 취약점을 고쳤습니다. [v5.0.0](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.0.0), [v5.5.5](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.5.5) |
| [token-principles.md:76](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-system/references/token-principles.md:76) | DTCG 예시에 `$schema` 사용 | 조회한 2025.10 Final Report의 그룹 속성 목록에는 `$schema`가 없습니다. DTCG 필수/선택 속성으로 단정할 근거를 못 찾았습니다. 별도 도구 확장이라면 DTCG 규격과 구분해야 합니다. [DTCG Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) |
| [token-principles.md:81](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-system/references/token-principles.md:81) | color `$value`가 `oklch(...)` 문자열 | DTCG 2025.10 color 값은 `colorSpace`, `components`, 선택적 `alpha`·`hex`를 가진 객체 형식입니다. 이 예시는 같은 킷의 [design-system/SKILL.md:42](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-system/SKILL.md:42)와도 충돌합니다. [DTCG Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) |
| [token-principles.md:94](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-system/references/token-principles.md:94) | dimension `$value`가 `"16px"` 문자열 | DTCG dimension 값은 `{ "value": 16, "unit": "px" }` 객체여야 하며 단위는 `px` 또는 `rem`입니다. [DTCG Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) |
| [audit-criteria.md:41](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/references/audit-criteria.md:41), [audit-criteria.md:59](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/references/audit-criteria.md:59) | `2023-10 권고안`, `2026 법적 컴플라이언스 타겟` | 현재 게시본은 W3C Recommendation 2024-12-12입니다. 조회한 W3C 문서에서는 세계 공통 “2026 법적 타겟” 근거를 찾지 못했습니다. 관할 법령 출처가 없으면 법적 표현을 제거해야 합니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| [audit-criteria.md:96](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/references/audit-criteria.md:96) | `block-size`/`size` 쿼리 전면 금지, `2026 Baseline` | MDN은 `container-type`의 유효값으로 `size`, `inline-size`, `normal`을 설명합니다. 기본 size container queries는 Chrome 105, Firefox 110, Safari 16부터 지원되고 deprecated가 아닙니다. 전면 금지는 공식 자료가 지지하지 않습니다. [MDN 가이드](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries), [호환 데이터](https://github.com/mdn/browser-compat-data/blob/main/css/properties/container-type.json) |
| [audit-criteria.md:97](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-audit/references/audit-criteria.md:97) | 375px에서 `scrollWidth-clientWidth <= 2`를 WCAG Reflow 근거로 사용 | WCAG 2.2 SC 1.4.10의 규범값은 320 CSS px 상당 폭에서 콘텐츠·기능 손실 및 양방향 스크롤이 없는 것입니다. 375px와 2px 허용치는 레포 로컬 오라클로는 쓸 수 있지만 WCAG 수치로 표기하면 안 됩니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| [mockup-guidelines.md:67](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/design-kit/skills/design-mockup/references/mockup-guidelines.md:67) | 모든 터치 타겟 `44×44pt 이상` | WCAG 2.2 AA SC 2.5.8은 24×24 CSS px 또는 간격 등 예외 조건입니다. 44×44는 AAA SC 2.5.5/플랫폼 권장과 구분해야 합니다. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |

추가 현행화 결과:

- Tailwind는 최신도 v4 계열이므로 `v4`라는 major 표기 자체는 낡지 않았습니다. [v4.3.3](https://github.com/tailwindlabs/tailwindcss/releases/tag/v4.3.3)
- Bootstrap 5 표기도 최신 major와 맞습니다. 최신 안정판은 v5.3.8입니다. [Bootstrap v5.3.8](https://github.com/twbs/bootstrap/releases/tag/v5.3.8)
- Container size queries는 폐기되지 않았습니다. 다만 최신 MDN은 size query 외에 style·scroll-state·anchored query도 구분하므로 “모든 container query가 모든 주요 브라우저 지원”이라고 일반화하면 안 됩니다. [MDN 가이드](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries)

## 4. 권장안

추론: Phase 6 계약 조건은 다음으로 고정하는 것이 근거와 내부 정합성이 가장 좋습니다.

1. 기존 화면 대조 수는 **최소 2개**로 통일합니다. 동일 역할의 서로 다른 화면이어야 하며, 두 화면이 없으면 존재하는 화면을 모두 기록하고 `[미검증]`으로 둡니다.
2. P1 목록은 앱 코드가 있는 경우에만 필수로 합니다.
   - `재사용 부품: 실제 심볼명 · 파일:줄 · 한 줄 용도`
   - `구조 관례: 역할 · 관례 · 기존 화면 최소 2개의 파일:줄`
   - 실제 코드 검색에서 발견되지 않은 부품 이름은 사용 금지
   - 관례는 Variant Matrix `constants`에 기록
   - 관례 이탈안은 사용자 요청/승인 때만 생성
3. P2는 현행 `미지정 3 · 사용자 지정 N · 4개 이상 사전 승인 · 승인 상한 5`를 유지합니다.
4. P3는 파일 생성 전 `대상 화면 파일·라우트`와 `배치까지 포함한 한 문장 되말하기`를 남깁니다. 요소 하나를 지목한 요청도 Change Manifest 대상입니다.
5. P4는 각 기준/재캡처에 `넘침 · 깨진 글리프 · 칩/뱃지/줄 관례 · 디버그 겹침` 네 항목을 적용합니다. 웹은 텍스트 200% 상태를 한 번 더 캡처하고 320 CSS px reflow도 별도 판정합니다.
6. P5 승인 기록에 `확정 구성`과 `폐기한 대안·이유`를 추가합니다. 제품 요구 결정은 중복 저장하지 말고 공용 결정 기록을 참조합니다.
7. P6 자기 수정 상한은 **3회**로 통일합니다. 반영 표식이 바뀌지 않으면 재캡처 비교로 진행하지 않고 다시 렌더/재실행합니다. 3회 실패 뒤에는 증거와 함께 사용자에게 에스컬레이션합니다.
8. P7은 `같은 역할의 기존 화면 관례 일치`로 좁힙니다. 무관한 화면까지 동일 레이아웃으로 강제하지 않습니다. P1 목록 부재는 FAIL이 아니라 `[미검증]`입니다.
9. DTCG 예시는 Phase 6에서 함께 고쳐야 합니다. 현재 토큰 원칙 예시는 Final Report와 직접 충돌하므로 새 UI 계약보다 우선순위가 높은 명세 오류입니다.
10. Style Dictionary 파이프라인 표기는 v5로 갱신하고 Node.js 22 및 참조 구문 breaking change를 명시해야 합니다.

## 5. 못 가져온 것 / 열린 질문

- Material 3 Expressive와 Apple HIG 2026 자료는 조회하지 않았습니다. 필수 3건 이상의 근거가 모이면 멈추라는 규칙에 따라 추가 조회를 중단했습니다.
- “기존 화면 정확히 2개/3개”, “자기 수정 정확히 3회/5회”를 규정하는 외부 표준은 찾지 못했습니다. 위 숫자 선택은 **추론: sibling 규약 정합성과 운영 비용을 기준으로 한 레포 계약 결정**입니다.
- P5의 폐기 결정이 design approval, 제품 결정 기록, 핸드오프 중 어디에 하나의 정본으로 남아야 하는지에 대한 외부 근거는 가져오지 못했습니다.
- DTCG `$schema` URL과 Figma Variables의 현재 OKLCH 지원 여부는 별도로 검증하지 않았습니다. 따라서 이번 Phase에서는 `$schema`를 DTCG 표준 필드로 단정하지 말고, Figma 관련 문구도 확인 전에는 현행 사실로 강화하지 않는 것이 안전합니다.
