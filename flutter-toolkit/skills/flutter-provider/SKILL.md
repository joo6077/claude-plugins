---
name: flutter-provider
description: >
  Riverpod Notifier + State 클래스를 생성한다.
  @Riverpod codegen, copyWith, ref.mounted 체크, Result.when 분기 패턴 포함.
  상태 관리 Provider를 만들 때 사용.
  "provider 만들어줘", "notifier 생성", "상태 관리", "state management",
  "riverpod provider", "notifier class" 같은 요청 시 트리거.
argument-hint: "<feature>/<provider-name>"
user-invocable: true
---

## Gotchas

- keepAlive provider는 keepAlive provider만 참조해야 한다 — 비keepAlive를 참조하면 stale state 발생
- `ref.watch(provider)`로 전체 객체를 감시하면 불필요한 리빌드 — `ref.watch(provider.select((s) => s.isLoading))`으로 필요한 필드만 선택
- `Result<T>.when(success:, failure:)` 양쪽 분기를 반드시 처리 — 한쪽만 처리하면 unhandled state
- `@Riverpod` codegen 사용 시 `build_runner`를 돌려야 `.g.dart` 생성됨 — 코드만 쓰고 codegen을 빠뜨리면 컴파일 에러
- Riverpod 3.0에서 `.valueOrNull`이 `.value`로 변경됨 — 기존 코드에 `.valueOrNull`이 있으면 마이그레이션 필요. `dart fix --apply`로 자동 처리 가능
- Riverpod 3.0의 offline persistence/mutations는 아직 experimental — 프로덕션에서는 수동 캐싱 패턴 유지 권장

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

### 1. 파싱 및 검증

`$ARGUMENTS`를 `/`로 분리하여 feature 이름과 provider 이름(snake_case)을 추출한다.
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

State에서 특정 값만 노출할 때 파생 provider를 추가한다:

```dart
@riverpod
bool isSomething(Ref ref) {
  return ref.watch(<providerName>NotifierProvider).someField;
}
```

## Code Rules

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
- **MUST** 프로젝트에 Result 타입이 있으면 `Result.when(success:, failure:)` 패턴, 없으면 try-catch 패턴을 사용한다

## Related Skills

- codegen 실행 → `flutter-run codegen <feature>`
- 이 provider가 호출할 UseCase/Repository가 없으면 → `flutter-feature`
- 화면에서 에러 표시 패턴 → 프로젝트의 에러 처리 관습을 참조
