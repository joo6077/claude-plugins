---
title: 네비게이션 패턴
version: 0.2.0
last_updated: 2026-03-30
---

# 네비게이션 패턴

사용자가 앱 내에서 길을 잃지 않고 원하는 콘텐츠에 도달하도록 돕는 네비게이션 설계 원칙과 패턴을 정리한다.

---

## 원칙

### 1. 보이지 않으면 존재하지 않는다

네비게이션 항목을 숨기면 사용자의 발견율이 급격히 떨어진다. NNGroup은 "Out of sight is out of mind"라는 표현으로, 햄버거 메뉴 등 숨겨진 네비게이션이 카테고리 발견율을 크게 저하시킨다고 경고한다. 큰 화면에서는 반드시 네비게이션을 노출해야 한다.

> **출처:** [Menu-Design Checklist: 17 UX Guidelines — NNGroup](https://www.nngroup.com/articles/menu-design/)

### 2. 현재 위치를 항상 알려준다

사용자가 "지금 어디에 있는가?"라는 질문에 즉시 답할 수 있어야 한다. 메뉴의 활성 상태 표시, 브레드크럼, 페이지 제목 등 복수의 시각적 단서를 조합하여 현재 위치를 전달한다.

> **출처:** [Navigation: You Are Here — NNGroup](https://www.nngroup.com/articles/navigation-you-are-here/)

### 3. 익숙한 패턴을 우선한다

혁신적이거나 기발한 네비게이션 패턴은 사용자에게 혼란을 준다. NNGroup의 17가지 메뉴 가이드라인 중 17번째는 "사용자는 훌륭한 콘텐츠를 가진 익숙한 메뉴를 선호한다"고 명시한다. 입증된 이점이 없다면 표준 패턴을 따른다.

> **출처:** [Menu-Design Checklist: 17 UX Guidelines — NNGroup](https://www.nngroup.com/articles/menu-design/)

### 4. 검색은 네비게이션을 보완하지, 대체하지 않는다

NNGroup 연구에 따르면 "사용자는 좋은 검색 쿼리를 만드는 데 매우 서투르다." 네비게이션과 검색을 병행 제공해야 모든 사용자 유형을 지원할 수 있다.

> **출처:** [Basic Patterns for Mobile Navigation — NNGroup](https://www.nngroup.com/articles/mobile-navigation-patterns/)

---

## 네비게이션 구조

### Flat Hierarchy (플랫 구조)

모든 주요 섹션이 동일한 레벨에 존재하는 구조. 탭 바나 하단 네비게이션 바로 구현한다.

**적합한 경우:**
- 최상위 목적지가 3~5개 이하
- 섹션 간 빈번한 전환이 필요한 경우
- 각 섹션이 동등한 중요도를 가진 경우

**주의사항:**
- 5개를 초과하면 탭 바에 적절한 터치 타겟 크기를 유지하기 어렵다 (NNGroup)
- Apple HIG는 iPhone에서 3~5개, iPad에서는 그보다 약간 많은 탭을 권장한다

> **출처:** [Basic Patterns for Mobile Navigation — NNGroup](https://www.nngroup.com/articles/mobile-navigation-patterns/)
> **출처:** [Tab bars — Apple HIG](https://developer.apple.com/design/human-interface-guidelines/tab-bars)

### Deep Hierarchy (깊은 구조)

허브 페이지에서 하위 페이지로 점진적으로 내려가는 구조. 네비게이션 허브, 드로어, 메가 메뉴로 구현한다.

**적합한 경우:**
- 목적지가 5개 이상이며 콘텐츠가 풍부한 경우
- 사용자가 하나의 태스크를 완료하고 돌아오는 패턴
- 콘텐츠 소비 중심의 앱/사이트 (뉴스, 이커머스 등)

**주의사항:**
- 깊이가 3단계를 초과하면 사용자가 위치를 잃기 쉽다
- 캐스케이딩 메뉴는 2단계 이상에서 "물리적으로 조작하기 어렵다" — 메가 메뉴나 랜딩 페이지를 대안으로 사용한다 (NNGroup 가이드라인 #14)

> **출처:** [Menu-Design Checklist: 17 UX Guidelines — NNGroup](https://www.nngroup.com/articles/menu-design/)

---

## 탭/사이드바/드로어

### 탭 바 (Tab Bar / Bottom Navigation)

| 기준 | 권장 |
|------|------|
| 항목 수 | 3~5개 (iPhone), 최대 7개 (iPad/태블릿) |
| 위치 | iOS: 하단, Android: 하단 (M3 Navigation Bar) |
| 아이콘 | 반드시 텍스트 라벨과 함께 사용 |
| 스크롤 시 | 항상 화면에 고정 유지 |

**사용 시기:** 최상위 목적지 3~5개, 섹션 간 빈번한 전환이 필요할 때.

- Apple HIG: "탭 바는 엄격하게 네비게이션 용도로만 사용하며, 액션 수행에 사용하지 않는다."
- Material Design 3: Navigation Bar는 compact 화면에서 최대 5개 목적지를 지원한다.

> **출처:** [Tab bars — Apple HIG](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
> **출처:** [Navigation bar — Material Design 3](https://m3.material.io/components/navigation-bar/guidelines)

### 사이드바 (Sidebar / Navigation Rail)

| 기준 | 권장 |
|------|------|
| 항목 수 | 3~7개 (Navigation Rail), 그 이상은 Drawer |
| 위치 | 좌측 고정 |
| 화면 크기 | 태블릿·데스크톱 (medium~expanded) |

**사용 시기:** 태블릿/데스크톱에서 탭 바 대신 사용. iPad 앱에서는 Apple이 탭 바 대신 사이드바를 권장한다.

- Material Design 3: Navigation Rail은 medium 크기 화면에서 3~7개 목적지 + 선택적 FAB를 지원한다.
- Apple HIG: "iPadOS 앱에서는 탭 바 대신 사이드바를 고려하라. 사이드바는 많은 수의 항목을 표시할 수 있다."

> **출처:** [Navigation rail — Material Design 3](https://m3.material.io/components/navigation-rail/guidelines)
> **출처:** [Navigation and search — Apple HIG](https://developer.apple.com/design/human-interface-guidelines/navigation-and-search)

### 드로어 (Navigation Drawer)

| 기준 | 권장 |
|------|------|
| 항목 수 | 5개 이상 |
| 위치 | 좌측에서 슬라이드 |
| 화면 크기 | expanded (대형 화면)에서 상시 노출, compact에서는 오버레이 |

**사용 시기:** 목적지가 5개 이상이고 큰 화면에서 사용할 때. compact 화면에서 5개 미만이면 Navigation Bar를 대신 사용한다.

- Material Design 3: "compact 화면에서 5개 미만의 목적지에는 드로어를 사용하지 말라. Navigation Bar를 대신 사용하라."
- NNGroup: 햄버거 메뉴(드로어의 모바일 변형)는 "콘텐츠 중심의 브라우징 앱"에 가장 적합하다.

> **출처:** [Navigation drawer — Material Design 3](https://m3.material.io/components/navigation-drawer/guidelines)
> **출처:** [Basic Patterns for Mobile Navigation — NNGroup](https://www.nngroup.com/articles/mobile-navigation-patterns/)

### 선택 가이드 요약

```
목적지 수    compact(모바일)       medium(태블릿)        expanded(데스크톱)
─────────  ──────────────────  ──────────────────  ──────────────────
≤ 5        Navigation Bar      Navigation Rail     Navigation Rail/Drawer
> 5        Drawer(오버레이)     Navigation Rail     Drawer(상시 노출)
콘텐츠 내   Tabs                Tabs                Tabs
```

---

## 뎁스 관리

### 브레드크럼 (Breadcrumbs)

NNGroup의 사용자 테스트에서 브레드크럼은 "많은 이점이 있으며 단점은 발견되지 않았다"고 보고되었다. 특히 외부 링크를 통해 사이트에 진입한 사용자에게 효과적이다.

**NNGroup 11가지 브레드크럼 가이드라인 (핵심 요약):**

1. **보조 수단으로 사용** — 브레드크럼은 기본 네비게이션을 "보완하되 대체하지 않는다"
2. **히스토리가 아닌 계층 구조를 표시** — 세션 히스토리가 아닌 사이트의 구조적 계층을 보여준다
3. **현재 페이지를 마지막 항목으로 포함** — 단, 클릭 불가능하게 하고 시각적으로 구분한다
4. **실제 페이지만 링크** — URL이 있는 페이지만 포함하고, 페이지 없는 카테고리 라벨은 제외한다
5. **플랫/선형 사이트에서는 생략** — 계층이 1~2단계뿐인 경우 불필요하다
6. **모바일에서 줄바꿈 방지** — "이미 좁은 모바일 화면에서 소중한 공간"을 낭비하지 않도록 한다
7. **모바일 터치 타겟 최소 1cm x 1cm** — 터치스크린에서 적절한 상호작용을 위해
8. **모바일에서 축약 표시** — 마지막 1~2단계만 표시하여 공간을 절약한다

> **출처:** [Breadcrumbs: 11 Design Guidelines for Desktop and Mobile — NNGroup](https://www.nngroup.com/articles/breadcrumbs/)
> **출처:** [Breadcrumb Navigation Increasingly Useful — NNGroup](https://www.nngroup.com/articles/breadcrumb-navigation-useful/)

### 뒤로 가기 (Back Navigation)

**플랫폼별 패턴:**
- **iOS:** 좌측 상단 Back 버튼 + 엣지 스와이프 제스처. 이전 화면의 제목을 Back 버튼 라벨로 표시한다.
- **Android:** 시스템 Back 버튼/제스처. 예측 가능한 Back 동작(Predictive Back)을 지원하여 사용자가 뒤로 갈 곳을 미리 볼 수 있다.
- **웹:** 브라우저 뒤로 가기 버튼이 히스토리 기반으로 동작한다. SPA에서는 라우터 히스토리를 올바르게 관리해야 한다.

**핵심 원칙:**
- 뒤로 가기는 항상 예측 가능해야 한다 — 사용자가 어디로 돌아갈지 알 수 있어야 한다
- 모달/다이얼로그에서 뒤로 가기는 모달을 닫아야 하며, 이전 페이지로 이동하면 안 된다
- 다단계 플로우(회원가입, 결제 등)에서는 단계 표시기(stepper)와 함께 뒤로 가기를 제공하여 진행 상황을 명확히 한다

> **출처:** [Navigation and search — Apple HIG](https://developer.apple.com/design/human-interface-guidelines/navigation-and-search)

### 뎁스 제한 권장

| 뎁스 | 사용자 경험 | 권장 |
|------|------------|------|
| 1~2단계 | 쉽고 직관적 | 대부분의 앱에 적합 |
| 3단계 | 관리 가능하지만 브레드크럼 필요 | 콘텐츠 앱, 이커머스 |
| 4단계 이상 | 길 잃기 쉬움, 포고스틱 발생 | 가능한 피하고, 로컬 네비게이션으로 보완 |

NNGroup은 관련 콘텐츠를 위한 로컬 네비게이션(가이드라인 #6)을 제공하여 사용자가 계층을 오르내리는 "포고스틱" 행동을 방지하라고 권장한다.

> **출처:** [Menu-Design Checklist: 17 UX Guidelines — NNGroup](https://www.nngroup.com/articles/menu-design/)
