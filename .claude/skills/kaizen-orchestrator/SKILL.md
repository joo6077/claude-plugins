---
name: kaizen-orchestrator
description: >
  카이젠 전체 실행을 의존성 순서에 맞춰 오케스트레이션한다.
  설계 가이드 → contract → evaluator → harness → flutter-toolkit → design-kit → backend-kit → infra-kit → rust-kit → react-kit → planning-kit 순서로
  Phase별 실행하며, 각 Phase마다 자체 리서치 + Sprint Contract + QA Evaluator를 실행한다.
  주 1회 cron 자동 실행, 또는 수동 호출("/kaizen", "카이젠 전체 실행").
  개별 플러그인만 카이젠하려면 해당 카이젠 스킬을 직접 사용.
argument-hint: "[phase1|phase2|phase3|phase4|phase5|phase6|phase7|phase8|phase9|phase10|phase11|final]"
user-invocable: true
---

# Kaizen Orchestrator

설계 가이드 → contract → evaluator → harness → flutter-toolkit → design-kit → backend-kit → infra-kit → rust-kit → react-kit → planning-kit 순서로 카이젠을 실행한다.
각 Phase마다 자체 리서치 + Sprint Contract + QA Evaluator를 실행한다.
전체 Phase 완료 후 크로스 Phase 정합성을 최종 검증한다.

## 이 스킬 폴더의 파일

필요할 때 읽어라:

- `references/phase-dependencies.md` — Phase 간 의존성 맵 + 업데이트 순서 규칙
- `references/search-sources.md` — Phase 1 전용 리서치 소스 (스킬/에이전트 설계 패턴)
- `references/phase-research-templates.md` — **Phase 1~14 각 의무 리서치 소스 테이블**. 각 Phase 서브에이전트는 이 템플릿에 명시된 최소 3 건 이상을 조회해야 한다. (Phase 11 planning-kit 추가 2026-04-14, Phase 12 reflect-kit / Phase 13 bambu-kit 섹션 신설 + Phase 14 onboarding 번호 정정 2026-07-27)

## 연동 스크립트

- `scripts/sync-orchestrator.py` — marketplace.json → AUTO:plugin_phases 마커 영역 자동 동기화
- `scripts/spawn-kaizen-phase.sh <N>` — Phase N 부트스트랩 (git tag + data-pool §N + subagent 프롬프트)
- `scripts/finalize-phase.sh <N> <pass|fail> [--revert]` — Phase 종료 처리 (failure-count 갱신 + auto-revert 제안)
- `scripts/validate-post-kaizen.py` — Step F4 Post-Kaizen Checklist 자동 검증. PR 생성 전 필수 실행 (검사 항목 수는 스크립트가 요약 줄에 출력한다 — 여기에 숫자를 박아두면 항목이 늘 때 조용히 틀린다)
- `scripts/append-audit-log.py` — Step 11 Final 종료 시 이번 사이클 meta-issue 를 `.harness/.meta/orchestrator-audit-log.md` 에 append
- `scripts/detect-docs-drift.py` — Step F2 에서 재생성 필요한 HTML 경로 manifest 생성
- `scripts/fix-markdown-lint.py` — MD031/MD032/MD034/MD060 auto-fix. **디렉토리 인자(`docs/`)로 실행 금지** — 이번 사이클에서 변경하지 않은 100여 파일까지 일괄 수정하여 PR scope 를 오염시킨다. 반드시 **이번 사이클에 변경한 파일만** 개별 경로로 전달하라 (스크립트는 단일 path 인자만 받으므로 파일별 호출)
- `scripts/sync-evals.py` — 각 플러그인 skills/ 와 evals/evals.json 동기화

## 관련 스킬

- `/meta-kaizen` — 이 오케스트레이터 SKILL.md 자체를 리서치 기반으로 개선하는 메타 카이젠. Phase 1~14 범위 밖. 주 1 회 이하 권장.

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
- **Step F2 (docs-site 재생성) 과 Step F3 (글로벌 피드백 정리) 는 건너뛰기 금지.** 이 두 단계는 "조건부 실행" 이 아니라 **필수 실행** 이다. docs-site 가 빠지면 공개 HTML 문서가 카이젠 이전 상태에 멈추고, 피드백 정리가 빠지면 다음 사이클 data pool 품질이 저하된다.
- **Step F4 의 Post-Kaizen Checklist 는 PR 생성 전 blocking gate** 다. 하나라도 미통과면 PR 생성을 중단하고 해당 Step 으로 돌아간다. 체크리스트를 "대부분 OK" 로 넘기지 마라.
- **per-kit research-log 는 파일이 없어도 신규 생성하라.** 이전 조문 "존재 시 갱신" 은 영구 누락을 유발했다. `docs/{backend,infra,rust,react,flutter}/research-log.md` 가 없으면 반드시 만든다.
- **`AUTO:plugin_phases` 마커 영역(Process 절의 Phase 5~N)을 직접 편집하지 마라.** 이 영역은 `scripts/sync-orchestrator.py` 가 `marketplace.json` 을 기반으로 자동 생성한다. 킷 추가/수정/삭제 시 marketplace.json 을 고친 뒤 `python3 scripts/sync-orchestrator.py` 를 실행하면 이 섹션이 동기화된다. 직접 편집 시 다음 실행에서 덮어써진다. **마커를 산문에서 설명할 때 HTML 주석 형태를 그대로 적지 마라** — 실측 2026-08-13: 이 불릿이 마커를 리터럴로 품고 있었고 `sync-orchestrator.py` 가 `str.find()` 로 그 첫 등장을 잡아 자동 생성 블록 92 행을 **이 불릿 안으로** 주입했다. 진짜 Process 위치는 갱신되지 않아 Phase 12·13 의 `### Step` 절이 통째로 빠졌는데도 `--check-only` 는 exit 0 을 보고했다. 지금은 스크립트가 행 앵커 + 마커 유일성 검사로 막는다 (1 쌍이 아니면 exit 2).

- **Step 0.5 Orchestrator Self-Audit 는 건너뛰기 금지.** 이전 사이클의 수동 개입 이력 (`.harness/.meta/orchestrator-audit-log.md`) 과 `sync-orchestrator.py --check-only` drift 를 먼저 확인해야 Phase 1 로 진입한다.

## Phase 의존성

```text
Step 0:   Pre-flight — 피드백 데이터 풀 수집 (scripts/collect-kaizen-data.py)
    ↓
Step 0.5: Orchestrator Self-Audit — 이전 사이클 meta-feedback 반영 + sync-orchestrator drift 확인
    ↓
Step 0.6: Phase Relevance Triage — §0 중복도 + 신호 농도로 선별 범위 제안 (전체는 사용자 선택)
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
Phase 11: Planning-kit 카이젠 (planning-kaizen)
    ↓
Phase 12: Reflect-kit 카이젠 (reflect-kaizen)
    ↓
Phase 13: Bambu-kit 카이젠 (bambu-kaizen)
    ↓
Phase 14: Onboarding-kit 카이젠 (onboarding-kaizen)
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
11. Planning-kit 카이젠 — 제품 기획 스킬 개선 (docs/planning/ 리서치 기준, Discovery/PRD/Prioritization/Risks/Stories/Flows/Data Model/GitHub Sync)
12. Reflect-kit 카이젠 — 개인 Claude Code 피드백 → 학습 → 재주입 파이프라인 개선 (Reflexion 방법론)
13. Bambu-kit 카이젠 — Bambu Studio 프로파일 생성 스킬 개선 (references SSOT 7종 + 실측 dogfood 기준). references 대량 갱신은 `/bambu-research` 소관
14. Onboarding-kit 카이젠 — 외부 서비스 셋업 가이드 스킬 개선 (docs/help 변경 + 사용자 피드백 + marketplace 트렌드)

## 트리거 조건

### 주기적 (cron)

- 매주 월요일 09:00 KST (= UTC 00:00)
- Claude Code `schedule` 스킬로 remote trigger 등록
- 개별 카이젠(contract-kaizen, evaluator-kaizen, harness-kaizen, flutter-kaizen, design-kaizen, backend-kaizen, infra-kaizen, rust-kaizen, react-kaizen, planning-kaizen, reflect-kaizen)의 cron은 비활성화하고 이 오케스트레이터만 실행

**등록 명령 (최초 1 회):**

```text
/schedule create --cron "0 0 * * 1" --command "/kaizen-orchestrator research-mode" --description "주간 카이젠 research-mode 자동 실행"
```

**상태 확인:**

```text
/schedule list
```

**해제 (임시 비활성화):**

```text
/schedule delete <id>
```

### 수동

- `/kaizen-orchestrator` — 전체 (Phase 1→2→3→4→5→6→7→8→9→10→11→Final)
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
- `/kaizen-orchestrator phase11` — planning-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase12` — reflect-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase13` — bambu-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator phase14` — onboarding-kaizen만 (Phase 1 완료 전제)
- `/kaizen-orchestrator final` — Final QA만 (Phase 1~14 완료 전제)

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

모든 Phase 1~14 서브에이전트가 공유할 **통합 데이터 풀**을 먼저 생성한다. 이는 각 Phase 가 단절된 리서치에 매몰되지 않고 글로벌 피드백·외부 프로젝트·followup 이슈·개인 메모리(`~/.claude/projects/*/memory/`)·`/insights` 30 일 분석을 근거로 개선하도록 보장한다.

데이터 풀의 섹션 구성은 **§0 · §0.5 · §1 · §2 · §3 · §4 · §5 · §6** 이다. **§0.5 (개인 메모리) 는 §0 과 §1 _사이_ 에 렌더된다** — 순서가 어긋나 있으면 산문을 고치지 말고 수집 로직(`scripts/collect-kaizen-data.py`)의 결함으로 다뤄라.

**실행:**

```bash
python3 scripts/collect-kaizen-data.py
```

**출력:** `.harness/.meta/kaizen-data-pool.md`

**스크립트 인터페이스 (기계 검증 대상):**

아래 블록은 산문이 아니라 **선언**이다. `scripts/validate-doc-contracts.py` 가 이 값을
`scripts/collect-kaizen-data.py` 의 argparse·모듈 상수와 대조하며, 실체가 SSOT 다.
스크립트 인터페이스를 바꾸면 이 블록도 같이 고쳐야 post-kaizen 게이트를 통과한다.
**여기 없는 옵션이나 입력 경로를 산문으로 주장하지 마라** — 2026-08-13 에 자유 서술로 주장한
`--insights=PATH` 와 repo 자동 탐색이 실제로는 미구현이었고, 그동안 사람이 정리한 §0 델타
분석본이 데이터 풀에 들어가지 못했다.

```yaml
# docs-contract
script: scripts/collect-kaizen-data.py
options: ["--hub-dir", "--insights", "--output", "--skip-validate"]
input_candidates:
  - .claude/kaizen-input/insights-report.md
  - ~/.claude/kaizen-input/insights-report.md
  - ~/.claude/usage-data/report.html
exit_codes: [0, 2]
```

**수집 소스 (스크립트 내장):**

0. **`/insights` 외부 도구 산출물** — 위 `input_candidates` 를 **우선순위대로** 탐색. `--insights PATH` 로 명시 지정하면 자동 탐색보다 우선한다

   - `/insights` 는 Claude Code 마켓플레이스 등록 스킬이 아니라 사용자가 외부 도구로 30일 세션 사용 데이터를 분석한 산출물 (Friction Points / Recommended Patterns / Feature Suggestions)
   - `.md` 후보는 본문 그대로, `.html` 후보는 태그를 벗겨 데이터 풀 §0 (최상위) 으로 삽입되어 **모든 Phase 가 최우선 참조**
   - 선택 결과는 stderr 에 후보별로 찍힌다 (`✓ 선택` / `· 후순위` / `✗ 없음`) — 무엇을 읽었는지 확인하고 넘어가라
   - 60일 초과 시 STALE 경고 표시. STALE 이면 사용자에게 `/insights` 재실행 권고
   - 후보가 하나도 없으면 §0 에 "(없음)" 안내 후 진행 — Step 0 자체는 막지 않는다
   - `--insights` 로 지정한 파일이 없으면 **다른 후보로 조용히 대체하지 않고 exit 2** 로 멈춘다

**0.5. 개인 메모리 (전 프로젝트 교차)** — `~/.claude/projects/*/memory/` · 데이터 풀 §0.5 로 렌더

- `metadata.type: feedback` 엔트리만 수집한다. 범위는 이 레포가 아니라 **전 프로젝트 교차**다 — 다른 프로젝트에서 얻은 교훈이 이 레포의 Phase 에도 그대로 걸린다.
- 각 엔트리는 frontmatter 에 `grounding` 필드를 갖는다. **정의와 판정 절차의 SSOT 는 `reflect-kit/references/memory-grounding.md`** 다 — 이 문서에서 값을 나열하거나 재정의하지 마라.
- 선별은 **관련성 · 중요도 2 축**이다. recency 를 쓰지 마라 — `modified` 필드 보유율이 낮아 상당수가 임의 판정이 된다.
- 선별에서 탈락한 엔트리는 **제목 목록**이 §0.5 말미에 남는다. 그 Phase 에 결정적이라고 판단되면 원문을 직접 읽어라.
- 메모리 디렉토리가 없거나 엔트리가 0 건이어도 Step 0 은 멈추지 않는다 (§0.5 에 `(없음)` 표기).

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

§0 (`/insights`) 가 존재할 때는 **모든 Phase** 가 §0 을 최우선 참조한 뒤 자신의 도메인 섹션을 본다. 각 Phase subagent 프롬프트는 데이터 풀 §0 을 첫 번째 참조로 명시해야 한다.

**§0.5 (개인 메모리) 는 §0 다음, 도메인 섹션 이전에 읽는 전 Phase 공통 참조다.** 아래 표의 "주요 참조 섹션" 열에 §0.5 를 행마다 반복 표기하지 않는 것은 생략이 아니라 **헤더 레벨 1 회 공통 선언**이다 — 조건마다 반복해서 적으면 언젠가 하나를 빠뜨린다.

**§0.5 사용 제한 (전 Phase 공통 전제):** `grounding: self_inference` 로 라벨된 엔트리는 **아무도 확인하지 않은 자기추론**이다. 배경 참고까지만 쓰고 **계약 조건의 PASS 근거로 인용하지 마라** — amendment 의 `consent: unanchored` 를 PASS 근거로 쓸 수 없는 것과 정확히 같은 취급이다. 카이젠이 쓴 것을 카이젠이 다시 근거로 먹으면 자기검증 피드백 루프가 되고, 이는 Final 계약이 자기참조 카브아웃으로 막은 것과 같은 구조다. `grounding` 필드가 아예 없는 엔트리는 `self_inference` 가 아니라 **미태깅**이며, 이 역시 PASS 근거가 될 수 없다.

| Phase | 주요 참조 섹션 |
| ------- | ------------- |
| 1 설계 가이드 | §0 + §1 improvement suggestions |
| 2 Contract | §0 + §1 reject 사유 (계약 모호성 패턴) |
| 3 Evaluator | §0 + §1 improvement (L3 커버리지, set intersection) |
| 4 Harness | §0 + §5 validate-plugin 현재 상태 |
| 5 Flutter | §0 + §2 Hub 외부 프로젝트 (fit-pal, apps) |
| 6 Design | §0 + §5 validate-plugin 현재 상태 |
| 7 Backend | §0 + §1 backend 관련 feedback |
| 8 Infra | §0 + §5 validate-plugin 현재 상태 |
| 9 Rust | §0 + §2 Hub 외부 프로젝트 (fit-pal server) |
| 10 React | §0 + §3 followup-2026-04-11, §5 |
| 11 Planning | §0 + §1 planning 관련 feedback (있을 시), §5 validate-plugin 현재 상태 |
| 12 Reflect | §0 + §1 Reflexion 패턴 피드백 |
| 13 Bambu | §0 + §2 실측 dogfood 결과, bambu-kit references SSOT |
| 14 Onboarding | §0 + §5 validate-plugin 현재 상태 |

**각 Phase 서브에이전트 프롬프트에 데이터 풀 경로 전달 필수:**

```text
데이터 소스:
- `.harness/.meta/kaizen-data-pool.md` — 카이젠 공통 데이터 풀 (Step 0 에서 생성)
  §0 (`/insights`) → §0.5 (개인 메모리) 순으로 먼저 읽고, 그 다음 너의 Phase
  범위에 해당하는 섹션 (§N) 을 본다.
  §0.5 에서 `grounding: self_inference` 인 엔트리 (및 `grounding` 미보유 엔트리) 는
  배경 참고까지만이다 — 계약 조건의 PASS 근거로 인용하지 마라.
  4 값 정의는 `reflect-kit/references/memory-grounding.md` 가 SSOT.
```

**Gotchas:**

- Step 0 을 건너뛰고 Phase 1 부터 시작하지 마라 — 각 Phase 가 같은 데이터를 다시 수집하면 중복 작업이다.
- 데이터 풀은 Phase 진행 중에는 재생성하지 마라 — Phase 별로 상태가 흔들린다. 전체 카이젠 종료 후 다음 사이클에 다시 수집한다.
- 데이터 풀 파일은 스크립트 생성물이므로 직접 수정 금지. 내용이 틀리면 수집 로직(`scripts/collect-kaizen-data.py`)을 고친다.
- 글로벌 feedback 이 0건이어도 Step 0 은 실행한다 — 외부 프로젝트 피드백이나 followup 은 여전히 유효할 수 있다.
- `/insights` 리포트 파일이 없어도 Step 0 은 진행한다 (§0 에 "(없음)" 으로 표시). 사용자가 외부 `/insights` 도구를 실행하지 않은 상태일 수 있다.
- `/insights` 리포트가 60일 초과 STALE 이면 데이터 풀에 ⚠ 마커가 붙는다. 이 사이클은 진행하되, **사용자에게 `/insights` 재실행을 권고**하라.
- `/insights` 가 30일 세션 분석이지만 카이젠 사이클(주 1 회)이 더 빈번하므로, 이전 사이클과 같은 리포트가 재참조될 수 있다. 매 사이클 §0 의 friction point 가 이미 해결되었는지 각 Phase QA Acceptance Criteria 에 명시한다.
- `--insights=PATH` 인자가 명시적으로 전달되면 자동 탐색 경로보다 우선한다 (사용자가 특정 리포트 버전을 강제하고 싶을 때).
- **§0.5 개인 메모리를 "카이젠이 쓴 것" 이라는 이유로 통째로 배제하지 마라.** 메모리의 `feedback` 엔트리는 전부 Claude 가 쓴 것이라 저자로 가르면 아무것도 끊기지 않는다. 가르는 축은 저자가 아니라 **근거**(`grounding`)다 — 외부 신호(사용자 교정 · 실행 증거)가 붙은 엔트리는 카이젠 산출이라도 유효하다. 취급을 달리할 대상은 `self_inference` 와 미태깅뿐이고, 그것도 삭제가 아니라 **PASS 근거 금지 라벨**이다.
- **메모리는 카이젠의 입력이자 출력이다 — 같은 사이클 안에서 왕복시키지 마라.** 이번 사이클이 Step F3.5 로 낸 승격 후보는 이번 사이클 §0.5 의 근거가 될 수 없다. 후보는 `/reflect-promote` 승인을 거쳐 메모리가 된 뒤에야 **다음** 사이클 §0.5 로 들어온다.

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

### Step 0.6: Phase Relevance Triage — 선별 (자동 — 건너뛰기 금지)

**목적:** 전체 Phase 를 기본값으로 spawn 하면, 신호가 없는 Phase 도 서브에이전트 비용(리서치+분석, Phase 당 ~70k~140k 토큰)을 먼저 지불한 뒤에야 NO_CHANGE/1줄 Gotcha 를 발견한다. `/insights` 리포트는 롤링 윈도우라 직전 사이클과 크게 겹치는 경우가 많아, 이 낭비가 반복된다. Step 0.6 은 phase 를 spawn **하기 전에** 신호 농도를 평가하여 **선별 실행 범위를 사용자에게 제안**한다.

**절차:**

1. **§0 중복도 평가** — 데이터 풀 §0 `/insights` 리포트의 friction/suggestion 항목이 직전 사이클 audit-log(Step 0.5) 또는 직전 changelog 에서 이미 흡수됐는지 대조. 겹침이 높으면 §0 의 한계효용은 낮다 (각 Phase 프롬프트에 "직전 사이클 흡수분 중복 금지" 를 전달하는 것과 별개로, 애초에 spawn 할 Phase 를 줄인다).
2. **Phase 별 신호 농도 산출** — 각 Phase 에 대해 (a) §1 글로벌 feedback 에 해당 kit 의 REJECT/improvement 신호가 있는가 (b) §2 외부 프로젝트에 해당 스택 사용 흔적이 있는가 (c) 직전 사이클 이후 해당 kit 소스가 변경됐는가 (d) §0 friction 이 해당 도메인에 직접 매핑되는가 — 4 신호 중 **0 개면 low-signal**.
3. **선별 범위 제안** — low-signal Phase 가 다수면, 사용자에게 "고신호 Phase N 개만 실행 vs 전체" 를 **명시적 근거(어느 Phase 가 왜 low-signal 인지 표)와 함께 제안**한다. 사용자가 전체를 택하면 전체 실행한다 — 선별은 강제가 아니라 비용 인지 후 선택이다.
4. 설계 가이드 Phase(1~3)는 **신호와 무관하게 항상 후보에 포함** — 하위 kit Phase 의 정합성 기준이기 때문. 단 변경 없으면 자체적으로 NO_CHANGE.
5. 선별 결정(전체/부분 + 근거)을 audit-log 의 이번 사이클 엔트리에 기록한다.

**Gotchas:**

- 이 단계는 기존 "Phase 스킵 규칙"(reactive: spawn 후 0 개면 skip)의 **proactive 버전**이다 — spawn 비용 자체를 아낀다. 둘은 보완 관계이지 대체가 아니다.
- low-signal 이라고 **자동으로** 빼지 마라 — 반드시 사용자에게 근거와 함께 제안하고 동의를 받는다. 사용자가 "전체" 를 이미 지시했으면 그 지시를 존중한다(재질문 금지, 단 비용은 1 회 고지).
- 선별로 제외한 Phase 는 changelog/research-log 에 "이번 사이클 미실행(low-signal, 선별 제외)" 으로 1 줄 기록하여 누락과 구분한다.
- §0 리포트가 VERY FRESH(24h)여도 내용이 직전 사이클과 겹치면 "신선함 ≠ 새 신호" 다. 타임스탬프가 아니라 **내용 델타**로 판단하라.

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

**범위:** `flutter-toolkit/skills/*/SKILL.md`, `flutter-toolkit/references/`
, `docs/flutter/` 리서치 문서

공통 실행 패턴에 따라 `/flutter-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 flutter-toolkit 전 스킬을 전수 감사한다. flutter-toolkit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.7.0 · 2026-08-13] Flutter 개발 워크플로우 스킬 모음 (Freezed·Flutter·Impeller 사실 정정 3종 + Primitive Substitution Gate + invalidate 경계)

### Step 6: Phase 6 — design-kit 카이젠

**범위:** `design-kit/skills/*/SKILL.md`, `design-kit/references/`
, `design-kit/docs/design/` 리서치 문서

공통 실행 패턴에 따라 `/design-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 design-kit 전 스킬을 전수 감사한다. design-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.4.0 · 2026-08-13] 스택 무관 UI/UX 디자인 가이드 + 감사 (Variant Distinctiveness Gate + Decision Propagation Manifest + 증거 채널 + WCAG 24×24 정정)

### Step 7: Phase 7 — backend-kit 카이젠

**범위:** `backend-kit/skills/*/SKILL.md`, `backend-kit/references/`
, `docs/backend/` 리서치 문서

공통 실행 패턴에 따라 `/backend-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 backend-kit 전 스킬을 전수 감사한다. backend-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.3.0 · 2026-08-13] 스택 무관 백엔드 개발 가이드 + 감사 + 아키텍처 세팅 (쓰기 경로 무결성 SSOT (경합 invariant 3유형 · upsert arbiter · 통합 테스트 대상 증명))

### Step 8: Phase 8 — infra-kit 카이젠

**범위:** `infra-kit/skills/*/SKILL.md`, `infra-kit/references/`
, `docs/infra/` 리서치 문서

공통 실행 패턴에 따라 `/infra-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 infra-kit 전 스킬을 전수 감사한다. infra-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.3.0 · 2026-08-13] 스택 무관 인프라/DevOps 가이드 + 감사 + 초기 세팅 (게이트 결과 상태 taxonomy 5종 + YAML 파서 액션 핀닝 + USE×RED 환경 선배제)

### Step 9: Phase 9 — rust-kit 카이젠

**범위:** `rust-kit/skills/*/SKILL.md`, `rust-kit/references/`
, `docs/rust/` 리서치 문서

공통 실행 패턴에 따라 `/rust-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 rust-kit 전 스킬을 전수 감사한다. rust-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.3.0 · 2026-08-13] Rust 전용 백엔드 개발 워크플로우 — Rust 2024 / Axum 0.8 / SeaORM 1.1 / Clippy 2026 (sqlx::test 격리 단위 정정 + clippy unwrap 게이트 E3 + 동시성 가드 판별력 SSOT)

### Step 10: Phase 10 — react-kit 카이젠

**범위:** `react-kit/skills/*/SKILL.md`, `react-kit/references/`
, `docs/react/` 리서치 문서

공통 실행 패턴에 따라 `/react-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 react-kit 전 스킬을 전수 감사한다. react-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.3.0 · 2026-08-13] React + Vite + Tauri 2 + Rust WASM 개발 워크플로우 — React 19 / TanStack Query v5 / Tauri 2 GA / Tailwind v4 / Zustand v5, 라이브러리 0개 애니메이션 (템플릿 의존성 현행화 + 표준 커버리지 공백 문서화 (라이브러리 0개 원칙 유지))

### Step 11: Phase 11 — planning-kit 카이젠

**범위:** `planning-kit/skills/*/SKILL.md`, `planning-kit/references/`

공통 실행 패턴에 따라 `/planning-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 planning-kit 전 스킬을 전수 감사한다. planning-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.5.0 · 2026-08-13] 스택 무관 제품 기획 플러그인 — 레퍼런스 teardown · Lightning Demo · VPC · Blue Ocean · HMW · Crazy 8s · JTBD · PR-FAQ · Shape Up · RICE·Kano·WSJF · DDD Event Storming · GitHub Projects v2 (Projects v2 REST 지원 정정 + one-When 과잉 인용 라벨링 + HBR 절차 미확인 강등)

### Step 12: Phase 12 — reflect-kit 카이젠

**범위:** `reflect-kit/skills/*/SKILL.md`, `reflect-kit/references/`

공통 실행 패턴에 따라 `/reflect-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 reflect-kit 전 스킬을 전수 감사한다. reflect-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.6.0 · 2026-08-13] 개인 Claude Code 대화 피드백 → 학습 → 재주입 파이프라인 (Reflexion 방법론) — Hybrid project_id (basename 기본 + 충돌 시 hash fallback · backward-compatible) · 정규화 쿼리 · 내부 디렉토리 자동 제외 · 3 훅 수집 · /reflect-digest 집계 (+ project=all cross-project) · /reflect-promote 승격 + ledger · /reflect-kaizen 30d calibration · codex 실패 시 Claude CLI fallback · install-scheduler/legacy-id-migrate 유틸 (태그 정규화 결정론화 + hook coverage audit 라우팅 + 파편화 게이트 calibration 무효화)

### Step 13: Phase 13 — bambu-kit 카이젠

**범위:** `bambu-kit/skills/*/SKILL.md`, `bambu-kit/references/`

공통 실행 패턴에 따라 `/bambu-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 bambu-kit 전 스킬을 전수 감사한다. bambu-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.6.0 · 2026-08-13] Bambu Lab H2S 자동 process+filament JSON 생성 — MakerWorld URL 전체 크롤링(다국어/페이지네이션) → Phase 1.6 댓글 분석(designer_reply/user_success/user_failure/user_variant) → Override Rule 범위 좁힘 → Phase 1.6.5 4-옵션([A]속도/[B]top만/[C]디자이너∧surface-first 병행 default/[D]풀) → Phase 1.7 Tolerance & Fit Analysis (베어링/볼트/heat-set insert/슬라이드 fit + 공차 보정 키 elefant_foot/xy_hole/xy_contour + 소재별 수축률) → 소재 추천 → seam 전략 → fit calibration coupon → Bambu Studio import 번들 (실측 실패 3종 인테이크 + 지원가능성 분기 + E3 금지 키 확장)

### Step 14: Phase 14 — onboarding-kit 카이젠

**범위:** `onboarding-kit/skills/*/SKILL.md`, `onboarding-kit/references/`

공통 실행 패턴에 따라 `/onboarding-kaizen` 서브에이전트로 실행. Phase 1 에서 설계 가이드가 변경되었으면 onboarding-kit 전 스킬을 전수 감사한다. onboarding-kit 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다.

> 플러그인 설명: [v0.3.0 · 2026-08-13] 스택 무관 외부 서비스 셋업 가이드 자동 생성 — 그 시점 최신 정보(WebFetch → Context7 → Codex) 기준 step-by-step MD (배포 가이드 사실 정정 4종 + Guide Conformance Gate)

<!-- /sync-orchestrator.py 자동 생성 끝. 다음 사이클 전에 marketplace.json 을 수정했으면 다시 실행하세요. -->
<!-- AUTO:plugin_phases:end -->

### Phase 별 추가 지시 (자동 생성 영역 밖)

위 AUTO 영역은 `marketplace.json` 에서 기계 생성되므로 킷별 특수 지시를 담지 못한다.
아래는 그 **보완**이며 손으로 관리한다. `### Step` 헤딩을 여기서 다시 만들지 마라 —
Phase 당 `### Step` 헤딩은 AUTO 영역에 **정확히 하나**만 존재한다 (실측 2026-08-13: 수기로
`Step 10.9` · `Step 10.95` 를 덧붙인 결과 Phase 11·14 가 두 번 등장하고 번호 체계가 깨졌다).

- **Phase 10 (react-kit) — 라이브러리 0개 원칙**: `react-animation` 스킬, animation-architect-react
  에이전트, `react-audit` 의 Library Policy 카테고리는 Motion / framer-motion / dnd-kit /
  react-spring / react-transition-group / animate.css 등을 빌드 게이트로 금지한다.
  카이젠에서 **절대 완화하지 말고**, 신규 금지 라이브러리 추가만 허용한다.
- **Phase 11 (planning-kit) — 필수 리서치 소스**: `references/phase-research-templates.md` 의
  Phase 11 테이블 (Teresa Torres OST / Marty Cagan 4-risks / Basecamp Shape Up / Alan Klement JTBD /
  Strategyn ODI / Agile Alliance INVEST / Cucumber Gherkin / HBR Pre-mortem / Mermaid ER /
  GitHub Projects REST / Lean Stack RAT) 최소 3 건 이상 조회. 리서치 문서가 부족하면
  `/planning-research` 를 먼저 호출해 `docs/planning/` 를 갱신한 뒤 진행한다. 개선 대상은
  planning-kit 플러그인의 10 개 스킬 + planning-reviewer 에이전트이며, `/planning-kaizen` 스킬
  자체는 이 레포 개발용이라 플러그인에 포함되지 않는다.
- **Phase 14 (onboarding-kit) — 필수 리서치 소스 · 의존성**:
  `references/phase-research-templates.md` 의 **Phase 14** 테이블 (Firebase iOS/Flutter setup /
  Apple Developer / Stripe / GCP / 패키지 레지스트리) 최소 3 건 이상 조회.
  개선 대상은 `/setup-guide` 1 개 스킬 + `references/` 3 종 + `evals/evals.json` 이다.
  의존성은 Phase 1 (skill-design-guide) 결과뿐이며 다른 Phase 결과에는 영향받지 않는다 (독립 스택).

### Step F1: Final — 전체 정합성 검증 (구 Step 11)

**범위:** Phase 1~14 전체 변경사항 (Phase 11 planning-kit · Phase 12 reflect-kit · Phase 13 bambu-kit · Phase 14 onboarding-kit 포함 전수 체크)

1. **Final Sprint Contract 생성:**

   - 크로스 Phase 정합성 조건:
     - Phase 1에서 업데이트된 설계 원칙이 Phase 2~14 변경에 반영되었는가 (planning-kit 10 스킬 + planning-reviewer 에이전트 + reflect-kit 3 스킬 + 3 훅 + bambu-kit + onboarding-kit 포함)
     - Phase 2 contract 변경이 Phase 3 evaluator와 정합하는가
     - Phase 4 harness 변경이 Phase 5~14 (flutter-toolkit, design-kit, backend-kit, infra-kit, rust-kit, react-kit, planning-kit, reflect-kit, bambu-kit, onboarding-kit)과 충돌하지 않는가
     - 버전 번호가 각 플러그인에서 올바르게 업데이트되었는가 (planning-kit + reflect-kit plugin.json 포함)
     - changelog, research-log이 모든 Phase 변경을 포함하는가 (docs/planning/research-log.md 포함)
   - Diagnostics: 전체 `bash -n` 검증

2. **QA Evaluator 실행:**

   - **APPROVE** → Step F2 로 진행
   - **REJECT** → 해당 Phase로 돌아가 수정 후 Final 재실행

### Step F2: docs-site 재생성 (자동 — 건너뛰기 금지 · 구 Step 11.5)

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
| planning-kit | `planning-kit/references/`, `docs/planning/` | `docs/planning-kit/` |
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

### Step F3: 글로벌 피드백 정리 (자동 — 건너뛰기 금지 · 구 Step 11.6)

Step F2 이후 실행. 다음 카이젠 사이클의 data pool 품질 유지를 위해 오래되거나 누적된 피드백을 정리한다.

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

### Step F3.5: 메모리 승격 후보 산출 (자동 — 건너뛰기 금지)

**목적:** 이번 사이클이 얻은 교훈을 다음 사이클의 §0.5 로 되돌리는 **유일한 경로**다. 이 단계가 없으면 사이클 산출물이 계약 본문과 감사 로그에만 남는다. 실측: `oracle-must-execute-not-grep` 교훈이 2026-07-28 에 기록됐는데, 2 주 반 뒤 kaizen-2026-08-13 사이클의 재평가 REJECT 3 건이 정확히 그 유형(계약 측정문 결함)이었다 — 루프가 메모리를 먹지 않아 계약 작성 단계에 전달되지 않았다.

**경계 — 카이젠은 후보만 낸다. 승격하지 않는다.**

- 승격 ledger (`~/.claude/logs/<project_id>/promotions-ledger.md`) 에 **쓰지 마라.** 이 파일은 `/reflect-promote` 소유다. 카이젠이 병렬 쓰기 경로를 만들면 ledger 가 두 갈래로 갈라져 rollback 이 깨진다.
- 승격 판정 로직(precedence table · `rule_id` 발급 · `status` 전환 · enforcement 등급 상향 · 중복 판정)을 **여기서 재구현하지 마라.** 전부 `reflect-kit/skills/reflect-promote/SKILL.md` 가 정본이다. 카이젠은 그 스킬을 **참조·호출**한다.
- 메모리 파일(`~/.claude/projects/*/memory/`)과 `MEMORY.md` 인덱스도 카이젠이 직접 쓰지 않는다.

**산출물:** `.harness/.meta/memory-promotion-candidates-{YYYY-MM-DD}.md` — 사이클당 1 파일 (기존 사이클 파일에 append 하지 않는다)

**포맷** — 관측과 근거만 담는다. `promoted_to` · `rule_id` · `enforcement_level` · `status` 같은 **판정 결과 필드를 넣지 마라.** 그것을 채우는 순간 승격 로직의 복제가 된다.

```yaml
# kaizen-memory-candidates
cycle_id: kaizen-YYYY-MM-DD
generated_at: <ISO8601+TZ>
candidates:
  - canonical_tag: <kebab-case>
    grounding: <reflect-kit/references/memory-grounding.md 의 4 값 중 하나>
    actionability: claude_behavior | user_environment
    scope: session | project | global
    risk_class: low | medium | high
    procedurality: single_rule | multi_step_procedure
    enforcement_need: soft_reminder | hard_gate
    user_stated_constraint: true | false
    freq: <int>
    undesired_behavior: <str>
    desired_behavior: <str>
    source_evidence:
      - path: <계약 파일 · QA 피드백 · 명령 출력 로그의 경로>
        anchor: <조건 ID · verdict · 헤더>
    draft_rule: "<한 줄 초안>"
```

**절차:**

1. 이번 사이클의 Phase QA verdict (REJECT 사유 · iteration 사유) 와 Final 재평가 지적을 **근본원인 단위**로 묶는다. 표기가 닮았다고 합치지 마라.
2. 각 후보의 `grounding` 을 판정한다 — 기준은 `reflect-kit/references/memory-grounding.md`. **`self_inference` 로 판정되면 후보로 내지 마라.** 카이젠 자신의 추론을 외부 확인 없이 영속 규칙으로 증류하는 경로가 정확히 이것이다. QA verdict · 명령 출력 · 실측 수치를 `source_evidence` 에 댈 수 있는 것만 후보다.
3. `actionability: user_environment` 는 후보에서 제외한다 (Claude 행동 개선 대상이 아니다). 필요한 사용자 조치는 리포트에만 적는다.
4. 후보 파일을 쓰고, 사용자에게 **경로와 건수를 보고한 뒤 `/reflect-promote` 호출을 제안**한다. 승격 여부 · surface · 등급은 그 스킬이 사용자 승인을 거쳐 판정한다.
5. 후보가 0 건이어도 파일은 만든다 (`candidates: []`). 실행 증거가 남아야 다음 사이클이 "후보 없음" 과 "단계 누락" 을 구분할 수 있다.

**Gotchas:**

- 후보 파일을 만든 것을 "승격 완료" 로 보고하지 마라 — 승격은 `/reflect-promote` 가 ledger 에 append 했을 때 완료다.
- 같은 교훈이 ledger 에 `status: active` 로 이미 있는지 여기서 판정하려 하지 마라 — 중복 판정도 `/reflect-promote` §A-3 소관이다. 카이젠은 후보를 그대로 내고 중복은 그쪽이 거른다.
- 이 후보 파일은 **이번 사이클 §0.5 의 입력이 아니다.** 같은 사이클 안에서 왕복시키면 자기검증 루프다.

### Step F4: PR 생성 (구 Step 12)

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

   - planning-kit 변경 있으면: `planning-kit/.claude-plugin/plugin.json` 버전 bump
     (⚠ `/planning-kaizen` 스킬은 이 레포 개발용으로 planning-kit 플러그인에 포함되지 않는다 — bump 대상은 planning-kit 플러그인에 포함된 10 개 스킬 + planning-reviewer 에이전트)

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
   - `docs/planning/research-log.md` (planning 관련, Phase 11) — **파일이 없으면 신규 생성**
   - `docs/flutter/research-log.md` (flutter 관련, Phase 5) — **파일이 없으면 신규 생성**
   - 각 per-kit research-log 는 frontmatter (title, version, last_updated), "## [YYYY-MM-DD] - Phase N kaizen" 엔트리, 리서치 소스 URL 최소 5 건 포함.

4. **evals 갱신 체크:**

   - 각 플러그인 `evals/evals.json` (존재 시) 의 `id` 필드와 현재 `<plugin>/skills/` 디렉토리의 스킬 목록이 일치하는지 확인
   - 스킬이 신규 추가 / 삭제 / 리네임되었으면 evals.json 도 갱신
   - 정합성 유지 확인을 `.harness/.meta/evals-audit-{YYYY-MM-DD}.md` 에 기록 (변경 없음이어도 점검 기록)

5. **kaizen-failure-count.yaml 업데이트:**

   - `.harness/.meta/kaizen-failure-count.yaml` 에 `phase_1` ~ `phase_12` 엔트리가 모두 존재하는지 확인 (없으면 추가)
   - Regression PASS 인 Phase 는 카운터 0 으로 리셋
   - Regression FAIL 인 Phase 는 카운터 +1 → 2 이상이면 사용자 에스컬레이션
   - `last_updated` 필드를 카이젠 실행 날짜로 갱신
   - REJECT → iter2 APPROVE 흐름이 있었으면 해당 Phase 엔트리에 주석으로 기록

6. **Post-Kaizen Checklist (최종 검증 — 모든 항목 PASS 후에만 PR 생성):**

   아래 체크리스트를 **완전히** 통과하지 않으면 PR 생성을 **금지**한다. 하나라도 미통과 시 해당 Step 으로 돌아가 수정한다.

   - [ ] 각 변경된 플러그인 `plugin.json` 버전이 bump 되었다 (planning-kit 포함)
   - [ ] `.claude-plugin/marketplace.json` 의 플러그인 `description` (planning-kit 포함) 이 버전/날짜와 정합한다
   - [ ] `python3 scripts/sync-docs.py --check-only` 가 "모든 README가 동기화 상태입니다" 를 반환한다
   - [ ] `python3 scripts/validate-plugin.py` 가 모든 플러그인 (planning-kit 포함) OK, Exit 0 을 반환한다
   - [ ] `docs/kaizen/changelog.md` 에 이번 사이클 엔트리가 추가되었다 (Phase 1~4 변경 반영)
   - [ ] `docs/kaizen/flutter-changelog.md` 에 Phase 5 엔트리가 추가되었다 (해당 Phase 변경 있을 시)
   - [ ] `docs/kaizen/research-log.md` + `docs/kaizen/flutter-research-log.md` + per-kit research-log 6개 파일 (backend/infra/rust/react/flutter/planning) 이 모두 존재하고 이번 사이클 엔트리를 포함한다
   - [ ] Step F2 docs-site 재생성이 실행되었다 — 변경된 소스에 대응하는 `docs/<plugin>/*.html` 이 최신 상태다
   - [ ] Step F3 글로벌 피드백 정리가 실행되었다 — `.harness/.meta/cleanup-log.yaml` 에 이번 사이클 엔트리가 있다
   - [ ] Step F3.5 메모리 승격 후보 산출이 실행되었다 — `.harness/.meta/memory-promotion-candidates-{YYYY-MM-DD}.md` 가 존재하고 (후보 0 건이면 `candidates: []`), 카이젠이 승격 ledger 를 직접 수정하지 않았다
   - [ ] `.harness/.meta/kaizen-failure-count.yaml` `last_updated` 필드가 이번 사이클 날짜다
   - [ ] `.harness/.meta/evals-audit-{YYYY-MM-DD}.md` 가 존재한다 (evals 점검 기록)
   - [ ] Phase 1~14 간 scope 격리가 유지되었다 — 각 Phase commit 이 다른 Phase 의 소스 파일을 수정하지 않았다 (검사 대상 킷 목록은 `marketplace.json` 에서 유도된다 — 하드코드하지 않는다)

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
