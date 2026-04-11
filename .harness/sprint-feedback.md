# Sprint Feedback
Feature: rust-kit 16 스킬 + references 2026 최신 생태계 반영 카이젠 (Phase 9)
Evaluated: 2026-04-11 15:30
Verdict: REJECT
Iteration: 1

## Results

### R — Research & Rust 2024 Edition (4/4)
- [x] R-01: rust-init Gotchas에 edition="2024" + resolver="3" 기본 채택 + 2021/2024 매트릭스 — PASS
  - 근거: `rust-kit/skills/rust-init/SKILL.md:16` (Gotcha #2), `rust-kit/skills/rust-init/SKILL.md:153` (Cargo.toml 예시 `edition = "2024"`)
- [x] R-02: rust-init Process에 rust-toolchain.toml channel/components/profile 3요소 + 2 옵션 — PASS
  - 근거: `rust-kit/skills/rust-init/SKILL.md:219-226` (§4b 템플릿)
- [x] R-03: rust-init Process에 [workspace.lints] SSOT 패턴 + 3 네임스페이스 + pedantic deny + 노이즈 allow + member 규약 — PASS
  - 근거: `rust-kit/skills/rust-init/SKILL.md:21-22` (Gotcha #7), `rust-kit/skills/rust-init/SKILL.md:170-213` (§4a 템플릿)
- [x] R-04: rust-init Process에 deny.toml v2 형식 초기 템플릿 + advisories/licenses/bans/sources 섹션 — PASS
  - 근거: `rust-kit/skills/rust-init/SKILL.md:228-266` (§4c 템플릿)

### A — Axum 0.8 breaking changes (5/5)
- [x] A-01: rust-api Gotcha에 Axum 0.8 path parameter :id → {id} breaking change + 코드 예시 교체 — PASS
  - 근거: `rust-kit/skills/rust-api/SKILL.md:13` (Gotcha), `rust-kit/skills/rust-api/SKILL.md:169` (라우터 예시 `/users/{id}`)
- [x] A-02: rust-api Gotcha에 async_trait 제거 + native async fn 사용 + axum::async_trait deprecated — PASS
  - 근거: `rust-kit/skills/rust-api/SKILL.md:14` (Gotcha)
- [x] A-03: rust-auth extractor에서 async_trait 제거, native async fn 형태 + Gotcha 명시 — PASS
  - 근거: `rust-kit/skills/rust-auth/SKILL.md:16` (Gotcha #4), `rust-kit/skills/rust-auth/SKILL.md:167-173` (extractor 구현)
- [x] A-04: rust-middleware tower-http 0.6.x 명시 + feature 조합 + :id 잔재 없음 — PASS
  - 근거: `rust-kit/skills/rust-middleware/SKILL.md:14` (Gotcha #2)
- [x] A-05: rust-api Router::with_state + Arc<dyn Trait> + path {id} 통일 — PASS
  - 근거: `rust-kit/skills/rust-api/SKILL.md:141,169,171` (핸들러 + 라우터 예시)

### D — Database layer — SQLx 0.8 + SeaORM 1.1 (4/4)
- [x] D-01: rust-model ORM 선택 분기 섹션 + SeaORM 경로 fit-pal 패턴 명시 — PASS
  - 근거: `rust-kit/skills/rust-model/SKILL.md:13-15` (Gotcha), `rust-kit/skills/rust-model/SKILL.md:32-35` (§0a 분기 표), `rust-kit/skills/rust-model/SKILL.md:204-303` (SeaORM 어댑터)
- [x] D-02: rust-model SQLx 0.8 runtime feature 최신 조합 명시 — PASS
  - 근거: `rust-kit/skills/rust-model/SKILL.md:15-16` (Gotcha — runtime-tokio + tls-rustls)
- [x] D-03: rust-model SeaORM 마이그레이션 CLI + 런타임 2종 + SQLx 기존 유지 — PASS
  - 근거: `rust-kit/skills/rust-model/SKILL.md:430-457` (§7S), `rust-kit/skills/rust-model/SKILL.md:414-426` (§7X)
- [x] D-04: rust-test SeaORM MockDatabase 분기 추가 + serial_test + TRUNCATE 격리 — PASS
  - 근거: `rust-kit/skills/rust-test/SKILL.md:14-17` (Gotcha), `rust-kit/skills/rust-test/SKILL.md:219-266` (§7S)

### H — Hexagonal / Consumer-Owned Port (1/3)
- [x] H-02: rust-api/rust-service 포트에서 인프라 타입 제거 원칙 — PASS
  - 근거: `rust-kit/skills/rust-api/SKILL.md:18` (Gotcha), `rust-kit/skills/rust-service/SKILL.md:17` (Gotcha)
- [ ] H-01: rust-init/rust-feature Gotchas에 Consumer-Owned Port + domain event + outbox 원칙 — FAIL
  - 근거: `rust-kit/skills/rust-init/SKILL.md` Gotcha #5에 Consumer-Owned Port는 있으나 "cross-module write 후처리는 domain event + outbox"가 없음. `rust-kit/skills/rust-feature/SKILL.md` Gotcha #5에도 동일하게 누락. domain event + outbox 원칙은 `rust-kit/skills/rust-service/SKILL.md:18` (Gotcha)에만 있음.
  - 수정: rust-init Gotcha #5 또는 #6 하단에 "cross-module write 후처리(알림 발송, 감사 로그, 인덱스 동기화)는 직접 호출 대신 domain event 발행 + outbox 테이블 기록으로 처리한다" 원칙을 추가. rust-feature Gotcha에도 동일 추가.
- [ ] H-03: rust-feature/rust-api Gotchas에 Composition Root 단일화 원칙 — FAIL
  - 근거: `rust-kit/skills/rust-feature/SKILL.md:19` (Gotcha #6)에는 있음. 그러나 `rust-kit/skills/rust-api/SKILL.md` Gotchas 전체를 확인한 결과 Composition Root 단일화 원칙이 없음 — "Composition Root" 문자열 검색 결과 0건.
  - 수정: rust-api Gotchas에 "모듈 조립(`Arc<dyn Port>` 와이어링)은 apps/api/src/main.rs 한 곳에서만 한다. 핸들러가 서비스 구현체를 직접 생성하지 않는다" 원칙 추가.

### T — Tonic 0.13 + Testing + Tooling (4/4)
- [x] T-01: rust-grpc tonic/prost/tonic-build 0.13 버전 + #[tonic::async_trait] 유지 원칙 — PASS
  - 근거: `rust-kit/skills/rust-grpc/SKILL.md:37-47` (의존성), `rust-kit/skills/rust-grpc/SKILL.md:16` (Gotcha #4)
- [x] T-02: rust-test SeaORM MockDatabase + mockall 병행 + test_support 모듈 + multi_thread 기준 — PASS
  - 근거: `rust-kit/skills/rust-test/SKILL.md:14-19` (Gotcha 전반), `rust-kit/skills/rust-test/SKILL.md:16-17` (test_support + multi_thread)
- [x] T-03: rust-run/rust-preflight Makefile 타겟 + 환경변수 주입 필수 원칙 — PASS
  - 근거: `rust-kit/skills/rust-run/SKILL.md:21-25` (Gotcha #7), `rust-kit/skills/rust-preflight/SKILL.md:19` (Gotcha #5)
- [x] T-04: rust-run audit 서브커맨드에 cargo deny check v2 포함 — PASS
  - 근거: `rust-kit/skills/rust-run/SKILL.md:20` (Gotcha #6), `rust-kit/skills/rust-run/SKILL.md:43,45-47` (Step 1 표 + audit 우선순위)

### C — Clippy lints + error patterns (4/4)
- [x] C-01: audit-criteria.md Clippy pedantic 2026 기준 카테고리 — PASS
  - 근거: `rust-kit/skills/rust-audit/references/audit-criteria.md:11-14` (needless_pass_by_value, redundant_clone, cloned_instead_of_copied, inefficient_to_string), `audit-criteria.md:33` (large_futures)
- [x] C-02: audit-criteria.md Security에 unsafe_code forbid + unwrap/expect 범위 완화 — PASS
  - 근거: `rust-kit/skills/rust-audit/references/audit-criteria.md:41` (unsafe_code forbid), `audit-criteria.md:21` (unwrap/expect 범위)
- [x] C-03: rust-error Gotcha에 anyhow::Error domain 금지 원칙 — PASS
  - 근거: `rust-kit/skills/rust-error/SKILL.md:13` (Gotcha 첫 번째)
- [x] C-04: rust-audit Gotcha에 workspace lints 기반 lint 발견 절차 — PASS
  - 근거: `rust-kit/skills/rust-audit/SKILL.md:20-21` (Gotcha #5, #6)

### P — Preventive / regressions (5/5)
- [x] P-01: unimplemented! 2건 (rust-api) + 3건 (rust-auth) 유지 + 스켈레톤 주석 명시 — PASS
  - 근거: `rust-kit/skills/rust-api/SKILL.md:111,115`, `rust-kit/skills/rust-auth/SKILL.md:129,133,137` — 모두 "예시 스켈레톤 — ... 구현 필요" 메시지 포함
- [x] P-02: rust-l10n Axum 0.8 axum::extract::Request/Next API 유지 명시 — PASS
  - 근거: `rust-kit/skills/rust-l10n/SKILL.md:16` (Gotcha 세 번째)
- [x] P-03: bare fenced code block 0건 — PASS
  - 근거: `python3 scripts/validate-plugin.py rust-kit --check=code-fence` → "V6 code-fence 0 bare — OK"
- [x] P-04: 파일 끝 newline 1개 유지 — PASS
  - 근거: 검증된 5개 파일 모두 0x0a (newline)으로 끝남
- [x] P-05: validate-plugin 7 OK + sync-docs 통과 — PASS
  - 근거: `python3 scripts/validate-plugin.py` → "Total: 7 plugins, 7 OK, Exit: 0". `python3 scripts/sync-docs.py --check-only` → "모든 README가 동기화 상태입니다"

### Anti-patterns (1/1)
- [x] AP-03: bare code fence 0건 — PASS (validate-plugin V6 확인)

### Diagnostics
- 런타임 검증 미수행 — MCP 서버 미설정
- analyze/test: rust-kit은 편집 전용 스킬 파일, 빌드/런타임 없음 (계약 Commands 명시)

## Summary
- Total: 27/29 conditions passed
- Verdict: REJECT
- FAIL 항목:
  1. **H-01** (high): rust-init, rust-feature Gotchas에 "cross-module write 후처리는 domain event + outbox"가 누락됨
  2. **H-03** (high): rust-api Gotchas에 Composition Root 단일화 원칙이 누락됨
- 수정 우선순위: H-01 → H-03 순서로 2개 파일 편집 후 재평가

---

# Sprint Feedback — Iteration 2
Feature: rust-kit 16 스킬 + references 2026 최신 생태계 반영 카이젠 (Phase 9)
Evaluated: 2026-04-11 16:00
Verdict: APPROVE
Iteration: 2

## Scope

iter1 FAIL 조건 H-01, H-03만 재검증. iter1 PASS 조건 27개는 PASS 유지.

## Results — 재검증 조건

### H — Hexagonal / Consumer-Owned Port (3/3)

- [x] H-01: rust-init/rust-feature Gotchas에 Consumer-Owned Port + domain event + outbox 원칙 — PASS
  - 근거 (rust-init): `rust-kit/skills/rust-init/SKILL.md:22` (Gotcha #8) — "cross-module write 후처리(알림 발송, 감사 로그, 인덱스 동기화)는 직접 호출 대신 domain event 발행 + outbox 테이블 기록으로 처리한다. 트랜잭션 경계 안에서 write + outbox insert를 원자적으로 실행하고 별도 워커가 outbox를 폴링하여 외부 시스템에 전달한다." — 계약 원문과 정확히 일치 (L3)
  - 근거 (rust-feature): `rust-kit/skills/rust-feature/SKILL.md:20` (Gotcha #7) — 동일 원칙이 feature 스킬 컨텍스트에 맞게 service.rs write + outbox insert 원자적 실행 및 워커 폴링까지 명시 (L3)
- [x] H-02: rust-api/rust-service 포트에서 인프라 타입 제거 원칙 — PASS (iter1 유지)
  - 근거: `rust-kit/skills/rust-api/SKILL.md:18` (iter1 확인 완료)
- [x] H-03: rust-feature/rust-api Gotchas에 Composition Root 단일화 원칙 — PASS
  - 근거 (rust-api): `rust-kit/skills/rust-api/SKILL.md:19` (Gotcha 마지막 항목) — "Composition Root 단일화 — 핸들러가 서비스 구현체를 직접 UserServiceImpl::new(...)로 생성하지 마라. 모듈 조립(DI 와이어링)은 apps/api/src/main.rs 한 곳에서만 하고, 핸들러는 State<Arc<dyn UserServicePort>>로 trait object만 받는다." — iter1 FAIL 사유(0건)가 해소됨. main.rs 단일 조립 + Arc<dyn Port> 주입까지 구체 기술 (L3)
  - 근거 (rust-feature): `rust-kit/skills/rust-feature/SKILL.md:19` (Gotcha #6) — iter1 PASS 유지

## Summary

- Total: 29/29 conditions passed (27 iter1 PASS 유지 + H-01 + H-03 신규 PASS)
- Verdict: APPROVE
- FAIL 항목: 없음
