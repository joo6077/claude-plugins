---
name: api-init
description: >
  블랙박스 API 검증의 기반이 되는 `.api/` 를 초기화한다. OpenAPI 스펙 · 사람이 쓴 md ·
  curl/Talend 덤프를 하나의 operation 인벤토리로 정규화하고, 환경(baseUrl · allowHosts · tier)과
  인증 프로파일을 정의해 `project.yaml` · `auth.yaml` · `inventory.yaml` 을 만든다.
  "API 인벤토리", "api init", "엔드포인트 목록 만들어줘", "스펙 가져와" 같은 요청 시 트리거.
  이미 `.api/` 가 있으면 트리거하지 않는다 — 재초기화는 사용자가 명시적으로 요청할 때만 한다.
  엔드포인트를 실제로 호출하는 요청에는 트리거하지 않는다 — `/api-probe` 를 쓴다.
argument-hint: "[spec-path]"
user-invocable: true
---

## Gotchas

- **operation 키는 `METHOD + 정규화된 path template` 이다. `operationId` 로 dedupe 하지 마라** — `operationId` 는 OpenAPI 선택 필드라 curl·Talend·md 출처에는 대부분 없다. 이걸 원시 키로 쓰면 외부 덤프와의 매칭이 통째로 실패하고 dedupe 가 동작하지 않는다. `operationId` 는 별칭 컬럼에만 저장하고, 별칭 매칭에서 case-fold 하지 마라 — `getUser` 와 `GetUser` 는 서로 다른 별칭이다. (`docs/api/discovery/api-inventory-normalization.md` §1, 안티패턴)
- **path template 은 두 방향에서 틀린다 — 우선순위와 역템플릿화** — (1) concrete path 가 templated path 를 이긴다. `/users/me` 는 `/users/{id}` 보다 먼저 매칭한다. 반대로 같은 hierarchy 에서 변수명만 다른 `/users/{id}` 와 `/users/{name}` 은 동일 path 라 둘 다 살려두면 안 되고, 모호한 후보를 임의로 고르지 말고 conflict 로 남겨야 한다. (2) curl·HAR 의 관측 URL 을 역으로 템플릿화할 때는 **세그먼트 경계에서만** 변수화한다. `/files/a/b/c` 를 `/files/{path}` 로 접으면 실제로 존재하지 않는 operation 을 만든다 — path template 변수값에는 unescaped `/`, `?`, `#` 가 들어갈 수 없다. (`api-inventory-normalization.md` §3, Gotchas)
- **신뢰도 높은 출처가 낮은 출처의 값을 자동으로 덮어쓰지 않는다** — 스펙(1.00)이 관측 덤프(0.80)를 덮어쓰면 스펙과 실호출의 drift 가 사라진다. drift 를 지우는 순간 인벤토리는 계약 검증 근거로서의 가치를 잃는다. 충돌은 병합하지 말고 `needs_review: true` 로 보존하고 두 후보를 모두 적어라. (`api-inventory-normalization.md` §2·§8)
- **md·curl 예시의 누락 필드를 기본값으로 채우지 마라** — 사람이 쓴 문서와 curl 한 줄은 auth·base URL·environment 를 생략하는 게 정상이다. 빈 자리를 그럴듯한 기본값으로 메우면 나중에 스펙과의 diff 가 가짜로 사라진다. `unknown` 으로 남기고 출처를 "불완전한 관측치" 로 표시한다. (`api-inventory-normalization.md` Gotchas)
- **파라미터 키는 `(in, name)` 쌍이고, 예약 헤더 셋은 아예 파라미터가 아니다** — path/query/header/cookie 를 한 namespace 로 합치면 이름이 같고 위치가 다른 파라미터가 서로를 덮어써 조용히 사라진다. `in: path` 는 항상 required 로 강제하고, 헤더 이름만 case-fold 비교한다. 그리고 `Accept` · `Content-Type` · `Authorization` 은 파라미터 테이블에 넣지 마라 — OpenAPI 는 이 셋을 header parameter 로 정의해도 무시하며, 각각 media negotiation · requestBody media type · security requirement 에서 파생시켜야 한다. `Authorization` 을 일반 헤더로 저장하면 auth scheme·scope 판단 경로가 끊겨 인증 요구사항을 재현할 수 없다. (`api-inventory-normalization.md` §4·§5)
- **`.gitignore` 등록이 자격증명 파일 생성보다 먼저다** — 파일을 만들고 나서 `.gitignore` 를 손보는 순서로 하면, 등록에 실패했을 때 평문 id/pw 가 추적 가능한 상태로 남는다. 등록 → 등록 확인 → 그 다음에 생성이다. 등록에 실패하면 **파일을 만들지 않고 중단한다**. (설계문서 §10.2b 안전장치 1)
- **`auth.yaml` 본문에는 시크릿 값을 절대 쓰지 않는다** — `env:` / `keychain:` / `credentialsFile` 참조만 기록한다. 세 방식은 택일이며 CI 에서는 `env:` 가 맞다. 자격증명 값은 scrubber deny list 에 자동 등록되어야 하므로 그 등록 항목도 이 단계에서 같이 만든다. (`docs/api/execution/auth-secret-lifecycle.md` §4)
- **`oauth2_password` 라는 타입 이름을 만들지 마라** — id/pw 로 토큰을 받는 커스텀 로그인은 OAuth grant 가 아니다. OAuth 2.1 draft 에서 ROPC 가 빠졌고 RFC 9700 은 "MUST NOT be used" 다. `custom_login` 으로 격리해서 표준 grant 와 섞이지 않게 한다. 또한 `client_credentials` 에는 refresh token 이 없으므로(RFC 6749 §4.4.3) 갱신이 아니라 **재발급** 모델로 프로파일을 쓴다. (설계문서 §10.1)
- **토큰 캐시는 repo 밖에 두고 캐시 키를 환경별로 쪼갠다** — `~/.cache/api-kit/`, 디렉토리 0700 / 파일 0600. 캐시 키에 `환경 + 프로파일 + tokenUrl + clientId + scope + username 해시` 를 전부 넣어야 stg 토큰이 prod 요청에 실려 나가지 않는다. env 하나를 여러 프로파일이 공유하게 만들지 마라. (`auth-secret-lifecycle.md` §1, 설계문서 §6)
- **커버리지를 단일 숫자로 합치지 마라** — `OpenAPI operation` · `observed-only request`(스펙에 없는데 덤프에서 관측된 호출) · `generated probe` 세 축을 따로 센다. 합치면 스펙에 없는 실호출이 커버리지에 흡수되어, 블랙박스 검증에서 가장 중요한 신호가 사라진다. (`api-inventory-normalization.md` §9)

# `.api/` 초기화

## 0. 선행 조건 확인

```bash
test -d .api && echo "EXISTS" || echo "NEW"
git rev-parse --is-inside-work-tree 2>/dev/null || echo "NOT_A_GIT_REPO"
```

- `.api/` 가 이미 있으면 **중단하고 사용자에게 확인받는다**. 덮어쓸지, 인벤토리만 추가할지, 다른 경로에 만들지 물어본다. 조용히 덮어쓰지 마라.
- git repo 가 아니면 `.gitignore` 강제 게이트(§6)를 걸 수 없다. 이 경우 `credentials.local.json` 경로를 제안하지 말고 `env:` / `keychain:` 참조만 쓰도록 안내한다.

`$ARGUMENTS` 에 스펙 경로가 있으면 그 파일을 1순위 입력으로 잡고 §1 의 자동 탐색은 보조로만 돌린다.

---

## 1. 입력 소스 수집

`references/input-source-precedence.md` 의 탐색 경로와 신뢰도 매트릭스를 따른다.

로컬 스펙 탐색:

```bash
find . -maxdepth 4 \
  \( -name 'openapi.json' -o -name 'openapi.yaml' -o -name 'openapi.yml' \
     -o -name 'swagger.json' -o -name 'swagger.yaml' -o -name 'api-docs.json' \) \
  -not -path './node_modules/*' -not -path './.git/*' -not -path './target/*'
```

라이브 엔드포인트 후보(`/v3/api-docs`, `/openapi.json`, `/swagger/v1/swagger.json`)는 **사용자가 baseUrl 을 확정한 뒤에만** 조회한다. 이 시점엔 아직 `allowHosts` 가 없어서 안전 게이트를 못 건다.

스펙이 하나도 없으면 사용자에게 입력을 요청한다. md 문서, curl 덤프, Talend export, HAR 중 무엇이든 받는다. 아무것도 없으면 빈 인벤토리로 초기화하고 `/api-probe` 실행마다 observed-only operation 이 쌓이는 경로를 안내한다.

수집한 모든 소스에 대해 `sourceType` · `sourceVersion` · 원본 hash · 처리 못 한 필드 목록을 기록한다. unsupported/unknown 필드가 하나라도 있으면 경고를 낸다 — 조용한 필드 손실은 곧 false pass 다.

---

## 2. operation 후보 생성

소스별로 후보를 뽑되 **출처별로 따로 유지한 채** 다음 단계로 넘긴다. 이 단계에서 합치지 않는다.

| 소스 | 뽑는 것 | 주의 |
|------|---------|------|
| OpenAPI | paths → method → parameters/requestBody/responses/security | `servers` 누락 시 기본 server URL 은 `/` |
| curl 덤프 | method, URL, 헤더, body 인코딩 | shell tokenization 파서 필요 — 공백 split 금지 |
| Talend export | project/service/scenario 계층, 환경변수 | 계층을 평탄화하지 말고 provenance 로 보존 |
| HAR | `entries[]` → request/response | `queryString` 은 배열로 유지 (같은 name 반복 가능) |
| md 문서 | method + path + 설명 | 누락 필드는 `unknown` |

curl 옵션은 URL 앞뒤 어디에나 올 수 있고 `--header` 처럼 반복 가능하다. `--data` / `--data-binary` / `--data-urlencode` / `--form` / `--get` 은 각각 다른 wire 결과를 만드므로 하나로 뭉뚱그리지 않는다. 다만 curl 한 줄은 실행 예시이지 schema 계약이 아니므로, 신뢰도를 **보강하는 증거**로만 쓰고 계약 근거로 승격하지 않는다.

---

## 3. 정규화와 충돌 판정

`references/input-source-precedence.md` §충돌 판정 절차를 그대로 실행한다. 요약:

```text
1. canonical key 생성   METHOD + 정규화 path template
2. path 우선순위 적용    concrete > templated, 변수명만 다른 중복은 무효
3. 파라미터 정규화       (in, name) 쌍, path 는 required 강제
4. 예약 헤더 분리        Accept / Content-Type / Authorization 제외
5. media type 선택       가장 구체적인 key 하나, wildcard 는 fallback 목록으로
6. auth scope 매핑       operation-level security 가 top-level 을 override
7. collapse 판정         key exact match AND param-set Jaccard >= 0.80
8. conflict 판정         top-2 후보 confidence 차이 < 0.15 → needs_review
```

`inventory.yaml` 초안:

```yaml
schemaVersion: 1
operations:
  - key: "GET /orders"
    aliases: { operationId: listOrders }
    group: orders
    sources:
      - { type: openapi, confidence: 1.00, ref: "#/paths/~1orders/get" }
      - { type: curl, confidence: 0.80, ref: "docs/curl-dump.txt:14" }
    params:
      - { in: query, name: status, required: false, type: string, provenance: openapi }
      - { in: query, name: limit, required: false, type: integer, provenance: openapi }
    request: { mediaType: null }
    response: { mediaType: application/json }
    security: [{ scheme: bearerAuth, scopes: ["orders:read"] }]
    sideEffect: false
    needsReview: false

  - key: "POST /orders/{id}/cancel"
    sources:
      - { type: md, confidence: 0.55, ref: "docs/api.md:88" }
      - { type: curl, confidence: 0.80, ref: "docs/curl-dump.txt:31" }
    conflicts:
      - field: "params.query.reason"
        candidates:
          - { value: required, provenance: md }
          - { value: absent, provenance: curl }
    needsReview: true
```

`needsReview: true` 인 operation 은 개수와 함께 사용자에게 보고한다. 이 단계에서 사람이 확정하지 않아도 되지만, 계약 추출 전에는 반드시 정리해야 한다는 점을 알린다.

---

## 4. 환경 정의

사용자와 환경별로 확정한다. 값을 추측해서 채우지 마라.

| 항목 | 내용 |
|------|------|
| `tier` | `dev` / `stg` / `prod` — 안전 게이트 판정의 입력 |
| `baseUrl` | 환경별 절대 URL |
| `allowHosts` | 화이트리스트. 목록 밖 호스트로 나가는 요청은 무조건 차단 |
| `authProfile` | §5 에서 만드는 프로파일 이름 |
| 타임아웃 | `connectTimeout` · `maxTime` — 둘 다 없으면 probe 가 실행을 거부한다 |

```yaml
# .api/project.yaml
schemaVersion: 1
environments:
  dev:
    tier: dev
    baseUrl: https://dev.api.example.com
    allowHosts: ["dev.api.example.com"]
    authProfile: user-dev
    connectTimeout: 5s
    maxTime: 30s
  prod:
    tier: prod
    baseUrl: https://api.example.com
    allowHosts: ["api.example.com"]
    authProfile: svc-prod
    readOnlyByDefault: true
    requiresExplicitConfirm: true
    jobs: 1
    connectTimeout: 5s
    maxTime: 30s
writeAllowlist: []   # env + host + path + method 4중 일치 항목만 unsafe 실행 허용
```

`allowHosts` 는 baseUrl 변수 오염으로 stg 케이스가 prod 를 때리는 사고를 막는 장치다. 비워두지 마라.

---

## 5. auth 프로파일 정의

환경마다 별도 프로파일을 만든다. 하나를 여러 환경이 공유하지 않는다. 요청 scope 는 검증에 필요한 최소로 잡는다.

```yaml
# .api/auth.yaml
schemaVersion: 1
authProfiles:
  svc-prod:
    type: oauth2_client_credentials
    tokenUrl: https://idp.example.com/oauth/token
    clientIdRef: env:PROD_CLIENT_ID
    clientSecretRef: keychain:api-kit/prod-client-secret
    clientAuth: basic            # basic | body
    scope: ["orders:read"]
    token:
      accessTokenPath: "$.access_token"
      expiresInPath: "$.expires_in"
    cache:
      enabled: true
      expirySkewSeconds: 60
    inject:
      header: Authorization
      valueTemplate: "Bearer {{access_token}}"

  user-dev:
    type: custom_login           # 표준 OAuth grant 아님 — Gotchas 참조
    credentialsFile: .api/credentials.local.json
    request:
      method: POST
      url: "{{baseUrl}}/auth/login"
      headers: { Content-Type: application/json }
      json:
        id: "{{cred.id}}"
        password: "{{cred.password}}"
    token:
      accessTokenPath: "$.access_token"
      expiresInPath: "$.expires_in"
      fallbackTtlSeconds: 900
    inject:
      header: Authorization
      valueTemplate: "Bearer {{access_token}}"

cache:
  dir: ~/.cache/api-kit
  keyFields: [env, profile, tokenUrl, clientId, scope, usernameHash]

scrubber:
  denyKeys: [token, access_token, refresh_token, password, authorization, secret, client_secret, api_key, ssn]
  denyValuePatterns:
    - name: jwt
      pattern: "eyJ[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+"
    - name: email
      pattern: "[A-Za-z0-9._%%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
    - name: bearer-header
      pattern: "(?i)bearer\\s+[A-Za-z0-9._~+/-]+=*"
  credentialValuesAutoRegistered: true
```

갱신 규칙은 프로파일 값으로만 표현한다. `expires_at = 응답시각 + expires_in`, `refresh_at = expires_at - expirySkewSeconds`, skew 기본 60초(장시간 CI 는 프로파일별로 300초까지). `expires_in` 이 응답에도 프로파일 기본값에도 없으면 자동 갱신을 **추측하지 말고 금지**하고 매 실행 재발급으로 되돌린다.

`bearer` 는 헤더로만 전달한다. query parameter 주입 옵션을 프로파일에 만들지 마라 — 액세스 로그·Referer·프록시 로그에 토큰이 남는다.

---

## 6. 자격증명 파일 — gitignore 강제 게이트

`credentialsFile` 을 쓰는 프로파일이 하나라도 있을 때만 실행한다. **순서를 바꾸지 마라.**

```bash
# 1) 등록
grep -qxF '.api/credentials.local.json' .gitignore 2>/dev/null \
  || printf '\n.api/credentials.local.json\n' >> .gitignore

# 2) 등록 확인 — git 이 실제로 무시하는지 검사한다
git check-ignore -q .api/credentials.local.json && echo IGNORED || echo NOT_IGNORED

# 3) 이미 추적 중이면 즉시 중단
git ls-files --error-unmatch .api/credentials.local.json 2>/dev/null && echo TRACKED
```

- `NOT_IGNORED` 이면 **파일을 만들지 않고 중단한다.** 사용자에게 `.gitignore` 가 왜 안 먹는지(전역 ignore 충돌, negation 규칙, 상위 `.gitignore`) 확인을 요청한다.
- `TRACKED` 이면 중단하고 `git rm --cached` 안내 후 재실행하게 한다.
- 게이트 통과 후에만 생성하고 권한을 바로 조인다.

```bash
umask 177 && cat > .api/credentials.local.json <<'JSON'
{
  "dev":  { "id": "", "password": "" },
  "prod": { "id": "", "password": "" }
}
JSON
chmod 600 .api/credentials.local.json
```

`umask 177` 로 만들면 생성 순간부터 0600 이다. 만든 뒤 `chmod` 하는 것만으로는 그 사이 구간이 남는다.

---

## 7. 나머지 gitignore 와 권한

```bash
for p in '.api/reports/' '.api/snapshots/prod/' '.env'; do
  grep -qxF "$p" .gitignore 2>/dev/null || printf '%s\n' "$p" >> .gitignore
done
mkdir -p ~/.cache/api-kit && chmod 700 ~/.cache/api-kit
```

prod 스냅샷을 커밋하지 않는 이유는 실 고객 데이터 때문이다. 한 번 git history 에 들어가면 영구히 남는다. prod 는 **계약 스키마만 커밋**한다 — 값이 아니라 형태만.

dev/stg 스냅샷은 커밋한다. 회귀 diff 의 기준선이 되기 때문이다.

---

## 8. 보고

생성한 파일과 함께 다음 3축을 **따로** 보고한다.

```text
OpenAPI operation      : 34
observed-only request  : 6    (스펙에 없는데 덤프에서 관측됨)
generated probe        : 0

needs_review           : 5    (충돌 보존 — 계약 추출 전 정리 필요)
불완전한 관측치         : 6    (auth/baseUrl 미상)
lossy conversion 경고   : 2    (Talend 환경변수 2건 미매핑)
```

다음 단계를 안내한다.

> `/api-probe orders.list --env dev` 로 실제 응답을 받아 스냅샷을 만드세요.
> `needs_review` 5건은 `/api-contract` 실행 전까지 확정해야 합니다.

## References

- `../../../docs/api/discovery/api-inventory-normalization.md` — operation 키 표준화, 소스 신뢰도, path 우선순위, 충돌 판정, 커버리지 3축
- `../../../docs/api/discovery/artifact-interop-import-export.md` — curl/Talend/HAR/OpenAPI import 규칙, linkback, lossy conversion 경고
- `../../../docs/api/execution/auth-secret-lifecycle.md` — env 별 프로파일 분리, TTL 갱신, 시크릿 주입, 마스킹 한계
- `references/input-source-precedence.md` — 스펙 탐색 경로, 신뢰도 매트릭스, 충돌 판정 절차
