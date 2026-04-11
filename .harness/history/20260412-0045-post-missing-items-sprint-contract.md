---
feature: "카이젠 미처리 항목 일괄 처리 + 오케스트레이터 자체 개선"
created: "2026-04-11 23:50"
complexity: "복잡"
conditions: 28
---

# Sprint Contract — Post-Kaizen Missing Items

## Context

이전 카이젠 research-mode rerun (Phase 1~10 + Final, 27 commits on `kaizen/2026-04-11-research`) 후 사용자가 구조적 누락을 지적했다:

1. **docs-site HTML 페이지 재생성이 파이프라인에 없음** — 84개 HTML이 카이젠 전 상태로 멈춤
2. **per-kit research-log 가 존재 시만 갱신" 조문이라 영구 누락** — `docs/{backend,infra,rust,react,flutter}/research-log.md` 없음
3. **flutter-changelog/flutter-research-log 갱신 누락** — Step 12에 명시됐는데 이번 세션에 빠뜨림
4. **kaizen-failure-count.yaml 최신 상태 미반영** — Phase 7~10 엔트리 없음, iter 흐름 미기록
5. **글로벌 피드백 정리 미실행** — Step 11 뒤 조문 있지만 트리거 없음
6. **evals/evals.json 갱신 점검 조문 부재**
7. **가장 근본적 — 카이젠 오케스트레이터 SKILL.md 자체에 "완료 체크리스트" 가 없어서 매번 놓칠 가능성**

본 스프린트는 위 7개를 일괄 처리하고, 오케스트레이터 SKILL.md를 개선하여 다음 카이젠부터 자동 포함되도록 한다.

## 영향 범위

수정 대상:

- `.claude/skills/kaizen-orchestrator/SKILL.md` (자체 개선)
- `docs/kaizen/flutter-changelog.md`
- `docs/kaizen/flutter-research-log.md`
- `docs/backend/research-log.md` (신규)
- `docs/infra/research-log.md` (신규)
- `docs/rust/research-log.md` (신규)
- `docs/react/research-log.md` (신규)
- `docs/flutter/research-log.md` (신규)
- `docs/harness/skill-design.html` (재생성)
- `docs/harness/agent-design.html` (재생성)
- `docs/harness/contract-design.html` (재생성)
- `docs/harness/contract-schema.html` (재생성)
- `docs/harness/qa-evaluation.html` (재생성)
- `docs/harness/feedback-system.html` (재생성)
- `.harness/.meta/kaizen-failure-count.yaml`
- `.harness/.meta/cleanup-log.yaml` (신규)

**수정 금지 (Phase 1~10 완료 파일):**

- harness/skills/, harness/docs/guides/, harness/agents/, harness/references/
- flutter-toolkit/skills/, flutter-toolkit/agents/, flutter-toolkit/references/
- design-kit/skills/, design-kit/agents/, design-kit/references/
- backend-kit/skills/, backend-kit/agents/, backend-kit/references/
- infra-kit/skills/, infra-kit/agents/, infra-kit/references/
- rust-kit/skills/, rust-kit/agents/, rust-kit/references/
- react-kit/skills/, react-kit/agents/, react-kit/references/
- 모든 plugin.json (버전 재 bump 금지)
- `.claude-plugin/marketplace.json`

## 완료 조건

### OR (kaizen-orchestrator 자체 개선)

- [ ] OR-01 [structural]: `.claude/skills/kaizen-orchestrator/SKILL.md` 에 **"Step 11.5: docs-site 재생성"** 신규 섹션 추가. 각 Phase 에서 변경된 `.md` 소스 파일(harness/docs/guides/, harness/references/, docs/{backend,infra,rust,react,flutter}/, design-kit/docs/design/, flutter-toolkit/references/)이 있으면 대응 HTML 페이지를 `/docs-site` 스킬로 재생성하라는 지시 포함. 매핑 테이블 (플러그인 → 소스 경로 → 출력 경로) 포함.
- [ ] OR-02 [structural]: Step 12 PR 생성 섹션에 **"per-kit research-log 자동 생성"** 조문 추가. `docs/{backend,infra,rust,react,flutter}/research-log.md` 가 존재하지 않으면 해당 Phase subagent 가 **신규 생성** 하도록 명시 ("존재 시" 문구 제거).
- [ ] OR-03 [structural]: Step 12 에 **"evals 갱신 체크"** 조문 추가. 각 플러그인 evals/evals.json 이 이번 Phase 변경 스킬 목록과 정합하는지 점검하고, 스킬이 새로 추가/삭제되었으면 evals 도 갱신.
- [ ] OR-04 [structural]: Step 12 에 **"kaizen-failure-count.yaml 업데이트"** 조문 추가. 각 Phase 완료 후 해당 phase 카운터 0 으로 리셋, last_updated 갱신. Phase 7~10 엔트리가 파일에 없으면 추가.
- [ ] OR-05 [structural]: Step 11 "Final — 전체 정합성 검증" 다음에 **"Step 11.5: 글로벌 피드백 정리"** 섹션을 승격 (현재는 "글로벌 피드백 정리" 가 Step 12 전 본문에 있으나 명확한 Step 이 아님). 실행 명령: `bash harness/scripts/feedback-path.sh` → 6개월 초과 삭제 → 500개 초과 oldest-first 삭감 → `.harness/.meta/cleanup-log.yaml` 기록.
- [ ] OR-06 [structural]: Step 12 말미에 **"완료 체크리스트 (Post-Kaizen Checklist)"** 섹션 신규 추가. 8개 이상 항목 (plugin.json bump / marketplace.json / sync-docs / changelog / research-log / per-kit research-log / docs-site / flutter-changelog / flutter-research-log / evals / failure-count / feedback cleanup / validate-plugin 7 OK / Phase 간 scope 격리) 을 체크박스로 나열. 다음 카이젠에서 subagent 가 이 체크리스트를 반드시 통과한 뒤에만 PR 생성 가능.
- [ ] OR-07 [exact]: OR-01 ~ OR-06 의 변경이 **하나의 섹션에 응집** 되지 않고 SKILL.md 원래 Step 구조를 유지하며 자연스럽게 삽입됨. 기존 Step 번호 (Step 0~12) 를 재번호하지 말고 **Step 11.5, Step 11.6** 같은 소수점 번호 또는 소절로 추가.
- [ ] OR-08 [exact]: `.claude/skills/kaizen-orchestrator/SKILL.md` 본문 내 bare fenced code block (` ``` ` 뒤 개행) 0 건.

### OR-meta (오케스트레이터 자체 개선 자동화 + 킷 자동 반영)

- [ ] OR-09 [exact]: `scripts/sync-orchestrator.py` 신규 작성. 기능: (1) `.claude-plugin/marketplace.json` 읽어 플러그인 목록 추출 (2) 각 플러그인에 대해 Phase N 섹션 (Step 5 ~ Step N) 을 자동 생성 (3) `kaizen-orchestrator/SKILL.md` 의 `<!-- AUTO:plugin_phases:begin -->` ~ `<!-- AUTO:plugin_phases:end -->` 마커 사이 영역을 교체. (4) `--check-only` 모드 지원 (drift 감지). harness 플러그인은 Phase 1~4 고정이므로 자동 생성 영역에 포함하지 않음. Python 실행 가능 (`python3 scripts/sync-orchestrator.py` 정상 exit 0).
- [ ] OR-10 [structural]: `.claude/skills/kaizen-orchestrator/SKILL.md` 에 `<!-- AUTO:plugin_phases:begin -->` / `<!-- AUTO:plugin_phases:end -->` 마커 삽입. 마커 사이에 현재 Phase 5~10 (flutter-toolkit, design-kit, backend-kit, infra-kit, rust-kit, react-kit) 이 `sync-orchestrator.py` 로 생성된 형식으로 들어감. 기존 본문과 diff 가 최소화되도록 컨텐츠 보존.
- [ ] OR-11 [structural]: `.claude/skills/kaizen-orchestrator/SKILL.md` 에 **Step 0.5: Orchestrator Self-Audit** 섹션 신규 추가. 이 단계는 Step 0 (Pre-flight) 직후, Phase 1 직전에 실행. 동작:
  1. `.harness/.meta/orchestrator-audit-log.md` 읽기 — 이전 사이클의 수동 개입 이력 확인
  2. 이력이 있으면 "지난 사이클에서 발생한 meta-issue 를 이번 사이클에서 재검증하라" 를 subagent 에 지시
  3. `python3 scripts/sync-orchestrator.py --check-only` 실행. drift 있으면 사용자 에스컬레이션
  4. drift 없으면 Phase 1 로 진행
- [ ] OR-12 [exact]: `.harness/.meta/orchestrator-audit-log.md` 신규 생성. 2026-04-11 엔트리에 이번 사이클에서 수동 개입한 내용 3+ 건 기록 (docs-site 누락, per-kit research-log 영구 누락, flutter-changelog 갱신 누락, OR-01~OR-08 수동 추가, OR-09~OR-15 추가).
- [ ] OR-13 [exact]: `.claude/kaizen-orchestrator/SKILL.md` Gotchas 에 "AUTO:plugin_phases 마커 영역 직접 편집 금지 — `scripts/sync-orchestrator.py` 만 수정" 항목 추가.
- [ ] OR-14 [structural]: `.claude/settings.json` PostToolUse 훅에 `.claude-plugin/marketplace.json` 변경 감지 조문 추가. 조문 형태: `marketplace.json` 을 Edit/Write 할 때 `python3 scripts/sync-orchestrator.py --check-only` 자동 실행 → drift 있으면 사용자에게 알림. settings.json 구조 유효 (JSON parse OK).
- [ ] OR-15 [exact]: `.claude/skills/kaizen-orchestrator/SKILL.md` 의 Phase 의존성 다이어그램 (line 39 부근) 에 **"Step 0.5: Orchestrator Self-Audit"** 가 Phase 1 이전 위치로 추가됨.

### FL (flutter-changelog / flutter-research-log 갱신)

- [ ] FL-01 [exact]: `docs/kaizen/flutter-changelog.md` 에 **"## [2026-04-11] - Phase 5 research-mode kaizen"** 엔트리 추가. 내용에 Riverpod 3.0 / Freezed 3.0 / go_router StatefulShellRoute / Flutter 3.29 / Makefile monorepo 감지 / widget-inspector Props 번들링 5개 이상 항목 포함. last_updated 필드를 `2026-04-11` 로 갱신.
- [ ] FL-02 [exact]: `docs/kaizen/flutter-research-log.md` 에 **"## [2026-04-11] - Phase 5 research sources"** 엔트리 추가. pub.dev / riverpod.dev / docs.flutter.dev / apps fit-pal ground truth 등 최소 6 개 URL 인용. last_updated `2026-04-11`.

### RL (per-kit research-log 5 개 신규 생성)

- [ ] RL-01 [exact]: `docs/backend/research-log.md` 신규 생성. frontmatter (title, version 1.0.0, last_updated 2026-04-11), "2026-04-11 Phase 7 research-mode kaizen" 엔트리, Hexagonal/Clean/DDD / OpenAPI 3.1 / RFC 9700 / Outbox / Pact 관련 URL 최소 7 건 인용.
- [ ] RL-02 [exact]: `docs/infra/research-log.md` 신규 생성. Phase 8 엔트리, K8s PSA / Terraform 1.10 / OpenTofu state encryption / SLSA / Cosign / OTel / Argo Rollouts / Flux 관련 URL 최소 8 건.
- [ ] RL-03 [exact]: `docs/rust/research-log.md` 신규 생성. Phase 9 엔트리, Rust 2024 edition / Axum 0.8 / SQLx 0.8 / SeaORM 1.1 / Tonic 0.13 / Clippy 관련 URL 최소 6 건. fit-pal server ground truth 언급.
- [ ] RL-04 [exact]: `docs/react/research-log.md` 신규 생성. Phase 10 엔트리, React 19 / Tauri 2 GA / Tailwind v4 / Vite 8 / TanStack Query v5 / Zustand v5 / Lingui v5 / Zod v4 호환 관련 URL 최소 9 건.
- [ ] RL-05 [exact]: `docs/flutter/research-log.md` 신규 생성. Phase 5 엔트리. `docs/kaizen/flutter-research-log.md` 와 중복 허용 (per-kit view 용도).

### DS (docs-site harness 6 개 HTML 재생성)

- [ ] DS-01 [structural]: `docs/harness/skill-design.html` 가 **v1.1.0 (Phase 1)** 내용 반영 — Anthropic 공식 frontmatter 엄격 스키마, undertrigger 방지, 500 라인 상한, Reference 1-level deep, Degrees of Freedom, Evaluation-Driven Development, MCP fully-qualified name 중 **최소 5 개** 원칙 카드로 포함. 각 원칙 카드에 출처 URL 링크 필수 (`<a class="card-source" href="...">출처명</a>`).
- [ ] DS-02 [structural]: `docs/harness/agent-design.html` 가 **v1.1.0 (Phase 1)** 내용 반영 — `use proactively` 공식 의미, `initialPrompt`/`color` 필드, Agent(agent_type) 화이트리스트, 계약 모호성 방지 (`[exact]/[structural]/[goal]` 태그), 서브에이전트는 다른 서브에이전트 생성 불가 원칙 중 최소 5 개 포함.
- [ ] DS-03 [structural]: `docs/harness/contract-design.html` 가 **Phase 2 contract-schema v2** 내용 반영 — `[exact]/[structural]/[goal]` 태그 체계, Aggregation Mode (`[enumerated]/[collective]`), 태그 선택 기준, 한·영 표현 병기 권고, AAA 패턴, LLM-as-Judge 연구 인용 중 최소 5 개 원칙 카드로 포함.
- [ ] DS-04 [structural]: `docs/harness/contract-schema.html` 가 **contract-schema v2 (2026-04-11)** 내용 반영 — specificity tag, aggregation mode, v1→v2 변경점 명시.
- [ ] DS-05 [structural]: `docs/harness/qa-evaluation.html` 가 **Phase 3 qa-evaluation-guide** 내용 반영 — Swap Test (position bias), Self-preference/Scoring bias 완화, Recursive Rubric Decomposition, CheckEval boolean 분해, Specificity Tag 소비 규칙, Aggregation Mode 소비 규칙, CoT 효용 한계 중 최소 6 개 원칙 카드 + arxiv URL.
- [ ] DS-06 [structural]: `docs/harness/feedback-system.html` 가 **Phase 4 feedback-schema v1 extension** 내용 반영 — `repeat_count`, `first_seen_at`, `regression_link` 3개 필드 + 기존 필드와의 차이 + 2026 누적 분석 트렌드 출처 (ContextQA, Sauce Labs 등) 언급.
- [ ] DS-07 [exact]: 6개 HTML 페이지 모두 **최소 400 라인** (docs-site 원칙 8).
- [ ] DS-08 [exact]: 6개 HTML 페이지 모두 **standalone** — 외부 CDN `<link>`, `<script src=`, `@import url(` 0 건. 모든 스타일 인라인 `<style>`.
- [ ] DS-09 [exact]: 6개 HTML 페이지 모두 **`--accent` / `--accent2` CSS 변수**가 harness accent 컬러 (teal 계열 또는 references/css-tokens.md 매핑) 로 설정.
- [ ] DS-10 [exact]: 6개 HTML 페이지 모두 `<a class="card-source"` 패턴을 최소 3 건 포함 (출처 URL 누락 0 건).
- [ ] DS-11 [exact]: `docs/index.html` 의 `categories` 배열에 6 개 파일이 모두 등록되어 있음 (이미 등록돼 있으면 유지 확인).
- [ ] DS-12 [exact]: 6 개 HTML 페이지 모두 WCAG 2.2 SC 2.5.8 준수 — 터치 타겟 최소 24x24 CSS px (Phase 6 design-kit 정합성). 버튼/링크/인터랙티브 요소에 해당.

### MA (메타 관리 — failure-count + feedback cleanup + evals)

- [ ] MA-01 [exact]: `.harness/.meta/kaizen-failure-count.yaml` 에 `phase_7`, `phase_8`, `phase_9`, `phase_10` 엔트리 추가 (값 0). `last_updated: 2026-04-11`. `phase_9: 0` 에 "iter1 REJECT → iter2 APPROVE, reset" 주석 포함.
- [ ] MA-02 [exact]: 글로벌 피드백 정리 실행. 현재 `/Users/jackson/.harness/feedback/evaluator` 에 85개 파일 존재, 6개월 초과 0 건, 500 개 미만이므로 **삭제 액션은 없음**. `.harness/.meta/cleanup-log.yaml` 을 신규 생성하고 실행 기록 ("2026-04-11: 85 files, 0 aged, 0 over-500, no deletion").
- [ ] MA-03 [exact]: evals/evals.json 점검 — `flutter-toolkit/evals/evals.json`, `rust-kit/evals/evals.json`, `react-kit/evals/evals.json`, `design-kit/evals/evals.json` 4 개 파일의 `id` 필드와 현재 `<plugin>/skills/` 디렉토리의 스킬 목록이 일치하는지 확인. 불일치 시 `.harness/.meta/evals-audit-2026-04-11.md` 에 diff 기록. 현재 세션에서 스킬 신규 추가/삭제는 없었으므로 정합성 유지가 기대값.

### I (Integration / Hygiene)

- [ ] I-01 [exact]: `python3 scripts/validate-plugin.py` Total 7 plugins, 7 OK, Exit 0.
- [ ] I-02 [exact]: `python3 scripts/sync-docs.py --check-only` 모든 README 동기화 상태.
- [ ] I-03 [exact]: 본 스프린트의 **수정 금지 파일** 목록 (harness/skills/, harness/docs/guides/, harness/agents/, harness/references/, flutter-toolkit/, design-kit/, backend-kit/, infra-kit/, rust-kit/, react-kit/, 모든 plugin.json, marketplace.json) 중 단 1 건도 diff 에 등장하지 않음. `git diff HEAD~1 --name-only` 로 확인.
- [ ] I-04 [exact]: 본 스프린트 commit 1+ 건이 브랜치 `kaizen/2026-04-11-research` 에 추가됨. commit prefix 는 `kaizen(post-missing-items):` 또는 유사. commit body 에 OR/DS/FL/RL/MA 각 섹션 변경 요약 포함.
- [ ] I-05 [exact]: 전 변경 파일에 bare fenced code block 0 건 (AP-03 anti).
- [ ] I-06 [exact]: git push 완료 후 기존 PR #6 (`kaizen/2026-04-11-research`) 에 추가 커밋이 반영됨. 새 PR 생성 금지.

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 모든 fenced block에 언어 힌트 (`text`, `bash`, `yaml`, `html`, `json` 등) 필수
- [ ] AP-04: frontmatter name 필드 누락 금지

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (스펠체크 cSpell 제외)
- [ ] DG-03: 콘솔 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 (해당 없음 — 문서/메타 작업)
