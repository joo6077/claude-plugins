# Sprint Feedback
Feature: howto-kaizen 1 사이클 — G4 주장 탐지 정밀화 · 미확정 원장 인덱스 동기화
Evaluated: 2026-09-10 15:20
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-howto-kaizen-g4-precision.md
- sha256: 2446f0321cc85aa297a7b6de8ae9859d6f38a59984a460573de84f81789bd33c
- status: active
- slug: howto-kaizen-g4-precision
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (owner_session 도 일치 — ladder 2 로도 유일 성립)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT)

## Amendments
- amendments: 0 (사이드카 없음, 확인됨)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (스프린트 윈도우 14:20 이후 로그된 추가 사용자 prompt 없음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (3/3)
- [x] SK-01: 게이트가 `- 확인:` 줄을 deprecation 주장 탐지에서 제외 — PASS
  - 근거: `howto-kit/scripts/howto-gate.sh:89` `if ($0 !~ /^- 확인:/ && $0 ~ dep) dep_claim = 1`. 이유 주석 `:85-88`.
- [x] SK-02: `HOWTO_DEP` 에 `종료 예정` 추가, `삭제`/`종료` 단독 없음 — PASS
  - 근거: `howto-kit/scripts/howto-gate.sh:23` `HOWTO_DEP='...|삭제 예정|삭제가 예정|종료 예정'`. 파이프 분해 후 정확히 `삭제`/`종료` 인 토큰 0건 (grep -nx 확인).
- [x] SK-03: README "이 킷이 사실로 말하지 않는 것" 절이 원장 절 수(9)를 정확히 서술 — PASS
  - 근거: `awk` 비-범위형 추출 결과에 "현재 9 절" 등장, 옛 서술 문자열 전체 파일 기준 0건.

### Script (3/4)
- [x] SC-01: CI validate job 8종 전수 exit 0 — PASS
  - 근거(직접 실행): validate-plugin.py=0, sync-evals.py --check-only=0, sync-docs.py --check-only=0, sync-orchestrator.py --check-only=0, run-evals.py --verbose=0 (106 passed/0 failed), check-contrast-claims.py=0, check-docs-links.py=0 (내부링크 358·깨진링크 0·내비 176/176), check-stale-values.py=0.
- [ ] SC-02: 게이트 변경이 7 케이스 매트릭스를 모두 만족한다 — **FAIL**
  - 근거: 계약이 명시한 양성 3종은 `삭제 예정` · `종료 예정` · `폐지 예정`(근거 없음) 이다 [exact, enumerated]. 실제 커밋된 픽스처/`evals.json` 전체에서 리터럴 `폐지 예정` 을 grep 하면 **0건** (`grep -rn "폐지 예정" howto-kit/ docs/` → 매치 없음). 7번째 슬롯으로 실제 쓰인 것은 기존(이번 스프린트 이전부터 있던) `fail-g4-deprecation-ko.md` 이며 그 안의 토큰은 `지원 종료` 다 — `폐지 예정` 이 아니다. `evals.json` 신규분(E13/E14/E15) 3건도 데이터 보존·설치 완료·종료 예정만 다루고 `폐지 예정` 케이스는 어디에도 없다.
  - 참고(기능 자체는 정상): QA 가 직접 만든 적대적 픽스처(`폐지 예정` 근거 없음, 스크래치패드)로 실행한 결과 `G4_DEPRECATION FAIL unsourced_claims=1` 로 올바르게 잡힌다 — **기능적 결함은 아니고, 계약이 요구한 리터럴 7번째 케이스가 산출물에 커밋되지 않은 것**이다.
  - 수정: `howto-kit/evals/fixtures/` 에 `폐지 예정` 근거 없음 전용 픽스처를 추가하고 `evals.json` 에 등록하거나(케이스 16), 계약 SC-02 문구의 세 번째 토큰을 실제 구현이 쓰는 `지원 종료` 로 정정한다(어느 쪽이든 리터럴 일치가 필요).
- [x] SC-03: `sh howto-kit/evals/run-evals.sh` → EVALS_PASS, 15케이스 — PASS
  - 근거: 실행 출력 `EVALS total=15 pass=15 fail=0` + `EVALS_PASS` (E1~E15 전부 PASS 나열).
- [x] SC-04: 게이트가 zsh·bash 동일 출력 — PASS
  - 근거: `pass-g4-retention-notice-not-deprecation.md` · `fail-g4-korean-shutdown-unsourced.md` · `pass-fcm-ios.md` 3종에 대해 `zsh -c` vs `bash -c` 로 `howto_gate` 직접 실행, `diff` 결과 모두 동일 (IDENTICAL).

### Error (4/4, 단 아래 Critical Finding 참조)
- [x] ER-01: 오탐 원인이 토큰이 아니라 스캔 범위였다는 실측이 문서에 남음 — PASS
  - 근거: `docs/howto/deprecation-policy.md:169-186` 수정 전/후 `G4_DEPRECATION FAIL`→`PASS` 인용 + "게이트가 `- 확인:` 줄까지 주장으로 세고 있던 것" 서술.
- [x] ER-02: `확인:` 제외해도 양성 케이스가 여전히 잡힌다는 근거 명시 — PASS (계약 리터럴 기준. **아래 Critical Finding 참조 — 이 조건의 측정 범위 자체가 좁다**)
  - 근거: 같은 절 "주장이 스텝 헤더나 다른 필드에 오면 여전히 잡힌다 — 양성 3 종(...)이 수정 후에도 FAIL 이다" 서술 존재. SC-02 양성 케이스가 그 증거로 인용됨.
- [x] ER-03: 원장 9절이 줄지 않음 — PASS
  - 근거: `grep -cE '^## [0-9]\.' howto-kit/references/provenance-notes.md` → `9`.
- [x] ER-04: overview.html 표가 원장과 어긋나지 않음 — PASS
  - 근거: `docs/howto-kit/overview.html:343-351` 표에 §1~§9 전부 열거, "전체는 `references/provenance-notes.md` 가 정본" 포인터 병기. README.md 와 항목·순서 일치.

### Architecture (5/5)
- [x] AR-01: 신규 픽스처 3종 존재 — PASS
  - 근거: `test -f` 3건 모두 존재 확인 (pass-g4-retention-notice-not-deprecation.md, pass-g4-completion-phrase-not-deprecation.md, fail-g4-korean-shutdown-unsourced.md).
- [x] AR-02: overview.html 이 README.md 와 짝으로 갱신 — PASS
  - 근거: `git diff --name-only origin/main...HEAD` 에 두 파일 모두 포함.
- [x] AR-03: step-contract.md 변경 없음 — PASS
  - 근거: `git diff --name-only origin/main...HEAD -- howto-kit/references/step-contract.md` 출력 없음.
- [x] AR-04: .gitignore 에 두 항목 추가, 추적 파일 0 — PASS
  - 근거: `.gitignore` tail 에 `.claude/worktrees/` · `result.json` 존재. `git ls-files .claude/worktrees result.json` 출력 없음(추적 안 됨).
- [x] AR-05: 변경 범위가 선언 경로와 정확히 일치 — PASS
  - 근거: scoped pathspec 집합과 전체 diff 집합을 `diff` 로 비교 → IDENTICAL (10개 파일 모두 일치).

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` → 전 14플러그인 `0 bare — OK`.
- [x] AP-04: frontmatter name 필드 누락 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py` 전체 exit 0, 14 plugins 14 OK (howto-kit 포함 V1 정상).

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private 처리하지 않음 — PASS (구조적, 신규 공유 컴포넌트 없음)
- [x] RE-02: 기존 픽스처 포맷을 그대로 따름 — PASS
  - 근거: 신규 3픽스처의 필드 라벨 순서(`대상/조회일/어디서/무엇을/동작/값/확인/안 보이면/출처`)가 기존 `pass-g4-korean-delete-sourced.md` 와 동일.

### Diagnostics (4/4)
- [x] DG-01: 워닝 0개 — PASS
  - 근거: `bash -n scripts/release.sh` exit 0, `sh -n howto-kit/scripts/howto-gate.sh` exit 0.
- [x] DG-02: N/A — 검증됨 (project.yaml `commands.lint: null` 확인, IDE 진단 MCP 없음)
- [x] DG-03: 콘솔 에러/예외 0개 — PASS
  - 근거: `bash scripts/release.sh 2>&1` 출력에 대해 `grep -inE "error|exception|traceback"` → 매치 없음 (사용법 안내만 출력).
- [x] DG-04: N/A — 검증됨 (플러그인 모노레포, SC-02 게이트 실행이 런타임 검증 대신함)

## Critical Finding — 적대적 탐색으로 발견한 게이트 홀 (조건 밖, REJECT 사유에 포함)

`- 확인:` 줄을 deprecation 주장 탐지에서 전면 제외한 결과, **`확인:` 줄에만 조작된(fabricated)
deprecation 주장을 적으면 출처와 무관하게 항상 G4 를 통과한다.**

재현 (QA 직접 작성 픽스처, 레포에 커밋되지 않음 — 스크래치패드 전용):

```text
## S1. 구 버전 API 키를 재발급한다
...
- 확인: 이 기능은 폐지 예정이니 서두르라는 안내가 뜬다
- 출처: https://example.com/docs/api-keys (조회 2026-09-10)   ← deprecation 과 무관한 일반 문서
```

실행 결과: `G4_DEPRECATION PASS unsourced_claims=0`, `GATE_PASS`.

수정 전(이번 스프린트 이전) 게이트라면 이 케이스는 `dep_claim=1`(캐치올이 모든 줄을 셈) +
`dep_src=0`(출처 줄이 deprecation 을 언급하지 않음) 이 되어 `G4_DEPRECATION FAIL` 로 잡혔을
것이다. 즉 이번 수정은 "데이터 보존 안내 오탐" 을 없애는 대신, **"확인: 줄에 적힌 조작된
주장은 절대 못 잡는다"는 새 사각지대**를 만들었다.

ER-02 의 계약 리터럴 측정("주장이 스텝 헤더에 오면 여전히 탐지된다")은 이 시나리오를 요구하지
않으므로 문면상 PASS 하지만, ER-02 가 스스로 내세우는 "구멍을 만들지 않았다"는 주장의 실질은
이 시나리오에서 깨진다 — `확인:` 필드 자체가 새로 뚫린 유일한 구멍이기 때문이다.

무엇을:/값:/동작: 줄에 있는 주장은 여전히 정상적으로 잡힌다 (adv2/adv3 직접 재현, 아래 참조).
다중 스텝 중 1개만 위반인 케이스의 카운트도 정확하다 (adv4, unsourced_claims=1).

**권장**: `확인:` 줄 전체를 면제하는 대신, "그 줄이 deprecation 성격 주장을 담고 있으면 같은
스텝의 `출처:` 줄도 deprecation 관련 근거를 담아야 한다"는 조건부 규칙으로 좁히거나, 최소한
이 사각지대를 `provenance-notes.md`/`deprecation-policy.md` 에 "알려진 잔여 갭"으로 명시해야
한다. 현재 문서는 이 사각지대를 언급하지 않는다.

## 종료 단독 토큰 재현 (SK-02 근거 검증)

과제 지시대로 `종료` 단독을 토큰에 추가해 재현·원복했다:
- 기존 픽스처 `pass-g4-completion-phrase-not-deprecation.md` 자체는 "설치가 종료됩니다" 가
  `확인:` 줄 안에 있어, 이미 그 줄이 면제 대상이라 바로 이 픽스처만으로는 재현되지 않았다
  (여전히 `G4_DEPRECATION PASS`).
- 그러나 같은 문구를 스텝 **헤더**(`## S1. 설치 진행 후 종료한다`)나 스텝 안의 **일반 서술
  줄**(필드 접두 없는 자유 텍스트)에 두면 `종료` 단독 추가 시 즉시 `G4_DEPRECATION FAIL` 로
  오탐한다 — 원본(`종료 예정`만 있음) 은 같은 입력에서 `PASS` 를 유지한다. 재현 확인됨,
  코드 주석의 근거는 유효하다 (단, 인용된 기존 픽스처 자체는 최선의 재현 사례는 아니었다).
- 두 토큰 세트 모두 스크래치패드 임시 파일로만 테스트했고 원본 `howto-gate.sh` 는 변경 없이
  그대로 복원했다 (`git diff` 로 원상 확인).

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 24/24 = 1.00 (임계 0.60 충족)
- Verdict 영향: 통상 (전 조건 정적/실행 검증 완료, [미검증] 마커 없음)

## Discrimination (규칙 12 적용 조건 — SC-02/ER-02, "입력 검증" 범주로 판단)
- 결합 확인: `howto-kit/evals/run-evals.sh:39-40` 이 `. "$GATE"; howto_gate` 로 실제 게이트
  함수를 zsh·bash 양쪽에서 직접 호출 — 로직 재구현 없음, 결합 확인됨.
- 음성 대조: 계약 SC-01(`docs/index.html` 등록 제거 시 FAIL)·SC-04(`set -- $var` 형태 시
  zsh 만 결과 갈림) 에 명시됨.

## User-Reported Failures
- 해당 없음 (이번 평가는 최초 라운드이며 사용자 실패 보고 없음).

## Evidence Validity
- 검사 대상 증거: 24건 (조건별) + Critical Finding 1건
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 다수 건 (howto_gate 직접 호출, 8개 CI 스크립트, run-evals.sh) ·
  zsh/bash 양쪽 확인 3건(SC-04) · 미실행 0건
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 23/24 conditions passed
- Verdict: REJECT
- FAIL 항목: SC-02 (7 케이스 매트릭스 중 `폐지 예정` 근거 없음 리터럴 픽스처 누락)
- 추가 필수 확인 사항(REJECT 미해결 시 재발 위험): `확인:` 줄 전면 면제로 인한 조작 주장
  사각지대 (Critical Finding 참조) — 재제출 시 함께 검토 요망.
- 수정 우선순위: (1) SC-02 픽스처/계약 문구 정합 (2) `확인:` 사각지대 문서화 또는 조건부 규칙
  으로 좁히는 방안 검토.

## Improvement Suggestions
- [SC-02] 증거-경로-부재 — 계약이 리터럴로 요구한 `폐지 예정` 근거 없음 케이스의 실제 픽스처
  파일을 `howto-kit/evals/fixtures/`에 추가하고 `evals.json`에 16번째 케이스로 등록하거나,
  계약 문구의 세 번째 토큰을 구현이 실제로 커버한 `지원 종료`로 정정한다.
- [ER-02] 범위-미명시 — "구멍을 만들지 않았다"의 측정 범위가 "헤더에 오면 잡히는가"로만
  좁혀져 있어 "확인: 줄 자체에 조작된 주장이 있고 출처가 무관한 경우"를 검증하지 않는다.
  다음 사이클에서 이 시나리오를 명시적 서브체크로 추가하거나, deprecation 성격 확인: 줄은
  같은 스텝의 출처: 줄도 deprecation 토큰을 포함해야 한다는 조건부 규칙 도입을 검토한다.
