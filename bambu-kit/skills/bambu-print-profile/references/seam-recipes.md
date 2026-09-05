# Seam / Scarf Seam 레시피 (Bambu Studio H2S)

> Last updated: 2026-05-16 (v2 — surface-first 정책 추가)
> Source: Codex research run `afcf4968339021b29` (score 25/25, v1 기반) + run `a25261e23b21252b2` (score 24/25, v2 surface-first 정책)
> Bambu Studio reference version: **런타임에 조회한다 — 이 줄에 버전을 하드코딩하지 마라.**
>   앱 `/Applications/BambuStudio.app/Contents/Info.plist` · 프로파일 번들
>   `~/Library/Application Support/BambuStudio/system/BBL.json` 의 `version`.
>   두 값은 **따로 갱신된다** (프로파일은 앱과 무관하게 네트워크로 갱신). 조회 절차는 `SKILL.md` §환경 검증.
>   최초 작성 시점 기준: 앱 `02.06.00.51` / 번들 `02.06.00.05`. 2026-09-05 확인: 앱 `02.08.02.61` / 번들 `02.08.00.06`, H2S 0.4 앵커값 10/10 동일.

스킬이 모델 형상 + 선택된 소재에 맞춰 process 측 `seam_*` / `seam_slope_*` + filament 측 `filament_scarf_*` 권장 조합을 도출할 때 참조.

## 0. Surface-first 모드 — 회전체 default 정책 (2026-09-05 v4)

> v4 근거: Codex research D/E (2026-09-05, foreground read-only) + 설치본 `02.08.02.61` 소스·바이너리 추적.
> 결정 트리 본문은 [`surface-recipes.md`](./surface-recipes.md) §2.1 과 동일하게 유지한다.

### v4 의 전제 — random 은 해결책이 아니다

Prusa 공식 KB 는 spiral vase 가 아닌 이상 모든 perimeter loop 에 시작/끝점이 있고 그것이 seam 이
된다고 명시한다. `random` 은 **한 줄을 표면 전체의 specks 로 바꾸는 것**이지 seam 을 없애지 않는다.

### 사용자 피드백 두 건 — 모순이 아니다

| 시점 | 발언 | 거부 대상 |
|---|---|---|
| 2026-05-17 | *"한쪽에 몰아넣는거 말고 차라리 랜덤"* · *"내가 뭘 페인팅해야 한다는 거"* | **수작업 부담** (painted) |
| 2026-09-05 | *"솔직히 랜덤 별로임"* · *"심 해결하는 방법 안 나옴?"* | **결과 품질** (random) |

두 발언은 같은 목표(품질)의 다른 측면이다. random 은 수작업을 없애는 대신 품질을 포기한
타협이었고, 그 타협이 실패했다. **`spiral_mode` + `spiral_mode_smooth` 는 수작업이 0 이면서
진짜 해결이므로 두 요구를 동시에 만족한다** — 그래서 v4 의 1 순위다.

### v4 결정 트리

```text
회전체 · 원통 모델 감지
  │
  ├─ (1) vase 가능한가?  (판정 체크리스트는 SKILL.md §vase 가능 판정)
  │      YES → spiral_mode = 1 + spiral_mode_smooth = 1
  │            ★ 유일한 실질적 "해결". 사용자 수작업 0.
  │            ⚠️ H2S: 전송 시 timelapse 를 꺼라 (SKILL.md §timelapse 경고)
  │
  ├─ (2) vase 불가 + 숨길 면·방향이 있는가?
  │      YES → seam_position = aligned 또는 back
  │            + Studio seam paint (Enforce/Block) 로 비노출 면에 은닉
  │            + scarf external, 길이는 §2.2 상한 준수, gap 0
  │            사용자 작업: Studio 페인팅 5-10 분 — 사전 고지 필수
  │
  ├─ (3) vase 불가 + 360° 노출 (숨길 곳 없음)
  │      → aligned/back + 짧은 scarf 로 "약한 한 줄" 을 받는다
  │      → 또는 CAD 에서 seam 은폐 feature 를 만든다
  │         (0.2-0.5mm 세로 홈 · 작은 flat · 로고/텍스처 라인)
  │      → 소재 선택도 대책이다: PLA Matte · PLA-CF 는 공식적으로 layer line 은폐 (§4)
  │
  └─ (4) random 은 fallback 전용
         기능품 · 텍스처 허용 부품에만. **surface-first default 로 쓰지 마라.**
```

### 정책 변경 이력

- **v1** 회전체 default `random + entire_loop` (분산)
- **v2** spiral → painted → random. painted 를 default top 에 둠
- **v3** (2026-05-17) 자동화 우선 — painted 를 OPT-IN 으로 내리고 **random 을 default top 으로**
- **v4** (2026-09-05) random 이 품질 요구를 만족하지 못함이 실측·문헌으로 확인 →
  **vase+smooth spiral 을 1 순위로, random 을 fallback 으로.** v3 의 "자동화 우선" 원칙은
  유지되지만, 그 원칙을 만족하는 최선은 random 이 아니라 vase 였다는 것이 v4 의 정정이다.

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
| **Scarf length** (`seam_slope_min_length`) | **scarf 램프의 길이(mm).** `0`이면 scarf 비활성 | Bambu 기본 **10 mm**. 상한은 §2.2 |
| **Scarf start height** | ramp 시작 Z 오프셋. `%`는 layer height 기준. 예: 0.2 mm layer에서 50%는 0.1 mm | `0%/0 mm` (가장 낮게 시작, 부드러운 블렌드) |
| **Scarf slope gap** (`seam_slope_gap`) | **내벽·외벽을 지정량만큼 짧게 잘라낸다.** mm 또는 노즐 지름 대비 `%` | **`0`** (Bambu 기본). 올리지 마라 — §2.1 |
| **Scarf steps** | scarf ramp 분할 단계 | **10** |
| **Scarf around entire wall** | 두 번째 seam 흔적 줄이기 실험값 | **Off** (공식 문서 권장) |

⚠️ Bambu UI에서 `%` 표기는 반드시 `%` 기호를 붙여야 한다는 보고가 있음 (Reddit Bambu guide).

### 2.1 `seam_slope_gap` 과 `seam_gap` 은 다른 키다

이 둘을 섞으면 seam 에 의도치 않은 결손이 쌓인다. 설치된 Bambu Studio `02.06.00.51` 바이너리에서
추출한 툴팁 원문:

| 키 | 라벨 | 툴팁 (원문) | 기본값 |
|---|---|---|---|
| `seam_slope_gap` | Scarf slope gap | *"In order to reduce the visiblity of the seam in closed loop, **the inner wall and outer wall are shortened** by a specified amount."* | **`0`** |
| `seam_gap` | Seam gap | *"In order to reduce the visibility of the seam in a closed loop extrusion, **the loop is interrupted and shortened** by a specified amount. This amount as a percentage of the current extruder diameter."* | **`15%`** |

**둘 다 재료를 덜어내는 키다.** 차이는 대상이다 — `seam_gap` 은 비-scarf seam 의 루프 닫힘부
blob 을 막으려고 루프를 끊고, `seam_slope_gap` 은 벽 자체를 줄인다.

scarf 는 이미 ramp 로 시작·끝을 완만하게 만든다. 거기에 `seam_slope_gap` 을 얹으면 **덜어내기가
중복**되어 언더익스트루전이 된다. Bambu 가 `seam_gap` 만 `15%` 로 두고 `seam_slope_gap` 은 `0` 으로
둔 이유다.

⚠️ **`seam_position: aligned` + `seam_gap 15%`(기본) 조합 주의.** 매 레이어가 같은 각도에서 루프를
잘라내면 그 단축이 Z 축으로 누적돼 표면 라인이 아니라 **세로 홈**이 된다. 회전체에서 aligned 를
쓸 때는 scarf 를 켜거나 `random` 으로 분산한다 (§0 회전체 트리). 2026-08-13 superlube 실측의
"단면상 골 파임" 이 이 기전이다.

출처:
- Orca wiki: https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_seam
- Reddit optimal settings: https://www.reddit.com/r/OrcaSlicer/comments/1b7lthr/what_are_the_optimal_settings_for_scarf_seams/
- Reddit Bambu guide: https://www.reddit.com/r/3Dprinting/comments/1o6i5a1/how_to_improve_your_seams_on_curved_surfaces/

### 2.2 scarf 길이 상한 — 루프 둘레 대비

`seam_slope_min_length` 는 **최소 길이 필터가 아니다.** 이 값은 scarf 램프의 길이이며,
짧은 루프에 큰 값을 주면 램프가 루프의 상당 부분 또는 전체를 차지해 **표면 feature 자체가 된다.**

```text
scarf_length = clamp( min(10mm, 둘레 x 0.10~0.15), 하한 3mm )
```

| 둘레 | 권장 scarf 길이 | 비고 |
|---|---|---|
| `>= 100 mm` | `10 mm` (Bambu 기본) | 여유 |
| `60 ~ 100 mm` | `8 ~ 10 mm` | |
| `30 ~ 60 mm` | `3 ~ 6 mm` | ⌀10~⌀19 원통 구간 |
| `< 30 mm` | scarf **off** 권장 | 램프가 루프를 지배한다 |

**실측 근거**: ⌀10.19 팁(둘레 32.0 mm)에 `8 mm`(둘레의 25%)를 적용해 표면에 눈에 띄는
세로 파임이 나왔다 (2026-09-05 사용자 보고). 위 식으로는 `3.2~4.8 mm` 가 나온다.

⚠️ 공식 문서에 비율 임계는 없다. 위 `0.10~0.15` 는 **추론**이며, Bambu/Prusa/Orca 가 모두
scarf 를 "수평 램프 길이" 로 정의하고 짧은 루프에서의 실패를 인정한다는 사실 + 위 실측에
근거한 시작값이다. coupon 으로 확정하라.

## 3. 형상별 권장 조합 (0.4mm nozzle / 0.2mm layer 기준)

| 형상 | Process 추천 | Filament scarf 추천 |
|------|-------------|---------------------|
| **회전체/원기둥, 컵, 화병** | `seam_position: aligned` 또는 `back`<br>보이는 면 없는 원통은 `aligned`<br>`wall_sequence: inner-outer-inner`<br>outer wall 60-80 mm/s<br>Preview 확인 | `Contour and Hole / All`<br>start `0%`, gap `0`, length `20mm`, steps `10`<br>`Scarf around entire wall: Off`<br>Smart 먼저 On, 줄 끊기면 Off |
| **원통 "선 최대한 안 보이게"** | 가능하면 **Spiral vase가 유일한 진짜 무 seam**<br>일반 벽 구조면 위 원통값 + seam 위치를 후면/내측으로 paint | 검증 조합: `Contour and Hole`, start `0 mm/0%`, **gap `0`** (§2.1), length `20 mm`, `10 steps`, around entire wall Off |
| **구체/돔** | `aligned back` 또는 painted back<br>Smart가 중간 각도에서 끊기면 Off / threshold 낮춤 | `Contour`, start `0-10%`, gap `0`, length `10-20 mm`<br>overhang 큰 하부는 scarf 기대 낮춤 |
| **평면 박스/직육면체** | scarf보다 `painted seam` / `back` / `aligned corner`<br>sharp corner에 숨김 | 보통 `None` 또는 `Contour` 짧게 `5-10 mm`<br>All 비추천 |
| **유기적 곡면 / 피규어** | `aligned back` + seam painting (주름/머리카락/후면)<br>wall order inner-first | `Contour`, start `0-10%`, gap `0`, length `10-20 mm`<br>Smart On 후 Preview 끊기면 Off |
| **얇은 벽 / 미세 디테일** | seam painting 우선, `nearest`는 시간 절약용<br>작은 홀에는 scarf 확장 주의 | `Contour` 또는 `None`<br>length `5-10 mm`, start `5-10%`, gap `0`<br>All/holes는 치수·내벽 흔적 위험 |

검증 출처:
- MakerWorld 원통 테스트: https://makerworld.com/en/models/1886187-scarf-seam-test-cylinder-with-hole
- Reddit 검증: https://www.reddit.com/r/OrcaSlicer/comments/1b7lthr/what_are_the_optimal_settings_for_scarf_seams/

## 4. 소재 x seam 전략 결정표 (2026-09-05 v4)

> 근거: Codex research E (2026-09-05). 공식 문서에 12 소재별 scarf 수치표는 **없다** —
> 아래는 물성·공식 소재 설명·로컬 실측에서 도출한 **시작값**이며 coupon 으로 확정한다.

**전 소재 공통**: `seam_slope_gap = 0` (§2.1) · `seam_slope_steps = 10` ·
`seam_slope_entire_loop = 0` · `seam_slope_inner_walls = 0`. 길이 상한은 §2.2.

| 소재 | 1 순위 전략 | scarf 길이 | 금지 · 주의 |
|---|---|---|---|
| **PLA Basic** | vase → aligned/back + painted | `10-15 mm` | random 을 default 로 쓰지 마라. 기준 소재 |
| **PLA Matte** | 소재 자체가 은폐 → aligned/back | off 또는 `5-8 mm` | 공식 layer-line 은폐 근거 있음. 긴 scarf 이득 작다 |
| **PLA Silk** | **vase 최우선**, 불가 시 painted 필수 | `5-10 mm` | 광택 끊김이 seam 보다 치명적. 속도 차 큰 scarf 금지 |
| **PLA-CF** | 소재 은폐력 활용 + painted/back | off 또는 `5-8 mm` | hardened nozzle 전제. CF 텍스처가 seam 을 가장 잘 숨긴다 |
| **PETG HF** | 건조 후 vase → painted + 짧은 external | `8-12 mm` | `entire_loop` 금지 (Finding 4). 젖은 상태 금지 |
| **PETG Basic** | painted/back 우선, scarf 는 조건부 | `5-10 mm` | blob/stringing 나오면 scarf off |
| **ABS** | painted/back + 안정 챔버 | `8-12 mm` | warping 이 seam 보다 우선 실패 모드 |
| **ASA** | ABS 와 동일 | `8-12 mm` | 외장재는 UV·환기 조건이 우선 |
| **PC** | 불투명 painted, **투명은 vase/설계** | off 또는 `5-10 mm` | 투명은 뒷면 seam 도 비친다. 건조 필수 |
| **PAHT-CF** | painted/back (소재가 이미 은폐) | off 또는 `5-10 mm` | 공식 0.6 노즐 권장 — 0.4 는 hardened + coupon |
| **PA6-CF** | PAHT-CF 와 동일, 건조 게이트 더 강함 | off 또는 `5-10 mm` | 흡습 큼. 미건조 금지 |
| **TPU (95A / for AMS)** | vase 가능하면 vase, 아니면 painted | **기본 off**, 필요 시 `3-5 mm` 실험 | 압출 압력 지연으로 scarf 램프 신뢰 낮다. ironing 금지 |

### seam 가시성 순위 (근거 강도 병기)

`PLA Silk` (강, 최악) > `PETG Basic`·투명 PC (중) > `PLA Basic` (중) > `PETG HF` (강) >
`ABS/ASA/불투명 PC` (중) > `PLA Matte` (강) > `PLA-CF` (강, 최선).

**소재 선택 자체가 seam 대책이다.** PLA Matte 와 PLA-CF 는 Bambu 공식 설명에 layer line
은폐가 명시돼 있다. 반대로 PLA Silk 와 투명 소재는 같은 설정에서 seam 이 가장 잘 보인다.

## 5. 흔한 실패 모드와 회피

| 실패 모드 | 원인 | 회피 |
|----------|------|------|
| **scarf가 아예 안 걸림** | filament profile의 scarf type이 `None`, 또는 1.10 이후 슬롯/프로파일 버그 | Preview에서 적용 여부 확인 필요 |
| **중간부터 세로 줄 재등장** | Smart scarf가 각도/overhang 판단으로 일부 레이어만 적용 | `scarf_angle_threshold` ↓ 또는 Smart Off |
| **blob** | PA 낮음, ooze, 온도 과다 | PA 보정, 외벽 전 wipe + inner-first wall order. **`seam_slope_gap` 을 올려 덮지 마라** — 그건 벽을 깎는 키다 (§2.1) |
| **underextrusion / gap** | PA 과다, `seam_slope_gap` 이 `0` 이 아님, start height 과다, flow ratio 낮음 | `seam_slope_gap` 을 `0` 으로, start height 0-10%, flow 보정 |
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

### Finding 1: 회전체 vent pipe에서 random > aligned (시각적) — 분산 전략 fallback

> v2 surface-first 정책 (§0)에서 이 Finding은 **(3) FALLBACK 단계의 컨텍스트**로 적용된다. 즉, spiral_mode 불가 + painted seam 가능한 숨김 면 없는 완전 노출 원통에서만 random 분산을 쓴다. painted 가능하면 §0의 (2)가 우선.

**상황**: H2S + PETG HF + 0.4mm + 30×30×35mm 쿠폰 (4 wall, hollow tube), `seam_slope_entire_loop: 1` + `seam_slope_type: all` 적용.

**Codex 이론**:
> 외관 우선은 `aligned_back` 또는 `back` + painted seam, 전방향 노출 원통은 `aligned` + entire_loop 테스트가 낫습니다.

**실측 결과**:
- `seam_position: aligned`: 외벽 한쪽에 미세 수직 라인 (광택 변화) **눈에 띔**
- `seam_position: random`: 외벽 둘레에 작은 specks 분산 **덜 거슬림**

**결론**: 전방향 노출 회전체에서 random + entire_loop가 visually 더 깔끔. 단 micro-banding 같은 specks 트레이드오프 수용해야.

**적용 권장 (2026-09-05 v4 로 폐기)**: 이 Finding 은 `aligned` 와 `random` 만 비교한 결과이며,
`spiral_mode` 는 후보에 없었다. v4 는 vase 를 1 순위로 두므로 이 결론을 default 정책으로 쓰지 마라.
`random` 은 fallback 전용이다 (§0). Finding 자체는 *aligned vs random* 비교 기록으로만 유효하다.

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
