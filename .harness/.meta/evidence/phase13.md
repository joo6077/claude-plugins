---
phase: 13
title: "Phase 13 bambu-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치·설정 키를 지어내지 마라.
---

출처 유형: Codex. read-only 준수, 파일 수정 없음. 웹 검색 5/12회 사용.

**1. 관찰 사실**
**L1 곡면 계단현상**
| 항목 | 확인값 |
|---|---|
| (a) 키 | `layer_height`는 활성 PrintConfig 키. 단위 `mm`, source default `0.2`이며 “작을수록 정확도 ↑, 시간 ↑”로 정의됨. `resolution`도 활성 키, 단위 `mm`, source default `0.01`, H2S common profile default `0.012`. 근거: PrintConfig.cpp `layer_height` lines 796-802, `resolution` lines 4071-4078, fdm_process_common lines 67/101. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json)) |
| adaptive 핵심 | Bambu Studio는 UI상 Variable/Adaptive Layer Height가 존재하는 것으로 확인됨. Bambu 커뮤니티 이슈가 공식 guide path와 “Variable Layer Height / adaptive” 조작을 언급함. ([github.com](https://github.com/bambulab/BambuStudio/issues/9518?utm_source=openai)) ([forum.bambulab.com](https://forum.bambulab.com/t/set-minimum-and-maximums-for-variable-layer-height/67875?utm_source=openai)) |
| JSON 표현 가능성 | **process+filament JSON으로는 불가능으로 처리해야 함.** `adaptive_layer_height`는 fdm_process_common에 `"0"`으로 남아 있지만, PrintConfig.cpp의 실제 option 정의는 주석 처리되어 있고, legacy ignore set에도 `adaptive_layer_height`가 들어감. 따라서 import에 넣어도 의미 있게 켜진다고 볼 근거가 없음. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) |
| (b) 기본값 | `layer_height`: source `0.2mm`; H2S 0.20 Standard inherits `0.2`, 0.12 HQ 체인은 `fdm_process_single_0.12`의 `0.12`. `min_layer_height`: `0.07mm`, `max_layer_height`: `0` nullable, 둘 다 adaptive limit 설명. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_single_0.12.json)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) |
| (c) 권장 | process JSON에서는 `layer_height=0.12`를 1차 권장, 계단이 핵심이고 시간 허용 시 `0.08-0.12`. `0.08`은 `min_layer_height 0.07` 위이지만 H2S 공식 0.08 process 근거는 미확인. `resolution=0.006-0.010`은 XY 곡선 faceting 완화용이지 Z 계단의 주 해결책은 아님. Orca precision 문서도 `resolution`은 작을수록 해상도↑/slicing time↑라고 설명함.  |
| (d) 부작용 | `0.20→0.12`는 대략 레이어 수 1.67배, `0.08`은 2.5배. 작은 `resolution`은 slicing/G-code 부담 증가. Arc fitting은 Orca 문서상 품질 개선 기능이 아니라 G-code encoding 변경이며 firmware arc segmentation 리스크가 있음.  |

**L2 Voronoi stringing**
| 항목 | 확인값 |
|---|---|
| (a) 키 | filament JSON override 키는 `filament_retraction_length`, `filament_retraction_speed`, `filament_retraction_minimum_travel`, `filament_wipe`, `filament_wipe_distance`, `filament_z_hop`, `filament_z_hop_types`. 공통 filament profile 기본은 대체로 `"nil"`이라 printer/extruder 기본에 위임. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/fdm_filament_common.json)) |
| underlying defaults | `retraction_length=0.8mm`, `retraction_speed=30mm/s`, `retraction_minimum_travel=2mm`, `wipe=false`, `wipe_distance=2mm`, `z_hop=0.4mm`, `z_hop_types=Spiral`. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp))  |
| 온도 키 | `nozzle_temperature`, `nozzle_temperature_initial_layer`, range low/high는 °C. common default 200/200/190/240이나 실제 소재 profile이 override함. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) |
| (c) 권장 | 자동으로 retraction을 크게 올리지 말 것. Bambu 커뮤니티 사례는 PETG/stringing에서 “retraction 기본값이면 충분, 건조가 우선”이라는 답과, 다중 retraction 파트에서 `wipe while retract` 및 -5~-10°C가 도움 된다는 보고가 같이 있음. 권장 게이트: 건조/소재 상태 확인 → 그래도 voronoi travel stringing이면 `filament_wipe=1`, `filament_wipe_distance=2`부터. retraction length는 `0.8` 기준, 필요 시 `1.0-1.2`까지만 coupon 후 적용.   |
| (d) 부작용 | 과한 retraction은 underextrusion, grinding, clog. z-hop 증가는 시간과 ooze 기회 증가. 온도 하향은 stringing 감소 가능성이 있지만 층간 접착/flow 부족을 만들 수 있으므로 자동 JSON 변경 금지에 가깝다. |

**L3 바닥 박리 / first-layer lifting**
| 항목 | 확인값 |
|---|---|
| (a) 키 | `brim_type` enum: `auto_brim`, `brim_ears`, `outer_only`, `inner_only`, `outer_and_inner`, `no_brim`; source default `auto_brim`. `brim_width` mm source default `0`, fdm_process_common `5`; `brim_object_gap` mm source default `0`, fdm_process_common `0.1`.  ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json)) |
| 추가 키 | `raft_layers` layers source/common default `0`, tooltip이 ABS warping 회피 용도를 명시. `raft_first_layer_expansion` mm default `-1` auto. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) |
| 첫 레이어 | `initial_layer_print_height=0.2mm`, `initial_layer_line_width=0.4mm` source default, common profile은 line width `0.5`; `initial_layer_speed=30mm/s` source, common `20`, H2S standard `50`. 두꺼운 initial layer가 adhesion 개선 가능하다고 source tooltip이 명시. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json)) |
| 온도/팬 | plate 온도는 `hot_plate_temp_initial_layer`, `textured_plate_temp_initial_layer`, `eng_plate_temp_initial_layer` 등 plate-specific 키를 써야 함. `bed_temperature_initial_layer`는 obsolete ignored key. Aux fan은 `additional_cooling_fan_speed` %, `close_additional_fan_first_x_layers` layers. ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)) ([raw.githubusercontent.com](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/fdm_filament_common.json)) |
| (c) 권장 | first-layer lifting 감지 시 process JSON에 `brim_type="outer_only"` 또는 `auto_brim`, `brim_width=5-8`, `brim_object_gap=0-0.1`. 큰 PLA/PETG 출력은 aux fan off/낮춤을 notes로 우선 안내. ASA/ABS/PC는 chamber preheat와 high temp/engineering plate, brim gap 0, 필요 시 `raft_layers=1-3`만 게이트 적용. Bambu 커뮤니티도 aux fan off, bed temp↑, brim gap 0, chamber 40°C+를 반복 보고함.   |
| (d) 부작용 | brim은 제거 흔적/edge cleanup 발생. gap 0은 접착은 좋지만 제거 어려움. raft는 바닥면 품질 저하, 시간/소재 증가, `elefant_foot_compensation` 무효화와 충돌. fan off는 overhang/stringing을 악화할 수 있음. |

**2. 권장안**
references SSOT에는 새 `failure-recipes.md`를 추가하거나 `surface-recipes.md`를 확장하는 편이 맞습니다.

추가할 항목:
- `curved_surface_stair_stepping`: `layer_height`, `resolution`, `min_layer_height`, `max_layer_height`, `adaptive_layer_height` 금지 규칙.
- `voronoi_stringing`: filament override 키 사전, “drying first”, `filament_wipe` 우선, retraction 자동 과상향 금지.
- `first_layer_lifting`: `brim_type/brim_width/brim_object_gap`, `initial_layer_*`, plate-specific temperature keys, aux fan/chamber notes, `raft_layers` emergency gate.

스킬 프로세스 변경:
- Phase 1에 failure-mode detector 추가: `curved/stair-step`, `voronoi/stringing`, `peeling/lifting/warping`.
- Phase 3 JSON 생성 전 “지원 가능/불가능” 분기 추가: L1 adaptive는 **notes only**, process JSON에는 넣지 않음.
- Completion Evidence Gate에 금지 키 검사 추가: `adaptive_layer_height`, `bed_temperature`, `bed_temperature_initial_layer`, `elephant_foot_compensation`.

넣지 말아야 할 것:
- `adaptive_layer_height`를 process JSON에 넣지 말 것.
- `bed_temperature_initial_layer`를 쓰지 말 것. plate-specific key만 사용.
- stringing 대응으로 retraction/temperature/fan을 무조건 덮어쓰지 말 것.
- `raft_layers > 0`와 `elefant_foot_compensation`을 같이 쓰지 말 것.

**3. 트레이드오프**
- L1은 가장 확실한 자동 대응이 fixed `layer_height` 하향이라 출력 시간이 크게 는다. UI variable layer height가 더 효율적이지만 이 플러그인의 process+filament JSON 범위 밖이다.
- L2는 건조/소재 상태가 지배적이면 JSON 튜닝이 효과 없거나 악화한다. wipe/retraction은 coupon 기반으로만 올려야 한다.
- L3는 brim/raft가 성공률을 올리지만 후처리와 바닥 품질을 희생한다. 팬/온도 조정은 소재별 부작용이 커서 자동 적용 범위를 좁혀야 한다.

**4. 열린 질문**
- Bambu Studio의 per-object/project variable layer height가 3MF 내부에서 어떤 키/구조로 저장되는지 미확인.
- `brim_ears`가 process JSON만으로 재현 가능한지, 아니면 painted/per-object 좌표가 필요한지 미확인.
- H2S 선택 소재별 공식 filament profile에서 실제 aux fan/plate temp override를 모델별로 다시 확인해야 함.
- L2/L3 자동 적용 임계값: 사용자 실측 실패 1회만으로 적용할지, 댓글/모델 형상/소재 신호가 함께 있을 때만 적용할지 정책 결정 필요.
