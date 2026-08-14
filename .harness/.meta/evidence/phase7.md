---
phase: 7
title: "Phase 7 backend-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

출처 유형: WebSearch fallback

**1. 관찰 사실**

**H1 — read-check-then-write 경합은 SQL/DB 레벨 분류로 다뤄야 한다.**  
PostgreSQL `READ COMMITTED`에서 `UPDATE`/`DELETE`/`SELECT FOR UPDATE`는 동시 갱신자가 있으면 기다린 뒤 `WHERE` 조건을 갱신된 row에 다시 평가한다. 따라서 `UPDATE ... WHERE col = $expected` 같은 조건부 갱신은 같은 row의 낙관적 동시성 가드로 성립한다. 출처: https://www.postgresql.org/docs/current/transaction-iso.html ([postgresql.org](https://www.postgresql.org/docs/current/transaction-iso.html))

추론: `UPDATE ... WHERE EXISTS (...)`로 사전 read-check를 쓰기 SQL 안에 넣은 것은 “앱 레벨 TOCTOU”를 “단일 SQL statement의 predicate 평가”로 내리는 패턴이다. 다만 PostgreSQL 문서도 `READ COMMITTED`에서 복잡한 search condition은 일관성에 부적합할 수 있다고 경고하므로, cross-row/predicate invariant는 조건부 UPDATE만으로 충분하다고 일반화하면 안 된다. 출처: https://www.postgresql.org/docs/current/transaction-iso.html ([postgresql.org](https://www.postgresql.org/docs/current/transaction-iso.html))

`SELECT FOR UPDATE`는 반환된 기존 row를 잠가 다른 writer/locker를 막지만, “존재하지 않는 row”나 predicate 전체를 자동으로 잠그는 해법은 아니다. 출처: https://www.postgresql.org/docs/current/explicit-locking.html ([postgresql.org](https://www.postgresql.org/docs/current/explicit-locking.html))

격리수준 분류는 dirty read / nonrepeatable read / phantom read / serialization anomaly 기준으로 확립되어 있고, PostgreSQL에서 `Serializable`만 serialization anomaly를 막는다. 출처: https://www.postgresql.org/docs/current/transaction-iso.html ([postgresql.org](https://www.postgresql.org/docs/current/transaction-iso.html)) Berenson et al.은 Snapshot Isolation에서 write skew(A5B)가 가능하다고 분류한다. 출처: https://sigmodrecord.org/1995/06/06/a-critique-of-ansi-sql-isolation-levels/ ([sigmodrecord.org](https://sigmodrecord.org/?download_id=8550&smd_process_download=1))

**H2 — partial/expression unique index와 `ON CONFLICT` 대상 불일치는 실제 upsert 함정이다.**  
PostgreSQL partial index는 predicate를 만족하는 subset에만 적용되고, query 조건이 index predicate를 수학적으로 함의한다고 planner가 인식해야 한다. 문서상 일반 정리 증명기는 없고, 많은 경우 predicate가 query `WHERE`에 정확히 맞아야 하며 parameterized clause는 partial index와 맞지 않을 수 있다. 출처: https://www.postgresql.org/docs/current/indexes-partial.html ([postgresql.org](https://www.postgresql.org/docs/current/indexes-partial.html))

`ON CONFLICT`의 unique index inference는 column/expression과 선택적 `index_predicate`가 arbiter index를 만족해야 한다. inference 실패 시 에러가 나며, `DO UPDATE`는 conflict target이 필수다. partial unique index는 `ON CONFLICT (cols) WHERE predicate ...`처럼 predicate까지 맞춰야 의도한 arbiter로 잡힌다. 출처: https://www.postgresql.org/docs/current/sql-insert.html ([postgresql.org](https://www.postgresql.org/docs/current/sql-insert.html))

idempotent write 규약은 “같은 key + 같은 payload 재시도는 원 결과 반환, 진행 중 중복은 conflict, 다른 payload 재사용은 오류, key expiry 문서화”다. IETF Idempotency-Key 문서는 2026-04-18 만료된 Internet-Draft이므로 표준이라고 쓰면 안 되지만, 상태코드 규약 근거로는 유용하다. 출처: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ ([datatracker.ietf.org](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)) Stripe도 POST 재시도 중복 생성을 막기 위해 idempotency key, 결과 저장, payload 비교, 24h pruning을 문서화한다. 출처: https://docs.stripe.com/api/idempotent_requests ([docs.stripe.com](https://docs.stripe.com/api/idempotent_requests))

**H3 — 통합 테스트는 실제 대상 코드 경로를 통과한다는 증거가 필요하다.**  
Testcontainers는 테스트가 production과 같은 실제 서비스에 의존하고 mock/in-memory 서비스를 피하도록 설계됐다. in-memory/fake는 production 기능과 동작이 다를 수 있다고 명시한다. 출처: https://testcontainers.com/getting-started/ ([testcontainers.com](https://testcontainers.com/getting-started/))

Pact provider verification은 pact 요청을 locally running provider에 replay하고 실제 응답을 expected response와 비교한다. 또한 request body를 추출·검증하기 전 레이어를 stub하면 “아무 garbage body도 통과”할 수 있다고 경고한다. 출처: https://docs.pact.io/provider ([docs.pact.io](https://docs.pact.io/provider)) Pact CLI도 running provider에 요청을 보내 mismatch를 보고하는 단일 실행 바이너리를 제공한다. 출처: https://docs.pact.io/implementation_guides/cli/pact-verifier ([docs.pact.io](https://docs.pact.io/implementation_guides/cli/pact-verifier))

mutation testing 관점에서는 코드에 fault를 주입했는데 테스트가 통과하면 mutation이 살아남은 것이며, 테스트가 의미 있게 결함을 잡지 못한다는 신호다. 출처: https://pitest.org/ ([pitest.org](https://pitest.org/))

**2. 권장안**

backend-kit에 넣을 조항:

- **Database / Concurrency Guard Fit**: write path가 사전 조회 후 쓰기이면 FAIL 후보로 보고, invariant를 먼저 분류한다. 같은 row의 상태 전이는 조건부 `UPDATE ... WHERE expected_state/version` 또는 동등한 compare-and-swap로 판정한다. 존재/권한/가시성 predicate는 가능한 경우 쓰기 SQL의 `WHERE EXISTS`로 넣는다. cross-row, absence, aggregate invariant는 unique/exclusion/partial unique constraint, 명시적 lock, 또는 `Serializable + retry(SQLSTATE 40001 상당)` 중 하나가 있어야 PASS.
- **No Generic “Use Transactions” Advice**: “트랜잭션으로 감싸라”만으로는 PASS 금지. 어떤 anomaly를 막는지, 어떤 DB primitive가 담당하는지 적어야 한다.
- **Postgres Upsert Arbiter Check**: PostgreSQL이 감지되면 partial/expression unique index의 정의와 모든 `ON CONFLICT` target을 대조한다. column/expression/predicate가 맞지 않으면 FAIL. `ON CONFLICT DO NOTHING` target 생략은 “모든 usable constraint 회피”라서 의도한 idempotency 결과 반환을 보장하지 않으면 WARN/FAIL.
- **Idempotent Write Contract**: 비멱등 write는 idempotency scope를 문서화한다. key/natural key 범위, payload fingerprint, replay response, in-flight duplicate, different-payload reuse, expiry를 계약에 적어야 PASS.
- **Integration Target Proof**: 통합 테스트는 production handler/repository/binary 또는 locally running provider를 호출한다는 증거가 있어야 PASS. 독립 재작성 SQL로 정상 동작만 확인한 테스트는 integration이 아니라 query-level/unit 보조 테스트로 분류한다.
- **Negative Control / Mutation Guard**: 동시성 가드, auth guard, idempotency arbiter 같은 핵심 guard는 제거/무력화 mutation 또는 동등한 negative control에서 테스트가 실패해야 PASS. 실행 못 했으면 `[미검증]`이 아니라 “guard proof 없음”으로 FAIL 후보.
- **Contract Surface**: HTTP 계약은 OpenAPI 3.1.x로, async/message 계약은 AsyncAPI 3.0으로 표면을 문서화한다. AsyncAPI는 sender 문서에서 receiver 문서를 파생하지 말라고 하므로 producer/consumer 문서를 따로 확인한다. 출처: https://spec.openapis.org/oas/v3.1.1.html ([spec.openapis.org](https://spec.openapis.org/oas/v3.1.1.html)), https://www.asyncapi.com/docs/reference/specification/v3.0.0 ([asyncapi.com](https://www.asyncapi.com/docs/reference/specification/v3.0.0))
- **Outbox Idempotency Link**: outbox를 쓰는 write path는 DB update와 outbox insert가 같은 트랜잭션이어야 하고, relay 중복 발행 가능성 때문에 consumer idempotency를 같이 요구한다. 출처: https://microservices.io/patterns/data/transactional-outbox.html ([microservices.io](https://microservices.io/patterns/data/transactional-outbox.html))

넣지 말 것:

- backend-kit에 PostgreSQL 전용 SQL 문법을 필수 구현으로 박지 말 것. 원칙은 스택 무관, PostgreSQL 세부 rule은 “PostgreSQL 감지 시” 감사 항목으로 둔다.
- `Serializable`을 전 write path 기본값으로 강제하지 말 것. retry 비용과 abort율이 있다.
- `SELECT FOR UPDATE`를 모든 TOCTOU의 해법으로 제시하지 말 것. 기존 row lock용이다.
- Testcontainers/Pact를 모든 테스트에 강제하지 말 것. 단위 테스트에는 과하다.
- 만료된 Idempotency-Key draft를 RFC/표준으로 부르지 말 것.
- OAuth 2.0 BCP(RFC 9700)는 이번 H1~H3의 직접 근거가 아니다. auth baseline 유지 근거로만 둔다. 출처: https://datatracker.ietf.org/doc/rfc9700/ ([datatracker.ietf.org](https://datatracker.ietf.org/doc/rfc9700/))

**3. 트레이드오프**

조건부 UPDATE/`WHERE EXISTS`는 단순하고 빠르지만 invariant가 단일 statement로 표현될 때만 충분하다. `SELECT FOR UPDATE`는 명시적이고 이해하기 쉽지만 blocking과 deadlock 관리가 필요하다. unique/partial unique constraint는 중복 방지에 강하지만 predicate/index inference mismatch가 있으면 upsert가 깨진다. `Serializable`은 가장 일반적이지만 retry 설계와 운영 관측이 필요하다.

실제 프로세스/Testcontainers 기반 테스트는 신뢰도가 높지만 CI 시간과 Docker 의존성이 늘어난다. Pact는 계약 drift 방지에 좋지만 provider 기능 테스트나 side effect 검증을 대체하지 않는다. mutation/negative control은 guard 검증에 강하지만 모든 코드에 적용하면 비용이 크므로 핵심 guard에 한정해야 한다.

**4. 열린 질문**

- backend-kit에 DB-specific annex를 둘지, `backend-audit`의 “PostgreSQL 감지 시 추가 rule”로만 둘지 결정 필요.
- H1의 `EXISTS` guard를 일반 “predicate-in-write” 원칙으로 둘지, “authorization/visibility predicate는 write SQL에 포함”처럼 더 좁힐지 결정 필요.
- H3 negative control을 필수 CI gate로 할 범위: 동시성/idempotency/auth guard만인지, 모든 critical invariant인지 정해야 한다.
- 실측 H1~H3의 원 프로젝트 커밋/테스트 로그는 이 세션에서 확인하지 못했다. 사용자 제공 신호 기준이며 외부 검증은 미확인.
