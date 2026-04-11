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
