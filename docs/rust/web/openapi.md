---
title: OpenAPI 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# OpenAPI 원칙

`utoipa 5.x`를 사용하여 Rust 코드에서 OpenAPI 3.x 스펙을 생성한다. 핸들러 함수와 DTO에 매크로를 붙이면 런타임에 JSON 스펙이 자동 생성되고, Swagger UI로 서빙한다.

---

## 원칙

### 1. DTO에 `ToSchema`, 핸들러에 `#[utoipa::path]`를 붙인다

```rust
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, ToSchema)]
pub struct CreateUserRequest {
    /// 사용자 이메일 주소
    pub email: String,
    /// 사용자 이름 (2~50자)
    pub name: String,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct UserResponse {
    pub id: Uuid,
    pub email: String,
    pub name: String,
    pub created_at: DateTime<Utc>,
}

#[utoipa::path(
    post,
    path = "/users",
    request_body = CreateUserRequest,
    responses(
        (status = 201, description = "사용자 생성 성공", body = UserResponse),
        (status = 400, description = "잘못된 요청", body = ErrorResponse),
        (status = 409, description = "이미 존재하는 이메일"),
    ),
    tag = "users",
    security(("bearer_auth" = [])),
)]
pub async fn create_user(
    State(state): State<AppState>,
    Json(req): Json<CreateUserRequest>,
) -> impl IntoResponse {
    // ...
}
```

### 2. `#[derive(OpenApi)]`로 스펙 루트를 정의한다

```rust
use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    paths(
        users::create_user,
        users::get_user,
        users::list_users,
        users::delete_user,
    ),
    components(schemas(
        CreateUserRequest,
        UserResponse,
        ErrorResponse,
        Pagination,
    )),
    tags(
        (name = "users", description = "사용자 관리 API"),
    ),
    modifiers(&SecurityAddon),
    info(
        title = "My API",
        version = "1.0.0",
        description = "API 서버",
    )
)]
pub struct ApiDoc;

// Bearer 인증 스키마 추가
struct SecurityAddon;
impl Modify for SecurityAddon {
    fn modify(&self, openapi: &mut utoipa::openapi::OpenApi) {
        let components = openapi.components.get_or_insert_with(Default::default);
        components.add_security_scheme(
            "bearer_auth",
            SecurityScheme::Http(
                HttpBuilder::new()
                    .scheme(HttpAuthScheme::Bearer)
                    .bearer_format("JWT")
                    .build(),
            ),
        );
    }
}
```

### 3. Swagger UI를 axum 라우터에 마운트한다

```toml
[dependencies]
utoipa = { version = "5", features = ["axum_extras"] }
utoipa-swagger-ui = { version = "9", features = ["axum"] }
```

```rust
use utoipa_swagger_ui::SwaggerUi;

pub fn create_router(state: AppState) -> Router {
    Router::new()
        .merge(SwaggerUi::new("/swagger-ui")
            .url("/api-docs/openapi.json", ApiDoc::openapi()))
        .nest("/users", users::router())
        .with_state(state)
}
```

Swagger UI는 `/swagger-ui`에서, 원시 JSON은 `/api-docs/openapi.json`에서 접근 가능하다.

### 4. 대규모 앱은 `paths`를 모듈별로 분산한다

`#[derive(OpenApi)]`의 `paths`에 모든 핸들러를 나열하면 유지보수가 어렵다. 각 모듈에 서브 `OpenApi`를 정의하고 `merge`로 합친다.

```rust
#[derive(OpenApi)]
#[openapi(paths(create_user, get_user), components(schemas(UserResponse)))]
struct UsersApiDoc;

#[derive(OpenApi)]
#[openapi(paths(create_post, get_post), components(schemas(PostResponse)))]
struct PostsApiDoc;

// 최상위에서 머지
let mut doc = ApiDoc::openapi();
doc.merge(UsersApiDoc::openapi());
doc.merge(PostsApiDoc::openapi());
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| utoipa 버전 | 5.4.x | axum_extras feature 필요 |
| utoipa-swagger-ui 버전 | 9.0.x | axum feature 필요 |
| Swagger UI 경로 | `/swagger-ui` (프로덕션 비활성화) | 환경변수로 조건부 마운트 |

---

## 안티패턴

### `paths()`에 모든 핸들러를 한 파일에 나열

수십 개의 핸들러가 생기면 컴파일 시간이 늘고 충돌이 잦아진다. 모듈별 `OpenApi`를 분리하고 `merge`로 조합한다.

### 프로덕션에서 Swagger UI를 무조건 노출

내부 API 스펙이 외부에 노출된다. 환경 변수 `ENABLE_SWAGGER_UI` 등으로 조건부 마운트한다.

### `ToSchema`와 실제 직렬화 타입 불일치

`#[serde(rename_all = "camelCase")]`를 쓰면서 `ToSchema`에 반영하지 않으면 스펙과 실제 JSON이 다르다. `#[schema(rename_all = "camelCase")]`를 함께 명시한다.

---

## Gotchas

### `utoipa 5.x`에서 `axum_extras` feature가 필요

axum의 `Path`, `Query` extractor를 utoipa가 인식하려면 `features = ["axum_extras"]`를 활성화해야 한다. 없으면 extractor 파라미터가 스펙에 반영되지 않는다.

### `Modify` 트레잇으로만 런타임 스펙 변경 가능

`#[derive(OpenApi)]`는 컴파일 타임에 스펙을 생성한다. 서버 URL이나 보안 스키마처럼 환경에 따라 달라지는 값은 `Modify` 구현체를 통해 런타임에 주입한다.

### `openapi.json` 엔드포인트는 `GET`만 지원

`SwaggerUi::url()`이 등록하는 엔드포인트는 GET만 처리한다. 별도 인증이 필요하면 `.merge()` 이전에 미들웨어를 적용하거나, 스펙 엔드포인트를 직접 구현한다.

### 제네릭 타입은 `ToSchema` 자동 파생이 제한적

`PageResponse<T>`처럼 제네릭 타입은 `#[schema(value_type = ...)]`으로 구체 타입을 지정하거나, 사용되는 모든 구체 타입을 `components`에 등록해야 한다.
