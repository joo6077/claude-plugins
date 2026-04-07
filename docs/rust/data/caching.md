---
title: 캐싱 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 캐싱 원칙

`moka 0.12.x`(인메모리 L1)와 `deadpool-redis 0.23.x`(분산 L2)를 계층적으로 조합한다. moka는 동일 프로세스 내 고속 캐시, Redis는 다중 인스턴스 공유 캐시로 사용한다.

---

## 원칙

### 1. `moka::future::Cache`로 인메모리 캐시를 구성한다

```toml
[dependencies]
moka = { version = "0.12", features = ["future"] }
```

```rust
use moka::future::Cache;
use std::time::Duration;

pub fn build_user_cache() -> Cache<Uuid, Arc<User>> {
    Cache::builder()
        .max_capacity(10_000)
        .time_to_live(Duration::from_secs(300))   // 5분 TTL
        .time_to_idle(Duration::from_secs(60))    // 60초 미사용 시 퇴거
        .build()
}
```

캐시 미스 시 중복 초기화(thundering herd)는 `get_with`로 방지한다.

```rust
let user = cache
    .get_with(user_id, async {
        Arc::new(db.find_user(user_id).await.unwrap())
    })
    .await;
```

### 2. `deadpool-redis`로 Redis 연결 풀을 구성한다

```toml
[dependencies]
deadpool-redis = { version = "0.23", features = ["rt_tokio_1"] }
redis = "0.28"
```

```rust
use deadpool_redis::{Config, Runtime, Pool};

pub fn build_redis_pool(url: &str) -> Pool {
    Config::from_url(url)
        .create_pool(Some(Runtime::Tokio1))
        .expect("Redis pool creation failed")
}

// 사용
pub async fn get_cached_session(pool: &Pool, session_id: &str) -> Option<String> {
    let mut conn = pool.get().await.ok()?;
    redis::cmd("GET")
        .arg(session_id)
        .query_async::<String>(&mut conn)
        .await
        .ok()
}

pub async fn set_cached_session(
    pool: &Pool,
    session_id: &str,
    value: &str,
    ttl_secs: u64,
) -> Result<(), anyhow::Error> {
    let mut conn = pool.get().await?;
    redis::cmd("SETEX")
        .arg(session_id)
        .arg(ttl_secs)
        .arg(value)
        .query_async::<()>(&mut conn)
        .await?;
    Ok(())
}
```

### 3. L1(moka) + L2(Redis) 계층 캐시 패턴

```rust
pub struct TieredCache {
    l1: Cache<String, Arc<UserProfile>>,
    l2: Pool,
}

impl TieredCache {
    pub async fn get(&self, key: &str) -> Option<Arc<UserProfile>> {
        // L1 먼저
        if let Some(v) = self.l1.get(key).await {
            return Some(v);
        }
        // L2 fallback
        let mut conn = self.l2.get().await.ok()?;
        let json: String = redis::cmd("GET")
            .arg(key)
            .query_async(&mut conn)
            .await
            .ok()?;
        let profile: UserProfile = serde_json::from_str(&json).ok()?;
        let arc = Arc::new(profile);
        self.l1.insert(key.to_string(), arc.clone()).await;
        Some(arc)
    }

    pub async fn invalidate(&self, key: &str) {
        self.l1.invalidate(key).await;
        if let Ok(mut conn) = self.l2.get().await {
            let _ = redis::cmd("DEL")
                .arg(key)
                .query_async::<()>(&mut conn)
                .await;
        }
    }
}
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| moka 버전 | 0.12.x | `future` feature 필요 |
| deadpool-redis 버전 | 0.23.x | `rt_tokio_1` feature 필요 |
| moka max_capacity | 엔티티당 1만~10만 | 메모리 사용량 모니터링 |
| Redis TTL | 데이터 성격에 따라 | 세션 30분, 사용자 프로필 5분 |
| Redis 연결 풀 크기 | 기본값 사용 | `deadpool` 기본값은 CPU 코어 수 기반 |

---

## 안티패턴

### `moka` 캐시 없이 모든 요청을 Redis로

Redis는 네트워크 왕복이 발생한다. 동일 프로세스에서 자주 읽는 데이터는 moka L1으로 먼저 확인한다.

### 캐시 무효화를 쓰기 경로에서 누락

DB를 업데이트하고 캐시를 무효화하지 않으면 낡은 데이터가 제공된다. 쓰기 작업 후 반드시 `invalidate(key)`를 호출한다.

### Redis 직접 연결(풀 없이) 사용

`redis::Client::get_async_connection()`을 매 요청마다 생성하면 연결 오버헤드가 크다. `deadpool-redis`로 풀을 사용한다.

### TTL 없는 캐시 항목

Redis에 TTL을 설정하지 않으면 메모리가 무한히 증가한다. 모든 캐시 항목에 적절한 TTL을 설정한다.

---

## Gotchas

### `moka::future::Cache`는 `Clone`이 `O(1)`이다

내부적으로 `Arc`를 사용하므로 `AppState`에 직접 포함해도 된다. 별도로 `Arc<Cache<...>>`로 감쌀 필요가 없다.

### `get_with`는 동일 키에 대한 동시 초기화를 한 번만 실행한다

여러 태스크가 동시에 캐시 미스를 경험해도 초기화 클로저는 한 번만 실행된다. thundering herd 문제를 자동으로 방지한다. `try_get_with`는 실패 시 에러를 반환한다.

### `deadpool-redis`는 `MultiplexedConnection`을 사용한다

단일 물리 연결을 멀티플렉싱하므로 pub/sub이나 블로킹 커맨드(`BLPOP` 등)에는 적합하지 않다. 블로킹 작업에는 별도 연결을 사용한다.

### Redis 직렬화는 JSON 또는 MessagePack을 명시적으로 처리한다

Redis는 바이트열만 저장한다. `serde_json::to_string()`으로 직렬화하고 `serde_json::from_str()`로 역직렬화하는 패턴을 일관되게 유지한다.
