---
title: Kaizen Research Log
version: 1.0.0
last_updated: 2026-03-30
---

# Kaizen Research Log

> 매주 연구한 소스와 채택/폐기 여부를 기록한다.
> 다음 실행 시 이 로그를 참조하여 중복 연구를 방지한다.

---

<!-- 엔트리는 최신순으로 추가 -->

## 2026-03-30 (evaluator-kaizen)

**트리거:** manual (첫 실행, 리서치 전용 모드)
**피드백 분석:** 0건, 피드백 없음 — search-sources.md 우선순위 상위 3개 도메인 리서치

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
|---|------|-----|------|--------|------|
| 1 | A Survey on LLM-as-a-Judge | https://arxiv.org/abs/2411.15594 | peer-reviewed survey `[preprint]` | 높음 | 채택 |
| 2 | CheckEval: Robust Evaluation Framework using LLM via Checklist | https://arxiv.org/abs/2403.18771 | EMNLP 2025 | 높음 | 채택 |
| 3 | Understanding LLM-Driven Test Oracle Generation | https://arxiv.org/abs/2601.05542 | AIware 2025 | 높음 | 채택 |
| 4 | Rubric Is All You Need: LLM-based Code Evaluation with Question-Specific Rubrics | https://arxiv.org/abs/2503.23989 | ICER 2025 | 높음 | 채택 (참고) |
| 5 | A Statistical Approach to Model Evaluations | https://www.anthropic.com/research/statistical-approach-to-model-evals | 공식 (Anthropic) | 높음 | 채택 |
| 6 | Bloom: Automated Behavioral Evaluations | https://alignment.anthropic.com/2025/bloom-auto-evals/ | 공식 (Anthropic) | 높음 | 채택 (참고) |
| 7 | Test Oracle Automation in the Era of LLMs (ACM TOSEM) | https://dl.acm.org/doi/10.1145/3715107 | peer-reviewed | 높음 | 폐기 |

### 채택한 인사이트

- **구현 추종 편향 (Implementation-following bias):** LLM은 코드를 읽을 때 구현된 로직을 "의도된 행동"으로 추종하는 경향이 있다. qa-evaluator는 계약을 먼저 읽고 기대 행동을 확립한 뒤 코드를 검증해야 한다 (Specification-First 원칙) — 적용 영역: guide, skills
- **확장된 편향 분류:** 기존 3개(위치/장황함/자기강화)에서 6개로 확장. 구체성 편향, 구현 추종 편향, 지시 해석 불일치 추가. 각 편향별 완화 전략 명시 — 적용 영역: guide
- **CheckEval 3단계 분해 프로토콜:** Aspect Selection → Checklist Generation → Boolean Evaluation. 평가자 간 일치도 0.45 향상. 복합 조건에 대한 체계적 분해 예시 추가 — 적용 영역: guide, skills
- **판정 확신도 체계:** Anthropic 통계적 접근법 기반. 검증 레벨(L1/L2/L3)과 연동한 높음/중간/낮음 확신도 태그. 낮은 확신도 PASS는 미검증 취급 — 적용 영역: guide

### 폐기 사유

- **소스 7 (ACM TOSEM):** HTTP 403 접근 불가. GATE 2 실패로 폐기

### 개선 적용

- 대상: `docs/guides/qa-evaluation-guide.md`
- 변경: 편향 테이블 6개로 확장, 구현 추종 편향 경고 blockquote 추가, CheckEval 3단계 분해 프로토콜 + 복합 조건 예시, 판정 신뢰도 평가 섹션 신설 (확신도 테이블 + Specification-First 원칙)
- 대상: `harness/agents/qa-evaluator.md`
- 변경: Specification-First 원칙 Step 2에 추가, 복합 조건 분해(CheckEval) 프로토콜 참조 추가, Red Flags에 구현 추종 편향 항목 추가, Rationalization Table에 구현 추종 변명 차단 추가
- 버전: v0.3.4 → v0.3.5

### PR

- 커밋으로 직접 적용 (첫 실행, 리서치 전용 모드)

---

## 2026-03-30 (contract-kaizen)

**트리거:** manual (첫 실행, 리서치 전용 모드)
**피드백 분석:** 0건, 피드백 없음 — search-sources.md 우선순위 상위 3개 도메인 리서치

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
|---|------|-----|------|--------|------|
| 1 | Spec-driven development (Thoughtworks) | https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices | blog `[blog]` | 중간 | 채택 |
| 2 | Automated Repair of Ambiguous Problem Descriptions (SpecFix) | https://arxiv.org/abs/2505.07270 | preprint `[preprint]` | 높음 | 채택 |
| 3 | Evaluation-Driven Development of LLM Agents (EDDOps) | https://arxiv.org/abs/2411.13768 | preprint `[preprint]` `[dated: 2024-11]` | 높음 | 채택 (참고) |
| 4 | ATDD for Claude Code (swingerman/atdd) | https://github.com/swingerman/atdd | community `[community]` | 중간 | 채택 |
| 5 | Given-When-Then Acceptance Criteria Guide | https://www.parallelhq.com/blog/given-when-then-acceptance-criteria | blog `[blog]` | 중간 | 채택 |

### 채택한 인사이트

- **구현 누수 방지 (External Observables Only):** 조건에 클래스명/메서드명/DB명 등 구현 상세를 쓰면 구현 변경 시 조건이 깨진다. ATDD 프레임워크(swingerman/atdd)에서 "Golden Rule"로 강조 — 적용 영역: guide, skills
- **반구조화 조건의 할루시네이션 감소:** Thoughtworks SDD 리서치에서 semi-structured specs가 LLM 추론 정확도를 높이고 할루시네이션을 줄인다고 확인. 복잡도 중간 이상에서 GWT 필수화 — 적용 영역: guide, skills
- **모호성 분류 체계 (Ambiguity Taxonomy):** SpecFix 논문에서 문제 기술의 43.58%에 수정 가능한 모호성 존재 확인. 어휘적/구문적/의미적 3단계 분류로 체계적 점검 — 적용 영역: guide
- **비기능 요구사항 커버리지:** BDD 리서치에서 NFR(성능/보안/접근성) 누락이 일반적 안티패턴으로 지적 — 적용 영역: guide, skills

### 폐기 사유

- 없음 (첫 실행이므로 모든 채택 소스가 신규)

### 개선 적용

- 대상: `docs/guides/contract-design-guide.md`
- 변경: 외부 관찰 가능성 섹션 추가, 안티패턴 2개 추가 (구현 누수, NFR 누락), 모호성 분류 체계 추가, 진단 체크리스트 2개 항목 추가, GWT 적용 기준 명확화
- 대상: `harness/skills/sprint-contract/SKILL.md`
- 변경: Gotchas 3개 추가 (구현 누수, GWT 필수화, NFR), 자기진단 체크리스트 2개 항목 추가 (implementation_leakage, nfr_coverage)
- 버전: v0.3.3 → v0.3.4

### PR

- 커밋으로 직접 적용 (첫 실행, QA 충돌 없음)

---

## 2026-03-30

**트리거:** manual (전체)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
|---|------|-----|------|--------|------|
| 1 | Survey on Evaluation of LLM-based Agents | https://arxiv.org/abs/2503.16416 | peer-reviewed `[preprint]` | 높음 | 채택 (참고) |
| 2 | Beyond Task Completion: Assessment Framework for Agentic AI | https://arxiv.org/abs/2512.12791 | peer-reviewed `[preprint]` | 높음 | 채택 (참고) |
| 3 | Agentic AI Coding: Best Practice Patterns for Speed with Quality | https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality | blog | 중간 | 채택 |
| 4 | agentic-code: Quality Gates Framework | https://github.com/shinpr/agentic-code | community | 중간 | 채택 |
| 5 | Best Practices for Claude Code | https://code.claude.com/docs/en/best-practices | 공식 | 높음 | 채택 |
| 6 | Evaluation and Benchmarking of LLM Agents: A Survey | https://arxiv.org/abs/2507.21504 | peer-reviewed `[preprint]` | 높음 | 폐기 |

### 채택한 인사이트

- **검증 가능한 성공 기준:** Claude Code 공식 best practices에서 "Give Claude a way to verify its work"가 단일 최고 레버리지 행동으로 제시됨 — 적용 영역: guide
- **Multi-Level Code Safeguards:** CodeScene이 3단계 검증(생성 중 → pre-commit → PR)을 권장. 단일 시점 검증보다 효과적 — 적용 영역: skill (sprint-contract)
- **Isolated Review:** agentic-code 프레임워크에서 "LLMs cannot reliably review their own outputs within the same context" 확인. Generator의 self-review를 독립 검증으로 취급하면 안 됨 — 적용 영역: agent (qa-evaluator)

### 폐기 사유

- **소스 6 (arxiv:2507.21504):** 2025년 7월 발행이나 내용이 소스 1과 대부분 중복. 추가 인사이트 없음

### PR

- (이 세션에서 PR 생성 예정)
