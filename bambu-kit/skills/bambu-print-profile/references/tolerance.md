# 공차 (Tolerance) & Fit 매뉴얼

> Last updated: 2026-05-27
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
- `precise_outer_wall`은 Bambu Studio v2.6.0에 없음. PrusaSlicer/Orca 전용. 사용 금지.

## 2. 소재별 수축률 (Bambu 공식 + 실측 보정)

3D 프린팅 후 cooling 단계에서 발생하는 dimensional 수축. PLA가 가장 안정적, ASA/ABS는 가장 큰 수축. fit-critical 부품의 공차 보정값은 수축률에 비례.

| 소재 | 평균 수축률 | 권장 `xy_hole_compensation` | 권장 `xy_contour_compensation` |
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
- **Bolt 통과 hole** (볼트가 자유롭게 통과): hole 3.2-3.4mm (실제 3.0mm 볼트 + clearance). `xy_hole_compensation` 위 값에 +0.05 추가.
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

권장 공차 (PLA Basic, 회전체 surface-first 가능):
- `xy_hole_compensation: "0.075"` — 베어링 외경 22mm hole이 22.10mm로 출력 (PLA 기본 +0.05 + safe margin)
- `xy_contour_compensation: "-0.075"` — 중심 축 외경 8mm이 7.90mm로 출력 (PLA 기본 -0.05 + safe margin)
- `elefant_foot_compensation: "0.15"` — 첫 레이어 베어링 hole 좁아짐 방지

## 8. 미해결 / 검증 필요

- Bambu Studio v2.7.0 beta에 추가 공차 키 있는지 (precise_z_height 등) bambu-kaizen 확인 필요
- 실측 dogfood — 9mm sheath blade fit + 페리스 휠 608ZZ 압입은 출력 후 측정해야 정확한 값 확정
- 소재별 수축률은 색상/lot/습도에 영향 — 실측 calibration 필수
- Slicer scaling factor (`xy_size_compensation` 등 다른 키 존재 여부) 확인

## 9. 출처

- Bambu Studio v02.06.00.51 시스템 base: `fdm_process_common.json` 직접 grep (2026-05-27 검증)
- ISO 메트릭 패스너 표준 (DIN 912 cap screw, ISO 4762)
- ISO 608ZZ bearing spec (22 OD / 8 ID / 7 thickness)
- 3D 프린팅 커뮤니티 표준값 (Hackaday, Printables 가이드)
- 페리스 휠 사용자 dogfood 피드백 (2026-05-27)
