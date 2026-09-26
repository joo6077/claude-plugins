# rust-kit

Rust 전용 백엔드 개발 워크플로우 플러그인.

## 개요

Axum + Tokio + SQLx 기반 Rust 백엔드 프로젝트의 스캐폴딩, API 생성, 모델 관리, 빌드/테스트/감사를 자동화한다. flutter-toolkit과 동일한 개발 워크플로우 패턴.

## 스킬

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `rust-api` | Axum 라우터/핸들러를 생성하고 OpenAPI 스펙을 등록한다. |
| `rust-audit` | Rust 코드를 원칙 기준으로 체계적으로 감사한다. |
| `rust-auth` | JWT/OAuth 인증 레이어를 생성한다. AuthProvider trait(포트) 정의 → |
| `rust-build` | cargo build + clippy를 순서대로 실행한다. |
| `rust-docker` | Rust 프로젝트용 Dockerfile과 docker-compose.yml을 생성한다. |
| `rust-error` | Rust 프로젝트의 에러 처리 패턴을 안내한다. 3계층 에러 구조(InfraError → DomainError → ApiError)를 기반으로 |
| `rust-feature` | feature 모듈을 프로젝트 아키텍처에 맞는 구조로 스캐폴딩한다. |
| `rust-grpc` | tonic gRPC 서비스를 생성한다. proto 파일 → build.rs → gRPC 서비스 trait(포트) 정의 → |
| `rust-init` | Rust 백엔드 프로젝트를 스캐폴딩한다. Cargo workspace 구조, rust-toolchain.toml, |
| `rust-l10n` | Rust 백엔드 프로젝트에 i18n을 설정하거나 번역 키를 추가/수정한다. |
| `rust-middleware` | Axum 미들웨어를 생성하고 라우터에 등록한다. CORS, request logging, rate limiting, |
| `rust-model` | SQLx 모델 구조체와 마이그레이션 SQL을 생성한다. |
| `rust-preflight` | Pre-commit quality gate. fmt → clippy → test → audit 순서로 실행하고 |
| `rust-run` | Rust 빌드 프리미티브 실행 (build, clippy, fmt, test, audit, check). |
| `rust-service` | 비즈니스 로직 서비스 레이어를 생성한다. |
| `rust-test` | 대상 파일/모듈을 분석하여 Rust 테스트 코드를 자동 생성한다. |
<!-- /AUTO:skills -->

## 에이전트

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| `rust-reviewer` | Rust 코드를 원칙 기준으로 독립 평가한다. |
<!-- /AUTO:agents -->

## 리서치 문서

`docs/rust/` 디렉토리에 20개 원칙 문서가 있으며, 모든 스킬이 이를 SSOT로 참조한다.

### fundamentals
- **소유권과 빌림** — ownership, borrowing, lifetime, clone 회피
- **에러 처리** — thiserror, anyhow, Result 패턴, 에러 계층화
- **비동기/동시성** — Tokio, async/await, spawn, 동시성 프리미티브
- **테스팅** — cargo-nextest, mockall, sqlx::test, 통합 테스트
- **프로젝트 구조** — workspace, 모듈 레이아웃, 크레이트 분리
- **성능** — allocation, iterator, 벤치마크, 프로파일링
- **헥사고날 아키텍처** — Ports & Adapters, trait 기반 포트, 어댑터 교체 패턴

### web
- **Axum 패턴** — Router, State, Extractor, IntoResponse
- **미들웨어** — tower 레이어, tower-http, 미들웨어 순서
- **인증** — JWT, OAuth, Bearer 토큰, Claims
- **OpenAPI** — utoipa, Swagger UI, 스키마 자동 생성

### data
- **SQLx 패턴** — query_as!, FromRow, 타입 매핑, 트랜잭션
- **마이그레이션** — sqlx migrate, 오프라인 모드
- **캐싱** — Redis, in-memory 캐시, 캐시 전략

### protocols
- **gRPC** — tonic, proto 정의, streaming
- **GraphQL** — async-graphql, schema, dataloader
- **실시간** — WebSocket, SSE

### ops
- **Docker** — cargo-chef, 멀티스테이지 빌드, compose
- **CI/CD** — GitHub Actions, 캐시 전략, 배포 파이프라인
- **관측성** — tracing, metrics, structured logging

## 카이젠

- `/rust-research` — 외부 소스 크롤링으로 docs/rust/ 문서 갱신
- `/rust-kaizen` — 리서치 문서 기준으로 스킬 품질 점진 개선

### Phase 9 kaizen (2026-05-07)

- Phase 1 v1.3.0 신규 원칙 흡수 — `/insights` Friction #1·#2·#3 의 rust-kit 측 reframe
- 적용 매핑은 **harness/references/cross-kit-principles.md** rust-kit 열 참조
- rust-audit ANALYZE ↔ Pre-Edit Batch Audit, rust-reviewer self-check ↔ Self-Evaluator Audit, PostToolUse cargo fmt/clippy ↔ Hook-Triggered Auto-Correction
