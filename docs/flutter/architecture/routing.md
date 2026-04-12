---
title: 라우팅
version: 0.1.0
last_updated: 2026-04-05
---

# 라우팅

GoRouter vs auto_route vs Navigator 2.0 선택 기준, 중첩 라우트, 가드, 딥링크, URL 전략, 전환 애니메이션을 다룬다.

---

## 원칙

### 1. 복잡한 딥링크/웹 URL 동기화/다중 Navigator 시 Router 기반 필수

단순 push/pop만 있는 앱은 Navigator 1로 충분하지만, 딥링크·웹 URL 동기화·중첩 Navigator가 필요하면 Router API(go_router, auto_route) 기반으로 가야 한다.

> **출처:** [Flutter Navigation Overview](https://docs.flutter.dev/ui/navigation)

### 2. go_router는 Flutter team 배포, URL 선언형, redirect, ShellRoute, 딥링크 지원

공식 권장 라우팅 패키지. URL 기반 선언형 라우팅, redirect로 가드, ShellRoute로 중첩 네비게이션, 딥링크를 기본 제공.

> **출처:** [go_router on pub.dev](https://pub.dev/packages/go_router)

### 3. auto_route는 코드 생성 기반 strongly-typed, nested, guards, tab routing 제공

build_runner 기반 코드 생성으로 type-safe 라우트 인자. 중첩 라우팅과 가드, 탭 라우팅을 제공.

> **출처:** [auto_route on pub.dev](https://pub.dev/packages/auto_route)

### 4. 중첩 네비게이션은 go_router의 ShellRoute, auto_route의 AutoTabsRouter로 구성

BottomNavigationBar 같은 탭별 독립 back stack이 필요할 때 이 구조를 사용한다.

> **출처:** [go_router on pub.dev](https://pub.dev/packages/go_router), [auto_route on pub.dev](https://pub.dev/packages/auto_route)

### 5. 웹 URL 전략은 기본 hash, PathUrlStrategy 적용 시 서버 rewrite 필수

`usePathUrlStrategy()`로 `#` 제거 시, 모든 경로를 `index.html`로 rewrite하도록 서버 설정이 반드시 따라와야 한다.

> **출처:** [Flutter URL Strategies](https://docs.flutter.dev/ui/navigation/url-strategies)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| go_router 최신 버전 | 17.2.0 |
| auto_route 최신 버전 | 11.1.0 |
| CustomTransitionPage 기본 전환 시간 | 300ms |
| adaptive 레이아웃 분기점 | 600dp |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| auth 상태를 build 안에서 imperative push/pop | 상태-라우트 불일치, race condition |
| 딥링크 필요한데 Navigator 1 named routes 사용 | URL 동기화/딥링크 불가 |
| 탭별 독립 back stack 필요한데 단일 Navigator | 탭 전환 시 스택 공유로 UX 붕괴 |
| PathUrlStrategy만 켜고 서버 rewrite 미설정 | 새로고침 시 404 |

---

## 실전 패턴

### GoRouter 기본 설정

```dart
final router = GoRouter(
  initialLocation: '/',
  redirect: (context, state) {
    final isLoggedIn = ref.read(authProvider).isLoggedIn;
    final isLoginRoute = state.matchedLocation == '/login';
    if (!isLoggedIn && !isLoginRoute) return '/login';
    if (isLoggedIn && isLoginRoute) return '/';
    return null; // no redirect
  },
  routes: [
    GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
    GoRoute(path: '/login', builder: (_, __) => const LoginPage()),
    ShellRoute(
      builder: (_, __, child) => MainShell(child: child),
      routes: [ /* nested tabs */ ],
    ),
  ],
);
```

- 출처: https://pub.dev/documentation/go_router/latest/

### ShellRoute로 탭 네비게이션

`ShellRoute`를 사용하면 탭 전환 시에도 shell(BottomNavigationBar)이 유지되고, 각 탭은 독립적 네비게이션 스택을 가질 수 있다.

- `StatefulShellRoute.indexedStack` — 각 탭의 상태를 보존하면서 탭 전환
- 출처: https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html

### 딥링크 + 인증 가드 조합

```text
1. 딥링크 수신 → GoRouter redirect 실행
2. 미인증? → /login으로 redirect + 원래 경로를 queryParam에 저장
3. 로그인 성공 → queryParam의 returnTo로 redirect
```

### Route 별 transition

```dart
GoRoute(
  path: '/detail/:id',
  pageBuilder: (context, state) => CustomTransitionPage(
    key: state.pageKey,
    child: DetailPage(id: state.pathParameters['id']!),
    transitionsBuilder: (_, animation, __, child) =>
        FadeTransition(opacity: animation, child: child),
  ),
)
```

## 테스트 전략

- `GoRouter.of(context).go('/path')`를 widget test에서 검증하려면 `GoRouter`를 `MaterialApp.router`에 주입
- `MockGoRouter`로 `go`/`push` 호출 여부 검증
- 출처: https://pub.dev/packages/go_router#testing

## Gotchas

- **go_router active feature development 크지 않음** — 메이저 신기능보다 안정화 위주. 최신 변경사항은 CHANGELOG로 확인.
- **auto_route는 코드생성 의존** — CI에 `build_runner` 단계가 반드시 필요하고, 생성 파일 커밋 정책을 명확히 정해야 한다.
- **`context.go` vs `context.push`** — `go`는 스택을 교체, `push`는 스택에 추가. "뒤로가기"가 필요하면 push, 탭 전환처럼 완전히 이동이면 go.
- **redirect 무한 루프** — redirect 함수에서 자기 자신의 경로로 redirect하면 무한 루프. redirect 내에서 "이미 해당 경로면 null 반환" 조건이 필수다.
