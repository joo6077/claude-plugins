# Phase 의존성 맵

## 업데이트 순서

```
Phase 1: 설계 가이드
  docs/guides/skill-design-guide.md
  docs/guides/agent-design-guide.md
      ↓ 설계 원칙이 Phase 2~3의 판단 기준
Phase 2: harness
  harness/skills/*/SKILL.md
  harness/agents/qa-evaluator.md
  .harness/project.yaml
  harness/evals/
      ↓ QA 프레임워크가 Phase 3 eval/audit 기반
Phase 3: flutter-toolkit (내부 순서 있음)
  3-a. flutter-toolkit/references/project-detection.md
  3-b. flutter-toolkit/skills/*/SKILL.md (기존)
  3-c. flutter-toolkit/skills/*/SKILL.md (신규 생성)
  3-d. flutter-toolkit/evals/evals.json
```

## Phase 간 의존성 상세

| 상위 | 하위 | 관계 |
|------|------|------|
| skill-design-guide.md | 모든 SKILL.md | Gotchas 패턴, 아키타입 분류, 트리거 조건 원칙 |
| agent-design-guide.md | qa-evaluator.md | 도구 스코핑, 모델 선택, 영속 메모리 원칙 |
| skill-design-guide.md | sprint-contract | 검증 가능한 성공 기준 원칙 (섹션 3.5) |
| project.yaml | sprint-contract | contract_categories, anti_patterns |
| qa-evaluator.md | Phase 3 QA | flutter-toolkit 변경도 같은 QA로 검증 |
| project-detection.md | flutter-toolkit 전 스킬 | $FLUTTER, ARCH, HAS_* 변수 제공 |

## Phase 스킵 시 전파 규칙

- Phase 1 스킵 → Phase 2~3는 기존 설계 가이드 기준으로 진행
- Phase 2 스킵 → Phase 3는 기존 harness 설정 기준으로 진행
- Phase 3 내부: project-detection 변경 없으면 3-a 스킵, 바로 3-b로

## QA 실패 시 롤백 범위

- Phase N QA REJECT → Phase N 변경만 수정 (이전 Phase 건드리지 않음)
- Final QA REJECT → 해당 Phase로 돌아가 수정 (다른 Phase 건드리지 않음)
