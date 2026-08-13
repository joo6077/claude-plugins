# 게이트 exit code taxonomy

> 이 파일이 **SSOT** 다. 게이트 스크립트(eval 테스트 · post-kaizen 검증 · docs-contract 검증)는
> 여기 정의된 4 값만 쓰고, 값의 의미를 자기 파일에서 다시 정의하지 않는다. 인용만 한다.
>
> 신설: 2026-08-13 (Phase 4 kaizen)

## 왜 필요한가 — 실측

`harness/evals/kaizen/feedback-system/aggregation-test.sh` 는 `yq` 가 없으면 검증을 건너뛴 뒤
마지막에 `=== ALL TESTS PASSED ===` 를 출력하고 exit 0 했다. 이 머신에는 `yq` 가 설치돼 있지
않으므로 (`command -v yq` → exit 1) **이 게이트는 아무것도 검증하지 않으면서 통과를 보고하고
있었다.** 도구 부재가 "위반 0 건" 으로 집계되는 순간 게이트는 없는 것보다 나쁘다 — 통과 기록이
남기 때문이다.

`scripts/validate-post-kaizen.py` 도 같은 형태였다. `git_diff_names()` 가 git 실패 시 빈 목록을
돌려주어 diff 기반 검사 전부가 "변경 없음 → 위반 없음" 으로 통과했고, `check_scope_isolation` 은
`git log` 실패를 `SKIP` 으로 처리했는데 `SKIP` 은 종료 코드에 영향을 주지 않았다.

## 4 값

| code | 이름 | 의미 | 예 |
| ------ | ------ | ------ | ------ |
| `0` | `pass` | 검사를 **실제로 수행**했고 위반이 없다 | 3 건 fixture 를 파싱해 전부 기대값과 일치 |
| `1` | `policy_violation` | 검사를 수행했고 **위반을 찾았다** | 선언된 옵션 집합과 argparse 실체가 다르다 |
| `2` | `usage_or_infra_error` | 검사를 **수행하지 못했다** — 도구 부재 · 파싱 실패 · 권한 거부 · 잘못된 인자 | `yq` 와 `python3` 둘 다 없음 · `git log` 실패 · 마커 개수 이상 |
| `3` | `no_data_not_run` | 검사 대상이 **하나도 없었다** (정상적으로 해당 없음과 구분해야 할 때만 쓴다) | 레포에 `docs-contract` 블록이 0 개 |

## 규칙

- **`tool_missing` · `parse_failed` · `permission_denied` 는 위반 0 건이 아니다.** `2` 로 낸다.
  `command -v tool || { echo WARN; exit 0; }` 형태는 게이트에서 금지다.
- **`2>/dev/null` 은 금지 기본값이다.** 필요하면 `stderr 를 변수에 캡처 → assert 또는 로그` 형태만
  쓴다. 특히 네거티브 테스트는 stderr 를 버리지 말고 "실패해야 하며 **이 에러 메시지**가 있어야
  한다" 를 검증한다.
- **정책 위반과 인프라 오류가 동시에 나면 `2` 가 우선한다.** 실행이 불완전한 run 의 결과 집합을
  완전한 분석 결과로 보고해서는 안 되기 때문이다 (SARIF 가 `executionSuccessful` 을 results 와
  별도로 두는 것과 같은 이유). 두 카운트는 요약 줄에 **모두** 출력한다 — 종료 코드가 하나라고
  해서 다른 하나를 감추지 않는다.
- **`--help` 는 side-effect free 여야 한다.** 인자 처리를 최상단에 두고, `mktemp` · `cd` ·
  외부 파일 읽기 · 쓰기 가능한 TMP 의존은 help 출력 **뒤로** 내린다. help 가 실행 환경에 따라
  실패하면 그 스크립트는 docs-as-code 검증 대상이 될 수 없다.
- **아직 도래하지 않은 단계의 산출물은 위반이 아니다 — 그렇다고 조용히 넘기지도 마라.**
  사이클 종료 단계가 생산하는 산출물을 진행 중에 검사해 `1` 로 내면 게이트가 거짓 위반을
  쌓고, 그 게이트는 아무도 안 본다. 실측 2026-07-27: `validate-post-kaizen.py` 가 "오늘 날짜
  엔트리" 를 오라클로 써서 자정을 넘긴 사이클의 changelog · research-log · cleanup-log ·
  failure-count 4 건을 false negative FAIL 로 냈다 (엔트리는 전부 07-27 자로 실재했다 —
  `.harness/.meta/orchestrator-audit-log.md` §2026-07-27 사이클 meta-issue 1). 규칙 3 개다.
  1. 단계 도래 여부는 **기계 판독 가능한 상태 파일**로 판정한다 (사람의 선언·주석·커밋 메시지
     금지). 카이젠은 `.harness/.meta/kaizen-state.yaml` 의 `status` 다.
  2. 도래 전이면 **사유를 붙여** 건너뛰고, 유예 건수를 요약에 별도로 센다. 유예가 있는 run 은
     완결 판정이 아니라는 사실을 stderr 로 함께 알린다. 도래 후에는 예외 없이 강제한다 —
     유예는 상태가 바뀌는 순간 **자동으로 닫혀야** 하고, 사람이 다시 켤 필요가 없어야 한다.
  3. **판정 자체가 불가능하면**(상태 파일 부재 · 파싱 실패 · 미지의 status) 건너뛰지 말고
     `2` 다. "모르니까 통과" 는 도구 부재를 통과로 집계하던 것과 같은 실패 모드다.
  날짜 오라클은 "오늘" 이 아니라 **사이클 날짜**를 쓴다. 반대로 "이번 달 아무 파일" 같은 느슨한
  매칭도 금지다 — 8/31 사이클이 8/1 산출물로 green 이 된다 (실제로 그랬다).
- **`set -euo pipefail` 만으로 "fail loud" 가 됐다고 보지 마라.** `set -e` 는 조건문 · 파이프 ·
  command substitution 안에서 무력화된다. 실패를 반드시 잡아야 하는 지점은 명시적으로 검사한다.

## 소비처

| 파일 | 쓰는 값 |
| ------ | ------ |
| `harness/evals/kaizen/feedback-system/aggregation-test.sh` | 0 · 1 · 2 |
| `harness/evals/kaizen/feedback-system/save-test.sh` | 0 · 1 · 2 |
| `scripts/validate-post-kaizen.py` | 0 · 1 · 2 |
| `scripts/validate-doc-contracts.py` | 0 · 1 · 2 · 3 |
