---
name: rust-error
description: >
  Rust 프로젝트의 에러 처리 패턴을 안내한다. 3계층 에러 구조(InfraError → DomainError → ApiError)를 기반으로
  현재 코드의 에러 패턴을 분석하고 개선점을 제시하는 가이드형 스킬이다.
  "에러 처리", "error handling", "에러 타입", "Result", "rust error" 같은 요청 시 사용한다.
argument-hint: "[파일 또는 모듈 경로]"
user-invocable: true
---

## Gotchas

- `anyhow`와 `thiserror` 혼용은 금지가 아니다. 라이브러리/도메인 코드에는 `thiserror`(구체적 에러 타입), 앱 진입점(`main.rs`, CLI 스크립트)에는 `anyhow`(편의)가 관용적이다.
- `.unwrap()`과 `.expect()`는 프로덕션 코드에서 금지다. 테스트 코드에서만 허용된다. 발견 즉시 `?` 또는 명시적 에러 처리로 교체를 제안한다.
- `?` 연산자 체이닝 시 `From<SrcError> for DstError` impl이 누락되면 컴파일 에러가 난다. 에러 타입 간 변환 경로를 먼저 확인하라.

# 에러 처리 패턴 가이드

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
`ARCH`, `IS_WORKSPACE`, `$PACKAGE`를 확인한다.

`Cargo.toml`에서 `thiserror`, `anyhow` 의존성 여부를 확인한다.
없으면 추가를 제안한다:

```toml
[dependencies]
thiserror = "2"
anyhow = "1"
```

---

## 1. 현재 에러 패턴 분석

`$ARGUMENTS`에서 파일/모듈 경로를 파싱한다. 경로가 없으면 에러 관련 파일을 자동으로 탐색한다:

```text
ARCH = workspace_service → crates/domain/src/errors.rs, crates/api/src/errors.rs, crates/infra/src/errors.rs
ARCH = modular          → src/domain/errors.rs, src/api/errors.rs, src/infra/errors.rs
ARCH = flat             → src/errors.rs
```

읽은 파일에서 다음을 파악한다:

| 항목 | 확인 내용 |
|------|---------|
| 에러 타입 정의 방식 | `thiserror`, `anyhow`, 직접 구현 |
| 계층 분리 여부 | Infra/Domain/Api 분리 또는 단일 에러 |
| `From` impl | 에러 타입 간 변환 경로 |
| `unwrap`/`expect` 사용 | 프로덕션 코드 내 위치 |
| `IntoResponse` impl | Axum HTTP 상태 코드 매핑 |

---

## 2. 3계층 에러 구조 제안

현재 구조를 분석한 뒤, 아래 3계층 구조로의 개선점을 제안한다.
이미 잘 구성된 경우 확인만 한다.

### 계층 구조

```text
InfraError (DB, 외부 API, IO)
    ↓ From impl
DomainError (비즈니스 규칙 위반, 리소스 없음)
    ↓ From impl  
ApiError (HTTP 응답 래퍼)
```

### Infra 계층 (`infra/errors.rs` 또는 `crates/infra/src/errors.rs`)

구체적인 외부 시스템 에러를 정의한다. SQLx, 외부 HTTP 클라이언트, IO 에러가 여기에 속한다:

```rust
#[derive(Debug, thiserror::Error)]
pub enum InfraError {
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("http client error: {0}")]
    HttpClient(#[from] reqwest::Error),
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
}
```

### Domain 계층 (`domain/errors.rs` 또는 `crates/domain/src/errors.rs`)

비즈니스 규칙 위반과 도메인 개념으로 표현된 에러를 정의한다. 인프라 구체 타입을 노출하지 않는다:

```rust
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("user not found: {0}")]
    UserNotFound(String),
    #[error("duplicate email: {0}")]
    DuplicateEmail(String),
    #[error("insufficient balance")]
    InsufficientBalance,
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}

// infra 에러를 domain 에러로 변환
impl From<InfraError> for DomainError {
    fn from(e: InfraError) -> Self {
        DomainError::Internal(anyhow::anyhow!(e))
    }
}
```

### Api 계층 (`api/errors.rs` 또는 `crates/api/src/errors.rs`)

`DomainError`를 HTTP 응답으로 변환한다. Axum의 `IntoResponse`를 구현한다:

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;

pub struct AppError(pub DomainError);

impl From<DomainError> for AppError {
    fn from(e: DomainError) -> Self {
        AppError(e)
    }
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self.0 {
            DomainError::UserNotFound(id) => (
                StatusCode::NOT_FOUND,
                format!("User not found: {id}"),
            ),
            DomainError::DuplicateEmail(email) => (
                StatusCode::CONFLICT,
                format!("Email already in use: {email}"),
            ),
            DomainError::InsufficientBalance => (
                StatusCode::UNPROCESSABLE_ENTITY,
                "Insufficient balance".to_string(),
            ),
            DomainError::Internal(_) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                "Internal server error".to_string(),
            ),
        };

        (status, Json(json!({ "error": message }))).into_response()
    }
}
```

---

## 3. 핸들러에서의 에러 전파

핸들러에서 `?` 연산자로 에러를 전파하는 패턴:

```rust
pub async fn get_user(
    State(service): State<Arc<dyn UserService>>,
    Path(id): Path<i64>,
) -> Result<Json<UserResponse>, AppError> {
    // DomainError → AppError 자동 변환 (From impl)
    let user = service.get_user(id).await?;
    Ok(Json(user.into()))
}
```

`From<DomainError> for AppError` impl이 있으면 `?`가 자동으로 변환한다.

---

## 4. 개선점 보고

분석 결과를 바탕으로 현재 코드의 문제점과 권장 조치를 정리한다:

| 항목 | 현재 상태 | 권장 조치 |
|------|---------|---------|
| 에러 계층 분리 | (분석 결과) | (필요 시 분리 제안) |
| `unwrap`/`expect` | (발견 위치) | `?` 또는 명시적 처리로 교체 |
| `From` impl 누락 | (누락 경로) | impl 추가 |
| HTTP 상태 코드 매핑 | (매핑 존재 여부) | `IntoResponse` impl 추가 |
| 에러 메시지 노출 | (Internal 에러 노출 여부) | `Internal` 케이스는 generic 메시지 반환 |

코드 수정을 원하면 사용자에게 확인 후 진행한다. 이 스킬은 기본적으로 가이드형이며, 수정은 명시적 요청이 있을 때만 수행한다.

## After Analysis

1. 현재 에러 구조 요약 (계층 분리 여부, thiserror/anyhow 사용 여부).
2. 발견된 문제점 목록 (`unwrap`, `From` 누락, HTTP 매핑 미흡 등).
3. 권장 개선 순서:
   - 급함: `unwrap`/`expect` 제거 → 비즈니스 에러 정의 → `IntoResponse` 구현
   - 점진: 계층 분리 리팩토링 (기존 코드가 단일 에러 타입인 경우)
4. 수정을 원하면 `rust-service`, `rust-api` 스킬과 함께 사용하도록 안내한다.
