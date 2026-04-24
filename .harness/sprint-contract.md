---
feature: "kaizen-phase9-rust-kit-kaizen"
created: "2026-04-24"
complexity: "high"
conditions: 22
branch: "kaizen/2026-04-24"
phase: 9
---

# Sprint Contract — Phase 9: Rust-kit Kaizen

Generated: 2026-04-24
Feature: Phase 1~8 누적 9 신규 원칙을 rust-kit 16 스킬 + rust-reviewer 에이전트 + `.claude/skills/rust-kaizen` 에 전수하고, rust-kit 4 REJECT reasons(H-01 · H-03 · SK-03 · AR-02) 을 전수 해소 또는 회귀 방지 검증한다. Phase 9 리서치 테이블 7 건 중 최소 3 건(Axum 0.8 `with_state` · SQLx 0.8 offline cache `cargo sqlx prepare` · Clippy workspace lints) 의 URL 을 변경 근거로 인용한다. infra-kit Phase 8 및 backend-kit Phase 7 sibling 패턴을 rust-kit 에 이식하는 것이 핵심.

Scope (수정 허용): `rust-kit/skills/*/SKILL.md`, `rust-kit/agents/rust-reviewer.md`, `rust-kit/references/*.md`, `rust-kit/README.md`, `rust-kit/evals/evals.json`, `.claude/skills/rust-kaizen/SKILL.md`, `.harness/sprint-contract.md` (본 파일), `.harness/history/` (Phase 8 아카이브), `docs/superpowers/plans/2026-04-06-rust-kit.md` (AR-02 17 vs 20 수치 수정).
범위 외 금지: harness/, flutter-toolkit/, design-kit/, backend-kit/, infra-kit/, react-kit/, reflect-kit/, planning-kit/, `docs/rust/` 리서치 문서 (rust-research 영역), 기타 최상위 파일.

Branch: kaizen/2026-04-24

## Research (R)

Phase 9 리서치 테이블 (phase-research-templates.md §Phase 9) 소스 7 건 중 최소 3 건의 URL 을 변경 근거로 인용한다:

1. [Axum 0.8 `Router::with_state`](https://docs.rs/axum/latest/axum/struct.Router.html#method.with_state) — state 주입 타입 안전성
2. [Axum 0.8 announcement](https://tokio.rs/blog/2025-01-01-announcing-axum-0-8-0) — path 파라미터 `{id}` 중괄호 문법
3. [SQLx `cargo sqlx prepare`](https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md) — offline mode `.sqlx/` 메타데이터
4. [Rust Edition 2024 Guide](https://doc.rust-lang.org/edition-guide/rust-2024/index.html) — edition 전환 기준
5. [Clippy workspace lints](https://context7.com/rust-lang/rust-clippy/llms.txt) — `[workspace.lints.clippy]` SSOT
6. [SeaORM MockDatabase](https://www.sea-ql.org/SeaORM/docs/write-test/mock/) — Docker 없는 단위 테스트
7. fit-pal `server/CLAUDE.md` — Composition Root / Consumer-Owned Port / Domain Event + Outbox 실무 패턴

## Goals (G)

- **G-01**: rust-kit 4 REJECT reason(H-01 · H-03 · SK-03 · AR-02) 전수 해소 또는 회귀 방지 Gotcha 명시
- **G-02**: Phase 1~8 누적 9 신규 원칙(skill §3.5 · §3.6 · §5.5 · §8.7 · §8.8 · §11 + agent §3.5 · §10 · §12) 을 rust-kit 에 전수 반영
- **G-03**: Sibling Consistency (rust-service ↔ backend-system · rust-test ↔ backend-test · rust-audit ↔ backend-audit) 3 쌍 parity 표 추가
- **G-04**: `.claude/skills/rust-kaizen` 에 Phase 8 infra-kaizen 패턴(Cross-Surface Parity Checklist · I-02 예외 목록 · Phase 1~8 감사 Gotcha · README/evals 회귀 방지 Gotcha) 이식
- **G-05**: 계획 파일 `docs/superpowers/plans/2026-04-06-rust-kit.md` 의 "17개" 을 "20개" 로 수정 (AR-02)
- **G-06**: `scripts/validate-plugin.py rust-kit` 7/7 OK 유지 · `run-evals.py rust-kit` pass 유지

## Contract Conditions (C)

### H (Hexagonal/아키텍처 원칙 일관성) — H-01 · H-03 해소

- [x] **H-01**: rust-init Gotcha 에 **domain event + outbox** 원칙 존재 (#8 line ~25 기존 확인). rust-feature Gotcha 에 동일 원칙 존재 (#7 line ~20 기존 확인). 두 스킬 모두 "fit-pal `server/CLAUDE.md` §아키텍처" 출처 명시.
- [x] **H-02 · Composition Root 단일화 rust-init**: rust-init Gotcha #6 에 존재 (line ~23 기존).
- [x] **H-03 · Composition Root 단일화 rust-api**: rust-api Gotchas line 19 에 존재. 동일 문구가 rust-feature Gotcha #6 · rust-service Gotcha "Consumer-Owned Port" 블록에 일관되게 존재. **신규**: rust-api Gotchas 블록에 fit-pal §아키텍처 3번 출처 (이미 존재) 재확인.

### SK (Skill Content) — SK-03 해소

- [x] **SK-03 · rust-api 핸들러 trait DI**: rust-api Step 5 예시 line 147 `State(service): State<Arc<dyn UserService>>` 기반 (기존 확인). PgPool 직접 사용 0 건 (Grep `PgPool` rust-api/SKILL.md — 어댑터 예시 line 98 의 `use sqlx::PgPool;` 은 adapter 레이어로 의도된 용도). **신규 Gotcha**: rust-api Gotchas 에 "핸들러 PgPool/SQLx/SeaORM 직접 import 금지" 명시 강화.
- [x] **SK-04 · Phase 1~8 원칙 스킬 반영**:
  - skill §3.5 QA 계약 1:1 매칭 → rust-audit · rust-reviewer
  - skill §3.6 Rule-by-Rule Audit → rust-audit Gotcha 신규 + Step 3 에 Rule-by-Rule 14-row 표 + rust-reviewer 핵심 규칙
  - skill §5.5 Enumerate-before-Act → rust-init · rust-feature Gotcha 신규
  - skill §8.7 Code Examples → code-fence 0 bare 유지 (validate-plugin V6)
  - skill §8.8 Sibling Consistency → rust-test Gotcha 신규 (backend-test parity), rust-service Gotcha 신규 (backend-system parity), rust-audit Gotcha 신규 (backend-audit parity)
  - skill §11 Cross-Surface Parity → rust-kaizen Gotcha 신규 sibling group 3 종
  - agent §3.5 Binary Decidability → rust-audit Gotcha 신규 + rust-reviewer 규칙 신규
  - agent §10 Unverifiable 마커 → rust-audit Gotcha 신규 + rust-reviewer 출력 포맷 신규
  - agent §12 L3 Coverage Honesty → rust-reviewer 최종 판정 규칙 신규 (CONDITIONAL APPROVE)

### AR (Architecture / 구조)

- [x] **AR-01 · sibling 패턴 이식**: `.claude/skills/rust-kaizen` 에 Phase 8 infra-kaizen Gotcha #6/#7/#8/#9/#10 pattern 을 rust 용으로 이식. Sibling group 표는 rust-guide 없음 이므로 (rust-init · rust-feature) · (rust-audit · rust-reviewer) · (rust-test · backend-test) · (rust-service · backend-system) · (rust-audit · backend-audit) 5 종.
- [x] **AR-02 · 리서치 문서 수 통일**: `docs/superpowers/plans/2026-04-06-rust-kit.md` 의 "17개" → "20개" 2 곳 수정. rust-kit/README.md:42 의 "20개" 기존 확인. 최종 실제 docs/rust/ 하위 .md 파일 카운트 = 20 과 일치.
- [x] **AR-03 · I-02 예외 목록 명시화**: rust-kaizen Gotcha 신규 — `.harness/sprint-contract.md` · `.harness/sprint-feedback.md` · `.harness/.meta/kaizen-data-pool.md` · `.vscode/` · sync-docs 자동 갱신 README/HTML 예외. **추가**: Rust 전용 산출물 예외 — `Cargo.toml`, `migrations/*.sql` (산출물 placeholder/code-fence 검사에서 제외).

### I (Integrity / 무결성)

- [x] **I-01 · Phase 8 히스토리 아카이브**: `.harness/history/20260424-phase8-sprint-contract.md` · `20260424-phase8-sprint-feedback.md` 존재 확인.
- [x] **I-02 · Working tree modified 예외**: 커밋 직전 `git status --short` 실행 결과 modified/untracked 가 위 예외 목록(AR-03) 에 한정.
- [x] **I-03 · validate-plugin 회귀 방지**: `python3 scripts/validate-plugin.py rust-kit` 7/7 OK 유지 (V1~V7 모두 OK).
- [x] **I-04 · run-evals 회귀 방지**: `python3 scripts/run-evals.py rust-kit` exit 0.

### E (External / 외부 인용)

- [x] **E-01 · Context7 최소 3 건 인용**: Axum 0.8 `with_state` + SQLx `cargo sqlx prepare` + Clippy workspace lints 중 최소 3 URL 을 변경된 SKILL.md Gotcha 또는 References 섹션에 포함.
- [x] **E-02 · 변경 근거 커밋 메시지**: Phase 9 리서치 표 7 건 중 인용한 3 건 이상을 커밋 메시지 "Phase 9 리서치" 섹션에 명시.

## Verdict Rules

- APPROVE: 22 condition 전수 PASS + 미검증 0 건.
- CONDITIONAL APPROVE: 22 condition 전수 PASS + `[미검증]` 태그 1 건.
- REJECT: FAIL 1 건 이상 또는 `[미검증]` 2 건 이상.

## References

- `.claude/kaizen-input/plugin-qa-data.md` §rust-kit (REJECT reasons 4 건 원문)
- `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` §Phase 9
- `rust-kit/skills/*/SKILL.md` (16 개), `rust-kit/agents/rust-reviewer.md`, `rust-kit/README.md`
- `backend-kit/skills/backend-audit/SKILL.md` (sibling ground truth — 20-row Rule-by-Rule 표)
- `infra-kit/skills/infra-audit/SKILL.md` (sibling ground truth — CONDITIONAL APPROVE 프로토콜)
- `harness/docs/guides/skill-design-guide.md` §3.5 · §3.6 · §5.5 · §8.7 · §8.8 · §11
- `harness/docs/guides/agent-design-guide.md` §3.5 · §10 · §12
- fit-pal `server/CLAUDE.md` §아키텍처 1~4 번
