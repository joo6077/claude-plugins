# Surface-first 레시피 (Bambu Studio H2S)

> Last updated: 2026-05-16
> Source: Codex research run `a25261e23b21252b2` (score 24/25)
> Bambu Studio reference version: 2.6.0 (v02.06.00.51)
> Sibling references: `seam-recipes.md` (seam 전용), `bambu-fields-baseline.md` §8 · §10 (필드 enum/default), `materials.md` (소재 카탈로그), `failure-recipes.md` (**실측 실패 후 사후 대응** — 이 파일은 사전 정책이다)
>
> **2026-08-13 정정 (카이젠 Phase 13):** `layer_height` `0.08` 의 공식 근거 표기 · `enable_arc_fitting` 성격 · `resolution` 적용 축 3 건. 근거: `.harness/.meta/evidence/phase13.md`

스킬이 사용자 의도가 "완벽한 표면 + seam이 안 보임 + 속도 무시"일 때 참조. seam 분산 전략(이전 default)이 아닌 **은닉(invisible) 전략**과 외벽/Top·Bottom/Ironing 정책을 함께 다룬다.

## 1. Surface-first 모드 개요

### 트리거 조건

다음 중 하나면 surface-first 모드 ON:
- 사용자가 "표면 매끈하게", "심 안 보이게", "완벽한 표면", "퀄리티 우선", "속도 신경 안 씀" 같은 요구를 명시
- 모델이 외관 prototype, 피규어, 장식품, 케이스 외관, 회전체 화병/컵
- 사용자가 직접 surface-first 키워드 사용

### 우선순위

1. **seam 은닉 ≥ 외벽 매끈** > top 마감 > 강도/치수 > 시간
2. 속도는 무시 (단, 너무 느린 PETG/PC/ABS는 열 축적/warping 부작용 별도 관리)
3. 안전성 (PETG 건조, CF 노즐 호환)은 항상 우선

### 출력 시간 예상

- 일반 0.20mm Standard 대비 **2~4배** 늘어남 (0.12mm + outer 30mm/s + wall 3 + ironing)
- 사용자에게 시간 추정치 사전 고지

## 2. 형상별 결정 트리 (Auto-select)

스킬이 모델 형상을 분석한 후 다음 순서로 자동 판정. 모호하면 사용자에게 옵션 제시.

### 2.1. 회전체 / 원기둥 / 컵 / 화병 (v3 — 자동화 우선)

```text
회전체 모델 감지
  ※ 우선순위 원칙: 사용자 추가 작업이 없는 옵션이 default top.
  │
  ├─ (1) spiral_mode 적용 가능한가?
  │      조건: 단일 외벽, top 없음, infill 불필요, 멀티컬러 아님
  │      YES → spiral_mode = 1
  │             (wall_loops=1, top_shell_layers=0, sparse_infill_density=0 자동 강제)
  │             seam: 없음 (Z축 연속 나선이라 진짜 무 seam)
  │             사용자 작업: 없음
  │
  ├─ (2) DEFAULT — random 분산 전략 (자동, 사용자 작업 X)
  │      seam_position = random + seam_slope_entire_loop = 1
  │      + scarf external + length 15-20mm, gap 5-10%, height 0-10%, steps 10
  │      → wheel/원통 둘레 전체에 ramp 분산, 한 줄 라인 없이 specks
  │      → spoke/텍스처 구조에 자연 위장
  │      트레이드오프: micro-banding (specks)
  │      seam-recipes.md Real-world Finding 1 (vent pipe에서 random > aligned 검증) 적용
  │      사용자 작업: 없음
  │
  └─ (3) 사용자가 명시적으로 "specks도 싫고 완벽한 클린 면" 요청 시에만 OPT-IN
         → seam_position = aligned (또는 back)
         + 사용자가 Studio UI에서 seam paint tool로 숨김 영역 페인팅 필수
         + scarf external + length 15-20mm, gap 5-10%, height 0-10%, steps 10
         ※ painted 안 하면 visible 면에 한 줄 라인 그대로 남음 (위험)
         사용자 작업: 필수 (Studio UI 페인팅 5-10분)
```

v3 변경 사유: v2에서는 painted를 default top에 두었으나 (페리스 휠 dogfood 케이스에서) 사용자가 페인팅 부담을 직관에 위배된다고 피드백 → 자동화 우선 원칙으로 painted는 명시적 요청 시에만 OPT-IN.

### 2.2. 박스 / 직육면체

- `seam_position`: **back** (또는 aligned)
- Sharp corner에 seam 숨김 + 필요 시 painted seam으로 코너 강조
- scarf: 일반적으로 off 또는 length 5-8mm (corner sharpness 보존)
- random 금지 (평평한 면에 specks 분산되면 외관 ↓)

### 2.3. 유기적 곡면 / 피규어

- `seam_position`: aligned (back 방향 우선)
- Studio UI seam paint로 후면, 주름, 접합부, 머리카락 텍스처에 페인팅
- scarf: `Contour` (외벽만), length 10-15mm, gap 5-10%, height 0-10%, steps 10
- Smart scarf는 각도 판정 흔들리면 Off 고려 (seam-recipes.md §1 참조)

### 2.4. 얇은 벽 / 미세 디테일

- `seam_position`: aligned
- scarf: 짧게 (length 5-10mm) 또는 off — scarf ramp가 얇은 벽 형상 침범
- `wall_loops`: 1-2 (Arachne wall generator 검토)
- 작은 홀에는 `Contour and Hole` 비추 (내경 치수 영향)

### 2.5. 평면 top 강조 (도구, 케이스 lid, 박스 top)

- seam은 후면/코너에 숨김 (위 §2.2 박스 규칙)
- **Top surface 품질이 외벽보다 더 중요** — outer 속도보다 top 속도/flow에 집중
- Ironing **적극 적용** (§5 참조)
- `top_surface_pattern`: `monotonicline` 또는 원형이면 `concentric` 실험

### 2.6. Spiral vase 가능 모델

- 단일 외벽 / top 없음 / infill 없음 / 멀티컬러 아님 만족 시
- `spiral_mode = 1`
- 다른 설정(seam_position, scarf, ironing)은 무의미 — 슬라이서가 normalize에서 무시
- 단점: 강도 ↓ (외벽 1겹), top 없음 (밀폐 불가), 멀티컬러 불가

## 3. 외벽 표면 권장값 (공통)

H2S 0.4 hardened nozzle 기준. 모든 단위 명시.

| 항목 | Surface-first 값 | 기본 baseline | 근거 |
|----|----|----|----|
| `layer_height` | **`0.12` mm 1 차 권장** (전 형상). 회전체/유기적에서 계단이 핵심이고 시간을 감수할 때만 `0.08-0.12` mm, 큰 평면 `0.12-0.16` mm | H2S 0.20 Standard | `0.12`: 0.12mm High Quality @BBL H2S.json (공식 체인 실재). **`0.08` 은 이 파일의 공식 근거가 아니다** — `min_layer_height 0.07` 하한 위라는 것만 확인되고 H2S 공식 0.08 process 프로파일 근거는 `[미확인]` (`bambu-fields-baseline.md` §10.1) |
| `wall_loops` | `3` (표면 우선) ~ `4` (강도까지 우선) | `2` (fdm_process_common) | fdm_process_common.json |
| `outer_wall_speed` | `20-40` mm/s (PLA/PETG), `15-25` (Silk), `20-30` (PA/PC/ABS), `10-20` (TPU) | H2S 0.12 HQ `60` mm/s | 0.12mm High Quality @BBL H2S.json |
| `inner_wall_speed` | outer의 `2-3배` 이하 (예: outer 30 → inner 60-90) | H2S 0.12 HQ `90` mm/s | 동일 |
| `wall_sequence` | `inner-outer-inner wall` 기본; 박스 sharp 치수 우선만 `inner wall/outer wall` | `inner wall/outer wall` | fdm_process_common.json:58 (enum) |
| `reduce_crossing_wall` | `1` | `0` | fdm_process_common.json:100 |
| `enable_arc_fitting` | `1` (**기본값 유지 — 표면 품질 카드가 아니다**) | `1` | fdm_process_common.json:29. ⚠️ 이것은 품질 개선 기능이 아니라 **G-code encoding 변경**(직선 세그먼트 → arc 명령)이며 firmware arc segmentation 리스크가 있다. 곡면 계단(Z) 해결책으로 제시하지 마라 — `failure-recipes.md` §1.2 |
| `resolution` | `0.006-0.010` mm | `0.012` mm | fdm_process_common.json:103. ⚠️ **XY 세그먼트 해상도 전용** — Z 계단의 주 해결책이 아니다 (`failure-recipes.md` §1.2) |
| flow ratio | 소재/색상별 calibration 후 적용 (PLA Basic 기본 `0.98`) | 동일 | Bambu PLA Basic @BBL H2S.json:29-42 |
| Pressure Advance (PA) | 소재/노즐/건조 후 PA profile 저장 필수 (Bambu Studio Calibration → PA test) | — | Bambu 공식 calibration 가이드 |

### 소재별 외벽 보정 (matrix)

| 소재 | outer wall (mm/s) | layer (mm) | 추가 보정 |
|----|----|----|----|
| PLA Basic | `25-40` | `0.08-0.12` | 가장 예측 가능. ironing 적극 |
| PLA Matte | `25-40` | `0.08-0.12` | layer line 가장 잘 숨음. 표면 매끈함 최강 |
| PLA Silk | `15-25` | `0.10-0.12` | 광택 보존 위해 더 느림. ironing은 topmost_only만 (광택 죽음 주의) |
| PETG HF | `20-35` | `0.12` | **AMS HT 65°C 8h 사전 건조 + continuous drying 필수**. fan 20-50% 유지 |
| PA-CF / PAHT-CF | `20-30` | `0.12` | fiber 질감으로 완전 매끈함 한계. **AMS HT 80°C 8h 건조 + hardened nozzle 필수** |
| PC | `20-30` | `0.12` | 건조 필수 (chamber 60°C). ooze 많으면 외벽 first wipe |
| ABS / ASA | `25-35` | `0.12` | enclosure + brim. 후가공(vapor smoothing) 가능 |
| TPU | `10-20` | `0.16-0.20` | scarf/ironing 비추. layer 두껍게 가도 됨 (유연성 우선) |

⚠️ 위 표의 `layer` 열에 나오는 `0.08-0.12` 범위는 **`0.12` 를 1 차값으로 읽는다.** `0.08` 쪽 끝은
`min_layer_height 0.07` 하한 위라는 것만 확인된 비공식 영역이고 H2S 공식 process 프로파일 근거는
`[미확인]` 이다 (`bambu-fields-baseline.md` §10.1). 사용자에게 시간 배수(레이어 수 `기존/신규` 배)를
고지하고 선택을 받은 뒤에만 `0.08` 로 내려라 — 자동으로 밀어넣지 마라.

## 4. Top / Bottom 표면 권장값

| 항목 | Surface-first 값 | 기본 baseline | 근거 |
|----|----|----|----|
| `top_shell_layers` | `0.12mm`: 7-9, `0.16mm`: 6, `0.20mm`: 5-6 | common `3`, single 0.12 `5` | fdm_process_common.json:7-16; fdm_process_single_0.12.json:26-47 |
| `bottom_shell_layers` | `4-6` | common `3` | fdm_process_common.json |
| `top_surface_pattern` | 기본 `monotonicline`; 원형 top은 `concentric` 실험; `archimedean`/`hilbert`는 의도적 텍스처일 때만 | `monotonicline` | fdm_process_common.json:167 |
| `top_surface_speed` | PLA `20-40`, PETG `15-30`, PA/PC/ABS `20-30`, TPU `10-20` mm/s | H2S 0.20 `200`, 0.12 HQ `150` mm/s | 0.12mm High Quality @BBL H2S.json:146-168 |
| `top_surface_acceleration` | `500-1000` mm/s² | H2S `2000` mm/s² | 0.20mm Standard @BBL H2S.json:165-167 |
| `top_solid_infill_flow_ratio` | calibration 후 `1.00` 기본; gap 시 `+0.02`, ridge 시 `-0.02` | `1` | fdm_process_common.json:172-174 |
| `bridge_flow` | `1.0` 유지; 외관 노출 bridge는 `0.95-1.0` | common `0.95`, override `1` | fdm_process_common.json:12; fdm_process_single_0.12.json:9 |
| `bridge_speed` | `20-30` mm/s | common `25`, H2S `50` | fdm_process_common.json:14-16 |

## 5. Ironing 형상×소재 매트릭스

`ironing_type` enum: `no ironing`, `top_surfaces`, `topmost_only`, `all_solid`. surface-first 권장은 대부분 `topmost_only` (외벽 주변 과다 ironing 회피).

### 5.1. 소재별 ironing 정책 (필수 enumerate)

| 소재 | ironing_type | ironing_speed (mm/s) | ironing_flow (%) | ironing_spacing (mm) | ironing_inset (mm) | 판정 |
|----|----|----|----|----|----|----|
| **PLA Basic** | `topmost_only` 또는 `top_surfaces` | `15-20` | `10-15%` | `0.10-0.15` | `0.21-0.42` | **적극 권장** |
| **PLA Matte** | `topmost_only` | `15-20` | `8-12%` | `0.10-0.15` | `0.21-0.42` | **권장**, 과하면 chalky 변색 |
| **PLA Silk** | `topmost_only` only | `10-15` | `5-10%` | `0.10-0.15` | `0.3-0.5` | 광택 죽을 수 있음 — 실측 후 결정 |
| **PETG HF** | 원칙 `no ironing`, 평면 장식만 `topmost_only` | `10-15` | `5-8%` | `0.15-0.20` | `0.4-0.6` | **비추** — blob/scar 위험 |
| **PA-CF / PAHT-CF** | `no ironing` | — | — | — | — | **비추** — fiber 질감, 노즐 마모 |
| **PC** | `no ironing` 또는 소형 `topmost_only` 실험 | `10-15` | `5-8%` | `0.15-0.20` | `0.4` | heat creep / ooze 위험 |
| **ABS / ASA** | `topmost_only` 실험 가능 | `15-20` | `8-12%` | `0.12-0.18` | `0.3-0.5` | 후가공(vapor smoothing) 가능하면 ironing 의존 낮춤 |
| **TPU** | `no ironing` | — | — | — | — | **불가** — TPU 유연성으로 표면 drag |

### 5.2. 형상별 ironing 적용성

| 형상 | ironing 적용 | 비고 |
|----|----|----|
| 회전체 / 원기둥 | **무의미** | top이 없음 (cylinder는 위쪽 평면 X). spiral vase면 더더욱 무의미 |
| 박스 / 직육면체 (top 있음) | **강함** | 평면 top에 가장 효과적 |
| 유기적 곡면 | **부분** | 작은 수평 island top만 `topmost_only` |
| 얇은 벽 / 미세 디테일 | **거의 off** | 표면 면적 부족, ironing pass가 detail 침범 |
| 평면 top 강조 | **필수** | surface-first의 핵심 영역 |
| Spiral vase | **무의미** | top_shell_layers=0 강제 |

## 6. 트레이드오프

surface-first 모드를 켜면 발생하는 비용. 모든 사용자에게 사전 고지 필수.

### 6.1. 표면 vs 치수

낮은 outer speed + scarf + ironing + flow 조정은 외관 ↑하지만:
- **Sharp corner / edge sharpness 흐려짐**
- **작은 hole 내경 영향** (`Contour and Hole` 모드 켜면 더 심함)
- 얇은 벽에서 wall 3-4겹 적용 시 형상 깨짐

### 6.2. 표면 vs 강도

- `inner-outer-inner` wall sequence는 외관 ↑하지만 일부 형상에서 벽 접합/overhang 안정성 변화
- scarf ramp 구간은 layer 강도 미세 변화
- 낮은 cooling fan은 광택 ↑하지만 PLA 층간 접착 ↓ 가능

### 6.3. 표면 vs 실패 확률

- **PETG / PC / TPU ironing은 blob, drag mark, clog / heat creep 위험 ↑**
- Smart scarf가 angle/overhang에서 끊기면 표면 불균일 — Off 또는 threshold 낮춤 필요
- PA-CF / PAHT-CF의 0.4mm hardened nozzle은 0.6mm 권장 소재에서 막힘 위험

### 6.4. 표면 vs 시간 / 소재

- 출력 시간 **2~4배** (예: 4시간 → 12시간)
- top_shell 7-9 layers, wall 3-4, calibration coupons → 소재 소모 ↑

### 6.5. 속도 무시 시 부작용

속도 무시는 사용자 명시 요구지만, 너무 느리면:
- **PETG / PC / ABS**: 열 축적 → warping, 광택 불균일, stringing 누적 시간 ↑
- 외벽 50mm/s 미만에서 chamber 온도 관리 필수 (특히 ABS/ASA enclosure)
- 0.04mm 같은 극단적 fine layer는 nozzle ooze 누적 → blob 위험 ↑

## 7. 매끈 표면 TOP 3 소재 (Codex 권장)

1. **PLA Matte** — layer line 은폐 최강. 강도/층간 접착은 PLA Basic보다 보수적
2. **PLA Basic** — calibration, ironing, 낮은 outer speed 가장 예측 가능. 색상 선택 폭 넓음
3. **ABS / ASA** — 출력 난도 ↑, but vapor smoothing 같은 후가공 가능. H2S chamber / 환기 / 수축 관리 필요

비추 (매끈함 목표 한정):
- **PETG HF**: 기능 OK, 단 stringing/blob 의존성 큼
- **PA-CF / PAHT-CF**: fiber 질감으로 완전 매끈 부적합 (다만 "고급 무광" 텍스처로는 매력)
- **TPU**: scarf/ironing 한계로 표면 마감 약함

## 8. 검증 사례 / 출처

### Codex 리서치 근거

- Codex run `a25261e23b21252b2` (2026-05-16, score 24/25)
- Primary sources:
  - Bambu Studio GitHub release `v02.06.00.51`: https://github.com/bambulab/BambuStudio/releases/tag/v02.06.00.51
  - Scarf seam 회귀 이력: 1.10.0 → 1.10.1 hotfix (https://github.com/bambulab/BambuStudio/releases/tag/v01.10.01.50)
  - Bambu PETG HF guide: https://bambulab.com/en-us/filament/petg-hf
  - Bambu PAHT-CF guide: https://bambulab.com/en-us/filament/pa6-cf
  - Bambu ABS/ASA: https://bambulab.com/en-us/filament/abs, /asa
  - Bambu TPU 95A HF: https://bambulab.com/en-us/filament/tpu-95a-hf
  - AMS HT documentation: https://cdn1.bambulab.com/documentation/h2d/en/AMS_HT_20250109.pdf
  - OrcaSlicer Ironing wiki: https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_ironing.html
- 로컬 system profile 출처:
  - `~/Library/Application Support/BambuStudio/system/BBL/process/fdm_process_common.json`
  - `~/Library/Application Support/BambuStudio/system/BBL/process/0.20mm Standard @BBL H2S.json`
  - `~/Library/Application Support/BambuStudio/system/BBL/process/0.12mm High Quality @BBL H2S.json`
  - `~/Library/Application Support/BambuStudio/system/BBL/filament/Bambu PLA Basic @BBL H2S.json`
  - `~/Library/Application Support/BambuStudio/system/BBL/filament/Bambu PETG HF @BBL H2S.json`
  - `~/Library/Application Support/BambuStudio/system/BBL/filament/Bambu PAHT-CF @BBL H2S.json`
  - `~/Library/Application Support/BambuStudio/system/BBL/filament/Bambu PC @BBL H2S.json`

### 후속 검증 필요

`BACKLOG.md` "Surface-first 후속 검증" 섹션 참조:
- precise z-seam JSON 키 매핑
- `seam_slope_steps` / `seam_slope_entire_loop` / `seam_slope_inner_walls` 누락 default 재확인
- Coupon 부족 소재 (PLA Matte/Silk, PC, ASA, PAHT-CF, TPU) 실측
- PETG HF lot/습도 의존성 비교 coupon
- PLA Silk top ironing 광택 불일치 사례 검증
