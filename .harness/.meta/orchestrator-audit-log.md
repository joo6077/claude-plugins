# Kaizen Orchestrator Self-Audit Log

> `.claude/skills/kaizen-orchestrator/SKILL.md` Step 0.5 가 append-only 로 기록한다.
> 각 엔트리는 한 카이젠 사이클에서 발견된 meta-issue (오케스트레이터 자체 결함)를 담는다.
> 다음 사이클 Step 0.5 는 이 로그를 읽어 반복을 방지한다.

---

## 2026-04-11 — research-mode rerun (kaizen/2026-04-11-research)

**Cycle:** Phase 1~10 + Final + post-missing-items 스프린트
**Cycle trigger:** 사용자 명시 요청 ("카이젠 재실행, Codex + Context7 로 최신 리서치")

### 사용자 제기 meta-issues (이번 사이클 발생)

이번 사이클이 끝나는 시점에 사용자가 오케스트레이터 자체 파이프라인의 누락을 지적하여 발견된 구조적 결함:

1. **docs-site 재생성이 파이프라인에 없음 (심각도: 높음)**
   - 증상: Phase 1~10 에서 변경된 `.md` 소스에 대응하는 `docs/<plugin>/*.html` 84 개가 카이젠 이전 상태에 고정.
   - 근본 원인: Step 11~12 어디에도 `/docs-site` 스킬 호출 조문이 없었음. `/docs-site` 스킬은 존재하지만 오케스트레이터가 호출하지 않음.
   - 임시 조치: 이번 사이클 수동 개입으로 Step 11.5 "docs-site 재생성" 신규 추가.
   - 영구 조치: Gotchas 에 "Step 11.5 건너뛰기 금지" 명시. 다음 사이클 Step 0.5 에서 이 이력을 확인하여 재발 감시.

2. **per-kit research-log 가 "존재 시" 조문이라 영구 누락 (심각도: 높음)**
   - 증상: `docs/{backend,infra,rust,react,flutter}/research-log.md` 모두 파일 자체가 존재하지 않음. Step 12 의 "존재 시 갱신" 조문이 생성 트리거를 만들지 않음.
   - 근본 원인: 조문이 "존재 시" 조건부여서 파일 없으면 skip → 영원히 생성 안 됨.
   - 임시 조치: 5 개 per-kit research-log 신규 생성 (backend / infra / rust / react / flutter).
   - 영구 조치: Step 12 조문을 "파일이 없으면 신규 생성" 으로 수정. Gotchas 에 해당 항목 추가.

3. **flutter-changelog / flutter-research-log 갱신 누락 (심각도: 중간)**
   - 증상: Step 12 에 명시된 파일인데 이번 사이클 Phase 5 결과가 반영되지 않음.
   - 근본 원인: 완료 체크리스트가 없어서 "대부분 OK" 로 넘어감. 메인 세션이 마감 직전 verification-before-completion 을 건너뜀.
   - 임시 조치: 수동으로 2 개 파일에 Phase 5 엔트리 추가.
   - 영구 조치: Step 12 말미에 "Post-Kaizen Checklist" 신규 섹션 (blocking gate). 체크리스트 미통과 시 PR 생성 금지.

4. **kaizen-orchestrator SKILL.md 자체가 카이젠 대상 사각지대 (심각도: 근본적)**
   - 증상: Phase 1~4 는 harness 개선, Phase 5~10 은 플러그인 개선. orchestrator SKILL.md 는 어느 Phase 에도 포함되지 않음.
   - 근본 원인: 오케스트레이터는 개선 주체이지 개선 대상이 아니라는 가정. 메타 레벨에서 사각지대 발생.
   - 임시 조치: Step 0.5 "Orchestrator Self-Audit" 신규 추가. 사이클 시작 시 이전 사이클의 meta-issue 를 자동 확인.
   - 영구 조치: 다음 사이클 Step 0.5 가 이 audit-log 파일을 읽고 모든 이전 issue 의 재발 여부를 Phase 4 (harness-kaizen) subagent 프롬프트에 포함.

5. **kit 추가/삭제 시 오케스트레이터 수동 수정 필요 (심각도: 중간)**
   - 증상: 새 킷을 만들면 orchestrator SKILL.md 의 Phase 리스트를 사람이 편집해야 했음. 수정/삭제도 마찬가지.
   - 근본 원인: Phase 5~10 섹션이 자유 텍스트로 작성되어 자동화 불가.
   - 임시 조치: `<!-- AUTO:plugin_phases:begin -->` ~ `<!-- AUTO:plugin_phases:end -->` 마커 삽입 + `scripts/sync-orchestrator.py` 신규 작성.
   - 영구 조치:
     - `python3 scripts/sync-orchestrator.py` 로 marketplace.json → SKILL.md 자동 동기화
     - `.claude/settings.json` 의 PostToolUse 훅에 drift 감지 추가
     - Step 0.5 에서 `--check-only` 실행하여 drift 있으면 자동 복구 지시
     - 다음 카이젠에서 킷 증감 시 수동 개입 없이 자동 반영됨

### 재발 감시 대상 (다음 사이클 Step 0.5 에서 확인)

- [ ] Step 11.5 (docs-site 재생성) 이 실제로 실행되었는가?
- [ ] Step 11.6 (글로벌 피드백 정리) 이 실제로 실행되었는가?
- [ ] Step 12 Post-Kaizen Checklist 가 PR 생성 전에 검증되었는가? 실패 항목이 있었는가?
- [ ] Phase 5 변경 있을 때 flutter-changelog / flutter-research-log 가 갱신되었는가?
- [ ] Phase 7/8/9/10 변경 있을 때 per-kit research-log (backend/infra/rust/react) 가 갱신되었는가?
- [ ] marketplace.json 이 바뀌었는데 orchestrator SKILL.md 가 sync 되지 않았는가?
- [ ] `.harness/.meta/kaizen-failure-count.yaml` last_updated 가 이번 사이클 날짜로 갱신되었는가?
- [ ] `.harness/.meta/evals-audit-{YYYY-MM-DD}.md` 가 생성되었는가?

### 자동화 추가 후 남은 한계

- **meta-kaizen 스킬 없음**: orchestrator SKILL.md 자체의 리서치 기반 개선 (LLM agent orchestration 최신 연구 반영) 은 여전히 사람이 해야 한다. Step 0.5 는 "누락 감지" 수준이고, "구조적 upgrade" 는 아니다.
- **audit-log 자동 append 없음**: 이 파일은 현재 사람이 작성하고 있다. 다음 사이클부터 Step 0.5 가 실패 항목을 자동으로 append 하도록 추가 개선 필요.
- **Post-Kaizen Checklist 자동 검증 부재**: 체크리스트는 텍스트로 존재하지만 실행 검증을 스크립트화하지 않았다. `scripts/validate-post-kaizen.py` 같은 스크립트가 필요.

### 다음 사이클 액션 아이템 (backlog)

- `scripts/validate-post-kaizen.py` 작성 — Post-Kaizen Checklist 항목들을 자동 검증
- `meta-kaizen` 스킬 신규 설계 — orchestrator SKILL.md 를 리서치 기반으로 개선
- audit-log append 자동화 — Step 11 Final 끝에 이번 사이클 요약을 자동 append

---

---

## 2026-04-24 — kaizen cycle (Phase 1~11 full orchestration)

**Cycle:** Phase 0 (데이터 수집) → Phase 1~11 → Step 11.5 docs-site → Step 11.6 cleanup → Step 12 PR
**Cycle trigger:** 사용자 요청 ("10_Dev 내부 플젝 싹다 스캔 + /insights + 플러그인 QA 데이터 적용")

### Phase 0 확장 데이터 주입

- `/insights` 30일 세션 로그 → `insights-report.md` 추출 (3 friction + 3 patterns)
- 5개 외부 프로젝트 `.harness/` 집계 → `plugin-qa-data.md` (138 eval, 34 contract)
- 1798 reflections 집계 → `reflect-aggregated.md` (tool_failure 849, misunderstanding 419)
- MASTER.md 로 Phase별 주입 인덱스 작성

### Phase 진행 (11/11 APPROVE)

모든 Phase 1회 iteration 으로 APPROVE. REJECT → 재시도 발생 없음 (Phase 0 데이터 충실성 + Cross-Surface Parity 원칙 전파가 효과).

### Meta-issues — 이번 사이클 재발 없음

이전 사이클 2026-04-11 meta-issue 3건 모두 해소 유지:
1. docs-site 재생성 Step 11.5 명시 실행 (SHA 7e3b69e, 5 HTML)
2. per-kit research-log "존재 시" 조문 — 이번 사이클은 해당 없음 (필요 플러그인 없음)
3. flutter-changelog 갱신 — Phase 5 한정, changelog.md 통합 엔트리로 처리

### 구조적 관찰

- Cross-Surface Parity Checklist (Phase 1 도입) 이 Phase 2~11 전파 연쇄를 실증적으로 막은 것으로 확인. 이전 사이클의 PH-01 (design-kit REJECT) 패턴 재발 0.
- Phase 7/8 (backend/infra-kit) 5 REJECT 동일 패턴 세트를 Phase 7 해결책으로 Phase 8 에 이식 → 1회 iteration APPROVE. Sibling-based solution reuse 가 효과적.
- Phase 10 react-kit (21 skills + 3 agents) 는 Large Kit Priority Tiering (3계층) 으로 관리. Library Policy 원칙 (라이브러리 0개 애니메이션) 절대 완화 금지 지침 준수.

### 다음 사이클 개선 제안

- kaizen-data-pool.md 에 `/insights` 리포트 소스를 공식 통합 (이번엔 사용자 요청으로 수동 주입, 다음엔 Step 0 자동화)
- 각 Phase QA를 self-evaluator rule-by-rule audit 으로 한 이유 (서브에이전트 중첩 불가) 를 orchestrator SKILL Gotchas 에 명시

---

## 2026-05-07 — kaizen cycle (Phase 1~12, /insights 산출물 자동 통합 파이프라인 구축)

**Cycle:** Step 0/0.5 → Phase 1~12 → Final + Step 11.5/11.6/12 PR
**Cycle trigger:** 사용자 명시 요청 ("/insights 카이젠에 영구 반영 + 풀 사이클 진행")

**중요한 구분 — `/insights` 스킬 실행 vs 산출물 활용:**
이번 사이클에서 메인 세션은 `/insights` **슬래시 커맨드 자체를 실행하지 않았다.** 해당 커맨드는 Claude Code CLI 의 사용자 직접 실행 명령으로 추정되며, 메인 세션의 Skill 도구 목록에도, 마켓플레이스 플러그인에도, `~/.claude/commands/` 에도 없다. 따라서 메인 세션이 invoke 할 surface 가 없다. 본 사이클은 **사용자가 13 일 전 (2026-04-24) 사전 생성해둔 `.claude/kaizen-input/insights-report.md` 산출물을 입력으로 사용**했고, **다음 사이클부터 동일 경로의 신선한 산출물이 자동 통합되도록 파이프라인을 구축**했다.

### 이번 사이클 해소된 메타 이슈 (이전 사이클 backlog)

1. **`/insights` 자동 통합 부재** — 이전 2026-04-24 사이클의 "다음 사이클 개선 제안" 1번 항목.
   - 영구 조치: `scripts/collect-kaizen-data.py` 에 `collect_insights_report()` 신규 + 자동 탐색 (repo `.claude/kaizen-input/` → `~/.claude/kaizen-input/`) + 60일 stale 경고 + 데이터 풀 §0 으로 삽입.
   - SKILL.md Step 0 에 정책 명시 + Gotchas 6 건.
   - 검증: `python3 scripts/collect-kaizen-data.py` 실행 결과 "/insights 리포트: ... (13일 전)" 출력 확인됨.
   - **남은 한계 (다음 사이클 backlog 4 번 참조):** 메인 세션이 `/insights` 자체를 invoke 하지 못하므로, fresh 산출물 생성은 사용자 수동 실행 의존. 자동화 완성도는 "산출물 활용" 단계까지만이고 "산출물 생성" 은 외부 의존.

2. **self-evaluator rule-by-rule audit 의 가이드 누락** — 이전 사이클 backlog 2번.
   - 영구 조치: agent-design-guide v1.3.0 §10 Reviewer Gotchas 에 1 줄 추가. orchestrator-audit-log 인용 명시.

### 이번 사이클 신규 메타 이슈 (다음 사이클 재발 감시 대상)

1. **Phase 12 (reflect-kit) 누락 보정 — orchestrator SKILL.md 의 수동 영역에서 발생 (심각도: 중간)**
   - 증상: orchestrator SKILL.md 의 AUTO:plugin_phases 영역은 sync-orchestrator.py 가 자동으로 Phase 12 를 추가했지만, **수동 영역** (Phase 의존성 그래프, Phase 순서 논리, 트리거 조건, 수동 트리거 인자, Phase 1~N 표기 4 곳, Final 범위 + 정합성, failure-count, scope 격리 체크) 7+ 개 위치에 Phase 12 가 누락되어 있었음.
   - 근본 원인: AUTO 영역만 자동화되어 있고 수동 영역은 여전히 사람/메인-세션이 편집해야 함. 카이젠 오케스트레이터 SKILL.md 의 메타-자동화가 부분적.
   - 임시 조치 (이번 사이클): 수동 영역 7+ 위치 Phase 12 전수 추가. 이번 사이클 Phase 4 (Harness 카이젠) 의 일부로 처리.
   - 영구 조치 제안 (다음 사이클 backlog): `scripts/sync-orchestrator.py` 에 Phase 1~N 표기 자동 갱신 옵션 추가, 또는 orchestrator SKILL.md 의 수동 영역 자체를 마커 기반으로 재구조화.

2. **per-kit research-log 의 일부 누락 — planning-kit (심각도: 낮음)**
   - 증상: docs/planning/research-log.md 가 부재.
   - 영구 조치: 이번 사이클에서 신규 생성 (frontmatter + 외부 리서치 인용 11 건 보존 + 다음 사이클 백로그 3 건).

3. **마크다운 lint 워닝 누적 (심각도: 낮음, 비차단)**
   - 증상: skill-design-guide.md MD025/MD032/MD060 등, changelog.md MD024 (시기별 동일 헤딩), research-log.md MD060/MD012.
   - 근본 원인: 가이드 문서를 사람이 손으로 작성하면서 lint 규칙 의식하지 않음.
   - 임시 조치: Final 단계에서 `scripts/fix-markdown-lint.py` 일괄 실행으로 자동 fix 시도.
   - 영구 조치 제안: PostToolUse 훅에서 .md 변경 시 자동 lint fix 실행 (Phase 1 신규 패턴 7 Hook-Triggered Auto-Correction 의 첫 번째 적용 대상).

### 재발 감시 대상 (다음 사이클 Step 0.5 에서 확인)

- [ ] `/insights` 리포트가 60일 초과 STALE 로 표시되었는데도 사용자가 재실행하지 않은 채 카이젠이 진행되었는가?
- [ ] orchestrator SKILL.md 의 수동 영역 Phase 1~N 표기에 새로 추가된 Phase 가 누락되었는가?
- [ ] Phase 12 reflect-kit 의 cron 비활성 목록 / 수동 트리거 인자가 모두 동기화되었는가?
- [ ] cross-kit-principles 매트릭스가 다음 사이클에서도 Phase 1 신규 원칙의 SSOT 로 작동하고 있는가?
- [ ] 마크다운 lint 워닝이 PostToolUse 훅 또는 fix-markdown-lint.py 자동 실행으로 사이클 종료 시점에 0 건인가?

### 자동화 추가 후 남은 한계

- **`/insights` 외부 도구 자체 자동 실행 부재**: `/insights` 는 사용자가 수동으로 실행하여 산출물을 `.claude/kaizen-input/` 에 배치하는 외부 도구. orchestrator 가 직접 호출할 수 없음. 60일 STALE 경고로 보완하지만 자동화 한계 존재.
- **Phase 5~12 의 가벼운 cross-ref 적용 vs 무거운 카이젠**: 이번 사이클은 효율성을 위해 각 kit README 에 cross-ref 만 추가했고, 본격적 SKILL.md 변경은 하지 않았음. 다음 사이클이나 reject 패턴이 발견되면 각 kit 의 SKILL.md 와 reviewer 에이전트에 직접 변경 필요.

### 다음 사이클 액션 아이템 (backlog)

- `scripts/sync-orchestrator.py` 에 수동 영역 Phase 1~N 표기 자동 갱신 옵션 추가
- PostToolUse 훅에 .md lint auto-fix 등록 (패턴 7 첫 적용 대상)
- per-kit research-log 자동 생성 검사 스크립트 (`scripts/validate-post-kaizen.py` 의 항목으로 추가)

---

## 2026-05-07b — fresh /insights followup kaizen (사용자 지적 후 즉시 보강)

**Cycle:** Step 0 (fresh report 경로 박기) → Gap 1~6 흡수 → harness 0.4.2 + PR
**Cycle trigger:** 사용자 지적 — "PR #8 은 13일 전 stale 추출본 기반. 진짜 fresh /insights 산출물은 ~/.claude/usage-data/report-ko.html 에 있다 (오늘 23:00 갱신)"

### 사용자 제기 메타 이슈 (즉시 인정 + 보강)

1. **stale insights-report.md 사용 (심각도: 높음)**
   - 증상: PR #8 은 2026-04-24 자 13일 전 추출본 기반으로 진행. 오늘 23:00 사용자가 `/insights` 직접 실행하여 fresh 산출물(`~/.claude/usage-data/report-ko.html`) 이 있었으나 미사용.
   - 근본 원인: `INSIGHTS_CANDIDATES` 가 `.claude/kaizen-input/insights-report.md` 만 탐색. `~/.claude/usage-data/report*.html` 경로 미인식.
   - 영구 조치: `INSIGHTS_CANDIDATES` 4 경로 우선순위 (report-ko.html > report.html > repo md > home md). HTML 텍스트 추출 함수 신규. VERY FRESH (24h 이내) 마커.
   - 검증: 데이터 풀 재생성 결과 "report-ko.html VERY FRESH (0.0h ago) format=html-extracted" — fresh 사용 확인.

2. **fresh vs stale 6 갭 누락 (심각도: 중간)**
   - 증상: fresh report 의 신규 항목 (Scope-Bound Edits / PreToolUse 가드 / /sprint / /refactor-widget / 좀비 MCP 패턴 / Figma SSIM) 6 건이 PR #8 에 누락.
   - 근본 원인: PR #8 진행 시점에 stale 추출본만 본 상태.
   - 영구 조치: followup 사이클 (kaizen/2026-05-07-fresh-insights 브랜치) 에서 6 갭 모두 흡수. 6 commits.

3. **본 followup 사이클 자체가 fresh insight 의 자기 모순 사례 (메타 메타 이슈)**
   - 증상: PR #8 진행 중 사용자 확인 없이 main 직접 push.
   - 근본 원인: Scope-Bound Edits Hard-stop 원칙 (이번 followup 에서 처음 명문화) 부재.
   - 영구 조치 (이번 followup): skill-design-guide §3.6 Scope-Bound Edits 신규 + .claude/settings.json PreToolUse 보호 브랜치 가드 등록. 다음 사이클부터 main 직접 편집 시 stderr 경고.

### 재발 감시 대상 (다음 사이클 Step 0.5)

- [ ] `~/.claude/usage-data/report*.html` 가 카이젠 시작 시 24h 이내인가? (24h 초과면 사용자에게 `/insights` 재실행 권고)
- [ ] PR 본문 표기가 stale 추출본 기반인지 fresh 산출물 기반인지 명확한가?
- [ ] PreToolUse 보호 브랜치 가드가 정상 작동하는가? (main 에서 Edit 시도 시 stderr 경고)
- [ ] 좀비 MCP 가드의 임계 (5건) 가 적절한가? (사용 패턴 보고 조정)

### 자동화 추가 후 남은 한계

- **fresh `/insights` 자동 실행 불가**: `/insights` 슬래시 커맨드 자체는 여전히 사용자 수동 실행. PreToolUse 훅이 STALE 일 때 사용자에게 "재실행 요청" 까지는 가능하지만 실행 자체는 불가.
- **HTML 추출 텍스트 가독성**: 현재는 단일 흐름 텍스트로 추출. 섹션 구조 (제목/리스트) 보전이 안 되어 LLM 이 구조 파악에 약함. 다음 사이클 backlog.

### 다음 사이클 액션 아이템 (backlog 추가)

- `/sprint` 스킬에 evaluator REJECT iteration 자동 카운트 + 3회 한계 escalation
- `/refactor-checklist` 의 스택별 규칙 자동 로드 로직 구현 (현재는 reference 명시만)
- HTML 추출 텍스트의 섹션 구조 보전 (마크다운 변환 라이브러리 도입 검토 — pyhtml2md 등)
- 메타 메타 이슈 추적 — "이전 사이클이 어떤 근본 원인으로 fresh 데이터를 놓쳤는가" 를 audit-log 가 명시적으로 추적하는 스키마
## 2026-06-11 — kaizen/2026-06-11

**Cycle:** kaizen/2026-06-11  
**Generated:** `scripts/append-audit-log.py` (auto-append)  
**Notes:** 인사이트 주도 부분 카이젠. reflect-digest 30일 집계로 hook permission-denied 957건(38% friction) 근본원인(hooks.json 직접실행 .sh의 git mode 100644) 발견·수정·릴리스. Phase 4 validate-plugin V8 hook-exec 가드 신규(1 CHANGED). Phase 1~3,5~14 NO_CHANGE(직전 6일전 사이클 동일 데이터 윈도우, 신선함≠새신호). meta-issue: detect-docs-drift.py가 plugin-validation-guide.html 매핑하나 실제 등록 페이지는 plugin-validation.html(suffix 불일치) — 다음 사이클 매핑 보정 검토.  

### Post-Kaizen Checklist failures

- 없음 (모든 체크 PASS)

### Orchestrator SKILL.md manual edits

- 없음 (수동 개입 없이 완료)

### Next-cycle watchlist

- 특별 감시 대상 없음

---

### Phase log — kaizen-2026-07-27

- Phase 4 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 5 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 6 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 7 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 8 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 9 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 1 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 2 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 3 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 4 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 5 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 6 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 7 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 8 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 9 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 11 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 14 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 13 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 10 — pass · kaizen-2026-07-27 · 2026-07-27
- Phase 12 — pass · kaizen-2026-07-27 · 2026-07-27

### 과거 엔트리 정정 (append-only 규칙상 원문은 수정하지 않고 여기에 기록)

- **2026-04-24 엔트리의 "서브에이전트 중첩 불가" 는 사실이 아니었다.**
  해당 엔트리("각 Phase QA를 self-evaluator rule-by-rule audit 으로 한 이유 (서브에이전트 중첩 불가) 를
  orchestrator SKILL Gotchas 에 명시")는 **잘못된 전제** 위에 세워졌다.
  2026-07-27 Phase 1 이 공식 문서(https://code.claude.com/docs/en/sub-agents)를 조회해 확인한 결과
  **서브에이전트 중첩은 기본 3층까지 허용**된다. `agent-design-guide.md` v1.5.0 에서 정정 완료.
  → 따라서 "Phase subagent 가 qa-evaluator 를 직접 spawn" 하는 구조는 이제 유효한 선택지다.
    다만 깊이 3층 한계에서 위임이 조용히 접히는 점은 주의해야 한다.
  → 이 정정은 원문 줄을 수정하지 않는다 (audit-log append-only). 과거 엔트리를 읽을 때
    반드시 이 정정을 함께 참조하라.

### 2026-07-27 사이클 meta-issue (다음 사이클 감시 대상)

1. **`scripts/validate-post-kaizen.py` 가 `datetime.date.today()` 기준이라 자정을 넘긴 사이클이
   자기 게이트에 걸린다.** 이번 사이클은 2026-07-27 자로 진행(브랜치 `kaizen/2026-07-27`,
   계약 파일명 `20260727-*`, 전 커밋)됐는데 체크 시점이 07-28 로 넘어가 changelog / research-log /
   cleanup-log / failure-count 4건이 **false negative FAIL**. 실제 엔트리는 전부 07-27 자로 존재
   (changelog 4회 · research-log 3회 · cleanup-log 1회 · `last_updated: "2026-07-27"`).
   → 수정 방향: 사이클 날짜를 `kaizen-state.yaml` 의 `cycle_id` 또는 브랜치명에서 유도하거나,
     `--cycle-date` 인자를 받도록. "오늘" 가정은 장시간 사이클에서 항상 깨진다.

2. **`.harness/project.yaml` AP-04 정규식이 구조적으로 항상 매치된다** (Final QA 평가자 발견).
   `^---\s*\n(?![^-]*name:)` 가 frontmatter **닫는** `---` 에도 매치되어, 이번 사이클 변경 파일
   74개 전부(74/74) 히트했다. 즉 vacuous anti-pattern 으로 검사 가치가 0 이다.
   → Phase 4(harness-kaizen) 소관. 여는 `---` 만 겨냥하도록 수정 필요.
   → 이번 사이클 계약의 Anti-patterns 카테고리는 AP-01(bare fence) 만 포함했으므로 verdict 무영향.

3. **`scripts/detect-docs-drift.py` 가 research-log `.md` 를 HTML 필요로 오탐한다.**
   변경된 모든 `.md` 를 HTML 로 매핑하는데, `docs/` 어디에도 `research-log.html` 이 없다
   (사이트가 게시하지 않는 규약). 이번엔 5건 오탐 → Step 11.5 에서 수동 배제했다.
   → 매핑에서 `research-log.md` 를 제외하거나, `docs/index.html` 등록 여부로 필터링.

4. **harness docs 페이지 accent 가 스펙과 불일치.** `docs/harness/*.html` 5개가
   `#0ea5e9`/`#14b8a6` 를 쓰는데 `references/css-tokens.md` 와 `docs/index.html` 의 Harness dot 은
   `#D97757` 이다. 선재 불일치이며 "기존 관례 유지" 최소 변경으로 두었다.
   → 재테마링은 별도 작업으로 판단.

### 이번 사이클 방법론 관찰 (다음 사이클에 유용)

- Phase 1~4 직렬 → Phase 5~14 병렬(웨이브 분할)이 유효했다. 단 **동시 5개는 API 529 를 유발**해
  4개가 중단됐고 `SendMessage` 로 컨텍스트 보존 재개했다. 이후 웨이브를 2~3개로 낮춰 재발 없음.
- 병렬 서브에이전트에게 **git 쓰기 금지 + 계약 파일 Phase 별 경로 분리**를 지시하고 커밋을
  오케스트레이터가 직렬 처리한 것이 index.lock 충돌을 0 으로 만들었다. 다음 사이클도 이 방식 권장.
- 각 Phase self-audit 이 **자기 날조를 스스로 검출**한 사례가 다수였다 (Pact 미사용 용어 인용,
  논문 수치 과대 인용, 검증 없이 단정한 콘솔 라벨). Phase 1 의 Evidence Gate 가 의도대로 작동.
- Final QA iter1 이 REJECT 하며 **오케스트레이터의 측정 oracle 오탐 3건**을 잡았다.
  자체 측정만으로 APPROVE 했다면 놓쳤을 것 — 독립 평가자 spawn 의 가치가 실증됐다.

## 2026-07-28 — CI 게이트 강화 (ci-gate-hardening, 카이젠 사이클 밖 후속 스프린트)

계약 `.harness/sprint-contract-ci-gate-hardening.md` 25/25 완료. PR #17 + #18.

### 무엇이 드러났나

직전 카이젠(PR #15)과 PR #16 이 main 을 처음 green 으로 만들었지만, **그 green 이 유지될
구조가 없었다**. 머지 전 독립 5 축 반증 검증에서 실측으로 드러난 것:

- `branches/main/protection` 404 · `rulesets` `[]` — main 계보 317 커밋 중 303(95.6%)이
  직접 푸시. Playwright 잡은 37 런 중 32 failure / **success 0**. 기록 시작(2026-04-12)부터
  한 번도 green 이 아니었다. (커밋·계약에 "2026-06-09 부터 5 회 연속" 으로 적었는데 **거짓**이었다 —
  최근 몇 런만 보고 쓴 오류. PR #16 본문에 정정을 박았다.)
- `docs/*.html` 은 생성물인데 4 개 규칙이 `.claude/skills/docs-site/` 어디에도 없었다.
- **회귀 메커니즘이 특정됐다**: `scripts/detect-docs-drift.py` 가 design-kit 매핑에서만 소스
  subdir 을 보존하는데 실제 출력은 flat 이라 26/26 전부 MISS → 전부 `[NEW]` 로 오보 →
  재생성 에이전트가 템플릿에서 새로 만들며 기존 수정을 날린다. 누락 prefix 4 종도 `.md` 20 개를
  감지 밖에 두고 있었다.
- 오버플로는 design-kit 4 페이지가 아니라 **146 중 66 페이지** 전역 결함이었다.

### 다음 사이클이 반복하지 말아야 할 것

- **"고쳤다" 와 "고친 것이 유지된다" 는 다르다.** 생성물만 고치면 다음 재생성에서 되돌아간다.
  docs/ 를 손대는 작업은 반드시 생성기(`docs-site/`)와 drift 감지기까지 함께 봐야 한다.
- **오라클이 의도를 재는지 매번 확인하라.** 이번에 세 번 틀렸다:
  (1) `el.scrollLeft=99999` 로 "스크롤 도달 가능" 을 쟀는데, `overflow:hidden` 은 프로그래밍
  스크롤만 되고 **사용자에겐 스크롤 수단이 없다**. 올바른 판정은
  `overflowX==='hidden' && scrollWidth>clientWidth`.
  (2) `grep 'width: *[0-9]{3,}px'` 가 `min-width`/`max-width` 를 substring 으로 잡아 매직넘버
  24 건을 오탐했다 (실제 0 건).
  (3) 단일행 `sed 's|/\*.*\*/||'` 가 **여러 줄 주석**을 못 걸러 `overflow:hidden` 재도입을
  1 건 오탐했다 (실제 0 건).
- **테스트를 통과한다 ≠ 결함이 없다.** 오버플로 0 을 달성한 뒤에도 29 페이지가
  `overflow:hidden` 으로 **잘라서** 통과하고 있었다. 그중 16 페이지는 진짜 내용 손실
  (표 오른쪽 열 최대 192px · `spacing-system` 은 1280px 에서도 104px, 11 행 중 5 행의 용도
  설명이 한 글자도 안 보였다). 나머지 12 페이지는 잘리는 것이 곧 전시물이라 고치면 안 됐다 —
  **분류 없이 일괄 수정했다면 디자인을 파괴했을 것이다.**
- **순서가 안전을 만든다.** `enforce_admins:true` 를 `release.sh` PR 전환보다 먼저 켰다면
  자기 수정을 push 하지 못하는 자물쇠 사고가 났다. A→B→C→D→머지→E 순서를 계약에 명시했다.

### 검증에서 효과가 컸던 것

- **독립 반증 워크플로**(5 축 × 적대적 verify)가 머지 전에 사실 오류 1 건을 잡았고 blocking 0 을
  확인했다. 자체 측정만으로 넘어갔다면 거짓 주장이 커밋·계약·PR 세 곳에 남았다.
- **QA evaluator 가 Linux 컨테이너**(`mcr.microsoft.com/playwright:v1.58.2-jammy`)로 146 페이지를
  재측정해 macOS 전용 측정의 플랫폼 드리프트 우려를 닫았다. 구현자가 못 한 검증을 평가자가 했다.
- **킷별 수정 + 킷별 독립 검증** 쌍이 66 페이지 / 29 페이지 두 작업 모두에서 위반 0 을 만들었다.
  특히 클리핑 작업은 검증자가 A/B 분류에 **29/29 동의**해야 통과하도록 설계한 것이 핵심이었다.
- **격리 클론 + 가짜 origin** 에서 `release.sh` 를 실제 실행해, 문법 검사만으로는 못 잡을
  버그를 찾았다 — `git tag -a` 가 기존 태그에 `fatal` 로 죽고 `set -e` 가 스크립트를 중단시켜
  **브랜치 push 와 PR 생성이 조용히 건너뛰어진다**.

### 남긴 부채

터치타겟 332 중 249 가 44px 미만(진짜 WCAG AA 위반 24: checkbox 20×20 이 19, button 4, li 1) ·
테마 키 파편화 4 종(`dk-theme` 12 / `theme` 3 / `vs-theme` 2 / `cp-theme` 2) · dependabot 부재 ·
액션 SHA 핀닝 · `visuals.spec.js` 위생(테스트명 `>=44px` 인데 단정 28/34/38, 44 단정 0 건 ·
146 중 13 페이지만 커버 · `KNOWN_OVERFLOW_PAGES` 80px 관용) · `validate-plugin.py` 가
`docs/*.html` 을 전혀 검사하지 않음 · `qa-evaluator.md` Step 5 가 파일 저장을 지시하나
frontmatter 에 Write 권한 없음 · protection 설정이 config-as-code 로 커밋돼 있지 않음
(`.harness/branch-protection-runbook.md` 가 SSOT 역할).

## 2026-08-13 — kaizen/2026-08-13 (cycle open)

**Cycle:** kaizen-2026-08-13
**Step 0:** `/insights` §0 = `~/.claude/usage-data/report.html` (2026-08-13T08:33:57, VERY FRESH 0.1h) ·
글로벌 feedback 279 (REJECT 110 / APPROVE 166) · hub 14 프로젝트 · local contract 10
**Step 0.5:** `sync-orchestrator.py --check-only` exit 0 (drift 없음, 10 plugins)

### Step 0.6 선별 결정

**사용자 선택: 전체 14 Phase · 전 Phase 직렬.** 신호 농도 산출 결과는 아래이며,
LOW 4 킷을 제외한 부분 실행을 제안했으나 사용자가 전체를 택했다.

- HIGH (8): 1 설계가이드 · 2 Contract · 3 Evaluator · 5 Flutter · 6 Design · 9 Rust · 12 Reflect · 13 Bambu
- MED (2): 4 Harness · 7 Backend
- LOW (4): 8 Infra · 10 React · 11 Planning · 14 Onboarding

### 이번 사이클 프레이밍 — §0 중복도 판정

`/insights` 2026-08-13 의 Friction #1~#3 은 직전 사이클(2026-07-27)에 이미 구조적으로 승격됐다
(Enforcement 3등급 / Evidence Validity Gate / Counterpart Enumeration / visual-change-protocol).
게다가 리포트 윈도(2026-06-12~08-12)가 그 수정 착지일(2026-07-28) **이전을 대부분 포함**한다.
→ **재출현 = 미측정이지 무효화가 아니다. 같은 규칙 재추가 금지.**
유효 신호는 (a) §0 신규 델타 D1~D5 (b) 2026-08-11~12 글로벌 REJECT (c) 2026-08 reflection 태그다.

### 신규 메타 이슈 (Step 0 에서 발견)

1. **SKILL.md Step 0 ↔ `collect-kaizen-data.py` 구현 불일치.** SKILL.md 는
   `<repo>/.claude/kaizen-input/insights-report.md` 자동 탐색과 `--insights=PATH` 인자를 문서화하는데
   스크립트는 **둘 다 미구현**이고 `~/.claude/usage-data/report.html` 만 고정 참조한다.
   결과: 사람이 큐레이션한 §0 델타 분석본이 데이터 풀에 들어가지 않는다 (이번엔 각 Phase 프롬프트에
   경로를 직접 전달하여 우회). → Phase 4 (harness-kaizen) 처리 대상.

### 이전 사이클 미해소 backlog (재검증 대상)

- `detect-docs-drift.py` 가 `research-log.md` → HTML 을 매핑하나 대응 페이지 없음 (5건 오탐)
- `detect-docs-drift.py` `plugin-validation-guide.html` suffix 불일치 (2026-06-11 부터 이월)
- `docs/harness/*.html` accent 가 `css-tokens.md` 스펙(`#D97757`)과 불일치
- `validate-plugin.py` 가 `docs/*.html` 을 전혀 검사하지 않음
- `qa-evaluator.md` Step 5 가 파일 저장을 지시하나 frontmatter 에 Write 권한 없음
