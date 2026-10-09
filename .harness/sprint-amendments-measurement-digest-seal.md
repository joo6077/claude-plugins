# measurement-digest-seal 개정

계약 `sprint-contract-measurement-digest-seal.md` (봉인 `sha256:bcea1a2c7f50997a` · 측정 봉인 `sha256:423bec66e0f41168`, 봉인 커밋 e754311)
의 조건 줄과 측정 줄은 고치지 않았다. 바뀐 것은 여기에만 적는다.

## A-01 — 평가자 1-e-3 의 재봉인 검출이 `measurement_digest` 교체도 잡는다

**무엇이 달라졌나**: 조건 AR-02 에 요구를 하나 더한다 — `harness/agents/qa-evaluator.md` 1-e-3 의 bash 코드 블록을 원문 그대로,
봉인 커밋 뒤 측정 줄을 고치고 `measurement_digest` 를 다시 계산해 넣은 계약에 돌리면 재봉인 줄
(`-measurement_digest:` · `+measurement_digest:`)이 재봉인 검출 출력에 나온다. 결과표의 재봉인 행이 두 필드를 함께 다룬다.
측정: `bash $M/reseal_probe.sh harness/agents/qa-evaluator.md`. 음성 대조: 기준 판(1922551) 평가자로 돌리면 재봉인 검출 줄이 0 이고
바뀐 줄은 산문 차이 목록에만 나온다 — 2026-09-26 실측.

**왜** — Iteration 1 APPROVE 뒤 부모 교차 진단이 찾았다. 1-e-3 는 조용한 재봉인을 `^[+-]conditions_digest:` 로만 찾는다. 측정 줄을 고친 뒤
새 지문을 계산해 넣으면 `verify_seal` · `verify_measurement` 가 둘 다 OK 이고, 1-e-3 도 그 변경을 "산문 차이 — 경고" 로만 본다.
이번 스프린트가 막으려던 변경이 경고 한 줄로 빠져나간다.

**amend_direction**: `narrowing` — 통과하려면 만족해야 할 것이 하나 늘고 줄어든 것은 없다 (허용 파일 6 경로는 그대로, AR-05 불변).

**consent**: `unanchored` — 부모 판단. 좁힘이라 PASS 근거로 쓸 수 있다.
