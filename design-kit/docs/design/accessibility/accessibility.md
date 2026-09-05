---
title: 접근성
version: 0.3.0
last_updated: 2026-03-30
---

# 접근성 (Accessibility)

WCAG 2.2 핵심 요구사항, 인지 접근성, 모션 감수성, 투명도 감소, 실제 보조 기술 테스트 방법을 다룬다.

---

## 원칙 (POUR)

WCAG는 웹 콘텐츠 접근성의 4가지 근본 원칙인 **POUR**를 정의한다. 모든 접근성 성공 기준은 이 4가지 원칙 중 하나에 속한다.

### 1. 인식 가능 (Perceivable)

정보와 사용자 인터페이스 구성 요소는 사용자가 인식할 수 있는 방식으로 제시되어야 한다.

- 텍스트가 아닌 콘텐츠에 대체 텍스트 제공 (SC 1.1.1, Level A)
- 시간 기반 미디어에 자막 및 음성 해설 제공 (SC 1.2.x)
- 콘텐츠를 의미 손실 없이 다양한 방식으로 표현 가능 (SC 1.3.x)
- 전경과 배경의 구분이 용이하도록 설계 (SC 1.4.x)

### 2. 운용 가능 (Operable)

사용자 인터페이스 구성 요소와 내비게이션은 조작 가능해야 한다.

- 모든 기능이 키보드로 접근 가능 (SC 2.1.x)
- 충분한 시간 제공 (SC 2.2.x)
- 발작 유발 콘텐츠 회피 (SC 2.3.x)
- 사용자가 콘텐츠를 찾고 탐색할 수 있는 방법 제공 (SC 2.4.x)
- 다양한 입력 방식 지원 (SC 2.5.x)

### 3. 이해 가능 (Understandable)

정보와 사용자 인터페이스 조작은 이해할 수 있어야 한다.

- 텍스트를 읽고 이해할 수 있어야 함 (SC 3.1.x)
- 웹 페이지가 예측 가능한 방식으로 표시되고 작동 (SC 3.2.x)
- 사용자가 실수를 방지하고 수정할 수 있도록 지원 (SC 3.3.x)

### 4. 견고성 (Robust)

콘텐츠는 보조 기술을 포함한 다양한 사용자 에이전트가 안정적으로 해석할 수 있어야 한다.

- 마크업의 구문 분석 호환성 보장 (SC 4.1.x)
- 보조 기술이 이름, 역할, 값을 프로그래밍 방식으로 확인 가능 (SC 4.1.2)
- 상태 메시지를 보조 기술이 감지 가능 (SC 4.1.3)

> **출처:** [W3C WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)

---

## 색상 대비 (WCAG)

색상 대비는 시각 장애, 저시력, 색각 이상 사용자에게 핵심적인 접근성 요소다. WCAG 2.2는 세 가지 수준의 대비 요구사항을 정의한다.

### AA 수준 — 대비 최솟값 (SC 1.4.3)

| 대상 | 최소 대비비 |
|------|-----------|
| 일반 텍스트 (18pt 미만) | **4.5:1** |
| 큰 텍스트 (18pt 이상 또는 14pt 이상 볼드) | **3:1** |

> **출처:** [W3C WCAG 2.2 — SC 1.4.3 Contrast (Minimum)](https://www.w3.org/TR/WCAG22/#contrast-minimum)

### AAA 수준 — 대비 향상 (SC 1.4.6)

| 대상 | 최소 대비비 |
|------|-----------|
| 일반 텍스트 | **7:1** |
| 큰 텍스트 (18pt 이상 또는 14pt 이상 볼드) | **4.5:1** |

> **출처:** [W3C WCAG 2.2 — SC 1.4.6 Contrast (Enhanced)](https://www.w3.org/TR/WCAG22/#contrast-enhanced)

### 비텍스트 대비 (SC 1.4.11)

UI 컴포넌트(버튼 테두리, 입력 필드 등)와 의미 있는 그래픽 요소는 인접 색상과 최소 **3:1** 대비비를 충족해야 한다.

> **출처:** [W3C WCAG 2.2 — SC 1.4.11 Non-text Contrast](https://www.w3.org/TR/WCAG22/#non-text-contrast)

### 실무 권장사항

- 디자인 단계에서 대비 검증 도구를 사용한다 (예: WebAIM Contrast Checker, Stark)
- 브랜드 컬러가 대비 기준을 충족하지 않으면 대체 팔레트를 준비한다
- 다크 모드/라이트 모드 각각에서 별도로 대비를 검증한다
- 색상만으로 정보를 전달하지 않는다 — 패턴, 아이콘, 텍스트 레이블을 병행한다

---

## 터치 타겟 크기

터치 타겟 크기는 운동 장애 사용자와 일반 사용자 모두의 조작 정확도에 직접적인 영향을 미친다. Apple HIG 권장치인 44pt 미만의 버튼은 **탭 오류율이 25% 이상** 증가한다는 연구 결과가 있다 (WCAG 2.2 의 AA 하한은 24×24 CSS px 이며, 44×44 는 AAA 다 — 아래 표 참조).

### 플랫폼별 최소 요구사항

| 표준 | 최소 크기 | 수준 |
|------|----------|------|
| **WCAG 2.5.8** (Minimum) | **24 x 24 CSS px** | Level AA |
| **WCAG 2.5.5** (Enhanced) | **44 x 44 CSS px** | Level AAA |
| **Apple HIG** | **44 x 44 pt** | 필수 |
| **Android / Material Design** | **48 x 48 dp** | 권장 |

> **출처:** [W3C — Understanding SC 2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

### WCAG 2.5.8 상세 (Level AA, WCAG 2.2 신규)

인터랙티브 타겟은 최소 **24 x 24 CSS px** 이상이어야 한다. 예외 사항:

- **간격 예외**: 24px 미만이더라도 24px 직경 원을 각 타겟 중심에 그렸을 때 인접 타겟과 겹치지 않으면 허용
- **인라인 예외**: 문장 내부의 인라인 링크는 줄 높이에 의해 크기가 결정되므로 예외
- **동등 대안**: 동일 기능의 다른 컨트롤이 기준을 충족하면 예외
- **사용자 에이전트 결정**: 브라우저 기본 컨트롤의 크기는 저자가 수정하지 않은 경우 예외

> **출처:** [W3C WCAG 2.2 — SC 2.5.8 Target Size (Minimum)](https://www.w3.org/TR/WCAG22/#target-size-minimum)

### 실무 권장사항

- 시각적으로 작은 요소도 padding을 포함한 **히트 영역**은 최소 크기를 충족해야 한다
- 인접 타겟 간 최소 **8px** 이상의 간격을 권장한다
- 터치 디바이스에서는 Apple HIG의 44pt를 기본 기준으로 삼는 것이 안전하다

> **출처:** [Apple Human Interface Guidelines — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

---

## 스크린 리더

스크린 리더는 시각 장애 사용자가 디지털 콘텐츠에 접근하는 핵심 보조 기술이다. 올바른 시맨틱 마크업, ARIA 속성, 포커스 관리가 스크린 리더 호환성의 핵심이다.

### 시맨틱 마크업 우선

HTML의 네이티브 시맨틱 요소를 항상 ARIA보다 우선적으로 사용한다.

| 목적 | 올바른 마크업 | 잘못된 마크업 |
|------|-------------|-------------|
| 탐색 영역 | `<nav>` | `<div role="navigation">` |
| 메인 콘텐츠 | `<main>` | `<div role="main">` |
| 헤딩 | `<h1>` ~ `<h6>` | `<div role="heading">` |
| 버튼 | `<button>` | `<div role="button">` |
| 목록 | `<ul>`, `<ol>` | `<div role="list">` |

> **출처:** [MDN — Using HTML landmark roles to improve accessibility](https://developer.mozilla.org/en-US/blog/aria-accessibility-html-landmark-roles/)

### ARIA 랜드마크

ARIA 랜드마크는 페이지의 주요 영역을 식별하여 스크린 리더 사용자가 빠르게 탐색할 수 있도록 한다. **모든 페이지 콘텐츠는 랜드마크 안에 포함**하여 스크린 리더 사용자가 콘텐츠를 놓치지 않도록 해야 한다.

주요 랜드마크 역할:

| 역할 | HTML 요소 | 용도 |
|------|----------|------|
| `banner` | `<header>` | 사이트 전체 헤더 |
| `navigation` | `<nav>` | 탐색 링크 그룹 |
| `main` | `<main>` | 페이지의 핵심 콘텐츠 |
| `complementary` | `<aside>` | 보조 콘텐츠 |
| `contentinfo` | `<footer>` | 사이트 전체 푸터 |
| `search` | `<search>` (HTML Living Standard, 2023-03) | 검색 기능. Chrome 118 · Safari 17 · Firefox 118 이상 |
| `form` | `<form>` | 입력 양식 |
| `region` | `<section>` | 이름 붙여진 영역 |

> **출처:** [W3C — ARIA11: Using ARIA landmarks to identify regions of a page](https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA11)

### ARIA 필수 속성

- **`aria-label`**: 시각적 레이블이 없는 요소에 접근 가능한 이름 제공
- **`aria-labelledby`**: 화면에 보이는 다른 요소를 레이블로 참조
- **`aria-describedby`**: 추가 설명 텍스트 연결
- **`aria-live`**: 동적으로 변경되는 콘텐츠를 스크린 리더에 알림 (`polite`, `assertive`)
- **`aria-hidden="true"`**: 장식용 요소를 보조 기술에서 숨김
- **`aria-expanded`**: 접기/펼치기 상태를 전달

> **출처:** [W3C — ARIA Techniques for WCAG 2.0](https://www.w3.org/TR/WCAG20-TECHS/aria)

### 포커스 관리

- 모달/다이얼로그가 열리면 포커스를 내부로 이동한다
- 모달이 닫히면 포커스를 트리거 요소로 복원한다
- 포커스 트랩 (focus trap)으로 모달 외부로 포커스가 나가지 않도록 한다
- 동적으로 추가된 콘텐츠에 적절히 포커스를 이동한다
- `tabindex="-1"`로 프로그래밍 방식으로 포커스 가능한 요소를 만든다

---

## 키보드 네비게이션

키보드 접근성은 운동 장애 사용자, 스크린 리더 사용자, 파워 유저 모두에게 필수적이다.

### 포커스 순서 (SC 2.4.3, Level A)

포커스 가능한 구성 요소는 **의미와 조작성을 유지하는 순서**로 포커스를 받아야 한다.

- DOM 순서를 논리적 시각 순서와 일치시킨다
- CSS로 시각적 순서를 변경할 때 (`order`, `flex-direction: row-reverse`) 탭 순서가 어긋나지 않는지 검증한다
- `tabindex` 양수 값 사용을 피한다 — 자연스러운 DOM 순서를 깨뜨린다
- 복합 위젯(탭, 메뉴, 트리) 내부에서는 `roving tabindex` 또는 `aria-activedescendant` 패턴을 사용한다

> **출처:** [W3C WCAG 2.2 — SC 2.4.3 Focus Order](https://www.w3.org/TR/WCAG22/#focus-order)

### 포커스 가시성 (SC 2.4.7, Level AA)

키보드 조작 가능한 UI에는 **키보드 포커스 표시기가 보여야** 한다.

- 브라우저 기본 포커스 링을 제거(`outline: none`)하면 반드시 커스텀 포커스 스타일을 제공한다
- 포커스 표시기의 대비비는 최소 **3:1** 이상 권장 (WCAG 2.4.11, Level AAA에서는 필수)
- `:focus-visible` 의사 클래스를 활용하여 키보드 포커스만 스타일링한다

```css
/* 키보드 포커스만 시각적으로 강조 */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

> **출처:** [W3C WCAG 2.2 — SC 2.4.7 Focus Visible](https://www.w3.org/TR/WCAG22/#focus-visible)

### 키보드 트랩 방지 (SC 2.1.2, Level A)

포커스가 특정 컴포넌트에 갇히지 않아야 한다. 표준 키보드 방법(Tab, Shift+Tab, Escape)으로 포커스를 이동할 수 있어야 하며, 비표준 방법이 필요한 경우 사용자에게 안내한다.

> **출처:** [W3C WCAG 2.2 — SC 2.1.2 No Keyboard Trap](https://www.w3.org/TR/WCAG22/#no-keyboard-trap)

### 스킵 링크 (Skip Links)

반복되는 탐색 블록을 건너뛸 수 있는 메커니즘을 제공한다 (SC 2.4.1, Level A).

```html
<!-- 페이지 최상단에 배치 -->
<a href="#main-content" class="skip-link">
  메인 콘텐츠로 건너뛰기
</a>

<!-- 스타일: 포커스 시에만 표시 -->
<style>
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  position: static;
  left: auto;
}
</style>
```

- 스킵 링크는 페이지에서 Tab 키를 누르면 **첫 번째로 포커스**를 받아야 한다
- 메인 콘텐츠뿐 아니라 반복 영역이 많은 경우 여러 스킵 링크를 제공할 수 있다

> **출처:** [W3C WCAG 2.2 — SC 2.4.1 Bypass Blocks](https://www.w3.org/TR/WCAG22/#bypass-blocks)

### 키보드 인터랙션 패턴 요약

| 컴포넌트 | 키보드 동작 |
|---------|-----------|
| 버튼 | `Enter` / `Space` — 활성화 |
| 링크 | `Enter` — 이동 |
| 탭 패널 | `Arrow Left/Right` — 탭 전환, `Tab` — 패널 콘텐츠로 이동 |
| 메뉴 | `Arrow Up/Down` — 항목 이동, `Enter` — 선택, `Escape` — 닫기 |
| 모달 | `Escape` — 닫기, `Tab` — 내부 순환 |
| 드롭다운 | `Arrow Up/Down` — 옵션 이동, `Enter` — 선택, `Escape` — 닫기 |

> **출처:** [W3C WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)

---

## 인지 접근성 (Cognitive Accessibility)

WCAG는 시각/청각/운동 장애에 집중하는 경향이 있지만, 인지 장애(학습 장애, ADHD, 자폐 스펙트럼, 노인성 인지 저하)는 전체 장애의 약 **40%**를 차지한다. W3C의 Cognitive and Learning Disabilities Accessibility Task Force(COGA TF)가 별도 가이드를 발행했다.

### 핵심 원칙

| 원칙 | 설명 | 실무 적용 |
|------|------|----------|
| **단순한 언어** | 전문 용어, 약어, 이중 부정을 피한다 | 에러 메시지: "유효하지 않은 입력" → "이메일에 @ 기호가 필요합니다" |
| **예측 가능한 UI** | 같은 기능은 항상 같은 위치, 같은 모양 | 뒤로가기는 항상 좌측 상단. 저장은 항상 우측 하단 |
| **주의 분산 최소화** | 자동 재생 미디어, 깜빡이는 배너, 움직이는 광고 제거 | 자동 재생 비디오에 반드시 일시정지 제공 |
| **충분한 시간** | 세션 타임아웃 전 경고 + 연장 옵션 | "세션이 5분 후 만료됩니다 [연장하기]" |
| **명확한 피드백** | 액션 결과를 즉시, 명시적으로 전달 | "저장됨" 표시가 0.5초 만에 사라지면 인지 장애 사용자가 놓친다 — 최소 3초 유지 |
| **기억 의존 최소화** | 이전 단계 정보를 다음 단계에서 참조할 필요를 없앤다 | 멀티 스텝 폼에서 이전 입력 요약을 표시한다 |

### COGA 실패 사례

- **CAPTCHA**: 시각적 퍼즐은 인지 장애 사용자에게 극도로 어렵다. reCAPTCHA v3(스코어 기반, 사용자 상호작용 불필요)를 권장
- **복잡한 비밀번호 규칙**: "대문자+소문자+숫자+특수문자+8자 이상"은 인지 부하가 높다. 패스키(Passkey)나 생체 인증을 대안으로 제공
- **컨텍스트 없는 아이콘**: 라벨 없는 아이콘은 학습 장애 사용자에게 특히 어렵다

> **출처:** [W3C — Making Content Usable for People with Cognitive and Learning Disabilities](https://www.w3.org/TR/coga-usable/)
> **출처:** [W3C COGA Task Force](https://www.w3.org/WAI/GL/task-forces/coga/)

---

## 모션 감수성 상세

### prefers-reduced-motion

전정 기관(vestibular system) 장애 사용자는 화면 내 대규모 움직임으로 어지러움, 구역질, 두통을 경험한다. iOS "동작 줄이기", macOS "동작 줄이기", Windows "애니메이션 효과 끄기"가 이 쿼리를 트리거한다.

**위험 모션 유형 (높은 순):**

| 위험도 | 모션 유형 | 대안 |
|--------|----------|------|
| 최고 | 시차 스크롤(parallax) | 정적 배경 |
| 최고 | 전체 화면 줌/확대 | 크로스페이드 전환 |
| 높음 | 회전/스핀 (큰 요소) | 정적 아이콘 또는 소형 인디케이터 |
| 높음 | 스크롤 연동 애니메이션 | 정적 배치 |
| 중간 | 자동 캐러셀/슬라이더 | 수동 전환 + 일시정지 |
| 낮음 | 페이드 인/아웃 (150ms 이하) | 유지 가능 |
| 낮음 | 체크마크 그리기 | 유지 가능 |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

> **출처:** [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
> **출처:** [A11y Project — Understanding Vestibular Disorders](https://www.a11yproject.com/posts/understanding-vestibular-disorders/)

---

## 투명도 감소 (Reduced Transparency)

### prefers-reduced-transparency

시력이 약하거나 광과민성이 있는 사용자는 반투명 배경 위의 텍스트를 읽기 어렵다. iOS "투명도 줄이기", macOS "투명도 줄이기" 설정이 이 쿼리를 트리거한다.

```css
/* 기본: 반투명 배경 */
.overlay {
  background: rgba(0, 0, 0, 0.5);
}

/* 투명도 감소: 불투명 배경 */
@media (prefers-reduced-transparency: reduce) {
  .overlay {
    background: rgb(30, 30, 30);  /* 불투명으로 전환 */
  }
}
```

Apple은 다크 모드에서 사이드바, 시트 배경에 반투명 효과를 기본 적용하지만, "투명도 줄이기" 활성 시 불투명 배경으로 자동 전환한다.

> **출처:** [MDN — prefers-reduced-transparency](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency)
> **출처:** [Apple HIG — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

---

## 실제 보조 기술 테스트

### 테스트 환경 구성

디자인 단계의 접근성 검증(대비 체크, 구조 검토)만으로는 충분하지 않다. 실제 보조 기술로 테스트해야 발견되는 문제가 있다.

### 스크린 리더 테스트 매트릭스

| 플랫폼 | 스크린 리더 | 브라우저/앱 | 점유율 (WebAIM 2024) |
|--------|-----------|-----------|---------------------|
| iOS | **VoiceOver** | Safari | 약 34.2% |
| Windows | **NVDA** | Chrome/Firefox | 약 30.7% |
| Windows | **JAWS** | Chrome/Edge | 약 26.5% |
| Android | **TalkBack** | Chrome | 약 5.1% |
| macOS | **VoiceOver** | Safari | 약 2.5% |

**최소 테스트 조합:** iOS VoiceOver + Safari, Windows NVDA + Chrome (전체의 약 65% 커버).

### 스크린 리더 테스트 체크리스트

- [ ] 페이지 제목(`<title>`)이 페이지 목적을 명확히 설명하는가?
- [ ] 헤딩 구조(h1→h2→h3)가 논리적 순서를 따르는가? (h1 건너뛰고 h3 사용 금지)
- [ ] 모든 이미지에 의미 있는 `alt` 텍스트가 있는가? (장식 이미지는 `alt=""`)
- [ ] 폼 필드마다 연결된 `<label>`이 있는가?
- [ ] 버튼/링크의 접근 가능한 이름이 기능을 설명하는가? ("여기를 클릭" 금지)
- [ ] 동적 콘텐츠 변경이 `aria-live`로 스크린 리더에 통보되는가?
- [ ] 모달 열림 시 포커스가 모달 내부로 이동하는가?
- [ ] 모달 닫힘 시 포커스가 트리거 요소로 복귀하는가?
- [ ] Tab 순서가 시각적 순서와 일치하는가?

### 자동화 도구 한계

Deque 의 자동 검사 커버리지 보고서는 자사 자동화 테스트가 전체 이슈의 **57.38%** 를 검출했다고 밝힌다 (같은 보고서가 업계 통념을 "20~30%" 로 소개한다). 어느 쪽이든 나머지는 수동 테스트로만 발견된다 — 자동화만으로 끝내지 마라.

- 의미적으로 잘못된 alt 텍스트 (기술적으로는 존재하지만 내용이 부적절)
- 논리적이지 않은 탭 순서
- 시각적 포커스 표시가 있지만 대비가 부족한 경우
- 모달 내 포커스 트랩이 불완전한 경우
- 동적 콘텐츠의 aria-live 누락

> **출처:** [WebAIM — Screen Reader User Survey #10](https://webaim.org/projects/screenreadersurvey10/)
> **출처:** [Deque — Automated Accessibility Testing](https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues/)
