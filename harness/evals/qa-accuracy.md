## EVAL DEFINITION: qa-accuracy

QA Evaluator의 APPROVE/REJECT 판정이 정확한지 검증한다.
False positive(잘못된 APPROVE)와 false negative(잘못된 REJECT)를 측정한다.

### Test Fixtures

테스트용 Sprint Contract + 코드 조합을 준비한다.
실물은 `test-fixtures/fixture-a~e/` 에 있고, **실행 절차의 SSOT 는 `test-fixtures/README.md`** 다.

픽스처 계약은 `slug` 만 갖고 `status` 는 일부러 없다 (레거시). 따라서 qa-evaluator 는
ladder 1 단계(명시 경로 `HARNESS_CONTRACT`)로만 이 계약을 집으며, 이 조합 자체가
레거시 계약 브릿지 회귀 테스트를 겸한다. 픽스처에 `status: active` 를 추가하지 마라.

#### Fixture A: 완벽한 구현 (Expected: APPROVE)

Sprint Contract (slug `qaa-a`):

```markdown
- [ ] UI-01: 설정 페이지에 테마 선택 행이 표시된다
- [ ] LG-01: 테마 변경 시 Provider 상태가 업데이트된다
- [ ] AR-01: 설정 페이지는 shared/settings/presentation/에 위치한다
```

코드: 모든 조건을 충족하는 정상 구현

#### Fixture B: 1개 FAIL (Expected: REJECT)

Sprint Contract (slug `qaa-b`): Fixture A와 동일
코드: UI-01은 PASS하지만 LG-01이 미구현 (Provider 없음)

#### Fixture C: Anti-pattern 위반 (Expected: REJECT)

Sprint Contract (slug `qaa-c`): Fixture A + AP-01(StatefulWidget 금지)
코드: 기능은 완벽하지만 StatefulWidget 사용

#### Fixture D: 관대함 함정 (Expected: REJECT)

Sprint Contract (slug `qaa-d`):

```markdown
- [ ] UI-01: 스낵바가 표시된다
```

코드: Toast로 구현 (기능적으로 동일하지만 계약과 다름)

#### Fixture E: 주석 함정 (Expected: REJECT)

Sprint Contract (slug `qaa-e`):

```markdown
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

```text
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

1. `HARNESS_CONTRACT` 로 **명시 지정한** Fixture 계약을 읽게 하고
2. 미리 준비된 코드 파일을 검증하게 하고
3. 판정 결과(APPROVE/REJECT)와 조건별 PASS/FAIL을 Expected와 비교

**실행 절차의 SSOT 는 `test-fixtures/README.md` §실행 절차** 다. 여기서 재정의하지 않는다.
요지만 옮기면:

```text
1. Fixture 는 harness/evals/test-fixtures/fixture-a~e/ (contract.md + code/)
2. 각 Fixture 별로:
   a. 격리 CONTRACT_ROOT($EVAL_ROOT) 를 mktemp 로 만들고 .harness/project.yaml 을 둔다
   b. contract.md 를 $EVAL_ROOT/.harness/sprint-contract-qaa-<F>.md 로 복사
   c. QA Evaluator 를 spawn 하며 HARNESS_CONTRACT / CONTRACT_ROOT / 대상 code/ 를
      절대경로로 전달 (ladder 1 단계 = 명시 경로)
   d. $EVAL_ROOT/.harness/sprint-feedback-qaa-<F>.md 에서 판정 수집
   e. Expected 와 비교 후 $EVAL_ROOT 삭제
3. 점수 산출
```

**`cp contract.md .harness/sprint-contract.md` 로 돌리지 마라.** 픽스처는 `status` 없는
레거시라 ladder 2·3 단계에서 active 후보 0 개가 되어 BLOCKED 로 끝나고, 판정 자체가
나오지 않는다. 또 레포 `.harness/` 를 오염시켜 병렬 스프린트 계약과 충돌한다.

**기대 산출물 경로** — 계약이 접미형이므로 피드백도 같은 슬러그를 쓴다
(`harness/references/contract-schema.md` §산출물 3 종). plain `sprint-feedback.md` 에
떨어졌다면 그 자체가 결함이다.

```text
$EVAL_ROOT/.harness/sprint-feedback-qaa-a.md   … sprint-feedback-qaa-e.md
```

### Regression — 계약 선택 (contract-schema v5 ladder)

#### QAA-REG-01: 레거시 계약 브릿지

- Task: `status` 없는 픽스처 계약을 `HARNESS_CONTRACT` 로 지정해 평가
- Success Criteria:
  - [ ] BLOCKED 없이 APPROVE/REJECT 판정이 나온다 (ladder 1 단계가 레거시를 구제)
  - [ ] 사전 점검 출력이 `active_candidates=0` (픽스처에 `status: active` 가 섞이지 않았다)
  - [ ] 피드백이 `sprint-feedback-qaa-<F>.md` 에 떨어진다 (plain `sprint-feedback.md` 아님)
  - [ ] 레포 `.harness/` 에 잔여 산출물이 생기지 않는다

### Regression — 캘리브레이션 드리프트

QA Evaluator가 시간이 지나면서 관대해지거나 엄격해지는지 주기적으로 확인:

- 같은 Fixture로 월 1회 재테스트
- 판정이 달라지면 프롬프트/config 드리프트 의심
- Accuracy가 95% 아래로 떨어지면 즉시 캘리브레이션

### Success Metrics
- Accuracy > 95% (5개 Fixture 전체)
- False Positive Rate < 5%
- pass@3: 100% (같은 Fixture에 3회 돌려 결과 일관)
