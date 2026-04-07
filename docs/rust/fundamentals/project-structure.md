---
title: 프로젝트 구조 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 프로젝트 구조 원칙

Rust 프로젝트는 Cargo workspace로 여러 크레이트를 관리한다. 크레이트 경계가 의존성 규칙을 컴파일 타임에 강제한다 — 도메인이 인프라를 import하면 컴파일이 실패한다. 초기부터 workspace를 구성하면 나중에 분리 비용이 없다.

---

## 원칙

### 1. Cargo workspace로 시작한다

단일 크레이트로 시작해도 되지만, workspace 구조는 초기에 설정하는 것이 이후 리팩토링 비용을 줄인다. 공통 의존성은 workspace 루트 `Cargo.toml`에 선언하여 버전을 일관되게 유지한다.

```toml
# Cargo.toml (workspace 루트)
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
thiserror = "2"
sqlx = { version = "0.8", features = ["postgres", "runtime-tokio-native-tls", "uuid"] }

# crates/domain/Cargo.toml
[dependencies]
thiserror = { workspace = true }
serde = { workspace = true }
```

> **출처:** [Cargo Book — Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)

### 2. 크레이트는 의존 방향 기준으로 분리한다

의존 방향: `app → api → adapters → domain`. `domain`은 외부 인프라 크레이트를 가지지 않는다. 순환 의존은 Cargo가 컴파일 에러로 강제 차단한다.

```
crates/
├── domain/      # 외부 인프라 의존성 없음 (thiserror, serde만 허용)
├── adapters/    # domain만 의존. sqlx, aws-sdk 등 인프라 라이브러리 포함
├── api/         # domain + adapters 의존. axum/actix-web HTTP 레이어
└── app/         # 모든 크레이트 의존. main.rs, DI 조립
```

크레이트가 너무 많아지면 `adapters`를 `adapters-db`, `adapters-storage`처럼 기술 도메인별로 분리한다.

> **출처:** [Cargo Book — Package Layout](https://doc.rust-lang.org/cargo/guide/project-layout.html)

### 3. `mod.rs` 대신 파일명 기반 모듈을 사용한다

Rust 2018 edition부터 `mod.rs` 없이 `foo.rs` + `foo/bar.rs` 구조를 사용할 수 있다. `mod.rs`는 디렉토리 안에 숨어 있어 에디터에서 혼동을 일으킨다. 새 코드는 파일명 기반 방식을 사용한다.

```
# 권장 (Rust 2018+)
src/
├── lib.rs
├── user.rs          # mod user
└── user/
    ├── model.rs     # mod user::model
    └── service.rs   # mod user::service

# 지양 (구형 스타일)
src/
├── lib.rs
└── user/
    ├── mod.rs       # 에디터에서 여러 mod.rs가 혼동을 일으킴
    ├── model.rs
    └── service.rs
```

> **출처:** [Rust Edition Guide — Path clarity](https://doc.rust-lang.org/edition-guide/rust-2018/path-changes.html)

### 4. 가시성은 필요한 최소 범위로 제한한다

기본은 비공개(`pub` 없음). 크레이트 내부 공유는 `pub(crate)`. 상위 모듈에만 공개는 `pub(super)`. 외부 API는 명시적 `pub`. 과도한 `pub`은 내부 구현이 외부에 노출되어 리팩토링을 어렵게 만든다.

```rust
pub struct UserService {           // 외부 공개
    db: Arc<dyn DatabasePort>,     // 비공개 필드
}

pub(crate) fn internal_helper() { ... }  // 크레이트 내부만
pub(super) fn module_helper() { ... }    // 상위 모듈만
```

> **출처:** [Rust Reference — Visibility and Privacy](https://doc.rust-lang.org/reference/visibility-and-privacy.html)

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| 크레이트 분리 기준 | 의존 방향 경계 | 크기가 아닌 의존성 규칙 기준 |
| workspace 멤버 수 권장 | 3~7개 | 그 이상이면 추가 workspace 분리 검토 |
| 크레이트당 public API 수 | 최소화 | `pub use`로 re-export 선별 |
| 빌드 캐시 효율 | 변경된 크레이트만 재빌드 | workspace 분리의 주요 이점 |
| 순환 의존 | 0 (Cargo 강제) | 컴파일 에러로 차단됨 |

---

## 안티패턴

### 모든 타입을 `pub`으로 선언

"일단 다 공개"는 내부 구현이 외부 계약이 되어 리팩토링을 막는다. 기본 비공개에서 시작하고 필요할 때 공개 범위를 넓힌다.

### 단일 크레이트에 모든 코드 집적

크레이트가 하나이면 의존 방향을 컴파일 타임에 강제할 수 없다. 도메인 코드가 인프라 코드를 import해도 경고가 없다. workspace + 크레이트 분리로 아키텍처 규칙을 강제한다.

### `use super::super::super::` 체인

깊은 상대 경로 import는 모듈 구조 변경 시 모두 수정해야 한다. `crate::domain::user::UserId`처럼 절대 경로를 사용하거나, `pub use`로 re-export하여 경로를 단축한다.

### `lib.rs`에 비즈니스 로직 직접 작성

`lib.rs`는 모듈 선언과 re-export만 담당한다. 실제 구현은 하위 모듈 파일에 둔다.

---

## Gotchas

### workspace `Cargo.lock`은 루트에 하나만 존재한다

workspace 멤버 크레이트에 별도 `Cargo.lock`이 생기지 않는다. 루트의 `Cargo.lock`이 전체 workspace를 관리한다. 멤버 크레이트를 독립 배포하는 경우에는 별도 workspace로 분리한다.

### `pub use`로 re-export할 때 API surface가 의도치 않게 넓어진다

`pub use adapters::*`처럼 glob re-export하면 내부 타입이 모두 공개된다. 명시적으로 필요한 타입만 re-export한다.

### `#[cfg(feature = "...")]`로 선택적 의존성을 관리할 때 workspace 주의

workspace 멤버에서 feature를 활성화하려면 루트 `Cargo.toml`의 `workspace.dependencies`에 feature를 미리 나열하거나, 멤버의 `Cargo.toml`에서 직접 feature를 지정한다. 루트에서 feature를 활성화해도 멤버에 자동 전파되지 않는다.

### 크레이트 이름과 파일 시스템 경로는 독립적이다

`crates/domain/Cargo.toml`의 `[package] name = "my-domain"`이 크레이트 이름이다. 디렉토리명과 다를 수 있다. `use domain::...` 대신 `use my-domain::...`이어야 한다면 혼동이 생기므로 이름을 일치시키는 것이 좋다.
