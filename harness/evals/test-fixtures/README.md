# QA Accuracy Test Fixtures

qa-accuracy.md eval에서 사용하는 테스트 픽스처.
각 Fixture는 sprint-contract + 코드 조합으로 구성된다.

## 디렉토리 구조

```
test-fixtures/
├── fixture-a/          # 완벽한 구현 → Expected: APPROVE
│   ├── contract.md
│   └── code/
├── fixture-b/          # 1개 FAIL → Expected: REJECT
│   ├── contract.md
│   └── code/
├── fixture-c/          # Anti-pattern 위반 → Expected: REJECT
│   ├── contract.md
│   └── code/
├── fixture-d/          # 관대함 함정 (동의어) → Expected: REJECT
│   ├── contract.md
│   └── code/
└── fixture-e/          # 주석 함정 → Expected: REJECT
    ├── contract.md
    └── code/
```

## 사용법

```bash
# Fixture A 테스트
cp test-fixtures/fixture-a/contract.md .harness/sprint-contract.md
# QA Evaluator 서브에이전트 spawn → test-fixtures/fixture-a/code/ 검증
# Expected: APPROVE
```
