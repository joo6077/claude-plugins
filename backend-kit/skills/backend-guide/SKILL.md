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
10. **OAuth 2.1 은 아직 Draft** — 2026-04 기준 OAuth 2.1 은 `draft-ietf-oauth-v2-1-15` (Active Internet-Draft, expires 2026-09). 최종 RFC 가 아니므로 "OAuth 2.1 표준"이라고 단정하지 마라. 실무 기준선은 RFC 9700(BCP) + FAPI 2.0 Final 을 사용한다. 출처: [IETF OAuth 2.1 Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
11. **마이크로서비스 무조건 권장 금지** — 팀 규모 10명 미만이면 Modular Monolith First 를 기본으로 제안하라. 마이크로서비스는 인프라 비용 3.75-6x, 디버깅 시간 35% 증가. Amazon Prime Video 가 마이크로서비스→모놀리스 전환으로 인프라 비용 90% 절감한 사례를 참고. 출처: [ByteIota 2026](https://byteiota.com/modular-monolith-42-ditch-microservices-in-2026/)
12. **Enumerate-before-Act (skill-design-guide §5.5 대응)** — 가이드 제공 전에 해당 코드/설명에서 **관련 원칙 위반 후보를 전부 나열** 한 뒤 한 번에 제시하라. "하나 고치면 다음에 또 지적"의 round-trip 을 차단한다 (/insights 마찰점 #1). 예: auth 코드를 보면 Implicit grant / PKCE 미사용 / JWT localStorage 저장 / CORS wildcard 를 한 번에 모두 나열하고 사용자 승인을 기다린다.
13. **3-Step Process (Phase 5 flutter-error/flutter-hooks parity)** — 가이드형 스킬은 반드시 탐색(코드/설명 맥락 파악) → 진단(원칙 위반 rule-by-rule 열거) → 처방(우선순위 + 트레이드오프 + 출처) 3단계를 **순서 고정**으로 따른다. 맥락 없이 바로 처방을 내지 말 것.

# Process (3-Step · 탐색 → 진단 → 처방)

## Step 1: 탐색 — 맥락 파악

사용자가 제공한 코드/설명에서 관련 백엔드 카테고리를 식별한다:

| 카테고리 | 키워드 |
|----------|--------|
| architecture | hexagonal, ports, adapter, clean, DDD, 도메인, bounded context, layered |
| api-design | REST, 엔드포인트, URL, 상태코드, 페이지네이션, OpenAPI 3.1 |
| database | 스키마, 인덱스, 쿼리, N+1, migration, 풀링 |
| auth | 인증, 인가, JWT, OAuth, OAuth 2.1, PKCE, DPoP, RBAC, 세션, CORS, FAPI 2.0, Passkeys, WebAuthn, FIDO2 |
| error-handling | 에러, retry, circuit breaker, 예외, fallback, problem+json, RFC 9457, rate limiter |
| testing | 테스트, mock, fixture, 커버리지, contract test, Pact, PactFlow, Testcontainers |
| security | 보안, injection, XSS, SSRF, OWASP, 헤더 |
| caching | 캐시, Redis, TTL, stampede, 무효화 |
| event-driven | 메시지 큐, Kafka, outbox, CQRS, saga, DLQ, idempotency, AsyncAPI, CDC, Debezium, RabbitMQ |
| api-lifecycle | 버저닝, deprecation, rate limiting, idempotency key, Sunset header |
| graphql | GraphQL, 스키마, resolver, DataLoader, federation, Apollo Federation |
| grpc | gRPC, proto, streaming, deadline, metadata |
| realtime | WebSocket, SSE, 실시간, 구독, heartbeat |
| observability | OTel, OpenTelemetry, 로깅, tracing, metrics, 구조화 로그, W3C Trace Context |
| architecture-decision | 마이크로서비스, 모듈러 모놀리스, 아키텍처 선택, 팀 규모 |
| validation | 검증, Pydantic, Zod, JSON Schema, 입력 검증 |
| serverless | Lambda, cold start, SnapStart, edge, Cloudflare Workers, Hono |
| workflow | Temporal, Dapr, saga, 워크플로우, orchestration |
| type-safe-api | tRPC, Effect-TS, Hono RPC, 타입 안전 |
| edge-db | D1, Durable Objects, Neon, Turso, TiDB, 서버리스 DB |

## Step 2: 진단 — 원칙 위반 Rule-by-Rule 열거

references/principle-index.md 에서 해당 카테고리의 원칙 문서 경로를 찾아 읽고, 사용자 코드/설명에 적용되는 원칙 위반 후보를 **개별 row 단위로 모두 열거** 한다 (Gotcha 12 Enumerate-before-Act). 카테고리 단위 묶음 평가 금지.

## Step 3: 처방 — 가이드 제시 (우선순위 · 트레이드오프 · 출처)

각 피드백 항목은 반드시 이 포맷을 따른다:

### [카테고리] 항목 제목

**원칙:** [원칙 이름]
**근거:** [구체적 설명 + 수치 기준]
**권장:** [개선 방향]

> **출처:** [출처명](URL)

# References

- references/principle-index.md — 카테고리별 원칙 문서 매핑
