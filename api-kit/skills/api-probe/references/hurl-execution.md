# Hurl 실행 규약

`/api-probe` 가 `.hurl` 을 합성하고 실행할 때의 게이트 순서, 파일 규칙, 커맨드 배선, 시크릿 처리.

엔진은 Hurl `8.0.1` (릴리스 2026-04-28) 기준이다. 근거는 `docs/api/execution/probe-synthesis-hurl-semantics.md`, `docs/api/execution/environment-safety-gates.md`, `docs/api/execution/auth-secret-lifecycle.md` 다.

---

## 1. 안전 게이트 — 7단계

실행 직전에 순서대로 판정한다. 하나라도 걸리면 그 자리에서 멈춘다.

```text
1. method class 판정
2. env 정책 조회
3. allowlist 조회
4. retry 정책 판정
5. redirect 정책 판정
6. 부하 예산 계산
7. 타임아웃 주입 확인
```

### 1-1. method class

| 분류 | 메서드 | 기본 |
|------|--------|------|
| safe | `GET` `HEAD` `OPTIONS` | 실행 허용 |
| unsafe | `POST` `PUT` `PATCH` `DELETE` | allowlist 있을 때만 |
| 금지 | `TRACE` | 0회. 자격증명이 붙는 프로파일에서는 명시 요청도 거부 |

`TRACE` 는 RFC 9110 상 safe 지만 요청을 loop-back 하므로 쿠키·`Authorization` 이 응답 본문으로 돌아온다(OWASP Cross-Site Tracing). **분류(safe)와 허용(allow)은 다른 축**이다.

인벤토리에 `sideEffect: true` 가 있으면 메서드와 무관하게 unsafe 로 올린다.

### 1-2. env 정책

| tier | 기본 |
|------|------|
| dev / stg | safe 실행 허용, unsafe 는 allowlist |
| prod | read-only 기본 — `GET`/`HEAD`/`OPTIONS`. `--jobs 1` 고정 |

prod read-only 의 정확한 범위는 미확정이다. 현재는 위 3개로 두고 allowlist 로 넓힐 여지만 남긴다. 임의로 확장하지 마라.

### 1-3. allowlist

unsafe 메서드는 **env + host + path + method 네 값이 모두 일치**하는 항목이 `project.yaml` 의 `writeAllowlist` 에 있을 때만 실행한다. 세 개만 맞는 항목은 통과가 아니다.

prod unsafe 실행은 allowlist 통과 후에도 대상 목록을 보여주고 사용자 확인을 받는다.

### 1-4. retry

| 대상 | 재시도 |
|------|--------|
| safe 메서드 · `PUT` · `DELETE` · 명시적 idempotent 태깅 | 허용 |
| 그 외 | `0`회 |

Hurl `--retry` 는 HTTP 실패뿐 아니라 assert·capture·runtime 오류에도 재시도한다. 파일 전체에 걸지 말고 게이트가 좁게 잘라라. `--retry-interval` 기본값은 `1000ms`, `--retry` 기본값은 `0`(`-1` 은 무제한)이다.

### 1-5. redirect

- 기본은 follow 하지 않는다. `3xx` assert 실패를 계약 위반으로 오독하지 마라.
- follow 가 필요하면 entry 의 `location: true` 또는 `--location`.
- same-origin 상한 `3`회, cross-host `0`회.
- `--location-trusted` 는 금지 옵션이다. 리다이렉트된 임의 host 로 자격증명이 전송되고, host 가 바뀌면 토큰 audience 가정도 깨진다.
- `--max-redirs` 기본값은 `50`(`-1` 은 무제한)이므로 명시적으로 낮춘다.

### 1-6. 부하 예산

```text
총 요청 수 = 파일 수 × 파일당 요청 수 × --repeat × --jobs
```

`--test` 는 파일 단위 병렬이 기본이고 `--jobs` 기본값이 CPU 수 기반이다. 단일 파일 감각으로 계산하면 실제 부하가 배로 커진다. safe 메서드도 반복·병렬이면 서버에 부담이므로 메서드가 아니라 총량으로 판정한다.

### 1-7. 타임아웃

`connect-timeout` 과 `max-time` 이 **둘 다** 지정되어야 한다. 비어 있으면 env 기본값(prod: 5s / 30s)을 주입하고, 그래도 없으면 실행을 막는다.

---

## 2. 폭발 반경 태깅

실행 항목마다 아래를 태깅하고 이 태그로 게이트를 판정한다. 리포트에도 같은 값을 남긴다.

```yaml
env: prod
host: api.example.com
authProfile: svc-prod
methodClass: safe
retry: 0
jobs: 1
maxRequests: 1
```

---

## 3. `.hurl` 합성 규칙

### 값 생성 우선순위

```text
media type 의 explicit example / examples
  → schema example
    → JSON Schema default
      → const / enum
```

`default` 는 validation 키워드가 아니라 annotation 이므로 그 값이 schema 를 만족한다는 보장이 없다. `enum` 에서 골라도 마찬가지로, 고른 뒤 schema 검증을 한 번 더 돌린다.

operation 당 기본 probe 는 `1`개(preferred media type), explicit examples 가 여럿이면 최대 `3`개.

### query 직렬화

`[Query]` 섹션 **한 경로만** 쓴다. URL 문자열 query 와 동시에 만들면 Hurl 이 둘 다 전송해 파라미터가 중복된다. OpenAPI 의 `style` / `explode` / `allowReserved` 를 반영해 직렬화한다.

### 헤더

`Accept` · `Content-Type` · `Authorization` 은 추론하지 말고 명시 생성한다.

| 헤더 | 파생 출처 |
|------|-----------|
| `Accept` | 기대 response media type |
| `Content-Type` | requestBody media type |
| `Authorization` | 해당 operation 의 security requirement |

bearer 는 헤더로만 전달한다. query parameter 로 넣지 마라 — 액세스 로그·Referer·프록시 로그에 남는다.

### entry 격리

- 상태를 공유하는 흐름(로그인 → 조회 → 삭제)은 반드시 **한 파일** 안에 둔다. cookie store 는 파일 단위로 공유되고, `--test` 는 파일 단위 병렬이라 파일 간 의존은 순서를 보장받지 못한다.
- 서로 독립인 probe 는 파일을 나눠야 병렬 실행이 안전하다.
- `[Captures]` 는 downstream 이 실제로 쓰는 값만 뽑는다. body 전체 capture 는 진단 목적일 때만.
- 체인 안에서 capture 이름을 재사용하지 마라. 같은 이름으로 다시 capture 하면 앞 값이 조용히 덮인다.
- `[Options]` 항목은 그 entry 에서만 유효한데 **`variable` 만 예외로 다음 entry 로 이어진다.** entry 별로 같은 이름 변수를 다르게 주면 뒤 entry 가 앞 값을 상속하거나 덮는다.

### 옵션 우선순위

```text
environment variable  <  command-line option  <  per-entry [Options]
```

뒤쪽이 앞쪽을 이긴다. cli-only 옵션을 `[Options]` 에 적으면 무시되어 파일에 적힌 실행 의미와 실제 실행이 어긋난다. 프로파일 설정과 `[Options]` 가 충돌하면 실행 전에 킷이 먼저 잡는다.

### 예시

```hurl
# 독립 probe — 최소 assert 는 status 하나
GET {{baseUrl}}/orders
[Query]
status: active
limit: 10
[Headers]
Accept: application/json
Authorization: Bearer {{access_token}}
[Options]
connect-timeout: 5
max-time: 30

HTTP 200
[Asserts]
header "content-type" contains "application/json"
```

```hurl
# 의존 흐름 — 한 파일 안에서만
POST {{baseUrl}}/auth/login
[Headers]
Content-Type: application/json
{
  "id": "{{login_id}}",
  "password": "{{login_password}}"
}

HTTP 200
[Captures]
access_token: jsonpath "$.access_token" redact

GET {{baseUrl}}/orders
[Headers]
Accept: application/json
Authorization: Bearer {{access_token}}

HTTP 200
```

`redact` 로 캡처하면 이후 로그·리포트 마스킹 대상에 들어간다. 다만 **소급 적용되지 않는다** — 이미 출력된 원본 응답은 지우지 못한다.

---

## 4. 실행 커맨드

```bash
SECRETS="$(mktemp)"; chmod 600 "$SECRETS"
cat > "$SECRETS" <<EOF
access_token=$TOKEN
login_id=$CRED_ID
login_password=$CRED_PW
EOF

hurl --test \
     --jobs "$JOBS" \
     --secrets-file "$SECRETS" \
     --connect-timeout "$CONNECT_TIMEOUT" \
     --max-time "$MAX_TIME" \
     --max-redirs 3 \
     --json \
     "$CASE_FILE" > "$RAW_OUT" 2> "$LOG_OUT"
STATUS=$?

rm -f "$SECRETS"
```

- `--secrets-file` 은 실행 직후 지운다. wrapper 가 발급을 마친 뒤에만 만든다.
- `.hurl` 파일에는 `{{access_token}}` 만 남고 실제 값은 절대 들어가지 않는다.
- 순차 실행이 필요하면 `--jobs 1`. prod 는 항상 `1`.
- `--continue-on-error` 는 서로 독립인 배치에만. dependency chain 이나 auth 실패 뒤에는 쓰지 않는다.
- `--very-verbose` 는 request/response body 를 stderr 로 뱉는다. 진단으로 켤 때만 쓰고 그 출력을 artifact 로 남기지 않는다.

---

## 5. exit code 규약

| exit | 의미 | 분류 | 처리 |
|------|------|------|------|
| `0` | 성공 | — | pass |
| `1` | CLI 옵션 파싱 오류 | 도구 사용 오류 | 실행 중단, 재시도 금지 |
| `2` | 입력(.hurl) 파싱 오류 | probe 생성 버그 | 합성 로직 수정 |
| `3` | 런타임 오류 | 환경 실패 | 계약 판정 보류, `error` 기록 |
| `4` | assert 실패 | 계약 신호 | `failure` 기록 |

`3` 은 DNS · TLS · timeout · connect 를 전부 포함한다. exit code 만으로는 "네트워크가 끊겼다" 이상을 알 수 없으므로 리포트에 subreason 필드를 별도로 남긴다. 안 그러면 일시적 타임아웃과 인증서 만료가 구분되지 않는다.

non-zero 를 전부 계약 실패로 보고하면 회귀 diff 가 노이즈로 덮인다.

---

## 6. 시크릿 처리

### `--secret` 의 한계

아래는 hurl 8.0.1 로 실측한 것이다 (2026-09-05). "리포트" 를 한 덩어리로 보면 틀린다 —
JSON 리포트는 두 종류의 파일을 쓰고 그 둘의 처리가 다르다.

| 가려지는 곳 | 가려지지 않는 곳 |
|-------------|------------------|
| stderr 로그 (`--verbose` / `--very-verbose`) | 기본 stdout (HTTP 응답) |
| JSON 리포트의 `report.json` (`curl_cmd` · 요청 헤더) | `--include` 출력 |
| | `--output <file>` |
| | `--json` stdout 전체 — `curl_cmd` · 요청 헤더 · `captures[].value` |
| | JSON 리포트의 `store/*_response.json` (원본 응답 본문) |

HTML 리포트는 응답 본문을 아예 담지 않아 어느 쪽에도 없다.

Hurl 은 응답 stdout 을 "unaltered output" 으로 취급한다. 따라서 응답을 파일로 남기는 경로에는 **api-kit 자체 redaction** 을 반드시 건다. `--secret` 에 위임할 수 없다.

**"안 보인다" 를 마스킹으로 읽지 마라.** `--json` stdout 의 `response` 에는 `body` 필드 자체가 없고,
`--verbose` stderr 에는 본문이 안 찍힌다. 두 곳 다 시크릿이 안 보이지만 가려서가 아니라 담기지 않아서다.
본문이 찍히는 건 `--very-verbose` 부터이고 거기서는 실제로 `***` 가 된다.

### 등록 단위

exact value 1개당 secret 1개다. 변형이 N개면 secret 도 N개를 따로 등록한다.

```text
<token>
Bearer <token>
<token 의 base64 인코딩본>
<token 의 대소문자 변환본>
```

하나라도 빠지면 그 형태로 로그에 노출된다. 자격증명 파일의 id/password 값도 같은 방식으로 등록한다.

### 저장 파이프라인

```text
scrub → I-JSON 검문 → raw 봉인 → normalized(JCS) → manifest
```

scrub 이 하나라도 실패하면 **저장하지 않는다**. 리포트 생성 전에 스크러빙이 끝나 있어야 한다 — 리포트를 만든 뒤 마스킹하면 이미 파일과 CI 로그에 비밀이 남는다.

Hurl 자체 JSON 리포트를 그대로 노출하지 마라. `store/*_response.json` 에 원본 응답이 마스킹 없이 떨어진다 (실측).
CI artifact 로 저장할 경우 저장을 끄거나 후처리 scrubber 를 강제한다.
리포트 디렉토리는 스냅샷과 **같은 fail-closed 게이트**를 지나야 한다 — 리포트를 켜는 순간
시크릿이 파일로 떨어지기 때문이다.

---

## 7. 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| URL query 와 `[Query]` 섹션 동시 생성 | Hurl 이 둘 다 전송해 파라미터가 중복된다 |
| dependent flow 를 여러 `.hurl` 파일로 분할 | `--test` 가 파일을 병렬 실행해 순서 보장이 깨진다 |
| cli-only 옵션을 `[Options]` 에 기입 | 무시되어 파일의 실행 의미와 실제 실행이 달라진다 |
| 모든 response body 를 capture | 리포트가 비대해지고 토큰·시크릿이 로그에 남는다 |
| auth 실패 뒤에도 `--continue-on-error` 로 진행 | 이후 실패가 계약 위반이 아니라 인증 전이 실패가 된다 |
| `--retry` 를 파일 전체에 지정 | non-idempotent 요청까지 재시도되어 중복 생성·중복 결제가 난다 |
| 인증 요청에 `--location-trusted` | 리다이렉트된 임의 host 로 자격증명이 전송된다 |
| `--repeat` + 병렬을 예산 없이 실행 | 파일 수 × jobs 배로 부하가 늘어 rate limit 또는 장애를 유발한다 |
| `--secret` 만 믿고 `--json` stdout 을 artifact 로 보관 | 실측에서 `curl_cmd` · 요청 헤더 · `captures[].value` 가 평문이었다 |
| `--output <file>` 로 응답을 떨구면서 마스킹됐다고 가정 | 이 경로도 unaltered output 이다. 실측에서 평문이 남았다 |
| `redact` capture 를 `--very-verbose` 와 함께 사용 | Hurl 8.0.1 이 `redacted secret not authorized in verbose` 로 **실행 자체를 거부**한다 |

---

## 8. Gotchas

- **`rawbytes` 가 아닌 capture/assert 는 decoded·decompressed 본문 기준이다** — gzip 응답의 바이트 길이나 원본 인코딩을 검증하려 했는데 디코딩된 값이 비교되어 조용히 통과한다. 바이트 수준 계약은 `rawbytes` 로 명시한다.
- **entry 번호는 `1` 부터다** — `--from-entry` / `--to-entry` 로 부분 실행할 때 0-based 로 계산하면 한 칸씩 밀린다.
- **`redact` capture 는 소급 적용되지 않는다** — 이후 로그에만 유효하고 이미 출력된 원본은 지우지 못한다. 실측에서는 사정거리가 더 좁았다: 캡처값을 다음 entry 헤더로 넘기면 `--json` 의 `curl_cmd` 와 요청 헤더에 평문으로 나타나고, JSON 리포트의 원본 응답 파일도 평문이다.
- **`redact` capture 와 `--very-verbose` 는 함께 못 쓴다** — 진단하려고 verbose 를 켜는 순간 Hurl 이 실행을 거부한다.
- **`HURL_*` 환경변수는 옵션에만 붙고 변수에는 안 붙는다** — `HURL_INSECURE` 는 `--insecure` 가 되지만 `HURL_who` 는 `{{who}}` 가 되지 않는다 (실측: assert `actual: none`).
- **Hurl `--curl` 은 export 전용이다** — curl 명령을 뽑는 기능이지 읽어들이는 기능이 아니다.
- **JUnit 매핑은 `.hurl` 파일 1개 = `<testcase>` 1개다** — 이 매핑을 바꾸면 CI 대시보드가 계약 실패와 환경 실패를 구분하지 못한다. JUnit 만 저장하고 `.hurl` 을 폐기하면 실패를 재현할 수 없다.
