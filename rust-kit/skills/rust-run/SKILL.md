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
9. **타깃 필터는 `PKG_TARGETS` 확인 후에만 붙인다** — 바이너리 전용 패키지에 `--lib` 을 붙이면 실행할 테스트가 0 개이거나 에러다. `references/project-detection.md` Step 3a 로 각 패키지의 타깃 kind 를 먼저 열거하고, `lib` 이 없으면 `--bins`(또는 `--bin <name>` · `--tests` · `--all-targets`) 를 쓴다. 좁힐 이유가 없으면 **필터를 아예 붙이지 않는 것이 기본값**이다 — `cargo test` 는 필터가 없을 때 lib/bin 단위 테스트 + 통합 테스트 + doctest 를 모두 돈다 ([cargo-test 타깃 선택](https://doc.rust-lang.org/cargo/commands/cargo-test.html)). 출처: 2026-07 실측 `cargo-test-wrong-target` (`cargo test -p fitpal-api --lib healthcheck` 가 bin-only 크레이트에서 실패).
10. **파이프라인 종료 코드 캡처 규약 (E2 — 3 회 재발 승급)** — `unreliable-exit-status-capture` · `unreliable-piped-exit-code-capture` · `broken-pipeline-exit-capture` 가 2026-07 한 달에 3 회 재발했다. 문장 다짐이 아니라 **명령 형태를 고정**한다:
    - 파이프를 쓰는 순간 **`set -o pipefail` 을 같은 명령 안에서 켠다.** bash 기본값은 "파이프라인의 종료 상태 = 마지막 명령의 종료 상태" 이므로 `cargo test ... | tee log` 는 cargo 가 실패해도 0 을 돌려준다. `pipefail` 이 켜지면 "0 이 아닌 상태로 끝난 가장 오른쪽 명령의 값" 이 파이프라인 상태가 된다 ([Bash Reference Manual — Pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)).
    - **정식 형태 (쉘 무관, 이것을 기본으로 쓴다):** `set -o pipefail; cargo clippy ... 2>&1 | tee /tmp/clippy.log; rc=$?` — `rc` 를 리포트에 그대로 적는다. `pipefail` + 파이프라인 **직후** 의 `$?` 조합은 bash·zsh 양쪽에서 동작한다.
    - 개별 단계 상태까지 필요하면 배열을 **파이프라인 직후 한 번에** 복사한다. **배열 이름이 쉘마다 다르다** — bash 는 `st=("${PIPESTATUS[@]}")`, zsh 는 `st=("${pipestatus[@]}")` (zsh 에서 대문자 `PIPESTATUS` 는 정의되지 않는다). 쉘을 모르면 배열에 의존하지 말고 위 정식 형태를 쓴다. 중간에 다른 명령을 끼우면 배열이 덮어써진다.
    - **금지:** `$?` 를 여러 명령 뒤에 읽기 · `if cmd | grep -q ...` 결과를 cmd 의 성공으로 해석 · exit code 를 출력 텍스트("error" 문자열 유무)로 추정하기.
11. **실행 가드를 cwd 로 우회하지 마라** — `.harness/env.sh` 같은 실행 가드가 `APP_ENV`/`DATABASE_URL` 을 요구하며 `cargo run` 을 막으면, 상위 디렉토리로 옮겨 다른 `.harness` 를 소싱해 통과시키지 마라. (a) 가드가 요구하는 환경변수를 실제로 주입하거나 (b) 가드가 잘못됐다고 판단되면 **우회 대신 사용자에게 명시 보고**한다. 모든 명령은 `references/project-detection.md` Step 1a 에서 확정한 `$CARGO_ROOT` 기준으로 실행한다. 출처: 2026-07 실측 `bypass-run-guard-by-cwd`.
12. **비-Rust 산출물에 Rust 기준 적용 금지** — 이 스킬이 셸 스크립트·compose·CI YAML 을 다루게 되면 `unwrap()`/`println!` 같은 Rust 안티패턴 기준을 그대로 옮기지 마라. 스택별 대응 기준은 `references/project-detection.md` Step 0 표를 따른다.

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
- **tokio-console로 async task 디버깅** — `console-subscriber` 크레이트를 추가하면 htop 스타일로 task/resource/span을 실시간 모니터링할 수 있다. **개발 전용** — 프로덕션에서는 비활성화한다. `RUSTFLAGS="--cfg tokio_unstable"` 환경변수가 필요하다.
- **Cranelift 백엔드로 dev build 가속** — `rustc_codegen_cranelift`는 nightly에서 `codegen-backend = "cranelift"`로 사용 가능하며 debug compile time ~20% 개선을 목표로 한다. SIMD/panic unwind 제약이 있어 LLVM 완전 대체가 아닌 dev profile 전용이다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO_ROOT`, `$CARGO`, `IS_WORKSPACE`, `PKG_TARGETS`, `HAS_NEXTEST`) 를 사용한다.

`test` 서브커맨드에 `-p`/`--lib`/`--bin` 같은 필터를 붙일 예정이면 **Step 3a(패키지 타깃 구조 감지)를
건너뛰지 않는다** — `PKG_TARGETS` 없이 타깃 필터를 붙이는 것은 추측이다 (Gotcha 9).

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

> **타깃 필터 주의 (Gotcha 9):** `test`/`build`/`check` 에 `--lib` 을 붙이려면 `PKG_TARGETS` 에서 해당
> 패키지가 `lib` 타깃을 가지는지 먼저 확인한다. `bin` 만 있으면 `--lib` 대신 `--bins` 를 쓴다.

## 2. 실행 + 결과 출력

파이프를 쓰는 경우 Gotcha 10 의 정식 형태(`set -o pipefail` + `rc=$?`)로 실행한다. 실행 결과를 아래
포맷으로 출력하며, **종료 코드 칸은 비워 두지 않는다** (자기보고가 아닌 도구 출력 아티팩트 —
`skill-design-guide.md` §3.7 Completion Evidence Gate):

### rust-run {서브커맨드} 결과

**커맨드:** `{실행된 전체 커맨드}`
**종료 코드:** `{rc}` (파이프 사용 시 `PIPESTATUS=({...})` 병기)
**상태:** PASS / FAIL
**상세:** {에러 메시지 또는 요약}

- 종료 코드를 확보하지 못했으면 상태를 PASS 로 적지 말고 `[미검증] 종료 코드 캡처 실패 — 재실행 필요`
  로 보고한다. 출력 텍스트만 보고 성공을 추정하지 않는다.
- `test` 결과는 **실행된 테스트 수**를 함께 적는다. `0 passed` 는 통과가 아니라 타깃 필터가 틀렸다는
  신호다 (Gotcha 9).

# References

- references/project-detection.md
