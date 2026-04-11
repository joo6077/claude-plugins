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

## [2026-04-10] - kaizen Phase 1~10 + Final (전체 9 Phase 오케스트레이션)

### 변경 유형: patch (code-fence, gotchas, guides, disambiguation)

### 변경 범위
- **Phase 1** (a925a31): kaizen-orchestrator Step 0 pre-flight 데이터 수집
- **Phase 2** (0af5ecc): contract-design-guide 구체성 레벨 [L1/L2/L3] + 예외 조항 패턴 추가
- **Phase 3** (1f73810): qa-evaluator L1~L3 검증 깊이 vs 계약 구체성 레벨 용어 분리 + set intersection 키워드 배타성 절차 추가
- **Phase 4** (07c6074): harness README/create-skill/init bare code fence 7건 언어 힌트 추가
- **Phase 5** (6a43a5e): flutter-toolkit Gotchas 강화 + cross-kit disambiguation
- **Phase 6** (31808d4): design-kit bare fences 7건 수정 + Gotchas 강화
- **Phase 7**: SKIPPED (backend-kit — 이번 카이젠 범위 외)
- **Phase 8** (a45a7b7): infra-kit bare fence 수정 + references 디렉토리 생성
- **Phase 9** (ec00e20): rust-kit bare fences + todo!() false positive fix + fit-pal monorepo insights
- **Phase 10** (6ded56a): react-kit bare fence 수정 + 세션 REJECT 패턴 공통 Gotchas 문서화
- **Final** (이번): harness V5 (TODO→미완성 마커) + V6 (bare fence line 86) residue 해결

### 핵심 개선
- 전체 7 플러그인 validate-plugin: ERROR 0 (before: 1 ERROR harness), WARNING은 cross-kit 허용 케이스
- Phase 2↔3 L 기호 충돌 해소: 계약 구체성 레벨 [L1/L2/L3] vs evaluator 검증 깊이 L1~L3 용어 분리 명시
- react-kit 라이브러리 0개 원칙 회귀 없음 확인

## [0.3.5] - 2026-03-30 (evaluator-kaizen)

### 변경 유형: patch (guide, agent-prompt)

### 연구 기반
- [A Survey on LLM-as-a-Judge](https://arxiv.org/abs/2411.15594) — LLM 판정자 편향 분류 + 완화 전략 체계
- [CheckEval: Robust Evaluation Framework](https://arxiv.org/abs/2403.18771) `EMNLP 2025` — Boolean 체크리스트 분해로 평가자 간 일치도 0.45 향상
- [Understanding LLM-Driven Test Oracle Generation](https://arxiv.org/abs/2601.05542) `AIware 2025` — LLM이 구현을 정답으로 추종하는 편향 발견
- [A Statistical Approach to Model Evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals) (Anthropic) — 평가 신뢰도 측정 통계적 프레임워크

### 변경 내역
- **docs/guides/qa-evaluation-guide.md**: 편향 테이블 3개 → 6개로 확장
  - Before: 위치 편향, 장황함 편향, 자기강화 편향 (3개)
  - After: + 구체성 편향, 구현 추종 편향, 지시 해석 불일치 (6개). 각 편향별 완화 전략 명시
  - 근거: [LLM-as-a-Judge Survey](https://arxiv.org/abs/2411.15594), [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **docs/guides/qa-evaluation-guide.md**: 구현 추종 편향 경고 blockquote 추가
  - Before: 구현 추종 편향에 대한 명시적 경고 없음
  - After: LLM이 코드를 읽을 때 구현을 정답으로 추종하는 편향 경고 + 출처 URL 포함
  - 근거: [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **docs/guides/qa-evaluation-guide.md**: CheckEval 3단계 분해 프로토콜 체계화
  - Before: 단일 예시만 제공 ("로그인 실패 시 HTTP 401")
  - After: 3단계 프로토콜 (Aspect Selection → Checklist Generation → Boolean Evaluation) + 복합 조건 분해 예시 + 적용 기준
  - 근거: [CheckEval](https://arxiv.org/abs/2403.18771)
- **docs/guides/qa-evaluation-guide.md**: "판정 신뢰도 평가" 섹션 신설
  - Before: 판정 확신도에 대한 가이드라인 없음
  - After: 확신도 3단계(높음/중간/낮음) 테이블 + 규칙 + Specification-First 검증 순서 원칙
  - 근거: [Anthropic Statistical Approach](https://www.anthropic.com/research/statistical-approach-to-model-evals), [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **harness/agents/qa-evaluator.md**: Specification-First 원칙을 Step 2에 추가
  - Before: 검증 순서에 대한 명시적 지침 없음
  - After: "코드를 보기 전에 각 조건의 기대 행동을 먼저 확립한다" 원칙 명시
  - 근거: [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **harness/agents/qa-evaluator.md**: 복합 조건 분해(CheckEval) 프로토콜 참조 추가
  - Before: 복합 조건에 대한 체계적 분해 가이드 없음
  - After: CheckEval 프로토콜 4단계 요약 + qa-evaluation-guide.md 상세 참조
- **harness/agents/qa-evaluator.md**: Red Flags + Rationalization Table에 구현 추종 편향 항목 추가
  - Before: 구현 추종 편향에 대한 변명 차단 없음
  - After: "코드가 이렇게 동작하니까 맞다" 변명 차단 + Red Flag 항목 추가

### 버전 판단 근거
> 편향 테이블 확장, 분해 프로토콜 체계화, 확신도 체계 추가는 기존 판정 로직의 구조를 변경하지 않고 가이드라인을 보강한 것이므로 patch bump

---

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
