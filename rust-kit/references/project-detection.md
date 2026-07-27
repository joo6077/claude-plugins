# Rust 프로젝트 감지

rust-kit 스킬이 공통으로 실행하는 프로젝트 환경 감지 절차.

---

## Step 0. 적용 범위 선언 (스택 경계)

rust-kit 의 규칙·안티패턴·감사 기준은 **cargo 가 관리하는 Rust 산출물**(`*.rs`, `Cargo.toml`,
`rust-toolchain.toml`, `deny.toml`, `migrations/*.sql`) 에만 적용된다. 같은 리포지토리 안에 있어도
아래 산출물에는 Rust 기준을 적용하지 않는다:

| 산출물 | Rust 기준 적용 | 대신 적용할 기준 |
| ------ | -------------- | ---------------- |
| 셸 스크립트 (`*.sh`), Makefile 타겟 | ✗ (`unwrap()` · `println!` · `?` 연산자 기준 무의미) | `set -euo pipefail` · 실패 전파(early exit) · 시크릿 하드코딩 금지 · trap 정리 |
| `docker-compose.yml`, Dockerfile | ✗ | infra-kit 기준 (헬스체크 · non-root · 이미지 핀 고정) |
| CI 워크플로 (`.github/workflows/*.yml`) | ✗ | infra-kit 기준 (권한 최소화 · 액션 SHA 핀) |
| 프런트엔드/클라이언트 코드 | ✗ | 해당 kit 기준 (flutter-toolkit · react-kit) |

**금지:** 셸/compose/CI 작업의 완료 조건이나 감사 항목에 `unwrap()` 금지 · `println!` 금지 같은
Rust 전용 조건을 넣지 마라. 스택이 다르면 같은 이름의 결함이 존재하지 않으므로 그 조건은 항상
공허하게 통과한다 (증거 무효 — `qa-evaluation-guide.md` §Evidence Validity Gate 검사 2).
출처: 2026-07 실측 `stack-inappropriate-rust-antipatterns` (셸/compose 백업 사이드카 계약에
Rust 안티패턴 조건 오적용).

## Step 1. Rust 프로젝트 확인

`Cargo.toml` 존재 여부 확인. 없으면 "Rust 프로젝트가 아닙니다" 안내 후 중단.

## Step 1a. 프로젝트 루트 고정 (cwd 드리프트 차단)

명령을 실행하기 전에 루트를 **한 번 확정하고 이후 모든 명령에서 고정**한다:

```bash
CARGO_ROOT="$(dirname "$(cargo locate-project --workspace --message-format plain)")"
```

- `cargo locate-project` 는 cwd 에서 위로 올라가며 매니페스트를 찾고, `--workspace` 는 현재 멤버가
  아니라 **워크스페이스 루트**의 `Cargo.toml` 을 돌려준다
  ([cargo-locate-project](https://doc.rust-lang.org/cargo/commands/cargo-locate-project.html)).
- 확정한 `$CARGO_ROOT` 는 환경 파일(`.env`, `.harness/env.sh`) · Makefile · 마이그레이션 경로의
  **유일한 기준**이다. 서브디렉토리마다 다른 파일을 소싱하지 마라.
- **가드 우회 금지:** 실행 가드(예: `server/.harness/env.sh` 의 `APP_ENV` 요구)가 명령을 막으면,
  cwd 를 옮겨 다른 `.harness` 를 소싱하거나 상위 디렉토리에서 재시도하는 방식으로 우회하지 마라.
  가드가 요구하는 환경을 실제로 충족시키거나, 가드 자체가 잘못됐다고 판단되면 **우회 대신 명시 보고**한다.
  출처: 2026-07 실측 `bypass-run-guard-by-cwd`.

## Step 2. 툴체인 감지

| 조건 | 결과 |
|------|------|
| `rust-toolchain.toml` 존재 | 파일에서 `channel`, `components`, `profile` 파싱 → `$RUST_CHANNEL` |
| 없음 | `rustup default` 결과 사용 |

## Step 2a. Edition 감지

`Cargo.toml` 또는 `[workspace.package]`의 `edition` 값을 읽어 `$EDITION` 에 저장한다.

| 값 | 의미 |
|----|------|
| `"2024"` | Rust 2024 Edition (1.85+, 2026 기본) — RPIT capture 변경, `unsafe extern`, let chain stable |
| `"2021"` | 레거시 지원 — 신규 프로젝트에는 권장하지 않음 |
| 미지정 | `Cargo.toml`이 잘못됨 — 에러 |

## Step 2b. Workspace lints 감지

`[workspace.lints]` 섹션 존재 여부:

| 조건 | 결과 |
|------|------|
| `[workspace.lints.clippy]` pedantic = deny | `HAS_WORKSPACE_LINTS = true`, `LINTS_STRICTNESS = "pedantic"` |
| `[workspace.lints]` 존재하나 pedantic 없음 | `HAS_WORKSPACE_LINTS = true`, `LINTS_STRICTNESS = "basic"` |
| 없음 | `HAS_WORKSPACE_LINTS = false` — audit 시 권장 메시지 출력 |

member crate가 `[lints] workspace = true`를 선언하는지도 같이 확인한다.

## Step 3. Workspace 감지

`Cargo.toml`에 `[workspace]` 섹션 존재 여부:

| 조건 | 결과 |
|------|------|
| `[workspace]` 존재 | `IS_WORKSPACE = true`, `WORKSPACE_MEMBERS` = members 목록, `$RESOLVER` = resolver 값 |
| 없음 | `IS_WORKSPACE = false` |

## Step 3a. 패키지 타깃 구조 감지 (`PKG_TARGETS`) — 테스트/실행 전 필수

`cargo test`/`cargo run` 에 패키지 필터(`-p`)나 타깃 필터(`--lib` 등)를 붙이기 **전에** 각 패키지가
어떤 타깃을 가지는지 확정한다. 추측 금지 — 아래 명령으로 열거한다:

```bash
cargo metadata --no-deps --format-version 1 \
  | python3 -c "import json,sys;[print(p['name'], sorted({k for t in p['targets'] for k in t['kind']})) for p in json.load(sys.stdin)['packages']]"
```

`cargo metadata` 의 `packages[].targets[].kind` 는 `lib` / `bin` / `example` / `test` / `bench` /
`custom-build` 중 하나 이상을 담는다. **어떤 타깃의 `kind` 배열에도 `lib` 이 없으면 그 패키지는
바이너리 전용**이다 ([cargo-metadata](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html)).

결과를 `PKG_TARGETS` (패키지명 → 타깃 kind 집합) 로 보관하고 아래 규칙을 적용한다:

| 패키지 타깃 | 허용 필터 | 금지 |
| ----------- | --------- | ---- |
| `lib` 포함 | `--lib` · `--tests` · `--all-targets` | — |
| `bin` 만 (바이너리 전용) | `--bins` · `--bin <name>` · `--tests` · `--all-targets` | **`--lib`** — lib 타깃이 없어 실행할 테스트가 0 개이거나 에러 |
| `lib` + `bin` | 전부 | — |

- `cargo test` 는 타깃 필터를 **주지 않으면** lib 단위 테스트 · bin 단위 테스트 · 통합 테스트 · lib
  doctest 를 모두 빌드/실행한다. 특정 타깃만 좁히고 싶을 때만 필터를 붙인다
  ([cargo-test 타깃 선택](https://doc.rust-lang.org/cargo/commands/cargo-test.html)).
- **타깃 필터는 매니페스트의 `test` 플래그를 무시하고 해당 타깃을 강제**하므로, 존재하지 않는 타깃을
  지정하면 "테스트 0 개 실행" 또는 에러로 끝난다. **테스트 0 개는 통과가 아니다** (`qa-evaluation-guide.md`
  §Evidence Validity Gate 검사 2).
- 출처: 2026-07 실측 `cargo-test-wrong-target` — 바이너리 크레이트 `fitpal-api` 에
  `cargo test -p fitpal-api --lib healthcheck` 를 실행해 실패.

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
| `$CARGO_ROOT` | 워크스페이스 루트 절대 경로 (Step 1a — 이후 모든 명령의 고정 기준) |
| `$PACKAGE` | Cargo.toml [package].name |
| `$EDITION` | 2021 \| 2024 |
| `IS_WORKSPACE` | true \| false |
| `WORKSPACE_MEMBERS` | 크레이트 목록 (IS_WORKSPACE일 때만) |
| `PKG_TARGETS` | 패키지명 → 타깃 kind 집합 (Step 3a — `--lib`/`--bins` 선택 근거) |
| `ARCH` | hexagonal \| workspace_service \| modular \| flat \| library |

### 의존성 플래그 (HAS_*)

위 Step 4 테이블 참조.

### 빌드 도구

위 Step 6 테이블 참조.
