# Rust Audit Criteria

rust-reviewer 에이전트가 사용하는 유일한 감사 기준. 카테고리별 PASS/FAIL 조건을 정의한다. 2026-04 갱신 — Rust 2024 Edition, Axum 0.8, SeaORM 1.1, Clippy pedantic 2026 lint 세트 (fit-pal workspace.lints 실무 기준).

**적용 범위:** 아래 기준은 **cargo 가 관리하는 `.rs` 소스**에만 적용된다. 셸 스크립트 · compose ·
CI YAML · 클라이언트 코드에는 적용하지 마라 (`unwrap()`/`println!` 같은 기준이 그 스택에는 존재할 수
없어 항상 공허하게 통과한다). 스택별 대응 기준은 `rust-kit/references/project-detection.md` Step 0 표를
따른다.

**증거 유효성:** 각 기준을 PASS 로 확정하기 전에 `qa-evaluation-guide.md` §Evidence Validity Gate 의
4 검사(비공백 · 활성화 · 반증 가능성 · 출처)를 통과시킨다. **0 매치 grep · 0 개 실행 테스트는 PASS
근거가 아니다** — 대상 파일 수와 패턴 positive control 을 함께 기록해야 한다.

---

## 1. Ownership & Borrowing

| 기준 | PASS 조건 | 출처 |
| ------ | ----------- | ------ |
| 불필요한 clone | `.clone()` 호출이 빌림으로 대체 가능한 곳이 없다 (`redundant_clone`, `cloned_instead_of_copied`) | Clippy lints + fit-pal `workspace.lints.clippy` |
| &String / &Vec 사용 | 함수 인자에 `&String` 대신 `&str`, `&Vec<T>` 대신 `&[T]` 사용 (`ptr_arg`) | Clippy pedantic |
| needless_pass_by_value | `fn foo(x: String)`처럼 소유권을 받는데 참조로 충분한 경우 없다 | Clippy `needless_pass_by_value` (fit-pal deny) |
| Lifetime 명시 | 생략 가능한 lifetime을 불필요하게 명시하지 않는다 | Rust RFC 141 |
| RPIT capture (2024) | Rust 2024에서 `impl Trait` 반환이 필요 없는 lifetime을 capture하지 않는다 (`+ use<>` 명시 고려) | Rust Edition Guide 2024 |

## 2. Error Handling

| 기준 | PASS 조건 | 출처 |
| ------ | ----------- | ------ |
| unwrap/expect 범위 | **main 초기화와 테스트 코드 외에는** `.unwrap()` / `.expect()` 없다. `main()` 안의 `std::env::var("...").expect(...)` 같은 startup panic은 허용 | fit-pal `CLAUDE.md` §금지 사항 |
| 에러 타입 일관성 | 도메인 레이어는 `thiserror` 구체 enum만 사용. `anyhow::Error`는 app 최상위(main.rs, CLI)에서만 | fit-pal `CLAUDE.md` §코딩 컨벤션 |
| From impl | 에러 변환에 수동 매핑 대신 `#[from]` 또는 `From` impl 사용 | thiserror docs |
| 인프라 타입 누설 | 포트 trait 시그니처에 `sqlx::Error`, `DbErr`, `PgPool`, `DatabaseTransaction`, `reqwest::Error` 등 인프라 구체 타입 노출 없다 | fit-pal `CLAUDE.md` §아키텍처 2 |

## 3. Async

| 기준 | PASS 조건 | 출처 |
| ------ | ----------- | ------ |
| blocking in async | `std::thread::sleep`, `std::fs::*`, `reqwest::blocking::*` 등 blocking 호출이 async 함수 내에 없다 | Tokio docs |
| 불필요한 .await | 반환값을 사용하지 않는 `let _ = foo().await;` 패턴이 없다 (fire-and-forget이면 `tokio::spawn`) | Clippy |
| Mutex in async | `std::sync::Mutex` 대신 `tokio::sync::Mutex` 사용 (`.await`를 넘겨 잡으면) | Tokio docs |
| large_futures | 거대한 async 블록이 Future 크기를 키워 stack overflow 유발하지 않는다. `Box::pin`으로 heap 할당 유도 | Clippy `large_futures` (fit-pal deny) |
| Axum 0.8 async_trait | `FromRequest`/`FromRequestParts` 구현에 `#[async_trait]` 어노테이션이 **없다** (Axum 0.8 native async fn) | Axum 0.8 CHANGELOG |

## 4. Security

| 기준 | PASS 조건 | 출처 |
| ------ | ----------- | ------ |
| 시크릿 하드코딩 | API 키, JWT 시크릿, DB 비밀번호가 소스코드에 없다 — 환경변수 또는 Secrets Manager 경유 | OWASP + fit-pal `CLAUDE.md` §금지 사항 |
| unsafe_code | workspace-wide `unsafe_code = "forbid"`. `unsafe` 블록이 어떤 crate에도 없다 (외부 FFI는 별도 shared crate로 격리) | fit-pal `workspace.lints.rust` |
| SQL injection | 문자열 보간 대신 파라미터 바인딩 사용 (`sqlx::query!` / `$1`, SeaORM `ColumnTrait::eq`) | SQLx docs + SeaORM docs |
| 입력 검증 | 외부 입력(HTTP body, query param)에 `validator::Validate` 또는 명시적 길이/형식 검증이 있다 | fit-pal §API 설계 |
| 민감정보 로깅 | 패스워드, 토큰, 개인정보가 `tracing` 필드에 그대로 기록되지 않는다 (마스킹 또는 redact) | fit-pal `CLAUDE.md` §12 준수 |
| `println!` 금지 | 라이브러리 코드에 `println!`/`eprintln!`/`dbg!` 없다 — `tracing::info!`/`warn!`/`error!` 사용. **`.rs` 파일 한정 기준** (셸/CI 산출물에 적용 금지) | fit-pal `CLAUDE.md` §금지 사항 |
| 의존성 취약점 | `cargo audit` 또는 `cargo deny check advisories` 를 **실행**하여 advisory 0 건. 실행 없이 `deny.toml` 존재만으로 PASS 처리 금지 | [RustSec Advisory DB](https://rustsec.org/) |

## 5. Performance

| 기준 | PASS 조건 | 출처 |
| ------ | ----------- | ------ |
| 불필요한 allocation | 루프 내 불필요한 `String::new()` / `Vec::new()` 없다 | Clippy |
| collect 후 iterate | `.collect::<Vec<_>>()` 후 다시 `.iter()`하지 않는다 | Clippy |
| 사전 할당 | 크기를 아는 Vec에 `Vec::with_capacity()` 사용 | Rust Book |
| inefficient_to_string | `format!("{}", x)` 대신 `x.to_string()`, 또는 `&str` 직접 사용 | Clippy `inefficient_to_string` (fit-pal deny) |
| N+1 쿼리 | 리스트 조회 후 루프 안에서 `find_by_id`를 호출하지 않는다 — JOIN 또는 batch fetch 사용 | fit-pal `CLAUDE.md` §12 성능 |

## 6. Testing

| 기준 | PASS 조건 | 출처 |
| ------ | ----------- | ------ |
| 핵심 로직 테스트 | 비즈니스 로직 함수에 최소 1개 테스트 존재 | 일반 관행 |
| 에러 경로 테스트 | 주요 에러 경로(NotFound, Conflict, Validation)에 대한 테스트 존재 | 일반 관행 |
| 테스트 격리 | 테스트 간 상태 공유가 없다. 통합 테스트는 `serial_test` + TRUNCATE로 격리 | fit-pal `CLAUDE.md` §테스트 가능성 |
| Mock 주입 가능성 | 라우터 상태가 `Arc<dyn Port>` 형태 trait object. 테스트 시 mock 교체 가능 | fit-pal `CLAUDE.md` §테스트 가능성 |
| SeaORM MockDatabase | `HAS_SEAORM`이면 Docker 없는 단위 테스트에 `MockDatabase`를 활용하고 있다 | SeaORM 1.1 mock docs |
| 실 DB 통합 테스트 존재 | mock 단위 테스트와 **별도로** 실제 엔진 대상 테스트가 있다 (`#[sqlx::test]` 또는 testcontainers). mock 은 SQL 정합성을 검증하지 못하므로 mock-only 는 FAIL | [SeaORM mock 한계](https://www.sea-ql.org/SeaORM/docs/write-test/mock/) · [sqlx::test](https://docs.rs/sqlx/latest/sqlx/attr.test.html) |
| 테스트 실행 증거 | 감사 시 실행한 명령 · `running N tests` 의 N(>0) · 종료 코드가 근거에 기록돼 있다. N=0 은 PASS 가 아니라 타깃 필터/환경 오류 | [cargo-test 타깃 선택](https://doc.rust-lang.org/cargo/commands/cargo-test.html) |
| 마이그레이션 선적용 | 공유 DB 대상 통합 테스트가 있으면 스키마가 최신임을 확인했다 (`sqlx migrate info` pending 0 또는 마이그레이션 크레이트 실행). 컬럼 부재 실패를 코드 결함으로 오진하지 않는다 | [sqlx-cli](https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md) |

## 7. API Design

| 기준 | PASS 조건 | 출처 |
| ------ | ----------- | ------ |
| HTTP 메서드 일관성 | CRUD에 적절한 메서드 사용 (GET=조회, POST=생성, PUT/PATCH=수정, DELETE=삭제) | REST 관행 |
| 응답 코드 일관성 | 성공(200/201), 없음(404), 충돌(409), 입력 검증 실패(422), 서버 에러(500) 등 적절한 상태 코드 | HTTP spec |
| OpenAPI 정합 | `HAS_UTOIPA`면 모든 공개 엔드포인트에 `#[utoipa::path]` 존재, `ApiDoc` struct에 등록 | utoipa 5.4 docs |
| Axum 0.8 path 문법 | 모든 `.route(...)` 문자열이 `{id}` 중괄호 문법. `:id` colon 문법 0건 | Axum 0.8 CHANGELOG |
| Consumer-Owned Port | 모듈이 다른 모듈의 `port.rs`를 직접 import하지 않는다 — adapter는 Composition Root에서 주입 | fit-pal `CLAUDE.md` §아키텍처 1, 3 |
