---
title: 계약 추출 모드 — partial · pin · exact
version: 0.1.0
last_updated: 2026-09-04
---

# 계약 추출 모드 — partial · pin · exact

봉인된 baseline 에서 어떤 강도의 계약을 뽑을지 결정하는 규칙.
강도는 3단계이며, 각 단계는 잡아내는 회귀의 종류가 다르다.

```text
partial (기본)  존재 · 타입 · enum          — 형태만 본다
pin             위 + 경로별 명시 assertion   — 타입은 멀쩡한데 값만 망가진 회귀를 잡는다
exact           정규화 후 본문 전체 diff
```

---

## 원칙

### 1. partial 은 최소 계약이다

partial 은 관측된 안정 필드에 대한 최소 계약이다.
JSON Schema 에서 `properties` 는 명시된 필드만 검증하고 `additionalProperties` 를 생략하면 열린 schema 로 동작한다.
partial 에서는 객체를 닫지 않는다 — 서버가 필드를 추가했다는 이유로 실패하면 안 된다.

> **출처:** [JSON Schema 2020-12 Core](https://json-schema.org/draft/2020-12/json-schema-core)

### 2. pin 은 '값 고정' 이 아니라 경로별 명시 assertion 이다

pin 은 payload 를 얼리는 모드가 아니다. **경로마다 하나의 assertion 을 명시**하는 모드다.
assertion 종류는 exists, type, nullable, pattern, range, enum, const, header predicate 등이며,
값 고정(`const`)은 그중 한 종류일 뿐이다. `total`·`cursor`·`id`·`timestamp` 처럼 매번 변하는 필드에는 범위·패턴·불변식을 건다.

```text
$.token_type = "Bearer"                        값 고정 (const)
$.meta.total >= len($.data)                    불변식
$.data[].status ∈ {active, shipped, cancelled} 집합
$.orderId ^ord_                                패턴
$.createdAt : string(date-time)                타입 + format
```

> **출처:** [JSON Schema 2020-12 Validation](https://json-schema.org/draft/2020-12/json-schema-validation)

### 3. exact 는 자격 조건을 통과해야 쓴다

exact 는 변동 필드 레지스트리를 적용한 뒤 JCS 정규화 payload 전체가 안정적일 때만 가능하다.
JCS 는 object key order 를 제거하지만 array order 와 값 변화는 그대로 계약 차이로 남긴다.
자격 미달인 응답에 exact 를 걸면 매 실행이 실패하고, 그 실패는 곧 무시된다.

> **출처:** [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html)

### 4. exact 는 본문만 본다

exact diff 대상은 **응답 본문뿐**이다(2026-09-04 결정).
`Date` 는 응답마다 생성되는 필드이고 `X-Request-Id` 류도 매 호출 달라지므로 헤더를 전체 diff 에 넣으면 항상 실패한다.
계약에 필요한 헤더는 exact 가 아니라 **pin 으로 개별 지정**한다 — 예: `Content-Type ^application/json`, `Cache-Control = "no-store"`.

> **출처:** [RFC 9110 HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110), [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html)

### 5. required 와 optional 은 샘플 교집합으로 판정한다

`required` 는 property name 의 존재 조건이지 값의 non-null 조건이 아니다.
GenSON 은 관측된 모든 object 에 등장한 key 의 교집합만 required 로 삼는다.
단일 샘플에서 본 필드를 required 로 올리는 것은 그 자체로 오탐 생성기다.

> **출처:** [JSON Schema 2020-12 Validation](https://json-schema.org/draft/2020-12/json-schema-validation), [GenSON](https://github.com/wolverdude/GenSON)

### 6. null 과 missing 을 합치지 않는다

`null` 은 '없는 필드' 가 아니라 하나의 JSON 값이다.
JSON Schema 에서는 `type: ["string", "null"]` 처럼 null type 을 명시해야 하고,
OpenAPI 3.0 의 `nullable` 은 같은 Schema Object 에 `type` 이 있을 때만 의미가 있다.

> **출처:** [JSON Schema — null](https://json-schema.org/understanding-json-schema/reference/null), [OpenAPI 3.0.4](https://spec.openapis.org/oas/v3.0.4.html)

### 7. enum 은 1 샘플이면 후보로만 표시한다

JSON Schema `enum` 은 닫힌 값 집합이고 `const` 는 단일 값 enum 과 동등하다 — 둘 다 관측 밖의 값을 실패시킨다.
그래서 **1 샘플에서는 enum 을 확정하지 않고 후보로 표시하며 경고만 낸다**(2026-09-04 결정).
3 샘플 이상에서 승격하고, 사용자가 직접 확정하는 수동 경로도 둔다. 오탐 실패가 도구 신뢰를 가장 빨리 깎기 때문이다.
GenSON 은 seed 없이는 enum 을 아예 추론하지 않고, json-schema-inferrer 는 enum extractor 를 별도 설정으로 분리한다.

> **출처:** [JSON Schema 2020-12 Validation](https://json-schema.org/draft/2020-12/json-schema-validation), [GenSON](https://github.com/wolverdude/GenSON), [json-schema-inferrer](https://github.com/saasquatch/json-schema-inferrer)

### 8. 배열 item 은 union 으로 일반화한다

JSON array 의 원소는 같은 type 일 필요가 없다.
여러 샘플·여러 item 에서 type 이 섞이면 첫 item 기준 schema 를 쓰지 말고 union/`anyOf` 계열로 일반화한다.

> **출처:** [RFC 8259 JSON](https://www.rfc-editor.org/rfc/rfc8259.html), [json-schema-inferrer](https://github.com/saasquatch/json-schema-inferrer)

### 9. additionalProperties 정책은 모드가 결정한다

`additionalProperties: false` 는 관측되지 않은 모든 property 를 실패시키는 strict 정책이다.
partial 에서는 열고, pin 에서는 명시한 path 만 검사하고, exact 에서만 전체 diff 로 닫는다.
모드와 무관하게 닫으면 서버의 정상적인 필드 추가가 전부 회귀로 보고된다.

> **출처:** [JSON Schema 2020-12 Core](https://json-schema.org/draft/2020-12/json-schema-core)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| `required` 승격 조건 | scoped sample 내 presence `100%` | 관측 object 전체의 key 교집합 ([GenSON](https://github.com/wolverdude/GenSON)) |
| `optional` 판정 | presence `<100%`. `null` presence 는 missing 으로 세지 않음 | null 은 값이지 부재가 아님 ([JSON Schema null](https://json-schema.org/understanding-json-schema/reference/null)) |
| `additionalProperties: false` 허용 unexpected property | `0` — exact 또는 명시 strict 설정에서만 | strict 정책 정의 ([JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core)) |
| `const` 승격 | 사용자 pin 또는 공식 API spec 근거 필요. 단일 샘플 값만으로는 금지 | 추론 — JSON Schema 상 `const` 는 단일 허용값이라 오탐 비용이 큼 |
| enum 자동 승격 | 독립 샘플 `>=3`, distinct value `>=2`, 최근 `20` 관측에서 신규 값 없음, domain 크기 `<=12` | 추론 — GenSON 의 "seed 없이는 enum 미추론" 을 보수 기준으로 채택 |
| enum 1 샘플 처리 | 확정 금지, 후보 표시 + 경고 | 2026-09-04 결정 — 오탐 실패가 도구 신뢰를 가장 빨리 깎음 |
| exact 자격 | 동일 request fingerprint 로 `>=3` 회 반복 후 normalized JCS digest variance `0` | 추론 — JCS digest 안정성 실측 |
| exact diff 대상 | 응답 본문만. 헤더 `0`개 | 2026-09-04 결정 — `Date`·`X-Request-Id` 등 매 응답 변동. 필요한 헤더는 pin |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 단일 샘플 scalar 를 바로 `const` 또는 닫힌 `enum` 으로 승격 | 두 번째 정상 값이 회귀로 보고된다. 오탐 한 번이면 사용자는 도구를 끈다 |
| `null` 을 missing 과 합쳐 optionality 계산 | nullable 필드가 optional 로 오분류되어 필드 소실 회귀를 놓친다 |
| partial 모드에서 `additionalProperties: false` 를 기본값으로 사용 | 서버의 정상적 필드 추가가 전부 실패로 잡힌다 |
| pin 을 payload 전체 value freeze 로 구현 | `total`·`cursor`·`timestamp` 때문에 매번 실패한다. pin 은 경로별 assertion 이다 |
| 빈 배열이나 첫 item 하나로 `items` schema 확정 | 이후 등장하는 다른 type 원소가 전부 위반이 된다. union 으로 일반화해야 한다 |

---

## Gotchas

- **`required` 는 non-null 을 보장하지 않는다** — 필드가 있어도 값이 `null` 일 수 있다. non-null 을 원하면 type 에서 `null` 을 제외해야 한다.
- **`format` 은 구현마다 annotation/assertion 지원이 다르다** — format 을 hard fail 조건으로 쓰려면 validator 설정에 명시적으로 묶어야 한다. 안 그러면 조용히 통과한다.
- **OpenAPI 3.0 `nullable: true` 는 다른 제약을 무력화하지 않는다** — `enum` 에 `null` 이 없으면 nullable 을 켜도 null 이 실패한다.
- **composition 에서는 `additionalProperties` 보다 `unevaluatedProperties` 가 정확하다** — `additionalProperties` 는 같은 schema object 의 `properties`/`patternProperties` annotation 에만 의존하기 때문이다.
