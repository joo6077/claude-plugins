---
version: 1.1.0
last_updated: 2026-06-05
---

# Rust Kit Research Log

## [2026-06-05] — Phase 9 kaizen

rust-model 에 §5.5 Enumerate-before-Act 가드 추가 — 생성형 형제 스킬은 보유했으나 rust-model 만 누락된 sibling drift 차단. fit-pal Rust server(SeaORM) 실측 정합 확인.

출처: skill-design-guide §5.5, fit-pal server/CLAUDE.md.


> rust-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.

## [2026-05-07] — Phase 9 kaizen (rust, /insights 흡수)

### 데이터 소스

- 데이터 풀 §0 `/insights` 30 일 분석 (3 friction · 3 pattern · 3 feature)
- `harness/references/cross-kit-principles.md` v1 매트릭스의 rust 열

### Phase 9 변경

- rust/README.md 에 cross-kit-principles 매트릭스 cross-reference 섹션 추가
- plugin.json patch bump (이번 사이클)
- 매핑: rust-audit ANALYZE ↔ Pre-Edit Batch Audit, rust-reviewer self-check ↔ Self-Evaluator Audit, PostToolUse 정적 검증 ↔ Hook-Triggered Auto-Correction

### 외부 리서치 인용 (이전 사이클 보존, 이번 사이클 추가 없음)

이전 카이젠 사이클의 리서치 인용은 본 로그 하단 + cross-kit-principles 매트릭스로 보존된다.

---


---

## 2026-04-12

**트리거:** rust-research 스킬 (research-log 확충)

### 조사한 소스

| # | 제목 | URL | 태그 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 13 | Rust 1.85.0 & 2024 Edition 공식 발표 | <https://blog.rust-lang.org/2025/02/20/Rust-1.85.0/> | [official] [dated: 2025-02] | 높음 | 채택 |
| 14 | Rust 2024 Edition Guide | <https://doc.rust-lang.org/edition-guide/rust-2024/index.html> | [official] | 높음 | 채택 |
| 15 | Axum 0.8.0 공식 발표 | <https://tokio.rs/blog/2025-01-01-announcing-axum-0-8-0> | [official] [dated: 2025-01] | 높음 | 채택 |
| 16 | Axum docs.rs (middleware 패턴) | <https://docs.rs/axum/latest/axum/middleware/index.html> | [official] | 높음 | 채택 |
| 17 | Axum CHANGELOG | <https://github.com/tokio-rs/axum/blob/main/axum/CHANGELOG.md> | [official] | 높음 | 채택 |
| 18 | SQLx 0.8.6 docs.rs | <https://docs.rs/crate/sqlx/latest> | [official] [dated: 2025-05] | 높음 | 채택 |
| 19 | SQLx CHANGELOG | <https://github.com/launchbadge/sqlx/blob/main/CHANGELOG.md> | [official] | 높음 | 채택 |
| 20 | SQLx compile-time SQL 해설 | <https://iamanuragh.in/blog/2026-03-06-rust-sqlx-compile-time-sql-your-database-queries-reviewed-before-production/> | [blog] [dated: 2026-03] | 중간 | 채택 |
| 21 | Tonic 0.14.5 docs.rs | <https://docs.rs/crate/tonic/latest> | [official] [dated: 2026-02] | 높음 | 채택 |
| 22 | Tonic CHANGELOG | <https://github.com/hyperium/tonic/blob/master/CHANGELOG.md> | [official] | 높음 | 채택 |
| 23 | Tokio 1.51.1 docs.rs | <https://docs.rs/crate/tokio/latest> | [official] [dated: 2026-04] | 높음 | 채택 |
| 24 | Tokio Console (async debugger) | <https://github.com/tokio-rs/console> | [official] | 높음 | 채택 |
| 25 | TokioConf 2026 공지 | <https://tokio.rs/blog/2026-03-03-tokioconf-update> | [official] [dated: 2026-03] | 높음 | 참고 |
| 26 | Evolution of Async Rust (JetBrains) | <https://blog.jetbrains.com/rust/2026/02/17/the-evolution-of-async-rust-from-tokio-to-high-level-applications/> | [blog] [dated: 2026-02] | 중간 | 참고 |
| 27 | tracing-opentelemetry docs.rs | <https://docs.rs/tracing-opentelemetry> | [official] | 높음 | 채택 |
| 28 | Rust OpenTelemetry 공식 문서 | <https://opentelemetry.io/docs/languages/rust/> | [official] | 높음 | 채택 |
| 29 | OpenTelemetry Rust GitHub | <https://github.com/open-telemetry/opentelemetry-rust> | [official] | 높음 | 채택 |
| 30 | Rust Observability: OTel + Tokio 해설 | <https://dasroot.net/posts/2026/01/rust-observability-opentelemetry-tokio/> | [blog] [dated: 2026-01] | 중간 | 채택 |
| 31 | thiserror 2.0.18 docs.rs | <https://docs.rs/crate/thiserror/latest> | [official] [dated: 2026-01] | 높음 | 채택 |
| 32 | Error Handling for Large Rust Projects (GreptimeDB) | <https://greptime.com/blogs/2024-05-07-error-rust> | [blog] [dated: 2024-05] | 중간 | 채택 |
| 33 | Rust Error Handling Compared: anyhow vs thiserror vs snafu | <https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003> | [blog] [dated: 2025-03] | 중간 | 채택 |
| 34 | Error backtraces in Rust libraries (Iroh) | <https://www.iroh.computer/blog/error-handling-in-iroh> | [blog] [dated: 2025-01] | 중간 | 참고 |
| 35 | Async fn in Trait 안정화 블로그 | <https://blog.rust-lang.org/inside-rust/2023/05/03/stabilizing-async-fn-in-trait.html> | [official] [dated: 2023-05] | 높음 | 채택 |
| 36 | Rust Project Goals: Async Parity | <https://rust-lang.github.io/rust-project-goals/2024h2/async.html> | [official] | 높음 | 채택 |
| 37 | Rust Project Goals Update July 2025 | <https://blog.rust-lang.org/2025/08/05/july-project-goals-update/> | [official] [dated: 2025-08] | 높음 | 채택 |
| 38 | Rust Serialization Benchmark | <https://github.com/djkoloski/rust_serialization_benchmark> | [official] | 높음 | 채택 |
| 39 | rkyv 0.8 GitHub | <https://github.com/rkyv/rkyv> | [official] | 높음 | 채택 |
| 40 | proptest 1.11.0 docs.rs | <https://docs.rs/crate/proptest/latest> | [official] [dated: 2026-03] | 높음 | 채택 |
| 41 | rstest 0.26.1 docs.rs | <https://docs.rs/crate/rstest/latest> | [official] [dated: 2025-07] | 높음 | 채택 |
| 42 | testcontainers 0.27.2 docs.rs | <https://docs.rs/crate/testcontainers/latest> | [official] [dated: 2026-03] | 높음 | 채택 |
| 43 | Rust Testing Patterns for Reliable Releases | <https://dasroot.net/posts/2026/03/rust-testing-patterns-reliable-releases/> | [blog] [dated: 2026-03] | 중간 | 채택 |
| 44 | utoipa 5.4.0 docs.rs | <https://docs.rs/crate/utoipa/latest> | [official] [dated: 2025-06] | 높음 | 채택 |
| 45 | utoipa GitHub | <https://github.com/juhaku/utoipa> | [official] | 높음 | 채택 |
| 46 | axum-autoroute (utoipa + axum 타이트 통합) | <https://users.rust-lang.org/t/new-crate-axum-autoroute/137402> | [blog] [dated: 2026-02] | 중간 | 참고 |
| 47 | wasm-bindgen 0.2.118 docs.rs | <https://docs.rs/crate/wasm-bindgen/latest> | [official] [dated: 2026-04] | 높음 | 채택 |
| 48 | wasm-pack GitHub (새 org) | <https://github.com/wasm-bindgen/wasm-pack> | [official] | 높음 | 채택 |
| 49 | rustwasm org 아카이브 발표 | <https://blog.rust-lang.org/inside-rust/2025/07/21/sunsetting-the-rustwasm-github-org/> | [official] [dated: 2025-07] | 높음 | 채택 |
| 50 | Rust & WASM in 2026 | <https://dev.to/dataformathub/rust-wasm-in-2026-a-deep-dive-into-high-performance-web-apps-20c6> | [blog] [dated: 2026-01] | 중간 | 참고 |
| 51 | criterion 0.8.2 docs.rs | <https://docs.rs/crate/criterion/latest> | [official] [dated: 2026-02] | 높음 | 채택 |
| 52 | Rust Performance Book (profiling) | <https://nnethercote.github.io/perf-book/profiling.html> | [official] | 높음 | 채택 |
| 53 | cargo-flamegraph 해설 | <https://dasroot.net/posts/2026/03/performance-profiling-rust-apps/> | [blog] [dated: 2026-03] | 중간 | 채택 |
| 54 | Cargo Workspace 대규모 프로젝트 패턴 | <https://reintech.io/blog/cargo-workspace-best-practices-large-rust-projects> | [blog] [dated: 2025-09] | 중간 | 채택 |
| 55 | Advanced Cargo Workspace Patterns (TechKoala) | <https://medium.techkoalainsights.com/7-advanced-cargo-workspace-patterns-for-scalable-rust-monorepo-management-and-build-orchestration-66b7913c1acb> | [blog] [dated: 2025-11] | 중간 | 채택 |
| 56 | Modern Rust Best Practices 2026 | <https://onehorizon.ai/blog/modern-rust-best-practices-in-2026-beyond-the-borrow-checker> | [blog] [dated: 2026-01] | 중간 | 참고 |
| 57 | Rust ORMs in 2026: Diesel vs SQLx vs SeaORM | <https://aarambhdevhub.medium.com/rust-orms-in-2026-diesel-vs-sqlx-vs-seaorm-vs-rusqlite-which-one-should-you-actually-use-706d0fe912f3> | [blog] [dated: 2026-02] | 중간 | 참고 |

### 채택한 인사이트

#### Rust 2024 Edition 심화

- **async closure (`async || {}`)**: Rust 1.85 에서 안정화. `AsyncFn`, `AsyncFnMut`, `AsyncFnOnce` trait 도입. 기존 `|| async {}` (매 호출마다 새 future) 대비 환경 변수 캡처가 가능해 고차 함수 시그니처가 자연스러워짐. 적용: rust-api, rust-service 템플릿에서 미들웨어 팩토리 패턴. [official] [dated: 2025-02]
- **`unsafe extern` 블록**: 2024 edition 에서 `extern` 블록 자체에 `unsafe` 키워드 필수. FFI boundary 를 명시적으로 unsafe 로 표기하여 안전성 리뷰 범위를 줄임. 적용: rust-wasm FFI 가이드. [official]
- **`gen` 키워드 예약**: 2024 edition 에서 `gen` 을 미래 generator 블록용으로 예약. 변수/함수명으로 `gen` 사용 시 마이그레이션 필요. 적용: rust-init Gotcha. [official]
- **`#[diagnostic::do_not_recommend]`**: 라이브러리 author 가 특정 trait impl 을 컴파일러 에러 메시지에서 제외할 수 있음. 사용자 경험 개선. 적용: rust-error 가이드에서 커스텀 에러 trait 설계 시 언급. [official] [dated: 2025-02]
- **rustfmt style editions**: 포맷팅 규칙이 language edition 과 독립적으로 진화. `style_edition = "2024"` 지정 가능. 적용: rust-init 템플릿의 `rustfmt.toml`. [official]

#### Axum 0.8 심화

- **`OptionalFromRequestParts` trait**: `Option<T>` extractor 가 rejection 을 에러 응답으로 변환 가능. 기존에는 rejection → `None` 무조건 변환이라 디버깅 어려웠음. 적용: rust-auth 에서 optional auth 헤더 처리. [official] [dated: 2025-01]
- **middleware 패턴 정리**: Axum 자체 미들웨어 시스템 없이 tower/tower-http 통합. `Router::layer` (전체), `MethodRouter::route_layer` (메서드별), `Handler::layer` (핸들러별) 3단계 적용점. `from_extractor` 는 extractor/middleware 겸용, `from_fn` 은 미들웨어 전용. 적용: rust-middleware 스킬 Gotcha. [official]
- **OpenAPI 경로 일관성**: `{id}` 중괄호 문법이 OpenAPI path parameter 와 동일. utoipa 와 조합 시 경로 정의 불일치 감소. 적용: rust-api + utoipa 연동 가이드. [official]

#### SQLx 0.8 심화

- **버전 현황**: SQLx 0.8.6 stable (2025-05), 0.9.0-alpha.1 preview (2025-10). 프로덕션은 0.8.x 유지 권장. [official]
- **`cargo sqlx prepare` 오프라인 모드**: 로컬에서 DB 연결 상태로 `.sqlx/` 메타데이터 생성 → git commit → CI 에서 DB 없이 쿼리 검증. 적용: rust-model Gotcha, rust-preflight CI 가이드. [official]
- **`query_as!()` 타입 매핑**: 컴파일 타임에 SQL 결과 컬럼을 struct 필드에 1:1 매핑. `FromRow` derive 보다 strict 하지만 안전. 적용: rust-model 템플릿. [official]
- **tls-rustls 표준화**: `runtime-tokio` + `tls-rustls` 조합이 2026 표준. OpenSSL 의존 제거로 cross-compilation 용이. 적용: rust-init Cargo.toml 템플릿. [official]

#### Tokio 생태계 현황

- **Tokio 1.51.1** (2026-04 현재): LTS 릴리스 정책 — 1.47.x LTS until 2026-09, 1.51.x LTS until 2027-03. 프로덕션에서 LTS pinning 권장. [official] [dated: 2026-04]
- **tokio-console**: htop 스타일 async task 디버거. `console-subscriber` 크레이트를 추가하면 런타임에서 task/resource/span 을 실시간 모니터링. 개발 전용 — 프로덕션에서는 비활성화. 적용: rust-run 디버그 모드 가이드. [official]
- **TokioConf 2026 주요 토픽**: executor 블로킹 task 탐지, async cancellation 시맨틱스, zero-downtime 배포. 적용: rust-middleware, rust-service 가이드에 cancellation safety 강조. [official] [dated: 2026-03]

#### OpenTelemetry + tracing 통합

- **tracing-opentelemetry 스택**: `tracing` (instrument) → `tracing-subscriber` (collector) → `tracing-opentelemetry` (bridge) → `opentelemetry-otlp` (exporter). 이 4계층이 2026 Rust observability 표준 스택. [official]
- **OTLP exporter 권장**: 프로덕션에서 `opentelemetry-otlp` 사용. stdout/jaeger exporter 는 개발용. Traces beta, Logs/Metrics stable 상태. [official]
- **zero-cost abstraction**: 비활성 span 은 no-op 으로 컴파일. parent-based sampling 으로 프로덕션 데이터량 조절. `flush()` 미호출 시 마지막 이벤트 유실 위험. 적용: rust-observability backlog 스킬 설계. [official]

#### 에러 처리 생태계

- **thiserror 2.0.18** (2026-01): `#[error(transparent)]`, `#[from]`, `#[source]` 어트리뷰트로 구조적 에러 타입 정의. 라이브러리 크레이트 표준. [official]
- **anyhow**: 애플리케이션 코드용 — `context()` 로 에러 체인에 설명 추가. 라이브러리에서 사용 금지 (타입 정보 손실). [blog]
- **color-eyre**: CLI 도구용 — 풍부한 panic hook + 스택 트레이스 + 색상 포맷. `miette` 와 조합하면 사용자 친화적 에러 출력. [blog]
- **error-stack (Google 출신)**: snafu 수준의 context 강제 + anyhow 수준의 편의성 균형. 대규모 프로젝트에 적합. GreptimeDB 가 채택한 패턴. [blog] [dated: 2024-05]
- **실무 가이드라인**: 라이브러리 → `thiserror`, 애플리케이션 → `anyhow` or `eyre`, CLI → `color-eyre` + `miette`. 적용: rust-error 스킬 Decision Table. [blog]

#### Async Rust 진화

- **async fn in trait**: Rust 1.75 (2023-12) 에서 안정화. 단, `dyn Trait` 에서 async fn 은 미지원 — `#[async_trait]` 매크로가 여전히 필요한 경우. Axum 0.8 은 RPITIT 활용으로 `#[async_trait]` 제거, Tonic 0.14 는 자체 매크로 유지. [official]
- **async generator / Stream**: `gen` 키워드 예약 완료. `poll_next` vs `async fn next` 설계 논의 진행중. `futures::Stream` 이 사실상 표준이지만 std 편입은 미확정. [official] [dated: 2025-08]
- **Pin ergonomics**: autoreborrowing for pinned references 실험적 구현 완료. Pin 사용성 개선이 2025H2 목표였으나 설계 불확실성으로 지연. [official]

#### 직렬화 생태계

- **serde**: 유연성과 생태계 최강이지만 compile time 이 주요 단점 (monomorphisation 비용). 대안: miniserde, nanoserde (runtime dispatch 로 코드 bloat 감소). [official]
- **bitcode 0.6.6**: 직렬화 속도 + 압축 크기 모두 1위 (벤치마크 기준). HTTP/REST JSON 대비 바이너리 프로토콜 (gRPC, 내부 IPC) 에 적합. [official] [dated: 2026-01]
- **rkyv 0.8.10**: zero-copy deserialization. 역직렬화 비용 0 — 직접 메모리 접근. 게임 엔진, 캐시 레이어 등 극한 성능 요구 시. 타입 제약 없음, 외부 스키마 불필요. [official]
- **실무 가이드라인**: 외부 API → serde_json, 내부 IPC/캐시 → bitcode or rkyv, Protobuf 대체 → prost. 적용: rust-grpc (prost), rust-api (serde_json). [official]

#### 테스트 생태계

- **proptest 1.11.0** (2026-03): property-based testing + 자동 shrinking. Hypothesis 영감. 날짜 파싱, 수학 invariant, 직렬화 round-trip 검증에 효과적. [official]
- **rstest 0.26.1** (2025-07): `#[rstest]` 매크로로 parameterized test + fixture injection. `#[case]` 로 테이블 기반 테스트, `#[fixture]` 로 setup 공유. [official]
- **testcontainers 0.27.2** (2026-03): Docker 기반 통합 테스트. PostgreSQL, Redis, Kafka 등 실제 인스턴스를 테스트 격리 환경에서 구동. CI에서 `--test-threads=1` 과 조합. [official]
- **테스트 전략 조합**: unit (cargo test) → property (proptest) → integration (testcontainers) → benchmark (criterion). 적용: rust-test 스킬 Decision Table. [blog] [dated: 2026-03]

#### utoipa OpenAPI

- **utoipa 5.4.0** (2025-06): OpenAPI 3.1 지원. `#[utoipa::path]` proc macro 로 코드 기반 문서 자동 생성. framework-agnostic 이지만 Axum 통합이 가장 성숙. [official]
- **axum-autoroute**: utoipa + axum 타이트 통합 — REST route 와 OpenAPI 문서 정의를 강제 일치시키는 새 크레이트. 코드/문서 불일치 방지. 적용: rust-api utoipa 가이드에 언급. [blog] [dated: 2026-02]

#### Rust WASM

- **wasm-bindgen 0.2.118** (2026-04): Library MSRV 1.77, CLI MSRV 1.86. `js_sys::Promise<T>` 가 `IntoFuture` 구현 → `wasm-bindgen-futures` 가 `js-sys` 내부로 이동 (optional `futures` feature). [official]
- **rustwasm org 아카이브**: 2025-07 공식 발표. wasm-bindgen/wasm-pack 이 새 `wasm-bindgen` org 으로 이전. 유지보수 인력 확충. 프로젝트 쇠퇴가 아닌 조직 재편. [official] [dated: 2025-07]
- **`--target emscripten` 지원**: wasm-bindgen 에서 emscripten 타겟 추가. futures, JS closures, TypeScript 출력 지원. 적용: react-kit rust-wasm 가이드에 타겟 옵션 갱신. [official]

#### 성능 프로파일링

- **criterion 0.8.2** (2026-02): warmup, 통계 분석, 회귀 감지. flamegraph 와 조합하여 벤치마크 중 프로파일링 가능. `#[bench]` 대체 표준. [official]
- **cargo-flamegraph**: perf/DTrace 기반 flame graph 자동 생성. `cargo flamegraph --bench my_bench` 로 벤치마크 핫스팟 시각화. [blog] [dated: 2026-03]
- **DHAT (Dynamic Heap Allocation Tool)**: `dhat` 크레이트로 힙 할당 핫스팟 + 피크 메모리 + memcpy 핫콜 탐지. 메모리 최적화에 필수. [official]
- **eBPF + Parca**: 2026 신규 — 프로덕션 continuous profiling. eBPF 기반 스택 언와인딩으로 오버헤드 최소화. CPU/GPU/메모리 통합 프로파일링. [blog] [dated: 2026-02]

#### Cargo Workspace 패턴

- **workspace.lints SSOT**: `[workspace.lints.clippy]` 한 번 정의 → 멤버 크레이트 `[lints] workspace = true` 상속. Rust 1.74+ stable. [official]
- **workspace.dependencies**: 공통 의존성 버전을 루트에서 관리. 멤버는 `dep.workspace = true` 로 참조. 버전 충돌 방지. [official]
- **test-utils 크레이트**: `publish = false` 로 dev-only 유틸리티. mock, fixture, helper 를 한 곳에 집중. [blog]
- **계층적 구조 (100+ 크레이트)**: `infra/`, `services/`, `domain/` 등 카테고리별 디렉토리. 100 크레이트 이상이면 flat 구조는 탐색 불가. [blog]
- **cargo-chef + sccache**: CI 파이프라인에서 의존성 컴파일 레이어 캐싱. Docker 빌드 시간 50%+ 단축. 적용: rust-docker 스킬. [blog]

#### 메모리 안전성 고급 패턴

- **Data-Oriented Design (SoA)**: `Vec<User>` (AoS) 대신 struct-of-arrays 패턴으로 CPU 캐시 적중률 향상. hot path 에서 throughput 유의미하게 개선. [blog] [dated: 2026-01]
- **interior mutability 가이드라인**: `RefCell<T>` (single-thread), `Mutex<T>` / `RwLock<T>` (multi-thread), `Cell<T>` (Copy 타입). 선택 기준 명확화. [official]
- **Box for recursive types**: 재귀 타입 정의 시 `Box<T>` 필수. 힙 할당으로 컴파일 타임 크기 결정. [official]

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `rust-observability` | 런북 | tracing + opentelemetry + OTLP 프로덕션 설정. 리서치 충분 | 높음 | ready |
| `rust-bench` | 가이드 | criterion + flamegraph + DHAT 벤치마킹 워크플로우 | 중간 | backlog |
| `rust-serialize` | 가이드 | serde vs bitcode vs rkyv 선택 가이드 | 낮음 | backlog |

### 폐기 사유

- 없음 — WebSearch + WebFetch + docs.rs 검증으로 전체 URL 확인 완료.

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

---

## 2026-04-12 (추가 확장)

**트리거:** research-mode 수동 확장 (13개 토픽 backfill)

### 조사한 소스

| # | 제목 | URL | 태그 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 58 | rust-analyzer Changelog #277 | <https://rust-analyzer.github.io/thisweek/2025/03/17/changelog-277.html> | [official] [dated: 2025-03] | 높음 | 채택 |
| 59 | Cargo: Rust-version aware resolver | <https://doc.rust-lang.org/beta/edition-guide/rust-2024/cargo-resolver.html> | [official] | 높음 | 채택 |
| 60 | Rustfmt: Version sorting | <https://doc.rust-lang.org/nightly/edition-guide/rust-2024/rustfmt-version-sorting.html> | [official] | 높음 | 채택 |
| 61 | Rustdoc combined tests | <https://doc.rust-lang.org/edition-guide/rust-2024/rustdoc-doctests.html> | [official] | 높음 | 채택 |
| 62 | axum `from_fn` docs | <https://docs.rs/axum/latest/axum/middleware/fn.from_fn.html> | [official] | 높음 | 채택 |
| 63 | axum `from_fn_with_state` docs | <https://docs.rs/axum/latest/axum/middleware/fn.from_fn_with_state.html> | [official] | 높음 | 채택 |
| 64 | sqlx 0.9.0-alpha.1 docs.rs | <https://docs.rs/crate/sqlx/0.9.0-alpha.1> | [official] [dated: 2025-10] | 높음 | 채택 |
| 65 | sql-check 0.9.0-alpha.1 docs.rs | <https://docs.rs/crate/sql-check/0.9.0-alpha.1> | [official] [dated: 2026-01] | 중간 | 채택 |
| 66 | SQLx GitHub README | <https://github.com/launchbadge/sqlx> | [official] | 높음 | 채택 |
| 67 | SeaORM Data Loader | <https://www.sea-ql.org/SeaORM/docs/relation/data-loader/> | [official] [dated: 2025-03] | 높음 | 채택 |
| 68 | SeaORM Nested Selects | <https://www.sea-ql.org/SeaORM/docs/relation/nested-selects/> | [official] | 높음 | 채택 |
| 69 | SeaORM Multi Selects | <https://www.sea-ql.org/SeaORM/docs/relation/multi-selects/> | [official] | 높음 | 채택 |
| 70 | SeaORM Advanced Joins | <https://www.sea-ql.org/SeaORM/docs/advanced-query/advanced-joins/> | [official] | 높음 | 채택 |
| 71 | Shuttle Introduction | <https://docs.shuttle.dev/welcome/introduction> | [official] | 높음 | 채택 |
| 72 | Shuttle FAQ | <https://docs.shuttle.dev/support/faq> | [official] | 높음 | 채택 |
| 73 | Rust on Fly.io | <https://fly.io/docs/rust/> | [official] | 높음 | 채택 |
| 74 | leptos 0.8.17 docs.rs | <https://docs.rs/crate/leptos/latest> | [official] [dated: 2026-03] | 높음 | 채택 |
| 75 | leptos `server_fn` docs | <https://docs.rs/leptos/latest/leptos/server_fn/index.html> | [official] | 높음 | 채택 |
| 76 | dioxus 0.7.3 docs.rs | <https://docs.rs/crate/dioxus/0.7.3> | [official] [dated: 2026-01] | 높음 | 채택 |
| 77 | Dioxus server functions guide | <https://dioxuslabs.com/learn/0.6/guides/fullstack/server_functions> | [official] | 높음 | 채택 |
| 78 | Miri GitHub | <https://github.com/rust-lang/miri> | [official] | 높음 | 채택 |
| 79 | cargo-mutants overview | <https://mutants.rs/> | [official] | 높음 | 채택 |
| 80 | cargo-mutants baseline tests | <https://mutants.rs/baseline.html> | [official] | 높음 | 채택 |
| 81 | cargo-mutants parallelism | <https://mutants.rs/parallelism.html> | [official] | 높음 | 채택 |
| 82 | tokio runtime module docs | <https://docs.rs/tokio/latest/tokio/runtime/> | [official] | 높음 | 채택 |
| 83 | async-std README | <https://github.com/async-rs/async-std> | [official] | 높음 | 채택 |
| 84 | smol docs.rs | <https://docs.rs/smol> | [official] | 높음 | 채택 |
| 85 | glommio docs.rs | <https://docs.rs/glommio> | [official] | 높음 | 채택 |
| 86 | Embassy homepage | <https://embassy.dev/> | [official] | 높음 | 채택 |
| 87 | embassy-executor docs | <https://docs.embassy.dev/io/index.html> | [official] | 높음 | 채택 |
| 88 | embassy-net docs | <https://docs.embassy.dev/embassy-net/> | [official] | 높음 | 채택 |
| 89 | Leadership Council update — March 2026 | <https://blog.rust-lang.org/inside-rust/2026/04/06/leadership-council-update/> | [official] [dated: 2026-04] | 높음 | 채택 |
| 90 | January 2026 Project Director Update | <https://blog.rust-lang.org/inside-rust/2026/02/09/project-director-update/> | [official] [dated: 2026-02] | 높음 | 채택 |
| 91 | Program management update — January 2026 | <https://blog.rust-lang.org/inside-rust/2026/02/11/program-management-update-2026-01/> | [official] [dated: 2026-02] | 높음 | 채택 |
| 92 | Rust project goals 2025H2 overview | <https://rust-lang.github.io/rust-project-goals/2025h2/index.html> | [official] | 높음 | 채택 |
| 93 | Promoting Parallel Front End | <https://rust-lang.github.io/rust-project-goals/2025h2/parallel-front-end.html> | [official] | 높음 | 채택 |
| 94 | rustc_codegen_cranelift | <https://github.com/rust-lang/rustc_codegen_cranelift> | [official] | 높음 | 채택 |
| 95 | bevy_ecs docs.rs | <https://docs.rs/bevy_ecs/latest/bevy_ecs/> | [official] | 높음 | 채택 |
| 96 | Bevy ECS quick start | <https://bevy.org/learn/quick-start/getting-started/ecs/> | [official] | 높음 | 채택 |
| 97 | cargo-mutants iterate mode | <https://mutants.rs/iterate.html> | [official] | 높음 | 채택 |

### 채택한 인사이트

#### Rust 2024 edition adoption / tooling updates

- **이미 커버된 것**: 2024 edition 기본값, `unsafe extern`, `gen` 예약어, rustfmt style edition, `cargo fix --edition` 는 기존 로그에 이미 있음.
- **신규 델타 - Cargo resolver 3**: 2024 edition 은 `resolver = "3"` 를 암묵 적용하고 `package.rust-version` 을 고려하는 Rust-version-aware dependency resolution 을 기본값으로 활성화한다. 대형 workspace 에서 MSRV 가 서로 다른 크레이트를 섞을 때 dependency 선택이 더 보수적으로 바뀐다. 적용: rust-init 템플릿의 workspace resolver 설명 강화. [official]
- **신규 델타 - rustfmt 정렬 규칙 변경**: 2024 style edition 에서 import/identifier 정렬이 ASCIIbetical 에서 version-sort 류 알고리즘으로 바뀐다. 숫자가 들어간 식별자(`NonZeroU8`, `NonZeroU16`...) 정렬 결과가 달라져 대규모 리포지토리에서 포맷 diff 가 한 번 더 발생할 수 있다. [official]
- **신규 델타 - rustdoc doctest 결합**: 2024 edition 은 doctest 들을 하나의 바이너리로 합쳐 compile overhead 를 줄인다. `Location`/`type_name` 같은 code-location 민감 테스트는 `standalone_crate` 태그가 필요할 수 있다. 적용: rust-ci / rust-doc 가이드. [official]
- **신규 델타 - rust-analyzer 채택**: rust-analyzer 는 2025-03 릴리스에서 자체적으로 2024 edition 으로 전환했고 crate graph 를 incremental 하게 바꿨다. edition 전환뿐 아니라 dependency/proc-macro/build-script 수정 시 전체 workspace 재분석을 줄이는 방향이어서 2024 tooling 성숙도 지표로 볼 만하다. [official] [dated: 2025-03]

#### Axum 0.8 migration 추가 함정

- **이미 커버된 것**: `:id` → `{id}` path syntax 변경, `OptionalFromRequestParts`, `#[async_trait]` 제거는 기존 로그에 이미 있음.
- **신규 델타 - middleware state 함정**: `middleware::from_fn` 은 `State` extractor 를 지원하지 않는다. 상태가 필요한 미들웨어는 반드시 `from_fn_with_state(state, f)` 를 써야 한다. Axum 0.7/0.8 마이그레이션에서 가장 흔한 “왜 State 가 안 뽑히지?” 류 오류 포인트다. 적용: rust-middleware / rust-auth Gotcha 추가. [official]
- **신규 델타 - extractor 순서 제약**: `from_fn` 계열 미들웨어는 `FromRequestParts` extractor 0개 이상 + 마지막 직전 하나의 `FromRequest` extractor + 마지막 `Next` 라는 함수 시그니처 제약이 있다. 커스텀 extractor 와 `Request` 를 섞을 때 인자 순서가 틀리면 에러 메시지가 장황해진다. [official]

#### SQLx 0.9 alpha / roadmap

- **이미 커버된 것**: `0.9.0-alpha.1` 존재 자체와 “프로덕션은 0.8.x 유지 권장”은 기존 로그에 이미 있음.
- **신규 델타 - compile-time SQL 분리**: 2026-01 기준 `sql-check` 크레이트가 SQLx 에서 분리된 compile-time SQL validation 레이어로 공개됐다. SQL 문자열 검증만 필요하고 SQLx query macro 전체 타입 시스템은 원치 않는 프로젝트(예: `tokio-postgres`, custom driver) 에 적합하다. [official] [dated: 2026-01]
- **신규 델타 - 0.9 alpha 포지셔닝**: `sqlx 0.9.0-alpha.1` 문서는 여전히 PostgreSQL/MySQL/SQLite 3개 드라이버 중심이며, README 는 MSSQL 이 0.7 이후 제거되었고 SQLx Pro initiative 의 일부로 rewrite 예정이라고 명시한다. 즉 0.9 alpha 의 핵심은 안정 드라이버 확장보다 macro/tooling 분리와 생태계 재구성에 가깝다. [official] [dated: 2025-10]

#### SeaORM vs SQLx for complex queries

- **이미 커버된 것**: SeaORM 1.1 `MockDatabase` 는 기존 로그에 이미 있음.
- **신규 델타 - batch loading**: SeaORM `LoaderTrait` 는 `find_with_related` JOIN 결과의 중복 row 전송을 피하기 위해 관련 엔티티를 배치 쿼리로 불러온다. one-to-many / many-to-many 에서 상위 row duplication 이 큰 경우 SQLx 수동 JOIN 보다 유지보수성이 좋다. [official] [dated: 2025-03]
- **신규 델타 - nested partial model**: SeaORM 2.0 의 `DerivePartialModel` / nested select 는 alias boilerplate 를 줄이면서 복합 조회 결과를 중첩 struct 로 바로 매핑한다. SQLx 의 `query_as!` 는 엄격하지만 flat row 중심이고, SeaORM 은 nested object projection 이 강점이다. [official]
- **신규 델타 - multi-select consolidate**: `find_also_related` + `and_also_related` + `consolidate()` 로 chain/star topology 를 계층 결과로 재구성할 수 있다. 조회 결과가 “order + line items + cakes” 같이 3계층 이상이면 SeaORM 쪽이 모델링 편의성이 높다. [official]
- **신규 델타 - advanced joins 는 2.0 에서 축소됨**: SeaORM 2.0 docs 는 “대부분의 필요는 nested select 와 entity loader 로 해결된다”고 명시한다. 즉 복잡한 join 케이스에서도 raw SQL 로 바로 도망가기 전, partial model / loader 조합을 먼저 시도하는 것이 최신 권장 경로다. [official]

#### Shuttle.rs / deployment platforms

- **Shuttle**: `#[shuttle_runtime::main]` 과 resource macro 로 Postgres, secrets 등 인프라 provisioning 을 코드에서 직접 요청한다. `shuttle deploy` 시 코드를 archive 해서 Docker image 로 빌드하고 AWS London(`eu-west-2`) 에 배포한다. 빠른 프로토타이핑과 Rust-web-framework boilerplate 제거가 강점이다. [official]
- **Shuttle 제약**: 각 프로젝트는 AWS Fargate VM 격리로 실행되고, 현재 배포 리전은 `eu-west-2` 단일 리전이다. 멀티리전/저지연 글로벌 서비스가 중요하면 Fly.io 같은 대안 검토가 필요하다. [official]
- **Fly.io**: Rust 전용 문서와 `fly launch` / `fly deploy` / `fly scale` 워크플로우를 제공하며, 다중 리전/VM 중심 운영 관점이 Shuttle 보다 더 강하다. 백엔드 프로덕션 운영, 지역 분산, volume/networking 세밀 제어가 우선이면 Fly 쪽이 더 맞다. [official]

#### Leptos / Dioxus full-stack Rust

- **Leptos**: 2026-03 기준 `leptos 0.8.17` 는 “full-stack, isomorphic Rust web framework” 로 정리되어 있고, `#[server]` 기반 server function 으로 클라이언트 호출과 서버 구현을 공존시킨다. 인자/반환 타입은 serialize 가능해야 하고, 함수는 사실상 ad-hoc HTTP API endpoint 라는 점을 명시한다. 적용: full-stack Rust 조사 시 “숨겨진 magic RPC” 로 오해하지 않도록 주의. [official] [dated: 2026-03]
- **Leptos 강점**: `server_fn` 가 middleware, 다양한 codec, HTTP/WebSocket protocol 추상화를 갖고 있어 SSR + hydration + API co-location 에 유리하다. Axum 기반 백엔드와 함께 쓰기 좋은 성격. [official]
- **Dioxus**: 2026-01 기준 `dioxus 0.7.3` 는 하나의 코드베이스로 web/desktop/mobile/fullstack 을 겨냥한다. fullstack 기능은 server functions 와 server state 중심이며, `dioxus/fullstack` + `server` feature 조합을 통해 target 별 의존성을 분리한다. [official] [dated: 2026-01]
- **Dioxus 강점**: UI 코드를 웹에만 묶지 않고 desktop/mobile 까지 확장하려면 Dioxus 가 더 자연스럽다. 반대로 웹 SSR + 서버 함수 중심 백엔드는 Leptos 쪽이 더 직접적이다. [official]

#### Miri / mutation testing

- **Miri**: out-of-bounds, use-after-free, uninitialized data, alignment 위반, invalid enum/bool, data race 일부, Stacked Borrows / Tree Borrows aliasing 위반까지 잡는다. unsafe 코드가 있거나 low-level crate 를 만들면 CI 에 `cargo +nightly miri test` 레인을 별도로 두는 가치가 있다. [official]
- **Miri 한계**: 모든 UB 를 증명하지는 못하고, 특정 실행 하나를 해석할 뿐이며, 네트워킹/FFI 지원이 제한된다. “Miri 통과 = soundness 보장”은 아님. 적용: rust-test 스킬에서 sanitizer 와 구분해 설명 필요. [official]
- **cargo-mutants**: coverage 와 달리 “코드가 실행되었는지”가 아니라 “테스트가 동작 차이를 감지하는지”를 본다. baseline test 로 원본 트리가 통과하는지 먼저 검증하고, scratch directory 를 재사용해 incremental build 이점을 얻는다. [official]
- **cargo-mutants 실무 포인트**: `--iterate` 로 missed mutant 개선 루프를 줄이고, `--jobs` 병렬화는 linker / test straggler 때문에 실효성이 있지만 너무 높이면 머신이 thrash 할 수 있다. flaky test 가 있으면 의미가 무너진다. [official]

#### Async runtime 비교 / Embassy

- **Tokio**: scheduler + I/O driver + timer + blocking pool 이 통합된 범용 런타임이며, multi-threaded work-stealing 스케줄러가 기본 강점이다. 기존 로그의 observability / ecosystem 우위와 결합하면 서버 기본값은 여전히 Tokio 다. [official]
- **async-std**: 공식 README 가 “discontinued; use smol instead” 를 명시한다. 2026 기준 새 프로젝트에서 async-std 선택은 사실상 제외해도 된다. [official]
- **smol**: 작은 런타임이며 다른 작은 async crate 들을 재수출하고, Tokio 기반 라이브러리와는 `async-compat` 어댑터를 권장한다. 런타임 자체를 최소 구성요소로 가져가고 싶은 경우 후보. [official]
- **glommio**: Linux `io_uring` 기반 thread-per-core 런타임이다. 범용 웹백엔드 기본값이 아니라, shard-per-core 설계와 thread-local I/O 를 적극 활용하는 고성능 Linux 서비스에 맞는다. [official]
- **Embassy**: async/await 기반 embedded 프레임워크로, task 가 compile-time state machine 으로 변환되고 heap 없이 single stack 으로 동작한다. RTOS 대체 포지션이 분명하다. [official]
- **Embassy executor/net**: `embassy-executor` 는 static task allocation, integrated timer queue, no busy-loop polling, fair polling 을 제공하고, `embassy-net` 은 no-std/no-alloc async network stack 을 제공한다. embedded async 를 실제 제품 수준으로 끌어올리는 핵심 조합. [official]

#### Governance / foundation / backend architecture / compile times

- **Rust governance 2026**: 2026-04 Leadership Council update 에 따르면 second Program Manager 채용, 2026 project priorities 예산 배정(`$306k` 신규 + 이전 잔액 이월), maintainers fund / grants 재개 논의가 진행 중이다. 재단/프로젝트 협력이 “인력과 운영 예산” 중심으로 제도화되는 중. [official] [dated: 2026-04]
- **Foundation / infra 방향성**: 2026-02 Project Director update 는 2026-2028 전략 승인, crates.io 트래픽/CloudFront 비용 대응, Trusted Publishing GitLab beta, crates.io vulnerability scanning RFC 진행을 언급한다. backend 팀 관점에서는 공급망/배포 신뢰성 이슈가 재단 우선순위로 올라와 있다. [official] [dated: 2026-02]
- **2026 project goals 구조 변화**: 목표 체계가 반기에서 연간 로드맵으로 이동했다. funding 을 application area 와 roadmap 에 연결하려는 움직임이 있어, Rust 언어/툴링 우선순위를 읽을 때 roadmap 단위를 봐야 한다. [official] [dated: 2026-02]
- **Bevy ECS 를 백엔드에 가져오는 포인트**: Bevy ECS 는 standalone crate 로도 사용 가능하고, system parameter 의 data access 정보로 병렬 실행 가능성을 계산한다. backend 에서는 “request pipeline = system”, “singleton config/cache = Resource”, “changed filters = dirty-set 처리” 같은 식으로 적용 가능하다. event-driven workflow, background jobs, simulation-heavy domain 로직에 유효하다. [official]
- **Compile time 개선**: Rust project goals 2025H2 는 parallel front-end 의 20~30% 빠른 build 와 Cranelift backend 의 debug build codegen 약 20% 개선을 목표로 제시한다. 즉 “frontend 병렬화 + LLVM 대체 backend” 가 별개 트랙으로 추진된다. [official]
- **Parallel front-end 상태**: 2025H2 goal 은 deadlock/안정화/성능 개선을 계속 진행한다고 명시한다. 아직 기본 on 이 아니라 feature promotion 단계로 보는 편이 정확하다. [official]
- **Cranelift backend 상태**: `rustc_codegen_cranelift` 는 nightly 의 `rustc-codegen-cranelift-preview` component 로 배포되며 dev profile 에서 `codegen-backend = "cranelift"` 로 쓸 수 있다. 목표는 debug compile time 최적화이지 LLVM 완전 대체가 아니다. SIMD / panic unwind 등 제약이 남아 있다. [official]

### 폐기 / 스킵 메모

- 없음. 13개 요청 토픽 모두 “신규 델타 추가” 혹은 “이미 커버된 부분을 명시한 뒤 신규 정보만 추가”로 처리함.

<!--
추가 요약 (2026-04-12 append-only)

Added:
- Rust 2024 adoption/tooling: resolver 3, rustfmt version sorting, rustdoc combined doctests, rust-analyzer 2024 + incremental crate graph
- Axum 0.8 pitfalls: from_fn does not support State, use from_fn_with_state; middleware extractor ordering constraint
- SQLx 0.9 alpha/roadmap: sql-check extraction, 0.9 alpha positioning, MSSQL still removed pending rewrite
- SeaORM as SQLx alternative: LoaderTrait batching, nested partial models, multi-select consolidate, advanced joins positioning in 2.0
- Deployment: Shuttle provisioning/runtime model, Shuttle region/isolation limits, Fly.io as multi-region alternative
- Full-stack Rust: Leptos server_fn model, Dioxus fullstack/server feature split
- Verification/testing: Miri UB scope and limits, cargo-mutants baseline/iterate/parallelism workflow
- Async runtimes: async-std discontinued, smol minimal runtime, glommio thread-per-core niche, Embassy executor/net details
- Governance 2026: council/foundation budget, program management, annual roadmap model
- Bevy ECS backend carryover: resources, schedules, change detection, parallel systems
- Compile times: project goal claims for parallel front-end and Cranelift, current maturity constraints

Already covered before this append:
- Rust 2024 edition basics, cargo fix, rustfmt style edition
- Axum 0.8 path syntax change, OptionalFromRequestParts, async_trait removal
- SQLx 0.8 stable guidance and 0.9 alpha existence
- SeaORM 1.1 MockDatabase
- Tokio ecosystem general status and observability stack
-->
