---
feature: "끝 — 깨진 바로가기 · 머리말 시험 · 평가 실행기 · 평가자 머리 읽기"
slug: after-0930-end
created: "2026-09-30 12:36"
complexity: "복잡"
conditions: 22
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:d2437ae0709e3d1a
measurement_digest: sha256:1775115ab58ed74e
locked_at: "2026-09-30 14:57"
---

## 배경

- 묶음 end. 출처는 `.harness/.meta/after-kaizen-0928/cx-notes.md` 「남은 것」 · 「남은 것 (막지 않음)」 과 `.harness/.meta/after-kaizen-0928/last-notes.md` 「남긴 것」 이다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-end`, 가지 `chore/ak3-end`, 시작 판 `BASE` = `f0fcc534` (가지 `chore/after-kaizen-0928` 끝 — last · cx 가 합쳐진 판).
- 사용자가 할 일: 없음.
- 교차 진단 반영(봉인 전): 남은 일 목록은 `main 01b1cac` 기준이고 시작 판 `f0fcc534` 는 그보다 319 커밋 앞선 가지 끝이다. 목록의 B2 · B3(`superseded_by` 확인 도구 · `superseded` 로 바꾸는 절차)는 커밋 `e2ff8652` 에서 `harness/scripts/check-superseded.sh` · `harness/skills/sprint-contract/SKILL.md` 352 ~ 370 줄로 이미 들어갔고, B9(평가 실행기 손 목록)는 커밋 `dd607550` 에서 마켓 목록을 읽게 바뀌었다 — 이 계약에서 다시 다루지 않는다. `SKIP_KITS` 는 B9 와 다른 것이며 `## 범위 경계` 「하지 않는 것」 에 있다. `check-install-docs-guidance.py` · `check-docs-mermaid.js` 는 목록이 쓰인 뒤 생긴 검사라 목록에 없다.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-end` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 다시 돌린 뒤 W 맨 위 폴더에서 root 가 아닌 사용자로 잰다(권한을 빼 못 읽는 파일을 만들어야 한다). 이 가지는 이 스프린트만 커밋한다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. `TMPDIR` 는 scratch 아래 폴더로 둔다.

항목별 처리 방침 (결정):

- **(1) 깨진 바로가기** — `scripts/check-install-docs-guidance.py` 97 ~ 101 줄은 `FileNotFoundError` 하나로 「작업 폴더에서 지워짐」 을 판정한다. 추적 중인 바로가기(심볼릭 링크)가 남아 있는데 가리키는 파일만 없어도 `open` 이 같은 예외를 내므로 `SKIP … (작업 폴더에서 지워짐)` · 종료 코드 0 으로 지나간다(봉인 전 재현 — 아래 GAP). 고치는 방법은 cx 기록이 적은 그대로다: `os.path.lexists(path)` 가 참이면(바로가기가 남아 있으면) 못 읽음으로 세어 `UNREADABLE <경로> (…)` · 종료 코드 2, 거짓일 때만 SKIP. 시험 `scripts/test-check-install-docs-guidance.py` 에 대상 없는 바로가기 경우 4 를 더한다(경우 3 진짜 지운 파일은 그대로 넘긴다).
- **(2) 머리말 시험** — `scripts/check-docs-mermaid.js` 41 ~ 42 줄(이름표 없는 `<pre>` 의 `---` 머리말을 건너는 줄)을 `return lines[0] || '';` 로 되돌려도 시험 여덟 경우가 모두 통과한다(경우 6 · 7 이 이름표 길로만 세어진다). 이름표 없는 `<pre>` 에 머리말 + 정상 `flowchart LR` 만 있는 경우 9 를 `scripts/test-check-docs-mermaid.js` 에 더하고, CI 단계 이름을 「아홉 경우」 로 맞춘다. 검사 파일은 고치지 않는다.
- **(3) 평가 실행기** — `scripts/run-evals.py` 는 인자로 준 킷이 없으면 `SKIP: <킷> (디렉토리 없음)`, 평가 파일이 없으면 `SKIP (evals.json 없음)` 으로 넘겨 종료 코드 0 이다. 이름으로 준 킷은 꼭 재라는 뜻이므로 둘 다 종료 코드 2 로 바꾼다(`SKIP_KITS` 에 사유와 함께 적힌 킷 이름은 지금처럼 SKIP · 0). `scripts/run-evals.py` · `scripts/sync-evals.py` 는 `evals.json` 읽기의 `OSError`(권한 등)를 잡지 않아 추적 출력과 종료 코드 1 로 죽는다 — `UNREADABLE <경로> (<까닭>)` 줄과 종료 코드 2 로 바꾼다. 시험 `scripts/test-run-evals.py`(경우 4 · 5 · 6) · `scripts/test-sync-evals.py`(경우 3)에 경우를 더하고 CI 단계 이름에 새 경우를 적는다.
- **(4) 평가자 머리 읽기** — 이미 됨. `harness/agents/qa-evaluator.md` Step 1-b 의 `fm_get` 은 커밋 `e2ff8652` 에서 줄 끝 주석 벗기기가 들어가 `contract-schema.md` 의 `fm_get` · `commit-guard.sh` 의 `val()` 과 같다. 레포 안 머리 읽개 사본 다섯(아래 오류-01)을 `status: active   # 메모` 모양으로 돌리면 모두 `active` 를 읽는다(봉인 전 실측). last 기록이 짚은 것은 설치본 캐시(harness 0.16.0)의 옛 사본이다 — 그 사본은 `active   # 메모` 를 읽는다. 레포 파일은 고치지 않고, 사본 다섯이 같은 값을 읽는다는 것을 오류-01 로 잠근다. 설치본은 다음 harness 릴리스로 풀린다(범위 밖).

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 읽은 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `scripts/check-install-docs-guidance.py` | 88 ~ 105 줄(읽기 예외 셋) · 11 ~ 14 줄(설명) | `FileNotFoundError` 면 무조건 SKIP — 대상 없는 바로가기도 지운 파일로 친다 | 스크립트-01 · 구조-02 |
| `scripts/test-check-install-docs-guidance.py` | 5 ~ 13 줄 · 83 ~ 91 줄 | 세 경우, 바로가기 경우 없음 | 스크립트-02 |
| `scripts/check-docs-mermaid.js` | 39 ~ 43 줄 `firstLine` | 41 ~ 42 줄이 머리말 건너뛰기 — 지키는 시험 없음. 고치지 않음 | 스크립트-03 음성 대조의 원본 |
| `scripts/test-check-docs-mermaid.js` | 3 ~ 18 줄 · 43 ~ 73 줄 | 여덟 경우 모두 이름표 달린 머리말만 | 스크립트-03 |
| `scripts/run-evals.py` | 65 ~ 73 줄 `load_evals` · 146 ~ 150 줄 · 180 ~ 191 줄 · 19 ~ 22 줄(설명) | 이름으로 준 없는 킷 · 평가 파일 없는 킷 SKIP · 0, `OSError` 안 잡음 | 스크립트-04 · 05 · 구조-02 · 오류-03 |
| `scripts/sync-evals.py` | 50 ~ 59 줄 `load_evals` · 18 ~ 21 줄(설명) | `OSError` 안 잡음(`path.exists()` 뒤 `read_text`) | 스크립트-05 · 구조-02 |
| `scripts/test-run-evals.py` · `scripts/test-sync-evals.py` | 전체 | 세 경우 · 두 경우, 새 모양 없음 | 스크립트-06 |
| `.github/workflows/ci.yml` | 37 ~ 39 · 53 ~ 55 · 211 ~ 212 줄 | 단계 이름 「깨진 evals.json 은 2」 · 「빈 목록 · 목록 열쇠 없음은 2」 · 「여덟 경우」 | 스크립트-03 · 06 |
| `harness/agents/qa-evaluator.md` | 231 ~ 250 줄 `fm_get` | 줄 끝 주석 벗기기 이미 있음 | 오류-01 (고치지 않음) |
| `harness/references/contract-schema.md` · `docs/harness/contract-schema.html` · `harness/skills/sprint-contract/SKILL.md` · `harness/scripts/commit-guard.sh` | 241 ~ 259 줄 · 475 줄 부근 · 283 ~ 298 줄 `read_fm` · 227 ~ 233 줄 `val()` | 같은 벗기기 | 오류-01 (고치지 않음) |
| 소비처 `.claude/skills/tone-kaizen/SKILL.md` · `backend-kit/README.md` · `infra-kit/README.md` | 95 줄 · 56 줄 · 56 줄 | 킷 이름을 주고 `run-evals.py` 를 부름 — 셋 다 평가 파일이 있는 킷 | 오류-03 |

봉인 전 실측 (W 시작 판, 2026-09-30):

- (1) 대상 없는 바로가기가 추적된 임시 저장소에서 시작 판 검사 → `SKIP k/link.md (작업 폴더에서 지워짐)` · `TOTAL files=1 ok=1 need=0 exempt=0 unreadable=0` · 종료 코드 0.
- (2) `firstLine` 41 ~ 42 줄을 `return lines[0] || '';` 로 바꾼 사본을 `--check` 로 주면 시험 `경우 8 개 중 통과 8` · 종료 코드 0.
- (3) `python3 scripts/run-evals.py no-such-kit` → `Total: 0 passed, 0 failed` · 종료 코드 0, `python3 scripts/run-evals.py planning-kit` → 같음 · 0. 권한 0 인 `evals.json` 에 `run-evals.py` · `sync-evals.py --check-only` → 둘 다 `PermissionError` 추적 출력 · 종료 코드 1.
- (4) 사본 다섯 모두 `active|abc|x-y|a#b`, 설치본 캐시 `~/.claude/plugins/cache/joo6077-plugins/harness/0.16.0/agents/qa-evaluator.md` 의 `fm_get` 은 `active   # 메모|abc<탭># 탭 주석|x-y"  # q`.

## Script

- [ ] 스크립트-01: 설치본 안내 검사가 대상 없는 바로가기를 못 읽음으로 잡는다 — 킷 `k` 와 뿌리 `docs/foo/` 칸을 가진 임시 git 저장소 넷에서 W 의 `scripts/check-install-docs-guidance.py` 를 돌려 ① `broken-link`(추적된 `k/link.md` → 없는 `missing.md`) 종료 코드 2 · 줄 머리 `UNREADABLE k/link.md` ② `deleted`(추적된 `k/gone.md` 를 작업 폴더에서 지움) 0 · `SKIP k/gone.md` ③ `link-deleted`(추적된 바로가기 `k/link.md` 자체를 지움) 0 · `SKIP k/link.md` ④ `live-link`(`k/link.md` → 안내 붙은 `a.md`) 0 · `TOTAL files=2 ok=2` 이다. Given 공통 전제 G, When `m 스크립트-01`, Then 네 줄 `OK` · `cases=4 right=4 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` (도우미 `INSTALL_CASES` · `install_repo`). 시작 판 `BAD broken-link rc=0 want=2` · `cases=4 right=3 ok=0` · 종료 코드 1 (결함 재현). 구현 뒤 모양 사본 `cases=4 right=4 ok=1` · 0. ② ③ ④ 는 시작 판도 `OK` — 넘겨야 할 모양이 그대로인지 본다
- [ ] 스크립트-02: 설치본 안내 시험이 두 모양을 가른다 — `python3 scripts/test-check-install-docs-guidance.py` 가 끝 줄 `경우 4 개 중 통과 4` · 종료 코드 0 이고, `--tool` 로 시작 판 검사(`git show f0fcc534:scripts/check-install-docs-guidance.py`)를 주면 `FAIL 경우 4` 하나만 · 종료 코드 1, 지운 파일도 못 읽음으로 치던 판(`git show 8dca3e73^:scripts/check-install-docs-guidance.py`)을 주면 `FAIL 경우 3` 하나만 · 종료 코드 1 이다. Given 공통 전제 G, When `m 스크립트-02`, Then `test_ok=1 base_fails=4 base_ok=1 pre_fails=3 pre_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02`. 시작 판 `test_rc=0 test_tail=[경우 3 개 중 통과 3] test_ok=0 base_rc=0 base_fails= base_ok=0 pre_rc=1 pre_fails=3 pre_ok=1` · 종료 코드 1. 구현 뒤 모양 사본 `test_tail=[경우 4 개 중 통과 4] … base_rc=1 base_fails=4 … pre_rc=1 pre_fails=3` · 0
  음성 대조: 시작 판 검사는 걸려야 할 모양(경우 4)을 넘겨 실패하고, 지운 파일을 못 읽음으로 치던 판은 넘겨야 할 모양(경우 3)에서 실패한다 — 시험이 양쪽 결함을 따로 가른다
- [ ] 스크립트-03: Mermaid 시험이 머리말 건너뛰기를 지킨다 — `node scripts/test-check-docs-mermaid.js` 가 끝 줄 `경우 9 개 중 통과 9` · 종료 코드 0 이고, 시험 머리 설명(`/** … */`)에 「아홉 경우」 와 두 칸 들여 쓴 `9.` 항목이 있으며, `.github/workflows/ci.yml` 의 `playwright` 묶음 `run: node scripts/test-check-docs-mermaid.js` 단계가 정확히 1 개 · `run: npm ci` 뒤 · 이름에 「아홉 경우」 가 있다. Given 공통 전제 G, When `m 스크립트-03`, Then `test_ok=1 old_fails=9 old_ok=1 stub_ok=1 head_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03`. 시작 판 `test_rc=0 test_tail=[경우 8 개 중 통과 8] test_ok=0 old_rc=0 old_fails= old_ok=0 stub_rc=1 stub_ok=1 head_ok=0 ci_ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `test_tail=[경우 9 개 중 통과 9] … old_rc=1 old_fails=9 … head_ok=1 ci_ok=1` · 0
  음성 대조: 도우미가 W 의 `scripts/check-docs-mermaid.js` 에서 머리말 건너뛰기 두 줄(`MM_FRONT_SKIP`)을 `return lines[0] || '';` 로 바꾼 사본(한 곳이 아니면 `NOT_APPLIED` · 2)을 `--check` 로 주면 `FAIL 경우 9` 하나만 · 종료 코드 1 (`old_fails=9`). 늘 `쪽 0 · 예시 0 · 안 그려진 예시 0` 과 0 을 내는 가짜 검사는 종료 코드 1 (`stub_ok`)
- [ ] 스크립트-04: 평가 실행기가 이름으로 받은 킷을 재지 못하면 2 로 끝난다 — W 에서 `python3 scripts/run-evals.py no-such-kit`(킷 폴더 없음) · `python3 scripts/run-evals.py planning-kit`(폴더는 있고 `evals/evals.json` 없음)이 모두 종료 코드 2 이고 출력에 그 킷 이름이 있으며, `python3 scripts/run-evals.py backend-kit` 은 종료 코드 0 이다. Given 공통 전제 G, When `m 스크립트-04`, Then 세 줄 `OK` · `cases=3 right=3 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04`. 시작 판 `BAD no-such-kit rc=0` · `BAD planning-kit rc=0` · `OK backend-kit rc=0` · `cases=3 right=1 ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `right=3` · 0
- [ ] 스크립트-05: 평가 실행기 둘이 못 읽는 평가 파일을 2 로 끝낸다 — 킷 하나짜리 임시 트리(W 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py` 사본)에서 `k/evals/evals.json` 권한을 0 으로 두면 `python3 scripts/run-evals.py` 와 `python3 scripts/sync-evals.py --check-only` 가 각각 종료 코드 2 이고 `UNREADABLE` 로 시작하며 `k/evals/evals.json` 을 담은 줄을 내고, 권한을 돌리면 둘 다 0 이다. Given 공통 전제 G, When `m 스크립트-05`, Then `run_ok=1 sync_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-05` (root 로 돌면 권한을 빼도 읽혀 종료 코드 2). 시작 판 `run unreadable rc=1 line=0 good rc=0` · `sync unreadable rc=1 line=0 good rc=0` · `run_ok=0 sync_ok=0` · 종료 코드 1 (추적 출력 `PermissionError`). 구현 뒤 모양 사본 `rc=2 line=1 good rc=0` 둘 · 0
- [ ] 스크립트-06: 평가 실행기 시험이 새 모양을 실패 경우로 갖고 CI 이름이 맞다 — `python3 scripts/test-run-evals.py` 끝 줄 `경우 6 개 중 통과 6` · `python3 scripts/test-sync-evals.py` 끝 줄 `경우 3 개 중 통과 3` · 둘 다 종료 코드 0 이고, `--tool` 로 시작 판 도구(`git show f0fcc534:` 의 `scripts/run-evals.py` · `scripts/sync-evals.py` · `scripts/plugin_utils.py` 를 한 임시 폴더에)를 주면 run 시험은 `FAIL 경우 4` · `5` · `6` 만, sync 시험은 `FAIL 경우 3` 만 내고 둘 다 종료 코드 1 이다. CI 단계 `run: python3 scripts/test-run-evals.py` 이름에 `없는 킷` 과 `못 읽` 이, `run: python3 scripts/test-sync-evals.py` 이름에 `못 읽` 이 있다. Given 공통 전제 G, When `m 스크립트-06`, Then `run_ok=1 sync_ok=1 run_base_fails=4,5,6 run_base_ok=1 sync_base_fails=3 sync_base_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-06`. 시작 판 `run_tail=[경우 3 개 중 통과 3] run_ok=0 sync_tail=[경우 2 개 중 통과 2] sync_ok=0 run_base_fails= run_base_ok=0 sync_base_fails= sync_base_ok=0 ci_ok=0` · 종료 코드 1. 구현 뒤 모양 사본 모든 값 `1` · `run_base_fails=4,5,6` · `sync_base_fails=3` · 0
  음성 대조: 시작 판 도구는 새 경우(없는 킷 이름 · 평가 파일 없는 킷 이름 · 못 읽는 파일)에서만 실패하고 기존 경우 1 ~ 3 · 1 ~ 2 는 통과한다 — 시험이 고친 자리를 직접 부른다는 뜻이다

## Error

- [ ] 오류-01: 머리 읽개 사본 다섯이 줄 끝 주석을 값으로 읽지 않는다 — 머리가 `status: active   # 메모` · `owner_session: abc<탭># 탭 주석` · `slug: "x-y"  # q` · `superseded_by: a#b` 인 임시 파일을 `harness/agents/qa-evaluator.md` 의 `fm_get` · `harness/references/contract-schema.md` 의 `fm_get` · `docs/harness/contract-schema.html` 의 `fm_get`(HTML 글자 풀어서) · `harness/skills/sprint-contract/SKILL.md` 의 `read_fm` · `harness/scripts/commit-guard.sh` 의 `val()` 로 읽으면 다섯 모두 `active|abc|x-y|a#b` 이고, 레포에서 `index($0, k ":") == 1` 모양 읽개를 가진 파일(`.harness` 빼고 `git grep`)이 앞 넷과 정확히 같다. Given 공통 전제 G, When `m 오류-01`, Then 다섯 줄 `OK` · `copies=5 right=5 ok=1 mut_ok=1 grep_files=4 grep_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01`. 시작 판 `copies=5 right=5 ok=1 mut_ok=1 grep_files=4 grep_ok=1` · 종료 코드 0 (이미 됨 — 지킬 동작). 구현 뒤 모양 사본 같음 · 0
  음성 대조: 도우미가 qa-evaluator 사본에서 주석 벗기기 줄(`FM_STRIP`)을 지운 변이는 `active   # 메모|abc<탭># 탭 주석|x-y|a#b` 를 읽는다(`mut_ok=1` = 변이가 한 곳에 걸렸고 값이 틀렸다). 설치본 캐시 0.16.0 사본도 틀린 값을 읽는다(GAP 실측)
- [ ] 오류-02: 앞 묶음 cx 재현의 평가 · 안내 검사 줄이 그대로다 — `bash .harness/.meta/after-0929-codex-silent-pass/repro.sh <W> ~/.claude/hooks` 출력에서 `d2` · `d4` · `d6` 로 시작하는 줄이 차례대로 정확히 `d2 broken-json rc=2 msg=1` · `d2 good rc=0` · `d4 unreadable rc=2 msg=1` · `d4 good rc=0` · `d6 empty-list rc=2 msg=1` · `d6 no-key rc=2 msg=1` · `d6 good rc=0` 이다. Given 공통 전제 G, When `m 오류-02`, Then `lines=7 same=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02`. 시작 판 `lines=7 same=1` · 0. 구현 뒤 모양 사본 같음 · 0 (「더하라」 조건 스크립트-01 · 04 · 05 와 「그대로」 조건 오류-02 가 함께 겨누는 `scripts/check-install-docs-guidance.py` · `scripts/run-evals.py` · `scripts/sync-evals.py` 에서 부딪히지 않는다)
- [ ] 오류-03: 킷 이름을 주고 평가 실행기를 부르는 소비처가 그대로 통과한다 — `.claude/skills/tone-kaizen/SKILL.md` 95 줄 · `backend-kit/README.md` 56 줄 · `infra-kit/README.md` 56 줄이 부르는 `python3 scripts/run-evals.py tone-kit` · `python3 scripts/run-evals.py backend-kit` · `python3 scripts/run-evals.py infra-kit` 과 CI 의 인자 없는 `python3 scripts/run-evals.py` 가 모두 종료 코드 0 이다. Given 공통 전제 G, When `m 오류-03`, Then 네 줄 `OK` · `cases=4 right=4 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-03`. 시작 판 `right=4` · 0 (`Total: 4 passed` · `8 passed` · `6 passed` · `122 passed`). 구현 뒤 모양 사본 같음 · 0. 킷 이름을 주고 부르는 소비처는 `git grep -n 'run-evals.py'` 로 찾은 이 셋뿐이다(나머지는 인자 없음 · 설명 글)

## Architecture

- [ ] 구조-01: 커밋 규칙 — `f0fcc534..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(`scripts` · `.github` · `.harness` 는 서로 다른 폴더)이며, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이고, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-01`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-01` (tail `m_commits` 를 이 기준 판 · 계약으로). 시작 판 `commits=0 bad=0 scope_entries=0` · 종료 코드 1. 구현 뒤 모양 사본 `commits` 1 이상 · `bad=0` · 0
- [ ] 구조-02: 도구 설명 글이 새 종료 코드 까닭을 적는다 — `scripts/check-install-docs-guidance.py` 맨 앞 설명에 `바로가기`, `scripts/run-evals.py` 맨 앞 설명에 `없는 킷` · `평가 파일` · `못 읽`, `scripts/sync-evals.py` 맨 앞 설명에 `못 읽` 이 있다. Given 공통 전제 G, When `m 구조-02`, Then `miss=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02`. 시작 판 `miss=[check-install-docs-guidance.py:바로가기,run-evals.py:없는 킷,run-evals.py:평가 파일,run-evals.py:못 읽,sync-evals.py:못 읽] ok=0` · 종료 코드 1. 구현 뒤 모양 사본 `miss=[] ok=1` · 0
- [ ] 구조-03: 기록 — `.harness/.meta/after-kaizen-0928/end-notes.md` 에 낱말 `check-install-docs-guidance` · `lexists` · `test-check-docs-mermaid` · `머리말` · `run-evals` · `sync-evals` · `OSError` · `fm_get` · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 3 개 이상이 있다. Given 공통 전제 G, When `m 구조-03`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03`. 시작 판 파일 없음 · `keys_ok=0` · 종료 코드 1

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-end` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 새 기록 `.harness/.meta/after-kaizen-0928/end-notes.md` 에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)
- [ ] 금지-04: N/A (바뀌는 파일에 SKILL.md · agents/*.md 가 없다 — 항목 (4) 는 이미 됨이라 `harness/agents/qa-evaluator.md` 를 고치지 않는다. 측정: `git diff --name-only f0fcc534..chore/ak3-end | grep -cE '(SKILL|agents/[^/]+)\.md$'` 이 0)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 코드는 기존 검사 · 실행기 안의 예외 처리 · 판정 몇 줄과 기존 시험 파일의 경우뿐이고, 시험은 모두 CI 에 등록돼 누구나 부른다 — 스크립트-03 · 06 `ci_ok`, `run: python3 scripts/test-check-install-docs-guidance.py` 단계는 이미 있다)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 새 검사 · 새 시험 파일을 만들지 않고 기존 파일을 고친다 — `git diff --name-status f0fcc534..chore/ak3-end -- scripts .github` 에 `A` 줄 0. 못 읽음 줄 모양은 이미 쓰는 `UNREADABLE <경로> (<까닭>)` 을 따른다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only f0fcc534..chore/ak3-end | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.py` 여섯(`scripts/check-install-docs-guidance.py` · `scripts/test-check-install-docs-guidance.py` · `scripts/run-evals.py` · `scripts/test-run-evals.py` · `scripts/sync-evals.py` · `scripts/test-sync-evals.py`)은 `python3 -m py_compile` 종료 코드 0, 바뀐 `.js` 하나(`scripts/test-check-docs-mermaid.js`)는 `node --check` 종료 코드 0, 새 `.md` 하나(`.harness/.meta/after-kaizen-0928/end-notes.md`)는 markdownlint-cli2(MD013 끔) 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`
  측정: `<scratch>/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/rest/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(설정 파일 내용 `{ "config": { "MD013": false } }`, `<scratch>` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`). 시작 판 `.py` 여섯 · `.js` 하나 종료 코드 0, 구현 뒤 모양 사본 같음. 양성 대조: tail 이 봉인 전에 같은 markdownlint 명령으로 잰 `pos.md` → 경고 4
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 검사 · 실행기 스크립트 · 시험 · CI 파일 · 기록. 측정: git diff --name-only f0fcc534..HEAD -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/)' 이 0. 브라우저로 도는 시험은 스크립트-03 이 잰다)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` (TMPDIR 은 scratch 아래 새 폴더)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외)이고 `docs-a11y` 로그 끝이 `206/206 PASS`, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/test-check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-check-docs-common-css.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/test-check-cause-table-copies.py` · `python3 scripts/check-install-docs-guidance.py` · `python3 scripts/test-check-install-docs-guidance.py` · `python3 scripts/test-run-evals.py` · `python3 scripts/test-sync-evals.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `node scripts/check-docs-mermaid.js` · `node scripts/test-check-docs-mermaid.js` 의 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 `grep -c 'rc=0' <TMPDIR>/ci-local/summary.txt`. 봉인 전 시작 판 · 구현 뒤 모양 사본 값은 `## 회귀 게이트` 에 적는다

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
scripts/check-install-docs-guidance.py
scripts/test-check-install-docs-guidance.py
scripts/test-check-docs-mermaid.js
scripts/run-evals.py
scripts/test-run-evals.py
scripts/sync-evals.py
scripts/test-sync-evals.py
.github/workflows/ci.yml
```

- 하지 않는 것: `scripts/check-docs-mermaid.js` 고치기(검사 동작은 맞다 — 시험만 더한다), 레포의 머리 읽개 사본 다섯 고치기(이미 됨), 설치본 캐시 고치기 · harness 릴리스, `SKIP_KITS` 에 적힌 킷(`howto-kit`)을 이름으로 줄 때의 SKIP 바꾸기(사유가 적힌 뺀 킷이다), `evals.json` 의 UTF-8 이 아닌 바이트(추적 출력 · 종료 코드 1 로 이미 CI 를 멈춘다 — 조용한 통과가 아니다)와 `marketplace.json` 읽기 실패 처리, `backend-kit/README.md` · `infra-kit/README.md` 의 「2 = 파싱 오류」 글 고치기(그 킷 이름으로는 새 2 까닭이 생기지 않는다 — 오류-03), `harness/evals/gate-exit-codes.md` 표에 행 더하기(두 실행기는 표에 없고, 이번 변경이 새 종료 코드 값을 만들지 않는다), 킷 버전 올리기 · 릴리스 · 합치기 · push, 로컬 CI 도구 `ci-local.sh`(레포 밖) 고치기, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일 고치기.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약들은 `status: done` 이고 이 계약의 조건을 느슨하게 하지 않는다): last 계약 `스크립트-04` 측정이 적은 시험 끝 줄 `경우 8 개 중 통과 8` 과 CI 단계 이름 「여덟 경우」 는 아홉으로 는다. cx 계약 `스크립트-11` 의 BASE 도구 대조는 시험 경우가 늘어도 여전히 종료 코드 1 이다(더 엄격해지는 쪽). 두 쪽 모두 경우를 더하는 쪽이라 더 엄격하다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` · `.github/` 는 따로. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0930-end/`) · 기록 커밋은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0930-end/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). CI 단계 읽기 · 커밋 규칙은 tail 도우미 `.harness/.meta/after-0929-tail/measure.py` 를 불러 쓴다.
- `TMPDIR` 는 절대 경로로 준다. 상대 경로를 주면 node 시험의 임시 폴더가 작업 폴더 기준으로 풀려 경우 4 가 헛 실패한다(봉인 전 실측 — last 도우미를 `TMPDIR=../t6` 로 돌려 `경우 9 개 중 통과 8`).
- 봉인 전 실측(2026-09-30, W 시작 판 `f0fcc534`): 스크립트-01 ~ 06 · 구조-01 ~ 03 종료 코드 1 (결함 재현 · 산출물 없음), 오류-01 ~ 03 종료 코드 0 (지킬 동작). 값은 각 조건 측정 줄에 있다.
- 진단-05 봉인 전 실측 — 시작 판(W): ci-local 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `206/206 PASS`, CI 전용 명령 스물하나 모두 종료 코드 0 (`12/12 PASS` · `경우 10 개 중 통과 10` · `어긋남 0` · `경우 4 개 중 통과 4` · `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0` · `경우 8 개 중 통과 8` · `checked=2 violations=0 infra_errors=0` · `실패 0 건` · `TOTAL files=94 ok=73 need=0 exempt=21 unreadable=0` · `경우 3 개 중 통과 3` · `경우 3 개 중 통과 3` · `경우 2 개 중 통과 2` · `실패 0 건` 셋 · `checked=6 violations=0 unreadable=0` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `174 passed` · `쪽 3 · 예시 9 · 안 그려진 예시 0` · `경우 8 개 중 통과 8`). ci-local 끝에 적는 「이 스크립트 밖의 것」 은 `pip install pyyaml` · `test-sync-evals.py` · `test-run-evals.py` 셋 — 뒤 둘은 CI 전용 명령 목록에 넣어 따로 잰다.
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 `git clone --shared` 에 install 검사 · 시험 / Mermaid 시험 / 실행기 둘 · 시험 둘 / CI 이름 셋을 폴더별 서명 커밋 넷에 담고, 계약 · 도우미 · 기록 사본 커밋 셋, 2026-09-30): 이 계약 측정 열둘(스크립트-01 ~ 06, 오류-01 ~ 03, 구조-01 ~ 03) 모두 종료 코드 0 (구조-01 `commits=7 bad=0`). 같은 사본에서 ci-local 25 단계 `rc=0` · `docs-a11y` `206/206 PASS`, CI 전용 명령 스물하나 모두 종료 코드 0 (바뀐 끝 줄은 `경우 4 개 중 통과 4` · `경우 6 개 중 통과 6` · `경우 3 개 중 통과 3` · `경우 9 개 중 통과 9` 넷뿐), `.py` 여섯 `py_compile` · `.js` 하나 `node --check` 종료 코드 0, 기록 사본 markdownlint 경고 0 · `Linting: 1 file`, `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 재사용-02 `A` 줄 0, 금지-04 · 진단-04 세기 0.
- 교차 대조(봉인 전): 바뀌는 글자 · 파일(`check-install-docs-guidance` · `test-check-install-docs-guidance` · `test-check-docs-mermaid` · `run-evals` · `sync-evals` · `test-run-evals` · `test-sync-evals` · `여덟 경우` · `경우 8 개` · `empty list test` · `broken file test` · `디렉토리 없음` · `evals.json 없음` · `작업 폴더에서 지워짐`)을 읽는 기존 검사를 `scripts/` · `.github/` · `harness/evals/` · `harness/scripts/` · `package.json` 에서 `git grep` 으로 찾았다 — `.github/workflows/ci.yml` 뿐(100 줄 「여덟 경우」 는 공통 CSS 시험이라 그대로 둔다). 앞 묶음 측정 도우미 가운데 cx `repro.sh`(오류-02 가 그대로 잰다)와 last `measure.py 스크립트-04`(사본에서 `test_tail=[경우 9 개 중 통과 9] base_fails=5,6,7,9 ci_ok=0` · 종료 코드 1 — 경우를 늘려 일부러 바꾸는 것, `## 범위 경계`)가 이 파일들을 읽는다. 「더하라」 조건(스크립트-01 ~ 06 · 구조-02)과 「그대로」 조건(오류-02 · 오류-03 · 진단-05)이 함께 겨누는 파일은 `scripts/check-install-docs-guidance.py` · `scripts/run-evals.py` · `scripts/sync-evals.py` 이고, 위 사본에서 두 쪽이 모두 종료 코드 0 이라 부딪히지 않는다. CI 전용 단계와 범위 목록을 맞대면 범위 밖 스크립트를 고쳐야 하는 경우는 없다.
- 도우미 지문(봉인 전, `shasum -a 256 <파일> | cut -c1-16`): 이 계약 `measure.py` `df94cf7e2ab7d3c1` · tail `measure.py` `3d920fd41c46e7f6`.
- 커버리지 해소: 스크립트-01 — 네 경우의 이름 · 저장소 모양 · 기대 종료 코드 · 줄 머리는 도우미 `INSTALL_CASES` · `install_repo` 에 글자 그대로 있고 `m` 이 경우마다 한 줄을 찍는다.
- 커버리지 해소: 스크립트-03 — 되돌린 두 줄은 도우미 `MM_FRONT_SKIP` · `MM_OLD` 에 글자 그대로 있다. 경우 9 의 쪽 내용은 시험 파일의 몫이고, 도우미는 끝 줄 · 실패 경우 번호 · 머리 설명 · CI 이름으로 잰다.
- 커버리지 해소: 스크립트-05 · 스크립트-06 — 임시 트리 모양은 도우미 `evals_tree`, 시작 판 도구 세 파일은 `m_eval_tests` 에 글자 그대로 있다.
- 커버리지 해소: 오류-01 — 사본 다섯의 파일 · 모양은 도우미 `FM_COPIES`, 입력 머리와 기대 값은 `FM_TEXT` · `FM_WANT`, 변이 줄은 `FM_STRIP` 에 있다.
- 오라클 해소: 오류-01 — 글자 찾기가 아니라 다섯 사본을 파일에서 원문 그대로 뽑아 셸로 실행한 출력으로 판정한다. 음성 대조(주석 벗기기 줄을 지운 변이)가 붙어 있다.
- 오라클 해소: 오류-03 — 소비처 줄은 찾는 대상이 아니라 부를 명령의 출처다. 판정은 `run-evals.py` 를 그 킷 이름으로 실제로 부른 종료 코드다.
- 오라클 해소: 진단-02 · 진단-05 — 파일 · 명령 목록을 백틱으로 적었을 뿐, 판정은 `py_compile` · `node --check` · markdownlint · 각 명령을 실행한 종료 코드와 끝 줄이다. 진단-02 는 양성 대조(경고 4)가 있다.
- 오라클 해소: 스크립트-01 ~ 06 — 검사 · 실행기 · 시험을 실제로 돌린 종료 코드 · 출력 줄로 판정한다. 스크립트-02 · 03 · 06 은 옛 판 도구를 넣어 시험이 실패하는지 보는 음성 대조가 붙어 있다.
- 커버리지 해소: 오류-03 — 소비처 파일 셋은 부를 킷 이름의 출처를 적은 것이다. 도우미 `m_consumers` 는 그 킷 이름 셋(`tone-kit` · `backend-kit` · `infra-kit`)과 인자 없는 실행을 글자 그대로 부른다.
- 커버리지 해소: 구조-02 — 세 파일 경로와 찾을 낱말은 도우미 `m_usage` 의 `heads` · `need` 에 글자 그대로 있다.
- 커버리지 검출기(6.5 (4)) 출력 여섯 건(스크립트-01 · 05 · 06, 오류-01 · 03, 구조-02)은 모두 위 해소 줄로 처리했다 — 경로는 도우미가 상수로 들고 조건 줄의 `m <조건 번호>` 가 부른다.
