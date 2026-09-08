# Bambu Studio 캘리브레이션 레퍼런스

> **용도**: Claude Code 글로벌 스킬의 소스 문서. "이 증상엔 어떤 캘리브레이션을 어떤 순서로
> 어떻게 실행하는가" 를 결정 트리로 답하기 위한 사실 모음이다.
> **작성**: 2026-09-06
> **검증 기준**: 설치본 Bambu Studio `02.08.02.61` / 프로파일 번들 `02.08.00.06` · 프린터 H2S 0.4 노즐

## 0. 근거 등급 — 이 문서를 읽는 규칙

문장마다 출처 등급이 다르다. 스킬로 옮길 때 등급을 지우지 마라.

| 등급 | 뜻 | 표기 |
|---|---|---|
| **[설치본]** | 설치된 바이너리·시스템 프로파일에서 직접 추출. 이 환경에서 참 | 인용문은 원문 그대로 |
| **[공식]** | Bambu 공식 wiki·매뉴얼 | URL 명시 |
| **[Orca]** | OrcaSlicer 문서. 같은 계보지만 **Bambu 와 값·이름이 다를 수 있다** | 반드시 라벨 유지 |
| **[추론]** | 구현·정황에서 끌어낸 것 | 단정하지 마라 |
| **[미검증]** | 확인 못 함 | 스킬이 이걸 사실로 말하면 안 된다 |

⚠️ **UI 라벨을 기억으로 쓰지 마라.** 버전마다 바뀐다. 스킬은 실행 시점에 설치본에서
확인하거나, 사용자 화면을 받아서 대조해야 한다. 이 문서의 라벨도 `02.08.02.61` 기준이다.

## 1. 캘리브레이션 6 종 카탈로그

`02.08.02.61` 바이너리에 실존하는 내부 모드 이름 **[설치본]**:

| # | UI 이름 | 내부 mode | 보정 대상 | 실행 위치 |
|---|---|---|---|---|
| 1 | **Flow Dynamics** | `auto_pa_line_calib_mode` · `pa_line_calib_mode` · `pa_pattern_calib_mode` | 압출 압력 지연 (PA / K 계수) | Calibration 탭 (프린터 연결) |
| 2 | **Flow Rate** | `flow_rate_coarse_calib_mode` · `flow_rate_fine_calib_mode` | 기대 대비 실제 압출량 비 (`filament_flow_ratio`) | Calibration 탭 (프린터 연결) |
| 3 | **Max Volumetric Speed** | `vol_speed_tower_calib_mode` | 안정 압출 가능한 최대 체적속도 `mm³/s` | Calibration 탭 |
| 4 | **Temperature** | `temp_tower_calib_mode` | 노즐 온도 | 타워 출력 후 육안 |
| 5 | **Retraction test** | `retration_tower_calib_mode` (Bambu 코드의 오타 그대로) | 리트랙션 길이/속도 | 타워 출력 후 육안 |
| 6 | **VFA** | `vfa_tower_calib_mode` | 특정 외벽 속도대의 미세 줄무늬 | 타워 출력 후 육안 |

**[설치본]** 구현 클래스로 확인된 마법사 단계: `Preset → Calibration1 → Calibration2 → Record Factor`

## 2. 실행 순서

### 공식 근거가 있는 것 — Flow Dynamics → Flow Rate

Studio 의 `When to use Flow Rate Calibration` 섹션이 이렇게 시작한다 **[설치본, 원문]**:

> *"**After using Flow Dynamics Calibration**, there might still be some extrusion issues, such as: …"*

즉 **Flow Rate 는 Flow Dynamics 이후**를 전제한다. 이 순서를 뒤집으면 안 된다.

### 그 밖의 순서

**[공식]** 6 종 전체의 권장 순서는 Bambu 공식 문서에 **없다**.
**[Orca]** Orca 가이드는 `Temperature → Volumetric Speed → Pressure Advance → Flow Ratio → Retraction`
성격의 순서를 제시한다 — **Orca 기준이며 Bambu 공식이 아니다.**

**[추론]** 다만 의존 방향은 명확하다. Studio 가 *"The nozzle temp and max volumetric speed will affect
the calibration results"* 라고 경고하므로 **[설치본]**, 온도와 MVS 를 바꾸면 PA 를 다시 봐야 한다.
따라서 실무 순서는:

```text
온도 확정 → MVS 확정 → Flow Dynamics(PA) → Flow Rate → (필요 시) Retraction / VFA
```

## 3. 증상 → 캘리브레이션 결정 트리

Studio 자신이 갖고 있는 매핑이 1 차 근거다 **[설치본, 원문]**:

> 1. **Over-Extrusion**: Excess material on your printed object, forming blobs or zits, or the layers seem thicker than expected and not uniform.
> 2. **Under-Extrusion**: Very thin layers, weak infill strength, **or gaps in the top layer of the model**, even when printing slowly.
> 3. **Poor Surface Quality**: The surface of your prints seems rough or uneven.
> 4. **Weak Structural Integrity**: Prints break easily or don't seem as sturdy as they should be.

→ 위 4 종은 전부 **Flow Rate** 의 적응증이다 (단, Flow Dynamics 를 먼저 한 뒤).

### 결정 트리

```text
증상 파악
  │
  ├─ 프린터를 옮겼다 / 분해했다 / 핫엔드·노즐을 건드렸다 / 첫 층이 불량하다
  │     → 필라멘트 캘리브 이전에 프린터 캘리브(ABL·노즐 오프셋) 먼저          [공식]
  │
  ├─ Bambu 정품 필라멘트 + 증상 없음
  │     → 아무것도 하지 마라. 프리셋이 이미 pre-calibrated 다                  [설치본]
  │
  ├─ 코너에서 부풀거나 패임 · 가감속 지점에서 선폭이 흔들림
  │     → Flow Dynamics (PA)
  │
  ├─ 인접 압출선이 안 붙어 틈 · 느리게 뽑아도 under-extrusion · 인필이 약함
  │     → ① 노즐 지름 설정 확인 ② 막힘 확인 ③ 건조 확인
  │       그다음 Flow Rate                                                     [공식]
  │
  ├─ 빠를 때만 under-extrusion, 속도 낮추면 사라짐
  │     → Max Volumetric Speed
  │
  ├─ 스트링잉 / 우징
  │     → 건조 확인 → Temperature → Retraction test
  │
  └─ 외벽에 특정 속도대에서만 주기적 미세 줄무늬
        → 기본 motion/vibration 확인 → VFA
```

⚠️ **틈의 위치를 먼저 보라.** 전면적이면 Flow Rate, **코너·외벽↔인필 접점처럼 가감속 지점에
몰려 있으면 Flow Dynamics(PA)** 가 후보다 **[공식 매뉴얼 기반]**. 이 구분을 건너뛰면 엉뚱한
캘리브레이션을 돌린다.

## 4. Flow Rate — 절차 (가장 자주 쓴다)

### 4.1 진입

```text
Calibration 탭 → 좌측 Flow Rate
```

### 4.2 Preset 화면에서 정하는 것 **[설치본 UI]**

| 항목 | 선택 | 근거 |
|---|---|---|
| **Calibration Type** | `Complete Calibration` = coarse + fine (Calibration1 + Calibration2)<br>`Fine Calibration based on flow ratio` = fine 단독 | 처음이면 Complete **[공식]** |
| **Nozzle Diameter** | 실제 노즐과 일치 | |
| **Nozzle Flow** | `Standard` / `High Flow` — 프로파일의 MVS 열과 같아야 함 | |
| **Plate Type** | **실제 장착된 플레이트와 반드시 일치** | 불일치 → 접착 불량 → 결과 무효 **[설치본]** |
| **Filament For Calibration** | 실제로 그 출력에 쓴 스풀 | |

### 4.3 판정

각 단계에서 Studio 가 묻는 문구 **[설치본, 원문]**:

> *"Please choose a block with smoothest top surface"*
> *"Fill in the value above the block with smoothest top surface"*

**[Codex/미검증]** coarse 는 프리셋 flow 기준 `80–120%` 를 `5%` 간격, fine 은 입력값 기준
`91–100%` 를 `1%` 간격으로 훑는다고 조사됐으나 **설치본 문자열로는 확인되지 않았다.**
스킬은 이 숫자를 단정하지 말고 화면에 표시된 값을 읽으라고 안내해야 한다.

저장 성공 시 **[설치본, 원문]**: *"Flow rate calibration result has been saved to preset"*

### 4.4 결과가 무효가 되는 조건 **[설치본, 원문]**

- *"insufficient adhesion on the build plate. Improving adhesion can be achieved by washing the build plate or applying glue"*
- *"The current nozzle, heatbed, or **chamber temperature** differs from the calibration conditions"*
- *"The calibration results have about **10 percent jitter** in our test"* — 1 회 결과를 절대값으로 믿지 마라

### 4.5 소재 제약 — 자동 방식 한정 **[설치본, 원문]**

> *"Auto Flow Rate Calibration utilizes Bambu Lab's Micro-Lidar technology… the efficacy and accuracy of this
> method may be compromised with specific types of materials. Particularly, filaments that are **transparent or
> semi-transparent, sparkling-particled, or have a high-reflective finish** may not be suitable"*

→ 투명·반투명·펄·고광택이면 **자동 금지, 수동(Complete/Fine)으로 간다.**
**[공식]** 수동 방식에는 투명 소재 금지 근거가 없다.

## 5. Flow Dynamics — 자동이 막히는 조건 **[설치본, 원문]**

아래는 **자동(auto) Flow Dynamics 가 아예 안 되는** 경우다. 수동으로 가야 한다.

> - *"TPU 90A/TPU 85A is too soft and does not support automatic Flow Dynamics calibration."*
> - *"The nozzle diameter of %s extruder is **0.2mm** which does not support automatic Flow Dynamics calibration."*
> - *"The type of %s extruder is **bowden** which does not support automatic Flow Dynamics calibration."*
> - *"(Aux) does not support automatic flow calibration."*

TPU 관련 상세 **[설치본, 원문]**:
> *"TPU 90A/TPU 85A are too soft. It is recommended to perform **manual** flow calibration on the 'Calibration' page.
> If 'Dynamic Flow Calibration' is set to auto/on, the system will use the **previous calibration value and skip**
> the flow calibration process."*

→ auto 로 두면 **조용히 옛 값을 쓰고 건너뛴다.** 실패로 보이지 않는다는 점이 중요하다.

## 6. Max Volumetric Speed — 언제 **[설치본, 원문]**

> *"Max Volumetric Speed calibration is recommended when you print with:*
> *1. If you introduce a new filament of different brands/models or the filament is **damp**;*
> *2. if the nozzle is **worn out or replaced** with a new one;*
> *3. If the max volumetric speed or print temperature is **changed in the filament setting**."*

그리고 **[설치본, 원문]**: *"The nozzle temp and max volumetric speed will affect the calibration results.
Please fill in the **same values as the actual printing**."*

## 7. H2S 특이사항

**[공식]** H2S 는 350 °C 노즐 · 65 °C 능동 가열 챔버 · 서보 익스트루더 + 노즐 압력 센싱을 갖는다.
그래서 Flow Dynamics 자동의 센서 기반이 X1 의 Micro-Lidar 와 **다르다**.
출처: <https://us.store.bambulab.com/en/products/h2s>

**[미검증]** H2S 에서 **Auto Flow Rate** 가 지원되는지는 공식 근거를 찾지 못했다.

**[설치본]** 가열 챔버가 있으므로 "chamber temperature differs from the calibration conditions" 조항이
실질적으로 작동한다 — ABS/ASA 처럼 챔버를 쓰는 소재는 **문을 닫고 챔버가 올라온 상태에서** 캘리브레이션해야
결과가 실제 출력에 옮겨진다. 예: `Bambu ABS @BBL H2S` 는 `chamber_temperatures = 60` **[설치본]**.

## 8. Flow Rate 결과와 layer height

**[미검증]** "0.08mm 에서 보정한 flow ratio 를 0.12mm 에 그대로 써도 되는가" 에 대한 공식 문장은 없다.

**[Codex/추론]** Bambu 구현은 Flow Rate 테스트의 layer height 를 노즐 지름의 절반(0.4 → 0.2mm)으로
고정하고, 결과를 **filament 레벨** `flow_ratio` 로 저장해 모든 압출에 비례 적용한다. 따라서 특정
process preset 전용 값이 아니라 소재 단위 값으로 설계된 것으로 보인다.
→ **실무 결론**: 값 자체는 layer height 무관하게 적용되지만, **극단적 layer height(0.08 등)에서는
목표 두께로 검증 출력을 따로 해야 한다.** 스킬은 이걸 "보정하면 끝" 으로 말하면 안 된다.

## 9. 스킬 작성 시 반영할 것

1. **UI 라벨을 하드코딩하지 마라.** 실행 시점에 설치본(`/Applications/BambuStudio.app`) 문자열을
   조회하거나 사용자 스크린샷과 대조한다. 이 문서의 라벨도 한 버전 기준이다.
2. **증상의 *위치*를 먼저 묻는다.** 전면적 틈 ↔ 가감속 지점 집중은 다른 캘리브레이션으로 갈린다.
3. **캘리브레이션 전에 배제할 것을 먼저 배제한다** — 노즐 지름 설정 · 막힘 · 건조 · 플레이트 접착.
   이걸 안 하고 캘리브레이션부터 시키면 무효 결과를 얻는다.
4. **정품 필라멘트면 "하지 마라" 가 정답일 수 있다** — Studio 가 pre-calibrated 라고 명시한다.
   스킬이 무조건 캘리브레이션을 권하면 안 된다.
5. **10 % jitter 를 고지한다.** 1 회 결과를 절대값으로 다루지 않는다.
6. **자동이 조용히 건너뛰는 경로를 경고한다** (TPU + auto → 옛 값 사용 후 skip).
7. **챔버 온도 일치**를 ABS/ASA/PC 계열에서 필수 체크로 넣는다.

## 10. 확인 못 한 것 (스킬이 사실로 말하면 안 되는 것)

- 6 종 전체의 공식 권장 순서 — **없다**. Flow Dynamics → Flow Rate 만 근거 있음
- Flow Rate coarse/fine 의 정확한 스캔 범위와 간격
- Temperature / Retraction / VFA 의 **Bambu 공식** 판정 기준 (Orca 기준만 있음)
- VFA 의 Bambu 공식 wiki 페이지 존재 여부
- H2S 에서 Auto Flow Rate 지원 여부

## 출처

- 설치본 `02.08.02.61` 바이너리 문자열 · 시스템 프로파일 직접 조회 (2026-09-06)
- Bambu wiki: [PA](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa) ·
  [Flow Rate](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate) ·
  [Volumetric](https://wiki.bambulab.com/en/software/bambu-studio/calibration_volumetric) ·
  [Temperature](https://wiki.bambulab.com/en/software/bambu-studio/calibration_temperature) ·
  [Retraction](https://wiki.bambulab.com/en/software/bambu-studio/calibration_retraction)
- BambuStudio `CalibUtils.cpp` · `PrintConfig.cpp` (GitHub master)
- H2S 제품 페이지 <https://us.store.bambulab.com/en/products/h2s>
- Codex research run (2026-09-06, read-only, 15 검색 상한)
