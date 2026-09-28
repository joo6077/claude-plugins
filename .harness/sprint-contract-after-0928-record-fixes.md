---
feature: "지난 기록 줄 참조 · 기록 정정 (B20 · D6 · D8)"
slug: after-0928-record-fixes
created: "2026-09-28 12:31"
complexity: "복잡"
conditions: 23
status: active
conditions_digest: "sha256:eeed04ad09b3a423"
measurement_digest: "sha256:31aef57f8264fd42"
locked_at: "2026-09-28 12:40"
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
---

## 배경

- 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/remaining.md` 의 B20 · D6 · D8. 사용자 결정(2026-09-28T02:09:55.834Z 「3. 이건 고쳐 4. 고치긴해야지」)은 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md` 에 있다.
- 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 기준 판(이하 BASE): `e500a63` (가지 `chore/ak3-rec` 를 만든 시점). 끝 판(이하 TIP): 모든 커밋이 끝난 뒤 `git rev-parse chore/ak3-rec` 의 출력. `HEAD` 를 쓰지 않는다.
- 모든 측정은 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rec` 를 현재 폴더로 두고 돌린다. 측정 명령의 `$R` 은 `R=.harness/.meta/after-kaizen-0928/rec` 로 먼저 정한다.
- 경고 정리(마크다운 경고를 없앤 묶음 l1 · l3a · l3b · l4 · l2)는 `c3e45f3` 뒤 첫 부모 줄의 병합 다섯 `31859e2` · `b8f0995` · `ac4def3` · `4cc2e61` · `f51bd6e` 다. 이 병합들이 빈 줄 · 주석을 넣어 407 파일의 줄이 밀렸다.
- 밀린 참조의 정의(`$R/lineref.py find` 가 이대로 잰다):
  - 대상: BASE 에 추적되는 `.harness/` 아래 `.md` · `.yaml` · `.yml` · `.txt` 기록(이 묶음 폴더 `.harness/.meta/after-kaizen-0928/` 제외)에 적힌 `경로:줄` · `경로:줄-줄` 토큰. 경로는 저장소 경로 그대로 · 절대 경로(뒤쪽이 저장소 경로) · 저장소 경로의 뒤쪽 일부 · 파일 이름만 넷을 받되, 경고 정리 전 판(`c3e45f3`)의 추적 파일 가운데 하나로만 풀릴 때 쓴다. 그 파일이 경고 정리 병합에서 고쳐진(M) 파일이어야 한다.
  - 참조가 가리키는 판: 그 기록 줄을 쓴 커밋(`git blame BASE`)이 `c3e45f3` 의 조상이면 `c3e45f3`, 아니면 그 커밋 자체다. 뒤의 경우는 그 커밋 뒤에 들어온 경고 정리 병합이 그 대상 파일을 고쳤을 때만 센다.
  - 밀렸다: 앞 경우는 `c3e45f3` → `f51bd6e` 의 `git diff -U0` 로 옮긴 번호가 옛 번호와 다를 때, 뒤 경우는 그 커밋 → BASE 로 옮긴 번호가 다를 때. 새 번호는 가리키는 판 → BASE 의 `git diff -U0` 로 옮긴 값이다. 고쳐진 줄(조각 안의 줄)은 새 줄 가운데 글자가 가장 닮은 줄로 보내고 `changed` 로 적는다.
  - 자리(`zone`): 계약 파일(이름에 `sprint-contract` 가 든 파일)의 조건 줄(`^- \[[ x]\] [A-Z]{2,}-[0-9]{2}`)은 `condition`, 그 아래 들여쓴 줄은 `measure` (규약 `measurement_digest` 와 같은 식), 계약의 나머지 줄은 `prose`, 계약이 아닌 기록은 `record`.
- 처리 규칙 (결정 B20):
  - `condition` · `measure` 줄은 봉인 지문(`conditions_digest` · `measurement_digest`)이 덮으므로 글자를 바꾸지 않는다. 그 계약 옆에 정정 파일을 두고 옛 참조 → 새 참조를 적는다.
  - `prose` 줄은 봉인 밖이라 직접 고친다. 다만 조건이 가리키는 산문일 수 있어(규약 「조건 줄이 가리키는 산문을 고치면 개정 파일에 남긴다」) 같은 정정 파일에도 한 행씩 적는다. 옛 개정 파일은 고치지 않는다.
  - `record` 줄(QA 리포트 · 개정 · notes · 근거 기록)은 직접 고친다.
  - 정정 파일 이름: 계약 파일 이름의 `sprint-contract` 를 `sprint-lineref` 로 바꾼 것, 같은 폴더. 예: `.harness/sprint-contract-after-0924-kits-a.md` → `.harness/sprint-lineref-after-0924-kits-a.md`, `.harness/history/20260727-kaizen-phase8-infra-sprint-contract.md` → `.harness/history/20260727-kaizen-phase8-infra-sprint-lineref.md`.
  - 정정 파일 모양: 첫 줄 `# 줄 번호 정정 — <계약 파일 이름>`, 옛 참조 판과 새 참조 판(`e500a63`)을 적은 목록, 표 머리 `| 계약 줄 | 옛 참조 | 새 참조 | 대상 파일 | 처리 |`, 목록 한 행마다 표 한 행 `| <줄> | `<옛 참조>` | `<새 참조>` | <대상 저장소 경로> | <조건 줄 — 그대로 둠 / 측정 줄 — 그대로 둠 / 본문 — 직접 고침> |`.
- D6 대상: `docs/flutter/research-log.md` 20 행(남은 일 목록의 「19 행」 은 경고 정리 전 번호다 — 이 행도 밀렸다)의 build_runner CHANGELOG 행. 같은 옛 문장이 `docs/kaizen/flutter-research-log.md` 20 행(이름이 `-log.md` 로 끝나는 같은 날짜별 기록)에도 있어 함께 정정한다. 근거 원문 대조: `.harness/.meta/after-kaizen-0926b/ex/EX-5.md` — `-d` 무시 전환은 2.7.0, 「2.16 부터 잘못된 생성물을 기본으로 고친다」 는 맞음.
- D8 대상: main 끝 `01b1cac` 에서 닿는 커밋 1535 개 가운데 메시지에 쉬운 말 목록 낱말이 든 커밋. 가리기와 낱말 판정은 `~/.claude/hooks/check-plain-korean.sh` 1) 단계와 같은 식(`$R/plain_words.py`)이고, 목록은 `~/.claude/rules/plain-korean.md` (지문 `694f07858cf9016c`), 목록 읽기 도구 `~/.claude/hooks/_plain-korean-glossary.py` (지문 `793e5682f39120f3`). main 기록은 보호 설정으로 다시 쓸 수 없어 `git notes add` 로 메모(`refs/notes/commits`)만 단다. 메모 본문은 `python3 $R/plain_words.py note <해시>` 의 출력이다.

## GAP 분석

| 항목 | BASE 실측 (2026-09-28) | 조건 |
| --- | --- | --- |
| B20 밀린 참조 | 1065 행 (기록 170 파일). 자리: `record` 686 · `prose` 311 · `measure` 37 · `condition` 31. 종류: `moved` 1021 · `changed` 44. 정정 파일이 필요한 계약 60 개. 목록 지문(정렬 뒤) `2e65984b2b251b03` | SC-01 · SC-02 · SC-03 · SC-04 · ER-01 |
| B20 l4 notes 의 「520 곳」 | 셈 방식이 notes 에 없다. 이 계약은 토큰마다 센다(같은 자리를 상대 · 절대 경로로 두 번 적은 줄은 둘로 센다) · 경고 정리 중에 쓰인 기록(`c3e45f3` 조상이 아닌 커밋)도 센다 — 그래서 수가 다르다 | 범위 경계 |
| B20 봉인 | BASE 계약 231 개(`*sprint-contract*.md`, history 포함) 가운데 `SEAL_BROKEN` · `MEASURE_BROKEN` 0 | ER-01 |
| D6 | `docs/flutter/research-log.md:20` · `docs/kaizen/flutter-research-log.md:20` 에 옛 문장만 있고 정정 표시 0. 대응 페이지: 앞 파일은 `detect-docs-drift` 짝 이름이 `docs/flutter-toolkit/research-log.html` 이지만 파일이 없다(A2 매핑 결정 「페이지 없음이 맞음」), 뒤 파일은 짝 없음(`None`). `docs` 아래 html 에 `2.16 부터` 0 줄 | SK-01 · SK-02 · SK-03 |
| D8 | 걸린 커밋 271 개 (해시 목록 정렬 지문 `07bc82fc875822a0`). 낱말 상위: 게이트 87 · 정본 36 · 오라클 34 · 스키마 34 · 승격 32 · API 30. `git notes list` 0 줄, 원격 `refs/notes/*` 0 줄 | SC-05 · ER-02 |

## 범위 경계

- 하지 않는 것: `.harness` 밖 참조(`docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 의 `qa-evaluator.md:42` 등) — lt 묶음 몫이다 (ER-02 가 잰다).
- 하지 않는 것: 봉인된 계약의 조건 줄 · 측정 줄 글자, 옛 QA 리포트 · 개정 파일의 목록 밖 줄. 계약 · 기록의 줄 수를 바꾸지 않는다 (SC-03 이 잰다).
- 하지 않는 것: `c3e45f3` 전부터 이미 어긋나 있던 참조를 경고 정리 말고 다른 변경까지 되짚어 고치는 일. 이 계약은 경고 정리가 만든 밀림만 다룬다. 새 참조는 BASE 기준이라 BASE 뒤 다른 묶음(dz · h1 · h2 · k1 · orca · lt)이 대상 파일을 또 바꾸면 다시 밀릴 수 있다 — 정정 파일에 기준 판을 적는 까닭이다.
- 하지 않는 것: D8 메모를 원격에 올리는 일 — 부모가 올린다 (`git push origin refs/notes/commits`). 메모 목록은 `.harness/.meta/after-kaizen-0928/rec-notes.md` 에 적는다.
- 하지 않는 것: D8 에서 낱말이 일상 뜻으로 쓰인 커밋(예: 출력물 「표면」)을 사람이 골라 빼는 일. 기계 판정을 그대로 따르고, 메모 머리에 「목록의 뜻으로 쓴 자리에만 해당한다」 를 적는다.
- 측정 도구 셋(`$R/lineref.py` · `$R/content_check.py` · `$R/plain_words.py`)은 CI 에 넣지 않는다. 까닭: 셋 다 고정된 옛 판(`c3e45f3` · `f51bd6e` · `e500a63` · `01b1cac`)의 `git blame` · `git diff` 를 읽는데 CI 는 `actions/checkout@v7` 기본 얕은 복제라 그 판이 없다. `plain_words.py` 는 레포 밖 `~/.claude` 파일과 로컬 `refs/notes/commits` 를 읽는다. 이 셋은 이 계약의 측정 도구이고, 양성 · 음성 대조는 조건마다 적었다.
- 조건 수: 기능 조건 15 개(가이드 「복잡」 9~20 안).
- 커버리지 해소: SC-02 · SC-03 · SC-04 — 산문의 파일 이름들은 도구가 목록 전체를 한 번에 재는 대상이라 측정 절에 하나씩 다시 적지 않는다(목록은 `$R/lineref.py find` 출력이 정본). SC-03 의 `*sprint-lineref*.md` · `.harness/.meta/after-kaizen-0928/` 는 `scope` 모드가 허용하는 새 파일 이름이다.
- 커버리지 해소: SK-01 · SK-02 · AR-04 — 검출기가 짚은 `f=…` · `n=…` 은 측정 변수 정의, SK-01 의 `EX-5.md` 경로는 찾을 문자열이라 파일 대상이 아니다. ER-02 · AR-02 — `refs/notes/*` · `chore/ak3-rec` 는 원격 참조 이름, `.harness` 는 제외 경로, `CF=…` 는 변수 정의다.
- 오라클 해소: SK-01 · SK-02 — 산출물이 기록 문장 자체라 글자 대조가 곧 동작 관찰이다. BASE 값(양성 대조)을 적어 구현을 빼면 FAIL 함을 보였다. SC-05 · SC-06 · ER-01 · ER-02 · AR-02 — 측정이 도구 · 명령을 실제로 돌려 종료 코드와 출력으로 판정한다(검출기 오탐).
- 교차 진단 반영: AR-01 의 서명 줄 기대값은 이 묶음 지시문이 정한 줄(`Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`)이고, 구현 세션(2026-09-28, 모델 Opus 5.5 (1M context))의 커밋 서명 지침과 같음을 봉인 전에 확인했다. 다른 서명으로 커밋하면 지시를 어긴 것이므로 AR-01 이 FAIL 을 내는 것이 맞다.
- 범위 목록 (이 밖의 경로를 담은 커밋은 막힌다 — `.harness/` 는 늘 허용):

```text
# sprint-scope
docs/flutter/research-log.md
docs/kaizen/flutter-research-log.md
```

## 회귀 게이트

- BASE 실측(2026-09-28): `ci-local.sh` 25 단계 rc=0 · `feedback-agg-test SKIP (yq 없음)` 1 줄. CI 파일에만 있는 여섯 단계(`check-api-kit-docs` · `detect-docs-drift --check-table` · `check-cause-table-copies` · `measure-helpers-test` · `bambu-kit/evals/run-gate-fixtures.sh` · `bambu-kit/evals/makerworld-fetch-test.sh`) 전부 rc=0.
- BASE 실측: `docs/flutter/research-log.md` · `docs/kaizen/flutter-research-log.md` markdownlint-cli2 0.23.2 (`{ "config": { "MD013": false } }`) 경고 각 0. 양성 대조: 앞 파일 사본 끝에 `#bad heading` · 빈 줄 셋 · 줄 끝 공백 둘을 붙이면 3.
- BASE 실측: 제안한 정정 파일 모양(제목 · 목록 둘 · 표 머리 · 구분 줄 · 행 하나)의 표본에 같은 markdownlint 경고 0.

## Skill

- [ ] SK-01: (D6) `docs/flutter/research-log.md` 의 build_runner CHANGELOG 행이 옛 문장을 지우지 않고 바로 뒤에 정정 표시를 단다 — 그 행이 정확히 1 개이고, 옛 문장 `2.16 부터 잘못되거나 고쳐진 생성물을 기본으로 고친다` 와 정정 문자열 `정정(2026-09-28): build_runner 원문 기준 2.7.0 부터 — ` · `.harness/.meta/after-kaizen-0926b/ex/EX-5.md` 가 같은 줄에 옛 문장 · 정정 순서로 있다. 파일 줄 수는 BASE 와 같다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에서. `f=docs/flutter/research-log.md`.
  측정: `grep -cF 'build_runner/CHANGELOG.md> |' $f` 이 1. `L=$(grep -F 'build_runner/CHANGELOG.md> |' $f)`. `printf '%s\n' "$L" | grep -cF '<낱말>'` 이 세 낱말 각 1. 순서: `printf '%s\n' "$L" | awk '{ print (index($(0), "2.16 부터 잘못되거나") < index($(0), "정정(2026-09-28)")) }'` 이 1. `wc -l < $f` 이 `git show e500a63:$f | wc -l` 과 같다.
  양성 대조: BASE 에서 행 1 개, 옛 문장 1, 정정 문자열 둘은 각 0 (2026-09-28 실측).
  측정 대상: `docs/flutter/research-log.md`
- [ ] SK-02: (D6 같은 문장) `docs/kaizen/flutter-research-log.md` 의 `[build_runner CHANGELOG]` 줄이 옛 문장 `2.16 부터 생성물을 기본으로 고치고` 를 지우지 않고 그 뒤에 SK-01 과 같은 정정 문자열 둘을 단다. 파일 줄 수는 BASE 와 같다 [exact, enumerated]
  Given: 모든 커밋 뒤. `f=docs/kaizen/flutter-research-log.md`.
  측정: `grep -cF -- '- [build_runner CHANGELOG]' $f` 이 1. `L=$(grep -F -- '- [build_runner CHANGELOG]' $f)`. `printf '%s\n' "$L" | grep -cF '<낱말>'` 이 `2.16 부터 생성물을 기본으로 고치고` · `정정(2026-09-28): build_runner 원문 기준 2.7.0 부터 — ` · `.harness/.meta/after-kaizen-0926b/ex/EX-5.md` 각 1. 순서: `printf '%s\n' "$L" | awk '{ print (index($(0), "2.16 부터 생성물을") < index($(0), "정정(2026-09-28)")) }'` 이 1. `wc -l < $f` 이 `git show e500a63:$f | wc -l` 과 같다.
  양성 대조: BASE 에서 줄 1 개, 옛 문장 1, 정정 문자열 둘 각 0.
  측정 대상: `docs/kaizen/flutter-research-log.md`
- [ ] SK-03: (D6 페이지) 두 원본에 대응 페이지가 없음을 확인하고 페이지를 새로 만들지 않는다 — `docs/flutter-toolkit/research-log.html` 이 없고, `docs` 아래 html 가운데 `2.16 부터` 를 담은 파일이 0 개다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `test ! -e docs/flutter-toolkit/research-log.html` 종료 코드 0. `grep -rlF '2.16 부터' docs --include='*.html' | grep -c .` 이 0. `python3 -c "import importlib.util as u; s=u.spec_from_file_location('d','scripts/detect-docs-drift.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.map_source_to_html('docs/kaizen/flutter-research-log.md'))"` 출력이 `None`.
  양성 대조: 같은 `grep -rlF` 를 `docs/flutter/research-log.md` 가 든 `docs --include='*.md'` 로 돌리면 1 이상이다 (명령이 살아 있음).
  측정 대상: `docs/flutter-toolkit/research-log.html` · `docs/kaizen/flutter-research-log.md`

## Script

- [ ] SC-01: (B20 목록) 밀린 참조 목록이 BASE 실측과 같고, 줄 번호 계산을 쓰지 않는 내용 대조가 목록을 뒷받침한다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에서. 목록은 git 개체만 읽으므로 작업 폴더 편집과 무관하다.
  측정: `python3 $R/lineref.py find | grep -c .` 이 1065, `python3 $R/lineref.py find | LC_ALL=C sort | shasum -a 256 | cut -c1-16` 이 `2e65984b2b251b03`. `python3 $R/lineref.py find | python3 $R/content_check.py` 마지막 줄이 `SUMMARY moved=1021 changed=44 bad=0`, 종료 코드 0.
  알려진 답: 손으로 `git show <판>:<파일> | sed -n` 으로 대조한 세 행이 목록에 있다 — `.harness/history/20260727-kaizen-phase8-infra-sprint-contract.md` 120 행 `qa-evaluation-guide.md:431-446` → `qa-evaluation-guide.md:436-451` (`c3e45f3` 431~446 행 = BASE 436~451 행), `.harness/.meta/after-kaizen-0926/c1a-notes.md` 117 행 `harness/docs/guides/plugin-validation-guide.md:417-421` → `:449-453` (내용 같음), `.harness/.meta/after-kaizen-0926b/k1-notes.md` 37 행 `docs/planning/flows.md:53` → `:61` `changed` (BASE 61 행이 옛 53 행을 고친 줄). 목록에 없어야 하는 두 토큰 `reflect-kit/README.md:156` (경고 정리가 안 고친 파일) · `slang-4.14.0/README.md:190` (저장소 밖 파일) 은 `grep -cF` 0 (2026-09-28 실측 일치).
  음성 대조: 목록 첫 행의 새 번호를 1 늘려 `content_check.py` 에 넣으면 `bad=1`, 종료 코드 1 (2026-09-28 실측).
  측정 대상: `.harness/.meta/after-kaizen-0928/rec/lineref.py` · `.harness/.meta/after-kaizen-0928/rec/content_check.py`
- [ ] SC-02: (B20 고침) 목록 1065 행이 처리 규칙대로 고쳐졌다 — `condition` · `measure` 68 행은 줄이 BASE 그대로이고 정정 파일에 옛 · 새 참조 행이 있으며, `prose` 311 행은 줄이 「BASE 줄의 해당 토큰만 새 참조로 바꾼 줄」 과 글자까지 같고 정정 파일에도 행이 있으며, `record` 686 행은 줄이 같은 방식으로 바뀌었다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에 미커밋 변경이 없을 때.
  측정: `python3 $R/lineref.py check` 마지막 줄이 `SUMMARY rows=1065 in_place=997 lineref_file=68 bad=0`, 종료 코드 0.
  알려진 답: BASE 사본에서 `history/20260727-kaizen-phase8-infra-sprint-contract.md` 120 행(`prose`)만 고치고 그 정정 파일 한 행, `sprint-contract-after-0924-reviewer-unverified.md` 789 행(`condition`)의 정정 파일 한 행만 두면 `in_place=1 lineref_file=1 bad=1063` (2026-09-28 실측).
  음성 대조: BASE 그대로면 `in_place=0 lineref_file=0 bad=1065`, 종료 코드 1. 조건 줄(789 행)의 참조를 직접 바꾸면 그 줄 두 행이 `sealed-line-edited` 로 나온다. 한 줄에 여섯 토큰이 있는 `.harness/.meta/evidence/phase1.md` 92 행에서 하나만 고치면 여섯 행 모두 `not-fixed-in-place` 로 나온다 (2026-09-28 실측).
- [ ] SC-03: (B20 범위) BASE 에서 TIP 까지 `.harness/` 변경은 목록의 `record` · `prose` 줄과 정해진 새 파일뿐이다 — 기존 파일의 줄 수 변화 0, 목록 밖 줄 변경 0, 지우거나 옮긴 파일 0, 새 파일은 `*sprint-lineref*.md` · 이 계약의 계약 · 피드백 · 개정 파일 · `.harness/.meta/after-kaizen-0928/` 아래뿐 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: `python3 $R/lineref.py scope --tip $TIP` 마지막 줄이 `SUMMARY scope_bad=0`, 종료 코드 0.
  알려진 답: BASE 에서 떼어 낸 임시 작업 폴더에 허용 두 줄(120 · 121 행) · `.harness/project.yaml` 첫 줄 · 허용 새 파일 `history/x-sprint-lineref-y.md` · 허용 밖 새 파일 `.harness/stray.md` 를 커밋하면 출력이 `line-not-in-list@1 .harness/project.yaml` · `new-file-outside-allowed-names .harness/stray.md` 두 줄과 `scope_bad=2`, 종료 코드 1 (2026-09-28 실측).
  음성 대조: `--tip` 을 빼면 종료 코드 2 로 멈춘다(`HEAD` 를 짐작하지 않는다).
- [ ] SC-04: (B20 정정 파일) 정정 파일이 필요한 계약 60 개마다 정정 파일이 하나씩 있고 그 밖의 정정 파일은 없으며, 파일마다 첫 줄 `# 줄 번호 정정 — <계약 파일 이름>` · 표 머리 `| 계약 줄 | 옛 참조 | 새 참조 | 대상 파일 | 처리 |` · 기준 판 `e500a63` · 그 계약의 목록 행 수만큼 표 행을 갖췄다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `python3 $R/lineref.py files` 마지막 줄이 `SUMMARY files_expected=60 files_found=60 bad=0`, 종료 코드 0. 이름 집합: `find .harness -type f -name '*sprint-lineref*.md' | LC_ALL=C sort | shasum -a 256 | cut -c1-16` 이 `aae51cb9240e20ff` (목록의 계약 이름에서 `sprint-contract` 를 `sprint-lineref` 로 바꿔 정렬한 BASE 실측값).
  알려진 답: `sprint-lineref-after-0924-kits-a.md` 는 맞게, `sprint-lineref-kaizen-0924-p02-contract.md` 는 행 하나를 빼고 만들면 `row-count-24-of-25` 한 줄 · `missing` 58 줄 · `bad=59` (2026-09-28 실측).
  음성 대조: 정정 파일이 없으면 `files_found=0 bad=60`, 종료 코드 1.
- [ ] SC-05: (D8) 쉬운 말 목록 낱말이 든 main 커밋 271 개마다 메모가 있고, 메모가 걸린 낱말마다 `「<낱말>」 → <바꿔 쓸 말>` 줄을 담으며, 메모가 달린 커밋 집합이 그 271 개와 정확히 같다 [exact, enumerated]
  Given: 메모를 모두 단 뒤, 부모가 올리기 전. 목록 파일 지문 `shasum -a 256 ~/.claude/rules/plain-korean.md | cut -c1-16` 이 `694f07858cf9016c`, 읽기 도구 지문이 `793e5682f39120f3` 일 때 (다르면 목록이 바뀐 것이라 판정하지 않고 보고한다).
  측정: `python3 $R/plain_words.py scan | grep -c .` 이 271, `python3 $R/plain_words.py scan | cut -f1 | LC_ALL=C sort | shasum -a 256 | cut -c1-16` 이 `07bc82fc875822a0`. `python3 $R/plain_words.py check` 마지막 줄이 `SUMMARY commits=271 bad=0`, 종료 코드 0. `diff <(git notes list | cut -d' ' -f2 | LC_ALL=C sort) <(python3 $R/plain_words.py scan | cut -f1 | LC_ALL=C sort)` 출력 0 줄.
  알려진 답: 낱말 판정에 `게이트를 고치고 API(프로그램 창구)와 `오라클` 그리고 `sweep` 및 scripts/cache.py 를 봤다. 연락처` 를 넣으면 `['오라클', '게이트']` 두 낱말만 나온다 (괄호 풀이가 붙은 `API` · 한글 없는 백틱 `sweep` · 경로 `cache` · 일상어 `연락처` 는 빠짐, 2026-09-28 실측).
  음성 대조: 따로 둔 메모 참조(`GIT_NOTES_REF=refs/notes/rec-selftest`)에 첫 커밋은 바른 메모, 둘째 커밋은 낱말 줄 없는 메모를 달면 `check` 가 `missing:스키마` 한 줄 · `no-note` 269 줄 · `bad=270` 을 낸다 (2026-09-28 실측, 그 참조는 지웠다).
  측정 대상: `.harness/.meta/after-kaizen-0928/rec/plain_words.py`
- [ ] SC-06: 로컬 CI 와 CI 파일에만 있는 여섯 단계가 모두 통과한다 [exact, enumerated]
  Given: 모든 커밋 뒤, `TMPDIR` 을 세션 scratch 아래 새 폴더로 두고.
  측정: `TMPDIR=<scratch 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rec` 뒤 `<scratch 폴더>/ci-local/summary.txt` 에서 `grep -c 'rc=0'` 이 25, `grep -v 'rc=0'` 출력이 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐.
  이어서 여섯 명령 각각 종료 코드 0: `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh`.
  음성 대조: 판정 근거는 단계별 종료 코드다. BASE 25 단계 rc=0 · 여섯 단계 rc=0 은 회귀 게이트 절에 적었다.

## Error

- [ ] ER-01: (B20 봉인) BASE 에 있던 계약 231 개(`*sprint-contract*.md`, history 포함)가 TIP 에서 BASE 와 같은 봉인 판정을 내고 `SEAL_BROKEN` · `MEASURE_BROKEN` 이 0 이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: 바로 아래 들여쓴 열 줄을 들여쓰기를 뺀 채 `sealcmp.sh` 로 저장하고 `TMPDIR=<scratch 폴더> bash sealcmp.sh "$PWD" e500a63 "$TIP"` 의 표준 출력이 0 줄, 표준 오류 첫 줄이 `contracts=231`.
    #!/bin/bash
    R="${1}"; B="${2}"; T="${3}"
    cd "$R" || exit 2
    . harness/scripts/measure-common.sh || exit 2
    D=$(scratch_dir sealcmp) || exit 2
    unpack_rev "$B" "$D/b" && unpack_rev "$T" "$D/t" || exit 2
    ( cd "$D/b" && find .harness -type f -name '*sprint-contract*.md' | LC_ALL=C sort ) > "$D/list"; echo "contracts=$(grep -c . "$D/list")" >&2
    while IFS= read -r f; do printf '%s %s %s %s %s\n' "$f" "$(cd "$D/b" && verify_seal "$f" | cut -d' ' -f1)" "$(cd "$D/b" && verify_measurement "$f" | cut -d' ' -f1)" "$(cd "$D/t" && verify_seal "$f" | cut -d' ' -f1)" "$(cd "$D/t" && verify_measurement "$f" | cut -d' ' -f1)"; done < "$D/list" \
      | awk '$2 != $4 || $3 != $5 || $4 == "SEAL_BROKEN" || $5 == "MEASURE_BROKEN"'
    rm -rf "$D"
  양성 대조: BASE 에서 떼어 낸 임시 작업 폴더에서 `sprint-contract-after-0924-reviewer-unverified.md` 789 행 조건 줄의 `SKILL.md:113` 을 `SKILL.md:118` 로 바꿔 커밋하고 그 판을 TIP 자리에 넣으면 `.harness/sprint-contract-after-0924-reviewer-unverified.md SEAL_OK MEASURE_ABSENT SEAL_BROKEN MEASURE_ABSENT` 한 줄이 나온다 (2026-09-28 실측). BASE 와 BASE 를 넣으면 0 줄.
- [ ] ER-02: 범위 밖을 건드리지 않았다 — `.harness` 밖 참조 파일 `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 가 BASE 와 같고, 원격에 `refs/notes/*` 와 가지 `chore/ak3-rec` 가 없다(올리지 않았다) [exact, enumerated]
  Given: 모든 커밋과 메모 뒤, 부모가 올리기 전. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: `git diff --quiet e500a63 $TIP -- docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 종료 코드 0. `git ls-remote origin 'refs/notes/*' | grep -c .` 이 0. `git ls-remote origin refs/heads/chore/ak3-rec | grep -c .` 이 0.
  양성 대조: `git ls-remote origin refs/heads/main | grep -c .` 이 1 (원격 조회가 살아 있음, 2026-09-28 실측). 원격 조회가 실패하면(종료 코드 ≠ 0) 이 조건은 `[미검증]` 이다.
  측정 대상: `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md`

## Architecture

- [ ] AR-01: BASE 뒤 가지 `chore/ak3-rec` 의 모든 커밋이 맨 위 폴더 하나만 건드리고, 메시지 마지막 줄이 서명 줄이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: `for c in $(git rev-list e500a63..$TIP); do n=$(git show --name-only --format='' $c | cut -d/ -f1 | sort -u | grep -c .); s=$(git log -1 --format=%B $c | sed '/^[[:space:]]*$/d' | tail -1); [ "$n" = 1 ] && [ "$s" = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>' ] || echo "BAD $c n=$n"; done | grep -c BAD` 이 0. `git rev-list e500a63..$TIP | grep -c .` 이 1 이상.
  양성 대조: 같은 폴더 세기를 `a5152c5` 에 돌리면 17 이다 (2026-09-28 실측).
- [ ] AR-02: BASE 에서 TIP 까지 바뀐 경로(`.harness/` 제외)가 전부 `## 범위 경계` 의 `# sprint-scope` 블록 안에 있고, 그 두 경로가 모두 바뀌었다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`, `CF=.harness/sprint-contract-after-0928-record-fixes.md`.
  측정: `comm -23 <(git diff --name-only e500a63 $TIP -- . ':(exclude).harness' | sort -u) <(awk '/^# sprint-scope$/{p=1;next} p&&/^```/{p=0} p' $CF | sort -u) | grep -c .` 이 0. `git diff --name-only e500a63 $TIP -- . ':(exclude).harness' | grep -c .` 이 2.
  양성 대조: 같은 `comm` 을 `git diff --name-only a5152c5~1 a5152c5` 에 돌리면 1 이상이다.
- [ ] AR-03: 측정 도구 셋이 BASE 실측 때와 같은 글자로 커밋됐다 — TIP 에 추적되고 지문이 `$R/lineref.py` `4bec89e65a00cafd` · `$R/content_check.py` `d76b1fac1c43d92e` · `$R/plain_words.py` `c8435287d9a18234` 이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: 세 파일 각각 `git show $TIP:<파일> | shasum -a 256 | cut -c1-16` 이 위 값. 세 파일 모두 `git ls-files --error-unmatch <파일>` 종료 코드 0.
  양성 대조: BASE 에는 세 파일이 없다 (`git show e500a63:<파일>` 종료 코드 128).
  측정 대상: `.harness/.meta/after-kaizen-0928/rec/lineref.py` · `.harness/.meta/after-kaizen-0928/rec/content_check.py` · `.harness/.meta/after-kaizen-0928/rec/plain_words.py`
- [ ] AR-04: 부모가 읽을 기록 `.harness/.meta/after-kaizen-0928/rec-notes.md` 가 있고, D8 메모를 단 271 커밋의 전체 해시를 모두 담으며, B20 수(`1065` · `60`)와 올리는 명령 `git push origin refs/notes/commits` 를 적었다 [exact, enumerated]
  Given: 모든 커밋 뒤. `n=.harness/.meta/after-kaizen-0928/rec-notes.md`.
  측정: `python3 $R/plain_words.py scan | cut -f1 | while read -r h; do grep -qF "$h" $n || echo "$h"; done | grep -c .` 이 0. `grep -cF '1065' $n` · `grep -cF 'git push origin refs/notes/commits' $n` 각 1 이상. `grep -cE '(^|[^0-9])60([^0-9]|$)' $n` 이 1 이상.
  양성 대조: 파일이 없으면 첫 측정이 271 이다.
  측정 대상: `.harness/.meta/after-kaizen-0928/rec-notes.md`

## Anti-patterns

- [ ] AP-02: force push 금지
  측정: ER-02 의 두 `git ls-remote` 가 0 — 이 스프린트는 아무것도 올리지 않는다.
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 (BASE 0).

## Reusability

- [ ] RE-01: N/A (측정 도구 셋은 이 계약의 고정 판만 재는 일회용이라 공용 `scripts/` 로 올릴 대상이 아니다. 측정: 세 파일이 모두 `.harness/.meta/after-kaizen-0928/rec/` 아래에 있고 `scripts/` 아래 새 파일 0 — `git diff --name-only --diff-filter=A e500a63 $(git rev-parse chore/ak3-rec) -- scripts | grep -c .` 이 0)
- [ ] RE-02: 봉인 확인은 기존 규약 함수를 다시 쓴다 — ER-01 의 측정이 `harness/scripts/measure-common.sh` 로 `verify_seal` · `verify_measurement` · `unpack_rev` · `scratch_dir` 를 읽고, 세 도구 파일에 봉인 계산을 새로 짠 곳이 없다
  측정: `grep -cE 'sha256|digest|verify_seal' $R/lineref.py $R/content_check.py $R/plain_words.py` 의 세 값이 모두 0.

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only e500a63 $(git rev-parse chore/ak3-rec) | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 바꾸거나 만든 md 가운데 문서 둘 · 정정 파일 60 개 · `rec-notes.md` 가 편집기와 같은 설정의 markdownlint 경고 0 개다 — 설정은 markdownlint-cli2 0.23.2 · `{ "config": { "MD013": false } }`
  Given: 모든 커밋 뒤. 도구가 없으면 scratch 새 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 로 설치한다.
  측정: 대상 63 파일(`docs/flutter/research-log.md` · `docs/kaizen/flutter-research-log.md` · `find .harness -type f -name '*sprint-lineref*.md'` 60 개 · `.harness/.meta/after-kaizen-0928/rec-notes.md`)마다 `markdownlint-cli2 --config <설정 파일> <경로>` 출력에서 `^<경로>:[0-9]+` 줄 수가 0 이고 종료 코드 0. 직접 고친 옛 기록(`record` · `prose` 줄)은 숫자만 바뀌어 새 경고를 만들 수 없으므로 대상이 아니다.
  양성 대조: 회귀 게이트 절 — 나쁜 줄을 붙인 사본은 3.
- [ ] DG-03: N/A (commands.test 는 scripts/release.sh 를 돌린다 — 이번 변경과 무관. 실제 시험은 SC-06 이 잰다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경이 기록 · 문서 · 측정 도구뿐이다)
