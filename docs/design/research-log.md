---
version: 1.2.0
last_updated: 2026-07-27
---

# Design Kit Research Log

> design-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.
> 다음 사이클에서 중복 리서치를 방지하고, 개선 결정의 근거 출처를 추적한다.

---

## 2026-04-12

**트리거:** design-research 스킬 실행 (10개 카테고리 리서치 — 디자인 토큰, 아키텍처, 접근성, 색상 과학, 타이포, 스페이싱, 컴포넌트 API, 다크모드, 디자인-코드 워크플로우, 반응형 토큰)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
| - | ---- | --- | ---- | ---- | ---- |
| 1 | Design Tokens Format Module 2025.10 | <https://www.designtokens.org/tr/2025.10/format/> | spec | [spec] [dated: 2025-10] | 채택 |
| 2 | DTCG Announcement — First Stable Version | <https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/> | official | [official] [dated: 2025-10] | 채택 |
| 3 | Style Dictionary Docs | <https://styledictionary.com/> | official | [official] [dated: 2024-Q2] | 채택 |
| 4 | Style Dictionary — DTCG Integration | <https://styledictionary.com/info/dtcg/> | official | [official] | 채택 |
| 5 | Spectrum Design Tokens | <https://spectrum.adobe.com/page/design-tokens/> | official | [official] [dated: 2025] | 채택 |
| 6 | Spectrum CSS Architecture | <https://deepwiki.com/adobe/spectrum-css/2-architecture> | blog | [blog] | 참조 |
| 7 | Polaris Goes Stable | <https://www.shopify.com/partners/blog/polaris-goes-stable-the-future-of-shopify-app-development-is-here> | official | [official] [dated: 2025-10] | 채택 |
| 8 | Polaris Tokens GitHub | <https://github.com/Shopify/polaris-tokens> | official | [official] | 참조 |
| 9 | Carbon Color Tokens | <https://carbondesignsystem.com/elements/color/tokens/> | official | [official] [dated: 2025] | 채택 |
| 10 | Carbon Color Overview | <https://carbondesignsystem.com/elements/color/overview/> | official | [official] | 참조 |
| 11 | M3 Design Tokens | <https://m3.material.io/foundations/design-tokens> | official | [official] [dated: 2025] | 채택 |
| 12 | M3 Color Roles | <https://m3.material.io/styles/color/roles> | official | [official] | 채택 |
| 13 | M3 Expressive | <https://supercharge.design/blog/material-3-expressive> | blog | [blog] | 참조 |
| 14 | WCAG 2.2 What's New | <https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/> | official | [official] [dated: 2023-10] | 채택 |
| 15 | WCAG 2.2 Specification | <https://www.w3.org/TR/WCAG22/> | spec | [spec] [dated: 2023-10] | 채택 |
| 16 | APCA in a Nutshell | <https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html> | official | [official] [dated: 2025] | 채택 |
| 17 | APCA Contrast Calculator | <https://apcacontrast.com/> | official | [official] | 참조 |
| 18 | WCAG 3.0 Status 2026 | <https://web-accessibility-checker.com/en/blog/wcag-3-0-guide-2026-changes-prepare> | blog | [blog] | 참조 |
| 19 | OKLCH in CSS — Evil Martians | <https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl> | blog | [blog] | 채택 |
| 20 | CSS Color Module Level 5 — W3C | <https://www.w3.org/TR/css-color-5/> | spec | [spec] [dated: 2025] | 채택 |
| 21 | OKLCH Color Picker | <https://oklch.org/> | official | [official] | 참조 |
| 22 | CSS-Only Fluid Modular Scales — Utopia.fyi | <https://utopia.fyi/blog/css-modular-scales/> | blog | [blog] [dated: 2025] | 채택 |
| 23 | Fluid Type Scale Calculator | <https://www.fluid-type-scale.com/> | official | [official] | 참조 |
| 24 | Modern CSS — Generating font-size Rules | <https://moderncss.dev/generating-font-size-css-rules-and-creating-a-fluid-type-scale/> | blog | [blog] | 채택 |
| 25 | Spacing Best Practices — Cieden | <https://cieden.com/book/sub-atomic/spacing/spacing-best-practices> | blog | [blog] [dated: 2025] | 채택 |
| 26 | Space, Grids, and Layouts — designsystems.com | <https://www.designsystems.com/space-grids-and-layouts/> | blog | [blog] | 채택 |
| 27 | 8-pt Grid — Spec.fm | <https://spec.fm/specifics/8-pt-grid> | blog | [blog] | 채택 |
| 28 | Compound Pattern — patterns.dev | <https://www.patterns.dev/react/compound-pattern/> | blog | [blog] [dated: 2025] | 채택 |
| 29 | Building Component Slots in React | <https://sandroroth.com/blog/react-slots/> | blog | [blog] | 채택 |
| 30 | Compound Components Pattern (Svelte/React) | <https://manuelsanchezdev.com/blog/compound-components-pattern-svelte-react-api/> | blog | [blog] | 참조 |
| 31 | Color Tokens Guide — Light and Dark Modes | <https://medium.com/design-bootcamp/color-tokens-guide-to-light-and-dark-modes-in-design-systems-146ab33023ac> | blog | [blog] [dated: 2025] | 채택 |
| 32 | Complete Dark Mode Design Guide 2025 | <https://ui-deploy.com/blog/complete-dark-mode-design-guide-ui-patterns-and-implementation-best-practices-2025> | blog | [blog] [dated: 2025] | 채택 |
| 33 | Designing Scalable Accessible Dark Theme | <https://www.fourzerothree.in/p/scalable-accessible-dark-mode> | blog | [blog] | 채택 |
| 34 | Figma Variables to Production Code | <https://www.designsystemscollective.com/design-tokens-in-practice-from-figma-variables-to-production-code-fd40aeccd6f5> | blog | [blog] [dated: 2025] | 채택 |
| 35 | 2025/2026 Figma Variables Playbook | <https://www.designsystemscollective.com/design-system-mastery-with-figma-variables-the-2025-2026-best-practice-playbook-da0500ca0e66> | blog | [blog] [dated: 2025] | 채택 |
| 36 | Tokens Studio + Style Dictionary | <https://docs.tokens.studio/transform-tokens/style-dictionary> | official | [official] | 채택 |
| 37 | CSS Container Queries — LearnWebCraft | <https://learnwebcraft.com/learn/css/css-container-queries> | blog | [blog] [dated: 2025] | 채택 |
| 38 | CSS Breakpoints 2025 | <https://viadreams.cc/en/blog/css-media-queries-breakpoints-2025/> | blog | [blog] [dated: 2025] | 채택 |
| 39 | CSS Container Queries — MDN | <https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries> | official | [official] | 채택 |

### 채택한 인사이트

#### A. Design Token Standards (W3C DTCG + Style Dictionary v4)

- W3C DTCG 2025.10이 첫 안정 버전. MIME 타입 `application/design-tokens+json`, 파일 확장자 `.tokens` 또는 `.tokens.json`.
- 지원 타입: color, dimension(px/rem), font-family, font-weight(1-1000), duration(ms/s), cubic-bezier, number. 복합: stroke-style, border, transition, shadow, gradient, typography.
- 2025.10 신규: `$extends` 그룹 상속(deep merge), `$root` 예약명, RFC 6901 JSON Pointer `$ref`, 순환 참조 감지 필수.
- 참여 조직 50+: Adobe, Amazon, Google, Microsoft, Meta, Figma, Shopify, Salesforce, Tokens Studio 등. 레퍼런스 구현체: Style Dictionary, Tokens Studio, Terrazzo.
- Style Dictionary v4: ESM 전환, DTCG 포맷 호환, sd-transforms v1 함께 릴리스. Platform = 빌드 타겟, Transform = 토큰 변환 함수(attribute/name/value 3종). Transform 순서 의존성 주의.

#### B. Modern Design System Architectures (Spectrum, Polaris, Carbon, M3)

- **Adobe Spectrum**: 토큰 3계층 — Global → Alias(시맨틱) → Component-Specific. 네이밍 3파트: Context → Common Unit → Clarification (예: `checkbox-control-size-small`). CSS → React → Web Components → iOS → Android 확장.
- **Shopify Polaris**: Primitive(`space-100`=4px, base 4px) + Semantic(`space-card-padding`). 2025-10 Web Components 기반 전환으로 프레임워크 무관. 60+ 프로덕션 컴포넌트.
- **IBM Carbon**: 4테마(White, Gray 10, Gray 90, Gray 100)에 52개 범용 색상 변수. 레이어 토큰: Light = White↔Gray 10 교대, Dark = Gray 100→80 점진 밝아짐. AI 전용 색상 토큰 세트 추가.
- **Material Design 3**: tokens → themes → components 3계층. 색상 역할 분리("blue" 아닌 "primary"). Dynamic Color: 배경화면에서 접근성 기준 충족하는 light/dark 스킴 자동 생성. 2025 로드맵: shape/motion 토큰 + 크로스 플랫폼 내보내기(Flutter, React, Web).

#### C. Accessibility Standards (WCAG 2.2 + APCA)

WCAG 2.2 주요 신규 기준 (2023-10 발표. ADA/Section 508/EAA 현행 법적 표준):

| 기준 | 레벨 | 핵심 요구사항 |
|------|------|---------------|
| 2.4.11 Focus Not Obscured (Minimum) | AA | 포커스된 컴포넌트가 완전히 가려지면 안 됨 |
| 2.4.13 Focus Appearance | AAA | 포커스 인디케이터 최소 2px 두께, 3:1 대비 |
| 2.5.7 Dragging Movements | AA | 드래그 기능에 단일 포인터 대안 필수 |
| 2.5.8 Target Size (Minimum) | AA | 포인터 타겟 최소 24×24 CSS px |
| 3.2.6 Consistent Help | A | 도움말 메커니즘 동일 상대 위치 유지 |
| 3.3.7 Redundant Entry | A | 이전 입력 정보 자동 채움 또는 선택 가능 |
| 3.3.8 Accessible Authentication | AA | 인지 기능 테스트 없는 인증 대안 필수 |

APCA Lc(Lightness Contrast) 임계값 (WCAG 3.0 Working Draft):

| Lc 값 | 용도 | 최소 폰트 요구 |
|--------|------|-----------------|
| Lc 90 | 본문 텍스트 (권장) | 18px/300w, 14px/400w, 12px/400w(비본문) |
| Lc 75 | 본문 텍스트 (최소) | 24px/300w, 18px/400w, 16px/500w, 14px/700w |
| Lc 60 | 비본문 콘텐츠 텍스트 최소 | — |
| Lc 15 | 다수 사용자에게 비가시 | — |

- WCAG 2.x는 단일 대비율(4.5:1, 3:1). APCA는 폰트 크기+굵기별 차등 Lc — 가는 폰트에 더 높은 대비 요구. 역호환 불가.
- WCAG 3.0 상태: Working Draft, 2026-2027 Candidate Recommendation 예상. 합격/불합격 → Bronze/Silver/Gold 등급제 전환. 법적 채택은 2028-2030 예상. **현재는 WCAG 2.2 AA 준수가 표준.**

#### D. Color Science — OKLCH

- CSS Color Module Level 4/5 포함. 2025년 기준 모든 주요 브라우저 안정 지원. 폴리필 불필요.
- 채널: L(Lightness 0-1), C(Chroma 0~∞, 실용 범위 0.37 미만), H(Hue 0-360°, red≈20°, yellow≈90°, green≈140°, blue≈220°).
- HSL 대비 이점: (1) 지각적 균일성 — 동일 수치 변화 = 동일 시각적 차이. (2) Wide gamut — Display P3/Rec2020, sRGB보다 50% 더 넓은 색역 (Apple 디바이스, OLED). (3) 예측 가능한 팔레트 — CSS relative color syntax와 결합.
- Tailwind CSS 4.0이 OKLCH 채택. 하나의 brand color에서 접근성 기준 충족 전체 팔레트 도출 가능.

#### E. Typography Scale Systems (Modular Scale + Fluid)

주요 스케일 비율:

| 비율 | 이름 | 특성 |
|------|------|------|
| 1.125 | Major Second | 밀도 높은 UI, 조밀한 진행 |
| 1.200 | Minor Third | 미묘하고 작은 진행 |
| 1.250 | Major Third | 일반적인 본문-제목 진행 |
| 1.333 | Perfect Fourth | 중간 진행 |
| 1.500 | Perfect Fifth | 명확한 계층 |
| 1.618 | Golden Ratio | 수학적으로 조화로운 비율 |

- Fluid Typography with `clamp()`: 뷰포트 너비에 따라 최소-최대 선형 보간. 미디어 쿼리 없이 모든 화면 크기 적응.

```css
font-size: clamp(min, preferred, max);
/* 공식: minimum + (maximum - minimum) × viewport-scaling-factor */
```

- Utopia 접근법: 소형/대형 화면용 두 스케일 사이를 보간. CSS 변수 `var(--fluid-2)` 등 연속 적응 사이즈 제공. Jen Simmons "Intrinsic Web Design" 철학 구현.
- Variable Fonts: 하나의 파일로 weight/width/optical-size 축 연속 조절. fluid 사이즈와 결합 시 optical-size도 뷰포트에 따라 최적화 가능.

#### F. Spacing and Layout Systems (8pt Grid + Fluid Spacing)

- **8pt Grid**: 기본 배수 8, 16, 24, 32, 40, 48, 56, 64. iOS 및 여유 있는 웹 레이아웃에 적합.
- **4pt Subgrid**: Material Design 기본 단위. 아이콘/텍스트 미세 조정, 8pt half-step.
- **Internal ≤ External 규칙**: 요소 내부 여백(padding) ≤ 외부 여백(margin). 내부가 크면 요소 경계가 모호해짐.
- **Fluid Spacing**: Fixed(고정), Fluid(유동), Adaptive(적응) 중 선택. Utopia fluid space scale도 `clamp()` 기반 연속 간격 제공.

#### G. Component API Design Patterns (Compound Components + Slots)

- Compound Components: 관련 컴포넌트들이 공유 상태로 함께 동작. "prop soup" 문제 해결.

```text
Parent (상태 관리)
├── Parent.Toggle (컨텍스트로 상태 읽기)
├── Parent.List (상태 기반 조건부 렌더)
└── Parent.Item (목록 자식)
```

- 구현 방식: (1) Context API — Provider로 상태 공유, 중첩 깊이 무관, 권장. (2) React.Children.map — 직계 자식만 가능, 래퍼 div에 취약.
- 사용 시점: Dropdown, Select, Modal 등 여러 파트로 구성된 컴포넌트. 네임스페이스 API (FlyOut.Toggle, FlyOut.List).
- **Slot Pattern**: Card/CardHeader/CardFooter처럼 named slot으로 분리. `createSlots()`로 타입 안전 슬롯 생성. Radix UI, ShadCN의 유연성 비결.

#### H. Dark Mode / Theming Best Practices

- **시맨틱 토큰 필수**: `color/text/primary`, `color/icon/default` 등 역할 기반. 하드코딩 hex 금지.
- **순수 블랙 회피**: `#000000` 대신 짙은 회색(예: `#09111A`) + 브랜드 색상 약간 혼합.
- **채도 낮추기**: Dark 모드에서 desaturated/muted 색상 사용.
- **표면 레이어 시스템**: base → raised → overlay 계층. 밝기 미세 차이로 구분 (테두리 대신).
- **시스템적 접근**: 차트, disabled 버튼, empty states, 모달, 토스트, 서드파티 임베드까지 토큰으로 커버. 개별 화면 수동 디자인 금지.
- 접근성: 모든 모드에서 WCAG 기준 충족. hover/focus 상태 배경 대비 3:1 이상.
- Figma Variables로 Light/Dark 모드 값 정의 → 모드 전환 시 전체 UI 자동 전환.

#### I. Design-to-Code Workflows (Figma Variables → Tokens → Code)

- 표준 파이프라인: Figma Variables (primitive + semantic) → Tokens Studio DTCG JSON 내보내기 → Style Dictionary v4 플랫폼별 변환 → Git 동기화.
- 토큰 레이어: Primitive(`--color-blue-500: #3B82F6`) → Semantic(`color.text.primary`) → Component-specific(`button.primary.background`).
- Figma Variables만으로는 코드 동기화 불가. Tokens Studio: W3C JSON 내보내기 + Git 직접 연동 + downstream 자동화. 대부분의 팀이 Figma Variables + Tokens Studio 병행.
- Best Practices: Code Syntax 활성화(디자인-코드 번역 제거), Description 필드 활용(의도 설명), Scope 제한(관리 가능성 유지).

#### J. Responsive Design Tokens (Container Queries + Fluid Tokens)

- 2025 패러다임: 리지드 브레이크포인트 → 유동적 컴포넌트 인식 반응형. 2026 "Intrinsic Design" — 브레이크포인트 중심 설계의 종말.
- Container Queries: 페이지 레벨 → media queries, 컴포넌트 레벨 → container queries. 유닛: `cqw`, `cqh`, `cqi`, `cqb`.
- 2025 권장 브레이크포인트 (레거시 호환):

| 브레이크포인트 | 용도 |
|---------------|------|
| 480px | 모바일 가로 |
| 768px | 태블릿 |
| 1024px | 랩톱 |
| 1280px | 데스크톱 |
| 1536px | 대형 데스크톱/4K |

- Best Practice: 디바이스 타겟이 아닌 콘텐츠가 깨지는 지점에 브레이크포인트 설정.
- Fluid Typography: `clamp()` = 2025 유동 타이포그래피 골드 스탠다드. 여러 미디어 쿼리 브레이크포인트 제거.

### Backlog

| 제안 항목 | 근거 | 우선순위 |
| --------- | ---- | -------- |
| design-audit에 WCAG 2.2 신규 기준 체크리스트 추가 (Focus Not Obscured, Target Size 24px) | 법적 표준 2023-10 업데이트 | 높음 |
| design-system 스킬에 OKLCH 팔레트 생성 가이드 추가 | Tailwind 4.0 채택, Wide gamut 대응 | 높음 |
| design-guide에 APCA Lc 임계값 표 참조 추가 | WCAG 3.0 준비, 현재는 informational | 중간 |
| design-system에 Figma Variables → Tokens Studio → Style Dictionary v4 파이프라인 가이드 | DTCG 1.0 안정 버전 출시 | 중간 |
| design-audit에 Container Queries 체크 항목 추가 | 2025 반응형 패러다임 전환 | 낮음 |

---

## Changelog

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-04-12 | 초기 작성 — 10개 카테고리 리서치 (DTCG spec, Style Dictionary, Spectrum, Polaris, Carbon, M3, WCAG 2.2, APCA, OKLCH, typography scales, spacing grids, compound components, dark mode, Figma workflows, container queries). 포맷 v1.1.0으로 재구성. |
| 2026-04-12 | 추가 조사 — 11개 확장 토픽 보강 (DTCG post-2025.10 상태 확인, Style Dictionary v4.4.0/migration, Figma auto layout/variables/dev mode 최신 문서, Open Props, Radix Colors/Themes, Panda CSS, Lightning CSS, design system analytics, Figma AI/Galileo→Stitch, axe-core/Pa11y/Lighthouse, OKLCH/Lab/LCH 브라우저 채택 현황). |

### 조사한 소스 (추가 조사 — 기존 표 연속)

| # | 제목 | URL | 유형 | 태그 | 결과 |
| - | ---- | --- | ---- | ---- | ---- |
| 40 | Design Tokens Community Group Reports Index | <https://www.w3.org/community/design-tokens/> | official | [official] [dated: 2025-10] | 채택 |
| 41 | Style Dictionary v4.4.0 Release | <https://github.com/style-dictionary/style-dictionary/releases/tag/v4.4.0> | official | [official] [dated: 2025-04] | 채택 |
| 42 | Style Dictionary v4 Migration Guidelines | <https://styledictionary.com/versions/v4/migration/> | official | [official] | 채택 |
| 43 | Style Dictionary Built-in Transforms | <https://styledictionary.com/reference/hooks/transforms/predefined/> | official | [official] | 채택 |
| 44 | Figma Guide to Auto Layout | <https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout> | official | [official] | 채택 |
| 45 | Figma Suggest Auto Layout | <https://help.figma.com/hc/en-us/articles/5731482952599-Toggle-auto-layout-on-designs> | official | [official] | 채택 |
| 46 | Figma Modes for Variables | <https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables> | official | [official] | 채택 |
| 47 | Variables in Dev Mode | <https://help.figma.com/hc/en-us/articles/27882809912471-Variables-in-Dev-Mode> | official | [official] | 채택 |
| 48 | Figma Dev Mode | <https://www.figma.com/dev-mode/> | official | [official] | 채택 |
| 49 | Open Props | <https://open-props.style/> | official | [official] | 채택 |
| 50 | Radix Themes Color System | <https://www.radix-ui.com/themes/docs/theme/color> | official | [official] | 채택 |
| 51 | Radix Colors Usage Guide | <https://www.radix-ui.com/colors/docs/overview/usage> | official | [official] | 채택 |
| 52 | Panda CSS Tokens | <https://panda-css.com/docs/theming/tokens> | official | [official] | 채택 |
| 53 | Panda CSS Multi-Theme Tokens | <https://panda-css.com/docs/guides/multiple-themes> | official | [official] | 채택 |
| 54 | Lightning CSS | <https://lightningcss.dev/> | official | [official] | 채택 |
| 55 | Lightning CSS Releases | <https://github.com/parcel-bundler/lightningcss/releases> | official | [official] [dated: 2025-09] | 참조 |
| 56 | zeroheight Adoption Measurement | <https://help.zeroheight.com/hc/en-us/articles/35887053202459-Introduction-to-measuring-design-system-adoption-in-zeroheight> | official | [official] [dated: 2025-09] | 채택 |
| 57 | Design Systems Report 2026 | <https://report.zeroheight.com/> | official | [official] [dated: 2026-01] | 채택 |
| 58 | Figma Design Systems Overview | <https://www.figma.com/design-systems/> | official | [official] | 채택 |
| 59 | Figma AI | <https://www.figma.com/ai/> | official | [official] | 채택 |
| 60 | Figma Q4/FY2025 Results (AI Adoption Metrics) | <https://investor.figma.com/news-events/news/news-details/2026/Figma-Announces-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results/default.aspx> | official | [official] [dated: 2026-02] | 채택 |
| 61 | Stitch - Design with AI (redirect from usegalileo.ai) | <https://www.usegalileo.ai/> | official | [official] [dated: 2025-05] | 참조 |
| 62 | axe-core Releases | <https://github.com/dequelabs/axe-core/releases> | official | [official] [dated: 2025-10] | 채택 |
| 63 | Pa11y | <https://pa11y.org/> | official | [official] | 채택 |
| 64 | Lighthouse Accessibility Score | <https://developer.chrome.com/docs/lighthouse/accessibility/scoring> | official | [official] [dated: 2025-10] | 채택 |
| 65 | MDN: oklch() | <https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch> | official | [official] [dated: 2025-12] | 채택 |
| 66 | Can I Use: Relative OKLCH Syntax | <https://caniuse.com/mdn-css_types_color_oklch_relative_syntax> | official | [official] | 채택 |
| 67 | MDN: lab() | <https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/lab> | official | [official] [dated: 2025-12] | 채택 |
| 68 | Can I Use: Relative Lab Syntax | <https://caniuse.com/mdn-css_types_color_lab_relative_syntax> | official | [official] | 채택 |

### 채택한 인사이트 (추가 조사)

#### A. Design Token Standards (W3C DTCG + Style Dictionary v4) — 추가

- 2026-04-12 기준 W3C DTCG 공식 리포트 인덱스에는 여전히 2025-10-28 최종 리포트(Format/Color/Resolver)만 보인다. 즉, **2025.10 이후 새 최종 스펙 발행은 확인되지 않았다.**
- Style Dictionary v4 최신 안정 릴리스는 현재 조사 범위에서 `v4.4.0`(2025-04-24). 릴리스 노트상 `javascript/esm` 포맷에 `flat` 옵션이 추가됐다.
- Style Dictionary v4 migration 문서는 Node.js 18+ 요구, async API 전환, codemod 레시피(`npx codemod styledictionary/4/migration-recipe`) 제공을 명시한다.
- v4의 핵심 전환점은 CTI 중심 매칭에서 `token.type` / DTCG `$type` 중심 매칭으로 이동한 점. 기존 CTI 의존 커스텀 transform/format은 업그레이드 시 검토가 필요하다.

#### D. Color Science — OKLCH / Lab / LCH — 추가

- MDN은 `oklch()`, `oklab()`, `lab()`, `lch()`를 모두 Baseline Widely available로 표시하며, 공통적으로 **2023-05부터 주요 브라우저 전반 사용 가능**으로 정리한다.
- Can I Use 기준 상대 구문(relative syntax)도 이미 실사용 구간에 진입했다. `oklch()` 상대 구문 글로벌 사용량은 약 `89.57%`, `lab()` 상대 구문도 약 `89.57%`.
- 다만 상대 구문은 Safari 16.4~17.x와 Chromium 119~121 구간에서 부분 지원이 존재했다. 구형 Safari/사내 고정 브라우저를 지원해야 하면 fallback 색상 전략은 아직 유효하다.

#### G. Component API Design Patterns / Token Libraries — 추가

- Open Props는 500+ CSS custom properties를 제공하는 범용 토큰 라이브러리이며, CDN/NPM/PostCSS/JS import를 모두 지원한다.
- Open Props는 `open-props.style-dictionary-tokens.json`과 `open-props/resolver` 진입점을 제공해, 단순 CSS 변수 세트가 아니라 **Style Dictionary 및 최신 spec 기반 토큰 소스**로도 활용 가능하다.
- Radix Themes는 12-step color scale + alpha scale + functional token(`--accent-surface`, `--accent-contrast`, `--gray-surface` 등) 조합을 표준 패턴으로 제공한다.
- Radix Themes는 `highContrast` 옵션, `accentColor`/`grayColor` 조합, 색상 CSS 개별 import를 지원해 대형 디자인 시스템에서 번들 크기와 접근성 제어를 동시에 잡기 좋다.
- Radix Colors 문서는 `.light`/`.dark` 및 `.light-theme`/`.dark-theme` 클래스 단위 변수 적용 패턴을 제시한다. 이는 토큰 aliasing이나 app-shell 레벨 theme scope 설계와 잘 맞는다.

#### I. Design-to-Code Workflows (Figma Variables → Tokens → Code) — 추가

- 요청된 "`auto-layout v5`"라는 공식 명칭은 확인되지 않았다. 대신 현행 Figma 문서는 auto layout을 **horizontal / vertical / grid flow**, wrap, nested flow, suggest auto layout 중심으로 설명한다.
- 특히 `Suggest auto layout`은 기존 프레임을 한 번에 auto layout frame들로 재구성하려는 방향이며, 카드/내비/모바일 화면처럼 중간 복잡도 UI에서 유용하다.
- Variables UI는 새 left navigation과 edge-to-edge variables view 방향으로 이동 중이다. 이는 대규모 collection/mode 운영 경험을 개선하려는 신호로 볼 수 있다.
- Dev Mode의 변수 관련 최신 포인트는 variable details, alias chain 추적, suggested variables, read-only collection access다. 즉, 디자이너가 변수 연결을 완벽히 유지하지 않아도 개발자가 대응 가능한 보조 장치가 늘었다.
- Dev Mode 자체도 inspect/code copy를 넘어서 compare changes, Ready for dev, Code Connect, component playground, VS Code extension, MCP context 쪽으로 확장 중이다.

#### J. Responsive Design Tokens / CSS Processing — 추가

- Panda CSS는 토큰 정의를 `{ value, description }` 객체로 강제하고, semantic token이 `{colors.red}` 같은 reference 및 `_dark` 같은 condition을 직접 포함하도록 설계한다.
- Panda의 multi-theme guide는 theme selector와 color mode를 중첩 condition으로 다루며, light/dark를 넘어 brand theme까지 토큰 계층으로 확장하는 패턴을 제시한다.
- Lightning CSS는 토큰 생성기가 아니라 **토큰 산출 CSS를 후처리하는 고성능 transformer/minifier** 역할이 더 적합하다.
- 특히 Lightning CSS는 high-gamut color spaces, custom media, nesting 등을 target browser에 맞춰 변환하므로, OKLCH/relative colors/custom media를 쓰는 토큰 출력물의 배포 단계에 잘 맞는다.

#### K. Design System Analytics and Adoption Metrics — 신규

- zeroheight는 2025-09부터 package version monitoring과 component usage metrics를 제공하며, CLI 기반으로 repo/NPM package를 스캔해 adoption을 측정한다.
- zeroheight 2026 report 응답 분포는 `Fully adopted 7%`, `Widely adopted 31%`, `Moderately adopted 38%`로, 조직 전면 채택은 여전히 드물다.
- 같은 보고서에서 가장 흔한 측정 지표는 adoption(41%), design tool component usage(41%), code component usage(38%), a11y compliance(36%)였다. 즉, **성과(outcome)보다 사용량(coverage) 지표가 아직 우세**하다.
- Figma의 현재 design systems 페이지는 variables REST API와 usage analytics를 함께 전면 배치한다. 디자인 시스템 운영이 "라이브러리 배포"에서 "운영 데이터/자동화"로 이동 중이라는 신호다.

#### L. AI-Assisted Design Tools — 신규

- Figma AI는 이제 단일 생성 기능이 아니라 Figma Make, Code Layers, copy rewrite/translate, FigJam AI를 포함하는 플랫폼 레이어로 정리되고 있다.
- Figma의 2026-02 실적 발표에 따르면 Figma Make 주간 활성 사용자는 전분기 대비 70% 이상 증가했고, $100k+ ARR 고객 절반 이상이 주간 단위로 사용했다. 엔터프라이즈 레벨에서도 AI-assisted workflow가 실사용 단계에 들어갔다는 뜻이다.
- `usegalileo.ai` 공식 도메인은 현재 Google Stitch로 리다이렉트된다. 따라서 Galileo AI는 **독립 제품보다 Stitch로 흡수된 시장 신호**로 보는 편이 정확하다.

#### M. Accessibility Automation — 신규

- axe-core 최신 릴리스는 현재 `4.11.0`이며, RGAA 태그 추가와 함께 일부 best-practice rule 분류가 확장됐다. 규칙 태그 기반 필터링을 쓰는 내부 툴은 버전 업 시 결과 해석이 달라질 수 있다.
- `target-size` 관련 동작도 axe-core 릴리스마다 조정되고 있어, WCAG 2.2 신규 기준을 자동화에 연결할 때는 **엔진 버전 고정 + 주기적 업그레이드 검증**이 필요하다.
- Pa11y는 단발성 CLI뿐 아니라 Dashboard/Webservice/CI를 함께 제공해, 여러 URL에 대한 회귀 추적용 자동화 계층으로 여전히 유효하다.
- Lighthouse accessibility score는 pass/fail audit의 가중 평균이며, 가중치는 axe의 user-impact 분류를 따른다. 즉 Lighthouse accessibility 수치는 사실상 axe 규칙 체계와 강하게 연결돼 있다.

### 중복 검토 메모

- 기존 로그에 이미 있는 내용: DTCG 2025.10 안정 버전 자체, Style Dictionary v4 존재 자체, Figma variables 일반론, OKLCH 기본 개념.
- 이번 추가 조사는 위 항목의 **최신 운영 상태 / 세부 migration / 채택 지표 / 브라우저 지원 수치 / 공식 제품 변화**만 보강했다.

---

## [2026-07-27] - Phase 6 kaizen

**트리거:** kaizen-orchestrator Phase 6 (design-kit). `/insights` 2026-07-27 Friction #2(시각·런타임 검증 신뢰 불가, 신규 최상위) + 글로벌 REJECT `UI-06`(시안 승인 기록 artifact 부재) + reflect-digest 색상 재위반 3종을 신호로 삼았다.

### 조사한 소스 (Phase 6 — 2026-07-27)

| # | 제목 | URL | 유형 | 결과 |
| - | ---- | --- | ---- | ---- |
| 1 | WCAG 2.2 Understanding SC 2.5.8 Target Size (Minimum) | <https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html> | official | 재확인 — 변경 없음 |
| 2 | DTCG Design Tokens Format Module — Final CG Report 2025-10-28 | <https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/> | spec | 채택 (alias 표기 정정 근거) |
| 3 | DTCG Design Tokens Format Module — drafts | <https://www.designtokens.org/TR/drafts/format/> | spec | 채택 (2 확인) |
| 4 | MDN — CSS Container Queries | <https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries> | official | 참조 |
| 5 | MDN — `prefers-reduced-motion` | <https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion> | official | 채택 (reduced-motion 테스트 의미 정정) |
| 6 | Playwright — Visual Comparisons | <https://playwright.dev/docs/test-snapshots> | official | 채택 (baseline vacuous pass 근거) |
| 7 | MDN — `oklch()` | <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch> | official | 재확인 — 변경 없음 |

### 확인된 사실

#### N. DTCG alias 는 중괄호 참조다 (기존 스킬 기재 오류)

- 스펙의 토큰 참조 문법은 **`{group.token}` 중괄호 문자열**이다. 맨몸 dot-notation(`"color.background.surface"`)은 참조가 아니라 일반 문자열 값으로 해석된다.
- 중괄호 참조는 **`$value` 를 가진 완전한 토큰만** 가리킬 수 있다. 토큰 값 내부의 개별 속성을 참조하려면 JSON Pointer(RFC 6901) 형식의 `$ref`(`#/path/to/target`)를 쓴다.
- color 토큰 값은 `colorSpace` / `components` / `hex`(선택) / `alpha`(선택) 객체 구조다. hex 문자열 단독 형식은 스펙에 없다.
- 그룹은 `$extends` 로 다른 그룹을 상속하며 deep merge, 동일 경로에서는 로컬 속성이 우선한다.
- → `design-system` Gotcha 14, `design-component` Gotcha 3 의 "dot notation 권장" 기재를 정정했다. 기존 문구대로 산출하면 Style Dictionary / Tokens Studio 에서 alias 가 해석되지 않는다.

#### O. Playwright 시각 회귀 첫 실행은 아무것도 검증하지 않는다

- 스냅샷이 없으면 Playwright 는 실제 화면을 baseline 으로 자동 기록하고 그 실행을 통과 처리한다 (`A snapshot doesn't exist at ... writing actual`).
- 따라서 `--update-snapshots` 직후의 green 은 증거가 아니다 — 비교 대상이 없었기 때문이다. Evidence Validity Gate 검사 2(활성화)·3(반증 가능성) 실패에 해당한다.
- 렌더가 실패해 빈 화면이 캡처돼도 baseline 과 동일하면 통과한다. Friction #2 의 unbounded-height collapse 사고와 같은 구조다.
- → `design-test` 에 negative control 4 단계 루프(baseline → 의도적 변형으로 실패 확인 → revert 후 통과 → 두 출력 인용)와 콘텐츠 존재 assertion 을 추가했다.

#### P. `prefers-reduced-motion: reduce` 는 "애니메이션 제거" 가 아니다

- 이 설정은 vestibular trigger(scale·pan 등 이동감을 주는 모션)를 **더 온건한 대안으로 교체**하라는 의미다. MDN 예시도 pulse(scale) → dissolve(opacity) 교체를 보여준다.
- Baseline 2020-01 로 널리 지원된다.
- → "애니메이션 개수 0" 으로 assert 하는 테스트는 잘못된 기준이다. `design-test` Gotcha 13 으로 반영했다.

#### Q. WCAG SC 2.5.8 / oklch / Container Queries — 재확인, 변경 없음

- SC 2.5.8 은 AA 24×24 CSS px, 예외 5 종(Spacing / Equivalent / Inline / User Agent Control / Essential). 페이지 갱신일 2026-05-11. 킷의 기존 기재와 일치하므로 수정하지 않았다.
- `oklch()` 는 2023-05 부터 widely available. L 0–1, C 0–0.4, H 0–360(red ≈ 41°). 모던 브라우저는 fallback 불필요, 레거시 대응 시에만 필요. 킷 기재와 일치.
- Container queries 는 baseline 안정. `container-type: size | inline-size | normal`, 단위 `cqw/cqh/cqi/cqb/cqmin/cqmax`. 킷은 `cqw/cqi` 만 언급하나 축소 기재일 뿐 오류가 아니므로 변경하지 않았다.

### 중복 검토 메모 (Phase 6 — 2026-07-27)

- Friction #1(의도 확인 전 편집)·#3(스코프 드리프트)은 직전 사이클에 이미 승격됐고 design-kit 은 관련 Gotcha 를 보유 중이다. 문장을 다시 다듬지 않고 **enforcement 등급 상향**으로만 대응했다.
- 이번 사이클 신규분은 (1) canonical 미검증 임계 정합, (2) Evidence Validity Gate, (3) 시각 변경 프로토콜 SSOT 신설, (4) 승인 기록 아티팩트, (5) DTCG alias 사실 정정 — 5 unit 이다.
