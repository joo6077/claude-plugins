---
version: 1.3.0
last_updated: 2026-08-13
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

---

## [2026-08-13] - Phase 6 kaizen

**트리거:** kaizen-orchestrator Phase 6 (design-kit). Step 0.6 선별에서 design-kit 은 low-signal 제외
후보였으나 사용자가 전체 14 Phase 를 선택했다. 신호는 글로벌 REJECT `UI-04`(계약이 4 축을 **이미 명시**
했는데 두 안이 전 축 동일값)와 §0 신규 델타다. 외부 근거는 codex 를 foreground 로 호출해
`.harness/.meta/evidence/phase6.md` 에 파일로 고정한 뒤 그 파일만 읽고 작업했다 (백그라운드 실행 중
네트워크 조회 금지). 커밋 `965af48` — 13 파일. sync-docs 자동 동기화는 `450e553`.

### 조사한 소스 (Phase 6 — 2026-08-13)

| # | 제목 | URL | 유형 | 결과 |
| - | ---- | --- | ---- | ---- |
| 69 | Morphological Charts — Cambridge IfM DMG | <https://www.ifm.eng.cam.ac.uk/research/dmg/tools-and-techniques/morphological-charts/> | official | 채택 (축 → 값 → 조합 구조의 근거) |
| 70 | Morphological chart 조합 폭발 — Clemson thesis | <https://open.clemson.edu/all_theses/274/> | paper | 참조 |
| 71 | 생성 디자인 거리 기반 sampling — Strathprints | <https://strathprints.strath.ac.uk/70009/> | paper | 참조 (구조 feature vector 우선, perceptual diff 는 보조) |
| 72 | Playwright — Visual Comparisons | <https://playwright.dev/docs/test-snapshots> | official | 채택 (골든 단독은 증거가 아님) |
| 73 | Playwright — Actionability | <https://playwright.dev/docs/actionability> | official | 채택 (visible locator) |
| 74 | Playwright — Assertions | <https://playwright.dev/docs/test-assertions> | official | 채택 (count/height assertion) |
| 75 | Chromatic — Visual tests | <https://www.chromatic.com/docs/visual/> | official | 참조 — decision → surface → golden 을 native 로 강제하는 개념 미확인 |
| 76 | Percy — How it works | <https://percy.io/how-it-works> | official | 참조 (75 와 동일 결론) |
| 77 | BackstopJS | <https://github.com/garris/BackstopJS> | official | 참조 (75 와 동일 결론) |
| 78 | W3C ACT Rules Format | <https://www.w3.org/TR/act-rules-format/> | spec | 채택 (manifest 를 요구사항–테스트 traceability 로 정당화) |
| 79 | WCAG 2.2 Specification | <https://www.w3.org/TR/WCAG22/> | spec | 채택 (터치 타겟 레벨 귀속 정정) |
| 80 | Tailwind CSS v4 | <https://tailwindcss.com/blog/tailwindcss-v4> | official | 참조 — OKLCH 를 승인값 위에 두지 않음 |
| 81 | DTCG Format Module — Final CG Report 2025-10-28 | <https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/> | spec | 재확인 — 변경 없음 |
| 82 | DTCG — 첫 stable 버전 발표 | <https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/> | official | 재확인 — 변경 없음 |
| 83 | MDN — Container Queries (Guides/Containment) | <https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries> | official | 재확인 — 변경 없음 |
| 84 | Expressive Material Design — Google Research | <https://design.google/library/expressive-material-design-google-research?pubDate=20250521> | official | 참조 — 기존 승인값보다 상위로 두지 않음 |
| 85 | Apple — Adopting Liquid Glass | <https://developer.apple.com/tutorials/data/documentation/technologyoverviews/adopting-liquid-glass.md> | official | 참조 (84 와 동일 결론) |

### 확인된 사실

#### R. 변형 구별성은 "확립된 UI 표준" 이 아니라 설계 탐색 방법의 이식이다

- Morphological chart 는 기능/축별 가능한 수단을 나열하고 조합해 design space 를 만드는 방법이며,
  조합 폭발과 비실용 해를 제한해야 한다고 설명한다. UI 변형도 `축 → 값 → 조합` 으로 다루면 동일
  feature vector 를 가진 두 안을 **기계적으로** 잡을 수 있다.
- 생성 디자인 연구에는 거리 기반 sampling·clustering·psychophysical distance 로 "서로 다르게 지각되는
  대안" 을 만드는 접근이 있다. 다만 design-kit 에는 **구조 feature vector / Hamming distance 를 먼저**
  두고 렌더 후 perceptual diff 는 보조 신호로만 두는 편이 맞다 — 큰 pixel diff 가 구조 중복을 면제하지 않는다.
- → `visual-change-protocol.md` §5 Variant Contract Matrix + Distinctiveness Gate 로 반영했다.

#### S. 시각 회귀 도구는 "결정이 모든 표면에 갔는가" 를 강제하지 않는다

- Playwright · Chromatic · Percy · BackstopJS 는 baseline snapshot, diff, threshold, ignore/delay/
  selector/scenario 를 제공한다. 그러나 확인한 공식 문서 범위에서
  `decision → required surface → golden coverage` 를 native 개념으로 강제하는 패턴은 **미확인**이다.
- 즉 이것은 도구의 기본 기능이 아니라 그 위에 얹는 **manifest 기반 traceability gate** 다. W3C ACT
  Rules Format 이 테스트 규칙에 requirement mapping · applicability · expectations · outcome mapping 을
  요구하는 구조가 같은 형태의 선례다.
- → §6 Decision Propagation Manifest 로 반영했다.

#### T. "스크린샷 파일이 있다" 는 "사용자가 보는 상태를 측정했다" 가 아니다

- Playwright 의 visual comparison 은 첫 실행에서 reference 를 만들고 다음 실행부터 비교하며, rendering
  은 OS·브라우저·폰트·하드웨어에 따라 달라질 수 있다고 경고한다. 실제 관측에는 locator visibility,
  non-empty bounding box, count/text/in-viewport 같은 assertion 이 필요하다.
- → §7 Evidence Channels 4 종과 PASS 문장 5 요소로 반영했다. 이 항목은 2026-07-27 의 O(첫 실행 vacuous
  pass)와 같은 뿌리이지만, 그때는 `design-test` 안의 negative control 루프였고 이번에는 **증거 강도를
  이름으로 구분하는 채널 규약**으로 승격한 것이다.

#### U. 44×44 는 AA 가 아니다 (킷 기재 오류)

- WCAG 2.2 에서 AA 하한은 **SC 2.5.8 의 24×24 CSS px** 이고, **44×44 는 SC 2.5.5 AAA** 다. Apple HIG 의
  44pt 는 플랫폼 권장치로 그와 별개다.
- 킷 문서 **6 줄**이 44 를 레벨 귀속 없이 터치 타겟 기준으로 제시하고 있었다 (`design-guide` 의 예시
  문장 포함). 5 파일에서 "AA 24×24 / AAA·Apple HIG 44×44" 로 귀속 표기했고 범위 안 잔존은 0 건이다.
- 음성 대조로 판별력을 확인했다 — 귀속 낱말 1 개를 제거하니 다시 1 건이 검출됐다.
- 직전 사이클(2026-07-27)은 같은 SC 를 "킷 기재와 일치 — 수정하지 않았다" 로 기록했다. 이번에
  `docs/design/**` 산문까지 범위를 넓히자 6 줄이 나왔다.

### 변경 내역

- `references/visual-change-protocol.md` — §5~§7 을 **append-only** 로 신설 (§1~§4 삭제 0 줄).
  - **§5 Variant Contract Matrix + Distinctiveness Gate** — variant 필수 4 필드(`variant_id` ·
    `strategy_label` · `axis_vector` · `intended_user_scenario`), 산출 **전** 합의하는 6 열 매트릭스,
    pairwise 판정식(지정 축 3 개 이상이면 Hamming ≥ 2, 2 개 이하면 ≥ 1). 색상·토큰 값·카피·아이콘은
    축으로 세지 않는다. 실행 가능한 게이트가 `UI-04` 를 hamming=0 으로 재현하고 exit 1 을 낸다.
    개수 상한·부대 산출물 금지는 재정의하지 않고 `harness/docs/guides/skill-design-guide.md` §5.6
    Variant Budget 을 인용했으며, design-kit 추가분은 "사용자 지정 N 은 정확히 N · 승인 상한 5" 2 조뿐이다.
  - **§6 Decision Propagation Manifest** — `decisions.yaml` 스키마(`decision_id` → `required_surfaces[]`
    → `golden` + `assertions`, `excluded_surfaces` 는 이유 필수) + coverage rule 4 조. 핵심은
    **골든만 있고 visible / count / height assertion 이 없으면 FAIL** 이라는 것 — 빈 화면도 baseline 과
    같으면 통과하기 때문이다. 체커는 manifest 부재를 통과로 접지 않고 `NO_MANIFEST` + exit 3 을 낸다.
  - **§7 Evidence Channels** — `artifact_snapshot` / `dom_snapshot` / `browser_user_visible` /
    `device_user_visible` 4 채널 + PASS 문장 5 요소(viewport · route/state · visible locator ·
    count/height · screenshot/golden id). 사용자 보고 규약은 재서술하지 않고 skill-design-guide §3.8 ·
    agent-design-guide §10 을 경로+절 번호로 참조했다.
- `skills/design-mockup/SKILL.md` — 고정 "시안 5개" 3 곳 제거 → 개수 계약(미지정 3 · 사용자 지정 N 은
  정확히 N · 승인 상한 5). Step 3 을 3-a(개수·축 합의) / 3-b(합의된 개수만큼 생성)로 분리. 전략 레이블
  5 종을 "전부 내라" 는 목록에서 **후보 풀**로 재규정. Gotcha 1 재작성 + 16(매트릭스 선합의) ·
  17(시안 캡처는 `artifact_snapshot`) 신설.
- `skills/design-concept/SKILL.md` — Gotcha 6 을 "구별성은 계산해서 확인한다" 로 재작성하고 §5 게이트에 연결.
- `skills/design-test/SKILL.md` — Gotcha 14 · 15 신설, Step 5-b(결정 전파 테스트 생성) 신설. manifest
  부재는 "해당 없음" 이 아니라 "manifest 부재" 로 보고한다.
- `skills/design-audit/SKILL.md` — Gotcha 14 · 15 신설. Decision Propagation Coverage 를 10 카테고리
  **앞의 전제 조건 검사**로 두고 `N/10` 과 L3 커버리지 계산에는 넣지 않는다. FAIL 1 건 이상이면 REJECT.
- `skills/design-guide/SKILL.md` — Gotcha 1 예시 문장의 44pt 를 24×24 로 교체.
- `agents/design-reviewer.md` — 규칙 12(Decision Propagation Coverage) · 13(증거 채널) 신설 +
  안티패턴 3 줄 + REJECT 조건 1 줄.
- `docs/design/` 5 파일 — 터치 타겟 레벨 귀속 정정 (`accessibility/accessibility.md` ·
  `foundations/ratio-proportion.md` · `foundations/visual-hierarchy.md` · `interaction/navigation.md` ·
  `systems/apple-hig.md`).

검증: 25 조건 · 하위 검사 47 건을 zsh · bash 양쪽에서 실행해 출력 동일을 확인했다. 게이트 2 종은
문서에서 그대로 추출해 음성 대조까지 돌렸다.

### 경계 준수 — 넣지 않은 것

- **특정 시각 회귀 도구를 표준으로 강제하지 않았다.** Playwright · Chromatic · Percy · BackstopJS 중
  어느 것도 design-kit 전체 표준으로 지정하지 않았고, §6 은 도구 중립 manifest 계층으로만 얹었다.
- **OKLCH · M3 Expressive · Liquid Glass 를 기존 승인값보다 상위 규칙으로 두지 않았다.** "승인 기록이
  이긴다" 는 §1 우선순위는 그대로다.
- 모든 화면·상태에 골든을 무차별 생성하도록 만들지 않았다 — manifest 가 대상 표면을 좁힌다.
- perceptual / pixel diff 만으로 "서로 다른 시안" 이라고 판정하지 않는다 — 구조 feature vector 가 먼저고
  렌더 diff 는 보조다.

### 중복 검토 메모 (Phase 6 — 2026-08-13)

- 직전 사이클(2026-07-27)의 Evidence Validity Gate · 시각 변경 프로토콜 SSOT · 승인 기록 아티팩트는
  **다시 손대지 않았다.** 이번 §5~§7 은 그 위에 얹은 신규 절이며 §1~§4 삭제는 0 줄이다.
- 직전 사이클이 "재확인 — 변경 없음" 으로 남긴 DTCG · container queries 는 이번에도 변경 사항이 없었다.
- `design-kit/README.md` 는 Phase 6 범위 밖이라 손대지 않았고, `design-mockup` description 1 줄 변경으로
  생긴 드리프트 1 건은 DG-04 로 측정해 Final 단계에 넘겼다 (`450e553` 에서 해소).

### 다음 사이클 후보 (이번에 미반영)

- `Hamming ≥ 2` 를 전역 기본으로 둘지, 지정 축 4 개 이상일 때만 둘지.
- `decisions.yaml` 위치를 `.design/decisions.yaml` 로 고정할지, toolkit 별 manifest 를 허용할지.
- golden 을 repo 에 커밋할지, CI artifact / 외부 baseline 으로 둘지.
- surface registry 를 수동 작성하게 할지, 라우트 · 스토리북 · 화면 목록에서 자동 생성하게 할지.
- Distinctiveness Gate 의 현재 등급은 **E1**(문장 규약 + 매트릭스 아티팩트)이다. 축 값이 겹치는
  variant 가 다시 관측되면 문장을 다듬지 말고 판정식을 CI 게이트로 승급할 것.
