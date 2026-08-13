---
name: backend-audit
description: >
  백엔드 코드를 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  backend-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "백엔드 감사", "API 검수", "backend audit", "보안 감사" 같은 요청 시 트리거.
  디자인/UI 검사에는 트리거하지 않는다 — design-kit 사용.
argument-hint: "<target-path>"
user-invocable: true
---

# Gotchas

1. **디자인/UI 평가 금지** — UI 디자인 원칙은 평가하지 마라. 백엔드 원칙 준수 여부만 판정한다.
2. **스택 특정 린트 규칙 강제 금지** — ESLint/Pylint 규칙을 강제하지 마라. 아키텍처·보안·성능 원칙만 평가.
3. **N+1 탐지 시 ORM 코드 필수 확인** — 쿼리 패턴을 보지 않고 "N+1일 수 있다"는 추측성 FAIL 금지. 실제 코드에서 루프 내 쿼리를 확인해야 한다.
4. **보안 검사 생략 금지** — 코드가 "내부용"이어도 injection, 시크릿 노출, CORS 설정은 반드시 검사한다.
5. **PASS/FAIL 근거에 파일:라인 필수** — "Architecture FAIL — 의존 방향 위반"만으로는 사용자가 수정 위치를 알 수 없다. 반드시 `src/api/handler.rs:42`처럼 구체적 파일과 라인 번호를 포함해야 한다.
6. **리포트 카테고리 순서 변경 금지** — `audit-criteria.md`에 정의된 순서(Architecture → API Design → Database → Auth → Error → Security → Caching → Event-Driven → Testing → Observability)를 반드시 따른다. 순서를 바꾸면 이전 리포트와 비교가 불가능해진다.
7. **N/A 남발 금지** — 해당 없는 카테고리는 N/A로 표시하되, 프로젝트에 DB가 있는데 Database를 N/A로 처리하거나, 인증 코드가 있는데 Auth를 N/A로 처리하면 안 된다. 코드를 실제로 확인한 후에만 N/A를 판정하라.
8. **단일 파일 감사 시에도 아키텍처 컨텍스트 확인** — 파일 하나만 감사하더라도 해당 파일이 속한 레이어(domain/infra/api)와 의존 방향을 파악해야 정확한 판정이 가능하다. import 구문만 봐도 레이어 위반을 탐지할 수 있다.
9. **Binary Decidability Pre-Check (agent-design-guide §3.5 대응)** — 각 카테고리를 평가하기 전에 "이 기준은 코드에서 객관적으로 PASS/FAIL 판정 가능한가?"를 먼저 자문하라. "더 나을 것 같다"처럼 주관 해석 여지가 남는 기준은 **카테고리 평가 시작 시점에** 근거 제약(파일:라인 + 출처 URL)을 추가하여 이진 판정으로 재정식화한 뒤 평가한다. 예: "API Design 이 깔끔한지"가 아니라 "error response 가 `application/problem+json` Content-Type 을 반환하는지 (RFC 9457)"로 좁힌다.
10. **Rule-by-Rule Audit 프로토콜 (skill-design-guide §3.6 대응)** — `audit-criteria.md` 10 카테고리 × N 체크항목을 한 번에 묶어 "대체로 PASS/FAIL" 로 리포트하지 말고, 각 체크항목 단위로 개별 판정과 근거를 생성하라. 묶음 판정은 PASS 세부가 가려지고 FAIL 누락 추적이 불가능해진다. 리포트 표의 각 row 는 한 체크항목에 대응한다.
11. **미검증 항목 마커 프로토콜 (evaluator v3 대응)** — 런타임 환경/외부 시스템 접근 불가(예: production DB pool 설정·실제 Kafka broker 연결·OAuth provider 응답)로 L3 검증이 불가능한 항목은 **조용히 PASS 처리하지 말고** `[미검증]` 태그를 붙이고 근거에 이유를 기술하라 (예: `[미검증:ENV] production DB 접근 불가 — pool 설정 파일 정적 리뷰만 수행`). **정본 v5.0 기준 마커는 두 분류로 갈린다** — `UNVERIFIED_ENV`(구현자 통제 밖 · 남용 방지 4 요건 충족)와 `UNVERIFIED_INVALID_EVIDENCE`(4 요건 미충족 · 공허한 증거). 임계값 2 는 후자에만 적용되고 전자는 `env_gaps` 로 따로 센다 (Step 4 참조). 대상 미구현·의도적 미실행은 미검증이 아니라 FAIL 이다. 마커 의미·임계값·4 요건의 SSOT 는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이며, 복제본은 `backend-kit/agents/backend-reviewer.md` §Canonical Unverified-Evidence Protocol 이다 — 여기서 재정의하지 않는다.
12. **소비면을 안 보고 계약 카테고리를 PASS 처리하지 마라 (enforcement 등급 E2)** — API Design · 직렬화 · 이벤트 페이로드 · DB 스키마 rule 은 producer 파일만 읽고 판정하면 실제 통합 실패를 놓친다. 해당 응답을 역직렬화하는 소비면 코드(클라이언트 모델 · 리포지토리 · 생성 코드 · 테스트 픽스처)가 **같은 저장소 안에 있으면 반드시 열거해서 대조**하라. 열거 결과를 리포트에 남긴다 (문장 다짐 아님 — 등급 정의는 `harness/docs/guides/skill-design-guide.md` §3.7, 절차는 같은 문서 §5.5). **같은 저장소 안에 소비면이 있는데 안 본 것은 `[미검증]` 이 아니라 감사 누락이다** — `[미검증]` 은 검증 도구·환경 부재 전용이며, 소비면이 접근 불가한 별도 저장소에 있을 때만 `[미검증]` + 사유(저장소 접근 불가)로 처리한다.
13. **감지된 스택에 없는 기준을 FAIL 근거로 쓰지 마라** — Step 0 스택 감지 결과에 존재하지 않는 기술을 근거로 판정하면 오탐이다 (Go 프로젝트에 HikariCP 부재로 FAIL, Node 프로젝트에 Pydantic 부재로 FAIL, 셸/compose 작업에 언어 전용 안티패턴 적용). 스택에 **대응물이 있으면 그 스택의 등가물로 재정식화**하고(HikariCP → `database/sql` `SetMaxOpenConns` / PgBouncer), **대응물 자체가 없으면 N/A + 사유**로 처리한다. FAIL 이 아니다. 근거: 카이젠 입력 신호 `stack-inappropriate-rust-antipatterns` — insights 2026-07-27 §Phase 7/9 힌트에 "셸/compose 작업에 Rust 안티패턴 조건 오적용" 으로 기록된 실측 사례.
14. **쓰기 경로 무결성 rule 은 별도 SSOT 에서 가져온다** — Database · Testing 카테고리를 평가할 때 `audit-criteria.md` 만 읽고 끝내지 마라. 경합 가드 적합성 · upsert arbiter 정합 · 멱등 저장 계약 · 통합 타깃 증명 · 핵심 guard 음성 대조 5 개 rule 의 SSOT 는 `backend-kit/references/write-path-integrity-protocol.md` 다. 두 문서의 rule 집합은 **교집합이 없으므로** 어느 한쪽에만 있는 rule 을 누락하면 감사 누락이다. Step 3 표에서 두 출처의 rule 을 하나의 연속 번호로 열거한다.
15. **"트랜잭션으로 감싸라" 만으로 동시성 항목을 PASS 시키지 마라** — 트랜잭션 경계는 원자성을 주지 사전 조회 후 쓰기 경합을 막지 않는다. PASS 하려면 (a) 어떤 anomaly 를 막는지 (b) 어떤 DB primitive 가 담당하는지 **둘 다** 근거에 있어야 한다. invariant 분류 3 유형과 primitive 매핑은 `write-path-integrity-protocol.md` §1~§2 가 SSOT 다. 실측 근거: 2026-08-12 글로벌 REJECT `ER-02` (동시성 가드를 삭제해도 테스트가 통과).
16. **`audit-criteria.md` §8 "CDC 파이프라인" 행의 `exactly-once 보장 가능` 서술을 PASS 근거로 쓰지 마라** — outbox relay 는 중복 발행할 수 있으므로 outbox 또는 outbox+CDC 조합만으로 exactly-once 가 보장되지 않는다. 이 축의 판정 기준은 `write-path-integrity-protocol.md` §6 이며, consumer idempotency 가 함께 있어야 PASS 다. 출처: [microservices.io Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html).

# Process

## Step 0: 스택 감지 (backend-test Step 0 parity)

감사 기준을 적용하기 전에 대상 프로젝트의 스택을 먼저 확정한다. 이 결과가 없으면 Gotcha 13 위반(타 스택 고유 기준 오적용)을 판정할 수 없다.

| 감지 파일 | 스택 | 대응 확인 대상 예시 |
|-----------|------|--------------------|
| `requirements.txt` / `pyproject.toml` | Python | SQLAlchemy · Pydantic · asyncpg pool |
| `package.json` | Node.js | Prisma/Drizzle/TypeORM · Zod · pg-pool |
| `build.gradle` / `pom.xml` | Java/Kotlin | JPA · HikariCP · Bean Validation |
| `go.mod` | Go | GORM/sqlc · `database/sql` `SetMaxOpenConns` |
| `mix.exs` | Elixir | Ecto · DBConnection pool |
| `Cargo.toml` | Rust | → rust-audit 스킬로 리다이렉트 |

추가로 API 프레임워크 · 메시지 브로커 · 관측성 SDK 존재 여부를 확인하고, 감지되지 않은 영역의 카테고리는 N/A 후보로 표시한다 (Gotcha 7 의 "코드를 실제로 확인한 후에만 N/A" 와 함께 적용).

**DB 엔진도 함께 확정한다.** 마이그레이션 DDL · 드라이버 의존성 · 접속 문자열 중 하나로 판정한다. `write-path-integrity-protocol.md` §3 의 PostgreSQL 전용 rule(partial/expression unique index 와 `ON CONFLICT` 대상 대조)은 **PostgreSQL 이 감지됐을 때만** 적용하고, 다른 엔진이면 같은 절의 스택 무관 원칙만 적용한다. 엔진을 확정하지 못하면 그 rule 은 `[미검증]` + 사유(엔진 미확정)로 처리한다.

## Step 1: 대상 범위 결정

사용자가 지정한 경로를 기준으로 감사 대상을 결정한다:
- 파일 경로 → 해당 파일만
- 디렉토리 경로 → 하위 백엔드 관련 파일 전체
- 미지정 → 최근 변경된 백엔드 파일 (git diff 기준)

## Step 2: backend-reviewer 에이전트 호출

Agent 도구를 사용하여 backend-reviewer 서브에이전트를 생성한다:

- subagent_type: backend-reviewer
- prompt: "다음 파일을 백엔드 원칙 기준으로 평가하라: [대상 파일 목록]"

에이전트가 읽기 전용으로 분석 후 카테고리별 PASS/FAIL 결과를 반환한다.

## Step 3: 리포트 생성 (Rule-by-Rule 표)

카테고리 순서는 `references/audit-criteria.md` 섹션 순서와 일치시킨다 (총 10 카테고리). 각 row 는 **하나의 체크항목(rule)** 에 대응하며, 카테고리 단위로 묶지 않고 개별 판정·근거·출처를 생성한다 (Gotcha 10 참조). 표 자리표시자(`...`) 금지.

| # | 카테고리 | 체크항목 | 판정 | 근거(파일:라인) | 출처 URL |
|---|----------|---------|------|-----------------|----------|
| 1 | Architecture | 도메인-persistence 분리 | PASS/FAIL | `src/domain/user.py:1-40` 에 SQLAlchemy 애노테이션 없음 | [Vaadin DDD+Hexagonal](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture) |
| 2 | Architecture | Port/Adapter 경계 | PASS/FAIL | `src/infra/db.py:12` 가 domain 을 import / domain 은 infra 미참조 | [AWS Hexagonal](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html) |
| 3 | Architecture | Modular Monolith First | PASS/FAIL/WARN | `docker-compose.yml:1-30` 서비스 수 vs 팀 규모 명시 | [ByteIota 2026](https://byteiota.com/modular-monolith-42-ditch-microservices-in-2026/) |
| 4 | API Design | RFC 9457 problem+json | PASS/FAIL | `src/api/errors.py:8` Content-Type 확인 | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| 5 | API Design | OpenAPI 3.1 스펙 일치 | PASS/FAIL | `openapi.yaml:1` version + 실제 응답 정합 | [OpenAPI 3.1](https://swagger.io/specification/) |
| 6 | API Design | Pagination (cursor/keyset) | PASS/FAIL | `src/api/users.py:20` 쿼리 파라미터 | [Slack Pagination](https://slack.engineering/evolving-api-pagination-at-slack/) |
| 7 | API Design | 빈 상태 상태코드 일관성 | PASS/FAIL | `src/api/schedule.py:31` 빈 목록에 200 `[]` 반환 (404 아님) | [RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.html) |
| 8 | API Design | Timestamp 직렬화 규칙 | PASS/FAIL | `src/api/schema.py:12` 전 timestamp 필드 RFC 3339 `Z` 표기 | [RFC 3339 §4.3](https://www.rfc-editor.org/rfc/rfc3339) |
| 9 | API Design | 비멱등 write path idempotency | PASS/FAIL | `src/api/payment.py:44` 재시도 시 중복 생성 방지 경로 | [Idempotency-Key draft-07 (만료)](https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.html) |
| 10 | API Design | 소비면 정합성 (provider verification) | PASS/FAIL/`[미검증]` | `app/lib/data/model/schedule_model.dart:18` 이 200 빈 배열을 파싱 | [Pact](https://docs.pact.io/getting_started/what_is_pact_good_for) |
| 11 | Database | N+1 부재 | PASS/FAIL | `src/service/list.py:34` 루프 내 쿼리 없음 | PostgreSQL docs |
| 12 | Database | 인덱스 존재 | PASS/FAIL | `migrations/0003_add_idx.sql:1` WHERE 컬럼 커버 | PostgreSQL indexes |
| 13 | Database | 경합 가드 적합성 (invariant 분류) | PASS/FAIL | `src/service/order.py:88` 사전 SELECT 없이 `UPDATE ... WHERE status='pending'` + 영향 행 0 → conflict | [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) |
| 14 | Database | upsert arbiter 정합 (PostgreSQL 감지 시) | PASS/FAIL/N/A | `migrations/0007_fcm.sql:4` partial unique index predicate 와 `src/repo/fcm.py:31` 의 `ON CONFLICT` 대상 문자 일치 | [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html) |
| 15 | Database | 멱등 저장 계약 6 항목 | PASS/FAIL | `docs/contracts/payment.md:12-30` 에 key 범위·fingerprint·replay·in-flight·다른 payload·expiry 6 항 전부 기재 | [Stripe Idempotent requests](https://docs.stripe.com/api/idempotent_requests) |
| 16 | Auth | Authorization Code + PKCE | PASS/FAIL | `src/auth/oauth.py:15` PKCE 구현 | [RFC 9700](https://datatracker.ietf.org/doc/rfc9700/) |
| 17 | Auth | Deprecated grant 금지 | PASS/FAIL | Implicit/ROPC 코드 부재 (OAuth 2.1 draft-15 제거) | [OAuth 2.1 draft-15](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) |
| 18 | Error | 글로벌 핸들러 + problem+json | PASS/FAIL | `src/api/error_handler.py:10` | [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) |
| 19 | Error | Circuit Breaker + Rate Limiter 조합 | PASS/FAIL | `src/infra/resilience.py:1` 3-state CB + RL 공존 | [Azure CB](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) |
| 20 | Security | Injection 방어 (파라미터화) | PASS/FAIL | `src/repo/*.py` raw SQL 부재 | OWASP Top 10 |
| 21 | Security | 시크릿 관리 | PASS/FAIL | `.env.example` + repo 하드코딩 0 건 | OWASP |
| 22 | Caching | TTL 존재 | PASS/FAIL | `src/cache/*.py:SET_EX` 확인 | Redis docs |
| 23 | Event-Driven | Transactional Outbox | PASS/FAIL | `migrations/000N_outbox.sql:1` + relay 존재 | [microservices.io Outbox](https://microservices.io/patterns/data/transactional-outbox.html) |
| 24 | Event-Driven | Consumer Idempotency | PASS/FAIL | `src/consumer/*.py` dedupe key 처리 | Stripe Idempotency |
| 25 | Testing | Pact v4 + Testcontainers | PASS/FAIL | `tests/contract/*.py` + `docker-compose.test.yml` | [Pact+Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact) |
| 26 | Testing | 통합 테스트가 실제 의존성 사용 | PASS/FAIL | `tests/integration/test_user.py:9` Testcontainers Postgres (MockDatabase 아님) | [Testcontainers](https://testcontainers.com/getting-started/) |
| 27 | Testing | 통합 테스트 전 마이그레이션 적용 | PASS/FAIL | `tests/conftest.py:22` 컨테이너 기동 후 migration 실행 | [Testcontainers](https://testcontainers.com/getting-started/) |
| 28 | Testing | 통합 타깃 증명 (결합) | PASS/FAIL | `tests/integration/test_order.py:14` 가 `src/service/order.py:place_order` 를 직접 호출 (SQL 독립 재작성 아님) | [Pact Provider verification](https://docs.pact.io/provider) |
| 29 | Testing | 핵심 guard 음성 대조 | PASS/FAIL | 가드 술어 제거 시 `tests/integration/test_order.py::test_stale_update` 가 FAIL 함을 확인 | [PIT Mutation testing](https://pitest.org/) |
| 30 | Observability | OTel 3 Signals 통합 | PASS/FAIL | `src/telemetry.py:1` traces+metrics+logs OTLP exporter | [OTel Status](https://opentelemetry.io/docs/specs/status/) |
| 31 | Observability | PII 마스킹 | PASS/FAIL | `src/logging.py:filter` 에 이메일/IP 마스킹 | OWASP Logging |

위 표는 대표 rule 예시이며, 실제 리포트는 `audit-criteria.md` 와 `backend-kit/references/write-path-integrity-protocol.md` **두 출처의 모든 기준 rule** 을 빠짐없이 열거해야 한다 (Rule-by-Rule Audit · Gotcha 10 · Gotcha 14).

## Step 4: 최종 판정

판정 분류는 세 가지다:

카운터는 두 개이며 **합산하지 않는다** (정본 조항 3): `UNVERIFIED_INVALID_EVIDENCE`(임계 판정용)와 `env_gaps`(= `UNVERIFIED_ENV`, 커버리지 게이트용).

- **APPROVE** — 전 카테고리 PASS + `UNVERIFIED_INVALID_EVIDENCE` 0 건.
- **CONDITIONAL APPROVE** — 전 카테고리 PASS 이지만 `UNVERIFIED_INVALID_EVIDENCE` 1 건 존재. 리포트에 "미검증 1 건: [체크항목] — [이유]" 를 명시하고 환경 개선(예: production DB 접근권한 · Docker 설치) 후 재검증 권고.
- **REJECT** — 1 건 이상 FAIL 또는 `UNVERIFIED_INVALID_EVIDENCE` 2 건 이상. 각 FAIL 에 대해 구체적 개선 액션(파일:라인 + 권장 변경 + 출처) 을 함께 제시한다.
- **BLOCKED** — `(총 rule 수 − env_gaps) / 총 rule 수 < 0.60`. 판정 자체를 내지 않고 환경 부재 목록과 재검증 명령을 보고한다.

`env_gaps` 로 세려면 남용 방지 4 요건을 모두 채워야 한다 (`backend-reviewer.md` §`UNVERIFIED_ENV` 남용 방지 4 요건). 못 채운 주장은 `UNVERIFIED_INVALID_EVIDENCE` 로 강등된다.

# References

- references/audit-criteria.md — 10 카테고리 기존 rule 의 PASS/FAIL 체크리스트
- ../../references/write-path-integrity-protocol.md — 쓰기 경로 무결성 rule (경합 가드 적합성 · upsert arbiter · 멱등 저장 계약 · 통합 타깃 증명 · guard 음성 대조) SSOT
