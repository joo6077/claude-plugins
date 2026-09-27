# Sprint Feedback
Feature: 카이젠 뒤 남은 것 — api · onboarding · howto-kit (k4)
Evaluated: 2026-09-27 11:47
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4/.harness/sprint-contract-after-0926-kits-api-onboarding-howto.md
- sha256: 8572e0f84b274a2adf8513286636466a5feed8a07371bce6c0707f454a5bce11
- status: active
- slug: after-0926-kits-api-onboarding-howto
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (m.sh AR-03 실측: `9 SEAL_ABSENT 90 SEAL_OK`, 이 계약 자체는 목록에서 OK 쪽)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256 · status 재확인 동일)
- status_transition: skipped (verdict=REJECT status=active)

## Amendments
- amendments: 1
- PASS 근거 가능: 0
- PASS 근거 불가: 1 — **사용자 확인 필요** [relaxing · unanchored]
  - [A-01 · relaxing · unanchored (consent 칸 공백, 세션 bda55d45 jsonl 전체 및 reflect-kit 프롬프트 로그 2026-09.md 전체 대조, 11:16 봉인 이후 사용자 발언 0 건)] RE-01·RE-02 측정 명령에 `':(exclude).harness'` 추가 → RE-01, RE-02
- 집합형 direction 계산 결과: `amend_direction_oracle` → `relaxing measured_removed=5 measured_added=0` (사이드카 기재값과 직접 재확인 일치)
- 계약 자체가 명시: "조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다" (배경 절) — 2026-09-26 일반 위임은 이 개정의 동의로 쓸 수 없다는 것이 계약 문언

## User Correction Audit
- correction_log_status: available (`/Users/jackson/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (봉인 11:16 이후 프롬프트 로그 항목 0 건 — 세션 jsonl 마지막 발언도 02:07:11Z(=11:07 KST)로 봉인 전. 교정 자체가 없어 반영 여부를 따질 대상이 없음)
- verdict 영향: 없음 (표면화 전용 · 미검증 카운터 비합산)

## Deletions
- deletions_range: 6378948..aafcd94
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4/.harness/sprint-contract-after-0926-kits-api-onboarding-howto.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 RE-01·RE-02 를 amendment 미동의 상태에서 문자 그대로 FAIL 판정한 것이 타당한지)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? m.sh 자체는 이번 스프린트가 새로 만든 검사 스크립트이므로 규칙 10 의 다섯 가지 중 돌리지 않은 것이 있는지도 확인 필요 — 아래 Check Artifacts 참고
- cross_diagnosis_by: pending-parent (평가자가 직접 서브에이전트를 띄우지 않음)

## Results

### Skill (16/17)
- [x] SK-01 — PASS · `step7_lines=1 chips=1 rows=1` (m.sh 실측, 기대와 일치)
- [x] SK-02 — PASS · `s6_prefixed_example=2 s6_id_word=1 s9_item7_id=1`
- [x] SK-03 — PASS · `s2_strip_rule=1`
- [x] SK-04 — PASS · `hold=3 flaky=3 hold_fail=3 flaky_fail=3 label=2 state_enum=1 new_state=0`
- [x] SK-05 — PASS · 세 파일 모두 `strict_note=1` (`api-kit/skills/api-contract/SKILL.md` · `api-verify/SKILL.md` · `api-probe/SKILL.md`) [enumerated 3/3 확인]
- [x] SK-06 — PASS · `index_asserts=0 collection_line=1` · `n=0/1/2 rc=0` (hurl 8.0.1 실행 확인, goal 태그 충족)
- [x] SK-07 — PASS · `s7_cmd=1 s7_row=1 s6_csp=1` · `example_csp=1 mockup_v8_csp=0`
- [x] SK-08 — PASS · `ko1_cases=1` · `runner_rc=0 EVALS declared=11 ran=11 fail=0`
- [x] SK-09 — PASS · `example_same_shell=1 example_g5_pass=1 example_gate_pass=1`
- [x] SK-10 — PASS · `cases=11=g5_one` · `five_lines=0 six_lines=2 run_line_g5=1`
- [x] SK-11 — PASS · `cocoapods_line=1 flutter_keep=1 evals_spm_assert=1`
- [x] SK-12 — PASS · `howto_ok=1 source_line=1 grade_line=1 tools=[Read, Grep, Glob]`
- [x] SK-13 — PASS · `unverified_line=1 not_pass=1`
- [x] SK-14 — PASS · `dita_lines=1 url=1 d13=1 checked=1`
- [x] SK-15 — PASS · `lit_assert=1 lit_shell=2`, mutated 사본 둘 다 `rc=1 EVALS_FAIL`, 원본은 `rc=0 EVALS_PASS` (goal, 판별력 확인됨)
- [x] SK-16 — PASS · 측정값 `seconds=12.7` (기준: <=30) · `rc=0 total=35 pass=35 fail=0`
- [x] SK-17 — PASS · `c5_three=1`

### Script (1/1)
- [x] SC-01 — PASS · `copies_rc=0 ok_lines=8 howto_ok=1 checked=8 violations=0 infra_errors=0 excluded=0 docstring_eight=1`

### Error (3/3)
- [x] ER-01 — PASS · `report_unjudged=2 matched=2`
- [x] ER-02 — PASS · `contract_gate=1 verify_class=1 probe_gate=1`
- [x] ER-03 — PASS · `g5_fail_cases=2 empty_kind=1 nourl_kind=1` · `runner_rc=0`

### Architecture (4/4)
- [x] AR-01 — PASS · 측정값: `scope_out=0 required_missing=0 new_onboarding_fixtures=4` (기준: >=3)
- [x] AR-02 — PASS · `mixed=0 seal_commit_files=1 impl_before_seal=0`
- [x] AR-03 — PASS · `SEAL_BROKEN` 없음, `tools_sha=8569f2af6e22daa3` (기대와 일치)
- [x] AR-04 — PASS · 로컬 CI 직접 실행, `rc=0` 25 줄 + `feedback-agg-test SKIP (yq 없음)` 1 줄, 봉인 전 값과 동일

### Anti-patterns (2/2)
- [x] AP-03 — PASS · `validate-plugin.py --check=code-fence` 세 킷 모두 exit 0
- [x] AP-04 — PASS · `validate-plugin.py` 세 킷 모두 exit 0 (name 필드 누락 없음)

### Reusability (0/2)
- [ ] RE-01 — FAIL
  - 근거: N/A 사유 「측정: `git diff --diff-filter=A --name-only 6378948 chore/ak2-k4 -- scripts '*.sh' '*.py'` 0 줄」이 거짓 — 직접 재실행 결과 5 줄(`.harness/.meta/after-0926-kits-api-onboarding-howto/{ci-local.sh,ka5.sh,m.sh,ob.py,stub.py}`). 이를 배제하는 amendment A-01 은 `relaxing · unanchored` 라 PASS 근거로 쓸 수 없다(Amendments 절 참고). 계약 규칙 "N/A 사유가 거짓이면 FAIL — N/A 남용" 적용
  - 수정: 사용자가 amendment A-01 에 명시 동의(발언 인용 + 시각 + 세션)를 남기거나, 조건 문언에 `':(exclude).harness'` 를 직접 반영한 재승인 버전으로 재봉인
- [ ] RE-02 — FAIL
  - 근거: 같은 N/A 사유가 "RE-01 과 같은 명령 0 줄"을 요구하는데 그 값이 5 줄로 확인됨(위와 동일 근거). 두 번째 하위 측정(`run-gate-evals.sh` unchanged, `git diff --quiet` rc=0)은 참이지만 N/A 성립에는 두 측정 모두 참이어야 한다
  - 수정: RE-01 과 동일

### Diagnostics (3/4, N/A 3)
- [x] DG-01 — N/A (사유 참: `scripts/release.sh` 교집합 0, 직접 재확인)
- [x] DG-02 — PASS · `files=17 new_warnings=0`, `json_ok evals.json` (markdownlint-cli2 0.23.2 · pyflakes 로 직접 재측정, 양성 대조는 계약 봉인 전 실측 기록 인용)
- [x] DG-03 — N/A (사유 참: 동일 교집합 0)
- [x] DG-04 — N/A (사유 참: 바뀐 파일에 실행 진입점 0개, 직접 파일 목록 확인)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (33 - 0) / 33 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (RE-01·RE-02 FAIL 이 REJECT 사유이며, 미검증 카운터와는 무관)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 이번 조건군에 동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션 안전성·재시도/중복제거·보안 경계·사용자 결함 보고 대상 없음

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: `m.sh`(이번 스프린트가 봉인 뒤 커밋한 새 측정 도구, 33개 조건 대부분이 이 스크립트로 판정됨)
- ① 첫 칸만: 해당 없음 (m.sh 는 표 형식 검사가 아니라 조건 ID 별 개별 서브루틴 — "첫 칸만 읽기" 실패 유형이 구조적으로 적용되지 않음)
- ② 실행 목록: 해당 없음 (m.sh 는 CI 러너에 등록된 시험 파일이 아니라 이 QA 세션이 직접 호출하는 계약 부속 도구)
- ③ 못 읽는 칸 + 실제 위반: 해당 없음 (표/칸 구조 아님)
- ④ zsh · bash: SK-06·SK-08·SK-09·SK-10·ER-03·DG-02·AR-03·AR-04·SC-01 등을 이 세션의 zsh 로 직접 실행(위 Results 근거). m.sh 내부는 `#!/usr/bin/env bash` 로 시작해 해석기 고정 — bash 로만 도는 것이 맞음. `해당 없음 (고정 해석기)`
- ⑤ 효과 증명: **직접 확인됨.** SK-06(음성 대조: `$.data[*].id` 로 바꾼 사본 `n=1 rc=4`, 이번 세션 값과 별개로 계약이 봉인 전 실측 기록), SK-15(이번 세션이 직접 재현: assertion·셸 대조를 무력화한 사본 각각 `rc=1 EVALS_FAIL`, 원본은 `rc=0 EVALS_PASS`), ER-01(`onHand`→`onHandX` 변형 사본 `matched=1` vs 원본 `matched=2`, 계약 기록), DG-02(MD040·pyflakes 위반 삽입 사본 `new_warnings=2` vs 이번 실측 `0`), AR-01(`onboarding-kit/README.md` 삽입 사본 `scope_out=1`, 계약 기록), AR-02(묶음 섞은 사본 `mixed=1`, 계약 기록) — m.sh 가 알려진 위반에서 실제로 실패를 내는 것을 다건 확인. 판별력 있는 검사로 판단

## Evidence Validity
- 검사 대상 증거: 33 건 전부 이 세션이 직접 명령을 실행해 수집 (m.sh 호출, validate-plugin.py 직접 실행, ci-local.sh 직접 실행, git diff 직접 실행)
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 실행 33 건 (전부 zsh 에서 직접 실행. m.sh 내부는 고정 bash 해석기라 해당 없음)
- 양성 대조: SK-06 · SK-15 · ER-01 · DG-02 · AR-01 · AR-02 — 위 Check Artifacts ⑤ 참고, 전부 계약 기재값과 이번 세션 직접 실측이 일치
- 무효 0 건이므로 미검증 카운터 영향 없음

## Summary
- Total: 31/33 conditions passed
- Verdict: REJECT
- FAIL 항목: RE-01, RE-02 — 둘 다 같은 원인(측정 명령이 이 계약 자체가 봉인 뒤 커밋하기로 정한 `.harness/` 측정 도구 5개 파일을 "새 스크립트"로 잡아 N/A 사유가 거짓이 됨). Amendment A-01 이 이를 고치는 개정이지만 `relaxing · unanchored`(동의 칸 공백, 세션 로그·프롬프트 로그 전체 대조 결과 봉인 이후 사용자 발언 0건)라 PASS 근거로 쓸 수 없다.
- 수정 우선순위: 1) 사용자가 amendment A-01 에 명시 동의(발언 인용 · 시각 · 세션)를 남긴다, 또는 2) 계약을 재작성해 RE-01·RE-02 측정에 `':(exclude).harness'` 를 처음부터 반영한 뒤 재봉인한다. 그 외 31개 조건은 전부 PASS이며 구현 자체의 결함은 없다 — 이번 REJECT 는 순수하게 계약-측정 충돌(교차 진단이 사전에 지적한 사안)에 대한 동의 미비 때문이다.

## Improvement Suggestions
- [RE-01, RE-02] 측정-환경-오염 — 조건 작성 시점에 "이 계약 자신이 봉인 뒤 커밋하는 `.harness/` 측정 도구"가 "새 스크립트 0줄" 측정에 걸리지 않도록 최초 조건 문언에 `':(exclude).harness'` pathspec 을 포함해 작성한다. 이번처럼 봉인 뒤에야 발견되면 amendment 동의를 받는 데 시간이 걸려 매 iteration REJECT 가 반복될 위험이 있다.
