---
title: 관측성 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 관측성 원칙

`tracing`으로 구조화 로깅과 스팬을 생성하고, `tracing-opentelemetry`로 OTLP 트레이싱을 내보내며, `metrics-exporter-prometheus`로 Prometheus 메트릭을 노출한다.

---

## 원칙

### 1. `tracing-subscriber`로 구조화 JSON 로깅을 설정한다

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
tracing-opentelemetry = "0.32"
opentelemetry = "0.28"
opentelemetry_sdk = { version = "0.28", features = ["rt-tokio"] }
opentelemetry-otlp = { version = "0.28", features = ["tonic"] }
metrics = "0.24"
metrics-exporter-prometheus = "0.18"
```

```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

pub fn init_tracing() -> anyhow::Result<()> {
    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    let fmt_layer = tracing_subscriber::fmt::layer()
        .json()                    // 구조화 JSON 출력
        .with_target(true)
        .with_thread_ids(false)
        .with_file(false);

    tracing_subscriber::registry()
        .with(env_filter)
        .with(fmt_layer)
        .init();

    Ok(())
}
```

### 2. `tracing-opentelemetry`로 OTLP 트레이싱을 내보낸다

```rust
use opentelemetry_otlp::SpanExporter;
use opentelemetry_sdk::{runtime, trace::SdkTracerProvider};
use tracing_opentelemetry::OpenTelemetryLayer;

pub fn init_tracing_with_otel(service_name: &str) -> anyhow::Result<SdkTracerProvider> {
    let exporter = SpanExporter::builder()
        .with_tonic()
        .build()?;

    let provider = SdkTracerProvider::builder()
        .with_batch_exporter(exporter, runtime::Tokio)
        .build();

    let tracer = provider.tracer(service_name.to_string());

    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    let fmt_layer = tracing_subscriber::fmt::layer().json();
    let otel_layer = OpenTelemetryLayer::new(tracer);

    tracing_subscriber::registry()
        .with(env_filter)
        .with(fmt_layer)
        .with(otel_layer)
        .init();

    Ok(provider)
}
```

### 3. `#[instrument]`로 함수를 자동으로 스팬으로 계측한다

```rust
use tracing::{instrument, info, warn, error, Span};

#[instrument(skip(pool), fields(user_id = %id))]
pub async fn get_user(pool: &PgPool, id: Uuid) -> Result<User, AppError> {
    info!("Fetching user");

    let user = sqlx::query_as!(UserRow, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(pool)
        .await
        .map_err(|e| {
            error!(error = %e, "Database query failed");
            AppError::Database(e)
        })?
        .ok_or_else(|| {
            warn!("User not found");
            AppError::NotFound
        })?;

    // 현재 스팬에 동적 필드 추가
    Span::current().record("email", &user.email.as_str());

    Ok(user.into())
}
```

### 4. `metrics-exporter-prometheus`로 Prometheus 메트릭을 노출한다

```rust
use metrics::{counter, gauge, histogram};
use metrics_exporter_prometheus::PrometheusBuilder;

pub fn init_metrics() -> anyhow::Result<()> {
    PrometheusBuilder::new()
        .with_http_listener(([0, 0, 0, 0], 9090))  // /metrics 엔드포인트
        .install()?;
    Ok(())
}

// 사용
pub async fn handle_request(/* ... */) {
    counter!("http_requests_total", "method" => "POST", "path" => "/users").increment(1);

    let start = std::time::Instant::now();
    let result = process_request().await;
    histogram!("http_request_duration_seconds", "path" => "/users")
        .record(start.elapsed().as_secs_f64());

    if result.is_err() {
        counter!("http_errors_total", "path" => "/users").increment(1);
    }
}

// 현재 활성 연결 수 게이지
gauge!("active_connections").set(active_count as f64);
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| tracing-subscriber 버전 | 0.3.x | `env-filter`, `json` feature |
| tracing-opentelemetry 버전 | 0.32.x | opentelemetry 0.28과 호환 |
| metrics-exporter-prometheus 버전 | 0.18.x | metrics 0.24와 호환 |
| Prometheus 포트 | 9090 | 앱 포트(8080)와 분리 |
| OTLP 기본 포트 | 4317 (gRPC) | `OTEL_EXPORTER_OTLP_ENDPOINT` 환경변수 |

---

## 안티패턴

### `println!`/`eprintln!` 대신 `tracing` 미사용

구조화되지 않은 출력은 로그 집계 시스템에서 파싱하기 어렵다. 모든 로그는 `tracing::{info!, warn!, error!}` 매크로를 사용한다.

### 스팬 없이 분산 트레이싱 설정

OTLP exporter를 설정해도 코드에 `#[instrument]`나 `span!`이 없으면 트레이스가 생성되지 않는다. 핵심 서비스 함수에 `#[instrument]`를 붙인다.

### 메트릭 레이블 카디널리티 폭발

`"user_id" => user_id`처럼 높은 카디널리티 값을 레이블로 사용하면 Prometheus 메모리가 폭발한다. 레이블 값은 열거형 수준(method, status_code, path 패턴 등)으로 제한한다.

### `SdkTracerProvider`를 drop하면 스팬이 유실된다

앱 종료 시 배치 exporter가 버퍼에 있는 스팬을 flush하기 전에 drop되면 데이터가 유실된다. `provider.shutdown()`을 `main` 종료 전에 호출한다.

---

## Gotchas

### `tracing-opentelemetry`와 `opentelemetry_sdk` 버전을 정확히 맞춰야 한다

`tracing-opentelemetry 0.32`는 `opentelemetry 0.28`과 호환된다. 버전이 맞지 않으면 trait 구현 불일치 컴파일 에러가 발생한다. `Cargo.toml`에서 버전을 명시적으로 고정한다.

### `RUST_LOG` 환경변수로 런타임에 로그 레벨을 제어한다

```bash
RUST_LOG=info,my_crate=debug,sqlx=warn
```

`EnvFilter::try_from_default_env()`가 이 환경변수를 자동으로 읽는다.

### `#[instrument(skip(...))]`로 민감한 파라미터를 스팬에서 제외한다

`#[instrument]`는 기본적으로 모든 파라미터를 스팬 필드로 기록한다. 비밀번호, 토큰 같은 민감한 값은 `skip(password, token)`으로 제외한다.

### `tower-http`의 `TraceLayer`와 `#[instrument]`는 독립적이다

`TraceLayer`는 HTTP 요청/응답 스팬을 자동으로 생성한다. `#[instrument]`는 서비스 함수 스팬을 생성한다. 두 스팬은 자동으로 부모-자식 관계로 연결된다.
