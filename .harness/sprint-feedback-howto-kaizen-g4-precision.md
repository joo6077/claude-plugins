# Sprint Feedback
Feature: howto-kaizen 1 사이클 — G4 주장 탐지 정밀화 · 미확정 원장 인덱스 동기화
Evaluated: 2026-09-11 11:25
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: .harness/sprint-contract-howto-kaizen-g4-precision.md
- sha256: 2446f0321cc85aa297a7b6de8ae9859d6f38a59984a460573de84f81789bd33c
- status: active
- slug: howto-kaizen-g4-precision
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session 4d264694-eb0e-4e84-801f-52b2db804772 == 현재 세션)
- legacy_contract_used: false
- seal_status: SEAL_OK (조건 열거 정규식 `^- \[[ x]\] [A-Z]{2,}-[0-9]{2}` 로 재계산 — rec=bcf7e7535ec1a339 act=bcf7e7535ec1a339)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 sha256/status 동일)
- status_transition: active -> done (APPROVE 이므로 전환)

## Amendments
- amendments: 3 (AM-01, AM-02, AM-03 — AM-03 이번 iteration 신규)
- PASS 근거 가능: 3 [AM-01 narrowing·unanchored → SC-03 / AM-02 narrowing·unanchored → ER-01·ER-02 /
  AM-03 narrowing·unanchored → SK-01]
- PASS 근거 불가: 0
- AM-03 direction 재현 (자기신고 아님, 직접 재계산):
  - 근거 코드 diff 직접 확인: `git show f99c181 -- howto-kit/scripts/howto-gate.sh` 가
    `if ($0 !~ /^- 확인:/ && $0 ~ dep) dep_claim = 1` (확인 줄 제외, 계약 SK-01 리터럴 요구)를 도입했고,
    `git show 5de075f -- howto-kit/scripts/howto-gate.sh` 가 그 제외 조건만 제거해
    `if ($0 ~ dep) dep_claim = 1` (확인 줄 포함)로 되돌렸다 — diff 상 순수 조건 제거 1건, 그 외 스캔
    대상 변화 없음.
  - 사이드카가 제시한 필드 집합 파일(스캔 필드 6개 vs 7개, +확인)을 직접 재구성해 재현:
    ```
    $ amend_direction_oracle fld_orig.txt fld_new.txt
    narrowing measured_removed=0 measured_added=1
    ```
    (evaluator 가 스크립트에서 그대로 정의·실행, 사이드카 출력과 일치)
  - 헬퍼 선택 타당성: SK-01은 게이트(오라클)가 스캔하는 "재는 것의 집합" 을 바꾸는 조건이다.
    확인 줄이 스캔 대상에 추가되면 더 많은 문서가 걸리므로(통과 집합 축소) `narrowing` 이 맞다 —
    diff-scope 오라클이 아니어도 "오라클이 재는 집합" 이라는 동일 구조라 `amend_direction_oracle`
    적용이 타당하다. AM-01·AM-02 에서 이미 같은 근거로 수용된 헬퍼 선택과 일치한다.
  - direction×consent 표 대조: `narrowing` 은 `anchored`/`unanchored` 무관하게 PASS 근거 가능
    (contract-schema.md:846). AM-03 은 `unanchored` 이나 앵커를 지어내지 않고 명시했다 — 표에
    맞는 처리.

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md) — 재사용 (직전
  iteration 값, 이번 회차는 사용자 지시로 예산 절약 대상에서 제외)
- unreflected_corrections: 0 (직전 iteration 스크리닝 결과 재사용, `[샘플링-키워드스캔]`)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (3/3)
- [x] SK-02: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] SK-03: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] SK-01: 게이트가 `- 확인:` 줄을 deprecation 주장 탐지에서 제외한다 — **PASS (AM-03 적용)**
  [exact, L3, REOPENED→RESOLVED]
  - AM-03 이 SK-01 의 요구를 "제외한다" → "제외하지 않는다" 로 반전시켰다 (narrowing·unanchored,
    PASS 근거 가능 — 위 Amendments 절 참조). 반전된 요구를 기준으로 재판정한다.
  - 코드: `grep -n 'dep_claim = 1' howto-kit/scripts/howto-gate.sh` → 78행(헤더 블록,
    `if ($0 ~ dep) dep_claim = 1`), 91행(캐치올 블록, `if ($0 ~ dep) dep_claim = 1`). 두 줄 다
    `확인` 제외 조건 없음 — AM-03 이 재정의한 "제외하지 않는다" 요구와 일치.
  - 동적 재현(적대적 픽스처 신규 생성, `- 확인:` 줄에만 조작된 주장 + 무관 출처):
    ```
    $ zsh -c '. howto-kit/scripts/howto-gate.sh; howto_gate adversarial-blindspot.md'
    G4_DEPRECATION FAIL unsourced_claims=1
    $ bash -c '. howto-kit/scripts/howto-gate.sh; howto_gate adversarial-blindspot.md'
    G4_DEPRECATION FAIL unsourced_claims=1
    ```
    확인 줄에만 있는 조작 주장이 zsh·bash 양쪽에서 정상 탐지됨 — AM-03 반전 요구 충족을 실행으로 확인.

### Script (4/4)
- [x] SC-01: CI validate job 8종 전부 exit 0 — **PASS, 이번 iteration 재실행**
  | # | 명령 | exit |
  |---|---|---|
  | 1 | `scripts/validate-plugin.py` | 0 |
  | 2 | `scripts/sync-evals.py --check-only` | 0 |
  | 3 | `scripts/sync-docs.py --check-only` | 0 |
  | 4 | `scripts/sync-orchestrator.py --check-only` | 0 |
  | 5 | `scripts/run-evals.py --verbose` | 0 |
  | 6 | `scripts/check-contrast-claims.py` | 0 |
  | 7 | `scripts/check-docs-links.py` | 0 |
  | 8 | `scripts/check-stale-values.py` | 0 |
- [x] SC-02: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] SC-03: PASS (AM-01 적용) — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] SC-04: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)

### Error (4/4)
- [x] ER-03: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] ER-04: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] ER-01: PASS (AM-02 적용) — **재확인**: `git diff 5de075f..43aa77f -- docs/howto/deprecation-policy.md`
  로 이번 iteration 변경분이 §7.1 뒤쪽에 신규 서브섹션만 추가했을 뿐, ER-01 이 인용한 원인
  서술(170-197행 부근, "확인: 줄까지 세는 것이 원인" + 수정 전 FAIL(170-171행)/수정 후 PASS(190-193행))은
  변경되지 않았음을 diff로 확인. 직전 판정 유효.
- [x] ER-02: 제외해도 양성 케이스가 여전히 잡힌다는 근거 + 구멍 없음 — **PASS**
  [structural, L3]
  - `docs/howto/deprecation-policy.md` §7.1 에 신규 서브섹션 "구멍을 만들지 않았다 — 주장은 어느
    필드에 와도 잡힌다" (199-217행)가 추가됨. "면제를 되돌렸으므로 주장이 스텝 헤더에 오면 여전히
    탐지된다" 서술 + SC-02 양성 3종(fail-g4-korean-delete/shutdown/abolish-unsourced.md)을 표로
    인용 — 계약이 요구한 두 요소(스텝 헤더 탐지 서술 · 양성 3종 인용) 모두 충족.
  - 표의 주장을 1건이 아니라 **3건 전부** 직접 재현(양성 3종이 실제로 문서가 주장하는 "스텝 헤더"
    위치에 있는지 + 결과가 FAIL인지):
    ```
    $ grep -n "^##" fail-g4-korean-delete-unsourced.md   → "## S1. 구 기능은 삭제 예정이므로..."
    $ grep -n "^##" fail-g4-korean-shutdown-unsourced.md → "## S1. 구 기능은 종료 예정이므로..."
    $ grep -n "^##" fail-g4-korean-abolish-unsourced.md  → "## S1. 구 기능은 폐지 예정이므로..."
    (3종 모두 zsh/bash) G4_DEPRECATION FAIL unsourced_claims=1
    ```
    문서 표의 주장과 실제 실행 결과가 정확히 일치 — narrated 서술이 아니라 실행 재현으로 검증.

### Architecture (5/5)
- [x] AR-01: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] AR-02: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] AR-03: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] AR-04: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] AR-05: 변경 범위 == 선언 pathspec — **PASS, 이번 iteration 재실행**
  - 근거: `git diff --name-only origin/main...HEAD -- howto-kit docs .harness .gitignore
    ':(exclude).claude/worktrees' ':(exclude)result.json'` (12개 파일)과
    `git diff --name-only origin/main...HEAD` 전체(12개 파일)를 정렬해 `diff` → IDENTICAL.
    이번 iteration 추가분(`.harness/sprint-amendments-*.md` 갱신, `docs/howto/deprecation-policy.md`
    갱신)도 선언 pathspec 안에 있어 드리프트 없음.

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — **PASS, 이번 iteration 재실행** (`python3 scripts/validate-plugin.py
  --check=code-fence` exit=0, `V6 code-fence 0 bare — OK` 14/14 plugins)
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS (SC-01 #1 `validate-plugin.py` 전체 실행 exit=0 에
  V1 포함 확인됨, 재사용)

### Reusability (2/2)
- [x] RE-01: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] RE-02: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)

### Diagnostics (2/4, 2 N/A)
- [x] DG-01: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] DG-02: N/A — 계약 명시, 재사용
- [x] DG-03: PASS — 재사용 (직전 근거, 이번 diff 미변경 대상)
- [x] DG-04: N/A — 계약 명시, 재사용

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (24-0)/24 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination
- 규칙 12의 9항(동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고-테스트충돌)
  해당 조건 없음. 다만 SK-01·ER-02 는 "적대적 사각지대" 성격이 있어 실행 기반 결합 확인을 별도 수행함
  (아래 참조).
- 결합 확인: SK-01 — 신규 적대적 픽스처(`- 확인:` 줄에만 조작 주장)를 `. howto-kit/scripts/howto-gate.sh`
  경유로 직접 실행해 `dep_claim`/`dep_src` 로직을 통과, 구현을 직접 경유함을 확인 (grep 으로 대체하지
  않고 실행).
- 음성 대조: 계약 SK-01/ER-02 모두 명시적 "음성 대조" 절은 없으나, 코드 diff(f99c181→5de075f)로 "확인
  줄 제외 조건을 넣으면 이 픽스처가 PASS로 통과한다"는 반증을 이미 f99c181/5de075f 커밋 메시지가
  실측했고(면제 상태 재현: `G4_DEPRECATION PASS unsourced_claims=0`), 이번 재현(철회 후)에서 동일
  픽스처가 `FAIL`로 바뀌는 것을 확인함 — 무력화 시 다른 결과가 남을 것이 이미 실측으로 입증됨.

## User-Reported Failures
- 해당 없음

## Evidence Validity
- 검사 대상 증거: SK-01, ER-02, SC-01(8건), AR-05, AP-03 — 이번 iteration 신규/재실행 대상 12건
  (나머지 19개 조건은 diff 미변경 대상이라 직전 근거 재사용, 재사용 표기 명시)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: SK-01 적대적 픽스처(zsh+bash), ER-02 양성 3종(zsh+bash 각 3건=6회) 모두 직접
  실행. SC-01 8종은 zsh(도구 기본 셸)로 실행 — 셸 종속성 없는 python 명령이라 bash 이중검증 생략.
  AR-05/AP-03 은 git/python 명령으로 셸 비종속.
- 무효 0건

## Summary
- Total: 24/24 conditions passed
- Verdict: APPROVE
- Iteration 2 REJECT 사유 2건 모두 해소:
  1. SK-01 — AM-03 사이드카(narrowing·unanchored, PASS 근거 가능)가 SK-01 을 명시적으로 대상 선언.
     direction 계산을 코드 diff 직접 대조 + 필드집합 재구성 실행으로 재현, 헬퍼 선택 타당성도
     AM-01/AM-02 선례와 일치함을 확인. 반전된 요구를 실제 코드/실행이 충족함을 적대적 픽스처로
     zsh·bash 양쪽 재현.
  2. ER-02 — `docs/howto/deprecation-policy.md` §7.1 에 요구된 서술(스텝 헤더 탐지 지속)과 SC-02
     양성 3종 표 인용이 추가됨. 표의 3건 주장을 개별 실행 재현해 문서-실행 일치를 확인.
- 회귀 없음: ER-01(diff로 미변경 확인) · AR-05(전체 diff-scope IDENTICAL 재확인) · SC-01(8종 재실행
  전부 exit 0) · 계약 봉인(SEAL_OK, 조건 문구 무변조).

## Improvement Suggestions
- [AM-01] 측정-방식-불일치 — Iteration 2 에서 지적한 raw-id 반전 위험을 이번 사이드카가 명시적으로
  기록했다(behavior 튜플 정규화 기준 서술). 해소됨 — 재발 시에만 재기록.
- 신규 없음. 이번 iteration 은 직전 REJECT 사유 2건을 정확히 겨냥한 최소 수정이었고, 회귀 검사에서도
  추가 결함이 발견되지 않았다.

## Cross Diagnosis
- cross_diagnosis_by: sprint-contract (미실행 — 이 실행 환경에 Task/Agent 도구가 제공되지 않아
  서브에이전트 스폰 불가). 자기진단(Step 6)으로 대체.

## Self-Diagnosis (Step 6)
- l3_unreached: false — 재실행 12건 전부 L3(코드 diff 대조 + 실행 재현). 재사용 19건은 직전 iteration에서
  이미 L3 도달, 이번 diff 로 그 근거가 무효화되지 않음을 diff 대조로 확인(ER-01/AR-05/SC-01은 명시 재실행).
- bias_detected: false — SK-01/ER-02 를 amendment 존재만으로 관대하게 PASS 처리하지 않고, 코드 diff
  직접 확인 + 독립 적대적 픽스처 실행으로 검증했다. AM-03 의 헬퍼 선택도 재검산했다(사이드카 출력을
  그대로 믿지 않음).
- evidence_missing: false — 전 조건 파일:라인 또는 명령 출력 인용, 재사용 조건은 재사용임을 명시.
- contract_misinterpret: false — AM-03 이 SK-01 요구를 반전시켰음을 direction×consent 표(narrowing
  은 anchored 무관 PASS 근거 가능)와 대조해 확인 후 반전된 요구로 재판정했다. 원 조건을 임의 무효화
  하지 않고 사이드카 경유로만 재해석했다.
- perspective_gap: false — 코드(diff 직접대조) + 실행(zsh/bash 적대적 재현) + 문서(ER-02 서술/표
  대조) + 구조(AR-05 diff-scope) 4관점 점검.
