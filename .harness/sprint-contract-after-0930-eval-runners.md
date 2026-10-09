---
feature: "평가 실행기 둘 — 대상 없는 바로가기 · 못 읽는 킷 하나"
slug: after-0930-eval-runners
created: "2026-09-30 18:05"
complexity: "복잡"
conditions: 20
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:680e37872c5063e7
measurement_digest: sha256:6757b915845ee19d
locked_at: "2026-09-30 18:31"
---

## 배경

- 묶음 ev. 출처는 `.harness/.meta/after-kaizen-0928/end-notes.md` 「남긴 것」 첫 항목과 PR #123 설명 「알려진 남은 것」 첫 항목이다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev`, 가지 `chore/ak3-ev`, 시작 판 `BASE` = `fe6704d8` (`origin/main`, PR #126 합침). 통합 가지 없이 main 에서 새로 팠다.
- 사용자가 할 일: 없음.
- 킷 폴더 밖(`scripts/` · `.github/` · `.claude/`)만 바뀌므로 킷 릴리스는 없다.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-ev` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 다시 돌린 뒤 W 맨 위 폴더에서 root 가 아닌 사용자로 잰다(권한을 빼 못 읽는 파일을 만들어야 한다). 이 가지는 이 스프린트만 커밋한다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. `TMPDIR` 는 scratch 아래 절대 경로 폴더로 둔다.

용어 (조건마다 되풀이하지 않는다):

- 「세 도구」 = `python3 scripts/run-evals.py`(인자 없음) · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/sync-evals.py`(옵션 없음). 도우미 이름 `run` · `sync-check` · `sync-plain`.
- 「킷 셋 트리」 = 임시 폴더에 W 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py` 사본과 킷 `a` · `b` · `c` 를 적은 마켓 목록, 킷마다 스킬 `s` 와 그 스킬 항목 하나짜리 `evals/evals.json` 을 둔 트리(도우미 `tree`). 못 읽는 칸이 있는 경우에는 읽히는 킷마다 평가에 없는 스킬 `extra` 를 더 둔다 — 그 킷을 쟀다는 줄이 나오게 하려는 것이다.
- 「쟀다」 = 그 킷 칸(`→ <킷>` 줄부터 다음 `→` 줄 앞까지)에 `run` 은 `PASS: 1 passed, 0 failed`, `sync-check` 는 `[<킷>] MISSING: extra`, `sync-plain` 은 `[<킷>] added 1 skeleton entries` 가 있다(도우미 `MEASURED`).
- 「요약 줄」 = 정확히 `못 읽은 킷 <수> 개: <킷 이름을 마켓 목록 차례로 ", " 로 이은 것>` 인 줄 하나가 마지막 `→` 줄보다 뒤에 있다(도우미 `summary_after`). 출력은 표준 출력과 표준 오류를 한 흐름으로 모아 `PYTHONUNBUFFERED=1` 로 받는다.

항목별 처리 방침 (결정):

- **(1) 대상 없는 바로가기** — 두 실행기는 대상 킷을 `(… / "evals.json").is_file()` 로 고르고, `sync-evals.py` 는 읽기 전에 `path.exists()` 를 본다. 둘 다 바로가기(심볼릭 링크)를 따라가므로 가리키는 파일이 없는 바로가기는 「평가 파일 없는 킷 — 대상 아님」 으로 빠지고 종료 코드 0 이다(봉인 전 재현 — 아래 GAP). `scripts/check-install-docs-guidance.py` 102 줄이 쓰는 `os.path.lexists` 로 가른다 — 파일 자리가 있으면(바로가기 포함) 대상으로 잡고, 못 읽으면 `UNREADABLE <경로> (<까닭>)` 줄을 낸다. 자리가 아예 없는 킷은 지금처럼 「대상 아님」 목록에 적고 넘긴다.
- **(2) 못 읽는 킷 하나에서 멈춤** — 두 실행기의 `load_evals` 는 `OSError`(권한)와 `JSONDecodeError`(깨진 글) 모두 `sys.exit(2)` 로 바로 끝나 뒤 킷을 재지 않는다. 못 읽은 킷 이름을 모아 두고 나머지 킷을 끝까지 잰 뒤, 끝에 요약 줄을 찍고 2 로 끝낸다. 깨진 글도 같은 길로 보낸다 — 「못 읽음」 과 「깨짐」 이 다르게 멈추면 한 칸만 나빠도 나머지를 못 재는 구멍이 그대로 남는다. 종료 코드 값은 그대로(0 · 1 · 2)이고, 못 읽은 킷이 있으면 FAIL · 차이가 함께 있어도 2 다.
- **(3) 받아 쓰는 쪽** — `.claude/skills/backend-kaizen/SKILL.md` 40 줄(10 번 항목)이 「`JSONDecodeError` 시 `sys.exit(2)` 로 즉시 종료하는 구조 유지」 를 규칙으로 적고 있어 (2) 와 부딪힌다. 「나머지 킷을 끝까지 재고 끝에 2」 로 고친다(스킬-01). 킷 이름을 주고 실행기를 부르는 소비처 셋과 CI 의 인자 없는 호출은 그대로 0 이어야 한다(오류-01).
- **(4) 시험** — `scripts/test-sync-evals.py` 에 경우 4 · 5 · 6, `scripts/test-run-evals.py` 에 경우 7 · 8 · 9 를 더한다: 대상 없는 바로가기(걸려야 함) · 진짜 없는 평가 파일(넘겨야 함) · 킷 셋 중 가운데 하나만 못 읽음(나머지 둘은 재고 끝에 2). 넘겨야 하는 경우(5 · 8)는 시작 판도 통과하므로, 그 경우의 음성 대조는 「바로가기 판정을 늘 참으로 바꾼 지나친 판」 이다(도우미 `LEXISTS_TRUE`). CI 는 두 시험을 이미 돌리므로 단계 이름에 경우 수만 적는다.

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 읽은 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `scripts/run-evals.py` | 39 ~ 46 줄 `eval_kits` · 56 ~ 77 줄 `load_evals` · 140 ~ 154 줄 `validate_kit` · 180 ~ 206 줄 `main` · 18 ~ 22 줄(설명) | 대상 고르기가 `is_file()` · 못 읽음 · 깨짐이 `sys.exit(2)` | 스크립트-01 ~ 03 · 구조-02 |
| `scripts/sync-evals.py` | 38 ~ 46 줄 `target_kits` · 49 ~ 62 줄 `load_evals` · 180 ~ 205 줄 `main` · 17 ~ 21 줄(설명) | 같음 + `path.exists()`. 킷마다 두 번 읽는다(`main` · `process_kit`) | 스크립트-01 ~ 03 · 구조-02 |
| `scripts/check-install-docs-guidance.py` | 97 ~ 111 줄 | `os.path.lexists` 로 바로가기를 가르는 선례 — 고치지 않는다 | 방침 (1) 의 기준 |
| `scripts/test-sync-evals.py` · `scripts/test-run-evals.py` | 전체 | 경우 3 · 6, 바로가기 · 없는 파일 · 여러 킷 경우 없음 | 스크립트-04 · 구조-02 |
| `.github/workflows/ci.yml` | 37 ~ 39 · 53 ~ 55 줄 | 단계 이름에 경우 수 없음 | 스크립트-04 |
| `.claude/skills/backend-kaizen/SKILL.md` | 40 줄 | 「즉시 종료하는 구조 유지」 | 스킬-01 · 금지-04 |
| 소비처 `.claude/skills/tone-kaizen/SKILL.md` · `backend-kit/README.md` · `infra-kit/README.md` | 94 ~ 95 줄 · 56 줄 · 56 줄 | 킷 이름을 주고 부름(셋 다 평가 파일 있음) | 오류-01 |
| 앞 묶음 측정 `.harness/.meta/after-0928-harness-checks-r2/m-evals-absent.sh` · `.harness/.meta/after-0929-codex-silent-pass/repro.sh` | 전체 | 「대상 아님」 줄 · 못 읽음 · 깨짐 종료 코드를 잰다 | 오류-01 · 오류-02 |

봉인 전 실측 (W 시작 판 `fe6704d8`, 2026-09-30):

- (1) 가운데 킷 `b` 의 평가 파일이 대상 없는 바로가기인 킷 셋 트리: `run` 종료 코드 0 · `sync-check` 1(`a` · `c` 의 `extra` 차이만) · `sync-plain` 0, 셋 다 `UNREADABLE` 줄 없음 · 요약 줄 없음 — `b` 는 「대상 아님」 으로 빠진다.
- (2) `b` 권한 0 · `b` 깨진 글: 세 도구 모두 2 이지만 `c` 를 재지 않고 요약 줄이 없다. `a` · `c` 권한 0: 셋 다 `a` 에서 멈춰 `b` 를 재지 않는다.
- (3) 레포에서 `run-evals.py --verbose` → `Total: 122 passed, 0 failed` · 0, `sync-evals.py --check-only` → `Total: 0 added, 0 orphans, 0 missing (preview)` · 0, 킷 이름 `tone-kit` · `backend-kit` · `infra-kit` → `4` · `8` · `6 passed` · 0, `m-evals-absent.sh` → 두 줄 모두 `rc=0 absent=[planning-kit, reflect-kit, bambu-kit, onboarding-kit]`.

## Script

- [ ] 스크립트-01: 대상 없는 바로가기를 못 읽음으로 잡는다 — 킷 셋 트리에서 `b/evals/evals.json` 을 없는 `missing.json` 을 가리키는 바로가기로 두면 세 도구가 각각 종료 코드 2 이고, `UNREADABLE` 로 시작하며 `b/evals/evals.json` 을 담은 줄을 내고, `a` · `c` 를 쟀고, 요약 줄 `못 읽은 킷 1 개: b` 가 있다. Given 공통 전제 G, When `m 스크립트-01`, Then 세 줄 `OK b-dangling <run|sync-check|sync-plain>` · `cases=3 right=3 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` (도우미 `tree` · `TOOLS` · `case_bad`). 시작 판 `BAD b-dangling run rc=0 line=0 measured=1 summary=0` · `BAD … sync-check rc=1 …` · `BAD … sync-plain rc=0 …` · `cases=3 right=0 ok=0` · 종료 코드 1 (결함 재현). 구현 뒤 모양 사본 `right=3` · 0
  음성 대조: `m 스크립트-03-base` 가 시작 판 도구 셋으로 같은 모양을 돌려 세 줄 모두 `BAD` 를 낸다(`base_all_wrong=1`)
- [ ] 스크립트-02: 진짜 없는 평가 파일은 지금처럼 넘긴다 — 킷 셋 트리에서 `b/evals` 폴더가 아예 없으면 세 도구가 각각 종료 코드 0 이고, `평가 파일(evals/evals.json) 없는 킷 1 개 — 대상 아님: b` 로 시작하는 줄이 있으며 `UNREADABLE` 글자가 없다. 세 킷 모두 정상이면 세 도구가 0 이고 `대상 아님` 글자가 없다. 두 실행기가 바로가기 판정에 `os.path.lexists` 를 쓴다 — 그 판정을 늘 참으로 바꾼 변이(두 파일 맨 앞에 `import os` · `os.path.lexists = lambda _p: True` 를 붙인 사본)는 `b` 가 없는 트리에서 세 도구 모두 0 이 아니다. Given 공통 전제 G, When `m 스크립트-02`, Then 여섯 줄 `OK` · `cases=6 right=6 ok=1 … mut_right=0 mut_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02` (도우미 `absent_cases` · `mutant_dir` · `LEXISTS_TRUE`). 시작 판 `right=6 ok=1` · `mut_right=3 mut_ok=0` · 종료 코드 1 (변이가 걸릴 자리가 없다). 구현 뒤 모양 사본 `right=6` · `mut_right=0 mut_ok=1` · 0
  음성 대조: 변이는 진짜 없는 킷을 못 읽음으로 치는 지나친 판이다 — 이 조건의 여섯 경우 가운데 `b-absent` 셋이 그 판을 잡는다(`mut_ok`)
- [ ] 스크립트-03: 한 칸을 못 읽어도 나머지를 재고 끝에 2 — 킷 셋 트리의 세 모양 ① `b-unreadable`(`b/evals/evals.json` 권한 0) ② `b-broken`(`b/evals/evals.json` 이 `{ broken`) ③ `ac-unreadable`(`a` · `c` 권한 0) 에서 세 도구가 각각 종료 코드 2 이고, 못 읽은 킷마다 그 경로를 담은 줄(권한 0 은 `UNREADABLE` 로 시작)이 있고, 읽히는 킷을 모두 쟀고, 요약 줄이 ① ② `못 읽은 킷 1 개: b` ③ `못 읽은 킷 2 개: a, c` 이다. Given 공통 전제 G, When `m 스크립트-03`, Then 아홉 줄 `OK` · `cases=9 right=9 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03` (도우미 `BAD_SETS` · `case_bad` · `summary_after`, root 로 돌면 2). 시작 판 아홉 줄 모두 `BAD` (`rc=2 … measured=0 summary=0`) · `cases=9 right=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=9` · 0
  음성 대조: `m 스크립트-03-base` — 시작 판 도구 셋(`git show fe6704d8:` 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py`)으로 스크립트-01 · 03 의 네 모양 × 세 도구를 돌리면 열두 줄 모두 `BAD` · `cases=12 base_right=0 base_all_wrong=1` · 종료 코드 0 (봉인 전 실측 그대로)
- [ ] 스크립트-04: 시험 두 파일이 새 경우를 갖고 옛 판 · 지나친 판을 가른다 — `python3 scripts/test-sync-evals.py` 끝 줄 `경우 6 개 중 통과 6` · `python3 scripts/test-run-evals.py` 끝 줄 `경우 9 개 중 통과 9` · 둘 다 종료 코드 0 이다. `--tool` 로 시작 판 도구(`git show fe6704d8:` 의 세 파일을 한 임시 폴더에)를 주면 sync 시험은 `FAIL 경우 4` · `6` 만, run 시험은 `FAIL 경우 7` · `9` 만 내고 둘 다 1 이다. `--tool` 로 스크립트-02 의 변이 사본을 주면 sync 시험은 `FAIL 경우 5` 만, run 시험은 `FAIL 경우 8` 만 내고 둘 다 1 이다. `.github/workflows/ci.yml` 에서 `run: python3 scripts/test-sync-evals.py` · `run: python3 scripts/test-run-evals.py` 단계가 각각 정확히 1 개이고, 이름에 각각 `여섯 경우` · `아홉 경우` 가 있다. Given 공통 전제 G, When `m 스크립트-04`, Then `run_ok=1 sync_ok=1 run_base_fails=7,9 run_base_ok=1 sync_base_fails=4,6 sync_base_ok=1 run_mut_fails=8 run_mut_ok=1 sync_mut_fails=5 sync_mut_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04` (도우미 `m_tests` · `base_dir` · `mutant_dir`). 시작 판 `run_tail=[경우 6 개 중 통과 6] run_ok=0 sync_tail=[경우 3 개 중 통과 3] sync_ok=0 run_base_fails= … ci_ok=0` · 종료 코드 1. 구현 뒤 모양 사본 모든 `_ok` 값 1 · 0
  음성 대조: 시작 판 도구는 걸려야 할 경우(바로가기 · 가운데 못 읽음)에서만, 지나친 판은 넘겨야 할 경우(없는 평가 파일)에서만 실패한다 — 시험이 두 방향 결함을 따로 가른다

## Error

- [ ] 오류-01: 이미 되던 호출은 그대로다 — W 에서 `python3 scripts/run-evals.py --verbose` · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/run-evals.py tone-kit --verbose` · `python3 scripts/run-evals.py backend-kit` · `python3 scripts/run-evals.py infra-kit` 이 모두 종료 코드 0 이고, 킷 셋 트리에서 이름으로 준 킷 `b` 가 대상 없는 바로가기면 `python3 scripts/run-evals.py b` 가 2 이고 출력에 `b` 가 있으며, `bash .harness/.meta/after-0928-harness-checks-r2/m-evals-absent.sh <W> fe6704d8` 과 `… <W> HEAD` 의 두 줄이 판 이름을 빼면 같다(`run rc=0 absent=[planning-kit, reflect-kit, bambu-kit, onboarding-kit]` · `sync rc=0 absent=[…같음]`). Given 공통 전제 G, When `m 오류-01`, Then 여섯 줄 `OK` · `cases=6 right=6 ok=1 absent_same=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01` (도우미 `m_keep` · `ABSENT`). 시작 판 `right=6 ok=1 absent_same=1` · 0 (지킬 동작). 구현 뒤 모양 사본 같음 · 0. 킷 이름을 주고 부르는 소비처는 `git grep -n 'run-evals.py'` 로 찾은 셋뿐이다(나머지는 인자 없음 · 설명 글)
- [ ] 오류-02: 앞 묶음 cx 재현의 평가 줄이 그대로다 — `bash .harness/.meta/after-0929-codex-silent-pass/repro.sh <W> ~/.claude/hooks` 출력에서 `d2` · `d4` · `d6` 로 시작하는 줄이 차례대로 정확히 `d2 broken-json rc=2 msg=1` · `d2 good rc=0` · `d4 unreadable rc=2 msg=1` · `d4 good rc=0` · `d6 empty-list rc=2 msg=1` · `d6 no-key rc=2 msg=1` · `d6 good rc=0` 이다. Given 공통 전제 G, When `m 오류-02`, Then `lines=7 same=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02`. 시작 판 `lines=7 same=1` · 0. 구현 뒤 모양 사본 같음 · 0 (「더하라」 조건 스크립트-01 ~ 04 와 「그대로」 조건 오류-01 · 02 가 함께 겨누는 `scripts/run-evals.py` · `scripts/sync-evals.py` 에서 부딪히지 않는다)

## Skill

- [ ] 스킬-01: backend-kaizen 규칙이 새 동작을 적는다 — `.claude/skills/backend-kaizen/SKILL.md` 에 `` `sys.exit(2)` 로 즉시 종료하는 구조 유지 `` 글이 없고, `10. **run-evals.py` 로 시작하는 줄이 하나 있으며 그 줄에 `sync-evals.py` · `나머지` · `2` 가 있다. Given 공통 전제 G, When `m 스킬-01`, Then `line=1 old=0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-01` (도우미 `KAIZEN_OLD`). 시작 판 `line=1 old=1 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `line=1 old=0 ok=1` · 0

## Architecture

- [ ] 구조-01: 커밋 규칙 — `fe6704d8..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(`scripts` · `.github` · `.claude` · `.harness` 는 서로 다른 폴더)이며, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이고, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-01`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-01` (tail `m_commits` 를 이 기준 판 · 계약으로). 시작 판 `commits=0 bad=0 scope_entries=6 git_rc=0` · 종료 코드 1 (범위 목록 여섯 줄은 읽히지만 커밋이 0 개). 구현 뒤 모양 사본 `commits` 1 이상 · `bad=0` · 0
- [ ] 구조-02: 설명 글이 새 동작을 적는다 — `scripts/run-evals.py` · `scripts/sync-evals.py` 맨 앞 설명(첫 `"""` 덩어리)에 `바로가기` · `나머지` 가 있고, `scripts/test-run-evals.py` 맨 앞 설명에 두 칸 들여 쓴 `7.` · `8.` · `9.` 항목과 `바로가기`, `scripts/test-sync-evals.py` 맨 앞 설명에 `4.` · `5.` · `6.` 항목과 `바로가기` 가 있다. Given 공통 전제 G, When `m 구조-02`, Then `miss=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02` (도우미 `m_usage` 의 `need`). 시작 판 `miss=[run-evals.py:바로가기,run-evals.py:나머지,sync-evals.py:바로가기,sync-evals.py:나머지,test-run-evals.py:7.,test-run-evals.py:8.,test-run-evals.py:9.,test-run-evals.py:바로가기,test-sync-evals.py:4.,test-sync-evals.py:5.,test-sync-evals.py:6.,test-sync-evals.py:바로가기] ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `miss=[] ok=1` · 0
- [ ] 구조-03: 기록 — `.harness/.meta/after-kaizen-0928/ev-notes.md` 에 낱말 `lexists` · `run-evals` · `sync-evals` · `바로가기` · `못 읽은 킷` · `backend-kaizen` · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 3 개 이상이 있다. Given 공통 전제 G, When `m 구조-03`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03`. 시작 판 파일 없음 · `keys_ok=0` · 종료 코드 1

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-ev` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 새 기록 `.harness/.meta/after-kaizen-0928/ev-notes.md` 에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)
- [ ] 금지-04: 바꾸는 SKILL.md 의 머리말(name 필드 포함)을 건드리지 않는다 — `.claude/skills/backend-kaizen/SKILL.md` 의 첫 `---` 부터 다음 `---` 까지가 `fe6704d8` 판과 같다. `validate-plugin.py --check=frontmatter` 는 마켓 목록 킷만 읽어 이 파일을 재지 못하므로 직접 맞댄다 (측정: `m 금지-04` 이 `found=1 same=1` · 종료 코드 0. 시작 판 같음 · 0)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 코드는 두 실행기 안의 예외 처리 · 요약 몇 줄과 기존 시험 파일의 경우뿐이고, 시험은 CI 에 등록돼 누구나 부른다 — 스크립트-04 `ci_ok`)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 새 검사 · 새 시험 파일을 만들지 않고 기존 파일을 고친다 — `git diff --name-status fe6704d8..chore/ak3-ev -- scripts .github .claude` 에 `A` 줄 0. 바로가기 판정은 `check-install-docs-guidance.py` 와 같은 `os.path.lexists`, 못 읽음 줄 모양은 이미 쓰는 `UNREADABLE <경로> (<까닭>)` 을 따른다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only fe6704d8..chore/ak3-ev | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.py` 넷(`scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/test-run-evals.py` · `scripts/test-sync-evals.py`)은 `python3 -m py_compile` 종료 코드 0, 바뀐 `.md` 하나(`.claude/skills/backend-kaizen/SKILL.md`)와 새 `.md` 하나(`.harness/.meta/after-kaizen-0928/ev-notes.md`)는 markdownlint-cli2(MD013 끔) 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`
  측정: 파일마다 `<scratch>/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/rest/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(설정 파일 내용 `{ "config": { "MD013": false } }`, `<scratch>` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`). 시작 판 `.py` 넷 종료 코드 0, `backend-kaizen/SKILL.md` 경고 0. 양성 대조: 같은 명령으로 잰 `<scratch>/ev/pos.md`(여는 fence 언어 없음 · 제목 건너뜀) → 경고 1 이상
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 실행기 스크립트 · 시험 · CI 파일 · 스킬 글 한 줄 · 기록. 측정: git diff --name-only fe6704d8..HEAD -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/|\.claude/skills/backend-kaizen/)' 이 0)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash scripts/ci-local.sh <W>` (W 맨 위 폴더에서, TMPDIR 은 scratch 아래 새 폴더. 레포 밖 옛 도구 `.harness/handoff/2026-09-26-tools/ci-local.sh` 는 지금 없다 — 봉인 전 확인)의 끝 줄이 정확히 `steps=52 run=47 skip=5 unsupported=0 failed=0` 이고 `FAIL` 로 시작하는 줄이 0 · 종료 코드 0 (이 도구는 CI 파일의 run 단계를 모두 읽어 `npx playwright test` · 두 평가 시험 단계도 돈다), 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `python3 scripts/test-run-evals.py` · `python3 scripts/test-sync-evals.py` 를 따로 돌린 종료 코드가 모두 0 [exact, enumerated]
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
.claude/skills/backend-kaizen/SKILL.md
```

- 하지 않는 것: `scripts/check-install-docs-guidance.py` 고치기(선례일 뿐), 이름으로 준 킷의 평가 파일이 대상 없는 바로가기일 때의 문구(`evals/evals.json 없음`) 바꾸기(종료 코드가 이미 2 — 오류-01 이 지킨다), `run-evals.py` 의 eval 항목 0 개 즉시 2 바꾸기(못 읽음이 아니라 빈 목록이다 — 앞 묶음 cx 재현 `d6` 이 지킨다), `SKIP_KITS` 에 적힌 킷(`harness` · `howto-kit`)의 평가 파일 상태 판정(재지 않는 킷이다), `evals.json` 의 UTF-8 이 아닌 바이트 · `marketplace.json` 읽기 실패 처리(이미 추적 출력 · 종료 코드 1 로 CI 를 멈춘다 — 조용한 통과가 아니다), `backend-kit/README.md` · `infra-kit/README.md` 의 「2 = 파싱 오류」 글(그 킷 이름으로는 새 2 까닭이 생기지 않는다), `harness/evals/gate-exit-codes.md` 표(두 실행기는 표에 없고 새 종료 코드 값이 없다), 킷 버전 올리기 · 릴리스 · 합치기 · push, 레포 밖 파일, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일.
- 문서 사이트 대응 페이지: `.claude/skills/backend-kaizen/SKILL.md` 를 옮긴 `docs/` 페이지는 없다(`grep -rln '즉시 종료하는 구조' docs` 0 건, 봉인 전 확인) — 맞출 페이지가 없다.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약들은 `status: done` 이고 이 계약의 조건을 느슨하게 하지 않는다): end 계약 `스크립트-06` 측정이 적은 시험 끝 줄 `경우 6 개 중 통과 6` · `경우 3 개 중 통과 3` 은 `9` · `6` 으로 늘고, 그 계약 도우미의 CI 이름 낱말(`없는 킷` · `못 읽`)은 새 이름에 남긴다(아래 회귀 게이트 사본 대조). 경우를 더하는 쪽이라 더 엄격하다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` · `.github/` · `.claude/` 는 따로. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0930-eval-runners/`) · 기록 커밋은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0930-eval-runners/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). CI 단계 읽기 · 커밋 규칙은 tail 도우미 `.harness/.meta/after-0929-tail/measure.py` 를 불러 쓴다. `m 스크립트-03-base` 는 스크립트-01 · 03 의 음성 대조 전용 명령이다.
- `TMPDIR` 는 절대 경로로 준다(상대 경로면 시험 임시 폴더가 작업 폴더 기준으로 풀린다 — end 계약 실측).
- 봉인 전 실측(2026-09-30, W 시작 판 `fe6704d8`): 스크립트-01 ~ 04 · 스킬-01 · 구조-01 ~ 03 종료 코드 1 (결함 재현 · 산출물 없음), 오류-01 · 오류-02 · 금지-04 · `스크립트-03-base` 종료 코드 0 (지킬 동작 · 음성 대조). 값은 각 조건 측정 줄에 있다.
- 진단-05 봉인 전 실측 — 시작 판(W): `bash scripts/ci-local.sh <W>` 끝 줄 `steps=52 run=47 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 종료 코드 0 (그 안의 `Run Playwright tests` 단계 `rc=0`), 따로 돌린 여덟(`12/12 PASS` · `어긋남 0` · `checked=2 violations=0 infra_errors=0` · `실패 0 건` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `경우 6 개 중 통과 6` · `경우 3 개 중 통과 3`) 모두 종료 코드 0. 레포 밖 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 없어(`No such file or directory`) 레포 안 `scripts/ci-local.sh`(CI 파일을 그때그때 읽는 판)를 쓴다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 `git clone --shared` 에 실행기 둘 · 시험 둘 / CI 이름 둘 / backend-kaizen 줄 / 기록을 폴더별 서명 커밋에 담고, 계약 · 도우미 사본 커밋 둘, 2026-09-30): 이 계약 측정 열둘(스크립트-01 ~ 04 · `스크립트-03-base`, 오류-01 · 02, 스킬-01, 구조-01 ~ 03, 금지-04) 모두 종료 코드 0 (구조-01 `commits=6 bad=0`, 스크립트-02 `lexists_uses=4`). 같은 사본에서 `ci-local.sh` 끝 줄 `steps=52 run=47 skip=5 unsupported=0 failed=0` · 0, 따로 돌린 여덟 모두 0 (바뀐 끝 줄은 `경우 9 개 중 통과 9` · `경우 6 개 중 통과 6` 둘뿐), `npx playwright test` `174 passed` · 0, `.py` 넷 `py_compile` 0, `.md` 둘 markdownlint 경고 0 · `Linting: 1 file`, `validate-plugin.py --check=code-fence` 0, 재사용-02 `A` 줄 0, 진단-04 세기 0. 양성 대조 `<scratch>/ev/pos.md` 경고 2.
- 교차 대조(봉인 전): 바뀌는 글자 · 파일(`run-evals` · `sync-evals` · `test-run-evals` · `test-sync-evals` · `broken file test` · `empty list test` · `ER-01 회귀` · `backend-kaizen/SKILL` · `대상 아님`)을 읽는 기존 검사를 `scripts/` · `.github/` · `harness/` · `package.json` · `.claude/` 에서 `git grep` 으로 찾았다 — `.github/workflows/ci.yml` 과 `.claude/skills/backend-kaizen/SKILL.md` 자신뿐이다. 앞 묶음 측정 도우미 가운데 `after-0928-harness-checks-r2/m-evals-absent.sh`(오류-01 이 그대로 잰다) · `after-0929-codex-silent-pass/repro.sh`(오류-02) · `after-0930-end/measure.py`(사본에서 `스크립트-05` `run_ok=1 sync_ok=1` 그대로, `스크립트-06` 은 `경우 9 · 6` 과 옛 판 실패 번호가 늘어 1 — 경우를 늘려 일부러 바꾸는 것, `## 범위 경계`)가 이 파일들을 읽는다. end 도우미의 CI 이름 낱말(`없는 킷` · `못 읽`)은 사본 이름에 남아 그 값(`ci_ok=1`)은 그대로다. 「더하라」 조건(스크립트-01 ~ 04 · 스킬-01 · 구조-02)과 「그대로」 조건(오류-01 · 02 · 금지-04 · 진단-05)이 함께 겨누는 파일은 `scripts/run-evals.py` · `scripts/sync-evals.py` · `.claude/skills/backend-kaizen/SKILL.md` 이고, 위 사본에서 두 쪽이 모두 종료 코드 0 이라 부딪히지 않는다. CI 파일에만 있는 단계와 범위 목록을 맞대면 범위 밖 스크립트를 고쳐야 하는 경우는 없다.
- 도우미 지문(봉인 전, `shasum -a 256 <파일> | cut -c1-16`): 이 계약 `measure.py` `e1d81f6a7352fe42` · tail `measure.py` `3d920fd41c46e7f6`.
- 오라클 해소: 오류-01 — 판정은 글자 찾기가 아니라 다섯 명령 · 이름 준 바로가기 호출 · `m-evals-absent.sh` 두 판을 실제로 돌린 종료 코드와 출력이다.
- 오라클 해소: 진단-02 · 진단-05 — 파일 · 명령 목록을 백틱으로 적었을 뿐, 판정은 `py_compile` · markdownlint · 각 명령을 실행한 종료 코드와 끝 줄이다. 진단-02 는 양성 대조(경고 2)가 있다.
- 커버리지 해소: 스크립트-01 ~ 03 — 트리 모양 · 세 도구 명령 · 「쟀다」 글 · 요약 줄 모양은 도우미 `tree` · `TOOLS` · `MEASURED` · `BAD_SETS` · `summary_after` 에 글자 그대로 있고 `m` 이 경우마다 한 줄을 찍는다.
- 커버리지 해소: 스크립트-04 — 시작 판 도구 세 파일은 `base_dir`, 변이 줄은 `LEXISTS_TRUE`, CI 단계 두 줄은 `m_tests` 에 글자 그대로 있다.
- 커버리지 해소: 구조-02 — 네 파일 경로와 찾을 낱말은 도우미 `m_usage` 의 `need` 에 글자 그대로 있다.
- 커버리지 해소: 오류-01 · 오류-02 — 다섯 명령 · 비교 판 · 일곱 줄은 도우미 `m_keep` · `ABSENT` · `CX_KEEP` 에 글자 그대로 있다.
- 커버리지 해소: 스킬-01 — 파일 경로 · 옛 글 · 찾을 낱말(`sync-evals.py` · `나머지` · `2`)은 도우미 `KAIZEN` · `KAIZEN_OLD` · `m_kaizen` 에 글자 그대로 있다.
- 커버리지 검출기(6.5 (4)) 출력 다섯 건(스크립트-01 · 02 · 03, 스킬-01, 구조-02)은 모두 위 해소 줄로 처리했다 — 경로 · 글자는 도우미가 상수로 들고 조건 줄의 `m <조건 번호>` 가 부른다. 스크립트-02 의 `os.path.lexists` 는 변이 `LEXISTS_TRUE` 가 그 자리를 무력화해 재고(`mut_ok`), 도우미가 두 파일의 사용 수(`lexists_uses`)를 찍는다.
