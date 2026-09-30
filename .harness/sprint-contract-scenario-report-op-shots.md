---
feature: "flutter-scenario-report — 조작마다 캡처 · 조작 줄 왼쪽 사진 · 많은 조작 접기 · 번호 배지"
slug: scenario-report-op-shots
created: "2026-09-30 15:50"
complexity: "복잡"
conditions: 22
status: done
owner_session: 97f28e34-99ea-4a74-9baa-3288b7964458
conditions_digest: sha256:807d5560d2670b8c
measurement_digest: sha256:61d60e275b0ee4cb
locked_at: "2026-09-30 15:55"
---

## 배경

- 앞 계약 `scenario-report-per-case`(APPROVE, 커밋 `36fa7faf`)가 행동 단계에 조작 순서 `do`(글자 목록)를 넣었다. 사용자가 "스텝바이스텝" 을 조작 하나마다 캡처가 붙는 모양으로 원했다(2026-09-30 대화).
- 사용자 결정: (1) 모든 조작에 캡처 필수 (2) 시안 A2 — 사진을 조작 글자 왼쪽에 (3) 조작이 많으면 시안 A3 — 앞 세 개만 보이고 나머지 접기, 펼치면 "접기" (4) 번호를 조금 눈에 띄게 (5) 조작이 5 개를 넘으면 나누라는 작성 규칙과, 8 개를 넘으면 스크립트 경고. 시안 캡처: 세션 임시 폴더 `opshot-mock/opshot-a2.png` · `opshot-a3-closed.png` · `opshot-a3-open.png`
- 건너뛴 시나리오는 조작을 실제로 하지 않았으므로 캡처가 없을 수 있다 — 그 시나리오에서만 캡처를 선택으로 둔다

## GAP 분석

- `do` 는 지금 글자 목록이다(`build_report.py` `STEP_FIELDS`). 조작별 캡처를 담을 자리가 없다
- 보고서는 `do` 를 `<ol class="do"><li>글자</li></ol>` 로만 그린다. 사진 · 접기 · 번호 배지가 없다
- 사진 확대 창 스크립트는 `.shots img,.zoom img` 만 연결한다(`templates/report.html`)
- 기준값(2026-09-30 15:48, 커밋 `36fa7faf`): 단위 테스트 35 개 통과 · 예시 사진 크기 402×874

## 범위 경계

```text
# sprint-scope
flutter-toolkit/skills/flutter-scenario-report/
flutter-toolkit/evals/scenario-report/
.harness/
```

- 하지 않는 것: 루트 · 킷 README 수정(스킬 설명 문장은 그대로), 버전 올리기와 릴리스
- 측정 공통 정의: `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/scenario-report-per-case` · `K=$W/flutter-toolkit/skills/flutter-scenario-report` · `T=$W/flutter-toolkit/evals/scenario-report` · 시작 커밋 `BASE=36fa7faf` · 끝 `TIP=$(git -C $W rev-parse feat/scenario-report-per-case)` · 단위 테스트 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v` (`$W` 에서)
- 음성 대조는 `BUILD_REPORT_SCRIPT` 로 검사를 뺀 스크립트 사본을 돌린다. 사본 옆에 `templates/` 를 복사하고, 변이 전후 글이 다른지 먼저 확인한다
- 브라우저 확인은 앞 계약 개정 A-01 과 같이 `python3 -m http.server --bind 127.0.0.1` 로 예시 폴더를 띄워 `mcp__playwright__*` 로 연다. 캡처는 세션 임시 폴더 `evidence/` 로 옮긴다
- 마크다운 경고 측정: 세션 임시 폴더 `mdlint/node_modules/.bin/markdownlint-cli2 --config mdlint/cfg.markdownlint-cli2.jsonc <파일>`
- 기존 테스트 중 옛 글자 목록 `do` 를 전제한 것은 이름을 두고 본문을 새 형식으로 다시 쓴다 — 공용 데이터 `VALID` 의 모든 `do`, `test_do_rendered_as_list`(새 그림 조각으로), `test_error_do_empty`(빈 목록 · 빈 `act`), `test_error_do_not_list`, `test_do_optional_on_setup`, 그리고 문서 예시의 사진 파일을 모으는 `test_format_doc_example_passes`(조작 `shot` 도 모은다) · 키 목록을 모으는 `test_format_doc_lists_every_key`(조작 항목 키 표도 넣는다)
- `shot` 은 파일 이름 글자다. 검사는 기존 사진 검사 함수에 `{"file": shot, "caption": act}` 로 넘겨 그대로 쓴다 — 새 사진 검사 함수를 만들지 않는다
- SK-02 의 여섯 주제 검사는 앞 계약 `sprint-contract-scenario-report-per-case.md` SK-04 측정과 같은 논리다(파일을 `^## ` 로 쪼개 `의도` · `먼저` · `그러면` · `숨김` · `사라` · `질문` 절마다 `https://` · `좋은 예` · `나쁜 예` 확인)
- 오라클 해소: SK-01 · SK-02 — 산출물이 스킬 안내문이라 문구 존재가 결과다. 안내가 가리키는 동작은 SC 조건이 테스트로 잰다

## Skill

- [ ] SK-01: 3 단계(실행 · 캡처)가 시나리오 사진(`shots`)과 따로 조작 하나마다 캡처하고 곧바로 케이스 폴더로 복사하라고 적고, 4 단계가 `do` 항목을 `act` · `shot` 짝으로 쓰라고 적는다 [exact]
    측정: `awk '/^### 3\./,/^### 4\./' $K/SKILL.md` 에 `조작 하나마다 캡처하고` 가 1 줄 이상, `awk '/^### 4\./,/^### 5\./' $K/SKILL.md` 에 `` `act` `` 와 `` `shot` `` 이 함께 든 줄이 1 줄 이상
- [ ] SK-02: `references/scenario-writing.md` 1 절에 "한 단계의 조작이 5 개를 넘으면 상태를 만드는 앞부분을 `먼저` 로 옮기거나 단계를 나눈다" 규칙이 출처 주소와 함께 있고, 여섯 주제 검사가 계속 빈 목록이다 [exact]
    측정: `awk '/^## 1\./,/^## 2\./' $K/references/scenario-writing.md` 에 `5 개를 넘으면` 이 든 줄 1 이상 · 같은 절의 `https://` 2 개 이상 · 세션 임시 폴더 `sk04.py $K/references/scenario-writing.md` 출력 `[]`
- [ ] SK-03: 기록 형식 문서가 `do` 항목을 `act` · `shot` 객체로 설명하고, 문서 안 예시 기록이 검사를 통과한다 [exact]
    측정: `test_format_doc_lists_every_key` 가 `act` · `shot` 을 포함한 모든 키를 문서에서 찾고 통과 · `test_format_doc_example_passes` 통과

## Script

- [ ] SC-01: `do` 항목은 `act`(비어 있지 않은 글자) · `shot`(캡처 파일 이름 글자) 두 키를 가진 객체여야 한다 — 글자 항목 · `shot` 없는 항목 · 모르는 키가 든 항목 · 빈 `act` 를 각각 막는다 [exact, enumerated]
    측정: 단위 테스트 `test_error_do_string_item` · `test_error_do_item_without_shot` · `test_error_do_item_unknown_key` · `test_error_do_empty`(빈 목록과 빈 `act` 두 경우, 오류 줄에 `.do`) 통과
    음성 대조: `shot` 필수 검사를 뺀 사본에서 `test_error_do_item_without_shot` 이 FAIL
- [ ] SC-02: `shot` 은 기존 사진 검사를 그대로 받는다 — 케이스 폴더에 없는 파일 · 이름 규칙 위반 · PNG 가 아닌 파일을 막고, 오류 줄이 `시나리오 N 단계 M.do[K].shot` 을 짚는다. 조작 사진으로 쓴 파일은 "기록이 가리키지 않는 캡처" 경고에 나오지 않는다 [exact]
    측정: 단위 테스트 `test_error_do_shot_missing_file` · `test_do_shot_counts_as_used` 통과
- [ ] SC-03: 건너뛴 시나리오(`skipped`)의 조작 항목은 `shot` 이 없어도 된다. 건너뛰지 않은 시나리오에서는 필수다 [exact]
    측정: 단위 테스트 `test_do_shot_optional_when_skipped` 통과 (건너뛴 시나리오 `shot` 없음 → 종료 0, 같은 기록에서 `skipped` 를 빼면 → 종료 1)
- [ ] SC-04: 케이스 페이지에서 조작 한 줄은 번호 · 사진 · 조작 글자 순서로 그려진다 — `<li><span class="n">1</span><img src="{shot}" width="{w}" height="{h}" alt="{act}"><span class="act">{act}</span></li>` [exact]
    측정: 단위 테스트 `test_do_rendered_with_shots` 가 위 조각을 케이스 페이지에서 찾고 통과
- [ ] SC-05: 조작이 4 개 이상인 단계는 앞 3 개만 목록에 두고 나머지를 `<details class="more">` 안의 두 번째 목록에 넣는다. 요약 줄에 `조작 {남은 수}개 더 보기 (모두 {전체}개)` 와 `접기` 두 글자가 있고, 접힌 목록의 번호는 4 부터 이어진다. 조작이 3 개 이하면 `<details` 가 0 개다 [exact]
    측정: 단위 테스트 `test_do_folds_after_three` 통과 (조작 9 개 · 3 개 두 경우)
    음성 대조: 접기를 빼고 전부 한 목록에 그리는 사본에서 이 테스트가 FAIL
- [ ] SC-06: 한 단계의 조작이 9 개 이상이면 `경고:` 줄을 내고 보고서는 만든다(종료 0). 8 개 이하면 그 경고가 없다 [exact]
    측정: 단위 테스트 `test_warn_many_actions` 통과 (9 개 → 경고 줄에 `시나리오 1 단계 1.do` 와 `9개`, 8 개 → 경고 0 줄)
    음성 대조: 경고를 빼는 사본에서 이 테스트가 FAIL
- [ ] SC-07: 조작 번호가 배지로 보이고 조작 사진은 작게 나온다 — 페이지 틀의 `.do .n` 규칙에 `font-weight:600` 과 `background` 가 있고, `.do img` 규칙의 `width` 가 48px 이하이며, 조작 사진도 확대 창에 연결된다(`.do img` 가 확대 창 스크립트 선택자에 있다) [exact]
    측정: `grep -oE '\.do \.n\{[^}]*\}' $K/templates/report.html` 출력에 `font-weight:600` · `background` 가 함께 있다 · `grep -oE '\.do img\{[^}]*\}' $K/templates/report.html` 의 `width:` 값이 48px 이하 · 확대 창 스크립트의 `querySelectorAll(` 인자에 `.do img` 가 있다
    양성 대조: 봉인 시점 틀(`36fa7faf`)에서 세 측정 모두 0 건
- [ ] SC-08: 기존 35 개 테스트 이름이 모두 남아 있고 전체 테스트가 통과한다. 예시 기록의 건너뛰지 않은 시나리오는 모든 조작에 `shot` 이 있고, 커밋된 예시 보고서 전부(루트 + 케이스)가 다시 만든 것과 바이트 단위로 같다 [exact]
    측정: 기준 커밋 `36fa7faf` 의 테스트 파일에서 뽑은 `def test_` 이름 35 개가 현재 파일에 각 1 · 단위 테스트 종료 0 · 출력 끝 `OK` · 예시 `record.json` 을 파이썬으로 읽어 건너뛰지 않은 시나리오의 `do` 항목 중 `shot` 없는 것 0 개

## Error

- [ ] ER-01: 새 오류 줄이 케이스 폴더 · 시나리오 · 단계 · 조작 번호를 짚는다 — 예 `TC-001-transfer/record.json 시나리오 1 단계 1.do[2].shot` [exact]
    측정: `test_error_do_item_without_shot` 가 stderr 에 `TC-001-transfer/record.json 시나리오 1 단계 1.do[2].shot` 을 담는지 확인하고 통과

## Architecture

- [ ] AR-01: 바뀐 파일이 범위 경계 세 경로 안에만 있다 [exact]
    측정: `git -C $W diff --name-only $BASE..$TIP -- . ':(exclude).harness'` 각 줄이 `flutter-toolkit/skills/flutter-scenario-report/` · `flutter-toolkit/evals/scenario-report/` 로 시작한다. 밖 경로 0 줄
- [ ] AR-02: Given 예시 보고서를 다시 만든 뒤. When 간이 서버로 조작이 있는 케이스 페이지를 열고 조작 사진 하나를 누르면 Then 확대 창이 열리고(`dialog.viewer` 가 open), 콘솔 오류가 0 건이다. 캡처 한 장을 세션 임시 폴더 `evidence/` 에 남긴다 [exact]
    측정: `browser_navigate` → `browser_click` (`.do img` 첫 번째) → `browser_evaluate` 로 `document.querySelector('dialog.viewer').open === true` → `browser_console_messages` 오류 0 → `browser_take_screenshot`

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 종료 0
- [ ] AP-04: SKILL.md frontmatter 에서 name 필드 누락 금지
    측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=frontmatter` 종료 0

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — `shot` 검사는 기존 사진 검사를 그대로 쓰고, 확대는 기존 확대 창을 쓴다
    측정: `grep -c 'def check_image' $K/scripts/build_report.py` 가 1 · `grep -c 'dialog class="viewer"' $K/templates/report.html` 가 1

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 대신 SC-08 단위 테스트와 `python3 scripts/validate-plugin.py flutter-toolkit` 종료 0 을 본다)
- [ ] DG-02: 바뀐 마크다운 파일(`$K/SKILL.md` · `$K/references/record-format.md` · `$K/references/scenario-writing.md`)의 마크다운 경고가 0 건이다
    측정: 범위 경계의 markdownlint-cli2 명령에 세 파일을 넘겨 `Summary: 0 issues`
- [ ] DG-03: N/A (commands.test 는 scripts/release.sh 실행 — 이번 변경과 무관. 콘솔 오류는 SC-08 단위 테스트 출력 `OK` 로 본다)
- [ ] DG-04: N/A (구동할 앱 · 서버 없음 — 산출물은 스크립트와 정적 HTML. 브라우저 확인은 AR-02 가 맡는다)
