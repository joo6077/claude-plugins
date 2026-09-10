---
feature: "bambu-kit surface-first geometry class"
slug: bambu-kit-surface-first-geometry-class
created: "2026-09-08 11:52"
complexity: "복잡"
conditions: 26
status: done
owner_session: 1778a3e2-770b-4a28-9989-61c31f9c4ecc
conditions_digest: sha256:65d829d758d1fc9e
locked_at: "2026-09-08 11:56"
---

## 배경

bambu-kit 의 surface-first 정책은 **부품 형상을 구분하지 않는다.** `surface-recipes.md` §3 속도표는
소재 축만 갖고 (`:104-133`), `SKILL.md` Phase 3 는 그 표를 유량비 게이트로 감싸 큰 평면이든 얇은
래티스든 똑같이 외벽 `30` 과 인접 4 키를 깎는다 (`:840-870`, `:986-989`). 형상 6 종 트리에 "얇은 벽 /
미세 디테일" 분기가 있지만 (`:966`) seam · scarf · `wall_loops` 만 다루고 **속도 규칙이 없다.**

2026-09-07 래티스 통(AMS 2 Pro Lattice Dry Pods, ABS, `0.12mm High Quality @BBL H2S` 상속) 실측:
Side Container 는 레이어당 루프 20~52 개가 **전부 둘레 30 mm 미만**(최대 20.59 mm)인 스트럿 단면이고,
Funnel 은 루프 2 개(91.72~175.47 mm)다. 같은 surface-first 값이 두 부품에 그대로 들어갔다. 워크플로우
25 에이전트 진단 결과 결함 원인은 flow · PA · Z · 워핑 · 습기가 아니라 **속도값과 냉각 문턱**이었다 —
래티스의 병목은 유량이 아니라 **열 방출 시간**이라 느릴수록 나빠지고, 층시간 `8.6~14.6 s` 가 ABS 실효
`slow_down_layer_time 12` 를 주기적으로 가로질렀으며, 사선 스트럿의 미지지율(20°=10.4 % / 40°=24.0 %)이
ABS 실효 `overhang_fan_threshold 25%` 에 안 걸려 `overhang_fan_speed 100` 이 구조적으로 발동하지 못했다.

그런데 그 보상 경로가 정책으로 막혀 있다. `SKILL.md:876` "fan/cooling 안 건드림 — base에 위임",
`failure-recipes.md:158`, `user-preferences.md:17` 세 곳이 냉각을 자동 범위 밖으로 둔다. 한편
`user-preferences.md:42-43` 은 *"속도를 낮추는 것이 품질에 기여한다는 근거가 그 소재·형상에 있을 때만
낮춘다"* 고 선언한다 — **선언은 형상 의존인데 그것을 실행하는 절차·측정·게이트가 없다.** 이것이 결함이다.

같은 세션에서 키 스코프도 두 번 틀렸다 (`overhang_fan_threshold` 를 process 에 넣으려 했고, enum 이름을
Orca 것으로 읽었다). 설치본 실측: 냉각 키 10 종이 **process 0 / filament 146~1218** — process 에 넣으면
조용히 무시된다. Phase 4.3 게이트는 이 스코프를 검사하지 않는다 (`:1125-1290`).

## GAP 분석

Pre-Edit Audit — 대상 파일을 실제로 열어 확인한 갭. 증거 열이 빈 행은 없다.

| 대상 | Read 증거 | 갭 | 조건 |
| --- | --- | --- | --- |
| `references/surface-recipes.md` | `:28` 속도 무시 · `:104-133` §3 표 · `:211-216` §6.5 열 축적 | 형상 축 부재. 부작용은 적고 기구는 없음 | SK-01 SK-02 |
| `SKILL.md` Phase 3 | `:711` 튜닝 목록 `outer_wall_speed (소재별)` · `:876` 냉각 위임 · `:929-993` surface-first 블록 · `:961-967` 형상 트리 | 얇은 벽 분기에 속도 규칙 없음. 냉각 예외 없음 | SK-02 SK-03 |
| `SKILL.md` Phase 1.0 · vase 판정 | `:64` bbox 파서 · `:815` "Z 사다리로 잘라 루프 수를 세어" | 루프 둘레 측정 코드가 본문에 없다 — 직전 세션은 즉석 스크립트로 쟀다 (notes.md §1.2.2) | SK-04 SC-04 |
| `SKILL.md` Phase 4.3 게이트 | `:1125-1290` · `_scarf_loop_circumference_mm` 소비 `:1237-1248` | 형상 입력 없음 · 키 스코프 검사 없음. `_` 접두 주석 키 선례 있음 | SC-01 SC-02 ER-01 ER-02 |
| `SKILL.md` Gotcha | `:1370-1402` | 형상 클래스 · 스코프 항목 없음 | SK-05 |
| `references/bambu-fields-baseline.md` | `:289-305` §10.3 aux fan 2 키만 | 냉각 보상 키 5 종 부재 · 스코프 열 없음 | AR-03 |
| `references/user-preferences.md` | `:17` 팬 자동 X · `:42-43` 형상 근거 선언 | 수정하지 않는다 — 예외는 "확인 후" 라 선언과 모순 없음 | (범위 밖) |
| `docs/bambu-kit/surface-recipes.html` | `:308` PETG `20-35` · `:317` `0.006-0.010` | md 정본(`50-70` · 기본값 유지)과 **이미 불일치** | AR-01 AR-02 |
| `docs/bambu-kit/bambu-print-profile.html` | `:425` "retraction / fan / cooling 관련 모든 필드 ×" | 냉각 예외 미반영 예정 | AR-01 |
| Bambu user preset | `.../user/671408350/process/AMS 2 Pro Dry Pods FUNNEL - ABS 0.12mm.json` 존재 · `_scarf_loop_circumference_mm` 0 건 | import 는 `_` 키를 거부하지 않고 버린다 | AR-05 |

구현 옵션 대조 (선택: **A**):

| 옵션 | 내용 | 장점 | 단점 |
| --- | --- | --- | --- |
| **A** 형상 클래스 축 + 측정 + 게이트 | `_geometry_class` 를 측정으로 정하고 `thin` 이면 속도 하향 생략, 냉각은 확인 후 filament 1 키, 게이트가 클래스·스코프 검사 | 결함의 세 층(정책·측정·검증)을 모두 닫음. 기존 형상 트리 4 번과 정합 | 파일 6 + 픽스처 7 |
| B 냉각 키만 항상 추가 | 모든 surface-first 에 `overhang_fan_threshold 10%` | 1 파일 | 형상을 여전히 구분하지 않음. 큰 평면에서 과냉각 부작용 |
| C 사용자에게 매번 형상을 묻기 | 질문 1 줄 추가 | 코드 0 | 측정 없는 자기신고. 이번 세션이 틀린 것과 같은 방식으로 다시 틀림 |

## 리서치 소스

- 설치본 실측 (앱 `02.08.02.61` · 번들 `02.08.00.06`, `/Applications/BambuStudio.app/Contents/Resources/profiles/BBL` 과 `~/Library/Application Support/BambuStudio/system/BBL` 두 경로 동일): `overhang_fan_threshold` process 0 / filament 146 · `overhang_fan_speed` 0/165 · `fan_cooling_layer_time` 0/364 · `slow_down_layer_time` 0/553 · `slow_down_min_speed` 0/1218 · `fan_min_speed` 0/552 · `fan_max_speed` 0/562 · `additional_cooling_fan_speed` 0/293 · `outer_wall_speed` 180/0 · `overhang_1_4_speed` 147/0
- 소재 부모 실효값: `Bambu ABS @BBL H2S` = threshold `25%` · overhang fan `100` · `fan_cooling_layer_time 30` · `slow_down_layer_time 12` · fan `10~60`. `Bambu ABS-GF @BBL H2S` 와 `Bambu PETG HF @BBL H2S` 는 threshold `10%`, `Bambu PLA Basic @BBL H2S` 는 `50%`
- process 부모 실효값: `0.12mm High Quality @BBL H2S` = `outer_wall_speed 60` · `inner_wall_speed 150` · `overhang_1_4_speed 60` · `bridge_speed 50` · `line_width 0.42`
- 래티스 실측: `/Users/jackson/Hub/60_3D Print/Settings/ams-2-pro-lattice-dry-pods/notes.md` §1.2.2 루프 둘레 표 · 전달물 `LatticePods-FANFIX.zip` (filament `overhang_fan_threshold 10%` 만 변경)
- 핸드오프: `.harness/handoff/2026-09-08-0100.md` (feat/howto-kit 브랜치) §In Progress · §Queued

## 범위 경계

- 공통 전제 — 아래 조건의 `SKILL.md` 는 `bambu-kit/skills/bambu-print-profile/SKILL.md`, `surface-recipes.md` 와 `bambu-fields-baseline.md` 는 `bambu-kit/skills/bambu-print-profile/references/` 아래 파일이다. 게이트 실행은 `CONTRACT_ROOT` (격리 워크트리) 기준 상대경로다.
- **추출 규약** — 게이트는 `SKILL.md` 의 Phase 4.3 코드 블록을 `awk '/^python3 - <output_dir>/{p=1;next} /^PY$/{p=0} p'` 로 뽑아 **편집 없이** `python3 <추출파일> <픽스처...>` 로 실행한다. 분류기는 첫 줄 주석 `bambu-kit geometry-class probe` 부터 다음 `PY` 줄 직전까지를 같은 방식으로 뽑아 `python3 <추출파일> <3mf> <오브젝트명>...` 으로 실행한다. 추출 결과가 0 줄이면 그 조건은 FAIL 이다 (빈 출력은 PASS 가 아니다).
- 픽스처 7 개는 `bambu-kit/evals/gate-fixtures/` 에 둔다: `process-scope-filament-key.json` · `filament-scope-process-key.json` · `process-thin-speed-lowered.json` · `process-thin-baseline.json` · `filament-lattice-fanfix.json` · `process-speed-without-class.json` · `process-class-unknown.json`. 픽스처는 `inherits` 를 실존 시스템 프리셋(`0.12mm High Quality @BBL H2S` / `Bambu ABS @BBL H2S`)으로 둔다.
- 형상 클래스는 기존 형상 6 종 트리의 4 번 "얇은 벽 / 미세 디테일" 을 **측정으로 트리거하는 것**이지 새 분류 체계가 아니다. 값은 `planar` · `thin` 2 종으로 고정한다.
- `thin` 의 냉각 보상은 filament 스코프 `overhang_fan_threshold` **1 키**, 사용자 확인 후에만이다. `user-preferences.md` §1 "팬 자동으로 건드리지 않는다" 는 그대로 참이므로 그 파일은 수정하지 않는다. `fan_cooling_layer_time` · `slow_down_layer_time` 은 키 정본에 스코프만 기록하고 자동 결정 대상에 넣지 않는다.
- 이번 스프린트가 다루지 않는 것: 3.36 mm 주기 돌출(`slow_down_layer_time` 문턱 재배치 — 실물 A/B 이후) · `overhang_1_4_speed` 센티넬 `0` · `failure-recipes.md` 에 L4 실패 모드 신설 · STL 입력의 단면 측정(3mf 만) · 플러그인 릴리스.
- `docs/bambu-kit/surface-recipes.html` §3 의 stale 값 2 건(AR-02)은 이번에 손대는 같은 표 안의 것이라 함께 정합한다. Pre-Edit Audit 에서 발견한 기존 갭이며 의도적 범위 포함이다.
- 변경 범위는 정확히 13 경로로 한정된다 (수정 6 + 신규 7). 열거는 AR-04 측정 절 한 곳에서만 한다.
- 커버리지 해소: AR-01 — 3 경로를 조건 산문과 측정 절에 동일 백틱 표기로 열거했다.
- 커버리지 해소: SC-03 — 픽스처 2 파일명을 산문과 측정 절 양쪽에 같은 표기로 적었다.

## 회귀 게이트

- 음성 대조가 붙은 조건(SC-01 SC-02 SC-03 SC-04 ER-02 ER-03)은 해당 구현 지점을 무력화했을 때 실제로 FAIL 로 뒤집히는지를 평가자가 1 회 확인한다. 뒤집히지 않으면 그 측정은 oracle 이 아니다.
- 기존 `ENUM_ALLOW` · `FORBIDDEN` · 유량비 · scarf 길이 검사는 그대로 살아 있어야 한다 — `process-thin-baseline.json` 이 PASS 하는 것(SC-03)과 `validate-plugin` exit 0 (SC-05) 이 회귀 방어선이다.

## Skill

- [ ] SK-01: 정책 정본 `surface-recipes.md` 에 형상 클래스 축이 한 섹션으로 정의된다 — 클래스 값 2 종 `planar` · `thin`, 판정 지표(레이어 단면 루프 둘레 `30` mm 미만 비율의 3 높이 중앙값이 `0.5` 이상이면 `thin`), 근거(2026-09-07 래티스 실측 + seam-recipes §2.2 와 같은 30 mm 임계) [exact, enumerated] (측정: 대상 `surface-recipes.md` 에서 `grep -cE '^##+ .*형상 클래스'` == 1 이고 그 섹션 본문에서 `planar` · `thin` · `_geometry_class` · `30` · `0.5` 각 `grep -c` >= 1)
- [ ] SK-02: `thin` 클래스에서는 surface-first 속도 하향(`outer_wall_speed` + 인접 4 키 + `top_surface_speed`)을 적용하지 않고 부모 process 실효값을 그대로 둔다는 규칙이 3 표면에 있다 — (a) `surface-recipes.md` §3 (b) `SKILL.md` Phase 3 "Surface-first 모드" 블록 (c) `SKILL.md` process JSON 튜닝 정책 목록의 `outer_wall_speed` 항목 [exact, enumerated] (측정: `grep -nE 'thin.*outer_wall_speed|outer_wall_speed.*thin'` 가 `surface-recipes.md` 에서 >= 1, `SKILL.md` 에서 >= 2 이고 그 매치 줄 번호가 (b) 블록 범위와 (c) 목록 범위에 각 1 건 이상)
- [ ] SK-03: `SKILL.md` 의 냉각 위임 규칙 줄("fan/cooling 안 건드림 — base에 위임")에 `thin` 예외가 붙는다 — 예외 범위는 filament 스코프 키 `overhang_fan_threshold` 1 키, 사용자 확인 후에만, 값 근거는 설치본 `Bambu ABS-GF @BBL H2S` · `Bambu PETG HF @BBL H2S` 실효값 `10%` [exact, enumerated] (측정: `grep -nE 'fan/cooling.*위임' SKILL.md` 매치 줄부터 +4 줄 안에 `thin` · `overhang_fan_threshold` · `확인` · `10%` 각 >= 1)
- [ ] SK-04: 형상 클래스 측정 코드가 `SKILL.md` 에 실행 가능한 python 블록으로 존재한다 — 3mf 메시에 빌드 변환을 적용한 뒤 높이 25/50/75 % 3 지점에서 절단해 오브젝트별 루프 수 · 둘레 · 30 mm 미만 비율 · `_geometry_class` 를 JSON 으로 출력하고, 루프 0 인 결과는 non-zero exit 로 끝낸다 [structural] (측정: 블록 첫 줄 주석 `bambu-kit geometry-class probe` 1 건, 블록 안에 `_geometry_class` · `0.25` · `0.75` 각 >= 1 이고 `sys.exit(` 또는 `raise` >= 1; 실행 판정은 SC-04)
- [ ] SK-05: Gotcha 체크리스트에 두 항목이 추가된다 — (a) `_geometry_class` 를 process JSON 에 기록했는지 (b) 키를 넣기 전에 설치본 스코프(process/filament)를 확인했는지 [structural, enumerated] (측정: `## Gotcha 체크리스트` 섹션 안에서 `_geometry_class` 포함 줄 >= 1, `스코프` 포함 줄 >= 1)

## Script

- [ ] SC-01: Phase 4.3 게이트가 키 스코프를 설치본 시스템 프로파일에서 도출해 검사한다 — 픽스처 `process-scope-filament-key.json`(process 에 `overhang_fan_threshold`) 과 `filament-scope-process-key.json`(filament 에 `outer_wall_speed`) 이 각각 `RESULT: FAIL` 과 exit 1 [goal, enumerated] (측정: §추출 규약으로 게이트를 `process-scope-filament-key.json` · `filament-scope-process-key.json` 각각에 실행, 출력과 `echo $?` 인용) 음성 대조: 스코프 검사 블록을 삭제하면 두 픽스처가 `RESULT: PASS` 로 통과한다
- [ ] SC-02: 게이트가 형상 클래스와 속도의 모순을 잡는다 — 픽스처 `process-thin-speed-lowered.json`(`_geometry_class` `thin` + `outer_wall_speed` `30`, 부모 `0.12mm High Quality @BBL H2S` 실효값 `60`) 이 `RESULT: FAIL` 과 exit 1 [goal] (측정: 게이트 실행 출력과 `echo $?` 인용) 음성 대조: 클래스 검사 블록을 삭제하면 같은 픽스처가 PASS 한다
- [ ] SC-03: 정상 산출물은 통과한다 — 픽스처 `process-thin-baseline.json`(`thin`, 속도 키 없음) 과 `filament-lattice-fanfix.json`(`overhang_fan_threshold` `10%`, 전달물 `Bambu ABS - Lattice Pods.json` 의 사본) 이 각각 `RESULT: PASS` 와 exit 0 [goal, enumerated] (측정: 게이트를 `process-thin-baseline.json` · `filament-lattice-fanfix.json` 각각에 실행, 출력과 `echo $?` 인용) 음성 대조: 전자에 `"outer_wall_speed": ["30","30","30"]` 을 추가하면 FAIL 한다
- [ ] SC-04: 분류기가 실물에서 형상을 가른다 — `/Users/jackson/Hub/60_3D Print/Settings/ams-2-pro-lattice-dry-pods/AMS 2 Pro Lattice Dry Pods VERSION 2 - All Materials.3mf` 의 오브젝트 `Side Container LHS V1` 이 `thin`, `Funnel V1` 이 `planar` 로 출력된다 [goal, enumerated] (측정: SK-04 블록을 §추출 규약으로 추출해 두 오브젝트명을 인자로 실행, 출력 JSON 의 `_geometry_class` 값 인용) 음성 대조: 둘레 임계 `30` 을 `3` 으로 바꾸면 `Side Container LHS V1` 이 `planar` 로 뒤집힌다
- [ ] SC-05: `python3 scripts/validate-plugin.py bambu-kit` 이 exit 0 으로 통과한다 [goal] (측정: 명령 실행 후 `echo $?` == 0)

## Error

- [ ] ER-01: 스코프 FAIL 메시지 1 줄이 (a) 키 이름 (b) 그 파일의 `type` (c) 설치본에서 그 키가 발견된 스코프 3 요소를 모두 담는다 [exact, enumerated] (측정: SC-01 의 `process-scope-filament-key.json` 출력 FAIL 줄 1 개에 `overhang_fan_threshold` · `process` · `filament` 3 토큰 존재)
- [ ] ER-02: 클래스 결측·오염을 FAIL 로 잡고 원인을 지목한다 — `process-speed-without-class.json`(`outer_wall_speed` 있음 + `_geometry_class` 없음) 과 `process-class-unknown.json`(`_geometry_class` 가 `lattice`) 이 각각 `RESULT: FAIL` 하고 FAIL 줄에 `_geometry_class` 와 허용값 `planar` · `thin` 이 나온다 [exact, enumerated] (측정: 게이트를 `process-speed-without-class.json` · `process-class-unknown.json` 각각에 실행, FAIL 줄 인용) 음성 대조: 클래스 검사 블록을 삭제하면 두 픽스처가 PASS 한다
- [ ] ER-03: 시스템 프로파일 경로가 없으면 스코프·클래스 검사는 FAIL 이 아니라 `[미검증]` 으로 강등된다 [goal] (측정: `env HOME=<빈 임시 디렉토리>` 로 `process-scope-filament-key.json` 에 게이트 실행 — 출력에 `[미검증]` 줄 >= 1 이고 `스코프` 를 담은 FAIL 줄 0) 음성 대조: 미지 스코프를 `[미검증]` 대신 FAIL 로 바꾸면 이 실행이 FAIL 한다

## Architecture

- [ ] AR-01: 파생 발행물 3 파일 `docs/bambu-kit/surface-recipes.html` · `docs/bambu-kit/bambu-print-profile.html` · `docs/bambu-kit/bambu-fields-baseline.html` 이 각각 `_geometry_class` 를 1 건 이상 담는다 [exact, enumerated] (측정: `docs/bambu-kit/surface-recipes.html` `docs/bambu-kit/bambu-print-profile.html` `docs/bambu-kit/bambu-fields-baseline.html` 각각 `grep -c '_geometry_class'` >= 1)
- [ ] AR-02: `docs/bambu-kit/surface-recipes.html` §3 의 정본 불일치 2 건이 해소된다 — PETG HF 외벽 속도 `20-35` 와 `resolution` 권장 `0.006-0.010` 이 0 건이고 정본값 `50-70` 이 1 건 이상 [exact, enumerated] (측정: 대상 `docs/bambu-kit/surface-recipes.html`, 값 토큰 `20-35` · `0.006-0.010` · `50-70` 각각 `grep -c` 로 세어 순서대로 == 0 · == 0 · >= 1)
- [ ] AR-03: 키 정본 `bambu-fields-baseline.md` 에 냉각 보상 키 5 종 `overhang_fan_threshold` · `overhang_fan_speed` · `fan_cooling_layer_time` · `slow_down_layer_time` · `slow_down_min_speed` 이 filament 스코프 표기와 설치본 실측 버전(`02.08.02.61` 또는 `02.08.00.06`)과 함께 한 표에 있다 [exact, enumerated] (측정: 대상 `bambu-fields-baseline.md` 에서 5 키 각각 `grep -c` >= 1, 그 표가 속한 섹션에 `filament` 와 `02.08.02.61`|`02.08.00.06` 각 >= 1)
- [ ] AR-04: 변경 범위가 정확히 13 경로로 한정된다 [exact, enumerated] (Given: 격리 워크트리 브랜치 `worktree-bambu-surface-first-geometry`, baseline 커밋 `4fb1382`, 커밋 직전 working tree, 다른 세션의 동시 편집 없음 · 측정: `git status --porcelain -uall -- bambu-kit docs/bambu-kit` 출력이 다음 13 경로와 정확히 일치 — 수정 `bambu-kit/skills/bambu-print-profile/SKILL.md` `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` `docs/bambu-kit/surface-recipes.html` `docs/bambu-kit/bambu-print-profile.html` `docs/bambu-kit/bambu-fields-baseline.html`, 신규 `bambu-kit/evals/gate-fixtures/process-scope-filament-key.json` `bambu-kit/evals/gate-fixtures/filament-scope-process-key.json` `bambu-kit/evals/gate-fixtures/process-thin-speed-lowered.json` `bambu-kit/evals/gate-fixtures/process-thin-baseline.json` `bambu-kit/evals/gate-fixtures/filament-lattice-fanfix.json` `bambu-kit/evals/gate-fixtures/process-speed-without-class.json` `bambu-kit/evals/gate-fixtures/process-class-unknown.json`. baseline: 계약 작성 시점 이 명령 출력 0 행)
- [ ] AR-05: 소비면 — Bambu Studio import 가 `_` 접두 주석 키를 거부하지 않는다는 근거가 평가 시점에 실재한다: `/Users/jackson/Library/Application Support/BambuStudio/user/671408350/process/AMS 2 Pro Dry Pods FUNNEL - ABS 0.12mm.json` 이 존재하고(import 성공) 그 파일에서 `_scarf_loop_circumference_mm` 가 0 건이다(버림, 거부 아님) [goal] (측정: `ls` 로 존재 확인 + `grep -c '_scarf_loop_circumference_mm'` == 0 인용)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 실행 — §추출 규약으로 뽑은 게이트를 픽스처 7 개 전부에, 분류기를 SC-04 의 실물 3mf 에 실행했을 때 python `Traceback` 이 0 건이다 (측정: 두 실행의 stderr 를 인용, `grep -c Traceback` == 0)
