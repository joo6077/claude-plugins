# Sprint Feedback
Feature: `/howto-research` 5 사이클 — deprecation-policy 확정 · G4 false negative 수정
Evaluated: 2026-09-10 (독립 QA)
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-howto-research-deprecation-policy.md
- sha256: 394ac66e466c021397d766ee48aab20cdbdd6629eadd2109a792dba2e1c91c90
- status: active
- slug: howto-research-deprecation-policy
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 시 HARNESS_CONTRACT 상당 절대경로 지정, owner_session 도 일치)
- legacy_contract_used: false
- seal_status: SEAL_OK (verify_seal 실행 확인, contract-schema.md 정의 함수 그대로 사용)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256/status 동일, TOCTOU 없음)
- status_transition: active -> done (APPROVE 이므로 전환)

## Amendments
- amendments: 0 (사이드카 파일 부재 확인 — `ls .harness/sprint-amendments-howto-research-deprecation-policy.md` no such file)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (스프린트 시간대(2026-09-10 11:04~) 내 세션 4d264694 프롬프트는 "ㄱㄱ" 뿐이며 별도 교정 지시 없음. 로그가 12:10 이후로는 아직 harvest 안 됨 — Stop 훅 비동기 특성)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (3/3)
- [x] SK-01: `howto-gate.sh` 의 `HOWTO_DEP` 에 `삭제 예정`·`삭제가 예정` 추가, `삭제` 단독 없음 — PASS
  - 근거: `grep -o "HOWTO_DEP='[^']*'" howto-kit/scripts/howto-gate.sh` → `...|삭제 예정|삭제가 예정'`. 파이프 분리 시 정확히 `삭제` 인 항목 없음 (L3, 실행 확인)
- [x] SK-02: `source-tiers.md` deprecation 절 — 약속/관행 구분 + 한국어 매핑 — PASS
  - 근거: `awk` 절 추출 → `at least 12 months` 1회, `typically 12 months` 2회, `지원 중단됨` 2회 (L3, awk 범위형 미사용 확인)
- [x] SK-03: `step-contract.md` 마커 정본 무변경 — PASS
  - 근거: `git diff --name-only origin/main...HEAD -- howto-kit/references/step-contract.md` 빈 출력 (L3)

### Script (4/4)
- [x] SC-01: CI validate 8종 exit 0 — PASS
  - 근거: validate-plugin.py/sync-evals/sync-docs/sync-orchestrator/run-evals/check-contrast-claims/check-docs-links/check-stale-values 전부 exit=0 직접 실행 확인. 음성 대조: `docs/index.html` 573행 제거 후 `check-docs-links.py` 재실행 → exit=1 `고아 (내비 미등록): howto-kit/deprecation-policy.html` 확인, 파일 원상복구 후 `git diff --exit-code` clean 확인 (L3, 실행+음성대조)
- [x] SC-02: 게이트 토큰 3방향 대조 — PASS
  - 근거: `. howto-kit/scripts/howto-gate.sh` 로드 후 3개 픽스처 직접 실행 —
    (a) fail-g4-korean-delete-unsourced.md → `G4_DEPRECATION FAIL unsourced_claims=1`
    (b) pass-g4-korean-delete-sourced.md → `G4_DEPRECATION PASS unsourced_claims=0`
    (c) pass-g4-delete-action-not-deprecation.md → `G4_DEPRECATION PASS unsourced_claims=0`
    계약이 요구한 3방향과 정확히 일치 (L3, 실행 재현)
  - 추가 검증 (SC-02 문언 요구를 넘어선 적대적 탐색, 결과는 조건 판정에 미반영 — Improvement 항목 참조):
    토큰 되돌리기(narrow 제거) → fail 픽스처가 `PASS unsourced_claims=0` 으로 복귀 확인 (ER-04 사전상태 실측 재현)
    표준 `삭제` 단독 토큰 추가 → 정상 계정삭제 픽스처가 `FAIL unsourced_claims=2` 로 깨짐 확인 (범위 경계의 근거 문장 실측 검증)
    **잔여 오탐 발견**: "30일 지난 데이터를 삭제 예정입니다" 류 정상 데이터 보존 절차 문구도 `삭제 예정` 토큰에 걸려 `FAIL unsourced_claims=1` 로 오탐됨 (SC-02 의 enumerated 3개 대상 밖의 케이스라 조건 판정에는 영향 없음)
    **잔여 미탐 발견**: "종료 예정"(지원/서비스 접두 없는 단독형), "종료됩니다" 단독형은 여전히 미탐 (`PASS unsourced_claims=0`) — 이번 사이클 범위 밖의 기존 갭
- [x] SC-03: `run-evals.sh` exit 0, 12/12 PASS (기존 9 + 신규 3) — PASS
  - 근거: `bash howto-kit/evals/run-evals.sh` 직접 실행 → `EVALS total=12 pass=12 fail=0` `EVALS_PASS` exit=0 (L3)
- [x] SC-04: `check-docs-a11y.js` exit 0 — PASS
  - 근거: 직접 실행 → `OK deprecation-policy.html ... contrastFail=0` `1/1 PASS` exit=0. 음성 대조: `--text3` 를 `#7A6F64` 로 낮춘 사본 실행 → `FAIL ... contrastFail=2` 확인, 원본 복구 후 `git diff --exit-code` clean (L3, 실행+음성대조)

### Error (4/4)
- [x] ER-01: 3단계 개별 1차 출처 + 조회일 — PASS
  - 근거: `docs/howto/deprecation-policy.md` §1 표 3행 각각 출처 열 비어있지 않음(Amazon SP-API/AWS/Amazon SP-API), `2026-09-10` 7회 등장 (L3)
- [x] ER-02: 약속 vs 관행 구분 서술 — PASS
  - 근거: `at least 12 months`(약관상 약속) / `typically 12 months`(관행 서술) 각각 등장 + 성격 라벨 명시 (L3)
- [x] ER-03: Apple 확인 실패 리터럴 + 시도 URL — PASS
  - 근거: `provenance-notes.md` §8 표에 "Apple"과 리터럴 "확인 실패" 같은 행, 시도 URL 5개 코드블록 (L3)
- [x] ER-04: G4 false negative 실측 문서화 — PASS
  - 근거: `deprecation-policy.md` §4 에 `unsourced_claims=0`(수정 전, "놓친다") / `unsourced_claims=1`(수정 후, "잡는다") 병기. **직접 재현**: HOWTO_DEP 에서 `삭제 예정` 토큰 제거 후 동일 픽스처 실행 → `G4_DEPRECATION PASS unsourced_claims=0` 확인, 원상복구 후 `git diff --exit-code` clean (L3, 재현 완료)

### Architecture (6/6)
- [x] AR-01: `docs/howto/deprecation-policy.md` 존재 — PASS (`test -f` 확인, L1+내용 실사용 확인 L3)
- [x] AR-02: design-brief §11-4 부분해소 + 정본 포인터 — PASS
  - 근거: `grep -c 'deprecation-policy.md'` = 1, §11 4번 항목이 취소선 + "2026-09-10 부분 해소" + 정본/미확인 원장 포인터 명시 (L3)
- [x] AR-03: HTML 미러 + index.html 이중 등록(동일 id) — PASS
  - 근거: 파일 존재, `grep -c "howto-deprecation-policy" docs/index.html` = 2 (573행 `pages` 배열 `file:` 항목, 678행 `getIcon` 매핑) (L3)
- [x] AR-04: accent/text3/localStorage 키 5개 리터럴 — PASS
  - 근거: `--accent:#F59E0B`(1) `--accent:#B45309`(1) `--text3:#948779`(1) `--text3:#656C7A`(1) `dk-theme`(2) 전부 개별 grep 확인 (L3, 5개 전수 확인 — enumerated 준수)
- [x] AR-05: 400줄 이상 + 외부 리소스 0건 — PASS
  - 근거: `wc -l` = 457 (>=400), 외부 로드 패턴 매치 0건 (L3)
- [x] AR-06: diff-scope 정확 일치 — PASS
  - 근거: `git diff --name-only origin/main...HEAD -- docs howto-kit .harness ':(exclude)...'` 결과와 `git diff --name-only origin/main...HEAD` 전체 결과가 `diff` 명령으로 완전 일치 확인 (12개 파일, 차이 0) (L3)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS (`python3 scripts/validate-plugin.py --check=code-fence` → V6 code-fence 0 bare, exit 0)
- [x] AP-04: frontmatter name 누락 금지 — PASS (`python3 scripts/validate-plugin.py` 전체 14 plugins OK, exit 0)

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트 private화 없음 — PASS (신규 산출물은 독립 문서 페이지·픽스처 데이터이며 은닉된 재사용 컴포넌트 없음)
- [x] RE-02: 기존 토큰 블록/테마 토글 재사용 — PASS
  - 근거: `docs/howto-kit/branch-catalog.html` 과 신규 `deprecation-policy.html` 의 CSS 토큰 블록·`dk-theme` localStorage 테마 토글 구조가 동일 패턴으로 재사용됨 확인 (L3, diff 대조)

### Diagnostics (2/2 PASS + 2 N/A)
- [x] DG-01: `bash -n release.sh`, `sh -n howto-gate.sh` 워닝 0 — PASS (둘 다 exit=0)
- [ ] DG-02: N/A — project.yaml `commands.lint: null` + MCP 부재 확인, 계약 justification 정확 (contract-justified N/A, FAIL 아님)
- [x] DG-03: `release.sh` 콘솔 에러 0 — PASS (usage 메시지만 출력, error/exception/traceback/fatal 패턴 0건)
- [ ] DG-04: N/A — `runtime_inspection.mcp_server: null` 확인, SC-02/SC-04 가 런타임 검증 대체 수행 확인 (contract-justified N/A, FAIL 아님)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 25/25 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (자동 REJECT/BLOCKED 트리거 없음)

## Discrimination
- 적용 대상 없음 (규칙 12의 9개 카테고리 — 동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고충돌 — 중 해당 조건 없음)

## User-Reported Failures
- 없음 (사용자 실패 보고 없음)

## Evidence Validity
- 검사 대상 증거: 25건 (조건별 1개 이상)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: SC-02/SC-04/ER-04 의 명령 및 음성 대조를 전부 zsh 환경(사용자 기본 셸)에서 직접 실행. bash 전용 문법(글로빙 등) 없음을 확인. 8건 인용은 실제 curl 로 라이브 페이지 재조회하여 대조 (bash 환경, WebFetch 도구 부재로 curl 대체 — 결과 아래 인용 대조 참조)
- 무효 0건은 미검증 카운터에 영향 없음

## 인용 8건 직접 재조회 대조 (parent 요청 4번 항목)
전부 curl 로 라이브 페이지를 재조회하여 원문과 대조했다 (WebFetch 도구가 이 세션에 없어 curl 대체, 결과는 동등):

| # | 출처 | 인용 문구 | 재조회 결과 |
| --- | --- | --- | --- |
| 1 | Amazon SP-API deprecations | "no longer in active development as of the deprecation date" | 원문 그대로 확인 |
| 2 | Amazon SP-API deprecations | "calls to the resources fail as of the removal date" | 원문 그대로 확인 |
| 3 | AWS sunset_services | "sunset time line (typically 12 months)... AWS will end operations" | 원문 그대로 확인 |
| 4 | Google Cloud service-usage/deprecations | "the service is scheduled for shutdown" | 원문 확인. **단, `raw=miss decoded=HIT` 주장은 재현 안 됨** — curl 직접 재조회 시 raw HTML 에 해당 문장이 개행만 포함하고 HTML 엔티티 없이 그대로 검색됨(1회 매치). 이는 계약의 "리서치 소스" 섹션(non-parsed 서술) 서술이라 조건 판정에 영향 없으나, Codex 가 사용한 fetch 경로와 curl 결과가 다를 수 있음을 참고 기록 |
| 5 | Google Cloud products (en) | "Deprecated features are scheduled to be shut down and removed" | 원문 그대로 확인 |
| 6 | Google Cloud terms | "Google will notify Customer at least 12 months before... unless Google replaces such discontinued Service..." | 원문 그대로 확인. **예외 단서("unless...replaces") 실재 확인** — §2 논거의 근거가 유효함 |
| 7 | Google Cloud products?hl=ko | "지원 중단된 기능은 서비스 종료 및 삭제가 예정된 기능입니다" | 원문 그대로 확인. **한국어 매핑(deprecated=지원 중단됨, removed 연관=삭제) 근거로 유효** |
| 8 | Naver 단축URL 공지 | "단축 URL 기능의 지원이 2024년 11월 28일(목)부로 종료됩니다" | 원문 그대로 확인 (meta description) |

부가 확인: Google Cloud 한국어 deprecations lifecycle 페이지(`?hl=ko`)는 "삭제" 대신 "종료될 예정입니다"를 쓰며 "삭제" 단어가 아예 등장하지 않음(count=0) — 그러나 계약이 인용한 출처는 `products?hl=ko` (별개 페이지)이고 거기서는 "삭제가 예정된 기능"으로 명확히 등장하므로 인용 자체는 정확함. Apple 개별 공지(`developer.apple.com/support/deprecated-sirikit-intent-domains`) 실재 확인.

## Summary
- Total: 25/25 conditions passed (DG-02/DG-04는 project.yaml 근거의 정당한 N/A)
- Verdict: **APPROVE**

### 중대 발견 — 조건 판정에는 미반영이지만 최우선 후속조치 권고
게이트 안전성 적대적 탐색(parent 요청 2번)에서 SC-02가 요구하는 3개 enumerated 픽스처 밖의 **실사용 가능성이 높은 오탐 케이스**를 발견했다:

```
$ . howto-kit/scripts/howto-gate.sh
$ howto_gate <"30일 지난 데이터를 삭제 예정입니다" 포함 픽스처>
G4_DEPRECATION FAIL unsourced_claims=1   ← 오탐. 이건 deprecation 주장이 아니라 정상 데이터 보존정책 문구다
```

`삭제 예정` 토큰은 계정 삭제(단문 동사구) 오탐은 막았지만, "N일 후 자동 삭제 예정입니다" 류의 **흔한 데이터 보존/파기 안내 문구**는 여전히 오탐한다. 이 패턴은 로그 정리, 휴지통, 계정 비활성 정책 등에서 실제로 매우 흔하다. SC-02의 (c) 픽스처("계정을 삭제한다")는 이 패턴 계열을 대표하지 못한다.

또한 "종료 예정"(지원/서비스 접두어 없는 단독형) 은 여전히 미탐이다 — 이번 사이클 범위 밖(기존 갭)이라 회귀는 아니지만, 다음 사이클 후보로 남긴다.

## Improvement Suggestions
- [SC-02] 측정-방식-불일치 — "정상 절차가 안 깨진다"는 목표를 계정삭제 단일 픽스처로만 대표시켰다. "N 일 후 자동 삭제 예정입니다" 류 데이터 보존정책 문구를 오탐 방지 픽스처로 추가하고, 토큰을 `삭제 예정`(스텝 요약 맥락 한정) 대신 더 좁은 결합 조건(예: 주어가 기능/서비스/API 인 경우만)으로 재설계할 것을 권고한다.
- [SK-01] 범위-미명시 — "종료 예정"(단독형), "종료됩니다"(단독형) 미탐은 이번 사이클 범위 밖이나, 다음 `/howto-research` deprecation-policy 후속 사이클의 GAP 분석에 명시적으로 등록할 것을 권고한다.
