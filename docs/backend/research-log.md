---
version: 1.1.0
last_updated: 2026-05-07
---

# Backend Kit Research Log

> backend-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.
> 다음 사이클에서 중복 리서치를 방지하고, 개선 결정의 근거 출처를 추적한다.

## [2026-05-07] — Phase 7 kaizen (backend, /insights 흡수)

### 데이터 소스

- 데이터 풀 §0 `/insights` 30 일 분석 (3 friction · 3 pattern · 3 feature)
- `harness/references/cross-kit-principles.md` v1 매트릭스의 backend 열

### Phase 7 변경

- backend/README.md 에 cross-kit-principles 매트릭스 cross-reference 섹션 추가
- plugin.json patch bump (이번 사이클)
- 매핑: backend-audit ANALYZE ↔ Pre-Edit Batch Audit, backend-reviewer self-check ↔ Self-Evaluator Audit, PostToolUse 정적 검증 ↔ Hook-Triggered Auto-Correction

### 외부 리서치 인용 (이전 사이클 보존, 이번 사이클 추가 없음)

이전 카이젠 사이클의 리서치 인용은 본 로그 하단 + cross-kit-principles 매트릭스로 보존된다.

---


---

## 2026-04-12

**트리거:** backend-research 스킬 실행 (12개 토픽 확장 리서치)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
| - | ---- | --- | ---- | ---- | ---- |
| 16 | FAPI 2.0 Security Profile (Final) | <https://openid.net/specs/fapi-security-profile-2_0-final.html> | spec | [spec] [dated: 2025-02] | 채택 |
| 17 | ScaleKit — OAuth 2.0 Best Practices RFC 9700 | <https://www.scalekit.com/blog/oauth-2-0-best-practices-rfc9700> | blog | [blog] | 참조 |
| 18 | FIDO Alliance Passkeys | <https://fidoalliance.org/passkeys/> | official | [official] | 채택 |
| 19 | Wultra — Passkeys and FIDO2 Quantum-Safe | <https://www.wultra.com/blog/passkeys-and-fido2-quietly-became-quantum-safe-heres-what-changed> | blog | [blog] [dated: 2025-04] | 채택 |
| 20 | Microsoft Learn — Passkeys (FIDO2) in Entra ID | <https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-passkeys-fido2> | official | [official] | 참조 |
| 21 | OpenTelemetry Specification Status Summary | <https://opentelemetry.io/docs/specs/status/> | official | [official] | 채택 |
| 22 | OpenTelemetry OTLP 1.10.0 Specification | <https://opentelemetry.io/docs/specs/otlp/> | official | [official] | 채택 |
| 23 | OpenTelemetry AI Agent Observability Blog | <https://opentelemetry.io/blog/2025/ai-agent-observability/> | official | [official] [dated: 2025] | 참조 |
| 24 | BetterStack — OpenTelemetry Best Practices | <https://betterstack.com/community/guides/observability/opentelemetry-best-practices/> | blog | [blog] | 채택 |
| 25 | AWS Prescriptive Guidance — Event Sourcing Pattern | <https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html> | official | [official] | 채택 |
| 26 | microservices.io — Event Sourcing Pattern | <https://microservices.io/patterns/data/event-sourcing.html> | official | [official] | 채택 |
| 27 | Debezium — Event Sourcing vs CDC | <https://debezium.io/blog/2020/02/10/event-sourcing-vs-cdc/> | blog | [blog] [dated: 2020-02] | 참조 |
| 28 | Streamkap — Event Sourcing with CDC | <https://streamkap.com/resources-and-guides/event-sourcing-cdc> | blog | [blog] | 채택 |
| 29 | Azure Architecture — Circuit Breaker Pattern | <https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker> | official | [official] | 채택 |
| 30 | 1xAPI — Circuit Breaker & Retry Node.js 2026 | <https://1xapi.com/blog/resilient-api-circuit-breaker-bulkhead-retry-nodejs-2026> | blog | [blog] | 참조 |
| 31 | Moesif — API Versioning REST and GraphQL | <https://www.moesif.com/blog/technical/api-design/Best-Practices-for-Versioning-REST-and-GraphQL-APIs/> | blog | [blog] | 채택 |
| 32 | NerdLevelTech — Mastering API Versioning | <https://nerdleveltech.com/mastering-api-versioning-strategies-tradeoffs-and-best-practices> | blog | [blog] | 채택 |
| 33 | Dan Vega — GraphQL API Evolution Without Versioning | <https://www.danvega.dev/blog/2025/09/30/api-versioning-with-graphql> | blog | [blog] [dated: 2025-09] | 채택 |
| 34 | ByteByte Go — Monolith vs Microservices vs Modular Monolith | <https://blog.bytebytego.com/p/monolith-vs-microservices-vs-modular> | blog | [blog] | 채택 |
| 35 | ByteIota — 42% Ditch Microservices in 2026 | <https://byteiota.com/modular-monolith-42-ditch-microservices-in-2026/> | blog | [blog] | 채택 |
| 36 | JavaCodeGeeks — Microservices vs Modular Monoliths 2025 | <https://www.javacodegeeks.com/2025/12/microservices-vs-modular-monoliths-in-2025-when-each-approach-wins.html> | blog | [blog] [dated: 2025-12] | 채택 |
| 37 | AWS Blog — Lambda Cold Start Remediation | <https://aws.amazon.com/blogs/compute/understanding-and-remediating-cold-starts-an-aws-lambda-perspective/> | official | [official] | 채택 |
| 38 | AWS Blog — SnapStart Advanced Priming Strategies | <https://aws.amazon.com/blogs/compute/optimizing-cold-start-performance-of-aws-lambda-using-advanced-priming-strategies-with-snapstart/> | official | [official] | 채택 |
| 39 | JavaCodeGeeks — Serverless Java 2026 | <https://www.javacodegeeks.com/2025/12/serverless-java-in-2026-aws-lambda-azure-functions-and-beyond.html> | blog | [blog] [dated: 2025-12] | 참조 |
| 40 | Pact Docs — Contract Testing | <https://docs.pact.io/> | official | [official] | 채택 |
| 41 | PactFlow — MCP Server AI-Powered Contract Testing | <https://pactflow.io/blog/pactflow-mcp-server/> | blog | [blog] | 채택 |
| 42 | Sachith — Pact Best Practices 2025 Practical Guide | <https://www.sachith.co.uk/contract-testing-with-pact-best-practices-in-2025-practical-guide-feb-10-2026/> | blog | [blog] [dated: 2026-02] | 참조 |
| 43 | Apollo GraphQL — Federation Docs | <https://www.apollographql.com/docs/graphos/schema-design/federated-schemas/federation> | official | [official] | 채택 |
| 44 | WunderGraph — GraphQL Federation over gRPC | <https://wundergraph.com/blog/graphql-federation-over-grpc> | blog | [blog] | 채택 |
| 45 | Swagger — RFC 9457 Problem Details for API Errors | <https://swagger.io/blog/problem-details-rfc9457-doing-api-errors-well/> | blog | [blog] | 채택 |
| 46 | Swagger — RFC 9457 Hands-On API Error Handling | <https://swagger.io/blog/problem-details-rfc9457-api-error-handling/> | blog | [blog] | 참조 |
| 47 | Pydantic v2 JSON Schema Docs | <https://docs.pydantic.dev/latest/concepts/json_schema/> | official | [official] | 채택 |
| 48 | SuperJSON — Pydantic vs Zod JSON Schema Comparison | <https://superjson.ai/blog/2025-08-14-pydantic-vs-zod-json-schema-generation-comparison/> | blog | [blog] [dated: 2025-08] | 채택 |
| 49 | JavaCodeGeeks — Kafka vs RabbitMQ vs Pulsar 2025 | <https://www.javacodegeeks.com/2025/12/event-driven-architecture-kafka-vs-rabbitmq-vs-pulsar-a-2025-decision-framework.html> | blog | [blog] [dated: 2025-12] | 채택 |
| 50 | arxiv — Next-Gen Event-Driven Architectures Performance | <https://arxiv.org/html/2510.04404v2> | paper | [paper] | 채택 |
| 51 | Fordel Studios — GraphQL vs REST vs gRPC 2026 Decision Framework | <https://fordelstudios.com/research/graphql-rest-grpc-2026-decision-framework> | blog | [blog] | 채택 |

### 채택한 인사이트

#### 1. FAPI 2.0 Security Profile (인증/인가 강화)

- FAPI 2.0 Final 이 2025-02 에 공개됨. 고가치 API(금융, 의료, 정부)를 위한 OAuth 2.0 보안 프로필.
- **핵심 요구사항**: confidential client 필수, PKCE 필수, sender-constrained token(DPoP 또는 mTLS), PAR(Pushed Authorization Requests) 필수, JARM(JWT-Secured Authorization Response Mode) 권장.
- 기존 RFC 9700 의 OAuth 2.1 BCP 위에 추가 레이어로 적용.
- **적용**: backend-audit Security 기준에 FAPI 2.0 compliance 체크 항목 추가, backend-guide Auth 섹션에 "고가치 API → FAPI 2.0" 판단 기준 추가.

#### 2. Passkeys / WebAuthn / FIDO2 (패스워드리스 인증)

- FIDO Alliance 기준, 2026 은 대규모 패스워드리스 전환의 전환점.
- 2025-04 IANA COSE 코드리스트 업데이트로 **양자 안전 암호화(PQC) 알고리즘** 공식 추가 — Passkeys 가 quantum-safe 로 진화.
- **백엔드 구현 실무**: IAM 플랫폼(Okta, Azure AD, Auth0)이 drop-in passkey 위젯 제공. 마이그레이션 기간 2-3 스프린트로 단축.
- ASP.NET Core Identity 가 내장 passkey 등록/인증 지원 (Blazor Web App 템플릿 포함).
- **적용**: backend-guide Auth 섹션에 Passkeys 가이드 추가, backend-audit 에 "패스워드 전용 인증 → WARNING" 기준 추가.

#### 3. OpenTelemetry Logs Stable GA + OTLP 1.10.0

- OTel 의 세 신호(Traces, Metrics, Logs) 모두 **Stable** 상태 도달. OTLP 1.10.0 스펙.
- Logs 가 stable 로 올라가면서 "3 signals 통합 관측" 이 프로덕션 레디.
- **W3C Trace Context** 가 기본 전파 포맷 — 커스텀 propagation 불필요.
- **AI Agent Observability**: OTel 이 2025 부터 AI 에이전트 계측 표준을 논의 중. LLM 호출, 토큰 사용량, 에이전트 체인 추적 등.
- **구조화 로깅 필수 패턴**: JSON 포맷, 표준 필드명, trace_id/span_id 포함, 커스텀 속성은 semantic conventions 준수.
- **적용**: backend-observability 스킬 backlog → 우선순위 상향, backend-guide Observability 섹션 갱신.

#### 4. CQRS / Event Sourcing / Outbox / CDC 패턴 정리

- **Event Sourcing**: 비즈니스 엔티티를 상태 변경 이벤트 시퀀스로 저장. 100% 감사 추적, 시간 여행 쿼리 가능. 단 학습 곡선 높고 CQRS 와 조합 필수.
- **CDC (Change Data Capture)**: 대부분의 팀에서 실용적 시작점. Debezium 등으로 기존 DB 에서 코드 변경 없이 이벤트 스트리밍. 이후 Outbox 또는 Event Sourcing 으로 점진 이행.
- **Outbox + CDC 조합**: 비즈니스 테이블과 outbox 테이블에 같은 트랜잭션으로 쓰기 → CDC 로 outbox 읽기 → 메시지 큐 발행. exactly-once 보장.
- **CQRS + Outbox**: 애플리케이션 DB 내 강한 일관성 + CQRS 프로젝션은 eventual consistency.
- **2026 트렌드**: 고동시성 시스템에서 CQRS + Event Sourcing 이 기본 선택으로 자리잡는 추세.
- **적용**: backend-system Event-Driven 섹션에 CDC 파이프라인 가이드 추가, backend-event 스킬 backlog 구체화.

#### 5. Circuit Breaker + Rate Limiting 패턴

- **Circuit Breaker 3-state**: Closed → Open (실패 임계 초과) → Half-Open (시험 요청 허용). Azure Architecture Center 가 레퍼런스 구현 제공.
- **2026 트렌드**: AI/ML 기반 adaptive threshold — 실시간 트래픽 패턴과 이력 기반으로 임계치 동적 조정.
- **Service Mesh 통합**: Envoy/Istio sidecar 로 애플리케이션 코드 변경 없이 circuit breaking 적용 가능.
- **Rate Limiter 와 Circuit Breaker 차이**: Rate Limiter 는 요청률 제어(abuse 방지), Circuit Breaker 는 장애 전파 차단(resilience). 상호 보완적으로 조합.
- **Resilience4j** (Java), **Opossum 9.0.0** (Node.js, 2025-06 릴리스, Node 20+ 필수) 가 주요 라이브러리.
- **적용**: backend-guide Error Handling/Resilience 섹션에 Circuit Breaker + Rate Limiter 조합 패턴 추가.

#### 6. API Versioning 전략

- **REST**: URL path (/v1/, /v2/) 가 가장 단순하고 널리 사용. Header-based (Accept-Version, Sunset RFC 8594) 도 지원.
- **GraphQL**: 버전 없는 진화가 원칙 — field deprecation + additive changes. `@deprecated` 디렉티브로 점진 마이그레이션.
- **2026 현황**: 약 2/3 팀이 REST public endpoint, 40% 가 GraphQL 신규 기능 시범, 25% 가 gRPC 내부 서비스. 하이브리드 스택이 대세.
- **Contract-First**: OpenAPI + GraphQL introspection 으로 스키마 우선 진화, 버전 증식 대신 incremental evolution.
- **적용**: backend-guide API Design 섹션에 versioning 전략 비교표 추가.

#### 7. Microservices vs Modular Monolith (2026 동향)

- **2025 CNCF 설문**: 마이크로서비스 도입 조직의 42% 가 서비스를 더 큰 배포 단위로 통합 중.
- **비용**: 마이크로서비스 인프라 비용이 모놀리스 대비 3.75x~6x. 월 $15K vs $40K-65K (인프라+운영+플랫폼팀+협업 오버헤드 포함).
- **디버깅**: DZone 2024 연구 — 마이크로서비스 아키텍처에서 디버깅에 평균 35% 더 많은 시간 소요.
- **팀 규모 기준**: 개발자 10명 미만이면 모놀리스가 일관되게 우월. 마이크로서비스 이점은 10명+ 부터.
- **사례**: Amazon Prime Video — 분산 마이크로서비스 → 단일 프로세스 모놀리스로 전환, 인프라 비용 90% 절감. Shopify — 모듈러 모놀리스 유지, checkout/fraud 등 특정 도메인만 마이크로서비스 추출.
- **적용**: backend-guide Architecture 섹션에 "Modular Monolith First" 전략 가이드 추가, backend-audit Architecture 기준에 "팀 규모 < 10 + 마이크로서비스 = WARNING" 추가.

#### 8. Serverless Cold Start 완화 패턴

- **SnapStart**: 초기화된 실행 환경의 스냅샷을 촬영. Java 11+ (Corretto), .NET 8 Native AOT 지원. Java 기존 3-10초 → 200-400ms (약 10x 개선).
- **주의점**: 랜덤, 타임스탬프, 네트워크 연결이 스냅샷에 동결됨 → Restore phase 훅으로 재초기화 필수.
- **Provisioned Concurrency**: 가장 확실하지만 가장 비싼 옵션. 예약된 동시성 만큼 cold start 제거.
- **코드 레벨 최적화**: 패키지 크기 최소화 (MB 당 ms 증가), 메모리 할당 증가 (512MB 가 128MB 보다 cold start 40% 빠름 — CPU 비례 할당).
- **런타임별**: Go/Rust 가 compiled 중 최고 (sub-100ms), .NET 8 AOT + SnapStart 로 경쟁력 확보.
- **적용**: backend-guide Serverless 섹션 신설, "cold start 완화 결정 트리" 추가.

#### 9. Contract Testing + AI 도구 (Pact 진화)

- Pact 는 code-first consumer-driven contract testing 도구. HTTP + message queue pact 지원.
- **PactFlow MCP Server**: AI 기반 계약 테스트 도구가 IDE 에 통합. 테스트 생성/유지보수 60% 가속화.
- **2026 주요 도구**: TestSprite, Pact, Spring Cloud Contract, Specmatic, Karate.
- **Pact + Testcontainers**: 격리된 인프라에서 consumer-driven 계약 검증. AsyncAPI/Event 기반 시스템도 검증 가능 (기존 리서치 #14 와 연계).
- **적용**: backend-system Testing 섹션에 "AI-assisted contract testing" 추가, 도구 비교표 추가.

#### 10. GraphQL Federation + gRPC 하이브리드 (최신 패턴)

- **Apollo Federation 2**: supergraph + subgraph 아키텍처. 라우터가 요청을 분배하고 통합 응답 반환.
- **gRPC over Federation**: WunderGraph 가 제안 — subgraph SDL 을 gRPC 서비스로 직접 컴파일. `_entities` 해석 대신 strictly typed gRPC 인터페이스로 대체. compile-time safety + batching + 성능 향상.
- **실무 패턴**: GraphQL 은 API boundary (클라이언트 대면), gRPC 은 내부 서비스 간 통신.
- **적용**: backend-guide API Design 섹션에 "Federation + gRPC 하이브리드" 패턴 추가.

#### 11. RFC 9457 Problem Details (에러 핸들링 강화)

- RFC 9457 이 RFC 7807 을 대체. `type`, `title`, `status`, `detail`, `instance` 필드로 구조화된 에러 응답.
- **type 필드 개선**: URI 레퍼런스로 문제 유형을 식별. 문서화 자동 연결.
- **확장성**: 커스텀 필드 추가 가능. 분산 시스템 디버깅에 특히 유용.
- **프레임워크 지원**: Spring Boot (ErrorResponse), ASP.NET Core (ProblemDetails), Express.js (수동 구현) 등.
- **적용**: backend-guide Error Handling 섹션에 RFC 9457 적용 가이드 구체화 (기존 #7 소스와 연계).

#### 12. Data Validation: Pydantic v2 / Zod / JSON Schema 크로스 에코시스템

- **Pydantic v2**: Rust 코어로 v1 대비 5-50x 성능 향상. 모델 인스턴스화 17x, 검증 5x, 직렬화 10x 빠름.
- **Zod**: TypeScript-first, 뛰어난 타입 추론. React Hook Form 과 최적 조합.
- **크로스 에코시스템 전략**: JSON Schema 를 중간 포맷으로 사용하여 프론트(Zod) ↔ 백엔드(Pydantic) 일관성 유지. pydantic2zod 도구로 양방향 변환.
- **12-layer validation**: 입력 → API boundary → 비즈니스 로직 → 데이터 저장까지 다층 검증 패턴.
- **적용**: backend-guide Data Validation 섹션 신설.

#### 13. Message Queue: Kafka 4.x / RabbitMQ Quorum Queues

- **Kafka 4.1.x**: KRaft 완전 도입으로 ZooKeeper 제거 → 단일 바이너리 배포. Queues (preview) 기능으로 point-to-point 메시지 처리 지원. eBay 가 하루 100억+ 이벤트 처리.
- **RabbitMQ**: Quorum Queues 가 기본 HA — Raft 합의 기반 split-brain 해결. 개별 메시지 최저 지연시간 (sub-ms 가능).
- **선택 기준**: 대용량 텔레메트리/로그 → Kafka, 트랜잭션 메시지 라우팅/정확한 단건 처리 → RabbitMQ, 경량 pub/sub → NATS.
- **Exactly-Once**: Kafka 는 트랜잭셔널 프로듀서 + 멱등 컨슈머. RabbitMQ 는 Quorum Queues 로 강한 일관성.
- **적용**: backend-system Event-Driven 섹션에 메시지 브로커 선택 가이드 추가.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `backend-observability` | 런북 | OTel 3 signals stable — 프로덕션 레디 계측 가이드 시급 | 높음 | backlog (우선순위 상향) |
| `backend-event` | 코드 스캐폴딩 | AsyncAPI 3.0 + Outbox + CDC 파이프라인 스캐폴딩 | 중간 | backlog |
| `backend-resilience` | 런북 | Circuit Breaker + Rate Limiter + Retry 조합 패턴 가이드 | 중간 | backlog (신규) |
| `backend-validation` | 런북 | Pydantic v2 / Zod / JSON Schema 크로스 에코시스템 검증 가이드 | 낮음 | backlog (신규) |
| `backend-serverless` | 런북 | Cold start 완화 + SnapStart + runtime 선택 가이드 | 낮음 | backlog (신규) |

### 폐기 사유

없음.

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

---

## 2026-04-12

**트리거:** backend-research 스킬 실행 (백엔드 최신 스택 보강 리서치)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
| - | ---- | --- | ---- | ---- | ---- |
| 52 | IETF OAuth 2.1 Authorization Framework Draft 15 | <https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/> | spec | [spec] [dated: 2026-03] | 채택 |
| 53 | OpenTelemetry Profiles Enters Public Alpha | <https://opentelemetry.io/blog/2026/profiles-alpha/> | official | [official] [dated: 2026-03] | 채택 |
| 54 | OpenTelemetry Profiles Specification | <https://opentelemetry.io/docs/specs/otel/profiles/> | official | [official] | 채택 |
| 55 | Dapr v1.17 is now available | <https://blog.dapr.io/posts/2026/02/27/dapr-v1.17-is-now-available/> | official | [official] [dated: 2026-02] | 채택 |
| 56 | Dapr Workflow Docs | <https://docs.dapr.io/developing-applications/building-blocks/workflow/> | official | [official] | 채택 |
| 57 | Temporal Worker Versioning Docs | <https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning> | official | [official] | 채택 |
| 58 | Temporal TypeScript Workflow Versioning Docs | <https://docs.temporal.io/develop/typescript/workflows/versioning> | official | [official] | 채택 |
| 59 | Effect Documentation — Expected Errors | <https://effect.website/docs/error-management/expected-errors/> | official | [official] | 채택 |
| 60 | Bun 1.3 Release Blog | <https://bun.com/blog/bun-v1.3> | official | [official] [dated: 2025-10] | 채택 |
| 61 | Bun Node.js Compatibility Docs | <https://bun.com/docs/runtime/nodejs-compat> | official | [official] | 채택 |
| 62 | Prisma ORM vs Drizzle | <https://docs.prisma.io/docs/orm/more/comparisons/prisma-and-drizzle> | official | [official] | 채택 |
| 63 | Drizzle ORM Overview | <https://orm.drizzle.team/docs/overview> | official | [official] | 채택 |
| 64 | tRPC v11 Migration Guide | <https://trpc.io/docs/migrate-from-v10-to-v11> | official | [official] | 채택 |
| 65 | tRPC v11 Server Components Guide | <https://trpc.io/docs/client/tanstack-react-query/server-components> | official | [official] | 채택 |
| 66 | Hono Docs | <https://hono.dev/docs> | official | [official] | 채택 |
| 67 | Cloudflare D1 Overview | <https://developers.cloudflare.com/d1/> | official | [official] | 채택 |
| 68 | Cloudflare D1 Global Read Replication | <https://developers.cloudflare.com/d1/best-practices/read-replication/> | official | [official] | 채택 |
| 69 | Cloudflare Durable Objects Overview | <https://developers.cloudflare.com/durable-objects/> | official | [official] | 채택 |
| 70 | TiDB Cloud Starter FAQs | <https://docs.pingcap.com/tidbcloud/serverless-faqs/> | official | [official] | 채택 |
| 71 | TiDB Cloud Branching (Beta) Overview | <https://docs.pingcap.com/tidbcloud/branch-overview> | official | [official] | 채택 |
| 72 | TiDB Cloud Vector Search Overview | <https://docs.pingcap.com/tidbcloud/vector-search-overview/> | official | [official] | 채택 |
| 73 | Neon Documentation | <https://neon.com/docs/introduction> | official | [official] | 채택 |
| 74 | Turso Branching | <https://docs.turso.tech/features/branching> | official | [official] | 채택 |
| 75 | Turso Embedded Replicas | <https://docs.turso.tech/features/embedded-replicas/introduction> | official | [official] | 채택 |
| 76 | OpenAI File Search Guide | <https://platform.openai.com/docs/guides/tools-file-search?lang=javascript> | official | [official] | 채택 |
| 77 | OpenAI Function Calling Guide | <https://developers.openai.com/api/docs/guides/function-calling> | official | [official] | 채택 |

### 토픽별 처리 결과

- OAuth 2.1 finalization status (RFC timeline): 기존 #8, #16, #17 참고 + 신규 #52 추가
- OpenTelemetry Profiling signal progress: 기존 #21-#24 참고 + 신규 #53, #54 추가
- Dapr (Distributed Application Runtime) latest: 신규 #55, #56 추가
- Temporal.io workflow engine latest patterns: 신규 #57, #58 추가
- Effect-TS and functional error handling in TypeScript backends: 신규 #59 추가
- Bun runtime for backend services (stability, adoption): 신규 #60, #61 추가
- Drizzle ORM vs Prisma latest comparison: 신규 #62, #63 추가
- tRPC v11 and type-safe API patterns: 신규 #64, #65 추가
- Hono.js as lightweight backend framework: 신규 #66 추가
- Edge computing backends (Cloudflare Workers D1, Durable Objects): 신규 #67, #68, #69 추가
- Database: TiDB Serverless, Neon Postgres, Turso/libSQL latest: 신규 #70, #71, #72, #73, #74, #75 추가
- AI-augmented backends (LLM integration patterns, RAG architectures): 기존 #23 참고 + 신규 #76, #77 추가

### 채택한 인사이트

#### 1. OAuth 2.1 finalization status (RFC timeline)

- OAuth 2.1 은 2026-04 기준 최종 RFC 가 아니고, 최신 문서는 `draft-ietf-oauth-v2-1-15` 상태의 Active Internet-Draft 이다. `Last updated 2026-03-02`, `Expires 2026-09-03` 로 표시된다. (출처: <https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/> [spec] [dated: 2026-03])
- 실무적으로는 OAuth 2.1 을 "새 보안 요구사항을 통합한 단일 RFC" 로 기다리기보다, 기존에 채택한 RFC 9700 보안 BCP(#8) 와 FAPI 2.0 Final(#16) 을 현재 기준선으로 유지하는 편이 맞다. (출처: <https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/> [spec] [dated: 2026-03], <https://datatracker.ietf.org/doc/rfc9700/> [spec], <https://openid.net/specs/fapi-security-profile-2_0-final.html> [spec] [dated: 2025-02])

#### 2. OpenTelemetry Profiling signal progress

- OTel Profiles 는 2026-03 에 Public Alpha 로 진입했고, 연속 프로덕션 프로파일링을 traces / metrics / logs 옆의 공용 신호로 표준화하려는 단계다. 아직 critical production workload 용 안정 신호는 아니다. (출처: <https://opentelemetry.io/blog/2026/profiles-alpha/> [official] [dated: 2026-03], <https://opentelemetry.io/docs/specs/otel/profiles/> [official])
- 프로파일 샘플에 `trace_id` / `span_id` 를 연결하고 Collector 파이프라인, eBPF agent, OTLP Profiles 를 함께 쓰는 방향이 공식 로드맵이다. 기존 "3 signals" 관측에서 "4th signal 후보" 로 확장되는 흐름으로 봐야 한다. (출처: <https://opentelemetry.io/blog/2026/profiles-alpha/> [official] [dated: 2026-03], <https://opentelemetry.io/docs/specs/otel/profiles/> [official])

#### 3. Dapr latest

- Dapr 최신 메이저 흐름은 v1.17 이고, 핵심 변화는 Workflow Versioning, state retention policy, workflow tracing, Bulk PubSub API stable 이다. 특히 workflow throughput 이 최대 41% 향상되었다고 공식 릴리스 노트가 밝힌다. (출처: <https://blog.dapr.io/posts/2026/02/27/dapr-v1.17-is-now-available/> [official] [dated: 2026-02])
- Dapr Workflows 는 이제 장기 실행 워크플로우를 안전하게 진화시키는 운영 패턴에 더 가까워졌고, 버저닝과 tracing 이 들어오면서 단순 sidecar primitive 를 넘어 orchestration 계층으로 쓰기 쉬워졌다. (출처: <https://blog.dapr.io/posts/2026/02/27/dapr-v1.17-is-now-available/> [official] [dated: 2026-02], <https://docs.dapr.io/developing-applications/building-blocks/workflow/> [official])

#### 4. Temporal.io workflow engine latest patterns

- Temporal 은 2026 기준 Worker Versioning 을 "production 에서의 기본 권장" 으로 두고 있으며, 가능하면 patching 보다 Worker Versioning 을 우선하라고 문서화한다. 다만 기능 상태는 아직 Public Preview 다. (출처: <https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning> [official], <https://docs.temporal.io/develop/typescript/workflows/versioning> [official])
- 최신 패턴은 `Pinned` / `Auto-Upgrade` 를 워크플로우 유형별로 나누고, 장기 실행 워크플로우는 `Continue-as-New` 경계에서 업그레이드하는 것이다. AI agent / chatbot 같은 주 단위 워크플로우도 `Pinned + upgrade on CaN` 예시로 직접 제시된다. (출처: <https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning> [official], <https://docs.temporal.io/develop/typescript/workflows/versioning> [official])

#### 5. Effect-TS and functional error handling

- Effect 는 `Effect<Success, Error, Requirements>` 타입에서 에러 채널을 타입 수준으로 추적한다. 기대 가능한 실패를 예외가 아니라 값으로 다루고, `catchAll` / `catchTag` 처리 후 에러 타입을 `never` 로 수렴시키는 패턴이 공식 문서의 중심이다. (출처: <https://effect.website/docs/error-management/expected-errors/> [official])
- TypeScript 백엔드에서 이 접근은 "throw 중심 예외 흐름" 보다 도메인 에러를 명시적으로 모델링하기 좋다. 특히 validation / HTTP / infra 에러를 합성하고 복구 정책을 타입으로 노출하는 데 유리하다. (출처: <https://effect.website/docs/error-management/expected-errors/> [official])

#### 6. Bun runtime for backend services

- Bun 1.3 계열은 내장 Postgres / MySQL / SQLite / Redis 클라이언트, `Bun.serve()` 라우팅, 단일 프로세스 full-stack 실행을 전면에 내세우며 백엔드 런타임 포지셔닝을 강화했다. (출처: <https://bun.com/blog/bun-v1.3> [official] [dated: 2025-10])
- 안정성 판단의 핵심은 Node 호환성이다. Bun 문서는 최신 버전 기준으로 Node API 호환성을 지속 갱신하고, Node test suite 수천 건을 매 릴리스 전에 돌리며, Node 에서 동작하는 패키지가 Bun 에서 안 되면 Bun 버그로 간주한다고 명시한다. 따라서 "빠른 실험용" 단계를 넘어 Express/Next 급 호환 워크로드까지 겨냥하고 있다. (출처: <https://bun.com/docs/runtime/nodejs-compat> [official], <https://bun.com/blog/bun-v1.3> [official] [dated: 2025-10])

#### 7. Drizzle ORM vs Prisma latest comparison

- Prisma 공식 비교 문서는 Prisma 를 "complete type-safe data toolkit" 으로, Drizzle 을 headless / driver-first ORM 으로 위치시킨다. Prisma 는 Schema, Client, Studio, native integrations 를 묶은 batteries-included 접근이고, Drizzle 은 SQL-like query 와 opt-in tooling 을 강조한다. (출처: <https://docs.prisma.io/docs/orm/more/comparisons/prisma-and-drizzle> [official], <https://orm.drizzle.team/docs/overview> [official])
- 2026 선택 기준은 더 선명하다. Cloudflare D1, `bun:sqlite`, HTTP proxy SQLite 같은 edge/serverless 특화 드라이버는 Drizzle 쪽 장점이 있고, DB 종류 폭, Studio, relation mode, 통합 도구체인은 Prisma 쪽 장점이 있다. (출처: <https://docs.prisma.io/docs/orm/more/comparisons/prisma-and-drizzle> [official], <https://orm.drizzle.team/docs/overview> [official])

#### 8. tRPC v11 and type-safe API patterns

- tRPC v11 의 실무 포인트는 TanStack React Query v5 와의 결합, React Server Components 지원 가이드, stricter HTTP semantics 다. v11 migration 문서는 잘못된 `Content-Type` 에 대해 `415 Unsupported Media Type` 를 반환하도록 명시한다. (출처: <https://trpc.io/docs/migrate-from-v10-to-v11> [official], <https://trpc.io/docs/client/tanstack-react-query/server-components> [official])
- 동시에 공식 문서는 RSC 가 tRPC 의 일부 문제를 자체 해결하므로 "tRPC 가 꼭 필요하지 않을 수 있다"고 경고한다. 즉 v11 은 무조건 채택 대상이 아니라, TypeScript 단일 저장소에서 shared types / caller / query hydration 이 중요한 팀에 특히 적합하다. (출처: <https://trpc.io/docs/client/tanstack-react-query/server-components> [official], <https://trpc.io/> [official])

#### 9. Hono.js as lightweight backend framework

- Hono 는 "built on Web Standards" 를 전면에 두고 Cloudflare Workers, Fastly, Deno, Bun, AWS Lambda, Node.js 등 다중 런타임 공용 코드를 지향한다. edge-first 백엔드에서 프레임워크 portability 가 강점이다. (출처: <https://hono.dev/docs> [official])
- Hono Client `hc` 와 validator 조합의 RPC mode 로 서버 API spec 을 클라이언트와 타입 안전하게 공유할 수 있다. 즉 Hono 는 단순 초경량 라우터에 그치지 않고, edge 환경용 타입 안전 API 패턴의 대안으로 볼 수 있다. (출처: <https://hono.dev/docs> [official])

#### 10. Edge computing backends (Cloudflare Workers D1, Durable Objects)

- D1 은 Workers/Pages 에 직접 붙는 serverless SQL 데이터베이스이고, point-in-time `Time Travel` 복구와 다중 소형 DB 분할 전략을 전면에 둔다. (출처: <https://developers.cloudflare.com/d1/> [official])
- 최신 패턴은 D1 단독보다 `D1 + Sessions API + Global read replication` 이다. 읽기 복제는 글로벌 복제본으로 읽기 지연을 낮추지만, 순차 일관성은 Sessions API 의 bookmark 메커니즘으로 보장해야 한다. (출처: <https://developers.cloudflare.com/d1/best-practices/read-replication/> [official])
- Durable Objects 는 compute 와 storage 를 같은 객체에 붙여 상태를 직렬화하고, globally-unique object name 으로 coordination 을 담당한다. 실시간 룸, rate limiter, per-tenant coordinator 같은 stateful edge 제어면에 더 적합하다. (출처: <https://developers.cloudflare.com/durable-objects/> [official])

#### 11. Database: TiDB Serverless, Neon Postgres, Turso/libSQL latest

- TiDB Cloud Serverless 는 2025-08 부터 `TiDB Cloud Starter` 로 이름이 바뀌었고, 자동 확장, HTAP, 벡터 검색, full-text search 를 유지한다. 또 Branching 이 beta 로 들어와 Starter / Essential 클러스터에서 분기 기반 개발이 가능하다. (출처: <https://docs.pingcap.com/tidbcloud/serverless-faqs/> [official], <https://docs.pingcap.com/tidbcloud/branch-overview> [official], <https://docs.pingcap.com/tidbcloud/vector-search-overview/> [official])
- Neon 은 serverless Postgres 에서 autoscaling, branching, instant restore, AI/embeddings 가이드를 공식 문서 첫 화면에 배치한다. 즉 "Postgres 그대로" 를 유지하면서 preview database branching 워크플로우에 가장 공격적인 포지셔닝이다. (출처: <https://neon.com/docs/introduction> [official])
- Turso/libSQL 은 branch-per-PR 과 embedded replica 가 핵심 차별점이다. Branch 는 별도 DB 인스턴스로 생성되고, embedded replicas 는 로컬 읽기, 원격 primary 쓰기, sync, read-your-writes semantics 를 제공해 offline/edge/mobile 시나리오에 유리하다. (출처: <https://docs.turso.tech/features/branching> [official], <https://docs.turso.tech/features/embedded-replicas/introduction> [official])

#### 12. AI-augmented backends (LLM integration patterns, RAG architectures)

- OpenAI 공식 패턴은 "모델 + tool calling + application-side execution loop" 다. 함수 호출 가이드는 도구 선언, 모델의 tool call 수신, 애플리케이션에서 실행, 결과를 다시 모델에 전달하는 5단계 루프를 명시한다. 이 패턴은 agent backend 와 LLM orchestration backend 의 기본 골격이다. (출처: <https://developers.openai.com/api/docs/guides/function-calling> [official])
- RAG 쪽은 직접 벡터 검색 파이프라인을 전부 구현하는 대신, Responses API 의 hosted `file search` / `vector stores` 를 써서 semantic + keyword retrieval 을 붙이는 managed retrieval 패턴이 공식화되어 있다. 즉 최신 흐름은 "앱에서 오케스트레이션, 검색은 managed tool, 도메인 데이터는 vector store" 조합이다. (출처: <https://platform.openai.com/docs/guides/tools-file-search?lang=javascript> [official], <https://developers.openai.com/api/docs/guides/function-calling> [official])

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `backend-edge` | 런북 | Hono + Workers + D1 + Durable Objects 조합 가이드 필요 | 중간 | backlog (신규) |
| `backend-ai-runtime` | 런북 | Tool calling / file search / vector store / agent backend 패턴 가이드 필요 | 높음 | backlog (신규) |

### 폐기 사유

없음.
