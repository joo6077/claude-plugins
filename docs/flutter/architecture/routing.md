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

## Gotchas

- **go_router active feature development 크지 않음** — 메이저 신기능보다 안정화 위주. 최신 변경사항은 CHANGELOG로 확인.
- **auto_route는 코드생성 의존** — CI에 `build_runner` 단계가 반드시 필요하고, 생성 파일 커밋 정책을 명확히 정해야 한다.
