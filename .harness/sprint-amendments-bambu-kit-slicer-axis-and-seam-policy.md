# Amendments — bambu-kit-slicer-axis-and-seam-policy

계약 본문은 봉인(`sha256:209ae5150c40cb31`)되어 수정하지 않는다. 아래는 구현 중 발견한
조건 결함과 그 처리를 기록한 것이다.

## AM-01 — AR-03 측정문이 판별력 없음

- **조건 원문**: "파생 HTML 3 종 … 이 소스 변경을 반영한다 [exact, enumerated]
  (측정: 3 파일 각각 `grep -c 'Orca'` >= 1)"
- **결함**: 구현 착수 시점에 이미 세 파일 모두 `Orca` 를 포함하고 있었다 (실측:
  `bambu-print-profile.html` 2 건 · `seam-recipes.html` 14 건 · `surface-recipes.html` 7 건).
  기존 문서가 오르카를 *배제 맥락*으로 언급했기 때문이다. 따라서 이 측정문은
  **아무 작업을 하지 않아도 통과**한다 — 조건의 의도(소스 변경 반영)를 측정하지 못한다.
- **태그**: `측정-무판별`
- **direction**: `unknown` — 측정 오라클의 결함이며 조건 범위를 넓히거나 좁히지 않는다
- **consent**: 불필요 (조건 문구를 바꾸지 않는다)
- **처리**: 원 측정문을 그대로 두고, 구현은 **의도 기준으로 수행**한다. 아래를 실제 판정 근거로 삼는다.

  | 파일 | 반영해야 할 소스 신설 | 실판정 측정 |
  | --- | --- | --- |
  | `seam-recipes.html` | `seam-recipes.md` §6.5 (루프가 작고 많은 형상) | `grep -c 'seam_slope_conditional'` >= 1 |
  | `surface-recipes.html` | `surface-recipes.md` §2.8 (벽 예산) | `grep -c 'outer_wall_line_width'` >= 1 |
  | `bambu-fields-baseline.html` | `bambu-fields-baseline.md` §11 (슬라이서 키 차이) | `grep -c 'scarf_joint_speed'` >= 1 |

  세 값이 모두 >= 1 이어야 실제로 반영된 것이다. 원 조건의 `grep -c 'Orca'` 는 그대로 충족되므로
  계약상 PASS 이나, 그 통과는 **근거가 되지 못한다**는 사실을 여기 남긴다.

- **다음 계약 반영 사항**: 측정문에 쓸 토큰은 **구현 전 baseline 을 1 회 실행해 0 건임을 확인**한
  뒤 고른다. 이미 존재하는 토큰을 세면 판별력이 없다.

## AM-02 — Codex 감사 지적 6 건 (2026-09-14, 미조치·다음 세션 이월)

감사 호출: `codex exec --model gpt-5.6-sol -s workspace-write -o <out> ... </dev/null` (조회 전용)
결과 원문: `scratchpad/audit.md` (7,763 bytes)

**방법론 오류 — 프로파일 등장 횟수를 "키 존재"로 해석했다.** 기본값과 같으면 프로파일 JSON 에
안 적히므로, 프로파일 차집합은 **기능 차집합이 아니다.** 이것이 아래 1~4 의 공통 뿌리다.

| # | 위치 | 지적 | 올바른 값 |
| --- | --- | --- | --- |
| 1 | `bambu-fields-baseline.md:388-391` | "뱀부 전용" 7 개 중 5 개가 오르카에도 있다 | `filament_scarf_seam_type`(뱀부 7/오르카 89) · `filament_scarf_height`(10/66) · `filament_scarf_gap`(12/67) · `filament_scarf_length`(5/54) · `override_filament_scarf_seam_setting`(1/2) · `seam_placement_away_from_overhangs`(1/2) · `seam_slope_gap`(1/2). 실제 뱀부 전용은 `monotonic_travel_into_wall` · `reduce_infill_retraction_mode` 둘뿐 |
| 2 | `bambu-fields-baseline.md:376` | "`wall_sequence` 는 뱀부에 없다" 가 틀림 | 프로파일 명시 0 건이지만 **바이너리에 존재**. 같은 문제가 `seam_slope_steps` · `wall_distribution_count` · `wall_transition_length` · `wall_transition_angle` · `wall_transition_filter_deviation` 에도 있다 |
| 3 | `bambu-fields-baseline.md:209-213` ↔ `:376` | **자기모순** — 209 줄이 "프로파일 0 건이어도 키가 없는 게 아니다" 라고 이미 써놨다. `:62-64` 도 뱀부 신규 JSON 에 `wall_sequence` 를 쓰라고 한다 | 표현 통일 |
| 4 | `bambu-fields-baseline.md:371` · `seam-recipes.md:298` | "`scarf_joint_speed` 가 없어서 뱀부에선 짧은 루프에 경사를 못 쓴다" 가 과장 | "경사 구간 속도를 **따로 제어할 수 없다**". 뱀부에도 `seam_slope_type` · `seam_slope_min_length` · `filament_scarf_*` 가 있다 |
| 5 | `SKILL.md:723` ↔ `:1327` ↔ `:1338` | **`TARGET_SLICER` 전달 경로가 없다.** Phase 1.95 가 값을 정해도 실행 명령이 Python 에 안 넘겨서 `globals().get("TARGET_SLICER")` 가 항상 `None` → 늘 뱀부로 폴백. **오르카 산출물을 뱀부 스코프로 검사하는 회귀** | 실행 명령에 인자 추가 |
| 6 | `gate-fixtures/*.json` 2 종 | **음성 대조 역할을 못 한다.** 두 픽스처가 각각 오류 7 건·6 건을 내는데 `version`·`from`·`print_settings_id` 누락과 `thin` 인데 외벽 하향 등 목표 외 위반이 섞였다. **검사를 지워도 계속 떨어져** 판별력이 없다 | 목표 위반 1 개만 남기고 나머지 필드를 정상값으로 채운다 |

**부수 지적** — enum 허용값 표(`SKILL.md:1415-1425`)도 슬라이서별로 분기하지 않고 뱀부 값 하나만
쓴다. 양쪽 지원을 선언한 변경과 어긋나 오르카에서 오탐·누락 위험이 있다.

**계약 영향** — #6 은 SC-01 의 `음성 대조:` 절 요구를 실질적으로 충족하지 못한 상태다. 별도
스크립트로 돌린 음성 대조(3 종=오류 2 건 / 2 종=통과)는 판별력이 있었으나, 픽스처 파일로 옮기면서
그것을 잃었다. **QA 평가 전에 #5·#6 을 먼저 고쳐야 한다.**

**다음 계약 반영 사항** — "키가 어느 슬라이서에 있는가" 를 판정할 때는 프로파일 집계만으로
결론내지 말고 **바이너리 문자열까지 함께** 본다. 두 근거가 갈리면 그 사실 자체를 적는다.

---

## AM-02 처리 결과 (2026-09-14, 같은 스프린트 내 조치)

계약 본문은 건드리지 않았다. 아래는 위 표 6 건과 부수 지적 1 건의 조치 결과다.
**우선순위 지시대로 #5 · #6 을 먼저 고쳤다.**

### #5 — `TARGET_SLICER` 전달 경로 없음 → 조치 완료

`SKILL.md` 실행 명령을 `TARGET_SLICER=<bambu|orca> python3 - …` 로 바꾸고, 스크립트는
`os.environ.get("TARGET_SLICER")` 로 읽는다. heredoc 안의 스크립트는 셸 변수도 파이썬 전역도
못 보므로 `globals().get(...)` 은 구조적으로 항상 `None` 이었다.

**폴백을 없앴다.** 종전에는 지정 슬라이서 경로가 없으면 *실재하는 다른 쪽*으로 넘어갔다 —
오르카 산출물을 뱀부 스코프로 검사하는 바로 그 회귀다. 이제 미전달 · 오타값 · 설치본 부재는
전부 `[미검증]` 으로 떨어뜨리고 다른 슬라이서로 대신 검사하지 않는다 (ER-02 경로와 합치).

실측 — 같은 파일을 네 조건으로 돌린 출력:

```text
TARGET_SLICER=orca   → SLICER orca: /Applications/OrcaSlicer.app/Contents/Resources/profiles/BBL
                       [미검증] brim_type 는 설치본 어느 시스템 프로파일에도 없는 키
TARGET_SLICER=bambu  → SLICER bambu: /Applications/BambuStudio.app/Contents/Resources/profiles/BBL
                       RESULT: PASS   (미검증 0 건)
미전달                → [미검증] TARGET_SLICER 미전달 — 스코프/부모값 검사 미실행
TARGET_SLICER=orcaslicer → [미검증] TARGET_SLICER='orcaslicer' 는 bambu|orca 가 아니다
```

첫 두 줄이 **서로 다른 경로를 잡고 서로 다른 결과를 낸다**는 점이 인자 전달이 실제로 먹었다는
근거다. 경로만 출력되고 결과가 같으면 증거가 못 된다.

### #6 — gate-fixtures 판별력 없음 → 조치 완료

두 픽스처에 `version` · `from` · `print_settings_id` 를 채우고, `thin` + 외벽 하향 충돌과
유량비 초과를 없앴다 (`_geometry_class` 를 `planar` 로, 인접 속도를 정상값으로). 스코프 픽스처는
목표 키를 `retraction_minimum_travel` 하나로 줄였다. 결과는 **각 파일 FAIL 정확히 1 건**이다.

검사 제거 대조를 실제로 돌린 출력:

```text
[검사 유지]    FAIL process-machine-scope-key.json: 키 스코프 불일치 retraction_minimum_travel
               RESULT: FAIL   exit=1
[machine 제거] OK   process-machine-scope-key.json: type=process from=User keys=17 …
               [미검증] retraction_minimum_travel 는 설치본 어느 시스템 프로파일에도 없는 키
               RESULT: PASS   exit=0

[검사 유지]    FAIL process-seam-slope-type-invalid.json: enum seam_slope_type='hole' 는 허용값이 아니다
               RESULT: FAIL   exit=1
[enum 제거]    OK   process-seam-slope-type-invalid.json: type=process from=User keys=19 …
               RESULT: PASS   exit=0
```

변이가 실제로 적용됐는지 먼저 확인했다 — `KINDS` 행 원본 1 건 → 변이본 0 건, enum 행 원본 1 건 →
변이본 0 건, 줄 수 213 → 212. `TARGET_SLICER` 를 `bambu` · `orca` 로 각각 돌려 동일 결과였다.

`machine` 분기를 지웠을 때 FAIL 이 사라지고 `[미검증]` 으로 **강등**된다는 점이 핵심이다.
판정 불가는 통과로 취급되므로 스코프 종류를 하나 빠뜨리면 위반이 조용히 통과한다.
이 절차와 실측 출력을 `SKILL.md` 음성 대조 절에 그대로 넣었다 — SC-01 의 `음성 대조:` 요구가
이제 문서에서 재현 가능하다.

### 방법론 — #1~#4 의 공통 뿌리를 먼저 측정했다

지시대로 **바이너리 문자열과 프로파일 집계를 둘 다** 쟀다.

| 방법 | 뱀부 전용 | 오르카 전용 | 양쪽 |
| --- | --- | --- | --- |
| 프로파일 차집합 (전 벤더) | 33 | 401 | 486 |
| 바이너리 문자열 (같은 키 집합) | 116 | 189 | 469 |

"오르카 프로파일 전용" 401 개 중 **107 개가 뱀부 바이너리에도 있다.** 대조군으로 넣은 가짜 키
`jackson_totally_fake_key` 는 양쪽 0 건이라 이 측정이 아무거나 잡는 게 아님도 확인했다.

### #1 — "뱀부 전용 7 개 중 5 개가 오르카에도 있다" → **감사가 틀렸다**

Codex 는 오르카 *프로파일* 등장 횟수(89 / 66 / 67 / 54 / 2 / 2 / 2)를 근거로 댔는데, 그건
감사 자신이 지적한 바로 그 오류다. **오르카 바이너리에는 이 문자열이 부분일치조차 0 건이다.**

```text
filament_scarf_seam_type              오르카 부분일치 0   뱀부 부분일치 1
filament_scarf_height                 오르카 부분일치 0   뱀부 부분일치 1
filament_scarf_gap                    오르카 부분일치 0   뱀부 부분일치 1
filament_scarf_length                 오르카 부분일치 0   뱀부 부분일치 1
override_filament_scarf_seam_setting  오르카 부분일치 0   뱀부 부분일치 1
seam_placement_away_from_overhangs    오르카 부분일치 0   뱀부 부분일치 1
seam_slope_gap                        오르카 부분일치 0   뱀부 부분일치 1
```

오르카 프로파일에 들어 있는 이유는 **오르카가 뱀부 벤더 프로파일을 통째로 실어 나르기 때문**이다.
해당 파일이 속한 벤더를 세어 확인했다 — `BBL` 46 · `OrcaFilamentLibrary` 11 · `Flashforge` 5 ·
`WonderMaker` 4, 그리고 `seam_slope_gap` 등은 `BBL/process/fdm_process_common.json` 과
거기서 갈라진 `Qidi/process/fdm_process_n_common.json` 2 곳뿐이다. 오르카는 읽는 순간 버린다.

따라서 원문 "뱀부 전용" 판정 자체는 **맞았고**, 다만 근거가 약했다. §11.3 을 "오르카 프로파일에
있어도 오르카는 모른다" 로 다시 쓰고 바이너리 · 프로파일 두 열을 나란히 넣었다.

### #2 — "`wall_sequence` 는 뱀부에 없다" → **감사가 맞다. 고쳤다**

```text
wall_sequence                    뱀부bin=True  뱀부prof=0  오르카prof=303
seam_slope_steps                 뱀부bin=True  뱀부prof=0  오르카prof=189
wall_distribution_count          뱀부bin=True  뱀부prof=0  오르카prof=237
wall_transition_length           뱀부bin=True  뱀부prof=0  오르카prof=235
wall_transition_angle            뱀부bin=True  뱀부prof=0  오르카prof=237
wall_transition_filter_deviation 뱀부bin=True  뱀부prof=0  오르카prof=235
reduce_infill_retraction         뱀부bin=True  뱀부prof=0  오르카prof=733
```

이 7 개를 §11.2(오르카 전용)에서 빼고 **§11.2a "양쪽 다 아는데 뱀부 프로파일에는 안 적힌 키"** 를
신설해 옮겼다. 감사가 짚지 않은 것도 하나 더 잡았다 — §11.2 의 `percise_outer_wall` 철자는
**어느 바이너리에도 없다.** 양쪽 바이너리에 있는 것은 `precise_outer_wall` 이고, 틀린 철자는
오르카가 싣는 Cubicon 벤더 프로파일 1 건에만 남은 옛 이름이다.

### #3 — 자기모순 → 해소

§11.2 에서 "뱀부에는 없다" 가 사라져 §8.4(:209-213) · §3(:62-64) 과 어긋나지 않는다.
§8.4 에 §11.1 로 가는 한 줄을 걸어 방법론이 한 곳에만 살게 했다. `wall_sequence` 가 나오는
6 곳(62 · 64 · 142 · 210 · 242 · 405)이 전부 "뱀부에서 쓸 수 있는 키" 로 일치한다.

### #4 — `scarf_joint_speed` 과장 → 고쳤다

`scarf_joint_speed` 가 오르카 전용인 것은 맞다 (뱀부bin=False · 오르카bin=True). 틀린 것은
그래서 "경사 자체를 못 쓴다" 는 결론이다. `seam-recipes.md` §6.5 표와
`bambu-fields-baseline.md` §11.3 양쪽을 **"경사 구간 속도를 따로 낮출 수 없다"** 로 고치고,
뱀부에 있는 `seam_slope_type` · `seam_slope_min_length` · `seam_slope_start_height` ·
`seam_slope_conditional` · `filament_scarf_*` 를 나열해 오해를 막았다.

### 부수 지적 (enum 표가 슬라이서별로 안 갈림) → 고쳤다

지적이 옳은지 먼저 쟀다. 표의 6 키 값 전부를 양쪽 바이너리에 대조한 결과 **갈리는 값은 하나뿐**
이었다 — `seam_position` 의 `aligned_back` (뱀부 0 · 오르카 1). 나머지(`topmost` · `solid` ·
`brim_ears` · `inner-outer-inner wall` 등)는 전부 양쪽에 있다.

그래서 표를 통째로 복제하지 않고 한 줄 분기만 더했다. 양방향으로 확인한 출력:

```text
seam_position=aligned_back · TARGET_SLICER=orca   → RESULT: PASS
seam_position=aligned_back · TARGET_SLICER=bambu  → FAIL … 허용: nearest, aligned, back, random
```

같은 파일이 슬라이서에 따라 갈린다 — 분기가 실제로 살아 있다는 증거다. 안 고쳤으면
**오르카 정상 산출물을 FAIL 로 잡는 오탐**이 남았을 것이다.

### 남은 것

- AR-03 원 측정문(`grep -c 'Orca'`)의 판별력 문제는 AM-01 그대로다. AM-01 의 실판정 3 종은
  이번 변경 후에도 충족한다 (`scarf_joint_speed` 2 · `outer_wall_line_width` 1 ·
  `seam_slope_conditional` 2).
- 이번 조치는 전부 문서·게이트 레이어다. 계약 «범위 경계» 대로 실물 출력 검증은 범위 밖이다.

---

## QA 평가 1 회차 (2026-09-14) — REJECT · 21/23. 그 뒤 조치

평가자가 AM-02 조치 7 건을 **직접 돌려 확인**했고 전부 주장대로 동작했다 (음성 대조 제거 대조,
`TARGET_SLICER` 양방향 분기, 바이너리·프로파일 이중 근거 30 키 전수 대조). 떨어진 것은 2 건이다.

### AR-03 실패 — `docs/bambu-kit/bambu-print-profile.html` 미반영 → 조치 완료

평가자 지적: `SKILL.md` 는 크게 바뀌었는데 파생 페이지는 손도 안 댔고, 151 줄에
**SK-01 이 지우라고 요구한 바로 그 배제 문장**이 공개 문서에 살아 있었다.

> "다른 프린터(X1/P1/A1)나 다른 슬라이서(OrcaSlicer/PrusaSlicer) 요청에는 트리거되지 않는다"

**이것이 AM-01 이 예고한 바로 그 사고다.** 원 측정문 `grep -c 'Orca' >= 1` 의 2 건이 **배제 문장
자체에서** 나왔다. 조건이 완전히 깨진 상태에서 조건의 측정이 통과했다 — 판별력 없는 측정문이
실제로 결함을 숨긴 실측 사례다.

조치 — 4 곳을 고치고 2 개 절을 새로 넣었다.

| 위치 | 전 | 후 |
| --- | --- | --- |
| 트리거 절 머리말 | "H2S + Bambu Studio 환경에 한정" | "슬라이서는 양쪽을 다룬다. Phase 1.95 가 확정" |
| 트리거함 목록 | — | "오르카 프로파일" 추가 |
| 트리거 안 함 목록 | "다른 슬라이서 언급 (… OrcaSlicer, PrusaSlicer)" | "PrusaSlicer — **OrcaSlicer 는 이제 트리거한다**" |
| Why H2S만 설명 | 슬라이서 언급 없음 | "슬라이서는 왜 둘인가" 단락 + §11 링크 추가 |
| Phase 카드 | Phase 1 → 2 | **Phase 1.95 카드 신설** (4 갈래 판정표 + 환경변수 전달) |
| 자기 검증 절 | — | **음성 대조 절 신설** (제거 대조 · 강등 설명) |

재측정: 배제 문구 0 건 · `Phase 1.95` 2 건 · `TARGET_SLICER` 2 건 · `음성 대조` 1 건 ·
`Orca` 2 → 3 건.

### DG-04 실패 — 스킬 미실행 → **사용자 확인 대기**

평가자 지적이 맞다. 봉인(2026-09-13 11:44) 이후 스킬 산출물이 0 건이고, `_target_slicer` 표식이
전 산출물에 0 건이다. 계약 «범위 경계» 는 **실물 출력**만 제외하므로 면제되지 않는다.

다만 **스킬 자신의 규칙이 사용자 입력을 요구한다.** Phase 1.95 판정표는 "둘 다 설치돼 있고
사용자 미지정 → **묻는다. 임의로 고르지 마라**" 이고, 뱀부·오르카가 둘 다 설치돼 있다. Phase 2 도
소재 후보를 내고 사용자 픽을 받는다. 슬라이서를 임의로 골라 돌리면 스킬의 첫 게이트를 스스로
위반하는 셈이라, 사용자에게 슬라이서 지정을 받고 나서 돌린다.

### 평가자가 곁다리로 찾은 것 2 건

1. **`mktemp` 버그 → 조치 완료.** 이번 세션이 SKILL.md 에 새로 쓴 음성 대조 절차의
   `mktemp /tmp/gate-XXXX.py` 가 macOS 에서 2 회차부터 죽는다 (macOS mktemp 은 `X` 가 맨 끝이어야
   치환한다). `mktemp -t gate` 로 고치고 **문서에 적힌 절차를 그대로 2 회 연속 실행**해 확인했다.
   "고쳤으면 다시 확인하라" 는 절차가 다시 못 돌던 상태였다.
2. **`scripts/detect-docs-drift.py` 에 bambu-kit 매핑 0 건 → 사용자 확인 대기.** AR-03 이 새어나간
   직접 원인이다. 다만 이 파일은 계약 AR-01 이 열거한 경로 밖의 공용 도구라, 조용히 손대지 않고
   올린다.

### 재검증 (AR-03 조치 후)

```text
python3 scripts/validate-plugin.py bambu-kit   → exit 0
node scripts/check-docs-a11y.js docs/bambu-kit/*.html → 7/7 PASS, exit 0
python3 scripts/check-docs-links.py            → 깨진 링크 0 · 페이지 176/등록 176, exit 0
```

---

## DG-04 조치 (2026-09-14) — 스킬 1 회 완주 · 양쪽 슬라이서

사용자가 «양쪽 다» 를 지정해 Phase 1.95 의 "둘 다 설치 · 미지정 → 묻는다" 분기가 해소됐다.

### 먼저 걸린 것 — Skill 도구는 레포가 아니라 설치본을 부른다

`bambu-kit:bambu-print-profile` 을 부르니 `~/.claude/plugins/cache/.../bambu-kit/0.9.0/` 의
**옛 SKILL.md** 가 로드됐다. 세션 시작 훅이 경고한 그대로다 (레포가 앞서는데 버전이 같아 갱신이
안 걸린다).

```text
              설치본  레포
TARGET_SLICER    0     15
Phase 1.95       0      4
"machine"        1      3
음성 대조         0      1
줄 수         1690   1838
```

DG-04 는 «**수정된** 스킬» 을 요구하므로 캐시본을 돌리면 엉뚱한 것을 검증하게 된다.
**레포 `SKILL.md` 를 정본으로 삼아** 그 안의 절차·스크립트를 그대로 뽑아 실행했다.

### 실행 경과

| 단계 | 결과 |
| --- | --- |
| 환경 검증 | 앱 `02.08.02.61` · 번들 `02.08.00.06` · 온전성 4 키 전부 범위 안 · `RESULT: PASS` exit 0 |
| Phase 1.0 메시 | build item 26 · 메시 18 개 파싱 |
| Phase 1.0 형상 클래스 | Side Container **thin** (루프 52/25/20 전부 <30mm, 최소 5.31mm) · Funnel **planar** (루프 2/2/2, 최소 91.72mm) |
| Phase 1.95 | 사용자 지정 — `bambu` · `orca` 양쪽 |
| Phase 2 | ABS (기존 케이스 승계) |
| Phase 3 | 클래스가 갈려 process 를 둘로 나눔 → 슬라이서당 process 2 · filament 1 = **총 6 개** |
| Phase 4.3 | 아래 |

```text
TARGET_SLICER=bambu → RESULT: PASS  exit=0
TARGET_SLICER=orca  → RESULT: PASS  exit=0
```

산출물: `/Users/jackson/Hub/60_3D Print/Settings/ams-2-pro-lattice-dry-pods/dogfood-2026-09-14/`
(`bambu/` `orca/` 각 process 2 · filament 1 · zip 2 · `notes.md`). `_target_slicer` 표식 6/6 기록.

### 이번 실행이 실제로 증명한 것

**직전 세션 산출물을 새 게이트에 넣으면 떨어진다.** 게이트가 장식이 아니라는 근거다.

```text
$ TARGET_SLICER=orca … "orca/AMS 2 Pro Dry Pods CONTAINER - ABS 0.12mm ORCA-SEAM-V2.json"
FAIL … outer_wall_speed 를 명시했는데 _geometry_class 가 없다
FAIL … 유량비 11.5x (gap_infill_speed) — 5x 초과. 인접 속도를 낮춰라
RESULT: FAIL   exit=1
```

새로 만든 것은 thin 에 속도 키를 안 넣고(부모 실효값 유지) planar 는 인접 속도까지 낮춰
최대 유량비를 2.86x 로 맞췄다.

### 이번 실행에서 새로 드러난 것 (조치 안 함 · 백로그)

1. **게이트 스코프 색인이 `profiles/BBL` 만 읽는다.** 그래서 이번 스프린트가 권장하기 시작한
   오르카 전용 키가 전부 `[미검증]` 으로 떨어진다 — `scarf_joint_speed` 는 오르카 전 벤더
   프로파일에 **187 건** 있는데 BBL 트리에는 **0 건**이다. `staggered_inner_seams` 251 ·
   `wipe_before_external_loop` 233 · `brim_type` 353 도 같다. 키가 틀린 게 아니라 **근거를 못 찾는
   것**이고, 판정 불가는 통과로 취급되므로 위반을 놓치는 쪽으로도 샌다.
2. **작은 루프에서 스카프 상·하한이 양립 불가다.** 게이트는 `길이/둘레 <= 15%` 와 `길이 >= 3mm` 를
   같이 요구하는데, 둘레 5.31mm 면 상한이 0.80mm 라 만족할 값이 없다. 이번엔 스카프를 꺼서
   넘겼고 그건 `seam-recipes.md` §6.5.3 결론과도 맞지만, **둘레 20mm 미만에서는 게이트가 사실상
   "스카프 금지" 로 동작한다**는 점이 문서 어디에도 안 적혀 있다.
3. **Skill 도구 = 설치본.** 킷을 고치고 도그푸드하려면 먼저 릴리스하거나, 이번처럼 레포 파일을
   정본으로 직접 실행해야 한다. 이 사실이 `bambu-kit` 문서에 없다.
