---
name: rust-run
description: >
  Rust 빌드 프리미티브 실행 (build, clippy, fmt, test, audit, check).
  "빌드해줘", "clippy 돌려줘", "포맷팅", "테스트 실행",
  "cargo build", "cargo clippy", "lint" 같은 요청 시 사용한다.
  상위 워크플로우 스킬(rust-build, rust-preflight)에서 내부적으로도 호출된다.
  코드를 직접 수정하거나 새 파일을 생성하는 작업에는 사용하지 않는다.
argument-hint: "<build|clippy|fmt|test|audit|check> [args]"
user-invocable: true
---

# Gotchas

1. **`cargo clippy`에 `-- -D warnings` 필수** — 없으면 워닝이 에러로 잡히지 않아 CI와 불일치한다. 권장 전체 커맨드: `cargo clippy --workspace --all-targets --all-features -- -D warnings`. `workspace.lints.clippy.pedantic = "deny"`가 설정되어 있으면 `-D warnings` 없이도 pedantic 위반은 에러가 되지만, `-- -D warnings`는 모든 일반 warning도 함께 실패시키므로 항상 붙인다.
2. **`cargo fmt --all -- --check`** — preflight/CI에서는 `--check`로 포맷 불일치를 에러로 노출한다. 로컬 편집 시에는 `cargo fmt --all` (check 제외)로 자동 적용한다. fit-pal Makefile 패턴.
3. **workspace에서 `--workspace` 필수** — 없으면 루트 크레이트만 실행되어 하위 크레이트 문제를 놓친다. `--all-targets`도 함께 붙여 binary/test/example 전부 검사.
4. **`cargo nextest`가 없을 때 에러 금지** — 설치 여부 확인 후 없으면 `cargo test`로 폴백한다.
5. **`cargo audit` 미설치 시 skip** — 설치 안내만 출력하고 중단하지 않는다. `cargo deny check`도 동일 정책.
6. **`cargo deny check` v2 형식** — advisories/licenses/bans/sources 4개 섹션을 `deny.toml`에서 관리. advisories v2는 `vulnerability`/`notice` 필드가 제거되어 항상 에러로 동작. `cargo deny check all`로 전체 검사, `cargo deny check advisories` 등으로 개별 실행 가능.
7. **Makefile 기반 monorepo에서는 `cargo` 직접 호출 금지** — `make server-run`, `make server-test`, `make server-lint`, `make server-fmt`, `make server-fmt-fix`, `make server-migrate`, `make server-preflight` 같은 Makefile 타겟을 사용한다. Makefile이 `APP_ENV`, `RUST_LOG`, `DATABASE_URL` 등 필수 환경변수를 주입하므로 직접 `cargo run`하면 환경변수 누락으로 실행 실패한다. 정식 예시 (fit-pal Makefile APPROVE iter 2, 33/33 검증):
   - `APP_ENV=dev RUST_LOG=debug cargo run -p fitpal-api`
   - `APP_ENV=dev cargo test --workspace`
   - `DATABASE_URL=postgres://fitpal:fitpal@localhost:5432/fitpal cargo run -p fitpal-migration`
8. **`.PHONY` 타겟 누락 금지** — Makefile 기반 프로젝트에서 새 타겟 추가 시 반드시 `.PHONY:` 선언에도 추가한다. 누락 시 동일 이름 파일/디렉토리와 충돌. fit-pal REJECT 히스토리에서 `server-fmt-fix`, `server-preflight`가 누락되어 REJECT → 재수정 사례 존재.

# Process

## Gotchas

- **서브커맨드 문자열을 정규화하지 않으면 안 된다** — 사용자가 "빌드", "build", "b" 등 다양한 형태로 입력할 수 있다. 매핑 테이블을 통해 정규화하라. 인식 불가 시 사용 가능한 서브커맨드 목록을 보여주라.
- **workspace 플래그를 단일 크레이트 프로젝트에 전달하지 마라** — `[workspace]` 섹션이 없는 프로젝트에서 `--workspace`를 붙이면 에러가 발생한다. Cargo.toml을 읽어 workspace 여부를 먼저 판단하라.
- **nightly 전용 커맨드를 stable에서 실행하지 마라** — `cargo +nightly udeps`, `cargo miri test` 등은 nightly가 필수다. 실행 전 `rustup show`로 현재 toolchain을 확인하고, stable이면 `rustup run nightly`로 감싸거나 불가능을 알려라.
- **`cargo test`와 `cargo nextest run`을 혼용하지 마라** — 프로젝트에 `cargo-nextest`가 설정되어 있으면(`.config/nextest.toml` 존재) nextest를 사용하라. 둘의 출력 형식과 필터 문법이 다르다.
- **`cargo fmt`를 `--check` 없이 실행하면 파일이 수정된다** — 확인만 하고 싶은 경우 `--check`를 반드시 붙여라. 의도치 않은 파일 변경은 git status를 오염시킨다.
- **`cargo clippy --fix`의 자동 수정을 맹신하지 마라** — clippy의 자동 수정이 의미를 바꿀 수 있다(예: `clone()` 제거가 borrow checker 에러 유발). 수정 후 반드시 `cargo check`로 컴파일을 확인하라.
- **`cargo audit`를 `advisory-db` 업데이트 없이 실행하지 마라** — 오래된 DB로 검사하면 최신 취약점을 놓친다. `cargo audit fetch` 후 `cargo audit`를 실행하거나 `--deny warnings`로 새 advisory를 감지하라.
- **환경변수 `RUST_LOG`를 설정하지 않고 테스트 로그가 안 보인다고 보고하지 마라** — `cargo test`는 기본적으로 stdout을 캡처한다. `-- --nocapture`와 `RUST_LOG=debug`를 함께 설정해야 로그가 출력된다.
- **병렬 테스트가 서로 간섭할 때 `--test-threads=1`을 기본값으로 강제하지 마라** — 전체 테스트를 직렬화하면 CI 시간이 폭증한다. 간섭하는 테스트만 `#[serial]` (serial_test 크레이트)로 표시하라.
- **`cargo check`와 `cargo build`의 차이를 무시하지 마라** — `check`는 코드 생성(codegen) 단계를 건너뛰어 빠르지만, 링크 에러나 proc-macro 런타임 문제를 잡지 못한다. 최종 검증은 반드시 `build`로 하라.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `IS_WORKSPACE`, `HAS_NEXTEST`) 를 사용한다.

## 1. 서브커맨드 파싱

| 서브커맨드 | 실행 커맨드 | 성공 조건 |
|-----------|------------|----------|
| `build` | `$CARGO build` + (`--workspace --all-targets` if `IS_WORKSPACE`) | exit 0 |
| `clippy` | `$CARGO clippy` + (`--workspace --all-targets --all-features` if `IS_WORKSPACE`) + `-- -D warnings` | exit 0, 워닝 0 |
| `fmt` | `$CARGO fmt --all` (적용) / `$CARGO fmt --all -- --check` (검사만) | exit 0 |
| `test` | `HAS_NEXTEST` → `cargo nextest run --workspace` / else → `$CARGO test` + (`--workspace` if `IS_WORKSPACE`) | 전 테스트 통과 |
| `audit` | `cargo deny check` (있으면, v2 형식 `deny.toml`) + `cargo audit` (있으면) | 취약점 0 |
| `check` | `$CARGO check` + (`--workspace --all-targets` if `IS_WORKSPACE`) | exit 0 |

> **`audit` 우선순위**: `cargo-deny`가 설치되어 있고 `deny.toml`이 존재하면 `cargo deny check`를 먼저 실행하여 advisories/licenses/bans/sources 4 카테고리를 동시에 검사한다. `cargo-audit`은 advisories만 다루므로 `cargo-deny` 사용 시 중복이지만 보조 검증으로 병행 가능하다. 둘 다 없으면 설치 안내만 출력 후 skip.

추가 args가 있으면 커맨드 끝에 전달한다.

## 2. 실행 + 결과 출력

실행 결과를 아래 포맷으로 출력한다:

### rust-run {서브커맨드} 결과

**커맨드:** `{실행된 전체 커맨드}`
**상태:** PASS / FAIL
**상세:** {에러 메시지 또는 요약}

# References

- references/project-detection.md
