---
title: 인증·시크릿 수명주기
version: 0.1.0
last_updated: 2026-09-04
---

# 인증·시크릿 수명주기

OAuth2 client_credentials와 커스텀 로그인(id/pw → JSON 토큰)을 다루는 규칙. 자격증명 주입, 토큰 캡처·갱신, 로그 마스킹의 한계를 정의한다. MFA·CSRF는 범위 밖이다.

---

## 원칙

### 1. env별 auth profile 분리

dev/stg/prod 각각 token endpoint, base URL, client id, scope, credential source를 따로 정의한다. 한 profile을 여러 env가 공유하지 않는다.
OAuth 보안 BCP도 명시적 metadata가 misconfiguration을 줄인다고 본다 — profile이 곧 그 metadata다.

> **출처:** [RFC 9700 §2.6 OAuth 2.0 Security BCP](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.6)

### 2. 토큰은 첫 entry에서 캡처

OAuth `client_credentials` 응답이나 커스텀 로그인 응답의 JSON 토큰은 파일 첫 entry에서 capture하고 이후 entry에서 변수로 참조한다.
캡처된 동적 값은 Hurl `redact`로 secret 처리하여 이후 로그·리포트 마스킹 대상에 넣는다.

> **출처:** [Hurl — Capturing Response](https://hurl.dev/docs/capturing-response.html)

### 3. TTL 기반 갱신

OAuth token response의 `expires_in`은 초 단위 lifetime이다. `expires_in=3600`이면 1시간이다.
만료 정보가 응답에도 profile 기본값에도 없으면 자동 갱신을 추측하지 말고 금지한다 — 매 실행 재발급으로 되돌린다.

> **출처:** [RFC 6749 §5.1 Successful Response](https://datatracker.ietf.org/doc/html/rfc6749#section-5.1)

### 4. 시크릿은 주입만

client secret, id/password, bearer token은 `.hurl` 본문에 쓰지 않는다. `--secret`, secrets file, 외부 secret store 중 하나로 주입한다.
api-kit은 자격증명을 `.api/credentials.local.json`에 두고 gitignore와 파일 권한 0600을 강제한다.

> **출처:** [Hurl — Templates / Secrets](https://hurl.dev/docs/templates.html#secrets) · [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

### 5. 리포트 전 마스킹 등록

Hurl `--secret`은 stderr 로그와 리포트에서 해당 값을 exact match로 가린다. 부분 일치나 인코딩 변형은 잡지 못한다.
base64 인코딩본, 대소문자 변환본, `Bearer ` 접두 포함본 같은 변형값은 각각 별도 secret으로 등록해야 한다.

> **출처:** [Hurl — Templates / Secrets](https://hurl.dev/docs/templates.html#secrets)

### 6. stdout은 마스킹되지 않는다

Hurl은 HTTP 응답 stdout을 "unaltered output"으로 취급한다. 기본 stdout, `--include`, `--json` stdout, JSON 리포트의 raw response dump에는 secret이 그대로 남는다.
따라서 응답 본문을 artifact로 남길 때는 api-kit이 별도 redaction 레이어를 거쳐야 한다 — `--secret`에 위임할 수 없다.

> **출처:** [Hurl — Templates / Secrets](https://hurl.dev/docs/templates.html#secrets) · [Hurl — JSON Report](https://hurl.dev/docs/running-tests.html#json-report)

### 7. bearer는 헤더로만 전달

bearer token은 `Authorization: Bearer <token>` 헤더로 보낸다. URI query parameter 방식은 쓰지 않는다.
RFC 6750은 header 방식을 권고하고, query 방식은 로그·Referer·브라우저 히스토리에 남는 문제로 비권장한다.

> **출처:** [RFC 6750 §2.1 Authorization Request Header Field](https://datatracker.ietf.org/doc/html/rfc6750#section-2.1)

### 8. 인증 실패 분류

토큰 발급 실패와 리소스 접근 실패를 다른 축으로 분류한다. token endpoint 오류는 `invalid_client`, `invalid_grant`, `invalid_scope` 등으로,
리소스 접근 오류는 `invalid_token`(401 후보)과 `insufficient_scope`(403 후보)로 나눈다. 전부 "login failed"로 합치면 재시도 판단이 불가능해진다.

> **출처:** [RFC 6749 §5.2 Error Response](https://datatracker.ietf.org/doc/html/rfc6749#section-5.2) · [RFC 6750 §3.1 Error Codes](https://datatracker.ietf.org/doc/html/rfc6750#section-3.1)

### 9. scope 최소화와 granted scope 검증

요청 scope는 검증에 필요한 최소로 잡는다. 응답 scope가 요청과 다르면 요청값이 아니라 실제 granted scope를 기준으로 계약을 검증한다.
OAuth BCP도 access token 권한을 최소 필요 범위로 제한하라고 규정한다.

> **출처:** [RFC 6749 §3.3 Access Token Scope](https://datatracker.ietf.org/doc/html/rfc6749#section-3.3) · [RFC 9700 §2.3](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| bearer token 권장 lifetime | 1시간 이하 | RFC 6750 §5.3 |
| `expires_in=3600` | 1시간 | RFC 6749 §5.1 |
| `--secret` 등록 단위 | exact value 1개당 secret 1개 (변형값 N개면 +N개) | Hurl Templates/Secrets |
| token response 캐시 헤더 | `Cache-Control: no-store`, `Pragma: no-cache` | RFC 6749 §5.1 |
| 갱신 시점 | `expires_at − max(60s, TTL의 10%)` | 추론 — 만료 경계 요청 실패 회피 |
| 자격증명 파일 | `.api/credentials.local.json`, gitignore 강제, 권한 0600 | api-kit 확정 결정 |
| 토큰 캐시 위치 | repo 밖 `~/.cache/api-kit/`, 디렉토리 0700 / 파일 0600 | api-kit 확정 결정 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| `.hurl` 파일에 client secret·id/pw·bearer token 직접 작성 | git 히스토리에 영구 기록된다. 되돌릴 수 없다 |
| `access_token`을 query string으로 전달 | 액세스 로그·Referer·프록시 로그에 토큰이 남는다 |
| `--secret`만 믿고 `--json` stdout이나 리포트 raw body를 artifact로 보관 | stdout은 마스킹 대상이 아니다. 평문 토큰이 그대로 저장된다 |
| prod와 stg가 같은 client credential 또는 같은 token audience 공유 | stg 유출이 prod 침해가 되고, audience 검증이 무의미해진다 |
| 만료·폐기·권한 부족을 모두 "login failed"로 뭉갬 | 갱신하면 되는 실패와 재시도 불가 실패가 구분되지 않는다 |

---

## Gotchas

- **`--secret`은 stdout 응답을 가리지 않는다** — stderr 로그와 리포트만 마스킹한다. 기본 stdout, `--include`, `--json` stdout, JSON 리포트의 raw response body 파일에는 secret이 평문으로 남는다. 응답 저장 경로에는 api-kit 자체 redaction을 반드시 걸어라.
- **`--secret`은 exact value 매칭이다** — 값 하나당 등록 하나다. base64본, 대소문자 변환본, `Bearer ` 접두 포함본처럼 변형이 N개면 secret도 N개를 따로 등록해야 한다. 하나라도 빠지면 그 형태로 로그에 노출된다.
- **`redact` capture는 소급 적용되지 않는다** — 이후 로그·리포트 마스킹에는 유효하지만, 이미 출력된 원본 응답을 지우지는 못한다.
- **Hurl 옵션 우선순위는 env < CLI < `[Options]`** — 파일 안 `[Options]`가 profile 설정을 덮어쓴다. profile 충돌은 실행 전에 api-kit이 먼저 잡아야 한다.
