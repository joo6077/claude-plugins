---
feature: "Codex 최종 점검이 찾은 조용한 통과 결함 10 (cx)"
slug: after-0929-codex-silent-pass
created: "2026-09-29 20:10"
complexity: "복잡"
conditions: 27
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: "sha256:29a945b036808430"
measurement_digest: "sha256:82260932be2d56a1"
locked_at: "2026-09-29 20:23"
---

## 배경

- 묶음 cx. 근거는 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/codex-final.md` 의 결함 1~10 전부다. 검사가 실패해야 할 입력에서 종료 코드 0 을 내거나(결함 1~8) 경고 · 안내를 빠뜨린다(결함 9 · 10).
- 이름 주의: `remaining.md` 에 나오는 「cx」 · 「cx2」 · 「cx3」 은 지난 회차(after-kaizen-0926b) 묶음 이름이다. 이 계약의 cx 는 `codex-final.md` 한 파일만 근거로 한다.
- 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72). 결정 기록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md`.
- 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-cx` (가지 `chore/ak3-cx`). 모든 측정은 이 폴더를 현재 폴더로 두고 돌린다. 기준 판(이하 BASE) `cf51b6e1` — 가지를 만든 시점의 `chore/after-kaizen-0928`. 끝 판(이하 TIP)은 모든 커밋이 끝난 뒤 `git rev-parse chore/ak3-cx` 의 출력이다. `HEAD` 를 상한으로 쓰지 않는다.
- 측정 묶음 `$M` = `.harness/.meta/after-0929-codex-silent-pass/` — `repro.sh` (지문 `dab47b27e2cf24a7`) · `notes-check.sh` (지문 `c2ea108172d7be73`). 지문은 sha256 앞 16 자리다. 봉인 커밋과 따로 커밋한다. 앞 묶음 측정 `.harness/.meta/after-0929-final-sweep-rules/bambu-nosl.sh` (지문 `408752fe07c0f51e`) 을 그대로 부른다.
- `$B` = BASE 를 푼 폴더. 세션 scratch 아래 새 폴더에 `git archive cf51b6e1 | tar -x -C $B` 로 만든다.
- `$BK` = 고치기 전 훅 사본 폴더 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/hooks-backup-cx` — `lint-contract-oracle.sh` 지문 `f00b60e16f87135c` · `qa-pending-check.sh` 지문 `b18721b2ab224706`. 2026-09-29 20:05 에 `~/.claude/hooks/` 의 두 파일과 `cmp` 로 같았다. 이 폴더는 지우지 않는다.
- 임시 폴더는 세션 scratch 아래 새 폴더를 `TMPDIR` 로 준다. `node_modules` 는 작업 폴더에서 `npm ci` 로 만든다 (2026-09-29 실측 rc=0).
- 레포 밖 훅 둘(`~/.claude/hooks/lint-contract-oracle.sh` · `~/.claude/hooks/qa-pending-check.sh`)은 레포 커밋에 담기지 않는다. 고친 줄과 시험 출력 끝 줄을 notes 파일 `$N` = `.harness/.meta/after-kaizen-0928/cx-notes.md` 에 옮겨 적는다 (구조-03). 같은 묶음의 다른 notes(`ex-notes.md` · `fs1-notes.md` 등)와 같은 폴더다.
- 종료 코드 정책 (구현이 따를 것): 결함 1 · 2 · 4 · 5 · 6 · 7 은 준비 · 구조 실패라 2. 결함 3 은 run 단계 0 개와 「run 단계가 있지만 모두 준비 단계(SKIP)라 하나도 안 돌림」 둘 다 2 — 돌린 것이 없으면 통과가 아니다. 못 다룬 단계(UNSUPPORTED)만 있는 경우는 지금처럼 1 이다. 결함 8 은 표 · 실행 줄의 불일치라 1. 결함 9 · 10 의 훅은 설계상 늘 0 으로 끝나므로 출력(경고 · 안내 유무)으로 판정한다.
- 톤: 구현 전 `tone-kit:tone-guide` 1 단계, 완료 선언 전 5 단계를 돈다. 주석은 새 동작의 이유만, 쉬운 한국어.

## GAP 분석

| 결함 | 출처 요지 | 저장소 자리 (BASE 에서 연 줄) | BASE 재현 (`$M/repro.sh $B $BK`, 2026-09-29) | 결과 | 조건 |
| --- | --- | --- | --- | --- | --- |
| 1 | `git diff` 실패를 변경 0 으로 읽음 | `scripts/detect-docs-drift.py:238-248` `run_git` 이 실패 때 `""` · `:251` `changed_files` | `d1 bad-ref rc=0 nodrift=1` | 계약에 넣음 | 스크립트-01 · 스크립트-11 · 오류-01 |
| 2 | 깨진 `evals.json` 을 없는 파일처럼 SKIP | `scripts/sync-evals.py:50-58` 파싱 실패도 `None` · `:184-186` SKIP | `d2 broken-json rc=0` | 계약에 넣음 | 스크립트-02 · 스크립트-11 |
| 3 | 돌릴 run 단계 0 개여도 성공 | `scripts/ci-local.sh:47-48` `uses` 단계 버림 · `:96` 끝 판정 `failed=0 && unsupported=0` 뿐 | `d3 uses-only rc=0` · `d3 uses-only-list rc=0` · `d3 all-skip rc=0` | 계약에 넣음 (모두 SKIP 정책 포함) | 스크립트-03 · 스크립트-11 · 오류-01 |
| 4 | 추적 파일 읽기 실패를 버림 | `scripts/check-install-docs-guidance.py:84-87` `except (OSError, UnicodeDecodeError): continue` | `d4 unreadable rc=0 msg=0` | 계약에 넣음 | 스크립트-04 · 스크립트-11 · 오류-01 |
| 5 | `fm_get` 실패를 OK 로 | `harness/scripts/check-superseded.sh:24` · `:29` — 못 읽는 새 판은 `OK`, 못 읽는 계약은 대상에서 빠짐. `fm_get` 자체는 못 읽으면 2 를 돌려준다 (실측) | `d5 target-unreadable rc=0 ok=1` · `d5 contract-unreadable rc=0 ok=0` | 계약에 넣음 | 스크립트-05 · 스크립트-11 · 오류-01 |
| 6 | 빈 eval 목록 PASS | `scripts/run-evals.py:150-153` WARN 뒤 `(0, 0)` | `d6 empty-list rc=0` · `d6 no-key rc=0` | 계약에 넣음 | 스크립트-06 · 스크립트-11 |
| 7 | HTML 0 개면 `0/0 PASS` | `scripts/check-docs-a11y.js:40-47` `walk('docs')` · `:162-163` | `d7 no-html rc=0 pass_line=1` | 계약에 넣음 | 스크립트-07 · 스크립트-11 · 오류-01 |
| 8 | 같은 시험 파일 표 행 중복 시 첫 행만 | `bambu-kit/evals/run-gate-fixtures.sh:52-53` `sort -u` · `:60` `head -1` | `d8 dup-row rc=0 dup=0` · `d8 dup-run rc=0 dup=0 last=[결과: 29 경우 중 불일치 0]` | 계약에 넣음 | 스크립트-08 · 스크립트-11 |
| 9 | 한 백틱 안 grep 명령 전체를 건너뜀 | `~/.claude/hooks/lint-contract-oracle.sh:84` `if (is_command(t)) continue` | C · en_US.UTF-8 모두 `in-span-en` · `in-span-ko` · `in-span-rg` `found=[]` | 계약에 넣음 (CI 등록은 못 함 — 범위 경계) | 스크립트-09 · 스크립트-12 · 구조-03 |
| 10 | 0 바이트 QA 결과를 완료로 봄 | `~/.claude/hooks/qa-pending-check.sh:82-91` 빈 판정은 `REJECT\|BLOCKED` 가 아니라 넘어감 | `d10 empty pending=0` · `d10 no-verdict pending=0` | 계약에 넣음 (CI 등록은 못 함 — 범위 경계) | 스크립트-10 · 스크립트-12 · 구조-03 |
| 소비처 | 종료 코드 값이 바뀌는 도구의 설명 · 종료 코드 표 | `harness/evals/gate-exit-codes.md:71` `check-docs-a11y.js` 행 `0 · 1` · 각 도구 머리 설명 | 표 행 옛 값 1 · 새 값 0 | 계약에 넣음 | 오류-01 |

- 대응 페이지: 바꾸는 원본 문서는 `harness/evals/gate-exit-codes.md` 하나다. `scripts/detect-docs-drift.py` 매핑에 이 파일의 짝이 없고 `docs/` 에 이 표를 옮긴 쪽도 없다 (`git grep -l 'check-reviewer-protocol-copies.py' -- docs` 가 `docs/harness/qa-evaluation-guide.html` 하나이고, 그 쪽은 평가 가이드를 옮긴 것이다). 그래서 페이지 변경은 없다.

## 범위 경계

- 하지 않는 것: `scripts/check-api-kit-docs.py` · `scripts/check-docs-common-css.py` · `docs/` 아래 전부 — 다른 묶음(tail)이 고치는 중이다. `.github/workflows/ci.yml` 은 줄을 더하기만 한다.
- 하지 않는 것: `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일. `harness/references/contract-schema.md` 의 `fm_get` (못 읽으면 이미 2 를 돌려준다 — 고칠 곳은 부르는 쪽이다).
- 하지 않는 것: Codex 목록 밖의 같은 모양 결함 — `scripts/run-evals.py` 가 없는 킷 이름을 받으면 `SKIP` 으로 0, `evals.json` 이 없는 킷을 이름으로 받아도 0, `sync-evals.py` · `run-evals.py` 가 `OSError` 를 잡지 않는 것. 보고 때 남은 일로 적는다.
- 못 함: 훅 시험 둘(`harness/evals/hooks/lint-contract-oracle-test.sh` · `harness/evals/hooks/qa-pending-check-test.sh`)의 CI 등록. 훅이 레포 밖(`~/.claude/hooks/`)이라 CI 러너에 없다 — 등록하면 매번 준비 실패 2 로 떨어진다. 대신 스크립트-12 가 이 맥에서 두 로캘로 돌린다.
- 이어받는 전제: 스크립트-14 (b) 의 옛 로컬 CI 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 git 이 추적하지 않는 파일이다 (`remaining.md` D2). 이 계약이 새로 만든 의존이 아니라 앞 묶음들의 관행을 그대로 잇는다. 그 파일을 옮기거나 추적시키는 일은 이 계약 밖이다.
- 판 번호 올리기 · 릴리스 · 변경 기록은 하지 않는다. 합친 뒤 main 에서 한다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>`, 한 커밋에 맨 위 폴더 하나(`scripts` · `harness` · `bambu-kit` · `.github` 따로), 메시지 한국어, 끝에 빈 줄 뒤 서명 줄. `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 시험 파일이 `chmod 000` 으로 못 읽는 파일을 만든다(결함 4 · 5). root 로 돌면 읽혀 버리므로 CI 러너(비 root 사용자)와 이 맥에서만 뜻이 있다.
- 봉인 전 조건 충돌 확인 (2026-09-29):
  - 바뀌는 파일을 읽는 기존 검사 — `scripts/ci-local.sh` 는 `.github/workflows/ci.yml` 을 읽고 `scripts/test-ci-local.sh` 가 `ci-local.sh` 를 잰다. `test-ci-local.sh` 의 `워크플로열쇠` 경우(단계 모두 UNSUPPORTED)는 `rc=1` 을 기대한다 — 새 정책이 UNSUPPORTED 만 있는 경우를 1 로 두므로 부딪히지 않는다. `harness/evals/superseded/check-superseded-test.sh` 와 CI 단계 `bash harness/scripts/check-superseded.sh .harness` 는 레포 `.harness/` 전체를 재는데, 못 읽는 계약이 0 개라 새 판에서도 0 이다(`find .harness -maxdepth 1 -name 'sprint-contract-*.md' ! -perm -u=r` 0 줄).
  - `python3 scripts/run-evals.py --verbose` (CI) — BASE 에서 `WARN` 0 줄이라 빈 목록을 2 로 바꿔도 CI 가 깨지지 않는다. `python3 scripts/sync-evals.py --check-only` (CI) — BASE rc 0, 깨진 JSON 0.
  - `bambu-kit/evals/run-gate-fixtures.sh` 를 실제 SKILL.md 에 돌릴 때 표 행 중복 0 · 실행 줄 중복 0 (`sort | uniq -d` 두 번 모두 빈 출력) — 중복을 불일치로 바꿔도 CI 가 깨지지 않는다.
  - `node scripts/check-docs-a11y.js` (CI) 는 `docs/` 에 HTML 이 있어 0 개 분기에 들지 않는다.
  - 「더하라」 조건(스크립트-13 이 `ci.yml` 에 단계를 더함)과 「그대로」 조건(스크립트-14 전체 CI)이 겹치는 파일은 `.github/workflows/ci.yml` 하나 — 더한 단계에 `name` · `run` 밖 열쇠가 있으면 `ci-local.sh` 가 `UNSUPPORTED` 로 세어 스크립트-14 가 깨진다. 스크립트-14 가 `unsupported=0` 을 잰다. 단계 수는 늘어나므로 스크립트-14 는 `steps=` · `run=` 값을 잠그지 않는다.
  - `harness/evals/gate-exit-codes.md` 를 인용하는 다른 검사(`scripts/`·`.github/`)는 없다 — 인용 줄을 가진 스크립트들은 설명만 한다.
- 오라클 해소: 스크립트-01 ~ 10 — `repro.sh` 가 도구 · 훅을 실제로 돌려 종료 코드와 출력으로 판정한다. 산문 grep 이 아니다. 오류-01 — 산출물이 도구 설명 글 자체라 그 글을 찾는 것이 결과 관찰이다.
- 오라클 해소: 스크립트-01 · 스크립트-08 · 스크립트-09 · 구조-02 — 검출기가 짚은 한글은 `repro.sh` 출력 줄(`결과: 28 경우 중 불일치 0` · `산문-grep`)과 `<scratch 새 폴더>` 자리표시다. 문서를 찾는 것이 아니라 실행 출력을 대조한다.
- 커버리지 해소: 구조-02 — 측정 줄의 awk 안 ```` ``` ```` 세 백틱이 검출기의 백틱 짝을 어긋나게 해 `측정 대상:` 줄의 세 경로를 못 읽는다. `.harness/` 는 측정이 일부러 빼는 경로, `CF=…` 는 측정 변수 정의라 대상이 아니다.
- 범위 목록 (이 밖의 경로를 담은 커밋은 막힌다):

```text
# sprint-scope
scripts/detect-docs-drift.py
scripts/test-detect-docs-drift.py
scripts/sync-evals.py
scripts/test-sync-evals.py
scripts/ci-local.sh
scripts/test-ci-local.sh
scripts/check-install-docs-guidance.py
scripts/test-check-install-docs-guidance.py
scripts/run-evals.py
scripts/test-run-evals.py
scripts/check-docs-a11y.js
scripts/test-check-docs-a11y.sh
harness/scripts/check-superseded.sh
harness/evals/superseded/check-superseded-test.sh
harness/evals/gate-exit-codes.md
harness/evals/hooks/lint-contract-oracle-test.sh
harness/evals/hooks/qa-pending-check-test.sh
bambu-kit/evals/run-gate-fixtures.sh
bambu-kit/evals/run-gate-fixtures-test.sh
.github/workflows/ci.yml
```

## 회귀 게이트

- BASE 재현 전체 (2026-09-29, `TMPDIR=<scratch> NODE_MODULES=$PWD/node_modules bash $M/repro.sh $B $BK`, 42 줄, 출력 sha256 앞 16 자리 `067f4f10420e2686` — 두 번 돌려 같았다):
  `d1 bad-ref rc=0 nodrift=1 msg=1` · `d1 good rc=0 nodrift=1` · `d2 broken-json rc=0 msg=1` · `d2 good rc=0` · `d3 uses-only rc=0` · `d3 uses-only-list rc=0` · `d3 all-skip rc=0` · `d3 good rc=0` · `d4 unreadable rc=0 msg=0` · `d4 good rc=0` · `d5 target-unreadable rc=0 ok=1 unreadable=0` · `d5 contract-unreadable rc=0 ok=0 unreadable=0` · `d5 good rc=0 ok=1 unreadable=0` · `d6 empty-list rc=0 msg=0` · `d6 no-key rc=0 msg=0` · `d6 good rc=0` · `d7 no-html rc=0 pass_line=1` · `d7 good rc=0 last=[1/1 PASS]` · `d8 inserted row=2 run=2` · `d8 dup-row rc=0 dup=0 last=[결과: 28 경우 중 불일치 0]` · `d8 dup-run rc=0 dup=0 last=[결과: 29 경우 중 불일치 0]` · `d8 good rc=0 dup=0 last=[결과: 28 경우 중 불일치 0]` · d9 두 로캘 모두 `in-span-en` · `in-span-ko` · `in-span-rg` · `ascii-pattern` · `korean-path` 가 `found=[]`, `split-span-en` 이 `found=[SK-03 (산문-grep)]`, `split-span-ko` 가 `found=[스킬-03 (산문-grep)]` · `d10 empty rc=0 pending=0` · `d10 no-verdict rc=0 pending=0` · `d10 approve rc=0 pending=0` · `d10 approve-old rc=0 pending=1` · `d10 reject rc=0 pending=1` · `d10 none rc=0 pending=1`.
- 측정 알려진 답: `d10 reject` · `d10 none` · `d10 approve-old` 의 `pending=1` 과 `d9 split-span-*` 의 `found=[…]` 가 세는 명령이 1 이상을 낸다는 것을 보인다. `d8` 의 `dup=` 세기는 `불일치 process-bambu-only-key-in-orca.json — 표 행 중복 2 줄` 을 내는 가짜 러너에서 `dup=1` (2026-09-29 실측). `notes-check.sh` 는 한 줄 바꾼 lint 훅 · 한 줄 더한 qa 훅 사본과 그 둘 중 lint 두 줄만 적은 notes 로 `hook=lint-contract-oracle.sh diff_lines=2 missing=0` · `hook=qa-pending-check.sh diff_lines=1 missing=1` · `last_in_notes=1` · `last_in_notes=0` 을 냈고, zsh · bash 출력 md5 가 같았다.
- 기존 시험 BASE 값: `python3 scripts/test-detect-docs-drift.py` 끝 줄 `경우 3 개 중 통과 3` rc 0 · `bash scripts/test-ci-local.sh` `^PASS ` 6 줄 rc 0 · `bash harness/evals/superseded/check-superseded-test.sh` `^PASS ` 3 줄 rc 0.
- 전체 CI (BASE, 2026-09-29): `bash scripts/ci-local.sh $PWD` 끝 줄 `steps=45 run=40 skip=5 unsupported=0 failed=0` · 종료 코드 0, `^PASS ` 40 줄 — CI 에만 있는 check-api-kit-docs · detect-docs-drift --check-table · check-cause-table-copies · measure-helpers-test · bambu 시험 둘 · Playwright 두 단계 · 접근성 단계가 이 안에서 `PASS` 로 나왔다. 옛 도구 `summary.txt` 26 줄 가운데 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나. `bash .harness/.meta/after-0929-final-sweep-rules/bambu-nosl.sh $PWD` 첫 두 줄 `here 결과: 28 경우 중 불일치 0 rc=0` · `noslicer 결과: 28 경우 중 불일치 0 · 건너뜀 20 rc=0 left_paths=0`.
- 진단 BASE: `shellcheck scripts/ci-local.sh scripts/test-ci-local.sh harness/scripts/check-superseded.sh harness/evals/superseded/check-superseded-test.sh bambu-kit/evals/run-gate-fixtures.sh ~/.claude/hooks/lint-contract-oracle.sh ~/.claude/hooks/qa-pending-check.sh` 종료 코드 0. markdownlint-cli2 0.23.2 (`{ "config": { "MD013": false } }`) 로 `harness/evals/gate-exit-codes.md` `Summary: 0 issues in 0 files`, 나쁜 머리 줄을 붙인 사본은 경고 4 줄.

## Skill

- [ ] 스킬-00: N/A (이번 변경에 SKILL.md · 에이전트 파일이 없다 — 범위 목록 20 경로 가운데 `skills/` · `agents/` 0 개)

## Script

- [ ] 스크립트-01: 결함 1 — `scripts/detect-docs-drift.py` 가 없는 기준 판으로 불리면 「drift 없음」 대신 종료 코드 2 로 멈추고, 있는 기준 판은 그대로 「no docs drift」 로 끝난다 [exact, enumerated]
  Given: 모든 커밋 뒤, 작업 폴더가 TIP. `$M/repro.sh` 지문 `dab47b27e2cf24a7`, `$BK` 두 파일 지문이 배경 절 값과 같다.
  측정: `TMPDIR=<scratch 새 폴더> NODE_MODULES=$PWD/node_modules bash $M/repro.sh $PWD ~/.claude/hooks > <scratch>/out.txt` (이 파일이 이하 OUT). `grep -cxF '<줄>' OUT` 이 아래 줄마다 1 — `d1 bad-ref rc=2 nodrift=0 msg=1` · `d1 good rc=0 nodrift=1`.
  양성 대조: 같은 명령을 `$B $BK` 로 돌린 BASE 값 `d1 bad-ref rc=0 nodrift=1 msg=1` (2026-09-29 실측).
  측정 대상: `scripts/detect-docs-drift.py` · `$M/repro.sh` (결함 1 경우 `d1`)
- [ ] 스크립트-02: 결함 2 — `scripts/sync-evals.py --check-only` 가 마켓에 등록된 킷의 깨진 `evals.json` 을 없는 파일처럼 넘기지 않고 종료 코드 2 로 끝나며, 정상 `evals.json` 은 0 이다 [exact, enumerated]
  Given: 스크립트-01 과 같다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 줄마다 1 — `d2 broken-json rc=2 msg=1` · `d2 good rc=0`.
  양성 대조: BASE `d2 broken-json rc=0 msg=1`.
  측정 대상: `scripts/sync-evals.py` · `evals.json` (결함 2 경우 `d2`)
- [ ] 스크립트-03: 결함 3 — `scripts/ci-local.sh` 가 돌릴 run 단계가 없는 CI 파일(`uses` 만 있음)과 run 단계가 모두 준비 단계(SKIP)인 CI 파일에서 실행 · `--list` 모두 종료 코드 2 로 끝나고, run 단계 하나가 도는 CI 파일은 0 이다 [exact, enumerated]
  Given: 스크립트-01 과 같다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 줄마다 1 — `d3 uses-only rc=2` · `d3 uses-only-list rc=2` · `d3 all-skip rc=2` · `d3 good rc=0`.
  양성 대조: BASE 네 줄 모두 `rc=0`.
- [ ] 스크립트-04: 결함 4 — `scripts/check-install-docs-guidance.py` 가 킷의 추적 파일을 못 읽으면 그 경로를 출력에 적고 종료 코드 2 로 끝나며, 읽히고 안내가 붙은 파일은 0 이다 [exact, enumerated]
  Given: 스크립트-01 과 같다. 비 root 사용자로 돈다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 줄마다 1 — `d4 unreadable rc=2 msg=1` · `d4 good rc=0`.
  양성 대조: BASE `d4 unreadable rc=0 msg=0`.
- [ ] 스크립트-05: 결함 5 — `harness/scripts/check-superseded.sh` 가 `superseded_by` 로 가리킨 계약을 못 읽거나 superseded 판정할 계약 자체를 못 읽으면 `OK` 대신 `UNREADABLE ` 로 시작하는 줄을 한 줄 내고 종료 코드 2 로 끝나며, 둘 다 읽히면 지금처럼 `OK` 와 0 이다 [exact, enumerated]
  Given: 스크립트-01 과 같다. 비 root 사용자로 돈다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 줄마다 1 — `d5 target-unreadable rc=2 ok=0 unreadable=1` · `d5 contract-unreadable rc=2 ok=0 unreadable=1` · `d5 good rc=0 ok=1 unreadable=0`.
  양성 대조: BASE `d5 target-unreadable rc=0 ok=1 unreadable=0` · `d5 contract-unreadable rc=0 ok=0 unreadable=0`.
- [ ] 스크립트-06: 결함 6 — `scripts/run-evals.py` 가 `{"evals":[]}` 와 알려진 목록 열쇠가 없는 `{}` 를 경고만 하고 넘기지 않고, 그 `evals.json` 경로를 출력에 적고 종료 코드 2 로 끝나며, 항목 하나가 맞는 파일은 0 이다 [exact, enumerated]
  Given: 스크립트-01 과 같다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 줄마다 1 — `d6 empty-list rc=2 msg=1` · `d6 no-key rc=2 msg=1` · `d6 good rc=0`.
  양성 대조: BASE `d6 empty-list rc=0 msg=0` · `d6 no-key rc=0 msg=0`.
  측정 대상: `scripts/run-evals.py` · `evals.json` (결함 6 경우 `d6`)
- [ ] 스크립트-07: 결함 7 — `scripts/check-docs-a11y.js` 가 `docs/` 에 HTML 이 0 개면 `0/0 PASS` 를 내지 않고 종료 코드 2 로 끝나며, HTML 하나가 있는 `docs/` 는 `1/1 PASS` 와 0 이다 [exact, enumerated]
  Given: 스크립트-01 과 같다. 이 맥에 Playwright chromium 이 깔려 있다 (`~/Library/Caches/ms-playwright/chromium-1234` 등, 2026-09-29 확인).
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 줄마다 1 — `d7 no-html rc=2 pass_line=0` · `d7 good rc=0 last=[1/1 PASS]`.
  양성 대조: BASE `d7 no-html rc=0 pass_line=1`.
  측정 대상: `scripts/check-docs-a11y.js` · `docs/` (결함 7 경우 `d7`). `~/Library/Caches/ms-playwright/chromium-1234` 는 전제라 대상이 아니다
- [ ] 스크립트-08: 결함 8 — `bambu-kit/evals/run-gate-fixtures.sh` 가 음성 대조 표에 같은 시험 파일 행이 둘이거나 실행 줄이 둘이면 그 시험 파일 이름과 「중복」 을 담은 `불일치 ` 줄을 내고 종료 코드 1 로 끝나며, 실제 SKILL.md 는 지금처럼 불일치 0 · 종료 코드 0 이다 [exact, enumerated]
  Given: 스크립트-01 과 같다. 이 맥에 Bambu Studio · OrcaSlicer 설치본이 있다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF 'd8 inserted row=2 run=2'` 이 1, `grep -cE '^d8 dup-row rc=1 dup=[1-9][0-9]* last='` 이 1, `grep -cE '^d8 dup-run rc=1 dup=[1-9][0-9]* last='` 이 1, `grep -cxF 'd8 good rc=0 dup=0 last=[결과: 28 경우 중 불일치 0]'` 이 1.
  양성 대조: BASE `d8 dup-row rc=0 dup=0 …` · `d8 dup-run rc=0 dup=0 last=[결과: 29 경우 중 불일치 0]`.
- [ ] 스크립트-09: 결함 9 — 레포 밖 훅 `~/.claude/hooks/lint-contract-oracle.sh` 가 한 백틱 안에 든 grep · rg 명령의 검색 글이 한글 산문이면 그 조건을 `산문-grep` 으로 짚고, 검색 글이 ASCII 인 명령과 경로에만 한글이 든 명령은 짚지 않으며, 영어 · 한국어 조건 번호 모두 C · en_US.UTF-8 두 로캘에서 같다 [exact, enumerated]
  Given: 스크립트-01 과 같다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 아래 14 줄마다 1 — 로캘 `C` 와 `en_US.UTF-8` 각각에 대해 `d9 <로캘> in-span-en found=[SK-01 (산문-grep)]` · `d9 <로캘> in-span-ko found=[스킬-01 (산문-grep)]` · `d9 <로캘> in-span-rg found=[스킬-02 (산문-grep)]` · `d9 <로캘> split-span-en found=[SK-03 (산문-grep)]` · `d9 <로캘> split-span-ko found=[스킬-03 (산문-grep)]` · `d9 <로캘> ascii-pattern found=[]` · `d9 <로캘> korean-path found=[]`.
  양성 대조: BASE 두 로캘 모두 `in-span-en` · `in-span-ko` · `in-span-rg` 가 `found=[]`.
  음성 대조: 명령 백틱을 건너뛰는 줄만 지운 사본(`is_command` 검사 삭제)은 `korean-path` 에서 `found=[스킬-05 (산문-grep)]` 를 내 이 조건이 FAIL 한다 — 명령 전체를 산문으로 재면 안 되고 검색 글만 재야 한다.
- [ ] 스크립트-10: 결함 10 — 레포 밖 훅 `~/.claude/hooks/qa-pending-check.sh` 가 이 세션 소유 active 계약의 QA 결과 파일이 0 바이트이거나 `Verdict:` 줄이 없으면 그 계약을 안내에 넣고, 판정이 `APPROVE` 이고 봉인 뒤 시각일 때만 완료로 본다 [exact, enumerated]
  Given: 스크립트-01 과 같다.
  측정: 스크립트-01 의 OUT 에서 `grep -cxF` 가 줄마다 1 — `d10 empty rc=0 pending=1` · `d10 no-verdict rc=0 pending=1` · `d10 approve rc=0 pending=0` · `d10 approve-old rc=0 pending=1` · `d10 reject rc=0 pending=1` · `d10 none rc=0 pending=1`.
  양성 대조: BASE `d10 empty rc=0 pending=0` · `d10 no-verdict rc=0 pending=0`.
- [ ] 스크립트-11: 레포 시험 파일 여덟이 결함 1~8 의 재현 입력을 담아 TIP 도구로 통과하고, 같은 시험을 BASE 도구로 돌리면 종료 코드 1 로 실패한다 — `scripts/test-detect-docs-drift.py` · `scripts/test-sync-evals.py` · `scripts/test-ci-local.sh` · `scripts/test-check-install-docs-guidance.py` · `harness/evals/superseded/check-superseded-test.sh` · `scripts/test-run-evals.py` · `scripts/test-check-docs-a11y.sh` · `bambu-kit/evals/run-gate-fixtures-test.sh` [exact, enumerated]
  Given: 모든 커밋 뒤. `$B` 는 배경 절대로 만든 BASE 폴더. `TMPDIR` 은 scratch 아래 새 폴더.
  측정 (TIP, 여덟 모두 종료 코드 0): `python3 scripts/test-detect-docs-drift.py` 끝 줄 `경우 4 개 중 통과 4` · `python3 scripts/test-sync-evals.py` · `bash scripts/test-ci-local.sh` 에서 `^PASS ` 9 줄 이상 · `^FAIL ` 0 줄 · `python3 scripts/test-check-install-docs-guidance.py` · `bash harness/evals/superseded/check-superseded-test.sh` 에서 `^PASS ` 5 줄 이상 · `^FAIL ` 0 줄 · `python3 scripts/test-run-evals.py` · `bash scripts/test-check-docs-a11y.sh` · `bash bambu-kit/evals/run-gate-fixtures-test.sh`.
  음성 대조 (여덟 모두 종료 코드 1): `python3 scripts/test-detect-docs-drift.py --tool $B/scripts/detect-docs-drift.py` · `python3 scripts/test-sync-evals.py --tool $B/scripts/sync-evals.py` · `CI_LOCAL=$B/scripts/ci-local.sh bash scripts/test-ci-local.sh` · `python3 scripts/test-check-install-docs-guidance.py --tool $B/scripts/check-install-docs-guidance.py` · `CHECK_SUPERSEDED=$B/harness/scripts/check-superseded.sh bash harness/evals/superseded/check-superseded-test.sh` · `python3 scripts/test-run-evals.py --tool $B/scripts/run-evals.py` · `A11Y_TOOL=$B/scripts/check-docs-a11y.js bash scripts/test-check-docs-a11y.sh` · `RUN_GATE_FIXTURES=$B/bambu-kit/evals/run-gate-fixtures.sh bash bambu-kit/evals/run-gate-fixtures-test.sh`. BASE 시험 파일 셋(detect-docs-drift · ci-local · superseded)은 BASE 도구로 종료 코드 0 이다 (2026-09-29 실측) — 새 경우가 없으면 이 대조가 통과해 버린다.
  측정 대상: `scripts/test-detect-docs-drift.py` · `scripts/test-sync-evals.py` · `scripts/test-ci-local.sh` · `scripts/test-check-install-docs-guidance.py` · `harness/evals/superseded/check-superseded-test.sh` · `scripts/test-run-evals.py` · `scripts/test-check-docs-a11y.sh` · `bambu-kit/evals/run-gate-fixtures-test.sh`
- [ ] 스크립트-12: 훅 시험 둘 `harness/evals/hooks/lint-contract-oracle-test.sh` · `harness/evals/hooks/qa-pending-check-test.sh` 가 결함 9 · 10 의 재현 입력과 정상 입력을 담아 지금 훅(`~/.claude/hooks/`)으로 통과하고, 고치기 전 사본으로 돌리면 종료 코드 1 로 실패하며, lint 시험은 C · en_US.UTF-8 두 로캘과 영어 · 한국어 조건 번호를 모두 돈다 [exact, enumerated]
  Given: 모든 커밋 뒤. 훅 경로는 환경 변수 `LINT_ORACLE_HOOK` · `QA_PENDING_HOOK` 로 바꾸고, 없으면 `~/.claude/hooks/` 의 같은 이름이다. 훅 파일이 없으면 시험은 종료 코드 2.
  측정: `bash harness/evals/hooks/lint-contract-oracle-test.sh` 종료 코드 0 · `bash harness/evals/hooks/qa-pending-check-test.sh` 종료 코드 0. `grep -c 'LC_ALL=C' harness/evals/hooks/lint-contract-oracle-test.sh` 1 이상 · `grep -c 'en_US.UTF-8' harness/evals/hooks/lint-contract-oracle-test.sh` 1 이상 · `grep -cE 'SK-[0-9]{2}' harness/evals/hooks/lint-contract-oracle-test.sh` 1 이상 · `grep -cE '스킬-[0-9]{2}' harness/evals/hooks/lint-contract-oracle-test.sh` 1 이상.
  음성 대조: `LINT_ORACLE_HOOK=$BK/lint-contract-oracle.sh bash harness/evals/hooks/lint-contract-oracle-test.sh` 종료 코드 1 · `QA_PENDING_HOOK=$BK/qa-pending-check.sh bash harness/evals/hooks/qa-pending-check-test.sh` 종료 코드 1. `LINT_ORACLE_HOOK=/nonexistent bash harness/evals/hooks/lint-contract-oracle-test.sh` 종료 코드 2.
  측정 대상: `harness/evals/hooks/lint-contract-oracle-test.sh` · `harness/evals/hooks/qa-pending-check-test.sh` · `~/.claude/hooks/`
- [ ] 스크립트-13: `.github/workflows/ci.yml` 에 새 레포 시험 다섯이 각각 새 단계(열쇠 `name` · `run` 둘뿐, run 이 그 명령 한 줄)로 더해지고 기존 셋은 그대로이며, 줄은 더하기만 했다 — 명령 `python3 scripts/test-sync-evals.py` · `python3 scripts/test-check-install-docs-guidance.py` · `python3 scripts/test-run-evals.py` · `bash scripts/test-check-docs-a11y.sh` · `bash bambu-kit/evals/run-gate-fixtures-test.sh` · `python3 scripts/test-detect-docs-drift.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/superseded/check-superseded-test.sh` [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-cx)`.
  측정: 여덟 명령 각각 `grep -cF '<명령>' .github/workflows/ci.yml` 이 1. `python3 -c "import yaml,sys;d=yaml.safe_load(open('.github/workflows/ci.yml'));steps=[s for b in d['jobs'].values() for s in b['steps']];print(' '.join(str(sum(1 for s in steps if set(s)=={'name','run'} and s['run'].strip()==c)) for c in sys.argv[1:]))" <여덟 명령을 위 차례대로 하나씩 따옴표로>` 출력이 `1 1 1 1 1 1 1 1`. `python3 -c "import yaml;d=yaml.safe_load(open('.github/workflows/ci.yml'));print([j for j,b in d['jobs'].items() for s in b['steps'] if 'test-check-docs-a11y.sh' in s.get('run','')])"` 출력이 `['playwright']`. `git diff -U0 cf51b6e1 $TIP -- .github/workflows/ci.yml | grep -cE '^-($|[^-])'` 이 0.
  양성 대조: 새 다섯 명령은 BASE 에서 각각 0 (단계 세기 BASE 값 `0 0 0 0 0 1 1 1`. 같은 세기에 인자 셋 `python3 scripts/test-detect-docs-drift.py` · `bash scripts/test-ci-local.sh` · `python3 scripts/test-sync-evals.py` 만 주면 `1 1 0` — 있는 단계는 1, 없는 단계는 0 을 낸다는 확인이다). 지운 줄 세기를 `git diff -U0 000da1ae~1 000da1ae -- .github/workflows/ci.yml` 에 돌리면 1 (2026-09-29 실측).
- [ ] 스크립트-14: 전체 CI 와 슬라이서 없는 사본이 통과한다 — (a) `scripts/ci-local.sh` 로 CI 파일 전 단계 (b) 옛 로컬 CI 도구 (c) 슬라이서 설치본 경로를 지운 SKILL.md 사본으로 bambu 완료 검사 시험 [exact, enumerated]
  Given: 모든 커밋 뒤. `TMPDIR` 은 scratch 아래 서로 다른 폴더. `npm ci` 를 한 작업 폴더.
  측정: (a) `bash scripts/ci-local.sh $PWD` 종료 코드 0, 끝 줄이 `unsupported=0 failed=0` 으로 끝나고 `run=` 값이 45 이상, 출력에 `^FAIL ` 0 줄 — CI 에만 있는 check-api-kit-docs · detect-docs-drift --check-table · check-cause-table-copies · measure-helpers-test · bambu 시험 둘 · Playwright 두 단계 · 접근성 단계가 이 안에서 `PASS` 로 나온다. (b) `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $PWD` 의 `summary.txt` 에서 `rc=0` 이 아닌 줄이 `feedback-agg-test SKIP (yq 없음)` 하나뿐. (c) `bash .harness/.meta/after-0929-final-sweep-rules/bambu-nosl.sh $PWD` 첫 줄이 `here 결과: 28 경우 중 불일치 0 rc=0`, 둘째 줄이 `noslicer 결과: 28 경우 중 불일치 0 · 건너뜀 ` 으로 시작하고 `rc=0 left_paths=0` 으로 끝난다.
  양성 대조: 회귀 게이트 절 BASE 값 (`run=40`). 새 단계 다섯이 더해지므로 `run=` 이 45 보다 작으면 등록이 빠진 것이다.

## Error

- [ ] 오류-01: 종료 코드가 바뀐 도구의 설명과 종료 코드 표가 새 값을 적는다 — `harness/evals/gate-exit-codes.md` 소비처 표 · `scripts/check-docs-a11y.js` 머리 주석 · `scripts/ci-local.sh --help` · `harness/scripts/check-superseded.sh --help` · `scripts/check-install-docs-guidance.py` 문서 문자열 · `scripts/detect-docs-drift.py` 문서 문자열 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `grep -cF '| \`scripts/check-docs-a11y.js\` | 0 · 1 · 2 |' harness/evals/gate-exit-codes.md` 1 · `grep -cF '| \`scripts/check-docs-a11y.js\` | 0 · 1 |' harness/evals/gate-exit-codes.md` 0 · `grep -E '^ \* exit 0 = ' scripts/check-docs-a11y.js | grep -c '2 ='` 1 · `bash scripts/ci-local.sh --help | grep -c '돌릴 run 단계가 0 개'` 1 이상 · `bash harness/scripts/check-superseded.sh --help | grep -c 'UNREADABLE'` 1 이상 · `grep -E '^종료 코드:' scripts/check-install-docs-guidance.py | grep -c '못 읽'` 1 · `awk '/^"""/{n++; if(n==2) exit; next} n==1' scripts/detect-docs-drift.py | grep -c 'exit 2'` 1 이상.
  양성 대조: BASE 값 차례대로 `0 · 1 · 0 · 0 · 0 · 0 · 0` (2026-09-29 실측).

  측정 대상: `harness/evals/gate-exit-codes.md` · `scripts/check-docs-a11y.js` · `scripts/ci-local.sh` · `harness/scripts/check-superseded.sh` · `scripts/check-install-docs-guidance.py` · `scripts/detect-docs-drift.py`
## Architecture

- [ ] 구조-01: BASE 뒤 가지 `chore/ak3-cx` 의 모든 커밋이 병합 커밋이 아니고, 맨 위 폴더 하나만 건드리며, 서명 줄이 `Claude … <noreply@anthropic.com>` 모양이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-cx)`.
  측정: `git rev-list --merges cf51b6e1..$TIP | grep -c .` 이 0. `for c in $(git rev-list cf51b6e1..$TIP); do n=$(git show --name-only --format='' $c | cut -d/ -f1 | LC_ALL=C sort -u | grep -c .); s=$(git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' $c | grep -cE '^Claude .+ <noreply@anthropic\.com>$'); [ "$n" = 1 ] && [ "$s" = 1 ] || echo "BAD $c n=$n s=$s"; done | grep -c BAD` 이 0. `git rev-list cf51b6e1..$TIP | grep -c .` 이 1 이상.
  양성 대조: 같은 서명 세기를 `01b1cace` 에 돌리면 0 (GitHub 병합 커밋, 서명 줄 없음), 폴더 세기를 `a5152c5` 에 돌리면 17.
- [ ] 구조-02: BASE 에서 TIP 까지 바뀐 경로(`.harness/` 제외)가 전부 `## 범위 경계` 의 `# sprint-scope` 블록 안에 있고, `scripts/check-api-kit-docs.py` · `scripts/check-docs-common-css.py` · `docs/` 는 0 경로다 [exact, enumerated]
  Given: 모든 커밋 뒤. `CF=.harness/sprint-contract-after-0929-codex-silent-pass.md`.
  측정: `comm -23 <(git diff --name-only cf51b6e1 $TIP -- . ':(exclude).harness' | LC_ALL=C sort -u) <(awk '/^# sprint-scope$/{p=1;next} p&&/^```/{p=0} p' $CF | LC_ALL=C sort -u) | grep -c .` 이 0. `git diff --name-only cf51b6e1 $TIP -- scripts/check-api-kit-docs.py scripts/check-docs-common-css.py docs | grep -c .` 이 0.
  양성 대조: 같은 `comm` 을 `git diff --name-only a5152c5~1 a5152c5` 에 돌리면 1 이상 (그 커밋은 `.harness` 밖 17 경로).
  측정 대상: `scripts/check-api-kit-docs.py` · `scripts/check-docs-common-css.py` · `docs/`
- [ ] 구조-03: notes 파일 `$N` (`.harness/.meta/after-kaizen-0928/cx-notes.md`) 에 레포 밖 훅 둘의 고친 줄 전부와 훅 시험 둘의 출력 끝 줄이 옮겨 적혀 있다 [exact, enumerated]
  Given: 모든 커밋 뒤, 훅을 고친 뒤. `$M/notes-check.sh` 지문 `c2ea108172d7be73`.
  측정: `bash $M/notes-check.sh .harness/.meta/after-kaizen-0928/cx-notes.md $BK ~/.claude/hooks $PWD` 출력 네 줄 — `hook=lint-contract-oracle.sh diff_lines=` 뒤 값 1 이상 · `missing=0`, `hook=qa-pending-check.sh diff_lines=` 뒤 값 1 이상 · `missing=0`, `test=lint-contract-oracle-test.sh rc=0 last_in_notes=1`, `test=qa-pending-check-test.sh rc=0 last_in_notes=1`.
  양성 대조: 회귀 게이트 절 알려진 답 — 한 줄만 옮긴 notes 는 `missing=1` · `last_in_notes=0`. 훅을 안 고치면 `diff_lines=0` 이라 FAIL 한다.

  측정 대상: `.harness/.meta/after-kaizen-0928/cx-notes.md` · `$M/notes-check.sh`
## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0.
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0.

## Reusability

- [ ] 재사용-01: `harness/scripts/check-superseded.sh` 는 머리말을 공용 측정 파일의 `fm_get` 으로만 읽는다 — 자기 awk 파서를 두지 않는다 [exact]
  측정: `grep -c 'awk' harness/scripts/check-superseded.sh` 이 0 (BASE 0) · `grep -c '\. "\$script_dir/measure-common.sh"' harness/scripts/check-superseded.sh` 이 1 (BASE 1).
- [ ] 재사용-02: 훅 시험 둘은 훅 도우미를 다시 정의하지 않고 실제 훅 파일을 부른다 [exact, enumerated]
  측정: `grep -cE '^(hook_field|hook_notice|hook_stop_context)\(\)' harness/evals/hooks/lint-contract-oracle-test.sh harness/evals/hooks/qa-pending-check-test.sh` 가 두 파일 모두 `:0`.

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only cf51b6e1 $(git rev-parse chore/ak3-cx) | grep -c '^scripts/release.sh$'` 이 0)
- [ ] 진단-02: 바꾸거나 만든 셸 파일 아홉과 훅 둘이 shellcheck 경고 0, 파이썬 파일 아홉이 컴파일되고, 자바스크립트 하나가 문법 검사를 통과하며, md 하나가 markdownlint 경고 0 이다 [exact, enumerated]
  Given: 모든 커밋 뒤. markdownlint-cli2 0.23.2, 설정 `{ "config": { "MD013": false } }`.
  측정: `shellcheck scripts/ci-local.sh scripts/test-ci-local.sh scripts/test-check-docs-a11y.sh harness/scripts/check-superseded.sh harness/evals/superseded/check-superseded-test.sh harness/evals/hooks/lint-contract-oracle-test.sh harness/evals/hooks/qa-pending-check-test.sh bambu-kit/evals/run-gate-fixtures.sh bambu-kit/evals/run-gate-fixtures-test.sh ~/.claude/hooks/lint-contract-oracle.sh ~/.claude/hooks/qa-pending-check.sh` 종료 코드 0. `python3 -m py_compile scripts/detect-docs-drift.py scripts/test-detect-docs-drift.py scripts/sync-evals.py scripts/test-sync-evals.py scripts/check-install-docs-guidance.py scripts/test-check-install-docs-guidance.py scripts/run-evals.py scripts/test-run-evals.py scripts/plugin_utils.py` 종료 코드 0. `node --check scripts/check-docs-a11y.js` 종료 코드 0. `markdownlint-cli2 --config <설정 파일> harness/evals/gate-exit-codes.md` 출력에 `Linting: 1 file` 과 `Summary: 0 issues in 0 files`.
  양성 대조: 회귀 게이트 절 — BASE 셸 일곱 shellcheck 종료 코드 0, 나쁜 머리 줄을 붙인 md 사본 경고 4 줄.
- [ ] 진단-03: N/A (commands.test 는 scripts/release.sh 를 돌린다 — 이번 변경과 무관. 실제 시험은 스크립트-11 · 12 · 14 가 잰다)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 도구와 훅은 스크립트-01 ~ 10 이 직접 돌려 잰다)
