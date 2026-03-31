---
title: 이미지 & 일러스트 사용 원칙
version: 0.2.0
last_updated: 2026-03-30
---

# 이미지 & 일러스트 사용 원칙

UI에서 이미지와 일러스트를 선택, 배치, 최적화, 접근성 처리하는 원칙을 정리한다.

---

## 원칙

### 1. 이미지는 콘텐츠를 보조하지, 대체하지 않는다

이미지가 텍스트 없이 독립적으로 의미를 전달해야 하는 경우는 드물다. 대부분의 UI에서 이미지는 텍스트 콘텐츠를 시각적으로 보강하는 역할이다. "이미지가 없으면 이해할 수 없는 UI"는 접근성에 실패한 UI다.

> **출처:** [W3C WAI — Images Tutorial](https://www.w3.org/WAI/tutorials/images/)

### 2. 모든 이미지는 목적이 있어야 한다

장식적 이미지(decorative image)도 미학적 목적이라는 의도가 있어야 한다. "이 이미지를 제거하면 무엇이 달라지는가?"에 답할 수 없다면 그 이미지는 불필요하다. 불필요한 이미지는 페이지 로딩 시간만 늘리고 사용자의 주의를 분산시킨다.

### 3. 일관된 시각 언어를 유지한다

하나의 제품 내에서 사진, 3D 일러스트, 2D 일러스트, 아이콘을 무작위로 혼용하면 브랜드 정체성이 훼손된다. 시각적 스타일을 하나 선택하고 전체 제품에 일관되게 적용해야 한다.

### 4. 성능은 시각적 품질만큼 중요하다

고해상도 이미지가 3초 동안 로딩되는 것보다 최적화된 이미지가 0.5초 내에 표시되는 것이 UX에 유리하다. Google Core Web Vitals에서 LCP(Largest Contentful Paint)는 2.5초 이내를 "Good"으로 분류한다.

> **출처:** [web.dev — Largest Contentful Paint](https://web.dev/articles/lcp)

---

## 사진 vs 일러스트 선택 기준

### 사진이 적합한 경우

| 상황 | 이유 |
|------|------|
| 실제 제품 표시 | 구매 결정에 실물 확인 필요 |
| 사람/팀 소개 | 신뢰감, 인간적 연결 |
| 장소/환경 표현 | 분위기 전달, 현장감 |
| 음식/요리 | 시각적 욕구 자극 |
| 포트폴리오/갤러리 | 실제 결과물 전시 |
| 사용자 생성 콘텐츠 | 아바타, 리뷰 이미지 |

### 일러스트가 적합한 경우

| 상황 | 이유 |
|------|------|
| 추상 개념 설명 | "클라우드 컴퓨팅", "보안" 등 사진으로 표현 어려움 |
| 프로세스/단계 안내 | 순서도, 워크플로우 시각화 |
| 빈 상태(Empty State) | "검색 결과 없음", "장바구니 비어 있음" |
| 에러/성공 상태 | 404 페이지, 가입 완료 |
| 브랜드 차별화 | 고유한 일러스트 스타일로 정체성 구축 |
| 온보딩 | 기능 설명, 가치 제안 |

### 혼용이 필요한 경우

- 사진 배경 + 일러스트 오버레이 (예: 지도 위의 핀 아이콘)
- 아바타 사진 + 일러스트 배지/프레임
- 제품 사진 + 도표/다이어그램

혼용 시 **시각적 무게가 일관**되어야 한다. 사진은 무겁고 일러스트는 가벼운 느낌이므로, 두 요소의 크기와 위치를 균형 있게 배치한다.

---

## 이미지 크롭 규칙

### 용도별 권장 비율

| 용도 | 비율 | 해상도 예시 | 특성 |
|------|------|------------|------|
| **히어로 배너** | 16:9 | 1920x1080 | 넓고 드라마틱 |
| **히어로 (모바일)** | 4:3 또는 3:4 | 1080x1440 | 세로 공간 활용 |
| **카드 썸네일** | 16:9 또는 4:3 | 640x360 / 640x480 | 가로형 카드 |
| **정사각형 카드** | 1:1 | 600x600 | 제품, 프로필 |
| **리스트 아이템** | 1:1 또는 3:2 | 80x80 / 120x80 | 소형 썸네일 |
| **프로필 아바타** | 1:1 (원형 크롭) | 200x200 | 원형 마스크 |
| **OG 이미지** | 1.91:1 | 1200x630 | 소셜 미디어 공유 |

> **출처:** [Tiny-img — Best Image Size for Website](https://tiny-img.com/blog/best-image-size-for-website/)

### 초점(Focal Point) 규칙

이미지의 핵심 피사체가 크롭 영역 안에 있어야 한다. 반응형 디자인에서 동일한 이미지가 여러 비율로 크롭되므로, 핵심 피사체는 이미지 중앙 60% 영역(safe zone)에 위치해야 한다.

```
┌───────────────────────────────┐
│                               │
│    ┌─────────────────────┐    │
│    │                     │    │
│    │    SAFE ZONE        │    │
│    │    (focal point     │    │
│    │     goes here)      │    │
│    │                     │    │
│    └─────────────────────┘    │
│                               │
└───────────────────────────────┘
  ↑ 양쪽 20%는 크롭될 수 있음 ↑
```

### CSS object-fit 활용

```css
/* 비율 유지하며 영역 채우기 (크롭 허용) */
.thumbnail {
  aspect-ratio: 16 / 9;
  object-fit: cover;
  object-position: center top; /* 초점이 상단에 있는 경우 */
}

/* 비율 유지하며 영역 안에 맞추기 (여백 허용) */
.product-image {
  aspect-ratio: 1 / 1;
  object-fit: contain;
  background: var(--color-surface-variant);
}
```

### 크롭 안티패턴

```
[BAD]  인물 사진에서 머리 잘림 → object-position: center top 사용
[BAD]  제품 사진 좌우 잘림 → object-fit: contain으로 변경
[BAD]  세로 이미지를 16:9로 강제 크롭 → 별도 세로용 크롭 제공
[BAD]  텍스트가 포함된 이미지 크롭 → 텍스트는 이미지 밖에 배치
```

---

## 이미지 최적화

### 포맷 선택 가이드

| 포맷 | 압축 | 투명도 | 애니메이션 | 용도 |
|------|------|--------|-----------|------|
| **WebP** | 손실/무손실 | O | O | 범용 웹 이미지 (90%+ 브라우저 지원) |
| **AVIF** | 손실/무손실 | O | O | 고화질 사진 (WebP 대비 20–50% 더 작음) |
| **JPEG** | 손실 | X | X | 폴백용, 레거시 브라우저 |
| **PNG** | 무손실 | O | X | 정밀한 투명도, 스크린샷 |
| **SVG** | 벡터 | O | O | 아이콘, 로고, 일러스트 |
| **GIF** | 무손실 | 1bit | O | 짧은 애니메이션 (비효율적, 대안 권장) |

선택 순서: SVG(벡터) → AVIF(사진) → WebP(범용) → JPEG/PNG(폴백)

### `<picture>` 요소로 포맷 분기

```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="제품 히어로 이미지" width="1920" height="1080">
</picture>
```

### srcset으로 해상도 분기

```html
<img
  srcset="photo-400w.webp 400w,
          photo-800w.webp 800w,
          photo-1200w.webp 1200w,
          photo-1920w.webp 1920w"
  sizes="(max-width: 600px) 100vw,
         (max-width: 1200px) 50vw,
         33vw"
  src="photo-800w.webp"
  alt="설명 텍스트"
  width="1920"
  height="1080"
>
```

브라우저가 디바이스 해상도와 뷰포트 크기에 따라 최적의 이미지를 자동 선택한다.

> **출처:** [web.dev — Browser-level Image Lazy Loading](https://web.dev/articles/browser-level-image-lazy-loading)

### Lazy Loading

```html
<!-- 스크롤 아래 이미지에만 적용 -->
<img src="photo.webp" loading="lazy" alt="..." width="800" height="600">

<!-- LCP 이미지(히어로)에는 절대 lazy 적용하지 않는다 -->
<img src="hero.webp" loading="eager" fetchpriority="high" alt="...">
```

주의: LCP 이미지에 `loading="lazy"`를 적용하면 오히려 LCP가 악화된다. Above the fold 이미지는 반드시 `loading="eager"` (기본값)을 유지한다.

> **출처:** [DebugBear — Optimizing Images for Web Performance](https://www.debugbear.com/blog/image-optimization-web-performance)

### 플레이스홀더 전략

이미지 로딩 중 빈 공간이나 깜빡임을 방지하는 기법이다.

| 전략 | 설명 | 적합한 상황 |
|------|------|------------|
| **고정 영역 (width/height)** | 이미지 크기를 미리 지정해 Layout Shift 방지 | 모든 이미지에 필수 |
| **단색 배경** | 이미지 주요 색상 추출 후 배경으로 사용 | 갤러리, 카드 |
| **LQIP (Low Quality Image Placeholder)** | 극소 해상도(20–40px) 이미지를 블러 처리 후 표시 | 사진 중심 레이아웃 |
| **BlurHash** | 4x3 해시 문자열로 블러 이미지 생성 | 모바일 앱, 최소 데이터 |
| **스켈레톤 shimmer** | 이미지 영역에 shimmer 애니메이션 | 피드, 리스트 |

### 파일 크기 가이드라인

| 용도 | 목표 크기 | 최대 허용 |
|------|-----------|-----------|
| 썸네일 (80–200px) | 5–15KB | 30KB |
| 카드 이미지 (400–600px) | 30–60KB | 100KB |
| 콘텐츠 이미지 (800px) | 50–100KB | 200KB |
| 히어로 이미지 (1920px) | 100–200KB | 400KB |
| 전체 페이지 이미지 합계 | — | 1.5MB |

> **출처:** [Request Metrics — High Performance Images Guide](https://requestmetrics.com/web-performance/high-performance-images/)

---

## 접근성

### alt 텍스트 작성 규칙

WCAG 1.1.1은 모든 비텍스트 콘텐츠에 텍스트 대안을 요구한다. WebAIM Million 조사에서 alt 텍스트 부재/부적절이 **58%의 홈페이지**에서 발견되었다.

> **출처:** [W3C WAI — Images Tutorial](https://www.w3.org/WAI/tutorials/images/)

### 이미지 유형별 alt 텍스트

| 이미지 유형 | alt 처리 | 예시 |
|------------|----------|------|
| **정보 전달(Informative)** | 이미지가 전달하는 정보를 텍스트로 기술 | `alt="2025년 매출 추이: 1분기 대비 4분기 23% 증가"` |
| **기능적(Functional)** | 이미지의 **기능**을 기술 (모양 아님) | `alt="검색"` (돋보기 아이콘), `alt="홈으로 이동"` (로고) |
| **장식적(Decorative)** | 빈 alt 사용 | `alt=""` (스크린 리더가 건너뜀) |
| **복잡한(Complex)** | 간략 alt + 상세 설명(longdesc 또는 인접 텍스트) | 차트, 인포그래픽, 다이어그램 |
| **텍스트 이미지** | 이미지 내 텍스트를 그대로 기술 | `alt="30% 할인 쿠폰 - 코드: SAVE30"` |

### alt 텍스트 작성 원칙

| 규칙 | 설명 |
|------|------|
| "~의 이미지" 불필요 | 스크린 리더가 이미 "이미지"라고 안내함 |
| 핵심 정보를 앞에 | 중요한 내용부터 기술 |
| 1–2문장 이내 | 간결하게 (125자 이내 권장) |
| 맥락 반영 | 같은 사진이라도 페이지 맥락에 따라 다른 alt |
| 로고+이름은 한 번만 | "ABC 로고" 반복 불필요 |

### 복잡한 이미지의 상세 설명

차트, 다이어그램, 인포그래픽은 alt만으로 정보를 전달할 수 없다. 인접한 텍스트 또는 `<details>` 요소로 상세 설명을 제공한다.

```html
<figure>
  <img src="sales-chart.webp"
       alt="2025년 분기별 매출 차트. 상세 수치는 아래 표 참조.">
  <figcaption>
    <details>
      <summary>차트 데이터 보기</summary>
      <table>
        <tr><td>1분기</td><td>120억</td></tr>
        <tr><td>2분기</td><td>135억</td></tr>
        <tr><td>3분기</td><td>142억</td></tr>
        <tr><td>4분기</td><td>148억</td></tr>
      </table>
    </details>
  </figcaption>
</figure>
```

> **출처:** [W3C WAI — An alt Decision Tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)

### 장식적 이미지 판별 기준

다음 질문에 모두 "아니오"이면 장식적 이미지다:
1. 이 이미지를 제거하면 페이지의 의미가 달라지는가?
2. 이 이미지가 링크나 버튼의 일부인가?
3. 이 이미지에 텍스트가 포함되어 있는가?

---

## 안티패턴

### 스톡 사진 클리셰

| 클리셰 | 문제 | 대안 |
|--------|------|------|
| 악수하는 비즈니스맨 | 모든 B2B 사이트에서 사용, 차별화 불가 | 실제 팀/오피스 사진 |
| 헤드셋 쓴 고객 지원 직원 | 진부하고 인위적 | 실제 지원 과정 캡처 |
| 화이트보드 앞 브레인스토밍 | 연출감 과다 | 실제 작업 환경 촬영 |
| 노트북 든 행복한 사람 | 모든 SaaS 랜딩에서 사용 | 제품 스크린샷 + 일러스트 |
| 지구본/네트워크 그래픽 | "글로벌" 표현의 남용 | 실제 서비스 지역 지도 |

### 스타일 불일치

```
[BAD]  같은 페이지에 사실적 사진 + 플랫 일러스트 + 3D 렌더링 혼재
[BAD]  온보딩은 컬러풀한 일러스트, 설정 화면은 무미건조한 아이콘
[GOOD] 전체 제품에서 하나의 일러스트 스타일(선 굵기, 색상 팔레트, 원근법) 통일
```

### 최적화 미흡

| 문제 | 영향 | 해결 |
|------|------|------|
| 원본 5000x3000 JPEG 그대로 사용 | 파일 크기 2–5MB, LCP 5초+ | srcset으로 해상도 분기 |
| PNG를 사진에 사용 | JPEG/WebP 대비 3–10배 큰 파일 | WebP/AVIF로 변환 |
| 모든 이미지 eager loading | 초기 로딩 시간 증가 | Below the fold에 lazy loading |
| width/height 미지정 | Cumulative Layout Shift 발생 | 항상 크기 속성 명시 |
| LCP 이미지에 lazy loading | LCP 지표 악화 | 히어로 이미지는 eager + fetchpriority="high" |

### 접근성 위반

| 문제 | WCAG 위반 | 해결 |
|------|-----------|------|
| alt 속성 누락 | 1.1.1 Non-text Content | 모든 `<img>`에 alt 필수 |
| 장식 이미지에 `alt="이미지"` | 스크린 리더가 무의미한 텍스트 읽음 | `alt=""` 사용 |
| 텍스트를 이미지로 제작 | 1.4.5 Images of Text | 실제 텍스트 + CSS 스타일링 |
| 색상만으로 정보 전달하는 차트 | 1.4.1 Use of Color | 패턴/라벨 추가 |

---

## 참고 문헌

- [W3C WAI — Images Tutorial](https://www.w3.org/WAI/tutorials/images/)
- [W3C WAI — An alt Decision Tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)
- [web.dev — Browser-level Image Lazy Loading](https://web.dev/articles/browser-level-image-lazy-loading)
- [DebugBear — Optimizing Images for Web Performance](https://www.debugbear.com/blog/image-optimization-web-performance)
- [Request Metrics — High Performance Images Guide](https://requestmetrics.com/web-performance/high-performance-images/)
- [web.dev — Largest Contentful Paint](https://web.dev/articles/lcp)
- [Tiny-img — Best Image Size for Website](https://tiny-img.com/blog/best-image-size-for-website/)
