# rust-kit

Rust 전용 백엔드 개발 워크플로우 플러그인.

## 개요

Axum + Tokio + SQLx 기반 Rust 백엔드 프로젝트의 스캐폴딩, API 생성, 모델 관리, 빌드/테스트/감사를 자동화한다. flutter-toolkit과 동일한 개발 워크플로우 패턴.

<!-- AUTO:skills -->
## 스킬

| 스킬 | 용도 |
|------|------|
| `/rust-init` | 프로젝트 스캐폴딩 (workspace + toolchain + 구조) |
| `/rust-feature` | feature 모듈 스캐폴딩 |
| `/rust-api` | Axum 라우터/핸들러 + utoipa OpenAPI |
| `/rust-model` | SQLx 모델 + 마이그레이션 |
| `/rust-service` | 비즈니스 로직 서비스 레이어 |
| `/rust-auth` | JWT/OAuth 인증 레이어 |
| `/rust-middleware` | Axum 미들웨어 (CORS, logging, rate-limit) |
| `/rust-grpc` | tonic gRPC 서비스 |
| `/rust-test` | 테스트 코드 생성 (unit + integration) |
| `/rust-docker` | Dockerfile + docker-compose |
| `/rust-error` | 에러 처리 패턴 가이드 (thiserror/anyhow) |
| `/rust-l10n` | 백엔드 i18n (rust-i18n/fluent) |
| `/rust-run` | 빌드 프리미티브 개별 실행 (build, clippy, fmt, test, audit, check) |
| `/rust-build` | cargo build + clippy (rust-run wrapper) |
| `/rust-preflight` | pre-commit gate (fmt → clippy → test → audit) |
| `/rust-audit` | 코드 품질 감사 (quick/deep 모드) |
<!-- AUTO:skills -->

<!-- AUTO:agents -->
## 에이전트

| 에이전트 | 용도 |
|---------|------|
| `rust-reviewer` | rust-audit에서 호출. 읽기 전용 독립 평가 |
<!-- AUTO:agents -->

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
