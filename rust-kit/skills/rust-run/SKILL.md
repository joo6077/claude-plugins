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

1. **`cargo clippy`에 `-- -D warnings` 누락 금지** — 없으면 워닝이 에러로 잡히지 않아 CI와 불일치한다.
2. **workspace에서 `--workspace` 누락 금지** — 없으면 루트 크레이트만 실행되어 하위 크레이트 문제를 놓친다.
3. **`cargo nextest`가 없을 때 에러 금지** — 설치 여부 확인 후 없으면 `cargo test`로 폴백한다.
4. **`cargo audit` 미설치 시 skip** — 설치 안내만 출력하고 중단하지 않는다.
5. **Makefile 기반 monorepo에서는 `cargo` 직접 호출 금지** — `make server-run`, `make server-test` 등 Makefile 타겟을 사용한다. Makefile이 `APP_ENV`, `RUST_LOG`, `DATABASE_URL` 등 필수 환경변수를 주입하므로 직접 `cargo run`하면 환경변수 누락으로 실행 실패한다 (fit-pal 패턴: `APP_ENV=dev RUST_LOG=debug cargo run -p fitpal-api`).

# Process

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `IS_WORKSPACE`, `HAS_NEXTEST`) 를 사용한다.

## 1. 서브커맨드 파싱

| 서브커맨드 | 실행 커맨드 | 성공 조건 |
|-----------|------------|----------|
| `build` | `$CARGO build` + (`--workspace` if `IS_WORKSPACE`) | exit 0 |
| `clippy` | `$CARGO clippy` + (`--workspace` if `IS_WORKSPACE`) + `-- -D warnings` | exit 0, 워닝 0 |
| `fmt` | `$CARGO fmt` (적용) / `$CARGO fmt -- --check` (검사만) | exit 0 |
| `test` | `HAS_NEXTEST` → `cargo nextest run` / else → `$CARGO test` + (`--workspace` if `IS_WORKSPACE`) | 전 테스트 통과 |
| `audit` | `cargo audit` (있으면) + `cargo deny check` (있으면) | 취약점 0 |
| `check` | `$CARGO check` + (`--workspace` if `IS_WORKSPACE`) | exit 0 |

추가 args가 있으면 커맨드 끝에 전달한다.

## 2. 실행 + 결과 출력

실행 결과를 아래 포맷으로 출력한다:

### rust-run {서브커맨드} 결과

**커맨드:** `{실행된 전체 커맨드}`
**상태:** PASS / FAIL
**상세:** {에러 메시지 또는 요약}

# References

- references/project-detection.md
