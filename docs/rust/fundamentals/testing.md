---
title: 테스팅 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 테스팅 원칙

Rust는 언어 차원에서 테스트를 지원한다(`#[test]`, `#[cfg(test)]`). 외부 크레이트(cargo-nextest, mockall)는 실행 속도와 모킹을 보완한다. 테스트는 격리되어야 하고, 외부 의존성(DB, 네트워크)은 주입 가능해야 한다.

---

## 원칙

### 1. 단위 테스트는 같은 파일, 통합 테스트는 `tests/`에 둔다

Rust 관례: 단위 테스트는 구현 파일 하단의 `#[cfg(test)]` 모듈, 통합 테스트는 크레이트 루트의 `tests/` 디렉토리. 통합 테스트는 크레이트 public API만 사용한다.

```rust
// src/domain/user.rs
pub fn validate_email(email: &str) -> bool { ... }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valid_email_passes() {
        assert!(validate_email("user@example.com"));
    }

    #[test]
    fn empty_email_fails() {
        assert!(!validate_email(""));
    }
}
```

```text
crates/domain/
├── src/
│   └── user.rs          # 단위 테스트 포함
└── tests/
    └── user_flow.rs     # 통합 테스트 — public API만
```

> **출처:** [Rust Book Ch.11 — How to Write Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)

### 2. cargo-nextest로 테스트를 실행한다

`cargo test`보다 2~3배 빠르고, 테스트를 프로세스 단위로 격리한다. 글로벌 상태 오염이 자동으로 방지된다. CI에서도 `cargo nextest run`을 표준으로 사용한다.

```bash
# 설치
cargo install cargo-nextest

# 실행
cargo nextest run
cargo nextest run --test-threads 4   # 병렬 수 제한
cargo nextest run -p domain          # 특정 크레이트만
```

설정 파일(`.config/nextest.toml` 또는 `nextest.toml`):
```toml
[profile.default]
fail-fast = false          # 실패해도 계속 실행
test-threads = "num-cpus"  # CPU 수만큼 병렬

[profile.ci]
fail-fast = true
```

> **출처:** [cargo-nextest — Configuration](https://nexte.st/docs/configuration/)

### 3. trait 기반 모킹으로 외부 의존성을 격리한다

헥사고날 아키텍처의 Port trait을 활용하면 테스트에서 가짜 구현을 주입할 수 있다. `mockall` 크레이트는 `#[automock]` 매크로로 mock을 자동 생성한다.

```rust
// domain/src/ports/database.rs
#[cfg_attr(test, mockall::automock)]
#[async_trait::async_trait]
pub trait DatabasePort: Send + Sync {
    async fn find_user(&self, id: UserId) -> Result<Option<User>, DomainError>;
}

// 테스트에서 mock 사용
#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;

    #[tokio::test]
    async fn get_user_returns_not_found() {
        let mut mock_db = MockDatabasePort::new();
        mock_db
            .expect_find_user()
            .with(eq(UserId::from(1)))
            .returning(|_| Ok(None));

        let service = UserService::new(Arc::new(mock_db));
        let result = service.get_user(UserId::from(1)).await;
        assert!(matches!(result, Err(DomainError::NotFound { .. })));
    }
}
```

> **출처:** [mockall — Getting Started](https://docs.rs/mockall/latest/mockall/)

### 4. DB 테스트는 `sqlx::test`로 테스트별 새 테스트 DB 를 쓴다

`#[sqlx::test]`는 테스트 함수마다 **새 테스트 DB** 를 만들어 live connection 을 주입하고, `migrations`
폴더가 있으면 자동 적용하며, 테스트가 성공하면 그 DB 를 정리한다. 테스트 간 DB 상태 오염이 없다.

> **정정 2026-08-13:** 이전 판이 "테스트마다 트랜잭션을 열고 끝나면 롤백한다" 고 적었으나 공식
> 문서 기준 사실이 아니다. 격리 단위는 트랜잭션이 아니라 **DB** 이며, 커밋된 데이터도 남았다가
> DB 단위로 폐기된다. Postgres/MySQL 은 `DATABASE_URL` 이 필요하다.

```rust
// adapters/tests/user_repository.rs
#[sqlx::test(fixtures("users"))]
async fn find_existing_user(pool: sqlx::PgPool) {
    let adapter = PostgresUserAdapter::new(pool);
    let result = adapter.find_user(UserId::from(1)).await;
    assert!(result.unwrap().is_some());
}
```

fixture 파일(`tests/fixtures/users.sql`):
```sql
INSERT INTO users (id, email) VALUES (1, 'test@example.com');
```

> **출처:** [sqlx — Testing](https://docs.rs/sqlx/latest/sqlx/attr.test.html)

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| cargo-nextest vs cargo test 속도 | 2~3× 빠름 | 프로세스 격리 + 병렬 실행 |
| mockall 모킹 오버헤드 | 무시 가능 | 테스트 전용 코드 |
| sqlx::test 테스트별 새 테스트 DB 생성 + migration | 프로젝트에서 실측 | 트랜잭션 롤백이 아니라 DB 생성·정리 비용 — 환경 의존이라 고정 수치를 쓰지 마라 |
| 단위 테스트 실행 목표 | < 1ms/테스트 | 외부 I/O 없을 때 |
| 통합 테스트 실행 목표 | < 100ms/테스트 | DB, 네트워크 포함 |

---

## 안티패턴

### 글로벌 상태를 통한 테스트 데이터 공유

`static mut`나 `lazy_static`으로 공유 상태를 두면 테스트 실행 순서에 따라 결과가 달라진다. 각 테스트는 독립적으로 필요한 데이터를 생성해야 한다.

### 단위 테스트에서 실제 DB 연결

단위 테스트는 네트워크/DB 없이 실행되어야 한다. Port trait을 mock으로 교체하면 DB 없이 도메인 로직을 테스트할 수 있다.

### 테스트 파일에 `#[allow(dead_code)]` 남기기

사용하지 않는 테스트 헬퍼는 삭제한다. 테스트 코드도 프로덕션 코드와 같은 품질 기준을 적용한다.

### `unwrap()`으로 테스트 실패 메시지를 감추기

`result.unwrap()`이 패닉하면 "called `Option::unwrap()` on a `None` value"만 출력된다. `assert!(result.is_ok(), "error: {:?}", result.err())`나 `result.expect("구체적인 메시지")`를 사용한다.

---

## Gotchas

### `#[tokio::test]`와 `#[sqlx::test]`를 동시에 사용할 수 없다

`#[sqlx::test]`는 자체 tokio 런타임을 포함한다. 두 속성을 중복 사용하면 런타임 중첩 에러가 발생한다. DB 테스트에는 `#[sqlx::test]`만 사용한다.

### mockall `expect_*`은 drop 시 검증한다

`MockDatabasePort`가 드롭될 때 `expect_*`으로 설정한 호출 횟수를 검증한다. `assert!` 이전에 mock이 드롭되면 검증이 테스트 결과와 분리된다. 명시적으로 `drop(mock)`을 테스트 마지막에 호출하거나 블록 스코프를 사용한다.

### `cargo test`와 달리 `nextest`는 `--nocapture` 대신 `--no-capture`

출력을 확인하려면 `cargo nextest run --no-capture`를 사용한다. `cargo test -- --nocapture`와 플래그 이름이 다르다.

### fixture 경로는 크레이트 루트 기준이다

`#[sqlx::test(fixtures("users"))]`는 `tests/fixtures/users.sql`을 찾는다. 경로가 잘못되면 "fixture not found" 에러가 발생한다.
