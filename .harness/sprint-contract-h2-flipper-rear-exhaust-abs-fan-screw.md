---
feature: "H2 Flipper 배기관 ABS — 나사 조임에 층이 벌어진 실패를 팬과 바닥 솔리드로 막는다"
slug: h2-flipper-rear-exhaust-abs-fan-screw
created: "2026-09-26 18:30"
complexity: "중간"
conditions: 26
status: done
owner_session: d204ea78-091c-4f5b-a8db-ec3ead359b73
conditions_digest: sha256:e686afa5b607ccd7
locked_at: "2026-09-26 19:01"
---

## 배경

**사용자 실물 실패**: "이거 스크류 박으니깐 옆면이 박살나던데". 깨진 모양을 물으니
**가로 층 선을 따라 벌어짐**이라고 답했다 — 구멍 둘레가 부서진 것도, 세로로 쪼개진 것도
아니다. 층 사이가 안 붙은 형태다.

### 원인 — 측정으로 좁힌 것

**(1) 나사는 판을 관통해 프린터 본체에 물린다. ABS 판은 사이에 끼인다.**
G-code 에서 구멍을 찾으니 지름 **3.72 mm** 가 세 자리, Z 1.32~3.24 mm 에 있고 **높이 전체에서
지름이 일정**했다 (머리 자리가 아니다). 나사 바깥지름 3.0 mm 에 대한 여유 구멍이라 나사산이
ABS 를 물 자리가 없다. 나사 길이 20 mm 가 판 3.2 mm 를 한참 넘는 것도 관통 구조를 가리킨다.

`HB3x20` 은 Bambu 공식 나사 목록에 없다 (`HB` 풀이도 못 찾았다). H2S 배기관 어댑터에 공식
지정된 것은 `BT3×20` (판매 코드 AA111, 플라스틱용 셀프태핑)이고, 그 공식 CAD 실측 나사산
포함각은 **약 60도**다 — "플라스틱용이면 30도" 는 성립하지 않는다. 다만 공식 문서끼리도
상충한다 (H2S 가이드 `BT3-20` vs H2 계열 목록 `BTG 3×20`). **이 스프린트는 나사 종류를
전제하지 않는다** — 여유 구멍이라는 측정 사실만 쓴다.

**(2) 그 판이 속이 비어 있다.** `bottom_shell_layers 4` = 솔리드 0.68 mm 로, 판 3.2 mm 의
**21 %** 뿐이고 나머지는 채움 25 % 다. 나사 머리가 조여지며 이 속 빈 판을 눌러 층을 벌렸다.

**(3) 층 접착이 약했다.** 자른 G-code 에서 부품 냉각 팬을 압출 길이로 가중해 재니 **평균 56.1 %**
였고 (Z 10 mm 이상 전 구간 52~79 %), 팬이 40 %p 이상 급변한 것이 **41,135 회**였다.

리서치로 확보한 근거 (Codex `gpt-5.6-sol`, 읽기 전용, 2026-09-26):

- Bambu ABS 자료 기준 **Z 방향 충격강도가 XY 대비 약 81 % 낮다** (39.3 → 7.4 kJ/m²).
  인장강도 차이는 15 % 뿐인데 충격·연성 차이가 훨씬 크다 — 나사 조임은 국부 쐐기 하중이라
  여기에 걸린다.
- ABS 실험에서 층간 대기 0 → 20 초에 압축 항복 약 12 %, 층간 전단 관련 강도 약 25 % 감소.
- Bambu ABS 데이터시트 권장 팬 범위는 **0~80 %**. H2S 전용 프로파일만 돌출 구간 100 % 다.

### 고른 값과 그 실측

세 판을 명령줄로 잘라 비교했다 (뱀부 02.08.02.61).

```text
판      팬 평균   팬 급변(40%p)  모델 시간    무게      폭 0.44 초과 안쪽벽
지금     56.1 %      41,135 회   4h31m28s  126.94 g   0.2 %
판 B     18.4 %           6 회   4h31m28s  126.94 g   0.2 %   팬만
판 C     18.2 %           6 회   4h33m25s  127.64 g   0.2 %   팬 + 바닥 8 층  ← 채택
```

판 C 를 채택한다. 팬은 대가가 0 이고, 바닥 솔리드는 **+118 초 · +0.70 g** 로 판 지지력을
21 % → 41 % 로 올린다. 형상(벽 폭)은 세 판 모두 같다 — 팬과 바닥 층수는 벽을 안 바꾼다.

**`fan_cooling_layer_time` 은 손대지 않는다.** 30 → 15 로 내린 판을 먼저 시험했더니 평균 팬이
**3.7 %** 로 떨어져 과했다 (층 시간이 15 초를 넘는 구간에서 팬이 아예 안 돈다). 되돌렸다.

### 조립 쪽은 이 스프린트 범위 밖이다

넓은 와셔로 머리 면압을 분산하는 것이 가장 직접적인 대응이고, 지금 있는 부품에도 적용된다.
설정으로 할 수 있는 일이 아니므로 `notes.md` 에 적고 조건으로 재지 않는다.

## 리서치 소스

- ABS 층 접착·나사 체결 리서치 `<SCRATCH>/codex-layer-bond-out.txt` (출처 16 종)
- 나사 규격 조사 `<SCRATCH>/codex-screw-out.txt` (출처 10 종)
- `<KIT>/references/option-keys/bambu-02.08.02.61.tsv` · `orca-2.4.2.tsv` — 키 실재·종류 판정
- 세 판 슬라이스 결과 `<SCRATCH>/final/out` · `<SCRATCH>/fan-B/out` · `<SCRATCH>/fan-C/out`

## 범위 경계

```text
<OUT>      /Users/jackson/Hub/60_3D Print/Settings/h2-flipper-rear-exhaust-abs
<PETG>     /Users/jackson/Hub/60_3D Print/Settings/h2-flipper-rear-exhaust
<KIT>      bambu-kit/skills/bambu-print-profile
<SCRATCH>  /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/d204ea78-091c-4f5b-a8db-ec3ead359b73/scratchpad/exhaust
```

**고치는 것** — `<OUT>` 의 filament JSON 2 개 · process JSON 2 개 · 3mf 2 개 · zip 2 개 ·
`notes.md`. 아홉 파일 전부다.

**안 고치는 것** — `<PETG>` 폴더 전체, 레포의 어느 파일도 (이번은 킷 수정이 아니다),
`fan_cooling_layer_time` · `slow_down_layer_time` · 노즐 온도 · 층 높이 · 채움 밀도 · 벽 수 ·
모델 구멍 지름.

**앞선 두 스프린트가 정한 것은 건드리지 않는다** — `wall_generator` `classic` ·
`_wall_outer_block_ratio` `0.993` · `outer_wall_speed` `200` · 돌출 4 단 `60/30/10/10` ·
이음매 경사 `external`/`10`/`0`.

## 공통 전제

**(전제 1) 슬라이스 1 회 실행** — `<OUT>` 의 뱀부 3mf 를 사본으로 풀어
`Metadata/project_settings.config` 의 `enable_wrapping_detection` 만 `"0"` 으로 바꿔 다시 압축한
뒤 `BambuStudio --slice 1 --outputdir <폴더> <사본.3mf>` 를 돌린다. **그 외 어떤 값도 사본에서
바꾸지 않는다.** 산출물 3mf 자체는 이 치환을 담지 않는다.

**(전제 2) 팬 측정 규약** — `M106` 의 `S` 값을 255 로 나눠 백분율로 본다. 평균은 **압출 이동
길이로 가중**한다 (`G1` 직선과 `G2`·`G3` 호를 모두 세고, 호는 `I`·`J` 로 곡률을 구한다).
급변은 연속한 두 `M106` 사이 차이가 40 %p 이상인 횟수다.

**(전제 3) 키 실재와 프리셋 종류** — 옵션 목록 실측 (2026-09-26).

```text
키                     뱀부              오르카
fan_min_speed          filament          filament
fan_max_speed          filament          filament
overhang_fan_speed     filament          filament
pre_start_fan_time     filament          없음 (실재 0)   ← 오르카에 넣으면 조용히 버려진다
bottom_shell_layers    process           process
```

**(전제 4) 기준 상태** — 2026-09-26 18:25 실측. `<OUT>` 9 파일 sha256 앞 16 자. **아홉 개 전부
이번에 바뀐다.**

```text
process/...-bambu.json     31202c4280a70750
process/...-orca.json      1b9e86d630ae4c15
filament/...-bambu.json    3533d0e5a17a6156
filament/...-orca.json     07bc44c16624f730
..._baked-bambu.3mf        41e4c2e980ad9e78
..._baked-orca.3mf         39047b12a26131e3
...-abs-bambu.zip          b8aedb2571317bce
...-abs-orca.zip           6d3fe9dd645c0b80
notes.md                   ac77150fa73ed1d2
```

`<PETG>` 폴더 묶음 지문 `d422a04c00816cfa` — **그대로여야 한다.** 재는 법은 그 폴더 안에서
`find . -type f | sort | xargs shasum -a 256 | shasum -a 256 | cut -c1-16` 다 (`cd` 를 빼면
경로가 지문에 섞여 값이 달라진다 — 앞 스프린트 개정 A-01).

**(전제 5) 회귀 방지 조건** — `SC-05` · **`SK-04`** · **`SK-05`** · **`DG-04`** 는 구현 전에도
통과한다. 봉인 전 교차 진단이 지금 상태로 넷 다 통과함을 실측으로 확인했다 — 11 키는 이미 그
값이고, `fan_cooling_layer_time`·`slow_down_layer_time` 은 원래 안 쓰던 키라 이미 0 개이며,
고치기 전 판도 `return_code` 0 · 경고 없음이다. 이 넷은 「이번 변경이 멀쩡한 것을 깨뜨리지
않았는지」 재는 자리이며 **구현 의존 조건이 아니다.** 통과했다는 사실만으로 구현이 됐다는
근거로 쓰지 않는다.

구현 의존 조건은 나머지 열다섯이다 — `SK-01` `SK-02` `SK-03` `SC-01` `SC-02` `SC-03` `SC-04`
`ER-01` `ER-02` `ER-03` `ER-04` `AR-01` `AR-02` `AR-03` `AR-04` (`AR-05` 는 범위 조건).

## Skill

- [ ] SK-01: `<OUT>` 의 두 filament JSON 에 팬 키 **3 개**가 `fan_min_speed` `5` · `fan_max_speed` `25` · `overhang_fan_speed` `35` 로 들어 있다 [exact, enumerated] (근거: 배경의 판 C 실측. 측정: `python3` 로 두 파일의 세 키 값을 각각 출력해 비교. 값이 배열이면 모든 칸이 그 값인지 본다)
- [ ] SK-02: `pre_start_fan_time` `0` 이 **뱀부 filament JSON 에만** 있고 **오르카 filament JSON 에는 0 개**다 [exact] (근거: 전제 3 — 오르카 2.4.2 옵션 목록에 없는 키라 넣으면 조용히 버려지고 Phase 4.3 이 `모르는 키` 로 FAIL 한다. 측정: 두 파일에서 그 키의 존재와 값. 양성 대조: 오르카 사본에 그 키를 넣으면 Phase 4.3 이 `모르는 키` FAIL 을 내는지 확인하고 사본을 지운다)
- [ ] SK-03: 두 process JSON 의 `bottom_shell_layers` 가 `8` 이다 [exact, enumerated] (근거: 솔리드 0.68 → 1.32 mm, 판 3.2 mm 의 21 % → 41 %. 측정: 두 파일의 값)
- [ ] SK-04: 앞선 두 스프린트가 정한 값 **11 키**가 두 process JSON 에서 그대로다 — `wall_generator` `classic` · `_wall_outer_block_ratio` `0.993` · `_wall_budget_short_share` `0.933` · `outer_wall_speed` `200` · `overhang_1_4_speed` `60` · `overhang_2_4_speed` `30` · `overhang_3_4_speed` `10` · `overhang_4_4_speed` `10` · `seam_slope_type` `external` · `seam_slope_min_length` `10` · `seam_slope_conditional` `0` [exact, enumerated] (측정: 같은 명령의 11 키 값)
- [ ] SK-05: `fan_cooling_layer_time` 과 `slow_down_layer_time` 이 두 filament JSON 에 **0 개**다 [exact, enumerated] (근거: 30 → 15 로 내린 판이 평균 팬 3.7 % 로 과했다 — 배경. 부모값을 그대로 쓴다. 측정: 두 파일에서 두 키의 존재 여부)

## Script

- [ ] SC-01: 갱신한 4 개 JSON(process 2 · filament 2)을 슬라이서별로 Phase 4.3 검사에 돌려 `RESULT: PASS` 와 종료 코드 0 이 나온다 [exact] (측정: `<KIT>/SKILL.md` 의 추출 절차로 게이트를 뽑아 — 뽑은 줄 수와 `RESULT` 줄 수를 먼저 출력하고 빈 파일이면 멈춘다 — `TARGET_SLICER=bambu` 로 뱀부 2 개, `TARGET_SLICER=orca` 로 오르카 2 개)
- [ ] SC-02: 전제 1 의 1 회 실행에서 **압출 가중 평균 팬이 15 % 이상 22 % 이하**다 [exact] (근거: 판 C 실측 18.2 %. 15 % 미만이면 과냉각을 너무 줄여 돌출이 처질 위험, 22 % 초과면 층 접착 개선이 모자라다. 측정: 전제 2 규약. 알려진 답: `<SCRATCH>/final/out/plate_1.gcode` 는 56.1 %, `<SCRATCH>/fan-C/out/plate_1.gcode` 는 18.2 % 가 나온다 — 두 값이 안 나오면 스크립트가 틀린 것이니 조건 판정 전에 고친다. 음성 대조: 고치기 전 판(56.1 %)으로 재면 이 조건이 FAIL 해야 한다)
- [ ] SC-03: 같은 1 회 실행에서 **팬이 40 %p 이상 급변한 횟수가 100 회 미만**이다 [exact] (근거: 고치기 전 41,135 회 · 판 C 6 회. 급변은 층마다 냉각을 달라지게 해 수축 차이를 만든다. 측정: 전제 2 규약. 음성 대조: 고치기 전 판으로 재면 41,135 회가 나와 FAIL 해야 한다)
- [ ] SC-04: 같은 1 회 실행의 `result.json` 에서 `sliced_plates[0].main_predication` 이 16800 초(4 시간 40 분) 미만이고 `sliced_plates[0].filaments[*].total_used_g` 합이 126.0 g 이상 128.5 g 이하다 [exact] (근거: 판 C 실측 16406 초 · 127.64 g. 바닥 층 추가로 무게가 0.70 g 늘어 상한을 127.5 → 128.5 로 둔다. 측정: 두 필드 — 둘 다 최상위가 아니라 판 배열 안에 있다)
- [ ] SC-05: 같은 1 회 실행이 낸 `plate_1.gcode` 를 갱신한 process · filament JSON 과 대조했을 때 `MISMATCH` 가 0 건이다 [exact] (측정: `<KIT>/SKILL.md` Phase 4.4 의 대조 스크립트를 그 문서에 적힌 대로 뽑아 실행 — 종료 코드 0. 양성 대조: 사본의 `fan_max_speed` 를 `60` 으로 되돌리면 `MISMATCH` 가 나오는지 확인한다)

## Error

- [ ] ER-01: `<OUT>/notes.md` 에 이번 실패의 원인이 적혀 있다 — 문자열 `3.72`, `0.68`, `81%`, `56.1` 이 **모두** 있다 [exact, enumerated] (근거: 구멍 지름 · 바닥 솔리드 두께 · Z 방향 충격강도 차이 · 고치기 전 평균 팬. 측정: **`grep -F` 로** 네 문자열 각각 센다 — `grep` 의 `.` 은 아무 글자나 대신하므로 `3.72` 가 이미 문서에 있는 `3772`(허공 구간 길이) 세 건에 걸린다. 봉인 전 교차 진단이 이 오탐을 잡았고 실측으로 확인했다(`grep -c` 3 건 / `grep -Fc` 0 건). `81` 단독은 `181`·`810` 같은 무관한 값에도 걸리므로 `%` 를 붙여 좁힌다)
- [ ] ER-02: `<OUT>/notes.md` 에 **와셔 안내**가 적혀 있다 — `와셔` 와 `머리` 가 같은 문단(빈 줄로 구분된 블록)에 있는 블록이 1 개 이상이다 [structural] (근거: 설정으로 못 하는 대응이고 지금 있는 부품에도 적용된다. 측정: `awk` 로 빈 줄 기준 블록을 나눠 센다)
- [ ] ER-03: `<OUT>/notes.md` 에 나사 규격이 **확정되지 않았다는 사실**이 적혀 있다 — `HB3x20` 과 `BT3` 가 모두 있다 [exact, enumerated] (근거: 공식 목록에 `HB3x20` 이 없고 공식 문서끼리 `BT3-20` / `BTG 3×20` 로 상충한다. 확정한 것처럼 적으면 다음에 틀린 전제로 간다. 측정: 두 문자열 각각 grep)
- [ ] ER-04: `<OUT>/notes.md` 에 `fan_cooling_layer_time` 을 손대지 않은 이유가 적혀 있다 — 그 키와 `3.7%` 가 같은 문단(빈 줄로 구분된 블록)에 있는 블록이 1 개 이상이다 [structural] (근거: 30 → 15 로 내린 판이 평균 팬 3.7 % 로 과했다. 측정: `awk` 로 빈 줄 기준 블록을 나누고 **고정 문자열 비교**(`index()`)로 센다 — 정규식으로 `3.7` 을 찾으면 `3772` 에 걸린다. 그래서 `%` 를 붙인 형태로 요구한다)

## Architecture

- [ ] AR-01: `<OUT>` 의 파일 9 개가 모두 존재하고, 전제 4 의 **아홉 지문이 전부 달라졌다** [exact, enumerated] (측정: 9 경로에 `test -f` + 9 개 지문을 기준값과 각각 비교. 하나라도 같으면 그 파일을 갱신하지 않은 것이니 FAIL)
- [ ] AR-02: `<PETG>` 폴더 묶음 지문이 `d422a04c00816cfa` 로 그대로다 [exact] (측정: 전제 4 에 적은 명령을 그 폴더 안에서 실행. 양성 대조: 그 폴더에 빈 임시 파일을 하나 만들면 지문이 달라지는지 확인한 뒤 지운다)
- [ ] AR-03: 두 3mf 의 `Metadata/project_settings.config` 에 팬 키 3 개와 `bottom_shell_layers` 가 갱신된 값으로 들어 있다 [exact, enumerated] (근거: 3mf 를 열어 바로 자르는 것이 권장 경로다 — JSON 만 고치면 3mf 는 옛 값으로 자른다. 측정: 두 3mf 를 열어 `fan_min_speed` `fan_max_speed` `overhang_fan_speed` `bottom_shell_layers` 네 키 값을 각각 출력. **뱀부 3mf 에는 `pre_start_fan_time` `0` 도 있어야 하고, 오르카 3mf 에는 그 키가 0 개여야 한다** — 오르카 2.4.2 옵션 목록에 없는 키라 「부모값」 이라는 경우는 성립하지 않는다. 봉인 전 교차 진단이 이 문구를 짚었다)
- [ ] AR-04: 두 zip 이 각각 `process/` 와 `filament/` 를 갖고 **그 안의 네 파일이 모두** `<OUT>` 의 같은 이름 파일과 내용이 같다 [exact, enumerated] (측정: `unzip -l` 로 구조 + `unzip -p` 로 꺼낸 네 파일의 `sha256` 을 폴더 파일과 각각 비교)
- [ ] AR-05: Given — 구현 완료 시점. 작업 폴더 `bambu-wall-gen-shape` 에서 `git status --porcelain` 의 변경이 **아래 화이트리스트 안에만** 있다 — `.harness/sprint-contract-h2-flipper-rear-exhaust-abs-fan-screw.md` · `.harness/sprint-feedback-h2-flipper-rear-exhaust-abs-fan-screw.md` · `.harness/sprint-amendments-h2-flipper-rear-exhaust-abs-fan-screw.md` · `.harness/sprint-contract-bambu-kit-frag-ratio-counts.md` [exact, enumerated] (근거: 이번은 레포 파일을 고치지 않는다 — 산출물이 전부 레포 밖이다. 네 번째는 이 세션이 먼저 선점해 둔 **다른 계약**이며 봉인 전 상태로 멈춰 있다. **제외 경로**: `00000.log` · `.harness/.meta/` 하위 · `.DS_Store`. 측정: `git status --porcelain` 목록에서 제외 경로를 뺀 뒤 화이트리스트 4 경로와 `comm` 으로 대조해 밖의 항목이 0 개인지 본다)

## Anti-patterns

- [ ] AP-00: N/A (대상이 레포 밖 출력 설정 파일 — `project.yaml` 의 AP-01~AP-04 는 레포 플러그인 파일 전용이고 이번 변경 파일과 교집합 0 개)

## Reusability

- [ ] RE-01: N/A (산출물이 설정 JSON · 문서 · 3mf · zip 뿐 — 재사용 단위 코드 0 개. 이번은 킷 파일을 고치지 않으므로 문서에 박힌 코드도 안 바뀐다)
- [ ] RE-02: `<OUT>/notes.md` 에 이번 판단의 근거가 인용돼 있다 — `Z 방향` 과 `충격강도` 가 같은 문단에 있는 블록이 1 개 이상이다 [structural] (근거: `surface-recipes.md` 단독 인용은 앞선 스프린트가 남긴 것이 이미 여러 건 있어 이번에 안 고쳐도 통과한다 — 앞 계약 개정에서 짚은 함정. 측정: `awk` 로 블록을 나눠 센다)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개)
- [ ] DG-02: N/A (레포 파일을 하나도 고치지 않으므로 편집기 진단 대상 변경이 0 개다. 앞 스프린트 개정 A-02 가 「마크다운은 진단 대상이 아니다」를 틀린 사유로 짚었으나, 이번은 마크다운 자체를 안 고친다 — `git status` 로 레포 변경이 계약 파일 넷뿐임을 AR-05 가 확인한다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` — 이번 변경 파일과 교집합 0 개)
- [ ] DG-04: 전제 1 의 1 회 실행에서 `result.json` 의 `return_code`(최상위)가 0 이고 `sliced_plates[0].warning_message` 가 빈 문자열이다 [exact] (측정: 두 필드 — 서로 다른 중첩 깊이에 있다)
