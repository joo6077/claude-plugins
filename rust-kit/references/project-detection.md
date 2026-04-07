# Rust 프로젝트 감지

rust-kit 스킬이 공통으로 실행하는 프로젝트 환경 감지 절차.

---

## Step 1. Rust 프로젝트 확인

`Cargo.toml` 존재 여부 확인. 없으면 "Rust 프로젝트가 아닙니다" 안내 후 중단.

## Step 2. 툴체인 감지

| 조건 | 결과 |
|------|------|
| `rust-toolchain.toml` 존재 | 파일에서 `channel`, `components` 파싱 |
| 없음 | `rustup default` 결과 사용 |

## Step 3. Workspace 감지

`Cargo.toml`에 `[workspace]` 섹션 존재 여부:

| 조건 | 결과 |
|------|------|
| `[workspace]` 존재 | `IS_WORKSPACE = true`, `WORKSPACE_MEMBERS` = members 목록 |
| 없음 | `IS_WORKSPACE = false` |

## Step 4. 의존성 감지

`Cargo.toml`의 `[dependencies]`와 `[dev-dependencies]`에서 다음 크레이트 존재 여부를 확인하고 `HAS_*` 플래그를 설정한다.

IS_WORKSPACE이면 workspace root + 모든 member의 Cargo.toml을 합산한다.

| 크레이트 | 플래그 |
|----------|--------|
| `axum` | `HAS_AXUM` |
| `actix-web` | `HAS_ACTIX` |
| `rocket` | `HAS_ROCKET` |
| `sqlx` | `HAS_SQLX` |
| `diesel` | `HAS_DIESEL` |
| `sea-orm` | `HAS_SEAORM` |
| `tokio` | `HAS_TOKIO` |
| `async-std` | `HAS_ASYNC_STD` |
| `tonic` | `HAS_TONIC` |
| `serde` | `HAS_SERDE` |
| `utoipa` | `HAS_UTOIPA` |
| `jsonwebtoken` | `HAS_JSONWEBTOKEN` |
| `tracing` | `HAS_TRACING` |
| `rust-i18n` | `HAS_RUST_I18N` |
| `fluent` | `HAS_FLUENT` |
| `mockall` | `HAS_MOCKALL` |

`cargo-nextest` 설치 여부: `command -v cargo-nextest` 또는 `cargo nextest --version` → `HAS_NEXTEST`

## Step 5. 아키텍처 패턴 감지

| 조건 | `ARCH` 값 |
|------|-----------|
| `ports/` + `adapters/` 디렉토리 존재 (workspace 또는 단일 크레이트) | `hexagonal` |
| `IS_WORKSPACE` + `crates/` 디렉토리 (api/domain/infra 등) | `workspace_service` |
| 단일 크레이트 + `src/api/`, `src/domain/` 등 모듈 분리 | `modular` |
| `src/main.rs` + `src/lib.rs` 수준 | `flat` |
| `[lib]` only, `[[bin]]` 없음 | `library` |

감지 순서가 중요하다: hexagonal이 최우선 (다른 아키텍처와 중첩 가능).

## Step 6. 빌드 도구 감지

| 파일 | 플래그 |
|------|--------|
| `Makefile` | `HAS_MAKEFILE` |
| `justfile` | `HAS_JUST` |
| `Makefile.toml` (cargo-make) | `HAS_CARGO_MAKE` |
| `Cross.toml` | `HAS_CROSS` → `$CARGO = cross` |
| `build.rs` | `HAS_BUILD_SCRIPT` |

## Step 7. CI 감지

| 파일/디렉토리 | CI 플랫폼 |
|---------------|-----------|
| `.github/workflows/` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `.circleci/` | CircleCI |

---

## 감지 결과 변수 요약

### 커맨드

| 변수 | 기본값 | 조건 |
|------|--------|------|
| `$CARGO` | `cargo` | `HAS_CROSS`이면 `cross` |
| `$RUSTFMT` | `cargo fmt` | |
| `$CLIPPY` | `cargo clippy` | |

### 프로젝트 메타

| 변수 | 설명 |
|------|------|
| `$PACKAGE` | Cargo.toml [package].name |
| `$EDITION` | 2021 \| 2024 |
| `IS_WORKSPACE` | true \| false |
| `WORKSPACE_MEMBERS` | 크레이트 목록 (IS_WORKSPACE일 때만) |
| `ARCH` | hexagonal \| workspace_service \| modular \| flat \| library |

### 의존성 플래그 (HAS_*)

위 Step 4 테이블 참조.

### 빌드 도구

위 Step 6 테이블 참조.
