# Sprint Feedback
Feature: 킷 약점 (api · bambu · onboarding · 설치본 안내) — 묶음 k1
Evaluated: 2026-09-28 12:19
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: .harness/sprint-contract-after-0928-kit-weaknesses.md
- sha256: 2d350634ca1bfdaecdd43597b6c167fab7e0f4e74011cbe0a12a227e1a869fcc
- status: done (round 1에서 전환. 계약 산문 변경 없음 — 재확인 일치)
- slug: after-0928-kit-weaknesses
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-k1
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 봉인 커밋 c8e2d0e — 파일 1개, 봉인 이후 산문 변경 0 (frontmatter status 줄 제외, 직접 diff 재확인)
- 측정 묶음 13개 sha256 앞 16자리 전부 봉인 전 값과 일치 (직접 재계산 확인)
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=APPROVE 이나 status 가 이미 "active" 아닌 "done" — 전환 대상 아님)

## Amendments
- amendments: 0 (사이드카 파일 없음 — `sprint-amendments-after-0928-kit-weaknesses.md` 부재 확인)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/ 존재 확인)
- unreflected_corrections: 0 (이번 QA 요청("약점과 일부만 한 거 다처리하지??")은 계약 범위 밖 12개 항목(A1·A2·A3·B12~B20·D1·D3)에 대한 것이며, 계약 「범위 경계」·「교차 진단 반영」 절에 이미 표면화되어 있음 — 부모 세션이 배정할 몫)
- verdict 영향: 없음

## Deletions
- deletions_range: 95508d9..chore/ak3-k1
- 커밋 구간 삭제: 0 (`git diff --no-renames --name-status` 재확인)
- 커밋하지 않은 삭제: 0 (`git status --porcelain --no-renames` 재확인)
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-k1/.harness/sprint-contract-after-0928-kit-weaknesses.md` · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 SC-02 의 m1/m4 콜래터럴 불일치를 계약 문구 그대로 "존재만 요구"로 읽어 PASS 로 유지한 것 — round2 에서도 같은 결론, 개선 제안으로만 표면화)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? DG-02 는 이번 라운드에 실제로 baseline 밖 파일 위반이 있었다가(round2 REJECT) 고쳐져 0 이 된 사례라 공허한 0 이 아님을 직접 재현 확인했다.
- 끝내 띄우지 못했으면 `none` 으로 내리고 사유를 적는다 — 이번 세션은 서브에이전트를 띄우지 않았다(tools 에 Agent 없음)

## Results

### Skill (6/6)
- [x] SK-01: A15 예시 화면 자료 — PASS
  - 근거: `python3 $M/a15-ep.py ...` → `SUMMARY eps=6 fail=2 hold=1 flaky=1 misplaced=0`, `MATCH report_hold=1 report_flaky=1 expect_fail=2 ok=1` (직접 재실행) [L3]
- [x] SK-02: A15 화면이 표지를 그린다 — PASS
  - 근거: `npx playwright test api-kit/evals/` → `12 passed`(>8), rc=0. `--list` 에 `보류`·`flaky` 시험 각 1개 이상 [L3]
- [x] SK-03: A15 음성 대조 — PASS
  - 근거: 두 변이 모두 직접 재현. (1) `failMark:'보류'/'flaky'` → null 사본: `grep -c "failMark:'"` 0, `npx playwright test` rc=1, 4 failed [L3]. (2) `failMarkHTML()` 함수 본문을 빈 문자열 반환으로 치환한 사본: `grep -c '게이트를 깨지 않음'` 1(코드 밖 라벨 딕셔너리에만 남음, 실제 렌더 경로 제거), `npx playwright test` rc=1, 4 failed [L3]
- [x] SK-04: B11 설치본 안내 — PASS
  - 근거: `python3 $M/b11-docs-guidance.py $W` → `TOTAL files=94 ok=73 need=0 exempt=21`, `comm -23` 결과 0(60개 파일 전부 OK) [L3]
- [x] SK-05: B21 — PASS
  - 근거: (1) `<https://` 0, 백틱 인용 1 (2) N-12 제목줄 0, SHOULD 동반 줄 1, `### ` 4개 [L3]
- [x] SK-06: D7 SKILL.md 버전 표 — PASS
  - 근거: `02.06.00.51\` 기준` 0, `references baseline` 0, `bambu-02.08.02.61.tsv` 1(파일 존재 확인), `02.08.02` 든 표줄 2, `02.06.00` 표줄에 `그대로 사용` 0 [L3]

### Script (7/7)
- [x] SC-01: B5 이 맥 — PASS
  - 근거: `bash bambu-kit/evals/run-gate-fixtures.sh` → `결과: 24 경우 중 불일치 0`, rc=0. 지정 5행 전부 `일치` 확인 [L3]
- [x] SC-02: B5 음성 대조 — PASS
  - 근거: `sh $M/b5-controls.sh $W` → m1(차이줄=1, rc=1, 불일치줄에 filament-lattice-fanfix.json 포함), m2(차이줄=2, rc=1, 불일치=filament-unreadable-slot.json), m3(차이줄=2, rc=1, 불일치=process-thin-unreadable-slot.json), m4(차이줄=2, rc=1, 불일치줄에 process-thin-baseline.json 포함) [L3]
  - 관찰(개선 제안 유지): m1/m4 는 지정 파일 외에 부수적으로 다른 파일도 불일치로 잡힌다. 계약 문구는 "이름이 나온다"(포함 여부)만 요구하므로 FAIL 은 아니다.
- [x] SC-03: B6 표 모양 — PASS
  - 근거: `sh $M/b6-check.sh $W <폴더> zsh` → `total=30 diff=0`, `... bash` → `total=30 diff=0` [L3]
- [x] SC-04: B6 시험 등록 — PASS
  - 근거: `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` → `EVALS declared=23 ran=23 fail=0`, `EVALS_PASS`. `python3 $M/b6-registered.py` → `SHAPES covered=7/7 crlf_cases=2` [L3]
- [x] SC-05: B6 기존 판정 유지 — PASS
  - 근거: 12개 기존 사례 `fixture`·`stack`·`expect` 를 python 으로 BASE 판과 맞댐 → diffs=0 [L3]
- [x] SC-06: B11 레포 검사 — PASS
  - 근거: `ci.yml` 의 `run: python3 scripts/check-install-docs-guidance.py` 1줄, 직접 실행 rc=0 [L3]
- [x] SC-07: 로컬 CI — PASS
  - 근거: `ci-local.sh` 25단계 직접 재실행, 전부 rc=0(feedback-agg-test 는 yq 없어 SKIP, 조건 허용). CI 전용 6단계(check-api-kit-docs 12/12 PASS, detect-docs-drift 어긋남 0, check-cause-table-copies violations=0, measure-helpers-test 실패 0건, makerworld-fetch-test 불일치 0, check-install-docs-guidance rc=0) 전부 직접 재실행 rc=0 [L3]

### Error (3/3)
- [x] ER-01: B5 설치본 없는 기계 — PASS
  - 근거: `sh $M/b5-controls.sh $W` noinst 사본 → `결과: 24 경우 중 불일치 0 · 건너뜀 19`, rc=0. 지정 3파일 모두 건너뜀 줄에 `[미검증]` 포함 [L3]
- [x] ER-02: B6 알아보지 못한 표 — PASS
  - 근거: `empty-five-col(-crlf).md` → `G5_BLOCKING FAIL rows=0 ... unrecognized=1`(PASS rows=0 아님), `plain-unrelated(-crlf).md` → `G5_BLOCKING PASS rows=0` [L3]
- [x] ER-03: B11 raw 도 못 읽을 때 — PASS
  - 근거: 60개 파일에서 raw 주소 + 안내 줄 A=61, 두 문구 동시 포함 줄 B=61 (재실행 확인) [L3]

### Architecture (4/4)
- [x] AR-01: D7 문서 쪽 — PASS
  - 근거: `02.06.00.51</code> 기준` 0, `references 기준값` 0, `<tr>` 줄 중 `02.08.02` 1, `bambu-02.08.02.61.tsv` 1. CSS 링크 1개. `page-overflow.js` → `OVERFLOW checked=3 bad=0` [L3]
- [x] AR-02: B6 문서 쪽 함수 사본 — PASS
  - 근거: `python3 $M/b6-page-copy.py $W` → `COPY lines=105 page_lines=105 diff=0` [L3]
- [x] AR-03: B5 문서 쪽 표 — PASS
  - 근거: `python3 $M/b5-page-table.py $W` → `TABLE skill_rows=24 page_rows=24 diff=0 only_one_side=0` [L3]
- [x] AR-04: 바뀐 경로와 커밋 모양 — PASS
  - 근거: `git diff --name-only 95508d9..chore/ak3-k1 -- . ':(exclude).harness'` 84개 경로 전부 `# sprint-scope` 블록 안(직접 대조). 구간 내 19개 커밋 전부 `git show --name-only` 로 맨 위 폴더 1개씩(멀티폴더 커밋 0, 직접 루프 확인) [L3]

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` → `Total: 14 plugins, 14 OK` [L3]
- [x] AP-04: frontmatter name 누락 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=frontmatter` → `Total: 14 plugins, 14 OK` [L3]

### Reusability (2/2)
- [x] RE-01: 새 레포 검사는 scripts/ 에 둔다 — PASS
  - 근거: `test -f scripts/check-install-docs-guidance.py` [L2]
- [x] RE-02: 기존 컴포넌트 재사용 — PASS
  - 근거: `grep -c '^guide_gate() {'` = 1, `grep -cE '^[a-z_]+\(\) \{'` 현재판=1, BASE판(95508d9)=1 (동일) [L3]

### Diagnostics (2/4, N/A 2)
- [ ] DG-01: N/A — `git diff --name-only 95508d9..chore/ak3-k1 | grep -c '^scripts/release.sh$'` = 0 확인. 대체 검증: `shellcheck bambu-kit/evals/run-gate-fixtures.sh` 경고 0(직접 재실행) [L3]
- [x] DG-02: IDE diagnostics 워닝/인포 0개 — **PASS**
  - 근거: 이번 스프린트에서 바뀐 비-.harness `.md` 파일 75개 전체에 `markdownlint-cli2 --config {"config":{"MD013":false}}` 직접 재실행 → `Linting: 75 files`, `Summary: 147 issues in 3 files`. 파일별 위반 수: `bambu-kit/skills/bambu-print-profile/SKILL.md` 120 · `api-kit/skills/api-ui/SKILL.md` 25 · `onboarding-kit/skills/setup-guide/SKILL.md` 2 — 세 파일 모두 `md-before.txt` 봉인 전 값과 정확히 일치. 나머지 72개 파일(round2 에서 REJECT 사유였던 신규 픽스처 2개 포함)은 0건. round3 커밋(`56f3356`)이 두 픽스처에 `<!-- markdownlint-disable MD050 -->` / `<!-- markdownlint-disable MD055 -->` 를 줄 단위로 추가해 해당 규칙만 끈 것을 직접 확인(`onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-blocking-empty-under-head.md`, `-no-edge-pipe.md` head 확인) — G5 가 알아보는 표기(밑줄 강조·양끝 파이프 없는 표) 자체는 손대지 않음 [L3]
- [ ] DG-03: N/A — DG-01 과 동일 확인(대상 파일 0). 대체 검증: SC-01·SC-04·SK-02 실행 결과로 완료 [L3]
- [x] DG-04: 실제 앱/서버 구동 시 에러 0개 — PASS
  - 근거: SK-02 의 `npx playwright test api-kit/evals/` 결과(12 passed, 콘솔 error 확인 4개 조합 포함) [L3]

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (28 - 0) / 28 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건 없음)
- 해당 없음 — 이번 계약 조건 중 동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션 안전성·재시도/중복제거·보안 경계·사용자 결함 보고 충돌 어디에도 해당하지 않음

## Check Artifacts (해당 조건: SC-01·SC-02·SC-03·SC-04·ER-01·ER-02)
- 대상: bambu-kit/evals/run-gate-fixtures.sh, onboarding-kit/skills/setup-guide/SKILL.md (guide_gate)
- ① 첫 칸만: 해당 없음 (24개 픽스처 전부 개별 실행되는 구조라 "칸" 개념 없음)
- ② 실행 목록: `run-gate-fixtures.sh`·`run-gate-evals.sh` 모두 `ci.yml`·`ci-local.sh` 단계로 이번 세션에서 직접 재실행 확인
- ③ 못 읽는 칸 + 실제 위반: ER-01(noinst 사본, 3파일 건너뜀·나머지 21개 정상)과 SC-02(m1~m4 알려진 위반 주입 → 전부 rc=1)로 직접 재확인
- ④ zsh·bash: SC-03 에서 zsh(`total=30 diff=0`)·bash(`total=30 diff=0`) 둘 다 이번 세션에서 재실행
- ⑤ 효과 증명: SC-02(bambu, m1~m4), SK-03(api, 2가지 변이), SC-05(onboarding, round2 확인 유지) 전부 알려진 위반 → 실패 재현 직접 확인

## User-Reported Failures
- 해당 없음

## Evidence Validity
- 검사 대상 증거: 28건 (조건별)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 이번 세션에서 전 조건 직접 재실행(zsh 기본 + SC-03 bash 명시 확인). ci-local.sh 는 백그라운드 실행 완료까지 대기 후 rc 확인
- 양성 대조: SK-03(2가지 변이 직접 재현, 둘 다 rc=1·4 failed), SC-02(m1~m4 직접 재현), SC-05(round2 확인 유지, 이번 라운드 관련 파일 미변경 diff 확인), DG-02(round2 FAIL → round3 PASS 전환을 직접 재현해 "정상 동작하는 검사"임을 확인)
- DG-02 는 이전 라운드 REJECT 사유였던 실제 위반(3건)이 이번 라운드 수정 커밋으로 사라진 것을 직접 실행으로 재현 확인 — 공허한 0 이 아님

## Summary
- Total: 26/26 유효 조건 PASS (DG-01·DG-03 은 N/A 로 총계 제외)
- Verdict: APPROVE
- 이전 라운드(Iteration 2) REJECT 사유였던 DG-02(markdownlint 위반 3건)를 커밋 `56f3356`(두 픽스처에 규칙별 disable 주석 추가)으로 해결. 재측정 결과 baseline 3파일 값 일치, 나머지 72파일 0건 확인.

## Improvement Suggestions
- [SC-02] 측정-방식-불일치 — 계약 문구를 "각 사본에서 불일치 줄로 나오는 파일 집합이 정확히 {지정 파일} 하나뿐이다"로 명확히 할지, 현재처럼 포함 여부만 요구할지 다음 계약 작성 시 결정. m1 은 전역 변이라 5개 파일 모두 영향받고, m4 는 process-thin-unreadable-slot.json 에도 부수 영향을 준다.
- [DG-02] 범위-미명시 — "이번에 바뀐 .md 파일마다"의 범위에 테스트 픽스처(의도적으로 비표준 마크다운을 담는 음성 입력 파일)를 포함할지 다음 계약 작성 시 명시. 이번 라운드는 규칙별 disable 주석으로 해결했으나, 향후 유사 사례를 위해 픽스처 작성 시 markdownlint 사전 검증을 구현 체크리스트에 추가 권장.
- [맡길 곳 없는 12개 항목] 계약 범위 밖 — remaining.md 의 A1·A2·A3·B12~B20·D1·D3 은 이 계약을 포함해 확인된 네 작업 폴더(ak3-ex·ak3-h1·ak3-h2·ak3-k1) 어느 계약에도 없다. 부모 세션이 배정을 결정해야 한다 (계약 「교차 진단 반영」 절과 k1 notes 에 이미 표면화됨).

## References
- 측정 로그 원본: 이번 세션의 Bash 실행 출력 (커밋되지 않음, 리포트에 근거로 인용)
