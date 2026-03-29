# Kaizen Research Log

> 매주 연구한 소스와 채택/폐기 여부를 기록한다.
> 다음 실행 시 이 로그를 참조하여 중복 연구를 방지한다.

---

<!-- 엔트리는 최신순으로 추가 -->

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
