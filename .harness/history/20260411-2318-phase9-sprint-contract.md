# Sprint Contract — Phase 9 Kaizen Research Mode (rust-kit)

Feature: rust-kit 16 스킬 + rust-reviewer 에이전트 + references 2026 최신 Rust 2024/Axum 0.8/SQLx 0.8/tonic 0.13/SeaORM 1.1/Clippy 생태계 트렌드 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1~8 완료 (commit 4587154 → 71835bb). Phase 9는 rust-kit 플러그인의 16개 스킬(rust-init, rust-feature, rust-api, rust-model, rust-service, rust-auth, rust-middleware, rust-grpc, rust-test, rust-docker, rust-error, rust-l10n, rust-run, rust-build, rust-preflight, rust-audit), `agents/rust-reviewer.md`, 그리고 플러그인 수준 references (`rust-kit/references/project-detection.md`, `rust-kit/skills/rust-audit/references/audit-criteria.md`)를 2026 Rust 생태계 현실에 맞춰 갱신한다.

데이터 풀 §5 validate-plugin 스냅샷 — rust-kit v0.1.0, 16 skills + 1 agent, V1~V7 OK. 회귀 금지 기준선.

§2 Hub 외부 프로젝트 피드백: `/Users/jackson/Hub/10_Dev/fit-pal/server` 는 **실무 운영 중인 Rust 2024 + Axum 0.8.8 + SeaORM 1.1.19 모듈러 모놀리스**로, 본 Phase 9의 ground truth 출처다. `/Users/jackson/Hub/10_Dev/fit-pal/.harness/sprint-feedback.md` (Monorepo Makefile APPROVE iter 2, 33/33)은 Rust preflight 명령 체계(`cargo clippy --workspace --all-targets -- -D warnings`, `cargo fmt --all -- --check`, `APP_ENV`/`DATABASE_URL` 환경변수 주입)를 검증한다.

외부 리서치 (2026-04-11):

- **Rust 2024 Edition**: Rust 2024는 `stable` 1.85 (2025-02-20)에 편입되어 2026-04 현재 **거의 모든 신규 프로젝트의 기본 edition**. `edition = "2024"`는 `resolver = "3"`를 자동 활성화한다. 주요 마이그레이션 포인트: (1) **`let` chain**이 stable (`if let Some(a) = x && let Some(b) = y`), (2) **RPIT capture rules**: `impl Trait` 반환값이 기본적으로 모든 in-scope lifetime을 capture하도록 변경 (`+ use<>`로 명시 필요한 경우 존재), (3) **`unsafe extern`**: `extern "C" { ... }` 블록 전체를 `unsafe extern`으로 감싸야 함, (4) **`if let` temporary scope** 변경 (drop 순서 영향 가능), (5) **`Future`/`IntoFuture` prelude 포함**. Rust 1.88 (2025-06-26)까지 반영 필요. `rust-toolchain.toml` 예시: `channel = "1.88.0"` (fit-pal 실무 기준) 또는 `stable`. ([Rust 2024 edition guide](https://doc.rust-lang.org/edition-guide/rust-2024/index.html), [Rust 1.85 블로그](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0/), [Rust 1.88 블로그](https://blog.rust-lang.org/2025/06/26/Rust-1.88.0/))

- **Axum 0.8 breaking changes (2024-12-01 릴리스)**: (1) **Path 파라미터 문법**: `:id` colon 문법 **완전 제거**, **`{id}` 중괄호 문법만 지원** — `.route("/users/:id", ...)` → `.route("/users/{id}", ...)`. 모든 기존 라우트 마이그레이션 필요. (2) **async fn in traits native 채택**: `#[async_trait]`가 `FromRequest`, `FromRequestParts`, `Handler` 등에서 **제거됨**. 직접 trait 구현 시 `async fn` 사용. axum이 재export하던 `axum::async_trait`도 deprecated. (3) **`Handler::call`이 `IntoFuture`** 기반으로 변경. (4) **Extractor 타입 파라미터 순서** 일부 완화. (5) `matchit` 라우터 2.x로 업그레이드 — 충돌 감지/역추적 개선. ([Axum 0.8 changelog](https://github.com/tokio-rs/axum/blob/main/axum/CHANGELOG.md), [Axum 0.8 announcement](https://tokio.rs/blog/2024-12-01-announcing-axum-0-8-0), [path parameter matchit2 PR](https://github.com/tokio-rs/axum/pull/2945))

- **SeaORM 1.1.x vs SQLx**: fit-pal은 **SeaORM 1.1.19** 사용 (SQLx 아님). 2025-2026 Rust 백엔드 실무에서 **SQLx와 SeaORM은 상호 배타가 아닌 병렬 옵션**이다. rust-kit은 현재 SQLx만 가정 — SeaORM 패턴 추가 필요. SeaORM 1.1 (2024-10 + 패치)은 (1) `ActiveModel::insert().exec_with_returning()`, (2) `ConnectionTrait` 제네릭으로 transaction/connection 통합, (3) **`MockDatabase`** 네이티브 단위 테스트 (Docker 불필요), (4) `sea-orm-migration`로 마이그레이션 (sqlx-cli 아님), (5) `with-chrono`/`with-uuid`/`with-json` feature, (6) `runtime-tokio-rustls` 기본. ([SeaORM 1.1 docs](https://www.sea-ql.org/SeaORM/docs/), [SeaORM migration](https://www.sea-ql.org/sea-orm-tutorial/ch01-09-migration.html), [SeaORM MockDatabase](https://www.sea-ql.org/SeaORM/docs/write-test/mock/), [ActiveModel](https://www.sea-ql.org/SeaORM/docs/basic-crud/insert/))

- **SQLx 0.8 (2024-07-22 릴리스, 0.8.x 2026-Q1 현재 0.8.x 계열 유지)**: (1) `.sqlx/` 오프라인 캐시는 0.7부터 사이드카 방식 — 0.8도 동일. (2) **runtime feature 재편**: `runtime-tokio` + `tls-rustls` 조합. `runtime-tokio-native-tls`/`runtime-tokio-rustls` 레거시 네이밍은 alias만 유지. (3) `query_as!`는 여전히 compile-time 검증. (4) **PgConnection::in_transaction()** 헬퍼 추가. (5) `sqlx-cli` `database drop/create/reset` 자동화. ([SQLx 0.8 announcement](https://github.com/launchbadge/sqlx/blob/main/CHANGELOG.md), [SQLx offline](https://docs.rs/sqlx/latest/sqlx/macro.query.html#offline-mode))

- **Tonic 0.13 (2025 릴리스)**: (1) prost 0.13 동반. (2) `tonic-build` API는 `configure().compile_protos(&[...], &[...])` 유지. (3) `#[tonic::async_trait]` 여전히 권장 — Tonic의 `Server` trait이 dyn 호환을 유지하기 위해 async_trait 매크로 필요. native async fn in trait는 tonic 내부 코드 생성 시 점진적으로 migration 중이지만, **사용자 impl은 여전히 `#[tonic::async_trait]` 표준**. (4) streaming은 `type XxxStream = Pin<Box<dyn Stream<...> + Send>>` + `ReceiverStream` 패턴 유지. (5) `tonic-health`/`tonic-reflection`이 별도 크레이트로 분리. ([tonic 0.13 CHANGELOG](https://github.com/hyperium/tonic/blob/master/CHANGELOG.md), [tonic async_trait 논의](https://github.com/hyperium/tonic/issues/1242))

- **Clippy 최신 lint (rustc 1.88 기준, 2025-2026)**: **pedantic 기본 deny**는 fit-pal 패턴 (`workspace.lints.clippy.pedantic = { level = "deny", priority = -1 }`). 2026 실무 권장 lint 패키지: `all`/`correctness`/`pedantic`/`suspicious` 모두 deny, 노이즈가 큰 일부만 allow (`module_name_repetitions`, `must_use_candidate`, `missing_errors_doc`, `missing_panics_doc`). 명시적 deny: `needless_pass_by_value`, `redundant_clone`, `cloned_instead_of_copied`, `inefficient_to_string`, **`large_futures`** (Send async recursion 비용). `unsafe_code = "forbid"` workspace 레벨. `broken_intra_doc_links = "deny"`. ([Clippy lints index](https://rust-lang.github.io/rust-clippy/master/), [large_futures lint](https://rust-lang.github.io/rust-clippy/master/#large_futures), [workspace lints RFC](https://rust-lang.github.io/rfcs/3389-manifest-lint.html))

- **SeaORM MockDatabase + mockall 테스트 패턴**: 2026 Rust 백엔드 단위 테스트 표준은 "**trait 추상화 + mockall `#[automock]` + SeaORM MockDatabase 조합**". 외부 HTTP 클라이언트, OIDC, 이메일, FCM 등은 `Arc<dyn Port>` trait object로 라우터 상태에 주입, 테스트 시 mock 구현체로 교체. DB 레이어는 SeaORM `MockDatabase`로 SQL 실행 없이 단위 테스트. 통합 테스트는 `serial_test` + TRUNCATE 격리로 crate `tests/` 디렉토리에. ([SeaORM mock](https://www.sea-ql.org/SeaORM/docs/write-test/mock/), [mockall automock](https://docs.rs/mockall/latest/mockall/attr.automock.html), [serial_test](https://docs.rs/serial_test/))

- **utoipa 5.4 + Scalar UI**: fit-pal은 `utoipa = "5.4"` + `utoipa-scalar = "0.3"`. 2026 Rust OpenAPI 표준 조합은 **utoipa (매크로 기반 스펙 생성) + Scalar UI (Swagger UI 대체 모던 UI)**. `#[utoipa::path(...)]` + `#[derive(ToSchema)]` + `#[derive(OpenApi)]` 상속 구조. ApiDoc struct의 `paths(...)` / `components(schemas(...))`에 등록. Scalar mount: `.route("/docs", Scalar::with_url("/docs/openapi.json", ApiDoc::openapi()))`. ([utoipa 5.4](https://docs.rs/utoipa/5.4/), [utoipa-scalar](https://docs.rs/utoipa-scalar/), [Scalar API reference](https://scalar.com/))

- **Cargo workspace lints + deny.toml + rust-toolchain.toml**: 2026 프로젝트 스캐폴딩 삼종 세트. (1) **`[workspace.lints]`** — workspace 루트에서 모든 member crate의 clippy/rustc/rustdoc lint를 SSOT로 관리. member crate에서는 `[lints] workspace = true` 한 줄만 작성. (2) **`deny.toml`** — `cargo-deny`의 v2 형식 (advisories `vulnerability`/`notice` 필드 제거), `licenses.allow` allow-list 방식, `bans.multiple-versions = "warn"`, `sources.unknown-registry = "deny"`. (3) **`rust-toolchain.toml`** — `channel = "1.88.0"` 또는 `stable`, `components = ["rustfmt", "clippy"]`, `profile = "default"`. ([workspace lints RFC 3389](https://rust-lang.github.io/rfcs/3389-manifest-lint.html), [cargo-deny v2](https://embarkstudios.github.io/cargo-deny/checks/advisories/cfg.html), [rust-toolchain.toml](https://rust-lang.github.io/rustup/overrides.html#the-toolchain-file))

- **tracing-opentelemetry 0.32 + OTel 0.31**: fit-pal 기준 `tracing = "0.1.44"`, `tracing-subscriber = "0.3.23"`, `tracing-opentelemetry = "0.32.1"`, `opentelemetry = "0.31.0"`, `opentelemetry_sdk = "0.31.0"`, `opentelemetry-otlp = "0.31.0"`. 2026 Rust observability 표준은 **tracing layer + OTel otlp exporter + Grafana LGTM**. `RUST_LOG` env + `EnvFilter` + `fmt` layer + `OpenTelemetryLayer` 조합. ([tracing-opentelemetry](https://docs.rs/tracing-opentelemetry/), [opentelemetry-otlp](https://docs.rs/opentelemetry-otlp/0.31/))

- **Makefile / justfile 환경변수 주입 패턴**: fit-pal 검증 패턴은 (1) `APP_ENV=dev RUST_LOG=debug cargo run -p <crate>`, (2) `DATABASE_URL=postgres://user:pass@host:port/db cargo run -p migration`, (3) `cargo clippy --workspace --all-targets -- -D warnings`, (4) `cargo fmt --all -- --check`, (5) Makefile 타겟 `server-run`/`server-test`/`server-lint`/`server-fmt`/`server-fmt-fix`/`server-migrate`/`server-preflight`. `.PHONY` 선언 필수. Makefile 없이 직접 cargo 호출 시 환경변수 누락. `justfile` 대안도 동일 패턴. (fit-pal `.harness/sprint-feedback.md` 33/33 APPROVE 근거)

## 범위

- rust-kit/skills/*/SKILL.md (16개)
- rust-kit/agents/rust-reviewer.md
- rust-kit/references/project-detection.md
- rust-kit/skills/rust-audit/references/audit-criteria.md

## 수정 금지

- harness/**, flutter-toolkit/**, design-kit/**, backend-kit/**, infra-kit/**, react-kit/** (Phase 1~8/10)
- rust-kit/.claude-plugin/plugin.json (버전은 Final Phase에서)
- .harness/*.yaml, .meta/*, evals/*, history/*, .superpowers/*, scripts/*, docs/rust/** (리서치 소스)
- docs/index.html, docs/rust-kit.html, backend-kit.html 등 plugin docs pages (Final Phase 대상)

## Conditions

### R (Research & Rust 2024 Edition, 4개)

- [ ] R-01: **rust-init** Gotchas가 `edition = "2024"` + `resolver = "3"` 기본 채택을 명시하고, 2021/2024 매트릭스 제공 (기존 Gotcha #2는 2021→2024 기본 전환으로 갱신). workspace_service/modular 구조 예시 `Cargo.toml`이 `edition = "2024"` 샘플 포함.
- [ ] R-02: **rust-init** Gotchas 또는 Process에 `rust-toolchain.toml` 생성 절차가 `channel`/`components`/`profile` 3요소 명시. 예시 `channel = "1.88.0"` 또는 `stable` 2 옵션.
- [ ] R-03: **rust-init** Process에 **`[workspace.lints]`** SSOT 패턴 가이드 추가 (rust/rustdoc/clippy 3 네임스페이스, pedantic deny + 노이즈 allow 샘플, `[lints] workspace = true` member 규약). fit-pal 실무 세트를 레퍼런스로 인용.
- [ ] R-04: **rust-init** Process에 **`deny.toml`** v2 형식 초기 템플릿 생성 단계 추가 (advisories v2, licenses.allow allow-list, bans.multiple-versions="warn", sources.unknown-registry="deny").

### A (Axum 0.8 breaking changes, 5개)

- [ ] A-01: **rust-api** Gotchas에 Axum 0.8 **path parameter 문법** breaking change 명시 (`:id` deprecated → `{id}` only). 본문 코드 예시 `.route("/users/:id", ...)` → `.route("/users/{id}", ...)` 전부 교체.
- [ ] A-02: **rust-api** Gotchas에 Axum 0.8 **`#[async_trait]` 제거 — `FromRequest`/`FromRequestParts`는 native async fn 사용** 원칙 추가. `axum::async_trait`은 deprecated로 명시.
- [ ] A-03: **rust-auth** extractor 코드 예시에서 `#[async_trait]` + `use axum::async_trait` 제거. `impl<S> FromRequestParts<S> for AuthUser` 블록을 native `async fn from_request_parts` 형태로 교체. Gotchas에 Axum 0.8 이주 포인트 명시.
- [ ] A-04: **rust-middleware** 본문 예시 경로가 `:id` 스타일이면 `{id}`로 교체. Gotchas에 tower-http 0.6.x 버전대 명시 + `request-id`/`compression-gzip`/`limit`/`trace` feature 조합.
- [ ] A-05: **rust-api** Process에서 라우터 예시가 Axum 0.8 `Router::with_state` + `Arc<dyn Trait>` state 주입 패턴을 유지하되 path 예시를 `{id}`로 통일.

### D (Database layer — SQLx 0.8 + SeaORM 1.1, 4개)

- [ ] D-01: **rust-model** 상단에 **ORM 선택 분기** 섹션 추가 — HAS_SQLX 또는 HAS_SEAORM 감지 후 각각의 구현 경로 제시. SeaORM 경로는 fit-pal 패턴(Entity/ActiveModel/Repository trait/ConnectionTrait 제네릭) 명시.
- [ ] D-02: **rust-model** SQLx 경로 Gotchas에 SQLx 0.8 runtime feature 최신 조합 (`runtime-tokio` + `tls-rustls` 또는 `runtime-tokio-rustls` alias) 명시.
- [ ] D-03: **rust-model** SeaORM 경로가 `sea-orm-migration` CLI 사용법과 `Migrator::up(&db, None).await` 런타임 마이그레이션 방식 2종 명시. SQLx 경로는 기존 `cargo sqlx migrate run` + `.sqlx/` 오프라인 캐시 유지.
- [ ] D-04: **rust-test** DB 통합 테스트 섹션에 **SeaORM MockDatabase** 분기 추가 (SQLx `#[sqlx::test]`와 병렬). fit-pal `test_support` 모듈 + `serial_test` + TRUNCATE 격리 패턴 참조.

### H (Hexagonal / Consumer-Owned Port, 3개)

- [ ] H-01: **rust-init**/**rust-feature** Gotchas에 **Consumer-Owned Port** 원칙 명시 — "포트는 소비자가 소유한다. 모듈이 다른 모듈의 port.rs를 직접 import하면 안 된다". cross-module write 후처리는 **domain event + outbox**로 한다는 원칙 추가.
- [ ] H-02: **rust-api**/**rust-service** Gotchas에 **포트에서 인프라 타입 제거** 원칙 명시 — `DatabaseTransaction`, SeaORM model, `PgPool`, `sqlx::Error` 등 인프라 타입을 포트 trait 시그니처에 노출 금지. DTO/도메인 이벤트만 주고받는다.
- [ ] H-03: **rust-feature**/**rust-api** Gotchas에 **Composition Root 단일화** 원칙 명시 — 모듈 조립은 `apps/api/src/main.rs` 또는 `apps/worker/src/main.rs` 한 곳에서만. 모듈끼리 직접 생성 금지, `Arc<dyn Port>` trait object 주입.

### T (Tonic 0.13 + Testing + Tooling, 4개)

- [ ] T-01: **rust-grpc** 의존성 버전을 `tonic = "0.13"`, `prost = "0.13"`, `tonic-build = "0.13"` 수준으로 업데이트. Gotchas에 `#[tonic::async_trait]` 유지 원칙 명시 (tonic 사용자 impl은 여전히 매크로 사용).
- [ ] T-02: **rust-test** Gotchas에 SeaORM MockDatabase 패턴과 mockall `#[automock]` 병행 사용법 + fit-pal `test_support` 모듈 컨벤션 명시. `#[tokio::test(flavor = "multi_thread")]` 사용 기준 명확화.
- [ ] T-03: **rust-run**/**rust-preflight** Gotchas에 fit-pal 검증된 Makefile 타겟 (`server-run`, `server-test`, `server-lint`, `server-fmt`, `server-fmt-fix`, `server-migrate`, `server-preflight`) 예시 + `APP_ENV`/`RUST_LOG`/`DATABASE_URL` 환경변수 주입 필수 원칙 추가.
- [ ] T-04: **rust-run** `audit` 서브커맨드에 `cargo deny check` v2 형식(`advisories`/`licenses`/`bans`/`sources`) 기본 실행 포함 명시. `cargo-audit` 미설치 skip 정책은 유지.

### C (Clippy lints + error patterns, 4개)

- [ ] C-01: **rust-audit** `audit-criteria.md`에 **Clippy pedantic 2026 기준** 카테고리 행 추가 — `needless_pass_by_value`, `redundant_clone`, `cloned_instead_of_copied`, `inefficient_to_string`, `large_futures` 등 fit-pal workspace lint 세트 명시. 출처는 "Clippy lints index + fit-pal workspace.lints".
- [ ] C-02: **rust-audit** `audit-criteria.md` Security 행에 `unsafe_code = "forbid"` 원칙 + `unwrap()`/`expect()`은 main 초기화와 테스트에서만 허용(FAIL 판정 조건 완화) 명시. 출처 fit-pal CLAUDE.md.
- [ ] C-03: **rust-error** Gotchas에 **`anyhow::Error` in domain layer 금지** 원칙 추가 — domain layer에는 `thiserror` 구체 enum만, `anyhow`는 app 최상위(main.rs, CLI)에서만. fit-pal CLAUDE.md 인용.
- [ ] C-04: **rust-audit** SKILL.md Gotchas에 workspace lints 기반 lint 발견 절차 명시 — `cargo clippy --workspace --all-targets -- -D warnings`가 workspace.lints.clippy 설정을 반영한다는 점.

### P (Preventive / regressions / deferred from previous kaizen, 5개)

- [ ] P-01: **rust-api** `unimplemented!()` 2건 (lines 108, 112), **rust-auth** `unimplemented!()` 3건 (lines 127, 131, 135)은 **유지 허용** (todo!() false-positive 회피 — 이전 Phase 9 결정 사항). 단 위 블록이 여전히 스킬 예시 코드임을 주석으로 명시 ("예시: refresh_token_store 연동 후 구현")하여 실제 프로덕션으로 복사될 때 에러를 유도.
- [ ] P-02: `rust-l10n` Extension/Locale 패턴은 유지하되 Gotchas에 Axum 0.8에서 `axum::extract::Request`/`axum::middleware::Next` API 그대로 사용 가능함을 명시.
- [ ] P-03: **모든 rust-kit SKILL.md와 agents/rust-reviewer.md**의 bare fenced code block 0건 유지 (validate-plugin V6 회귀 금지). 새로 추가하는 code block은 `rust`, `bash`, `toml`, `text`, `dockerfile` 등 언어 힌트 필수.
- [ ] P-04: **모든 수정 파일**의 파일 끝 newline 1개 유지. 한글 띄어쓰기/조사 일관성 유지 ("—" 대시 사용, "·" 중점 허용).
- [ ] P-05: 수정 후 **`python3 scripts/validate-plugin.py`** 실행 결과 **7 OK (rust-kit V1~V7 포함)** 유지. **`python3 scripts/sync-docs.py --check-only`** 에서 rust-kit README drift 없음 (있으면 sync-docs 실행 후 commit 포함).

## Commands

- 실행: (수동 편집만, 빌드/런타임 없음)
- 검증: `python3 scripts/validate-plugin.py rust-kit` + `python3 scripts/validate-plugin.py` (7 OK) + `python3 scripts/sync-docs.py --check-only`
- bare fence 검증: `python3 scripts/validate-plugin.py rust-kit --check=code-fence`

## Inputs

- `rust-kit/skills/*/SKILL.md` (16)
- `rust-kit/agents/rust-reviewer.md`
- `rust-kit/references/project-detection.md`
- `rust-kit/skills/rust-audit/references/audit-criteria.md`
- `.harness/.meta/kaizen-data-pool.md` §2, §5
- `/Users/jackson/Hub/10_Dev/fit-pal/server/Cargo.toml` (실무 ground truth)
- `/Users/jackson/Hub/10_Dev/fit-pal/server/CLAUDE.md` (실무 컨벤션)
- `/Users/jackson/Hub/10_Dev/fit-pal/server/deny.toml` (cargo-deny v2 실제 예시)
- `/Users/jackson/Hub/10_Dev/fit-pal/server/rust-toolchain.toml`
- `/Users/jackson/Hub/10_Dev/fit-pal/.harness/sprint-feedback.md` (Makefile 검증)

## Outputs

- 16 SKILL.md 수정 (Gotchas/Process 갱신)
- `rust-reviewer.md` 감사 기준 연동 (수정 필요 시)
- `audit-criteria.md` — Clippy 2026 lint 카테고리, Security 행 갱신
- `project-detection.md` — edition/lints 감지 (필요 시)
- commit message: `kaizen(phase9-research): rust-kit 2026 Rust 2024/Axum 0.8/SeaORM 1.1/Clippy 반영`
- validate-plugin 7 OK + sync-docs check 통과

## Acceptance (자기 감사 L3)

1. 위 R/A/D/H/T/C/P 조건이 각 파일:라인 근거와 함께 충족.
2. `python3 scripts/validate-plugin.py rust-kit` 출력 `V1 16 skills + 1 agent`, `V6 0 bare`, `V7 v0.1.0 matches marketplace`.
3. `python3 scripts/validate-plugin.py` 전체 7 OK.
4. `python3 scripts/sync-docs.py --check-only` 변경 없음 (있으면 sync 실행 후 재검증).
5. git status 에 **수정 대상 파일 + sprint-contract.md** 외 다른 modified 없음 (kaizen-data-pool.md 제외).
6. commit 1개 (또는 필요 시 sync-docs commit 1개 추가).

## Rollback

- 실패 시: `git checkout rust-kit/` + `git checkout .harness/sprint-contract.md`로 원복.
- 각 조건 REJECT 시 개별 Edit 로 재수정 후 재평가.
