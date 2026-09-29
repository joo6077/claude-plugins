# Sprint Feedback
Feature: 마지막 정리 — 규칙 · 코드 · 시험 (fs1)
Evaluated: 2026-09-29 11:07
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-fs1/.harness/sprint-contract-after-0929-final-sweep-rules.md
- sha256: ba277cd85f9fe8d43ba52bc55d374ff8e09c204c251925aec9e7486d34abff24
- status: active
- slug: after-0929-final-sweep-rules
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-fs1
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출자가 계약 경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- measure_status: MEASURE_OK
- 봉인 커밋 대조: seal_commit=1e003eb0 files=1 (계약 파일 단독). 봉인 뒤 산문·지문 차이 0줄 — 조용한 재봉인 없음
- 재확인(Step 5): 일치
- status_transition: active -> done (본 리포트 저장 뒤 전환)

## Amendments
- amendments: 0 (사이드카 파일 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (스프린트 기간 10:23~ 사용자 발언 없음 — 로그된 항목은 다른 계약의 교차 진단 배치 완료 알림뿐이었다)
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: cacd9da3..93ab618d (TIP)
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-fs1/.harness/sprint-contract-after-0929-final-sweep-rules.md` · 본 리포트 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중 공허한 통과가 있는가? $M/ 아래 새 측정 스크립트 6 종에 규칙 10 의 다섯 가지(특히 ① 첫 칸만 읽기 · ② 표에만 올린 시험) 가운데 evaluator 가 짧게만 확인하고 넘긴 지점이 있는가?
- cross_diagnosis_by: pending-parent

## Results

### Skill (10/10)
- [x] 스킬-01: search-strategy.md 역방향 금지 문단 「안내」로 전환 + 레포 전체 재권장 주장 0 — PASS
  - 근거: `onboarding-kit/skills/setup-guide/references/search-strategy.md:88` 새 문구 「`.p8` 을 안내한다는 사실로부터 `.p8` 권장이나 `.p12` 의 deprecation 을 추론하지 마라」 확인(L3). `bash $M/texts.sh $PWD` → `ss_old=0 ss_new=1 repo_p8_recommend=0`. `git grep -nE '\.p8.{0,20}(을|를) ?권장한다' -- . ':!.harness' ':!docs/kaizen/research-log.md'` rc=1(매치 0) 직접 재확인. 양성 대조 BASE `ss_old=1 ss_new=0 repo_p8_recommend=2` 일치
- [x] 스킬-02: docs/onboarding-kit/search-strategy.html 407·474행 동기화 — PASS
  - 근거: `docs/onboarding-kit/search-strategy.html:407,474` Read로 새 문구 두 곳 글자 그대로 확인(L3). `texts.sh` → `sh407_old=0 sh407_new=1 sh474_old=0 sh474_new=1`
- [x] 스킬-03: evals.json 67행 설명 좁힘 + JSON 유효 — PASS
  - 근거: `onboarding-kit/skills/setup-guide/evals/evals.json:67` Read로 「Firebase iOS 설정 문서는 APNs 인증 키 업로드만 지시하고」 확인. `python3 -c "import json; json.load(...)"` 성공. `texts.sh` → `ev_old=0 ev_new=1 ev_json=ok`
- [x] 스킬-04: design-mockup SKILL.md 참조 줄 갱신 — PASS
  - 근거: `design-kit/skills/design-mockup/SKILL.md:203` Read로 「§5.6 Variant Budget · §3.8 User-Reported Failure Gate — 개수 규칙·부대 산출물 금지·사용자 보고 규약의 기준 원본」 글자 그대로 확인. `texts.sh` → `dm201_old=0 dm201_new=1`
- [x] 스킬-05: skill-design-guide.md + html 두 곳 승인 경로 문장 — PASS
  - 근거: `harness/docs/guides/skill-design-guide.md:806`, `docs/harness/skill-design-guide.html:1143` 두 곳 모두 「시안 밖 산출물의 4 개 이상도, 3 축 변주도」 확인. `texts.sh` → `sg_old=0 sg_new=1 sgh_old=0 sgh_new=1`
- [x] 스킬-06: contract-schema.md §측정 관례 절 안 세 문장 — PASS
  - 근거: `harness/references/contract-schema.md:1142,1143,1144` Read로 세 굵은 머리 문장 + 같은 줄 낱말(`git grep`/`슬라이서`/`xargs`·`배열`) 전부 확인, 절 경계(1099~1170) 안. `texts.sh` → `cs_l1=1 cs_l2=1 cs_l3=1 cs_file_l1=1 cs_file_l2=1 cs_file_l3=1`. 알려진 답 대조(절 안/밖 사본)는 계약에 이미 기록된 실측과 일치
- [x] 스킬-07: docs/harness/contract-schema.html #measure-habits 절 동기화 — PASS
  - 근거: `docs/harness/contract-schema.html:1254-1256` `<strong>` 세 문장 + 같은 줄 낱말 확인. `texts.sh` → `ch_l1=1 ch_l2=1 ch_l3=1 ch_file_l1=1 ch_file_l2=1 ch_file_l3=1`
- [x] 스킬-08: 여섯째 시안 CSS 안내 두 곳 — PASS
  - 근거: `design-kit/skills/design-mockup/SKILL.md:115`, `docs/design-kit/design-mockup.html:570` 둘 다 `grid-auto-flow: column` 설명 확인. `texts.sh` → `dm_six_css=1 dp_six_css=1`
- [x] 스킬-09: users.me.yaml 비교 기준값 블록 — PASS
  - 근거: `api-kit/evals/fixtures/unjudged/.api/contracts/users.me.yaml` baseline 블록 Read 확인(state: pending, 5키 전부 ALLOWED 9종 안). `python3 $M/api-baseline.py $PWD` → `block=1 state=pending nd=1 media=1 mode=1 lineage=1 extra=[] others=0` 종료 코드 0. 다른 4 계약(auth.token 등) 미수정 직접 확인(git diff 0)
- [x] 스킬-10: bambu 시험 파일 벽 예산 값 + 표 두 곳 동기화 — PASS
  - 근거: `bambu-kit/evals/gate-fixtures/process-thin-unreadable-slot.json` `_wall_budget_short_share: "0.00"` 확인. `bash $M/bambu-nosl.sh $PWD` 셋째 줄 `thin-unreadable fails=1 unv=1 wall=0 rc=1`. 표 두 곳(`bambu-kit/skills/bambu-print-profile/SKILL.md:1938`, `docs/bambu-kit/bambu-print-profile.html:1722`) 「`[미검증]` 1 줄 (슬롯 1)」 확인. **음성 대조 직접 실행**: 표는 새 값 유지, 시험 파일만 BASE로 되돌린 임시 사본에서 `bash bambu-kit/evals/run-gate-fixtures.sh` → 「`불일치 process-thin-unreadable-slot.json — `[미검증]` 기대 1 줄 · 결과 2 줄`」 + 끝줄 「결과: 28 경우 중 불일치 1」 계약 기재값과 정확히 일치(판별력 확인 — 조건이 실제 구현을 경유함)

### Script (6/6)
- [x] 스크립트-01: mockup.html 그리드 — PASS
  - 근거: `node $M/grid-rows.js design-kit/templates/mockup.html` 여섯 줄 전부 계약 지정 문자열과 글자 그대로 일치, 종료 코드 0
- [x] 스크립트-02: 비교 이름표 시험 — PASS
  - 근거: `design-kit/evals/visuals.spec.js:1208` `test('비교 화면 왼쪽에 f 를 고르면...')` 확인. `bash $M/spec-neg.sh $PWD $TIP none` → `rc=0 failed=0 passed=2`. 음성 대조 `label` 모드 → `applied=1 rc=1 failed=1`
- [x] 스크립트-03: 한 줄 배치 시험 — PASS
  - 근거: `design-kit/evals/visuals.spec.js:1221` `test('1280 폭에서...각각 한 줄에 놓인다')` 확인. 음성 대조 `oldgrid` 모드 → `applied=2 rc=1 failed=1`
- [x] 스크립트-04: ci-local.sh UNSUPPORTED 라우팅 — PASS
  - 근거: `bash $M/ci-scope.sh scripts/ci-local.sh` 4개 구간(job/wf-env/wf-defaults/plain) 전부 계약 지정 줄과 일치, `FAIL ` 줄 0. 양성 대조(BASE ci-local.sh)에서 `FAIL a Where rc=1` 등 재현
- [x] 스크립트-05: test-ci-local.sh 새 시험 — PASS
  - 근거: `bash scripts/test-ci-local.sh` → `PASS` 6줄 · `FAIL` 0줄 · rc=0. `CI_LOCAL=<BASE사본> bash scripts/test-ci-local.sh` → `FAIL` 4줄 · rc=1 (신규 시험이 옛 도구를 실제로 구분함을 확인)
- [x] 스킬/스크립트-06: 전체 CI + 옛 도구 + 슬라이서없는사본 — PASS
  - 근거: (a) `bash scripts/ci-local.sh $PWD` 실제 실행(백그라운드 완주 대기) → `steps=44 run=39 skip=5 unsupported=0 failed=0` 종료 코드 0. 지정된 6개 named PASS 라인(api-kit docs check·Docs drift mapping check·Cause table copy check·Bambu-kit gate fixtures·Run Playwright tests·Api-kit viewer test) 전부 로그에서 직접 확인 (b) `bash .harness/handoff/.../ci-local.sh $PWD` summary.txt → rc=0 아닌 줄 0(SKIP 1종만) (c) `bash $M/bambu-nosl.sh $PWD` → `here 결과: 불일치 0`, `noslicer 결과: 불일치 0 · 건너뜀 20 rc=0 left_paths=0`

### Error (1/1)
- [x] 오류-01: CI 파일 없음/빈 jobs/jobs 없음 3경우 종료 코드 2 — PASS
  - 근거: 세 scratch 폴더(`none/`, `bad1/`, `bad2/`) 직접 생성 후 `bash scripts/ci-local.sh --list <폴더>` 실행 → 셋 다 rc=2, `steps=` 줄 0

### Architecture (3/3)
- [x] 구조-01: 커밋 구조(병합0·단일폴더·서명줄) — PASS
  - 근거: `git rev-list --merges cacd9da3..TIP` 0줄. 10개 커밋 전수 루프로 폴더수=1·서명줄=1 확인, BAD 0건. 양성 대조: 병합커밋 `01b1cace` 서명0, `a5152c5` 폴더수17
- [x] 구조-02: 범위 밖 변경 0 — PASS
  - 근거: `comm -23` 결과 0줄. 양성 대조(`a5152c5~1..a5152c5`) 17줄
- [x] 구조-03: 문서 페이지 5개 CSS링크+a11y — PASS
  - 근거: 5개 파일 각각 `href="../assets/site.css"` count=1. `node scripts/check-docs-a11y.js` 5개 파일 지정 → 전부 `OK ... of=0/0/0/0`, 마지막줄 `5/5 PASS`, 종료 코드 0

### Anti-patterns (2/2)
- [x] 금지-03: bare code fence — PASS (`python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 14개 플러그인 전부 OK)
- [x] 금지-04: frontmatter name 필드 — PASS (`python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0)

### Reusability (2/2)
- [x] 재사용-01: 시안 틀 도우미 단일화 — PASS
  - 근거: `grep -cF "...mockup-vote-card...castVote('e')..." design-kit/evals/visuals.spec.js` = 1. `buildMockupWithVariants()` 함수(라인 1117)가 6개·8개 시안 시험 양쪽에서 재사용됨을 코드 경로로 직접 확인(L3)
- [x] 재사용-02: ci-local.sh 단일 읽기 — PASS (`grep -c 'yaml.safe_load' scripts/ci-local.sh` = 1)

### Diagnostics (2/2, N/A 2)
- [ ] 진단-01: N/A (측정: `git diff --name-only cacd9da3 TIP | grep -c '^scripts/release.sh$'` = 0, 사유 사실 확인됨)
- [x] 진단-02: markdownlint 5개 md + shellcheck 2개 sh — PASS
  - 근거: scratch에 `markdownlint-cli2@0.23.2` 정확 버전 설치(계약 지정) 후 5개 md 파일 전부 warnings=0 rc=0. `shellcheck scripts/ci-local.sh scripts/test-ci-local.sh` rc=0. 양성 대조: 나쁜 헤더 줄 삽입한 사본에서 `MD018` 위반 1건·rc=1 확인(패턴 유효성 검증)
- [ ] 진단-03: N/A (변경 파일 전부가 스크립트-02·03·05·06이 직접 측정하는 대상과 일치, release.sh 무관 사실 확인됨)
- [ ] 진단-04: N/A (git diff로 확인한 변경 파일 24개 전부 문서/설정/시험 파일 — 구동할 앱·서버 코드 0건 확인됨)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (28 - 0) / 28 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (전 조건 실측 완료, [미검증] 마커 없음)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 28개 조건 전부 문서 원문 대조·스크립트 종료 코드/출력 매칭·커밋 구조 검사이며 동시성/인증/멱등성/데이터유실/마이그레이션/재시도/보안경계/사용자결함보고 9항목에 해당하는 조건이 없음
- 스킬-10 은 9항목 해당은 아니나 계약 자체가 음성 대조를 명시해 evaluator가 직접 실행 재현함(위 근거 참조)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: $M/ 아래 신규 측정 스크립트 6종(texts.sh·ci-scope.sh·bambu-nosl.sh·grid-rows.js·spec-neg.sh·api-baseline.py) — 대부분의 조건 PASS가 이 출력에 의존
- ① 첫 칸만: texts.sh는 25개 이상 독립 플래그를 각각 별도 grep으로 산출(코드 Read로 확인, `both()` 헬퍼가 필드별 독립 호출) — 순차 중단 구조 아님을 코드 경로로 확인
- ② 실행 목록: 스크립트-02/03 신규 시험명(「비교」·「한 줄」)이 `npx playwright test design-kit/evals/visuals.spec.js` 전체 실행(스크립트-06(a) CI 경로)에 포함되어 실제로 돎을 확인. spec-neg.sh 자체도 passed=2 로 두 시험 모두 실행 확인
- ③ 못 읽는 칸 + 실제 위반: 스킬-10 음성 대조로 직접 재현 — 기대 1줄·결과 2줄 불일치 정확히 검출
- ④ zsh · bash: texts.sh·ci-scope.sh·bambu-nosl.sh 3종을 zsh·bash 양쪽 직접 실행, md5 동일 확인
- ⑤ 효과 증명: 전 스크립트에서 계약이 명시한 양성/음성 대조(BASE값·손으로 구성한 나쁜 사본)를 evaluator가 직접 재현하여 계약 기재값과 일치 확인

## Evidence Validity
- 검사 대상 증거: 28건 (전 조건)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 28건 · zsh/bash 양쪽 확인 3건(측정 스크립트) · 미실행 0건
- 양성 대조: 스킬-01(repo grep rc=1) · 구조-01(01b1cace·a5152c5) · 구조-02(a5152c5~1) · 구조-03(계약 기록 인용) · 스크립트-04(BASE ci-local.sh) · 스크립트-05(BASE 도구) · 진단-02(나쁜 헤더 사본 MD018 rc=1) 등 전부 실행 확인
- 무효 0건은 미검증 카운터에 합산 없음 (현재 누계: 0)

## Summary
- Total: 26/26 conditions passed (N/A 2건은 총계·판정에서 제외, 사유 실측 확인됨) · 전체 조건수(계약 declared) 28
- Verdict: APPROVE

## Improvement Suggestions
- 없음 (계약 결함·모호성·측정-방식-불일치 미발견)
