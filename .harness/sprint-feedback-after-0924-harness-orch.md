# Sprint Feedback
Feature: harness 커밋 훅 · 오케스트레이터 · 문서 매핑 후속 (c1b)
Evaluated: 2026-09-26 13:35
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1b/.harness/sprint-contract-after-0924-harness-orch.md
- sha256: 22a9d884ff8be626f5aef08dd0ec94ac3522547aa445772f3729f620ac4aae5e
- status: done (working tree — HEAD 커밋 값은 active. 라운드 1 QA가 저장 뒤 전환만 하고 커밋은 안 함. 조건 줄과는 무관 — 봉인 판정에 영향 없음)
- slug: after-0924-harness-orch
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1b
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (computed task 가 계약 경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (조건 27개 실측 digest 가 frontmatter conditions_digest sha256:d65525591fade384 와 일치. 계약 전체 sweep 재실행: SEAL_OK 74 · SEAL_ABSENT 9 · SEAL_BROKEN 0)
- contract_seal_broken: n/a
- 봉인 커밋 대조(1-e-3): 봉인 커밋 86f63a3 파일 1개 확인. `git diff 86f63a3 HEAD -- <계약경로>` 출력 없음 — 봉인 이후 계약 원문 무변경(라운드 1 이후 재봉인·산문 변조 없음)
- 재확인(Step 5): 일치 (평가 시작·저장 직전 sha256/status 동일: 22a9d884...)
- status_transition: skipped (이미 라운드 1 QA가 working tree에서 done으로 전환해둠 — 커밋은 지시에 따라 하지 않음)

## Amendments
- amendments: 0 (sprint-amendments-after-0924-harness-orch.md 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (사용자 위임은 계약 배경에 타임스탬프·세션 인용으로 이미 반영됨)
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: f81568d..986bb8d
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1b/.harness/sprint-contract-after-0924-harness-orch.md` · 본 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 SC-01의 [exact,enumerated] 측정범위가 G1~G9로 한정돼 있어, 이번에 고친 두 결함이 "원래도 SC-01 위반"이었는지 "SC-01 측정 밖의 새 발견"이었는지 재확인 필요)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다. 끝내 띄우지 못했으면 `none` 으로 내리고 사유를 `cross_diagnosis_notes` 에 적는다

## Results

### Skill (6/6)
- [x] SK-01: 원본→페이지 매핑 표가 docs-site SKILL.md Step 1 한 곳에만, detect-docs-drift.py 와 쌍 집합 일치 — PASS
  - 근거: 직접 재실행 `python3 .../map_tables.py $W` → `docs-site: rows=15 script_only=0 table_only=0 ghost=0`, `kaizen-orchestrator: rows=0`, `script_ghost=0` (L3)
- [x] SK-02: F2는 가리키기만, 두벌 문장 삭제, 초안 매핑 밖 — PASS
  - 근거: 직접 재실행 (a)1 (b)1 (c)0 (d)1 (L3)
- [x] SK-03: css-tokens Howto Kit 행 1개, 값 일치 — PASS
  - 근거: `accent.py` → `rows=1 pages=7 page_variants=1 match=1` (L3)
- [x] SK-04: Phase 17 절 신설, invented=0/missing_paths=0, 옛문장 삭제 — PASS
  - 근거: `phase17.py` → `heading=1 rows=7 urls=9 invented=0 missing_paths=0`; grep(b)=0 (c)=0 (L3)
- [x] SK-05: 오케스트레이터·데이터풀 §6 Phase 1~17 일치 — PASS
  - 근거: `phase_ref.sh` → `orch_missing=[] pool_missing=[] dup_orch=[] dup_pool=[] ref_13_17_differ=[] ref_13_17_not_s0=[] collector_rc=0` (L3, 실제 collect-kaizen-data.py 실행 포함)
- [x] SK-06: 킷별 리서치 기록 9개 네 자리 일치 — PASS
  - 근거: `rlog_sets.py` → 네 줄 모두 `n=9 missing_vs_want=[] extra=[]`, `checklist_number=9 want_files_exist=9/9 all_equal=1` (L3)

### Script (8/8)
- [x] SC-01: `-a`/같은 명령 `git add` 이동을 이름바꾸기로, 진짜 삭제는 막는다 — PASS
  - 근거: 직접 재실행 `guard_probe.sh` → G1~G9 전부 MATCH, `mismatch_sc=0/7 mismatch_er=0/2` (L3, 실제 훅 실행)
  - Discriminating Evidence: 결합 확인 — guard_probe.sh/guard_test_neg.sh 가 `harness/scripts/commit-guard.sh` 실 파일을 직접 호출(재구현 아님, 코드 추적 확인). 음성 대조(직접 재실행) — `guard_test_neg.sh`가 `git show f81568d:harness/scripts/commit-guard.sh`로 실제 옛 훅을 꺼내 COMMIT_GUARD_HOOK 환경변수로 스왑 실행(자기참조 아님, 스크립트 코드로 확인) → `old_fail=11`(교차 진단이 찾은 신규 케이스 ㊵㊶㊷㊹㊺㊻㊼㊿ 포함), `new_fail=0`
- [x] SC-02: 훅 시험이 SC-01/ER-01 결함 6개+ 각각 한 줄로 잡고 지금 훅은 전부 통과 — PASS
  - 근거: 직접 재실행 `guard_test_neg.sh $W f81568d` → `old_fail=11 old_rc=1 new_pass=65 new_fail=0 new_rc=0`(기준 50 이상 충족). 신규 시험 ㉛~㊴·㊵~㊿ 이 `harness/evals/hooks/commit-guard-test.sh` 실행 목록에 실제 포함되어 도는 것을 grep 으로 라인 확인(L3, 표에만 올리고 안 도는 케이스 없음)
- [x] SC-03: 낡음 감지 원본 7쌍 정확 연결, 초안 미생성 — PASS
  - 근거: 직접 재실행 `drift_e2e.sh` (clone+commit+detect-docs-drift.py 실제 실행) → `expected_hit=7/7 unexpected=0 entries=7 rc=0` (L3)
- [x] SC-04: 매핑 변경 후 신규 고아 페이지/원본 없음 — PASS
  - 근거: 직접 새 클론 2개 생성 후 `drift_map.py` 재실행 → `orphan_pages=21 new_targets=43 added_orphan=0 added_new=0`(기준 21/43 이하 충족) (L3)
- [x] SC-05: AUTO 범위 줄이 Phase5~17·킷 폴더 모두 덮음, 생성기 산출물, 옛문장 삭제 — PASS
  - 근거: 직접 재실행 (a)`scope_gap.py`→`uncovered=0 phases=13` (b)`scope_folders.py`→`folder_miss=0 ghost=0 kits=13` (c)`sync-orchestrator.py --check-only`→exit 0("이미 동기화됨") (d)grep→0 (L3)
- [x] SC-06: Post-Kaizen 검사가 9개 파일 제거를 모두 FAIL, PASS줄에 오답수 없음 — PASS
  - 근거: 직접 재실행 `validator_neg.sh` → `caught=9/9`, intact 줄 `PASS ... all 9 per-kit research-logs exist`(숫자 9만 등장) (L3)
- [x] SC-07: 2000파일 이동 저장소에서 `-a`/`add -A` 2초내 통과 — PASS
  - 근거: 직접 재실행 각 1회(6줄 세트는 c1b-notes.md 기록과 일치) `rc=0 sec=0.27`(add) `rc=0 sec=0.41`(noadd), 2.00초 이하 (L3)
- [x] SC-08: 기존검사 8개+구문검사 전부 exit 0 — PASS
  - 근거: 직접 재실행 `regress.sh $W f81568d 986bb8d` → `steps=14 nonzero=0`, 14단계 전부 rc=0 개별 확인 (L3)

### Error (2/2)
- [x] ER-01: `-i` 막힘 설명 조건부 "작업 폴더 삭제 포함" — PASS
  - 근거: guard_probe.sh G8·G9 MATCH, `mismatch_er=0/2` (L3, SC-01과 같은 실행에 포함)
- [x] ER-02: 생성기 고친 뒤에도 구조오류 exit 2 유지(퇴행 방지) — PASS
  - 근거: 직접 재실행 `sync_err.sh` → `intact=0 no_begin_marker=2 no_marketplace=2` (L3)

### Architecture (3/3)
- [x] AR-01: 커밋구간 변경 허용13/필수10, 킷1개이하, 한국어 제목 — PASS
  - 근거: 직접 재실행 `scope_diff.sh $W f81568d 986bb8d` → `changed=10 outside=0 missing=0 commits=13 multi_kit=0 no_hangul=0`(commits 수는 라운드1의 11에서 신규 수정커밋 2개 추가로 13 — 판정에 영향 없음), git diff로 10개 파일 목록 직접 재확인 (L3)
- [x] AR-02: 봉인 유지·구현기록 넘김/톤대조 — PASS
  - 근거: (a) 전체 sweep `SEAL_OK 74 SEAL_ABSENT 9 SEAL_BROKEN 0`(SEAL_BROKEN 0건이 조건 충족 기준) (b) `c1b-notes.md`의 `## 넘김` 절에 N1~N6 전부(N7·N8은 그 뒤 `## 교차 진단 뒤 고침` 절에 별도 기재, 조건 요구인 N1~N6은 모두 존재), `## 톤 대조` 절(87~119행)에 AR-01 변경파일 10개 전부 등장(awk+grep 직접 실행 확인) (L3)
- [x] AR-03: 측정 도우미 17개가 봉인 때 그대로 — PASS
  - 근거: 직접 재계산 `shasum` vs 계약 표 diff 없음, exit 0 (L3)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py harness --check=code-fence` → exit 0 (L3)
- [x] AP-04: SKILL.md frontmatter name 필드 — PASS
  - 근거: 두 SKILL.md 모두 `name:` 확인 (L3)

### Reusability (2/2)
- [x] RE-01: private 컴포넌트로 만들지 않음 — PASS
  - 근거: `git diff -U0 f81568d 986bb8d -- '*.py' | grep -cE '^\+def _'` = 0 (L3)
- [x] RE-02: 기존 컴포넌트 재사용(새 함수 복제 안 함) — PASS
  - 근거: `overlay_deletes() {` 정의 1개, 호출 3곳(라운드2 수정 후에도 새 함수 안 만들고 기존 함수에 --replace·fallback 추가) (L3)

### Diagnostics (3/4, N/A 1)
- [x] DG-01: N/A (release.sh 교집합 0, 사유 확인) — PASS
  - 근거: `git diff --name-only f81568d 986bb8d | grep -cx 'scripts/release.sh'` = 0 (L3)
- [x] DG-02: IDE 워닝/인포 0건(더한 줄만) — PASS
  - 근거: 직접 재실행 `lint_new.sh $W f81568d 986bb8d <scratchpad markdownlint-cli2 0.23.2> <scratchpad pyflakes 4.0.0, shellcheck 시스템설치>` → `files=10 new_warnings=0` (L3)
- [x] DG-03: N/A (release.sh 교집합 0, 사유 확인) — PASS
- [x] DG-04: N/A (앱/서버 없음, 확장자 md/py/sh만) — PASS
  - 근거: 확장자 집계 `md 4 · py 4 · sh 2` (L3)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 27/27 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-01, ER-01, SC-02 — 데이터 유실(대량 삭제 오판) 방지 가드
- 결합 확인: guard_probe.sh/guard_test_neg.sh 가 `$W/harness/scripts/commit-guard.sh` 실 파일을 GIT_INDEX_FILE 환경 등으로 직접 호출(재구현 없음) — 코드 추적 확인
- 음성 대조: SC-02는 계약에 "음성 대조:" 명시, 이번 평가에서 실제로 옛 훅(`f81568d`)을 `git show`로 꺼내 스왑 실행하여 `old_fail=11`(교차진단이 찾은 신규 회귀 케이스 포함) 확인 — 무력화 시 실패가 재현됨을 실행으로 검증(discrimination: executed)

## Check Artifacts (harness/evals/hooks/commit-guard-test.sh — 이번 라운드 신규 시험 ㊵~㊿)
- 대상: SC-01, SC-02 — 검사 파일 `harness/evals/hooks/commit-guard-test.sh`
- ① 첫 칸만 읽기: 해당 없음 (표-칸 구조 아님, 개별 assert 라인 방식)
- ② 실행 목록: `guard_test_neg.sh`가 `bash "$test_sh"`로 파일 전체를 직접 실행 — ㊵~㊿ 라인이 old/new 실행 출력 grep에 실제로 등장함을 확인(표에만 올리고 안 도는 케이스 아님)
- ③ 한 칸 못 읽으면 전체 꺼짐: 해당 없음 (표-칸 구조 아님)
- ④ zsh·bash: 해당 없음 (고정 해석기 — `bash "$test_sh"`로 스크립트 자체가 bash 고정 호출)
- ⑤ 효과 증명: 알려진 위반(옛 훅 f81568d)에서 ㊵㊶㊷㊹㊺㊻㊼㊿ 8개 신규 케이스 FAIL 확인, 지금 훅에서는 전부 PASS — 검사가 실제로 결함을 가른다는 것을 실행으로 확인

## Evidence Validity
- 검사 대상 증거: 27건, 이번 라운드에서 전건 독립 재실행(구현자 self-측정을 신뢰하지 않고 별도로 도구 재호출)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 전체 조건의 측정 명령을 이 세션이 직접 재실행(zsh 환경, Bash 도구). 고정 해석기(.sh→bash, .py→python3) 스크립트는 해당 없음(고정 해석기)으로 표기
- 양성 대조: [AR-02(a) verify_seal — 계약 전체 sweep에서 SEAL_BROKEN 0건 확인] [DG-02 lint_new.sh — 도우미 내장 로직이 별도 클론에 경고 주입해 검증(구현측 실측값과 일치)] [SC-01/SC-02 — 옛 훅(f81568d) 재실행으로 11건 FAIL 확인, 신규 회귀 케이스 8개 포함]
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 27/27 conditions passed (독립 재실행 기준, 구현자 self-측정값과 전 항목 일치)
- Verdict: APPROVE
- 라운드 1(Iteration 1)이 APPROVE(27/27) 한 뒤, 교차 진단이 commit-guard.sh의 `overlay_deletes`(파일↔폴더 자리바뀜 시 update-index 128 실패로 빈값 통과) 및 `handle_git add`(경로를 좁힌 `-A`가 저장소 전체 추적안된파일을 얹어 경로밖 backup/이 이동으로 위장되는 문제) 결함 2건을 찾았고, 구현자가 커밋 `bb4b2b1`(훅 수정 + 시험 ㊵~㊿ 추가)·`986bb8d`(기록)으로 고쳤다. 본 라운드에서 두 수정이 실제로 결함을 막는지 옛 훅 재실행으로 직접 재현·검증했고, SC-01의 [exact,enumerated] 측정(G1~G9)은 이 두 결함을 포함하지 않아 라운드 1의 PASS 판정 자체는 유효했다 — 교차 진단은 계약 문언 밖의 추가 실무 결함을 찾아 구현이 선제 보강한 사례로 본다.
- 계약 봉인(SEAL_OK, 봉인 커밋 86f63a3 단일 파일, 봉인 이후 조건 줄 무변경) 확인. 삭제 열거 0건, amendments 0건

## Improvement Suggestions
- [SC-01] 범위-미명시 — SC-01의 [exact, enumerated] 측정을 G1~G9로 고정했는데, "진짜 삭제는 그대로 막는다"는 목표(goal) 문언은 이번처럼 엄밀 스코프 밖의 실제 결함(파일↔폴더 자리바뀜, 경로좁힌 -A의 untracked 누락)을 배제한다. 다음 계약에서는 이런 goal 성격 하위절을 별도 `[goal]` 서브조건으로 분리하거나, enumerate 목록에 "known edge cases"를 넘어 fuzzing/랜덤 케이스 최소 요건을 추가하는 것을 권한다
