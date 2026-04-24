---
feature: "kaizen-phase2-contract-design"
created: "2026-04-24 11:15"
complexity: "medium"
conditions: 19
branch: "kaizen/2026-04-24"
phase: 2
---

# Sprint Contract — Phase 2: Contract Kaizen

Generated: 2026-04-24
Feature: kaizen-phase2-contract-design
Scope (수정 허용): `harness/docs/guides/contract-design-guide.md`, `harness/skills/sprint-contract/SKILL.md`, `harness/references/contract-schema.md` (3 files only)
Branch: kaizen/2026-04-24

## Context

Phase 1 에서 skill-design-guide §11 + agent-design-guide §3.5/§12 (Cross-Surface Parity · Binary Decidability Pre-Check) 가 승격되었다. Phase 2 는 그 원칙을 **계약 설계 레이어**에 전수하고, 글로벌 피드백 61 REJECT 중 계약 작성 단계에서 예방 가능했던 패턴을 구조화한다.

**대표 REJECT 패턴 (data-pool §1 · plugin-qa-data §harness/react/rust/infra):**

- SK-02 (harness): "Neubrutalism shadow offset 3px" 조건에서 적용 범위 (버튼/카드 vs badge/decoration) 모호 → 범위 인라인 명시 필요
- 미검증 항목 2건 이상 REJECT (mcp_server=null): LG-02/DG-04 시각 검증 불가 → 계약 단계에서 **대체 검증 경로** 또는 **`[미검증]` 수용 정책** 미정의
- H-01/H-03 (rust-kit): rust-service 에는 domain event + outbox 원칙 있으나 rust-init/rust-feature/rust-api 에 누락 → sibling skill cross-check 조건 부재
- RE-02 (react-kit): "API 연동" ⊂ "API 연동 화면" substring 중복 → Process 에 set intersection 뿐 아니라 substring 검사도 명시 필요
- KZ-04 (이전 사이클): aggregation mode 미명시로 REJECT (이미 반영, 유지)

**Research sources consulted (3건):**

1. [LLM-as-Judge Reliability — arxiv 2506.13639](https://arxiv.org/html/2506.13639v1) — criteria 품질이 judge alignment 에 결정적 (상관계수 0.666 → 0.487 drop), 극단값 정의가 중간값보다 중요 → **이진 판정 우선주의** + CoT 는 명확한 criteria 있을 때 효과 미미 → **계약 명확화가 ROI 최고**
2. [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices) — one When-Then pair, 복합 assertion 분리, "2-3 Ands" 상한
3. [Agile Alliance INVEST — Testable](https://www.agilealliance.org/glossary/invest/) — 제3자가 objectively 확인 가능해야 하며 측정 가능 값 + 구체 행동 명시

Research inputs: `.claude/kaizen-input/MASTER.md`, `.claude/kaizen-input/insights-report.md`, `.claude/kaizen-input/plugin-qa-data.md` (harness/react/rust/infra 섹션), `.harness/.meta/kaizen-data-pool.md` §1.

---

## Success Criteria (binary PASS/FAIL)

### CSP — Cross-Surface Parity (Phase 1 원칙 전수, 필수)

- [ ] **CSP-01** [structural]: `contract-design-guide.md` 에 새 섹션 "§N. 원칙 전수성 · Cross-Surface Parity Checklist" 가 존재하며, Phase 1 의 5개 parity item (계약 모호성 방지 / 트리거 키워드 배타성 / 검증 가능한 성공 기준 / rule-by-rule audit / 미검증 항목 정책) 중 **계약 설계에 해당하는 3 개 이상** 에 대해 contract-design-guide 내 대응 위치를 표로 명시한다
- [ ] **CSP-02** [exact]: CSP-01 섹션이 `skill-design-guide §11` 과 `agent-design-guide §12` 를 링크로 **둘 다** 참조한다 (둘 중 하나만 참조하면 FAIL). `[exact, enumerated]`

### BD — Binary Decidability (계약 작성자 의무 — Phase 1 §3.5 전수)

- [ ] **BD-01** [structural]: `contract-design-guide.md` 에 "계약 작성자 의무 — 이진 판정 가능성" 서브섹션이 신설되며, `[exact]`/`[structural]`/`[goal]` 태그 3 종 모두의 판정 기준을 재확인한다
- [ ] **BD-02** [exact]: 해당 서브섹션에 agent-design-guide §3.5 Binary Decidability Pre-Check 로 링크/참조가 **정확한 문자열로** 포함된다 (링크 텍스트에 "agent-design-guide §3.5" 또는 "Binary Decidability" 중 하나라도 포함되면 PASS)
- [ ] **BD-03** [goal]: Gotchas/안티패턴 표에 "정성적 수식어 (충분히, 상당한, 적절히 등) 가 1개 이상 포함된 조건은 작성 금지" 가 이진 판정 실패 사례로 1 항목 이상 언급된다

### SR — Scope Range Notation (SK-02 재발 방지)

- [ ] **SR-01** [structural]: `contract-design-guide.md` 조건 작성법 섹션에 "스코프 범위 인라인 명시 (Scope Range)" 서브섹션이 존재한다. "주요 interactive element", "모든 파일" 같은 범위어는 **예시를 인라인으로 열거** 하거나 `applies_to` 로 한정해야 한다는 원칙을 서술
- [ ] **SR-02** [exact]: SR-01 에 Bad/Good 예시가 각 1 쌍 이상 포함된다. Bad 예시는 "주요 interactive element 의 shadow offset >= 4px" 형태의 범위 모호 조건, Good 예시는 "버튼·카드·입력 요소 의 shadow offset >= 4px (badge/decoration 은 예외)" 형태의 인라인 enumerate
- [ ] **SR-03** [structural]: contract-design-guide 의 안티패턴 표에 "스코프 범위어 미명시" 1 행이 추가된다

### UV — Unverifiable Condition Policy (mcp_server=null · fit-pal LG-02/DG-04 재발 방지)

- [ ] **UV-01** [structural]: `contract-design-guide.md` 에 "검증 수단 명시 의무 — Verification Method Required" 서브섹션이 존재한다. 모든 조건은 **어떤 도구·명령·관찰로 판정할지** 를 인라인으로 명시하거나, `[미검증]` 정책을 따르는 대체 검증 경로를 기술해야 한다
- [ ] **UV-02** [exact]: 해당 섹션에 "MCP/외부 도구 의존 조건" 에 대한 **3 단계 fallback 규칙** 이 enumerate 된다: (1) 기본 검증 방법, (2) MCP/외부 도구 미가용 시 대체 정적 검증 방법, (3) 어떤 것도 불가능하면 `[미검증]` 마커 + 수용 임계 (이 조건 미검증 총 1 건까지 허용)
- [ ] **UV-03** [goal]: qa-evaluation-guide 와 충돌 없음 — qa-evaluation-guide 의 "미검증 2 건 이상 REJECT" 정책을 계약 작성자 관점에서 **사전 예방**하는 서술 포함 ("계약 작성 단계에서 `[미검증]` 허용 건수가 2 건 이상 예상되면 조건을 재설계하라")

### SC — Sibling Consistency (rust-kit H-01/H-03 재발 방지)

- [ ] **SC-01** [structural]: `contract-design-guide.md` 에 "형제 스킬 일관성 조건 (Sibling Consistency)" 서브섹션 존재. 동일 플러그인 내 여러 스킬이 **공통 원칙**을 요구할 때, 계약은 "X 원칙이 sibling 스킬 N 개 **전부** 에 적용되어 있다 [exact, enumerated]" 형태로 명시해야 한다는 원칙 서술
- [ ] **SC-02** [exact]: SC-01 에 rust-kit H-01/H-03 REJECT 사례 인용 — "rust-service 에는 있고 rust-init/rust-feature/rust-api 에 없는 domain event + outbox 원칙" 반례를 Bad 블록으로 삽입

### SB — Substring Exclusivity in Skill Process (RE-02 · SK-05 재발 방지)

- [ ] **SB-01** [structural]: `harness/skills/sprint-contract/SKILL.md` Process 섹션 (Step 1~10 중 계약 생성 전 단계) 에 **"트리거 키워드 중복 검사 — set intersection + substring containment 둘 다 수행"** 이 명시적 Step 또는 Process 내 sub-step 으로 존재한다
- [ ] **SB-02** [exact]: SB-01 Step 본문에 구체적 명령/로직 예시가 포함된다. "다른 스킬 description 의 트리거 키워드를 grep 하여 (a) 완전 일치 교집합과 (b) 한 쪽 키워드가 다른 키워드의 부분문자열인 쌍을 모두 찾아 0 건임을 확인" 형태의 절차 기술 1 문단 이상

### VC — Verifiability Charter (research-backed 보강)

- [ ] **VC-01** [structural]: `contract-design-guide.md` 핵심 원칙 §검증 가능성 섹션에 INVEST Testable 원칙 인용 ("제3자가 objectively 확인 가능" 문구 또는 유사 표현) 1 문장 이상
- [ ] **VC-02** [structural]: `contract-design-guide.md` 에 LLM-as-Judge (arxiv 2506.13639) 의 "criteria 품질이 judge alignment 에 결정적" 인용이 1 회 이상 (기존 인용이 있어도 이 사이클에서 extreme-value definition 관련 새 문장 1 개 이상 추가)

### SCH — Schema Update (contract-schema.md)

- [ ] **SCH-01** [exact]: `harness/references/contract-schema.md` 의 스키마 버전을 `v3` 로 bump 하고 변경 이력에 "v3 (2026-04-24) — 검증 수단 명시 의무, 스코프 범위 인라인 명시, sibling consistency 조건 패턴 추가" 1 줄 이상 기록한다
- [ ] **SCH-02** [structural]: schema 파일에 `[미검증]` 마커 또는 "verification_method" 필드 표기 규칙이 1 문단 이상 서술된다

## Anti-patterns

- [ ] AP-range-missing: 스코프 범위어 ("주요", "모든", "대부분") 가 인라인 enumerate 없이 계약 조건에 등장
- [ ] AP-verif-missing: 조건이 측정/관찰 방법 없이 작성되어 qa-evaluator 가 판정 도구를 임의 선택해야 함
- [ ] AP-sibling-skip: 동일 원칙이 sibling 스킬 일부에만 적용되는 상태를 계약이 방치
- [ ] AP-parity-leak: Phase 1 guide 의 원칙이 contract-design-guide 에 전수되지 않음

## Reusability

- [ ] RE-01: contract-design-guide 의 새 섹션은 `harness/references/contract-schema.md` 와 중복 서술 없이 링크로 참조한다
- [ ] RE-02: 기존 "조건 구체성 태그" 서브섹션을 삭제하거나 이름을 바꾸지 않는다 (다른 스킬/에이전트에서 참조 중)

## Diagnostics

- [ ] DG-01: 문서 변경 후 `python3 scripts/validate-plugin.py harness` 실행 시 exit 0 (7 카테고리 모두 OK)
- [ ] DG-02: 세 파일의 공개 구조 (frontmatter, 주요 헤더) 가 파싱 에러 없이 유지 (Markdown 렌더러 기준)
- [ ] DG-03: 기존 cross-reference 링크가 깨지지 않음 — `harness/references/contract-schema.md` 가 contract-design-guide 로 redirect 하는 문구 유지
- [ ] DG-04: 수정 후 `git diff --stat` 결과에 범위 3 파일 외 변경 없음 (sprint-contract.md, sprint-feedback.md, .harness/.meta/ 는 scope_out 예외)

---

## 자기진단 (Self-diagnosis checklist)

| 항목 | 판정 |
|------|------|
| ambiguous_conditions | false — 모든 조건에 `[exact]/[structural]/[goal]` 태그 부여 |
| missing_error_paths | false — UV 카테고리가 검증 불가 경로 커버 |
| untestable_conditions | false — Grep/읽기 기반으로 전 조건 검증 가능 |
| category_coverage_gap | false — CSP/BD/SR/UV/SC/SB/VC/SCH 8 개 카테고리 |
| complexity_underestimate | false — medium 복잡도, 19 조건 (가이드 8-12 범위 상회 — Cross-Surface 성격상 의도) |
| implementation_leakage | false — 파일명/섹션 기반, 내부 API 용어 없음 |
| nfr_coverage | partial — 문서 품질이 기능 요구이므로 NFR 는 DG 카테고리로 대체 |
| boundary_without_measurement | false — 수치 조건 없음 (SCH-01 의 "v3" 만 문자 매칭) |
| format_granularity_missing | false — 각 조건에 field-level 명시 (섹션명/문구 포함) |

## Rationale — 왜 이 계약인가

LLM-as-Judge 연구는 "criteria 품질이 judge alignment 에 결정적" 이라고 보고한다. Phase 2 는 계약 작성 단계 자체가 평가 품질의 상한을 결정한다는 전제로, (1) Phase 1 원칙 전수 (CSP/BD), (2) 반복 REJECT 패턴의 구조적 예방 (SR/UV/SC/SB), (3) 연구 기반 원칙 보강 (VC), (4) 스키마 버전 bump (SCH) 를 구성한다. 19 조건은 parity + prevention + research backing 을 독립 검증 가능하도록 쪼갠 결과이며, 각 조건은 파일 읽기 + Grep 만으로 이진 판정 가능하다.
