# Sprint Feedback
Feature: 인사이트 2026-09-24 — 커밋 안전 훅 · dart 편집 파일 포맷 훅 · 화면 확인 스킬 · 카이젠 수집기 최신 인사이트 반영
Evaluated: 2026-09-24 15:20
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-insights-0924-hooks-skill-collector.md
- sha256: de02208cf9ebac6a8370eded98950bca45635b36d714daa13439a746206d85db
- status: active
- slug: insights-0924-hooks-skill-collector
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 봉인 커밋 대조(1-e-3): seal_commit=36cfbbd, files=1, 산문 차이 없음, conditions_digest 불변
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT status=active)

## Amendments
- amendments: 2
- A-01 (DG-02 옛 판 같은 경고 줄 제외): direction=relaxing (amend_direction_oracle — 측정 집합에서 CLAUDE.md:142 MD036 1줄 제외, PASS 집합 증가) · consent=anchored (Codex 검토 `insights/codex-amend-a01.md` VERDICT: APPROVE, 사용자 위임 발언 인용 + queued_command 앵커) → **PASS 근거 가능**. DG-02 측정에 실제 반영함
- A-02 (end_sha 기록): 조건 완화/강화가 아니라 AR-01 상한값 기록. 0a32b969752164ce76bc2c2d6afd43c88b5e34dd — `sprint_head` 의 조상 확인됨(merge-base --is-ancestor 통과)
- PASS 근거 가능: 1 (A-01) · PASS 근거 불가: 0
- 집합형 direction 계산 결과: A-01 = `relaxing removed=1(CLAUDE.md:142/MD036)`  (자기신고 아님, 390dea8 판과 직접 대조해 계산)

## User Correction Audit
- correction_log_status: available (`/Users/jackson/.claude/logs/insights-0924-kaizen/2026-09.md`)
- unreflected_corrections: 0 — 로그의 [prompt] 항목은 전부 reflect-kit 자동 분석 서브세션(다른 session id)의 분석 지시문과 구현 워크플로 task-notification이며, 사용자가 직접 방향을 바꾼 교정 발언은 없었다
- verdict 영향: 없음 (표면화 전용)

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `.harness/sprint-contract-insights-0924-hooks-skill-collector.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. DG-02(신규 MD025 중복 H1)·DG-03(validate-post-kaizen.py 2 FAIL) 을 FAIL 로 판정한 것이 계약 조건의 원래 의도와 다르게 해석한 오판인가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중 공허한 통과가 있는가? (SK-02/SK-08/AR-05/AR-06/SC-04/SC-08/SC-01 은 음성 대조·mutation 으로 직접 재확인했다)
- 끝내 못 띄웠으면 `none` 으로 내리고 사유를 `cross_diagnosis_notes` 에 적는다 (부모 담당)

## Results

### Skill (9/9)
- [x] SK-01: flutter-ui-verify 스킬 존재 + 절차 참조 + 복제 검사 — PASS
  - 근거: `flutter-toolkit/skills/flutter-ui-verify/SKILL.md` 존재, `validate-plugin.py flutter-toolkit` exit 0, frontmatter name/user-invocable 각 1회, 본문에 `visual-evidence-protocol.md`·`Step 0`~`Step 4`·`Visual Evidence Block` 각 ≥1회, 복제 검사(python3, 25자 이상 줄 완전 일치) = 0
- [x] SK-02: trigger_overlap 0쌍 — PASS
  - 근거: 계약의 `# oracle: trigger_overlap` 블록 원문 실행 → `new_phrases=5 other_files=19 exact=0 substring=0` exit 0. 양성 대조(임시 사본에 `"UI 컴포넌트 확인"` 삽입) → `substring=1` exit 1 확인
- [x] SK-03: visual-evidence-protocol.md 21낱말 구간별 검사 — PASS
  - 근거: awk 구간 절단(Step0~1/Step2~3/Step3~4/Step4~VEB/머리말) 후 21낱말 전부 ≥1회, Step0 구간에 `관례 표`+`2 개 이상` 같은 줄 1회(`flutter-toolkit/references/visual-evidence-protocol.md:52`). 음성 대조: 390dea8 판 같은 섹션 절단 기준 21낱말 전부 0 (직접 재현, git show 390dea8 사본으로 측정)
- [x] SK-04: UI 스킬 5개 편집 전 규약 호출 — PASS
  - 근거: 5개 파일 모두 지정 구간에서 `기준 캡처는 편집 전에`+`Step 0` 같은 줄 발견(head_line 87·47·14·14·13, 계약 claim과 일치). 음성 대조: 390dea8 판 5파일 모두 0회
- [x] SK-05: flutter-kaizen 짝 맞춤 표 갱신 — PASS
  - 근거: `flutter-toolkit/skills/flutter-kaizen/SKILL.md:45` 에 `편집 전` 포함. 390dea8 판 :45행에는 없음
- [x] SK-06: evals.json 신규 사례 2개(A: flutter-ui-verify, B: flutter-widget 채점기준) — PASS
  - 근거: `evals.json` id=21(flutter-ui-verify) · id=22(flutter-widget, 7낱말 전부 포함 + `서로 다른 기존 화면 경로`·`2 개 이상`·`1 개면 FAIL` 한 assertion에 공존). id 중복 0(22개 전부 unique). `sync-evals.py --check-only` exit 0, `run-evals.py` 108 passed 0 failed
- [x] SK-07: harness 카이젠 3스킬이 데이터 풀 §0 참조 — PASS
  - 근거: 3파일 각각 `kaizen-input/insights-report.md`=0, `kaizen-data-pool`≥1 (2·1·1 매칭). 390dea8 판은 각각 2·1·1(옛 참조 존재) 확인
- [x] SK-08: 오케스트레이터 Step 0 신규 선언 — PASS
  - 근거: Step0~0.5 구간에 `--usage-data`(docs-contract 블록 내)1회·`usage_data_inputs`1회·`우선순위대로`0회·`report_file`≥1·`0-b`≥1. `validate-doc-contracts.py -v` exit 0. 390dea8 판 같은 구간 `우선순위대로` 1회
- [x] SK-09: check-insights-tracking.py --final 4경우 + 오케스트레이터 Final 호출 — PASS
  - 근거: (a) 현재 판 `--final` → exit 1(74행 미완료) (b) 전 Phase행 채운 사본 → exit 0 (c) 그 사본의 QA칸 1개만 비움 → exit 1 (d) `--final` 없이 exit 0. `### Step F1:`~`### Step F2` 구간에 명령 1회

### Script (9/9)
- [x] SC-01: 커밋 안전 훅이 5가지 사고 형태 차단 — PASS
  - 근거: `commit-guard-test.sh` 실행 exit 0, ①~⑤(및 ⑤-cd·⑤-C) 전부 exit 2 + stderr 사유. discriminating: `del_count -gt limit` 판정 줄 제거한 사본으로 재시험 → ①②⑤ exit 0 으로 반전, 시험 exit 1 (직접 mutation 확인)
- [x] SC-02: 정상 커밋 9경우 차단하지 않음 — PASS
  - 근거: ⑥~⑭ 전부 exit 0 · stdout 빈 값
- [x] SC-03: 커밋 직후 알림 — PASS
  - 근거: ⑮ additionalContext에 `60`·`git reset --soft HEAD~1` 포함, ⑯ 빈 값
- [x] SC-04: dart 포맷 훅 8경우 — PASS
  - 근거: `format-edited-dart-test.sh` exit 0, 12경우 불일치 0. discriminating: 생성물 제외 줄 삭제한 사본 → ⑤ 두 경우 기록 1로 반전, 시험 exit 1 (직접 mutation 확인)
- [x] SC-05: 수집기 보고서 선택 로직 7경우 — PASS
  - 근거: `test-collect-kaizen-data.py` 29 통과 0 실패 (①~⑦ 전부 PASS, ER-03 포함)
- [x] SC-06: 실제 수집 결과가 최신 인사이트 반영 — PASS
  - 근거: `collect-kaizen-data.py --skip-validate` 실행 → `✓ 선택 .claude/kaizen-input/insights-report.md`, `report_file` frontmatter = 최신 보고서명과 일치. pool.md `## 0.`~`## 0.5` 구간에 `2026-09-14`·`2026-09-23` 각 ≥1회, `2026-06-12 ~ 2026-08-12` 0회 (양성 대조: `insights/pool-before.md` 는 1회 확인)
- [x] SC-07: 데이터 풀 §0 `### 0-b` 절 + facets 대조값 일치 — PASS
  - 근거: 제목 순서 `## 0.`(8) < `### 0-b`(194) < `## 0.5`(271). `# oracle: facets_count` 실행값(sessions=18, fit-pal 10·claude-plugins 6·temp 2, buggy_code 28·wrong_approach 20·misunderstood_request 14)이 pool.md 문구와 정확히 일치
- [x] SC-08: 수집기·검사기 facets 입력 짝 — PASS
  - 근거: `--help`에 `--usage-data`, `KNOWN_KEYS`/`COMPARED_KEYS`에 `usage_data_inputs`. `validate-doc-contracts.py -v` exit 0. discriminating(2건, 사본 사용 후 원상복구 `git diff --exit-code` 확인): ① `usage_data_inputs` 줄 삭제 → exit 1(불일치 신규 검출) ② 경로값 오타 → exit 1
- [x] SC-09: 신규 파일 문법·CI 등록 — PASS
  - 근거: `bash -n` 4파일 exit 0, `shellcheck -S warning` 4파일 경고 0, `py_compile` 4파일 exit 0, `ci.yml`에 3개 run: 줄 각 1회 이상, 로컬 재실행 3개 전부 exit 0

### Error (3/3)
- [x] ER-01: 깨진 입력 10경우 무해 처리 + 알림 — PASS
  - 근거: commit-guard.sh pre(a)(b)(c)(d)+post(a)(b)(c) 7경우, format-edited-dart.sh (a)(b)(c) 3경우, 총 10경우 전부 계약대로 동작(jq 없는 PATH 준비 확인 포함)
- [x] ER-02: 차단 시 판단 재료 제공 — PASS
  - 근거: stderr 5줄, `51`·상위폴더·`HARNESS_COMMIT_GUARD=off`·`승인` 전부 포함, 파일명 목록 없음
- [x] ER-03: facets 못 읽음 비침묵 처리 — PASS
  - 근거: `test-collect-kaizen-data.py` ER-03 관련 7개 서브체크 전부 PASS(세션3·묶음1·임시1·못읽은파일1 stderr+풀 양쪽, facets 없으면 exit0+`(없음)`)

### Architecture (6/6)
- [x] AR-01: 변경이 34경로 화이트리스트 내 — PASS
  - 근거: `git diff --name-only 390dea8..0a32b96...` (`.harness` 제외) = 정확히 34개 파일, whitelist와 `comm` 비교 결과 양방향 차집합 0. end_sha가 sprint_head(8a3ff98)의 조상(`merge-base --is-ancestor`) 확인. `.harness/sprint-contract*.md` 전체 `verify_seal` → SEAL_BROKEN 0개(SEAL_ABSENT 5개는 레거시, 경고일 뿐)
- [x] AR-02: 훅 등록 + 실행 비트 — PASS
  - 근거: `harness/hooks/hooks.json` PreToolUse/PostToolUse 각 1개, `settings-hooks.json` 동일, `flutter-toolkit/hooks/hooks.json` matcher `Edit|Write|MultiEdit`(Edit·Write 모두 포함) 1개. 두 스크립트 `stat -f %Lp` = 755. `validate-plugin.py harness`/`flutter-toolkit` 각 exit 0
- [x] AR-03: 특정 앱 이름 없음 — PASS
  - 근거: 4파일 `grep -ciE 'fitpal|fit-pal'` 전부 0. 양성 대조(임시 파일에 `mcp__fitpal-mobile__...`) → 1
- [x] AR-04: 문서-훅/스킬 정합 — PASS
  - 근거: skill-design-guide.md 1회, harness/README.md `commit-guard` 4회·`HARNESS_COMMIT_GUARD=off` 1회, flutter-toolkit/README.md 3항목 각 ≥1회. `# oracle: skill_count_lines` 4곳 모두 hits=19=dirs=19 OK exit 0. `sync-docs.py --check-only` exit 0
- [x] AR-05: 포맷 권고가 변경 파일만 대상 — PASS
  - 근거: 3파일 `format (lib|\.)...`=0, `git diff --name-only`≥1(전부 1). 390dea8 판 3파일 첫 grep 전부 1
- [x] AR-06: 인사이트 항목·제안 전부 처리 배정 — PASS
  - 근거: `# oracle: tracking_check` 실행 → exit 0 `TRACKING_OK`. 390dea8 판 같은 스크립트로 재실행 → exit 1(F01~F32 배정 없음 다수, 지정 배정 3건 어긋남) — discriminating 확인

### Anti-patterns (3/3)
- [x] AP-01: 신규 6파일 버전 하드코딩 없음 — PASS
  - 근거: `harness/scripts/commit-guard.sh`·`harness/evals/hooks/commit-guard-test.sh`·`flutter-toolkit/scripts/format-edited-dart.sh`·`flutter-toolkit/evals/hooks/format-edited-dart-test.sh`·`scripts/check-insights-tracking.py`·`scripts/test-collect-kaizen-data.py` 전부 `grep -nE '[0-9]+\.[0-9]+\.[0-9]+'` 0건
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `validate-plugin.py --check=code-fence` 14 플러그인 전부 `0 bare` exit 0
- [x] AP-04: SKILL.md name 필드 — PASS
  - 근거: `validate-plugin.py flutter-toolkit` V1 OK, `grep -c '^name: flutter-ui-verify$'` = 1

### Reusability (2/2)
- [x] RE-01: 두 훅이 독립 실행 파일 — PASS
  - 근거: 두 스크립트 `grep -cE '^[[:space:]]*(\.|source)[[:space:]]'` 각 0
- [x] RE-02: 규약 재사용(복제 아님) + 기존 차단 방식 재사용 — PASS
  - 근거: SK-01의 복제 검사 0(재확인), `commit-guard.sh` 내 `exit 2` ≥1(실측 2)

### Diagnostics (2/4, N/A 1)
- [x] DG-01: N/A — release.sh 미변경 (측정값: 0, 기준: 0) — PASS(N/A)
  - 근거: `git diff --name-only 390dea8..0a32b96... | grep -c '^scripts/release.sh$'` = 0
- [ ] DG-02: 이번에 더한 줄에 걸린 새 markdownlint 경고 0개 — **FAIL**
  - 근거: `markdownlint-cli2@0.23.2`(세션 scratchpad 설치본, `{"config":{"MD013":false}}`)로 diff 대상 20개 .md 파일(`.harness` 제외) 전수 실행(xargs로 일괄 호출, 445건 전체 경고 파싱) → `git diff -U0 390dea8..0a32b96` 로 각 파일의 실제 추가 줄 번호를 계산해 교집합만 필터링 → A-01 예외(`CLAUDE.md:142` MD036) 제외 후에도 **1건 잔존**: `flutter-toolkit/skills/flutter-ui-verify/SKILL.md:23 MD025/single-title/single-h1 — Multiple top-level headings [Context: "UI Verify"]`. 이 파일은 통째로 새 파일(전 줄이 added line)이라 13행 `# Flutter UI Verify`(A-01 커밋에서 MD041 대응으로 추가)와 23행 `# UI Verify` 두 H1이 공존한다. 측정값: 1 (기준: 0)
  - 수정: `flutter-toolkit/skills/flutter-ui-verify/SKILL.md:23`의 `# UI Verify`를 `## UI Verify`로 낮추거나 제거한다 (본문 구조상 Process 앞 소개 문단의 제목이라 H2가 맞다)
- [ ] DG-03: N/A 주장(release.sh 미변경) — 첨부 측정(run-evals.py·validate-post-kaizen.py FAIL 0) 불충족 — **FAIL**
  - 근거: DG-01과 같은 grep 0(확인). `python3 scripts/run-evals.py` → 108 passed 0 failed(충족). 그러나 `python3 scripts/validate-post-kaizen.py --verbose`(기본 `--since main`, `main`=`origin/main`=390dea8로 계약 기준 커밋과 정확히 일치) → **11 PASS / 2 FAIL / 2 SKIP**: (1) `docs-site-regen` — `harness/docs/guides/skill-design-guide.md` 내용이 바뀌었는데(AR-04가 요구한 1줄) `docs/harness/*.html`이 재생성되지 않음 (2) `scope-isolation` — 유일 구현 커밋 `cb5d0a1`이 `harness/skills/`(contract-kaizen·evaluator-kaizen·harness-kaizen)와 `flutter-toolkit/skills/`를 동시에 건드려 cross-phase 판정. 이 조건이 명시한 "FAIL 0" 요건이 거짓이므로 N/A 남용에 해당(Canonical Unverified-Evidence Protocol 2항)
  - 참고: AR-01의 34파일 화이트리스트 자체가 `docs/harness/*.html`을 포함하지 않아, 이 조건대로 하려면 계약 범위를 벗어나거나(문서 사이트 재생성) 구현 커밋을 분리해야 했다 — 계약 내부 충돌 가능성이 있다(아래 Improvement 참조)
  - 수정: (a) `/docs-site` 스킬로 `docs/harness/*.html` 재생성 후 커밋에 추가, 또는 (b) 계약을 개정해 `docs-site-regen`·`scope-isolation`을 DG-03 측정에서 제외하고 그 사유를 문서화
- [x] DG-04: 실기 Claude Code 세션에서 훅 작동 확인 — PASS
  - 근거: 임시 저장소(65개 파일 커밋 후 60개 삭제 스테이징)에서 `claude -p "...git commit -m 'delete batch'..." --plugin-dir <워크트리>/harness --permission-mode acceptEdits` 실행(1차 시도 성공, 재시도 불요). 실행 후 `git rev-list --count HEAD` = 1(불변, 커밋 안 생김). 출력에 "커밋 안전 훅이 막았습니다. 삭제 50개 초과라서..." 및 삭제 60개·위치·승인 필요 문구 확인

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (36 - 0) / 36 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (미검증 카운터에 의한 자동 REJECT 아님 — DG-02·DG-03은 직접 측정된 FAIL)

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-01·ER-02(데이터 유실 방지) · SC-04(생성물 오염 방지) · SC-08(선언-실체 대조) · AR-06(추적 표 무결성)
- 결합 확인: 전부 계약이 지목한 실제 구현 스크립트를 직접 mutation → 시험 exit 반전 확인
- 음성 대조: SC-01(판정 줄 삭제, exit0→2건 반전) · SC-04(생성물 제외 줄 삭제, ⑤ 반전) · SC-08(선언 줄 삭제/오타, 2건 각각 exit1) · AR-06(390dea8 판 재실행, exit1) — 전부 계약에 명시된 대로 직접 실행 확인. SC-08 사본 사용 후 `git diff --exit-code` 로 원상 복구 확인

## Evidence Validity
- 검사 대상 증거: 36건 전 조건
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 계약의 `# oracle:` 5블록(trigger_overlap·facets_count·report_period·skill_count_lines·tracking_check) 전부 원문 그대로 추출해 zsh(사용자 셸)에서 직접 실행 완료. bash 별도 검증은 SC-01/SC-04 테스트 스크립트가 이미 `#!/bin/bash` 셔뱅으로 zsh 환경에서 정상 실행되는 것으로 대체 확인(둘 다 macOS 기본 zsh 세션에서 bash 서브프로세스로 무사고 실행)
- 양성 대조: SK-02(임시 사본 삽입 substring=1) · SK-03(390dea8 섹션 재현 0/21) · AR-03(임시 파일 1) · SC-06(pool-before.md 1) · SC-07/AR-06(390dea8 재실행 exit1) — 전부 evaluator 직접 실행
- 무효 0건은 미검증 카운터에 영향 없음

## User-Reported Failures
- 해당 없음 (이번 평가는 최초 판정이며 사용자 재현 보고 없음)

## Summary
- Total: 34/36 conditions passed (N/A 1: DG-01)
- Verdict: REJECT
- FAIL 항목:
  1. DG-02 — `flutter-toolkit/skills/flutter-ui-verify/SKILL.md:23` MD025 중복 H1 (신규 추가 줄). 수정 우선순위: 상 (2줄 수정으로 해결 가능, 가장 빠른 재평가 경로)
  2. DG-03 — `validate-post-kaizen.py`가 요구한 "FAIL 0"이 미충족(docs-site-regen·scope-isolation). 수정 우선순위: 중 (문서 사이트 재생성 또는 계약 개정 필요, 사용자 판단 필요)

## Improvement Suggestions
- [DG-02] 측정-환경-오염 — SKILL.md 신규 작성 시 H1이 정확히 1개인지(`grep -c '^# '`) 계약에 직접 못박아, A-01류 "MD041만 고치고 MD025를 못 봄" 재발을 막는다
- [DG-03] 측정-환경-오염 — AR-01의 화이트리스트(34경로, `docs/harness/*.html` 미포함)와 DG-03이 요구하는 `validate-post-kaizen.py`의 `docs-site-regen`/`scope-isolation` 체크가 구조적으로 부딪힌다. 다음 계약에서는 (a) `docs/harness/*.html` 재생성을 화이트리스트에 포함하거나 (b) DG-03 측정에서 `--verbose` 출력 중 `docs-site-regen`·`scope-isolation` 두 검사를 명시적으로 제외한다고 적어, "N/A 인데 FAIL 0을 요구"하는 자기모순을 없앤다
