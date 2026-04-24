---
name: flutter-feature
description: >
  새 feature 모듈을 프로젝트 아키텍처에 맞는 디렉토리 구조와 보일러플레이트 파일로 스캐폴딩한다.
  새 기능 모듈, feature 디렉토리, 전체 레이어를 처음부터 만들 때 사용.
  "새 feature 만들어줘", "feature 스캐폴딩", "기능 모듈 생성",
  "scaffold feature", "new feature", "feature directory" 같은 요청 시 트리거.
  기존 feature 내 개별 파일 추가는 flutter-screen, flutter-provider 등 사용.
argument-hint: "<feature-name>"
user-invocable: true
disable-model-invocation: true
---

## Gotchas

- 아키텍처 감지 결과(Clean/Feature-first/Flat)에 따라 디렉토리 구조가 완전히 달라진다 — 감지 없이 하드코딩하면 기존 구조와 충돌
- 새 feature 디렉토리 생성 후 반드시 codegen 실행 — Freezed/Retrofit 어노테이션이 있으면 `.g.dart`/`.freezed.dart` 없어서 컴파일 에러
- import는 반드시 `package:app/features/<feature>/...` 절대 경로 — 상대 import 사용하면 preflight에서 FAIL
- **Enumerate-before-Act (low-freedom 영역 · skill-design-guide §5.5)** — 새 feature 모듈 생성 전에 (a) `ls lib/features/` 로 기존 feature 이름을 **전수 나열** 하여 중복·유사명을 방지하고, (b) 해당 프로젝트의 기존 feature 중 하나를 샘플로 읽어 레이어별 파일 naming 관례(`*_page.dart` vs `*_screen.dart`, `*_repository.dart` vs `*_repo.dart`)를 파악한 뒤 생성한다. 근사치 추정으로 feature 명·naming 을 결정하면 기존 컨벤션과 드리프트가 생겨 전체 feature 재명명 iteration 이 발생 (insights-report #2 Wrong approach 대응)

프로젝트의 아키텍처 패턴에 맞게 새 feature 모듈을 생성한다.

Feature name: `$ARGUMENTS` (required, snake_case. e.g., `workout`, `profile`)

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `ARCH`, `HAS_RIVERPOD`, `HAS_FREEZED`, `HAS_RETROFIT`, `HAS_GO_ROUTER_BUILDER`, `HAS_HOOKS` 등)를 사용한다.

## Steps

### 1. 아키텍처 패턴에 따른 디렉토리 구조 결정

감지된 `ARCH` 값에 따라 구조를 결정한다.

**ARCH = clean** (Clean Architecture):

```text
lib/features/$ARGUMENTS/
  ├── data/
  │   ├── datasources/
  │   ├── models/
  │   └── repositories/
  ├── domain/
  │   ├── entities/
  │   ├── repositories/
  │   └── usecases/
  └── presentation/
      ├── providers/
      └── widgets/
```

**ARCH = feature_first**:

```text
lib/features/$ARGUMENTS/
  ├── models/
  ├── services/
  ├── <state-dir>/
  ├── pages/ (또는 screens/, views/)
  └── widgets/
```

상태 관리 디렉토리는 프로젝트의 상태관리 라이브러리에 따라:
- `HAS_RIVERPOD` → `providers/`
- `HAS_BLOC` → `blocs/`
- 둘 다 없음 → `controllers/` (또는 프로젝트 기존 관습)

**ARCH = flat**:

```text
lib/src/$ARGUMENTS/
  ├── $ARGUMENTS_model.dart
  ├── $ARGUMENTS_service.dart
  └── $ARGUMENTS_page.dart
```

`lib/src/`가 존재하지 않으면 `lib/` 직하에 feature 디렉토리를 생성한다.

**기존 feature가 있으면** 해당 구조를 참조하여 동일한 패턴으로 생성한다 (기존 프로젝트 관습 우선).

기존 feature가 있으면 해당 구조를 참조하되, 아래 사항에 주의:
- `presentation/screens/` 하위 구조가 보이면 레거시로 간주한다 — 신규 코드에서는 `presentation/` 직하에 Screen, `presentation/pages/`에 Page를 배치
- 기존 코드에 `StatefulWidget`이 사용되고 있어도, `HAS_HOOKS`면 `HookWidget` 사용
- 기존 코드에 상대경로 import가 있어도 신규 코드는 `package:$PACKAGE/...` 사용

### 2. 보일러플레이트 파일 생성

기존 feature 코드를 참조하여 동일한 패턴으로 생성한다. 기존 feature가 없으면 아래 기본 템플릿을 사용한다.

#### Clean Architecture (ARCH = clean)

**Data Layer**

- **Remote data source** (`data/datasources/{name}_remote_data_source.dart`):
  - `HAS_RETROFIT` → Retrofit `@RestApi()` 패턴
  - Retrofit 없음 → 일반 abstract class + impl
  - `HAS_RIVERPOD` → `@Riverpod(keepAlive: true)` provider 추가

- **Data model** (`data/models/{name}_model.dart`):
  - `HAS_FREEZED` → Freezed + JsonSerializable + `toEntity()` extension
  - Freezed 없음 → 수동 class + `fromJson`/`toJson` factory

- **Repository impl** (`data/repositories/{name}_repository_impl.dart`):
  - implements domain interface
  - 예외 → Failure 변환 패턴 (프로젝트에 `Failure` 타입이 있으면 사용, 없으면 기본 Exception 전파)
  - 프로젝트에 Failure sealed class가 있으면 `_mapFailure` 헬퍼를 포함한다
  - `HAS_RIVERPOD` → `@Riverpod(keepAlive: true)` provider

**Domain Layer**

- **Entity** (`domain/entities/{name}.dart`):
  - `HAS_FREEZED` → Freezed class
  - Freezed 없음 → immutable class

- **Repository interface** (`domain/repositories/{name}_repository.dart`):
  - abstract class, `Future<T>` return types (프로젝트에 `Result<T>` 타입이 있으면 `ResultFuture<T>` 사용)

- **UseCase** (`domain/usecases/{name}_usecase.dart`):
  - 프로젝트에 `UseCase` base class가 있으면 extends 패턴
  - 없으면 단순 callable class

**Presentation Layer**

- **Provider** (`presentation/providers/{name}_provider.dart`):
  - `HAS_RIVERPOD` → Notifier + State class (flutter-provider 스킬 패턴)
  - `HAS_RIVERPOD` 없음 → ChangeNotifier 또는 프로젝트 상태관리 패턴

- **Screen** (`presentation/{name}_screen.dart`):
  - 바텀 네비 탭 최상위 화면, Scaffold
  - Widget base: `HAS_HOOKS` → `HookConsumerWidget`, `HAS_RIVERPOD` → `ConsumerWidget`, 기본 → `StatelessWidget`

#### Feature-First / Flat Architecture

기존 feature 코드를 참조하여 동일한 파일 구조와 패턴으로 생성한다.

### 3. 라우트 등록

- `HAS_GO_ROUTER_BUILDER` → `@TypedGoRoute` codegen 패턴으로 라우터 파일에 추가
- `HAS_GO_ROUTER` (builder 없음) → `GoRoute()` 수동 등록
- `HAS_AUTO_ROUTE` → Screen/Page에 `@RoutePage()` annotation을 추가하고, 라우터 파일에 `AutoRoute(page: <Name>Route.page, path: '/<name>')` 등록. `@RoutePage()`는 build_runner codegen 대상.
- 라우터 없음 → 라우트 등록 스킵

라우터 파일 위치는 기존 코드에서 감지한다 (e.g., `lib/core/router/`, `lib/app/router/`, `lib/routes/`).

### 4. codegen 안내

`HAS_BUILD_RUNNER`가 true이면:
> "`.g.dart`와 `.freezed.dart` 파일을 생성하려면 codegen을 실행하세요:
> `$DART run build_runner build --delete-conflicting-outputs`"

## Code Style

- import는 `package:$PACKAGE/...`만 사용 (상대경로 금지)
- import 순서: `dart:` → `package:` (그룹 사이 빈 줄, 알파벳순)
- Codegen 파일: `part '{filename}.g.dart';` / `part '{filename}.freezed.dart';`
- Screen(바텀 네비 탭) 파일은 `presentation/` 직하에, Page(push 진입) 파일은 `presentation/pages/`에 위치 (기존 프로젝트 관습이 다르면 그것을 따른다)

## _mapFailure 기본 템플릿

프로젝트에 Failure sealed class가 있으면 Repository impl에 `_mapFailure` 헬퍼를 포함한다:

```dart
// 프로젝트의 기존 _mapFailure 패턴을 읽어 동일한 분기를 사용한다.
// 기존 패턴이 없으면 아래 기본 템플릿 사용:
Object _mapFailure(Object error, [StackTrace? st]) {
  if (error is DioException) {
    return switch (error.type) {
      DioExceptionType.connectionError ||
      DioExceptionType.connectionTimeout ||
      DioExceptionType.receiveTimeout => NetworkFailure(message: error.message ?? ''),
      _ => switch (error.response?.statusCode) {
        401 => UnauthorizedFailure(),
        >= 500 => ServerFailure(message: error.message ?? ''),
        _ => UnknownFailure(error: error),
      },
    };
  }
  return UnknownFailure(error: error);
}
```

## Rules

- **MUST** 기존 feature가 있으면 해당 코드를 읽어 패턴을 일치시킨다
- **MUST** 감지된 아키텍처(`ARCH`)에 맞는 구조만 생성한다
- **MUST** 의존성이 없는 기능(Freezed, Retrofit 등)은 해당 보일러플레이트를 스킵하고, 대체 패턴으로 생성한다
- **MUST NOT** 프로젝트에 없는 패키지를 import하는 코드를 생성하지 않는다

## Post-Creation: Widget Inspector

생성 완료 후 `widget-inspector` 에이전트를 quick 모드로 실행하여 변경 파일 주변의 재사용 가능한 위젯 패턴을 스캔한다. 추출 후보가 있으면 리포팅하고, 없으면 조용히 넘어간다.

## Related Skills

- 이 스킬은 디렉토리 구조 + 보일러플레이트만 생성. 이후 단계:
  - 화면 추가 → `flutter-screen`
  - Provider 생성 → `flutter-provider`
  - Widget 생성 → `flutter-widget`
  - 위젯 추출 → `flutter-extract`
  - codegen 실행 → `flutter-run codegen`
