---
feature: "끝 — 평가 실행기 남은 다섯 · 레포 밖 훅 둘을 레포로"
slug: after-0930-final
created: "2026-10-01 09:15"
complexity: "복잡"
conditions: 28
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: "sha256:26b3fa100e0df3b3"
measurement_digest: "sha256:51181469f470782b"
locked_at: "2026-10-01 09:43"
---

## 배경

- 묶음 fin. 출처는 `.harness/.meta/after-kaizen-0928/ev-notes.md` 「QA 판정과 독립 검토」 의 남은 것 다섯(평가 실행기)과, 부모가 넘긴 「레포 밖 훅 둘을 레포로」 다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-fin`, 가지 `chore/ak3-fin`, 시작 판 `BASE` = `7fe274fc` (가지 `chore/ak3-ev` 끝 — QA APPROVE, 아직 main 에 안 합쳐짐). 그 위에서 이어 한다.
- 사용자가 할 일: 없음.
- 바뀌는 곳은 `scripts/` · `.github/` · `harness/evals/hooks/` 뿐이다. harness 는 시험 폴더만 바뀌어 동작이 바뀌지 않으므로 판 번호를 올리지 않는다 — 판단과 까닭은 기록(구조-03)에 적는다.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-fin` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 다시 돌린 뒤 W 맨 위 폴더에서 root 가 아닌 사용자로 잰다. 이 가지는 이 스프린트만 커밋한다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. `TMPDIR` 는 scratch 아래 절대 경로 폴더로 둔다.

용어 (조건마다 되풀이하지 않는다):

- 「세 도구」 = `python3 scripts/run-evals.py`(인자 없음) · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/sync-evals.py`(옵션 없음). 도우미 이름 `run` · `sync-check` · `sync-plain`.
- 「킷 셋 트리」 = 앞 묶음 ev 계약과 같은 임시 트리 — W 의 도구 세 파일 사본, 킷 `a` · `b` · `c` 를 적은 마켓 목록, 킷마다 스킬 `s` 와 그 스킬 항목 하나짜리 `evals/evals.json`. 나쁜 칸이 있는 경우에는 정상 킷마다 평가에 없는 스킬 `extra` 를 더 둔다(도우미 `content_tree`).
- 「쟀다」 = 그 킷 칸(`→ <킷>` 줄부터 다음 `→` 줄 앞까지)에 `run` 은 `PASS: 1 passed, 0 failed`, `sync-check` 는 `[<킷>] MISSING: extra`, `sync-plain` 은 `[<킷>] added 1 skeleton entries` 가 있다.
- 「요약 줄」 = 마지막 `→` 줄보다 뒤에 있는, `못 읽은 킷 ` 또는 `항목 없는 킷 ` 으로 시작하는 줄들(도우미 `summary_lines`). 기대값은 조건마다 차례까지 적는다. 출력은 표준 출력과 표준 오류를 한 흐름으로 모아 `PYTHONUNBUFFERED=1` 로 받는다.
- 「객체가 아닌 내용 다섯」 = `null` · `5` · `"x"` · `[]` · `true` (세면 안 되는 모양). 「정상 모양 셋」 = 목록 열쇠가 `evals` · `tests` · `cases` 이고 항목 하나가 맞는 객체 (넘겨야 할 모양).
- 「옮긴 세 파일」 = `harness/evals/hooks/lint-contract-oracle.sh` · `harness/evals/hooks/qa-pending-check.sh` · `harness/evals/hooks/_lib-hook-payload.sh`. 「훅 시험 둘」 = `harness/evals/hooks/lint-contract-oracle-test.sh` · `harness/evals/hooks/qa-pending-check-test.sh`. 「맞대기 검사」 = `scripts/check-user-hook-copies.py`, 그 시험 = `scripts/test-check-user-hook-copies.py`.

항목별 처리 방침 (결정):

- **(A1 · A2) 객체가 아닌 내용** — 두 실행기는 `json.loads` 결과를 그대로 쓴다. `null` 은 `None` 이라 「파일 없음」 표시와 섞여 `run` · `sync-check` · `sync-plain` 이 모두 0 으로 거짓 통과하고, 숫자 · 글 · 목록 · 참거짓은 추적 출력과 함께 1 로 끝난다(봉인 전 재현 — 아래 GAP). 읽은 내용이 객체(`dict`)가 아니면 「못 읽음」 과 같은 길로 보낸다 — 경로와 `객체가 아니다` 를 담은 오류 한 줄을 찍고, 나머지 킷을 끝까지 재고, 요약 줄 `못 읽은 킷 …` 에 이름을 적은 뒤 2. 계약상 받는 모양은 이 레포의 평가 파일 열하나가 모두 그런 것처럼 최상위가 객체인 파일뿐이다(봉인 전 확인).
- **(A3) 항목 0 개에서 멈춤** — `run-evals.py` 는 항목이 0 개인 파일에서 `sys.exit(2)` 로 그 자리에서 끝나 뒤 킷을 재지 않는다. 그 킷 이름을 모아 두고 끝까지 잰 뒤 요약 줄 `항목 없는 킷 N 개: …` 를 찍고 2. 못 읽은 킷과 함께 있으면 `못 읽은 킷` 줄이 먼저, `항목 없는 킷` 줄이 뒤다.
- **(A4) 이름으로 준 대상 없는 바로가기** — `run-evals.py <킷>` 의 인자 검사가 `is_file()` 이라 「evals/evals.json 없음」 으로 안내한다. `os.path.lexists` 로 갈라 자리가 있으면 넘겨서 `UNREADABLE <경로> (바로가기 대상 없음)` 으로 잰다. 자리가 아예 없는 킷 · 없는 킷 이름의 안내는 그대로다.
- **(A5) 두 번째 읽기** — `sync-evals.py` 는 킷마다 평가 파일을 두 번 읽는다(`main` · `process_kit`). 두 번째 읽기가 못 읽음 표시를 받으면 추적 출력으로 죽는다. 두 번째 읽기에서도 못 읽음을 확인해 그 킷을 못 읽은 킷으로 센다. 두 읽기를 하나로 합치지는 않는다(부모 지시가 「확인해 못 읽음으로」). 시험은 도구를 모듈로 불러 킷 b 의 두 번째 읽기만 못 읽음 표시를 돌려주게 바꿔 흉내 낸다(도우미 `SECOND_READ`) — 두 읽기 사이에 파일이 바뀌는 드문 경우라 실제 파일로는 만들 수 없다.
- **(A 시험)** `scripts/test-run-evals.py` 에 경우 10 ~ 20, `scripts/test-sync-evals.py` 에 경우 7 ~ 15 를 더한다(번호와 모양은 스크립트-06). 세면 안 되는 모양과 넘겨야 할 정상 모양을 둘 다 넣고, CI 단계 이름의 경우 수를 「스무 경우」 · 「열다섯 경우」 로 맞춘다.
- **(B) 훅 둘을 레포로** — 두 훅은 같은 폴더의 도우미 `_lib-hook-payload.sh` 를 `CLAUDE_HOOK_LIB`(없으면 `~/.claude/hooks/`)로 불러 쓰고, 못 찾으면 조용히 0 으로 끝난다. 훅 둘만 옮기면 CI 에서 시험이 「훅 도우미가 없다」 로 2 이므로 도우미도 함께 옮긴다(부모 지시 「두 훅」 에 도우미 하나를 더한 것 — 조건을 넓히는 쪽이 아니라 CI 에서 돌게 하는 데 꼭 필요한 파일이다). 세 파일을 설치본 바이트 그대로 `harness/evals/hooks/` 에 커밋한다. `harness/hooks/` · `hooks.json` 에는 손대지 않는다. 훅 시험 둘은 환경 변수(`LINT_ORACLE_HOOK` · `QA_PENDING_HOOK` · `CLAUDE_HOOK_LIB`)를 그대로 받되, 기본값을 이 폴더의 레포 본으로 바꾸고 `CLAUDE_HOOK_LIB` 를 훅에 넘긴다(넘기지 않으면 설치본이 없는 곳에서 훅이 도우미를 못 찾는다). `.github/workflows/ci.yml` 에 훅 시험 둘 · 맞대기 시험 · 맞대기 검사 네 단계를 더하기만 한다. 맞대기 검사는 `--installed <폴더>`(기본 `~/.claude/hooks`)를 받아 옮긴 세 파일을 바이트로 맞대고, 설치본이 하나도 없으면 `설치본 없음 — 건너뜀` 한 줄과 0, 있는 파일만 맞대어 다르면 `다름: <이름> (…)` 줄과 차이 몇 줄 · 1. `~/.claude/hooks/` 는 읽기만 한다.
- **(B 리눅스)** 봉인 전 도커(ubuntu:24.04 · LC_ALL=C.UTF-8 · mawk 1.3.4 · GNU grep 3.11)에서 설치본 사본으로 훅 시험 둘이 모두 0 이었다 — 리눅스 수정은 필요 없을 것으로 본다. 그래도 구현 중 리눅스에서 깨져 레포 본을 고치면, 설치본에 옮길 정확한 줄을 기록에 적는다(구조-05 가 그 경우를 받는다).

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 읽은 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `scripts/run-evals.py` | 61 ~ 87 줄 `load_evals` · 154 ~ 183 줄 `validate_kit` · 186 ~ 225 줄 `main` · 19 ~ 23 줄(설명) | `json.loads` 결과를 그대로 돌려준다 · 165 ~ 169 줄 항목 0 개 `sys.exit(2)` · 192 ~ 197 줄 인자 검사 `is_file()` | 스크립트-01 ~ 04 · 구조-02 |
| `scripts/sync-evals.py` | 57 ~ 72 줄 `load_evals` · 139 ~ 172 줄 `process_kit` · 175 ~ 228 줄 `main` | `json.loads` 결과를 그대로 돌려준다 · 141 줄 두 번째 읽기가 못 읽음 표시를 안 본다 · `get_eval_list` 가 `in` 으로 열쇠를 찾아 글 · 목록은 추적 없이 1 | 스크립트-01 · 02 · 05 · 구조-02 |
| `scripts/test-run-evals.py` · `scripts/test-sync-evals.py` | 전체 | 경우 9 · 6. 객체가 아닌 내용 · 다른 목록 열쇠 · 항목 0 개 다음 킷 · 이름 준 바로가기 · 두 번째 읽기 경우 없음 | 스크립트-06 · 구조-02 |
| `.github/workflows/ci.yml` | 37 ~ 39 · 53 ~ 55 · 242 ~ 243 줄 | 평가 시험 이름에 「여섯 경우」 · 「아홉 경우」. 훅 시험 둘이 없다 | 스크립트-06 · 11 |
| `~/.claude/hooks/lint-contract-oracle.sh` · `qa-pending-check.sh` · `_lib-hook-payload.sh` | 전체 (132 · 137 · 99 줄) | 두 훅이 23 · 22 줄에서 `CLAUDE_HOOK_LIB` 기본 `~/.claude/hooks/_lib-hook-payload.sh` 를 불러 쓴다 — 못 찾으면 `exit 0` | 구조-04 · 05 · 스크립트-07 |
| `harness/evals/hooks/lint-contract-oracle-test.sh` · `qa-pending-check-test.sh` | 1 ~ 13 · 1 ~ 12 줄 | 기본 훅 경로가 `$HOME/.claude/hooks/…`, `lib` 를 검사만 하고 훅에 넘기지 않는다, 머리에 「CI 에 등록하지 않는다」 | 스크립트-07 · 구조-02 |
| `harness/hooks/hooks.json` | 전체 | 세 이름 없음 — 그대로 둔다 | 구조-04 |
| `scripts/check-installed-sync.py` | 1 ~ 40 줄 | 플러그인 설치본(`~/.claude/plugins/cache`)의 skills · agents 만 맞댄다 — `~/.claude/hooks/` 는 안 본다. 새 맞대기 검사의 선례(알림 목적)일 뿐 고치지 않는다 | 재사용-02 |
| 소비처 `.claude/skills/backend-kaizen/SKILL.md` 40 줄 · `backend-kit/README.md` · `infra-kit/README.md` 56 줄 | 해당 줄 | 「못 읽거나 깨지면 나머지를 재고 2」 · 「2 = 파싱 오류」 — 새 2 까닭(객체가 아님 · 항목 0 개)과 부딪히지 않는다 | 오류-01 |

봉인 전 실측 (W 시작 판 `7fe274fc`, 2026-10-01):

- (A1) 킷 하나짜리 트리에서 내용 `null` → `run` 0 · `sync-check` 0, 추적 출력 0. 킷 셋 트리 가운데 `b` 가 `null` 이면 `run` 이 `b` 칸에 `PASS: 0 passed, 0 failed` 를 찍고 0, `sync-check` 는 `b` 를 `SKIP (no evals.json)` 로 넘기고 0.
- (A2) `5` · `true` → 두 실행기 모두 추적 출력 · 1. `"x"` · `[]` → `run` 추적 · 1, `sync-check` 추적 없이 1(스킬 차이로).
- (A3) 가운데 `b` 가 `{"evals":[]}` → `run` 이 `a` 만 재고 `b` 에서 2 로 끝나 `c` 를 안 잰다.
- (A4) `b` 가 대상 없는 바로가기일 때 `run-evals.py b` → `ERROR: 이름으로 준 킷 b — evals/evals.json 없음` · 2.
- (A5) 두 번째 읽기만 못 읽음 → `TypeError: argument of type 'object' is not a container or iterable` 추적 · 1.
- (B) `~/.claude/hooks/` 의 세 파일 지문(`shasum -a 256` 앞 16 자리)은 `lint-contract-oracle.sh` `182ed51390abd4ae` · `qa-pending-check.sh` `07c427c14a16523e` · `_lib-hook-payload.sh` `dff1e68e020a5028`, 크기 7185 · 7340 · 4512 바이트. 이 맥에서 훅 시험 둘은 `LC_ALL=C` · `en_US.UTF-8` 모두 `실패 0 건` · 0. 도커(ubuntu:24.04, 설치본 사본에 환경 변수로 경로를 넘김)도 둘 다 `실패 0 건` · 0. 시작 판 훅 시험을 빈 `HOME` 으로 돌리면 둘 다 `훅이 없다: …` · 2.

## Script

- [ ] 스크립트-01: 객체가 아닌 내용은 구조 오류 2 다 — 킷 셋 트리에서 `b/evals/evals.json` 이 객체가 아닌 내용 다섯 중 하나일 때, 세 도구가 각각 종료 코드 2 이고, `b/evals/evals.json` 과 `객체가 아니다` 를 함께 담은 줄이 있고, 출력에 `Traceback` 이 없고, `a` · `c` 를 쟀고, 요약 줄이 정확히 `못 읽은 킷 1 개: b` 하나다. Given 공통 전제 G, When `m 스크립트-01`, Then 열다섯 줄 `OK` · `cases=15 right=15 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` (도우미 `NON_OBJECT` · `TOOLS` · `content_tree` · `summary_lines`). 시작 판 열다섯 줄 모두 `BAD` · `cases=15 right=0 ok=0` · 종료 코드 1 (결함 재현). 구현 뒤 모양 사본 `right=15` · 0
  음성 대조: `m 스크립트-01-base` — 시작 판 도구 셋(`git show 7fe274fc:` 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py`)으로 같은 열다섯 경우를 돌리면 모두 `BAD` · `cases=15 base_right=0 base_all_wrong=1` · 종료 코드 0 (봉인 전 실측 그대로)
- [ ] 스크립트-02: 정상 모양은 그대로 넘긴다 — 킷 셋 트리에서 `b/evals/evals.json` 이 정상 모양 셋 중 하나일 때 세 도구가 각각 종료 코드 0 이고 출력에 `객체가 아니다` · `UNREADABLE` · `Traceback` 이 없다. 평가 파일 내용을 모두 `null` 로 읽는 지나친 판(두 도구 맨 앞에 도우미 `NULL_EVALS` 세 줄을 붙인 사본 — 마켓 목록 읽기는 그대로)은 같은 아홉 경우에서 하나도 0 이 아니다. Given 공통 전제 G, When `m 스크립트-02`, Then 아홉 줄 `OK` · `cases=9 right=9 ok=1 mut_right=0 mut_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02` (도우미 `NORMAL` · `mutant_dir` · `NULL_EVALS`). 시작 판 `right=9 ok=1 mut_right=9 mut_ok=0` · 종료 코드 1 (변이가 걸릴 자리가 없다 — 시작 판은 `null` 을 없는 파일로 넘긴다). 구현 뒤 모양 사본 `right=9 mut_right=0` · 0
  음성 대조: 변이는 정상 파일까지 객체가 아니라고 치는 지나친 판이다 — 이 조건의 아홉 경우가 그 판을 잡는다(`mut_ok`)
- [ ] 스크립트-03: 항목 0 개 킷에서 멈추지 않는다 — `run` 이 킷 셋 트리의 네 모양 ① `b-empty-list`(`b` 가 `{"evals":[]}`) ② `b-no-key`(`b` 가 `{}`) ③ `ac-empty-list`(`a` 가 `{"evals":[]}` · `c` 가 `{"tests":[]}`) ④ `b-unreadable-c-empty`(`b` 권한 0 · `c` 가 `{"cases":[]}`) 에서 각각 종료 코드 2 이고, 항목 없는 킷마다 그 `<킷>/evals/evals.json` 을 담은 줄이 있고, 나머지 킷을 모두 쟀고, 요약 줄이 차례까지 정확히 ① ② `[항목 없는 킷 1 개: b]` ③ `[항목 없는 킷 2 개: a, c]` ④ `[못 읽은 킷 1 개: b, 항목 없는 킷 1 개: c]` 다. Given 공통 전제 G, When `m 스크립트-03`, Then 네 줄 `OK` · `cases=4 right=4 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03` (도우미 `EMPTY_SETS`, root 로 돌면 2). 시작 판 네 줄 모두 `BAD` (`summary=[]`) · `cases=4 right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=4` · 0
  음성 대조: 시작 판 도구는 네 모양 모두에서 요약 줄이 없고 ① ~ ③ 은 뒤 킷을 안 잰다 — 이 측정이 W 의 도구를 직접 부르므로 그 판으로 되돌리면 그대로 1 이다(봉인 전 시작 판 실측이 그 값)
- [ ] 스크립트-04: 이름으로 준 대상 없는 바로가기는 못 읽음으로 안내한다 — 킷 셋 트리에서 `python3 scripts/run-evals.py b` 가 ① `b` 평가 파일이 대상 없는 바로가기면 종료 코드 2 · `UNREADABLE` 로 시작하고 `b/evals/evals.json` 을 담은 줄이 있고 `evals.json 없음` 글이 없다 ② `b/evals` 가 없으면 2 · 줄 `ERROR: 이름으로 준 킷 b — evals/evals.json 없음` 그대로 ③ 없는 킷 `nope` 이면 2 · 줄 `ERROR: 이름으로 준 킷 nope — 킷 폴더 없음` 그대로 ④ `b` 가 정상이면 0 · `b` 를 쟀다. Given 공통 전제 G, When `m 스크립트-04`, Then 네 줄 `OK` · `cases=4 right=4 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04`. 시작 판 `BAD named b-dangling rc=2 tail=[ERROR: 이름으로 준 킷 b — evals/evals.json 없음]` · 나머지 셋 `OK` · `cases=4 right=3 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=4` · 0
  음성 대조: ① 은 시작 판에서 `BAD` 이고 ② ③ ④ 는 시작 판에서도 `OK` 다 — 판정을 늘 「못 읽음」 으로 바꾸면 ② 가, 늘 「없음」 으로 두면 ① 이 깨진다
- [ ] 스크립트-05: 두 번째 읽기에서 못 읽으면 못 읽은 킷으로 센다 — 킷 셋 트리(정상 킷마다 `extra`)에서 `sync-evals.py` 를 모듈로 불러 킷 `b` 의 두 번째 읽기만 못 읽음 표시를 돌려주게 바꾸고(도우미 `SECOND_READ`) `--check-only` · 옵션 없이 각각 돌리면, 둘 다 종료 코드 2 이고 출력에 `Traceback` 이 없고, `a` · `c` 를 쟀고, 요약 줄이 정확히 `못 읽은 킷 1 개: b` 하나다. Given 공통 전제 G, When `m 스크립트-05`, Then 두 줄 `OK` · `cases=2 right=2 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-05`. 시작 판 두 줄 `BAD … rc=1 trace=1 measured=0 summary=0` · `cases=2 right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=2` · 0
  음성 대조: 시작 판 도구는 두 경우 모두 추적 출력 · 1 이다(봉인 전 실측) — 두 번째 읽기 확인을 지우면 이 측정이 그대로 1 로 돌아간다
- [ ] 스크립트-06: 평가 시험 두 파일이 새 경우를 갖고 옛 판 · 지나친 판을 가른다 — `python3 scripts/test-run-evals.py` 끝 줄 `경우 20 개 중 통과 20` · `python3 scripts/test-sync-evals.py` 끝 줄 `경우 15 개 중 통과 15` · 둘 다 종료 코드 0 이다. `--tool` 로 시작 판 도구(`git show 7fe274fc:` 의 세 파일을 한 임시 폴더에)를 주면 run 시험은 `FAIL 경우 10,11,12,13,14,17,18,19` 만, sync 시험은 `FAIL 경우 7,8,9,10,11,14,15` 만 내고 둘 다 1 이다. `--tool` 로 스크립트-02 의 지나친 판을 주면 run 시험은 `3,9,15,16,17,18` 만, sync 시험은 `2,6,12,13,14` 만 실패하고 둘 다 1 이다. `.github/workflows/ci.yml` 에서 `run: python3 scripts/test-run-evals.py` · `run: python3 scripts/test-sync-evals.py` 단계가 각각 정확히 1 개이고, 이름에 각각 `스무 경우` · `열다섯 경우` 가 있으며 run 쪽 이름에 `없는 킷` · `못 읽`, sync 쪽 이름에 `못 읽` 이 남아 있다. Given 공통 전제 G, When `m 스크립트-06`, Then `run_ok=1 sync_ok=1 run_base_fails=10,11,12,13,14,17,18,19 run_base_ok=1 sync_base_fails=7,8,9,10,11,14,15 sync_base_ok=1 run_mut_fails=3,9,15,16,17,18 run_mut_ok=1 sync_mut_fails=2,6,12,13,14 sync_mut_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-06` (도우미 `m_eval_tests` · `tool_dir_of` · `mutant_dir`). 시작 판 `run_tail=[경우 9 개 중 통과 9] run_ok=0 sync_tail=[경우 6 개 중 통과 6] sync_ok=0 … ci_ok=0` · 종료 코드 1. 구현 뒤 모양 사본 모든 `_ok` 값 1 · 0
  음성 대조: 시작 판 도구는 세면 안 되는 모양 · 멈춤 경우에서만, 지나친 판은 정상 모양 경우(3 · 15 · 16 / 2 · 12 · 13)와 정상 킷을 재야 하는 여러 킷 경우에서만 실패한다 — 시험이 두 방향 결함을 따로 가른다
- [ ] 스크립트-07: 훅 시험 둘이 설치본 없이 레포 본으로 돈다 — `HOME` 을 빈 임시 폴더로 두고 `CLAUDE_HOOK_LIB` · `LINT_ORACLE_HOOK` · `QA_PENDING_HOOK` 을 지운 채 훅 시험 둘을 `LC_ALL=C` · `LC_ALL=en_US.UTF-8` 로 각각 돌리면 네 번 모두 끝 줄 `실패 0 건` · 종료 코드 0 이다. 같은 빈 `HOME` 에서 ① 시험이 받는 환경 변수로 훅 자리에 `exit 0` 만 하는 대역 파일을 주면 두 시험 모두 1 ② 시험 사본에서 `export CLAUDE_HOOK_LIB=` 를 `CLAUDE_HOOK_LIB=` 로 바꿔(훅에 도우미를 안 넘김) 옮긴 세 파일 옆에서 돌리면 두 시험 모두 1 ③ 시작 판 훅 시험(`git show 7fe274fc:`)은 두 시험 모두 2 다. Given 공통 전제 G, When `m 스크립트-07`, Then `runs=4 pass=4 ok=1 stub_rcs=1,1 stub_ok=1 noexport_rcs=1,1 noexport_ok=1 base_rcs=2,2 base_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-07` (도우미 `HOOK_TESTS` · `HOOK_ENV` · `HOOK_STUB` · `hook_env`). 시작 판 `MISSING harness/evals/hooks/lint-contract-oracle.sh …` · `ok=0` · 종료 코드 1. 구현 뒤 모양 사본 위 값 그대로 · 0
  음성 대조: ① ② ③ 이 이 조건의 음성 대조다 — 훅이 아무것도 안 하거나 도우미를 못 찾으면 시험이 실패하고, 옛 기본 경로로는 설치본 없는 곳에서 준비 실패한다
- [ ] 스크립트-08: 리눅스에서도 돈다 — W 를 읽기 전용으로 붙인 도커 `ubuntu:24.04`(`LC_ALL=C.UTF-8`, `apt-get install -y jq zsh python3`)에서 훅 시험 둘과 맞대기 시험을 돌리면 셋 다 종료 코드 0 이고 끝 줄이 `실패 0 건` · `실패 0 건` · `경우 6 개 중 통과 6` 이며, 그 안의 awk 는 mawk · grep 은 GNU grep 이다. Given 공통 전제 G · 도커 데몬이 돈다, When `m 스크립트-08`, Then `results=3 mawk=1 gnu_grep=1 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-08` (도우미 `DOCKER_SCRIPT`). 도커를 못 쓰거나 apt 가 실패하면 2 (잴 수 없음 — `[미검증]` 이 아니라 다시 잰다). 시작 판 `results=3 … ok=0` · 종료 코드 1 (레포 본 훅이 없어 훅 시험 둘이 2, 맞대기 시험 파일 없음). 구현 뒤 모양 사본 `results=3 mawk=1 gnu_grep=1 ok=1` · 0
  음성 대조: 시작 판 훅 시험은 이 도커에서 `훅이 없다` 로 2 다 — 레포 본 기본값과 도우미 넘기기를 되돌리면 이 측정이 1 로 돌아간다
- [ ] 스크립트-09: 맞대기 검사가 설치본 상태를 바르게 알린다 — 맞대기 검사를 ① `--installed <없는 폴더>` 로 돌리면 종료 코드 0 · 출력이 정확히 `설치본 없음 — 건너뜀` 한 줄 ② 옮긴 세 파일의 사본 폴더로 돌리면 0 · `다름:` 으로 시작하는 줄 없음 ③ 그 사본에서 `qa-pending-check.sh` 끝에서 둘째 바이트만 바꾼(크기 같음) 폴더로 돌리면 1 · `다름:` 줄의 이름이 정확히 `qa-pending-check.sh` 하나 ④ 기본값(`~/.claude/hooks`)으로 돌리면, 도우미가 세 파일을 직접 바이트로 맞댄 답(알려진 답 — 다른 이름 목록)과 `다름:` 줄 이름 목록이 같고, 종료 코드가 그 목록이 비면 0 · 아니면 1 이다. Given 공통 전제 G, When `m 스크립트-09`, Then `none_ok=1 same_ok=1 flip_ok=1 installed_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-09` (도우미 `m_checker` · `COPIED` · `INSTALLED`). 시작 판 `MISSING scripts/check-user-hook-copies.py …` · `ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `none_ok=1 same_ok=1 flip_ok=1 installed_ok=1` · 0 (그때 이 맥의 알려진 답은 빈 목록 · 검사 `rc=0`)
  알려진 답: ③ 은 손으로 바꾼 한 바이트라 답이 `[qa-pending-check.sh]` 다. ④ 는 도우미가 검사와 따로 `read_bytes()` 로 맞댄 목록이 답이다 — 봉인 전 사본에서 `known=[]` · 검사 `differ=[]` · `rc=0`
- [ ] 스크립트-10: 맞대기 시험이 대역 검사를 잡는다 — `python3 scripts/test-check-user-hook-copies.py` 끝 줄 `경우 6 개 중 통과 6` · 종료 코드 0 이고, `--tool` 로 `print("설치본 없음 — 건너뜀")` 한 줄짜리 대역(도우미 `CHECKER_STUB`)을 주면 `FAIL 경우 4,5,6` 만 내고 1 이다. Given 공통 전제 G, When `m 스크립트-10`, Then `tail=[경우 6 개 중 통과 6] ok=1 stub_fails=4,5,6 stub_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-10`. 시작 판 시험 파일 없음 · `ok=0 stub_ok=0` · 종료 코드 1. 구현 뒤 모양 사본 위 값 그대로 · 0
  음성 대조: 대역은 늘 건너뜀으로 0 을 내는 검사다 — 다름을 못 보는 판을 경우 4 · 6 이, 파일별 건너뜀 줄을 못 내는 판을 경우 5 가 잡는다
- [ ] 스크립트-11: CI 에 네 단계를 더하기만 한다 — `.github/workflows/ci.yml` 의 run 줄에 `bash harness/evals/hooks/lint-contract-oracle-test.sh` · `bash harness/evals/hooks/qa-pending-check-test.sh` · `python3 scripts/test-check-user-hook-copies.py` · `python3 scripts/check-user-hook-copies.py` 가 각각 정확히 1 개 있고, 새 넷을 뺀 run 줄 목록이 시작 판의 run 줄 52 개와 차례까지 같으며, 전체 run 줄이 정확히 56 개다. Given 공통 전제 G, When `m 스크립트-11`, Then `base_runs=52 runs=56 new_once=1 kept=1 added_only=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-11` (도우미 `NEW_RUNS`). 시작 판 `base_runs=52 runs=52 new_once=0 kept=1 added_only=0` · 종료 코드 1. 구현 뒤 모양 사본 위 값 그대로 · 0
  음성 대조: 구현 뒤 모양 사본에서 시작 판 run 줄 둘(`python3 scripts/validate-plugin.py` · `python3 scripts/sync-evals.py --check-only`)의 자리를 맞바꾼 `ci.yml` 은 개수가 같아도 `kept=0` · 종료 코드 1 (봉인 전 실측 — 교차 진단이 짚은 「개수만 보면 지우고 끼워도 통과」 를 막는다)

## Error

- [ ] 오류-01: 이미 되던 호출은 그대로다 — 앞 묶음 ev 도우미의 같은 측정 그대로: W 에서 `python3 scripts/run-evals.py --verbose` · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/run-evals.py tone-kit --verbose` · `python3 scripts/run-evals.py backend-kit` · `python3 scripts/run-evals.py infra-kit` 이 모두 종료 코드 0, 킷 셋 트리에서 이름으로 준 대상 없는 바로가기 킷 `b` 는 2 이고 출력에 `b` 가 있으며, `bash .harness/.meta/after-0928-harness-checks-r2/m-evals-absent.sh <W> fe6704d8` 과 `… <W> HEAD` 의 두 줄이 판 이름을 빼면 같다. Given 공통 전제 G, When `m 오류-01`, Then 여섯 줄 `OK` · `cases=6 right=6 ok=1 absent_same=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01` (ev 도우미 `m_keep` 을 그대로 부른다). 시작 판 `cases=6 right=6 ok=1 absent_same=1` · 0 (지킬 동작). 구현 뒤 모양 사본 같음 · 0
- [ ] 오류-02: 앞 묶음 cx 재현의 평가 줄이 그대로다 — `bash .harness/.meta/after-0929-codex-silent-pass/repro.sh <W> ~/.claude/hooks` 출력에서 `d2` · `d4` · `d6` 로 시작하는 줄이 차례대로 정확히 `d2 broken-json rc=2 msg=1` · `d2 good rc=0` · `d4 unreadable rc=2 msg=1` · `d4 good rc=0` · `d6 empty-list rc=2 msg=1` · `d6 no-key rc=2 msg=1` · `d6 good rc=0` 이다. Given 공통 전제 G, When `m 오류-02`, Then `lines=7 same=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02` (ev 도우미 `m_cx_keep`). 시작 판 `lines=7 same=1` · 0. 구현 뒤 모양 사본 같음 · 0 (「더하라」 조건 스크립트-01 ~ 06 과 「그대로」 조건 오류-01 · 02 가 함께 겨누는 `scripts/run-evals.py` · `scripts/sync-evals.py` 에서 부딪히지 않는다)

## Skill

- [ ] 스킬-00: N/A (이번 변경은 스킬 · 에이전트 파일을 건드리지 않는다 — 바뀌는 곳은 scripts/ · .github/ · harness/evals/hooks/ 뿐. 측정: git diff --name-only 7fe274fc..chore/ak3-fin -- '*SKILL.md' 'harness/agents' '.claude/skills' | grep -c . 이 0)

## Architecture

- [ ] 구조-01: 커밋 규칙 — `7fe274fc..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(`scripts` · `.github` · `harness` · `.harness` 는 서로 다른 폴더)이며, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이고, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-01`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-01` (tail `m_commits` 를 이 기준 판 · 계약으로). 시작 판 `commits=0 bad=0 scope_entries=12 git_rc=0` · 종료 코드 1 (범위 목록 열두 줄은 읽히지만 커밋이 0 개). 구현 뒤 모양 사본 `commits` 1 이상 · `bad=0` · 0
- [ ] 구조-02: 설명 글이 새 동작을 적는다 — 맨 앞 설명(파이썬은 첫 `"""` 덩어리, 셸은 첫 빈 줄 앞)에 `scripts/run-evals.py` 는 `객체` · `항목 없는 킷`, `scripts/sync-evals.py` 는 `객체`, `scripts/test-run-evals.py` 는 두 칸 들여 쓴 `17.` · `18.` · `19.` · `20.` 항목과 `객체가 아니다`, `scripts/test-sync-evals.py` 는 `14.` · `15.` 항목과 `객체가 아니다`, `scripts/check-user-hook-copies.py` 는 `설치본 없음 — 건너뜀`, `scripts/test-check-user-hook-copies.py` 는 `6.` 항목, 훅 시험 둘은 `레포 본` · `check-user-hook-copies.py` 를 담고, 훅 시험 둘 어디에도 `CI 에 등록하지 않는다` 가 없다. Given 공통 전제 G, When `m 구조-02`, Then `miss=[] stale=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02` (도우미 `m_usage` 의 `need`). 시작 판 `miss=[run-evals.py:객체,run-evals.py:항목 없는 킷,sync-evals.py:객체,test-run-evals.py:17.,test-run-evals.py:18.,test-run-evals.py:19.,test-run-evals.py:20.,test-run-evals.py:객체가 아니다,test-sync-evals.py:14.,test-sync-evals.py:15.,test-sync-evals.py:객체가 아니다,check-user-hook-copies.py:설치본 없음 — 건너뜀,test-check-user-hook-copies.py:6.,lint-contract-oracle-test.sh:레포 본,lint-contract-oracle-test.sh:check-user-hook-copies.py,qa-pending-check-test.sh:레포 본,qa-pending-check-test.sh:check-user-hook-copies.py] stale=[lint-contract-oracle-test.sh,qa-pending-check-test.sh] ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `miss=[] stale=[] ok=1` · 0
- [ ] 구조-03: 기록 — `.harness/.meta/after-kaizen-0928/fin-notes.md` 에 낱말 `객체가 아니다` · `항목 없는 킷` · `두 번째 읽기` · `lint-contract-oracle.sh` · `qa-pending-check.sh` · `_lib-hook-payload.sh` · `check-user-hook-copies` · `도커` · `판 번호`(harness 판 번호를 올릴지 판단과 까닭) · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 4 개 이상이 있다. Given 공통 전제 G, When `m 구조-03`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03`. 시작 판 파일 없음 · `keys_ok=0` · 종료 코드 1
- [ ] 구조-04: 훅은 시험 폴더에만 놓고 등록하지 않는다 — `git diff --name-status 7fe274fc..chore/ak3-fin -- harness` 가 정확히 다섯 줄 `A harness/evals/hooks/_lib-hook-payload.sh` · `A harness/evals/hooks/lint-contract-oracle.sh` · `M harness/evals/hooks/lint-contract-oracle-test.sh` · `A harness/evals/hooks/qa-pending-check.sh` · `M harness/evals/hooks/qa-pending-check-test.sh` 이고(새 폴더 · `harness/hooks/` 변경 0), `harness/hooks/hooks.json` 에 옮긴 세 파일 이름이 하나도 없다. Given 공통 전제 G, When `m 구조-04`, Then `files=5 same_set=1 registered=[] not_registered=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-04` (도우미 `WANT_HARNESS`). 시작 판 `files=0 same_set=0 registered=[] not_registered=1` · 종료 코드 1. 구현 뒤 모양 사본 위 값 그대로 · 0
- [ ] 구조-05: 옮긴 세 파일은 설치본 바이트 그대로 들어왔다 — 옮긴 세 파일마다 `7fe274fc..chore/ak3-fin` 에서 그 파일을 더한 커밋이 정확히 1 개이고, 그 커밋의 내용 지문(`sha256` 앞 16 자리)이 `lint-contract-oracle.sh` `182ed51390abd4ae` · `qa-pending-check.sh` `07c427c14a16523e` · `_lib-hook-payload.sh` `dff1e68e020a5028` 이다. 가지 끝 내용 지문이 그 값과 다르면(리눅스 수정) 기록 `.harness/.meta/after-kaizen-0928/fin-notes.md` 에 그 파일 이름과 `설치본에 옮길 줄` 이 있다. Given 공통 전제 G, When `m 구조-05`, Then 세 줄 `adds=1 first=<기대 지문> …` · `files=3 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-05` (도우미 `COPIED`). 시작 판 세 줄 `adds=0 first=None tip=None` · `files=3 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 세 줄 모두 `adds=1 first=tip=want` · `ok=1` · 0
  알려진 답: 기대 지문 셋은 봉인 전 `cd ~/.claude/hooks && shasum -a 256 lint-contract-oracle.sh qa-pending-check.sh _lib-hook-payload.sh` 의 앞 16 자리를 옮긴 것이다(도우미 `COPIED` 와 같다)

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-fin` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 새 기록 `.harness/.meta/after-kaizen-0928/fin-notes.md` 에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 검사 · 새 시험은 `scripts/` 에 두고 CI 에 등록돼 누구나 부른다 — 스크립트-11 `new_once=1`. 옮긴 세 파일은 레포에서 누구나 읽는 시험 폴더에 있다)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — `scripts/` · `.github/` 에 새로 생긴 파일은 정확히 `scripts/check-user-hook-copies.py` · `scripts/test-check-user-hook-copies.py` 둘이다(`~/.claude/hooks/` 를 맞대는 기존 검사가 없다 — `scripts/check-installed-sync.py` 는 플러그인 설치본만 본다). 평가 시험은 기존 두 파일에 경우를 더하고, 못 읽음 줄 모양은 이미 쓰는 `UNREADABLE <경로> (<까닭>)` · `못 읽은 킷 N 개: …` 를 따른다. Given 공통 전제 G, When `m 재사용-02`, Then `added=2 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 재사용-02`. 시작 판 `added=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `added=2 ok=1` · 0

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only 7fe274fc..chore/ak3-fin | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀌거나 새로 생긴 `.py` 여섯(`scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/test-run-evals.py` · `scripts/test-sync-evals.py` · `scripts/check-user-hook-copies.py` · `scripts/test-check-user-hook-copies.py`)은 `python3 -m py_compile` 종료 코드 0, `.sh` 다섯(옮긴 세 파일 · 훅 시험 둘)은 `bash -n` 종료 코드 0 이고 `shellcheck -f gcc <파일> | grep -c .` 이 0, 새 `.md` 하나(`.harness/.meta/after-kaizen-0928/fin-notes.md`)는 markdownlint-cli2(MD013 끔) 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`
  측정: md 는 `<scratch>/fin/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/fin/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(markdownlint-cli2 0.23.3, 설정 파일 내용 `{ "config": { "MD013": false } }`, `<scratch>` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`. 앞 묶음이 쓴 `<scratch>/mdl` 설치본은 봉인 전 확인에서 모듈이 빠져 추적 출력으로 죽고 경고 0 을 냈다 — 양성 대조가 잡았다. 다시 설치한 `<scratch>/fin/mdl` 을 쓴다). 시작 판 `.py` 넷 `py_compile` 0, 훅 시험 둘 `shellcheck` 0 줄. 양성 대조: 같은 md 명령으로 잰 `<scratch>/ev/pos.md`(여는 fence 언어 없음 · 제목 건너뜀) → 경고 1 이상, `printf 'x=$1\necho $x\n' | shellcheck -s bash -f gcc - | grep -c .` → 1 이상
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 실행기 스크립트 · 검사 · 시험 · 훅 사본 · CI 파일 · 기록. 측정: git diff --name-only 7fe274fc..chore/ak3-fin -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/|harness/evals/hooks/)' 이 0)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash scripts/ci-local.sh <W>` (W 맨 위 폴더에서, TMPDIR 은 scratch 아래 새 폴더. 레포 밖 옛 도구 `.harness/handoff/2026-09-26-tools/ci-local.sh` 는 지금 없다 — 봉인 전 확인)의 끝 줄이 정확히 `steps=56 run=51 skip=5 unsupported=0 failed=0` 이고 `FAIL` 로 시작하는 줄이 0 · 종료 코드 0 이고, `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `python3 scripts/test-run-evals.py` · `python3 scripts/test-sync-evals.py` · `python3 scripts/test-check-user-hook-copies.py` · `bash harness/evals/hooks/lint-contract-oracle-test.sh` · `bash harness/evals/hooks/qa-pending-check-test.sh` 를 따로 돌린 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 ci-local 끝 줄 · `grep -c '^FAIL'`. 봉인 전 시작 판 · 구현 뒤 모양 사본 값은 `## 회귀 게이트` 에 적는다

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
scripts/run-evals.py
scripts/sync-evals.py
scripts/test-run-evals.py
scripts/test-sync-evals.py
scripts/check-user-hook-copies.py
scripts/test-check-user-hook-copies.py
.github/workflows/ci.yml
harness/evals/hooks/lint-contract-oracle.sh
harness/evals/hooks/qa-pending-check.sh
harness/evals/hooks/_lib-hook-payload.sh
harness/evals/hooks/lint-contract-oracle-test.sh
harness/evals/hooks/qa-pending-check-test.sh
```

- 하지 않는 것: `~/.claude/hooks/` 의 파일 고치기(읽기만 — 리눅스 수정이 생기면 기록에 옮길 줄만 적는다), `harness/hooks/` · `harness/hooks/hooks.json` 에 훅 등록, 새 폴더 만들기, `sync-evals.py` 의 두 읽기를 하나로 합치기, 평가 항목 하나하나가 객체가 아닌 경우(`{"evals":[5]}` 같은 안쪽 모양 — 최상위 모양만 이번 범위), `SKIP_KITS` 에 적힌 킷의 판정, `.claude/skills/backend-kaizen/SKILL.md` · `backend-kit/README.md` · `infra-kit/README.md` 의 글(새 2 까닭이 「못 읽거나 깨지면 2」 · 「2 = 파싱 오류」 와 부딪히지 않는다 — 고치지 않는다), `harness/evals/gate-exit-codes.md` 표(새 종료 코드 값이 없다), harness 판 번호 올리기 · 릴리스 · 합치기 · push, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일.
- 문서 사이트 대응 페이지: 바뀌는 원본 문서가 없다(스크립트 · 시험 · CI · 훅 사본뿐). `grep -rln 'run-evals\|sync-evals\|qa-pending-check\|lint-contract-oracle' docs --include='*.html'` 은 `docs/howto-kit/overview.html` 하나뿐이고 그 줄(740)은 다른 도구 `howto-kit/evals/run-evals.sh` 를 적은 것이다(봉인 전 확인) — 맞출 페이지가 없다.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약들은 `status: done` 이고 이 계약의 조건을 느슨하게 하지 않는다): ev 계약 `스크립트-04` 측정이 적은 시험 끝 줄 `경우 9 개 중 통과 9` · `경우 6 개 중 통과 6` 과 CI 이름 「아홉 경우」 · 「여섯 경우」 는 `20` · `15` · 「스무 경우」 · 「열다섯 경우」 로 바뀌고, 그 측정의 옛 판 · 변이 실패 번호도 경우가 늘어 달라진다. end 계약 도우미의 CI 이름 낱말(`없는 킷` · `못 읽`)은 새 이름에 남긴다(스크립트-06 `ci_ok`). 두 쪽 모두 경우를 더하는 쪽이라 더 엄격하다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` · `.github/` · `harness/` 는 따로. 옮긴 세 파일은 설치본에서 바이트 그대로 복사해 커밋한다(구조-05). 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0930-final/`) · 기록 커밋은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0930-final/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 평가 실행기 임시 트리 · 킷 칸 나누기 · 이미 되던 호출(오류-01 · 02)은 ev 도우미 `.harness/.meta/after-0930-eval-runners/measure.py` 를, CI 단계 읽기 · 커밋 규칙은 tail 도우미 `.harness/.meta/after-0929-tail/measure.py` 를 불러 쓴다. `m 스크립트-01-base` 는 스크립트-01 의 음성 대조 전용 명령이다.
- `TMPDIR` 는 절대 경로로 준다(상대 경로면 시험 임시 폴더가 작업 폴더 기준으로 풀린다 — end 계약 실측).
- 봉인 전 실측(2026-10-01, W 시작 판 `7fe274fc`): 스크립트-01 ~ 11 · 구조-01 ~ 05 · 재사용-02 종료 코드 1 (결함 재현 · 산출물 없음), 오류-01 · 오류-02 · `스크립트-01-base` 종료 코드 0 (지킬 동작 · 음성 대조). 값은 각 조건 측정 줄에 있다.
- 진단-05 봉인 전 실측 — 시작 판(W, `npm ci` 뒤): `bash scripts/ci-local.sh <W>` 끝 줄 `steps=52 run=47 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 종료 코드 0, 따로 돌린 열둘 가운데 시작 판에 있는 열하나(`12/12 PASS` · `어긋남 0` · `checked=2 violations=0 infra_errors=0` · `실패 0 건` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `174 passed` · `경우 9 개 중 통과 9` · `경우 6 개 중 통과 6` · 훅 시험 둘 `실패 0 건`(설치본 기본값)) 모두 0, 맞대기 시험은 파일이 없어 2. 레포 밖 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 없어(`No such file or directory`) 레포 안 `scripts/ci-local.sh`(CI 파일을 그때그때 읽는 판)를 쓴다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 `<scratch>/fin/impl` — W 를 `git clone --shared` 한 뒤 옮긴 세 파일 · 훅 시험 둘 / 실행기 둘 · 시험 둘 · 맞대기 검사 · 그 시험 / CI 네 단계 · 이름 둘을 폴더별 서명 커밋 셋에 담고, 이 계약 · 이 도우미 · 기록 사본 커밋 셋, 2026-10-01): 이 계약 측정 스물(스크립트-01 ~ 11 · `스크립트-01-base` · 오류-01 · 02 · 구조-01 ~ 05 · 재사용-02) 모두 종료 코드 0 (구조-01 `commits=6 bad=0 scope_entries=12`, 스크립트-08 도커 `results=3 mawk=1 gnu_grep=1 ok=1`, 스크립트-09 이 맥의 알려진 답 `known=[]` · 검사 `rc=0`). 같은 사본에서 `ci-local.sh` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 종료 코드 0 (새 네 단계 모두 `PASS`, 맞대기 검사는 이 맥 설치본과 같아 `설치본 3 개가 레포 본과 같다`), 따로 돌린 열둘 모두 0 (바뀐 끝 줄은 `경우 20 개 중 통과 20` · `경우 15 개 중 통과 15` · `경우 6 개 중 통과 6` 셋), `.py` 여섯 `py_compile` 0, `.sh` 다섯 `bash -n` 0 · `shellcheck` 0 줄, 기록 사본 markdownlint `0 issues` · `Linting: 1 file`, `validate-plugin.py --check=code-fence` 0. 양성 대조 `<scratch>/ev/pos.md` 경고 2 (MD041 · MD040), `x=$1` 셸 조각 `shellcheck` 1 줄.
- 앞 묶음 도우미를 같은 사본에서 돌린 값: ev `오류-01` · `오류-02` 0 (그대로), end `스크립트-05` `run_ok=1 sync_ok=1` 0 (그대로). ev `스크립트-04` · end `스크립트-06` 은 끝 줄이 `경우 20 · 15` 로 늘고 옛 판 실패 번호가 늘어 1 — 경우를 더해 일부러 바꾸는 값이다(범위 경계).
- 교차 대조(봉인 전): 바뀌는 글자 · 파일(`run-evals` · `sync-evals` · `test-run-evals` · `test-sync-evals` · `아홉 경우` · `여섯 경우` · `lint-contract-oracle` · `qa-pending-check` · `_lib-hook-payload` · `evals/hooks` · `CI 에 등록하지 않는다`)을 `scripts/` · `.github/` · `harness/` · `package.json` · `.claude/` 에서 `git grep` 으로 찾았다 — 검사로 읽는 곳은 `.github/workflows/ci.yml` 과 바뀌는 파일 자신뿐이다. 나머지는 이름만 적은 글이다: `package.json` 의 npm 단축 `sync-evals`(`--check-only` 로 부를 뿐 — 레포에서 0 그대로, 오류-01), `.claude/skills/*-kaizen/SKILL.md` · `.claude/kaizen-input/*.md`(도구 이름 · 부르는 법), `harness/README.md` 66 · 73 줄과 `harness/references/contract-schema.md` 819 줄(범위 목록 예시 `harness/evals/hooks/`), `harness/evals/amend-direction/measured-*.txt`(다른 도구 `howto-kit/evals/run-evals.sh`), `scripts/test-check-docs-mermaid.js`(「아홉 경우」 는 자기 시험 설명). 커밋 직전 훅의 범위 목록 검사는 이 계약의 `# sprint-scope` 열두 줄로 이번 커밋을 모두 통과시킨다(사본 대조 구조-01 `bad=0`). `scripts/validate-plugin.py` 의 `$`+숫자 검사(V9)는 SKILL.md 만 읽고, 훅 실행 비트 검사(V8)는 `hooks.json` 이 부르는 파일만 읽어 옮긴 세 파일(awk 의 `$0` · `$2` 를 담음)을 재지 않는다. 앞 묶음 측정 도우미 가운데 `after-0928-harness-checks-r2/m-evals-absent.sh`(오류-01 이 그대로 잰다) · `after-0929-codex-silent-pass/repro.sh`(오류-02) · `after-0930-end/measure.py` · `after-0930-eval-runners/measure.py`(경우 수가 늘어 일부러 바꾸는 값 — 위 범위 경계) 가 이 파일들을 읽는다. 「더하라」 조건(스크립트-01 ~ 11 · 구조-02 ~ 05 · 재사용-02)과 「그대로」 조건(오류-01 · 02 · 진단-05)이 함께 겨누는 파일은 `scripts/run-evals.py` · `scripts/sync-evals.py` · `.github/workflows/ci.yml` 이다.
- 도우미 지문(봉인 전, `shasum -a 256 <파일> | cut -c1-16`): 이 계약 `measure.py` `f066b5cdac40442c` · ev `measure.py` `e1d81f6a7352fe42` · tail `measure.py` `3d920fd41c46e7f6`.
- 오라클 해소: 오류-01 — 판정은 글자 찾기가 아니라 다섯 명령 · 이름 준 바로가기 호출 · `m-evals-absent.sh` 두 판을 실제로 돌린 종료 코드와 출력이다.
- 오라클 해소: 스크립트-08 — 판정은 도커 안에서 시험 셋을 실제로 돌린 종료 코드와 끝 줄이다. 백틱 안 한글(`실패 0 건` 등)은 기대하는 끝 줄 값이지 grep 할 문장이 아니다.
- 오라클 해소: 진단-02 · 진단-05 — 파일 · 명령 목록을 백틱으로 적었을 뿐, 판정은 `py_compile` · `bash -n` · `shellcheck` · markdownlint · 각 명령을 실행한 종료 코드와 끝 줄이다. 진단-02 는 양성 대조가 있다.
- 커버리지 해소: 스크립트-01 ~ 05 — 트리 모양 · 세 도구 명령 · 「쟀다」 글 · 요약 줄 모양 · 내용 다섯 · 정상 모양 셋 · 변이 줄 · 두 번째 읽기 대역은 도우미 `NON_OBJECT` · `NORMAL` · `NULL_EVALS` · `EMPTY_SETS` · `SECOND_READ` · `TOOLS` · `summary_lines` 에 글자 그대로 있고 `m` 이 경우마다 한 줄을 찍는다.
- 커버리지 해소: 스크립트-06 · 10 — 시작 판 도구 세 파일은 `tool_dir_of`, 변이 · 대역은 `NULL_EVALS` · `CHECKER_STUB`, CI 단계 두 줄은 `m_eval_tests` 에 글자 그대로 있다.
- 커버리지 해소: 스크립트-07 · 08 · 09 · 11 — 훅 시험 · 환경 변수 · 대역 훅 · 도커 명령 · 맞대기 경우 · 새 run 줄 넷은 도우미 `HOOK_TESTS` · `HOOK_ENV` · `HOOK_STUB` · `DOCKER_SCRIPT` · `m_checker` · `NEW_RUNS` 에 글자 그대로 있다.
- 커버리지 해소: 구조-02 ~ 05 · 재사용-02 — 파일 경로 · 찾을 낱말 · 기대 다섯 줄 · 지문 셋은 도우미 `m_usage` 의 `need` · `m_notes` 의 `keys` · `WANT_HARNESS` · `COPIED` · `m_new_files` 에 글자 그대로 있다.
- 커버리지 해소: 오류-01 · 오류-02 — 다섯 명령 · 비교 판 · 일곱 줄은 ev 도우미 `m_keep` · `ABSENT` · `CX_KEEP` 에 글자 그대로 있다.
- 커버리지 검출기(6.5 (4)) 출력 여덟 건(스크립트-01 · 04 · 09, 구조-02 · 03 · 04 · 05, 재사용-02)은 모두 위 해소 줄로 처리했다 — 경로 · 파일 이름 · 커밋 구간은 도우미가 상수(`COPIED` · `HOOK_DIR` · `NOTES` · `BASE` · `BRANCH` · `CHECKER` · `need` · `WANT_HARNESS`)로 들고 조건 줄의 `m <조건 번호>` 가 부른다. 재사용-02 의 `scripts/check-installed-sync.py` · `~/.claude/hooks/` 는 재는 대상이 아니라 「기존 검사가 없다」 는 까닭을 적은 것이다(봉인 전 `git grep -l ".claude/hooks" -- scripts` 결과 0 건).
