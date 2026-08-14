---
phase: 2
title: Phase 2 Contract — 확보된 외부 근거 + 실측 결함
collected: 2026-08-13
method: codex (foreground 회수)
note: 이 파일이 Phase 2 의 유일한 외부 근거다. 추가 외부 조회 금지. 여기 없는 URL·수치를 지어내지 마라.
---

## 0. 먼저 확인할 것

`harness/references/contract-schema.md` 의 **실제 현재 버전**을 파일에서 읽어 확인하라.
로컬 관측은 **v5.2** 다. 문서 어딘가에 v4 로 적힌 곳이 있으면 그것이 drift 다.

## 1. 실측 결함 (데이터풀 §1, 2026-08-11~12 — 이번 사이클 최대 신호)

### F1. 산문 조건과 측정문이 서로 다른 것을 잰다

improvement 원문:

> "[AR-04] 계약-측정-불일치 — 조건 프로즈(화이트리스트 12항목)와 측정 필드(5개 무관 디렉토리 grep)의
> 커버리지 갭. 측정 필드에 화이트리스트 개별 대조를 포함시켜라"

### F2. 경로 화이트리스트 위반 5건 연속 + 계약 자기편집

- "AR-04: 계약 명시 5개 pathspec 밖에 위치"
- "AR-04: 허용 경로 밖 (1건)"
- "AR-04: git show --name-only 결과가 계약이 enumerate 한 3개 경로 밖에 있다 — 리터럴 위반"
- **"AR-04: 계약 write-once 위반 — 생성자가 자신이 만든 산출물을 사후에 허용하려 계약 AR-04 조건 문구를
  직접 편집(5→7 경로, 사이드카/사용자 승인 앵커 없음)"**

직전 사이클이 amendment 사이드카를 도입했는데도 발생했다.
**왜 사이드카가 쓰이지 않았는지 근본원인을 규명하라.** 문장 추가로는 6번째 재발이 난다.

### F3. 조합 케이스 수를 사람이 타이핑해서 틀린다

- "3 visibility x 6 relation = 18 케이스 중 15케이스(5 relation)만 재현. GroupMemberAndFollower 관계 전체 누락"
- "16종 매핑 단위 테스트 커버리지 부족 (2종만 검증)"
- improvement: "audience_matrix.rs 의 6 relation 을 feed_integration.rs 가 상수/enum 으로 재사용해
  6 author x 3 visibility = 18 을 기계적으로 순회하게 만들면 수 불일치 재발 방지"

### F4. QA 모호성 태그가 계약 작성 단계로 되먹여지지 않는다

improvement 태그로 반복 등장: `측정-수단-부재`, `측정-방식-불일치`, `측정-환경-오염`,
`측정-산출물-부재`, `검증경로-미기재`, `측정-중복`.

### F5. write-once 원문이 amendment 로 대체된 채 남는다

> "[LG-02, LG-04] write-once 계약 원문이 amendment 로 대체된 채 남아있다 — 다음 계약 작성 시 확정 문구 반영 권장"

## 2. 확보된 외부 근거

### F1 — 확립된 이름과 기법

단일 용어보다 `requirements traceability gap` / `verification method mismatch` /
`verification-validation mismatch` 에 가깝다.

- NASA 는 요구사항마다 검증 접근을 식별하고, 각 `shall` 을 고유 ID 와 source 에 연결한
  **verification matrix** 를 요구한다. 또한 trace 가 parent requirement 를 **"fully addresses"** 하는지
  **독립적으로 평가**하라고 한다.
  <https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/>
  <https://www.nasa.gov/reference/6-2-requirements-management/>
- LLM judge 문헌도 평가 입력을 `evaluation criteria` / `reference` / `item` 으로 분리하고,
  criteria·reference 누락이 신뢰도를 낮춘다고 본다.
  <https://arxiv.org/html/2412.05579>
  <https://arxiv.org/html/2506.13639v1>

### F2 — baseline + change control

- NASA: established requirements baseline 변경은 **change request 로 평가하고 change board/CCB
  승인 후** 반영. <https://www.nasa.gov/reference/6-2-requirements-management/>
- IEEE 830 은 **ISO/IEC/IEEE 29148 로 대체**되었다.
  <https://standards.ieee.org/ieee/830/1222/>
  <https://www.iso.org/standard/72089.html>

### F3 — 조합 커버리지

- NIST ACTS / Combinatorial Testing 은 t-way 조합 커버리지와 covering array 를 공식적으로 다룬다.
  combinatorial coverage 는 statement/branch coverage 와 **다른** 정적 test-set 속성이다.
  <https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software/faqs>
  <https://www.nist.gov/publications/combinatorial-coverage-measurement>
- Gherkin: 한 시나리오에 one When-Then pair.
  <https://github.com/andredesousa/gherkin-best-practices>

### F4 — 모호성 분류

- Tjong/Berry 는 lexical / syntactic / semantic ambiguity 를 분류하고 guiding rules 를
  **inspection checklist** 로 쓸 수 있다고 한다.
  <https://cs.uwaterloo.ca/~dberry/FTP_SITE/tech.reports/TjongThesis.pdf>
- SREE 는 ambiguity indicator corpus 를 lexical scan 으로 잡고, lexical scope 에서 **100% recall 을
  목표로 하되 사람이 false positive 를 판단**한다.
  <https://cs.uwaterloo.ca/~dberry/ambig.in.RSs.html>
- Tjong/Berry 분류를 그대로 acceptance criteria contract schema 로 전환한 1차 선례는 **미확인**.
  인접: AmbiTRUS 2025 <https://www.sciencedirect.com/science/article/abs/pii/S0164121225000251>

## 3. 제안된 스키마 조항 (초안 — 우리 체계에 맞게 재작성하고, 과잉이면 줄여라)

- 각 조건에 `condition_id`, `intent_claims[]`, `required_targets[]`, `measurement.targets[]`,
  `measurement.command`, `precondition`, `coverage_relation: exact|superset|subset`, `evidence_artifact`.
- E3 게이트가 `required_targets - measurement.targets == ∅` 를 **계산**한다.
  산문이 화이트리스트 12개면 측정도 12개를 전부 포함하거나, 상위 패턴이 12개를 덮는다는 **확장 결과**를 출력.
- `measurement.command` 는 파싱 가능한 구조. free text grep 금지. pathspec / exclude / expected set 분리 필드.
- path whitelist 는 `scope_allowlist` 로 **단일 관리**. `git diff --name-only` 결과가 밖이면 즉시 FAIL.
- 계약 최초 저장 시 `locked_at`, `baseline_sha256`, `author_session`, `allowed_paths_hash` 기록.
  구현 시작 후 본문 수정 금지 — 본문을 고쳐 allowlist 를 늘려도 `baseline_sha256` 이 깨져 FAIL.
- amendment 는 **`narrowing` 만 자동 적용**. `relaxing`/`unknown` 은 PASS 근거 금지 + 사용자 재승인 필요.
- 조합 조건은 `factors` 블록으로 선언하고 generator 가 케이스를 산출. `cases_total` 수기 입력 금지.
- QA taxonomy 4종을 조건 작성 preflight 로 승격:
  `missing_measurement` / `oracle_mismatch` / `environment_contamination` / `missing_evidence_artifact`.

## 4. 넣지 말아야 할 것 (명시적 금지)

- "측정이 조건 의도를 커버하는지 확인하라" 같은 Gotcha 한 줄 추가
- LLM 에게 "모호한가?" 만 묻는 게이트
- `conditions:` 처럼 사람이 숫자를 옮겨 적는 필드
- `relaxing` amendment 를 조용히 최신 계약으로 간주하는 규칙
- path whitelist 를 자연어 문장과 grep 명령 양쪽에 중복 관리하는 구조

## 5. 트레이드오프 (반영하라)

계약 작성 비용이 오른다. 조합 게이트를 작은 변경에도 강제하면 과잉 절차다.
권장 기준: **"2개 이상 축의 곱이 조건 의미를 결정할 때만 필수"**.
lexical ambiguity linter 는 false positive 가 많아 자동 판정기가 아니라
"검출기 + 사람의 해소 기록" 으로 써야 한다.

## 6. 열린 질문 (계약에 결정 근거를 남겨라)

- path whitelist 판정 기준을 `working tree` / `staged` / `branch diff` 중 무엇으로 고정할지.
- `relaxing` amendment 승인 주체를 사용자 명시 승인으로 할지, reviewer 확인까지 요구할지.
- 조합 full Cartesian 과 pairwise 의 기본값을 복잡도별로 나눌지.
