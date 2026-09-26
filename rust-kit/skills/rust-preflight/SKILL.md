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

1. **순서 변경 금지** — fmt → clippy → test → audit 순서는 고정이다. clippy 전에 fmt를 해야 포맷 워닝이 없다. 실사용 프로젝트의 `server-preflight` Makefile 타겟 검증 순서와 동일.
2. **fmt 실패 시 자동 적용** — `cargo fmt --all -- --check` 실패 시 `cargo fmt --all`를 적용한 후 재검사한다. 자동 수정 후 unstaged changes가 생기므로 `git add` 안내를 출력한다.
3. **audit은 non-blocking** — 외부 크레이트 취약점은 즉시 수정 불가할 수 있으므로 WARN으로만 표시한다. 단 `deny.toml`의 `licenses.allow` 위반이나 `sources.unknown-registry = "deny"` 위반은 즉시 FAIL.
4. **clippy 또는 test 실패 시 즉시 중단** — 이후 단계를 실행하지 않는다.
5. **Makefile 환경에서는 `make server-preflight` 사용** — `APP_ENV`, `DATABASE_URL`, `RUST_LOG` 등 환경변수가 Makefile에 정의된 경우 직접 `cargo` 호출 시 누락된다. migration이 포함된 프로젝트(예: `DATABASE_URL=postgres://myapp:myapp@localhost:5432/myapp`)는 preflight 전에 DB가 올라와 있어야 한다. 실사용 프로젝트의 `server-preflight` 타겟 = `server-fmt` → `server-lint` → `server-test` 체인.
6. **DB 의존 테스트가 있으면 `infra-up`을 선행** — `sqlx::test` 또는 `serial_test` 통합 테스트는 실제 Postgres를 요구한다. 실사용 프로젝트 패턴은 `make infra-up` (docker compose up -d) → `make server-migrate` → `make server-preflight` 순서. preflight 단독 실행은 DB가 이미 기동된 상태를 가정한다.
7. **마이그레이션 미적용 상태에서 test 를 돌리지 마라 (DG-03 회귀 방지)** — 공유 로컬 DB 를 쓰는 통합 테스트는 스키마가 뒤처지면 `column "..." of relation "..." does not exist` 로 실패한다. 이건 코드 결함이 아니라 **환경 미준비**이므로 test 실패로 보고하기 전에 Step 2.5 의 마이그레이션 확인을 먼저 통과시킨다. 2026-06 실측: `cargo test --workspace` 통합 테스트 2 건이 `is_admin` 컬럼 부재로 REJECT → `cargo run -p myapp-migration` 후 통과.
8. **각 단계의 종료 코드를 기록한다 (E2)** — rust-run Gotcha 10 의 파이프라인 규약(`set -o pipefail` + 파이프라인 직후 `rc=$?`)을 그대로 쓰고, Step 5 리포트 표의 `Exit` 칸을 반드시 채운다. 종료 코드 없는 PASS 는 자기보고이지 증거가 아니다 (`skill-design-guide.md` §3.7).
9. **타깃 필터를 임의로 좁히지 마라** — preflight 의 test 단계는 워크스페이스 전체가 기본이다. 특정 패키지/타깃으로 좁힐 때는 `references/project-detection.md` Step 3a 의 `PKG_TARGETS` 를 확인한다 (바이너리 전용 패키지 `--lib` 금지 — rust-run Gotcha 9).
10. **빨간 clippy · test 를 내 변경 탓으로 단정하지 말고 원인을 셋으로 가른다 (enforcement 등급 E2)** — 내 변경 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패. 여럿이 같이 쓰는 작업 폴더에서는 남이 고치다 만 파일까지 같이 컴파일돼 내 검사가 실패한다. 가르는 절차는 Step 3.5 이고, 그 결과를 Step 5 리포트의 FAIL 행 Details 첫머리에 적는다. **원인을 갈라도 Status 는 FAIL 그대로다** — 남의 탓이라고 PASS 로 바꾸지 않는다. 남의 변경을 치우려고 `git stash` 를 쓰지 마라 — stash 는 작업 폴더를 `HEAD` 로 되돌려 남이 하던 변경까지 옮긴다 ([git stash](https://git-scm.com/docs/git-stash)). 실측(2026-09-18): 다른 세션들이 깬 공용 개발 가지의 자동 검사 실패 다섯 건을 고치는 데 몇 시간을 썼다.

# Process

## Gotchas

- **fmt를 clippy보다 반드시 먼저 실행하라** — `cargo fmt` 후 코드 레이아웃이 변경되면 clippy 경고 위치가 달라진다. fmt 없이 clippy를 실행하면 수정 후 다시 clippy 위치가 바뀌어 혼란스럽다.
- **테스트 실패 시 파이프라인을 즉시 중단하라** — test가 실패했는데 audit까지 진행하면 시간만 낭비된다. `cargo test` 실패 → 즉시 FAIL 보고 → 파이프라인 종료가 올바른 흐름이다.
- **`cargo audit`은 non-blocking(경고)으로 처리하라** — advisory DB의 취약점이 프로젝트에 실제 영향을 주는지 판단이 필요하다. audit 경고만으로 커밋을 차단하면 upstream 패치를 기다리는 동안 개발이 멈춘다.
- **workspace에서 `--workspace` 플래그를 빠뜨리지 마라** — `cargo test`만 실행하면 루트 크레이트만 테스트된다. `cargo test --workspace`로 모든 멤버 크레이트를 테스트하라.
- **fmt 는 먼저 `--check` 모드로 확인한다** — 처음부터 `cargo fmt`(수정 모드)를 돌리면 무엇이 바뀌었는지 모른 채 파일이 바뀐다. 확인이 실패했을 때만 Gotcha 2 · Step 1 대로 `cargo fmt --all` 을 적용하고 다시 검사한 뒤, 바뀐 파일과 `git add` 안내를 보고한다(Step 5 표의 `FIXED`).
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
- FAIL → 에러 출력 후 중단. 이후 단계 skip. 고치기 전에 Step 3.5 로 원인을 가른다.

## 2.5. 마이그레이션 적용 상태 확인 (DB 의존 테스트가 있을 때만)

`HAS_SQLX` 또는 `HAS_SEAORM` 이고 실제 DB 를 쓰는 통합 테스트가 존재하면, test 단계 **이전에** 스키마가
최신인지 확인한다. 확인 없이 test 로 넘어가면 환경 문제를 코드 결함으로 오진한다 (Gotcha 7).

| 스택 | 확인 명령 | 미적용 시 적용 명령 |
| ---- | --------- | ------------------- |
| SQLx (sqlx-cli 설치) | `sqlx migrate info` — `migrations/` 와 DB 이력을 대조해 pending 목록 표시 | `sqlx migrate run` (pending 스크립트만 실행) |
| SeaORM / 전용 migration 크레이트 | 마이그레이션 크레이트를 `PKG_TARGETS` 에서 확인 | `cargo run -p <migration-crate>` (예: `cargo run -p myapp-migration`) |
| Makefile 보유 | — | `make server-migrate` (환경변수 주입 포함) |

- `DATABASE_URL` 은 `--database-url` 플래그 또는 환경변수/`.env` 로 주어져야 한다
  ([sqlx-cli README](https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md)).
- **`#[sqlx::test]` 만 쓰는 테스트에는 이 단계가 불필요하다** — 이 매크로는 테스트마다 새 DB 를 만들고
  `CARGO_MANIFEST_DIR` 의 `migrations` 폴더를 자동 적용한다
  ([sqlx::test](https://docs.rs/sqlx/latest/sqlx/attr.test.html)). 공유 DB 를 직접 쓰는
  `#[tokio::test]` + `serial_test` 계열만 수동 선적용이 필요하다.
- DB 가 아예 없어 확인이 불가능하면 test 단계를 조용히 통과시키지 말고 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을
  채워 리포트에 남긴다 — 예: 막는 것: DB 접속 명령과 그 거부 출력 · 시도한 우회: DB 컨테이너 기동 명령(Gotcha 6)과 그 결과 ·
  통제 불가 사유: 이 환경에서 컨테이너를 띄울 수 없다 · 재검증 명령: DB 를 띄운 뒤 Step 2.5 와 test 단계.

## 3. test 실행

rust-run test를 실행한다.
- PASS → Step 4로
- FAIL → 에러 출력 후 중단. 이후 단계 skip. 고치기 전에 Step 3.5 로 원인을 가른다.
- 실행된 테스트 수가 0 이면 PASS 가 아니라 **타깃 필터/환경 오류**로 처리한다 (Gotcha 9).

## 3.5. 실패 원인 가르기 (Step 2 · 3 이 FAIL 일 때 — Gotcha 10)

고치기 전에 같은 명령을 깨끗한 임시 워크트리에서 다시 돌려 원인을 가른다. 워크트리마다 `HEAD` 와 목록을 따로 두므로
공용 작업 폴더의 남의 변경을 건드리지 않는다 ([git worktree](https://git-scm.com/docs/git-worktree)).
`<실패한 검사 명령>` 은 Step 2 · 3 에서 실패한 rust-run 명령 그대로이고, `<기준 가지>` 는 합칠 대상 가지다.
임시 워크트리에는 추적하지 않는 파일(`target/` · `.env` · DB 에 적용한 마이그레이션)이 없으니 `<준비 명령>` 에 환경 변수
주입과 Step 2.5 의 마이그레이션 적용을 넣는다 — 안 넣으면 준비가 안 된 탓의 실패를 기준 커밋 탓으로 읽는다.
`target/` 이 비어 있어 처음부터 빌드한다.

```bash
FORK_BASE=$(git merge-base HEAD origin/<기준 가지>)
for ref in HEAD "$FORK_BASE" origin/<기준 가지>; do
  t=$(mktemp -d)
  git worktree add -q --detach "$t" "$ref"
  ( cd "$t" && <준비 명령> && <실패한 검사 명령> ) >/dev/null 2>&1
  rc=$?
  echo "$ref $(git rev-parse --short "$ref") $(cd "$t" && rustc --version) exit=$rc"
  git worktree remove --force "$t"
done
```

판정 세 줄은 harness `/sprint` Step 3 의 표를 글자 그대로 옮겼다. 플러그인이 따로 설치돼 경로로 가리킬 수 없다.

| 공용 작업 폴더 | `HEAD` 임시 | `FORK_BASE` 임시 | 판정 |
| --- | --- | --- | --- |
| 실패 | 통과 | — | 미커밋 변경 탓 — `git status --short` 의 파일이 내가 쓴 목록 밖이면 남의 미커밋이다 |
| 실패 | 실패 | 실패 | 기준 커밋에서 이미 실패 — 내 변경 전부터다 |
| 실패 | 실패 | 통과 | 이번 커밋 탓일 가능성이 크다 |

preflight 는 커밋 전에 돈다 — 첫 줄의 미커밋 변경에는 내 변경도 들어 있다. 내 것과 남의 것을 가르려면 `HEAD` 임시
워크트리에 내가 쓴 파일만 얹어 한 번 더 돌린다. `<내 경로…>` 는 이번 작업에서 실제로 쓴 파일 목록이다.
그래서 표 첫 줄 판정 칸의 「남의 미커밋이다」 는 이 블록과 아래 세 조건을 채울 때만 확정한다.

```bash
t=$(mktemp -d)
git worktree add -q --detach "$t" HEAD
for f in <내 경로…>; do
  if [ -e "$f" ]; then mkdir -p "$t/$(dirname "$f")" && cp -p "$f" "$t/$f"; else rm -f "$t/$f"; fi
done
( cd "$t" && <준비 명령> && <실패한 검사 명령> ) >/dev/null 2>&1
echo "HEAD+내 변경 exit=$?"
git worktree remove --force "$t"
```

- 이 블록은 표 첫 줄(`HEAD` 임시 통과)일 때만 돌린다. `HEAD+내 변경` 이 실패하면 **내 변경** 탓이다
- `HEAD` 임시가 실패하면 이 블록으로 가르지 않는다 — 표 둘째 줄은 `기준 커밋에서 이미 실패`, 셋째 줄은 `FORK_BASE..HEAD` 사이 커밋이 원인 후보다.
  셋째 줄에서 그 커밋을 이번 작업이 만들었으면 Details 를 `내 변경` 으로, 아니면 `[미검증]` 으로 시작하고 통제 불가 사유 칸에 「귀속 불명」 을 적는다
- `HEAD+내 변경` 이 통과하는데 공용 작업 폴더만 실패하면 **남의 미커밋** 이 원인 후보다. 확정하려면 (a) 실패 진단의 첫 위치(`-->` 줄)가 가리키는
  파일이 작업을 시작할 때 떠 둔 `git status --porcelain=v1 --untracked-files=all` 출력에도 있었고 (b) 그 파일이 내 경로 밖이며
  (c) 진단이 내가 바꾼 이름(함수 · 타입 · 필드)을 가리키지 않아야 한다. 하나라도 확인하지 못하면 `[미검증]` 으로 적고
  네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채운다 — 통제 불가 사유 칸에 「귀속 불명」 을 적는다
- 시작 때 떠 둔 목록이 없으면 남의 미커밋으로 확정하지 않는다 — git 은 누가 파일을 고쳤는지 알려주지 않는다
  ([git status](https://git-scm.com/docs/git-status))

`FORK_BASE` 는 분기점이지 기준 가지의 지금 상태가 아니다 ([git merge-base](https://git-scm.com/docs/git-merge-base)).
`origin/<기준 가지>` 줄은 분기 뒤 기준 가지가 깨졌는지를 본다. 각 줄에 toolchain 을 함께 적는 이유 — `rust-toolchain.toml` 이
없거나 `stable` 을 따르면 toolchain 이 오를 때 새 Clippy lint 가 더해져, workspace lint 를 `deny` 로 둔 코드는 기준 커밋도
새로 실패한다 ([Clippy CHANGELOG](https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md)).

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
Details 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채운다.

**FAIL 행의 Details 는 원인으로 시작한다 (Gotcha 10).** Step 3.5 결과에 따라 아래 넷 중 하나로 시작하고 증거를 붙인다.
원인을 적어도 그 행의 Status 와 **Result** 는 FAIL 그대로다.

- `내 변경 — {내 파일:줄 또는 diff 한 덩어리}`
- `남의 미커밋 — {시작 때 떠 둔 목록의 그 파일 줄 + 실패 파일:줄}`
- `기준 커밋에서 이미 실패 — {FORK_BASE sha · 명령 · exit · toolchain}`
- `[미검증]` — 네 칸, 통제 불가 사유 칸에 「귀속 불명」

# References

- references/project-detection.md
