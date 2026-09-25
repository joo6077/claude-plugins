---
feature: "flutter-scenario-report template — 보고서 HTML 틀을 템플릿 파일로 분리하고 예시 보고서를 레포에 둔다"
slug: flutter-scenario-report-template
created: "2026-09-25 16:32"
complexity: "중간"
conditions: 25
status: active
owner_session: e6978555-fef9-4611-a5d0-f6a8085b3924
conditions_digest: sha256:dd6e00e15297ea92
locked_at: "2026-09-25 16:42"
---

<!-- markdownlint-disable-file MD041 -->

## 배경

- `flutter-scenario-report` (flutter-toolkit v0.9.0) 이후 사용자 지시 (2026-09-25): "남은 거 진행해. 일단 핏팰에 있는 건 없애. 템플릿은 여기서 관리해야지."
- 질문 답 (2026-09-25 `AskUserQuestion` 세 건): fit-pal 은 시안 두 폴더와 `test-evidence` 전부 지운다 — **이미 지웠다** (백업 `$SP/fitpal-backup/`) · 템플릿은 "HTML 틀을 템플릿 파일로 분리" 와 "예시 보고서를 레포에 두기" 둘 다 · 다른 앱 실사용은 이번에 뺀다.
- 지금 보고서의 HTML 뼈대 · 스타일 · 화면 스크립트는 `scripts/build_report.py` 안에 문자열(`CSS` · `VIEWER` · `RAIL_SCRIPT` · `page_html`)로 박혀 있다. 이것을 `templates/report.html` 한 파일로 옮기고, 스크립트는 그 파일의 자리 하나에 케이스 HTML 을 끼워 넣는다. 케이스 · 시나리오 · 단계의 조각 HTML 은 판정 계산과 붙어 있어 스크립트에 남긴다.
- 예시: fit-pal 두 케이스 기록을 `flutter-toolkit/evals/scenario-report/example/` 에 두고 보고서를 만들어 커밋한다. **이 레포는 공개**(`gh repo view --json visibility` → `PUBLIC`)라 fit-pal 앱 화면 캡처는 넣지 않는다 — 캡처와 같은 비율로 만든 대체 그림을 쓴다. 기록 글은 이미 공개된 `record-format.md` 예시와 같은 테스트 데이터다.
- README 제목 `# Flutter Toolkit · v0.5.0` 은 실제 버전(0.9.0)과 어긋나 있다. 다른 13 개 킷 README 제목은 버전 없이 이름만 쓴다 → `# Flutter Toolkit` 으로 맞춘다.
- 복잡도 4 축: 레이어 2 (생성 스크립트 · 템플릿) — 공개 기록 형식 변경 아니오 — 소비면 예 (스크립트가 템플릿을 읽는다) — 회귀 위험 예 (보고서 모양이 바뀔 수 있다). "예" 2 개라 **중간**.
- 설정 리터럴 대조: `commands.analyze` `bash -n scripts/release.sh` → DG-01 N/A · `commands.test` `bash scripts/release.sh 2>&1 || true` → DG-03 N/A · 카테고리 Skill/SK · Script/SC · Error/ER · Architecture/AR · 안티패턴 AP-01 ~ AP-04.

## GAP 분석

| 대상 파일 | 실제 Read 증거 | 기존 갭 | 조건화 |
| --------- | -------------- | ------- | ------ |
| `$SKILL/scripts/build_report.py` (v0.9.0, `cf235be`) | `CSS = """` 블록 · `VIEWER = """` · `RAIL_SCRIPT = """` · `def page_html(cases)` 의 f-string 뼈대 | 디자인을 고치려면 파이썬 문자열을 고쳐야 한다 | AR-01 · AR-02 · AR-03 |
| `flutter-toolkit/README.md` | `:1` `# Flutter Toolkit · v0.5.0` | 버전 어긋남 | AR-07 |
| `$SKILL/SKILL.md` | References 절에 `templates/` 언급 없음 | 템플릿 위치를 모른다 | AR-08 |
| fit-pal `test-evidence` (지움, 백업 `$SP/fitpal-backup/test-evidence`) | TC-001 · TC-002 `record.json` | 예시가 레포에 없다 | AR-04 · AR-05 · AR-06 |

- 착수 전 실측: `python3 scripts/validate-plugin.py flutter-toolkit` `Exit: 0` · `sync-docs --check-only` 동기화 상태 · 단위 테스트 20 개 `OK` · `git diff --name-only origin/main...feat/flutter-scenario-report-template` 0 줄 · `"$SP/md_count.sh" "$WT"` → `SKILL.md 0` · `record-format.md 0` · `CLAUDE.md 77` · `README.md 10`.

## 범위 경계

```bash
WT=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/flutter-scenario-report
SKILL="$WT/flutter-toolkit/skills/flutter-scenario-report"
EX="$WT/flutter-toolkit/evals/scenario-report/example"
SP=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/e6978555-fef9-4611-a5d0-f6a8085b3924/scratchpad
OLD=cf235be   # v0.9.0 릴리스 병합 커밋 — 분리 전 스크립트
```

- 측정 M · M2 는 앞 스프린트들의 측정 스크립트 `$SP/measure_clean.js` (지문 `8e64b6678eaaad1d`) · `$SP/measure_rail2.js` (지문 `f2bf1aef7d50c848`). 기대값은 두 번 QA 승인된 시안의 값이고, `flutter-scenario-report` 계약 AR-03 과 같다.
- 변경 파일 허용 집합 (AR-09 의 유일한 열거처): `.harness/sprint-contract-flutter-scenario-report-template.md` · `.harness/sprint-feedback-flutter-scenario-report-template.md` · (생겼을 때만) `.harness/sprint-amendments-flutter-scenario-report-template.md` · `flutter-toolkit/README.md` · `flutter-toolkit/skills/flutter-scenario-report/SKILL.md` · `flutter-toolkit/skills/flutter-scenario-report/references/record-format.md` · `flutter-toolkit/skills/flutter-scenario-report/scripts/build_report.py` · `flutter-toolkit/skills/flutter-scenario-report/templates/report.html` · `flutter-toolkit/evals/scenario-report/test_build_report.py` · `flutter-toolkit/evals/scenario-report/example/` 아래 10 파일 (`index.html` · `TC-001-transfer-leader-cancel/` 의 `record.json` · `01-picker.png` · `02-after-picker-cancel.png` · `03-confirm.png` · `04-after-confirm-cancel.png` · `TC-002-appoint-vice-leader/` 의 `record.json` · `01-menu.png` · `02-picker.png` · `02-picker-title.png`).
- 커밋은 허용 집합의 경로를 하나씩 지정해 담는다 (`git add -A` · `git add .` 금지). 단위 테스트와 `py_compile` 이 만드는 `__pycache__` 를 레포 `.gitignore:4` (`scripts/__pycache__/`, 루트 경로만)가 거르지 못하기 때문이다.
- 이번 스프린트 밖: 버전 올리기와 릴리스는 QA APPROVE 뒤 PR 을 합치고 `main` 에서 `bash scripts/release.sh flutter-toolkit patch` 로 한다.
- 오라클 해소: AR-07 · AR-08 — 산출물이 문서 글자다.
- 교차 진단 반영 (qa-evaluator, 봉인 전): (1) SK-01 · AR-03 의 `$OLD:` 를 zsh 가 변수 수정자로 읽어 `cf235beutter-toolkit` 이 됐다 → `${OLD}` (2) AR-01 정렬이 언어 설정에 따라 달라졌다 → `LC_ALL=C sort` (3) `__pycache__` 가 `.gitignore` 에 안 걸려 전체 스테이징 시 AR-09 가 깨진다 → 경로 지정 커밋 명시 (4) AR-03 음성 대조를 QA 가 직접 재현 (5) ER-01 의 자리 표시 0 개 · 2 개를 테스트 둘로 나눔.
- 커버리지 해소: AR-01 — 네 파일 이름은 측정 절의 `find` 기대 출력에 그대로 있다. 명령 전체가 백틱 하나라 검출기가 따로 못 읽었다.

## Skill

- [ ] SK-01: 스킬 frontmatter 와 트리거는 그대로다 — `name` · `description` · `argument-hint` · `user-invocable` 네 값이 `$OLD` 판과 같다 [exact] (측정: `diff <(git -C "$WT" show ${OLD}:flutter-toolkit/skills/flutter-scenario-report/SKILL.md | awk 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f') <(awk 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f' "$SKILL/SKILL.md") | wc -l` 이 0)

## Script

- [ ] SC-01: 이 PR 브랜치는 버전을 손으로 바꾸지 않는다 [exact] (측정: `git -C "$WT" diff --name-only origin/main...feat/flutter-scenario-report-template -- flutter-toolkit/.claude-plugin/plugin.json .claude-plugin/marketplace.json | wc -l` 이 0. Given: 구현 커밋 완료 후)

## Error

- [ ] ER-01: Given 템플릿 파일이 없거나 케이스 자리 표시가 0 개 또는 2 개 이상, When 스크립트를 돌리면, Then 종료 코드 2 · 오류 줄에 `templates/report.html` 이 찍히고 `index.html` 을 쓰지 않는다 [exact] (측정: 단위 테스트 `test_error_template_missing` · `test_error_template_slot_zero` · `test_error_template_slot_extra` 세 개가 `ok`. 셋 다 스크립트와 템플릿을 임시 폴더에 복사해 템플릿만 망가뜨린다 — 파일 없음 / 자리 표시 0 개 / 자리 표시 2 개)
- [ ] ER-02: 기존 검사 동작이 그대로다 — 기존 단위 테스트 20 개가 전부 통과한다 [exact] (측정: `python3 -m unittest discover -s "$WT/flutter-toolkit/evals/scenario-report" -v 2>&1 | grep -cE '^test_.* \.\.\. ok$'` 이 22 이상이고 마지막 줄 `OK`)

## Architecture

- [ ] AR-01: 스킬 폴더 파일이 정확히 네 개다 — `SKILL.md` · `references/record-format.md` · `scripts/build_report.py` · `templates/report.html` [exact, enumerated] (측정: `(cd "$SKILL" && find . -type f -not -name '.DS_Store' -not -path '*/__pycache__/*' | LC_ALL=C sort | paste -sd' ' -)` 이 `./SKILL.md ./references/record-format.md ./scripts/build_report.py ./templates/report.html`)
- [ ] AR-02: 스크립트에 페이지 뼈대 · 스타일 · 화면 스크립트가 남아 있지 않고 템플릿에만 있다 [exact] (측정: `grep -cE '<style|<script|<!doctype|:root\{|@media' "$SKILL/scripts/build_report.py"` 이 0, 같은 패턴 `grep -cE` 로 `"$SKILL/templates/report.html"` 은 5 이상. 스타일 원문의 한 줄 `.rail-scn a[aria-current="true"]` 이 들어 있는 파일이 `grep -rlF '.rail-scn a[aria-current="true"]' "$WT/flutter-toolkit"` 로 템플릿 하나뿐 — 예시 `index.html` 은 빌드 결과라 제외하고 센다: `| grep -v '/example/index.html$' | wc -l` 이 1)
- [ ] AR-03: Given 같은 예시 기록, When 분리 전 스크립트(`$OLD` 판)와 분리 뒤 스크립트로 각각 보고서를 만들면, Then 두 `index.html` 이 바이트까지 같다 [exact] (측정: `T=$(mktemp -d); git -C "$WT" show ${OLD}:flutter-toolkit/skills/flutter-scenario-report/scripts/build_report.py > "$T/old.py"; cp -R "$EX" "$T/a"; cp -R "$EX" "$T/b"; python3 "$T/old.py" "$T/a" >/dev/null; python3 "$SKILL/scripts/build_report.py" "$T/b" >/dev/null; cmp -s "$T/a/index.html" "$T/b/index.html" && echo SAME || echo DIFF` 이 `SAME`. 음성 대조: 스크립트와 템플릿을 임시 폴더에 복사하고 템플릿의 `--fail:#cf222e` 를 `--fail:#cf2220` 으로 바꿔 만들면 `DIFF` — QA 가 직접 재현한다. 구현자가 붙인 결과는 참고용이다)
- [ ] AR-04: 레포에 예시가 있고 커밋된 예시 보고서가 지금 템플릿과 맞는다 — `$EX` 에 범위 경계의 10 파일이 있고, `--check` 가 종료 코드 0, 예시를 다시 만들면 커밋된 `index.html` 과 같다 [exact, enumerated] (측정: `(cd "$EX" && find . -type f -not -name '.DS_Store' | sort | wc -l)` 이 10, `python3 "$SKILL/scripts/build_report.py" "$EX" --check; echo $?` 이 0, 단위 테스트 `test_example_report_is_current` 가 `ok` — 이 테스트는 예시를 임시 폴더에 복사해 다시 만든 `index.html` 을 커밋된 것과 바이트 비교한다. 음성 대조: AR-03 과 같은 템플릿 변경 사본으로 돌리면 이 테스트가 FAIL)
- [ ] AR-05: 예시 그림은 앱 캡처가 아니라 가벼운 대체 그림이고 캡처와 비율이 같다 — 시나리오 사진 6 장은 402×874, 확대 사진 1 장은 402×107, 각 파일 20000 바이트 이하, 예시 폴더 전체 250000 바이트 이하 [exact, enumerated] (측정: `python3 -c "import pathlib;r=pathlib.Path('$EX');ps=sorted(r.rglob('*.png'));print([(p.name,int.from_bytes(p.read_bytes()[16:20],'big'),int.from_bytes(p.read_bytes()[20:24],'big'),p.stat().st_size) for p in ps]);print(sum(f.stat().st_size for f in r.rglob('*') if f.is_file()))"` — 7 개 모두 조건 크기와 바이트 이하, 마지막 줄 250000 이하)
- [ ] AR-06: 예시 보고서가 승인 시안과 같게 그려진다 [exact, enumerated] (측정: `node "$SP/measure_rail2.js" "$EX/index.html"` 첫 줄이 `rail_scn_status=✅❌-|✅✅ card_status=✅❌-|✅✅ rail_marks=✅1❌1|✅2❌0 card_marks=✅1❌1|✅2❌0 rail_extra_verdict=0/2 rail_fail_color_ok=5/5 spy=c0:1,2,3 c1:1,2 spy_visual=true click_jump=2/2 head_mid=2/2 head_at_top=0/2`, 둘째 줄 `console_errors=0 console_probe=1`. `node "$SP/measure_clean.js" "$EX/index.html"` 의 `W1440x900` 줄이 `rail_top=160` · `rail_follow_diff=0` · `rail_switch=true` · `card2_bottom=770` · `shot_h=594` · `steps_sig=14:95d99243` · `card_style=14px|rgb(255,255,255)`, `W1281x800 mode=rail` 에 `steps_min_w` 300 이상, `W1280x800 mode=bar`, `W390x844 bar_h` 100 이하 · `chip_rows=1`, 네 폭 `scroll_w` 가 폭과 같고, 마지막 줄 `console_errors=0 console_probe=1`)
- [ ] AR-07: README 제목이 버전 없이 `# Flutter Toolkit` 이다 [exact] (측정: `head -1 "$WT/flutter-toolkit/README.md"` 이 `# Flutter Toolkit`)
- [ ] AR-08: SKILL.md References 가 템플릿과 예시 위치를 알려 준다 [structural] (측정: `awk '/^## References/{f=1;next} /^## /{f=0} f' "$SKILL/SKILL.md" | grep -c 'templates/report.html'` 이 1 이상, 같은 구간 `grep -c 'evals/scenario-report/example'` 이 1 이상)
- [ ] AR-09: 이 브랜치가 바꾼 파일이 범위 경계의 허용 집합 안에만 있다 [exact] (측정: `git -C "$WT" diff --name-only origin/main...feat/flutter-scenario-report-template` 의 모든 줄이 허용 집합 중 하나. Given: 구현 커밋 완료 후. 상한은 가지 끝이고 `HEAD` 가 아니다. 봉인 전 실측 0 줄)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 (측정: `grep -rnE 'hardcoded.*version' "$SKILL" "$WT/flutter-toolkit/evals/scenario-report" | wc -l` 이 0)
- [ ] AP-02: force push 금지 (측정: 구현자 보고에 `git push` 명령 전문을 붙이고 `--force` · `-f` 가 없다)
- [ ] AP-03: bare code fence 금지 (측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=code-fence` 가 `0 bare`)
- [ ] AP-04: SKILL.md frontmatter name 누락 금지 (측정: `python3 scripts/validate-plugin.py flutter-toolkit --check=frontmatter` 가 OK)

## Reusability

- [ ] RE-01: N/A (재사용 단위가 새로 생기지 않는다 — 템플릿은 이 스크립트만 읽는다)
- [ ] RE-02: 템플릿을 두 벌 두지 않는다 — 스크립트는 템플릿을 자기 파일 위치 기준(`scripts/` 옆의 `templates/`)으로 읽고, 다른 곳에 복사본이 없다 [exact] (측정: `find "$WT" -name 'report.html' -not -path '*/node_modules/*' | wc -l` 이 1)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 scripts/release.sh 만 잰다 — 이번 변경과 교집합 0 개. 측정: `git -C "$WT" diff --name-only origin/main...feat/flutter-scenario-report-template | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 바꾼 마크다운이 새 경고를 만들지 않는다 [exact] (측정: `"$SP/md_count.sh" "$WT"` 가 `SKILL.md 0` · `record-format.md 0` · `README.md` 10 이하)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 는 릴리스 스크립트 실행 — 이번 변경과 교집합 0 개. 측정: DG-01 과 같다)
- [ ] DG-04: 예시 보고서를 네 화면 크기로 열 때 콘솔 오류 0 건이다 [exact] (측정: AR-06 의 두 측정 마지막 줄 `console_errors=0 console_probe=1`)
- [ ] DG-05: 레포 검사가 전부 통과한다 [exact] (측정: `"$SP/ci_local.sh"` 의 일곱 줄이 모두 `== [0]` 으로 시작하고, `python3 -m py_compile "$SKILL/scripts/build_report.py"; echo $?` 이 0)
- [ ] DG-06: SKILL.md 가 한다체이고 번역투·음역 목록이 0 건이다 [exact] (측정: `grep -cE '(합니다|습니다|세요)[.)]?$' "$SKILL/SKILL.md"` 0, `grep -cE '(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)|핫 ?리로드|쿼리|리셋|디폴트' "$SKILL/SKILL.md"` 0)
