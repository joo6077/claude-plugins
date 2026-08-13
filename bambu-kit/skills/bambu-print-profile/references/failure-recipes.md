# 실측 실패 모드 → 프로파일 키 레시피 (Bambu Studio H2S)

> Last updated: 2026-08-13
> Source: `.harness/.meta/evidence/phase13.md` (카이젠 Phase 13 외부 근거 · Codex foreground · read-only)
> Bambu Studio reference version: 2.6.0 (v02.06.00.51)
> Sibling references: `bambu-fields-baseline.md` **§10** (이 문서가 쓰는 키의 enum / 단위 / default **정본**) ·
> `surface-recipes.md` (표면 우선 정책) · `seam-recipes.md` (seam 전략) · `tolerance.md` (공차 보정)

## 0. 이 문서의 위치

`surface-recipes.md` 는 **사용자가 처음부터 표면을 원할 때** 쓰는 사전 정책이다. 이 문서는 반대 방향 —
**실물을 출력했고 실패했을 때** 그 실패 표현을 프로파일 키로 되돌리는 사후 레시피다.

**키 이름 · 단위 · default 수치를 이 문서에 적지 마라.** 정본은 `bambu-fields-baseline.md` §10 이며,
이 문서는 **판정 절차 · 게이트 순서 · 권장 방향 · 부작용 · 금지**만 갖는다. 두 곳에 같은 수치를 두면
한쪽만 고쳐지는 순간 프로파일에 틀린 값이 박힌다 (`xy_hole_compensation` 2× 오해 선례 — `tolerance.md` §1.1).

### 실패 모드 3 종

| ID | 사용자가 쓰는 표현 | 절 |
|----|------------------|----|
| **L1** | "곡면이 계단처럼 보인다", "둥근 데가 층층이", stair-stepping, "curved surface 거칠다" | §1 |
| **L2** | "실이 늘어진다", "거미줄", stringing, "voronoi 인필 사이에 실" | §2 |
| **L3** | "바닥이 떴다", "가장자리 들림", 박리, peeling, lifting, warping, "첫 층이 안 붙는다" | §3 |

### 사용자 실측 실패 보고의 취급 — 규칙을 여기서 재정의하지 마라

정본은 `harness/docs/guides/skill-design-guide.md` **§3.8 User-Reported Failure Gate** 다. 요지만 인용한다:
사용자 관측은 **반증 대상이 아니라 재현 대상**이고, 상태는 PASS 가 아니라 `REOPENED` 이며, 재현 전에
"정상입니다" 를 다시 말하지 않는다.

§3.8 의 재현 6 축을 3D 프린팅 도메인으로 치환한 대응표 (이것만 이 문서가 갖는다):

| §3.8 축 | 3D 프린팅 대응 | 확인 질문 |
|---------|---------------|----------|
| URL / 경로 | **모델 리비전** | 실패한 출력이 지금 슬라이스하려는 STL/3MF 와 같은 리비전인가 |
| 브랜치 / 커밋 | **적용된 preset 이름** | 실패한 출력이 실제로 그 process/filament preset 으로 슬라이스됐는가 (드롭다운 확인) |
| viewport | **슬라이서 버전** | 프로파일 생성 시 버전과 출력 시 버전이 같은가 (필수 사전 절차 1) |
| 디바이스 / 플랫폼 | **plate 종류 + chamber/환기** | textured PEI / high temp / engineering 중 무엇이고 chamber 는 몇 °C 였나 |
| auth · cache | **소재 lot + 건조 상태** | 같은 스풀인가, AMS HT 건조를 몇 시간 돌렸나 |
| 데이터 상태 | **AMS 슬롯 매핑** | 실패한 슬롯과 지금 슬롯이 같은 소재·색인가 |

**6 축 중 하나라도 다르면 그것을 먼저 값으로 특정**하고, 프로파일 키를 바꾸기 전에 사용자에게 보고한다.
슬라이서 버전이나 건조 상태가 달랐던 실패에 retraction 을 올리는 것은 원인이 아닌 곳을 고치는 것이다.

## 1. L1 — 곡면 계단현상 (curved surface stair-stepping)

### 1.1 JSON 으로 **지원 불가** — adaptive / variable layer height

⚠️ **`adaptive_layer_height` 를 process JSON 에 넣지 마라.** 이 스킬의 산출물(process+filament JSON)로는
**구현 불가능**하다. 근거 2 가지 (`bambu-fields-baseline.md` §10.1 · §10.4):

1. `fdm_process_common.json` 에 `"0"` 으로 값이 남아 있지만, `PrintConfig.cpp` 의 실제 option 정의는
   **주석 처리**돼 있다.
2. 같은 키가 **legacy ignore set** 에도 들어간다 — 즉 로딩 시 무시 대상이다.

따라서 JSON 에 넣어도 **의미 있게 켜진다고 볼 근거가 없다.** Bambu Studio UI 에 Variable / Adaptive
Layer Height 기능 자체는 존재하지만 그것은 **per-object / project 레벨 조작**이며 이 플러그인의
process+filament JSON 범위 밖이다.

**처리 규약 — notes only.** L1 이 감지되면:

- process JSON 에는 **넣지 않는다** (Phase 4.3 게이트가 잔존을 잡는다 — §4).
- `notes.md` §1.2 에 **"Variable Layer Height 는 이 프로파일 범위 밖 — Bambu Studio UI 에서 직접
  적용해야 함"** 을 명시 보고한다. 조용히 생략하지 마라. Flutter inset shadow 를 조용히 빠뜨리는 것과
  같은 종류의 누락이다.
- 사용자가 UI 조작 경로를 물으면 커뮤니티 이슈/포럼 링크만 안내한다 (§7).

### 1.2 JSON 으로 **대응 가능** — 고정 레이어 하향 + resolution

| 순서 | 조치 | 값 | 판단 근거 |
|------|------|----|----------|
| 1 | `layer_height` 하향 | **`0.12` 1 차 권장** | H2S 0.12 High Quality 체인이 공식 프로파일로 실재 (§10.1) |
| 2 | 계단이 핵심이고 시간을 감수한다면 | `0.08`–`0.12` | `min_layer_height` 하한(§10.1) 위이지만 **H2S 공식 0.08 process 프로파일 근거는 `[미확인]`** — 사용자에게 "비공식 영역" 임을 알린 뒤 적용 |
| 3 | XY 곡선 faceting 이 함께 거칠면 | `resolution` `0.006`–`0.010` (§8.3) | ⚠️ **Z 계단의 주 해결책이 아니다.** XY 평면 세그먼트 해상도만 올린다 |

⚠️ **`enable_arc_fitting` 을 계단 해결책으로 쓰지 마라.** 이것은 표면 품질 기능이 아니라 **G-code
encoding 변경**(직선 세그먼트 → arc 명령)이며, firmware arc segmentation 리스크가 따라온다. 기본값을
유지하고 계단 대응 카드로 제시하지 않는다.

### 1.3 부작용 — 반드시 사전 고지

| 조치 | 비용 |
|------|------|
| `0.20` → `0.12` | 같은 높이에서 **레이어 수 약 1.67 배** (`0.20 / 0.12`) |
| `0.20` → `0.08` | **약 2.5 배** (`0.20 / 0.08`) |
| `resolution` 하향 | slicing 시간 + G-code 크기 증가 |

레이어 수 배수는 타이핑하지 말고 `기존 layer_height / 새 layer_height` 로 계산해서 보고한다.
출력 시간은 레이어 수에 비례하지 않을 수 있으므로 "레이어 수 N 배" 로만 말하고 시간 배수를 단정하지 않는다.

**트레이드오프 요약:** L1 에서 가장 확실한 자동 대응은 고정 `layer_height` 하향이라 시간이 크게 는다.
UI variable layer height 가 더 효율적이지만 §1.1 대로 범위 밖이다. 이 트레이드오프를 사용자에게
그대로 제시하고 선택을 받아라 — 자동으로 `0.08` 을 밀어넣지 마라.

## 2. L2 — 스트링잉 (voronoi 인필 / travel stringing)

### 2.1 진단 게이트 — **건조가 먼저다**

⚠️ **소재 상태를 확인하기 전에 프로파일을 만지지 마라.** 커뮤니티 사례는 PETG/stringing 에서
"retraction 기본값이면 충분, 건조가 우선" 이라는 답과, 다중 retraction 파트에서 wipe-while-retract 및
노즐 온도 −5~−10 °C 가 도움 된다는 보고가 **같이** 존재한다. 즉 지배 변수는 프로파일이 아니라 습도다.

게이트 순서 (앞 단계를 통과하지 않으면 다음으로 가지 않는다):

```text
L2 감지
  │
  ├─ (0) 소재 상태 확인 — 이 단계에서 대부분 끝난다
  │      · AMS HT 건조 이력 (소재별 시간/온도는 materials.md)
  │      · 스풀 개봉 시점 / 보관 상태
  │      · 같은 스풀로 다른 모델에서도 났는가
  │      → 건조 미충족이면 **JSON 변경 없이** 건조 후 재출력 권고로 종료
  │
  ├─ (1) 건조 충족인데도 travel stringing → filament wipe 만 opt-in
  │      `filament_wipe` = 1 · `filament_wipe_distance` = 2 (기본값 §10.2)
  │      → 이 2 키가 L2 의 유일한 무조건 허용 override 다
  │
  └─ (2) (1) 로도 남으면 retraction 소량 상향 — **coupon 통과 후에만**
         `filament_retraction_length` 를 기준값(§10.2)에서 `1.0`–`1.2` 까지만
         → Phase 5 coupon 으로 검증한 뒤 본 출력에 반영
```

**공통 filament profile 기본은 대체로 `"nil"` 이다.** 즉 값이 비어 보이는 것은 0 이 아니라
**printer / extruder 기본에 위임**된 상태다. `"nil"` 을 "설정 안 됨" 으로 읽고 임의 숫자로 채우면
프린터 기본 튜닝을 통째로 덮어쓴다. 위임 상태의 실효값은 §10.2 의 underlying default 열을 본다.

### 2.2 금지

| 금지 | 이유 |
|------|------|
| retraction 을 **자동으로 크게** 올리기 | underextrusion · 필라멘트 grinding · clog |
| `nozzle_temperature*` 자동 하향 | stringing 은 줄 수 있으나 층간 접착/flow 부족을 만든다. **이 스킬은 온도를 건드리지 않는다** (사용자 명시 요청 2026-05-16) |
| fan / cooling 자동 변경 | 소재별 부작용이 커서 자동 적용 범위 밖 |
| z-hop 증가를 기본 카드로 제시 | 출력 시간 + ooze 기회 증가 |

`filament_retraction_speed` · `filament_retraction_minimum_travel` · `filament_z_hop` ·
`filament_z_hop_types` 는 **키 사전으로만** 갖는다 (§10.2). 사용자가 명시 요청할 때 정확한 키 이름을
쓰기 위한 것이고, 자동 결정 대상이 아니다.

### 2.3 부작용

건조/소재 상태가 지배적이면 JSON 튜닝은 **효과가 없거나 악화**한다. wipe/retraction 상향은 coupon
기반으로만 올려야 하며, coupon 없이 올린 값은 다음 실패의 원인이 된다.

## 3. L3 — 바닥 박리 / 첫 레이어 들림 (base peeling · first-layer lifting · warping)

### 3.1 process JSON 자동 대응 — brim 우선

| 키 | 값 | 비고 |
|----|----|-----|
| `brim_type` | `outer_only` 또는 `auto_brim` | enum 전체·default 는 §10.3 |
| `brim_width` | `5`–`8` | fdm_process_common 기본과의 차이는 §10.3 |
| `brim_object_gap` | `0`–`0.1` | ASA/ABS/PC 는 `0` (접착 우선) |

첫 레이어 보강 (조건부 — 사용자가 바닥면 품질을 포기할 수 있을 때만):
`initial_layer_print_height` 상향 · `initial_layer_line_width` 상향 · `initial_layer_speed` 하향.
두꺼운 첫 레이어가 adhesion 을 개선할 수 있다는 것은 source tooltip 근거가 있다 (§10.3).
단 H2S standard 의 `initial_layer_speed` 는 source/common 보다 **높게** 잡혀 있으므로 (§10.3)
"기본값보다 낮춘다" 를 계산 없이 말하지 마라 — 상속 체인의 실효값을 먼저 확인한다.

### 3.2 소재별 게이트

| 소재군 | 조치 | 형태 |
|--------|------|------|
| **PLA / PETG 대형 출력** | aux fan off 또는 하향 | **notes 우선 안내** — `additional_cooling_fan_speed` · `close_additional_fan_first_x_layers` (§10.3) 를 JSON 으로 자동 변경하지 않는다 |
| **ASA / ABS / PC** | chamber preheat + high temp / engineering plate + `brim_object_gap` `0` | plate 온도는 **plate-specific 키**로만 (§3.3) · 자동 변경 전 사용자 확인 |
| **최후 수단** | `raft_layers` `1`–`3` | **emergency gate** — §3.3 의 충돌 규칙을 먼저 확인 |

### 3.3 금지

⚠️ **`bed_temperature_initial_layer` 를 쓰지 마라.** obsolete ignored key 다. plate 온도는
`hot_plate_temp_initial_layer` / `textured_plate_temp_initial_layer` / `eng_plate_temp_initial_layer`
같은 **plate-specific 키**로만 지정한다 (§10.3). `bed_temperature` 도 게이트 금지 목록에 있다 (§4).

⚠️ **`raft_layers > 0` 과 `elefant_foot_compensation` 을 같이 쓰지 마라.** raft 가 있으면 elephant foot
보정이 **조용히 0 으로 무효화**된다 (`tolerance.md` §1.2 에 소스 근거). fit-critical 부품이 있는 모델에
raft 를 켜면 Phase 1.7 의 공차 계산이 통째로 무의미해진다.

⚠️ **fan off 를 무조건 권하지 마라.** overhang 품질과 stringing(§2)을 악화시킬 수 있다 — L2 와 L3 가
같이 보고되면 이 둘은 **상충**한다는 것을 사용자에게 먼저 알린다.

### 3.4 부작용

| 조치 | 비용 |
|------|------|
| brim | 제거 흔적 · edge cleanup 필요 |
| `brim_object_gap` `0` | 접착은 좋아지지만 제거가 어렵다 |
| raft | 바닥면 품질 저하 · 시간/소재 증가 · `elefant_foot_compensation` 무효화 |
| aux fan off | overhang / stringing 악화 |

## 4. 금지 키 — Phase 4.3 Completion Evidence Gate 가 검사하는 목록

아래 4 키가 생성 JSON 에 **존재하면 FAIL** 이다. 게이트 구현은 SKILL.md Phase 4.3 스크립트에 있고,
이 표는 그 목록의 사유 정본이다.

| 금지 키 | 사유 | 대체 |
|---------|------|------|
| `adaptive_layer_height` | option 정의 주석 처리 + legacy ignore set — 켜진다는 근거 없음 (§1.1) | `layer_height` 하향 + notes 명시 |
| `bed_temperature_initial_layer` | obsolete ignored key (§3.3) | plate-specific 키 (§10.3) |
| `bed_temperature` | 위와 같은 규칙의 대상. **obsolete 여부 자체는 근거상 `bed_temperature_initial_layer` 만 확인됨 → 이 키는 게이트 금지 목록으로만 취급** `[미확인]` | plate-specific 키 (§10.3) |
| `elephant_foot_compensation` | Bambu 의도적 오타 미반영 — silent skip (`tolerance.md`) | `elefant_foot_compensation` |

> **마커 규약:** 이 문서의 `[미확인]` 은 **문서 근거 미확보**를 뜻하는 서술 라벨이고,
> `[미검증]`(qa-evaluator 의 검증 도구·환경 부재 마커 · 정본
> `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol) 과 **다른 축**이다.
> 두 낱말을 서로 바꿔 쓰지 마라.

## 5. 3 종 동시 보고 시 우선순위

실측에서는 3 종이 한 출력에서 같이 나온다. 순서를 지켜라 — 뒤 항목부터 만지면 앞 항목이 원인일 때
증거가 오염된다.

1. **L3 먼저** — 첫 레이어가 안 붙으면 나머지 관측은 전부 신뢰할 수 없다.
2. **L2 다음** — 건조 문제면 L1 튜닝(느린 외벽 · 낮은 layer)이 stringing 을 **더** 키운다
   (`surface-recipes.md` §6.5 PETG HF 경고와 같은 구조).
3. **L1 마지막** — 시간 비용이 가장 크고, 위 둘이 원인이면 효과가 없다.
4. **L2 ∧ L3 동시**: fan 방향이 상충한다 (§3.3). 어느 쪽을 우선할지 사용자에게 명시적으로 물어라.

## 6. 열린 질문 — 근거 부족으로 이번 사이클 미반영

이 문서는 아래를 **추측으로 채우지 않는다.** `/bambu-research` 소관이다.

- Bambu Studio 의 per-object / project variable layer height 가 3MF 내부에서 어떤 키/구조로 저장되는지 `[미확인]`.
- `brim_ears` 가 process JSON 만으로 재현 가능한지, painted / per-object 좌표가 필요한지 `[미확인]`.
- H2S 선택 소재별 공식 filament profile 의 실제 aux fan / plate temp override 값 — 모델별 재확인 필요.
- L2 / L3 자동 적용 임계값 정책: 사용자 실측 실패 **1 회**만으로 적용할지, 댓글·모델 형상·소재 신호가
  함께 있을 때만 적용할지 미결. **현재 이 문서는 "1 회 보고 → 게이트 진입, 자동 적용은 §2.1 / §3.1 범위
  한정" 으로 보수 운용한다.**

## 7. 출처

- 카이젠 Phase 13 근거 파일: `.harness/.meta/evidence/phase13.md` (Codex foreground · read-only)
- 슬라이서 소스 / 공식 프로파일:
  - <https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp>
  - <https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json>
  - <https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_single_0.12.json>
  - <https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/fdm_filament_common.json>
- Variable / Adaptive Layer Height 가 UI 기능으로 존재함을 보이는 커뮤니티 근거 (JSON 근거 아님):
  - <https://github.com/bambulab/BambuStudio/issues/9518>
  - <https://forum.bambulab.com/t/set-minimum-and-maximums-for-variable-layer-height/67875>
- 실측 실패 출처: `/insights` 2026-08-13 (관측 윈도 2026-06-12~08-12) — shower-box 부품 + holster
  모델 5 세션에서 곡면 계단현상 · voronoi stringing · 바닥 박리 반복 보고, 결과 "partially successful".
