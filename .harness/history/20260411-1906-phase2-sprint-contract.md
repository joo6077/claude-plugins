# Sprint Contract — Phase 2 Kaizen Research Mode (Contract)

Feature: contract-design-guide / sprint-contract 2026 최신 패턴 리서치 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1 (commit 4587154, e7b2a10, 5061714) 이 skill-design-guide / agent-design-guide 를 v1.1.0 으로 갱신하면서 두 가지 정합성 이슈를 남겼다:

1. **L1/L2/L3 네이밍 충돌** — skill-design-guide §5.5 가 `L1/L2/L3` 을 **QA 평가 깊이 전용** 으로 예약했고, agent-design-guide §10 이 계약에서 `[exact]`/`[structural]`/`[goal]` 태그를 사용한다고 referencing 한다. 그런데 현재 contract-design-guide §5 는 여전히 `[L1]`/`[L2]`/`[L3]` 을 "조건 구체성 레벨" 로 사용 중. Phase 1 변경과 직접 충돌.
2. **sprint-contract SKILL.md Gotcha** 도 `[L1]`/`[L2]`/`[L3]` 태그 지시가 들어 있어 동일 충돌.

동시에 최근 REJECT 패턴 (kaizen-data-pool §1) 에서 도출된 아래 이슈를 해결한다:

- PU-04: 함수 이름 고정 (L1 exact) vs 동작 목표 (L3 goal) 혼선 — 태그 기본값/선택 기준 가이드 부재
- CD-02: 예외 조항 없는 전체 적용 패턴 — 예외 가이드는 이미 있으나 aggregation mode (개별 명시 vs 포괄 경로) 부재
- KZ-04: "개별 명시" vs "포괄 경로" 형식 요구 불명확 → contract 구조에 aggregation mode 개념 신규 추가
- Improvement: 한국어/영어 표현 변형 병기 권장 (Layout shift vs 레이아웃 shift)
- 구체성 레벨 L1/L2/L3 명칭 혼용 모니터링 (Improvement 직접 언급)

## 리서치 소스 (URL 필수)

1. [LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — arxiv 2412.05579](https://arxiv.org/abs/2412.05579) — judge criteria·rubric 체계화
2. [An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability — arxiv 2506.13639](https://arxiv.org/html/2506.13639v1) — "evaluation criteria are critical for reliability" (CoT minimal gain)
3. [A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System — arxiv 2510.09721](https://arxiv.org/html/2510.09721v3) — unit test = executable formal contract
4. [Automatically Benchmarking LLM Code Agents (AAA methodology) — arxiv 2510.24358](https://arxiv.org/html/2510.24358v1) — PRD blueprint + Arrange-Act-Assert
5. [Specification and Evaluation of Multi-Agent LLM Systems — arxiv 2506.10467](https://arxiv.org/html/2506.10467) — agent schema specification language
6. [Gherkin Best Practices (one When-Then pair per scenario)](https://github.com/andredesousa/gherkin-best-practices)
7. [Avoiding Ambiguity in Requirements Specifications — Tjong thesis (Waterloo)](https://cs.uwaterloo.ca/~dberry/FTP_SITE/tech.reports/TjongThesis.pdf) — 어휘/구문/의미 모호성 분류 원전
8. [Acceptance Criteria Anti-patterns — nextgenanalysts](https://nextgenanalysts.co.uk/how-to-write-clear-and-concise-acceptance-criteria-with-practical-examples/)

## 완료 조건 (Sprint Contract)

### CG (contract-design-guide.md)

- [ ] CG-01 [exact]: "조건 구체성 레벨" 표에서 컬럼 `L1/L2/L3` 을 `[exact]/[structural]/[goal]` 태그명으로 교체. 표에 `[Lx]` 문자열이 0건이며, `[exact]`, `[structural]`, `[goal]` 각 1회 이상 등장
- [ ] CG-02 [exact]: 네이밍 충돌 경고 노트 추가 — "L1/L2/L3 은 QA 평가 깊이 전용 (skill-design-guide §5.5) 이므로 계약 태그로 재사용 금지" 문장이 §5 에 1건 이상 존재
- [ ] CG-03 [exact]: 태그 미명시 시 기본값이 `[structural]` 임을 명시 (기존 "L2" 기본값과 의미 등가)
- [ ] CG-04 [structural]: "태그 선택 기준" 서브섹션 신규 추가 — 함수명 고정 시 `[exact]`, 구조 서명 시 `[structural]`, 동작 목표 서명 시 `[goal]` 선택 기준이 각각 최소 1문장으로 설명됨 (PU-04 REJECT 패턴 fix)
- [ ] CG-05 [structural]: "Aggregation Mode" 서브섹션 신규 추가 — 조건이 다수 대상(파일/모듈/키워드)에 적용될 때 `각자 개별 명시` vs `포괄 경로 하나로 지정` 중 어느 형식을 요구하는지 계약 작성자가 선택·명시하는 방법 설명. KZ-04 REJECT 사유를 예시로 인용
- [ ] CG-06 [structural]: "Consumer-Driven 원칙" 항목 아래 LLM-as-Judge 연구 인용 추가 — "evaluation criteria are critical for reliability" 요지와 arxiv 2506.13639 URL 1건
- [ ] CG-07 [exact]: AAA (Arrange-Act-Assert) 패턴 언급 1건 이상 추가 — Given-When-Then 과 병행 사용 가능함을 명시, arxiv 2510.24358 URL 1건 인용
- [ ] CG-08 [structural]: 조건에 **한국어/영어 표현 변형이 있는 키워드** (예: "Layout shift" vs "레이아웃 shift") 를 병기하거나 한쪽으로 통일할 것을 권고하는 노트 1건 이상 (Improvement §1 반영)
- [ ] CG-09 [exact]: 안티패턴 표의 "판정 기준 범주 미명시" 행에서 `[L1]/[L2]/[L3]` 문자열을 `[exact]/[structural]/[goal]` 로 교체
- [ ] CG-10 [exact]: 안티패턴 표에 "한·영 표현 변형 비통일" 행 신규 추가
- [ ] CG-11 [exact]: 본문 내 모든 `[L1]`/`[L2]`/`[L3]` 문자열 등장 횟수 0건 (전수 교체 확인용). 단, `qa` 나 `platform` 같은 비계약 맥락에서의 L1/L2/L3 이 필요하면 그 케이스는 없으므로 0 을 기대한다
- [ ] CG-12 [exact]: 각 신규/개정 섹션에 **출처 URL** 이 최소 1건 인용됨 (CG-04 는 REJECT 사유 실제 사례, CG-05 는 KZ-04 사유 실제 사례, CG-06/07 은 arxiv URL)
- [ ] CG-13 [exact]: 문서 내 bare code fence (` ``` ` 뒤 바로 개행) 0건 — DG-02 anti 준수
- [ ] CG-14 [exact]: 문서 상단에 `> 최근 갱신: 2026-04-11 (Phase 2 kaizen research)` 노트 추가

### SC (sprint-contract/SKILL.md)

- [ ] SC-01 [exact]: Gotchas 의 "판정 기준 범주" 항목에서 `[L1]`/`[L2]`/`[L3]` 을 `[exact]`/`[structural]`/`[goal]` 로 교체. 의미(이름/값 일치, 섹션/필드 존재, 목표 달성) 설명은 유지
- [ ] SC-02 [exact]: "미명시 시 기본값 `[structural]`" 으로 문구 갱신 (기존 L2 → structural 등가)
- [ ] SC-03 [structural]: Gotchas 에 "aggregation mode 명시" 항목 신규 추가 — 다수 대상 조건 작성 시 개별/포괄 형식을 명시적으로 선언하도록 경고
- [ ] SC-04 [exact]: References 섹션 유지 — `contract-design-guide.md`, `contract-schema.md`, `feedback-schema.yaml` 3건 모두 존재
- [ ] SC-05 [exact]: 본문 내 모든 `[L1]`/`[L2]`/`[L3]` 문자열 등장 0건
- [ ] SC-06 [exact]: 문서 내 bare code fence 0건

### RS (references/contract-schema.md)

- [ ] RS-01 [exact]: "조건 태그 (Specificity Tag)" 서브섹션 신규 추가 — 계약 조건 포맷에 `[exact]/[structural]/[goal]` 태그를 어떻게 붙이는지 1줄 예시 포함
- [ ] RS-02 [exact]: "aggregation mode" 언급 1건 이상 추가 — 개별 명시 vs 포괄 경로 중 어느 쪽을 선택할지 계약 작성자가 결정한다는 원칙
- [ ] RS-03 [exact]: 스키마 버전 `v1` → `v2` 로 bump, 변경 사항 한 줄 요약
- [ ] RS-04 [exact]: `[L1]`/`[L2]`/`[L3]` 문자열 등장 0건
- [ ] RS-05 [exact]: bare code fence 0건

### I (Integration / Hygiene)

- [ ] I-01 [exact]: `python3 scripts/validate-plugin.py` Total 7 plugins, 7 OK, Exit 0
- [ ] I-02 [exact]: Working tree modified 예외 4항목 외 없음 — 예외: `.harness/sprint-contract.md`, `harness/docs/guides/contract-design-guide.md`, `harness/skills/sprint-contract/SKILL.md`, `harness/references/contract-schema.md`
- [ ] I-03 [exact]: git commit 1건 (`kaizen(phase2-research): ...`) 생성. commit message body 에 리서치 소스 URL 2건 이상 인용
- [ ] I-04 [exact]: Phase 1 변경 (skill-design-guide.md, agent-design-guide.md) 파일을 수정하지 않음 — `git diff HEAD~3 --name-only` 에 두 파일 미포함

## 검증 절차

1. Edit 로 3 개 파일 수정 (contract-design-guide.md, sprint-contract/SKILL.md, contract-schema.md)
2. Grep `\[L[123]\]` 전수 확인 (0건)
3. Grep bare code fence 확인
4. `python3 scripts/validate-plugin.py` 7 OK 확인
5. git add + commit
6. self-audit (Phase 2 서브에이전트는 서브에이전트 스폰 불가 — 최종 QA 는 오케스트레이터에 위임)

## Anti-patterns (절대 하지 마라)

- Phase 1 변경 (skill-design-guide / agent-design-guide) 수정 (I-04)
- `[L1]/[L2]/[L3]` 을 살려두기 (네이밍 충돌 유지)
- `[L1]/[L2]/[L3]` 대신 `[L1-contract]` 같은 prefix 편법으로 해결 시도
- 리서치 출처 없이 "2026 트렌드" 같은 추측성 주장 추가
- sprint-contract 와 qa-evaluator 를 직접 재구현 (harness 내장 사용)
- 스프린트 범위 밖 파일 수정 (validate-plugin 스크립트, 다른 스킬/킷 등)
