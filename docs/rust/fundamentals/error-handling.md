---
title: 에러 처리 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 에러 처리 원칙

Rust의 에러 처리는 `Result<T, E>`로 표현된다. panic은 복구 불가능한 프로그래밍 오류에만 사용하고, 예상 가능한 실패는 모두 `Result`로 전파한다. 라이브러리 크레이트와 애플리케이션 크레이트는 에러 전략이 다르다.

---

## 원칙

### 1. 라이브러리는 `thiserror`, 애플리케이션은 `anyhow`

두 크레이트는 목적이 다르다.

- **thiserror**: 라이브러리(domain, adapters) 전용. `derive(Error)`로 구체 에러 타입을 생성한다. 호출자가 매칭할 수 있는 타입 정보를 보존한다.
- **anyhow**: 애플리케이션 바이너리(main.rs, CLI, scripts) 전용. `Box<dyn Error>`를 `?`로 전파할 때 컨텍스트를 추가한다. 타입 정보는 소실되지만 개발 생산성이 높다.

```rust
// 라이브러리 — thiserror
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("user not found: {id}")]
    NotFound { id: UserId },
    #[error("persistence error: {0}")]
    Persistence(String),
    #[error("validation failed: {field} — {reason}")]
    Validation { field: String, reason: String },
}

// 애플리케이션 — anyhow
fn main() -> anyhow::Result<()> {
    let config = Config::load().context("config 로드 실패")?;
    run(config).await
}
```

> **출처:** [thiserror README](https://github.com/dtolnay/thiserror), [anyhow README](https://github.com/dtolnay/anyhow)

### 2. 3계층 에러 변환: Infra → Domain → API

에러는 계층 경계에서 변환된다. 하위 계층의 에러 타입이 상위 계층에 노출되면 의존성 역전이 발생한다.

```
sqlx::Error → DomainError::Persistence   (Adapter 책임)
DomainError → ApiError                   (Handler 책임)
ApiError    → HTTP Response              (IntoResponse 책임)
```

```rust
// Adapter: sqlx::Error → DomainError
impl From<sqlx::Error> for DomainError {
    fn from(e: sqlx::Error) -> Self {
        match e {
            sqlx::Error::RowNotFound => DomainError::NotFound { id: UserId::default() },
            _ => DomainError::Persistence(e.to_string()),
        }
    }
}

// Handler: DomainError → HTTP 응답 (axum)
impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, body) = match self {
            ApiError::Domain(DomainError::NotFound { .. }) => (StatusCode::NOT_FOUND, "not found"),
            ApiError::Domain(DomainError::Validation { .. }) => (StatusCode::UNPROCESSABLE_ENTITY, "validation error"),
            _ => (StatusCode::INTERNAL_SERVER_ERROR, "internal error"),
        };
        (status, body).into_response()
    }
}
```

> **출처:** [axum — Error Handling](https://docs.rs/axum/latest/axum/error_handling/index.html)

### 3. `?` 연산자와 `From` impl로 보일러플레이트를 제거한다

`From<E1> for E2`가 구현되어 있으면 `?`가 자동으로 변환한다. `#[from]` 속성(thiserror)으로 `From` impl을 자동 생성할 수 있다.

```rust
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("db error: {0}")]
    Db(#[from] sqlx::Error),   // From<sqlx::Error> 자동 생성

    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
}

async fn load_user(id: UserId, pool: &PgPool) -> Result<User, DomainError> {
    let row = sqlx::query_as!(UserRow, "SELECT * FROM users WHERE id = $1", id.0)
        .fetch_one(pool)
        .await?; // sqlx::Error → DomainError::Db 자동 변환
    Ok(row.into())
}
```

> **출처:** [thiserror — `#[from]` attribute](https://docs.rs/thiserror/latest/thiserror/)

### 4. 에러 컨텍스트를 보존한다

에러 메시지만으로는 원인 파악이 어렵다. `.context()` (anyhow) 또는 `#[error("... {source}")]` (thiserror)로 원인 체인을 유지한다. 로그에 남길 때는 `{:?}` (Display + cause chain)를 사용한다.

```rust
// anyhow — 컨텍스트 추가
let user = repo.find(id).await
    .context(format!("user {id} 조회 실패"))?;

// 에러 로깅
tracing::error!(error = %err, "요청 처리 실패");       // Display
tracing::error!(error = ?err, "요청 처리 실패");       // Debug (cause chain)
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| `Result<T, E>` 반환 오버헤드 | ~0ns | 값 크기만큼 스택 이동 |
| `Box<dyn Error>` (anyhow) | ~1 힙 할당 | 에러 경로에서만 발생 |
| `unwrap()` panic 비용 | 프로세스 종료 | 에러 경로에서 사용 금지 |
| `From` 변환 | ~0ns | 인라인 컴파일 |
| thiserror derive 컴파일 추가 시간 | ~무시 가능 | proc-macro, 한 번만 실행 |

---

## 안티패턴

### `.unwrap()` / `.expect()` 프로덕션 코드에 남기기

`.unwrap()`은 테스트 코드와 불가능한 상황(`// SAFETY: ...`로 설명된)에만 허용한다. 서비스 코드에서 `.unwrap()`은 프로세스를 종료시킨다. Clippy `unwrap_used` lint를 활성화하여 감지한다.

### 모든 에러를 `String`으로 변환

`DomainError::Persistence(e.to_string())`처럼 에러를 String으로 변환하면 호출자가 에러를 프로그래밍적으로 처리할 수 없다. 구조체 variant를 사용하고 원본 에러를 `source`로 보존한다.

### 라이브러리에 `anyhow` 사용

`anyhow::Error`를 라이브러리 public API의 에러 타입으로 반환하면 호출자가 에러 종류를 매칭할 수 없다. 라이브러리는 반드시 구체 에러 타입(thiserror)을 노출한다.

### 에러를 무시하고 기본값 반환

`result.unwrap_or_default()`로 에러를 조용히 삼키는 코드. 에러가 발생했는지 알 수 없다. 에러를 로그에 남기거나 상위로 전파한다.

---

## Gotchas

### `#[from]`과 수동 `From` impl이 충돌한다

thiserror `#[from]` 속성은 `From` impl을 자동 생성한다. 동일한 `From<E>` impl을 수동으로 작성하면 "conflicting implementations" 컴파일 에러가 발생한다. `#[from]`을 사용할 때는 수동 impl을 제거한다.

### `IntoResponse` impl에서 민감 정보 노출

`DomainError`를 직접 HTTP 응답 body에 포함하면 내부 구현(DB 쿼리, 스택 트레이스)이 클라이언트에 노출된다. API 레이어에서 별도 `ApiError`로 변환하고, 사용자에게는 추상적인 메시지만 반환한다.

### `?` 연산자는 `async` 클로저 안에서 주의가 필요하다

`tokio::spawn(async { some_result? })` 패턴은 에러가 spawn된 태스크 안에서 소실될 수 있다. `JoinHandle`의 반환값을 `.await`하고 에러를 처리해야 한다.

### 에러 타입이 `Send + Sync`를 구현하지 않으면 tokio task에서 사용 불가

`Arc<dyn Error>`를 tokio task 간에 전달하려면 에러가 `Send + Sync`여야 한다. thiserror derive는 구현체가 `Send + Sync`이면 자동으로 만족한다. `Box<dyn Error>`는 기본적으로 `Send + Sync`가 아니므로 `Box<dyn Error + Send + Sync>`를 사용한다.
