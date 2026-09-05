---
title: 스냅샷 봉인과 정규화
version: 0.1.0
last_updated: 2026-09-04
---

# 스냅샷 봉인과 정규화

응답을 baseline 으로 봉인할 때 무엇을 원본 증거로 남기고 무엇을 비교 기준선으로 파생시킬지 가르는 규칙.
비교 기준선은 RFC 8785 JCS canonical JSON 이며, 사람이 읽는 화면 표시용 포매팅은 기준선이 아니다.

---

## 원칙

### 1. 원본 증거 보존 (Raw Evidence Preservation)

baseline 은 raw 를 보관한다. 상태코드, 원본 헤더 라인, wire/content 바이트, 디코딩 전후 digest 를 그대로 남긴다.
단 **시크릿 값만 마스킹한 raw** 다 — 토큰·키·쿠키 값은 자리를 유지한 채 값만 가린다(2026-09-04 결정).
계약 비교 입력은 이 raw 에서 파생된 별도 산출물이고, JCS 역시 원본 전송 데이터와 canonical counterpart 를 분리하는 사용 모델을 전제한다.

> **출처:** [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html), [RFC 9530 Digest Fields](https://www.rfc-editor.org/rfc/rfc9530/)

### 2. JCS 정규 형식 (JCS Canonical Form)

정규화된 계약 입력의 JSON 기준선은 RFC 8785 JCS 로 고정한다.
JCS 는 I-JSON 입력, 토큰 사이 공백 0개, ECMAScript primitive serialization, 객체 property 재귀 정렬, UTF-8 출력을 요구한다.
따라서 pretty print 결과는 어떤 경우에도 비교 기준이 될 수 없다.

> **출처:** [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html)

### 3. 정규화 전 I-JSON 게이트

JCS 로 넘기기 전에 I-JSON 으로 먼저 검문한다.
중복 키, Unicode 로 표현 불가한 문자열, IEEE 754 binary64 로 표현 불가한 숫자, NaN/Infinity, lone surrogate 는 정규화 대상이 아니라 **실패 또는 fallback 대상**이다.
게이트를 건너뛰면 파서가 조용히 값을 바꾼 뒤의 결과를 봉인하게 된다.

> **출처:** [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html), [RFC 7493 I-JSON](https://www.rfc-editor.org/rfc/rfc7493.html)

### 4. 헤더 정규화는 JCS 밖에서

HTTP 헤더는 JSON 이 아니므로 JCS 에 섞지 않고 별도 규칙을 둔다.
field name 은 대소문자 무시, 같은 이름의 field line 결합은 그 field 가 comma-list 를 허용할 때만 가능하며 `Set-Cookie` 는 예외로 특별 취급한다.

> **출처:** [RFC 9110 HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)

### 5. 미디어 타입 처리 경계

JSON 파싱 여부는 `Content-Type` 과 `Content-Encoding` 을 해석한 뒤의 representation 의미로 판단한다.
`application/json` 에는 charset parameter 가 정의되어 있지 않고, 네트워크로 오가는 JSON 은 UTF-8 이어야 한다.
따라서 charset 선언은 파싱 근거가 아니라 증거로만 남긴다.

> **출처:** [RFC 8259 JSON](https://www.rfc-editor.org/rfc/rfc8259.html), [RFC 9110 HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)

### 6. 변동 필드 레지스트리와 마스킹 경계

timestamp, id, nonce, token 류는 raw 를 건드리지 말고 **normalized 단계에서 path registry** 로 처리한다.
Jest propertyMatchers, insta redactions, ApprovalTests scrubbers 가 모두 같은 관례 — 비결정 값을 비교 직전에 안정화하고 원본은 그대로 둔다 — 를 제공한다.

> **출처:** [Jest Snapshot Testing](https://jestjs.io/docs/snapshot-testing), [insta redactions](https://insta.rs/docs/redactions/), [ApprovalTests Scrubbers](https://approvaltestscpp.readthedocs.io/en/latest/generated_docs/explanations/Scrubbers.html)

### 7. 매니페스트 해싱과 불변 baseline ID

baseline id 는 응답 바이트가 아니라 **매니페스트의 digest** 로 만든다.
매니페스트에는 raw digest, normalized JCS digest, redaction registry 버전, media type, extraction mode 를 담는다.
HTTP digest fields 가 content digest 와 representation digest 를 분리하고 algorithm agility 를 두는 것이 이 구조의 선례다.

> **출처:** [RFC 9530 Digest Fields](https://www.rfc-editor.org/rfc/rfc9530/), [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| 중복 JSON object member 허용치 | `0` | 중복 이름은 I-JSON/JCS 위반 ([RFC 7493](https://www.rfc-editor.org/rfc/rfc7493.html)) |
| 안전 정수 범위 | `-9007199254740991 ~ 9007199254740991` | 범위 밖 정수는 exact interchange 를 기대할 수 없음 ([RFC 7493](https://www.rfc-editor.org/rfc/rfc7493.html)) |
| JCS 토큰 사이 추가 공백 | `0 byte` | JCS 정의 ([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html)) |
| lone surrogate / noncharacter 허용 | `0` | 정상 surrogate pair 는 허용, 단독 surrogate 는 실패 ([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), [RFC 7493](https://www.rfc-editor.org/rfc/rfc7493.html)) |
| manifest digest 기본 알고리즘 | `sha-256` (옵션 `sha-512`) | 추론 — RFC 9530 의 algorithm agility 와 sha-256/sha-512 사용례 |
| baseline 내 시크릿 원문 | `0건` | 2026-09-04 결정 — raw 보존과 시크릿 0건을 동시에 만족하기 위해 값만 마스킹 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| pretty-print JSON, 키 삽입 순서, diff UI 문자열을 해싱해 기준선으로 사용 | 표시 포매터가 바뀌면 계약이 통째로 깨진다. 기준선은 JCS 결과여야 한다 |
| 파서가 "last key wins" 로 삼킨 뒤 중복 키를 검사 | 이미 값이 소실된 상태라 검사 자체가 무의미하다. 검문은 파싱 게이트에서 |
| 배열을 안정화한다며 정렬 | JCS 는 object property 만 정렬하고 array order 는 보존한다. 정렬은 실제 순서 회귀를 은폐한다 |
| `Set-Cookie` 를 comma-join 해서 헤더 정규화 입력에 투입 | `Set-Cookie` 는 comma-list 결합이 불가능한 예외 헤더다. 쿠키가 잘못 병합된다 |
| 마스킹 결과만 저장하고 raw digest·원본 접근 경계를 남기지 않음 | 회귀 조사 시 원본을 복원할 수 없어 baseline 이 증거로서 기능하지 못한다 |

---

## Gotchas

- **JCS property sort 는 UTF-16 code unit 순서다** — unescaped property name 기준이라 UTF-8 byte sort 와 비ASCII 구간에서 결과가 달라진다. 자체 구현 정렬을 쓰지 말고 JCS 구현을 쓴다.
- **Unicode normalization 은 하지 않는다** — NFC/NFD 가 화면상 같아 보여도 JCS digest 는 다르다. "같아 보이는데 왜 다르냐" 는 대부분 이 케이스다.
- **`Content-Encoding: gzip` 이면 digest 가 둘이다** — raw content bytes digest 와 decoded representation digest 가 다르므로 매니페스트에 둘을 구분해 기록한다.
- **charset parameter 는 파싱 근거가 아니다** — `application/json; charset=utf-8` 의 charset 은 compliant recipient 에게 의미가 없지만, 증거에는 원문 그대로 남긴다.
