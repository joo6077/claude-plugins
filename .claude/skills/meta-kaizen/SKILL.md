---
name: meta-kaizen
description: >
  kaizen-orchestrator 자체를 리서치 기반으로 개선하는 메타 카이젠 스킬.
  Phase 1~10 은 플러그인/harness 를 개선하지만 orchestrator SKILL.md 는 어느 Phase 에도 포함되지 않아 메타 레벨 사각지대다.
  이 스킬은 이전 사이클 audit-log + LLM agent orchestration 최신 연구를 기반으로 orchestrator SKILL.md 를 개선한다.
  "/meta-kaizen", "오케스트레이터 개선", "meta kaizen" 같은 요청 시 트리거.
  단순 텍스트 수정이나 Phase 내부 조정에는 트리거하지 않는다 — 개별 카이젠 스킬 사용.
argument-hint: "[--dry-run]"
user-invocable: true
---

# Gotchas

1. **Phase 1~10 범위 밖** — 이 스킬은 `.claude/skills/kaizen-orchestrator/SKILL.md` 와 그 `references/` 만 개선 대상으로 삼는다. 플러그인 스킬, harness 스킬, 계약 가이드, qa-evaluator 는 건드리지 마라 — 그것들은 각 카이젠 스킬이 개선한다.
2. **`<!-- AUTO:plugin_phases:begin -->` ~ `<!-- AUTO:plugin_phases:end -->` 마커 영역 직접 편집 금지** — 이 영역은 `scripts/sync-orchestrator.py` 가 `marketplace.json` 을 기반으로 자동 생성한다. 이 스킬은 마커 바깥의 Step 0, Step 0.5, Step 11, Step 11.5, Step 11.6, Step 12, Gotchas, Process 공통 패턴, Post-Kaizen Checklist 섹션만 수정한다.
3. **리서치 소스는 공식 문서/학술 논문 우선** — Anthropic skill authoring 가이드, arxiv LLM agent orchestration 논문, Claude Code plugin 공식 가이드를 1순위로. 블로그/트위터는 2순위.
4. **audit-log 는 read-only 입력** — `.harness/.meta/orchestrator-audit-log.md` 는 이 스킬이 읽고 판단 근거로 쓰지만 직접 수정하지 마라. 수정은 `scripts/append-audit-log.py` 로만.
5. **Self-reference 방지** — 이 스킬이 orchestrator SKILL.md 를 개선하면, 다음 사이클 Step 0.5 가 이 변경을 detect 한다. 너무 자주 돌리면 무한 개선 루프 위험 — 주 1회 이상 돌리지 마라.
6. **Pre-flight 이전 실행** — 이 스킬은 `/kaizen-orchestrator` 실행보다 **먼저** 돌아야 한다. 다음 사이클 Step 0.5 가 개선된 SKILL.md 를 읽을 수 있도록.
7. **bare fenced code block 0 건** — SKILL.md 수정 시 모든 fence 에 언어 힌트 (`text`, `bash`, `yaml`) 필수.

# Process

## Step 1: 전제 조건 확인

1. `.harness/.meta/orchestrator-audit-log.md` 존재 확인 — 없으면 "첫 실행" 으로 간주
2. `python3 scripts/validate-plugin.py` 7 OK 확인 — FAIL 이면 중단
3. `python3 scripts/sync-orchestrator.py --check-only` exit 0 확인 — drift 있으면 먼저 `python3 scripts/sync-orchestrator.py` 실행

## Step 2: 이전 사이클 meta-feedback 로드

`.harness/.meta/orchestrator-audit-log.md` 를 Read 로 읽고 다음을 추출:

- 가장 최근 엔트리의 "Post-Kaizen Checklist failures" 목록
- "Orchestrator SKILL.md manual edits" 목록 (라인 수 + 이유)
- "Next-cycle watchlist" 항목

여러 엔트리가 있으면 최근 3 개까지만 읽는다 (이전 이슈가 해결됐는지 검증용).

## Step 3: 리서치 (필수)

아래 소스를 조회하여 최신 LLM agent orchestration 패턴을 확보:

### 1) Context7 — Anthropic / Claude Code 공식 문서

- `mcp__claude_ai_Context7__resolve-library-id` 쿼리: "anthropic skill" / "claude code plugin"
- 성공 시 `query-docs` 로 skill authoring 최신 best practices 추출

### 2) Codex (codex-rescue) 위임 — 학술 / 커뮤니티

`subagent_type: codex:codex-rescue` 로 아래 주제 리서치:

- "LLM agent orchestration 2026 latest patterns — multi-phase pipeline, self-improvement, meta-learning"
- "agentic workflow authoring best practices 2026"
- "LLM-based code review pipeline orchestration research papers"
- "multi-agent system self-audit patterns"

URL/arxiv 링크 필수. Codex 40 초 무응답 시 WebSearch fallback.

## Step 4: GAP 분석

이전 사이클 audit-log 의 meta-issue + 리서치 결과를 대조하여 orchestrator SKILL.md 의 개선 포인트를 추출:

- **반복 발생 이슈**: audit-log 최근 3 엔트리에서 동일 meta-issue 가 반복되었나? → 해당 Step 의 Gotchas 강화
- **최신 패턴 미반영**: 리서치에서 발견한 2026 orchestration 패턴이 SKILL.md 에 없나? → 신규 Step / 서브섹션 추가
- **Post-Kaizen Checklist 항목 부족**: 이전 사이클에서 특정 자동화가 누락됐는데 체크리스트에 없나? → 체크리스트 항목 추가

## Step 5: Sprint Contract DRAFT

`.harness/sprint-contract.md` 를 `harness:sprint-contract` 스킬로 생성. 범위는 orchestrator SKILL.md + references/ 파일만. 계약 조건은 각 개선 포인트별 `[exact]/[structural]/[goal]` 태그로.

## Step 6: 개선 적용

1. orchestrator SKILL.md 를 Edit 로 수정 (AUTO 마커 영역 피해서)
2. 필요 시 `.claude/skills/kaizen-orchestrator/references/*.md` 갱신
3. bare fence 0 건 유지

## Step 7: Self-audit + 독립 QA

1. `python3 scripts/validate-plugin.py` 7 OK
2. `python3 scripts/sync-orchestrator.py --check-only` drift 없음 (수정이 AUTO 영역 침범 안 함)
3. `harness:qa-evaluator` 서브에이전트 spawn 하여 독립 평가
4. REJECT 시 수정 후 재평가 최대 3 회

## Step 8: git commit

- commit prefix: `meta-kaizen: <요약>`
- body 에 리서치 URL / 개선 근거 / audit-log 반영 항목 명시

## Step 9: audit-log 엔트리 자동 append

`scripts/append-audit-log.py --cycle-id meta-kaizen-<date>` 로 이번 실행 자체도 audit-log 에 기록. 다음 사이클 Step 0.5 가 이를 인지한다.

# References

- `.claude/skills/kaizen-orchestrator/SKILL.md` — 개선 대상
- `.harness/.meta/orchestrator-audit-log.md` — 입력 자료 (read-only)
- `scripts/sync-orchestrator.py` — AUTO 영역 동기화 스크립트
- `scripts/append-audit-log.py` — 실행 후 append
- `scripts/validate-plugin.py` — 회귀 검증
- `harness/docs/guides/skill-design-guide.md` — 스킬 작성 원칙
- `harness/docs/guides/agent-design-guide.md` — 에이전트 작성 원칙
