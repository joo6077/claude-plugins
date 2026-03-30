---
name: kaizen-orchestrator
description: >
  카이젠 전체 실행을 의존성 순서에 맞춰 오케스트레이션한다.
  설계 가이드 → harness → flutter-toolkit 순서로 Phase별 실행하며,
  각 Phase마다 Sprint Contract + QA Evaluator를 자체 실행한다.
  주 1회 cron 자동 실행, 또는 수동 호출("/kaizen", "카이젠 전체 실행").
  개별 플러그인만 카이젠하려면 /harness-kaizen 또는 /flutter-kaizen을 직접 사용.
argument-hint: "[phase1|phase2|phase3|final]"
user-invocable: true
---

# Kaizen Orchestrator

설계 가이드 → harness → flutter-toolkit 순서로 카이젠을 실행한다.
각 Phase마다 Sprint Contract로 완료 조건을 정의하고 QA Evaluator로 검증한다.
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
- 리서치(COLLECT→VERIFY)는 Phase 1에서 한 번만 수행하고 결과를 전 Phase에서 공유한다 — Phase마다 반복 검색하면 토큰 낭비
- Phase 1에서 가이드를 변경했으면 Phase 2/3에서 **모든** 기존 스킬/에이전트를 전수 체크해라 — 눈에 띄는 것만 수정하면 나머지가 누락된다. 테이블로 기록하여 누락을 방지

## 의존성 체인

```
Phase 1: 설계 가이드 (docs/guides/skill-design-guide.md, docs/guides/agent-design-guide.md)
    ↓ 설계 원칙이 하위 모든 스킬/에이전트의 기준
Phase 2: harness (project.yaml, procedures, skills, agents)
    ↓ QA 프레임워크가 flutter-toolkit eval/audit의 기반
Phase 3: flutter-toolkit (project-detection → 개별 스킬 → 신규 스킬)
    ↓ detection이 먼저, 그 위에 개별 스킬
Final: 전체 크로스 Phase 정합성 검증
```

## 트리거 조건

### 주기적 (cron)
- 매주 월요일 09:00 KST
- Claude Code schedule (remote trigger) 사용
- 개별 카이젠(harness-kaizen, flutter-kaizen)의 cron은 비활성화하고 이 오케스트레이터만 실행

### 수동
- `/kaizen-orchestrator` — 전체 (Phase 1→2→3→Final)
- `/kaizen-orchestrator phase1` — 설계 가이드만
- `/kaizen-orchestrator phase2` — harness만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase3` — flutter-toolkit만 (Phase 1 완료 전제)
- `/kaizen-orchestrator final` — Final QA만 (Phase 1~3 완료 전제)

## Process

### Step 0: 리서치 (전 Phase 공유)

모든 Phase에서 사용할 리서치를 한 번에 수행한다.

1. **3개 소스 목록 읽기:**
   - `references/search-sources.md` — Phase 1용 (스킬/에이전트 설계 패턴, Anthropic 공식, 경쟁 도구)
   - `harness/skills/harness-kaizen/references/search-sources.md` — Phase 2용 (QA, 프롬프트 엔지니어링)
   - `flutter-toolkit/skills/flutter-kaizen/references/search-sources.md` — Phase 3용 (Flutter/Dart 생태계)
2. 3개 소스를 합쳐 중복 제거 후 검색 실행:
   - **WebSearch**: 학술 논문, Anthropic 공식 문서, 커뮤니티 소스, 경쟁 도구 패턴
   - **WebFetch**: skills.sh, Flutter/Dart 공식 changelog, Claude Code changelog
3. 3중 검증 게이트 (GATE 1→2→3) 실행
4. 검증된 소스를 Phase별로 분류:
   - 스킬/에이전트 설계 원칙, 프롬프트 패턴 → **Phase 1** (설계 가이드)
   - QA/계약/평가, harness 구조 → **Phase 2** (harness)
   - Flutter/Dart 생태계, 위젯 패턴 → **Phase 3** (flutter-toolkit)
   - 복수 Phase 해당 → 가장 상위 Phase에 우선 배정

### Step 1: Phase 1 — 설계 가이드

**범위:** `docs/guides/skill-design-guide.md`, `docs/guides/agent-design-guide.md`

1. **ANALYZE:**
   - Step 0 리서치 중 Phase 1 배정 인사이트와 현재 가이드를 비교
   - 새 설계 원칙, 아키타입, Gotchas 패턴 도출
   - 개선 포인트가 없으면 "Phase 1: 변경 없음" 기록 후 Phase 2로

2. **Sprint Contract 생성:**
   - `.harness/sprint-contract.md`에 Phase 1 범위 계약 저장
   - 카테고리: Guide (GD-XX)
   - 복잡도: 변경 파일 수 기준 판단
   - 사용자 확인 없이 자동 생성 (카이젠 자체 실행이므로)

3. **APPLY:**
   - 가이드 파일 수정
   - 커밋: `kaizen-phase1: {변경 설명}`

4. **QA Evaluator 실행:**
   - `qa-evaluator` 에이전트로 Phase 1 Sprint Contract 기준 평가
   - **APPROVE** → Phase 2로 진행
   - **REJECT** → 피드백 반영하여 수정 후 재QA (최대 3회, 초과 시 Phase 1 중단하고 사용자 알림)

### Step 2: Phase 2 — harness

**범위:** `harness/skills/*/SKILL.md`, `harness/agents/qa-evaluator.md`, `.harness/project.yaml`, `harness/evals/`

1. **ANALYZE — 리서치 기반:**
   - Step 0 리서치 중 Phase 2 배정 인사이트와 현재 harness 상태를 비교

2. **ANALYZE — Phase 1 정합성 전수 체크 (필수):**
   Phase 1에서 설계 가이드가 변경되었으면, harness의 **모든** 스킬과 에이전트를 전수 검사한다.

   a. Phase 1 변경사항을 목록으로 정리 (예: "패턴 6 추가", "Model Routing 추가")
   b. harness 전 스킬 목록 나열: `harness/skills/*/SKILL.md`
   c. harness 전 에이전트 목록 나열: `harness/agents/*.md`
   d. 각 스킬/에이전트에 대해:
      - 해당 가이드 변경이 이 스킬/에이전트에 적용되는가?
      - 적용 대상 → 개선 포인트로 등록
      - 비적용 → "확인됨 — 변경 불필요" 기록 (근거 1줄)
   e. **전수 체크 결과를 테이블로 기록:**

   ```markdown
   | 스킬/에이전트 | Phase 1 변경 | 적용 여부 | 근거 |
   |--------------|-------------|----------|------|
   | init | 패턴 6 | 불필요 | 초기화 스킬, 에이전트 패턴 무관 |
   | create-agent | 패턴 6 | **적용** | description에 5가지→6가지 반영 필요 |
   | ... | ... | ... | ... |
   ```

   - 개선 포인트 없으면 "Phase 2: 변경 없음" 기록 후 Phase 3로

3. **Sprint Contract 생성:**
   - Phase 2 범위 계약 저장
   - 기존 Phase 1 계약은 `.harness/history/`로 이동
   - 카테고리: `project.yaml`의 `contract_categories` 사용

4. **APPLY:**
   - harness 파일 수정
   - 커밋: `kaizen-phase2: {변경 설명}`

5. **QA Evaluator 실행:**
   - **APPROVE** → Phase 3로
   - **REJECT** → 피드백 반영하여 수정 후 재QA (최대 3회, 초과 시 Phase 2 중단하고 사용자 알림)

### Step 3: Phase 3 — flutter-toolkit

**범위:** `flutter-toolkit/skills/*/SKILL.md`, `flutter-toolkit/references/`, `flutter-toolkit/evals/`

**내부 순서 (필수):**
1. `project-detection.md` 먼저
2. 개별 스킬 (detection 변경에 영향받는 스킬 우선)
3. 신규 스킬 생성

**실행:**

1. **ANALYZE — 리서치 기반:**
   - Step 0 리서치 중 Phase 3 배정 인사이트와 현재 flutter-toolkit 비교

2. **ANALYZE — Phase 1 정합성 전수 체크 (필수):**
   Phase 1에서 설계 가이드가 변경되었으면, flutter-toolkit의 **모든** 스킬과 에이전트를 전수 검사한다.

   a. Phase 1 변경사항 목록 정리
   b. flutter-toolkit 전 스킬 목록 나열: `flutter-toolkit/skills/*/SKILL.md`
   c. flutter-toolkit 에이전트 목록 나열 (있으면)
   d. 각 스킬/에이전트에 대해:
      - 해당 가이드 변경이 적용되는가?
      - 적용 대상 → 개선 포인트로 등록
      - 비적용 → "확인됨 — 변경 불필요" 기록 (근거 1줄)
   e. 전수 체크 결과를 테이블로 기록

3. **ANALYZE — 신규 스킬 갭 분석:**
   - 신규 스킬 갭 분석 포함 (flutter-kaizen SKILL.md 참조)
   - 개선 포인트 없으면 "Phase 3: 변경 없음" 기록 후 Final로

4. **Sprint Contract 생성:**
   - Phase 3 범위 계약 저장
   - 기존 Phase 2 계약은 `.harness/history/`로 이동

5. **APPLY:**
   - project-detection.md 수정 → 커밋
   - 개별 스킬 수정 → 각각 커밋
   - 신규 스킬 초안 생성 → 커밋
   - 커밋: `kaizen-phase3: {변경 설명}`

6. **QA Evaluator 실행:**
   - **APPROVE** → Final로
   - **REJECT** → 피드백 반영하여 수정 후 재QA (최대 3회, 초과 시 Phase 3 중단하고 사용자 알림)

### Step 4: Final — 전체 정합성 검증

**범위:** Phase 1~3 전체 변경사항

1. **Final Sprint Contract 생성:**
   - 크로스 Phase 정합성 조건:
     - Phase 1에서 업데이트된 설계 원칙이 Phase 2~3 변경에 반영되었는가
     - Phase 2 harness 변경이 Phase 3 flutter-toolkit과 충돌하지 않는가
     - 버전 번호가 각 플러그인에서 올바르게 업데이트되었는가
     - changelog, research-log이 모든 Phase 변경을 포함하는가
   - Diagnostics: 전체 `bash -n` 검증

2. **QA Evaluator 실행:**
   - **APPROVE** → PR 생성
   - **REJECT** → 해당 Phase로 돌아가 수정 후 Final 재실행

### Step 5: PR 생성

1. **버전 업데이트:**
   - harness 변경 있으면: `harness/.claude-plugin/plugin.json` 버전 bump
   - flutter-toolkit 변경 있으면: `flutter-toolkit/.claude-plugin/plugin.json` 버전 bump
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

- `/harness-kaizen`, `/flutter-kaizen`은 **독립 실행 가능** — 긴급 수정이나 특정 영역만 업데이트할 때
- 독립 실행 시에는 오케스트레이터 순서를 따르지 않음 (자체 프로세스 실행)
- 정기 cron은 **오케스트레이터만 실행** — 개별 카이젠 cron은 비활성화
