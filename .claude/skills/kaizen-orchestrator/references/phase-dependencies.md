# Phase 의존성 맵

## 업데이트 순서

```
Phase 1: 설계 가이드 카이젠
  harness/docs/guides/skill-design-guide.md
  harness/docs/guides/agent-design-guide.md
      ↓ 설계 원칙이 Phase 2~9의 판단 기준
Phase 2: Contract 카이젠 (contract-kaizen)
  harness/docs/guides/contract-design-guide.md
  harness/skills/sprint-contract/SKILL.md
      ↓ 계약 작성 원칙이 Phase 3 evaluator 기준
Phase 3: Evaluator 카이젠 (evaluator-kaizen)
  harness/docs/guides/qa-evaluation-guide.md
  harness/agents/qa-evaluator.md
      ↓ QA 평가 기준이 Phase 4~9 검증 기반
Phase 4: Harness 카이젠 (harness-kaizen)
  harness/skills/*/SKILL.md (sprint-contract, evaluator-kaizen 제외)
  harness/agents/ (qa-evaluator 제외)
  .harness/project.yaml
      ↓ Harness 인프라가 Phase 5~9 실행 환경
Phase 5: Flutter-toolkit 카이젠 (flutter-kaizen)
  flutter-toolkit/references/project-detection.md
  flutter-toolkit/skills/*/SKILL.md
  flutter-toolkit/evals/evals.json
      ↓ Flutter 스킬 완료 후 Design-kit으로
Phase 6: Design-kit 카이젠 (design-kaizen)
  design-kit/skills/*/SKILL.md
  design-kit/references/
      ↓ UI/UX 원칙 완료 후 Backend-kit으로
Phase 7: Backend-kit 카이젠 (backend-kaizen)
  backend-kit/skills/*/SKILL.md
  backend-kit/references/
  docs/backend/ (리서치 문서)
      ↓ 백엔드 아키텍처 완료 후 Infra-kit으로
Phase 8: Infra-kit 카이젠 (infra-kaizen)
  infra-kit/skills/*/SKILL.md
  infra-kit/references/
  docs/infra/ (리서치 문서)
      ↓ 인프라/DevOps 완료 후 Rust-kit으로
Phase 9: Rust-kit 카이젠 (rust-kaizen)
  rust-kit/skills/*/SKILL.md
  rust-kit/references/
  docs/rust/ (리서치 문서)
      ↓ Rust 백엔드 완료 후 React-kit으로
Phase 10: React-kit 카이젠 (react-kaizen)
  react-kit/skills/*/SKILL.md
  react-kit/agents/*.md
  react-kit/references/
  docs/react/ (리서치 문서)
```

## Phase 간 의존성 상세

| 상위 | 하위 | 관계 |
|------|------|------|
| skill-design-guide.md | 모든 SKILL.md | Gotchas 패턴, 아키타입 분류, 트리거 조건 원칙 |
| agent-design-guide.md | qa-evaluator.md | 도구 스코핑, 모델 선택, 영속 메모리 원칙 |
| contract-design-guide.md | sprint-contract SKILL.md | 계약 작성 원칙, 카테고리 설계, 이진 판정 기준 |
| qa-evaluation-guide.md | qa-evaluator.md | 편향 분류, CheckEval 프로토콜, 확신도 체계 |
| contract-schema.md | sprint-contract, qa-evaluator | 계약 포맷 스키마 공유 |
| project.yaml | sprint-contract | contract_categories, anti_patterns |
| qa-evaluator.md | Phase 4~9 QA | 모든 Phase 변경이 같은 QA로 검증됨 |
| project-detection.md | flutter-toolkit 전 스킬 | $FLUTTER, ARCH, HAS_* 변수 제공 |
| docs/backend/ | backend-kit 전 스킬 | 백엔드 리서치 원칙 (프레임워크/패턴/보안) |
| docs/infra/ | infra-kit 전 스킬 | 인프라/DevOps 리서치 원칙 (IaC/CI/관측성) |
| docs/rust/ | rust-kit 전 스킬 | Rust 백엔드 리서치 원칙 (Axum/SQLx/tonic) |
| docs/react/ | react-kit 전 스킬 | React + Vite + Tauri + WASM 리서치 원칙 (21 스킬 + 3 에이전트) |

## Phase 스킵 시 전파 규칙

- Phase 1 스킵 → Phase 2~9는 기존 설계 가이드 기준으로 진행
- Phase 2 스킵 → Phase 3는 기존 contract-schema 기준으로 진행
- Phase 3 스킵 → Phase 4~9는 기존 evaluator 기준으로 진행
- Phase 4 스킵 → Phase 5~9는 기존 harness 설정 기준으로 진행
- Phase 5 내부: project-detection 변경 없으면 바로 기존 스킬로
- Phase 6 스킵 → Phase 7~9 진행에 영향 없음 (독립 스택)
- Phase 7 스킵 → Phase 8~9 진행에 영향 없음 (독립 스택)
- Phase 8 스킵 → Phase 9 진행에 영향 없음 (독립 스택)
- Phase 9 스킵 → Phase 10 진행에 영향 없음 (독립 스택)
- Phase 7/8/9/10 중 어느 하나라도 피드백 0건이면 SKIP하지 않고 **리서치 전용 모드**로 진행 (docs/{backend|infra|rust|react}/ 기준 점진 개선)

## QA 실패 시 롤백 범위

- Phase N QA REJECT → Phase N 변경만 수정 (이전 Phase 건드리지 않음)
- Final QA REJECT → 해당 Phase로 돌아가 수정 (다른 Phase 건드리지 않음)
- 2+ 연속 실패 → .harness/.meta/kaizen-failure-count.yaml에 기록, 해당 Phase 일시 중지 (Phase 7/8/9도 동일 규칙 적용)
