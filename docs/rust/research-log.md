---
version: 1.0.0
last_updated: 2026-04-11
---

# Rust Kit Research Log

> rust-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 9 (research-mode rerun)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 1 | Rust Edition 2024 Guide | <https://doc.rust-lang.org/edition-guide/> | 공식 | 높음 | 채택 (기본 edition) |
| 2 | Rust 1.85/1.88 release blog | <https://blog.rust-lang.org/> | 공식 | 높음 | 채택 |
| 3 | Axum 0.8 announcement | <https://tokio.rs/blog/2024-12-01-announcing-axum-0-8-0> | 공식 | 높음 | 채택 |
| 4 | Axum 0.8 CHANGELOG | <https://github.com/tokio-rs/axum/blob/main/axum/CHANGELOG.md> | 공식 | 높음 | 채택 |
| 5 | SQLx 0.8 CHANGELOG | <https://github.com/launchbadge/sqlx/blob/main/CHANGELOG.md> | 공식 | 높음 | 채택 |
| 6 | SeaORM 1.1 docs | <https://www.sea-ql.org/SeaORM/> | 공식 | 높음 | 채택 (MockDatabase) |
| 7 | Tonic 0.13 CHANGELOG | <https://github.com/hyperium/tonic/blob/master/CHANGELOG.md> | 공식 | 높음 | 채택 |
| 8 | RFC 3389 manifest-lint (workspace.lints) | <https://rust-lang.github.io/rfcs/3389-manifest-lint.html> | 공식 | 높음 | 채택 |
| 9 | Clippy lints index | <https://rust-lang.github.io/rust-clippy/master/> | 공식 | 높음 | 채택 |
| 10 | cargo-deny v2 advisories | <https://embarkstudios.github.io/cargo-deny/> | 공식 | 높음 | 채택 |
| 11 | fit-pal server/ (Rust 백엔드 ground truth) | (internal) | ground truth | 높음 | 채택 |
| 12 | fit-pal sprint-feedback iter2 (33/33) | (internal) | ground truth | 높음 | 채택 (Makefile monorepo 인사이트) |

### 채택한 인사이트

- **Rust 2024 edition 기본값**: 신규 프로젝트는 `edition = "2024"` + `resolver = "3"` 로 생성. Rust 1.85+ (2025-02-20) 에서 stable 편입. RPIT capture 규칙 변경, `unsafe extern`, `let` chain, `if let` temporary scope 변경 포함. 마이그레이션 시 `cargo fix --edition` 사용. 적용: rust-init Gotcha #2.
- **Axum 0.8 path parameter breaking change**: `:id` colon 문법 완전 제거 → `{id}` 중괄호만. 와일드카드는 `{*rest}`. `matchit` 2.x 기반 교체. 적용: rust-api, rust-auth, rust-middleware.
- **Axum 0.8 `#[async_trait]` 제거**: `FromRequest`, `FromRequestParts`, `Handler` 등 핵심 trait 이 native `async fn in trait` 으로 전환. 사용자 extractor 구현 시 `#[async_trait]` 붙이지 말고 `async fn from_request_parts(...)` 직접 선언. `axum::async_trait` 재수출은 deprecated. 적용: rust-auth.
- **SQLx 0.8 + rustls 조합**: runtime-tokio + tls-rustls 가 2026 표준. tls-native 는 OpenSSL 의존성 이슈로 비권장. chrono/time crate 선택 주의. 적용: rust-model.
- **SeaORM 1.1 MockDatabase**: 단위 테스트에서 DB 없이 mock 으로 쿼리 결과 주입. fit-pal server 실제 사용 패턴. 적용: rust-test.
- **Tonic 0.13**: gRPC 서비스 구현 시 `#[tonic::async_trait]` 은 **유지**. Axum 과 다르게 Tonic 은 자체 async_trait 매크로를 계속 사용한다. prost 0.14 호환. 적용: rust-grpc.
- **workspace.lints SSOT (RFC 3389)**: Rust 1.74+ 에서 workspace 루트 `[workspace.lints]` 한 번 정의 → member crate 는 `[lints] workspace = true` 한 줄 상속. clippy 설정 중복 금지. 적용: rust-init §4a, rust-audit.
- **Clippy 2026 lint 세트**: `needless_pass_by_value`, `redundant_clone`, `cloned_instead_of_copied`, `inefficient_to_string`, `large_futures` 를 pedantic deny 기본 포함. 적용: audit-criteria.
- **cargo-deny v2**: advisories / licenses / bans / sources 4 섹션 v2 형식. `multiple-versions = "warn"`, `unknown-registry = "deny"` 가 2026 실무 기본값. 적용: rust-init §4c, rust-run.
- **Consumer-Owned Port + Composition Root 단일화 + Domain event/outbox**: fit-pal server 의 헥사고날 패턴 3개 원칙이 rust-init / rust-feature / rust-api Gotchas 에 전파됨. 적용: rust-init #5, #6, #8, rust-feature #5~#7, rust-api Composition Root.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `rust-migrate` | 런북 | 2021 → 2024 edition, Axum 0.7 → 0.8 마이그레이션 가이드 | 중간 | backlog |
| `rust-observability` | 런북 | tracing-opentelemetry 실무 설정 | 중간 | backlog |

### 폐기 사유

- Context7 monthly quota 소진으로 resolve 실패. fit-pal server ground truth + 공식 CHANGELOG 로 대체.

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>
