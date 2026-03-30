---
title: 타이포그래피
version: 0.2.0
last_updated: 2026-03-30
---

# 타이포그래피

디자인 시스템의 타이포그래피 기초 원칙, 스케일 체계, 가독성, 반응형 접근 방식을 정리한다.

---

## 원칙

### 1. 계층 구조(Visual Hierarchy)를 명확히 한다

텍스트의 크기, 굵기, 색상을 조합하여 정보의 중요도를 시각적으로 전달한다. 제목-본문-캡션의 구분이 즉시 인지되어야 한다. Material Design 3는 Display, Headline, Title, Body, Label 5단계 역할(role)로 계층을 체계화한다.

> **출처:** [Material Design 3 — Type Scale Tokens](https://m3.material.io/styles/typography/type-scale-tokens)

### 2. 시스템 서체를 우선 사용한다

플랫폼 기본 서체(iOS: SF Pro/NY, Android: Roboto Flex, Web: system-ui)를 우선 채택하면 렌더링 성능과 일관성을 확보할 수 있다. Apple HIG는 "가능한 한 내장 텍스트 스타일을 사용하라"고 권고한다.

> **출처:** [Apple HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

### 3. Dynamic Type / 사용자 설정을 존중한다

사용자가 선택한 텍스트 크기를 반영해야 한다. iOS의 Dynamic Type, Android의 sp 단위, 웹의 rem 단위를 사용하면 시스템 글꼴 크기 설정이 자동 반영된다. WCAG 1.4.4는 텍스트를 200%까지 확대할 수 있어야 한다고 요구한다.

> **출처:** [WCAG 1.4.4 Resize Text](https://www.w3.org/WAI/WCAG21/Understanding/resize-text.html)

### 4. 글꼴 크기는 충분히 크게 설정한다

NNGroup 연구에 따르면 빠르게 인지해야 하는 텍스트(glanceable text)일수록 더 큰 크기가 필요하며, 좁은(condensed) 서체는 일반 너비 대비 11.2% 더 긴 인지 시간이 소요된다. 모바일 본문은 최소 16px(1rem), 데스크톱 본문은 16-18px를 권장한다.

> **출처:** [NNGroup — Typography for Glanceable Reading: Bigger Is Better](https://www.nngroup.com/articles/glanceable-fonts/)

---

## 스케일 체계

### Material Design 3 Type Scale

MD3는 5가지 역할(role) x 3가지 크기(Large/Medium/Small) = 15단계 스케일을 정의한다. 2024년 업데이트로 Display XL이 추가되었다.

| 역할 | 크기 | Font Size | Line Height | Weight | 용도 |
|------|------|-----------|-------------|--------|------|
| **Display XL** | - | 88px | 96px | 475 | 히어로 배너 |
| **Display L** | Large | 57px | 64px | 475 | 랜딩 페이지 주요 수치 |
| **Display M** | Medium | 45px | 52px | 475 | 대형 텍스트 |
| **Display S** | Small | 36px | 44px | 475 | 강조 텍스트 |
| **Headline L** | Large | 32px | 40px | 475 | 페이지 제목 |
| **Headline M** | Medium | 28px | 36px | 475 | 섹션 제목 |
| **Headline S** | Small | 24px | 32px | 475 | 카드 제목 |
| **Title L** | Large | 22px | 30px | 400 | 앱바, 다이얼로그 제목 |
| **Title M** | Medium | 16px | 24px | 500 | 리스트 아이템 제목 |
| **Title S** | Small | 14px | 20px | 500 | 탭, 칩 라벨 |
| **Body L** | Large | 16px | 24px | 400 | 장문 본문 |
| **Body M** | Medium | 14px | 20px | 400 | 일반 본문 |
| **Body S** | Small | 12px | 16px | 400 | 보조 설명 |
| **Label L** | Large | 14px | 20px | 500 | 버튼 라벨 |
| **Label M** | Medium | 12px | 16px | 500 | 내비게이션 라벨 |
| **Label S** | Small | 11px | 16px | 500 | 배지, 최소 텍스트 |

> **출처:** [Material Design 3 — Type Scale Tokens](https://m3.material.io/styles/typography/type-scale-tokens)

### Apple HIG Type Styles (iOS)

Apple은 의미론적(semantic) 텍스트 스타일을 정의하며, Dynamic Type에 의해 사용자 설정에 따라 크기가 조정된다. 아래는 기본(Default) 크기이다.

| 스타일 | Size (pt) | Weight | 비고 |
|--------|-----------|--------|------|
| **Large Title** | 34 | Regular | 최상위 네비게이션 |
| **Title 1** | 28 | Regular | 주요 제목 |
| **Title 2** | 22 | Regular | 보조 제목 |
| **Title 3** | 20 | Regular | 하위 제목 |
| **Headline** | 17 | Semibold | 강조 본문 |
| **Body** | 17 | Regular | 기본 본문 |
| **Callout** | 16 | Regular | 부가 설명 |
| **Subheadline** | 15 | Regular | 부제목 |
| **Footnote** | 13 | Regular | 각주 |
| **Caption 1** | 12 | Regular | 캡션 |
| **Caption 2** | 11 | Regular | 최소 캡션 |

- SF Pro와 New York(NY) 두 서체를 혼용하여 대비를 줄 수 있다.
- Accessibility 카테고리에서 최대 AX5까지 확대 가능하다.

> **출처:** [Apple HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
> **출처:** [Learn UI Design — iOS Font Size Guidelines](https://www.learnui.design/blog/ios-font-size-guidelines.html)

---

## 가독성

### 줄 높이(Line Height)

본문 텍스트의 줄 높이는 **1.4~1.6em**이 최적이다. 줄 길이가 길어지면 줄 높이도 함께 증가시켜야 한다. 2004년 University of Reading 연구에 따르면 긴 줄에서 줄 간격이 부족하면 다음 줄을 찾는 데 실패(line-tracking error)가 발생한다.

| 텍스트 유형 | 권장 줄 높이 |
|------------|-------------|
| 본문 (Body) | 1.4~1.6em (MD3: 1.5em = 24px/16px) |
| 제목 (Heading) | 1.1~1.3em |
| 작은 텍스트 (Caption) | 1.3~1.4em |

> **출처:** [Smashing Magazine — Balancing Line Length and Font Size](https://www.smashingmagazine.com/2014/09/balancing-line-length-font-size-responsive-web-design/)

### 줄 길이(Line Length)

최적 줄 길이는 **50~75자**(공백 포함)이며, **66자**가 이상적인 기준점으로 자주 인용된다. Baymard Institute 연구에서도 이를 확인한다. CSS에서 `max-width: 65ch` 정도로 제한할 수 있다.

- 75자 초과: 집중력 저하, 줄 추적 실패, 재독(re-reading) 발생
- 45자 미만: 잦은 줄바꿈으로 읽기 리듬 방해

> **출처:** [Baymard Institute — Readability: The Optimal Line Length](https://baymard.com/blog/line-length-readability)

### 텍스트 대비(Contrast)

WCAG 2.1 기준으로 텍스트와 배경 간 최소 대비를 지켜야 한다.

| 수준 | 일반 텍스트 | 대형 텍스트 (18pt 이상 또는 14pt Bold) |
|------|-----------|--------------------------------------|
| **AA** (최소) | **4.5:1** | **3:1** |
| **AAA** (향상) | **7:1** | **4.5:1** |

- 대형 텍스트 기준: 18pt(24px) 이상 또는 14pt(약 18.66px) Bold 이상
- 비활성(disabled) UI 요소와 장식 텍스트는 대비 요구사항에서 제외
- 4.499:1은 4.5:1 기준을 **충족하지 못한다** (반올림 불가)

> **출처:** [WCAG 1.4.3 — Contrast Minimum](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

### 추가 가독성 팁

- **자간(Letter Spacing)**: 본문은 기본값 유지, Label S/M 같은 소형 텍스트에서만 0.1px 추가
- **단어 간격(Word Spacing)**: 기본값 유지. WCAG 1.4.12는 단어 간격을 0.16em까지 늘려도 콘텐츠가 유실되지 않아야 한다고 요구
- **텍스트 정렬**: 본문은 좌측 정렬(LTR), 양쪽 정렬(justify)은 단어 간격이 불규칙해져 가독성을 해침

> **출처:** [WCAG 1.4.12 — Text Spacing](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html)

---

## 반응형 타이포그래피

### 접근 방식 비교

| 방식 | 설명 | 장점 | 단점 |
|------|------|------|------|
| **Breakpoint 기반** | `@media` 쿼리로 폰트 크기 변경 | 예측 가능, 디버깅 용이 | 계단식 전환, 중간 뷰포트 대응 부족 |
| **Fluid (clamp)** | `clamp(min, preferred, max)` | 부드러운 스케일링, 코드 간결 | 줌 200% 접근성 검증 필요 |
| **Container Query** | 부모 컨테이너 크기 기준 | 컴포넌트 독립적 | 브라우저 지원 확인 필요 |

### CSS clamp()를 이용한 Fluid Typography

`clamp()` 함수는 최솟값, 선호값, 최댓값 세 인자를 받아 뷰포트에 따라 부드럽게 전환한다.

```css
/* 기본 문법 */
font-size: clamp(최솟값, 선호값, 최댓값);

/* 실전 예시: 제목 텍스트 */
h1 {
  font-size: clamp(2rem, 4vw + 1rem, 3.25rem);
  /* 최소 32px, 최대 52px, 뷰포트에 비례하여 변화 */
}

/* 본문 텍스트 */
body {
  font-size: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  /* 최소 16px, 최대 18px, 미세 조정 */
}
```

#### 계산 공식

600px 뷰포트에서 36px, 1400px 뷰포트에서 52px를 원할 때:

```
뷰포트 계수(v) = 100 * (52 - 36) / (1400 - 600) = 2vw
상대 기준(r)   = (600*52 - 1400*36) / (600 - 1400) = 24px = 1.5rem
결과: clamp(2.25rem, 2vw + 1.5rem, 3.25rem)
```

> **출처:** [Smashing Magazine — Modern Fluid Typography Using CSS Clamp](https://www.smashingmagazine.com/2022/01/modern-fluid-typography-css-clamp/)

### 접근성 주의사항

- **반드시 rem 단위를 사용한다**: px 단위는 브라우저 글꼴 크기 설정을 무시한다
- **줌 200% 테스트 필수**: `vw` 단위는 줌 시 변하지 않으므로, `clamp()` 내 선호값에 `vw + rem`을 조합해야 줌 접근성(WCAG 1.4.4)을 확보할 수 있다
- **폴백(fallback) 제공**: 구형 브라우저를 위해 `clamp()` 위에 고정 `font-size`를 선언한다

```css
font-size: 2rem; /* fallback */
font-size: clamp(2rem, 4vw + 1rem, 3rem);
```

> **출처:** [Adrian Roselli — Responsive Type and Zoom](https://adrianroselli.com/2019/12/responsive-type-and-zoom.html)
> **출처:** [web.dev — Responsive and Fluid Typography with Baseline CSS](https://web.dev/articles/baseline-in-action-fluid-type)

### 모바일 네이티브 반응형 타이포그래피

| 플랫폼 | 메커니즘 | 핵심 단위 |
|--------|---------|----------|
| **iOS** | Dynamic Type + UIFontMetrics | pt (포인트) + 텍스트 스타일 |
| **Android** | sp (Scale-independent Pixels) | sp |
| **Flutter** | `MediaQuery.textScaleFactor` | logical pixels |

- iOS는 `UIFont.preferredFont(forTextStyle:)` 사용 시 사용자 설정 자동 반영
- Android sp 단위는 사용자의 글꼴 크기 설정을 자동 반영
- Flutter는 `textScaleFactor`를 존중하되, 최대 배율 제한(`maxScaleFactor`)으로 레이아웃 깨짐을 방지한다

> **출처:** [Apple HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
> **출처:** [Material Design 3 — Type Scale Tokens](https://m3.material.io/styles/typography/type-scale-tokens)
