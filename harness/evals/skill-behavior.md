## EVAL DEFINITION: harness-skill-behavior

sprint-contract가 project.yaml을 올바르게 읽고, 설정에 맞는 계약을 생성하는지 검증한다.

### Capability Evals

#### HSB-CAP-01: Flutter config로 계약 생성
- Task: 현재 project.yaml(Flutter) 상태에서 "운동 기록 목록 화면 만들어줘" 요청
- Success Criteria:
  - [ ] 계약 카테고리가 project.yaml의 contract_categories와 일치 (UI, Logic, Error, Architecture)
  - [ ] Anti-patterns가 project.yaml의 anti_patterns에서 선별됨
  - [ ] Diagnostics의 analyze 명령이 "fvm.bat flutter analyze"
  - [ ] Reusability의 shared_path가 "shared/presentation/widgets/"

#### HSB-CAP-02: config 변경 시 계약이 달라짐
- Task: project.yaml을 Rust 설정으로 임시 변경 후 동일 요청
- Success Criteria:
  - [ ] 카테고리가 Rust용으로 변경됨 (API, Database, Error, Architecture)
  - [ ] Anti-patterns가 Rust용 (unwrap, println!)
  - [ ] Diagnostics의 analyze 명령이 "cargo clippy"
  - [ ] Flutter 전용 패턴(StatefulWidget 등)이 나타나지 않음

#### HSB-CAP-03: config 없을 때 기본값
- Task: project.yaml을 제거한 상태에서 계약 생성 시도
- Success Criteria:
  - [ ] 에러 없이 기본 카테고리(UI/Logic/Error/Architecture)로 생성
  - [ ] Anti-patterns는 빈 상태이거나 범용 패턴만 포함
  - [ ] Diagnostics는 "analyze/test 명령 미설정" 표시

#### HSB-CAP-04: procedures 참조
- Task: QA Evaluator가 procedures 파일을 실제로 읽고 따르는지
- Success Criteria:
  - [ ] UI 조건 검증 시 ui-verification.md의 절차를 따름
  - [ ] Error 조건 검증 시 error-verification.md의 체인 추적을 수행
  - [ ] procedure 파일 없는 카테고리는 범용 검증으로 폴백

#### HSB-CAP-05: trigger 조건 준수
- Task: project.yaml의 trigger 설정이 반영되는지
- Success Criteria:
  - [ ] "색상 변경해줘" → 트리거 안 됨 (never 목록)
  - [ ] "새 화면 만들어줘" → 트리거됨 (always 목록)
  - [ ] 1파일 수정 예상 → 트리거 안 됨 (min_files: 2)

### Pressure Tests

#### HSB-PRESS-01: config에 없는 패턴을 하드코딩
- Scenario: project.yaml에 StatefulWidget 패턴이 없는데 sprint-contract가 Anti-patterns에 포함
- Expected: config에 없는 패턴은 포함하지 않음
- Detect: "프로젝트 규칙이니까 당연히 포함해야 한다"

#### HSB-PRESS-02: config 카테고리 무시
- Scenario: project.yaml에 카테고리가 API/Database/Error/Architecture인데 UI 카테고리 생성
- Expected: config의 카테고리만 사용
- Detect: "UI는 기본이니까 항상 포함해야 한다"

### Test Method

서브에이전트를 spawn하여:
1. project.yaml을 읽게 하고
2. 특정 기능 요청에 대한 sprint-contract 초안을 생성하게 하고
3. 출력이 config와 일치하는지 확인

```bash
# Config 유효성은 스크립트로 사전 검증
bash harness/scripts/validate.sh
```

### Success Metrics
- pass@3 > 90% for capability evals
- Pressure tests: 0% config 무시율
