---
title: 상태 관리
version: 0.2.0
last_updated: 2026-08-13
---

<!-- 코드 펜스 규약: 이 문서의 fenced code block 은 백틱 4 개로 연다/닫는다.
     닫는 펜스를 백틱 3 개 단독 줄로 되돌리지 마라 — bare-fence 검사 오라클이
     닫는 펜스를 언어 힌트 없는 여는 펜스로 오탐한다 (Phase 5 AP-03). -->

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

````dart
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
````

- 출처: https://docs-v2.riverpod.dev/docs/providers/notifier_provider

### State 설계 원칙

| 상태 유형 | 관리 위치 | 예시 |
|----------|----------|------|
| 서버 데이터 (캐시) | AsyncNotifierProvider | 상품 목록, 사용자 프로필 |
| UI 로컬 상태 | useState (hooks) 또는 StateProvider | 탭 인덱스, 폼 입력 |
| 앱 전역 설정 | NotifierProvider | 테마 모드, 로케일 |
| 인증 상태 | AsyncNotifierProvider + StreamProvider | 로그인/로그아웃 |

### ref 4종의 역할 분리 — watch / listen / invalidate / refresh

| API | 역할 | 쓰는 곳 |
|-----|------|--------|
| `ref.watch` | **선언형 구독** — source 가 바뀌면 자동 재평가 | build / Notifier build / 파생 provider |
| `ref.listen` | **side effect** — dialog, navigation, logging | build 안에서 등록, 콜백에서 부수효과 |
| `ref.invalidate` | 현재 state 를 버리고 **다음 read 때 재평가** | mutation 후 영향 provider 정리 |
| `ref.refresh` | invalidate 후 즉시 read 하는 sugar | **즉시 새 값이 필요할 때만** |

- **파생 값은 `ref.watch(source.select(...))` 로 연결한다.** `ref.read` 로 계산해 state 에
  캐시하면 source 변경이 화면에 반영되지 않는다 — 이미 렌더된 화면이 이전 값을 계속 보여준다
- **화면 캐시에 영향을 주는 write 후에는 영향 provider 목록을 열거해 `invalidate` 한다.**
  목록은 write 메서드 옆에 주석으로 남겨야 리뷰에서 누락을 잡을 수 있다
- **`family` 전체를 통째로 invalidate 하지 마라.** stale 은 줄지만 네트워크 재요청과 UX 흔들림이
  커진다. 영향받는 인자 조합만 지정한다
- `Ref.onManualInvalidation()` (**`flutter_riverpod` 3.4.x 이상 전용**) 으로 source 의 수동
  invalidation 을 파생 provider 에 전파할 수 있다. `pubspec.lock` 의 버전을 확인하고 쓴다

출처: https://riverpod.dev/docs/concepts2/refs , https://pub.dev/packages/flutter_riverpod/changelog

### Provider 선택 플로우차트

1. 외부 값을 그대로 노출? → `Provider`
2. 비동기 데이터 fetch? → `FutureProvider` (단순) 또는 `AsyncNotifierProvider` (CRUD 포함)
3. 스트림 구독? → `StreamProvider`
4. 동기 상태 + 로직? → `NotifierProvider`
5. `@riverpod` codegen 사용 시 위 구분이 자동으로 결정됨

## 테스트 전략

- unit test 는 `ProviderContainer.test()` 로 격리 환경 생성 — 컨테이너를 테스트 간 공유하지 않는다
- `overrideWith`로 mock repository 주입 (override 는 `ProviderScope` / `ProviderContainer` 의 `overrides` 로만)
- `container.listen`으로 상태 전이 순서(loading → data) 검증. `autoDispose` provider 는 `read` 만 하면 중간에 dispose 될 수 있어 `listen` 으로 붙잡아야 한다
- **화면이 provider 변화를 반영하는지**는 unit test 로 못 잡는다 — `ProviderScope` 루트 + `tester.container()` 하네스가 필요하다 (`docs/flutter/quality/testing.md` §Riverpod widget test 하네스)
- 출처: https://riverpod.dev/docs/how_to/testing

## Gotchas

- `ChangeNotifierProvider`는 Riverpod 공식 문서상 scalable app에서는 **migration 용도로만** 권장된다. 새 코드는 `Notifier` / `AsyncNotifier`를 쓰는 편이 장기적으로 안전하다.
- sealed union + `Result.when` 분기는 강력하지만 단순 로그인 폼처럼 상태가 3개 이하인 화면에는 과한 ceremony가 된다. 화면당 상태 수를 보고 판단하라.
- `ref.watch`를 `onPressed` callback 안에서 호출하면 안 된다 — callback 내부는 `ref.read`만 허용된다. watch는 build 메서드(또는 Notifier의 build)에서만 호출하라.
- `autoDispose`를 모든 provider에 붙이면 화면 전환 시 캐시가 사라져 불필요한 재요청이 발생한다 — keepAlive를 조합하거나 autoDispose 없이 명시적 invalidate를 쓰라.
- **`autoDispose` 의 실제 수명**: listener 가 0 이 된 **즉시가 아니라 한 프레임 후** dispose 된다. 그리고 provider 가 recompute 되면 **autoDispose 여부와 무관하게 기존 state 가 파괴**된다 — "keepAlive 니까 값이 유지된다" 는 recompute 앞에서 성립하지 않는다. `family` / 파라미터 provider 는 인자 조합마다 인스턴스가 쌓이므로 autoDispose 가 권장된다. 출처: https://riverpod.dev/docs/concepts2/auto_dispose
