# Sprint Feedback
Feature: bambu-kit seam 정책 전환 + 실물 기준 버전·값 검증
Evaluated: 2026-09-05 23:55
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-bambu-seam-policy.md
- sha256: 10fb06e6608eb97845ff71278a4c7d80c809a87b592350b7b0a70a995571e242
- status: active
- slug: bambu-seam-policy
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (launching agent 가 절대경로 지정, 존재 확인 완료; session_id 도 owner_session 과 일치해 ladder 2 로도 동일 결과)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (FINGERPRINT OK)
- status_transition: skipped (verdict=REJECT — active 유지)

## Amendments
- amendments: 0 (사이드카 `sprint-amendments-bambu-seam-policy.md` 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (23:04~23:48 세션 80e6651a... 구간 프롬프트 검토 — 앱 업그레이드/타임랩스 토글 등은 계약 조건과 무관, seam/scarf 정책 관련 미반영 교정 없음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (8/8)
- [x] SK-01: 회전체 결정 트리 재작성, random 이 default top 아님 — PASS
  - 근거: `references/seam-recipes.md:13-58` §0 v4 트리 (1)vase→(2)painted→(3)aligned+scarf→(4)random fallback. `references/surface-recipes.md:40-56` §2.1 도 "(4) random → fallback 전용. surface-first default 아님". 측정 범위(§0, §2.1) 내 "random ... DEFAULT" 표기 0건 확인(L3, Grep+Read)
  - 참고(FAIL 아님): `references/seam-recipes.md:246` (구 "Real-world findings" 아카이브 섹션, §0 밖)에 "default = seam_position: random" 잔존 — 측정 범위 밖이라 조건 자체엔 영향 없으나 내용 상충. Improvement 참조
- [x] SK-02: spiral_mode 3키 표 존재 — PASS
  - 근거: `references/bambu-fields-baseline.md:218-220` 표에 `spiral_mode`/`spiral_mode_smooth`/`spiral_mode_max_xy_smoothing` 각 1행, 이름/타입/기본값/출처 모두 존재 (grep -c 각 1, L2/L3)
- [x] SK-03: H2S timelapse 경고 + issue 번호 + 프로파일 해결 불가 — PASS
  - 근거: `SKILL.md:830` `9166` 1건, `SKILL.md:832` "이것은 프로파일로 고칠 수 없다." 1건 (L3)
- [x] SK-04: vase 판정 체크리스트 + 폴백 경고 — PASS
  - 근거: `SKILL.md:812-819` 7개 항목(>=5), `SKILL.md:809,821` 조용한 폴백 경고 (L3)
- [x] SK-05: scarf 상한 비율 + mm 하한 같은 문단 — PASS
  - 근거: `references/seam-recipes.md:127-148` §2.2, 식 `clamp(min(10mm, 둘레x0.10~0.15), 하한 3mm)` 동일 문단 (L3)
- [x] SK-06: seam_slope_min_length "필터" 서술 0건(부정문 제외) — PASS
  - 근거: `SKILL.md`+`references/` 전체 grep "필터" 1건 검색됨, `references/seam-recipes.md:129` "**최소 길이 필터가 아니다**" 뿐 — 긍정 서술 0건 (L3)
- [x] SK-07: 12소재 seam 전략 표 — PASS
  - 근거: `references/seam-recipes.md:165-186` §4, PLA Basic·Matte·Silk·CF/PETG HF·Basic/ABS/ASA/PC/PAHT-CF/PA6-CF/TPU 12행 전부 확인(enumerated 전수, L3)
- [x] SK-08: wall_sequence inner-outer-inner ↔ wall_loops>=3 전제 — PASS
  - 근거: `references/surface-recipes.md:115` "`inner-outer-inner wall` 은 `wall_loops >= 3` 을 전제한다 ... 쓰지 마라" (L3)

### Script (4/4)
- [x] SC-01: 설치본 버전 실시간 조회 — PASS [실행검증]
  - 근거: `SKILL.md:729-788` ENVPY 블록을 그대로 추출·실행. 음성 대조(현재 설치본): 앱 `02.08.02.61` / 번들 `02.08.00.06` 정확 출력, RESULT: PASS, exit 0. 잘못된 경로로 SYS 교체 시 값 대신 실패 보고 확인("프로파일 번들 버전 조회 실패...", RESULT: FAIL, exit 1)
  - [contract_ambiguity 플래그] 조건 본문의 리터럴 측정값("02.06.00.51"/"02.06.00.05")은 계약 작성 시점(23:03) 기준 구버전이며, 같은 세션에서 23:04~23:13 사이 사용자가 brew 로 앱을 업그레이드해 현재 실치본은 02.08.02.61/02.08.00.06 이다(배경 §9행도 이를 인정: "2026-09-05 확인: 앱 02.08.02.61..."). [goal] 태그의 의미 검증(진짜 실시간 조회 여부)으로 판정 — 상태 전제 미명시(Binary Decidability 규칙 6) → Improvement 로 하향 기록, FAIL 처리하지 않음
- [x] SC-02: 손상 프리셋 탐지 — PASS [실행검증]
  - 근거: 시스템 프로파일 전체를 스크래치패드로 복사(`/private/tmp/.../scratchpad/qa-bambu/system`) 후 `Bambu Lab H2S 0.4 nozzle.json` 의 `nozzle_volume` 을 `["32","32","32"]` 로만 변조. 스크립트의 SYS 경로만 사본으로 교체 실행 → "이상 nozzle_volume 32.0 ... FAIL nozzle_volume=32.0 이 상식 범위 [80,400] 밖", RESULT: FAIL, exit 1. 정상값(145.0)에서는 RESULT: PASS. 실제 설치본은 조작하지 않음(조작 전/후 원본 파일 값 145/148/148 유지 확인)
- [x] SC-03: Phase 4.3 scarf 길이/둘레 비율 게이트 — PASS [실행검증, discriminating]
  - 근거: `SKILL.md:1126-1256` 블록을 그대로 추출해 `gate43.py` 로 저장, 테스트 process JSON 2건 실행. `seam_slope_min_length=8, _scarf_loop_circumference_mm=32.0` → `FAIL test.json: scarf 길이 8.0mm 가 루프 둘레 32.0mm 의 25% — 상한 15% 초과 (seam-recipes.md §2.2)`, exit 1. `=3, C=32.0` → `OK ... RESULT: PASS`, exit 0. 음성 대조: 해당 검사 블록만 제거한 `gate43_noscarf.py` 로 8mm 케이스 재실행 → `RESULT: PASS`(exit 0)로 뒤집힘 — 가드가 실제로 load-bearing임을 확인. 회귀 확인: 기존 유량비 게이트(6.2x 입력 → FAIL) 및 filament 부모값 이탈 게이트(2.0 vs 부모 0.4*1.5 → FAIL) 모두 정상 생존
- [x] SC-04: validate-plugin.py bambu-kit exit 0 — PASS [실행검증]
  - 근거: `python3 scripts/validate-plugin.py bambu-kit` 실행 → V1~V8 전부 OK/SKIP, "Exit: 0", `echo $?` == 0

### Error (3/3)
- [x] ER-01: 버전 조회 실패 시 동작(추측 금지) — PASS
  - 근거: `SKILL.md:790-792` "추측값을 쓰지 마라. `[미검증]`으로 표시하고..." (L3)
- [x] ER-02: vase 불확실 시 조용히 켜지 않고 사용자 제시 — PASS
  - 근거: `SKILL.md:821-822` "판정이 불확실하면 켜지 마라 ... 애매하면 (2) painted 분기를 제안하고 사용자에게 형상 판단을 물어라" (L3)
- [x] ER-03: 손상 프리셋 탐지 시 생성 중단 + 보고 — PASS
  - 근거: `SKILL.md:794-798` "프리셋 온전성 검사가 FAIL 이면 프로파일 생성을 진행하지 마라" (L3)

### Architecture (4/4)
- [x] AR-01: 5개 references 헤더가 런타임 조회를 가리킴 — PASS (enumerated 5/5)
  - 근거: bambu-fields-baseline.md:5, surface-recipes.md:5, seam-recipes.md:5, materials.md:5, failure-recipes.md:5 전부 "런타임에 조회한다 — 이 줄에 버전을 하드코딩하지 마라." + 조회 절차 안내 (L3)
- [x] AR-02: spiral_mode 근거 라인 인용 정정 — PASS
  - 근거: `references/bambu-fields-baseline.md` 에서 "277-282" 0건 (grep 결과 없음). 현재 인용은 "PrintConfig.cpp:5280-5286"(218행) (L3)
- [x] AR-03: seam_gap 실재 키 + JSON 부재≠키 부재 — PASS
  - 근거: `references/bambu-fields-baseline.md:209` "프로파일 JSON 에 키가 없다고 그 키가 없는 것이 아니다." + `:223` seam_gap 상세 (L3)
- [x] AR-04: 변경 범위 한정 — PASS
  - 측정값: `git status --porcelain -- bambu-kit/` = 7건 (기준: <=8), 전부 `bambu-kit/skills/bambu-print-profile/` 하위, 그 밖 경로 0건

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS
  - 근거: `python3 scripts/validate-plugin.py bambu-kit` → "V6 code-fence 0 bare — OK"
- [x] AP-04: SKILL.md frontmatter name 필드 유지 — PASS
  - 근거: 동일 실행 → "V1 frontmatter 1 skill — OK"

### Reusability (1/2)
- [x] RE-01: 수치 정본 references/ 유지, SKILL.md 중복 기재 없음 — PASS
  - 근거: Phase 4.3 게이트 코드의 `r>0.15`/`L<3` 리터럴은 실행 가능한 게이트 자체에 필요한 값이며 에러 메시지에 "(seam-recipes.md §2.2)" 로 출처를 명시(SKILL.md:1231,1233) — 독립적 프로즈 재서술이 아님. 유량비 3x/5x 는 SKILL.md 가 SSOT이고 surface-recipes.md 가 역참조("§유량비 게이트", surface-recipes.md:102)하는 기존 패턴과 일치
- [ ] RE-02: 기존 references 파일 확장 원칙, 신규 생성 금지 — **FAIL**
  - 근거: `git status --porcelain` 확인 결과 `bambu-kit/skills/bambu-print-profile/references/user-preferences.md` 가 `??`(신규 미추적) 상태. `git log --all -- references/user-preferences.md` 결과 0건 — 과거에 존재한 적이 없는 완전히 새로운 references 파일. 기존 8개 references 파일(bambu-fields-baseline/comment-analysis/failure-recipes/kaizen-sources/materials/seam-recipes/surface-recipes/tolerance) 중 "지속적 사용자 선호" 를 다루는 섹션은 없었음 — 즉 "해당 섹션을 확장" 하지 않고 새 파일을 만들었다. 27개 조건 중 SK/SC/ER/AR 어디에도 "사용자 선호 영속화" 신규 파일을 요구하는 조건이 없어, 계약 범위 밖의 추가 작업이 RE-02 를 정면으로 위반한 것으로 판단
  - 수정: `user-preferences.md` 의 내용을 `seam-recipes.md` §0(seam 정책) 또는 `surface-recipes.md`(Phase 1.8 Surface Intent Gate 관련) 기존 섹션으로 흡수하거나, 이 신규 파일 생성이 정당하다면 사용자 승인을 받아 사이드카 amendment 로 남긴 뒤 RE-02 조건 자체를 조정할 것

### Diagnostics (3/4, 1 env-gap)
- [x] DG-01: bash -n scripts/release.sh 워닝 0개 — PASS
  - 근거: `bash -n scripts/release.sh` exit 0, 출력 없음. (참고: 이번 변경은 전부 마크다운이라 release.sh 자체는 미변경 — project.yaml 의 고정 analyze 명령을 문자 그대로 실행)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — **[미검증:ENV]**
  - 1차 도구 시도: `command -v markdownlint` 및 `npx markdownlint` 시도 → "markdownlint not found" / npm 실행 실패 로그 확보
  - fallback 시도: project.yaml `diagnostics.lint: null` — 대체 린터 미설정(계약/설정 결함)
  - 실패 로그: 위 커맨드 출력 그대로
  - 통제 불가 사유: 이 evaluator 는 에디터 UI/Problems 패널에 접근할 IDE 도구가 없음(runtime_inspection.mcp_server: null). 재검증 명령: VSCode 등에서 `bambu-kit/skills/bambu-print-profile/**/*.md` 를 열어 Problems 패널 확인, 또는 `npm i -g markdownlint-cli && markdownlint bambu-kit/skills/bambu-print-profile/**/*.md`
- [x] DG-03: release.sh 콘솔 로그 에러/예외 0개 — PASS
  - 근거: `bash scripts/release.sh 2>&1` → usage 안내만 출력, 에러/트레이스백 없음
- [x] DG-04: sync-docs.py --check-only 동기화 통과 — PASS
  - 근거: `python3 scripts/sync-docs.py bambu-kit --check-only` → "모든 README가 동기화 상태입니다.", exit 0

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02: 1차 도구 시도(markdownlint 미설치) / fallback 시도(계약에 대체 린터 미설정) / 실패 로그(위 커맨드 출력) / 통제 불가 사유+재검증 명령 기재]
- verified_coverage: (27 - 1) / 27 = 0.96 (임계 0.60 이상 — 커버리지 게이트 통과)
- Verdict 영향: 통상 (env_gaps 는 자동 REJECT 카운터에 미합산). REJECT 사유는 RE-02 FAIL 1건

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-03 (동시성/데이터 유실류는 아니지만 "측정이 구현을 실제로 재는가" 가 계약 자체에 음성 대조로 명시된 케이스)
- 결합 확인: SC-03 — 테스트가 `SKILL.md:1126-1256` 코드 블록을 그대로 추출·실행(로직 독립 재작성 아님). 결합 확인됨
- 음성 대조: SC-03 — 계약에 "음성 대조: 검사 블록을 삭제하면 8mm 입력이 통과한다" 명시되어 있고, 실제로 scarf 검사 블록 제거 후 재실행 → 8mm 케이스가 RESULT: PASS 로 뒤집힘 확인(FAIL 확인 완료, 가드 load-bearing 입증)

## Evidence Validity
- 검사 대상 증거: 27건 (조건별)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: SC-01/SC-02/SC-03 관련 스니펫 전부 실제 python3 실행(zsh 환경) — bash 별도 재검증은 미실시(순수 python3 히어독 스크립트라 zsh/bash 셸 차이의 영향을 받는 구문 없음, glob 미사용)
- 무효 0건 — 미검증 카운터 변동 없음

## Summary
- Total: 26/27 conditions passed (RE-02 FAIL, DG-02 [미검증:ENV])
- Verdict: REJECT
- REJECT 사유: RE-02 — `references/user-preferences.md` 신규 생성이 "기존 references 파일 확장" 원칙을 위반. 수정 우선순위: (1) 해당 콘텐츠를 기존 파일 섹션으로 흡수하거나 사용자 승인 하에 예외로 유지, (2) SC-01 관련 상태 전제 계약 문구 보강(Improvement), (3) DG-02 는 재평가 시 markdownlint 설치 또는 IDE 접근 확보 시도 권장

## Improvement Suggestions
- [SC-01] 측정-상태-모호 — 조건 본문의 리터럴 예시 버전 문자열("02.06.00.51"/"02.06.00.05")을 삭제하고 "Given: 평가 시점의 실제 설치본 값" 같은 상태 전제를 명시할 것. 외부 앱 버전처럼 세션 중 합법적으로 변할 수 있는 값을 리터럴 정답으로 못박으면 다음 iteration 마다 재발한다
- [RE-02] 태그-산출물-불일치 — "이미 존재하는 references 파일을 새로 만들지 않고 해당 섹션을 확장한다" 문구가 bambu-kit 의 다른 스프린트 계약(`sprint-contract-bambu-kit.md:104`)에도 동일하게 보일러플레이트로 재사용되고 있다. "새 파일 생성 자체를 금지"하는 것인지 "이미 존재하는 콘텐츠의 중복 생성만 금지"하는 것인지 문법이 모호하다 — enumerate 된 허용/금지 파일 목록 또는 "신규 references 파일이 필요하면 사전 합의 필요" 식으로 조건을 구체화할 것
- [SK-01] 범위-미명시 — `references/seam-recipes.md:246` (구 "Real-world findings" 아카이브, Finding 1)에 "적용 권장: 회전체 모델에서 default = `seam_position: random`" 잔존. 측정 범위(§0, surface-recipes.md §2.1) 밖이라 FAIL 처리하지 않았으나, v4 정책과 정면 상충하는 잔존 서술이므로 다음 스프린트에서 아카이브 섹션에 "v4 로 대체됨" 표기 또는 삭제 권장
- [DG-01] 측정-중복 — `commands.analyze: "bash -n scripts/release.sh"` 는 마크다운/references 전용 변경에 항상 무관하게 통과하는 고정 명령이다. bambu-kit 처럼 셸 스크립트가 없는 스킬 전용 킷에는 실질적으로 아무 것도 검증하지 못하므로, 스택별 project.yaml 오버라이드(예: markdown lint) 도입을 고려할 것
