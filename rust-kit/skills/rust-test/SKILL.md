---
name: rust-test
description: >
  대상 파일/모듈을 분석하여 Rust 테스트 코드를 자동 생성한다.
  순수 함수는 단위 테스트, trait impl은 mockall mock, 핸들러는 통합 테스트, DB 의존은 sqlx::test로 생성한다.
  "테스트 만들어줘", "unit test", "integration test", "테스트 추가", "rust test" 같은 요청 시 사용한다.
argument-hint: "<file_or_module> [unit|integration|mock]"
user-invocable: true
---

## Gotchas

- **SQLx `#[sqlx::test]`** — 테스트별 독립 DB 트랜잭션을 자동으로 제공한다. 직접 `PgPool`을 만들거나 수동으로 롤백하지 마라. `migrations = "./migrations"` 인자로 마이그레이션 자동 적용 가능.
- **SeaORM `MockDatabase`** — SeaORM은 Docker/실제 DB 없이 **`MockDatabase::new(DatabaseBackend::Postgres)`**로 단위 테스트를 실행할 수 있다. `.append_query_results(vec![...])`로 쿼리 응답을 주입한다. `HAS_SEAORM` + `features = ["mock"]` (fit-pal 기준). `cargo test --lib`만으로 완전히 격리된 단위 테스트 가능.
- **통합 테스트는 `serial_test` + TRUNCATE 격리** — 실제 DB를 사용하는 통합 테스트는 `modules/{module}/tests/` 크레이트 `tests/` 디렉토리에 두고, 각 테스트를 `#[serial_test::serial]`로 직렬화한 뒤 fixture setup에서 `TRUNCATE TABLE ... RESTART IDENTITY CASCADE`로 상태 초기화한다. 병렬 실행 시 테스트간 데이터 간섭을 방지한다. 출처: fit-pal `server/CLAUDE.md` §테스트 가능성.
- **`test_support` 모듈** — `src/test_support.rs`에 `#[cfg(test)]`로 mock 구현체, fixture builder, test DB setup 헬퍼를 모아두고 `pub(crate)`로 공개한다. 각 테스트 파일에서 중복 작성 금지 (SSOT).
- **`#[tokio::test]`는 기본이 `current_thread` flavor** — `tokio::spawn`이나 멀티스레드 동작이 필요하면 `#[tokio::test(flavor = "multi_thread")]`를 명시하라. OTel 트레이싱 subscriber, Axum TestServer 같은 case에서 필요할 수 있다.
- **mockall `#[automock]`은 trait에만** — 구체 struct 메서드에는 사용할 수 없으니, 테스트 대상이 trait이 아니면 먼저 trait 추출을 제안하라. 외부 HTTP 클라이언트, OIDC, 이메일 등은 반드시 port trait으로 먼저 감싼다.
- **라우터 상태는 trait object** — 통합 테스트에서 mock 서비스를 주입하려면 프로덕션 코드가 `Arc<dyn UserService>` 형태의 trait object를 `Router::with_state()`에 받아야 한다. 구체 타입 `UserServiceImpl`를 state로 넣으면 테스트에서 mock으로 교체 불가. 출처: fit-pal `server/CLAUDE.md` §테스트 가능성.
- **테스트 간 상태 격리 필수** — 테스트가 공유 리소스(DB, 파일, 환경 변수)를 사용하면 병렬 실행 시 간헐적 실패가 발생한다. 환경 변수는 `temp_env` 크레이트로 scoped 설정하고, DB는 `#[sqlx::test]` 또는 테스트별 트랜잭션 롤백으로 격리해라.
- **Fixture builder 패턴 사용** — 테스트 데이터를 매번 인라인으로 구성하면 50줄짜리 setup이 테스트 의도를 가린다. `UserFixture::builder().email("test@x.com").build()` 패턴으로 `test_support` 모듈에 builder를 두고 재사용해라.
- **`#[tokio::test]` vs `#[sqlx::test]` 혼용 주의** — 같은 파일에서 둘을 섞으면 DB pool 초기화 충돌이 날 수 있다. DB 관련 테스트는 `#[sqlx::test]`로 통일하고, pure logic 테스트만 `#[tokio::test]`를 사용해라.
- **proptest로 property-based testing** — `proptest 1.11` (2026-03)은 자동 shrinking 포함 property-based testing을 제공한다. 날짜 파싱, 수학 invariant, 직렬화 round-trip 검증에 효과적이다. 단위 테스트로 커버하기 어려운 경계값/조합 케이스에 활용하라.
- **rstest로 parameterized test** — `rstest 0.26` (2025-07)의 `#[rstest]` + `#[case]`로 테이블 기반 테스트, `#[fixture]`로 setup 공유가 가능하다. 동일 로직을 여러 입력으로 반복 검증할 때 boilerplate를 줄인다.
- **testcontainers로 실제 인프라 통합 테스트** — `testcontainers 0.27` (2026-03)은 Docker 기반으로 PostgreSQL, Redis, Kafka 등 실제 인스턴스를 테스트 격리 환경에서 구동한다. CI에서 `--test-threads=1`과 조합하라.
- **cargo-mutants로 테스트 품질 검증** — coverage가 아니라 "테스트가 동작 차이를 감지하는지"를 본다. `--iterate`로 missed mutant 개선 루프를 줄이고, baseline test로 원본 트리가 통과하는지 먼저 검증한다. flaky test가 있으면 의미가 무너진다.
- **Miri로 unsafe UB 검증** — `cargo +nightly miri test`는 out-of-bounds, use-after-free, data race, aliasing 위반 등을 잡는다. unsafe 코드가 있거나 low-level crate를 만들면 CI에 Miri 레인을 별도로 두되, "Miri 통과 = soundness 보장"은 아님을 인지하라.

# Rust 테스트 코드 생성

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 `$CARGO`, `ARCH`, `IS_WORKSPACE`, `HAS_SQLX`, `HAS_TOKIO`를 사용한다.

`dev-dependencies`에 `mockall`이 있는지 확인한다. 없으면 mock 생성 시 추가를 제안한다.
`cargo nextest`가 설치되어 있는지 확인한다 (`cargo nextest --version`).

---

## 1. 대상 분석

`$ARGUMENTS`에서 파일/모듈 경로를 파싱한다. 대상 파일을 읽어 다음을 추출한다:

| 항목 | 추출 대상 |
|------|-----------|
| 공개 함수 | `pub fn`, `pub async fn` 목록 |
| trait 정의 | `pub trait` 목록과 메서드 시그니처 |
| 구조체 | `pub struct` + 주요 메서드 |
| 에러 타입 | `Result<T, E>`의 E 타입 |

---

## 2. 기존 테스트 패턴 읽기

같은 모듈이나 `tests/` 디렉토리에 기존 테스트가 있으면 읽어 컨벤션을 파악한다:

- assert 스타일 (`assert_eq!`, `pretty_assertions`, `insta` 등)
- fixture 생성 패턴 (`TestFixture`, builder 패턴 등)
- mock 초기화 방식 (mockall 기반이면 `MockXxx::new()` 패턴)
- DB 테스트가 있으면 `#[sqlx::test]` 시그니처 확인

---

## 3. 테스트 타입 결정

대상 코드 특성에 따라 테스트 타입을 선택한다:

| 대상 유형 | 테스트 타입 | 위치 |
|----------|------------|------|
| 순수 함수 (I/O 없음) | 단위 테스트 | 같은 파일 `#[cfg(test)] mod tests` |
| trait impl | mock 기반 단위 테스트 | 같은 파일 또는 `tests/unit/` |
| Axum 핸들러 | 통합 테스트 (TestClient 또는 실제 서버) | `tests/integration/` |
| DB 의존 함수 | `#[sqlx::test]` 통합 테스트 | `tests/integration/` |
| 경계값/조합 검증 | proptest property-based | 같은 파일 또는 `tests/property/` |
| 테이블 기반 반복 검증 | rstest parameterized | 같은 파일 `#[cfg(test)] mod tests` |
| 실제 인프라 (Docker) | testcontainers 통합 테스트 | `tests/integration/` |
| unsafe 코드 UB 검증 | Miri (`cargo +nightly miri test`) | 기존 테스트에 추가 실행 |

여러 타입이 혼재하면 사용자에게 우선순위를 확인한다.

---

## 4. 단위 테스트 생성 (순수 함수)

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_discount_zero_for_no_items() {
        let result = calculate_discount(0, 100.0);
        assert_eq!(result, 0.0);
    }

    #[test]
    fn test_calculate_discount_applies_bulk_rate() {
        let result = calculate_discount(10, 100.0);
        assert!(result > 0.0);
    }
}
```

비동기 함수는 `#[tokio::test]`를 붙인다:

```rust
#[tokio::test]
async fn test_fetch_user_returns_error_when_not_found() {
    let result = fetch_user(9999).await;
    assert!(result.is_err());
}
```

---

## 5. Mock 기반 단위 테스트 생성 (trait)

mockall이 설치되어 있으면 trait에 `#[automock]`을 추가하고, 테스트에서 mock을 사용한다:

```rust
// domain/ports/user_repository.rs
use mockall::automock;

#[automock]  // 추가
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: i64) -> Result<User, DomainError>;
    async fn save(&self, user: &User) -> Result<(), DomainError>;
}
```

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::ports::MockUserRepository;

    #[tokio::test]
    async fn test_create_user_calls_repository_save() {
        let mut mock_repo = MockUserRepository::new();
        mock_repo
            .expect_save()
            .once()
            .returning(|_| Ok(()));

        let service = UserServiceImpl::new(mock_repo);
        let req = CreateUserRequest { email: "test@example.com".into(), name: "Test".into() };
        let result = service.create_user(req).await;

        assert!(result.is_ok());
    }
}
```

---

## 6. 통합 테스트 생성 (Axum 핸들러)

`axum::body::to_bytes`와 `axum_test` 또는 `tower::ServiceExt`를 사용한다:

```rust
// tests/integration/users_test.rs
use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::ServiceExt;
use serde_json::json;

#[tokio::test]
async fn test_create_user_returns_201() {
    let app = create_test_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/users")
                .header("Content-Type", "application/json")
                .body(Body::from(
                    serde_json::to_string(&json!({
                        "email": "test@example.com",
                        "name": "Test User"
                    })).unwrap(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::CREATED);
}
```

---

## 7. DB 테스트 생성 (SQLx 또는 SeaORM)

### §7X — SQLx `#[sqlx::test]` 통합 테스트

`HAS_SQLX`이면 `#[sqlx::test]`를 사용한다. 테스트마다 독립 트랜잭션이 제공되어 롤백이 자동으로 된다:

```rust
// tests/integration/user_repository_test.rs
use sqlx::PgPool;

#[sqlx::test(migrations = "./migrations")]
async fn test_find_user_by_id_returns_user(pool: PgPool) {
    let repo = UserRepositoryImpl::new(pool.clone());

    // 테스트 데이터 삽입
    sqlx::query!("INSERT INTO users (id, email, name) VALUES (1, 'test@example.com', 'Test')")
        .execute(&pool)
        .await
        .unwrap();

    let user = repo.find_by_id(1).await.unwrap();
    assert_eq!(user.email, "test@example.com");
}

#[sqlx::test(migrations = "./migrations")]
async fn test_find_user_by_id_returns_error_when_missing(pool: PgPool) {
    let repo = UserRepositoryImpl::new(pool);
    let result = repo.find_by_id(9999).await;
    assert!(matches!(result, Err(DomainError::UserNotFound(_))));
}
```

### §7S — SeaORM `MockDatabase` 단위 테스트

`HAS_SEAORM`이면 Docker/실제 DB 없이 `MockDatabase`로 Repository adapter를 단위 테스트한다. Cargo feature에 `"mock"`이 포함되어야 한다.

```rust
// modules/user/src/test_support.rs 또는 인라인 #[cfg(test)]
#[cfg(test)]
mod tests {
    use super::*;
    use sea_orm::{DatabaseBackend, MockDatabase, MockExecResult};
    use std::sync::Arc;
    use chrono::Utc;
    use crate::infra::entities::user;

    #[tokio::test]
    async fn test_find_by_id_returns_user() {
        let db = MockDatabase::new(DatabaseBackend::Postgres)
            .append_query_results(vec![vec![user::Model {
                id: 1,
                name: "Alice".to_string(),
                email: "alice@example.com".to_string(),
                created_at: Utc::now(),
            }]])
            .into_connection();

        let repo = SeaUserRepository::new(Arc::new(db));
        let found = repo.find_by_id(1).await.unwrap();
        assert!(found.is_some());
        assert_eq!(found.unwrap().email, "alice@example.com");
    }

    #[tokio::test]
    async fn test_create_inserts_row() {
        let db = MockDatabase::new(DatabaseBackend::Postgres)
            .append_exec_results(vec![MockExecResult { last_insert_id: 1, rows_affected: 1 }])
            .append_query_results(vec![vec![user::Model {
                id: 1,
                name: "Bob".to_string(),
                email: "bob@example.com".to_string(),
                created_at: Utc::now(),
            }]])
            .into_connection();

        let repo = SeaUserRepository::new(Arc::new(db));
        let created = repo.create("Bob", "bob@example.com").await.unwrap();
        assert_eq!(created.name, "Bob");
    }
}
```

`MockDatabase`는 `cargo test --lib`만으로 완전히 격리되어 CI에서 Docker 없이 실행 가능하다. 실제 쿼리 실행 대신 사전 설정된 응답을 순서대로 반환한다.

### §7I — 통합 테스트 (실제 DB, serial_test 격리)

실제 DB 동작까지 확인하려면 `modules/{mod}/tests/` 에 통합 테스트를 둔다:

```rust
// modules/user/tests/user_integration_test.rs
use serial_test::serial;
use sqlx::PgPool; // 또는 sea_orm::Database

async fn reset_db(pool: &PgPool) {
    sqlx::query("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
        .execute(pool)
        .await
        .expect("reset_db failed");
}

#[tokio::test]
#[serial]
async fn test_create_user_persists_to_db() {
    let pool = test_support::setup_db().await;
    reset_db(&pool).await;

    let repo = UserRepositoryImpl::new(pool.clone());
    let user = repo.create("Alice", "alice@example.com").await.unwrap();
    assert_eq!(user.name, "Alice");
}
```

`#[serial]`로 직렬화하면 여러 테스트가 같은 DB에 접근해도 충돌하지 않는다.

---

## 8. 실행 안내

생성 완료 후 실행 명령을 안내한다:

```bash
# cargo-nextest (권장 — 빠른 병렬 실행)
cargo nextest run

# 특정 테스트만 실행
cargo nextest run test_create_user

# 기본 cargo test (nextest 미설치 시)
cargo test

# workspace 전체
cargo nextest run --workspace
```

## After Creation

1. 생성/수정된 파일 목록 출력.
2. mock을 위해 trait에 `#[automock]`을 추가한 경우, 원본 파일 변경을 명시한다.
3. `#[sqlx::test]`를 사용하는 경우 `DATABASE_URL` 환경변수 설정 필요 여부를 안내한다.
4. 다음 단계 안내:
   - 빌드와 clippy도 확인하려면 `rust-build` 스킬을 사용하세요.
   - Pre-commit 전체 gate를 실행하려면 `rust-preflight` 스킬을 사용하세요.
