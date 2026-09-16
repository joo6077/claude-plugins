---
feature: "bambu-kit 옵션 키 판정을 태그 등록부 기준으로 교체"
slug: bambu-kit-option-key-registry-probe
created: "2026-09-15 16:12"
complexity: "복잡"
conditions: 33
status: done
owner_session: 5d88caf0-e6ef-425e-a688-7cd21beae1d9
conditions_digest: sha256:2cae367545296fef
locked_at: "2026-09-15 16:14"
---

## 배경

오르카 전용 Funnel 프로파일을 만들다가 Phase 4.3 검사의 구멍이 드러났다. 뱀부 전용 키
`override_filament_scarf_seam_setting` 을 오르카 파일에 넣어도 통과한다. 검사가 키 존재와 프리셋 종류를
**번들 프로파일에 그 키가 등장하는지**로 판정하는데, 오르카는 뱀부 제조사 프로파일을 복사해 싣고 다니므로
그 안에 뱀부 키가 들어 있다. 같은 이유로 종류 판정도 샌다 — 뱀부 제조사의 process 기본 프로파일
`fdm_process_common.json` 이 filament 키 `pre_start_fan_time` 을 잘못 담고 있어서, 그 키를 process 파일에
넣어도 통과한다 (2026-09-15 실측). enum 허용값은 손으로 적은 6 개 키 표라 슬라이서별 차이를 놓친다 —
오르카는 `top_surface_pattern: zig-zag` 를 `rectilinear` 로 바꿔 넣는데 지금 검사는 통과시키고, 오르카가
받는 `brim_type: painted` 는 떨어뜨린다 (실측).

실행 파일 문자열로 판정하는 대안을 먼저 검토했으나 리서치(Codex · 두 태그 소스)와 실측으로 한계가 확인됐다.
사용자가 **태그 소스로 판정 프로그램을 빌드해 슬라이서 자신의 판정 함수로 목록을 뽑는 방법**을 골랐고,
범위를 키 존재 · 프리셋 종류 · enum 값 셋 다로 넓혔다.

빌드 가능성과 판정 정확도는 계약 전에 확인했다. 두 태그의 옵션 등록부 · 옛 이름 처리 · 프리셋 소스를
부분 컴파일한 판정 프로그램이 돌고, 설치본 슬라이서를 명령줄로 잘라 낸 결과와 **주입한 14 개 사례 전부
일치**했다 (가짜 키 · 슬라이서 전용 키 · 옛 키 · 옛 값 · 별칭 · 무시 목록 · 받지 않는 enum 값).

## 리서치 소스

- Codex 리서치 1 회 (gpt-5.6-sol · 조회 전용 · 526 초) — OrcaSlicer `v2.4.2` · BambuStudio `v02.08.02.61`
  태그의 `PrintConfig.cpp` · `Config.cpp` · `Preset.cpp` · `PresetBundle.cpp` · `bbs_3mf.cpp` · `GCode.cpp`
- 설치본 명령줄 자르기 실험 8 회 (오르카 4 · 뱀부 4) — 주입 키·값이 결과 3mf 에 어떻게 남는지 판정
- 판정 프로그램 부분 빌드 · 목록 생성 (2026-09-15) — 오르카 받는 키 749 · 뱀부 679
- 제조사 프로파일 교차 확인 — 오르카 11,554 개 · 뱀부 3,390 개를 목록으로 판정

## GAP 분석

| 대상 | 현재 | 갭 |
| --- | --- | --- |
| `SKILL.md` Phase 4.3 키 존재 | 번들 프로파일 등장 여부 | 슬라이서가 모르는 키를 통과시킨다 |
| `SKILL.md` Phase 4.3 키 종류 | 번들 프로파일 종류 합집합 | 제조사 프로파일의 실수가 허용 근거가 된다 |
| `SKILL.md` Phase 4.3 enum 값 | 손으로 적은 6 키 표 + 오르카 `aligned_back` 분기 | 슬라이서별 차이 · 옛 값 바꾸기를 놓친다 |
| `references/bambu-fields-baseline.md` §11.1 | 키 존재 1 순위 근거가 `strings -a` | 옛 이름 통과 · 4 글자 미만 누락 · 명령 실패 시 빈 출력 |
| `bambu-kit/scripts/` · `references/option-keys/` | 없음 | 목록을 다시 만들 도구도, 버전별 기준 목록도 없다 |

## 범위 경계

키 존재 · 프리셋 종류 · enum 값 판정을 목록 기준으로 바꾼다. 형상 클래스 · 유량비 · 금지 키 · 부모값 검사는
그대로 둔다.

종류 판정은 설정 가져오기 화면을 거친 **직접 실행 확인이 불가능하다** (명령줄 경로는 `remove_invalid_keys` 를
거치지 않고, 뱀부 실행 로그는 암호화돼 있다). 대신 SC-08(생성자 원문 그대로 추출)과 SC-10(제조사 프로파일
교차 판정)으로 확인한다.

사용자 설정 폴더의 과거 프로파일 19 개가 `ironing_type: topmost_only` 를 쓰고 있고 실제 뱀부가 이를
`no ironing` 으로 바꾼다 (명령줄 자르기로 확인 · G-code 다림질 구간 0). 사용자 요청으로 **범위에 넣는다** —
설정 폴더 JSON 19 개와 가져오기용 zip 15 개 안의 JSON 17 개를 `topmost` 로 고치고, 원본은 백업 폴더에 둔다.

뱀부 안에 **이미 가져온 사용자 프리셋 14 개**는 고치지 않는다. 가져올 때 잘못된 값이 기본값으로 바뀌면서
`ironing_type` 키 자체가 빠진 상태인데, 뱀부가 실행 중이라 내부 저장소를 직접 고치면 종료 시 덮어써지거나
동기화와 충돌할 수 있다. 고친 zip 으로 다시 가져오도록 안내한다.

AR-01 사전 값 — 계약 작성 시점 `git status --porcelain -- bambu-kit docs/bambu-kit` 결과 **0 건**.
조건 낱말 `모르는 키` · `옛 이름` · `옛 값` · `받지 않는 값` · `option-keys` · `process-bambu-only-key-in-orca` ·
`process-pre-start-fan-time` 은 대상 파일 전부에서 0 건. 구현 전 기준 커밋은 `03b2122` 다.

커버리지 해소: AR-01 — 측정 명령 `git status --porcelain -- bambu-kit docs/bambu-kit` 한 번이 산문에 열거한 경로 8 개를 모두 포함하는 상위 범위를 출력하고, 판정은 그 출력이 열거 경로 이내인지를 본다. 경로를 측정 절에 다시 적으면 같은 목록을 두 번 쓰게 된다.

## 회귀 게이트

SC-06 이 기존 통과분을 지킨다. 목록 규칙 시범판으로 기존 163 개 파일(설정 폴더 154 · 시험용 파일 9)을
미리 재서, 떨어지는 파일 집합이 `03b2122` 의 검사와 **같음**을 확인했다 — enum 값 20 개 파일(과거
`topmost_only` 19 + `process-seam-slope-type-invalid.json`), 종류 3 개 시험 파일, 모르는 키 0, 경고 0.
AR-05 로 과거 파일 19 개를 고친 뒤에는 두 검사 모두에서 enum 값으로 떨어지는 파일이 시험 파일 1 개로 준다 —
SC-06 은 **같은 파일에 두 검사를 돌려 비교**하므로 고친 뒤에 재도 성립한다.

## Skill

- [ ] SK-01: `SKILL.md` 의 음성 대조 절(`#### 음성 대조` 헤더부터 다음 `####` 헤더 전까지)에 신규 시험 파일 `process-bambu-only-key-in-orca.json` · `process-pre-start-fan-time.json` 의 행이 각각 있다 [exact, enumerated] (측정: `SKILL.md` 의 그 범위를 `awk` 로 잘라 `process-bambu-only-key-in-orca.json` · `process-pre-start-fan-time.json` 각각 `grep -c` >= 1 · 사전 값 둘 다 0)
- [ ] SK-02: `references/bambu-fields-baseline.md` §11.1 이 키 판정의 1 순위 기준을 `option-keys/` 목록으로 명시하고, 실행 파일 문자열의 한계(옛 이름·무시 목록 통과, `strings -a -n 3` 필요)를 적는다 [structural] (측정: `### 11.1` ~ `### 11.2` 범위 `awk` 추출 후 `grep -c 'option-keys/'` >= 1 이고 `grep -c 'strings -a -n 3'` >= 1 · 사전 값 둘 다 0)
- [ ] SK-03: `references/option-keys/` 에 `orca-2.4.2.tsv` · `bambu-02.08.02.61.tsv` 2 개가 있고 `canonical` 줄 수가 각각 749 · 679 이다 [exact, enumerated] (측정: `references/option-keys/` 의 `orca-2.4.2.tsv` · `bambu-02.08.02.61.tsv` 각각 `grep -c '^canonical'` · 시범 생성 실측값)
- [ ] SK-04: 같은 두 파일의 종류별 줄 수가 오르카 process 356 · filament 127 · machine 161, 뱀부 process 277 · filament 143 · machine 136 이고 `enum` 줄 수가 오르카 384 · 뱀부 385 다 [exact, enumerated] (측정: 파일별 `grep -c '^process'` · `'^filament'` · `'^machine'` · `'^enum'` · 시범 생성 실측값)
- [ ] SK-05: 같은 두 파일에 옛 이름 사례가 들어 있다 — 두 파일 모두 `renamed wall_infill_order wall_sequence` · `renamed enable_wipe_tower enable_prime_tower` · `renamed-value wall_infill_order inner wall/outer wall/infill inner wall/outer wall` · `enum filament_z_hop_types nil`, 오르카 파일에만 `renamed-value top_surface_pattern zig-zag rectilinear` [exact, enumerated] (측정: 탭 구분 줄 정확 일치 `grep -cx` · 오르카 1 / 뱀부 0 · 시범 생성 실측값)
- [ ] SK-06: `SKILL.md` 에서 옛 판정 구현이 사라진다 — `ENUM_ALLOW` 0 건 · `SYS.parent.rglob` 0 건 · `"aligned_back",))` 0 건 [exact, enumerated] (측정: `SKILL.md` 에서 `ENUM_ALLOW` · `SYS.parent.rglob` · `"aligned_back",))` 각 `grep -c` == 0 · 사전 값 5 / 1 / 1)

## Script

- [ ] SC-01: Given 구현 완료. When `TARGET_SLICER=orca` 로 `evals/gate-fixtures/process-bambu-only-key-in-orca.json` 을 Phase 4.3 검사에 넣으면 Then FAIL 줄이 정확히 1 개이고 그 줄에 `모르는 키` 가 있으며 exit 1 이다 [goal] (측정: `SKILL.md` 에서 검사 코드를 추출해 실행, `grep -c '^FAIL'` == 1 · `grep -c '모르는 키'` == 1 · `echo $?` == 1) 음성 대조: 목록의 키 존재 판정 분기를 지운 사본으로 같은 입력을 넣으면 `RESULT: PASS` · exit 0 이 된다 (구현 전 사전 값: 같은 키를 담은 사본이 PASS · 2026-09-15 실측)
- [ ] SC-02: Given 구현 완료. When `evals/gate-fixtures/process-thin-baseline.json` 에 오르카 전용 키 `scarf_joint_speed` 1 개만 더한 사본을 `TARGET_SLICER=bambu` 로 검사하면 Then FAIL 줄 1 개에 `모르는 키` 가 있고 exit 1 이다 [goal] (측정: 임시 사본 실행 · 구현 전 사전 값: `[미검증]` 1 줄 + PASS 실측) 음성 대조: 목록의 키 존재 판정 분기를 지우면 PASS
- [ ] SC-03: Given 구현 완료. When `TARGET_SLICER=bambu` 로 `evals/gate-fixtures/process-pre-start-fan-time.json` 을 검사하면 Then FAIL 줄이 정확히 1 개이고 그 줄에 `키 스코프 불일치` · `pre_start_fan_time` · `filament` 가 모두 있으며 exit 1 이다 [goal] (측정: 추출 검사 코드 실행 · 구현 전 사전 값: 같은 키를 담은 사본이 PASS · 2026-09-15 실측) 음성 대조: 종류 판정 근거를 번들 프로파일 종류 합집합으로 되돌린 사본으로 같은 입력을 넣으면 `RESULT: PASS` 가 된다
- [ ] SC-04: Given 구현 완료. When `evals/gate-fixtures/process-thin-baseline.json` 에 옛 키 `wall_infill_order` 1 개만 더한 사본을 `TARGET_SLICER=bambu` 로 검사하면 Then FAIL 줄은 0 개이고 `옛 이름` 과 `wall_sequence` 가 같은 한 줄에 나온다 [goal] (측정: 임시 사본 실행 · `grep -c '^FAIL'` == 0 · `grep '옛 이름' | grep -c 'wall_sequence'` == 1)
- [ ] SC-05: Given 구현 완료. 슬라이서별 enum 판정이 실제 슬라이서 동작과 같다. 사례 3 개(각각 `process-machine-scope-key.json` 에서 `retraction_minimum_travel` 을 빼고 한 키만 더한 사본): (a) `TARGET_SLICER=orca` · `brim_type: painted` → FAIL 0 (사전 값: FAIL 1) (b) `TARGET_SLICER=orca` · `top_surface_pattern: zig-zag` → FAIL 0 이고 `옛 값` · `rectilinear` 가 같은 한 줄 (사전 값: PASS · 경고 없음) (c) `TARGET_SLICER=bambu` · `seam_position: aligned_back` → FAIL 1 이고 그 줄에 `받지 않는 값` (사전 값: FAIL 1) [goal] (측정: 사본 3 개 실행 · 사례 수는 열거한 3 개 고정 · 세 사례의 실제 슬라이서 결과는 명령줄 자르기로 확인됨 — painted 유지 / rectilinear 로 바뀜 / aligned 로 바뀜)
- [ ] SC-06: Given 구현 완료. `/Users/jackson/Hub/60_3D Print/Settings` 아래 `type` 이 process · filament 인 JSON 154 개와 `bambu-kit/evals/gate-fixtures/` 기존 9 개(합 163)를 각자의 대상 슬라이서로 검사했을 때, FAIL 이 한 줄이라도 나오는 파일의 집합이 `git show 03b2122:bambu-kit/skills/bambu-print-profile/SKILL.md` 의 검사로 잰 집합과 같고, `모르는 키` · `옛 이름` · `옛 값` 줄은 0 건이다. 대상 슬라이서는 `_target_slicer` 값, 없으면 경로에 `orca` 가 있으면 orca, 아니면 bambu 다 [goal] (측정: 두 검사 코드로 전 파일 순회 후 파일 집합 `comm -3` 0 줄 · 토큰 `grep -c` 0 · 신규 시험 파일 2 개는 합산 제외)
- [ ] SC-07: `bambu-kit/scripts/option-key-probe/` 의 빌드 스크립트를 `orca` · `bambu` 로 각각 실행하면 판정 프로그램이 만들어지고, 그것으로 다시 만든 목록이 SK-03 의 커밋된 목록과 한 줄도 다르지 않다 [goal] (측정: 빌드 → 목록 재생성 → `diff` 출력 0 줄, 슬라이서별 2 회)
- [ ] SC-08: 종류별 키 목록은 태그 `PresetBundle.cpp` 의 기본 생성자를 원문 그대로 잘라 컴파일해 얻는다. 빌드 스크립트가 만든 생성자 추출 파일의 생성자 본문이 태그 원본의 해당 본문과 문자 단위로 같다 — 오르카 · 뱀부 각각 [goal] (측정: 원본에서 `PresetBundle::PresetBundle()` 부터 짝 맞는 `}` 까지와 추출 파일의 같은 범위를 `diff` · 출력 0 줄)
- [ ] SC-09: 커밋된 목록이 설치본과 일치한다 — 설치본을 명령줄로 잘라 낸 `Metadata/project_settings.config` 의 키가 목록의 `canonical` 또는 `header` 에 모두 있다, 오르카 2.4.2 · 뱀부 02.08.02.61 각각 [goal] (측정: 명령줄 자르기 1 회씩 후 집합 차 0 · 사전 실측 오르카 641 · 뱀부 578 키)
- [ ] SC-10: 커밋된 목록으로 설치본 제조사 프로파일 전체를 Phase 4.3 검사에 넣었을 때 `받지 않는 값` 줄이 오르카 11,554 개 · 뱀부 3,390 개 모두 0 건이고, `키 스코프 불일치` 줄이 오르카 0 건 · 뱀부 정확히 1 건(`BBL/process/fdm_process_common.json` 의 `pre_start_fan_time`)이다 [goal] (측정: 대상 슬라이서별로 제조사 JSON 을 여러 묶음으로 나눠 검사 코드에 넣고 토큰 합산 · 시범 규칙 실측값)
- [ ] SC-11: `python3 scripts/validate-plugin.py bambu-kit` 가 exit 0 이다 [goal] (측정: 실행 후 `echo $?` == 0)
- [ ] SC-12: `bambu-kit/evals/gate-fixtures/` 신규 파일이 정확히 2 개 `process-bambu-only-key-in-orca.json` · `process-pre-start-fan-time.json` 이다 [exact, enumerated] (측정: 대상 폴더 `bambu-kit/evals/gate-fixtures/` 에 `git status --porcelain -- bambu-kit/evals/gate-fixtures/` 를 실행해 `??` 줄 == 2 이고 그 경로가 `process-bambu-only-key-in-orca.json` · `process-pre-start-fan-time.json` 와 일치)

## Error

- [ ] ER-01: Given 구현 완료. When 설치본 슬라이서 버전에 해당하는 목록 파일이 없으면(목록 폴더 경로를 존재하지 않는 곳으로 바꾼 검사 코드 사본) Then 조용히 통과하지 않고 `[미검증]` 줄을 1 개 이상 출력하며 `모르는 키` · `키 스코프 불일치` · `받지 않는 값` FAIL 은 0 개다 [goal] (측정: 경로 변이 사본을 `TARGET_SLICER=orca` 로 `process-bambu-only-key-in-orca.json` 에 실행 · 변이 적용은 `grep -c` 로 먼저 확인)

## Architecture

- [ ] AR-01: 변경 범위가 한정된다. Given 구현 완료 · 커밋 전. `git status --porcelain -- bambu-kit docs/bambu-kit` 결과가 `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` · `bambu-kit/skills/bambu-print-profile/references/option-keys/` 하위 · `bambu-kit/scripts/option-key-probe/` 하위 · `bambu-kit/evals/gate-fixtures/process-bambu-only-key-in-orca.json` · `bambu-kit/evals/gate-fixtures/process-pre-start-fan-time.json` · `docs/bambu-kit/bambu-print-profile.html` · `docs/bambu-kit/bambu-fields-baseline.html` 이내이고 그 밖 0 건이다 [exact, enumerated] (측정: 위 명령 · 사전 값 0 건)
- [ ] AR-02: 파생 페이지 2 종이 소스 변경을 반영한다 — `docs/bambu-kit/bambu-print-profile.html` 에 `모르는 키` >= 1 · `받지 않는 값` >= 1, `docs/bambu-kit/bambu-fields-baseline.html` 에 `option-keys` >= 1 [exact, enumerated] (측정: `docs/bambu-kit/bambu-print-profile.html` 의 `모르는 키` · `받지 않는 값`, `docs/bambu-kit/bambu-fields-baseline.html` 의 `option-keys` 각 `grep -c` · 사전 값 전부 0)
- [ ] AR-03: 파생 페이지에서 옛 판정 서술이 사라진다 — `docs/bambu-kit/bambu-print-profile.html` 의 `제조사 전체를 읽는다` 0 건 [exact] (측정: `grep -c` == 0 · 사전 값 1)
- [ ] AR-04: 사용자 출력 폴더 `/Users/jackson/Hub/60_3D Print/Settings/ams-2-pro-lattice-dry-pods/orca-funnel/notes.md` 의 검사 사각 경고가 해소 서술로 바뀐다 [exact] (측정: `grep -c '못 잡는다'` == 0 · 사전 값 1)
- [ ] AR-05: 사용자 설정 폴더의 과거 프로파일에서 받지 않는 값이 사라진다. Given 구현 완료. `/Users/jackson/Hub/60_3D Print/Settings` 아래 JSON 중 `"topmost_only"` 문자열을 담은 파일이 0 개이고, 백업 폴더 `/Users/jackson/Hub/60_3D Print/Settings/_backup-2026-09-15-ironing-topmost_only/` 에 원본 19 개가 원래 상대 경로 그대로 있으며 각각 `"topmost_only"` 를 1 건씩 담는다. 고친 19 개 파일은 `ironing_type` 이 `topmost` 이고 그 밖의 키·값은 원본과 같다 [exact] (측정: `find` + `grep -l` 개수 · 백업 파일 수 · 원본과 고친 파일을 JSON 으로 읽어 `ironing_type` 외 키별 비교 차이 0 · 사전 값 19 개 파일, 파일당 1 건)
- [ ] AR-06: 가져오기용 zip 안의 과거 프로파일도 고친다. Given 구현 완료. `/Users/jackson/Hub/60_3D Print/Settings` 아래 zip 안 JSON 중 `"topmost_only"` 를 담은 항목이 0 개이고, 고친 zip 15 개는 항목 이름 목록이 원본과 같으며 고친 JSON 외 항목의 내용이 원본과 바이트 단위로 같다. 원본 zip 은 AR-05 의 백업 폴더에 원래 상대 경로 그대로 있다 [exact] (측정: `zipfile` 로 항목 순회 · 이름 목록 비교 · 고친 항목 외 CRC 비교 · 사전 값 zip 15 개 · 항목 17 개)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트가 있다 (측정: `python3 scripts/validate-plugin.py --check=code-fence` exit 0)
- [ ] AP-04: `SKILL.md` 머리말에 `name` 필드가 유지된다 (측정: `python3 scripts/validate-plugin.py bambu-kit` V1 OK)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
