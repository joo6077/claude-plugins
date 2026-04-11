---
version: 1.0.0
last_updated: 2026-04-11
---

# Backend Kit Research Log

> backend-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.
> 다음 사이클에서 중복 리서치를 방지하고, 개선 결정의 근거 출처를 추적한다.

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 7 (research-mode rerun)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 1 | Hexagonal vs Clean vs Onion 2026 | <https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f> | blog | 중간 | 채택 |
| 2 | AWS Prescriptive Hexagonal Architecture | <https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html> | 공식 | 높음 | 채택 |
| 3 | Vaadin DDD + Hexagonal | <https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture> | blog | 중간 | 채택 |
| 4 | GraphQL vs REST vs gRPC 2026 | <https://www.javacodegeeks.com/2026/02/graphql-vs-rest-vs-grpc-the-2026-api-architecture-decision.html> | blog | 중간 | 채택 |
| 5 | OpenAPI 3.1 Specification | <https://swagger.io/specification/> | 공식 | 높음 | 채택 (JSON Schema 완전 호환) |
| 6 | AsyncAPI 3.0 Specification | <https://www.asyncapi.com/docs/reference/specification/v3.0.0> | 공식 | 높음 | 채택 |
| 7 | RFC 9457 Problem Details for HTTP APIs | <https://www.rfc-editor.org/rfc/rfc9457.html> | 표준 | 높음 | 채택 |
| 8 | RFC 9700 OAuth 2.1 BCP | <https://datatracker.ietf.org/doc/rfc9700/> | 표준 | 높음 | 채택 |
| 9 | WorkOS OAuth best practices | <https://workos.com/blog/oauth-best-practices> | blog | 중간 | 채택 |
| 10 | Kong DPoP | <https://konghq.com/blog/engineering/demonstrating-proof-of-possession-dpop-preventing-illegal-access-of-apis> | blog | 중간 | 채택 |
| 11 | microservices.io Transactional Outbox | <https://microservices.io/patterns/data/transactional-outbox.html> | 공식 | 높음 | 채택 |
| 12 | Azure Cosmos Outbox | <https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos> | 공식 | 높음 | 채택 |
| 13 | Solace Event-Driven Architecture patterns | <https://solace.com/event-driven-architecture-patterns/> | blog | 중간 | 채택 |
| 14 | Pact + Testcontainers | <https://prgrmmng.com/contract-testing-with-testcontainers-and-pact> | blog | 중간 | 채택 |
| 15 | Microsoft ISE Pact Contract Testing | <https://devblogs.microsoft.com/ise/pact-contract-testing-because-not-everything-needs-full-integration-tests/> | 공식 | 높음 | 채택 |

### 채택한 인사이트

- **Architecture 카테고리 신설 (9번째)**: Hexagonal / Clean / DDD + Port-Adapter 경계 + 의존성 inward-only + 과복잡도 FAIL 사유. backend-kit audit-criteria 에 신설. 적용: backend-audit, backend-guide, backend-system.
- **하이브리드 API 경계 기준**: REST (CRUD/리소스 지향), GraphQL (클라이언트 요구 조립), gRPC (서비스 간 내부) 를 단일 시스템에서 병용 가능. 경계 원칙은 "클라이언트 성격" + "성능 요건" + "진화 속도". 적용: backend-guide API Design 섹션.
- **OpenAPI 3.1 JSON Schema**: OpenAPI 3.1 이 JSON Schema 2020-12 와 완전 호환. 기존 3.0 의 pseudo-JSON Schema 제약 제거. 적용: backend-system API 템플릿.
- **AsyncAPI 3.0**: 이벤트 기반 API 문서화 표준. Outbox / Kafka / RabbitMQ / SNS 등 채널 정의. 적용: backend-system Event-Driven 섹션.
- **RFC 9700 OAuth 2.1 BCP**: PKCE 필수 (confidential client 포함), Implicit flow 금지, Resource Owner Password Credentials (ROPC) 금지, RFC 9068 JWT profile 준수, DPoP / mTLS sender-constrained token 권장. 적용: backend-audit Security 기준 4건 재작성.
- **DPoP (Demonstrating Proof-of-Possession)**: OAuth 2.1 의 sender-constrained token 메커니즘. Bearer token 탈취 대비 최상위 방어. 적용: backend-guide Auth 섹션.
- **Outbox relay 실무 튜닝**: batch 200~500 + backpressure (처리 지연 시 큐에 재적재) + checkpoint (마지막 처리 position 기록). 실패 시 attempts/DLQ/backoff. 적용: backend-system Event-Driven 섹션.
- **Pact v4 + Testcontainers**: Consumer-driven contract testing. Pact v4 의 message queue pact 지원으로 AsyncAPI / Event 기반 시스템 검증 가능. Testcontainers 로 격리된 인프라 실행. 적용: backend-system Testing 섹션.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `backend-observability` | 런북 | OTel 3 signals 시대 — 공용 계측 가이드 필요 | 중간 | backlog |
| `backend-event` | 코드 스캐폴딩 | AsyncAPI 3.0 + Outbox 패턴 실무 스캐폴딩 | 중간 | backlog |

### 폐기 사유

없음.

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>
