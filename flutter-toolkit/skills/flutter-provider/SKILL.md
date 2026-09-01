---
name: flutter-provider
description: >
  Riverpod Notifier + State 클래스를 생성한다.
  @Riverpod codegen, copyWith, ref.mounted 체크, Result.when 분기 패턴 포함.
  상태 관리 Provider를 만들 때 사용.
  "provider 만들어줘", "notifier 생성", "상태 관리", "state management",
  "riverpod provider", "notifier class" 같은 요청 시 트리거.
  `lib/features/<feature>/` 아래에 새 provider 파일을 생성하는 전용 스킬이다.
  이미 존재하는 컨트롤러·서비스·notifier 의 수정에는 트리거하지 않는다 (feature 디렉토리
  밖의 core/shared 파일 포함) — 그 경우 해당 파일을 직접 읽고 수정한다.
argument-hint: "<feature>/<provider-name>"
user-invocable: true
---

## Gotchas

- **요청 범위를 넘는 캐시/추상화/스캐폴딩을 임의 추가하지 마라 — 최소 구현 우선.** "상태 하나 추가"에 캐시 레이어·중간 provider·새 추상화를 끼워 넣지 말고, 요청한 provider만 만들어라. 더 큰 구조가 필요해 보이면 구현 전에 먼저 물어라
- keepAlive provider는 keepAlive provider만 참조해야 한다 — 비keepAlive를 참조하면 stale state 발생
- `ref.watch(provider)`로 전체 객체를 감시하면 불필요한 리빌드 — `ref.watch(provider.select((s) => s.isLoading))`으로 필요한 필드만 선택
- `Result<T>` 의 성공/실패 **양쪽 분기를 반드시 처리** — 한쪽만 처리하면 unhandled state. 분기 문법은 **신규 코드에서는 Dart pattern matching (switch expression) 을 우선**하되, `.when`/`.map` 을 금지 규칙으로 삼지 마라 — 이 메서드들은 Freezed 3.0 에서 제거됐다가 **3.1.0 에서 다시 추가**됐고 최신 stable 은 3.2.5 다. 프로젝트가 이미 generated `when`/`map` 을 쓰고 있으면 **기존 코드와의 일관성**을 우선한다 (출처: <https://pub.dev/packages/freezed/changelog>)
- `@Riverpod` codegen 사용 시 `build_runner`를 돌려야 `.g.dart` 생성됨 — 코드만 쓰고 codegen을 빠뜨리면 컴파일 에러
- **Riverpod 3.0 Notifier 재생성 라이프사이클** — 2.x의 pseudo-singleton 동작이 폐기됐다. provider 가 rebuild 될 때마다 Notifier 도 재생성되므로 **Timer/StreamSubscription/TextEditingController 등 생명주기 객체를 Notifier 의 필드로 직접 유지하면 리소스 누수**가 발생한다. 해결: 해당 객체를 **별도 provider 로 분리하고 `ref.onDispose(() => controller.dispose())` 로 바인딩**한다. 공식 권장 패턴은 async 메서드 끝에 `if (!ref.mounted) return;` 을 항상 붙이는 것이다 (출처: <https://riverpod.dev/docs/3.0_migration>, <https://riverpod.dev/docs/whats_new>)
- **Riverpod 3.0 legacy provider** — `StateNotifierProvider`, `StateProvider`, `ChangeNotifierProvider` 는 3.0 에서 legacy 로 분류됐다. 제거되지는 않았지만 메인 API 에서 제외되었으므로 **신규 코드는 `@riverpod` / `Notifier` / `AsyncNotifier` 기반**으로 작성한다. 기존 코드 마이그레이션 시에는 프로젝트의 기존 패턴을 존중하되, 새 파일에서 legacy 를 추가하지 않는다 (출처: <https://pub.dev/packages/flutter_riverpod/changelog>)
- **Riverpod 3.0 `==` 기반 알림 필터링** — 3.0 부터 모든 provider 가 상태 알림을 `==` 비교로 필터링한다. 특히 `StreamProvider`/`StreamNotifier` 에서 값 동등성이 있는 이벤트는 listener 에 전달되지 않는다. 모델에 `operator ==` / `hashCode` 를 정의하지 않으면 참조 동등성으로 판단되어 매번 알림이 발생하거나, Freezed/Equatable 로 값 동등성을 정의하면 같은 값이 필터링되므로 **의도한 동작을 명시적으로 설계**하라 (출처: <https://riverpod.dev/docs/whats_new>)
- Riverpod 3.0 에서 `.valueOrNull` 이 `.value` 로 변경됨 — 기존 코드에 `.valueOrNull` 이 있으면 마이그레이션 필요. `dart fix --apply` 로 자동 처리 가능
- Riverpod 3.0 에서 `Ref` 의 타입 파라미터가 제거됨 — `FutureProviderRef` / `StreamProviderRef` 등 subclass 가 전부 삭제됐다. 신규 코드는 **`Ref` 를 직접** 사용한다 (출처: <https://riverpod.dev/docs/3.0_migration>)
- Riverpod 3.0 의 offline persistence/mutations 는 아직 experimental (2026-03 기준 안정화 선언 없음) — 프로덕션에서는 수동 캐싱 패턴 유지 권장. mutations 는 폼 제출 등 사이드이펙트에 loading/success/error 상태를 자동 관리하지만 API 가 변경될 수 있다 (출처: <https://riverpod.dev/docs/whats_new>)
- **Riverpod 3.4.1 (2026-07-27 실측 최신) deprecation** — 3.2.0 부터 `family.overrideWith` 가 deprecated 되고 `family.overrideWith2` 가 권장된다 (4.0 에서 rename 예정). 3.4.0 부터 `SyncProviderTransformerMixin` 이 deprecated. 신규 API: `Ref.onManualInvalidation()`(수동 invalidation 감지·전파), `ProviderContainer.allProviders()`, `AsyncValue.requireValue`(3.1), `CustomProviderListenable` 과 `ValueListenable` 지원(3.4). mutations / offline persistence 는 **여전히 experimental** 이며 `package:riverpod/experimental/...` 경로로만 노출된다 — 프로덕션 코드에 넣지 마라 (출처: <https://pub.dev/packages/flutter_riverpod>, <https://pub.dev/packages/flutter_riverpod/changelog>)
- **파생 provider 는 source 를 `ref.watch` 로 연결한다 — `ref.read` 로 계산해 캐시하지 마라** — 다른 provider 의 값에서 파생되는 값은 `ref.watch(sourceProvider.select((s) => s.field))` 로 **선언형 연결**해야 source 가 바뀔 때 자동으로 재평가된다. 메서드 안에서 `ref.read` 로 읽어 state 에 저장해두면 그 순간의 스냅샷이 화면 캐시로 굳어 **stale 값이 계속 표시**된다. `ref.watch` 는 선언형 구독, `ref.listen` 은 dialog/navigation/logging 같은 **side effect** 용이다 — 둘을 바꿔 쓰지 마라 (출처: <https://riverpod.dev/docs/concepts2/refs>)
- **mutation 후 영향 provider 를 열거하고 `ref.invalidate` 하라 (실측 REJECT `LG-02`)** — 색상/테마/멤버십/권한처럼 **화면 캐시에 영향을 주는 write** 를 수행하는 메서드에는 그 옆에 **영향받는 provider 목록을 주석 한 줄**로 적고 각각 `ref.invalidate(affectedProvider)` 를 호출한다. `invalidate` 는 현재 state 를 버리고 **다음 read 때 재평가**, `refresh` 는 invalidate 후 즉시 read 하는 sugar다 — **즉시 새 값이 필요할 때만** `refresh` 를 쓴다. 실측 REJECT (2026-08-12 fit-pal): *"`groupDetailDataProvider` 가 팔레트 색상 변경 시 invalidate 되지 않아, 이미 로드된 그룹 상세 화면이 새 색이 아닌 캐시된 이전 색을 계속 표시"*. **반대로 "모든 mutation 후 전체 family invalidate" 는 하지 마라** — stale 은 줄지만 네트워크 재요청과 UX 흔들림이 커진다. 영향 목록은 열거된 provider 로 한정한다 (출처: <https://riverpod.dev/docs/concepts2/refs>)
- **`autoDispose` 의 실제 수명** — listener 가 0 이 된 뒤 **한 프레임 후** dispose 된다 (즉시가 아니다). 그리고 provider 가 recompute 되면 **autoDispose 여부와 무관하게 기존 state 가 파괴**된다 — "keepAlive 니까 값이 남아 있겠지" 는 recompute 앞에서 성립하지 않는다. `family` / 파라미터 provider 는 인자 조합마다 인스턴스가 쌓이므로 **autoDispose 권장** (출처: <https://riverpod.dev/docs/concepts2/auto_dispose>)
- **`Ref.onManualInvalidation()` 은 버전 가드가 필요하다** — 파생 provider 가 source 의 수동 invalidation 을 **전파**해야 할 때 쓸 수 있는 API 지만, `flutter_riverpod` **3.4.x 이상**에서만 존재한다. 같은 3.4.x 대에서 scoped `ProviderScope`/`ProviderContainer` override 환경에서 `invalidate`/`refresh` 가 provider/family 를 못 찾던 버그도 수정됐다. **`pubspec.lock` 의 실제 버전을 확인하고, 하한을 만족할 때만 이 API 를 쓴다** — 만족하지 않으면 위 mutation 후 명시적 `invalidate` 목록 패턴으로 처리한다 (출처: <https://pub.dev/packages/flutter_riverpod/changelog>)
- **Riverpod 3.0 Pause/Resume** — `ref.listen` 리스너를 `pause()`/`resume()` 으로 수동 일시정지/재개 가능. 화면 비가시 시 자동 일시정지도 지원한다. `Ref.isPaused` 로 상태 확인 가능. 일시정지 후 resume 시 누락된 알림이 있을 수 있으므로 resume 직후 상태를 명시적으로 읽는 패턴을 권장 (출처: <https://pub.dev/packages/flutter_riverpod/changelog>)

Riverpod Notifier + State 클래스를 프로젝트 codegen 패턴에 맞게 생성한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `HAS_RIVERPOD`, `HAS_HOOKS` 등)를 사용한다.

**전제 조건**: `HAS_RIVERPOD`가 true여야 한다.
- `HAS_BLOC`이 감지되면: "이 프로젝트는 Bloc을 사용합니다. 이 스킬은 Riverpod 전용입니다. Bloc/Cubit 생성은 프로젝트의 기존 Bloc 패턴을 참조해주세요."
- 둘 다 없으면: "flutter_riverpod 또는 hooks_riverpod가 pubspec.yaml에 없습니다. `$FLUTTER pub add flutter_riverpod` 또는 `$FLUTTER pub add hooks_riverpod`로 설치해주세요."

## Input

`$ARGUMENTS`: `<feature>/<provider_name>` (e.g., `workout/workout`, `profile/profile_edit`)

## Steps

### 1. 적용 대상 확인 (신규 생성 전용 — 오적용 차단)

먼저 **요청이 신규 생성인지 기존 파일 수정인지** 판정한다. 아래 중 하나라도 해당하면
이 스킬을 **중단**하고 안내한다 (digest `mismatched-provider-skill`):

- 사용자가 특정 기존 파일/클래스(예: `RealtimeController`, `SocketService`)의 동작 변경을 요청
- 대상이 `lib/core/` · `lib/shared/` 등 feature 디렉토리 밖에 있음
- `$ARGUMENTS` 로 지정한 경로에 이미 같은 이름의 provider 파일이 존재

> "이 요청은 기존 `<파일 경로>` 수정입니다. flutter-provider 는 `lib/features/<feature>/` 아래
> 신규 provider 생성 전용이라 feature 디렉토리 워크플로우를 전제합니다. 해당 파일을 직접 읽고
> 수정하겠습니다."

신규 생성이 맞으면 `$ARGUMENTS`를 `/`로 분리하여 feature 이름과 provider 이름(snake_case)을 추출한다.
feature가 `lib/features/<feature>/`에 존재하는지 확인한다. 없으면 중단하고 안내:
> "feature 디렉토리가 없습니다. `flutter-feature` 스킬로 먼저 feature를 생성해주세요."

### 2. 기존 패턴 분석

기존 provider 파일을 읽어 프로젝트 관습을 파악한다:
- `lib/features/<feature>/presentation/providers/` 내 기존 파일
- codegen 스타일 (`@riverpod` vs `@Riverpod(keepAlive: true)` vs legacy `StateNotifierProvider`)
- State 클래스 패턴 (수동 copyWith vs Freezed)
- Result 타입 사용 여부 (`Result<T>`, `Either<L,R>`, `AsyncValue<T>` 등)
- Failure 타입 존재 여부

### 3. 사용자 확인

다음을 확인한다:
- State에 필요한 필드는?
- 어떤 usecase/repository를 호출하는지?
- `keepAlive: true` 여부 (기본값: feature-level notifier는 true)

### 4. Provider 생성

`lib/features/<feature>/presentation/providers/<provider_name>_provider.dart`에 생성한다.

#### Codegen 스타일 (프로젝트가 `@riverpod` annotation 사용 시)

```dart
import 'dart:async';

import 'package:$PACKAGE/...';  // 실제 사용하는 import만 추가
import 'package:riverpod_annotation/riverpod_annotation.dart';

part '<provider_name>_provider.g.dart';

class <ProviderName>State {
  const <ProviderName>State({
    this.isLoading = false,
    this.failure,
    // nullable entity fields
  });

  final bool isLoading;
  final Object? failure;  // 프로젝트에 Failure 타입이 있으면 해당 타입 사용

  <ProviderName>State copyWith({
    bool? isLoading,
    Object? failure,       // Failure? 또는 Object?
    bool clearFailure = false,
    // nullable entity 필드에는 clear* 파라미터 추가
    // e.g., User? user, bool clearUser = false,
  }) {
    return <ProviderName>State(
      isLoading: isLoading ?? this.isLoading,
      failure: clearFailure ? null : failure ?? this.failure,
      // nullable: clearUser ? null : (user ?? this.user),
    );
  }
}

@Riverpod(keepAlive: true)
class <ProviderName>Notifier extends _$<ProviderName>Notifier {
  @override
  <ProviderName>State build() {
    // 초기화가 필요하면 unawaited()로 호출 (build는 sync여야 함)
    // unawaited(_initialize());
    return const <ProviderName>State();
  }

  Future<void> someMethod({required String param}) async {
    // 1. loading + 이전 에러 클리어
    state = state.copyWith(isLoading: true, clearFailure: true);

    // 2. usecase/repository 호출 (ref.read — 메서드 내 일회성 읽기)
    // final result = await ref.read(someUseCaseProvider)(params);

    // 3. mounted 확인
    if (!ref.mounted) return;

    // 4. 결과 분기 (프로젝트에 Result 타입이 있으면 Result.when 패턴)
    // result.when(
    //   success: (data) {
    //     state = state.copyWith(isLoading: false, clearFailure: true);
    //   },
    //   failure: (failure) {
    //     state = state.copyWith(isLoading: false, failure: failure);
    //   },
    // );

    // Result 타입이 없으면 try-catch 패턴
    // try {
    //   final data = await someRepository.fetch();
    //   if (!ref.mounted) return;
    //   state = state.copyWith(isLoading: false);
    // } catch (e) {
    //   if (!ref.mounted) return;
    //   state = state.copyWith(isLoading: false, failure: e);
    // }
  }
}
```

#### Legacy 스타일 (프로젝트가 `StateNotifierProvider` 사용 시)

기존 코드에서 패턴을 읽어 동일한 스타일로 생성한다. `StateNotifier<State>` + `StateNotifierProvider` 패턴.

### 5. 파생 Provider (선택)

State에서 특정 값만 노출할 때 파생 provider를 추가한다. **source 는 반드시 `ref.watch` +
`select` 로 연결한다** — 필요한 필드만 골라야 불필요한 재평가가 없다.

```dart
@riverpod
bool isSomething(Ref ref) {
  // select 로 필요한 필드만 구독 — 다른 필드가 바뀌어도 이 provider 는 재평가되지 않는다
  return ref.watch(<providerName>NotifierProvider.select((s) => s.someField));
}
```

두 provider 의 값을 합쳐야 하면 **양쪽 다 `watch`** 한다. 한쪽을 `ref.read` 로 읽으면 그 쪽이
바뀌어도 파생값이 갱신되지 않는다 (실측 REJECT `LG-02` 의 형태).

### 6. Invalidation 경계 (write 메서드가 있는 경우 필수)

화면 캐시에 영향을 주는 write 메서드를 만들었으면 **영향 provider 목록**을 메서드 옆에 남기고
성공 분기에서 invalidate 한다. 목록이 코드 옆에 있어야 리뷰에서 누락을 잡을 수 있다.

```dart
  /// 영향 provider: groupDetailDataProvider, myGroupsProvider
  Future<void> updatePalette(String groupId, Palette palette) async {
    state = state.copyWith(isLoading: true, clearFailure: true);
    await ref.read(updatePaletteUseCaseProvider)(groupId, palette);
    if (!ref.mounted) return;

    // 캐시된 화면이 이전 값을 계속 보여주지 않도록 영향 provider 를 버린다.
    // 다음 read 때 재평가된다 — 즉시 값이 필요하면 그때만 refresh 를 쓴다.
    ref.invalidate(groupDetailDataProvider(groupId));
    ref.invalidate(myGroupsProvider);

    state = state.copyWith(isLoading: false);
  }
```

**판정 기준** — 아래 셋 중 하나면 invalidate 대상이다.

1. 그 값을 **이미 렌더된 다른 화면**이 읽고 있다 (상세 화면 · 리스트 · 뱃지)
2. 그 값이 **keepAlive provider** 에 캐시되어 있다
3. 그 값이 서버 상태이고 write 가 서버를 바꿨다

**대상이 아닌 것** — 이 Notifier 의 자기 state 는 `copyWith` 로 이미 갱신되므로 invalidate 하지
않는다. 그리고 **family 전체를 통째로 invalidate 하지 마라**. 영향받는 인자 조합만 지정한다.

## Code Rules

- **MUST** 기존 파일을 수정하기 전에 그 파일을 `Read` 로 먼저 읽는다 (digest `edit-before-read`) — 읽지 않은 파일에 Edit 를 시도하면 실패하거나, 더 나쁘게는 기존 구현을 덮어쓴다. Grep 결과 한 줄만 보고 편집하지 마라
- **MUST** import는 `package:$PACKAGE/...`만 사용 (상대경로 금지). 순서: `dart:` → `package:` (그룹 사이 빈 줄, 알파벳순)
- **MUST** State 클래스를 Notifier 위에 선언한다 — 기존 코드베이스 패턴과 일치시켜야 코드 탐색이 일관된다
- **MUST** feature-level notifier에는 `@Riverpod(keepAlive: true)` 사용 — feature 상태가 화면 전환 시 소멸되면 사용자 데이터가 유실되고 불필요한 재요청이 발생한다
- **MUST** 모든 async 작업 후 `ref.mounted` 확인 — Notifier가 dispose된 뒤 state를 변경하면 런타임 에러가 발생한다
- **MUST** async 작업 전에 `state = state.copyWith(isLoading: true, clearFailure: true)` — 이전 에러가 남아 있으면 UI가 에러와 로딩을 동시에 표시하는 버그가 생긴다
- **MUST** 메서드 내에서 usecase/repository는 `ref.read()` (일회성)로 접근. `ref.watch()`는 build 내 또는 파생 provider에서만 사용 — 메서드 내 `ref.watch()`는 구독이 누적되어 메모리 릭과 예측 불가능한 리빌드를 유발한다
- **MUST** nullable 필드는 `clearX` bool 파라미터 패턴 사용: `clearX ? null : (x ?? this.x)` — Dart의 `copyWith`에서 null을 "값이 없음"과 "null로 설정"으로 구분할 수 없기 때문
- **MUST** State class는 manual `copyWith` 사용 (Freezed 아님) — nullable clear 파라미터를 Freezed가 자동 생성할 수 없다
- **MUST** `part '{filename}.g.dart';` 선언 포함 (codegen 스타일인 경우)
- **MUST** 초기화 로직은 `build()` 내에서 `unawaited(_method())`로 호출 — build는 sync return이어야 한다
- **MUST** 프로젝트에 Result 타입이 있으면 그 타입의 성공/실패 양쪽 분기를 처리하고, 없으면 try-catch 패턴을 사용한다 — 분기 문법(switch expression vs `.when`)은 프로젝트 기존 관습을 따른다
- **MUST** 파생 provider 의 source 는 `ref.watch(source.select(...))` 로 연결한다 — `ref.read` 로 계산해 state 에 캐시하면 source 변경이 화면에 반영되지 않는다 (실측 REJECT `LG-02`)
- **MUST** 화면 캐시에 영향을 주는 write 메서드에는 영향 provider 목록 주석 + 성공 분기의 `ref.invalidate` 를 함께 넣는다 — 목록이 없으면 리뷰가 누락을 발견할 수단이 없다
- **MUST NOT** mutation 후 family 전체를 invalidate 하지 않는다 — 영향받는 인자 조합만 지정한다. 전체 invalidate 는 stale 을 줄이는 대신 네트워크 재요청과 UX 흔들림을 만든다
- **MUST** `Ref.onManualInvalidation()` 을 쓰기 전에 `pubspec.lock` 에서 `flutter_riverpod` 이 3.4.x 이상인지 확인한다 — 하한 미달 프로젝트에서는 컴파일되지 않는다

## Related Skills

- codegen 실행 → `flutter-run codegen <feature>`
- 이 provider가 호출할 UseCase/Repository가 없으면 → `flutter-feature`
- 화면에서 에러 표시 패턴 → 프로젝트의 에러 처리 관습을 참조

## Templates

- `../../templates/provider-riverpod.md` — `@riverpod` notifier 골격. 파생 뷰 번들 골격은 **freezed State 컨벤션 프로젝트 한정** 이며, manual `copyWith` 컨벤션이면 위 State 규칙이 우선한다
