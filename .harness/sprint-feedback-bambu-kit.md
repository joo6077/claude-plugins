# Sprint Feedback
Feature: bambu-kit 표면 품질 회귀 수정
Evaluated: 2026-09-05 22:40
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-bambu-kit.md
- sha256: a47df30fc0a9cc30e6b5fcf80ffa45bed50ca90d2c79a1a5b32c3bcd2d4afca6
- status: active
- slug: bambu-kit
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 인자로 계약 경로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT status=active — active 유지, 재작업 대상)

## Amendments
- amendments: 0 (사이드카 파일 없음 — `.harness/sprint-amendments-bambu-kit.md` 부재)

## User Correction Audit
- correction_log_status: 조회 생략 (독립 QA 평가 태스크로 위임되어 reflect-kit 로그 경로 미접근. 표면화 전용 단계이며 verdict 에 영향 없음)
- unreflected_corrections: 0 (조회 생략)

## Results

### Skill (5/5)
- [x] SK-01: Phase 3 튜닝 허용 키 목록에 5키 존재 — PASS
  - 근거: `SKILL.md:714-715` — `internal_solid_infill_speed`, `sparse_infill_speed`, `gap_infill_speed` (line 714, ✅ 블록), `outer_wall_acceleration`, `default_acceleration` (line 715, ✅ 블록). 5키 전부 grep 확인, 모두 ✅ 로 시작하는 허용 목록 블록 내부. [L3, exact-enumerated]
- [x] SK-02: 유량비 게이트 산식 + 3단계 임계 — PASS
  - 근거: `SKILL.md:730` `Q = line_width x layer_height x speed x flow_ratio`. `SKILL.md:736-738` 3단계 표(`<=3x` 통과 / `3x~5x` 경고 / `>5x` FAIL). `flow_ratio` grep count=3. [L3, exact]
- [x] SK-03: filament 부모값 조회 절차 + nil-fallback 금지 — PASS
  - 근거: `SKILL.md:789-811` "filament 부모값 조회" 문단 (조회 명령 + 실측 결과 인용). `SKILL.md:807-808` "machine ... 0.8 / 2 와 다르다 ... 그것을 소재값으로 쓰면 안 된다" (금지 문구). [L3, structural]
- [x] SK-04: "JSON 변경 없이" 0건 + 관측 신호 기반 분기 대체 — PASS
  - 근거: `grep -c "JSON 변경 없이" SKILL.md` = 0, `references/failure-recipes.md` = 0 (측정값 0/0, 기준 ==0 충족). 대체: `SKILL.md:766-779` L2 게이트가 (a)~(d) 관측 신호 분기로 재구성, `failure-recipes.md` §2.1 동일 분기 존재. [L3, exact-enumerated]
- [x] SK-05: user-preferences.md 신규 + 참조 + 목표/수단 구분 — PASS
  - 근거: `references/user-preferences.md` 파일 존재 확인(L1). `SKILL.md:815`가 경로 참조. `user-preferences.md:21-33` "저장하는 것은 목표(품질)이고 속도는 수단이다... 즉 느림은 목표가 아니다" (저속을 목표로 저장하지 않는다는 문장 확인). [L3, exact]

### Script (4/4)
- [x] SC-01: Phase 4.3 게이트 유량비 검사 양성/음성 대조 — PASS
  - 근거(실행 산출물): SKILL.md:1009-1127 게이트 스크립트를 추출해 실제 실행. 실측 불량 프로파일(`opus-xero-rear-desiccant-ams2pro.zip`)에 실행 → `FAIL ...json: 유량비 8.3x (gap_infill_speed) — 5x 초과` (exit 1). 수동 교정 프로파일(≤3x)에 실행 → `RESULT: PASS` (exit 0). 음성 대조: 유량비 검사 블록(`if who: ...worst>5.0`)을 제거하고 재실행 → 동일 프로파일이 `OK`(통과)로 전환 확인 (`gate_no_flow.py` 실행 결과). [L3, goal — Discriminating Evidence 확인 완료: 결합 O · 음성 대조 실행 확인]
- [x] SC-02: Phase 4.3 게이트 filament 부모값 이탈 검사 — PASS
  - 근거(실행 산출물): 동일 불량 프로파일 filament JSON(`filament_retraction_length=0.8`, 부모 `Bambu ABS @BBL H2S`=0.4) 실행 → `FAIL ...: filament_retraction_length=0.8 가 소재 부모값 0.4 의 1.5 배 초과`. 음성 대조: `GUARDED` 이탈 검사 루프를 제거하고 재실행 → 동일 파일이 `OK`(통과)로 전환 확인 (`gate_no_parent.py`). [L3, goal — Discriminating Evidence 확인 완료]
- [x] SC-03: `python3 scripts/validate-plugin.py bambu-kit` exit 0 — PASS
  - 근거(실행 산출물): 실제 실행 결과 `Total: 1 plugins, 1 OK` / `Exit: 0`. V1~V8 전 항목 OK/SKIP. [L3, goal]
- [x] SC-04: 회귀 게이트 — 재생성 전/후 유량비 비교, after ≤3x — PASS
  - 근거(실행 산출물): BEFORE(원본 불량 process JSON, 부모 체인 해석) 유량비 `8.333x` (gap_infill_speed). AFTER(수정된 SK-01 5키를 surface-recipes.md §3 권장 착지값으로 반영해 수동 재생성) 유량비 `2.83x`(sparse_infill_speed, `line_width` 부모 해석 반영). before>after, after≤3x 충족. 음성 대조: AFTER 에서 SK-01 추가 키(6개) 를 제거(되돌림) → 유량비 `8.3x` 로 BEFORE 와 동일하게 복원됨을 실측 확인. [L3, goal — Discriminating Evidence 확인 완료]
  - 주의: 회귀 게이트 서술 섹션은 "스킬 실행 검증(DG-04)을 먼저 통과한 뒤 수행한다"고 명시하나, DG-04가 FAIL(미실행)이므로 이 SC-04 재생성은 계약이 지정한 순서를 어기고 evaluator가 독립적으로(SK-01 정책을 손으로 적용해) 수행한 것이다. SC-04 자체의 측정 결과는 유효하나, 회귀 게이트의 절차 전제(DG-04 선행)는 위반 상태로 남아 있음.

### Error (3/3)
- [x] ER-01: 건조 미확인=confidence cap, 종료 분기 0건 — PASS
  - 근거: `SKILL.md:777` "건조 미확인은 진단 중단 사유가 아니다 — confidence cap 이다." `grep -c "종료" SKILL.md` = 0, `grep -c "중단" SKILL.md` = 1 (해당 1건이 바로 이 금지 문구 자신). [L3, structural]
- [x] ER-02: 부모 조회 실패 시 폴백(추측 금지) — PASS
  - 근거: `SKILL.md:810-811` "조회에 실패하면(시스템 프로파일 경로 없음 등) 추측값을 쓰지 말고 해당 filament 키를 아예 생략하고 [미검증]으로 보고한다." [L3, structural]
- [x] ER-03: 유량비 FAIL 시 조용히 통과 금지 + 사용자 제시 경로 — PASS
  - 근거: `SKILL.md:738` "`> 5x` FAIL ... 조용히 통과시키지 마라." `SKILL.md:1007` "생성한 JSON 전부에 대해 아래를 실행하고, 출력 원문을 응답에 붙여라" — 유량비 FAIL 라인을 포함한 게이트 전체 출력이 응답(사용자 노출 경로)에 그대로 포함되도록 강제. [L3, structural — 두 문장의 결합으로 "조용히 통과 금지 + 사용자 제시" 충족. 유량비 전용 문장 하나에 두 요소가 응집되어 있지 않아 [structural] 태그 기준 다소 약하나 요건은 충족]

### Architecture (2/4)
- [x] AR-01: outer_wall_speed 문서 간 충돌 해소 — PASS (조건부, 잔여 모호점 있음)
  - 근거: surface-recipes.md:118 이 소재별 매트릭스(PLA 25-40·Silk 15-25·PETG 50-70·PA/PC 20-30·ABS/ASA 25-35·TPU 10-20)를 SSOT로 선언(`surface-recipes.md:107` "이 표가 속도·가속 값의 정본(SSOT)이다"). seam-recipes.md 의 소재별 표(§4, PETG/ABS/ASA/PC/PA-CF 행)는 절대 속도값을 제거하고 "속도는 surface-recipes.md §3 표가 정본"으로 교체됨(`seam-recipes.md:139-143`) — 배경에 명시된 원 충돌("seam-recipes.md:117 PETG outer 50-70" vs "SKILL.md:804 outer 20-40")은 양쪽 다 해소 확인. 재질명이 태그된 outer_wall_speed 쌍 중 값이 다른 쌍 0건.
  - [미검증 아님 — 단, 개선사항 기재] `seam-recipes.md:123` "회전체/원기둥, 컵, 화병" 행에 재질 미태그 "outer wall 60-80 mm/s" 잔존 (0.2mm layer 기준 baseline 표, surface-first 표와는 별개 컨텍스트로 보이나 SSOT 참조/적용조건 명시가 없음). 계약 측정문(같은 소재 쌍)의 문자 그대로는 위반이 아니라고 판단했으나, 조건의 상위 취지("단일 SSOT 참조 또는 적용조건 명시")는 완전히 충족되지 않음. [L3, exact-enumerated]
- [ ] AR-02: seam_slope_gap 기본값 0 환원 + seam_gap 과 구분 — **FAIL**
  - 근거: `seam-recipes.md:92-107` §2.1 "seam_slope_gap 과 seam_gap 은 다른 키다" 신설 문단 존재, 대부분의 gap 값이 `0`으로 교정됨(line 32,41,86,123,125,127,128,160 등). 그러나 **`seam-recipes.md:124`** "원통 '선 최대한 안 보이게'" 행이 여전히 `검증 조합: Contour and Hole, 0 mm/0%, **10%**, 20 mm, 10 steps, around entire wall Off` 로 gap 값 `10%` 를 그대로 방치. 바로 위(123행) · 아래(125행) 형제 행은 모두 `gap 0` 으로 교정되었는데 이 행만 누락됨 (sibling consistency 위반). 측정: "gap 권장값 10%를 기본으로 처방하는 행" = 1건(기준 0건).
  - 수정: `seam-recipes.md:124` 의 `10%` 를 `0` 으로 교정.
- [x] AR-03: resolution 0.006-0.010 / enable_arc_fitting 끄기 권장 — surface-first 공통값에서 0건 — PASS
  - 근거: `SKILL.md:871-878` (외벽 표면 공통 섹션)에 `resolution 0.006-0.010` 문자열 0건, 오히려 `SKILL.md:876` "resolution 하향과 enable_arc_fitting 끄기는 surface-first 공통값이 아니다"로 명시적 배제. `SKILL.md:720` 도 "enable_arc_fitting — 기본값 유지... 곡면 계단 대응 카드로 제시하지 마라"로 끄기 권장 없음. 전체 파일에서 `resolution 0.006-0.010` 은 `SKILL.md:577`(Phase 3.0 Supportability Split, 실패모드 사후 대응 표, "surface-first 공통값" 섹션과 무관한 별개 컨텍스트) 1건 잔존 — 조건 조건문이 명시한 "surface-first 공통값" 범위에는 포함되지 않음. [L3, exact — 측정 범위(전체파일 vs 특정 섹션) 모호 플래그 기록]
- [x] AR-04: 변경 범위 6파일 이내, 그 밖 0건 — PASS
  - 근거(측정값 우선 출력): `git diff --stat -- bambu-kit/` = 4개 파일(SKILL.md, failure-recipes.md, seam-recipes.md, surface-recipes.md), 그 밖 0건 — 단 이 명령은 untracked(신규) 파일을 구조적으로 못 잡음. 보완: `git status --porcelain -- bambu-kit/` 로 대조 → `?? .../user-preferences.md` 1건 추가 확인. 합산 총 5개 파일, 전부 계약이 허용한 6개 이내(bambu-fields-baseline.md 는 미변경, 허용범위 내 0건 사용), 허용 목록 밖 경로 0건. [L3, exact-enumerated]
  - 계약 개선 제안: 측정 명령이 `git diff --stat` 단독이라 신규(untracked) 파일을 못 잡는 Diff-Scope Oracle 결함. `git status --porcelain` 병기 권장.

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS
  - 근거: `python3 scripts/validate-plugin.py bambu-kit` 실행 결과 `V6 code-fence  0 bare — OK`. (단순 `grep -cE '^```\s*$'` 는 닫는 펜스까지 함께 세어 공허한 카운트가 되므로 validate-plugin.py 의 언어-힌트 인식 로직을 정본으로 채택.) [L3]
- [x] AP-04: SKILL.md frontmatter name 필드 유지 — PASS
  - 근거: `SKILL.md:2` `name: bambu-print-profile`. `validate-plugin.py` 결과 `V1 frontmatter  1 skill — OK`. [L3]

### Reusability (1/2)
- [ ] RE-01: 수치 정본을 references/ 에 두고 SKILL.md 중복 기재 금지 — **FAIL**
  - 근거: `SKILL.md:744` "권장 착지값 (outer 30 mm/s 기준): inner `60-90` · internal_solid `70-120` · gap `30-70`." 이 값은 `surface-recipes.md:119` (`outer 30 → inner 60-90`), `surface-recipes.md:120` (`outer 30 기준 70-120mm/s`), `surface-recipes.md:122` (`30-70mm/s, 최대 80`) 와 완전히 동일한 수치의 재기재다. `surface-recipes.md:107` 자신이 "이 표가 속도·가속 값의 정본(SSOT)이다... 두 문서에 같은 소재의 속도 범위를 따로 적지 마라" 라고 선언했음에도 SKILL.md 가 같은 수치를 그대로 복제했다. (반면 `SKILL.md:874` 는 올바르게 "§유량비 게이트 + surface-recipes.md §3 표 참조" 로 참조만 한다 — 같은 파일 안에서 참조 방식과 복제 방식이 혼재.)
  - 수정: `SKILL.md:744` 를 구체 수치 대신 "권장 착지값은 `surface-recipes.md` §3 표를 따른다" 로 교체.
- [x] RE-02: 기존 references 파일 확장(신규 생성 지양) — PASS
  - 근거: `git diff --stat` 상 `failure-recipes.md`/`seam-recipes.md`/`surface-recipes.md` 3개는 모두 `M`(수정, 섹션 확장)이며 재생성이 아님. 신규 파일은 `user-preferences.md` 1건뿐이며 이는 SK-05가 명시적으로 요구하는 별도 조건의 산출물(기존 3파일 중 어디에도 속하지 않는 신규 기능 영역)로, RE-02의 "불필요한 신규 파일 지양" 취지와 충돌하지 않는다고 판단. [L3]
  - 계약 개선 제안: RE-02와 SK-05가 문면상 긴장 관계(하나는 신규 파일 금지, 하나는 신규 파일 요구)에 있음 — RE-02에 "단, 다른 조건이 명시적으로 신규 파일을 요구하는 경우는 예외" 카브아웃 명시 권장.

### Diagnostics (2/4, 1 미검증:ENV)
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS
  - 근거: 실행 결과 `EXIT=0`, 출력 없음(구문 오류 0건). [L3]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — **[미검증:ENV]**
  - 근거(4요건): (1) 1차 도구 시도 — `which markdownlint markdownlint-cli2` 실행 → `not found` (실패 출력 인용). (2) fallback 시도 — `.markdownlint*` 설정 파일 탐색(`no matches found`), `project.yaml.runtime_inspection.mcp_server: null` 확인(IDE MCP 미설정, 계약에 fallback 절차 자체가 없음 — 계약 결함으로 기록). (3) 실패 로그 — 위 명령 stderr/출력 그대로 인용됨. (4) 통제 불가 사유 — 이 evaluator는 CLI 환경이며 IDE Problems 패널에 접근할 도구가 전혀 설치되어 있지 않음(구현자가 통제할 수 없는 환경 제약). 재검증 명령: VSCode 등 IDE로 변경 5개 파일(SKILL.md, failure/seam/surface-recipes.md, user-preferences.md)을 열어 Problems 패널 0건 확인.
  - Improvement: `[DG-02] 검증경로-미기재 — project.yaml 에 markdown lint 도구(markdownlint-cli2 등) 또는 IDE MCP 바인딩을 명시하거나, DG-02 조건에 "N/A (마크다운 전용 킷)" 카브아웃 권장`
- [x] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 에러/예외 0개 — PASS
  - 근거: 실행 결과 사용법 안내 + 플러그인 목록만 출력(`bambu-kit` 포함), 에러/예외/트레이스백 0건, exit 0. [L3]
- [ ] DG-04: 수정된 스킬 실제 1회 실행(process+filament JSON 생성) 에러 0개 — **FAIL**
  - 근거: 구현자 자가 보고와 독립 확인 결과 일치 — Phase 1~4 전체(모델 컨텍스트 추출 → 소재 추천 → JSON 생성 → Completion Evidence Gate)를 실제로 1회 실행한 산출물(신규 생성된 process/filament JSON, 새 notes.md 등)이 존재하지 않는다. `/Users/jackson/Hub/60_3D Print/Settings/` 하위 디렉토리 중 이 세션 시각대(2026-09-05)에 새로 생성된 모델 폴더 없음(가장 최근 `opus-xero-rear-desiccant-box-ams2pro` 는 사전 존재하던 버그 재현용 zip이며 mtime 16:30, 이는 회귀 조사용 기존 산출물이지 "수정된 스킬"의 신규 실행 결과가 아님).
  - SC-01/SC-02/SC-04 에서 수행한 Phase 4.3 게이트 스크립트의 독립 실행 및 수동 JSON 패치는 **완전한 스킬 워크플로우(Phase 1~3의 대화형 판단 경로)를 대체하지 못한다** — 별도 축의 증거이며 DG-04 를 대신할 수 없다 (엄격도 규칙 9: 실행 주장 조건은 산출물 요구, 대체 불가). 계획적 이연(구현자가 "미충족"으로 명시 보고)이므로 도구·환경 부재가 아니라 **의도적 미실행 = FAIL**.
  - 수정: 실제 MakerWorld URL 또는 로컬 모델 파일로 스킬을 1회 완주해 새 process+filament JSON을 생성하고, Phase 4.3 게이트 출력(RESULT: PASS, exit 0)을 응답에 첨부해야 함.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02 — 1차 시도: markdownlint/markdownlint-cli2 not found · fallback 시도: .markdownlint 설정 부재 + mcp_server null 확인(계약에 fallback 미기술) · 실패 로그: 명령 출력 인용 · 통제 불가 사유: CLI 환경에 IDE 도구 자체 부재 + 재검증 명령 제시]
- verified_coverage: (24 - 1) / 24 = 0.958 (임계 0.60 충족)
- 연속 ENV 승급: 해당 없음 (이번이 1st iteration)
- Verdict 영향: 통상 (env_gaps 1건은 자동 REJECT 카운터에 비합산. 커버리지 게이트도 충족되므로 REJECT 사유는 전적으로 AR-02/RE-01/DG-04 3건의 FAIL)

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-01, SC-02, SC-04 (테스트/실행 산출물 기반 판정이며 "동시성 가드/입력검증/재시도" 류는 아니지만, "실측 실패 재현·수정" 성격상 판별력 확인이 계약에 음성 대조로 명시되어 있어 그대로 수행)
- 결합 확인: SC-01/SC-02 — Phase 4.3 게이트 스크립트를 SKILL.md 원문에서 그대로 추출해 실행(구현과 직접 결합, 별도 재작성 없음)
- 음성 대조: SC-01 — 계약 기재 있음 · 유량비 검사 블록 제거 시 FAIL→PASS 전환 확인(무력화 시 실제로 통과 확인). SC-02 — 계약 기재 있음 · GUARDED 검사 제거 시 FAIL→PASS 전환 확인. SC-04 — 계약 기재 있음 · SK-01 키 복원(되돌림) 시 after=before(8.3x) 복원 확인

## Evidence Validity
- 검사 대상 증거: 24건 (조건별 1건씩)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 8건(Phase 4.3 게이트 3variant, validate-plugin.py, release.sh 2회, bash -n, grep 다수) · zsh/bash 양쪽 확인 0건(모든 명령을 evaluator 셸(zsh)에서 직접 실행 — bash 전용 문법 없음 확인) · 미실행 0건
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 20/24 conditions passed (FAIL 3: AR-02, RE-01, DG-04 / 미검증:ENV 1: DG-02)
- Verdict: REJECT
- 수정 우선순위:
  1. **DG-04** (최우선) — 수정된 스킬을 실제 MakerWorld/로컬 모델로 1회 완주 실행하고 Phase 4.3 게이트 원문 출력을 첨부. 이것 없이는 "회귀가 실제로 고쳐졌다"는 최종 증거가 없음.
  2. **AR-02** — `seam-recipes.md:124` 의 잔존 `10%` gap 값을 `0`으로 교정 (형제 행과의 일관성 위반, 사소해 보이지만 계약이 정확히 겨냥한 결함 유형).
  3. **RE-01** — `SKILL.md:744` 의 중복 수치를 `surface-recipes.md` §3 참조로 교체.

## Improvement Suggestions
- [AR-04] 측정-경로-부재 — `git diff --stat -- bambu-kit/` 는 untracked 신규 파일을 구조적으로 못 잡는다. 측정 명령에 `git status --porcelain -- bambu-kit/` 병기 권장 (Diff-Scope Oracle 4요소 중 "생성물 제외/포함 pathspec" 재검토).
- [AR-01] 측정-상태-모호 — "outer wall 60-80mm/s"(seam-recipes.md:123, 재질 미태그)가 surface-recipes.md 의 SSOT 선언과 공존해 실무 적용 시 혼선 소지. 재질 태그 없는 shape 기반 속도값도 조건의 "단일 SSOT 참조 또는 적용조건 명시" 대상에 포함되도록 조건문 구체화 권장.
- [DG-02] 검증경로-미기재 — 마크다운 전용 킷에 대한 IDE/lint 도구 바인딩이 project.yaml에 없음. markdownlint-cli2 등의 도구명 명시 또는 DG-02에 "N/A (문서 전용 변경)" 카브아웃 권장.
- [RE-02] 조건-충돌 — RE-02(신규 참조파일 생성 지양)와 SK-05(신규 참조파일 생성 요구)가 문면상 충돌. RE-02에 "다른 조건이 명시적으로 요구하는 신규 파일은 예외" 명시 권장.
- [회귀 게이트 서술] 절차-위반 — 계약의 "회귀 게이트" 서술이 "DG-04 통과 후 SC-04 수행"을 명시하나 실제로는 DG-04 FAIL 상태에서 SC-04가 (evaluator에 의해 독립적으로) 수행됨. 다음 iteration에서는 DG-04 선행 통과 후 SC-04를 구현자가 직접 재수행할 것을 권장.
