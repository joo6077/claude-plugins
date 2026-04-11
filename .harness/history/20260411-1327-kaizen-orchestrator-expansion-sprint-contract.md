---
feature: "Kaizen Orchestrator에 react-kit 추가 + 9 kaizen 스킬에 plugin-validation 통합"
created: "2026-04-11T13:30:00+09:00"
complexity: "복잡"
conditions: 16
scope: "kaizen-orchestrator 에 Phase 10 (react-kit) 추가 + 9개 kaizen 스킬 각각에 validate-plugin.py 결과 반영 Step 추가 + CLAUDE.md 9 Phase → 10 Phase 갱신"
---

## Orchestrator (kaizen-orchestrator/SKILL.md)
- [ ] OC-01: description 의 Phase 순서 목록에 "react-kit" 포함 (설계 → contract → evaluator → harness → flutter → design → backend → infra → rust → **react** → Final)
- [ ] OC-02: argument-hint 에 `phase10` 추가 (기존 phase1~9 + phase10 + final)
- [ ] OC-03: "Phase 의존성" 다이어그램 (ASCII) 에 `Phase 10: React-kit 카이젠 (react-kaizen)` 추가
- [ ] OC-04: "### Step 10: Phase 10 — React-kit 카이젠" 섹션 추가. rust-kit (Step 9) 과 일관된 형식: 범위 = `react-kit/skills/*/SKILL.md`, `react-kit/agents/*.md`, `react-kit/references/`, `docs/react/` 리서치 문서. 리서치 문서 부족 시 `/react-research` 선호출. Phase 1 가이드 변경 시 전수 감사.
- [ ] OC-05: "트리거 조건" 수동 목록에 `/kaizen-orchestrator phase10` 추가
- [ ] OC-06: Step 11 PR 생성 의 plugin.json bump 목록에 react-kit 추가
- [ ] OC-07: research-log 목록에 `docs/react/research-log.md` 추가 (존재 시)
- [ ] OC-08: "개별 카이젠과의 관계" 섹션의 개별 카이젠 리스트에 `/react-kaizen` 추가
- [ ] OC-09: Final Sprint Contract 의 "크로스 Phase 정합성 조건" 에 Phase 10 포함 문구 반영

## Plugin Validation Integration
- [ ] PV-01: 아래 **9개 kaizen 스킬** 각각에 "Step: Plugin Validation 체크 반영" 단계 추가:
  - `harness/skills/harness-kaizen/SKILL.md`
  - `harness/skills/contract-kaizen/SKILL.md`
  - `harness/skills/evaluator-kaizen/SKILL.md`
  - `flutter-toolkit/skills/flutter-kaizen/SKILL.md`
  - `.claude/skills/design-kaizen/SKILL.md`
  - `.claude/skills/backend-kaizen/SKILL.md`
  - `.claude/skills/infra-kaizen/SKILL.md`
  - `.claude/skills/rust-kaizen/SKILL.md`
  - `.claude/skills/react-kaizen/SKILL.md`
- [ ] PV-02: 각 kaizen 스킬에 "Step 실행 규칙" 이 명시됨 — (a) `python3 scripts/validate-plugin.py <해당 kit>` 실행, (b) V1~V7 결과를 읽어 ERROR 는 즉시 수정 / WARNING 은 개선 우선순위 높음 / PASS 는 skip, (c) `--fix` 자동 모드 먼저 시도 후 수동 보정
- [ ] PV-03: 각 kaizen 스킬의 References 섹션에 `harness/docs/guides/plugin-validation-guide.md` + `scripts/validate-plugin.py` 2개 링크 추가

## References 부속 문서
- [ ] RF-01: `.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` 파일이 존재한다면 Phase 10 추가. 없으면 skip (조건 자동 PASS)

## CLAUDE.md
- [ ] CD-01: `CLAUDE.md` 의 `/kaizen` 설명에 있는 "전체 9 Phase" → "전체 10 Phase" 로 갱신 + react-kit 포함되도록 Phase 목록 문구 수정
- [ ] CD-02: `CLAUDE.md` 의 "Kaizen Orchestration" 섹션 (있는 경우) 도 10 Phase 로 갱신 + react-kit 포함

## Diagnostics
- [ ] DG-01: 모든 수정 파일 내 TODO/TBD/FIXME 0건
- [ ] DG-02: 수정 후 `python3 scripts/validate-plugin.py --check=frontmatter` 실행 시 9개 kaizen 스킬 모두 V1 frontmatter PASS 유지 (user-invocable, name, description 등 회귀 없음)
