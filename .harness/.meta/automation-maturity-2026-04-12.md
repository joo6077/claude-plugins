# Kaizen 파이프라인 자동화 성숙도 리포트 (2026-04-12)

## 종합 점수: 23 / 35 (66%)

이번 세션의 meta-automation 사프린트로 Step 0 (data pool) + Step 0.5 (self-audit) + sync-orchestrator + Post-Kaizen Checklist + per-kit research-log 5종 신규 생성이 마무리되면서, 오케스트레이터는 "수동 orchestration → 반자동 pipeline" 경계를 넘었다. 다만 (a) cron 미등록, (b) Phase subagent 자동 dispatch 부재, (c) Post-Kaizen Checklist 스크립트화 부재, (d) audit-log 자동 append 부재, (e) meta-kaizen 리서치 루프 부재라는 5 개 구조적 한계가 남아 있다.

## 영역별 점수

| # | 영역 | 점수 | 평가 |
| - | ---- | ---- | ---- |
| 1 | 트리거 / 진입점 | 2 / 5 | 수동/문서화 O, 실제 cron 미등록 |
| 2 | Pre-flight / 데이터 수집 | 4 / 5 | Step 0/0.5 스크립트화, 전달은 수동 프롬프트 |
| 3 | Phase 실행 | 2 / 5 | 문서는 자동화 지시, 실행은 사람 주도 |
| 4 | 사이드 이펙트 / 산출물 동기화 | 4 / 5 | 5/6 단계 스크립트화, docs-site 만 수동 |
| 5 | 오케스트레이터 자체 개선 (meta) | 3 / 5 | 구조 드리프트는 자동, 콘텐츠 개선은 수동 |
| 6 | 품질 보증 | 4 / 5 | validate-plugin + sync-docs + sync-orchestrator 세 드리프트 훅 완비 |
| 7 | 안전성 / 복구 | 4 / 5 | failure-count/audit-log/scope 격리 강제, auto-revert 없음 |

## 영역별 상세 분석

### 1. 트리거 / 진입점 (2 / 5)

**잘 된 것**
- `kaizen-orchestrator/SKILL.md` Line 149~166 에 cron 트리거 (매주 월 09:00 KST), 수동 트리거 11 종 (`/kaizen-orchestrator`, `phase1`~`phase10`, `final`) 가 문서화되어 있다.
- 이벤트 트리거 조건 (REJECT 연속 2 회, Phase regression FAIL) 은 `kaizen-failure-count.yaml` + SKILL.md Line 36 "연속 2 회 FAIL 시 일시 중단" 으로 정의됨.
- 개별 kaizen 스킬 cron 은 비활성화하고 오케스트레이터만 단일 진입점으로 강제 — 트리거 중복 방지.

**남은 한계**
- **실제 cron 이 등록되지 않았다.** `/loop`, `/schedule` 같은 Claude Code remote trigger 도구로 등록된 증거가 없다 (`~/.claude/triggers/` 없음). 매주 월요일에 자동 실행되는 보장은 없고, 사람이 수동으로 `/kaizen` 을 호출해야만 실행된다.
- 이벤트 트리거 (REJECT 연속, validate-plugin FAIL) 가 자동으로 kaizen 을 kick-off 하지 않는다. 문서상 조건은 있지만 이를 모니터링하는 데몬/훅이 없다.
- `collect-kaizen-data.py` 가 "threshold 초과 시 자동 트리거" 같은 로직을 포함하지 않는다 — 순수 수집 스크립트다.

**개선 제안**
- `schedule` 스킬로 실제 remote trigger 생성: "매주 월 09:00 KST, `/kaizen` 실행".
- `scripts/kaizen-should-run.py` — 글로벌 feedback 디렉토리에 REJECT 가 임계치 초과 시 exit 0 을 반환하여 cron 이 조건부 실행하는 방식.

### 2. Pre-flight / 데이터 수집 (4 / 5)

**잘 된 것**
- Step 0 `collect-kaizen-data.py` (360 줄) 이 글로벌 feedback / Hub 외부 프로젝트 / followup / 레포 history / validate-plugin 5 소스를 한 번의 호출로 `kaizen-data-pool.md` (12 994 byte) 로 통합한다.
- Step 0.5 Orchestrator Self-Audit 가 신설되어 `orchestrator-audit-log.md` 를 매 사이클 읽도록 SKILL.md Line 252~273 에 blocking 조문이 박혀 있다. `sync-orchestrator.py --check-only` drift 감지도 같은 단계에서 실행된다.
- Phase 별 데이터 풀 참조 매핑 테이블 (SKILL.md Line 224~235) 이 명시되어 각 서브에이전트가 자기 Phase 의 §N 을 우선 참조할 수 있다.

**남은 한계**
- 데이터 풀이 **수동 프롬프트 전달** 에 의존한다. SKILL.md Line 237~243 은 "각 Phase subagent 프롬프트에 경로 전달 필수" 라고 지시하지만, 사람이 서브에이전트를 spawn 할 때 직접 프롬프트에 넣어야 한다. 스크립트로 자동 주입되지 않는다.
- Step 0 실행이 SKILL.md 에는 "필수" 로 명시됐지만 pre-commit hook / CI 로 검증되지 않는다. 사람이 잊으면 그냥 건너뛴다.

**개선 제안**
- `scripts/spawn-kaizen-phase.sh <phase>` — 데이터 풀 경로 + 관련 §N 추출까지 포함한 subagent 프롬프트를 stdout 으로 출력. 사람은 복사만 하면 된다.
- Step 0 실행 유무를 `.harness/.meta/kaizen-data-pool.md` mtime 으로 검증 (당일 생성 아니면 Step 0 재실행 강제).

### 3. Phase 실행 (2 / 5)

**잘 된 것**
- Phase 1~10 순서가 SKILL.md 에 hardcoded 되어 있고 Gotchas Line 28 이 순서 변경을 금지한다.
- 각 Phase 의 subagent 호출 규약이 SKILL.md Line 170~186 "공통 실행 패턴" 에 표준화되어 있다 — Triage → 리서치 → GAP → Draft → QA → 태그 → 커밋 → Regression.
- REJECT 시 재시도 규약 (iter +1), 연속 2 회 FAIL 시 에스컬레이션은 `kaizen-failure-count.yaml` 로 영속화된다 (Phase 9 가 실제로 iter1 REJECT → iter2 APPROVE 되며 검증됨).

**남은 한계**
- **Phase subagent dispatch 가 자동이 아니다.** SKILL.md 는 "서브에이전트로 실행" 이라고 지시하지만, 실제 `Task` / `Agent` 도구를 자동 호출하는 스크립트가 없다. 메인 Agent 가 직접 11 번 Task 를 spawn 해야 한다.
- **리서치 자동화 부재.** 각 Phase 가 Context7/Codex 를 호출하도록 `search-sources.md` 가 가이드하지만, 자동 호출 orchestration 은 없다. 실제로 이번 사이클 모든 리서치는 메인/서브 Agent 가 수동 호출로 수행했다.
- QA Evaluator spawn 도 문서상 "각 Phase 끝에 실행" 이지만, 자동 트리거는 없고 Agent 가 "이제 QA 실행" 이라고 의식적으로 선택해야 한다.
- Phase 간 상태 전이가 메모리 (메인 Agent) 에 의존한다 — 중간에 세션이 끊기면 `kaizen-failure-count.yaml` 과 git tag 외에는 recovery 실마리가 없다.

**개선 제안**
- `scripts/run-kaizen-phase.sh <phase>` — git tag 생성 + subagent 호출 프롬프트 생성 + regression smoke test + failure-count 업데이트를 한 번에 처리.
- Phase state machine 을 `.harness/.meta/kaizen-state.yaml` 로 persistence (현재 Phase / iter / 마지막 APPROVE 타임스탬프).

### 4. 사이드 이펙트 / 산출물 동기화 (4 / 5)

**잘 된 것**
- `sync-docs.py` (468 줄) 이 README 자동 동기화를 담당. PostToolUse 훅 (`settings.json` Line 6~11) 이 Edit/Write 후 `--check-only` 를 자동 실행하여 drift 시 알림.
- per-kit research-log 5 개 (backend 61 줄, infra 69 줄, rust 59 줄, react 70 줄, flutter 45 줄) 가 이번 사이클에 신규 생성되어 SKILL.md Step 12 조문 "파일이 없으면 신규 생성" 에 부합.
- plugin.json / marketplace.json 버전 bump 는 `release.sh` 가 자동화 (description 날짜+버전 동기화 포함).
- `kaizen-failure-count.yaml` / `cleanup-log.yaml` / `evals-audit-2026-04-11.md` 이 모두 append-only 로 기록되며 이번 사이클 엔트리가 포함됨.
- `docs/kaizen/changelog.md` (166 줄) + `research-log.md` (221 줄) + `flutter-changelog.md` + `flutter-research-log.md` 갱신 조문이 Step 12 에 하드코딩됨.

**남은 한계**
- **docs-site (HTML) 재생성이 여전히 수동 스킬 호출.** Step 11.5 는 `docs-site` 스킬을 호출한다고 명시하지만 스크립트 자동화가 아니다. 이번 사이클에도 6 개 harness HTML 을 수동 재생성했다 (commit `c52c135`).
- changelog / research-log 업데이트는 메인 Agent 가 "Step 12 확인" 하면서 직접 작성한다 — 커밋 메시지/diff 에서 엔트리를 자동 생성하는 스크립트가 없다.
- evals-audit 파일명이 `{YYYY-MM-DD}` 기반이라 Agent 가 매번 오늘 날짜로 새로 만들어야 한다.

**개선 제안**
- `scripts/regen-docs-site.py` — 변경된 소스 `.md` 를 감지해서 대응 HTML 을 `docs-site` 스킬 규약에 맞게 재생성하는 배치 스크립트.
- `scripts/append-changelog.py <phase> <summary>` — 표준 엔트리 포맷으로 자동 append.

### 5. 오케스트레이터 자체 개선 (meta) (3 / 5)

**잘 된 것**
- `sync-orchestrator.py` (199 줄) 이 `marketplace.json` → SKILL.md AUTO 마커 영역을 자동 생성. 현재 6 plugins 동기 상태 (`sync-orchestrator: 이미 동기화됨 (6 plugins)` exit 0 확인됨).
- PostToolUse 훅이 `marketplace.json` 또는 orchestrator SKILL.md 변경 시 drift 감지를 자동 실행한다 (`settings.json` Line 13~16).
- `orchestrator-audit-log.md` (6039 byte) 가 이번 사이클의 5 개 meta-issue (docs-site 누락, per-kit research-log 영구 누락, flutter-changelog 누락, orchestrator SKILL 사각지대, kit 증감 수동 편집) 를 기록하고, Step 0.5 가 다음 사이클에 이를 자동 재확인하도록 blocking gate 로 삽입됨.
- Post-Kaizen Checklist (SKILL.md Line 470~485) 가 PR 생성 전 blocking gate 로 작동하도록 Gotchas Line 39 에 명시됨.

**남은 한계**
- **SKILL.md 콘텐츠 (텍스트 본문) 는 여전히 사람이 개선한다.** AUTO 마커 영역 (Phase 5~10 리스트) 만 자동이고, Step 0/0.5/11.5/11.6/12 같은 핵심 조문은 사람이 직접 편집한다. meta-kaizen 루프가 존재하지 않는다.
- **audit-log 자동 append 부재.** Step 0.5 가 로그를 읽지만, 사이클 종료 시 이번 사이클의 meta-issue 를 자동으로 append 하는 루틴이 없다. 이번 엔트리 (2026-04-11 research-mode rerun) 도 사람이 작성.
- **Post-Kaizen Checklist 가 스크립트화되지 않았다.** 체크리스트 12 개 항목은 텍스트로만 존재하고, `validate-post-kaizen.py` 같은 실행 검증 스크립트가 없다 (audit-log Line 67 에 이미 backlog 로 기록됨).
- meta-kaizen 이 학술/공식 문서 리서치 기반으로 orchestrator 자체를 개선하는 루프가 없다. 현재 Step 0.5 는 "회고 기반 자가진단" 수준이며 "외부 발전 반영" 이 아니다.

**개선 제안**
- `scripts/validate-post-kaizen.py` — 체크리스트 12 항목을 자동 검증 (sync-docs, validate-plugin, docs/kaizen/changelog.md 변경 여부, evals-audit 존재, failure-count last_updated, per-kit research-log 이번 사이클 엔트리 등).
- `scripts/append-audit-log.py` — Step 11 Final 완료 시점에 이번 사이클 요약을 audit-log 에 자동 append.
- `meta-kaizen` 스킬 신설 — LLM-agent orchestration 최신 리서치 (예: AutoGen, CrewAI, AgentOps) 를 근거로 orchestrator SKILL.md 를 개선.

### 6. 품질 보증 (4 / 5)

**잘 된 것**
- `validate-plugin.py` (800 줄) 이 7 카테고리 (V1 frontmatter / V2 templates / V3 refs / V4 trigger 키워드 중복 / V5 placeholders / V6 bare fence / V7 plugin-json 버전) 를 검증. 현재 `Total 7 plugins, 7 OK, Exit 0` 통과 확인됨.
- `--fix` 모드로 V5 (placeholder) + V6 (bare fence) 자동 수정 지원.
- PostToolUse 훅이 Edit/Write 후 `sync-docs.py --check-only` 와 `sync-orchestrator.py --check-only` 두 드리프트를 동시에 감지한다.
- `markdownlint` 관련 fix 를 이전 Phase 마다 별도 commit 으로 정리 (`chore(kaizen-p1)`, `p3`, `p5`, `p9` 등).
- `evals-audit-2026-04-11.md` 가 7 kit evals.json 을 skills/ 디렉토리와 대조하여 covered/orphan 리포트를 제공.

**남은 한계**
- validate-plugin 이 **카이젠 Phase 종료 시 자동 실행되지 않는다.** Post-Kaizen Checklist 에는 "검증 수동 실행" 만 적혀 있다. PostToolUse 는 sync-docs/sync-orchestrator 만 감지하고 validate-plugin 은 빠져 있다.
- `evals-audit` 에서 발견된 orphan (rust-kit `rust-kaizen` evals entry) 과 react-kit evals 0 개 coverage 가 아직 해결되지 않았다. 감지는 되지만 자동 수정 액션이 없다.
- markdownlint 검사가 `validate-plugin.py` 범위 밖이라 별도 단계로 운영된다 (V6 bare fence 만 커버).

**개선 제안**
- PostToolUse 훅에 `validate-plugin.py --check=v1,v4,v5,v6` (속도 빠른 것만) 추가.
- `scripts/fix-evals-orphans.py` — evals.json 과 skills/ 디렉토리 mismatch 를 자동 패치.

### 7. 안전성 / 복구 (4 / 5)

**잘 된 것**
- Phase 간 scope 격리가 SKILL.md Line 32 + Post-Kaizen Checklist Line 485 에 하드코딩: "각 Phase commit 이 다른 Phase 의 소스 파일을 수정하지 않았다".
- Regression smoke test 가 APPROVE 후 강제 실행되며 실패 시 `git revert` 조문 (SKILL.md Line 184) 이 명시됨 — Phase 9 실제 사례 존재 (iter1 H-01/H-03 FAIL → iter2 fix).
- `kaizen-failure-count.yaml` 이 Phase 별 연속 실패 카운터를 영속화. 카운터 >= 2 시 Phase 일시 중단 + 사용자 에스컬레이션 (SKILL.md Line 193).
- `orchestrator-audit-log.md` 가 append-only 로 변경 이력을 보존 (Gotchas Line 273 "기존 엔트리 수정/삭제 금지").
- `cleanup-log.yaml` 은 매 사이클 0 액션이어도 엔트리 추가 (SKILL.md Line 415) — 실행 증거 확보.

**남은 한계**
- **git revert 가 자동이 아니다.** SKILL.md 는 "Regression 실패 시 git revert" 지시만 있고, 실제 실행은 메인 Agent 가 한다. 스크립트화 부재.
- Phase scope 격리 검증이 Post-Kaizen Checklist 에 텍스트로만 있고 `git log --name-only` 기반 자동 감사 스크립트가 없다.
- 중간 세션 interrupt 시 recovery — 어느 Phase 까지 APPROVE 했는지 복구하려면 git tag 와 failure-count 를 수동 조회해야 한다.

**개선 제안**
- `scripts/verify-phase-isolation.py <phase_n>` — 해당 Phase commit range 가 자기 scope 외 파일을 건드렸는지 감사.
- `scripts/auto-revert-on-regression.sh <phase>` — regression FAIL 시 `kaizen-phase-N-pre` 태그로 자동 revert.

## 자동화 Tier 분류

| Tier | 설명 | 해당 항목 |
| ---- | ---- | -------- |
| **완전 자동** | 사람 개입 0 | sync-orchestrator drift 감지 (PostToolUse), sync-docs drift 감지 (PostToolUse), marketplace.json → SKILL.md AUTO 영역 생성, validate-plugin 7 카테고리, collect-kaizen-data 수집, release.sh (수동 트리거 1 회 후 버전 bump+commit+tag+push), `--fix` 모드 placeholder/bare fence 자동 교정 |
| **반자동 (보조 필요)** | 스크립트 실행하지만 사람이 언제 돌릴지 결정 | Step 0 `collect-kaizen-data.py` (SKILL.md 에 지시, 사람이 호출), Step 0.5 `sync-orchestrator.py --check-only` (훅은 자동, Step 0.5 는 사람이 호출), Phase 별 markdownlint fix, per-kit research-log 갱신 (사람이 템플릿에 내용 채움), kaizen-failure-count 업데이트 (사람이 yaml 편집), evals-audit 생성 (사람이 스크립트 대체 작성) |
| **수동 (오케스트레이터가 지시)** | 메인 Agent 가 subagent 에 지시, subagent 가 수행 | Phase 1~10 subagent dispatch (Task 도구 수동 호출), 각 Phase 리서치 (Context7/Codex 수동 호출), Sprint Contract DRAFT 작성, QA Evaluator spawn, 개선안 코드 패치, regression smoke test, `docs-site` 스킬로 HTML 재생성, changelog/research-log 본문 작성, Post-Kaizen Checklist 실행 |
| **사람만 가능** | 완전 수동 | cron 등록 (schedule 스킬로 사람이 한 번 세팅), orchestrator SKILL.md 본문 개선 (meta-kaizen 없음), audit-log 엔트리 작성, 이번 사이클 같은 meta-automation 스프린트 기획, 학술 리서치 방향 선정 |

## Meta Observations

이번 세션에서 드러난 구조적 한계 5 가지:

1. **"문서화된 자동화" 와 "실행되는 자동화" 의 갭.** SKILL.md 는 "Step 0 필수 실행", "Step 11.5 건너뛰기 금지", "Post-Kaizen Checklist blocking gate" 를 텍스트로 선언하지만, 선언을 강제하는 실행 레이어 (pre-commit hook, CI, script) 가 없다. Agent 가 규율을 지키길 기대하는 구조.
2. **Meta-recursion 이 1 단계에 멈춤.** Step 0.5 가 "이전 사이클 meta-issue 재검증" 을 하지만, "이번 사이클의 meta-issue 를 자동 발견해 audit-log 에 append" 는 하지 못한다. meta 의 meta 가 없다.
3. **외부 리서치 의존.** Phase 별 카이젠이 Context7/Codex 로 최신 리서치를 수행하는 것은 문서에만 있고, 자동 호출 orchestration 이 없다. 메인 Agent 가 자각적으로 호출해야 한다.
4. **State persistence 빈약.** Phase 진행 상태가 git tag + failure-count.yaml 에 흩어져 있어 중단 복구가 어렵다.
5. **Plugin 증감 파이프라인 단방향.** `sync-orchestrator.py` 는 marketplace.json → SKILL.md 방향만 있고, 반대로 SKILL.md 에 신규 Phase 를 정의해서 kit 을 프로비저닝하는 반대 방향은 없다 (이건 `/create-kit` 이 담당하지만 연결이 느슨).

## 다음 단계 권장

우선순위 상위 3 개 자동화 gap 과 구현 아이디어:

1. **`scripts/validate-post-kaizen.py` 작성 (최우선)**  
   Post-Kaizen Checklist 12 개 항목을 한 번에 자동 검증. sync-docs / validate-plugin / docs/kaizen/changelog.md grep / evals-audit 존재 / failure-count last_updated / per-kit research-log 이번 사이클 엔트리 / Phase scope 격리 (`git log --name-only --grep=kaizen`) 전부 스크립트로 판정. Exit 1 이면 PR 생성 차단. 구현 난이도 중, 예상 300~400 줄.

2. **`schedule` 스킬로 실제 cron 등록**  
   `/schedule create --cron "0 9 * * 1" --command "/kaizen"` 형태로 매주 월 09:00 KST 에 remote trigger 를 등록. 등록 후 첫 실행까지 모니터링하여 진입점 자동화를 실증. 구현 난이도 하, 1 회 세팅.

3. **`scripts/spawn-kaizen-phase.sh <phase>` 작성**  
   Phase N 을 시작할 때 (a) `kaizen-phase-N-pre` git tag 생성, (b) `kaizen-data-pool.md` §N 추출, (c) subagent 프롬프트를 stdout 으로 생성 (data pool 경로 + scope + search-sources + 공통 실행 패턴 전부 포함), (d) 실행 완료 후 regression smoke test 자동 실행, (e) failure-count.yaml 갱신. 이로 인해 "Phase 실행" 영역을 2/5 → 4/5 로 끌어올릴 수 있다. 구현 난이도 중, 200 줄 내외.

추가 backlog (audit-log Line 70~73):
- `meta-kaizen` 스킬 설계 — orchestrator SKILL.md 의 학술 리서치 기반 개선 루프.
- audit-log 자동 append — Step 11 Final 완료 시점에 실행.
