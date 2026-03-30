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
