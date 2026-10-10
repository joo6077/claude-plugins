# rust-kit

Rust 전용 백엔드 개발 워크플로우 플러그인.

## 개요

Axum + Tokio + SQLx 기반 Rust 백엔드 프로젝트의 스캐폴딩, API 생성, 모델 관리, 빌드/테스트/감사를 자동화한다. flutter-toolkit과 동일한 개발 워크플로우 패턴.

## 스킬

<!-- AUTO:skills -->
| 스킬 | 설명 |
| --- | --- |
| `rust-api` | Axum 라우터/핸들러를 생성하고 OpenAPI 스펙을 등록한다. |
| `rust-audit` | Rust 코드를 원칙 기준으로 체계적으로 감사한다. |
| `rust-auth` | JWT/OAuth 인증 레이어를 생성한다. |
| `rust-build` | cargo build + clippy를 순서대로 실행한다. |
| `rust-docker` | Rust 프로젝트용 Dockerfile과 docker-compose.yml을 생성한다. |
| `rust-error` | Rust 프로젝트의 에러 처리 패턴을 안내한다. |
| `rust-feature` | feature 모듈을 프로젝트 아키텍처에 맞는 구조로 스캐폴딩한다. |
| `rust-grpc` | tonic gRPC 서비스를 생성한다. |
| `rust-init` | Rust 백엔드 프로젝트를 스캐폴딩한다. |
| `rust-l10n` | Rust 백엔드 프로젝트에 i18n을 설정하거나 번역 키를 추가/수정한다. |
| `rust-middleware` | Axum 미들웨어를 생성하고 라우터에 등록한다. |
| `rust-model` | SQLx 모델 구조체와 마이그레이션 SQL을 생성한다. |
| `rust-preflight` | Pre-commit quality gate. |
| `rust-run` | Rust 빌드 프리미티브 실행 (build, clippy, fmt, test, audit, check). |
| `rust-service` | 비즈니스 로직 서비스 레이어를 생성한다. |
| `rust-test` | 대상 파일/모듈을 분석하여 Rust 테스트 코드를 자동 생성한다. |
<!-- /AUTO:skills -->

## 에이전트

<!-- AUTO:agents -->
| 에이전트 | 설명 |
| --- | --- |
| `rust-reviewer` | Rust 코드를 원칙 기준으로 독립 평가한다. |
<!-- /AUTO:agents -->

## 훅

`lint-edited-rust` (`scripts/lint-edited-rust.sh`) — 두 훅이 한 스크립트를 쓴다. `PostToolUse`(Edit · Write · MultiEdit) 는 고친 `.rs` 파일 경로를 세션별 기록에 적기만 하고, `Stop` 은 답을 끝내기 직전에 워크스페이스마다 `cargo clippy` 를 한 번 돌려 기록한 파일의 줄만 고른다.

- 경고·오류가 있으면 종료 코드 2 로 끝내 Claude 가 그 줄을 받아 고치게 한다. clippy 는 경고만 있으면 0 으로 끝나므로 종료 코드가 아니라 출력 줄로 판정한다
- 편집마다 돌리지 않는 이유: 파일 하나 바꾼 뒤 clippy 가 10 초 넘게 걸렸다
- 다른 세션이 고친 파일은 섞이지 않는다. 같은 세션에서 이미 한 번 막혔으면(`stop_hook_active`) 그다음은 통과시키고 기록은 남겨 다음 끝내기 때 다시 잰다
- `cargo` 를 못 찾거나, cargo 가 비정상 종료하거나, 다른 파일의 컴파일 오류로 기록한 파일까지 검사가 닿지 못하면 막지 않고 「검사 못 함」 알림을 띄운다
- 끄는 법: 환경 변수 `RUST_KIT_LINT_ON_STOP=off`. 기록 위치는 `CLAUDE_LINT_STATE_DIR` (기본 `$TMPDIR/claude-lint-edited`)

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
- rust-audit ANALYZE ↔ Pre-Edit Batch Audit, rust-reviewer self-check ↔ Self-Evaluator Audit, Hook-Triggered Auto-Correction ↔ 이 킷의 훅 (당시엔 훅이 없었고 2026-10 `lint-edited-rust` 로 채웠다 — 위 훅 절)
