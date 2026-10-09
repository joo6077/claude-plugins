---
feature: "flutter-scenario-report — 조작 칸을 화면 폭 통째로 · 넓은 화면 108px · 오른쪽 큰 화면(마우스 올리기)"
slug: scenario-report-op-follow
created: "2026-10-09 11:26"
complexity: "중간"
conditions: 17
status: done
owner_session: 97f28e34-99ea-4a74-9baa-3288b7964458
conditions_digest: sha256:f7d8e8f769383b87
measurement_digest: sha256:e6ac9f143e2ebfa7
locked_at: "2026-10-09 11:29"
---

## 배경

- 앞 계약 `scenario-report-op-roi`(APPROVE, 커밋 `676301f3`)가 조작 칸 72px 에 누를 곳 주변만 잘라 넣었다. 사용자 평가(2026-10-08 ~ 10-09 대화): 확대 창은 별로, 작은 칸도 별로, 확대해서 자르면 어떤 화면인지 헷갈린다
- 시안을 거쳐 사용자가 고른 것(2026-10-09 "ㅇㅋ 이걸로 진행해", 시안 세션 임시 폴더 `roi/mock/TC-003/mock-e.html` · `roi/mock/multi/TC-009-multi/mock-e.html`):
  - 결정 1: 잘라 보기는 화면 폭을 통째로 두고 위아래만 누를 곳 주변으로 자른다
  - 결정 2: 넓은 화면(폭 901px 이상)에서 칸을 1.5 배인 108px 로 그린다. 폰 폭은 72px 그대로
  - 결정 3: 폭 1100px 이상에서 조작 사진이 있는 시나리오마다 단계 목록 오른쪽에 큰 화면 하나를 붙인다. 조작 칸에 마우스를 올리거나 키보드 초점을 옮기면 그 조작으로 바뀐다. 스크롤로는 바뀌지 않는다(사용자: "스크롤보다 호버가 나을거 같앙"). 처음에는 그 시나리오의 첫 조작을 보여 준다
  - 칸을 누르면 뜨는 확대 창은 그대로 둔다 — 폰 폭에는 큰 화면이 없어 크게 볼 수단이 그것뿐이다

## GAP 분석

- 잘라 보기 계산이 화면을 폭 200px 로 줄여 가로세로 모두 자른다 (`build_report.py:46` `OP_THUMB_SCREEN = 200`, `:216-217`)
- 틀의 `.op-thumb img` 폭이 200px 이다 (`templates/report.html:78`)
- 넓은 화면 칸 크기 규칙 · 오른쪽 큰 화면이 없다
- 형식 문서가 "그 주변만 잘라 넣고" 라고 적는다 (`record-format.md:126`)
- 기준값(2026-10-09 11:26, 커밋 `676301f3`): 단위 테스트 57 개 통과

## 범위 경계

```text
# sprint-scope
flutter-toolkit/skills/flutter-scenario-report/
flutter-toolkit/evals/scenario-report/
.harness/
```

- 하지 않는 것: 확대 창 제거 · 시나리오 사진 줄 변경 · README · 릴리스
- 측정 공통 정의: `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/scenario-op-roi` · `K=$W/flutter-toolkit/skills/flutter-scenario-report` · `T=$W/flutter-toolkit/evals/scenario-report` · 시작 커밋 `BASE=676301f3` · 끝 `TIP=$(git -C $W rev-parse feat/scenario-op-roi)` (구현 커밋 뒤) · 단위 테스트 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v` (`$W` 에서)
- 잘라 보기 계산(알려진 답의 근거): 칸 72px, 배율 `s = 72 / 사진 폭`(사진 폭이 칸 폭), `left` 는 늘 0, `top = 반올림(min(0, max(72 - 사진 높이·s, 36 - y·s)))`, 동그라미 `(반올림(x·s), 반올림(y·s) + top)`, 반올림은 `floor(v + 0.5)`. 손 계산: 402×874 에 `[355, 97]` → 17.37 이라 36 - 17.37 > 0 → top 0, 동그라미 (64, 17) · `[137, 684]` → 36 - 122.51 = -86.51 은 하한 72 - 156.54 = -84.54 로 막혀 top -85, 동그라미 (25, 123 - 85 = 38) · 0.5 경계 144×800(`s = 0.5`)에 `[1, 147]` → 36 - 73.5 = -37.5 → top -37 (짝수 쪽 반올림이면 -38), 동그라미 (1, 74 - 37 = 37)
- 넓은 화면 108px 는 칸 안 계산을 72px 기준으로 둔 채 틀이 칸 전체를 1.5 배로 그려 얻는다. `zoom` 을 모르는 옛 브라우저에서는 72px 칸 옆에 빈 자리가 남는다 — 깨지지 않으므로 받아들인다
- 칸 테두리는 그림을 가리지 않는 바깥 선(`box-shadow`)으로 그리고 `border` 는 0 이다. 지금은 `box-sizing:border-box` 에 1px 테두리라 안쪽이 70px 이고 그림 오른쪽 · 아래 2px 가 가려진다
- 조작 번호(`조작 k/n`)는 확대 창 `.info` 와 같은 규칙이다 — 그 단계(`do` 목록, 접힌 것 포함) 안 순번 / 개수
- 큰 화면은 보조 기술에 같은 내용을 두 번 읽히지 않도록 `aria-hidden="true"` 이고 그림 `alt` 는 빈 글자다. 조작 칸 버튼의 `aria-label` 이 이미 같은 정보를 준다
- 알려진 한계: 폭 1100px 이상 터치 기기(태블릿 가로)는 마우스 올리기가 없어 큰 화면이 첫 조작에 머문다. 칸을 누르면 확대 창으로 볼 수 있다
- 측정 브라우저는 Chromium(`playwright` 의 `chromium`) 기준이다
- 사전 측정 스크립트가 고장을 잡는지 본 결과(동그라미 위치를 틀리게 한 사본 · 마우스 올리기 처리를 지운 사본에서 각각 FAIL)는 `.harness/.meta/scenario-report-op-follow/neg-results.txt` 에 명령과 출력째 남긴다
- 브라우저 확인: 예시 폴더를 `python3 -m http.server --bind 127.0.0.1` 로 띄워 연다. 판정 격리 안에서는 브라우저가 막히므로 이번에 만들 사전 측정 스크립트 `.harness/.meta/scenario-report-op-follow/measure.sh {id}` 를 `codex_audit.premeasure` 에 건다(앞 계약과 같은 방식). 그 스크립트가 고장을 잡는지(동그라미 위치를 틀리게 한 사본 · 마우스 올리기 처리를 지운 사본에서 FAIL)를 구현 단계에서 확인해 판정 자료에 남긴다
- 마크다운 경고 측정: 세션 임시 폴더 `mdlint/node_modules/.bin/markdownlint-cli2 --config mdlint/cfg.markdownlint-cli2.jsonc <파일>`
- 오라클 해소: 스킬-01 — 산출물이 안내 문서라 문구 존재가 결과다. 동작은 스크립트 · 구조 조건이 잰다

## Skill

- [ ] 스킬-01: 기록 형식 문서의 `at` 줄이 "화면 폭은 그대로 두고 위아래만 누른 곳 주변으로 잘라" 보여 준다고 적고, "그 주변만 잘라 넣고" 는 남지 않는다 [exact]
    측정: `grep -c '화면 폭은 그대로 두고 위아래만' $K/references/record-format.md` 1 · `grep -c '그 주변만 잘라 넣고' $K/references/record-format.md` 0
    양성 대조: 봉인 시점(`676301f3`) 파일에서 뒤 측정이 1

## Script

- [ ] 스크립트-01: Given 402×874 조작 사진과 `at` `[355, 97]`. When 보고서를 만들면 Then 조작 칸 그림이 `<img src="02-confirm.png" width="402" height="874" alt="" style="left:0px;top:0px"><i class="tap" style="left:64px;top:17px"></i>` 이고, `[137, 684]` 면 `style="left:0px;top:-85px"><i class="tap" style="left:25px;top:38px">`, 144×800 사진에 `[1, 147]` 이면 `style="left:0px;top:-37px"><i class="tap" style="left:1px;top:37px">` 다 [exact]
    측정: 단위 테스트 `test_at_rendered_as_crop` 통과 — 기대 글자는 범위 경계의 손 계산 값을 그대로 적는다. 이 테스트의 옛 200px 기준 기대 글자는 새 값으로 바꾸고 이름은 그대로 둔다
    음성 대조: 아래 경계(`max(72 - 사진 높이·s, …)`)를 뺀 사본 · 반올림을 파이썬 기본 `round` 로 바꾼 사본에서 이 테스트가 FAIL
- [ ] 스크립트-02: 틀에서 `.op-thumb img{` 규칙의 폭이 `width:72px` 이고, `.op-thumb{` 규칙에 `border:0` 과 `box-shadow` 가 있고, `@media (min-width:901px){` 로 시작하는 한 줄에 `22px 108px` 칸 폭과 `.op-thumb{zoom:1.5` 가 있다 [exact]
    측정: 단위 테스트 `test_template_op_thumb_rules` 통과 (규칙은 `re.search(r"\.op-thumb\{[^}]*\}")` 꼴로, 넓은 화면 규칙은 `@media (min-width:901px){` 로 시작하는 줄을 찾아 글자 확인). 옛 `width:200px` 단언은 새 값으로 바꾸고 이름은 그대로 둔다
    양성 대조: 봉인 시점 틀에서 `width:72px` 은 `.op-thumb img{` 규칙에 0 건, `zoom:1.5` 0 건
- [ ] 스크립트-03: 기존 테스트 57 개 이름이 모두 남고 전체가 통과하며, 커밋된 예시 보고서 전부(구현 커밋에서 다시 만든 것)가 다시 만든 것과 바이트 단위로 같다 [exact]
    측정: 기준 커밋 `676301f3` 테스트 파일의 `def test_` 이름 57 개가 현재 파일에 각 1 · 단위 테스트 종료 0 · 출력 끝 `OK` · `test_example_report_is_current` 통과

- [ ] 스크립트-04: 틀에 큰 화면 규칙과 처리가 정적으로 있다 — `@media (min-width:1100px){` 로 시작하는 줄에 `.follow{display:block` 이 있고 그 밖의 `.follow{display:none}` 이 있으며, 틀 스크립트에 `"mouseenter"` · `"focusin"` · `aria-hidden` 이 있고, `addEventListener("scroll"` 개수는 기준과 같은 2 다 (큰 화면은 스크롤로 바뀌지 않는다) [exact]
    측정: 단위 테스트 `test_template_follow_rules` 통과 · `grep -o 'addEventListener("scroll"' $K/templates/report.html | wc -l` 이 2
    양성 대조: 봉인 시점 틀에서 `.follow{` · `"mouseenter"` 0 건

## Error

- [ ] 오류-00: N/A (기록 형식 · 검사 규칙은 바뀌지 않는다 — `at` 검사는 앞 계약 그대로. 측정: `git -C $W diff $BASE..$TIP -- $K/scripts/build_report.py` 에서 `errors.append` 가 든 바뀐 줄 0)

## Architecture

- [ ] 구조-01: 바뀐 파일이 범위 경계 세 경로 안에만 있다 [exact]
    측정: `git -C $W diff --name-only $BASE..$TIP -- . ':(exclude).harness'` 각 줄이 `flutter-toolkit/skills/flutter-scenario-report/` · `flutter-toolkit/evals/scenario-report/` 로 시작
- [ ] 구조-02: Given 예시 `TC-003-shot-strip/index.html` 을 1280×900 으로 연다. Then (a) `.op-thumb` 가 108×108 이고 그 안 그림의 표시 폭도 108 (테두리가 가리지 않음) (b) 시나리오 1 카드에 큰 화면(`.follow`)이 하나 보이고 글줄이 `PGA 브라보를 골라 확인 창을 연다 — 조작 1/3 · ⋯ 버튼 탭`, 큰 화면 왼쪽 끝이 단계 목록(`.stepl`) 오른쪽 끝 이상이고 큰 화면 위쪽 끝이 단계 목록 위아래 범위 안 (단계 목록 오른쪽에 놓임). When 문서 순서로 세 번째 `.op-thumb` 에 마우스를 올리면 Then 글줄이 `… — 조작 3/3 · "PGA 브라보" 탭` 이고 큰 화면의 동그라미 가운데가 큰 사진 왼쪽 위 + (137/402 · 표시 폭, 684/874 · 표시 높이) 에서 가로 · 세로 2px 안. When 마우스를 칸 밖 빈 곳으로 옮기고 페이지를 300px 스크롤하면 Then 글줄이 그대로 `조작 3/3`. When 첫 `.op-thumb` 에 키보드 초점을 두면 Then 글줄이 `조작 1/3`. When 첫 `.op-thumb` 를 누르면 Then 확대 창이 열리고 `.info` 가 `조작 1/3 · ⋯ 버튼 탭`. 콘솔 오류 0 건 [exact]
    측정: 사전 측정 출력 또는 `mcp__playwright__*` 로 단계마다 값 읽기 (`browser_hover` · `browser_evaluate` · `browser_click`). 크기 · 위치는 `getBoundingClientRect()` 로 읽는다
- [ ] 구조-03: Given 예시 `TC-002-appoint-vice-leader/index.html` 을 1280×900 으로 연다. Then 큰 화면이 정확히 2 개(조작 사진이 있는 시나리오 1 · 2)이고 건너뛴 시나리오 3 카드에는 0 개. When 시나리오 2 의 `.op-thumb` 에 마우스를 올리면 Then 시나리오 2 큰 화면 글줄만 `부방장 임명을 누른다 — 조작 1/1 · "부방장 임명" 탭` 이고 시나리오 1 큰 화면 글줄은 `⋯ 버튼을 누른다 — 조작 1/1 · ⋯ 버튼 탭` 그대로. Given 폭 1000×900 이면 Then 칸 108×108 이고 큰 화면이 안 보인다(`display` 가 `none`). Given 390×844 면 Then 칸 72×72 · 큰 화면 안 보임 · `scrollWidth <= innerWidth`. Given 접힌 조작 임시 예시(`python3 $T/fold_fixture.py $T/example <임시 폴더> && python3 $K/scripts/build_report.py <임시 폴더>`, 1280×900). When 접힌 목록을 펼치고 네 번째 조작 그림에 마우스를 올리면 Then 글줄이 `… — 조작 4/4 · 네 번째 조작` 이고 좌표 없는 조작이라 큰 화면 동그라미 `hidden` 참. 콘솔 오류 0 건 [exact]
    측정: 구조-02 와 같은 도구

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 종료 0
- [ ] 금지-04: SKILL.md frontmatter 에서 name 필드 누락 금지
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=frontmatter` 종료 0

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 큰 화면의 동그라미 위치는 확대 창과 같은 칸 속성(`data-x` · `data-y`)과 사진 크기 속성으로 계산하고, 잘라 보기는 기존 함수 하나를 고친다
    측정: `grep -c 'def op_thumb_html' $K/scripts/build_report.py` 1 · `grep -c '<dialog' $K/templates/report.html` 1

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경과 교집합 0. 대신 스크립트-03 단위 테스트와 `python3 scripts/validate-plugin.py flutter-toolkit` 종료 0)
- [ ] 진단-02: 바뀐 마크다운 파일 `$K/references/record-format.md` 의 마크다운 경고 0 건
    측정: 범위 경계의 markdownlint-cli2 명령 → `Summary: 0 issues`
- [ ] 진단-03: N/A (commands.test 는 scripts/release.sh 실행 — 이번 변경과 무관. 콘솔 오류는 스크립트-03 출력 `OK`)
- [ ] 진단-04: N/A (구동할 앱 · 서버 없음 — 정적 HTML. 브라우저 확인은 구조-02 · 구조-03)
