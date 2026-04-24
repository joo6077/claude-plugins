# Sprint Contract — Kaizen Phase 4 (harness 지원 스킬)

Feature: harness 플러그인 지원 스킬에 Phase 1~3 신규 원칙 전수
Date: 2026-04-24
Scope: `harness/skills/init`, `harness/skills/create-skill`, `harness/skills/create-agent`, `harness/skills/contract-kaizen`, `harness/skills/evaluator-kaizen`, `harness/skills/harness-kaizen`
Scope-out: `harness/skills/sprint-contract/*` (Phase 2), `harness/agents/qa-evaluator.md` (Phase 3), `harness/docs/guides/*` (Phase 1~3), `harness/references/contract-schema.md` (Phase 2)

## Goal

Phase 1~3에서 skill-design-guide/agent-design-guide/contract-design-guide/qa-evaluation-guide에 추가된 신규 원칙을 **스캐폴더(create-skill, create-agent)와 카이젠 스킬(contract/evaluator/harness-kaizen)**이 자동으로 따르도록 Gotchas/Process를 업데이트한다. 이로써 다음 Phase 5~10의 플러그인 카이젠이 일관된 원칙 하에 수행된다.

## Completion Conditions

### CS (Create-Skill 전수)
- [ ] CS-01: `harness/skills/create-skill/SKILL.md`의 Gotchas에 **Cross-Surface Parity 체크** 항목이 추가되어, 새 스킬 생성 시 상위 가이드(skill-design-guide §11)와의 정합성을 확인하도록 명시한다. 키워드: "Cross-Surface Parity", "skill-design-guide §11" 등장.
- [ ] CS-02: Gotchas에 **Binary Decidability 검증 가능 성공 기준** 항목이 추가되어, 새 스킬의 Process가 계약-1:1-매칭 가능한 검증 기준을 포함해야 함을 명시한다 (skill-design-guide §3.5 참조).
- [ ] CS-03: Gotchas에 **Sibling-Skill 원칙 일관성** 항목이 추가되어, 형제 스킬이 이미 존재하면 동일 Gotchas 패턴을 enumerated Grep으로 비교해야 함을 명시한다 (§8.8).
- [ ] CS-04: Gotchas에 **Code Examples 품질 규칙** 항목이 추가되어, fenced code block 언어 힌트 필수 + TODO/placeholder 금지를 명시한다 (§8.7).
- [ ] CS-05: Gotchas에 **Enumerate-before-Act** 항목이 추가되어, Process가 low-freedom 영역(스캐폴딩/생성)에서 선-목록화 후-편집 패턴을 따르도록 명시한다 (§5.5).
- [ ] CS-06: Step 5 검증 체크리스트에 "skill-design-guide §11 parity 5개 항목 확인" 항목이 추가된다.

### CA (Create-Agent 전수)
- [ ] CA-01: `harness/skills/create-agent/SKILL.md`의 Gotchas에 **Binary Decidability Pre-Check** 항목이 추가되어, 평가 에이전트 계열(reviewer)의 경우 모호 조건 감지 프로토콜 포함을 명시한다 (agent-design-guide §3.5).
- [ ] CA-02: Gotchas에 **Unverifiable 조건 정책 3항**이 추가되어, mcp_server:null 등 검증 불가 상황에서 에이전트가 `[미검증]` 마커로 보고하고 2건 이상이면 자동 REJECT하도록 명시한다 (§10).
- [ ] CA-03: Gotchas에 **Cross-Surface Parity (agent-design-guide §12)** 항목이 추가된다.
- [ ] CA-04: Step 5 검증 체크리스트에 "agent-design-guide §12 parity 4개 항목 확인" 항목이 추가된다.

### CK (Contract-Kaizen)
- [ ] CK-01: `harness/skills/contract-kaizen/SKILL.md`의 Step 5 (GAP 분석)에 **Cross-Surface Parity 확인** 하위 항목이 추가되어, 계약 가이드 변경 시 skill-design-guide/agent-design-guide/qa-evaluation-guide로의 전수 필요성을 체크한다.
- [ ] CK-02: Gotchas에 **`/insights` 3대 마찰점 반영 체크리스트**가 추가되어 카이젠 개선 제안 시 Proactive quality gaps / Wrong approach / Session truncation을 검토하도록 명시한다.

### EK (Evaluator-Kaizen)
- [ ] EK-01: `harness/skills/evaluator-kaizen/SKILL.md`의 Step 5에 **Cross-Surface Parity 확인** 하위 항목이 추가된다 (qa-evaluation-guide §Cross-Surface Parity 참조).
- [ ] EK-02: Gotchas에 **L3 Coverage Honesty 회귀 체크** 항목이 추가되어, 최근 10건 피드백에서 `[샘플링-N/전체-M]` 태그 누락률이 30% 초과하면 우선 개선 대상으로 승격하도록 명시한다.
- [ ] EK-03: Gotchas에 `/insights` 3대 마찰점 반영 체크리스트 추가.

### HK (Harness-Kaizen)
- [ ] HK-01: `harness/skills/harness-kaizen/SKILL.md`의 Gotchas에 **`/insights` 3대 마찰점 반영 체크리스트** 항목이 추가된다.
- [ ] HK-02: Gotchas에 **Cross-Phase 범위 제외** 항목이 보강되어 sprint-contract SKILL.md / qa-evaluator.md / 4개 가이드 / contract-schema.md를 명시적으로 scope_out으로 열거한다 (기존 Gotcha 강화).

### IN (Init)
- [ ] IN-01: `harness/skills/init/SKILL.md`의 "실행 후 안내"에 신규 원칙 참조 가이드(Binary Decidability, Cross-Surface Parity)를 짧게 언급하여, 초기화 후 사용자가 관련 가이드를 읽도록 유도한다.

### CMT (Commit & Validation)
- [ ] CMT-01: 변경을 단일 커밋 `chore(kaizen-phase4): ...`로 `kaizen/2026-04-24` 브랜치에 기록한다.
- [ ] CMT-02: `python3 scripts/validate-plugin.py harness` 실행 시 V1~V7 전부 OK.
- [ ] CMT-03: 범위 밖 파일(sprint-contract SKILL.md, qa-evaluator.md, 4개 가이드, contract-schema.md, feedback-schema.yaml)은 전혀 수정되지 않음을 `git diff --stat`으로 확인한다.

## Anti-patterns (즉시 REJECT)

- 범위 밖 파일 수정 (sprint-contract, qa-evaluator, guides, schema)
- Phase 1~3 guide 원본을 복붙 (참조만 하라)
- 기존 Gotchas 삭제 또는 재작성 (append-only)
- 출처 없는 주장 추가

## Verification Method

- **L3**: `grep -n "Cross-Surface Parity\|Binary Decidability\|Sibling\|Enumerate-before-Act\|Rule-by-Rule" harness/skills/{init,create-skill,create-agent,contract-kaizen,evaluator-kaizen,harness-kaizen}/SKILL.md`로 키워드 존재 확인
- **L3**: `python3 scripts/validate-plugin.py harness` V1~V7 모두 OK
- **L3**: `git diff --stat main..HEAD -- harness/` 결과에서 scope_out 파일 미포함 확인
