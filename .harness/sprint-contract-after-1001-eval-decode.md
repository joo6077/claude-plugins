---
feature: "평가 실행기 — 잘못된 UTF-8 · 쓰이지 않는 target_skill 읽기"
slug: after-1001-eval-decode
created: "2026-10-01 14:39"
complexity: "복잡"
conditions: 22
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:41fe586b4b54ea5f
measurement_digest: sha256:e9d05f9ca834ad3c
locked_at: "2026-10-01 15:09"
---

## 배경

- 묶음 ev3. 출처는 `.harness/.meta/after-kaizen-0928/ev2-notes.md` 「남은 것 (막지 않는 약점)」 1 번(`target_skill` 읽는 줄)과 3 번(잘못된 UTF-8 문자). 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev3`, 가지 `chore/ak3-ev3`, 시작 판 `BASE` = `9390bf96` (가지 `chore/ak3-ev2` 끝 — ev2 QA 승인, 아직 main 에 안 합쳐짐). 그 위에서 이어 한다.
- 사용자가 할 일: 없음.
- 킷 폴더 밖(`scripts/` · `.github/`)만 바뀌므로 킷 릴리스는 없다.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-ev3` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 다시 돌린 뒤 W 맨 위 폴더에서 root 가 아닌 사용자로, 환경 변수 `PYTHONINTMAXSTRDIGITS` 없이 잰다. 이 가지는 이 스프린트만 커밋한다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. `TMPDIR` 는 scratch 아래 절대 경로 폴더로 둔다.

용어 (조건마다 되풀이하지 않는다):

- 「세 도구」 = `python3 scripts/run-evals.py`(인자 없음) · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/sync-evals.py`(옵션 없음). 도우미 이름 `run` · `sync-check` · `sync-plain`.
- 「킷 셋 트리」 = 임시 폴더에 W 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py` 사본과 킷 `a` · `b` · `c` 를 적은 마켓 목록(`.claude-plugin/marketplace.json`), 킷마다 스킬 `s` 와 그 스킬 항목 하나짜리 `evals/evals.json` 을 둔 트리. `extra` 가 참이면 킷마다 평가에 없는 스킬 `extra` 를 더 둔다(앞 묶음 도우미 `content_tree` 를 그대로 부른다).
- 「쟀다」 = 그 킷 칸(`→ <킷>` 줄부터 다음 `→` 줄 앞까지)에 `run` 은 `PASS: 1 passed, 0 failed`, `sync-check` 는 `[<킷>] MISSING: extra`, `sync-plain` 은 `[<킷>] added 1 skeleton entries` 가 있다.
- 「요약 줄」 = 마지막 `→` 줄 뒤의 요약 줄 목록이 정확히 `못 읽은 킷 1 개: b` 하나다. 출력은 표준 출력과 표준 오류를 한 흐름으로 모아 `PYTHONUNBUFFERED=1` 로 받는다.
- 「정상 항목」 = `{"id":1,"skill":"s","prompt":"p","expected_output":"e","assertions":[{"text":"a","type":"output"}]}`.
- 「읽기 오류 셋」(도우미 `READ_ERRORS`, 이 차례 그대로 · 두 시험 파일의 새 경우도 이 차례):

| 이름표 | `b/evals/evals.json` 바이트 | 오류 줄에 경로와 함께 있어야 할 낱말 |
| --- | --- | --- |
| `bad-utf8` | `{"evals":[<정상 항목>]}` 에서 `"prompt":"p"` 의 `p` 뒤에 바이트 `0xFF` 하나 | `utf-8` (대소문자 가리지 않음) |
| `big-number` | `{"evals":[<정상 항목>]}` 에서 `"id":1` 을 `1` 이 5000 자리인 숫자로 | 없음(경로만) |
| `deep-nest` | `{"evals":[<정상 항목>],"x":` + `[` 200000 개 + `]` 200000 개 + `}` | 없음(경로만) |

- 「마켓 목록 읽기 오류 셋」(도우미 `MARKET_ERRORS`) — `market-utf8` = `{"plugins":[{"name":"a","source":"./a<0xFF>"}]}`, `market-broken` = `{ broken`, `market-missing` = 마켓 목록 파일을 지움.
- 「지나친 판」(도우미 `OVERSTRICT`) — 두 실행기 맨 앞에, 이름이 `evals.json` 인 파일을 읽으면 늘 `UnicodeDecodeError` 를 내는 줄을 붙인 W 도구 사본. 정상 킷도 못 읽은 킷으로 센다.

항목별 처리 방침 (결정):

- **(1) 무엇을 고치나** — 두 실행기의 평가 파일 읽기(`run-evals.py` 132 줄 · `sync-evals.py` 117 줄)는 `FileNotFoundError` · `OSError` · `json.JSONDecodeError` 만 받는다. 잘못된 UTF-8 문자(`UnicodeDecodeError`), 자릿수 한도 4300 을 넘는 숫자(`ValueError`), 너무 깊은 중첩(`RecursionError`)은 그 셋에 안 걸려 세 도구 모두 오류 추적을 찍고 1 로 끝나 뒤 킷을 재지 못한다(봉인 전 재현 — 아래 GAP). 이 셋도 그 킷을 못 읽은 킷으로 세고, 경로와 까닭 한 줄을 찍고, 나머지 킷을 끝까지 잰 뒤 끝에 `못 읽은 킷 N 개: …` 요약 줄과 2 로 끝낸다. 새 요약 줄 모양 · 새 종료 코드 값은 만들지 않는다.
- **(2) 같은 처리로 맞출 다른 읽기 자리** — 두 실행기의 파일 · 폴더 읽기 자리를 grep(`read_text` · `open(` · `json.load` · `iterdir` · `load_marketplace`)으로 모두 찾았다(아래 GAP 표). 그중 오류 추적으로 죽는 자리는 (a) 마켓 목록 읽기(`run-evals.py` 44 줄이 부르는 `plugin_utils.load_marketplace` · `sync-evals.py` 44 줄) — 잘못된 UTF-8 · 깨진 JSON · 파일 없음 모두 추적 · 1, (b) `sync-evals.py` 의 skills 폴더 목록 읽기(`discover_skills` 의 `iterdir`) — 읽기 권한이 없으면 `PermissionError` 추적 · 1. (a) 는 킷이 아니라 잴 킷 목록 자체라 「못 읽은 킷」 으로 셀 수 없다 — 경로와 까닭 한 줄을 찍고 킷을 하나도 재지 않고 2 로 끝낸다. (b) 는 평가 파일과 같이 그 킷을 못 읽은 킷으로 센다. `run-evals.py` 의 스킬 파일 확인(`_asset_exists` 의 `exists()`)은 내용을 읽지 않고, 권한이 없으면 지금도 추적 없이 FAIL 1 을 낸다 — 바꾸지 않는다(`## 범위 경계`).
- **(3) `target_skill`** — `sync-evals.py` 174 줄 `get_skill_field` 의 `entry.get("target_skill")` 은 허용 목록에 그 열쇠가 없어 앞에서 「모르는 열쇠」 2 가 나므로 닿지 않는다. 레포 사용 0 회(`git grep -n target_skill` 이 이 줄 하나)라 읽는 줄을 지운다. 허용 목록은 넓히지 않는다 — 그 열쇠를 가진 항목은 지금처럼 구조 오류 2 다.
- **(4) 시험** — `scripts/test-run-evals.py` 에 경우 34 ~ 38, `scripts/test-sync-evals.py` 에 경우 29 ~ 34 를 더한다: 킷 셋 가운데 b 만 읽기 오류 셋(34 ~ 36 · 29 ~ 31, 나머지 둘은 재고 끝에 2), 마켓 목록 잘못된 UTF-8(37 · 32, 2 · 경로 한 줄 · 추적 없음), sync 만 가운데 b 의 skills 폴더 권한 없음(33), 킷 셋 모두 정상(38 · 34, 세 칸 · 0). 읽기 오류 경우는 시작 판이 실패하고, 정상 킷 셋 경우는 시작 판도 통과하므로 그 음성 대조는 지나친 판이다. CI 는 두 시험을 이미 돌리므로 단계 이름의 경우 수와 낱말만 맞춘다.
- **(5) 마켓 목록 처리를 어디 두나** — 두 실행기 안(킷 목록을 만드는 자리)에서 받는다. `scripts/plugin_utils.py` 의 `load_marketplace` 는 다른 스크립트 다섯이 함께 쓰므로 고치지 않는다.

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 읽은 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `scripts/run-evals.py` | 19 ~ 25 줄(설명) · 43 ~ 51 줄 `eval_kits` · 118 ~ 153 줄 `load_evals` · 161 ~ 167 줄 `_asset_exists` · 252 ~ 299 줄 `main` | 읽기 자리 둘: 132 줄 평가 파일(`ValueError` · `RecursionError` 안 받음), 44 줄 마켓 목록(아무것도 안 받음). 스킬 확인은 `exists()` 라 내용 읽기 아님 | 스크립트-01 ~ 05 · 구조-02 |
| `scripts/sync-evals.py` | 18 ~ 24 줄(설명) · 42 ~ 51 줄 `target_kits` · 111 ~ 135 줄 `load_evals` · 146 ~ 154 줄 `discover_skills` · 173 ~ 174 줄 `get_skill_field` · 202 ~ 238 줄 `process_kit` · 241 ~ 297 줄 `main` | 읽기 자리 넷: 117 줄 평가 파일(같은 구멍), 44 줄 마켓 목록, 152 줄 skills 폴더 목록(`main` 273 줄 · `process_kit` 213 줄에서 두 번), 174 줄 닿지 않는 `target_skill` | 스크립트-01 · 03 ~ 07 · 구조-02 |
| `scripts/plugin_utils.py` | 34 ~ 37 줄 `load_marketplace` · 49 ~ 54 줄 `read_text` | 마켓 목록을 받지 않고 그대로 올린다. 다른 스크립트 다섯이 함께 쓴다 | 방침 (5) — 고치지 않음 |
| `scripts/test-run-evals.py` · `scripts/test-sync-evals.py` | 전체 | 경우 33 · 28 개. 내용을 글로만 써서 잘못된 바이트 경우가 없다. sync 시험은 잠근 파일을 `0o644` 로 돌려 폴더 잠금에는 맞지 않는다 | 스크립트-05 · 구조-02 |
| `.github/workflows/ci.yml` | 38 · 54 줄 | 이름 「스물여덟 경우」 · 「서른세 경우」 | 스크립트-05 |
| 레포 평가 파일(마켓 목록 킷의 `evals/evals.json`) | 앞 묶음 셈 도구 | 122 항목, 잘못된 UTF-8 · 큰 숫자 · 깊은 중첩 없음 — 결과가 안 바뀐다 | 오류-01 |
| 앞 묶음 측정 `.harness/.meta/after-1001-eval-item-shape/measure.py` 외 셋 | 전체 | 두 실행기 · 두 시험 · CI 이름을 잰다 | 오류-02 · `## 범위 경계` |

봉인 전 실측 (W 시작 판 `9390bf96`, 2026-10-01, Python 3.14.3):

- (1) 킷 셋 트리에서 b 를 읽기 오류 셋으로 두면 세 도구 아홉 경우 모두 오류 추적 · 1 이고 c 를 재지 않는다(`m 스크립트-01` `cases=9 right=0`). 끝 줄은 `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff …` · `ValueError: Exceeds the limit (4300 digits) …` · `RecursionError: Stack overflow …`. 이름 준 킷 b 도 셋 모두 같다(`m 스크립트-02` `right=0`).
- (2) 마켓 목록 읽기 오류 셋은 세 도구 아홉 경우 모두 추적 · 1(`m 스크립트-03` `right=0`). skills 폴더 권한 없음은 `sync-check` · `sync-plain` 이 `PermissionError` 추적 · 1(`m 스크립트-07` `right=0`), `run` 은 추적 없이 `Total: 2 passed, 1 failed` · 1.
- (3) `git grep -n target_skill -- scripts .github` → `scripts/sync-evals.py:174` 한 줄. 그 열쇠를 가진 항목은 지금도 세 도구 모두 2 · 모르는 열쇠 줄(`m 스크립트-06` `hits=1 … right=3`).
- (4) 레포에서 `run-evals.py --verbose` → `Total: 122 passed, 0 failed` · 0, `sync-evals.py --check-only` → `Total: 0 added, 0 orphans, 0 missing (preview)` · 0 (`m 오류-01` 의 `totals_ok=1`).

## Skill

- [ ] 스킬-00: N/A (이번 변경에 스킬 파일이 없다. 측정: `git diff --name-only 9390bf96..chore/ak3-ev3 -- '*SKILL.md' | grep -c .` 이 0)

## Script

- [ ] 스크립트-01: 평가 파일 읽기 오류를 못 읽은 킷으로 세고 나머지 킷을 끝까지 잰다 — 킷 셋 트리(extra 참)에서 b 를 읽기 오류 셋 각각으로 두면 세 도구가 각각 종료 코드 2 이고, 경로 `b/evals/evals.json` 이 든 줄(`bad-utf8` 은 같은 줄에 `utf-8`)이 있고, `Traceback` 이 없고, `a` · `c` 를 쟀고, 요약 줄이 `못 읽은 킷 1 개: b` 이며, 도구가 돈 뒤 `b/evals/evals.json` 바이트가 그대로다. Given 공통 전제 G, When `m 스크립트-01`, Then 아홉 줄 `OK` · `cases=9 right=9 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` (도우미 `READ_ERRORS` · `TOOLS` · `read_matrix`). 시작 판 아홉 줄 모두 `BAD` · `cases=9 right=0 ok=0` · 종료 코드 1 (결함 재현). 구현 뒤 모양 사본 `right=9` · 0
  음성 대조: `m 스크립트-01-base` 가 시작 판 도구 셋(`git show 9390bf96:` 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py`)으로 스크립트-01 · 02 · 03 · 07 의 스물세 경우를 돌려 모두 `BAD` · `cases=23 base_right=0 base_all_wrong=1` · 종료 코드 0 (봉인 전 실측 그대로)
- [ ] 스크립트-02: 이름으로 준 킷도 같다 — 킷 셋 트리(extra 거짓)에서 b 를 읽기 오류 셋 각각으로 두고 `python3 scripts/run-evals.py b` 를 부르면 종료 코드 2 이고, 스크립트-01 과 같은 경로 줄이 있고, `Traceback` 이 없고, 출력에 `못 읽은 킷 1 개: b` 가 있다. Given 공통 전제 G, When `m 스크립트-02`, Then 세 줄 `OK` · `cases=3 right=3 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02` (도우미 `named_matrix`). 시작 판 세 줄 모두 `BAD` · `right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=3` · 0
  음성 대조: 스크립트-01 의 `m 스크립트-01-base` 가 시작 판으로 이 세 경우도 돌려 모두 `BAD` 를 낸다
- [ ] 스크립트-03: 마켓 목록을 못 읽으면 한 줄로 알리고 2 로 끝난다 — 킷 셋 트리에서 마켓 목록을 `market-utf8` · `market-broken` · `market-missing` 각각으로 두면 세 도구가 각각 종료 코드 2 이고, 출력에 `.claude-plugin/marketplace.json` 이 든 줄이 있고, `Traceback` 이 없고, `→ ` 로 시작하는 줄이 0 개다. Given 공통 전제 G, When `m 스크립트-03`, Then 아홉 줄 `OK` · `cases=9 right=9 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03` (도우미 `MARKET_ERRORS` · `market_matrix`). 시작 판 아홉 줄 모두 `BAD` · `right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=9` · 0
  음성 대조: `m 스크립트-01-base` 가 시작 판으로 이 아홉 경우도 돌려 모두 `BAD` 를 낸다
- [ ] 스크립트-04: 정상 킷 셋은 그대로 넘긴다 — 킷 셋 트리(extra 거짓, 세 킷 모두 정상)에서 세 도구가 각각 종료 코드 0 이고, 킷 칸이 정확히 `a` · `b` · `c` 셋이고, 출력에 `ERROR` · `UNREADABLE` · `Traceback` · `못 읽은 킷` 글자가 없고, `run` 은 세 칸 모두 `PASS: 1 passed, 0 failed` 를 갖는다. 지나친 판은 같은 세 경우에서 하나도 맞히지 못한다. Given 공통 전제 G, When `m 스크립트-04`, Then 세 줄 `OK` · `cases=3 right=3 ok=1 mut_right=0 mut_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04` (도우미 `good_cases` · `OVERSTRICT` · `tool_dir`). 시작 판 `right=3 ok=1 mut_right=0 mut_ok=1` · 0 (지킬 동작). 구현 뒤 모양 사본 같음 · 0
  음성 대조: 지나친 판은 정상 킷을 못 읽은 것으로 치는 판이다 — 이 조건의 세 경우가 그 판을 모두 잡는다(`mut_ok`)
- [ ] 스크립트-05: 시험 두 파일이 새 경우를 갖고 옛 판 · 지나친 판을 가른다 — `python3 scripts/test-run-evals.py` 끝 줄 `경우 38 개 중 통과 38` · `python3 scripts/test-sync-evals.py` 끝 줄 `경우 34 개 중 통과 34` · 둘 다 종료 코드 0 이다. `--tool` 로 시작 판 도구(`git show 9390bf96:` 의 세 파일을 한 임시 폴더에)를 주면 run 시험은 정확히 `FAIL 경우 34` · `35` · `36` · `37` 넷만, sync 시험은 정확히 `29` · `30` · `31` · `32` · `33` 다섯만 내고 둘 다 1 이다. `--tool` 로 지나친 판을 주면 둘 다 1 이고 실패 번호에 정상 킷 셋 경우(run `38` · sync `34`)가 들어 있다. `.github/workflows/ci.yml` 에서 `run: python3 scripts/test-sync-evals.py` · `run: python3 scripts/test-run-evals.py` 단계가 각각 정확히 1 개이고, 이름에 각각 `서른네 경우` · `서른여덟 경우` 와 `잘못된 UTF-8` 이 있다. Given 공통 전제 G, When `m 스크립트-05`, Then `run_ok=1 sync_ok=1 run_base_fails=34,35,36,37 run_base_ok=1 sync_base_fails=29,30,31,32,33 sync_base_ok=1 run_mut_ok=1 sync_mut_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-05` (도우미 `m_tests` · `tool_dir` · `OVERSTRICT`). 시작 판 `run_tail=[경우 33 개 중 통과 33] run_ok=0 sync_tail=[경우 28 개 중 통과 28] sync_ok=0 … ci_ok=0` · 종료 코드 1. 구현 뒤 모양 사본 모든 `_ok` 값 1 · 0 (`run_mut_fails` · `sync_mut_fails` 의 나머지 번호는 구현의 검사 차례에 따라 달라질 수 있어 정상 킷 셋 경우가 들어 있는지만 잰다)
  음성 대조: 시작 판 도구는 새 읽기 오류 경우에서만, 지나친 판은 정상 킷 셋 경우에서 실패한다 — 시험이 두 방향 결함을 따로 가른다
- [ ] 스크립트-06: 닿지 않는 `target_skill` 읽기를 지웠고 허용 목록은 그대로다 — `git grep -n target_skill -- scripts .github` 출력이 0 줄이고, 킷 셋 트리(extra 참)에서 b 의 정상 항목에 `"target_skill":"s"` 를 더하면 세 도구가 각각 종료 코드 2 · 같은 줄에 경로 `b/evals/evals.json` 과 `1 번째 항목` · `target_skill` · `Traceback` 없음 · a c 잼 · 요약 줄 `못 읽은 킷 1 개: b` · b 바이트 그대로다. Given 공통 전제 G, When `m 스크립트-06`, Then `hits=0 hits_ok=1 cases=3 right=3 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-06` (도우미 `m_target` 이 ev2 도우미 `bad_matrix` 를 부른다). 시작 판 `HIT scripts/sync-evals.py:174:…` · `hits=1 hits_ok=0 cases=3 right=3 ok=1` · 종료 코드 1. 구현 뒤 모양 사본 `hits=0` · 0
  음성 대조: 시작 판이 `hits=1` 로 1 을 낸다. 허용 목록을 넓혀 `target_skill` 을 받는 판은 세 경우가 2 가 아니게 되어 `right` 가 3 보다 작다
- [ ] 스크립트-07: sync 가 skills 폴더를 못 읽는 킷을 못 읽은 킷으로 센다 — 킷 셋 트리(extra 참)에서 `b/skills` 폴더의 권한을 모두 빼면 `sync-check` · `sync-plain` 이 각각 종료 코드 2 이고, 경로 `b/skills` 가 든 줄이 있고, `Traceback` 이 없고, `a` · `c` 를 쟀고, 요약 줄이 `못 읽은 킷 1 개: b` 다. Given 공통 전제 G, When `m 스크립트-07`, Then 두 줄 `OK` · `cases=2 right=2 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-07` (도우미 `skills_dir_matrix`, root 로 돌면 2). 시작 판 두 줄 모두 `BAD` · `cases=2 right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=2` · 0
  음성 대조: `m 스크립트-01-base` 가 시작 판으로 이 두 경우도 돌려 모두 `BAD` 를 낸다

## Error

- [ ] 오류-01: 정상 입력 전체 대조 — 레포 평가 파일 전부를 옮긴 임시 트리(마켓 목록 · 킷마다 `evals/evals.json` · `skills/*/SKILL.md` · `agents/*.md`)에서 열한 명령 `run-evals.py --verbose` · `sync-evals.py --check-only` · `run-evals.py <킷> --verbose`(harness · flutter-toolkit · design-kit · backend-kit · infra-kit · rust-kit · react-kit · tone-kit · api-kit)의 종료 코드와 출력이 시작 판 도구로 돌린 것과 글자까지 같고 모두 0 이며, 앞 두 명령의 끝 줄이 `Total: 122 passed, 0 failed` · `Total: 0 added, 0 orphans, 0 missing (preview)` 이고, `sync-evals.py`(옵션 없음)가 0 이며 평가 파일을 하나도 바꾸지 않는다. 지나친 판은 열한 명령 모두에서 시작 판과 다르다. Given 공통 전제 G, When `m 오류-01`, Then 열한 줄 `OK` · `cmds=11 same=11 ok=1 totals_ok=1 plain_ok=1 mut_differs=11 mut_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01` (도우미 `m_keep` 이 ev2 도우미 `keep_run` · `mirror` · `KEEP_CMDS` 를 부른다). 시작 판 같은 값 · 0 (지킬 동작). 구현 뒤 모양 사본 같은 값 · 0
  음성 대조: 지나친 판(`OVERSTRICT`)은 레포 평가 파일 전부를 못 읽은 것으로 쳐 열한 명령 모두 출력이 달라진다 — 이 대조가 너무 넓게 받는 구현을 잡는다
- [ ] 오류-02: 앞 묶음 ev2 측정이 그대로다 — `python3 .harness/.meta/after-1001-eval-item-shape/measure.py <조건>` 의 `스크립트-01` · `스크립트-01-base` · `스크립트-02` · `스크립트-03` · `스크립트-05` · `오류-01` · `오류-02` · `구조-02` 여덟 개가 모두 종료 코드 0 이다. Given 공통 전제 G, When `m 오류-02`, Then 여덟 줄 `OK` · `cases=8 zero=8 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02` (도우미 `PRIOR`). 시작 판 `cases=8 zero=8 ok=1` · 0 (지킬 동작). 구현 뒤 모양 사본 같음 · 0 (「더하라」 조건 스크립트-01 ~ 07 · 구조-02 와 「그대로」 조건 오류-01 · 02 가 함께 겨누는 두 실행기 · 두 시험 · CI 파일에서 부딪히지 않는다)

## Architecture

- [ ] 구조-01: 커밋 규칙 — `9390bf96..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(`scripts` · `.github` · `.harness` 는 서로 다른 폴더)이며, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이고, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-01`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-01` (tail `m_commits` 를 이 기준 판 · 계약으로). 시작 판 `commits=0 bad=0` · 종료 코드 1 (커밋이 0 개). 구현 뒤 모양 사본 `commits` 1 이상 · `bad=0` · 0
- [ ] 구조-02: 설명 글이 새 동작을 적는다 — `scripts/run-evals.py` · `scripts/sync-evals.py` 맨 앞 설명(첫 `"""` 덩어리)에 `잘못된 UTF-8` · `마켓 목록` 이 있고, `scripts/test-run-evals.py` 맨 앞 설명에 두 칸 들여 쓴 `34 ~ 36.` · `37.` · `38.` 항목과 `잘못된 UTF-8`, `scripts/test-sync-evals.py` 맨 앞 설명에 `29 ~ 31.` · `32.` · `33.` · `34.` 항목과 `잘못된 UTF-8` 이 있다. Given 공통 전제 G, When `m 구조-02`, Then `miss=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02` (도우미 `m_usage` 의 `need`). 시작 판 `miss=[run-evals.py:잘못된 UTF-8,run-evals.py:마켓 목록,sync-evals.py:잘못된 UTF-8,sync-evals.py:마켓 목록,test-run-evals.py:34 ~ 36.,test-run-evals.py:37.,test-run-evals.py:38.,test-run-evals.py:잘못된 UTF-8,test-sync-evals.py:29 ~ 31.,test-sync-evals.py:32.,test-sync-evals.py:33.,test-sync-evals.py:34.,test-sync-evals.py:잘못된 UTF-8] ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `miss=[] ok=1` · 0
- [ ] 구조-03: 기록 — `.harness/.meta/after-kaizen-0928/ev3-notes.md` 에 낱말 `잘못된 UTF-8` · `target_skill` · `마켓 목록` · `skills 폴더` · `run-evals` · `sync-evals` · `못 읽은 킷` · `122` · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 3 개 이상이 있다. Given 공통 전제 G, When `m 구조-03`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03`. 시작 판 파일 없음 · `keys_ok=0` · 종료 코드 1

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-ev3` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 새 기록 `.harness/.meta/after-kaizen-0928/ev3-notes.md` 에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 코드는 두 실행기 안의 받는 오류 몇 줄과 기존 시험 파일의 경우뿐이고, 시험은 CI 에 등록돼 누구나 부른다 — 스크립트-05 `ci_ok`)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 새 검사 · 새 시험 파일을 만들지 않고 기존 파일을 고친다 — `git diff --name-status 9390bf96..chore/ak3-ev3 -- scripts .github` 에 `A` 줄 0. 읽기 오류는 이미 있는 「못 읽은 킷」 길 · `UNREADABLE` 표시 · 요약 줄로 보낸다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only 9390bf96..chore/ak3-ev3 | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.py` 넷(`scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/test-run-evals.py` · `scripts/test-sync-evals.py`)은 `python3 -m py_compile` 종료 코드 0, 새 `.md` 하나(`.harness/.meta/after-kaizen-0928/ev3-notes.md`)는 markdownlint-cli2(MD013 끔) 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`
  측정: `<scratch>/ev2/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/ev2/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(markdownlint-cli2 v0.23.3, 설정 파일 내용 `{ "config": { "MD013": false } }`, `<scratch>` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`). 시작 판 `.py` 넷 종료 코드 0. 양성 대조: 같은 명령으로 잰 `<scratch>/ev2/pos.md`(여는 fence 언어 없음 · 제목 건너뜀) → 경고 2(MD001 · MD040) · `Linting: 1 file`
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 실행기 스크립트 · 시험 · CI 파일 · 기록. 측정: git diff --name-only 9390bf96..chore/ak3-ev3 -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/)' 이 0)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash scripts/ci-local.sh <W>` (W 맨 위 폴더에서, TMPDIR 은 scratch 아래 새 폴더. 레포 밖 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 지금 없다 — 봉인 전 확인)의 끝 줄이 정확히 `steps=56 run=51 skip=5 unsupported=0 failed=0` 이고 `FAIL` 로 시작하는 줄이 0 · 종료 코드 0, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `python3 scripts/test-run-evals.py` · `python3 scripts/test-sync-evals.py` 를 따로 돌린 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 ci-local 끝 줄 · `grep -c '^FAIL'`. 봉인 전 시작 판 · 구현 뒤 모양 사본 값은 `## 회귀 게이트` 에 적는다

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
scripts/run-evals.py
scripts/sync-evals.py
scripts/test-run-evals.py
scripts/test-sync-evals.py
.github/workflows/ci.yml
```

- 하지 않는 것: `scripts/plugin_utils.py` 고치기(방침 (5)), `target_skill` 을 허용 목록에 넣기(레포 0 회), `run-evals.py` 의 스킬 파일 확인(`exists()`)이 권한 없는 skills 폴더에서 「SKILL.md도 agent .md도 없음」 FAIL 1 을 내는 것 바꾸기(추적으로 죽지 않고 그 킷을 실패로 센다 — 까닭 글만 어긋난다. `남긴 것` 에 적는다), 평가 파일 맨 바깥 열쇠 검사, 마켓 목록의 내용 모양(객체 · `plugins` 목록) 검사(읽기 오류가 아니다), `SKIP_KITS` 에 적힌 킷의 판정, `scripts/check-user-hook-copies.py` 의 레포 본 없음 추적 출력, 킷 버전 올리기 · 릴리스 · 합치기 · push, 레포 밖 파일, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일.
- 문서 사이트 대응 페이지: 바뀌는 파일은 `scripts/` · `.github/` 뿐이고 이 두 스크립트의 동작을 옮긴 `docs/` 페이지는 없다(`git grep -c 'scripts/run-evals.py\|scripts/sync-evals.py' -- docs` 0 건, 봉인 전 확인) — 맞출 페이지가 없다.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약은 `status: done` 이고 이 계약의 조건을 느슨하게 하지 않는다): ev2 계약 `스크립트-04` 는 시험 끝 줄 `경우 33 · 28` 과 CI 이름 `서른세 경우` · `스물여덟 경우` 를 잰다 — 경우가 `38` · `34` 로 늘고 이름이 `서른여덟 경우` · `서른네 경우` 로 바뀌어 1 이 된다. 경우를 더하는 쪽이라 더 엄격하다. fin `스크립트-06` · ev `스크립트-04` · end `스크립트-06` 은 시작 판에서 이미 1 이다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` · `.github/` 는 따로. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-1001-eval-decode/`) · 기록 커밋은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-1001-eval-decode/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 킷 셋 트리 · 킷 칸 · 요약 줄 · 정상 입력 대조 · CI 단계 읽기 · 커밋 규칙은 ev2 도우미 `.harness/.meta/after-1001-eval-item-shape/measure.py` 와 그 도우미가 부르는 fin · ev · tail 도우미를 불러 쓴다. `m 스크립트-01-base` 는 스크립트-01 · 02 · 03 · 07 의 음성 대조 전용 명령이다.
- `TMPDIR` 는 절대 경로로 준다.
- 봉인 전 실측(2026-10-01, W 시작 판 `9390bf96`): 스크립트-01 · 02 · 03 · 05 · 06 · 07 · 구조-01 ~ 03 종료 코드 1 (결함 재현 · 산출물 없음), 스크립트-04 · 오류-01 · 오류-02 · `스크립트-01-base` 종료 코드 0 (지킬 동작 · 음성 대조). 값은 각 조건 측정 줄에 있다.
- 진단-05 봉인 전 실측 — 시작 판(W, `npm ci` 뒤): `bash scripts/ci-local.sh <W>` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 종료 코드 0, 따로 돌린 아홉(`12/12 PASS` · `어긋남 0` · `checked=2 violations=0 infra_errors=0` · `실패 0 건` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `174 passed` · `경우 33 개 중 통과 33` · `경우 28 개 중 통과 28`) 모두 종료 코드 0. 레포 밖 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/` 는 폴더째 없어(`No such file or directory`) 레포 안 `scripts/ci-local.sh` 를 쓴다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 `<scratch>/ev3/impl` = `git clone --shared` W, 실행기 둘 · 시험 둘을 한 `scripts` 커밋, CI 이름 둘을 한 `.github` 커밋, 계약 · 도우미 · 기록을 `.harness` 커밋 셋에 서명 줄과 함께 담고 `npm ci`, 2026-10-01): 이 계약 측정 열셋(스크립트-01 ~ 07 · `스크립트-01-base`, 오류-01 · 02, 구조-01 ~ 03) 모두 종료 코드 0 (스크립트-05 `run_mut_fails=3,6,7,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38 sync_mut_fails=2,3,4,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34`, 구조-01 `commits=5 bad=0 scope_entries=5`). 같은 사본에서 `ci-local.sh` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 0, 따로 돌린 아홉 모두 0 (바뀐 끝 줄은 `경우 38 개 중 통과 38` · `경우 34 개 중 통과 34` 둘뿐), `.py` 넷 `py_compile` 0, `validate-plugin.py --check=code-fence` 0, 재사용-02 `A` 줄 0, 진단-04 세기 0. 사본의 기록 `.md` 는 끝 공백 하나로 markdownlint 경고 1(MD009) · `Linting: 1 file` 이 나왔다 — 진단-02 측정이 실제 기록에서 경고를 잡는다는 양성 대조로 쓴다.
- 진단-02 의 markdownlint 는 ev2 묶음이 `<scratch>/ev2/mdl` 에 깐 markdownlint-cli2 v0.23.3 을 그대로 쓴다. 봉인 전 같은 명령으로 `<scratch>/ev2/pos.md` 가 경고 2(MD001 · MD040) · `Linting: 1 file` 인 것을 확인했다.
- 교차 대조(봉인 전): 바뀌는 글자 · 파일(`run-evals.py` · `sync-evals.py` · `서른세 경우` · `스물여덟 경우` · `target_skill`)을 읽는 기존 검사를 `scripts/` · `.github/` · `harness/` · `package.json` · `.claude/` · `docs/` · `.harness/.meta/` 에서 `git grep` 으로 찾았다 — 레포 검사는 `.github/workflows/ci.yml` 과 두 시험 자신뿐이고(`.claude/skills/*-kaizen` · `package.json` · `.claude/kaizen-input/plugin-qa-data.md` 는 도구를 부르거나 글로 적을 뿐 — 레포 평가 파일 결과는 오류-01 이 잰다), 앞 묶음 측정 도우미 `after-0930-final` · `after-0930-eval-runners` · `after-0930-end` · `after-1001-eval-item-shape` 가 이 파일들을 읽는다. 네 도우미의 조건 쉰셋을 시작 판 W 와 구현 뒤 모양 사본(커밋 전)에서 모두 돌려 맞댔다: 바뀐 것은 ev2 `스크립트-04`(0 → 1, `## 범위 경계` 에 적은 의도한 변화) 하나뿐이다. 시작 판에서 이미 0 이 아닌 것은 fin `스크립트-06` · `구조-01` · `구조-04`(2) · `구조-05` · `재사용-02`, ev `스크립트-04` · `구조-01`, end `스크립트-06` · `구조-01` 이고 사본에서도 같다. 커밋을 담은 사본에서 ev2 `구조-01` 은 `commits=12 bad=0` · 0 이다. 「더하라」 조건(스크립트-01 ~ 07 · 구조-02)과 「그대로」 조건(오류-01 · 02 · 진단-05)이 함께 겨누는 파일은 두 실행기 · 두 시험 · `.github/workflows/ci.yml` 이고, 위 사본에서 두 쪽이 모두 종료 코드 0 이라 부딪히지 않는다. CI 파일에만 있는 단계와 범위 목록을 맞대면 범위 밖 스크립트를 고쳐야 하는 경우는 없다.
- 도우미 지문(봉인 전, `shasum -a 256 <파일> | cut -c1-16`): 이 계약 `measure.py` `34a8b26ad31b5898` · ev2 `measure.py` `98ee7757ba3a65ba` · fin `measure.py` `f066b5cdac40442c` · ev `measure.py` `e1d81f6a7352fe42` · tail `measure.py` `3d920fd41c46e7f6`.
- 오라클 해소: 진단-02 · 진단-05 — 파일 · 명령 목록을 백틱으로 적었을 뿐, 판정은 `py_compile` · markdownlint · 각 명령을 실행한 종료 코드와 끝 줄이다. 진단-02 는 양성 대조(경고 2 · 사본 기록의 경고 1)가 있다.
- 커버리지 해소: 스크립트-01 · 07 — 경로 `b/evals/evals.json` · `b/skills` 는 도우미 `read_matrix` · `skills_dir_matrix` 의 `line_ok` 인자에 글자 그대로 있고, 세 도구 명령 · 「쟀다」 글 · 요약 줄은 ev · fin 도우미의 `TOOLS` · `MEASURED` · `summary_lines` 에 있다.
- 커버리지 해소: 오류-01 — 열한 명령과 킷 이름은 ev2 도우미 `KEEP_CMDS` · `KNOWN_KITS`, 임시 트리에 옮기는 파일 종류(`evals/evals.json` · `skills/*/SKILL.md` · `agents/*.md`)는 ev2 도우미 `mirror` 에 글자 그대로 있다.
- 커버리지 해소: 구조-02 — 네 파일 경로와 찾을 낱말은 도우미 `m_usage` 의 `need` 에 글자 그대로 있다.
- 교차 진단(Step 8, 봉인 전 · 부르는 쪽이 새로 띄운 평가자): 계약 서술의 줄 번호 · 동작은 실제 코드와 어긋남 0 곳, 조건 의도와 무관하게 늘 같은 값을 내는 측정 0 개, 빈 대조 0 개, 이 범위에서 `remaining.md` 가 짚었는데 빠진 항목 0 개. 짚은 두 가지와 처리 — (가) 스크립트-04 의 지나친 판은 평가 파일 읽기 과잉만 잡고 skills 폴더 · 마켓 목록 읽기 과잉은 잡지 않는다: 그 둘을 과하게 막는 구현은 오류-01 의 열한 명령(레포 실제 마켓 목록 · skills 폴더를 읽는다)이 시작 판과 출력이 달라져 잡으므로 조건은 그대로 둔다. (나) `remaining.md` 의 B9 는 `dd607550` 이 이미 처리했는데 목록에 반영이 안 됐다: 그 파일은 이 묶음에서 읽기만 하므로 기록 `ev3-notes.md` 의 「남긴 것」 에 적는다.
