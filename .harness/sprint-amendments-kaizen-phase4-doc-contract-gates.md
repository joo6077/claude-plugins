# Sprint Amendments — kaizen-phase4-doc-contract-gates

계약 본문(`.harness/sprint-contract-kaizen-phase4-doc-contract-gates.md`)은 **무수정**이다.
`conditions_digest: sha256:cd66d3b1ff6b051e` 봉인이 그대로 유효하며, 아래 항목은 전부
"이 조건을 이렇게 읽어라" 를 덧붙인 것이지 조건 문구를 바꾼 것이 아니다.

포맷은 `harness/references/contract-schema.md` §Amendment 사이드카 (v5.3 · direction × consent
2 축) 를 따른다.

## AM-01 — relaxing · unanchored

- **대상 조건**: SC-04
- **원 조건 측정문**: `python3 scripts/validate-post-kaizen.py --since b161d80` 출력에
  `doc-contracts` 행이 있고 **FAIL 0 · 종료 코드 0**
- **문제 (실행으로 확인)**: 이 게이트는 카이젠 **종료 단계** 산출물까지 함께 검사한다.
  실행 결과 5 행이 FAIL 이고 exit 1 이다 —
  `changelog-entry` (`docs/kaizen/changelog.md`) · `research-log` (`docs/kaizen/research-log.md`) ·
  `cleanup-log` · `failure-count` · `evals-audit`.
  이들은 오케스트레이터 Step F1~F4 가 사이클 끝에 생산하는 것이고, 앞의 둘은 **Phase 4 scope
  밖 경로**다. 따라서 원 측정문은 **이 스프린트 안에서 원리적으로 만족 불가능**했다.
  Phase 3 §폐기·재작성이 다룬 자기모순의 네 번째 변종이다.
- **제안 해석**: `doc-contracts` 행이 **존재하고 그 상태가 PASS** 이며, 종료 코드가 인프라
  오류(2)가 아닐 것. 게이트 **전체** green 은 Final 단계 계약의 조건이지 Phase 계약의 조건이 아니다.
- **direction 계산**: PASS 집합이 **늘어난다** (전체 15 행 green 요구 → 1 행 PASS 요구).
  자기신고가 아니라 포함관계로 계산한 값이다 → `relaxing`.
- **consent**: `unanchored`. 사용자 승인·prompt 로그 앵커가 없다. 지어내지 않는다.
- **효력**: `relaxing · unanchored` 는 **PASS 근거로 쓸 수 없다.**
  따라서 자기 검증에서 SC-04 는 **미충족**으로 보고한다. 관측된 사실만 남긴다 —
  `doc-contracts` 행 존재 ✓ · 상태 PASS ✓ · 전체 FAIL 5 · exit 1.
  판정은 QA/사용자에게 넘긴다.
- **재발 방지**: 이 결함의 조문 개정안을
  `.harness/.meta/phase4-handoff-to-contract.md` §F4 (`측정-소유권-초과` preflight 태그)에
  남겼다. Phase 2 소관이라 Phase 4 가 직접 고치지 않는다.

## AM-02 — 음성 대조 관측 정정 (조건 변경 아님)

- **대상 조건**: ER-04
- **원 조건의 음성 대조 문구**: "`git_diff_names()` 를 실패 시 `[]` 반환으로 되돌리면 같은
  입력이 **exit 0** 으로 통과해야 한다"
- **실제 관측**: mutant(구 동작)의 종료 코드는 **1** 이었다. exit 0 이 아닌 이유는 AM-01 과
  같다 — 사이클 종료 산출물 5 행이 무관하게 FAIL 이기 때문이며, 인프라 오류 은폐와는 별개다.
- **결합은 그대로 증명됐다** (행 단위 대조):

  | 검사 | mutant (구 동작) | 현 동작 |
  | ------ | ------ | ------ |
  | `plugin-json-bumps` | SKIP "no plugin.json in diff" | ERROR "git diff 실패 (rc=128)" |
  | `marketplace-sync` | SKIP "no plugin bumps this cycle" | ERROR "git diff 실패 (rc=128)" |
  | `docs-site-regen` | SKIP "no harness source changes" | ERROR "git diff 실패 (rc=128)" |
  | `scope-isolation` | SKIP "git log failed" | ERROR "git log 실패 (rc=128)" |
  | 합계 | 0 ERROR · exit 1 | 4 ERROR · **exit 2** |

- **direction**: 없음. 조건의 PASS 집합을 건드리지 않는다 — 음성 대조 문구가 가정한
  "green 베이스라인" 이 사이클 중간에는 성립하지 않는다는 **관측 기록**이다.
  판정 기준은 원문 그대로 "인프라 오류를 위반 0 건으로 둔갑시키지 않는다" 이며, 위 표가 그 증거다.
- **consent**: `unanchored`.
