# Evaluator-Kaizen Expected Improvements

## fixture: l3-miss

l3_unreached가 반복될 때 기대하는 개선:

- [ ] qa-evaluator.md에 L3 도달 강제 규칙이 강화되어야 한다
- [ ] qa-evaluation-guide.md에 L3 미도달 시 FAIL 처리 명시가 추가되어야 한다

## fixture: false-approve

bias_detected + evidence_missing가 반복될 때 기대하는 개선:

- [ ] qa-evaluator.md Red Flags에 "증거 없는 PASS" 감지 규칙이 추가되어야 한다
- [ ] qa-evaluation-guide.md에 증거 체크리스트가 구체화되어야 한다

## fixture: reject-loop

contract_misinterpret가 반복될 때 기대하는 개선:

- [ ] qa-evaluator.md에 리터럴/의미 해석 균형 기준이 추가되어야 한다
- [ ] Gotchas에 "동의어 FAIL 판정 시 의미 동일성 한 번 더 확인" 추가되어야 한다

## fixture: vacuous-zero

APPROVE 뒤에 교차 진단(또는 사용자)이 "0 건을 근거로 한 PASS 가 공허했다" 를 지적하고, 평가자는 도구가 없어 교차 진단을 못 했다고 적는 패턴이 반복될 때 기대하는 개선:

- [ ] qa-evaluator.md 규칙 10 에 0 이 기대값인 측정의 양성 대조 절차(명령 성공 · 대상 수 · 알려진 나쁜 예)가 추가되어야 한다
- [ ] qa-evaluator.md 의 `tools` 에 7단계 교차 진단용 `Agent(general-purpose)` 가 있어야 하고, 7단계를 못 하면 `cross_diagnosis_by: none` 으로 적게 해야 한다
  - 2026-09-22 대체됨 — 평가자가 직접 띄우는 설계를 폐기했다. 도구를 쥐어줘도 띄우지 않고 띄웠다고 적는 일이 두 번 연속 관측되어, 교차 진단 주체를 부모로 옮기고 평가자는 `pending-parent` 로 저장한다. 이 항목을 "아직 못 한 개선" 으로 읽지 마라. `assertions.json` 의 이 fixture 둘째 패턴도 2026-09-24 에 `Agent\(general-purpose\)` 에서 `cross_diagnosis_by: pending-parent` 로 바꿨다 — 옛 패턴은 2026-09-22 부터 0 건이었다

## fixture: silent-check

APPROVE 뒤에 교차 검토가 「새 검사가 조용히 실패한다」(첫 칸만 읽기 · 표에만 올린 시험 · 한 칸 못 읽으면 전체 꺼짐)를 잡는 패턴이 반복될 때 기대하는 개선:

- [ ] qa-evaluator.md 규칙 10 에 산출물이 검사일 때 평가자가 임시 사본으로 돌리는 다섯 가지가 있어야 한다
- [ ] 리포트 형식에 `Check Artifacts` 블록이 있어 항목마다 사본 · 명령 · 종료 코드 · 읽은 대상 수를 남겨야 한다
- [ ] qa-evaluation-guide.md 에 `### 산출물이 검사일 때` 절이 있어야 한다
