# Sprint Contract — Phase 3 Kaizen Research Mode (Evaluator)

Feature: qa-evaluation-guide / qa-evaluator 2026 LLM-as-judge 최신 리서치 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1 (commit 4587154, e7b2a10, 5061714) 은 skill/agent design guide 를 v1.1.0 으로 갱신하면서 L1/L2/L3 을 QA 평가 깊이 전용으로 예약했다. Phase 2 (commit ba2b8d9, ea0ac3c) 는 contract-schema 를 v2 로 bump 하고 `[exact]`/`[structural]`/`[goal]` 태그 + `enumerated`/`collective` aggregation mode 를 신규 도입했다.

현재 evaluator 쪽 (qa-evaluation-guide.md, qa-evaluator.md) 은 Phase 3 이전 commit 1f73810 에서 용어 분리 1차 반영을 했으나, 아래 2026 최신 리서치 반영이 누락되어 있다:

1. **Position bias swap test 부재** — 2026 최신 연구 (arxiv 2406.07791 IJCNLP 2025, 2602.02219) 가 pairwise swap (A,B → B,A) 을 표준 완화 기법으로 확립했으나 가이드에 실행 절차 없음
2. **Self-preference bias (perplexity 기반)** 구체 완화 전략 부재 — arxiv 2410.21819 인용 없음
3. **Rubric Decomposition 연구 업데이트 부족** — arxiv 2602.05125 Recursive Rubric Decomposition (RRD) 미반영. 현재 CheckEval 만 참조
4. **Chain-of-Thought 무용성 연구 (arxiv 2506.13639)** — Phase 2 contract-design-guide 는 인용했으나 evaluator 쪽은 "rubric 이 잘 정의되어 있으면 CoT 효과 미미" 명시 부재
5. **Scoring Bias / Justice or Prejudice 편향 survey (arxiv 2506.22316, 2410.02736)** 미인용
6. **Human-in-the-loop rubric refinement (arxiv 2511.10865)** — 교차 진단 프로토콜과 호환되는 최신 패턴 미반영
7. **Aggregation mode 인지 부재** — Phase 2 에서 `[enumerated]`/`[collective]` 태그를 도입했으나 qa-evaluator 가 이 태그를 어떻게 소비하는지 가이드 없음. KZ-04 재발 리스크
8. **Specificity tag 소비 규칙 부재** — `[exact]` / `[structural]` / `[goal]` 태그별 검증 방식 차이 명시 부재. `[goal]` 태그는 L3 의미 추적을 더 적극적으로 요구해야 하나 가이드 없음
9. **L3 커버리지 경계선 사례 누락** — design-tokens.md / audit-report.md 외 "Markdown 전수 검사" 계열 (CD-02, DG-02) 에 대한 L3 도달 절차 부재

## 리서치 소스 (URL 필수)

1. [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge — arxiv 2406.07791](https://arxiv.org/abs/2406.07791) (IJCNLP 2025) — swap test 권고
2. [Am I More Pointwise or Pairwise? Revealing Position Bias in Rubric-Based LLM-as-a-Judge — arxiv 2602.02219](https://arxiv.org/html/2602.02219) — rubric 기반 판정에서도 position bias 발생
3. [Self-Preference Bias in LLM-as-a-Judge — arxiv 2410.21819](https://arxiv.org/abs/2410.21819) — perplexity 기반 familiarity, generator-evaluator 컨텍스트 분리 근거
4. [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge — arxiv 2410.02736](https://arxiv.org/html/2410.02736v1) — 12 개 편향 분류
5. [Evaluating Scoring Bias in LLM-as-a-Judge — arxiv 2506.22316](https://arxiv.org/html/2506.22316v1) — scoring bias 측정
6. [An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability — arxiv 2506.13639](https://arxiv.org/html/2506.13639v1) — CoT minimal gain when rubric well-defined
7. [Rethinking Rubric Generation for Improving LLM Judge and Reward Modeling — arxiv 2602.05125](https://arxiv.org/html/2602.05125v1/) — Recursive Rubric Decomposition (RRD)
8. [A Survey on LLM-as-a-Judge — arxiv 2411.15594](https://arxiv.org/html/2411.15594v6) — 종합 bias 분류
9. [Towards a Human-in-the-Loop Framework for Reliable Patch Evaluation Using an LLM-as-a-Judge — arxiv 2511.10865](https://arxiv.org/abs/2511.10865) — one-time rubric refinement 패턴
10. [CodeBERTScore — arxiv 2302.05527](https://arxiv.org/abs/2302.05527) — 참고용 (계약 기반 검증이 우선이므로 본 가이드는 채택하지 않고 "왜 채택하지 않는가" 근거로 사용)

## 완료 조건 (Sprint Contract)

### QG (qa-evaluation-guide.md)

- [ ] QG-01 [exact]: 문서 상단 frontmatter blockquote 에 `> 최근 갱신: 2026-04-11 (Phase 3 kaizen research)` 노트 1 줄 추가
- [ ] QG-02 [structural]: "LLM-as-a-Judge 편향 완화" 표에 **Position bias** 행의 완화 전략을 `조건 순서를 무작위로 평가` 에서 `Swap Test: (A,B) 와 (B,A) 순서로 2 회 평가하고 결과가 일치할 때만 판정 확정 (arxiv 2406.07791)` 형태로 구체화. arxiv URL 1 건 문서 하단 참조 섹션에 추가
- [ ] QG-03 [structural]: 편향 표에 **Self-preference bias** 행의 완화 전략을 `perplexity 기반 familiarity 경고 + generator-evaluator 컨텍스트 분리 의무화 (arxiv 2410.21819)` 로 구체화. URL 참조 섹션에 추가
- [ ] QG-04 [structural]: 편향 표에 **Scoring bias** (점수 분포 왜곡) 행 1 개 신규 추가 — arxiv 2506.22316 인용
- [ ] QG-05 [structural]: "Rubric 기반 분해 (CheckEval 프로토콜)" 섹션에 **Recursive Rubric Decomposition (RRD)** 개념 단락 1 개 신규 추가 — 고수준 루브릭 항목을 더 세밀한 서브포인트로 재귀 분해, arxiv 2602.05125 URL 인용
- [ ] QG-06 [structural]: "Chain-of-Thought 효용 한계" 노트 1 개 신규 추가 — 루브릭이 잘 정의되어 있으면 CoT 이득 미미 (arxiv 2506.13639), 따라서 장황한 reasoning 보다 boolean 서브체크 + 증거(파일:라인) 에 집중하라는 지침
- [ ] QG-07 [structural]: "Specificity Tag 소비 규칙" 서브섹션 신규 추가 — 계약 태그별 검증 방식 명시 테이블 (`[exact]` → 문자 그대로 grep + literal 매칭, `[structural]` → 파일/섹션 존재 + Read 로 구조 확인, `[goal]` → L3 의미 추적 필수 + 다관점 평가 강화). 모든 태그는 evaluator 검증 깊이 L3 까지 도달해야 한다는 원칙 재확인
- [ ] QG-08 [structural]: "Aggregation Mode 소비 규칙" 서브섹션 신규 추가 — `[enumerated]` 태그 조건은 각 대상을 개별 Grep + 개별 증거 수집, `[collective]` 태그 조건은 포괄 경로/패턴 1 건 증거로 충분. KZ-04 실패 사례 1 줄 언급
- [ ] QG-09 [structural]: "L3 검증 심층화 절차" 섹션에 Markdown 전수 검사 조건 (CD-02, DG-02 계열) 에 대한 절차 1 개 추가 — Glob 으로 파일 목록 수집 → 각 파일 Read → 조건 요소 누락 0 건 확인 → FAIL 파일명:라인 나열. 기존 design-tokens.md 예시는 유지
- [ ] QG-10 [structural]: "Human-in-the-loop 교차 진단 개선" 노트 추가 — arxiv 2511.10865 의 one-time rubric refinement 패턴을 기존 교차 진단 프로토콜과 연결. 계약 모호성 발견 시 evaluator 가 계약 수정 권장을 피드백에 명시하되, 실제 수정은 사용자 권한임을 재확인
- [ ] QG-11 [exact]: 판정 신뢰도 평가 섹션에 "Swap Test 불안정 → 판정 확신도 `[low-confidence]` 강등" 규칙 1 줄 추가
- [ ] QG-12 [exact]: 문서 내 bare code fence (` ``` ` 뒤 바로 개행, 언어 힌트 없음) 0 건 — DG-02 anti 준수
- [ ] QG-13 [exact]: 문서 내 `[L1]` / `[L2]` / `[L3]` 대괄호 문자열이 계약 태그 의미로 사용되지 않음 — evaluator 검증 깊이 용례만 허용. 기존 "용어 구분" 섹션의 계약 태그 참조 표에 있는 `[L1]` / `[L2]` / `[L3]` 는 네이밍 충돌 경고 맥락이므로 PASS (기존 문맥 유지)
- [ ] QG-14 [exact]: 문서 하단에 `## References` 또는 유사 섹션이 존재하고, 본 Phase 에서 추가한 arxiv URL 최소 5 건이 그 안에 나열됨

### QA (qa-evaluator.md)

- [ ] QA-01 [structural]: "판정 엄격도" 섹션 아래에 **Specificity Tag 소비 규칙** 항목 신규 추가 — `[exact]`/`[structural]`/`[goal]` 태그를 만났을 때 검증 방식이 어떻게 달라지는지 3~5 줄 요약. 모든 태그는 검증 깊이 L3 까지 도달한다는 원칙 재확인
- [ ] QA-02 [structural]: "판정 엄격도" 섹션 아래에 **Aggregation Mode 소비 규칙** 항목 신규 추가 — `[enumerated]` → 개별 대상 증거 N 건 필수, `[collective]` → 포괄 경로 1 건 증거로 충분
- [ ] QA-03 [structural]: Red Flags 섹션에 **Swap Test 불안정** 또는 **CoT 장황성으로 증거 희석** 항목 1 개 신규 추가 — 장황한 reasoning 보다 증거(파일:라인) 우선
- [ ] QA-04 [structural]: Rationalization Table 에 `"판정이 swap 으로 바뀌었다"` 또는 `"rubric 해석이 방향마다 달랐다"` 행 1 개 신규 추가 — 현실 컬럼: position bias 의심, `[low-confidence]` 태그 + 재검증 지시
- [ ] QA-05 [exact]: References 섹션에 `qa-evaluation-guide.md` 링크 유지 (기존)
- [ ] QA-06 [exact]: 문서 내 bare code fence 0 건
- [ ] QA-07 [exact]: Phase 1 `[L1]`/`[L2]`/`[L3]` 기호 충돌 주의 blockquote (commit 1f73810 에서 추가) 유지 — 제거·이동 금지
- [ ] QA-08 [structural]: Process 의 Step 2 에 "Specificity tag 식별 후 검증 방식 결정" 단계 1 줄 추가 — Sprint Contract 로드 직후 각 조건 끝의 태그를 먼저 파싱하라는 절차 명시

### I (Integration / Hygiene)

- [ ] I-01 [exact]: `python3 scripts/validate-plugin.py` Total 7 plugins, 7 OK, Exit 0
- [ ] I-02 [exact]: Working tree modified 예외 3 항목 외 없음 — 예외: `.harness/sprint-contract.md`, `harness/docs/guides/qa-evaluation-guide.md`, `harness/agents/qa-evaluator.md`
- [ ] I-03 [exact]: git commit 1 건 (`kaizen(phase3-research): ...`) 생성. commit message body 에 리서치 소스 URL 3 건 이상 인용
- [ ] I-04 [exact]: Phase 1 변경 (skill-design-guide.md, agent-design-guide.md) 파일을 수정하지 않음
- [ ] I-05 [exact]: Phase 2 변경 (contract-design-guide.md, sprint-contract/SKILL.md, contract-schema.md) 파일을 수정하지 않음

## 검증 절차

1. Edit 로 2 개 파일 수정 (qa-evaluation-guide.md, qa-evaluator.md)
2. Grep bare code fence 전수 확인 (0 건)
3. Grep `\[L[123]\]` 문자열 전수 확인 — 기존 용어 구분/기호 충돌 맥락만 유지
4. `python3 scripts/validate-plugin.py` 7 OK 확인
5. git add + commit
6. self-audit (Phase 3 서브에이전트는 서브에이전트 스폰 불가 — 최종 QA 는 오케스트레이터에 위임)

## Anti-patterns (절대 하지 마라)

- Phase 1 / Phase 2 변경 파일 수정 (I-04, I-05)
- Swap Test 를 "2 번 읽는다" 수준의 모호한 표현으로 추가 (구체적 (A,B) / (B,A) 매핑 없으면 FAIL)
- arxiv URL 없이 "2026 최신 연구" 같은 추측성 주장 추가
- 기존 CheckEval 서브섹션 제거 — RRD 는 병기로 추가
- L1/L2/L3 기호 충돌 주의 blockquote 제거 또는 이동
- 스프린트 범위 밖 파일 수정
