# Sprint Feedback
Feature: bambu-kit 옵션 키 판정을 태그 등록부 기준으로 교체
Evaluated: 2026-09-15 17:30
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-bambu-kit-option-key-registry-probe.md
- sha256: 5305680c0aa33b15b387a8cdd68279cef614762d14ed1d6d2abea06f01d4177f
- status: active
- slug: bambu-kit-option-key-registry-probe
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (사용자가 계약 절대경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (재검증: `verify_seal` 직접 실행, recorded=actual=2cae367545296fef)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 시작·종료 시 sha256 동일)
- status_transition: active -> done (APPROVE 확정으로 아래 Step 5.5 절차 실행)

## 재평가 범위 (Iteration 1 → 2)
직전 REJECT 사유는 DG-02(신규 `build-option-list.sh`의 shellcheck SC2206 경고 3건, 26·27·35행)
단 1건이었다. `git status --porcelain -- bambu-kit docs/bambu-kit` 와 파일 mtime을 대조한 결과
Iteration 1 평가 시각(17:10) 이후 변경된 파일은 `bambu-kit/scripts/option-key-probe/build-option-list.sh`
하나뿐이었다 — SKILL.md·bambu-fields-baseline.md·option-keys/*.tsv·docs html·gate-fixtures는 불변.
따라서 이번 평가는 (a) DG-02 수정 확인 (b) 그 수정이 다른 조건(특히 SC-07 재생성 동일성)에
회귀를 일으키지 않았는지 확인 (c) 나머지 32개 조건 전부를 처음부터 다시 직접 실행/측정하는
Rule-by-Rule 전수 재현의 세 갈래로 수행했다. Iteration 1의 판정을 인용하지 않고 33개 조건 전부
독립적으로 재현했다.

## Amendments
- amendments: 4 (AM-01~AM-04, 사이드카 불변 — Iteration 1 이후 추가/수정 없음)
- PASS 근거 가능: 4 (AM-01 relaxing·anchored, AM-02 relaxing(오라클 방향)·anchored, AM-03 narrowing·unanchored, AM-04 절차 명시·방향판정 대상 아님)
- PASS 근거 불가: 0
- 재확인(직접 재현):
  - AM-01: 오르카 CLI 슬라이싱을 내가 직접 재실행 — amendment 미적용 시 3mf 키 641개 중 목록 밖 `silent_mode` 1개 정확히 재현. amendment 적용(허용 집합에 `silent_mode` 추가) 시 목록 밖 0개. `relaxing added=1 removed=0` 계산 재확인
  - AM-02: 설정 폴더(백업 제외) `topmost_only` 0건 / 백업 폴더 19건 각 1건 — 내가 직접 `find`+JSON 파싱으로 재확인. 이 amendment 없이는 AR-05·AR-06·SC-06이 동시 성립 불가함을 재확인
  - AM-03: `bash -n build-option-list.sh` + `python3 -m py_compile extract-bundle-ctor.py generate-option-list.py` 직접 실행, 경고/오류 0개
- 집합형 direction 계산 결과 재확인 (자기신고 아닌 계산값): AM-01 `relaxing added=1 removed=0`, AM-02 `relaxing measured_removed=19/15 measured_added=0`

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0
  - 계약 창(2026-09-15 16:12~평가시각 17:30) 사이 사용자 발언을 직접 읽었다. 16:25~17:14 구간의
    항목은 전부 백그라운드 task-notification과 reflect-kit Stop훅 자동 프롬프트(transcript 분석
    요청)였고, 실사용자의 방향 교정 텍스트는 없었다. AM-01/AM-02가 인용한 질문·답(16:12 계약
    창 이전 세션 대화 기록)은 이미 두 amendment에 반영되어 있다
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (6/6)
- [x] SK-01: `SKILL.md` 음성 대조 절(`#### 음성 대조`~다음 `####` 직전, 115줄)에 신규 시험 파일
  2종 행 존재 — PASS
  - 근거: 직접 `awk` 로 절 범위를 잘라 `grep -c` 실측. `process-bambu-only-key-in-orca.json`=7,
    `process-pre-start-fan-time.json`=5 (사전값 0/0). L3
- [x] SK-02: `bambu-fields-baseline.md` §11.1~§11.2 범위에 `option-keys/`·`strings -a -n 3` 명시 — PASS
  - 근거: 직접 `awk` 범위 추출 후 `grep -c 'option-keys/'`=2, `grep -c 'strings -a -n 3'`=2 (사전값 0/0)
- [x] SK-03: `option-keys/` 2개 파일 canonical 749/679 — PASS
  - 근거: 직접 `grep -c '^canonical'` 실측, `orca-2.4.2.tsv`=749, `bambu-02.08.02.61.tsv`=679, 계약 수치와 정확 일치
- [x] SK-04: 종류별 줄 수(오르카 process 356/filament 127/machine 161, 뱀부 277/143/136), enum(384/385) — PASS
  - 근거: 두 파일 각각 `grep -c '^process\|^filament\|^machine\|^enum'` 직접 실측, 8개 수치 전부 계약과 정확 일치
- [x] SK-05: 옛 이름/값 5개 사례 exact-line 존재 — PASS
  - 근거: `grep -cxF` 5개 패턴을 두 파일에 직접 실행. 4개 사례는 오르카·뱀부 각 1건, `renamed-value top_surface_pattern zig-zag rectilinear`는 오르카 1/뱀부 0 — 계약과 정확 일치
- [x] SK-06: 옛 판정 구현 3종 전부 0건 — PASS
  - 근거: `SKILL.md`에서 `ENUM_ALLOW`=0, `SYS.parent.rglob`=0, `"aligned_back",))`=0 직접 확인 (사전값 5/1/1)

### Script (12/12)
- [x] SC-01: orca 대상 신규 픽스처 FAIL 1건·모르는 키·exit 1 + 음성 대조 — PASS
  - 근거: `SKILL.md`에서 AM-04가 명시한 절차(`awk`)로 게이트 코드를 직접 추출해 실행.
    `TARGET_SLICER=orca`로 FAIL 1건("모르는 키 override_filament_scarf_seam_setting"), exit=1.
    음성 대조: 판정 분기(`errs.append(f"모르는 키 ...`) 제거 사본은 exit=0·`RESULT: PASS` — 직접 재현
- [x] SC-02: 오르카 전용 키 `scarf_joint_speed`를 bambu 대상에 주입 시 FAIL 1건·모르는 키·exit 1 — PASS
  - 근거: `process-thin-baseline.json`에 키 1개만 더한 사본을 직접 생성·실행, FAIL 1건, exit=1
- [x] SC-03: bambu 대상 `pre_start_fan_time` FAIL 1건·키 스코프 불일치·exit 1 + 음성 대조 — PASS
  - 근거: 직접 실행, FAIL 줄에 "키 스코프 불일치"·"pre_start_fan_time"·"filament" 모두 포함(각 grep -c=1), exit=1.
    음성 대조(종류 판정을 번들 프로파일 합집합으로 되돌린 사본, "기준점 1개" 변이 확인) 실행 시 `RESULT: PASS`로 재현
- [x] SC-04: 옛 키 `wall_infill_order` 주입 시 FAIL 0·"옛 이름"과 "wall_sequence" 한 줄 — PASS
  - 근거: 직접 실행, FAIL=0, WARN 줄에 "옛 이름"·"wall_sequence" 동시 존재
- [x] SC-05: 슬라이서별 enum 3사례 — PASS
  - 근거: `process-machine-scope-key.json`에서 `retraction_minimum_travel`을 빼고 각 키 1개씩 주입한
    사본 3개를 직접 실행. (a) orca `brim_type: painted` → FAIL=0 (b) orca `top_surface_pattern: zig-zag`
    → FAIL=0, WARN에 "옛 값"·"rectilinear" 동일 줄 (c) bambu `seam_position: aligned_back` → FAIL=1,
    "받지 않는 값" 포함. 3사례 모두 계약 기대치와 정확 일치
- [x] SC-06: 설정 폴더 154 + 기존 픽스처 9(합 163) FAIL 집합이 `03b2122` 검사와 동일, 3종 토큰 0건 — PASS
  - 근거: `git show 03b2122:.../SKILL.md`에서 옛 게이트를 직접 추출하고, 신규 게이트와 함께 163개
    파일(신규 픽스처 2개 제외, `_backup-...` 폴더 제외로 154개 확인)에 각각 실행하는 비교 스크립트를
    직접 작성·실행. old_fail=64, new_fail=64, 대칭차 0, "모르는 키"·"옛 이름"·"옛 값" 토큰 0건
- [x] SC-07: 빌드 스크립트(수정된 버전) 재실행 시 목록이 커밋본과 완전 일치 — PASS
  - 근거: 수정된(quoting 반영) `build-option-list.sh`를 `OPTION_KEY_PROBE_WORK` 캐시로 orca·bambu
    각 1회 재빌드(둘 다 exit 0), 결과 tsv를 커밋본과 `diff` — 0줄. canonical 749/679 등 SK-03/04
    수치와도 재일치. **수정된 스크립트 자체로 재생성해 회귀 없음을 확인**
- [x] SC-08: `PresetBundle::PresetBundle()` 생성자 원문과 추출 파일이 문자 단위로 동일 — PASS
  - 근거: 태그 원본(`fresh-work/{orca,bambu}/src/libslic3r/PresetBundle.cpp`)에서 동일한 괄호짝
    규칙으로 직접 원문 블록을 추출(오르카 3737자·뱀부 3643자)해, 커밋된 `extract-bundle-ctor.py`가
    만든 추출 파일에 그 블록이 문자 그대로 포함되는지 `in` 연산으로 확인 — 둘 다 True
- [x] SC-09: 설치본 명령줄 자르기 결과 키가 목록(+AM-01 `silent_mode`)에 전부 포함 — PASS
  - 근거: OrcaSlicer·BambuStudio CLI를 직접 구동(`--load-settings`+`--load-filaments`+`--slice 0`
    +`--export-3mf`), 두 슬라이서 모두 exit=0·로그 에러 0건. 3mf `Metadata/project_settings.config`
    키 수 오르카 641·뱀부 578(계약 사전값과 정확 일치), 목록 밖 키 0개(AM-01 미적용 시 오르카에서
    `silent_mode` 1개 재현되어 amendment 필요성도 재확인)
- [x] SC-10: 제조사 프로파일 전체(오르카 11,554/뱀부 3,390) "받지 않는 값" 0/0, "키 스코프 불일치"
  오르카 0·뱀부 정확히 1(`fdm_process_common.json`/`pre_start_fan_time`) — PASS
  - 근거: 두 슬라이서 설치본의 process/filament/machine 타입 JSON 전체(직접 카운트 11554/3390 —
    계약 수치와 정확 일치)를 커밋된 게이트로 배치 실행(400개씩 서브프로세스). "받지 않는 값" 오르카
    0·뱀부 0, "키 스코프 불일치" 오르카 0·뱀부 정확히 1건이며 그 1건이 정확히
    `fdm_process_common.json`의 `pre_start_fan_time`
- [x] SC-11: `validate-plugin.py bambu-kit` exit 0 — PASS
  - 근거: 직접 실행, exit=0, V1~V8 전부 OK
- [x] SC-12: `gate-fixtures/` 신규 파일 정확히 2개 — PASS
  - 근거: `git status --porcelain -- bambu-kit/evals/gate-fixtures/` `??` 2줄, 파일명 정확 일치

### Error (1/1)
- [x] ER-01: 목록 없음 → `[미검증]` 1개 이상 + 3종 FAIL 0개 — PASS
  - 근거: 목록 경로를 존재하지 않는 경로로 바꾼 사본(변이 적용 `grep -c`=1로 먼저 확인)을 직접
    실행, `[미검증]` 1줄, "모르는 키"·"키 스코프 불일치"·"받지 않는 값" 전부 0

### Architecture (6/6)
- [x] AR-01: 변경 범위가 열거된 8개 경로 이내 — PASS
  - 근거: `git status --porcelain -- bambu-kit docs/bambu-kit` 직접 실행, 4개 수정(SKILL.md·
    bambu-fields-baseline.md·두 docs html) + 4개 신규(option-keys/ 하위·option-key-probe/ 하위·
    신규 픽스처 2개) 전부 열거 목록 이내, 그 밖 0건. `bambu-kit/scripts/`·`option-keys/` 내부
    파일 목록도 직접 확인해 하위 경로 조건과 일치
- [x] AR-02: 파생 페이지 2종에 신규 서술 존재 — PASS
  - 근거: `bambu-print-profile.html` "모르는 키"=2·"받지 않는 값"=2, `bambu-fields-baseline.html`
    "option-keys"=1 (직접 grep)
- [x] AR-03: 옛 판정 서술 "제조사 전체를 읽는다" 0건 — PASS
  - 근거: grep -c=0 (사전값 1)
- [x] AR-04: notes.md 검사 사각 경고가 해소 서술로 교체 — PASS
  - 근거: "못 잡는다" 0건. 파일 전문에서 "검사의 사각 해소(2026-09-15)" 절과 FAIL/PASS 재현 로그
    실측 서술을 직접 확인
- [x] AR-05: 과거 프로파일 19개 고침, 백업 원본 보존, 그 외 키 불변 — PASS
  - 근거: 설정 폴더(백업 제외) `"topmost_only"` 0건(직접 `find`+grep), 백업 폴더 19개 파일 각 1건.
    19개 파일 전부 원본·수정본을 JSON으로 직접 파싱해 `ironing_type` 외 키 차이 0건(전수 비교 스크립트 직접 작성·실행)
- [x] AR-06: 가져오기 zip 15개 고침, 이름목록·CRC 보존 — PASS
  - 근거: 메인 zip 56개(직접 카운트) 중 `topmost_only` 0건. 백업 zip 15개(항목 17개)를 직접
    `zipfile`로 순회해 이름 목록 동일성, 미수정 항목 CRC 동일성, 수정 항목 17개의 `ironing_type`
    외 키 불변을 전수 확인 — 불일치 0건

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS
  - 근거: `validate-plugin.py --check=code-fence` 전체 14개 플러그인 exit=0
- [x] AP-04: `SKILL.md` name 필드 유지 — PASS
  - 근거: `validate-plugin.py bambu-kit` V1 OK, frontmatter 직접 확인

### Reusability (2/2)
- [x] RE-01: private화된 재사용 가능 컴포넌트 없음 — PASS
  - 근거: 신규 스크립트는 `bambu-kit/scripts/option-key-probe/`에 위치, 다른 킷(`design-kit/scripts`
    등)과 동일 위치 관행. 측정 명령이 계약에 없어 판단 근거는 정성적(계약 결함 — Improvement 참조)
- [x] RE-02: 기존 유사 컴포넌트 재사용 확인 — PASS
  - 근거: `grep -rln "PresetBundle::PresetBundle\|option_key_probe\|extract-bundle-ctor"` 레포 전체
    실행 결과 신규 위치 외 0건. 측정 명령 부재(계약 결함, Improvement 참조)

### Diagnostics (4/4)
- [x] DG-01: `bash -n scripts/release.sh` + (AM-03) `bash -n build-option-list.sh` 워닝 0개 — PASS
  - 근거: 두 스크립트 모두 직접 `bash -n` 실행, 출력 없음
- [x] DG-02: IDE diagnostics 워닝/인포 0개(제외 없음) — **PASS (Iteration 1 REJECT 사유 해소 확인)**
  - 근거: `shellcheck bambu-kit/scripts/option-key-probe/build-option-list.sh` 직접 실행 —
    기본 심각도 및 `-S style`·`-S info` 전부 exit=0·출력 없음(Iteration 1의 SC2206 경고 3건은
    26·27행 `"SLIC3R_VERSION=$VERSION"`·`"SoftFever_VERSION=$VERSION"` 인용 처리로 해소됨을
    직접 diff 대조). 신규 파이썬 2개는 `py_compile`+`ast.parse` 0 오류. 이 맥에 python/cpp 정적
    분석기(ruff·pyflakes·pylint·flake8·mypy·cpplint·cppcheck·clang-tidy)가 전부 미설치임을
    직접 확인(`which` 전부 not found) — 레포 전체에 python lint 설정(`pyproject.toml`/`.flake8`/
    CI 워크플로우)이 전무해 기존 관행과 동일선상이므로 이 부분은 shell 외 언어의 측정-수단-부재로
    Improvement에 기록(PASS를 막지 않음, 이 스프린트가 새로 만든 결함이 아님)
- [x] DG-03: `bash scripts/release.sh 2>&1 \|\| true` + (AM-03) `py_compile` 오류 0개 — PASS
  - 근거: release.sh는 사용법 안내만 출력(에러/예외 문자열 0건). `python3 -m py_compile
    extract-bundle-ctor.py generate-option-list.py` 오류 0개. 실행 중 생성된 `__pycache__`는
    내가 만든 것임을 mtime으로 확인 후 즉시 삭제해 원상 복구(레포에 흔적 없음)
- [x] DG-04: 실제 앱/서버 구동 시 에러 0개 — PASS
  - 근거: SC-09/AM-01 재현 과정에서 OrcaSlicer·BambuStudio CLI를 직접 구동(2회, 각 300초
    타임아웃 하에 정상 종료), 둘 다 exit=0·로그에 error/exception/crash/abort 토큰 0건. 측정
    명령이 계약에 없어 판단 근거는 실행 재현(계약 결함, Improvement 참조)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (33 - 0) / 33 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (33개 조건 전부 이번 평가자가 직접 재실행/재측정. Iteration 1의 판정을
  인용만 한 조건은 0개)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션 안전성·
  재시도/중복제거·보안 경계·사용자 결함-테스트 충돌 9항목에 해당하는 조건이 이 계약에 없음)
- 계약 자체가 SC-01~SC-05, SC-09에 "음성 대조" 절을 요구하므로 별도로 전부 직접 재현했다
  (판정 분기 제거 시 PASS로 뒤집힘을 SC-01·SC-03에서, 종류판정 원복 시 SC-03에서, enum/스코프
  판정 분기 제거 시 SC-01/SC-05 계열에서 각각 재현 — 위 Results 참조)

## User-Reported Failures
- 해당 없음

## Evidence Validity
- 검사 대상 증거: 33건, 전부 이번 세션에서 새로 직접 실행/측정 (Iteration 1 결과 인용 0건)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 계약 자체가 요구하는 것은 문서형 셸 스니펫이 아니라 실행형 검사 코드다.
  AM-04가 명시한 `awk` 추출 절차를 zsh(현재 셸)에서 직접 실행해 정상 동작 확인. SC-06/SC-10의
  대규모 배치 스크립트도 별도로 새로 작성해 이 세션에서 직접 실행
- 무효 0건은 미검증 카운터에 합산 없음 (누계 0)

## Summary
- Total: 33/33 conditions passed
- Verdict: APPROVE
- Iteration 1의 유일한 FAIL(DG-02, `build-option-list.sh`의 shellcheck SC2206 경고 3건)이
  `"${VERSION}"` 형태의 인용 처리로 해소되었음을 직접 확인했다. 그 수정이 유일한 변경분이었고
  (mtime 대조로 확인), 수정된 스크립트로 재빌드한 목록도 커밋본과 완전히 일치해(SC-07) 회귀가
  없다. 나머지 32개 조건도 Iteration 1의 판정을 그대로 인용하지 않고 이번 세션에서 전부 독립
  재실행하여 동일한 결과(SK-01~06, SC-01~12, ER-01, AR-01~06, AP-03/04, RE-01/02, DG-01/03/04)를
  얻었다. 33/33 PASS로 APPROVE.

## Improvement Suggestions
- [RE-01] 측정-수단-부재 — "다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다"에
  검증 명령이 없다. 예: `grep -rn "class \|def " bambu-kit/scripts/` 로 공개 API 후보를 나열하고
  사용처를 grep으로 대조
- [RE-02] 측정-수단-부재 — "이미 동일/유사 컴포넌트가 있으면 재사용" 판정 기준이 없다. 예:
  `grep -rl <핵심 함수명 후보> --include=*.py --include=*.sh . | grep -v <신규 경로>` 로 0건 확인을
  측정으로 명시
- [DG-02] 측정-방식-불일치 — "IDE diagnostics 워닝/인포 0개(제외 없음)"가 shell 외 언어(python·
  cpp)에는 이 환경에 대응 정적 분석 도구가 전무하고, 레포 전체에도 python lint 설정이 없다.
  스택별 측정 도구를 조건에 명시(예: `shellcheck` for `*.sh`, 파이썬은 `python3 -m py_compile`
  까지만 요구)하지 않으면 다음 스프린트도 같은 해석 모호성이 반복된다
- [DG-04] 측정-수단-부재 — "실제 앱/서버 구동 시 에러 0개"가 이 스프린트에서 무엇을 구동하라는
  것인지 정의가 없다(project.yaml 템플릿 상투구로 추정). 예: `TARGET_SLICER=<orca|bambu> 로 실제
  슬라이서 CLI를 1회 이상 구동해 로그에 error/exception 0건`으로 구체화
