---
title: 마이그레이션 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 마이그레이션 원칙

`sqlx migrate`는 SQL 파일 기반의 데이터베이스 마이그레이션 도구다. `sqlx::migrate!()` 매크로로 앱 시작 시 자동 실행하거나 `sqlx-cli`로 수동 관리한다.

---

## 원칙

### 1. 마이그레이션 파일은 타임스탬프 접두사로 네이밍한다

```
migrations/
├── 20240101000000_create_users.sql
├── 20240102000000_create_posts.sql
├── 20240103000000_add_user_roles.sql
```

`sqlx migrate add <name>` 명령이 현재 시각 기반 타임스탬프를 자동으로 붙인다. 숫자 순서가 실행 순서를 결정한다.

### 2. Reversible 마이그레이션은 `.up.sql` / `.down.sql`로 분리한다

```bash
sqlx migrate add -r create_users
# migrations/20240101000000_create_users.up.sql
# migrations/20240101000000_create_users.down.sql
```

```sql
-- 20240101000000_create_users.up.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);
CREATE INDEX idx_users_email ON users(email);

-- 20240101000000_create_users.down.sql
DROP TABLE IF EXISTS users;
```

### 3. 앱 시작 시 `sqlx::migrate!()`로 자동 마이그레이션을 실행한다

```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let pool = PgPoolOptions::new()
        .connect(&env::var("DATABASE_URL")?)
        .await?;

    // migrations/ 디렉토리의 SQL 파일을 순서대로 실행
    sqlx::migrate!("./migrations")
        .run(&pool)
        .await?;

    // 라우터 시작...
    Ok(())
}
```

`sqlx::migrate!()` (인자 없음)는 `./migrations` 를 기본 경로로 사용한다. 경로는 `Cargo.toml` 위치 기준이다.

### 4. CI에서는 `cargo sqlx prepare --check`로 드리프트를 감지한다

```bash
# 개발 환경에서 캐시 생성
cargo sqlx prepare

# 워크스페이스 전체
cargo sqlx prepare --workspace

# CI에서 캐시가 최신인지 검증
cargo sqlx prepare --check
```

`.sqlx/` 디렉토리를 git에 커밋하면 DB 없이도 `cargo build`가 가능하다.

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| sqlx-cli 버전 | 0.8.x | `cargo install sqlx-cli --no-default-features --features native-tls,postgres` |
| 타임스탬프 형식 | `YYYYMMDDHHmmss` | `sqlx migrate add`가 자동 생성 |
| 마이그레이션 실행 순서 | 타임스탬프 오름차순 | 숫자 정렬 |
| `_sqlx_migrations` 테이블 | 자동 생성 | 실행 이력 추적 |

---

## 안티패턴

### 이미 실행된 마이그레이션 파일 수정

sqlx는 마이그레이션 파일의 체크섬을 저장한다. 기존 파일을 수정하면 체크섬 불일치로 실행이 거부된다. 변경이 필요하면 새 마이그레이션 파일을 추가한다.

### 프로덕션에서 `migrate revert` 사용

`revert`는 `.down.sql`을 실행한다. 데이터 삭제가 포함될 수 있으므로 프로덕션에서는 반드시 백업 후 수동 검토 후 실행한다.

### 하나의 마이그레이션에 너무 많은 변경 포함

테이블 생성, 인덱스 추가, 데이터 마이그레이션을 하나의 파일에 묶으면 롤백 범위가 커진다. 논리적으로 분리하여 파일을 나눈다.

---

## Gotchas

### `sqlx::migrate!()`의 경로는 `Cargo.toml` 기준이다

`./migrations`는 현재 실행 디렉토리가 아니라 `Cargo.toml`이 있는 크레이트 루트 기준이다. 워크스페이스 구조에서 경로가 달라질 수 있으므로 절대 경로 또는 `CARGO_MANIFEST_DIR`을 활용한다.

```rust
sqlx::migrate!(concat!(env!("CARGO_MANIFEST_DIR"), "/migrations"))
```

### `_sqlx_migrations` 테이블이 없으면 첫 실행 시 자동 생성된다

마이그레이션 추적 테이블은 sqlx가 자동으로 만든다. 별도로 생성하지 않아도 된다.

### `sqlx migrate run`과 `sqlx::migrate!()`는 동일한 체크섬 검증을 사용한다

CLI와 코드 중 어느 쪽으로 실행해도 같은 `_sqlx_migrations` 테이블을 공유한다. 두 방식을 혼용해도 중복 실행되지 않는다.

### reversible과 non-reversible 마이그레이션을 혼용하면 `revert`가 non-reversible에서 실패한다

프로젝트 내에서 한 가지 방식으로 통일하는 것을 권장한다.
