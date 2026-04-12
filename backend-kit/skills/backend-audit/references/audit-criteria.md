# Backend Audit Criteria

섹션 순서가 `backend-reviewer` 에이전트의 평가 카테고리 순서와 일치한다. 2026-04 기준 최신 표준·BCP·커뮤니티 모범 사례를 반영한다.

## 1. Architecture

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 도메인-persistence 분리 | 도메인 엔티티와 DB 매핑 클래스가 분리되어 있다 (단일 엔티티로 DB 애노테이션·비즈니스 규칙 혼재 없음) | [Vaadin DDD+Hexagonal](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture) |
| Port / Adapter 경계 | 외부 시스템(DB, HTTP, MQ)은 어댑터 경계 뒤에 있고 도메인이 어댑터를 직접 import 하지 않는다 | [AWS Prescriptive Hexagonal](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html) |
| 의존성 방향 inward-only | 외부 레이어가 내부 레이어에 의존하고 반대는 금지 (Clean Architecture의존성 규칙) | [Hexagonal vs Clean 2026](https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f) |
| 과복잡도 경고 | 단순 CRUD에 Hexagonal/DDD/CQRS가 강제되어 있지 않다 (bounded context 2+ 또는 풍부한 규칙이 있어야 적용) | [Hexagonal vs Clean 2026](https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f) |
| Modular Monolith First | 팀 규모 10명 미만이면서 마이크로서비스를 도입했으면 WARNING. 인프라 비용 3.75-6x, 디버깅 시간 35% 증가. Shopify 모델(모놀리스 + 특정 도메인만 추출) 참고 | [ByteIota Modular Monolith 2026](https://byteiota.com/modular-monolith-42-ditch-microservices-in-2026/) |

## 2. API Design

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| HTTP 메서드 의미론 | GET=safe, PUT=전체교체, PATCH=부분수정 | [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110) |
| 에러 응답 포맷 | application/problem+json (RFC 9457) — `type` URI로 문제 유형 식별, `title`/`status`/`detail`/`instance` 필수. 커스텀 확장 필드 허용 | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), [Swagger RFC 9457](https://swagger.io/blog/problem-details-rfc9457-doing-api-errors-well/) |
| 페이지네이션 | 대량 목록에 cursor/keyset 사용 | [Slack Engineering — Evolving Pagination](https://slack.engineering/evolving-api-pagination-at-slack/) |
| OpenAPI 3.1 JSON Schema 호환 | 스펙이 OpenAPI 3.1.x 이상이고 JSON Schema draft와 호환되며 실제 응답과 일치 | [OpenAPI Spec 3.1](https://swagger.io/specification/) |
| 하이브리드 API 경계 선택 | REST/GraphQL/gRPC 선택이 boundary별 설명되어 있다 (단일 프로토콜 강요 금지, public=REST / 다중 클라이언트=GraphQL / internal=gRPC) | [GraphQL vs REST vs gRPC 2026](https://www.javacodegeeks.com/2026/02/graphql-vs-rest-vs-grpc-the-2026-api-architecture-decision.html), [Fordel Studios 2026](https://fordelstudios.com/research/graphql-rest-grpc-2026-decision-framework) |
| API Versioning 전략 | REST: URL path(/v1/) 기본, Header(Accept-Version + Sunset RFC 8594) 보조. GraphQL: 버전 없는 진화(@deprecated + additive changes). Contract-First 스키마 진화 원칙 존재 | [Moesif API Versioning](https://www.moesif.com/blog/technical/api-design/Best-Practices-for-Versioning-REST-and-GraphQL-APIs/), [Dan Vega GraphQL Evolution](https://www.danvega.dev/blog/2025/09/30/api-versioning-with-graphql) |

## 3. Database

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| N+1 부재 | 루프 내 개별 쿼리 없음 | PostgreSQL docs |
| 인덱스 존재 | WHERE/JOIN 컬럼에 적절한 인덱스 | PostgreSQL indexes |
| Connection pooling | 풀링 설정 존재 (HikariCP/PgBouncer) | HikariCP docs |
| Migration 안전성 | expand-contract 패턴 준수 | Martin Fowler |

## 4. Authentication & Authorization

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 비밀번호 해싱 | bcrypt(12+) 또는 Argon2id | OWASP |
| 토큰 저장 | JWT를 localStorage에 미저장 (XSS 탈취 방지) | OWASP Session |
| CORS 설정 | 와일드카드(*) + credentials 미사용 | MDN CORS |
| CSRF 방어 | 쿠키 인증 시 SameSite + 토큰 | OWASP CSRF |
| Authorization Code + PKCE | 모든 public client는 Authorization Code Flow + PKCE 사용 (Implicit grant는 사용 금지) | [RFC 9700 OAuth 2.0 BCP](https://datatracker.ietf.org/doc/rfc9700/) |
| Deprecated grant 금지 | Implicit grant, Resource Owner Password Credentials(ROPC) 미사용 — OAuth 2.1 draft에서 제외 | [WorkOS OAuth BCP](https://workos.com/blog/oauth-best-practices) |
| JWT access token 포맷 | 자가발급 JWT는 RFC 9068 profile (typ=at+jwt, iss/aud/exp/sub/client_id) 준수 | [RFC 9700](https://datatracker.ietf.org/doc/rfc9700/) |
| Sender-constrained tokens | FAPI 2.0 / 고보안 환경은 DPoP(RFC 9449) 또는 mTLS (RFC 8705) binding 적용. FAPI 2.0: confidential client 필수 + PKCE 필수 + PAR 필수 + JARM 권장 | [Kong DPoP](https://konghq.com/blog/engineering/demonstrating-proof-of-possession-dpop-preventing-illegal-access-of-apis), [FAPI 2.0 Final](https://openid.net/specs/fapi-security-profile-2_0-final.html) |
| Passkeys / WebAuthn 지원 | 패스워드 전용 인증만 존재하면 WARNING — Passkeys/WebAuthn 도입 계획 또는 MFA 대안 필요. IAM 플랫폼(Okta, Azure AD, Auth0) drop-in 위젯으로 2-3 스프린트 내 마이그레이션 가능 | [FIDO Alliance Passkeys](https://fidoalliance.org/passkeys/), [Wultra PQC Passkeys](https://www.wultra.com/blog/passkeys-and-fido2-quietly-became-quantum-safe-heres-what-changed) |

## 5. Error Handling

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 글로벌 핸들러 | 표준 에러 포맷(RFC 9457 problem+json)으로 변환. `type` URI 필드로 에러 문서 자동 연결 | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), [Swagger RFC 9457](https://swagger.io/blog/problem-details-rfc9457-doing-api-errors-well/) |
| 스택트레이스 미노출 | 프로덕션 에러에 내부 정보 없음 | OWASP |
| Retry 전략 | exponential backoff + jitter | AWS Architecture |
| Circuit breaker | 외부 호출에 3-state(Closed→Open→Half-Open) circuit breaker 적용. Service mesh(Envoy/Istio) 적용도 유효 | [Azure Circuit Breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) |
| Rate Limiter + Circuit Breaker 조합 | Rate Limiter(요청률 제어, abuse 방지)와 Circuit Breaker(장애 전파 차단)를 상호 보완적으로 조합. 단독 적용은 불완전 | [Azure Circuit Breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) |

## 6. Security

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| Injection 방어 | 파라미터화된 쿼리 | OWASP Top 10 |
| XSS 방어 | 출력 인코딩 + CSP | OWASP XSS |
| 보안 헤더 | HSTS, X-Content-Type-Options, CSP | OWASP Headers |
| 시크릿 관리 | 하드코딩 없음, 환경변수/vault | OWASP |
| PII 로깅 | 로그에 이메일/전화번호/IP 미노출 | OWASP Logging |

## 7. Caching

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| TTL 존재 | 모든 캐시 키에 TTL 설정 | Redis docs |
| Stampede 방지 | 인기 키에 lock/early expiry | Cloudflare |
| 무효화 전략 | TTL만이 아닌 이벤트 기반 | Azure Architecture |

## 8. Event-Driven

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| Idempotency | consumer에 중복 처리 방어 (dedupe key, per-aggregate sequence) | Stripe |
| DLQ 존재 | 실패 메시지 격리 경로 | AWS SQS |
| 이중쓰기 방지 | outbox 패턴 또는 동등한 원자성 | [microservices.io Outbox](https://microservices.io/patterns/data/transactional-outbox.html) |
| Outbox relay 실무 패턴 | relay는 200-500 rows batch + windowed concurrency backpressure + checkpoint commit on batch success | [Azure Cosmos Outbox](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos) |
| Retry / Backoff / DLQ | PublishedAt / Attempts 컬럼 + exponential backoff + DLQ routing 구현 | [Solace EDA patterns](https://solace.com/event-driven-architecture-patterns/) |
| AsyncAPI 3.x 스펙 | 이벤트 API는 AsyncAPI 3.0+ 스펙 + bindings 정의 (REST에서 OpenAPI가 차지하는 위치) | [AsyncAPI 3.0 spec](https://www.asyncapi.com/docs/reference/specification/v3.0.0) |
| CDC 파이프라인 | 기존 DB에서 코드 변경 없이 이벤트 스트리밍 시 CDC(Debezium 등) 사용. Outbox+CDC 조합으로 exactly-once 보장 가능 | [Debezium Event Sourcing vs CDC](https://debezium.io/blog/2020/02/10/event-sourcing-vs-cdc/), [Streamkap CDC](https://streamkap.com/resources-and-guides/event-sourcing-cdc) |
| 메시지 브로커 선택 근거 | 대용량 텔레메트리/로그→Kafka 4.x(KRaft, ZooKeeper 제거), 트랜잭션 단건→RabbitMQ(Quorum Queues), 경량 pub/sub→NATS. 선택 근거가 문서화되어 있다 | [JavaCodeGeeks Kafka vs RabbitMQ vs Pulsar 2025](https://www.javacodegeeks.com/2025/12/event-driven-architecture-kafka-vs-rabbitmq-vs-pulsar-a-2025-decision-framework.html) |

## 9. Testing

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 테스트 존재 | 핵심 로직에 단위 테스트 | Google Testing Blog |
| DB 테스트 | 실제 DB (Testcontainers 등) | Testcontainers |
| Contract test (Pact v4+) | consumer-driven contract, Pact v4 + Testcontainers 기반, GraphQL/async 메시지 지원. AI-assisted contract testing(PactFlow MCP Server) 도입 시 생성/유지보수 60% 가속화 가능 | [prgrmmng Pact+Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact), [PactFlow MCP Server](https://pactflow.io/blog/pactflow-mcp-server/) |
| Mock 정합성 | mock이 실제 API와 drift 없음 (Pact provider verification) | [Microsoft ISE Pact](https://devblogs.microsoft.com/ise/pact-contract-testing-because-not-everything-needs-full-integration-tests/) |

## 10. Observability

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 구조화 로깅 | JSON 포맷, 표준 필드명, trace_id/span_id 포함, semantic conventions 준수 | [BetterStack OTel Best Practices](https://betterstack.com/community/guides/observability/opentelemetry-best-practices/) |
| OTel 3 Signals 통합 | Traces + Metrics + Logs 가 OTLP exporter 로 통합 수집된다. W3C Trace Context 가 기본 전파 포맷 | [OTel Specification Status](https://opentelemetry.io/docs/specs/status/), [OTLP 1.10.0](https://opentelemetry.io/docs/specs/otlp/) |
| PII 마스킹 | 로그에 이메일/전화번호/IP 등 개인정보가 마스킹 처리되어 있다 (GDPR/PIPA 준수) | OWASP Logging |
