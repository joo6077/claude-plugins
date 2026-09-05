# Bambu Lab 필라멘트 카탈로그 (H2S + AMS HT + AMS 2 Pro)

> Last updated: 2026-05-15
> Source: Codex research run `aeb457c7603a420db` (score 23/25)
> Bambu Studio reference version: **런타임에 조회한다 — 이 줄에 버전을 하드코딩하지 마라.**
>   앱 `/Applications/BambuStudio.app/Contents/Info.plist` · 프로파일 번들
>   `~/Library/Application Support/BambuStudio/system/BBL.json` 의 `version`.
>   두 값은 **따로 갱신된다** (프로파일은 앱과 무관하게 네트워크로 갱신). 조회 절차는 `SKILL.md` §환경 검증.
>   최초 작성 시점 기준: 앱 `02.06.00.51` / 번들 `02.06.00.05`. 2026-09-05 확인: 앱 `02.08.02.61` / 번들 `02.08.00.06`, H2S 0.4 앵커값 10/10 동일.

스킬이 모델 형상/용도에 맞는 필라멘트를 추천한 뒤 `inherits`로 가리키는 base 프로파일명을 조회하기 위한 카탈로그.

⚠️ **규약**:
- `Studio값` = H2S 기본 0.4 계열 프로파일의 `nozzle / bed / MVS (max volumetric speed mm³/s)`
- `mm/s 속도`는 Studio JSON에 직접 키로 들어가지 않음 — `filament_max_volumetric_speed`가 실제 키. 표의 MVS 참고.
- `SS` = stainless steel nozzle, `HS` = hardened steel nozzle
- `H2S 챔버` = 65°C까지 active chamber 가능

## 1. 전체 카탈로그

| 제품명 | Studio base profile | nozzle/bed/MVS (H2S) | 건조 / AMS HT | AMS 2 Pro 직접 로드 | H2S 노즐/챔버 | 용도/한줄 평 |
|---|---|---:|---|---|---|---|
| **PLA Basic** | `Bambu PLA Basic @base` | 220 / 55 / 25-40 | 55°C 8h, AMS HT 가능 | 가능 | SS/HS, 비가열 | cosmetic/prototype: 쉬운 출력, 낮은 내열 |
| **PLA Matte** | `Bambu PLA Matte @base` | 220 / 55 / 25-40 | 55°C 8h | 가능 | SS/HS, 비가열 | cosmetic: 무광, 레이어 은폐 좋음, PLA급 내열 |
| **PLA Silk** | `Bambu PLA Silk @base` | 230 / 55 / 12 | 55°C 8h | 가능 | SS/HS, 비가열 | cosmetic: 광택, 강도는 Basic보다 보수적 |
| **PLA Silk+** | `Bambu PLA Silk+ @base` | 230 / 55 / 12 | 55°C 8h | 가능 | SS/HS, 비가열 | cosmetic: Silk보다 개선형 광택/인성 |
| **PLA Aero** | `Bambu PLA Aero @base` | 220 / 55 / 6 | 55°C 8h | 가능 | SS/HS, 비가열 | lightweight: 발포 경량 부품, 강도 낮음 |
| **PLA Lite** | `Bambu PLA Lite @base` | 220 / 55 / 20-30 | 55°C 8h | 가능 | SS/HS, 비가열 | prototype: 저가/경량 일반 PLA |
| **PLA Tough** | `Bambu PLA Tough @base` | 220 / 55 / 21 | 55°C 8h | 가능 | SS/HS, 비가열 | functional-light: Basic보다 충격에 유리 |
| **PLA Tough+** | `Bambu PLA Tough+ @base` | 245 / 55 / 21 | 55°C 8h | 가능 | SS/HS, 비가열 | functional-light: PLA계 고인성 |
| **PLA-CF** | `Bambu PLA-CF @base` | 230 / 55 / 15 | 55°C 8h 권장 | 가능 | hardened 0.4/0.6 권장 | cosmetic/functional: 무광·강성, 마모성 |
| **PLA Glow** | `Bambu PLA Glow @base` | 220 / 55 / 18 | 55°C 8h | 가능, 마모 주의 | hardened 권장 | cosmetic: 야광, 노즐 마모/막힘 주의 |
| **PLA Galaxy** | `Bambu PLA Galaxy @base` | 220 / 55 / 21 | 55°C 8h | 가능 | hardened 0.4+ 권장 | cosmetic: 반짝임/광택, 0.2 비권장 |
| **PLA Sparkle** | `Bambu PLA Sparkle @base` | 220 / 55 / 12 | 55°C 8h | 가능 | hardened 권장 | cosmetic: 펄/스파클, 속도 낮춤 |
| **PLA Marble** | `Bambu PLA Marble @base` | 220 / 55 / 12 | 55°C 8h | 가능 | 0.4+ 권장 | cosmetic: 석재 질감, 디테일보다 외관 |
| **PLA Metal** | `Bambu PLA Metal @base` | 220 / 55 / 21 | 55°C 8h | 가능 | SS/HS, 비가열 | cosmetic: 금속 질감 (실 금속 충전 아님) |
| **PLA Wood** | `Bambu PLA Wood @base` | 220 / 55 / 18 | 55°C 8h | 가능 | 0.4+ 권장 | cosmetic: 목재 질감, 막힘 주의 |
| **PLA Translucent** | `Bambu PLA Translucent @base` | 220 / 55-60 / 12 | 55°C 8h | 가능 | SS/HS, 비가열 | cosmetic: 반투명, 느린 출력 유리 |
| **PLA Dynamic** | `Bambu PLA Dynamic @base` | 220 / 55 / 21 | 55°C 8h | 가능 | SS/HS, 비가열 | cosmetic: 색/효과 계열 |
| **PETG Basic** | `Bambu PETG Basic @base` | 245 / 70 / 18-21 | 65°C 8h 권장, AMS HT 가능 | 가능 | SS/HS, 챔버 낮게 | functional: PLA보다 내열/내수성 우수 |
| **PETG HF** | `Bambu PETG HF @base` | 245 / 70 / 25-40 | 65°C 8h 필수급, AMS HT 가능 | 가능 | SS/HS, 낮은 챔버 | functional: 빠른 PETG, 실사용 부품 우선 |
| **PETG Translucent** | `Bambu PETG Translucent @base` | 245-250 / 70 / 6 | 65°C 8h | 가능 | SS/HS, 낮은 챔버 | cosmetic/functional: 투명감, 속도 낮게 |
| **PETG-CF** | `Bambu PETG-CF @base` | 255 / 70 / 11.5 | 65°C 8h | 가능 | hardened 0.4/0.6 | functional: 강성/무광, 내열은 PETG급 |
| **ABS** | `Bambu ABS @base` | 260-270 / 90 / 20-35 | 80°C 8h 권장 | 가능 | SS 가능, 챔버 45-60°C | engineering: 내열/후가공, 냄새·수축 |
| **ABS-GF** | `Bambu ABS-GF @base` | 260-270 / 90 / 12 | 80°C 8h | 가능 | hardened 0.6 권장, 45-60°C | engineering: ABS보다 강성/치수안정 |
| **ASA** | `Bambu ASA @base` | 270 / 100 / 20-35 | 80°C 8h 권장 | 가능 | SS 가능, 45-60°C | outdoor: UV/내후성 우수 |
| **ASA-CF** | `Bambu ASA-CF @base` | 275 / 100 / 18 | 80°C 8h | 가능 | hardened 0.6 권장, 45-60°C | outdoor engineering: ASA+강성/무광 |
| **ASA-Aero** | `Bambu ASA-Aero @base` | 270 / 90 / 6 | 80°C 8h | 가능 | hardened/0.6 권장, 45-60°C | lightweight outdoor: 경량+내후성 |
| **PC** | `Bambu PC @base` | 270-280 / 110 / 20-35 | 80°C 8h 필수급 | 가능 | SS 가능, 45-60°C | engineering: 고내열/고강도, 수축 관리 |
| **PC FR** | `Bambu PC FR @base` | 270-280 / 110 / 18 | 80°C 8h | 가능 | SS/HS, 45-60°C | engineering: 난연 PC, 전장/하우징 |
| **PA-CF** ⚠️ | `Bambu PA-CF @base` | 290 / 100 / 8 | 80°C 8-12h, AMS HT 권장 | 자료상 구형/단종 주의 | hardened 0.6 권장, 45-60°C | engineering: **단종**, PAHT-CF 사용 권장 |
| **PAHT-CF** | `Bambu PAHT-CF @base` | 290 / 100 / 8 | 80°C 8-12h, AMS HT 권장 | 가능 | hardened 0.6 권장, 45-60°C | engineering: 저흡습 PA12-CF, 고내열 |
| **PA6-CF** | `Bambu PA6-CF @base` | 275 / 100 / 8 | 80-100°C 필수, AMS HT 보관/출력 유리 | 공식 비교상 제한 가능성 | hardened 0.6 권장, 45-60°C | engineering: 강도/인성 ↑, 흡습 ↑ |
| **PA6-GF** | `Bambu PA6-GF @base` | 265 / 100 / 10.5 | 80°C+ 필수 | 가능 | hardened 0.6 권장, 45-60°C | engineering: 강성/치수안정, 흡습 |
| **PET-CF** | `Bambu PET-CF @base` | 270 / 100 / 8 | 80°C+ 필수, AMS HT 보관만 | **외부 스풀 우선** | hardened 0.6 권장, 45-60°C | engineering: 고강성·저흡습, AMS 제약 |
| **PPA-CF** | `Bambu PPA-CF @base` | 290 / 100 / 8 | 100°C 외부 오븐 권장, AMS HT는 보관 | **외부 스풀 우선** | hardened 0.6 권장, 45-60°C | engineering: PA계 고성능/고내열 |
| **PPS-CF** | `Bambu PPS-CF @base` | 320 / 110 / 6 | 100°C 외부 오븐 필요, AMS HT만으론 부족 | **외부 스풀 우선** | hardened 0.6 권장, 50-65°C | engineering: 최고 내열/내화학 |
| **TPU 85A** | `Bambu TPU 85A @base` | 225 / 35 / 3 | 70°C 8h | 외부 스풀 우선 | SS/HS, 비가열 | flexible: 매우 유연, 느림 |
| **TPU 90A** | `Bambu TPU 90A @base` | 225 / 35 / 5.6 | 70°C 8h | 외부 스풀 우선 | SS/HS, 비가열 | flexible: 유연 |
| **TPU 95A** | `Bambu TPU 95A @base` | 230 / 35 / 3.6 | 70°C 8h | 외부 스풀 우선 | SS/HS, 비가열 | flexible: 일반 TPU, AMS 제약 |
| **TPU 95A HF** | `Bambu TPU 95A HF @base` | 230 / 35 / 12 | 70°C 8h | **불가, 외부 스풀** | SS/HS, 비가열 | flexible: 고속 TPU, AMS 불가 |
| **TPU for AMS** | `Bambu TPU for AMS @base` | 230 / 35 / 12 | 70°C 8h | 가능 | SS/HS 0.4+, 비가열 | flexible: AMS용 68D TPU |
| **PVA** | `Bambu PVA @base` | 240 / 55 / 6 | 건조 필수, AMS HT 권장 | 가능 (dried 조건) | SS/HS, 낮은 챔버 | support: 수용성 서포트 |
| **Support W** | `Bambu Support W @base` | 220 / 55 / 12 | 55°C 8h | 가능 | SS/HS | support: PLA 계열 서포트 |
| **Support For PLA** | `Bambu Support For PLA @base` | 220 / 55 / 6 | 55°C 8h | 가능 | SS/HS | support: PLA 전용 인터페이스 |
| **Support For PLA/PETG** | `Bambu Support For PLA/PETG @base` | 210 / 60 / 6 | 건조 권장 | 가능 | SS/HS | support: PLA/PETG 분리성 |
| **Support for ABS** | `Bambu Support for ABS @base` | 260-270 / 90 / 6 | 80°C 8h | 가능 | SS/HS, 45-60°C | support: ABS용 |
| **Support For PA/PET** | `Bambu Support For PA/PET @base` | 280 / — / 8 | 건조 필수 | 확인 필요 | hardened 권장, 45-60°C | support: PA/PET-CF 계열 |
| **Support G** | `Bambu Support G @base` | 280 / 100 / 8 | 건조 필수 | 확인 필요 | hardened 권장 | support: 고온재 서포트 |

## 2. 용도별 우선 추천

| 용도 | 우선 소재 |
|------|----------|
| 빠른 시제품 / 치수 확인 | PLA Basic, PLA Lite |
| 고급 외관 / 무광 | PLA Matte, PLA-CF, ASA-CF |
| 광택 / 장식 | PLA Silk+, PLA Metal, PLA Galaxy, PLA Sparkle |
| 반투명 / 라이트 파이프 | PETG Translucent, PLA Translucent |
| 실사용 브래킷 / 커버 | **PETG HF** |
| 실외 외장 / UV 노출 | ASA, ASA-CF, 경량이면 ASA-Aero |
| 내열 하우징 | PC, PC FR |
| 기어 / 지그 / 고강도 | **PAHT-CF** 우선, 흡습 감수 시 PA6-CF |
| 최고 내열 / 내화학 | PPS-CF, PPA-CF |
| 유연 + AMS 멀티컬러 | **TPU for AMS** |
| 유연 단일 소재 | TPU 95A HF (외부 스풀) |
| 쉬운 서포트 제거 | PLA/PETG → Support For PLA/PETG · PA/PET → Support For PA/PET · ABS → Support for ABS |

## 3. 비슷한 소재 트레이드오프

**PLA Matte vs PETG Translucent**
- PLA Matte: 외관·쉬운 출력 ↑, 내열·내충격 ↓
- PETG Translucent: 질김·내열 ↑, 투명감 위해 속도 ↓ 필요, 표면 튜닝 민감

**PETG HF vs ABS/ASA**
- PETG HF: 냄새/수축 ↓, 실사용 부품 기본값으로 적합
- ABS/ASA: 내열·후가공·내후성 ↑, 챔버 45-60°C + 환기 사실상 필수

**PAHT-CF vs PA6-CF**
- PAHT-CF: 저흡습·안정성 ↑, 추천 기본값
- PA6-CF: 강도·인성 ↑, 흡습 관리 빡빡

**PPA-CF / PPS-CF vs PAHT-CF**
- PPA/PPS: 고내열 최상위, 건조 온도·AMS 경로 제약 큼 → "필요할 때만"
- PAHT-CF: 범용 엔지니어링은 더 현실적

**TPU 95A HF vs TPU for AMS**
- TPU 95A HF: 더 TPU답고 빠름, 외부 스풀 전제
- TPU for AMS: 멀티컬러/AMS 워크플로 우선

## 4. 소재별 수축률 (v0.4.2 신규 — fit-critical 부품 공차 보정용)

3D 출력 후 cooling 단계에서 발생하는 dimensional 수축률. PLA 계열이 가장 안정, ASA/ABS가 가장 큰 수축. fit-critical 부품(베어링/볼트/인서트/슬라이드 fit)의 process JSON 공차 보정값(`xy_hole_compensation`, `xy_contour_compensation`, `elefant_foot_compensation`)을 결정할 때 참조.

| 소재 | 평균 수축률 | 권장 `xy_hole_compensation` | 권장 `xy_contour_compensation` | 비고 |
|------|-----------|-----------------------------|-------------------------------|------|
| **PLA Basic** | 0.2-0.3% | `+0.05` mm | `-0.05` mm | 가장 예측 가능, fit-critical 기본 |
| **PLA Matte** | 0.2-0.3% | `+0.05` mm | `-0.05` mm | PLA Basic과 동일 |
| **PLA Tough+** | 0.25-0.35% | `+0.075` mm | `-0.05` mm | 약간 더 크게 보정 |
| **PLA-CF** | 0.15-0.20% | `+0.05` mm | `-0.05` mm | CF가 수축 억제 |
| **PETG Basic** | 0.3-0.5% | `+0.075` mm | `-0.075` mm | 건조 필수 |
| **PETG HF** | 0.3-0.5% | `+0.075` mm | `-0.075` mm | 건조 필수 |
| **PETG-CF** | 0.2-0.3% | `+0.05` mm | `-0.05` mm | CF로 수축 억제, 건조 필수 |
| **ASA** | 0.5-0.8% | `+0.10` mm | `-0.10` mm | 챔버 + 환기 필수 |
| **ABS** | 0.5-0.8% | `+0.10` mm | `-0.10` mm | 챔버 + 환기 필수 |
| **PC** | 0.6-0.7% | `+0.10` mm | `-0.10` mm | 건조 필수, 수축 큼 |
| **PAHT-CF** | 0.4-0.6% | `+0.075` mm | `-0.075` mm | 어닐링 후 추가 수축 |
| **PA6-CF** | 0.4-0.6% | `+0.075` mm | `-0.075` mm | 흡습 영향 큼 |
| **TPU 90A** | 1.0-1.5% | `+0.15` mm | `-0.10` mm | 유연 — contour는 squeezable |
| **TPU 95A** | 1.0-1.5% | `+0.15` mm | `-0.10` mm | 유연 — contour는 squeezable |

⚠️ **권장값은 0.4mm nozzle + Bambu default flow ratio + flow calibration 완료 기준**. 다음 변수가 추가 영향:
- Flow calibration 미수행 시 ±0.05 추가 필요
- Pressure Advance 미수행 시 외벽 거친 영역 ±0.05
- AMS HT 건조 미수행 흡습 소재(PETG/PA/PC)는 +0.05 추가

자세한 공차 정책 + fit-critical 부품 분류 + calibration coupon 가이드는 `references/tolerance.md` 참조.

## 5. 미해결 / 검증 필요

1. **PLA Pure** — 2026-05-14 Bambu Studio 2.7.0 Public Beta에 신규 프리셋 추가됨. 2.6.0 stable에는 미포함이라 자동 추천/inherits 대상으로는 보류 안전.
2. **PA-CF 단종** — PAHT-CF 스토어 페이지에 PA-CF가 discontinued라고 명시. Studio에는 base가 남아 있지만 신규 추천은 PAHT-CF로.
3. **AMS 2 Pro 직접 로드 제약** — 공식 표는 PLA/PETG/ABS/ASA/PET/PA/PC/PVA/BVOH/PP/POM/HIPS, Bambu PLA-CF/PAHT-CF/PETG-CF/Support for PLA/PETG/TPU for AMS를 지원. **PET-CF/PPA-CF/PPS-CF/TPU 95A HF는 외부 스풀 또는 AMS HT bypass 권장.**
4. **챔버 값** — Bambu Studio H2S filament JSON은 챔버 목표값을 행별 명시하지 않음. 표의 챔버 범위는 TDS 권장 + H2S 65°C active chamber 스펙 기반 분류.

## 출처

- Bambu Filament Guide: https://bambulab.com/en-us/filament-guide
- AMS 2 Pro 공식: https://us.store.bambulab.com/products/ams-2-pro
- H2S 공식: https://us.store.bambulab.com/products/h2s
- H2/P2S hotend compatibility: https://us.store.bambulab.com/en/products/bambu-hotend-h2-p2s
- Bambu Studio Releases: https://github.com/bambulab/BambuStudio/releases
- 로컬 Bambu Studio `02.06.00.51` 시스템 프로파일
