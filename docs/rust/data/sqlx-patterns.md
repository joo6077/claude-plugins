---
title: SQLx 패턴
version: 0.1.0
last_updated: 2026-04-07
---

# SQLx 패턴

`sqlx 0.8.x`는 컴파일 타임 SQL 검증을 지원하는 비동기 Rust DB 라이브러리다. 매크로 기반 쿼리(`query!`, `query_as!`)와 런타임 쿼리(`query`, `query_as`) 두 방식을 제공한다.

---

## 원칙

### 1. 정적 SQL은 `query_as!`, 동적 SQL은 `query_as`로 분리한다

`query_as!`는 컴파일 타임에 SQL과 Rust 타입을 검증한다. 동적으로 조건이 붙는 쿼리는 `QueryBuilder`나 `query_as::<_, T>()`를 사용한다.

```rust
// 컴파일 타임 검증 — 정적 쿼리
#[derive(Debug, FromRow)]
pub struct UserRow {
    pub id: Uuid,
    pub email: String,
    pub name: String,
    pub created_at: DateTime<Utc>,
}

pub async fn find_by_id(pool: &PgPool, id: Uuid) -> Result<Option<UserRow>, sqlx::Error> {
    sqlx::query_as!(
        UserRow,
        "SELECT id, email, name, created_at FROM users WHERE id = $1",
        id
    )
    .fetch_optional(pool)
    .await
}

// 런타임 동적 쿼리
pub async fn search_users(
    pool: &PgPool,
    email_like: Option<&str>,
) -> Result<Vec<UserRow>, sqlx::Error> {
    let mut qb = QueryBuilder::new("SELECT id, email, name, created_at FROM users WHERE 1=1");
    if let Some(email) = email_like {
        qb.push(" AND email ILIKE ").push_bind(format!("%{email}%"));
    }
    qb.build_query_as::<UserRow>().fetch_all(pool).await
}
```

### 2. `#[derive(FromRow)]`로 DB 컬럼을 Rust 구조체에 매핑한다

컬럼명이 필드명과 다를 때는 `#[sqlx(rename = "...")]`을 사용한다. `query_as!` 매크로는 `FromRow`를 무시하고 컬럼 순서로 매핑하므로 SELECT 컬럼 순서가 구조체 필드 순서와 일치해야 한다.

```rust
#[derive(Debug, Clone, FromRow)]
pub struct UserRow {
    pub id: Uuid,
    pub email: String,
    #[sqlx(rename = "display_name")]
    pub name: String,
    pub created_at: DateTime<Utc>,
    pub deleted_at: Option<DateTime<Utc>>,
}
```

### 3. 타입 매핑은 feature로 활성화한다

```toml
[dependencies]
sqlx = { version = "0.8", features = [
    "postgres",
    "runtime-tokio-native-tls",
    "uuid",       # Uuid 타입 지원
    "chrono",     # DateTime<Utc> 지원 (time 대신 chrono 선택)
    "json",       # serde_json::Value 지원
    "rust_decimal", # Decimal 타입 지원
] }
```

### 4. 트랜잭션은 `pool.begin()`으로 시작하고 명시적으로 commit한다

트랜잭션 객체를 drop하면 자동으로 rollback된다. 성공 경로에서 반드시 `commit()`을 호출해야 한다.

```rust
pub async fn transfer_credits(
    pool: &PgPool,
    from_id: Uuid,
    to_id: Uuid,
    amount: i64,
) -> Result<(), sqlx::Error> {
    let mut tx = pool.begin().await?;

    sqlx::query!(
        "UPDATE accounts SET credits = credits - $1 WHERE id = $2",
        amount, from_id
    )
    .execute(&mut *tx)
    .await?;

    sqlx::query!(
        "UPDATE accounts SET credits = credits + $1 WHERE id = $2",
        amount, to_id
    )
    .execute(&mut *tx)
    .await?;

    tx.commit().await?;
    Ok(())
}
```

### 5. 풀은 앱 시작 시 한 번 생성하고 `Arc`나 axum `State`로 공유한다

```rust
let pool = PgPoolOptions::new()
    .max_connections(20)
    .min_connections(2)
    .acquire_timeout(Duration::from_secs(5))
    .max_lifetime(Duration::from_secs(1800))
    .idle_timeout(Duration::from_secs(600))
    .connect(&database_url)
    .await?;
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| sqlx 버전 | 0.8.6 | PostgreSQL + tokio |
| 풀 max_connections | 10~20 | DB 서버 max_connections의 1/5 이하 |
| acquire_timeout | 5초 | 초과 시 즉시 에러 반환 |
| 오프라인 모드 디렉토리 | `.sqlx/` | `cargo sqlx prepare` 생성 |
| CI 검증 | `cargo sqlx prepare --check` | 스펙 드리프트 감지 |

---

## 안티패턴

### `query!` 매크로를 CI 없이 사용

`query!`는 실제 DB 연결이 있어야 컴파일된다. `SQLX_OFFLINE=true` 없이 CI에서 빌드하면 DB가 없으면 실패한다. `cargo sqlx prepare`로 `.sqlx/` 캐시를 생성하고 커밋한다.

### `fetch_all`로 무제한 행 조회

페이지네이션 없이 `fetch_all`을 사용하면 대용량 테이블에서 OOM이 발생한다. `LIMIT`와 커서 기반 페이지네이션을 함께 사용한다.

### 트랜잭션 내에서 다른 풀 연결 사용

트랜잭션 컨텍스트 밖의 쿼리는 트랜잭션에 참여하지 않는다. `&mut *tx`를 executor로 전달해야 같은 트랜잭션 안에서 실행된다.

---

## Gotchas

### `query_as!`에서 nullable 컬럼은 `Option<T>`로 받아야 한다

DB 컬럼이 nullable인데 Rust 타입이 `T`이면 컴파일 에러가 발생한다. `Option<T>`로 선언하거나 `SELECT COALESCE(col, default)`로 처리한다.

### `query!` 매크로에서 `$N` 바인딩은 1-indexed다

PostgreSQL의 파라미터 바인딩은 `$1`, `$2`로 시작한다. `?` (MySQL 스타일)는 사용하지 않는다.

### `cargo sqlx prepare`는 `DATABASE_URL` 환경변수가 필요하다

`.env` 파일이나 환경변수로 `DATABASE_URL`을 설정해야 한다. `cargo sqlx prepare --workspace`는 워크스페이스 전체 쿼리를 캐시한다.

### `tx.execute()`에 `&mut *tx` 패턴이 필요하다

`sqlx 0.8`에서 트랜잭션을 executor로 전달할 때 `&mut *tx`로 역참조해야 한다. `&tx`는 `Executor`를 구현하지 않는다.
