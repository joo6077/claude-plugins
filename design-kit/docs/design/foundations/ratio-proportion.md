---
title: 비율과 프로포션
version: 0.3.0
last_updated: 2026-03-30
---

# 비율과 프로포션 (Ratio & Proportion)

## 원칙

비율(Ratio)은 요소 간 관계를 수학적으로 정의하는 기본 도구다. 임의 수치 대신 체계적 비율을 적용하면:

1. **시각적 조화** — 수학적 관계 기반 크기/간격은 인간 시각 체계가 자연스럽게 인지한다
2. **일관성** — 하나의 비율 체계에서 파생된 값들이 디자인 시스템 전체에 통일감을 부여한다
3. **확장성** — 비율 기반 레이아웃은 다양한 화면 크기에서 비례를 유지한다
4. **의사결정 효율** — "왜 이 크기인가?"에 대한 답이 명확해져 리뷰와 협업이 빨라진다

> **출처:** [The Golden Ratio and User-Interface Design — NN/g](https://www.nngroup.com/articles/golden-ratio-ui-design/)

---

## 황금비 (Golden Ratio, 1:1.618)

### 정의

황금비(φ, phi)는 약 1:1.618의 비율로, 자연계와 예술에서 반복적으로 나타나는 수학적 상수다. UI 디자인에서는 레이아웃, 타이포그래피, 간격에 활용된다.

### UI 레이아웃 적용

황금 사각형을 활용한 2단 레이아웃이 대표적이다:

| 전체 너비 | 메인 콘텐츠 | 사이드바 |
|-----------|------------|---------|
| 960px | 593px (61.8%) | 367px (38.2%) |
| 1200px | 742px (61.8%) | 458px (38.2%) |
| 1440px | 890px (61.8%) | 550px (38.2%) |

```
┌─────────────────────────────┬──────────────────┐
│                             │                  │
│     메인 콘텐츠 (61.8%)      │  사이드바 (38.2%) │
│                             │                  │
└─────────────────────────────┴──────────────────┘
```

### 타이포그래피 적용

본문 크기를 기준으로 1.618을 곱하여 제목 크기를 산출한다:

| 기준 본문 | × 1.618 (h3) | × 1.618² (h2) | × 1.618³ (h1) |
|----------|-------------|---------------|---------------|
| 14px | 22.65px → 23px | 36.65px → 37px | 59.29px → 59px |
| 16px | 25.89px → 26px | 41.89px → 42px | 67.77px → 68px |
| 18px | 29.12px → 29px | 47.12px → 47px | 76.24px → 76px |

행간(line-height)도 황금비를 참조할 수 있다. 본문 16px 기준 line-height ≈ 26px (16 × 1.618).

> **출처:** [Golden Ratio in UI Design — Figma Resource Library](https://www.figma.com/resource-library/golden-ratio/)

### 한계

- 반응형 웹에서 모든 뷰포트에 황금비를 완벽히 적용하기 어렵다
- 행간 계산 시 줄 길이에 따른 가독성 조정이 필요하다
- 수학은 디자이너의 경험적 판단을 대체하지 못한다 — 도구일 뿐 절대 법칙이 아니다
- NNGroup은 황금비가 "디자인 문제를 해결하는 데 거의 도움이 안 된다"고 지적하며, 콘텐츠 요구사항이 비율보다 우선해야 한다고 강조한다

> **출처:** [The Golden Ratio and User-Interface Design — NN/g](https://www.nngroup.com/articles/golden-ratio-ui-design/)

---

## 3분할 법칙 (Rule of Thirds)

### 정의

화면을 가로 3등분, 세로 3등분하여 9개 영역으로 나누는 구성 기법이다. 교차점(power point) 4곳에 핵심 요소를 배치하면 시각적 긴장감과 균형을 동시에 얻는다.

### UI 적용

```
┌───────────┬───────────┬───────────┐
│           │           │           │
│     ●─────┼─────●     │           │
│           │           │           │
├───────────┼───────────┼───────────┤
│           │           │           │
│     ●─────┼─────●     │           │
│           │           │           │
└───────────┴───────────┴───────────┘
  ● = power point (CTA, 핵심 이미지 배치)
```

| 적용 영역 | 기법 |
|----------|------|
| Hero 섹션 | 핵심 메시지를 상단 1/3 교차점에 배치 |
| 랜딩 페이지 | CTA 버튼을 하단 1/3 교차점에 배치 |
| 카드 레이아웃 | 이미지 영역 2/3 + 텍스트 영역 1/3 |
| 대시보드 | 주요 KPI를 상단 1/3에 집중 배치 |

### 3단 그리드 시스템

CSS Grid로 3분할 구현:

```css
.rule-of-thirds {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr;
}
```

> **출처:** [Golden Ratio in Design — Mockplus](https://www.mockplus.com/blog/post/the-golden-ratio-in-design)

---

## 화면 비율 체계

### 주요 화면 비율

| 비율 | 종횡비 | 주요 용도 | 특성 |
|------|-------|----------|------|
| **16:9** | 1.778 | 데스크톱 모니터, YouTube, TV | 가장 보편적인 와이드스크린 비율 |
| **4:3** | 1.333 | 태블릿(iPad), 레거시 모니터 | 20세기 표준, 문서/읽기에 적합 |
| **1:1** | 1.000 | 소셜 미디어 프로필, 썸네일 | 정사각형, 시선 집중 효과 |
| **3:2** | 1.500 | Surface 디바이스, 사진 | DSLR 사진 표준 비율 |
| **9:16** | 0.563 | 모바일 세로, Shorts/Reels | 세로 동영상 표준 |
| **21:9** | 2.333 | 울트라와이드 모니터 | 멀티태스킹, 영화 비율 |

### 반응형 고려사항

디바이스별 화면 비율이 다르므로 고정 비율 레이아웃은 주의가 필요하다:

- **데스크톱** (16:9 ~ 16:10): 가로 중심 레이아웃, 사이드바 활용 가능
- **태블릿** (4:3 ~ 3:2): 가로/세로 전환 대응 필수
- **모바일** (9:16 ~ 9:19.5): 세로 스크롤 중심, 컨텐츠 스택 레이아웃

> **출처:** [CSS aspect-ratio — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio)

---

## 비율 기반 레이아웃

### CSS aspect-ratio 속성

모던 CSS에서 비율 컨테이너를 직접 선언할 수 있다 (Chrome 88+, Firefox 89+, Safari 15.4+):

```css
/* 16:9 비디오 컨테이너 */
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

/* 1:1 정사각형 썸네일 */
.thumbnail {
  aspect-ratio: 1 / 1;
  width: 200px;
}

/* 4:3 카드 이미지 */
.card-image {
  aspect-ratio: 4 / 3;
  width: 100%;
  object-fit: cover;
}
```

### 레거시 패딩 핵 (Padding Hack)

`aspect-ratio` 미지원 환경에서는 padding-top 퍼센트를 활용한다:

| 비율 | padding-top 값 | 계산식 |
|------|---------------|--------|
| 16:9 | 56.25% | 9 ÷ 16 × 100 |
| 4:3 | 75% | 3 ÷ 4 × 100 |
| 1:1 | 100% | 1 ÷ 1 × 100 |
| 3:2 | 66.67% | 2 ÷ 3 × 100 |
| 21:9 | 42.86% | 9 ÷ 21 × 100 |

```css
/* 레거시 16:9 컨테이너 */
.ratio-16-9 {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
}
.ratio-16-9 > * {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}
```

### 퍼센트 기반 그리드

비율을 직접 그리드 컬럼에 적용:

```css
/* 황금비 2단 레이아웃 */
.golden-grid {
  display: grid;
  grid-template-columns: 61.8% 38.2%;
  gap: 24px;
}

/* 3분할 레이아웃 */
.thirds-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

/* 2:1 비율 레이아웃 */
.two-one-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}
```

> **출처:** [The CSS aspect-ratio property — web.dev](https://web.dev/articles/aspect-ratio)

---

## 모듈러 스케일 (Modular Scale)

### 정의

모듈러 스케일은 기준값(base)에 일정한 비율(ratio)을 반복적으로 곱하여 생성하는 수열이다. 공식: `value = base × ratio^n`

Tim Brown이 A List Apart에서 소개한 이 개념은 임의의 수치 대신 수학적 관계에 기반한 타이포그래피 시스템을 만든다.

> **출처:** [More Meaningful Typography — A List Apart](https://alistapart.com/article/more-meaningful-typography/)

### 주요 비율

| 비율 | 이름 | 값 | 특성 | 적합한 용도 |
|------|------|-----|------|-----------|
| 1.067 | Minor Second | 15:16 | 매우 미세한 차이 | 밀집 데이터 UI |
| 1.125 | Major Second | 8:9 | 미세한 차이 | 대시보드, 테이블 |
| 1.200 | Minor Third | 5:6 | 부드러운 대비 | 모바일 UI |
| 1.250 | Major Third | 4:5 | 적당한 대비 | 일반 웹 UI |
| 1.333 | Perfect Fourth | 3:4 | 명확한 계층 | 가장 보편적인 웹 UI 비율 |
| 1.414 | Augmented Fourth | √2 | 극적인 대비 | 프로모션, A4 비율 |
| 1.500 | Perfect Fifth | 2:3 | 강한 대비 | 에디토리얼 |
| 1.618 | Golden Ratio | φ | 극적 대비 | 고급 브랜드, 에디토리얼 |

### 실전 스케일 예시 (base: 16px, ratio: 1.333)

| 단계 | 계산 | 크기 | 용도 |
|------|------|------|------|
| -2 | 16 ÷ 1.333² | 9px | Caption, 부가 텍스트 |
| -1 | 16 ÷ 1.333 | 12px | Small, 레이블 |
| 0 | 16 × 1.333⁰ | 16px | Body (기준) |
| 1 | 16 × 1.333¹ | 21px | H4 / Subtitle |
| 2 | 16 × 1.333² | 28px | H3 |
| 3 | 16 × 1.333³ | 38px | H2 |
| 4 | 16 × 1.333⁴ | 50px | H1 |
| 5 | 16 × 1.333⁵ | 67px | Display |

### 이중 기준 스케일 (Double-Stranded Scale)

하나의 비율만으로는 필요한 값이 부족할 수 있다. Tim Brown은 두 개의 기준값(예: 18px + 190px)을 사용하여 더 촘촘한 스케일을 생성하는 기법을 제안했다.

```
기준 A: 18px × 1.618^n → 18, 29, 47, 76, 123, 199...
기준 B: 190px ÷ 1.618^n → 190, 117, 73, 45, 28, 17...
병합 스케일: 17, 18, 28, 29, 45, 47, 73, 76, 117, 123, 190, 199...
```

### 간격(Spacing)에의 적용

타이포그래피뿐 아니라 간격 시스템에도 동일한 비율을 적용한다:

```css
:root {
  --space-base: 16px;
  --space-ratio: 1.333;

  --space-3xs: calc(var(--space-base) / 1.333 / 1.333 / 1.333); /* 7px */
  --space-2xs: calc(var(--space-base) / 1.333 / 1.333);          /* 9px */
  --space-xs:  calc(var(--space-base) / 1.333);                   /* 12px */
  --space-sm:  var(--space-base);                                  /* 16px */
  --space-md:  calc(var(--space-base) * 1.333);                   /* 21px */
  --space-lg:  calc(var(--space-base) * 1.333 * 1.333);          /* 28px */
  --space-xl:  calc(var(--space-base) * 1.333 * 1.333 * 1.333);  /* 38px */
}
```

> **출처:** [How do I establish a type scale for my project? — Cieden](https://cieden.com/book/sub-atomic/typography/establishing-a-type-scale)

---

## 컴포넌트 비율

### 카드 (Card)

| 카드 유형 | 권장 비율 | 이미지 영역 | 적합한 콘텐츠 |
|----------|----------|-----------|-------------|
| 상품 카드 | 3:4 또는 4:5 | 상단 60~70% | 이커머스, 포트폴리오 |
| 뉴스 카드 | 16:9 | 상단 40~50% | 뉴스, 블로그 |
| 소셜 카드 | 1:1 | 상단 50% | SNS 피드 |
| 가로형 카드 | 2:1 | 좌측 40% | 리스트, 검색 결과 |
| 세로형 카드 | 9:16 | 전체 배경 | 스토리, 릴스 썸네일 |

### 이미지 크롭

| 용도 | 권장 비율 | 해상도 예시 |
|------|----------|-----------|
| Hero 배너 | 21:9 또는 16:9 | 2560×1097, 1920×1080 |
| OG 이미지 | 1.91:1 | 1200×630 |
| 썸네일 (YouTube) | 16:9 | 1280×720 |
| 프로필 이미지 | 1:1 | 400×400 |
| 인스타그램 포스트 | 1:1 또는 4:5 | 1080×1080, 1080×1350 |
| Pinterest 핀 | 2:3 | 1000×1500 |

### Hero 섹션

Hero 섹션의 높이는 뷰포트 비율로 결정하는 것이 일반적이다:

| 유형 | 높이 | 비율 근사값 |
|------|------|-----------|
| Full-screen Hero | 100vh | 뷰포트 전체 |
| 3/4 Hero | 75vh | 약 4:3 (데스크톱 기준) |
| Half Hero | 50vh | 약 8:3 (데스크톱 기준) |
| Compact Hero | 33vh | 약 16:3 (데스크톱 기준) |

### 아이콘 및 터치 타겟

디바이스 밀도에 따른 비율 관계:

| 밀도 | 배율 | 아이콘 기준 (24dp) |
|------|------|------------------|
| mdpi (1x) | 1.0 | 24×24px |
| hdpi (1.5x) | 1.5 | 36×36px |
| xhdpi (2x) | 2.0 | 48×48px |
| xxhdpi (3x) | 3.0 | 72×72px |
| xxxhdpi (4x) | 4.0 | 96×96px |

8의 배수 시스템을 사용하면 0.5배 스케일링에서도 정수 픽셀을 유지할 수 있다 (예: 8 × 1.5 = 12, 소수점 없음).

> **출처:** [Remain Design System — 비율 디자인](https://www.remain.co.kr/page/designsystem/ratio-design.php)

### 최소 터치 타겟 비교

| 플랫폼 | 최소 크기 | 권장 크기 |
|--------|----------|----------|
| Apple (iOS) | 44×44pt | 44×44pt |
| Material (Android) | 48×48dp | 48×48dp |
| WCAG 2.2 | 24×24px (SC 2.5.8 AA) | 44×44px (SC 2.5.5 AAA) |

> **출처:** [Tommso Design Style Guide](https://www.tommso.com/our_service/design/style_guide)

---

## 실전 가이드라인

### 비율 선택 체크리스트

1. **콘텐츠 밀도가 높은 UI** (대시보드, 테이블) → Minor Third (1.200) 또는 Major Third (1.250)
2. **일반 웹 UI** (블로그, 서비스 페이지) → Perfect Fourth (1.333)
3. **에디토리얼 / 마케팅** (랜딩 페이지, 매거진) → Golden Ratio (1.618)
4. **모바일 우선** → Minor Third (1.200), 화면이 좁아 큰 비율은 과도함

### 주의사항

- 모듈러 스케일은 도구이지 마법이 아니다. 스케일에서 벗어난 값이 시각적으로 더 적합하면 그 값을 쓴다
- 반응형 환경에서 황금비를 모든 뷰포트에 적용하려 하지 않는다. 브레이크포인트별로 비율을 조정한다
- 8px 그리드 시스템과 모듈러 스케일 값이 충돌하면 8의 배수로 라운딩하는 것이 실용적이다
- 디바이스 픽셀 밀도를 고려하여 2x 기준(xhdpi, ~430ppi)을 표준 작업 해상도로 채택한다

> **출처:** [Remain Design System — 비율 디자인](https://www.remain.co.kr/page/designsystem/ratio-design.php), [Tommso Design Style Guide](https://www.tommso.com/our_service/design/style_guide)
