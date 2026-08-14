# Sprint Amendments — kaizen-phase4-doc-contract-gates

계약 본문(`.harness/sprint-contract-kaizen-phase4-doc-contract-gates.md`)은 **무수정**이다.
`conditions_digest: sha256:cd66d3b1ff6b051e` 봉인이 그대로 유효하며, 아래 항목은 전부
"이 조건을 이렇게 읽어라" 를 덧붙인 것이지 조건 문구를 바꾼 것이 아니다.

포맷은 `harness/references/contract-schema.md` §Amendment 사이드카 (v5.3 · direction × consent
2 축) 를 따른다.

**QA iteration 2 요약**: 이전 판의 AM-01 · AM-02 는 **둘 다 철회**했다. QA 가 REJECT 한 blocking
2 건(SC-04 · DG-02)을 조문 재해석이 아니라 **구현 수정**으로 해소했고, 그 결과 두 조건 모두
원 측정문 문자 그대로 충족한다. 지금 이 파일에 살아 있는 amendment 는 AM-03(관측 기록) 하나뿐이며
어떤 조건의 PASS 근거로도 쓰이지 않는다.

## AM-01 — 철회됨 (원 분류: relaxing · unanchored)

- **대상 조건**: SC-04
- **철회 사유**: QA 판정이 옳다. `relaxing · unanchored` 는 PASS 근거가 될 수 없고, 정직한
  자기신고라도 FAIL 은 FAIL 이다. 조문을 좁혀 읽는 대신 **게이트 구현을 고쳤다.**
- **원 amendment 가 주장하던 것**: "게이트 전체 green 은 Phase 계약의 조건이 아니다" 로
  SC-04 를 `doc-contracts` 행 한정으로 읽어달라는 요청. → **폐기.**
- **대신 무엇을 고쳤나** (`scripts/validate-post-kaizen.py`): 다섯 검사
  (`changelog-entry` · `research-log` · `cleanup-log` · `failure-count` · `evals-audit`)의
  **오라클이 틀렸다.** "오늘 날짜 엔트리가 있는가" 로 무조건 검사하던 구판은 양방향으로 다
  틀렸고, 이 결함은 이번 계약과 무관하게 **직전 사이클에 이미 기록된 백로그**다 —
  `.harness/.meta/orchestrator-audit-log.md` §2026-07-27 사이클 meta-issue 1:
  *"`datetime.date.today()` 기준이라 자정을 넘긴 사이클이 자기 게이트에 걸린다 … 4 건이
  false negative FAIL … 수정 방향: 사이클 날짜를 `kaizen-state.yaml` 의 `cycle_id` 에서 유도"*.
  그 기록된 수정 방향을 그대로 구현했다.
  1. **단계 인지** — 다섯은 Phase 구현이 아니라 오케스트레이터 **Step F1~F4** 산출물이다
     (`.claude/skills/kaizen-orchestrator/SKILL.md:32` 이 이 게이트를 "Step F4 … PR 생성 전
     필수 실행" 으로 규정한다). 도래 여부를 `.harness/.meta/kaizen-state.yaml` 의 `status` 로
     판정해 `completed` 전이면 사유를 붙여 유예하고 요약·stderr 에 유예 건수를 드러낸다.
     같은 러너가 이미 `plugin-json-bumps` · `marketplace-sync` · `docs-site-regen` 3 건을
     같은 방식(전제 미성립 → SKIP)으로 다루고 있었다 — 다섯만 일관성 밖에 있었다.
  2. **날짜 오라클** — "오늘" 대신 `cycle_id` 에서 유도한 **사이클 날짜**(+오늘)를 쓴다.
  3. **거짓 통과 제거** — `evals-audit` 의 "이번 달 아무 파일" fallback 을 삭제했다.
     8/31 사이클이 8/1 감사 파일로 green 이 되던 구멍이다.
  4. **판정 불가 = 통과 아님** — 상태 파일 부재 · 파싱 실패 · 미지의 status 는 유예가 아니라
     `ERROR` → exit 2 다 (`harness/evals/gate-exit-codes.md` §규칙에 규약으로 추가).
- **약화가 아님 (실행 증거)**:

  | 뮤테이션 | 입력 | 결과 |
  | ------ | ------ | ------ |
  | M1 정상 사용 시점 재현 | `status: completed` · 산출물 없음 | 다섯 전부 **FAIL** · exit 1 — 구판과 동일 강제 |
  | M2 미지의 status | `status: bogus` | 5 **ERROR** · exit 2 (유예 아님) |
  | M3 상태 파일 부재 | 파일 이동 | 5 **ERROR** · exit 2 |
  | M4 기록된 false negative 재현 | `cycle_id: kaizen-2026-07-27` · `completed` · 오늘 08-13 | 다섯 전부 **PASS** (엔트리 실재) |
  | M4b 구판 오라클 뮤턴트 | 같은 입력 | 5 **FAIL** — 구 결함 재현 |
  | M5 거짓 통과 구멍 | `cycle_id: kaizen-2026-07-01` · 실제 파일은 07-27 자 | 신판 **FAIL** / 구판 fallback 뮤턴트 **PASS** — 신판이 더 엄격 |
  | M6 음성 대조 | 유예 가드 제거 | 5 **FAIL** 복귀 — 유예는 오직 `status` 가 만든다 |

  유예는 `finalize-phase.sh` 가 마지막 Phase pass 에서 `status: completed` 를 쓰는 순간
  **자동으로 닫힌다.** 사람이 다시 켜야 하는 스위치가 아니다.
- **원 측정문 충족 (문자 그대로)**: `python3 scripts/validate-post-kaizen.py --since b161d80`
  → `[ PASS ] ✓ doc-contracts: … violation 0` 행 존재 · `7 PASS / 0 FAIL / 0 ERROR / 8 SKIP` ·
  **exit 0**.
- **핸드오프는 유지한다**: `.harness/.meta/phase4-handoff-to-contract.md` §F4
  (`측정-소유권-초과` preflight 태그)는 그대로 둔다. 이번엔 게이트를 고쳐 해소했지만,
  "게이트 전체 exit code 를 조건 오라클로 삼는 조문" 자체가 취약하다는 지적은 여전히 유효하고
  Phase 2 소관이다.

## AM-02 — 철회됨 (원 분류: 관측 기록 · direction 없음)

- **대상 조건**: ER-04
- **원 관측**: 음성 대조 뮤턴트의 종료 코드가 계약 문구("exit 0 으로 통과해야 한다")와 달리
  **1** 이었다 — 사이클 종료 산출물 5 행이 무관하게 FAIL 이었기 때문.
- **철회 사유**: AM-01 의 구현 수정으로 그 5 행이 사라졌고, **계약 문구가 문자 그대로 참이 됐다.**
  재실행 (`git_diff_names()` → 실패 시 `[]`, `check_scope_isolation` → git 실패 시 SKIP 로
  되돌린 뮤턴트 · `--since deadbeef99`):
  `6 PASS / 0 FAIL / 0 ERROR / 9 SKIP` · **exit 0**.
  현 구현은 같은 입력에서 `4 ERROR` · **exit 2**. 관측 정정이 더 이상 필요 없다.

## AM-03 — 관측 기록 (direction 없음 · PASS 근거로 쓰지 않음)

- **대상 조건**: DG-02
- **관측**: 조건은 "**변경된** `.sh` 전부" 를 요구하고, 변경된 3 개
  (`aggregation-test.sh` · `save-test.sh` · `finalize-phase.sh`)는 `bash -n` 0 · `shellcheck -o all`
  0 건으로 충족했다. 다만 레포 전체로 보면 `shellcheck -o all` 부채가 **범위 밖 `.sh` 약 30 개**에
  남아 있다 (최다: `reflect-kit/hooks/log-reflection.sh` 152 · `harness/scripts/save-feedback.sh` 142 ·
  `scripts/release.sh` 88). 대부분 SC2250 같은 style 계열이다.
- **왜 이번에 안 고치나**: AR-01 이 구현 변경 경로를 11 개로 못 박는다. 범위 밖 파일을 손대면
  AR-01 이 깨진다. 조건 간 충돌을 만들지 않는 것이 우선이다.
- **후속**: 레포에 셸 린트 게이트가 **없다**(`.github/workflows/ci.yml` 에 shellcheck 없음).
  전수 정리 + CI 게이트 도입은 다음 사이클 백로그다. 이 항목은 어떤 조건의 PASS 근거도 아니다.
- **direction**: 없음 — 조건의 PASS 집합을 건드리지 않는다.
- **consent**: `unanchored`.
