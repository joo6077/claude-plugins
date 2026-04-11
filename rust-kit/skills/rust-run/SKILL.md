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
