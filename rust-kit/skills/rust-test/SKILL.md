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

- `#[sqlx::test]`는 테스트별 독립 DB 트랜잭션을 자동으로 제공한다. 직접 `PgPool`을 만들거나 수동으로 롤백하지 마라.
- `#[tokio::test]`는 기본이 `current_thread` flavor다. `tokio::spawn`이나 멀티스레드 동작이 필요하면 `#[tokio::test(flavor = "multi_thread")]`를 명시하라.
- mockall의 `#[automock]`은 trait에만 적용 가능하다. 구체 struct 메서드에는 사용할 수 없으니, 테스트 대상이 trait이 아니면 먼저 trait 추출을 제안하라.

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

## 7. DB 통합 테스트 생성 (sqlx::test)

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
