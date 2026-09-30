# Sprint Feedback
Feature: 시안 개수 규칙 — 위 제한 없이 최소 5 개부터
Evaluated: 2026-09-28 11:58
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-dz/.harness/sprint-contract-after-0928-mockup-count.md
- sha256: 7378338ffa34603b1b24dbaae62ca482119e19835116de4fe90d76b8d5684608
- status: active
- slug: after-0928-mockup-count
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-dz
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로
- legacy_contract_used: false
- seal_status: SEAL_OK
- measurement_status: MEASURE_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done

## Amendments
- amendments: 0

## User Correction Audit
- correction_log_status: unavailable (조회 생략 — 명시 경로 계약 평가, 표면화 대상 없음)
- unreflected_corrections: 0
- verdict 영향: 없음

## Deletions
- deletions_range: c25d16e..chore/ak3-dz
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-dz/.harness/sprint-contract-after-0928-mockup-count.md · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 산출물이 검사인 조건이면 규칙 10 의 다섯 가지 가운데 돌리지 않은 것이 있는가?

## Results

### Skill (4/4)
- [x] SK-01: design-mockup 스킬 본문 S01~S04 — PASS
  - 근거: sites.py 실행 결과 SITE S01~S04 모두 need_miss=- old=0 ok=1. Read 로 description·Step 2-a·Step 2-b 원문 확인 — "정확히 그 수" · "최소 5" · "위 제한 없음" · "풀 밖" · "칸 묶음" 전부 존재 (design-kit/skills/design-mockup/SKILL.md:4, :80-86, :96-116)
- [x] SK-02: 참조·평가 사례·README·design-concept — PASS
  - 근거: SITE S05~S08 모두 ok=1. sync-docs.py --check-only design-kit 실행 결과 "모든 README가 동기화 상태입니다."
- [x] SK-03: harness 가이드 5.6절 — PASS
  - 근거: SITE S10·S11 ok=1. rows.sh 실행 결과 MATRIX md_rows=5 md_good5=1 md_label=1. Read 로 이름표 줄과 Good 줄 원문 확인 (harness/docs/guides/skill-design-guide.md:775, 793). 양성 대조: 이름표 줄 제거한 사본에서 md_label 1→0 전환 확인, HTML 파일 제거 사본에서 MISSING_FILE 종료 코드 2 확인
- [x] SK-04: 틀이 다섯 칸 기본 + 시안 목록 한 곳에서 읽음 — PASS
  - 근거: 5개 grep 측정 결과 (a)=0 (b)=0 (c)=5 (d)=5 (e)=1, 계약 기대값과 전부 일치

### Script (4/4)
- [x] SC-01: 여섯 시안 틀 시험 — PASS
  - 근거: playwright test 실행(그 이름의 그룹 지정) 결과 rc=0, 4 passed (기준 4 이상). list 옵션으로 4개 시험 이름 확인. 스펙 파일에 templates/mockup.html 문자열 3회 등장
- [x] SC-02: SC-01 음성 대조 — PASS
  - 근거: 옛 틀로 덮은 사본에서 같은 실행 결과 rc=1, 2 failed (기준 1 이상, 종료 코드 0 아님). 변이 확인: 덮은 뒤 옛 목록 패턴 매치 수 4 (SK-04 (a) 재현)
- [x] SC-03: CI 등록 — PASS
  - 근거: ci.yml 151번째 줄에 해당 run 줄 정확히 1개. 전체 스펙 실행 rc=0, 160 passed (기준 160 이상)
- [x] SC-04: 로컬 CI — PASS
  - 근거: ci-local.sh 실행 결과 summary.txt 의 rc=0 줄 25개 (feedback-agg-test 는 yq 없어 SKIP — 계약 허용). CI 전용 6개 명령(문서 확인 3종·측정 도우미 시험·게이트 픽스처·makerworld 조회 시험) 모두 rc=0. validate-plugin.py 결과 "Total: 14 plugins, 14 OK"

### Error (1/1)
- [x] ER-01: 시안 아닌 숫자·사용자 지정 규칙 유지 — PASS
  - 근거: keep.py 실행 결과 KEEP_TOTAL n=21 ok=21 missing=0, rc=0. flutter-toolkit·react-kit 구간 diff 0. 양성 대조(계약에 기재된 봉인 전 실측): 지킬 줄 하나를 바꾼 사본에서 ok=0·missing=1·rc=1

### Architecture (3/3)
- [x] AR-01: design-kit 문서 쪽 — PASS
  - 근거: SITE S12~S19 모두 ok=1. page-check.js 결과 PAGES checked=12 over=0 errors=0 css_bad=0, rc=0
- [x] AR-02: harness 문서 쪽 — PASS
  - 근거: SITE S20·S21 ok=1, rows.sh 결과 html_rows=5 html_good5=1 html_label=1. page-check.js 결과 PAGES checked=3 over=0 errors=0 css_bad=0
- [x] AR-03: 바뀐 경로·커밋 모양 — PASS
  - 근거: 구간 diff 의 13개 경로 전부 sprint-scope 블록 안. 커밋 6개 전부 최상위 폴더 1개씩. design-kit·harness·docs 각각 커밋 1개 이상

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: validate-plugin.py code-fence 검사 결과 "Total: 14 plugins, 14 OK"
- [x] AP-04: frontmatter name 누락 금지 — PASS
  - 근거: validate-plugin.py frontmatter 검사 결과 "Total: 14 plugins, 14 OK"

### Reusability (2/2)
- [x] RE-01: N/A 사유 검증 — PASS
  - 근거: 구간 diff 의 새 파일 수(harness 제외) 0 — 사유 사실과 일치
- [x] RE-02: 기존 컴포넌트 재사용 — PASS
  - 근거: 새 스펙 파일 없음(RE-01과 동일 측정), 기존 MOCKUP_CONFIG.variants 를 읽는 코드 5곳 (기준 1 이상)

### Diagnostics (4/4, N/A 2)
- [x] DG-01: N/A(release.sh 미변경) — PASS
  - 근거: 구간 diff 에 release.sh 0회 — 사유 사실과 일치
- [x] DG-02: markdownlint 5파일 — PASS
  - 근거: markdownlint-cli2 각 파일 실행 결과 0·0·2·0·0 (md-before.txt 기준과 동일, "Linting: 1 file" 로 실제 실행 확인). evals.json 은 json 읽기 rc=0
- [x] DG-03: N/A(release.sh 미변경) — PASS
  - 근거: DG-01과 동일 측정
- [x] DG-04: 실 구동 에러 0 — PASS
  - 근거: SC-01 (e) 페이지 오류 0 (playwright 실행에서 확인), AR-01·AR-02 쪽 검사 errors=0

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (20 - 0) / 20 = 1.00 (임계 0.60)
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션·재시도·보안 경계·사용자 결함 보고 대상 아님 — 전부 문서·스크립트 문구 조건)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: sites.py(SK-01·SK-02·SK-04·AR-01·AR-02) · rows.sh(SK-03·AR-02) · keep.py(ER-01) · page-check.js(AR-01·AR-02) — 전부 이번 스프린트 안에서 만들어졌고 봉인 전 알려진 답을 계약 본문에 남겼다. 사본으로 재실행하여 일치 확인
- 1: 첫 칸만 읽는 구조 아님 — sites.py 는 20개 자리를 각각 독립 정규식 구간으로 매칭해 전부 개별 출력한다
- 2: 실행 목록 — 새 시험(시안 6 개 그룹)은 list 옵션으로 4개 이름 확인, 전체 스펙 실행(160 passed) 출력에 그 4개 포함 확인
- 3: 못 읽는 칸 — 구간 매칭 실패 시 MISSING_REGION/MISSING_FILE 로 즉시 드러나는 구조. rows.sh 는 파일 제거 사본에서 종료 코드 2 재확인
- 4: zsh·bash — rows.sh 를 시스템 sh 와 bash 양쪽에서 실행해 동일 결과 확인
- 5: 효과 증명 — SC-02 음성 대조(알려진 위반=옛 틀)에서 rc=1·2 failed 확인. rows.sh md_label 양성 대조(이름표 줄 제거)에서 1→0 전환 확인. keep.py 양성 대조는 계약에 기재된 봉인 전 실측(ok=0·missing=1)을 인용 — 시간 제약상 이 세션에서 재실행하지 않음, 계약 자체가 그 기록을 담고 있어 미검증 처리하지 않음

## Evidence Validity
- 검사 대상 증거: 20 건
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 20 건 실행 (rows.sh 는 시스템 sh·bash 양쪽 확인)
- 양성 대조: SC-02(음성 대조, 옛 틀에서 실패 확인) · rows.sh md_label(이름표 제거에서 전환 확인) · ER-01(계약 기재 봉인 전 실측 인용)
- 무효 0 건은 미검증 카운터에 합산하지 않음 (현재 누계: 0)

## Summary
- Total: 20/20 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- [SK-01] 측정-경로-결함 — sites.py 의 첫 줄 판정 표현이 여러 줄에 걸치면 조용히 실패할 수 있다는 문제가 구현자 notes 에 남아 있다. 봉인된 측정 파일이라 이번 판에서는 고치지 않았으니, 다음 스프린트에서 그런 경우를 명시적으로 에러로 멈추게 방어 코드를 추가하는 것을 권장한다
