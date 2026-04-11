# Sprint Contract — Phase 7 Kaizen Research Mode (backend-kit)

Feature: backend-kit 3 스킬 + backend-reviewer 에이전트 + references 2026 최신 백엔드 아키텍처 트렌드 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1~6 완료 (commit 4587154 → 20a8415). Phase 7은 backend-kit 플러그인의 3개 스킬(backend-guide, backend-audit, backend-system), `agents/backend-reviewer.md`, 관련 `skills/*/references/**` 파일을 2026 최신 백엔드 아키텍처 생태계에 맞춰 갱신한다.

데이터 풀 §1에는 backend-kit 스킬/에이전트에 직접 귀속된 REJECT 피드백은 없다 (claude-plugins 레포 72 feedback 중 backend-kit 관련 0건 — react/design/evaluator 중심). 따라서 Phase 7은 **예방적 + 2026 트렌드 반영** 중심이다.

데이터 풀 §5 validate-plugin 스냅샷 — backend-kit v0.1.0, 3 skills + 1 agent, V1~V7 전부 OK. 회귀 금지 기준선.

외부 리서치 (WebSearch, 2026-04-11):

- **Hexagonal / Clean / DDD 2026 실무 패턴**: "insurance policy against technological churn" — Hexagonal이 small-mid 앱에 sweet spot. Clean은 Hexagonal에 추가 규칙·명명을 더한 것. DDD는 도메인 모델과 persistence 모델 분리 필수 (단일 엔티티 금지). 작은 CRUD 앱엔 over-engineering 경고. 하지만 2+ bounded context가 있거나 비즈니스 규칙이 풍부하면 Hexagonal+DDD 조합이 현재도 기본값. ([Hexagonal vs Clean vs Onion 2026](https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f), [AWS Prescriptive Hexagonal](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html), [Vaadin DDD+Hexagonal](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture))

- **REST / GraphQL / gRPC 하이브리드 전략 2026**: binary choice는 false dichotomy — 3개 프로토콜을 boundary 기준 병용이 모범. Netflix/Shopify 사례. gRPC 5-10x 내부 서비스 throughput, Protobuf 3-10x JSON 대비, HTTP/2 multiplexing. **REST**: public API + 단순 CRUD, **GraphQL**: 다중 클라이언트(mobile/web/3rd) 다른 데이터 요구, **gRPC**: internal service-to-service 성능/지연 critical. 2026 기준 엔터프라이즈 50%+ GraphQL 프로덕션 사용. ([Java Code Geeks 2026 decision](https://www.javacodegeeks.com/2026/02/graphql-vs-rest-vs-grpc-the-2026-api-architecture-decision.html), [Fordel 2026 framework](https://fordelstudios.com/research/graphql-rest-grpc-2026-decision-framework), [DEV pockit 2026](https://dev.to/pockit_tools/rest-vs-graphql-vs-trpc-vs-grpc-in-2026-the-definitive-guide-to-choosing-your-api-layer-1j8m))

- **OpenAPI 3.1 / AsyncAPI 3**: OpenAPI 3.1은 JSON Schema 완전 호환 (3.0 대비 주요 변화). AsyncAPI 3.0/3.1은 이벤트 기반 API 계약 표준 — REST에서 OpenAPI가 차지하는 위치를 이벤트 기반 시스템에서 담당. 3.1.0은 minor/non-breaking, ROS 2 binding 추가, AND logic security, discriminator 확장. ([OpenAPI 3.1 Swagger](https://swagger.io/specification/), [AsyncAPI 3.1 release notes](https://www.asyncapi.com/blog/release-notes-3.1.0), [AsyncAPI 3.0.0 spec](https://www.asyncapi.com/docs/reference/specification/v3.0.0))

- **RFC 9457 Problem Details**: RFC 7807 obsolete, 5개 표준 필드(type/title/status/detail/instance) + extensions + **common problem type registry** 신규. 2026 기준 Stripe/GitHub/Cloudflare 등 대형 API 표준 채택. 하위 호환. ([RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), [Swagger RFC 9457](https://swagger.io/blog/problem-details-rfc9457-doing-api-errors-well/), [Redocly RFC 9457](https://redocly.com/blog/problem-details-9457))

- **OAuth 2.1 / RFC 9700 / DPoP / mTLS**: **RFC 9700 (2025-01)**이 OAuth 2.0 Security BCP 최신판. Implicit grant / ROPC **deprecated** (OAuth 2.1 draft에서 제외). **Authorization Code + PKCE** 가 public client 기본값. JWT access token은 **RFC 9068** profile 권장. **Sender-constrained tokens** — DPoP (RFC 9449) 또는 mTLS binding. FAPI 2.0 Security Profile은 둘 중 하나 mandate. DPoP는 asymmetric JWT 기반, mTLS는 X.509 cert 기반. 2026 권장은 DPoP (PKI 불필요, 앱 레이어). ([RFC 9700](https://datatracker.ietf.org/doc/rfc9700/), [WorkOS OAuth BCP](https://workos.com/blog/oauth-best-practices), [Auth0 DPoP](https://auth0.com/blog/protect-your-access-tokens-with-dpop/), [Kong DPoP](https://konghq.com/blog/engineering/demonstrating-proof-of-possession-dpop-preventing-illegal-access-of-apis))

- **CQRS / Outbox / Event Sourcing 2026**: Transactional Outbox는 dual-write 문제의 표준 해법. 2026 권장 실무: batch read(200–500 rows) + backpressure(windowed concurrency) + checkpoint commit on success, idempotency(dedupe keys) + per-aggregate sequence + PublishedAt/Attempts + exponential backoff + DLQ. CQRS 는 read/write 모델 분리로 독립 스케일링. Event Sourcing은 tooling cost 주의 (over-engineering 경고 유지). ([microservices.io Outbox](https://microservices.io/patterns/data/transactional-outbox.html), [Azure Cosmos Outbox](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos), [Azure CQRS](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs), [Solace EDA patterns](https://solace.com/event-driven-architecture-patterns/))

- **Contract Testing 2026 — Pact + Testcontainers**: 2026 권장은 Pact(consumer-driven) + Testcontainers(ephemeral broker/dependencies). Pact v4.0.0은 GraphQL 지원 + async message 개선 + MatchersV2. Integration test 시간 최대 60% 단축. 시작 방법: consumer tests 먼저 → provider verification 추가 → CI/CD 통합. ([prgrmmng Pact+Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact), [testsprite 2026 tools](https://www.testsprite.com/use-cases/en/the-best-contract-testing-tools), [Microsoft ISE Pact](https://devblogs.microsoft.com/ise/pact-contract-testing-because-not-everything-needs-full-integration-tests/))

## Scope

### 수정 대상

- `backend-kit/skills/backend-guide/SKILL.md`
- `backend-kit/skills/backend-audit/SKILL.md`
- `backend-kit/skills/backend-system/SKILL.md`
- `backend-kit/agents/backend-reviewer.md`
- `backend-kit/skills/backend-guide/references/principle-index.md`
- `backend-kit/skills/backend-audit/references/audit-criteria.md`
- `backend-kit/skills/backend-system/references/system-principles.md`

### 수정 금지 (Phase 1~6 파일 / 범위 외)

- `harness/**` (Phase 1~4)
- `flutter-toolkit/**` (Phase 5)
- `design-kit/**` (Phase 6)
- `docs/backend/**` — 범위 외 (docs 갱신은 `/backend-research` 스킬 영역)
- `backend-kit/.claude-plugin/plugin.json` — 버전 bump는 Final Phase에서
- `.harness/` 파일 (`.harness/sprint-contract.md` 외)
- `.harness/.meta/kaizen-data-pool.md` 수정 금지

## Goal

데이터 풀 (직접 REJECT 없음)을 감안하여 2026 백엔드 트렌드(Hexagonal/Clean/DDD, 하이브리드 API, OpenAPI 3.1/AsyncAPI 3, RFC 9457, OAuth 2.1/RFC 9700, DPoP/mTLS, Outbox+CQRS 2026 실무 패턴, Pact+Testcontainers)를 backend-kit 3 스킬 + backend-reviewer 에이전트 + 3 references에 반영한다. 계약 기준 완료 조건을 모두 충족하고 validate-plugin 7 OK / markdownlint 주요 규칙 / bare fence 0건을 유지해야 한다.

## 완료 조건

### AR: Architecture 카테고리 신설 (Hexagonal/Clean/DDD)

- [ ] **AR-01**: `backend-guide/SKILL.md` Step 1 카테고리 표에 `architecture` 행 1개 추가 — 키워드 최소 3개(예: `hexagonal`, `clean`, `DDD`, `ports`, `adapter`, `도메인`, `bounded context` 중 3개 이상). 기존 12개 카테고리 유지.
- [ ] **AR-02**: `backend-audit/SKILL.md` 또는 `backend-reviewer.md` 평가 카테고리 목록에 `Architecture` 카테고리 1개 추가 (신규 카테고리). 기존 8개 카테고리 유지 + Architecture 포함 9개. 순서는 Architecture를 1번 또는 마지막 중 택1.
- [ ] **AR-03**: `backend-audit/references/audit-criteria.md`에 `## N. Architecture` 섹션 신설 — 최소 3개 기준 표(예: "도메인 모델-persistence 분리", "Port/Adapter 경계", "의존성 방향 inward only") + 각 PASS 조건 + 출처. 출처 URL 최소 2개 (Hexagonal/DDD 관련).
- [ ] **AR-04**: `backend-system/SKILL.md` Step 2 카테고리 표에 `아키텍처 패턴` 행 1개 추가 — "Hexagonal/Clean/DDD 중 프로젝트 규모에 맞게 선택. 단순 CRUD는 과도 경고". 필수/선택 표시 및 산출물 명시.
- [ ] **AR-05**: `backend-system/references/system-principles.md`에 `## 아키텍처 패턴` 섹션 1개 추가 — Hexagonal/Clean/DDD 3패턴 요약 + 도입 기준(bounded context 2+ 또는 복잡 도메인 규칙). 출처 URL 최소 1개.
- [ ] **AR-06**: `backend-guide/references/principle-index.md`에 `Architecture` 카테고리 행 1개 추가 — 문서 경로는 `docs/backend/fundamentals/` 하위 또는 `docs/backend/patterns/` 중 적절한 기존 문서 경로. docs 신규 파일 생성 금지 (docs는 Phase 범위 외) — 기존 경로 중 가장 근접한 것을 연결하거나 TBD 주석 허용.

### AP: API 하이브리드 전략 + OpenAPI 3.1 / AsyncAPI 3

- [ ] **AP-01**: `backend-guide/SKILL.md` Gotchas 섹션에 **하이브리드 API 전략** Gotcha 1개 추가 — "REST/GraphQL/gRPC는 boundary 기준 병용. 단일 선택 강요 금지. public API는 REST, 다중 클라이언트 쿼리는 GraphQL, internal 성능 critical은 gRPC" 요지. 출처 URL 1개.
- [ ] **AP-02**: `backend-audit/references/audit-criteria.md` `## 1. API Design` 표에 **OpenAPI 3.1 JSON Schema 호환** 기준 1줄 또는 **하이브리드 API 경계 선택** 기준 1줄 추가. 출처 URL 1개.
- [ ] **AP-03**: `backend-audit/references/audit-criteria.md` `## 7. Event-Driven` 표에 **AsyncAPI 3.x 스펙** 기준 1줄 추가 — "이벤트 API는 AsyncAPI 3.0+ 스펙 + bindings 정의". 출처 URL 1개 (asyncapi.com).

### SE: Security — RFC 9700 / OAuth 2.1 / DPoP / mTLS

- [ ] **SE-01**: `backend-audit/references/audit-criteria.md` `## 3. Authentication & Authorization` 표에 **RFC 9700 / OAuth 2.1 BCP** 기준 최소 2개 추가 — Implicit/ROPC deprecated, Authorization Code + PKCE 필수. 출처 URL 1개 (RFC 9700).
- [ ] **SE-02**: `backend-audit/references/audit-criteria.md` Auth 섹션 또는 Security 섹션에 **Sender-constrained tokens (DPoP RFC 9449 / mTLS)** 기준 1줄 추가 — "FAPI 2.0 / 고보안 환경은 DPoP 또는 mTLS binding". 출처 URL 1개.
- [ ] **SE-03**: `backend-system/references/system-principles.md` 인증/인가 섹션 또는 신규 항목에 **OAuth 2.1 + PKCE + DPoP/mTLS** 원칙 1줄 추가. 출처 URL 1개.
- [ ] **SE-04**: `backend-guide/SKILL.md` Step 1 카테고리 표 `auth` 행 키워드에 `PKCE` 또는 `DPoP` 1개 추가 (기존 키워드 유지).

### ED: Event-Driven 2026 실무 패턴 강화

- [ ] **ED-01**: `backend-audit/references/audit-criteria.md` `## 7. Event-Driven` 표에 **Outbox relay batch+backpressure** 기준 1줄 추가 — "outbox relay는 200-500 rows batch + windowed concurrency + checkpoint commit on success". 출처 URL 1개 (microservices.io 또는 Azure Cosmos outbox).
- [ ] **ED-02**: `backend-audit/references/audit-criteria.md` Event-Driven 표에 **per-aggregate sequence + PublishedAt/Attempts + exponential backoff + DLQ** 요지 1줄 추가 (1줄 또는 분리). 출처 URL 1개.
- [ ] **ED-03**: `backend-guide/SKILL.md` Step 1 카테고리 표 `event-driven` 행 키워드에 `CQRS` 추가 (기존 키워드 유지). CQRS는 이미 없다면 추가.

### TE: Testing — Pact + Testcontainers 2026

- [ ] **TE-01**: `backend-audit/references/audit-criteria.md` `## 8. Testing` 표에 **Pact 컨슈머 드리븐 계약 테스트** 기준 1줄 추가 또는 기존 `Mock 정합성` 행을 `Contract test (Pact v4+) — consumer-driven, GraphQL/async 지원` 맥락으로 확장. 출처 URL 1개.
- [ ] **TE-02**: `backend-system/references/system-principles.md` 테스트 행 원칙에 `Pact + Testcontainers` 맥락 1줄 추가 또는 섹션 확장. 출처 URL 1개.

### RV: backend-reviewer 에이전트 갱신

- [ ] **RV-01**: `backend-reviewer.md` 핵심 규칙 또는 평가 기준 참조 섹션에 "audit-criteria.md가 유일한 진실원천"이라는 기존 문장 유지 + **Architecture 카테고리 추가**를 반영 (AR-02 변경과 sync).
- [ ] **RV-02**: `backend-reviewer.md` 출력 포맷 예시 표에 Architecture 행이 자연스럽게 포함 가능하도록 컬럼/예시 유지 또는 보강 (이미 일반 컬럼이면 추가 변경 불필요 — self-audit 명시).

### QO: 과복잡도 경고 (Anti-over-engineering)

- [ ] **QO-01**: `backend-system/SKILL.md` Gotcha #4 (과도한 복잡도 경고)에 **Hexagonal/Clean/DDD/CQRS/Event Sourcing** 구체 키워드 명시 추가. 기존 "CQRS, 이벤트 소싱, 마이크로서비스" 문구 유지 + "Hexagonal/Clean/DDD도 단순 CRUD 앱에 강요 금지. bounded context 2+ 또는 풍부한 비즈니스 규칙 있을 때만 권장"이라는 맥락 1문장 추가. 출처 URL 1개.

### I: 인프라 / 품질 게이트

- [ ] **I-01**: `python3 scripts/validate-plugin.py backend-kit` → V1~V7 전부 OK.
- [ ] **I-02**: `python3 scripts/validate-plugin.py` (전체 7 킷) → Total 7 OK, Exit 0. 회귀 금지.
- [ ] **I-03**: `python scripts/sync-docs.py --check-only` → backend-kit 영역 "모두 최신 상태" 또는 sync 필요 없음. 필요 시 sync 후 재실행하여 통과.
- [ ] **I-04**: bare code fence 0건 (V6 code-fence OK로 검증) — 새로 추가하는 모든 fenced block은 반드시 언어 힌트 명시 (`bash`, `json`, `text`, `markdown`, `yaml` 등).
- [ ] **I-05**: 변경된 파일들에 MD031/MD032/MD060/MD028/MD034/MD033 markdownlint 규칙 위반 0건 — 수정 영역 주변 context 기준.
- [ ] **I-06**: git working tree modified 파일이 위 Scope 외로 벗어나지 않는다. `scripts/__pycache__/`, `.harness/sprint-contract.md` 등은 허용. `.harness/.meta/kaizen-data-pool.md`는 수정 금지.
- [ ] **I-07**: git commit 메시지 prefix `kaizen(phase7-research):` 형식 + 한국어 본문. commit hash 리포트에 기재.
- [ ] **I-08**: 브랜치 유지 — `kaizen/2026-04-11-research`, push 금지.

### TR: Trace / 출처 / 2026 트렌드

- [ ] **TR-01**: 새로 추가된 출처 URL 최소 **6개 이상** (Hexagonal/Clean/DDD 1 + 하이브리드 API 1 + OpenAPI 3.1 1 + AsyncAPI 3 1 + RFC 9700 또는 DPoP 1 + Outbox 또는 CQRS 1 + Pact 또는 Testcontainers 1). 중복 URL은 1회만 카운트, 최소 6개 순증 기준.
- [ ] **TR-02**: `backend-kit` 파일 변경을 한번이라도 touching한 파일 내에 해당 출처 URL이 실제 인용되어 있어야 한다 (단순 sprint-contract.md 인용은 카운트하지 않는다).
- [ ] **TR-03**: 리포트에 리서치 출처 URL 목록 (최소 6개) 명시.

## Rollback

Self-audit FAIL 3회 연속 또는 validate-plugin 회귀 발생 시 `git checkout -- backend-kit/` 로 롤백. commit 전이면 working tree만 버리면 된다.

## Notes

- `docs/backend/**`는 이번 Phase 범위 외 — 해당 갱신은 별도 `/backend-research` Phase 책임. 이번 Phase는 스킬/에이전트/references 레벨 갱신만.
- AR-06은 docs 파일 신규 생성 금지 조건이라 "TBD 주석 허용"으로 완화 — 기존 경로 중 근접한 것에 연결하거나 후속 backend-research 대기 주석이 허용된다.
- RFC 9700 자체 URL은 DPoP(RFC 9449)와 별개이므로 둘 다 쓰면 TR-01 카운트 증가.
- 과복잡도 경고(QO-01)는 2026 리서치에서도 반복 강조된 안티패턴 — 단순 CRUD 강제 적용 방지를 위해 반드시 추가한다.
- backend-kit은 현재 3 스킬 + 1 agent로 단순한 구조 — over-sprawl 없이 최소 침습적으로 수정하여 validate-plugin V1~V7을 유지한다.
