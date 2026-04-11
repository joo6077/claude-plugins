---
name: kaizen-orchestrator
description: >
  카이젠 전체 실행을 의존성 순서에 맞춰 오케스트레이션한다.
  설계 가이드 → contract → evaluator → harness → flutter-toolkit → design-kit → backend-kit → infra-kit → rust-kit → react-kit 순서로
  Phase별 실행하며, 각 Phase마다 자체 리서치 + Sprint Contract + QA Evaluator를 실행한다.
  주 1회 cron 자동 실행, 또는 수동 호출("/kaizen", "카이젠 전체 실행").
  개별 플러그인만 카이젠하려면 해당 카이젠 스킬을 직접 사용.
argument-hint: "[phase1|phase2|phase3|phase4|phase5|phase6|phase7|phase8|phase9|phase10|final]"
user-invocable: true
---

# Kaizen Orchestrator

설계 가이드 → contract → evaluator → harness → flutter-toolkit → design-kit → backend-kit → infra-kit → rust-kit → react-kit 순서로 카이젠을 실행한다.
각 Phase마다 자체 리서치 + Sprint Contract + QA Evaluator를 실행한다.
전체 Phase 완료 후 크로스 Phase 정합성을 최종 검증한다.

## 이 스킬 폴더의 파일

필요할 때 읽어라:

- `references/phase-dependencies.md` — Phase 간 의존성 맵 + 업데이트 순서 규칙
- `references/search-sources.md` — Phase 1 전용 리서치 소스 (스킬/에이전트 설계 패턴)

## Gotchas

- Phase 간 순서를 절대 바꾸지 마라 — 설계 가이드가 먼저 업데이트되어야 하위 스킬이 정합성을 유지한다
- 각 Phase의 QA가 REJECT되면 해당 Phase를 수정 후 재QA해라 — 다음 Phase로 넘어가지 마라
- 단일 브랜치에서 모든 Phase를 진행해라 — Phase별로 브랜치를 분리하면 의존성 반영이 깨진다
- Final QA에서 REJECT되면 해당 Phase로 돌아가 수정해라 — Final에서 새 기능을 추가하지 마라
- Phase 1에서 가이드를 변경했으면 이후 Phase에서 **모든** 기존 스킬/에이전트를 전수 체크해라 — 눈에 띄는 것만 수정하면 나머지가 누락된다. 테이블로 기록하여 누락을 방지
- 각 Phase의 리서치는 해당 카이젠 스킬이 자체 수행한다. 오케스트레이터는 순서만 관리한다.
- Phase 4(harness-kaizen)는 sprint-contract와 qa-evaluator를 개선 대상에서 제외한다. 이 둘은 Phase 2, 3에서 처리한다.
- 피드백이 0건인 Phase도 SKIP하지 않는다. 리서치 전용 모드로 진행한다.
- Regression 실패 카운터는 `.harness/.meta/kaizen-failure-count.yaml`에 Phase별로 영속화한다. 연속 2회 FAIL 시 해당 Phase를 일시 중단하고 사용자에게 알린다.
- 정리 정책(6개월 초과 삭제, 500개 제한)은 모든 Phase 완료 후 Final 단계에서 실행한다. 분석 중 데이터 손실을 방지한다.
- **Step 11.5 (docs-site 재생성) 과 Step 11.6 (글로벌 피드백 정리) 는 건너뛰기 금지.** 이 두 단계는 "조건부 실행" 이 아니라 **필수 실행** 이다. docs-site 가 빠지면 공개 HTML 문서가 카이젠 이전 상태에 멈추고, 피드백 정리가 빠지면 다음 사이클 data pool 품질이 저하된다.
- **Step 12 의 Post-Kaizen Checklist 는 PR 생성 전 blocking gate** 다. 하나라도 미통과면 PR 생성을 중단하고 해당 Step 으로 돌아간다. 체크리스트를 "대부분 OK" 로 넘기지 마라.
- **per-kit research-log 는 파일이 없어도 신규 생성하라.** 이전 조문 "존재 시 갱신" 은 영구 누락을 유발했다. `docs/{backend,infra,rust,react,flutter}/research-log.md` 가 없으면 반드시 만든다.
- **`<!-- AUTO:plugin_phases:begin -->
<!-- 이 섹션은 scripts/sync-orchestrator.py 에 의해 자동 생성됩니다.
     marketplace.json 을 변경한 뒤 스크립트를 재실행하면 동기화됩니다.
     직접 편집하지 마세요. -->

### Step 5: Phase 5 — flutter-toolkit 카이젠

**범위:** `flutter-toolkit/skills/*/SKILL.md`, `flutter-toolkit/references/`
, `docs/flutter/` 리서치 문서

공통 실행 패턴에 따라 `/flutter-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 flutter-toolkit 전 스킬을 전수 감사한다. flutter-toolkit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.5.1 · 2026-04-11] Flutter 개발 워크플로우 스킬 모음 (Riverpod 3.0 / Freezed 3.0 / go_router StatefulShellRoute)

### Step 6: Phase 6 — design-kit 카이젠

**범위:** `design-kit/skills/*/SKILL.md`, `design-kit/references/`
, `design-kit/docs/design/` 리서치 문서

공통 실행 패턴에 따라 `/design-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 design-kit 전 스킬을 전수 감사한다. design-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.2.1 · 2026-04-11] 스택 무관 UI/UX 디자인 가이드 + 감사 (OKLCH / DTCG v1 / WCAG 2.2 / Container Queries)

### Step 7: Phase 7 — backend-kit 카이젠

**범위:** `backend-kit/skills/*/SKILL.md`, `backend-kit/references/`
, `docs/backend/` 리서치 문서

공통 실행 패턴에 따라 `/backend-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 backend-kit 전 스킬을 전수 감사한다. backend-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.1.1 · 2026-04-11] 스택 무관 백엔드 개발 가이드 + 감사 + 아키텍처 세팅 (Hexagonal/Clean/DDD + OAuth 2.1 + Outbox + Pact)

### Step 8: Phase 8 — infra-kit 카이젠

**범위:** `infra-kit/skills/*/SKILL.md`, `infra-kit/references/`
, `docs/infra/` 리서치 문서

공통 실행 패턴에 따라 `/infra-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 infra-kit 전 스킬을 전수 감사한다. infra-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.1.1 · 2026-04-11] 스택 무관 인프라/DevOps 가이드 + 감사 + 초기 세팅 (K8s PSA / Terraform 1.10 / SLSA / OTel)

### Step 9: Phase 9 — rust-kit 카이젠

**범위:** `rust-kit/skills/*/SKILL.md`, `rust-kit/references/`
, `docs/rust/` 리서치 문서

공통 실행 패턴에 따라 `/rust-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 rust-kit 전 스킬을 전수 감사한다. rust-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.1.1 · 2026-04-11] Rust 전용 백엔드 개발 워크플로우 — Rust 2024 / Axum 0.8 / SeaORM 1.1 / Clippy 2026

### Step 10: Phase 10 — react-kit 카이젠

**범위:** `react-kit/skills/*/SKILL.md`, `react-kit/references/`
, `docs/react/` 리서치 문서

공통 실행 패턴에 따라 `/react-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 react-kit 전 스킬을 전수 감사한다. react-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.1.1 · 2026-04-11] React + Vite + Tauri 2 + Rust WASM 개발 워크플로우 — React 19 / TanStack Query v5 / Tauri 2 GA / Tailwind v4 / Zustand v5, 라이브러리 0개 애니메이션

<!-- /sync-orchestrator.py 자동 생성 끝. 다음 사이클 전에 marketplace.json 을 수정했으면 다시 실행하세요. -->
<!-- AUTO:plugin_phases:end -->` 마커 영역을 직접 편집하지 마라.** 이 영역은 `scripts/sync-orchestrator.py` 가 `marketplace.json` 을 기반으로 자동 생성한다. 킷 추가/수정/삭제 시 marketplace.json 을 고친 뒤 `python3 scripts/sync-orchestrator.py` 를 실행하면 이 섹션이 동기화된다. 직접 편집 시 다음 실행에서 덮어써진다.
- **Step 0.5 Orchestrator Self-Audit 는 건너뛰기 금지.** 이전 사이클의 수동 개입 이력 (`.harness/.meta/orchestrator-audit-log.md`) 과 `sync-orchestrator.py --check-only` drift 를 먼저 확인해야 Phase 1 로 진입한다.

## Phase 의존성

```text
Step 0:   Pre-flight — 피드백 데이터 풀 수집 (scripts/collect-kaizen-data.py)
    ↓
Step 0.5: Orchestrator Self-Audit — 이전 사이클 meta-feedback 반영 + sync-orchestrator drift 확인
    ↓
Phase 1: 설계 가이드 카이젠
    ↓
Phase 2: Contract 카이젠 (contract-kaizen)
    ↓
Phase 3: Evaluator 카이젠 (evaluator-kaizen)
    ↓
Phase 4: Harness 카이젠 (harness-kaizen)
    ↓
Phase 5: Flutter-toolkit 카이젠 (flutter-kaizen)
    ↓
Phase 6: Design-kit 카이젠 (design-kaizen)
    ↓
Phase 7: Backend-kit 카이젠 (backend-kaizen)
    ↓
Phase 8: Infra-kit 카이젠 (infra-kaizen)
    ↓
Phase 9: Rust-kit 카이젠 (rust-kaizen)
    ↓
Phase 10: React-kit 카이젠 (react-kaizen)
    ↓
Final: 전체 정합성 검증
```

### Phase 순서 논리

1. 설계 가이드가 최상위 — 모든 스킬/에이전트 설계의 기준
2. Contract 카이젠 — 계약 작성 원칙 개선 (contract-design-guide + sprint-contract)
3. Evaluator 카이젠 — 평가 방법론 개선 (qa-evaluation-guide + qa-evaluator). Phase 2에서 contract-schema 변경 시 반영.
4. Harness 카이젠 — sprint-contract, qa-evaluator **제외**한 나머지 harness 스킬/설정 (sprint-feedback, init, project.yaml, procedures)
5. Flutter-toolkit 카이젠 — Flutter 스킬 개선
6. Design-kit 카이젠 — UI/UX 디자인 스킬 개선
7. Backend-kit 카이젠 — 백엔드 스킬 개선 (docs/backend/ 리서치 기준)
8. Infra-kit 카이젠 — 인프라/DevOps 스킬 개선 (docs/infra/ 리서치 기준)
9. Rust-kit 카이젠 — Rust 백엔드 스킬 개선 (docs/rust/ 리서치 기준)
10. React-kit 카이젠 — React + Vite + Tauri + WASM 스킬 개선 (docs/react/ 리서치 기준)

## 트리거 조건

### 주기적 (cron)
- 매주 월요일 09:00 KST
- Claude Code schedule (remote trigger) 사용
- 개별 카이젠(contract-kaizen, evaluator-kaizen, harness-kaizen, flutter-kaizen, design-kaizen)의 cron은 비활성화하고 이 오케스트레이터만 실행

### 수동
- `/kaizen-orchestrator` — 전체 (Phase 1→2→3→4→5→6→7→8→9→10→Final)
- `/kaizen-orchestrator phase1` — 설계 가이드만
- `/kaizen-orchestrator phase2` — contract-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase3` — evaluator-kaizen만 (Phase 2 완료 전제)
- `/kaizen-orchestrator phase4` — harness-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase5` — flutter-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase6` — design-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase7` — backend-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase8` — infra-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase9` — rust-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase10` — react-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator final` — Final QA만 (Phase 1~10 완료 전제)

## Process

### 각 Phase 공통 실행 패턴

각 Phase는 **새 서브에이전트**로 실행한다 (Agent tool). 이전 Phase의 변경사항이 디스크에 커밋되어 있으므로 fresh load로 반영된다.

```text
1. Triage: 피드백 읽기 → 개선 필요? → 불필요 시 SKIP + 로그
   ⚠ 피드백이 0건이면 SKIP하지 않고 리서치 전용 모드로 진행
2. 자체 리서치: 해당 스킬의 search-sources.md 기반, 3-5개 도메인만
3. GAP 분석: 리서치 + 피드백 + 현재 스킬/가이드 대조
4. 예방적 분석: 리서치 anti-pattern을 현재 프롬프트에 대조
5. Sprint Contract (DRAFT): 현재 버전 sprint-contract 사용
6. 개선안 DRAFT 작성 (파일 미적용)
7. QA Evaluator: 현재 버전으로 DRAFT 평가
8. APPROVE → kaizen-phase-N-pre 태그 생성 → 파일 적용 + 커밋 → Regression Smoke Test
9. Regression 실패 → git revert (kaizen-phase-N-pre 태그) → BLOCKED
10. 다음 Phase → 새 서브에이전트 (fresh load)
```

### Regression 실패 카운터

Phase 완료 후 `.harness/.meta/kaizen-failure-count.yaml`을 업데이트한다:
- Regression PASS → 해당 Phase 카운터 0으로 리셋
- Regression FAIL → 해당 Phase 카운터 +1
- 카운터 >= 2 → Phase 일시 중단 + 사용자 에스컬레이션

### Step 0: Pre-flight — 피드백 데이터 풀 수집 (Phase 1 이전 **필수** 실행)

모든 Phase 1~10 서브에이전트가 공유할 **통합 데이터 풀**을 먼저 생성한다. 이는 각 Phase 가 단절된 리서치에 매몰되지 않고 글로벌 피드백·외부 프로젝트·followup 이슈를 근거로 개선하도록 보장한다.

**실행:**

```bash
python3 scripts/collect-kaizen-data.py
```

**출력:** `.harness/.meta/kaizen-data-pool.md`

**수집 소스 (스크립트 내장):**

1. **글로벌 Evaluator 피드백** — `~/.harness/feedback/evaluator/*.yaml`
   - verdict 분포 (APPROVE/REJECT)
   - skill/project 분포
   - 최근 REJECT 사유 Top 20
   - 최근 improvement_suggestions Top 15
2. **외부 프로젝트 피드백** — `~/Hub/10_Dev/*/.harness/`
   - `sprint-feedback.md` 앞부분 (실사용 현장의 QA 리포트)
   - `history/*-sprint-contract.md` 최근 5개 (사용자가 어떤 계약을 자주 작성하는지)
3. **followup 문서** — `docs/superpowers/followup-*.md` 최근 5개 (해결되지 않은 숙제 목록)
4. **레포 sprint-contract 이력** — `.harness/history/*-sprint-contract.md` 최근 10개
5. **validate-plugin 스냅샷** — `python3 scripts/validate-plugin.py` 현재 실행 결과 (7 kit 상태)
   - `--skip-validate` 옵션으로 생략 가능

**Phase 별 참조 매핑** (데이터 풀 §6 에 테이블 포함):

| Phase | 주요 참조 섹션 |
|-------|-------------|
| 1 설계 가이드 | §1 improvement suggestions |
| 2 Contract | §1 reject 사유 (계약 모호성 패턴) |
| 3 Evaluator | §1 improvement (L3 커버리지, set intersection) |
| 4 Harness | §5 validate-plugin 현재 상태 |
| 5 Flutter | §2 Hub 외부 프로젝트 (fit-pal, apps) |
| 6 Design | §5 validate-plugin 현재 상태 |
| 7 Backend | §1 backend 관련 feedback |
| 8 Infra | §5 validate-plugin 현재 상태 |
| 9 Rust | §2 Hub 외부 프로젝트 (fit-pal server) |
| 10 React | §3 followup-2026-04-11, §5 |

**각 Phase 서브에이전트 프롬프트에 데이터 풀 경로 전달 필수:**

```text
데이터 소스:
- `.harness/.meta/kaizen-data-pool.md` — 카이젠 공통 데이터 풀 (Step 0 에서 생성)
  너의 Phase 범위에 해당하는 섹션 (§N) 을 우선 참조.
```

**Gotchas:**

- Step 0 을 건너뛰고 Phase 1 부터 시작하지 마라 — 각 Phase 가 같은 데이터를 다시 수집하면 중복 작업이다.
- 데이터 풀은 Phase 진행 중에는 재생성하지 마라 — Phase 별로 상태가 흔들린다. 전체 카이젠 종료 후 다음 사이클에 다시 수집한다.
- 데이터 풀 파일은 스크립트 생성물이므로 직접 수정 금지. 내용이 틀리면 수집 로직(`scripts/collect-kaizen-data.py`)을 고친다.
- 글로벌 feedback 이 0건이어도 Step 0 은 실행한다 — 외부 프로젝트 피드백이나 followup 은 여전히 유효할 수 있다.

### Step 0.5: Orchestrator Self-Audit (자동 — 건너뛰기 금지)

**목적:** 이전 카이젠 사이클에서 오케스트레이터 자체에 발생한 meta-issue (docs-site 누락, per-kit research-log 누락, 신규 킷 미반영 등) 를 이번 사이클에 반영한다. 이 단계가 없으면 오케스트레이터 SKILL.md 는 "메타 레벨 사각지대" 로 영구 개선되지 않는다.

**절차:**

1. `.harness/.meta/orchestrator-audit-log.md` 읽기 — 이전 사이클의 수동 개입 이력 확인
   - 파일이 없으면 "첫 실행" 으로 간주하고 빈 이력으로 진행
   - 이력이 있으면 각 meta-issue 가 이번 사이클에서도 반복되지 않았는지 후속 Phase subagent 프롬프트에 "지난 사이클 meta-issue 재검증" 지시 포함
2. `python3 scripts/sync-orchestrator.py --check-only` 실행
   - exit 0 → drift 없음, Phase 1 로 진행
   - exit 1 → drift 있음 (marketplace.json 이 SKILL.md 와 불일치). `python3 scripts/sync-orchestrator.py` 를 먼저 실행하여 동기화 후 재시도
   - exit 2 → 구조적 에러 (마커 누락, 파일 없음). 사용자 에스컬레이션
3. Post-Kaizen Checklist 이력 조회 — `.harness/history/` 의 최근 10개 sprint-contract archive 에서 FAIL 항목 추출
   - 반복 발생 항목이 있으면 해당 Step 의 Gotchas 를 강화하는 meta-fix 를 Phase 4 (harness-kaizen) subagent 에 전달
4. `.harness/.meta/orchestrator-audit-log.md` 에 이번 사이클 엔트리 append (initial-empty — 실제 meta-issue 는 사이클 종료 시 Step 11 이후에 기록)

**Gotchas:**

- 이 단계를 건너뛰면 오케스트레이터 자체 개선이 발생하지 않는다
- `sync-orchestrator.py --check-only` drift 가 있는데 Phase 1 로 진행하지 마라 — AUTO 영역이 어긋난 채 Phase 가 실행되면 소스 파일과 SKILL.md 가 다른 킷 목록을 가리킨다
- audit-log 는 append-only. 기존 엔트리를 수정/삭제하지 마라

### Step 1: Phase 1 — 설계 가이드 카이젠

**범위:** `harness/docs/guides/skill-design-guide.md`, `harness/docs/guides/agent-design-guide.md`

공통 실행 패턴에 따라 서브에이전트로 실행. 리서치 소스는 `references/search-sources.md`.

### Step 2: Phase 2 — Contract 카이젠

**범위:** `harness/docs/guides/contract-design-guide.md`, `harness/skills/sprint-contract/SKILL.md`

공통 실행 패턴에 따라 `/contract-kaizen` 서브에이전트로 실행. Phase 1에서 설계 가이드가 변경되었으면 정합성 반영.

### Step 3: Phase 3 — Evaluator 카이젠

**범위:** `harness/docs/guides/qa-evaluation-guide.md`, `harness/agents/qa-evaluator.md`

공통 실행 패턴에 따라 `/evaluator-kaizen` 서브에이전트로 실행. Phase 2에서 contract-schema가 변경되었으면 반영.

### Step 4: Phase 4 — Harness 카이젠

**범위:** `harness/skills/*/SKILL.md` (sprint-contract, qa-evaluator **제외**), `.harness/project.yaml`, `harness/agents/` (qa-evaluator **제외**)

공통 실행 패턴에 따라 `/harness-kaizen` 서브에이전트로 실행. sprint-contract와 qa-evaluator는 Phase 2, 3에서 이미 처리되었으므로 제외.

<!-- AUTO:plugin_phases:begin -->
<!-- 이 섹션은 scripts/sync-orchestrator.py 에 의해 자동 생성됩니다.
     marketplace.json 을 변경한 뒤 스크립트를 재실행하면 동기화됩니다.
     직접 편집하지 마세요. -->

### Step 5: Phase 5 — flutter-toolkit 카이젠

**범위:** `flutter-toolkit/skills/*/SKILL.md`, `flutter-toolkit/references/`, `docs/flutter/` 리서치 문서

공통 실행 패턴에 따라 `/flutter-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 flutter-toolkit 전 스킬을 전수 감사한다. flutter-toolkit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: Flutter 개발 워크플로우 스킬 모음

### Step 6: Phase 6 — design-kit 카이젠

**범위:** `design-kit/skills/*/SKILL.md`, `design-kit/references/`, `design-kit/docs/design/` 리서치 문서

공통 실행 패턴에 따라 `/design-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 design-kit 전 스킬을 전수 감사한다. design-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: 스택 무관 UI/UX 디자인 가이드 + 감사 플러그인

### Step 7: Phase 7 — backend-kit 카이젠

**범위:** `backend-kit/skills/*/SKILL.md`, `backend-kit/references/`, `docs/backend/` 리서치 문서

공통 실행 패턴에 따라 `/backend-kaizen` 서브에이전트로 실행. 리서치 문서가 부족하면 `/backend-research` 를 먼저 호출하여 `docs/backend/` 를 갱신한 뒤 진행한다. Phase 1 에서 설계 가이드가 변경되었으면 backend-kit 전 스킬을 전수 감사한다.

> 플러그인 설명: 스택 무관 백엔드 개발 가이드 + 감사 + 아키텍처 세팅 플러그인

### Step 8: Phase 8 — infra-kit 카이젠

**범위:** `infra-kit/skills/*/SKILL.md`, `infra-kit/references/`, `docs/infra/` 리서치 문서

공통 실행 패턴에 따라 `/infra-kaizen` 서브에이전트로 실행. 리서치 문서가 부족하면 `/infra-research` 를 먼저 호출하여 `docs/infra/` 를 갱신한 뒤 진행한다. Phase 1 에서 설계 가이드가 변경되었으면 infra-kit 전 스킬을 전수 감사한다.

> 플러그인 설명: 스택 무관 인프라/DevOps 가이드 + 감사 + 초기 세팅 플러그인

### Step 9: Phase 9 — rust-kit 카이젠

**범위:** `rust-kit/skills/*/SKILL.md`, `rust-kit/references/`, `docs/rust/` 리서치 문서

공통 실행 패턴에 따라 `/rust-kaizen` 서브에이전트로 실행. 리서치 문서가 부족하면 `/rust-research` 를 먼저 호출하여 `docs/rust/` 를 갱신한 뒤 진행한다. `/rust-kaizen` 스킬 자체는 이 레포 개발용이며 rust-kit 플러그인에 포함되지 않는다 — 개선 대상은 rust-kit 플러그인 스킬이다. Phase 1 에서 설계 가이드가 변경되었으면 rust-kit 전 스킬을 전수 감사한다.

> 플러그인 설명: Rust 전용 백엔드 개발 워크플로우 플러그인

### Step 10: Phase 10 — react-kit 카이젠

**범위:** `react-kit/skills/*/SKILL.md`, `react-kit/agents/*.md`, `react-kit/references/`, `docs/react/` 리서치 문서

공통 실행 패턴에 따라 `/react-kaizen` 서브에이전트로 실행. 리서치 문서가 부족하면 `/react-research` 를 먼저 호출하여 `docs/react/` 를 갱신한 뒤 진행한다. `/react-kaizen` 스킬 자체는 이 레포 개발용이며 react-kit 플러그인에 포함되지 않는다 — 개선 대상은 react-kit 플러그인에 포함된 21개 스킬 + 3개 에이전트다. Phase 1 에서 설계 가이드가 변경되었으면 react-kit 전 스킬을 전수 감사한다.

**특별 주의**: react-kit 의 G5b 애니메이션 스킬 (`react-animation`) 과 animation-architect-react 에이전트, 그리고 `react-audit` 의 Library Policy 카테고리는 **라이브러리 0개 원칙** (Motion / framer-motion / dnd-kit / react-spring / react-transition-group / animate.css 등 빌드 게이트급 금지) 을 빌드 게이트로 enforce 한다. 이 원칙은 카이젠에서 절대 완화하지 말고, 신규 금지 라이브러리 추가만 허용한다.

> 플러그인 설명: React + Vite + Tauri 2 + Rust WASM 개발 워크플로우 플러그인
<!-- AUTO:plugin_phases:end -->

**특별 주의**: react-kit 의 G5b 애니메이션 스킬 (`react-animation`) 과 animation-architect-react 에이전트, 그리고 `react-audit` 의 Library Policy 카테고리는 **라이브러리 0개 원칙** (Motion/framer-motion/dnd-kit/react-spring/react-transition-group 등 빌드 게이트급 금지) 을 빌드 게이트로 enforce 한다. 이 원칙은 카이젠에서 절대 완화하지 말고, 신규 금지 라이브러리 추가만 허용한다.

### Step 11: Final — 전체 정합성 검증

**범위:** Phase 1~10 전체 변경사항

1. **Final Sprint Contract 생성:**
   - 크로스 Phase 정합성 조건:
     - Phase 1에서 업데이트된 설계 원칙이 Phase 2~10 변경에 반영되었는가
     - Phase 2 contract 변경이 Phase 3 evaluator와 정합하는가
     - Phase 4 harness 변경이 Phase 5~10 (flutter-toolkit, design-kit, backend-kit, infra-kit, rust-kit, react-kit)과 충돌하지 않는가
     - 버전 번호가 각 플러그인에서 올바르게 업데이트되었는가
     - changelog, research-log이 모든 Phase 변경을 포함하는가
   - Diagnostics: 전체 `bash -n` 검증

2. **QA Evaluator 실행:**
   - **APPROVE** → Step 11.5 로 진행
   - **REJECT** → 해당 Phase로 돌아가 수정 후 Final 재실행

### Step 11.5: docs-site 재생성 (자동 — 건너뛰기 금지)

**목적:** 각 Phase 에서 변경된 `.md` 리서치/가이드 소스 파일에 대응하는 `docs/*.html` 시각 페이지를 재생성한다. 이 단계가 없으면 docs site 가 카이젠 이전 상태에 멈춘다.

**실행 방식:** `Skill` 도구로 `docs-site` 스킬을 호출한다. 변경된 소스를 기반으로 HTML 페이지를 재생성한다. subagent 로 위임해도 좋다.

**소스 → 출력 매핑 (docs-site 스킬 Step 1 참조):**

| 플러그인 | 소스 경로 | 출력 경로 |
| -------- | --------- | --------- |
| harness | `harness/docs/guides/`, `harness/references/` | `docs/harness/` |
| flutter-toolkit | `flutter-toolkit/references/` | `docs/flutter-toolkit/` |
| design-kit | `design-kit/docs/design/` | `docs/design-kit/` |
| backend-kit | `docs/backend/` | `docs/backend-kit/` |
| infra-kit | `docs/infra/` | `docs/infra-kit/` |
| rust-kit | `rust-kit/references/`, `docs/rust/` | `docs/rust-kit/` |
| react-kit | `react-kit/references/`, `docs/react/` | `docs/react-kit/` |
| process (공유) | (내부 문서) | `docs/process/` |

**절차:**

1. `git diff {병합_base}..HEAD --name-only` 로 본 카이젠 사이클에서 변경된 소스 `.md` / `.yaml` 파일 목록 확보
2. 매핑 테이블에 따라 대응하는 `docs/<plugin>/<name>.html` 파일 식별
3. 각 HTML 페이지를 docs-site 스킬 원칙 (standalone, 최소 400 라인, design-kit audit-criteria 준수, card-source URL 인용, accent 컬러) 로 재생성
4. `docs/index.html` `categories` 배열에 신규/갱신 페이지 등록
5. `python3 scripts/validate-plugin.py` 로 7 OK 재확인

**Gotchas:**

- docs-site 재생성을 건너뛰면 GitHub Pages 의 공개 문서가 카이젠 이전 상태에 고정된다
- 소스 `.md` 변경이 없는 플러그인은 재생성하지 않아도 된다 (불필요한 diff 방지)
- 한 파일만 수정되어도 대응 HTML 은 전체 재렌더링 해야 한다 (부분 패치 금지)

### Step 11.6: 글로벌 피드백 정리 (자동 — 건너뛰기 금지)

Step 11.5 이후 실행. 다음 카이젠 사이클의 data pool 품질 유지를 위해 오래되거나 누적된 피드백을 정리한다.

1. `bash harness/scripts/feedback-path.sh` 로 경로 확인
2. 6개월 초과 파일 삭제 (oldest-first) — `find $PATH -type f -mtime +180 -delete`
3. 500개 초과 시 oldest-first 로 삭감
4. 정리 로그를 `.harness/.meta/cleanup-log.yaml` 에 append
5. 삭제 액션이 0 건이어도 로그 엔트리는 추가 (실행 증거 확보)

**cleanup-log.yaml 예시:**

```yaml
cleanup_log:
  - date: "2026-04-11"
    total_before: 85
    aged_over_6months: 0
    over_500_truncated: 0
    deleted: 0
    notes: "no action needed"
```

### Step 12: PR 생성

1. **버전 업데이트:**
   - harness 변경 있으면: `harness/.claude-plugin/plugin.json` 버전 bump
   - flutter-toolkit 변경 있으면: `flutter-toolkit/.claude-plugin/plugin.json` 버전 bump
   - design-kit 변경 있으면: `design-kit/.claude-plugin/plugin.json` 버전 bump
   - backend-kit 변경 있으면: `backend-kit/.claude-plugin/plugin.json` 버전 bump
   - infra-kit 변경 있으면: `infra-kit/.claude-plugin/plugin.json` 버전 bump
   - rust-kit 변경 있으면: `rust-kit/.claude-plugin/plugin.json` 버전 bump
     (⚠ `/rust-kaizen` 스킬은 이 레포 개발용으로 rust-kit 플러그인에 포함되지 않는다 — bump 대상은 rust-kit 플러그인에 포함된 스킬뿐)
   - react-kit 변경 있으면: `react-kit/.claude-plugin/plugin.json` 버전 bump
     (⚠ `/react-kaizen` 스킬은 이 레포 개발용으로 react-kit 플러그인에 포함되지 않는다 — bump 대상은 react-kit 플러그인에 포함된 스킬뿐)
   - `.claude-plugin/marketplace.json` 갱신 (모든 플러그인 description 날짜/버전 동기화)

2. **changelog 업데이트 (모든 Phase 변경 반영 — 건너뛰기 금지):**
   - `docs/kaizen/changelog.md` (harness 관련, Phase 1~4)
   - `docs/kaizen/flutter-changelog.md` (flutter 관련, Phase 5) — **이 파일이 존재하면 반드시 Phase 5 엔트리 추가**
   - 존재하지 않는 per-plugin changelog 파일은 research-log 에서 대체

3. **research-log 업데이트 (per-kit 자동 생성 — "존재 시" 조문 제거):**
   - `docs/kaizen/research-log.md` (harness 관련, Phase 1~4)
   - `docs/kaizen/flutter-research-log.md` (flutter 관련, Phase 5) — **파일이 존재하면 반드시 Phase 5 엔트리 추가**
   - `docs/backend/research-log.md` (backend 관련, Phase 7) — **파일이 없으면 신규 생성**
   - `docs/infra/research-log.md` (infra 관련, Phase 8) — **파일이 없으면 신규 생성**
   - `docs/rust/research-log.md` (rust 관련, Phase 9) — **파일이 없으면 신규 생성**
   - `docs/react/research-log.md` (react 관련, Phase 10) — **파일이 없으면 신규 생성**
   - `docs/flutter/research-log.md` (flutter 관련, Phase 5) — **파일이 없으면 신규 생성**
   - 각 per-kit research-log 는 frontmatter (title, version, last_updated), "## [YYYY-MM-DD] - Phase N kaizen" 엔트리, 리서치 소스 URL 최소 5 건 포함.

4. **evals 갱신 체크:**
   - 각 플러그인 `evals/evals.json` (존재 시) 의 `id` 필드와 현재 `<plugin>/skills/` 디렉토리의 스킬 목록이 일치하는지 확인
   - 스킬이 신규 추가 / 삭제 / 리네임되었으면 evals.json 도 갱신
   - 정합성 유지 확인을 `.harness/.meta/evals-audit-{YYYY-MM-DD}.md` 에 기록 (변경 없음이어도 점검 기록)

5. **kaizen-failure-count.yaml 업데이트:**
   - `.harness/.meta/kaizen-failure-count.yaml` 에 `phase_1` ~ `phase_10` 엔트리가 모두 존재하는지 확인 (없으면 추가)
   - Regression PASS 인 Phase 는 카운터 0 으로 리셋
   - Regression FAIL 인 Phase 는 카운터 +1 → 2 이상이면 사용자 에스컬레이션
   - `last_updated` 필드를 카이젠 실행 날짜로 갱신
   - REJECT → iter2 APPROVE 흐름이 있었으면 해당 Phase 엔트리에 주석으로 기록

6. **Post-Kaizen Checklist (최종 검증 — 모든 항목 PASS 후에만 PR 생성):**

   아래 체크리스트를 **완전히** 통과하지 않으면 PR 생성을 **금지**한다. 하나라도 미통과 시 해당 Step 으로 돌아가 수정한다.

   - [ ] 각 변경된 플러그인 `plugin.json` 버전이 bump 되었다
   - [ ] `.claude-plugin/marketplace.json` 의 7개 플러그인 `description` 이 버전/날짜와 정합한다
   - [ ] `python3 scripts/sync-docs.py --check-only` 가 "모든 README가 동기화 상태입니다" 를 반환한다
   - [ ] `python3 scripts/validate-plugin.py` 가 Total 7 plugins, 7 OK, Exit 0 을 반환한다
   - [ ] `docs/kaizen/changelog.md` 에 이번 사이클 엔트리가 추가되었다 (Phase 1~4 변경 반영)
   - [ ] `docs/kaizen/flutter-changelog.md` 에 Phase 5 엔트리가 추가되었다 (해당 Phase 변경 있을 시)
   - [ ] `docs/kaizen/research-log.md` + `docs/kaizen/flutter-research-log.md` + per-kit research-log 5개 파일이 모두 존재하고 이번 사이클 엔트리를 포함한다
   - [ ] Step 11.5 docs-site 재생성이 실행되었다 — 변경된 소스에 대응하는 `docs/<plugin>/*.html` 이 최신 상태다
   - [ ] Step 11.6 글로벌 피드백 정리가 실행되었다 — `.harness/.meta/cleanup-log.yaml` 에 이번 사이클 엔트리가 있다
   - [ ] `.harness/.meta/kaizen-failure-count.yaml` `last_updated` 필드가 이번 사이클 날짜다
   - [ ] `.harness/.meta/evals-audit-{YYYY-MM-DD}.md` 가 존재한다 (evals 점검 기록)
   - [ ] Phase 1~10 간 scope 격리가 유지되었다 — 각 Phase commit 이 다른 Phase 의 소스 파일을 수정하지 않았다

7. **PR 생성:**
   - 브랜치명: `kaizen/{날짜}`
   - PR 제목: `[kaizen] {Phase별 핵심 변경 요약}`
   - PR 본문: Phase별 변경 내역 + Final QA 결과 + Post-Kaizen Checklist 결과

   ```bash
   git push -u origin kaizen/{YYYY-MM-DD}
   gh pr create --title "[kaizen] {요약}" --body "{본문}"
   ```

## Phase 스킵 규칙

- Phase의 ANALYZE에서 개선 포인트가 0개면 해당 Phase를 스킵한다
- 스킵된 Phase는 Sprint Contract/QA 없이 다음 Phase로 진행
- 모든 Phase가 스킵이면 research-log에 "개선 포인트 없음" 기록 후 종료 (PR 생성 안 함)
- Final은 최소 1개 Phase가 실행되었을 때만 실행

## 개별 카이젠과의 관계

- `/contract-kaizen`, `/evaluator-kaizen`, `/harness-kaizen`, `/flutter-kaizen`, `/design-kaizen`, `/backend-kaizen`, `/infra-kaizen`, `/rust-kaizen`, `/react-kaizen`은 **독립 실행 가능** — 긴급 수정이나 특정 영역만 업데이트할 때
- 독립 실행 시에는 오케스트레이터 순서를 따르지 않음 (자체 프로세스 실행)
- 정기 cron은 **오케스트레이터만 실행** — 개별 카이젠 cron은 비활성화
