---
feature: "flutter-scenario-report — 시나리오 테스트 기록을 캡처와 함께 HTML 보고서로 만드는 flutter-toolkit 스킬"
slug: flutter-scenario-report
created: "2026-09-25 15:42"
complexity: "복잡"
conditions: 32
status: done
owner_session: e6978555-fef9-4611-a5d0-f6a8085b3924
conditions_digest: sha256:be16c86ab07f4154
locked_at: "2026-09-25 15:55"
---

<!-- markdownlint-disable-file MD041 -->

## 배경

- 사용자가 Flutter Playwright MCP 로 앱을 테스트하며 찍은 캡처와 시나리오를 문서로 받고 싶어 했다. 여러 시안을 거쳐 `fit-pal/.mcp_screenshots/report-layouts/layout-clean.html` 을 최종으로 골랐다 ("이걸로 진행해", 2026-09-25). 이 시안은 두 스프린트 `scenario-report-clean-rail` · `scenario-report-rail-scenario-status` 에서 QA APPROVE 를 받았다.
- 사용자 결정 (2026-09-25 대화 질문 답): 스킬 이름 `flutter-scenario-report` · 범위는 시나리오 작성 → MCP 실행·캡처 → 판정 기록 → HTML 보고서 · 사진은 케이스 폴더에 파일로 두고 HTML 이 가리킨다 · 마무리는 릴리스까지.
- 앞선 결정: 다시 돌리면 덮어쓴다 · 결과물은 커밋하지 않는다 · 결과 폴더는 앱 프로젝트의 `.mcp_screenshots/test-evidence/` (fit-pal `.gitignore:39` 의 `.mcp_screenshots/` 로 빠진다) · 판정 표시는 ✅ ❌ 만 쓴다 · 시나리오는 Gherkin 공식 한국어 키워드.
- 설계: 테스트하는 Claude 가 케이스 폴더마다 `record.json` 을 적고, 스킬의 `scripts/build_report.py`(파이썬 표준 라이브러리만)가 모든 케이스를 검사한 뒤 `test-evidence/index.html` 하나로 만든다. 시나리오 판정은 스크립트가 단계 판정에서 계산한다. 화면 구조와 스타일은 승인된 시안을 그대로 옮긴다 — 같은 측정 스크립트로 같은 값이 나와야 한다.
- 복잡도 4 축 판정:

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 3 (스킬 문서 · 생성 스크립트 · 레포 문서·검사) |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 새 스킬 진입점과 새 기록 형식 `record.json` |
| 소비면 존재 | 반대편이 있는가 | 예 — 기록 형식을 설명하는 쪽(`record-format.md` · SKILL.md)과 읽는 쪽(`build_report.py`) |
| 회귀 위험 | 기존 동작이 깨질 경로가 있는가 | 예 — README 자동 표, 레포 `CLAUDE.md` 스킬 수, 플러그인 검사 V1~V10 |

- "공개 계약 변경 = 예" 이면서 "소비면 = 예" 라 **복잡**이다. Counterpart 조건: 설명하는 쪽 AR-06, 읽는 쪽 ER-01 · AR-06.
- 설정 리터럴 대조:

| config key | project.yaml 값 | 계약에 쓴 값 |
| ---------- | --------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | 제외 없음 |
| `contract_categories` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 네 섹션 그대로 |
| `anti_patterns` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-02 · AP-03 · AP-04 그대로 |

## GAP 분석

- Pre-Edit Audit (대상 파일을 실제로 읽은 근거):

| 대상 파일 | 실제 Read 증거 | 발견한 기존 갭 | 조건화 |
| --------- | -------------- | -------------- | ------ |
| `flutter-toolkit/skills/flutter-ui-verify/SKILL.md` | `:4`~`:8` 트리거 "화면 확인해줘" · "스크린샷으로 확인" · "UI 검증", `:17` 캡처 경로가 없으면 확인했다고 말하지 않는다, `:38` 캡처 채널은 `project-detection.md` 가 고른다 | 형제 스킬과 트리거가 겹치면 안 된다. 캡처 채널 감지를 새로 만들지 말고 재사용해야 한다 | SK-02 · SK-04 · RE-02 |
| `flutter-toolkit/references/project-detection.md` | Step 8 `:132`~`:152` — `VISUAL_CHANNEL = mcp:<서버명>` 을 `.mcp.json` 등에서 읽는다, `:147` 도구 이름 추측 금지 | 새 스킬은 이 감지를 가리켜야 한다 | RE-02 |
| `flutter_playwright` MCP `image_file_saver.dart` | `:34` 폴더 이름 `.mcp_screenshots`, `:68` 파일 이름 `screenshot-<시각>.png`, `:162` · `:167` `screenshot-` 이 든 24 시간 넘은 파일 삭제 | 캡처를 찍자마자 케이스 폴더로 복사해야 한다 | SK-04 |
| `flutter-toolkit/README.md` | `:7`~`:29` `AUTO:skills` 표 (스킬 19 행), `:1` 제목 `v0.5.0` (plugin.json 0.8.0 과 이미 어긋남 — 이번 범위 밖) | 새 스킬 행이 없다 | AR-08 |
| `CLAUDE.md` | `:11` "스킬 19종", `:142` "(19종)", `:164` `/flutter-ui-verify` 행 | 새 스킬 행과 수가 없다 | AR-08 |
| `flutter-toolkit/evals/evals.json` | 항목 형식 `{"id","skill","prompt","expected_output","assertions":[{"text","type"}]}`, 항목 22 개 | 새 스킬 평가 항목이 없다 | AR-07 |
| 승인 시안 빌더 `$SP/build_clean.py` · `$SP/build_layouts.py` | 케이스 자료 구조 `CASES` (`build_layouts.py:17`~`:84`), 옆 칸·시나리오 목록·스크롤 스크립트 (`build_clean.py`) | 시안은 사진을 JPEG 로 줄여 HTML 에 넣고 요소 ID 오버레이를 붙인다 — 스킬 결과물에는 둘 다 없어야 한다 | AR-03 · AR-04 |

- 착수 전 실측 (봉인 전): `python3 scripts/validate-plugin.py flutter-toolkit` V1~V10 전부 OK · `Exit: 0` (스킬 19 개) · `python3 scripts/sync-docs.py --check-only` "모든 README가 동기화 상태입니다." · `git diff --name-only origin/main...feat/flutter-scenario-report` 0 줄 · `diff -rq "$EV" "$SP/backup-test-evidence"` 0 줄.

## 범위 경계

- 측정 변수 (모든 조건 공통):

```bash
WT=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/flutter-scenario-report
SKILL="$WT/flutter-toolkit/skills/flutter-scenario-report"
SP=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/e6978555-fef9-4611-a5d0-f6a8085b3924/scratchpad
EV=/Users/jackson/Hub/10_Dev/fit-pal/.mcp_screenshots/test-evidence
```

- **읽기 전용 원본 — 지우거나 옮기거나 고치지 마라:** `$EV` 아래 기존 파일 10 개(README.md 3 · PNG 7)는 git 에서 빠진 캡처 원본이다. 이번 스프린트는 그 폴더에 `index.html` 과 케이스 폴더마다 `record.json` 을 **더하기만** 한다. 백업은 `$SP/backup-test-evidence/`.
- 측정 M · M2 는 앞 두 스프린트가 봉인한 측정 스크립트 `$SP/measure_clean.js` (지문 `8e64b6678eaaad1d`) · `$SP/measure_rail2.js` (지문 `f2bf1aef7d50c848`) 다. 레포 `node_modules/playwright-core` 1.58.2 의 머리 없는 Chromium 으로 잰다. 이번 스프린트에서 이 둘을 고치지 않는다.
- 승인 시안 `fit-pal/.mcp_screenshots/report-layouts/layout-clean.html` 의 측정값 (봉인 전 실측, AR-03 의 기대값):

```text
M2  W1440x900 rail_scn_status=✅❌-|✅✅ card_status=✅❌-|✅✅ rail_marks=✅1❌1|✅2❌0 card_marks=✅1❌1|✅2❌0 rail_extra_verdict=0/2 rail_fail_color_ok=5/5 spy=c0:1,2,3 c1:1,2 spy_visual=true click_jump=2/2 head_mid=2/2 head_at_top=0/2
M2  console_errors=0 console_probe=1
M   W1440x900 rail_top=160 rail_follow_diff=0 rail_switch=true card2_bottom=770 shot_h=594 steps_sig=14:95d99243 card_style=14px|rgb(255,255,255) fail_bg=rgb(255,245,245) pass_color=rgb(26,127,55) fail_color=rgb(207,34,46) run_marker_closed="▸"@none run_marker_open="▸"@matrix(0,1,-1,0,0,0) scroll_w=1440
M   W1281x800 mode=rail steps_min_w=353 scroll_w=1281 · W1280x800 mode=bar scroll_w=1280 · W390x844 bar_top=0 bar_h=80 chip_rows=1 last_chip_reachable=true scroll_w=390 · console_errors=0 console_probe=1
```

- 기록 파일에 들어갈 fit-pal 두 케이스(TC-002 실패 · TC-001 통과)의 내용은 승인 시안의 `CASES` 와 같다. 구현자가 `$EV/TC-002-appoint-vice-leader/record.json` · `$EV/TC-001-transfer-leader-cancel/record.json` 로 옮겨 적는다.
- 변경 파일 허용 집합 (AR-10 의 기대 집합, 이 목록이 유일한 열거처다): `.harness/sprint-contract-flutter-scenario-report.md` · `.harness/sprint-feedback-flutter-scenario-report.md` · `CLAUDE.md` · `flutter-toolkit/README.md` · `flutter-toolkit/evals/evals.json` · `flutter-toolkit/evals/scenario-report/test_build_report.py` · `flutter-toolkit/skills/flutter-scenario-report/SKILL.md` · `flutter-toolkit/skills/flutter-scenario-report/references/record-format.md` · `flutter-toolkit/skills/flutter-scenario-report/scripts/build_report.py`. 조건을 사이드카로 고치게 되면 `.harness/sprint-amendments-flutter-scenario-report.md` 도 허용한다 (생겼을 때만).
- 이번 스프린트 밖: 버전 올리기와 릴리스(`plugin.json` · `marketplace.json`)는 이 계약의 QA 가 APPROVE 된 뒤 PR 을 합치고 `main` 에서 `bash scripts/release.sh flutter-toolkit minor` 로 한다. `flutter-toolkit/README.md:1` 의 `v0.5.0` 어긋남은 이미 있던 것이라 이번에 고치지 않는다.
- 오라클 해소: SK-01 · SK-03 · SK-04 · AR-08 · AR-09 · DG-06 — 산출물이 문서 자체라 문서 글자를 재는 것이 곧 산출물을 확인하는 일이다. SK-01 · AR-08 은 글자 확인에 더해 `validate-plugin.py` · `sync-docs.py` 를 실제로 돌린다. 스킬의 동작(검사·보고서 생성·화면)은 DG-05 단위 테스트와 AR-03 브라우저 측정이 실제로 실행해 잰다.
- 교차 진단 반영 (qa-evaluator, 봉인 전): (1) AR-04 기대값 `8 0` 이 승인 시안에서도 `7 0` 이라 늘 떨어졌다 — 확대 사진이 사진 파일 7 개에 이미 들어 있다 → `7 0` 으로 고침 (2) AR-10 허용 집합에 개정 사이드카가 없어 정해진 절차를 따르면 AR-10 이 깨졌다 → 생겼을 때만 허용 (3) SK-01 의 `awk` 구간이 `argument-hint` 줄의 따옴표까지 트리거로 셌다 → 구간을 좁힘. 그 밖에 봉인 전 실측값 · 네 스크립트 지문 · SK-02 음성 대조 · DG-07 형태를 평가자가 직접 재현해 확인했다.
- 커버리지 해소: AR-01 — 세 파일 이름은 측정 절의 `find` 기대 출력에 그대로 있다. 명령 전체가 백틱 하나라 검출기가 따로 못 읽었다.
- 커버리지 해소: AR-03 — `$EV/index.html` 은 측정 절의 두 `node` 명령 인자로 있고, `record.json` 은 그 보고서를 만든 입력(Given)이라 따로 재지 않는다.
- 커버리지 해소: AR-08 — `flutter-toolkit/README.md` · `CLAUDE.md` · `/flutter-scenario-report` 는 측정 절의 `grep` 명령 안에 있다.
- 커버리지 해소: DG-02 — 네 파일은 `md_count.sh` 가 이름을 박아 잰다 (스크립트 본문의 `for pair in` 줄).
- 측정 스크립트 지문 (봉인 전 실측): `$SP/md_count.sh fce3ec13de811372` · `$SP/md_base.sh 16ecdd056b0ed059`. QA 는 이 지문이 같은지 먼저 본다.

## Skill

- [ ] SK-01: 스킬 파일 `$SKILL/SKILL.md` 가 있고 frontmatter 의 `name` 이 `flutter-scenario-report`, `user-invocable` 이 `true`, `argument-hint` 가 비어 있지 않으며, `description` 에 하는 일 · 트리거 문구 3 개 이상 · "트리거하지 않는다" 로 끝나는 비트리거 문장이 1 개 이상 있다 [exact] (측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=frontmatter` 가 `20 skills` 를 포함한 OK, `awk '/^description:/{f=1;next} /^argument-hint:/{f=0} f' "$SKILL/SKILL.md" | grep -c '트리거하지 않는다'` 이 1 이상 (description 다음 줄부터 argument-hint 앞줄까지만 본다), 같은 구간의 `"…"` 따옴표 트리거 문구 수 `grep -o '"[^"]*"' | wc -l` 이 3 이상)
- [ ] SK-02: 새 스킬의 트리거 문구가 기존 flutter-toolkit 스킬과 겹치지도 서로 부분 문자열이지도 않다 [exact] (측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=triggers` 가 OK. 음성 대조: 봉인 전 사본 실험 — 새 스킬 description 에 형제 트리거 `"화면 확인해줘"` 를 넣으면 V4 가 FAIL 한다, 구현 뒤 임시 사본으로 재현)
- [ ] SK-03: SKILL.md 의 Process 가 아래 여섯 단계를 이 순서로 담는다 — (1) 프로젝트 감지 (2) 시나리오 작성과 사용자 확인 (3) 실행·캡처 (4) 판정 기록 (5) 보고서 만들기 (6) 완료 전 대조. 각 단계는 `### N.` 제목 줄로 시작한다 [structural, enumerated] (측정: `grep -nE '^### [1-6]\. ' "$SKILL/SKILL.md"` 가 6 줄이고 번호가 1→6 순서이며, 제목 줄에 차례로 `감지` · `시나리오` · `캡처` · `판정` · `보고서` · `대조` 가 들어 있다)
- [ ] SK-04: SKILL.md 의 Gotchas 가 5 개 이상이고, 그중 아래 다섯 내용이 각각 한 항목씩 있다 — (a) MCP 캡처는 24 시간 뒤 지워지니 찍자마자 케이스 폴더로 복사 (b) 같은 위젯 캡처는 같은 파일 이름으로 덮어써진다 (c) 판정은 캡처를 보고 짐작하지 않고 도구가 돌려준 관측값으로 적는다 (d) `test-evidence` 는 git 밖 원본이라 지우지 않는다 (e) `flutter-ui-verify` 와의 경계 [structural, enumerated] (측정: `awk '/^## Gotchas/{f=1;next} /^## /{f=0} f && /^- /' "$SKILL/SKILL.md"` 줄 수 5 이상, 그 출력에서 `24 시간` · `덮어` · `관측` · `지우지` · `flutter-ui-verify` 가 각각 1 번 이상 나온다)
- [ ] SK-05: SKILL.md 가 300 줄 이하다 [exact] (측정: `wc -l < "$SKILL/SKILL.md"` 이 300 이하)

## Script

- [ ] SC-01: 이 PR 브랜치는 버전을 손으로 바꾸지 않는다 — 버전은 릴리스 스크립트가 바꾼다 [exact] (측정: `git diff --name-only origin/main...feat/flutter-scenario-report -- flutter-toolkit/.claude-plugin/plugin.json .claude-plugin/marketplace.json | wc -l` 이 0. Given: 구현 커밋 완료 후)

## Error

- [ ] ER-01: Given 잘못된 기록, When `python3 "$SKILL/scripts/build_report.py" <루트>` 를 돌리면, Then 종료 코드 1 · 오류 줄에 케이스 폴더 이름과 문제 필드가 찍히고 `index.html` 을 쓰지 않는다. 잘못된 기록 열 가지 — 기록 JSON 문법 오류 · 모르는 키(오타) · 필수 키 누락 · 없는 사진 파일 · 규칙에 안 맞는 사진 이름(대문자·공백) · 한국어 Gherkin 키워드가 아닌 `kw` · `pass`/`fail` 이 아닌 `result` · `만일` 처럼 확인 단계가 아닌 곳의 `result` · `seen` 없는 `result` · 건너뛰지 않았는데 판정한 단계가 없는 시나리오 [exact, enumerated] (측정: DG-05 의 단위 테스트가 열 가지를 각각 한 테스트로 확인한다 — `python3 -m unittest discover -s "$WT/flutter-toolkit/evals/scenario-report" -v 2>&1 | grep -c '^test_error_'` 이 10 이상이고 전부 `ok`. 음성 대조: 스크립트의 모르는 키 검사를 지운 사본으로 돌리면 모르는 키 테스트가 FAIL — 구현자가 QA 전에 한 번 실측해 보고에 붙인다)
- [ ] ER-02: 케이스 폴더에 기록이 가리키지 않는 PNG 가 있으면 경고 줄을 찍되 종료 코드는 0 이고, 루트에 `record.json` 을 가진 케이스 폴더가 하나도 없으면 종료 코드 1 이다 [exact] (측정: DG-05 단위 테스트 `test_warn_unreferenced_png` · `test_error_empty_root` 가 `ok`)
- [ ] ER-03: `--check` 로 돌리면 검사만 하고 파일을 하나도 만들거나 바꾸지 않는다 [exact] (측정: DG-05 단위 테스트 `test_check_writes_nothing` 이 `ok` — 실행 전후 루트의 파일 목록과 수정 시각이 같다)

## Architecture

- [ ] AR-01: 스킬 폴더 안 파일이 정확히 세 개 — `SKILL.md` · `references/record-format.md` · `scripts/build_report.py` — 다 [exact, enumerated] (측정: `(cd "$SKILL" && find . -type f -not -name '.DS_Store' | sort | paste -sd' ' -)` 이 `./SKILL.md ./references/record-format.md ./scripts/build_report.py`)
- [ ] AR-02: `build_report.py` 는 파이썬 표준 라이브러리만 가져다 쓴다 [exact] (측정: `python3 -c "import ast,sys;t=ast.parse(open('$SKILL/scripts/build_report.py',encoding='utf-8').read());m={(n.module or '').split('.')[0] for n in ast.walk(t) if isinstance(n,ast.ImportFrom)}|{a.name.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.Import) for a in n.names};print(sorted(x for x in m if x and x not in sys.stdlib_module_names))"` 이 `[]`)
- [ ] AR-03: Given fit-pal 두 케이스를 `record.json` 으로 적고 스크립트로 만든 `$EV/index.html`, When 측정 M2 · M 을 돌리면, Then 범위 경계의 승인 시안 값과 같다 — M2 줄의 11 키 전부 같은 값, M 의 `W1440x900` 줄 `rail_top` 120~200 · `rail_follow_diff=0` · `rail_switch=true` · `card2_bottom` 900 이하 · `shot_h=594` · `steps_sig=14:95d99243` · `card_style=14px|rgb(255,255,255)` · `fail_bg` · `pass_color` · `fail_color` · 두 펼침 표시 값이 같고, `W1281x800 mode=rail` 에 `steps_min_w` 300 이상, `W1280x800 mode=bar`, `W390x844` 의 `bar_top=0` · `bar_h` 100 이하 · `chip_rows=1` · `last_chip_reachable=true`, 네 폭의 `scroll_w` 가 폭과 같다 [exact, enumerated] (측정: `node "$SP/measure_rail2.js" "$EV/index.html"` · `node "$SP/measure_clean.js" "$EV/index.html"`. FAIL: 스킬이 만든 보고서가 승인된 시안과 다르게 그려진다)
- [ ] AR-04: 보고서가 사진을 HTML 안에 넣지 않고 케이스 폴더의 파일을 가리키며, 가리키는 파일이 모두 있고, 시안 전용 요소 ID 오버레이가 없다 [exact] (측정: `grep -c 'data:image' "$EV/index.html"` 이 0, `grep -c 'id-toggle' "$EV/index.html"` 이 0, `python3 -c "import re,os;h=open('$EV/index.html',encoding='utf-8').read();s=re.findall(r'<img[^>]*src=\"([^\"]+)\"',h);print(len(s),sum(not os.path.exists(os.path.join('$EV',x)) for x in s))"` 이 `7 0` — 확대 사진을 포함한 사진 파일 7 개가 한 번씩이라 첫 값 7, 없는 파일 수인 둘째 값 0. 확대 보기 창의 `<img>` 는 처음엔 `src` 가 없어 세지 않는다 — 승인 시안에서 봉인 전 실측 7)
- [ ] AR-05: 같은 기록으로 두 번 돌리면 `index.html` 이 바이트까지 같고, 루트에 `index.html` 말고 새 파일이 생기지 않는다 [exact] (측정: DG-05 단위 테스트 `test_rerun_is_identical` 이 `ok`)
- [ ] AR-06: 기록 형식 문서와 스크립트가 서로 맞다 — (a) `record-format.md` 의 첫 ```json 예시를 케이스 폴더에 `record.json` 으로 두고 예시가 가리키는 사진을 1×1 PNG 로 만들어 `--check` 하면 종료 코드 0, (b) 스크립트가 받는 모든 키가 `record-format.md` 에 백틱으로 적혀 있다 [exact] (측정: DG-05 단위 테스트 `test_format_doc_example_passes` · `test_format_doc_lists_every_key` 가 `ok`. `test_format_doc_lists_every_key` 는 스크립트를 모듈로 읽어 허용 키 집합을 꺼내 문서와 대조한다)
- [ ] AR-07: `flutter-toolkit/evals/evals.json` 이 올바른 JSON 이고, `skill` 이 `flutter-scenario-report` 인 항목이 1 개 이상, 그 항목의 `assertions` 가 4 개 이상이다 [exact] (측정: `python3 -c "import json;d=json.load(open('$WT/flutter-toolkit/evals/evals.json',encoding='utf-8'));x=[e for e in d['evals'] if e.get('skill')=='flutter-scenario-report'];print(len(x),min(len(e['assertions']) for e in x) if x else 0)"` 이 첫 값 1 이상, 둘째 값 4 이상)
- [ ] AR-08: 레포 문서가 새 스킬을 담는다 — `flutter-toolkit/README.md` 자동 표에 `flutter-scenario-report` 행, `CLAUDE.md` 의 flutter-toolkit 스킬 표에 `/flutter-scenario-report` 행이 있고, `CLAUDE.md` 의 flutter-toolkit 스킬 수 표기 두 곳이 `20종` 이며, `sync-docs` 가 동기화 상태다 [exact, enumerated] (측정: `grep -c 'flutter-scenario-report' "$WT/flutter-toolkit/README.md"` 1 이상, `grep -c '^| .*/flutter-scenario-report' "$WT/CLAUDE.md"` 이 1, `grep -cE 'flutter-toolkit.*(19|20)종' "$WT/CLAUDE.md"` 과 `grep -cE 'flutter-toolkit.*20종' "$WT/CLAUDE.md"` 이 둘 다 2, `(cd "$WT" && python3 scripts/sync-docs.py --check-only)` 마지막 줄이 `모든 README가 동기화 상태입니다.`)
- [ ] AR-09: SKILL.md 가 결과 폴더를 git 에서 빼는 확인과, 빠져 있지 않을 때 `.gitignore` 에 `.mcp_screenshots/` 를 더하는 절차를 담는다 [structural] (측정: `grep -c 'git check-ignore' "$SKILL/SKILL.md"` 과 `grep -c '\.mcp_screenshots/' "$SKILL/SKILL.md"` 이 둘 다 1 이상)
- [ ] AR-10: 이 브랜치가 바꾼 파일이 범위 경계의 허용 집합 안에만 있다 [exact] (측정: `git -C "$WT" diff --name-only origin/main...feat/flutter-scenario-report` 출력의 모든 줄이 범위 경계의 허용 집합(9 경로, 사이드카가 생겼으면 10 경로) 중 하나다. Given: 구현 커밋 완료 후. 상한은 가지 끝 `feat/flutter-scenario-report` 이고 `HEAD` 가 아니다. 봉인 전 실측 0 줄)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json 에서 읽어야 한다 (측정: `grep -rnE 'hardcoded.*version' "$SKILL" "$WT/flutter-toolkit/evals/scenario-report" | wc -l` 이 0)
- [ ] AP-02: force push 금지 (측정: 이번 스프린트의 셸 기록에 `git push --force` · `git push -f` 가 없다 — 구현자 보고에 `git push` 명령 전문을 붙인다)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 가 `0 bare`)
- [ ] AP-04: SKILL.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=frontmatter` 가 OK)

## Reusability

- [ ] RE-01: N/A (보고서 생성은 CLI 스크립트 하나이고 다른 스킬이 가져다 쓸 공개 함수가 없다 — 테스트가 모듈로 읽는 것은 허용 키 집합 확인용이다)
- [ ] RE-02: 캡처 채널과 MCP 서버 이름 감지를 새로 만들지 않고 기존 `references/project-detection.md` 를 가리킨다 [exact] (측정: `grep -c 'project-detection.md' "$SKILL/SKILL.md"` 이 1 이상, `python3 scripts/validate-plugin.py flutter-toolkit --check=refs` 가 OK)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 scripts/release.sh 만 잰다 — 이번 변경과 교집합 0 개. 측정: `git -C "$WT" diff --name-only origin/main...feat/flutter-scenario-report | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 바꾼 마크다운 파일 네 개(`SKILL.md` · `record-format.md` · `flutter-toolkit/README.md` · `CLAUDE.md`)의 편집기 조건 마크다운 검사에서 이번 변경이 새 경고를 만들지 않는다 [exact, enumerated] (측정: `"$SP/md_count.sh" "$WT"` 가 `SKILL.md 0` · `record-format.md 0` · `CLAUDE.md` 77 이하 · `README.md` 10 이하. 77 과 10 은 `"$SP/md_base.sh" "$WT"` 로 잰 `origin/main` 판의 경고 수다 — 봉인 전 실측. 두 스크립트는 편집기와 같은 조건(markdownlint-cli2 0.23.2, `MD013` 끔)으로 잰다. 양성 대조: 봉인 전 지금 브랜치에서 `md_count.sh` 는 새 두 파일에 `MISSING` 을 찍는다 — 파일이 없으면 통과로 읽히지 않는다)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 는 릴리스 스크립트 실행 — 이번 변경과 교집합 0 개. 측정: DG-01 과 같다. 대신 DG-05 의 단위 테스트가 이 스프린트의 테스트다)
- [ ] DG-04: `$EV/index.html` 을 네 화면 크기로 열었을 때 콘솔 오류와 페이지 오류가 0 건이다 [exact] (측정: 측정 M 마지막 줄 `console_errors=0 console_probe=1`, 측정 M2 둘째 줄 `console_errors=0 console_probe=1`)
- [ ] DG-05: 단위 테스트가 전부 통과하고 12 개 이상이며, 플러그인 검사가 전부 OK 다 [exact] (측정: `python3 -m unittest discover -s "$WT/flutter-toolkit/evals/scenario-report" -v` 마지막에 `OK` 와 `Ran N tests` 의 N 이 12 이상, `(cd "$WT" && python3 scripts/validate-plugin.py flutter-toolkit)` 이 `Exit: 0`, `python3 -m py_compile "$SKILL/scripts/build_report.py"` 종료 코드 0. 음성 대조: ER-01 과 같다)
- [ ] DG-06: SKILL.md · record-format.md 가 한다체로 쓰였고 번역투·음역 목록이 0 건이다 [exact] (측정: `grep -cE '(합니다|습니다|세요)[.)]?$' <파일>` 두 파일 모두 0, `grep -cE '(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)|핫 ?리로드|쿼리|리셋|디폴트' <파일>` 두 파일 모두 0. 양성 대조: 임시 사본에 `버튼이 표시된다.` 한 줄을 넣으면 1)
- [ ] DG-07: `$EV` 의 기존 원본 10 개가 그대로이고, 더해진 것은 `index.html` 과 두 `record.json` 뿐이다 [exact] (측정: `diff -rq "$SP/backup-test-evidence" "$EV"` 출력이 정확히 3 줄이고 전부 `Only in <$EV 쪽 경로>` 로 시작하며 파일 이름이 `index.html` · `record.json` · `record.json` 이다. 봉인 전 실측 0 줄)
