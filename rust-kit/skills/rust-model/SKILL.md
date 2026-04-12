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

- **SQLx와 SeaORM 중 프로젝트가 이미 사용하는 ORM을 먼저 감지** — 둘을 한 프로젝트에 섞지 마라. `HAS_SEAORM`이면 SeaORM 경로, `HAS_SQLX` only면 SQLx 경로를 따른다. 둘 다 있는 "hybrid"는 fit-pal 같은 대형 프로젝트에서도 안티패턴이다.
- **SQLx 매크로 컴파일 타임 검증** — `sqlx::query!`/`query_as!` 매크로는 컴파일 타임에 DB에 연결해 쿼리를 검증한다. `DATABASE_URL` 환경변수 또는 `.env` 파일이 없으면 컴파일 자체가 실패한다. 오프라인 CI를 위해서는 `cargo sqlx prepare`로 `.sqlx/` 디렉토리를 미리 생성해야 한다. (`sqlx-data.json`은 구버전 패턴이다 — 현재 0.8은 `.sqlx/` 디렉토리를 사용한다.)
- **SQLx 0.8 오프라인 모드** — `SQLX_OFFLINE=true`는 `.sqlx/` 디렉토리가 존재하고 최신 상태일 때만 동작한다. 쿼리를 수정한 후에는 반드시 `cargo sqlx prepare`를 다시 실행해야 한다. runtime feature는 `runtime-tokio` + `tls-rustls` 조합을 권장 (`runtime-tokio-rustls`는 alias).
- **SeaORM 1.1 ActiveModel/Entity 분리** — SeaORM은 `Entity`(쿼리 진입점) + `Model`(read DTO) + `ActiveModel`(insert/update용 opt field wrapper)을 분리한다. 포트 trait에는 이 타입들을 노출하지 말고 순수 도메인 모델로 DTO를 주고받아라.
- **SeaORM `ConnectionTrait` 제네릭** — 트랜잭션과 일반 커넥션을 동시에 지원하려면 내부 메서드 시그니처를 `<C: ConnectionTrait>(conn: &C, ...)` 형태로 받는다. 이렇게 해야 `&DatabaseConnection`과 `&DatabaseTransaction` 모두 전달 가능하다. 출처: fit-pal `server/CLAUDE.md` §테스트 가능성.
- **마이그레이션 타임스탬프 중복 금지** — 파일명 타임스탬프(`YYYYMMDDHHMMSS`)가 겹치면 SQLx/SeaORM 양쪽 모두 에러를 낸다. 항상 현재 시각을 사용하고 같은 초에 여러 파일을 만들지 마라.
- **nullable 컬럼은 `Option<T>` 필수** — DB가 `NOT NULL`인데 Rust 필드를 `Option<T>`로 하면 조회 시 항상 Some(..)이지만 타입 안전성이 떨어진다. 반대로 nullable 컬럼을 `T`로 하면 `null` 조회 시 SQLx는 `Error::ColumnDecode`, SeaORM은 `DbErr::AttrNotSet`이 발생한다.
- **마이그레이션 파일은 한 번 적용되면 수정 금지** — 이미 prod/staging에 적용된 마이그레이션을 수정하면 체크섬 불일치로 전체 마이그레이션이 실패한다. 수정이 필요하면 새 마이그레이션 파일을 추가하여 `ALTER TABLE`로 변경해라.
- **인덱스 네이밍 컨벤션** — `idx_{table}_{columns}` 형식을 따라라(예: `idx_users_email`). 복합 인덱스는 `idx_orders_user_id_created_at`. 이름 없이 생성하면 DB가 자동 생성하는 이름이 DB 벤더마다 달라 마이그레이션 이식성이 깨진다.
- **`DEFAULT` 값이 있는 컬럼 추가 시 `NOT NULL` 안전하게 적용** — 기존 테이블에 `NOT NULL` 컬럼을 추가하려면 반드시 `DEFAULT` 값을 함께 지정해라. `DEFAULT` 없이 `NOT NULL`을 추가하면 기존 행이 제약 위반으로 마이그레이션 자체가 실패한다.

# DB 모델 + 마이그레이션 생성 (SQLx 또는 SeaORM)

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `$PACKAGE`, `ARCH`, `IS_WORKSPACE`, `HAS_SQLX`, `HAS_SEAORM`, `HAS_SERDE`)를 사용한다.

## 0a. ORM 경로 분기

| 감지 | 경로 |
|------|------|
| `HAS_SEAORM` = true | **SeaORM 1.1 경로** (§5S: ActiveModel/Entity + sea-orm-migration) — fit-pal 실무 패턴 |
| `HAS_SQLX` = true, `HAS_SEAORM` = false | **SQLx 0.8 경로** (§5X: query_as! + sqlx migrate) |
| 둘 다 false | 사용자에게 선택 요청 후 의존성 추가 안내 |
| 둘 다 true | 사용자에게 단일화 권고 (hybrid는 관리 부담이 크다) |

**SQLx 0.8 추가 명령**:

```bash
cargo add sqlx --features postgres,runtime-tokio,tls-rustls,macros,migrate,uuid,chrono
```

**SeaORM 1.1 추가 명령**:

```bash
cargo add sea-orm --features sqlx-postgres,runtime-tokio-rustls,macros,with-chrono,with-uuid,with-json,mock
cargo add sea-orm-migration --features sqlx-postgres,runtime-tokio-rustls
```

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

## 4. 어댑터 구현 (SQLx §4X 또는 SeaORM §4S)

`infra/adapters/` (또는 `ARCH = modular`이면 `src/infra/adapters/`)에 Repository impl을 생성한다.

- DB 라이브러리 의존은 이 레이어에만 존재한다. `domain/` 크레이트에서 sqlx/sea-orm을 직접 import하지 않는다.
- **소비자 소유 포트 원칙**: 포트 trait 시그니처에 DB 타입을 노출하지 말고 DTO/도메인 모델만 반환한다.

### §4X — SQLx 어댑터

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

### §4S — SeaORM 어댑터

SeaORM은 Entity/Model/ActiveModel 3종을 `sea-orm-codegen` 또는 `sea-orm-cli generate entity`로 생성한다. 아래는 수동 작성 시 패턴:

```rust
// infra/entities/user.rs — DeriveEntityModel로 생성 (보통 sea-orm-cli로 자동 생성)
use sea_orm::entity::prelude::*;
use chrono::{DateTime, Utc};

#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i64,
    pub name: String,
    #[sea_orm(unique)]
    pub email: String,
    pub created_at: DateTime<Utc>,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

Repository adapter는 **`ConnectionTrait` 제네릭**으로 내부 메서드를 작성한다. 이렇게 해야 일반 커넥션과 트랜잭션을 모두 지원한다 (fit-pal 실무 패턴):

```rust
// infra/adapters/user_repository_sea.rs
use async_trait::async_trait;
use sea_orm::{
    ActiveModelTrait, ColumnTrait, ConnectionTrait, DatabaseConnection,
    EntityTrait, QueryFilter, Set,
};
use std::sync::Arc;

use crate::domain::models::User;
use crate::domain::ports::UserRepository;
use crate::domain::errors::DomainError;
use super::entities::user::{self, ActiveModel, Entity as UserEntity};

pub struct SeaUserRepository {
    db: Arc<DatabaseConnection>,
}

impl SeaUserRepository {
    pub fn new(db: Arc<DatabaseConnection>) -> Self {
        Self { db }
    }

    // 내부 헬퍼는 ConnectionTrait 제네릭 — 트랜잭션/일반 커넥션 모두 지원
    async fn find_by_id_inner<C: ConnectionTrait>(
        conn: &C,
        id: i64,
    ) -> Result<Option<User>, DomainError> {
        let row = UserEntity::find_by_id(id)
            .one(conn)
            .await
            .map_err(|e| DomainError::Internal(anyhow::anyhow!(e)))?;
        Ok(row.map(Self::model_to_domain))
    }

    fn model_to_domain(m: user::Model) -> User {
        User {
            id: m.id,
            name: m.name,
            email: m.email,
            created_at: m.created_at,
        }
    }
}

#[async_trait]
impl UserRepository for SeaUserRepository {
    async fn find_by_id(&self, id: i64) -> Result<Option<User>, DomainError> {
        Self::find_by_id_inner(self.db.as_ref(), id).await
    }

    async fn create(&self, name: &str, email: &str) -> Result<User, DomainError> {
        let active = ActiveModel {
            name: Set(name.to_string()),
            email: Set(email.to_string()),
            created_at: Set(chrono::Utc::now()),
            ..Default::default()
        };
        let m = active
            .insert(self.db.as_ref())
            .await
            .map_err(|e| DomainError::Internal(anyhow::anyhow!(e)))?;
        Ok(Self::model_to_domain(m))
    }

    async fn delete(&self, id: i64) -> Result<(), DomainError> {
        UserEntity::delete_by_id(id)
            .exec(self.db.as_ref())
            .await
            .map_err(|e| DomainError::Internal(anyhow::anyhow!(e)))?;
        Ok(())
    }
}
```

> `sea_orm::DbErr`, `DatabaseConnection`, `DatabaseTransaction` 등 SeaORM 구체 타입은 **포트 시그니처에 노출 금지**. adapter 내부에서만 사용하고 `DomainError`로 변환하여 반환한다.

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

## 6. 마이그레이션 생성

### §6X — SQLx 마이그레이션 (SQL 파일)

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

### §6S — SeaORM 마이그레이션 (Rust 코드)

SeaORM은 마이그레이션을 **Rust 코드**로 작성한다. 별도 `migration/` 크레이트에 배치한다:

```rust
// migration/src/m20260407_120000_create_users.rs
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Users::Table)
                    .if_not_exists()
                    .col(ColumnDef::new(Users::Id).big_integer().not_null().auto_increment().primary_key())
                    .col(ColumnDef::new(Users::Name).string().not_null())
                    .col(ColumnDef::new(Users::Email).string().not_null().unique_key())
                    .col(ColumnDef::new(Users::CreatedAt).timestamp_with_time_zone().not_null().default(Expr::current_timestamp()))
                    .to_owned(),
            )
            .await?;

        manager
            .create_index(
                Index::create()
                    .name("idx_users_email")
                    .table(Users::Table)
                    .col(Users::Email)
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.drop_table(Table::drop().table(Users::Table).to_owned()).await
    }
}

#[derive(DeriveIden)]
enum Users {
    Table,
    Id,
    Name,
    Email,
    CreatedAt,
}
```

`migration/src/lib.rs`의 `Migrator::migrations()` 배열에 새 `Migration` 모듈을 등록한다.

---

## 7. 마이그레이션 실행 안내

### §7X — SQLx

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

### §7S — SeaORM

SeaORM은 두 가지 실행 방식을 제공한다:

**방식 1: CLI (개발 시)**
```bash
# sea-orm-cli 설치 (최초 1회)
cargo install sea-orm-cli --locked

# 마이그레이션 생성 골격 (파일만 만들고 up/down은 직접 작성)
DATABASE_URL=postgres://... sea-orm-cli migrate generate create_users -d migration

# 실행
DATABASE_URL=postgres://... sea-orm-cli migrate up -d migration

# 롤백
DATABASE_URL=postgres://... sea-orm-cli migrate down -d migration
```

**방식 2: 런타임 마이그레이션 (실무 표준 — fit-pal 패턴)**
```rust
// apps/api/src/main.rs 또는 별도 fitpal-migration 바이너리
use sea_orm_migration::MigratorTrait;
use migration::Migrator;
use sea_orm::Database;

let db = Database::connect(std::env::var("DATABASE_URL")?).await?;
Migrator::up(&db, None).await?;
```

Docker 이미지에 `cargo install sea-orm-cli`를 포함시키지 않고 앱 시작 시 자동 마이그레이션이 가능해 배포가 간편하다.

## After Creation

1. 생성/수정된 파일 목록 출력.
2. `mod.rs` 등록이 누락된 파일이 없는지 확인한다.
3. 다음 단계 안내:
   - Repository를 활용하는 서비스 레이어가 필요하면 `rust-service` 스킬을 사용하세요.
   - API 핸들러를 바로 연결하려면 `rust-api` 스킬을 사용하세요.

# References

- references/project-detection.md
- templates/rust-model.rs.template — SQLx 모델 템플릿
