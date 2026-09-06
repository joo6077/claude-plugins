---
title: 스페이싱 & 레이아웃
version: 0.3.0
last_updated: 2026-03-30
---

# 스페이싱 & 레이아웃

간격 체계, 그리드 시스템, 네거티브 스페이스, 콘텐츠 밀도 전략, 터치 타겟 수치를 정리한다.

---

## 원칙

### 1. 일관된 간격 체계 사용

모든 간격 값은 **기본 단위의 배수**로 제한한다. 13px vs 15px를 고민할 필요 없이, 8px 또는 16px 중 선택하면 된다. 선택지를 제한해야 디자이너가 계층 구조와 인터랙션에 집중할 수 있다.

> **출처:** [The 8pt Grid System — Rejuvenate Digital](https://www.rejuvenate.digital/news/designing-rhythm-power-8pt-grid-ui-design)

### 2. 여백(Whitespace)은 디자인 도구다

여백은 "비어있는 공간"이 아니라 정보 계층을 구성하는 능동적 도구다. NNGroup 연구에서 미학적으로 우수한 디자인은 공통적으로 충분한 여백, 일관된 타이포그래피, 명확한 계층을 보유했다.

**네거티브 스페이스(Negative Space)의 두 가지 유형:**

| 유형 | 설명 | 예시 |
|------|------|------|
| **마이크로 여백** | 요소 내부/사이의 작은 공간 (아이콘-텍스트 간격, 줄 간격) | 버튼 패딩 12px, 리스트 아이템 간 8px |
| **매크로 여백** | 콘텐츠 블록 간 큰 공간 (섹션 간격, 페이지 마진) | 섹션 간 64px, 히어로 상하 80px |

마이크로 여백이 부족하면 "답답한" UI, 매크로 여백이 부족하면 "복잡한" UI가 된다. 둘 다 부족하면 사용자는 1.5배 더 많은 시간을 써서 정보를 찾는다(NNGroup 아이트래킹).

> **출처:** [Why Does a Design Look Good? — Nielsen Norman Group](https://www.nngroup.com/articles/why-does-design-look-good/)

### 3. 내부 간격 ≤ 외부 간격 (근접성 원칙)

관련 요소 간 내부 간격(padding)은 비관련 요소 간 외부 간격(margin)보다 작아야 한다. 게슈탈트 근접성 원칙: 가까이 있는 요소는 관련된 것으로 인식된다.

**안티패턴:** 카드 내부 패딩 24px인데 카드 간 간격도 24px이면, 카드 경계가 모호해진다. 카드 간 간격을 32px 이상으로 벌려야 그룹이 구분된다.

> **출처:** [Spacing Best Practices — Cieden](https://cieden.com/book/sub-atomic/spacing/spacing-best-practices)

### 4. 그리드 기반 정렬

그리드는 레이아웃 구조를 제공할 뿐 아니라 사용자의 **스캔 용이성**을 향상시킨다. 정렬이 무너진 UI는 사용자에게 "대충 만든" 인상을 준다 — 이는 브랜드 신뢰도에 직접 영향한다.

> **출처:** [Using Grids in Interface Designs — Nielsen Norman Group](https://www.nngroup.com/articles/using-grids-in-interface-designs/)

---

## 스페이싱 스케일

### 4px 기본 단위 (하프 그리드)

아이콘 내부 여백, 텍스트와 아이콘 사이 미세 간격 등 **세밀한 조정**에 4px 단위를 사용한다.

### 8px 기본 단위 (풀 그리드)

대부분의 디바이스 화면 크기는 8의 배수이므로, 그리드 구성 요소 값을 8의 배수로 유지하면 다양한 디바이스와 픽셀 밀도에서 **일관된 스케일링과 구현**이 가능하다.

> **출처:** [Space, Grids, and Layouts — designsystems.com](https://www.designsystems.com/space-grids-and-layouts/)

### 스페이싱 토큰 테이블

| 토큰        | 값     | 용도 예시                      |
| ----------- | ------ | ------------------------------ |
| `space-0`   | 0px    | 요소 간 간격 없음              |
| `space-1`   | 4px    | 아이콘-텍스트 미세 간격        |
| `space-2`   | 8px    | 인라인 요소 간 기본 간격       |
| `space-3`   | 12px   | 컴팩트 리스트 아이템 패딩      |
| `space-4`   | 16px   | 카드 내부 패딩, 섹션 간 간격   |
| `space-5`   | 24px   | 섹션 타이틀과 콘텐츠 사이      |
| `space-6`   | 32px   | 주요 섹션 간 구분              |
| `space-7`   | 40px   | 페이지 상단/하단 여백          |
| `space-8`   | 48px   | 대형 카드 간 간격              |
| `space-9`   | 64px   | 페이지 레벨 구분               |
| `space-10`  | 80px   | 히어로 섹션 상하 여백          |

Material Design에서 마진과 거터는 **8, 16, 24, 40dp** 중 하나를 사용한다. 마진과 컬럼은 **8dp 정사각형 베이스라인 그리드**를 따른다.

> **출처:** [Applying Layout — Material Design 3](https://m3.material.io/foundations/layout/applying-layout)

---

## 그리드 시스템

### Material Design 3 윈도우 크기 클래스

M3는 M2의 반응형 그리드 대신 **윈도우 크기 클래스(Window Size Class)**와 **정규 레이아웃(Canonical Layout)**을 활용하는 방식으로 전환했다.

| 크기 클래스 | 브레이크포인트  | 컬럼 수 | 마진      |
| ----------- | --------------- | ------- | --------- |
| Compact     | < 600dp         | 4       | 16dp      |
| Medium      | 600dp ~ 839dp   | 8       | 24dp      |
| Expanded    | 840dp ~ 1199dp  | 12      | 24dp      |
| Large       | 1200dp ~ 1599dp | 12      | 24 ~ 40dp |
| Extra-large | ≥ 1600dp        | 12      | 40dp      |

> **출처:** [Responsive Layout Grid — Material Design](https://mdc.almoamen.net/layout/responsive-layout-grid)
> **출처:** [Design an Adaptive Layout with Material Design — Google Codelabs](https://codelabs.developers.google.com/codelabs/adaptive-material-guidance)

### 컬럼 너비

컬럼 너비는 고정값이 아닌 **퍼센트(%)** 로 정의하여, 콘텐츠가 모든 화면 크기에 유연하게 적응한다.

### Apple HIG 레이아웃 마진

| 디바이스     | 최대 콘텐츠 너비 | 수평 마진         |
| ------------ | ---------------- | ----------------- |
| iPhone       | 화면 87.5%       | 좌우 각 약 6.25%  |
| iPad         | 692px            | 자동 센터링       |
| Desktop      | 980px            | 자동 센터링       |

> **출처:** [Layout — Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/layout)

---

## 터치 타겟

### Apple HIG: 최소 44 x 44pt

Apple은 모든 탭 가능한 요소(버튼, 링크, 테이블 행 등)에 **최소 44 x 44 포인트**의 터치 영역을 요구한다. 시각적 요소가 더 작게 보이더라도, 탭 가능 영역은 반드시 이 최솟값을 충족해야 한다. 연구에 따르면 작은 요소는 **25% 이상의 탭 오류율**을 유발한다.

> **출처:** [Apple Human Interface Guidelines — Touch Target](https://developer.apple.com/design/human-interface-guidelines/accessibility#Buttons-and-controls)

### Material Design: 최소 48 x 48dp

Material Design은 터치 타겟으로 **48 x 48dp** (약 9mm)를 권장한다. 밀집 레이아웃(데스크톱)에서는 **40 x 40dp**까지 축소할 수 있다.

> **출처:** [Accessibility — Material Design 3](https://m3.material.io/foundations/designing/structure)

### WCAG 2.5.8: 최소 24 x 24 CSS 픽셀 (Level AA)

WCAG 2.2에서 도입된 **성공 기준 2.5.8 Target Size (Minimum)**은 포인터 입력 대상의 크기가 최소 **24 x 24 CSS 픽셀**이어야 한다고 규정한다. 이는 ADA, Section 508, 유럽 접근성법(EAA, 2025년 6월 시행)에서 법적으로 요구된다.

**5가지 예외 조건:**

1. **간격(Spacing):** 24 CSS 픽셀 지름의 원을 각 타겟 바운딩 박스 중앙에 그렸을 때, 다른 타겟이나 인접 타겟의 원과 겹치지 않으면 통과
2. **동등 대안(Equivalent):** 같은 페이지에 기준을 충족하는 동일 기능의 다른 컨트롤이 있는 경우
3. **인라인(Inline):** 문장 내부에 있거나 텍스트 line-height에 의해 크기가 제한되는 경우
4. **사용자 에이전트 컨트롤(User Agent):** 브라우저 기본 렌더링 컨트롤 (예: 날짜 선택기)
5. **필수적(Essential):** 타겟 위치가 전달하는 정보에 본질적인 경우 (예: 지도 핀)

> **출처:** [Understanding SC 2.5.8 — W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

### WCAG 2.5.5: 최소 44 x 44 CSS 픽셀 (Level AAA)

더 엄격한 기준인 **2.5.5 Target Size (Enhanced)**는 중요한 컨트롤에 대해 **44 x 44 CSS 픽셀**을 요구한다.

> **출처:** [Understanding SC 2.5.5 — W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)

### 물리적 근거

MIT Touch Lab 연구에 따르면, 성인 손가락 끝의 평균 너비는 **16~20mm**이다. 운동 장애가 있는 사용자는 작은 타겟에서 오류율이 **최대 75% 증가**한다.

> **출처:** [Touch Target Sizes — LukeW](https://www.lukew.com/ff/entry.asp?1085=)

### 플랫폼별 터치 타겟 요약

| 플랫폼           | 최소 터치 타겟 | 권장 터치 타겟 | 단위       |
| ---------------- | -------------- | -------------- | ---------- |
| Apple (iOS)      | 44 x 44        | 44 x 44        | pt (point) |
| Material (Android)| 48 x 48       | 48 x 48        | dp         |
| WCAG 2.2 AA      | 24 x 24        | —              | CSS px     |
| WCAG 2.2 AAA     | 44 x 44        | —              | CSS px     |
| Web (일반)       | 24 x 24        | 44 x 44        | CSS px     |

---

## 콘텐츠 밀도 (Content Density)

### 밀도 수준 정의

콘텐츠 밀도는 단위 면적당 정보량이다. 동일한 데이터를 밀도에 따라 완전히 다르게 표시할 수 있다.

| 밀도 | 행 높이 (리스트) | 패딩 | 적합한 맥락 | 사용자 행동 |
|------|---------------|------|-----------|-----------|
| **Compact** | 32~40dp | 4~8dp | 데이터 테이블, 개발 도구, 전문가용 대시보드 | 빠른 스캔, 대량 데이터 비교 |
| **Default** | 48~56dp | 12~16dp | 일반 앱, 이커머스, 콘텐츠 피드 | 편안한 읽기, 탐색 |
| **Comfortable** | 64~72dp | 16~24dp | 온보딩, 설정, 접근성 우선 | 여유로운 터치, 큰 텍스트 |

Material Design 3는 `dense`, `default`, `comfortable` 세 밀도를 공식 지원한다. Gmail이 대표 사례로, 사용자가 밀도를 직접 선택할 수 있다.

> **출처:** [Material Design 3 — Applying Layout](https://m3.material.io/foundations/layout/applying-layout)

### 밀도 결정 기준

```
사용자가 한 화면에서 10개 이상의 항목을 비교해야 하는가?
├─ Yes → Compact 기본, Default 옵션 제공
└─ No
    ├─ 터치 디바이스가 주 입력인가?
    │   ├─ Yes → Default 기본 (터치 타겟 48dp 보장)
    │   └─ No (마우스/키보드) → Compact도 허용
    └─ 접근성이 최우선인가?
        └─ Yes → Comfortable 기본
```

### 실전 레이아웃 감사 (Layout Audit) 방법

기존 화면의 간격 문제를 진단하는 체계적 방법:

**1단계: 스크린샷 캡처 + 그리드 오버레이**
- Figma에서 8px 그리드를 오버레이하고, 그리드에 정렬되지 않는 요소를 표시한다

**2단계: 간격 값 수집**
- 화면 내 모든 간격 값을 추출한다. 5개 이상의 서로 다른 간격 값이 나오면 체계가 무너진 것이다
- 안티패턴: 7px, 13px, 15px, 18px, 22px 같은 임의의 값 혼재

**3단계: 근접성 검증**
- 관련 요소 간 간격 < 비관련 요소 간 간격인지 확인
- 위반 사례: 폼 라벨-필드 간격 16px, 필드-필드 간격 12px → 라벨이 아래 필드에 더 가까워 보임

**4단계: 터치 타겟 검증**
- 모든 인터랙티브 요소에 48dp(또는 44pt) 히트 영역이 있는지 확인
- 인접 터치 타겟이 겹치지 않는지 확인

> **출처:** [Nathan Curtis — Space in Design Systems](https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62)
> **출처:** [Cieden — Spacing Best Practices](https://cieden.com/book/sub-atomic/spacing/spacing-best-practices)
