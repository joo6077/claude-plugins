# Sprint Feedback
Feature: howto-kaizen 1 사이클 — G4 주장 탐지 정밀화 · 미확정 원장 인덱스 동기화
Evaluated: 2026-09-11 11:20
Verdict: REJECT
Iteration: 2

## Contract Fingerprint
- path: .harness/sprint-contract-howto-kaizen-g4-precision.md
- sha256: 2446f0321cc85aa297a7b6de8ae9859d6f38a59984a460573de84f81789bd33c
- status: active
- slug: howto-kaizen-g4-precision
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session 4d264694-eb0e-4e84-801f-52b2db804772 == 현재 세션, active 후보 3개 중 유일 소유)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:bcf7e7535ec1a339 == 실측 contract_digest)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 sha256/status 동일)
- status_transition: skipped (verdict=REJECT status=active)

## Amendments
- amendments: 2 (AM-01, AM-02)
- PASS 근거 가능: 2 [AM-01 narrowing·unanchored → SC-03 / AM-02 narrowing·unanchored → ER-01·ER-02]
- PASS 근거 불가: 0
- 집합형 direction 재현 (자기신고 아님, 직접 재계산):
  - AM-01(SC-03): 원 커밋 f99c181(15케이스) vs 현재(16케이스)를 **behavior 튜플**(fixture|expect_final|assertions)로
    비교 → `narrowing measured_removed=0 measured_added=1` (E16 1건 순수 추가, 행동 제거 0건). 재현 명령·출력:
    ```
    $ diff behavior_orig.txt behavior_new.txt
    5a6
    > fixtures/fail-g4-korean-abolish-unsourced.md | GATE_FAIL | G4_DEPRECATION FAIL,unsourced_claims=1
    ```
    단, **raw id 문자열**(`E13-g4-retention-notice-not-deprecation` → `E13-g4-retention-notice-sourced`
    로 개명)로 그대로 비교하면 `relaxing measured_removed=1 measured_added=2`로 **극성이 반전**된다
    (재현: `amend_direction_oracle ev_orig.txt ev_new.txt` = relaxing 1/2). E13은 fixture·assertions·
    expect_final이 전부 동일하고 note/id만 바뀐 순수 개명이므로, 개명을 "제거"로 세지 않는 behavior
    비교가 실체에 맞다고 판단했다 — 사이드카의 "narrowing 0/1" 결론을 **행동 단위 재구성으로 재현**했다.
    헬퍼 선택(`amend_direction_oracle`, 측정 집합)은 옳다 — eval 케이스 목록은 G4 구현이 스캔당하는
    모집단이라 diff-scope 스캔 대상과 동일 구조다. 다만 사이드카는 이 raw-id 반전 위험을 문서화하지
    않았다 — Improvement로 남긴다.
  - AM-02(ER-01·ER-02): "확인:에만 조작된 주장 + 무관 출처" 픽스처를 f99c181(면제 상태) 코드에 돌리면
    `G4_DEPRECATION PASS unsourced_claims=0`(버그), 현재(반영 후) 코드에 돌리면
    `G4_DEPRECATION FAIL unsourced_claims=1`(수정됨) — 사이드카의 before/after 서술을 **직접 실행 재현**.
    zsh·bash 동일. narrowing 판정 타당.

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (2026-09-10T14:20~2026-09-11 구간 키워드 스캔 — "아니/다시/잘못/틀렸/취소/되돌려"
  매칭 0건. 전수 정독은 아니고 키워드 기반 스크리닝이다 — `[샘플링-키워드스캔]`)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (2/3)
- [x] SK-02: `HOWTO_DEP`에 `종료 예정` 추가, `삭제`·`종료` 단독 없음 — PASS [exact, L3]
  - 근거: `howto-kit/scripts/howto-gate.sh:24` `HOWTO_DEP='...|삭제 예정|삭제가 예정|종료 예정'`.
    `grep -o "HOWTO_DEP='[^']*'" ... | tr '|' '\n' | grep -nE '^(삭제|종료)$'` → 0건.
- [x] SK-03: README "이 킷이 사실로 말하지 않는 것"이 원장 절 수(9)를 정확히 말한다 — PASS [exact, L3]
  - 근거: `awk '/^## 이 킷이 사실로 말하지 않는 것/{f=1;print;next} f&&/^## /{exit} f' howto-kit/README.md`
    → "현재 9 절" + 표 9행. 옛 문자열("체크리스트 방법론의 1 차 출처, 변경 로그 피드 3 건... ") 매칭 0건.
- [ ] SK-01: 게이트가 `- 확인:` 줄을 deprecation 주장 탐지에서 **제외한다** — **FAIL** [exact, L3]
  - 근거: `grep -n 'dep_claim = 1' howto-kit/scripts/howto-gate.sh` → 78행(헤더 블록), 91행(캐치올 블록).
    두 줄 중 `확인` 제외 조건을 포함한 줄 0건 (`grep -c '확인'` = 0). 91행은
    `if ($0 ~ dep) dep_claim = 1` — 조건 없이 모든 열린-스텝 줄(`- 확인:` 포함)을 그대로 센다.
    실제로 `howto-kit/scripts/howto-gate.sh:85-90` 주석이 "면제해 봤다가 **되돌렸다**"라고 명시한다 —
    이 조건이 요구하는 동작을 구현이 **의도적으로 반대로** 만든 것이다.
  - AM-02는 ER-01·ER-02만 대상 조건으로 선언했고 SK-01은 사이드카 어디에도 등장하지 않는다 —
    이 FAIL을 흡수할 amendment가 없다.
  - 수정: SK-01을 폐기/역전 표현으로 바꾸는 AM-03을 추가하거나(예: "게이트가 `- 확인:` 줄을 deprecation
    주장 탐지에서 제외하지 않는다 — 출처 인용 규약으로 오탐을 막는다"), 계약 재작성 시 SK-01 문구
    자체를 이 결론에 맞게 고쳐야 한다.

### Script (4/4)
- [x] SC-01: CI validate job 8종 전부 exit 0 — PASS [exact, enumerated, L3]
  | # | 명령 | exit |
  |---|---|---|
  | 1 | `scripts/validate-plugin.py` | 0 |
  | 2 | `scripts/sync-evals.py --check-only` | 0 |
  | 3 | `scripts/sync-docs.py --check-only` | 0 |
  | 4 | `scripts/sync-orchestrator.py --check-only` | 0 |
  | 5 | `scripts/run-evals.py --verbose` | 0 (Total: 106 passed, 0 failed) |
  | 6 | `scripts/check-contrast-claims.py` | 0 |
  | 7 | `scripts/check-docs-links.py` | 0 (내부 링크 358개, 깨진 링크 0, 등록 176/176) |
  | 8 | `scripts/check-stale-values.py` | 0 |
- [x] SC-02: 7케이스 매트릭스 전수 — PASS [exact, enumerated, L3]
  | 케이스 | 파일 | G4 결과 |
  |---|---|---|
  | 삭제 예정(양성) | fail-g4-korean-delete-unsourced.md | FAIL unsourced_claims=1 |
  | 종료 예정(양성) | fail-g4-korean-shutdown-unsourced.md | FAIL unsourced_claims=1 |
  | 폐지 예정(양성) | fail-g4-korean-abolish-unsourced.md | FAIL unsourced_claims=1 |
  | 데이터 보존(오탐대조) | pass-g4-retention-notice-not-deprecation.md | PASS unsourced_claims=0 |
  | 설치 완료(오탐대조) | pass-g4-completion-phrase-not-deprecation.md | PASS unsourced_claims=0 |
  | 계정 삭제 액션(오탐대조) | pass-g4-delete-action-not-deprecation.md | PASS unsourced_claims=0 |
  | 출처 뒷받침 | pass-g4-korean-delete-sourced.md | PASS unsourced_claims=0 |
  zsh·bash 동일 결과 확인.
- [x] SC-03: `run-evals.sh`가 EVALS_PASS, 케이스 16 — PASS (AM-01 적용) [exact, L3]
  - 근거: `bash howto-kit/evals/run-evals.sh` → `EVALS total=16 pass=16 fail=0` / `EVALS_PASS`. zsh 동일.
    원 계약 리터럴은 15이나 AM-01(narrowing·unanchored, PASS 근거 가능)로 16을 기준값으로 채택.
- [x] SC-04: zsh/bash 동일 출력 — PASS [exact, L3]
  - 근거: `pass-g4-retention-notice-not-deprecation.md`에 대해 zsh/bash 각각 실행한 G1~G6 전체 출력을
    `diff`로 비교 → IDENTICAL.

### Error (2/4)
- [x] ER-03: 원장 9절 유지 — PASS [exact, L3]
  - 근거: `grep -c '^## [0-9]\.' howto-kit/references/provenance-notes.md` = 9.
- [x] ER-04: overview.html 표가 원장과 어긋나지 않음 — PASS [structural, L3]
  - 근거: `docs/howto-kit/overview.html:342-351` 표 9행이 `provenance-notes.md`의 9개 절과 1:1 일치
    (번호·제목 대조 완료).
- [x] ER-01: 오탐 원인이 스캔범위였다는 실측 문서화 — PASS (AM-02 적용) [exact, L3]
  - 근거: `docs/howto/deprecation-policy.md` §7.1(168-207행)이 "확인: 줄 제외"를 **첫 시도(과교정)**로
    서술하고 QA 사각지대 지적을 인용, 최종 해법(출처 주석 규약)으로 재서술했다. 수정 전/후 인용:
    `170-171행: "30일 지난 데이터를 삭제 예정입니다"... G4_DEPRECATION FAIL 로 잡혔다` (수정 전, 오탐)
    → `190-193행: 출처 주석 후 G4_DEPRECATION PASS unsourced_claims=0` (수정 후, 정상).
    AM-02(narrowing·unanchored, PASS 근거 가능)가 "해법이 반대로 뒤집혔다"를 정당하게 흡수한다.
- [ ] ER-02: 제외해도 양성 케이스가 여전히 잡힌다는 근거 + 구멍 없음 — **FAIL** [structural, L3]
  - 근거: 측정 요건 "같은 절에 주장이 스텝 헤더에 오면 여전히 탐지된다는 서술이 있고, SC-02의 양성
    3종이 그 증거로 인용된다"가 문서에 없다. `grep -n "헤더" docs/howto/deprecation-policy.md` → 0건
    (파일 전체). `grep -n "3종\|3 종\|매트릭스\|여전히" docs/howto/deprecation-policy.md` → 무관한
    1건("Apple 은 여전히...")만 있고 SC-02 양성 3종을 근거로 인용한 문장 없음.
  - AM-02는 "해법 방향이 뒤집혔다"만 서술했지 ER-02의 이 특정 증거 요건을 갱신하지 않았다 — 사이드카가
    원 조건의 이 하위 요건을 흡수하지 않는다.
  - 별개로, 실제 "구멍 없음" 자체는 **직접 재현으로 검증됨**: `- 확인:`에만 조작된 주장 + 무관 출처
    픽스처가 현재 코드에서 `G4_DEPRECATION FAIL unsourced_claims=1`로 정상 탐지된다(사각지대 폐쇄,
    zsh·bash 동일). 즉 **행동은 옳으나 계약이 요구하는 문서화 형태가 없다** — FAIL은 문서화 결함이지
    구현 결함이 아니다.
  - 수정: `docs/howto/deprecation-policy.md` §7.1에 "주장이 `- 확인:`이 아니라 스텝 헤더(`## S1. 구
    기능은 폐지 예정이므로...`)에 와도 여전히 탐지된다"는 서술과 SC-02 3종 양성(fail-g4-korean-*
    -unsourced.md 3파일)을 그 증거로 명시 인용.

### Architecture (5/5)
- [x] AR-01: 신규 픽스처 3종 존재 — PASS [exact, enumerated, L3]
  | 파일 | 존재 |
  |---|---|
  | pass-g4-retention-notice-not-deprecation.md | O |
  | pass-g4-completion-phrase-not-deprecation.md | O |
  | fail-g4-korean-shutdown-unsourced.md | O |
- [x] AR-02: overview.html이 README.md와 짝으로 갱신 — PASS [exact, L3]
  - 근거: `git diff --name-only origin/main...HEAD`에 `docs/howto-kit/overview.html`,
    `howto-kit/README.md` 둘 다 포함.
- [x] AR-03: step-contract.md 미변경 — PASS [exact, L3]
  - 근거: `git diff --name-only origin/main...HEAD -- howto-kit/references/step-contract.md` 빈 결과.
- [x] AR-04: .gitignore에 워크트리·result.json 추가, 추적 파일 0 — PASS [exact, enumerated, L3]
  - 근거: `.gitignore:10` `.claude/worktrees/`, `.gitignore:13` `result.json`.
    `git ls-files .claude/worktrees result.json` → 빈 결과.
- [x] AR-05: 변경 범위 == 선언 pathspec — PASS [exact, enumerated, L3]
  - 근거: `git diff --name-only origin/main...HEAD -- howto-kit docs .harness .gitignore
    ':(exclude).claude/worktrees' ':(exclude)result.json'` 결과와 `git diff --name-only
    origin/main...HEAD` 전체 결과를 정렬해 `diff` → IDENTICAL (12개 파일).

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS [exact, L3]
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` exit=0, `V6 code-fence 0 bare — OK` (howto-kit 포함 14 plugins).
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS [exact, L3]
  - 근거: `python3 scripts/validate-plugin.py` exit=0, `V1 frontmatter ... — OK` 14/14.

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private으로 만들지 않음 — PASS [L2]
  - 근거: 이번 diff는 신규 셸 함수/컴포넌트 추가 없음(토큰·픽스처·문서 변경뿐). 해당 없음으로 위반 없음.
- [x] RE-02: 기존 컴포넌트 재사용, 새 포맷 미발명 — PASS [exact, L3]
  - 근거: 신규 픽스처 3종(+ AM-01의 E16)을 기존 `pass-g4-korean-sourced.md`와 대조.
    두 파일의 `출처:` 줄 포맷이 `출처: <URL> (조회 <날짜>) — 문서에 "<용어>" 명시`로 **동일**하고
    필드 순서(어디서→무엇을→동작→값→확인→안 보이면→출처)도 동일. 새 포맷 발명 없음 — 편법 아님.

### Diagnostics (2/4, 2 N/A)
- [x] DG-01: `bash -n scripts/release.sh` / `sh -n howto-kit/scripts/howto-gate.sh` 워닝 0 — PASS
  - 근거: 둘 다 exit=0, 출력 없음.
- [x] DG-02: N/A — 계약 명시 (IDE 진단 MCP 없음, `commands.lint`=null). DG-01·SC-04로 대체 검증됨.
- [x] DG-03: `bash scripts/release.sh 2>&1 \|\| true` 콘솔 에러/예외 0 — PASS
  - 근거: `grep -iE "error|exception|traceback"` 매칭 0건.
- [x] DG-04: N/A — 계약 명시 (플러그인 모노레포, SC-02가 런타임 검증 대신함).

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (24-0)/24 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (미검증 카운터 REJECT 사유 아님 — REJECT는 SK-01·ER-02 FAIL 때문)

## Discrimination
- 규칙 12의 9항(동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고-테스트충돌) 해당 조건 없음 — 게이트 자체다 판별력 검증은 과제 지시에 따라 별도 적대적 재현으로 수행함(위 ER-01/ER-02 근거 참조: 반전 코드 대비 실행 결과 대조 완료).

## User-Reported Failures
- 해당 없음 (이번 재평가는 QA 자체 판정, 사용자 결함 보고 없음)

## Evidence Validity
- 검사 대상 증거: 24건 (조건별 1개 이상, SC-01/SC-02는 다중 하위 실행)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: SC-02(7건) · SC-04(1건) · ER-01/ER-02 재현(2건, exempted-code vs current-code) · 사각지대 재현(2건) 모두 zsh·bash 양쪽 실행 확인. 나머지는 zsh(도구 기본 셸)로 실행, 셸 종속성 없는 grep/awk/python 명령이라 bash 이중검증 생략.
- 무효 0건 — 미검증 카운터 변화 없음

## Summary
- Total: 22/24 conditions passed
- Verdict: REJECT
- FAIL 2건:
  1. **SK-01** — 게이트가 `- 확인:` 줄을 deprecation 탐지에서 제외해야 하는데, 구현은 QA(Iteration 1)
     지적을 수용하며 이 제외를 **의도적으로 되돌렸다**. 계약 문구와 구현이 정면으로 반대다. 이 FAIL을
     흡수할 amendment가 없다 — AM-02는 ER-01·ER-02만 대상으로 선언했다.
  2. **ER-02** — "구멍 없음"의 실제 동작은 재현 검증했지만(사각지대 폐쇄 확인), 계약이 요구하는
     특정 증거 형태(스텝 헤더 서술 + SC-02 3종 인용)가 문서에 없다. 문서화 결함.
- 수정 우선순위:
  1. SK-01을 다루는 AM-03 사이드카를 추가하거나(narrowing/relaxing 판정 포함), 다음 계약 개정에서
     SK-01 문구를 최종 해법(출처 주석 규약)에 맞게 재작성한다.
  2. `docs/howto/deprecation-policy.md` §7.1에 스텝 헤더 탐지 지속 서술 + SC-02 3종 인용을 추가한다.

## Improvement Suggestions
- [SK-01] 검증경로-미기재 — AM-02가 ER-01·ER-02의 "해법 방향 반전"을 흡수했음에도 동일 반전의 영향을
  받는 SK-01은 사이드카 대상에서 누락됐다. 다음 사이클에서 SK-01을 "게이트가 `- 확인:` 줄을 deprecation
  주장 탐지에서 제외하지 **않는다** — 대신 `- 출처:` 줄의 인용 주석으로 오탐을 방지한다"로 재작성 권장.
- [ER-02] 태그-산출물-불일치 — 측정이 "스텝 헤더 서술 + SC-02 3종 인용"이라는 구체적 문서 산출물을
  요구하는데, 실제 문서(§7.1)는 그 형태를 갖추지 않고도 같은 절의 다른 곳(§4)에서 유사 내용을 다룬다.
  다음 계약에서는 "§7.1에 아래 요소가 모두 있어야 한다"처럼 위치까지 고정하거나, 반대로 파일 전체
  범위로 완화해 위치 종속성을 없앨 것을 권장.
- [AM-01] 측정-방식-불일치 — eval 케이스 ID 문자열 개명(E13)이 raw-string 비교에서는 `relaxing`으로
  반전되는데 사이드카는 이 반전 가능성을 문서화하지 않았다. 다음 사이드카부터는 "id 개명이 있는 경우
  behavior 튜플(fixture+assertions+expect_final)로 정규화해 비교했다"는 방법론 문장을 명시할 것.

## Cross Diagnosis
- cross_diagnosis_by: sprint-contract (미실행 — 이 실행 환경에 Task/Agent 도구가 제공되지 않아 서브
  에이전트 스폰 불가. Read/Bash만 사용 가능). 자기진단(Step 6)으로 대체.

## Self-Diagnosis (Step 6)
- l3_unreached: false — 24개 조건 전부 L3(의미 추적/재현)까지 도달. SK-01/ER-02는 코드·문서를 직접
  대조하고 반례(exempted-code vs current-code, blindspot fixture)를 실행해 재현했다.
- bias_detected: false — SC-01/SC-02/SC-04/AR-05 등 대부분 PASS이지만 SK-01·ER-02를 관대하게
  덮지 않고 FAIL로 유지. amendment 적용 범위를 조건별로 엄격히 구분했다(AM-02가 ER-01·ER-02만
  선언했음에도 SK-01까지 봐주지 않음).
- evidence_missing: false — 전 조건 파일:라인 또는 명령 출력 인용.
- contract_misinterpret: 낮음 — SK-01/ER-02 FAIL이 "계약이 틀렸다"는 방향일 수 있어 리스크가 있으나,
  Step 3.3 규칙(원 조건을 amendment 없이 임의로 무효화하지 않는다)을 따라 문자 그대로 판정했다.
- perspective_gap: false — 기능(SC-02 매트릭스) + 보안/적대적(사각지대 재현) + 문서(ER-01/ER-02) +
  구조(AR-05 diff-scope) 4관점에서 점검.
