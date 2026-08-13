# 쓰기 경로 무결성 프로토콜 (SSOT)

사전 조회 후 쓰기(read-check-then-write) 경합 · 중복 방지 제약과 upsert 대상의 정합 · 멱등 쓰기
계약 · 그 가드가 실제로 동작함을 증명하는 테스트를 다룬다. backend-kit 안에서 이 규칙의 본문은
**이 파일 (`backend-kit/references/write-path-integrity-protocol.md`) 하나**다 — 소비 표면
(`backend-guide` · `backend-system` · `backend-audit` · `backend-test` · `backend-reviewer`) 은 이
경로를 **인용만** 하고 규칙을 재열거하지 않는다.

> **왜 생겼나 (2026-08-12 실측 REJECT `ER-02`):** *"신규 통합 테스트가 실제 바이너리를 호출하지
> 않고 독립적으로 재작성한 SQL 로 낙관적 동시성의 일반 동작만 검증한다. **mutation test 로 확정 —
> 실제 코드에서 동시성 가드를 완전히 삭제해도 이 테스트는 여전히 통과한다.**"* 가드는 구현돼
> 있었고 테스트도 통과했는데, 그 테스트는 가드를 재고 있지 않았다. 같은 기간 신호로 FCM 토큰
> 등록의 partial unique index 충돌(§3)과 feed TOCTOU 의 in-SQL 술어 해소(§1)가 함께 관측됐다.

**기존 기준과 겹치지 않는다.** `backend-audit` 의 rule SSOT 는 두 파일로 나뉜다:

| 문서 | 담당 범위 |
| ------ | ------ |
| `skills/backend-audit/references/audit-criteria.md` | 10 카테고리의 기존 rule (§3 Database = N+1 · 인덱스 · pooling · migration, §9 Testing = 6 rule(테스트 유무 · 실 DB · contract test · mock drift · 통합 실체 · 마이그레이션 선행)) |
| **이 프로토콜** | write path 무결성 rule (경합 가드 적합성 · upsert arbiter 정합 · 멱등 저장 계약 · 통합 타깃 증명 · 핵심 guard 음성 대조) |

두 문서의 rule 집합은 **교집합이 없다.** 하나의 rule 을 두 곳에 적지 마라.

---

## 1. 경합을 발견하면 invariant 부터 분류한다 (E2)

`SELECT` 로 상태를 읽고 → 애플리케이션 코드에서 판단하고 → `INSERT`/`UPDATE`/`DELETE` 하는 흐름은
두 문장 사이에 다른 트랜잭션이 끼어들 수 있다. 앱 레벨 `if` 는 이 창을 좁힐 뿐 닫지 못한다.

이 패턴을 발견하면 **FAIL 후보로 보고 먼저 invariant 를 분류**한다. 분류 없이 "동시성 처리됨" 으로
PASS 를 주지 마라 — 어떤 primitive 가 그 invariant 를 담당하는지가 판정의 전부다.

| # | invariant 유형 | 담당 primitive | PASS 조건 |
| - | ------ | ------ | ------ |
| A | **같은 row 의 상태 전이** (승인 → 완료, 잔여 수량 차감, 낙관적 락) | 조건부 `UPDATE ... WHERE <기대 상태/버전>` 또는 동등한 compare-and-swap | 기대값이 술어에 들어 있고, **영향 행 수 0 을 성공으로 흘리지 않는다** (도메인 conflict 로 승격) |
| B | **존재 · 권한 · 가시성 predicate** (내 리소스인가, 차단 관계인가, 공개 범위에 드는가) | 쓰기 SQL 자체의 `WHERE EXISTS (...)` / 조인 술어 | 사전 `SELECT` 검사가 아니라 **쓰기 문장의 술어**로 들어가 있다 |
| C | **cross-row · absence · aggregate invariant** (중복 없음, 구간 겹침 없음, 합계 상한) | unique / partial unique / exclusion 제약, 명시적 lock, 또는 `Serializable` + 직렬화 실패 재시도 | 셋 중 **하나가 명시적으로 존재**하고 어떤 것을 골랐는지 근거에 적혀 있다 |

**분류 산출물(E2)** — 감사·가이드·계약 어디서든 아래 3 줄을 남긴다. 문장 다짐으로 대체하지 마라.

```text
invariant: <A|B|C> — <무엇이 깨지면 안 되는가>
primitive: <조건부 UPDATE | WHERE EXISTS | 제약명 | 명시적 lock | Serializable+retry>
증거: <파일:라인 — 그 primitive 가 실재하는 위치>
```

**유형별 주의:**

- **A 는 `READ COMMITTED` 에서도 성립한다.** PostgreSQL 의 `READ COMMITTED` 는 `UPDATE`/`DELETE`/
  `SELECT FOR UPDATE` 가 동시 갱신자를 만나면 기다린 뒤 **갱신된 row 에 `WHERE` 조건을 다시
  평가**한다. 그래서 기대값을 술어에 넣은 조건부 갱신이 낙관적 동시성 가드로 성립한다.
  출처: [PostgreSQL — Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- **B 를 A 로 일반화하지 마라.** 같은 문서가 `READ COMMITTED` 에서 **복잡한 search condition 은
  일관성 판단에 부적합할 수 있다**고 경고한다. 조건부 `UPDATE` 하나로 cross-row predicate 까지
  덮는다고 주장하면 FAIL 이다.
- **C 를 `SELECT FOR UPDATE` 로 덮지 마라.** 이 lock 은 **반환된 기존 row** 를 잠근다. "존재하지
  않는 row"(absence invariant)나 predicate 전체를 자동으로 잠그는 수단이 아니다.
  출처: [PostgreSQL — Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)

## 2. "트랜잭션으로 감싸라" 만으로 PASS 금지 (E1)

트랜잭션 경계는 **원자성**을 준다. 그것만으로 경합이 막히지는 않는다. 동시성 항목을 PASS 하려면
아래 두 문장이 **둘 다** 있어야 한다.

1. **어떤 anomaly 를 막는가** — dirty read / nonrepeatable read / phantom read /
   serialization anomaly 중 무엇인가.
2. **어떤 primitive 가 담당하는가** — §1 표의 primitive 중 무엇인가.

둘 중 하나라도 없으면 FAIL 이다. "`BEGIN ... COMMIT` 으로 감쌌으니 안전하다" 는 근거가 아니다.

- 위 4 종 anomaly 분류와, PostgreSQL 에서 **`Serializable` 만 serialization anomaly 를 막는다**는
  사실은 [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) 에
  있다.
- Snapshot Isolation 은 **write skew(A5B)** 를 허용한다 — 두 트랜잭션이 각자 읽은 스냅샷 위에서
  서로 다른 row 를 갱신해 합쳐진 결과가 불변식을 깨는 경우다. "SI 를 쓰니 직렬화된다" 는 서술은
  틀렸다. 출처: [Berenson et al., A Critique of ANSI SQL Isolation Levels](https://sigmodrecord.org/1995/06/06/a-critique-of-ansi-sql-isolation-levels/)

**금지 3 종 (권고로도 쓰지 마라):**

- **`Serializable` 을 전 write path 기본값으로 강제하지 마라.** 직렬화 실패 재시도 설계와 abort율
  운영 관측이 따라와야 하는 선택지다. §1-C 의 세 수단 중 하나일 뿐 기본값이 아니다.
- **`SELECT FOR UPDATE` 를 모든 TOCTOU 의 해법으로 제시하지 마라** (§1-C 주의 참조).
- **`READ COMMITTED` + 복잡한 술어를 "안전" 으로 서술하지 마라** (§1-B 주의 참조).

## 3. 중복 방지 제약과 upsert 대상은 문자 그대로 일치해야 한다 (E2)

**스택 무관 원칙:** 중복을 막는 제약이 **일부 행에만 적용되는 형태**(조건부 · 계산식 기반)인데
upsert 문이 지목하는 충돌 대상이 그 조건까지 포함하지 않으면, 제약은 존재하지만 upsert 는
그것을 쓰지 못한다. 결과는 "가끔 성공하고 가끔 중복 키 오류" 다. 제약 정의와 upsert 의 충돌
대상을 **양쪽 다 열거해 대조**하라. 한쪽만 읽고 PASS 를 주지 마라.

**대조 산출물(E2):**

```text
| 제약명 | 대상 컬럼/식 | 적용 조건(predicate) | upsert 문 위치 | upsert 충돌 대상 | 일치 |
```

### PostgreSQL 감지 시 추가 rule

DB 엔진 감지는 마이그레이션 DDL · 드라이버 의존성 · 접속 문자열 중 하나로 확정한다. PostgreSQL 이
아니면 이 절은 N/A 이며, 위 스택 무관 원칙만 적용한다.

- partial index 는 predicate 를 만족하는 **subset 에만** 적용되고, 플래너가 쿼리 조건이 index
  predicate 를 함의한다고 인식해야 쓰인다. 공식 문서는 일반 정리 증명기가 없으며 많은 경우
  predicate 가 쿼리 `WHERE` 와 정확히 맞아야 하고, 파라미터화된 절은 partial index 와 맞지 않을 수
  있다고 적는다. 출처: [PostgreSQL — Partial Indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
- `ON CONFLICT` 의 unique index inference 는 column/expression 과 선택적 `index_predicate` 가
  arbiter index 를 만족해야 한다. inference 에 실패하면 에러이며, `DO UPDATE` 는 conflict target 이
  **필수**다. partial unique index 를 arbiter 로 쓰려면 `ON CONFLICT (cols) WHERE predicate` 처럼
  predicate 까지 맞춰야 한다. column/expression/predicate 중 하나라도 어긋나면 **FAIL**.
  출처: [PostgreSQL — INSERT](https://www.postgresql.org/docs/current/sql-insert.html)
- `ON CONFLICT DO NOTHING` 에서 conflict target 을 **생략**하면 "사용 가능한 모든 제약 위반을
  회피" 하는 의미가 된다. 의도한 멱등 결과(원 레코드 반환 등)를 보장하지 못하므로, 반환값을
  쓰는 경로에서는 WARN, 멱등 계약(§4)의 근거로 삼고 있으면 FAIL.

## 4. Idempotent Write Contract — 6 항목 (E2)

비멱등 write path(POST/PATCH · 메시지 소비 · 백필 잡)는 재시도 안전성을 **계약에 적어야** PASS 다.
아래 6 항목 중 하나라도 비면 FAIL.

| # | 항목 | 적어야 하는 것 |
| - | ------ | ------ |
| 1 | **key 범위** | 멱등 키가 무엇이고 어느 범위에서 유일한가 (전역 · 테넌트별 · 엔드포인트별 · 자연키 조합). 범위를 안 적으면 서로 다른 자원이 같은 키를 재사용한다 |
| 2 | **payload fingerprint** | 같은 키의 재요청이 같은 요청인지 무엇으로 판정하는가 (체크섬 · 필드 매칭 · 요청 다이제스트). fingerprint 없이 키만 보면 4·5 를 구분할 수 없다 |
| 3 | **replay response** | 완료된 원 요청의 결과를 어디에 저장하고 무엇을 그대로 돌려주는가 |
| 4 | **in-flight duplicate** | 원 요청이 **처리 중**일 때 도착한 중복을 어떻게 처리하는가 |
| 5 | **different-payload reuse** | 같은 키에 **다른 페이로드**가 오면 어떻게 거절하는가 |
| 6 | **expiry** | 키·결과 레코드를 언제까지 보관하고 만료 후 같은 키가 오면 어떻게 되는가 |

- HTTP 상태코드 규약(원 결과 반환 · 처리 중 · 다른 페이로드 · 헤더 누락)의 SSOT 는
  `skills/backend-audit/references/audit-criteria.md` §2 "비멱등 write path idempotency" 다.
  **여기서 상태코드를 다시 정의하지 마라.** 이 절은 그 규약이 성립하려면 저장소 측에 무엇이
  있어야 하는지만 정한다.
- **IETF `draft-ietf-httpapi-idempotency-key-header` 는 만료된 Internet-Draft 다.** "표준" ·
  "RFC" 로 서술하면 FAIL 이며, 사실상 관행으로만 인용한다.
  출처: [IETF datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
- 벤더 구현 참조: Stripe 는 멱등 키, 결과 저장, **페이로드 비교**, 24 시간 후 키 정리(pruning)를
  문서화한다. 6 항목 중 1·2·3·5·6 에 대응하는 실무 레퍼런스다.
  출처: [Stripe — Idempotent requests](https://docs.stripe.com/api/idempotent_requests)

## 5. Integration Target Proof 와 핵심 guard 음성 대조

### 5a. 실체 확인과 타깃 증명은 다른 검사다 (E3 — 결합 확인)

`audit-criteria.md` §9 의 통합 테스트 **실체** rule 은 **의존성이 진짜인가**(Testcontainers/실 DB 인가,
인메모리 대체물인가)를 본다. 이 절은 **대상 코드가 진짜인가**를 본다. `ER-02` 는 전자를 통과하고
후자에서 걸렸다 — 실 DB 를 썼지만 테스트가 SQL 을 독립 재작성해서, 구현의 가드를 지워도 통과했다.

통합 테스트가 PASS 하려면 **production handler / repository / 서비스 함수 / 실제 실행 바이너리
또는 로컬 기동된 provider 를 실제로 통과한다는 증거**가 있어야 한다.

- 결합 확인은 정적으로 결정론적이다 — 테스트 파일이 구현 심볼을 import·호출하는지 grep 한다.
  근거란에 `결합: {테스트 파일:라인} → {구현 심볼}` 을 남긴다.
- **독립 재작성 SQL 로 "일반적인 동작" 만 확인한 테스트는 integration 이 아니다.** query-level
  보조 테스트로 재분류하고, 통합 테스트 개수에 계상하지 마라.
- 로컬 기동된 provider 에 실제 요청을 재생해 응답을 비교하는 방식도 유효한 타깃 증명이다. 다만
  요청 본문을 추출·검증하기 **전 레이어를 stub 하면 어떤 garbage body 도 통과**하므로, stub 위치가
  검증 지점보다 뒤에 있는지 함께 확인한다.
  출처: [Pact — Provider verification](https://docs.pact.io/provider)
- 인메모리·mock 대체물이 프로덕션 서비스와 동작이 다르다는 근거:
  [Testcontainers — Getting started](https://testcontainers.com/getting-started/)

### 5b. 핵심 guard 는 음성 대조에서 실패해야 한다

동시성 가드(§1) · 인증/인가 guard · 멱등 arbiter(§3·§4) 세 가지는 **그 지점을 제거·무력화한
상태에서 테스트가 FAIL 해야** PASS 다. 코드에 결함을 주입했는데 테스트가 통과하면 그 테스트는
결함을 잡지 못한다는 신호다. 출처: [PIT — Mutation testing](https://pitest.org/)

- 실행하지 못했으면 `[미검증]` 이 **아니라** "guard proof 없음" 으로 FAIL 후보다. `[미검증]` 은
  검증 도구·환경 부재 전용 마커다.
- **판정 절차 · 안전 조건 · 임계값은 여기서 정의하지 않는다.** 정본은 아래 §8 표를 따른다.

### 5c. 적용 범위 한정 — 전면 강제 금지

- **Testcontainers / 계약 테스트 도구를 모든 테스트에 요구하지 마라.** 단위 테스트에는 과하고,
  CI 시간과 Docker 의존성 비용이 실재한다. 실 의존성 요구는 DB·브로커 상호작용을 주장하는
  테스트에만 적용한다.
- **음성 대조 요구는 위 3 종 guard 에만 적용한다.** 모든 조건에 요구하면 계약에 없는 비용이 된다.
- **전체 저장소 mutation score 임계값을 세우지 마라** (§8 정본의 금지 조항).

## 6. Outbox 는 at-least-once 다 — "exactly-once 보장" 서술 금지

- 비즈니스 테이블 갱신과 outbox insert 는 **같은 트랜잭션**이어야 한다. 이것이 이중쓰기(dual
  write)를 막는 부분이다.
- 그러나 relay 는 **중복 발행할 수 있다.** 따라서 outbox 를 쓰는 write path 는 **consumer 측
  idempotency(§4)를 함께 요구**해야 PASS 다. outbox 단독으로, 또는 outbox + CDC 조합으로
  "exactly-once 가 보장된다" 고 서술하면 **FAIL** 이다.
  출처: [microservices.io — Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html)

## 7. 안티패턴

- 사전 `SELECT` 검사 + 앱 레벨 `if` 를 원자적 가드로 설명한다.
- 경합 질문에 "트랜잭션으로 감싸세요" 만 답한다 (§2).
- 조건부 갱신 술어는 있는데 **영향 행 수 0** 을 성공으로 흘린다.
- `SELECT FOR UPDATE` 를 absence/predicate invariant 의 해법으로 제시한다.
- 조건부 unique 제약이 있는데 upsert 충돌 대상에 그 조건을 빼먹는다 (§3).
- 멱등 키만 있고 payload fingerprint · expiry 를 계약에 안 적는다 (§4).
- 실 DB 를 쓴다는 이유로, SQL 을 독립 재작성한 테스트를 통합 테스트로 계상한다 (§5a).
- guard 의 positive 경로만 테스트하고 "동시성 검증됨" 으로 보고한다 (§5b).
- outbox 를 근거로 "exactly-once" 를 주장한다 (§6).

## 8. 정본 인용 (재정의 금지)

이 프로토콜은 **생산 측**(무엇을 만들고 무엇을 테스트할지)만 정의한다. 판정 절차와 임계 규칙은
아래 정본을 따르며 여기서 다시 정의하지 않는다.

| 축 | 정본 | 이 프로토콜의 역할 |
| ------ | ------ | ------ |
| 측정 판별력 판정 | `harness/docs/guides/qa-evaluation-guide.md` §Discriminating Evidence Gate (적용 범위 1·2·3 번 = 동시성 가드 · auth · 멱등성) | 그 게이트가 요구하는 **결합**과 **음성 대조 지점**을 코드 쪽에서 미리 만족시킨다 |
| 계약 문구 | `harness/references/contract-schema.md` §음성 대조 | 조건에 적을 `음성 대조:` 절의 대상 지점(= §1 술어 · §3 arbiter · §4 키 판정)을 지정해 준다 |
| `[미검증]` 마커 의미·임계값 | `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol | 마커를 쓰지 않아야 할 경우(§5b)만 지정한다 |
| enforcement 등급 정의·승급 | `harness/docs/guides/skill-design-guide.md` §3.7 | 아래 표는 이 프로토콜 조항의 **현재 등급 기록**이다 |

### 이 프로토콜 조항의 enforcement 등급

| 조항 | 등급 | 근거 · 승급 트리거 |
| ------ | ------ | ------ |
| §1 invariant 분류 | **E2** | 3 줄 분류 산출물을 남긴다. 분류 없이 PASS 가 2 회 재발하면 분류표 존재를 검사하는 E3 |
| §2 generic transaction advice 금지 | **E1** | 최초 도입 · 문맥 해석이 필요한 판정. 재발 2 회 → E2 |
| §3 arbiter 대조 | **E2** | 제약↔upsert 대조 표 아티팩트 |
| §4 멱등 계약 6 항목 | **E2** | 6 항목 체크리스트 아티팩트 |
| §5a 결합 확인 | **E3** | 테스트가 구현 심볼을 호출하는지는 grep 으로 LLM 없이 판정된다. `ER-02` 는 이 검사만 있었어도 걸렸다 |
| §5b 음성 대조 | 정본 등급을 따른다 | `qa-evaluation-guide.md` §원칙별 Enforcement 등급 표의 `Discriminating Evidence Gate` 행. **여기서 재정의하지 않는다** |
| §6 outbox 전달 보장 | **E1** | 사실 서술 규칙 |

> **Rust 프로젝트는 이 킷의 대상이 아니다.** `backend-audit` · `backend-test` 는 `Cargo.toml` 감지
> 시 rust-kit 으로 리다이렉트하며, rust-kit 에는 같은 문제의 Rust 전용 SSOT 가 따로 있다.
