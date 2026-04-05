---
title: API 설계
version: 0.1.0
last_updated: 2026-04-04
---

# API 설계

REST 리소스 설계, HTTP 메서드 의미론, 상태 코드, 페이지네이션, 에러 응답 표준화, OpenAPI 스펙 관리를 다룬다.

---

## 원칙

### 1. URI는 리소스 명사 중심, 행위는 HTTP 메서드로 표현한다

`/users`(리소스)에 GET/POST/PUT/DELETE를 적용한다. `/getUsers`, `/createUser` 같은 동사 URI는 쓰지 않는다. 컬렉션은 복수형(`/users`), 개별 리소스는 식별자(`/users/{id}`). 중첩은 2단계까지 허용하고(`/users/{id}/orders`), 그 이상은 독립 리소스로 승격한다.

> **출처:** [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)

### 2. HTTP 메서드와 상태 코드는 RFC 의미론을 준수한다

- **GET**: 안전(safe), 멱등(idempotent). 서버 상태를 변경하지 않는다.
- **POST**: 리소스 생성. 201 Created + Location 헤더 반환.
- **PUT**: 전체 교체(full replacement). 멱등.
- **PATCH**: 부분 수정(partial update). 멱등성은 구현에 따라 다르다.
- **DELETE**: 리소스 삭제. 멱등.

상태 코드 범위: 1xx(정보), 2xx(성공), 3xx(리다이렉션), 4xx(클라이언트 에러), 5xx(서버 에러). 100~599 범위에서 RFC 9110이 정의한 코드만 사용한다. 자체 정의 상태 코드는 금지.

> **출처:** [RFC 9110 — HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)

### 3. 에러 응답은 application/problem+json(RFC 9457)으로 표준화한다

모든 4xx/5xx 응답은 다음 5개 필드를 포함한다:

| 필드 | 설명 |
|------|------|
| `type` | 에러 유형 URI (문서 링크) |
| `title` | 사람이 읽을 수 있는 짧은 설명 |
| `status` | HTTP 상태 코드 (정수) |
| `detail` | 이 요청에 대한 구체적 설명 |
| `instance` | 이 에러 발생의 고유 참조 URI |

```json
{
  "type": "https://api.example.com/errors/insufficient-balance",
  "title": "Insufficient Balance",
  "status": 422,
  "detail": "계좌 잔액이 50,000원 부족합니다.",
  "instance": "/transfers/abc-123"
}
```

> **출처:** [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)

### 4. 큰 컬렉션은 cursor 기반 페이지네이션을 우선한다

| 방식 | 장점 | 단점 |
|------|------|------|
| **Offset** | 임의 페이지 점프 가능 | 삽입/삭제 시 row 누락·중복, `OFFSET N`이 클수록 성능 저하 |
| **Cursor** | 일관된 결과, O(1) 탐색 | 임의 페이지 점프 불가 |

Cursor 응답 형태:

```json
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTAwfQ==",
  "has_more": true
}
```

Offset은 데이터 변경이 드문 정적 목록(관리자 대시보드 등)에서만 사용한다. 실시간 피드, 타임라인, 검색 결과는 반드시 cursor를 쓴다.

> **출처:** [Slack Engineering — Evolving API Pagination at Slack](https://slack.engineering/evolving-api-pagination-at-slack/)

### 5. OpenAPI 스펙은 코드와 항상 동기화한다

OpenAPI 3.1.1 스펙을 단일 소스로 유지한다. 코드에서 스펙을 생성하거나(code-first), 스펙에서 코드를 생성하는(spec-first) 방식 중 하나를 선택하되 혼용하지 않는다. CI에서 스펙과 실제 응답의 불일치를 검증하는 계약 테스트를 실행한다.

> **출처:** [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html)

### 6. API 버전은 URL 경로 또는 헤더 방식 중 하나를 선택한다

- **URL 경로**: `/v1/users` — 명시적, 캐싱 친화적.
- **헤더**: `Accept: application/vnd.api+json;version=1` — URL 깔끔.

하이브리드(경로 + 헤더 동시 사용)는 혼란을 유발하므로 지양한다. 메이저 버전만 URL에 반영하고, 하위 호환 변경은 버전을 올리지 않는다.

### 7. 필터와 정렬은 쿼리 파라미터로 표현한다

`/users?status=active&sort=-created_at&fields=id,name` 형태를 사용한다. 리소스 경로에 필터를 넣지 않는다(`/users/active` 금지 — 이것은 `active`라는 ID의 사용자처럼 보인다). 복합 필터가 필요하면 LHS brackets(`filter[status]=active`) 또는 RHS colon(`status:eq:active`) 컨벤션을 선택한다.

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| HTTP 상태 코드 범위 | 100~599 (RFC 9110) |
| RFC 9457 problem+json 필수 필드 | 5개 (type, title, status, detail, instance) |
| OpenAPI 최신 버전 | 3.1.1 |
| Cursor 페이지 크기 기본값 | 20~100 (리소스 크기에 따라) |
| API 응답 시간 목표 | p50 < 100ms, p99 < 500ms |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| GET 바디에 데이터 전송 | RFC 9110은 GET 바디의 의미를 정의하지 않음. 프록시/캐시가 무시할 수 있다. |
| 모든 응답 200 OK + 커스텀 에러 코드 | HTTP 인프라(로드밸런서, 모니터링)가 에러를 감지 못한다. |
| 버전 없는 API | Breaking change 시 모든 클라이언트가 동시에 깨진다. |
| 에러 포맷 비표준 | 클라이언트마다 파싱 로직이 달라지고, 에러 처리 자동화 불가. |

---

## Gotchas

- **PATCH는 부분 수정이지 upsert가 아니다.** 리소스가 없으면 404를 반환해야 한다. upsert가 필요하면 PUT을 사용하거나 별도 엔드포인트를 만든다.
- **204 No Content는 body가 없어야 한다.** 일부 프레임워크가 빈 JSON `{}`을 반환하면 클라이언트 파서가 실패할 수 있다. Content-Length: 0이 올바른 동작이다.
- **Cursor 토큰이 영구 유효하다고 가정하면 안 된다.** 서버 재시작, 데이터 마이그레이션, TTL 만료로 cursor가 무효화될 수 있다. 클라이언트는 400 응답 시 처음부터 다시 시작하는 로직을 갖춰야 한다.
