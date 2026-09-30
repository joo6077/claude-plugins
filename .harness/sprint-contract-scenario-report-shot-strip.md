---
feature: "flutter-scenario-report — 시나리오 사진을 칸 단위 가로 줄로 · 가로로 긴 조각은 두 칸 · 넘치면 옆으로 넘기고 더 있음 표시"
slug: scenario-report-shot-strip
created: "2026-09-30 16:57"
complexity: "중간"
conditions: 16
status: active
owner_session: 97f28e34-99ea-4a74-9baa-3288b7964458
conditions_digest: sha256:138129e244344c31
measurement_digest: sha256:b4a6771747498786
locked_at: "2026-09-30 17:01"
---

## 배경

- 사용자 요구(2026-09-30 대화): 사진이 많으면 가로 스크롤이 생기게 하되 한 번에 보이는 최대 수와 최소 폭을 정한다. 잘라 낸 사진(한 영역만 올린 것)도 고려한다. 스크롤이 생기면 옆에 사진이 더 있다는 걸 보여 준다
- 사용자 결정: 시안 `scroll2.html` 그대로 — 사진은 장수와 관계없이 단계 글 위 한 줄, 한 번에 4 장 남짓(4.3 칸), 한 칸 최소 160px, 가로로 긴 사진(폭 > 높이 × 1.2)은 두 칸, 4 장을 넘으면 "사진 N장" 표시, 넘칠 때 오른쪽 흐림 · "›" 버튼. 시안 캡처: 세션 임시 폴더 `four-shots/crop-new-wide4.png` · `crop-new-wide4-end.png`
- main 에서 들어온 `f77b580c` 의 3 장 이상 규칙(`.body:has(.shots figure:nth-child(3))`)을 이 규칙이 대신한다

## GAP 분석

- 실측(합친 판 `d8bb68b4`, 1440px): 사진 2 장 시나리오에 402×160 조각을 넣으면 폭 1489px 로 카드 밖으로 넘친다(`scrollWidth > clientWidth`). 3 장 이상이면 모든 사진이 같은 폭 191px 라 같은 조각이 높이 77px 로 줄어든다
- 사진 줄에 넘김 · 더 있음 표시가 없다
- 시안에서 "더 있음" 에 `more` 이름을 쓰자 조작 접기 `.more{grid-column:2 / 3}` 와 겹쳐 단계 글 폭이 0 이 됐다 — 새 이름은 틀에 없는 것을 쓴다(실측 0 건: `shot-strip` · `shot-frame` · `shot-count` · `shot-next` · `has-more` · `wide`)
- 기준값(2026-09-30 16:55, 커밋 `d8bb68b4`): 단위 테스트 44 개 통과

## 범위 경계

```text
# sprint-scope
flutter-toolkit/skills/flutter-scenario-report/
flutter-toolkit/evals/scenario-report/
.harness/
```

- 하지 않는 것: 조작 사진(`do`) · 확대 사진(`zoom`) 모양 변경, README 수정, 버전 올리기
- 측정 공통 정의: `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/scenario-report-per-case` · `K=$W/flutter-toolkit/skills/flutter-scenario-report` · `T=$W/flutter-toolkit/evals/scenario-report` · 시작 커밋 `BASE=d8bb68b4` · 끝 `TIP=$(git -C $W rev-parse feat/scenario-report-per-case)` · 단위 테스트 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v` (`$W` 에서)
- 브라우저 확인은 예시 폴더를 `python3 -m http.server --bind 127.0.0.1` 로 띄워 `mcp__playwright__*` 로 연다. 창 크기는 `browser_resize` 로 1440×900 과 600×900. 캡처는 세션 임시 폴더 `evidence/` 로 옮긴다
- 예시에 사진 5 장 케이스 `TC-003-shot-strip` 을 더한다 — 기존 예시 캡처를 복사해 쓰고, 그중 하나는 가로로 긴 조각(402×107)이다. TC-002 시나리오 2 의 사진에도 그 조각을 더해 2 장 시나리오의 넘침을 잰다
- 오라클 해소: SK-01 — 산출물이 스킬 안내문이라 문구 존재가 결과다

## Skill

- [ ] SK-01: 스킬 3 단계가 잘라 낸 사진도 시나리오 사진(`shots`)에 넣을 수 있고, 가로로 긴 사진은 보고서에서 두 칸을 쓴다고 적는다 [exact]
    측정: `awk '/^### 3\./,/^### 4\./' $K/SKILL.md` 에 `두 칸` 이 든 줄이 1 이상

## Script

- [ ] SC-01: 시나리오 사진은 `<div class="shot-strip">` 안의 `<div class="shots">` 에 들어가고, 사진마다 `<figure>` 안에 `<div class="shot-frame">` 가 이미지를 감싼다. 폭이 높이의 1.2 배를 넘는 사진의 `figure` 에는 `class="wide"` 가 붙고, 아니면 붙지 않는다 [exact]
    측정: 단위 테스트 `test_shots_in_strip` · `test_wide_shot_takes_two_slots` 통과 (20×5 PNG → `wide`, 3×7 · 7×7 PNG → 없음)
    음성 대조: `wide` 판정을 빼는 사본에서 `test_wide_shot_takes_two_slots` 가 FAIL
- [ ] SC-02: 사진이 5 장 이상이면 사진 줄 위에 `<p class="shot-count">사진 {N}장</p>` 이 있고, 4 장 이하면 없다. `<button class="shot-next"` 는 사진이 있는 모든 줄에 1 개다 [exact]
    측정: 단위 테스트 `test_shot_count_after_four` 통과 — 같은 테스트가 `shot-count` (5 장 → 1, 4 장 → 0)와 `shot-next` 개수(사진 있는 시나리오 수와 같음)를 함께 잰다
- [ ] SC-03: 페이지 틀의 사진 규칙 — `.body` 는 한 칸 그리드이고 3 장 이상 전용 규칙(`.body:has(`)이 0 개다. `.shots` 에 `overflow-x:auto` 가 있고, 칸 폭이 `max(160px,calc((100% - 4 * 14px) / 4.3))` 이며, `.wide` 는 두 칸 폭이다. `.shot-strip.has-more` 가 흐림과 `.shot-next` 를 보이게 한다 [exact]
    측정: 단위 테스트 `test_template_strip_rules` 가 위 글자들을 틀에서 찾고 `.body:has(` 0 개를 확인하고 통과
    양성 대조: 시작 커밋 `d8bb68b4` 의 틀에서 같은 테스트 로직이 `.body:has(` 4 개를 낸다
- [ ] SC-04: 페이지 틀의 반응형 · 스크립트 — 900px 이하 규칙 안에 옛 사진 규칙(`.shots figure{` · `.shots img{`)이 0 개다. 화면 스크립트가 사진 줄마다 `scrollLeft + clientWidth < scrollWidth - 2` 일 때 `has-more` 를 붙이고(스크롤 · 창 크기 바뀔 때 다시 계산), `.shot-next` 를 누르면 `clientWidth * 0.8` 만큼 넘긴다. `has-more` 는 장수가 아니라 실제 넘침으로 정한다 — `shot-count`(장수 기준)와 별개다 [exact]
    측정: 단위 테스트 `test_template_strip_script` 가 900px 이하 블록(`@media (max-width:900px){` 부터 짝 닫는 괄호까지)에서 두 옛 규칙 0 개, 스크립트에서 `has-more` · `scrollLeft+row.clientWidth<row.scrollWidth-2` · `clientWidth*0.8` 글자를 찾고 통과
    양성 대조: 시작 커밋 틀의 900px 이하 블록에서 두 옛 규칙이 각 1 개

## Error

- [ ] ER-00: N/A (새 입력 키가 없다 — 사진 크기는 기존 PNG 검사가 읽은 값을 쓴다. 측정: `git diff d8bb68b4 -- $K/scripts/build_report.py | grep -cE '^\+.*_FIELDS'` 가 0)

## Architecture

- [ ] AR-01: 바뀐 파일이 범위 경계 세 경로 안에만 있다 [exact]
    측정: `git -C $W diff --name-only $BASE..$TIP -- . ':(exclude).harness'` 각 줄이 `flutter-toolkit/skills/flutter-scenario-report/` · `flutter-toolkit/evals/scenario-report/` 로 시작. 밖 경로 0 줄
- [ ] AR-02: Given 예시 보고서를 다시 만든 뒤 1440×900. When `TC-001` · `TC-002` · `TC-003` 케이스 페이지를 각각 열면 Then 모든 시나리오 카드가 넘치지 않고(`scrollWidth <= clientWidth`) — 가로로 긴 조각이 든 TC-002 시나리오 2 포함 — 사진이 있는 시나리오마다 단계 목록 폭이 사진 줄 폭과 같다(±1px, 단계 글이 눌리지 않는다). 사진 없는 시나리오는 폭 비교에서 뺀다 [exact]
    측정: 페이지마다 `browser_evaluate` 로 카드마다 `section.scrollWidth <= section.clientWidth`, `.shot-strip` 이 있는 카드는 `.stepl` 폭과 `.shot-strip` 폭 차이 ≤ 1
- [ ] AR-03: Given 1440×900 에서 `TC-003` 을 연다. Then 사진 줄에 `has-more` 가 붙어 있고 5 번째 사진이 오른쪽에 일부 보인다. When `.shot-next` 를 `has-more` 가 빠질 때까지 누르면(최대 3 번, 누를 때마다 0.8 초 기다림) Then 줄 끝에 닿아 `has-more` 가 빠진다. 600×900 에서는 칸 폭이 160px 이상이고 페이지 전체 가로 넘침이 없다 [exact]
    측정: `browser_evaluate` (`has-more` 여부 · 5 번째 `figure` 의 왼쪽 < 줄 오른쪽 < 오른쪽) → `browser_click` 반복(최대 3 번) → `Math.abs(scrollLeft - (scrollWidth - clientWidth)) <= 1` 와 `has-more` 없음 → `browser_resize 600 900` → 칸 폭 최소값 ≥ 160, `document.documentElement.scrollWidth <= innerWidth` → 캡처 두 장

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 종료 0

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 사진 확대는 기존 확대 창을 그대로 쓴다
    측정: `grep -c 'dialog class="viewer"' $K/templates/report.html` 가 1 · 확대 창 선택자에 `.shots img` 가 그대로 있다

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 대신 DG-03 자리의 단위 테스트와 validate-plugin 을 본다)
- [ ] DG-02: 바뀐 마크다운 파일(`$K/SKILL.md`)의 마크다운 경고가 0 건이다
    측정: 세션 임시 폴더 `mdlint/node_modules/.bin/markdownlint-cli2 --config mdlint/cfg.markdownlint-cli2.jsonc $K/SKILL.md` 가 `Summary: 0 issues`
- [ ] DG-03: 단위 테스트 전체가 통과하고 기존 44 개 이름이 모두 남아 있으며, 예시 보고서 전부가 다시 만든 것과 바이트 단위로 같다
    측정: 시작 커밋 테스트 파일의 `def test_` 이름 44 개가 현재 파일에 각 1 · 단위 테스트 종료 0 · `OK`
- [ ] DG-04: 브라우저 콘솔 오류 0 건 (AR-02 · AR-03 을 연 페이지)
    측정: `browser_console_messages` level error 0
