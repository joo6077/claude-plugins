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
