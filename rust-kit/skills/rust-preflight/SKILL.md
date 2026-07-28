---
name: rust-preflight
description: >
  Pre-commit quality gate. fmt → clippy → test → audit 순서로 실행하고
  결과를 요약 보고한다.
  "preflight", "프리플라이트", "커밋 전 검사", "pre-commit",
  "품질 게이트", "커밋 전에 확인" 같은 요청 시 사용한다.
  개별 프리미티브만 실행하려면 rust-run을 직접 사용한다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **순서 변경 금지** — fmt → clippy → test → audit 순서는 고정이다. clippy 전에 fmt를 해야 포맷 워닝이 없다. fit-pal `server-preflight` Makefile 타겟 검증 순서와 동일.
2. **fmt 실패 시 자동 적용** — `cargo fmt --all -- --check` 실패 시 `cargo fmt --all`를 적용한 후 재검사한다. 자동 수정 후 unstaged changes가 생기므로 `git add` 안내를 출력한다.
3. **audit은 non-blocking** — 외부 크레이트 취약점은 즉시 수정 불가할 수 있으므로 WARN으로만 표시한다. 단 `deny.toml`의 `licenses.allow` 위반이나 `sources.unknown-registry = "deny"` 위반은 즉시 FAIL.
4. **clippy 또는 test 실패 시 즉시 중단** — 이후 단계를 실행하지 않는다.
5. **Makefile 환경에서는 `make server-preflight` 사용** — `APP_ENV`, `DATABASE_URL`, `RUST_LOG` 등 환경변수가 Makefile에 정의된 경우 직접 `cargo` 호출 시 누락된다. migration이 포함된 프로젝트(fit-pal 패턴: `DATABASE_URL=postgres://fitpal:fitpal@localhost:5432/fitpal`)는 preflight 전에 DB가 올라와 있어야 한다. fit-pal `server-preflight` 타겟 = `server-fmt` → `server-lint` → `server-test` 체인.
6. **DB 의존 테스트가 있으면 `infra-up`을 선행** — `sqlx::test` 또는 `serial_test` 통합 테스트는 실제 Postgres를 요구한다. fit-pal 패턴은 `make infra-up` (docker compose up -d) → `make server-migrate` → `make server-preflight` 순서. preflight 단독 실행은 DB가 이미 기동된 상태를 가정한다.
7. **마이그레이션 미적용 상태에서 test 를 돌리지 마라 (DG-03 회귀 방지)** — 공유 로컬 DB 를 쓰는 통합 테스트는 스키마가 뒤처지면 `column "..." of relation "..." does not exist` 로 실패한다. 이건 코드 결함이 아니라 **환경 미준비**이므로 test 실패로 보고하기 전에 Step 2.5 의 마이그레이션 확인을 먼저 통과시킨다. 2026-06 실측: `cargo test --workspace` 통합 테스트 2 건이 `is_admin` 컬럼 부재로 REJECT → `cargo run -p fitpal-migration` 후 통과.
8. **각 단계의 종료 코드를 기록한다 (E2)** — rust-run Gotcha 10 의 파이프라인 규약(`set -o pipefail` + 파이프라인 직후 `rc=$?`)을 그대로 쓰고, Step 5 리포트 표의 `Exit` 칸을 반드시 채운다. 종료 코드 없는 PASS 는 자기보고이지 증거가 아니다 (`skill-design-guide.md` §3.7).
9. **타깃 필터를 임의로 좁히지 마라** — preflight 의 test 단계는 워크스페이스 전체가 기본이다. 특정 패키지/타깃으로 좁힐 때는 `references/project-detection.md` Step 3a 의 `PKG_TARGETS` 를 확인한다 (바이너리 전용 패키지 `--lib` 금지 — rust-run Gotcha 9).

# Process

## Gotchas

- **fmt를 clippy보다 반드시 먼저 실행하라** — `cargo fmt` 후 코드 레이아웃이 변경되면 clippy 경고 위치가 달라진다. fmt 없이 clippy를 실행하면 수정 후 다시 clippy 위치가 바뀌어 혼란스럽다.
- **테스트 실패 시 파이프라인을 즉시 중단하라** — test가 실패했는데 audit까지 진행하면 시간만 낭비된다. `cargo test` 실패 → 즉시 FAIL 보고 → 파이프라인 종료가 올바른 흐름이다.
- **`cargo audit`은 non-blocking(경고)으로 처리하라** — advisory DB의 취약점이 프로젝트에 실제 영향을 주는지 판단이 필요하다. audit 경고만으로 커밋을 차단하면 upstream 패치를 기다리는 동안 개발이 멈춘다.
- **workspace에서 `--workspace` 플래그를 빠뜨리지 마라** — `cargo test`만 실행하면 루트 크레이트만 테스트된다. `cargo test --workspace`로 모든 멤버 크레이트를 테스트하라.
- **fmt 체크를 `--check` 모드로 실행하지 않으면 안 된다** — preflight에서 `cargo fmt`(수정 모드)를 실행하면 파일이 변경되어 staged 상태가 꼬인다. `cargo fmt --check`로 확인만 하고, 실패 시 사용자에게 `cargo fmt` 실행을 안내하라.
- **clippy의 `--all-targets`를 빠뜨리지 마라** — 기본 clippy는 lib + bin만 검사한다. `--all-targets`를 추가해야 tests, examples, benches도 검사된다. 테스트 코드의 lint 위반이 CI에서 터지는 것을 방지한다.
- **환경변수에 의존하는 테스트가 실패할 때 전체를 FAIL로 보고하지 마라** — `.env` 파일 미존재, DB 미연결 등 환경 문제로 실패하는 통합 테스트는 `#[ignore]` 표시 여부를 확인하고, 단위 테스트만 게이트로 사용하라.
- **preflight 결과를 구조화하지 않고 텍스트 덤프로 보고하지 마라** — 각 단계별 PASS/FAIL + 소요 시간 + 실패 시 핵심 에러 메시지 1~3줄로 요약하라. cargo 전체 출력을 붙이면 사용자가 읽지 않는다.
- **이전 preflight에서 생성된 아티팩트를 정리하지 않으면 안 된다** — `cargo test`가 남긴 임시 파일, `cargo audit`의 advisory-db lock 등이 다음 실행에 영향을 줄 수 있다. 각 단계 시작 전 clean 상태를 확인하라.
- **nightly 전용 옵션을 stable toolchain에서 실행하지 마라** — `cargo fmt`의 일부 옵션(`imports_granularity` 등)은 nightly에서만 동작한다. `rust-toolchain.toml`의 channel이 stable이면 해당 옵션을 `.rustfmt.toml`에서 제거하라.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$CARGO`, `IS_WORKSPACE`, `HAS_NEXTEST`) 를 사용한다.

## 1. fmt 검사

rust-run `fmt --check`를 실행한다.
- PASS → Step 2로
- FAIL → rust-run `fmt`를 실행하여 자동 적용 후 재검사. 재검사도 FAIL이면 중단.
  - 자동 적용 시: "`cargo fmt`가 파일을 수정했습니다. `git add`로 변경사항을 스테이징하세요." 안내.

## 2. clippy 검사

rust-run clippy를 실행한다.
- PASS → Step 3로
- FAIL → 에러 출력 후 중단. 이후 단계 skip.

## 2.5. 마이그레이션 적용 상태 확인 (DB 의존 테스트가 있을 때만)

`HAS_SQLX` 또는 `HAS_SEAORM` 이고 실제 DB 를 쓰는 통합 테스트가 존재하면, test 단계 **이전에** 스키마가
최신인지 확인한다. 확인 없이 test 로 넘어가면 환경 문제를 코드 결함으로 오진한다 (Gotcha 7).

| 스택 | 확인 명령 | 미적용 시 적용 명령 |
| ---- | --------- | ------------------- |
| SQLx (sqlx-cli 설치) | `sqlx migrate info` — `migrations/` 와 DB 이력을 대조해 pending 목록 표시 | `sqlx migrate run` (pending 스크립트만 실행) |
| SeaORM / 전용 migration 크레이트 | 마이그레이션 크레이트를 `PKG_TARGETS` 에서 확인 | `cargo run -p <migration-crate>` (fit-pal: `cargo run -p fitpal-migration`) |
| Makefile 보유 | — | `make server-migrate` (환경변수 주입 포함) |

- `DATABASE_URL` 은 `--database-url` 플래그 또는 환경변수/`.env` 로 주어져야 한다
  ([sqlx-cli README](https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md)).
- **`#[sqlx::test]` 만 쓰는 테스트에는 이 단계가 불필요하다** — 이 매크로는 테스트마다 새 DB 를 만들고
  `CARGO_MANIFEST_DIR` 의 `migrations` 폴더를 자동 적용한다
  ([sqlx::test](https://docs.rs/sqlx/latest/sqlx/attr.test.html)). 공유 DB 를 직접 쓰는
  `#[tokio::test]` + `serial_test` 계열만 수동 선적용이 필요하다.
- DB 가 아예 없어 확인이 불가능하면 test 단계를 조용히 통과시키지 말고 `[미검증] DB 미기동 — 통합 테스트
  미실행` 으로 리포트에 남긴다.

## 3. test 실행

rust-run test를 실행한다.
- PASS → Step 4로
- FAIL → 에러 출력 후 중단. 이후 단계 skip.
- 실행된 테스트 수가 0 이면 PASS 가 아니라 **타깃 필터/환경 오류**로 처리한다 (Gotcha 9).

## 4. audit 검사

rust-run audit를 실행한다.
- PASS → 정상
- FAIL → WARN으로 표시 (non-blocking). 취약점 목록 출력.

## 5. 리포트

## Preflight Report

| Step | Exit | Status | Details |
| ---- | ---- | ------ | ------- |
| fmt | {rc} | {PASS/FAIL/FIXED} | {상세} |
| clippy | {rc} | {PASS/FAIL/SKIP} | {상세} |
| migration | {rc} | {PASS/SKIP/[미검증]} | {pending N 건 / 적용 완료 / DB 미기동} |
| test | {rc} | {PASS/FAIL/SKIP} | {N tests passed / failed — N=0 이면 FAIL 처리} |
| audit | {rc} | {PASS/WARN/SKIP} | {N advisories} |

**Result:** {PASS / PASS (with warnings) / FAIL}

`Exit` 칸은 실제 종료 코드다 (Gotcha 8). 캡처하지 못한 단계는 `-` 가 아니라 `[미검증]` 으로 적고
사유를 Details 에 남긴다.

# References

- references/project-detection.md
