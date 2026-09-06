---
title: API 인벤토리 정규화
version: 0.1.0
last_updated: 2026-09-04
---

# API 인벤토리 정규화

OpenAPI 스펙 / 사람이 쓴 md / curl·Talend 덤프를 하나의 operation 인벤토리로 합칠 때 적용하는 판단 규칙. 키 표준화, 출처 신뢰도, 충돌 처리, 커버리지 집계를 다룬다.

---

## 원칙

### 1. Operation Key 표준화

operation의 기본 키는 `METHOD + normalized path template` 로 잡는다. `operationId` 는 별칭 컬럼에만 저장하고 키로 쓰지 않는다. `operationId` 는 있으면 유일해야 하지만 선택 필드이고 대소문자를 구분하므로, 원시 키로 삼으면 md·curl 출처와 매칭이 깨진다.

> **출처:** [OpenAPI 3.1.0 Operation Object](https://spec.openapis.org/oas/v3.1.0#operation-object)

### 2. Source Confidence Matrix

출처마다 구조 신뢰도를 다르게 매기고, 모든 필드에 provenance 를 남긴다. 유효한 OpenAPI 는 계약 설명 형식이므로 최상위, curl·Talend·HAR 는 "실제로 본 호출" 증거, 사람이 쓴 md 는 설명 증거다. 신뢰도가 높은 출처라도 낮은 출처의 값을 자동 덮어쓰지 않는다 — 덮어쓰면 drift 가 사라진다.

> **출처:** [OpenAPI 3.1.0 Introduction](https://spec.openapis.org/oas/v3.1.0#introduction)

### 3. Path Template Resolution

concrete path 는 templated path 보다 먼저 매칭한다. `/users/me` 는 `/users/{id}` 보다 우선한다. 같은 hierarchy 에서 `{id}` 와 `{name}` 처럼 변수명만 다른 path 는 동일 path 로 보고 무효 처리한다. 모호한 후보는 임의 선택하지 않고 conflict 로 남긴다.

> **출처:** [OpenAPI 3.1.0 Paths Object](https://spec.openapis.org/oas/v3.1.0#paths-object)

### 4. Parameter Location Canonicalization

파라미터 키는 `(in, name)` 쌍이다. `in` 은 `path` / `query` / `header` / `cookie` 넷으로 정규화하고, `in: path` 는 항상 required 로 강제한다. HTTP header 이름은 case-insensitive 이지만 OpenAPI 파라미터 이름 자체는 case-sensitive 이므로, header 비교만 case-fold 하고 나머지는 원문 그대로 비교한다.

> **출처:** [OpenAPI 3.1.0 Parameter Object](https://spec.openapis.org/oas/v3.1.0#parameter-object), [RFC 9110 Field Names](https://www.rfc-editor.org/rfc/rfc9110.html#name-field-names)

### 5. Reserved Protocol Headers 분리

`Accept`, `Content-Type`, `Authorization` 은 파라미터 테이블에 넣지 않는다. OpenAPI 는 이 셋을 header parameter 로 정의해도 무시한다. 각각 media negotiation, requestBody media type, security requirement 에서만 파생시킨다.

> **출처:** [OpenAPI 3.1.0 Parameter Object](https://spec.openapis.org/oas/v3.1.0#parameter-object)

### 6. Media Type 우선순위

request/response `content` 에서 여러 media range 가 동시에 매칭되면 가장 구체적인 key 하나만 적용한다. `text/plain` 이 `text/*` 보다 우선한다. wildcard 는 fallback 후보 목록에만 남기고 기본 선택값으로 쓰지 않는다.

> **출처:** [OpenAPI 3.1.0 Request Body Object](https://spec.openapis.org/oas/v3.1.0#request-body-object), [OpenAPI 3.1.0 Response Object](https://spec.openapis.org/oas/v3.1.0#response-object)

### 7. Auth Scope Mapping

operation-level `security` 가 있으면 top-level `security` 를 override 한다. security requirement 배열의 원소 간 관계는 OR, 한 객체 안의 여러 scheme 은 AND 다. OAuth2/OpenID Connect scheme 의 값 배열은 scope 목록이고, 그 외 scheme 은 빈 배열이어야 한다.

> **출처:** [OpenAPI 3.1.0 Security Requirement Object](https://spec.openapis.org/oas/v3.1.0#security-requirement-object)

### 8. Duplicate Collapse + Conflict Flagging

canonical key 가 같은 후보만 collapse 한다. method, path template, parameter location, auth scheme, media type 중 하나라도 충돌하면 병합하지 않고 conflict 레코드로 보존한다. 충돌을 버리는 순간 인벤토리는 계약 검증 근거로 쓸 수 없다.

> **출처:** [OpenAPI 3.1.0 Operation Object](https://spec.openapis.org/oas/v3.1.0#operation-object), [OpenAPI 3.1.0 Paths Object](https://spec.openapis.org/oas/v3.1.0#paths-object)

### 9. Coverage Accounting 분리

커버리지는 단일 숫자로 합치지 않는다. `OpenAPI operation`, `observed-only request`(스펙에 없는데 덤프에서 관측된 호출), `generated probe` 세 축을 각각 센다. 합산하면 스펙에 없는 실호출이 커버리지에 흡수돼 블랙박스 검증의 핵심 신호가 사라진다.

> **출처:** [OpenAPI 3.1.0 Paths Object](https://spec.openapis.org/oas/v3.1.0#paths-object)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| operation/path item 내 `(name, in)` 중복 허용치 | `0` | [OpenAPI Operation Object](https://spec.openapis.org/oas/v3.1.0#operation-object) |
| 같은 hierarchy 내 path template ambiguity 허용치 | `0` | [OpenAPI Paths Object](https://spec.openapis.org/oas/v3.1.0#paths-object) |
| header name case 구분 | `0` (case-insensitive 비교) | [RFC 9110 Field Names](https://www.rfc-editor.org/rfc/rfc9110.html#name-field-names) |
| `servers` 누락 시 기본 server URL | `/` | [OpenAPI Object](https://spec.openapis.org/oas/v3.1.0#openapi-object) |
| source confidence 기본값 | OpenAPI `1.00` / observed curl·Talend·HAR `0.80` / md `0.55` / synthetic inference `0.35` | 추론 |
| auto-collapse 조건 | method·path-template exact match **그리고** param-set Jaccard `>= 0.80` | 추론 |
| conflict 판정 임계 | top-2 후보 confidence 차이 `< 0.15` | 추론 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| `operationId` 만으로 dedupe | 선택 필드라 외부 덤프에는 대부분 없어 dedupe 자체가 동작하지 않는다 |
| raw path 문자열만 비교 | `/users/me` 와 `/users/{id}` 의 우선순위를 놓쳐 잘못된 operation 에 probe 를 붙인다 |
| path/query/header/cookie 를 한 namespace 에 병합 | 이름이 같고 위치가 다른 파라미터가 서로를 덮어써 사라진다 |
| `Authorization` 을 일반 header parameter 로 저장 | auth scheme·scope 판단 경로가 끊겨 인증 요구사항을 재현할 수 없다 |
| 충돌 시 가장 최신 파일만 채택 | 스펙과 실호출의 drift 를 숨긴다 — 계약 검증 문서로서의 가치가 사라진다 |

---

## Gotchas

- **OpenAPI path template 변수값에는 unescaped `/`, `?`, `#` 가 들어갈 수 없다** — 관측 덤프의 concrete URL 을 역으로 템플릿화할 때 슬래시가 포함된 세그먼트를 하나의 `{id}` 로 접으면 실제로는 존재하지 않는 operation 을 만든다. 세그먼트 경계에서만 변수화한다.
- **`GET` request body 는 문법상 허용되지만 의미가 정의돼 있지 않다** — 스펙에 `GET` + requestBody 가 있어도 probe 기본값으로 body 를 생성하지 않는다. 서버·프록시마다 처리가 달라 실패가 계약 위반인지 전송 계층 문제인지 구분되지 않는다.
- **md·curl 예시는 auth·base URL·environment 를 생략하는 경우가 많다** — 이런 출처는 "불완전한 관측치" 로 표시하고, 누락 필드를 기본값으로 채우지 말고 미상(unknown)으로 남긴다. 채우면 스펙과의 diff 가 가짜로 사라진다.
- **`operationId` 는 대소문자를 구분한다** — `getUser` 와 `GetUser` 는 서로 다른 별칭이다. 별칭 매칭에서 case-fold 하면 서로 다른 operation 이 하나로 붙는다.
