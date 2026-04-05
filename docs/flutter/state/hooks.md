---
title: Flutter Hooks
version: 0.1.0
last_updated: 2026-04-05
---

# Flutter Hooks

## 요약

`flutter_hooks`의 호출 규칙, `HookWidget` 계열 사용법, `useState` / `useEffect` / `useMemoized` / `useAnimationController` 기본 훅과 커스텀 훅 작성 패턴.

## 원칙

1. **Hook은 `HookWidget` / `StatefulHookWidget` / `HookConsumerWidget`의 `build` 메서드 안에서만, 항상 같은 순서로 호출한다.** 조건문/반복문 안에서 호출 금지.
   - 출처: https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/use.html

2. **`HookWidget`은 별도 lifecycle 메서드 없이 local state와 disposable 객체를 선언적으로 관리한다.** `StatefulWidget`의 보일러플레이트(`initState`/`dispose`)를 대체하는 용도.
   - 출처: https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/HookWidget-class.html

3. **목적별로 훅을 구분해 쓴다.** side effect는 `useEffect`, 비싼 계산 캐싱은 `useMemoized`, 순수 local ephemeral 값은 `useState`.
   - 출처: https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/useEffect.html

4. **`AnimationController`는 `useAnimationController`로 생성한다.** 수동 `dispose` 없이도 위젯 제거 시 자동 해제된다.
   - 출처: https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/

5. **Riverpod과 함께 쓸 때는 `HookConsumerWidget`을 사용한다.** `HookWidget` + `Consumer` 중첩은 피한다.
   - 출처: https://pub.dev/documentation/hooks_riverpod/latest/hooks_riverpod/HookConsumerWidget-class.html

## 수치 기준

- `flutter_hooks` 0.21.3+1, `hooks_riverpod` 3.3.1 (2026-04 기준 최신 안정).
- `useEffect`의 `keys` 인자는 의존 값 리스트 — 생략하면 매 build마다 effect가 재실행된다.

## 안티패턴

- 조건문/반복문 안에서 hook 호출 (`if (cond) useState(...)`).
- `useEffect`에 `keys` 인자 생략해서 매 build마다 effect가 재실행되는 구조.
- 전역/비즈니스 상태를 `useState`에 가둬 화면 재진입 시 날아가는 설계.
- `HookWidget`이 결국 `StatefulWidget`보다 코드가 길어지는데도 유지하는 선택.

## Gotchas

- Hook 호출 순서가 바뀌면 각 hook의 내부 상태 매핑이 깨진다. 리팩토링 중 훅을 재배치할 때 가장 자주 터지는 버그 포인트다.
- `useMemoized`는 **캐시**지 reactive recompute가 아니다. 값이 keys 변화 없이 바뀔 일이 있다면 `useState` + `useEffect` 조합이나 Riverpod provider로 빼라.
