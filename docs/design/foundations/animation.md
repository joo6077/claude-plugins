---
title: 애니메이션 디자인 가이드
version: 0.2.0
last_updated: 2026-03-30
---

# 애니메이션 디자인 가이드

모션(duration/easing/transitions)과 마이크로인터랙션(button states/toggles/gestures)은 별도 문서에서 다룬다. 이 문서는 **애니메이션을 디자인 규율(discipline)로서** 체계적으로 접근하는 방법을 다룬다. Disney 12원칙의 UI 적용, 코레오그래피, 스크롤 기반 애니메이션, 페이지 전환, 로딩 전략, 스프링 물리학, Lottie/Rive, 토큰 시스템, 성능 최적화, 접근성을 포함한다.

---

## 원칙 — Disney의 12원칙을 UI에 적용한다

Disney의 Frank Thomas와 Ollie Johnston이 1981년 《The Illusion of Life》에서 정리한 12원칙은 물리 법칙과 인지 심리학의 결합이다. UI에 적용할 때는 "캐릭터에 생명을 불어넣는다"가 아니라 **"인터페이스 요소에 물리적 실재감을 부여한다"**로 재해석한다.

> **출처:** [UI Animation — How to Apply Disney's 12 Principles of Animation to UI Design — IxDF](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design)

### 1. Squash & Stretch → 스케일 피드백

오브젝트의 무게감과 유연성을 전달한다. UI에서는 버튼 누름 시 약간의 scaleY(0.95) 압축(squash)과 릴리즈 시 scaleY(1.02) 팽창(stretch)으로 촉각적 피드백을 만든다. 볼륨은 보존해야 한다 — scaleX와 scaleY를 동시에 조절해 면적이 일정하게 유지되도록 한다.

### 2. Anticipation → 버튼 프레스 예비 동작

주요 동작 전의 준비 동작이다. 버튼의 hover 상태에서 살짝 들어올리거나(translateY(-2px)), 삭제 전에 아이템이 좌측으로 살짝 밀리는 것이 해당한다. 사용자에게 "이것은 인터랙티브하다"는 신호를 보낸다.

> **출처:** [Disney's 12 Principles of Animation, Exemplified in UX Design — UX Collective](https://uxdesign.cc/disneys-12-principles-of-animation-exemplified-in-ux-design-5cc7e3dc3f75)

### 3. Staging → 시선 유도

씬에서 가장 중요한 요소에 시선을 집중시킨다. UI에서는 모달이 열릴 때 배경을 dimming하고, 중요 CTA만 컬러를 유지하며, 나머지 요소의 모션을 최소화하는 것이 staging이다.

### 4. Straight Ahead vs. Pose to Pose → 키프레임 전략

Pose to Pose는 핵심 포즈(keyframe)를 먼저 잡고 사이를 채우는 방식이다. CSS `@keyframes`와 정확히 일치한다. 0%, 50%, 100% 포즈를 먼저 정의하고 이징으로 보간한다.

### 5. Follow Through & Overlapping Action → 관성 스크롤

주요 동작이 멈춘 후에도 부수 요소가 약간 더 움직이는 것이다. iOS의 바운스 스크롤, 드래그 후 카드가 살짝 오버슈트했다가 제자리로 돌아오는 것, 리스트 아이템의 시차 정지(staggered settle)가 이에 해당한다.

> **출처:** [Applying Disney's Basic Principles of Animation to UI Design — Dribbble](https://dribbble.com/stories/2020/07/27/disney-principles-of-animation-ui-interactions)

### 6. Slow In & Slow Out → 이징 커브

자연계의 모든 움직임은 시작과 끝에서 느려진다. 선형(linear) 움직임은 기계적이고 부자연스럽다. `ease-out`(감속)은 진입에, `ease-in`(가속)은 퇴장에, `ease-in-out`은 화면 내 이동에 사용한다.

### 7. Arc → 곡선 경로

자연스러운 움직임은 직선이 아닌 호를 그린다. FAB가 확장될 때, 드래그 앤 드롭 시 아이템이 이동할 때 약간의 arc path를 적용하면 물리적 실재감이 생긴다. Material Design의 경로 커브(Path Motion)가 이 원칙의 구현이다.

### 8. Secondary Action → 부수 효과

주요 액션을 보조하는 부수 동작이다. 버튼 클릭 시 ripple 이펙트, 체크박스 체크 시 아이콘이 바운스하면서 배경색이 변하는 것, 토스트 알림이 슬라이드인하면서 약간 흔들리는 것이 해당한다. 모든 마이크로인터랙션이 이 원칙에 기반한다.

### 9. Timing → 듀레이션 설계

같은 이징이라도 듀레이션에 따라 무게감이 달라진다. 100ms는 가볍고 즉각적이며, 400ms는 무겁고 의도적이다. 작은 요소는 짧게, 큰 화면 전환은 길게 — 크기와 거리에 비례하여 듀레이션을 설정한다.

### 10. Exaggeration → 과장

현실을 정확히 복제하면 오히려 밋밋해 보인다. UI에서 과장은 **미세한** 수준이어야 한다 — 삭제 시 아이템이 옆으로 120% 정도 날아가거나, 에러 시 인풋이 살짝 흔들리는(2-3px shake) 수준이다. 과도한 과장은 놀이공원 느낌을 준다.

### 11. Solid Drawing → 일관된 시각 체계

3D에서의 볼륨감과 무게감에 해당한다. UI에서는 shadow, depth, z-index의 일관성이다. 떠 있는 요소는 그림자가 있어야 하고, 뒤로 밀린 요소는 블러되어야 한다.

### 12. Appeal → 매력

보기 좋고 사용하기 즐거운 인터페이스다. 잘 설계된 애니메이션은 브랜드 개성을 전달한다 — Stripe의 절제된 우아함, Duolingo의 장난기, Linear의 정밀한 엔지니어링 느낌.

> **출처:** [Disney's 12 Principles of Animation in Everyday UI Design — Medium/Bootcamp](https://medium.com/design-bootcamp/disneys-12-principles-of-animation-in-everyday-ui-design-71c6592064fe)

---

## 애니메이션 코레오그래피

여러 요소가 동시에 움직일 때의 조율(choreography)을 다룬다. 개별 요소의 모션이 아무리 좋아도 전체가 조화롭지 않으면 혼란스럽다.

### Staggered Animation (시차 애니메이션)

리스트나 그리드의 아이템이 순차적으로 나타나는 패턴이다. 모든 아이템이 동시에 나타나면 포커스가 분산되고, 하나씩 기다리면 너무 느리다.

**Material Design 스태거 타이밍:**

- 아이템 간 간격: **20-40ms** (아이템이 완전히 끝나기를 기다리지 않고 겹쳐서 시작)
- 총 스태거 시간: 전체 그룹이 **500ms 이내**에 완료
- 리스트: 위에서 아래로 순차 진입
- 그리드: 좌측 상단에서 우측 하단으로 대각선 진입

> **출처:** [Choreography — Motion — Material Design](https://m2.material.io/design/motion/choreography.html)

### 시퀀싱 패턴

| 패턴 | 설명 | 용도 |
|------|------|------|
| **Cascade (폭포식)** | 위→아래로 순차 등장, 가장 자연스러운 읽기 방향 | 리스트, 카드 피드 |
| **Radial (방사형)** | 중심점에서 바깥으로 퍼져나감 | 그리드 레이아웃, 대시보드 |
| **Random** | 무작위 순서로 등장, 유기적 느낌 | 갤러리, 마소닉 레이아웃 |
| **Group** | 관련 요소가 그룹으로 동시 등장 후 다음 그룹 | 폼 섹션, 카드 그룹 |

### 진입/퇴장 코레오그래피

진입(entrance)과 퇴장(exit)은 대칭이 아니다:

- **진입**: 느린 감속(decelerate)으로 자리잡기 — 사용자가 새 콘텐츠를 인지할 시간 확보
- **퇴장**: 빠른 가속(accelerate)으로 사라지기 — 나가는 콘텐츠에 시간을 낭비하지 않는다
- **원칙**: 퇴장 듀레이션은 진입의 60-80%

> **출처:** [Motion — Carbon Design System](https://carbondesignsystem.com/elements/motion/choreography/)

### 코레오그래피 규칙

1. **하나의 포커스**: 한 시점에 사용자의 시선이 향하는 곳은 하나여야 한다
2. **연속성**: 이전 상태와 다음 상태 사이의 관계가 명확해야 한다
3. **시간 예산**: 전체 코레오그래피 시퀀스는 **800ms를 초과하지 않는다**
4. **깊이 우선**: 가장 앞(z-index 높은)의 요소부터 애니메이션한다

---

## 스크롤 기반 애니메이션

스크롤은 웹에서 가장 자연스러운 인터랙션이다. 스크롤 위치에 연동된 애니메이션은 사용자에게 직접 제어하는 느낌을 준다.

### Scroll-triggered Animation

Intersection Observer API를 사용하여 요소가 뷰포트에 진입할 때 애니메이션을 트리거한다.

```css
/* 기본 패턴 */
.reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.6s ease-out, transform 0.6s ease-out; }
.reveal.visible { opacity: 1; transform: translateY(0); }
```

**threshold 설정 가이드:**
- `0.1` (10%): 요소가 살짝 보이면 즉시 — 긴 콘텐츠 카드에 적합
- `0.3` (30%): 기본 권장값 — 충분히 보일 때 트리거
- `0.5` (50%): 절반 노출 시 — 중요한 CTA나 히어로 섹션

> **출처:** [CSS Scroll-driven Animations — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations)

### CSS Scroll-driven Animations (scroll-timeline)

JavaScript 없이 CSS만으로 스크롤 연동 애니메이션을 구현하는 신규 사양이다. 메인 스레드를 차단하지 않아 성능이 우수하다.

```css
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.element {
  animation: fadeIn linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

- `scroll()`: 스크롤 컨테이너의 전체 스크롤 진행률에 연동
- `view()`: 개별 요소의 뷰포트 가시성에 연동

> **출처:** [An Introduction to CSS Scroll-Driven Animations — Smashing Magazine](https://www.smashingmagazine.com/2024/12/introduction-css-scroll-driven-animations/)

### Parallax (시차 스크롤)

배경과 전경이 서로 다른 속도로 스크롤되어 깊이감을 만든다.

**구현 방식:**
- CSS `perspective` + `translateZ`: 순수 CSS, 성능 최적 — 권장
- `transform: translateY(calc(var(--scroll) * 0.5))`: JS 기반 — Intersection Observer와 조합
- `background-attachment: fixed`: 가장 단순하지만 모바일 성능 문제

**주의:** 시차 스크롤은 전정 기관 장애 사용자에게 어지러움을 유발한다. `prefers-reduced-motion: reduce` 시 반드시 비활성화한다.

### Sticky Header

`position: sticky`와 결합하여 스크롤 시 헤더가 축소되거나, 배경이 불투명해지거나, 그림자가 추가되는 패턴이다. `scroll-timeline`과 결합하면 JS 없이 구현 가능하다.

### Progress Indicator

스크롤 진행률을 시각화하는 바(bar)다. 페이지 최상단에 얇은 프로그레스 바를 배치하여 읽기 진행률을 표시한다. `animation-timeline: scroll()`로 CSS만으로 구현 가능하다.

### Scroll Snap

`scroll-snap-type`과 `scroll-snap-align`으로 스크롤이 특정 지점에 자연스럽게 "걸리는" 효과를 만든다. 캐러셀, 풀스크린 섹션 네비게이션에 적합하다.

```css
.container { scroll-snap-type: x mandatory; overflow-x: auto; }
.item { scroll-snap-align: start; }
```

---

## 페이지 전환 애니메이션

화면 간 이동은 앱에서 가장 빈번한 애니메이션 컨텍스트다. 잘 설계된 전환은 공간적 관계를 전달하고 사용자의 멘탈 모델을 강화한다.

### Shared Element Transition (공유 요소 전환)

두 화면이 공유하는 요소(이미지, 제목 등)가 시작 위치에서 끝 위치로 자연스럽게 변환되는 패턴이다. 카드 → 상세 화면, 썸네일 → 전체 이미지, 리스트 → 상세 등에서 사용한다.

**핵심 원리:**
1. 공유 요소에 고유 식별자 부여 (`view-transition-name`)
2. 시작과 끝 상태의 위치/크기/형태를 캡처
3. 두 상태 사이를 보간(interpolate)

> **출처:** [Smooth Transitions with the View Transition API — Chrome for Developers](https://developer.chrome.com/docs/web-platform/view-transitions)

### View Transitions API

웹 플랫폼의 네이티브 전환 API다. SPA와 MPA 모두 지원한다.

```javascript
// SPA: 같은 문서 내 전환
document.startViewTransition(() => {
  updateDOM(); // DOM 변경
});
```

```css
/* 기본 크로스페이드를 커스텀 애니메이션으로 대체 */
::view-transition-old(hero-image) {
  animation: slide-out 0.3s ease-in;
}
::view-transition-new(hero-image) {
  animation: slide-in 0.3s ease-out;
}
```

> **출처:** [View Transition API — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)

### 라우트 기반 전환 패턴

| 패턴 | 설명 | 용도 |
|------|------|------|
| **Fade** | 단순 크로스페이드 | 관계 없는 페이지 간 이동 |
| **Slide** | 좌우/상하 슬라이드 | 순서가 있는 네비게이션 (탭, 스텝퍼) |
| **Scale** | 축소/확대 전환 | 깊이 이동 (부모 → 자식) |
| **Shared Element Morph** | 공유 요소 변환 | 카드 → 상세, 목록 → 상세 |

### Hero Animation

화면 전환 시 중심이 되는 대형 요소의 전환이다. Flutter의 `Hero` 위젯, 웹의 `view-transition-name`이 이 패턴을 구현한다. 히어로 요소는 전환 중 다른 모든 요소보다 높은 z-index를 가져야 하며, 듀레이션은 300-400ms가 적절하다.

---

## 로딩 애니메이션

로딩은 피할 수 없는 대기 시간이다. 이 시간을 어떻게 설계하느냐가 **체감 성능(perceived performance)**을 결정한다.

### Skeleton Shimmer

콘텐츠의 실제 레이아웃을 모방한 회색 플레이스홀더에 빛이 스치는(shimmer) 효과를 적용한다. Facebook, YouTube, LinkedIn이 대표적이다.

**파형(wave) vs 맥동(pulse):** 좌→우 파형 shimmer가 맥동(opacity 페이드)보다 **대기 시간을 20-30% 짧게** 인식하게 한다.

> **출처:** [Skeleton Loading Screen Design — How to Improve Perceived Performance — LogRocket](https://blog.logrocket.com/ux-design/skeleton-loading-screen-design/)

**구현 가이드:**
- shimmer 속도: 1.5-2초 주기 — 너무 빠르면 주의를 빼앗고, 너무 느리면 정지해 보인다
- 색상: 배경보다 약간 밝은 회색 (dark theme: `#1a1c2e` → `#252840`)
- 0.5초 미만의 로딩에는 스켈레톤을 표시하지 않는다 — 깜빡임만 유발

### Progress Bar

확정적 진행률이 있을 때(파일 업로드, 다운로드) 사용한다. 불확정 진행(indeterminate)에는 좌우로 왕복하는 바를 사용한다.

**착시 효과:** 프로그레스 바에 역방향으로 움직이는 줄무늬를 넣으면 실제보다 빠르게 느껴진다.

> **출처:** [Everything You Need to Know About Skeleton Screens — UX Collective](https://uxdesign.cc/what-you-should-know-about-skeleton-screens-a820c45a571a)

### Spinner 가이드라인

스피너는 가장 단순한 로딩 인디케이터이지만 남용하면 안 된다:

- **크기**: 16-24px (인라인), 32-48px (페이지 레벨)
- **속도**: 0.8-1.2초/회전
- **사용 시점**: 2초 이상 로딩이 예상될 때만 — 짧은 로딩에는 아무것도 표시하지 않는다
- **수량**: 화면에 동시에 2개 이상의 스피너는 금지

### Content Placeholder (블러업)

저해상도 이미지를 먼저 표시하고, 고해상도 이미지가 로드되면 블러를 해제하는 패턴이다. Medium의 이미지 로딩이 대표적이다. `filter: blur(20px)`에서 `blur(0)`으로 전환한다.

### 체감 성능 전략

| 기법 | 효과 | 구현 난이도 |
|------|------|-----------|
| 스켈레톤 shimmer | 체감 20-30% 단축 | 중 |
| 낙관적 업데이트 (Optimistic UI) | 즉각 반응 | 높 |
| 점진적 로딩 (Progressive) | 빠른 첫 인상 | 중 |
| 블러업 이미지 | 레이아웃 안정 + 부드러운 전환 | 낮 |
| 프로그레스 바 착시 | 체감 10-15% 단축 | 낮 |

---

## Spring 물리학

이징 커브(cubic-bezier)는 시작과 끝 상태를 미리 알아야 한다. Spring 애니메이션은 물리 시뮬레이션에 기반하므로 **중단과 방향 전환이 자연스럽다** — 진행 중인 애니메이션을 끊고 새 목적지로 전환할 때 특히 유리하다.

### 핵심 파라미터

| 파라미터 | 설명 | 효과 |
|---------|------|------|
| **Tension (Stiffness)** | 스프링의 강성 — 얼마나 세게 당기는가 | 높을수록 빠르고 급격한 움직임 |
| **Friction (Damping)** | 마찰력 — 얼마나 빨리 안정되는가 | 높을수록 오버슈트 감소, 낮으면 탄성적 |
| **Mass** | 오브젝트의 질량 | 높을수록 느리게 시작, 관성이 큼 |

> **출처:** [A Friendly Introduction to Spring Physics Animation — Josh W. Comeau](https://www.joshwcomeau.com/animation/a-friendly-introduction-to-spring-physics/)

### 프레임워크별 구현

**Framer Motion (React):**
```jsx
<motion.div animate={{ x: 100 }} transition={{ type: "spring", stiffness: 100, damping: 10, mass: 1 }} />
```
- 기본값: stiffness=100, damping=10, mass=1

**React Spring:**
```jsx
useSpring({ to: { x: 100 }, config: { tension: 170, friction: 26, mass: 1 } })
```

**iOS UIKit:**
```swift
UIView.animate(withDuration: 0.5, delay: 0, usingSpringWithDamping: 0.7, initialSpringVelocity: 0.5, options: [], animations: { ... })
```

> **출처:** [The Physics Behind Spring Animations — Maxime Heckel](https://blog.maximeheckel.com/posts/the-physics-behind-spring-animations/)

### Spring vs Ease 비교

| 특성 | Ease (cubic-bezier) | Spring |
|------|-------------------|--------|
| 중단 시 전환 | 부자연스러운 점프 | 현재 속도 유지하며 자연 전환 |
| 오버슈트 | 불가 | friction에 따라 조절 |
| 동적 목표 변경 | 어려움 | 자연스러움 |
| 듀레이션 | 명시적 지정 | 물리 시뮬레이션에 의해 결정 |
| 디버깅 | 쉬움 | 파라미터 조합이 비직관적일 수 있음 |

### UI별 권장 Spring 설정

| 용도 | Stiffness | Damping | Mass | 특성 |
|------|----------|---------|------|------|
| 버튼 프레스 | 300 | 15 | 0.5 | 빠르고 스냅 |
| 모달 진입 | 200 | 20 | 1 | 부드럽고 안정 |
| 드래그 릴리즈 | 150 | 12 | 1 | 탄성적, 약간의 바운스 |
| 페이지 전환 | 250 | 25 | 1.2 | 무겁고 의도적 |

---

## Lottie & Rive

복잡한 애니메이션은 CSS/JS 코드만으로 유지보수가 어렵다. 전용 애니메이션 도구가 필요한 시점이 있다.

### 도구 선택 기준

| 기준 | CSS Animation | Lottie | Rive |
|------|--------------|--------|------|
| **최적 용도** | 간단한 상태 전환, hover/focus | 재생 전용 일러스트 애니메이션 | 인터랙티브, 상태 기반 UI 애니메이션 |
| **파일 크기** | 0 (코드 내장) | 10-100KB (JSON) | 1-20KB (바이너리) |
| **렌더링** | CPU (composited) | CPU (Lottie-web), GPU (lottie-light) | GPU (WebGL/Metal) |
| **프레임레이트** | 60fps (단순 시) | ~17fps (복잡 시) | ~60fps |
| **인터랙션** | 완전 지원 | 제한적 (dotLottie interactivity) | 완전 지원 (State Machine) |
| **워크플로** | 개발자가 직접 작성 | After Effects → Bodymovin 플러그인 | Rive 에디터에서 직접 |
| **플랫폼** | 웹 전용 | 웹, iOS, Android, Flutter, React Native | 웹, iOS, Android, Flutter, React Native |

> **출처:** [Advanced UI Animation Strategies: When to Use CSS, Lottie, Rive, JS, or Video — Medium](https://medium.com/@vacmultimedia/advanced-ui-animation-strategies-when-to-use-css-lottie-rive-js-or-video-56289e8d2629)

### 파일 크기 예산

- **아이콘 애니메이션**: < 5KB
- **로딩 애니메이션**: < 15KB
- **일러스트 애니메이션**: < 50KB
- **히어로 애니메이션**: < 100KB
- **전체 페이지 합산**: 200KB 이내

> **출처:** [Lottie vs Rive: Optimizing Mobile App Animation — Callstack](https://www.callstack.com/blog/lottie-vs-rive-optimizing-mobile-app-animation)

### 선택 의사결정 트리

```
애니메이션이 필요한가?
├─ CSS로 구현 가능한가? (단순 전환, hover, 스피너)
│   └─ Yes → CSS 사용
├─ 사용자 입력에 반응해야 하는가?
│   ├─ Yes → Rive (State Machine)
│   └─ No → 재생만 필요한가?
│       ├─ Yes → 팀이 After Effects를 사용하는가?
│       │   ├─ Yes → Lottie
│       │   └─ No → Rive
│       └─ No → Rive
└─ 비디오급 복잡도인가?
    └─ Yes → MP4/WebM 비디오
```

### 성능 고려사항

- Lottie-web(기본)은 SVG 렌더러를 사용하며 복잡한 애니메이션에서 프레임 드롭이 발생한다. `lottie-light`(Canvas 렌더러)나 `@lottiefiles/dotlottie-web`을 대안으로 검토한다.
- Rive는 자체 렌더러로 GPU 가속을 활용하므로 복잡한 애니메이션에서도 60fps를 유지한다. 다만 WebGL 컨텍스트를 사용하므로 한 페이지에 너무 많은 Rive 캔버스는 피한다.
- 모바일에서 Lottie JSON을 dotLottie(.lottie)로 변환하면 파일 크기가 50-80% 감소한다.

> **출처:** [Rive vs Lottie — Rive Blog](https://rive.app/blog/rive-as-a-lottie-alternative)

---

## 애니메이션 토큰 시스템

색상, 타이포그래피에 토큰이 있듯이 애니메이션에도 토큰이 필요하다. 토큰은 디자이너와 개발자가 동일한 어휘로 소통하게 하고, 일관성을 보장한다.

### 듀레이션 토큰

| 토큰 | 값 | 용도 |
|------|-----|------|
| `duration-instant` | 50ms | 체크박스, 토글 스위치 |
| `duration-fast` | 100ms | 버튼 피드백, 리플 |
| `duration-normal` | 200ms | 카드 호버, 드롭다운 |
| `duration-moderate` | 300ms | 모달 진입, 바텀시트 |
| `duration-slow` | 400ms | 페이지 전환, 대형 레이아웃 변경 |
| `duration-slower` | 600ms | 복잡한 코레오그래피, 시퀀스 |

### 이징 토큰

| 토큰 | 값 | 용도 |
|------|-----|------|
| `ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | 화면 내 요소 이동 |
| `ease-enter` | `cubic-bezier(0, 0, 0, 1)` | 요소 진입 (감속) |
| `ease-exit` | `cubic-bezier(0.3, 0, 1, 1)` | 요소 퇴장 (가속) |
| `ease-emphasis` | `cubic-bezier(0.05, 0.7, 0.1, 1)` | 강조 진입 |
| `ease-linear` | `linear` | 색상, 투명도 변화 |
| `ease-spring` | `linear(0, 0.009, ...)` | 스프링 근사 |

### 딜레이 토큰

| 토큰 | 값 | 용도 |
|------|-----|------|
| `delay-none` | 0ms | 즉시 반응이 필요한 피드백 |
| `delay-stagger` | 30ms | 리스트/그리드 스태거 간격 |
| `delay-sequence` | 80ms | 코레오그래피 시퀀스 간격 |
| `delay-entrance` | 150ms | 첫 번째 요소 등장 대기 |

> **출처:** [Animation/Motion Design Tokens — Medium](https://medium.com/@ogonzal87/animation-motion-design-tokens-8cf67ffa36e9)

### CSS Custom Properties 구현

```css
:root {
  --duration-instant: 50ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-moderate: 300ms;
  --duration-slow: 400ms;
  --duration-slower: 600ms;

  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-enter: cubic-bezier(0, 0, 0, 1);
  --ease-exit: cubic-bezier(0.3, 0, 1, 1);
  --ease-emphasis: cubic-bezier(0.05, 0.7, 0.1, 1);

  --delay-stagger: 30ms;
  --delay-sequence: 80ms;
}
```

> **출처:** [5 Steps for Including Motion Design in Your System — DesignSystems.com](https://www.designsystems.com/5-steps-for-including-motion-design-in-your-system/)

---

## 성능 최적화

60fps는 프레임당 **16.67ms** 예산이다. 이 안에 JavaScript 실행, 스타일 계산, 레이아웃, 페인트, 컴포지팅이 모두 완료되어야 한다.

### 렌더링 파이프라인과 애니메이션

```
JavaScript → Style → Layout → Paint → Composite
```

- **Composite만 트리거**: `transform`, `opacity` — GPU에서 처리, 메인 스레드 비차단
- **Paint 트리거**: `background-color`, `box-shadow` — 레이아웃은 안 바꾸지만 리페인트 발생
- **Layout 트리거**: `width`, `height`, `margin`, `padding` — 전체 파이프라인 재실행, **절대 애니메이션하지 않는다**

> **출처:** [CSS and JavaScript Animation Performance — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance)

### will-change 사용법

`will-change`는 브라우저에 "이 요소가 곧 변할 것"이라 알려 GPU 레이어를 미리 생성하게 한다.

```css
/* 올바른 사용: 호버 시에만 활성화 */
.card:hover { will-change: transform; }
.card:active { transform: scale(0.98); }

/* 잘못된 사용: 모든 요소에 상시 적용 */
* { will-change: transform, opacity; } /* GPU 메모리 폭발 */
```

**규칙:**
- 페이지당 1-2개 요소에만 적용
- 애니메이션 직전에 추가, 완료 후 제거
- `transform: translateZ(0)` 해킹 대신 `will-change` 사용

> **출처:** [Updates in Hardware-Accelerated Animation Capabilities — Chrome for Developers](https://developer.chrome.com/blog/hardware-accelerated-animations)

### requestAnimationFrame

JavaScript로 애니메이션할 때는 반드시 `requestAnimationFrame`(rAF)을 사용한다. `setInterval`이나 `setTimeout`은 프레임과 동기화되지 않아 프레임 드롭의 원인이 된다.

```javascript
function animate(timestamp) {
  // 16.67ms 예산 내에서 업데이트
  element.style.transform = `translateX(${position}px)`;
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### GPU Acceleration 체크리스트

- [ ] `transform`과 `opacity`만 애니메이션하는가?
- [ ] `will-change`를 필요한 요소에만 적용했는가?
- [ ] `position: fixed/absolute` 요소가 독립 레이어를 형성하는가?
- [ ] 큰 이미지/캔버스에 `contain: strict`를 적용했는가?
- [ ] 동시에 애니메이션하는 레이어가 10개 이하인가?

### Jank 감지

DevTools의 Performance 패널에서:
1. **Long Frame**: 16.67ms를 초과하는 프레임 (빨간 바)
2. **Layout Shift**: 예상치 못한 레이아웃 이동 (CLS)
3. **Forced Synchronous Layout**: JS에서 `.offsetHeight` 등을 읽은 직후 스타일 변경

> **출처:** [Animations and Performance — web.dev](https://web.dev/articles/animations-and-performance)

---

## 접근성

애니메이션 접근성은 선택이 아니라 **법적 의무**에 가깝다. WCAG 2.1은 Level A에서 발작 방지를, Level AAA에서 모션 감소를 요구한다.

### prefers-reduced-motion

사용자가 OS 설정에서 "모션 줄이기"를 활성화하면 이 미디어 쿼리가 `reduce`를 반환한다.

**구현 전략 — "제거"가 아닌 "대체":**

```css
/* 기본: 풀 애니메이션 */
.card-enter {
  animation: slideUp 300ms var(--ease-enter) forwards;
}

/* reduced-motion: 크로스페이드로 대체 */
@media (prefers-reduced-motion: reduce) {
  .card-enter {
    animation: fadeIn 150ms linear forwards;
  }
  .parallax, .hero-video { animation: none !important; }
}
```

모든 모션을 제거하면 상태 변화를 인지할 수 없다. **크로스페이드(opacity 전환)는 유지**하되, 위치 이동/회전/스케일 변환을 제거한다.

> **출처:** [prefers-reduced-motion — web.dev](https://web.dev/articles/prefers-reduced-motion)

### 전정 기관 장애 (Vestibular Disorders)

전정 기관은 균형감과 공간 인식을 담당한다. 장애가 있는 사용자는 대규모 모션에서 어지러움, 메스꺼움, 두통을 경험한다.

**위험 등급별 대응:**

| 위험도 | 모션 유형 | 대응 |
|--------|----------|------|
| 높음 | 시차 스크롤, 대규모 줌, 3D 회전 | 완전 제거 |
| 중간 | 흔들림(shake), 자동재생 비디오 | 크로스페이드로 대체 |
| 낮음 | 부드러운 스크롤, 앵커 링크 | 유지 가능 |
| 매우 낮음 | 150ms 이하 opacity 전환 | 항상 유지 |

> **출처:** [A11y Project — Understanding Vestibular Disorders](https://www.a11yproject.com/posts/understanding-vestibular-disorders/)

### 발작 위험 — WCAG 2.3.1 / 2.3.3

**WCAG 2.3.1 (Level A):** 콘텐츠에 1초에 3회 이상 깜빡이는 요소가 없어야 한다. 빨간색 번쩍임(red flash)은 특히 위험하다 — 광과민성 간질 환자에게 발작을 유발할 수 있다.

**WCAG 2.3.3 (Level AAA):** 인터랙션으로 트리거되는 모션 애니메이션을 비활성화할 수 있어야 한다. `prefers-reduced-motion`을 존중하면 자동으로 충족된다.

> **출처:** [Understanding Success Criterion 2.3.1 — W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html)

### 접근성 체크리스트

- [ ] `prefers-reduced-motion: reduce` 시 위치 이동/회전/스케일 모션이 크로스페이드로 대체되는가?
- [ ] 자동 재생 애니메이션에 일시정지/중지 컨트롤이 있는가?
- [ ] 1초에 3회 이상 깜빡이는 요소가 없는가?
- [ ] 빨간색 번쩍임이 전체 화면의 25% 미만인가?
- [ ] 스크롤 연동 애니메이션이 reduced-motion 시 비활성화되는가?
- [ ] 5초 이상 자동 재생되는 콘텐츠에 정지 버튼이 있는가?

> **출처:** [Web Accessibility for Seizures and Physical Reactions — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Seizure_disorders)
