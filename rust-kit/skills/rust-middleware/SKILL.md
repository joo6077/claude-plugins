---
name: rust-middleware
description: >
  Axum 미들웨어를 생성하고 라우터에 등록한다. CORS, request logging, rate limiting,
  request ID, timeout 등을 tower Layer 패턴으로 추가한다.
  "미들웨어 추가", "CORS", "rate limit", "로깅 미들웨어", "rust middleware" 같은 요청 시 트리거.
argument-hint: "[cors|logging|rate-limit|request-id|timeout]"
user-invocable: true
---

# Gotchas

1. **tower 레이어 순서** — `.layer()`는 안쪽부터 바깥으로 적용된다. 마지막에 등록한 `.layer()`가 요청을 가장 먼저 받는다. CORS는 바깥쪽(마지막)에, 인증은 안쪽(먼저)에 등록한다.
2. **tower-http 0.6 feature 조합** — Axum 0.8과 호환되는 tower-http 버전은 **0.6.x** (fit-pal 기준 `tower-http = "0.6.8"`). `Cargo.toml`에 `tower-http = { version = "0.6", features = ["cors", "trace", "request-id", "timeout", "compression-gzip", "limit"] }`처럼 필요한 feature를 명시한다. feature를 빠뜨리면 `CorsLayer`/`TraceLayer`/`TimeoutLayer` 타입이 아예 제공되지 않고 컴파일 에러가 난다.
3. **rate limiting 상태는 공유 저장소 필요** — `Arc<Mutex<HashMap>>` 방식은 단일 인스턴스에서만 동작한다. 멀티 인스턴스(K8s 등) 환경이면 Redis 어댑터가 필요하다. 구현 전에 배포 환경을 확인한다. 실무 2026 표준은 `tower_governor = "0.8"` + `governor = "0.10"` 조합으로 in-memory GCRA rate limiting을 시작하고, 멀티 인스턴스에서 Redis로 이주 (fit-pal 실무 기준).
4. **`governor`/`tower_governor` Axum 호환 버전** — `tower_governor 0.8` + `axum 0.8` + `tower-http 0.6` 조합이 2026-04 기준 안정적. 버전 mismatch 시 `Service` trait bound 에러가 발생한다.
5. **`from_fn`은 `State` extractor를 지원하지 않는다** — `middleware::from_fn` 클로저 안에서 `State(s): State<AppState>`를 뽑으면 컴파일 에러가 난다. 상태가 필요한 미들웨어는 반드시 **`middleware::from_fn_with_state(state, f)`**를 사용한다. Axum 0.7/0.8 마이그레이션에서 가장 흔한 "왜 State가 안 뽑히지?" 류 오류 포인트다.
6. **`from_fn` 계열 extractor 순서 제약** — 미들웨어 함수 시그니처는 `FromRequestParts` extractor 0개 이상 + (선택) 하나의 `FromRequest` extractor + 마지막 인자 `Next` 순서여야 한다. 커스텀 extractor와 `Request`를 섞을 때 인자 순서가 틀리면 에러 메시지가 장황하고 원인 파악이 어렵다.

# Process

## Gotchas

- **미들웨어 적용 순서가 실행 순서와 반대임을 잊지 마라** — Axum에서 `.layer(A).layer(B)` 순서로 추가하면 요청은 B → A 순서로 통과한다. CORS를 인증보다 먼저 실행하려면 인증을 먼저 `.layer()`하고 CORS를 나중에 `.layer()`해야 한다.
- **CORS preflight(OPTIONS)를 인증 미들웨어가 차단하지 않도록 하라** — 브라우저의 preflight 요청은 Authorization 헤더를 포함하지 않는다. 인증 미들웨어에서 OPTIONS 메서드를 예외 처리하거나, CORS 레이어를 인증 밖에 배치하라.
- **Tower Layer와 Axum handler middleware를 혼동하지 마라** — `tower::Layer`는 `Service`를 감싸는 범용 래퍼, `axum::middleware::from_fn`은 Axum 전용 함수형 미들웨어다. 재사용성이 필요하면 Layer, 빠른 프로토타이핑이면 `from_fn`을 사용하라.
- **rate limiter 상태를 요청마다 새로 생성하지 마라** — `Arc<Mutex<HashMap<IpAddr, ...>>>`나 `governor` 크레이트의 `RateLimiter`를 앱 상태에 한 번 생성하고 공유하라. 미들웨어 함수 안에서 매번 새 인스턴스를 만들면 제한이 작동하지 않는다.
- **로깅 미들웨어에서 요청 body를 소비하지 마라** — `Body`를 읽으면 후속 핸들러가 body를 사용할 수 없다. `tower_http::trace::TraceLayer`를 사용하거나, body를 clone한 후 되돌려 넣어야 한다.
- **`CorsLayer::permissive()`를 프로덕션에 사용하지 마라** — 개발 편의용이며, 모든 origin/method/header를 허용한다. 프로덕션에서는 `.allow_origin()`, `.allow_methods()`, `.allow_headers()`를 명시적으로 설정하라.
- **미들웨어에서 `next.run(req).await` 호출을 빠뜨리지 마라** — `from_fn` 미들웨어에서 next를 호출하지 않으면 요청이 핸들러에 도달하지 못하고 영원히 대기하거나 즉시 응답한다. early return 경로에서도 의도적인지 확인하라.
- **에러 응답 형식을 미들웨어마다 다르게 만들지 마라** — 인증 실패는 JSON, rate limit은 plain text로 응답하면 클라이언트 파싱이 깨진다. 모든 미들웨어 에러 응답을 `application/json` 형식의 통일된 에러 구조체로 반환하라.
- **타임아웃 미들웨어를 라우트 전체에 일괄 적용하지 마라** — 파일 업로드, WebSocket, SSE 같은 장시간 연결은 별도 타임아웃이 필요하다. `tower_http::timeout::TimeoutLayer`를 라우트 그룹별로 차등 적용하라.
- **미들웨어의 타입 에러를 `Box<dyn Error>`로 뭉뚱그리지 마라** — Axum의 `HandleError`나 `IntoResponse` 구현에서 구체적 에러 타입을 사용해야 디버깅이 가능하다. 모든 에러를 박싱하면 로그에서 원인을 추적할 수 없다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 `ARCH`, `HAS_AXUM`, `HAS_TRACING` 등을 파악한다.

## 1. 미들웨어 종류 확인

사용자에게 추가할 미들웨어를 확인한다:
- **cors** — `CorsLayer` (tower-http)
- **logging** — `TraceLayer` (tower-http) + tracing
- **rate-limit** — 커스텀 레이어 또는 `governor` 크레이트
- **request-id** — `SetRequestIdLayer` (tower-http)
- **timeout** — `TimeoutLayer` (tower-http)
- 복수 선택 가능

## 2. 기존 미들웨어 스택 확인

라우터 설정 파일(`router.rs`, `main.rs` 등)을 읽어 이미 등록된 레이어를 파악한다. 새 레이어를 어느 위치에 삽입할지 결정한다.

## 3. 포트 정의 (외부 상태 의존 시)

rate limiting이나 캐시처럼 외부 저장소에 의존하는 미들웨어는 포트를 분리한다. 단순 CORS/logging/timeout은 포트 불필요.

### ARCH = workspace_service / hexagonal (rate limit 예시)

`crates/domain/src/ports/rate_limiter.rs`:

```rust
use async_trait::async_trait;
use crate::errors::DomainError;

#[async_trait]
pub trait RateLimiter: Send + Sync {
    /// key에 대한 요청을 허용하면 Ok(남은 횟수), 초과하면 Err 반환
    async fn check_rate(&self, key: &str) -> Result<u32, DomainError>;
    async fn reset(&self, key: &str) -> Result<(), DomainError>;
}
```

### ARCH = modular / flat

`src/domain/ports/rate_limiter.rs` (modular) 또는 `src/rate_limiter.rs` (flat)에 동일 trait 정의.

## 4. 어댑터 구현 (외부 상태 의존 시)

구체 구현은 infra 레이어에만 둔다.

### In-memory 어댑터 (단일 인스턴스용)

`crates/infra/src/adapters/rate_limiter.rs` (workspace_service) 또는 `src/infra/adapters/rate_limiter.rs` (modular):

```rust
use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;
use domain::ports::rate_limiter::RateLimiter;
use domain::errors::DomainError;

pub struct InMemoryRateLimiter {
    state: Arc<Mutex<HashMap<String, u32>>>,
    max_requests: u32,
}

impl InMemoryRateLimiter {
    pub fn new(max_requests: u32) -> Self {
        Self {
            state: Arc::new(Mutex::new(HashMap::new())),
            max_requests,
        }
    }
}

#[async_trait]
impl RateLimiter for InMemoryRateLimiter {
    async fn check_rate(&self, key: &str) -> Result<u32, DomainError> {
        let mut state = self.state.lock().await;
        let count = state.entry(key.to_string()).or_insert(0);
        if *count >= self.max_requests {
            return Err(DomainError::RateLimitExceeded);
        }
        *count += 1;
        Ok(self.max_requests - *count)
    }

    async fn reset(&self, key: &str) -> Result<(), DomainError> {
        self.state.lock().await.remove(key);
        Ok(())
    }
}
```

## 5. 미들웨어 생성 + `.layer()` 등록

선택된 종류별로 생성한다.

### CORS

```rust
// Cargo.toml: tower-http = { features = ["cors"] }
use tower_http::cors::{Any, CorsLayer};

let cors = CorsLayer::new()
    .allow_origin(Any)
    .allow_methods(Any)
    .allow_headers(Any);

// 라우터에 등록 (가장 바깥쪽 — 마지막 .layer())
let app = Router::new()
    // ... routes ...
    .layer(cors);
```

### Request Logging (TraceLayer)

```rust
// Cargo.toml: tower-http = { features = ["trace"] }
use tower_http::trace::TraceLayer;

let app = Router::new()
    // ... routes ...
    .layer(TraceLayer::new_for_http());
```

### Timeout

```rust
// Cargo.toml: tower-http = { features = ["timeout"] }
use tower_http::timeout::TimeoutLayer;
use std::time::Duration;

let app = Router::new()
    // ... routes ...
    .layer(TimeoutLayer::new(Duration::from_secs(30)));
```

### Request ID

```rust
// Cargo.toml: tower-http = { features = ["request-id"] }
use tower_http::request_id::{MakeRequestUuid, SetRequestIdLayer, PropagateRequestIdLayer};
use axum::http::HeaderName;

let x_request_id = HeaderName::from_static("x-request-id");

let app = Router::new()
    // ... routes ...
    .layer(PropagateRequestIdLayer::new(x_request_id.clone()))
    .layer(SetRequestIdLayer::new(x_request_id, MakeRequestUuid));
```

### 커스텀 미들웨어 (from_fn 패턴)

```rust
use axum::middleware;

async fn auth_middleware(
    State(auth): State<Arc<dyn AuthProvider>>,
    mut req: axum::extract::Request,
    next: axum::middleware::Next,
) -> Result<axum::response::Response, AppError> {
    // 토큰 검증 로직
    next.run(req).await
}

// 특정 라우터 그룹에만 적용
let protected = Router::new()
    .route("/me", get(me_handler))
    .layer(middleware::from_fn_with_state(state.clone(), auth_middleware));
```

## 6. 빌드 확인 안내

> `cargo build`를 실행하여 미들웨어 등록이 올바른지 확인하세요.
> tower-http features가 누락되면 컴파일 에러로 즉시 확인 가능합니다.

# After Creation

1. 생성/수정된 파일 목록을 출력한다.
2. 다음 단계를 안내한다:
   > - 레이어 순서 재확인: 인증 미들웨어는 라우터 내부, CORS는 가장 바깥
   > - 멀티 인스턴스 환경이면 rate limiter를 Redis 어댑터로 교체
   > - 미들웨어 테스트: `/rust-test`로 통합 테스트 생성

# References

- references/project-detection.md
