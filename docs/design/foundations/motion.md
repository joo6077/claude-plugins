---
title: 모션
version: 0.2.0
last_updated: 2026-03-30
---

# 모션

UI 애니메이션과 트랜지션의 목적, 타이밍, 이징 커브, 패턴을 체계적으로 정리한다. 모든 모션은 **기능적(functional)**이어야 하며, 장식적 용도는 지양한다.

---

## 원칙

### 1. 목적 있는 모션만 사용한다

모션은 사용자에게 **미묘한 피드백**을 제공하는 마이크로인터랙션 형태로 사용할 때 가장 적절하다. 즐거움을 주거나 사용자를 즐겁게 하기 위한 용도보다는, 시스템이 현재 무엇을 하고 있는지 보여주는 **단서** 역할을 해야 한다.

> **출처:** [The Role of Animation and Motion in UX — Nielsen Norman Group](https://www.nngroup.com/articles/animation-purpose-ux/)

### 2. 인지 부하를 줄인다

애니메이션은 사용자가 시스템의 작동 방식에 대한 **멘탈 모델을 구축**하도록 돕는다. UI 요소가 어떻게 동작할지 보여주는 시그니파이어(signifier), 정보 공간 내 사용자 위치를 나타내는 **공간적 메타포**로 활용한다. 호버 애니메이션은 사용자가 무엇이 클릭 가능한지 추측할 필요를 없애 인지 부하를 줄인다.

> **출처:** [Animation for Attention and Comprehension — Nielsen Norman Group](https://www.nngroup.com/articles/animation-usability/)

### 3. 대부분의 애니메이션은 너무 길다

애니메이션이 너무 짧은 것보다 **너무 긴 경우가 훨씬 흔하다**. 0.1초(100ms)의 차이가 사용자 인식에 눈에 띄게 다른 결과를 만든다. 애니메이션 설계 시 항상 짧은 쪽으로 편향하라.

> **출처:** [Executing UX Animations: Duration and Motion Characteristics — Nielsen Norman Group](https://www.nngroup.com/articles/animation-duration/)

### 4. 접근성을 고려한다

`prefers-reduced-motion` 미디어 쿼리를 존중하여, 전정 기관 장애가 있는 사용자에게는 모션을 줄이거나 제거해야 한다. 필수 피드백은 모션 대신 색상/아이콘 변화로 대체한다.

> **출처:** [prefers-reduced-motion — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)

---

## 듀레이션 체계

### 일반 가이드라인

대부분의 애니메이션 듀레이션은 **100~500ms** 범위 내에 있어야 한다.

| 유형                    | 듀레이션       | 설명                                            |
| ----------------------- | -------------- | ----------------------------------------------- |
| 단순 피드백             | ~100ms         | 체크박스, 토글 스위치 — 물리적 조작 착각 생성    |
| 중간 크기 변화          | 200~300ms      | 모달 진입, 중간 거리 이동                       |
| 대형 화면 변화          | 300~400ms      | 전체 화면 전환, 넓은 영역 이동                  |
| **최대 임계값**         | **500ms**      | 이 이상은 "끌리는(drag)" 느낌 — 사용자에게 짜증 유발 |

> **출처:** [Executing UX Animations: Duration and Motion Characteristics — Nielsen Norman Group](https://www.nngroup.com/articles/animation-duration/)

### 방향 비대칭 (Directional Asymmetry)

등장하는 요소는 사라지는 요소보다 **더 긴 듀레이션**이 필요하다:

- 팝업 등장: **300ms**
- 팝업 퇴장: **200~250ms**

> **출처:** [Executing UX Animations: Duration and Motion Characteristics — Nielsen Norman Group](https://www.nngroup.com/articles/animation-duration/)

### 디바이스별 보정

| 디바이스  | 보정      | 결과 범위   |
| --------- | --------- | ----------- |
| 모바일    | 기준      | 200~300ms   |
| 태블릿    | +30%      | 260~400ms   |
| 웨어러블  | -30%      | 150~200ms   |

> **출처:** [The Ultimate Guide to Proper Use of Animation in UX — UX Collective](https://uxdesign.cc/the-ultimate-guide-to-proper-use-of-animation-in-ux-10bd98614fa9)

### Material Design 3 듀레이션 토큰

M3는 4단계 x 4세분화 = **16개 듀레이션 토큰**을 정의한다:

| 토큰 그룹    | 1     | 2     | 3     | 4     |
| ------------ | ----- | ----- | ----- | ----- |
| **Short**    | 50ms  | 100ms | 150ms | 200ms |
| **Medium**   | 250ms | 300ms | 350ms | 400ms |
| **Long**     | 450ms | 500ms | 550ms | 600ms |
| **Extra-long** | 700ms | 800ms | 900ms | 1000ms |

- **Short**: 단순 피드백, 아이콘 상태 변경
- **Medium**: 카드 확장, 바텀시트 진입, 대부분의 UI 전환
- **Long**: 복잡한 레이아웃 변경, 다중 요소 조율
- **Extra-long**: 전체 화면 전환, 스플래시 → 메인 화면

> **출처:** [Motion — Material Components Android (GitHub)](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)

---

## 이징 커브

이징 커브는 애니메이션의 가속/감속 패턴을 결정하며, 자연스러운 움직임을 구현하는 핵심 요소다.

### Material Design 3 이징 토큰

| 이징 타입                 | cubic-bezier 값                  | 용도                                     |
| ------------------------- | -------------------------------- | ---------------------------------------- |
| **Standard**              | `cubic-bezier(0.2, 0, 0, 1)`    | 화면 내 요소 이동 (가장 범용)            |
| **Standard Decelerate**   | `cubic-bezier(0, 0, 0, 1)`      | 요소 진입 — 빠르게 들어와 천천히 정지    |
| **Standard Accelerate**   | `cubic-bezier(0.3, 0, 1, 1)`    | 요소 퇴장 — 천천히 시작해 빠르게 사라짐  |
| **Emphasized**            | 경로 커브 (Path Motion)          | 강조가 필요한 대형 전환                  |
| **Emphasized Decelerate** | `cubic-bezier(0.05, 0.7, 0.1, 1)` | 강조 진입 — 극적인 감속으로 주목 유도  |
| **Emphasized Accelerate** | `cubic-bezier(0.3, 0, 0.8, 0.15)` | 강조 퇴장 — 빠르게 가속해 퇴장         |
| **Linear**                | `cubic-bezier(0, 0, 1, 1)`      | 색상/투명도 변화 (위치 이동에는 비권장)  |

> **출처:** [Motion — Material Components Android (GitHub)](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)

### Emphasized 경로 커브 상세

Emphasized 이징은 단순한 cubic-bezier가 아닌 **SVG 경로 커브**로 정의된다:

```
M 0,0 C 0.05,0 0.133333,0.06 0.166666,0.4 C 0.208333,0.82 0.25,1 1,1
```

이 커브는 시작 시 강한 가속 후 긴 감속 구간을 가지며, 컨테이너 트랜스폼과 같은 **대형 전환**에 사용된다.

> **출처:** [Easing and Duration — Material Design 3](https://m3.material.io/styles/motion/easing-and-duration)

### 이징 선택 가이드

```
요소가 화면에 남아 있는가?
├─ Yes → Standard (0.2, 0, 0, 1)
│   └─ 강조가 필요한가?
│       ├─ Yes → Emphasized (경로 커브)
│       └─ No → Standard
└─ No
    ├─ 진입하는가? → Standard Decelerate (0, 0, 0, 1)
    │   └─ 강조 필요? → Emphasized Decelerate (0.05, 0.7, 0.1, 1)
    └─ 퇴장하는가? → Standard Accelerate (0.3, 0, 1, 1)
        └─ 강조 필요? → Emphasized Accelerate (0.3, 0, 0.8, 0.15)
```

---

## 트랜지션 패턴

Material Design 3는 4가지 핵심 트랜지션 패턴을 정의한다.

### 1. Container Transform (컨테이너 트랜스폼)

**공유 요소 전환(shared element transition)**으로, 시작 뷰의 바운딩 컨테이너가 끝 뷰의 크기와 형태로 변환된다. 카드를 탭하면 카드가 확장되어 상세 화면이 되는 패턴이 대표적이다.

- **듀레이션**: Medium 3~4 (350~400ms)
- **이징**: Emphasized
- **용도**: 카드 → 상세, 리스트 아이템 → 상세, FAB → 전체 화면

> **출처:** [Motion — Material Components Android (GitHub)](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)

### 2. Shared Axis (공유 축)

같은 공간적 축(X, Y, Z)을 따라 이동하는 **방향성 전환**이다. 전진/후진 네비게이션에서 사용자에게 이동 방향을 알려준다.

- **듀레이션**: Medium 3~4 (350~400ms)
- **이징**: Standard
- **X축**: 탭 간 수평 이동
- **Y축**: 스텝퍼(stepper) 단계 간 수직 이동
- **Z축**: 부모 → 자식 깊이 이동

> **출처:** [Motion — Material Components Android (GitHub)](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)

### 3. Fade Through (페이드 스루)

두 화면 사이에 **공간적 또는 순서적 관계가 없는** 최상위 전환에 사용한다. 나가는 요소가 먼저 페이드 아웃되고, 들어오는 요소가 페이드 인 + 스케일 업된다.

- **듀레이션**: Medium 2~3 (300~350ms)
- **이징**: Standard Accelerate (퇴장) + Standard Decelerate (진입)
- **용도**: 바텀 네비게이션 탭 전환, 홈 → 검색 → 프로필

> **출처:** [Motion — Material Components Android (GitHub)](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)

### 4. Fade (페이드 진입/퇴장)

단순한 **투명도 전환**으로, 요소가 나타나거나 사라질 때 사용한다. 스낵바, 다이얼로그, 메뉴 등 UI 위에 겹쳐지는(overlay) 요소에 적합하다.

- **듀레이션**: Short 3~4 (150~200ms)
- **이징**: Standard Decelerate (진입), Standard Accelerate (퇴장)
- **용도**: 스낵바, 툴팁, 메뉴, 다이얼로그

> **출처:** [Motion — Material Components Android (GitHub)](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)

### 트랜지션 선택 가이드

```
두 화면이 공유하는 요소가 있는가?
├─ Yes → Container Transform
└─ No
    ├─ 순서/방향 관계가 있는가?
    │   ├─ Yes → Shared Axis (X/Y/Z)
    │   └─ No → Fade Through
    └─ 오버레이 요소인가?
        └─ Yes → Fade
```

### Flutter 구현 참고

Flutter에서 M3 트랜지션을 구현할 때는 `animations` 패키지의 다음 위젯을 사용한다:

| 패턴              | Flutter 위젯                     |
| ----------------- | -------------------------------- |
| Container Transform | `OpenContainer`                |
| Shared Axis       | `SharedAxisTransition`           |
| Fade Through      | `FadeThroughTransition`          |
| Fade              | `FadeScaleTransition`            |
