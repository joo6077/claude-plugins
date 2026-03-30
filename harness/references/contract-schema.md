# Sprint Contract 스키마

> sprint-contract와 qa-evaluator가 공유하는 계약 포맷 정의.
> contract-kaizen이 변경 제안 가능, evaluator-kaizen이 읽어서 평가 루브릭에 반영.

## 계약 파일

**경로**: `.harness/sprint-contract.md`

## 메타데이터 (YAML frontmatter)

```yaml
feature: "{기능명}"
created: "{YYYY-MM-DD HH:mm}"
complexity: "{simple|medium|complex}"
conditions: {총 조건 수}
```

## 필수 섹션

### 1. 카테고리별 조건

```markdown
## {CategoryID}
- [ ] {PREFIX}-{NN}: {PASS/FAIL 이진 판정 가능한 조건문}
```

- `CategoryID`와 `PREFIX`는 `project.yaml.contract_categories`에서 가져온다
- 조건문은 능동태, 단일 조건, 측정 가능해야 한다
- "잘 동작한다", "적절히 처리한다" 같은 모호 표현 금지

### 2. Anti-patterns

```markdown
## Anti-patterns
- [ ] {id}: {message}
```

- `project.yaml.anti_patterns`에서 최소 2개 선별
- 해당 구현에서 발생 가능성이 높은 것을 우선 선택

### 3. Reusability (자동 포함)

```markdown
## Reusability
- [ ] RE-01: private 일회용 컴포넌트가 없다
- [ ] RE-02: 기존 공용 컴포넌트를 재사용한다
```

### 4. Diagnostics (자동 포함)

```markdown
## Diagnostics
- [ ] DG-01: analyze 경고 0건
- [ ] DG-02: analyze 에러 0건
- [ ] DG-03: 테스트 전체 통과
- [ ] DG-04: 콘솔 에러 0건
```

## 복잡도별 조건 수 가이드

| 복잡도 | 파일 영향 | 조건 수 |
|--------|----------|--------|
| 단순 | 1-3 | 4-6 |
| 중간 | 4-8 | 8-12 |
| 복잡 | 9+ | 12-20 |

## 스키마 버전

현재: v1
