---
feature: "지난 기록 줄 참조 · 기록 정정 (B20 · D6 · D8) 2 회차 계약"
slug: after-0928-record-fixes-r2
created: "2026-09-28 14:04"
complexity: "복잡"
conditions: 24
status: done
conditions_digest: "sha256:021a7910c47726ef"
measurement_digest: "sha256:b59bb2faed5a212a"
locked_at: "2026-09-28 14:18"
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
---

## 배경

### 2 회차 계약을 쓴 까닭

- 1 회차 계약: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rec/.harness/sprint-contract-after-0928-record-fixes.md`
  (조건 지문 `sha256:eeed04ad09b3a423` · 측정 지문 `sha256:31aef57f8264fd42` · 봉인 커밋 `a6c1487`, 이제 `status: superseded` · `superseded_by: after-0928-record-fixes-r2`).
  1 회차 QA 리포트 `sprint-feedback-after-0928-record-fixes.md` (APPROVE 23/23)는 커밋 `5d2e349` 에 그대로 남겼다. 1 회차 조건 줄 · 측정 줄은 건드리지 않아 봉인은 `SEAL_OK` · `MEASURE_OK` 그대로다.
- 1 회차 뒤 독립 검토가 막는 결함을 찾았고, 1 회차 조건은 고정값(목록 1065 행 · 목록 지문 `2e65984b2b251b03` · 허용 줄 집합)에 묶여 그 결함을 고친 결과를 통과시킬 수 없다. 틀린 측정은 넷이다.
  1. 범위 참조를 반쪽만 읽었다. `harness/agents/qa-evaluator.md:1089`~`:1097` 처럼 끝 번호가 백틱 · 쌍점으로 떨어진 범위에서 1 회차 도구(`$R/lineref.py`)는 앞 번호만 참조로 보고 옮겨, `.harness/sprint-contract-kaizen-0924-p17-howto-kit.md` 39 · 76 행이 `:1101`~`:1097` 로 앞뒤가 뒤집혔다.
  2. 파일 이름 없이 앞 참조에 이어 붙은 번호(`a.md:194` · `:212` 의 `:212`)를 보지 못해 옛 번호로 남았다. 2 회차 규칙으로 세면 경고 정리 대상 파일을 가리키는 이어 붙은 번호가 123 개이고, 그중 밀린 것이 90 개다 (독립 검토가 적은 142 는 그 검토 자신의 세는 식이라 여기서는 쓰지 않는다).
  3. 줄 자체가 고쳐진(`changed`) 참조를 글자가 가장 닮은 줄로 보냈는데, 기록 줄이 그 옛 줄을 인용하고 있으면 새 줄에는 그 인용문이 없어 인용이 거짓이 됐다. 2 회차 규칙으로 7 곳이다 (예: `.harness/.meta/evidence/phase15.md` 108 행 — 옛 `docs/tone/comment-economy.md:232` 의 「`DO use /// for public APIs` 계열」 문장은 뒤에 고쳐져 새 233 행에 없다).
  4. 내용 대조(`$R/content_check.py`)가 범위의 첫 줄만 보고 끝 줄을 안 봤고, 빈 줄 · `>` 만 있는 줄끼리 같다고 통과시켰다. 2 회차 규칙으로 옛 줄 덩어리가 빈 줄 · `>` 줄뿐인 행이 98 개다.
- 바로잡은 것: 새 측정 도구 둘(`$R2/lineref.py` · `$R2/content_check.py`)을 봉인 전에 만들어 BASE · 가지 끝 · 고친 모습을 흉내 낸 사본 · 구현을 되돌린 사본에서 돌렸다. 1 회차 도구 셋은 글자를 바꾸지 않는다.
  - 참조 토큰: `경로:번호` · `경로:번호-번호` 에 더해, 범위 끝이 `` `~` `` · 쌍점으로 떨어진 꼴(`a.md:12`~`:14`)과 앞 참조 바로 뒤에 `·` · `,` · `/` · `및` · `와` · `과` 나 빈칸만 두고 이어 붙은 `:번호` (앞 참조의 파일을 물려받는다)를 받는다. 번호 자리마다 줄 안 위치를 목록에 적는다(3 번째 칸, 쉼표로 이음).
  - 범위는 두 끝 번호를 함께 옮기고, 사이 줄에 고쳐지거나 지워진 줄이 있으면 `changed` 로 적는다(사이에 끼어든 줄만 있으면 `moved`).
  - `changed` 행은 같은 기록 줄의 인용문(백틱 · 「」 안 네 글자 이상, 참조 꼴 제외) 가운데 옛 줄 덩어리에 있던 것을 새 줄에서 찾는다. 찾으면 그 줄(여럿이면 닮은 줄에 가장 가까운 것)로 보내고 `quoted`, 못 찾으면 `unresolved` 다. 인용문이 없으면 1 회차처럼 닮은 줄로 보내고 `changed` 다.
  - `unresolved` 행은 기록 줄을 BASE 번호 그대로 두고 사람 확인 목록 `.harness/.meta/after-kaizen-0928/rec-review.md` 에 한 행씩 적는다. 계약의 정정 파일에는 넣지 않는다.
  - 내용 대조: 범위는 첫 줄부터 끝 줄까지 덩어리로 맞대고, 새 범위의 앞뒤가 뒤집히면 틀림이다. `moved` 는 빈 줄 · markdownlint 끄고 켜는 주석 줄을 뺀 두 덩어리가 글자까지 같아야 하고(경고 정리가 범위 안에 넣은 줄이다), `changed` · `quoted` 는 달라야 한다. 옛 덩어리에 있던 기록 줄의 인용문은 새 덩어리에도 있어야 한다. 옛 덩어리가 빈 줄 · `>` 줄뿐이면 「판정 못 함」(`undecidable`)으로 따로 센다.
- 시작 판: 지시문은 `6378948` 을 적었지만 그 판은 경고 정리 병합보다 앞선 main 릴리스(#119)라 `.harness` 기록에 밀린 참조가 아직 없고, 이 묶음의 도구가 읽는 기록 절반이 그 판에 없다. 그래서 2 회차의 시작 판은 둘로 잰다 — 고치기 전 BASE `e500a63` 과, 1 회차 결과 위에 QA 기록을 더한 가지 끝 `5d2e349` (2 회차 구현이 출발하는 상태).
- 1 회차에 개정 파일은 없다(`sprint-amendments-after-0928-record-fixes.md` 없음). D6 · D8 은 1 회차에서 된 것을 같은 측정으로 다시 확인만 한다(SK-01~SK-03 · SC-05 · AR-04 의 해시 부분).
- 사용자 위임: 2026-09-26T10:09:00.557Z · 10:30:16.222Z · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 (세션 bda55d45-296c-491f-89ba-b52042d58e72). 봉인된 측정이 처음부터 틀렸으면 새 판 계약을 다시 봉인한다 — `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md` 와 앞 묶음 결정 파일의 「추가 위임」 절.

### 1 회차 배경 (같은 뜻으로 옮김)

- 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/remaining.md` 의 B20 · D6 · D8. 사용자 결정(2026-09-28T02:09:55.834Z 「3. 이건 고쳐 4. 고치긴해야지」)은 같은 폴더 `decisions.md` 에 있다.
- 기준 판(이하 BASE): `e500a63` (가지 `chore/ak3-rec` 를 만든 시점). 끝 판(이하 TIP): 모든 커밋이 끝난 뒤 `git rev-parse chore/ak3-rec` 의 출력. `HEAD` 를 쓰지 않는다.
- 모든 측정은 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rec` 를 현재 폴더로 두고 돌린다. 측정 명령의 `$R` 은 `R=.harness/.meta/after-kaizen-0928/rec`, `$R2` 는 `R2=.harness/.meta/after-kaizen-0928/rec2` 로 먼저 정한다.
- 경고 정리는 `c3e45f3` 뒤 첫 부모 줄의 병합 다섯 `31859e2` · `b8f0995` · `ac4def3` · `4cc2e61` · `f51bd6e` 다.
- 밀린 참조의 정의(`$R2/lineref.py find` 가 이대로 잰다): 대상은 BASE 에 추적되는 `.harness/` 아래 `.md` · `.yaml` · `.yml` · `.txt` 기록(`.harness/.meta/after-kaizen-0928/` 제외)의 위 참조 토큰이다. 경로는 저장소 경로 · 절대 경로 · 저장소 경로의 뒤쪽 일부 · 파일 이름만 넷을 받되 `c3e45f3` 추적 파일 하나로만 풀리고 그 파일이 경고 정리 병합에서 고쳐진(M) 파일일 때 쓴다. 참조가 가리키는 판은 그 기록 줄을 쓴 커밋(`git blame BASE`)이 `c3e45f3` 의 조상이면 `c3e45f3`, 아니면 그 커밋이고(뒤의 경우는 뒤에 들어온 경고 정리 병합이 대상 파일을 고쳤을 때만), 밀렸다는 것은 번호 가운데 하나라도 옮긴 값이 다를 때다. 자리(`zone`)는 계약 파일의 조건 줄 `condition` · 그 아래 들여쓴 줄 `measure` · 계약의 나머지 `prose` · 계약이 아닌 기록 `record` 다.
- 처리 규칙 (결정 B20): `condition` · `measure` 줄은 글자를 바꾸지 않고 정정 파일에 적는다. `prose` 줄은 직접 고치고 정정 파일에도 적는다. `record` 줄은 직접 고친다. 정정 파일 이름은 계약 파일 이름의 `sprint-contract` 를 `sprint-lineref` 로 바꾼 것(같은 폴더), 모양은 첫 줄 `# 줄 번호 정정 — <계약 파일 이름>` · 새 참조 판 `e500a63` 을 적은 목록 · 표 머리 `| 계약 줄 | 옛 참조 | 새 참조 | 대상 파일 | 처리 |` · 목록 한 행마다 표 한 행 `| <줄> | `<옛 참조>` | `<새 참조>` | <대상 저장소 경로> | <조건 줄 — 그대로 둠 / 측정 줄 — 그대로 둠 / 본문 — 직접 고침> |`. 옛 · 새 참조 칸은 목록 4 · 5 번째 칸 글자 그대로다(백틱을 뺀 토큰, 이어 붙은 번호는 `:212` 꼴). 같은 줄에 같은 참조가 두 번 있으면 표 행도 두 번이다.
- 사람 확인 목록 모양(2 회차 새 파일): 표 머리 `| 기록 | 줄 | 옛 참조 | 후보 참조 | 대상 파일 | 인용 |`, `unresolved` 행마다 `| `<기록 경로>` | <줄> | `<옛 참조>` | `<후보 참조>` | <대상 저장소 경로> | <무엇이 안 맞는지> |`.
- D6 대상: `docs/flutter/research-log.md` 20 행 · `docs/kaizen/flutter-research-log.md` 20 행의 build_runner CHANGELOG 행 (근거 `.harness/.meta/after-kaizen-0926b/ex/EX-5.md`). 1 회차 커밋 `a078903` 에서 끝났다.
- D8 대상: main 끝 `01b1cac` 에서 닿는 커밋 1535 개 가운데 메시지에 쉬운 말 목록 낱말이 든 271 개에 `git notes` 메모(`refs/notes/commits`). 목록 `~/.claude/rules/plain-korean.md` (지문 `694f07858cf9016c`), 읽기 도구 `~/.claude/hooks/_plain-korean-glossary.py` (지문 `793e5682f39120f3`). 1 회차에서 끝났다.

## GAP 분석

| 항목 | 실측 (2026-09-28, 2 회차 도구) | 조건 |
| --- | --- | --- |
| B20 밀린 참조 | 1155 행. 자리: `record` 728 · `prose` 359 · `measure` 37 · `condition` 31. 종류: `moved` 1101 · `changed` 36 · `quoted` 11 · `unresolved` 7. 목록 지문(정렬 뒤) `3739abc49de7ebd9`. 1 회차 목록과 견주면 같은 행 1061, 새 행 94 (이어 붙은 번호 90 · 쌍점 범위 4), 1 회차 행 가운데 모양이 바뀐 것 4 (범위 끝을 붙여 읽은 행) | SC-01 |
| B20 내용 대조 | `SUMMARY moved=1101 changed=36 quoted=11 unresolved=7 undecidable=98 bad=0` 종료 코드 0 | SC-01 |
| B20 고침 상태 | BASE 사본: `rows=1155 in_place=0 lineref_file=0 review=0 bad=1155`. 가지 끝 `5d2e349`: `rows=1155 in_place=913 lineref_file=68 review=0 bad=174` (`not-fixed-in-place` 174). 고친 모습을 흉내 낸 사본: `rows=1155 in_place=1080 lineref_file=68 review=7 bad=0` | SC-02 |
| B20 정정 파일 | 정정 파일이 필요한 계약 60 개(이름 집합 지문 `aae51cb9240e20ff`, 1 회차와 같음). 가지 끝: `files_expected=60 files_found=60 review_rows=7 bad=19` (행이 모자란 정정 파일 17 · 사람 확인 목록 없음 2). BASE 사본: `bad=62`. 흉내 낸 사본: `bad=0` | SC-04 |
| B20 범위 | 가지 끝 `SUMMARY scope_bad=0` · 흉내 낸 사본 `scope_bad=0` | SC-03 |
| 1 회차 계약 | `status: superseded` · `superseded_by: after-0928-record-fixes-r2`, `SEAL_OK` · `MEASURE_OK` (작업 폴더, 2026-09-28 14:04 뒤 실측) | AR-05 |
| D6 · D8 | 1 회차 QA 값 그대로 (행 1 · 줄 수 477 · 203, 메모 271 · 지문 `07bc82fc875822a0`) | SK-01~SK-03 · SC-05 |

## 범위 경계

- 하지 않는 것: 앞 참조 없이 파일 이름만 앞에 적고 번호를 뒤에 둔 꼴(표의 다른 칸에 파일 이름이 있는 `` `:1089` `` 등). 어느 파일인지 기계로 정할 수 없어 2 회차 규칙에서 뺐다. `.harness` 밖 참조(lt 묶음 몫)도 그대로다.
- 하지 않는 것: `unresolved` 7 곳의 새 번호를 사람 대신 정하는 일. 기록 줄은 BASE 번호로 두고 사람 확인 목록에 남긴다.
- 하지 않는 것: `undecidable` 98 곳(옛 줄이 빈 줄 · `>` 줄)을 다른 식으로 다시 판정하는 일. 수만 따로 센다.
- 하지 않는 것: 봉인된 계약의 조건 줄 · 측정 줄 글자, 1 회차 계약의 조건 · 측정 줄, 1 회차 도구 셋(`$R/lineref.py` · `$R/content_check.py` · `$R/plain_words.py`) 글자. 기록 · 계약의 줄 수를 바꾸지 않는다 (SC-03 이 잰다).
- 하지 않는 것: D8 메모를 원격에 올리는 일 — 부모가 올린다 (`git push origin refs/notes/commits`).
- 측정 도구(`$R2/lineref.py` · `$R2/content_check.py` · `$R/plain_words.py`)는 CI 에 넣지 않는다. 고정된 옛 판의 `git blame` · `git diff` 를 읽는데 CI 는 얕은 복제라 그 판이 없고, `plain_words.py` 는 레포 밖 `~/.claude` 파일과 로컬 `refs/notes/commits` 를 읽는다.
- 조건 수: 기능 조건 16 개(가이드 「복잡」 9~20 안).
- 커버리지 해소: SC-02 · SC-03 · SC-04 — 정정 파일 60 개 · 기록 파일 이름들은 도구가 목록 전체를 한 번에 재는 대상이라 측정 절에 하나씩 다시 적지 않는다(목록은 `$R2/lineref.py find` 출력이 기준). SC-03 의 새 파일 이름은 도구의 허용 이름 규칙이 받는다.
- 커버리지 해소: SK-01 · SK-02 · AR-04 — 검출기가 짚을 `f=…` · `n=…` 은 측정 변수 정의, SK-01 의 `EX-5.md` 경로는 찾을 문자열이다. ER-02 · AR-02 — `refs/notes/*` · `chore/ak3-rec` 는 원격 참조 이름, `.harness` 는 제외 경로, `CF=…` 는 변수 정의다. AR-04 · AR-05 — `n=…` · `O=…` 는 측정 변수 정의이고 측정 절이 그 변수로 파일을 연다. SC-03 — `.harness/` · `*sprint-lineref*.md` · `.harness/.meta/after-kaizen-0928/` 는 도구의 허용 새 파일 이름 규칙이 재는 이름 꼴이다.
- 오라클 해소: SK-01 · SK-02 — 산출물이 기록 문장 자체라 글자 대조가 곧 동작 관찰이고 BASE 값(양성 대조)이 구현을 빼면 FAIL 함을 보인다. SC-01 · SC-05 · SC-06 · ER-01 · ER-02 · AR-02 — 측정이 도구 · 명령을 실제로 돌려 종료 코드와 출력으로 판정한다(검출기 오탐). SC-01 은 구현을 되돌린 목록(1 회차 결과)으로 FAIL 을 실측했다.
- 범위 목록 (이 밖의 경로를 담은 커밋은 막힌다 — `.harness/` 는 늘 허용):

```text
# sprint-scope
docs/flutter/research-log.md
docs/kaizen/flutter-research-log.md
```

## 회귀 게이트

- 1 회차 QA 실측(2026-09-28 13:24): `ci-local.sh` 25 단계 rc=0 · `feedback-agg-test SKIP (yq 없음)` 1 줄, CI 파일에만 있는 여섯 단계 rc=0, 계약 231 개 봉인 판정 차이 0, markdownlint 63 파일 경고 0.
- 교차 진단 반영 (2026-09-28, 봉인 전): SC-05 측정을 이 작업 폴더에서 다시 돌려 목록 지문 `694f07858cf9016c` · 읽기 도구 지문 `793e5682f39120f3` · `scan` 271 행 · 지문 `07bc82fc875822a0` · `check` 마지막 줄 `SUMMARY commits=271 bad=0` · 메모 집합 차이 0 줄을 얻었다. AR-04 의 `60` 측정은 문구 `정정 파일 60` 으로 좁혔다. 봉인 뒤 이 계약 자신의 `verify_seal` · `verify_measurement` 를 돌려 `SEAL_OK` · `MEASURE_OK` 를 확인한다.
- 흉내 낸 사본 만드는 법(재현용, 계약 밖 scratch 스크립트): `git clone --shared <작업 폴더> <scratch>/clone -b chore/ak3-rec` 에 `$R2` 두 파일을 복사하고, 목록 행마다 기록 줄을 「BASE 줄의 번호 자리만 새 번호로 바꾼 줄」(`unresolved` 는 BASE 그대로, `condition` · `measure` 는 BASE 그대로)로 쓰고, 정정 파일 표 행을 목록대로 다시 쓰고, 사람 확인 목록 7 행을 쓴 뒤 커밋했다 — 51 파일 바뀜. 이 사본에서 SC-01~SC-04 가 모두 통과했다(통과 집합이 비지 않음).

## Skill

- [ ] SK-01: (D6) `docs/flutter/research-log.md` 의 build_runner CHANGELOG 행이 옛 문장을 지우지 않고 바로 뒤에 정정 표시를 단다 — 그 행이 정확히 1 개이고, 옛 문장 `2.16 부터 잘못되거나 고쳐진 생성물을 기본으로 고친다` 와 정정 문자열 `정정(2026-09-28): build_runner 원문 기준 2.7.0 부터 — ` · `.harness/.meta/after-kaizen-0926b/ex/EX-5.md` 가 같은 줄에 옛 문장 · 정정 순서로 있다. 파일 줄 수는 BASE 와 같다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에서. `f=docs/flutter/research-log.md`.
  측정: `grep -cF 'build_runner/CHANGELOG.md> |' $f` 이 1. `L=$(grep -F 'build_runner/CHANGELOG.md> |' $f)`. `printf '%s\n' "$L" | grep -cF '<낱말>'` 이 세 낱말 각 1. 순서: `printf '%s\n' "$L" | awk '{ print (index($(0), "2.16 부터 잘못되거나") < index($(0), "정정(2026-09-28)")) }'` 이 1. `wc -l < $f` 이 `git show e500a63:$f | wc -l` 과 같다.
  양성 대조: BASE 에서 행 1 개, 옛 문장 1, 정정 문자열 둘은 각 0 (2026-09-28 실측). 가지 끝 `5d2e349` 에서 셋 다 1 · 순서 1 · 줄 수 477 = 477 (1 회차 QA 실측).
  측정 대상: `docs/flutter/research-log.md`
- [ ] SK-02: (D6 같은 문장) `docs/kaizen/flutter-research-log.md` 의 `[build_runner CHANGELOG]` 줄이 옛 문장 `2.16 부터 생성물을 기본으로 고치고` 를 지우지 않고 그 뒤에 SK-01 과 같은 정정 문자열 둘을 단다. 파일 줄 수는 BASE 와 같다 [exact, enumerated]
  Given: 모든 커밋 뒤. `f=docs/kaizen/flutter-research-log.md`.
  측정: `grep -cF -- '- [build_runner CHANGELOG]' $f` 이 1. `L=$(grep -F -- '- [build_runner CHANGELOG]' $f)`. `printf '%s\n' "$L" | grep -cF '<낱말>'` 이 `2.16 부터 생성물을 기본으로 고치고` · `정정(2026-09-28): build_runner 원문 기준 2.7.0 부터 — ` · `.harness/.meta/after-kaizen-0926b/ex/EX-5.md` 각 1. 순서: `printf '%s\n' "$L" | awk '{ print (index($(0), "2.16 부터 생성물을") < index($(0), "정정(2026-09-28)")) }'` 이 1. `wc -l < $f` 이 `git show e500a63:$f | wc -l` 과 같다.
  양성 대조: BASE 에서 줄 1 개, 옛 문장 1, 정정 문자열 둘 각 0. 가지 끝 `5d2e349` 에서 줄 수 203 = 203.
  측정 대상: `docs/kaizen/flutter-research-log.md`
- [ ] SK-03: (D6 페이지) 두 원본에 대응 페이지가 없음을 확인하고 페이지를 새로 만들지 않는다 — `docs/flutter-toolkit/research-log.html` 이 없고, `docs` 아래 html 가운데 `2.16 부터` 를 담은 파일이 0 개다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `test ! -e docs/flutter-toolkit/research-log.html` 종료 코드 0. `grep -rlF '2.16 부터' docs --include='*.html' | grep -c .` 이 0. `python3 -c "import importlib.util as u; s=u.spec_from_file_location('d','scripts/detect-docs-drift.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.map_source_to_html('docs/kaizen/flutter-research-log.md'))"` 출력이 `None`.
  양성 대조: 같은 `grep -rlF` 를 `docs --include='*.md'` 로 돌리면 1 이상이다 (1 회차 QA 실측 2).
  측정 대상: `docs/flutter-toolkit/research-log.html` · `docs/kaizen/flutter-research-log.md`

## Script

- [ ] SC-01: (B20 목록 · 2 회차) 밀린 참조 목록이 봉인 전 실측과 같고 — 이어 붙은 번호와 범위 끝 번호를 함께 세고, 줄이 고쳐진 참조는 인용문으로 가른다 — 범위 끝 줄까지 보는 내용 대조가 목록을 뒷받침한다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에서. 목록은 git 개체만 읽으므로 작업 폴더 편집과 무관하다.
  측정: `python3 $R2/lineref.py find | grep -c .` 이 1155, `python3 $R2/lineref.py find | LC_ALL=C sort | shasum -a 256 | cut -c1-16` 이 `3739abc49de7ebd9`. `python3 $R2/lineref.py find | cut -f7 | sort | uniq -c` 가 `changed` 36 · `moved` 1101 · `quoted` 11 · `unresolved` 7, `cut -f8` 로 같은 셈이 `condition` 31 · `measure` 37 · `prose` 359 · `record` 728. `python3 $R2/lineref.py find | python3 $R2/content_check.py` 마지막 줄이 `SUMMARY moved=1101 changed=36 quoted=11 unresolved=7 undecidable=98 bad=0`, 종료 코드 0.
  알려진 답 (손으로 `git show <판>:<파일> | sed -n` 대조, 2026-09-28 실측 일치): `.harness/sprint-contract-kaizen-0924-p17-howto-kit.md` 39 행 `harness/agents/qa-evaluator.md:1089~:1097` → `harness/agents/qa-evaluator.md:1101~:1109` `moved` (범위 끝을 함께 옮김). `.harness/.meta/evidence/phase16.md` 138 행 이어 붙은 `:25` → `:26` (대상 `docs/api/execution/probe-synthesis-hurl-semantics.md`, `c3e45f3` 25 행 = BASE 26 행 `> **출처:** [Hurl Request]…`). `.harness/.meta/evidence/phase15.md` 108 행 `docs/tone/comment-economy.md:232` → 후보 `:233` `unresolved` (인용 `DO use /// for public APIs` 가 BASE 에 없음). 1 회차 알려진 답 셋도 그대로 있다 — `history/20260727-kaizen-phase8-infra-sprint-contract.md` 120 행 `qa-evaluation-guide.md:431-446` → `qa-evaluation-guide.md:436-451`, `.harness/.meta/after-kaizen-0926/c1a-notes.md` 117 행 `harness/docs/guides/plugin-validation-guide.md:417-421` → `harness/docs/guides/plugin-validation-guide.md:449-453`, `.harness/.meta/after-kaizen-0926b/k1-notes.md` 37 행 `docs/planning/flows.md:53` → `docs/planning/flows.md:61` (이제 `quoted`). 없어야 하는 두 토큰 `reflect-kit/README.md:156` · `slang-4.14.0/README.md:190` 은 `grep -cF` 0. `undecidable` 알려진 답: `.harness/.meta/after-kaizen-0926b/cs-notes.md` 55 행 `harness/docs/guides/qa-evaluation-guide.md:1968` 의 `c3e45f3` 1968 행은 빈 줄이다.
  음성 대조 (2026-09-28 실측): 목록에서 p17 39 행의 새 참조를 1 회차 결과 `harness/agents/qa-evaluator.md:1101~:1097` 로 바꿔 `content_check.py` 에 넣으면 `reversed-range` 한 줄 · `bad=1` · 종료 코드 1. `phase15.md` 108 행의 종류를 `changed` 로 바꿔 넣으면(1 회차 처리) `quote-lost` 한 줄 · `bad=1`.
  측정 대상: `.harness/.meta/after-kaizen-0928/rec2/lineref.py` · `.harness/.meta/after-kaizen-0928/rec2/content_check.py`
- [ ] SC-02: (B20 고침) 목록 1155 행이 처리 규칙대로 고쳐졌다 — `condition` · `measure` 68 행은 줄이 BASE 그대로이고 정정 파일에 옛 · 새 참조 행이 있으며, `unresolved` 7 행은 줄의 그 번호가 BASE 그대로이고 사람 확인 목록에 행이 있으며, 나머지 `prose` · `record` 행은 줄이 「BASE 줄의 번호 자리만 새 번호로 바꾼 줄」 과 글자까지 같고 `prose` 는 정정 파일에도 행이 있다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더에 미커밋 변경이 없을 때.
  측정: `python3 $R2/lineref.py check` 마지막 줄이 `SUMMARY rows=1155 in_place=1080 lineref_file=68 review=7 bad=0`, 종료 코드 0.
  알려진 답: 회귀 게이트 절의 흉내 낸 사본에서 같은 명령이 `SUMMARY rows=1155 in_place=1080 lineref_file=68 review=7 bad=0` · 종료 코드 0 (2026-09-28 실측).
  음성 대조 (2026-09-28 실측): BASE 사본은 `in_place=0 lineref_file=0 review=0 bad=1155`. 1 회차 결과인 가지 끝 `5d2e349` 는 `in_place=913 lineref_file=68 review=0 bad=174` (`not-fixed-in-place` 174 줄) · 종료 코드 1. 흉내 낸 사본에서 p17 39 · 76 행을 1 회차의 뒤집힌 범위(`:1101`~`:1097`)로 되돌리면 그 두 행이 `not-fixed-in-place` 로 나오고 `bad=2`. 사람 확인 목록을 치우면 `review=0 bad=7`.
- [ ] SC-03: (B20 범위) BASE 에서 TIP 까지 `.harness/` 변경은 목록의 `record` · `prose` 줄과 정해진 새 파일뿐이다 — 기존 파일의 줄 수 변화 0, 목록 밖 줄 변경 0, 지우거나 옮긴 파일 0, 새 파일은 `*sprint-lineref*.md` · 1 회차 · 2 회차 계약의 계약 · 피드백 · 개정 파일 · `.harness/.meta/after-kaizen-0928/` 아래뿐 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: `python3 $R2/lineref.py scope --tip $TIP` 마지막 줄이 `SUMMARY scope_bad=0`, 종료 코드 0.
  알려진 답: 흉내 낸 사본 위에 `.harness/project.yaml` 첫 줄 · 허용 새 파일 `.harness/history/x-sprint-lineref-y.md` · 허용 밖 새 파일 `.harness/stray.md` 를 커밋하면 출력이 `line-not-in-list@1 .harness/project.yaml` · `new-file-outside-allowed-names .harness/stray.md` 두 줄과 `scope_bad=2`, 종료 코드 1. 그 한 판 앞(흉내 낸 사본 자체)은 `scope_bad=0` (2026-09-28 실측).
  음성 대조: `--tip` 을 빼면 종료 코드 2 로 멈춘다(`HEAD` 를 짐작하지 않는다, 2026-09-28 실측).
- [ ] SC-04: (B20 정정 파일 · 사람 확인 목록) 정정 파일이 필요한 계약 60 개마다 정정 파일이 하나씩 있고 그 밖의 정정 파일은 없으며, 파일마다 첫 줄 `# 줄 번호 정정 — <계약 파일 이름>` · 표 머리 `| 계약 줄 | 옛 참조 | 새 참조 | 대상 파일 | 처리 |` · 기준 판 `e500a63` 을 갖추고 표 행(줄 · 옛 참조 · 새 참조)이 그 계약의 목록 행(`unresolved` 제외)과 중복까지 같다. 사람 확인 목록 `.harness/.meta/after-kaizen-0928/rec-review.md` 는 표 머리 `| 기록 | 줄 | 옛 참조 | 후보 참조 | 대상 파일 | 인용 |` 를 갖추고 표 행이 `unresolved` 7 행과 같다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `python3 $R2/lineref.py files` 마지막 줄이 `SUMMARY files_expected=60 files_found=60 review_rows=7 bad=0`, 종료 코드 0. 이름 집합: `find .harness -type f -name '*sprint-lineref*.md' | LC_ALL=C sort | shasum -a 256 | cut -c1-16` 이 `aae51cb9240e20ff`.
  알려진 답: 흉내 낸 사본에서 `bad=0` · 이름 집합 지문 `aae51cb9240e20ff` (2026-09-28 실측).
  음성 대조 (2026-09-28 실측): 가지 끝 `5d2e349` 는 `bad=19` (행이 모자란 정정 파일 17 줄 `rows-<n>-missing-0-extra` · 사람 확인 목록 표 머리 · 행 2 줄), 종료 코드 1. BASE 사본은 `files_found=0 bad=62`. 흉내 낸 사본에서 사람 확인 목록을 치우면 `rows-7-missing-0-extra .harness/.meta/after-kaizen-0928/rec-review.md` 를 포함해 `bad=2`.
- [ ] SC-05: (D8 확인) 쉬운 말 목록 낱말이 든 main 커밋 271 개마다 메모가 있고, 메모가 걸린 낱말마다 `「<낱말>」 → <바꿔 쓸 말>` 줄을 담으며, 메모가 달린 커밋 집합이 그 271 개와 정확히 같다 [exact, enumerated]
  Given: 메모를 모두 단 뒤, 부모가 올리기 전. 목록 파일 지문 `shasum -a 256 ~/.claude/rules/plain-korean.md | cut -c1-16` 이 `694f07858cf9016c`, 읽기 도구 지문이 `793e5682f39120f3` 일 때 (다르면 목록이 바뀐 것이라 판정하지 않고 보고한다).
  측정: `python3 $R/plain_words.py scan | grep -c .` 이 271, `python3 $R/plain_words.py scan | cut -f1 | LC_ALL=C sort | shasum -a 256 | cut -c1-16` 이 `07bc82fc875822a0`. `python3 $R/plain_words.py check` 마지막 줄이 `SUMMARY commits=271 bad=0`, 종료 코드 0. `diff <(git notes list | cut -d' ' -f2 | LC_ALL=C sort) <(python3 $R/plain_words.py scan | cut -f1 | LC_ALL=C sort)` 출력 0 줄.
  알려진 답: 낱말 판정에 `게이트를 고치고 API(프로그램 창구)와 `오라클` 그리고 `sweep` 및 scripts/cache.py 를 봤다. 연락처` 를 넣으면 `['오라클', '게이트']` 두 낱말만 나온다 (1 회차 실측).
  음성 대조: 따로 둔 메모 참조(`GIT_NOTES_REF=refs/notes/rec-selftest`)에 첫 커밋은 바른 메모, 둘째 커밋은 낱말 줄 없는 메모를 달면 `check` 가 `missing:스키마` 한 줄 · `no-note` 269 줄 · `bad=270` 을 낸다 (1 회차 실측, 그 참조는 지웠다).
  측정 대상: `.harness/.meta/after-kaizen-0928/rec/plain_words.py`
- [ ] SC-06: 로컬 CI 와 CI 파일에만 있는 여섯 단계가 모두 통과한다 [exact, enumerated]
  Given: 모든 커밋 뒤, `TMPDIR` 을 세션 scratch 아래 새 폴더로 두고.
  측정: `TMPDIR=<scratch 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rec` 뒤 `<scratch 폴더>/ci-local/summary.txt` 에서 `grep -c 'rc=0'` 이 25, `grep -v 'rc=0'` 출력이 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐.
  이어서 여섯 명령 각각 종료 코드 0: `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh`.
  음성 대조: 판정 근거는 단계별 종료 코드다. 1 회차 QA 가 가지 끝에서 25 단계 rc=0 · 여섯 단계 rc=0 을 재었다(회귀 게이트 절).

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
  양성 대조: BASE 에서 떼어 낸 임시 작업 폴더에서 `sprint-contract-after-0924-reviewer-unverified.md` 789 행 조건 줄의 `SKILL.md:113` 을 `SKILL.md:118` 로 바꿔 커밋하고 그 판을 TIP 자리에 넣으면 `.harness/sprint-contract-after-0924-reviewer-unverified.md SEAL_OK MEASURE_ABSENT SEAL_BROKEN MEASURE_ABSENT` 한 줄이 나온다 (1 회차 실측). BASE 와 BASE 를 넣으면 0 줄.
- [ ] ER-02: 범위 밖을 건드리지 않았다 — `.harness` 밖 참조 파일 `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 가 BASE 와 같고, 원격에 `refs/notes/*` 와 가지 `chore/ak3-rec` 가 없다(올리지 않았다) [exact, enumerated]
  Given: 모든 커밋과 메모 뒤, 부모가 올리기 전. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: `git diff --quiet e500a63 $TIP -- docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 종료 코드 0. `git ls-remote origin 'refs/notes/*' | grep -c .` 이 0. `git ls-remote origin refs/heads/chore/ak3-rec | grep -c .` 이 0.
  양성 대조: `git ls-remote origin refs/heads/main | grep -c .` 이 1 (원격 조회가 살아 있음). 원격 조회가 실패하면(종료 코드 ≠ 0) 이 조건은 `[미검증]` 이다.
  측정 대상: `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md`

## Architecture

- [ ] AR-01: BASE 뒤 가지 `chore/ak3-rec` 의 모든 커밋이 맨 위 폴더 하나만 건드리고, 메시지 마지막 줄이 서명 줄이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: `for c in $(git rev-list e500a63..$TIP); do n=$(git show --name-only --format='' $c | cut -d/ -f1 | sort -u | grep -c .); s=$(git log -1 --format=%B $c | sed '/^[[:space:]]*$/d' | tail -1); [ "$n" = 1 ] && [ "$s" = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>' ] || echo "BAD $c n=$n"; done | grep -c BAD` 이 0. `git rev-list e500a63..$TIP | grep -c .` 이 1 이상.
  양성 대조: 같은 폴더 세기를 `a5152c5` 에 돌리면 17 이다 (1 회차 실측). 가지 끝 `5d2e349` 까지 BAD 0 (2026-09-28 실측).
- [ ] AR-02: BASE 에서 TIP 까지 바뀐 경로(`.harness/` 제외)가 전부 `## 범위 경계` 의 `# sprint-scope` 블록 안에 있고, 그 두 경로가 모두 바뀌었다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`, `CF=.harness/sprint-contract-after-0928-record-fixes-r2.md`.
  측정: `comm -23 <(git diff --name-only e500a63 $TIP -- . ':(exclude).harness' | sort -u) <(awk '/^# sprint-scope$/{p=1;next} p&&/^```/{p=0} p' $CF | sort -u) | grep -c .` 이 0. `git diff --name-only e500a63 $TIP -- . ':(exclude).harness' | grep -c .` 이 2.
  양성 대조: 같은 `comm` 을 `git diff --name-only a5152c5~1 a5152c5` 에 돌리면 1 이상이다.
- [ ] AR-03: 측정 도구가 봉인 전 실측 때와 같은 글자로 커밋됐다 — TIP 에 추적되고 지문이 2 회차 `$R2/lineref.py` `96c549d8cb953761` · `$R2/content_check.py` `69d5a4be44af4580`, 1 회차 셋은 바뀌지 않아 `$R/lineref.py` `4bec89e65a00cafd` · `$R/content_check.py` `d76b1fac1c43d92e` · `$R/plain_words.py` `c8435287d9a18234` 이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`.
  측정: 다섯 파일 각각 `git show $TIP:<파일> | shasum -a 256 | cut -c1-16` 이 위 값. 다섯 파일 모두 `git ls-files --error-unmatch <파일>` 종료 코드 0.
  양성 대조: 가지 끝 `5d2e349` 에는 2 회차 두 파일이 없다 (`git show 5d2e349:<파일>` 종료 코드 128).
  측정 대상: `.harness/.meta/after-kaizen-0928/rec2/lineref.py` · `.harness/.meta/after-kaizen-0928/rec2/content_check.py` · `.harness/.meta/after-kaizen-0928/rec/lineref.py` · `.harness/.meta/after-kaizen-0928/rec/content_check.py` · `.harness/.meta/after-kaizen-0928/rec/plain_words.py`
- [ ] AR-04: 부모가 읽을 기록 `.harness/.meta/after-kaizen-0928/rec-notes.md` 가 D8 메모를 단 271 커밋의 전체 해시를 모두 담고, 2 회차 수(`1155` 와 문구 `정정 파일 60`)와 사람 확인 목록 경로 `rec-review.md` 와 올리는 명령 `git push origin refs/notes/commits` 를 적었다 [exact, enumerated]
  Given: 모든 커밋 뒤. `n=.harness/.meta/after-kaizen-0928/rec-notes.md`.
  측정: `python3 $R/plain_words.py scan | cut -f1 | while read -r h; do grep -qF "$h" $n || echo "$h"; done | grep -c .` 이 0. `grep -cF '1155' $n` · `grep -cF 'rec-review.md' $n` · `grep -cF 'git push origin refs/notes/commits' $n` 각 1 이상. `grep -cF '정정 파일 60' $n` 이 1 이상.
  양성 대조: 가지 끝 `5d2e349` 의 같은 파일은 `1155` · `rec-review.md` · `정정 파일 60` 이 각 0 이다 (2026-09-28 실측). 옛 측정 `grep -cE '(^|[^0-9])60([^0-9]|$)'` 은 그 판에서도 2 줄(11 · 28 행)이 걸려 2 회차 수를 적었는지 가르지 못해 교차 진단 지적대로 문구로 좁혔다.
  측정 대상: `.harness/.meta/after-kaizen-0928/rec-notes.md`
- [ ] AR-05: 1 회차 계약이 이 계약으로 넘겨졌다 — `.harness/sprint-contract-after-0928-record-fixes.md` 의 frontmatter 가 `status: superseded` · `superseded_by: after-0928-record-fixes-r2` 이고 봉인 판정이 `SEAL_OK` · `MEASURE_OK` 그대로다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-rec)`, `O=.harness/sprint-contract-after-0928-record-fixes.md`.
  측정: `git show $TIP:$O | awk 'NR==1{next} /^---/{exit} {print}' | grep -cxE 'status: superseded|superseded_by: after-0928-record-fixes-r2'` 이 2. 작업 폴더에서 `bash -c '. harness/scripts/measure-common.sh; verify_seal "${1}"; verify_measurement "${1}"' _ $O` 의 두 줄 첫 낱말이 `SEAL_OK` · `MEASURE_OK`. `git diff --quiet $TIP -- $O` 종료 코드 0.
  양성 대조: 가지 끝 `5d2e349` 에서 첫 측정은 0 이다 (그때 `status: done`, 2026-09-28 실측).
  측정 대상: `.harness/sprint-contract-after-0928-record-fixes.md`

## Anti-patterns

- [ ] AP-02: force push 금지
  측정: ER-02 의 두 `git ls-remote` 가 0 — 이 스프린트는 아무것도 올리지 않는다.
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 (1 회차 QA 0).

## Reusability

- [ ] RE-01: N/A (측정 도구는 이 계약의 고정 판만 재는 일회용이라 공용 `scripts/` 로 올릴 대상이 아니다. 측정: 2 회차 두 파일이 `.harness/.meta/after-kaizen-0928/rec2/` 아래에 있고 `scripts/` 아래 새 파일 0 — `git diff --name-only --diff-filter=A e500a63 $(git rev-parse chore/ak3-rec) -- scripts | grep -c .` 이 0)
- [ ] RE-02: 봉인 확인은 기존 규약 함수를 다시 쓴다 — ER-01 · AR-05 의 측정이 `harness/scripts/measure-common.sh` 로 `verify_seal` · `verify_measurement` · `unpack_rev` · `scratch_dir` 를 읽고, 2 회차 도구 둘에 봉인 계산을 새로 짠 곳이 없다
  측정: `grep -cE 'sha256|digest|verify_seal' $R2/lineref.py $R2/content_check.py` 의 두 값이 모두 0 (2026-09-28 실측 0 · 0).

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only e500a63 $(git rev-parse chore/ak3-rec) | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 바꾸거나 만든 md 가운데 문서 둘 · 정정 파일 60 개 · `rec-notes.md` · `rec-review.md` 가 편집기와 같은 설정의 markdownlint 경고 0 개다 — 설정은 markdownlint-cli2 0.23.2 · `{ "config": { "MD013": false } }`
  Given: 모든 커밋 뒤. 도구가 없으면 scratch 새 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 로 설치한다.
  측정: 대상 64 파일(`docs/flutter/research-log.md` · `docs/kaizen/flutter-research-log.md` · `find .harness -type f -name '*sprint-lineref*.md'` 60 개 · `.harness/.meta/after-kaizen-0928/rec-notes.md` · `.harness/.meta/after-kaizen-0928/rec-review.md`)마다 `markdownlint-cli2 --config <설정 파일> <경로>` 출력에서 `^<경로>:[0-9]+` 줄 수가 0 이고 종료 코드 0. 직접 고친 옛 기록(`record` · `prose` 줄)은 숫자만 바뀌어 새 경고를 만들 수 없으므로 대상이 아니다.
  양성 대조: 앞 파일 사본 끝에 `#bad heading` · 빈 줄 셋 · 줄 끝 공백 둘을 붙이면 1 이상 (1 회차 실측 3 · 1 회차 QA 실측 5).
- [ ] DG-03: N/A (commands.test 는 scripts/release.sh 를 돌린다 — 이번 변경과 무관. 실제 시험은 SC-06 이 잰다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경이 기록 · 문서 · 측정 도구뿐이다)
