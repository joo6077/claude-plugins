---
title: 인증·시크릿 수명주기
version: 0.2.0
last_updated: 2026-09-05
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
캡처된 동적 값은 Hurl `redact`로 secret 처리한다. 다만 `redact`의 사정거리는 좁다 —
실측(8.0.1)에서 `--json` stdout의 `captures[].value`·`curl_cmd`·요청 헤더와 JSON 리포트의
원본 응답 파일에는 **평문이 그대로 남았다**. 그리고 `redact` capture가 있는 파일을
`--very-verbose`로 돌리면 Hurl이 실행을 거부한다(`redacted secret not authorized in verbose`).

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

Hurl `--secret`은 exact match로만 가린다. 부분 일치나 인코딩 변형은 잡지 못한다.
base64 인코딩본, 대소문자 변환본, `Bearer ` 접두 포함본 같은 변형값은 각각 별도 secret으로 등록해야 한다.

실측(8.0.1)으로 확인했다 — `--secret token=<v>`를 걸고 `X-B64` 헤더에 그 값의 base64본을 실어 보내면
`Authorization`의 원본은 `***`로 바뀌지만 base64본은 stderr·`curl_cmd`·리포트 3곳에 평문으로 남는다.

> **출처:** [Hurl — Templates / Secrets](https://hurl.dev/docs/templates.html#secrets)

### 6. 마스킹되는 채널은 절반뿐이다

Hurl은 HTTP 응답 stdout을 "unaltered output"으로 취급한다. 실측(8.0.1) 결과 마스킹 여부는 채널마다 갈린다.

가려지는 곳은 stderr 로그(`--verbose` / `--very-verbose`)와 JSON 리포트의 `report.json`(`curl_cmd`·요청 헤더)뿐이다.
가려지지 않는 곳이 더 넓다 — 기본 stdout, `--include`, `--output <file>`,
`--json` stdout 전체(`curl_cmd`·요청 헤더·`captures[].value`), 그리고 JSON 리포트가 원본 응답을
따로 떨구는 `store/*_response.json`이다. HTML 리포트는 응답 본문을 아예 담지 않아 이 목록에 없다.

따라서 응답 본문을 artifact로 남길 때는 api-kit이 별도 redaction 레이어를 거쳐야 한다 — `--secret`에 위임할 수 없다.

> **출처:** [Hurl — Templates / Secrets](https://hurl.dev/docs/templates.html#secrets) · [Hurl — JSON Report](https://hurl.dev/docs/running-tests.html#json-report) · 실측 (hurl 8.0.1, 2026-09-05)

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
| `--secret` 등록 단위 | exact value 1개당 secret 1개 (변형값 N개면 +N개) | Hurl Templates/Secrets · 실측 2026-09-05 |
| `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json` | 실측 2026-09-05 (hurl 8.0.1) |
| `--secret` 마스킹 안 되는 채널 | 기본 stdout, `--include`, `--output`, `--json` stdout 전체, JSON 리포트 `store/*_response.json` | 실측 2026-09-05 |
| `redact` capture 마스킹 범위 | stderr만. `--json` stdout·리포트 원본 응답은 평문 | 실측 2026-09-05 |
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
| `--secret`만 믿고 `--json` stdout이나 리포트 raw body를 artifact로 보관 | 실측에서 둘 다 평문이었다. 평문 토큰이 그대로 저장된다 |
| `--output <file>`로 응답을 떨구면서 마스킹됐다고 가정 | 이 경로도 unaltered output이다. 실측에서 평문이 남았다 |
| `redact` capture를 `--very-verbose`와 함께 사용 | Hurl 8.0.1이 `redacted secret not authorized in verbose`로 **실행 자체를 거부**한다 |
| prod와 stg가 같은 client credential 또는 같은 token audience 공유 | stg 유출이 prod 침해가 되고, audience 검증이 무의미해진다 |
| 만료·폐기·권한 부족을 모두 "login failed"로 뭉갬 | 갱신하면 되는 실패와 재시도 불가 실패가 구분되지 않는다 |

---

## Gotchas

- **`--secret`이 가리는 채널은 stderr 로그와 `report.json` 둘뿐이다** — 기본 stdout, `--include`, `--output <file>`, `--json` stdout 전체, JSON 리포트의 `store/*_response.json`에는 평문이 남는다(실측 2026-09-05). 응답 저장 경로에는 api-kit 자체 redaction을 반드시 걸어라.
- **`--json` stdout에는 응답 body 필드가 아예 없다** — 그래서 "body가 안 새더라"는 관측은 마스킹의 증거가 아니다. 대신 같은 출력의 `curl_cmd`·요청 헤더·`captures[].value`가 평문이다. 새는 자리가 다를 뿐 새는 건 맞다.
- **`--secret`은 exact value 매칭이다** — 값 하나당 등록 하나다. base64본, 대소문자 변환본, `Bearer ` 접두 포함본처럼 변형이 N개면 secret도 N개를 따로 등록해야 한다. 하나라도 빠지면 그 형태로 로그에 노출된다.
- **`redact` capture는 소급 적용되지 않는다** — 이후 로그에만 유효하고, 이미 출력된 원본 응답을 지우지는 못한다. 실측에서는 사정거리가 더 좁았다: 캡처값을 다음 entry 헤더로 넘기면 `--json` stdout의 `curl_cmd`와 요청 헤더에 평문으로 나타났고, JSON 리포트의 원본 응답 파일도 평문이었다.
- **`redact` capture와 `--very-verbose`는 함께 쓸 수 없다** — Hurl 8.0.1은 `redacted secret not authorized in verbose`로 실행을 거부한다. 진단하려고 verbose를 켜는 순간 파일이 안 돈다.
- **Hurl 옵션 우선순위는 env < CLI < `[Options]`** — 파일 안 `[Options]`가 profile 설정을 덮어쓴다. profile 충돌은 실행 전에 api-kit이 먼저 잡아야 한다. 실측으로 `HURL_MAX_REDIRS=3` < `--max-redirs 5` < `[Options] max-redirs: 7` 순서를 확인했다.
- **`HURL_*` 환경변수는 옵션에만 붙고 변수에는 안 붙는다** — `HURL_INSECURE`는 `--insecure`가 되지만 `HURL_who`는 `{{who}}` 변수가 되지 않는다(실측: `actual: none`). 변수는 `--variable` / `--variables-file` / `--secret` / `--secrets-file` / `[Options] variable:`로만 들어간다.
