---
name: flutter-screen
description: >
  Flutter Screen 또는 Page 위젯을 생성하고 GoRouter/auto_route에 등록한다.
  StatelessWidget/HookConsumerWidget 기반 화면, 바텀 네비 탭(Screen), push 진입(Page) 구분.
  "화면 추가", "페이지 만들어줘", "screen 생성", "page 생성",
  "new screen", "new page", "route 추가", "라우트 등록" 같은 Flutter 프로젝트 요청 시 트리거.
argument-hint: "<feature>"
user-invocable: true
---

## Gotchas

- 네비게이션은 `go_router_builder` 생성 Route 클래스로만 — `context.go('/path')` 문자열 경로 직접 사용 금지
- 페이지 전환 애니메이션 커스텀 적용 금지 — `buildPage` 대신 `build`로 위젯만 반환. 예외: 탭 전환 시 `buildNoTransition`만 허용
- BottomSheet에 SafeArea 래핑 금지 — `MediaQuery.paddingOf(context).bottom`으로 내부에서 처리
- Flutter 3.38+에서 `PredictiveBackPageTransitionBuilder`가 Android 기본 페이지 전환이 됨 — 커스텀 전환 적용 시 Android에서 시스템 백 제스처와 충돌할 수 있으므로 확인 필요
- **go_router 17.0 breaking change** — `ShellRoute` 가 기본으로 GoRouter observer 에 알림을 보내게 변경됨. 기존에 observer 가 ShellRoute 이벤트를 받지 않는다고 가정한 코드는 의도치 않은 동작 발생 가능. `notifyRootObserver: false` 파라미터로 이전 동작을 복원할 수 있다. 최소 SDK 요구사항: Flutter 3.32 / Dart 3.8 (출처: Context7 `/websites/pub_dev_packages_go_router` 2026-04-24 기준 v17.2.2)
- **Enumerate-before-Act (low-freedom 영역 · skill-design-guide §5.5)** — 새 화면/페이지 추가 전에 (a) 기존 route path · route name enum/extension 을 `grep -r "GoRoute\|TypedGoRoute\|AutoRoute" lib/` 로 **전수 나열** 하고, (b) 동일 feature 의 기존 Screen/Page 파일을 `ls lib/features/$ARGUMENTS/presentation/` 으로 전수 확인한 뒤, (c) Screen vs Page · 경로 · 파라미터 후보를 1..N 인덱스로 사용자에게 제시한다. 근사치로 "아마 /workout 일 것" 이라고 추정하면 기존 라우트와 충돌하거나 중복 생성된다 (insights-report #2 Wrong approach 대응)
- **요청한 화면만 만들어라 — 동반 provider/state/usecase 를 임의로 끼워 넣지 마라 (insights-report #3 과잉설계 대응).** "화면 추가" 요청에 state notifier·API 레이어·캐시를 함께 스캐폴딩하지 마라. 화면이 명백히 상태나 데이터를 필요로 해도, 그것을 자동 생성하지 말고 화면 골격만 만든 뒤 "이 화면에 provider/API 가 필요하면 `flutter-provider` / `flutter-api` 로 이어가겠다" 고 안내한다. 더 큰 구조가 필요해 보이면 생성 전에 먼저 물어라

Screen 또는 Page를 생성하고 라우터에 등록한다.

**Screen vs Page 기준:**
- **Screen** = 바텀 네비게이션 탭에 등록된 최상위 화면
- **Page** = 독립 라우트가 있지만 바텀 네비에는 없는 화면 (push로 진입)

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `HAS_RIVERPOD`, `HAS_GO_ROUTER`, `HAS_GO_ROUTER_BUILDER`, `HAS_HOOKS` 등)를 사용한다.

## Input

`$ARGUMENTS`: feature name in snake_case (e.g., `workout`, `profile`, `settings`)

## Steps

### 1. 대상 경로 확인

ARCH에 따라 대상 경로를 결정한다:
- `ARCH = clean` / `feature_first`: `lib/features/$ARGUMENTS/` 존재 확인. 없으면 중단하고 `flutter-feature` 스킬 안내.
- `ARCH = flat`: `lib/features/` 구조가 없으면 `lib/src/` 또는 `lib/` 직하에 생성. 프로젝트의 기존 screen 파일 위치를 참조한다.

### 2. 기존 패턴 분석

기존 screen/page 파일과 라우트 등록을 읽어 프로젝트 관습을 파악한다:
- `lib/features/$ARGUMENTS/presentation/` 내 기존 파일
- 라우터 파일 위치와 등록 패턴 (기존 코드에서 감지)
- 네이밍 관습: `Screen` vs `Page` vs `View` 접미사
- Widget base class: `ConsumerWidget`, `HookConsumerWidget`, `StatelessWidget` 등

### 3. 사용자 확인

다음을 확인한다:
- **Screen인지 Page인지** (바텀 네비 탭 여부)
- Route path (e.g., `/workout`, `/settings`)
- Route parameters 필요 여부

### 4. Widget Base Class 결정

프로젝트 감지 결과에 따라:

| 조건 | Base Class |
|------|-----------|
| `HAS_HOOKS` + `HAS_RIVERPOD` | `HookConsumerWidget` |
| `HAS_RIVERPOD` (hooks 없음) | `ConsumerWidget` |
| `HAS_HOOKS` (riverpod 없음) | `HookWidget` |
| 둘 다 없음 | `StatelessWidget` |

기존 코드에서 다른 base class를 사용하고 있으면 그것을 따른다.

> **HAS_AUTO_ROUTE 프로젝트는 Route 클래스가 codegen으로 자동 생성되므로 수동 Route 클래스 작성이 불필요하다.**

### 5. Screen 생성

생성할 파일이 이미 존재하면 사용자에게 덮어쓸지 확인한다.

**Screen인 경우** — `lib/features/$ARGUMENTS/presentation/${ARGUMENTS}_screen.dart`:

```dart
import 'package:flutter/material.dart';
// HAS_RIVERPOD: import 'package:flutter_riverpod/flutter_riverpod.dart';
// HAS_HOOKS: import 'package:hooks_riverpod/hooks_riverpod.dart';

class <Feature>Screen extends <BaseClass> {
  const <Feature>Screen();

  @override
  Widget build(BuildContext context, /* WidgetRef ref - if Riverpod */) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('<Feature>'),
      ),
      body: const Center(
        child: Text('<Feature> Screen'),
      ),
    );
  }
}
```

### 6. Page 생성

**Page인 경우** — `lib/features/$ARGUMENTS/presentation/pages/${name}_page.dart`:

```dart
import 'package:flutter/material.dart';

class <Name>Page extends <BaseClass> {
  const <Name>Page();

  @override
  Widget build(BuildContext context, /* WidgetRef ref - if Riverpod */) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('<Name>'),
      ),
      body: const Center(
        child: Text('<Name> Page'),
      ),
    );
  }
}
```

### 7. 라우트 등록

프로젝트의 라우터 설정에 따라 등록 방식을 분기한다.

#### HAS_GO_ROUTER_BUILDER (TypedGoRoute codegen)

라우터 파일에 `@TypedGoRoute` 엔트리를 추가한다:

```dart
// Screen → 바텀 네비 탭의 최상위 라우트
@TypedGoRoute<<Feature>Route>(path: '/<feature>')

// Page → 일반 라우트
@TypedGoRoute<<Name>Route>(path: '/<name>')
```

Route 클래스 패턴은 프로젝트마다 다를 수 있다. 기존 Route 클래스를 읽어 패턴을 확인한다:
- `with $<Name>Route` mixin이 있으면 동일하게 사용 (go_router_builder 일부 버전)
- mixin 없이 `extends GoRouteData`만 사용하면 동일하게 따른다

```dart
// 프로젝트에 `with $<Name>Route` mixin 패턴이 있는 경우:
class <Name>Route extends GoRouteData with $<Name>Route {
  const <Name>Route();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const <Name>Screen(); // 또는 <Name>Page()
  }
}

// mixin 없이 extends만 사용하는 경우:
class <Name>Route extends GoRouteData {
  const <Name>Route();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const <Name>Screen(); // 또는 <Name>Page()
  }
}
```

**Type-Safe Navigation** (프로젝트가 go_router_builder를 사용하는 경우):

```dart
// 문자열 경로 직접 사용 금지
// context.go('/home');  // X

// Route 클래스 사용
const HomeRoute().go(context);                  // O — 네비게이션 스택 교체
DetailRoute(id: 'abc').push(context);             // O — 스택에 추가
const HomeRoute().replace(context);               // O — 현재 라우트를 교체
DetailRoute(id: 'abc').pushReplacement(context);  // O — push 후 현재 라우트 제거
```

#### HAS_GO_ROUTER (builder 없음)

```dart
GoRoute(
  path: '/<feature>',
  builder: (context, state) => const <Feature>Screen(),
),
```

#### StatefulShellRoute (바텀 네비 탭 + 탭별 독립 스택)

Screen 타입이 **바텀 네비게이션 탭이고 각 탭이 독립적인 네비게이션 히스토리를 유지**해야 하면 (예: 홈 탭에서 푸시한 detail 이 다른 탭으로 이동 후 돌아왔을 때 유지), `StatefulShellRoute.indexedStack` 을 사용한다. 2026 기준 go_router 공식 권장 패턴이다.

```dart
// lib/core/router/app_router.dart
StatefulShellRoute.indexedStack(
  builder: (context, state, navigationShell) {
    return ScaffoldWithNavBar(navigationShell: navigationShell);
  },
  branches: [
    StatefulShellBranch(
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeScreen(),
        ),
      ],
    ),
    StatefulShellBranch(
      // preload: true → 탭 최초 진입 전에 미리 빌드 (go_router 최신 지원)
      preload: true,
      routes: [
        GoRoute(
          path: '/profile',
          builder: (context, state) => const ProfileScreen(),
        ),
      ],
    ),
  ],
),
```

bottom navigation 은 `navigationShell.currentIndex` / `navigationShell.goBranch(index)` 로 제어한다. `navigationShell` 이 bottom nav 의 현재 index 와 탭 전환을 모두 담당하므로 별도 상태가 필요 없다.

출처:

- <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html>
- <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellBranch-class.html>
- <https://pub.dev/packages/go_router/changelog> (preload, notifyRootObserver)

#### HAS_AUTO_ROUTE

Screen/Page 클래스에 `@RoutePage()` annotation을 추가하고, 라우터 파일에 등록한다:

```dart
@RoutePage()
class <Name>Screen extends <BaseClass> {
  const <Name>Screen();
  // ...
}
```

라우터 파일(보통 `app_router.dart` 또는 `router.dart`)에 등록:
```dart
AutoRoute(page: <Name>Route.page, path: '/<name>'),
```

auto_route의 `@RoutePage()`는 build_runner codegen 대상이므로 생성 후 codegen 필요.

#### 라우터 없음

라우트 등록을 스킵한다. Navigator.push 패턴이나 프로젝트의 기존 네비게이션 패턴을 안내한다.

## Code Rules

- **MUST** Screen은 `presentation/` 직하에 `<feature>_screen.dart`로 배치하고, Page는 `presentation/pages/` 하위에 `<name>_page.dart`로 배치한다 — 프로젝트에 다른 관습이 있으면 그것을 따른다
- **MUST** 클래스명은 `<Feature>Screen` / `<Name>Page` (PascalCase) — 클래스명만으로 Screen/Page 역할이 드러나야 한다
- **MUST** import는 `package:$PACKAGE/...`만 사용 (상대경로 금지)
- **MUST** import 순서: `dart:` → `package:` (그룹 사이 빈 줄, 알파벳순)
- **MUST** `HAS_GO_ROUTER_BUILDER`인 경우 Route 클래스: `<Name>Route extends GoRouteData` 패턴
- **MUST NOT** 프로젝트에 없는 패키지를 import하는 코드를 생성하지 않는다

## After Creation

`HAS_BUILD_RUNNER`가 true이고 라우트를 등록했으면:
> "route codegen 파일을 생성하려면 실행하세요:
> `$DART run build_runner build --delete-conflicting-outputs`"

## Post-Creation: Widget Inspector

생성 완료 후 `widget-inspector` 에이전트를 quick 모드로 실행하여 변경 파일 주변의 재사용 가능한 위젯 패턴을 스캔한다. 추출 후보가 있으면 리포팅하고, 없으면 조용히 넘어간다.

## Related Skills

- Feature 디렉토리가 없으면 → `flutter-feature`
- 이 화면에서 사용할 Provider → `flutter-provider`
- Widget 생성 → `flutter-widget`
- 위젯 추출 → `flutter-extract`
- codegen 실행 → `flutter-run codegen`
