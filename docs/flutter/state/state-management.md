---
title: 상태 관리
version: 0.1.0
last_updated: 2026-04-05
---

# 상태 관리

## 요약

Riverpod / Bloc / Provider 비교와 선택 기준. Notifier·AsyncNotifier, `ref.mounted`, `copyWith`, `Result.when` 같은 핵심 패턴을 정리한다.

## 원칙

1. **변경 가능한 복잡 상태는 Riverpod의 `NotifierProvider` / `AsyncNotifierProvider`를 기본으로 쓴다.** 단순 파생값은 `Provider`, 비동기 로딩은 `AsyncNotifierProvider`.
   - 출처: https://docs-v2.riverpod.dev/docs/providers/notifier_provider

2. **`provider` 패키지는 얇은 `InheritedWidget` 래퍼, `flutter_bloc`은 이벤트/상태 전이 모델이다.** 팀 규모와 상태 복잡도에 맞춰 선택하고 한 프로젝트에서 혼용하지 않는다.
   - 출처: https://pub.dev/packages/provider
   - 출처: https://pub.dev/packages/flutter_bloc

3. **비동기 UI 상태는 `AsyncValue`처럼 loading / error / data 3 케이스 타입으로 표현한다.** `bool isLoading` + nullable data 조합 금지.
   - 출처: https://pub.dev/packages/flutter_riverpod

4. **상태 객체는 immutable + `copyWith` 기본.** `freezed`로 sealed union과 `copyWith`를 자동 생성한다.
   - 출처: https://pub.dev/packages/freezed

5. **Provider/Notifier 내부에서 `await` 이후 UI에 반영하기 전 `ref.mounted`를 확인한다.** dispose 이후 접근은 state 설정 예외를 발생시킨다.
   - 출처: https://pub.dev/documentation/flutter_riverpod/latest/flutter_riverpod/Ref-class.html

## 수치 기준

- `flutter_riverpod` 3.3.1, `flutter_bloc` 9.1.1, `provider` 6.1.5+1 (2026-04 기준 최신 안정)
- Provider 트리에 150개 이상의 `ChangeNotifierProvider`를 쌓으면 rebuild 추적 + stack overflow 위험이 커진다.
- 비동기 액션은 반드시 loading / error / data 3 상태를 명시 — nullable bool 하나로 표현하지 않는다.

## 안티패턴

- Notifier 바깥에서 state의 내부 필드를 직접 mutate (`state.items.add(...)`).
- `build` 메서드 안에서 HTTP/DB 호출을 바로 시작하는 구조.
- `loading`/`error`/`data`를 `bool isLoading` + nullable 값으로 표현.
- 같은 feature 안에 Bloc / Riverpod / Provider를 섞어 쓰는 구조.

## 실전 패턴

### AsyncNotifier 기본 구조

```dart
@riverpod
class ProductList extends _$ProductList {
  @override
  FutureOr<List<Product>> build() => _fetch();

  Future<List<Product>> _fetch() async {
    final repo = ref.read(productRepositoryProvider);
    return repo.getAll();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(_fetch);
  }

  Future<void> delete(String id) async {
    final prev = state.valueOrNull ?? [];
    state = AsyncData(prev.where((p) => p.id != id).toList()); // optimistic
    final result = await ref.read(productRepositoryProvider).delete(id);
    if (!ref.mounted) return;
    result.fold(
      (failure) { state = AsyncData(prev); /* rollback */ },
      (_) { /* success, already updated */ },
    );
  }
}
```

- 출처: https://docs-v2.riverpod.dev/docs/providers/notifier_provider

### State 설계 원칙

| 상태 유형 | 관리 위치 | 예시 |
|----------|----------|------|
| 서버 데이터 (캐시) | AsyncNotifierProvider | 상품 목록, 사용자 프로필 |
| UI 로컬 상태 | useState (hooks) 또는 StateProvider | 탭 인덱스, 폼 입력 |
| 앱 전역 설정 | NotifierProvider | 테마 모드, 로케일 |
| 인증 상태 | AsyncNotifierProvider + StreamProvider | 로그인/로그아웃 |

### ref.invalidate vs ref.refresh

- `ref.invalidate(provider)` — 다음 읽을 때 rebuild (lazy)
- `ref.refresh(provider)` — 즉시 rebuild 후 새 값 반환 (eager)
- 리스트 갱신은 `invalidate`로 충분, 즉시 새 값이 필요하면 `refresh`

출처: https://docs-v2.riverpod.dev/docs/concepts/combining_providers

### Provider 선택 플로우차트

1. 외부 값을 그대로 노출? → `Provider`
2. 비동기 데이터 fetch? → `FutureProvider` (단순) 또는 `AsyncNotifierProvider` (CRUD 포함)
3. 스트림 구독? → `StreamProvider`
4. 동기 상태 + 로직? → `NotifierProvider`
5. `@riverpod` codegen 사용 시 위 구분이 자동으로 결정됨

## 테스트 전략

- `ProviderContainer`로 격리된 테스트 환경 생성
- `overrideWith`로 mock repository 주입
- `container.listen`으로 상태 전이 순서(loading → data) 검증
- 출처: https://docs-v2.riverpod.dev/docs/essentials/testing

## Gotchas

- `ChangeNotifierProvider`는 Riverpod 공식 문서상 scalable app에서는 **migration 용도로만** 권장된다. 새 코드는 `Notifier` / `AsyncNotifier`를 쓰는 편이 장기적으로 안전하다.
- sealed union + `Result.when` 분기는 강력하지만 단순 로그인 폼처럼 상태가 3개 이하인 화면에는 과한 ceremony가 된다. 화면당 상태 수를 보고 판단하라.
- `ref.watch`를 `onPressed` callback 안에서 호출하면 안 된다 — callback 내부는 `ref.read`만 허용된다. watch는 build 메서드(또는 Notifier의 build)에서만 호출하라.
- `autoDispose`를 모든 provider에 붙이면 화면 전환 시 캐시가 사라져 불필요한 재요청이 발생한다 — keepAlive를 조합하거나 autoDispose 없이 명시적 invalidate를 쓰라.
