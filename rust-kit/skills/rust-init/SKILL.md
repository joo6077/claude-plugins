---
name: rust-init
description: >
  Rust 백엔드 프로젝트를 스캐폴딩한다. Cargo workspace 구조, rust-toolchain.toml,
  디렉토리 레이아웃, 의존성 설정을 생성한다.
  "프로젝트 만들어줘", "rust init", "새 프로젝트", "cargo new",
  "프로젝트 생성", "프로젝트 셋업" 같은 요청 시 트리거.
  기존 프로젝트에 모듈을 추가할 때는 트리거하지 않는다 — rust-feature 사용.
argument-hint: "[project-name]"
user-invocable: true
---

# Gotchas

1. **`cargo init` vs `cargo new` 혼동 금지** — 기존 디렉토리에 초기화하면 `cargo init`, 새 디렉토리를 만들면 `cargo new`.
2. **workspace resolver 누락 금지** — edition 2021+는 `resolver = "2"`, edition 2024는 `resolver = "3"` 필수.
3. **타겟 아키텍처 고정 금지** — `.cargo/config.toml`에 `[target.x86_64-unknown-linux-gnu]` 같은 타겟을 고정하면 크로스 플랫폼이 깨진다.
4. **과도한 의존성 금지** — 사용자가 선택한 의존성만 추가한다. "나중에 필요할 수도 있으니" 추가하지 않는다.

# Process

## 1. 프로젝트 이름/설명 확인

사용자에게 프로젝트 이름을 확인한다. 미지정 시 현재 디렉토리 이름 사용.

## 2. 아키텍처 선택

사용자에게 아키텍처를 제안한다:

| 아키텍처 | 적합 규모 | 특징 |
|----------|----------|------|
| `workspace_service` (권장) | 중~대규모 | crates/api + domain + infra 분리. ports/adapters hexagonal 기본 포함 |
| `modular` | 소~중규모 | 단일 크레이트 내 모듈 분리. ports/adapters hexagonal 기본 포함 |
| `flat` | 프로토타입/소규모 | src/main.rs + lib.rs |

## 3. 의존성 선택

체크리스트로 제시:
- [x] axum (기본)
- [x] tokio (기본)
- [x] serde + serde_json (기본)
- [x] tracing + tracing-subscriber (기본)
- [ ] sqlx (PostgreSQL)
- [ ] utoipa + utoipa-swagger-ui (OpenAPI)
- [ ] jsonwebtoken (JWT 인증)
- [ ] tower-http (CORS, 로깅 등)
- [ ] rust-i18n (다국어)

## 4. 구조 생성

선택한 아키텍처에 따라 파일/디렉토리를 생성한다.

### workspace_service 구조

```
{project}/
├── Cargo.toml              # [workspace] members = ["crates/*"], resolver = "2"
├── rust-toolchain.toml     # channel = "stable", components = ["rustfmt", "clippy"]
├── .cargo/config.toml
├── .env.example
├── crates/
│   ├── api/
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── main.rs
│   │       ├── router.rs
│   │       └── handlers/
│   │           └── mod.rs
│   ├── domain/
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── models/
│   │       │   └── mod.rs
│   │       ├── services/
│   │       │   └── mod.rs
│   │       ├── ports/      # 서비스 trait 정의 (hexagonal)
│   │       │   └── mod.rs
│   │       └── errors.rs
│   └── infra/
│       ├── Cargo.toml
│       └── src/
│           ├── lib.rs
│           ├── adapters/   # trait impl (hexagonal)
│           │   └── mod.rs
│           └── db/
│               └── mod.rs
├── migrations/
└── tests/
```

### modular 구조

```
{project}/
├── Cargo.toml
├── rust-toolchain.toml
├── .cargo/config.toml
├── .env.example
├── src/
│   ├── main.rs
│   ├── api/
│   │   ├── mod.rs
│   │   ├── router.rs
│   │   └── handlers/
│   │       └── mod.rs
│   ├── domain/
│   │   ├── mod.rs
│   │   ├── models/
│   │   │   └── mod.rs
│   │   ├── services/
│   │   │   └── mod.rs
│   │   └── ports/          # 서비스 trait 정의 (hexagonal)
│   │       └── mod.rs
│   └── infra/
│       ├── mod.rs
│       ├── adapters/       # trait impl (hexagonal)
│       │   └── mod.rs
│       └── db/
│           └── mod.rs
├── migrations/
└── tests/
```

### flat 구조

```
{project}/
├── Cargo.toml
├── rust-toolchain.toml
├── src/
│   ├── main.rs
│   └── lib.rs
└── tests/
```

## 5. 초기 컴파일 확인

`cargo build`를 실행하여 프로젝트가 정상 컴파일되는지 확인한다.

## After Creation

1. 생성된 파일/디렉토리 목록 출력.
2. 다음 단계 안내:
   > - API 엔드포인트 추가: `/rust-api`
   > - DB 모델 추가: `/rust-model`
   > - 인증 설정: `/rust-auth`

# References

- references/project-detection.md
- docs/rust/fundamentals/project-structure.md
