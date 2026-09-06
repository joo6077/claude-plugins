---
title: 캐싱
version: 0.1.0
last_updated: 2026-04-04
---

# 캐싱

캐시 계층 구조, 캐싱 전략(cache-aside, write-through, write-behind, refresh-ahead), TTL, cache stampede, Redis vs Memcached, 캐시 무효화, 분산 캐시를 다룬다.

---

## 원칙

### 1. 캐시는 계층적으로 구성한다

데이터가 사용자에게 도달하기까지 여러 계층에서 캐싱이 가능하다: **브라우저 캐시** → **CDN** → **애플리케이션 캐시(Redis)** → **DB 쿼리 캐시**. 각 계층은 역할이 다르며, 가능한 사용자에게 가까운 계층에서 응답하는 것이 최선이다. 정적 자산은 CDN, 동적 데이터는 애플리케이션 캐시, 쿼리 결과는 DB 캐시에서 처리한다.

> **출처:** [AWS — Caching Overview](https://aws.amazon.com/caching/)

### 2. Cache-aside가 가장 범용적인 전략이다

애플리케이션이 먼저 캐시를 조회하고, 미스면 DB에서 읽어 캐시에 저장한다. 캐시 장애 시에도 DB에서 직접 서빙할 수 있어 복원력이 높다. 단점은 첫 요청이 항상 느리고(cold miss), 캐시와 DB 간 일시적 불일치가 발생할 수 있다는 점이다.

> **출처:** [Microsoft — Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)

### 3. Write-through는 일관성, write-behind는 쓰기 성능을 우선한다

**Write-through**: 쓰기 시 캐시와 DB를 동기적으로 갱신한다. 일관성이 보장되지만 쓰기 지연이 증가한다. **Write-behind(write-back)**: 캐시만 즉시 갱신하고 DB 쓰기는 비동기로 배치 처리한다. 쓰기 성능이 높지만 캐시 장애 시 데이터 유실 위험이 있다. **Refresh-ahead**: TTL 만료 전에 백그라운드에서 미리 갱신한다. 읽기 지연을 최소화하지만 예측이 빗나가면 불필요한 갱신이 발생한다.

> **출처:** [Redis — Caching Patterns](https://redis.io/docs/latest/develop/use/patterns/)

### 4. TTL은 데이터 특성에 맞게 설정한다

TTL(Time-To-Live)은 캐시 항목의 유효 기간이다. 변경 빈도가 낮은 설정 데이터는 1시간, 자주 바뀌는 피드 데이터는 5분, 사용자 세션은 30분이 일반적이다. TTL이 너무 짧으면 캐시 효과가 없고, 너무 길면 stale 데이터를 서빙한다.

> **출처:** [Redis — EXPIRE Command](https://redis.io/docs/latest/commands/expire/)

### 5. Cache stampede를 방지한다

인기 키의 TTL이 만료되면 다수의 요청이 동시에 DB를 조회하는 thundering herd 문제가 발생한다. 방어 전략 2가지: **Lock(mutex)** — 첫 요청만 DB를 조회하고 나머지는 lock 해제까지 대기(lock timeout 1~5초). **Probabilistic early expiration** — TTL 만료 전에 확률적으로 미리 갱신하여 동시 만료를 회피한다.

> **출처:** [Redis — Cache Stampede](https://redis.io/docs/latest/develop/use-cases/cache-aside/)

### 6. Redis와 Memcached는 용도가 다르다

**Redis**는 문자열, 해시, 리스트, sorted set, stream 등 다양한 데이터 구조를 지원하며, 영속성(RDB/AOF), pub/sub, Lua 스크립팅이 가능하다. **Memcached**는 단순 key-value에 특화되어 멀티스레드로 순수 캐싱 처리량이 높다. 대부분의 경우 Redis가 범용적이고, Memcached는 대규모 단순 캐싱에 적합하다.

> **출처:** [Redis — Getting Started](https://redis.io/docs/latest/get-started/), [Memcached Documentation](https://docs.memcached.org/)

### 7. 캐시 무효화는 이벤트 기반으로 한다

Phil Karlton의 격언대로 캐시 무효화는 컴퓨터 과학에서 가장 어려운 문제 중 하나다. TTL 만료에만 의존하면 stale 데이터 기간이 길어진다. 데이터 변경 이벤트(DB 트리거, 메시지 큐)가 발생하면 즉시 관련 캐시를 삭제하는 이벤트 기반 무효화가 일관성과 신선도를 모두 확보한다.

> **출처:** Phil Karlton 격언, [Microsoft — Caching Best Practices](https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching)

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| Redis maxmemory-policy | `allkeys-lru` 권장 | 기본값 `noeviction`은 메모리 초과 시 쓰기 거부 |
| TTL — 설정/메타데이터 | 30분~1시간 | 변경 빈도 낮은 데이터 |
| TTL — 피드/목록 | 5분~15분 | 변경 빈도 높은 데이터 |
| TTL — 세션 | 30분 | 사용자 활동 기준 갱신 |
| Stampede lock timeout | 1~5초 | 초과 시 직접 DB 조회로 fallback |
| Redis 단일 키 최대 크기 | 512 MB | 실무에서는 1 MB 이하 권장 |
| Redis 최대 키 수 | 약 2^32개 (42억) | 메모리가 제한 요소 |

---

## 안티패턴

### TTL 없는 캐시

TTL을 설정하지 않으면 데이터가 영구히 캐시에 남아 stale 데이터를 서빙하고, 메모리가 무한 증가한다. 모든 캐시 항목에 TTL을 설정한다.

### 모든 데이터 캐싱

자주 조회되지 않는 데이터까지 캐싱하면 메모리 낭비이고 캐시 적중률(hit rate)이 떨어진다. 파레토 법칙: 20%의 핫 데이터가 80%의 요청을 처리한다.

### 캐시를 primary storage로 사용

Redis를 DB 대용으로 쓰면 장애 시 데이터가 유실된다. 영속성(AOF/RDB)을 켜도 DB 수준의 내구성은 보장하지 않는다. 캐시는 언제든 전체 삭제 가능해야 한다.

### 무효화 없는 write-behind

비동기 쓰기만 하고 무효화를 누락하면, 다른 서버가 stale 캐시를 읽는다. 분산 환경에서는 쓰기 후 반드시 관련 캐시 키를 무효화한다.

---

## Gotchas

- **Redis 단일 스레드라 O(N) 명령이 전체를 블로킹** — `KEYS *`, 대량 `SMEMBERS`, `HGETALL`(큰 해시)은 수백 ms 이상 블로킹한다. 프로덕션에서는 `SCAN` 계열 명령 사용. `KEYS` 명령은 `rename-command`로 비활성화 권장
- **캐시 웜업 없이 배포하면 cold start stampede** — 새 인스턴스 배포 시 캐시가 비어있어 모든 요청이 DB로 직행한다. 배포 전 캐시 프리워밍(prewarming) 스크립트를 실행하거나, 점진적 트래픽 전환(canary)으로 완화
- **분산 캐시 일관성은 eventual** — 멀티 리전 Redis 클러스터에서 노드 간 동기화는 비동기다. 강한 일관성이 필요한 데이터(재고, 결제)는 캐시가 아닌 DB에서 직접 읽는다
