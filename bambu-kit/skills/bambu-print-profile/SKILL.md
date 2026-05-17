---
name: bambu-print-profile
description: Bambu Lab H2S 환경에서 MakerWorld URL이나 로컬 모델 파일을 받아 process+filament JSON 프로파일을 자동 생성하여 import용 zip 번들로 떨궈주는 스킬. references/ 4종을 토대로 모델 형상 분석 → 소재 추천 → seam 전략 결정 → Bambu Studio용 JSON 생성까지 수행한다. "삼프 설정", "Bambu 프로파일 만들어줘", "출력 셋팅 추천", "프린트 프로파일", "MakerWorld 출력" 같은 요청 시 트리거. 단순 색상/온도/한 값 변경에는 트리거 X. 다른 프린터(X1/P1/A1 등)나 다른 슬라이서(OrcaSlicer/PrusaSlicer)에는 트리거 X — H2S + Bambu Studio 고정.
user-invocable: true
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

bambu-kit 플러그인 일부. 설치 시 `~/.claude/plugins/cache/joo6077-plugins/bambu-kit/<version>/skills/bambu-print-profile/`에 풀린다.

```text
bambu-kit/skills/bambu-print-profile/
├── SKILL.md                          # 이 파일
├── BACKLOG.md                        # v2 카이젠/자동 capture 백로그
└── references/
    ├── bambu-fields-baseline.md      # Bambu Studio JSON schema (필수 필드, 키 이름) + §8 Surface 필드 19종
    ├── materials.md                  # 40+ 필라멘트 카탈로그 + 용도 매핑
    ├── seam-recipes.md               # 형상×소재 scarf 매트릭스 + Real-world findings + §0 Surface-first 회전체 default v2
    ├── surface-recipes.md            # Surface-first 정책 (Auto-select 결정 트리 + 외벽/Top·Bottom/Ironing 매트릭스 + 트레이드오프)
    └── kaizen-sources.md             # 주 1회 갱신용 데이터 소스 (카이젠 스킬용)
```

출력 경로: **`/Users/jackson/Hub/60_3D Print/Settings/<모델명>/`**

## 워크플로우 (3단계)

### Phase 1 — 모델 컨텍스트 추출

**입력 분기:**

1. **MakerWorld URL** → **Playwright MCP 1차** (`mcp__playwright__browser_navigate` → `mcp__playwright__browser_snapshot` 또는 `browser_take_screenshot`). MakerWorld Cloudflare 차단을 우회하고 JS-rendered 모델 상세/댓글/사진까지 추출 가능. 추출 정보: 모델명/제작자/부품 구성/회전체 부품/권장 프로파일/사용자 댓글에서 소재 후기. Playwright 미사용 환경이면 `codex-rescue` 에이전트에 위임 (research mode), 둘 다 실패 시 사용자에게 직접 입력 요청.
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

**Surface-first 모드 (default ON — 사용자 요구가 "표면 매끈 / 심 안 보임 / 속도 무시"일 때):**

상세 정책은 `references/surface-recipes.md` 참조. SKILL은 결정 트리 분기와 형상 enumerate만 인라인으로 가진다.

```text
회전체 default — Auto-select 결정 트리 (surface-recipes.md §2.1)
  ※ 우선순위 원칙: 사용자 추가 작업이 없는 옵션이 default top.
  │
  ├─ 1. spiral_mode 적용 가능? (단일 외벽, top 없음, infill 불필요, 단일 색상)
  │      YES → spiral_mode = 1 (진짜 무 seam, Z축 연속 나선)
  │             사용자 작업: 없음
  │
  ├─ 2. DEFAULT — random 분산 전략 (사용자 작업 X)
  │      seam_position: random + seam_slope_entire_loop: 1
  │      + scarf external (length 15-20mm, gap 5-10%, height 0-10%, steps 10)
  │      → wheel/원통 둘레 전체에 ramp 분산, 한 줄 라인 없이 specks
  │      → spoke/텍스처 구조에 자연 위장
  │      트레이드오프: micro-banding (specks). seam-recipes.md Real-world Finding 1
  │      사용자 작업: 없음
  │
  └─ 3. 사용자가 명시적으로 "specks도 싫고 완벽한 클린 면" 요청 시에만 OPT-IN
         → seam_position: aligned (또는 back) + scarf external
         + 사용자가 Studio UI seam paint tool로 숨김 영역 페인팅 필수 (5-10분)
         ※ painted 안 하면 visible 면에 한 줄 라인 그대로 남음
         사용자 작업: 필수 (Studio UI 페인팅)
```

⚠️ **자동화 우선 원칙**: spiral 불가 회전체는 (2) random fallback이 default. (3) painted는 사용자가 명시적으로 "specks 분산도 거슬린다, 한 줄로 완벽히 숨기고 싶다"고 요청할 때만 OPT-IN으로 전환. 사용자 작업이 필요한 옵션을 자동으로 default top에 두지 않는다.

**형상별 결정 트리 (6개 enumerate — surface-recipes.md §2 참조):**

1. **회전체 / 원기둥 / 컵 / 화병** (rotational / cylinder): 위 Auto-select 트리
2. **박스 / 직육면체** (box / rectangular): `seam_position: back` (또는 aligned) + corner painted seam + scarf off 또는 length 5-8mm. random 금지 (평평한 면에 specks 분산 시 외관 ↓)
3. **유기적 곡면 / 피규어** (organic / curved): `seam_position: aligned` (back 우선) + painted seam (주름/접합부/머리카락 텍스처) + scarf external length 10-15mm
4. **얇은 벽 / 미세 디테일** (thin wall): `seam_position: aligned` + scarf length 짧게 (5-10mm) 또는 off. `Contour and Hole` 비추 (내경 치수 영향). `wall_loops` 1-2 + Arachne 검토
5. **평면 top 강조** (flat top — 도구/케이스 lid/박스 top): seam은 후면/코너 + **Top surface 품질이 외벽보다 우선** + ironing 적극 적용 (surface-recipes.md §5)
6. **spiral vase 가능 모델** (spiral mode applicable): 단일 외벽 + top X + infill X + 단일 색상 → `spiral_mode = 1`. 다른 설정 (seam_position, scarf, ironing) 무의미

**Ironing 정책 (surface-recipes.md §5 위임):**

8개 소재 적용 판정 요약 — 자세한 `ironing_type` / `ironing_speed` / `ironing_flow` / `ironing_spacing` / `ironing_inset` 값은 `references/surface-recipes.md` §5.1 매트릭스 참조.

| 소재 | 판정 |
|------|------|
| PLA Basic / PLA Matte | `topmost_only` 적극 권장 |
| PLA Silk | `topmost_only` only — 광택 죽음 주의 |
| PETG HF | 원칙 off, 평면 장식만 `topmost_only` (blob/scar 위험) |
| PA-CF / PAHT-CF | off (fiber 질감, 노즐 마모) |
| PC | off 또는 소형 `topmost_only` 실험 (heat creep / ooze) |
| ABS / ASA | `topmost_only` 실험 가능 (후가공 가능 시 의존 낮춤) |
| TPU | off (불가 — 유연성으로 표면 drag) |

형상별 ironing 적용성: 회전체/spiral vase는 무의미(top 없음), 박스/평면 top은 강함, 유기적 곡면은 부분, 얇은 벽은 거의 off. surface-recipes.md §5.2 참조.

**외벽 표면 공통 (surface-recipes.md §3):**

`layer_height` 0.08-0.12mm / `wall_loops` 3-4 / `outer_wall_speed` 20-40 mm/s / `wall_sequence` `inner-outer-inner wall` / `reduce_crossing_wall: 1` / `resolution` 0.006-0.010mm / PA · flow calibration 전제. 소재별 보정은 surface-recipes.md §3 표 참조.

⚠️ **PETG HF 안전 경고 — surface-first 모드 적용 시 PETG HF는 AMS HT 65°C 8h 사전 건조 + continuous drying 필수**. 건조 부족 + 낮은 outer speed 조합은 stringing/blob 폭발. seam-recipes.md Finding 4 + surface-recipes.md §6.5 참조.

### Phase 4 — Bundle + Verify

zip 구조 (Bambu Studio Import Configs 호환):
```text
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

## MakerWorld URL fallback 체인 (2026-05-16 갱신)

1. **Playwright MCP** (1차, 권장) — `mcp__playwright__browser_navigate` + `mcp__playwright__browser_snapshot` 조합. JS 렌더링 페이지 정상 처리, Cloudflare bot challenge 우회. 이미지 캡처가 필요하면 `mcp__playwright__browser_take_screenshot` 추가. **개인 환경에 Playwright MCP가 설치되어 있을 때 가장 정확**.
2. **`codex-rescue` 에이전트** (Playwright 미설치 환경) — research mode 위임. Codex 측 캐시/웹검색 결과 활용 가능. 단 MakerWorld 본문은 못 가져올 수 있음 (캐시된 페이지 또는 우회 정보만).
3. **WebFetch** (마지막 대안) — 보통 Cloudflare 차단으로 실패. 트래픽 패턴이 가벼운 시간대에만 간헐적 성공.
4. **사용자 직접 입력** — 위 모두 실패 시 "이 모델 어떤 부품 구성이고 어떤 소재 권장돼?" 질문으로 핵심 정보만 받기.

> ⚠️ **WebFetch만 단독 시도 금지** — Cloudflare 차단이 default이므로 무한 retry 시 토큰 낭비. 1번부터 4번 순서로 시도하고 명시적으로 fallback 보고.

## v2 백로그 (수동으로 진행)

플러그인 내 `bambu-kit/skills/bambu-print-profile/BACKLOG.md` 참조. 핵심:
- 홈서버 Linux에 print outcome capture daemon (MQTT + FTPS + JSONL)
- 카이젠 스킬은 이 레포의 `.claude/skills/bambu-research` + `.claude/skills/bambu-kaizen`에 분리됨 (자동 주기 폴링 + SKILL 격차 분석). bambu-kit 플러그인에는 포함되지 않는다.
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
