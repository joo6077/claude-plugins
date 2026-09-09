# Sprint Feedback
Feature: howto-research 2 사이클 — deep-links 1차 출처 확정
Evaluated: 2026-09-09 16:20
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-howto-research-deep-links.md
- sha256: a2adf400daa22e01819c7f59777b8c112cd4befed3cf4249e826f95fb1fac25b
- status: active (전환 예정 → done)
- slug: howto-research-deep-links
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 명시 경로 지정 (사용자가 절대경로로 계약 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256/status 동일 — TOCTOU 없음)
- status_transition: active -> done (APPROVE 확정)

## Amendments
- amendments: 0 (사이드카 파일 없음 — 사용자 확인 및 파일시스템 확인 일치)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 1
  - [2026-09-09T09:36:33 · session 4d264694-eb0e-4e84-801f-52b2db804772] 세션 시작 지시 "확정된 항목은 provenance-notes.md 에서 옮기고, 그것을 인용하던 킷 파일도 같은 커밋에서 고친다 (Gotcha 2 — 원장만 고치면 본문에 옛 등급 표기가 남는다)" 가 이번 deep-links 사이클에도 적용되는 표준 지시였으나, `docs/howto/design-brief.md` §P3 (line 45, 97-106)가 Firebase `_` 플레이스홀더를 "(`_` 는 프로젝트 id 자리)"로 **확정 사실처럼** 계속 인용 중임 — 이 사이클이 바로 그 항목을 `[미확인]`으로 명시 판정했음에도 수정되지 않았다. 직전 changelog-feeds 사이클(AR-04)은 동일 패턴(§11 항목 6)에 대해 최소 1줄 포인터 수정을 계약에 명시해 실행한 전례가 있다 — 이번 계약의 GAP 분석에는 design-brief.md 가 대상에서 누락됨.
- verdict 영향: 없음 (표면화 전용 · 미검증 카운터 비합산). 아래 Improvement Suggestions 참조.

## Results

### Skill (3/3)
- [x] SK-01: 확정 인용이 전부 출처 URL 짝 — PASS
  - 근거: `docs/howto/deep-links.md:19-28` 표 8행 전부 `출처 문서` 열에 `https://` 시작 URL 존재, 빈 행 0 (python3 파싱 확인)
- [x] SK-02: Apple JSON 검증 경로 명시 — PASS
  - 근거: `grep -c 'tutorials/data/documentation' docs/howto/deep-links.md` → 2 (>=1)
- [x] SK-03: Stripe MODE 세그먼트 원문 인용 — PASS
  - 근거: `grep -c 'omit a value for live mode' docs/howto/deep-links.md` → 1 (>=1). curl 로 `docs.stripe.com/stripe-apps/deep-links` 원문 대조 완료 (아래 §외부 검증)

### Script (3/3)
- [x] SC-01: CI validate 8종 exit 0 — PASS
  - 근거: validate-plugin.py=0, sync-evals.py --check-only=0, sync-docs.py --check-only=0, sync-orchestrator.py --check-only=0, run-evals.py --verbose=0, check-contrast-claims.py=0, check-docs-links.py=0, check-stale-values.py=0 (전부 직접 실행 확인)
- [x] SC-02: a11y 게이트 exit 0 — PASS
  - 근거: `node scripts/check-docs-a11y.js docs/howto-kit/deep-links.html` → `OK deep-links.html ... 1/1 PASS`
- [x] SC-03: save-test.sh exit 0 — PASS
  - 근거: 직접 실행, `=== ALL TESTS PASSED ===`, exit=0

### Error (4/4)
- [x] ER-01: 7 벤더 각각 조회일 2026-09-09 표기 — PASS [enumerated 전수 확인]
  - 근거: Firebase 1 · Google Cloud 1 · Apple 1 · Stripe 2 · GitHub 1 · AWS 1 · Azure 1 (각 벤더별 grep 개별 실행, 전부 >=1)
- [x] ER-02: Codex/curl 구분 서술 — PASS
  - 근거: `grep -c Codex` → 3, `grep -c curl` → 1, `docs/howto/deep-links.md:142-162` §4가 위임 결과와 로컬 curl 조회 결과를 명확히 구분 서술
- [x] ER-03: 대조/MISS 토큰 — PASS
  - 근거: `grep -c 대조` → 6, `grep -c MISS` → 4, `:147-154` 표가 3건 MISS 원인을 기록
- [x] ER-04: 미확인 2건 + 시도 URL — PASS
  - 근거: `howto-kit/references/provenance-notes.md:131-142` §5 두 항목(`/u/0/`, Firebase `_`) 모두 `확인 실패` 등급 + 시도 URL/검색어 각 1개 이상 나열

### Architecture (6/6)
- [x] AR-01: `docs/howto/deep-links.md` 존재 — PASS (`test -f` 성공)
- [x] AR-02: navigation-anchors.md §2 확정 인용 + AWS/Azure + 정본 포인터, awk 플래그형 — PASS
  - 근거: 계약 지정 awk 명령 실행 결과 46줄 블록(1줄 아님 — flag 기반 정상 추출), AWS 2회·Azure 2회·`deep-links.md` 포인터 1회
- [x] AR-03: HTML 미러 존재 + docs/index.html 이중 등록 — PASS
  - 근거: 파일 존재, `grep -c howto-deep-links docs/index.html` → 2 (`pages` 엔트리 1 + `getIcon` 매핑 1, `:570,672`)
- [x] AR-04: 토큰 5종 리터럴 — PASS
  - 근거: `#F59E0B`→1, `#B45309`→2, `#948779`→1, `#656C7A`→1, `dk-theme`→2 (전부 >=1)
- [x] AR-05: 400줄 이상 + 외부 리소스 0건 — PASS
  - 근거: `wc -l` → 434 (>=400), 외부 로드 정규식 매치 0건
- [x] AR-06: diff-scope 정확 일치 — PASS
  - 근거: `git diff --name-only main...HEAD` 전체와 pathspec 필터링 결과가 6개 파일로 완전 동일

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS (`validate-plugin.py --check=code-fence` 전 14 플러그인 OK, exit 0)
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS (`validate-plugin.py` 전체 실행 exit 0, howto-kit V1 OK)
- (사전 sanity, 비그레이딩) AP-01 하드코딩 버전 · AP-02 force push — diff 내 매치 0건

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트 부당 private화 없음 — PASS (신규 코드/컴포넌트 없음, 문서 전용 산출물)
- [x] RE-02: HTML 미러가 changelog-feeds.html 토큰/테마 구조 재사용 — PASS
  - 근거: `diff` 결과 첫 120줄 title 외 동일, `dk-theme`/`toggleTheme` 함수 구조 동일 패턴 확인

### Diagnostics (3/4 PASS, 1 [미검증:ENV])
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS (exit 0)
- [~] DG-02: IDE diagnostics 워닝/인포 0개 — [미검증:ENV]
  - 1차 도구 시도: 이 평가 세션 도구셋에 IDE Diagnostics MCP(`mcp__ide__getDiagnostics`) 미탑재 — 호출 불가 확인
  - fallback 시도: `validate-plugin.py`(구조 검사) + AP-03 code-fence 검사로 대체 정적 검증 수행, 둘 다 exit 0
  - 실패 로그: 도구 부재로 실행 자체 불가 (출력 없음)
  - 통제 불가 사유 + 재검증 명령: 이 CLI 세션에 IDE 확장 연결이 없음 — 재검증 명령: `Claude Code IDE 확장이 연결된 세션에서 mcp__ide__getDiagnostics 호출 후 결과 확인`
- [x] DG-03: 콘솔 로그 에러/예외 0개 — PASS (`grep -iE "error|exception|traceback"` → 0건)
- [x] DG-04: 실제 앱/서버 구동 에러 — PASS (계약이 N/A 자기선언: 정적 HTML, SC-02 a11y 게이트가 렌더 검증 대신)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02 — IDE Diagnostics MCP 부재, fallback(validate-plugin+code-fence) 수행, 재검증 명령 명시]
- verified_coverage: (24 - 1) / 24 = 0.958  (임계 0.60 충족)
- 연속 ENV 승급: 없음 (DG-02 는 이 계약 최초 평가, iteration 1)
- Verdict 영향: 통상 (env_gaps 1건은 자동 REJECT 카운터에 불포함, 커버리지 임계 통과)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (24개 조건 모두 동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고충돌 9항목에 해당하지 않음 — CI 스크립트 exit code, 문서 인용, 정적 파일 검증 조건)

## User-Reported Failures
- 해당 없음 (이번 평가에 사용자 실패 보고 없음)

## Evidence Validity
- 검사 대상 증거: 24건 (조건별 측정 명령 실행 결과)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: AR-02 의 awk 명령을 포함해 계약이 지정한 모든 측정 명령을 실제 zsh 환경에서 직접 실행함 (24/24). bash 교차 검증은 미수행이나 대상 명령이 셸 분기 민감 문법(glob 등)을 포함하지 않아 위험 낮음
- 외부 검증 (핵심 자산 — 인용 진위): 8/8 확정 인용 전건을 실제 벤더 서버에서 `curl` 로 조회해 원문 대조 완료 (사용자 요청 "최소 3건" 초과 달성)
  - Apple: `https://developer.apple.com/tutorials/data/documentation/xcode/understanding-infrastructure-validation-builds.json` (200, 8711 bytes) → `"[Team ID]"` + `"replace ... in the following URL with your Team ID"` 원문 확인 (HTML 페이지는 SPA 라 17KB 껍데기이므로 문서가 명시한 JSON 엔드포인트로 검증 — 문서의 주장과 일치)
  - Stripe (a): `docs.stripe.com/keys` (200) → `dashboard.stripe.com/test/apikeys` 6회 확인 (문서의 "6회" 서술과 일치)
  - Stripe (b): `docs.stripe.com/stripe-apps/deep-links` (200) → `"omit a value for live mode"` 원문 확인
  - GitHub: `docs.github.com/.../automate-with-actions` (200) → `github.com/settings/personal-access-tokens/new` 원문 확인
  - AWS: `docs.aws.amazon.com/IAM/.../access_policies_last-accessed-view-data.html` (200) → `"Sign in to the AWS Management Console and open the IAM console at ..."` 원문 확인
  - Azure: `learn.microsoft.com/.../log-analytics-overview` (200) → `#view/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade` 원문 확인
  - Firebase: `firebase.google.com/docs/reference/admin/node/firebase-admin.auth.decodedidtoken` (200) → `console.firebase.google.com/project/_/settings/general/android:com.random.android` 원문 확인
  - Google Cloud: `docs.cloud.google.com/iam/docs/grant-role-console` (200) → `"Send the following URL to the principal"` 원문 확인
  - **결론: 8/8 인용 전부 실제 원문과 정확히 일치. 조작/오기 없음.**
- 미확인 2건 승격 여부 검사: `docs/howto/deep-links.md`, `navigation-anchors.md`, `provenance-notes.md`, `docs/howto-kit/deep-links.html` 전수 grep — `/u/0/` 와 Firebase `_` 설명 문장 모두 `[미확인]`/`확인 실패` 등급 유지, 어디서도 확정으로 승격되지 않음. **단, 계약 범위 밖의 `docs/howto/design-brief.md` §P3 (line 45, 103)에서는 Firebase `_`가 여전히 확정 사실처럼 서술됨 — User Correction Audit 및 Improvement Suggestions 참조.**
- 무효 0건은 미검증 카운터에 미합산

## Summary
- Total: 23/24 PASS, 1 [미검증:ENV] (DG-02, 커버리지 영향 미미)
- Verdict: APPROVE
- 이 사이클의 핵심 자산인 "7 벤더 8 인용"은 전건 실제 벤더 서버 조회로 원문 일치가 확인되었고, Apple SPA 우회 기법(JSON 엔드포인트)도 실제로 유효하다. 미확인 2건은 어디에서도 조용히 확정으로 승격되지 않았다(계약 범위 내 파일 기준). AR-02 awk 플래그형은 정상적으로 46줄 블록을 추출했다(1줄 헤더만 반환하는 과거 결함 재발 없음). diff-scope(AR-06)도 선언 그대로 정확히 일치한다. 계약 봉인도 SEAL_OK.

## Improvement Suggestions
- [GAP분석] 범위-미명시 — `docs/howto/design-brief.md` §3 P3절(line 42-46, 97-106)이 Firebase `_` 플레이스홀더를 이번 사이클이 방금 `[미확인]`으로 판정한 바로 그 설명("`_` 는 프로젝트 id 자리")을 여전히 확정 사실처럼 서술 중이다. 세션 시작 지시("인용하던 킷 파일도 같은 커밋에서 고친다")와 직전 changelog-feeds 사이클의 AR-04 전례(설계 정본에 대한 최소 1줄 포인터 수정)를 참고하여, 다음 커밋에서 design-brief.md P3 표의 Firebase 행에 `[미확인]` 각주 또는 `docs/howto/deep-links.md` 정본 포인터를 추가하는 조건을 계약 GAP 분석에 명시적으로 포함시킬 것을 권장한다. 이 킷의 회귀 게이트("확인 못 한 것을 확인한 척하는 것") 정신에 정면으로 저촉되는 지점이므로 우선순위가 높다.
- [계약 메타] 검증경로-미기재 — frontmatter의 `created: "2026-09-09 16:05"`가 `locked_at: "2026-09-09 15:38"`보다 늦은 시각으로 기록되어 있다(생성이 봉인보다 나중). 실제 커밋 시각(15:41:43)과 파일 mtime(15:38)을 볼 때 `created` 값이 오기로 추정된다. 그레이딩 대상 조건은 아니나 다음 계약 작성 시 자동 타임스탬프 검증을 권장한다.
