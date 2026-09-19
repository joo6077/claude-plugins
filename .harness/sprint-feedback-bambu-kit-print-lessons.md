# Sprint Feedback
Feature: bambu-kit 출력 교훈 3종 — 벽 예산 · 출력 안 함 부품 · 값 섞임 방지
Evaluated: 2026-09-19 14:07
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/bambu-print-lessons/.harness/sprint-contract-bambu-kit-print-lessons.md
- sha256: 6bf3dedf3fd7baf5dc70f8b12d0bf2c75b62ee1b87d5077e5783b394e9631867
- status: active
- slug: bambu-kit-print-lessons
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/bambu-print-lessons
- contract_root_unconfigured: false
- 선택 근거: ladder 2 (세션소유 — owner_session == CLAUDE_CODE_SESSION_ID == be3037df-1ee8-45db-aa79-f54d3cadb2fc)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:47696418d0328fc4 == 재계산값)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 sha256 재계산 동일)
- status_transition: active -> done (APPROVE + 재확인 일치 조건 충족, 아래 실행)

## Amendments
- amendments: 2
- PASS 근거 가능: 1 [AM-02: direction=relaxing · consent=anchored → 사용자 재승인 성립]
- PASS 근거 불가(형식상): 1 [AM-01: direction=unknown · consent=anchored → 표의 "unknown" 행은 anchored 여도 PASS 근거 불가]
  - [unknown · anchored · AM-03 세션 be3037df… 2026-09-19] "제작자 원본 (3) 사본 소실 → 「꽃톡」 폴더 사본으로 대체" → 관련 조건 SK-01·SK-02·SK-03·SK-06
- 집합형 direction 계산 결과(AM-02, 0.1%p 단위 나열): `relaxing added=101 removed=101` (53.8~63.8% → 67.0~77.0%)
- AM-01 별도 처리: amendment의 "unknown" 라벨을 PASS 근거로 쓰지 않았다. 대신 evaluator가 **직접** sha256 을 계산해
  대체 파일(`.../scratchpad/lessons/creator-original-abs.3mf`)과 `~/Downloads/꽃톡/H2_simple_AMS_Flipper--ABS.3mf` 가
  `8eeeecc00af3fdc08f981fec77090b67d8fe6d34d5a1382a92f1824469c93fa0` 로 완전히 동일한 바이트임을 확인했고, 그 값이
  계약 공통전제가 명시한 바이트 수(8,008,196)와도 일치함을 확인했다. 이 독립 측정(출처: evaluator 직접 수집,
  amendment 서술에 의존하지 않음)을 SK-01/02/03/06 의 근거로 사용했다 — **사용자 확인 필요 항목**으로 아래에 별도 표기.

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/bambu-print-lessons/2026-09.md`)
- unreflected_corrections: 0 (로그 1건은 사용자 발화가 아니라 계약 품질 사전진단 서브에이전트 출력 — 반영 대상 아님. 그 진단 내용은 아래 Improvement Suggestions 에 흡수함)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (8/8)
- [x] SK-01: PASS — 근거: `bambu-kit/skills/bambu-print-profile/SKILL.md:84-111` 3MF 추출 스크립트를 원문 그대로 추출(anchor+body, PY 종료줄 직전까지)해 실행. 제작자 원본(대체 사본, AM-01) 실행 결과 `axis_insert` 경고 줄 1개, v2 완성본(`.../v2/H2_AMS_Flipper_ABS_v2_2_main.3mf`) 실행 결과 0개. 음성 대조: `WARN printable=` 출력 줄을 삭제한 사본으로 재실행 시 경고 0개로 떨어짐 — 판별력 확인. [L3]
- [x] SK-02: PASS — 근거: `SKILL.md:131-335`(anchor "# bambu-kit geometry-class probe") 스크립트를 `WALL_LOOPS=4 OUTER_LINE_WIDTH=0.42 INNER_LINE_WIDTH=0.45` 로 실행. 바닥 0.1mm 부족 비율(`wall_short_share[0]`) — rear_bracket 71.9%(좌우 동일, AM-02 적용 범위 67.0~77.0% 이내) · 80angle_bracket 72.1/72.2%(원 범위 69.5~79.5% 이내) · AMS2_bracket 0.0%(원 범위 0~5% 이내). `_wall_budget_short_share` 요약값 0.907(≥0.5) 1줄 확인. 음성 대조: `WALL_LOOPS=1`(예산 0.84mm) 재실행 시 rear_bracket 바닥 비율이 71.9%→0.0%로 급락 — 판별력 확인. [L3]
- [x] SK-03: PASS — 근거: 같은 스크립트를 `WALL_LOOPS` 없이 제작자 원본에 실행 → 10개 부품 전부 `_geometry_class="planar"`, `wall_budget` 문자열 0회. `origin/main:bambu-kit/skills/bambu-print-profile/SKILL.md`(옛 스크립트, line 116-254)로 같은 방식 추출·실행한 결과와 부품 10개 전부 `_geometry_class` 일치 확인. [L3]
- [x] SK-04: PASS — 근거: `SKILL.md:1418-1649` Phase 4.3 게이트(anchor "TARGET_SLICER=") 원문 추출, `TARGET_SLICER=bambu SKILL_DIR=bambu-kit/skills/bambu-print-profile` 로 `process-wall-budget-classic.json` 실행 → FAIL 줄 정확히 1개(`벽 예산` · `arachne` 포함), exit=1. 음성 대조: 해당 `errs.append` 줄을 `pass` 로 바꾼 사본 실행 시 `RESULT: PASS` exit=0. [L3]
- [x] SK-05: PASS — 근거: (a) `wall_generator` 만 `arachne` 로 바꾼 사본 → exit=0, `벽 예산` FAIL 0개. (b) `_wall_budget_short_share` 키만 지운 사본 → exit=0, `_wall_budget_short_share` 를 포함한 `[미검증]` 줄 정확히 1개. [L3, enumerated 2/2]
- [x] SK-06: PASS — 근거: `SKILL.md:1794-1836`(4.4절 "값 박기" 스크립트) 원문 추출, 제작자 원본(AM-01 대체 사본) + `.../v2/process/H2 AMS Flipper - ABS 0.12mm HQ v2.json` + `.../v2/filament/H2 AMS Flipper - ABS retract 0.6.json` 로 실행해 만든 3mf 를 `Metadata/project_settings.config` 대조 — `_`/META 제외 전 키 값 일치, `print_settings_id`·`filament_settings_id` 도 두 JSON의 `name` 과 일치, 불일치 0건. 음성 대조: 값을 안 박은 제작자 원본 자체를 같은 방식으로 대조하면 불일치 27건. [L3, collective]
- [x] SK-07: PASS — 근거: `SKILL.md:1844-1893`(4.4절 "보낸 G-code 대조" 스크립트) 원문 추출, `$SP/sent-first-print-head.gcode` + `$SP/v1-process.json` 로 실행 → 불일치 키 정확히 `bottom_shell_layers`·`outer_wall_acceleration`·`default_acceleration` 3개, exit=1. 음성 대조: 세 값을 G-code 기록값(5·4000·9000)으로 맞춘 사본 실행 시 불일치 0개 exit=0. [L3, enumerated 3/3]
- [x] SK-08: PASS — 근거: (a) `awk '/^# 4\. 임포트/{s=1;next} /^# 5\./{s=0} s'` 범위(1382-1393줄)에 "설정을 바꾸지 않는다" 1회·"보낸 G-code" 1회. (b) `## Gotcha 체크리스트` 섹션(1968-2010줄, 다음 `## ` 직전까지)에 `printable`·`벽 예산`·`보낸 G-code` 각 1회. (c) `surface-recipes.md` `awk '/^### 2\.8\./{s=1;next} /^## 3\./{s=0} s'` 범위(138-208줄)에 `planar` 3회·`WALL_LOOPS` 1회. [L3, structural enumerated 3/3]

### Script (1/1)
- [x] SC-00: PASS(N/A 명시) — 근거: AR-01 diff 목록에 `scripts/release.sh`·`.claude-plugin/plugin.json`·`marketplace.json` 없음 — 계약이 선언한 대상 제외를 실측으로 재확인. [L3]

### Error (3/3)
- [x] ER-01: PASS — 근거: `process-wall-budget-classic.json` 사본에서 `_wall_budget_short_share`→`"abc"` 로 바꿔 SK-04 게이트 실행 → `Traceback` 0회, `[미검증] ...: _wall_budget_short_share 미기록` 줄 1개 보고(`num("abc")`→None→미검증 분기로 정상 처리, 예외 미발생). [L3]
- [x] ER-02: PASS — 근거: SK-02 스크립트 `WALL_LOOPS=0` 실행 → exit=1, `Traceback` 0, `FAIL: WALL_LOOPS=0 — 벽은 1 겹 이상이어야 한다` 1줄. `WALL_LOOPS=x` 실행 → exit=1, `Traceback` 0, `FAIL: WALL_LOOPS · OUTER_LINE_WIDTH · INNER_LINE_WIDTH 는 숫자여야 한다` 1줄. [L3, enumerated 2/2]
- [x] ER-03: PASS — 근거: 기존 시험 파일 11개를 `origin/main`(line 116-1557 대역 추출) 게이트와 이 브랜치(line 1418-1649 대역 추출) 게이트로 각각 실행 — 11개 전부 FAIL 줄 집합·exit 동일(`process-bambu-only-key-in-orca`=orca, 나머지=bambu). `[미검증]` 줄 수는 새 브랜치가 다수 파일에서 0→1로 늘었으나(계약이 명시적으로 허용한 차이) FAIL 판정 자체는 무변. [L3, enumerated 11/11]

### Architecture (4/4)
- [x] AR-01: PASS — 측정값: `git diff --name-only origin/main...feat/bambu-kit-print-lessons` → 5개 파일(`sprint-amendments-*.md`·`sprint-contract-*.md`·`process-wall-budget-classic.json`·`SKILL.md`·`surface-recipes.md`), 전부 허용 6개 집합의 부분집합 (기준: 부분집합 여부). exit=0. working tree clean, 커밋 완료 확인. [L3]
- [x] AR-02: PASS — 측정값: `.github/workflows/*.yml` 에서 추출한 10개 명령 전부 exit=0 (validate-plugin.py · sync-evals.py --check-only · sync-docs.py --check-only · sync-orchestrator.py --check-only · run-evals.py --verbose(106 passed 0 failed) · check-contrast-claims.py · check-docs-links.py · check-stale-values.py · save-test.sh(ALL TESTS PASSED) · check-docs-a11y.js(177/177 PASS)). [L3, enumerated 10/10]
- [x] AR-03: PASS — 측정값: `git merge-tree --write-tree feat/bambu-kit-orca-h2s-feedback feat/bambu-kit-print-lessons` exit=0 (트리 해시 반환, 충돌 안내 없음). [L3]
- [x] AR-04: PASS — 근거: `bambu-kit/evals/gate-fixtures/process-wall-budget-classic.json` 이 기존 11개 픽스처와 같은 폴더에 위치(ls 확인). SK-04 실행에서 FAIL 정확히 1개(벽 예산 외 위반 0개)로 판정 — SK-04 실행과 동일 측정 재사용. [L3]

### Anti-patterns (2/2)
- [x] AP-01: PASS — 근거: AR-01 diff 목록에 `bambu-kit/.claude-plugin/plugin.json` 없음(측정값: 0회 등장). [L3]
- [x] AP-03: PASS — 근거: `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` 실행 결과 "V6 code-fence 0 bare — OK", exit=0. [L3]

### Reusability (2/2)
- [x] RE-01: PASS — 근거: `git diff --stat origin/main...feat/bambu-kit-print-lessons` 확인 결과 이번 스프린트는 새 독립 컴포넌트를 만들지 않았다(SKILL.md 기존 스크립트 확장·references 문서 보강·JSON 픽스처 1개 추가뿐) — private 은폐 대상 자체가 없음. [L3]
- [x] RE-02: PASS — 근거: SK-02용 벽 예산 계산은 기존 형상 클래스 프로브 스크립트(`SKILL.md:131-335`, 원래 있던 것)를 `WALL_LOOPS` 환경변수 분기로 확장한 것이지 새 스크립트를 병행 작성하지 않았다(diff 확인 — 같은 heredoc 블록 안에 로직 추가). 의도적 재사용 패턴 확인. [L3]

### Diagnostics (2/4 PASS, 2/4 [미검증:ENV])
- [x] DG-01: PASS — 측정값: `bash -n scripts/release.sh` exit=0, 워닝 0개. [L3]
- [ ] DG-02: [미검증:ENV] — IDE diagnostics 연동 도구가 evaluator 툴셋에 없음(mcp__ide 계열 도구 미등록, project.yaml `runtime_inspection.mcp_server: null`). 4요건: (1) 1차 시도 — 이 세션 도구 목록에 IDE 진단 도구 자체가 없어 호출 불가(도구 부재, 실패 출력 아님) (2) fallback — `validate-plugin.py`(V1~V8 전체 OK) · `bash -n` · JSON 파싱(SK-06/SK-04 실행에서 전부 `json.loads` 성공) · `check-docs-links.py`(깨진 링크 0) 로 정적 대체 수행 (3) 실패 로그 — 해당 없음(도구 미등록) (4) 통제 불가 사유 — evaluator 에이전트 tool 목록에 IDE 커넥터가 등록되어 있지 않음. 재검증 명령: IDE MCP 서버 연결 후 `mcp__ide__getDiagnostics` 재실행.
- [x] DG-03: PASS — 측정값: `bash scripts/release.sh 2>&1 || true`(인자 없음) → 사용법 안내 출력만(에러/예외 패턴 0건, `diagnostics.console_errors: []` 이므로 매칭 대상 자체가 없음). [L3]
- [ ] DG-04: [미검증:ENV] — 이 스프린트 산출물에 구동 가능한 앱/서버가 없음(project.yaml `runtime_inspection.launch_script: null`, stack: shell-scripts). 4요건: (1) 1차 시도 — launch_script 미설정으로 실행 대상 자체 없음 (2) fallback — 범위 경계 절이 "실제 출력 효과 측정은 범위 밖" 이라 명시, AR-02 CI 10종 전부 통과로 정적 측면 대체 확인 (3) 실패 로그 — 해당 없음(대상 부재) (4) 통제 불가 사유 — 이 프로젝트 타입(shell-scripts, 문서/스킬 변경)에는 구동할 앱/서버 컴포넌트가 존재하지 않음. 재검증 명령: 실행 가능 app/server 컴포넌트가 포함된 변경이 생기면 그때 재실행.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 2  [DG-02, DG-04 — 위 4요건 각각 근거란에 기재]
- verified_coverage: (24 - 2) / 24 = 0.92  (임계 0.60)
- 연속 ENV 승급: 없음 (이 슬러그의 첫 평가, iteration 1)
- Verdict 영향: 통상 (자동 REJECT 미해당, 커버리지 게이트 통과)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 24개 조건 중 동시성 가드 · 인증/권한 · 멱등성 · 입력 검증 · 데이터 유실 · 마이그레이션 안전성 · 재시도/중복제거 · 보안 경계 · 사용자 결함 보고 충돌에 해당하는 조건 0개 (기하 측정·설정 파일 검증·문서 검증 범주)

## User-Reported Failures
- 해당 없음 — 이 슬러그의 최초 평가이며 이전 PASS 판정이나 사용자 실패 보고가 없음

## Evidence Validity
- 검사 대상 증거: 22건 (직접 실행/DG-01/DG-03 포함, ENV 2건 제외)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 22건 · 전부 evaluator 가 직접 bash 로 실행해 exit code·stdout 캡처 (zsh 는 사용자 셸이나, 본 평가는 Bash 도구를 통해 bash 로 실행 — 계약 스크립트 자체가 python3/bash 대상이라 zsh 고유 glob 이슈 대상 아님. AR-02 의 `bash harness/evals/kaizen/feedback-system/save-test.sh` 는 스크립트 내부에서 bash 로 실행됨을 확인)
- 무효 0건 — 미검증 카운터에 추가 없음

## Summary
- Total: 24/24 conditions PASS 판정 가능 (22 직접 PASS + 2 [미검증:ENV], invalid_evidence 0)
- Verdict: APPROVE
- 24개 조건 전부 실행 산출물(명령 출력·exit code·음성 대조)로 확인했다. AM-01(입력 파일 경로 교체, direction=unknown)은 amendment 자체를 PASS 근거로 쓰지 않고 evaluator 가 직접 sha256 해시로 파일 동일성을 재확인해 SK-01/02/03/06 의 근거로 삼았다 — 사용자 확인 항목으로 아래에 남긴다. AM-02(rear_bracket 범위 완화, direction=relaxing·consent=anchored)는 규칙상 PASS 근거로 바로 사용 가능해 그대로 적용했다.

## 사용자 확인 필요
- AM-01 은 형식상 `unknown` 방향이라 amendment 자체만으로는 PASS 근거가 되지 않는다. 다만 evaluator 가 독립적으로 대체 파일과 `~/Downloads/꽃톡/H2_simple_AMS_Flipper--ABS.3mf` 의 sha256 이 완전히 동일함(`8eeeecc0...`)을 확인했고, 계약이 명시한 바이트 수(8,008,196)와도 일치해 이를 SK-01/02/03/06 의 근거로 채택했다. 이 판단에 동의하는지 확인 바란다.

## Improvement Suggestions
- [SK-02] 범위-미명시 — 음성 대조 기준이 "크게 떨어져야 한다" 로만 적혀 있다. `WALL_LOOPS=1(예산 0.84mm)일 때 rear_bracket 바닥 비율이 X%p 이하로 떨어진다` 처럼 구체 임계값을 명시해라 (evaluator 실측: 71.9% → 0.0%, 이 경계로 못박을 수 있다).
- [SK-08(b)] 검증경로-미기재 — (a)(c)는 awk 범위식이 있는데 (b) "Gotcha 체크리스트 섹션"만 추출 범위 스크립트가 없다. `awk '/^## Gotcha 체크리스트/{s=1;next} /^## /{s=0} s'` 처럼 명시해라.
- [ER-01] 검증경로-미기재 — Then 절 두번째 요구("[미검증] 또는 FAIL 줄로 보고된다")의 측정 방법이 없다. `grep -c '_wall_budget_short_share'` 같은 구체 명령을 측정란에 추가해라.
- [AR-04] 측정-중복 — "벽 예산 외 위반 0개" 부분이 SK-04 의 "FAIL 정확히 1개"와 같은 측정을 재사용한다. 의도된 재사용이면 계약에 "SK-04 결과를 그대로 쓴다" 라고 명시해 평가자가 별도 측정을 시도하지 않게 해라.
- [DG-01, DG-03] 측정-환경-오염 — `commands.analyze`/`commands.test` 가 이 스프린트가 건드리지 않는 `scripts/release.sh` 를 대상으로 한다. project.yaml 의 analyze/test 명령이 SKILL.md 임베디드 스크립트나 JSON 픽스처를 검사하지 못해 판별력이 없다. bambu-kit 전용 명령(예: 임베디드 python 조각 `python3 -m py_compile` 등)을 project.yaml 에 추가하는 걸 검토해라.
- [DG-04] 태그-산출물-불일치 — SC-00 처럼 명시적으로 N/A 표시가 없어 "빈 통과" 로 보일 여지가 있다. app/server 가 없는 스프린트는 SC-00 패턴을 따라 조건 자체에 "N/A: 이 스프린트는 구동 가능한 앱/서버가 없다" 를 명시해라.
- [RE-01, RE-02] 범위-미명시 — 이번 스프린트 산출물(SKILL.md 임베디드 스크립트, references 문서, JSON 픽스처) 중 무엇이 "컴포넌트" 로 간주되는지 불명확하다. 복잡도가 낮은 문서/설정 전용 스프린트에서는 RE-01/02 를 "해당 없음" 으로 명시하거나 대상 아티팩트를 조건에 열거해라.
