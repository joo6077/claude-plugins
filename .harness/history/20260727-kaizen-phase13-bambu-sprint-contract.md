# Sprint Contract — Kaizen Phase 13 (bambu-kit)

- 날짜: 2026-07-27
- 브랜치: `kaizen/2026-07-27`
- 범위: `bambu-kit/skills/bambu-print-profile/SKILL.md`, `.../references/tolerance.md`, `.claude/skills/bambu-kaizen/SKILL.md`
- 판정 예정: CHANGED

## 리서치 (실측 조회 · URL 기록)

| # | 소스 | 확인 사실 |
| - | ---- | --------- |
| 1 | `PrintConfig.cpp` (bambulab/BambuStudio master) | `xy_hole_compensation` tooltip "Holes of object will be grown or shrunk in XY plane by the configured value" · `elefant_foot_compensation` `min = 0` · `precise_z_height` 는 coBool 실험 파라미터(Z 전용, XY 공차 아님) |
| 2 | `PrintConfig.hpp` | 공차 3키 모두 `PrintObjectConfig` 소속 → **per-object 오버라이드 가능**, 단 process JSON 은 값 1개만 표현 |
| 3 | `PrintObjectSlice.cpp` | `_shrink_contour_holes(contour, hole, expolygons)` = **경계 오프셋** → 지름 변화 = 2× · MM color-paint / fuzzy-skin 시 공차 강제 0 · `raft_layers != 0` 시 elefant foot 무효 |
| 4 | OrcaSlicer wiki quality_settings_precision | 동일 문구 + 폴리곤 오프셋 확인 (교차검증) |
| 5 | GitHub Releases API | 최신 2.8.1 (`v02.08.01.55`, 2026-07-14). 로컬 설치본 `02.06.00.51` |
| 6 | 3MF Core Spec | `<build>` 는 `@anyAttribute` 허용 → `<build p:UUID=...>` 스펙 적법 |
| 7 | 실측 3MF (`ferris-wheel-608zz/.../coupon1-608zz-OD-pocket.3mf`) | `<build p:UUID="2c7c…">` 실존 · 지오메트리는 `3D/Objects/object_N.model` (root `3dmodel.model` 는 vertex 0) · 임베드 config 에 `xy_hole_compensation: "0.075"` |

## 완료 조건

### T. 공차 SSOT 프레임 정합성 (PL-01)

- [ ] **T-01** [exact] `tolerance.md` 에 보정값이 **경계 오프셋**이고 **지름 변화 = 2 × 보정값**임을 명시한 절과 변환식 `보정값 = (목표지름 − 모델지름) / 2` 가 존재한다. 근거 URL 포함.
- [ ] **T-02** [exact] `tolerance.md` §2 / §4 표에서 "오프셋 값"과 "최종 지름"이 서로 다른 컬럼으로 분리되어 한 표 안에서 두 프레임이 섞이지 않는다.
- [ ] **T-03** [exact] §7 페리스 휠 worked example 의 수치가 2× 규칙과 일치한다 (`+0.05` → 22.10mm, `-0.05` → 7.90mm). 기존 `0.075 → 22.10mm` 서술이 남아있지 않다.
- [ ] **T-04** [exact] `SKILL.md` Phase 1.7.3 매핑표와 Phase 3 공차 매트릭스에서 "볼트 통과 hole = +0.05 추가" 단독 서술이 제거되고 두 곳의 볼트 처리 서술이 동일 규칙을 가리킨다.
- [ ] **T-05** [goal] PL-01 재발 방지: 계약(지름 프레임)과 구현(오프셋 프레임)이 갈라질 수 없도록 단일 변환식이 SSOT 1곳에 존재하고 SKILL.md 는 그것을 인용한다.

### S. Silent-skip 상호작용 (신규 · 소스 검증)

- [ ] **S-01** [exact] MM color-paint / fuzzy-skin painted 오브젝트에서 `xy_hole/xy_contour_compensation` 이 **강제 0** 이 된다는 경고가 `tolerance.md` 와 `SKILL.md` Gotcha 체크리스트 양쪽에 있다.
- [ ] **S-02** [exact] `raft_layers != 0` 이면 `elefant_foot_compensation` 이 무효라는 경고가 존재하고, `raft_layers` 를 override 대상으로 나열한 Phase 3 정책과 교차 참조된다.
- [ ] **S-03** [exact] `elefant_foot_compensation` 은 음수 불가(`min = 0`) 가 명시된다.

### G. 모델 형상 추출 견고성 (brittle-xml-tag-match)

- [ ] **G-01** [exact] `SKILL.md` Phase 1 로컬 `.3mf` 분기에 정식 XML 파서 기반 지오메트리 추출 절차가 있고, 지오메트리가 `3D/Objects/*.model` 에 있을 수 있음을 다룬다.
- [ ] **G-02** [exact] `sed`/`grep` 태그 범위 매칭 금지 + 속성 있는 태그(`<build p:UUID=…>`) 예시가 안티패턴으로 명시된다.
- [ ] **G-03** [exact] **빈 출력은 PASS 증거가 아니라 검증 실패 신호**라는 규칙이 명시된다 (skill-design-guide §3.7 정합).

### U. Surface Intent Gate (missed-surface-first-ironing)

- [ ] **U-01** [exact] 표면 품질 의도를 **모든 입력 분기**(MakerWorld / 로컬 3mf / STL / 채팅)에서 확인하는 게이트가 존재한다. MakerWorld 전용 Phase 1.6.5 에만 의존하지 않는다.
- [ ] **U-02** [exact] 게이트 미통과 시 Phase 3 진입 금지 문구가 있다.
- [ ] **U-03** [goal] "표면 매끈" 의도인데 `ironing_type: no ironing` 으로 완료 보고되는 경로가 차단된다.

### E. Completion Evidence Gate

- [ ] **E-01** [exact] Phase 4 에 생성된 JSON 을 **실제로 파싱해** 필수 키/값을 검증하는 결정론적 명령(LLM 미호출, 실패 시 non-zero exit)이 있다.
- [ ] **E-02** [exact] 해당 명령 출력 없이 완료 선언 금지 문구가 있다. `[미검증]` 마커는 정본(`qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol) 을 인용하며 동의어를 새로 정의하지 않는다.
- [ ] **E-03** [exact] 기존 Gotcha 체크리스트 항목은 삭제되지 않는다 (bambu-kaizen Gotcha 5 보존).

### D. 문서 위생 / 자기정합성

- [ ] **D-01** [exact] SKILL.md 의 중복된 "필수 메타필드" 헤더 1개가 제거된다.
- [ ] **D-02** [exact] SKILL.md 파일 구조 트리와 description 의 "references 4종" 이 실제 7개 파일과 일치한다.
- [ ] **D-03** [exact] Studio 버전 cross-check 표에 2.7.x / 2.8.x 밴드가 실측 릴리스 근거와 함께 반영된다.
- [ ] **D-04** [exact] `bambu-kaizen/SKILL.md` 의 "references 4종" → 실제 7종, Step 1 대상 목록에 누락된 references 가 추가된다.
- [ ] **D-05** [exact] `bambu-kaizen/SKILL.md` Step 4 에 `validate-plugin.py` 회귀 검증이 **8 카테고리 (V1~V8)** 로 명시된다.

### R. 회귀 / 정책 보존

- [ ] **R-01** [exact] `python3 scripts/validate-plugin.py bambu-kit` 8 카테고리 전부 OK.
- [ ] **R-02** [exact] `nozzle_temperature` / retraction / cooling 미수정 정책, `compatible_printers` H2S 고정, `wipe_on_loops` 부재 서술이 보존된다.
- [ ] **R-03** [exact] description 트리거 키워드("삼프 설정" 등)가 제거되지 않는다.
- [ ] **R-04** [exact] 범위 밖 파일(다른 kit, `harness/`, marketplace.json, plugin.json, changelog) 변경 0건.
- [ ] **R-05** [exact] 모든 code fence 에 언어 태그 (bare fence 0건).

## 측정 방법

- `git diff --stat` 로 R-04 확인
- `python3 scripts/validate-plugin.py bambu-kit` 로 R-01 / R-05
- `grep` 로 각 [exact] 문구 존재 확인
- E-01 명령은 실제 실행하여 출력 확보
