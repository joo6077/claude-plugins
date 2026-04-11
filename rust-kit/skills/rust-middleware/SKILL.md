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

# Process

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
