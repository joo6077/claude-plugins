---
title: 아이코노그래피
version: 0.2.0
last_updated: 2026-03-30
---

# 아이코노그래피

아이콘의 크기, 스타일, 접근성을 체계적으로 관리하여 일관되고 명확한 시각 언어를 구축하는 원칙과 수치를 정리한다.

---

## 원칙

### 1. 명확성 (Clarity)

아이콘은 최소한의 시각 요소로 의미를 **즉각적으로 전달**해야 한다. 복잡한 디테일은 작은 크기에서 뭉개지므로, 핵심 형태만 남기고 단순화한다. Material Symbols는 수천 개의 아이콘을 7단계 굵기와 3가지 스타일로 제공하며, 광학 크기(optical size) 축을 통해 크기별로 획 두께를 자동 최적화한다.

> **출처:** [Material Symbols Guide — Google Fonts](https://developers.google.com/fonts/docs/material_symbols)

### 2. 일관성 (Consistency)

같은 제품 내 모든 아이콘은 **동일한 스타일, 굵기, 크기 체계**를 사용해야 한다. Outlined와 Filled를 혼용하면 시각적 노이즈가 발생한다. 아이콘 그리드는 일관성을 위해 개발된 것으로, 그래픽 요소의 위치에 대한 **명확한 규칙 세트**를 제공하여 유연하면서도 일관된 시스템을 구축한다.

> **출처:** [Icons — Material Design 1](https://m1.material.io/style/icons.html)

### 3. 보편성 (Universality)

아이콘은 문화적 맥락에 관계없이 보편적으로 이해되어야 한다. 텍스트 레이블과 함께 사용하는 것이 인식률을 크게 높인다. 아이콘만 단독으로 사용할 경우, 사용자 테스트를 통해 의미 전달을 검증해야 한다.

> **출처:** [Icon Usability — Nielsen Norman Group](https://www.nngroup.com/articles/icon-usability/)

### 4. 접근성 (Accessibility)

장식적 아이콘에는 `aria-hidden="true"`를, 의미를 전달하는 아이콘에는 적절한 `aria-label`을 제공한다. 아이콘의 터치 타겟은 시각적 크기와 별개로 플랫폼 최소 기준을 충족해야 한다.

> **출처:** [WCAG 2.2 — Understanding SC 1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

---

## 크기 체계

### Material Design 기본 크기

시스템 아이콘의 기본 크기는 **24dp**이며, 터치 타겟은 **48dp**이다.

| 용도               | 아이콘 크기 | 터치 타겟 | 비고                           |
| ------------------ | ----------- | --------- | ------------------------------ |
| 밀집 레이아웃 (데스크톱) | 20dp   | 40dp      | 데스크톱 밀집 UI 전용          |
| **시스템 아이콘 (기본)** | **24dp** | **48dp** | 대부분의 UI 요소에 사용        |
| 강조 아이콘        | 40dp        | 48dp      | 빈 상태, 온보딩 일러스트       |
| 대형 디스플레이    | 48dp        | 48dp+     | 내비게이션 레일, 대시보드 타일  |

> **출처:** [Icons — Material Design 3](https://m3.material.io/styles/icons/designing-icons)

### Material Symbols 광학 크기 (Optical Size)

전통적으로 아이콘은 24dp 소스 벡터에서 리사이즈하지만, 광학 크기 축을 사용하면 **크기가 변해도 획 두께(stroke weight)를 일정하게 유지**할 수 있다.

| 광학 크기 | 용도                     | 특징                           |
| --------- | ------------------------ | ------------------------------ |
| 20dp      | 밀집 UI, 작은 공간       | 더 굵은 획으로 가독성 유지     |
| 24dp      | 기본 시스템 아이콘       | 표준 획 두께                   |
| 40dp      | 중형 강조 아이콘         | 약간 가는 획으로 우아한 느낌   |
| 48dp      | 대형 디스플레이 아이콘   | 가장 가는 획, 디테일 증가      |

> **출처:** [Material Symbols Guide — Google Fonts](https://developers.google.com/fonts/docs/material_symbols)

### Apple SF Symbols 크기 스케일

SF Symbols는 San Francisco 시스템 폰트의 cap-height에 상대적인 **3단계 스케일**을 제공한다. 동일한 포인트 크기를 유지하면서 스케일만 변경하여, 인접 텍스트와의 무게 매칭을 깨뜨리지 않는다.

| 스케일   | 크기 비율           | 용도                             |
| -------- | ------------------- | -------------------------------- |
| Small    | 기본 대비 약 -20%   | 보조 정보, 밀집 UI               |
| Medium   | 기본 (default)       | 대부분의 UI 요소                 |
| Large    | 기본 대비 약 +30%   | 내비게이션 바, 탭 바, 강조 영역  |

SF Symbols는 모든 스케일과 무게에서 San Francisco의 cap-height에 자동으로 **수직 중앙 정렬**된다.

> **출처:** [SF Symbols — Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

### CSS 기본 구현

```css
/* Material Symbols 기본 설정 */
.material-symbols-outlined {
  font-size: 24px;           /* 기본 크기 */
  font-variation-settings:
    'FILL' 0,                /* 0: outlined, 1: filled */
    'wght' 400,              /* 100~700 */
    'GRAD' 0,                /* -25~200 */
    'opsz' 24;               /* 20, 24, 40, 48 */
}
```

> **출처:** [Material Symbols Guide — Google Fonts](https://developers.google.com/fonts/docs/material_symbols)

---

## 스타일 일관성

### Outlined vs Filled 사용 규칙

Material Design에서 아이콘 스타일은 **fill 축** (0 또는 1)으로 제어한다.

| 스타일     | fill 값 | 사용 맥락                                    |
| ---------- | ------- | -------------------------------------------- |
| **Outlined** | 0     | 비선택 상태, 기본 UI, 정보 전달 아이콘       |
| **Filled** | 1       | 선택/활성 상태, 강조, 내비게이션 선택된 탭   |

**핵심 규칙:** 같은 화면 내에서 Outlined와 Filled를 **상태 표현 용도로만** 혼용한다. 예를 들어 바텀 내비게이션에서 선택된 탭은 Filled, 비선택 탭은 Outlined로 표시한다. 임의로 섞어 쓰면 시각적 계층이 무너진다.

> **출처:** [Material Symbols Guide — Google Fonts](https://developers.google.com/fonts/docs/material_symbols)

### Weight (굵기) 매칭

아이콘의 굵기는 인접 텍스트의 폰트 무게와 **시각적으로 일치**시켜야 한다.

| 텍스트 무게   | 아이콘 Weight 값 | 비고                    |
| ------------- | ---------------- | ----------------------- |
| Light (300)   | 200~300          | 얇은 텍스트에 맞춤      |
| Regular (400) | 400              | 기본 조합               |
| Medium (500)  | 400~500          | 중간 강조               |
| Bold (700)    | 600~700          | 강조 텍스트에 맞춤      |

> **출처:** [Material Symbols Guide — Google Fonts](https://developers.google.com/fonts/docs/material_symbols)

### Grade (등급) 활용

Grade는 아이콘의 굵기를 미세하게 조정하되, 아이콘의 전체 크기를 변경하지 않는다.

| Grade 값 | 용도                                              |
| --------- | ------------------------------------------------ |
| -25       | 저강조 — 어두운 배경에서 눈부심 감소             |
| 0         | 기본값                                           |
| 200       | 고강조 — 특정 아이콘에 주의를 끌 때              |

> **출처:** [Material Symbols Guide — Google Fonts](https://developers.google.com/fonts/docs/material_symbols)

### 아이콘 그리드와 키라인

Material Design 아이콘은 **24 x 24dp 그리드** 위에 디자인된다. 키라인 형태(keyline shape)가 그리드의 기초이며, 다음 기본 형태에 대한 사전 정의 표준이 있다:

| 키라인 형태     | 크기           | 용도                    |
| --------------- | -------------- | ----------------------- |
| 원 (Circle)     | 20dp 지름      | 원형 아이콘             |
| 정사각형 (Square) | 18 x 18dp   | 정사각형 아이콘         |
| 직사각형 (세로) | 16 x 20dp     | 세로로 긴 아이콘        |
| 직사각형 (가로) | 20 x 16dp     | 가로로 긴 아이콘        |

아이콘 콘텐츠는 **라이브 영역(live area)** 안에 유지해야 하며, 이 안전 영역 밖의 그래픽은 표시 시 잘릴 수 있다.

> **출처:** [Icons — Material Design 1](https://m1.material.io/style/icons.html)

### 아이콘 터치 타겟

아이콘이 인터랙티브(탭 가능)한 경우, 시각적 크기와 별개로 **터치 타겟 최소 기준**을 반드시 충족해야 한다.

| 플랫폼           | 아이콘 크기 | 최소 터치 타겟 | 패딩               |
| ---------------- | ----------- | -------------- | ------------------- |
| Material (Android)| 24dp       | 48dp           | 아이콘 주변 12dp    |
| Apple (iOS)      | ~22pt       | 44 x 44pt      | 아이콘 주변 ~11pt   |
| WCAG 2.2 AA      | —           | 24 x 24 CSS px | 인접 타겟과 비중첩  |

24dp 아이콘에 48dp 터치 타겟을 적용하면, 아이콘 주변에 **12dp의 투명 패딩**이 추가되어 탭 가능 영역이 확장된다. 시각적으로는 24dp로 보이지만 실제 탭 영역은 48dp이다.

> **출처:** [Accessibility — Material Design 3](https://m3.material.io/foundations/accessible-design/accessibility-basics)
> **출처:** [Understanding SC 2.5.8 — W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

### 체크리스트: 아이콘 일관성 검증

- [ ] 한 화면 내 모든 아이콘이 동일한 스타일(Outlined 또는 Filled)을 사용하는가?
- [ ] 선택/비선택 상태만 fill 축으로 구분하는가?
- [ ] 아이콘 weight가 인접 텍스트 폰트 무게와 시각적으로 매칭되는가?
- [ ] 광학 크기(opsz)가 표시 크기에 맞게 설정되어 있는가?
- [ ] 인터랙티브 아이콘의 터치 타겟이 플랫폼 최소 기준을 충족하는가?
- [ ] 의미를 전달하는 아이콘에 `aria-label`이 제공되는가?
- [ ] 장식적 아이콘에 `aria-hidden="true"`가 설정되는가?
