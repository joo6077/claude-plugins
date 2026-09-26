---
slug: after-0926-contract-schema
created: "2026-09-26 20:16"
---

## AM-01 — relaxing (동의 대기)

- 대상 조건: AR-06 (로컬 CI 가 기준과 같은 상태로 끝난다)
- 원 조건: 요약 파일에서 `rc=0` 줄이 **22 줄**, `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐
  (yq 가 있으면 `rc=0` 23 줄). 기준 실측 「B 판에서 22 · SKIP 1」
- 변경: `rc=0` 줄 **25 줄** · SKIP 1 줄 (yq 가 있으면 `rc=0` 26 줄). 측정 명령 · 측정 묶음 `ci-local.sh`
  (sha256 앞 16 자리 `59fe55125c0dbc77`, AR-05 가 잠금) · 나머지 판정은 그대로
- 근거 (실측, 2026-09-26 20:1x):
  - 봉인된 측정 묶음의 `ci-local.sh` 는 단계가 스물여섯이다 — `run` 스물다섯(`kaizen-assertions` ·
    `reviewer-copies` · `api-ui-viewer` 포함)과 yq 분기 하나. 원 조건의 「22 · SKIP 1」 은 이 셋이 없던 옛 판
    스크립트로 잰 값이다 (세션 스크래치 `cs/ci-base.txt` 에 22 단계 요약이 남아 있다)
  - 기준 판 `6378948` 사본(세션 스크래치 `cs/mock`, 분리 체크아웃)에 봉인된 `ci-local.sh` 를 돌리면 `rc=0` 25 · SKIP 1 · 종료 0
  - 구현 판 `5e1a74b`(작업 폴더 W, `HEAD` = 가지 끝, `.harness` 밖 미커밋 0)에서도 `rc=0` 25 · SKIP 1 · 종료 0 —
    기준 판과 같다. 조건 이름 「기준과 같은 상태」 는 성립한다
  - 원 조건은 봉인된 스크립트로는 통과할 수 없다 — 요약 줄이 26 줄이라 「`rc=0` 22 줄 + 그 밖 1 줄」 이 나올 수 없다.
    PASS 집합이 비어 있던 조건이라 무엇으로 고쳐도 PASS 집합이 는다
- direction: `relaxing added=2 removed=2` — `harness/references/contract-schema.md` 의 `amend_direction` (허용 집합 헬퍼)에
  원 허용 요약 모양 둘(`rc0=22 skip=feedback-agg-test` · `rc0=23 agg=rc0`)과 개정 둘(`rc0=25 …` · `rc0=26 …`)을 넣은 출력
- consent: (비어 있음 — 사용자 동의 대기. 위임 2026-09-26T10:09:00.557Z 는 느슨하게 하는 개정의 동의로 쓰지 않는다)
- 앵커: (비어 있음)
