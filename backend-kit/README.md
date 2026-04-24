# backend-kit

스택 무관 백엔드 개발 가이드, 감사, 아키텍처 세팅 플러그인.

## 개요

백엔드 코드와 설계에 대해 원칙 기반 가이드를 제공하고, 체계적 감사를 수행하며, 프로젝트 아키텍처 기반을 세팅한다. 특정 프레임워크(Express, Django, Spring 등)에 종속되지 않는 범용 원칙을 다룬다.

## 스킬

| 스킬 | 용도 |
|------|------|
| `/backend-guide` | 백엔드 코드/설계에 대한 원칙 기반 가이드 (가벼운 리뷰) |
| `/backend-audit` | 백엔드 코드를 카테고리별 PASS/FAIL로 체계적 감사 |
| `/backend-system` | 프로젝트 백엔드 아키텍처 기반 세팅 (API 규격, 에러 처리 등) |
| `/backend-test` | 대상 파일/모듈 분석 후 테스트 코드 자동 생성 (pytest/jest/JUnit/go test 등 스택 무관) |

## 에이전트

| 에이전트 | 용도 |
|---------|------|
| `backend-reviewer` | backend-audit에서 호출하는 읽기 전용 독립 평가 에이전트 |

## 리서치 문서

`docs/backend/` 디렉토리에 12개 원칙 문서가 있으며, 모든 스킬이 이를 SSOT(Single Source of Truth)로 참조한다.

### Fundamentals
- **api-design** — REST 리소스 설계, HTTP 의미론, RFC 9457 에러, 페이지네이션
- **database** — 스키마 설계, 인덱스, EXPLAIN, N+1, connection pooling, migration
- **auth** — JWT/Session, OAuth 2.0/OIDC, RBAC/ABAC, 비밀번호 해싱, CORS/CSRF
- **error-handling** — Result 패턴, retry+backoff, circuit breaker, graceful degradation
- **testing** — 테스트 피라미드, contract testing, testcontainers, 부하 테스트
- **security** — OWASP Top 10, injection, XSS, 보안 헤더, PII 마스킹

### Patterns
- **caching** — 캐시 계층, cache-aside/write-through, stampede, Redis/Memcached
- **event-driven** — 메시지 큐 vs 스트리밍, outbox, saga, idempotency, CQRS

### Protocols
- **api-lifecycle** — 버저닝, deprecation/sunset, rate limiting, idempotency key
- **graphql** — 스키마 설계, DataLoader, demand control, federation, subscriptions
- **grpc** — proto 계약, streaming, deadline, 구조화 에러, 헬스체크
- **realtime** — WebSocket/SSE, 연결 관리, 수평 확장, 백프레셔

## 카이젠

- `/backend-research` — 외부 소스 크롤링으로 docs/backend/ 문서 갱신
- `/backend-kaizen` — 리서치 문서 기준으로 스킬 품질 점진 개선

## 검증

- `python3 scripts/run-evals.py backend-kit` — 7 스킬 assertion 전수 검증 (exit 0 = PASS, 1 = FAIL, 2 = 파싱 오류)
- `python3 scripts/validate-plugin.py backend-kit` — 7 카테고리 구조 감사 (refs/placeholders/code-fence 등)

## Phase 7 kaizen (2026-04-24)

- Phase 1~6 신규 원칙 전수 반영 (Binary Decidability · Rule-by-Rule Audit · Enumerate-before-Act · Cross-Surface Parity · CONDITIONAL APPROVE · L3 Coverage Honesty · 미검증 마커)
- 리서치 반영: OAuth 2.1 draft-15 · Transactional Outbox · Pact v4 + Testcontainers
- REJECT reason 해소: AR-03 · AR-04 · SK-07 · SK-13 · ER-01
