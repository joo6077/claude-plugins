---
title: API 수명주기
version: 0.1.0
last_updated: 2026-04-04
---

# API 수명주기

API 버전 전략, deprecation/sunset 신호, rate limiting과 throttling, 멱등성 키, gateway 역할, changelog 관리를 다룬다.

---

## 원칙

### 1. 호환적 진화를 기본으로 하고 breaking change에만 버전을 올린다

필드 추가, 선택적 파라미터 추가 등 하위 호환 변경은 기존 버전에서 수행한다. 기존 클라이언트가 깨지는 변경(필드 삭제, 타입 변경, 필수 파라미터 추가)만 새 버전을 만든다. 불필요한 버전 분기는 유지보수 비용을 기하급수적으로 늘린다.

> **출처:** [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)

### 2. 버전 식별은 한 방식만 일관 적용한다

path(`/v1/`), header(`Accept-Version`), query(`?version=1`) 중 하나를 선택한다. path가 가장 명시적이고 캐싱 친화적이다. 하이브리드는 라우팅 혼란과 문서 중복을 유발한다.

> **출처:** [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/), [Azure API Management — Versions](https://learn.microsoft.com/en-us/azure/api-management/api-management-versions)

### 3. Deprecation 헤더로 수명주기 신호를 전달한다

`Deprecation: @1735689600` 헤더로 해당 API가 더 이상 권장되지 않음을 알린다. `Link: <https://docs.example.com/migration>; rel="deprecation"` 헤더로 마이그레이션 문서를 연결한다. Deprecation은 동작 변경이 아니라 신호일 뿐이다.

> **출처:** [RFC 9745 — The Deprecation HTTP Header Field](https://datatracker.ietf.org/doc/html/rfc9745)

### 4. Sunset 헤더로 일몰 시점을 명시한다

`Sunset: Sat, 01 Feb 2026 00:00:00 GMT` 형태로 API가 완전히 제거되는 시점을 알린다. Sunset 날짜는 반드시 Deprecation 날짜 이후여야 한다. 클라이언트에게 마이그레이션 시간을 확보해 준다.

> **출처:** [RFC 9745 — The Deprecation HTTP Header Field](https://datatracker.ietf.org/doc/html/rfc9745), [RFC 8594 — The Sunset HTTP Header Field](https://www.rfc-editor.org/info/rfc8594)

### 5. Rate limiting과 throttling을 분리 설계한다

Rate limiting은 시간 단위 허용량 정책(예: 1000 req/hour)이고, throttling은 실시간 속도 억제(예: 100 req/sec burst 제한)이다. 429 Too Many Requests는 rate limit 초과 전용, 503 Service Unavailable + Retry-After는 throttling/과부하 상황에 사용한다.

> **출처:** [RFC 6585 — Additional HTTP Status Codes](https://datatracker.ietf.org/doc/html/rfc6585), [AWS API Gateway — Request Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)

### 6. Rate limiting 알고리즘은 요구사항에 맞게 선택한다

- **Fixed window**: 단순 구현, 윈도우 경계에서 폭주(burst) 발생 가능.
- **Sliding window**: 공정한 분배, 상태 저장 비용이 높다.
- **Token bucket**: burst를 허용하면서 평균 속도를 제한. 공개 API에서 가장 실용적.

rate(초당 보충 속도)와 burst(버킷 크기)를 별도로 설정한다.

> **출처:** [AWS API Gateway — Request Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)

### 7. 429 응답에 재시도 힌트를 포함한다

`Retry-After` 헤더는 필수. `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` 헤더로 클라이언트가 사전에 속도를 조절할 수 있게 한다. 힌트 없는 429는 클라이언트에게 맹목적 재시도를 강요한다.

> **출처:** [RFC 6585 — Additional HTTP Status Codes](https://datatracker.ietf.org/doc/html/rfc6585)

### 8. Idempotency key로 재시도 안전성을 보장한다

POST 같은 비멱등 요청에 `Idempotency-Key` 헤더를 첨부한다. 같은 키로 재요청 시 서버는 파라미터 동일성을 검사하고, 이전 결과를 그대로 재생한다. 네트워크 장애로 인한 중복 생성을 방지하는 Stripe 패턴.

> **출처:** [Stripe API — Idempotent Requests](https://docs.stripe.com/api/idempotent_requests)

### 9. API gateway는 횡단 관심사까지만 담당한다

인증, rate limiting, 라우팅, observability(로깅, 트레이싱)는 gateway에서 처리한다. 비즈니스 로직 판단(주문 승인, 결제 검증 등)은 반드시 서비스 레이어에 둔다. gateway에 도메인 로직이 들어가면 서비스 간 결합도가 올라가고 테스트가 어려워진다.

> **출처:** [AWS API Gateway — Request Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)

### 10. Changelog는 소비자 영향 중심으로 작성한다

변경 이력은 내부 구현이 아니라 API 소비자에게 미치는 영향 기준으로 기술한다. 각 항목에 deprecation notice, migration guide 링크, sunset date를 연결한다. changelog 없이 문서를 덮어쓰면 소비자가 변경을 인지할 수 없다.

> **출처:** [RFC 9745 — The Deprecation HTTP Header Field](https://datatracker.ietf.org/doc/html/rfc9745)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| Retry-After 형식 | HTTP-date 또는 non-negative seconds (정수) |
| 429 용도 | rate limiting 전용 (throttling은 503 + Retry-After) |
| Stripe idempotency key 최대 길이 | 255자 |
| Stripe idempotency key 권장 형식 | UUID v4 |
| Stripe idempotency key 최소 보존 기간 | 24시간 |
| Token bucket 설정 | rate(보충 속도)와 burst(버킷 크기) 별도 설정 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| /v1에 breaking change를 계속 넣기 | 기존 클라이언트가 예고 없이 깨진다. 버전의 의미가 없어진다. |
| 429에 Retry-After 없음 | 클라이언트가 재시도 시점을 알 수 없어 맹목적 폴링 또는 포기한다. |
| Idempotency key를 주문 ID와 혼용 | 같은 주문의 다른 요청(수정, 취소)이 첫 요청 결과를 재생한다. |
| Gateway에서 도메인 권한 판단 | 서비스 간 결합도 증가, 테스트 불가, 정책 변경 시 gateway 재배포 필요. |
| Changelog 없이 문서 덮어쓰기 | 소비자가 변경을 인지 못하고 통합이 깨진다. |

---

## Gotchas

- **Deprecation은 힌트일 뿐 동작 변경이 아니다.** Deprecation 헤더가 붙어도 API는 정상 동작한다. 클라이언트가 헤더를 무시하면 sunset까지 아무 일도 일어나지 않는다. 모니터링과 알림을 별도로 구축해야 한다.
- **Sunset과 Deprecation 날짜 형식이 다르다.** Deprecation은 `@`-prefixed Unix timestamp(structured field), Sunset은 HTTP-date(RFC 7231). 형식을 혼동하면 파싱 실패한다.
- **Stripe idempotency는 validation 실패를 저장하지 않는다.** 파라미터 검증 실패(400)는 idempotency store에 기록되지 않으므로, 수정된 파라미터로 같은 키를 재사용할 수 있다. 서버 처리 성공/실패만 저장된다.
