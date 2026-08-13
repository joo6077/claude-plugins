---
title: 데이터베이스
version: 0.2.0
last_updated: 2026-08-13
---

# 데이터베이스

스키마 설계, 정규화와 반정규화, 인덱스 전략, 쿼리 최적화, N+1 문제, connection pooling, 마이그레이션 전략, 파티셔닝, 쓰기 경로 경합(동시성 가드)을 다룬다.

---

## 원칙

### 1. 정규화 우선, 읽기 성능 병목에서만 반정규화한다

3NF(제3정규형)까지 정규화하여 데이터 무결성과 저장 효율을 확보한다. 반정규화는 측정된 읽기 병목이 있을 때만 적용한다. 반정규화 시 갱신 이상(update anomaly)이 발생하므로, 어떤 쿼리의 어떤 지표(latency, throughput)를 얼마나 개선하는지 수치로 증명한 후 진행한다.

> **출처:** [PostgreSQL Documentation — Table Basics](https://www.postgresql.org/docs/current/ddl-basics.html)

### 2. 인덱스는 쿼리 패턴 기반으로 선택한다

| 인덱스 타입 | 용도 | 적합한 쿼리 |
|------------|------|------------|
| **B-tree** | 범위 검색, 정렬, 등치 비교 | `WHERE created_at > ?`, `ORDER BY id` |
| **Hash** | 등치 비교 전용 | `WHERE email = ?` (PostgreSQL에서는 B-tree가 대부분 더 나음) |
| **GIN** | 전문 검색, 배열, JSONB | `WHERE tags @> '{python}'`, `to_tsvector() @@ to_tsquery()` |
| **GiST** | 공간 데이터, 범위 타입 | `WHERE location <-> point(x,y)`, `WHERE range && '[1,10]'` |

복합 인덱스의 컬럼 순서는 선택도(selectivity)가 높은 컬럼을 앞에 둔다. 인덱스가 많을수록 쓰기 성능이 저하되므로, 실제 사용되는 쿼리 패턴에만 인덱스를 건다.

> **출처:** [PostgreSQL Documentation — Indexes](https://www.postgresql.org/docs/current/indexes.html)

### 3. EXPLAIN ANALYZE로 실행 계획을 확인한다

쿼리 작성 후 반드시 `EXPLAIN ANALYZE`로 실행 계획을 확인한다. 주의할 지표:

- **Seq Scan**: 전체 테이블 스캔. 대형 테이블에서 발생하면 인덱스 추가를 검토한다.
- **Nested Loop**: 소규모 결과 집합에서 효율적. 대규모에서는 Hash Join이 더 낫다.
- **actual time vs planned rows**: 예측 row 수와 실제 row 수의 괴리가 크면 `ANALYZE`로 통계를 갱신한다.

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 42 AND status = 'pending';
```

> **출처:** [PostgreSQL Documentation — Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)

### 4. N+1 문제는 ORM 레벨에서 해결한다

N+1은 1번의 목록 조회 후 각 항목마다 1번씩 추가 쿼리가 발생하는 패턴이다. 100개의 주문을 조회하면 101번의 쿼리가 실행된다.

해결 방법:
- **Eager loading**: `joinedload()` (SQLAlchemy), `include()` (Prisma), `prefetch_related()` (Django).
- **DataLoader 패턴**: 같은 이벤트 루프 내 중복 요청을 배치로 묶는다 (GraphQL에서 필수).
- **SQL 직접 작성**: ORM이 비효율적인 쿼리를 생성하면 JOIN을 직접 작성한다.

> **출처:** [SQLAlchemy — Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)

### 5. Connection pooling은 운영 환경 필수다

데이터베이스 연결은 비용이 크다(TCP 핸드셰이크 + 인증 + 메모리 할당). Pool 없이 요청마다 연결을 생성하면 수백 동시 요청에서 DB가 연결 한도에 도달한다.

- **PgBouncer**: PostgreSQL 전용 경량 프록시. Transaction mode에서 쿼리 실행 중에만 연결을 점유하므로 효율적이다.
- **HikariCP**: JVM 생태계 표준. 최소한의 오버헤드로 최대 throughput을 제공한다.
- **애플리케이션 내장 풀**: SQLAlchemy `create_engine(pool_size=5)`, Prisma `connection_limit` 등.

> **출처:** [PgBouncer Configuration](https://www.pgbouncer.org/config.html), [HikariCP](https://github.com/brettwooldridge/HikariCP)

### 6. Migration은 expand-contract 패턴을 따른다

무중단 배포 환경에서 스키마 변경은 3단계로 진행한다:

1. **Expand**: 새 컬럼/테이블 추가. 기존 코드는 영향 없음.
2. **Migrate**: 이중 쓰기(dual write). 새 코드는 새 컬럼에 쓰고, 백필(backfill)로 기존 데이터를 옮긴다.
3. **Contract**: 이전 컬럼/테이블 제거. 모든 코드가 새 스키마를 사용하는 것을 확인한 후.

`ALTER TABLE ... ADD COLUMN`은 PostgreSQL에서 NOT NULL + DEFAULT가 없으면 테이블 재작성(rewrite) 없이 즉시 완료된다. 반면 컬럼 타입 변경(`ALTER COLUMN ... TYPE`)은 전체 테이블을 잠글 수 있다.

> **출처:** [Martin Fowler — Parallel Change](https://martinfowler.com/bliki/ParallelChange.html)

### 7. 파티셔닝은 TB급 테이블에서 range/list/hash 중 선택한다

| 전략 | 적합한 케이스 | 예시 |
|------|-------------|------|
| **Range** | 시계열, 날짜 기반 | 월별 로그 테이블 |
| **List** | 이산적 카테고리 | 국가별, 상태별 |
| **Hash** | 균등 분산 | 사용자 ID 기반 샤딩 |

파티셔닝은 쿼리가 파티션 키를 포함할 때만 효과적이다(partition pruning). 파티션 키 없는 쿼리는 모든 파티션을 스캔하므로 오히려 느려진다.

> **출처:** [PostgreSQL Documentation — Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)

### 8. 쓰기 경합은 invariant 를 분류한 뒤 DB primitive 로 막는다

`SELECT` 로 읽고 → 애플리케이션에서 판단하고 → 쓰는 흐름(read-check-then-write)은 두 문장 사이에
다른 트랜잭션이 끼어든다. 트랜잭션으로 감싸는 것은 **원자성**을 줄 뿐 이 창을 닫지 않는다. 무엇을
지켜야 하는지부터 분류하고 담당 primitive 를 고른다.

| invariant 유형 | 담당 primitive | 예시 |
|---------------|---------------|------|
| 같은 row 의 상태 전이 | 조건부 `UPDATE ... WHERE <기대 상태/버전>` (compare-and-swap) | `UPDATE orders SET status='paid' WHERE id=$1 AND status='pending'` |
| 존재 · 권한 · 가시성 predicate | 쓰기 SQL 자체의 `WHERE EXISTS (...)` / 조인 술어 | 차단 관계·공개 범위를 사전 `SELECT` 가 아니라 `INSERT ... SELECT ... WHERE EXISTS` 로 |
| cross-row · absence · aggregate | unique / partial unique / exclusion 제약, 명시적 lock, `Serializable` + 직렬화 실패 재시도 | 구간 겹침 금지 → exclusion 제약 |

- 조건부 갱신은 `READ COMMITTED` 에서도 성립한다 — PostgreSQL 은 `UPDATE`/`DELETE`/
  `SELECT FOR UPDATE` 가 동시 갱신자를 만나면 대기 후 **갱신된 row 에 `WHERE` 를 재평가**한다.
- **영향 행 수 0 을 성공으로 흘리지 마라.** 0 행은 "경합으로 스킵됨" 이며 도메인 conflict 로
  올려야 호출자가 재시도·보고를 결정할 수 있다.
- 격리 수준은 dirty read / nonrepeatable read / phantom read / serialization anomaly 로 나뉘고,
  PostgreSQL 에서 **`Serializable` 만 serialization anomaly 를 막는다**. Snapshot Isolation 은
  **write skew** 를 허용하므로 "SI 를 쓰니 직렬화된다" 는 서술은 틀렸다.
- `SELECT FOR UPDATE` 는 **반환된 기존 row** 를 잠근다. 존재하지 않는 row(absence invariant)나
  predicate 전체를 잠그는 수단이 아니다.

> **출처:** [PostgreSQL — Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [PostgreSQL — Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html), [Berenson et al. — A Critique of ANSI SQL Isolation Levels](https://sigmodrecord.org/1995/06/06/a-critique-of-ansi-sql-isolation-levels/)

### 9. 조건부 unique 제약과 upsert 의 충돌 대상은 문자 그대로 일치해야 한다

중복 방지 제약이 **일부 행에만 적용되는 형태**(조건부 · 계산식 기반)인데 upsert 문이 지목하는
충돌 대상이 그 조건을 포함하지 않으면, 제약은 있는데 upsert 가 그것을 쓰지 못한다. 증상은
"가끔 성공하고 가끔 중복 키 오류" 다.

- PostgreSQL partial index 는 predicate 를 만족하는 subset 에만 적용되고, 플래너가 쿼리 조건이
  index predicate 를 함의한다고 인식해야 쓰인다. 공식 문서는 일반 정리 증명기가 없어 많은 경우
  predicate 가 쿼리 `WHERE` 와 정확히 맞아야 한다고 적는다.
- `ON CONFLICT` 의 unique index inference 는 column/expression 과 선택적 `index_predicate` 가
  arbiter index 를 만족해야 하며, inference 실패는 에러다. `DO UPDATE` 는 conflict target 이
  필수이고, partial unique index 를 쓰려면 `ON CONFLICT (cols) WHERE predicate` 로 predicate 까지
  맞춰야 한다.
- `ON CONFLICT DO NOTHING` 에서 target 을 생략하면 "사용 가능한 모든 제약 위반 회피" 가 되어,
  의도한 멱등 결과(원 레코드 반환 등)를 보장하지 못한다.

> **출처:** [PostgreSQL — Partial Indexes](https://www.postgresql.org/docs/current/indexes-partial.html), [PostgreSQL — INSERT](https://www.postgresql.org/docs/current/sql-insert.html)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| HikariCP `maximumPoolSize` 기본값 | 10 |
| HikariCP `connectionTimeout` 기본값 | 30초 |
| HikariCP `idleTimeout` 기본값 | 10분 |
| HikariCP `maxLifetime` 기본값 | 30분 |
| PgBouncer `default_pool_size` 기본값 | 20 |
| PostgreSQL `shared_buffers` 권장값 | 시스템 RAM의 25% |
| PostgreSQL `work_mem` 기본값 | 4MB (복잡한 정렬/해시에서 증가 검토) |
| Pool size 공식 (HikariCP 권장) | `connections = (core_count * 2) + effective_spindle_count` |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 모든 컬럼에 인덱스 | 쓰기 성능 저하, 디스크 낭비, 옵티마이저 혼란. |
| `SELECT *` | 불필요한 데이터 전송, covering index 활용 불가. |
| ORM 기본 lazy loading 방치 | N+1 문제로 쿼리 수가 데이터 크기에 비례하여 폭증. |
| Pool 크기 무제한 | DB 연결 한도 초과, 메모리 고갈, 전체 서비스 장애. |
| 사전 `SELECT` + 앱 레벨 `if` 로 경합 방어 | 두 문장 사이의 창이 닫히지 않는다. 부하가 오르면 중복 생성·이중 차감이 실제로 발생한다. |
| 조건부 갱신 후 **영향 행 수 0** 을 성공으로 처리 | 가드가 있으나 마나 — 갱신되지 않았는데 성공으로 보고된다. |
| 조건부 unique 제약에 조건 없는 `ON CONFLICT` 대상 | arbiter inference 실패 또는 의도하지 않은 제약 회피. 간헐적 중복 키 오류로 나타난다. |

---

## Gotchas

- **GIN 인덱스는 쓰기 성능을 저하시킨다.** GIN은 역인덱스 구조로 삽입 시 인덱스 갱신 비용이 크다. `fastupdate=on`(기본값)으로 완화할 수 있지만, 첫 번째 읽기에서 펜딩 리스트를 정리하므로 읽기 latency 스파이크가 발생할 수 있다.
- **EXPLAIN과 EXPLAIN ANALYZE 결과가 다를 수 있다.** `EXPLAIN`은 통계 기반 예측이고, `EXPLAIN ANALYZE`는 실제 실행 결과다. 통계가 오래되면 예측 row 수와 실제 row 수가 크게 다를 수 있다. `ANALYZE` 명령으로 통계를 갱신한다.
- **`Serializable` 은 기본값이 아니다.** 모든 write path 에 걸면 직렬화 실패 재시도 설계와 abort율 관측이 따라와야 한다. 위 §8 표의 세 수단 중 cross-row·absence·aggregate invariant 에만 후보로 올린다.
- **`READ COMMITTED` + 복잡한 search condition 을 "안전" 으로 서술하지 마라.** PostgreSQL 문서 자신이 이 조합은 일관성 판단에 부적합할 수 있다고 경고한다. 조건부 `UPDATE` 하나로 cross-row predicate 까지 덮는다고 일반화하면 안 된다.
- **Connection pool exhaustion은 deadlock처럼 보인다.** 모든 커넥션이 점유된 상태에서 새 요청이 커넥션을 기다리면 타임아웃까지 멈춘다. 로그에는 "connection timeout"이지만 증상은 서비스 전체 행(hang)이므로 deadlock으로 오진하기 쉽다. 모니터링에 pool 사용률 메트릭을 반드시 포함한다.
