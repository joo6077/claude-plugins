# planning-kit

스택 무관 제품 기획 플러그인. 아이디어를 Sprint Contract 로 넘어갈 수 있는 수준의 기획 산출물로 변환한다.

## 개요

planning-kit 은 harness 파이프라인의 **0번 단계**다. "기획 → 계약 → 구현 → QA" 흐름에서 sprint-contract 보다 앞에 위치하며, 문제 정의·PRD·우선순위·리스크·개념 데이터 모델·GitHub 동기화까지 한 벌로 다룬다.

다른 kit(backend-kit, rust-kit 등) 이 "구현 단계의 스키마"를 만든다면, planning-kit 은 "개념 단계의 도메인 모델"을 만든다. Mermaid erDiagram / flowchart / sequenceDiagram 으로 시각화한다.

## 스킬

<!-- AUTO:skills:start -->
| 스킬 | 용도 |
|------|------|
| `/plan-discover` | 소크라테스식 질문으로 문제·사용자·가정·성공기준을 드러낸다 (JTBD + 5 Whys + Riskiest Assumption) |
| `/plan-prd` | Amazon PR/FAQ 또는 Shape Up Pitch 포맷으로 PRD 작성 |
| `/plan-stories` | 유저 스토리 + INVEST 검증 + Acceptance Criteria(Gherkin) |
| `/plan-prioritize` | RICE / Kano / WSJF / MoSCoW 중 컨텍스트에 맞는 프레임워크 선택 후 스코어링 |
| `/plan-flow` | 유저 플로우 / 서비스 블루프린트 (Mermaid flowchart, sequenceDiagram, stateDiagram) |
| `/plan-data-model` | 개념 ERD + 도메인 이벤트 + 데이터 사전 (Mermaid erDiagram/classDiagram) |
| `/plan-risks` | Pre-mortem + Inversion + 인지 편향 체크리스트 |
| `/plan-sync-github` | PRD/스토리를 GitHub Issues · Milestones · Projects v2 에 동기화 |
| `/plan-guide` | 기획 문서/아이디어에 대한 가벼운 원칙 기반 피드백 |
| `/plan-audit` | 완성된 기획의 완성도 감사 — sprint-contract 로 넘어갈 수 있는지 판정 |
<!-- AUTO:skills:end -->

## 에이전트

<!-- AUTO:agents:start -->
| 에이전트 | 용도 |
|---------|------|
| `planning-reviewer` | plan-audit 에서 호출. 기획 산출물을 독립 평가하여 카테고리별 PASS/FAIL 판정 |
<!-- AUTO:agents:end -->

## harness 연계

```text
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
