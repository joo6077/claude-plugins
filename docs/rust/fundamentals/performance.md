---
title: 성능 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 성능 원칙

Rust는 기본적으로 빠르지만 잘못된 패턴은 불필요한 힙 할당과 복사를 유발한다. 최적화는 측정 후 수행한다 — 추측 기반 최적화는 코드 복잡도를 높이고 실제 병목과 다를 수 있다. `cargo flamegraph`와 `criterion` 벤치마크로 병목을 확인한 뒤 수정한다.

---

## 원칙

### 1. 불필요한 힙 할당을 줄인다

힙 할당(`Box`, `Vec`, `String` 생성)은 시스템 콜 수준의 비용이다(~50ns). 루프 안에서 반복 할당하거나 크기를 알고 있는데도 동적 할당하면 성능에 영향을 준다.

```rust
// 비효율 — 루프마다 String 할당
for item in items {
    let s = format!("prefix_{}", item.name); // 매 반복 힙 할당
    process(&s);
}

// 효율 — 버퍼 재사용
let mut buf = String::with_capacity(64);
for item in items {
    buf.clear();
    write!(&mut buf, "prefix_{}", item.name).unwrap();
    process(&buf);
}
```

> **출처:** [Rust Performance Book — Heap Allocations](https://nnethercote.github.io/perf-book/heap-allocations.html)

### 2. 크기를 알면 `Vec::with_capacity`로 사전 할당한다

`Vec::new()`에 원소를 push하면 용량 초과 시 2배 재할당이 발생한다. 원소 수를 알거나 추정할 수 있으면 `with_capacity`로 재할당을 방지한다.

```rust
// 재할당 발생 가능
let mut results = Vec::new();
for item in source.iter() {
    results.push(transform(item));
}

// 재할당 없음
let mut results = Vec::with_capacity(source.len());
for item in source.iter() {
    results.push(transform(item));
}

// 또는 Iterator::collect — 크기 힌트를 자동 활용
let results: Vec<_> = source.iter().map(transform).collect();
```

> **출처:** [Rust Performance Book — Vec](https://nnethercote.github.io/perf-book/vec.html)

### 3. Iterator 체이닝은 collect 없이 지연 평가한다

`collect()`는 새 컬렉션을 힙에 할당한다. 중간 결과가 필요 없으면 iterator 체인을 끝까지 이어서 한 번에 처리한다.

```rust
// 중간 Vec 할당 발생
let filtered: Vec<_> = items.iter().filter(|x| x.active).collect(); // 힙 할당
let names: Vec<_> = filtered.iter().map(|x| &x.name).collect();     // 힙 할당

// 지연 평가 — collect 한 번
let names: Vec<_> = items.iter()
    .filter(|x| x.active)
    .map(|x| &x.name)
    .collect();

// 소비만 할 경우 collect 불필요
items.iter()
    .filter(|x| x.active)
    .for_each(|x| process(x));
```

> **출처:** [Rust Docs — Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html)

### 4. `criterion`으로 벤치마크를 측정하고 최적화한다

직관 기반 최적화 전에 반드시 측정한다. `criterion`은 통계적으로 유의미한 결과를 제공하며, 워밍업과 반복 실행을 자동 처리한다.

```toml
# Cargo.toml
[[bench]]
name = "user_processing"
harness = false

[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
```

```rust
// benches/user_processing.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_validate_email(c: &mut Criterion) {
    c.bench_function("validate_email valid", |b| {
        b.iter(|| validate_email(black_box("user@example.com")))
    });
}

criterion_group!(benches, bench_validate_email);
criterion_main!(benches);
```

```bash
cargo bench                          # 전체 벤치마크 실행
cargo bench -- user_processing       # 특정 벤치마크만
cargo bench -- --save-baseline main  # 기준선 저장
```

> **출처:** [criterion — Getting Started](https://bheisler.github.io/criterion.rs/book/getting_started.html)

### 5. `release` 빌드로 성능을 측정한다

`cargo run`(debug 빌드)은 최적화가 없어 release 빌드보다 10~100배 느릴 수 있다. 성능 측정과 프로파일링은 항상 `--release`로 실행한다.

```bash
cargo build --release
cargo bench                    # 자동으로 release 빌드 사용
cargo flamegraph --release     # 프로파일링
```

`Cargo.toml`에서 release 프로파일 최적화 수준을 조정할 수 있다:

```toml
[profile.release]
opt-level = 3       # 기본값. 최대 최적화
lto = true          # Link-Time Optimization (빌드 시간 증가, 바이너리 성능 향상)
codegen-units = 1   # 병렬 코드 생성 비활성화 (빌드 느림, 최적화 향상)
```

> **출처:** [Cargo Book — Profiles](https://doc.rust-lang.org/cargo/reference/profiles.html)

---

## 수치 기준

| 작업 | 비용 | 비고 |
|------|------|------|
| 힙 할당 (`malloc`) | ~50ns | OS/할당자에 따라 다름 |
| `Vec` 재할당 | O(n) 복사 | `with_capacity`로 방지 |
| Iterator `map/filter` (지연) | ~0ns 추가 | collect 시점에만 실행 |
| `String::new()` + `push_str` vs `format!` | `format!`이 ~2× 느림 | 루프 내 문자열 조합은 write! + 버퍼 재사용 |
| debug vs release 빌드 속도 차이 | 10~100× | 최적화 수준 차이 |
| LTO 효과 | 5~20% 성능 향상 | CI 빌드 시간과 트레이드오프 |

---

## 안티패턴

### 루프 내 `String::new()` 반복 생성

문자열을 루프마다 새로 만들면 매 반복 힙 할당이 발생한다. `with_capacity`로 미리 할당하거나 버퍼를 재사용한다.

### `collect()` 후 즉시 iterate

```rust
items.iter().map(f).collect::<Vec<_>>().iter().for_each(g)
// → items.iter().map(f).for_each(g)
```

중간 `Vec`이 필요 없으면 체인을 이어서 한 번에 처리한다.

### debug 빌드로 성능 측정

debug 빌드 결과로 최적화 여부를 판단하는 것은 의미가 없다. 항상 `--release` 빌드로 측정한다.

### `black_box` 없이 벤치마크 작성

컴파일러가 벤치마크 함수 호출을 최적화로 제거할 수 있다. `criterion::black_box`로 입력을 감싸 최적화를 방지한다.

### 측정 없이 최적화

"아마 느릴 것 같아서" 코드를 복잡하게 만드는 것은 유지보수 비용만 늘린다. `criterion` 벤치마크로 병목을 확인하고, 실제로 느린 곳만 최적화한다.

---

## Gotchas

### `criterion` 0.4와 0.5는 API가 다르다

`criterion` 0.5에서 `BenchmarkGroup`의 일부 메서드 시그니처가 변경됐다. `Cargo.toml`의 버전을 명시하고, 업그레이드 시 변경 사항을 확인한다.

### `flamegraph`는 debug 심볼이 필요하다

`cargo flamegraph`로 프로파일링하려면 release 빌드에 debug 심볼이 있어야 한다:

```toml
[profile.release]
debug = 1  # 심볼 포함, 성능 영향 없음
```

### `lto = true`는 CI 빌드 시간을 크게 늘린다

LTO는 링크 단계에서 전체 코드베이스를 최적화한다. 프로덕션 릴리스에만 활성화하고, 개발/CI에는 기본 설정을 유지한다. `profile.release-lto`처럼 별도 프로파일로 분리할 수 있다.

### iterator `size_hint`가 잘못되면 `collect` 재할당이 발생한다

커스텀 iterator를 구현할 때 `size_hint()`를 정확히 구현하지 않으면 `collect` 시 재할당이 발생한다. 크기를 알면 반드시 `size_hint`를 구현한다.
