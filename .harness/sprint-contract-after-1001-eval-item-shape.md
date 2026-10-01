---
feature: "평가 실행기 — 목록 항목 모양이 깨진 평가 파일"
slug: after-1001-eval-item-shape
created: "2026-10-01 12:48"
complexity: "복잡"
conditions: 20
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:e1ba8785808ab308
measurement_digest: sha256:4c1e26738fe00e0c
locked_at: "2026-10-01 13:24"
---

## 배경

- 묶음 ev2. 출처는 PR #127 설명 「알려진 남은 것」(`{"evals":[1]}` 이면 실행기가 파이썬 오류로 1 을 낸다)과 `.harness/.meta/after-kaizen-0928/fin-notes.md` 「QA 판정과 독립 검토」 1 번 항목이다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev2`, 가지 `chore/ak3-ev2`, 시작 판 `BASE` = `b33ed94a` (`origin/main`, PR #128 합침). 통합 가지 없이 main 에서 새로 팠다.
- 사용자가 할 일: 없음.
- 킷 폴더 밖(`scripts/` · `.github/`)만 바뀌므로 킷 릴리스는 없다.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-ev2` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 다시 돌린 뒤 W 맨 위 폴더에서 root 가 아닌 사용자로 잰다. 이 가지는 이 스프린트만 커밋한다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. `TMPDIR` 는 scratch 아래 절대 경로 폴더로 둔다.

용어 (조건마다 되풀이하지 않는다):

- 「세 도구」 = `python3 scripts/run-evals.py`(인자 없음) · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/sync-evals.py`(옵션 없음). 도우미 이름 `run` · `sync-check` · `sync-plain`.
- 「킷 셋 트리」 = 임시 폴더에 W 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py` 사본과 킷 `a` · `b` · `c` 를 적은 마켓 목록, 킷마다 스킬 `s` 와 그 스킬 항목 하나짜리 `evals/evals.json` 을 둔 트리. 가운데 킷 `b` 의 평가 파일만 정한 내용으로 바꾸고, `a` · `c` 에는 평가에 없는 스킬 `extra` 를 더 둔다(앞 묶음 도우미 `content_tree` 를 그대로 부른다).
- 「쟀다」 = 그 킷 칸(`→ <킷>` 줄부터 다음 `→` 줄 앞까지)에 `run` 은 `PASS: 1 passed, 0 failed`, `sync-check` 는 `[<킷>] MISSING: extra`, `sync-plain` 은 `[<킷>] added 1 skeleton entries` 가 있다.
- 「요약 줄」 = 마지막 `→` 줄 뒤의 요약 줄 목록이 정확히 `못 읽은 킷 1 개: b` 하나다. 출력은 표준 출력과 표준 오류를 한 흐름으로 모아 `PYTHONUNBUFFERED=1` 로 받는다.
- 「구조 오류 줄」 = 경로 `b/evals/evals.json` 과 아래 표의 낱말이 모두 들어 있는 줄 하나 이상. 출력 어디에도 `Traceback` 이 없다.
- 「깨진 모양 아홉」(도우미 `BROKEN`, 이 차례 그대로 · 두 시험 파일의 새 경우도 이 차례):

| 이름표 | `b/evals/evals.json` 내용 | 구조 오류 줄의 낱말 |
| --- | --- | --- |
| `item-number` | `{"evals":[1]}` | `1 번째 항목` · `객체가 아니다` |
| `list-object` | `{"evals":{"x":1}}` | `evals` · `목록이 아니다` |
| `list-string` | `{"evals":"abc"}` | `evals` · `목록이 아니다` |
| `list-null` | `{"evals":null}` | `evals` · `목록이 아니다` |
| `no-prompt` | 정상 항목 하나에서 `"prompt":"p",` 를 뺌 | `1 번째 항목` · `prompt` |
| `skill-number` | 정상 항목의 `"skill":"s"` 를 `"skill":5` 로 | `1 번째 항목` · `skill` |
| `assertion-number` | 정상 항목의 assertions 를 `[5]` 로 | `1 번째 항목` · `assertions` |
| `unknown-key` | 정상 항목에 `"promt":"p"` 를 더함 | `1 번째 항목` · `promt` |
| `second-item` | `{"evals":[<정상 항목>,1]}` | `2 번째 항목` · `객체가 아니다` |

- 「정상 항목」 = `{"id":1,"skill":"s","prompt":"p","expected_output":"e","assertions":[{"text":"a","type":"output"}]}`.
- 「정상 모양 셋」(도우미 `GOOD`) — 레포 평가 파일이 실제로 쓰는 모양: `react-shape` = `{"tests":[{"id":"r1","skill":"s","prompt":"p","expected_output":"e","assertions":["a"]}]}`(글 id · 글 assertions, react-kit), `api-shape` = `cases` 목록에 `expect` 객체 · `example` · `fixture` 를 가진 항목(api-kit), `agent-item` = 정상 항목 뒤에 `"agent":"s"` 항목을 둔 `evals` 목록.
- 「허용 목록」 — 봉인 전에 레포 평가 파일을 센 모양이다(아래 GAP 의 실측). 항목은 객체이고, 열쇠는 `id`(정수 · 글, 참거짓은 아님) · `skill`(글) · `agent`(글) · `prompt`(글) · `expected_output`(글) · `expect`(객체) · `assertions`(목록) · `example`(글) · `fixture`(글) 아홉 가운데서만 쓴다. `id` · `prompt` · `assertions` 는 꼭 있고, `skill` · `agent` 는 정확히 하나, `expected_output` · `expect` 도 정확히 하나다. assertions 의 칸은 글이거나 열쇠가 정확히 `text` · `type`(둘 다 글)인 객체다. 목록 열쇠 `evals` · `tests` · `cases` 가 있으면 그 값은 목록이다. 이 밖의 모양은 구조 오류다(아는 모양만 통과).
- 「경계 모양 열일곱」(도우미 `PROBES`) — 허용 목록의 칸마다 하나씩 어긴 모양: 아는 열쇠 아홉마다 다른 값 모양(`id` 참거짓 · `skill` 숫자 · `agent` 숫자 · `prompt` 숫자 · `expected_output` 숫자 · `expect` 글 · `assertions` 글 · `example` 숫자 · `fixture` 숫자), assertions 칸에 모르는 열쇠 · `text` 숫자, `id` 없음 · `assertions` 없음 · `skill`·`agent` 둘 다 없음 · 둘 다 있음 · `expected_output`·`expect` 둘 다 없음 · 둘 다 있음. 구조 오류 줄 낱말은 `1 번째 항목` 과 어긴 열쇠 이름이다(도우미에 글자 그대로).

항목별 처리 방침 (결정):

- **(1) 무엇을 고치나** — 두 실행기는 평가 파일 맨 바깥이 객체인지까지만 본다. 그 안 목록 값이 목록이 아니거나 항목이 객체가 아니면 `run-evals.py` 는 `entry.get` · `prompt.strip()` 에서, `sync-evals.py` 는 `get_skill_field` · `for e in None` 에서 파이썬 오류 추적을 찍고 1 로 끝나 뒤 킷을 재지 못한다(봉인 전 재현 — 아래 GAP). 킷 하나짜리 트리에서 `prompt` 없음 · `assertions` 안 숫자 · 모르는 열쇠(오타 `promt`)는 `sync-evals.py --check-only` 가 0 으로, 모르는 열쇠는 `run-evals.py` 도 0 으로 통과한다(시작 판 도구로 새 시험을 돌린 실측 — 아래 회귀 게이트).
- **(2) 어떻게 보고하나** — 이런 파일은 지금의 「객체가 아닌 내용」 과 같은 길로 보낸다: 그 자리에서 끝내지 않고 경로 · 몇 번째 항목(1 부터 센다) · 까닭을 한 줄로 찍고, 그 킷을 못 읽은 킷으로 센 뒤 나머지 킷을 끝까지 재고 끝에 `못 읽은 킷 N 개: …` 요약 줄을 찍고 2. 새 요약 줄 모양이나 새 종료 코드 값은 만들지 않는다 — 앞 묶음이 객체가 아닌 내용을 이미 「못 읽은 킷」 으로 세고 있다.
- **(3) 모양의 기준** — 허용 목록이다(위 용어). 금지 목록으로 깨진 모양을 하나씩 막으면 오타 난 열쇠 · 처음 보는 모양이 다 통과한다. 그래서 레포 평가 파일이 지금 쓰는 열쇠와 값 모양을 세어 그것만 통과시킨다. 빈 값(`"prompt": ""`) · 자리표시 글 · assertion `type` 값 같은 내용 검사는 지금처럼 `run-evals.py` 의 FAIL(1)이다 — 모양과 내용을 가른다.
- **(4) 시험** — `scripts/test-run-evals.py` 에 경우 21 ~ 33, `scripts/test-sync-evals.py` 에 경우 16 ~ 28 을 더한다: 깨진 모양 아홉(경우 21 ~ 29 · 16 ~ 24) · 킷 셋 가운데 b 만 `{"evals":[1]}`(30 · 25, 나머지 둘은 재고 끝에 2) · 정상 모양 셋(31 ~ 33 · 26 ~ 28). 깨진 모양 경우는 시작 판이 실패하고, 정상 모양 경우는 시작 판도 통과하므로 그 음성 대조는 「아는 모양도 깨진 것으로 치는 지나친 판」 이다(도우미 `STRICT` — 평가 파일 항목마다 모르는 열쇠 하나를 끼워 읽게 하는 줄을 두 실행기 맨 앞에 붙인 사본). CI 는 두 시험을 이미 돌리므로 단계 이름의 경우 수와 낱말만 맞춘다.
- **(5) 허용 목록을 어디 두나** — 구현이 정한다. 두 실행기가 이미 `JSON_KINDS` · `UNREADABLE` 을 따로 들고 있으니 각자 두어도 되고, `scripts/plugin_utils.py` 에 하나로 두어도 된다(그때 `sync-evals.py` 가 pyyaml 을 새로 부르게 되는 점과 `test-sync-evals.py` 가 도구 옆 `plugin_utils.py` 를 복사해야 하는 점을 같이 처리한다). 어느 쪽이든 두 실행기의 판정은 스크립트-01 · 05 의 같은 모양 표로 함께 잰다.

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 읽은 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `scripts/run-evals.py` | 65 ~ 96 줄 `load_evals` · 99 ~ 101 줄 `get_eval_list` · 118 ~ 160 줄 `validate_eval_entry` · 163 ~ 192 줄 `validate_kit` · 19 ~ 24 줄(설명) | 맨 바깥 객체 검사(92 줄)만 있고 항목은 `entry.get` · `.strip()` · `a.get` 으로 바로 읽는다 | 스크립트-01 ~ 03 · 05 · 구조-02 |
| `scripts/sync-evals.py` | 58 ~ 78 줄 `load_evals` · 100 ~ 117 줄 `get_eval_list` · `get_skill_field` · 145 ~ 181 줄 `process_kit` · 184 ~ 240 줄 `main` · 18 ~ 22 줄(설명) | 같음. 목록 값을 그대로 돌고(`for e in entries`), assertions 는 읽지 않는다 | 스크립트-01 · 02 · 05 · 구조-02 |
| `scripts/test-run-evals.py` · `scripts/test-sync-evals.py` | 전체 | 경우 20 · 15 개, 목록 안 모양 경우 없음 | 스크립트-04 · 구조-02 |
| `.github/workflows/ci.yml` | 38 · 54 줄 | 이름 「열다섯 경우」 · 「스무 경우」, 「객체가 아닌」 은 맨 바깥만 뜻한다 | 스크립트-04 |
| 레포 평가 파일 10 개(마켓 목록 킷의 `evals/evals.json`) | 셈 도구 `census` 로 전부 | 아래 실측 (3) — 허용 목록의 근거 | 스크립트-05 · 오류-01 |
| 소비처 `.claude/skills/tone-kaizen/SKILL.md` 94 ~ 95 줄 · `backend-kit/README.md` 56 줄 · `infra-kit/README.md` 56 줄 · `package.json` 13 줄 · `.claude/skills/backend-kaizen/SKILL.md` 40 줄 | 해당 줄 | 킷 이름 · `--check-only` 로 부르거나 종료 코드 뜻을 적는다. 그 킷들의 평가 파일은 허용 목록 안이라 결과가 안 바뀐다 | 오류-01 |
| 앞 묶음 측정 `.harness/.meta/after-0930-final/measure.py` · `.harness/.meta/after-0930-eval-runners/measure.py` | 전체 | 두 실행기 · 두 시험 · CI 이름을 잰다 | 오류-02 · `## 범위 경계` |

봉인 전 실측 (W 시작 판 `b33ed94a`, 2026-10-01):

- (1) 킷 셋 트리에서 b 를 깨진 모양 아홉으로 두면 세 도구 스물일곱 경우 모두 어긋난다(`m 스크립트-01` `cases=27 right=0`). `{"evals":[1]}` 은 세 도구 모두 `AttributeError: 'int' object has no attribute 'get'` 추적 · 1 이고 c 를 재지 않는다. `list-null` 은 `run` 이 「항목 없음」 2(추적 없음)로, 나머지 둘은 추적 · 1 로 끝난다. `sync-plain` 은 `no-prompt` · `skill-number` · `assertion-number` · `unknown-key` 에서 0 으로 끝나고, `skill-number` 에서는 b 평가 파일에 뼈대 항목을 써 넣는다. `run` 은 `unknown-key` 에서 0 이다.
- (2) 이름으로 준 킷 b 가 깨진 모양이면 아홉 모두 어긋난다(`m 스크립트-03` `right=0`).
- (3) 레포 평가 파일 셈(`m 스크립트-05` 의 `census`): `run-evals.py` 가 읽는 9 킷(howto-kit 은 SKIP) 122 항목 — 킷별 harness 7 · flutter-toolkit 24 · design-kit 30 · backend-kit 8 · infra-kit 6 · rust-kit 17 · react-kit 21 · tone-kit 4 · api-kit 5. 항목은 모두 객체, 열쇠와 값 모양은 `agent`[str] · `assertions`[list] · `example`[str] · `expect`[dict] · `expected_output`[str] · `fixture`[str] · `id`[int, str] · `prompt`[str] · `skill`[str], assertions 칸은 `str` · `dict:text,type` 둘. 열쇠 조합은 `id·skill·prompt·expected_output·assertions` 119 · `id·agent·prompt·expected_output·assertions` 2 · `id·skill·prompt·expect·assertions` 1(+ `example` · `fixture`). `sync-evals.py` 가 읽는 `target_skill` 은 0 회라 허용 목록에 넣지 않는다.
- (4) 레포에서 `run-evals.py --verbose` → `Total: 122 passed, 0 failed` · 0, `sync-evals.py --check-only` → `Total: 0 added, 0 orphans, 0 missing (preview)` · 0.

## Skill

- [ ] 스킬-00: N/A (이번 변경에 스킬 파일이 없다. 측정: `git diff --name-only b33ed94a..chore/ak3-ev2 -- '*SKILL.md' | grep -c .` 이 0)

## Script

- [ ] 스크립트-01: 깨진 모양을 구조 오류로 보고하고 나머지 킷을 끝까지 잰다 — 킷 셋 트리에서 b 를 깨진 모양 아홉 각각으로 두면 세 도구가 각각 종료 코드 2 이고, 구조 오류 줄이 있고(그 모양의 낱말 둘이 경로와 한 줄에), `Traceback` 이 없고, `a` · `c` 를 쟀고, 요약 줄이 `못 읽은 킷 1 개: b` 이며, `sync-plain` 뒤에도 `b/evals/evals.json` 바이트가 그대로다. Given 공통 전제 G, When `m 스크립트-01`, Then 스물일곱 줄 `OK` · `cases=27 right=27 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` (도우미 `BROKEN` · `TOOLS` · `bad_matrix`). 시작 판 스물일곱 줄 모두 `BAD` · `cases=27 right=0 ok=0` · 종료 코드 1 (결함 재현). 구현 뒤 모양 사본 `right=27` · 0
  음성 대조: `m 스크립트-01-base` 가 시작 판 도구 셋(`git show b33ed94a:` 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py`)으로 깨진 모양 아홉 · 경계 모양 열일곱 × 세 도구와 이름 준 깨진 모양 아홉을 돌려 여든일곱 줄 모두 `BAD` · `cases=87 base_right=0 base_all_wrong=1` · 종료 코드 0 (봉인 전 실측 그대로)
- [ ] 스크립트-02: 레포가 쓰는 정상 모양은 그대로 넘긴다 — 킷 셋 트리(extra 없음)에서 b 를 정상 모양 셋 각각으로 두면 세 도구가 각각 종료 코드 0 이고 출력에 `ERROR` · `UNREADABLE` · `Traceback` · `못 읽은 킷` 글자가 없다. 지나친 판(`STRICT` 줄을 두 실행기 맨 앞에 붙인 W 도구 사본)은 같은 아홉 경우에서 하나도 맞히지 못한다. Given 공통 전제 G, When `m 스크립트-02`, Then 아홉 줄 `OK` · `cases=9 right=9 ok=1 mut_right=0 mut_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02` (도우미 `GOOD` · `good_cases` · `STRICT` · `tool_dir`). 시작 판 `right=9 ok=1 mut_right=9 mut_ok=0` · 종료 코드 1 (시작 판은 모양을 안 봐 지나친 판도 통과한다). 구현 뒤 모양 사본 `right=9 mut_right=0` · 0
  음성 대조: 지나친 판은 정상 모양을 깨진 것으로 치는 판이다 — 이 조건의 아홉 경우가 그 판을 모두 잡는다(`mut_ok`)
- [ ] 스크립트-03: 이름으로 준 킷도 같다 — 킷 셋 트리(extra 없음)에서 b 를 깨진 모양 아홉 각각으로 두고 `python3 scripts/run-evals.py b` 를 부르면 종료 코드 2 이고, 구조 오류 줄이 있고, `Traceback` 이 없고, 출력에 `못 읽은 킷 1 개: b` 가 있다. Given 공통 전제 G, When `m 스크립트-03`, Then 아홉 줄 `OK` · `cases=9 right=9 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03` (도우미 `named_matrix`). 시작 판 아홉 줄 모두 `BAD` · `right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=9` · 0
  음성 대조: 스크립트-01 의 `m 스크립트-01-base` 가 시작 판으로 이 아홉 경우도 돌려 모두 `BAD` 를 낸다
- [ ] 스크립트-04: 시험 두 파일이 새 경우를 갖고 옛 판 · 지나친 판을 가른다 — `python3 scripts/test-run-evals.py` 끝 줄 `경우 33 개 중 통과 33` · `python3 scripts/test-sync-evals.py` 끝 줄 `경우 28 개 중 통과 28` · 둘 다 종료 코드 0 이다. `--tool` 로 시작 판 도구(`git show b33ed94a:` 의 세 파일을 한 임시 폴더에)를 주면 run 시험은 정확히 `FAIL 경우 21` ~ `30` 열 개만, sync 시험은 정확히 `16` ~ `25` 열 개만 내고 둘 다 1 이다. `--tool` 로 지나친 판을 주면 둘 다 1 이고, 실패 번호에 정상 모양 경우가 모두 들어 있다 — run `3` · `15` · `16` · `31` · `32` · `33`, sync `2` · `12` · `13` · `26` · `27` · `28`. `.github/workflows/ci.yml` 에서 `run: python3 scripts/test-sync-evals.py` · `run: python3 scripts/test-run-evals.py` 단계가 각각 정확히 1 개이고, 이름에 각각 `스물여덟 경우` · `서른세 경우` 와 `항목 모양` 이 있다. Given 공통 전제 G, When `m 스크립트-04`, Then `run_ok=1 sync_ok=1 run_base_fails=21,22,23,24,25,26,27,28,29,30 run_base_ok=1 sync_base_fails=16,17,18,19,20,21,22,23,24,25 sync_base_ok=1 run_mut_ok=1 sync_mut_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04` (도우미 `m_tests` · `tool_dir` · `STRICT`). 시작 판 `run_tail=[경우 20 개 중 통과 20] run_ok=0 sync_tail=[경우 15 개 중 통과 15] sync_ok=0 … ci_ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `run_mut_fails=3,9,15,16,17,18,27,29,30,31,32,33 sync_mut_fails=2,6,12,13,14,22,24,25,26,27,28` 와 모든 `_ok` 값 1 · 0 (지나친 판의 나머지 실패 번호는 구현의 검사 차례에 따라 달라질 수 있어 정상 모양 경우가 들어 있는지만 잰다)
  음성 대조: 시작 판 도구는 새 깨진 모양 경우에서만, 지나친 판은 정상 모양 경우에서 실패한다 — 시험이 두 방향 결함을 따로 가른다
- [ ] 스크립트-05: 허용 목록이 레포가 쓰는 모양과 같다 — (a) 레포 평가 파일 셈이 `## GAP 분석` 실측 (3) 의 열쇠 · 값 모양 · assertions 칸 모양 · 킷별 항목 수와 같고 (b) 킷 셋 트리에서 b 를 경계 모양 열일곱 각각으로 두면 세 도구가 각각 스크립트-01 과 같은 판정(2 · 구조 오류 줄에 `1 번째 항목` 과 어긴 열쇠 이름 · 추적 없음 · a c 잼 · 요약 줄 · b 그대로)을 낸다. Given 공통 전제 G, When `m 스크립트-05`, Then `census_ok=1 cases=51 right=51 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-05` (도우미 `census` · `KNOWN_FIELDS` · `KNOWN_ASSERTIONS` · `KNOWN_KITS` · `PROBES` · `bad_matrix`). 시작 판 `census_ok=1 cases=51 right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `census_ok=1 right=51` · 0
  음성 대조: 정상 모양 셋(스크립트-02)은 허용 목록의 아는 열쇠 아홉 · 두 id 모양 · 두 assertions 칸 모양을 모두 쓴다 — 너무 좁으면 스크립트-02 가, 너무 넓으면 이 조건의 경계 모양이 걸린다. 시작 판은 `m 스크립트-01-base` 에서 이 열일곱 × 세 도구를 모두 틀린다

## Error

- [ ] 오류-01: 정상 입력 전체 대조 — 레포 평가 파일 전부를 옮긴 임시 트리(마켓 목록 · 킷마다 `evals/evals.json` · `skills/*/SKILL.md` · `agents/*.md`)에서 열한 명령 `run-evals.py --verbose` · `sync-evals.py --check-only` · `run-evals.py <킷> --verbose`(harness · flutter-toolkit · design-kit · backend-kit · infra-kit · rust-kit · react-kit · tone-kit · api-kit)의 종료 코드와 출력이 시작 판 도구로 돌린 것과 글자까지 같고 모두 0 이며, 앞 두 명령의 끝 줄이 `Total: 122 passed, 0 failed` · `Total: 0 added, 0 orphans, 0 missing (preview)` 이고, `sync-evals.py`(옵션 없음)가 0 이며 평가 파일을 하나도 바꾸지 않는다. 지나친 판은 열한 명령 모두에서 시작 판과 다르다. Given 공통 전제 G, When `m 오류-01`, Then 열한 줄 `OK` · `cmds=11 same=11 ok=1 totals_ok=1 plain_ok=1 mut_differs=11 mut_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01` (도우미 `mirror` · `KEEP_CMDS` · `keep_run` · `KNOWN_KITS`). 시작 판 `same=11 ok=1 totals_ok=1 plain_ok=1 mut_differs=0 mut_ok=0` · 종료 코드 1 (시작 판은 모양을 안 봐 지나친 판도 같다 — 음성 대조 자리만 1). 구현 뒤 모양 사본 `same=11 … mut_differs=11 mut_ok=1` · 0. 킷 이름을 주고 부르는 소비처(tone-kaizen · backend-kit · infra-kit README)의 킷은 열한 명령에 모두 들어 있다
  음성 대조: 지나친 판(`STRICT`)은 레포 평가 파일 전부를 깨진 것으로 쳐 열한 명령 모두 출력이 달라진다 — 이 대조가 허용 목록이 너무 좁은 구현을 잡는다
- [ ] 오류-02: 앞 묶음 평가 실행기 측정이 그대로다 — `python3 .harness/.meta/after-0930-final/measure.py <조건>` 의 `스크립트-01` · `스크립트-02` · `스크립트-03` · `스크립트-04` · `스크립트-05` 와 `python3 .harness/.meta/after-0930-eval-runners/measure.py <조건>` 의 `스크립트-01` · `스크립트-02` · `스크립트-03` · `오류-01` · `오류-02` 열 개가 모두 종료 코드 0 이다. Given 공통 전제 G, When `m 오류-02`, Then 열 줄 `OK` · `cases=10 zero=10 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02` (도우미 `PRIOR`). 시작 판 `cases=10 zero=10 ok=1` · 0 (지킬 동작). 구현 뒤 모양 사본 같음 · 0 (「더하라」 조건 스크립트-01 ~ 05 와 「그대로」 조건 오류-01 · 02 가 함께 겨누는 `scripts/run-evals.py` · `scripts/sync-evals.py` 에서 부딪히지 않는다)

## Architecture

- [ ] 구조-01: 커밋 규칙 — `b33ed94a..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(`scripts` · `.github` · `.harness` 는 서로 다른 폴더)이며, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이고, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-01`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-01` (tail `m_commits` 를 이 기준 판 · 계약으로). 시작 판 `commits=0 bad=0` · 종료 코드 1 (커밋이 0 개). 구현 뒤 모양 사본 `commits` 1 이상 · `bad=0` · 0
- [ ] 구조-02: 설명 글이 새 동작을 적는다 — `scripts/run-evals.py` · `scripts/sync-evals.py` 맨 앞 설명(첫 `"""` 덩어리)에 `항목 모양` · `허용 목록` 이 있고, `scripts/test-run-evals.py` 맨 앞 설명에 두 칸 들여 쓴 `21 ~ 29.` · `30.` · `31 ~ 33.` 항목과 `항목 모양`, `scripts/test-sync-evals.py` 맨 앞 설명에 `16 ~ 24.` · `25.` · `26 ~ 28.` 항목과 `항목 모양` 이 있다. Given 공통 전제 G, When `m 구조-02`, Then `miss=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02` (도우미 `m_usage` 의 `need`). 시작 판 `miss=[run-evals.py:항목 모양,run-evals.py:허용 목록,sync-evals.py:항목 모양,sync-evals.py:허용 목록,test-run-evals.py:21 ~ 29.,test-run-evals.py:30.,test-run-evals.py:31 ~ 33.,test-run-evals.py:항목 모양,test-sync-evals.py:16 ~ 24.,test-sync-evals.py:25.,test-sync-evals.py:26 ~ 28.,test-sync-evals.py:항목 모양] ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `miss=[] ok=1` · 0
- [ ] 구조-03: 기록 — `.harness/.meta/after-kaizen-0928/ev2-notes.md` 에 낱말 `항목 모양` · `허용 목록` · `run-evals` · `sync-evals` · `못 읽은 킷` · `122` · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 3 개 이상이 있다. Given 공통 전제 G, When `m 구조-03`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03`. 시작 판 파일 없음 · `keys_ok=0` · 종료 코드 1

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-ev2` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 새 기록 `.harness/.meta/after-kaizen-0928/ev2-notes.md` 에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 코드는 두 실행기 안의 모양 검사 몇 줄과 기존 시험 파일의 경우뿐이고, 시험은 CI 에 등록돼 누구나 부른다 — 스크립트-04 `ci_ok`)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 새 검사 · 새 시험 파일을 만들지 않고 기존 파일을 고친다 — `git diff --name-status b33ed94a..chore/ak3-ev2 -- scripts .github` 에 `A` 줄 0. 깨진 모양은 이미 있는 「못 읽은 킷」 길 · `UNREADABLE` 표시 · 요약 줄로 보낸다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only b33ed94a..chore/ak3-ev2 | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.py` (`scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/test-run-evals.py` · `scripts/test-sync-evals.py`, `scripts/plugin_utils.py` 를 바꿨으면 그것도)는 `python3 -m py_compile` 종료 코드 0, 새 `.md` 하나(`.harness/.meta/after-kaizen-0928/ev2-notes.md`)는 markdownlint-cli2(MD013 끔) 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`
  측정: `<scratch>/ev2/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/ev2/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(markdownlint-cli2 v0.23.3, 설정 파일 내용 `{ "config": { "MD013": false } }`, `<scratch>` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`). 시작 판 `.py` 넷 종료 코드 0. 양성 대조: 같은 명령으로 잰 `<scratch>/ev2/pos.md`(여는 fence 언어 없음 · 제목 건너뜀) → 경고 2(MD001 · MD040) · `Linting: 1 file`
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 실행기 스크립트 · 시험 · CI 파일 · 기록. 측정: git diff --name-only b33ed94a..chore/ak3-ev2 -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/)' 이 0)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash scripts/ci-local.sh <W>` (W 맨 위 폴더에서, TMPDIR 은 scratch 아래 새 폴더. 레포 밖 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 지금 없다 — 봉인 전 확인)의 끝 줄이 정확히 `steps=56 run=51 skip=5 unsupported=0 failed=0` 이고 `FAIL` 로 시작하는 줄이 0 · 종료 코드 0, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `python3 scripts/test-run-evals.py` · `python3 scripts/test-sync-evals.py` 를 따로 돌린 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 ci-local 끝 줄 · `grep -c '^FAIL'`. 봉인 전 시작 판 · 구현 뒤 모양 사본 값은 `## 회귀 게이트` 에 적는다

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다. `scripts/plugin_utils.py` 는 방침 (5) 에서 허용 목록을 하나로 둘 때만 고친다.

```text
# sprint-scope
scripts/run-evals.py
scripts/sync-evals.py
scripts/test-run-evals.py
scripts/test-sync-evals.py
scripts/plugin_utils.py
.github/workflows/ci.yml
```

- 하지 않는 것: 평가 파일 맨 바깥 열쇠(`skill_name` · `plugin` · `version` · `kit` · `runner` · `description` · `gate_blocks`) 검사(이번 대상은 목록 안 항목이다), 빈 값 · 자리표시 글 · assertion `type` 값 같은 내용 검사 바꾸기(지금처럼 FAIL 1), `sync-evals.py` 가 읽는 `target_skill` 을 허용 목록에 넣기(레포에서 0 회 — 쓰는 파일이 생기면 그때 넣는다), `SKIP_KITS` 에 적힌 킷(`harness` 는 sync 만 · `howto-kit` 은 둘 다)의 항목 모양 판정(재지 않는 킷이다), 목록 열쇠가 둘 이상인 파일(`evals` 와 `tests` 를 함께 가진 파일 — 레포에 없다)에서 어느 열쇠를 먼저 읽는지 바꾸기, `.claude/skills/backend-kaizen/SKILL.md` 40 줄 · `backend-kit/README.md` · `infra-kit/README.md` 의 종료 코드 글(그 킷 평가 파일은 허용 목록 안이고 2 의 뜻 「구조 오류」 는 그대로다), `scripts/check-user-hook-copies.py` 의 레포 본 없음 추적 출력(fin-notes 2 번 — 이번 묶음 대상이 아니다), 킷 버전 올리기 · 릴리스 · 합치기 · push, 레포 밖 파일, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일.
- 문서 사이트 대응 페이지: 바뀌는 파일은 `scripts/` · `.github/` 뿐이고 이것을 옮긴 `docs/` 페이지는 없다(`git grep -c 'scripts/run-evals.py\|scripts/sync-evals.py' -- docs` 0 건, 봉인 전 확인 — 낱말 `run-evals` 만으로 찾으면 howto-kit 의 다른 `run-evals.sh` 와 카이젠 변경 기록 세 곳이 나오는데 이 두 스크립트의 동작을 옮긴 글이 아니다) — 맞출 페이지가 없다.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약들은 `status: done` 이고 이 계약의 조건을 느슨하게 하지 않는다): fin 계약 `스크립트-06` 은 시험 끝 줄 `경우 20 · 15` 와 CI 이름 `스무 경우` · `열다섯 경우` 를 잰다 — 경우가 `33` · `28` 로 늘고 이름이 `서른세 경우` · `스물여덟 경우` 로 바뀌어 1 이 된다. ev 계약 `스크립트-04` 는 앞 묶음(fin)에서 이미 1 이다. 경우를 더하는 쪽이라 더 엄격하다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` · `.github/` 는 따로. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-1001-eval-item-shape/`) · 기록 커밋은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-1001-eval-item-shape/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 킷 셋 트리 · 킷 칸 · 요약 줄은 fin 도우미 `.harness/.meta/after-0930-final/measure.py` 를, CI 단계 읽기 · 커밋 규칙은 그 도우미가 부르는 ev · tail 도우미를 불러 쓴다. `m 스크립트-01-base` 는 스크립트-01 · 03 · 05 의 음성 대조 전용 명령이다.
- `TMPDIR` 는 절대 경로로 준다.
- 봉인 전 실측(2026-10-01, W 시작 판 `b33ed94a`): 스크립트-01 ~ 05 · 구조-01 ~ 03 · 오류-01 종료 코드 1 (결함 재현 · 산출물 없음 · 오류-01 은 `mut_differs=0` 자리만), 오류-02 · `스크립트-01-base` 종료 코드 0 (지킬 동작 · 음성 대조). 값은 각 조건 측정 줄에 있다.
- 진단-05 봉인 전 실측 — 시작 판(W, `npm ci` 뒤): `bash scripts/ci-local.sh <W>` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 종료 코드 0, 따로 돌린 아홉(`12/12 PASS` · `어긋남 0` · `checked=2 violations=0 infra_errors=0` · `실패 0 건` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `174 passed` · `경우 20 개 중 통과 20` · `경우 15 개 중 통과 15`) 모두 종료 코드 0. 레포 밖 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/` 는 폴더째 없어(`No such file or directory`) 레포 안 `scripts/ci-local.sh` 를 쓴다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 `<scratch>/ev2/impl` = `git clone --shared` W, 실행기 둘 · 시험 둘을 한 `scripts` 커밋, CI 이름 둘을 한 `.github` 커밋, 계약 · 도우미 · 기록을 `.harness` 커밋 셋에 서명 줄과 함께 담고 `npm ci`, 2026-10-01): 이 계약 측정 열하나(스크립트-01 ~ 05 · `스크립트-01-base`, 오류-01 · 02, 구조-01 ~ 03) 모두 종료 코드 0 (스크립트-01 `right=27`, 스크립트-04 `run_mut_fails=3,9,15,16,17,18,27,29,30,31,32,33 sync_mut_fails=2,6,12,13,14,22,24,25,26,27,28`, 스크립트-05 `right=51`, 오류-01 `mut_differs=11`, 구조-01 `commits=5 bad=0 scope_entries=6`). 같은 사본에서 `ci-local.sh` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 0, 따로 돌린 아홉 모두 0 (바뀐 끝 줄은 `경우 33 개 중 통과 33` · `경우 28 개 중 통과 28` 둘뿐), `.py` 넷 `py_compile` 0, 기록 `.md` markdownlint 경고 0 · `Linting: 1 file`, `validate-plugin.py --check=code-fence` 0, 재사용-02 `A` 줄 0, 진단-04 세기 0. 사본의 허용 목록은 두 실행기에 각자 둔 판이다(방침 (5) 의 한 갈래).
- 진단-02 의 markdownlint: 앞 묶음이 쓰던 `<scratch>/mdl` 설치본은 지금 `ERR_MODULE_NOT_FOUND` 로 죽어 경고 수를 0 으로 잘못 낸다(봉인 전 양성 대조 `pos.md` 에서 0 이 나와 찾았다). 그래서 `<scratch>/ev2/mdl` 에 새로 깐 markdownlint-cli2 v0.23.3 을 쓰고, 같은 명령으로 `pos.md` 가 경고 2 · `Linting: 1 file` 인 것을 봉인 전에 확인했다.
- 교차 대조(봉인 전): 바뀌는 글자 · 파일(`run-evals` · `sync-evals` · `test-run-evals` · `test-sync-evals` · `열다섯 경우` · `스무 경우` · `객체가 아닌`)을 읽는 기존 검사를 `scripts/` · `.github/` · `harness/` · `package.json` · `.claude/` · `.harness/.meta/` 에서 `git grep` 으로 찾았다 — 레포 검사는 `.github/workflows/ci.yml` 과 두 시험 자신뿐이고, 앞 묶음 측정 도우미 `after-0930-final` · `after-0930-eval-runners` · `after-0930-end` 가 이 파일들을 읽는다. 위 사본에서 세 도우미의 조건을 모두 돌렸다: fin `스크립트-01` ~ `05` · ev `스크립트-01` ~ `03` · `오류-01` · `오류-02`(오류-02 가 그대로 잰다)와 end `스크립트-01` ~ `05` · `오류-01` ~ `03` · `구조-02` · `구조-03` 은 시작 판 · 사본 모두 0. 바뀌는 것은 fin `스크립트-06`(시작 판 0 → 사본 1, 경우 수와 CI 이름이 늘어 — `## 범위 경계`)뿐이고, end `스크립트-06` · `구조-01` 과 ev `스크립트-04` 는 시작 판에서 이미 1 이다(앞 묶음에서 경우를 늘린 결과 · 다른 가지 커밋). end `스크립트-03`(Mermaid 시험)은 `node_modules` 없는 사본에서 1 이 났다가 `npm ci` 뒤 0 — 공통 전제 G 의 `npm ci` 가 필요한 까닭이다. 「더하라」 조건(스크립트-01 ~ 05 · 구조-02)과 「그대로」 조건(오류-01 · 02 · 진단-05)이 함께 겨누는 파일은 `scripts/run-evals.py` · `scripts/sync-evals.py` · 두 시험 · `.github/workflows/ci.yml` 이고, 위 사본에서 두 쪽이 모두 종료 코드 0 이라 부딪히지 않는다. CI 파일에만 있는 단계와 범위 목록을 맞대면 범위 밖 스크립트를 고쳐야 하는 경우는 없다.
- 도우미 지문(봉인 전, `shasum -a 256 <파일> | cut -c1-16`): 이 계약 `measure.py` `98ee7757ba3a65ba` · fin `measure.py` `f066b5cdac40442c` · ev `measure.py` `e1d81f6a7352fe42` · tail `measure.py` `3d920fd41c46e7f6`.
- 오라클 해소: 진단-02 · 진단-05 — 파일 · 명령 목록을 백틱으로 적었을 뿐, 판정은 `py_compile` · markdownlint · 각 명령을 실행한 종료 코드와 끝 줄이다. 진단-02 는 양성 대조(경고 2)가 있다.
- 오라클 해소: 오류-01 — 판정은 글자 찾기가 아니라 레포 평가 파일 전부로 열한 명령을 실제로 돌린 종료 코드 · 출력을 시작 판 도구 출력과 글자까지 맞댄 결과다.
- 커버리지 해소: 스크립트-01 · 03 — 깨진 모양 아홉의 내용과 낱말은 위 표와 도우미 `BROKEN` 에 글자 그대로 있고, 세 도구 명령 · 「쟀다」 글 · 요약 줄은 ev · fin 도우미의 `TOOLS` · `MEASURED` · `summary_lines` 에 있다. `m` 이 경우마다 한 줄을 찍는다.
- 커버리지 해소: 스크립트-02 · 05 — 정상 모양 셋 · 경계 모양 열일곱 · 센 모양은 도우미 `GOOD` · `PROBES` · `KNOWN_FIELDS` · `KNOWN_ASSERTIONS` · `KNOWN_KITS` 에 글자 그대로 있다.
- 커버리지 해소: 스크립트-04 — 시작 판 도구 세 파일은 `tool_dir(BASE)`, 지나친 판 줄은 `STRICT`, CI 단계 두 줄과 이름 낱말은 `m_tests` 에 글자 그대로 있다.
- 커버리지 해소: 오류-01 · 오류-02 — 열한 명령(`run-evals.py` · `sync-evals.py`)과 킷 이름은 `KEEP_CMDS` · `KNOWN_KITS`, 임시 트리에 옮기는 파일 종류(`evals/evals.json` · `skills/*/SKILL.md` · `agents/*.md`)는 `mirror`, 앞 묶음 측정 열 개는 `PRIOR` 에 글자 그대로 있다. 커버리지 검출기(6.5 (4)) 출력 두 건(오류-01 · 구조-02)은 이 줄과 아래 구조-02 줄로 처리했다.
- 커버리지 해소: 구조-02 · 구조-03 — 네 파일 경로와 찾을 낱말은 `m_usage` 의 `need`, 기록 낱말은 `m_notes` 의 `keys` 에 글자 그대로 있다.
