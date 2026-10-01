---
feature: "레포 밖 훅 둘을 harness 플러그인 훅으로 — 원본 하나"
slug: after-1001-hooks-into-harness
created: "2026-10-01 13:04"
complexity: "복잡"
conditions: 26
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
---

## 배경

- 묶음 hk. 사용자 결정(2026-10-01): 훅 원본을 하나로 — `~/.claude/settings.json` 에 개인 등록으로 돌던 두 훅(Stop → `qa-pending-check.sh`, PostToolUse `Edit|Write` → `lint-contract-oracle.sh`)을 harness 플러그인 훅으로 등록한다. 개인 설정 쪽 등록 · 파일은 부모가 릴리스 · 설치 뒤 지운다 — 이 묶음은 레포만 바꾼다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-hk`, 가지 `chore/ak3-hk`, 시작 판 `BASE` = `b33ed94a` (`origin/main`, #128 합침 — 2026-10-01 `git fetch` 뒤).
- 사용자가 할 일: 없음. 부모가 할 일(이 계약 밖): harness 를 minor 로 릴리스(0.17.1 → 0.18.0)하고 설치한 뒤 `~/.claude/settings.json` 의 두 등록과 `~/.claude/hooks/` 의 두 훅 파일을 지우고, `~/.claude/CLAUDE.md` 의 `~/.claude/hooks/qa-pending-check.sh` 언급을 플러그인 훅으로 고친다. `~/.claude/hooks/_lib-hook-payload.sh` 는 개인 훅 `block-dirwide-autofixer.sh` · `parallel-session-guard.sh` 가 계속 쓰므로 지우지 않는다. 기록(구조-04)에 이 할 일과 판 올림 판단을 적는다.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-hk` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 돌린 뒤 W 맨 위 폴더에서 root 가 아닌 사용자로 잰다. 이 가지는 이 스프린트만 커밋한다. 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. `TMPDIR` 는 scratch 아래 절대 경로 폴더로 둔다. `~/.claude` 아래는 읽기만 한다.

용어 (조건마다 되풀이하지 않는다):

- 「두 훅」 = `lint-contract-oracle.sh` · `qa-pending-check.sh`. 「도우미」 = `_lib-hook-payload.sh`. 「옮긴 세 파일」 = 두 훅과 도우미 — 옛 자리 `harness/evals/hooks/`, 새 자리 `harness/scripts/`(기존 플러그인 훅 `env-check.sh` · `sdk-guard.sh` · `run-guard.sh` · `commit-guard.sh` 와 같은 폴더).
- 「훅 시험 둘」 = `harness/evals/hooks/lint-contract-oracle-test.sh` · `harness/evals/hooks/qa-pending-check-test.sh`. 「플러그인 훅 시험」 = 새 `harness/evals/hooks/plugin-hooks-test.sh`.
- 「겹침 검사」 = `scripts/check-user-hook-overlap.py`(옛 `scripts/check-user-hook-copies.py` 를 바꾼 것), 그 시험 = `scripts/test-check-user-hook-overlap.py`(옛 `scripts/test-check-user-hook-copies.py`).
- 「두 등록」 = hooks.json 의 ① PostToolUse · matcher `Edit|Write` · timeout 10 · statusMessage `계약 오라클 린터` · 명령 `"${CLAUDE_PLUGIN_ROOT}/scripts/lint-contract-oracle.sh"` ② Stop · matcher 없음 · timeout 10 · statusMessage `QA 실행 여부 확인` · 명령 `"${CLAUDE_PLUGIN_ROOT}/scripts/qa-pending-check.sh"`. 일 · 조건 · timeout · statusMessage 는 2026-10-01 개인 설정 값 그대로이고, 명령 모양은 기존 플러그인 훅처럼 큰따옴표로 감싼 직접 실행이다(실행 비트 필요 — `validate-plugin.py` V8).

항목별 처리 방침 (결정):

- **(1) 옮기기** — 옮긴 세 파일을 `git mv` 로 `harness/scripts/` 에 둔다. 두 훅의 도우미 찾는 줄은 `LIB="${CLAUDE_HOOK_LIB:-$(dirname "${BASH_SOURCE[0]}")/_lib-hook-payload.sh}"` — 이 파일 옆 도우미가 기본이고 `CLAUDE_HOOK_LIB` 를 주면 그것이다. 홈의 `.claude/hooks` 에 기대지 않는다. 바뀌는 줄은 이 줄과 그 설명 한 줄, 도우미 머리 설명 두 줄(누가 부르는지), 그리고 계약 오라클 훅 머리 설명 두 줄이다 — 그 설명이 레포 뿌리 `docs/superpowers/…` 경로를 적어 설치본에서 못 여는 경로 검사(`scripts/check-install-docs-guidance.py`)가 `NEED` 를 낸다(봉인 전 구현 뒤 모양 사본에서 실측). 경로 글자만 빼고 뜻은 남긴다. 그 밖의 줄은 바꾸지 않는다(구조-03).
- **(2) 등록** — `harness/hooks/hooks.json` 에 두 등록을 더한다. 기존 등록 다섯은 차례까지 그대로다.
- **(3) 사본 정리** — 옛 자리 세 파일은 지운다(옮김). 훅 시험 둘은 기본 훅 경로를 `harness/scripts/` 로 바꾸고, `CLAUDE_HOOK_LIB` 를 더는 훅에 넣지 않는다(훅이 제 옆 도우미를 찾는지 시험이 확인하게). 시험의 준비 확인 `lib` 는 `CLAUDE_HOOK_LIB` 가 없으면 `harness/scripts/_lib-hook-payload.sh` 를 본다 — 훅 자리 옆을 보게 두면 대역 훅을 줄 때 준비 실패 2 로 끝나 음성 대조가 1 을 못 낸다(봉인 전 사본 실측). 레포 안 같은 이름 훅 파일은 `.harness/` 기록을 빼면 한 벌씩이다.
- **(3+) 플러그인 훅 시험** — 새 시험이 hooks.json 의 명령 글자를 jq 로 꺼내, `CLAUDE_PLUGIN_ROOT` 만 빈칸이 든 플러그인 사본 폴더로 주고, 빈 `HOME` · `CLAUDE_HOOK_LIB` 없이 훅 입력 JSON 을 넣어 돌린다. 등록 둘의 값, 양성(계약 파일 편집 → 경고, Stop · 내 계약 QA 없음 → 안내), 음성(계약 아닌 파일, 남의 계약, 되돌린 답 `stop_hook_active`)을 본다. 플러그인 폴더는 환경 변수 `PLUGIN_HOOKS_ROOT`(기본: 시험 파일 기준 `harness/`)로 바꿀 수 있고, 시험은 그 폴더의 `hooks/` · `scripts/` 를 늘 임시 폴더 아래 빈칸 든 폴더(`plugin root`)로 복사해 그 복사본을 `CLAUDE_PLUGIN_ROOT` 로 준다 — 따옴표 빠진 명령을 잡으려면 이 복사가 있어야 한다. 등록이 없거나 값이 다르거나 훅이 기대 출력을 안 내면 실패 1, hooks.json · jq 가 없으면 준비 실패 2. 끝 줄은 `실패 N 건`. CI 에 등록한다.
- **(3++) 실제 claude 실행** — 이 맥에서 `claude -p --setting-sources project --plugin-dir <W>/harness --no-session-persistence --include-hook-events` 로 개인 설정 · 설치된 플러그인 없이 이 플러그인 폴더 하나만 얹어 돌리면 두 훅이 실제로 돈다(봉인 전 구현 뒤 모양 사본에서 실측: PostToolUse:Write 에 계약 오라클 경고, Stop 에 QA 안내, 되돌린 Stop 은 빈 출력). 이것을 조건으로 잰다(스크립트-04). CI 에는 claude 가 없어 넣지 않는다.
- **(4) 겹침 검사** — 설치본 맞대기는 필요 없어졌다. 같은 자리에서 「개인 설정(`settings.json` · `settings.local.json`)이 두 훅을 아직 등록해 두 번 도는지」 를 알리는 검사로 바꾸고 이름을 `check-user-hook-overlap.py` 로 바꾼다. `--settings-dir`(기본 `~/.claude`). 두 파일이 다 없으면 `개인 설정 없음 — 건너뜀` · 0, 훅 명령에 두 훅 파일 이름이 든 등록마다 `겹침: <설정 파일> <이벤트> <명령>` · 1, 없으면 `겹침 없음 (설정 파일 N 개)` · 0, 못 읽거나 깨진 JSON 은 `UNREADABLE <경로> (<까닭>)` · 2(`harness/evals/gate-exit-codes.md` 값). `겹침:` 줄 차례는 설정 파일 차례(`settings.json` → `settings.local.json`), 그 안에서 hooks 의 이벤트 차례 · 등록 차례다. 시험은 `--tool <검사 사본>`(기본 레포 검사)을 받고 임시 설정 폴더 일곱 경우를 돌려 경우마다 `PASS 경우 <번호> …` 또는 `FAIL 경우 <번호> …` 한 줄, 끝 줄 `경우 7 개 중 통과 N` 을 찍는다 — 경우 1 설정 폴더 없음 · 2 폴더만 있고 두 파일 없음(둘 다 건너뜀 0), 3 다른 훅만 있는 `settings.json`(겹침 없음 1 개 · 0), 4 `settings.json` 에 두 훅이 Stop · PostToolUse 로(1 · 그 차례), 5 `settings.local.json` 에만 qa 훅(1), 6 깨진 `settings.json`(2), 7 두 파일 모두 겹침 없음(겹침 없음 2 개 · 0). CI 의 옛 두 단계를 새 두 단계로 바꾸고 플러그인 훅 시험 단계를 더한다.
- **(5) 문서** — `harness/README.md` 에 `## 플러그인 훅` 절과 `<!-- AUTO:hooks -->` 표지를 두고 `python3 scripts/sync-docs.py harness` 로 표를 채운다. 그 표에서 matcher `Edit|Write` 의 세로 막대가 표 칸을 가르므로(봉인 전 실측 — 고치지 않으면 markdownlint MD056) `scripts/sync-docs.py` 의 훅 표 칸에서 `|` 를 `\|` 로 바꾼다. 다른 킷 README 는 바뀌지 않는다(`--check-only` 동기화 상태). README 를 옮긴 문서 사이트 페이지는 없다(아래 범위 경계).
- **(6) 판 번호** — 이 훅들이 harness 를 설치한 모든 사람에게 새로 돌게 되므로 minor 로 올릴 것을 기록에 적는다. 이 묶음은 `plugin.json` · `marketplace.json` 을 바꾸지 않는다(구조-05).

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 읽은 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `harness/evals/hooks/qa-pending-check.sh` | 1 ~ 137 줄 전체, 21 ~ 23 줄 | 도우미 기본이 `$HOME/.claude/hooks/_lib-hook-payload.sh` — 다른 사람 기계에서는 못 찾고 조용히 0 | 스크립트-02 · 03 · 오류-01 · 구조-03 |
| `harness/evals/hooks/lint-contract-oracle.sh` | 1 ~ 132 줄 전체, 9 · 22 줄 | 같은 도우미 기본. 9 줄 설명이 레포 뿌리 `docs/superpowers/` 경로 | 스크립트-02 · 03 · 구조-03 · 진단-05 |
| `harness/evals/hooks/_lib-hook-payload.sh` | 1 ~ 99 줄 | 2 ~ 4 줄 설명이 개인 훅(`block-dirwide-autofixer.sh` · `parallel-session-guard.sh`)을 부르는 쪽으로 적음 — 그 개인 훅은 `~/.claude/hooks/` 사본을 계속 쓴다 | 구조-03 |
| `harness/hooks/hooks.json` | 전체 | 등록 다섯(SessionStart · PreToolUse 셋 · PostToolUse 하나), Stop 없음 | 스크립트-01 |
| `harness/evals/hooks/lint-contract-oracle-test.sh` · `qa-pending-check-test.sh` | 1 ~ 17 · 1 ~ 16 줄 | 기본 훅 경로가 같은 폴더, `CLAUDE_HOOK_LIB` 를 같은 폴더 도우미로 넣어 줌, 설명이 `check-user-hook-copies.py` | 스크립트-03 · 구조-02 |
| `scripts/check-user-hook-copies.py` · `scripts/test-check-user-hook-copies.py` | 전체 (64 · 약 100 줄) | 설치본 세 파일 바이트 맞대기 — 원본이 하나가 되면 쓸모없다 | 스크립트-05 · 06 |
| `.github/workflows/ci.yml` | 242 ~ 257 줄 | 훅 시험 둘 · 맞대기 시험 · 맞대기 검사 단계. run 줄 56 개 | 스크립트-07 |
| `harness/README.md` | 1 ~ 80 줄 | AUTO 표지는 skills · agents 뿐, 훅 목록 없음. 44 ~ 75 줄 `## 커밋 안전 훅` | 스크립트-09 |
| `scripts/sync-docs.py` | 135 ~ 160 · 264 ~ 270 줄 | 훅 표가 matcher 를 그대로 넣어 `Edit\|Write` 가 표 칸을 가른다 | 스크립트-09 |
| `scripts/validate-plugin.py` | 606 ~ 720 줄 (V8) | hooks.json 이 직접 실행하는 `.sh` 의 실행 비트 · 따옴표를 본다 — 새 두 등록도 잰다 | 구조-03 |
| `scripts/check-install-docs-guidance.py` | 1 ~ 40 줄 | 킷 파일의 레포 뿌리 `docs/<칸>/` 경로에 안내 줄을 요구 — `harness/scripts/` 로 옮긴 계약 오라클 훅의 9 줄이 걸린다(evals/ 아래는 안 봤다) | 진단-05 |
| `~/.claude/settings.json` (읽기만) | hooks 절 | Stop · PostToolUse 두 등록 값 = 두 등록 값(명령만 `bash /Users/jackson/.claude/hooks/…`). `settings.local.json` 에는 hooks 없음 | 스크립트-01 · 05 |

봉인 전 실측 (W 시작 판 `b33ed94a`, 2026-10-01): 이 계약 측정은 오류-02 · 구조-05 · 진단-04 만 종료 코드 0(지킬 동작), 나머지는 1 (산출물 없음 — 각 조건 측정 줄의 「시작 판」 값). 시작 판 `bash scripts/ci-local.sh <W>` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · 종료 코드 0. 이 맥의 `python3 scripts/check-user-hook-copies.py` 는 `설치본 3 개가 레포 본과 같다` · 0.

## Script

- [ ] 스크립트-01: 두 등록이 hooks.json 에 한 번씩 있다 — `harness/hooks/hooks.json` 의 등록(이벤트 · matcher · timeout · statusMessage · 명령)에서 두 등록이 각각 정확히 1 개이고, 두 등록을 뺀 목록이 시작 판 등록 다섯과 차례까지 같으며, `~/.claude/settings.json` 이 두 훅을 등록해 두었으면 그 이벤트 · matcher · timeout · statusMessage 가 두 등록과 같다(지웠으면 `absent`). Given 공통 전제 G, When `m 스크립트-01`, Then `new_found=2 base_kept=1 base_regs=5 regs=7 personal=same` 또는 `personal=absent` · `ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` (도우미 `NEW_REGS` · `registrations`). 시작 판 `new_found=0 base_kept=1 base_regs=5 regs=5 personal=same ok=0` · 종료 코드 1
  음성 대조: 등록 하나를 빼거나 timeout · statusMessage 를 바꾸면 `new_found` 가 2 가 아니고, 기존 등록 차례를 바꾸면 `base_kept=0` 이다
- [ ] 스크립트-02: 플러그인 훅 시험이 hooks.json 명령 그대로 두 훅을 돌린다 — 빈 `HOME` 에서 `CLAUDE_HOOK_LIB` · `PLUGIN_HOOKS_ROOT` 를 지우고 `bash harness/evals/hooks/plugin-hooks-test.sh` 를 `LC_ALL=C` · `LC_ALL=en_US.UTF-8` 로 돌리면 둘 다 끝 줄 `실패 0 건` · 종료 코드 0 이다. 같은 빈 `HOME` 에서 `PLUGIN_HOOKS_ROOT` 로 ① 시작 판 `harness/`(`git archive b33ed94a harness`) ② 두 등록 명령의 큰따옴표를 뺀 플러그인 사본 ③ 두 훅의 도우미 기본을 옛 `$HOME/.claude/hooks/_lib-hook-payload.sh` 로 되돌린 플러그인 사본을 주면 셋 다 종료 코드 1 이다. Given 공통 전제 G, When `m 스크립트-02`, Then `runs=2 pass=2 base_rc=1 noquote_rc=1 homelib_rc=1 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02` (도우미 `PLUGIN_TEST` · `strip_quotes` · `home_lib` · `base_tree`). 시작 판 `MISSING harness/evals/hooks/plugin-hooks-test.sh` · `ok=0` · 종료 코드 1
  음성 대조: ① ② ③ 이 이 조건의 음성 대조다 — 등록이 없거나, 빈칸 든 경로를 셸이 쪼개거나, 훅이 홈의 도우미를 찾으면 시험이 실패한다
- [ ] 스크립트-03: 훅 시험 둘이 새 자리 훅으로 돈다 — 옮긴 세 파일이 `harness/scripts/` 에 있고, 빈 `HOME` 에서 `CLAUDE_HOOK_LIB` · `LINT_ORACLE_HOOK` · `QA_PENDING_HOOK` 을 지운 채 훅 시험 둘을 `LC_ALL=C` · `LC_ALL=en_US.UTF-8` 로 돌리면 네 번 모두 끝 줄 `실패 0 건` · 종료 코드 0 이다. 시험이 받는 환경 변수로 훅 자리에 `exit 0` 만 하는 대역을 주면 두 시험 모두 1 이다. 그리고 훅 시험 둘의 줄 가운데 앞뒤 빈칸을 뗀 모양이 `export CLAUDE_HOOK_LIB` 로 시작하는 줄이 0 개다(시험이 훅에 도우미를 넣지 않는다). Given 공통 전제 G, When `m 스크립트-03`, Then `runs=4 pass=4 stub_rcs=1,1 lib_exports=0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03` (도우미 `HOOK_TESTS` · `HOOK_ENV`). 시작 판 `MISSING harness/scripts/lint-contract-oracle.sh harness/scripts/qa-pending-check.sh harness/scripts/_lib-hook-payload.sh` · `ok=0` · 종료 코드 1
  음성 대조: 대역 훅(아무것도 안 함)이면 두 시험이 실패한다 — 시험이 훅 출력을 직접 잰다
- [ ] 스크립트-04: 실제 claude 에서 플러그인 훅으로 돈다 — 이 맥에서 임시 프로젝트(이 실행의 세션 번호가 `owner_session` 인 활성 계약 `sprint-contract-x.md`, 결과 파일 없음)에서 `claude -p --setting-sources project --plugin-dir <W>/harness --session-id <새 번호> --no-session-persistence --model haiku --permission-mode acceptEdits --output-format stream-json --verbose --include-hook-events` 로 「Write 로 `.harness/sprint-contract-y.md` 에 산문 grep 측정 조건 하나를 쓰고 done」 을 시키면, 시작 이벤트의 플러그인 목록(내장 `builtin` 빼고)이 정확히 `[<W>/harness]` 이고, PostToolUse 훅 응답 가운데 `계약 오라클 경고` 를 담은 것이 1 개 이상, Stop 훅 응답 가운데 `QA 가 끝나지 않았습니다` 와 `sprint-contract-x.md` 를 함께 담은 것이 1 개 이상이고, 모든 훅 응답이 종료 코드 0 · `success` 다. 같은 실행을 시작 판 `harness/` 사본으로 하면 두 수가 모두 0 이다. Given 공통 전제 G · `claude` 가 로그인된 채 PATH 에 있다, When `m 스크립트-04`, Then `plugin_ok=1 lint=1 stop=1 errors=0 base_lint=0 base_stop=0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04` (도우미 `e2e_run` · `E2E_PROMPT`). claude 가 없거나, 실행 결과가 `success` 가 아니거나, 모델이 Write 를 안 부르면 2 (잴 수 없음 — 다시 잰다. 2 가 세 번 이어지면 평가자는 이 조건을 `[미검증]` 으로 적고, 계약 전체에서 `[미검증]` 은 1 건까지 받는다). 시작 판 `MISSING harness/scripts/lint-contract-oracle.sh harness/scripts/qa-pending-check.sh` · `ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `plugin_ok=1 lint=1 stop=1 errors=0 base_lint=0 base_stop=0 ok=1` · 0
  음성 대조: 시작 판 `harness/` 는 두 등록이 없어 같은 실행에서 두 훅이 안 돈다(`base_lint=0 base_stop=0`) — 등록을 지우면 이 측정이 1 이다
- [ ] 스크립트-05: 겹침 검사가 개인 설정 상태를 바르게 알린다 — 겹침 검사를 ① `--settings-dir <없는 폴더>` 로 돌리면 종료 코드 0 · 출력이 정확히 `개인 설정 없음 — 건너뜀` 한 줄 ② 인자 없이 돌리면, 도우미가 검사와 따로 `~/.claude/settings.json` · `settings.local.json` 을 읽어 낸 알려진 답(「파일 이름:이벤트:훅 이름」 목록)과 `겹침:` 줄에서 뽑은 같은 꼴 목록이 차례까지 같고, 종료 코드가 그 목록이 비면 0 · 아니면 1 ③ 이 맥 개인 설정 사본에서 두 훅 등록만 지운 폴더로 돌리면 0 · 출력이 정확히 `겹침 없음 (설정 파일 N 개)` 한 줄(N 은 이 맥에 있는 개인 설정 파일 수) ④ 깨진 `settings.json` 하나만 둔 폴더로 돌리면 2 · `UNREADABLE` 과 빈칸으로 시작하는 줄 정확히 1 개다. 도우미가 이 맥 개인 설정을 못 읽으면 2 (잴 수 없음). Given 공통 전제 G, When `m 스크립트-05`, Then `none_ok=1 home_ok=1 cleaned_ok=1 broken_ok=1 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-05` (도우미 `known_overlaps` · `got_overlaps`). 시작 판 `MISSING scripts/check-user-hook-overlap.py` · `ok=0` · 종료 코드 1
  알려진 답: 봉인 전 이 맥 `known=['settings.json:Stop:qa-pending-check.sh', 'settings.json:PostToolUse:lint-contract-oracle.sh']` — 구현 뒤 모양 사본 검사 `got` 이 같고 `home_rc=1`. 부모가 개인 등록을 지우면 답이 빈 목록 · 0 으로 바뀌며 도우미가 그때그때 읽는다
- [ ] 스크립트-06: 겹침 시험이 대역 검사를 잡는다 — `python3 scripts/test-check-user-hook-overlap.py` 끝 줄 `경우 7 개 중 통과 7` · 종료 코드 0 이고, `--tool` 로 `print("개인 설정 없음 — 건너뜀")` 한 줄짜리 대역을 주면 `FAIL 경우` 번호가 정확히 3,4,5,6,7 이고 1 이다. Given 공통 전제 G, When `m 스크립트-06`, Then `tail=[경우 7 개 중 통과 7] ok_tail=1 stub_fails=3,4,5,6,7 stub_rc=1 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-06`. 시작 판 `MISSING scripts/test-check-user-hook-overlap.py` · `ok=0` · 종료 코드 1
  음성 대조: 대역은 늘 건너뜀으로 0 을 내는 검사다 — 겹침 · 깨진 JSON · 겹침 없음 줄을 못 내는 판을 경우 3 ~ 7 이 잡는다
- [ ] 스크립트-07: CI 는 옛 두 단계를 새 셋으로 바꿨을 뿐이다 — `.github/workflows/ci.yml` 의 run 줄에서 `bash harness/evals/hooks/plugin-hooks-test.sh` · `python3 scripts/test-check-user-hook-overlap.py` · `python3 scripts/check-user-hook-overlap.py` 가 각각 정확히 1 개, `python3 scripts/test-check-user-hook-copies.py` · `python3 scripts/check-user-hook-copies.py` 는 0 개(시작 판에는 각각 1 개)이고, 새 셋을 뺀 run 줄 목록이 시작 판에서 옛 둘을 뺀 목록과 차례까지 같으며, 전체 run 줄이 시작 판보다 정확히 1 개 많다. Given 공통 전제 G, When `m 스크립트-07`, Then `base_runs=56 runs=57 new_once=1 old_gone=1 kept=1 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-07` (도우미 `NEW_RUNS` · `OLD_RUNS` · `ci_runs`). 시작 판 `base_runs=56 runs=56 new_once=0 old_gone=0 kept=0 ok=0` · 종료 코드 1
  음성 대조: 남은 run 줄 둘의 자리를 바꾸면 개수가 같아도 `kept=0` 이다
- [ ] 스크립트-08: 리눅스에서도 돈다 — W 를 읽기 전용으로 붙인 도커 `ubuntu:24.04`(`LC_ALL=C.UTF-8`, `apt-get install -y jq zsh python3`, root 가 아닌 사용자)에서 훅 시험 둘 · 플러그인 훅 시험 · 겹침 시험 · 겹침 검사를 돌리면 다섯 다 종료 코드 0 이고 끝 줄이 차례대로 `실패 0 건` · `실패 0 건` · `실패 0 건` · `경우 7 개 중 통과 7` · `개인 설정 없음 — 건너뜀` 이며, 그 안의 awk 는 mawk · grep 은 GNU grep 이다. Given 공통 전제 G · 도커 데몬이 돈다, When `m 스크립트-08`, Then `results=5 good=5 mawk=1 gnu_grep=1 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-08` (도우미 `DOCKER_SCRIPT`). 도커를 못 쓰거나 apt 가 실패하면 2 (잴 수 없음 — 다시 잰다). 시작 판 `results=5 good=2 mawk=1 gnu_grep=1 ok=0` · 종료 코드 1 (플러그인 훅 시험 127 · 겹침 시험 · 검사 2 — 파일이 없다). 구현 뒤 모양 사본 `results=5 good=5 mawk=1 gnu_grep=1 ok=1` · 0
  음성 대조: 시작 판에서는 플러그인 훅 시험 · 겹침 시험 · 겹침 검사 파일이 없어 `good` 이 5 가 아니다
- [ ] 스크립트-09: README 훅 목록이 hooks.json 과 맞는다 — `python3 scripts/sync-docs.py --check-only` 가 종료 코드 0 이고 `모든 README가 동기화 상태입니다.` 를 찍으며, `harness/README.md` 의 `<!-- AUTO:hooks -->` 안 표 몸통 줄이 도우미 `WANT_HOOK_ROWS` 일곱 줄(마지막 둘이 ``| `PostToolUse` | `lint-contract-oracle.sh` | PostToolUse (matcher: Edit\|Write) |`` · ``| `Stop` | `qa-pending-check.sh` | Stop |``)과 차례까지 같고, 표지 밖 글에 `scripts/qa-pending-check.sh` · `scripts/lint-contract-oracle.sh` · `scripts/check-user-hook-overlap.py` · `CLAUDE_HOOK_LIB` · `plugin-hooks-test.sh` 가 모두 있고, markdownlint-cli2(MD013 끔) 경고 0 건 · `Linting: 1 file` 이다. 양성 대조: 같은 README 에서 `Edit\|Write` 를 `Edit|Write` 로 되돌린 사본은 MD056 이 1 건 이상이다. Given 공통 전제 G, When `m 스크립트-09`, Then `synced=1 rows=7 rows_ok=1 prose_miss=[] mdl=0 pos_md056=1` 이상 · `ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-09` (도우미 `WANT_HOOK_ROWS` · `auto_rows` · `mdl_issues`, markdownlint-cli2 0.23.3 `<scratch>/fin/mdl`). markdownlint 가 없으면 2. 시작 판 `synced=1 rows=0 rows_ok=0 prose_miss=[다섯] mdl=0 pos_md056=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `rows=7 rows_ok=1 prose_miss=[] mdl=0 pos_md056=1` · 0

## Error

- [ ] 오류-01: 두 훅은 실패해도 막지 않는다 — `harness/scripts/` 의 두 훅마다 ① `CLAUDE_HOOK_LIB=<없는 파일>` 에 걸릴 입력(계약 파일 Write · 내 활성 계약의 Stop) ② 빈 입력 ③ 깨진 JSON `{` 을 넣으면 종료 코드 0 · 출력 0 바이트이고, ④ 도우미가 있을 때 같은 걸릴 입력은 0 · 출력에 `additionalContext` 가 있다. Given 공통 전제 G, When `m 오류-01`, Then 여덟 줄 `OK` · `cases=8 right=8 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01`. 시작 판 `MISSING harness/scripts/lint-contract-oracle.sh harness/scripts/qa-pending-check.sh` · `ok=0` · 종료 코드 1
  음성 대조: ④ 가 ① ~ ③ 의 짝이다 — 훅이 늘 아무것도 안 내는 판이면 ④ 가 `BAD` 다
- [ ] 오류-02: 기존 플러그인 훅은 그대로다 — `git diff --name-only b33ed94a..chore/ak3-hk -- harness/scripts/env-check.sh harness/scripts/sdk-guard.sh harness/scripts/run-guard.sh harness/scripts/commit-guard.sh` 가 빈 출력이고, `bash harness/evals/hooks/commit-guard-test.sh` 가 끝 줄 `실패 0 건` · 종료 코드 0 이다. Given 공통 전제 G, When `m 오류-02`, Then `same=1 commit_guard_rc=0 tail=[실패 0 건] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02` (도우미 `KEEP_SCRIPTS`). 시작 판 `same=1 commit_guard_rc=0 tail=[실패 0 건] ok=1` · 0 (지킬 동작). 구현 뒤 모양 사본 같음 · 0

## Skill

- [ ] 스킬-00: N/A (이번 변경은 스킬 · 에이전트 파일을 건드리지 않는다 — 바뀌는 곳은 harness/scripts · harness/hooks · harness/evals/hooks · harness/README.md · scripts/ · .github/. 측정: git diff --name-only b33ed94a..chore/ak3-hk -- '*SKILL.md' 'harness/agents' '.claude/skills' | grep -c . 이 0)

## Architecture

- [ ] 구조-01: 커밋 규칙 — `b33ed94a..chore/ak3-hk` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(`harness` · `scripts` · `.github` · `.harness` 는 서로 다른 폴더)이며, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이고, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-01`, Then 모든 줄 `OK` · `bad=0` · `scope_entries=17` · 종료 코드 0 (범위 목록이 열일곱이 아니면 1) [exact]
  측정: `m 구조-01` (도우미 `scope_block` · `in_scope`). 시작 판(봉인 커밋 전) `commits=0 bad=0` · 종료 코드 1
- [ ] 구조-02: 바뀐 파일 열일곱 · 훅 파일 한 벌 — `git diff --no-renames --name-only b33ed94a..chore/ak3-hk -- . ':(exclude).harness'` 가 정확히 도우미 `WANT_CHANGED` 열일곱(옛 자리 셋 · 새 자리 셋 · 훅 시험 둘 · 플러그인 훅 시험 · `harness/hooks/hooks.json` · `harness/README.md` · 옛 검사 둘 · 새 검사 둘 · `scripts/sync-docs.py` · `.github/workflows/ci.yml`)이고, 가지 끝에서 `.harness/` 밖에 추적되는 옮긴 세 파일 이름은 정확히 `harness/scripts/_lib-hook-payload.sh` · `harness/scripts/lint-contract-oracle.sh` · `harness/scripts/qa-pending-check.sh` 셋이다. Given 공통 전제 G, When `m 구조-02`, Then `files=17 extra=[] lack=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02` (도우미 `WANT_CHANGED` · `MOVED`). 시작 판 `files=0 extra=[] lack=[열일곱]` · `ok=0` · 종료 코드 1
- [ ] 구조-03: 옮긴 세 파일은 필요한 줄만 바뀌고 홈에 기대지 않는다 — 시작 판 옛 자리 대비 (지운 줄, 더한 줄)이 `lint-contract-oracle.sh` (3, 4) · `qa-pending-check.sh` (1, 2) · `_lib-hook-payload.sh` (2, 2) 이고, 세 파일의 주석이 아닌 줄에 `.claude/hooks` 가 0 번이며, 가지 끝 git 모드가 셋 다 `100755` 이고, `python3 scripts/validate-plugin.py harness --check=hook-exec` 가 종료 코드 0 이다. Given 공통 전제 G, When `m 구조-03`, 지운 줄은 도우미 `WANT_REMOVED` 의 줄(시작 판 글자 그대로 — 두 훅의 옛 도우미 찾는 줄, 계약 오라클 훅 9 · 10 줄, 도우미 3 · 4 줄)과 정확히 같아야 한다. Given 공통 전제 G, When `m 구조-03`, Then 세 줄 `OK` · `removed_ok=1` · `files=3 right=3 v8_rc=0 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03` (도우미 `WANT_MOVE_DIFF`). 시작 판 `MISSING harness/scripts/…` 셋 · `ok=0` · 종료 코드 1
  음성 대조: 도우미 기본을 옛 `$HOME/.claude/hooks/…` 로 두면 주석 아닌 줄의 `.claude/hooks` 가 1 이라 `BAD`, 실행 비트를 빼면 V8 이 1 이다
- [ ] 구조-04: 기록 — `.harness/.meta/after-kaizen-0928/hk-notes.md` 에 낱말 `minor` · `0.18.0`(판 올림 판단과 까닭) · `settings.json` · `_lib-hook-payload.sh` · `block-dirwide-autofixer.sh`(지우면 안 되는 까닭) · `CLAUDE.md`(부모가 고칠 언급) · `check-user-hook-overlap` · `--plugin-dir`(실제 claude 확인) · `도커` · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수 가운데 `b33ed94a..chore/ak3-hk` 커밋 해시 앞 8 자리와 같은 것이 3 개 이상이다. Given 공통 전제 G, When `m 구조-04`, Then `keys_ok=1 miss=[] branch_hashes=` 3 이상 · `ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-04` (도우미 `NOTE_KEYS`). 시작 판 `MISSING .harness/.meta/after-kaizen-0928/hk-notes.md keys_ok=0` · 종료 코드 1
- [ ] 구조-05: 판 번호는 이 묶음에서 안 바꾼다 — `git diff --name-only b33ed94a..chore/ak3-hk -- harness/.claude-plugin .claude-plugin` 이 빈 출력이다(릴리스는 부모). Given 공통 전제 G, When `m 구조-05`, Then `version_files_changed=[] ok=1` · 종료 코드 0 [exact]
  측정: `m 구조-05`. 시작 판 `version_files_changed=[] ok=1` · 0 (지킬 동작)

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git ls-remote origin chore/ak3-hk | grep -c .` 이 0. 봉인 전 0)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 `harness/README.md` · 새 기록 `.harness/.meta/after-kaizen-0928/hk-notes.md` 에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 두 훅 · 도우미는 플러그인 `harness/scripts/` 에 있어 설치한 누구나 돌고, 새 시험 · 검사는 CI 에 등록돼 누구나 부른다 — 스크립트-01 `new_found=2` · 스크립트-07 `new_once=1`)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 도우미는 `.harness/` 밖에 정확히 하나(`harness/scripts/_lib-hook-payload.sh`)이고 두 훅이 모두 그것을 기본으로 부르며(`LIB_DEFAULT_NEW` 줄), 새로 더한 파일이 놓인 폴더가 모두 시작 판에 이미 있던 폴더다(새 폴더 0). 겹침 검사는 옛 맞대기 검사 자리를 바꿔 쓰고, 출력 · 종료 코드 모양은 레포의 `UNREADABLE <경로> (<까닭>)` · 0/1/2 를 따른다. Given 공통 전제 G, When `m 재사용-02`, Then `libs=['harness/scripts/_lib-hook-payload.sh'] lib_users=2 new_dirs=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 재사용-02`. 시작 판 `libs=['harness/evals/hooks/_lib-hook-payload.sh'] lib_users=0 new_dirs=[] ok=0` · 종료 코드 1

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only b33ed94a..chore/ak3-hk | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀌거나 새로 생긴 `.py` 셋(`scripts/check-user-hook-overlap.py` · `scripts/test-check-user-hook-overlap.py` · `scripts/sync-docs.py`)은 `python3 -m py_compile` 종료 코드 0, `.sh` 여섯(옮긴 세 파일 · 훅 시험 둘 · 플러그인 훅 시험)은 `bash -n` 종료 코드 0 이고 `shellcheck -f gcc <파일> | grep -c .` 이 0, `.json` 하나(`harness/hooks/hooks.json`)는 `jq empty` 종료 코드 0, `.md` 둘(`harness/README.md` · `.harness/.meta/after-kaizen-0928/hk-notes.md`)은 markdownlint-cli2(MD013 끔) 경고 0 건 · 파일마다 `Linting: 1 file`
  측정: md 는 `<scratch>/fin/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/fin/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(`<scratch>` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`, 설정 `{ "config": { "MD013": false } }`). 시작 판 `harness/README.md` 0 건, 훅 시험 둘 · 옮길 세 파일 `shellcheck` 0 줄. 양성 대조: `printf 'x=$1\necho $x\n' | shellcheck -s bash -f gcc - | grep -c .` → 1 이상, 스크립트-09 의 막대 되돌린 README 사본 → MD056 1 이상
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: 실제 claude 구동에서 훅 오류 0 — 스크립트-04 와 같은 꼴의 실행(이 가지 `harness/` 만)에서 모든 훅 응답(SessionStart · PostToolUse · Stop)이 종료 코드 0 · `success` 이다. Given 공통 전제 G, When `m 진단-04`, Then `errors=0 ok=1` · 종료 코드 0 [exact]
  측정: `m 진단-04` (도우미 `m_diag04` — `e2e_run` 을 이 가지 폴더로 한 번). claude 를 못 쓰거나 Write 를 안 부르면 2 (스크립트-04 와 같은 재시도 규칙). 시작 판 `errors=0 ok=1` · 0 (시작 판에도 기존 훅은 오류 없이 돈다 — 이 조건은 새 훅이 오류를 더하지 않는지 지키는 조건이다)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 통과한다 — `bash scripts/ci-local.sh <W>` (W 맨 위 폴더에서, TMPDIR 은 scratch 아래 새 폴더. 레포 밖 옛 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 지금 없다 — 봉인 전 확인)의 끝 줄이 `steps=57 run=52 skip=5 unsupported=0 failed=<F>` 이고, `FAIL` 로 시작하는 줄은 단계 `User hook overlap check (개인 설정과 harness 플러그인 훅)` 하나뿐이거나 없으며, F 는 스크립트-05 의 알려진 답이 비었으면 0 · 아니면 1 이다(이 맥 개인 설정이 아직 두 훅을 등록한 동안 그 단계가 1 로 알리는 것이 이 검사의 할 일이다). 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `python3 scripts/check-install-docs-guidance.py` · `bash harness/evals/hooks/plugin-hooks-test.sh` · `python3 scripts/test-check-user-hook-overlap.py` 를 따로 돌린 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 ci-local 끝 줄 · `grep '^FAIL'`. 시작 판 · 구현 뒤 모양 사본 값은 `## 회귀 게이트` 에 적는다

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
harness/evals/hooks/_lib-hook-payload.sh
harness/evals/hooks/lint-contract-oracle.sh
harness/evals/hooks/qa-pending-check.sh
harness/scripts/_lib-hook-payload.sh
harness/scripts/lint-contract-oracle.sh
harness/scripts/qa-pending-check.sh
harness/evals/hooks/lint-contract-oracle-test.sh
harness/evals/hooks/qa-pending-check-test.sh
harness/evals/hooks/plugin-hooks-test.sh
harness/hooks/hooks.json
harness/README.md
scripts/check-user-hook-copies.py
scripts/test-check-user-hook-copies.py
scripts/check-user-hook-overlap.py
scripts/test-check-user-hook-overlap.py
scripts/sync-docs.py
.github/workflows/ci.yml
```

- 금지 패턴 고른 까닭: `project.yaml` 넷 가운데 금지-01(버전 하드코딩)은 이번에 버전 글자를 쓰는 파일이 없고(판 번호는 구조-05 가 안 바뀜으로 잰다), 금지-04(SKILL.md · 에이전트 frontmatter)는 스킬 · 에이전트 파일을 안 건드려(스킬-00) 걸릴 자리가 없다. 금지-02 · 03 만 둔다.
- 하지 않는 것: `~/.claude/` 아래 파일 고치기(개인 설정 등록 · 훅 파일 지우기 · `~/.claude/CLAUDE.md` 고치기는 부모가 릴리스 · 설치 뒤에 한다 — 기록에 할 일만 적는다), harness 판 번호 올리기 · 릴리스 · 합치기 · push, 레포 `.claude/settings.json`(프로젝트 설정) 훅, 개인 훅 `block-dirwide-autofixer.sh` · `parallel-session-guard.sh` 를 플러그인으로 옮기기, 도우미에서 두 훅이 안 쓰는 함수(`hook_deny` · `strip_heredoc_bodies`) 떼어 내기(개인 훅과 같은 파일 모양을 지켜 부모가 비교하기 쉽게 둔다), `.claude/kaizen-input/insights-report.md` 71 줄(지난 기록 글자), `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일.
- 문서 사이트 대응 페이지: `harness/README.md` 를 옮긴 HTML 페이지가 없다 — `grep -rln -E '커밋 안전 훅|HARNESS_COMMIT_GUARD|qa-pending-check|lint-contract-oracle|check-user-hook' docs --include='*.html'` 은 `docs/harness/contract-schema.html` 하나이고 그 자리는 계약 범위 목록 예시(`commit-guard.sh`)다(봉인 전 확인). 맞출 페이지가 없다.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약들은 `status: done` · APPROVE 이고 이 계약의 조건을 느슨하게 하지 않는다): fin 계약 `.harness/sprint-contract-after-0930-final.md` 의 도우미 `.harness/.meta/after-0930-final/measure.py` 가 재던 옛 자리 세 파일 · `scripts/check-user-hook-copies.py` · 그 시험 · CI 옛 두 단계 · 「`harness/hooks/hooks.json` 에 세 이름 없음」(그 계약 구조-04)은 2026-10-01 사용자 결정으로 뒤집힌다. `.harness/.meta/after-0928-harness-checks-r2/m-qapending*.sh` · `.harness/.meta/after-0929-codex-silent-pass/repro.sh` 는 `~/.claude/hooks` 설치본을 인자로 재는 지난 측정이다. 셋 다 CI 가 부르지 않는다(봉인 전 `grep -n 'after-0930-final\|after-0928-harness-checks-r2\|after-0929-codex-silent-pass' .github/workflows/ci.yml` 0 줄).
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `harness/` · `scripts/` · `.github/` · `.harness/` 는 따로. 옮기기는 `git mv` 뒤 옛 경로와 새 경로를 함께 `git commit -o` 한다(커밋 직전 훅이 이름 바꾸기를 풀어 두 경로를 다 대조한다 — 둘 다 범위 목록에 있다). 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋 · 기록 커밋은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-1001-hooks/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 다른 묶음 도우미를 부르지 않는다.
- `TMPDIR` 는 절대 경로로 준다.
- 봉인 전 실측(2026-10-01, W 시작 판 `b33ed94a`): 스크립트-01 ~ 09 · 오류-01 · 구조-01 ~ 04 · 재사용-02 종료 코드 1 (산출물 없음), 오류-02 · 구조-05 · 진단-04 종료 코드 0 (지킬 동작). 값은 각 조건 측정 줄에 있다.
- 진단-05 봉인 전 실측 — 시작 판(W, `npm ci` 뒤): `bash scripts/ci-local.sh <W>` 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 종료 코드 0.
- 오라클 해소: 스크립트-08 — 판정은 도커 안에서 시험 · 검사 다섯을 실제로 돌린 종료 코드와 끝 줄이다. 백틱 안 한글(`실패 0 건` 등)은 기대하는 끝 줄 값이지 grep 할 문장이 아니다.
- 오라클 해소: 진단-02 · 진단-05 — 파일 · 명령 목록을 백틱으로 적었을 뿐, 판정은 `py_compile` · `bash -n` · `shellcheck` · `jq empty` · markdownlint · 각 명령을 실행한 종료 코드와 끝 줄이다. 진단-02 는 양성 대조가 있다.
- 커버리지 해소: 스크립트-01 · 05 — `~/.claude/settings.json` · `settings.json` · `settings.local.json` · `harness/hooks/hooks.json` 은 도우미 `m_registration` · `known_overlaps` 가 경로 그대로 읽는다(`Path.home() / ".claude"` · `"harness/hooks/hooks.json"`).
- 커버리지 해소: 스크립트-02 · 04 — `harness/` · `$HOME/.claude/hooks/_lib-hook-payload.sh` · `.harness/sprint-contract-y.md` 는 도우미 `base_tree("harness")` · `LIB_DEFAULT_OLD` · `E2E_PROMPT` 에 글자 그대로 있다.
- 커버리지 해소: 스크립트-09 — README 경로와 표지 밖에 있어야 할 다섯 낱말은 도우미 `m_docs` 의 읽는 경로 `harness/README.md` 와 찾는 목록에 글자 그대로 있다. `lint-contract-oracle.sh` · `qa-pending-check.sh` 는 `WANT_HOOK_ROWS` 의 표 줄 안 글자다.
- 커버리지 해소: 구조-02 · 03 · 재사용-02 — 열일곱 경로 · 옮긴 세 파일 이름 · `.harness/` 제외는 도우미 `WANT_CHANGED` · `MOVED` · `NEW_DIR` 와 `not x.startswith(".harness/")` 에 글자 그대로 있다(경로 목록은 범위 목록 블록과 같은 열일곱이다 — 「목록을 두 번 적지 마라」 에 따라 조건 산문에는 개수만 둔다).
- 커버리지 해소: 구조-04 — 기록 경로와 낱말 열하나는 도우미 `NOTES` · `NOTE_KEYS` 에 글자 그대로 있다.
- 커버리지 검출기(6.5 (4)) 출력 아홉 건(스크립트-01 · 02 · 04 · 05 · 09, 구조-02 · 03 · 04, 재사용-02)은 모두 위 해소 줄로 처리했다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 `<scratch>/hk/impl` — W 를 `git clone --shared` 한 뒤 옮기기 · 등록 · 시험 / 겹침 검사 · 그 시험 · `sync-docs.py` / CI 를 폴더별 서명 커밋에 담고, 이 계약 · 이 도우미 · 기록 초안 사본 커밋, 2026-10-01): 이 계약 측정 열여덟(스크립트-01 ~ 09 · 오류-01 · 02 · 구조-01 ~ 05 · 재사용-02 · 진단-04) 모두 종료 코드 0 — 교차 진단 반영 뒤 고친 도우미로 다시 잼 (구조-01 `commits=8 bad=0 scope_entries=17`, 스크립트-03 `lib_exports=0`, 구조-03 `removed_ok=1` 셋, 구조-04 `branch_hashes=3`, 스크립트-04 실제 claude `plugin_ok=1 lint=1 stop=1 errors=0 base_lint=0 base_stop=0`, 스크립트-05 알려진 답 둘 · `home_rc=1`, 스크립트-08 도커 `results=5 good=5 mawk=1 gnu_grep=1`). 같은 사본에서 `ci-local.sh` 끝 줄 `steps=57 run=52 skip=5 unsupported=0 failed=1` · `FAIL` 줄은 `User hook overlap check (개인 설정과 harness 플러그인 훅)` 하나(이 맥 개인 설정의 두 등록을 알림 — 진단-05 의 F=1), CI 파일에만 있는 열 단계 모두 0 (`12/12 PASS` · `어긋남 0` · `checked=2 violations=0 infra_errors=0` · `실패 0 건` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `174 passed` · `need=0` · `실패 0 건` · `경우 7 개 중 통과 7`), `.py` 셋 `py_compile` 0, `.sh` 여섯 `bash -n` 0 · `shellcheck` 0 줄, `jq empty` 0, README markdownlint `Linting: 1 file` · 0 건, `validate-plugin.py --check=code-fence` 0. 양성 대조 `x=$1` 셸 조각 `shellcheck` 1 줄, 기록 초안의 줄 끝 빈칸 MD009 1 건(검사가 살아 있다 — 구현 때 기록은 0 건이어야 한다).
- 교차 대조(봉인 전): 바뀌는 글자 · 파일(`qa-pending-check` · `lint-contract-oracle` · `_lib-hook-payload` · `check-user-hook-copies` · `evals/hooks` · `hooks.json` · `harness/scripts`)을 `scripts/` · `.github/` · `harness/` · `.claude/` 에서 `grep -rn` 으로 찾았다 — 검사로 읽는 곳은 `.github/workflows/ci.yml` · `scripts/validate-plugin.py`(V8 실행 비트 · 따옴표 — 사본에서 0) · `scripts/sync-docs.py`(훅 표) · `scripts/check-install-docs-guidance.py`(킷 파일의 `docs/` 경로 — 사본에서 처음 `NEED harness/scripts/lint-contract-oracle.sh missing=superpowers` 로 1 이 나와 처리 방침 (1) 에 설명 두 줄 고치기를 더했다)와 바뀌는 파일 자신이다. 나머지는 이름만 적은 글이다(`.claude/kaizen-input/insights-report.md` 71 줄). 「더하라」 조건(스크립트-01 ~ 09 · 구조-02 ~ 04 · 재사용-02)과 「그대로」 조건(오류-02 · 구조-05 · 진단-05)이 함께 겨누는 파일은 `harness/hooks/hooks.json`(기존 등록 다섯 차례 유지 — 스크립트-01 `base_kept`) · `.github/workflows/ci.yml`(남은 run 줄 차례 유지 — 스크립트-07 `kept`)이고 사본에서 부딪히지 않았다.
- 도우미 지문(봉인 전, `shasum -a 256 <파일> | cut -c1-16`): 이 계약 `measure.py` `32eeb4f07489fd12`.
- 교차 진단(봉인 전, 2026-10-01 — Agent 도구가 없는 세션이라 새 `claude -p` 프로세스에 qa-evaluator 규칙 · 계약 · 도우미만 읽혀 읽기 전용으로 받았다): 지적 열둘 가운데 반영 아홉 — 금지-02 측정을 `git ls-remote`(push 0)로, 플러그인 훅 시험의 `PLUGIN_HOOKS_ROOT` · 빈칸 폴더 복사 · 종료 코드를 처리 방침 (3+) 에, 겹침 출력 차례와 시험 일곱 경우 · `--tool` · 출력 꼴을 (4) 에, 스크립트-03 에 `lib_exports=0`, 스크립트-05 개인 설정 못 읽음 → 2, 진단-04 를 따로 재는 `m_diag04`, 스크립트-04 재시도 세 번 · `[미검증]` 1 건, 구조-01 범위 목록 열일곱을 판정에, 구조-03 지운 줄 글자 대조 `WANT_REMOVED`, 구조-04 해시를 이 가지 커밋으로, 재사용-02 주석 아닌 줄로, 금지-01 · 04 를 고르지 않은 까닭. 반영 안 함 셋 — 스크립트-01 `personal` 이 재는 때에 따라 갈림(지운 뒤 `absent` 를 받게 이미 적음), 스크립트-08 mawk · GNU grep 은 컨테이너 도구 확인 수준(앞 묶음과 같은 수준), 스크립트-09 낱말 존재(표 일곱 줄은 글자 그대로 잰다).
