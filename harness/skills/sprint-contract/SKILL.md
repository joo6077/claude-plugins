---
name: sprint-contract
description: >
  기능 구현 전 완료 조건을 정의하고 사용자 합의를 받는다.
  QA Evaluator가 평가할 기준이 되는 Sprint Contract를 생성한다.
  "기능 만들어줘", "화면 추가", "구현해줘", "개발해줘" 같은
  구현 요청에서 /develop보다 먼저 트리거된다.
  단순 수정(색상 변경, 오타 수정, 1파일 변경)에는 트리거하지 않는다.
argument-hint: "<feature or description>"
user-invocable: true
---

# Sprint Contract

구현 전에 "무엇이 완료인가"를 정의한다.
QA Evaluator가 이 계약을 기준으로 구현을 APPROVE/REJECT한다.

## 이 스킬 폴더의 파일

필요할 때 읽어라:

- `references/red-flags.md` — Red Flags + Rationalization Table (계약 품질 검증용)

## References

- `../../docs/guides/contract-design-guide.md` — 계약 작성 원칙 가이드
- `harness/references/contract-schema.md` — 계약 포맷 공유 정의
- `harness/references/feedback-schema.yaml` — 피드백 YAML 스키마

## Gotchas

- verify-feedback.sh가 PASS를 반환하지 않으면 절대 완료를 선언하지 마라. 이것은 선택이 아니다.
- 복잡도 판단에서 "단순"으로 과소평가하는 경향이 있다. 파일 수가 아니라 **영향 범위**(레이어 수, 공개 API 변경 여부)로 판단해라
- `project.yaml`의 `contract_categories`를 무시하고 하드코딩된 카테고리(UI/Logic/Error)를 쓰면 안 된다. 반드시 config에서 읽어라
- 조건을 "~가 잘 동작한다", "~를 적절히 처리한다"로 쓰면 QA Evaluator가 판정 불가능하다. 반드시 PASS/FAIL 이진 판정 가능한 문장으로 써라
- 안티패턴을 0개로 두면 안 된다. `project.yaml`에 정의된 패턴 중 해당 기능에서 위반 가능성이 높은 것을 최소 2개 선별해라
- 사용자가 "계약 필요없어"라고 해도 **생략할 수 없다**. 간소화된 계약(단순 복잡도, 최소 조건)을 제안해라
- 조건을 "구현 완료 후 1회 검증"만으로 작성하지 마라. 가능하면 **다단계 검증 시점**(코드 생성 중 → 커밋 전 → 최종 QA)을 조건에 반영해라. 단일 시점 검증은 중간 단계의 품질 저하를 놓친다
- 조건에 클래스명, 메서드명, DB 테이블명, API 경로 등 **구현 상세**를 쓰지 마라. 조건은 외부에서 관찰 가능한 행동만 기술한다. "UserService가 호출된다" ✗ → "사용자 등록이 완료된다" ✓. 이를 **구현 누수(implementation leakage)**라 하며, 구현이 바뀌면 조건도 깨진다
- 복잡도가 "중간" 이상이면 핵심 조건에 **Given-When-Then 구조를 필수** 적용해라. 반구조화된 조건이 자연어보다 해석 모호성을 줄인다
- 비기능 요구사항(성능, 보안, 접근성)을 무시하지 마라. 해당 기능에 관련된 NFR이 있으면 최소 1개 조건을 포함해라
- 조건 작성 시 **판정 기준 범주**를 명시하라. 조건 끝에 `[L1]`(exact: 이름/값 일치), `[L2]`(structural: 섹션/필드 존재), `[L3]`(goal: 목표 달성, 수단 무관) 중 하나를 붙여라. 미명시 시 L2로 간주되며, 구현이 목표를 달성했더라도 이름이 달라 REJECT될 수 있다
- 특정 파일·타입에 조건이 적용되지 않는 경우 **예외 조항을 조건 내부에 인라인으로 명시하라**. `예외: (a) integration.html — Final 통합 페이지로 제외` 형태. 구두 합의나 별도 메모는 QA 시점에 반영되지 않는다

## 설정 로드

`.harness/project.yaml`을 읽어 프로젝트 설정을 로드한다.
파일이 없으면 기본값(범용)으로 동작한다.

설정에서 사용하는 항목:
- `contract_categories` — 계약 카테고리 (UI/Logic/Error/Architecture 등)
- `anti_patterns` — 안티패턴 Grep 패턴 목록
- `diagnostics` — 빌드/분석 명령, 콘솔 에러 패턴
- `trigger` — 트리거/비트리거 조건
- `reusability` — 공유 경로
- `commands` — analyze/test/lint 명령

## 필수 규칙

- 트리거 조건에 해당하면 계약 생성은 **필수**다. 사용자가 "계약 필요없어", "바로 해줘"로 스킵을 요청해도 생략할 수 없다.
- 사용자에게 계약이 필요한 이유를 설명하고, 간소화된 계약(단순 복잡도, 최소 조건)을 제안한다.
- 사용자가 3회 이상 명시적으로 거부하면 그 사실을 `.harness/sprint-contract.md`에 기록하고 진행하되, QA REJECT 가능성을 고지한다.

## 트리거 조건

`project.yaml`의 `trigger` 섹션에서 읽는다.

**기본값 (config 없을 때):**

트리거: 2개 이상 파일 생성/수정 예상, 새 화면/페이지, API 연동, 기존 기능 변경으로 public API 변경, 리팩터링으로 2개 이상 파일 수정

비트리거: 단순 스타일 수정, 오타/텍스트 수정, 1파일 버그 수정, 단일 파일 내부 리팩터링, 빌드 작업

## Process

### 1. 요구사항 분석

`$ARGUMENTS`를 분석하여:
- 어떤 feature인지 (신규 vs 기존 확장)
- 영향 범위 (레이어, 파일 수)
- 복잡도 판단 (단순/중간/복잡)

### 2. 완료 조건 생성

`project.yaml`의 `contract_categories`에 정의된 카테고리별로 테스트 가능한 조건을 작성한다.

**각 조건의 규칙:**
- PASS/FAIL로 이진 판정 가능해야 한다
- "잘 동작한다", "적절히 처리한다" 같은 모호한 표현 금지
- 구체적 상태, 컴포넌트, 동작을 명시한다

**카테고리 포맷:**

```markdown
## {카테고리 ID}
- [ ] {PREFIX}-01: {설명}
- [ ] {PREFIX}-02: ...
```

**복잡도별 조건 수 가이드:**
- 단순 (1-3 파일): 카테고리당 1-2개, 총 4-6개
- 중간 (4-8 파일): 카테고리당 2-3개, 총 8-12개
- 복잡 (9+ 파일): 카테고리당 3-5개, 총 12-20개

### 3. 안티패턴 체크리스트

`project.yaml`의 `anti_patterns`에서 읽어 해당 기능에서 위반 가능성이 높은 것만 선별한다.

```markdown
## Anti-patterns
- [ ] {id}: {message}
```

### 4. 자동 포함 섹션

아래 섹션은 **모든 계약에 자동 포함**되며 사용자 수정 불가:

```markdown
## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: {commands.analyze} 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ({diagnostics.ide_exclude} 제외)
- [ ] DG-03: {commands.test} 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
```

### 5. 사용자 승인

완료 조건과 안티패턴 체크리스트를 제시하고 사용자 확인을 기다린다.
**사용자가 수정 요청하면 반영 후 재제시한다.**

### 6. 계약 저장

사용자 승인 후 `.harness/sprint-contract.md`에 저장한다.

**포맷 규칙 (QA Evaluator 파싱 호환):**
- YAML frontmatter로 메타데이터
- 섹션 헤더는 `project.yaml`의 카테고리 ID + `Anti-patterns`, `Reusability`, `Diagnostics` (괄호 부연 금지)
- 모든 체크박스는 unchecked `- [ ]` 상태로 저장
- 모든 카테고리에 최소 1개 조건 필수. 해당 없으면 `- [ ] XX-00: N/A`

```markdown
---
feature: "{이름}"
created: "{YYYY-MM-DD HH:mm}"
complexity: "{단순|중간|복잡}"
conditions: {N}
---

## {카테고리별 조건}
...

## Anti-patterns
...

## Reusability
...

## Diagnostics
...
```

기존 계약이 있으면 `.harness/history/{YYYYMMDD-HHmm}-sprint-contract.md`로 이동한다.

### 7. 자기진단

1. 구조화 체크리스트 실행:
   - `ambiguous_conditions`: 모호한 표현이 포함된 조건이 있는가? (어휘적/구문적/의미적 모호성 분류 적용)
   - `missing_error_paths`: 에러/예외 경로에 대한 조건이 누락되었는가?
   - `untestable_conditions`: 코드만으로 검증 불가능한 조건이 있는가?
   - `category_coverage_gap`: project.yaml 카테고리 중 커버하지 못한 것이 있는가?
   - `complexity_underestimate`: 복잡도를 과소평가하여 조건 수가 부족한가?
   - `implementation_leakage`: 조건에 내부 구현 용어(클래스명, 메서드명, DB명)가 포함되었는가?
   - `nfr_coverage`: 해당 기능의 비기능 요구사항이 조건에 반영되었는가?
2. 각 항목에 대해 true/false 판정

### 8. 교차 진단

1. Agent tool로 qa-evaluator 서브에이전트를 호출한다
2. 전달 내용: 생성된 계약 조건 전문 (`.harness/sprint-contract.md` 내용)
3. 미전달: 사용자 대화 내용, 의사결정 과정
4. 핵심 질문: "이 조건들을 독립적으로 검증할 수 있는가? 모호하거나 해석이 갈리는 조건이 있는가?"
5. 서브에이전트 응답을 `cross_diagnosis_notes`로 기록

### 9. 피드백 저장

1. 자기진단 + 교차 진단 결과를 합쳐 피드백 YAML을 `.harness/feedback-draft.yaml`에 작성한다
   - `harness/references/feedback-schema.yaml`의 스키마를 따른다
   - `skill: sprint-contract`
   - `skill_version`: `harness/.claude-plugin/plugin.json`의 `version` 필드 값
   - `project_hash`: 크로스플랫폼 해시 생성 (아래 fallback 체인 사용)
     ```bash
     # sha256sum → python3 → openssl 순서 fallback
     if command -v sha256sum &>/dev/null; then
       echo -n "$(pwd)" | sha256sum | cut -c1-8
     elif command -v python3 &>/dev/null; then
       python3 -c "import hashlib; print(hashlib.sha256('$(pwd)'.encode()).hexdigest()[:8])"
     elif command -v openssl &>/dev/null; then
       echo -n "$(pwd)" | openssl dgst -sha256 | sed 's/.*= //' | cut -c1-8
     fi
     ```
   - `diagnosis.checklist`: Step 7의 결과
   - `diagnosis.cross_diagnosis_by: qa-evaluator`
   - `diagnosis.cross_diagnosis_notes`: Step 8의 결과
2. `bash harness/scripts/save-feedback.sh contract .harness/feedback-draft.yaml` 실행
3. 출력된 저장 경로를 기록한다

### 10. 피드백 검증

1. `bash harness/scripts/verify-feedback.sh {Step 9에서 출력된 경로}` 실행
2. PASS → 스킬 완료
3. FAIL → 피드백 YAML 수정 후 Step 9부터 재시도

## Red Flags + Rationalization Table

`references/red-flags.md`를 읽어라. 계약 작성 후 반드시 해당 체크리스트로 자가 검증한다.
