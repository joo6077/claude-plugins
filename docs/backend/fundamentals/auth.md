---
title: 인증과 인가
version: 0.1.0
last_updated: 2026-04-04
---

# 인증과 인가

JWT와 Session 비교, OAuth 2.0/OIDC, RBAC/ABAC, 토큰 갱신 전략, 비밀번호 해싱, MFA, CORS, CSRF 방어를 다룬다.

---

## 원칙

### 1. JWT는 stateless 확장성, Session은 서버 제어력 — 트레이드오프 기반으로 선택한다

| 항목 | JWT | Session |
|------|-----|---------|
| 상태 저장 | 클라이언트 (토큰 자체에 클레임 포함) | 서버 (Redis, DB) |
| 수평 확장 | 세션 저장소 공유 불필요 | 공유 저장소 필요 (Redis 등) |
| 즉시 무효화 | 어려움 (블랙리스트 필요) | 쉬움 (세션 삭제) |
| 토큰 크기 | 크다 (클레임 포함, 수백 바이트~수 KB) | 작다 (세션 ID만 전송) |

JWT는 마이크로서비스 간 인증 전파에 유리하고, Session은 단일 서비스에서 즉시 무효화가 중요할 때 유리하다. 둘을 혼용하면 복잡성만 증가한다.

> **출처:** [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)

### 2. OAuth 2.0은 인가, OIDC는 인증 레이어 — 혼동하지 않는다

- **OAuth 2.0**: "이 앱이 내 Google Drive에 접근해도 되는가?" — 리소스 접근 권한 위임.
- **OIDC (OpenID Connect)**: "이 사용자가 누구인가?" — OAuth 2.0 위에 ID Token(JWT)을 추가한 인증 프로토콜.

소셜 로그인을 구현할 때 OAuth 2.0의 access token으로 사용자 식별을 시도하면 안 된다. OIDC의 `id_token`을 사용하거나, userinfo 엔드포인트를 호출한다.

> **출처:** [RFC 6749 — OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749), [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)

### 3. 비밀번호 해싱은 bcrypt(cost 10+) 또는 Argon2id — MD5/SHA 절대 금지

| 알고리즘 | 권장 여부 | 파라미터 |
|----------|----------|---------|
| **Argon2id** | 최우선 권장 | 메모리 19MiB 이상, iterations 2, parallelism 1 |
| **bcrypt** | 권장 | cost factor 최소 10 (OWASP: 10 이상) |
| **scrypt** | 허용 | N=2^17, r=8, p=1 |
| **PBKDF2** | 레거시 허용 | iterations 600,000+ (SHA-256) |
| MD5, SHA-1/256 | **금지** | GPU로 초당 수십억 해시 가능 |

bcrypt의 cost factor 1 증가 = 해싱 시간 2배. cost 10은 약 100ms, cost 12는 약 400ms. 서버 부하와 보안 사이에서 균형을 잡는다.

> **출처:** [OWASP — Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### 4. RBAC는 역할 기반, ABAC는 속성 기반 — 요구사항 복잡도에 맞춰 선택한다

- **RBAC (Role-Based Access Control)**: 사용자 → 역할 → 권한. 역할 수가 적고 정적일 때 적합. 예: admin, editor, viewer.
- **ABAC (Attribute-Based Access Control)**: 사용자 속성, 리소스 속성, 환경 조건의 조합으로 접근 결정. 예: "본인 부서의 문서만 영업 시간 내 편집 가능."

RBAC로 시작하고, "역할 폭발"(role explosion — 조합마다 새 역할이 필요한 상황)이 발생하면 ABAC로 전환한다.

> **출처:** [NIST SP 800-162 — Guide to ABAC](https://csrc.nist.gov/publications/detail/sp/800-162/final)

### 5. Access token은 짧게(15분), Refresh token은 길게(7일) + 회전한다

- **Access token TTL**: 15분. 탈취되어도 피해 시간을 제한한다.
- **Refresh token TTL**: 7~14일. 사용할 때마다 새 refresh token을 발급하고 이전 것을 무효화한다(rotation).
- **Refresh token 재사용 감지**: 이미 사용된 refresh token이 다시 제출되면 해당 사용자의 모든 refresh token을 무효화한다 (token family invalidation).

```
[Client] --access_token(만료)--> [Server] 401
[Client] --refresh_token-------> [Auth Server] 새 access + 새 refresh 발급
```

> **출처:** [RFC 6749 — OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749)

### 6. CORS는 허용 origin을 명시적으로 지정한다

- `Access-Control-Allow-Origin: *`는 credentials(쿠키, Authorization 헤더)와 함께 사용할 수 없다. 브라우저가 거부한다.
- 허용 origin 목록을 서버에 유지하고, 요청의 `Origin` 헤더와 대조하여 동적으로 응답한다.
- `Access-Control-Max-Age`로 preflight 캐싱을 설정한다. 기본값은 5초, 최대 86400초(24시간, 브라우저별 상한 다름).

```
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Max-Age: 3600
```

> **출처:** [MDN — Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

### 7. CSRF 방어는 SameSite 쿠키 + CSRF 토큰 이중 방어를 적용한다

- **SameSite=Lax** (기본값): 대부분의 cross-site 요청에서 쿠키를 전송하지 않는다. 단, top-level GET 네비게이션은 허용.
- **SameSite=Strict**: 모든 cross-site 요청에서 쿠키 차단. 링크를 통한 로그인 유지가 안 되므로 UX 저하.
- **CSRF 토큰**: SameSite를 지원하지 않는 구형 브라우저 대비 이중 방어. Synchronizer Token 또는 Double Submit Cookie 패턴.

SameSite만으로 충분하다고 판단하지 않는다. 서브도메인 공격, 브라우저 버그 등 엣지 케이스가 존재한다.

> **출처:** [OWASP — CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| bcrypt cost factor 최소값 | 10 이상 (OWASP: work factor of 10 or more) |
| Argon2id 최소 메모리 | 19 MiB |
| Argon2id iterations | 최소 2 |
| JWT access token TTL | 15분 |
| JWT refresh token TTL | 7~14일 |
| PBKDF2 iterations (SHA-256) | 600,000+ |
| CORS preflight 캐시 최대값 | 86,400초 (브라우저별 상이) |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| JWT payload에 민감 정보 저장 | JWT는 서명만 되고 암호화되지 않음. Base64 디코딩으로 즉시 노출. |
| Refresh token 미회전 | 탈취된 refresh token으로 무한히 새 access token 발급 가능. |
| `CORS: Access-Control-Allow-Origin: *` | Credentials와 함께 사용 불가. 우회하려고 모든 Origin을 동적 반영하면 의미 없음. |
| 비밀번호 평문 저장 또는 MD5 해싱 | MD5는 GPU로 초당 수십억 해시 가능. 레인보우 테이블 공격에 무방비. |

---

## Gotchas

- **JWT 서명 검증을 생략하면 `alg:none` 공격에 노출된다.** 공격자가 헤더의 `alg`을 `none`으로 변경하고 서명을 빈 문자열로 보내면, 검증 없이 통과한다. 라이브러리에서 허용 알고리즘을 명시적으로 지정한다(`algorithms: ['RS256']`).
- **Refresh token 탈취 시 세션 전체를 무효화해야 한다.** 단일 refresh token만 무효화하면 공격자가 이미 발급받은 access token으로 15분간 활동할 수 있다. Token family 전체를 무효화하고, 필요하면 access token 블랙리스트를 추가한다.
- **`SameSite=None`은 `Secure` 속성이 필수다.** Chrome 80+에서 `SameSite=None`이면서 `Secure`가 없는 쿠키는 거부된다. HTTPS가 아닌 환경에서는 `SameSite=None` 자체를 사용할 수 없다.
