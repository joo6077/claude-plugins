---
name: bambu-print-profile
description: Bambu Lab H2S 환경에서 MakerWorld URL이나 로컬 모델 파일을 받아 process+filament JSON 프로파일을 자동 생성하여 import용 zip 번들로 떨궈주는 스킬. references/ 4종을 토대로 모델 형상 분석 → 소재 추천 → seam 전략 결정 → Bambu Studio용 JSON 생성까지 수행한다. "삼프 설정", "Bambu 프로파일 만들어줘", "출력 셋팅 추천", "프린트 프로파일", "MakerWorld 출력" 같은 요청 시 트리거. 단순 색상/온도/한 값 변경에는 트리거 X. 다른 프린터(X1/P1/A1 등)나 다른 슬라이서(OrcaSlicer/PrusaSlicer)에는 트리거 X — H2S + Bambu Studio 고정.
---

# Bambu Print Profile Skill

H2S + AMS HT + AMS 2 Pro + Bambu Studio v2.6.0+ 환경 가정. 사용자의 모델(URL/파일)을 받아 process+filament JSON을 생성하고 import용 zip을 떨궈준다.

## 트리거 조건

**트리거함:**
- MakerWorld URL이 메시지에 포함 (`makerworld.com/en/models/...`)
- 로컬 모델 파일 경로(.3mf/.stl/.step) 언급
- "삼프 설정", "Bambu 프로파일 만들어줘", "출력 셋팅", "프린트 셋팅", "MakerWorld 모델 출력하려고" 같은 표현
- "원기둥 seam 안 보이게", "회전체 표면 깔끔하게" 같은 형상 + seam 결합 요청

**트리거 안 함:**
- 단순 1필드 변경 ("온도 245로 해줘", "색만 바꿔줘")
- 기존 프로파일 리뷰
- 다른 프린터 / 다른 슬라이서 언급
- 슬라이싱 결과 분석만 요청 ("이 출력 어땠어?")

## 작업 디렉토리 / 파일 구조

```
~/.claude/skills/bambu-print-profile/
├── SKILL.md                          # 이 파일
├── TODO.md                           # v2 카이젠/자동 capture 메모
└── references/
    ├── bambu-fields-baseline.md      # Bambu Studio JSON schema (필수 필드, 키 이름)
    ├── materials.md                  # 40+ 필라멘트 카탈로그 + 용도 매핑
    ├── seam-recipes.md               # 형상×소재 scarf 매트릭스 + Real-world findings
    └── kaizen-sources.md             # 주 1회 갱신용 데이터 소스 (카이젠 스킬용)
```

출력 경로: **`/Users/jackson/Hub/60_3D Print/Settings/<모델명>/`**

## 워크플로우 (3단계)

### Phase 1 — 모델 컨텍스트 추출

**입력 분기:**

1. **MakerWorld URL** → WebFetch가 Cloudflare 차단으로 실패할 가능성 100%. 바로 `codex-rescue` 에이전트에 위임 (research mode). 추출할 정보: 모델명/제작자/부품 구성/회전체 부품/권장 프로파일/사용자 댓글에서 소재 후기.
2. **로컬 .3mf 파일** → `unzip -p <path> Metadata/project_settings.config` 등으로 embedded 설정 직접 읽기. 부품별 dimension은 Bambu Studio에서 확인 권장.
3. **STL 파일** → bounding box + 부품 수 정도만 셸로 추출 (`du -h`, file inspection). 회전체 식별은 사용자 설명 의존.
4. **이미 정보가 채팅에 있음** → 그대로 사용.

추출 후 사용자에게 짧게 보고: 모델명, 부품 수, 회전체 여부, 권장 소재 후기 (있다면).

### Phase 2 — 소재 추천 (2-3개 + 사용자 픽)

`references/materials.md`를 로드. 모델 용도/형상/사용자 요구에 매칭:

| 용도 | 우선 후보 |
|------|----------|
| 박스 오프너/도구 (functional) | PETG HF, PLA Tough+ |
| 내열 부품 (vent, hot duct) | PETG HF, ASA, PC |
| 외관 prototype | PLA Basic, PLA Matte |
| 실외 부품 | ASA, ASA-CF |
| 기어/지그 | PAHT-CF, PETG-CF |
| 멀티컬러 가벼운 출력 | PLA Basic (같은 base 공유) |
| Sealing/gasket | TPU 90A (TPU 85A 비추 — 검증된 문제) |

**필수 cross-check:**
- AMS 2 Pro 직접 로드 가능 여부 (PET-CF/PPA-CF/PPS-CF/TPU 95A HF는 외부 스풀)
- 건조 요구 (PETG/PA/PC는 AMS HT 65°C 사전 + continuous)
- H2S 노즐 호환 (CF류는 hardened 권장)

후보 제시 → 사용자 픽. 단일/멀티 소재 결정.

### Phase 3 — 프로파일 JSON 생성

`references/bambu-fields-baseline.md` + `references/seam-recipes.md` 로드.

**필수 메타필드 (silent skip 회피 — Codex run `a2a01770a87626167` 검증):**

| 필드 | 값 | 비고 |
|------|----|------|
| `type` | `"process"` 또는 `"filament"` | |
| `name` | `"<모델명> - <변종> 0.12mm"` 등 사용자 인지 가능 이름 | |
| `version` | `"2.6.0.2"` | Semver parseable 필수. 이 값이 현재 v2.6.0과 호환. |
| `from` | `"User"` | **대문자 U** — `"user"` 소문자는 실패 |
| `inherits` | 시스템 프리셋명 정확 일치 | 못 찾으면 silent skip |
| `print_settings_id` / `filament_settings_id` | name과 동일. filament은 **배열 형태** | 빠지면 "Preset type is unknown" |
| `compatible_printers` | `["Bambu Lab H2S 0.4 nozzle"]` | H2S 고정 |

**process JSON 튜닝 정책 (override 대상):**

- ✅ `layer_height`, `initial_layer_print_height` (사용자 요구 반영)
- ✅ `wall_loops`, `sparse_infill_density`, `top/bottom_shell_layers`, `wall_sequence` (모델 형상 기반)
- ✅ `seam_position`, `seam_slope_*`, `scarf_angle_threshold`, `override_filament_scarf_seam_setting` (seam 전략)
- ✅ `outer_wall_speed`, `inner_wall_speed` (소재별)
- ✅ `enable_arc_fitting` (원통 모델)
- ✅ 멀티컬러: `enable_prime_tower`, `prime_tower_width/brim_width/flat_ironing`, `flush_into_*`
- ✅ `enable_support`, `raft_layers`

**filament JSON 튜닝 정책 — `seam-recipes.md`에서 결정된 scarf 필드만 override:**

- ✅ `filament_scarf_seam_type` (none/external/all)
- ✅ `filament_scarf_height`, `filament_scarf_gap`, `filament_scarf_length`
- ❌ **`nozzle_temperature`, `nozzle_temperature_initial_layer` 안 건드림** — 사용자가 .3mf의 creator 튜닝 값이나 base profile 기본값을 유지하길 원함 (사용자 명시 요청 2026-05-16)
- ❌ retraction/fan/cooling 안 건드림 — base에 위임

**Seam 전략 결정 트리 (seam-recipes.md + Real-world findings 활용):**

```
회전체/원기둥 (전방향 노출)?
  YES → seam_position: random + seam_slope_type: external + seam_slope_entire_loop: 1
        + seam_slope_inner_walls: 0 (내벽 scarf 불필요 — 안 보이는 곳)
        + wall_sequence: inner-outer-inner wall
        + 소재별 scarf 파라미터 (PETG는 gap 8%/length 12, PLA는 gap 10%/length 20)
  NO → 형상 분기:
       박스/직육면체 → seam_position: back + 일반 seam (scarf 짧게 또는 none)
       유기적/피규어 → seam_position: aligned + painted seam 가이드 (Studio UI)
       얇은 벽/미세 → seam_position: aligned + scarf length 짧게 (5-10mm)
```

⚠️ **PETG HF + entire_loop 콤보는 stringing 민감** — `seam-recipes.md` Finding 4 참조. 사용자에게 **AMS HT 65°C 8h 사전 건조 + continuous drying 필수** 강조.

### Phase 4 — Bundle + Verify

zip 구조 (Bambu Studio Import Configs 호환):
```
<modelname>.zip
├── process/
│   └── <process name>.json
└── filament/
    ├── <filament 1>.json
    └── <filament 2>.json   (멀티 소재인 경우)
```

생성 후 사용자에게 안내:
1. `File → Import → Import Configs...` → `<modelname>.zip` 선택
2. 좌측 Process/Filament 드롭다운에 새 preset 보이는지 **반드시 확인**
3. 안 보이면 셸로 검증:
   ```bash
   ls "$HOME/Library/Application Support/BambuStudio/user/<userid>/process/"
   ls "$HOME/Library/Application Support/BambuStudio/user/<userid>/filament/"
   ```
   `.json` + `.info` 페어 확인.

### Phase 5 — Coupon Test (선택, 강력 권장)

다음 케이스에 coupon test 가이드 제공:
- 출력 시간 > 4시간
- 회전체 + seam-critical
- 새 소재 또는 새 scarf 조합 첫 시도

coupon-process.json도 함께 생성 (lean: top/bottom_shell 0, infill 0%, 같은 scarf settings). 사용자가 Studio에서 cylinder primitive 추가 (30x30x9mm 등) → coupon process 적용 → 짧게 출력 → 결과 평가 후 본 출력 결정.

## Gotcha 체크리스트 (생성 직후 자기 검증)

생성한 JSON이 silent skip 안 되도록:

- ☐ `version`이 `"2.6.0.2"` (또는 현재 Bambu Studio 버전 매칭)
- ☐ `from`이 `"User"` (대문자)
- ☐ `print_settings_id` / `filament_settings_id` 존재 (filament은 배열)
- ☐ `inherits`가 시스템 프리셋에 실제 존재 (필요 시 셸로 `ls ~/Library/Application Support/BambuStudio/system/BBL/{process,filament,machine}/ | grep`)
- ☐ `compatible_printers`에 H2S 명시
- ☐ filament JSON의 scarf 필드는 모두 **배열** (`["..."]`)
- ☐ `nozzle_temperature` 등 사용자 영역 필드 안 건드렸는지

## MakerWorld URL fallback 체인

WebFetch (보통 Cloudflare 차단)
→ `codex-rescue` 에이전트에 research 위임 (캐시 검색 결과 활용 가능)
→ 사용자에게 직접 정보 요청 ("이 모델 어떤 부품 구성이고 어떤 소재 권장돼?")

## v2 TODO (수동으로 진행)

`~/.claude/skills/bambu-print-profile/TODO.md` 참조. 핵심:
- 홈서버 Linux에 print outcome capture daemon (MQTT + FTPS + JSONL)
- 카이젠 스킬 (`bambu-print-profile-kaizen`) 주 1회 cron → kaizen-sources.md 데이터 소스 폴링 → references 자동 보강
- 실측 피드백을 references에 자동 환류 (v1은 손으로 함)

## 매 실행 시 권장 사전 절차

1. **현재 Bambu Studio 버전 cross-check** (memory 또는 셸로):
   ```bash
   defaults read /Applications/BambuStudio.app/Contents/Info.plist CFBundleShortVersionString
   ```
   `02.06.00.xx`이면 references baseline 그대로. major 버전이 다르면 references 업데이트 권장.

2. **memory 자동 로드:**
   - `3d_printing_setup.md` — 하드웨어 환경 확인
   - `bambu_studio_json_import.md` — silent skip 회피 규칙
   - `bambu_print_profile_skill.md` — v1 학습 환류

## 검증된 실측 사례

| 모델 | 소재 | 결과 |
|------|------|------|
| Box opener knife (583712) | PLA Basic dual-color | ✅ 정상 출력 검증. 회전체 손잡이 seam은 random + external 처리 |
| H2D Vent Pipe (1441653) | PETG HF + TPU 90A | ⚠️ stringing 발생 (필라멘트 건조 부족 의심). seam은 random + external + entire_loop |

`/Users/jackson/Hub/60_3D Print/Settings/<modelname>/notes.md`에 케이스별 detail 보존.

## 출처

- 4개 Codex research run으로 references 빌드 (`a5afcf864d05cf3b7`, `aeb457c7603a420db`, `afcf4968339021b29`, `ab679b7fbc81fa7b6`)
- 추가 검증: `aab7cad186e9523af` (멀티컬러 필드), `a2a01770a87626167` (JSON import gate), `a06a8ac153247d901` (wipe_on_loops Bambu 부재 확인)
- 실측 피드백: 2026-05-15 ~ 2026-05-16 박스 오프너 + vent pipe 테스트
- 전체 로그: `~/.claude/codex-research-log/2026-05.md`
