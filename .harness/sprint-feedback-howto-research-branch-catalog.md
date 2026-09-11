# Sprint Feedback
Feature: howto-research 4 사이클 — branch-catalog 사유 유형 재정의
Evaluated: 2026-09-10 12:30
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-howto-research-branch-catalog.md
- sha256: 6d00689e43181170e409a73ee15843c8cc53c482332a8cff33e20a7084ce3bb5
- status: done (APPROVE 직후 active -> done 전환)
- slug: howto-research-branch-catalog
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 명시 경로 (사용자 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest: sha256:de2726387b7bbb38, actual 동일 — status 전환 후 재확인해도 불변)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (TOCTOU 없음)
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (세션 4d264694 의 이번 사이클 관련 자유텍스트 프롬프트 — "ㄱㄱ"(진행 지시) 1건 뿐. AR-01 REJECT→수정은 harness 계약 루프 자체이며 반영 안 된 "사용자 교정"이 아니다)
- verdict 영향: 없음

## Results

### Skill (3/3)
- [x] SK-01: navigation-anchors.md §5 사유 표 6종 + 각 행 출처 — PASS (재확인, 회귀 없음)
  - 근거: `awk '/^## 5\./{f=1;print;next} f&&/^## /{exit} f' howto-kit/references/navigation-anchors.md` 실행 → `선행조건` 3회, `Dropbox` 1회, `Windows` 1회, `rolled out gradually` 1회. 전부 ≥1.
- [x] SK-02: step-contract.md cause enum 확장 + 언어 분리 — PASS (재확인)
  - 근거: `howto-kit/references/step-contract.md:29` — `- cause: 권한-역할|권한-조직정책|선행조건|요금제|버전|A-B`. `선행조건` 포함, `언어` 파이프 목록 안에 없음.
- [x] SK-03: SKILL.md "5종"→"6종" — PASS (재확인)
  - 근거: `howto-kit/skills/howto/SKILL.md:111`. `grep -c '분기 사유 5 종'`=0, `grep -c '분기 사유 6 종'`=1.

### Script (3/3)
- [x] SC-01: CI validate 8종 전부 exit 0 — PASS (재실행)
  - 측정값: validate-plugin.py=0 · sync-evals.py --check-only=0 · sync-docs.py --check-only=0 · sync-orchestrator.py --check-only=0 · run-evals.py --verbose=0 · check-contrast-claims.py=0 · check-docs-links.py=0 · check-stale-values.py=0. 8/8 exit 0.
- [x] SC-02: howto-kit evals 9/9 exit0 — PASS (재실행)
  - 근거: `bash howto-kit/evals/run-evals.sh` → `EVALS total=9 pass=9 fail=0` / `EVALS_PASS`, exit=0.
- [x] SC-03: a11y 게이트 exit0 — PASS (재실행)
  - 근거: `node scripts/check-docs-a11y.js docs/howto-kit/branch-catalog.html` → `OK ... contrastFail=0` / `1/1 PASS`, exit=0.

### Error (4/4)
- [x] ER-01: 6종 각각 1차 출처 — PASS (재확인, 회귀 없음)
  - 근거: `docs/howto/branch-catalog.md:30-37` 표 6행(권한/역할·권한/조직정책·기능 선행조건·요금제·버전·A/B 롤아웃) 각각 출처열(Atlassian/GitHub/Apple/Dropbox/Microsoft/Google URL) 비어있지 않음. 언어 행은 `docs/howto/branch-catalog.md:85` `[미확인]` 명시.
- [x] ER-02: 언어/로케일 분리 + 이유 명시 — PASS (재확인)
  - 근거: `docs/howto/branch-catalog.md:72-83` §3 표 — "항목이 없다" vs "항목은 있는데 이름이 다르다" 증상 구분 명시.
- [x] ER-03: 확인 실패 2건 + 시도 URL — PASS (재확인, 미변경)
  - 근거: `howto-kit/references/provenance-notes.md` §7 — (a) 언어/로케일 분기 문장 (b) 스타일 가이드 조항 두 행 모두 리터럴 `확인 실패` + 시도 URL.
- [x] ER-04: HTML 엔티티 검증 함정 서술 — PASS (재확인, 회귀 없음)
  - 근거: `docs/howto/branch-catalog.md:119-131` §6 — `&#39;` 리터럴 + "엔티티를 디코드한 뒤 대조하라" + 5 HIT/1 MISS 경위 서술.

### Architecture (6/6) — AR-01 재측정 결과 PASS
- [x] AR-01: 신규 리서치 문서 `docs/howto/branch-catalog.md` — **PASS (L3, 재측정)**
  - L1(존재): `test -f docs/howto/branch-catalog.md` PASS.
  - L3(의미, 직접 판정): 직전 REJECT 사유였던 자기모순을 재확인한 결과 해소됨. `git show b8d0398`로 확인한 실제 diff는 정확히 2곳 — 라인 26 "확정된 분기 사유 5 종"→"6 종", 라인 76 "위 5 종"→"6 종". 재측정 결과: (1) §2 헤더(`26행`) "확정된 분기 사유 6 종" ↔ 바로 아래 표(`30-37행`) 6행 — 일치. (2) §3 비교표(`76행`) "위 6 종" ↔ 헤더와 일치. (3) 잔존하는 "5 종" 문자열 2건(`8행`, `17행`)을 직접 읽고 문맥을 판정: `8행` "이 킷은 그 분기의 사유를 **5 종**으로 유형화해 놓았었다. 이번 사이클이 그 목록을 검증했고, **둘이 틀렸다**는 것을 확인했다" — 과거완료 시제("~해 놓았었다")로 이번 사이클 이전의 잘못된 상태를 서술하며, 바로 이어지는 문장이 그것을 "틀렸다"고 명시적으로 교정한다. `17행`은 "## 1. 무엇이 틀렸나" 섹션의 표 안에서 같은 과거 오류를 서술한다. 두 잔존 사례 모두 §1(무엇이 틀렸나) 섹션 안에 있고, §2(확정된 사유, 6 종)·§3(비교표, 6 종)과 구조적으로 분리되어 있어 오류가 아니라 의도된 역사적 서술이다.
  - 결론: 문서가 이제 내적으로 정합하다. 헤더 숫자(6)와 표 행수(6)가 일치하고, 잔존 "5 종"은 명시적 과거 서술 문맥이다.
- [x] AR-02: design-brief.md 교정 + 정본 포인터 — PASS (재확인, 회귀 없음)
  - 근거: `grep -c 'branch-catalog.md' docs/howto/design-brief.md`=1, `grep -c '분기 사유는 5 가지로 유형화한다' docs/howto/design-brief.md`=0. `docs/howto/design-brief.md:151-156` — "2026-09-10 교정" 각주 + "6 가지"로 확정.
- [x] AR-03: HTML 미러 등록 (동일 id 2곳) — PASS (재확인)
  - 근거: `docs/index.html:572`(`pages` 배열, title "…사유 6종") · `:676`(`getIcon` 매핑) 양쪽 `howto-branch-catalog` 동일 id. `grep -c`=2.
- [x] AR-04: 토큰 5개 리터럴 — PASS (재확인)
  - 근거: `docs/howto-kit/branch-catalog.html` — `--accent:#F59E0B`=1, `--accent:#B45309`=1, `--text3:#948779`=1, `--text3:#656C7A`=1, `dk-theme`=2. 전부 ≥1.
- [x] AR-05: 400줄 이상 + 외부 리소스 0건 — PASS (재확인)
  - 측정값: `wc -l`=414 (기준: >=400). 외부 리소스 정규식 매치=0.
- [x] AR-06: diff-scope 정확 일치 — PASS (재실행)
  - 근거: `git diff --name-only origin/main...HEAD -- docs howto-kit .harness ':(exclude).claude/worktrees' ':(exclude)result.json'` 결과와 `git diff --name-only origin/main...HEAD` 전체 결과가 `diff`로 완전 일치 (9개 파일).

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS (재실행)
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` → 전 플러그인(howto-kit 포함) "V6 code-fence 0 bare — OK", 14 plugins 14 OK, exit 0.
- [x] AP-04: frontmatter name 필드 — PASS (재실행)
  - 근거: `python3 scripts/validate-plugin.py` → "14 plugins, 14 OK", exit 0. 이번 iteration 변경 파일은 `docs/howto/branch-catalog.md`(본문만, frontmatter 없음) 뿐.

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트 private화 없음 — PASS (재확인)
  - 근거: 산출물 전부 공개 docs/references, `docs/index.html`에 정식 등록(AR-03).
- [x] RE-02: 기존 컴포넌트 재사용 — PASS (재확인)
  - 근거: `docs/howto-kit/branch-catalog.html`과 `docs/howto-kit/ui-anchoring.html`의 1-60행 diff — `<title>` 한 줄만 차이, 토큰/토글 구조 동일.

### Diagnostics (3/4, 1건 [미검증:INVALID] — 규칙 11 escalation)
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS (재실행, exit=0, 출력 없음)
- [미검증:INVALID] DG-02: IDE diagnostics 워닝/인포 0개 — **[low-confidence] 강등, ENV→INVALID 이관 (규칙 11)**
  - 1차 도구 시도: 이 세션에 IDE Problems 패널 접근 수단 없음(서브에이전트, `runtime_inspection.mcp_server: null`).
  - fallback 시도: `which markdownlint markdownlint-cli2 remark` → 전부 not found (iteration 1과 동일 결과 재확인).
  - 실패 로그: "markdownlint not found" / "markdownlint-cli2 not found" / "remark not found" (실제 커맨드 출력).
  - **재분류 사유**: 같은 계약(슬러그 `howto-research-branch-catalog`)의 동일 조건 ID DG-02가 iteration 1(REJECT)과 iteration 2(이번) **2회 연속** `[미검증:ENV]`였다. 엄격도 규칙 11: "같은 조건 ID가 2 iteration 연속 ENV이면 환경 문제가 아니라 계약 결함(검증경로-미기재)이다." 이 조건은 계약에 `측정:` 인라인 절이 아예 없고(다른 카테고리는 대부분 측정 명령이 인라인 기술됨), 3단계 fallback 경로도 계약에 명시되지 않았다 — 이는 environment 우연이 아니라 조건 작성 시점의 검증경로 미기재다.
  - 재검증 명령(4요건 충족 유지): 마크다운 린터 설치 후 `npx markdownlint-cli2 "docs/howto/*.md" "howto-kit/**/*.md"` 또는 VSCode Problems 패널 직접 확인.
  - Verdict 영향: invalid_evidence=1 (< 2 임계) → 자동 REJECT 미해당. verdict는 여전히 APPROVE.
- [x] DG-03: 콘솔 로그 에러 0개 — PASS (재실행, usage 메시지만 출력)
- [x] DG-04: N/A — 계약 명시대로 SC-03 a11y 게이트가 대신함.

## Unverifiable Summary
- invalid_evidence: 1 [DG-02 — 분기 B2(4요건 자체는 갖췄으나 규칙 11의 "2 iteration 연속 ENV" 로 INVALID 강등), 사유: 계약에 DG-02 전용 측정/fallback 인라인 절 부재, 시도한 fallback 단계: markdownlint 계열 3종 탐색]
- env_gaps: 0 (DG-02가 ENV에서 INVALID로 이관되어 이 장부에서 제외됨)
- verified_coverage: (24 - 0) / 24 = 1.00 (임계 0.60 이상, env_gaps 없음)
- 연속 ENV 승급: [DG-02 — iteration 1, 2 연속 ENV → invalid_evidence로 이관, Improvement에 검증경로-미기재 등록]
- Verdict 영향: PASS 허용 (invalid_evidence=1 은 2건 미만이므로 자동 REJECT 아님)

## Discrimination (규칙 12 적용 조건 없음)
- 24개 조건 중 동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션·재시도/중복제거·보안 경계·사용자 결함 보고 충돌 해당 조건 없음(문서/스크립트 검증형). 규칙 12 미적용.

## User-Reported Failures
- 해당 없음. AR-01은 사용자 실패 "보고"가 아니라 iteration 1의 QA REJECT였고, 이번 iteration에서 재측정하여 PASS로 전환함 (상태 전이: FAIL(iter1) → PASS(iter2)).

## Evidence Validity
- 검사 대상 증거: 24건(조건) 전부 이번 iteration에서 재실행/재측정
- 무효 판정: 1건 (DG-02 — 검사 3 반증가능성: 계약에 측정경로가 없어 도구 유무와 무관하게 이 조건은 애초에 판정 불가능한 형태였음)
- 셸 스니펫 실행 검증: 실행 25+건 (SC-01의 8개 명령, SC-02, SC-03, AP-03/04, DG-01/03, AR-06 git diff ×2, SK-01/02/03 grep/awk, ER-01~04 grep/read, AR-02~05 grep/wc, AR-01 원문 직독)
- 무효 1건은 미검증 카운터에 합산됨 (invalid_evidence=1, 위 참조)

## Summary
- Total: 23/24 conditions PASS, 1건 [미검증:INVALID] (DG-02, verified_coverage=1.00)
- Verdict: APPROVE
- Iteration 1의 REJECT 사유(AR-01 자기모순)가 2줄 교정(라인 26, 76의 "5 종"→"6 종")으로 해소됨을 직접 원문 재독 + L3 의미 검증으로 확인. 회귀 검증: 파일이 변경된 조건(ER-01/02/04, AR-01~06)과 전역 스크립트(SC-01~03, AP-03/04, DG-01/03)를 전부 재실행하여 회귀 없음 확인. 카운트 정합성을 branch-catalog.md·navigation-anchors.md·SKILL.md·design-brief.md·HTML 미러·index.html 전 표면에서 재확인 — 모두 "6 종"/"6종"/"6 가지"로 일치하고, 잔존하는 "5 종" 표기(branch-catalog.md 8·17행, HTML 미러 227·231·242행, design-brief.md 151행)는 전부 명시적 과거 서술 문맥으로 확인됨. 계약 봉인 SEAL_OK 유지. DG-02는 규칙 11에 따라 ENV→INVALID로 재분류했으나 1건이라 자동 REJECT 임계(2건) 미만.

## 검증 참고 사항 (verdict에 영향 없음, 참고용)
- iteration 1의 "검증 참고 사항" 3건(6번째 유형 신설 타당성, 언어 축 분리 타당성, enum 확장 무해성)은 이번 iteration에서 재검토 대상 파일이 바뀌지 않아 그대로 유효.

## Improvement Suggestions
- [AR-01] 측정-산출물-부재 — `test -f`만 요구하는 측정으로는 "신규 리서치 문서"의 내적 일관성(자기모순 여부)을 계약 조건 자체로 자동 검증할 수 없다. 유사 계약에는 `grep -c '<확정 카운트> 종' <정본파일>`처럼 문서 자신의 헤더-표 카운트 일치를 검사하는 보조 측정을 추가할 것을 권장한다 (iteration 1과 동일 제안, 재발 방지 목적으로 유지).
- [DG-02] 검증경로-미기재 — Diagnostics 카테고리의 DG-02(IDE diagnostics)는 2 iteration 연속 `[미검증:ENV]`로 종결됐다. project.yaml의 `diagnostics.ide_exclude`만으로는 서브에이전트 환경에서 판정할 measurement path가 없다. 향후 계약에는 DG-02에 인라인 측정 절을 추가하라 — 예: "1차 IDE Problems 패널 MCP, 2차 fallback `npx markdownlint-cli2` 정적 검사, 3차 불가 시 [미검증] 허용"과 같이 3단계 fallback을 명시하거나, project.yaml에 실제로 설치된 린터 커맨드를 `commands.lint`로 바인딩해 DG-02가 그 커맨드를 참조하게 하라.
