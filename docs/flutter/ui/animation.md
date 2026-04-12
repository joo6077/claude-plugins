---
title: 애니메이션
version: 0.1.0
last_updated: 2026-04-05
---

# 애니메이션

AnimationController, Tween, Hero, implicit vs explicit, Curves, Rive/Lottie, CustomPainter의 shouldRepaint를 다룬다.

## 원칙

1. **단순 property 변화는 implicit(AnimatedContainer 등), 정밀 제어가 필요하면 explicit(AnimationController)을 쓴다.** 선택 기준은 "직접 컨트롤/동기화/역재생이 필요한가"다.
   - 출처: https://docs.flutter.dev/ui/animations/implicit-animations , https://docs.flutter.dev/ui/animations/tutorial
2. **AnimationController는 vsync를 요구하며 반드시 dispose()해야 한다.** SingleTickerProviderStateMixin 또는 HookWidget의 useAnimationController로 자동 관리하라.
   - 출처: https://api.flutter.dev/flutter/animation/AnimationController-class.html
3. **Tween은 값 범위, Curve는 속도 곡선을 담당한다.** 둘을 분리해 조합하면 동일 animation에 다양한 interpolation을 붙일 수 있다.
   - 출처: https://api.flutter.dev/flutter/animation/Curves-class.html
4. **Hero는 shared element transition 전용이다.** route 간 "동일한 semantic element가 이동하는" 경우에만 쓰고, 단순 fade/slide에는 쓰지 마라.
   - 출처: https://docs.flutter.dev/ui/animations/hero-animations
5. **CustomPainter 기반 애니메이션은 shouldRepaint를 정확히 구현한다.** 애니메이션 값이 바뀔 때만 true를 반환해야 하며, 항상 true는 비용이 심각하다.
   - 출처: https://api.flutter.dev/flutter/rendering/CustomPainter/shouldRepaint.html

## 수치·경계값

- AnimationController는 60–120 fps에 맞춰 초당 60–120회 값을 갱신한다 — 내부 작업이 비싸면 프레임 드롭 원인이 된다.
- go_router `CustomTransitionPage`의 기본 transitionDuration은 300ms.
- Lottie 애니메이션은 보통 10–30 fps로 authored 되지만, `FrameRate.max`로 디바이스 refresh rate에 맞춰 재생할 수 있다.

## 안티패턴

- 단순 색/크기 변경에 AnimationController를 직접 만든다 — AnimatedContainer/AnimatedOpacity로 충분.
- AnimatedBuilder 내부에서 불변 subtree까지 rebuild — `child` 파라미터로 hoisting 하라.
- Hero tag 충돌 방치 — route 하나에 동일 tag가 둘 이상이면 런타임 assertion.
- CustomPainter의 shouldRepaint를 항상 true로 — 매 프레임 전체 repaint가 발생해 성능이 망가진다.

## 실전 패턴

### Staggered Animation

여러 위젯이 순차적으로 등장하는 패턴. `Interval`로 각 요소의 시작/끝 시점을 배분한다.

```dart
// Interval(0.0, 0.5) → 전체 duration의 전반부에서 실행
// Interval(0.3, 0.8) → 30%~80% 구간에서 실행
final slideAnim = Tween<Offset>(begin: Offset(0, 0.3), end: Offset.zero)
    .animate(CurvedAnimation(parent: controller, curve: Interval(0.0, 0.6, curve: Curves.easeOut)));
```

- 출처: https://docs.flutter.dev/ui/animations/staggered-animations

### AnimatedSwitcher vs PageRouteBuilder

같은 위치에서 위젯을 교체할 때는 `AnimatedSwitcher`, route 전환은 `PageRouteBuilder`/`CustomTransitionPage`를 쓴다. 혼동하면 layout shift가 발생한다.

- 출처: https://api.flutter.dev/flutter/widgets/AnimatedSwitcher-class.html

### RepaintBoundary 활용

애니메이션되는 위젯을 `RepaintBoundary`로 감싸면 해당 서브트리만 별도 레이어로 분리되어 나머지 UI의 repaint를 방지한다.

- 출처: https://api.flutter.dev/flutter/widgets/RepaintBoundary-class.html

## 성능 프로파일링

- DevTools의 "Performance Overlay"에서 UI thread와 Raster thread 모두 16ms 이내인지 확인
- `Timeline.startSync('animation_label')`로 특정 애니메이션의 비용을 측정
- Impeller 환경(iOS 기본, Android opt-in)에서는 shader compilation jank가 사라지므로 first-frame 성능이 개선됨
- 출처: https://docs.flutter.dev/perf/ui-performance

## Gotchas

- Rive는 renderer 선택과 Impeller 사용 환경에 따라 동작 차이가 있다 — iOS/Android/웹에서 동일하게 보이는지 QA 단계에서 반드시 확인하라.
- Lottie는 CPU/GPU 부담이 커질 수 있다 — 반복 재생되는 경우 `LottieOptions.enableMergePaths`, renderCache 등 옵션을 검토하라.
- AnimationController를 HookWidget에서 사용할 때 `useAnimationController`의 `duration` 파라미터 변경은 hot reload에서 반영되지 않을 수 있다 — restart가 필요하다.
- `addStatusListener`를 사용할 때 dispose에서 제거하지 않으면 메모리 릭이 발생한다. `useEffect`의 cleanup에서 반드시 제거하라.
