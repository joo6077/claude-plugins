# Seam / Scarf Seam 레시피 (Bambu Studio H2S)

> Last updated: 2026-05-15
> Source: Codex research run `afcf4968339021b29` (score 25/25)
> Bambu Studio reference version: 2.6.0 (v02.06.00.51)

스킬이 모델 형상 + 선택된 소재에 맞춰 process 측 `seam_*` / `seam_slope_*` + filament 측 `filament_scarf_*` 권장 조합을 도출할 때 참조.

## 1. Scarf seam 메커니즘 — Contour vs All

### Contour
- 외곽 perimeter에만 scarf 적용
- 외관 대비 비용 가장 좋음
- 내부 구멍 seam은 그대로 남음

### Contour and Hole / "All"
- 외곽 + 구멍 주변 내벽까지 확장
- 내경 치수 영향, 작은 디테일 거칠어짐, 시간 ↑

⚠️ **Bambu 1.10 이력**: Bambu Studio 1.10에서 scarf seam이 filament 설정으로 옮겨졌고 PLA Basic/Matte/Silk에 한때 기본 활성화됐다가 **1.10.1에서 기본 비활성화**됨. 이유는 모델 각도 판정에 따라 같은 Z 라인에서 scarf 적용/미적용이 섞여 표면 품질이 불균일해졌기 때문. Bambu 권장 해결책은 `Scarf application angle threshold` 낮추기 또는 `Smart scarf seam application` 끄기.

출처:
- Bambu Studio 1.10 beta: https://github.com/bambulab/BambuStudio/releases/tag/v01.10.00.74
- 1.10.1 hotfix: https://github.com/bambulab/BambuStudio/releases/tag/v01.10.01.50
- Orca seam wiki: https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_seam
- Bambu inside-circle case: https://forum.bambulab.com/t/scarf-seam-does-not-work-on-the-inside-of-a-circle/187310

## 2. 주요 파라미터의 의미

| 파라미터 | 단위 의미 | 기본 시작점 / 권장 |
|---------|---------|-------------------|
| **Scarf length** | mm 절대길이. `0`이면 scarf 비활성 | 커뮤니티 기본 시작점 **20 mm** |
| **Scarf start height** | ramp 시작 Z 오프셋. `%`는 layer height 기준. 예: 0.2 mm layer에서 50%는 0.1 mm | `0%/0 mm` (가장 낮게 시작, 부드러운 블렌드) |
| **Scarf slope gap** | scarf 구간 start/end overlap 주변 gap 보정. nozzle/line 기준 보정 | 커뮤니티 기본 **10%** |
| **Scarf steps** | scarf ramp 분할 단계 | **10** |
| **Scarf around entire wall** | 두 번째 seam 흔적 줄이기 실험값 | **Off** (공식 문서 권장) |

⚠️ Bambu UI에서 `%` 표기는 반드시 `%` 기호를 붙여야 한다는 보고가 있음 (Reddit Bambu guide).

출처:
- Orca wiki: https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_seam
- Reddit optimal settings: https://www.reddit.com/r/OrcaSlicer/comments/1b7lthr/what_are_the_optimal_settings_for_scarf_seams/
- Reddit Bambu guide: https://www.reddit.com/r/3Dprinting/comments/1o6i5a1/how_to_improve_your_seams_on_curved_surfaces/

## 3. 형상별 권장 조합 (0.4mm nozzle / 0.2mm layer 기준)

| 형상 | Process 추천 | Filament scarf 추천 |
|------|-------------|---------------------|
| **회전체/원기둥, 컵, 화병** | `seam_position: aligned` 또는 `back`<br>보이는 면 없는 원통은 `aligned`<br>`wall_sequence: inner-outer-inner`<br>outer wall 60-80 mm/s<br>Preview 확인 | `Contour and Hole / All`<br>start `0%`, gap `10%`, length `20mm`, steps `10`<br>`Scarf around entire wall: Off`<br>Smart 먼저 On, 줄 끊기면 Off |
| **원통 "선 최대한 안 보이게"** | 가능하면 **Spiral vase가 유일한 진짜 무 seam**<br>일반 벽 구조면 위 원통값 + seam 위치를 후면/내측으로 paint | 검증 조합: `Contour and Hole`, `0 mm/0%`, `10%`, `20 mm`, `10 steps`, around entire wall Off |
| **구체/돔** | `aligned back` 또는 painted back<br>Smart가 중간 각도에서 끊기면 Off / threshold 낮춤 | `Contour`, start `0-10%`, gap `10%`, length `10-20 mm`<br>overhang 큰 하부는 scarf 기대 낮춤 |
| **평면 박스/직육면체** | scarf보다 `painted seam` / `back` / `aligned corner`<br>sharp corner에 숨김 | 보통 `None` 또는 `Contour` 짧게 `5-10 mm`<br>All 비추천 |
| **유기적 곡면 / 피규어** | `aligned back` + seam painting (주름/머리카락/후면)<br>wall order inner-first | `Contour`, start `0-10%`, gap `10%`, length `10-20 mm`<br>Smart On 후 Preview 끊기면 Off |
| **얇은 벽 / 미세 디테일** | seam painting 우선, `nearest`는 시간 절약용<br>작은 홀에는 scarf 확장 주의 | `Contour` 또는 `None`<br>length `5-10 mm`, start `5-10%`, gap `5-10%`<br>All/holes는 치수·내벽 흔적 위험 |

검증 출처:
- MakerWorld 원통 테스트: https://makerworld.com/en/models/1886187-scarf-seam-test-cylinder-with-hole
- Reddit 검증: https://www.reddit.com/r/OrcaSlicer/comments/1b7lthr/what_are_the_optimal_settings_for_scarf_seams/

## 4. 소재별 scarf 적용성 보정

| 소재 | scarf 적용성 | 추천 보정 |
|------|------------|----------|
| **PLA** | 좋음 | 기본값. Matte/CF는 더 잘 숨음. **Silk**는 length `10-15 mm`, 속도 ↓ |
| **PETG** | 중간 | **반드시 건조**. gap `10-15%`, length `15-20 mm`, outer/scarf 속도 `50-70 mm/s` |
| **ABS** | 중간 | enclosure + PA 보정. length `10-15 mm`, gap `10%` |
| **ASA** | 중간 | ABS와 동일. 외관물은 painted/back + Contour |
| **PC** | 중간 ↓ | **건조 필수**. ooze 많으면 scarf Off + painted seam. 쓰면 length `10-15 mm`, gap `10-15%` |
| **PA-CF / PAHT-CF** | 좋음 (건조 전제) | **건조 필수**, hardened nozzle. `Contour`, length `10-15 mm`, gap `10%` |
| **TPU** | 낮음 | **기본 `None`**. 필요 시 `Contour`, length `5-10 mm`, 매우 느린 외벽. 대안: vase mode, painted seam, fuzzy skin |

소재 적용성 출처:
- PLA 1.10 default: https://github.com/bambulab/BambuStudio/releases/tag/v01.10.00.74
- Silk 표면 흔적 community note: https://www.reddit.com/r/OrcaSlicer/comments/1jybcrh/question_about_seams/
- Bambu filament guide: https://bambulab.com/en-us/filament-guide
- Bambu PA6-CF 건조: https://bambulab.com/en-us/filament/pa6-cf
- MakerWorld TPU preset (`Scarf seam type: None`): https://makerworld.com/it/models/661830-perfect-tpu-print-settings

## 5. 흔한 실패 모드와 회피

| 실패 모드 | 원인 | 회피 |
|----------|------|------|
| **scarf가 아예 안 걸림** | filament profile의 scarf type이 `None`, 또는 1.10 이후 슬롯/프로파일 버그 | Preview에서 적용 여부 확인 필요 |
| **중간부터 세로 줄 재등장** | Smart scarf가 각도/overhang 판단으로 일부 레이어만 적용 | `scarf_angle_threshold` ↓ 또는 Smart Off |
| **blob** | PA 낮음, ooze, 온도 과다, slope gap 부족 | PA 보정, gap 10-15%, 외벽 전 wipe + inner-first wall order |
| **underextrusion / gap** | PA 과다, start height/gap 과다, flow ratio 낮음 | start height 0-10%, gap ↓, flow 100% |
| **거친 패치 / 두 번째 선** | scarf start와 end가 분산되어 length만큼 떨어진 두 흔적 발생 | length ↓ 또는 `Scarf around entire wall` 실험 (대신 print time + 거친 면 ↑) |

출처:
- Bambu forum scarf 안 걸림: https://forum.bambulab.com/t/scarf-joints-doesnt-seam-to-always-work/157900
- Smart scarf 회귀: https://github.com/bambulab/BambuStudio/releases/tag/v01.10.01.50
- Reddit guide update: https://www.reddit.com/r/3Dprinting/comments/1phmaak/how_to_improve_your_seams_on_curved_surfaces/

## 6. 옵션별 트레이드오프

- **Scarf On**: 원통/곡면 외관 ↑, print time 약간 ↑. start/end 두 지점이 거친 패치로 보일 수 있음. PA/건조/속도 튜닝 안 되면 일반 seam보다 나빠짐.
- **Scarf Off**: 예측 가능, 치수/코너 깨끗. 원통에는 세로 seam line 잔존.
- **Contour**: 외관 대비 비용 best. 내부 구멍 seam은 잔존.
- **All / Contour and Hole**: 구멍/내벽까지 개선, 시간 ↑, 내경 치수 영향, 작은 디테일 거칠어짐.
- **Painted/Aligned**: 실패 가능성 ↓, 박스/피규어에 강함. 완전 원통에는 "위치 이동"일 뿐 제거 아님.
- **Scarf around entire wall**: 두 번째 seam 흔적 줄이는 실험. 공식 문서는 보통 Off 권장. 시간 + 전체 벽 질감 변화가 대가.

## 7. 미해결 / 검증 필요

- Bambu Studio 최신 UI의 `All`이 내부적으로 `Contour and Hole`과 완전 동일한지, inner wall scarf까지 더 넓게 켜는지 버전별 확인 필요.
- 소재별 정량 강도 데이터 부족. "scarf가 seam 강도 약간 개선" 문서 설명은 있으나 PLA/PETG/PA-CF별 파단 테스트 충분하지 않음.
- PETG, PC, TPU에서 최적 `start height`는 필라멘트 브랜드 + 건조 상태 의존성 큼. 같은 값이 재현되지 않을 수 있음.
- Bambu Smart scarf angle/overhang threshold는 모델 형상별 적용/미적용 경계가 생김. 원통처럼 표면 균일성 중요한 출력은 **Preview 확인 후 Smart Off가 더 안정적**.

## Real-world findings (2026-05-15)

스킬 v1 테스트 출력에서 얻은 실측 데이터 — Codex 이론과 다르거나 보강할 점.

### Finding 1: 회전체 vent pipe에서 random > aligned (시각적)

**상황**: H2S + PETG HF + 0.4mm + 30×30×35mm 쿠폰 (4 wall, hollow tube), `seam_slope_entire_loop: 1` + `seam_slope_type: all` 적용.

**Codex 이론**:
> 외관 우선은 `aligned_back` 또는 `back` + painted seam, 전방향 노출 원통은 `aligned` + entire_loop 테스트가 낫습니다.

**실측 결과**:
- `seam_position: aligned`: 외벽 한쪽에 미세 수직 라인 (광택 변화) **눈에 띔**
- `seam_position: random`: 외벽 둘레에 작은 specks 분산 **덜 거슬림**

**결론**: 전방향 노출 회전체에서 random + entire_loop가 visually 더 깔끔. 단 micro-banding 같은 specks 트레이드오프 수용해야.

**적용 권장**: 회전체 모델에서 default = `seam_position: random` + scarf entire_loop 콤보.

### Finding 2: `seam_slope_type: external`로 충분 (내벽 scarf 불필요)

**상황**: 동일 쿠폰. 처음 `all` (외+내벽 scarf) → 사용자 피드백 "내벽은 어차피 안 보이는데 scarf 처리 비효율" → `external` 로 전환.

**결과**: 외부 표면 시각 차이 없음 (외벽은 같은 scarf 처리). 내벽엔 일반 seam 1줄 → vent pipe처럼 외부만 보이는 케이스에서 가성비 ↑.

**적용 권장**: 외부만 cosmetically 중요한 회전체에서 `seam_slope_type: external` + `seam_slope_inner_walls: 0`. all 모드는 양면 cosmetic 필요할 때만.

### Finding 3: `wipe_on_loops`는 Bambu에 없음 (Orca only)

**가설**: 외벽 perimeter 끝 wipe를 안쪽으로 향하게 해서 stringing/blob을 내부로 묻음.

**Codex 검증 (`a06a8ac153247d901`)**: Bambu Studio v2.6.0 PrintConfig.cpp에 `wipe_on_loops` **없음**. Orca 전용. Bambu의 `wipe`/`wipe_distance`는 retract 시 wipe용 (방향성 wipe 아님).

**결론**: scarf wipe 방향 제어는 Bambu에서 직접 못 함. Bambu의 seam-hide 한계는 `seam_slope_type` + `seam_slope_entire_loop` + `seam_position` 조합이 max.

### Finding 4: PETG HF + entire_loop 조합 stringing 민감

**상황**: PETG HF + `seam_slope_entire_loop: 1` 출력에서 stringing 다수 발생.

**원인 분석**:
- entire_loop는 perimeter당 scarf ramp 길어서 travel/direction change 증가
- PETG는 흡습성 강함 — 건조 부족 시 stringing 폭발
- PETG HF의 nozzle temp 250°C 상단은 과압출 위험

**적용 권장**:
- PETG HF + entire_loop 콤보는 반드시 **AMS HT 65°C 8h 사전 건조 + continuous drying** 전제
- nozzle_temperature: 245°C 권장 (TDS 245-250 하단)
- 건조 환경 의심되면 entire_loop 끄고 일반 seam으로 fallback

### Finding 5: TPU에 scarf 비추 — 이미 검증된 사항 재확인

vent pipe 모델의 sealing ring은 TPU 90A로 출력. `filament_scarf_seam_type: ["none"]` 적용. 정상 출력 (이건 Codex가 이미 예측한 대로).
