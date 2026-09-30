# Sprint Feedback
Feature: 마지막 — Mermaid 예시 세기 · check-superseded 안내
Evaluated: 2026-09-30 12:08
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-last/.harness/sprint-contract-after-0930-last.md
- sha256: bd3647fd38c4d747446debb6e16b65f35ce76989575722f720a69f9fe55c8b40
- status: active
- slug: after-0930-last
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-last
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 지정된 경로, test -f 로 존재 확인 후 채택)
- legacy_contract_used: false
- seal_status: SEAL_OK (주의: 설치된 플러그인 캐시 harness 0.16.0 의 §계약 봉인 정규식은 영문 ID 전용이라
  이 계약(한글 조건 ID)에 적용하면 SEAL_BROKEN 오탐이 남. 워크트리 자신의 harness/references/contract-schema.md
  (한글 ID 지원 정규식 `([A-Z]{2,}|[가-힣]+)-[0-9]{2}`, sprint-contract 스킬의 Step 6.6/6.7 이 실제로 쓰는 것과 동일)
  로 재계산하여 SEAL_OK 확정. 이 워크트리는 harness 자체를 아직 릴리스 전 상태로 고치는 중이라
  "harness 레포 자체" 가 "설치된 플러그인" 보다 최신인 특수 상황 — Step 1-e-2 의 경로 ladder 순서를
  기계적으로 첫 항만 적용하면 자기 자신을 평가할 때 오판을 낸다)
- contract_seal_broken: n/a
- measure_status: MEASURE_OK (같은 사유로 워크트리 정규식 재계산)
- 재확인(Step 5): 일치
- status_transition: active -> done (Step 5.5 에서 전환 — 아래 실행)

## 봉인 커밋 대조 (Step 1-e-3)
- seal_commit: 7d156456 (files=1, 계약 파일 단독)
- 산문 diff (조건 줄·status 전환 제외): 없음
- 지문 필드(conditions_digest/measurement_digest) 변화: 없음
- reseal_detected: false

## Amendments
- amendments: 0 (사이드카 sprint-amendments-after-0930-last.md 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (스프린트 구간 2026-09-30 11:01~11:37 동안 세션 bda55d45 의
  [prompt] 항목 없음 — tool-failure 기록만 있고 이는 도구 실행 로그이지 사용자 교정 발언이 아님.
  동일 시간대의 [prompt] 2건(11:10, 11:24)은 다른 세션 97f28e34, 다른 작업 폴더(flutter-scenario-report)의 것)
- verdict 영향: 없음

## Deletions
- deletions_range: 0928bf65..chore/ak3-last
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-last/.harness/sprint-contract-after-0930-last.md` · 이 판정 결과 전문 (verdict=APPROVE, 23/23 PASS, N/A 3건)
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 스킬-01의 "알려진 답" 대조가 chore/ak3-cx 스크립트 실제 출력과 안내 문구를 올바르게 맞댔는지)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? (구조-03 ext_files=0, 진단-01/03/04 의 grep -c 0 등)
- 부모가 교차 진단을 마친 뒤 cross_diagnosis_by 를 sprint-contract 로 갱신한다.

## Results

### Skill (2/2)
- [x] 스킬-01: check-superseded 안내가 새 출력 모양을 적는다 — PASS
  - 근거: harness/skills/sprint-contract/SKILL.md:357-373 (안내 덩어리) 에 UNREADABLE <계약> / UNREADABLE <계약> -> <새 판> / unreadable= / checked= / violations= / 종료 코드 2 / 못 읽 및 기존 MISSING_BY · MISSING_TARGET · CHAIN · 종료 코드 0 모두 존재 (369-372줄 직접 Read 확인).
  - 재측정: `m 스킬-01` → `block=357-373 cx_rc=2,0 cx_heads=OK,UNREADABLE cx_keys=checked,unreadable,violations known_ok=1 miss=[] ok=1`, 종료 코드 0 (evaluator 직접 실행 재현, 사용자 보고값과 일치). 알려진 답: git show chore/ak3-cx:harness/scripts/check-superseded.sh 머리 주석(1-9줄) 직접 Read 로 MISSING_BY/MISSING_TARGET/CHAIN/UNREADABLE 어휘 확인.

- [x] 스킬-02: 스킬 파일은 안내 덩어리 밖이 그대로다 — PASS
  - 근거: `git diff -U0 0928bf65..chore/ak3-last -- harness/skills/sprint-contract/SKILL.md` 직접 실행 → 덩어리 1개, 370줄 범위(357-373 안) 한정.
  - 재측정: `m 스킬-02` → `hunks=1 outside=0 ok=1`, 종료 코드 0.

### Script (4/4)
- [x] 스크립트-01: 그림 종류 이름 오타 예시를 안 그려짐으로 잡음 — PASS
  - 재측정: `m 스크립트-01` → 3개 사본(flows-typo/ref-typo/flows-front-typo) 모두 `OK` rc=1, `cases=3 right=3 ok=1`, 종료 코드 0. tail 값도 사용자 보고(예시 4·3·4, 안 그려진 예시 각 1)와 일치.
- [x] 스크립트-02: 머리말 붙은 정상 예시는 그려진 예시로 셈 — PASS
  - 재측정: `m 스크립트-02` → 2개 사본(flows-front/ref-front) 모두 `OK` rc=0, `cases=2 right=2 ok=1`, 종료 코드 0.
- [x] 스크립트-03: 세지 말아야 할 pre 는 여전히 안 세고 레포 전체 수 그대로 — PASS
  - 재측정: `m 스크립트-03` → `rc=0 tail=[쪽 3 · 예시 9 · 안 그려진 예시 0] repo_ok=1 shell_rc=3 shell_ok=1`, 종료 코드 0.
- [x] 스크립트-04: 시험이 두 모양을 실패 경우로 갖고 CI 이름이 맞음 — PASS
  - 근거: scripts/test-check-docs-mermaid.js 직접 Read → 경우 5~8 존재(9-12줄), CASES 배열에 5개 신규 경우(57-72줄) 코드로 확인. .github/workflows/ci.yml:195-196 직접 grep → `node scripts/test-check-docs-mermaid.js` 정확히 1회, npm ci(171줄) 뒤 위치, 이름에 "여덟 경우" 포함.
  - 재측정: `m 스크립트-04` → `test_ok=1 base_rc=1 base_fails=5,6,7 base_ok=1 stub_ok=1 head_ok=1 ci_ok=1`, 종료 코드 0. 음성 대조: 시작 판 검사 사본은 경우 5·6·7 만 FAIL(base_fails=5,6,7), 늘 0 내는 가짜 검사는 stub_rc=1 로 잡힘 — 판별력 있는 측정 확인.

### Error (2/2)
- [x] 오류-01: 이름표 붙은 빈 예시는 안 그려진 예시로 셈 — PASS
  - 재측정: `m 오류-01` → `rc=1 tail=[쪽 1 · 예시 2 · 안 그려진 예시 1] ok=1`, 종료 코드 0.
- [x] 오류-02: 앞 묶음 tail 의 Mermaid 측정이 이 판에서도 통과 — PASS
  - 재측정: `m 오류-02` → `tail_rc=0 ok=1`, 종료 코드 0. broken_applied=1 broken_rc=1(괄호 깨진 사본은 실패 재현 — 판별력 확인).

### Architecture (5/5)
- [x] 구조-01: 규약 문서와 쪽이 못 읽는 경우를 같이 적음 — PASS
  - 근거: harness/references/contract-schema.md:268, docs/harness/contract-schema.html:466 직접 Read → 둘 다 UNREADABLE·종료 코드 2 포함, 인라인 코드 집합 동일.
  - 재측정: `m 구조-01` → `md_need_ok=1 page_need_ok=1 codes_only_md=[] codes_only_page=[] codes_same=1`, 종료 코드 0.
- [x] 구조-02: 바뀐 docs 쪽 두 테마 320/375/1280 폭 가로 넘침 0 — PASS
  - 근거: `git diff --name-only 0928bf65..HEAD -- docs` → 2개 파일(contract-schema.html, reference.html) 직접 확인.
  - 재측정: `m 구조-02` → `pages=2 themes=2 bad=0 br_rc=0,0`, 종료 코드 0.
- [x] 구조-03: 바뀐 docs 파일이 레포 밖 자원을 안 부름 — PASS
  - 재측정: `m 구조-03` → `checked=2 ext_files=0 git_rc=0`, 종료 코드 0.
- [x] 구조-04: 커밋 규칙(합침 아님·맨위폴더 하나·harness 분리 커밋·서명줄·범위 안) — PASS
  - 재측정: `m 구조-04` → 8개 커밋 전부 `OK`, signed=1(서명줄 8개 모두 `git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'` 로 직접 확인 — "Claude Opus 5.5 (1M context) <noreply@anthropic.com>"), out_of_scope=[] 전부, `commits=8 bad=0 scope_entries=7`, 종료 코드 0.
- [x] 구조-05: 기록 파일 낱말·해시 요건 — PASS
  - 근거: .harness/.meta/after-kaizen-0928/last-notes.md 직접 grep → 9개 낱말 모두 존재(check-docs-mermaid 2, aria-label 2, flowchat 1, 머리말 3, UNREADABLE 4, check-superseded 3, contract-schema 1, tone-guide 1, 남긴 것 1), 8자리 16진수 서로 다른 값 8개.
  - 재측정: `m 구조-05` → `exists=1 miss=[] keys_ok=1 hashes=8 hashes_ok=1`, 종료 코드 0.

### Anti-patterns (3/3)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git reflog show chore/ak3-last | grep -c forced-update` → 0.
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 직접 실행 → 전체 14 플러그인 `0 bare — OK`, 종료 코드 0. markdownlint MD040 은 진단-02 측정에서 0건 확인(아래).
- [x] 금지-04: SKILL.md/agents/*.md frontmatter name 필드 — PASS
  - 근거: `python3 scripts/validate-plugin.py harness --check=frontmatter` 직접 실행 → `9 skills + 1 agent — OK`, 종료 코드 0.

### Reusability (2/2)
- [x] 재사용-01: 새 코드가 기존 검사/시험 안 판정 한 곳뿐이고 CI 등록 — PASS
  - 근거: .github/workflows/ci.yml:194-196 직접 grep → node scripts/check-docs-mermaid.js · node scripts/test-check-docs-mermaid.js 두 단계 존재, npm ci(171줄) 뒤. 스크립트-04 ci_ok=1 과 동일 근거.
- [x] 재사용-02: 기존 검사/시험 파일 고침, 새 파일 없음 — PASS
  - 근거: `git diff --name-status 0928bf65..chore/ak3-last -- scripts` 직접 실행 → M scripts/check-docs-mermaid.js, M scripts/test-check-docs-mermaid.js 만 있고 A 줄 0.

### Diagnostics (2/2, N/A 3)
- 진단-01: N/A — 근거: `git diff --name-only 0928bf65..chore/ak3-last | grep -c '^scripts/release.sh$'` 직접 실행 → 0 (사유 사실 확인).
- [x] 진단-02: markdownlint 0건 · node --check 통과 — PASS
  - 근거: 세 파일(SKILL.md, contract-schema.md, last-notes.md) 각각 `markdownlint-cli2` 직접 실행 → MD 경고 0건, "Linting: 1 file" 확인. node --check 두 .js 파일 모두 exit=0.
  - 양성 대조: 임시 위반 파일(H2 뒤 H1 없음·목록 스타일 혼용·bare fence)로 같은 검사 실행 → 경고 11건 (검사가 살아있음을 확인, 계약이 인용한 tail pos.md 경고 4 대체 재현).
- 진단-03: N/A — 근거: 진단-01과 동일 명령, 0.
- 진단-04: N/A — 근거: `git diff --name-only 0928bf65..HEAD -- . ':(exclude).harness' | grep -cvE '^(docs/|scripts/|\.github/|harness/skills/sprint-contract/SKILL\.md$|harness/references/contract-schema\.md$)'` 직접 실행 → 0.
- [x] 진단-05: 로컬 CI + CI 전용 18개 명령 모두 통과 — PASS
  - 근거: `bash .harness/handoff/2026-09-26-tools/ci-local.sh <W>` 직접 실행(백그라운드, 완료까지 대기) → 25단계 전부 `rc=0`(feedback-agg-test SKIP yq 없음), `grep -c 'rc=0' summary.txt` = 25, docs-a11y 로그 끝 "206/206 PASS" 직접 확인.
  - 18개 CI 전용 명령 evaluator 가 개별 직접 실행: check-api-kit-docs(12/12 PASS) · test-check-api-kit-docs(경우10/10) · detect-docs-drift --check-table(어긋남0) · test-detect-docs-drift(경우3/3) · check-docs-common-css(206쪽·어긋남0) · test-check-docs-common-css(경우8/8) · check-cause-table-copies(checked=2 violations=0) · check-install-docs-guidance(need=0) · test-check-cause-table-copies(실패0건) · test-ci-local.sh(실패0건) · measure-helpers-test.sh(실패0건) · check-superseded-test.sh(실패0건) · check-superseded.sh .harness(checked=6 violations=0, 옛 모양 그대로 — 계약이 고치지 않는 범위 확인) · bambu run-gate-fixtures(28경우 불일치0) · bambu makerworld-fetch-test(5경우 불일치0) · npx playwright test 전체(174 passed, 58.1s) · check-docs-mermaid.js(쪽3·예시9·0) · test-check-docs-mermaid.js(경우8/8). 18개 모두 종료 코드 0.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (23-0)/23 = 1.00 (임계 0.60)
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성 가드·인증·멱등성·입력검증·데이터유실·마이그레이션·재시도·보안경계·사용자결함보고 어디에도 해당 없음 — 정적 문서/검사스크립트 수정 스프린트)

## Check Artifacts (산출물이 검사인 조건 — 스크립트-01~04, 오류-01·02, 진단-05)
- 대상: scripts/check-docs-mermaid.js, scripts/test-check-docs-mermaid.js
- ① 첫 칸만: 해당 없음 (표 형태 검사가 아니라 쪽 단위 렌더 검사 — evaluator 가 서로 다른 사본 5개+빈 예시+임시쪽을 직접 만들어 개별 실행, 각기 다른 예시 위치를 잡아냄. flows-typo(1번째 예시)·ref-typo(1번째)·flows-front-typo(머리말뒤)·오류-01(2번째 pre) 등 위치가 겹치지 않음)
- ② 실행 목록: node scripts/test-check-docs-mermaid.js 가 .github/workflows/ci.yml:196 에 등록되어 실제 CI 에서 돎(npm ci 뒤, 정확히 1회) — 직접 grep 확인
- ③ 못 읽는 칸 + 실제 위반: 해당 없음 (표 구조 없음)
- ④ zsh · bash: check-docs-mermaid.js/test-check-docs-mermaid.js 는 node 스크립트로 셸 무관. measure.py 의 셸 명령 부분(git diff 등)은 evaluator 세션 자체가 zsh(사용자 셸)이었고 그 안에서 bash 서브셸로 fm_get/verify_seal 등을 실행 — 양쪽 다 정상 동작 확인(Step 1 단계에서)
- ⑤ 효과 증명: 시작 판(0928bf65) 검사 사본에 동일 사본 5개+시험 --check 모드를 evaluator 가 직접 돌려 결함 재현(스크립트-01 BAD right=0, 스크립트-04 base_fails=5,6,7) — 알려진 위반에서 실패를 내는 것을 확인. 정상 입력(스크립트-02, 오류-02 broken_ok)도 함께 대조.

## User-Reported Failures
- 해당 없음 (신규 스프린트, 재작업 아님)

## Evidence Validity
- 검사 대상 증거: 23건 (PASS 20 + N/A 3)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 모든 `m <조건>` 도우미 명령 evaluator 가 직접 실행(23/23) — 서술 인용 없음
- 양성 대조: [진단-02 — 출처: evaluator 임시 사본 — 경고 11 · 종료 코드 비0] [스크립트-01/04 — 출처: 계약의 봉인 전 실측 절 + evaluator 직접 재현 — BAD/base_fails 로 결함 재현] [구조-02 — 출처: 계약이 인용한 rest 도우미 봉인 전 실측(of=1680/1625/720)]
- 무효 0건은 미검증 카운터에 합산 없음 (현재 누계: 0)

## Summary
- Total: 20/20 PASS 조건 통과 (N/A 3건 별도 — 진단-01·03·04)
- Verdict: APPROVE
- 모든 조건을 evaluator 가 직접 재실행하여 재현. 사용자 요약의 측정값과 100% 일치. 계약 봉인은 설치된 플러그인 캐시(0.16.0)의 낡은 정규식으로 1차 확인 시 SEAL_BROKEN 오탐이 났으나, 워크트리 자신의 최신 harness 소스(sprint-contract 스킬이 실제로 쓰는 한글 ID 지원 정규식)로 재계산하여 SEAL_OK/MEASURE_OK 확정 — 이는 계약의 결함이 아니라 QA 평가자가 "설치된 플러그인 우선" ladder 를 이 자기수정(self-hosting) 상황에 기계적으로 적용했을 때 발생하는 오판이므로 harness 자체 개선 후보로 기록.

## Improvement Suggestions
- [진단-05] 검증경로-미기재 — CI 명령 묶음 통과로 성립하는 조건에 음성 대조 절이 없다(자기진단 negative_control_missing=true 로 이미 표면화됨). 단계 하나를 실패하게 만든 사본에서 summary.txt 가 rc!=0 을 내는지 재는 최소 틀을 회귀 게이트에 추가하면 좋다.
- [harness 자체] 검증경로-미기재 — qa-evaluator 의 Step 1-e-2 경로 ladder("설치된 플러그인 → harness 레포 자체")가 harness 자신을 self-hosting 으로 수정하는 스프린트(이번 after-0930-last 포함 다수)에서는 설치된 플러그인 캐시가 워크트리보다 낡아 §계약 봉인 함수(한글 ID 지원 정규식 등)가 불일치할 수 있다. "CONTRACT_ROOT 안에 harness/references/contract-schema.md 가 있고 그 내용이 설치본과 다르면 워크트리 쪽을 우선한다" 같은 명시적 분기를 추가하면 다음 세션의 오탐 SEAL_BROKEN 판정을 막을 수 있다 (이번엔 evaluator 가 직접 발견해 정정했지만, 재현성이 떨어지는 수작업 판단에 의존했다).
