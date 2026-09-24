# Sprint Feedback
Feature: 인사이트 2026-09-24 — 커밋 안전 훅 · dart 편집 파일 포맷 훅 · 화면 확인 스킬 · 카이젠 수집기 최신 인사이트 반영
Evaluated: 2026-09-24 17:55
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: .harness/sprint-contract-insights-0924-hooks-skill-collector.md
- sha256: de02208cf9ebac6a8370eded98950bca45635b36d714daa13439a746206d85db
- status: active
- slug: insights-0924-hooks-skill-collector
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — 사용자가 절대경로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 봉인 커밋 대조(1-e-3): seal_commit=36cfbbd files=1(계약 파일 단독) · 봉인 시점 원문과 산문 diff 없음(status 전환 없음, 조건 줄만 확인 대상인데 그마저 무변경) · conditions_digest 불변
- 재확인(Step 5): 일치 (sha256 동일)
- status_transition: active -> done

## Amendments
- amendments: 3 (A-01, A-02, A-03)
- PASS 근거 가능: 3
  - A-01 [direction=relaxing(amend_direction_oracle: 측정 대상 줄 1개 제외 → PASS 집합 증가) · consent=anchored(Codex 검토 `insights/codex-amend-a01.md` VERDICT: APPROVE, 기록시각 2026-09-24T14:57:31+0900 — 반영 커밋 22f1c5d(15:26:29)보다 앞섬. 사용자 위임 발언은 세션 de8c7935 queued_command 2026-09-24T04:04:16.964Z)] DG-02 측정에서 `CLAUDE.md:142`(390dea8 판 같은 줄에 이미 같은 MD036 경고 존재 — 직접 재현 확인) 1줄 제외
  - A-02 [절차성 — direction 없음] end_sha 고정값 선언, AR-01 상한으로 사용
  - A-03 [direction=unchanged] 구현 커밋 재분할(킷 경계 분리) — 조건 문구·PASS 집합 불변, 파일 내용은 H1 수정 외 무변경(직접 diff 확인)
- PASS 근거 불가: 0
- 집합형 direction 계산 결과: 해당 없음(A-01은 파일 화이트리스트가 아니라 측정 대상 줄이므로 amend_direction_oracle 적용 — 위에 기재)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/insights-0924-kaizen/2026-09.md`)
- unreflected_corrections: 0
  - 스프린트 구간(2026-09-24 13:45~평가시각)의 [prompt] 항목 11건 전수 확인 — reflect-kit 백그라운드 분석 프롬프트 6건·task-notification 4건·사용자 단문 "ㄱㄱ" 1건. 계약/구현 방향을 교정하는 사용자 발언 없음
- verdict 영향: 없음 (표면화 전용)

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/.harness/sprint-contract-insights-0924-hooks-skill-collector.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다. 끝내 띄우지 못했으면 `none` 으로 내리고 사유를 `cross_diagnosis_notes` 에 적는다

## Results

### Skill (9/9)
- [x] SK-01: flutter-ui-verify 스킬이 규약 단계를 번호로 가리킨다 — PASS
  - 근거: `flutter-toolkit/skills/flutter-ui-verify/SKILL.md` frontmatter `name`·`user-invocable: true` 각 1회, 본문에 visual-evidence-protocol.md·Step 0~4·Visual Evidence Block 각 1회 이상. 복제 검사(python3 직접 실행): 규약 25자 이상 줄 중 스킬 본문에 글자 그대로 있는 줄 0개. `validate-plugin.py flutter-toolkit` exit 0
- [x] SK-02: 새 스킬 description 구절이 기존 18스킬+1에이전트와 겹치지 않는다 — PASS
  - 근거: `# oracle: trigger_overlap` 원문 그대로 뽑아 실행 → `new_phrases=5 other_files=19 exact=0 substring=0` exit 0. 양성 대조: flutter-ui-verify description에 "UI 컴포넌트 확인" 주입한 사본 재실행 → `substring=1` exit 1 (직접 재현 확인)
- [x] SK-03: visual-evidence-protocol.md 가 인사이트 5가지를 21낱말로 담는다 — PASS
  - 근거: python3로 머리말/Step0/Step2/Step3/Step4 구간 절단 후 21낱말 전수 확인(전부 count≥1), Step0 구간 내 "관례 표"·"2 개 이상" 같은 줄 존재 확인
- [x] SK-04: UI 수정 스킬 5개가 편집 전 구간에서 규약을 부른다 — PASS
  - 근거: 5개 파일 각 지정 구간(widget/screen: `### 2. 기존 패턴 분석`~`### 3.`, skeleton/transition/responsive: `## Gotchas`~`## 0.`)에서 "기준 캡처는 편집 전에"+"Step 0" 같은 줄 확인. 구간 시작줄 87·47·14·14·13 — 계약 명시값과 일치
- [x] SK-05: flutter-kaizen 짝 맞춤 표가 편집 전 호출까지 대조한다 — PASS
  - 근거: `flutter-toolkit/skills/flutter-kaizen/SKILL.md:45` visual-evidence 행에 "편집 전" 포함
- [x] SK-06: evals.json 에 사례 A(flutter-ui-verify)·사례 B(flutter-widget, 편집전 채점) 가 있다 — PASS
  - 근거: python3로 evals.json 파싱 — flutter-ui-verify 1건(id 21), flutter-widget 중 7낱말 전부 포함 1건(id 22, assertion에 "서로 다른 기존 화면 경로"·"2 개 이상"·"1 개면 FAIL" 동일 문장 포함). id 중복 0. `sync-evals.py --check-only` exit 0 · `run-evals.py` 108 passed 0 failed
- [x] SK-07: harness 카이젠 3스킬이 요약본 대신 데이터 풀 §0 을 읽는다 — PASS
  - 근거: 3파일 각 `kaizen-input/insights-report.md`=0회·`kaizen-data-pool`≥1회 (390dea8 판은 2·1·1 — 계약 명시값과 일치, 직접 확인)
- [x] SK-08: 오케스트레이터 Step 0 이 usage-data 입력을 선언한다 — PASS
  - 근거: `### Step 0:`~`### Step 0.5:` 구간에서 `--usage-data` 1회(docs-contract 블록 내)·`usage_data_inputs` 1회·`우선순위대로` 0회·`report_file`≥1·`0-b`≥1. `validate-doc-contracts.py -v` exit 0
- [x] SK-09: 전체 카이젠 Final이 처리 배정표를 닫는다 — PASS
  - 근거: (a) 지금 판 `--final` → exit 1(74건 Phase 행 미완료) (b) 74행 전부 채운 사본 → exit 0 (c) 그중 1건 QA만 비운 사본 → exit 1 (d) `--final` 없이 지금 판 → exit 0 (e) `### Step F1:`~`### Step F2:` 구간에 `check-insights-tracking.py --final` 1회. 음성 대조: 390dea8 판 스크립트 부재·구간 내 `insights-report.md` 0회 확인

### Script (9/9)
- [x] SC-01: 커밋 안전 훅이 사고 형태 5종을 막는다 — PASS
  - 근거: `commit-guard-test.sh` 직접 실행 — ①~⑤(변형 포함 9개 하위 케이스) 전부 exit 2 + stderr 사유. 음성 대조(사본 mutation, 판정줄 제거): ①② exit 0 으로 반전, 시험 스크립트 exit 1 확인(직접 재현)
- [x] SC-02: 커밋 안전 훅이 정상 커밋을 막지 않는다 — PASS
  - 근거: 같은 시험 스크립트 ⑥~⑭ 전부 exit 0 · stdout 빈 값
- [x] SC-03: 커밋 직후 훅이 삭제 50개 초과를 알린다 — PASS
  - 근거: ⑮(60개 삭제) additionalContext에 "60"·"git reset --soft HEAD~1" 포함, ⑯(1개 삭제) stdout 빈 값
- [x] SC-04: 포맷 훅이 편집 파일 1개에만 포맷을 부른다 — PASS
  - 근거: `format-edited-dart-test.sh` 직접 실행 — ①~⑧ 전부 일치(12경우 불일치 0). 음성 대조(생성물 제외줄 삭제 사본): ⑤ 기록 1로 반전, 시험 exit 1 확인(직접 재현)
- [x] SC-05: 수집기가 report_file 기준으로 선택한다 — PASS
  - 근거: `test-collect-kaizen-data.py` 직접 실행 — ①~⑦ 전부 PASS(29 통과 0 실패)
- [x] SC-06: 실제 수집 결과가 최신 인사이트를 싣는다 — PASS
  - 근거: 직접 실행한 `collect-kaizen-data.py --skip-validate` — stderr `✓ 선택 .claude/kaizen-input/insights-report.md`, 그 파일 frontmatter `report_file`이 `# oracle: report_period`가 낸 newest(`report-2026-09-24-095238.html`)와 일치. pool.md `## 0.`~`## 0.5` 구간에 `2026-09-14`·`2026-09-23` 각 존재, 옛 기간 문자열 0회
- [x] SC-07: §0 안 `### 0-b` 가 원본 재집계값과 일치한다 — PASS
  - 근거: `## 0.` < `### 0-b`(194행) < `## 0.5`(271행) 순서 확인. `# oracle: facets_count` 직접 실행값(sessions=18·fit-pal10·claude-plugins6·temp2·buggy_code28·wrong_approach20·misunderstood_request14)이 `### 0-b` 절 숫자와 전부 일치
- [x] SC-08: 수집기·문서 선언검사기가 facets 입력을 짝으로 가진다 — PASS
  - 근거: `--help`에 `--usage-data`, `validate-doc-contracts.py` KNOWN_KEYS·COMPARED_KEYS에 `usage_data_inputs`. `-v` exit 0. compare() 함수 직접 호출 음성 대조: 키 삭제 사본→violation 1건, 값 오타 사본→violation 1건(직접 재현)
- [x] SC-09: 새 파일 문법 통과 + CI 시험 3종 등록 — PASS
  - 근거: `bash -n` 4개 exit 0, `shellcheck -S warning` 4개 exit 0, `py_compile` 4개 exit 0, `ci.yml`의 `run:` 줄에 3개 시험 각 1회 이상, 로컬 직접 실행 전부 exit 0

### Error (3/3)
- [x] ER-01: 두 훅이 깨진 입력에서 안 멈추고, 검사 불가를 알린다 — PASS
  - 근거: 두 시험 스크립트 내 총 10경우(commit-guard pre 4·post 3, format-edited-dart 3) 전부 기대와 일치
- [x] ER-02: 커밋 안전 훅이 판단 재료·우회법을 준다 — PASS
  - 근거: SC-01① stderr에 "51"·상위폴더명·"HARNESS_COMMIT_GUARD=off"·"승인" 전부 존재, 5줄(≤15줄)
- [x] ER-03: 수집기가 facets 못 읽음을 조용히 넘기지 않는다 — PASS
  - 근거: `test-collect-kaizen-data.py` ER-03 하위 10개 서브체크 전부 PASS(세션3·묶음1·임시1·못읽음1 stderr·풀 양쪽 확인, facets없음→exit0·"(없음)")

### Architecture (6/6)
- [x] AR-01: 변경이 화이트리스트 34경로 안에 있다 — PASS
  - 근거: `git diff --name-only 390dea8..2a447bc`(34파일)와 계약 화이트리스트(34경로) `comm -23` 비교 결과 차집합 0. end_sha(2a447bc71d7…)가 sprint_head의 조상임을 `merge-base --is-ancestor`로 확인. `.harness` SEAL_BROKEN 0건(전 계약 파일 전수 확인)
- [x] AR-02: 두 훅이 등록되고 실행 비트가 있다 — PASS
  - 근거: `harness/hooks/hooks.json`·`settings-hooks.json` 모두 PreToolUse·PostToolUse에 commit-guard.sh 각 1개, `flutter-toolkit/hooks/hooks.json` PostToolUse에 format-edited-dart.sh 1개(matcher `Edit|Write|MultiEdit`가 Edit·Write 모두 포함). 둘 다 `CLAUDE_PLUGIN_ROOT` 사용. 실행비트 755·755. `validate-plugin.py harness`·`flutter-toolkit` 둘 다 exit 0
- [x] AR-03: 새·고친 파일에 특정 앱 이름이 없다 — PASS
  - 근거: 4파일 `grep -ciE 'fitpal|fit-pal'` 전부 0. 양성 대조: `mcp__fitpal-mobile__…` 문자열 담은 임시파일에서 1 확인
- [x] AR-04: 킷 문서가 새 훅·스킬과 어긋나지 않는다 — PASS
  - 근거: skill-design-guide.md `commit-guard.sh` 1회↑, harness/README.md `commit-guard`4·`HARNESS_COMMIT_GUARD=off`1, flutter-toolkit/README.md `flutter-ui-verify`2·`format-edited-dart`1·`FLUTTER_TOOLKIT_FORMAT_ON_EDIT`1. `# oracle: skill_count_lines` 직접 실행 — CLAUDE.md 2줄·README.md 2줄 전부 19=19 OK exit 0. `sync-docs.py --check-only` exit 0
- [x] AR-05: 포맷 권고가 폴더 통째가 아니라 변경 파일 기준이다 — PASS
  - 근거: 3파일 `format (lib|\.)(/|[[:space:]]|$)` 0·`git diff --name-only` ≥1. 390dea8 판은 1·1·1(계약 명시값과 일치, 직접 확인)
- [x] AR-06: 인사이트 항목·빈틈 제안 전부가 처리 배정을 받았다 — PASS
  - 근거: `# oracle: tracking_check` 직접 실행(키파일 64줄·중복0) → `TRACKING_OK` exit 0. 음성 대조: 390dea8 판 파일로 재실행 → `TRACKING_FAIL` exit 1(직접 재현)

### Anti-patterns (3/3)
- [x] AP-01: 버전 하드코딩 없음 — PASS
  - 근거: 신규 6파일 전부 `grep -nE '[0-9]+\.[0-9]+\.[0-9]+'` 0건. 패턴 유효성: 임시 버전 문자열 삽입 시 1건 확인
- [x] AP-03: bare code fence 없음 — PASS
  - 근거: `validate-plugin.py --check=code-fence` exit 0 (14 plugins 14 OK)
- [x] AP-04: SKILL.md frontmatter name 필드 — PASS
  - 근거: `validate-plugin.py flutter-toolkit` V1 OK, `grep -c '^name: flutter-ui-verify$'` = 1

### Reusability (2/2)
- [x] RE-01: 두 훅이 독립 실행 파일이다 — PASS
  - 근거: 두 스크립트 `grep -cE '^[[:space:]]*(\.|source)[[:space:]]'` 각 0
- [x] RE-02: 기존 훅과 같은 차단 방식(exit 2) 재사용 — PASS
  - 근거: `commit-guard.sh` `exit 2` 2회. 기존 `sdk-guard.sh`·`run-guard.sh` 도 `exit 2` 사용 확인

### Diagnostics (2/2, N/A 2)
- N/A DG-01: release.sh 미변경 — 확인됨
  - 근거: `git diff --name-only 390dea8..2a447bc | grep -c '^scripts/release.sh$'` = 0
- [x] DG-02: 마크다운 진단 — 더한 줄 새 경고 0개 (amendment A-01 적용) — PASS
  - 근거: `count.py`(구현자 작성 스크립트를 QA가 직접 실행, markdownlint-cli2@0.23.2·MD013 off) → `new_line_warnings=1`(`CLAUDE.md:142` MD036). 이 줄은 A-01 예외 대상 — 390dea8 판 같은 줄(142행)을 같은 설정으로 직접 재검사해 같은 MD036 경고가 이미 있음을 확인. A-01 제외 적용 후 잔여 0. flutter-ui-verify H1(`# Flutter UI Verify`, 13행)과 본문 부제(`## 하는 일`, 23행) 확인 — QA1 지적 MD025 충돌 해소 확인
- N/A DG-03: release.sh 미실행(파일 불변) — 확인됨
  - 근거: DG-01과 동일 grep 0. `run-evals.py` 108 passed 0 failed. `validate-post-kaizen.py` 15 PASS 0 FAIL(특히 `scope-isolation: no cross-phase commits (5 commits · 13 kits)` — A-03 재분할로 QA1의 FAIL 사유 해소 확인)
- [x] DG-04: 실기 Claude Code 세션에서 훅이 대량 삭제 커밋을 막는다 — PASS
  - 근거: 임시 저장소(65파일 커밋 후 60개 삭제 스테이징)에서 `claude -p "...git commit -m 'delete batch'..." --plugin-dir <워크트리>/harness --permission-mode acceptEdits` 직접 실행(1차 시도 성공). 실행 후 `git rev-list --count HEAD` = 1(불변, 커밋 안 생김). 출력에 "커밋 안전 훅이 막았다. 삭제 50개 초과…", "삭제 파일 60개(기준 50개 초과)", "HARNESS_COMMIT_GUARD=off" 문구 확인

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (36 - 0) / 36 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (미검증 카운터에 의한 자동 REJECT 아님)

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-01·SC-02·SC-03·ER-01·ER-02(데이터 유실 방지 — 커밋 안전 훅) · SC-04(생성물 오염/데이터 유실 방지 — 포맷 훅 제외 규칙) · SC-08(선언-실체 대조) · AR-06(추적 표 무결성)
- 결합 확인: 전부 계약이 지목한 실제 구현 스크립트를 QA가 직접 mutation → 시험 재실행으로 exit 반전 확인(원본 파일은 건드리지 않고 스크래치패드 사본 + 환경변수 오버라이드로 실행)
- 음성 대조: SC-01~03·ER-01·ER-02(commit-guard.sh 사본에서 삭제수 판정줄 삭제 → ①② exit0 반전, 시험 exit1) · SC-04(format-edited-dart.sh 사본에서 생성물 제외줄 삭제 → ⑤ 기록1 반전, 시험 exit1) · SC-08(compare() 직접 호출, 키 삭제/오타 사본 → 각 violation1) · AR-06(390dea8 판 재실행 → exit1) — 전부 QA가 이번 평가에서 직접 재현

## User-Reported Failures
- 해당 없음(사용자가 이미 PASS된 조건에 대해 실패를 보고한 바 없음. 본 재평가는 QA1 REJECT 사유 재작업에 대한 통상 재평가)

## Evidence Validity
- 검사 대상 증거: 36건 전 조건
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 계약 내 `# oracle:` 블록 5종 전부 QA가 원문 그대로 뽑아 직접 실행(bash, 이 기계 기본 셸). 셸 종속 로직(zsh nomatch 등)은 없어 zsh 별도 재검증 불필요
- 양성 대조: SK-02(임시 사본 주입 → substring=1 exit1) · AR-03(임시 파일 → 1) · AP-01(임시 버전문자열 → 1) 직접 실행 확인
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 34/34 conditions passed (N/A 2: DG-01, DG-03)
- Verdict: APPROVE

## Improvement Suggestions
- 없음 (계약 결함 미발견 — 이번 재평가에서 측정-수단-부재/측정-방식-불일치 등 통합 어휘 10종에 해당하는 문제 없음)
