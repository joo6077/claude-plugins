# Sprint Feedback
Feature: howto-research 3 사이클 — ui-anchoring 규칙 강도 교정
Evaluated: 2026-09-09 18:20
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: .harness/sprint-contract-howto-research-ui-anchoring.md
- sha256: 6d665f10d27d8447dccafeea18602493d47e41f2dbfe02d61c8715f70f7871a7
- status: active
- slug: howto-research-ui-anchoring
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (owner_session 도 세션과 일치, ladder 2 로도 성립)
- legacy_contract_used: false
- seal_status: SEAL_OK (verify_seal 재실행 — recorded=ac14502f09311b6d actual=ac14502f09311b6d)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (iteration 1 과 sha256 동일 — 조건 문구 변조 없음)
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 부재 `.harness/sprint-amendments-howto-research-ui-anchoring.md` 없음)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (세션 4d264694 구간 스캔 — 이번 사이클 관련 사용자 교정은 전부
  계약/구현에 반영됨. 발견된 항목은 이전 사이클(체크리스트/이름충돌) 백로그 메모뿐, 이번
  ui-anchoring 사이클과 무관)
- verdict 영향: 없음

## Iteration 2 — 재평가 범위

직전 REJECT 사유는 ER-03 하나였다. 커밋 `9026aa7` 이 `howto-kit/references/provenance-notes.md`
**1개 파일**만 수정했으므로, ER-03 재측정 + 그 파일·전역 스크립트에 걸리는 회귀 조건만
새로 실행하고 나머지 21개는 iteration 1 근거를 재사용한다(대상 파일이 이번 커밋에서
전혀 변경되지 않았음을 `git diff --stat main...HEAD` 로 확인).

## Results

### Error (4/4)
- [x] ER-01: 단독 사용 금지 유지, 무조건 허용 진술 없음 — PASS (회귀 재측정)
  - 근거: 측정값 — 대상 817 파일(`git ls-files | grep -v '^\.harness/' | wc -l`, iteration 1과 동일).
    6개 표면(navigation-anchors.md/SKILL.md/howto-reviewer.md/provenance-notes.md/design-brief.md/
    docs/howto/ui-anchoring.md) + docs/index.html + docs/howto-kit/ui-anchoring.html 를 개별
    grep(`방향어를 써도`, `방향어 사용.*가능`, `방향어.*허용된다`) 재실행 — 전부 0건.
    `docs/howto-kit/ui-anchoring.html:329`에 "방향어를 써도 된다"라는 문자열이 등장하지만
    "&#8220;방향어를 써도 된다&#8221;로 읽으면 F4가 되살아난다"는 경고 문맥이라 무조건 허용
    진술이 아님(전체 문장 확인, L3)
- [x] ER-02: 허용 조건이 위치 단서 동반 시로 한정 — PASS (iteration 1 근거 재사용, 파일 미변경)
  - 근거: `docs/howto/ui-anchoring.md:59` `another indication of location` 원문. iteration 1
    이후 이 파일은 git diff에서 변경되지 않음(commit 9026aa7 은 provenance-notes.md만 수정)
- [x] ER-03: Apple 부재가 `[미확인]`으로 원장에 남고 `확인 실패` 리터럴이 Apple과 같은 항목에
  등장, 시도 URL 1개 이상 — **PASS** (재측정, REJECT 사유 해소 확인)
  - 근거: `howto-kit/references/provenance-notes.md:151`
    `| Apple Style Guide 에 "방향어를 위치 단서로 단독 사용하지 마라" 의 **동등 조항** | **확인 실패** | 아래 시도 URL 참조 |`
    — `grep -n "Apple" ... | grep "확인 실패"` 매치 1건, 리터럴 `확인 실패`가 Apple을 포함한
    같은 표 행(항목)에 정확히 등장. 시도 URL 2건(`support.apple.com/guide/applestyleguide/…`,
    `help.apple.com/pdf/applestyleguide/…`) — 계약 요구(1개 이상) 충족.
    §1(26-28행)·§5(133-134행)와 동일한 표 규약(항목/상태/근거 3열, `**확인 실패**` 볼드)으로
    통일되어 있음을 `git diff 3d462f5 9026aa7 -- .../provenance-notes.md` 로 대조 확인(L3)
- [x] ER-04: Google/Microsoft 입장 차이 구분 서술 — PASS (iteration 1 근거 재사용, 파일 미변경)
  - 근거: `docs/howto/ui-anchoring.md` §2(Google — 완화조건 없음)/§3(Microsoft — 완화조건 있음)
    분리 유지. 이번 커밋에서 이 파일은 변경되지 않음

### 의미 왜곡 점검 (지시사항 4번)
- §6 수정 전(`3d462f5`)과 후(`9026aa7`)를 `git diff`로 직접 대조: "Apple 동등 조항 확보 실패"와
  "Apple 이 방향어를 용법으로 다룬다"라는 **두 개의 서로 다른 사실**은 수정 후에도 표의
  별도 행(151행 vs 152행)으로 **계속 구분**되어 있다. 리터럴 `확인 실패`를 맞추기 위해 이
  구분 자체를 지우거나 병합하지 않았다 — 요청하신 "Apple이 확인 실패인 것과 용법으로는
  다룬다는 것이 여전히 구분되는가"는 YES.
- **별도 관찰(계약 조건 밖, 참고용)**: 152행에 이번 수정에서 새로 붙은 `확인됨 2026-09-09`
  상태 태그는 iteration 1까지는 없던 라벨이다. 원문 자체(`Apple 이 방향어를 용법으로 다룬다`)는
  `3d462f5`부터 있던 서술을 표로 옮긴 것뿐이라 내용 자체의 왜곡은 아니지만, 이 QA 세션이
  접근 가능한 `~/.claude/codex-research-log/2026-09.md`에는 이 URL(`help.apple.com/pdf/
  applestyleguide/...`) 재조회 기록이 없어 "확인됨" 라벨을 뒷받침하는 실행 산출물을 이
  세션에서는 찾지 못했다(단, 계약이 언급한 "세션 로컬 curl" 처럼 Codex 로그에 안 남는
  경로로 실제 확인했을 가능성도 있어 허위라고 단정할 근거도 없다 — 확증도 반증도 불가).
  ER-03은 152행이 아니라 151행만 요구하므로 조건 판정에는 영향 없음. 다만 provenance-notes.md
  자신의 존재 목적("확인 못 한 것을 확인한 척하지 않는다")에 비추어, 다음 사이클에서 이
  날짜 라벨의 근거(curl 로그 등)를 남기거나 라벨을 제거할 것을 권장한다(아래 Improvement 참고)

### 회귀 재측정 — 공유 스크립트 (파일 변경으로 인한 전역 재실행)
- SC-01 CI 8종: validate-plugin.py(exit0) · sync-evals.py --check-only(exit0, 0 added/orphans/missing)
  · sync-docs.py --check-only(exit0, "모든 README가 동기화 상태") · sync-orchestrator.py
  --check-only(exit0, "이미 동기화됨 13 plugins") · run-evals.py --verbose(exit0, `Total: 106
  passed, 0 failed`) · check-contrast-claims.py(exit0, 어긋난 것 0) · check-docs-links.py(exit0,
  357개 링크 깨진 것 없음, 내비 173/173) · check-stale-values.py(exit0, "되살아난 옛 값 없음")
  — **PASS 유지**
- SC-02 `bash howto-kit/evals/run-evals.sh`: `EVALS total=9 pass=9 fail=0 / EVALS_PASS`, exit0
  — **PASS 유지**
- SC-03 `node scripts/check-docs-a11y.js docs/howto-kit/ui-anchoring.html`: `OK … contrastFail=0
  … 1/1 PASS`, exit0 — **PASS 유지**
- AP-03/AP-04: `validate-plugin.py --check=code-fence`(14 plugins OK, exit0) · 전체
  `validate-plugin.py`(14 plugins OK, V1 frontmatter 포함 전부 OK, exit0) — **PASS 유지**
- DG-01/DG-03: `bash -n scripts/release.sh`(exit0) · `bash scripts/release.sh 2>&1 || true`(usage
  안내만 출력, 에러 스택 없음, exit0) — **PASS 유지**
- AR-06 변경 범위: `git diff --name-only main...HEAD -- docs howto-kit .harness
  ':(exclude).claude/worktrees' ':(exclude)result.json'` (14개 파일) vs
  `git diff --name-only main...HEAD` (14개 파일) — `diff` 출력 공집합, 정확히 일치 —
  **PASS 유지** (9026aa7 이 추가한 provenance-notes.md 변경도 두 집합에 동일하게 포함)

### 나머지 조건 (파일 미변경 — iteration 1 근거 재사용)
- Skill (3/3): SK-01/02/03 — PASS (근거는 iteration 1 피드백 참조. `navigation-anchors.md`,
  `SKILL.md`, `howto-reviewer.md` 모두 이번 커밋에서 미변경 — `git diff --stat main...HEAD`에
  provenance-notes.md 외 이 세 파일도 나타나지만 그건 `3d462f5`에서 만들어진 변경이고 9026aa7은
  건드리지 않음)
- Architecture (6/6): AR-01~AR-05 — PASS (근거는 iteration 1 피드백 참조, 대상 파일 미변경).
  AR-06은 위에서 재측정 완료
- Reusability (2/2): RE-01/RE-02 — PASS (근거는 iteration 1 피드백 참조, 대상 파일 미변경)
- Diagnostics: DG-01/DG-03 위에서 재측정 완료(PASS). DG-04 — PASS/N/A(계약 명시, SC-03 대체).
  DG-02 — [미검증:ENV] 유지(아래)
  - 1차 도구 시도: 이 세션 도구는 Read/Bash/Glob/Grep 뿐이며 IDE Problems 패널 MCP 미연결
  - fallback 시도: `project.yaml`의 `commands.lint: null` — 대체 정적 lint 명령 부재(스택이
    shell-scripts라 별도 lint 파이프라인이 애초에 없는 기존 설계, 계약/설정 결함 아님)
  - 실패 로그: N/A (도구 자체 부재로 호출 시도 불가)
  - 통제 불가 사유: QA 세션에 IDE extension/MCP 연결 없음. 재검증 명령: IDE 확장이 연결된
    세션에서 `getDiagnostics` 상당 기능으로 `provenance-notes.md` 재확인
  - 연속 ENV 승급 체크: iteration 1에서도 동일 사유로 ENV였음(2회 연속). 그러나 근본 원인이
    "계약의 검증경로 미기재"가 아니라 "이 QA 세션에 IDE MCP가 원천적으로 연결되지 않는
    환경 구성"이라 계약 결함으로 볼 수 없음(project.yaml에 IDE 검증 경로 자체가 정의되어
    있지 않고, 이는 스택이 shell-scripts인 모노레포 특성상 정상). `[low-confidence]` 강등은
    보류하되, Improvement로 기록

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02 — 위 4요건 근거 참조]
- verified_coverage: (24 - 1) / 24 = 0.958 (임계 0.60) — 통과
- 연속 ENV 승급: DG-02 는 2 iteration 연속 ENV. 계약 결함이 아니라 세션 환경 결함으로 판단한
  근거는 위 Diagnostics 절 참조. `[low-confidence]` 강등은 보류
- Verdict 영향: 통상 (모든 조건 PASS, 자동 REJECT/BLOCKED 게이트 미해당)

## Discrimination (규칙 12 적용 조건 없음)
- 적용 대상 조건 없음 — 문서·리서치 스프린트. 계약 자체 요구 음성 대조는 SC-01/02/03 모두 재실행
  검증 완료(실행 음성 대조는 iteration 1에서 이미 수행·원상복구 확인했고, 이번엔 구현이 변경
  안 된 스크립트 대상이라 재실행하지 않음 — `discrimination: static-only` 로 표기)

## User-Reported Failures
- 해당 없음

## Evidence Validity
- 검사 대상 증거: 24건 (조건별 1건, ER-03/ER-01/ER-04/AR-06/SC-01/SC-02/SC-03/AP-03/AP-04/
  DG-01/DG-03 은 이번 세션에서 직접 재실행, 나머지 13건은 iteration 1 원 증거 재확인)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 이번 세션 재실행 명령 전부 bash(Bash 도구 경유)로 실제 실행,
  출력 인용 완료. zsh 별도 실행은 안 함(iteration 1과 동일 사유 — 사용된 grep/awk/git/node/
  python 호출은 zsh 특유 glob 확장에 의존하지 않아 이식성 위험 낮음)
- 무효 0건은 미검증 카운터(env_gaps 1건)에 영향 없음

## Summary
- Total: 24/24 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- [ER-03] 검증경로-미기재(해소됨) — iteration 1에서 지적한 리터럴/동의어 불일치는 구현자가
  `provenance-notes.md` §6을 §1/§5와 동일한 표 규약으로 통일하며 해소했다. 향후 유사 조건은
  GAP 분석 표에 "리터럴 문자열 X를 정확히 쓴다"처럼 구체 문자열을 명시하면 재작업 루프를
  줄일 수 있다
- [§6 부가 관찰] 측정-산출물-부재(참고, 조건 미대응) — `provenance-notes.md:152`에 새로 붙은
  `확인됨 2026-09-09` 라벨은 이번 QA 세션이 접근 가능한 codex-research-log에서 대응하는 fetch
  기록을 찾지 못했다. 어떤 계약 조건도 이 행을 직접 요구하지 않아 verdict에 영향은 없으나,
  이 파일의 존재 목적(미확인 사실을 확인된 것처럼 적지 않기)에 비추어 다음 커밋에서 이
  라벨의 근거(curl 로그·조회 방법)를 남기거나 라벨을 제거할 것을 권장
