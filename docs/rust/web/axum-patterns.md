---
title: Axum 패턴
version: 0.1.0
last_updated: 2026-04-07
---

# Axum 패턴

Axum은 tokio와 tower 생태계 위에 구축된 ergonomic Rust 웹 프레임워크다. 0.8.x부터 Router, State, Extractor 구성 방식이 확립되었다. 매크로 없이 타입 시스템으로 라우팅과 미들웨어를 표현하는 것이 핵심이다.

---

## 원칙

### 1. Router는 계층적으로 구성한다

`Router::new()`에 라우트를 평면으로 나열하지 않는다. 도메인별로 `Router`를 분리하고 `.nest()`로 조합한다. 각 도메인 모듈이 자체 `router()` 함수를 반환하게 하면 변경 범위가 제한된다.

```rust
// api/src/routes/users.rs
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/:id", get(get_user).put(update_user).delete(delete_user))
}

// api/src/lib.rs
pub fn create_router(state: AppState) -> Router {
    Router::new()
        .nest("/users", users::router())
        .nest("/posts", posts::router())
        .with_state(state)
}
```

### 2. State는 `Arc`로 감싸거나 `Clone` 비용이 낮아야 한다

`axum::extract::State<T>`는 각 요청마다 `T`를 클론한다. `T`에 `PgPool`, `Arc<dyn Port>` 같은 저렴하게 클론 가능한 타입을 담는다. 무거운 리소스를 직접 포함하면 요청마다 복사 비용이 발생한다.

```rust
#[derive(Clone)]
pub struct AppState {
    pub db: PgPool,           // 내부적으로 Arc 사용
    pub auth: Arc<dyn AuthPort>,
    pub config: Arc<Config>,
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<Uuid>,
) -> impl IntoResponse {
    // ...
}
```

### 3. Extractor 조합으로 요청 파싱을 선언한다

`Path`, `Query`, `Json`, `Extension`, `TypedHeader` 등을 함수 파라미터로 선언하면 Axum이 자동으로 파싱하고 실패 시 400 응답을 반환한다. 핸들러 내부에서 `request.body()`를 직접 파싱하지 않는다.

```rust
#[derive(Deserialize)]
pub struct Pagination {
    pub page: Option<u32>,
    pub limit: Option<u32>,
}

async fn list_users(
    State(state): State<AppState>,
    Query(pagination): Query<Pagination>,
    Json(filter): Json<UserFilter>,
) -> impl IntoResponse {
    // ...
}
```

### 4. `IntoResponse` 구현으로 응답 타입을 통일한다

핸들러마다 `(StatusCode, Json<...>)` 튜플을 반복하지 않는다. `ApiResponse<T>` 래퍼 타입에 `IntoResponse`를 구현하고 공통 에러 변환을 처리한다.

```rust
pub enum ApiResponse<T: Serialize> {
    Ok(T),
    Created(T),
    Error(ApiError),
}

impl<T: Serialize> IntoResponse for ApiResponse<T> {
    fn into_response(self) -> Response {
        match self {
            Self::Ok(data) => (StatusCode::OK, Json(data)).into_response(),
            Self::Created(data) => (StatusCode::CREATED, Json(data)).into_response(),
            Self::Error(err) => err.into_response(),
        }
    }
}
```

### 5. `FromRequestParts`로 커스텀 Extractor를 구현한다

인증 토큰 추출, 요청 컨텍스트 주입 등 반복되는 파싱 로직은 커스텀 Extractor로 추출한다. 핸들러 시그니처가 의도를 명시적으로 표현하게 된다.

```rust
pub struct AuthUser(pub Claims);

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
    AppState: FromRef<S>,
{
    type Rejection = ApiError;

    async fn from_request_parts(parts: &mut Parts, state: &S) -> Result<Self, Self::Rejection> {
        let TypedHeader(Authorization(bearer)) =
            TypedHeader::<Authorization<Bearer>>::from_request_parts(parts, state)
                .await
                .map_err(|_| ApiError::Unauthorized)?;
        let app_state = AppState::from_ref(state);
        let claims = app_state.auth.verify_token(bearer.token()).await?;
        Ok(AuthUser(claims))
    }
}
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| Axum 최소 버전 | 0.8.x | `Router` API 안정화 |
| 핸들러당 Extractor 수 | 5개 이하 | 그 이상이면 커스텀 Extractor 묶음 고려 |
| `State` 클론 비용 | O(1) | `Arc`, `PgPool` 등 경량 핸들 사용 |
| `IntoResponse` 반환 타입 | `impl IntoResponse` | 구체 타입 노출 방지 |
| `#[async_trait]` 불필요 | Rust 1.75+ | 핸들러는 일반 async fn |

---

## 안티패턴

### `Router`에 `.with_state()`를 여러 번 호출

`with_state()`는 Router당 한 번만 호출한다. 서브 라우터에서 미리 호출하면 최상위 `with_state()`와 충돌한다. 서브 라우터는 타입 파라미터 `Router<AppState>`로 정의하고 최상위에서 한 번만 `with_state()`를 호출한다.

### 핸들러에서 `request` 직접 파싱

`Request<Body>`를 핸들러 파라미터로 받아 내부에서 파싱하면 Extractor 시스템을 우회한다. 타입 안전성과 에러 일관성이 깨진다.

### `Extension`으로 모든 데이터 전달

`Extension<T>`는 타입당 하나만 삽입할 수 있고 런타임 패닉이 발생할 수 있다. State 또는 커스텀 Extractor를 사용한다.

### 핸들러 반환 타입에 구체 타입 노출

`Json<Vec<UserDto>>`를 직접 반환하면 응답 포맷 변경 시 시그니처를 수정해야 한다. `impl IntoResponse`로 추상화한다.

---

## Gotchas

### `State<T>`는 `FromRef<S>` 기반으로 부분 추출된다

서브 라우터가 `AppState`의 일부만 필요하면 `FromRef<AppState> for SubState`를 구현한다. 전체 `AppState`를 공유하지 않아도 된다.

```rust
impl FromRef<AppState> for PgPool {
    fn from_ref(state: &AppState) -> Self {
        state.db.clone()
    }
}
```

### Extractor 순서가 소비 순서를 결정한다

`Body`를 소비하는 Extractor(`Json`, `Bytes`, `String`)는 함수 파라미터 중 마지막에 위치해야 한다. `Path`, `Query`, `State`가 먼저 와야 한다. 순서가 틀리면 컴파일 에러가 발생한다.

### `Router`는 `Send + Sync`를 요구한다

핸들러에서 `Rc`, `Cell` 등 `!Send` 타입을 캡처하면 컴파일 에러가 발생한다. tokio 멀티스레드 런타임에서 모든 핸들러는 `Send`여야 한다.

### 404 폴백은 `fallback()` 메서드로 처리한다

매칭되지 않는 경로에 대한 응답은 `Router::fallback(handler)`로 설정한다. 미들웨어에서 처리하지 않는다.

### `tower::ServiceBuilder` 레이어 순서가 요청/응답 방향을 결정한다

`.layer()`를 호출한 순서가 요청에 대해서는 역순(마지막 layer가 먼저 실행), 응답에 대해서는 정순으로 적용된다. 레이어 순서 의존성이 있는 미들웨어(예: auth → rate-limit)는 `ServiceBuilder`로 명시적으로 묶는다.
