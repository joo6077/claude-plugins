---
name: rust-l10n
description: >
  Rust 백엔드 프로젝트에 i18n을 설정하거나 번역 키를 추가/수정한다.
  rust-i18n 또는 fluent 기반으로 로케일 파일을 관리하고 Accept-Language 미들웨어를 구성한다.
  "다국어", "번역", "i18n", "l10n", "국제화", "rust l10n" 같은 요청 시 사용한다.
argument-hint: "<locale> <key> [value]"
user-invocable: true
---

## Gotchas

- **변수 플레이스홀더 일관성 필수** — 번역 키의 변수(`%{name}`)는 모든 로케일 파일에 동일하게 존재해야 한다. 한 로케일에만 있으면 다른 로케일에서 런타임 패닉이 난다.
- **`rust-i18n`은 컴파일 타임 키 검증 없음** — 키 오타 시 런타임에 키 이름 그대로 반환되므로, 생성 후 실제 응답을 확인해야 한다.
- **Accept-Language 헤더 파싱** — quality factor(`q=0.9`) 처리가 복잡하다. `accept-language` 크레이트를 사용하고 직접 파싱하지 마라.
- **Axum 0.8 호환성** — `axum::extract::Request`, `axum::middleware::Next`, `axum::response::Response`, `axum::middleware::from_fn` API는 Axum 0.8에서도 그대로 유지된다. 이 스킬의 Locale middleware 패턴은 0.8에서도 동일하게 동작. 단 라우터 등록 시 path 문자열은 `{id}` 문법을 사용할 것 (rust-api 참조).

# 백엔드 i18n 설정 + 번역 키 추가

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
`HAS_RUST_I18N`과 `HAS_FLUENT`를 확인한다.

---

## 1. i18n 라이브러리 확인

### 이미 설치된 경우

`HAS_RUST_I18N` → rust-i18n 기반으로 진행한다.
`HAS_FLUENT` → fluent 기반으로 진행한다.

### 미설치인 경우

두 옵션을 제안하고 사용자가 선택하게 한다:

| 라이브러리 | 특징 | 권장 케이스 |
|-----------|------|------------|
| `rust-i18n` | TOML 기반, 간단한 API (`t!` 매크로) | 대부분의 백엔드 앱 |
| `fluent` | Mozilla Fluent 포맷, 복잡한 pluralization | 복잡한 언어 규칙 필요 시 |

기본값은 `rust-i18n`을 권장한다. 선택 후 `Cargo.toml`에 추가를 안내한다:

```toml
# Cargo.toml
[dependencies]
rust-i18n = "3"
accept-language = "3"
```

---

## 2. 신규 설정 (첫 설정인 경우)

### 2a. i18n 초기화 매크로 추가

`src/main.rs` 또는 `src/lib.rs`에 매크로를 추가한다:

```rust
// src/main.rs
use rust_i18n::i18n;

i18n!("locales", fallback = "en");
```

### 2b. 로케일 디렉토리 생성

`locales/` 디렉토리를 생성하고 기본 로케일 파일을 만든다:

```toml
# locales/en.toml
[messages]
hello = "Hello, %{name}!"
user_not_found = "User not found: %{id}"
email_sent = "Verification email sent to %{email}"

[errors]
unauthorized = "Unauthorized"
internal = "Internal server error"
```

```toml
# locales/ko.toml
[messages]
hello = "안녕하세요, %{name}님!"
user_not_found = "사용자를 찾을 수 없습니다: %{id}"
email_sent = "인증 이메일이 %{email}로 발송되었습니다"

[errors]
unauthorized = "인증이 필요합니다"
internal = "내부 서버 오류"
```

### 2c. Accept-Language 미들웨어 추가

```rust
// api/middleware/locale.rs
use axum::{
    extract::Request,
    middleware::Next,
    response::Response,
};
use accept_language::parse;

pub async fn locale_middleware(mut req: Request, next: Next) -> Response {
    let locale = req
        .headers()
        .get("Accept-Language")
        .and_then(|v| v.to_str().ok())
        .map(|s| parse(s))
        .and_then(|langs| langs.into_iter().next())
        .unwrap_or_else(|| "en".to_string());

    req.extensions_mut().insert(Locale(locale));
    next.run(req).await
}

#[derive(Clone)]
pub struct Locale(pub String);
```

라우터에 레이어를 추가한다:

```rust
// api/router.rs
use axum::middleware;
use crate::api::middleware::locale::locale_middleware;

Router::new()
    // ... routes ...
    .layer(middleware::from_fn(locale_middleware))
```

---

## 3. 기존 로케일 패턴 읽기

`locales/` 디렉토리의 기존 파일을 읽어 다음을 파악한다:

- 키 네이밍 컨벤션 (snake_case, dot-notation 등)
- 섹션 구조 (`[messages]`, `[errors]`, feature별 섹션 등)
- 지원 로케일 목록

---

## 4. 번역 키 추가/수정

`$ARGUMENTS`에서 로케일, 키, 값을 파싱한다. 인자가 없으면 사용자에게 확인한다:

| 항목 | 예시 |
|------|------|
| 키 경로 | `messages.order_created` |
| 플레이스홀더 | `%{order_id}` |
| 지원 로케일 | `en`, `ko`, `ja` |

**모든 로케일 파일에 동시에** 키를 추가한다. 번역 값이 없는 로케일은 영어 값을 fallback으로 채우고 주석을 달아둔다:

```toml
# locales/ja.toml
[messages]
# 번역 대기 (fallback: EN)
order_created = "Order created: %{order_id}"
```

---

## 5. 핸들러에서 사용

번역 키를 핸들러에서 사용하는 방법을 안내한다:

```rust
use axum::extract::Extension;
use rust_i18n::t;
use crate::api::middleware::locale::Locale;

pub async fn create_order(
    Extension(Locale(locale)): Extension<Locale>,
    // ...
) -> impl IntoResponse {
    let message = t!("messages.order_created", order_id = "ORD-001", locale = &locale);
    Json(serde_json::json!({ "message": message }))
}
```

---

## 6. 빌드 확인

```bash
cargo build
```

`rust-i18n`은 컴파일 타임에 로케일 파일을 embed한다. 빌드 성공 후 실제 Accept-Language 헤더로 응답을 확인하도록 안내한다.

## After Creation

1. 생성/수정된 파일 목록 출력.
2. 추가된 번역 키 목록과 지원 로케일을 표로 정리한다.
3. 번역 대기 주석이 있는 로케일(번역 미완성)이 있으면 명시한다.
4. 다음 단계 안내:
   - 새 로케일을 추가하려면 `locales/<code>.toml` 파일을 생성하고 기존 키를 모두 채우세요.
   - 에러 메시지 국제화는 `rust-error` 스킬의 에러 타입에 locale을 전달하는 패턴을 참고하세요.
