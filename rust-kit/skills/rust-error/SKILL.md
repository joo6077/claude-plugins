---
name: rust-error
description: >
  Rust 프로젝트의 에러 처리 패턴을 안내한다. 3계층 에러 구조(InfraError → DomainError → ApiError)를 기반으로
  현재 코드의 에러 패턴을 분석하고 개선점을 제시하는 가이드형 스킬이다.
  "에러 처리", "error handling", "에러 타입", "Result", "rust error" 같은 요청 시 사용한다.
argument-hint: "[파일 또는 모듈 경로]"
user-invocable: true
---

## Gotchas

- **도메인 레이어에 `anyhow::Error` 금지** — 라이브러리/도메인 코드에는 **`thiserror` 기반 구체 enum만** 사용한다. `anyhow::Error`는 app 최상위(`apps/api/src/main.rs`, CLI 스크립트)에서만 허용. 도메인 에러에 anyhow를 섞으면 호출자가 `match`로 case를 분기할 수 없어 에러 처리가 전부 "generic 500"으로 퇴화한다. 출처: fit-pal `server/CLAUDE.md` §코딩 컨벤션.
- **`.unwrap()`/`.expect()` 는 `?` 치환이 아니라 타입 설계로 제거한다 (AP-05 회귀 방지 · E1→E3)** — 프로덕션 코드에서는 금지이며 **main 초기화와 테스트 코드**만 예외다 (fit-pal CLAUDE.md 금지 사항). 다만 발견 시 반사적으로 `?` 로 바꾸라고 제안하지 마라 — 2026-08-12 실측 REJECT `AP-05` (`personal_records.rs:139,142` 의 `into_entry()`) 는 `Option` 이 **논리상 불가능한데 타입에만 남아 있어서** 생긴 것이고, 같은 날 improvement 도 "구조상 non-optional 로 재설계하거나 `HashMap` 누적 방식으로 바꿔 `expect()` 제거" 를 권고했다. 제거 수단과 금지 목록은 **§4** 를 따르고, 강제는 workspace clippy deny lint(E3 게이트 — `rust-init` §4a)가 한다.
- **`unsafe` 금지** — workspace-wide `unsafe_code = "forbid"` 원칙. 외부 FFI가 반드시 필요한 경우 외에는 `unsafe` 블록을 만들지 마라. FFI가 필요하면 별도 shared crate로 격리한다. 출처: fit-pal `workspace.lints.rust` 및 `CLAUDE.md` §금지 사항.
- **`println!` 대신 `tracing::info!`/`tracing::warn!`/`tracing::error!`** — 구조화 로깅 없이는 OTel 트레이싱/필드 추출이 불가능하다. 라이브러리 코드에서는 `println!`/`eprintln!`/`dbg!`를 사용하지 마라.
- **`From<SrcError> for DstError` 누락 시 컴파일 에러** — `?` 연산자 체이닝 시 변환 경로를 먼저 확인하라. `#[from]` 또는 `impl From`을 추가한다.
- **에러 variant에 HTTP status code 매핑 필수** — API 레이어에서 `IntoResponse`를 구현할 때 모든 에러 variant에 적절한 status code를 매핑해라. `NotFound → 404`, `Unauthorized → 401`, `Conflict → 409`. 매핑 누락 시 모든 에러가 `500 Internal Server Error`로 퇴화한다.
- **에러 메시지에 내부 정보 노출 금지** — `Display` impl에 SQL 쿼리, 스택 트레이스, DB 스키마 정보를 포함하면 API 응답으로 유출된다. 사용자 대면 메시지와 내부 로깅 메시지를 분리해라. `tracing::error!`에는 상세 정보를, 응답에는 generic 메시지만 보낸다.
- **`#[from]` 남용 시 에러 출처 모호화** — `thiserror`의 `#[from]`은 편리하지만, 동일 source error(예: `std::io::Error`)가 여러 variant에서 `#[from]`으로 사용되면 컴파일 에러가 난다. 이 경우 수동 `impl From`으로 context를 추가하거나 variant를 세분화해라.
- **`anyhow::Context` trait을 도메인 에러에 쓰지 마라** — `.context("...")`는 `anyhow::Error`에만 체이닝 가능하다. 도메인 `thiserror` enum에 context를 추가하려면 별도 variant에 `String` 필드를 두거나 `#[error(transparent)]`로 inner error를 감싸라.
- **에러 enum variant 폭발 방지** — 하나의 에러 enum에 15개 이상의 variant가 생기면 도메인 경계를 재검토해라. 모듈별로 에러를 분리하고 상위 에러에서 `#[from]`으로 합성하는 계층 구조를 사용한다.
- **에러 크레이트 선택 Decision Table** — 용도에 따라 크레이트를 구분한다: **라이브러리/도메인** → `thiserror` (구조적 enum, `#[error]`/`#[from]`/`#[source]`), **애플리케이션 최상위** → `anyhow` (`context()`로 에러 체인 설명 추가), **CLI 도구** → `color-eyre` + `miette` (풍부한 panic hook + 색상 포맷 + 사용자 친화 에러 출력), **대규모 프로젝트** → `error-stack` (snafu 수준 context 강제 + anyhow 수준 편의성 균형, GreptimeDB 채택). 라이브러리에서 `anyhow`를 사용하면 타입 정보가 손실되어 호출자가 `match`로 분기할 수 없다.
- **`#[diagnostic::do_not_recommend]` 활용** — Rust 1.85+에서 라이브러리 author가 특정 trait impl을 컴파일러 에러 메시지에서 제외할 수 있다. 커스텀 에러 trait 계층이 복잡할 때 사용자에게 보이는 에러 메시지를 개선하는 데 유용하다.

# 에러 처리 패턴 가이드

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
`ARCH`, `IS_WORKSPACE`, `$PACKAGE`를 확인한다.

`Cargo.toml`에서 `thiserror`, `anyhow` 의존성 여부를 확인한다.
없으면 추가를 제안한다:

```toml
[dependencies]
thiserror = "2"
anyhow = "1"
```

---

## 1. 현재 에러 패턴 분석

`$ARGUMENTS`에서 파일/모듈 경로를 파싱한다. 경로가 없으면 에러 관련 파일을 자동으로 탐색한다:

```text
ARCH = workspace_service → crates/domain/src/errors.rs, crates/api/src/errors.rs, crates/infra/src/errors.rs
ARCH = modular          → src/domain/errors.rs, src/api/errors.rs, src/infra/errors.rs
ARCH = flat             → src/errors.rs
```

읽은 파일에서 다음을 파악한다:

| 항목 | 확인 내용 |
|------|---------|
| 에러 타입 정의 방식 | `thiserror`, `anyhow`, 직접 구현 |
| 계층 분리 여부 | Infra/Domain/Api 분리 또는 단일 에러 |
| `From` impl | 에러 타입 간 변환 경로 |
| `unwrap`/`expect` 사용 | 프로덕션 코드 내 위치 |
| `IntoResponse` impl | Axum HTTP 상태 코드 매핑 |

---

## 2. 3계층 에러 구조 제안

현재 구조를 분석한 뒤, 아래 3계층 구조로의 개선점을 제안한다.
이미 잘 구성된 경우 확인만 한다.

### 계층 구조

```text
InfraError (DB, 외부 API, IO)
    ↓ From impl
DomainError (비즈니스 규칙 위반, 리소스 없음)
    ↓ From impl  
ApiError (HTTP 응답 래퍼)
```

### Infra 계층 (`infra/errors.rs` 또는 `crates/infra/src/errors.rs`)

구체적인 외부 시스템 에러를 정의한다. SQLx, 외부 HTTP 클라이언트, IO 에러가 여기에 속한다:

```rust
#[derive(Debug, thiserror::Error)]
pub enum InfraError {
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("http client error: {0}")]
    HttpClient(#[from] reqwest::Error),
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
}
```

### Domain 계층 (`domain/errors.rs` 또는 `crates/domain/src/errors.rs`)

비즈니스 규칙 위반과 도메인 개념으로 표현된 에러를 정의한다. 인프라 구체 타입을 노출하지 않는다:

```rust
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("user not found: {0}")]
    UserNotFound(String),
    #[error("duplicate email: {0}")]
    DuplicateEmail(String),
    #[error("insufficient balance")]
    InsufficientBalance,
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}

// infra 에러를 domain 에러로 변환
impl From<InfraError> for DomainError {
    fn from(e: InfraError) -> Self {
        DomainError::Internal(anyhow::anyhow!(e))
    }
}
```

### Api 계층 (`api/errors.rs` 또는 `crates/api/src/errors.rs`)

`DomainError`를 HTTP 응답으로 변환한다. Axum의 `IntoResponse`를 구현한다:

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;

pub struct AppError(pub DomainError);

impl From<DomainError> for AppError {
    fn from(e: DomainError) -> Self {
        AppError(e)
    }
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self.0 {
            DomainError::UserNotFound(id) => (
                StatusCode::NOT_FOUND,
                format!("User not found: {id}"),
            ),
            DomainError::DuplicateEmail(email) => (
                StatusCode::CONFLICT,
                format!("Email already in use: {email}"),
            ),
            DomainError::InsufficientBalance => (
                StatusCode::UNPROCESSABLE_ENTITY,
                "Insufficient balance".to_string(),
            ),
            DomainError::Internal(_) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                "Internal server error".to_string(),
            ),
        };

        (status, Json(json!({ "error": message }))).into_response()
    }
}
```

---

## 3. 핸들러에서의 에러 전파

핸들러에서 `?` 연산자로 에러를 전파하는 패턴:

```rust
pub async fn get_user(
    State(service): State<Arc<dyn UserService>>,
    Path(id): Path<i64>,
) -> Result<Json<UserResponse>, AppError> {
    // DomainError → AppError 자동 변환 (From impl)
    let user = service.get_user(id).await?;
    Ok(Json(user.into()))
}
```

`From<DomainError> for AppError` impl이 있으면 `?`가 자동으로 변환한다.

---

## 4. 프로덕션 `.unwrap()`/`.expect()` 제거 — 치환보다 타입 설계

`?` 로 바꾸는 것은 **에러가 실제로 존재할 때만** 맞는 처방이다. "여기서는 절대 `None`/`Err` 일 리
없다" 는 주석이 붙는 자리는 에러 처리 문제가 아니라 **타입 설계 문제**다 — 검증 결과를 버리고
넓은 타입을 그대로 들고 다니면 같은 검증을 아래층에서 다시 하게 되고, 그 자리에 `expect()` 가
남는다 ([parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)).

### 판정 순서 (위에서부터)

| # | 질문 | 조치 |
| - | ---- | ---- |
| 1 | 이 `None`/`Err` 가 **논리상 발생 가능한가?** | 가능하면 → 도메인 에러로 승격 후 `?` 전파 |
| 2 | 불가능하다면 왜 타입에 남아 있는가? | 불가능한 상태를 **타입에서 제거** (아래 5 수단) |
| 3 | 지금 제거가 불가능한가? (외부 계약·대규모 리팩터) | 국소 `#[expect(clippy::expect_used, reason = "...")]` + 사유 명시. 범위는 그 표현식 한 줄 |

### 불가능한 상태를 제거하는 5 수단

| 수단 | 언제 | 효과 |
| ---- | ---- | ---- |
| **smart constructor** | 생성 시점에만 검증 가능한 불변식 | `Email::parse(s) -> Result<Email, _>` 이후로는 검증 없이 사용. 필드는 private |
| **`NonEmpty`** | "비어 있지 않은 컬렉션" 전제 | `first()`/`max()` 의 `Option` 이 사라진다 ([nonempty](https://docs.rs/nonempty/latest/nonempty/)) |
| **typestate** | 단계별로 허용 연산이 다른 객체 | 상태를 타입 파라미터로 올려 잘못된 순서 호출을 컴파일 에러로 만든다 ([typestate](https://cliffle.com/blog/rust-typestate/)) |
| **`builder` → `built` 분리** | 조립 중에는 `Option`, 완성 후에는 필수 | `Builder { a: Option<T> }` → `build()` 에서 한 번 검증 → `Built { a: T }`. 소비 측에 `Option` 이 새지 않는다 |
| **`HashMap::entry` 누적** | "첫 관찰 시 채우고 이후 갱신" 패턴 | `entry(k).or_insert_with(...)` 로 첫 값을 즉시 채워 `Option` 자체를 만들지 않는다 (실측 improvement 가 지목한 형태) |

### 강제는 문장이 아니라 lint 로 (E3)

같은 규칙이 세 표면에 문장으로 있었는데도 재발했다. `[workspace.lints.clippy]` 에 아래를 선언하면
`cargo clippy` 가 **매 실행마다** 판정한다 (선언·상속 형태는 `rust-init` §4a, 상속 확인은
`rust-audit` Gotcha 6):

```toml
[workspace.lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
panic_in_result_fn = "deny"
```

- 출처: Clippy [`unwrap_used`](https://rust-lang.github.io/rust-clippy/master/index.html#unwrap_used) ·
  [`expect_used`](https://rust-lang.github.io/rust-clippy/master/index.html#expect_used) ·
  [`panic`](https://rust-lang.github.io/rust-clippy/master/index.html#panic) ·
  `panic_in_result_fn` (같은 lint 인덱스에서 조회),
  상속은 [Cargo `[workspace.lints]`](https://doc.rust-lang.org/cargo/reference/workspaces.html#the-lints-table).
- main 초기화 예외는 가능하면 `main() -> Result<(), ConfigError>` 로 줄인다. 남기는 경우에만
  국소 `#[expect(..., reason = "startup invariant …")]` 를 붙인다.
- 이 lint 들은 테스트 타깃에도 적용된다. 테스트 코드 예외는 **`#[cfg(test)]` 스코프 안에서만**
  선언하고, crate 루트(`lib.rs`/`main.rs`)에 crate-wide 로 열지 마라. 프로젝트가 clippy 설정으로
  테스트 예외를 다루고 있으면 그 설정을 먼저 확인한다 (이번 근거 범위 밖이므로 특정 키를
  단정하지 않는다).

### 넣지 말 것 (제거처럼 보이지만 아닌 것)

- **`unwrap_or_default()` 로 치환하지 마라.** 실패를 기본값으로 삼켜 결함을 조용한 오동작으로
  바꾼다. 값이 없을 때 무엇이 맞는지 모른다면 그건 도메인 결정이지 기본값이 아니다.
- **"더 좋은 메시지의 `expect`" 로 바꾸는 것은 제거가 아니다.** panic 은 그대로 남는다.
- **broad `#[allow(...)]` 금지.** 파일·모듈 단위로 lint 를 끄면 게이트가 사라진다. 예외는
  표현식 단위 `#[expect(..., reason = "...")]` 만 허용한다.
- **전체 `clippy::restriction` 그룹을 deny 로 켜지 마라.** 서로 모순되는 lint 가 섞여 있어
  게이트가 무력화되고, 위 4 개만 필요하다.

---

## 5. 개선점 보고

분석 결과를 바탕으로 현재 코드의 문제점과 권장 조치를 정리한다:

| 항목 | 현재 상태 | 권장 조치 |
|------|---------|---------|
| 에러 계층 분리 | (분석 결과) | (필요 시 분리 제안) |
| `unwrap`/`expect` | (발견 위치) | §4 판정 순서 적용 — 발생 가능하면 도메인 에러 + `?`, 불가능하면 타입 설계로 제거 |
| clippy panic 계열 deny | (`[workspace.lints.clippy]` 선언 여부) | 미선언이면 §4 의 4 lint 추가 (E3 게이트) |
| `From` impl 누락 | (누락 경로) | impl 추가 |
| HTTP 상태 코드 매핑 | (매핑 존재 여부) | `IntoResponse` impl 추가 |
| 에러 메시지 노출 | (Internal 에러 노출 여부) | `Internal` 케이스는 generic 메시지 반환 |

코드 수정을 원하면 사용자에게 확인 후 진행한다. 이 스킬은 기본적으로 가이드형이며, 수정은 명시적 요청이 있을 때만 수행한다.

## After Analysis

1. 현재 에러 구조 요약 (계층 분리 여부, thiserror/anyhow 사용 여부).
2. 발견된 문제점 목록 (`unwrap`, `From` 누락, HTTP 매핑 미흡 등).
3. 권장 개선 순서:
   - 급함: `unwrap`/`expect` 제거(§4 판정 순서 — 치환이 아니라 타입 설계 우선) → 비즈니스 에러 정의 → `IntoResponse` 구현
   - 점진: 계층 분리 리팩토링 (기존 코드가 단일 에러 타입인 경우)
4. 수정을 원하면 `rust-service`, `rust-api` 스킬과 함께 사용하도록 안내한다.
