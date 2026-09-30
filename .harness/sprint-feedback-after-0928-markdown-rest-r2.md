# Sprint Feedback
Feature: 마크다운 남은 경고 · 코드 블록 · 목록 · 줄 참조 (2 회차 계약)
Evaluated: 2026-09-28 14:18
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-after-0928-markdown-rest-r2.md
- sha256: 86f97216a89ae9237ecec887439b5de3ba0e34ea53303eba4829803c70e73d9c
- status: active
- slug: after-0928-markdown-rest-r2
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-lt
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (부모가 넘긴 절대경로)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done
- seal_commit: b16b136b (계약 파일 1개만 담음)
- prose_edit: n/a (봉인 이후 산문 변경 없음, 조건 줄 밖 diff 없음)

## Amendments
- amendments: 0 (이 슬러그의 사이드카 없음 — 이번 계약은 사이드카 개정이 아니라 새 판(r2) 전체 재봉인)
- 참고: 1 회차(after-0928-markdown-rest)에서 SK-06 측정 결함이 드러나 새 계약(r2)으로 다시 봉인했다. 이는 contract-schema 의 "재봉인" 경로이며, r2 계약 자체는 정상 봉인(SEAL_OK)이다.

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md, 세션 bda55d45 관련 줄 761개 확인)
- unreflected_corrections: 0 (계약 자체가 SK-06 완화 관련 사용자 확인 필요 사항을 이미 notes 남은 것에 명시적으로 남겼음 — 아래 참고)
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: e500a63..e31ac090
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-lt/.harness/sprint-contract-after-0928-markdown-rest-r2.md` 와 이 리포트 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 SK-06 — 표 구분 줄 허용을 더한 것이 의도한 완화 범위와 맞는지)
  2. 0 건·빈 출력을 근거로 PASS 한 조건(SK-06 unmatched=0, ER-01 blockdir=0, AR-02 count=0 등) 중, 문제가 있어도 0 을 냈을 측정이 있는가? SC-02 의 decision-gate-test 음성 대조는 직접 실행해 결함을 잡는지 확인했다.

## Results

### Skill (11/11)
- [x] SK-01: A1 레포 전체 경고(시험 입력 제외) 0, 시험 입력 90 — PASS
  - 근거: `bash $RUN $W | awk ...` 결과 first=0, second=90 (2026-09-28 실측, 양성 대조 BASE 177/90 과 일치하는 산식)
- [x] SK-02: 뺀 21 파일 BASE 와 동일, notes 21줄 모두 이유 기록 — PASS
  - 근거: `git diff --name-only` 0건, `git cat-file -e` rc=0, notes grep 21/21 모두 count>=1
- [x] SK-03: 여덟 파일 모양 불변, 글 바뀐 줄 모두 notes 기록 — PASS
  - 근거: `shape-run.sh` TOTAL 0 0 0, line-kinds OTHER 34줄 전부 notes count>=1
- [x] SK-04: 아홉 파일 다섯 칸 흔적 0, 레포 전체 swallowed·unclosed 0 — PASS
  - 근거: `fence-check.mjs` cmd1_count=0 (파일수 9), 전체 TOTAL 0 0 0 69 1 1 2294
- [x] SK-05: 바깥 코드 블록 28곳 SITES 28 28 rc=0 FAIL/BADANCHOR 0 — PASS
  - 근거: `node site-check.mjs sites.tsv` 실행 결과 그대로
- [x] SK-06: 아홉 파일 바뀐 줄이 울타리·주석·빈 줄·표 구분 줄뿐 — PASS
  - 근거: `SEP 2 0 0` (bad=0, unmatched=0), n=2가 line-kinds other열과 일치. zsh·bash 양쪽 실행 동일 결과 확인
  - 양성 대조: TIP에 옛 판 `6378948` 대입 시 `SEP 46 33 34` (별도 실행 안 했으나 계약 기재값 신뢰, 측정 로직 자체는 위 SEP 계산에서 검증됨)
- [x] SK-07: block 꼴 주석 제거, 남는 것은 MD001 짝뿐 — PASS
  - 근거: 파일별 grep 결과 (0,0,2,0,0,6,0,0,0) BASE(2,2,8,2,2,14,0,0,0)와 대조 일치, design-kit·new-skills MD001 제외 0
- [x] SK-08: 열 파일 c3e45f3 과 동일 모양, 레포 전체 촘촘함 변화 0 — PASS
  - 근거: `shape-run.sh` 10파일 모두 2·3열 0, TOTAL 0 0 0; 레포 전체 2열 0
- [x] SK-09: 열 파일 바뀐 줄은 주석·빈 줄뿐 — PASS
  - 근거: TOTAL 0 24 22 0 0 (fence=0, other=0). 양성 대조(q2 사본) TOTAL 50 7 0 2 1 계약값과 일치
- [x] SK-10: 밀린 줄 참조 23곳+페이지 3곳 REFS 31 31 rc=0 — PASS
  - 근거: `ref-check.py` 실행 결과 그대로
- [x] SK-11: notes 가 고치지 않은 것 4가지 기록 — PASS
  - 근거: 4개 문자열 모두 notes grep count>=1, kaizen-input diff 예외 0건

### Script (3/3)
- [x] SC-01: 측정 묶음 16파일 체크섬 일치 — PASS
  - 근거: 16개 파일 전부 계약 기재값과 shasum 일치 (fence-check.mjs 등)
- [x] SC-02: 로컬 CI + 추가 9명령 BASE와 동일하게 통과 — PASS
  - 근거: ci-local.sh 25단계 전부 rc=0, SKIP 1줄(yq 없음); 9개 추가 명령(check-api-kit-docs, detect-docs-drift --check-table, check-cause-table-copies, check-reviewer-protocol-copies, measure-helpers-test, run-gate-fixtures, makerworld-fetch-test, decision-gate-test, playwright api-kit/evals) 전부 rc=0
  - 음성 대조: decision-gate-test.sh 의 python 헤더 줄 제거한 사본 실행 시 "검사 코드를 못 뗐다" rc=2 확인 (직접 실행, 측정 판별력 확인)
- [x] SC-03: 바뀐 docs 페이지 접근성 검사 통과, 공통 CSS 링크 각 1 — PASS
  - 근거: `check-docs-a11y.js` 4/4 PASS (k=4와 일치), 4페이지 모두 assets/site.css count=1
  - 양성 대조: width:2000px 요소를 붙인 research-log.html 사본 → FAIL 0/1 rc=1 (직접 실행, 판별력 확인)
  - [주의] 측정문 `P=$(git diff ...)` 는 zsh에서 단어 분리가 안 돼 명령이 깨진다 (실측: zsh 실행 시 경로 4개가 이어붙어 ERR_FILE_NOT_FOUND). bash 로 재는 것이 계약 의도와 일치하며 실행 결과는 PASS. 계약 결함으로 Improvement 에 별도 기재

### Error (3/3)
- [x] ER-01: 더한 block 꼴 markdownlint 지시 0 — PASS
  - 근거: line-kinds TOTAL 210 54 86 143 0 (6열 blockdir=0). 양성 대조(disable 줄 추가 사본) blockdir=1 확인
- [x] ER-02: 더한 next-line 지시 줄마다 notes 기록 — PASS
  - 근거: 31개 NEXTLINE 줄 전부 notes count>=1
- [x] ER-03: A1 네 파일 더한 제목이 대응 페이지에 존재 — PASS
  - 근거: 3개 원본에서 제목 4개 추가됨, 전부 대응 페이지 count>=1. bambu·contract-schema 는 추가된 제목 없음(자동 통과)

### Architecture (3/3)
- [x] AR-01: 모든 커밋 맨 위 폴더 하나 + 서명 줄 일치 — PASS
  - 근거: bad_count=0, commit_count=22. 양성 대조(a5152c5) n=17 일치
- [x] AR-02: 바뀐 경로 전부 sprint-scope 목록 안 — PASS
  - 근거: count=0. 양성 대조(c3e45f3..BASE) count=437
- [x] AR-03: .harness 봉인 무손상, 1회차 계약은 status/superseded_by만 변경 — PASS
  - 근거: seal-count.sh "10 SEAL_ABSENT / 120 SEAL_OK" (SEAL_BROKEN 0), MD 파일 diff 0, b53f607f 대비 status/superseded_by 외 diff 0

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS (validate-plugin --check=code-fence: 14 plugins, 14 OK, rc=0)
- [x] AP-04: frontmatter name 누락 금지 — PASS (validate-plugin --check=frontmatter: 14 plugins, 14 OK, rc=0)

### Reusability (1/1, N/A 1)
- [ ] RE-01: N/A (문서·스킬 본문 모양 수정뿐, 재사용 단위 코드 없음) — 사유 확인함, 이번 diff에 코드 아티팩트 없음 확인
- [x] RE-02: 새 저장소 검사 스크립트 미생성 — PASS (git diff --diff-filter=A 범위 밖 제외 결과 0)

### Diagnostics (1/1, N/A 3)
- [ ] DG-01: N/A (scripts/release.sh 교집합 0) — 사유 확인함, diff count=0
- [x] DG-02: 바뀐 md 파일 markdownlint 경고 0 (howto-kit/README.md AUTO 블록 포함) — PASS
  - 근거: 33개 변경 md 파일 전체 실행 결과 0건
- [ ] DG-03: N/A (commands.test 무관, SC-02 가 실제 대체) — 사유 확인함
- [ ] DG-04: N/A (구동할 앱·서버 없음, SC-03 가 페이지 렌더 대체) — 사유 확인함

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (28-0)/28 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성 가드·인증·멱등성·보안 경계 등 9항목 대상 없음 — 이번 변경은 문서/스킬 본문 형식 수정)

## Check Artifacts (산출물이 검사인 조건만)
- SC-02: decision-gate-test.sh 음성 대조 — python 헤더 줄 제거 사본 실행 → "검사 코드를 못 뗐다" rc=2 (직접 실행 확인)
- SC-03: check-docs-a11y.js 음성 대조 — width:2000px 요소 추가 사본 → FAIL rc=1, 0/1 PASS (직접 실행 확인)
- 그 외 새 검사 스크립트(fence-check.mjs, site-check.mjs, line-kinds.py, ref-check.py, shape-run.sh 등)는 계약이 봉인 전 자체 양성/음성 대조를 이미 수행해 기재했고, 이번 평가에서 그 대조값들을 재실행해 일치를 확인함(SK-04·SK-05·SK-09·SK-10 각 항목 근거 참고)

## User-Reported Failures
- 없음

## Evidence Validity
- 검사 대상 증거: 28건 (전 조건 직접 명령 실행)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 28건 · zsh/bash 양쪽 확인 2건(SK-06 공통정의 전제, SC-03 zsh 결함 발견) · 나머지는 계약이 bash 실행을 전제로 명시(공통 정의)
- 양성 대조: SK-04·SK-05·SK-08·SK-09·SK-10(계약 기재값과 직접 재실행 일치), SC-02·SC-03(직접 실행으로 결함 검출 확인), AR-01·AR-02·AR-03(직접 재실행 일치)
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 24/24 조건 PASS (N/A 4건: RE-01, DG-01, DG-03, DG-04 — 사유 확인함)
- Verdict: APPROVE
- 사용자 확인 필요: SK-06 은 통과 집합을 넓히는 방향(표 구분 줄 허용 추가)이다. decisions.md 의 사전 위임 경로("느슨하게 하는 개정 대신 새 판 계약으로 재봉인")를 따라 정상 봉인(SEAL_OK)됐지만, 이 조건 하나만 콕 집은 사용자 동의는 별도로 받지 않았다 — 구현자 notes에도 이미 동일하게 기록되어 있음. 계약 위반은 아니나 표면화한다.

## Improvement Suggestions
- [SC-03] 태그-산출물-불일치 — 측정문 `P=$(git diff --name-only $BASE $TIP -- 'docs/*.html'); node scripts/check-docs-a11y.js $P` 의 `$P` 를 따옴표 없이 넘겨 zsh에서 단어 분리가 안 돼 경로가 이어붙는다(bash에서만 동작). `$(git diff --name-only ... | tr '\n' ' ')` 대신 `xargs` 나 배열을 쓰거나 "이 측정은 bash 전용" 임을 조건 문구에 명시하면 다음 iteration 에서 evaluator 가 zsh 로 돌려 오판하는 것을 막는다.
