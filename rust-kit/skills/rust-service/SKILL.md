---
name: rust-service
description: >
  비즈니스 로직 서비스 레이어를 생성한다.
  Hexagonal Architecture 기반으로 서비스가 포트 trait을 의존하는 구조로 생성한다.
  서비스 자체도 포트 trait으로 노출하여 핸들러 레이어가 구체 구현을 모르도록 격리한다.
  "서비스 만들어줘", "비즈니스 로직", "유즈케이스", "rust service" 같은 요청 시 사용한다.
argument-hint: "<ServiceName> [dep:RepositoryTrait ...]"
user-invocable: true
---

## Gotchas

- **`#[async_trait]` 매크로 heap allocation** — 매크로는 내부적으로 `Box::pin`을 발생시킨다. 성능 크리티컬 경로라면 Rust 1.75+ RPITIT(`async fn`이 trait에서 직접 동작)로 native async trait을 고려할 수 있다. 단, `dyn Trait` object safety가 필요한 경우(예: `Arc<dyn Port>` 라우터 상태)에는 지금도 `#[async_trait]`가 실질적인 선택이다.
- **서비스 의존 폭발 방지** — 서비스가 여러 repository에 의존하면 제네릭 파라미터가 폭발적으로 복잡해진다(`UserServiceImpl<R1: UserRepo, R2: OrderRepo, ...>`). 의존이 3개 이상이면 구체 타입(`Arc<dyn Trait>`) 필드로 시작하고 필요 시 제네릭으로 추출하라.
- **Consumer-Owned Port** — 서비스 A가 다른 모듈 B의 기능을 필요로 하면 A 내부에 outbound port trait을 정의한다. B의 `port.rs`를 직접 import하지 마라. B는 그 trait을 구현하는 adapter를 제공하고, Composition Root(apps/api/main.rs)가 `Arc<dyn ATrait>`를 주입한다. 출처: fit-pal `server/CLAUDE.md` §아키텍처.
- **포트에서 인프라 타입 제거** — 포트 trait 시그니처에 `DatabaseTransaction`, `DatabaseConnection`, SeaORM `Model`, `sqlx::Error`, `reqwest::Response` 등 인프라 구체 타입을 노출 금지. DTO/도메인 이벤트만 주고받는다. adapter 교체 가능성이 깨진다.
- **Domain event + outbox 패턴** — cross-module write 후처리(알림 발송, 감사 로그, 인덱스 동기화)는 직접 호출 대신 **domain event** 발행 + **outbox 테이블** 기록으로 처리한다. 트랜잭션 경계 안에서 write + outbox insert를 원자적으로 실행하고 별도 워커가 outbox를 폴링하여 외부 시스템에 전달한다. 출처: fit-pal `server/CLAUDE.md` §아키텍처 4번.
- **트랜잭션 경계는 서비스 메서드 단위** — Repository 메서드 안에서 트랜잭션을 시작하지 마라. 서비스 메서드가 여러 repository를 호출할 때 각각이 독립 트랜잭션이면 부분 실패 시 데이터 정합성이 깨진다. `&mut Transaction`을 서비스에서 생성하고 repository에 전달해라.
- **서비스 메서드에 `&self` 불변 참조만 사용** — `&mut self`를 사용하면 `Arc<Service>`로 공유할 때 `Mutex` 래핑이 필요해져 동시성이 병목된다. 상태 변경이 필요하면 내부 필드를 `Arc<RwLock<T>>`로 감싸거나, 상태를 DB/캐시에 위임해라.
- **async 메서드에서 blocking I/O 호출 금지** — `std::fs::read`, `std::thread::sleep`, CPU 집약 연산을 async 메서드에서 직접 호출하면 tokio runtime이 블록된다. `tokio::task::spawn_blocking`으로 격리하거나 `tokio::fs`를 사용해라.
- **서비스 간 순환 의존 금지** — ServiceA → ServiceB → ServiceA 순환이 생기면 `Arc` 순환 참조로 메모리 릭이 발생하고 테스트에서 mock 주입이 불가능해진다. 공통 로직은 별도 서비스로 추출하거나 domain event로 간접 통신해라.
- **에러 변환은 서비스 레이어에서** — Repository가 반환하는 infra error(`sqlx::Error`, `reqwest::Error`)를 그대로 상위에 전파하지 마라. 서비스 메서드에서 도메인 에러로 변환(`map_err`)하여 핸들러가 infra 타입에 의존하지 않게 한다.
- **async closure 활용 (Rust 1.85+)** — `async || {}` 문법이 안정화되어 `AsyncFn`/`AsyncFnMut`/`AsyncFnOnce` trait을 사용할 수 있다. 기존 `|| async {}` (매 호출마다 새 future 생성)와 달리 환경 변수 캡처가 가능하여 미들웨어 팩토리, 재시도 래퍼 등 고차 함수 시그니처가 자연스러워진다.
- **cancellation safety 주의** — Tokio runtime에서 future가 도중에 drop되면 트랜잭션이 절반만 실행될 수 있다. `tokio::select!` 분기나 timeout 래핑 시 cancellation-safe한 메서드(`recv()`, `read()`)와 unsafe한 메서드(`read_exact()`)를 구분하라. TokioConf 2026에서도 주요 토픽으로 강조되었다.
- **외부 크레이트 API 는 조회 기록 후 작성 (usc 재위반 — E2)** — `sea_orm` · `chrono` · `tokio` · `tracing` · `reqwest`/`reqwest-middleware` 같은 외부 크레이트의 API 를 서비스 코드에 쓰기 **전에** Context7 또는 공식 문서/`docs.rs`/CHANGELOG 를 조회하고, 응답에 아래 3 항목을 그대로 적는다:

  ```text
  문서 조회: <crate> <Cargo.toml 기준 버전> — <조회한 URL>
  ```

  "in-repo 에 같은 크레이트를 쓰는 코드가 있다" 는 조회 면제 사유가 아니다 — 기존 코드가 구버전 API 를 쓰고 있을 수 있다. 조회 기록이 없는 상태로 외부 API 를 편집하는 것은 규칙 위반이며, 이 항목은 2026-07 한 달에 usc=true 로 3 회(`external-api-doc-lookup-skipped` · `missing-official-doc-lookup-for-external-api` · `research-before-edit-ignored`) 재발했다. 실측 사례: reqwest-middleware API 를 먼저 편집하고 **컴파일 실패 후에야** 로컬 cargo registry 를 뒤짐.
- **편집 전 Read 필수** — 수정 대상 서비스 파일을 열지 않고 Edit 하지 마라 (`edit-before-read`, 2026-07 실측). 기존 트랜잭션 경계·포트 시그니처를 모르는 상태의 편집은 계층 규칙을 깬다.
- **Sibling Consistency (skill-design-guide §8.8) — rust-service ↔ backend-system** — backend-system 이 다루는 백엔드 공통 원칙(Transactional Outbox · Circuit Breaker + Rate Limiter 조합 · OAuth 2.1 Authorization Code + PKCE · RFC 9457 problem+json) 중 Rust 서비스 레이어에서 적용 가능한 항목은 동일 참조로 기재한다. 예: Outbox 는 이미 Gotcha 에 반영됨; Circuit Breaker 는 `tower::Layer` 로 service 외부에서 감싸고 service 내부 구현으로 넣지 마라 (resilience 는 infra 관심사). 출처: [Azure Circuit Breaker 패턴](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) · [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html).
- **Enumerate-before-Act (skill-design-guide §5.5)** — 서비스 메서드를 추가하기 전에 기존 `src/domain/services/*` 또는 `modules/*/service.rs` 를 전수 스캔하여 중복 유즈케이스·유사 네이밍을 먼저 열거한다. 동일 도메인 로직이 두 서비스에 분산되면 트랜잭션 경계가 혼란스러워진다.

# 서비스 레이어 생성

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `$PACKAGE`, `ARCH`, `IS_WORKSPACE`, `HAS_SQLX`, `HAS_TOKIO`)를 사용한다.

---

## 1. 입력 확인

`$ARGUMENTS`에서 파싱하거나 사용자에게 확인한다:

| 항목 | 예시 |
|------|------|
| 서비스 이름 | `UserService` |
| 의존하는 포트 | `UserRepository`, `EmailPort` 등 |
| 주요 메서드 | `create_user`, `get_user`, `delete_user` |
| 에러 타입 | 기존 `DomainError` 탐색 후 확인 |

---

## 2. 기존 서비스 패턴 읽기

서비스를 생성하기 전에 기존 서비스 파일을 읽어 프로젝트 컨벤션을 파악한다:

- 서비스 위치 (`domain/services/`, `src/domain/services/` 등)
- 에러 타입 (`DomainError`, `AppError`, 커스텀 enum)
- `#[async_trait]` 사용 여부 vs native async fn in trait
- 기존 포트 trait 파일 위치 (`domain/ports/`)

---

## 3. 포트 정의

`domain/ports/`에 두 종류의 trait을 정의한다:

**3a. 서비스가 의존하는 포트 (이미 없는 경우만 생성)**

`rust-model` 스킬이 이미 Repository trait을 생성했다면 재사용한다. 새로 필요한 포트만 추가한다.

```rust
// domain/ports/email_port.rs — 서비스가 의존하는 외부 포트 예시
use async_trait::async_trait;
use crate::domain::errors::DomainError;

#[async_trait]
pub trait EmailPort: Send + Sync {
    async fn send_welcome(&self, email: &str, name: &str) -> Result<(), DomainError>;
}
```

**3b. 서비스 자체를 포트로 노출**

핸들러 레이어가 구체 서비스 타입을 모르도록 서비스도 trait으로 정의한다.

```rust
// domain/ports/user_service.rs
use async_trait::async_trait;
use crate::domain::models::{User, CreateUserRequest};
use crate::domain::errors::DomainError;

#[async_trait]
pub trait UserService: Send + Sync {
    async fn create_user(&self, req: CreateUserRequest) -> Result<User, DomainError>;
    async fn get_user(&self, id: i64) -> Result<User, DomainError>;
    async fn delete_user(&self, id: i64) -> Result<(), DomainError>;
}
```

`mod.rs`에 새 포트 모듈을 추가한다.

---

## 4. 서비스 trait + impl 생성

`domain/services/`에 서비스 구현체를 생성한다.

서비스 구현체는 포트 trait을 제네릭 파라미터로 받는다. 의존이 1~2개이면 제네릭으로, 3개 이상이면 `Arc<dyn Trait>` 필드로 한다:

**제네릭 방식 (의존 1~2개):**

```rust
// domain/services/user_service_impl.rs
use async_trait::async_trait;
use crate::domain::models::{User, CreateUserRequest};
use crate::domain::ports::{UserRepository, EmailPort, UserService};
use crate::domain::errors::DomainError;

pub struct UserServiceImpl<R, E>
where
    R: UserRepository,
    E: EmailPort,
{
    repo: R,
    email: E,
}

impl<R, E> UserServiceImpl<R, E>
where
    R: UserRepository,
    E: EmailPort,
{
    pub fn new(repo: R, email: E) -> Self {
        Self { repo, email }
    }
}

#[async_trait]
impl<R, E> UserService for UserServiceImpl<R, E>
where
    R: UserRepository + Send + Sync,
    E: EmailPort + Send + Sync,
{
    async fn create_user(&self, req: CreateUserRequest) -> Result<User, DomainError> {
        // 비즈니스 로직
        let user = self.repo.create(&req.name, &req.email).await?;
        self.email.send_welcome(&user.email, &user.name).await?;
        Ok(user)
    }

    async fn get_user(&self, id: i64) -> Result<User, DomainError> {
        self.repo
            .find_by_id(id)
            .await?
            .ok_or(DomainError::NotFound { id })
    }

    async fn delete_user(&self, id: i64) -> Result<(), DomainError> {
        self.repo.delete(id).await
    }
}
```

**Arc<dyn> 방식 (의존 3개 이상):**

```rust
// domain/services/user_service_impl.rs
use std::sync::Arc;
use async_trait::async_trait;
use crate::domain::ports::{UserRepository, EmailPort, UserService};
use crate::domain::models::{User, CreateUserRequest};
use crate::domain::errors::DomainError;

pub struct UserServiceImpl {
    repo: Arc<dyn UserRepository>,
    email: Arc<dyn EmailPort>,
}

impl UserServiceImpl {
    pub fn new(repo: Arc<dyn UserRepository>, email: Arc<dyn EmailPort>) -> Self {
        Self { repo, email }
    }
}

#[async_trait]
impl UserService for UserServiceImpl {
    async fn create_user(&self, req: CreateUserRequest) -> Result<User, DomainError> {
        let user = self.repo.create(&req.name, &req.email).await?;
        self.email.send_welcome(&user.email, &user.name).await?;
        Ok(user)
    }

    async fn get_user(&self, id: i64) -> Result<User, DomainError> {
        self.repo
            .find_by_id(id)
            .await?
            .ok_or(DomainError::NotFound { id })
    }

    async fn delete_user(&self, id: i64) -> Result<(), DomainError> {
        self.repo.delete(id).await
    }
}
```

`mod.rs`에 `pub mod user_service_impl;`를 추가한다.

---

## 5. 테스트 모듈 생성

같은 파일 하단에 `#[cfg(test)]` 모듈을 추가한다. 포트 trait에 mock 구현체를 인라인으로 작성한다.

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Mutex;

    struct MockUserRepository {
        users: Mutex<Vec<User>>,
    }

    impl MockUserRepository {
        fn new() -> Self {
            Self { users: Mutex::new(vec![]) }
        }
    }

    #[async_trait::async_trait]
    impl UserRepository for MockUserRepository {
        async fn find_by_id(&self, id: i64) -> Result<Option<User>, DomainError> {
            let users = self.users.lock().unwrap();
            Ok(users.iter().find(|u| u.id == id).cloned())
        }

        async fn find_all(&self) -> Result<Vec<User>, DomainError> {
            Ok(self.users.lock().unwrap().clone())
        }

        async fn create(&self, name: &str, email: &str) -> Result<User, DomainError> {
            let mut users = self.users.lock().unwrap();
            let user = User {
                id: users.len() as i64 + 1,
                name: name.to_string(),
                email: email.to_string(),
                created_at: chrono::Utc::now(),
            };
            users.push(user.clone());
            Ok(user)
        }

        async fn update(&self, id: i64, name: &str) -> Result<User, DomainError> {
            let mut users = self.users.lock().unwrap();
            let user = users.iter_mut().find(|u| u.id == id)
                .ok_or(DomainError::NotFound { id })?;
            user.name = name.to_string();
            Ok(user.clone())
        }

        async fn delete(&self, id: i64) -> Result<(), DomainError> {
            let mut users = self.users.lock().unwrap();
            users.retain(|u| u.id != id);
            Ok(())
        }
    }

    struct NoopEmailPort;

    #[async_trait::async_trait]
    impl EmailPort for NoopEmailPort {
        async fn send_welcome(&self, _email: &str, _name: &str) -> Result<(), DomainError> {
            Ok(())
        }
    }

    #[tokio::test]
    async fn test_create_user() {
        let svc = UserServiceImpl::new(
            MockUserRepository::new(),
            NoopEmailPort,
        );
        let user = svc
            .create_user(CreateUserRequest {
                name: "Alice".to_string(),
                email: "alice@example.com".to_string(),
            })
            .await
            .unwrap();
        assert_eq!(user.name, "Alice");
    }

    #[tokio::test]
    async fn test_get_user_not_found() {
        let svc = UserServiceImpl::new(
            MockUserRepository::new(),
            NoopEmailPort,
        );
        let result = svc.get_user(999).await;
        assert!(matches!(result, Err(DomainError::NotFound { .. })));
    }
}
```

---

## 6. 빌드 확인

생성 완료 후 안내한다:

> `cargo build`로 컴파일 에러를 확인하세요.
> 테스트를 실행하려면: `cargo test` 또는 `cargo nextest run` (HAS_NEXTEST)

## After Creation

1. 생성/수정된 파일 목록 출력.
2. `mod.rs` 등록이 누락된 파일이 없는지 확인한다.
3. 다음 단계 안내:
   - API 핸들러에 서비스를 주입하려면 `rust-api` 스킬을 사용하세요. 핸들러는 `Arc<dyn UserService>`를 `State`로 받습니다.
   - DB 모델과 Repository가 아직 없다면 먼저 `rust-model` 스킬로 생성하세요.

# References

- references/project-detection.md
- templates/rust-service.rs.template — 서비스 레이어 템플릿
