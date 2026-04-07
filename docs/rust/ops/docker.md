---
title: Docker 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# Docker 원칙

`cargo-chef 0.1.x`를 활용한 멀티스테이지 빌드로 Docker 레이어 캐시를 극대화한다. 의존성 레이어를 소스 레이어와 분리하여 소스만 변경될 때 의존성 재컴파일을 방지한다.

---

## 원칙

### 1. `cargo-chef` 3단계 멀티스테이지 패턴을 사용한다

```dockerfile
# syntax=docker/dockerfile:1

# ── 1단계: planner ──────────────────────────────────────────
FROM rust:1.87-slim AS planner
WORKDIR /app
RUN cargo install cargo-chef --locked
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

# ── 2단계: builder ──────────────────────────────────────────
FROM rust:1.87-slim AS builder
WORKDIR /app
RUN cargo install cargo-chef --locked
COPY --from=planner /app/recipe.json recipe.json

# 의존성만 먼저 컴파일 (캐시 레이어)
RUN cargo chef cook --release --recipe-path recipe.json

# 소스 복사 후 최종 빌드
COPY . .
RUN cargo build --release --bin my-server

# ── 3단계: runtime ───────────────────────────────────────────
FROM debian:bookworm-slim AS runtime
WORKDIR /app

# 런타임 의존성만 설치
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/my-server /usr/local/bin/my-server

EXPOSE 8080
CMD ["my-server"]
```

### 2. musl로 완전 정적 바이너리를 만들면 runtime stage를 `scratch`로 줄인다

```dockerfile
FROM rust:1.87-slim AS builder
WORKDIR /app
RUN rustup target add x86_64-unknown-linux-musl
RUN apt-get update && apt-get install -y musl-tools

RUN cargo install cargo-chef --locked
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --target x86_64-unknown-linux-musl --recipe-path recipe.json

COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl --bin my-server

FROM scratch AS runtime
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/my-server /my-server
EXPOSE 8080
ENTRYPOINT ["/my-server"]
```

### 3. `.dockerignore`로 불필요한 파일을 제외한다

```dockerignore
target/
.git/
.github/
*.md
.env
.env.*
docs/
tests/
```

`target/` 디렉토리는 수 GB에 달할 수 있다. 반드시 제외한다.

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| cargo-chef 버전 | 0.1.77 | `--locked` 플래그로 고정 |
| runtime base image | `debian:bookworm-slim` | glibc 링크 시. musl이면 `scratch` |
| 최종 이미지 크기 | 20~50MB (slim), ~10MB (musl+scratch) | |
| Rust toolchain | `rust:1.87-slim` | 모든 stage에서 동일 버전 사용 |

---

## 안티패턴

### 단일 스테이지 빌드

소스 한 줄이 바뀌어도 모든 의존성을 재컴파일한다. cargo-chef 3단계 패턴으로 의존성 레이어를 캐시한다.

### `cargo-chef` 없이 `Cargo.toml`만 복사

`COPY Cargo.toml Cargo.lock ./` 후 더미 `src/main.rs`를 만드는 수동 패턴은 workspace에서 깨지기 쉽다. `cargo-chef`가 더 안정적이다.

### `target/`을 `.dockerignore`에서 제외 누락

로컬 빌드 후 Docker 빌드를 실행하면 수 GB의 `target/`이 빌드 컨텍스트에 포함된다. 첫 번째 줄에 `target/`을 추가한다.

### runtime stage에 빌드 도구 포함

`rust:latest`를 runtime image로 사용하면 이미지 크기가 1GB 이상이 된다. 바이너리만 `debian:slim` 또는 `scratch`로 복사한다.

---

## Gotchas

### `cargo chef cook`과 `cargo build`의 `--target` 플래그를 일치시켜야 한다

musl 빌드 시 `cargo chef cook --target x86_64-unknown-linux-musl`과 `cargo build --target x86_64-unknown-linux-musl`을 동일하게 설정해야 캐시가 유효하다.

### OpenSSL vs rustls

`debian:slim` 런타임에서 OpenSSL 링크 에러가 나면 `libssl-dev` 설치 또는 `rustls` feature로 전환한다. sqlx의 경우 `runtime-tokio-rustls` feature를 사용하면 OpenSSL 의존성이 없어진다.

### `cargo install cargo-chef --locked`의 `--locked`가 중요하다

`--locked`가 없으면 최신 버전으로 업그레이드될 수 있고, planner/builder 단계 간 버전 불일치가 발생한다.

### 워크스페이스 구조에서 `COPY . .` 위치가 중요하다

`cargo chef prepare`는 전체 workspace를 스캔한다. `COPY . .` 이전에 일부 파일만 복사하면 `recipe.json`이 불완전하게 생성된다.
