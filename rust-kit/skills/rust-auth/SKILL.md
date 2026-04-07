---
name: rust-auth
description: >
  JWT/OAuth 인증 레이어를 생성한다. AuthProvider trait(포트) 정의 →
  jsonwebtoken 기반 impl(어댑터) → Axum extractor 순서로 헥사고날 패턴을 따른다.
  "인증 추가", "JWT", "로그인", "OAuth", "auth", "rust auth" 같은 요청 시 트리거.
argument-hint: "[jwt|oauth|refresh]"
user-invocable: true
---

# Gotchas

1. **JWT 시크릿 하드코딩 금지** — `JWT_SECRET`은 반드시 환경변수에서 로드한다. `.env.example`에 키 이름만 남긴다.
2. **exp 중복 검사 금지** — `jsonwebtoken::decode`는 `exp` 클레임을 자동으로 검증한다. 수동 만료 시간 비교를 추가하면 로직 중복이 된다.
3. **refresh token은 반드시 DB 저장** — refresh token을 메모리나 JWT 페이로드에 넣으면 무효화(로그아웃, 탈취 대응)가 불가능하다. `refresh_tokens` 테이블 또는 Redis에 저장한다.

# Process

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 `ARCH`, `IS_WORKSPACE`, `HAS_JSONWEBTOKEN`, `HAS_AXUM` 등을 파악한다.

## 1. 인증 방식 확인

사용자에게 인증 방식을 확인한다:
- **JWT only** — access token 발급/검증만
- **JWT + refresh** — access token + refresh token (DB 저장)
- **OAuth + JWT** — OAuth provider 연동 후 JWT 발급

## 2. 기존 auth 패턴 확인

이미 auth 관련 코드가 있으면 읽어 패턴을 파악한다:
- Claims 구조체 정의 위치
- 에러 타입 (`AppError` 등)
- 기존 미들웨어 스택

없으면 ARCH에 따라 아래 경로에 새로 생성한다.

## 3. AuthProvider trait (포트) 정의

JWT 라이브러리 타입을 domain에 노출하지 않는다. domain/ports에 순수 인터페이스만 정의한다.

### ARCH = workspace_service / hexagonal

`crates/domain/src/ports/auth.rs`:

```rust
use async_trait::async_trait;
use crate::errors::DomainError;

#[derive(Debug, Clone)]
pub struct Claims {
    pub sub: String,       // user_id
    pub email: String,
    pub exp: i64,
    pub iat: i64,
}

#[derive(Debug, Clone)]
pub struct TokenPair {
    pub access_token: String,
    pub refresh_token: String,
}

#[async_trait]
pub trait AuthProvider: Send + Sync {
    fn generate_access_token(&self, claims: &Claims) -> Result<String, DomainError>;
    fn validate_token(&self, token: &str) -> Result<Claims, DomainError>;
    async fn generate_refresh_token(&self, user_id: &str) -> Result<TokenPair, DomainError>;
    async fn rotate_refresh_token(&self, refresh_token: &str) -> Result<TokenPair, DomainError>;
    async fn revoke_refresh_token(&self, refresh_token: &str) -> Result<(), DomainError>;
}
```

### ARCH = modular / flat

`src/domain/ports/auth.rs` (modular) 또는 `src/auth.rs` (flat)에 동일한 trait을 정의한다.

## 4. JWT impl (어댑터) 생성

jsonwebtoken 의존은 이 레이어에만 존재한다.

### ARCH = workspace_service / hexagonal

`crates/infra/src/adapters/auth.rs`:

```rust
use async_trait::async_trait;
use jsonwebtoken::{decode, encode, Algorithm, DecodingKey, EncodingKey, Header, Validation};
use domain::ports::auth::{AuthProvider, Claims, TokenPair};
use domain::errors::DomainError;

pub struct JwtAuthProvider {
    encoding_key: EncodingKey,
    decoding_key: DecodingKey,
    access_token_ttl_secs: i64,
    // refresh_token_store: Arc<dyn RefreshTokenStore>,
}

impl JwtAuthProvider {
    pub fn from_env() -> Self {
        let secret = std::env::var("JWT_SECRET")
            .expect("JWT_SECRET must be set");
        Self {
            encoding_key: EncodingKey::from_secret(secret.as_bytes()),
            decoding_key: DecodingKey::from_secret(secret.as_bytes()),
            access_token_ttl_secs: 3600,
        }
    }
}

#[async_trait]
impl AuthProvider for JwtAuthProvider {
    fn generate_access_token(&self, claims: &Claims) -> Result<String, DomainError> {
        encode(&Header::default(), claims, &self.encoding_key)
            .map_err(|e| DomainError::Auth(e.to_string()))
    }

    fn validate_token(&self, token: &str) -> Result<Claims, DomainError> {
        decode::<Claims>(token, &self.decoding_key, &Validation::new(Algorithm::HS256))
            .map(|data| data.claims)
            .map_err(|e| DomainError::Auth(e.to_string()))
    }

    // refresh token 구현은 DB/Redis 어댑터와 조합
    async fn generate_refresh_token(&self, _user_id: &str) -> Result<TokenPair, DomainError> {
        todo!("refresh_token_store 연동 필요")
    }

    async fn rotate_refresh_token(&self, _refresh_token: &str) -> Result<TokenPair, DomainError> {
        todo!("refresh_token_store 연동 필요")
    }

    async fn revoke_refresh_token(&self, _refresh_token: &str) -> Result<(), DomainError> {
        todo!("refresh_token_store 연동 필요")
    }
}
```

### ARCH = modular / flat

`src/infra/adapters/auth.rs` (modular) 또는 `src/auth_adapter.rs` (flat)에 동일 패턴으로 생성한다.

## 5. Axum extractor 생성

핸들러에서 `AuthUser`를 파라미터로 선언하면 자동 검증된다.

```rust
// 위치: ARCH에 따라 crates/api/src/extractors/auth.rs 또는 src/api/extractors/auth.rs
use axum::{
    async_trait,
    extract::FromRequestParts,
    http::{request::Parts, StatusCode},
    RequestPartsExt,
};
use axum_extra::{
    headers::{authorization::Bearer, Authorization},
    TypedHeader,
};
use std::sync::Arc;
use domain::ports::auth::{AuthProvider, Claims};

pub struct AuthUser(pub Claims);

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, &'static str);

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let TypedHeader(Authorization(bearer)) = parts
            .extract::<TypedHeader<Authorization<Bearer>>>()
            .await
            .map_err(|_| (StatusCode::UNAUTHORIZED, "Missing Authorization header"))?;

        // State에서 AuthProvider 주입 (App 상태에 Arc<dyn AuthProvider> 등록 필요)
        let auth = parts
            .extensions
            .get::<Arc<dyn AuthProvider>>()
            .ok_or((StatusCode::INTERNAL_SERVER_ERROR, "AuthProvider not configured"))?;

        let claims = auth
            .validate_token(bearer.token())
            .map_err(|_| (StatusCode::UNAUTHORIZED, "Invalid or expired token"))?;

        Ok(AuthUser(claims))
    }
}
```

## 6. 환경변수 안내

`.env.example`에 다음을 추가하도록 안내한다:

```
JWT_SECRET=your-secret-key-min-32-chars
JWT_ACCESS_TTL_SECS=3600
JWT_REFRESH_TTL_SECS=604800
```

# After Creation

1. 생성/수정된 파일 목록을 출력한다.
2. 다음 단계를 안내한다:
   > - `cargo build`로 컴파일 확인
   > - `.env`에 `JWT_SECRET` 설정
   > - 핸들러에 `AuthUser` extractor 추가: `async fn protected(auth: AuthUser, ...) { ... }`
   > - refresh token이 필요하면 DB 어댑터 연동: `/rust-model`로 `refresh_tokens` 테이블 생성

# References

- references/project-detection.md
