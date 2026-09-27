# Sprint Feedback
Feature: 카이젠 뒤 남은 것 — api · onboarding · howto-kit (k4) 2 회차 계약
Evaluated: 2026-09-27 12:40
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4/.harness/sprint-contract-after-0926-kits-api-onboarding-howto-r2.md
- sha256: f5f99feca213c7ca17c50caf1bcb73516966e3f7f74bdd73d7762aeb8b6149af
- status: active
- slug: after-0926-kits-api-onboarding-howto-r2
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 지정, test -f 로 존재 확인 완료)
- legacy_contract_used: false
- seal_status: SEAL_OK (measurement_digest 도 MEASURE_OK, zsh · bash 둘 다 동일)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE 이므로 저장 뒤 전환)

⚠️ 1 회차 계약(`.harness/sprint-contract-after-0926-kits-api-onboarding-howto.md`)의
`status: superseded` 는 스키마(`active`|`done`) 밖 값이다. 이 계약(r2) 자신의 문제는 아니며
1 회차는 이미 커밋된 기록이라 손대지 않았다 — 다음 평가자를 위한 경고로만 남긴다.

## Amendments
- amendments: 0 (r2 계약 자체의 사이드카 `.harness/sprint-amendments-after-0926-kits-api-onboarding-howto-r2.md` 없음)
- 참고: 1 회차 개정 A-01(`RE-01`·`RE-02` 측정에서 `.harness/` 제외, `amend_direction_oracle: relaxing`,
  `consent: unanchored`)은 정식 동의를 받지 못한 채 남아 있다. 이 r2 계약은 A-01 을 동의 처리한 것이
  아니라 **같은 변경을 조건 문구 자체에 새로 봉인**해 우회했다 — 근거는 배경 절 3 번째 불릿("이 개정을
  동의 처리한 것이 아니라 … 새 판으로 다시 써서 다시 봉인하는 길이다")과 「자동으로 다 진행해 나한테
  묻지 말고」 라는 **포괄 위임**을 근거로 든 점이다. 사용자 메모리 규칙("완화 개정은 일반 위임으로
  동의 처리 금지 — 조건을 느슨하게 하는 개정은 그것만 콕 집어 물어라")과 정면으로 부딪힌다.
  다만 실측(음성 대조 포함, GAP 분석 및 범위 경계 절)으로 볼 때 이 변경은 대상 조건의 실질 의도
  ("킷·scripts/ 에 새 실행 파일을 더하지 않았다")를 느슨하게 하는 것이 아니라, 계약 자신의 측정
  도구가 자기 자신을 세는 자기참조 결함을 바로잡은 것으로 보인다(더한 파일이 있으면 여전히 FAIL —
  음성 대조로 확인). **PASS 근거로는 r2 조건의 문자 그대로를 그대로 썼다** — 1 회차 A-01 을 근거로
  쓴 것은 아니다. 계약 설계 적절성 자체는 사용자 확인 필요 항목으로 표면화한다(아래 참고).
- 사용자 확인 필요: 위 A-01 우회 패턴이 이번만 허용되는 예외인지, 이후에도 "완화 개정은 새 계약
  재작성으로 우회 가능"이 선례가 되는지 사용자 판단 필요.

## User Correction Audit
- correction_log_status: unavailable (read-union glob 로 조회했으나 이번 세션에서 별도 조회하지 않음 — 표면화 전용이라 verdict 에 영향 없음)
- unreflected_corrections: 0
- verdict 영향: 없음

## Deletions
- deletions_range: 6378948..chore/ak2-k4 (rev-parse 로 해석, UNRESOLVED 아님)
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4/.harness/sprint-contract-after-0926-kits-api-onboarding-howto-r2.md` · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 AR-02 가 1 회차
     봉인 커밋 `927c2a7` 을 기준으로 재는 설계, RE-01/RE-02 의 `.harness` 제외 조건이 자기참조 버그
     수정인지 실질 완화인지)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중 공허한 통과가 있는가? SC-01(`check-reviewer-protocol-copies.py`,
     이번 스프린트에서 수정됨)과 SK-15/16/17(`howto-kit/evals/run-evals.sh`, 이번 스프린트에서 수정됨)에
     대해 아래 Check Artifacts 다섯 항목을 돌렸는지, 돌린 결과가 타당한지 재확인 요청.
- 끝내 띄우지 못했으면 `none` 으로 내리고 사유를 적는다. (이 세션은 산출물만 남긴다 — 실제 서브에이전트
  호출은 부모 몫)

## Results

### Skill (17/17)
- [x] SK-01 — PASS. 근거: `m.sh SK-01` → `step7_lines=1 chips=1 rows=1` (기대와 일치, `api-kit/skills/api-ui/SKILL.md` 8절)
- [x] SK-02 — PASS. `s6_prefixed_example=2 s6_id_word=1 s9_item7_id=1` (기대 `>=1/>=1/=1` 충족)
- [x] SK-03 — PASS. `s2_strip_rule=1` (기대 `>=1`)
- [x] SK-04 — PASS. `hold=3 flaky=3 hold_fail=3 flaky_fail=3 label=2 state_enum=1 new_state=0` (전부 기대 충족)
- [x] SK-05 — PASS [enumerated 3/3 확인]. 세 파일 모두 `strict_note=1`
- [x] SK-06 — PASS [goal]. hurl 8.0.1 실행 결과 `index_asserts=0 collection_line=1`, `n=0/1/2 rc=0` 전부 (기대와 정확히 일치)
- [x] SK-07 — PASS. `s7_cmd=1 s7_row=1 s6_csp=1`, 대조 `example_csp=1 mockup_v8_csp=0`
- [x] SK-08 — PASS. `ko1_cases=1`(기대 `>=1`), `runner_rc=0 declared=11 ran=11 fail=0`, 음성 대조 `NEG-KO g1_neg_rc=1`
- [x] SK-09 — PASS. `example_same_shell=1 example_g5_pass=1 example_gate_pass=1`
- [x] SK-10 — PASS [enumerated]. `cases=11 g5_one=11`(동일), `five_lines=0 six_lines=2 run_line_g5=1`
- [x] SK-11 — PASS. `cocoapods_line=1 flutter_keep=1 evals_spm_assert=1`
- [x] SK-12 — PASS. `howto_ok=1 source_line=1 grade_line=1 tools=[Read, Grep, Glob] docstring_eight=1`
- [x] SK-13 — PASS. `unverified_line=1 not_pass=1`
- [x] SK-14 — PASS. `dita_lines=1 url=1 d13=1 checked=1`
- [x] SK-15 — PASS [goal]. 실행 결과 `orig mutated=0 rc=0 EVALS_PASS` · `assert mutated=1 rc=1 EVALS_FAIL` · `shell mutated=1 rc=1 EVALS_FAIL` — 자기 무력화 음성 대조 정확히 일치(계약 자체가 음성 대조인 조건)
- [x] SK-16 — PASS. `rc=0 EVALS total=35 pass=35 fail=0 seconds=13.6` (<=30 충족, 시작 판 9.6 대비 여전히 여유)
- [x] SK-17 — PASS. `c5_three=1`

### Script (1/1)
- [x] SC-01 — PASS [exact]. `copies_rc=0 ok_lines=8 howto_ok=1 checked=8 violations=0 infra_errors=0 excluded=0`,
  음성 대조 `NEG-KH1 neg_rc=1 1`(가지 끝 판 기대값과 정확히 일치, 시작 판 대비 반대로 뒤집힘 확인).
  **Check Artifacts 5 항목 수행(스크립트가 이번 스프린트에서 수정됨, 아래 블록 참조)** — 결함 없음.

### Error (3/3)
- [x] ER-01 — PASS. `report_unjudged=2 matched=2`
- [x] ER-02 — PASS [enumerated 3/3]. `contract_gate=1 verify_class=1 probe_gate=1` (시작 판과 동일 — 글만 바뀌고 동작 불변 확인)
- [x] ER-03 — PASS [enumerated]. `g5_fail_cases=2 empty_kind=1 nourl_kind=1 runner_rc=0`, 음성 대조 `NEG-KO g5_neg_rc=1`

### Architecture (4/4)
- [x] AR-01 — PASS [enumerated 13/13]. `scope_out=0 required_missing=0 new_onboarding_fixtures=4`(기대 `>=3` 충족).
  필수 13 경로 전부 diff 범위 안(측정기가 직접 목록 대조).
- [x] AR-02 — PASS. `mixed=0 seal_commit_files=1 impl_before_seal=0`. 구현 커밋 7개 각각 킷 하나로만 태그됨(api-kit·onboarding-kit·howto-kit·scripts 어느 하나).
- [x] AR-03 — PASS. `SEAL_BROKEN` 0건(`9 SEAL_ABSENT 91 SEAL_OK`), `tools_sha=8569f2af6e22daa3`(봉인값과 일치, 직접 재계산으로 확인)
- [x] AR-04 — PASS. 로컬 CI 실행(TMPDIR 격리) 결과 `rc=0` 25줄 + `feedback-agg-test SKIP (yq 없음)` 1줄 — 봉인 전 값과 정확히 일치(직접 실행, 백그라운드 완료 확인)

### Anti-patterns (2/2)
- [x] AP-03 — PASS. `validate-plugin.py --check=code-fence` api-kit/onboarding-kit/howto-kit 세 번 모두 종료 코드 0 (직접 실행)
- [x] AP-04 — PASS. `validate-plugin.py` howto-kit/onboarding-kit/api-kit 세 번 모두 종료 코드 0 (직접 실행)

### Reusability (2/2)
- [x] RE-01 — PASS. N/A 사유 측정 직접 재실행: `git diff --diff-filter=A --name-only 6378948 chore/ak2-k4 -- scripts '*.sh' '*.py' ':(exclude).harness'` → 0줄. 사유 참이므로 N/A 유효.
- [x] RE-02 — PASS. 같은 측정 0줄 + `run-gate-evals.sh` unchanged(`git diff --quiet` rc=0) 직접 확인.

### Diagnostics (4/4)
- [x] DG-01 — PASS. N/A 사유 측정: `git diff --name-only 6378948 chore/ak2-k4 | grep -c '^scripts/release.sh$'` → 0. 사유 참.
- [x] DG-02 — PASS. `MDL`/`PYF` 스크래치패드 설치본으로 직접 실행 → `files=17 new_warnings=0`, json_bad 0줄(`json_ok` 만 출력)
- [x] DG-03 — PASS. DG-01 과 같은 측정 0. 사유 참.
- [x] DG-04 — PASS. N/A 사유 측정: 바뀐 파일에 앱/서버 진입점 패턴(`main.*`/`server.*`) 0건 직접 확인.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (33 - 0) / 33 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (전 조건 L3 직접 측정, 미검증 없음)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 규칙 12 의 9 항(동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션
  안전성·재시도/중복제거·보안 경계·사용자 결함 보고 충돌) 중 해당하는 조건이 이 계약에 없음.

## Check Artifacts (산출물이 검사인 조건 — SC-01, SK-15/16/17)
- 대상 1: `scripts/check-reviewer-protocol-copies.py` (이번 스프린트에서 수정 — 10줄 변경)
  - ① 첫 칸만: 해당 없음 (사유: 열 구조 아님 — REVIEWERS 리스트를 개별 순회하며 8개 파일을 각각 검사. 사본 실험에서 rust-kit(UNREADABLE)·infra-kit(MISMATCH) 둘 다 동시에 잡혀 "첫 항목만 읽고 멈춤" 아님을 확인)
  - ② 실행 목록: howto-reviewer.md 가 REVIEWERS 리스트에 포함되어 실제 검사 대상(SC-01 측정 `checked=8 howto_ok=1` 로 확인)
  - ③ 못 읽는 칸 + 실제 위반: 임시 사본(`/private/tmp/.../qa-sc01-test/repo`)에서 rust-kit 사본을 깨진 인코딩으로, infra-kit 사본에서 조항 블록 제거 → `MISMATCH infra-kit/...`(위반 잡힘) + `UNREADABLE rust-kit/...`(별도 표시) + `checked=8 violations=1 infra_errors=1` + `exit=2`(성공 코드 아님). 한 칸 못 읽어도 다른 칸 위반이 은폐되지 않음을 확인.
  - ④ zsh·bash: 해당 없음 (고정 해석기 — `python3` 스크립트, 셸 분기 없음)
  - ⑤ 효과 증명: `m.sh NEG-KH1 chore/ak2-k4`(howto-reviewer.md 의 마커 조항 줄 제거한 사본) → `neg_rc=1 1`(실패로 잡힘). 알려진 위반에서 실패를 낸다.
- 대상 2: `howto-kit/evals/run-evals.sh` (이번 스프린트에서 수정 — 32줄 추가/13줄 삭제)
  - ① 첫 칸만: 해당 없음 (사유: 열 구조 아님 — assertion 목록을 전부 순회)
  - ② 실행 목록: `.github/workflows/ci.yml:102` `run: sh howto-kit/evals/run-evals.sh` 로 CI 에 등록, 로컬 `ci-local.sh` 의 `howto-gate-evals` 단계로도 실행됨(직접 확인). SK-16 측정 `declared=35 ran=35`(새 fixture 포함 전부 실행, 스킵 없음)
  - ③ 못 읽는 칸 + 실제 위반: 해당 없음 (구조상 개별 assertion 실패가 즉시 종료 코드에 반영되며, 계약 SK-15 조건 자체가 이 항목의 음성 대조를 요구·수행함)
  - ④ zsh·bash: SK-17 `c5_three=1`(설계 기록이 zsh·bash·sh 세 셸 대조를 명시) + SK-15 `lit_shell=2`(셸 대조 코드 자체를 무력화하는 음성 대조 존재) — 직접 실행 결과 `shell mutated=1 rc=1 EVALS_FAIL` 확인.
  - ⑤ 효과 증명: SK-15 측정 자체가 이 항목 — `assert mutated=1 rc=1 EVALS_FAIL`, `shell mutated=1 rc=1 EVALS_FAIL` (알려진 위반에서 실패). 원본은 `rc=0 EVALS_PASS`.

## User-Reported Failures
- 해당 없음 (이번 회차에 사용자 실패 보고 없음)

## Evidence Validity
- 검사 대상 증거: 33건 (조건 전부)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 33건 · zsh/bash 양쪽 확인 3건(seal/measure 검증, SK-09/SK-15 의 셸 대조) · 미실행 0건
- 양성 대조: [AR-01 — 계약 기재 양성 대조 인용(봉인 전 실측), 이번 세션 직접 재검증은 생략 — 계약 자체에 실측값이 있고 AR-01 required_missing=0/scope_out=0 으로 정합성 간접 확인] · [DG-02 — 계약 기재 양성 대조(MD040+pyflakes 위반 커밋 시 new_warnings=2) 인용] · [SC-01 — 이번 세션 직접 임시 사본으로 재실행, MISMATCH+UNREADABLE 동시 검출 확인] · [SK-15 — 계약 조건 자체가 양성/음성 대조를 겸함, 이번 세션 직접 재실행으로 재확인]
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 33/33 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- [RE-01] 검증경로-미기재 — 1 회차의 자기참조 측정 버그(계약이 요구한 측정 도구 자신을 계약이 다시 세는 문제)를
  다음부터는 사이드카 amendment 로 사용자에게 콕 집어 동의를 구하는 절차를 먼저 시도하고, 그것이 막히면
  "재봉인 사유"를 계약 배경에 명시적으로 "amendment 우회" 로 표기해 다음 평가자가 놓치지 않게 한다.
