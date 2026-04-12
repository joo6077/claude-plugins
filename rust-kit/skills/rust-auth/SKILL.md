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
4. **Axum 0.8 `FromRequestParts`는 native async fn** — `#[async_trait]`과 `use axum::async_trait`을 더 이상 사용하지 않는다. `impl<S> FromRequestParts<S> for AuthUser where S: Send + Sync { type Rejection = ...; async fn from_request_parts(parts: &mut Parts, state: &S) -> Result<Self, Self::Rejection> { ... } }` 형태로 직접 선언한다. 0.7 코드에서 마이그레이션할 때는 `#[async_trait]` 어노테이션과 `use axum::async_trait;` import를 함께 제거한다.
5. **jsonwebtoken 10.x `rust_crypto` feature** — `jsonwebtoken = { version = "10", features = ["rust_crypto"] }`로 고정하면 OpenSSL 동적 링크 없이 pure Rust crypto를 사용한다. Docker scratch/distroless 이미지 호환성이 좋다. fit-pal 실무 기준.
6. **`OptionalFromRequestParts`로 optional auth 처리** — Axum 0.8의 `OptionalFromRequestParts` trait을 사용하면 `Option<AuthUser>` extractor가 rejection을 에러 응답으로 변환할 수 있다. 기존에는 rejection이 무조건 `None`으로 변환되어 "토큰이 잘못된 건지 없는 건지" 디버깅이 어려웠다. 공개 API + 인증 사용자 추가 기능 패턴에서 유용하다.

# Process

## Gotchas

- **시크릿을 소스코드에 하드코딩하지 마라** — JWT signing key, OAuth client secret을 `const`나 `static`으로 박으면 git history에 영구 노출된다. 반드시 `std::env::var("JWT_SECRET")` 또는 `.env` 파일에서 로드하라.
- **토큰 만료 시간을 누락하지 마라** — `exp` 클레임 없이 JWT를 발급하면 토큰이 영원히 유효하다. access token은 15분~1시간, refresh token은 7~30일로 반드시 설정하라.
- **refresh token rotation을 빠뜨리지 마라** — refresh token 사용 시 기존 토큰을 무효화하고 새 토큰을 발급하라. 단일 refresh token을 재사용하면 탈취 시 무한 액세스가 가능하다.
- **비밀번호 해싱에 SHA-256을 사용하지 마라** — `argon2`, `bcrypt`, `scrypt` 같은 비용 기반 해시를 사용하라. SHA 계열은 무차별 대입에 취약하다. `password_hash` 크레이트의 `PasswordHasher` 트레이트를 권장한다.
- **HMAC과 RSA 알고리즘을 혼동하지 마라** — `jsonwebtoken` 크레이트에서 `Algorithm::HS256`으로 서명한 토큰을 `RS256` 키로 검증하면 항상 실패한다. 발급과 검증에 동일한 알고리즘+키 쌍을 사용하라.
- **Authorization 헤더 파싱에서 "Bearer " 접두사를 빠뜨리지 마라** — `Authorization: Bearer <token>` 형식에서 "Bearer " 7글자를 strip하지 않으면 토큰 디코딩이 실패한다. 대소문자도 주의하라.
- **CORS와 인증 미들웨어 순서를 잘못 배치하지 마라** — CORS preflight(OPTIONS)는 인증 없이 통과해야 한다. 인증 미들웨어가 CORS보다 먼저 실행되면 preflight가 401을 반환한다.
- **에러 응답에 내부 정보를 노출하지 마라** — "Invalid password for user admin@example.com" 같은 메시지는 사용자 존재 여부를 확인시켜 준다. "Invalid credentials"로 통일하라.
- **OAuth state 파라미터를 검증하지 않으면 CSRF에 노출된다** — OAuth 콜백에서 `state` 값을 세션에 저장한 값과 비교하라. 생략하면 공격자가 자신의 계정을 피해자 세션에 연결할 수 있다.
- **middleware extractor 순서를 잘못 배치하지 마라** — Axum에서 `Claims` extractor가 `Json<Body>` 뒤에 오면 body가 이미 소비되어 파싱 에러가 발생한다. 인증 extractor는 항상 body extractor 앞에 배치하라.

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
        unimplemented!("예시 스켈레톤 — refresh_token_store 어댑터 연동 필요")
    }

    async fn rotate_refresh_token(&self, _refresh_token: &str) -> Result<TokenPair, DomainError> {
        unimplemented!("예시 스켈레톤 — refresh_token_store 어댑터 연동 필요")
    }

    async fn revoke_refresh_token(&self, _refresh_token: &str) -> Result<(), DomainError> {
        unimplemented!("예시 스켈레톤 — refresh_token_store 어댑터 연동 필요")
    }
}
```

### ARCH = modular / flat

`src/infra/adapters/auth.rs` (modular) 또는 `src/auth_adapter.rs` (flat)에 동일 패턴으로 생성한다.

## 5. Axum 0.8 extractor 생성

Axum 0.8부터 `FromRequestParts`는 **native `async fn in trait`**을 사용한다. `#[async_trait]` 매크로와 `use axum::async_trait` import는 **제거**한다.

```rust
// 위치: ARCH에 따라 apps/api/src/extractors/auth.rs 또는 src/api/extractors/auth.rs
use axum::{
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

// Axum 0.8 — #[async_trait] 제거, native async fn 사용
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

        // 권장: AuthProvider를 Router::with_state()로 주입하고 State<Arc<dyn AuthProvider>>를
        // 별도 파라미터로 받는 middleware fn 패턴을 사용하라. 여기서는 Extension 기반 예시.
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

> **Axum 0.7 → 0.8 마이그레이션 체크리스트**:
> 1. `use axum::async_trait;` 제거
> 2. `FromRequest`/`FromRequestParts` impl 블록의 `#[async_trait]` 어노테이션 제거
> 3. trait impl 블록 내부의 `async fn` 시그니처는 그대로 유지 (Rust 1.75+ RPIT in trait)
> 4. 라우트 문자열의 `:id` → `{id}` 치환 (rust-api 스킬 참조)

## 6. 환경변수 안내

`.env.example`에 다음을 추가하도록 안내한다:

```text
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
