---
phase: 3
title: Phase 3 Evaluator — 확보된 외부 근거 + 실측 결함
collected: 2026-08-13
method: codex (foreground 회수)
note: 이 파일이 Phase 3 의 유일한 외부 근거다. 추가 외부 조회 금지. 여기 없는 URL·수치를 지어내지 마라.
---

## 1. 실측 결함 (데이터풀 §1, 2026-08-11~12)

### Q1. `[미검증]` 임계 규칙이 정당한 도구 부재를 오처벌 — 4건 연속

- "미검증 2건(UI-01, DG-02) — **둘 다 도구부재(런타임 캡처 MCP 미가용, IDE 진단 미가용)로 정당하나**
  임계 2건 이상이라 자동 REJECT 규칙 적용"
- "미검증 2건(DG-02 IDE lint 도구부재, DG-04 시뮬레이터 미부팅) — 2건 이상 자동 REJECT 규칙"
- "Unverifiable count = 2 (DG-02, DG-04) triggers automatic REJECT per contract v4 rule"

직전 사이클의 3분기 triage(도구부재 / 의도적 미실행 / 미구현 세탁)가 **판정 문구에는 반영되는데
임계 카운트에는 반영되지 않는다.** 구현자가 통제 불가능한 사유로 REJECT 된다.

**반대 극단은 잘 작동한다 — 완화하지 마라:**

- "DG-04: 실기 앱 구동 미실행(사용자 지시에 의한 계획적 이연) — 실행 산출물 부재로 FAIL
  (**도구 부재 아님, 의도적 미실행**)"

improvement 에 2회 등장: "qa-evaluator 에 fitpal-web MCP 바인딩 검토", "evaluator 에 런타임 MCP 도구 부여 권장"

### Q2. 증거의 판별력 — mutation 으로 판별력 0 이 실증됨

- "ER-02: 신규 통합 테스트가 실제 바이너리를 호출하지 않고 독립 재작성한 SQL 로 일반 동작만 검증한다.
  **mutation test 로 확정 — 실제 코드에서 동시성 가드(WHERE exercises = $3::jsonb)를 완전히 삭제해도
  이 테스트는 여전히 통과한다.**"
- "B-03 의 서술이 현재 코드와 불일치함을 **뮤테이션 테스트로 확인**"

### Q3. 사용자 관측 vs 자동 증거 충돌 (§0 D3)

### Q4. 이월 backlog

`harness/agents/qa-evaluator.md` frontmatter 는 `tools: Read, Grep, Glob, Bash` 로 Write 가 없는데
본문이 파일 저장을 지시한다는 지적이 있다. **본문을 직접 읽고** Write 도구를 요구하는지, Bash 로
저장 가능한지 확인한 뒤 실제 모순이면 해소하고, 모순이 아니면 audit-log 항목이 오탐이었다고 보고하라.

## 2. 확보된 외부 근거

### Q1 — abstention / selective prediction

- selective classification: 원하는 risk level 을 정하고 테스트 시 필요한 만큼 reject 해 risk 를 맞춘다.
  예시로 ImageNet top-5 error 2% 를 99.9% 확률로 보장하면서 **coverage 약 60%**.
  <https://arxiv.org/abs/1705.08500>
- uncertainty 기반 abstention: correctness **+2~8%**, unanswerable hallucination **50% 회피**,
  safety **70%~99% 개선**. <https://arxiv.org/abs/2404.10960>
- **AbstentionBench**: 20 dataset / 20 frontier LLM 평가에서 abstention 은 미해결 문제이고,
  **reasoning fine-tuning 이 abstention 을 평균 24% 악화**시켰다. <https://arxiv.org/abs/2506.09038>

함의: 결함은 `[미검증]` 자체가 아니라 **"정당한 도구·환경 부재" 와 "회피성 미실행/미구현/공허한 증거" 를
같은 reject counter 에 넣는 것**이다. selective prediction 관점에서 abstention 은 failure 가 아니라
**uncovered case** 로 따로 집계해야 한다.

### Q2 — mutation 기반 판별력

- Just et al. FSE 2014: 5개 OSS, **321K LOC, 357 real faults** 에서 mutant detection 과
  real fault detection 사이 **통계적으로 유의한 상관**, code coverage 와 **독립적으로도 성립**.
  <https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html>
- 장기 연구: **1,500만 mutants** 분석. 실제 결함을 유발한 변경에서 live mutant 가 보고되어
  bug 를 막을 수 있었다는 evidence.
  <https://research.google/pubs/long-term-effects-of-mutation-testing/>
- 대규모 적용: 전통적 방식은 대규모 코드베이스에 안 맞다. **changed code 만, irrelevant mutant
  filtering, line 당 제한, operator history 기반 선택**으로 줄였다. 적용 규모 **24,000+ developers /
  1,000+ projects**.
  <https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/>
- 산업 적용: full mutation adequacy 달성은 **"neither practical nor desirable"**.
  <https://research.google/pubs/an-industrial-application-of-mutation-testing-lessons-challenges-and-research-directions/>
- RRD: rubric 은 informative / comprehensive / non-redundant 여야 하며, 많은 응답에 동시에 만족되는
  rubric 은 **판별력이 낮아 더 세분화**해야 한다. <https://arxiv.org/html/2602.05125v1/>

### Q3 — oracle problem / human-in-the-loop

- 자동 oracle 이 불완전하면 최종 oracle 정보원은 human 이다. 단 human 도 비용/일관성 문제가 있다.
  <https://discovery.ucl.ac.uk/id/eprint/1471263/>
- APR patch 평가: pass@k 같은 실행 기반 metric 이 실제 patch validity 를 놓친다. human manual
  assessment 도 **Fleiss' Kappa 0.307** 로 낮았고, **shared high-quality rubric 이 agreement 를 크게 개선**.
  48 bugs / 115 patches 에서 human-refined golden rubric 기반 LLM judge 가 human developer consensus 와
  substantial agreement.
  <https://research.google/pubs/towards-a-human-in-the-loop-framework-for-reliable-patch-evaluation-using-an-llm-as-a-judge/>

### Q4 — 편향 (generator/evaluator 분리 후에도 남는 것)

- **position bias 는 분리 후에도 남는다.** 15 LLM judges, MTBench/DevBench 22 tasks, 약 40 generating
  models, **150,000+ evaluation instances**. random chance 가 아니며 judge/task/quality gap 에 따라 달라진다.
  <https://arxiv.org/abs/2406.07791>
- 편향 12종 분류: position, verbosity, compassion-fade/model-name, bandwagon, distraction,
  fallacy-oversight, authority, sentiment, diversity, CoT, self-enhancement, refinement-aware.
  <https://arxiv.org/html/2410.02736>
- self-preference 는 "같은 모델 자신" 만의 문제가 아니다. GPT-4 self-preference bias **0.520**,
  self-generated 여부와 무관하게 **lower perplexity / familiar text** 에 더 높은 평가.
  <https://arxiv.org/abs/2410.21819>
- 같은 모델 계열만으로도 leakage: same model **23.6%**, same family same series **8.9%**,
  different series **2.8%** (PLS). <https://arxiv.org/abs/2502.01534>

## 3. 사실 정정 (중요 — 우리 문서가 오인용하고 있으면 고쳐라)

**scoring bias 논문 <https://arxiv.org/html/2506.22316v1> 은 binary PASS/FAIL 을 직접 주장하지 않는다.**
원문은 score rubric order / score IDs / reference answer score 3종 scoring bias 를 정의하고,
scoring prompt perturbation 이 judge robustness 를 흔든다고 보인다.

**binary/decomposed 의 직접 근거는 CheckEval 이다** — Likert scale + subjective criteria 가
inconsistency 를 만들고, **decomposed binary questions 로 evaluator agreement 를 평균 0.45 개선**.
<https://arxiv.org/abs/2403.18771>

→ `harness/` 전체를 grep 해서 scoring bias 논문을 binary 근거로 인용한 곳이 있으면 CheckEval 로 정정하라.
**전수 조사하라 — 한 곳만 고치면 재발한다.**

## 4. 제안된 규칙 (초안 — 우리 체계에 맞게 재작성하라)

- `[미검증]` 임계를 **triage-aware** 로 전환:
  - `FAIL` — 대상 부재, 미구현, 조건 불충족, **회피성 미실행**
  - `UNVERIFIED_ENV` — 대상은 있으나 evaluator 가 통제 못 하는 도구/런타임/MCP/시뮬레이터 부재.
    자동 REJECT 카운터에서 **분리**
  - `UNVERIFIED_INVALID_EVIDENCE` — 테스트 0개, 빈 캡처, guard 삭제 mutation 에도 통과하는
    공허·무판별 증거. 기존처럼 REJECT 후보
- `UNVERIFIED_ENV` **남용 방지 4요건** (하나라도 없으면 이 분류 금지):
  1차 도구 시도 / fallback 시도 / 실패 로그 / 왜 구현자가 통제 불가능한지 + 재검증 명령
- **Discriminating Evidence Gate** — "위반 시 이 테스트가 깨지는가" 를 확인.
  필수 범위 **한정**: concurrency guard, auth/permission, idempotency, validation, data-loss,
  migration safety, retry/dedup, 보안 경계, **그리고 사용자 결함 보고와 테스트 PASS 가 충돌한 경우**.
  금지: 전체 repo mutation score 임계값, 모든 조건에 강제, cosmetic/doc-only 변경에 요구.
- **Human Oracle Challenge** — 사용자 보고에 구체적 steps/env/expected/actual 이 있으면 승격.
  재현되면 FAIL. 재현 불가가 환경 탓이면 `UNVERIFIED_ENV`. 모호하거나 계약 밖이면 자동 REJECT 하지 말고
  contract amendment 후보로 기록.

## 5. 트레이드오프 (반영하라)

abstention 완화는 회피 경로가 된다 → 4요건 없이는 `UNVERIFIED_ENV` 허용 금지.
mutation 은 비싸다 → diff-scoped / risk-scoped / mutant 수 제한. full adequacy 는 넣지 마라.
인간 보고 우선은 false alarm 비용이 있다 → "인간이 항상 이긴다" 가 아니라
**"구체적 인간 보고는 자동 PASS 를 무효화하고 재현 경로로 보낸다"**.

## 6. 열린 질문 (계약에 결정 근거를 남겨라)

- verdict taxonomy 에 `CONDITIONAL APPROVE_WITH_ENV_GAPS` 를 추가할지, 기존 `BLOCKED` 로만 표현할지.
- `UNVERIFIED_ENV` 가 몇 건이면 coverage 부족으로 BLOCKED 인지 threshold.
- stack 별 mutation 도구 표준 (JS/TS, Python, Rust, Flutter/Dart) 과 "temp copy 에서만 mutate" 규칙.
