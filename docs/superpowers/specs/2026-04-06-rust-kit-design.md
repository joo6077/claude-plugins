# rust-kit 설계 스펙

> Rust 전용 백엔드 개발 워크플로우 플러그인. flutter-toolkit 패턴을 따르되 Rust 생태계에 맞게 조정.

## 결정 사항

- **독립 플러그인** (`rust-kit/`)으로 생성. backend-kit(스택 무관)과 별개.
- **기본 스택**: Axum 0.8 + Tokio 1.50.0 + SQLx 0.8 + serde + thiserror/anyhow + utoipa + cargo-nextest <!-- Codex 검증: 2026-04-07, crates.io 기준 1.50.0 (2026-03-03 릴리스) -->
- **버전 관리**: `rust-toolchain.toml`에 `channel = "stable"` (롤링 최신)
- **스킬 17종 + 에이전트 1종 + 카이젠/리서치 2종** (카이젠/리서치는 `.claude/skills/`에 배치)
- **아키텍처**: Hexagonal Architecture (Ports & Adapters) 기본. 모든 생성형 스킬이 trait(포트) → impl(어댑터) 순서로 코드를 생성

## 플러그인 구조

```
rust-kit/
├── .claude-plugin/plugin.json
├── skills/
│   ├── rust-init/SKILL.md          # 프로젝트 스캐폴딩
│   ├── rust-feature/SKILL.md       # feature 모듈 스캐폴딩
│   ├── rust-api/SKILL.md           # Axum 라우터/핸들러 + OpenAPI
│   ├── rust-model/SKILL.md         # SQLx 모델 + 마이그레이션
│   ├── rust-service/SKILL.md       # 비즈니스 로직 서비스 레이어
│   ├── rust-auth/SKILL.md          # JWT/OAuth 인증 레이어
│   ├── rust-middleware/SKILL.md    # Axum 미들웨어
│   ├── rust-grpc/SKILL.md          # tonic gRPC 서비스
│   ├── rust-test/SKILL.md          # 테스트 코드 생성
│   ├── rust-docker/SKILL.md        # Dockerfile + docker-compose
│   ├── rust-error/SKILL.md         # 에러 처리 패턴 가이드
│   ├── rust-l10n/SKILL.md          # 백엔드 i18n
│   ├── rust-run/SKILL.md           # 빌드 프리미티브 개별 실행 (기반)
│   ├── rust-build/SKILL.md         # cargo build + clippy (wrapper)
│   ├── rust-preflight/SKILL.md     # pre-commit gate
│   └── rust-audit/SKILL.md         # 코드 품질 감사
├── agents/
│   └── rust-reviewer.md            # audit에서 호출하는 읽기 전용 평가 에이전트
├── references/
│   └── project-detection.md        # Rust 프로젝트 환경 자동 감지
├── evals/
│   └── evals.json                  # 스킬별 assertion
└── README.md

# .claude/skills/ (카이젠/리서치 — 플러그인 외부)
.claude/skills/rust-kaizen/SKILL.md
.claude/skills/rust-research/SKILL.md

# docs/rust/ (리서치 문서 — SSOT)
docs/rust/
├── fundamentals/
│   ├── ownership-borrowing.md
│   ├── error-handling.md
│   ├── async-concurrency.md
│   ├── testing.md
│   ├── project-structure.md
│   ├── performance.md
│   └── hexagonal-architecture.md
├── web/
│   ├── axum-patterns.md
│   ├── middleware.md
│   ├── authentication.md
│   └── openapi.md
├── data/
│   ├── sqlx-patterns.md
│   ├── migrations.md
│   └── caching.md
├── protocols/
│   ├── grpc-tonic.md
│   ├── graphql.md
│   └── realtime.md
└── ops/
    ├── docker.md
    ├── ci-cd.md
    └── observability.md
```

## 프로젝트 감지 (references/project-detection.md)

flutter-toolkit의 7단계 감지 파이프라인을 Rust에 맞게 조정.

### 감지 파이프라인

```
Step 1. Rust 프로젝트 확인      Cargo.toml 존재
Step 2. 툴체인 감지             rust-toolchain.toml → channel/components 파싱
                                없으면 → rustup default 확인
Step 3. Workspace 감지          Cargo.toml [workspace] 존재 여부
                                members 패턴 → 멀티크레이트 구조 파악
Step 4. 의존성 감지             Cargo.toml [dependencies] + [dev-dependencies]
                                주요 크레이트 존재 여부를 HAS_* 플래그로 설정
Step 5. 아키텍처 패턴 감지      src/ 디렉토리 구조 분석 (아래 테이블 참조)
Step 6. 빌드 도구 감지          Makefile, justfile, cargo-make, cross 등
Step 7. CI 감지                 .github/workflows/, .gitlab-ci.yml 등
```

**Step 5 아키텍처 감지 테이블**:

| ARCH | 감지 조건 |
|------|---------|
| `hexagonal` | `ports/` + `adapters/` 디렉토리 존재 (workspace 크레이트 내 또는 단일 크레이트 src/ 내) |
| `workspace_service` | `crates/` 디렉토리 + workspace members 존재 (ports/adapters 없을 때) |
| `modular` | `src/api/`, `src/domain/`, `src/infra/` 모듈 분리 (단일 크레이트, ports/adapters 없을 때) |
| `flat` | `src/main.rs` + `src/lib.rs` 수준 |
| `library` | `[lib]` only, `[[bin]]` 없음 |

### 감지 결과 변수

**커맨드**:
- `$CARGO` — `cargo` (기본) 또는 `cross` (크로스 컴파일 시)
- `$RUSTFMT` — `cargo fmt`
- `$CLIPPY` — `cargo clippy`

**프로젝트 메타**:
- `$PACKAGE` — Cargo.toml의 `[package].name`
- `$EDITION` — 2021 | 2024
- `IS_WORKSPACE` — true | false
- `WORKSPACE_MEMBERS` — 크레이트 목록

**의존성 플래그** (HAS_*):
- `HAS_AXUM`, `HAS_ACTIX`, `HAS_ROCKET` — 웹 프레임워크
- `HAS_SQLX`, `HAS_DIESEL`, `HAS_SEAORM` — ORM/DB
- `HAS_TOKIO`, `HAS_ASYNC_STD` — 런타임
- `HAS_TONIC` — gRPC
- `HAS_SERDE` — 직렬화
- `HAS_UTOIPA` — OpenAPI
- `HAS_JSONWEBTOKEN` — JWT
- `HAS_TRACING` — 로깅/추적
- `HAS_RUST_I18N`, `HAS_FLUENT` — i18n

**아키텍처**:
- `ARCH` = `hexagonal` | `workspace_service` | `modular` | `flat` | `library`
  - `hexagonal`: `ports/` + `adapters/` 디렉토리 존재 (workspace 또는 단일 크레이트 모두 가능)
  - `workspace_service`: `crates/` 디렉토리 + workspace members (API, domain, infra 분리)
  - `modular`: 단일 크레이트 내 `src/api/`, `src/domain/`, `src/infra/` 모듈 분리
  - `flat`: `src/main.rs` + `src/lib.rs` 수준
  - `library`: `[lib]` only, `[[bin]]` 없음

## 스킬 상세 설계

### 분류

| 분류 | 스킬 | 개수 |
|------|------|------|
| 생성형 | rust-init, rust-feature, rust-api, rust-model, rust-service, rust-auth, rust-middleware, rust-grpc, rust-test, rust-docker, rust-l10n | 11 |
| 가이드형 | rust-error | 1 |
| 실행형 | rust-run, rust-build, rust-preflight | 3 |
| 감사형 | rust-audit | 1 |
| 메타 | rust-kaizen | 1 |

### 의존 관계

```
rust-run  <── rust-build (build + clippy wrapper)
rust-run  <── rust-preflight (fmt → clippy → test → audit 오케스트레이션)
rust-feature ──> rust-api, rust-model, rust-service (내부 생성 가능)
rust-audit ──> rust-reviewer (에이전트 위임)
rust-kaizen ──> 전 스킬 (개선 대상)
```

---

### 1. rust-init — 프로젝트 스캐폴딩

**트리거**: "프로젝트 만들어줘", "rust init", "새 프로젝트", "cargo new", "프로젝트 생성"

**생성물**:
- `rust-toolchain.toml` (channel = "stable", components = ["rustfmt", "clippy"])
- `Cargo.toml` (workspace 또는 단일 크레이트)
- 디렉토리 구조 (ARCH에 따라)
- `.cargo/config.toml` (린터 설정)
- `.env.example`
- `sqlx-data.json` (SQLx offline mode용, 선택)

**프로세스**:
1. 프로젝트 이름, 설명 확인
2. 아키텍처 선택 제안 (workspace_service 권장, 규모에 따라 modular/flat)
3. 의존성 선택 (체크리스트: Axum, SQLx, serde, tracing, utoipa 등)
4. 구조 생성
5. `cargo build` 로 초기 컴파일 확인

**workspace_service 구조 예시**:
```
my-project/
├── Cargo.toml              # [workspace]
├── rust-toolchain.toml
├── .cargo/config.toml
├── crates/
│   ├── api/                # Axum 라우터, 핸들러, 미들웨어
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── main.rs
│   │       ├── router.rs
│   │       └── handlers/
│   ├── domain/             # 비즈니스 로직, 도메인 모델
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── models/
│   │       ├── services/
│   │       ├── ports/      # trait 정의
│   │       │   └── mod.rs
│   │       └── errors.rs
│   └── infra/              # DB, 외부 서비스 연동 (어댑터)
│       ├── Cargo.toml
│       └── src/
│           ├── lib.rs
│           ├── adapters/   # trait impl
│           │   └── mod.rs
│           ├── db/
│           ├── cache/
│           └── auth/
├── migrations/             # SQLx 마이그레이션
└── tests/                  # 통합 테스트
```

**modular 구조 예시**:
```
my-project/
├── Cargo.toml
├── rust-toolchain.toml
├── src/
│   ├── main.rs
│   ├── api/
│   │   ├── mod.rs
│   │   ├── router.rs
│   │   └── handlers/
│   ├── domain/
│   │   ├── mod.rs
│   │   ├── models/
│   │   ├── services/
│   │   └── ports/
│   │       └── mod.rs
│   └── infra/
│       ├── mod.rs
│       ├── adapters/
│       │   └── mod.rs
│       └── db/
├── migrations/
└── tests/
```

**Gotchas**:
- `cargo init` vs `cargo new` 혼동 금지 — 기존 디렉토리면 `init`, 새 디렉토리면 `new`
- workspace에서 `resolver = "2"` (edition 2021+) 필수. edition 2024는 `resolver = "3"` 사용
- `.cargo/config.toml`에 `[target.x86_64-unknown-linux-gnu]` 같은 타겟 고정 금지 — 크로스 플랫폼 깨짐

---

### 2. rust-feature — feature 모듈 스캐폴딩

**트리거**: "모듈 추가", "feature 생성", "새 기능 모듈", "rust feature"

**생성물** (ARCH에 따라):
- workspace_service: 해당 크레이트 내 모듈 디렉토리 + mod.rs + handler + service + model + test
- modular: `src/{layer}/{feature}/` 디렉토리 구조

**프로세스**:
1. 프로젝트 감지
2. feature 이름, 소속 레이어 확인
3. 기존 feature 패턴 읽기 (이미 있는 feature의 구조를 따름)
4. 파일 생성 + mod.rs 등록
5. 라우터에 `.nest()` 또는 `.merge()` 추가 안내

**Gotchas**:
- `mod.rs` vs 파일 이름 모듈(`feature.rs`) — 프로젝트 기존 패턴을 따름. 혼용 금지
- workspace 멤버 간 순환 의존 금지 — `domain`은 `api`나 `infra`를 의존하면 안 됨
- `pub` 범위 최소화 — `pub(crate)` 기본, `pub`은 크레이트 경계에서만

---

### 3. rust-api — Axum 라우터/핸들러 생성

**트리거**: "API 추가", "엔드포인트 추가", "핸들러 만들어줘", "라우터 추가", "rust api"

**생성물**:
- 핸들러 함수 (`async fn`)
- 라우터 모듈 (`.route()` 등록)
- Request/Response 구조체 (serde Serialize/Deserialize)
- utoipa `#[utoipa::path]` 어노테이션 (HAS_UTOIPA 시)

**프로세스**:
1. 프로젝트 감지
2. HTTP 메서드, 경로, 요청/응답 스키마 확인
3. 기존 핸들러 패턴 읽기 (에러 반환 방식, 추출자 사용 패턴)
4. 포트 정의 — `domain/ports/`에 핸들러가 의존할 서비스 trait을 정의한다. 구현 상세(SQLx, 외부 API 등)를 trait에 노출하지 않는다.
5. 어댑터 구현 — `infra/adapters/`에 trait impl을 생성한다. 구체 크레이트 의존은 이 레이어에만 존재한다.
6. 핸들러 + 라우터 생성 (핸들러는 trait을 의존성으로 주입받는 패턴)
7. OpenAPI 스펙 등록 (HAS_UTOIPA)
8. `cargo build` 확인 안내

**핸들러 패턴**:
```rust
// Axum extractor 기반
async fn create_user(
    State(pool): State<PgPool>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<Json<UserResponse>, AppError> {
    // ...
}
```

**Gotchas**:
- Axum 0.7+ 에서 `State`는 `Router::with_state()`로 주입. 글로벌 상태 사용 금지
- `Json<T>` 추출자는 요청 본문을 소비함 — 한 핸들러에서 두 번 추출 불가
- 경로 파라미터 `Path<(String, i64)>` 순서가 URL 세그먼트 순서와 일치해야 함

---

### 4. rust-model — SQLx 모델 + 마이그레이션

**트리거**: "모델 만들어줘", "테이블 추가", "마이그레이션 생성", "DB 모델", "rust model"

**생성물**:
- 구조체 + `sqlx::FromRow` derive
- 마이그레이션 SQL 파일 (`migrations/YYYYMMDDHHMMSS_<name>.sql`)
- CRUD 쿼리 함수 (compile-time checked `sqlx::query_as!`)

**프로세스**:
1. 프로젝트 감지
2. 테이블 이름, 컬럼, 관계 확인
3. 기존 모델 패턴 읽기
4. 포트 정의 — `domain/ports/`에 Repository trait을 정의한다. SQLx 타입(PgPool 등)을 trait 시그니처에 노출하지 않는다.
5. 어댑터 구현 — `infra/adapters/`에 SQLx 기반 Repository impl을 생성한다. sqlx 의존은 이 레이어에만 존재한다.
6. 마이그레이션 SQL 생성
7. Rust 구조체 + 쿼리 함수 생성
8. `sqlx migrate run` 또는 `cargo sqlx prepare` 안내

**Gotchas**:
- `sqlx::query!` 매크로는 컴파일 타임에 DB 연결 필요 — `DATABASE_URL` 환경변수 또는 `.env` 필수
- 오프라인 모드(`sqlx-data.json`)는 `cargo sqlx prepare`로 미리 생성해야 CI에서 동작
- 마이그레이션 파일 이름의 타임스탬프가 겹치면 에러 — 항상 현재 시각 사용
- nullable 컬럼은 `Option<T>`로 매핑. `NOT NULL`인데 `Option`으로 하면 런타임 패닉

---

### 5. rust-service — 비즈니스 로직 서비스 레이어

**트리거**: "서비스 만들어줘", "비즈니스 로직", "유즈케이스", "rust service"

**생성물**:
- 서비스 trait + impl
- DI를 위한 trait 기반 추상화
- 단위 테스트 스켈레톤

**프로세스**:
1. 프로젝트 감지
2. 서비스 이름, 의존성(repository trait 등) 확인
3. 기존 서비스 패턴 읽기
4. 포트 정의 — `domain/ports/`에 서비스가 의존할 port trait을 정의한다. 서비스 자체도 port trait으로 노출한다.
5. 어댑터 구현 — `infra/adapters/`에 port trait impl을 생성한다. 구체 크레이트 의존은 이 레이어에만 존재한다.
6. 서비스 trait + impl 생성
7. 테스트 모듈 생성 (mock 포함)

**패턴**:
```rust
// 포트 기반 DI (Hexagonal)
#[async_trait]
pub trait UserService: Send + Sync {
    async fn create_user(&self, req: CreateUserRequest) -> Result<User, DomainError>;
}

pub struct UserServiceImpl<R: UserRepository> {
    repo: R,
}
```

**Gotchas**:
- `async_trait`은 heap allocation 발생 — 성능 크리티컬 경로에서는 RPITIT (Rust 1.75+) 사용 고려
- 서비스가 여러 repository에 의존하면 제네릭이 복잡해짐 — 구체 타입으로 시작하고 필요 시 trait 추출

---

### 6. rust-auth — JWT/OAuth 인증 레이어

**트리거**: "인증 추가", "JWT", "로그인", "OAuth", "auth", "rust auth"

**생성물**:
- JWT 토큰 생성/검증 함수
- Axum 인증 미들웨어 (extractor 기반)
- Claims 구조체
- 선택: OAuth/OIDC 클라이언트 설정

**프로세스**:
1. 프로젝트 감지
2. 인증 방식 확인 (JWT only / JWT + refresh / OAuth + JWT)
3. 기존 auth 패턴 읽기
4. 포트 정의 — `domain/ports/`에 `AuthProvider` trait을 정의한다. JWT 라이브러리 타입을 trait에 노출하지 않는다.
5. 어댑터 구현 — `infra/adapters/`에 jsonwebtoken 기반 `AuthProvider` impl을 생성한다. jsonwebtoken 의존은 이 레이어에만 존재한다.
6. 토큰 유틸 + 미들웨어 + Claims 생성
7. 환경변수 (.env) 에 시크릿 키 설정 안내

**패턴**:
```rust
// Axum extractor로 인증
pub struct AuthUser(pub Claims);

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = AppError;
    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        // Authorization 헤더에서 Bearer 토큰 추출 + 검증
    }
}
```

**Gotchas**:
- JWT 시크릿을 소스코드에 하드코딩 금지 — 반드시 환경변수에서 로드
- `jsonwebtoken::decode`는 exp 클레임 자동 검증 — 추가 만료 검사 중복 금지
- refresh token은 DB에 저장해야 함 — 메모리/JWT 안에 넣으면 무효화 불가

---

### 7. rust-middleware — Axum 미들웨어

**트리거**: "미들웨어 추가", "CORS", "rate limit", "로깅 미들웨어", "rust middleware"

**생성물**:
- tower 미들웨어 레이어 또는 Axum `middleware::from_fn`
- 구성: CORS, request logging, rate limiting, request ID, timeout 중 선택

**프로세스**:
1. 프로젝트 감지
2. 미들웨어 종류 확인
3. 기존 미들웨어 스택 읽기
4. 포트 정의 — 미들웨어가 외부 상태(rate limiter, 캐시 등)에 의존할 경우 `domain/ports/`에 trait을 정의한다.
5. 어댑터 구현 — 구체 구현(Redis, in-memory 등)을 `infra/adapters/`에 생성한다.
6. 미들웨어 생성 + 라우터에 `.layer()` 등록
7. `cargo build` 확인

**Gotchas**:
- tower 레이어 순서가 중요 — `.layer()`는 안쪽부터 바깥으로 적용됨 (마지막 `.layer()`가 가장 먼저 실행)
- `CorsLayer`는 `tower-http` 크레이트 — `axum` 자체에 없음
- rate limiting 상태는 `Arc<Mutex<>>` 또는 외부 저장소(Redis) — 멀티 인스턴스 환경 고려

---

### 8. rust-grpc — tonic gRPC 서비스

**트리거**: "gRPC 추가", "proto 파일", "tonic", "rust grpc"

**생성물**:
- `.proto` 파일
- `build.rs` (tonic-build 코드 생성 설정)
- gRPC 서비스 impl
- 클라이언트 코드 (선택)

**프로세스**:
1. 프로젝트 감지
2. 서비스 이름, RPC 메서드 확인
3. proto 파일 생성
4. build.rs 설정
5. 포트 정의 — `domain/ports/`에 gRPC 서비스가 의존할 비즈니스 로직 trait을 정의한다. tonic 생성 타입을 domain에 노출하지 않는다.
6. 어댑터 구현 — `infra/adapters/`에 tonic 서비스 trait impl을 생성한다. tonic 의존은 이 레이어에만 존재한다.
7. 서비스 구현 스켈레톤 생성
8. `cargo build` 로 코드 생성 확인

**Gotchas**:
- `protoc` 시스템 설치 필요 — tonic-build가 자체 포함하지 않음. `prost-build`의 `protoc` 자동 다운로드 옵션 안내
- proto 파일 경로는 `build.rs`의 `compile_protos` 인자와 정확히 일치해야 함
- streaming RPC는 `impl Stream` 반환 — `tokio_stream::wrappers` 활용

---

### 9. rust-test — 테스트 코드 생성

**트리거**: "테스트 만들어줘", "unit test", "integration test", "테스트 추가", "rust test"

**생성물**:
- 단위 테스트 (`#[cfg(test)] mod tests`)
- 통합 테스트 (`tests/` 디렉토리)
- mock (mockall 기반, trait에 `#[automock]`)

**프로세스**:
1. 프로젝트 감지
2. 대상 파일/모듈 분석 — 공개 함수, trait 목록 추출
3. 기존 테스트 패턴 읽기
4. 테스트 타입 결정:
   - 순수 함수 → 단위 테스트
   - trait impl → mock 기반 단위 테스트
   - 핸들러 → 통합 테스트 (실제 서버 또는 `TestClient`)
   - DB 의존 → 통합 테스트 (테스트 DB + 마이그레이션)
5. 테스트 코드 생성
6. `cargo nextest run` 실행 안내

**Gotchas**:
- `#[sqlx::test]`는 테스트별 독립 DB 트랜잭션 제공 — 직접 connection pool 만들지 말 것
- `tokio::test`에 `#[tokio::test(flavor = "multi_thread")]` 필요한 케이스 있음 — spawn 사용 시
- mockall의 `#[automock]`은 trait에만 적용 가능 — 구체 struct 메서드에는 사용 불가

---

### 10. rust-docker — Dockerfile + docker-compose

**트리거**: "도커", "Dockerfile", "컨테이너", "배포 설정", "rust docker"

**생성물**:
- 멀티스테이지 Dockerfile (builder + runtime)
- docker-compose.yml (앱 + PostgreSQL + Redis 등)
- .dockerignore

**프로세스**:
1. 프로젝트 감지
2. 의존 서비스 확인 (DB, 캐시, 메시지 큐)
3. Dockerfile 생성 (cargo-chef 기반 캐싱 최적화)
4. docker-compose 생성
5. `.dockerignore` 생성

**Dockerfile 패턴** (cargo-chef):
```dockerfile
FROM rust:1-bookworm AS chef
RUN cargo install cargo-chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim AS runtime
COPY --from=builder /app/target/release/app /usr/local/bin/
CMD ["app"]
```

**Gotchas**:
- Rust 바이너리는 정적 링크가 아닐 수 있음 — `musl` 타겟 또는 동일 distro 베이스 사용
- `cargo-chef`로 의존성 캐싱 — `cargo build`만 하면 소스 변경마다 전체 재빌드
- `.sqlx/` 디렉토리를 이미지에 포함해야 오프라인 모드 동작 — `.dockerignore`에서 제외하지 말 것

---

### 11. rust-error — 에러 처리 패턴 가이드

**트리거**: "에러 처리", "error handling", "에러 타입", "Result", "rust error"

**가이드 내용**:
- 3계층 에러 구조: `InfraError` → `DomainError` → `ApiError`
- infra 계층: `thiserror`로 구체적 에러 정의 (DB, 외부 API 등)
- domain 계층: `thiserror`로 비즈니스 에러 정의, infra 에러를 `From` impl로 변환
- api 계층: `IntoResponse` impl로 HTTP 상태 코드 매핑
- 앱 경계(main, 스크립트): `anyhow::Result`로 간단히 처리

**패턴**:
```rust
// domain/errors.rs
#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("user not found: {0}")]
    UserNotFound(String),
    #[error("duplicate email")]
    DuplicateEmail,
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}

// api/errors.rs
impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, message) = match self.0 {
            DomainError::UserNotFound(_) => (StatusCode::NOT_FOUND, self.0.to_string()),
            DomainError::DuplicateEmail => (StatusCode::CONFLICT, self.0.to_string()),
            DomainError::Internal(_) => (StatusCode::INTERNAL_SERVER_ERROR, "internal error".into()),
        };
        // ...
    }
}
```

**Gotchas**:
- `anyhow`와 `thiserror` 혼용 금지하지 않음 — 라이브러리 코드는 `thiserror`, 앱 코드는 `anyhow`가 관용적
- `.unwrap()`, `.expect()` 는 프로덕션 코드에서 금지 — 테스트에서만 허용
- `?` 연산자 체이닝 시 `From` impl 누락이 흔한 컴파일 에러 원인

---

### 12. rust-l10n — 백엔드 i18n

**트리거**: "다국어", "번역", "i18n", "l10n", "국제화", "rust l10n"

**생성물**:
- i18n 설정 (rust-i18n 또는 fluent 기반)
- 로케일 파일 (`locales/ko.toml`, `locales/en.toml` 등)
- Accept-Language 미들웨어
- 번역 키 추가/수정

**프로세스**:
1. 프로젝트 감지 (`HAS_RUST_I18N` / `HAS_FLUENT`)
2. i18n 라이브러리 미설치 시 선택 제안 (rust-i18n 권장 — 간단한 TOML 기반)
3. 기존 로케일 파일 패턴 읽기
4. 새 번역 키 추가 또는 기존 키 수정
5. 미들웨어 설정 확인 (Accept-Language → locale 추출)

**rust-i18n 패턴**:
```toml
# locales/en.toml
[messages]
user_not_found = "User not found: %{id}"
email_sent = "Verification email sent to %{email}"

# locales/ko.toml
[messages]
user_not_found = "사용자를 찾을 수 없습니다: %{id}"
email_sent = "인증 이메일이 %{email}로 발송되었습니다"
```

```rust
use rust_i18n::t;
// 사용
let msg = t!("messages.user_not_found", id = user_id, locale = &locale);
```

**Gotchas**:
- 번역 키에 변수 플레이스홀더(`%{name}`)가 모든 로케일에 일관되어야 함
- `rust-i18n`은 컴파일 타임 키 검증 없음 — 오타 시 런타임에 키 이름 그대로 반환
- Accept-Language 파싱은 `accept-language` 크레이트 사용 — 직접 파싱 금지 (quality factor 처리 복잡)

---

### 13. rust-run — 빌드 프리미티브 개별 실행 (기반 스킬)

**트리거**: "빌드해줘", "clippy", "포맷팅", "테스트 실행", "cargo build", "rust run"

**argument-hint**: `<build|clippy|fmt|test|audit|check> [args]`

**서브커맨드**:
| 커맨드 | 실행 | 성공 조건 |
|--------|------|----------|
| `build` | `$CARGO build` | exit 0 |
| `clippy` | `$CARGO clippy -- -D warnings` | 워닝 0 |
| `fmt` | `$CARGO fmt` (적용) / `$CARGO fmt -- --check` (검사) | exit 0 |
| `test` | `cargo nextest run` (있으면) / `$CARGO test` | 전 테스트 통과 |
| `audit` | `cargo audit` (있으면) + `cargo deny check` (있으면) | 취약점 0 |
| `check` | `$CARGO check` | exit 0 (build보다 빠름) |

**Gotchas**:
- `cargo clippy`에 `-- -D warnings` 없으면 워닝이 에러로 안 잡힘
- workspace에서 `--workspace` 플래그 필수 — 없으면 루트 크레이트만 실행
- `cargo nextest`가 설치 안 되어 있으면 `cargo test`로 폴백

---

### 14. rust-build — cargo build + clippy (wrapper)

**트리거**: "빌드", "build", "컴파일", "rust build"

**프로세스**:
1. 프로젝트 감지
2. `rust-run build` 실행
3. `rust-run clippy` 실행
4. 결과 리포트

rust-run의 thin wrapper. flutter-build가 flutter-run의 wrapper인 것과 동일 패턴.

---

### 15. rust-preflight — pre-commit gate

**트리거**: "preflight", "커밋 전 검사", "pre-commit", "품질 게이트", "rust preflight"

**실행 순서**:
```
1. rust-run fmt --check    → 실패 시 자동 적용 후 재검사
2. rust-run clippy         → 실패 시 중단
3. rust-run test           → 실패 시 중단
4. rust-run audit          → 실패 시 경고 (중단 안 함, 보안 취약점만 보고)
```

**리포트 형식**:
```
## Preflight Report

| Step      | Status | Details          |
|-----------|--------|------------------|
| fmt       | PASS   |                  |
| clippy    | PASS   |                  |
| test      | PASS   | 42 tests passed  |
| audit     | WARN   | 1 advisory found |

Result: PASS (with warnings)
```

**Gotchas**:
- `cargo fmt`는 자동 수정이므로 unstaged changes를 만듦 — git add 필요 안내
- clippy 통과 후 test 실패 가능 — 순서 바꾸지 말 것
- audit은 non-blocking — 외부 크레이트 취약점은 즉시 수정 불가할 수 있음

---

### 16. rust-audit — 코드 품질 감사

**트리거**: "리뷰", "감사", "코드 검토", "품질 검사", "rust audit"

**argument-hint**: `[quick|deep]`

**모드**:
- `quick`: 단일 에이전트, 변경 파일만 검사
- `deep`: rust-reviewer 에이전트 위임, 전체 프로젝트 구조 + 코드 품질 감사

**감사 카테고리**:
1. Ownership & Borrowing — 불필요한 clone, lifetime 이슈
2. Error Handling — unwrap 남용, 에러 타입 일관성
3. Async — blocking in async, 불필요한 .await
4. Security — SQL injection, 시크릿 하드코딩
5. Performance — 불필요한 allocation, 비효율적 이터레이터
6. Testing — 커버리지, 엣지 케이스
7. API Design — 일관성, RESTful 규칙, OpenAPI 정합

**리포트**: 카테고리별 PASS/FAIL + 근거 + 개선 제안

---

### 17. rust-kaizen (.claude/skills/) — 메타 스킬

flutter-kaizen과 동일 패턴. docs/rust/ 리서치 문서 기준으로 스킬 품질을 주기적으로 개선.

---

## 에이전트: rust-reviewer

```yaml
tools: Read, Grep, Glob    # 읽기 전용
model: sonnet
```

backend-reviewer와 동일 패턴:
- rust-audit에서만 호출 (단독 실행 금지)
- PASS/FAIL 이진 판정
- 칭찬 금지
- 감사 기준은 `rust-kit/skills/rust-audit/references/audit-criteria.md`가 유일한 진실원천

## 리서치 문서 구조 (docs/rust/)

총 20개 문서, 5개 카테고리:

| 카테고리 | 문서 | 대응 스킬 |
|----------|------|----------|
| fundamentals/ | ownership-borrowing.md | rust-audit |
| fundamentals/ | error-handling.md | rust-error |
| fundamentals/ | async-concurrency.md | rust-service, rust-middleware |
| fundamentals/ | testing.md | rust-test |
| fundamentals/ | project-structure.md | rust-init, rust-feature |
| fundamentals/ | performance.md | rust-audit |
| fundamentals/ | hexagonal-architecture.md | rust-init, rust-feature, rust-api, rust-model, rust-service, rust-auth |
| web/ | axum-patterns.md | rust-api |
| web/ | middleware.md | rust-middleware |
| web/ | authentication.md | rust-auth |
| web/ | openapi.md | rust-api |
| data/ | sqlx-patterns.md | rust-model |
| data/ | migrations.md | rust-model |
| data/ | caching.md | rust-middleware |
| protocols/ | grpc-tonic.md | rust-grpc |
| protocols/ | graphql.md | (확장용) |
| protocols/ | realtime.md | (확장용) |
| ops/ | docker.md | rust-docker |
| ops/ | ci-cd.md | (확장용) |
| ops/ | observability.md | (확장용) |

## evals 설계 (evals/evals.json)

스킬별 최소 1개 assertion, 총 17+ 테스트 케이스:

```json
[
  {
    "skill": "rust-init",
    "trigger": "Rust 프로젝트 새로 만들어줘",
    "assertions": [
      "rust-toolchain.toml 생성됨",
      "Cargo.toml에 [workspace] 또는 [package] 존재",
      "cargo build 성공"
    ]
  },
  {
    "skill": "rust-run",
    "trigger": "clippy 돌려줘",
    "assertions": [
      "cargo clippy -- -D warnings 실행됨",
      "결과 출력됨"
    ]
  }
]
```

## QA 자체 검증

### Placeholder 스캔
- TBD/TODO 없음 확인 완료

### 내부 일관성
- 17종 스킬 분류(생성 11 + 가이드 1 + 실행 3 + 감사 1 + 메타 1) = 17 확인
- 의존 관계에 순환 없음 확인
- 리서치 문서 20개, docs-site HTML도 20페이지 (1:1 대응)

### 범위
- 단일 구현 계획으로 처리 가능 — Phase별 분할 필요 (리서치 문서 → 플러그인 스캐폴딩 → 스킬 작성 → 에이전트 → 카이젠 → 레지스트리 → evals → docs-site)

### 모호성
- Axum 기본 확정, SQLx 기본 확정 — 대안 프레임워크 지원은 v2 스코프
- rust-l10n은 rust-i18n 기본 — fluent는 감지 시 대응

### flutter-toolkit 대비 갭 최종 확인
- flutter-extract (위젯 추출) → Rust에는 해당 없음 (모듈 시스템이 대체) ✓
- flutter-screen (화면 생성) → rust-api (핸들러 생성)가 대응 ✓
- flutter-widget (위젯 생성) → rust-middleware (미들웨어 생성)가 부분 대응 ✓
- flutter-hooks (패턴 가이드) → rust-error (패턴 가이드)가 대응 ✓
- flutter-skeleton, flutter-responsive, flutter-transition → 프론트엔드 전용, 해당 없음 ✓
