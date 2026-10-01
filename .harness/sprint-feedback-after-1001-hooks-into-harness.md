# Sprint Feedback
Feature: 레포 밖 훅 둘을 harness 플러그인 훅으로 — 원본 하나
Evaluated: 2026-10-01 14:27
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-hk/.harness/sprint-contract-after-1001-hooks-into-harness.md
- sha256: b54469adaea53ad69745d21275d20397e76e052f1e016866ab46da6b34f5ad38
- status: active
- slug: after-1001-hooks-into-harness
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-hk
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (부모가 명시 경로로 지정. owner_session이 현재 세션과 같아 ladder 2 세션소유와도 일치)
- legacy_contract_used: false
- seal_status: SEAL_ABSENT (frontmatter에 conditions_digest 없음 — v5.3 이전 양식. 경고이지 실패 아님)
- contract_seal_broken: n/a
- measure_status: MEASURE_ABSENT (measurement_digest 필드 없음 — v5.6 이전 양식. 경고이지 실패 아님)
- 봉인 커밋 대조: seal_commit=1c905f28(파일 1개), `git diff 1c905f28 -- <계약>` 빈 출력 — 봉인 뒤 계약 본문 변경 0
- 재확인(Step 5): 일치 (저장 직전 재계산 sha256 동일, status 동일)
- status_transition: active -> done (APPROVE이므로 전환)

## Amendments
- amendments: 0 (사이드카 .harness/sprint-amendments-after-1001-hooks-into-harness.md 없음)

## User Correction Audit
- correction_log_status: available (/Users/jackson/.claude/logs/claude-plugins/2026-10.md)
- unreflected_corrections: 0
- 참고(판정 비영향 — 표면화만): 계약 13번째 줄이 근거로 든 "사용자 결정(2026-10-01)"은 `.harness/.meta/after-kaizen-0928/decisions.md`에 기록돼 있지 않다(1회차 QA가 이미 지적). 그런데 프롬프트 로그에서 독립 확인한 결과, 같은 세션(`bda55d45-…`)에서 2026-10-01T12:34:52+0900에 사용자가 이번 하네스 요청 원문("막지않는 약점 해결해 오르카 작업은 뭔데? / 앞으로 주의할 점은 … 중복되는거 아님?")을 보냈고, 2026-10-01T13:32:22+0900(= UTC 04:32, hk-notes.md 5번째 줄이 인용한 시각과 일치)에 같은 세션에서 "ㄱㄱ"로 승인했다. 계약 봉인 커밋(1c905f28)은 그 뒤인 13:54:02에 생성됐다 — 순서가 맞다. 즉 decisions.md에는 안 적혀 있지만 prompt-log 앵커(발언 원문 · 시각 · 세션 · cwd)로 봤을 때 이 hk 묶음을 진행하라는 사용자 동의 자체는 실재한다. decisions.md 미기재는 계약 범위 밖 사안이라 조건 판정에 영향 없음.

## Deletions
- deletions_range: b33ed94a..chore/ak3-hk
- 커밋 구간 삭제: 5 — harness/evals/hooks/_lib-hook-payload.sh · harness/evals/hooks/lint-contract-oracle.sh · harness/evals/hooks/qa-pending-check.sh · scripts/check-user-hook-copies.py · scripts/test-check-user-hook-copies.py (전부 계약 선언 안 — 범위 목록 17개에 모두 포함. 앞 셋은 harness/scripts/로 이동(R09x, --no-renames 기준으로는 D+A), 뒤 둘은 처리방침(4)이 명시한 "옛 맞대기 검사 자리를 바꿔 쓴다"는 의도적 삭제)
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-hk/.harness/sprint-contract-after-1001-hooks-into-harness.md` · 이 판정 결과 전문(아래 Results 포함)
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건(오류-02·구조-05·금지-02·진단-01·진단-03) 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 산출물이 검사인 조건(스크립트-01·02·03·05·06, 구조-02)은 아래 Check Artifacts에서 음성 대조·효과 증명을 직접 돌려 확인했다 — 그래도 놓친 지점이 있는지 봐달라.
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다. 끝내 띄우지 못했으면 `none` 으로 내리고 사유를 `cross_diagnosis_notes` 에 적는다

## 평가 전제

1회차 QA(REJECT)는 "구현이 전혀 없다"는 사실관계로 멈췄다(`git diff --name-only b33ed94a..chore/ak3-hk` 빈 출력). 이번 2회차 시점에는 봉인 커밋 1개 · 구현 커밋 7개 · 기록 커밋 1개(총 9개, `b33ed94a..chore/ak3-hk`)가 들어가 있고, 범위 목록 17경로가 모두 변경돼 있었다. 아래는 그 구현에 대한 전수 재측정 결과다 — 구현자가 보고한 값을 그대로 믿지 않고, 공통 전제(G: 작업 폴더 클린·`npm ci`)를 다시 맞춘 뒤 26개 조건의 측정 도우미(`python3 .harness/.meta/after-1001-hooks/measure.py <조건 번호>`)를 평가자가 전부 직접 재실행했다. 1회차에서 `[미검증:INVALID]`로 깎였던 스크립트-04·진단-04(실제 claude -p 중첩 실행)도 이번에는 평가자가 직접 돌려 종료 코드와 출력을 확보했다.

## Results

### Script (9/9)
- [x] 스크립트-01: hooks.json 두 등록 — PASS
  - 근거: `m 스크립트-01` 실측 `new_found=2 base_kept=1 base_regs=5 regs=7 personal=same ok=1` · 종료 코드 0. `harness/hooks/hooks.json`을 직접 Read해 PostToolUse(Edit\|Write)·Stop 두 등록과 기존 다섯 등록의 차례가 그대로임을 확인(L3)
- [x] 스크립트-02: 플러그인 훅 시험 — PASS
  - 근거: `m 스크립트-02` 실측 `runs=2 pass=2 base_rc=1 noquote_rc=1 homelib_rc=1 ok=1` · 종료 코드 0. LC_ALL=C·en_US.UTF-8 둘 다 "실패 0 건", 음성 대조(시작판 harness/·따옴표 뺀 등록·홈 도우미 되돌림) 셋 다 rc=1로 실패를 잡음
- [x] 스크립트-03: 훅 시험 둘이 새 자리로 — PASS
  - 근거: `m 스크립트-03` 실측 `runs=4 pass=4 stub_rcs=1,1 lib_exports=0 ok=1` · 종료 코드 0. 대역 훅(exit 0만)을 주면 두 시험 모두 실패(stub_rcs=1,1)해 시험이 실제로 훅 출력을 잰다는 것을 확인
- [x] 스크립트-04: 실제 claude 구동 — PASS
  - 근거: `m 스크립트-04`를 평가자가 직접 실행 — `plugin_ok=1 lint=1 stop=1 errors=0 base_lint=0 base_stop=0 ok=1` · 종료 코드 0. `claude -p --setting-sources project --plugin-dir <W>/harness ...` 실행에서 plugins=['<W>/harness'], PostToolUse 응답에 계약 오라클 경고(lint=1), Stop 응답에 "QA 가 끝나지 않았습니다"(stop=1) 확인. 시작 판 harness/ 사본으로 같은 실행을 하면 두 훅이 안 돎(base_lint=0 base_stop=0) — 음성 대조 통과
- [x] 스크립트-05: 겹침 검사 — PASS
  - 근거: `m 스크립트-05` 실측 `none_ok=1 known=[...Stop:qa-pending-check.sh, ...PostToolUse:lint-contract-oracle.sh] got=[같음] home_rc=1 home_ok=1 cleaned_ok=1 broken_ok=1 ok=1` · 종료 코드 0. 도우미가 독립적으로 읽어낸 "알려진 답"과 겹침 검사 출력이 차례까지 같음을 직접 비교
- [x] 스크립트-06: 겹침 시험이 대역을 잡는다 — PASS
  - 근거: `m 스크립트-06` 실측 `tail=[경우 7 개 중 통과 7] stub_fails=3,4,5,6,7 stub_rc=1 ok=1` · 종료 코드 0
- [x] 스크립트-07: CI 옛 두 단계 → 새 셋 — PASS
  - 근거: `m 스크립트-07` 실측 `base_runs=56 runs=57 new_once=1 old_gone=1 kept=1 ok=1` · 종료 코드 0. `.github/workflows/ci.yml`을 직접 Read해 새 세 단계(plugin-hooks-test.sh·test-check-user-hook-overlap.py·check-user-hook-overlap.py)가 각 1개, 옛 두 단계(check-user-hook-copies 계열)가 0개임을 확인(L3)
- [x] 스크립트-08: 리눅스 도커 구동 — PASS
  - 근거: `m 스크립트-08`을 평가자가 직접 실행(도커 `ubuntu:24.04`, 읽기 전용 마운트, 비루트 사용자, jq·zsh·python3 설치) — `results=5 good=5 mawk=1 gnu_grep=1 ok=1` · 종료 코드 0. 다섯 산출물 모두 `실패 0 건`/`경우 7 개 중 통과 7`/`개인 설정 없음 — 건너뜀`의 기대 끝 줄과 일치
- [x] 스크립트-09: README 훅 목록 — PASS
  - 근거: `m 스크립트-09` 실측 `synced=1 rows=7 rows_ok=1 prose_miss=[] mdl=0 pos_md056=1 ok=1` · 종료 코드 0. `python3 scripts/sync-docs.py --check-only` 직접 실행해 "모든 README가 동기화 상태입니다." 확인. 양성 대조(막대 되돌린 README 사본)에서 markdownlint가 MD056을 1건 이상 잡음을 평가자가 직접 재현(§Evidence Validity 참조)

### Error (2/2)
- [x] 오류-01: 두 훅은 실패해도 막지 않는다 — PASS
  - 근거: `m 오류-01` 실측 — 여덟 줄 모두 `OK`(nolib·empty·broken·live 경우 × 두 훅), `cases=8 right=8 ok=1` · 종료 코드 0. 음성 대조(도우미 없을 때도 늘 출력 없이 조용)가 ④ live 경우(도우미 있으면 context 포함)와 대비됨을 확인
- [x] 오류-02: 기존 플러그인 훅은 그대로다 — PASS
  - 근거: `git diff --name-only b33ed94a..chore/ak3-hk -- harness/scripts/env-check.sh harness/scripts/sdk-guard.sh harness/scripts/run-guard.sh harness/scripts/commit-guard.sh` 직접 실행 결과 빈 출력(변경 없음). `bash harness/evals/hooks/commit-guard-test.sh` 직접 실행 — 종료 코드 0 · 끝 줄 "실패 0 건". `m 오류-02` 실측 `same=1 commit_guard_rc=0 tail=[실패 0 건] ok=1` · 종료 코드 0과 일치

### Skill (N/A 1)
- [ ] 스킬-00: N/A — `git diff --name-only b33ed94a..chore/ak3-hk -- '*SKILL.md' 'harness/agents' '.claude/skills' | grep -c .` 평가자가 직접 실행 → 0. 사유 사실 확인(L3)

### Architecture (5/5)
- [x] 구조-01: 커밋 규칙 — PASS
  - 근거: `m 구조-01` 실측 — 커밋 9개 전부 `OK`(합침 아님·맨 위 폴더 1개·서명 "Claude Opus 5.5 (1M context) <noreply@anthropic.com>" ·범위 안), `commits=9 bad=0 scope_entries=17 git_rc=0` · 종료 코드 0. `git log -1 <커밋> --format=%B`로 67ef1cdb·1c905f28 서명 줄을 직접 재확인(L3)
- [x] 구조-02: 바뀐 파일 열일곱 · 훅 한 벌 — PASS
  - 근거: `m 구조-02` 실측 `files=17 extra=[] lack=[] copies=['harness/scripts/_lib-hook-payload.sh', 'harness/scripts/lint-contract-oracle.sh', 'harness/scripts/qa-pending-check.sh'] ok=1` · 종료 코드 0
- [x] 구조-03: 옮긴 세 파일은 필요한 줄만 — PASS
  - 근거: `m 구조-03` 실측 — 세 파일 모두 `OK`(지운/더한 줄 수 정확히 일치, removed_ok=1, 주석 아닌 줄의 `.claude/hooks` 0건, exec=1), `files=3 right=3 v8_rc=0 ok=1` · 종료 코드 0. `python3 scripts/validate-plugin.py harness --check=hook-exec` 포함된 V8 결과도 rc=0
- [x] 구조-04: 기록 — PASS
  - 근거: `m 구조-04` 실측 `keys_ok=1 miss=[] branch_hashes=8 ok=1` · 종료 코드 0. `.harness/.meta/after-kaizen-0928/hk-notes.md` 46줄을 Read로 직접 확인 — 낱말 11종(minor·0.18.0·settings.json·_lib-hook-payload.sh·block-dirwide-autofixer.sh·CLAUDE.md·check-user-hook-overlap·--plugin-dir·도커·tone-guide·남긴 것) 전부 존재(L3)
- [x] 구조-05: 판 번호 불변 — PASS
  - 근거: `git diff --name-only b33ed94a..chore/ak3-hk -- harness/.claude-plugin .claude-plugin` 직접 실행 → 빈 출력. `version_files_changed=[] ok=1` · 종료 코드 0

### Anti-patterns (2/2)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git ls-remote origin chore/ak3-hk | grep -c .` 평가자가 직접 실행 → 0 (이 가지는 원격에 없음 — push 된 적 없음)
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 직접 실행 → "Total: 14 plugins, 14 OK" · 종료 코드 0. `harness/README.md`·`.harness/.meta/after-kaizen-0928/hk-notes.md` 각각 markdownlint-cli2(MD013 끔)로 직접 실행 → 둘 다 "Linting: 1 file"·"Summary: 0 issues"

### Reusability (2/2)
- [x] 재사용-01: 공용 자리 — PASS
  - 근거: 스크립트-01 `new_found=2`·스크립트-07 `new_once=1`이 조건이 지정한 측정 그대로 PASS — 두 훅·도우미가 `harness/scripts/`에 있어 설치한 누구나 돌고, 새 시험·검사가 CI에 등록돼 누구나 부름
- [x] 재사용-02: 기존 컴포넌트 재사용(도우미 단일화) — PASS
  - 근거: `m 재사용-02` 실측 `libs=['harness/scripts/_lib-hook-payload.sh'] lib_users=2 new_dirs=[] ok=1` · 종료 코드 0. 도우미가 `.harness/` 밖에 정확히 1개이고 두 훅 모두 그것을 기본으로 부름(LIB_DEFAULT_NEW), 새 폴더 0개

### Diagnostics (3/5, N/A 2)
- [ ] 진단-01: N/A — `git diff --name-only b33ed94a..chore/ak3-hk | grep -c '^scripts/release.sh$'` 평가자가 직접 실행 → 0. 사유 사실 확인(L3)
- [x] 진단-02: IDE 진단 0건 — PASS
  - 근거: `.py` 3개(check-user-hook-overlap.py·test-check-user-hook-overlap.py·sync-docs.py) `python3 -m py_compile` 모두 rc=0. `.sh` 6개(옮긴 세 파일·훅 시험 둘·plugin-hooks-test.sh) `bash -n` 모두 rc=0 · `shellcheck -f gcc | grep -c .` 모두 0. `.json` 1개(hooks.json) `jq empty` rc=0. `.md` 2개(README·hk-notes.md) markdownlint-cli2(MD013 끔) 0건·"Linting: 1 file". 양성 대조 둘 다 직접 재현 — `printf 'x=$1\necho $x\n' | shellcheck -s bash -f gcc -` → 1건, 스크립트-09의 막대 되돌린 README 사본 → MD056 1건("Table column count Expected: 3; Actual: 4")
- [ ] 진단-03: N/A — 진단-01과 같은 측정, 평가자가 직접 실행 → 0. 사유 사실 확인(L3)
- [x] 진단-04: 실제 claude 구동 훅 오류 0 — PASS [직접 실행 · 서술 아님]
  - 근거: `m 진단-04`를 평가자가 직접 실행 — `E2E branch rc=0 result=success wrote=1 plugins=['<W>/harness'] hooks=4 lint=1 stop=1 errors=0` / `errors=0 ok=1` · 종료 코드 0. 1회차에서 `[미검증:INVALID]`로 깎였던 조건을 이번에는 서술이 아니라 실제 중첩 claude -p 실행으로 직접 확보
- [x] 진단-05: 로컬 CI 와 CI 전용 단계 — PASS
  - 근거: `bash scripts/ci-local.sh <W>` 평가자가 직접 실행(TMPDIR=scratch 하위, W 맨 위 폴더) — 끝 줄 `steps=57 run=52 skip=5 unsupported=0 failed=1` · `FAIL`로 시작하는 줄은 정확히 1개("User hook overlap check (개인 설정과 harness 플러그인 훅)" — 이 맥 개인 settings.json이 아직 두 훅을 등록해 둔 상태를 그대로 알리는 것, 계약이 F=1로 예정한 값과 일치). 열 개 개별 명령(check-api-kit-docs.py·detect-docs-drift.py --check-table·check-cause-table-copies.py·measure-helpers-test.sh·bambu-kit 2종·npx playwright test·check-install-docs-guidance.py·plugin-hooks-test.sh·test-check-user-hook-overlap.py) 전부 평가자가 개별 실행 — 모두 종료 코드 0

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (23 - 0) / 23 = 1.00  (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (전수 직접 실행 — [미검증] 0건)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션 안전성·재시도/중복제거·보안 경계·사용자 결함 보고 충돌 — 9항 어디에도 해당하는 조건이 이 계약에 없음)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: scripts/check-user-hook-overlap.py(스크립트-05·진단-05) · scripts/test-check-user-hook-overlap.py(스크립트-06) · harness/evals/hooks/plugin-hooks-test.sh(스크립트-02·04) · harness/scripts/{lint-contract-oracle.sh,qa-pending-check.sh}(오류-01·스크립트-01~04)
- ① 첫 칸만 읽기: 해당 없음(사유: 다중 칸 표 구조가 아니라 "설정 파일 × 이벤트 × 훅 이름" 목록 비교 — 스크립트-05에서 독립 재계산한 known 목록과 겹침 검사의 got 목록이 2개 항목(Stop·PostToolUse) 모두 차례까지 일치함을 직접 확인해 첫 항목만 읽는 결함이 없음을 간접 확인)
- ② 표에만 올린 시험: `python3 scripts/test-check-user-hook-overlap.py`를 평가자가 직접 실행 → rc=0, 이 파일이 `.github/workflows/ci.yml`에 정확히 1회 등장(스크립트-07 new_once=1)하고 `bash scripts/ci-local.sh`의 PASS 목록에 "harness User hook overlap check test" 로 실제로 돈 로그가 남음 — 표에만 올리고 안 돈 것이 아님
- ③ 못 읽는 칸 + 실제 위반: 스크립트-05 조건 ④(깨진 settings.json)에서 `UNREADABLE <경로> (<까닭>)` · 종료 코드 2를 직접 확인(broken_ok=1). 스크립트-06 경우 6(깨진 JSON)도 통과 목록에 포함(경우 7개 중 통과 7)
- ④ zsh·bash: 해당 없음(고정 해석기 — 계약이 모든 훅 시험을 `bash <스크립트>`로 명시 호출. LC_ALL=C·en_US.UTF-8 두 로캘로는 스크립트-02·03에서 직접 실행해 동일 결과 확인함)
- ⑤ 효과 증명: 스크립트-02 음성 대조 셋(시작 판 harness/·따옴표 뺀 등록·홈 도우미 되돌림) 모두 rc=1로 직접 재현. 스크립트-03 대역 훅(exit 0만)에서 두 시험 모두 실패(stub_rcs=1,1) 직접 재현. 스크립트-06 대역 겹침 검사(늘 "개인 설정 없음" 한 줄)에서 경우 3~5~7이 FAIL(stub_fails=3,4,5,6,7) 직접 재현. 오류-01 음성 대조(도우미 부재 시 늘 조용 vs 도우미 있을 때만 context)도 여덟 경우 전부 직접 확인

## User-Reported Failures
- 해당 없음 (REOPENED 대상 없음 — 1회차는 REJECT였고 이번이 그 이후 첫 재평가)

## Evidence Validity
- 검사 대상 증거: 23 건 (N/A 3건 제외)
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 해당 없음(이 계약에 문서 셸 스니펫 지시 조건 없음 — 모든 측정은 `m <조건 번호>` 단일 도우미 또는 git/jq/py_compile/shellcheck/markdownlint 직접 명령)
- 양성 대조: [진단-02 — `printf 'x=$1\necho $x\n' | shellcheck -s bash -f gcc -` 직접 실행 → 1건(검사 생존 확인)] [스크립트-09·진단-02 — 막대 되돌린 README 사본 markdownlint 직접 실행 → MD056 "Expected: 3; Actual: 4" 1건(검사 생존 확인)]
- 무효 0 건 (현재 누계: 0)

## Summary
- Total: 23/23 conditions passed (N/A 3건 별도 — 스킬-00·진단-01·진단-03)
- Verdict: APPROVE
- 참고(판정 비영향): hk-notes.md가 인용한 사용자 동의 시각(04:32 UTC/13:32 KST "ㄱㄱ")은 `decisions.md`에는 없지만 prompt-log에서 동일 세션으로 독립 확인됨(위 User Correction Audit 참조). decisions.md 미기재 자체는 이 계약의 26개 조건 중 어느 것도 측정하지 않으므로 verdict에 영향 없음 — 부모가 후속 조치(결정 기록 보완 여부)를 판단할 사안으로 표면화만 한다.

## Improvement Suggestions
- [해당 없음] 계약 설계는 1회차 때와 동일하게 [exact, enumerated]로 구체적이고 측정·음성 대조·커버리지 해소가 갖춰져 있다. 2회차에서 1회차의 invalid_evidence(진단-04 미실행)도 평가자 직접 실행으로 해소됐다.
