---
name: rust-api
description: >
  Axum 라우터/핸들러를 생성하고 OpenAPI 스펙을 등록한다.
  Hexagonal Architecture 기반으로 포트(trait) 정의 → 어댑터(impl) 구현 순서로 생성한다.
  "API 추가", "엔드포인트 추가", "핸들러 만들어줘", "라우터 추가", "rust api" 같은 요청 시 사용한다.
argument-hint: "<feature> <HTTP_METHOD> <path>"
user-invocable: true
---

## Gotchas

- **Axum 0.8 path parameter 문법 breaking change** — 0.8부터 `:id` colon 문법이 **완전 제거**되고 `{id}` 중괄호 문법만 지원한다. `.route("/users/:id", ...)` 는 컴파일 에러다. 반드시 `.route("/users/{id}", ...)`로 작성한다. 와일드카드는 `{*rest}`. (Axum 0.8 announcement 2024-12-01, matchit 2.x)
- **Axum 0.8 `#[async_trait]` 제거** — `FromRequest`, `FromRequestParts`, `Handler` 등 핵심 trait이 native `async fn in trait`으로 전환되었다. 사용자 extractor를 구현할 때 `#[async_trait]` 매크로를 **붙이지 말고** `async fn from_request_parts(...) -> Result<Self, Self::Rejection>`를 직접 선언한다. `axum::async_trait` 재수출은 deprecated.
- **State는 `Router::with_state()`로 주입** — `Extension` 레이어나 글로벌 상태를 쓰지 마라. 타입 안전성이 깨진다. 테스트 시 mock trait object를 주입하려면 `State<Arc<dyn Port>>` 패턴을 사용한다.
- **`Json<T>` 추출자는 요청 본문을 한 번만 소비** — 한 핸들러에서 `Json`과 `Bytes`를 동시에 추출하거나 두 번 추출하면 컴파일 에러가 난다.
- **`Path<(String, i64)>` 순서 일치 필수** — URL 세그먼트 순서와 정확히 일치해야 한다. 순서가 틀리면 런타임에 추출 실패한다. 복수 파라미터는 구조체 + `#[derive(Deserialize)]`로 이름 기반 추출을 선호하라 (`Path<UserIdPath>`).
- **포트에서 인프라 타입 제거** — 핸들러가 의존하는 `UserService`/`UserRepository` trait 시그니처에 `sqlx::Error`, `PgPool`, `sea_orm::DatabaseConnection`, `sea_orm::DbErr` 등 인프라 구체 타입을 노출하지 마라. DTO/`DomainError`만 주고받는다. 포트가 DB 타입을 노출하면 adapter 교체가 불가능해진다. 출처: fit-pal `server/CLAUDE.md`.
- **Composition Root 단일화** — 핸들러가 서비스 구현체를 직접 `UserServiceImpl::new(...)`로 생성하지 마라. 모듈 조립(DI 와이어링)은 `apps/api/src/main.rs` 한 곳에서만 하고, 핸들러는 `State<Arc<dyn UserServicePort>>`로 trait object만 받는다. Composition Root가 여러 곳에 흩어지면 테스트에서 mock 주입이 불가능해지고, 모듈 간 의존 그래프가 불투명해진다. 출처: fit-pal `server/CLAUDE.md` §아키텍처 3번.
- **라우트 네이밍은 복수형 명사 + RESTful 동사 매핑** — `/user`가 아니라 `/users`. 동작은 HTTP method로 표현하고 URL에 동사를 넣지 마라(`/users/delete` 금지 → `DELETE /users/{id}`). 비-CRUD 동작만 예외적으로 `/users/{id}/activate` 같은 동사 경로를 허용한다.
- **응답 타입은 항상 `Json<T>`로 래핑** — 핸들러가 raw `String`이나 `impl IntoResponse`를 반환하면 OpenAPI(utoipa) 스키마 생성이 불가능하다. `Json<ResponseDto>`를 반환하고 `#[utoipa::path(..., responses(...))]`로 문서화해라.
- **Extractor 순서 의존성** — Axum에서 body를 소비하는 extractor(`Json`, `Form`, `Multipart`)는 반드시 마지막 인자여야 한다. `Path`, `Query`, `State`는 body를 소비하지 않으므로 앞에 둔다. 순서가 틀리면 런타임에 "Missing request body" 에러가 발생한다.
- **핸들러 state 에 인프라 타입 직접 주입 금지 (SK-03 회귀 방지)** — `State<PgPool>` · `State<sqlx::PgPool>` · `State<sea_orm::DatabaseConnection>` 같이 핸들러 시그니처에 DB pool/connection 구체 타입을 직접 받으면 Composition Root 단일화가 깨지고 mock 주입이 불가능해진다. 항상 `State<Arc<dyn UserService>>` trait object 형태만 허용하고, 인프라 타입(`PgPool` 등)은 `infra/adapters/*_impl.rs` 어댑터 레이어에만 등장해야 한다. Grep 체크: `grep -n "State<PgPool>\|State<sqlx::\|State(pool)" src/api/handlers/` 결과 0 건이어야 한다. 출처: fit-pal `server/CLAUDE.md` §아키텍처 3번 + Axum 0.8 docs `with_state` 패턴(https://docs.rs/axum/latest/axum/struct.Router.html#method.with_state).
- **Enumerate-before-Act (skill-design-guide §5.5)** — 엔드포인트를 추가하기 전, 기존 핸들러 파일을 `Grep`/`Glob` 으로 전수 스캔하여 (a) 중복 라우트, (b) 유사 네이밍 충돌, (c) 기존 `ApiDoc` 등록 경로를 먼저 열거한다. 열거 결과를 간단 체크리스트로 사용자에게 보이고 합의한 뒤에만 파일을 생성한다. 선(先) 작성 후(後) 중복 발견은 롤백 비용이 크다.
- **Sibling Consistency (skill-design-guide §8.8)** — `rust-api` 는 `rust-service` · `rust-model` · `rust-middleware` · `rust-auth` 와 함께 Hexagonal 레이어 세트를 구성한다. 핸들러에서 "포트에서 인프라 타입 제거" 원칙을 강조할 때 sibling 스킬의 동일 원칙 문구 (rust-service Gotcha "포트에서 인프라 타입 제거") 와 네이밍·출처를 일치시킨다. 드리프트가 발생하면 동일 표현으로 복제.

# Axum 핸들러/라우터 생성

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `$PACKAGE`, `ARCH`, `IS_WORKSPACE`, `HAS_AXUM`, `HAS_UTOIPA`, `HAS_SERDE`)를 사용한다.

`HAS_AXUM`이 false이면 중단하고 사용자에게 알린다:
> `Cargo.toml`에 `axum` 의존성이 없습니다. `cargo add axum tokio --features tokio/full`으로 추가하세요.

---

## 1. 입력 확인

`$ARGUMENTS`에서 파싱하거나 사용자에게 확인한다:

| 항목 | 예시 |
|------|------|
| feature 이름 | `users` |
| HTTP 메서드 | `GET`, `POST`, `PUT`, `DELETE`, `PATCH` |
| 경로 | `/users/:id` |
| Request 스키마 | 필드 목록 또는 "없음" |
| Response 스키마 | 필드 목록 |
| 에러 반환 방식 | 기존 `AppError` 타입 탐색 후 확인 |

---

## 2. 기존 패턴 읽기

핸들러를 생성하기 전에 기존 핸들러 파일을 읽어 프로젝트 컨벤션을 파악한다:

- 에러 반환 타입 (`AppError`, `ApiError`, 커스텀 enum 등)
- 추출자 사용 패턴 (`State`, `Json`, `Path`, `Query`, `Extension`)
- Response 래핑 방식 (`Json<T>`, `(StatusCode, Json<T>)`, 커스텀 `ApiResponse<T>`)
- 라우터 등록 위치 (`router.rs`, `routes.rs`, `main.rs` 등)

---

## 3. 포트 정의

`domain/ports/` (또는 `ARCH = modular`이면 `src/domain/ports/`)에 핸들러가 의존할 서비스 trait을 정의한다.

- SQLx, HTTP 클라이언트 등 구체 인프라 타입을 trait 시그니처에 노출하지 않는다.
- 이미 해당 서비스 trait이 있으면 새로 만들지 말고 기존 trait을 사용한다.

```rust
// domain/ports/user_service.rs
use crate::domain::models::{User, CreateUserRequest};
use crate::domain::errors::DomainError;

/// Rust 1.75+ native async fn in trait — `#[async_trait]` 불필요.
/// `dyn Trait`이 필요한 경우만 `#[async_trait]` 사용 (trait object dispatch).
pub trait UserService: Send + Sync {
    fn create_user(&self, req: CreateUserRequest) -> impl Future<Output = Result<User, DomainError>> + Send;
    fn get_user(&self, id: i64) -> impl Future<Output = Result<User, DomainError>> + Send;
}
```

> **`dyn Trait` 필요 시**: `State<Arc<dyn UserService>>`처럼 trait object로 사용해야 한다면 native async fn in trait은 object-safe하지 않으므로 `#[async_trait]`을 유지한다. Composition Root에서 제네릭 `<S: UserService>`로 받는 경우에는 native async fn을 선호한다.

`mod.rs`에 `pub mod user_service;`를 추가한다.

---

## 4. 어댑터 구현

`infra/adapters/` (또는 `ARCH = modular`이면 `src/infra/adapters/`)에 trait impl을 생성한다.

- 구체 크레이트 의존(`sqlx`, `redis`, 외부 HTTP 클라이언트 등)은 이 레이어에만 존재한다.
- 이미 구현체가 있으면 메서드만 추가한다.

```rust
// infra/adapters/user_service_impl.rs  — 예시 스켈레톤 (실제 사용 시 SQL/ORM 쿼리 구현 필요)
use async_trait::async_trait;
use sqlx::PgPool;
use crate::domain::ports::UserService;
use crate::domain::models::{User, CreateUserRequest};
use crate::domain::errors::DomainError;

pub struct UserServiceImpl {
    pool: PgPool,
}

impl UserServiceImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl UserService for UserServiceImpl {
    async fn create_user(&self, req: CreateUserRequest) -> Result<User, DomainError> {
        // 예시: 실제 프로젝트에서는 sqlx::query_as!(..) 또는 SeaORM ActiveModel로 교체
        unimplemented!("예시 스켈레톤 — SQLx/SeaORM 구현 필요")
    }

    async fn get_user(&self, id: i64) -> Result<User, DomainError> {
        unimplemented!("예시 스켈레톤 — SQLx/SeaORM 구현 필요")
    }
}
```

> `#[async_trait]`은 user-defined trait에는 여전히 사용 가능하다 (Axum 0.8은 프레임워크 trait에서만 제거했다). 단, Rust 1.75+ RPITIT로 작성하면 heap allocation을 줄일 수 있으며 `dyn Trait`이 필요 없는 경우 우선 고려한다.

---

## 5. 핸들러 + 라우터 생성

핸들러는 포트(trait 객체)를 `State`로 주입받는다. 구체 구현 타입을 핸들러에서 직접 참조하지 않는다.

```rust
// api/handlers/users.rs
use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use std::sync::Arc;
use crate::domain::ports::UserService;
use crate::domain::models::{CreateUserRequest, UserResponse};
use crate::api::errors::AppError;

pub async fn create_user(
    State(service): State<Arc<dyn UserService>>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<UserResponse>), AppError> {
    let user = service.create_user(payload).await?;
    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn get_user(
    State(service): State<Arc<dyn UserService>>,
    Path(id): Path<i64>,
) -> Result<Json<UserResponse>, AppError> {
    let user = service.get_user(id).await?;
    Ok(Json(user.into()))
}
```

라우터에 등록한다. **Axum 0.8 path 문법은 `{id}` 중괄호만 지원**한다:

```rust
// api/router.rs 또는 api/routes/users.rs
use axum::Router;
use std::sync::Arc;
use crate::domain::ports::UserService;
use super::handlers::users;

pub fn users_router(service: Arc<dyn UserService>) -> Router {
    Router::new()
        .route("/users", axum::routing::post(users::create_user))
        .route("/users/{id}", axum::routing::get(users::get_user))
        .with_state(service)
}
```

> `.route("/users/:id", ...)`은 Axum 0.8에서 **컴파일 에러**가 난다. 기존 0.7 프로젝트를 마이그레이션할 때는 정규식 `:\w+`로 모든 라우트 문자열을 일괄 치환한다. 와일드카드는 `*rest` → `{*rest}`.

---

## 6. OpenAPI 등록 (HAS_UTOIPA)

`HAS_UTOIPA`이면 핸들러에 `#[utoipa::path]` 어노테이션을 추가하고, `ApiDoc`에 경로와 스키마를 등록한다.

```rust
#[utoipa::path(
    post,
    path = "/users",
    request_body = CreateUserRequest,
    responses(
        (status = 201, description = "유저 생성 성공", body = UserResponse),
        (status = 400, description = "잘못된 요청"),
        (status = 500, description = "서버 오류"),
    ),
    tag = "users"
)]
pub async fn create_user(/* ... */) { /* ... */ }
```

기존 `ApiDoc` struct에 경로와 스키마를 추가한다:
```rust
#[derive(OpenApi)]
#[openapi(
    paths(users::create_user, users::get_user),  // 추가
    components(schemas(CreateUserRequest, UserResponse)),  // 추가
)]
struct ApiDoc;
```

---

## 7. 빌드 확인

생성 완료 후 안내한다:

> `cargo build`로 컴파일 에러를 확인하세요.
> 에러가 있으면 `rust-build` 스킬로 clippy 진단도 함께 실행할 수 있습니다.

## After Creation

1. 생성/수정된 파일 목록 출력.
2. 라우터를 상위 `Router`에 `.merge()` 또는 `.nest()`로 등록하는 위치를 안내한다.
3. `HAS_UTOIPA`이면 `ApiDoc`에 경로/스키마 등록 여부를 확인한다.
4. 다음 단계 안내:
   - DB 모델이 필요하면 `rust-model` 스킬로 Repository trait + SQLx impl을 생성하세요.
   - 서비스 비즈니스 로직을 채우려면 `rust-service` 스킬을 사용하세요.

# References

- references/project-detection.md
- templates/rust-api-handler.rs.template — Axum 핸들러 템플릿
