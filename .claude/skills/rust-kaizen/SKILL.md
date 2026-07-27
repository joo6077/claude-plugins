---
name: rust-kaizen
description: >
  rust-kit 스킬 품질을 docs/rust/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, rust-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, design-kaizen과 동일한 패턴.
  "/rust-kaizen", "Rust 카이젠", "rust-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

0. **재발한 규칙은 문장을 다시 쓰지 말고 등급을 올려라 (skill-design-guide §3.7 Enforcement 등급)** — 데이터에 이미 승격된 원칙이 또 나오면 표현을 다듬는 것은 개선이 아니다. 등급 사다리와 승급 기준은 `harness/docs/guides/skill-design-guide.md` §3.7 이 **정본(SSOT)** 이다 — 여기서 등급을 다시 정의하거나 동의어를 만들지 않고, 개선 전에 그 절을 읽고 판정한다. 등급 판정 결과(현재 등급 → 목표 등급 → 근거 빈도)를 카이젠 리포트에 명시한다. 신호가 0 건이면 **NO_CHANGE** 가 정답이다 — 억지 변경 금지.
1. **리서치 문서 없이 개선 금지** — docs/rust/ 문서를 먼저 읽고, 그 기준으로만 개선한다.
2. **스킬 삭제 금지** — 기존 스킬을 삭제하지 않는다. 개선만 한다.
3. **범위는 파일 수가 아니라 unit(관심사) 수로 센다** — "한 번에 1~2 개 스킬" 같은 파일 수 기준은 오해를 만든다. 하나의 원칙(예: "명령 실행 규약")을 sibling 3 개 스킬에 **동일 문구로 복제**하는 것은 1 unit 이며 scope creep 이 아니다. 반대로 서로 무관한 관심사 2 개를 한 세션에 섞으면 파일이 2 개여도 scope creep 이다. **세션당 3~4 unit** 을 상한으로 삼고, 각 unit 이 어떤 데이터 신호(빈도·REJECT ID)에서 나왔는지 리포트에 1:1 로 적는다.
4. **validate-plugin.py 실행 없이 완료 선언 금지** — 카이젠 종료 시 `scripts/validate-plugin.py rust-kit`을 실행하라. 회귀가 있으면 즉시 수정한다.
5. **Gotchas에 Rust 컴파일러가 이미 잡는 실수를 넣지 마라** — borrow checker, lifetime, type mismatch는 컴파일러가 잡으므로 Gotchas에 불필요하다. 런타임 실수나 설계 실수만 추가한다.
6. **Cross-Surface Parity Checklist (skill-design-guide §11 · agent-design-guide §12 대응)** — 스킬 개선 시 아래 sibling group 간 공통 원칙(Gotcha · Process Step · 예시) 의 누락을 **1:1 Grep 대조** 로 확인한다. 누락된 sibling 이 있으면 즉시 동일 표현을 복제하여 비대칭 지식 상태를 제거한다 (2026-04 rust-kit Phase 9 에서 backend-kit Phase 7 · infra-kit Phase 8 패턴 계승 드리프트 차단).

   | Sibling Group | 공통 원칙 검증 항목 |
   |---------------|---------------------|
   | rust-init · rust-feature · rust-service · rust-api | **Composition Root 단일화 + Consumer-Owned Port + Domain Event + Outbox + 포트에서 인프라 타입 제거** 4 항목 일관 존재 |
   | rust-audit · rust-reviewer (agent) | **Binary Decidability Pre-Check · Rule-by-Rule Audit · 미검증 마커 · L3 Coverage Honesty** 4 항목 동시 존재 |
   | rust-audit · backend-audit | **10+ row Rule-by-Rule 표 + CONDITIONAL APPROVE 규칙 + Rust 고유 카테고리(Ownership / Async / unsafe / SQLx offline)** |
   | rust-test · backend-test | **Step 0 스택 감지 독립 단계 + 기존 패턴 탐색 + SeaORM MockDatabase · #[sqlx::test] · testcontainers 3 단계** |
   | rust-service · backend-system (Phase 7) | **Outbox · Circuit Breaker · OAuth 2.1 · RFC 9457 problem+json** 중 Rust 맥락에서 적용 가능한 원칙 참조 |
   | rust-run · rust-preflight · rust-test | **명령 실행 규약 3 항목** — (a) `PKG_TARGETS` 확인 후 타깃 필터 (bin-only 패키지 `--lib` 금지) (b) `set -o pipefail` + 파이프라인 직후 `rc=$?` 종료 코드 캡처 + 리포트 기록 (c) 실행된 테스트 수 0 을 PASS 로 쓰지 않기 |
   | rust-api · rust-model | **Counterpart Enumeration** — 계약/스키마 변경 시 producer·consumer 파일 양면 열거 + 체크리스트 아티팩트(E2) |
   | rust-service · rust-api | **외부 크레이트 문서 조회 기록** (crate · 버전 · URL 3 항목) + **편집 전 Read** |

7. **I-02 예외 목록 명시화** — 카이젠 세션 커밋 직전 `git status --short` 점검 시 modified/untracked 허용 예외는 고정 목록이다: `.harness/sprint-contract.md` (생성 대상) · `.harness/sprint-feedback.md` (QA 산출물) · `.harness/.meta/kaizen-data-pool.md` (auto-regenerated) · `.vscode/` (untracked) · sync-docs 자동 갱신 README/HTML. 이 외 modified 0 건이어야 한다 (2026-04 rust-kit I-02 회귀 방지 — Phase 6/7/8 design-kit/backend-kit/infra-kit 패턴 계승). **Rust 전용 산출물 예외**: rust-kit 의 산출물에 `Cargo.toml` · `rust-toolchain.toml` · `migrations/*.sql` · `deny.toml` 이 포함될 경우 placeholder/bare code-fence 규칙의 `.md` 전용 검사에서 제외한다 (파일 포맷상 태그 없는 fence 가 정상).
8. **Phase 1~8 신규 원칙 감사 (kaizen 시작 시 전수 확인)** — skill §3.5 QA 계약 1:1 매칭 / §3.6 Rule-by-Rule Audit / §5.5 Enumerate-before-Act / §8.7 Code Examples / §8.8 Sibling Consistency / §11 Cross-Surface Parity · agent §3.5 Binary Decidability / §10 Unverifiable / §12 L3 Coverage Honesty 9 항목 전수 확인. 각 원칙에 대해 반영 스킬 목록을 리포트에 명시.
9. **REJECT reason 회귀 방지 Grep 체크** — 카이젠 세션 종료 시 아래 체크를 수행:
   - H-01: `grep -c "domain event\|outbox" rust-kit/skills/rust-init/SKILL.md rust-kit/skills/rust-feature/SKILL.md` 각각 >= 1
   - H-03: `grep -c "Composition Root" rust-kit/skills/rust-api/SKILL.md` >= 1
   - SK-03: `grep -n "State<PgPool>\|State<sqlx::\|State(pool)" rust-kit/skills/rust-api/SKILL.md` 0 건 (핸들러 레이어 state 는 `Arc<dyn ...>` trait object 만 허용)
   - AR-02: `grep -rn "17개 리서치\|17 리서치\|docs/rust/ 리서치 문서 17" .` 0 건 (리서치 문서 실제 수 20 과 일치)
   - **DG-03** (마이그레이션 미적용 테스트 실패): `grep -c "마이그레이션" rust-kit/skills/rust-preflight/SKILL.md rust-kit/skills/rust-test/SKILL.md` 각각 >= 1
   - **API-01** (mock-only 를 통합 테스트로 주장): `grep -c "MockDatabase" rust-kit/skills/rust-test/SKILL.md` >= 1 이면서 "통합 테스트로 주장하지 마라" 문구 존재
   - **cargo-test-wrong-target**: `grep -c -- "--bins" rust-kit/skills/rust-run/SKILL.md rust-kit/skills/rust-test/SKILL.md rust-kit/references/project-detection.md` 각각 >= 1
   - **exit-code capture**: `grep -c "pipefail" rust-kit/skills/rust-run/SKILL.md` >= 1
   - **Axum 0.8 path 예시 드리프트**: `grep -rn '"/[a-z_/]*:[a-z_]\+"' rust-kit/skills/*/SKILL.md` 결과가 **negative example(금지 예시) 문맥 밖**에 있으면 FAIL
10. **16 스킬 + 1 에이전트 전수 모드** — 다른 kit 과 달리 rust-kit 은 16 개 SKILL.md + rust-reviewer 총 17 surface 로 대규모다. 한 세션에서 17 개 전체를 깊게 고칠 수 없으므로 **우선순위 3 계층** (1) REJECT 직접 대상 (rust-init · rust-feature · rust-api) → (2) Phase 1~8 원칙 핵심 surface (rust-audit · rust-reviewer · rust-test · rust-service) → (3) 잔여 10 스킬 경량 audit 으로 단계 분할하고 각 단계 완료 후 `validate-plugin.py` 를 실행한다.

# Process

## Step 1: 현재 상태 읽기

rust-kit 스킬 16 개 + rust-reviewer 에이전트:
- rust-kit/skills/{rust-init,rust-feature,rust-api,rust-model,rust-service,rust-auth,rust-middleware,rust-grpc,rust-test,rust-docker,rust-error,rust-l10n,rust-run,rust-build,rust-preflight,rust-audit}/SKILL.md
- rust-kit/agents/rust-reviewer.md

## Step 2: 격차 분석

docs/rust/ 원칙 vs 스킬 반영 상태:
- fundamentals/{ownership-borrowing,error-handling,async-concurrency,testing,project-structure,performance,hexagonal-architecture}.md
- web/{axum-patterns,authentication,middleware,openapi}.md
- data/{sqlx-patterns,migrations,caching}.md
- protocols/{grpc-tonic,graphql,realtime}.md
- ops/{docker,ci-cd,observability}.md
- 글로벌 피드백 (~/.harness/feedback/)

## Step 3: 개선 적용

- SKILL.md Gotchas 추가/수정 (우선순위 3 계층 순서로)
- rust-audit/references/audit-criteria.md 체크리스트 갱신 (존재 시)
- rust-reviewer.md 출력 포맷 / L3 Coverage Honesty 규칙 갱신
- templates/ 갱신 (필요 시)

## Step 4: 검증

- description 트리거 조건 유지 확인
- 리서치 문서 ↔ 스킬 references 경로 정합성
- Cross-Surface Parity Grep 대조 (Gotcha 6)
- REJECT 4 reason 회귀 체크 (Gotcha 9)

## Step 5: 커밋

```text
chore(kaizen-phase<N>): [개선 내용 요약]
```

## Step 6: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `scripts/validate-plugin.py rust-kit` 을 실행하여 **8 카테고리(V1~V8: frontmatter · templates · refs · triggers · placeholders · code-fence · plugin-json · hook-exec)** 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은 `harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT) — 해당 섹션을 그대로 따른다.

# References

- rust-kit/skills/ — 개선 대상 스킬 (16 개)
- rust-kit/agents/rust-reviewer.md — 독립 평가 에이전트
- rust-kit/references/project-detection.md — 스택 감지 공통 절차
- rust-kit/evals/evals.json — 플러그인 evals
- docs/rust/ — 리서치 SSOT (fundamentals / web / data / protocols / ops · 20 문서)
- backend-kit/skills/backend-audit/SKILL.md — sibling ground truth (10 카테고리 Rule-by-Rule · CONDITIONAL APPROVE)
- infra-kit/skills/infra-audit/SKILL.md — sibling ground truth (Phase 8 Rule-by-Rule 20-row)
- harness/docs/guides/skill-design-guide.md — §3.5 · §3.6 · §5.5 · §8.7 · §8.8 · §11 신규 원칙 SSOT
- harness/docs/guides/agent-design-guide.md — §3.5 · §10 · §12 신규 원칙 SSOT
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 8 카테고리(V1~V8) 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
- `scripts/run-evals.py` — 플러그인 evals 자동화 도구
