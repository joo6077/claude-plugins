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
- **키 네이밍 계층 구조 강제** — 번역 키는 `module.context.action` 형식(예: `user.profile.updated`)을 따라라. 평탄한 키(`profile_updated`)는 키 수가 100개를 넘으면 충돌과 검색 불가가 발생한다.
- **Fallback locale 미설정 시 빈 문자열 반환** — `rust-i18n`은 키가 없을 때 키 이름을 반환하지만, fluent는 빈 문자열을 반환할 수 있다. 항상 `fallback = "en"` 또는 기본 로케일을 `rust_i18n::set_locale()` 전에 설정해라.
- **Interpolation 변수 타입 불일치** — `rust-i18n`의 `t!("key", name = val)`에서 `val`은 `Display` trait을 구현해야 한다. `&str`이 아닌 커스텀 타입을 직접 전달하면 컴파일 에러가 난다. `.to_string()`으로 변환하거나 `Display`를 구현해라.
- **Plural form은 locale마다 규칙이 다르다** — 영어는 singular/plural 2개지만 러시아어는 3개, 아랍어는 6개다. fluent의 `PLURAL()` 함수를 사용하면 CLDR 규칙을 자동 적용한다. `rust-i18n`에서는 수동으로 키를 분기해야 하므로 복수형이 필요하면 fluent를 권장해라.
- **로케일 파일 위치 컨벤션** — `rust-i18n`은 기본적으로 `locales/` 디렉토리에서 `{locale}.toml` 또는 `{locale}.yaml`을 찾는다. 경로를 커스터마이즈하려면 `#[i18n(..., locales = "path")]` 매크로 인자를 정확히 지정해라. 상대 경로는 `Cargo.toml` 위치 기준이다.
- **번역 키 추가 후 모든 로케일 파일 동기화 필수** — 한 로케일에만 키를 추가하고 나머지를 누락하면 런타임에 fallback 키 이름이 사용자에게 노출된다. 키 추가 시 지원하는 모든 로케일 파일에 동시에 추가하고, 번역이 미확정이면 "NEEDS_TRANSLATION" 마커와 함께 영어 원문을 임시 삽입해라.

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
