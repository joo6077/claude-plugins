# Sprint Contract — Phase 4 Kaizen Research Mode (Harness)

Feature: harness 지원 스킬 + .harness/project.yaml + 지원 문서 2026 QA 자동화 트렌드 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1~3 는 skill/agent design guide (commit 4587154), contract-design-guide + sprint-contract (commit ba2b8d9), qa-evaluation-guide + qa-evaluator (commit 21203d8) 를 2026 최신 리서치 기준으로 정비했다. Phase 4 는 sprint-contract 와 qa-evaluator 를 **제외한** harness 의 나머지 표면 — init, create-skill, create-agent, harness-kaizen, contract-kaizen, evaluator-kaizen 스킬 + feedback-schema.yaml + .harness/project.yaml + .gitignore — 를 2026 QA 자동화 트렌드에 맞춰 갱신한다.

데이터 풀 (`.harness/.meta/kaizen-data-pool.md`) 의 §5 validate-plugin 7 OK baseline 과 §1 improvement suggestions 중 아래 항목이 Phase 4 범위:

1. `scripts/__pycache__/` → `.gitignore` 미등록 (improvement 2026-04-11)
2. feedback-schema 누적 분석 필드 부재 — 동일 진단 반복/리그레션 연결 구조 없음
3. create-skill / create-agent 에 validate-plugin 연동 지시 없음 (kaizen 3개에는 이미 있음)
4. init SKILL.md 에 스택 자동 감지 후 validate-plugin baseline 권장 없음
5. harness-kaizen Process 가 contract/evaluator kaizen 대비 피드백 triage 구체성 부족

리서치 insight (2026 최신):

- **Skill authoring best practices** (Anthropic 공식) — description 은 "무엇 + 언제" 양쪽 포함, 3인칭, negative trigger 명시, 1500-2000 words 타깃
- **Trigger collision detection** (skills-best-practices, mgechev) — description 에 "Don't use for X" 패턴 명시적 권장
- **Feedback-in-the-loop = 2026 breakthrough** (GrowthBook, Martin Fowler) — 누적 피드백 기반 패턴 감지가 agentic coding 의 차세대 돌파구
- **Agentic regression detection** (Sauce Labs, QA Wolf, ContextQA) — 히스토리컬 test data 분석으로 defect 예측, 다음 사이클 "스마트화"
- **Plan-action drift detection** (AgentFixer, arxiv 2603.29848) — agent 가 role specification 에서 이탈하는지 validation layer 필요

## 리서치 소스 (URL 필수)

1. [Skill authoring best practices — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — description 3인칭, "언제 사용" 명시
2. [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills) — SKILL.md 구조 공식 가이드
3. [How to create custom Skills — Claude Help Center](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) — description 선택 메커니즘 설명
4. [Anthropic official skills repo — anthropics/skills](https://github.com/anthropics/skills) — 공식 예제 (PDF, Excel 스킬 description 패턴)
5. [skills-best-practices — mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) — negative trigger, LLM isolation test
6. [AgentFixer — arxiv 2603.29848](https://arxiv.org/html/2603.29848) — 15 failure detection tools + 2 RCA modules
7. [Feedback Loops Are the Next Breakthrough in Agentic Coding — GrowthBook](https://blog.growthbook.io/feedback-loops-are-the-next-breakthrough-in-agentic-coding/) — 누적 피드백 루프의 2026 중요성
8. [Humans and Agents in Software Engineering Loops — Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html) — loop 설계 패턴
9. [3 Strategic QA Trends for 2026 — Sauce Labs](https://saucelabs.com/resources/blog/beyond-pass-fail-3-strategic-trends-that-will-define-qa-in-2026) — agentic regression, pattern-based defect prediction
10. [Agentic Testing Complete Guide 2026 — vtestcorp](https://vtestcorp.com/insights/agentic-testing-the-complete-guide-to-ai-powered-software-testing-in-2026/) — test selection model 누적 학습
11. [AI in Software Testing 2026 — ContextQA](https://contextqa.com/blog/ai-in-software-testing/) — git history + telemetry 기반 regression 감지
12. [2026 Software Testing Trends — CloudQA](https://cloudqa.io/2026-software-testing-trends-the-shift-from-scripted-to-agentic-ai/) — scripted → agentic shift

## Categories

- **GI** (Gitignore) — 레포 위생
- **PY** (project.yaml) — .harness 설정
- **FS** (Feedback Schema) — feedback-schema.yaml 누적 분석 필드
- **CS** (Create Skill) — create-skill SKILL.md
- **CA** (Create Agent) — create-agent SKILL.md
- **IN** (Init) — init SKILL.md
- **HK** (Harness Kaizen) — harness-kaizen SKILL.md
- **CK** (Contract Kaizen) — contract-kaizen SKILL.md
- **EK** (Evaluator Kaizen) — evaluator-kaizen SKILL.md
- **I** (Integrity) — Regression / validate-plugin

## Conditions (22)

### GI — Gitignore

- **GI-01** `[exact]` `.gitignore` 파일에 `scripts/__pycache__/` 라인이 exact string 으로 존재한다. 기존 3 줄(`node_modules/`, `test-results/`, `playwright-report/`) 은 보존한다. `git status --short` 실행 시 `?? scripts/__pycache__/` 가 untracked 로 더 이상 나타나지 않는다.
- **GI-02** `[structural]` `.gitignore` 파일이 최소 4 줄 이상이며 빈 줄로 끝나지 않는 line-ending drift 방지 (LF, POSIX 호환).

### PY — Project YAML

- **PY-01** `[goal]` `.harness/project.yaml` 의 `anti_patterns` 배열에 Phase 1~3 에서 발견된 최소 1 개의 신규 anti-pattern 이 추가된다. 예: bare code fence (```` ``` ```` 단독), frontmatter 필수 필드 누락 패턴. 기존 AP-01, AP-02 는 보존한다.
- **PY-02** `[exact]` `trigger.always` 배열에 `"kaizen"` 키워드가 exact string 으로 존재한다 (kaizen-orchestrator 실행 시 자동 트리거 보장).

### FS — Feedback Schema

- **FS-01** `[goal]` `harness/references/feedback-schema.yaml` 주석 블록에 누적 분석 필드 3 종 (`repeat_count`, `first_seen_at`, `regression_link`) 의 의미와 용도가 YAML 주석으로 명시된다. 기존 schema_version: 1 을 보존하되, 주석에 "v1 extension (optional)" 로 표기한다.
- **FS-02** `[structural]` `example:` 블록에 위 3 종 필드 중 최소 1 개가 실제 예시 값과 함께 포함된다 (validation 하위 호환성 유지 — save-feedback.sh 의 required 리스트는 변경 금지).

### CS — Create Skill

- **CS-01** `[goal]` `harness/skills/create-skill/SKILL.md` Process 4 단계 "SKILL.md 작성" 에 **negative trigger 명시적 요구** 항목이 추가된다 — 리서치 근거: skills-best-practices (mgechev) 와 Anthropic official docs.
- **CS-02** `[goal]` Process 5 단계 "검증" 체크리스트에 **validate-plugin 연동** 항목 추가 — 생성 직후 `python3 scripts/validate-plugin.py <plugin-name>` 실행하여 V1/V4/V5/V6 통과 확인. 리서치 근거: claude-plugin-validation 스킬 + drift detection.
- **CS-03** `[structural]` Gotchas 섹션에 **description 3인칭 일관성** 관련 Gotcha 최소 1 개 추가 (리서치 근거: Anthropic best practices "Always write in third person").
- **CS-04** `[exact]` Gotchas 섹션에 "negative trigger" 문자열 또는 "비트리거" 문자열이 최소 1 회 등장하여 본문에서 Gotcha 로 명시된다.

### CA — Create Agent

- **CA-01** `[goal]` `harness/skills/create-agent/SKILL.md` Process 5 단계 "검증" 체크리스트에 validate-plugin 연동 항목 추가 (CS-02 와 동일 근거).
- **CA-02** `[goal]` Gotchas 섹션에 **frontmatter drift 방지** Gotcha 추가 — `tools`, `model` 필드는 V1 검증 대상이며 누락 시 에이전트가 invisible 처리됨. 리서치 근거: LLM Model Drift (byaiteam.com 2025-12-30) + Anthropic YAML frontmatter 요구사항.
- **CA-03** `[structural]` Process 4 단계 "에이전트 파일 생성" 템플릿의 frontmatter 에 `tools`, `model` 필드가 필수 라는 주석 또는 설명이 존재한다.

### IN — Init

- **IN-01** `[goal]` `harness/skills/init/SKILL.md` "실행 후 안내" 섹션에 `scripts/validate-plugin.py` baseline 실행 권장 항목 추가 (플러그인 모노레포 환경일 때 한정). 리서치 근거: agentic regression detection 에서 baseline snapshot 확보 권장 (Sauce Labs 2026).
- **IN-02** `[structural]` Gotchas 섹션에 최소 1 개의 "v1 schema 하위 호환" 또는 "기존 .harness 덮어쓰기 금지" 관련 Gotcha 유지 (기존 `.harness/` 덮어쓰기 금지 Gotcha 는 보존).

### HK — Harness Kaizen

- **HK-01** `[goal]` `harness/skills/harness-kaizen/SKILL.md` 의 Step 2 COLLECT 또는 새 Step "Triage" 에 **글로벌 피드백 패턴 분석** 절차가 추가된다 — contract-kaizen/evaluator-kaizen 의 Step 2 Triage 와 동일한 수준의 구체성: `bash harness/scripts/feedback-path.sh` 실행 → 최근 N 건 YAML 파싱 → 반복 진단 패턴 식별. 리서치 근거: feedback-in-the-loop 2026 breakthrough.
- **HK-02** `[exact]` Gotchas 섹션에 "피드백 0건" 또는 "리서치 전용 모드" 문자열이 최소 1 회 등장하여 contract-kaizen/evaluator-kaizen 과 동일한 fallback 규칙을 공유한다.
- **HK-03** `[structural]` "개선 대상 범위" 표에 `../../references/feedback-schema.yaml` 행이 추가된다 (Phase 4 에서 본 파일이 개선 대상에 포함되었음을 명시).

### CK — Contract Kaizen

- **CK-01** `[goal]` `harness/skills/contract-kaizen/SKILL.md` Step 2 Triage 의 "패턴 분석" 불릿에 **regression_link 활용** 또는 **누적 반복 횟수 기반 우선순위** 개념이 1 개 이상 추가된다 (FS-01 의 신규 필드와 연계). 리서치 근거: 2026 agentic regression detection (ContextQA, Sauce Labs).
- **CK-02** `[structural]` Gotchas 섹션 줄 수가 기존 대비 최소 0 이상 유지되며, 기존 "피드백 0건 → 리서치 전용" Gotcha 는 보존된다.

### EK — Evaluator Kaizen

- **EK-01** `[goal]` `harness/skills/evaluator-kaizen/SKILL.md` Step 2 Triage 의 "패턴 분석" 불릿에 CK-01 과 동일한 누적 분석 필드 활용 개념 추가.
- **EK-02** `[structural]` 기존 "qa-evaluator 자체를 개선하는 Phase 에서 QA 는 현재(구) 버전 evaluator 로 수행한다" Gotcha 는 반드시 보존된다.

### I — Integrity

- **I-01** `[goal]` `python3 scripts/validate-plugin.py` 실행 결과 7 OK 유지 (Total: 7 plugins, 7 OK, Exit 0).
- **I-02** `[goal]` `python scripts/sync-docs.py --check-only` 실행 시 exit 0 (harness README 동기화 상태 유지).
- **I-03** `[structural]` Phase 1~3 에서 수정한 파일 목록 (`skill-design-guide.md`, `agent-design-guide.md`, `sprint-contract/SKILL.md`, `contract-design-guide.md`, `contract-schema.md`, `qa-evaluation-guide.md`, `qa-evaluator.md`) 은 Phase 4 커밋에서 modified 0 건.
- **I-04** `[exact]` Phase 4 커밋 메시지는 `kaizen(phase4-research):` prefix 로 시작하며, 리서치 소스 URL 이 최소 3 개 이상 포함된다.

## Aggregation

- 모든 조건은 `[enumerated]` 기본. 리스트성 검증(I-03) 만 `[collective]` — 모든 파일이 modified 0 이어야 함.

## Anti-patterns

- **AP-P4-01** 리서치 URL 없이 주장만 반영 — 3-gate verification 위반
- **AP-P4-02** Phase 1~3 파일 (예외 목록) 을 수정 — 범위 위반
- **AP-P4-03** feedback-schema.yaml 의 `schema_version` 을 2 로 올리면 save-feedback.sh 호환성 깨짐 — v1 유지 필수
- **AP-P4-04** bare code fence 삽입 (validate-plugin V6 FAIL)
- **AP-P4-05** `.gitignore` 에 `scripts/__pycache__/` 가 아닌 넓은 범위 (`**/__pycache__/`, `*.pyc`) 로 대체 — 데이터 풀이 지정한 exact 경로 위반

## Complexity

**medium** — 6 스킬 파일 + 1 schema + 1 project.yaml + 1 .gitignore = 9 파일 범위. 본문 추가/수정 위주, 아키텍처 변경 없음.

## Success Criteria

22/22 조건 PASS, validate-plugin 7 OK, sync-docs --check-only exit 0, Phase 1~3 파일 modified 0, commit hash 기록.
