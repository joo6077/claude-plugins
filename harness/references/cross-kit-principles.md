# Cross-Kit Principles Application Matrix

> Phase 1 (skill-design-guide v1.3.0 / agent-design-guide v1.3.0) 에서 추가/변경된
> 신규 원칙이 각 kit (flutter-toolkit, design-kit, backend-kit, infra-kit, rust-kit,
> react-kit, planning-kit, reflect-kit) 에 어떻게 적용되는지 매트릭스로 정리한다.
> 본 문서는 카이젠 사이클마다 갱신되며, 각 kit 의 README 또는 SKILL.md 가 본 문서를 cross-reference 한다.
>
> **현재 버전: v1 (2026-05-07 카이젠 사이클 Phase 5~12)**

## 배경

2026-05-07 카이젠 사이클은 `/insights` 30 일 세션 분석 (Friction Points + Recommended
Patterns + Feature Suggestions) 을 데이터 풀 §0 으로 자동 통합했다 (Step 0). Phase 1
이 그 결과로 5 건의 신규 원칙을 가이드에 반영했고 (`Pre-Edit Batch Audit`,
`Pre-Sprint Sync Check`, `Session Lifecycle 카테고리`, `Hook-Triggered Auto-Correction`,
`Self-Evaluator Rule-by-Rule Audit`), 이를 8 개 plugin kit 에 전수 적용해야 한다.

각 kit 별로 무거운 변경을 만드는 대신 본 문서에 매핑을 1 회만 명시하고, 각 kit README 가
"참조" 섹션에서 본 문서를 가리킨다. 카이젠의 cross-surface parity 원칙 (skill-design-guide
§11) 을 kit 레벨까지 확장한 형태.

## 신규 원칙 ↔ Kit 적용 매트릭스

| 원칙 (Phase 1 v1.3.0) | flutter-toolkit | design-kit | backend-kit | infra-kit | rust-kit | react-kit | planning-kit | reflect-kit |
|------------------------|-----------------|------------|-------------|-----------|----------|-----------|--------------|-------------|
| **1. Pre-Edit Batch Audit** (skill §3.6) — 리팩터링 시작 전 위반 enumerate → 사용자 승인 → 일괄 편집 | flutter-audit / flutter-extract 의 ANALYZE 단계가 이미 enumerate. 명시적 cross-ref. | design-audit ANALYZE 단계와 동일 패턴. cross-ref. | backend-audit ANALYZE. cross-ref. | infra-audit ANALYZE. cross-ref. | rust-audit ANALYZE. cross-ref. | react-audit ANALYZE 6 카테고리. cross-ref. | plan-audit + plan-discover 의 enumerate 단계에 cross-ref. | reflect-digest 의 카테고리별 집계 자체가 enumerate. cross-ref. |
| **2. Pre-Sprint Sync Check** (skill §9) — Long-running 스킬 시작 전 git fetch + log inspection | flutter-toolkit 의 멀티 스킬 sprint (예: flutter-feature) 진입 직전 적용. | design-kit sprint 진입 직전. | backend-kit sprint 진입 직전. | infra-kit sprint 진입 직전. | rust-kit sprint 진입 직전. | react-kit sprint (Clean Arch 4 layer) 진입 직전. | plan-discover/plan-prd 진입 직전. | (해당 없음 — reflect-kit 은 단일 호출 흐름) |
| **3. Session Lifecycle 카테고리** (skill §2 10번째 유형) — handoff/work-summary/resume 등 | (해당 없음 — flutter 도메인 무관) | (해당 없음) | (해당 없음) | (해당 없음) | (해당 없음) | (해당 없음) | plan-prd / plan-stories 의 sprint handoff 시점 적용 가능. | **핵심 적용** — reflect-kit 은 본질적으로 Session Lifecycle 카테고리. |
| **4. Hook-Triggered Auto-Correction** (agent §6 패턴 7) — PostToolUse + read-only reviewer | flutter-toolkit 의 PostToolUse 훅으로 dart format / analyze 자동 실행 + flutter-audit reviewer (deep mode) spawn 가능. | design-audit reviewer + PostToolUse 의 lint 협업. | backend-kit + PostToolUse pytest/lint. | infra-kit + PostToolUse hadolint/actionlint. | rust-kit + PostToolUse cargo fmt/clippy. | react-kit + PostToolUse eslint/tsc/biome. | (해당 없음 — 기획 산출물은 결정론적 lint 부재) | reflect-kit 의 3 훅 자체가 본 패턴의 한 구현. cross-ref. |
| **5. Self-Evaluator Rule-by-Rule Audit** (agent §10) — verdict 직전 자기 카테고리 전수 self-check | flutter-audit / widget-inspector 의 self-check 단계. cross-ref. | design-reviewer self-check 단계. cross-ref. | backend-reviewer self-check. cross-ref. | infra-reviewer self-check. cross-ref. | rust-reviewer self-check. cross-ref. | react-reviewer 6 카테고리 self-check. cross-ref. | planning-reviewer self-check. cross-ref. | (해당 없음 — reflect-kit reviewer 부재) |

## 적용 절차 (각 kit README 의 "참조" 섹션 표준 문구)

```markdown
## 참조 (Cross-Kit Principles)

본 kit 는 **harness/references/cross-kit-principles.md** 의 Phase 1 v1.3.0 신규 원칙
5 건 (Pre-Edit Batch Audit / Pre-Sprint Sync Check / Session Lifecycle / Hook-Triggered
Auto-Correction / Self-Evaluator Rule-by-Rule Audit) 을 본 kit 의 audit / reviewer /
sprint-entry 흐름에 매트릭스대로 적용한다. 자세한 적용 위치는 매트릭스 행/열 참조.
```

## 카이젠 사이클별 추가 원칙

다음 카이젠 사이클에서 Phase 1 이 새 원칙을 추가하면 본 매트릭스에 행을 추가하고
"현재 버전" 을 bump 한다. 본 문서는 cross-surface parity 의 단일 진실 원천 (single
source of truth) 으로 기능한다.

### 변경 이력

- **v1 (2026-05-07)** — 초기 작성. Phase 1 v1.3.0 신규 원칙 5 건 × 8 kit 매트릭스.
  reflect-kit (Phase 12 신규) 첫 포함. `/insights` Friction #1·#2·#3 흡수 결과 명시.
