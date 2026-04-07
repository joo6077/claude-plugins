---
title: 비동기와 동시성 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 비동기와 동시성 원칙

Rust async는 Zero-cost abstraction이다 — async fn은 상태 머신으로 컴파일되며 런타임 스레드 비용이 없다. Tokio는 멀티 스레드 work-stealing 런타임으로 I/O 집약 서버 애플리케이션의 사실상 표준이다. async와 동기 코드의 경계를 명확히 하는 것이 핵심이다.

---

## 원칙

### 1. async 컨텍스트에서 블로킹 코드를 실행하지 않는다

Tokio 런타임은 적은 수의 OS 스레드(기본 CPU 코어 수)로 수만 개의 태스크를 처리한다. 하나의 태스크가 스레드를 블로킹하면 같은 스레드의 다른 태스크가 모두 지연된다. CPU 집약 작업이나 동기 I/O는 반드시 `tokio::task::spawn_blocking`으로 별도 스레드풀에서 실행한다.

```rust
// 금지 — async 내 블로킹 호출
async fn process(path: &str) -> Result<String> {
    std::fs::read_to_string(path)?  // ❌ 런타임 스레드 블로킹
}

// 올바른 방법 — 블로킹 작업을 별도 스레드풀로 위임
async fn process(path: String) -> Result<String> {
    tokio::task::spawn_blocking(move || {
        std::fs::read_to_string(&path)
    })
    .await?
}

// 또는 Tokio async I/O 사용
async fn process(path: &str) -> Result<String> {
    tokio::fs::read_to_string(path).await  // ✅
}
```

블로킹으로 판단하는 기준: 100µs 이상 CPU를 점유하거나, 동기 I/O를 수행하거나, `std::thread::sleep`을 호출하는 경우.

> **출처:** [Tokio Docs — CPU-bound tasks and blocking code](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html)

### 2. async에서는 `tokio::sync`, 동기 코드에서는 `std::sync`를 사용한다

`std::sync::Mutex::lock()`은 스레드를 블로킹한다. async 태스크 안에서 사용하면 런타임 스레드를 점유한다. Tokio의 `tokio::sync::Mutex`는 lock을 기다리는 동안 스레드를 양보한다.

```rust
// async 컨텍스트 — tokio::sync 사용
use tokio::sync::{Mutex, RwLock};

let shared = Arc::new(Mutex::new(HashMap::new()));
let guard = shared.lock().await; // 스레드 블로킹 없이 대기

// 동기 코드 — std::sync 사용 (lock 대기 시간이 매우 짧은 경우)
use std::sync::Mutex;
let cache = Arc::new(Mutex::new(HashMap::new()));
let guard = cache.lock().unwrap();
```

예외: lock을 매우 짧은 시간(서브 마이크로초) 동안만 유지하고 await가 없는 경우, `std::sync::Mutex`가 더 빠르다.

> **출처:** [Tokio Docs — Shared State](https://tokio.rs/tokio/tutorial/shared-state)

### 3. 태스크 간 통신은 채널로 한다

공유 상태 대신 메시지 전달이 데이터 경쟁을 구조적으로 방지한다. Tokio는 용도별 채널을 제공한다.

| 채널 | 용도 | 비고 |
|------|------|------|
| `tokio::sync::mpsc` | 단방향 다대일 | 가장 일반적. 작업 큐, 이벤트 수집 |
| `tokio::sync::oneshot` | 단발 응답 | 요청-응답 패턴 |
| `tokio::sync::broadcast` | 일대다 방송 | 이벤트 팬아웃 |
| `tokio::sync::watch` | 상태 관찰 | 최신 값만 필요한 경우 |

```rust
// mpsc — 워커 풀 패턴
let (tx, mut rx) = tokio::sync::mpsc::channel::<Job>(100);

tokio::spawn(async move {
    while let Some(job) = rx.recv().await {
        process(job).await;
    }
});

tx.send(job).await?;
```

> **출처:** [Tokio Docs — Message Passing](https://tokio.rs/tokio/tutorial/channels)

### 4. 태스크 취소와 타임아웃을 명시적으로 처리한다

Tokio 태스크는 `JoinHandle::abort()`로 취소되거나 `tokio::time::timeout`으로 제한할 수 있다. 취소 지점은 `.await`이다 — await 없이 CPU만 사용하는 루프는 취소되지 않는다.

```rust
use tokio::time::{timeout, Duration};

let result = timeout(Duration::from_secs(5), fetch_data(url))
    .await
    .map_err(|_| AppError::Timeout)?;

// JoinSet으로 여러 태스크 관리
let mut set = tokio::task::JoinSet::new();
for item in items {
    set.spawn(process(item));
}
while let Some(result) = set.join_next().await {
    handle(result?)?;
}
```

> **출처:** [Tokio Docs — tokio::time::timeout](https://docs.rs/tokio/latest/tokio/time/fn.timeout.html)

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| tokio::spawn 태스크 생성 비용 | ~300ns | 스레드 생성(~10µs)보다 30배 저렴 |
| tokio::sync::Mutex lock (비경쟁) | ~50ns | std::sync::Mutex(~10ns)보다 느림 |
| mpsc channel send (비경쟁) | ~50ns | 버퍼 있는 경우 |
| spawn_blocking 스레드풀 크기 기본값 | 512개 | `TOKIO_WORKER_THREADS` 환경변수로 조정 |
| async fn 호출 오버헤드 | ~0ns | 상태 머신 컴파일, 가상 호출 없음 |

---

## 안티패턴

### `async fn main()`에 `#[tokio::main]` 없이 직접 런타임 블록 실행

`tokio::runtime::Runtime::block_on()`을 직접 호출하는 것은 테스트나 특수한 경우에만 사용한다. 일반 앱 진입점은 `#[tokio::main]`을 사용한다.

### async 내에서 `std::thread::sleep` 사용

`std::thread::sleep`은 스레드 블로킹이다. async 코드에서는 반드시 `tokio::time::sleep(Duration).await`를 사용한다.

### 모든 곳에 `Arc<Mutex<T>>` 사용

공유 가변 상태가 필요한지 먼저 검토한다. 채널로 해결되는 경우가 많다. Mutex가 필요하면 lock 범위를 최소화하고, await를 Mutex guard 보유 중에 실행하지 않는다.

### `JoinHandle`을 무시하고 태스크를 fire-and-forget

`tokio::spawn(...)` 반환값을 버리면 태스크 패닉이 조용히 소실된다. 중요한 태스크는 `JoinHandle`을 보관하고 `.await`로 결과를 확인한다.

---

## Gotchas

### async Mutex guard를 `.await` 경계에서 보유하면 컴파일 에러

`MutexGuard`를 들고 `.await`를 호출하면 "future is not Send" 에러가 발생한다. guard를 드롭한 후 await하거나, 별도 블록으로 분리한다.

```rust
// 에러 — guard가 await를 가로지름
let guard = mutex.lock().await;
do_something_async().await; // ❌ guard가 아직 살아있음

// 수정 — guard 먼저 드롭
let value = mutex.lock().await.clone();
drop(guard); // 또는 블록으로 분리
do_something_async().await; // ✅
```

### `spawn_blocking` 클로저는 `'static`을 요구한다

`spawn_blocking`의 클로저는 별도 스레드에서 실행되므로 `'static`이어야 한다. 지역 변수를 캡처하려면 `move` 클로저와 `Arc::clone`을 사용한다.

### `select!`에서 취소된 브랜치의 사이드 이펙트

`tokio::select!`는 먼저 완료된 브랜치를 선택하고 나머지를 취소한다. 취소된 future가 이미 부분 실행된 경우(예: 네트워크 요청 시작) 사이드 이펙트가 남을 수 있다. 취소 안전성이 필요한 작업은 `select!` 외부로 분리한다.

### `#[tokio::test]`를 빠뜨리면 async 테스트가 실행되지 않는다

async 테스트 함수에 `#[test]`만 달면 컴파일은 되지만 async 코드가 실행되지 않는다. 반드시 `#[tokio::test]`를 사용한다.
