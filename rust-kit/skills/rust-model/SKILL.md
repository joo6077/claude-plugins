---
name: rust-model
description: >
  SQLx 모델 구조체와 마이그레이션 SQL을 생성한다.
  Hexagonal Architecture 기반으로 Repository trait(포트) 정의 → SQLx impl(어댑터) 구현 순서로 생성한다.
  "모델 만들어줘", "테이블 추가", "마이그레이션 생성", "DB 모델", "rust model" 같은 요청 시 사용한다.
argument-hint: "<table_name> [field:type ...]"
user-invocable: true
---

## Gotchas

- `sqlx::query!`/`query_as!` 매크로는 컴파일 타임에 DB에 연결해 쿼리를 검증한다. `DATABASE_URL` 환경변수 또는 `.env` 파일이 없으면 컴파일 자체가 실패한다. 오프라인 CI를 위해서는 `cargo sqlx prepare`로 `.sqlx/` 디렉토리를 미리 생성해야 한다. (`sqlx-data.json`은 구버전 패턴이다 — 현재 0.8은 `.sqlx/` 디렉토리를 사용한다.)
- 오프라인 모드(`SQLX_OFFLINE=true`)는 `.sqlx/` 디렉토리가 존재하고 최신 상태일 때만 동작한다. 쿼리를 수정한 후에는 반드시 `cargo sqlx prepare`를 다시 실행해야 한다.
- 마이그레이션 파일 이름의 타임스탬프가 겹치면 sqlx가 에러를 낸다. 파일 생성 시 항상 현재 시각(YYYYMMDDHHMMSS)을 사용하고, 같은 초에 여러 파일을 만들지 마라.
- nullable 컬럼은 반드시 `Option<T>`로 매핑한다. DB가 `NOT NULL`인데 Rust 필드를 `Option<T>`로 하면 런타임 패닉이 발생하고, 반대로 nullable 컬럼을 `T`로 하면 `null` 조회 시 패닉이 난다.

# SQLx 모델 + 마이그레이션 생성

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `$PACKAGE`, `ARCH`, `IS_WORKSPACE`, `HAS_SQLX`, `HAS_SERDE`)를 사용한다.

`HAS_SQLX`가 false이면 중단하고 사용자에게 알린다:
> `Cargo.toml`에 `sqlx` 의존성이 없습니다. `cargo add sqlx --features postgres,runtime-tokio,macros,migrate`로 추가하세요.

---

## 1. 입력 확인

`$ARGUMENTS`에서 파싱하거나 사용자에게 확인한다:

| 항목 | 예시 |
|------|------|
| 테이블 이름 | `users` |
| 컬럼 목록 | `id: BIGSERIAL PK`, `name: TEXT NOT NULL`, `email: TEXT NOT NULL UNIQUE`, `created_at: TIMESTAMPTZ DEFAULT NOW()` |
| 관계 | 외래키 여부, `ON DELETE` 정책 |
| CRUD 범위 | 전체 / 특정 메서드만 (list, get, create, update, delete) |

---

## 2. 기존 모델 패턴 읽기

모델을 생성하기 전에 기존 모델 파일을 읽어 프로젝트 컨벤션을 파악한다:

- 구조체 위치 (`domain/models/`, `src/domain/models/` 등)
- ID 타입 (`i64`, `Uuid` 등)
- 타임스탬프 타입 (`chrono::DateTime<Utc>`, `time::OffsetDateTime` 등)
- 에러 타입 (`DomainError`, `AppError`, `sqlx::Error` 그대로 사용 여부)
- 기존 Repository trait 패턴

---

## 3. 포트 정의

`domain/ports/` (또는 `ARCH = modular`이면 `src/domain/ports/`)에 Repository trait을 정의한다.

- `PgPool`, `sqlx::Error` 등 SQLx 구체 타입을 trait 시그니처에 노출하지 않는다.
- 이미 해당 모델의 Repository trait이 있으면 메서드만 추가한다.

```rust
// domain/ports/user_repository.rs
use async_trait::async_trait;
use crate::domain::models::User;
use crate::domain::errors::DomainError;

#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: i64) -> Result<Option<User>, DomainError>;
    async fn find_all(&self) -> Result<Vec<User>, DomainError>;
    async fn create(&self, name: &str, email: &str) -> Result<User, DomainError>;
    async fn update(&self, id: i64, name: &str) -> Result<User, DomainError>;
    async fn delete(&self, id: i64) -> Result<(), DomainError>;
}
```

`mod.rs`에 `pub mod user_repository;`를 추가한다.

---

## 4. SQLx 어댑터 구현

`infra/adapters/` (또는 `ARCH = modular`이면 `src/infra/adapters/`)에 SQLx 기반 Repository impl을 생성한다.

- `sqlx` 의존은 이 레이어에만 존재한다. `domain/` 크레이트에서 sqlx를 직접 import하지 않는다.
- `query_as!` 매크로는 컴파일 타임 검증이 되므로 기본으로 사용한다. 동적 쿼리가 필요하면 `query_as::<_, T>(sql).bind(...)` 패턴을 사용한다.

```rust
// infra/adapters/user_repository_impl.rs
use async_trait::async_trait;
use sqlx::PgPool;
use crate::domain::models::User;
use crate::domain::ports::UserRepository;
use crate::domain::errors::DomainError;

pub struct PgUserRepository {
    pool: PgPool,
}

impl PgUserRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl UserRepository for PgUserRepository {
    async fn find_by_id(&self, id: i64) -> Result<Option<User>, DomainError> {
        let user = sqlx::query_as!(
            User,
            r#"SELECT id, name, email, created_at FROM users WHERE id = $1"#,
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(DomainError::from)?;
        Ok(user)
    }

    async fn find_all(&self) -> Result<Vec<User>, DomainError> {
        let users = sqlx::query_as!(
            User,
            r#"SELECT id, name, email, created_at FROM users ORDER BY id"#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(DomainError::from)?;
        Ok(users)
    }

    async fn create(&self, name: &str, email: &str) -> Result<User, DomainError> {
        let user = sqlx::query_as!(
            User,
            r#"
            INSERT INTO users (name, email)
            VALUES ($1, $2)
            RETURNING id, name, email, created_at
            "#,
            name,
            email
        )
        .fetch_one(&self.pool)
        .await
        .map_err(DomainError::from)?;
        Ok(user)
    }

    async fn update(&self, id: i64, name: &str) -> Result<User, DomainError> {
        let user = sqlx::query_as!(
            User,
            r#"
            UPDATE users SET name = $2
            WHERE id = $1
            RETURNING id, name, email, created_at
            "#,
            id,
            name
        )
        .fetch_one(&self.pool)
        .await
        .map_err(DomainError::from)?;
        Ok(user)
    }

    async fn delete(&self, id: i64) -> Result<(), DomainError> {
        sqlx::query!(r#"DELETE FROM users WHERE id = $1"#, id)
            .execute(&self.pool)
            .await
            .map_err(DomainError::from)?;
        Ok(())
    }
}
```

---

## 5. 도메인 모델 구조체 생성

`domain/models/` (또는 `src/domain/models/`)에 구조체를 생성한다.

```rust
// domain/models/user.rs
use chrono::{DateTime, Utc};

#[derive(Debug, Clone)]
pub struct User {
    pub id: i64,
    pub name: String,
    pub email: String,
    pub created_at: DateTime<Utc>,
}
```

`HAS_SERDE`이면 `#[derive(serde::Serialize, serde::Deserialize)]`를 추가한다.

`mod.rs`에 `pub mod user;`를 추가한다.

---

## 6. 마이그레이션 SQL 생성

`migrations/` 디렉토리에 타임스탬프 기반 파일명으로 생성한다. 현재 시각(YYYYMMDDHHMMSS)을 사용한다.

```sql
-- migrations/20260407120000_create_users.sql
CREATE TABLE users (
    id         BIGSERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users (email);
```

---

## 7. 마이그레이션 실행 안내

생성 완료 후 다음을 안내한다:

**마이그레이션 실행:**
```bash
cargo sqlx migrate run
```

**오프라인 모드용 메타데이터 생성 (CI 빌드용):**
```bash
DATABASE_URL=postgres://... cargo sqlx prepare
# 또는 workspace 전체:
DATABASE_URL=postgres://... cargo sqlx prepare --workspace
```

생성된 `.sqlx/` 디렉토리를 git에 커밋한다. CI에서 `SQLX_OFFLINE=true`로 빌드하면 DB 연결 없이 컴파일된다.

## After Creation

1. 생성/수정된 파일 목록 출력.
2. `mod.rs` 등록이 누락된 파일이 없는지 확인한다.
3. 다음 단계 안내:
   - Repository를 활용하는 서비스 레이어가 필요하면 `rust-service` 스킬을 사용하세요.
   - API 핸들러를 바로 연결하려면 `rust-api` 스킬을 사용하세요.
