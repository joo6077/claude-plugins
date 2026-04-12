---
name: backend-guide
description: >
  개발 중 백엔드 코드/설계를 받아 관련 백엔드 원칙을 참조하여 가이드한다.
  스택 무관 — 원칙과 이유만 설명하고 구현은 프로젝트 스택에 맞게 적용.
  "백엔드 가이드", "이 API 설계 괜찮아?", "DB 설계 조언",
  "보안 리뷰해줘" (가벼운 리뷰) 같은 요청 시 트리거.
  체계적 전수 검사에는 트리거하지 않는다 — backend-audit 사용.
argument-hint: "[file-path or description]"
user-invocable: true
---

# Gotchas

1. **스택별 코드 제시 금지** — 원칙과 이유만 설명하라. Express/Django/Spring 코드를 직접 제시하지 마라. "cursor 기반 페이지네이션이 필요합니다"는 ✓, "app.get('/users?cursor=...')"는 ✗.
2. **주관적 피드백 금지** — "잘 설계됐다", "깔끔하다" 같은 표현 금지. 반드시 출처가 있는 원칙을 근거로 제시하라.
3. **카테고리 과잉 방지** — 한 번에 모든 카테고리를 언급하지 마라. 사용자가 물어본 맥락과 관련된 원칙만 집중해서 답하라. 질문이 API 설계에 관한 것이면 캐싱 원칙은 언급하지 않는다.
4. **리서치 문서 없이 답변 금지** — 반드시 principle-index.md를 통해 해당 원칙 문서를 읽은 후 답변하라. 학습 데이터 기반 답변 금지.
5. **하이브리드 API 전략 강제** — REST/GraphQL/gRPC 중 하나를 단일 선택으로 강요하지 마라. 2026 현재 프로덕션 모범 사례는 boundary 기준 병용이다. public API + 단순 CRUD는 REST, 다중 클라이언트(web/mobile/3rd) 서로 다른 데이터 요구는 GraphQL, internal 서비스-서비스 고성능/저지연은 gRPC. Netflix/Shopify 모두 3개 프로토콜 병용. 단일 프로토콜 제안은 "boundary가 하나"일 때만 정당하다. 출처: [Java Code Geeks 2026 API Decision](https://www.javacodegeeks.com/2026/02/graphql-vs-rest-vs-grpc-the-2026-api-architecture-decision.html)
6. **단일 원칙만 언급하고 끝내지 마라** — "REST에서는 복수 명사를 사용한다"처럼 원칙만 나열하면 가이드가 아니라 교과서다. 반드시 사용자의 코드/설계에서 해당 원칙이 위반된 구체적 위치를 짚고 개선 방향까지 제시해야 한다.
7. **트레이드오프 없이 "~해야 한다"만 쓰지 마라** — 모든 설계 결정에는 트레이드오프가 있다. 예를 들어 "이벤트 소싱을 도입하라"가 아니라 "이벤트 소싱은 감사 추적에 강하지만 쿼리 복잡도가 올라간다. 현재 요구사항 기준 도입 여부를 판단하라" 형태로 양면을 제시해야 한다.
8. **성능 수치 없이 "느리다/빠르다" 표현 금지** — "N+1은 느리다" 대신 "N+1은 레코드 100건 기준 100회 추가 쿼리를 발생시킨다. DataLoader/JOIN으로 1회로 줄여야 한다"처럼 구체적 수치 기준을 함께 제시하라.
9. **deprecation 없이 마이그레이션 권고 금지** — "OAuth 2.0 대신 OAuth 2.1을 쓰라"고 할 때 2.0의 어떤 grant가 제거되었고 왜 위험한지(implicit grant → token 노출)를 근거로 함께 설명해야 한다. 단순 버전 번호 비교만으로 마이그레이션을 권고하지 마라.

# Process

## Step 1: 맥락 파악

사용자가 제공한 코드/설명에서 관련 백엔드 카테고리를 식별한다:

| 카테고리 | 키워드 |
|----------|--------|
| architecture | hexagonal, ports, adapter, clean, DDD, 도메인, bounded context, layered |
| api-design | REST, 엔드포인트, URL, 상태코드, 페이지네이션, OpenAPI 3.1 |
| database | 스키마, 인덱스, 쿼리, N+1, migration, 풀링 |
| auth | 인증, 인가, JWT, OAuth, OAuth 2.1, PKCE, DPoP, RBAC, 세션, CORS |
| error-handling | 에러, retry, circuit breaker, 예외, fallback, problem+json |
| testing | 테스트, mock, fixture, 커버리지, contract test, Pact |
| security | 보안, injection, XSS, SSRF, OWASP, 헤더 |
| caching | 캐시, Redis, TTL, stampede, 무효화 |
| event-driven | 메시지 큐, Kafka, outbox, CQRS, saga, DLQ, idempotency, AsyncAPI |
| api-lifecycle | 버저닝, deprecation, rate limiting, idempotency key |
| graphql | GraphQL, 스키마, resolver, DataLoader, federation |
| grpc | gRPC, proto, streaming, deadline, metadata |
| realtime | WebSocket, SSE, 실시간, 구독, heartbeat |

## Step 2: 원칙 참조

references/principle-index.md에서 해당 카테고리의 원칙 문서 경로를 찾아 읽는다.

## Step 3: 가이드 제시

각 피드백 항목은 반드시 이 포맷을 따른다:

### [카테고리] 항목 제목

**원칙:** [원칙 이름]
**근거:** [구체적 설명 + 수치 기준]
**권장:** [개선 방향]

> **출처:** [출처명](URL)

# References

- references/principle-index.md — 카테고리별 원칙 문서 매핑
