# Rust Audit Criteria

rust-reviewer 에이전트가 사용하는 유일한 감사 기준. 카테고리별 PASS/FAIL 조건을 정의한다.

---

## 1. Ownership & Borrowing

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 불필요한 clone | `.clone()` 호출이 빌림으로 대체 가능한 곳이 없다 | Rust Book Ch.4 |
| &String / &Vec 사용 | 함수 인자에 `&String` 대신 `&str`, `&Vec<T>` 대신 `&[T]` 사용 | Clippy |
| Lifetime 명시 | 생략 가능한 lifetime을 불필요하게 명시하지 않는다 | Rust RFC 141 |

## 2. Error Handling

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| unwrap/expect 사용 | 프로덕션 코드에 `.unwrap()` / `.expect()` 없다 (테스트 제외) | Clippy |
| 에러 타입 일관성 | 하나의 모듈/크레이트 내에서 에러 타입이 일관적이다 | thiserror docs |
| From impl | 에러 변환에 수동 매핑 대신 `#[from]` 또는 `From` impl 사용 | thiserror docs |

## 3. Async

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| blocking in async | `std::thread::sleep`, `std::fs::*` 등 blocking 호출이 async 함수 내에 없다 | Tokio docs |
| 불필요한 .await | 반환값을 사용하지 않는 `let _ = foo().await;` 패턴이 없다 (fire-and-forget이면 spawn) | Clippy |
| Mutex in async | `std::sync::Mutex` 대신 `tokio::sync::Mutex` 사용 (.await를 넘겨 잡으면) | Tokio docs |

## 4. Security

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 시크릿 하드코딩 | API 키, JWT 시크릿, DB 비밀번호가 소스코드에 없다 | OWASP |
| SQL injection | 문자열 보간 대신 파라미터 바인딩 사용 (`sqlx::query!` / `$1`) | SQLx docs |
| 입력 검증 | 외부 입력(HTTP body, query param)에 길이/형식 검증이 있다 | OWASP |

## 5. Performance

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 불필요한 allocation | 루프 내 불필요한 `String::new()` / `Vec::new()` 없다 | Clippy |
| collect 후 iterate | `.collect::<Vec<_>>()` 후 다시 `.iter()`하지 않는다 | Clippy |
| 사전 할당 | 크기를 아는 Vec에 `Vec::with_capacity()` 사용 | Rust Book |

## 6. Testing

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 핵심 로직 테스트 | 비즈니스 로직 함수에 최소 1개 테스트 존재 | 일반 관행 |
| 에러 경로 테스트 | 주요 에러 경로에 대한 테스트 존재 | 일반 관행 |
| 테스트 격리 | 테스트 간 상태 공유가 없다 (글로벌 변수, 공유 파일 등) | cargo test docs |

## 7. API Design

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| HTTP 메서드 일관성 | CRUD에 적절한 메서드 사용 (GET=조회, POST=생성, PUT/PATCH=수정, DELETE=삭제) | REST 관행 |
| 응답 코드 일관성 | 성공(200/201), 없음(404), 충돌(409), 서버 에러(500) 등 적절한 상태 코드 | HTTP spec |
| OpenAPI 정합 | HAS_UTOIPA면 모든 공개 엔드포인트에 `#[utoipa::path]` 존재 | utoipa docs |
