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

## 4. 리포트 생성

| 카테고리 | 판정 | 근거 |
|----------|------|------|
| Ownership & Borrowing | {PASS/FAIL} | {파일:라인 + 설명} |
| Error Handling | {PASS/FAIL} | |
| Async | {PASS/FAIL} | |
| Security | {PASS/FAIL} | |
| Performance | {PASS/FAIL} | |
| Testing | {PASS/FAIL} | |
| API Design | {PASS/FAIL} | |

**최종 판정:** {APPROVE / REJECT}
**FAIL 수:** {N}개

# References

- references/audit-criteria.md — 카테고리별 PASS/FAIL 체크리스트
