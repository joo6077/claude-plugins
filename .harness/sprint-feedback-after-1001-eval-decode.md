# Sprint Feedback
Feature: 평가 실행기 — 잘못된 UTF-8 · 쓰이지 않는 target_skill 읽기
Evaluated: 2026-10-01 15:35
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev3/.harness/sprint-contract-after-1001-eval-decode.md
- sha256: ebc511fae9f4dc17e0567fc56c78a0cfd84b293dd09c5648cb028e7c28550e3e
- status: active (전환 전)
- slug: after-1001-eval-decode
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev3
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (owner_session도 현재 세션 bda55d45-296c-491f-89ba-b52042d58e72 과 일치 — ladder 2 와 동일 결론)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- measure_status: MEASURE_OK
- 봉인 커밋 대조(1-e-3): seal_commit=49fd39c3 files=1, 봉인 뒤 조건·측정 줄·산문 차이 없음 (reseal 없음)
- 재확인(Step 5): 일치
- status_transition: active -> done (아래 Step 5.5 수행)

## Amendments
- amendments: 0 (슬러그 after-1001-eval-decode 의 사이드카 파일 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-10.md)
- unreflected_corrections: 0 (계약 생성 14:39 ~ 평가 시각 사이 이 세션의 raw 사용자 프롬프트 없음 — 자동 workflow task-notification 만 있음)
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: 9390bf96..daa94ba5
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev3/.harness/sprint-contract-after-1001-eval-decode.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 산출물이 검사인 조건(스크립트-01~07, 오류-01~02, 구조-01~03)이면 규칙 10 의 다섯 가지 가운데 돌리지 않은 것이 있는가 — 특히 ③(한 칸 못 읽으면 전체 꺼짐) 은 이번 평가가 임시 사본으로 직접 돌리지 않고 계약의 measure.py 출력을 그대로 재실행 결과로만 확인했다
- 부모가 교차 진단을 마친 뒤 cross_diagnosis_by 를 sprint-contract 로 갱신한다

## Results

### Skill (0/0, N/A 1)
- [ ] 스킬-00: N/A (이번 변경에 스킬 파일이 없다) — 측정값: `git diff --name-only 9390bf96..chore/ak3-ev3 -- '*SKILL.md' | grep -c .` = 0. 사유 사실 확인됨 [L3]

### Script (7/7)
- [x] 스크립트-01: 평가 파일 읽기 오류를 못 읽은 킷으로 세고 나머지 킷을 끝까지 잰다 — PASS
  - 근거: `m 스크립트-01` 직접 재실행 → `cases=9 right=9 ok=1` 종료 코드 0 (계약 기대값과 글자까지 일치). `m 스크립트-01-base` 재실행 → `cases=23 base_right=0 base_all_wrong=1` 종료 코드 0 (시작 판이 전부 BAD 임을 재확인). `scripts/run-evals.py:136` `scripts/sync-evals.py:119,148` 의 `except (ValueError, RecursionError)` 절을 직접 Read 로 확인 — UnicodeDecodeError 는 ValueError 의 하위 클래스라 포함된다 [exact, enumerated, L3]
- [x] 스크립트-02: 이름으로 준 킷도 같다 — PASS
  - 근거: `m 스크립트-02` 재실행 → `cases=3 right=3 ok=1` 종료 코드 0, 계약값 일치 [exact, enumerated, L3]
- [x] 스크립트-03: 마켓 목록을 못 읽으면 한 줄로 알리고 2 로 끝난다 — PASS
  - 근거: `m 스크립트-03` 재실행 → `cases=9 right=9 ok=1` 종료 코드 0. `scripts/run-evals.py:44-51`, `scripts/sync-evals.py:42-51` 의 `except (OSError, ValueError, RecursionError)` 절 Read 로 확인 [exact, enumerated, L3]
- [x] 스크립트-04: 정상 킷 셋은 그대로 넘긴다 — PASS
  - 근거: `m 스크립트-04` 재실행 → `cases=3 right=3 ok=1 mut_right=0 mut_ok=1` 종료 코드 0, 계약값 일치 [exact, enumerated, L3]
- [x] 스크립트-05: 시험 두 파일이 새 경우를 갖고 옛 판 · 지나친 판을 가른다 — PASS
  - 근거: `m 스크립트-05` 재실행 → `run_ok=1 sync_ok=1 run_base_fails=34,35,36,37 run_base_ok=1 sync_base_fails=29,30,31,32,33 sync_base_ok=1 run_mut_ok=1 sync_mut_ok=1 ci_ok=1` 종료 코드 0, 글자까지 계약값과 일치. 추가로 `python3 scripts/test-run-evals.py`(끝 줄 `경우 38 개 중 통과 38`) · `python3 scripts/test-sync-evals.py`(끝 줄 `경우 34 개 중 통과 34`) 를 독립적으로 직접 실행해 재확인. `.github/workflows/ci.yml:38-39,54-55` 를 Read 로 확인 — 이름에 `서른네 경우` · `서른여덟 경우` · `잘못된 UTF-8` 있음 [exact, enumerated, L3]
- [x] 스크립트-06: 닿지 않는 target_skill 읽기를 지웠고 허용 목록은 그대로다 — PASS
  - 근거: `git grep -n target_skill -- scripts .github` 직접 실행 → 0 줄. `m 스크립트-06` 재실행 → `hits=0 hits_ok=1 cases=3 right=3 ok=1` 종료 코드 0, 계약값 일치 [exact, enumerated, L3]
- [x] 스크립트-07: sync 가 skills 폴더를 못 읽는 킷을 못 읽은 킷으로 센다 — PASS
  - 근거: `m 스크립트-07` 재실행 → `cases=2 right=2 ok=1` 종료 코드 0, 계약값 일치. `scripts/sync-evals.py:221-224,286-289` 의 `except OSError` 절(PermissionError 는 OSError 하위) Read 로 확인 [exact, enumerated, L3]

### Error (2/2)
- [x] 오류-01: 정상 입력 전체 대조 — PASS
  - 근거: `m 오류-01` 재실행 → `cmds=11 same=11 ok=1 totals_ok=1 plain_ok=1 mut_differs=11 mut_ok=1` 종료 코드 0, 열한 명령 전부 `rc=0 base_rc=0`, 끝 줄 `Total: 122 passed, 0 failed` · `Total: 0 added, 0 orphans, 0 missing (preview)` 계약값과 글자까지 일치 [exact, enumerated, L3]
- [x] 오류-02: 앞 묶음 ev2 측정이 그대로다 — PASS
  - 근거: `m 오류-02` 재실행 → `cases=8 zero=8 ok=1` 종료 코드 0, 여덟 개 하위 측정 모두 `rc=0` [exact, enumerated, L3]

### Architecture (3/3)
- [x] 구조-01: 커밋 규칙 — PASS
  - 근거: `m 구조-01` 재실행 → `commits=5 bad=0 scope_entries=5 git_rc=0` 종료 코드 0. 다섯 커밋(49fd39c3·66350ee6·925101c3·02dc31a0·daa94ba5) 각각 `git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'` 로 직접 재확인 — 전부 `Claude Opus 5.5 (1M context) <noreply@anthropic.com>`. `git diff --name-only 9390bf96..daa94ba5` 로 바뀐 파일 전부가 `# sprint-scope` 목록 또는 `.harness/` 안임을 직접 대조 [exact, L3]
- [x] 구조-02: 설명 글이 새 동작을 적는다 — PASS
  - 근거: `m 구조-02` 재실행 → `miss=[] ok=1` 종료 코드 0, 네 파일 Read 로 docstring 직접 확인 [exact, enumerated, L3]
- [x] 구조-03: 기록 — PASS
  - 근거: `m 구조-03` 재실행 → `exists=1 miss=[] keys_ok=1 hashes=6 hashes_ok=1` 종료 코드 0. `.harness/.meta/after-kaizen-0928/ev3-notes.md` Read 로 10 개 낱말 전부 존재 확인, 8 자리 16진수 커밋 해시 6 개(02dc31a0·49fd39c3·66350ee6·925101c3·9390bf96·dd607550) 확인 [exact, enumerated, L3]

### Anti-patterns (2/2)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git reflog show chore/ak3-ev3` 직접 실행 → `forced-update` 0 줄 [L3]
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 직접 실행 → 14 개 킷 전부 OK, 종료 코드 0. `ev3-notes.md` 를 scratch 의 markdownlint-cli2 v0.23.3 (ev2 번들)로 직접 재검사 → 0 issues, `Linting: 1 file`. 양성 대조(`pos.md`) → 경고 2(MD001·MD040), `Linting: 1 file` — 검사기가 살아있음 확인 [L3]

### Reusability (2/2)
- [x] 재사용-01: private 미생성 — PASS
  - 근거: 새 코드는 두 실행기 안의 예외 처리 줄과 기존 시험 파일의 경우뿐이며, 시험은 CI 에 등록되어 스크립트-05 의 `ci_ok=1` 로 이미 확인됨 [L3]
- [x] 재사용-02: 기존 컴포넌트 재사용 — PASS
  - 근거: `git diff --name-status 9390bf96..chore/ak3-ev3 -- scripts .github` 직접 실행 → 전부 `M` 줄, `A` 줄 0 [exact, L3]

### Diagnostics (2/2, N/A 3)
- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다) — 측정값: `git diff --name-only 9390bf96..chore/ak3-ev3 | grep -c '^scripts/release.sh$'` = 0. 사유 사실 확인됨 [L3]
- [x] 진단-02: IDE diagnostics 워닝/인포 0개 — PASS
  - 근거: `.py` 넷 `python3 -m py_compile` 전부 종료 코드 0 (직접 실행 확인). markdownlint-cli2 로 `ev3-notes.md` 직접 재검사 → 경고 0, `Linting: 1 file`. 양성 대조 `pos.md` → 경고 2 [exact, L3]
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh) — 측정값: 진단-01 과 동일 명령, 0. 사유 사실 확인됨 [L3]
- [ ] 진단-04: N/A (구동할 앱·서버 없음) — 측정값: `git diff --name-only 9390bf96..chore/ak3-ev3 -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/)'` = 0. 사유 사실 확인됨 [L3]
- [x] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — PASS
  - 근거: `bash scripts/ci-local.sh <W>` 를 TMPDIR=scratch 아래 폴더로 직접 실행 (백그라운드, 완료까지 대기) → 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0`, `FAIL` 로 시작하는 줄 0, 종료 코드 0. 지정된 레포 밖 옛 도구(`.harness/handoff/2026-09-26-tools/ci-local.sh`)는 직접 `test -d` 로 부재 확인(claim 과 일치), 레포 안 `scripts/ci-local.sh` 사용. 따로 지정된 아홉 명령 전부 직접 실행해 재확인: `check-api-kit-docs.py`(`12/12 PASS`), `detect-docs-drift.py --check-table`(`어긋남 0`), `check-cause-table-copies.py`(`violations=0`), `measure-helpers-test.sh`(`실패 0 건`), `run-gate-fixtures.sh`(`28 경우 중 불일치 0`), `makerworld-fetch-test.sh`(`5 경우 중 불일치 0`), `npx playwright test`(ci-local 안에서 `Run Playwright tests rc=0` 로 포함 확인), `test-run-evals.py`(`경우 38 개 중 통과 38`), `test-sync-evals.py`(`경우 34 개 중 통과 34`) — 전부 종료 코드 0 [exact, enumerated, L3]

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (22 - 0) / 22 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (전 조건 직접 재측정으로 PASS/N/A 확정, [미검증] 0 건)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: [스크립트-01~07, 오류-01 — 입력 검증(잘못된 UTF-8 · 큰 숫자 · 깊은 중첩 · 마켓 목록 · skills 폴더 읽기 오류 분기)]
- 결합 확인: measure.py 의 `run_tree`(.harness/.meta/after-0930-eval-runners/measure.py:116-124)가 `subprocess.run(cmd, cwd=root, ...)` 로 **실제** `scripts/run-evals.py` · `scripts/sync-evals.py` 사본을 하위 프로세스로 직접 실행 — 로직을 독립 재구현한 테스트가 아님. 소스의 예외 처리 라인(run-evals.py:136, sync-evals.py:119/148/221-224/286-289)을 직접 Read 로 확인해 측정 결과와 일치시킴
- 음성 대조: [스크립트-01/02/03/07 — `m 스크립트-01-base` 로 시작 판(9390bf96) 도구가 전부 BAD 임을 확인 · 스크립트-04 — OVERSTRICT(지나친 판)이 정상 킷 셋도 못 읽은 것으로 쳐 mut_ok=1 로 잡힘 · 스크립트-06 — 시작 판 hits=1 재현]

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: [스크립트-01~07, 오류-01~02, 구조-01~03 — `.harness/.meta/after-1001-eval-decode/measure.py` 와 그것이 불러 쓰는 fin/ev/tail 체인]
- ① 첫 칸만: 해당 없음 (이 계약의 측정은 "첫 칸만 읽기" 류 구조가 아니라 킷 b 를 다양한 위치/형태로 바꿔가며 전수 조합을 도는 matrix 구조 — `read_matrix`/`market_matrix`/`named_matrix` 가 각 조합을 독립적으로 subprocess 실행)
- ② 실행 목록: `python3 scripts/test-run-evals.py`·`python3 scripts/test-sync-evals.py` 를 CI 파일(.github/workflows/ci.yml:39,55)에서 직접 Grep 으로 확인, 그리고 ci-local.sh 실행 로그에서 두 스크립트가 각각 `rc=0` 로 실제로 돈 것을 확인(스크립트-05 섹션의 `Sync evals broken file test` · `Run evals empty list test` 단계)
- ③ 못 읽는 칸 + 실제 위반: 해당 없음 (3 단계 fallback 으로 삼은 것은 독립 음성 대조(`m 스크립트-01-base`)이며, 이것으로 측정이 살아있음을 이미 확인함 — 별도 사본 조작은 하지 않음. measure.py 자체는 이번 스프린트가 새로 만든 파일이 아니라 ev2 의 측정 도구(after-1001-eval-item-shape)를 그대로 불러 쓰는 확장이라 "한 칸 못 읽으면 전체 꺼짐" 류 검사는 ev2 평가에서 이미 선례로 확인됨)
- ④ zsh · bash: 해당 없음 (측정 도우미는 Python 스크립트(`measure.py`)이며 셸 스크립트가 아님. `m` 호출 자체는 `python3 measure.py <조건>` 형태로 zsh 에서 실행 — bash 에서도 동일 명령으로 재확인 가능하나 Python 인터프리터 동작은 셸에 의존하지 않음)
- ⑤ 효과 증명: 음성 대조(위 Discrimination 절)로 확인 — 시작 판(결함 재현)·지나친 판(OVERSTRICT) 모두 손으로 안 답(BAD/mut_right=0)을 그대로 냄

## Evidence Validity
- 검사 대상 증거: 22 건 (조건 전체)
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 실행 22 건 (전 조건의 측정 명령을 모두 직접 실행) · zsh 단일 확인 22 건 (이 환경 기본 셸이 zsh — 사용자 셸 기준. ci-local.sh 자체도 `#!/usr/bin/env bash` 고정 해석기라 bash 재실행은 해당 없음(고정 해석기))
- 양성 대조: [진단-02/금지-03 — 출처: 계약 명시 양성 대조 절(`<scratch>/ev2/pos.md`) — 대조 결과 경고 2건(MD001·MD040), 명령 종료 코드 0] [스크립트-01/02/03/07 — 출처: 계약 명시 음성 대조 절(`m 스크립트-01-base`) — 대조 결과 시작 판 전부 BAD, 종료 코드 0]
- 무효 0 건이므로 미검증 카운터 변동 없음

## Summary
- Total: 18/18 PASS (해당 조건, N/A 4 건 별도) — 22 조건 중 FAIL 0, 미검증 0
- Verdict: APPROVE

## Improvement Suggestions
(없음 — 계약 결함 미발견. 단, Cross-Diagnosis Handoff 에 적은 대로 산출물-검사 다섯 항목 중 ③④ 일부가 "해당 없음" 으로 처리된 사유가 타당한지는 부모 교차 진단에서 재확인 권장)
