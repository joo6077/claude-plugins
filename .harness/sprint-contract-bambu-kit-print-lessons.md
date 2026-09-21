---
feature: "bambu-kit 출력 교훈 3종 — 벽 예산 · 출력 안 함 부품 · 값 섞임 방지"
slug: bambu-kit-print-lessons
created: "2026-09-19 12:55"
complexity: "복잡"
conditions: 24
status: done
owner_session: be3037df-1ee8-45db-aa79-f54d3cadb2fc
conditions_digest: sha256:47696418d0328fc4
locked_at: "2026-09-19 13:18"
---

## 배경

- 2026-09-19 H2 AMS Flipper(MakerWorld 1815860, ABS) 첫 출력이 2~3층에서 멈췄다. 사용자 보고: 모서리 · 둥근 경첩 구멍 둘레
  덩어리, 구멍 안 실. 원인 세 가지가 킷에 절차로 없었다. 사용자가 세 항목 모두 킷 반영을 선택했다.
  1. **벽 예산** — 형상 판정은 전부 `planar` 였는데 살이 벽 4겹(3.54 mm)보다 좁은 비율이 뒤쪽 브래킷 바닥 58.8 %,
     80° 브래킷 74.5 % 였다. `classic` 이 틈을 갭필 253 m 로 채웠다. `surface-recipes.md` §2.8 은 `thin` 에서만 계산했다.
  2. **출력 안 함 부품** — 제작자 3mf 에서 두 번째 축 부품이 `printable="0"` 이라 10 개 중 9 개만 출력됐다.
  3. **값 섞임** — 제작자 3mf 를 연 뒤 설정을 바꾸자 Studio 가 제작자 값 3 개(`bottom_shell_layers` 5 ·
     `outer_wall_acceleration` 4000 · `default_acceleration` 9000)를 옮겨 넣었다. 보낸 G-code 에서 확인.
- **공통 전제 (모든 조건에 적용):**
  `W` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/bambu-print-lessons` (브랜치 `feat/bambu-kit-print-lessons`) ·
  `S` = `$W/bambu-kit/skills/bambu-print-profile/SKILL.md` ·
  `SP` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/be3037df-1ee8-45db-aa79-f54d3cadb2fc/scratchpad/lessons` ·
  제작자 원본 = `~/Downloads/H2_simple_AMS_Flipper--ABS(3).3mf` (8,008,196 바이트) ·
  스크립트는 **`$S` 에서 원문 그대로 추출해 실행**한다. 추출 범위는 각 조건의 측정 절에 적은 첫 줄 문자열부터 다음 `PY` 줄 전까지다.
  저장소 스크립트는 `$W/scripts/` 안의 것을 `$W` 에서 실행한다(원래 폴더 스크립트 금지).
- 복잡도 4 축: 레이어 = 측정 스크립트 · 완료 검사 · 절차 문서 · 참고 문서 (예) / 공개 계약 = process JSON 에 새 `_` 키 2 개,
  완료 검사 판정 규칙 추가 (예) / 소비면 = 완료 검사가 새 키를 읽는다, 기존 시험 파일 11 개 (예) / 회귀 = 기존 시험 파일 판정이
  바뀔 수 있다 (예) → **복잡**. 생산 쪽(측정 스크립트가 키를 낸다)과 소비 쪽(완료 검사가 읽는다)을 SK-02 · SK-04 로 나눈다.
- 설정 리터럴 대조: `commands.analyze` = `bash -n scripts/release.sh` · `commands.test` = `bash scripts/release.sh 2>&1 || true` ·
  `diagnostics.ide_exclude` = `[]` · 카테고리 = `Skill/SK` · `Script/SC` · `Error/ER` · `Architecture/AR` · 안티패턴 선별
  `AP-01` · `AP-03`.

## GAP 분석

- Pre-Edit Audit (실제 Read 증거, 기준 `origin/main` baa1a38):
  - `$S:84-105` 3MF 추출 스크립트 — build item 을 세기만 하고 `printable` 을 보지 않는다 → SK-01
  - `$S:115-255` 형상 클래스 측정 — 루프 **둘레**만 잰다, 살 두께를 재지 않는다 → SK-02 · SK-03
  - `$S:1472-1478` 완료 검사의 형상 클래스 검사 — `wall_generator` 를 보는 규칙 0 개 → SK-04
  - `$S:1680-1690` 4.4 Verify — 가져오기 확인만 있고 보낸 값 대조가 없다 → SK-06 · SK-07
  - `$S:1298` notes 템플릿 `# 4.` — 3mf 를 열고 설정을 바꾸는 절차가 섞임 경로 → SK-08
  - `surface-recipes.md:140` §2.8 "형상 클래스(§2.7)가 `thin` 이면" — planar 를 제외하는 문구 → SK-08
- 다른 세션 브랜치 `feat/bambu-kit-orca-h2s-feedback`(미푸시 · QA 승인)이 같은 `$S` 와 `surface-recipes.md` 를 고쳤다.
  그쪽이 건드린 구간: 완료 검사의 META · 프린터 설정 블록, 음성 대조 표, 체크리스트 끝, `surface-recipes.md` §5.3.
  이 스프린트는 그 구간을 피한다 → AR-03 으로 병합 충돌 0 을 잰다.

## 범위 경계

- 실제 출력으로 효과를 재는 것은 범위 밖이다(사용자가 전체 판을 출력 중). 조건은 스크립트 실행 출력과 슬라이서 설정 기록으로만 판정한다.
- 버전 bump · 릴리스는 이 스프린트가 하지 않는다.
- 임계 10 % 는 추정이다. 결함이 난 실측 21.7~90 % 와 결함 없던 0 % 사이의 보수값이며 SKILL.md 에 추정으로 표시한다.
- 오라클 해소: SK-08 — 판정 대상이 절차 문서 문구라 서술 확인이 곧 산출물이다.
- 커버리지 해소: AR-01 — 경로 6 개는 기대 집합이고, 측정 명령 하나(`git diff --name-only`)가 바뀐 파일 전부를 한 번에 낸다.

## 회귀 게이트

- 봉인 전 독립 측정(구현과 별개인 `$SP/webwidth.py`, 루프 위 1 mm 간격 점 → 다른 루프 최단거리): 제작자 원본 바닥 0.1 mm 에서
  `rear_bracket` 58.8 % · `80angle_bracket` 74.5 % · `AMS2_bracket` 0.0 % (벽 4겹 · 선폭 0.42/0.45 · 예산 3.54 mm).
- 첫 출력에서 보낸 G-code 의 설정 구간 사본: `$SP/sent-first-print-head.gcode` (588 줄). v1 process JSON 사본: `$SP/v1-process.json`.
  둘을 대조하면 불일치가 정확히 3 개(`bottom_shell_layers` · `outer_wall_acceleration` · `default_acceleration`)다 — 직전 스프린트 실측.
- 기존 완료 검사 시험 파일 11 개: `filament-lattice-fanfix` · `filament-scope-process-key` · `process-bambu-only-key-in-orca` ·
  `process-class-unknown` · `process-machine-scope-key` · `process-pre-start-fan-time` · `process-scope-filament-key` ·
  `process-seam-slope-type-invalid` · `process-speed-without-class` · `process-thin-baseline` · `process-thin-speed-lowered`.

## Skill

- [ ] SK-01: Given 제작자 원본, When `$S` 의 3MF 추출 스크립트(첫 줄 `python3 - "<model.3mf>" <<'PY'` 중 처음 나오는 것)를 원문 그대로 추출해 실행하면, Then 출력에 `printable="0"` 부품을 알리는 줄이 1 개 있고 그 줄에 `axis_insert` 가 들어 있다. 같은 스크립트를 출력 안 함 부품이 없는 `/Users/jackson/Hub/60_3D Print/Settings/h2-simple-ams-flipper/v2/H2_AMS_Flipper_ABS_v2_2_main.3mf` 에 돌리면 그런 줄이 0 개다 [exact] (측정: 두 실행 출력에서 `axis_insert` 가 든 경고 줄 수 1 / 0. 음성 대조: 추출본에서 printable 보고 줄을 지우면 첫 실행도 0 이 되어 FAIL)
- [ ] SK-02: Given 제작자 원본, When `$S` 의 형상 클래스 측정 스크립트(첫 줄 `# bambu-kit geometry-class probe`)를 원문 그대로 추출해 `WALL_LOOPS=4 OUTER_LINE_WIDTH=0.42 INNER_LINE_WIDTH=0.45` 로 실행하면, Then 부품별 출력에 벽 예산 3.54 mm 와 바닥 높이의 부족 비율이 나오고 그 값이 회귀 게이트의 독립 측정과 ±5 %p 안이다 — `rear_bracket` 53.8~63.8 % · `80angle_bracket` 69.5~79.5 % · `AMS2_bracket` 0~5 %. 그리고 process JSON 에 옮겨 적을 `_wall_budget_short_share` 요약값이 0.5 이상으로 1 줄 나온다 [goal] (측정: JSON 줄 파싱. 음성 대조: 벽 수를 1 로 주면 예산이 0.84 mm 로 줄어 `rear_bracket` 비율이 크게 떨어져야 한다)
- [ ] SK-03: SK-02 의 스크립트를 `WALL_LOOPS` 없이 제작자 원본에 실행하면 출력의 `_geometry_class` 가 `origin/main` 판 같은 스크립트의 출력과 부품 10 개 모두 같고, 벽 예산 필드가 나오지 않는다 [exact] (측정: `git -C $W show origin/main:bambu-kit/skills/bambu-print-profile/SKILL.md` 에서 같은 방식으로 추출한 옛 스크립트 출력과 부품별 `_geometry_class` 비교 + 새 출력에 `wall_budget` 문자열 0 회)
- [ ] SK-04: Given 새 시험 파일 `$W/bambu-kit/evals/gate-fixtures/process-wall-budget-classic.json`, When `$S` 의 Phase 4.3 완료 검사(첫 줄 `TARGET_SLICER=`)를 원문 그대로 추출해 `TARGET_SLICER=bambu SKILL_DIR=$W/bambu-kit/skills/bambu-print-profile` 로 실행하면, Then FAIL 줄이 정확히 1 개이고 그 줄에 `벽 예산` 과 `arachne` 가 들어 있으며 exit 1 이다 [exact] (측정: FAIL 줄 수 + exit. 음성 대조: 추출본에서 그 FAIL 을 내는 `errs.append` 줄을 `pass` 로 바꾸면 `RESULT: PASS` · exit 0)
- [ ] SK-05: SK-04 의 시험 파일 사본 두 개로 같은 검사를 돌리면 — (a) `wall_generator` 만 `arachne` 로 바꾼 사본은 exit 0 · `벽 예산` FAIL 0 개, (b) `_wall_budget_short_share` 키만 지운 사본은 exit 0 이고 `_wall_budget_short_share` 가 든 `[미검증]` 줄이 1 개다 [exact, enumerated] (측정: 사본 2 개 실행 출력)
- [ ] SK-06: `$S` 의 4.4 절에 새로 들어간 **3mf 값 박기** 스크립트를 원문 그대로 추출해 제작자 원본 + `/Users/jackson/Hub/60_3D Print/Settings/h2-simple-ams-flipper/v2/process/H2 AMS Flipper - ABS 0.12mm HQ v2.json` + `/Users/jackson/Hub/60_3D Print/Settings/h2-simple-ams-flipper/v2/filament/H2 AMS Flipper - ABS retract 0.6.json` 로 실행해 만든 3mf 는, `Metadata/project_settings.config` 에서 두 JSON 의 모든 키(`_` 접두 · 메타 키 제외) 값 첫 원소가 JSON 과 같고 `print_settings_id` · `filament_settings_id` 가 두 JSON 의 `name` 이다 [exact, collective] (측정: python zipfile 로 비교, 불일치 0. 음성 대조: 만들어진 3mf 대신 제작자 원본을 대조하면 불일치가 1 개 이상)
- [ ] SK-07: `$S` 의 4.4 절에 새로 들어간 **보낸 G-code 대조** 스크립트를 원문 그대로 추출해 `$SP/sent-first-print-head.gcode` 와 `$SP/v1-process.json` 에 실행하면 불일치 키로 정확히 `bottom_shell_layers` · `outer_wall_acceleration` · `default_acceleration` 3 개를 낸다 [exact, enumerated] (측정: 추출본을 `$SP/sent-first-print-head.gcode` · `$SP/v1-process.json` 로 실행한 출력의 불일치 키 집합 == 위 3 개. 음성 대조: 같은 G-code 에 `$SP/v1-process.json` 의 세 값을 G-code 값(5 · 4000 · 9000)으로 바꾼 사본을 대조하면 불일치 0 개)
- [ ] SK-08: 문서 반영 — (a) `$S` 의 notes 템플릿 `# 4.` 블록(측정 범위: `awk '/^# 4\. 임포트/{s=1;next} /^# 5\./{s=0} s' $S`)에 "설정을 바꾸지 않는다" 와 "보낸 G-code" 가 각각 1 회 이상, (b) `$S` 의 `## Gotcha 체크리스트` 섹션에 `printable` · `벽 예산` · `보낸 G-code` 가 각각 1 회 이상, (c) `$W/bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` §2.8(측정 범위: `awk '/^### 2\.8\./{s=1;next} /^## 3\./{s=0} s'`)에 `planar` 실측 사례 줄과 `WALL_LOOPS` 가 각각 1 회 이상 [structural, enumerated] (측정: 각 범위에 `grep -c`)

## Script

- [ ] SC-00: N/A (이 스프린트는 `scripts/release.sh` · 버전 bump · marketplace.json 을 건드리지 않는다)

## Error

- [ ] ER-01: SK-04 시험 파일 사본에서 `_wall_budget_short_share` 를 숫자가 아닌 `"abc"` 로 바꿔 완료 검사를 돌리면 파이썬 오류 추적(`Traceback`)이 0 줄이고 `[미검증]` 또는 FAIL 줄로 보고된다 [exact] (측정: 출력에 `Traceback` 0 회)
- [ ] ER-02: SK-02 스크립트를 `WALL_LOOPS=0` 으로, 또 `WALL_LOOPS=x` 로 실행하면 두 경우 모두 `Traceback` 0 줄이고 `FAIL:` 로 시작하는 안내 줄 1 개와 0 이 아닌 exit 로 끝난다 [exact, enumerated] (측정: 두 실행의 출력 + exit)
- [ ] ER-03: 기존 시험 파일 11 개(회귀 게이트 목록)를 `origin/main` 판 완료 검사와 이 브랜치 판 완료 검사로 각각 돌리면 파일마다 FAIL 줄 집합과 exit 가 같다. 대상 슬라이서는 `process-bambu-only-key-in-orca` 만 `orca`, 나머지는 `bambu` [exact, enumerated] (측정: 두 판 추출본을 11 개에 실행해 FAIL 줄 집합 비교. `[미검증]` 줄 차이는 허용 — 새 키 미기록 보고가 늘어나는 것은 의도다)

## Architecture

- [ ] AR-01: Given 이 스프린트 커밋 완료, 브랜치 끝 `feat/bambu-kit-print-lessons` 기준 `git -C $W diff --name-only origin/main...feat/bambu-kit-print-lessons` 의 결과가 다음 집합에 포함된다 — `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` · `bambu-kit/evals/gate-fixtures/process-wall-budget-classic.json` · `.harness/sprint-contract-bambu-kit-print-lessons.md` · `.harness/sprint-feedback-bambu-kit-print-lessons.md` · `.harness/sprint-amendments-bambu-kit-print-lessons.md` [exact, enumerated] (측정: 위 명령. 상한 ref 는 브랜치 이름으로 고정, `HEAD` 금지)
- [ ] AR-02: `$W` 에서 CI 검사 10 개가 전부 exit 0 이다 — `python3 scripts/validate-plugin.py` · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/sync-docs.py --check-only` · `python3 scripts/sync-orchestrator.py --check-only` · `python3 scripts/run-evals.py --verbose` · `python3 scripts/check-contrast-claims.py` · `python3 scripts/check-docs-links.py` · `python3 scripts/check-stale-values.py` · `bash harness/evals/kaizen/feedback-system/save-test.sh` · `node scripts/check-docs-a11y.js` [exact, enumerated] (측정: `.github/workflows/*.yml` 의 `run:` 줄에서 추출한 목록. `npx playwright test design-kit/evals/visuals.spec.js` 는 design-kit 을 건드리지 않아 CI 에 맡긴다)
- [ ] AR-03: 다른 세션 브랜치와 병합 충돌이 없다 — `git -C $W merge-tree --write-tree feat/bambu-kit-orca-h2s-feedback feat/bambu-kit-print-lessons` 가 exit 0 이다 [exact] (측정: 위 명령 exit. exit 1 이면 충돌)
- [ ] AR-04: 새 시험 파일 `process-wall-budget-classic.json` 이 기존 시험 파일과 같은 폴더(`$W/bambu-kit/evals/gate-fixtures/`)에 있고, 벽 예산 외의 위반이 0 개다 [exact] (측정: SK-04 실행에서 FAIL 이 정확히 1 개인 것으로 판정 — 벽 예산 줄 외 FAIL 0)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다 (이 스프린트는 `bambu-kit/.claude-plugin/plugin.json` 을 바꾸지 않는다. 측정: AR-01 목록에 그 파일 없음)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `$W` 에서 `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` exit 0)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: bash -n scripts/release.sh 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외)
- [ ] DG-03: bash scripts/release.sh 2>&1 || true 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
