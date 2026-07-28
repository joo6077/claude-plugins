---
title: CI/CD 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# CI/CD 원칙

GitHub Actions에서 Rust 프로젝트의 빌드, 테스트, 보안 감사를 자동화한다. `cargo-nextest`로 빠른 테스트, `cargo-deny`로 의존성 보안 감사, `sccache`로 컴파일 캐시를 구성한다.

---

## 원칙

### 1. 표준 CI 워크플로우는 check → test → lint → audit 단계로 구성한다

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  CARGO_TERM_COLOR: always
  RUSTFLAGS: "-D warnings"

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo check --all-targets

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v7
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - uses: taiki-e/install-action@nextest
      - run: cargo nextest run --all-features
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/testdb

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - uses: Swatinem/rust-cache@v2
      - run: cargo fmt --all -- --check
      - run: cargo clippy --all-targets --all-features -- -D warnings

  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: taiki-e/install-action@cargo-deny
      - run: cargo deny check
```

### 2. `cargo-nextest`로 테스트 속도를 높인다

`cargo-nextest`는 테스트를 프로세스 단위로 격리하여 병렬 실행한다. 기존 `cargo test`보다 2~3배 빠른 경우가 많다.

```yaml
- uses: taiki-e/install-action@nextest
- run: cargo nextest run
# 특정 테스트만 실행
- run: cargo nextest run --test integration_tests
# 느린 테스트 타임아웃 설정
- run: cargo nextest run --test-threads 4
```

### 3. `cargo-deny`로 의존성 보안과 라이선스를 감사한다

```toml
# deny.toml
[advisories]
db-path = "~/.cargo/advisory-db"
db-urls = ["https://github.com/rustsec/advisory-db"]
vulnerability = "deny"
unmaintained = "warn"
yanked = "deny"

[licenses]
allow = ["MIT", "Apache-2.0", "Apache-2.0 WITH LLVM-exception", "ISC", "Unicode-DFS-2016"]
deny = ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]

[bans]
multiple-versions = "warn"
```

### 4. `Swatinem/rust-cache`로 빌드 캐시를 공유한다

```yaml
- uses: Swatinem/rust-cache@v2
  with:
    # 워크스페이스 루트 명시 (기본값은 자동 감지)
    workspaces: ". -> target"
    # 캐시 키 추가 구분자
    key: "v1"
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| Rust toolchain action | `dtolnay/rust-toolchain@stable` | 고정 버전보다 `stable` 권장 |
| 캐시 action | `Swatinem/rust-cache@v2` | `actions/cache` 직접 사용보다 간편 |
| `RUSTFLAGS` | `-D warnings` | 경고를 에러로 처리 |
| nextest 설치 | `taiki-e/install-action@nextest` | 바이너리 직접 다운로드, 빠름 |

---

## 안티패턴

### `cargo test` 대신 `cargo nextest` 미사용

`cargo test`는 테스트 바이너리를 순차적으로 실행한다. `cargo-nextest`는 더 세밀한 병렬화와 더 나은 출력을 제공한다.

### 캐시 없이 매 CI 실행마다 전체 재컴파일

의존성 컴파일은 수 분이 걸릴 수 있다. `Swatinem/rust-cache`는 `~/.cargo/registry`, `~/.cargo/git`, `target/` 를 캐시한다.

### `clippy`를 `-- -D warnings` 없이 실행

경고를 에러로 처리하지 않으면 clippy가 통과해도 코드 품질이 저하된다. `-D warnings`를 항상 붙인다.

### `cargo audit` 대신 `cargo deny` 미사용

`cargo audit`은 취약점만 검사한다. `cargo deny`는 라이선스, 중복 의존성, yanked 크레이트까지 통합 검사한다.

---

## Gotchas

### `SQLX_OFFLINE=true`를 CI 환경에 설정해야 한다

DB 없는 CI 단계(check, lint)에서 sqlx query 매크로를 컴파일하려면 `.sqlx/` 캐시와 `SQLX_OFFLINE=true`가 필요하다.

```yaml
env:
  SQLX_OFFLINE: "true"
```

### `dtolnay/rust-toolchain`은 `rust-toolchain.toml`을 자동으로 읽는다

프로젝트 루트에 `rust-toolchain.toml`이 있으면 toolchain 버전이 자동으로 고정된다. action에 별도 버전을 명시하지 않아도 된다.

### `cargo-deny`의 `deny.toml`이 없으면 `cargo deny check`가 실패한다

`cargo deny init`으로 기본 설정 파일을 생성한 뒤 커밋한다.

### GitHub Actions의 서비스 컨테이너는 `localhost`로 접근한다

`services.postgres`로 정의한 PostgreSQL은 `localhost:5432`로 접근한다. `DATABASE_URL`에 `localhost`를 사용한다.
