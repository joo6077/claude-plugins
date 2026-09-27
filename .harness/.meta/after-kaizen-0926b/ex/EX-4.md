# EX-4 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- LLM 평가자의 편향을 몇 가지로 분류하는가 — 각 논문에서 편향 종류 수와 그 문장 원문
- 「12 개 이상의 편향」 이라는 표현이 어느 논문의 어느 문장에 근거할 수 있는가, 없다면 실제 수

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase3.md 154행
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/harness/docs/guides/qa-evaluation-guide.md 143행

원문: https://arxiv.org/html/2411.15594v6 , https://arxiv.org/html/2410.02736v1

## 답

## 1. 출처 목록

모두 2026-09-26에 가져왔다.

- 저장소 근거: [phase3.md:154](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase3.md:154)
- 저장소 주장: [qa-evaluation-guide.md:143](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/harness/docs/guides/qa-evaluation-guide.md:143)
- 원문: [A Survey on LLM-as-a-Judge, arXiv:2411.15594v6](https://arxiv.org/html/2411.15594v6)
- 원문: [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge, arXiv:2410.02736v1](https://arxiv.org/html/2410.02736v1)

## 2. 질문별 확인

### A. 각 논문은 편향을 몇 가지로 분류하는가?

#### ① A Survey on LLM-as-a-Judge

원문은 편향을 명시적으로 **2개의 상위 클래스**로 분류한다.

> “broadly categorized into two classes: task-agnostic biases ... and judgment-specific biases”

출처: [원문 §4.2 Bias](https://arxiv.org/html/2411.15594v6), 가져온 날짜 2026-09-26.

두 클래스 아래 본문에서 이름을 붙여 설명하는 대표 편향은 다음 8개다.

- Task-agnostic: Diversity, Cultural, Self-Enhancement
- Judgment-specific: Position, Compassion-fade, Style, Length, Concreteness

추론: 이를 세면 **대표 항목 8개**지만, 논문은 “a few typical examples”라고 표현한다. 따라서 “총 8종으로 완결 분류했다”고 단정하면 안 된다. Sentiment는 Style의 사례이고, authority/citation은 Concreteness의 다른 명칭 또는 양상으로 서술된다.

이 논문은 별도로 CALM, 즉 둘째 논문을 소개하면서 다음과 같이 말한다.

> “examining 12 distinct types of potential biases in LLM evaluators”

출처: [원문 §4.1–4.2 경계 부분](https://arxiv.org/html/2411.15594v6), 가져온 날짜 2026-09-26.

**판정:** Survey 자체 분류는 **2개 상위 클래스**다. 대표 세부 항목은 **8개로 셀 수 있지만 이는 추론**이며, 본문이 총수를 8개라고 선언하지는 않는다. Survey에 나오는 “12”는 자체 분류 수가 아니라 **CALM의 분류를 소개한 수치**다.

#### ② Justice or Prejudice?

원문은 정확히 **12개 편향 유형**이라고 명시한다.

> “Figure 4 illustrates the influence of 12 distinct biases on the judging capabilities of six LLMs.”

출처: [원문 §4.1 Main Result](https://arxiv.org/html/2410.02736v1), 가져온 날짜 2026-09-26.

Table 1과 Table 2에 제시된 12개는 다음과 같다.

1. Position
2. Verbosity
3. Compassion-Fade
4. Bandwagon
5. Distraction
6. Fallacy-Oversight
7. Authority
8. Sentiment
9. Diversity
10. Chain-of-Thought
11. Self-Enhancement
12. Refinement-Aware

**판정:** **맞음 — 정확히 12개**다. “12개 초과”가 아니다.

### B. “12개 이상의 편향”은 어느 문장에 근거하는가?

직접 근거는 **Justice or Prejudice?**의 “12 distinct biases” 문장이다. Survey 역시 CALM을 소개하면서 “12 distinct types”라고 반복하지만, Survey 자신의 분류 수를 뜻하지는 않는다.

추론: 한국어의 “12개 이상”은 12개를 포함하므로 수학적으로는 틀리지 않다. 그러나 원문의 정확한 표현은 **“정확히 12개 유형”**이며, “12개 이상”은 불필요하게 범위를 넓힌 표현이다.

#### 저장소 주장 판정

- [phase3.md:154](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase3.md:154): Survey 본문에서 정확한 숫자를 확인하지 못했다고 적었다.
  - **판정: 틀림.**
  - 현재 v6 본문에는 CALM이 “12 distinct types”를 다룬다는 문장이 있다.
  - 다만 “Survey 자체의 총 분류 수가 12가 아니다”라는 문제의식은 맞다.

- [qa-evaluation-guide.md:143](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/harness/docs/guides/qa-evaluation-guide.md:143): 두 논문 “에서 12개 이상의 편향을 분류”한다고 적었다.
  - **판정: 틀림.**
  - 둘째 논문은 정확히 12개를 분류한다.
  - 첫째 논문의 자체 taxonomy는 2개 상위 클래스이며 대표 세부 항목 8개를 서술한다. 첫째 논문에 등장하는 12라는 수치는 둘째 논문 CALM을 소개한 것이다.
  - 추론: 두 인용 중 하나만 수치 근거로 충분하다는 느슨한 의미라면 최소 12개라는 말은 성립하지만, 현재 문장은 두 논문 모두가 12개 이상을 분류한 것처럼 읽혀 부정확하다.

## 3. 저장소 반영 문장 제안

- `phase3.md`: “현재 Survey v6는 CALM이 12개 편향 유형을 다룬다고 명시하지만, Survey 자체 taxonomy는 2개 상위 클래스이며 8개 대표 항목을 서술할 뿐 세부 유형 총수를 선언하지 않는다.”
- `qa-evaluation-guide.md`: “Survey는 편향을 2개 상위 클래스(task-agnostic, judgment-specific)로 구분하고, Justice or Prejudice?는 정확히 12개 편향 유형을 정의한다. 본 가이드는 그중 계약 기반 검증에 영향이 큰 6개에 집중한다.”

## 4. 못 가져온 것 / 열린 질문

- 못 가져온 원문은 없다. 두 arXiv HTML 페이지가 정상적으로 열려 `curl` 재시도는 필요하지 않았다.
- 열린 질문: Survey의 대표 항목을 “8종”이라고 부를지는 편집 기준의 문제다. 논문 자체가 이를 완결된 총수라고 선언하지 않으므로, 저장소에는 “8개 대표 항목을 서술”이라고 쓰는 편이 안전하다.