---
name: api-contract
description: >
  봉인된 응답 스냅샷에서 계약을 추출한다. 스키마(존재·타입·nullable·enum)와 경로별 assertion 을 뽑아
  `.api/contracts/*.yaml` · `.api/cases/*.hurl` · `.api/masks/*.yaml` 을 만들고 baseline 을 봉인한다.
  비교 기준선은 RFC 8785 JCS canonical JSON 이며, 화면 표시용 포매팅과 분리한다.
  "계약 뽑아줘", "스키마 추출", "api contract", "baseline 만들어" 같은 요청 시 트리거.
  회귀 실행·PASS/FAIL 판정에는 트리거하지 않는다 — `/api-verify` 가 담당한다.
  아직 스냅샷이 없어 실제로 때려봐야 하는 단계에도 트리거하지 않는다 — `/api-probe` 가 먼저다.
argument-hint: "<endpoint-id|group> [--mode partial|pin|exact] [--env dev|stg|prod]"
user-invocable: true
---

## Gotchas

- **`pin` 은 '값 고정' 이 아니다 — 경로별 명시 assertion 이다.** 값 고정(`const`)은 pin 이 표현할 수 있는 assertion 한 종류일 뿐이고, 안정 필드(discriminator·통화 코드·고정 status)에만 쓴다. `total`·`cursor`·`id`·`timestamp` 처럼 매 호출 변하는 필드에는 범위·패턴·불변식을 건다 (`$.meta.total >= len($.data)` · `$.orderId ^ord_`). pin 을 payload value freeze 로 구현하면 매 실행 실패한다. **그리고 타입 변경은 pin 이 아니라 partial 이 잡는다** — pin 이 잡는 것은 타입은 멀쩡한 채 값만 망가진 회귀다 (`"Bearer"` → `"bearer"`, `47` → `-1`, `"active"` → `"ACTIVE"` 는 전부 타입이 그대로라 partial 을 통과한다). 이 귀속을 헷갈리면 실패 원인을 잘못 보고하고 엉뚱한 모드를 올려 오탐을 만든다. 출처: `docs/api/contract/contract-extraction-modes.md` §2 · 안티패턴 4행, 설계문서 §9.2.
- **`exact` 는 본문만 본다. 헤더는 diff 대상 0개다.** `Date`·`X-Request-Id` 류가 매 응답 바뀌므로 헤더를 전체 diff 에 넣으면 항상 실패한다. 계약에 필요한 헤더는 `pin` 으로 개별 지정한다 (`Content-Type ^application/json`, `Cache-Control = "no-store"`). 2026-09-04 확정. 출처: `contract-extraction-modes.md` §4.
- **enum 은 1 샘플이면 확정하지 않는다 — 후보 표시 + 경고까지다.** 자동 승격은 독립 샘플 `>=3`, distinct value `>=2`, 최근 20 관측에서 신규 값 없음, domain 크기 `<=12` 를 모두 만족할 때만. 사용자가 직접 확정하는 수동 경로를 따로 둔다. 오탐 실패 한 번이면 사용자는 도구를 끈다. 2026-09-04 확정. 출처: `contract-extraction-modes.md` §7 · 수치 기준.
- **`required` 는 관측 샘플 presence 100% 일 때만이고, `null` 은 missing 이 아니다.** 단일 스냅샷 추론은 `required` / `optional` / `미확정` 3분류로 제시하고 사용자에게 확정받는다 — 스냅샷 하나에서 본 필드를 required 로 올리는 것 자체가 오탐 생성기다. `null` presence 를 부재로 세면 nullable 필드가 optional 로 오분류되어 필드 소실 회귀를 놓친다. 출처: `contract-extraction-modes.md` §5·§6, 설계문서 §9.2.
- **비교 기준선은 JCS 이고, 정규화 전에 I-JSON 게이트를 먼저 통과시킨다.** pretty-print 결과·키 삽입 순서·diff UI 문자열을 해싱해 기준선으로 쓰면 표시 포매터가 바뀔 때 계약이 통째로 깨진다. 중복 키·NaN/Infinity·lone surrogate·안전 정수 범위(`±9007199254740991`) 밖 숫자는 정규화 대상이 아니라 **실패 또는 fallback 대상**이다. 파서가 "last key wins" 로 삼킨 뒤 검사하면 이미 값이 소실된 상태다. **배열은 정렬하지 않는다** — JCS 는 object property 만 재귀 정렬하고 array order 는 보존한다. 배열을 정렬해 안정화하면 실제 순서 회귀가 은폐되고, 정렬 보장 없는 컬렉션의 순서는 pin 대상이 아니라 variance 신호다(`$.data[0].id` 같은 index assertion 금지). 출처: `snapshot-sealing-canonicalization.md` §2·§3 · 안티패턴 3행, `multi-sample-pagination-variance.md` §5.
- **partial 에서 스키마를 닫지 마라.** `additionalProperties: false` 는 exact 또는 사용자가 명시한 strict 설정에서만 쓴다. partial 에서 닫으면 서버의 정상적인 필드 추가가 전부 회귀로 보고된다. pin 은 명시한 path 만 검사하고 나머지는 열어 둔다. 출처: `contract-extraction-modes.md` §1·§9.
- **컬렉션은 한 덩어리로 계약하지 않는다 — envelope · item · pagination marker 세 조각이다.** 첫 페이지 item 개수를 컬렉션 길이로 봉인하면 서버 page size 를 데이터 크기로 착각한다. cursor/`nextLink` 는 opaque 이므로 파싱·합성하지 않고 존재·타입만 계약한다. `nextLink: null` 을 표준 종료 marker 로 일반화하지 마라 — 부재와 null 은 다른 신호다. 출처: `multi-sample-pagination-variance.md` §3·§4·§9 · Gotchas 1행.
- **오류 응답은 machine-readable 필드로만 계약한다.** `detail` 같은 사람용 설명 문자열을 exact match 로 고정하면 문구·다국어 변경만으로 깨진다. problem+json 은 `type` URI 가 1차 식별자이고 `type` 누락(= `about:blank`)은 위반이 아니다. 5xx 본문 exact pin 은 0개 — status class + envelope 형태 + retry metadata 만 검증한다. 출처: `error-status-contracts.md` §1·§3·§9.
- **`.hurl` 합성 규칙 3가지를 어기면 케이스가 조용히 틀린다.** (1) URL query 와 `[Query]` 섹션을 동시에 만들면 Hurl 이 둘 다 전송해 파라미터가 중복된다 — `[Query]` 한 경로만 쓴다. (2) 로그인→조회 같은 의존 흐름은 반드시 한 파일에 둔다. `--test` 는 파일 단위 병렬 실행이라 파일 경계가 곧 격리 경계다. (3) `Accept` · `Content-Type` · `Authorization` 은 추론에 맡기지 말고 명시 생성한다 — 생략하면 실패 원인이 계약인지 전송인지 구분되지 않는다. 시크릿 값은 `.hurl` 본문에 절대 쓰지 않고 주입한다. 그리고 **Hurl assert 는 경로 하나에 predicate 하나**이므로 `$.meta.total >= len($.data)` 같은 경로 간 불변식은 `.hurl` 이 아니라 `contracts/*.yaml` 의 `pin` 으로만 기록하고 `/api-verify` 후처리에서 검사한다 — 상수로 박아 넣으면(`>= 3`) 데이터가 늘어난 순간 오탐이 된다(Hurl 은 JSON Schema assert 가 네이티브가 아니다, 설계문서 §5.1). 출처: `probe-synthesis-hurl-semantics.md` §2·§3·§5, `auth-secret-lifecycle.md` §4.
- **baseline 은 시크릿 값만 마스킹한 raw 를 보관하고, redaction 은 저장 전 fail-closed 게이트다.** 요약본·스키마만 남기면 값 drift 를 재현할 수 없고, 마스킹 없는 raw 를 남기면 저장소가 자격증명 저장소가 된다. redaction 이 실패하면 스냅샷을 저장하지 않는다. prod 스냅샷은 커밋하지 않고 스키마 계약만 커밋한다(prod evidence 커밋 0건). 2026-09-04 확정. 출처: `baseline-governance-promotion.md` §2·§3·§10, 설계문서 §8.2·§8.3.

# 응답 스냅샷에서 계약 추출

## 0. 입력 확인과 스냅샷 로드

`$ARGUMENTS` 에서 파싱하거나 사용자에게 확인한다.

| 항목 | 예시 | 기본값 |
|---|---|---|
| 대상 | `orders.list` 또는 그룹 `orders.*` | 필수 |
| 환경 | `dev` / `stg` / `prod` | `.api/project.yaml` 의 기본 env |
| 모드 힌트 | `partial` / `pin` / `exact` | `partial` |

`.api/snapshots/<env>/<id>*.json` 을 모두 읽는다. 스냅샷이 0개면 **중단**하고 안내한다:

> 스냅샷이 없습니다. `/api-probe <endpoint-id>` 로 먼저 실제 응답을 봉인하세요.

---

## 1. 샘플 예산 점검

단일 응답은 계약이 아니라 후보다. 아래 하한을 채웠는지 먼저 확인한다.

| 항목 | 기준 |
|---|---|
| 일반 샘플 예산 | 최소 `3` captures, 최대 `5` pages 또는 `500` items |
| 컬렉션 대표 페이지 | first · next 중 최소 하나 · terminal 세 종류 |
| 수집 중지 후보 | 연속 `2` 페이지에서 신규 path/type 없음 |
| prod 샘플링 method | `GET` · `HEAD` · `OPTIONS` (2026-09-04 기본값) |

부족하면 사용자에게 선택지를 준다 — (a) `/api-probe` 로 샘플을 더 모은다, (b) 부족한 채로 진행하되 `required`·`enum` 을 전부 **미확정**으로 표시한다. 조용히 (b) 로 넘어가지 마라.

---

## 2. I-JSON 게이트

JCS 로 넘기기 전에 검문한다. 아래는 정규화 대상이 아니라 실패 또는 fallback 대상이다.

```text
중복 object member                  → 실패 (허용치 0)
NaN / Infinity                      → 실패
lone surrogate / noncharacter       → 실패
IEEE 754 binary64 표현 불가 숫자     → 실패
안전 정수 범위 밖 (±9007199254740991) → 경고 + 문자열 보존 검토
```

게이트 실패는 계약 실패가 아니라 **봉인 불가**다. 원인 경로를 그대로 보고하고 해당 필드를 마스크로 격리할지 사용자에게 묻는다.

---

## 3. 변동성 점수화 + `masks/*.yaml` 초안

path 별로 presence · type set · scalar churn · 배열 길이 · 순서 churn 을 계산한다. 점수 없이 승격하면 partial 로 충분한 필드에 pin 이 붙어 오탐이 쌓인다.

timestamp · uuid · nonce · cursor 류는 **raw 를 건드리지 말고 normalized 단계의 path registry** 로 처리한다.

```yaml
# .api/masks/orders.list.yaml
version: 1
id: orders.list
paths:
  - { path: "$.meta.requestId",   rule: sentinel, as: "<uuid>" }
  - { path: "$.data[].createdAt", rule: sentinel, as: "<ts>" }
  - { path: "$.meta.nextCursor",  rule: opaque }          # 존재·타입만, 값 비교 제외
  - { path: "$.data[].price",     rule: round, digits: 2 }
secrets:
  - { path: "$.accessToken", rule: mask }                 # 값만 가리고 자리는 유지
```

마스크 규칙 자체를 계약과 함께 버전 관리한다. 승격 전에 마스크부터 확정한다 — 비결정 필드를 그대로 승격하면 이후 모든 실행이 실패한다.

---

## 4. JCS 정규화로 비교 기준선 생성

순서를 지킨다. **redaction → 마스크 적용 → JCS 직렬화.**

- JCS: 토큰 사이 공백 `0 byte`, ECMAScript primitive serialization, object property 재귀 정렬, UTF-8 출력.
- property sort 는 UTF-16 code unit 순서다. 자체 구현 정렬을 쓰지 말고 JCS 구현을 쓴다.
- Unicode normalization(NFC/NFD)은 하지 않는다. "같아 보이는데 digest 가 다르다" 는 대부분 이 케이스다.
- 화면 표시용 pretty print 는 별도 산출물이다. **절대 기준선으로 쓰지 않는다.**
- `Content-Encoding: gzip` 이면 raw content digest 와 decoded representation digest 를 구분해 기록한다.

---

## 5. 스키마 초안 추론

추론은 초안일 뿐이다. 아래를 path 별로 뽑는다.

| 항목 | 규칙 |
|---|---|
| 타입 | 관측된 type set. 섞이면 union(`anyOf`)으로 일반화 — 첫 item 기준 금지 |
| nullable | `type: ["string", "null"]` 로 명시. `null` 과 missing 을 합치지 않는다 |
| required | presence 100% 만 후보. 그 외는 `optional`, 샘플 부족은 `미확정` |
| enum | 승격 조건 미달이면 `enumCandidate` 로만 기록 + 경고 |
| format | annotation 으로만 기록. hard fail 로 쓰려면 사용자 확정 필요 |
| 배열 | envelope / item / pagination marker 를 분리 (§3 컬렉션 규칙) |

빈 배열이나 item 하나로 `items` 를 확정하지 마라.

---

## 6. 사용자 확정 게이트 (건너뛰기 금지)

추론 결과를 표로 제시하고 확정받는다. 이 단계 없이 파일을 쓰지 않는다.

```text
$.data[].id          string   required   (3/3 샘플)
$.data[].status      string   required   enum 후보 [active, shipped] — 샘플 2개, 확정 보류 ⚠
$.data[].cancelledAt string?  optional   (1/3 샘플, null 1건)
$.meta.nextCursor    string?  미확정     terminal 페이지 미수집
```

확정 항목: (1) required/optional/미확정 3분류, (2) enum 후보의 수동 승격 여부, (3) 마스크 대상, (4) 모드.

---

## 7. 모드 배정

기본은 `partial` 이다. 아래 자격을 통과한 것만 올린다. 상세 표는 `references/strictness-modes.md`.

```text
partial (기본)  존재 · 타입 · enum          — 형태만 본다. 스키마를 닫지 않는다
pin             위 + 경로별 명시 assertion   — 타입은 멀쩡한데 값만 망가진 회귀를 잡는다
exact           정규화 후 본문 전체 diff     — 헤더 제외
```

`exact` 자격: 동일 request fingerprint 로 `>=3` 회 반복 후 normalized JCS digest variance `0`.
컬렉션 exact 는 추가로 — 안정 정렬/cursor 존재, duplicate stable id `0`, ordering variance `0`, item schema variance `0`. 네 조건 중 하나만 깨져도 매 실행 실패한다.

`pin` assertion 은 필드 성격에 맞춰 고른다.

| 필드 성격 | assertion | 예 |
|---|---|---|
| 안정값 | 값 고정 (`const`) | `$.token_type = "Bearer"` |
| 열거형 | 집합 소속 | `$.data[].status ∈ {active, shipped, cancelled}` |
| 변동 수치 | 범위·불변식 | `$.meta.total >= len($.data)` · `$.price > 0` |
| 식별자 | 패턴 | `$.orderId ^ord_` |
| 컬렉션 | 개수 불변식 | `$.data[].isDefault == true` 인 항목 정확히 1개 |
| 헤더 | predicate | `Content-Type ^application/json` |

---

## 8. `contracts/*.yaml` 작성

```yaml
# .api/contracts/orders.list.yaml
version: 1
id: orders.list
env: dev
mode: partial                      # partial | pin | exact
request:
  method: GET
  path: /v1/orders
  query: { status: active, limit: "10" }
response:
  status: 200
  statusPolicy: exact              # exact | class(2xx/4xx/5xx)
schema:
  additionalProperties: open       # partial 은 연다. exact 에서만 닫는다
  paths:
    "$.data":              { type: array,             required: true }
    "$.data[].id":         { type: string,            required: true }
    "$.data[].status":     { type: string,            required: true,
                             enumCandidate: [active, shipped], samples: 2, confirmed: false }
    "$.data[].cancelledAt": { type: [string, "null"], required: false }
    "$.meta.total":        { type: integer,           required: true }
    "$.meta.nextCursor":   { type: [string, "null"],  required: undetermined }
pin:
  - { path: "$.meta.total",   assert: ">= len($.data)" }        # 경로 간 불변식 — verify 후처리
  - { path: "$.orderId",      assert: "matches ^ord_" }
  - { header: "Content-Type", assert: "matches ^application/json" }
exact: false                        # true 이면 본문만 전체 diff. 헤더는 포함하지 않는다
masks: masks/orders.list.yaml
collection:
  envelope: { totalPath: "$.meta.total", cursorPath: "$.meta.nextCursor" }
  terminalSignal: "nextCursor 부재"   # null 과 부재를 구분해 기록
  orderGuaranteed: false             # false 면 index 기반 pin 금지
```

오류 케이스는 별도 계약 파일로 뺀다. 4xx 는 deterministic 하면 exact status pin 후보, 5xx 는 status class + envelope + `Retry-After` 만 계약한다(`Retry-After` 는 delay-seconds 와 HTTP-date 둘 다 파싱).

---

## 9. `cases/*.hurl` 합성

```hurl
# .api/cases/orders.list.hurl
GET {{baseUrl}}/v1/orders
Accept: application/json
Authorization: Bearer {{access_token}}
[Query]
status: active
limit: 10

HTTP 200
[Asserts]
header "Content-Type" matches "^application/json"
jsonpath "$.data" isCollection
jsonpath "$.data[0].id" isString
jsonpath "$.meta.total" isInteger
```

지킬 것:

- query 는 `[Query]` 한 경로만. URL 문자열에 중복 생성 금지.
- 의존 흐름(로그인 → 조회 → 삭제)은 한 파일 안에. `[Captures]` 이름을 체인 안에서 재사용하지 않는다.
- 최소 assert 는 expected status 하나. body 전체 capture 는 downstream 이 실제로 쓰거나 진단 목적일 때만 켠다.
- cli-only 옵션을 `[Options]` 에 적지 않는다 — 무시되어 파일과 실제 실행이 어긋난다.
- 시크릿은 본문에 쓰지 않는다. `/api-verify` 가 실행 직전 `--secrets-file` 로 주입한다.

---

## 10. baseline 봉인

baseline id 는 응답 바이트가 아니라 **매니페스트의 digest** 로 만든다.

```yaml
baseline:
  manifestDigest: sha-256:<...>
  rawDigest: sha-256:<...>            # 마스킹된 raw 기준
  normalizedDigest: sha-256:<...>     # JCS 결과 기준
  redactionRegistry: masks/orders.list.yaml@v1
  mediaType: application/json
  extractionMode: partial
  lineage: { env: dev, branch: main, capturedAt: 2026-09-04T02:11:07Z, samples: 3 }
  state: pending                      # pending | accepted — 첫 성공 verification 전까지 pending
  expiresAt: 2026-10-04               # 30일 warning / 90일 block
```

- 승인본은 소스 컨트롤에, 실행 산출물(`.received.*`)은 커밋 0건.
- prod 는 raw 스냅샷을 커밋하지 않고 스키마 계약만 커밋한다.
- `.gitignore` 에 `reports/`, `snapshots/prod/`, `credentials.local.json` 이 등록돼 있는지 확인한다. 없으면 등록하고 보고한다.
- 마스킹 규칙에만 의존하지 않는다 — gitignore + secret scanning 이중 방어다.

---

## 11. 보고

생성/수정 파일 목록과 함께 아래를 명시한다.

1. 모드 배정 결과 (partial / pin / exact 각 몇 개, 승격 근거)
2. **미확정으로 남긴 항목** — required 미확정, enum 후보, 자격 미달로 exact 를 못 올린 케이스
3. 샘플 부족으로 유보한 판정
4. 다음 단계 안내:
   - 회귀 검증은 `/api-verify <id>` 로 실행하세요.
   - baseline 은 `pending` 입니다. 첫 성공 verification 이 기록되면 `accepted` 로 전환됩니다 — 그 전 실패는 게이트를 깨지 않습니다.

# References

- references/strictness-modes.md — 모드별 assertion 어휘·승격 기준·자격 조건
- ../../../docs/api/contract/contract-extraction-modes.md — partial · pin · exact 판정 규칙
- ../../../docs/api/contract/snapshot-sealing-canonicalization.md — JCS·I-JSON 게이트·매니페스트 해싱
- ../../../docs/api/contract/multi-sample-pagination-variance.md — 샘플 예산·페이지네이션 계약
- ../../../docs/api/contract/error-status-contracts.md — 오류·상태 코드 계약
- ../../../docs/api/execution/probe-synthesis-hurl-semantics.md — `.hurl` 합성과 Hurl 실행 의미론
- ../../../docs/api/execution/auth-secret-lifecycle.md — 시크릿 주입·마스킹 한계
- ../../../docs/api/verification/baseline-governance-promotion.md — baseline 보관 형식·lineage·만료
- ../../../docs/superpowers/specs/2026-09-02-api-kit-design.md — §7.3 스킬 정의 · §9 정규화와 계약 실패 기준
