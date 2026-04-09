---
title: 비주얼 스타일
version: 0.1.0
last_updated: 2026-04-08
---

# 비주얼 스타일 (UI Visual Styles & Design Morphisms)

UI 비주얼 스타일 35종의 정의, 시각 특성, CSS 구현 기법, 시대적 맥락, 대표 사례를 다룬다. design-kit의 컨셉 시안 생성, 디자인 시스템 세팅, 디자인 감사에서 참조한다.

---

## 총칭 및 분류 체계

UI 비주얼 스타일을 가리키는 용어는 맥락에 따라 달라진다. 통일된 학술 용어는 없으며 커뮤니티 관행이 사실상 표준이다.

### Design Morphisms

`-morphism` 접미사를 공유하는 계열. 그리스어 morphe(형태)에서 유래. 물리 세계의 질감이나 깊이를 디지털 표면에 표현하는 방식을 지칭한다. Skeuomorphism, Neumorphism, Glassmorphism, Claymorphism 등이 속한다.

### UI Visual Styles / UI Design Paradigms

Morphism 계열을 포함한 모든 시각적 접근법을 포괄하는 상위 개념. Brutalism, Minimalism, Bento Grid처럼 `-morphism` 접미사를 쓰지 않는 스타일까지 아우른다. 본 문서에서는 이 용어를 총칭으로 사용한다.

### Surface Treatments

CSS/구현 관점에서 표면(surface)에 적용하는 시각 처리를 분류하는 용어. `box-shadow`, `backdrop-filter`, `gradient`, `texture` 등 속성 중심으로 스타일을 구분할 때 사용한다. 개발자 커뮤니티에서 주로 쓴다.

### Design Aesthetics

시대적 시각 문화와 연결하여 스타일을 분류하는 용어. Y2K Futurism, Vaporwave, Retro Futurism처럼 특정 시대의 문화적 감성을 반영하는 스타일을 지칭한다. 디자인 비평, 트렌드 분석에서 주로 쓴다.

---

## A. 핵심 Morphism 계열 (9종)

### 1. Skeuomorphism (스큐어모피즘)

물리 사물의 질감, 광택, 입체감을 디지털 인터페이스에 사실적으로 모방하는 스타일. iPhone 초기(2007)부터 iOS 6(2013)까지 Apple이 주도했다. 가죽 텍스처의 캘린더, 나무결 책장, 광택 버튼 등이 대표적이다.

**핵심 시각 특성**

- 사실적 텍스처 (가죽, 나무, 금속, 종이)
- 다층 그림자와 하이라이트로 깊이 표현
- 반사광(specular highlight)과 광택(gloss)
- 물리 사물과 1:1 대응하는 아이콘/UI 메타포
- 높은 디테일 밀도, 풍부한 그라데이션

**CSS 구현 핵심**

```css
/* 입체 버튼 */
.skeu-button {
  background: linear-gradient(180deg, #f7f7f7 0%, #d4d4d4 100%);
  border: 1px solid #a0a0a0;
  border-radius: 8px;
  box-shadow:
    0 1px 3px rgba(0,0,0,0.3),
    inset 0 1px 0 rgba(255,255,255,0.8);
  text-shadow: 0 1px 0 rgba(255,255,255,0.6);
}

/* 텍스처 배경 */
.skeu-surface {
  background-image: url('leather-texture.png');
  background-size: cover;
}
```

**시기:** 2007-2013 (주류), 이후 간헐적 복고

**대표 사례:** iOS 1-6, Apple iBooks 나무 책장, 초기 Instagram 아이콘, Samsung TouchWiz

---

### 2. Flat Design (플랫 디자인)

Skeuomorphism의 반작용으로 등장. 모든 장식적 요소(그림자, 그라데이션, 텍스처)를 제거하고 단색, 기하학적 형태, 타이포그래피에 집중한다. 콘텐츠 자체가 인터페이스라는 철학이다.

**핵심 시각 특성**

- 그림자, 그라데이션, 텍스처 완전 배제
- 선명한 단색(solid color) 블록
- 심플한 기하학적 아이콘
- 산세리프 타이포그래피 강조
- 명확한 색상 대비로 계층 구분

**CSS 구현 핵심**

```css
.flat-card {
  background: #3498db;
  color: #ffffff;
  border: none;
  border-radius: 0;
  box-shadow: none;
  padding: 16px 24px;
}

.flat-button {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 2px;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.5px;
}
```

**시기:** 2012-2015 (주류), Microsoft Metro가 선구

**대표 사례:** iOS 7 (2013), Windows 8 Metro, Google 2013 리디자인

---

### 3. Flat 2.0 / Semi-Flat (세미 플랫)

순수 Flat Design의 사용성 문제(클릭 가능 여부 구분 불가)를 해결하기 위해 미세한 그림자와 그라데이션을 재도입한 절충안. "Almost Flat Design"이라고도 부른다. 현재 대부분의 주류 UI가 이 범주에 속한다.

**핵심 시각 특성**

- 미묘한 그림자(subtle shadow)로 elevation 암시
- 미세한 그라데이션으로 깊이감 부여
- Flat의 단순함 유지 + 최소한의 시각적 단서
- 인터랙티브 요소에만 선택적 그림자 적용
- 아이콘은 여전히 단순 기하학 유지

**CSS 구현 핵심**

```css
.semi-flat-card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.semi-flat-button {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(102,126,234,0.25);
}
```

**시기:** 2014-현재 (사실상 주류 기본값)

**대표 사례:** Apple iOS 10+, Airbnb, Dropbox, Stripe 대시보드

---

### 4. Material Design (머티리얼 디자인)

Google이 2014년 발표한 디자인 시스템. "종이와 잉크" 메타포에 기반하며 elevation(높이)으로 계층을 표현한다. 명확한 가이드라인과 컴포넌트 라이브러리를 제공하여 일관된 크로스 플랫폼 경험을 추구한다.

**핵심 시각 특성**

- Elevation 기반 그림자 시스템 (0dp-24dp)
- 종이 레이어 메타포: 카드가 표면 위에 떠있는 듯한 표현
- Bold 컬러 팔레트 + 의미론적 컬러 역할
- Ripple 효과(터치 피드백)
- 8dp 그리드 시스템
- Material 3에서 Dynamic Color 도입

**CSS 구현 핵심**

```css
/* Elevation 단계 */
.elevation-1 { box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); }
.elevation-2 { box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23); }
.elevation-4 { box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23); }
.elevation-8 { box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22); }

/* Ripple 효과 */
.ripple {
  position: relative;
  overflow: hidden;
}
.ripple::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
  transform: scale(0);
  animation: ripple 0.6s linear;
}
```

**시기:** 2014-현재 (Material 1 → 2 → 3로 진화)

**대표 사례:** Android OS, Google Workspace, Flutter 기본 테마

---

### 5. Neumorphism / Soft UI (뉴모피즘)

배경과 동일한 색조의 요소에 밝은 그림자(상단-좌측)와 어두운 그림자(하단-우측)를 동시에 적용하여 요소가 표면에서 볼록하게 솟거나 오목하게 눌린 것처럼 보이게 하는 스타일. 시각적으로 매력적이나 접근성 문제(낮은 대비)로 전면 채택은 드물다.

**핵심 시각 특성**

- 배경과 동색조(monochromatic) 요소
- 이중 그림자: 밝은 쪽(빛) + 어두운 쪽(그림자)
- 볼록(convex) / 오목(concave) / 평면(flat) 3가지 상태
- 부드럽고 뭉근한(soft) 그림자 반경
- 최소한의 색상 변화, 단색 팔레트

**CSS 구현 핵심**

```css
:root {
  --bg: #e0e5ec;
  --shadow-dark: #a3b1c6;
  --shadow-light: #ffffff;
}

/* 볼록 (Raised) */
.neu-raised {
  background: var(--bg);
  border-radius: 16px;
  box-shadow:
    8px 8px 16px var(--shadow-dark),
    -8px -8px 16px var(--shadow-light);
}

/* 오목 (Pressed/Inset) */
.neu-pressed {
  background: var(--bg);
  border-radius: 16px;
  box-shadow:
    inset 8px 8px 16px var(--shadow-dark),
    inset -8px -8px 16px var(--shadow-light);
}

/* 볼록 + 오목 결합 (Toggle) */
.neu-toggle:active {
  box-shadow:
    inset 4px 4px 8px var(--shadow-dark),
    inset -4px -4px 8px var(--shadow-light);
}
```

**시기:** 2019-2021 (유행), 이후 부분적 사용

**대표 사례:** Dribbble 컨셉 디자인 다수, Tesla 앱 (부분 적용), 일부 스마트홈 앱

> **접근성 주의:** 요소 경계가 그림자로만 구분되므로 WCAG 대비비 3:1을 충족하기 어렵다. 보조 수단(아이콘, 텍스트 라벨, 포커스 링)을 반드시 병행한다.

---

### 6. Glassmorphism (글래스모피즘)

프로스티드 글라스(frosted glass) 효과. 반투명 배경 + 블러 + 미세한 보더로 유리판 뒤의 콘텐츠가 비쳐 보이는 듯한 느낌을 만든다. Apple의 macOS Big Sur(2020)가 대중화를 이끌었다.

**핵심 시각 특성**

- `backdrop-filter: blur()` 기반 반투명 레이어
- 배경 콘텐츠가 블러되어 비침
- 미세한 반투명 보더 (1px, white/10-20%)
- 미묘한 그림자로 레이어 분리
- 밝은 그라데이션 배경과 함께 사용 시 효과 극대화

**CSS 구현 핵심**

```css
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* 다크 모드 변형 */
.glass-card-dark {
  background: rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* 그라데이션 배경과 조합 */
.glass-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**시기:** 2020-현재

**대표 사례:** macOS Big Sur/Ventura, iOS Control Center, Windows 11, Linear, Vercel

> **접근성 주의:** 블러 강도가 약하면 뒤 콘텐츠와 혼동될 수 있다. `blur(8px)` 이상 권장. 텍스트 가독성을 위해 배경 불투명도를 충분히 확보한다.

---

### 7. Claymorphism (클레이모피즘)

3D 렌더링의 통통한 클레이(점토) 질감을 UI에 적용한 스타일. 둥글고 부드러운 형태, 파스텔 또는 비비드 컬러, 이중 그림자로 카툰 같은 친근함을 표현한다.

**핵심 시각 특성**

- 크고 둥근 border-radius (20px+)
- 이중 외부 그림자 (부드럽게 떠있는 듯한 느낌)
- 내부 그림자로 볼록한 표면감
- 파스텔 또는 비비드 컬러 팔레트
- 3D 일러스트레이션과 자주 조합

**CSS 구현 핵심**

```css
.clay-card {
  background: #f0e6ff;
  border-radius: 24px;
  box-shadow:
    8px 8px 24px rgba(0, 0, 0, 0.15),
    inset -4px -4px 8px rgba(0, 0, 0, 0.05),
    inset 4px 4px 8px rgba(255, 255, 255, 0.6);
}

.clay-button {
  background: #a78bfa;
  color: white;
  border: none;
  border-radius: 16px;
  box-shadow:
    6px 6px 16px rgba(0, 0, 0, 0.2),
    inset -2px -2px 6px rgba(0, 0, 0, 0.1),
    inset 2px 2px 6px rgba(255, 255, 255, 0.4);
}
```

**시기:** 2021-2022 (유행), 이후 3D 일러스트 맥락에서 간헐적 사용

**대표 사례:** Figma 커뮤니티 플러그인 UI, 일부 랜딩 페이지, 3D 캐릭터 기반 앱

---

### 8. Liquid Glass (리퀴드 글라스)

Apple이 iOS 26(2025)에서 도입한 차세대 UI 스타일. Glassmorphism을 확장하여 실시간 굴절(refraction), 반사(reflection), 광학 왜곡을 시뮬레이션한다. 유리가 아닌 액체 유리 렌즈처럼 뒤의 콘텐츠가 미세하게 왜곡되어 보인다.

**핵심 시각 특성**

- 실시간 굴절 효과 (콘텐츠가 렌즈처럼 왜곡)
- 동적 반사광 (디바이스 기울기/시선에 반응)
- 다층 투명도와 깊이감
- 시스템 전체에 일관 적용되는 재질(material) 시스템
- Glassmorphism보다 높은 시각적 복잡도

**CSS 구현 핵심**

```css
/* 웹에서의 근사 구현 — 완전한 Liquid Glass는 OS 네이티브 렌더링 필요 */
.liquid-glass {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(20px) saturate(180%) brightness(1.1);
  -webkit-backdrop-filter: blur(20px) saturate(180%) brightness(1.1);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 20px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  /* 미세 왜곡은 SVG filter로 근사 가능 */
}

/* 굴절 근사 (SVG filter) */
.liquid-glass-refraction {
  filter: url(#refraction-filter);
}
```

**시기:** 2025-현재

**대표 사례:** iOS 26, iPadOS 26, macOS Tahoe, watchOS 26

---

### 9. Artificial Morphism (아티피셜 모피즘)

AI 생성 텍스처와 패턴을 UI 표면에 적용하는 실험적 스타일. Neumorphism의 그림자 기법과 Skeuomorphism의 질감 표현을 결합하되, AI가 생성한 비현실적이거나 초현실적인 텍스처를 사용한다.

**핵심 시각 특성**

- AI 생성 텍스처/패턴 (절차적 생성, diffusion 기반)
- Neumorphism식 이중 그림자 + Skeuomorphism식 표면 질감
- 비현실적이면서도 촉각적인(tactile) 표면
- 고해상도 프로시저럴 노이즈
- 개인화된 동적 텍스처 변형 가능

**CSS 구현 핵심**

```css
.artificial-surface {
  /* AI 생성 텍스처를 배경 이미지로 적용 */
  background-image: url('ai-generated-texture.webp');
  background-size: cover;
  border-radius: 16px;
  box-shadow:
    6px 6px 12px rgba(0,0,0,0.15),
    -6px -6px 12px rgba(255,255,255,0.8);
  /* 또는 CSS Houdini Paint API로 절차적 생성 */
}

/* CSS Paint API 활용 (실험적) */
@supports (background: paint(artificialTexture)) {
  .artificial-surface {
    background: paint(artificialTexture);
    --texture-seed: 42;
    --texture-complexity: 0.7;
  }
}
```

**시기:** 2024-현재 (실험적)

**대표 사례:** 디자인 컨셉/프로토타입 단계, AI 네이티브 앱 인터페이스, Figma AI 플러그인 데모

---

## B. 타이포/레이아웃 기반 (6종)

### 10. Brutalism (브루탈리즘)

건축의 Brutalism(béton brut = 날것의 콘크리트)에서 차용. 의도적으로 "못생긴", 투박한, 가공하지 않은 느낌의 디자인. 세련됨을 거부하고 기능과 구조를 날것 그대로 드러낸다.

**핵심 시각 특성**

- 시스템 기본 폰트(Courier, Times New Roman, Arial)
- 의도적으로 깨진 듯한 레이아웃
- 검정 배경 + 흰색 텍스트 또는 극단적 색상 조합
- 장식 요소 부재, HTML 기본 스타일 노출
- 호버 효과 최소화 또는 과격한 전환
- 그리드 무시 또는 의도적 파괴

**CSS 구현 핵심**

```css
.brutal-page {
  font-family: 'Courier New', monospace;
  background: #000;
  color: #fff;
  margin: 0;
  padding: 20px;
}

.brutal-link {
  color: #00ff00;
  text-decoration: underline;
  font-size: 24px;
}

.brutal-block {
  border: 3px solid #fff;
  padding: 10px;
  margin: 10px 0;
}
```

**시기:** 2014-2018 (웹 디자인 유행), 계속 니치 존재

**대표 사례:** Craigslist, Bloomberg Businessweek (실험적 에디션), hfrn.art, Yale School of Art 사이트

---

### 11. Neubrutalism (뉴브루탈리즘)

Brutalism의 정신을 계승하되 더 접근 가능하고 쾌활한 방향으로 재해석. 두꺼운 검정 아웃라인, 하드 드롭 셰도우, 비비드 컬러가 특징이다. "Cartoon Brutalism"이라고도 부른다.

**핵심 시각 특성**

- 두꺼운 검정 보더 (2-4px solid black)
- 하드 드롭 셰도우 (블러 없는 오프셋 그림자)
- 비비드/네온 배경색
- 명확한 컴포넌트 경계
- 핸드드로잉 또는 조악한(lo-fi) 일러스트
- 과감한 타이포그래피

**CSS 구현 핵심**

```css
.neubr-card {
  background: #fee440;
  border: 3px solid #000;
  border-radius: 8px;
  box-shadow: 6px 6px 0 #000;
  padding: 24px;
}

.neubr-button {
  background: #a855f7;
  color: #000;
  border: 3px solid #000;
  border-radius: 8px;
  box-shadow: 4px 4px 0 #000;
  font-weight: 800;
  padding: 12px 24px;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.1s;
}

.neubr-button:active {
  transform: translate(4px, 4px);
  box-shadow: 0 0 0 #000;
}
```

**시기:** 2020-현재

**대표 사례:** Gumroad, Figma 일부 마케팅 페이지, Notion 템플릿, 많은 인디 SaaS 랜딩

---

### 12. Swiss / International Style (스위스/국제 타이포그래피)

1950년대 스위스에서 시작된 그래픽 디자인 운동. 수학적 그리드, 산세리프 타이포그래피(특히 Helvetica), 객관적 사진, 비대칭 레이아웃을 통한 "보편적 커뮤니케이션"을 추구한다.

**핵심 시각 특성**

- 엄격한 수학적 그리드 시스템
- Helvetica, Univers 등 네오그로테스크 산세리프
- 좌측 정렬(ragged right) 텍스트
- 비대칭이되 규칙적인 레이아웃
- 장식 배제, 정보 전달 우선
- 사진은 오브젝티브(연출 없음)

**CSS 구현 핵심**

```css
.swiss-layout {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.swiss-heading {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  text-align: left;
}

.swiss-body {
  font-size: 16px;
  line-height: 1.6;
  max-width: 60ch;
  text-align: left;
}
```

**시기:** 1950s 원형, 웹 디자인에서 지속적 영향

**대표 사례:** 원형 — Neue Grafik 매거진. 현대 — Apple 제품 페이지, 많은 에이전시 포트폴리오

---

### 13. Bento Grid (벤토 그리드)

일본 도시락(弁当)의 칸막이 구조에서 영감. 다양한 크기의 모듈 카드를 비대칭적으로 배치하여 대시보드, 기능 소개, 포트폴리오를 구성한다. Apple이 2023년 제품 발표에서 대중화했다.

**핵심 시각 특성**

- 다양한 크기의 직사각형 카드 조합 (1x1, 2x1, 2x2 등)
- 각 카드는 독립적 콘텐츠 단위
- 일정한 gap으로 구분 (보더 없이 여백만으로)
- 둥근 모서리 (12-20px)
- 카드 내부에 아이콘/숫자/그래프 등 단일 정보
- 스크롤 없이 한 화면에 핵심 정보 개요

**CSS 구현 핵심**

```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 16px;
  padding: 16px;
}

.bento-item {
  background: #f5f5f7;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* 2x2 대형 카드 */
.bento-item--large {
  grid-column: span 2;
  grid-row: span 2;
}

/* 2x1 와이드 카드 */
.bento-item--wide {
  grid-column: span 2;
}
```

**시기:** 2023-현재

**대표 사례:** Apple WWDC 2023 키노트, Apple 제품 페이지, Linear, 많은 SaaS 피처 소개 페이지

---

### 14. Maximalism (맥시멀리즘)

미니멀리즘의 반대. 패턴, 이미지, 텍스처, 컬러, 타이포그래피를 풍부하게 겹쳐 시각적 풍요로움을 추구한다. "More is more." 정보 과잉을 두려워하지 않고 감각적 자극을 극대화한다.

**핵심 시각 특성**

- 빈 공간 최소화, 모든 영역에 시각 요소
- 다수의 컬러와 패턴 중첩
- 혼합 타이포그래피 (여러 서체 동시 사용)
- 장식적 일러스트레이션, 사진, 텍스처 혼합
- 레이어링과 콜라주 기법
- 의도적 시각적 긴장감

**CSS 구현 핵심**

```css
.maxi-section {
  background:
    url('pattern-1.svg') repeat,
    linear-gradient(135deg, #ff6b6b 0%, #feca57 50%, #48dbfb 100%);
  background-blend-mode: overlay;
  color: #fff;
  padding: 60px;
}

.maxi-heading {
  font-family: 'Playfair Display', serif;
  font-size: 72px;
  text-shadow: 4px 4px 0 #000;
  mix-blend-mode: difference;
}

.maxi-accent {
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 4px;
}
```

**시기:** 2022-현재 (미니멀리즘 피로감 반작용)

**대표 사례:** 패션 브랜드 사이트(Gucci, Balenciaga), 음악 페스티벌 사이트, 일부 에디토리얼 매거진

---

### 15. Minimalism (미니멀리즘)

불필요한 요소를 제거하고 본질에 집중하는 디자인 철학. "Less is more." 넓은 여백, 제한된 컬러 팔레트, 명확한 타이포그래피로 콘텐츠가 스스로 말하게 한다.

**핵심 시각 특성**

- 넓은 여백(whitespace) 적극 활용
- 제한된 컬러 (2-3색)
- 하나의 산세리프 서체군
- 명확한 시각적 계층
- 장식 요소 최소화
- 콘텐츠 중심 레이아웃

**CSS 구현 핵심**

```css
.minimal-layout {
  max-width: 680px;
  margin: 0 auto;
  padding: 80px 24px;
  font-family: 'Inter', sans-serif;
  color: #1a1a1a;
  line-height: 1.7;
}

.minimal-heading {
  font-size: 36px;
  font-weight: 600;
  margin-bottom: 24px;
  letter-spacing: -0.02em;
}

.minimal-divider {
  border: none;
  border-top: 1px solid #e5e5e5;
  margin: 48px 0;
}
```

**시기:** 2010s-현재 (상시 주류)

**대표 사례:** Apple.com, Medium, Notion, Everlane, 대부분의 블로그 플랫폼

---

## C. 레트로/노스탤지어 (7종)

### 16. Frutiger Aero (프루티거 에어로)

Windows Vista/7 시대(2004-2013)의 시각적 감성. 광택 있는 UI, 자연 이미지(풀밭, 물방울, 꽃), 파란 하늘, 보케 효과, Segoe UI(Frutiger 계열) 폰트가 특징이다. 2023년 이후 Z세대의 노스탤지어와 함께 복고 유행이 나타났다.

**핵심 시각 특성**

- 글로시(glossy) 아이콘과 버튼
- 자연 이미지 배경 (초원, 물, 하늘)
- 보케(bokeh) 효과와 렌즈 플레어
- Frutiger 계열 산세리프(Segoe UI, Myriad Pro)
- 투명/반투명 유리 효과 (Aero Glass)
- 밝고 낙관적인 컬러 톤

**CSS 구현 핵심**

```css
.frutiger-aero-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.frutiger-aero-bg {
  background:
    radial-gradient(circle at 30% 50%, rgba(255,255,255,0.3) 0%, transparent 60%),
    url('nature-meadow.jpg') center/cover;
}

.frutiger-aero-button {
  background: linear-gradient(180deg, #7ec8e3 0%, #4a9fd5 100%);
  border: 1px solid #3a8bc2;
  border-radius: 4px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.5);
  color: white;
  text-shadow: 0 -1px 0 rgba(0,0,0,0.2);
}
```

**시기:** 2004-2013 (원형), 2023-현재 (복고)

**대표 사례:** Windows Vista/7 Aero, MSN Messenger, 2000년대 후반 Nokia 앱 UI

---

### 17. Y2K Futurism (Y2K 퓨처리즘)

1997-2004년 밀레니엄 전후의 미래지향적 디자인. 크롬/메탈릭 표면, 투명 플라스틱(iMac G3), 유기적 블롭(blob) 형태, 사이버 느낌의 타이포그래피가 특징이다. 2021년 이후 복고 유행이 활발하다.

**핵심 시각 특성**

- 크롬/메탈릭 반사 텍스처
- 투명 젤리/플라스틱 느낌의 UI 요소
- 유기적 블롭(blob) 형태
- 사이버/테크 느낌의 서체
- 실버, 라벤더, 아쿠아, 라임 등의 컬러
- 3D 렌더링 오브젝트와 혼합

**CSS 구현 핵심**

```css
.y2k-element {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 30%, #a0a0a0 60%, #d0d0d0 100%);
  border: 2px solid #808080;
  border-radius: 50px;
  box-shadow:
    0 4px 12px rgba(0,0,0,0.3),
    inset 0 2px 4px rgba(255,255,255,0.8);
}

.y2k-blob {
  background: linear-gradient(135deg, #7afcff 0%, #feff9c 50%, #ff7eb3 100%);
  border-radius: 60% 40% 70% 30% / 50% 60% 40% 50%;
  filter: blur(0.5px);
}

.y2k-text {
  font-family: 'Eurostile', 'Bank Gothic', sans-serif;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: #c0c0c0;
  text-shadow: 0 0 8px rgba(192, 192, 192, 0.5);
}
```

**시기:** 1997-2004 (원형), 2021-현재 (복고)

**대표 사례:** 원형 — iMac G3, PlayStation 2 UI, 초기 Flash 사이트. 복고 — Charli XCX 앨범 아트, Olivia Rodrigo 머천다이즈

---

### 18. Retro Futurism (레트로 퓨처리즘 / 신스웨이브)

1980년대 SF 영화의 미학. 네온 글로우, 원근법 그리드, 석양 그라데이션, 신디사이저 음악 문화와 연결된다. Synthwave/Outrun이라고도 부른다.

**핵심 시각 특성**

- 네온 핑크/시안/퍼플 글로우
- 원근법 그리드 (소실점을 향한 격자)
- 크롬 텍스트와 메탈릭 반사
- 석양 그라데이션 (핫핑크 → 오렌지 → 퍼플)
- 다크 배경 (남색/검정)
- 팜트리, 스포츠카, 네온사인 모티프

**CSS 구현 핵심**

```css
.retro-futurism-bg {
  background: linear-gradient(180deg, #0a0015 0%, #1a0030 40%, #ff6ec7 70%, #ff9a3c 100%);
  perspective: 800px;
}

.retro-grid {
  background-image:
    linear-gradient(rgba(255, 110, 199, 0.3) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 110, 199, 0.3) 1px, transparent 1px);
  background-size: 40px 40px;
  transform: rotateX(60deg);
  transform-origin: center top;
}

.retro-chrome-text {
  font-family: 'Audiowide', cursive;
  background: linear-gradient(180deg, #fff 0%, #aaa 40%, #fff 50%, #888 60%, #ddd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(255, 110, 199, 0.5);
}
```

**시기:** 1980s SF 원형, 2010s-현재 (복고 운동)

**대표 사례:** Hotline Miami, Far Cry 3: Blood Dragon, Kavinsky 앨범 아트, Tesla Cybertruck 발표

---

### 19. Vaporwave (베이퍼웨이브)

2010년대 인터넷 서브컬처. 핑크/틸/라벤더 컬러, 그리스-로마 석상, 일본어 텍스트, VHS 글리치, Windows 95/98 UI 요소를 콜라주한다. 소비주의와 디지털 문화에 대한 풍자적 태도가 깔려 있다.

**핵심 시각 특성**

- 핑크/틸/라벤더/사이버 퍼플 팔레트
- 그리스-로마 석상, 돌고래, 팜트리
- 일본어/한자 텍스트 (맥락 없이 장식적)
- VHS 글리치/스캔라인/색수차 효과
- Windows 95/98 UI 요소 콜라주
- 체커보드 바닥, 3D 렌더링 오브젝트

**CSS 구현 핵심**

```css
.vaporwave-bg {
  background: linear-gradient(180deg, #ff71ce 0%, #01cdfe 50%, #05ffa1 100%);
}

/* VHS 스캔라인 */
.vaporwave-scanlines::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    rgba(0, 0, 0, 0.1) 1px,
    transparent 2px,
    transparent 4px
  );
  pointer-events: none;
}

/* 글리치 텍스트 */
.vaporwave-glitch {
  font-family: 'MS PGothic', 'Arial', sans-serif;
  color: #ff71ce;
  text-shadow:
    2px 0 #01cdfe,
    -2px 0 #b967ff;
  animation: glitch 0.3s infinite alternate;
}

@keyframes glitch {
  0% { text-shadow: 2px 0 #01cdfe, -2px 0 #b967ff; }
  100% { text-shadow: -2px 0 #01cdfe, 2px 0 #b967ff; }
}
```

**시기:** 2010s (서브컬처), 2015-현재 (디자인 차용)

**대표 사례:** Macintosh Plus — Floral Shoppe 앨범 아트, Reddit r/VaporwaveAesthetics, 다수의 인디 게임

---

### 20. Cyberpunk (사이버펑크)

근미래 디스토피아의 시각 언어. 어두운 배경에 강렬한 네온 글로우, 산업적 텍스처, 글리치 효과, HUD(Heads-Up Display) 스타일 UI 요소가 특징이다.

**핵심 시각 특성**

- 다크 배경 (거의 검정 + 약간의 남색/군청)
- 강렬한 네온 글로우 (시안, 마젠타, 일렉트릭 블루)
- 산업/기계 텍스처 (금속, 콘크리트, 와이어)
- 글리치/디지털 노이즈 효과
- HUD 스타일 데이터 표시 (각진 프레임, 모서리 장식)
- 모노스페이스 폰트 + 일본어 혼합

**CSS 구현 핵심**

```css
.cyber-card {
  background: rgba(10, 10, 30, 0.9);
  border: 1px solid #00f0ff;
  clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 16px 100%, 0 calc(100% - 16px));
  padding: 24px;
  color: #e0e0e0;
}

.cyber-glow-text {
  color: #00f0ff;
  text-shadow:
    0 0 4px #00f0ff,
    0 0 12px #00f0ff,
    0 0 24px rgba(0, 240, 255, 0.5);
  font-family: 'Share Tech Mono', monospace;
}

/* 각진 보더 장식 */
.cyber-corner::before,
.cyber-corner::after {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  border: 2px solid #ff003c;
}
.cyber-corner::before { top: -2px; left: -2px; border-right: none; border-bottom: none; }
.cyber-corner::after { bottom: -2px; right: -2px; border-left: none; border-top: none; }
```

**시기:** 1980s 문학 원형 (William Gibson), 2010s-현재 (디자인 트렌드)

**대표 사례:** Cyberpunk 2077, Blade Runner 2049 프로모션, GMUNK 포트폴리오

---

### 21. Memphis Design (멤피스 디자인)

1981년 이탈리아 밀라노에서 Ettore Sottsass가 이끈 Memphis Group에서 시작. 모더니즘의 "좋은 디자인" 규범을 거부하고 대담한 기하학 패턴, 원색과 파스텔의 충돌, 비대칭 구성을 추구했다.

**핵심 시각 특성**

- 대담한 기하학 패턴 (지그재그, 물방울, 삼각형)
- 원색(빨강/파랑/노랑)과 파스텔 동시 사용
- 두꺼운 검정 아웃라인
- 비대칭/비정형 레이아웃
- 테라초(terrazzo) 패턴
- 의도적 "충돌"하는 컬러 조합

**CSS 구현 핵심**

```css
/* 테라초 패턴 */
.memphis-terrazzo {
  background-color: #fce4ec;
  background-image:
    radial-gradient(circle 4px, #ff5252 99%, transparent 100%),
    radial-gradient(circle 3px, #448aff 99%, transparent 100%),
    radial-gradient(circle 5px, #ffeb3b 99%, transparent 100%),
    radial-gradient(circle 2px, #000 99%, transparent 100%);
  background-size: 80px 80px;
  background-position: 0 0, 30px 40px, 60px 20px, 10px 60px;
}

.memphis-heading {
  font-family: 'Rubik', sans-serif;
  font-weight: 900;
  color: #ff5252;
  -webkit-text-stroke: 2px #000;
}

.memphis-zigzag {
  background: repeating-linear-gradient(
    135deg,
    #ffeb3b 0px, #ffeb3b 10px,
    #000 10px, #000 12px,
    #448aff 12px, #448aff 22px,
    #000 22px, #000 24px
  );
}
```

**시기:** 1981-1988 (원형), 2010s-현재 (복고)

**대표 사례:** 원형 — Sottsass Carlton 책장, David Bowie 앨범 아트. 현대 — Slack 초기 브랜딩, 다수의 그래픽 디자인 포트폴리오

---

### 22. Corporate Memphis / Alegria (코퍼레이트 멤피스)

Facebook(현 Meta)의 Alegria 디자인 시스템에서 유래한 이름. 긴 팔다리, 비현실적 신체 비율, 단순한 얼굴의 플랫 일러스트 스타일. 2017-2023년 SaaS/빅테크 마케팅을 지배했다. 이후 "bland corporate art"이라는 비판과 함께 퇴조했다.

**핵심 시각 특성**

- 비현실적으로 긴 팔다리와 작은 머리
- 단순화된 얼굴 (점 눈, 미니멀 표정)
- 파스텔 또는 비비드 단색 피부
- 그라데이션 배경과 플랫 오브젝트
- 다양성 표현을 위한 비자연적 피부색 (파랑, 보라 등)
- 화이트스페이스와 결합한 깔끔한 구성

**CSS 구현 핵심**

```css
/* Corporate Memphis는 주로 SVG 일러스트로 구현. CSS는 배경과 레이아웃 담당 */
.corp-memphis-hero {
  background: linear-gradient(135deg, #e0f7ff 0%, #fff0e6 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 80px 120px;
}

.corp-memphis-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}

.corp-memphis-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 20px;
  line-height: 1.6;
  color: #2d3748;
}
```

**시기:** 2017-2023 (주류, 현재 퇴조)

**대표 사례:** Facebook/Meta Alegria, Slack, Mailchimp, Google Workspace, Dropbox (2017-2020 시기)

---

## D. 컬러/표면 효과 (8종)

### 23. Aurora UI (오로라 UI)

다색 메시 그라데이션으로 오로라(북극광)와 유사한 몽환적 배경을 만드는 스타일. 부드럽게 흐르는 여러 색상이 유기적으로 혼합되어 깊이감과 움직임을 암시한다.

**핵심 시각 특성**

- 다색 메시 그라데이션 (3-5색)
- 부드럽게 흐르는 색상 전환
- 몽환적/꿈같은 분위기
- 블러 처리된 컬러 블롭 중첩
- 어두운 배경 위 발광하는 색상
- 미니멀 UI 요소와 조합

**CSS 구현 핵심**

```css
.aurora-bg {
  background: #0a0a1a;
  position: relative;
  overflow: hidden;
}

.aurora-bg::before {
  content: '';
  position: absolute;
  width: 150%;
  height: 150%;
  top: -25%;
  left: -25%;
  background:
    radial-gradient(circle at 20% 50%, rgba(120, 0, 255, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 80% 30%, rgba(0, 200, 255, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 50% 80%, rgba(0, 255, 150, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 70% 60%, rgba(255, 0, 128, 0.2) 0%, transparent 40%);
  filter: blur(60px);
  animation: aurora-drift 20s ease-in-out infinite alternate;
}

@keyframes aurora-drift {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(30px, -20px) rotate(3deg); }
}
```

**시기:** 2022-현재

**대표 사례:** Stripe 2022 리디자인, Linear, Vercel, 다수의 AI 스타트업 랜딩 페이지

---

### 24. Mesh Gradient (메시 그라데이션)

다수의 컬러 포인트가 유기적으로 블렌딩되는 그라데이션. 선형/원형 그라데이션과 달리 여러 색상 앵커가 2D 평면에 분포하여 자연스러운 색상 전환을 만든다.

**핵심 시각 특성**

- 4개 이상의 색상 포인트
- 비선형 색상 전환
- 부드러운 유기적 블렌딩
- 배경/카드 표면에 주로 적용
- Adobe Illustrator의 Mesh Gradient 도구 원형

**CSS 구현 핵심**

```css
/* 다중 radial-gradient로 근사 */
.mesh-gradient {
  background:
    radial-gradient(at 0% 0%, #ff9a9e 0%, transparent 50%),
    radial-gradient(at 100% 0%, #fecfef 0%, transparent 50%),
    radial-gradient(at 100% 100%, #a18cd1 0%, transparent 50%),
    radial-gradient(at 0% 100%, #fbc2eb 0%, transparent 50%),
    radial-gradient(at 50% 50%, #fad0c4 0%, transparent 60%);
  background-color: #ffecd2;
}

/* conic-gradient 활용 변형 */
.mesh-gradient-conic {
  background:
    conic-gradient(from 45deg at 30% 40%, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #ff6b6b),
    radial-gradient(circle at 70% 60%, rgba(255,255,255,0.3), transparent);
  filter: blur(40px);
}
```

**시기:** 2021-현재

**대표 사례:** Apple Music 앨범 배경, Instagram 로고 그라데이션, Figma Mesh Gradient 플러그인

---

### 25. Grain / Noise Texture (그레인/노이즈 텍스처)

디지털 표면에 아날로그 필름 그레인이나 종이 질감의 노이즈를 추가하여 촉감과 따뜻함을 부여하는 기법. 그라데이션의 밴딩(banding)을 해결하는 실용적 용도도 있다.

**핵심 시각 특성**

- 미세한 모노크롬 또는 컬러 노이즈
- 아날로그/필름 촉감
- 그라데이션과 조합 시 밴딩 방지
- 복고/핸드메이드 느낌 부여
- 불투명도 5-20%의 미묘한 적용

**CSS 구현 핵심**

```css
/* SVG filter 기반 노이즈 */
.grain-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.08'/%3E%3C/svg%3E");
  pointer-events: none;
  mix-blend-mode: overlay;
}

/* 또는 CSS 기반 (작은 영역에 적합) */
.grain-simple {
  background-image:
    url('noise-texture.png'),
    linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-blend-mode: overlay;
}
```

**시기:** 2021-현재

**대표 사례:** Gumroad, 많은 인디 브랜드 사이트, 일러스트레이션 포트폴리오

---

### 26. Duotone (듀오톤)

이미지나 UI 전체를 2가지 색상으로만 표현하는 기법. Spotify가 2015년 앨범 커버에 적용하면서 대중화되었다. 브랜드 아이덴티티를 강하게 부여하면서 시각적 통일감을 만든다.

**핵심 시각 특성**

- 2색 팔레트 (보통 대비되는 2색)
- 사진을 2색으로 맵핑 (그림자 → 색상A, 하이라이트 → 색상B)
- 강렬한 브랜드 인상
- 다양한 이미지에 일관된 톤 부여
- 히어로 이미지, 배경에 주로 활용

**CSS 구현 핵심**

```css
/* CSS filter + mix-blend-mode */
.duotone-container {
  position: relative;
  background: #2d1b69; /* 그림자 색상 */
}

.duotone-container img {
  filter: grayscale(100%) contrast(1.2);
  mix-blend-mode: multiply;
}

.duotone-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: #00d4ff; /* 하이라이트 색상 */
  mix-blend-mode: lighten;
}

/* SVG feColorMatrix 방식 (정밀 제어) */
/*
<filter id="duotone">
  <feColorMatrix type="matrix" values="
    0.2 0.2 0.2 0 0.18
    0.1 0.1 0.1 0 0.07
    0.4 0.4 0.4 0 0.41
    0   0   0   1 0" />
</filter>
*/
```

**시기:** 2016-현재

**대표 사례:** Spotify, Twitch, Adobe Creative Cloud 마케팅, VSCO

---

### 27. Holographic / Iridescent (홀로그래픽 / 이리데슨트)

보는 각도에 따라 색상이 변하는 무지갯빛 효과. 홀로그램 필름, 비눗방울, 진주 등 자연의 간섭 현상을 모방한다. 프리미엄/미래지향적 브랜딩에 사용된다.

**핵심 시각 특성**

- 각도/위치에 따라 변하는 다색 그라데이션
- 무지갯빛(rainbow) 색상 전환
- 프리즘 분산 효과
- 메탈릭/광택 표면과 자주 결합
- 마우스/스크롤 반응형 색상 변화

**CSS 구현 핵심**

```css
.holographic {
  background: linear-gradient(
    135deg,
    #ff0000 0%, #ff8000 14%,
    #ffff00 28%, #00ff00 42%,
    #00ffff 57%, #0000ff 71%,
    #8000ff 85%, #ff0080 100%
  );
  background-size: 200% 200%;
  animation: holo-shift 5s ease-in-out infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

@keyframes holo-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 카드 표면 홀로그래픽 */
.holo-card {
  background: linear-gradient(
    135deg,
    rgba(255,0,128,0.2), rgba(0,255,255,0.2),
    rgba(128,0,255,0.2), rgba(255,255,0,0.2)
  );
  background-size: 300% 300%;
  animation: holo-shift 8s ease infinite;
  backdrop-filter: blur(8px);
}
```

**시기:** 2020-현재

**대표 사례:** Apple Card 패키징, Nothing Phone 브랜딩, Chrome Hearts, 프리미엄 NFT 마켓플레이스

---

### 28. Metallic / Chrome (메탈릭 / 크롬)

금속 반사 표면(크롬, 실버, 골드, 로즈골드)을 시뮬레이션하는 스타일. 3D 렌더링 기술의 발전으로 웹에서도 실감나는 금속 질감 표현이 가능해졌다. Y2K 복고와 맞물려 2023년 이후 재유행 중이다.

**핵심 시각 특성**

- 다단계 선형 그라데이션으로 반사 시뮬레이션
- 하이라이트-그림자-하이라이트 반복 패턴
- 환경 맵핑(environment mapping) 효과
- 크롬(시안-실버), 골드(따뜻한 톤), 로즈골드 변형
- 3D 오브젝트와 자주 결합

**CSS 구현 핵심**

```css
/* 크롬 텍스트 */
.chrome-text {
  font-size: 72px;
  font-weight: 900;
  background: linear-gradient(
    180deg,
    #e8e8e8 0%, #b8b8b8 20%,
    #ffffff 25%, #a0a0a0 40%,
    #e0e0e0 50%, #808080 60%,
    #c0c0c0 70%, #ffffff 85%,
    #909090 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

/* 골드 표면 */
.gold-surface {
  background: linear-gradient(
    135deg,
    #bf953f 0%, #fcf6ba 25%,
    #b38728 50%, #fbf5b7 75%,
    #aa771c 100%
  );
}

/* 로즈골드 */
.rose-gold {
  background: linear-gradient(135deg, #b76e79 0%, #eacda3 50%, #d4a574 100%);
}
```

**시기:** 2023-현재 (Y2K 복고 영향)

**대표 사례:** Apple 제품 렌더링, 패션 브랜드 사이트, 프리미엄 주얼리 이커머스

---

### 29. Neon Glow (네온 글로우)

네온 사인의 발광 효과를 디지털로 재현. 다크 배경 위에 텍스트, 아이콘, 보더가 빛나는 듯한 효과를 만든다. `text-shadow`와 `box-shadow`의 다중 레이어가 핵심이다.

**핵심 시각 특성**

- 다크 배경 필수 (효과가 돋보이려면)
- 다층 text-shadow/box-shadow로 글로우 표현
- 네온관 특유의 색상 (핑크, 시안, 그린, 옐로우)
- 글로우 범위가 넓을수록 발광 강도 표현
- 간헐적 깜빡임 애니메이션 (선택)

**CSS 구현 핵심**

```css
.neon-text {
  color: #fff;
  text-shadow:
    0 0 4px #fff,
    0 0 8px #fff,
    0 0 16px #ff00de,
    0 0 32px #ff00de,
    0 0 64px #ff00de,
    0 0 80px #ff00de;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
}

.neon-border {
  border: 2px solid #00f0ff;
  border-radius: 8px;
  box-shadow:
    0 0 4px #00f0ff,
    0 0 12px #00f0ff,
    inset 0 0 4px #00f0ff;
}

/* 깜빡임 애니메이션 */
@keyframes neon-flicker {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; }
  20%, 24%, 55% { opacity: 0.6; }
}
.neon-flicker {
  animation: neon-flicker 3s infinite;
}
```

**시기:** 2019-현재

**대표 사례:** 바/레스토랑 사이트, 게임 UI, Cyberpunk 2077, 많은 나이트라이프 브랜딩

---

### 30. Dark Mode Design (다크 모드 디자인)

어두운 배경(#121212 등) 위에 밝은 전경 콘텐츠를 배치하는 시스템 수준의 디자인 패러다임. 단순히 색상을 반전하는 것이 아니라 elevation, 대비, 색상 채도를 체계적으로 조정해야 한다.

**핵심 시각 특성**

- 순수 검정(#000) 대신 짙은 회색(#121212, #1e1e1e) 사용
- Elevation이 높을수록 표면이 밝아지는 체계
- 텍스트 불투명도로 계층 표현 (87%, 60%, 38%)
- 채도를 낮춘(desaturated) 컬러 팔레트
- Primary 컬러는 밝은 톤 변형 사용
- 그림자 대신 elevation 오버레이로 깊이 표현

**CSS 구현 핵심**

```css
:root {
  /* Dark mode surface elevation */
  --surface-0: #121212;                          /* 0dp */
  --surface-1: color-mix(in srgb, #121212, white 5%);   /* 1dp */
  --surface-2: color-mix(in srgb, #121212, white 7%);   /* 2dp */
  --surface-3: color-mix(in srgb, #121212, white 8%);   /* 3dp */
  --surface-4: color-mix(in srgb, #121212, white 9%);   /* 4dp */
  --surface-8: color-mix(in srgb, #121212, white 12%);  /* 8dp */

  /* 텍스트 계층 */
  --text-high: rgba(255,255,255, 0.87);
  --text-medium: rgba(255,255,255, 0.60);
  --text-disabled: rgba(255,255,255, 0.38);
}

@media (prefers-color-scheme: dark) {
  body {
    background: var(--surface-0);
    color: var(--text-high);
  }
  .card {
    background: var(--surface-1);
    /* 다크 모드에서는 box-shadow 대신 surface 밝기로 elevation 표현 */
  }
}
```

**시기:** 2018-현재 (시스템 수준 지원: iOS 13, Android 10, macOS Mojave)

**대표 사례:** iOS/Android 시스템 다크 모드, GitHub, Twitter/X, Discord, VS Code

---

## E. 모션/인터랙션 (2종)

### 31. Kinetic Typography (키네틱 타이포그래피)

스크롤, 마우스, 시간에 반응하여 텍스트가 움직이고 변형되는 스타일. 텍스트 자체가 시각적 경험의 주인공이 된다. 포트폴리오, 에디토리얼, 브랜드 쇼케이스에서 주로 사용한다.

**핵심 시각 특성**

- 스크롤에 연동하여 텍스트 크기/위치/투명도 변화
- 마우스 커서에 반응하는 텍스트 왜곡/분산
- 글자별/단어별 순차 애니메이션 (stagger)
- 3D 변환, 회전, 원근법 적용
- 대형 타이포그래피 (72px+)

**CSS 구현 핵심**

```css
/* 스크롤 연동 텍스트 크기 변화 (Scroll-Driven Animation) */
.kinetic-heading {
  font-size: 120px;
  font-weight: 900;
  view-timeline-name: --heading;
  animation: scale-up both linear;
  animation-timeline: --heading;
  animation-range: entry 0% cover 50%;
}

@keyframes scale-up {
  from { transform: scale(0.5); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* 글자별 stagger — JS로 span 분리 후 CSS 적용 */
.kinetic-char {
  display: inline-block;
  animation: char-reveal 0.6s ease both;
  animation-delay: calc(var(--char-index) * 0.03s);
}

@keyframes char-reveal {
  from { transform: translateY(100%) rotate(10deg); opacity: 0; }
  to { transform: translateY(0) rotate(0); opacity: 1; }
}
```

**시기:** 2023-현재 (CSS Scroll-Driven Animations 지원 이후 가속)

**대표 사례:** Apple 제품 페이지 (텍스트 스크롤 효과), Locomotive Scroll 기반 사이트, 에이전시 포트폴리오

---

### 32. Parallax / Scroll-Driven Design (패럴랙스 / 스크롤 드리븐)

다층 요소가 서로 다른 속도로 스크롤되어 깊이감과 몰입감을 만드는 기법. 전경/중경/배경이 서로 다른 속도로 움직이면 시차(parallax) 효과가 발생한다.

**핵심 시각 특성**

- 다층 레이어 (전경/중경/배경)
- 레이어별 스크롤 속도 차이
- 3D 깊이감과 공간감
- 스크롤 위치에 따른 요소 등장/퇴장
- 스토리텔링과 결합한 순차적 정보 공개

**CSS 구현 핵심**

```css
/* CSS-only parallax (perspective 기반) */
.parallax-container {
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  perspective: 1px;
  perspective-origin: center center;
}

.parallax-bg {
  position: absolute;
  inset: 0;
  transform: translateZ(-2px) scale(3);
  z-index: -1;
}

.parallax-mid {
  transform: translateZ(-1px) scale(2);
}

.parallax-fg {
  transform: translateZ(0);
}

/* Scroll-Driven Animation API (모던 브라우저) */
.scroll-reveal {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}
```

**시기:** 2013-현재 (JS 라이브러리 시대 → 네이티브 CSS API 시대로 전환)

**대표 사례:** Apple 제품 스크롤 페이지, Firewatch 게임 사이트, Every Last Drop, 다수의 스토리텔링 사이트

---

## F. 플랫폼 특화 (3종)

### 33. Spatial Design (스페이셜 디자인)

Apple visionOS를 위한 3D 공간 UI 패러다임. 2D 윈도우가 3D 공간에 떠있으며, 시선 추적(eye tracking), 손 제스처, 깊이(depth)로 인터랙션한다. 기존 2D 디자인 원칙을 3차원으로 확장한 것이다.

**핵심 시각 특성**

- 글래스 머티리얼 윈도우 (주변 환경이 비침)
- Z축 깊이를 활용한 계층 구조
- 호버 → 시선(gaze) 피드백
- 둥근 모서리 + 동적 조명
- 볼류메트릭(3D) 콘텐츠와 2D 윈도우 혼합
- 미세한 그림자와 반사로 공간감 부여

**CSS 구현 핵심**

```css
/* 웹에서 Spatial 느낌 근사 */
.spatial-window {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px) saturate(150%);
  border: 0.5px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  box-shadow:
    0 16px 48px rgba(0, 0, 0, 0.15),
    0 2px 8px rgba(0, 0, 0, 0.1);
  transform: perspective(800px) rotateY(var(--rotate-y, 0deg));
  transition: transform 0.3s ease;
}

/* 시선/마우스 반응 (JS로 --rotate-y 업데이트) */
.spatial-window:hover {
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.2),
    0 4px 12px rgba(0, 0, 0, 0.15);
}

.spatial-icon {
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
  transform: translateZ(20px);
}
```

**시기:** 2023-현재

**대표 사례:** Apple visionOS, Apple Vision Pro 앱, Unity PolySpatial

---

### 34. Acrylic / Fluent Design (아크릴 / 플루언트 디자인)

Microsoft Fluent Design System의 핵심 머티리얼. 반투명 블러(Glassmorphism과 유사)에 노이즈 텍스처와 색상 틴트(tint)를 추가한다. Glassmorphism이 깨끗한 유리라면 Acrylic은 불투명한 젖빛 유리에 가깝다.

**핵심 시각 특성**

- 반투명 블러 + 노이즈 텍스처 결합
- 색상 틴트 레이어 (브랜드/테마 컬러)
- Glassmorphism보다 높은 불투명도
- 노이즈로 인한 "젖빛" 촉감
- Reveal Highlight (호버 시 빛 효과)
- 시스템 수준 Light/Dark 테마 연동

**CSS 구현 핵심**

```css
.acrylic {
  /* Tint 레이어 */
  background: rgba(32, 32, 32, 0.7);
  /* Blur 레이어 */
  backdrop-filter: blur(30px) saturate(125%);
  -webkit-backdrop-filter: blur(30px) saturate(125%);
  /* Noise 텍스처 */
  position: relative;
}

.acrylic::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  border-radius: inherit;
}

/* Reveal Highlight 효과 */
.acrylic-reveal {
  --mouse-x: 50%;
  --mouse-y: 50%;
  background-image: radial-gradient(
    circle at var(--mouse-x) var(--mouse-y),
    rgba(255,255,255,0.08) 0%,
    transparent 60%
  );
}
```

**시기:** 2017-현재

**대표 사례:** Windows 11, Microsoft Teams, Xbox 대시보드, Windows Terminal

---

### 35. Biomorphism (바이오모피즘)

자연의 유기적 형태(세포, 물결, 잎사귀, 산호)를 UI에 차용하는 스타일. 직선과 직각을 거부하고 부드러운 곡선, 불규칙한 형태, 자연 색상 팔레트로 친근하고 편안한 인터페이스를 만든다.

**핵심 시각 특성**

- 유기적/불규칙 곡선 형태
- 자연에서 영감받은 컬러 (그린, 어스톤, 옥색)
- blob 형태 (부드럽게 변형되는 비정형)
- 세포/조직/물결 패턴
- 직각/직선 최소화
- 자연스러운 그라데이션과 부드러운 전환

**CSS 구현 핵심**

```css
.bio-blob {
  border-radius: 60% 40% 70% 30% / 50% 60% 40% 60%;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  animation: morph 8s ease-in-out infinite;
}

@keyframes morph {
  0% { border-radius: 60% 40% 70% 30% / 50% 60% 40% 60%; }
  25% { border-radius: 40% 60% 30% 70% / 60% 40% 60% 40%; }
  50% { border-radius: 50% 50% 60% 40% / 40% 50% 50% 60%; }
  75% { border-radius: 70% 30% 40% 60% / 50% 60% 40% 50%; }
  100% { border-radius: 60% 40% 70% 30% / 50% 60% 40% 60%; }
}

.bio-container {
  clip-path: path('M0,50 C150,0 350,100 500,50 L500,400 L0,400 Z');
}

.bio-palette {
  --leaf: #2d6a4f;
  --moss: #52b788;
  --sand: #d4a373;
  --water: #a8dadc;
  --clay: #e07a5f;
}
```

**시기:** 2020s-현재

**대표 사례:** Headspace 앱, 환경/웰니스 브랜드 사이트, 일부 건강 앱 UI

---

## 시대별 흐름

```
2007 ──── Skeuomorphism 전성기 (iPhone 출시)
  │
2010 ──── Minimalism 부상
  │
2012 ──── Flat Design 등장 (Windows 8 Metro, iOS 7 예고)
  │
2013 ──── iOS 7 → Flat 전환 / Parallax 유행 시작
  │
2014 ──── Material Design 발표 / Flat 2.0 절충 / Brutalism 웹 등장
  │
2016 ──── Duotone (Spotify) / Swiss Style 웹 재해석
  │
2017 ──── Acrylic/Fluent Design (MS) / Corporate Memphis 확산
  │
2018 ──── Dark Mode 시스템 지원 시작 (macOS Mojave)
  │
2019 ──── Neumorphism 등장 / Neon Glow 유행
  │
2020 ──── Glassmorphism (macOS Big Sur) / Neubrutalism 등장
  │         Biomorphism, Holographic/Iridescent 부상
  │
2021 ──── Mesh Gradient / Grain Texture / Claymorphism
  │         Y2K 복고 유행 시작
  │
2022 ──── Aurora UI / Maximalism 반작용 / Memphis 복고
  │
2023 ──── Bento Grid (Apple) / Metallic/Chrome 재유행
  │         Frutiger Aero 복고 / Spatial Design (visionOS)
  │         Kinetic Typography 가속 (CSS Scroll-Driven)
  │
2024 ──── Artificial Morphism 실험 / AI 네이티브 인터페이스
  │
2025 ──── Liquid Glass (iOS 26) / Spatial Design 확장
  │
2026 ──── 현재: Liquid Glass + Aurora/Mesh 조합 트렌드
          Glassmorphism 계열의 지속적 진화
```

---

## design-kit 활용 가이드

### 컨셉 시안에 스타일 적용하기

컨셉 시안을 만들 때 각 스타일의 핵심 CSS 속성을 조합하여 룩앤필을 빠르게 전환할 수 있다. 단순히 색상만 바꾸는 것이 아니라 표면 처리(shadow, blur, border), 레이아웃 구조, 타이포그래피까지 달라져야 진정한 시안 차별화가 된다.

**표면 처리 기반 분류 (구현 관점)**

| 표면 처리 | 핵심 CSS 속성 | 해당 스타일 |
|-----------|--------------|------------|
| 그림자 깊이 | `box-shadow` 단계 | Material, Flat 2.0, Claymorphism |
| 이중 그림자 | `box-shadow` (light + dark) | Neumorphism |
| 하드 셰도우 | `box-shadow` (blur 0) | Neubrutalism |
| 블러 투명 | `backdrop-filter: blur()` | Glassmorphism, Liquid Glass, Acrylic, Spatial |
| 그라데이션 | `linear/radial/conic-gradient` | Aurora, Mesh, Metallic, Holographic |
| 텍스처 오버레이 | `background-image` + `mix-blend-mode` | Grain, Skeuomorphism, Acrylic |
| 글로우 발광 | `text-shadow`, `box-shadow` (넓은 blur) | Neon Glow, Cyberpunk, Retro Futurism |
| 보더 강조 | `border: 2-4px solid` | Neubrutalism, Brutalism, Memphis |
| 형태 왜곡 | `border-radius` 비정형, `clip-path` | Biomorphism, Y2K (blob) |
| 모션 연동 | `animation-timeline: view()` | Kinetic Typography, Parallax |

### 스타일 조합 가능성

단일 스타일을 그대로 적용하는 것보다 2-3개를 조합하면 더 독특하고 현대적인 결과물이 나온다. 단, 충돌하는 철학을 가진 스타일은 조합하지 않는다.

**검증된 조합**

| 조합 | 효과 | 적용 맥락 |
|------|------|----------|
| Glassmorphism + Aurora UI | 글라스 카드 뒤로 오로라 빛 투과 | SaaS 히어로 섹션, AI 제품 |
| Neubrutalism + Memphis | 두꺼운 보더 + 기하학 패턴 장식 | 크리에이티브/에디토리얼 |
| Dark Mode + Neon Glow | 다크 배경에서 네온 강조 | 게임, 나이트라이프, 테크 |
| Bento Grid + Glassmorphism | 벤토 카드에 글라스 재질 적용 | 대시보드, 제품 피처 소개 |
| Minimalism + Kinetic Typography | 여백 많은 레이아웃 + 움직이는 타이틀 | 포트폴리오, 에이전시 |
| Mesh Gradient + Grain Texture | 메시 그라데이션 위에 노이즈로 깊이감 | 랜딩 페이지 배경 |
| Liquid Glass + Spatial | 리퀴드 글라스 재질의 3D 공간 레이아웃 | visionOS 앱, 미래지향 UI |
| Flat 2.0 + Duotone | 깔끔한 UI + 듀오톤 이미지 처리 | 미디어, 음악 서비스 |

**충돌하는 조합 (피할 것)**

| 조합 | 충돌 이유 |
|------|----------|
| Skeuomorphism + Flat Design | 철학적 정반대 — 사실적 질감 vs 장식 제거 |
| Neumorphism + Neubrutalism | 미묘한 그림자 vs 강렬한 하드 셰도우, 시각적 혼란 |
| Brutalism + Minimalism | 의도적 투박함 vs 절제된 우아함, 톤 불일치 |
| Maximalism + Swiss Style | 시각적 풍요 vs 엄격한 그리드 규율, 양립 불가 |
| Corporate Memphis + Cyberpunk | 밝고 친근한 일러스트 vs 어두운 디스토피아, 세계관 충돌 |

### 접근성 고려사항

비주얼 스타일을 적용할 때 반드시 확인해야 할 접근성 체크리스트.

**1. 대비비 (Contrast Ratio)**

| 스타일 | 위험 요소 | 대응 |
|--------|----------|------|
| Neumorphism | 배경과 동색조 요소 → 경계 구분 불가 | 보조 보더 추가, 아이콘/라벨 병행 |
| Glassmorphism | 투명 배경 위 텍스트 가독성 저하 | 최소 blur(8px), 배경 불투명도 확보 |
| Neon Glow | 글로우가 텍스트 가장자리를 흐리게 함 | 본문이 아닌 제목/장식에만 적용 |
| Dark Mode | 순수 흰색(#fff) 텍스트 → 눈부심 | #e0e0e0 또는 87% 불투명도 사용 |
| Holographic | 색상 변화로 안정적 대비 확보 어려움 | 배경 전용, 텍스트 영역 분리 |

**2. 모션 감도 (Motion Sensitivity)**

```css
/* 모든 모션 스타일에 필수 적용 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Kinetic Typography, Parallax, Aurora(애니메이션), Holographic(색상 변화) 등 모션 의존 스타일은 `prefers-reduced-motion` 미디어 쿼리를 반드시 적용한다.

**3. 포커스 가시성 (Focus Visibility)**

```css
/* 모든 스타일에 공통 */
:focus-visible {
  outline: 2px solid var(--focus-color, #005fcc);
  outline-offset: 2px;
}
```

특히 Neumorphism, Glassmorphism처럼 경계가 모호한 스타일에서 포커스 링이 보이지 않으면 키보드 사용자가 현재 위치를 알 수 없다.

**4. 색상 의존 (Color Dependence)**

Duotone, Neon Glow, Aurora 등 색상 의존도가 높은 스타일에서는 색상만으로 정보를 전달하지 않아야 한다. 항상 텍스트 라벨, 아이콘, 패턴 등 보조 수단을 병행한다.

---

## 참고 자료

- [Neumorphism.io](https://neumorphism.io/) — Neumorphism CSS 생성기
- [Glassmorphism CSS Generator](https://hype4.academy/tools/glassmorphism-generator) — 글래스 효과 생성기
- [Material Design 3](https://m3.material.io/) — Google 공식 디자인 시스템
- [Apple Human Interface Guidelines — Materials](https://developer.apple.com/design/human-interface-guidelines/materials) — Apple 머티리얼 가이드
- [Fluent Design System](https://fluent2.microsoft.design/) — Microsoft Fluent 2
- [CSS Scroll-Driven Animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) — Chrome 스크롤 애니메이션 문서
- [WCAG 2.1 — 1.4 Distinguishable](https://www.w3.org/WAI/WCAG21/Understanding/distinguishable) — 접근성 가이드라인
