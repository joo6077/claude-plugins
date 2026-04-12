---
title: API 레이어
version: 0.1.0
last_updated: 2026-04-05
---

# API 레이어

Dio/Retrofit API 클라이언트, 인터셉터, Failure 변환, Freezed 모델, JsonSerializable, 응답 매핑을 다룬다.

---

## 원칙

### 1. Dio는 singleton으로 공통 BaseOptions와 함께 초기화

baseUrl, timeout, headers를 BaseOptions로 한 번만 설정하고 전체 앱에서 공유한다. 매 호출마다 Dio 인스턴스를 새로 만들지 않는다.

> **출처:** [dio on pub.dev](https://pub.dev/packages/dio)

### 2. 공통 처리는 Dio interceptor에서 한 번만

auth 토큰 주입, 로깅, 에러 변환, 재시도 같은 횡단 관심사는 Interceptor에 집중시키고, 개별 호출부에서는 반복하지 않는다.

> **출처:** [dio on pub.dev](https://pub.dev/packages/dio)

### 3. retrofit 인터페이스 + json_serializable DTO + freezed domain model 조합

retrofit으로 API 인터페이스를 선언하고, DTO는 json_serializable로 직렬화, 도메인 모델은 freezed로 불변·copyWith·union을 얻는다.

> **출처:** [retrofit on pub.dev](https://pub.dev/packages/retrofit), [Flutter JSON Serialization](https://docs.flutter.dev/data-and-backend/serialization/json), [freezed on pub.dev](https://pub.dev/packages/freezed)

### 4. Repository 경계에서 DioException → Failure로 변환

DioException은 transport 레이어 에러다. Repository가 잡아 도메인의 Failure 타입으로 변환하여 UI 레이어는 Failure만 다루게 한다.

> **출처:** [dio on pub.dev](https://pub.dev/packages/dio)

### 5. DTO와 Domain 모델 분리, 매핑은 repository/mapper에서

API 스키마 변경이 UI까지 전파되지 않도록 DTO와 Domain 모델을 분리하고, 변환은 repository 또는 전용 mapper에서 수행한다.

> **출처:** [Flutter App Architecture Guide](https://docs.flutter.dev/app-architecture/guide)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| Dio 예시 connectTimeout | 5s |
| Dio 예시 receiveTimeout | 3-5s |
| dio 최신 버전 | 5.9.2 |
| retrofit 최신 버전 | 4.9.2 |
| json_serializable 최신 버전 | 6.13.1 |
| freezed 최신 버전 | 3.2.5 |
| CancelToken | 여러 요청 간 공유 가능 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| Notifier/Widget에서 dio.get 직접 호출 | 레이어 경계 붕괴, 테스트 불가 |
| DTO에 비즈니스 로직 포함 | 스키마 변경 시 비즈니스 로직까지 영향 |
| 모든 에러를 단일 Exception으로 뭉갬 | 네트워크/파싱/서버 에러 구분 불가 |
| Map<String,dynamic>를 UI까지 전파 | 타입 안전성 상실 |

---

## 실전 패턴

### Retrofit DataSource 정의

```dart
@RestApi(baseUrl: '')
abstract class ProductApi {
  factory ProductApi(Dio dio, {String baseUrl}) = _ProductApi;

  @GET('/products')
  Future<List<ProductDto>> getProducts(@Query('page') int page);

  @GET('/products/{id}')
  Future<ProductDto> getProduct(@Path('id') String id);

  @POST('/products')
  Future<ProductDto> createProduct(@Body() CreateProductDto dto);

  @DELETE('/products/{id}')
  Future<void> deleteProduct(@Path('id') String id);
}
```

- 출처: https://pub.dev/packages/retrofit

### DTO → Entity 변환 (Repository에서)

```dart
class ProductRepositoryImpl implements ProductRepository {
  final ProductApi _api;

  @override
  Future<Either<Failure, List<Product>>> getProducts(int page) async {
    try {
      final dtos = await _api.getProducts(page);
      return Right(dtos.map((dto) => dto.toDomain()).toList());
    } on DioException catch (e) {
      return Left(e.toFailure());
    }
  }
}
```

### Dio Interceptor 계층

```text
Dio
├── AuthInterceptor — JWT 토큰 주입, 401 시 refresh
├── LogInterceptor — request/response 로깅 (debug only)
├── RetryInterceptor — 5xx/timeout 시 재시도 (최대 3회)
└── CacheInterceptor — GET 요청 ETag/304 캐싱 (선택)
```

- 출처: https://pub.dev/documentation/dio/latest/dio/Interceptor-class.html

### 에러 변환 Extension

```dart
extension DioExceptionX on DioException {
  Failure toFailure() => switch (type) {
    DioExceptionType.connectionTimeout => const Failure.network('연결 시간 초과'),
    DioExceptionType.receiveTimeout => const Failure.network('응답 시간 초과'),
    DioExceptionType.badResponse => _parseServerError(response),
    DioExceptionType.cancel => const Failure.cancelled(),
    _ => Failure.unknown(message ?? '알 수 없는 오류'),
  };
}
```

### Pagination 패턴

| 패턴 | 사용 시점 |
|------|----------|
| Offset-based (`?page=2&limit=20`) | 총 개수가 필요하거나, 특정 페이지 점프가 필요할 때 |
| Cursor-based (`?after=abc123`) | 실시간 데이터, 무한 스크롤, 일관된 결과 필요 시 |

Repository에서 pagination 메타(hasMore, nextCursor)를 Entity와 함께 반환:

```dart
class PaginatedResult<T> {
  final List<T> items;
  final bool hasMore;
  final String? nextCursor;
}
```

## 테스트 전략

- **DataSource**: `MockDio` 또는 `dio_test` 패키지로 HTTP 응답 모킹
- **Repository**: DataSource를 Fake/Mock으로 교체, Either<Failure, T> 반환 검증
- **DTO 변환**: 실제 JSON fixture 파일로 `fromJson`/`toJson` round-trip 검증
- **Interceptor**: `RequestInterceptorHandler`/`ResponseInterceptorHandler` mock으로 동작 검증

## Gotchas

- **retrofit Parser.FlutterCompute는 Map-heavy 응답에 역효과** — isolate 전송 비용이 파싱 비용보다 클 수 있다. 큰 배열/깊은 객체에만 선택적으로 적용.
- **json_serializable 옵션은 초기 합의 필수** — `explicitToJson`, `fieldRename`, `genericArgumentFactories`는 프로젝트 시작 시 통일해야 한다. 후행 변경은 전수 리제너레이션을 유발.
- **Dio baseUrl 중복** — Retrofit `@RestApi(baseUrl: '')`과 Dio 인스턴스의 `baseUrl`이 겹치면 URL이 이중 결합된다. 한쪽만 지정하라.
- **401 refresh 무한 루프** — refresh token도 만료되었는데 retry가 계속 refresh를 시도하면 무한 루프. refresh 실패 시 즉시 로그아웃으로 분기해야 한다.
- **freezed DTO vs Entity 분리** — DTO에 `@JsonSerializable`을 붙이고, Entity에는 순수 `@freezed`만 쓴다. 같은 클래스에 둘 다 붙이면 API 스키마 변경이 도메인 로직까지 전파된다.
