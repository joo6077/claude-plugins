# Sprint Contract — Phase 1: 설계 가이드 Kaizen

Generated: 2026-04-24
Feature: kaizen-phase1-design-guides
Scope: `harness/docs/guides/skill-design-guide.md`, `harness/docs/guides/agent-design-guide.md` (2 files only)
Branch: kaizen/2026-04-24

---

## Context

Previous cycle meta-issue: 설계 가이드의 원칙이 한쪽(skill-design-guide §3.5 계약 모호성 방지)에만 있고 다른 쪽(agent-design-guide)에 전수 반영되지 않아 design-kit PH-01 REJECT가 발생했다. 이번 Phase 1은 **원칙 전수성(parity)** 을 구조적으로 보장하고, 글로벌 피드백 61건 REJECT에서 반복 패턴으로 드러난 설계 레벨의 공백을 메운다.

Research sources consulted (3+ required):
1. [Skill Authoring Best Practices — Claude API Docs (2026-04)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
2. [Create custom subagents — Claude Code Docs (2026-04)](https://code.claude.com/docs/en/sub-agents)
3. [anthropics/skills — skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

Research inputs: `.claude/kaizen-input/insights-report.md` (30일 세션), `.claude/kaizen-input/plugin-qa-data.md` (138 QA), `.claude/kaizen-input/reflect-aggregated.md` (1798 reflections).

---

## Success Criteria (binary PASS/FAIL)

### CG — Cross-Guide Parity (원칙 전수성)

- [ ] **CG-01** [exact]: skill-design-guide.md 에 새 섹션 §11 "원칙 전수성 · Cross-Surface Parity Checklist" 가 존재하고, "skill-design-guide 개정 시 agent-design-guide 의 대응 원칙이 있는지 확인" 을 필수 체크리스트 항목으로 명시한다
- [ ] **CG-02** [exact]: agent-design-guide.md 에 동일 섹션 §12 "원칙 전수성 · Cross-Surface Parity Checklist" 가 존재하고, 동일 체크리스트를 에이전트→스킬 방향으로 서술한다
- [ ] **CG-03** [structural]: 두 guide 의 Cross-Surface Parity 섹션이 **동일한 5개 parity item** 을 포함한다 (계약 모호성 방지 · 트리거 키워드 배타성 · 검증 가능한 성공 기준 · rule-by-rule audit · 미검증 항목 정책)

### AP — Ambiguity Prevention (계약 모호성 방지 — PH-01 재발 방지)

- [ ] **AP-01** [exact]: skill-design-guide §3.5 "QA 계약과 1:1 매칭되는 이름을 사용하라" 유지
- [ ] **AP-02** [exact]: agent-design-guide 에 **§3.5 "계약 모호성 방지 — Binary Decidability Pre-Check"** 를 독립 섹션(Gotcha 내부가 아닌 최상위 §)으로 승격한다. 내용은 §10 Gotchas 의 기존 "계약 모호성 방지" bullet 을 확장하여 이진 판정 가능성 검토, `[exact]/[structural]/[goal]` 태그 처리, REJECT 사유 표기 의무를 기술한다

### KE — Keyword Exclusivity (트리거 키워드 배타성 — react-kit RE-02/SK-05 대응)

- [ ] **KE-01** [exact]: skill-design-guide §4 "트리거 키워드 중복 방지 원칙" 이 **substring containment** 규칙을 명시적으로 포함 ("set intersection이 공집합" 뿐 아니라 "어느 키워드도 다른 스킬 키워드의 부분문자열이 아니어야 한다" 명시)
- [ ] **KE-02** [exact]: KE-01 에 실제 REJECT 사례 인용 — react-api "API 연동" ⊂ react-feature "API 연동 화면" 반례를 Bad 블록으로 삽입
- [ ] **KE-03** [structural]: agent-design-guide §3 또는 §10 에 "에이전트 description 도 sibling agent 와 trigger 키워드 set intersection + substring 검사 필요" 1 문단 추가

### CE — Code Example Rules (react-kit DG-01/DG-02 · reflect-kit AP-03 대응)

- [ ] **CE-01** [exact]: skill-design-guide 에 새 섹션 "Code Examples — fenced block 규칙" 존재. 아래 3 원칙 포함:
  - 모든 fenced code block 은 언어 힌트 필수 (빈 fence 금지)
  - SKILL.md 내부 코드 템플릿에 `TODO`, `FIXME`, 미완성 placeholder 금지 (실제로 생성될 코드여야 함)
  - 의사 코드/설명용 예시는 언어 힌트로 `text` 또는 `pseudo` 사용
- [ ] **CE-02** [exact]: CE-01 에 Bad/Good 예시 각 1 쌍 포함 (bare fence vs 언어 힌트, TODO 잔존 vs 실제 코드)

### SC — Sibling-skill Consistency (rust-kit H-01/H-03 대응)

- [ ] **SC-01** [exact]: skill-design-guide 에 새 섹션 "Sibling-Skill Principle Consistency" 존재. 핵심 룰: "한 kit 내 동일 계열 스킬(init/feature/api 등)에 공통 원칙이 적용될 경우, 모든 sibling SKILL.md 의 Gotchas 에 동일 표현으로 등장해야 한다"
- [ ] **SC-02** [exact]: SC-01 에 실제 REJECT 사례 인용 — rust-service 의 "Composition Root 단일화"가 rust-api 에 누락된 H-03 · rust-service 의 "domain event + outbox"가 rust-init/rust-feature 에 누락된 H-01 반례 명시

### PA — Pre-completion Audit (insights 마찰점 #1 "Proactive quality gaps" 대응)

- [ ] **PA-01** [exact]: skill-design-guide §3.6 "검증 가능한 성공 기준" 또는 그 직후에 **"Rule-by-Rule Audit Before Completion"** 원칙 추가. 다음을 포함:
  - 스킬이 규칙 리스트(Gotchas, anti-patterns, contract categories)를 가지면, 산출물 제출 전 각 규칙을 1:1 대조하는 체크 패스를 명시적으로 실행
  - 체크 결과를 리포트(또는 dryrun 출력)로 Gen 자신이 스스로 확인
  - 사용자가 지적할 때까지 기다리는 패턴은 안티패턴

### EA — Enumerate-before-Act (insights 마찰점 #2 "Wrong approach" 대응)

- [ ] **EA-01** [exact]: skill-design-guide §5.5 "Degrees of Freedom" 섹션에 "Low-freedom 영역(토큰 네이밍, Figma 컴포넌트 식별, 스펙 수치)" 은 편집 전 **enumerate-before-act** 를 강제 — 존재하는 토큰/옵션을 먼저 나열하고 사용자 승인/명시된 스펙 대조 후 편집 시작 — 원칙을 1 문단 추가

### UV — Unverified/Degraded-Mode Policy (harness feedback LG-04/DG-04 mcp_server null 대응)

- [ ] **UV-01** [exact]: agent-design-guide §10 (Reviewer/Evaluator 전용 Gotchas) 에 **"Unverifiable 조건 정책"** bullet 추가. 인프라 부재(mcp_server null, 도구 미설치)로 검증 불가한 조건은 (a) `[정적]` 또는 `[미검증]` 마커로 결과 표기 (b) 2건 이상 누적 시 REJECT 규칙 일관 적용 (c) 조용한 PASS 금지 — 3항 필수

### EV — Eval Set Sizing (trigger accuracy)

- [ ] **EV-01** [exact]: skill-design-guide §8.5 "Evaluation-Driven Development" 의 "Trigger Eval Set" 하위 항목이 "20개 쿼리 · should-trigger 8-10 + should-not-trigger 8-10 · near-miss 필수" 를 유지하고, `flutter-toolkit/evals/evals.json` 실제 사례 링크 문장을 보존한다

### ST — Session Truncation Resilience (insights 마찰점 #3 대응)

- [ ] **ST-01** [structural]: skill-design-guide §9 "실전 시작 가이드" 근처에 "Long-Running Skills — Checkpoint Commits" 원칙 1 문단 추가. 긴 멀티페이즈 스킬(kaizen, create-kit 등)은 체크포인트마다 commit + SESSION_LOG 권장, 응답당 300 라인 제한 원칙 명시

### DG — Document Quality Gates (reflect-kit SK-06/AP-03 대응 — 자기 가이드에도 적용)

- [ ] **DG-01** [exact]: 두 guide 모두 수정 후 모든 fenced code block 에 언어 힌트 존재 (bare fence 0건)
- [ ] **DG-02** [exact]: 두 guide 모두 수정 후 신규 섹션에 (작성한) Bad/Good 예시 블록이 최소 1 쌍 이상 포함 (CE-02, KE-02, SC-02 에 해당)

### I — Implementation Hygiene

- [ ] **I-01** [exact]: 변경 후 `git status` 에 `harness/docs/guides/skill-design-guide.md`, `harness/docs/guides/agent-design-guide.md` 2 파일만 modified (+ `.harness/sprint-contract.md` 이 Phase 1 용으로 modified 허용)
- [ ] **I-02** [exact]: 커밋 메시지 `chore(kaizen-phase1): ...` 패턴, kaizen/2026-04-24 브랜치에 1 건 commit
- [ ] **I-03** [exact]: 두 guide 상단 frontmatter `version` 을 `1.1.0` → `1.2.0` 으로 bump, `last_updated` 를 `2026-04-24` 로 갱신

### QA — Post-implementation QA

- [ ] **QA-01** [goal]: harness/agents/qa-evaluator.md 기준으로 본 Sprint Contract 전 조건 이진 판정 수행, APPROVE 획득 (REJECT 시 1 회 재시도)

---

## Anti-patterns (automatic REJECT triggers)

- 범위 밖 파일(`harness/docs/guides/` 외부) 수정
- frontmatter 버전 미갱신
- Bad/Good 예시 없이 원칙만 나열 (CE, KE, SC 해당)
- 미검증 항목 3건 이상
- bare fenced code block 도입 (DG-01 위반)

---

## Out-of-Scope (다음 Phase로 넘김)

- Phase 2 (contract-kaizen) 은 sprint-contract 스킬 + contract-design-guide 개선. 본 가이드 §3.5 / Cross-Surface Parity 의 변경사항을 "계약 설계 원칙" 으로 흡수하는 것은 Phase 2 에서 처리.
- Phase 3 (evaluator-kaizen) 은 qa-evaluator 에이전트의 L3 커버리지 강화 + 미검증 항목 정책을 실행 레벨로 반영. 본 가이드 §10 의 UV-01 원칙을 evaluator 프로세스 단계로 편입하는 것은 Phase 3.

---

## Downstream Deliverables (다음 Phase 주입 신호)

Phase 2, Phase 3 서브에이전트에게 전달할 신규 원칙:
1. **Cross-Surface Parity Checklist** — 계약 설계 가이드 개정 시 evaluator 가이드에도 대응 원칙 존재 여부 필수 확인
2. **Binary Decidability Pre-Check** (agent-design-guide §3.5 신설) — contract-design-guide 에 동일 섹션 존재 보장 필요
3. **Substring-containment 키워드 배타성** — 계약에 keyword-exclusivity 조건 작성 시 substring 포함
4. **Sibling-skill Principle Consistency** — kaizen Phase 4+ (플러그인 개선) 에서 Gotchas 크로스 체크 의무
5. **Unverifiable 조건 정책** — evaluator 가 "미검증 2건 이상 REJECT" 를 guide 에 근거로 포함
