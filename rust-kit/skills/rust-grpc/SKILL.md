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
3. **streaming RPC는 `Pin<Box<dyn Stream>>` 반환** — streaming 메서드의 연관 타입 `type ...Stream`을 반드시 정의해야 한다. `tokio_stream::wrappers::ReceiverStream`으로 채널 기반 스트리밍을 구현한다. `impl Stream`을 직접 반환하는 패턴은 tonic 0.14에서도 지원하지 않는다 (tonic이 object-safe server trait을 유지하기 위함).
4. **`#[tonic::async_trait]` 유지** — Axum 0.8이 `#[async_trait]`을 제거한 것과 달리 **tonic 0.14의 사용자 impl은 여전히 `#[tonic::async_trait]` 매크로를 요구**한다. tonic이 코드 생성하는 Server trait이 dyn 호환을 유지하기 위해 `async_trait` 매크로 기반의 `Pin<Box<dyn Future>>` 시그니처를 사용한다. 네이티브 async fn in trait로 교체하지 마라 — 컴파일 에러가 난다.
5. **tonic-health / tonic-reflection은 별도 크레이트** — gRPC health checking protocol과 reflection은 `tonic` 본체에 포함되지 않는다. 필요하면 `tonic-health = "0.13"`, `tonic-reflection = "0.13"`을 별도로 추가한다.

# Process

## Gotchas

- **proto 파일 경로를 build.rs에서 잘못 지정하지 마라** — `tonic_build::compile_protos("proto/service.proto")`의 경로는 Cargo.toml 기준 상대경로다. workspace 루트가 아니라 크레이트 루트 기준임을 확인하라.
- **build.rs에 `tonic-build` 의존성을 `[build-dependencies]`에 넣어야 한다** — `[dependencies]`에 넣으면 런타임 바이너리에 protobuf 컴파일러가 포함된다. 반드시 `[build-dependencies]`에 배치하라.
- **protoc 바이너리 미설치를 간과하지 마라** — `tonic-build`는 시스템에 `protoc`가 설치되어 있어야 한다. CI/Docker에서 빌드 실패하면 `apt install protobuf-compiler` 또는 `prost-build`의 `protoc` feature로 번들링하라.
- **streaming RPC와 unary RPC의 반환 타입을 혼동하지 마라** — unary는 `Result<Response<T>, Status>`, server streaming은 `Result<Response<ReceiverStream<Result<T, Status>>>, Status>`다. 반환 타입이 틀리면 컴파일은 되지만 클라이언트가 데이터를 못 받는다.
- **proto 파일에서 package를 빠뜨리지 마라** — `package myapp.v1;` 없이 service를 정의하면 생성된 Rust 모듈 경로가 예측 불가능해진다. 항상 versioned package를 명시하라.
- **reflection 서비스를 프로덕션에 무조건 포함하지 마라** — `tonic_reflection::server::Builder`는 개발/디버깅용이다. 프로덕션에서는 feature flag로 감싸거나 제거하라. API 스키마가 외부에 노출된다.
- **gRPC 상태 코드를 HTTP 상태 코드처럼 사용하지 마라** — `Status::not_found()`는 리소스 부재, `Status::invalid_argument()`는 입력 검증 실패다. `Status::internal()`을 모든 에러에 쓰면 클라이언트가 재시도 판단을 못 한다.
- **proto import 경로를 include에 등록하지 않으면 안 된다** — `tonic_build::configure().proto_path("proto/")` 없이 다른 proto를 import하면 "file not found" 에러가 발생한다. 모든 proto 디렉토리를 `.proto_path()`에 등록하라.
- **메시지 필드에 `optional`을 빠뜨려 breaking change를 만들지 마라** — proto3에서 필드를 추가할 때 `optional` 없이 추가하면 기존 클라이언트가 디코딩 시 기본값을 받는다. 하위 호환성을 위해 새 필드는 항상 `optional`로 선언하라.
- **tonic 서버의 TCP listener 주소를 localhost로만 바인딩하지 마라** — Docker/k8s 환경에서 `127.0.0.1`로 바인딩하면 컨테이너 외부에서 접근 불가다. `0.0.0.0:50051`로 바인딩하고 네트워크 정책으로 접근을 제한하라.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 `ARCH`, `IS_WORKSPACE`, `HAS_TONIC` 등을 파악한다.

## 1. 서비스/RPC 확인

사용자에게 다음을 확인한다:
- 서비스 이름 (PascalCase, e.g. `UserService`)
- RPC 메서드 이름과 요청/응답 타입
- 스트리밍 종류: unary / server streaming / client streaming / bidirectional

## 2. 의존성 추가

`HAS_TONIC`이 false이면 `Cargo.toml`에 추가한다 (2026-04 기준 안정 버전):

```toml
[dependencies]
tonic = "0.14"
prost = "0.14"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
tokio-stream = "0.1"
# 선택 — gRPC health check / reflection protocol
# tonic-health = "0.14"
# tonic-reflection = "0.14"

[build-dependencies]
tonic-build = "0.14"
```

상위 minor/patch가 이미 나왔는지는 [tonic CHANGELOG](https://github.com/hyperium/tonic/blob/master/CHANGELOG.md) 또는 `cargo search tonic`으로 재확인한다.

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
