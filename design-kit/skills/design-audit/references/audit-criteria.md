# 디자인 감사 기준

design-reviewer 에이전트가 참조하는 카테고리별 체크리스트.

## Typography

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 스케일 일관성 | 정의된 타이포 스케일 외 임의 크기 미사용 | Material Design 3 Typography |
| 행간 비율 | line-height가 font-size의 1.2~1.6배 | WCAG 1.4.12 |
| 최소 크기 | 본문 텍스트 14px(모바일) / 16px(웹) 이상 | Apple HIG Typography |

## Color

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 대비 비율 | 텍스트/배경 대비 WCAG 2.2 AA (4.5:1 이상) | [WCAG 2.2 SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) |
| 시맨틱 사용 | 하드코딩된 컬러값 대신 시맨틱 토큰 사용 | [Material Design 3 Color](https://m3.material.io/styles/color/roles) |
| 다크 모드 | 다크 모드에서도 대비 비율 유지 | [Apple HIG Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) |
| OKLCH primitive | OKLCH 표기 권장 (Tailwind v4/shadcn v4 기본), P3 wide gamut 사용 시 sRGB fallback 명시 | [Tailwind v4 blog](https://tailwindcss.com/blog/tailwindcss-v4), [MDN oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch) |

## Spacing

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 스케일 일관성 | 정의된 스페이싱 스케일 외 임의 값 미사용 | EightShapes Space in DS |
| 터치 타겟 AA | WCAG 2.2 SC 2.5.8 AA — 최소 24×24 CSS px (예외: sufficient spacing / inline / user-agent / essential) | [WCAG 2.2 SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) |
| 터치 타겟 AAA | WCAG 2.2 SC 2.5.5 AAA — 최소 44×44 CSS px | [WCAG 2.2 SC 2.5.5](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html) |
| 터치 타겟 플랫폼 | Apple HIG 44pt 터치 디바이스 실용 권장치 | [Apple HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) |
| 여백 일관성 | 같은 레벨의 요소는 동일 간격 | Gestalt 근접성 원칙 |

## Accessibility

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 색상 대비 AA | 일반 텍스트 4.5:1, 대형 텍스트 3:1 | [WCAG 2.2 SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) |
| 터치 타겟 AA | WCAG 2.2 SC 2.5.8 — 24×24 CSS px 이상 | [WCAG 2.2 SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) |
| 터치 타겟 AAA | WCAG 2.2 SC 2.5.5 — 44×44 CSS px 이상 | [WCAG 2.2 SC 2.5.5](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html) |
| 포커스 표시 | 인터랙티브 요소에 포커스 인디케이터 존재 | [WCAG 2.2 SC 2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) |

## WCAG 2.2 신규 성공 기준 (2023-10 권고안, 2026 AA 컴플라이언스 타겟)

> WCAG 2.2는 WCAG 2.1의 상위 호환으로 9개 신규 SC를 추가했다. design-audit는 이 중 AA 레벨 기준을 체크리스트에 포함한다.
> 출처: [W3C WCAG 2.2 What's New](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/), [W3C WCAG 2.2 TR](https://www.w3.org/TR/WCAG22/)

| 기준 | 레벨 | PASS 조건 | 출처 |
|------|------|-----------|------|
| SC 2.4.11 Focus Not Obscured (Minimum) | AA | 키보드 포커스를 받은 요소가 author content(예: sticky header, toast)로 **완전히** 가려지지 않는다. 부분 가림은 허용. | [W3C SC 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) |
| SC 2.4.12 Focus Not Obscured (Enhanced) | AAA | 포커스 요소가 전혀 가려지지 않는다. | [W3C SC 2.4.12](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-enhanced.html) |
| SC 2.4.13 Focus Appearance | AAA | 포커스 인디케이터 최소 크기/대비 기준 (경계선 2 CSS px + 대비 3:1 등). | [W3C SC 2.4.13](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) |
| SC 2.5.7 Dragging Movements | AA | 드래그 동작이 필요한 기능은 단일 포인터(탭/클릭) 대체를 제공한다 (예: 순서 변경은 up/down 버튼, 슬라이더는 +/-). | [W3C SC 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) |
| SC 2.5.8 Target Size (Minimum) | AA | 포인터 타겟 최소 24×24 CSS px (예외 4종). | [W3C SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) |
| SC 3.2.6 Consistent Help | A | help 메커니즘이 여러 페이지에 존재할 경우 동일 순서로 표시한다. | [W3C SC 3.2.6](https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html) |
| SC 3.3.7 Redundant Entry | A | 같은 프로세스 내에서 이전에 입력한 정보를 다시 요구하지 않는다 (auto-fill / select from list 허용). | [W3C SC 3.3.7](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html) |
| SC 3.3.8 Accessible Authentication (Minimum) | AA | 인지 기능 테스트(암호 기억, 퍼즐)가 인증의 유일한 수단이면 안 된다. 대체 수단(이메일 매직링크, passkey, OAuth, copy-paste 허용 등) 제공. | [W3C SC 3.3.8](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html) |

## APCA / WCAG 3 보조 체크 (NOTE)

> **현재 상태 (2026-04):** WCAG 3.0은 Working Draft이며 Recommendation은 2028~2030 예상이다. **WCAG 2.2 AA가 2026 법적 컴플라이언스 타겟**이며, APCA는 보조 체크로 권장한다. Contra 자동 판정을 APCA로 대체하지 마라.

APCA(Advanced Perceptual Contrast Algorithm)는 WCAG 3 후보 대비 알고리즘으로, 폰트 크기·굵기·극성을 고려한 지각 대비 Lc 값을 반환한다. 대규모 디자인 시스템 리프레시 / 다크 모드 튜닝 / 얇은 텍스트가 섞인 팔레트에서 WCAG 2.x 수치 대비만으로는 실제 가독성이 떨어지는 경우가 있을 때 사이드 체크로 사용한다.

권장 Lc 임계값: **body text 최소 Lc 60, preferred Lc 75**. dark mode pair는 WCAG 2.2 통과해도 APCA Lc가 낮게 나올 수 있다. 출처: [APCA Easy Intro](https://git.apcacontrast.com/documentation/APCAeasyIntro.html), [web-accessibility-checker WCAG 3.0 2026](https://web-accessibility-checker.com/en/blog/wcag-3-0-guide-2026-changes-prepare), [Eric Eggert — WCAG 3 is not ready yet](https://yatil.net/blog/wcag-3-is-not-ready-yet).

## Interaction

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 피드백 존재 | 사용자 액션에 시각적 피드백 존재 | NNGroup Feedback |
| 로딩 상태 | 비동기 작업에 로딩 인디케이터 존재 | NNGroup Response Times |
| 에러 표시 | 에러 상태가 명확히 표시됨 | NNGroup Error Messages |

## Motion

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 목적성 | 장식용 애니메이션이 아닌 기능적 목적 존재 | Material Design 3 Motion |
| 듀레이션 | 200~500ms 범위 (너무 빠르거나 느리지 않음) | Apple HIG Motion |
| reduced-motion | prefers-reduced-motion 대응 | WCAG 2.3.3 |

## Visual Hierarchy

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 크기 위계 | 제목/본문/캡션 간 크기 차이가 명확함 (최소 1.2배 이상 비율) | Material Design 3 Typography |
| 대비 강조 | 핵심 콘텐츠가 주변보다 높은 대비를 가짐 | NNGroup Visual Hierarchy |
| 여백 분리 | 그룹 간 여백이 그룹 내 여백보다 넓음 (Gestalt 근접성) | Gestalt 근접성 원칙 |

## Layout & Grid

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 그리드 일관성 | 정의된 그리드 시스템 내에서 요소가 정렬됨 | Material Design 3 Layout |
| 거터 규칙성 | 열 간격(gutter)이 일관된 값을 사용함 | EightShapes Grid |
| 반응형 전략 | 주요 breakpoint에서 레이아웃이 적절히 변환됨 | Apple HIG Layout |
| Container Queries | 컴포넌트 수준 반응형은 `container-type: inline-size` + `@container` 사용. 글로벌 레이아웃/OS 선호(reduced-motion, color-scheme)는 media query 유지. `block-size`/`size` 쿼리 금지(layout loop). 2026 Baseline: Chrome 105+/Firefox 110+/Safari 16+ | [MDN CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries), [web.dev container queries](https://web.dev/blog/how-to-use-container-queries-now), [LogRocket container queries 2026](https://blog.logrocket.com/container-queries-2026/) |

## Ethical Design

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 다크 패턴 부재 | Confirmshaming, Roach Motel, Trick Questions 등 12가지 다크 패턴 미사용 | darkpatterns.org 분류 |
| 동의 명시성 | 체크박스 기본 해제, 이중 부정 문구 미사용 | GDPR, 한국 전자상거래법 |
| 탈퇴 대칭성 | 가입/구독 경로와 해지/탈퇴 경로의 단계 수가 동등함 | EU DSA |

## Authenticity

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 레이아웃 변주 | 연속 섹션이 동일 구조(예: 3열 카드)로 3회 이상 반복하지 않음 | NNGroup State of UX 2026 |
| 컬러 맥락 | 컬러 팔레트가 브랜드/프로젝트에서 도출됨 (제네릭 보라-파랑 기본값 아님) | 925 Studios AI Slop Guide |
| 장식 목적성 | blur, gradient, shadow 등 장식 효과에 기능적 목적 존재 | BSWEN AI UI Anti-Patterns |
| 카피 구체성 | 헤드라인/CTA가 이 제품에만 해당하는 구체적 내용 (범용 문구 아님) | Crea8ive Solution Anti-AI Trends 2026 |
| 이미지 고유성 | 이미지/일러스트가 프로젝트 고유 스타일임 (제네릭 스톡 느낌 아님) | authentic-design.md |
