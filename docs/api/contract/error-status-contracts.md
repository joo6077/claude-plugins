---
title: 오류·상태 코드 계약
version: 0.1.0
last_updated: 2026-09-04
---

# 오류·상태 코드 계약

실제 오류 응답을 SSOT로 삼아 계약을 만들 때, 무엇을 고정하고 무엇을 class 수준으로만 둘지 판정하는 규칙.

---

## 원칙

### 1. 오류 계약은 machine-readable 필드로만

status, content-type, 그리고 기계 판독 가능한 식별 필드로 계약을 잡는다. `detail` 같은 사람용 설명 문자열을 파싱해 판정하지 않는다.
설명 문구는 서버 배포마다 바뀌고 다국어에 따라 달라져 계약이 쉽게 깨진다.

> **출처:** [RFC 9457 §3.1.4 detail](https://www.rfc-editor.org/rfc/rfc9457.html#section-3.1.4)

### 2. problem+json 호환 해석

응답 content-type이 `application/problem+json`이면 `type`, `title`, `status`, `detail`, `instance`를 RFC 9457 의미대로 해석한다.
`type`이 없으면 `about:blank`로 간주되므로, 누락 자체를 계약 위반으로 잡지 않는다.

> **출처:** [RFC 9457 §3.1 Members of a Problem Details Object](https://www.rfc-editor.org/rfc/rfc9457.html#section-3.1)

### 3. problem type이 1차 식별자

problem detail의 primary identifier는 `type` URI다. 오류 종류를 구분하는 키는 `title`이나 `detail`이 아니라 `type`이다.
absolute URI가 권장되며, 도구는 디버그 목적이 아닌 한 이 URI를 자동으로 dereference하지 않는다.

> **출처:** [RFC 9457 §3.1.1 type](https://www.rfc-editor.org/rfc/rfc9457.html#section-3.1.1)

### 4. 불안정하면 status class로 계약

exact status가 배포마다 흔들리는 API는 먼저 4xx/5xx class 정책으로 계약화하고, 안정성이 관측된 뒤에 exact로 좁힌다.
RFC 9110은 status code의 첫 자리로 class 의미를 정의하며 4xx를 client error class로 규정한다.

> **출처:** [RFC 9110 §15 Status Codes](https://datatracker.ietf.org/doc/html/rfc9110#section-15)

### 5. 인증 오류 분리

`401`은 유효한 인증 정보가 없거나 실패한 경우이며 `WWW-Authenticate` challenge를 동반한다. `403`은 서버가 요청을 이해했으나 거부한 경우다.
OAuth bearer 오류도 같은 축으로 `invalid_token`과 `insufficient_scope`를 분리해 계약한다.

> **출처:** [RFC 9110 §15.5.2 401 Unauthorized](https://datatracker.ietf.org/doc/html/rfc9110#section-15.5.2) · [RFC 6750 §3.1 Error Codes](https://datatracker.ietf.org/doc/html/rfc6750#section-3.1)

### 6. validation 오류는 안정 필드만

validation 오류는 stable extension field만 계약 대상으로 삼는다. 메시지 문자열은 제외한다.
RFC 9457 예시는 `errors[]` 배열과 JSON Pointer를 problem extension으로 두므로, 필드 경로와 오류 키만 고정한다.

> **출처:** [RFC 9457 §3 Problem Details JSON Object](https://www.rfc-editor.org/rfc/rfc9457.html#section-3)

### 7. Retry-After 처리

`Retry-After`는 delay-seconds(0 이상 정수) 또는 HTTP-date 두 형식을 가진다. 파서는 둘 다 받아야 한다.
`429`, `503`, 일부 redirect 응답에서 재시도 가능성을 설명하는 계약 후보로 다룬다.

> **출처:** [RFC 9110 §10.2.3 Retry-After](https://datatracker.ietf.org/doc/html/rfc9110#section-10.2.3) · [RFC 6585 §4 429 Too Many Requests](https://datatracker.ietf.org/doc/html/rfc6585#section-4)

### 8. 4xx는 exact pin 후보

같은 입력에 같은 코드가 돌아오는 deterministic client error는 exact status pin 후보다.
malformed request, 인증 실패, 권한 부족, validation 실패, rate limit이 대표 사례다.

> **출처:** [RFC 9110 §15.5 Client Error 4xx](https://datatracker.ietf.org/doc/html/rfc9110#section-15.5)

### 9. 5xx는 계약 제외 버킷

5xx 응답 본문은 기본적으로 exact 계약에서 제외하고 status class + envelope 형태 + retry metadata만 검증한다.
RFC 9457도 problem detail이 구현 디버깅 도구가 아니며 내부 정보 노출 위험이 있다고 경고한다 — 그런 본문을 golden으로 고정하면 안 된다.

> **출처:** [RFC 9457 §4 Extension Members](https://www.rfc-editor.org/rfc/rfc9457.html#section-4) · [RFC 9457 §5 Security Considerations](https://www.rfc-editor.org/rfc/rfc9457.html#section-5)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| problem `status` 유효 범위 | 100..599 정수 | RFC 9457 Appendix A |
| problem extension member name | 3자 이상, letter로 시작, letter/digit/`_` 구성 권장 | RFC 9457 §4 |
| `Retry-After` delay-seconds | 0 이상 정수 (또는 HTTP-date) | RFC 9110 §10.2.3 |
| `429` 예시 | `Retry-After: 3600` — 예시일 뿐 표준 임계값 아님 | RFC 6585 §4 |
| 5xx 본문 exact pin | 0개 | 추론 — 내부 정보 노출·비결정성 |
| 오류 본문 스냅샷 비교 | 최대 8KB 샘플 | 추론 — 대용량 stack trace 저장 방지 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| `detail` 문자열 전체를 exact match로 고정 | 문구·다국어 변경만으로 계약이 깨진다. 실제 회귀와 구분되지 않는다 |
| body의 `status` 필드와 실제 HTTP status가 다를 때 body만 신뢰 | HTTP status가 실제 전송 계층 결과다. body 값은 advisory다 |
| 401 / 403 / `invalid_token` / `insufficient_scope`를 하나로 합침 | 토큰 갱신으로 풀리는 실패와 권한 자체가 없는 실패가 섞인다 |
| 500 응답의 stack trace를 golden contract로 저장 | 내부 구조가 저장소에 남고, 배포마다 달라져 항상 실패한다 |
| `429`를 단순 실패로만 처리하고 `Retry-After` 무시 | 재시도 가능 신호를 버려 불필요한 재실행·추가 차단을 부른다 |

---

## Gotchas

- **RFC 9457의 `status` member는 advisory다** — 그래도 generator는 실제 HTTP status와 일치시켜야 한다. 불일치는 서버 버그 신호로 보고 HTTP status를 기준으로 판정하라.
- **unknown extension은 무시 가능해야 한다** — 응답에 모르는 필드가 늘어난 것을 breaking change로 판정하면 오탐이 쏟아진다.
- **`about:blank`은 "type 없음"의 기본값이다** — `type` 누락 자체는 실패가 아니다. 단, 이 경우 오류 식별자가 없으므로 status class로 계약을 내려야 한다.
- **`Retry-After`는 HTTP-date도 온다** — 정수 파싱만 구현하면 date 형식에서 조용히 무시된다. 두 형식 모두 처리하라.
