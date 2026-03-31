---
name: kaizen-orchestrator
description: >
  카이젠 전체 실행을 의존성 순서에 맞춰 오케스트레이션한다.
  설계 가이드 → contract → evaluator → harness → flutter-toolkit → design-kit 순서로
  Phase별 실행하며, 각 Phase마다 자체 리서치 + Sprint Contract + QA Evaluator를 실행한다.
  주 1회 cron 자동 실행, 또는 수동 호출("/kaizen", "카이젠 전체 실행").
  개별 플러그인만 카이젠하려면 해당 카이젠 스킬을 직접 사용.
argument-hint: "[phase1|phase2|phase3|phase4|phase5|phase6|final]"
user-invocable: true
---

# Kaizen Orchestrator

설계 가이드 → contract → evaluator → harness → flutter-toolkit → design-kit 순서로 카이젠을 실행한다.
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

## Phase 의존성

```
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
Final: 전체 정합성 검증
```

### Phase 순서 논리

1. 설계 가이드가 최상위 — 모든 스킬/에이전트 설계의 기준
2. Contract 카이젠 — 계약 작성 원칙 개선 (contract-design-guide + sprint-contract)
3. Evaluator 카이젠 — 평가 방법론 개선 (qa-evaluation-guide + qa-evaluator). Phase 2에서 contract-schema 변경 시 반영.
4. Harness 카이젠 — sprint-contract, qa-evaluator **제외**한 나머지 harness 스킬/설정 (sprint-feedback, init, project.yaml, procedures)
5. Flutter-toolkit 카이젠 — Flutter 스킬 개선
6. Design-kit 카이젠 — UI/UX 디자인 스킬 개선

## 트리거 조건

### 주기적 (cron)
- 매주 월요일 09:00 KST
- Claude Code schedule (remote trigger) 사용
- 개별 카이젠(contract-kaizen, evaluator-kaizen, harness-kaizen, flutter-kaizen, design-kaizen)의 cron은 비활성화하고 이 오케스트레이터만 실행

### 수동
- `/kaizen-orchestrator` — 전체 (Phase 1→2→3→4→5→6→Final)
- `/kaizen-orchestrator phase1` — 설계 가이드만
- `/kaizen-orchestrator phase2` — contract-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase3` — evaluator-kaizen만 (Phase 2 완료 전제)
- `/kaizen-orchestrator phase4` — harness-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase5` — flutter-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase6` — design-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator final` — Final QA만 (Phase 1~6 완료 전제)

## Process

### 각 Phase 공통 실행 패턴

각 Phase는 **새 서브에이전트**로 실행한다 (Agent tool). 이전 Phase의 변경사항이 디스크에 커밋되어 있으므로 fresh load로 반영된다.

```
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

### Step 5: Phase 5 — Flutter-toolkit 카이젠

**범위:** `flutter-toolkit/skills/*/SKILL.md`, `flutter-toolkit/references/`, `flutter-toolkit/evals/`

공통 실행 패턴에 따라 `/flutter-kaizen` 서브에이전트로 실행.

### Step 6: Phase 6 — Design-kit 카이젠

**범위:** `design-kit/skills/*/SKILL.md`, `design-kit/references/`

공통 실행 패턴에 따라 `/design-kaizen` 서브에이전트로 실행.

### Step 7: Final — 전체 정합성 검증

**범위:** Phase 1~6 전체 변경사항

1. **Final Sprint Contract 생성:**
   - 크로스 Phase 정합성 조건:
     - Phase 1에서 업데이트된 설계 원칙이 Phase 2~6 변경에 반영되었는가
     - Phase 2 contract 변경이 Phase 3 evaluator와 정합하는가
     - Phase 4 harness 변경이 Phase 5 flutter-toolkit, Phase 6 design-kit과 충돌하지 않는가
     - 버전 번호가 각 플러그인에서 올바르게 업데이트되었는가
     - changelog, research-log이 모든 Phase 변경을 포함하는가
   - Diagnostics: 전체 `bash -n` 검증

2. **QA Evaluator 실행:**
   - **APPROVE** → PR 생성
   - **REJECT** → 해당 Phase로 돌아가 수정 후 Final 재실행

### 글로벌 피드백 정리

1. `bash harness/scripts/feedback-path.sh`로 경로 확인
2. 6개월 초과 파일 삭제 (oldest-first)
3. 500개 초과 시 oldest-first로 삭감
4. 정리 로그를 `.meta/cleanup-log.yaml`에 기록

### Step 8: PR 생성

1. **버전 업데이트:**
   - harness 변경 있으면: `harness/.claude-plugin/plugin.json` 버전 bump
   - flutter-toolkit 변경 있으면: `flutter-toolkit/.claude-plugin/plugin.json` 버전 bump
   - design-kit 변경 있으면: `design-kit/.claude-plugin/plugin.json` 버전 bump
   - `.claude-plugin/marketplace.json` 갱신
   - `docs/kaizen/changelog.md`, `docs/kaizen/flutter-changelog.md` 엔트리 추가

2. **research-log 업데이트:**
   - `docs/kaizen/research-log.md` (harness 관련)
   - `docs/kaizen/flutter-research-log.md` (flutter 관련)

3. **PR 생성:**
   - 브랜치명: `kaizen/{날짜}`
   - PR 제목: `[kaizen] {Phase별 핵심 변경 요약}`
   - PR 본문: Phase별 변경 내역 + Final QA 결과

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

- `/contract-kaizen`, `/evaluator-kaizen`, `/harness-kaizen`, `/flutter-kaizen`, `/design-kaizen`은 **독립 실행 가능** — 긴급 수정이나 특정 영역만 업데이트할 때
- 독립 실행 시에는 오케스트레이터 순서를 따르지 않음 (자체 프로세스 실행)
- 정기 cron은 **오케스트레이터만 실행** — 개별 카이젠 cron은 비활성화
