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

- **SQLx `#[sqlx::test]` 는 트랜잭션 롤백이 아니다 (사실 정정 2026-08-13)** — 이 매크로는 테스트 함수마다 **새 테스트 DB** 를 만들어 live connection(`PgPool`/`PgConnection`)을 인자로 주입하고, `migrations` 폴더가 있으면 **자동 적용**하며, 테스트가 **성공하면 그 DB 를 정리**한다. "테스트별 독립 트랜잭션을 열고 끝나면 롤백" 이라는 설명은 틀렸다 — 커밋된 데이터도 그대로 남았다가 DB 단위로 폐기된다. Postgres/MySQL 은 `DATABASE_URL` 이 필요하고, 자동 적용을 끄려면 `migrations = false`, 다른 경로를 쓰려면 `migrations = "./migrations"` 를 준다 ([sqlx::test](https://docs.rs/sqlx/latest/sqlx/attr.test.html)). 직접 `PgPool` 을 만들거나 수동 롤백 코드를 넣지 마라.
- **SeaORM `MockDatabase` — 능력 범위와 한계를 같이 적어라** — Docker/실제 DB 없이 **`MockDatabase::new(DatabaseBackend::Postgres)`** + `.append_query_results(vec![...])` 로 단위 테스트를 돌린다 (`HAS_SEAORM` + `features = ["mock"]`). **검증할 수 있는 것**: `rows_affected` 매핑, repository control flow(0 행일 때 conflict 분기·후속 호출 0 회), 생성된 statement/transaction log. **검증할 수 없는 것**: **실제 SQL predicate 의미** — 문법상 유효하지만 의미상 틀린 `WHERE` 절이 mock 에서는 그대로 통과한다 ([SeaORM MockDatabase](https://www.sea-ql.org/SeaORM/docs/write-test/mock/)). 술어 의미가 걸린 조건(동시성 가드·필터링·권한 범위)은 실 DB 엔진 테스트가 있어야 한다 — `references/concurrency-guard-protocol.md` §3.
- **통합 테스트는 `serial_test` + TRUNCATE 격리** — 실제 DB를 사용하는 통합 테스트는 `modules/{module}/tests/` 크레이트 `tests/` 디렉토리에 두고, 각 테스트를 `#[serial_test::serial]`로 직렬화한 뒤 fixture setup에서 `TRUNCATE TABLE ... RESTART IDENTITY CASCADE`로 상태 초기화한다. 병렬 실행 시 테스트간 데이터 간섭을 방지한다. 출처: fit-pal `server/CLAUDE.md` §테스트 가능성.
- **`test_support` 모듈** — `src/test_support.rs`에 `#[cfg(test)]`로 mock 구현체, fixture builder, test DB setup 헬퍼를 모아두고 `pub(crate)`로 공개한다. 각 테스트 파일에서 중복 작성 금지 (SSOT).
- **`#[tokio::test]`는 기본이 `current_thread` flavor** — `tokio::spawn`이나 멀티스레드 동작이 필요하면 `#[tokio::test(flavor = "multi_thread")]`를 명시하라. OTel 트레이싱 subscriber, Axum TestServer 같은 case에서 필요할 수 있다.
- **mockall `#[automock]`은 trait에만** — 구체 struct 메서드에는 사용할 수 없으니, 테스트 대상이 trait이 아니면 먼저 trait 추출을 제안하라. 외부 HTTP 클라이언트, OIDC, 이메일 등은 반드시 port trait으로 먼저 감싼다.
- **라우터 상태는 trait object** — 통합 테스트에서 mock 서비스를 주입하려면 프로덕션 코드가 `Arc<dyn UserService>` 형태의 trait object를 `Router::with_state()`에 받아야 한다. 구체 타입 `UserServiceImpl`를 state로 넣으면 테스트에서 mock으로 교체 불가. 출처: fit-pal `server/CLAUDE.md` §테스트 가능성.
- **테스트 간 상태 격리 필수** — 테스트가 공유 리소스(DB, 파일, 환경 변수)를 사용하면 병렬 실행 시 간헐적 실패가 발생한다. 환경 변수는 `temp_env` 크레이트로 scoped 설정하고, DB는 `#[sqlx::test]`(테스트별 새 테스트 DB) 또는 `serial_test` + TRUNCATE 로 격리해라.
- **Fixture builder 패턴 사용** — 테스트 데이터를 매번 인라인으로 구성하면 50줄짜리 setup이 테스트 의도를 가린다. `UserFixture::builder().email("test@x.com").build()` 패턴으로 `test_support` 모듈에 builder를 두고 재사용해라.
- **`#[tokio::test]` vs `#[sqlx::test]` 혼용 주의** — 같은 파일에서 둘을 섞으면 DB pool 초기화 충돌이 날 수 있다. DB 관련 테스트는 `#[sqlx::test]`로 통일하고, pure logic 테스트만 `#[tokio::test]`를 사용해라.
- **proptest로 property-based testing** — `proptest 1.11` (2026-03)은 자동 shrinking 포함 property-based testing을 제공한다. 날짜 파싱, 수학 invariant, 직렬화 round-trip 검증에 효과적이다. 단위 테스트로 커버하기 어려운 경계값/조합 케이스에 활용하라.
- **rstest로 parameterized test** — `rstest 0.26` (2025-07)의 `#[rstest]` + `#[case]`로 테이블 기반 테스트, `#[fixture]`로 setup 공유가 가능하다. 동일 로직을 여러 입력으로 반복 검증할 때 boilerplate를 줄인다.
- **testcontainers로 실제 인프라 통합 테스트** — Docker 기반으로 PostgreSQL, Redis, Kafka 등 실제 인스턴스를 테스트 격리 환경에서 구동한다. CI에서 `--test-threads=1`과 조합하라. 버전은 `references/project-detection.md` **Step 2c**(버전 현행성 표)를 따른다 — 프로젝트에 고정된 버전이 우선이며, 문서의 예시 버전을 근거로 업그레이드를 요구하지 마라.
- **cargo-mutants로 테스트 품질 검증** — coverage가 아니라 "테스트가 동작 차이를 감지하는지"를 본다. `--iterate`로 missed mutant 개선 루프를 줄이고, baseline test로 원본 트리가 통과하는지 먼저 검증한다. flaky test가 있으면 의미가 무너진다.
- **Miri로 unsafe UB 검증** — `cargo +nightly miri test`는 out-of-bounds, use-after-free, data race, aliasing 위반 등을 잡는다. unsafe 코드가 있거나 low-level crate를 만들면 CI에 Miri 레인을 별도로 두되, "Miri 통과 = soundness 보장"은 아님을 인지하라.
- **`MockDatabase` 단위 테스트를 통합 테스트로 주장하지 마라 (API-01 회귀 방지)** — SeaORM 공식 문서는 mock DB 에 실제 데이터가 없고 반환값을 직접 정의하는 방식이므로 **실 DB 기준 SQL 정합성을 검증하지 못한다**고 명시한다 — 문법상 유효하지만 의미상 틀린 쿼리가 mock 에서는 통과하고 프로덕션에서 깨진다 ([SeaORM MockDatabase](https://www.sea-ql.org/SeaORM/docs/write-test/mock/)). 계약이 "통합 테스트" 를 요구하면 `#[sqlx::test]` 또는 testcontainers 로 **실제 엔진**을 태워야 한다. 2026-07 실측: "user 통합 테스트(실제 PostgreSQL) 미존재 — MockDatabase 단위 테스트만 있음" 으로 REJECT. 리포트에는 항상 계층을 명시한다: `단위(mock) N 건 / 통합(실 DB) M 건`.
- **공유 DB 를 쓰는 테스트는 마이그레이션 선적용 필요 (DG-03)** — `#[sqlx::test]` 는 함수마다 새 테스트 DB 를 만들고 `CARGO_MANIFEST_DIR` 의 `migrations` 폴더를 **자동 적용**한다 (`migrations = false` 로 끌 수 있음) ([sqlx::test](https://docs.rs/sqlx/latest/sqlx/attr.test.html)). 반면 `#[tokio::test]` + `serial_test` 로 **공유 로컬 DB** 를 직접 쓰는 통합 테스트는 자동 적용이 없으므로 `sqlx migrate run` 또는 마이그레이션 크레이트 실행이 선행돼야 한다. 컬럼 부재 에러(`column "..." does not exist`)를 코드 결함으로 오진하지 마라 — 먼저 스키마 상태를 확인한다.
- **테스트 서버는 포트 0 으로 바인딩** — 통합 테스트에서 고정 포트(`127.0.0.1:8080`)를 쓰면 병렬 실행·이전 프로세스 잔존 시 `Address already in use` 로 간헐 실패한다. `TcpListener::bind("127.0.0.1:0")` 로 커널이 빈 포트를 할당하게 하고 `listener.local_addr()?` 로 실주소를 읽어 클라이언트 base URL 을 구성한다. 출처: 2026-07 실측 `port-already-in-use`.
- **타깃 필터 전 `PKG_TARGETS` 확인** — 생성한 테스트를 실행해 보일 때 `--lib` 을 반사적으로 붙이지 마라. 바이너리 전용 패키지에는 `lib` 타깃이 없어 테스트 0 개로 끝난다. `references/project-detection.md` Step 3a 로 타깃 kind 를 먼저 열거하고 `--bins`/`--tests`/무필터 중 맞는 것을 고른다 ([cargo-test 타깃 선택](https://doc.rust-lang.org/cargo/commands/cargo-test.html)). 출처: 2026-07 실측 `cargo-test-wrong-target`.
- **"테스트 0 개 통과" 는 증거가 아니다** — 생성한 테스트가 실제로 실행됐는지 **실행 수**로 확인한다 (`running N tests`). 필터 오타·`#[ignore]`·타깃 오지정으로 0 개가 실행됐는데 exit 0 이면 그건 통과가 아니라 측정 실패다 (`qa-evaluation-guide.md` §Evidence Validity Gate 검사 2). 완료 보고에는 실행 수와 종료 코드를 함께 적는다.
- **Sibling Consistency (skill-design-guide §8.8) — rust-test ↔ backend-test** — backend-test 가 강제하는 3 계층 패턴(단위 / 통합 / 컨트랙트) 과 동일 구조를 유지한다: (1) **단위** = SeaORM `MockDatabase::new(DatabaseBackend::Postgres)` 또는 mockall `#[automock]` (Docker 불필요), (2) **통합** = `#[sqlx::test]`(테스트별 새 테스트 DB) 또는 `testcontainers` 실제 DB, (3) **컨트랙트** = Pact v4 consumer-driven contract (존재 시). Step 0 에서 스택 감지 (`HAS_SQLX` / `HAS_SEAORM` / `HAS_MOCKALL`) 를 독립 단계로 분리하여 테스트 패턴 자동 선택. 외부 실환경(production DB) 강제 금지 — CI 에서 재현 불가.
- **동시성 가드에는 테스트 쌍이 필수다 (ER-02 회귀 방지 · E2)** — 조건부 `UPDATE`·낙관적 락 같은 가드를 테스트할 때 positive test 만 만들면 **가드를 지워도 통과하는 측정**이 된다. 2026-08-12 실측: *"mutation test 로 확정 — 실제 코드에서 동시성 가드(`WHERE exercises = $3::jsonb`)를 완전히 삭제해도 이 테스트는 여전히 통과한다"*. 생성 절차(호출부 함수 추출 · 영향 행 수 0 → `Conflict` · positive + **stale expected value** negative 쌍 · 실 DB 실행 · 테스트가 구현 심볼을 직접 호출)는 `references/concurrency-guard-protocol.md` 가 SSOT 다. 이 스킬에서 규칙을 재열거하지 말고 그 파일을 읽어 따르라.

# Rust 테스트 코드 생성

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 `$CARGO`, `ARCH`, `IS_WORKSPACE`, `PKG_TARGETS`, `HAS_SQLX`, `HAS_SEAORM`, `HAS_TOKIO`를 사용한다.
Step 3a(패키지 타깃 구조 감지)는 **필수**다 — 생성한 테스트의 실행 명령을 안내할 때 `--lib`/`--bins` 선택
근거가 된다.

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
| 동시성 가드 (조건부 UPDATE · 낙관적 락) | positive + stale negative **쌍** (실 DB) — `references/concurrency-guard-protocol.md` | `tests/integration/` |
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

`HAS_SQLX`이면 `#[sqlx::test]`를 사용한다. 테스트 함수마다 **새 테스트 DB** 가 만들어지고 `migrations`
가 자동 적용되며, 테스트가 성공하면 그 DB 가 정리된다 (트랜잭션 롤백이 아니다 — §Gotchas 첫 항목 참조):

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

`MockDatabase`는 Docker 없이 CI에서 실행 가능하다 (타깃 필터를 붙일 때는 `PKG_TARGETS` 확인 — §Gotchas 타깃 필터 항목).
실제 쿼리 실행 대신 사전 설정된 응답을 순서대로 반환하므로, **이 테스트는 단위 계층이다.**
`rows_affected` 매핑과 control flow 는 검증되지만 **실제 SQL predicate 가 행을 걸러내는지는 검증되지
않는다** — 술어 의미가 걸린 조건은 §7I 또는 `references/concurrency-guard-protocol.md` §3 의 실 DB
테스트로 별도 확보한다. 리포트에 "통합 테스트" 로 표기하지 마라.

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

생성 완료 후 실행 명령을 안내한다. **타깃 필터는 Step 0 에서 얻은 `PKG_TARGETS` 에 맞춰 고른다**:

```bash
# 무필터가 기본 — lib/bin 단위 테스트 + 통합 테스트 + doctest 를 모두 실행
cargo test --workspace

# lib 타깃이 있는 패키지만 좁힐 때
cargo test -p my-lib --lib

# 바이너리 전용 패키지 (PKG_TARGETS 에 lib 없음) — --lib 금지, --bins 사용
cargo test -p my-api --bins

# 통합 테스트(tests/ 디렉토리)만
cargo test -p my-api --tests

# cargo-nextest (설치돼 있으면 권장 — 빠른 병렬 실행)
cargo nextest run --workspace
```

## After Creation

1. 생성/수정된 파일 목록 출력.
2. mock을 위해 trait에 `#[automock]`을 추가한 경우, 원본 파일 변경을 명시한다.
3. `#[sqlx::test]`를 사용하는 경우 `DATABASE_URL` 환경변수 설정 필요 여부를 안내한다. 공유 DB 를 쓰는
   `serial_test` 계열이면 마이그레이션 선적용(`sqlx migrate run` 또는 마이그레이션 크레이트 실행)도 함께 안내한다.
4. **테스트 계층을 명시 집계한다** — `단위(mock) N 건 / 통합(실 DB) M 건 / 프로퍼티 K 건`. mock 만
   만들었으면 "통합 테스트 0 건" 을 숨기지 말고 그대로 적는다 (API-01 회귀 방지).
5. 실행 증거를 남긴다 — 실행한 명령 · **실행된 테스트 수** · 종료 코드. 실행하지 않았으면
   `[미검증] 테스트 미실행` 으로 명시하고 통과를 주장하지 않는다.
6. 다음 단계 안내:
   - 빌드와 clippy도 확인하려면 `rust-build` 스킬을 사용하세요.
   - Pre-commit 전체 gate를 실행하려면 `rust-preflight` 스킬을 사용하세요.
