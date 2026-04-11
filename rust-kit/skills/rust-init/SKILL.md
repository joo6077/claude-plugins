---
name: rust-init
description: >
  Rust 백엔드 프로젝트를 스캐폴딩한다. Cargo workspace 구조, rust-toolchain.toml,
  디렉토리 레이아웃, 의존성 설정을 생성한다.
  "프로젝트 만들어줘", "rust init", "새 프로젝트", "cargo new",
  "프로젝트 생성", "프로젝트 셋업" 같은 요청 시 트리거.
  기존 프로젝트에 모듈을 추가할 때는 트리거하지 않는다 — rust-feature 사용.
argument-hint: "[project-name]"
user-invocable: true
---

# Gotchas

1. **`cargo init` vs `cargo new` 혼동 금지** — 기존 디렉토리에 초기화하면 `cargo init`, 새 디렉토리를 만들면 `cargo new`.
2. **Edition 2024가 2026 기본값** — 신규 프로젝트는 `edition = "2024"` + `resolver = "3"`을 기본으로 생성한다. Rust 1.85+(2025-02-20)에서 stable 편입되어 2026 현재 실무 표준. 기존 코드 유지가 필요한 경우에만 `edition = "2021"` + `resolver = "2"` 유지. edition 2024는 RPIT capture 규칙 변경·`unsafe extern`·`let` chain·`if let` temporary scope 변경 등을 포함하므로 마이그레이션 시 `cargo fix --edition`으로 전환한다.
3. **타겟 아키텍처 고정 금지** — `.cargo/config.toml`에 `[target.x86_64-unknown-linux-gnu]` 같은 타겟을 고정하면 크로스 플랫폼이 깨진다.
4. **과도한 의존성 금지** — 사용자가 선택한 의존성만 추가한다. "나중에 필요할 수도 있으니" 추가하지 않는다.
5. **Consumer-Owned Port 원칙** — 헥사고날을 채택할 때 포트는 "소비자"가 소유한다. 모듈 A가 모듈 B의 기능이 필요하면 A 내부에 outbound port(trait)를 정의하고, B는 그 trait을 구현하는 adapter를 apps/ Composition Root에서 주입한다. 모듈이 다른 모듈의 `port.rs`를 직접 import하면 그 시점에서 헥사고날이 깨진다. 출처: fit-pal `server/CLAUDE.md` 아키텍처 섹션.
6. **Composition Root 단일화** — 모듈 조립(DI 와이어링)은 `apps/api/src/main.rs`, `apps/worker/src/main.rs` 한 곳에서만 한다. 모듈끼리 직접 인스턴스를 생성하지 말고 `Arc<dyn Port>` trait object로 주입한다. 출처: fit-pal `server/CLAUDE.md` §아키텍처.
7. **workspace lints는 SSOT** — 여러 crate에 같은 clippy 설정을 복붙하지 말고 workspace 루트 `[workspace.lints]`에 한 번만 정의하고 member crate에서는 `[lints] workspace = true` 한 줄로 상속받는다 (RFC 3389, Rust 1.74+).
8. **Domain event + outbox 패턴** — cross-module write 후처리(알림 발송, 감사 로그, 인덱스 동기화)는 직접 호출 대신 **domain event** 발행 + **outbox 테이블** 기록으로 처리한다. 트랜잭션 경계 안에서 write + outbox insert를 원자적으로 실행하고 별도 워커가 outbox를 폴링하여 외부 시스템에 전달한다. 초기 프로젝트 스캐폴딩 시 `modules/*/port.rs`에 `DomainEventPublisher` trait + `apps/worker/` outbox relay 스켈레톤을 함께 만들어 두면 이후 feature 추가가 깔끔해진다. 출처: fit-pal `server/CLAUDE.md` §아키텍처 4번.

# Process

## 1. 프로젝트 이름/설명 확인

사용자에게 프로젝트 이름을 확인한다. 미지정 시 현재 디렉토리 이름 사용.

## 2. 아키텍처 선택

사용자에게 아키텍처를 제안한다:

| 아키텍처 | 적합 규모 | 특징 |
|----------|----------|------|
| `workspace_service` (권장) | 중~대규모 | crates/api + domain + infra 분리. ports/adapters hexagonal 기본 포함 |
| `modular` | 소~중규모 | 단일 크레이트 내 모듈 분리. ports/adapters hexagonal 기본 포함 |
| `flat` | 프로토타입/소규모 | src/main.rs + lib.rs |

## 3. 의존성 선택

체크리스트로 제시 (2026-04 기준 minimum-compatible 최신):

- [x] `axum = "0.8"` (기본) — 0.8 path 파라미터는 `{id}` 문법, `#[async_trait]` 제거됨
- [x] `tokio = { version = "1", features = ["full"] }` (기본)
- [x] `serde = { version = "1", features = ["derive"] }` + `serde_json` (기본)
- [x] `tracing = "0.1"` + `tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }` (기본)
- [x] `thiserror = "2"` (기본, 2.x는 error source/display 매크로 안정화)
- [ ] ORM 택일:
  - `sqlx = { version = "0.8", features = ["postgres", "runtime-tokio", "tls-rustls", "macros", "migrate", "uuid", "chrono"] }` — `query!`/`query_as!` 컴파일 타임 검증, `.sqlx/` 오프라인 캐시 지원
  - `sea-orm = { version = "1.1", features = ["sqlx-postgres", "runtime-tokio-rustls", "macros", "with-chrono", "with-uuid", "with-json", "mock"] }` + `sea-orm-migration = "1.1"` — Entity/ActiveModel/MockDatabase 생태계
- [ ] `utoipa = { version = "5.4", features = ["axum_extras", "uuid"] }` + `utoipa-scalar = { version = "0.3", features = ["axum"] }` (OpenAPI + Scalar UI)
- [ ] `jsonwebtoken = { version = "10", features = ["rust_crypto"] }` (JWT)
- [ ] `tower-http = { version = "0.6", features = ["cors", "trace", "request-id", "timeout", "compression-gzip", "limit"] }`
- [ ] `rust-i18n = "3"` (다국어) 또는 `fluent` (복잡한 pluralization)
- [ ] `tracing-opentelemetry = "0.32"` + `opentelemetry = "0.31"` + `opentelemetry-otlp = { version = "0.31", features = ["trace", "metrics", "grpc-tonic"] }` (OTel 연동)
- [ ] 개발 의존성: `mockall = "0.13"` (`#[automock]` trait mock), `serial_test = "3"` (통합 테스트 격리)

> Context7 또는 공식 릴리스 노트로 상위 minor 버전이 이미 나왔는지 반드시 확인한다. 본 목록은 2026-04 기준 실무 검증 조합이며, 프로젝트 착수 시점 기준으로 재확인이 필요하다.

## 4. 구조 생성

선택한 아키텍처에 따라 파일/디렉토리를 생성한다.

### workspace_service 구조

```text
{project}/
├── Cargo.toml              # [workspace] members = ["apps/*", "modules/*", "shared/*"], resolver = "3", [workspace.lints]
├── rust-toolchain.toml     # channel = "1.88.0" (또는 "stable"), components = ["rustfmt", "clippy"], profile = "default"
├── deny.toml               # cargo-deny v2 (advisories / licenses.allow / bans / sources)
├── .cargo/config.toml
├── .env.example
├── apps/                   # 엔트리포인트 + Composition Root (비즈니스 로직 금지)
│   ├── api/
│   │   ├── Cargo.toml      # [lints] workspace = true
│   │   └── src/
│   │       ├── main.rs     # 모듈 조립의 유일한 장소
│   │       └── routes.rs
│   └── worker/
│       ├── Cargo.toml
│       └── src/main.rs
├── modules/                # 도메인별 기능 (Consumer-Owned Port)
│   └── user/
│       ├── Cargo.toml
│       └── src/
│           ├── lib.rs
│           ├── port.rs     # 이 모듈이 "소비"하는 outbound port trait
│           ├── service.rs  # 포트 구현 + 비즈니스 로직
│           └── dto.rs
└── shared/                 # 횡단 관심사 (도메인 로직 금지)
    ├── db/
    ├── error/
    ├── config/
    └── telemetry/
```

**참고** — 이 레이아웃은 fit-pal `/Users/jackson/Hub/10_Dev/fit-pal/server` 실무 프로젝트 구조(apps/api + apps/worker + modules/* + shared/*)를 기반으로 한다. 기존 `crates/api + crates/domain + crates/infra` 레이아웃도 유효하나, 모듈 경계가 뚜렷한 중대규모 프로젝트에서는 `modules/*` 레이아웃이 의존 방향을 더 명확히 강제한다 (apps → modules ← shared).

### modular 구조

```text
{project}/
├── Cargo.toml
├── rust-toolchain.toml
├── .cargo/config.toml
├── .env.example
├── src/
│   ├── main.rs
│   ├── api/
│   │   ├── mod.rs
│   │   ├── router.rs
│   │   └── handlers/
│   │       └── mod.rs
│   ├── domain/
│   │   ├── mod.rs
│   │   ├── models/
│   │   │   └── mod.rs
│   │   ├── services/
│   │   │   └── mod.rs
│   │   └── ports/          # 서비스 trait 정의 (hexagonal)
│   │       └── mod.rs
│   └── infra/
│       ├── mod.rs
│       ├── adapters/       # trait impl (hexagonal)
│       │   └── mod.rs
│       └── db/
│           └── mod.rs
├── migrations/
└── tests/
```

### flat 구조

```text
{project}/
├── Cargo.toml
├── rust-toolchain.toml
├── src/
│   ├── main.rs
│   └── lib.rs
└── tests/
```

## 4a. `Cargo.toml` 워크스페이스 루트 템플릿 (workspace_service)

```toml
[workspace]
resolver = "3"
members = ["apps/*", "modules/*", "shared/*"]

[workspace.package]
version = "0.1.0"
edition = "2024"
publish = false

[workspace.dependencies]
# 각 crate에서 `tokio.workspace = true` 로 참조
tokio = { version = "1", features = ["full"] }
axum = "0.8"
tower-http = { version = "0.6", features = ["cors", "trace", "request-id", "timeout", "compression-gzip", "limit"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "2"
anyhow = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
utoipa = { version = "5.4", features = ["axum_extras", "uuid"] }
utoipa-scalar = { version = "0.3", features = ["axum"] }

# ── 워크스페이스 공통 린트 (SSOT, RFC 3389) ──
[workspace.lints.rust]
unsafe_code = "forbid"

[workspace.lints.rustdoc]
broken_intra_doc_links = "deny"
bare_urls = "deny"

[workspace.lints.clippy]
all = { level = "deny", priority = -1 }
correctness = { level = "deny", priority = -1 }
pedantic = { level = "deny", priority = -1 }
suspicious = { level = "deny", priority = -1 }
# pedantic 노이즈 큰 것 allow
module_name_repetitions = "allow"
must_use_candidate = "allow"
missing_errors_doc = "allow"
missing_panics_doc = "allow"
# 추가 deny (2026 fit-pal 실무 세트)
needless_pass_by_value = "deny"
redundant_clone = "deny"
cloned_instead_of_copied = "deny"
inefficient_to_string = "deny"
large_futures = "deny"

[profile.dev]
debug = "line-tables-only"
split-debuginfo = "packed"
```

Member crate `Cargo.toml`은 이 `[workspace.lints]`를 한 줄로 상속한다:

```toml
[package]
name = "fitpal-api"
version.workspace = true
edition.workspace = true
publish.workspace = true

[dependencies]
axum.workspace = true
tokio.workspace = true

[lints]
workspace = true
```

## 4b. `rust-toolchain.toml` 템플릿

```toml
[toolchain]
channel = "1.88.0"
components = ["rustfmt", "clippy"]
profile = "default"
```

`channel`은 `"stable"` 또는 `"1.88.0"` 같은 명시 버전 중 선택. 팀 환경 정합성이 중요하면 명시 버전을 권장한다 (fit-pal 실무 기준).

## 4c. `deny.toml` 템플릿 (cargo-deny v2 형식)

```toml
[advisories]
# v2: vulnerability, notice 필드 제거됨 (항상 에러)
ignore = []

[licenses]
# v2: allow 목록에 없으면 전부 거부
allow = [
    "MIT",
    "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "Unicode-3.0",
    "Zlib",
    "MPL-2.0",
    "BSL-1.0",
    "0BSD",
]

[licenses.private]
ignore = true

[bans]
multiple-versions = "warn"
wildcards = "allow"
highlight = "all"

[sources]
unknown-registry = "deny"
unknown-git = "warn"
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
allow-git = []
```

설치: `cargo install cargo-deny --locked`. 실행: `cargo deny check` (CI preflight에 포함).

## 5. 초기 컴파일 확인

`cargo build`를 실행하여 프로젝트가 정상 컴파일되는지 확인한다.
추가로 `cargo clippy --workspace --all-targets -- -D warnings` 와 `cargo fmt --all -- --check`, `cargo deny check`도 함께 실행해 초기 상태를 green baseline으로 고정한다.

## After Creation

1. 생성된 파일/디렉토리 목록 출력.
2. 다음 단계 안내:
   > - API 엔드포인트 추가: `/rust-api`
   > - DB 모델 추가: `/rust-model`
   > - 인증 설정: `/rust-auth`

# References

- references/project-detection.md
- docs/rust/fundamentals/project-structure.md
