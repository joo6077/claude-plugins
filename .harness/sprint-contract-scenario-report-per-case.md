---
feature: "flutter-scenario-report — 케이스별 보고서 · 단계에 의도와 조작 순서 · 고친 뒤 다시 돌리기 · 시나리오 작성 규칙"
slug: scenario-report-per-case
created: "2026-09-30 12:10"
complexity: "복잡"
conditions: 26
status: done
owner_session: 97f28e34-99ea-4a74-9baa-3288b7964458
conditions_digest: sha256:1cc41eb17fedfa7c
measurement_digest: sha256:4a00a961f2baa29f
locked_at: "2026-09-30 12:17"
---

## 배경

- 사용자 요구 세 가지(2026-09-30 대화): (1) 지금 보고서는 모든 케이스를 한 `index.html` 에 이어 붙인다 — 케이스별로 나눈다. 실행할 때마다 새로 만드는 게 아니라 케이스별이다. (2) 단계마다 의도와 실제 조작 순서를 둘 다 적는다. (3) 실패하면 고친 뒤 다시 돌린 결과를 남긴다. 고치는 일은 이 스킬이 하지 않는다.
- 사용자 결정: 이전 차수는 남기지 않는다. 다시 돌리면 같은 케이스 폴더를 새 결과로 덮어쓴다. 차수 폴더(`1/` · `2/`)는 만들지 않는다.
- 시나리오 작성 규칙의 근거는 Codex 조사(Cucumber 공식 문서 · gherkin-languages.json · Flutter finder 소스 · 2025 논문)다. 핵심 인용 두 개(`3-5 steps` · `known state` · `observable`, 한국어 키워드 목록)는 원문을 직접 다시 확인했다.
- Codex 가 초안을 검토해 12 개를 짚었고 반영했다 — `do` 범위를 첫 `그러면` 앞 행동 단계 전부로, `do` 를 목록으로, 실패 즉시 멈춤 대신 기존 규칙 유지, `fix.commit` 선택, 전부 검사한 뒤에만 HTML 쓰기, 작성 규칙은 개수 대신 주제 목록.

## 리서치 소스

- 조사 결과 원문: 세션 임시 폴더 `scenario-research-out.md` (세션 한정). 구현이 참조 파일로 옮긴다.
- Cucumber Gherkin Reference — <https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/docs/gherkin/reference.md>
- Writing better Gherkin — <https://github.com/cucumber/website/blob/aeb31cd2f1e05840e36a07b46402edfe5586a59f/docs/bdd/better-gherkin.md>
- gherkin-languages.json ko — <https://github.com/cucumber/gherkin/blob/907e36b3d91dfa2a0a9c2b5c102100b6707fa84d/gherkin-languages.json>
- Acceptance Test Generation with LLMs (2025) — <https://arxiv.org/abs/2504.07244>

## GAP 분석

- `build_report.py:239` 가 `*/record.json` 을 모아 `:268` 에서 루트 `index.html` 하나에 모든 케이스를 쓴다 — 요구 (1) 의 원인
- `STEP_FIELDS`(`build_report.py:30`)에 조작 순서를 담을 키가 없다. 조작은 케이스 단위 `run` 에만 몰려 있다 — 요구 (2)
- 다시 돌린 기록이라는 표시가 없다. 기록이 가리키지 않는 캡처는 경고만 찍고 지우지 말라고 한다(`SKILL.md` Gotcha) — 요구 (3) 와 사용자 결정에 맞춰 바꾼다
- `SKILL.md` 2 단계에 시나리오를 잘 쓰는 기준이 3~5 단계 · 관측 가능한 확인 두 줄뿐이다
- Gotcha 가 데이터베이스 조회를 화면 관측과 같은 급의 관측값으로 둔다 — 공식 문서는 사용자에게 보이는 결과를 요구한다
- 기준값(2026-09-30 12:08, 커밋 `01b1cace`): 단위 테스트 24 개 통과 · `python3 scripts/validate-plugin.py flutter-toolkit` 종료 0 · 두 문서 마크다운 경고 0 · `python3 scripts/sync-docs.py flutter-toolkit --check-only` 종료 0

## 범위 경계

```text
# sprint-scope
flutter-toolkit/skills/flutter-scenario-report/
flutter-toolkit/evals/scenario-report/
flutter-toolkit/README.md
.harness/
```

- 하지 않는 것: 고치는 일을 이 스킬 안에 넣기 · 이전 차수 기록 보관과 비교 화면 · 버전 올리기와 릴리스 · 루트 `README.md` 수정
- 옛 기록(단계에 `do` 가 없는 `record.json`)은 새 검사에서 막힌다. 다시 돌려 새 형식으로 쓰면 된다 — 옛 형식 호환은 두지 않는다
- 측정 공통 정의: `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/scenario-report-per-case` · `K=$W/flutter-toolkit/skills/flutter-scenario-report` · `T=$W/flutter-toolkit/evals/scenario-report` · 시작 커밋 `BASE=01b1cace` · 끝 `TIP=$(git -C $W rev-parse feat/scenario-report-per-case)` · 단위 테스트 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v` (`$W` 에서)
- 오라클 해소: SK-01 · SK-02 · SK-05 · SK-06 — 산출물이 스킬 안내문 자체라 문구 존재가 곧 결과다. 안내가 가리키는 동작(`do` · `fix` · 케이스 페이지)은 SC 조건이 테스트로 실행해 잰다
- 오라클 해소: SC-06 · SC-07 — 측정이 단위 테스트 실행 종료 코드와 `OK` 출력이다. 문구 확인이 아니다
- 마크다운 경고 측정: 세션 임시 폴더 `mdlint/node_modules/.bin/markdownlint-cli2 --config mdlint/cfg.markdownlint-cli2.jsonc <파일>` (markdownlint-cli2 0.23.2, MD013 끔 — 편집기 확장과 같은 설정)

## Skill

- [ ] SK-01: 실패 뒤 흐름이 스킬 본문에 적혀 있다 — 「고치는 일은 이 스킬이 하지 않는다」고 쓰고, 화면 결함은 `flutter-ui-verify`, 원인을 모르면 `superpowers:systematic-debugging` 으로 넘기며, 고친 뒤 같은 케이스 ID 로 다시 부르면 그 케이스의 시나리오 전부를 다시 돌려 같은 케이스 폴더에 덮어쓰고, 기록 머리에 `fix` 를 적는다 [exact]
    측정: `grep -cF` 로 `$K/SKILL.md` 에서 `고치는 일은 이 스킬이 하지 않는다` · `flutter-ui-verify` · `superpowers:systematic-debugging` · `같은 케이스 ID 로 다시 부르면` · `시나리오 전부를 다시 돌린다` · `` `fix` `` 가 각 1 이상
    음성 대조: 넷째 · 다섯째 문구 중 하나를 지운 사본에서 그 grep 이 0
- [ ] SK-02: 앞 시나리오 결함 때문에 다음 시나리오를 진행할 수 없을 때만 멈추고, 서로 독립된 시나리오는 계속 돌린다는 규칙이 유지된다 — 실패 한 번에 전부 멈추라는 문구는 없다 [exact]
    측정: `grep -cF '앞 시나리오의 결함 때문에 다음 시나리오를 진행할 수 없으면 멈추고' $K/SKILL.md` 가 1 · `grep -cE '실패하면 (바로|즉시) 멈' $K/SKILL.md` 가 0
- [ ] SK-03: 2 단계(시나리오 작성과 사용자 확인)가 `references/scenario-writing.md` 를 따르라고 하고, 사용자에게 보여 주는 확인 표 머리 줄에 `의도` 와 `조작 순서` 두 칸이 있다 [exact]
    측정: `awk '/^### 2\./,/^### 3\./' $K/SKILL.md` 출력에서 `references/scenario-writing.md` 를 담은 줄 1 이상, `^\| 시나리오 \|` 로 시작하는 표 머리 줄에 `의도` 와 `조작 순서` 가 함께 있다
- [ ] SK-04: `references/scenario-writing.md` 가 여섯 주제를 각각 `## ` 절로 다루고, 절마다 출처 `https://` 주소 1 개 이상 · `좋은 예` · `나쁜 예` 가 있다. 여섯 주제는 절 제목 낱말로 판정한다 — `의도` · `먼저` · `그러면` · `숨김` · `사라` · `질문` [exact, enumerated]
    측정: 파이썬으로 파일을 `^## ` 기준으로 쪼개어 여섯 낱말마다 제목에 그 낱말이 든 절을 찾고, 그 절 본문에 `https://` · `좋은 예` · `나쁜 예` 가 모두 있는지 본다. 빠진 주제 · 빠진 항목 목록이 빈 목록이면 PASS
    양성 대조: `좋은 예` 를 하나 지운 사본에서 빠진 항목 목록이 1 이상
- [ ] SK-05: 관측값 Gotcha 가 화면에 보이는 결과를 먼저 적고 데이터베이스는 보조 증거라고 바뀐다 [exact]
    측정: `grep -cF '화면에 보이는 결과를 먼저' $K/SKILL.md` 1 이상 · `grep -cF '보조 증거' $K/SKILL.md` 1 이상 · 옛 문구 `grep -cF '위젯 찾기 · 보임 확인 도구나 데이터베이스 조회처럼' $K/SKILL.md` 가 0
- [ ] SK-06: 다시 돌릴 때 지우는 범위가 스킬에 적혀 있다 — 그 케이스 폴더 안에서 새 기록이 가리키지 않는 캡처만 지우고, 다른 케이스 폴더나 `test-evidence` 폴더를 통째로 지우거나 비우지 않는다. 옛 "지우지 말고 사용자에게 묻는다" 문구는 없다 [exact]
    측정: `grep -cF '그 케이스 폴더 안에서 새 기록이 가리키지 않는 캡처만 지운다' $K/SKILL.md` 1 · `grep -cF '폴더를 통째로 지우거나 비우지 않는다' $K/SKILL.md` 1 이상 · `grep -cF '확인한 뒤 사용자에게 묻는다' $K/SKILL.md` 0

## Script

- [ ] SC-01: Given 케이스 폴더 두 개(`TC-000-ok` 통과 · `TC-001-transfer` 실패). When 스크립트를 돌리면 Then 두 케이스 폴더에 각자 `index.html` 이 생기고, 각 케이스 페이지는 자기 케이스 `article` 만 1 개 담으며 사진 주소가 폴더 접두 없이 `01-picker.png` 모양이다. 루트 `index.html` 에는 시나리오 본문(`<section class="scn`)이 0 개이고 `href="TC-000-ok/index.html"` · `href="TC-001-transfer/index.html"` 링크가 각 1 개다 [exact]
    측정: 단위 테스트 `test_case_pages_and_list` 통과
    음성 대조: 케이스 페이지를 쓰지 않고 루트에 전부 쓰는 사본(`BUILD_REPORT_SCRIPT`)에서 이 테스트가 FAIL
- [ ] SC-02: 루트 목록은 실패 케이스를 먼저, 같은 판정 안에서는 ID 순으로 놓고, 줄마다 ID · 제목 · 판정 표시가 있다 [exact]
    측정: 단위 테스트 `test_failing_case_comes_first` 가 루트 목록의 케이스 순서 `TC-001` → `TC-000` 을 확인하고 통과
- [ ] SC-03: 단계의 조작 순서 `do` 규칙 — (a) 첫 `그러면` 앞의 `만일` · `만약` · `그리고` · `하지만` · `단` 단계에 `do` 가 없으면 막는다 (b) `do` 는 비어 있지 않은 문자열 1 개 이상의 목록이어야 한다 — 목록이 아닌 값 · 빈 목록 · 빈 문자열 항목을 각각 막는다 (c) 판정(`result`)이 붙은 단계에 `do` 가 있으면 막는다 (d) `먼저` · `조건` 단계와, 첫 `그러면` 뒤에서 판정이 없는 단계는 `do` 가 있어도 없어도 된다 (e) 케이스 페이지에서 `do` 는 그 단계 의도 문장 아래 `<ol class="do">` 목록으로, 항목마다 `<li>` 하나로 나온다 [exact, enumerated]
    측정: 단위 테스트 `test_error_action_step_without_do` (a) · `test_error_do_not_list` · `test_error_do_empty` (b) · `test_error_do_on_checked_step` (c) · `test_do_optional_on_setup` (d) · `test_do_rendered_as_list` (e) 여섯 개 통과. `test_error_do_empty` 는 빈 목록과 빈 문자열 항목 두 경우를 모두 넣어 본다
    음성 대조: (a) 검사를 지운 사본에서 `test_error_action_step_without_do` 가 FAIL
- [ ] SC-04: 고친 뒤 다시 돌린 표시 `fix` 규칙 — 케이스 최상위의 선택 키이고, `note`(비어 있지 않은 문자열)는 필수, `commit` 은 선택, 그 밖의 키는 막는다. 있으면 케이스 페이지 머리에 `note` 문장이 나온다 [exact]
    측정: 단위 테스트 `test_fix_rendered_in_case_header` · `test_error_fix_without_note` · `test_error_fix_unknown_key` 통과
    음성 대조: `note` 필수 검사를 지운 사본에서 `test_error_fix_without_note` 가 FAIL
- [ ] SC-05: Given 루트와 두 케이스 폴더에 이미 `index.html` 이 있고 한 케이스 기록이 틀렸다. When 스크립트를 돌리면 Then 종료 코드 1 이고, 세 `index.html` 의 내용이 한 바이트도 바뀌지 않는다 — 전부 검사한 뒤에만 쓴다 [exact]
    측정: 단위 테스트 `test_error_writes_no_page` 통과
    음성 대조: 케이스를 읽는 대로 바로 쓰는 사본에서 이 테스트가 FAIL
- [ ] SC-06: 기존 24 개 테스트 이름이 모두 남아 있고 전체 테스트가 통과한다. 루트 페이지를 보던 테스트 네 개는 검사 의도를 그대로 두고 보는 자리만 옮긴다 — `test_builds_report` · `test_status_is_computed_from_steps` 는 케이스 페이지로, `test_failing_case_comes_first` 는 루트 목록의 링크(`href="TC-…/index.html"`) 순서로, `test_example_report_is_current` 는 루트와 케이스 페이지 전부로 넓힌다 [exact, enumerated]
    측정: 기존 이름 24 개 — `test_builds_report` `test_status_is_computed_from_steps` `test_failing_case_comes_first` `test_error_invalid_json` `test_error_unknown_key` `test_error_missing_key` `test_error_missing_image` `test_error_bad_image_name` `test_error_bad_keyword` `test_error_bad_result_value` `test_error_result_on_action_step` `test_error_result_without_seen` `test_error_no_checked_step` `test_error_duplicate_id` `test_error_empty_root` `test_warn_unreferenced_png` `test_check_writes_nothing` `test_rerun_is_identical` `test_error_template_missing` `test_error_template_slot_zero` `test_error_template_slot_extra` `test_example_report_is_current` `test_format_doc_example_passes` `test_format_doc_lists_every_key` — 가 `grep -c "def <이름>("` 로 각 1, 그리고 단위 테스트 종료 코드 0 · 출력 끝 `OK`
- [ ] SC-07: 예시 폴더가 새 형식이다 — 모든 `만일` 단계에 `do` 가 있고, 한 케이스 이상에 `fix` 가 있으며, 커밋된 루트 `index.html` 과 케이스별 `index.html` 전부가 다시 만든 것과 바이트 단위로 같다 [exact]
    측정: `test_example_report_is_current` 가 예시 폴더의 모든 `index.html`(루트 1 + 케이스 수만큼)을 경로 집합과 바이트로 비교하고 통과 · `grep -l '"fix"' $T/example/*/record.json` 1 개 이상
- [ ] SC-08: 기록 형식 문서가 새 키와 구조를 담는다 — `do` · `fix` · `note` 가 키 표에 있고, 폴더 그림에 케이스 폴더 안 `index.html` 이 있으며, 문서 안 예시 기록이 검사를 통과한다 [exact]
    측정: `test_format_doc_lists_every_key` · `test_format_doc_example_passes` 통과 · `awk '/^## 폴더 구조/,/^## 예시/' $K/references/record-format.md` 에서 `index.html` 을 담은 줄 2 이상(루트 · 케이스)

## Error

- [ ] ER-01: 새 규칙의 오류 줄이 케이스 폴더 · 시나리오 번호 · 단계 번호 · 키를 짚는다 — 예 `TC-001-transfer/record.json 시나리오 1 단계 1.do` [exact]
    측정: `test_error_action_step_without_do` 가 stderr 에 `TC-001-transfer/record.json 시나리오 1 단계 1.do` 를 담는지 확인하고 통과

## Architecture

- [ ] AR-01: 바뀐 파일이 범위 경계 네 경로 안에만 있다 [exact]
    측정: `git -C $W diff --name-only $BASE..$TIP -- . ':(exclude).harness'` 출력 각 줄이 `flutter-toolkit/skills/flutter-scenario-report/` · `flutter-toolkit/evals/scenario-report/` 로 시작하거나 `flutter-toolkit/README.md` 와 같다. 밖 경로 0 줄
- [ ] AR-02: Given 예시 보고서를 다시 만든 뒤. When 브라우저 MCP(`mcp__playwright__*`)로 `file://$T/example/index.html` 을 열고 첫 케이스 링크를 누르면 Then 케이스 페이지로 넘어가 제목이 보이고, 두 페이지 모두 콘솔 오류가 0 건이다(글꼴 주소 `cdn.jsdelivr.net` 실패는 제외). 두 페이지 캡처를 세션 임시 폴더 `evidence/` 에 남긴다 [exact]
    측정: `browser_navigate` → `browser_click` → `browser_snapshot` 에 케이스 제목 · `browser_console_messages` 오류 0 · `browser_take_screenshot` 두 장
- [ ] AR-03: 스킬 설명을 바꿨으면 `flutter-toolkit/README.md` 가 같이 맞춰져 있다 [exact]
    측정: `python3 scripts/sync-docs.py flutter-toolkit --check-only` (`$W` 에서) 종료 0 이고 `모든 README가 동기화 상태` 출력

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 종료 0
- [ ] AP-04: SKILL.md frontmatter 에서 name 필드 누락 금지
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=frontmatter` 종료 0

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 페이지 틀은 기존 `templates/report.html` 하나를 케이스 페이지와 목록 페이지가 함께 쓴다
    측정: `find $K/templates -type f | wc -l` 이 1

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 대신 SC-06 단위 테스트와 `python3 scripts/validate-plugin.py flutter-toolkit` 종료 0 을 본다)
- [ ] DG-02: 바뀐 마크다운 파일(`$K/SKILL.md` · `$K/references/record-format.md` · `$K/references/scenario-writing.md`)의 마크다운 경고가 0 건이다
    측정: 범위 경계의 markdownlint-cli2 명령에 세 파일을 넘겨 `Summary: 0 issues`
- [ ] DG-03: N/A (commands.test 는 scripts/release.sh 실행 — 이번 변경과 무관. 콘솔 오류는 SC-06 단위 테스트 출력 `OK` 로 본다)
- [ ] DG-04: N/A (구동할 앱 · 서버 없음 — 산출물은 스크립트와 정적 HTML. 브라우저 확인은 AR-02 가 맡는다)
