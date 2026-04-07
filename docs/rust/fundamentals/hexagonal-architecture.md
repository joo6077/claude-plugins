---
title: 헥사고날 아키텍처 (Ports & Adapters)
version: 0.1.0
last_updated: 2026-04-07
---

# 헥사고날 아키텍처 (Ports & Adapters)

Alistair Cockburn이 2005년 제안한 아키텍처 패턴. 애플리케이션을 외부 세계(UI, DB, 메시지 브로커, 외부 API)로부터 격리하는 것이 핵심 목표다. 외부 시스템이 교체되어도 도메인 로직은 변경되지 않는다. Rust에서는 `trait`이 Port, `impl`이 Adapter 역할을 한다.

---

## 원칙

### 1. 도메인은 인프라를 모른다 (의존 방향 규칙)

도메인 크레이트(`domain/`)는 어떤 DB, 브로커, HTTP 클라이언트도 `use`하지 않는다. 의존성 방향은 항상 **인프라 → 도메인** 단방향이다. 도메인은 Port(trait)만 정의하고, 인프라 크레이트가 Adapter(impl)를 제공한다. Cargo.toml 의존성으로 규칙이 강제된다 — 도메인 크레이트가 sqlx, reqwest를 import하면 컴파일 단계에서 확인된다.

> **출처:** [Alistair Cockburn — Hexagonal Architecture (2005)](https://alistair.cockburn.us/hexagonal-architecture/)

### 2. Port는 최소화된 trait으로 표현한다

Port는 도메인이 필요한 능력만 선언한다. "이 포트를 통해 사용자를 찾을 수 있다"는 계약이지, PostgreSQL 쿼리나 HTTP 엔드포인트 상세가 아니다. trait의 associated type, 제네릭, 파라미터가 인프라 타입(sqlx::Row, hyper::Response 등)을 포함하면 Port가 아니라 구현 상세가 Port에 누출된 것이다.

```rust
// 올바른 Port — 도메인 타입만 사용
#[async_trait]
pub trait DatabasePort: Send + Sync {
    async fn find_user(&self, id: UserId) -> Result<User, DomainError>;
    async fn save_user(&self, user: &User) -> Result<(), DomainError>;
}

// 잘못된 Port — 인프라 타입 노출
pub trait DatabasePort {
    async fn find_user(&self, id: i64) -> Result<sqlx::Row, sqlx::Error>; // ❌
}
```

> **출처:** [Alistair Cockburn — Hexagonal Architecture (2005)](https://alistair.cockburn.us/hexagonal-architecture/)

### 3. Adapter는 인프라를 Port로 변환한다

Adapter는 인프라 라이브러리(sqlx, aws-sdk, lapin 등)를 호출하고 결과를 도메인 타입으로 변환한다. 에러 변환(sqlx::Error → DomainError)도 Adapter 책임이다. 도메인 로직이 Adapter에 들어오면 Adapter가 아니라 서비스 레이어다.

```rust
pub struct PostgresUserAdapter {
    pool: sqlx::PgPool,
}

#[async_trait]
impl DatabasePort for PostgresUserAdapter {
    async fn find_user(&self, id: UserId) -> Result<User, DomainError> {
        let row = sqlx::query_as::<_, UserRow>("SELECT * FROM users WHERE id = $1")
            .bind(id.0)
            .fetch_one(&self.pool)
            .await
            .map_err(|e| DomainError::NotFound(e.to_string()))?;
        Ok(row.into())
    }

    async fn save_user(&self, user: &User) -> Result<(), DomainError> {
        sqlx::query("INSERT INTO users (id, email) VALUES ($1, $2)")
            .bind(user.id.0)
            .bind(&user.email)
            .execute(&self.pool)
            .await
            .map_err(|e| DomainError::Persistence(e.to_string()))?;
        Ok(())
    }
}
```

> **출처:** [Rust Book — Traits: Defining Shared Behavior](https://doc.rust-lang.org/book/ch10-02-traits.html)

### 4. 어댑터 교체는 제네릭 기반 vs `Box<dyn Port>` 중 선택한다

두 방식은 트레이드오프가 다르다.

**제네릭 기반 (정적 디스패치)**
```rust
pub struct UserService<D: DatabasePort> {
    db: D,
}

impl<D: DatabasePort> UserService<D> {
    pub async fn get_user(&self, id: UserId) -> Result<User, DomainError> {
        self.db.find_user(id).await
    }
}
```
장점: 컴파일 타임 최적화, vtable 없음, 단형화(monomorphization)로 인라인 가능. 단점: 타입 파라미터가 늘어날수록 제네릭 폭발이 발생한다.

**트레잇 객체 기반 (동적 디스패치)**
```rust
pub struct UserService {
    db: Arc<dyn DatabasePort>,
    storage: Arc<dyn StoragePort>,
    email: Arc<dyn EmailPort>,
}
```
장점: 포트가 많을 때 구조체가 단순해짐, DI 컨테이너와 연동 용이. 단점: vtable 간접 호출 비용, `Arc` 힙 할당.

**실용 기준:** 포트가 1~2개면 제네릭, 3개 이상이면 `Arc<dyn Port>` 혼용.

> **출처:** [Rust Book — Trait Objects](https://doc.rust-lang.org/book/ch17-02-trait-objects.html)

---

## 8개 포트 정의

### DatabasePort — 관계형 데이터베이스

PostgreSQL, MySQL, SQLite, Supabase를 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait DatabasePort: Send + Sync {
    async fn find_user(&self, id: UserId) -> Result<Option<User>, DomainError>;
    async fn save_user(&self, user: &User) -> Result<(), DomainError>;
    async fn delete_user(&self, id: UserId) -> Result<(), DomainError>;
    async fn list_users(&self, cursor: Option<Cursor>) -> Result<Page<User>, DomainError>;
}
```

어댑터 예시: `PostgresUserAdapter` (sqlx), `SupabaseUserAdapter` (postgrest-rs), `SqliteUserAdapter` (sqlx with SQLite feature).

### StoragePort — 오브젝트 스토리지

S3, GCS, MinIO, Cloudflare R2를 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait StoragePort: Send + Sync {
    async fn upload(&self, key: &str, data: Bytes, content_type: &str) -> Result<Url, DomainError>;
    async fn download(&self, key: &str) -> Result<Bytes, DomainError>;
    async fn delete(&self, key: &str) -> Result<(), DomainError>;
    async fn presigned_url(&self, key: &str, expires_in: Duration) -> Result<Url, DomainError>;
}
```

어댑터 예시: `S3StorageAdapter` (aws-sdk-s3), `MinioStorageAdapter` (aws-sdk-s3 with custom endpoint), `GcsStorageAdapter` (cloud-storage).

### MessagingPort — 메시지 큐/이벤트 스트리밍

RabbitMQ, Kafka, NATS를 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait MessagingPort: Send + Sync {
    async fn publish(&self, topic: &str, payload: &[u8]) -> Result<(), DomainError>;
    async fn subscribe(&self, topic: &str, handler: MessageHandler) -> Result<(), DomainError>;
    async fn ack(&self, msg_id: &str) -> Result<(), DomainError>;
}

pub type MessageHandler = Arc<dyn Fn(Vec<u8>) -> BoxFuture<'static, Result<(), DomainError>> + Send + Sync>;
```

어댑터 예시: `RabbitMqAdapter` (lapin), `KafkaAdapter` (rdkafka), `NatsAdapter` (async-nats).

### AuthPort — 인증/IdP

JWT 자체 발급, Supabase Auth, Auth0를 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait AuthPort: Send + Sync {
    async fn verify_token(&self, token: &str) -> Result<Claims, DomainError>;
    async fn issue_token(&self, subject: &str, roles: &[Role]) -> Result<String, DomainError>;
    async fn revoke_token(&self, token: &str) -> Result<(), DomainError>;
}
```

어댑터 예시: `JwtAdapter` (jsonwebtoken), `SupabaseAuthAdapter` (supabase-rs), `Auth0Adapter` (reqwest 기반).

### EmailPort — 이메일 발송

SMTP, Resend, AWS SES를 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait EmailPort: Send + Sync {
    async fn send(&self, to: &EmailAddress, subject: &str, body: EmailBody) -> Result<(), DomainError>;
    async fn send_bulk(&self, recipients: &[EmailAddress], subject: &str, body: EmailBody) -> Result<(), DomainError>;
}

pub enum EmailBody {
    Text(String),
    Html(String),
    Both { text: String, html: String },
}
```

어댑터 예시: `SmtpEmailAdapter` (lettre), `ResendEmailAdapter` (resend-rs), `SesEmailAdapter` (aws-sdk-ses).

### PaymentPort — 결제

Stripe, Paddle을 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait PaymentPort: Send + Sync {
    async fn create_checkout(&self, amount: Money, metadata: &PaymentMetadata) -> Result<CheckoutSession, DomainError>;
    async fn capture(&self, session_id: &str) -> Result<Payment, DomainError>;
    async fn refund(&self, payment_id: &str, amount: Option<Money>) -> Result<Refund, DomainError>;
    async fn verify_webhook(&self, payload: &[u8], signature: &str) -> Result<WebhookEvent, DomainError>;
}
```

어댑터 예시: `StripeAdapter` (async-stripe), `PaddleAdapter` (reqwest 기반).

### InferencePort — AI/ML 추론

OpenAI, Ollama, vLLM을 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait InferencePort: Send + Sync {
    async fn complete(&self, prompt: &str, options: CompletionOptions) -> Result<String, DomainError>;
    async fn complete_stream(&self, prompt: &str, options: CompletionOptions) -> Result<BoxStream<'static, Result<String, DomainError>>, DomainError>;
    async fn embed(&self, text: &str) -> Result<Vec<f32>, DomainError>;
}
```

어댑터 예시: `OpenAiAdapter` (async-openai), `OllamaAdapter` (ollama-rs), `VllmAdapter` (reqwest 기반 OpenAI 호환 API).

### JobPort — 백그라운드 작업

apalis, fang을 어댑터로 교체할 수 있다.

```rust
#[async_trait]
pub trait JobPort: Send + Sync {
    async fn enqueue<J: Job>(&self, job: J) -> Result<JobId, DomainError>;
    async fn enqueue_at<J: Job>(&self, job: J, at: DateTime<Utc>) -> Result<JobId, DomainError>;
    async fn cancel(&self, job_id: JobId) -> Result<(), DomainError>;
    async fn status(&self, job_id: JobId) -> Result<JobStatus, DomainError>;
}
```

어댑터 예시: `ApalisAdapter` (apalis), `FangAdapter` (fang).

---

## 프로젝트 구조

Cargo workspace 기준 권장 레이아웃:

```
my-app/
├── Cargo.toml                  # workspace
├── crates/
│   ├── domain/                 # 도메인 크레이트 — 외부 의존성 없음
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── entities/       # User, Order 등 도메인 모델
│   │       ├── ports/          # Port trait 정의
│   │       │   ├── database.rs
│   │       │   ├── storage.rs
│   │       │   ├── messaging.rs
│   │       │   ├── auth.rs
│   │       │   ├── email.rs
│   │       │   ├── payment.rs
│   │       │   ├── inference.rs
│   │       │   └── job.rs
│   │       ├── services/       # 도메인 서비스 (Port 주입)
│   │       └── errors.rs       # DomainError 정의
│   ├── adapters/               # 어댑터 크레이트 (domain만 의존)
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── postgres/       # PostgresUserAdapter 등
│   │       ├── s3/             # S3StorageAdapter
│   │       ├── rabbitmq/       # RabbitMqAdapter
│   │       ├── stripe/         # StripeAdapter
│   │       ├── openai/         # OpenAiAdapter
│   │       └── ...
│   ├── api/                    # HTTP 레이어 (axum, actix-web)
│   │   └── src/
│   │       └── ...             # domain + adapters 의존
│   └── app/                    # 진입점, DI 조립
│       └── src/
│           └── main.rs         # Adapter 인스턴스화 + Service 조립
```

**Cargo.toml 의존 관계:**
```toml
# domain/Cargo.toml — 외부 인프라 크레이트 없음
[dependencies]
async-trait = "0.1"
thiserror = "2"
uuid = { version = "1", features = ["v4"] }

# adapters/Cargo.toml
[dependencies]
domain = { path = "../domain" }
sqlx = { version = "0.8", features = ["postgres", "runtime-tokio-native-tls"] }
aws-sdk-s3 = "1"
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| `Box<dyn Port>` vs 제네릭 전환 기준 | 포트 3개 이상 | 제네릭 폭발 방지 |
| async_trait 오버헤드 | ~5ns/call | vtable + Box<Future> 할당. hot path 회피 |
| `Arc<dyn Port>` 비용 | ~2ns/clone | atomic ref count. 대부분 무시 가능 |
| 포트당 메서드 수 권장 | 3~7개 | 그 이상이면 포트 분리를 검토 |
| 어댑터당 크레이트 기준 | 인프라 기술 1개 | S3 + GCS를 하나의 어댑터 크레이트에 묶어도 무방 |

---

## 안티패턴

### 포트에 인프라 타입 노출

`DatabasePort`가 `sqlx::PgPool`이나 `sqlx::Error`를 반환하면 포트를 구현하는 모든 어댑터가 sqlx에 의존해야 한다. 포트는 도메인 타입만 사용해야 한다.

### 과도한 포트 분리

CRUD 엔티티마다 포트를 별도로 만들면 (`UserDatabasePort`, `OrderDatabasePort`, `ProductDatabasePort`) DI 조립 코드가 폭발한다. 연관된 엔티티를 하나의 `DatabasePort`로 묶거나, Repository 패턴과 조합하여 `UserRepository`, `OrderRepository`를 각각의 포트 impl로 정의한다.

### Adapter에 도메인 로직 삽입

`PostgresUserAdapter::save_user`에서 이메일 유효성 검사나 비즈니스 규칙을 실행하면 도메인 로직이 인프라에 분산된다. Adapter는 변환(translation)만 담당한다.

### 테스트에 실제 인프라 사용

Port trait이 있으면 테스트에서 `MockDatabasePort`를 주입할 수 있다. 단위 테스트에서 PostgreSQL 컨테이너를 띄우는 것은 Port 추상화를 쓰지 않았다는 신호다. 통합 테스트에서만 실제 어댑터를 사용한다.

### 단일 구현에 헥사고날 적용

어댑터를 교체할 계획이 없고 팀이 소규모라면 헥사고날 아키텍처는 과도한 복잡성이다. 서비스 규모와 팀 구조에 맞는 아키텍처를 선택한다.

---

## Gotchas

### async_trait 매크로는 `Box<dyn Future>`를 생성한다

`#[async_trait]`는 async fn을 `fn(...) -> BoxFuture<'_, Result<...>>`로 변환한다. 매 호출마다 힙 할당이 발생한다. hot path(초당 수천 호출)에서는 async_trait 없이 `Pin<Box<dyn Future>>` 또는 `impl Future`를 직접 사용하거나, RPITIT(Return Position Impl Trait in Trait, Rust 1.75+)로 대체할 수 있다.

```rust
// Rust 1.75+ — async_trait 없이 async fn in trait 가능
pub trait DatabasePort: Send + Sync {
    fn find_user(&self, id: UserId) -> impl Future<Output = Result<Option<User>, DomainError>> + Send;
}
```

> **출처:** [Rust Blog — AFIT Stabilization (1.75)](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits.html)

### `dyn Trait`은 Send + Sync 명시가 필요하다

`Arc<dyn DatabasePort>` 또는 `Box<dyn DatabasePort>`가 `Send + Sync`를 요구하면 trait 정의에도 `: Send + Sync` 수퍼트레잇이 있어야 한다. tokio 런타임에서 task를 spawn할 때 `Send`가 없으면 컴파일 에러가 발생한다.

```rust
pub trait DatabasePort: Send + Sync { ... } // ✅
pub trait DatabasePort { ... }              // ❌ Arc<dyn DatabasePort>가 Send 아님
```

### 제네릭 폭발 (monomorphization explosion)

`UserService<D: DatabasePort, S: StoragePort, M: MessagingPort, A: AuthPort>`처럼 타입 파라미터가 4개 이상이면 컴파일 시간이 증가하고 바이너리 크기가 커진다. 포트가 3개 이상이면 `Arc<dyn Port>`로 전환하거나, `ServiceDeps` 구조체로 묶어 전달한다.

```rust
// 제네릭 폭발 방지 — 의존성 묶음
pub struct ServiceDeps {
    pub db: Arc<dyn DatabasePort>,
    pub storage: Arc<dyn StoragePort>,
    pub email: Arc<dyn EmailPort>,
}
```

### 어댑터 초기화 에러를 main에서 처리한다

어댑터 생성(`PgPool::connect`, AWS SDK 설정 등)은 실패할 수 있다. `main.rs`에서 모든 어댑터를 초기화하고, 실패 시 즉시 종료한다. 서비스 레이어에서 어댑터를 lazy init하면 에러를 늦게 발견한다.

```rust
// app/src/main.rs
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let pool = PgPool::connect(&env::var("DATABASE_URL")?).await?;
    let db: Arc<dyn DatabasePort> = Arc::new(PostgresUserAdapter::new(pool));
    let service = UserService::new(db);
    // ...
    Ok(())
}
```

### MockAdapter는 테스트 크레이트에만 둔다

`MockDatabasePort`를 `domain` 또는 `adapters` 크레이트의 프로덕션 코드에 포함하면 바이너리에 테스트 코드가 배포된다. `#[cfg(test)]` 또는 별도 `test-helpers` 크레이트로 분리한다.
