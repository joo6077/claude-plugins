# 계약 강도 모드 — partial · pin · exact

`/api-contract` 가 모드를 배정할 때 쓰는 유일한 기준. 각 모드가 **어떤 회귀를 잡고 어떤 회귀를 놓치는지**,
승격 자격이 무엇인지, 어떤 assertion 어휘를 쓰는지 정의한다.
원 규칙은 `../../../../docs/api/contract/contract-extraction-modes.md` 이고, 여기서는 실행 판정용으로만 정리한다.

---

## 1. 세 모드의 역할

```text
partial (기본)  존재 · 타입 · enum          — 형태만 본다
pin             위 + 경로별 명시 assertion   — 타입은 멀쩡한데 값만 망가진 회귀를 잡는다
exact           정규화 후 본문 전체 diff     — 헤더는 보지 않는다
```

| 모드 | 검사 내용 | 스키마 개폐 | 지정 방법 |
|---|---|---|---|
| `partial` | 상태코드, content-type, 필수 필드 존재, 타입 일치, 확정된 enum | **열림** (`additionalProperties` 미지정) | 기본값 |
| `pin` | partial + 지정 경로별 assertion 1개 | 명시한 path 만 검사, 나머지는 열림 | `pin: [{path, assert}]` |
| `exact` | 마스크 적용 후 JCS 정규화 **본문** 전체 diff | 닫힘 | `exact: true` |

`exact` 를 기본으로 두면 서버가 필드 하나 추가할 때마다 깨지고, `partial` 만 두면 조용한 회귀를 놓친다.
그래서 중요한 필드만 `pin` 으로 올리는 중간 단계를 둔다.

---

## 2. 모드별로 잡는 회귀 / 놓치는 회귀

| 회귀 사례 | partial | pin | exact |
|---|---|---|---|
| 필드 삭제 (`$.data[].status` 사라짐) | 잡음 | 잡음 | 잡음 |
| 타입 변경 (`total: 47` → `"47"`) | **잡음** | 잡음 | 잡음 |
| nullable 위반 (`null` 불가 필드에 `null`) | 잡음 | 잡음 | 잡음 |
| 값 케이싱 변경 (`"Bearer"` → `"bearer"`) | 통과 | **잡음** | 잡음 |
| 센티널 값 (`total: 47` → `-1`) | 통과 | **잡음** | 잡음 |
| enum 값 변경 (`"active"` → `"ACTIVE"`) | 확정 enum 이면 잡음 | 잡음 | 잡음 |
| 불변식 파괴 (`total < len(data)`) | 통과 | **잡음** | 잡음 |
| 식별자 prefix 변경 (`ord_` → `o-`) | 통과 | **잡음** | 잡음 |
| 필드 추가 (서버가 새 필드 반환) | 통과(정상) | 통과(정상) | **실패** |
| 배열 순서 변경 | 통과 | 순서 pin 이 있으면 잡음 | 잡음 |

**타입 변경은 partial 이 잡는다.** 이걸 pin 의 성과로 귀속하면 실패 원인 분석이 틀어진다.
`pin` 의 존재 이유는 위 표에서 partial 이 "통과" 인 행들이다.

---

## 3. pin assertion 어휘

pin 은 payload 를 얼리는 모드가 아니라 **경로마다 assertion 하나를 명시**하는 모드다.

| assertion | 표기 | 언제 |
|---|---|---|
| exists | `$.meta exists` | 존재만 계약할 때 |
| type | `$.createdAt : string(date-time)` | 타입 + format |
| nullable | `$.cancelledAt : [string, null]` | null 허용 명시 |
| const (값 고정) | `$.token_type = "Bearer"` | **안정 필드에만** |
| enum (집합 소속) | `$.data[].status ∈ {active, shipped, cancelled}` | 승격 조건 충족 시 |
| pattern | `$.orderId ^ord_` | 식별자 |
| range | `$.price > 0` · `$.limit <= 100` | 변동 수치의 하한/상한 |
| 불변식 | `$.meta.total >= len($.data)` | 경로 간 관계 |
| 개수 불변식 | `count($.data[?(@.isDefault)]) == 1` | 컬렉션 유일성 |
| header predicate | `Content-Type ^application/json` | exact 가 안 보는 헤더를 개별 계약 |

### 필드 성격 → assertion 선택

| 필드 성격 | 적합한 assertion | 예 |
|---|---|---|
| 안정값 (discriminator·통화·API 버전) | 값 고정 | `$.token_type = "Bearer"` |
| 열거형 | 집합 소속 | `$.data[].status ∈ {...}` |
| 변동 수치 (`total`·`count`·금액) | 범위·불변식 | `$.meta.total >= len($.data)` |
| 식별자 (`id`·`orderId`) | 패턴 | `$.orderId ^ord_` |
| 시각 (`createdAt`) | 타입 + format | `$.createdAt : string(date-time)` |
| cursor / opaque token | 존재 + 타입만 | `$.meta.nextCursor : [string, null]` |
| 헤더 | predicate | `Cache-Control = "no-store"` |

`total`·`cursor`·`id`·`timestamp` 에 값 고정을 걸면 매번 실패한다. 이것이 pin 을 value freeze 로 구현하면 안 되는 이유다.

### Hurl 표현 가능 여부

| assertion | `.hurl` 로 표현 | 표현 불가 시 처리 |
|---|---|---|
| exists · type · const · pattern · range · header | 가능 (`jsonpath`/`header` + predicate) | — |
| 집합 소속 | 가능하나 값마다 분해 필요 | 항목 수가 많으면 후처리로 |
| 경로 간 불변식 (`>= len($.data)`) | **불가** | `contracts/*.yaml` 에만 기록, `/api-verify` 후처리에서 검사 |
| 개수 불변식 | 부분적 (`count`) | 복합 조건은 후처리 |

Hurl assert 는 경로 하나에 predicate 하나다. 표현 불가한 항목을 상수로 근사(`>= 3`)하지 마라 — 데이터가 늘면 오탐이 된다.

---

## 4. 승격 자격

### partial → pin

아래 중 하나라도 해당하면 pin 후보다. 자동 승격은 하지 않고 사용자에게 제시한다.

| 후보 조건 | 예 |
|---|---|
| 값이 downstream 분기를 좌우한다 | `token_type`, `status`, `type` discriminator |
| 값이 센티널로 망가질 수 있다 | `total`, `count`, 잔액·금액 |
| 형식이 계약인 식별자 | `ord_` prefix, ULID/UUID 패턴 |
| 계약에 필요한 헤더 | `Content-Type`, `Cache-Control` |
| 변동성 점수가 낮은데 partial 만으로는 무의미한 필드 | 항상 같은 값인 boolean 플래그 |

### enum 승격 (자동)

네 조건을 **모두** 만족할 때만.

| 조건 | 값 |
|---|---|
| 독립 샘플 | `>= 3` |
| distinct value | `>= 2` |
| 최근 관측 | 최근 `20` 관측에서 신규 값 없음 |
| domain 크기 | `<= 12` |

미달이면 `enumCandidate` 로 기록하고 **경고만** 낸다. 1 샘플은 확정 금지(2026-09-04 확정).
사용자가 스펙 근거로 직접 확정하는 수동 경로는 항상 열려 있다.

### const 승격

사용자 pin 또는 공식 API spec 근거가 있을 때만. **단일 샘플 값만으로는 금지.**

### required 승격

| 판정 | 조건 |
|---|---|
| `required` | scoped sample 내 presence `100%` |
| `optional` | presence `< 100%`. `null` presence 는 missing 으로 세지 않는다 |
| `미확정` | 샘플 예산 미달 (< 3 captures) 또는 대표 페이지 미수집 |

`required` 는 property name 의 존재 조건이지 non-null 조건이 아니다. non-null 을 원하면 type 에서 `null` 을 제외해야 한다.

### pin → exact

| 대상 | 자격 조건 |
|---|---|
| 단일 객체 응답 | 동일 request fingerprint 로 `>= 3` 회 반복 후 normalized JCS digest variance `0` |
| 컬렉션 응답 | 위 + 안정 정렬/cursor 존재, duplicate stable id `0`, ordering variance `0`, item schema variance `0` |
| 오류 응답 | 4xx deterministic 만. **5xx 본문 exact 는 0개** |

자격 미달인 응답에 exact 를 걸면 매 실행이 실패하고, 그 실패는 곧 무시된다.

---

## 5. exact 의 범위 — 본문만

```text
diff 대상   응답 본문 (마스크 적용 → JCS 정규화 후)
제외        모든 응답 헤더
보완        필요한 헤더는 pin 으로 개별 지정
```

`Date` 는 응답마다 생성되고 `X-Request-Id` 류도 매 호출 달라진다. 헤더를 전체 diff 에 넣으면 항상 실패한다.
2026-09-04 확정 사항이며, 헤더 정규화 규칙은 JCS 밖에서 별도로 관리한다(field name 대소문자 무시, `Set-Cookie` 는 comma-join 금지).

---

## 6. additionalProperties 정책

| 모드 | 정책 |
|---|---|
| partial | 열림 — 서버의 필드 추가는 정상이다 |
| pin | 명시한 path 만 검사, 나머지 열림 |
| exact | 닫힘 — 전체 diff 가 곧 strict |

모드와 무관하게 닫으면 서버의 정상적인 필드 추가가 전부 회귀로 보고된다.
composition(`allOf`/`anyOf`)이 있는 스키마에서는 `additionalProperties` 보다 `unevaluatedProperties` 가 정확하다.

---

## 7. 컬렉션 계약은 세 조각

| 조각 | 계약 대상 | 기본 모드 |
|---|---|---|
| envelope schema | `data`/`items` 컨테이너, `meta` 형태 | partial |
| item schema | item 필드의 타입·required·enum | partial (+ 선별 pin) |
| pagination marker | 종료 신호, cursor 존재·타입 | pin |

- cursor·`$skiptoken`·`nextLink` 는 opaque. 파싱·수정·합성하지 않는다.
- 종료 신호는 `nextLink` **부재** 와 `null` 을 구분해 기록한다. 하나로 일반화하지 마라.
- 페이지 길이·전체 순서는 API 가 snapshot 또는 안정 정렬을 보장할 때만 exact 로 승격한다.
- item optionality 는 첫 페이지가 아니라 수집한 **모든 페이지의 item 집합**으로 계산한다.
- skip/duplicate 는 item schema 위반이 아니라 컬렉션 variance 신호다.

---

## 8. 오류 응답 계약

| 응답 | 계약 강도 |
|---|---|
| 4xx deterministic (malformed·인증 실패·권한 부족·validation·rate limit) | status exact pin 후보 |
| 4xx 불안정 (배포마다 코드가 흔들림) | status **class** 로 먼저 계약, 안정성 관측 후 exact 로 좁힌다 |
| 5xx | status class + envelope 형태 + retry metadata 만. 본문 exact `0개` |

- problem+json 이면 `type` URI 가 1차 식별자다. `title`·`detail` 이 아니다.
- `type` 누락은 `about:blank` 로 간주되며 위반이 아니다. 다만 식별자가 없으므로 status class 계약으로 내린다.
- `detail` 문자열을 exact match 로 고정하지 않는다.
- validation 오류는 `errors[]` 의 필드 경로와 오류 키만 계약하고 메시지 문자열은 제외한다.
- `Retry-After` 는 delay-seconds(0 이상 정수)와 HTTP-date 두 형식을 모두 파싱한다.
- 401 / 403 / `invalid_token` / `insufficient_scope` 를 하나로 합치지 않는다.
- 오류 본문 스냅샷 비교는 최대 `8KB` 샘플까지.

---

## 9. 안티패턴

| 안티패턴 | 문제 |
|---|---|
| 단일 샘플 scalar 를 바로 `const` 또는 닫힌 `enum` 으로 승격 | 두 번째 정상 값이 회귀로 보고된다. 오탐 한 번이면 사용자는 도구를 끈다 |
| pin 을 payload 전체 value freeze 로 구현 | `total`·`cursor`·`timestamp` 때문에 매번 실패한다 |
| 타입 회귀를 잡고 "pin 덕분" 이라고 보고 | 원인 귀속이 틀려 다음 판단(모드 승격)이 전부 어긋난다 |
| exact diff 에 헤더 포함 | `Date`·`X-Request-Id` 로 항상 실패한다 |
| partial 에서 `additionalProperties: false` 기본값 사용 | 서버의 정상적 필드 추가가 전부 실패로 잡힌다 |
| `null` 을 missing 과 합쳐 optionality 계산 | nullable 필드가 optional 로 오분류되어 필드 소실 회귀를 놓친다 |
| 빈 배열이나 첫 item 하나로 `items` 확정 | 이후 등장하는 다른 type 원소가 전부 위반이 된다 |
| 정렬 보장 없는 컬렉션에 index 기반 pin | `$.data[0].id` 가 정상 동작에도 실패한다 |
| 5xx stack trace 를 golden 으로 저장 | 내부 구조가 저장소에 남고 배포마다 달라져 항상 실패한다 |

---

## 10. 출처

- [contract-extraction-modes.md](../../../../docs/api/contract/contract-extraction-modes.md) — 모드 정의, 수치 기준, 안티패턴
- [multi-sample-pagination-variance.md](../../../../docs/api/contract/multi-sample-pagination-variance.md) — 샘플 예산, 컬렉션 3분할
- [error-status-contracts.md](../../../../docs/api/contract/error-status-contracts.md) — 오류·상태 코드 계약
- [snapshot-sealing-canonicalization.md](../../../../docs/api/contract/snapshot-sealing-canonicalization.md) — JCS·헤더 정규화 경계
- [probe-synthesis-hurl-semantics.md](../../../../docs/api/execution/probe-synthesis-hurl-semantics.md) — Hurl assert 표현 범위
- [api-kit 설계문서 §9.2](../../../../docs/superpowers/specs/2026-09-02-api-kit-design.md) — pin 의미 재정의, 확정 결정
