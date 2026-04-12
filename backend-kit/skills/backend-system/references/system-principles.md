# Backend System Principles

프로젝트 백엔드 아키텍처 세팅 시 참조하는 원칙 문서 매핑.

## 아키텍처 패턴

| 패턴 | 핵심 원칙 | 도입 기준 |
|------|-----------|-----------|
| Hexagonal (Ports & Adapters) | 도메인은 어댑터를 직접 import 하지 않고 port 인터페이스만 의존. 외부 시스템 교체 시 어댑터만 재작성. | 소~중 규모 앱. "technological churn 보험". [Hexagonal vs Clean vs Onion 2026](https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f) |
| Clean Architecture | Hexagonal + 의존성 규칙(inward-only) + 엔티티/유스케이스/인터페이스 어댑터/프레임워크 4계층 분리. | 중~대 규모, 명확한 레이어 네이밍이 필요할 때. [AWS Prescriptive Hexagonal](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html) |
| DDD (Domain-Driven Design) | 도메인 모델-persistence 모델 분리. Ubiquitous Language. Aggregate / Value Object / Bounded Context. | bounded context 2+ 또는 풍부한 비즈니스 규칙이 있을 때. 단순 CRUD엔 과도. [Vaadin DDD+Hexagonal](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture) |

**과복잡도 경고**: 위 패턴을 단순 CRUD 앱에 강요하지 마라. 비즈니스 규칙이 없는 CRUD는 "간소화 계층형 (Controller → Service → Repository)"이면 충분하다.

**Modular Monolith First**: 팀 규모 10명 미만이면 모놀리스가 일관되게 우월하다. 마이크로서비스는 인프라 비용 3.75-6x, 디버깅 시간 35% 증가. Shopify 모델(모놀리스 유지 + checkout/fraud 등 특정 도메인만 추출)이 실무 레퍼런스. 출처: [ByteIota 2026](https://byteiota.com/modular-monolith-42-ditch-microservices-in-2026/), [ByteByte Go](https://blog.bytebytego.com/p/monolith-vs-microservices-vs-modular).

## 필수 카테고리

| 카테고리 | 참조 문서 | 핵심 원칙 |
|----------|-----------|-----------|
| API 규격 | ../../../../docs/backend/fundamentals/api-design.md | 리소스 명사, RFC 9110 메서드, RFC 9457 에러(`type` URI 필드 필수), OpenAPI 3.1 JSON Schema 호환, API Versioning(REST=URL path, GraphQL=@deprecated 진화) |
| 에러 처리 | ../../../../docs/backend/fundamentals/error-handling.md | Result 패턴, backoff+jitter, circuit breaker(3-state) + rate limiter 조합, RFC 9457 problem+json 통일. 출처: [Azure Circuit Breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) |
| 인증/인가 | ../../../../docs/backend/fundamentals/auth.md | OAuth 2.1 Authorization Code + PKCE 필수 (Implicit/ROPC 금지), RFC 9068 JWT profile, 고보안 시 FAPI 2.0(DPoP/mTLS + PAR 필수 + JARM 권장). Passkeys/WebAuthn 도입 권장(패스워드 전용 인증은 WARNING). 출처: [RFC 9700](https://datatracker.ietf.org/doc/rfc9700/), [FAPI 2.0 Final](https://openid.net/specs/fapi-security-profile-2_0-final.html), [FIDO Alliance](https://fidoalliance.org/passkeys/) |
| 관측성 | ../../../../docs/backend/patterns/observability.md (TBD) | OTel 3 Signals(Traces+Metrics+Logs) 통합 관측, OTLP 1.10.0, W3C Trace Context 기본 전파, 구조화 로깅(JSON + trace_id/span_id), PII 마스킹 필수. OTel Profiles는 2026-03 Public Alpha — 프로덕션 안정 아님. 출처: [OTel Status](https://opentelemetry.io/docs/specs/status/), [OTLP 1.10.0](https://opentelemetry.io/docs/specs/otlp/) |
| 보안 | ../../../../docs/backend/fundamentals/security.md | OWASP Top 10, 보안 헤더, PII 마스킹 |

## 선택 카테고리

| 카테고리 | 참조 문서 | 도입 기준 |
|----------|-----------|-----------|
| 캐싱 | ../../../../docs/backend/patterns/caching.md | 읽기 비율 높은 데이터 존재 시 |
| 이벤트 | ../../../../docs/backend/patterns/event-driven.md | 비동기 처리, 서비스 간 통신 필요 시. **AsyncAPI 3.0+** 스펙 + **Outbox relay(batch 200-500 + backpressure + checkpoint)** + CDC(Debezium) + idempotency. 메시지 브로커: 대용량→Kafka 4.x(KRaft), 단건→RabbitMQ(Quorum Queues), 경량→NATS. 출처: [microservices.io Outbox](https://microservices.io/patterns/data/transactional-outbox.html), [JavaCodeGeeks Kafka vs RabbitMQ](https://www.javacodegeeks.com/2025/12/event-driven-architecture-kafka-vs-rabbitmq-vs-pulsar-a-2025-decision-framework.html) |
| 테스트 | ../../../../docs/backend/fundamentals/testing.md | 항상 권장. **Pact v4 + Testcontainers** 계약 테스트를 기본 도입. AI-assisted(PactFlow MCP Server) 도입 시 60% 가속. 출처: [prgrmmng Pact+Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact), [PactFlow MCP](https://pactflow.io/blog/pactflow-mcp-server/) |
| API Lifecycle | ../../../../docs/backend/protocols/api-lifecycle.md | 외부 공개 API 시. REST: URL path versioning + Sunset header(RFC 8594). GraphQL: @deprecated + additive evolution |
| 데이터 검증 | ../../../../docs/backend/patterns/validation.md (TBD) | API boundary 검증 필요 시. JSON Schema 중간 포맷으로 프론트(Zod)↔백엔드(Pydantic v2) 일관성 유지. 출처: [Pydantic v2 JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/) |
| 워크플로우 | ../../../../docs/backend/stacks/workflow-engines.md (TBD) | 장기 실행 프로세스, saga 필요 시. Temporal(Worker Versioning, Pinned/Auto-Upgrade) 또는 Dapr v1.17(Workflow + sidecar). 출처: [Temporal Worker Versioning](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning), [Dapr v1.17](https://blog.dapr.io/posts/2026/02/27/dapr-v1.17-is-now-available/) |
