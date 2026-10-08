---
feature: "flutter-scenario-report — 조작 칸에 누를 곳 주변만 잘라 보여 주기 · 확대 창에서 앞뒤 조작 넘기기"
slug: scenario-report-op-roi
created: "2026-10-08 18:46"
complexity: "복잡"
conditions: 20
status: active
owner_session: 97f28e34-99ea-4a74-9baa-3288b7964458
conditions_digest: sha256:b48fc19bba7ba404
measurement_digest: sha256:bd92284913f147f5
locked_at: "2026-10-08 18:53"
---

## 배경

- 앞 계약 `scenario-report-op-shots`(APPROVE) 가 조작마다 캡처를 붙이고 44px 폭으로 줄여 그렸다. 사용자는 "크게 보이면 불편, 작게 보이면 불편" 이라 했고, Codex 조사 2(필름 띠 · 탭 좌표 표시 · 부분 확대 · 확대 창 접근성)를 거쳐 두 가지를 함께 넣기로 했다 (2026-10-08 대화, 시안 세션 임시 폴더 `opfocus/TC-003/gallery.html` · 생성기 `opfocus/make_gallery.py`)
- 결정 1: 조작 칸을 72px 정사각형으로 키우고, 그 안에 누를 곳 주변만 잘라 넣고 파란 동그라미로 누를 곳을 표시한다. 칸 크기는 구현 뒤 사용자가 보고 작으면 키운다
- 결정 2: 조작 칸이나 시나리오 사진을 누르면 뜨는 확대 창에서 같은 묶음의 앞뒤 사진으로 넘긴다 — ‹ › 버튼 · ←/→ 키 · "조작 k/n · 조작 글자" 표시 · 처음/끝에서 반대쪽 버튼 숨김 · Esc 로 닫으면 누른 칸으로 초점이 돌아간다
- 결정 3 (2026-10-08 사용자 "ㄱㄱ"): 조작 칸 캡처를 "누른 직후 화면" 에서 "누르기 직전 화면 + 누를 곳" 으로 바꾼다. 누른 결과는 다음 조작 칸이나 확인 단계 사진에서 보인다. 앱을 누를 때 쓰는 좌표(화면 논리 단위)는 사진 폭 ÷ 화면 폭 비율로 사진 픽셀로 바꿔 적는다
- 좌표가 없는 옛 기록은 지금처럼 화면 전체를 줄여 보여 준다 — 하위 호환

## GAP 분석

- 기록에 누른 위치를 담을 자리가 없다 — 조작 항목 키는 `act` · `shot` 둘뿐이다 (`build_report.py:37`)
- 조작 한 줄은 44px 폭 `<img>` 하나라 키보드로 열 수 없고 잘라 보기도 없다 (`build_report.py:199` · `templates/report.html:73-75`)
- 확대 창은 사진 한 장만 띄우고 앞뒤로 넘기는 수단 · 몇 번째인지 표시가 없다 (`templates/report.html:117-120`)
- 스킬 3 · 4 단계와 형식 문서는 조작 캡처를 "직후" 로 적는다 (`SKILL.md:97` · `record-format.md:124` · `build_report.py:153`, `grep -c '직후'` 각 1)
- 예시 세 케이스의 조작 캡처는 누른 뒤 화면이고, TC-002 · TC-003 에는 아무것도 안 열린 첫 화면 사진이 없다. 첫 화면 그림은 `TC-003-shot-strip/05-after-cancel.png` 와 바이트가 같다 (`cmp` 0)
- 기준값(2026-10-08 18:40, 커밋 `fc9ab639`): 단위 테스트 49 개 통과 · 바뀔 마크다운 두 파일 경고 0 건 · 예시 사진은 모두 402 폭

## 범위 경계

```text
# sprint-scope
flutter-toolkit/skills/flutter-scenario-report/
flutter-toolkit/evals/scenario-report/
.harness/
```

- 하지 않는 것: 루트 · 킷 README · 문서 사이트 수정, 버전 올리기와 릴리스, 시나리오 사진(`shots`)의 잘라 보기, 넘기기 애니메이션
- 측정 공통 정의: 작업 폴더 `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/scenario-op-roi` · `K=$W/flutter-toolkit/skills/flutter-scenario-report` · `T=$W/flutter-toolkit/evals/scenario-report` · 시작 커밋 `BASE=fc9ab639` · 끝 `TIP=$(git -C $W rev-parse feat/scenario-op-roi)` (구현 커밋 뒤 잰다) · 단위 테스트 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v` (`$W` 에서) · 임시 폴더 `S=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/97f28e34-99ea-4a74-9baa-3288b7964458/scratchpad`
- 좌표 `at` 은 그 조작 칸 사진(`shot`)의 픽셀 기준 `[x, y]` 이다. 잘라 보기 계산(알려진 답의 근거): 사진 전체를 폭 200px 로 줄인 배율 `s = 200 / 사진 폭`, 칸 72px, `left = min(0, max(72 - 200, 36 - x·s))`, `top = min(0, max(72 - 사진 높이·s, 36 - y·s))`, 동그라미 위치 `(x·s + left, y·s + top)`, 반올림은 0.5 를 올리는 방식(`floor(v + 0.5)`)이고, 사진의 `left` · `top` 을 먼저 반올림한 뒤 동그라미 위치는 `반올림(x·s) + left`, `반올림(y·s) + top` 이다. 402×874 사진에 `[355, 97]` → 사진 `left:-128px;top:-12px` · 동그라미 `left:49px;top:36px` (손 계산: 355·200/402 = 176.62 → 36 - 176.62 = -140.62 는 -128 로 막힘 · 97·200/402 = 48.26 → -12.26 · 동그라미 176.62 - 128 = 48.62 → 49, 48.26 - 12.26 = 36.00 → 36). `[10, 10]` → 사진 `left:0px;top:0px` · 동그라미 `left:5px;top:5px`. 0.5 경계: 400×800 사진(`s = 0.5`)에 `[1, 1]` → 사진 `left:0px;top:0px` · 동그라미 `left:1px;top:1px` (0.5 → 1, 짝수 쪽 반올림이면 0 이 나와 갈린다), `[147, 1]` → 36 - 73.5 = -37.5 → 사진 `left:-37px;top:0px` · 동그라미 74 - 37 = `left:37px;top:1px` (짝수 쪽 반올림이면 -38). `data-x` · `data-y` 는 기록에 적힌 수를 그대로 적는다(355 → `355`, 355.5 → `355.5`)
- 넘기기 묶음: 조작 칸은 그 칸이 속한 한 단계의 `do` 목록 전체(접힌 것 포함), 시나리오 사진은 그 시나리오 `shots` 전체, 확인 단계의 `zoom` 사진은 단독 한 장이다. 확대 창은 누른 칸이 속한 묶음 안에서만 넘긴다. 표시 글자는 조작이 `조작 k/n · 조작 글자`, 시나리오 사진이 `사진 k/n · 캡션`, 확대 사진이 `확대 · 캡션` 이다. 묶음이 한 장이면 이전 · 다음 버튼이 모두 숨는다
- 확대 창의 동그라미는 큰 사진과 같은 크기의 `.stage` 안에 사진 크기 대비 백분율(`x / 사진 폭 · 100%`, `y / 사진 높이 · 100%`)로 놓는다 — 사진을 다 받기 전에 계산해 위치가 어긋나는 일을 막는다. `at` 이 없는 사진에서는 동그라미가 숨는다
- 예시 조작 표 (구현 뒤 기대값 — 파일 · 좌표는 2026-10-08 세션 임시 폴더 `roi/png.py` 로 각 그림에서 그 단추 · 글자 막대의 가운데를 잰 값):

| 케이스 | 시나리오 · 단계 | 조작 글자 | `shot` | `at` |
| --- | --- | --- | --- | --- |
| TC-001 | 1 · 1 | ⋯ 버튼 탭 | `00-start.png` | `[362, 81]` |
| TC-001 | 1 · 1 | "방장 넘기기" 탭 | `00-menu.png` | `[263, 236]` |
| TC-001 | 1 · 2 | "취소" 탭 | `01-picker.png` | `[201, 814]` |
| TC-001 | 2 · 1 | ⋯ 버튼 탭 | `00-start.png` | `[362, 81]` |
| TC-001 | 2 · 1 | "방장 넘기기" 탭 | `00-menu.png` | `[263, 236]` |
| TC-001 | 2 · 1 | "PGA 브라보" 탭 | `01-picker.png` | `[137, 684]` |
| TC-001 | 2 · 2 | "취소" 탭 | `03-confirm.png` | `[128, 486]` |
| TC-002 | 1 · 1 | ⋯ 버튼 탭 | `00-start.png` | `[362, 81]` |
| TC-002 | 2 · 1 | "부방장 임명" 탭 | `01-menu.png` | `[268, 184]` |
| TC-002 | 3 · 1 | "PGA 알파" 탭 | 없음 | 없음 |
| TC-003 | 1 · 1 | ⋯ 버튼 탭 | `00-start.png` | `[362, 81]` |
| TC-003 | 1 · 1 | "방장 넘기기" 탭 | `01-menu.png` | `[263, 236]` |
| TC-003 | 1 · 1 | "PGA 브라보" 탭 | `02-picker.png` | `[137, 684]` |
| TC-003 | 1 · 2 | "취소" 탭 | `04-confirm.png` | `[128, 486]` |

- TC-002 시나리오 3 은 건너뛴 시나리오라 그 조작에는 사진 · 좌표를 달지 않는다(실행하지 않은 조작에 누를 곳을 표시하지 않는다)
- 새 파일 `00-start.png` 는 세 케이스 폴더에 하나씩, 내용은 `TC-003-shot-strip/05-after-cancel.png` 와 바이트가 같다
- 음성 대조는 `BUILD_REPORT_SCRIPT` 로 검사를 뺀 스크립트 사본을 돌린다. 사본 옆에 `templates/` 를 복사하고, 변이 전후 글이 다른지 먼저 확인한다
- 브라우저 확인: `cd $T/example && python3 -m http.server 8765 --bind 127.0.0.1` 로 띄우고 `mcp__playwright__*` 로 연다. 접힌 조작 확인용 임시 예시는 이번에 만들어 커밋할 `$T/fold_fixture.py` 로 만든다 — 예시 TC-003 을 복사해 시나리오 1 단계 1 끝에 `at` 없는 조작 `{"act": "네 번째 조작", "shot": "02-picker.png"}` 하나를 더한다. 명령 `python3 $T/fold_fixture.py $T/example $S/roi/fold && python3 $K/scripts/build_report.py $S/roi/fold` (봉인 전 같은 내용의 임시 사본 `$S/roi/fold_fixture.py` 로 실측: 종료 0, `조작 1개 더 보기 (모두 4개)` 1 건) `cd $S/roi/fold && python3 -m http.server 8766 --bind 127.0.0.1` 로 띄운다. 캡처는 레포 안에 저장된 뒤 `$S/roi/evidence/` 로 옮긴다. 브라우저 도구를 못 쓰는 환경이면 대체 측정으로 틀의 확대 창 스크립트에 `ArrowLeft` · `ArrowRight` · `.focus()` · `hidden` 이 있는지 보고 그 조건은 `[미검증]` 으로 둔다 — 구조-02 · 구조-03 중 1 건까지 받아들인다
- 마크다운 경고 측정: `$S/mdlint/node_modules/.bin/markdownlint-cli2 --config $S/mdlint/cfg.markdownlint-cli2.jsonc <파일>` (봉인 전 실측: 바뀔 두 파일 `Summary: 0 issues`)
- 기존 테스트 중 옛 조작 그림 조각을 전제한 `test_do_rendered_with_shots` 는 좌표 없는 항목의 그림이라 그대로 둔다 (공용 데이터 `VALID` 에는 `at` 을 넣지 않는다)
- 오라클 해소: 스킬-01 · 스킬-02 — 산출물이 스킬 안내문이라 문구 존재가 결과다. 안내가 가리키는 동작은 스크립트 조건이 테스트로 잰다

## Skill

- [ ] 스킬-01: SKILL.md 3 단계가 조작 칸 캡처를 누르기 직전에 찍으라고 적고, 누른 위치를 사진 픽셀 좌표로 바꾸는 규칙(사진 폭 ÷ 화면 폭)을 적는다. 4 단계가 `do` 항목을 `act` · `shot` · `at` 으로 쓰라고 한 줄에 적는다. 조작 캡처를 "직후" 로 적은 문장이 SKILL.md · 형식 문서 · 스크립트에 남지 않는다 [exact]
    측정: `awk '/^### 3\./,/^### 4\./' $K/SKILL.md | grep -c '누르기 직전'` 1 이상 · 같은 절 `grep -cF '사진 폭 ÷ 화면 폭'` 1 이상 · `awk '/^### 4\./,/^### 5\./' $K/SKILL.md | grep -F '`at`' | grep -F '`shot`' | grep -c '`act`'` 1 이상 · `grep -c '직후' $K/SKILL.md $K/references/record-format.md $K/scripts/build_report.py` 셋 다 0
    양성 대조: 봉인 시점(`fc9ab639`) 세 파일의 `grep -c '직후'` 가 각 1
- [ ] 스킬-02: 기록 형식 문서의 조작 항목 표에 `at` 줄(선택 · 두 수 목록 · `shot` 픽셀 기준 · `shot` 필요)이 있고, 문서 안 예시 기록이 `at` 을 쓰며 검사를 통과한다 [exact]
    측정: `test_format_doc_lists_every_key` · `test_format_doc_example_passes` 통과 · 문서의 json 코드 블록 예시를 파이썬으로 읽어 `at` 키가 든 조작 항목 1 개 이상

## Script

- [ ] 스크립트-01: 조작 항목의 `at` 은 선택 키이고, 숫자 두 개(정수 · 실수, 참거짓 제외) 목록이어야 하며 `0 ≤ x < 사진 폭`, `0 ≤ y < 사진 높이` 여야 한다. `shot` 없이 `at` 만 있으면 막는다. 막는 경우: 숫자 하나 · 글자 · 숫자 아닌 원소 · 참거짓 원소 · NaN · 무한대 · `x = 사진 폭` · 음수 · `shot` 없는 `at`. 통과: `[사진 폭 - 1, 사진 높이 - 1]` · `[0, 0]` [exact, enumerated]
    측정: 단위 테스트 `test_error_at_not_pair`(숫자 하나 · 글자 · 숫자 아닌 원소 · 참거짓 원소 · NaN · 무한대를 JSON 글자 `NaN` · `Infinity` 로 넣어 각각 종료 1) · `test_error_at_outside_shot` · `test_error_at_without_shot` · `test_at_inside_edges_passes` 통과 (`$W` 에서 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -k _at_ -v` 출력에 네 이름이 각각 `... ok`)
    음성 대조: 범위 검사를 뺀 사본에서 `test_error_at_outside_shot` 이 FAIL · `shot` 확인을 뺀 사본에서 `test_error_at_without_shot` 이 FAIL
- [ ] 스크립트-02: Given 402×874 조작 사진과 `at` `[355, 97]` 인 조작 1. When 보고서를 만들면 Then 그 줄이 정확히 `<li><span class="n">1</span><button type="button" class="op-thumb" data-x="355" data-y="97" aria-label="조작 1: PGA 브라보 탭 — 크게 보기"><img src="02-confirm.png" width="402" height="874" alt="" style="left:-128px;top:-12px"><i class="tap" style="left:49px;top:36px"></i></button><span class="act">PGA 브라보 탭</span></li>` 이고, `at` `[10, 10]` 이면 `style="left:0px;top:0px"` 와 `<i class="tap" style="left:5px;top:5px">`, `[355.5, 97]` 이면 `data-x="355.5"` 다. 400×800 사진에 `[1, 1]` 이면 사진 `left:0px;top:0px` · 동그라미 `left:1px;top:1px`, `[147, 1]` 이면 사진 `left:-37px;top:0px` · 동그라미 `left:37px;top:1px` 다 [exact]
    측정: 단위 테스트 `test_at_rendered_as_crop` 통과 — 기대 글자는 범위 경계의 손 계산 값을 그대로 적는다(스크립트 상수나 함수를 불러 계산하지 않는다)
    음성 대조: 칸 경계에서 막는 계산(`max(72 - 200, …)`)을 뺀 사본에서 이 테스트가 FAIL · 반올림을 파이썬 기본 `round` 로 바꾼 사본에서 이 테스트가 FAIL
- [ ] 스크립트-03: 페이지 틀이 조작 칸을 72px 정사각형으로 그리고 넘치는 부분을 가린다 — `.op-thumb{` 규칙에 `width:72px` · `height:72px` · `overflow:hidden` 이 있고, `.op-thumb img{` 규칙에 `position:absolute` · `max-width:none` · `width:200px` 가 있고, `.op-thumb .tap{` 규칙에 `border-radius:50%` 가 있고, `.op-thumb:focus-visible{` 규칙에 `outline` 이 있다 [exact]
    측정: 단위 테스트 `test_template_op_thumb_rules` 통과 (각 규칙을 `re.search(r"\.op-thumb\{[^}]*\}", text)` 꼴로 뽑아 글자 확인)
    양성 대조: 봉인 시점 틀에서 네 규칙 모두 0 건
- [ ] 스크립트-04: 확대 창 마크업이 정확히 `<dialog class="viewer" aria-labelledby="viewer-info"><button type="button" class="close" autofocus>닫기</button><div class="stage"><img alt=""><i class="tap" hidden></i></div><button type="button" class="nav prev" aria-label="이전 사진">‹</button><button type="button" class="nav next" aria-label="다음 사진">›</button><p class="info" id="viewer-info" aria-live="polite"></p></dialog>` 로 틀에 한 번 있다 [exact]
    측정: 단위 테스트 `test_template_viewer_markup` 통과 (`text.count(위 글자) == 1`) — 마크업 글자만 재는 조건이다. 넘기기 동작은 구조-02 · 구조-03 이 브라우저에서 잰다
- [ ] 스크립트-05: `at` 이 없는 조작 항목은 지금 그림 그대로다 — 기존 49 개 테스트 이름이 모두 남아 있고 전체 테스트가 통과하며, `test_do_rendered_with_shots` 본문이 기준 커밋과 같다 [exact]
    측정: `git -C $W show fc9ab639:flutter-toolkit/evals/scenario-report/test_build_report.py | grep -oE 'def test_[a-z0-9_]+'` 49 개가 현재 파일에 각 1 · 단위 테스트 종료 0 · 출력 끝 `OK` · 기준 커밋과 현재 파일에서 `def test_do_rendered_with_shots` 부터 다음 함수 정의 줄 앞까지 잘라 `diff` 0 줄
- [ ] 스크립트-06: 예시 기록 세 개의 조작 항목이 범위 경계 "예시 조작 표" 14 줄과 글자 · 파일 · 좌표가 모두 같고(조작 항목 수도 14), 세 케이스 폴더의 `00-start.png` 가 `05-after-cancel.png` 와 바이트가 같으며, 커밋된 예시 보고서 전부가 다시 만든 것과 바이트 단위로 같다 [exact, enumerated]
    측정: 파이썬으로 `$T/example/TC-*/record.json` 의 `(케이스 id, 시나리오 번호, 단계 번호, act, shot, at)` 를 모아 표 14 줄과 집합 비교 → 차이 0 · `cmp` 세 번 종료 0 · `test_example_report_is_current` 통과
    알려진 답: 표 줄 수 14 = TC-001 7 + TC-002 3 + TC-003 4 (봉인 시점 예시의 조작 항목 수도 2+1+3+1 · 1+1+1 · 3+1 = 14)

## Error

- [ ] 오류-01: `at` 오류 줄이 케이스 폴더 · 시나리오 · 단계 · 조작 번호를 짚고, 범위를 벗어나면 사진 크기를 함께 적는다 — 예 `TC-001-transfer/record.json 시나리오 1 단계 1.do[1].at` 과 `402×874`. `shot` 검사가 실패한 항목(파일 없음 · PNG 아님)은 크기를 모르므로 `at` 범위 오류를 따로 내지 않고 `shot` 오류만 낸다 [exact]
    측정: `test_error_at_outside_shot` 가 stderr 에 `TC-001-transfer/record.json 시나리오 1 단계 1.do[1].at` 과 `402×874` 를 담는지 확인하고 통과 · `test_at_skipped_when_shot_bad`(없는 파일 `shot` + `at` `[9999, 0]`) 가 stderr 에 `.do[1].shot` 을 담고 `.do[1].at` 을 담지 않는지 확인하고 통과

## Architecture

- [ ] 구조-01: 바뀐 파일이 범위 경계 세 경로 안에만 있다 [exact]
    측정: `git -C $W diff --name-only $BASE..$TIP -- . ':(exclude).harness'` 각 줄이 `flutter-toolkit/skills/flutter-scenario-report/` · `flutter-toolkit/evals/scenario-report/` 로 시작한다. 밖 경로 0 줄
- [ ] 구조-02: Given 예시 보고서를 다시 만든 뒤 간이 서버로 `TC-003-shot-strip/index.html` 을 1280×900 으로 연다. When 시나리오 1 단계 1(조작 3 개)의 첫 `.op-thumb` 를 누르면 Then (a) 확대 창이 열리고 `.info` 글자가 `조작 1/3 · ⋯ 버튼 탭` (b) 이전 버튼 `hidden` 참 · 다음 버튼 `hidden` 거짓 (c) 동그라미 `.stage .tap` 이 보이고 그 가운데가 큰 사진 왼쪽 위 + (362/402 · 사진 표시 폭, 81/874 · 사진 표시 높이) 에서 가로 · 세로 각 2px 안 — 첫 클릭과, 닫았다 같은 칸을 다시 누른 두 번째 클릭 모두. When → 를 두 번 누르면 Then `.info` 가 `조작 3/3 · "PGA 브라보" 탭` 이고 다음 버튼 `hidden` 참. When ← 를 한 번 누르면 Then `조작 2/3 · "방장 넘기기" 탭`. When Esc 를 누르면 Then 확대 창이 닫히고 `document.activeElement` 가 처음 누른 `.op-thumb` 다. 콘솔 오류 0 건, 캡처 한 장 [exact]
    측정: `browser_navigate` → `browser_click`(첫 `.op-thumb`) → `browser_evaluate` 로 위 값 읽기 → `browser_press_key` ArrowRight ×2 · ArrowLeft · Escape 사이마다 `browser_evaluate` → `browser_console_messages` 오류 0 → `browser_take_screenshot` (확대 창 열린 상태 한 장, `$S/roi/evidence/` 로 옮김)
- [ ] 구조-03: Given 같은 페이지. When 시나리오 사진 줄의 두 번째 사진을 누르면 Then `.info` 가 `사진 2/5 · 그룹 고르는 창` 이고 동그라미 `hidden` 참. When 첫 `.op-thumb` 에 초점을 두고 Enter 를 누르면, 닫고 다시 초점을 두고 Space 를 누르면 Then 두 번 모두 확대 창이 열린다. Given `TC-002-appoint-vice-leader/index.html`. When 시나리오 1 의 `.op-thumb` 를 누르면 Then `.info` 가 `조작 1/1 · ⋯ 버튼 탭` 이고 이전 · 다음 버튼 `hidden` 모두 참. When 시나리오 2 확인 단계의 확대 사진(`.zoom img`)을 누르면 Then `.info` 가 `확대 · 잘린 제목` 이고 두 버튼 `hidden` 참 · 동그라미 `hidden` 참. Given 접힌 조작 확인용 임시 예시(범위 경계의 준비 명령). When 첫 `.op-thumb` 를 누르고 → 를 세 번 누르면 Then `.info` 가 `조작 4/4 · 네 번째 조작` (접힌 목록의 조작까지 한 묶음)이고, `at` 이 없는 그 조작에서 동그라미 `hidden` 참. Given 예시 TC-003 을 390×844 로 열면 Then `.op-thumb` 의 크기가 72×72 이고 `document.documentElement.scrollWidth <= innerWidth` [exact]
    측정: 구조-02 와 같은 도구로 단계마다 `browser_evaluate`, 390 폭은 `browser_resize` 뒤 `getBoundingClientRect()` · `scrollWidth` 읽기, 콘솔 오류 0

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 종료 0
- [ ] 금지-04: SKILL.md frontmatter 에서 name 필드 누락 금지
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=frontmatter` 종료 0

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — `at` 검사는 기존 사진 검사가 돌려준 크기를 쓰고, 확대는 기존 확대 창 하나를 넓힌다
    측정: `grep -c 'def check_image' $K/scripts/build_report.py` 가 1 · `grep -c 'def png_size' $K/scripts/build_report.py` 가 1 · `grep -c '<dialog' $K/templates/report.html` 가 1

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 대신 스크립트-05 단위 테스트와 `python3 scripts/validate-plugin.py flutter-toolkit` 종료 0 을 본다)
- [ ] 진단-02: 바뀐 마크다운 파일(`$K/SKILL.md` · `$K/references/record-format.md`)의 마크다운 경고가 0 건이다
    측정: 범위 경계의 markdownlint-cli2 명령에 두 파일을 넘겨 `Summary: 0 issues`
    양성 대조: SKILL.md 끝에 `#제목` 줄(샵 뒤 띄어쓰기 없음)을 붙인 임시 사본을 같은 명령에 넘기면 MD018 1 건 (봉인 전 실측 `Summary: 1 issue in 1 file`)
- [ ] 진단-03: N/A (commands.test 는 scripts/release.sh 실행 — 이번 변경과 무관. 콘솔 오류는 스크립트-05 단위 테스트 출력 `OK` 로 본다)
- [ ] 진단-04: N/A (구동할 앱 · 서버 없음 — 산출물은 스크립트와 정적 HTML. 브라우저 확인은 구조-02 · 구조-03 이 맡는다)
