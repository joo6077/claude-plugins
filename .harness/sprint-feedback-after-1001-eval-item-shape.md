# Sprint Feedback
Feature: 평가 실행기 — 목록 항목 모양이 깨진 평가 파일 (ev2)
Evaluated: 2026-10-01 14:03
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev2/.harness/sprint-contract-after-1001-eval-item-shape.md
- sha256: d36bec4ec99eaca248c6f3fff9a7eb38b220f73644e1abfaff8dc8e76f83264a
- status: active
- slug: after-1001-eval-item-shape
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev2
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- measure_status: MEASURE_OK
- 봉인 커밋: c2892771 (계약 파일 하나만, 산문·지문 차이 없음)
- 재확인(Step 5): 일치
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 파일 없음)

## User Correction Audit
- correction_log_status: available (/Users/jackson/.claude/logs/claude-plugins/2026-10.md)
- unreflected_corrections: 0
  - 12:34:52 프롬프트(「오르카 작업은 뭔데」·「주의할 점 중복」)는 이 스프린트 조건에 대한 수정 지시가 아니라 배경 질문이었고, 기록 `ev2-notes.md` 「남은 것」에 "교차 진단이 계약 지적 없이 사용자 질문에 답했다"고 투명하게 남아 있다. 13:32:22 「ㄱㄱ」로 진행 승인. 교정 누락 없음
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: b33ed94a..HEAD
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev2/.harness/sprint-contract-after-1001-eval-item-shape.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가?
- 참고: 이 작업의 1 회차 교차 진단(구현 단계)은 계약을 점검하지 않고 같이 넘어온 사용자 질문(오르카 작업 · 주의할 점 중복)에 답하고 끝났다 — 계약 지적 0 건. 이번 평가자 교차 진단은 별도로 수행 필요
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다

## Results

### Skill (0/0, N/A 1)
- [N/A] 스킬-00: 이번 변경에 스킬 파일 없음 — 측정: `git diff --name-only b33ed94a..HEAD -- '*SKILL.md' | grep -c .` = 0
  - 근거: L3, 직접 실행 확인

### Script (6/6)
- [x] 스크립트-01: 깨진 모양 아홉을 구조 오류로 보고하고 나머지 킷을 끝까지 잰다 — PASS
  - 근거: `m 스크립트-01` → `cases=27 right=27 ok=1` · 종료 코드 0 (직접 실행, L3). 음성 대조 `m 스크립트-01-base` → `cases=87 base_right=0 base_all_wrong=1` · 종료 코드 0 (시작 판 전부 BAD 확인)
- [x] 스크립트-02: 정상 모양은 그대로 넘긴다 — PASS
  - 근거: `m 스크립트-02` → `cases=9 right=9 ok=1 mut_right=0 mut_ok=1` · 종료 코드 0. 지나친 판 아홉 경우 전부 BAD(rc=2) 확인(로그 `/tmp/out_스크립트-02.log`)
- [x] 스크립트-03: 이름으로 준 킷도 같다 — PASS
  - 근거: `m 스크립트-03` → `cases=9 right=9 ok=1` · 종료 코드 0
- [x] 스크립트-04: 시험 두 파일이 새 경우를 갖고 옛 판·지나친 판을 가른다 — PASS
  - 근거: `m 스크립트-04` → `run_mut_fails=3,9,15,16,17,18,27,29,30,31,32,33 sync_mut_fails=2,6,12,13,14,22,24,25,26,27,28` 와 모든 `_ok=1` · 종료 코드 0 (계약 명시값과 글자까지 일치). CI 파일에서 "스물여덟 경우" "서른세 경우" "항목 모양" 글자 직접 확인(`.github/workflows/ci.yml:38,54`). `python3 scripts/test-run-evals.py` 끝 줄 `경우 33 개 중 통과 33` · `python3 scripts/test-sync-evals.py` 끝 줄 `경우 28 개 중 통과 28` 직접 실행 확인
- [x] 스크립트-05: 허용 목록이 레포가 쓰는 모양과 같다 — PASS
  - 근거: `m 스크립트-05` → `census_ok=1 cases=51 right=51 ok=1` · 종료 코드 0
- [x] 오류-01: 정상 입력 전체 대조 — PASS
  - 근거: `m 오류-01` → `cmds=11 same=11 ok=1 totals_ok=1 plain_ok=1 mut_differs=11 mut_ok=1` · 종료 코드 0. `Total: 122 passed, 0 failed` · `Total: 0 added, 0 orphans, 0 missing (preview)` 직접 확인
- [x] 오류-02: 앞 묶음 평가 실행기 측정이 그대로다 — PASS
  - 근거: `m 오류-02` → `cases=10 zero=10 ok=1` · 종료 코드 0

### Architecture (3/3)
- [x] 구조-01: 커밋 규칙 — PASS
  - 근거: `m 구조-01` → `commits=5 bad=0 scope_entries=6 git_rc=0` · 종료 코드 0. `git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'` 5 개 커밋 모두 직접 확인(패턴 일치), 각 커밋 맨 위 폴더 단일(`scripts`/`.github`/`.harness` 분리), 합침 커밋 없음
- [x] 구조-02: 설명 글이 새 동작을 적는다 — PASS
  - 근거: `m 구조-02` → `miss=[] ok=1` · 종료 코드 0. 네 파일 docstring 을 Read 로 직접 확인 — `run-evals.py:23`·`sync-evals.py:22` "항목 모양"·"허용 목록", `test-run-evals.py:22-23` "21 ~ 29."·"30."·"31 ~ 33.", `test-sync-evals.py:16-18` "16 ~ 24."·"25."·"26 ~ 28." 전부 존재
- [x] 구조-03: 기록 — PASS
  - 근거: `m 구조-03` → `exists=1 miss=[] keys_ok=1 hashes=5 hashes_ok=1` · 종료 코드 0. 낱말 8종 전부 1회 이상(직접 grep), 서로 다른 8자리 16진수 5개(`7ff2158e`·`9e1aeaee`·`b33ed94a`·`c2892771`·`ec444174`) 확인

### Anti-patterns (2/2)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git reflog show chore/ak3-ev2 | grep -c forced-update` = 0
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` → `Total: 14 plugins, 14 OK` · 종료 코드 0. `ev2-notes.md` markdownlint MD040 0건(아래 진단-02 측정과 동일 명령 재사용, 양성 대조로 검사기 생존 확인)

### Reusability (2/2)
- [x] 재사용-01: 사용 가능 컴포넌트를 private으로 만들지 않음 — PASS
  - 근거: 새 코드는 두 실행기 내부 모양 검사 몇 줄과 기존 시험 파일 경우뿐. CI 등록 확인 — `m 스크립트-04` `ci_ok=1`
- [x] 재사용-02: 기존 컴포넌트 재사용 — PASS
  - 근거: `git diff --name-status b33ed94a..HEAD -- scripts .github` 전부 `M`, `A` 줄 0건 직접 확인

### Diagnostics (2/2, N/A 3)
- [N/A] 진단-01: commands.analyze(`scripts/release.sh`)와 변경 파일 교집합 0 — 측정 직접 실행 0
- [x] 진단-02: IDE 워닝/인포 0개 — PASS
  - 근거: 바뀐 `.py` 4개 `python3 -m py_compile` 전부 종료 코드 0(직접 실행). `ev2-notes.md` markdownlint-cli2 v0.23.3(`<scratch>/ev2/mdl`) 실행 → `Summary: 0 issues in 0 files` · `Linting: 1 file` · MD 매치 0건. 양성 대조 `pos.md` → `Summary: 2 issues in 1 file`(MD001·MD040) 직접 실행해 검사기 생존 확인
- [N/A] 진단-03: commands.test 대상도 동일 — 측정 직접 실행 0
- [N/A] 진단-04: 구동할 앱·서버 없음 — 측정 직접 실행 0
- [x] 진단-05: 로컬 CI 와 CI 전용 단계 모두 통과 — PASS
  - 근거: `bash scripts/ci-local.sh <W>` 직접 실행 → 끝 줄 `steps=56 run=51 skip=5 unsupported=0 failed=0` · `FAIL` 줄 0 · 종료 코드 0. 레포 밖 옛 도구 폴더 부재 직접 확인. 따로 돌린 9개 전부 직접 실행 확인: `check-api-kit-docs.py`(`12/12 PASS`·0) · `detect-docs-drift.py --check-table`(`어긋남 0`·0) · `check-cause-table-copies.py`(`checked=2 violations=0`·0) · `measure-helpers-test.sh`(`실패 0 건`·0) · `run-gate-fixtures.sh`(`28 경우 중 불일치 0`·0) · `makerworld-fetch-test.sh`(`5 경우 중 불일치 0`·0) · `npx playwright test`(`174 passed`·0) · `test-run-evals.py`(`경우 33 개 중 통과 33`·0) · `test-sync-evals.py`(`경우 28 개 중 통과 28`·0)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (20 - 0) / 20 = 1.00 (임계 0.60)
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 이번 조건 20개 중 동시성 가드·인증/권한·멱등성(여러 번 보내도 결과가 같은 성질)·입력 검증·데이터 유실·마이그레이션 안전성·재시도/중복제거·보안 경계·사용자 결함 보고 충돌 어디에도 해당하지 않는다(모양 검사기 로직 변경)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: 스크립트-01~05, 오류-01~02 — `scripts/run-evals.py` · `scripts/sync-evals.py`(검사 로직 자체가 산출물)
- ① 첫 칸만: 해당 없음 — 평가 파일은 킷마다 1개뿐이라 "칸" 개념이 아니라 "킷" 단위. 대신 깨진 모양을 가운데 킷(b)에 두고 양옆(a·c)이 끝까지 재지는지 매 조건에서 직접 확인함(요약 줄 `못 읽은 킷 1 개: b`)
- ② 실행 목록: `python3 scripts/test-run-evals.py`·`test-sync-evals.py` 가 CI 파일(`.github/workflows/ci.yml:39,55`)에 등록되어 실제로 돎을 직접 Grep·실행 확인(경우 33/28 전부 통과)
- ③ 못 읽는 칸 + 실제 위반: 킷 셋 트리에서 b 를 깨진 모양 아홉 각각으로 두고 a·c는 정상으로 둔 사본을 `m 스크립트-01`이 자동 구성해 돌림 — b만 못 읽은 킷으로 잡히고 a·c는 쟀음을 직접 확인(27줄 전부)
- ④ zsh·bash: 해당 없음(고정 해석기) — 측정은 `python3`으로 돌리는 셸 무관 스크립트이고, `#!/usr/bin/env python3` 고정. 단, `m` 호출 자체는 bash로 실행했고 결과는 기존 zsh 세션(개발 시점)과 동일함이 `구조-03`의 지문 기록으로 교차 확인됨
- ⑤ 효과 증명: `스크립트-01-base`(시작 판 도구로 깨진 모양 아홉+경계 모양 열일곱 재실행) → `cases=87 base_right=0 base_all_wrong=1`(결함이 실제로 있었음을 재현). 지나친 판(STRICT) 음성 대조 → 정상 모양 9개 전부 거부(rc=2)됨을 `스크립트-02`에서 직접 확인

## User-Reported Failures
- 없음 (이번 회차는 1회차 QA이며 선행 사용자 결함 보고 없음)

## Evidence Validity
- 검사 대상 증거: 20건 (조건 17건 실측 + N/A 3건 측정 확인)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 전부 실제 실행(해당 조건에 셸 스니펫 문서화 요구 없음 — 실행기 자체가 산출물이므로 직접 실행으로 대체)
- 양성 대조: [진단-02 — 출처: 계약 절(`pos.md`) — 대조 결과 2건(MD001·MD040)·종료 코드 0] / [금지-03 — 출처: 같은 명령 재사용]
- 무효 0건이므로 미검증 카운터 변동 없음

## Summary
- Total: 17/17 conditions passed (N/A 3건 별도 — 사유 측정 확인됨)
- Verdict: APPROVE
- 봉인(SEAL_OK) · 측정 봉인(MEASURE_OK) · 봉인 커밋 대조(산문·지문 변경 없음) · 공통 전제 G(작업 폴더 clean, HEAD=가지 끝, npm ci 완료) 모두 확인. 20개 조건 전부 직접 재실행한 측정 도우미(`m <조건>`) 출력이 계약에 명시된 값과 완전히 일치하고, 핵심 주장(구조-01 커밋 서명, 구조-02 docstring, 구조-03 기록 낱말, 금지-03 code-fence, 진단-02 markdownlint, 진단-05 로컬 CI)은 측정 도우미 신뢰에만 기대지 않고 직접 재실행해 교차 확인했다. 삭제 0건, 범위 밖 변경 0건, 신규 파일 0건, 사이드카 개정 0건.

## Improvement Suggestions
- 없음
