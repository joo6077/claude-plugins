# Backend System Principles

프로젝트 백엔드 아키텍처 세팅 시 참조하는 원칙 문서 매핑.

## 아키텍처 패턴

| 패턴 | 핵심 원칙 | 도입 기준 |
|------|-----------|-----------|
| Hexagonal (Ports & Adapters) | 도메인은 어댑터를 직접 import 하지 않고 port 인터페이스만 의존. 외부 시스템 교체 시 어댑터만 재작성. | 소~중 규모 앱. "technological churn 보험". [Hexagonal vs Clean vs Onion 2026](https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f) |
| Clean Architecture | Hexagonal + 의존성 규칙(inward-only) + 엔티티/유스케이스/인터페이스 어댑터/프레임워크 4계층 분리. | 중~대 규모, 명확한 레이어 네이밍이 필요할 때. [AWS Prescriptive Hexagonal](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html) |
| DDD (Domain-Driven Design) | 도메인 모델-persistence 모델 분리. Ubiquitous Language. Aggregate / Value Object / Bounded Context. | bounded context 2+ 또는 풍부한 비즈니스 규칙이 있을 때. 단순 CRUD엔 과도. [Vaadin DDD+Hexagonal](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture) |

**과복잡도 경고**: 위 패턴을 단순 CRUD 앱에 강요하지 마라. 비즈니스 규칙이 없는 CRUD는 "간소화 계층형 (Controller → Service → Repository)"이면 충분하다.

## 필수 카테고리

| 카테고리 | 참조 문서 | 핵심 원칙 |
|----------|-----------|-----------|
| API 규격 | ../../../../docs/backend/fundamentals/api-design.md | 리소스 명사, RFC 9110 메서드, RFC 9457 에러, OpenAPI 3.1 JSON Schema 호환 |
| 에러 처리 | ../../../../docs/backend/fundamentals/error-handling.md | Result 패턴, backoff+jitter, circuit breaker, RFC 9457 problem+json 통일 |
| 인증/인가 | ../../../../docs/backend/fundamentals/auth.md | OAuth 2.1 Authorization Code + PKCE 필수 (Implicit/ROPC 금지), RFC 9068 JWT profile, 고보안 시 DPoP(RFC 9449)/mTLS(RFC 8705) sender-constrained tokens. 출처: [RFC 9700 OAuth BCP](https://datatracker.ietf.org/doc/rfc9700/) |
| 보안 | ../../../../docs/backend/fundamentals/security.md | OWASP Top 10, 보안 헤더, PII 마스킹 |

## 선택 카테고리

| 카테고리 | 참조 문서 | 도입 기준 |
|----------|-----------|-----------|
| 캐싱 | ../../../../docs/backend/patterns/caching.md | 읽기 비율 높은 데이터 존재 시 |
| 이벤트 | ../../../../docs/backend/patterns/event-driven.md | 비동기 처리, 서비스 간 통신 필요 시. **AsyncAPI 3.0+** 스펙 + **Outbox relay(batch 200-500 + backpressure + checkpoint)** + idempotency. 출처: [microservices.io Outbox](https://microservices.io/patterns/data/transactional-outbox.html) |
| 테스트 | ../../../../docs/backend/fundamentals/testing.md | 항상 권장. **Pact v4 + Testcontainers** 계약 테스트를 기본 도입. 출처: [prgrmmng Pact+Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact) |
| API Lifecycle | ../../../../docs/backend/protocols/api-lifecycle.md | 외부 공개 API 시 |
