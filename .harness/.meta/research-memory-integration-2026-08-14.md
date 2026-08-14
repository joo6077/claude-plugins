# 리서치 — 카이젠 ↔ 메모리 양방향 연동

수집: 2026-08-14 · 출처 유형: **WebSearch fallback** (Codex 사용량 한도 도달 — 리셋 8/20, 실패 출력 확인 후 사용자 승인)
대상: `docs/superpowers/followup-kaizen-memory-integration.md` 의 설계 근거

---

## 1. 승격 기준 — 언제 영속 메모리로 올리는가

**관찰 사실**

- 원시 trajectory 를 전부 저장하는 "add-all" 은 성공 시퀀스와 환각·오류를 뒤섞어 **오류 누적과
  실패 반복**을 낳는다. 저장 전략은 add-all → 자동 품질 평가기(LLM/human-in-the-loop 스코어링) →
  피드백 기반 적응적 선별의 스펙트럼에 놓인다
  ([From Storage to Experience 서베이](https://arxiv.org/pdf/2605.06716)).
- **선별적 추가·삭제가 장기 성능을 10% 올리고** 오류 전파와 잘못된 경험 재사용 위험을 줄인다는
  체계적 연구 결과가 보고돼 있다 (같은 서베이).
- SSGM 은 승격 전에 **Write Validation Gate** 를 둔다. 새 항목이 보호된 core fact 와 논리적으로
  모순되면(`ΔM ∧ M_core ⊧ ⊥`) 갱신을 **거부**한다. NLI 검사로 환각이 의미 그래프를 영구
  오염시키는 것을 막는다 ([SSGM](https://arxiv.org/html/2603.11768v1)).

**레포 현황 대조** — reflect-kit 은 이미 선별적이다.

- 승격 임계는 **`cluster_freq`** (정규화 후 클러스터 합산). 원시 태그 빈도 금지가 Gotcha #8 로
  박혀 있다. 실측 근거도 있다 — `skipped-required-api-doc-check` 원시 71 건 vs 클러스터 110 건,
  원시 집계는 55% 를 잃고 있었다.
- `actionability: user_environment` 는 승격 파이프라인에서 **배제**한다 (760 엔트리 중 351 건이
  단일 환경 오설정의 반복 로깅이었다).
- `user_stated_constraint == true` 는 **freq ≥ 1 로 임계 우회 fast-track**.

**갭**: reflect-kit 에 **모순 검사(Write Validation Gate)가 없다.** 새 교훈이 기존 메모리와
반대되는 내용일 때의 판정 절차가 없다. 지금은 엔트리 23 건이라 사람이 알아채지만 늘어나면 못 잡는다.

---

## 2. 중복·충돌 처리

**관찰 사실**

- SSGM 은 충돌 해소를 **미해결 문제로 명시**한다 — *"drift 와 update 를 구분할 수 있는 conflict
  resolution protocol 설계는 열린 알고리즘 문제로 남아 있다"*. 프레임워크는 immutable episodic
  ledger 로 재조정하라고만 하고 병합 규칙은 정하지 않는다.

**레포 현황** — reflect-kit 의 처리가 오히려 구체적이다.

- 같은 `canonical_tag`(또는 그 alias)가 `status: active` 로 있으면 **신규 append 금지**.
  대신 **enforcement 등급 상향** — *"같은 surface 에서 문구만 다시 다듬는 것은 이미 실패한
  처방의 반복이다"* (reflect-promote Gotcha #3).
- 표기 유사성으로 합치지 않는다. `undesired_behavior` 와 `desired_behavior` 가 **둘 다** 같을
  때만 alias 로 본다. 아니면 `family` 로만 보고하고 `cluster_freq` 에 합산하지 않는다.

**추론**: 재발을 "강화"가 아니라 "등급 상향"으로 처리하는 규칙은 공개 문헌에서 대응물을 못 찾았다.
같은 처방을 반복 주입하는 것을 실패로 규정한 점에서 SSGM 의 미해결 지점보다 앞서 있다.

---

## 3. 회수 — 무엇을 컨텍스트에 넣는가

**관찰 사실**

- Generative Agents 는 **relevance + recency + importance** 를 정규화 후 **동일 가중**으로 합산한다.
  relevance 는 임베딩 코사인 유사도, importance 는 LLM 이 매기는 의미적 중요도다.
  가중치는 **수기 튜닝**이며 저자들이 *"프로덕션에서는 RL 로 학습되어야 할 것"* 이라 적었다
  ([Generative Agents](https://dl.acm.org/doi/fullHtml/10.1145/3586183.3606763)).
- 세 축의 역할 분담이 명시돼 있다 — *recency 는 낡은 컨텍스트의 지배를 막고, relevance 는 주제
  일치를 보장하고, importance 는 고신호 관측이 잡음을 이기게 한다*.
- **ablation 에서 세 요소 각각이 성능에 critical** 로 확인됐다.
- 다요인 가치 모델(recency/relevance/importance + emotional salience)이 단일 축 baseline
  (recency-only · relevance-only · importance-only)을 전부 상회한다
  ([Learning What to Remember](https://arxiv.org/pdf/2606.12945)).

**갭**: 카이젠 데이터 풀은 섹션을 **전량 주입**한다. 메모리를 그대로 §0.5 에 통째로 넣으면
엔트리가 늘수록 신호가 희석된다. 현재 23 건이면 무해하지만 설계 시점에 회수 기준을 넣어야 한다.

---

## 4. 실패 모드 — 이 설계에서 가장 중요한 절

**관찰 사실**

- 진화하는 메모리는 **피드백 루프**를 만들고 여기서 오류가 누적된다. 핵심 실패 지점 3 개가
  식별돼 있다 — **입력 시 Memory Poisoning · 통합 시 Semantic Drift · 회수 시 Conflict/Hallucination**
  ([SSGM](https://arxiv.org/html/2603.11768v1) · [MemEvoBench](https://arxiv.org/pdf/2604.15774)).
- drift 는 세 종류다: **Semantic**(반복 요약으로 뉘앙스 소실) · **Procedural**(차선·낡은 워크플로
  강화) · **Goal**(누적 상호작용 편향으로 정렬 이동).
- **에이전트 자신의 행동 결과가 메모리에 기록되면 자기검증 피드백 루프가 된다** —
  로그 항목이나 DB 갱신이 메모리로 write-back 되는 순간 에이전트의 행동이 자기 오정렬을
  강화하는 근거가 된다 ([NeuralTrust](https://neuraltrust.ai/blog/memory-context-poisoning) ·
  [MintMCP](https://www.mintmcp.com/blog/ai-agent-memory-poisoning)).
- 자기진화 에이전트는 **국소적으로 맞지만 이전 불가능한 경험을 과일반화**해 스스로 메모리를
  오염시킨다. 공격자는 대화 이력을 조작해 통합 단계가 비이전적 국소 방법을 **영속 규칙으로
  증류**하게 만들 수 있다 ([OEP](https://arxiv.org/pdf/2605.18930)).
- **TTL 이 폭발 반경을 제한한다** — 오염 항목이 30 일 뒤 만료되면 공격 창이 유한해지지만,
  TTL 이 없으면 **단 한 번의 주입이 무기한 영향**을 준다.
- SSGM 의 완화책은 **Reversible Reconciliation** — 가변 active 그래프 + 불변 episodic 로그를
  짝지어 주기적으로 replay 하며 drift 를 교정한다. 이론적으로 무제약 시스템의 누적 drift
  `O(T·ε)` 를 N 스텝마다 재조정 시 `O(N·ε)` 로 묶는다 (Theorem 1). **경험 결과는 없다** —
  검증 가능한 가설 3 개(H1~H3)만 제시하고 baseline 수치는 없다.
- 시간 감쇠는 Weibull `w(Δτ)=exp(−(Δτ/η)^κ)` (Δτ = 마지막 회수 이후 경과)와
  freshness 임계 `θ_fresh` 로 표현한다.

**이 프로젝트에 직결되는 지점**

카이젠이 메모리를 쓰고 그 메모리를 다시 카이젠이 읽으면 **문헌이 이름 붙인 자기검증 루프
그대로**다. 이번 사이클이 Final 계약에서 겪은 자기참조 결함(피드백 파일이 위반을 인용해 다음
라운드의 위반 근거가 됨)과 **구조가 같다.** 그때 해법은 자기 산출물을 입력에서 제외하는
공통 전제를 헤더에 1 회 선언한 것이었다.

**레포 현황 대조**

- reflect-kit 의 **ledger + rollback** 이 SSGM 의 immutable episodic log + reversible
  reconciliation 과 정확히 대응한다. `rule_id` UUID · `status: active|removed|demoted` ·
  `demotion_reason` · rollback 은 ledger 삭제가 아니라 상태 갱신 + 실제 파일에서 제거.
- **30 일 post_freq 측정 후 재발 0 + low risk 면 `demoted` 후보** — TTL 의 조건부 형태다.
  단 `singleton_share` 가 임계(0.70)를 넘은 기간의 `post_freq` 는 과소집계라 그 상태에서는
  demotion 후보를 내지 않는다.
- **갭**: 무조건 TTL 이 없다. 재발이 없어도 high risk 면 영구 잔존한다. 문헌 기준으로는
  이것이 "단 한 번의 주입이 무기한 영향" 조건이다.
- **갭**: 메모리 엔트리에 **provenance(출처) 필드가 없다.** 누가 썼는지 — 세션 중 사용자 교정인지,
  카이젠 자기산출인지 — 구분이 안 된다. 자기검증 루프를 막으려면 이 구분이 선결이다.

---

## 5. 규칙 vs 메모리 vs 훅 — 배치 기준

**관찰 사실**: 이 세 표면의 배치를 다룬 **공개 방법론을 찾지 못했다.** 문헌은 메모리 내부
(저장·회수·거버넌스)를 다루고, "항상 로드되는 규칙 파일 / 온디맨드 메모리 / 기계적 강제 훅"
삼분할은 Claude Code 류 하네스 고유 구조로 보인다.

**레포 현황** — reflect-kit 의 4 축 precedence 가 사실상 이 문제의 자체 해법이다.

```text
scope            session | project | global
risk_class       low | medium | high
procedurality    single_rule | multi_step_procedure
enforcement_need soft_reminder | hard_gate
```

**4 축 타당성 평가 (사용자 질문)**

공개 다요인 모델과 **재는 대상이 다르다**. Generative Agents 의 relevance/recency/importance 와
다요인 가치 모델의 4 요인은 전부 **보존·회수 가치**(이 기억을 유지할까 / 지금 꺼낼까)를 매긴다.
reflect-kit 의 4 축은 **배치**(어느 표면에 둘까)를 결정한다. 둘은 직교하는 축이고 서로를
대체하지 않는다.

- **타당하다고 보는 근거**: `enforcement_need` 가 hard_gate 면 훅, soft_reminder 면 문서라는
  매핑은 문헌의 "선별적 저장" 원칙과 충돌하지 않고, 오히려 **강제 수단까지 포함해 선별**한다는
  점에서 확장이다. `procedurality` 로 단일 규칙과 다단계 절차를 가르는 것도
  Meta-Policy Reflexion 의 **재사용 가능한 반성 메모리 + rule admissibility** 개념과 결이 같다
  ([Meta-Policy Reflexion](https://arxiv.org/pdf/2509.03990)).
- **빠진 것**: 보존·회수 축이 없다. 4 축은 "어디에 둘까" 만 답하고 "언제 꺼낼까 / 언제 버릴까" 는
  답하지 않는다. 승격 후 회수는 description 문자열 매칭에 맡겨져 있다.
- **임계값은 스스로 hypothesis 로 라벨돼 있다** — 이건 정직한 설계다. 문헌도 Generative Agents 의
  가중치가 수기 튜닝이며 학습되어야 한다고 인정한다.

---

## 권장안

### R1. 읽기 — 데이터 풀 §0.5 는 전량 주입이 아니라 선별 주입

`feedback` 타입 우선 · 전 프로젝트 교차(사용자 결정). 다만 **전량이 아니라 상위 N**.
선별 축은 Generative Agents 3 축을 이 도메인에 옮긴다:

| 문헌 축 | 이 도메인 대응 | 데이터 출처 |
| --- | --- | --- |
| relevance | 해당 Phase 도메인과의 일치 | 메모리 description ↔ Phase 대상 킷 |
| recency | 최근 기록·갱신 | frontmatter `modified` |
| importance | 재발 빈도 · risk_class | ledger `initial_freq` / `post_freq` |

동일 가중으로 시작한다 (문헌이 그렇게 하고, 학습 근거가 없다). **임계는 hypothesis 로 라벨**한다.

### R2. 쓰기 — 카이젠은 직접 쓰지 말고 후보만 낸다

reflect-promote 가 이미 ledger · rule_id · rollback · 중복 판정(등급 상향)을 소유한다.
카이젠이 병렬 쓰기 경로를 만들면 **ledger 가 두 갈래로 갈라져 rollback 이 깨진다**
(reflect-digest Gotcha #1 이 digest 에 대해 금지한 것과 같은 이유).

→ 카이젠 Final 단계가 `reflect-promote` 가 먹을 수 있는 **후보 파일**을 산출하고,
승격 자체는 reflect-promote 를 호출해 처리한다.

### R3. grounding 필드 신설 — 자기검증 루프 차단 (최우선)

**초안 정정 (2026-08-14, 사용자 지적).** 처음에는 `origin: session | kaizen` 으로 **저자**를
가르려 했다. 틀렸다. 메모리의 `feedback_*.md` 는 **전부 Claude 가 쓴 것**이므로 저자로 가르면
모두 같은 쪽에 떨어지고 아무것도 끊기지 않는다.

가를 축은 저자가 아니라 **무엇이 그 교훈을 뒷받침하느냐** 다.

실측 (현재 레포 메모리 18 개 `feedback_*` 엔트리, 근거 어휘 계수):

| grounding | 대표 엔트리 | 사용자근거/자체관측 | 성격 |
| --- | --- | --- | --- |
| `user_correction` | `setup_guide_site_distinction` · `skill_invocation_evidence` | 4/0 · 1/0 | 외부 **인간** 신호 |
| `execution_evidence` | `no_schema_on_qa_subagent` · `oracle_must_execute_not_grep` | 0/6 · 0/2 | 외부 **기계** 신호 (QA verdict · 명령 출력 · 실측) |
| `mixed` | `qa_preference` · `always_sprint_contract_before_qa` | 2/6 · 3/5 | 둘 다 |
| `self_inference` | — (현재 0 건으로 보이나 명시 필드가 없어 확정 불가) | — | 외부 검증 **없는** 자기추론 |

```yaml
metadata:
  type: feedback
  grounding: user_correction | execution_evidence | mixed | self_inference
```

**왜 이 축인가.** OEP 가 지목한 오염 경로는 *"국소적으로 맞지만 이전 불가능한 경험을
과일반화"* 다 — 즉 **외부 검증 없는 자기추론**이 영속 규칙으로 증류되는 것이다. QA 가 REJECT 를
냈다거나 명령 출력이 그렇다는 것은 자기주장이 아니라 **기계적 뒷받침**이므로, 카이젠이
자기 사이클에서 쓴 교훈이라도 `execution_evidence` 면 되먹임 위험이 낮다.
차단해야 할 것은 "카이젠이 썼다" 가 아니라 "아무도 확인하지 않았다" 다.

**적용:**

- 데이터 풀 §0.5 는 `user_correction` · `execution_evidence` 를 **우선 주입**한다.
- `self_inference` 는 제외하거나 **명시 라벨**을 달아 Phase 가 근거로 삼지 않게 한다
  (계약 조건의 PASS 근거로 쓰지 마라 — amendment `consent: unanchored` 를 PASS 근거로 못 쓰는 것과 같다).
- 기존 18 건은 **소급 태깅이 필요**하다. 어휘 계수는 근사치일 뿐이라 사람 확인이 있어야 한다.

이것이 이번 사이클 Final v3 이 자기참조에 적용한 처방과 같은 계열이지만 **축이 다르다** —
Final 은 *자기 산출물인가* 로 갈랐고(파일 경로로 판정 가능), 메모리는 *검증됐는가* 로 가른다.

### R4. Write Validation Gate — 모순 검사

승격 전 기존 메모리와의 모순을 확인한다. NLI 모델을 붙일 필요는 없다 — 엔트리가 수십 건
규모이므로 **같은 `canonical_tag` 클러스터 내에서 `desired_behavior` 가 반대인 항목이 있는지**
확인하는 것으로 시작한다. reflect-promote 의 alias 판정(§2)이 이미 두 필드를 비교하고 있어
재사용 가능하다.

### R5. TTL — 무조건 만료를 하나 둔다

현재 demotion 은 조건부다(재발 0 + low risk). 문헌 기준으로는 그것만으로 "단 한 번의 주입이
무기한 영향" 을 막지 못한다. **risk_class 무관하게 N 일 미회수 시 재확인 대상으로 표시**하는
축을 하나 추가한다. 삭제가 아니라 **재확인 플래그**로 시작하는 것이 안전하다 —
`singleton_share` 과소집계 문제(§4)가 여기에도 걸린다.

---

## 트레이드오프

- **선별 주입(R1)은 신호를 놓칠 수 있다.** 상위 N 밖에 있던 메모리가 그 Phase 에 결정적일 수
  있다. 완화: 선별에서 탈락한 항목의 **제목 목록만** §0.5 말미에 붙여 Phase 가 필요하면
  직접 읽게 한다.
- **provenance 제외(R3)는 카이젠이 자기 교훈을 못 보게 한다.** 의도된 것이지만, 사이클 간
  누적 학습이 끊긴다. 완화: 제외가 아니라 **별도 섹션 + "자기산출" 라벨**로 두고 Phase 가
  가중치를 낮춰 읽게 하는 것도 가능하다. 어느 쪽인지는 결정 필요.
- **후보만 내기(R2)는 단계가 하나 늘어난다.** 카이젠이 끝나도 승격이 자동으로 안 된다.
  ledger 무결성과의 교환이다.
- **TTL(R5)은 오탐 위험.** 오래 안 걸렸다고 틀린 규칙이 아니다. 그래서 삭제가 아니라 재확인.

---

## 열린 질문 — 결정 필요

1. **R3 의 형태**: `origin: kaizen` 을 §0.5 에서 **완전 제외**할 것인가, **별도 섹션 + 라벨**로
   둘 것인가? 문헌은 자기검증 루프를 위험으로만 규정하고 "얼마나 끊어야 하는지" 는 안 다룬다.
2. **R1 의 N**: 상위 몇 건을 주입할 것인가. 현재 메모리 23 건이면 전량도 무해하다.
   N 을 지금 정할 것인가, 엔트리 수가 임계를 넘을 때 도입할 것인가?
3. **훅 3 종의 우선순위**: dir-wide autofixer 차단 · 계약 린터 · 기존 훅 오탐 개선 중
   무엇부터인가. (기존 훅 오탐 개선은 이번 세션에 **일부 착수됨** —
   `enforce-foreground-research.sh` 에 사용자 승인 센티넬 게이트를 넣어 문서만 있고 코드에는
   없던 fallback 경로를 구현했다. 4 축 대조로 검증 완료.)
4. **reflect-kit 과의 경계**: 카이젠이 후보를 내면 그것을 reflect-digest 가 집계하는가,
   reflect-promote 가 바로 먹는가? digest 는 대화 로그 기반이고 카이젠은 사이클 산출물 기반이라
   입력 성격이 다르다.

---

## 방법론적 한계 — 이 리서치 자체에 대해

- Codex 사용량 한도로 **WebSearch fallback** 을 썼다. Codex 의 자체 web search 대비 검색 깊이가
  얕을 수 있다.
- SSGM 은 **경험 결과가 없는 이론 프레임워크**다 (baseline 수치 0, 가설 3 개만 제시).
  Theorem 1 의 drift 경계도 가정 위의 이론값이다. 설계 근거로 쓰되 "검증된 수치" 로 인용하지 마라.
- "선별적 추가·삭제 10% 향상" 은 서베이가 인용한 수치이고 원 논문을 직접 확인하지 못했다.
  **[미확인]** 으로 취급한다.
- 다요인 가치 모델 논문은 PDF 구조상 구체적 임계값을 추출하지 못했다. 축 구성과 baseline 우위만
  확인했다.
