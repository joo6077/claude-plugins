---
title: 인증 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 인증 원칙

`jsonwebtoken 10.x`를 사용한 JWT 기반 인증 패턴이다. access token과 refresh token을 분리하고, axum의 `FromRequestParts`로 인증된 사용자를 Extractor로 추출한다.

---

## 원칙

### 1. Claims는 표준 필드와 커스텀 필드를 함께 정의한다

```rust
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Claims {
    pub sub: String,          // subject (user id)
    pub exp: usize,           // expiration time (Unix timestamp)
    pub iat: usize,           // issued at
    pub jti: String,          // JWT ID (revocation 용)
    pub token_type: TokenType, // "access" | "refresh"
    pub roles: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
#[serde(rename_all = "lowercase")]
pub enum TokenType {
    Access,
    Refresh,
}
```

### 2. `EncodingKey`와 `DecodingKey`를 앱 시작 시 초기화한다

`jsonwebtoken 10.x`는 crypto backend feature를 요구한다. `Cargo.toml`에 `features = ["aws_lc_rs"]` 또는 `["ring"]`을 명시한다.

```toml
[dependencies]
jsonwebtoken = { version = "10", features = ["aws_lc_rs"] }
```

```rust
use jsonwebtoken::{encode, decode, Header, Validation, EncodingKey, DecodingKey, Algorithm};

pub struct JwtService {
    encoding_key: EncodingKey,
    decoding_key: DecodingKey,
    access_duration: Duration,
    refresh_duration: Duration,
}

impl JwtService {
    pub fn new(secret: &[u8]) -> Self {
        Self {
            encoding_key: EncodingKey::from_secret(secret),
            decoding_key: DecodingKey::from_secret(secret),
            access_duration: Duration::minutes(15),
            refresh_duration: Duration::days(30),
        }
    }

    pub fn issue_access_token(&self, user_id: &str, roles: Vec<String>) -> Result<String, JwtError> {
        let now = Utc::now();
        let claims = Claims {
            sub: user_id.to_string(),
            exp: (now + self.access_duration).timestamp() as usize,
            iat: now.timestamp() as usize,
            jti: Uuid::new_v4().to_string(),
            token_type: TokenType::Access,
            roles,
        };
        encode(&Header::default(), &claims, &self.encoding_key)
            .map_err(JwtError::Encode)
    }

    pub fn verify(&self, token: &str) -> Result<Claims, JwtError> {
        let validation = Validation::new(Algorithm::HS256);
        decode::<Claims>(token, &self.decoding_key, &validation)
            .map(|data| data.claims)
            .map_err(JwtError::Decode)
    }
}
```

### 3. `FromRequestParts`로 인증된 사용자를 Extractor로 추출한다

핸들러마다 토큰 검증 코드를 반복하지 않는다. `AuthUser` Extractor 하나로 통일한다.

```rust
use axum::{async_trait, extract::{FromRequestParts, State}, http::request::Parts};
use axum_extra::{TypedHeader, headers::{Authorization, authorization::Bearer}};

pub struct AuthUser(pub Claims);

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
    AppState: FromRef<S>,
{
    type Rejection = ApiError;

    async fn from_request_parts(parts: &mut Parts, state: &S) -> Result<Self, Self::Rejection> {
        let TypedHeader(Authorization(bearer)) =
            TypedHeader::<Authorization<Bearer>>::from_request_parts(parts, state)
                .await
                .map_err(|_| ApiError::Unauthorized("Bearer token required"))?;

        let app_state = AppState::from_ref(state);
        let claims = app_state.jwt.verify(bearer.token())
            .map_err(|_| ApiError::Unauthorized("Invalid token"))?;

        if claims.token_type != TokenType::Access {
            return Err(ApiError::Unauthorized("Access token required"));
        }

        Ok(AuthUser(claims))
    }
}
```

### 4. Refresh token은 rotation과 revocation을 함께 구현한다

Refresh token은 단순 JWT가 아니라 서버 저장소(Redis/DB)와 연동하여 관리한다. 매 갱신마다 새 토큰으로 교체(rotation)하고, 이전 토큰을 무효화한다.

```rust
pub async fn refresh_token(
    State(state): State<AppState>,
    Json(req): Json<RefreshRequest>,
) -> Result<Json<TokenPair>, ApiError> {
    let claims = state.jwt.verify(&req.refresh_token)
        .map_err(|_| ApiError::Unauthorized("Invalid refresh token"))?;

    if claims.token_type != TokenType::Refresh {
        return Err(ApiError::Unauthorized("Refresh token required"));
    }

    // revocation 체크
    let is_revoked = state.token_store.is_revoked(&claims.jti).await?;
    if is_revoked {
        return Err(ApiError::Unauthorized("Token has been revoked"));
    }

    // 기존 토큰 무효화 (rotation)
    state.token_store.revoke(&claims.jti).await?;

    // 새 토큰 발급
    let access = state.jwt.issue_access_token(&claims.sub, claims.roles.clone())?;
    let refresh = state.jwt.issue_refresh_token(&claims.sub)?;

    Ok(Json(TokenPair { access_token: access, refresh_token: refresh }))
}
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| jsonwebtoken 버전 | 10.x | crypto backend feature 필수 |
| Access token 수명 | 15분 | 짧을수록 보안 강함 |
| Refresh token 수명 | 7~30일 | 앱 성격에 따라 조정 |
| JWT 알고리즘 | HS256 (대칭) or RS256 (비대칭) | MSA는 RS256 권장 |
| `jti` 저장소 | Redis TTL = token exp | 만료된 `jti` 자동 삭제 |

---

## 안티패턴

### Refresh token을 클라이언트 로컬스토리지에 저장

XSS 공격으로 탈취 가능하다. 웹 클라이언트는 `HttpOnly` 쿠키에 저장한다.

### 서버에서 JWT를 즉시 revoke할 수 없다고 가정

`jti`를 Redis 블랙리스트에 저장하면 만료 전 토큰도 무효화할 수 있다. 로그아웃이나 비밀번호 변경 시 기존 토큰을 블랙리스트에 추가한다.

### 핸들러마다 Bearer 토큰을 직접 파싱

반복 코드와 일관성 문제가 생긴다. `AuthUser` Extractor 하나로 모든 인증 검사를 캡슐화한다.

### 모든 에러에 동일한 메시지 반환

토큰 파싱 실패, 만료, 서명 불일치를 구분하지 않고 "Unauthorized"만 반환하면 디버깅이 어렵다. 서버 로그에는 상세 에러를, 응답에는 일반 메시지를 반환한다.

---

## Gotchas

### `exp` 필드는 `usize`가 아니라 `u64`를 권장하는 버전도 있다

`jsonwebtoken 10.x`에서 `exp`는 `usize`로 동작하지만, 크로스 플랫폼(32bit)에서 2038 문제가 생길 수 있다. `u64`나 `i64`로 정의하고 `Validation.set_required_spec_claims(&["exp", "sub"])`로 명시적 검증을 설정한다.

### `Validation::new(Algorithm::HS256)`은 `exp` 검증을 자동으로 수행한다

별도로 만료 시간을 체크하지 않아도 된다. 단, `leeway`(시계 오차 허용치)는 기본 60초이므로 보안이 중요하면 `validation.leeway = 0`으로 설정한다.

### HMAC 시크릿은 최소 256비트(32바이트)를 사용한다

짧은 시크릿은 브루트포스에 취약하다. `openssl rand -hex 32`로 생성하고 환경 변수로 주입한다.

### `axum-extra`의 `TypedHeader`는 별도 feature 활성화 필요

```toml
axum-extra = { version = "0.10", features = ["typed-header"] }
```
