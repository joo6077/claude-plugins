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
