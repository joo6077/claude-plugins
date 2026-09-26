---
feature: "H2 Flipper 배기관 ABS — 벽 생성기를 형상에 맞춰 되돌리고 킷 규칙에 파편화 지표를 넣는다"
slug: h2-flipper-rear-exhaust-abs-wall-gen
created: "2026-09-26 10:40"
complexity: "중간"
conditions: 31
status: active
owner_session: d204ea78-091c-4f5b-a8db-ec3ead359b73
conditions_digest: sha256:a6bb133d64d43f5c
locked_at: "2026-09-26 11:43"
---

## 배경

사용자가 이 설정으로 실제 출력한 결과 사진 2 장을 제출했다 — 꺾이는 구간의 **안쪽과 바깥쪽 같은
높이**에서 표면이 거칠고 층 선이 굵고 불규칙하며 거스러미가 일었다. 사용자 보고: "너가 준대로
한건데?? 뱀부랩".

**보낸 G-code 로 확인해 내 설정임이 확정됐다.** `$(getconf DARWIN_USER_TEMP_DIR)/bamboo_model/Fri_Sep_25/22_45_21#61719#53/Metadata/.61719.0.gcode`
(Sep 25 23:56 · 44.9 MB · `print_settings_id = H2 Flipper Exhaust ABS 0.16mm (bambu)`) 에서
내가 넣은 값 10 개가 전부 그대로 나왔고 무게 126.97 g 이 예측 범위와 맞았다.

**원인은 내가 `wall_generator` 를 `classic` → `arachne` 로 바꾼 것이다.** 갭필 시간을 없애려고
바꿨는데, 갭필 **피처 시간만 보고 전체 시간을 보지 않았다.** 같은 3mf 를 두 생성기로 명령줄 재슬라이스한
실측 (뱀부 02.08.02.61, 2026-09-26):

```text
                     굵은 안쪽벽(0.44mm 초과)   갭필        출력 시간      파일 크기
arachne (보낸 것)     140.91 m  (11.3%)        0.02 m    4h 50m 48s    46.8 MB
classic (되돌림)        3.01 m  ( 0.2%)      117.84 m    4h 31m 57s    25.0 MB
```

`arachne` 가 **표면도 나쁘고 시간도 19 분 길다 — 순손실이다.** 안쪽벽이 굵어지면 외벽을 밖으로
밀어 겉면에 요철로 드러난다. 갭필은 외벽 뒤에 들어가 숨는다 (제작자 판 실측: 갭필 블록 1660 개 중
바로 앞 피처가 `Outer wall` 790 · 바로 뒤가 `Inner wall` 759 — 외벽과 안쪽벽 **사이** 틈이다).

굵어진 안쪽벽의 높이 분포가 사용자가 말한 자리와 맞는다 — Z 40~49 mm 22.4% · Z 50~59 mm 18.1%
(아래 꺾임), Z 0~19 mm 2.6~5.3% (매끈한 직선 구간). 제작자 원본(`classic`)은 전 구간 0.0% 다.

### 킷 규칙이 이 형상에서 빗나간다

`SKILL.md` Phase 4.3 벽 예산 검사가 `_wall_budget_short_share >= 0.10` 이고 `classic` 이면 FAIL 한다
(실측: 이 배기관을 `classic` 으로 바꾼 사본이 양쪽 슬라이서에서 `FAIL · exit 1`). 그 규칙의 근거는
**평면·격자 부품** 실측인데, 세 사례를 같은 척도로 놓으면 갈리는 축이 벽 예산 비율이 아니다.

| 사례 | 형상 | 벽 예산 부족 | `classic` 외벽 블록 | `arachne` 외벽 블록 | 파편화 배수 | 맞는 선택 |
| --- | --- | --- | --- | --- | --- | --- |
| 래티스 통 (2026-09-14) | 스트럿 격자 | 56~90% | 18,267 | 9,875 | **1.850** | `arachne` |
| H2 AMS Flipper (2026-09-19) | 평면 + 구멍 21 개 | 71.9~72.1% | 기록 없음 | 기록 없음 | 미측정 | `arachne` |
| **H2 배기관 (2026-09-26)** | **곡면 꺾인 관** | **93.3%** | **1,202** | **1,211** | **0.993** | **`classic`** |

배기관은 벽 예산 부족이 **가장 심한데** `classic` 이 정답이다. 갈리는 축은 **`classic` 이 외벽을
조각내는지**다. 격자·구멍 많은 평면은 벽이 못 들어가는 자리가 외벽 경로 **중간**에 나타나 외벽이
조각나고 이음매 후보지가 두 배가 된다. 곡면 관은 벽 두께가 연속적으로 줄어 외벽이 온전한 고리로
남고 갭필이 그 안쪽에 들어간다.

그래서 검사를 **면제하지 않고 측정을 요구하는 방향**으로 고친다 — `classic` + 벽 예산 부족이면
파편화 배수 기록을 **요구**하고, 기록이 없으면 지금처럼 FAIL 한다.

## 리서치 소스

- `<KIT>/references/surface-recipes.md` §2.8 — 현행 벽 예산 규칙과 두 사례 실측표
- `<KIT>/SKILL.md:1756-1762` — 벽 예산 검사 코드 (v0.10.0, 게이트 284 줄)
- 뱀부 스튜디오 02.08.02.61 명령줄 재슬라이스 2 회 (2026-09-26) — 위 배경의 세 수치
- 보낸 G-code `.61719.0.gcode` 설정 기록 구간 + 피처별 압출 길이 측정
- ABS 돌출 팬 리서치 (`<SCRATCH>/codex-fan-out.txt`, Codex `gpt-5.6-sol` 읽기 전용) — **이번 범위
  밖이다.** 사용자가 "확정된 것만" 을 골라 팬·감속은 손대지 않는다. 근거만 `notes.md` 에 남긴다

## 범위 경계

경로 약칭:

```text
<OUT>      /Users/jackson/Hub/60_3D Print/Settings/h2-flipper-rear-exhaust-abs
<PETG>     /Users/jackson/Hub/60_3D Print/Settings/h2-flipper-rear-exhaust
<KIT>      bambu-kit/skills/bambu-print-profile
<FX>       bambu-kit/evals/gate-fixtures
<SCRATCH>  /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/d204ea78-091c-4f5b-a8db-ec3ead359b73/scratchpad/exhaust
```

**고치는 것** — `<OUT>` 의 process JSON 2 개 · 3mf 2 개 · zip 2 개 · `notes.md`,
그리고 `<KIT>/SKILL.md` · `<KIT>/references/surface-recipes.md` ·
`<KIT>/references/bambu-fields-baseline.md` · `<FX>` 의 새 시험 파일 2 개.

**안 고치는 것** — `<OUT>` 의 filament JSON 2 개, `<PETG>` 폴더 전체, 팬·감속 관련 어느 키도,
다른 킷, `docs/` HTML, 그리고 `bambu-fields-baseline.md` 에 빠져 있는 다른 기록 키
(`_wall_budget_short_share` · `_scarf_loop_circumference_mm`) 의 소급 등재.

**회귀 확인 범위** — 이번 검사 변경이 다른 실제 프로파일(H2 AMS Flipper 등 `<OUT>` 밖 산출물)에
어떻게 걸리는지는 **이번 범위 밖**이다. 새 갈래는 `classic` + 벽 예산 부족일 때만 갈라지고 그
경우에도 기록이 없으면 지금과 같이 FAIL 하므로, `arachne` 를 쓰는 기존 프로파일은 판정이 바뀌지
않는다. `<FX>` 시험 파일 전수 실행(SC-02)이 이 범위 안의 회귀 확인이다.

이 작업은 `main` 기반 별도 작업 폴더
`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/bambu-wall-gen-shape`
(브랜치 `feat/bambu-kit-wall-gen-shape`, 기준 `f81568d`) 에서 한다. `feat/bambu-kit-orca-h2s-feedback` 가지가 같은 파일 4 개를 건드리고 아직 병합되지 않았다.
**그 가지는 `origin/main` 보다 348 커밋 뒤처져 있고, 이번에 고치는 벽 예산 검사 자체를 아직 받지
못했다** — 공통 조상이 `baa1a38` (bambu-kit v0.9.2) 이고 벽 예산 검사는 그 뒤 `ea22121` 로 main 에
들어왔다. 그래서 `git diff main..그가지` 는 이 블록을 «삭제» 로 보여 주지만 실제로 지운 것이 아니다
(교차 진단이 이 자리를 「통째로 지웠다」 로 오진했고, 위 두 명령으로 반증했다). 그쪽이 main 을 받아
합칠 때 이 절이 함께 들어온다 — 이번 작업은 그 가지의 병합 부담을 늘리지만 `main` 기반이 정공법이다.

## 공통 전제

아래는 여러 조건이 함께 쓰는 전제다. 조건마다 반복하지 않는다.

**(전제 1) 슬라이스 1 회 실행** — `<OUT>` 의 3mf 를 사본으로 풀어
`Metadata/project_settings.config` 의 `enable_wrapping_detection` 만 `"0"` 으로 바꿔 다시 압축한 뒤
`/Applications/BambuStudio.app/Contents/MacOS/BambuStudio --slice 1 --outputdir <폴더> <사본.3mf>` 를
돌린다. 화면에서 경고인 감김 감지가 명령줄에서는 오류로 멈추기 때문이다. **`enable_wrapping_detection`
외에 어떤 값도 사본에서 바꾸지 않는다.** 산출물 3mf 자체는 이 치환을 담지 않는다.

**(전제 2) 길이 측정 규약** — G-code 길이는 `G1` 직선과 `G2`·`G3` 호를 **모두** 센다. 호는
중심 `= 현재 + (I, J)` · `r = hypot(I, J)` 로 시작각·끝각을 `atan2` 로 구해 `G2` 는 시계 ·
`G3` 는 반시계로 방향을 맞춘 뒤 `|각도차| x r` 로 잰다. 호 줄에서 현재 좌표를 갱신한다.
압출 폭은 `use_relative_e_distances = 1` 이므로 각 줄의 `E` 값이 그 자체로 증가량이다 —
누적 차이를 쓰지 않는다.

**(전제 3) 게이트 추출** — `<KIT>/SKILL.md` 의 Phase 4.3 검사를 그 문서에 적힌 추출 절차로
파일에 뽑아 쓴다. **뽑은 줄 수와 `RESULT` 줄 수를 먼저 출력**하고, 빈 파일이거나 `RESULT` 가
없으면 멈춘다. 고치기 전 판은 284 줄이었다.

**(전제 4) 기준 상태** — 2026-09-26 10:35 실측.

```text
기준 1 · <OUT> 9 파일 sha256 앞 16 자
  process/...-bambu.json    72ca12cf40e39657      ← 이번에 바뀐다
  process/...-orca.json     82764317d1f2b89d      ← 이번에 바뀐다
  filament/...-bambu.json   3533d0e5a17a6156      ← 그대로여야 한다
  filament/...-orca.json    07bc44c16624f730      ← 그대로여야 한다
  ..._baked-bambu.3mf       13407b3c734b1547      ← 이번에 바뀐다
  ..._baked-orca.3mf        172be1627e1f6de9      ← 이번에 바뀐다
  ...-abs-bambu.zip         c700cea427642eb3      ← 이번에 바뀐다
  ...-abs-orca.zip          90fe07ac3699e324      ← 이번에 바뀐다
  notes.md                  0235193d82a4952e      ← 이번에 바뀐다

기준 2 · <PETG> 폴더 묶음 지문   d422a04c00816cfa   ← 그대로여야 한다
기준 3 · 고치기 전 게이트로 현재 산출물 4 JSON = RESULT: PASS · exit 0 (양쪽 슬라이서)
기준 4 · 고치기 전 게이트로 classic 사본 = FAIL 1 건 · exit 1 (양쪽 슬라이서)
기준 5 · 고치기 전 게이트로 <FX> 시험 파일 23 개 원본 실행 = FAIL 20 개 · PASS 3 개
         PASS 3 개는 filament-unreadable-slot.json · filament-lattice-fanfix.json ·
         process-thin-baseline.json 이다 (경고·미검증 계열이라 PASS 가 기대값)
         죽은 검사는 0 건이다 — 나머지 20 개가 모두 FAIL 1 건 · exit 1 로 잡혔다
```

**(전제 7) `result.json` 의 시간 필드 두 종** — `sliced_plates[0]` 안에 둘이 있고 뜻이 다르다.
실측 (2026-09-26, 위 두 판):

```text
필드                  classic              arachne              G-code 머리글의 짝
main_predication      16288 초 (4h31m28s)  17420 초 (4h50m19s)  model printing time
total_predication      17366 초 (4h49m25s)  18497 초 (5h08m17s)  total estimated time
```

배경이 인용한 `4h 31m 57s` 는 **모델 출력 시간**이므로 `main_predication` 쪽이다.
`total_predication` 은 준비 시간을 포함해 약 18 분 더 크다 — 이 스프린트의 시간 조건은
`main_predication` 으로 잰다. 교차 진단이 이 어긋남을 잡았다 (`total_predication` 으로 재면
`classic` 으로 제대로 되돌려도 17366 초라 FAIL 이 난다).

**(전제 6) 회귀 방지 조건** — `SC-05` · `AP-01` · `AP-02` · `DG-04` 는 구현 전에도 통과한다. 이 조건들은 «이번 변경이 멀쩡한 것을 깨뜨리지 않았는지» 를 재는 자리이며, 구현 의존 조건이 아니다. 통과했다는 사실만으로 구현이 됐다는 근거로 쓰지 않는다.

**(전제 5) 파편화 배수의 뜻** — `_wall_outer_block_ratio` = (`classic` 으로 자른 G-code 의
`; FEATURE:Outer wall` 블록 수) ÷ (`arachne` 로 자른 같은 3mf 의 같은 블록 수). 같은 판 · 같은
나머지 설정으로 두 번 잘라 센다. 실측 0.993 (배기관) · 1.850 (래티스 통).

## Skill

- [ ] SK-01: `<KIT>/SKILL.md` 의 벽 예산 검사가 `_wall_outer_block_ratio` 를 읽어 **세 갈래**로 나뉜다 — (a) `classic` + 벽 예산 부족인데 그 키가 없으면 `errs` 에 넣는다 (b) 그 키가 임계 이상이면 `errs` 에 넣는다 (c) 임계 미만이면 넣지 않는다 [exact] (측정: 고친 뒤 게이트를 뽑아 세 갈래를 각각 타는 **기존 · 신규 시험 파일 3 개**로 돌려 확인한다 — (a) 는 기존 `<FX>/process-wall-budget-classic.json`(파편화 기록 없음) · (b) 는 신규 `<FX>/process-wall-budget-classic-high-frag.json` · (c) 는 신규 `<FX>/process-wall-budget-classic-low-frag.json` 이다. **임시 사본을 따로 만들지 않는다** — SC-01 이 만드는 파일을 그대로 쓴다. 기대: (a) FAIL · (b) FAIL · (c) PASS. 출력을 인용한다)
- [ ] SK-02: 그 검사 코드에 임계값과 **그 값이 추정임**이 주석으로 적혀 있다 — 같은 줄 또는 바로 위 줄에 문자열 `1.3` 과 `추정` 이 함께 있다 [structural] (근거: 현행 `10 %` 주석이 같은 형식으로 추정임을 밝힌다. 측정: `grep -n -A1 -B1 '_wall_outer_block_ratio' <KIT>/SKILL.md` 출력에서 두 문자열 동시 존재)
- [ ] SK-03: `<KIT>/references/surface-recipes.md` §2.8 에 배기관 사례가 **세 번째 실측으로** 추가되고, 세 사례의 파편화 배수를 한 표에 모은다 — 그 표에 문자열 `1.850` 과 `0.993` 이 모두 있다 [exact] (측정: `awk` 로 §2.8 구간을 잘라 그 안에서 두 문자열 각각 grep. 파일 전체를 grep 하지 않는다)
- [ ] SK-04: 같은 §2.8 의 **판정·처방 표 자체**가 `classic` 을 무조건 배제하지 않는다 — 그 표에서 `< 벽 예산, >= 외벽 2겹` 줄의 처방 칸이 「`arachne` 로」 하나만 적혀 있지 않고 파편화를 재라는 조건이 함께 적혀 있다 [exact] (근거: 표 아래에 새 문단만 붙여도 통과하면 표는 안 고쳐도 되는 조건이 된다 — 교차 진단 지적. 측정: SK-03 과 같은 구간 자르기 뒤 `awk -F'|'` 로 **`>= 외벽 2겹`** 을 포함하는 표 행 하나를 뽑아 (`< 외벽 2겹` 행도 `외벽 2겹` 을 담고 있어 좁혀 잡는다) 그 행의 마지막 칸에 `_wall_outer_block_ratio` 가 있는지 본다. 그 행을 못 찾으면 FAIL. 음성 대조: 그 행의 처방 칸을 원래 문구로 되돌린 사본에서 FAIL 이 나는지 확인한다)
- [ ] SK-05: `<KIT>/references/bambu-fields-baseline.md` 에 `_wall_outer_block_ratio` 가 기록 키로 등재돼 있다 [structural] (근거: `_geometry_class` 가 그 문서에 2 건 등재돼 있어 기록 키를 적는 자리가 이미 있다. **`_wall_budget_short_share` 와 `_scarf_loop_circumference_mm` 는 등재되지 않았다** — 교차 진단이 이 근거의 사실 오류를 잡았고 실측으로 확인했다(각 0 건). 그 둘을 소급 등재하는 것은 이번 범위 밖이다. 측정: `_wall_outer_block_ratio` 의 grep -c 가 1 이상)
- [ ] SK-06: `<KIT>/SKILL.md` 의 완료 체크리스트에 파편화 측정 지시가 한 줄 있다 — `_wall_outer_block_ratio` 를 포함하는 `- ☐` 로 시작하는 줄이 1 개 이상이다 [structural] (근거: 기존 `_geometry_class` 지시가 같은 형식으로 있다. 측정: `grep -cE '^- ☐.*_wall_outer_block_ratio'`)

## Script

- [ ] SK-07: `<KIT>/references/surface-recipes.md` §2.8 의 「측정」 절에 `_wall_outer_block_ratio` 를 **재는 절차**가 적혀 있다 — 그 절 안에 (a) 같은 3mf 를 두 생성기로 각각 자른다는 지시 (b) `; FEATURE:Outer wall` 블록을 센다는 지시 (c) 나눗셈 방향(`classic` 나누기 `arachne`)이 모두 있다 [exact, enumerated] (근거: 전제 5 가 뜻만 정의하고 재는 방법은 어디에도 없으면 다음에 이 킷을 쓰는 사람이 값을 채울 수 없다 — 교차 진단이 짚은 빠진 축이다. 측정: §2.8 구간에서 「측정」 소절을 다시 잘라 `FEATURE:Outer wall` · `classic` · `arachne` 세 문자열이 모두 있는지 각각 grep)

- [ ] SC-01: 새 시험 파일 **2 개**(`<FX>/process-wall-budget-classic-low-frag.json` · `<FX>/process-wall-budget-classic-high-frag.json`)가 (a) 폴더에 존재 (b) `SKILL.md` 의 시험 파일 표에 등재 (c) `SKILL.md` 의 `TARGET_SLICER=` 실행 줄에 등재 — **세 곳 모두** [exact, enumerated] (근거: 표에만 넣으면 그 검사는 한 번도 안 돈다. 측정: `SKILL.md` 가 이미 갖고 있는 누락 검출 블록 — `MISSING` 이 빈 문자열이어야 한다. 두 파일 이름을 각각 확인한 출력을 인용한다. 음성 대조: 새 파일 하나를 표에서만 지우면 `표에 없음 <파일명>` 이 나오고, 실행 줄에서만 지우면 `실행 줄에 없음 <파일명>` 이 나오는지 확인한 뒤 되돌린다)
- [ ] SC-02: 고친 게이트로 `<FX>` 의 시험 파일 **전부**를 `SKILL.md` 의 실행 줄대로 돌렸을 때 각 파일이 그 표에 적힌 기대 결과와 일치한다 [exact] (측정: 실행 줄을 순서대로 돌려 파일별 `RESULT` 와 `exit` 를 표의 기대 열과 대조한 표를 출력한다. 불일치 0 건이어야 한다. 알려진 답: 고치기 전 판의 원본 실행 결과가 전제 4 기준 5 다 — FAIL 20 개 · PASS 3 개. 고친 뒤에는 새 파일 2 개가 늘어 25 개가 되고, PASS 는 4 개(기존 3 개 + low-frag)가 된다)
- [ ] SC-03: 고친 게이트로 `<OUT>` 의 4 개 JSON(process 2 · filament 2)을 슬라이서별로 돌려 `RESULT: PASS` 와 종료 코드 0 이 나온다 [exact] (측정: `TARGET_SLICER=bambu` 로 뱀부 2 개, `TARGET_SLICER=orca` 로 오르카 2 개. **음성 대조**: 사본의 `_wall_outer_block_ratio` 를 `1.85` 로 바꾸면 벽 예산 FAIL 이 나오고, 그 키를 지우면 미기록 FAIL 이 나와야 한다 — 두 대조 출력을 함께 인용한다)
- [ ] SC-04: 기존 시험 파일 `<FX>/process-wall-budget-classic.json` 이 고친 게이트에서도 **여전히 FAIL 1 건 · exit 1** 이다 [exact] (근거: 그 파일은 파편화 기록이 없으므로 새 갈래 (a) 로 FAIL 해야 한다 — 통과로 바뀌면 검사에 구멍이 생긴 것이다. 측정: 그 파일 단독 실행의 `FAIL` 줄 수와 종료 코드. 그 FAIL 메시지에 `_wall_outer_block_ratio` 가 들어 있어야 한다 — 새 갈래 (a) 로 잡혔다는 증거다. 옛 메시지 그대로면 검사를 안 고친 것이다. 표의 기대 열도 함께 갱신한다)
- [ ] SC-05: `python3 scripts/validate-plugin.py bambu-kit` 가 통과한다 [exact] (측정: 종료 코드 0. 실패 항목이 있으면 그 목록을 출력에 남긴다)

## Error

- [ ] ER-01: `<OUT>/notes.md` 에 되돌린 근거 수치가 적혀 있다 — 문자열 `140.91`, `3.01`, `4h 31m`, `0.993` 이 **모두** 있다 [exact, enumerated] (측정: 네 문자열 각각 grep)
- [ ] ER-02: `<OUT>/notes.md` 에 킷 규칙이 이 형상에서 빗나간 이유가 적혀 있다 — **`외벽` 과 `파편화` 가 같은 문단**(빈 줄로 구분된 블록) 안에 있는 블록이 1 개 이상이다 [structural] (근거: 두 낱말이 문서 다른 곳에 따로 있어도 통과하면 설명을 안 쓴 것이 통과한다. 측정: `awk` 로 빈 줄 기준 블록을 나눠 두 문자열이 같은 블록에 있는 블록 수)
- [ ] ER-03: `<OUT>/notes.md` 에 이번에 **손대지 않은** 팬·감속 후보와 그 근거가 적혀 있다 — 문자열 `overhang_fan_speed` 와 `0~80` 이 모두 있다 [exact, enumerated] (근거: 리서치로 확보한 제조사 권장 범위를 남기지 않으면 다음에 같은 조사를 다시 한다. 측정: 두 문자열 각각 grep)

## Architecture

- [ ] AR-01: `<OUT>` 의 두 process JSON 에서 `wall_generator` 가 `classic` 이고 `_wall_outer_block_ratio` 가 `0.993` 으로 기록돼 있다 [exact, enumerated] (측정: `python3` 로 두 파일의 두 키 값을 각각 출력해 비교)
- [ ] AR-02: 앞선 스프린트가 봉인한 값 중 `wall_generator` **를 뺀 8 키**가 두 process JSON 에서 그대로다 — `outer_wall_speed` `200` · `overhang_1_4_speed` `60` · `overhang_2_4_speed` `30` · `overhang_3_4_speed` `10` · `overhang_4_4_speed` `10` · `seam_slope_type` `external` · `seam_slope_min_length` `10` · `seam_slope_conditional` `0` [exact, enumerated] (근거: 이번 범위는 벽 생성기 하나다. 측정: 같은 명령의 8 키 값)
- [ ] AR-03: 갱신한 뱀부 3mf 로 전제 1 을 1 회 돌린 G-code 에서 **폭 0.44 mm 를 넘는 안쪽벽 압출이 전체 안쪽벽의 1% 미만**이다 [exact] (근거: 실측 `arachne` 11.3% · `classic` 0.2%. 측정: 전제 2 규약으로 `; FEATURE:Inner wall` 구간의 압출 폭을 `(E x 필라멘트단면적 / 이동거리) / 0.16` 으로 내고 0.44 초과 길이 비율을 낸다. 알려진 답: 이 측정 스크립트를 `<SCRATCH>/wg/out-classic/plate_1.gcode` 에 돌리면 0.2%, `<SCRATCH>/wg/out-arachne/plate_1.gcode` 에 돌리면 11.3% 가 나온다 — 두 값이 안 나오면 스크립트가 틀린 것이니 조건 판정 전에 스크립트를 고친다. 음성 대조: 같은 측정을 보낸 G-code `.61719.0.gcode` 에 돌리면 11.3% 가 나와 FAIL 해야 한다 — 그 파일이 이미 지워졌으면 `<SCRATCH>/wg/out-arachne/plate_1.gcode` 를 쓴다)
- [ ] AR-04: 같은 1 회 실행의 `result.json` 에서 **`sliced_plates[0].main_predication`** 이 16800 초(4 시간 40 분) 미만이고 `sliced_plates[0].filaments[*].total_used_g` 합이 126.0 g 이상 127.5 g 이하다 [exact] (근거: 전제 7 — 배경이 인용한 모델 출력 시간에 대응하는 필드가 `main_predication` 이다. `total_predication` 은 준비 시간을 포함해 약 18 분 크므로 이 임계로 재면 제대로 고쳐도 FAIL 한다. 측정: 두 필드 — 둘 다 최상위가 아니라 판 배열 안에 있다. 알려진 답: `classic` 16288 초 · 126.94 g / `arachne` 17420 초 · 126.84 g — `arachne` 는 이 조건에서 FAIL 하므로 구현을 안 하면 통과하지 않는다)
- [ ] AR-05: `<OUT>` 의 파일 9 개가 모두 존재하고, 전제 4 기준 1 에서 **바뀐다고 적힌 7 개의 지문이 달라졌고 그대로여야 하는 2 개는 같다**. 전제 4 기준 2 의 `<PETG>` 묶음 지문도 같다 [exact, enumerated] (측정: 9 경로에 `test -f` + 9 개 지문을 기준값과 각각 비교 + `<PETG>` 묶음 지문 1 개 비교. 양성 대조: `<PETG>` 에 빈 임시 파일을 하나 만들면 묶음 지문이 달라지는지 확인한 뒤 지운다)
- [ ] AR-06: 같은 1 회 실행이 낸 `plate_1.gcode` 를 갱신한 process · filament JSON 과 대조했을 때 `MISMATCH` 가 0 건이다 [exact] (측정: `<KIT>/SKILL.md` Phase 4.4 의 대조 스크립트를 그 문서에 적힌 대로 뽑아 실행 — 종료 코드 0. 양성 대조: 사본의 `wall_generator` 를 `arachne` 로 바꾸면 `MISMATCH` 가 나오는지 확인한다)
- [ ] AR-07: 두 zip 이 각각 `process/` 와 `filament/` 를 갖고 **그 안의 네 파일(zip 2 개 x 2 파일)이 모두** `<OUT>` 의 같은 이름 파일과 내용이 같다 [exact, enumerated] (측정: `unzip -l` 로 구조 + `unzip -p` 로 꺼낸 네 파일의 `sha256` 을 폴더 파일과 각각 비교)
- [ ] AR-08: Given — 구현 완료 시점. 작업 폴더 `bambu-wall-gen-shape` 에서 `git status --porcelain` 의 변경이 **아래 화이트리스트 안에만** 있다 — `.harness/sprint-contract-h2-flipper-rear-exhaust-abs-wall-gen.md` · `.harness/sprint-feedback-h2-flipper-rear-exhaust-abs-wall-gen.md` · `.harness/sprint-amendments-h2-flipper-rear-exhaust-abs-wall-gen.md` · `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` · `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` · `bambu-kit/evals/gate-fixtures/process-wall-budget-classic-low-frag.json` · `bambu-kit/evals/gate-fixtures/process-wall-budget-classic-high-frag.json` [exact, enumerated] (근거: 이 작업 폴더는 `f81568d` 에서 새로 만들어 다른 세션이 쓰지 않는다 — 건수가 아니라 이름으로 잰다. **제외 경로**: `00000.log` · `.harness/.meta/` 하위 · `.DS_Store` — 도구가 자동으로 남기는 것이라 이번 작업의 산출물이 아니다. 슬라이스 임시 파일과 사본은 전부 `<SCRATCH>` 에 만들어 작업 폴더에 두지 않는다. 측정: `git status --porcelain` 목록에서 위 제외 경로를 뺀 뒤 화이트리스트 8 경로와 `comm` 으로 대조해 화이트리스트 밖 항목이 0 개인지 본다. 밖에 있는 항목이 있으면 그 이름을 출력에 남기고 FAIL)

## Anti-patterns

- [ ] AP-01: `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` 가 통과한다 [exact] (근거: `project.yaml` AP-03 — 이번에 `SKILL.md` 와 참조 문서에 코드 블록을 넣는다. 측정: 종료 코드 0)
- [ ] AP-02: `python3 scripts/validate-plugin.py bambu-kit --check=refs` 가 통과한다 [exact] (근거: 새 시험 파일 2 개를 문서에서 가리키므로 참조가 끊어질 수 있다. 측정: 종료 코드 0)

## Reusability

- [ ] RE-01: N/A (산출물이 설정 JSON · 문서 · 3mf · zip 과 킷 문서뿐 — 재사용 단위 코드 0 개)
- [ ] RE-02: `<OUT>/notes.md` 에 이번 판단의 근거 문서가 인용돼 있다 — 문자열 `surface-recipes.md` 와 `_wall_outer_block_ratio` 가 모두 있다 [exact, enumerated] (측정: 두 문자열 각각 grep)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개)
- [ ] DG-02: N/A (산출물 절반이 레포 밖 `60_3D Print/Settings/` 에 있고, 레포 쪽 변경은 마크다운과 JSON 뿐이라 편집기 진단 대상이 아니다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` — 이번 변경 파일과 교집합 0 개)
- [ ] DG-04: 전제 1 의 1 회 실행에서 `result.json` 의 `return_code`(최상위)가 0 이고 `sliced_plates[0].warning_message` 가 빈 문자열이다 [exact] (측정: 두 필드 — 서로 다른 중첩 깊이에 있다)
