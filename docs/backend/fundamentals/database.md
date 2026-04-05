---
title: 데이터베이스
version: 0.1.0
last_updated: 2026-04-04
---

# 데이터베이스

스키마 설계, 정규화와 반정규화, 인덱스 전략, 쿼리 최적화, N+1 문제, connection pooling, 마이그레이션 전략, 파티셔닝을 다룬다.

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

---

## Gotchas

- **GIN 인덱스는 쓰기 성능을 저하시킨다.** GIN은 역인덱스 구조로 삽입 시 인덱스 갱신 비용이 크다. `fastupdate=on`(기본값)으로 완화할 수 있지만, 첫 번째 읽기에서 펜딩 리스트를 정리하므로 읽기 latency 스파이크가 발생할 수 있다.
- **EXPLAIN과 EXPLAIN ANALYZE 결과가 다를 수 있다.** `EXPLAIN`은 통계 기반 예측이고, `EXPLAIN ANALYZE`는 실제 실행 결과다. 통계가 오래되면 예측 row 수와 실제 row 수가 크게 다를 수 있다. `ANALYZE` 명령으로 통계를 갱신한다.
- **Connection pool exhaustion은 deadlock처럼 보인다.** 모든 커넥션이 점유된 상태에서 새 요청이 커넥션을 기다리면 타임아웃까지 멈춘다. 로그에는 "connection timeout"이지만 증상은 서비스 전체 행(hang)이므로 deadlock으로 오진하기 쉽다. 모니터링에 pool 사용률 메트릭을 반드시 포함한다.
