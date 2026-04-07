---
name: rust-grpc
description: >
  tonic gRPC 서비스를 생성한다. proto 파일 → build.rs → gRPC 서비스 trait(포트) 정의 →
  tonic impl(어댑터) 순서로 헥사고날 패턴을 따른다.
  "gRPC 추가", "proto 파일", "tonic", "rust grpc" 같은 요청 시 트리거.
argument-hint: "<service-name>"
user-invocable: true
---

# Gotchas

1. **`protoc` 시스템 설치 필요** — `tonic-build`는 `protoc`를 자체 포함하지 않는다. `prost-build`의 `protoc` 자동 다운로드 기능(`PROTOC_NO_VENDOR=0`)을 쓰거나, `protoc-bin-vendored` 크레이트를 사용한다. 설치 여부를 먼저 확인한다 (`protoc --version`).
2. **proto 경로와 `build.rs` 인자 일치 필수** — `compile_protos(&["proto/foo.proto"], &["proto"])` 에서 첫 번째 인자(파일 경로)와 두 번째 인자(include 디렉토리)가 실제 파일 시스템 경로와 정확히 일치해야 한다. 경로 불일치는 `file not found` 컴파일 에러로 나타난다.
3. **streaming RPC는 `Pin<Box<dyn Stream>>` 반환** — streaming 메서드의 연관 타입 `type ...Stream`을 반드시 정의해야 한다. `tokio_stream::wrappers::ReceiverStream`으로 채널 기반 스트리밍을 구현한다. `impl Stream`을 직접 반환하는 패턴은 tonic 0.12에서 지원하지 않는다.

# Process

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 `ARCH`, `IS_WORKSPACE`, `HAS_TONIC` 등을 파악한다.

## 1. 서비스/RPC 확인

사용자에게 다음을 확인한다:
- 서비스 이름 (PascalCase, e.g. `UserService`)
- RPC 메서드 이름과 요청/응답 타입
- 스트리밍 종류: unary / server streaming / client streaming / bidirectional

## 2. 의존성 추가

`HAS_TONIC`이 false이면 `Cargo.toml`에 추가한다.

```toml
[dependencies]
tonic = "0.12.3"
prost = "0.13.5"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
tokio-stream = "0.1"

[build-dependencies]
tonic-build = "0.12.3"
```

## 3. gRPC 서비스 trait (포트) 정의

tonic 생성 타입(Request, Response, Status 등)을 domain에 노출하지 않는다. domain/ports에는 순수 비즈니스 인터페이스만 정의한다.

### ARCH = workspace_service / hexagonal

`crates/domain/src/ports/user_grpc.rs` (서비스명에 맞게 조정):

```rust
use async_trait::async_trait;
use crate::errors::DomainError;
use crate::models::user::User;

/// gRPC 서비스가 의존하는 비즈니스 로직 포트.
/// tonic 생성 타입(Request, Status 등)을 포함하지 않는다.
#[async_trait]
pub trait UserGrpcPort: Send + Sync {
    async fn get_user(&self, user_id: &str) -> Result<User, DomainError>;
    async fn list_users(&self) -> Result<Vec<User>, DomainError>;
}
```

### ARCH = modular / flat

`src/domain/ports/user_grpc.rs` (modular) 또는 `src/ports.rs` (flat)에 동일 trait 정의.

## 4. proto 파일 생성

`proto/{service_name}.proto` (snake_case 파일명):

```proto
syntax = "proto3";

package user;

service UserService {
  rpc GetUser (GetUserRequest) returns (UserResponse);
  rpc ListUsers (ListUsersRequest) returns (stream UserResponse);
}

message GetUserRequest {
  string user_id = 1;
}

message ListUsersRequest {}

message UserResponse {
  string id = 1;
  string email = 2;
  string name = 3;
}
```

## 5. build.rs 설정

프로젝트 루트(또는 gRPC 서비스를 담당하는 크레이트 루트)에 `build.rs`를 생성한다:

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::configure()
        .build_server(true)
        .build_client(false)  // 클라이언트 코드가 필요하면 true
        .compile_protos(&["proto/user.proto"], &["proto"])?;
    Ok(())
}
```

`protoc`가 설치되지 않은 환경이면 `protoc-bin-vendored`를 `build-dependencies`에 추가하고 다음과 같이 설정한다:

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let protoc = protoc_bin_vendored::protoc_bin_path().unwrap();
    std::env::set_var("PROTOC", protoc);
    tonic_build::configure()
        .compile_protos(&["proto/user.proto"], &["proto"])?;
    Ok(())
}
```

## 6. tonic impl (어댑터) 생성

tonic 의존은 이 레이어에만 존재한다.

### ARCH = workspace_service / hexagonal

`crates/infra/src/adapters/user_grpc.rs`:

```rust
use std::pin::Pin;
use std::sync::Arc;

use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tokio_stream::Stream;
use tonic::{Request, Response, Status};

use domain::ports::user_grpc::UserGrpcPort;

// build.rs로 생성된 코드 포함 (크레이트명은 실제 패키지명으로 조정)
pub mod user_proto {
    tonic::include_proto!("user");
}

use user_proto::user_service_server::UserService;
use user_proto::{GetUserRequest, ListUsersRequest, UserResponse};

pub struct UserGrpcAdapter {
    port: Arc<dyn UserGrpcPort>,
}

impl UserGrpcAdapter {
    pub fn new(port: Arc<dyn UserGrpcPort>) -> Self {
        Self { port }
    }
}

#[tonic::async_trait]
impl UserService for UserGrpcAdapter {
    async fn get_user(
        &self,
        request: Request<GetUserRequest>,
    ) -> Result<Response<UserResponse>, Status> {
        let user_id = &request.into_inner().user_id;
        let user = self.port.get_user(user_id).await
            .map_err(|e| Status::not_found(e.to_string()))?;

        Ok(Response::new(UserResponse {
            id: user.id,
            email: user.email,
            name: user.name,
        }))
    }

    type ListUsersStream =
        Pin<Box<dyn Stream<Item = Result<UserResponse, Status>> + Send + 'static>>;

    async fn list_users(
        &self,
        _request: Request<ListUsersRequest>,
    ) -> Result<Response<Self::ListUsersStream>, Status> {
        let port = Arc::clone(&self.port);
        let (tx, rx) = mpsc::channel(16);

        tokio::spawn(async move {
            match port.list_users().await {
                Ok(users) => {
                    for user in users {
                        let msg = UserResponse {
                            id: user.id,
                            email: user.email,
                            name: user.name,
                        };
                        if tx.send(Ok(msg)).await.is_err() {
                            break;
                        }
                    }
                }
                Err(e) => {
                    let _ = tx.send(Err(Status::internal(e.to_string()))).await;
                }
            }
        });

        Ok(Response::new(Box::pin(ReceiverStream::new(rx))))
    }
}
```

### ARCH = modular / flat

`src/infra/adapters/user_grpc.rs` (modular) 또는 `src/grpc_adapter.rs` (flat)에 동일 패턴으로 생성.

## 7. 서버 등록 안내

`main.rs` 또는 서버 초기화 파일에 gRPC 서버를 등록하도록 안내한다:

```rust
use tonic::transport::Server;
use infra::adapters::user_grpc::{UserGrpcAdapter, user_proto::user_service_server::UserServiceServer};

Server::builder()
    .add_service(UserServiceServer::new(UserGrpcAdapter::new(port)))
    .serve("0.0.0.0:50051".parse()?)
    .await?;
```

## 8. 빌드 확인 안내

> `cargo build`를 실행하세요. tonic-build가 proto를 컴파일하여 Rust 코드를 자동 생성합니다.
> `protoc` 관련 에러가 나오면 Gotcha #1을 확인하세요.

# After Creation

1. 생성/수정된 파일 목록을 출력한다.
2. 다음 단계를 안내한다:
   > - `cargo build`로 proto 코드 생성 확인
   > - `protoc` 미설치 시: `cargo add protoc-bin-vendored --build`
   > - gRPC 클라이언트 테스트: `grpcurl` 또는 `cargo test`
   > - 서비스 테스트: `/rust-test`로 mock 기반 단위 테스트 생성

# References

- references/project-detection.md
