---
title: 미들웨어 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 미들웨어 원칙

tower는 Rust 비동기 서비스 추상화 라이브러리다. `Service` trait이 미들웨어 합성의 핵심이며, axum은 tower 위에 구축되어 있다. `ServiceBuilder`로 레이어를 조합하고, `tower-http`가 HTTP 전용 미들웨어를 제공한다.

---

## 원칙

### 1. `ServiceBuilder`로 레이어를 선언적으로 조합한다

`ServiceBuilder::new().layer(A).layer(B).service(inner)`는 A → B → inner 순서로 요청을 처리한다. 나중에 추가한 레이어가 요청을 나중에 본다. 응답은 반대 방향이다.

```rust
use tower::ServiceBuilder;
use tower_http::{trace::TraceLayer, cors::CorsLayer, compression::CompressionLayer};

let middleware = ServiceBuilder::new()
    .layer(SetRequestIdLayer::x_request_id(MakeRequestUuid))
    .layer(TraceLayer::new_for_http())
    .layer(CorsLayer::permissive())
    .layer(CompressionLayer::new());

let app = Router::new()
    .route("/", get(handler))
    .layer(middleware);
```

### 2. `axum::middleware::from_fn`으로 간단한 미들웨어를 작성한다

tower `Service` 구현 없이 async fn 하나로 미들웨어를 정의한다. 상태가 필요하면 `from_fn_with_state`를 사용한다.

```rust
async fn auth_middleware(
    State(state): State<AppState>,
    request: Request,
    next: Next,
) -> impl IntoResponse {
    let token = request
        .headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok())
        .and_then(|v| v.strip_prefix("Bearer "));

    match token {
        Some(t) if state.auth.verify(t).is_ok() => next.run(request).await,
        _ => StatusCode::UNAUTHORIZED.into_response(),
    }
}

let app = Router::new()
    .route("/protected", get(handler))
    .layer(axum::middleware::from_fn_with_state(state.clone(), auth_middleware));
```

### 3. `tower-http` 레이어를 상황에 맞게 선택한다

| 레이어 | 용도 |
|--------|------|
| `TraceLayer` | 요청/응답 구조화 로깅 |
| `CorsLayer` | CORS 헤더 처리 |
| `CompressionLayer` | gzip/brotli 응답 압축 |
| `TimeoutLayer` | 요청 타임아웃 |
| `SetRequestIdLayer` / `PropagateRequestIdLayer` | 요청 ID 생성 및 전파 |
| `RequestBodyLimitLayer` | 요청 바디 크기 제한 |
| `CatchPanicLayer` | 핸들러 패닉 500 변환 |
| `NormalizePathLayer` | 후행 슬래시 정규화 |

### 4. `TraceLayer`를 커스터마이징하여 구조화 스팬을 만든다

```rust
use tower_http::trace::{TraceLayer, DefaultMakeSpan, DefaultOnResponse};

TraceLayer::new_for_http()
    .make_span_with(
        DefaultMakeSpan::new()
            .level(Level::INFO)
            .include_headers(false),
    )
    .on_response(
        DefaultOnResponse::new()
            .level(Level::INFO)
            .latency_unit(LatencyUnit::Micros),
    )
    .on_failure(DefaultOnFailure::new().level(Level::ERROR))
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| tower 버전 | 0.5.x | axum 0.8과 호환 |
| tower-http 버전 | 0.6.x | axum 0.8과 호환 |
| 권장 레이어 순서 | request-id → trace → cors → compression → timeout | 요청 기준 처리 순서 |
| `from_fn` vs `Service` | 간단한 로직은 `from_fn` | 복잡한 상태/스트리밍은 직접 구현 |

---

## 안티패턴

### `.layer()` 순서 혼동

`Router::layer()`에서 나중에 추가한 레이어가 요청을 먼저 처리한다(`ServiceBuilder`와 반대). `ServiceBuilder`로 한 번에 묶어 `.layer(middleware_stack)`으로 넘기면 순서를 명확하게 유지할 수 있다.

### 미들웨어에서 응답 바디 소비 후 재전달

`from_fn`에서 `next.run(request).await`로 받은 응답의 바디를 소비하면 클라이언트에 전달할 바디가 없어진다. 응답 바디 검사가 필요하면 `body::to_bytes()`로 버퍼링 후 `Response::new(body)`로 재구성한다.

### 모든 라우트에 무거운 미들웨어 적용

인증 미들웨어를 공개 엔드포인트에도 걸면 불필요한 오버헤드가 생긴다. `Router::merge()`로 인증 필요/불필요 라우터를 분리한 뒤 각각에만 미들웨어를 적용한다.

---

## Gotchas

### `tower 0.4` → `0.5` 호환성

tower 0.5에서 `ServiceExt`, `ServiceBuilder` API 일부가 변경됐다. axum 0.8은 tower 0.5를 요구한다. 직접 tower 의존성을 추가할 때 버전을 맞춰야 컴파일 에러가 나지 않는다.

### `from_fn` 미들웨어에서 `Request`를 소비하면 다음 핸들러에 전달 불가

`next.run(request)` 호출 전에 `request`를 분해하면 소유권이 이동한다. 요청 헤더나 경로만 검사할 때는 `request.headers()`로 참조만 가져오고, 요청 전체를 넘겨야 할 때는 소유권을 유지한다.

### `CorsLayer::permissive()`는 프로덕션에서 사용 금지

`permissive()`는 모든 출처, 헤더, 메서드를 허용한다. 프로덕션에서는 `CorsLayer::new().allow_origin(...)` 으로 허용 목록을 명시한다.

### 레이어와 라우터 선언 순서

`Router::layer()`는 그 시점까지 추가된 라우트에만 적용된다. `.layer()` 이후에 추가한 라우트에는 적용되지 않는다. 모든 라우트를 먼저 등록하고 마지막에 `.layer()`를 호출한다.
