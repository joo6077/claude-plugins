# 공차 (Tolerance) & Fit 매뉴얼

> Last updated: 2026-07-27 (§1.1 보정값 프레임 2× 규칙 · §1.2 무효화 3조건 · §7 수치 정정 · §8 미해결 2건 해소)
> Added in: bambu-kit v0.4.2
> Trigger: SKILL.md Phase 1.7 (Tolerance & Fit Analysis) + Phase 3 공차 보정 키 적용 시 로드

스킬이 fit-critical 부품(베어링/볼트/인서트/슬라이드 fit)을 식별하고 process JSON에 적절한 공차 보정 키를 자동으로 반영할 때 참조한다. 페리스 휠 608ZZ 회귀 + 9mm Knife sheath 가능성 모두 방지.

## 1. Bambu Studio 공차 보정 키 (실측 검증)

> Bambu Studio v2.6.0 / v02.06.00.51 시스템 base `fdm_process_common.json` 직접 grep 검증 (2026-05-27).

| 키 (Bambu JSON) | 단위 | default | 권장값 | 설명 |
|----------------|------|---------|--------|------|
| **`elefant_foot_compensation`** ⚠️ | mm | `"0"` | `0.10-0.20` | 첫 레이어 squish 보정 (Bambu **오타 "elefant"** — "elephant"로 쓰면 silent skip) |
| `xy_hole_compensation` | mm | `"0"` | PLA `+0.05`, PETG `+0.075`, ASA `+0.1` | 홀 직경 보정 (음수 = 더 좁게, 양수 = 더 넓게). **베어링 외경 압입 fit / 인서트 hole** 에 사용 |
| `xy_contour_compensation` | mm | `"0"` | PLA `-0.05`, PETG `-0.075`, ASA `-0.1` | 외경 보정. **베어링 내경에 들어가는 축 / 슬라이드 fit 외경**에 사용 |
| `circle_compensation_manual_offset` | mm | `"0"` | 0 또는 형상별 | 원형 보정 수동 오프셋 (xy_hole/contour와 별개로 원형만 추가 보정) |
| `enable_circle_compensation` | bool | `"0"` | OFF | 원형 자동 보정 enable. ON 시 circle_compensation_manual_offset 적용 |

⚠️ **키 이름 정확성 — silent skip 방지:**

- Bambu Studio의 키는 `elefant_foot_compensation` (오타 의도적 유지). `elephant_foot_compensation`으로 쓰면 무시됨.
- 모든 공차 키는 **mm 단위 문자열** (예: `"0.1"`, `"-0.05"`).
- `elefant_foot_compensation`은 **음수 불가** (`def->min = 0`). 음수를 넣으면 거부된다.
- `precise_outer_wall` — **사용 금지 유지, 단 사유 정정 (2026-07-27).** 이전 판은 "Bambu Studio v2.6.0에 없음 / Orca 전용" 이라고 적었으나 **사실이 아니다**: `v02.06.00.51` 태그의 `PrintConfig.cpp` 에 `coBool` 로 실존한다. 실제 금지 사유는 **`mode = comDevelop`** (개발자 모드 전용 · 기본 `false` · 일반 UI 비노출) 이라 자동 생성 프로파일에서 건드리면 예측 불가라는 점이다.
- `xy_size_compensation` 은 Bambu Studio 에 **없다** (`PrintConfig.cpp` 조회 0건). PrusaSlicer 계열 키이며 Bambu 는 hole/contour 로 분리했다. 쓰면 silent skip.

## 1.1 ⚠️ 보정값 프레임 — 경계 오프셋이지 지름 변화가 아니다 (지름 = 2×)

> **이 절이 공차 SSOT의 최상위 규칙이다.** 평가자 REJECT `PL-01` ("볼트 통과 hole 보정값 불일치 — 계약 `xy_hole` +0.2~0.3 vs 구현 +0.05")의 근본 원인이 바로 이 프레임 혼동이었다. 계약은 **지름** 기준으로, 구현은 **오프셋** 기준으로 같은 키를 서술해서 갈라졌다.

`xy_hole_compensation` / `xy_contour_compensation` 값은 **폴리곤 경계를 밀어내는 오프셋(반경 방향)** 이다. 지름/폭이 그 값만큼 변하는 게 아니다.

- 소스: `PrintObjectSlice.cpp` 가 값을 `_shrink_contour_holes(xy_contour_scaled, xy_hole_scaled, expolygons)` 로 넘겨 **경계 오프셋**으로 적용한다.
- `PrintConfig.cpp` tooltip: "Holes of object will be grown or shrunk in XY plane by the configured value."
- 교차검증: OrcaSlicer wiki `quality_settings_precision` 동일 문구.

**따라서:**

```text
지름 변화 = 2 × 보정값
보정값   = (목표 지름 − 모델 지름) / 2
```

**환산 예 (모델 hole 이 명목 3.0mm 인 M3 통과 홀):**

| 목표 최종 지름 | 필요한 `xy_hole_compensation` | 흔한 오류 |
|---------------|------------------------------|----------|
| 3.10mm | `+0.05` | — |
| **3.20mm** (권장 하한) | **`+0.10`** | `+0.20` 으로 쓰면 3.40mm (헐거움) |
| **3.40mm** (권장 상한) | **`+0.20`** | `+0.40` 으로 쓰면 3.80mm (볼트 유격 과다) |

⚠️ **표를 읽을 때 프레임을 먼저 확인하라.** 본 문서에서 §2 는 **오프셋 값**을, §4 는 **최종 지름**을 다룬다. §4 의 지름을 그대로 보정값 칸에 넣으면 PL-01 이 재발한다.

⚠️ **수축 보정과 설계 clearance 는 다른 목적이다.** §2 의 소재별 값(`+0.05` 등)은 **프린터/소재 치수 오차 보정**이고, 볼트 유격 같은 **설계 clearance** 는 원래 모델 지오메트리의 몫이다. 모델이 이미 3.4mm 로 설계돼 있으면 clearance 를 또 더하지 마라 — 수축 보정분만 적용한다. 모델이 명목 3.0mm 일 때만 clearance 를 보정값으로 대체 투입한다.

## 1.2 ⚠️ 공차 키가 조용히 무효화되는 3 조건 (소스 검증)

공차 키를 JSON 에 정확히 써도 아래 조건에서는 슬라이서가 **값을 버린다**. 생성 후 반드시 확인하라.

| 조건 | 무효화되는 키 | 근거 |
|------|--------------|------|
| **오브젝트가 multi-material / color-paint 됨** (`num_extruders > 1 && is_mm_painted()`) | `xy_hole_compensation`, `xy_contour_compensation` → **강제 `0`** | `PrintObjectSlice.cpp`: `xy_hole_scaled = (num_extruders > 1 && this->is_mm_painted()) ? scaled<float>(0.f) : …` · Studio 가 CRITICAL 경고 "XY Size compensation can not be combined with color-painting" |
| **오브젝트가 fuzzy skin paint 됨** | `xy_hole_compensation`, `xy_contour_compensation` | 동일 파일 `is_fuzzy_skin_painted()` 분기 + CRITICAL 경고 |
| **`raft_layers != 0`** | `elefant_foot_compensation` → **`0`** | `elephant_foot_compensation_scaled = (m_config.raft_layers == 0) ? … : 0.f` — "Only enable Elephant foot compensation if printing directly on the print bed" |

**실무 영향 (이 스킬 한정):**

- 이 스킬은 **멀티컬러 프로파일을 정식 지원**하고 dogfood 케이스도 dual-color 가 많다 (box-opener-knife, stealth-press-1s). **fit-critical 부품이 있는 모델을 color-paint 하면 공차 보정 전부가 무의미해진다.** 이 경우 공차는 슬라이서가 아니라 **모델 지오메트리 수정**으로 해결해야 한다.
- Phase 3 이 `raft_layers` 를 override 대상으로 나열하므로, `raft_layers > 0` 과 `elefant_foot_compensation` 을 동시에 지정하지 마라 (후자가 조용히 죽는다).

**per-object 오버라이드 가능성:** 공차 3키는 `PrintConfig.hpp` 상 `PrintObjectConfig` 소속이라 Studio 에서 오브젝트별 오버라이드가 가능하다. 그러나 **process JSON 은 값을 1개만 표현**한다. 한 모델에 베어링 압입(빡빡)과 볼트 통과(헐거움)가 같이 있으면 **하나의 process JSON 으로 둘을 동시에 만족시킬 수 없다** → 가장 fit-critical 한 카테고리 기준으로 process JSON 을 잡고, 나머지는 notes.md 에 "Studio 에서 오브젝트별 오버라이드 필요" 로 명시하라.

## 2. 소재별 수축률 (Bambu 공식 + 실측 보정)

3D 프린팅 후 cooling 단계에서 발생하는 dimensional 수축. PLA가 가장 안정적, ASA/ABS는 가장 큰 수축. fit-critical 부품의 공차 보정값은 수축률에 비례.

> **프레임: 아래는 전부 오프셋 값이다** (§1.1). 지름에 미치는 효과는 2배다 — `+0.05` 오프셋 = 지름 `+0.10mm`. 이 표의 값은 **소재 수축 보정 전용**이며 설계 clearance 는 포함하지 않는다.

| 소재 | 평균 수축률 | 권장 `xy_hole_compensation` (오프셋) | 권장 `xy_contour_compensation` (오프셋) |
|------|------------|----------------------------|------------------------------|
| **PLA Basic / Matte / Tough+** | 0.2-0.3% | `+0.05` mm | `-0.05` mm |
| **PLA-CF** | 0.15-0.20% (CF가 수축 억제) | `+0.05` mm | `-0.05` mm |
| **PETG Basic / HF** | 0.3-0.5% | `+0.075` mm | `-0.075` mm |
| **PETG-CF** | 0.2-0.3% | `+0.05` mm | `-0.05` mm |
| **ASA / ABS** | 0.5-0.8% | `+0.10` mm | `-0.10` mm |
| **PC** | 0.6-0.7% | `+0.10` mm | `-0.10` mm |
| **PAHT-CF / PA6-CF** | 0.4-0.6% (어닐링 후 추가 수축) | `+0.075` mm | `-0.075` mm |
| **TPU 90A/95A** | 1.0-1.5% (가장 큼, 유연소재) | `+0.15` mm | `-0.10` mm (TPU는 squeezable이라 contour는 less critical) |

⚠️ **권장값은 0.4mm nozzle + Bambu default flow ratio 기준**. 다음 변수가 추가 영향:
- Flow calibration 안 했으면 ±0.05 추가 필요
- Pressure Advance 안 했으면 외벽 거친 부분에서 추가 ±0.05
- AMS HT 건조 안 한 흡습 소재 (PETG/PA/PC)는 +0.05 추가 권장

## 3. Fit-critical 부품 결정 트리

모델에서 fit-critical 부품을 식별하는 단계별 분류. Phase 1.7에서 댓글/이미지/MakerWorld description에서 다음 키워드/번호를 enumerate.

### 3.1 Bearing (베어링 압입)

**식별 패턴:**
- "608ZZ", "608", "609", "688", "625", "MR105", "MR84" 등 ISO 베어링 번호
- "bearing", "베어링", "轴承"
- "ferris wheel", "spinner", "fidget", "회전체", "스피너" 모델

**처리:**
- 베어링 **외경 압입** (베어링이 인쇄물 hole에 들어감): `xy_hole_compensation` **양수** (소재별 표 §2 참조). 너무 빡빡 → 압입 실패, 너무 헐거움 → 베어링 회전 시 wobble
- 베어링 **내경에 축 fit** (인쇄물 축이 베어링 안에 들어감): `xy_contour_compensation` **음수** (소재별 표). 너무 빡빡 → 축 안 들어감, 너무 헐거움 → 베어링 빠짐

### 3.2 Bolt / Screw

**식별 패턴:**
- "M3", "M4", "M5", "M6", "M8" 표준 메트릭 볼트
- "self-tapping", "wood screw", "machine screw"
- Lanyard hole, mounting hole 표시

**처리 (M3 기준, 다른 사이즈는 §4 참조):**

⚠️ 아래 hole 값은 **최종 지름**이다. 보정값으로 옮길 때 §1.1 변환식 `보정값 = (목표지름 − 모델지름) / 2` 를 반드시 통과시켜라. (PL-01 재발 지점)

- **Bolt 통과 hole** (볼트가 자유롭게 통과): 최종 지름 **3.2-3.4mm** (실제 3.0mm 볼트 + clearance).
  - 모델이 이미 3.2-3.4mm 로 설계된 경우 → clearance 추가 금지. §2 수축 보정분만 적용 (PLA 오프셋 `+0.05`).
  - 모델이 명목 **3.0mm** 인 경우 → 오프셋 **`+0.10` ~ `+0.20`** (지름 +0.20~0.40mm). `+0.2~0.3` 을 오프셋으로 쓰면 지름이 3.4-3.6mm 가 되어 과다 유격.
- **Bolt head 매립 hole** (M3 head = 5.5mm): hole 5.6-5.8mm + counterbore 깊이.
- **Self-tapping screw** (PLA에 직접 스레드 만들기): hole 2.7-2.8mm (M3 thread minor diameter 2.39mm + interference). PLA만 가능, PETG/ASA는 crack 위험.

### 3.3 Heat-set Insert (열 인서트)

**식별 패턴:**
- "heat-set insert", "brass insert", "M3 insert", "M4 insert"
- "soldering iron" + "insert" 키워드
- 검은 brass cylinder + thread 이미지

**처리:**
- M3 heat-set insert (가장 흔함): hole **4.0mm** (insert 외경 3.8-4.0mm + 0.0-0.2 squeeze)
- M4 heat-set insert: hole **5.5mm**
- M5 heat-set insert: hole **6.5mm**
- 너무 빡빡 → 인서트 기울어짐, 너무 헐거움 → 인서트 빠짐
- `xy_hole_compensation` 위 권장값 그대로 적용

### 3.4 Slide-fit / Push-lock

**식별 패턴:**
- "push lock", "push button", "slide fit", "snap fit"
- Knife sheath, pen holder, drawer, sliding mechanism
- Linear motion 부품

**처리:**
- 슬라이드 부품 외경: `xy_contour_compensation` **약간 더 큰 음수** (예: PLA -0.10) — 슬라이드 매끄러움 우선
- 슬라이드 receiving hole: 원본 그대로 또는 `xy_hole_compensation +0.05` — 너무 빡빡 안 되게
- Snap-fit (탄성 의존): `xy_contour_compensation` 미세 보정만 (-0.025), 본체는 그대로

## 4. Standard Fastener / Bearing 사이즈 사전

3D 프린팅 커뮤니티에서 자주 쓰는 패스너/베어링의 표준 hole/clearance 사이즈. ISO/DIN 기준.

> **프레임: 아래 "권장 hole" / "권장 contour" 는 전부 최종 지름(mm)이다 — 보정값이 아니다.** 보정값으로 옮길 때 §1.1 변환식을 통과시켜라. 이 표의 지름을 보정값 칸에 직접 넣는 것이 PL-01 의 원인이었다.

| 부품 | 실제 외경/spec | 권장 hole | 권장 contour |
|------|---------------|-----------|------------|
| **M3 bolt pass** (M3 통과) | 3.0mm thread | **3.2-3.4mm** | — |
| **M3 head clearance** (DIN 912 cap screw head) | 5.5mm | **5.6mm** | — |
| **M3 heat-set insert** | 3.8-4.0mm OD | **4.0mm** | — |
| **M4 bolt pass** | 4.0mm thread | **4.3mm** | — |
| **M4 heat-set insert** | 5.3-5.6mm OD | **5.5mm** | — |
| **M5 bolt pass** | 5.0mm thread | **5.3mm** | — |
| **M3 nut (hex)** | 5.5mm flat-to-flat | hexagon hole **5.6mm** flat | — |
| **608ZZ bearing OD** (외경 압입) | 22.0mm | **22.05-22.10mm** (PLA) | — |
| **608ZZ bearing ID** (축이 들어감) | 8.0mm | — | shaft **7.90-7.95mm** (PLA) |
| **688ZZ bearing OD** | 16.0mm | **16.05-16.10mm** | — |
| **688ZZ bearing ID** | 8.0mm | — | shaft **7.90-7.95mm** |
| **625ZZ bearing OD** | 16.0mm | **16.05-16.10mm** | — |
| **MR105ZZ bearing OD** | 10.0mm | **10.05mm** | — |
| **MR84ZZ bearing OD** | 8.0mm | **8.05mm** | — |

⚠️ 위 권장값은 PLA 기준. PETG/ASA는 수축률 표(§2)에 따라 추가 +0.025~0.05.

## 5. Fit Calibration Coupon (peg-and-hole)

베어링/인서트 fit-critical 부품이 1개 이상 식별되면 Phase 5에서 자동 생성. 본 출력 전 ~15-20분에 fit 검증.

### 5.1 Coupon STL 가이드 (Bambu Studio primitive로 즉시 생성)

```text
Coupon 1 — Bearing OD pocket test:
  Add → Primitive → Cylinder
  Outer: 30mm OD × 8mm 두께
  Inner cavity (hole): 22.10mm (608ZZ OD + 0.10) — Bambu Studio Modifier → Subtract
  → 출력 후 608ZZ 베어링이 정확히 fit 되는지 확인

Coupon 2 — Shaft for bearing ID:
  Add → Primitive → Cylinder
  7.90mm OD × 20mm 높이
  → 출력 후 608ZZ 베어링이 슬라이드 fit 되는지 확인 (헐겁지도 빡빡하지도 않게)

Coupon 3 — Heat-set insert test:
  Add → Primitive → Box 20×20×8mm
  Subtract Cylinder 4.0mm × 6mm 깊이 (M3 insert용)
  → 출력 후 4.0mm hole에 M3 insert를 인두로 압입해서 정렬/유지력 확인

Coupon 4 — Bolt pass + nut catch (selective):
  Add → Primitive → Box 30×15×6mm
  Through hole: Cylinder 3.4mm × 6mm (M3 bolt pass)
  Hex pocket: Polygon 6-sided 5.6mm flat × 3mm (M3 nut catch)
  → M3 bolt + nut 통과/잡힘 확인
```

### 5.2 STL 직접 생성 안 하는 이유

Coupon용 STL은 OpenSCAD/CadQuery 같은 외부 도구 필요. Bambu Studio primitive (Cylinder + Box + Modifier Subtract) 조합으로 5분 안에 생성 가능. 사용자에게 가이드만 제공.

추후 v0.5+: 표준 coupon STL 사전 출력본 첨부 검토 (BACKLOG).

### 5.3 통과 / 실패 분기

**통과** (베어링이 손가락 압력으로 정확히 fit, 흔들림 없음):
- 본 출력 진행

**실패 — 너무 빡빡** (베어링 안 들어감, 압입 시 인쇄물 깨질 위험):
- `xy_hole_compensation` 0.05 증가 → 재출력
- 또는 hole 보정값을 모델 내부 cylinder도 같이 보정 (Bambu Studio variable layer height)

**실패 — 너무 헐거움** (베어링 흔들림 또는 빠짐):
- `xy_hole_compensation` 0.05 감소 → 재출력
- 또는 베어링에 thread locker 또는 super glue 한 방울 (영구 고정)

## 6. 9mm Craft Knife Elite fit 분석 (v0.4.2 dogfood)

9mm 커터칼 sheath:
- **slide-fit (push-lock 메커니즘)** — blade가 sheath 내부에서 슬라이드 + lock
- blade body 폭: 표준 9mm 커터칼은 약 8.9-9.0mm
- sheath 내부 slot: **9.0mm + clearance 0.1-0.2mm**
- 디자이너 의도: blade가 의도적으로 슬라이드 가능해야 함 (lock 시만 잡힘)

권장 공차 (PLA Basic):
- `elefant_foot_compensation: "0.15"` (첫 레이어 squish — slot 입구 좁아짐 방지)
- `xy_hole_compensation: "0.05"` (PLA 기본) — slot이 너무 좁게 출력 안 되도록
- `xy_contour_compensation: "-0.05"` — 외경 정확도 (손에 쥐기)

## 7. 페리스 휠 (MakerWorld 1186414, 608ZZ variant) fit 분석

페리스 휠 회전 부품 — 사용자 dogfood 회귀 (2026-05-27 보고: "베어링이랑 중심부랑 안맞았음").

식별 부품:
- **608ZZ 베어링 × 2** (중심 축 회전용)
- 회전체 (휠 본체) 회전축 hole — 베어링 외경(22mm) 압입
- 중심 축 — 베어링 내경(8mm) shaft fit

권장 공차 (PLA Basic, 회전체 surface-first 가능) — **§1.1 2× 규칙 적용 후 정정값**:

| 키 | 보정값 (오프셋) | 모델 지름 → 최종 지름 | 목표 (§4) |
|----|---------------|---------------------|----------|
| `xy_hole_compensation` | `"0.05"` | 22.00 → **22.10mm** | 22.05-22.10 ✅ |
| `xy_contour_compensation` | `"-0.05"` | 8.00 → **7.90mm** | 7.90-7.95 ✅ |
| `elefant_foot_compensation` | `"0.15"` | 첫 레이어 hole 좁아짐 방지 | — |

⚠️ **정정 이력 (2026-07-27 카이젠):** 이전 판은 `xy_hole "0.075"` 를 "22.10mm 로 출력" 이라고 적었으나, 2× 규칙상 `+0.075` 오프셋은 **22.15mm** 다 (목표 초과). `xy_contour "-0.075"` 도 7.90mm 가 아니라 **7.85mm** 였다. 즉 **두 조인트가 각각 0.05mm 씩 헐거워진다** — 베어링 외경↔포켓 유격이 목표보다 0.05mm 크고(22.15 vs 22.05-22.10), 축↔베어링 내경 유격도 0.05mm 크다(7.85 vs 7.90-7.95). 조립체 전체로는 두 유격이 겹쳐 반경 방향 흔들림으로 나타난다 — 사용자 실측 보고 "베어링이랑 중심부랑 안맞았음"(2026-05-27)과 방향이 일치한다. 실제 생성된 프로파일(`ferris-wheel-608zz/.../coupon1-608zz-OD-pocket.3mf` 임베드 config)에 `xy_hole_compensation: "0.075"` 가 박혀 있는 것으로 확인됨.

⚠️ **이 모델을 dual-color 로 paint 하면 위 공차 전부가 무효다** (§1.2). 페리스 휠은 멀티컬러 후보이므로 color-paint 여부를 반드시 사용자에게 확인하라.

## 8. 미해결 / 검증 필요

**해소됨 (2026-07-27 카이젠):**

- ~~Bambu Studio v2.7.0 beta에 추가 공차 키 있는지 (precise_z_height 등)~~ → **해소.** `precise_z_height` 는 v2.6.0.51 에 **이미 존재**하며 신규 키가 아니다. `coBool` / 기본 `0` / "experimental parameter" 로, 마지막 몇 레이어의 layer height 를 미세조정해 **Z 높이**를 맞추는 기능이다 — **XY 공차와 무관하므로 fit 보정에 쓰지 마라.**
- ~~Slicer scaling factor (`xy_size_compensation` 등)~~ → **해소.** Bambu 에 `xy_size_compensation` 은 없다 (§1 참조). `hole_to_polyhole` 도 없다 (조회 0건).

**미해결 (여전히 실측 필요):**

- 실측 dogfood — 9mm sheath blade fit + 페리스 휠 608ZZ 압입은 출력 후 측정해야 정확한 값 확정. **§7 정정값(`+0.05`/`-0.05`)으로 재출력 후 검증 필요** — 기존 `0.075` 출력본은 2× 오류가 반영된 값이다.
- 소재별 수축률은 색상/lot/습도에 영향 — 실측 calibration 필수
- §1.2 무효화 3조건의 UI 경고가 Studio 화면 어디에 뜨는지(슬라이스 시 popup vs sidebar) 실기 확인 — 사용자에게 안내할 문구 확정용

## 9. 출처

- Bambu Studio v02.06.00.51 시스템 base: `fdm_process_common.json` 직접 grep (2026-05-27 검증)
- **2026-07-27 카이젠 추가 검증 (소스 직접 조회):**
  - `PrintConfig.cpp` — 키 정의/tooltip/기본값/`min`. master 및 `v02.06.00.51` 태그 양쪽:
    <https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp>
  - `PrintConfig.hpp` — 공차 3키의 `PrintObjectConfig` 소속(per-object 오버라이드 가능) 확인:
    <https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.hpp>
  - `PrintObjectSlice.cpp` — `_shrink_contour_holes()` 경계 오프셋 적용(§1.1 2× 규칙) + MM color-paint / fuzzy-skin / `raft_layers` 무효화 분기(§1.2):
    <https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintObjectSlice.cpp>
  - OrcaSlicer wiki (교차검증): <https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_precision>
  - 실측 3MF 임베드 config: `ferris-wheel-608zz/bundle/coupon-stl/coupon1-608zz-OD-pocket.3mf` → `Metadata/project_settings.config`
- ISO 메트릭 패스너 표준 (DIN 912 cap screw, ISO 4762)
- ISO 608ZZ bearing spec (22 OD / 8 ID / 7 thickness)
- 3D 프린팅 커뮤니티 표준값 (Hackaday, Printables 가이드)
- 페리스 휠 사용자 dogfood 피드백 (2026-05-27)
