---
title: gRPC 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# gRPC 원칙

`tonic 0.14.x`는 Rust의 표준 gRPC 구현이다. `.proto` 파일에서 `tonic-prost-build`로 서버/클라이언트 코드를 생성하고, tokio 위에서 비동기로 동작한다.

---

## 원칙

### 1. `build.rs`에서 proto 파일을 컴파일한다

```toml
[dependencies]
tonic = "0.14"
prost = "0.13"

[build-dependencies]
tonic-prost-build = "0.14"
```

```rust
// build.rs
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_prost_build::configure()
        .build_server(true)
        .build_client(true)
        .compile_protos(
            &["proto/user.proto"],
            &["proto/"],
        )?;
    Ok(())
}
```

```protobuf
// proto/user.proto
syntax = "proto3";
package user;

service UserService {
    rpc GetUser (GetUserRequest) returns (UserResponse);
    rpc ListUsers (ListUsersRequest) returns (stream UserResponse);
    rpc CreateUser (CreateUserRequest) returns (UserResponse);
}

message GetUserRequest { string id = 1; }
message UserResponse {
    string id = 1;
    string email = 2;
    string name = 3;
}
```

### 2. 생성된 trait을 구현하여 서버를 만든다

```rust
use tonic::{transport::Server, Request, Response, Status};

// build.rs가 생성한 모듈 포함
pub mod user {
    tonic::include_proto!("user");
}
use user::user_service_server::{UserService, UserServiceServer};

#[derive(Debug, Default)]
pub struct UserServiceImpl {
    db: Arc<dyn DatabasePort>,
}

#[tonic::async_trait]
impl UserService for UserServiceImpl {
    async fn get_user(
        &self,
        request: Request<GetUserRequest>,
    ) -> Result<Response<UserResponse>, Status> {
        let id = request.into_inner().id;
        let user = self.db.find_user(&id).await
            .map_err(|e| Status::internal(e.to_string()))?
            .ok_or_else(|| Status::not_found("User not found"))?;

        Ok(Response::new(UserResponse {
            id: user.id.to_string(),
            email: user.email,
            name: user.name,
        }))
    }

    // 서버 스트리밍
    type ListUsersStream = Pin<Box<dyn Stream<Item = Result<UserResponse, Status>> + Send>>;

    async fn list_users(
        &self,
        _request: Request<ListUsersRequest>,
    ) -> Result<Response<Self::ListUsersStream>, Status> {
        let users = self.db.list_all_users().await
            .map_err(|e| Status::internal(e.to_string()))?;

        let stream = futures::stream::iter(users.into_iter().map(|u| {
            Ok(UserResponse { id: u.id.to_string(), email: u.email, name: u.name })
        }));
        Ok(Response::new(Box::pin(stream)))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let svc = UserServiceImpl::default();

    Server::builder()
        .add_service(UserServiceServer::new(svc))
        .serve(addr)
        .await?;
    Ok(())
}
```

### 3. `tonic::Status`로 gRPC 에러를 표현한다

```rust
// 표준 Status 생성자
Status::ok("success")
Status::not_found("User not found")
Status::invalid_argument("Email is required")
Status::unauthenticated("Invalid token")
Status::permission_denied("Insufficient permissions")
Status::internal("Database error")
Status::unavailable("Service temporarily unavailable")
Status::already_exists("Email already registered")

// 메타데이터 포함
let mut status = Status::invalid_argument("Validation failed");
status.metadata_mut().insert("x-request-id", request_id.parse()?);
Err(status)
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| tonic 버전 | 0.14.x | prost 0.13과 호환 |
| tonic-prost-build 버전 | 0.14.x | build-dependencies |
| 기본 포트 | 50051 | gRPC 관례 |
| 최대 메시지 크기 | 4MB (기본) | `Server::builder().max_decoding_message_size()` |

---

## 안티패턴

### proto 파일 없이 수동으로 타입 정의

tonic은 `.proto` 파일에서 타입과 서비스 코드를 생성한다. Rust 구조체를 직접 작성하면 proto 스키마와 불일치가 생긴다. 항상 `.proto` → codegen → 구현 순서를 따른다.

### `Status::internal`에 민감한 정보 포함

내부 에러 메시지(DB 에러, 스택 트레이스)를 `Status::internal()`에 직접 넣으면 클라이언트에 노출된다. 서버 로그에 상세 내용을 기록하고 클라이언트에는 일반 메시지만 반환한다.

### 스트리밍 핸들러에서 전체 데이터를 메모리에 수집 후 반환

`Vec` 전체를 수집한 뒤 스트림으로 변환하면 스트리밍의 이점이 없다. `futures::stream::try_unfold`나 DB cursor를 활용하여 진짜 스트리밍을 구현한다.

---

## Gotchas

### `tonic::include_proto!`의 인자는 패키지명이다

`tonic::include_proto!("user")`의 인자는 파일명이 아니라 `.proto` 파일 내 `package user;` 선언의 패키지명이다.

### `build.rs` 변경 후 `cargo clean`이 필요할 수 있다

proto 파일을 수정했는데 변경이 반영되지 않으면 `cargo clean && cargo build`로 생성 코드를 재생성한다.

### 서버 스트리밍의 반환 타입은 associated type으로 선언해야 한다

`type ListUsersStream = Pin<Box<dyn Stream<Item = Result<UserResponse, Status>> + Send>>`처럼 associated type을 명시해야 한다. async_trait과 달리 tonic은 이 패턴을 직접 요구한다.

### tonic 인터셉터로 인증을 공통 처리한다

```rust
Server::builder()
    .add_service(UserServiceServer::with_interceptor(svc, check_auth))
```

`check_auth`는 `fn(Request<()>) -> Result<Request<()>, Status>` 시그니처다.
