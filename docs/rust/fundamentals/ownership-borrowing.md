---
title: 소유권과 빌림 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 소유권과 빌림 원칙

Rust의 메모리 안전성은 런타임 GC 없이 컴파일 타임 소유권 규칙으로 보장된다. 핵심 규칙 세 가지: 값은 하나의 소유자, 소유자가 스코프를 벗어나면 해제, 불변 빌림과 가변 빌림은 동시에 존재할 수 없다. 이 규칙을 이해하면 불필요한 `.clone()` 없이 안전한 코드를 작성할 수 있다.

---

## 원칙

### 1. 불필요한 `.clone()`을 피한다

`.clone()`은 힙 할당 데이터를 완전히 복사한다. `String`은 평균 ~40ns, `Vec`은 길이에 비례한다. 함수에 소유권이 필요하지 않다면 참조를 넘긴다.

```rust
// 비효율 — 호출마다 String 복사
fn greet(name: String) { println!("Hello, {name}"); }
greet(user.name.clone());

// 효율 — 참조만 빌림
fn greet(name: &str) { println!("Hello, {name}"); }
greet(&user.name);
```

`.clone()` 사용이 정당한 경우: 소유권 이전이 실제로 필요한 경우, `Arc::clone()`처럼 복사 비용이 작은 경우(~5ns atomic op), 명시적 복사 의도를 문서화하는 경우.

> **출처:** [Rust Book Ch.4 — Understanding Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)

### 2. 함수 인자는 `&String` 대신 `&str`을 사용한다

`&String`은 `String`에서만 빌릴 수 있다. `&str`은 `String`, `&str` 리터럴, `String` 슬라이스 모두에서 빌릴 수 있어 더 범용적이다. 같은 이유로 `&Vec<T>` 대신 `&[T]`를, `&PathBuf` 대신 `&Path`를 사용한다.

```rust
fn process(name: &str) { ... }    // ✅ String, &str, 슬라이스 모두 수용
fn process(name: &String) { ... } // ❌ String에만 사용 가능 (Clippy: ptr_arg)
```

> **출처:** [Clippy — `ptr_arg` lint](https://rust-lang.github.io/rust-clippy/master/index.html#ptr_arg)

### 3. 빌림 범위를 최소화한다

빌림이 길수록 가변 접근이 차단되는 범위가 넓어진다. 값이 필요한 시점 직전에 빌리고, 필요가 끝나면 즉시 해제한다. 중간에 소유권을 이전할 필요가 있으면 빌림을 먼저 끝낸다.

```rust
// 빌림 범위 과도
let len = {
    let s = &data.name; // s는 이 블록 안에서만 살아있음
    s.len()
};
data.name.push_str(" Jr."); // ✅ 가변 접근 가능
```

> **출처:** [Rust Book Ch.4.2 — References and Borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)

### 4. lifetime 명시는 컴파일러가 추론 못할 때만 한다

lifetime 생략 규칙(elision rules)이 대부분의 경우를 자동 처리한다. 명시가 필요한 경우: 반환값이 여러 입력 중 하나에서 빌려오는 경우, 구조체가 참조를 필드로 가지는 경우. 불필요한 lifetime 명시는 코드를 복잡하게 만들고 유지보수를 어렵게 한다.

```rust
// lifetime 명시 불필요 — 컴파일러가 추론
fn first_word(s: &str) -> &str { ... }

// 명시 필요 — 반환값이 두 입력 중 하나
fn longer<'a>(x: &'a str, y: &'a str) -> &'a str { ... }

// 구조체 필드에 참조 — lifetime 필수
struct Excerpt<'a> {
    part: &'a str,
}
```

> **출처:** [Rust Book Ch.10.3 — Lifetime Syntax](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)

### 5. `Arc`/`Rc` 사용 기준을 명확히 한다

- `Rc<T>`: 단일 스레드 공유 소유권. 순환 참조는 `Weak<T>`로 방지.
- `Arc<T>`: 멀티 스레드 공유 소유권. atomic ref count로 `Rc`보다 ~3ns 더 비쌈.
- 가변 접근이 필요하면 `Arc<Mutex<T>>` 또는 `Arc<RwLock<T>>` 조합.

```rust
// 멀티 스레드 — Arc 사용
let shared: Arc<Config> = Arc::new(Config::load());
let clone = Arc::clone(&shared); // ~5ns atomic increment
tokio::spawn(async move { use_config(&clone) });
```

> **출처:** [Rust Book Ch.15 — Smart Pointers](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

---

## 수치 기준

| 작업 | 비용 | 비고 |
|------|------|------|
| `&str` 빌림 전달 | ~0ns | 포인터 + 길이만 복사 |
| `String::clone()` (빈 문자열) | ~40ns | 힙 할당 + memcpy |
| `Vec::clone()` (요소 n개) | O(n) | 요소별 clone 호출 |
| `Arc::clone()` | ~5ns | atomic fetch_add |
| `Rc::clone()` | ~2ns | 비원자적 ref count |
| `Mutex::lock()` 비경쟁 | ~10ns | 경쟁 시 수십 µs |

---

## 안티패턴

### 방어적 `.clone()` 남용

컴파일 에러를 피하기 위해 `.clone()`을 추가하는 습관. 에러 메시지를 읽고 소유권 이전 또는 빌림으로 해결하는 것이 올바른 접근이다.

### `&String`을 함수 인자로 사용

`fn process(s: &String)` 대신 `fn process(s: &str)`를 사용하라. Clippy `ptr_arg` lint가 자동 감지한다.

### 구조체에 `&str` 필드를 무분별하게 추가

구조체 lifetime이 복잡해지면 유지보수가 어렵다. 소유한 데이터(`String`)를 필드로 두고, 함수 인자에서만 `&str`을 사용하는 것이 일반적으로 단순하다.

### `Arc<Mutex<T>>`를 기본값으로 사용

공유 가변 상태가 필요한지 먼저 검토하라. 읽기 전용이면 `Arc<T>`, 채널로 메시지를 전달하는 구조라면 Mutex 없이 설계 가능하다.

---

## Gotchas

### NLL(Non-Lexical Lifetimes) 이후에도 빌림 충돌이 발생하는 경우

Rust 2018 이후 NLL로 빌림 범위가 실제 사용 종료 시점으로 단축됐다. 그러나 구조체 필드를 부분적으로 빌릴 때는 컴파일러가 전체 구조체를 빌린 것으로 판단하는 경우가 있다. 이때는 빌림 대상 필드를 지역 변수에 분리하거나, 메서드 대신 함수로 분리한다.

### 반환값 lifetime이 입력과 연결되지 않는 경우

`fn make_greeting() -> &str`은 컴파일 에러다 — 반환되는 참조가 어디서 빌려오는지 알 수 없다. 이때는 `String`을 반환하거나, static 데이터를 반환한다면 `&'static str`을 명시한다.

### `Deref` 강제 변환을 의도치 않게 방해하는 경우

`Box<String>`, `Arc<String>`을 `&str`로 넘길 때 자동 `Deref` 체인(`Box → String → str`)이 동작한다. `&*box_val`처럼 명시적으로 역참조하면 오히려 가독성이 떨어진다. `&box_val[..]`나 그냥 `&box_val`로 Deref 강제 변환에 맡긴다.

### `'static` lifetime을 과도하게 요구하는 설계

tokio `spawn`은 클로저가 `'static`을 요구한다. 이를 해결하기 위해 `Arc::clone`으로 공유하거나, 데이터를 move로 넘긴다. `unsafe` transmute로 lifetime을 지우는 것은 사용 금지.
