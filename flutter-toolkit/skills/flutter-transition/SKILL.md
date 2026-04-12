---
name: flutter-transition
description: >
  GoRouter, auto_route, Navigator 기반 커스텀 페이지 전환 애니메이션을 적용한다.
  fade-slide, scale-fade, none 중 선택.
  라우트 전환 애니메이션, 페이지 전환 효과, transition,
  'fade로 바꿔줘', '전환 애니메이션 추가', 'page transition',
  'route animation', '화면 전환 효과' 같은 요청 시 트리거.
  이미 적용된 전환을 수정할 때도 사용한다.
argument-hint: "<route-name> [transition-type]"
user-invocable: true
---

## Gotchas

- fit-pal에서는 커스텀 페이지 전환이 금지되어 있다 (`buildPage` 대신 `build`로 위젯만 반환) — 프로젝트 규칙을 먼저 확인해라
- 예외: 탭 전환 시 `buildNoTransition`만 허용되는 프로젝트가 있다 — 프로젝트의 CLAUDE.md 또는 라우터 설정 확인
- **auto_route 11.0 breaking changes** — `redirect` 가 `redirectUntil` 로 리네이밍됐고, `navigateNamed` / `pushNamed` 등 deprecated named navigation 메서드가 제거됐다. `.named` 생성자로 codegen 없이 shorthand named route 를 사용할 수 있다. 기존 코드에 `redirect` 가 남아 있으면 컴파일 에러 발생 (출처: <https://pub.dev/packages/auto_route/changelog>)
- **Flutter 3.44 page transition builders 재구성 (pre-stable)** — 3.44 에서 page transition builders 가 재구성될 예정. 커스텀 전환 코드가 있으면 3.44 업그레이드 시 호환성 확인 필요 (출처: <https://docs.flutter.dev/release/breaking-changes>)

GoRouter, auto_route, Navigator 기반 커스텀 페이지 전환 애니메이션을 적용한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `HAS_GO_ROUTER`, `HAS_GO_ROUTER_BUILDER`, `HAS_AUTO_ROUTE`, `HAS_BUILD_RUNNER` 등)를 사용한다.

### 전제 조건

- `HAS_GO_ROUTER`가 true이면 GoRouter 기반 전환을 적용한다.
- `HAS_AUTO_ROUTE`가 true이면 아래 "HAS_AUTO_ROUTE" 섹션을 따른다.
- 둘 다 false이면 아래 "HAS_GO_ROUTER = false" 섹션의 범용 Navigator 전환 가이드를 따른다.

### HAS_AUTO_ROUTE

auto_route에서는 `CustomRoute`로 전환 애니메이션을 정의한다:

```dart
// app_router.dart
CustomRoute(
  page: <Name>Route.page,
  path: '/<name>',
  transitionsBuilder: TransitionsBuilders.fadeIn,
  durationInMilliseconds: 300,
  reverseDurationInMilliseconds: 200,
),
```

커스텀 전환이 필요하면:
```dart
CustomRoute(
  page: <Name>Route.page,
  path: '/<name>',
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(
      opacity: animation,
      child: SlideTransition(
        position: Tween(begin: const Offset(0, 0.1), end: Offset.zero)
            .animate(CurvedAnimation(parent: animation, curve: Curves.easeInOut)),
        child: child,
      ),
    );
  },
),
```

auto_route의 `TransitionsBuilders`에 내장된 전환 목록:
- `TransitionsBuilders.fadeIn` — fade
- `TransitionsBuilders.slideLeft` — slide from right
- `TransitionsBuilders.slideBottom` — slide from bottom
- `TransitionsBuilders.noTransition` — 전환 없음

### HAS_GO_ROUTER = false (범용 Navigator 전환)

GoRouter가 없어도 `PageRouteBuilder`로 커스텀 전환을 적용할 수 있다:

```dart
Navigator.push(context, PageRouteBuilder(
  pageBuilder: (context, animation, secondaryAnimation) => const TargetScreen(),
  transitionsBuilder: (context, animation, secondaryAnimation, child) {
    return FadeTransition(
      opacity: animation,
      child: SlideTransition(
        position: Tween(begin: const Offset(0, 0.1), end: Offset.zero).animate(
          CurvedAnimation(parent: animation, curve: Curves.easeInOut),
        ),
        child: child,
      ),
    );
  },
  transitionDuration: const Duration(milliseconds: 300),
  reverseTransitionDuration: const Duration(milliseconds: 200),
));
```

프로젝트에 애니메이션 상수가 있으면 Duration/Curve를 해당 상수로 대체한다. 이후 GoRouter 전용 섹션은 스킵한다.

### 애니메이션 상수 감지

프로젝트에서 애니메이션 상수 파일을 탐색한다:

| 탐색 패턴 | 감지 결과 |
|-----------|----------|
| `lib/**/constants/animation*` | 애니메이션 상수 파일 경로 |
| `lib/**/tokens/*anim*` 또는 `lib/**/tokens/*motion*` | 모션 토큰 파일 경로 |
| 없음 | 기본값 사용 |

감지된 파일이 있으면 Duration/Curve 상수를 읽어 사용한다.
없으면 아래 기본값을 사용한다.

## Input

`$ARGUMENTS`: `<route-name> [transition-type]`
- `/flutter-transition login scale-fade`
- `/flutter-transition workout fade-slide`
- `/flutter-transition home none`

## Transition Types

| 타입 | 용도 | forward Duration | reverse Duration | Curve |
|------|------|-----------------|-----------------|-------|
| `fade-slide` | 일반 페이지 (기본값) | 300ms | 200ms | `Curves.easeInOut` |
| `scale-fade` | 모달, 로그인, 온보딩 | 450ms | 200ms | `Curves.easeOutBack` |
| `none` | 탭 전환, 같은 레벨 | 0ms | 0ms | - |

프로젝트에 애니메이션 상수가 감지되면 위 Duration/Curve를 해당 상수로 대체한다.

## Page Transition Builders

### page_transitions.dart 생성/확인

프로젝트에 페이지 전환 빌더 파일이 있는지 확인한다:
- `lib/**/router/page_transitions.dart`
- `lib/**/transitions/`

없으면 생성한다. 위치는 라우터 파일과 같은 디렉토리:

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

// 프로젝트에 애니메이션 상수가 있으면 import
// import 'package:$PACKAGE/core/constants/animation_constants.dart';

/// fade + slide-up 전환. 일반 페이지 네비게이션에 사용.
CustomTransitionPage<void> buildFadeSlideTransition({
  required LocalKey key,
  required Widget child,
}) {
  return CustomTransitionPage<void>(
    key: key,
    child: child,
    transitionDuration: const Duration(milliseconds: 300),
    reverseTransitionDuration: const Duration(milliseconds: 200),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      final curved = CurvedAnimation(
        parent: animation,
        curve: Curves.easeInOut,
      );
      return FadeTransition(
        opacity: curved,
        child: SlideTransition(
          position: Tween<Offset>(
            begin: const Offset(0, 0.05),
            end: Offset.zero,
          ).animate(curved),
          child: child,
        ),
      );
    },
  );
}

/// scale + fade 전환. 모달성 페이지(로그인, 온보딩 등)에 사용.
CustomTransitionPage<void> buildScaleFadeTransition({
  required LocalKey key,
  required Widget child,
}) {
  return CustomTransitionPage<void>(
    key: key,
    child: child,
    transitionDuration: const Duration(milliseconds: 450),
    reverseTransitionDuration: const Duration(milliseconds: 200),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      final curved = CurvedAnimation(
        parent: animation,
        curve: Curves.easeOutBack,
      );
      return FadeTransition(
        opacity: curved,
        child: ScaleTransition(
          scale: Tween<double>(begin: 0.95, end: 1.0).animate(curved),
          child: child,
        ),
      );
    },
  );
}

/// 전환 없음. 탭 전환, 같은 레벨 이동에 사용.
CustomTransitionPage<void> buildNoTransition({
  required LocalKey key,
  required Widget child,
}) {
  return CustomTransitionPage<void>(
    key: key,
    child: child,
    transitionDuration: Duration.zero,
    reverseTransitionDuration: Duration.zero,
    transitionsBuilder: (context, animation, secondaryAnimation, child) =>
        child,
  );
}
```

프로젝트에 애니메이션 상수가 있으면 하드코딩된 `Duration`/`Curves`를 해당 상수로 교체한다.

## Steps

### 1. 전제 조건 확인

a. `HAS_GO_ROUTER` 확인
b. page_transitions 파일 존재 확인 -> 없으면 위 템플릿으로 생성
c. 애니메이션 상수 파일 감지 -> 있으면 import하여 사용

### 2. 라우트 파일 찾기

프로젝트의 라우트 정의 파일을 찾는다:
- `HAS_GO_ROUTER_BUILDER`: `TypedGoRoute` 어노테이션이 있는 파일
- 일반 GoRouter: `GoRoute(` 또는 `GoRouter(` 정의가 있는 파일

### 3. 대상 라우트 수정

#### TypedGoRoute (go_router_builder) 사용 시

`build` override를 `buildPage`로 변경:

**Before:**
```dart
@TypedGoRoute<WorkoutRoute>(path: '/workout')
class WorkoutRoute extends GoRouteData {
  const WorkoutRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const WorkoutScreen();
  }
}
```

**After:**
```dart
@TypedGoRoute<WorkoutRoute>(path: '/workout')
class WorkoutRoute extends GoRouteData {
  const WorkoutRoute();

  @override
  Page<void> buildPage(BuildContext context, GoRouterState state) {
    return buildFadeSlideTransition(
      key: state.pageKey,
      child: const WorkoutScreen(),
    );
  }
}
```

#### 일반 GoRoute 사용 시

`pageBuilder`를 추가/수정:

**Before:**
```dart
GoRoute(
  path: '/workout',
  builder: (context, state) => const WorkoutScreen(),
)
```

**After:**
```dart
GoRoute(
  path: '/workout',
  pageBuilder: (context, state) => buildFadeSlideTransition(
    key: state.pageKey,
    child: const WorkoutScreen(),
  ),
)
```

### 4. Import 추가

page_transitions 파일의 import를 추가한다:
```dart
import 'package:$PACKAGE/<path>/page_transitions.dart';
```

### 5. Codegen (필요 시)

`HAS_GO_ROUTER_BUILDER`이면 route codegen을 실행한다:
```bash
$DART run build_runner build --delete-conflicting-outputs
```

## Rules

- **MUST** 커스텀 전환에는 `build` 대신 `buildPage` override를 사용한다 (TypedGoRoute) 또는 `builder` 대신 `pageBuilder`를 사용한다 (GoRoute) -- `build`/`builder`는 Widget만 반환하므로 `CustomTransitionPage`를 감쌀 수 없다
- **MUST** `state.pageKey`를 `key` 파라미터로 전달한다 -- 같은 라우트를 다른 파라미터로 방문할 때 key가 없으면 Flutter가 위젯을 재사용하여 전환 애니메이션이 발생하지 않는다
- **MUST** 프로젝트에 애니메이션 상수가 있으면 사용한다 (하드코딩 Duration/Curve 금지) -- 전환 타이밍을 전역에서 일괄 조정할 수 있어야 모션 일관성이 유지된다
- **MUST** 모든 전환 빌더를 한 파일에 정의한다 -- 전환 빌더가 여러 파일에 흩어지면 중복 구현이 생기고 모션 일관성이 깨진다
- **MUST** 일반 네비게이션에는 `fade-slide`, 모달성 페이지에는 `scale-fade`를 사용한다 -- 사용자가 "앞으로 가기"와 "팝업"을 시각적으로 구분할 수 있어야 내비게이션 맥락이 명확해진다
- **MUST** `$FLUTTER` / `$DART` / `$PACKAGE` 변수를 사용한다. 하드코딩된 명령 prefix 및 패키지명 금지
- **MUST NOT** 플랫폼 기본 전환을 사용한다 -- 앱 전체에서 일관된 전환 경험을 제공해야 한다
