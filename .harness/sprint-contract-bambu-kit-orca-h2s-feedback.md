---
feature: "bambu-kit 에 2026-09-19 fly-catcher 오르카·H2S 피드백 반영"
slug: bambu-kit-orca-h2s-feedback
created: "2026-09-19 09:40"
complexity: "복잡"
conditions: 31
status: active
owner_session: bcf7a121-42d2-47cf-a372-a4e8cb48fbe5
conditions_digest: sha256:3888c2d2c799092a
locked_at: "2026-09-19 10:16"
---

## 배경

2026-09-19 fly-catcher (PLA Basic · OrcaSlicer 2.4.2 · H2S) 세션에서 사용자 피드백 8 건이 나왔고, 조사 4 건과
G-code 실측으로 원인이 확인됐다. 킷에는 그중 어느 것도 반영돼 있지 않다.

1. 오르카로 자른 파일만 툴헤드 카메라 초기화 실패(`0500-8092`). 오르카 2.4.2 의 H2S 시작 명령은 2025/08/06 판,
   뱀부는 2026/04/21 판이다. 뱀부 커밋 `50bb6ab`("툴헤드 카메라 초기화 실패 방지")가 넣은 준비 블록
   (`M104 S0 T0` · `M562 P1 E0 B1` · `M18 E` · `M1028 S1` … `M1028 S0`)이 오르카에는 없다 (오르카 이슈 #14947 열림).
   뱀부 최신 시작 명령을 넣은 오르카 프린터 설정으로 다시 잘라 실행 줄에 준비 블록이 들어간 것을 확인했다.
2. 오르카에서 H2S 로 직접 보낼 수 없다 (뱀부 권한 제어). 킷은 슬라이서를 "설치됐나" 로만 판별한다.
3. 판에서 바로 시작하는 바닥 필렛 → 2층 벽이 1층 바깥 공중에 놓이고 그 자리의 테두리와 붙는다. 테두리를 떼면
   필렛 시작선을 따라 솟은 선이 남고 레일 직각 모서리에서 더 크다 (사용자 사진). 2층이 테두리 위에 얹힌 폭:
   8월 형상 0.38mm(모서리 0.44mm) · 사용자 3h6m 출력 0.21mm(0.22mm). 오르카 `make_overhang_printable` 을
   바닥 0~3mm 높이 구간에만 켜면 해결되고, 전체에 켜면 가로 M4 구멍 윗부분이 막힌다(폭 4.1→0.1mm).
4. `xy_hole_compensation` 은 층별 닫힌 안쪽 윤곽(`_shrink_contour_holes`)에만 걸린다 — 가로 구멍 폭 변화 0,
   컵 안쪽 벽만 0.24mm 커진다.
5. 다림질 줄·돌기: 면적당 재료는 `층 높이 × 흐름`이고 간격은 상쇄된다 (두 슬라이서 `Fill.cpp`). 세션에서
   "흐름÷간격" 으로 잘못 계산했다. `top_surface_acceleration` 은 다림질 경로에 안 걸린다. 오르카
   `ironing_pattern: rectilinear` 를 뱀부가 `zig-zag` 로 바꿔 읽는다 (사용자 캡처).
6. `seam-recipes.md` §6.5.4 "기본값이 `1`" 은 뱀부(`PrintConfig.cpp` 기본 true)만 맞고 오르카는 false 다.
   안팎이 모두 보이는 컵에서 `aligned_back` 은 안쪽 심 580 개를 컵 안 정면에 놓았다.
7. 오르카가 저장한 3mf 를 더블클릭하면 뱀부가 열고 오르카 전용 설정을 버린다. GUI 에서 프로젝트를 다시
   저장하면 3mf 안 프린터가 바뀌어 카메라 수정이 빠진 채 돌아온 것을 실측했다. 설정 전환 창(Transfer)을
   사용자가 물었다.
8. Phase 4.3 검사가 `type: machine` 파일을 FAIL 시킨다 (`type='machine' (process|filament 아님)` ·
   `filament_settings_id 누락` 2 건, 2026-09-19 실측) — 오르카 프린터 설정을 검사할 수 없다.

## 리서치 소스

- Codex 조사 4 회 (gpt-5.6-sol · 조회 전용) — r1 바닥 필렛·테두리 · r2 가로 구멍 치수 · r3 오르카/뱀부 H2S 기계
  명령 · r4 다림질 줄·돌기. 원문은 근거 문서 `.harness/.meta/evidence/bambu-orca-h2s-feedback.md` 에 옮긴다
- 오르카 `v2.4.2` 소스 직접 조회 — `PrintObjectSlice.cpp`(`apply_conical_overhang`) · `PrintConfig.cpp`
  (`seam_slope_conditional` 기본 false) · `OrcaSlicer.cpp`(명령줄) · `bbs_3mf.cpp`(`layer_config_ranges.xml`)
- 뱀부 `v02.08.02.61` `PrintConfig.cpp` — `seam_slope_conditional` 기본 true
- 오르카 2.4.2 명령줄 슬라이스 실측 — 기준 · 전체 45° · 0~3mm 구간 · 최종본 · 사용자 3h6m 파일

## GAP 분석

| 대상 | 현재 | 갭 |
| --- | --- | --- |
| `SKILL.md` Phase 1.95 (697–737) | 설치 여부 · 사용자 지정으로만 판별 | 전송 가능 여부를 안 본다 |
| `SKILL.md` Phase 3 · 4.1 (1205) | process · filament 만 만든다 | 오르카 H2 계열 프린터 설정이 없다 |
| `SKILL.md` Phase 4.3 (1432) | `type` 이 process · filament 가 아니면 FAIL | machine 파일 검사 불가 |
| `SKILL.md` Phase 4.4 (1680–1690) | 뱀부 경로만 안내 | 오르카 열기 · Transfer · 전송 안내 없음 |
| `references/bambu-fields-baseline.md` §11 (351–491) | 키 차이만 다룬다 | 기계 명령 판 차이 없음 |
| `references/tolerance.md` §3.2 (112–128) | 보정값 계산만 | 구멍 축 판정 · 가로 구멍 무효 · ISO 273 없음 |
| `references/failure-recipes.md` §3.1 (172–185) | "brim 우선" | 바닥 필렛 + 테두리 융착 예외 없음 |
| `references/surface-recipes.md` §5 (244–272) | 소재별 값 표만 | 솟은 선 / 홈 구분 · 재료량 식 없음 |
| `references/seam-recipes.md` §6.5.4 (302–312) | "기본값이 `1`" | 슬라이서별 기본값 아님 · 컵 사례 없음 |
| `docs/bambu-kit/bambu-print-profile.html` | "시험용 파일 4 종" | 새 시험 파일이 생기면 어긋난다 |

## 범위 경계

측정 공통 준비 (모든 조건이 이 정의를 쓴다. 워크트리 루트에서 zsh · bash 동일):

```bash
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/bambu-orca-h2s-feedback
S=bambu-kit/skills/bambu-print-profile/SKILL.md
R=bambu-kit/skills/bambu-print-profile/references
FX=bambu-kit/evals/gate-fixtures
export SKILL_DIR=bambu-kit/skills/bambu-print-profile
cut_sec() { awk -v a="$2" -v b="$3" 'index($0,a)==1{f=1;print;next} f&&index($0,b)==1{exit} f' "$1"; }
extract_gate() { A=$(grep -n '^TARGET_SLICER=.* python3 - ' "$1" | head -1 | cut -d: -f1)
  B=$(awk -v s="$A" 'NR>s && $0=="PY" {print NR; exit}' "$1"); sed -n "$((A+1)),$((B-1))p" "$1"; }
GATE=$(mktemp -t gate); extract_gate "$S" > "$GATE"
OLDMD=$(mktemp -t oldskill); git show baa1a38:"$S" > "$OLDMD"; OLD=$(mktemp -t oldgate); extract_gate "$OLDMD" > "$OLD"
sprint_head() { m=$(git log --merges --format=%H --grep="from joo6077/feat/bambu-kit-orca-h2s-feedback" -1)
  [ -n "$m" ] && { echo "$m"; return 0; }
  git rev-parse --verify -q "feat/bambu-kit-orca-h2s-feedback" && return 0
  echo "UNRESOLVED feat/bambu-kit-orca-h2s-feedback" >&2; return 1; }
```

- 기준 커밋은 `baa1a38` (bambu-kit v0.9.2 머지, 계약 작성 시점 `origin/main`). 변경 범위 기준값: 작성 시점
  `git diff --name-only baa1a38..$(sprint_head)` 0 줄
- 넣지 않는 것: 뱀부 끝·필라멘트 교체·층 변경·타임랩스·감김 감지 명령의 오르카 이식(필라멘트 교체 명령에 오르카가
  모르는 변수가 있다), 오르카 대상 환경 검사 스크립트, 5 단계 시험 출력 규정 변경, 버전 올림·릴리스
- 오르카 화면(GUI)에서 3mf 를 열어 높이 구간이 보이는지는 직접 확인할 수 없다. 명령줄 슬라이스가 같은 3mf
  읽기 코드를 쓴다는 것까지만 근거로 삼는다
- 노드 의존성(`node_modules`)이 이 작업 폴더에 없어 문서 접근성 검사(`node scripts/check-docs-a11y.js`)는
  `npm ci` 후 실행한다. 설치가 안 되면 `[미검증]` 1 건까지 받는다

- 커버리지 해소: SK-02 — 측정 절이 `machine/` 과 `§11.5` 를 각각 `grep -cF` 로 센다고 적었다 (백틱 안에 공백이 있어 검출기가 못 읽음)
- 커버리지 해소: SC-05 — 측정이 산문에 나열한 11 파일을 `$FX/$f` 로 하나씩 순회한다
- 커버리지 해소: ER-03 · AR-01 · AR-02 · AR-03 · AR-04 · AR-07 — 측정 절의 `'<토큰>'` 자리에 산문 토큰을 하나씩 넣어 센다. 파일명 토큰은 측정 명령의 `$R/<파일>` 인자로 들어 있다
- 커버리지 해소: AR-09 — 측정이 "17 경로 중 하나" 로 산문 목록 전체를 기준 집합으로 쓴다

## 회귀 게이트

- 기존 시험 파일 11 개의 판정(작성 시점 실측): bambu 기준 FAIL 0 = `filament-lattice-fanfix` ·
  `process-bambu-only-key-in-orca` · `process-thin-baseline`, 나머지 8 개 FAIL 1. orca 기준은
  `process-bambu-only-key-in-orca` 만 FAIL 1 로 바뀌고 나머지는 같다
- 작성 시점 로컬 CI 파이썬·셸 12 단계 전부 exit 0 (validate-plugin · sync-evals · sync-docs · sync-orchestrator ·
  run-evals · check-contrast-claims · check-docs-links · check-stale-values · code-fence · `bash -n` ·
  save-test · aggregation-test)

## Skill

- [ ] SK-01: Given H2S 에 오르카로 뽑으려는 사용자, When Phase 1.95 를 따르면, Then 직접 출력이 막힌다는 사실과 우회 경로를 안내받는다 — Phase 1.95 구간에 `권한 제어` · `Export plate sliced file` · `다시 슬라이스` · `Bambu Connect` · `USB` · `Developer Mode` 6 토큰이 모두 있다 [exact, enumerated] (측정: `cut_sec "$S" "### Phase 1.95" "### Phase 2" | grep -cF '<토큰>'` 을 토큰마다 실행해 전부 1 이상)
- [ ] SK-02: Given 오르카 대상 + H2 계열 프린터, When Phase 3 을 따르면, Then 뱀부 최신 시작 명령을 담은 프린터(machine) 설정을 함께 만든다고 적혀 있다 — Phase 3 구간에 `machine/` 과 `§11.5` 둘 다 있다 [exact, enumerated] (측정: `cut_sec "$S" "### Phase 3" "### Phase 4" | grep -cF 'machine/'` 과 `… | grep -cF '§11.5'` 둘 다 1 이상)
- [ ] SK-03: Phase 4.1 번들 구조 예시에 `machine/` 폴더가 있다 [exact] (측정: `cut_sec "$S" "#### 4.1" "#### 4.2" | grep -cF 'machine/'` 1 이상)
- [ ] SK-04: Given 오르카 사용자, When Phase 4.4 를 따르면, Then 오르카 안에서 프로젝트를 열고 설정 전환 창에서 무엇을 누를지 안내받는다 — Phase 4.4 구간에 `더블클릭` · `Transfer` · `프로젝트 열기` · `BS start` 4 토큰이 모두 있다 [exact, enumerated] (측정: `cut_sec "$S" "#### 4.4" "### Phase 5" | grep -cF '<토큰>'` 전부 1 이상)
- [ ] SK-05: Gotcha 체크리스트에 이번 피드백 항목이 들어갔다 — `M1028` · `brim_ears` · `가로 구멍` · `다림질` 4 토큰이 모두 있다 [exact, enumerated] (측정: `cut_sec "$S" "## Gotcha 체크리스트" "## MakerWorld" | grep -cF '<토큰>'` 전부 1 이상)

## Script

- [ ] SC-01: Given 준비 블록이 든 오르카 H2S 프린터 설정 `$FX/machine-orca-h2s-bs-start.json`, When 새 검사를 `TARGET_SLICER=orca` 로 돌리면, Then 마지막 줄 `RESULT: PASS` · exit 0 · `[미검증]` 줄 0 이다 [exact] (측정: `TARGET_SLICER=orca python3 "$GATE" "$FX/machine-orca-h2s-bs-start.json"; echo $?` · 음성 대조: 검사 사본에서 종류 허용 조건을 process · filament 둘만 받도록 되돌리면 같은 파일이 FAIL · exit 1)
- [ ] SC-02: Given 오르카 번들 시작 명령 그대로인 H2S 프린터 설정 `$FX/machine-orca-h2s-no-camera-prep.json`, When 새 검사를 `TARGET_SLICER=orca` 로 돌리면, Then FAIL 줄이 정확히 1 개이고 그 줄에 `M1028` 이 있으며 exit 1 이다 [exact] (측정: `… | grep -c '^FAIL'` == 1, `… | grep '^FAIL' | grep -cF 'M1028'` == 1 · 음성 대조: 그 판정의 `errs.append` 줄만 `pass` 로 바꾼 사본(바뀐 줄 1 개 확인)에서 `RESULT: PASS` · exit 0)
- [ ] SC-03: Given 시작 명령에 `cooling_filter_enabled` 가 남은 오르카 H2S 프린터 설정 `$FX/machine-orca-h2s-cooling-filter-var.json`, When 새 검사를 `TARGET_SLICER=orca` 로 돌리면, Then FAIL 줄이 정확히 1 개이고 그 줄에 `cooling_filter_enabled` 가 있으며 exit 1 이다 [exact] (측정: SC-02 와 같은 형태 · 음성 대조: 그 판정의 `errs.append` 줄만 `pass` 로 바꾼 사본에서 PASS · exit 0)
- [ ] SC-04: Given H2 계열이 아닌 오르카 프린터 설정 `$FX/machine-orca-x1c.json`(상속 `Bambu Lab X1 Carbon 0.4 nozzle`, 시작 명령에 `M1028` 없음), When 새 검사를 `TARGET_SLICER=orca` 로 돌리면, Then `M1028` 이 든 FAIL 줄이 0 이다 [exact] (측정: `… | grep '^FAIL' | grep -cF 'M1028'` == 0)
- [ ] SC-05: 기존 시험 파일 11 개를 `TARGET_SLICER` bambu · orca 로 각각 돌린 22 실행의 출력과 종료 코드가 옛 검사(`baa1a38` 의 SKILL.md 에서 뽑은 `$OLD`)와 같다 [exact, enumerated] — 대상 `filament-lattice-fanfix.json` · `filament-scope-process-key.json` · `process-bambu-only-key-in-orca.json` · `process-class-unknown.json` · `process-machine-scope-key.json` · `process-pre-start-fan-time.json` · `process-scope-filament-key.json` · `process-seam-slope-type-invalid.json` · `process-speed-without-class.json` · `process-thin-baseline.json` · `process-thin-speed-lowered.json` (측정: 파일마다 `diff <(TARGET_SLICER=$sl python3 "$OLD" "$FX/$f" 2>&1; echo "exit=$?") <(TARGET_SLICER=$sl python3 "$GATE" "$FX/$f" 2>&1; echo "exit=$?")` 22 회 모두 차이 0 줄)
- [ ] SC-06: 사용자 실제 산출물 2 개가 새 검사에서 `RESULT: PASS` · exit 0 이다 — `/Users/jackson/Hub/60_3D Print/Settings/fly-catcher/orca/process/fly-catcher - PLA Basic 0.12mm ORCA.json` · `/Users/jackson/Hub/60_3D Print/Settings/fly-catcher/orca/machine/Bambu Lab H2S 0.4 nozzle - BS start 2026-04.json` [exact, enumerated] (측정: 두 파일을 한 번에 `TARGET_SLICER=orca python3 "$GATE" …` · 기준값: 옛 검사는 machine 파일에 FAIL 2 건)

## Error

- [ ] ER-01: machine 시험 파일을 `TARGET_SLICER` 없이 돌리면 조용히 넘어가지 않고 `[미검증]` 줄이 1 개 이상 나온다 [exact] (측정: `env -u TARGET_SLICER python3 "$GATE" "$FX/machine-orca-h2s-bs-start.json" | grep -c '^\[미검증\]'` 1 이상)
- [ ] ER-02: `printer_settings_id` 를 뺀 machine 파일은 FAIL 이고 그 줄에 `printer_settings_id` 가 있다 [exact] (측정: `$FX/machine-orca-h2s-bs-start.json` 에서 그 키만 지운 임시 사본을 `TARGET_SLICER=orca` 로 돌려 `grep '^FAIL' | grep -cF 'printer_settings_id'` 1 이상 · exit 1)
- [ ] ER-03: 바닥 필렛 절에 `make_overhang_printable` 을 모델 전체에 켜면 가로 구멍이 막힌다는 경고가 실측값과 함께 있다 — `가로 구멍` · `4.1` · `0.1` 3 토큰 [exact, enumerated] (측정: `cut_sec "$R/failure-recipes.md" "### 3.5" "## 4." | grep -cF '<토큰>'` 전부 1 이상)

## Architecture

- [ ] AR-01: `bambu-fields-baseline.md` 에 `### 11.5` 절이 있고 `2025/08/06` · `2026/04/21` · `M104 S0 T0` · `M562 P1 E0 B1` · `M18 E` · `M1028 S1` · `M1028 S0` · `50bb6ab` · `#14947` · `cooling_filter_enabled` 10 토큰이 그 절 안에 있다 [exact, enumerated] (측정: `cut_sec "$R/bambu-fields-baseline.md" "### 11.5" "## " | grep -cF '<토큰>'` 전부 1 이상)
- [ ] AR-02: `tolerance.md` 에 `## 1.3` 구멍 축 절이 있고 `_shrink_contour_holes` · `가로 구멍` · `ISO 273` · `4.3` · `4.5` · `4.8` · `눈물방울` · `#7744` 8 토큰이 그 절 안에 있으며, §3.2 에 `§1.3` 이 있다 [exact, enumerated] (측정: `cut_sec "$R/tolerance.md" "## 1.3" "## 2." | grep -cF '<토큰>'` 전부 1 이상 · `cut_sec "$R/tolerance.md" "### 3.2" "### 3.3" | grep -cF '§1.3'` 1 이상)
- [ ] AR-03: `failure-recipes.md` 에 `### 3.5` 바닥 필렛 절이 있고 `0.38` · `0.44` · `layer_config_ranges.xml` · `make_overhang_printable` · `brim_ears` · `Brim.cpp` · `bambu-02.08.02.61.tsv` 7 토큰이 그 절 안에 있으며, §3.1 에 `§3.5` 가 있다 [exact, enumerated] (측정: `cut_sec "$R/failure-recipes.md" "### 3.5" "## 4." | grep -cF '<토큰>'` 전부 1 이상 · `cut_sec "$R/failure-recipes.md" "### 3.1" "### 3.2" | grep -cF '§3.5'` 1 이상)
- [ ] AR-04: `surface-recipes.md` 에 `### 5.3` 다림질 진단 절이 있고 `층 높이 × 흐름` · `솟은` · `홈` · `top_surface_acceleration` · `zig-zag` · `rectilinear` · `Fill.cpp` 7 토큰이 그 절 안에 있다 [exact, enumerated] (측정: `cut_sec "$R/surface-recipes.md" "### 5.3" "## 6." | grep -cF '<토큰>'` 전부 1 이상)
- [ ] AR-05: `seam-recipes.md` 에 "기본값이 `1` 이므로" 단일 서술이 남지 않고, §6.5.4 절이 뱀부 `true` · 오르카 `false` 를 `PrintConfig.cpp` 근거와 함께 적는다 [exact] (측정: `grep -cF '기본값이 \`1\` 이므로' "$R/seam-recipes.md"` == 0 (기준값 1) · `cut_sec "$R/seam-recipes.md" "### 6.5.4" "### 6.5.5"` 에서 `true` · `false` · `PrintConfig.cpp` 각각 1 이상)
- [ ] AR-06: `seam-recipes.md` 에 `## 6.6` 컵 사례 절이 있고 `485` · `466` · `580` · `aligned_back` · `back` 5 토큰이 그 절 안에 있다 [exact, enumerated] (측정: `cut_sec "$R/seam-recipes.md" "## 6.6" "## 7." | grep -cF '<토큰>'` 전부 1 이상)
- [ ] AR-07: 근거 문서 `.harness/.meta/evidence/bambu-orca-h2s-feedback.md` 가 있고 `50bb6ab` · `_shrink_contour_holes` · `Brim.cpp` · `Fill.cpp` · `0.21` 5 토큰을 담는다 [exact, enumerated] (측정: 파일마다 `grep -cF '<토큰>'` 전부 1 이상)
- [ ] AR-08: 문서 페이지 `docs/bambu-kit/bambu-print-profile.html` 의 음성 대조 설명이 새 시험 파일을 반영한다 — `시험용 파일 4 종` 0 건, `카메라 준비` 1 건 이상 [exact] (측정: `grep -cF '시험용 파일 4 종'` == 0 (기준값 1) · `grep -cF '카메라 준비'` 1 이상)
- [ ] AR-09: Given 이 스프린트의 커밋이 끝난 뒤, 변경 파일이 아래 목록 안에만 있다 [exact, enumerated] — `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` · `bambu-kit/skills/bambu-print-profile/references/tolerance.md` · `bambu-kit/skills/bambu-print-profile/references/failure-recipes.md` · `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` · `bambu-kit/skills/bambu-print-profile/references/seam-recipes.md` · `bambu-kit/evals/gate-fixtures/machine-orca-h2s-bs-start.json` · `bambu-kit/evals/gate-fixtures/machine-orca-h2s-no-camera-prep.json` · `bambu-kit/evals/gate-fixtures/machine-orca-h2s-cooling-filter-var.json` · `bambu-kit/evals/gate-fixtures/machine-orca-x1c.json` · `bambu-kit/README.md` · `docs/bambu-kit/bambu-print-profile.html` · `.harness/.meta/evidence/bambu-orca-h2s-feedback.md` · `.harness/sprint-contract-bambu-kit-orca-h2s-feedback.md` · `.harness/sprint-feedback-bambu-kit-orca-h2s-feedback.md` · `.harness/sprint-amendments-bambu-kit-orca-h2s-feedback.md` · `.harness/feedback-draft.yaml` (측정: `git diff --name-only baa1a38..$(sprint_head) -- .` 의 각 줄이 17 경로 중 하나 · 포함 관계 · 생성물 없음 · 기준값 0 줄)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` exit 0)
- [ ] AP-04: SKILL.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py bambu-kit` exit 0)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 새 machine 판정이 기존 옵션 목록(`references/option-keys/`)의 종류 줄을 그대로 쓴다 (측정: 새 검사 본문에서 `grep -cF 'references/option-keys'` == 1, 기준값 1)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 기계 명령 설명을 새 참조 파일이 아니라 기존 `bambu-fields-baseline.md` §11 에 넣었다 (측정: `find "$R" -maxdepth 1 -type f -name '*.md' | wc -l` == 9, 기준값 9)

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상) (측정: exit 0 · 출력 0 줄)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 목록 `[]`) — 변경 마크다운·JSON 파일에 새 경고 0 (기본: VS Code 문제 패널 · 대체: 없음 → `[미검증]` 1 건까지 허용)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개 (측정: 출력에서 `grep -cE 'Traceback|Error'` == 0)
- [ ] DG-04: 실제 구동 시 에러 0개 — 로컬 CI 12 단계(`python3 scripts/validate-plugin.py` · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/sync-docs.py --check-only` · `python3 scripts/sync-orchestrator.py --check-only` · `python3 scripts/run-evals.py --verbose` · `python3 scripts/check-contrast-claims.py` · `python3 scripts/check-docs-links.py` · `python3 scripts/check-stale-values.py` · `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` · `bash -n scripts/release.sh` · `bash harness/evals/kaizen/feedback-system/save-test.sh` · `bash harness/evals/kaizen/feedback-system/aggregation-test.sh`) 전부 exit 0, 그리고 `npm ci` 뒤 `node scripts/check-docs-a11y.js` exit 0 (노드 설치 불가 시 이 한 단계만 `[미검증]`)
