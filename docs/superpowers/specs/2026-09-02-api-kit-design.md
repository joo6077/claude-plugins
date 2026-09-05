# api-kit 설계

- 작성일: 2026-09-02
- 상태: 설계 확정 대기
- 관련 리서치: Codex MODE=research 2회 (실행 엔진 landscape / 인증 자동화)

## 1. 문제

API 엔드포인트가 실제로 어떤 데이터를 돌려주는지 확인하는 일이 지금은 전부 수동이다.

- Talend API Tester 같은 GUI 도구로 하나씩 때려보고 눈으로 확인한다.
- 문서(OpenAPI 또는 사람이 쓴 md)와 실제 응답이 어긋나는 게 정상이다. 문서를 믿을 수 없다.
- 확인한 내용이 휘발된다. 한 번 본 응답이 회귀 검증으로 이어지지 않는다.
- 토큰 발급이 매번 수동이다. 만료되면 다시 받아서 다시 붙여넣는다.

## 2. 정체성

**실제 응답을 SSOT로 삼는 블랙박스 API 계약 검증 킷.**

문서도 소스도 못 믿을 때, 한 번 실제로 때려서 받은 응답을 기준선으로 삼는다. 파이프라인은 네 단계다.

```text
탐색 실행  →  응답 스냅샷 봉인  →  계약(스키마) 추출  →  회귀 실행 시 diff
```

앞의 두 단계가 Talend 대체이고, 뒤의 두 단계가 테스트 자동화다. 사용자가 요청한 두 가지가 하나의 축에 놓인다.

## 3. 범위

**In scope**

- 실행 중인 HTTP(S) JSON API
- 인증: OAuth2 client_credentials, 커스텀 로그인 엔드포인트(단순 id/pw → JSON 토큰)
- 입력: OpenAPI/Swagger 스펙, 사람이 쓴 문서(md/노션/스크린샷), curl·Talend 컬렉션 덤프
- 환경: dev / stg / prod (prod 허용, 단 기본 read-only)

**Out of scope (v0.1)**

| 제외 항목 | 이유 |
|---|---|
| gRPC / GraphQL / WebSocket | 계약 모델이 다르다. 필요해지면 별도 어댑터로 |
| 부하·성능 테스트 | k6 영역 |
| consumer-driven contract | Pact 영역. 문제 정의가 다르다 (양쪽 코드를 통제할 때) |
| 소스 기반 테스트 생성 | backend-kit `/backend-test` 영역 (화이트박스) |
| MFA / CSRF / 캡차 로그인 | 사용자 확인 결과 해당 없음. escape hatch만 남기고 구현 안 함 |

## 4. 기존 킷과의 경계

`/backend-test`는 **화이트박스**다 — 소스를 읽고 테스트 코드를 만든다.
`api-kit`은 **블랙박스**다 — 돌아가는 서버를 밖에서 때려 계약을 뽑는다.

소스 접근 없이 동작하므로 다른 팀 API, 서드파티 API에도 쓸 수 있다. 겹치지 않는다.

## 5. 기술 선택과 근거

리서치(2026-09-02, Codex)로 확인한 사실에 근거한다.

### 5.1 실행 엔진: Hurl

| 후보 | 상태 (2026-09) | 판정 |
|---|---|---|
| **Hurl** | 8.0.1 (2026-04-28), Apache-2.0, 활발 | **채택** |
| Bruno | v4.1.0 (2026-08-20), MIT + 상용 | 2순위 |
| Karate | v2.0.9 (2026-05-13) | 탈락 — JVM 의존 |
| Tavern | 3.6.2 (2026-08-24) | 탈락 — Python 의존 |
| Keploy | v3.6.30 (2026-09-01) | 탈락 — BPF/프록시/TLS CA 운영 부담 |
| Postman + Newman | 활발 | 탈락 — 컬렉션 JSON diff 노이즈, LLM 오작성 위험 |
| Playwright APIRequestContext | 활발 | 탈락 — 계약 산출물이 아니라 테스트 코드 |
| Pact | pact-js v17.1.2 (2026-08-11) | 탈락 — 문제 정의 불일치 |
| k6 | v1.8.1 (2026-08-12), AGPL-3.0 | 탈락 — 부하 테스트 영역 |
| **Dredd** | **2024-11-08 아카이브** | 제외 |

Hurl 채택 근거:

1. **단일 바이너리, 런타임 없음** → 스택 무관 조건을 충족한다. 사용자 프로젝트가 Flutter든 Rust든 상관없다.
2. **`.hurl`이 plain text** → git diff가 사람 눈에 읽히고 코드리뷰 대상이 된다.
3. **LLM 작성 안정성** → 이 산출물을 사람이 아니라 Claude가 쓴다. 중첩 JSON이나 JS assertion보다 오작성 확률이 낮다. 1급 평가축이었다.
4. 요청 체이닝 · `[Captures]` · JSONPath assert 네이티브 지원.
5. `--secret` / `--secrets-file` / `HURL_SECRET_*` redaction 지원 (단 §8.2의 한계 있음).

약점: JSON Schema assert가 네이티브가 아니다. §9의 정규화 + partial assert 조합으로 대체한다.

> 출처: [Hurl releases](https://github.com/Orange-OpenSource/hurl/releases), [Hurl repo](https://github.com/Orange-OpenSource/hurl), [Dredd (archived)](https://github.com/apiaryio/dredd)

### 5.2 보조 레일 (옵트인)

| 도구 | 역할 | 조건 |
|---|---|---|
| Schemathesis 4.x | OpenAPI conformance / fuzz | OpenAPI 스펙이 있을 때만 |
| oasdiff | OpenAPI breaking change 게이트 | OpenAPI 스펙이 있을 때만 |

호출 지점은 `/api-verify`의 옵트인 플래그다. `--spec-conformance`가 Schemathesis를, `--spec-diff <base>`가 oasdiff를 돌린다. 기본 실행 경로에는 들어가지 않는다 — 둘 다 스펙이 있을 때만 의미가 있고, 없는 프로젝트에서 실패로 잡히면 안 된다.

본체가 아니라 곁다리다. Schemathesis는 실무 오탐이 스펙 느슨함·auth·destructive endpoint·정렬 불안정에서 나오므로, read-only allowlist + seed 고정 + 실패 케이스 저장을 강제한다.

> 출처: [Schemathesis docs](https://schemathesis.readthedocs.io/en/stable/reference/cli/), [oasdiff](https://github.com/oasdiff/oasdiff)

### 5.3 포맷팅 — 비교 기준선과 화면 표시를 분리한다

두 용도가 서로 다른 도구를 요구한다. 한 덩어리로 보면 틀린다.

| 용도 | 도구 | 근거 |
|---|---|---|
| **비교 기준선** | RFC 8785 JCS canonical JSON | prettier는 **키를 정렬하지 않는다** — 공식 rationale이 "sorting object keys"를 범위 밖으로 명시한다. 서버가 키 순서를 바꾸면 회귀가 깨진다 |
| **화면 표시 (JSON)** | prettier `json` parser | `JSON.stringify(obj, null, 2)`보다 읽기 좋다. print width와 object wrap 규칙으로 짧은 객체·배열을 한 줄에 둔다 (이 차이 때문에 prettier에 별도 `json-stringify` parser가 생겼다) |
| **화면 표시 (비-JSON)** | prettier + `@prettier/plugin-xml` | HTML·CSS·YAML·GraphQL은 내장. XML만 공식 플러그인 |

JCS는 키 재귀 lexicographic 정렬, whitespace 제거, ECMAScript 숫자 직렬화, UTF-8 출력을 규정한다. 지위는 Informational이지만 canonical JSON의 사실상 표준이고 JS·Java·Go·Python 구현이 있다.

**prettier는 생성 시점에만 쓴다.** 브라우저 standalone 번들이 JSON만 해도 `standalone 82.5kB + babel 319kB + estree 213kB = 615kB`이고 HTML 169kB, YAML 136kB가 더 붙는다. 단일 HTML에 넣을 크기가 아니다. Claude가 `ui.html`을 만들 때 포맷하고 결과 문자열만 인라인하면 런타임 의존성 0이 유지된다.

prettier가 없는 환경에서는 `JSON.stringify(obj, null, 2)`로 폴백한다. 표시 품질만 조금 떨어지고 기능은 같다.

> 출처: [Prettier rationale](https://prettier.io/docs/rationale/), [Prettier options](https://prettier.io/docs/options.html), [Prettier browser](https://prettier.io/docs/browser), [@prettier/plugin-xml](https://github.com/prettier/plugin-xml), [RFC 8785 JCS](https://www.rfc-editor.org/info/rfc8785/)

## 6. 산출물 레이아웃

```text
.api/
├── project.yaml            환경 정의 · baseUrl · allowHosts · tier
├── auth.yaml               auth 프로파일 (시크릿은 참조만)
├── inventory.yaml          엔드포인트 인벤토리
├── cases/*.hurl            실행 케이스 (plain text, 리뷰 대상)
├── contracts/*.yaml        계약 — 스키마 + assert 수준
├── snapshots/
│   ├── dev/*.json          canonical JSON, HAR entry 호환 (커밋 O)
│   └── prod/               커밋 X — §8.3
├── masks/*.yaml            비결정 필드 정규화 규칙
├── ui.html                 정적 뷰어 — 의존성 0 단일 파일 (§11)
└── reports/                gitignore
```

토큰 캐시는 **repo 밖**에 둔다: `~/.cache/api-kit/`, 디렉토리 0700 / 파일 0600.
캐시 키는 `환경 + 프로파일 + tokenUrl + clientId + scope + username 해시`로 분리한다. stg 토큰이 prod로 새지 않게 하는 장치다.

## 7. 스킬 5종

| 스킬 | 입력 | 출력 |
|---|---|---|
| `/api-init` | OpenAPI 스펙 / 사람 문서 / curl 덤프 | `project.yaml`, `auth.yaml`, `inventory.yaml` |
| `/api-probe` | 엔드포인트 (또는 그룹) | 마크다운 리포트 + `snapshots/*.json` |
| `/api-contract` | 스냅샷 | `cases/*.hurl`, `contracts/*.yaml`, `masks/*.yaml` |
| `/api-verify` | 계약 전체 (또는 필터) | PASS/FAIL 리포트 + canonical diff |
| `/api-ui` | `.api/` 전체 | `.api/ui.html` 생성 후 열기 — §11 |

인증은 별도 스킬로 빼지 않는다. `/api-init`에서 프로파일을 선언하면 probe와 verify가 자동으로 발급·주입한다. "토큰도 알아서 발급"이라는 요구에 스킬을 하나 더 미는 것보다 이 구조가 맞다.

### 7.1 `/api-init`

1. 프로젝트에서 OpenAPI 스펙 탐색 (`openapi.{json,yaml}`, `swagger.json`, `/v3/api-docs` 등)
2. 없으면 사용자가 준 문서·덤프를 읽어 인벤토리로 정규화
3. 환경 정의 — baseUrl, allowHosts, tier
4. auth 프로파일 대화형 정의 → 시크릿은 값이 아니라 **참조**만 기록
5. `.gitignore`에 `reports/`, `snapshots/prod/`, `.env` 추가

### 7.2 `/api-probe`

Talend 대체 지점이다.

1. 인벤토리에서 대상 엔드포인트 확정
2. auth 프로파일로 토큰 발급 (캐시 우선)
3. 요청 실행 — §8.1 prod 가드 통과 필수
4. 응답 → **redaction → 정규화 → canonical JSON** 순으로 처리 후 스냅샷 저장
5. 마크다운 리포트 출력: 상태코드, 헤더 요약, 응답 본문(포맷됨), 추론된 필드 타입 표

### 7.3 `/api-contract`

1. 스냅샷에서 스키마 추론 — 필드 경로, 타입, nullable, enum 후보, 필수 여부
2. 추론 결과를 사용자에게 제시하고 확정받는다 (추론은 초안일 뿐이라는 게 리서치 결론)
3. `.hurl` 케이스 생성 + `contracts/*.yaml`에 assert 수준 기록
4. 비결정 필드를 감지해 `masks/*.yaml` 초안 생성

### 7.4 `/api-verify`

1. 계약 전체(또는 필터) 실행
2. 응답 정규화 후 계약과 대조
3. PASS/FAIL + canonical diff 리포트
4. prod 환경이면 §8.1 게이트 적용

## 8. 안전 가드

prod 테스트가 허용되므로 가드는 "차단"이 아니라 "좁히기"로 설계한다.

### 8.1 prod 가드

- **기본 read-only**: `tier: prod`에서는 GET/HEAD/OPTIONS만 자동 실행한다.
- 쓰기 메서드는 케이스에 `prodWrite: true`를 명시해야 하고, 실행 시 대상 목록을 보여주고 사용자 확인을 받는다.
- **`allowHosts` 화이트리스트**: 목록 밖 호스트로 나가는 요청은 무조건 차단. baseUrl 변수 오염으로 stg 케이스가 prod를 때리는 사고를 막는다.
- prod auth 프로파일과 토큰 캐시는 다른 환경과 분리한다.

### 8.2 Redaction — Hurl에 맡기면 안 되는 지점

Hurl의 `--secret`이 exact match로 가리는 곳은 **stderr 로그와 JSON 리포트의 `report.json`** 둘뿐이다.
stdout의 HTTP 응답, `--include`, `--output <file>`, `--json` stdout 전체(`curl_cmd`·요청 헤더·`captures[].value`),
그리고 JSON 리포트가 원본 응답을 따로 떨구는 `store/*_response.json`은 **가리지 않는다**.
`redact` capture도 마찬가지로 `--json` stdout과 그 store 파일을 못 가린다.

따라서 스냅샷 저장 직전에 킷 자체 scrubber를 통과시킨다. 이건 선택이 아니라 필수 게이트다.

- 키 이름 deny list (`token`, `password`, `authorization`, `secret`, `ssn` 등)
- **값 형태 정규식** — 키 이름만으로는 못 잡는다. 이메일, 전화번호, JWT 형태, 카드번호 형태
- 도메인별 deny path 추가 가능
- redaction 실패 시 스냅샷을 저장하지 않는다 (fail-closed)

**게이트를 걸 경로는 스냅샷만이 아니다.** 2026-09-05 실측에서 유출 경로가 셋 더 드러났다 —
`--output`으로 떨군 파일, `--report-json`의 `store/` 디렉토리, `--json` stdout을 artifact로 남기는 경우다.
`/api-probe`가 리포트를 켜면 시크릿이 파일로 떨어진다는 뜻이므로 리포트 디렉토리도 같은 fail-closed 게이트를 지난다.

> 출처: [Hurl templates](https://hurl.dev/docs/templates.html), [Hurl captures](https://hurl.dev/docs/capturing-response.html), 실측 (hurl 8.0.1, 2026-09-05 — `docs/api/research-log.md`)

### 8.3 prod 스냅샷은 커밋하지 않는다

prod 응답에는 실 고객 데이터가 들어온다. 한 번 git history에 들어가면 영구히 남는다.

- **dev/stg**: 스냅샷 값까지 커밋한다. 회귀 diff의 기준선이 된다.
- **prod**: 스냅샷을 `.gitignore`하고 **계약 스키마만 커밋**한다. 값이 아니라 형태만 남긴다.

## 9. 정규화와 계약 실패 기준

### 9.1 정규화

정규화 없이는 회귀가 매 실행 빨간불이다. 실행 전 정규화가 표준 패턴이다.

- 타임스탬프 / UUID / 페이지네이션 커서 → sentinel 치환
- 배열 stable sort (정렬 불안정 대응)
- 부동소수 정밀도 고정
- 결과를 canonical JSON(키 정렬 + 2-space)으로 직렬화

### 9.2 계약 실패 기준 — 3단계

기본은 partial, 필요할 때 조인다.

| 수준 | 검사 내용 | 지정 방법 |
|---|---|---|
| **partial** (기본) | 상태코드, content-type, 필수 필드 존재, 타입 일치, enum 값 | 기본값 |
| **pin** | 위 + 지정 경로에 **명시 assertion** | `pin: [{path:"$.meta.total", assert:">= len($.data)"}]` |
| **exact** | canonical JSON 전체 diff (정규화 후) | `exact: true` |

exact를 기본으로 두면 서버가 필드 하나 추가할 때마다 깨진다. partial만 두면 조용한 회귀를 놓친다. 그래서 중요한 필드만 `pin`으로 올리는 중간 단계를 둔다.

**`pin`은 "값 고정"이 아니다.** 초안에서 그렇게 적었다가 뒤집었다. 값을 고정하면 total·cursor·id·timestamp
같이 매 호출 변하는 필드에 붙일 수 없어 쓸모가 없고, 실제로 픽스처의 `$.meta.total`이 그 모순에 걸렸다.
pin이 하는 일은 **타입이 멀쩡한 채 값만 망가진 회귀를 잡는 것**이다 — partial은 `"Bearer"` → `"bearer"`,
`47` → `-1`, `"active"` → `"ACTIVE"` 를 전부 통과시킨다. 전부 타입은 그대로이기 때문이다.

값 고정(`= "Bearer"`)은 pin이 표현할 수 있는 assertion **한 종류**일 뿐이고, 안정 필드
(discriminator·API 버전·통화 코드·고정 status)에만 쓴다. 변동 필드에는 범위·패턴·불변식을 건다.

**경로 간 불변식은 Hurl assert 로 표현되지 않는다.** Hurl 의 assert 는 경로 1 개에 predicate 1 개다
(`jsonpath "$.meta.total" >= 0`). `$.meta.total >= len($.data)` 처럼 **두 경로를 비교하는 불변식**은
Hurl 문법으로 쓸 수 없다. 상수로 근사하지 마라 — `>= 3` 으로 박으면 데이터가 늘어난 순간 무의미해진다.

이런 assertion 은 `contracts/*.yaml` 의 `pin` 에만 기록하고, `/api-verify` 가 Hurl 실행 뒤
**후처리 단계에서 검사**한다. 즉 pin assertion 은 두 부류다 — Hurl 이 직접 검사하는 것과
킷이 후처리로 검사하는 것. 계약 파일은 둘을 구분해 표기한다.
(2026-09-04 스킬 작성 중 발견. 설계문서 §5.1 "JSON Schema assert 가 네이티브가 아니다" 의 연장선)

| 필드 성격 | 적합한 assertion | 예 |
|---|---|---|
| 안정값 | 값 고정 | `$.token_type = "Bearer"` |
| 열거형 | 집합 소속 | `$.data[].status ∈ active·shipped·cancelled` |
| 변동 수치 | 범위·불변식 | `$.meta.total ≥ len($.data)` · `$.price > 0` |
| 식별자 | 패턴 | `$.orderId ^ord_` |
| 컬렉션 | 개수 불변식 | `$.data[].isDefault` 가 true 인 항목 정확히 1개 |

> 근거 (2026-09-04 리서치): `pin`은 조사한 주류 도구 어디에서도 "경로를 값까지 고정" 이라는 뜻으로
> 쓰이지 않는다 — 발견된 용례는 버전 pin([Dredd](https://dredd.org/en/latest/how-it-works.html))과
> 기준 snapshot pin뿐이다. 필드별 검증 강도의 실제 어휘는
> [Hurl assert + predicate](https://hurl.dev/docs/asserting-response.html),
> [Karate schema marker](https://docs.karatelabs.io/api-reference/syntax-reference/),
> [Pact matcher](https://docs.pact.io/getting_started/matching),
> [JSON Schema `const`/`enum`](https://json-schema.org/understanding-json-schema/reference/annotations) 이다.
> Dredd는 기본이 구조 검증(키 존재 + primitive 타입)이고 값 검증은 별도 expectation으로 올린다.
> 이름은 UI 전반에 아이콘이 깔려 있어 `pin`으로 유지하되, **의미는 assertion으로 재정의**한다.

**필수 필드 판정 주의.** 스냅샷 하나에서 추론하면 optional 필드가 required로 잡힌다. 그래서 `/api-contract`는 추론 결과를 required로 확정하지 않고 `required` / `optional` / `미확정` 3분류로 제시하고 사용자에게 확정받는다. 스냅샷이 2개 이상이면 교집합을 required 후보로, 합집합 차분을 optional 후보로 올린다.

## 10. 인증 설계

### 10.1 사실 정정 — ROPC는 OAuth grant가 아니다

사용자가 선택한 "로그인 API → 토큰"은 2026 기준 OAuth 표준 grant가 아니다.

- OAuth 2.1 draft-15 (2026-03-02) §1.8, §10 — Resource Owner Password Credentials grant가 **명세에서 빠졌다**.
- RFC 9700 §2.4 — ROPC는 **"MUST NOT be used"**.

따라서 `oauth2_password`라는 이름을 쓰지 않고 **`custom_login`**으로 격리한다. 실무에서 이건 대부분 표준 grant가 아니라 그냥 커스텀 `/auth/login`이므로 이름이 더 정확하기도 하다.

또한 `client_credentials`에는 refresh token이 발급되지 않는다 (RFC 6749 §4.4.3 "SHOULD NOT be included"). 갱신이 아니라 **재발급** 모델로 설계한다.

> 출처: [OAuth 2.1 draft-15](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-15), [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html), [RFC 6749](https://www.rfc-editor.org/info/rfc6749/)

### 10.2 auth 프로파일 스키마 (초안)

```yaml
version: 1

environments:
  dev:
    tier: dev
    baseUrl: https://dev.api.example.com
    allowHosts: ["dev.api.example.com"]
    authProfile: svc-dev
  prod:
    tier: prod
    baseUrl: https://api.example.com
    allowHosts: ["api.example.com"]
    authProfile: svc-prod
    readOnlyByDefault: true
    requiresExplicitConfirm: true

authProfiles:
  svc-dev:
    type: oauth2_client_credentials
    tokenUrl: https://dev-idp.example.com/oauth/token
    clientIdRef: env:DEV_CLIENT_ID
    clientSecretRef: keychain:api-kit/dev-client-secret
    clientAuth: basic          # basic | body
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
    type: custom_login         # 표준 OAuth grant 아님 — §10.1
    request:
      method: POST
      url: "{{baseUrl}}/auth/login"
      headers: { Content-Type: application/json }
      json:
        id: "{{secret:env:DEV_LOGIN_ID}}"
        password: "{{secret:keychain:api-kit/dev-login-password}}"
    token:
      accessTokenPath: "$.access_token"
      expiresInPath: "$.expires_in"
      fallbackTtlSeconds: 900
    inject:
      header: Authorization
      valueTemplate: "Bearer {{access_token}}"
```

### 10.2b 자격증명 파일 — id/비번을 적어두고 토큰은 알아서 갱신

사용자 요구(2026-09-02): "아이디하고 비번을 입력해두면 JSON 파일을 읽어서 토큰이 자동 갱신되게, 시간이 지나도."

`env:`/`keychain:` 참조만 허용하면 매번 셸에 환경변수를 export 해야 한다. 실사용에 마찰이 크다.
**자격증명 파일을 1급으로 지원하되, 커밋 경로를 원천 차단한다.**

`.api/credentials.local.json` — `/api-init`이 `.gitignore`에 자동 등록한다. 파일 권한 `0600`.

```json
{
  "dev":  { "id": "tester@shopflow.io", "password": "····" },
  "stg":  { "id": "qa@shopflow.io",     "password": "····" },
  "prod": { "id": "readonly@shopflow.io", "password": "····" }
}
```

프로파일에서 `credentialsFile`로 참조하고 `{{cred.id}}` / `{{cred.password}}`로 주입한다.

```yaml
  user-dev:
    type: custom_login
    credentialsFile: .api/credentials.local.json
    request:
      method: POST
      url: "{{baseUrl}}/auth/login"
      json:
        id: "{{cred.id}}"
        password: "{{cred.password}}"
    token:
      accessTokenPath: "$.access_token"
      expiresInPath: "$.expires_in"
      fallbackTtlSeconds: 900
```

**"시간이 지나도" 를 만드는 부분이 §10.3의 갱신 규칙이다.** 발급 시 `expires_at`을 캐시에 적고,
만료 60초 전에 도달하면 자격증명 파일을 다시 읽어 재로그인한다. 사용자는 한 번 적어두면 그만이다.
`client_credentials`에는 refresh token이 없으므로(RFC 6749 §4.4.3) 이 재발급 경로가 유일한 수단이다.

**안전 장치 3중.** (1) `/api-init`이 `.gitignore` 등록을 강제하고 등록 실패 시 파일을 만들지 않는다.
(2) 매 실행 전 파일이 git 추적 대상인지 검사하고, 추적 중이면 중단한다.
(3) 자격증명 값은 §8.2 scrubber의 deny list에 자동 등록되어 스냅샷·리포트·로그에 남지 않는다.

기존 `env:` / `keychain:` 참조도 계속 지원한다 — CI에서는 그쪽이 맞다. 세 방식 중 택일이다.

---

프로파일 본문에는 여전히 시크릿 **값**을 쓰지 않는다. 참조(`env:` / `keychain:` / `credentialsFile`)만 기록한다.

### 10.3 런타임 규칙

- `expires_at = 응답시각 + expires_in`, `refresh_at = expires_at - expirySkewSeconds`
- **skew 기본 60초.** Spring Security client credentials provider 기본값과 같다. 장시간 CI나 IdP 지연이 큰 환경은 프로파일별로 300초까지 올릴 수 있다 (Google Node auth library 기본값).
- `expires_in`이 없으면 `fallbackTtlSeconds` 사용. TTL이 skew보다 짧으면 캐시를 세션 한정으로 전환한다.
- **401 재시도는 1회.** `WWW-Authenticate`에 `error="invalid_token"`일 때만 기본 활성화한다. 커스텀 API는 status/body matcher를 명시한 경우만. 재발급 후에도 401이면 즉시 실패 — 무한 루프를 막는다.
- 병렬 실행 시 토큰 발급에 **파일 락**을 건다. 여러 케이스가 동시에 시작해서 IdP를 두들기는 걸 막는다.
- Hurl에는 wrapper가 발급을 마친 뒤 임시 `--secrets-file`로 넘긴다. `.hurl` 파일에는 `Authorization: Bearer {{access_token}}`만 남는다.

## 11. UI 레이어 — 정적 뷰어

### 11.1 결정: 브라우저는 요청을 쏘지 않는다

`.api/ui.html`을 생성한다. 의존성 0, 단일 파일, `file://` 더블클릭으로 열린다. 왼쪽은 폴더 트리, 오른쪽은 엔드포인트 상세와 응답 — Postman과 VSCode 탐색기의 조직화를 가져오되 **실제 요청 발사는 브라우저가 하지 않는다.**

브라우저에서 임의 호스트로 요청을 쏘면 따라오는 것:

- **CORS 실패가 기본값이다.** `Authorization` 헤더가 `Access-Control-Allow-Headers`에 없거나, preflight가 401을 뱉거나, credentials 요청에 `*` origin이면 막힌다. HTTPS 페이지에서 HTTP API를 부르는 것도 막힌다.
- **우회하려면 프록시가 필요한데, 프록시 운영자는 URL·헤더·베어러 토큰·body를 전부 본다.** hosted proxy는 시크릿이나 PII가 있는 요청에 쓰면 안 된다.
- **토큰을 브라우저에 두게 된다.** OWASP는 `localStorage`/`sessionStorage`에 auth token·JWT·refresh token·session id를 저장하지 말라고 명시한다. (Redocly legacy Try it은 실제로 sessionStorage에 토큰을 넣는다 — 기존 도구도 이 선을 넘는다.)

요청 실행은 이미 Hurl + CLI가 맡고 있다. 브라우저 Try it을 넣으면 얻는 것 없이 CORS·프록시·토큰 저장 세 문제가 새로 생긴다. §8의 redaction 설계도 통째로 재검토 대상이 된다.

> 출처: [Swagger UI CORS](https://swagger.io/docs/open-source-tools/swagger-ui/usage/cors/), [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [OAuth for Browser-Based Apps](https://oauth.net/2/browser-based-apps/)

### 11.2 폼은 만든다 — 발사 대신 커맨드를 만든다

엔드포인트별 요청 폼은 인벤토리에서 미리 생성한다. path 파라미터, 쿼리, 헤더, body 스키마가 채워진 채로 뜬다. 폼은 **편집 가능**하다.

값을 고치고 `실행` 을 누르면 브라우저가 요청을 쏘는 게 아니라, **편집한 값이 반영된 커맨드를 클립보드에 복사**한다.

```text
/api-probe orders.list --query status=active --query limit=10
```

이걸 Claude에게 붙여넣으면 Claude가 Hurl로 쏘고, 결과가 스냅샷에 저장되고, `ui.html`이 갱신된다. 시크릿은 브라우저 근처에 오지 않는다.

Postman의 조직화와 편집감은 얻고, CORS·프록시·토큰 저장은 발생하지 않는다.

### 11.3 기존 렌더러를 기본 UI로 쓰지 않는다

| 후보 | 상태 (2026-09) | 판정 |
|---|---|---|
| Redoc CE | 2.5.3 (2026-05-29), MIT | 보조 — `redocly build-docs` → 단일 `redoc-static.html`이 가장 깔끔. 단 Try it 없음, OpenAPI 전용 |
| Scalar | `@scalar/api-reference` 1.67.0, MIT | 탈락 — UI 품질 최고지만 단일 HTML이 기본 산출물이 아니고 OpenAPI 전용, proxy 전제 |
| Zudoku | 0.86.0 (2026-08-28) | 탈락 — nav는 가장 강하나 React/Vite 빌드 전제 |
| Stoplight Elements | 9.0.24, Apache-2.0, JS 2.08MB | 탈락 — 임의 폴더 트리 약함 |
| Swagger UI | swagger-ui-dist 5.32.14, JS 1.48MB | 탈락 — tag accordion만, 폴더 트리 없음 |
| RapiDoc | 9.3.8, **npm publish 2년 전** | 탈락 — 유지보수 정체 |
| Hoppscotch / Bruno | v2026.8.0 / v4.1.0 | 탈락 — 앱·서비스라 단일 HTML 산출물이 아님 |

전부 **OpenAPI 전용**이라는 게 결정적이다. 이 킷은 OpenAPI 없는 프로젝트(사람 문서·curl 덤프만 있는 경우)를 1급으로 지원해야 하고, 중심 데이터가 스펙이 아니라 **실측 스냅샷**이다. 기존 렌더러에 얹으면 두 요구를 계속 우회하게 된다.

따라서 **자체 단일 HTML**을 생성한다. 다만 OpenAPI가 있는 프로젝트에는 보너스로 `redoc-static.html` 생성을 옵트인으로 제공한다.

### 11.4 트리 UI — 완전한 ARIA tree 대신 accordion

W3C APG Tree View 패턴은 `role=tree`/`treeitem`/`group`, `aria-expanded`, roving focus 또는 `aria-activedescendant`, 방향키·Home·End·Enter·typeahead를 전부 요구한다. **반쯤 구현하면 평범한 `nav > ul > button` accordion보다 접근성이 나빠진다.**

의존성 0 단일 파일에 tree 패턴을 온전히 넣는 건 과하다. **시각적으로는 VSCode 탐색기 느낌을 내되 마크업은 accordion**으로 간다.

> 출처: [W3C WAI-ARIA APG Tree View](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/)

### 11.5 레이아웃 — 요약 먼저, 상세는 drill-down

Playwright HTML reporter와 k6 리포트의 확립된 패턴을 따른다.

- **상단**: 요약 — 환경 선택, 토큰 만료 미터, 전체 PASS/FAIL/미실행 카운트(클릭 시 트리 필터), 테마 토글
- **좌측**: 엔드포인트 트리 (그룹 → 엔드포인트). 실패한 항목에 배지. 경로는 **말줄임하지 않는다** — 경로가 식별자이므로 줄을 넘겨서라도 전문을 보여준다
- **우측**: 좌우 2패널. 왼쪽이 요청 폼 + 커맨드 바, 오른쪽이 응답. 드래그로 폭 조절
- **응답 탭**: `본문` · `헤더` · `타이밍` (실패 시 `실패 원인` 이 맨 앞에 붙는다)
- **큰 데이터는 인라인하지 않는다** — 스냅샷 본문 상한 256KB, 초과분은 잘라내고 원본 파일 경로를 표시한다

`file://`는 origin이 `null`이라 fetch가 막히므로 데이터는 HTML에 인라인한다. 위 상한이 그래서 필요하다.

> 출처: [Playwright reporters](https://playwright.dev/docs/test-reporters), [k6 end-of-test summary](https://grafana.com/docs/k6/latest/results-output/end-of-test/), [HAR Viewer](https://harviewer.com/)

### 11.5b 응답 뷰 — 본문과 스키마를 한 화면에, 단 같은 행에 넣지 않는다

확정 시안(`.mockups/api-ui-v7.html`)에서 실측으로 확정한 구조다.

응답 `본문` 탭은 위아래 두 블록이다.

1. **JSON 본문** — 값 그대로. 접기·pin 표시. 여기에 **인라인 diff** 가 얹힌다:
   좌측 거터 `+ − ~`, 행 배경 틴트, 사라진 필드는 취소선 유령 행. 툴바의 `변경 표시` 스위치로 끈다
2. **데이터 구조 표** — `필드` · `타입` · `필수` · `설명` 4열. 변경 표시가 켜져 있으면 표의 행에도
   같은 마크와 틴트가 붙는다

**스키마 열을 JSON 행 안에 넣는 설계를 먼저 시도했고 폐기했다.** 1280px 에서 재보면 스키마 열이
코드 열을 밀어 값이 통째로 사라진다 (`"orderId":"or…`). 1440px 에서만 겨우 읽혔다. 한 행에
"실제 값" 과 "계약이 아는 정보" 두 가지를 넣으면 좁은 폭에서 반드시 하나가 죽는다.

이 표가 별도 `구조 diff` 탭을 대신한다 — 탭을 따로 두면 같은 정보가 두 곳에 있게 되고 어느 쪽이
정본인지 흐려진다.

### 11.6 Hurl 자체 HTML 리포트로는 부족하다

Hurl은 `--report-html DIR`로 리포트를 만든다. 하지만 폴더 트리, 스키마 인지 탐색기, 자동 PII redaction이 없다. §8.2에서 확인한 대로 원본 응답 dump에 토큰이 남을 수 있으므로, Hurl 리포트를 그대로 노출하지 않고 킷이 scrubber를 거친 데이터로 자체 UI를 렌더한다.

> 출처: [Hurl running tests](https://hurl.dev/docs/running-tests.html)

### 11.7 핵심 원칙 — 생성 시점 precompute

"런타임 의존성 0"과 "Swagger UI보다 고급"은 충돌하지 않는다. **무거운 계산을 생성 시점으로 옮기면 된다.**

코드 스니펫, 스냅샷 간 diff, 검색 인덱스, shape summary를 Claude가 `ui.html`을 만들 때 미리 계산해 인라인한다. 브라우저는 렌더만 한다. `file://`에서 fetch 없이 즉시 열리고, 라이브러리를 번들할 필요도 없다.

대가는 하나다. 사용자가 폼에서 파라미터를 바꿨을 때 **모든 언어의 스니펫을 실시간 재생성할 수는 없다.** curl 정도는 클라이언트에서 문자열 치환으로 갱신하고, 나머지 언어는 precompute된 기본값을 보여준 뒤 §11.2의 커맨드 복사 흐름으로 넘긴다.

이 원칙 때문에 **런타임에 WASM을 따로 요청하는 도구는 배제한다** (`curlconverter` 등) — `file://`에서 로드되지 않는다.

### 11.8 고급 기능 — 무엇을 넣고 무엇을 버리는가

2026 API 도구들이 Swagger UI 대비 제공하는 기능 중, **실제 요청 발사 없이 성립하는 것만** 골랐다.

**P0 — v0.1에 넣는다**

| 기능 | 구현 |
|---|---|
| 스냅샷 컬렉션·히스토리 탐색 + 전역 검색 | 자체. 생성 시점 검색 인덱스 |
| resolved request 표시 | 템플릿 원문과 실제 치환값을 나란히. 시크릿은 마스킹된 채로 |
| JSON 트리 — 접기·구문강조·key/value/path 검색·JSON Pointer 복사 | 자체 구현 |
| **스냅샷 간 구조적 diff** | `microdiff` 1.6.0 — **minified 1kB 미만, 의존성 0, MIT**. 경로 단위 CREATE/REMOVE/CHANGE를 **JSON 본문에 인라인**(거터·틴트·유령 행)으로, 동시에 데이터 구조 표의 행 마크로 (§11.5b). on/off 토글 |

구조적 diff가 이 뷰어를 Swagger UI와 갈라놓는 지점이다. 텍스트 diff가 아니라 **값·타입·경로 단위**로 "지난번 대비 이 필드가 사라졌다"를 보여준다. 계약 회귀 킷의 UI가 마땅히 해야 할 일이고, Swagger UI에는 아예 없는 축이다.

**P1 — 여유 되면**

- shape summary — 응답의 top-level 형태, nullable/타입 변화, 배열 item 수
- 대형 JSON lazy rendering — 총 노드 10k 초과 또는 단일 배열 자식 500개 초과에서 pagination 전환

**P2 — v0.1에서 뺀다**

코드 스니펫 생성(사용자 판단으로 P0에서 강등 — 안 쓸 기능이 화면을 잡아먹는다), JSONPath/JMESPath 쿼리 플레이그라운드, 테이블 뷰, 저장된 테스트 결과 타임라인. 가치는 있으나 단일 파일 복잡도가 급격히 올라간다.

**애초에 못 가져오는 것**

mock server, 모니터링, 협업/RBAC/SSO, 실시간 테스트 러너. 요청 발사나 서버가 전제라 정적 뷰어의 범위 밖이다. 메타데이터 표시까지가 한계다.

### 11.9 JSON 뷰어는 자체 구현

기존 라이브러리를 검토했으나 단일 파일 제약과 맞지 않는다.

| 후보 | 판정 |
|---|---|
| `big-json-viewer` 0.2.2 | 의존성 0에 pagination·search·copy path가 있으나 번들 크기 미확인, 유지보수 정체 |
| `vanilla-jsoneditor` 3.13.0 | 기능은 최고지만 **의존성 26개** — 단일 파일 목표와 충돌 |
| JSON Bonsai | 라이브러리가 아니라 확장 프로그램. 100k+ 노드 virtualization 설계는 참고 |

P0 범위(접기·하이라이트·검색·경로 복사·배열 pagination)는 자체 구현이 더 작고 확실하다. §11.4의 accordion 결정과 같은 판단이다.

**diff는 예외적으로 `microdiff`를 인라인한다** — 1kB 미만에 의존성이 0이라 단일 파일 원칙을 깨지 않는다. 배열 원소 이동(move) 인식이 약한 게 알려진 한계이고, 그게 문제가 되면 `jsondiffpatch` 0.7.6(gzip 16kB)으로 올린다.

### 11.10 검색 — 사이드바 입력창이 아니라 커맨드 팔레트

엔드포인트만 찾는 게 아니다. 실패한 것만 보기, 최근 실행, pin 보유, 액션 실행(커맨드 복사·환경
전환·테마), 단축키 확인까지 한 입구로 묶는다. 사이드바 폭에 가둘 이유가 없다.

`⌘K` / `Ctrl+K` / `/` 로 열리고, fuzzy 매칭에 스코프 4종(`실패` · `최근 실행` · `pin` · `단축키`)을
둔다. `↑↓` 이동, `↵` 선택, `Esc` 닫기, 스코프 상태에서 `⌫` 로 해제.

### 11.11 요청 폼은 행을 더할 수 있어야 한다

§11.2 가 "폼은 편집 가능" 이라고만 적어 두면 픽스처 값만 고칠 수 있는 폼이 나온다. 실제로 그렇게
구현됐고 쓸 수 없었다. 인벤토리에 없는 쿼리·헤더를 그 자리에서 더하고, `GET` 처럼 본문이 없는
엔드포인트에도 본문을 붙일 수 있어야 한다.

| 추가 | 커맨드 반영 |
|---|---|
| 쿼리 파라미터 | `--query name=value` |
| 헤더 | `--header 'Name: value'` |
| JSON 본문 | `--body '{...}'` |

추가분은 엔드포인트별로 따로 산다. 본문을 더하면 `Content-Type: application/json` 이 헤더에
자동으로 붙는다.

## 12. 확정된 결정

| 항목 | 결정 | 근거 |
|---|---|---|
| 실행 엔진 | Hurl 8.0.1 | §5.1 리서치 |
| prod 테스트 | 허용, 단 기본 read-only + 건별 확인 | 사용자 확인 2026-09-02 |
| 로그인 방식 | 단순 id/pw. MFA·CSRF 없음 | 사용자 확인 2026-09-02 |
| 계약 실패 기준 | partial 기본 + pin + exact 옵트인. **pin = 값 고정이 아니라 경로별 assertion** | 사용자 확인 2026-09-02 · 의미 재정의 2026-09-04 (§9.2 리서치) |
| prod 스냅샷 | 커밋하지 않음, 스키마만 커밋 | §8.3 |
| 자격증명 | `.api/credentials.local.json` 지원 — gitignore 강제 + 추적 검사 + scrubber 등록 | §10.2b 사용자 요청 |
| UI 질감 | **park-golf-admin 디자인 언어** — Forest Canopy 그린(primary-600 `#457335`), Element Plus 그레이, glass 표면, 그라데이션 버튼. 인디고 폐기 | 사용자 결정 2026-09-03 |
| UI 밀도 | **가독성 우선으로 한 단 상향** — 타입 12/13/14/15/17/21, 라디우스 6/8/10/14 | 사용자 피드백 2026-09-03 |
| 검색 | **커맨드 팔레트** (`⌘K` · `/`). 사이드바 검색창 폐기 | §11.10 사용자 결정 2026-09-03 |
| 응답 뷰 | JSON 본문(인라인 diff) + 데이터 구조 표 **분리**. 별도 `구조 diff` 탭 없음 | §11.5b 사용자 결정 2026-09-03 |
| 요청 폼 | 파라미터·헤더·JSON 본문을 **행 추가**로 더할 수 있다 | §11.11 사용자 결정 2026-09-03 |
| 확정 시안 | `.mockups/api-ui-v7.html` — v1 골격 + v2 팔레트·인라인 diff | 사용자 확정 2026-09-03 |
| exact 모드 범위 | **본문만.** 헤더는 매 호출 변하는 값이 많아 제외하고, 필요한 헤더만 pin 으로 개별 지정 | 사용자 확정 2026-09-04 |
| prod read-only 범위 | **미확정.** 기본 GET/HEAD/OPTIONS, allowlist 여지만 남긴다 | 사용자 판단 유보 2026-09-04 |
| enum 승격 기준 | **1 샘플은 후보 표시만(경고), 3 샘플 이상에서 승격.** 수동 확정 경로 별도 | 사용자 확정 2026-09-04 |
| baseline raw 보관 | **보관.** 시크릿 값만 마스킹한 raw 를 남긴다 | 사용자 확정 2026-09-04 |
| prettier | **채택** — 화면 표시·비-JSON 포맷 전용, 생성 시점에만 실행 | §5.3 |
| 비교 기준선 | RFC 8785 JCS canonical JSON (prettier 아님) | §5.3 |
| 고급 기능 | 생성 시점 precompute로 런타임 의존성 0 유지 | §11.7 |
| 스냅샷 간 구조적 diff | `microdiff` 인라인 — P0 | §11.8 |
| UI | 정적 뷰어 — 의존성 0 단일 `ui.html`, 브라우저 발사 없음 | §11.1 사용자 요청 2026-09-02 |
| 폼 | 편집 가능, `실행`은 커맨드를 클립보드 복사 | §11.2 |
| 기존 렌더러 | 기본 UI 미채택. Redoc CE만 옵트인 보조 | §11.3 |

## 13. 리스크 / 미해결

1. **JSON Schema 역추론 도구 pinning 미확정** — quicktype / GenSON / json-schema-inferrer의 2026 최신 버전을 리서치 예산 안에서 primary source로 확인하지 못했다. 구현 단계에서 짧은 follow-up 리서치가 필요하다. 애초에 추론은 초안일 뿐이고 required/nullable/enum은 사람이 확정해야 한다. §9.2 참고.
2. **Hurl 리포트를 CI artifact로 저장할 경우** 원본 응답 body에 토큰이 남을 수 있다. 저장을 끄거나 후처리 scrubber를 강제해야 한다.
3. **headless Linux**에서는 keychain/libsecret이 없다. `pass`/GPG 또는 환경변수 fallback 경로가 필요하다.
4. **스냅샷 인라인 상한(256KB)의 근거가 관행이지 측정치가 아니다.** 실제 응답 크기 분포를 보고 조정해야 한다. 초과 시 잘라내는 규칙이 diff 정확도를 떨어뜨리는 지점도 확인 필요하다.
5. **`ui.html`을 git에 커밋할지 미결.** dev/stg 스냅샷이 인라인되므로 커밋 가능하나 diff가 매우 시끄럽다. 기본 gitignore + 옵트인이 무난해 보이지만 확정 안 했다.
6. **배열 diff 매칭 기준 미정.** index 기준이면 원소 하나 삽입에 전체가 어긋난다. `id`/`key` 같은 object identity 기준 매칭이 필요한지는 실제 응답을 봐야 정해진다. `microdiff`의 알려진 약점이기도 하다.
7. **스니펫 언어 셋을 4종(curl/fetch/Python/Go)으로 잡았으나 근거가 약하다.** 사용자 스택(Flutter/Rust)을 고려하면 Dart·Rust를 넣는 게 맞을 수 있다. `httpsnippet` 타깃 목록에 둘 다 있는지 확인 필요.
8. **prod read-only 판정을 HTTP 메서드로만 하는 것의 한계** — GET인데 사이드이펙트가 있는 엔드포인트가 실무에 존재한다. 인벤토리에 `sideEffect: true` 수동 표시를 허용한다.

## 14. 생성 파이프라인 체크리스트

`/create-kit`으로 실행한다. 아래 12항목이 모두 끝나야 완료다.

- [ ] `api-kit/` + `plugin.json` + 스킬 5종 `SKILL.md` + `references/` + `evals/`
- [ ] `docs/api/` 리서치 문서 (SSOT — 스킬보다 먼저)
- [ ] `.claude/skills/api-kaizen/`, `.claude/skills/api-research/`
- [ ] `marketplace.json` 등록
- [ ] `CLAUDE.md` Repository Overview + Skills Reference 갱신
- [ ] 루트 `README.md` 자동 갱신 (`sync-docs.py`)
- [ ] `validate-plugin.py` 통과
- [ ] `kaizen-orchestrator` 신규 Phase 등록 (SKILL.md + phase-research-templates.md + phase-dependencies.md)
- [ ] `docs/api-kit/*.html` 페이지 생성
- [ ] `docs/index.html` 카테고리 + getIcon SVG 등록
- [ ] `docs-site/references/css-tokens.md`에 accent 등록 (기존 색과 충돌 확인)
- [ ] qa-evaluator로 docs-site 7 카테고리 검증 PASS
