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

- **도메인 레이어에 `anyhow::Error` 금지** — 라이브러리/도메인 코드에는 **`thiserror` 기반 구체 enum만** 사용한다. `anyhow::Error`는 app 최상위(`apps/api/src/main.rs`, CLI 스크립트)에서만 허용. 도메인 에러에 anyhow를 섞으면 호출자가 `match`로 case를 분기할 수 없어 에러 처리가 전부 "generic 500"으로 퇴화한다. 출처: fit-pal `server/CLAUDE.md` §코딩 컨벤션.
- **`.unwrap()`/`.expect()` 허용 범위** — 프로덕션 코드에서는 금지. 단 **main 초기화 (`main()` 안의 `std::env::var("...").expect(...)` 등)와 테스트 코드**에서는 허용한다 (fit-pal CLAUDE.md 금지 사항). 기타 위치에서 발견 시 즉시 `?` 또는 명시적 에러 처리로 교체를 제안한다.
- **`unsafe` 금지** — workspace-wide `unsafe_code = "forbid"` 원칙. 외부 FFI가 반드시 필요한 경우 외에는 `unsafe` 블록을 만들지 마라. FFI가 필요하면 별도 shared crate로 격리한다. 출처: fit-pal `workspace.lints.rust` 및 `CLAUDE.md` §금지 사항.
- **`println!` 대신 `tracing::info!`/`tracing::warn!`/`tracing::error!`** — 구조화 로깅 없이는 OTel 트레이싱/필드 추출이 불가능하다. 라이브러리 코드에서는 `println!`/`eprintln!`/`dbg!`를 사용하지 마라.
- **`From<SrcError> for DstError` 누락 시 컴파일 에러** — `?` 연산자 체이닝 시 변환 경로를 먼저 확인하라. `#[from]` 또는 `impl From`을 추가한다.
- **에러 variant에 HTTP status code 매핑 필수** — API 레이어에서 `IntoResponse`를 구현할 때 모든 에러 variant에 적절한 status code를 매핑해라. `NotFound → 404`, `Unauthorized → 401`, `Conflict → 409`. 매핑 누락 시 모든 에러가 `500 Internal Server Error`로 퇴화한다.
- **에러 메시지에 내부 정보 노출 금지** — `Display` impl에 SQL 쿼리, 스택 트레이스, DB 스키마 정보를 포함하면 API 응답으로 유출된다. 사용자 대면 메시지와 내부 로깅 메시지를 분리해라. `tracing::error!`에는 상세 정보를, 응답에는 generic 메시지만 보낸다.
- **`#[from]` 남용 시 에러 출처 모호화** — `thiserror`의 `#[from]`은 편리하지만, 동일 source error(예: `std::io::Error`)가 여러 variant에서 `#[from]`으로 사용되면 컴파일 에러가 난다. 이 경우 수동 `impl From`으로 context를 추가하거나 variant를 세분화해라.
- **`anyhow::Context` trait을 도메인 에러에 쓰지 마라** — `.context("...")`는 `anyhow::Error`에만 체이닝 가능하다. 도메인 `thiserror` enum에 context를 추가하려면 별도 variant에 `String` 필드를 두거나 `#[error(transparent)]`로 inner error를 감싸라.
- **에러 enum variant 폭발 방지** — 하나의 에러 enum에 15개 이상의 variant가 생기면 도메인 경계를 재검토해라. 모듈별로 에러를 분리하고 상위 에러에서 `#[from]`으로 합성하는 계층 구조를 사용한다.

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
