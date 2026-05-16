# Bambu Studio JSON Fields Baseline

> Last updated: 2026-05-15
> Source: Codex research run `a5afcf864d05cf3b7` (score 25/25)
> Bambu Studio reference version: **2.6.0 / v02.06.00.51** (Public Release Hotfix, 2026-04-17)
> Latest beta at time of research: 2.7.0 Public Beta (2026-05-14)

스킬이 process / filament JSON을 inherits 기반으로 자동 생성할 때 참조하는 baseline. 매 실행 시 kaizen 데이터 소스로 cross-check 권장.

## 1. Bambu Studio 안정 버전

- **2.6.0 / v02.06.00.51** — Public Release Hotfix, 2026-04-17 13:02
- 2.6.1 / v02.06.01.55는 Public Beta (pre-release)
- 출처: https://github.com/bambulab/BambuStudio/releases/tag/v02.06.00.51, https://github.com/bambulab/BambuStudio/releases

## 2. H2S 공식 Base 프로파일

### Machine
- **이름:** `Bambu Lab H2S 0.4 nozzle`
- **파일:** `resources/profiles/BBL/machine/Bambu Lab H2S 0.4 nozzle.json`
- `default_print_profile`: `0.20mm Standard @BBL H2S`
- `default_filament_profile`: `Bambu PLA Basic @BBL H2S`
- 출처: https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/machine/Bambu%20Lab%20H2S%200.4%20nozzle.json

### Process (default 0.4mm nozzle)
- **이름:** `0.20mm Standard @BBL H2S`
- **파일:** `resources/profiles/BBL/process/0.20mm Standard @BBL H2S.json`
- `inherits: fdm_process_single_0.20`
- `compatible_printers: ["Bambu Lab H2S 0.4 nozzle"]`
- 출처: https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2S.json

### AMS 표기 정정
- 사용자가 자주 쓰는 "AMS Pro 2"의 **공식 표기는 `AMS 2 Pro`**.
- H2S 공식 페이지: 최대 4개 AMS 2 Pro + 8개 AMS HT, 총 24 슬롯 지원.
- 출처: https://us.store.bambulab.com/en/products/h2s, https://github.com/bambulab/BambuStudio/releases/tag/v02.00.00.95

## 3. Process 프로파일 — Seam/Scarf/Fuzzy/Wall 키

소스: `src/libslic3r/PrintConfig.cpp`, `resources/profiles/BBL/process/fdm_process_common.json`

| 키 | 허용값 / 단위 | 비고 |
|----|---------------|------|
| `seam_position` | `nearest`, `aligned`, `back`, `random` | |
| `seam_gap` | percent | |
| `seam_slope_type` | `none`, `external`, `all` | scarf 전체 토글 (process 측) |
| `seam_slope_conditional` | `0` / `1` | bool — Smart scarf application |
| `scarf_angle_threshold` | int, `0..180` | Smart scarf 각도 임계 |
| `seam_slope_entire_loop` | `0` / `1` | "Scarf around entire wall" |
| `seam_slope_steps` | int, min `1` | scarf ramp 분할 단계 |
| `seam_slope_inner_walls` | `0` / `1` | 내벽까지 scarf 적용 여부 |
| `seam_slope_start_height` | mm 또는 `%` (layer_height 기준) | |
| `seam_slope_gap` | mm 또는 `%` (nozzle_diameter 기준) | |
| `seam_slope_min_length` | mm | `0`이면 scarf 비활성화 |
| `override_filament_scarf_seam_setting` | `0` / `1` | bool — process 값으로 filament scarf 덮어쓰기 |
| `fuzzy_skin` | `none`, `external`, `all`, `allwalls`, `disabled_fuzzy` | |
| `fuzzy_skin_noise_type` | `classic`, `perlin`, `billow`, `ridgedmulti`, `voronoi` | |
| `fuzzy_skin_mode` | `displacement`, `extrusion`, `combined` | |
| `wall_sequence` | `inner wall/outer wall`, `outer wall/inner wall`, `inner-outer-inner wall` | |

⚠️ Legacy 주의: `wall_infill_order`는 로딩 시 자동 매핑되지만 신규 JSON 생성에는 `wall_sequence`를 써야 함.

출처:
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json

## 4. Filament 프로파일 — Seam/Scarf/온도 키

소스: `src/libslic3r/PrintConfig.cpp`, `resources/profiles/BBL/filament/fdm_filament_common.json`, `Bambu PLA Basic @base.json`, `Bambu PLA Basic @BBL H2S.json`

| 키 | 허용값 / 단위 | 비고 |
|----|---------------|------|
| `filament_scarf_seam_type` | `none`, `external`, `all` | array (variant-aware) |
| `filament_scarf_height` | mm 또는 `%` (layer_height 기준) | array |
| `filament_scarf_gap` | mm 또는 `%` (nozzle_diameter 기준) | array |
| `filament_scarf_length` | mm (`0`이면 비활성) | array |
| `nozzle_temperature` | int array, °C | |
| `nozzle_temperature_initial_layer` | int array, °C | |
| `nozzle_temperature_range_low` | int array, °C | |
| `nozzle_temperature_range_high` | int array, °C | |

⚠️ **흔한 실수**: 일부 가이드/스크린샷에서 보이는 `scarf_seam_type`, `scarf_start_height`, `scarf_slope_gap`, `scarf_length`는 **Bambu Studio filament JSON의 현재 키가 아님**. 항상 `filament_scarf_*` prefix 사용.

⚠️ **배열 길이**: H2S 프로파일은 Standard / High Flow variant 배열을 쓴다. variant-aware 필드(속도/온도/scarf)는 부모 프로파일의 해당 키 길이를 읽어 맞추는 편이 견고. 단일 값만 넣어도 Studio가 보정할 수는 있으나 자동 생성 스킬은 명시적 길이 매칭 권장.

출처:
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/fdm_filament_common.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40base.json

## 5. inherits 사용법과 권장 Base 체인

`inherits`는 부모 프리셋명. 저장 시 부모와 다른 키만 JSON에 저장되고, 로딩 시 부모 config 적용 후 child config가 apply된다.

### Process 체인

```text
사용자 preset
  → 0.20mm Standard @BBL H2S
    → fdm_process_single_0.20
      → fdm_process_single_common
        → fdm_process_common
```

### Filament 체인 (PLA Basic 예시)

```text
사용자 preset
  → Bambu PLA Basic @BBL H2S
    → Bambu PLA Basic @base
      → fdm_filament_pla
        → fdm_filament_common
```

### Machine
- **생성하지 말 것.** 시스템 `Bambu Lab H2S 0.4 nozzle`을 그대로 참조.

출처:
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/Preset.hpp
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/Preset.cpp

## 6. 권장 최소 JSON 형태

### Process (튜닝 필드만)
```json
{
  "type": "process",
  "name": "My H2S 0.20mm tuned process",
  "inherits": "0.20mm Standard @BBL H2S",
  "from": "user",
  "compatible_printers": ["Bambu Lab H2S 0.4 nozzle"],
  "seam_position": "aligned",
  "override_filament_scarf_seam_setting": "1",
  "seam_slope_type": "external",
  "seam_slope_conditional": "1",
  "seam_slope_start_height": "10%",
  "seam_slope_gap": "0%",
  "seam_slope_min_length": "10",
  "wall_sequence": "inner wall/outer wall"
}
```

### Filament (튜닝 필드만)
```json
{
  "type": "filament",
  "name": "My PLA @BBL H2S",
  "inherits": "Bambu PLA Basic @BBL H2S",
  "from": "user",
  "compatible_printers": ["Bambu Lab H2S 0.4 nozzle"],
  "filament_scarf_seam_type": ["external"],
  "filament_scarf_height": ["10%"],
  "filament_scarf_gap": ["0%"],
  "filament_scarf_length": ["10"],
  "nozzle_temperature": ["220"],
  "nozzle_temperature_initial_layer": ["220"]
}
```

## 7. inherits vs 전체 필드 명시 트레이드오프

**inherits 기반 (권장)**
- 장점: Bambu 공식 H2S/AMS/노즐/펌웨어 업데이트를 자동 반영. JSON 작고 schema 변경에 덜 취약.
- 단점: 부모 프로파일 업데이트 시 결과가 미세하게 변경 가능. 재현성 엄격 고정 필요 시 생성 시점 부모 버전 기록 필요.

**전체 필드 명시**
- 장점: 생성 당시 동작 고정, 독립 실행형 프리셋.
- 단점: v2.x schema 변화, H2S variant 배열, AMS HT/AMS 2 Pro 관련 필드 변화를 직접 추적해야 함. outdated 키 섞일 위험.

## 8. Surface Quality 관련 필드 (2026-05-16 v2 확장)

> Source: Codex research run `a25261e23b21252b2` (score 24/25)
> 추가 배경: surface-first 정책 풀 적용 (seam 은닉 + 표면 매끈 + 속도 무시). 자세한 정책 결정 트리는 `references/surface-recipes.md` 참조.

### 8.1. Ironing 필드 (top surface 마감)

| 키 | enum / 단위 | default | 출처 (file:line 또는 URL) |
|----|-------------|---------|--------------------------|
| `ironing_type` | enum: `no ironing` (default 표기), `top_surfaces`, `topmost_only`, `all_solid` | `"no ironing"` | fdm_process_common.json:57-61; Orca wiki https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_ironing.html |
| `ironing_flow` | `%` (line flow 대비) | `10%` (H2S 0.20 override `15%`) | fdm_process_common.json:57; 0.20mm Standard @BBL H2S.json:41 |
| `ironing_spacing` | `mm` (line spacing) | `0.15` mm | fdm_process_common.json:59 |
| `ironing_speed` | `mm/s` | `30` mm/s | fdm_process_common.json:60 |
| `ironing_inset` | `mm` (외벽에서 들여서 시작하는 거리) | `0.21` mm | fdm_process_common.json:58; https://github.com/bambulab/BambuStudio/releases/tag/v01.10.00.74 (lines 213-215) |

### 8.2. Top / Bottom Surface 필드

| 키 | enum / 단위 | default | 출처 (file:line 또는 URL) |
|----|-------------|---------|--------------------------|
| `top_surface_pattern` | enum: `monotonic`, `monotonicline`, `concentric`, `archimedean`, `hilbert` | `monotonicline` | fdm_process_common.json:167 |
| `top_surface_speed` | `mm/s` | common `30`; H2S 0.20 Standard `200`; 0.12 HQ `150` | fdm_process_common.json:169-170; 0.20mm Standard @BBL H2S.json; 0.12mm High Quality @BBL H2S.json |
| `top_surface_acceleration` | `mm/s²` | H2S default `2000` | 0.20mm Standard @BBL H2S.json:165-167; 0.12mm High Quality @BBL H2S.json:146-168 |
| `top_solid_infill_flow_ratio` | float (1.0 = 100%) | `1` | fdm_process_common.json:172-174 |
| `bridge_flow` | float | common `0.95`; single 0.12/0.20 override `1` | fdm_process_common.json:12; fdm_process_single_0.12.json:9 |
| `bridge_speed` | `mm/s` | common `25`; H2S profiles `50` | fdm_process_common.json:14-16; 0.20mm Standard @BBL H2S.json:9-12 |

### 8.3. Wall / Travel / Resolution 필드

| 키 | enum / 단위 | default | 출처 (file:line 또는 URL) |
|----|-------------|---------|--------------------------|
| `reduce_crossing_wall` | `0` / `1` (bool) | `0` (surface-first에서는 `1` 권장) | fdm_process_common.json:100; source: src/libslic3r/PrintConfig.cpp |
| `avoid_crossing_wall_includes_support` | `0` / `1` (bool) | `0` | fdm_process_common.json:76; source: src/libslic3r/PrintConfig.cpp |
| `resolution` | `mm` (gcode arc/segment resolution) | 로컬 default `0.012`; source default `0.01`; normalize min `0.001` | fdm_process_common.json:103; source: src/libslic3r/PrintConfig.cpp:188-189, 278-282 |

### 8.4. Spiral / Seam Placement 필드

| 키 | enum / 단위 | default | 출처 (file:line 또는 URL) |
|----|-------------|---------|--------------------------|
| `spiral_mode` | `0` / `1` (bool) | `0`; `1`로 켜면 normalize가 `wall_loops=1`, `top_shell_layers=0`, `sparse_infill_density=0` 강제 | fdm_process_common.json:123; source: src/libslic3r/PrintConfig.cpp:277-282 |
| `seam_placement_away_from_overhangs` | `0` / `1` (bool) | `0` | fdm_process_common.json:106; source: src/libslic3r/PrintConfig.cpp |

### 8.5. Seam Slope (scarf) 추가 필드 — 검증 필요

§3 표에 키 자체는 enumerate되어 있으나, 로컬 `fdm_process_common.json` 기본값이 누락된 항목. PrintConfig.cpp 또는 exported preset 재확인 (BACKLOG `Surface-first 후속 검증` 항목 (b) 참조).

| 키 | enum / 단위 | default | 출처 (file:line 또는 URL) |
|----|-------------|---------|--------------------------|
| `seam_slope_steps` | int (min `1`) | `10` (커뮤니티/Orca wiki 권장 기본; 로컬 fdm_process_common 미확인 — BACKLOG (b) 검증) | references/seam-recipes.md §2 표 `Scarf steps`; source: src/libslic3r/PrintConfig.cpp |
| `seam_slope_entire_loop` | `0` / `1` (bool) | `0` (Off — Bambu 공식 권장; 로컬 fdm_process_common 미확인 — BACKLOG (b) 검증) | references/seam-recipes.md §2 표 `Scarf around entire wall`; source: src/libslic3r/PrintConfig.cpp |
| `seam_slope_inner_walls` | `0` / `1` (bool) | `0` (외벽 한정 권장 — vent pipe Finding 2 실측; 로컬 fdm_process_common 미확인 — BACKLOG (b) 검증) | references/seam-recipes.md Finding 2; source: src/libslic3r/PrintConfig.cpp |

### 8.6. surface-first 모드 변경 핵심 요약

- 회전체 default: `seam_position: random + seam_slope_entire_loop: 1` (분산) → **Auto-select 결정 트리 (spiral_mode → painted seam → random fallback)** (은닉). 자세한 결정 트리는 `surface-recipes.md` 참조.
- Ironing 정책 신규 추가: PLA Basic/Matte/PLA Silk + flat top 한정. PETG/PC/TPU/CF류는 비추.
- 외벽 매끈함 공통값: `layer_height 0.08-0.12`, `wall_loops 3-4`, `outer_wall_speed 20-40 mm/s`, `reduce_crossing_wall 1`, `resolution 0.006-0.010`.

## 9. 미해결 / 검증 필요

- `master`는 2.6.0 이후 142 commits 진행 중 → 2.6.0 설치 번들 내장 JSON과 완전 동일 보장 아님. 안정판 tag/asset 내부 프로파일 직접 추출하여 diff 권장.
- 공식 문서가 "process에서 scarf override 시 filament 충돌 우선순위"를 명시하지 않음. 소스/UI 명칭상 `override_filament_scarf_seam_setting=1`이면 process의 `seam_slope_*`가 제어한다고 보는 것이 합리적.
- H2S + AMS HT + AMS 2 Pro 조합은 별도 machine preset명이 아님. 장치 동기화/AMS 구성으로 처리되며 별도 "H2S AMS HT + AMS 2 Pro" machine JSON은 공식 repo에서 미확인.
