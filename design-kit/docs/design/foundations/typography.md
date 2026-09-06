---
title: 타이포그래피
version: 0.3.0
last_updated: 2026-03-30
---

# 타이포그래피

타이포그래피 스케일, 서체 페어링, 가독성, CJK 특수 고려사항, 반응형 전략을 다룬다.

---

## 원칙

### 1. 계층 구조(Visual Hierarchy)를 3단계 이내로 유지한다

크기, 굵기, 색상 세 축을 조합해 정보 중요도를 전달한다. 제목-본문-캡션 구분이 0.5초 이내에 인지되어야 한다. MD3는 Display, Headline, Title, Body, Label 5가지 역할(role) 체계를 정의하지만, 실무에서 한 화면에 3단계 이상 쓰면 계층이 흐려진다. NNGroup 아이트래킹 연구에서 사용자는 시각 계층이 명확한 페이지를 47% 더 빠르게 스캔했다.

> **출처:** [Material Design 3 — Type Scale Tokens](https://m3.material.io/styles/typography/type-scale-tokens)
> **출처:** [NNGroup — How People Read Online](https://www.nngroup.com/articles/how-people-read-online/)

### 2. 시스템 서체를 우선 사용한다

플랫폼 기본 서체(iOS: SF Pro/NY, Android: Roboto Flex, Web: system-ui)를 우선 채택하면 렌더링 성능과 일관성을 확보한다. Apple HIG는 내장 텍스트 스타일 우선 사용을 권고한다. 커스텀 서체를 도입할 경우 FOUT(Flash of Unstyled Text)와 CLS(Cumulative Layout Shift) 리스크가 발생한다. Google Fonts 데이터에 따르면 웹폰트 하나의 평균 크기는 WOFF2 기준 약 20~40KB이며, 한글 서체는 글리프 수 때문에 1~5MB에 달한다.

> **출처:** [Apple HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

### 3. Dynamic Type / 사용자 설정을 존중한다

사용자가 선택한 텍스트 크기를 반영해야 한다. iOS Dynamic Type, Android sp 단위, 웹 rem 단위가 시스템 글꼴 크기 설정을 자동 반영한다. WCAG 1.4.4는 텍스트 200% 확대를 요구한다. WebAIM Million 2024 조사에서 텍스트 리사이즈 문제를 가진 사이트가 전체의 약 12%였다.

> **출처:** [WCAG 1.4.4 Resize Text](https://www.w3.org/WAI/WCAG21/Understanding/resize-text.html)

### 4. 글꼴 크기는 충분히 크게 설정한다

NNGroup 연구에서 빠르게 인지해야 하는 텍스트(glanceable text)일수록 더 큰 크기가 필요하며, 좁은(condensed) 서체는 일반 너비 대비 11.2% 더 긴 인지 시간이 소요된다. 모바일 본문 최소 16px(1rem), 데스크톱 본문 16~18px. 12px 미만 텍스트는 40세 이상 사용자의 가독성이 급격히 하락한다.

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

---

## 서체 페어링 (Font Pairing)

### 기본 원칙

서체 페어링은 "대비 속의 조화"가 핵심이다. 같은 성격의 서체 두 개를 쓰면 구분이 안 되고, 지나치게 다른 성격이면 통일감이 무너진다.

**3가지 페어링 전략:**

| 전략 | 설명 | 예시 |
|------|------|------|
| **대비 (Contrast)** | 산세리프 제목 + 세리프 본문 (또는 반대) | Montserrat + Merriweather |
| **슈퍼패밀리 (Superfamily)** | 동일 서체 패밀리의 산/세리프 변형 조합 | Noto Sans + Noto Serif, Source Sans + Source Serif |
| **단일 서체 (Single Family)** | 하나의 서체에서 굵기/크기로만 계층 표현 | Inter 400/500/700, Pretendard Light/Regular/Bold |

**실무 규칙:**
- 서체는 **최대 2~3개**로 제한한다. 3개 초과는 시각 노이즈를 유발한다.
- 제목용 서체의 x-height가 본문용 서체와 크게 다르면 병치 시 이질감이 발생한다. x-height 비율이 ±10% 이내인 서체를 선택한다.
- 두 서체의 글자 너비(character width)가 극단적으로 다르면 텍스트 블록 간 밀도 차이가 발생한다.

**한글 + 영문 페어링 고려사항:**
- 한글 서체의 시각적 무게는 영문보다 무겁다. 한글 본문 400weight에 영문 400weight를 그대로 쓰면 영문이 가벼워 보인다.
- Pretendard + Inter, Noto Sans KR + Noto Sans 조합은 x-height와 자간이 미리 조율되어 있다.
- 한글 서체의 글리프 수는 11,172자(현대 한글 완성형)로, 웹폰트 용량 관리가 필수다. 서브셋(subset) 적용 시 사용 빈도 기준 상위 2,350자만으로 일반 콘텐츠의 99%를 커버한다.

> **출처:** [Google Fonts — Choosing Type](https://fonts.google.com/knowledge/choosing_type)
> **출처:** [Typewolf — Font Pairing](https://www.typewolf.com/site-of-the-day)

---

## 가변 서체 (Variable Fonts)

### 개요

가변 서체(Variable Font)는 하나의 파일에 여러 스타일(굵기, 너비, 기울기 등)을 연속적인 축(axis)으로 포함한다. OpenType 1.8(2016)에서 도입되었으며, 주요 브라우저 지원률은 2024년 기준 97% 이상이다.

### 등록 축 (Registered Axes)

| 축 태그 | 이름 | 범위 (일반) | 설명 |
|---------|------|-----------|------|
| `wght` | Weight | 100~900 | 굵기. 100=Thin, 400=Regular, 700=Bold |
| `wdth` | Width | 75~125 | 자폭. 75=Condensed, 100=Normal, 125=Expanded |
| `ital` | Italic | 0 또는 1 | 이탤릭 on/off |
| `slnt` | Slant | -12~0 | 기울기 각도 (0=직립, -12=최대 기울기) |
| `opsz` | Optical Size | 8~144 | 광학 크기. 작은 크기에서 획을 두껍게, 큰 크기에서 가늘게 자동 조정 |

### 커스텀 축 예시

| 서체 | 축 | 효과 |
|------|-----|------|
| **Recursive** | `CASL` (Casualness) | 0=직선적 → 1=손글씨 느낌 |
| **Roboto Flex** | `GRAD` (Grade) | 배경 밝기에 따른 획 두께 미세 조정 |
| **Inter** | 없음 (단일 축 wght만 지원) | 400~700 범위의 단순한 가변 지원 |

### CSS 적용

```css
/* 가변 서체 선언 */
@font-face {
  font-family: 'InterVariable';
  src: url('Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;           /* 가변 범위 선언 */
  font-display: swap;
}

/* 축 값 설정 */
.headline {
  font-variation-settings: 'wght' 700, 'opsz' 48;
}
.body {
  font-variation-settings: 'wght' 400, 'opsz' 16;
}

/* 성능: 개별 폰트 파일 4~6개를 하나의 가변 파일로 대체 → HTTP 요청 감소 */
```

### 성능 이점

- 일반적으로 Regular + Bold + Italic 3파일 합산 크기 > 가변 폰트 1파일 크기
- Google Fonts 분석에서 Roboto의 정적 6weight 합산은 약 150KB, 가변 폰트는 약 90KB (WOFF2 기준)
- 한글 가변 폰트는 글리프 수 때문에 이점이 상대적으로 작다. Pretendard Variable은 약 4.5MB.

> **출처:** [web.dev — Introduction to Variable Fonts on the Web](https://web.dev/articles/variable-fonts)
> **출처:** [MDN — Variable Fonts Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts/Variable_fonts_guide)

---

## CJK 타이포그래피

### 한중일 텍스트의 특수성

CJK(Chinese, Japanese, Korean) 텍스트는 라틴 문자와 근본적으로 다른 특성을 가진다.

| 특성 | 라틴 | 한글 | 일본어 | 중국어 |
|------|------|------|--------|--------|
| 글자 형태 | 가변 폭 (i ≠ m) | 고정 폭(정사각 바운딩 박스) | 고정 폭 + 가변 폭(가나) 혼합 | 고정 폭 |
| 줄바꿈 | 단어 단위 (word-break) | 음절 단위 가능 | 금칙 처리(禁則處理) 필요 | 표점부호 금칙 필요 |
| 최적 줄 높이 | 1.4~1.6em | **1.6~1.8em** | **1.5~1.8em** | **1.5~1.7em** |
| 최적 줄 길이 | 50~75자 | **25~35자** | **25~40자** | **25~35자** |

### 한글 줄 높이(Line Height) 권장값

한글은 자모 조합 구조(초성+중성+종성)로 인해 라틴 문자보다 글자 내부 공간이 빽빽하다. 동일 줄 높이를 적용하면 답답하게 느껴진다.

| 텍스트 유형 | 라틴 권장 | 한글 권장 | 차이 근거 |
|------------|----------|----------|----------|
| 본문 (Body) | 1.4~1.6em | 1.6~1.8em | 한글 자모 밀도가 높아 행간 여유 필요 |
| 제목 (Heading) | 1.1~1.3em | 1.3~1.5em | 큰 크기에서도 0.2em 추가 |
| 작은 텍스트 | 1.3~1.4em | 1.5~1.6em | 작을수록 한글 가독성 더 민감 |

### 줄바꿈 & 워드 브레이크

```css
/* 한글: 음절 단위 줄바꿈 허용 (기본값) */
.ko-text {
  word-break: keep-all;     /* 단어 단위 유지 — 의미 단위 끊김 방지 */
  overflow-wrap: break-word; /* 긴 단어 시 컨테이너 오버플로 방지 */
}

/* 일본어: 금칙 처리 — 행두 금칙문자(。、)가 줄 첫머리에 오지 않도록 */
.ja-text {
  word-break: normal;
  line-break: strict;
}
```

`word-break: keep-all`은 한글에서 핵심이다. 미적용 시 "사용자가 선택한 텍스트" 같은 문장이 "사용자가 선택" / "한 텍스트"로 어색하게 끊긴다.

### 자간(Letter Spacing) 주의

한글 본문에 양수 letter-spacing을 적용하면 글자 간 연결감이 끊겨 가독성이 하락한다. 한글 본문은 letter-spacing 0을 유지하고, 영문 대문자 라벨에만 0.05~0.1em 정도 추가한다.

> **출처:** [W3C — Requirements for Chinese Text Layout](https://www.w3.org/TR/clreq/)
> **출처:** [W3C — Requirements for Japanese Text Layout](https://www.w3.org/TR/jlreq/)
> **출처:** [W3C — Requirements for Hangul Text Layout and Typography](https://www.w3.org/TR/klreq/)
