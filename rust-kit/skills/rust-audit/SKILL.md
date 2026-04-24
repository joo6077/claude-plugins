---
name: rust-audit
description: >
  Rust 코드를 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  rust-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "Rust 감사", "코드 검수", "rust audit", "코드 리뷰",
  "품질 검사" 같은 요청 시 트리거.
  빌드/테스트만 실행하려면 rust-run이나 rust-preflight를 사용한다.
argument-hint: "[quick|deep] [target-path]"
user-invocable: true
---

# Gotchas

1. **Rust 이외 도메인 평가 금지** — UI 디자인, 인프라 설정은 평가 대상이 아니다.
2. **추측성 FAIL 금지** — 실제 코드를 확인한 후 판정한다. "아마 문제가 있을 것"으로 FAIL하지 않는다.
3. **보안 카테고리 생략 금지** — 항상 Security 카테고리를 포함한다 (`unsafe_code = "forbid"` 준수, 시크릿 하드코딩, 민감정보 로깅 필수 체크).
4. **deep 모드에서만 에이전트 호출** — quick 모드는 직접 검사한다.
5. **clippy는 `--workspace --all-targets --all-features -- -D warnings` 필수** — workspace 전체 + 바이너리/테스트/예제 + 모든 feature 포함. `-D warnings` 없으면 워닝이 에러로 집계되지 않아 CI 불일치 발생. 프로젝트에 `[workspace.lints.clippy]` pedantic deny가 설정되어 있으면 해당 규칙이 lint 자동 반영되므로 별도 `-W clippy::pedantic` 플래그는 불필요. fit-pal 패턴: `cargo clippy --workspace --all-targets -- -D warnings`.
6. **workspace lints 상속 확인** — member crate가 `[lints] workspace = true`를 누락하면 pedantic deny가 적용되지 않는다. 감사 시 각 member `Cargo.toml`에 이 선언이 있는지 먼저 확인한다.
7. **Axum 0.8 path 문법 감사** — `.route("/...:\w+",)` 정규식으로 grep해서 `:id` colon 문법 잔재가 있으면 즉시 FAIL. Axum 0.8에서 컴파일 에러가 나기 때문에 사실상 빌드 확인만으로도 잡히지만, 리팩토링 중간 상태를 감사하는 경우 명시적으로 체크한다.
8. **SQLx vs SeaORM 구분** — DB adapter 감사 시 프로젝트가 SQLx를 쓰는지 SeaORM을 쓰는지 먼저 감지. 감사 기준은 해당 ORM에 맞게 적용 (예: SeaORM 프로젝트에 "sqlx::query! 필수" FAIL 기준 적용 금지).
9. **2026 clippy pedantic 필수 lint** — `needless_pass_by_value`, `redundant_clone`, `cloned_instead_of_copied`, `inefficient_to_string`, `large_futures`가 pedantic deny 기본 세트에 포함되어야 한다. 누락 시 INFO로 보고한다.
10. **cargo-deny v2 형식 확인** — `deny.toml`이 v2 형식(`multiple-versions = "warn"`, `unknown-registry = "deny"`)인지 확인한다. v1 형식(deprecated `vulnerability`/`notice` 필드)이면 마이그레이션을 권고한다.
11. **Edition 2024 준수 확인** — 신규 프로젝트에서 `edition = "2024"` + `resolver = "3"`이 아니면 INFO로 보고한다. `gen` 변수명, `:id` path 문법 등 edition 2024 비호환 패턴도 감사한다.
12. **Binary Decidability Pre-Check (agent-design-guide §3.5 대응)** — 각 카테고리를 평가하기 전에 "이 기준은 코드에서 객관적으로 PASS/FAIL 판정 가능한가?"를 먼저 자문하라. "더 나을 것 같다"처럼 주관 해석 여지가 남는 기준은 카테고리 평가 시작 시점에 근거 제약(파일:라인 + 출처 URL) 을 추가하여 이진 판정으로 재정식화한 뒤 평가한다. 예: "API Design 이 깔끔한지" → "핸들러 state 가 `Arc<dyn Port>` 인지 (파일:라인 + fit-pal §아키텍처 3번)".
13. **Rule-by-Rule Audit 프로토콜 (skill-design-guide §3.6 대응)** — `references/audit-criteria.md` 7 카테고리 × N 체크항목을 한 번에 묶어 "대체로 PASS/FAIL" 로 리포트하지 말고, 각 체크항목 단위로 개별 판정과 근거를 생성하라. 묶음 판정은 PASS 세부가 가려지고 FAIL 누락 추적이 불가능해진다. 리포트 표(Step 4) 각 row 는 한 체크항목에 대응한다.
14. **미검증 항목 마커 프로토콜 (evaluator v3 대응)** — 런타임 환경/외부 시스템 접근 불가(예: production DB pool 설정·실제 Redis 연결·OAuth provider 응답)로 L3 검증이 불가능한 항목은 **조용히 PASS 처리하지 말고** `[미검증]` 태그를 붙이고 근거에 이유를 기술하라 (예: `[미검증] production DB 접근 불가 — pool 설정 파일 정적 리뷰만 수행`). 미검증 2 건 이상은 CONDITIONAL APPROVE 규칙을 적용한다 (Step 4 참조).
15. **Sibling Consistency (skill-design-guide §8.8) — rust-audit ↔ backend-audit** — 동일 개념의 Rule-by-Rule 표 / CONDITIONAL APPROVE 판정 규칙 / 출처 URL 포맷을 backend-audit Step 3 와 parity 있게 유지한다. Rust 고유 카테고리(Ownership & Borrowing · unsafe 블록 · async Send+Sync · SQLx offline) 은 독립 row 로 추가하되, RFC 9457 / OWASP 같이 스택 공통인 원칙은 backend-audit 와 동일 문구로 인용한다.

# Process

## Gotchas

- **생성된 코드를 감사하지 마라** — `target/`, `generated/`, `*.generated.rs`, protobuf 출력 등 자동 생성 파일은 스캔 대상에서 제외하라. 수동 수정 불가능한 코드에 FAIL을 매기면 노이즈만 생긴다.
- **스타일 선호를 FAIL로 판정하지 마라** — `match` vs `if let`, `unwrap_or_else` vs `unwrap_or_default` 같은 동등한 관용구 차이는 INFO로 보고하되 FAIL 근거로 쓰지 마라.
- **quick 모드에서 전체 파일을 읽지 마라** — `git diff --name-only`로 변경 파일만 특정하고, 해당 파일만 읽어라. 전체 크레이트를 읽으면 토큰을 소진하고 리뷰 품질이 떨어진다.
- **clippy 경고와 감사 항목을 혼동하지 마라** — clippy가 이미 잡는 lint(unused_imports, dead_code)를 감사 리포트에 중복 나열하면 가치가 없다. 아키텍처/설계/보안 수준 이슈에 집중하라.
- **unsafe 블록을 무조건 FAIL로 처리하지 마라** — FFI 바인딩, 성능 크리티컬 경로에서 unsafe는 정당할 수 있다. `// SAFETY:` 주석 존재 여부와 실제 불변성 근거를 확인하라.
- **deep 모드에서 에이전트를 4개 초과 spawn하지 마라** — 병렬 에이전트가 많으면 컨텍스트 경합과 중복 발견이 발생한다. 카테고리별 최대 4개(아키텍처, 보안, 성능, 에러처리)로 제한하라.
- **Cargo.toml 의존성 버전을 감사 범위에서 빠뜨리지 마라** — `cargo audit`로 알려진 취약점을 확인하고, yanked 크레이트가 있는지 `cargo deny`도 체크하라.
- **테스트 코드에 프로덕션 수준 감사를 적용하지 마라** — `#[cfg(test)]` 모듈의 `unwrap()`, `expect()`, 하드코딩된 값은 테스트 맥락에서 정상이다. FAIL로 보고하면 false positive다.
- **리포트에 파일 경로 없이 발견 사항만 나열하지 마라** — 모든 항목에 `src/domain/auth.rs:42` 형식의 정확한 위치를 포함하라. 위치 없는 피드백은 실행 불가능하다.
- **이전 감사 결과를 참조하지 않고 매번 처음부터 시작하지 마라** — `.harness/` 디렉토리에 이전 감사 리포트가 있으면 읽어서 반복 지적을 피하고, 해결된 항목은 RESOLVED로 표시하라.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.

## 1. 대상 범위 결정

| 입력 | 범위 |
|------|------|
| 파일 경로 | 해당 파일만 |
| 디렉토리 경로 | 하위 전체 |
| 미지정 | `git diff --name-only` 기준 변경 파일 |

## 2. 모드 결정

| 모드 | 동작 |
|------|------|
| `quick` (기본) | 변경 파일만, 직접 검사, 경량 리포트 |
| `deep` | 전체 프로젝트, rust-reviewer 에이전트 위임, 상세 리포트 |

미지정 시: 변경 파일 5개 이하 → quick, 초과 → deep.

## 3-A. quick 모드 실행

references/audit-criteria.md를 읽고, 대상 파일을 직접 검사하여 카테고리별 PASS/FAIL 판정.

## 3-B. deep 모드 실행

rust-reviewer 에이전트를 Agent 도구로 호출:

```text
subagent_type: "rust-kit:rust-reviewer"
prompt: |
  다음 파일을 Rust 원칙 기준으로 평가하라.
  감사 기준: rust-kit/skills/rust-audit/references/audit-criteria.md
  대상 파일: [목록]
```

## 4. 리포트 생성 (Rule-by-Rule 표 — Gotcha 13 필수)

카테고리 순서는 `references/audit-criteria.md` 섹션 순서와 일치시킨다 (총 7 카테고리). 각 row 는 **하나의 체크항목(rule)** 에 대응하며, 카테고리 단위로 묶지 않고 개별 판정·근거·출처를 생성한다. 표 자리표시자(`...`) 금지.

| # | 카테고리 | 체크항목 | 판정 | 근거(파일:라인) | 출처 URL |
|---|----------|---------|------|-----------------|----------|
| 1 | Ownership & Borrowing | 불필요 `.clone()` 부재 | PASS/FAIL | `src/service/user.rs:42` Copy 타입에 clone 호출 0 건 | [Rust Book Ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html) |
| 2 | Ownership & Borrowing | `needless_pass_by_value` 위반 0 건 | PASS/FAIL | clippy 출력 해당 lint 0 건 | [Clippy needless_pass_by_value](https://rust-lang.github.io/rust-clippy/master/#needless_pass_by_value) |
| 3 | Error Handling | `?` 연산자 + `From` 구현 패턴 | PASS/FAIL | `src/domain/error.rs:1-40` thiserror 2 derive 사용 | [thiserror docs](https://docs.rs/thiserror/latest/thiserror/) |
| 4 | Error Handling | 프로덕션 경로 `.unwrap()/.expect()` 부재 | PASS/FAIL | `grep -rn "\.unwrap()\|\.expect(" src/ --include='*.rs' \| grep -v "#\[cfg(test)\]"` 결과 0 건 | fit-pal `server/CLAUDE.md` §에러 처리 |
| 5 | Async | `#[tokio::test(flavor = "multi_thread")]` 명시 (필요 시) | PASS/FAIL | `tests/integration/*.rs` Axum TestServer 케이스 확인 | [Tokio test attribute](https://docs.rs/tokio/latest/tokio/attr.test.html) |
| 6 | Async | blocking I/O 부재 (`std::fs::read` 등) | PASS/FAIL | async 함수 내 `std::thread::sleep`/`std::fs` 호출 0 건 | [Tokio spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html) |
| 7 | Async | trait 시그니처에 `Send + Sync` 일관 | PASS/FAIL | `src/domain/ports/*.rs` trait `Send + Sync` 선언 존재 | fit-pal `server/CLAUDE.md` §아키텍처 |
| 8 | Security | `unsafe` 블록 부재 또는 `// SAFETY:` 주석 필수 | PASS/FAIL | `grep -rn "unsafe {" src/` 결과 모두 주석 + `unsafe_code = "forbid"` 워크스페이스 lint | [Rust Reference Unsafe](https://doc.rust-lang.org/reference/unsafe-keyword.html) |
| 9 | Security | 시크릿 하드코딩 부재 | PASS/FAIL | `.env.example` + repo 내 `secret`/`token`/`password` 리터럴 0 건 | OWASP Top 10 A02 |
| 10 | Security | SQL injection 방어 (SQLx `query!`/`query_as!` 매크로 + bind 파라미터) | PASS/FAIL | `src/infra/db/*.rs` raw `format!("SELECT ...")` 0 건 | [SQLx query macro](https://docs.rs/sqlx/latest/sqlx/macro.query.html) |
| 11 | Performance | `large_futures` deny + `redundant_clone` deny workspace lint | PASS/FAIL | `Cargo.toml` `[workspace.lints.clippy]` 해당 lint 포함 | [Clippy lint index](https://rust-lang.github.io/rust-clippy/master/) |
| 12 | Performance | SQLx offline cache (`.sqlx/`) 존재 + CI 에서 `cargo sqlx prepare --check` 실행 | PASS/FAIL | `.sqlx/` 디렉토리 + CI workflow step 확인 | [SQLx prepare --check](https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md) |
| 13 | Testing | `#[sqlx::test]` 또는 `MockDatabase` 사용 (Docker 없는 단위 테스트 가능) | PASS/FAIL | `tests/*.rs` 각 테스트 어노테이션 확인 | [SeaORM MockDatabase](https://www.sea-ql.org/SeaORM/docs/write-test/mock/) |
| 14 | API Design | 핸들러 state 는 `Arc<dyn Port>` trait object (SK-03) | PASS/FAIL | `grep -n "State<PgPool>\|State<sqlx::" src/api/handlers/` 결과 0 건 | fit-pal `server/CLAUDE.md` §아키텍처 3번 |

위 표는 대표 rule 예시이며, 실제 리포트는 `references/audit-criteria.md` 의 모든 기준 rule 을 빠짐없이 열거해야 한다 (Rule-by-Rule Audit · Gotcha 13).

## 5. 최종 판정

판정 분류는 세 가지다:

- **APPROVE** — 전 row PASS + 미검증 태그 0 건.
- **CONDITIONAL APPROVE** — 전 row PASS 이지만 `[미검증]` 태그 1 건 존재. 리포트에 "미검증 1 건: [체크항목] — [이유]" 를 명시하고 환경 개선(예: production DB 접근권한 · MCP server 설정) 후 재검증 권고. 2 건 이상은 REJECT.
- **REJECT** — 1 건 이상 FAIL 또는 `[미검증]` 2 건 이상. 각 FAIL 에 대해 구체적 개선 액션(파일:라인 + 권장 변경 + 출처) 을 함께 제시한다.

# References

- references/audit-criteria.md — 카테고리별 PASS/FAIL 체크리스트 (존재 시 SSOT)
- backend-kit/skills/backend-audit/SKILL.md §Step 3 — 10 카테고리 Rule-by-Rule sibling ground truth
- harness/docs/guides/skill-design-guide.md §3.6 — Rule-by-Rule Audit 원칙 SSOT
- harness/docs/guides/agent-design-guide.md §3.5 · §10 · §12 — Binary Decidability · Unverifiable · L3 Coverage Honesty
