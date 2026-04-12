---
name: rust-docker
description: >
  Rust 프로젝트용 Dockerfile과 docker-compose.yml을 생성한다.
  cargo-chef 기반 멀티스테이지 빌드로 의존성 캐싱을 최적화하고, 의존 서비스(PostgreSQL, Redis 등)를 docker-compose로 구성한다.
  "도커", "Dockerfile", "컨테이너", "배포 설정", "rust docker" 같은 요청 시 사용한다.
argument-hint: "[서비스명...]"
user-invocable: true
---

## Gotchas

- Rust 바이너리는 glibc에 동적 링크되어 있어서 distro가 다르면 실행 안 된다. `musl` 타겟으로 정적 링크하거나, 빌더(`rust:1-bookworm`)와 runtime(`debian:bookworm-slim`)을 같은 distro로 맞춰라.
- `cargo-chef`로 의존성 레이어를 분리하지 않으면 소스 한 줄만 바꿔도 전체 재빌드된다. `cargo chef prepare` → `cargo chef cook` 순서로 레이어를 나눠야 캐시가 유효하다.
- `.sqlx/` 디렉토리(SQLx offline mode 캐시)를 `.dockerignore`에서 제외하면 오프라인 모드(`SQLX_OFFLINE=true`)가 컨테이너 빌드 시 실패한다. `.sqlx/`는 반드시 이미지에 포함돼야 한다.
- **Multi-stage 빌드 필수** — 단일 stage로 빌드하면 최종 이미지에 `rustc`, `cargo`, 빌드 의존성(수백 MB)이 남는다. 최소 `builder` → `runtime` 2-stage를 사용하고, runtime stage는 `debian:bookworm-slim` 또는 `gcr.io/distroless/cc-debian12`로 한다.
- **Non-root 유저 실행 필수** — `USER root`로 실행하면 컨테이너 탈출 시 호스트 root 권한 획득 위험이 있다. runtime stage에서 `RUN adduser --disabled-password --no-create-home appuser` + `USER appuser`를 반드시 추가한다.
- **`.dockerignore` 누락 시 빌드 컨텍스트 폭발** — `target/`, `.git/`, `*.log`, `node_modules/`를 `.dockerignore`에 반드시 포함해라. `target/`만 빠져도 컨텍스트 전송에 수 GB, 수 분이 소요된다.
- **BuildKit 캐시 마운트 활용** — `RUN --mount=type=cache,target=/usr/local/cargo/registry` + `--mount=type=cache,target=/app/target`을 사용하면 cargo-chef 없이도 의존성 재다운로드를 방지할 수 있다. Dockerfile 첫 줄에 `# syntax=docker/dockerfile:1`을 명시해야 BuildKit 문법이 활성화된다.
- **HEALTHCHECK 누락** — orchestrator(docker-compose, k8s)가 컨테이너 상태를 판단하려면 `HEALTHCHECK CMD curl -f http://localhost:$PORT/health || exit 1`이 필요하다. 누락 시 unhealthy 컨테이너가 트래픽을 계속 받는다.
- **환경 변수 secrets 하드코딩 금지** — `ENV DATABASE_URL=postgres://...`를 Dockerfile에 넣으면 이미지 히스토리에 영구 기록된다. secrets는 반드시 `docker-compose.yml`의 `env_file` 또는 runtime `--env-file`로 주입한다.
- **Workspace 빌드 시 `--bin` 지정 필수** — mono-repo workspace에서 `cargo build --release`만 하면 모든 binary를 빌드하여 이미지 크기와 빌드 시간이 불필요하게 늘어난다. `cargo build --release --bin $BINARY_NAME`으로 타깃을 한정한다.
- **`EXPOSE` 포트와 실제 바인드 포트 불일치** — `EXPOSE 3000`은 문서용이지 실제 포트 매핑이 아니다. 앱이 `0.0.0.0:8080`에 바인드하면서 `EXPOSE 3000`만 써놓으면 디버깅 시 혼란을 준다. 앱의 실제 바인드 포트와 일치시켜라.
- **`COPY . .` 위치 주의** — cargo-chef cook 이후에 `COPY . .`를 하지 않으면 소스 코드가 없어 빌드 실패한다. 반대로 cook 이전에 `COPY . .`를 하면 소스 변경마다 의존성 캐시가 무효화된다. 순서: `COPY Cargo.toml Cargo.lock ./` → chef cook → `COPY . .` → `cargo build`.

# Dockerfile + docker-compose 생성

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 `$PACKAGE`, `IS_WORKSPACE`, `WORKSPACE_MEMBERS`, `HAS_SQLX`, `HAS_TOKIO`, `ARCH`를 사용한다.

기존에 `Dockerfile` 또는 `docker-compose.yml`이 있으면 읽어 수정 여부를 확인한다.

---

## 1. 의존 서비스 확인

`$ARGUMENTS`를 파싱하거나 `Cargo.toml` 의존성을 보고 필요한 서비스를 추론한다:

| 의존성 플래그 | 포함 서비스 |
|-------------|-----------|
| `HAS_SQLX` | PostgreSQL |
| `HAS_REDIS` (또는 redis 크레이트) | Redis |
| `HAS_RDKAFKA` | Kafka |
| 없음 | 앱 단독 |

확실하지 않으면 사용자에게 확인한다.

---

## 2. Dockerfile 생성 (cargo-chef 멀티스테이지)

workspace이면 `--workspace` 플래그와 `--bin $PACKAGE` 조합을 사용한다.

```dockerfile
# Stage 1: cargo-chef 준비
FROM rust:1-bookworm AS chef
RUN cargo install cargo-chef --locked
WORKDIR /app

# Stage 2: 의존성 레시피 생성
FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

# Stage 3: 의존성만 빌드 (캐시 레이어)
FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json

# 소스 복사 후 앱 빌드
COPY . .
ENV SQLX_OFFLINE=true
RUN cargo build --release --bin <package_name>

# Stage 4: 최소 런타임 이미지
FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/target/release/<package_name> /usr/local/bin/app
EXPOSE 8080
CMD ["app"]
```

`$PACKAGE`로 `<package_name>`을 치환한다. workspace이면 `--bin` 대상 바이너리를 사용자에게 확인한다.

---

## 3. docker-compose.yml 생성

의존 서비스에 따라 서비스를 구성한다. `healthcheck`로 앱이 DB 준비 전 시작하는 것을 방지한다.

```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgres://postgres:password@db:5432/appdb
      RUST_LOG: info
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

Redis가 필요하면 아래 서비스를 추가한다:

```yaml
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
```

---

## 4. .dockerignore 생성

빌드 컨텍스트를 최소화하되 `.sqlx/`는 반드시 포함한다:

```text
# 빌드 산출물
target/

# 개발 도구
.git/
.github/
.vscode/
.idea/

# 환경 설정 (시크릿 제외)
.env
.env.local

# 문서/테스트 (선택)
docs/
tests/
*.md

# .sqlx/ 는 제외하지 않는다 — SQLX_OFFLINE=true 빌드에 필요
```

`HAS_SQLX`이면 `.sqlx/`가 `.dockerignore`에 없는지 확인하고, 있으면 제거한다.

---

## 5. 추가 안내

### musl 정적 링크 (선택)

OpenSSL 의존성 없이 최소 이미지를 원하면:

```dockerfile
FROM rust:1-bookworm AS chef
RUN rustup target add x86_64-unknown-linux-musl
RUN apt-get update && apt-get install -y musl-tools
RUN cargo install cargo-chef --locked
WORKDIR /app

# ... (동일) ...

RUN cargo build --release --target x86_64-unknown-linux-musl --bin <package_name>

FROM scratch AS runtime
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/<package_name> /app
CMD ["/app"]
```

단, `sqlx`는 OpenSSL 필요 — `features = ["native-tls"]` 대신 `features = ["rustls"]`로 전환이 필요하다.

## After Creation

1. 생성된 파일 목록 출력: `Dockerfile`, `docker-compose.yml`, `.dockerignore`.
2. `HAS_SQLX`이면 빌드 전 `cargo sqlx prepare`로 `.sqlx/` 디렉토리를 생성해야 한다고 안내한다:
   ```bash
   DATABASE_URL=postgres://... cargo sqlx prepare
   ```
3. 다음 빌드/실행 명령을 안내한다:
   ```bash
   docker compose up --build
   ```
4. 다음 단계 안내:
   - CI/CD 파이프라인이 필요하면 GitHub Actions 워크플로우 추가를 제안하세요.
   - 프로덕션 배포를 준비한다면 시크릿을 환경변수 대신 Docker secrets 또는 Vault로 관리하세요.
