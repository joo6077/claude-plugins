---
title: Material Design 분석
version: 0.2.0
last_updated: 2026-03-30
---

# Material Design 분석

Material Design은 Google이 2014년에 발표한 디자인 언어로, 현재 Material Design 3 (Material You)까지 발전하였다. 본 문서는 M3의 핵심 원칙, 디자인 토큰 체계, 주요 컴포넌트 패턴을 정리한다.

---

## 핵심 원칙

### Material You (Material Design 3)

2021년 Google I/O에서 발표된 Material You는 **개인화**와 **적응형 디자인**을 핵심으로 한다. 사용자의 배경화면에서 색상을 추출하여 앱과 시스템 UI에 적용하는 다이내믹 컬러가 가장 두드러지는 특징이다.

**버전 변천:**

| 버전 | 연도 | 핵심 특징 |
|------|------|----------|
| Material Design 1 | 2014 | 물리적 종이 메타포, 그림자, 그리드 기반 레이아웃 |
| Material Design 2 | 2018 | 커스터마이징 강화, 둥근 모서리, 흰 여백, 하단 네비게이션 |
| Material Design 3 | 2021 | 다이내믹 컬러, 개인화, 더 큰 버튼, 부드러운 곡선 |
| M3 Expressive | 2025 | 더 화려한 색상, 풍부한 애니메이션, 모던한 UI (Android 16) |

> **출처:** [Wikipedia — Material Design](https://en.wikipedia.org/wiki/Material_Design)

### 핵심 설계 원칙

**1. 개인화 (Personalization)**
- 사용자 배경화면에서 알고리즘으로 색상을 추출하여 개인 맞춤형 테마 생성
- 브랜드 컬러와 사용자 선호를 동시에 반영하는 유연한 색상 체계

**2. 적응형 디자인 (Adaptive Design)**
- 폰, 태블릿, 폴더블, 데스크톱, Wear OS까지 다양한 화면 크기와 폼 팩터에 적응
- 반응형 레이아웃 그리드와 적응형 컴포넌트 제공
- Canonical layouts (목록-상세, 피드, 보조 패널) 활용

**3. 접근성 우선 (Accessibility by Default)**
- 토널 팔레트 시스템으로 대비 있는 색상 조합을 자동 생성
- 대비비가 WCAG 기준을 충족하도록 설계된 색상 역할(role) 체계

> **출처:** [Material Design 3 — Foundations](https://m3.material.io/foundations)

---

## Material 3 토큰 체계

Material 3의 디자인 토큰은 UI 요소의 시각적 속성(색상, 타이포그래피, 간격, 모양)을 저장하는 이름 있는 엔티티다. 디자인, 도구, 코드에서 동일한 토큰을 사용하여 일관성을 보장한다.

### 3단계 토큰 계층

토큰은 계층 구조를 이루며, 각 수준이 하위 수준으로부터 값을 상속받는다.

```
Reference Tokens → System Tokens → Component Tokens
(구체적 값)        (역할/의미)       (컴포넌트 속성)
```

#### 1. 참조 토큰 (Reference Tokens)

구체적인 실제 값을 보유하는 가장 하위 수준의 토큰. HEX 색상, 픽셀 크기, 폰트 패밀리 이름 등 원시 값을 담는다.

```
md.ref.palette.primary40 = #6750A4
md.ref.palette.neutral90 = #E6E1E5
md.ref.typeface.brand = "Roboto"
md.ref.typeface.plain = "Roboto"
```

#### 2. 시스템 토큰 (System Tokens)

디자인 시스템의 성격과 의미를 부여하는 역할 기반 토큰. 참조 토큰에서 값을 상속받으며, 라이트/다크/고대비 테마 전환 시 **시스템 토큰이 가리키는 참조 토큰만 교체**하면 전체 테마가 변경된다.

```
md.sys.color.primary = md.ref.palette.primary40
md.sys.color.on-primary = md.ref.palette.primary100
md.sys.color.surface = md.ref.palette.neutral99
md.sys.typescale.body-large = { font: Roboto, size: 16sp, weight: 400 }
md.sys.shape.corner.medium = 12dp
```

주요 시스템 토큰 카테고리:
- `--md-sys-color-*`: 다이내믹 컬러 역할 (primary, secondary, surface 등)
- `--md-sys-typescale-*`: 타이포그래피 스케일 역할
- `--md-sys-shape-*`: 코너 반경 역할
- `--md-sys-elevation-*`: 그림자 수준 역할

#### 3. 컴포넌트 토큰 (Component Tokens)

개별 UI 요소에 할당되는 디자인 속성. 시스템 토큰 또는 구체적 값을 참조한다.

```
md.comp.filled-button.container.color = md.sys.color.primary
md.comp.filled-button.label-text.color = md.sys.color.on-primary
md.comp.filled-button.container.shape = md.sys.shape.corner.full
md.comp.filled-button.container.height = 40dp
```

> **출처:** [Material Design 3 — Design Tokens](https://m3.material.io/foundations/design-tokens)
> **출처:** [Medium — What are Design tokens in Material Design System?](https://medium.com/@niranjanky14/what-are-design-tokens-in-material-design-system-jetpack-compose-c925f4c37720)

### 다이내믹 컬러 (Dynamic Color)

Material 3의 핵심 기능으로, 사용자의 배경화면에서 알고리즘으로 색상을 추출하여 앱 전체에 적용한다.

**색상 역할 (Color Roles):**

| 역할 | 용도 |
|------|------|
| **Primary** | 주요 컴포넌트 — 눈에 띄는 버튼, 활성 상태, 높은 표면의 틴트 |
| **Secondary** | 필터 칩, 덜 두드러지는 컴포넌트 — 색상 표현의 확장 |
| **Tertiary** | Primary/Secondary의 균형을 맞추는 대비 악센트, 특정 요소 강조 |
| **Error** | 오류 상태 표시 |
| **Surface** | 배경, 카드, 시트 등의 표면 |
| **On-[역할]** | 해당 역할 위에 표시되는 콘텐츠 색상 (대비 보장) |
| **[역할]-Container** | 해당 역할의 컨테이너 색상 |

**토널 팔레트 생성 알고리즘:**

1. 브랜드 컬러(또는 배경화면)에서 기본 색상 추출
2. 알고리즘이 색조(hue)와 채도(chroma)를 조작하여 **5가지 키 컬러** 생성: Primary, Secondary, Tertiary, Neutral, Neutral Variant
   - Primary: chroma 48, tone 40 — 선명하고 눈에 띄는 색상
   - Secondary: chroma 16, tone 40 — 차분한 보조 색상
3. 각 키 컬러에서 **13단계 톤**(0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100)의 팔레트 생성
4. 대비되는 톤을 조합하여 접근성 기준을 자동 충족하는 색상 쌍 구성

> **출처:** [Material Design 3 — Color Roles](https://m3.material.io/styles/color/roles)
> **출처:** [Material Design 3 — How the Color System Works](https://m3.material.io/styles/color/system/how-the-system-works)

---

## 주요 컴포넌트 패턴

### FAB (Floating Action Button)

화면의 가장 중요한 단일 액션을 표시하는 플로팅 버튼.

**변형:**

| 변형 | 크기 | 용도 |
|------|------|------|
| **FAB** | 56 x 56 dp | 기본 크기, 주요 액션 |
| **Small FAB** | 40 x 40 dp | 보조 액션, 공간 절약 |
| **Large FAB** | 96 x 96 dp | 가장 시각적으로 두드러진 액션 |
| **Extended FAB** | 가변 너비 | 아이콘 + 텍스트 레이블, 가장 눈에 띄는 버튼 |

**M3 변경사항:**
- M2 대비 더 각진(boxier) 형태, 작은 코너 반경
- 코너 반경: FAB 16dp, Small FAB 12dp, Large FAB 28dp
- Surface 색상 위에 Primary Container 색상 사용
- 화면당 하나의 FAB만 사용 권장

> **출처:** [Material Design 3 — FAB](https://m3.material.io/components/floating-action-button/overview)

### 네비게이션 (Navigation)

M3는 화면 크기에 따라 다른 네비게이션 컴포넌트를 사용하는 적응형 패턴을 권장한다.

#### 네비게이션 바 (Navigation Bar)

하단에 위치하는 모바일 전용 네비게이션. iOS의 탭 바에 해당.

- **목적지 수**: 3~5개
- **높이**: 80dp
- 각 항목은 아이콘 + 선택적 레이블로 구성
- 활성 항목은 인디케이터(pill 형태)로 표시
- 모든 최상위 목적지에서 항상 표시

#### 네비게이션 레일 (Navigation Rail)

화면 측면(좌측)에 위치하는 중간 크기 디바이스용 네비게이션.

- **목적지 수**: 3~7개
- **너비**: 80dp
- 상단에 FAB 배치 가능 (선택)
- 태블릿, 폴더블 디바이스에서 사용
- M3 Expressive에서는 접힌 상태(collapsed)와 펼친 상태(expanded) 전환 가능, 펼친 상태는 네비게이션 드로어를 대체

#### 네비게이션 드로어 (Navigation Drawer)

대형 화면에서 사용하는 사이드 패널 네비게이션.

- **너비**: 360dp (표준)
- 목적지 수 제한 없음 — 많은 섹션을 가진 앱에 적합
- 영구(permanent), 일시(modal), 접힘(dismissible) 3가지 유형
- 섹션 분리, 레이블, 배지 지원

**적응형 네비게이션 전략:**

| 화면 크기 | 컴포넌트 | 너비 기준 |
|----------|---------|----------|
| 소형 (폰) | Navigation Bar | < 600dp |
| 중형 (태블릿) | Navigation Rail | 600~1240dp |
| 대형 (데스크톱) | Navigation Drawer | > 1240dp |

> **출처:** [Material Design 3 — Navigation Rail](https://m3.material.io/components/navigation-rail/guidelines)
> **출처:** [Material Design 3 — Navigation Drawer](https://m3.material.io/components/navigation-drawer/specs)
> **출처:** [Material Design 3 — Navigation Bar](https://m3.material.io/components/navigation-bar/overview)

### 카드 (Cards)

단일 주제에 대한 콘텐츠와 액션을 담는 표면 컨테이너.

**3가지 유형:**

| 유형 | 시각적 특징 | 용도 |
|------|-----------|------|
| **Elevated Card** | 그림자(elevation) 있음, 채움색 없음 | 기본 카드, 시각적 분리 필요 시 |
| **Filled Card** | 배경색 채움, 그림자 없음 | 다른 카드와 그룹핑 시 |
| **Outlined Card** | 테두리선, 그림자/채움 없음 | 가장 낮은 강조, 목록 아이템 |

**설계 원칙:**
- 카드 내부에 버튼, 아이콘 버튼 등 액션 배치 가능
- 전체 카드를 탭 가능한 단일 타겟으로 만들 수 있음
- 카드 내부 콘텐츠 영역: 헤더, 미디어, 텍스트, 액션
- 코너 반경: 12dp (medium)

> **출처:** [Material Design 3 — Cards](https://m3.material.io/components/cards/specs)

### 칩 (Chips)

사용자가 정보를 입력하거나, 선택하거나, 콘텐츠를 필터링하거나, 액션을 트리거하도록 돕는 컴팩트 요소.

**4가지 유형:**

| 유형 | 용도 | 예시 |
|------|------|------|
| **Assist Chip** | 스마트 제안, 바로가기 | "길 안내", "전화 걸기" |
| **Filter Chip** | 콘텐츠 필터링, 다중 선택 가능 | 카테고리 필터, 정렬 옵션 |
| **Input Chip** | 사용자 입력을 토큰화 | 이메일 수신자, 태그 |
| **Suggestion Chip** | 동적 제안 | 자동 완성, 추천 검색어 |

**공통 사양:**
- 높이: 32dp
- 코너 반경: 8dp (small)
- 아이콘(선택) + 레이블 텍스트 구성
- Filter/Input 칩은 선택 상태 표시(체크마크, 색상 변경)
- Input 칩은 삭제(x) 버튼 포함 가능

> **출처:** [Material Design 3 — Chips](https://m3.material.io/components/chips/specs)
