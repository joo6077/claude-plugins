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

## Gotchas

- Rive는 renderer 선택과 Impeller 사용 환경에 따라 동작 차이가 있다 — iOS/Android/웹에서 동일하게 보이는지 QA 단계에서 반드시 확인하라.
- Lottie는 CPU/GPU 부담이 커질 수 있다 — 반복 재생되는 경우 `LottieOptions.enableMergePaths`, renderCache 등 옵션을 검토하라.
