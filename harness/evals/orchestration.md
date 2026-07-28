## EVAL DEFINITION: harness-orchestration

Sprint Contract → Generator → QA Evaluator → REJECT/APPROVE 전체 루프가 작동하는지 검증한다.

### Capability Evals

#### HO-CAP-01: 전체 루프 실행
- Task: "운동 기록 목록 화면 만들어줘"를 전체 하네스로 처리
- Success Criteria:
  - [ ] Sprint Contract 생성 → 사용자 승인
  - [ ] Generator가 계약에 따라 구현
  - [ ] QA Evaluator가 별도 컨텍스트에서 평가
  - [ ] APPROVE 또는 REJECT 판정
  - [ ] 전체 과정이 중단 없이 완료

#### HO-CAP-02: REJECT → 재작업 루프
- Task: QA Evaluator가 REJECT했을 때 Generator가 피드백을 반영하여 수정
- Success Criteria:
  - [ ] Generator가 **평가된 계약과 같은 슬러그**의 QA 산출물을 읽음
        (`.harness/sprint-feedback-<slug>.md`, plain 모드면 `.harness/sprint-feedback.md`)
  - [ ] FAIL 항목에 대해서만 수정 (PASS 항목 건드리지 않음)
  - [ ] 수정 후 QA Evaluator 재실행
  - [ ] 최대 3회 루프 후에도 REJECT이면 사용자에게 에스컬레이션

#### HO-CAP-03: develop 워크플로우 통합
- Task: 기존 /develop 9단계에 하네스가 자연스럽게 삽입
- Success Criteria:
  - [ ] Step 1(Sprint Contract)에서 계약 생성
  - [ ] Step 4(구현) 완료 후 QA Evaluator 실행 (Step 5)
  - [ ] QA APPROVE 후에 Step 7(빌드)으로 진행
  - [ ] 기존 Step 8(audit)과 QA Evaluator(Step 5)는 독립적으로 동작

#### HO-CAP-04: .harness/ 파일 관리
- Task: 하네스 산출물이 체계적으로 관리되는지
- 경로 규약 SSOT: `harness/references/contract-schema.md` §산출물 3 종
- Success Criteria:
  - [ ] `.harness/sprint-contract-<slug>.md` — 계약서 (plain 모드면 `sprint-contract.md`)
  - [ ] `.harness/sprint-feedback-<slug>.md` — QA 피드백 (APPROVE 시 최종 결과 포함)
  - [ ] `.harness/sprint-amendments-<slug>.md` — 스프린트 중 합의 변경 (발생했을 때만)
  - [ ] 3 종의 슬러그가 서로 일치 (계약은 접미형인데 피드백만 plain 이면 FAIL)
  - [ ] 계약 frontmatter 에 `slug` / `status` 가 있고, 스프린트 종료 시 `status: done` 으로 전환
  - [ ] 이전 하네스 결과는 `.harness/history/{YYYYMMDD-HHmm}-sprint-contract-<slug>.md`로 보관

### Regression Evals

#### HO-REG-01: 기존 워크플로우 호환
- Tests:
  - develop-without-harness-still-works: PASS/FAIL (단순 수정엔 하네스 불필요)
  - audit-independent-of-qa: PASS/FAIL
  - preflight-unaffected: PASS/FAIL
  - legacy-plain-contract-still-evaluated: PASS/FAIL
    (`status` 없는 레거시 계약도 `HARNESS_CONTRACT` 명시 경로로 판정이 나온다 — BLOCKED 금지)

### End-to-End Test Scenario

```text
Input: "운동 기록을 날짜별로 그룹핑해서 보여주는 화면 만들어줘"

Expected Flow:
1. Sprint Contract 생성 (.harness/sprint-contract-<slug>.md · status: active)
   - UI: 날짜별 그룹 헤더 + 기록 리스트 표시
   - Logic: Repository에서 날짜별 그룹핑 처리
   - Error: 데이터 없을 때 빈 상태 화면 표시
   - Architecture: Clean Architecture 준수
   → 사용자 승인

2. Generator 구현
   → 코드 생성

3. QA Evaluator (별도 컨텍스트)
   → ladder 로 계약 특정 (명시 경로 > 세션 소유 active 유일 > active 유일 > BLOCKED)
   → 계약 파싱 + 코드 읽기 + 조건 대조
   → 판정: APPROVE or REJECT → sprint-feedback-<slug>.md 저장

4a. REJECT → Generator 가 같은 슬러그의 feedback 을 읽고 수정 → QA 재실행
4b. APPROVE → 빌드/감사/검증 진행 → 계약 status: done
```

### Success Metrics
- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
- E2E scenario: 3회 실행 중 2회 이상 APPROVE 도달
