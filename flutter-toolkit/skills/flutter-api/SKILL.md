---
name: flutter-api
description: >
  Clean Architecture 전 레이어를 일괄 또는 개별 생성한다.
  DataSource(Retrofit) → Model(Freezed) → Repository → UseCase.
  서브커맨드로 개별 레이어만 생성할 수도 있다: model, repository, usecase.
  아키텍처가 Clean Architecture가 아닌 경우 간소화된 Service+Model 패턴을 생성한다.
  "API 연동", "엔드포인트 연결", "모델 만들어줘", "리포지토리 추가",
  "유스케이스 생성", "DTO 생성", "entity 만들어줘", "레이어 추가",
  "서비스 생성", "service layer", "API layer" 같은 요청 시 사용한다.
  단순 위젯이나 화면 생성만 할 때는 사용하지 않는다.
argument-hint: "[model|repository|usecase] <feature>/<name>"
user-invocable: true
---

## Gotchas

- 상대 import `import '../'` 금지 — 반드시 `package:app/...` 절대 import 사용. 리팩터링 시 경로 깨짐 방지
- Failure 변환은 Repository/DataSource 경계에서 수행 — UseCase에서 try-catch 하지 마라
- **Freezed 3.2+ Mixed mode + `when`/`map` 제거** — Freezed 3.2.0 부터 `.when()`/`.map()` 메서드가 제거됐다. sealed class 기반 union 타입은 Dart 3 pattern matching (`switch` expression) 으로 분기해야 한다. `eject union cases` 기능으로 기존 union 을 standalone sealed class 로 변환 가능. 프로젝트에 `.when()` 호출이 남아 있으면 마이그레이션 필요 (출처: <https://pub.dev/packages/freezed/changelog>)
- **Freezed + json_serializable 버전 핀닝** — Freezed 3.2.3 + json_serializable 6.11.3 조합에서 analyzer >=9 / build >=4 호환 이슈가 보고됨. `pubspec.lock` 에서 버전 호환성을 반드시 확인하라 (출처: community report 2025-09)

# API 레이어 생성

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `ARCH`, `HAS_RETROFIT`, `HAS_FREEZED`, `HAS_RIVERPOD`)를 사용한다.

### 모드 결정

| 감지 결과 | 모드 | 생성 구조 |
|----------|------|----------|
| `ARCH = clean` | Clean Architecture | DataSource → Model → Repository(interface+impl) → UseCase |
| `ARCH = feature_first` 또는 `flat` | Simple | Service → Model |

---

## Clean Architecture 모드 (`ARCH = clean`)

### Input

`$ARGUMENTS` 파싱으로 서브모드를 결정한다:

| 호출 | 서브모드 | 동작 |
|------|---------|------|
| `<feature>/<method>` | 전체 생성 | DataSource → Model → Repository → UseCase 일괄 |
| `model <feature>/<name>` | 개별 | Entity + Model(DTO) 쌍 생성 |
| `repository <feature>` | 개별 | Repository interface + impl |
| `usecase <feature>/<name>` | 개별 | UseCase + Params |

### 전체 생성 흐름

1. `$ARGUMENTS`에서 feature 이름과 method 이름 파싱.
2. `lib/features/<feature>/` 디렉토리 존재 확인.
3. 기존 패턴(datasources, models, repositories, usecases) 읽기.
4. 사용자에게 확인: HTTP method, API path, request/response types, 새 model 필요 여부.
5. 필요 시 Entity + Model 생성. Entity + Model 파일명/경로는 위 '개별 생성: model' 섹션의 규칙을 따른다.
6. DataSource에 메서드 추가.
   - `HAS_RETROFIT` → Retrofit 어노테이션 (`@GET`, `@POST` 등) 사용
   - 없으면 → 일반 Dio 메서드 호출
7. API 경로 상수 추가 — 기존 패턴을 먼저 읽고 동일한 네이밍/경로 패턴 적용. prefix를 임의로 추가하지 않는다.
8. Repository interface(domain) + impl(data) 추가.
9. UseCase 생성.
   - `HAS_RIVERPOD` → `@riverpod` provider도 함께 생성
   - 없으면 → provider 없이 UseCase 클래스만 생성

### 개별 생성: model

Entity + DTO(Model) 쌍을 생성한다.

```text
lib/features/<feature>/
├── domain/entities/<name>_entity.dart       # 도메인 엔티티
└── data/models/<name>_model.dart            # DTO + toEntity()
```

- `HAS_FREEZED` → `@freezed` 사용
- 없으면 → 일반 `class` + `fromJson` / `toJson` 수동 작성

**Entity** (domain):
```dart
// HAS_FREEZED
@freezed
abstract class UserEntity with _$UserEntity {
  const factory UserEntity({
    required String id,
    required String name,
  }) = _UserEntity;
}

// HAS_FREEZED 없음
class UserEntity {
  const UserEntity({required this.id, required this.name});
  final String id;
  final String name;
}
```

**Model** (data):
```dart
// HAS_FREEZED
@freezed
abstract class UserModel with _$UserModel {
  const factory UserModel({
    required String id,
    required String name,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}

// toEntity extension
extension UserModelX on UserModel {
  UserEntity toEntity() => UserEntity(id: id, name: name);
}
```

### 개별 생성: repository

Repository interface(domain) + impl(data)을 생성한다.

```text
lib/features/<feature>/
├── domain/repositories/<feature>_repository.dart       # interface
└── data/repositories/<feature>_repository_impl.dart    # impl
```

**Interface** (domain):
```dart
abstract interface class UserRepository {
  Future<Result<UserEntity>> getUser(String id);
}
```

**Impl** (data):
```dart
class UserRepositoryImpl implements UserRepository {
  const UserRepositoryImpl(this._dataSource);
  final UserDataSource _dataSource;

  @override
  Future<Result<UserEntity>> getUser(String id) async {
    try {
      final model = await _dataSource.getUser(id);
      return Result.success(model.toEntity());
    } on DioException catch (error, st) {
      return Result.failure(_mapFailure(error, st));
    } on Exception catch (error, st) {
      return Result.failure(_mapFailure(error, st));
    }
  }
}
```

`HAS_RIVERPOD`이면 같은 파일에 Repository provider도 생성:
```dart
@Riverpod(keepAlive: true)
UserRepository userRepository(Ref ref) {
  return UserRepositoryImpl(ref.watch(userDataSourceProvider));
}
```

프로젝트에 `Result<T>` 타입이 없으면:
- `dartz`의 `Either<Failure, T>` 패턴을 감지하여 사용
- 둘 다 없으면 `try/catch` + 직접 throw 패턴 사용

프로젝트에 `Failure` sealed class가 있으면 `_mapFailure`에서 해당 타입으로 변환.
없으면 `Exception`을 그대로 전파하거나, 간단한 에러 래퍼를 생성한다.

**`_mapFailure` 패턴**: 반드시 **프로젝트의 기존 `_mapFailure` 구현을 먼저 읽고, 동일한 Exception 분기를 사용**한다.
기존 구현이 없으면 아래 범용 템플릿을 기반으로 프로젝트의 Failure 타입에 맞게 생성한다:

```dart
Failure _mapFailure(Object error, [StackTrace? st]) {
  if (error is DioException) {
    return switch (error.type) {
      DioExceptionType.connectionError ||
      DioExceptionType.connectionTimeout ||
      DioExceptionType.receiveTimeout =>
        NetworkFailure(message: error.message ?? ''),
      _ => switch (error.response?.statusCode) {
        401 => UnauthorizedFailure(),
        >= 500 => ServerFailure(message: error.message ?? ''),
        _ => UnknownFailure(error: error),
      },
    };
  }
  // 프로젝트에 정의된 커스텀 Exception 타입들도 분기
  // if (error is StorageException) return StorageFailure(...);
  // if (error is UnauthorizedException) return UnauthorizedFailure(...);
  // if (error is ServerException) return ServerFailure(...);
  return UnknownFailure(error: error);
}
```

### 개별 생성: usecase

UseCase + Params를 생성한다.

```text
lib/features/<feature>/domain/usecases/<name>_usecase.dart
```

**UseCase base class 탐색**: 먼저 프로젝트에 `UseCase` base class가 있는지 검색한다.
탐색 경로: `lib/core/`, `lib/shared/domain/usecases/`, `lib/core/usecases/` 등에서 `abstract class UseCase`를 검색.

- base class가 **있으면** (`UseCase<TResult, Params>` 등) → 상속하여 생성:
```dart
class GetUserUseCase extends UseCase<UserEntity, GetUserParams> {
  const GetUserUseCase(this._repository);
  final UserRepository _repository;

  @override
  ResultFuture<UserEntity> call(GetUserParams params) {
    return _repository.getUser(params.id);
  }
}
```

- base class가 **없으면** → plain class로 생성:
```dart
class GetUserUseCase {
  const GetUserUseCase(this._repository);
  final UserRepository _repository;

  Future<Result<UserEntity>> call(GetUserParams params) {
    return _repository.getUser(params.id);
  }
}

// HAS_FREEZED
@freezed
abstract class GetUserParams with _$GetUserParams {
  const factory GetUserParams({required String id}) = _GetUserParams;
}

// HAS_FREEZED 없음
class GetUserParams {
  const GetUserParams({required this.id});
  final String id;
}
```

`HAS_RIVERPOD`이면 provider도 생성:
```dart
@Riverpod(keepAlive: true)
GetUserUseCase getUserUseCase(Ref ref) {
  return GetUserUseCase(ref.watch(userRepositoryProvider));
}
```

> **Import 규칙**: UseCase provider에서 `ref.watch(userRepositoryProvider)`를 사용하므로, `data/repositories/<feature>_repository_impl.dart`를 import해야 한다 — `<feature>RepositoryProvider`가 해당 파일에 정의되어 있기 때문이다.

---

## Simple 모드 (`ARCH != clean`)

Clean Architecture가 아닌 프로젝트에서는 간소화된 Service + Model 패턴을 생성한다.

### 생성 구조

```text
lib/features/<feature>/
├── models/<name>_model.dart       # 데이터 모델
└── services/<feature>_service.dart # API 서비스
```

또는 프로젝트 구조에 맞게 `lib/src/`, `lib/services/` 등에 생성.

**Model**:
```dart
// HAS_FREEZED
@freezed
abstract class UserModel with _$UserModel {
  const factory UserModel({
    required String id,
    required String name,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}
```

**Service**:

HTTP 클라이언트는 프로젝트에서 감지한다:
- `HAS_DIO` → `Dio` 사용
- `http` 패키지 존재 → `http.Client` 사용
- 둘 다 없음 → "HTTP 클라이언트 패키지가 없습니다. `$FLUTTER pub add dio` 또는 `$FLUTTER pub add http`로 설치해주세요."

```dart
// HAS_DIO
class UserService {
  const UserService(this._dio);
  final Dio _dio;

  Future<UserModel> getUser(String id) async {
    final response = await _dio.get('/users/$id');
    return UserModel.fromJson(response.data as Map<String, dynamic>);
  }
}

// http 패키지
class UserService {
  const UserService(this._client);
  final http.Client _client;

  Future<UserModel> getUser(String id) async {
    final response = await _client.get(Uri.parse('/users/$id'));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return UserModel.fromJson(json);
  }
}
```

---

## Code Rules

- **Result typedef 탐색**: 프로젝트에 `ResultFuture<T>`, `ResultVoid` 등 typedef가 있는지 `lib/core/utils/`, `lib/shared/`, `lib/core/types/` 에서 검색한다. 있으면 `Future<Result<T>>` 대신 해당 typedef를 사용한다. (예: `ResultFuture<UserEntity>`, `ResultVoid`)
- `package:$PACKAGE/...` import만 사용 (상대경로 금지)
- Import 순서: `dart:` → `package:` (그룹 사이 빈 줄, 알파벳순)
- `ARCH = clean`이면 Repository는 예외를 프로젝트의 Failure/Error 타입으로 변환 — 호출부에서 `try/catch` 없이 결과 분기를 쓸 수 있게 한다
- DataSource: `HAS_RETROFIT`이면 Retrofit 어노테이션, 아니면 Dio 직접 호출
- Model: `HAS_FREEZED`이면 `@freezed`, 아니면 수동 `fromJson`/`toJson`
- UseCase/Repository provider: `HAS_RIVERPOD`이면 `@Riverpod(keepAlive: true)` — 앱 생명주기 동안 유지되는 인프라 계층이므로 자동 dispose하면 안 된다
- catch 변수: 사용하면 `error`, 미사용이면 `_`

## After Creation

1. 생성/수정된 파일 목록 출력.
2. `HAS_BUILD_RUNNER`이면 codegen 실행 안내:
   > `$DART run build_runner build --delete-conflicting-outputs`
