## EVAL DEFINITION: qa-accuracy

QA Evaluator의 APPROVE/REJECT 판정이 정확한지 검증한다.
False positive(잘못된 APPROVE)와 false negative(잘못된 REJECT)를 측정한다.

### Test Fixtures

테스트용 Sprint Contract + 코드 조합을 준비한다.

#### Fixture A: 완벽한 구현 (Expected: APPROVE)

Sprint Contract:
```
- [ ] UI-01: 설정 페이지에 테마 선택 행이 표시된다
- [ ] LG-01: 테마 변경 시 Provider 상태가 업데이트된다
- [ ] AR-01: 설정 페이지는 shared/settings/presentation/에 위치한다
```

코드: 모든 조건을 충족하는 정상 구현

#### Fixture B: 1개 FAIL (Expected: REJECT)

Sprint Contract: Fixture A와 동일
코드: UI-01은 PASS하지만 LG-01이 미구현 (Provider 없음)

#### Fixture C: Anti-pattern 위반 (Expected: REJECT)

Sprint Contract: Fixture A + AP-01(StatefulWidget 금지)
코드: 기능은 완벽하지만 StatefulWidget 사용

#### Fixture D: 관대함 함정 (Expected: REJECT)

Sprint Contract:
```
- [ ] UI-01: 스낵바가 표시된다
```
코드: Toast로 구현 (기능적으로 동일하지만 계약과 다름)

#### Fixture E: 주석 함정 (Expected: REJECT)

Sprint Contract:
```
- [ ] ER-01: 에러 시 사용자에게 표시된다
```
코드: `// 에러 처리 완료` 주석만 있고 실제 errorProvider 호출 없음

### Capability Evals

#### QAA-CAP-01: True Positive (정확한 APPROVE)
- Task: Fixture A를 QA Evaluator에게 평가시킴
- Success Criteria:
  - [ ] APPROVE 판정
  - [ ] 모든 조건 PASS + 근거(파일:라인) 제시

#### QAA-CAP-02: True Negative (정확한 REJECT)
- Task: Fixture B를 QA Evaluator에게 평가시킴
- Success Criteria:
  - [ ] REJECT 판정
  - [ ] LG-01이 FAIL + "Provider 없음" 근거 제시
  - [ ] UI-01, AR-01은 PASS 유지 (과잉 FAIL 아님)

#### QAA-CAP-03: Anti-pattern REJECT
- Task: Fixture C를 QA Evaluator에게 평가시킴
- Success Criteria:
  - [ ] REJECT 판정
  - [ ] AP-01 FAIL + StatefulWidget 발견 근거
  - [ ] 기능 조건(UI/LG/AR)은 PASS (Anti-pattern만 FAIL)

#### QAA-CAP-04: 관대함 방지 (Literal 해석)
- Task: Fixture D를 QA Evaluator에게 평가시킴
- Success Criteria:
  - [ ] REJECT 판정
  - [ ] UI-01 FAIL + "스낵바 ≠ Toast" 근거
  - [ ] 계약 수정 권장 ("스낵바 → Toast로 변경 권장")

#### QAA-CAP-05: 주석 편향 방지
- Task: Fixture E를 QA Evaluator에게 평가시킴
- Success Criteria:
  - [ ] REJECT 판정
  - [ ] ER-01 FAIL + "주석만 있고 실제 구현 없음" 근거
  - [ ] "에러 처리 완료" 주석을 증거로 인용하지 않음

### Scoring

```
Accuracy = (True Positive + True Negative) / Total
False Positive Rate = 잘못된 APPROVE / (잘못된 APPROVE + 정확한 REJECT)
False Negative Rate = 잘못된 REJECT / (잘못된 REJECT + 정확한 APPROVE)
```

목표:
- Accuracy > 95%
- False Positive Rate < 5% (잘못된 APPROVE가 가장 위험)
- False Negative Rate < 10% (과잉 REJECT는 수정 비용만 증가)

### Test Method

서브에이전트로 QA Evaluator를 spawn하여:
1. 미리 준비된 `.harness/sprint-contract.md`를 읽게 하고
2. 미리 준비된 코드 파일을 검증하게 하고
3. 판정 결과(APPROVE/REJECT)와 조건별 PASS/FAIL을 Expected와 비교

**테스트 실행 순서:**
```
1. Fixture는 harness/evals/test-fixtures/ 에 준비됨
   - fixture-a/ ~ fixture-e/ (contract.md + code/)
2. 각 Fixture별로:
   a. sprint-contract.md를 Fixture의 contract.md로 교체
   b. QA Evaluator 서브에이전트 spawn (code/ 디렉토리를 검증 대상으로 지정)
   c. 판정 결과 수집
   d. Expected와 비교
3. 점수 산출
```

### Regression — 캘리브레이션 드리프트

QA Evaluator가 시간이 지나면서 관대해지거나 엄격해지는지 주기적으로 확인:

- 같은 Fixture로 월 1회 재테스트
- 판정이 달라지면 프롬프트/config 드리프트 의심
- Accuracy가 95% 아래로 떨어지면 즉시 캘리브레이션

### Success Metrics
- Accuracy > 95% (5개 Fixture 전체)
- False Positive Rate < 5%
- pass@3: 100% (같은 Fixture에 3회 돌려 결과 일관)
