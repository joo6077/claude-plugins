---
title: 컬러
version: 0.3.0
last_updated: 2026-03-30
---

# 컬러

컬러 이론, 심리학, 조화 규칙, 브랜드 컬러 선정 방법론, 시맨틱 토큰 체계, 다크 모드, 접근성을 다룬다.

---

## 원칙

### 1. 60-30-10 법칙

인테리어 디자인에서 차용한 비율이다.

- **60%**: Surface/Background (주요 배경색)
- **30%**: Secondary/Container (카드, 영역 구분)
- **10%**: Primary/Accent (CTA 버튼, 핵심 인터랙션)

이 비율을 지키면 시각적 균형과 계층이 자연스럽게 형성된다. 반대로 Accent를 30% 이상 쓰면 눈이 어디를 봐야 할지 모르는 "크리스마스 트리" 현상이 발생한다.

> **출처:** [NNGroup — The Role of Color in UX](https://www.nngroup.com/articles/color-enhance-design/)

### 2. 색상만으로 정보를 전달하지 않는다

WCAG 1.4.1 "Use of Color"는 색상이 정보 전달의 유일한 수단이 되면 안 된다고 명시한다. 에러: 빨간색 + 아이콘 + 텍스트. 차트: 색상 + 패턴/라벨. 색각 이상(color vision deficiency) 사용자는 전체 남성의 약 8%, 전체 인구의 약 4.5%. 가장 흔한 유형은 적록색각이상(deuteranopia/protanopia)으로 빨강-초록 구분이 안 된다. 따라서 성공=초록 / 에러=빨강 조합은 반드시 아이콘이나 텍스트를 병행해야 한다.

> **출처:** [WCAG 1.4.1 — Use of Color](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html)

### 3. 의미론적(Semantic) 색상을 사용한다

하드코딩된 hex 대신 역할(role) 기반 토큰을 쓴다. `#FF0000` 대신 `color-error`, `#007AFF` 대신 `color-primary`. 이렇게 해야 테마 전환, 다크 모드, 화이트 라벨링이 가능하다.

> **출처:** [Material Design 3 — Color Roles](https://m3.material.io/styles/color/roles)

### 4. 대비(Contrast)를 우선한다

텍스트 최소 4.5:1(AA), UI 컴포넌트 최소 3:1. WebAIM 2024년 백만 사이트 분석에서 **83.6%**가 색상 대비 문제를 보유하고 있었다. 가장 빈번한 실패: 밝은 회색 placeholder 텍스트(대비비 약 2:1).

> **출처:** [WebAIM — The WebAIM Million 2024](https://webaim.org/projects/million/)

---

## 컬러 시스템 구조

### 3계층 토큰 시스템 (3-Tier Token Architecture)

현대 디자인 시스템은 색상을 3단계 계층으로 구조화한다. 이 구조는 일관성, 유지보수성, 테마 확장성을 동시에 확보한다.

```
┌─────────────────────────────────────────────┐
│  Tier 3: Component Token                    │
│  예: button-primary-bg → color-action       │
├─────────────────────────────────────────────┤
│  Tier 2: Semantic Token                     │
│  예: color-action → blue-600               │
├─────────────────────────────────────────────┤
│  Tier 1: Primitive Token (Global/Reference) │
│  예: blue-600 → #1D6AFF                    │
└─────────────────────────────────────────────┘
```

#### Tier 1: Primitive Token (프리미티브 토큰)

원시 색상값을 정의한다. 브랜드에 필요한 모든 색상을 열거하며, 색상 이름과 명도 단계로 구성한다.

```
blue-50, blue-100, blue-200, ..., blue-900
gray-50, gray-100, gray-200, ..., gray-900
red-500, green-500, yellow-500
```

- 무한한 가능성을 유한한 팔레트로 축소하는 역할
- 직접 UI에 사용하지 않고 Semantic 토큰이 참조한다

#### Tier 2: Semantic Token (시맨틱 토큰)

용도와 맥락을 부여한다. "이 색이 무엇에 쓰이는가"를 이름에 담는다.

```
color-text-primary → gray-900 (Light) / gray-50 (Dark)
color-bg-surface   → white (Light) / gray-900 (Dark)
color-action       → blue-600 (Light) / blue-400 (Dark)
color-error        → red-600 (Light) / red-400 (Dark)
```

- 다크 모드 전환 시 이 레이어에서 매핑만 변경하면 된다
- 컴포넌트는 시맨틱 토큰만 참조하므로 테마 변경에 영향받지 않는다

#### Tier 3: Component Token (컴포넌트 토큰)

특정 컴포넌트에 한정된 토큰이다. 컴포넌트별 커스터마이징이나 테마 변형이 필요할 때 사용한다.

```
button-primary-bg       → color-action
button-primary-text     → color-on-action
card-bg                 → color-bg-surface
input-border            → color-outline
input-border-focus      → color-action
```

- 대부분의 경우 Semantic 토큰을 직접 참조하지만, 테마별 독립 변형이 필요하면 별도 정의한다

> **출처:** [Contentful — Design Tokens Explained](https://www.contentful.com/blog/design-token-system/)
> **출처:** [GitLab Pajamas — Design Tokens Overview](https://design.gitlab.com/product-foundations/design-tokens/)
> **출처:** [Material Design 3 — Design Tokens](https://m3.material.io/foundations/design-tokens)

---

## 시맨틱 토큰

### Material Design 3 Color Roles

MD3는 색상을 **역할(Role)** 기반으로 분류한다. 각 역할은 쌍(pair)으로 존재하여 대비를 보장한다.

#### 브랜드 컬러 (Brand Colors)

| 역할 | 용도 | 쌍(Pair) |
|------|------|---------|
| **primary** | CTA 버튼, FAB, 주요 액션 | onPrimary |
| **primaryContainer** | 선택된 상태, 강조 영역 | onPrimaryContainer |
| **secondary** | 필터 칩, 보조 액션 | onSecondary |
| **secondaryContainer** | 내비게이션 선택 상태 | onSecondaryContainer |
| **tertiary** | 보색 강조, 입력 필드 | onTertiary |
| **tertiaryContainer** | 보조 강조 영역 | onTertiaryContainer |

#### 표면 컬러 (Surface Colors)

| 역할 | 용도 |
|------|------|
| **surface** | 페이지 기본 배경 |
| **surfaceContainer** (Low/Medium/High) | 카드, 시트, 다이얼로그 배경 (고도별 분류) |
| **inverseSurface** | 스낵바 등 반전 배경 |
| **onSurface** | 표면 위 텍스트/아이콘 |
| **onSurfaceVariant** | 보조 텍스트, 아이콘 |

#### 유틸리티 컬러 (Utility Colors)

| 역할 | 용도 | 쌍(Pair) |
|------|------|---------|
| **error** | 에러 상태 | onError |
| **errorContainer** | 에러 배경 | onErrorContainer |
| **outline** | 경계선, 구분선 | - |
| **outlineVariant** | 약한 구분선 | - |

> **출처:** [Material Design 3 — Color Roles](https://m3.material.io/styles/color/roles)

### Apple HIG Semantic Colors (iOS)

Apple은 역할 기반의 **Dynamic Color**를 제공하며, Light/Dark 모드에서 자동 전환된다.

| 토큰 | 용도 |
|------|------|
| **label** / **secondaryLabel** / **tertiaryLabel** | 텍스트 계층 (자동 불투명도 조절) |
| **systemBackground** / **secondarySystemBackground** | 배경 계층 |
| **separator** / **opaqueSeparator** | 구분선 |
| **systemFill** / **secondarySystemFill** | 채움 영역 |
| **tintColor** | 앱 강조색 (브랜드 컬러) |
| **systemRed**, **systemBlue**, **systemGreen** 등 | 시스템 색상 (Light/Dark 자동 전환) |

- iOS의 시맨틱 색상은 접근성 설정(고대비, 투명도 감소)에도 자동 대응한다

> **출처:** [Apple HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color)

### 시맨틱 토큰 네이밍 규칙

```
[카테고리]-[역할]-[변형]

예시:
color-text-primary        텍스트 기본색
color-text-secondary      텍스트 보조색
color-text-disabled       텍스트 비활성
color-bg-surface          기본 배경
color-bg-elevated         부유(elevated) 배경
color-action-primary      주요 액션
color-action-destructive  파괴적 액션 (삭제 등)
color-border-default      기본 경계선
color-border-focus        포커스 경계선
color-status-success      성공 상태
color-status-warning      경고 상태
color-status-error        에러 상태
color-status-info         정보 상태
```

---

## 다크 모드

### 핵심 원칙

#### 1. 단순 반전(Inversion)이 아니다

Apple HIG는 다크 모드를 "조명을 어둡게 낮춘 것"으로 비유하며, 라이트 모드의 단순 색상 반전이 아니라고 강조한다. 별도의 색상 세트를 할당해야 한다.

> **출처:** [Apple HIG — Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

#### 2. Base / Elevated 배경 체계 (Apple)

Apple은 다크 모드에서 두 가지 배경 세트를 사용한다.

| 세트 | 용도 | 밝기 |
|------|------|------|
| **Base** | 기본 화면 배경 | 더 어두움 (뒤로 밀려나는 느낌) |
| **Elevated** | 팝오버, 모달 시트, 전면 인터페이스 | 상대적으로 밝음 (앞으로 나오는 느낌) |

- 시스템 배경색을 사용하면 base/elevated 전환이 자동으로 처리된다
- 커스텀 배경색을 사용하면 이러한 시스템 제공 깊이 구분이 불가능해진다

> **출처:** [Apple HIG — Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

#### 3. 톤 기반 고도 시스템 (Material Design 3)

MD3는 다크 테마에서 그림자(shadow) 대신 **톤 컬러 오버레이(tonal color overlay)**로 고도(elevation)를 표현한다. primary 색상 슬롯에서 오버레이 색상을 가져온다.

| 고도 | Surface 토큰 | 설명 |
|------|-------------|------|
| 0 | surface | 기본 배경 |
| 1 | surfaceContainerLowest | 최하위 컨테이너 |
| 2 | surfaceContainerLow | 하위 컨테이너 |
| 3 | surfaceContainer | 기본 컨테이너 |
| 4 | surfaceContainerHigh | 상위 컨테이너 |
| 5 | surfaceContainerHighest | 최상위 컨테이너 |

- 고도가 높아질수록 primary tint가 가미되어 표면이 밝아진다
- 이전 MD2의 투명도 기반 오버레이에서 고정 톤값으로 변경되어 예측 가능성이 향상되었다

> **출처:** [Material Design 3 — Color System Overview](https://m3.material.io/styles/color/system/overview)

#### 4. 다크 모드 색상 조정 가이드

| 요소 | 라이트 모드 | 다크 모드 | 조정 방향 |
|------|-----------|----------|----------|
| **배경** | 밝은 회색/흰색 | 어두운 회색 (#121212~#1C1C1E) | 순수 검정(#000000) 피하기 |
| **텍스트** | gray-900 | gray-50~100 | 순수 흰색(#FFFFFF) 대신 약간 톤다운 |
| **Primary** | 채도 높은 원색 | 채도 낮추고 명도 올림 | tonal palette에서 밝은 톤 선택 |
| **그림자** | 그림자로 고도 표현 | 표면 밝기로 고도 표현 | 다크 배경 위 그림자는 비가시 |
| **이미지/일러스트** | 원본 유지 | 밝기/채도 감소 고려 | 눈부심 방지 |

- 다크 모드 배경에 순수 검정(#000000)을 사용하면 OLED 스미어링(smearing) 현상과 과도한 대비가 발생할 수 있다
- Apple은 systemBackground로 약간의 회색(#000000이 아님)을 기본 제공한다

> **출처:** [Median.co — Apple's HIG for Dark Mode](https://median.co/blog/what-are-apples-human-interface-guidelines-for-dark-mode)

---

## 접근성 (Contrast Ratio)

### WCAG 2.1 대비 요구사항

| 기준 | 일반 텍스트 | 대형 텍스트 | UI 컴포넌트/그래픽 |
|------|-----------|-----------|-------------------|
| **AA** (필수) | **4.5:1** | **3:1** | **3:1** |
| **AAA** (권장) | **7:1** | **4.5:1** | - |

#### 대형 텍스트 정의

- **18pt (24px)** 이상 일반 굵기 텍스트
- **14pt (약 18.66px)** 이상 Bold 텍스트
- CJK(한중일) 폰트도 동일 기준 적용

#### UI 컴포넌트 요구사항 (WCAG 2.1 추가)

WCAG 2.1에서 추가된 1.4.11 "Non-text Contrast"는 UI 컴포넌트(버튼 경계선, 입력 필드, 체크박스)와 의미 있는 그래픽이 인접 색상과 최소 **3:1** 대비를 유지해야 한다고 규정한다.

> **출처:** [WCAG 1.4.3 — Contrast Minimum](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
> **출처:** [WCAG 1.4.11 — Non-text Contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html)

### 면제 대상

- **비활성(Disabled) UI 요소**: 현재 조작 불가능한 컴포넌트 (예: disabled 버튼)
- **장식 텍스트**: 순수 장식 목적의 텍스트
- **로고/브랜드**: 로고타입에 사용된 텍스트
- **부수적 텍스트**: 사진 속 우연히 포함된 텍스트

### 대비 검사 도구

| 도구 | 유형 | URL |
|------|------|-----|
| **WebAIM Contrast Checker** | 웹 | https://webaim.org/resources/contrastchecker/ |
| **Stark** | Figma/Sketch 플러그인 | https://www.getstark.co/ |
| **Axe DevTools** | 브라우저 확장 | https://www.deque.com/axe/ |
| **Colour Contrast Analyser (CCA)** | 데스크톱 앱 | https://www.tpgi.com/color-contrast-checker/ |
| **Accessibility Insights** | 브라우저 확장 | https://accessibilityinsights.io/ |

> **출처:** [WebAIM — Contrast Checker](https://webaim.org/resources/contrastchecker/)

### 흔한 실수와 방지법

#### 1. 인터랙티브 요소의 상태별 대비 누락

버튼의 기본(default) 상태만 검사하고, hover, focus, disabled 상태의 대비를 무시하는 경우가 빈번하다. 모든 인터랙션 상태에서 대비를 검증해야 한다.

#### 2. 밝은 색상 + 흰색 배경 조합

밝은 파란색, 밝은 회색 등의 텍스트를 흰색 배경에 배치하면 상대 휘도(relative luminance)가 너무 가까워 대비를 충족하지 못한다. 특히 placeholder 텍스트에서 자주 발생한다.

#### 3. 이미지 위 텍스트

배경 이미지 위에 텍스트를 배치하면 이미지의 밝기가 부분마다 달라 대비가 일정하지 않다. 반드시 반투명 오버레이(scrim)를 추가하거나 텍스트에 그림자를 적용한다.

#### 4. 데이터 시각화에서 색상만 사용

차트, 그래프에서 색상만으로 데이터 시리즈를 구분하면 색각 이상 사용자가 구분할 수 없다. 패턴, 라벨, 모양(shape)을 병용해야 하며, 인접 색상 간 3:1 대비를 확보한다.

#### 5. 비텍스트 요소 대비 간과

WCAG 2.1의 비텍스트 대비(1.4.11) 기준을 인지하지 못하여, 입력 필드 경계선, 아이콘, 그래프 요소의 대비를 검증하지 않는 경우가 많다.

> **출처:** [UX Collective — 3 Color Contrast Mistakes Designers Still Make](https://uxdesign.cc/3-color-contrast-mistakes-designers-still-make-68cc224735b3)
> **출처:** [WebAIM — Contrast and Color Accessibility](https://webaim.org/articles/contrast/)
> **출처:** [Accessible Web — Color Contrast Checker](https://accessibleweb.com/color-contrast-checker/)

---

## 색상 심리학 (Color Psychology)

색상이 사용자 행동과 인식에 미치는 영향은 문화권에 따라 다르다. 아래는 서구권 + 동아시아권 공통 연구 결과를 기반으로 한 실무 참고 정보이며, 절대 법칙이 아니다.

### 색상별 연상과 UI 활용

| 색상 | 서구권 연상 | 동아시아 연상 | UI 활용 | 주의점 |
|------|-----------|-------------|---------|--------|
| **파란색** | 신뢰, 안정, 전문성 | 신뢰, 기술, 차가움 | 금융, 헬스케어, 기업 앱의 Primary | 과다 사용 시 차갑고 비인간적 인상 |
| **빨간색** | 긴급, 에너지, 경고 | 행운, 축하(중국), 경고 | CTA 버튼 강조, 에러 상태, 세일 뱃지 | 에러와 혼동 가능 — CTA로 쓸 때 맥락 분리 필수 |
| **초록색** | 자연, 성공, 성장 | 자연, 건강 | 성공 피드백, 헬스/환경 앱 | 적록색각이상자에게 빨강과 구분 어려움 |
| **노란색** | 주의, 낙관, 경고 | 황실(전통), 주의 | 경고 배너, 하이라이트 | 밝은 배경에서 대비 확보 어려움 (텍스트 금지) |
| **주황색** | 활력, 친근함 | 활력, 즐거움 | 보조 CTA, 알림 뱃지 | 빨강과 노랑 사이에서 의미 모호 |
| **보라색** | 고급, 창의성 | 고급, 신비 | 프리미엄 서비스, 크리에이티브 도구 | 남성 사용자에게 선호도 낮다는 연구 존재 |
| **검정색** | 세련, 권위 | 죽음(전통), 세련(현대) | 럭셔리 브랜드, 패션 | 다크 모드 배경에는 순수 검정(#000) 피하기 |

**HubSpot A/B 테스트 사례:** 빨간색 CTA 버튼이 초록색 대비 클릭률 21% 높았다. 단, 이 결과는 주변 색상 대비에 의한 것이지 빨간색 자체의 효과가 아닐 수 있다. 색상 심리학 연구의 재현성(replicability)은 낮은 편이므로, 반드시 자체 A/B 테스트로 검증한다.

> **출처:** [Smashing Magazine — Color Theory for Designers](https://www.smashingmagazine.com/2010/01/color-theory-for-designers-part-1-the-meaning-of-color/)
> **출처:** [HubSpot — The Button Color A/B Test](https://blog.hubspot.com/blog/tabid/6307/bid/20566/the-button-color-a-b-test-red-beats-green.aspx)

---

## 색상 조화 규칙 (Color Harmony)

색상환(color wheel) 위에서 색상 간 각도 관계로 조화를 정의한다. UI에서는 보통 1개의 Primary를 선정한 뒤, 아래 규칙으로 보조색을 도출한다.

### 주요 조화 유형

| 유형 | 색상환 관계 | 특성 | UI 적용 예 |
|------|-----------|------|-----------|
| **보색 (Complementary)** | 180° 반대편 | 강한 대비, 긴장감 | CTA 버튼 강조. 단, 동시 사용 면적을 10% 이하로 제한 |
| **유사색 (Analogous)** | 인접 30~60° | 부드럽고 자연스러운 조화 | 그라데이션 배경, 차트의 동일 카테고리 색상 |
| **삼각 (Triadic)** | 120° 등간격 | 풍부하고 활기찬 팔레트 | 3가지 정보 카테고리 구분(차트, 대시보드) |
| **분할보색 (Split-Complementary)** | 보색의 양옆 30° | 보색보다 덜 긴장되면서도 대비 유지 | Primary + 두 가지 Accent 조합 |
| **이중보색 (Tetradic)** | 90° 간격 4색 | 가장 풍부하지만 균형 잡기 어려움 | 4개 이상 카테고리 구분이 필요한 복잡한 대시보드 |
| **단색 (Monochromatic)** | 동일 색조, 명도/채도만 변경 | 가장 안전하고 일관성 높음 | 미니멀 UI, 단일 브랜드 색상 기반 디자인 시스템 |

### 실무 팔레트 구성 프로세스

1. **Primary 선정**: 브랜드 핵심 색상 1개 결정
2. **Neutral 도출**: Primary에서 채도를 2~5%로 낮춘 회색 계열 (순수 회색보다 따뜻하거나 차가운 뉘앙스)
3. **Secondary**: 유사색 또는 분할보색 규칙에서 도출
4. **Semantic 4색**: Success(초록), Warning(노랑/주황), Error(빨강), Info(파랑) — 브랜드와 독립적으로 고정
5. **명도 스케일**: 각 색상에 대해 50~950 (또는 100~900) 단계로 10~13개 명도 변형 생성

> **출처:** [Adobe Color — Color Wheel](https://color.adobe.com/create/color-wheel)
> **출처:** [Interaction Design Foundation — Color Theory](https://www.interaction-design.org/literature/topics/color-theory)

---

## 브랜드 컬러 선정 방법론

### 1단계: 경쟁사 컬러 감사

동일 업종 상위 10개 앱/사이트의 Primary 색상을 수집한다. 대부분 파란색 계열에 몰려 있다면 차별화를 위해 다른 색조를 검토한다. 반대로 업종 관례(예: 금융=파랑, 음식=빨강/주황)를 무시하면 사용자 기대와 충돌한다.

### 2단계: 60-30-10 시뮬레이션

후보 색상으로 실제 UI 목업을 만들어 60-30-10 비율을 적용한다. Figma에서 3가지 후보 팔레트를 병렬로 놓고 비교한다.

### 3단계: 접근성 사전 검증

Primary 색상이 흰색/검정 배경 모두에서 AA 대비(4.5:1)를 충족하는지 확인한다. 충족하지 않으면 명도를 조정하거나 대비용 변형(darker/lighter variant)을 준비한다.

### 4단계: 다크 모드 적합성

라이트 모드 Primary를 다크 모드에서 그대로 쓰면 채도가 과해 눈부심이 발생한다. 다크 모드용 변형(명도 +20~30, 채도 -10~20)을 미리 준비한다.

### 안티패턴

- **순수 검정(#000000) 배경**: OLED smearing, 과도한 대비. 대신 #121212~#1C1C1E 사용
- **Primary를 에러 색상으로 사용**: 브랜드 빨강이 Primary인 경우, Error와 Primary가 구분 불가. Error에는 별도 톤(더 어두운 빨강 또는 주황)을 지정
- **너무 많은 색상**: 6색 이상의 Primary/Secondary/Tertiary 조합은 시스템 복잡도만 증가시킨다

> **출처:** [Refactoring UI — Building Your Color Palette](https://www.refactoringui.com/)
> **출처:** [Material Design 3 — How the Color System Works](https://m3.material.io/styles/color/system/how-the-system-works)
