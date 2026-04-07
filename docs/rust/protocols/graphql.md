---
title: GraphQL 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# GraphQL 원칙

`async-graphql 7.x`는 Rust의 코드 퍼스트 GraphQL 라이브러리다. `#[Object]`, `#[SimpleObject]`, `#[InputObject]` 매크로로 스키마를 정의하고, `DataLoader`로 N+1 문제를 해결한다.

---

## 원칙

### 1. Schema는 Query/Mutation/Subscription 세 루트 타입으로 구성한다

```toml
[dependencies]
async-graphql = "7"
async-graphql-axum = "7"
```

```rust
use async_graphql::{Schema, EmptySubscription, EmptyMutation, Object, Context, Result};

pub struct QueryRoot;

#[Object]
impl QueryRoot {
    async fn user(&self, ctx: &Context<'_>, id: ID) -> Result<Option<User>> {
        let db = ctx.data_unchecked::<Arc<dyn DatabasePort>>();
        Ok(db.find_user(&id.to_string()).await?)
    }

    async fn users(&self, ctx: &Context<'_>) -> Result<Vec<User>> {
        let db = ctx.data_unchecked::<Arc<dyn DatabasePort>>();
        Ok(db.list_users().await?)
    }
}

pub struct MutationRoot;

#[Object]
impl MutationRoot {
    async fn create_user(
        &self,
        ctx: &Context<'_>,
        input: CreateUserInput,
    ) -> Result<User> {
        let db = ctx.data_unchecked::<Arc<dyn DatabasePort>>();
        Ok(db.create_user(input.into()).await?)
    }
}

pub type AppSchema = Schema<QueryRoot, MutationRoot, EmptySubscription>;

pub fn build_schema(db: Arc<dyn DatabasePort>) -> AppSchema {
    Schema::build(QueryRoot, MutationRoot, EmptySubscription)
        .data(db)
        .finish()
}
```

### 2. `#[SimpleObject]`와 `#[InputObject]`로 DTO를 선언한다

```rust
use async_graphql::{SimpleObject, InputObject, ID};

// 응답 타입 — 자동으로 모든 필드를 GraphQL 필드로 노출
#[derive(SimpleObject)]
pub struct User {
    pub id: ID,
    pub email: String,
    pub name: String,
    #[graphql(skip)]  // GraphQL에 노출하지 않을 필드
    pub password_hash: String,
}

// 입력 타입
#[derive(InputObject)]
pub struct CreateUserInput {
    pub email: String,
    pub name: String,
    pub password: String,
}
```

### 3. `DataLoader`로 N+1 쿼리를 해결한다

관계 필드에서 매 resolver마다 DB를 호출하면 N+1 문제가 발생한다. `DataLoader`는 동일 배치 내 요청을 한 번의 쿼리로 묶는다.

```rust
use async_graphql::dataloader::{DataLoader, Loader};
use std::collections::HashMap;

pub struct UserLoader {
    db: Arc<dyn DatabasePort>,
}

#[async_trait::async_trait]
impl Loader<String> for UserLoader {
    type Value = User;
    type Error = anyhow::Error;

    async fn load(&self, keys: &[String]) -> Result<HashMap<String, Self::Value>, Self::Error> {
        let users = self.db.find_users_by_ids(keys).await?;
        Ok(users.into_iter().map(|u| (u.id.to_string(), u)).collect())
    }
}

// Schema 빌드 시 DataLoader 등록
Schema::build(QueryRoot, MutationRoot, EmptySubscription)
    .data(DataLoader::new(UserLoader { db: db.clone() }, tokio::spawn))
    .data(db)
    .finish()

// Resolver에서 사용
#[Object]
impl Post {
    async fn author(&self, ctx: &Context<'_>) -> Result<Option<User>> {
        let loader = ctx.data_unchecked::<DataLoader<UserLoader>>();
        Ok(loader.load_one(self.author_id.clone()).await?)
    }
}
```

### 4. axum에 GraphQL 엔드포인트를 마운트한다

```rust
use async_graphql_axum::{GraphQLRequest, GraphQLResponse, GraphQLSubscription};

async fn graphql_handler(
    schema: Extension<AppSchema>,
    req: GraphQLRequest,
) -> GraphQLResponse {
    schema.execute(req.into_inner()).await.into()
}

pub fn create_router(schema: AppSchema) -> Router {
    Router::new()
        .route("/graphql", post(graphql_handler))
        .route("/graphql/ws", any(GraphQLSubscription::new(schema.clone())))
        .layer(Extension(schema))
}
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| async-graphql 버전 | 7.x | async-graphql-axum도 동일 버전 |
| DataLoader 배치 크기 | 기본값 (자동) | 동일 async 배치 내 요청 자동 묶음 |
| 쿼리 복잡도 제한 | `.limit_complexity(100)` | DoS 방지 |
| 쿼리 깊이 제한 | `.limit_depth(10)` | 중첩 쿼리 방지 |

---

## 안티패턴

### `#[Object]` resolver에서 직접 DB 호출로 N+1 발생

관계 필드마다 DB를 호출하면 100개 Post의 author를 조회할 때 101번의 쿼리가 발생한다. 항상 `DataLoader`를 사용한다.

### `ctx.data::<T>()` 대신 `data_unchecked::<T>()` 남용

`data_unchecked`는 데이터가 없으면 패닉한다. Schema 빌드 시 반드시 등록된 데이터에만 사용하고, 조건부로 존재하는 데이터는 `ctx.data::<T>()` (Result 반환)를 사용한다.

### 복잡도/깊이 제한 없이 프로덕션 배포

GraphQL은 임의로 중첩된 쿼리를 허용하므로 DoS 공격에 취약하다. `Schema::build(...).limit_complexity(100).limit_depth(10)` 설정을 반드시 추가한다.

---

## Gotchas

### `#[SimpleObject]`의 모든 public 필드가 자동으로 노출된다

민감한 필드(password_hash, internal_id 등)는 `#[graphql(skip)]`으로 명시적으로 제외한다.

### `DataLoader`는 같은 async 배치 내 요청만 묶는다

resolver들이 `await`로 중단되지 않고 동일 poll 사이클에서 실행되어야 배치가 묶인다. `tokio::spawn`을 executor로 전달하면 배치 타이밍이 최적화된다.

### `async-graphql`과 `async-graphql-axum` 버전을 반드시 맞춰야 한다

버전이 다르면 `Schema` 타입이 호환되지 않아 컴파일 에러가 발생한다.

### `ID` 타입은 내부적으로 `String`이다

`async_graphql::ID`는 GraphQL spec의 ID 스칼라 타입이다. DB의 `Uuid`를 `ID`로 변환할 때 `ID::from(uuid.to_string())`을 사용한다.
