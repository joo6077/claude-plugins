# Contract-Kaizen Expected Improvements

## fixture: ambiguous-conditions

ambiguous_conditions가 반복될 때 기대하는 개선:

- [ ] sprint-contract SKILL.md Gotchas에 모호 조건 감지 규칙이 추가되어야 한다
- [ ] contract-design-guide.md에 모호 표현 목록(적절히, 충분히, 잘)이 명시되어야 한다

## fixture: category-bias

category_coverage_gap가 반복될 때 기대하는 개선:

- [ ] sprint-contract Process에 카테고리 균형 검증 단계가 추가되어야 한다
- [ ] contract-design-guide.md에 GQM 기반 카테고리 도출 절차가 구체화되어야 한다

## fixture: low-coverage

complexity_underestimate가 반복될 때 기대하는 개선:

- [ ] sprint-contract Gotchas에 복잡도 판단 기준 강화가 추가되어야 한다
- [ ] 최소 조건 수 하한선이 복잡도별로 명시되어야 한다

## fixture: vacuous-boilerplate

레포 밖·스택 불일치 대상 계약에서 자동 포함 항목과 금지 패턴 최소 개수 규칙이 "아무것도 재지 않는 조건" 을 만들어
교차 진단이 반복 지적할 때 기대하는 개선:

- [ ] sprint-contract SKILL.md Step 3 에 "적용될 패턴이 없으면 `AP-00: N/A (사유)`" 경로가 있어야 한다
- [ ] sprint-contract SKILL.md Step 4 에 "이번 변경과 무관한 자동 항목은 `N/A (사유)`" 경로가 있어야 한다
- [ ] 0 이 기대값인 조건에 `양성 대조:` 절을 요구하는 패턴이 조건 패턴 표에 있어야 한다
