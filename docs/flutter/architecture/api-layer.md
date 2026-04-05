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

## Gotchas

- **retrofit Parser.FlutterCompute는 Map-heavy 응답에 역효과** — isolate 전송 비용이 파싱 비용보다 클 수 있다. 큰 배열/깊은 객체에만 선택적으로 적용.
- **json_serializable 옵션은 초기 합의 필수** — `explicitToJson`, `fieldRename`, `genericArgumentFactories`는 프로젝트 시작 시 통일해야 한다. 후행 변경은 전수 리제너레이션을 유발.
