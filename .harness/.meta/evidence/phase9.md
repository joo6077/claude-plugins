---
phase: 9
title: "Phase 9 rust-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

출처 유형: WebSearch fallback  
웹 검색 쿼리: 0/10, 공식 URL 직접 조회

**1. 관찰 사실**
- 현행 버전: docs.rs latest 기준 `axum 0.8.9`, `sqlx 0.9.0`, `sea-orm 2.0.1`, `testcontainers 0.28.0`입니다. rust-kit 템플릿의 `sqlx = "0.8"`와 `sea-orm = "1.1"`은 낡았습니다. 출처: https://docs.rs/axum/latest/axum/ · https://docs.rs/sqlx/latest/sqlx/ · https://docs.rs/sea-orm/latest/sea_orm/ · https://docs.rs/testcontainers/latest/testcontainers/
- Axum 0.8 관찰: path 문법은 `/:id`, `/*rest`에서 `/{id}`, `/{*rest}`로 바뀌었고, custom extractor의 `#[async_trait]` 제거가 필요합니다. rust-api의 방향은 맞지만 “announcement 2024-12-01” 표기는 공식 블로그 기준 `2025-01-01`로 고쳐야 합니다. 출처: https://tokio.rs/blog/2025-01-01-announcing-axum-0-8-0 · https://github.com/tokio-rs/axum/blob/main/axum/CHANGELOG.md
- J1: `.expect()` 제거는 단순히 `?`로 바꾸는 문제가 아니라 “불가능한 상태를 타입으로 제거”해야 하는 케이스입니다. `parse, don’t validate`는 검증 결과를 버리지 말고 더 정밀한 타입으로 반환하라는 패턴이고, `NonEmpty`는 빈 컬렉션 가능성을 타입에서 제거합니다. Typestate는 상태별 허용 연산을 타입으로 제한합니다. 출처: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ · https://docs.rs/nonempty/latest/nonempty/ · https://cliffle.com/blog/rust-typestate/
- J1 lint: 현행 Clippy lint 이름은 `clippy::unwrap_used`, `clippy::expect_used`, `clippy::panic`, `clippy::panic_in_result_fn`입니다. Cargo는 `[workspace.lints]`와 member crate의 `[lints] workspace = true` 상속을 지원합니다. 출처: https://rust-lang.github.io/rust-clippy/master/index.html#unwrap_used · https://rust-lang.github.io/rust-clippy/master/index.html#expect_used · https://rust-lang.github.io/rust-clippy/master/index.html#panic · https://doc.rust-lang.org/cargo/reference/workspaces.html#the-lints-table
- J2: `#[sqlx::test]`는 “테스트별 트랜잭션 롤백”이 아니라, 함수별 새 테스트 DB를 만들고 live connection을 제공하며 성공 시 정리합니다. Postgres/MySQL은 `DATABASE_URL`이 필요하고, `migrations` 폴더가 있으면 자동 적용됩니다. rust-test의 “트랜잭션 제공/롤백 자동” 문구는 수정해야 합니다. 출처: https://docs.rs/sqlx/latest/sqlx/attr.test.html
- J2: SQLx `query!`는 빌드 시 `DATABASE_URL` 또는 workspace root의 `.sqlx` 캐시가 필요하고, 쿼리는 string literal이어야 정적 검증됩니다. 출처: https://docs.rs/sqlx/latest/sqlx/macro.query.html
- J2: SeaORM `MockDatabase`는 mock 응답을 주입하는 단위 테스트 도구입니다. 추론: transaction log로 “어떤 SQL/statement가 만들어졌는지”는 확인할 수 있지만, 실제 PostgreSQL JSONB equality predicate가 행을 걸러내는지는 검증하지 못합니다. conflict guard 판별력은 `#[sqlx::test]` 또는 testcontainers 같은 실제 DB 엔진 테스트가 필요합니다. 출처: https://www.sea-ql.org/SeaORM/docs/write-test/mock/ · https://docs.rs/testcontainers/latest/testcontainers/
- J2: cargo-mutants는 “버그를 넣어도 테스트가 실패하지 않는 지점”을 찾는 mutation testing 도구입니다. guard 삭제 mutant가 살아남는지 보는 데 적합하지만, deterministic negative test를 대체하면 안 됩니다. 출처: https://mutants.rs/
- J3: `cargo metadata --format-version 1 --no-deps`의 `packages[].targets[].kind`가 `lib`, `bin`, `test`, `bench` 등을 담습니다. `cargo test`는 필터가 없으면 unit/integration/doc tests를 컴파일·실행합니다. 바이너리 전용 crate에 `--lib`를 붙이면 안 됩니다. 출처: https://doc.rust-lang.org/cargo/commands/cargo-metadata.html · https://doc.rust-lang.org/cargo/commands/cargo-test.html
- Rust 2024: Rust 1.85.0에서 stable이며 `edition = "2024"`는 resolver 3을 암시합니다. virtual workspace는 resolver를 명시해야 합니다. 출처: https://blog.rust-lang.org/2025/02/20/Rust-1.85.0/ · https://doc.rust-lang.org/edition-guide/rust-2024/cargo-resolver.html

**2. 권장안**
- rust-error/rust-reviewer에 추가: “프로덕션 `.unwrap()`/`.expect()`는 `?` 치환 전에 타입 설계 제거를 우선한다. `Option`이 논리상 불가능하면 최종 도메인 타입에 남기지 말고 smart constructor, `NonEmpty`, typestate, builder→built 분리, 또는 `HashMap::entry` 누적 구조로 재설계한다.”
- workspace lint 권장 조항:
  ```toml
  [workspace.lints.clippy]
  unwrap_used = "deny"
  expect_used = "deny"
  panic = "deny"
  panic_in_result_fn = "deny"
  arc_with_non_send_sync = "deny"
  ```
  main 초기화 예외는 가능하면 `Result` 반환으로 줄이고, 남기는 경우 국소 `#[expect(..., reason = "...startup invariant...")]`만 허용.
- 넣지 말 것: `unwrap_or_default`, “더 좋은 메시지의 expect”, broad `#[allow(...)]`, 전체 `clippy::restriction = deny`.
- rust-test에 추가: “DB guard는 호출부를 함수로 추출하고 `rows_affected == 0 → Conflict`를 반환하게 한다. positive test와 stale expected value negative test를 모두 live DB에서 실행한다.”
- rust-test 문구 수정: `#[sqlx::test]`는 “독립 트랜잭션”이 아니라 “테스트별 새 DB + 자동 migration + 성공 cleanup”으로 설명.
- MockDatabase 조항 수정: “단위 테스트 전용. rows_affected 매핑, repository control flow, generated statement/log assertion에는 사용 가능. 실제 SQL predicate 의미 검증 또는 통합 테스트로 보고 금지.”
- J3 조항 유지·강화: 테스트 명령 전 `cargo metadata`로 target kind를 열거하고, 기본은 무필터 `cargo test --workspace`. 필터를 붙이면 `running N tests`의 `N > 0`을 증거로 요구.

**3. 트레이드오프**
- 타입 설계는 초기 리팩터 비용이 있지만, production `expect()`와 중복 검증을 구조적으로 줄입니다.
- live DB negative test는 느리고 `DATABASE_URL`/권한이 필요하지만, JSONB predicate와 row count 의미를 검증합니다.
- MockDatabase는 빠르고 CI 친화적이지만 SQL 의미 검증력이 없습니다.
- SQLx 0.9/SeaORM 2.0 반영은 최신성은 얻지만, 기존 프로젝트가 0.8/1.1에 고정돼 있으면 migration 비용이 생깁니다.

**4. 열린 질문**
- rust-kit 템플릿을 즉시 `sqlx 0.9`, `sea-orm 2.0`으로 올릴지, “프로젝트 pinned 버전 우선 + 문서 조회 필수”로 둘지 결정 필요.
- main 초기화 예외를 계속 허용할지, 모든 startup config를 `Result<AppConfig, ConfigError>`로 강제할지 결정 필요.
- CI에서 Postgres superuser `DATABASE_URL` 또는 Docker/testcontainers 사용이 가능한지 확인 필요.
- cargo-mutants를 전체 workspace gate로 둘지, guard 변경 파일/패키지 한정 수동 gate로 둘지 범위 결정 필요.
