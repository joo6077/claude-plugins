# Backend Audit Criteria

섹션 순서가 `backend-reviewer` 에이전트의 평가 카테고리 순서와 일치한다. 2026-07 기준 최신 표준·BCP·커뮤니티 모범 사례를 반영한다.

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
| 하이브리드 API 경계 선택 | REST/GraphQL/gRPC 선택이 boundary별 설명되어 있다 (단일 프로토콜 강요 금지, public=REST / 다중 클라이언트=GraphQL / internal=gRPC) | [GraphQL vs REST vs gRPC 2026](https://www.javacodegeeks.com/2026/02/graphql-vs-rest-vs-grpc-the-2026-api-architecture-decision.html), [Fordel Studios 2026](https://fordelstudios.com/) |
| API Versioning 전략 | REST: URL path(/v1/) 기본, Header(Accept-Version + Sunset RFC 8594) 보조. GraphQL: 버전 없는 진화(@deprecated + additive changes). Contract-First 스키마 진화 원칙 존재 | [Moesif API Versioning](https://www.moesif.com/blog/technical/api-design/Best-Practices-for-Versioning-REST-and-GraphQL-APIs/), [Dan Vega GraphQL Evolution](https://www.danvega.dev/blog/2025/09/30/api-versioning-with-graphql) |
| 빈 상태 상태코드 일관성 | 원소 0 개인 컬렉션에 200(빈 배열) 또는 204 를 반환한다. 404 는 "대상 리소스의 현재 표현을 찾지 못했거나 존재를 밝히지 않겠다" 는 뜻이므로 **존재하는 빈 컬렉션에 쓰면 FAIL**. 같은 리소스군 안에서 빈 상태 처리가 엔드포인트마다 갈리는 것도 FAIL | [RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.html) |
| Timestamp 직렬화 규칙 | 모든 timestamp 응답 필드가 RFC 3339 문자열이며 타임존 표기가 스펙과 코드에서 일치한다. `Z` / `+00:00`(UTC 가 선호 기준점)과 `-00:00`(UTC 시각은 알지만 로컬 오프셋 미상)은 **의미가 다르므로** 혼용 시 FAIL. OpenAPI 3.1 은 `format` 을 JSON Schema 2020-12 에 위임하고 기본적으로 비검증 애노테이션으로 취급하므로 `format: date-time` 선언만으로 PASS 처리 금지 — 직렬화 코드까지 확인 | [RFC 3339 §4.3](https://www.rfc-editor.org/rfc/rfc3339), [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) |
| 비멱등 write path idempotency | POST/PATCH 등 비멱등 연산에 재시도 안전 경로가 있다 (Idempotency-Key 헤더 또는 동등한 업서트/자연키 dedupe). 헤더 방식 채택 시: 동일 키 재요청은 원 결과를 반환, 원 요청 처리 중이면 409, 같은 키에 다른 페이로드면 422, 필수인데 헤더 누락이면 400. **IETF `draft-ietf-httpapi-idempotency-key-header-07` 는 만료(expired)된 Internet-Draft 이므로 "표준" 으로 서술하면 FAIL** — 사실상 관행으로만 인용한다 | [draft-07 (expired)](https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.html), [IETF datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/) |
| 소비면 정합성 (provider verification) | 응답 형태·상태코드·직렬화가 바뀐 흔적이 있으면 그 응답을 역직렬화하는 소비면 코드가 같은 변경을 반영했는지 확인한다. 소비면이 **같은 저장소 안에 있으면 열거해서 대조**(안 봤으면 감사 누락), 접근 불가한 별도 저장소면 `[미검증]` + 사유. 열거 범위는 파일 경로와 외부 관찰 가능한 동작까지이며 소비면 내부 구현은 판정 대상이 아니다(over-specified contract 방지). 이벤트 계열은 AsyncAPI 가 "수신자 문서를 발신자 문서에서 파생하는 것은 권장되지 않는다" 고 명시하므로 양면 문서 존재 여부로 본다 | [Pact — What is Pact good for](https://docs.pact.io/getting_started/what_is_pact_good_for), [PactFlow BDCT](https://pactflow.io/bi-directional-contract-testing/), [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) |

## 3. Database

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| N+1 부재 | 루프 내 개별 쿼리 없음 | PostgreSQL docs |
| 인덱스 존재 | WHERE/JOIN 컬럼에 적절한 인덱스 | PostgreSQL indexes |
| Connection pooling | 풀링 설정 존재 (HikariCP/PgBouncer) | HikariCP docs |
| Migration 안전성 | expand-contract 패턴 준수 | Martin Fowler |

**정적 대체 판정 규약 (글로벌 개선제안 DA-01/DA-02 흡수)** — 라이브 DB 접속이 불가능한 환경에서 스키마·FK action·인덱스·제약 조건을 판정할 때는 **마이그레이션 파일(DDL) 정적 확인으로 대체 판정할 수 있다.** 이때 근거 열에 `[정적]` 보조 태그와 확인한 마이그레이션 파일 경로를 함께 남긴다. `[정적]` 은 `[미검증]` 을 대체하지 않는 보조 태그이며, 마이그레이션 파일 확인조차 불가능하면 그때 `[미검증]` + 사유를 쓴다. 마이그레이션 파일과 실제 DB 상태가 다를 수 있다는 한계는 리포트에 1 줄로 명시한다.

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
| 통합 테스트 실체 확인 | `tests/integration/` 에 있거나 이름이 integration 인 테스트가 **실제 의존성**(Testcontainers/실 DB/실 브로커)을 쓴다. MockDatabase·인메모리 대체물만 쓰는 테스트를 통합 테스트로 계상하면 FAIL — "인메모리 서비스는 프로덕션 서비스의 모든 기능을 갖지 못하고 동작이 조금씩 다르다"(Testcontainers). 실측 근거: 글로벌 REJECT `API-01` (user 통합 테스트 미존재 — MockDatabase 단위 테스트만 있음) | [Testcontainers](https://testcontainers.com/getting-started/) |
| 마이그레이션 적용 선행 | 통합 테스트 fixture 가 DB 기동 후 마이그레이션을 실행한다 (컨테이너 재사용 시에도 스키마 최신화 경로 존재). 미적용 시 `column ... does not exist` 로 실패한다. 실측 근거: 글로벌 REJECT `DG-03` (로컬 DB 에 마이그레이션 미적용으로 통합 테스트 2 건 실패) | [Testcontainers](https://testcontainers.com/getting-started/) |

## 10. Observability

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 구조화 로깅 | JSON 포맷, 표준 필드명, trace_id/span_id 포함, semantic conventions 준수 | [BetterStack OTel Best Practices](https://betterstack.com/community/guides/observability/opentelemetry-best-practices/) |
| OTel 3 Signals 통합 | Traces + Metrics + Logs 가 OTLP exporter 로 통합 수집된다. W3C Trace Context 가 기본 전파 포맷 | [OTel Specification Status](https://opentelemetry.io/docs/specs/status/), [OTLP 1.10.0](https://opentelemetry.io/docs/specs/otlp/) |
| PII 마스킹 | 로그에 이메일/전화번호/IP 등 개인정보가 마스킹 처리되어 있다 (GDPR/PIPA 준수) | OWASP Logging |
