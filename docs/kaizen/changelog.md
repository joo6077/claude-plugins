---
title: Kaizen Changelog
version: 1.0.0
last_updated: 2026-03-30
---

# Kaizen Changelog

> harness-kaizen 스킬이 적용한 모든 변경의 이력.
> 각 엔트리는 버전, 변경 유형, 연구 근거, Before/After를 포함한다.

---

<!-- 엔트리는 최신순으로 추가 -->

## [0.3.4] - 2026-03-30 (contract-kaizen)

### 변경 유형: patch (guide, skill-prompt)

### 연구 기반
- [Spec-driven development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) `[blog]` — semi-structured specs가 LLM 할루시네이션 감소
- [SpecFix: Automated Repair of Ambiguous Problem Descriptions](https://arxiv.org/abs/2505.07270) `[preprint]` — 문제 기술의 43.58%에 수정 가능한 모호성 존재
- [ATDD for Claude Code](https://github.com/swingerman/atdd) `[community]` — External Observables Only 원칙 (구현 누수 방지)
- [Given-When-Then Acceptance Criteria Guide](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria) `[blog]` — NFR 누락이 일반적 안티패턴

### 변경 내역
- **docs/guides/contract-design-guide.md**: "외부 관찰 가능성" 섹션 신규 추가
  - Before: 조건에 구현 상세 포함 여부를 점검하는 가이드라인 없음
  - After: 금지 요소 목록(클래스명/메서드명/DB명/프레임워크 용어) + 좋은 예/나쁜 예 제시
  - 근거: [ATDD for Claude Code](https://github.com/swingerman/atdd)
- **docs/guides/contract-design-guide.md**: GWT 적용 기준 명확화
  - Before: "모든 조건에 강제는 아니지만" (선택 사항)
  - After: 복잡도 중간 이상 필수, 단순은 권장. 반구조화 조건이 할루시네이션 감소
  - 근거: [Thoughtworks SDD](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- **docs/guides/contract-design-guide.md**: 모호성 분류 체계 추가
  - Before: "ambiguous_conditions" 체크만 존재, 구체적 분류 없음
  - After: 어휘적/구문적/의미적 3단계 모호성 분류 + 예시 + 수정 방법
  - 근거: [SpecFix](https://arxiv.org/abs/2505.07270)
- **docs/guides/contract-design-guide.md**: 안티패턴 테이블에 2개 추가 (구현 누수, NFR 누락)
- **docs/guides/contract-design-guide.md**: 진단 체크리스트에 2개 추가 (implementation_leakage, nfr_coverage)
- **harness/skills/sprint-contract/SKILL.md**: Gotchas 3개 추가 (구현 누수, GWT 필수화, NFR)
- **harness/skills/sprint-contract/SKILL.md**: 자기진단 체크리스트에 2개 항목 추가

### 버전 판단 근거
> Gotchas 추가와 설계 가이드 보완은 기존 동작을 변경하지 않으므로 patch bump

---

## [0.3.3] - 2026-03-30

### 변경 유형: patch (guide, skill-prompt, agent-logic)

### 연구 기반
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — "Give Claude a way to verify its work"가 단일 최고 레버리지 행동
- [Agentic AI Coding: Best Practice Patterns](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality) — Multi-Level Code Safeguards (3단계 검증)
- [agentic-code](https://github.com/shinpr/agentic-code) — "LLMs cannot reliably review their own outputs within the same context"

### 변경 내역
- **docs/guides/skill-design-guide.md**: Section 3.5 "검증 가능한 성공 기준을 제공하라" 추가
  - Before: 검증 관련 원칙 없음
  - After: 스킬별 검증 기준 예시 테이블 + 자가 검증 흐름 추가
  - 근거: [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- **harness/skills/sprint-contract/SKILL.md**: Gotchas에 다단계 검증 시점 항목 추가
  - Before: 검증 시점 관련 Gotcha 없음
  - After: "가능하면 다단계 검증 시점을 조건에 반영해라" Gotcha 추가
  - 근거: [CodeScene](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality)
- **harness/agents/qa-evaluator.md**: Rationalization Table에 self-review 편향 경고 추가
  - Before: Generator self-review 관련 변명 차단 없음
  - After: "Generator가 자가 검증했으니 PASS" 변명 차단 항목 추가
  - 근거: [agentic-code](https://github.com/shinpr/agentic-code)

### 버전 판단 근거
> Gotchas 추가와 설계 가이드 보완은 기존 동작을 변경하지 않으므로 patch bump
