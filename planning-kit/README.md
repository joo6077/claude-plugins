# planning-kit

스택 무관 제품 기획 플러그인. 아이디어를 Sprint Contract 로 넘어갈 수 있는 수준의 기획 산출물로 변환한다.

## 개요

planning-kit 은 harness 파이프라인의 **0번 단계**다. "기획 → 계약 → 구현 → QA" 흐름에서 sprint-contract 보다 앞에 위치하며, 문제 정의·PRD·우선순위·리스크·개념 데이터 모델·GitHub 동기화까지 한 벌로 다룬다.

다른 kit(backend-kit, rust-kit 등) 이 "구현 단계의 스키마"를 만든다면, planning-kit 은 "개념 단계의 도메인 모델"을 만든다. Mermaid erDiagram / flowchart / sequenceDiagram 으로 시각화한다.

## 스킬

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `plan-audit` | 완성된 기획 산출물을 카테고리별 PASS/FAIL 로 체계적 감사한다. |
| `plan-data-model` | 기획 단계에서 개념 데이터 모델을 Mermaid erDiagram + classDiagram 으로 작성한다. |
| `plan-discover` | 아이디어를 받아 소크라테스식 질문으로 문제·사용자·가정·성공기준을 드러낸다. |
| `plan-flow` | 기능의 유저 플로우, 서비스 블루프린트, 상태 머신을 Mermaid 다이어그램으로 작성한다. |
| `plan-guide` | 기획 문서나 아이디어에 대해 가벼운 원칙 기반 피드백을 제공한다. |
| `plan-ideate` | 제품 기획의 0단계 — 막연한 생각 덩어리를 발산(divergent) · 정리(organize) · 수렴(convergent)하여 |
| `plan-prd` | discovery 산출물 또는 충분히 정의된 문제를 받아 PRD(Product Requirements Document)를 작성한다. |
| `plan-prioritize` | 스토리 또는 기능 후보를 받아 RICE/Kano/WSJF/MoSCoW 중 컨텍스트에 맞는 프레임워크를 선택해 스코어링한다. |
| `plan-reference` | "X 같은 앱 만들고 싶다" 요청을 레퍼런스 제품 teardown + 기능 매트릭스 + 차별화 포인트로 정리한다. |
| `plan-risks` | 기획 산출물에 Pre-mortem, Inversion thinking, 인지 편향 체크리스트를 적용하여 |
| `plan-stories` | PRD 또는 기능 설명을 받아 유저 스토리로 분해한다. INVEST 기준 검증과 |
| `plan-sync-github` | 기획 산출물(PRD, Stories, Priorities)을 GitHub Issues · Milestones · Projects v2 에 동기화한다. |
<!-- /AUTO:skills -->

## 에이전트

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| `planning-reviewer` | 기획 산출물을 원칙 기준으로 독립 평가한다. plan-audit 스킬에서 Agent 도구로 위임받아 실행된다. |
<!-- /AUTO:agents -->

## harness 연계

```text
생각 덩어리 / "X 같은 앱"
  ↓ /plan-reference      ("X 같은" 일 때, teardown + Feature Matrix)
  ↓ /plan-ideate         (발산·정리·수렴, Top 3 선정)
아이디어
  ↓ /plan-discover       (문제·사용자·가정)
  ↓ /plan-prd            (PRD)
  ↓ /plan-stories        (유저 스토리)
  ↓ /plan-prioritize     (스코어링)
  ↓ /plan-flow           (플로우 다이어그램)
  ↓ /plan-data-model     (개념 ERD)
  ↓ /plan-risks          (Pre-mortem)
  ↓ /plan-audit          (완성도 감사)
  ↓ /plan-sync-github    (GitHub Issues 분해)
  ↓
  → /sprint-contract (harness) → 구현 → qa-evaluator
```

## 리서치 문서

`docs/planning/` 에 방법론별 리서치 문서가 있으며, 모든 스킬이 이를 SSOT 로 참조한다. 주기적으로 `/planning-research` 와 `/planning-kaizen` 으로 갱신된다.

## Phase 11 kaizen (2026-05-07)

- Phase 1 v1.3.0 신규 원칙 흡수 — `/insights` Friction #1·#2·#3 의 planning-kit 측 reframe
- 적용 매핑은 **harness/references/cross-kit-principles.md** planning-kit 열 참조
- plan-audit + plan-discover enumerate 단계 ↔ Pre-Edit Batch Audit, planning-reviewer self-check ↔ Self-Evaluator Audit, plan-prd/plan-stories sprint handoff 시점 ↔ Session Lifecycle
