---
title: 베이스라인 거버넌스와 승격
version: 0.1.0
last_updated: 2026-09-04
---

# 베이스라인 거버넌스와 승격

실제 응답을 SSOT 로 삼을 때 그 응답을 무엇으로 저장하고, 언제 새 truth 로 승격할지 결정하는 규칙. 보관 형식, 승격 리뷰, 환경 lineage, 만료를 다룬다.

---

## 원칙

### 1. Baseline Immutability

승인된 baseline 은 임의로 덮어쓰는 캐시가 아니라 리뷰를 거친 증거다. ApprovalTests 관례처럼 승인본(`.approved`)은 소스 컨트롤에 두고 실행 산출물(`.received`)은 생성물로만 취급한다. 둘을 같은 파일에 섞으면 "무엇이 승인된 값인지" 가 사라진다.

> **출처:** [ApprovalTests — Approval files](https://approvaltestscpp.readthedocs.io/en/latest/generated_docs/Tutorial.html#approval-files)

### 2. Masked-raw Baseline

baseline 은 **raw 를 보관한다 — 단 시크릿 값만 마스킹한 raw** 다. 요약본이나 스키마만 남기면 값 drift 를 재현할 수 없고, 마스킹 없는 raw 를 남기면 저장소가 자격증명 저장소가 된다. 마스킹 대상은 토큰·쿠키·`Authorization`·API key 이며, 마스킹 규칙 자체를 baseline 과 함께 버전 관리한다.

> **출처:** [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — 보관 형식은 api-kit 확정 결정

### 3. Contract Versioning — prod 는 스키마만 커밋

prod 환경의 raw 스냅샷은 커밋하지 않고 스키마 계약만 커밋한다. OpenAPI 가 `openapi`(feature set)와 `info.version`(API 계약 버전)을 구분하듯, baseline 도 contract version 과 evidence version 을 분리해 기록한다. prod 증거는 로컬·CI artifact 로만 보관한다.

> **출처:** [OpenAPI Specification v3](https://swagger.io/specification/v3/)

### 4. Promotion Review

baseline 승격은 코드 리뷰 대상이다. Jest 문서도 snapshot 을 코드처럼 커밋·리뷰하고, 실패 원인을 확인하지 않은 채 재생성하는 습관을 피하라고 명시한다. diff 를 보지 않은 승격은 회귀를 truth 로 만드는 행위다.

> **출처:** [Jest Snapshot Testing](https://github.com/jestjs/jest/blob/main/docs/SnapshotTesting.md)

### 5. Env-specific Lineage

baseline 은 환경, 브랜치, provider/API 버전 lineage 를 함께 갖는다. Pact 의 pending 여부도 contract content, verification result, provider branch 조합으로 계산된다. lineage 없는 baseline 은 어느 환경의 진실인지 알 수 없어 비교 대상이 되지 못한다.

> **출처:** [Pact Pending Pacts](https://docs.pact.io/pact_broker/advanced_topics/pending_pacts)

### 6. Drift Acceptance Record

accepted drift 에는 old/new diff, 승인자, 이유, 근거가 된 실행(run), 관련 schema version 을 남긴다. Pact 가 verification result 를 broker 에 publish 해 배포 가능성 판단에 쓰듯, 승인 기록 자체가 다음 판정의 입력이다.

> **출처:** [Pact Provider Verification](https://docs.pact.io/provider)

### 7. Branch Baseline Policy

main/release baseline 과 feature/WIP baseline 을 같은 파일에 섞지 않는다. Pact pending pacts 는 새 계약이 provider 빌드를 불필요하게 깨지 않게 하되, 한 번 accepted 된 뒤의 실패는 회귀로 처리한다. 같은 분리를 브랜치 축에도 적용한다.

> **출처:** [Pact Pending Pacts](https://docs.pact.io/pact_broker/advanced_topics/pending_pacts)

### 8. Expiry Warning

live response 기반 baseline 은 영구 진실이 아니다. 시크릿에 lifecycle 과 만료가 있듯 baseline 에도 "언제 다시 검증할지" 를 명시하고, 만료된 baseline 은 품질 게이트에서 경고 또는 차단 대상으로 올린다.

> **출처:** [OWASP Secrets Management — Secret lifecycle](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html#27-secret-lifecycle)

### 9. Human Override Audit

override 는 이유와 행위자가 남는 감사 이벤트여야 한다. GitHub push protection 도 bypass 시 reason, alert, audit log 를 남기는 모델을 제공한다. 사유 없는 강제 승격은 로그상 정상 승격과 구별되지 않는다.

> **출처:** [GitHub Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)

### 10. Secret-free Baselines

마스킹에만 의존하지 않고 gitignore 와 secret scanning 으로 저장소 유입을 이중으로 막는다. OWASP 와 GitHub 모두 hardcoded credential 을 저장소에 넣지 않는 것을 기본 통제로 둔다. 마스킹은 실수할 수 있고 스캐닝은 그 실수를 잡는 계층이다.

> **출처:** [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), [GitHub Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| 승인본/산출물 커밋 정책 | 승인본은 소스 컨트롤 포함, 실행 산출물(`.received.*`)은 `0건` 커밋 | [ApprovalTests — Approval files](https://approvaltestscpp.readthedocs.io/en/latest/generated_docs/Tutorial.html#approval-files) |
| CI 자동 baseline 갱신 | `0회` — 명시적 update/promote 플래그가 있을 때만 | [Jest Snapshot Testing](https://github.com/jestjs/jest/blob/main/docs/SnapshotTesting.md) |
| accepted 전환 기준 | 동일 contract content 가 해당 branch 에서 `첫 성공 verification` 을 기록하면 pending 해제, 이후 실패는 빌드 실패 | [Pact Pending Pacts](https://docs.pact.io/pact_broker/advanced_topics/pending_pacts) |
| 버전 필드 분리 | root `openapi` = OAS feature set, `info.version` = API 계약 버전 | [OpenAPI Specification v3](https://swagger.io/specification/v3/) |
| secret scanning 사각지대 | public repo push 가 `50MB` 초과면 push protection scan 이 skip 될 수 있음 → 대형 artifact 는 별도 스캔 | [GitHub secret scanning scope](https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-scope) |
| baseline 보관 형식 | 시크릿 값만 마스킹한 raw 응답 | api-kit 확정 결정 |
| prod evidence 커밋 | `0건` — 스키마 계약만 커밋 | api-kit 확정 결정 |
| baseline 만료 | `30일` warning, `90일` block | 추론 |
| 승격 승인자 수 | 기본 `1명`, breaking schema drift 또는 prod lineage 변경은 `2명` | 추론 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| prod raw 스냅샷을 저장소에 커밋 | 실제 고객 데이터와 자격증명이 영구 이력에 남는다 — 나중에 지워도 히스토리에서 사라지지 않는다 |
| diff 실패 시 baseline 을 자동 승격 | 회귀가 새 truth 가 되어 다음 실행부터 green 이 된다 |
| staging/prod/local 이 하나의 baseline 파일 공유 | 환경 차이가 회귀로, 회귀가 환경 차이로 오판된다 |
| 승인 이유 없이 "expected updated" 만 기록 | 6개월 뒤 그 변경이 의도된 것인지 사고인지 판단할 근거가 없다 |
| 만료된 baseline 을 계속 green signal 로 사용 | 검증했다는 착각만 유지되고 실제 계약은 이미 다른 곳에 있다 |

---

## Gotchas

- **baseline 은 비결정적 필드를 영구화하기 쉽다** — timestamp, uuid, 정렬 순서를 그대로 승격하면 이후 모든 실행이 실패한다. 승격 전에 normalize/mask 규칙부터 확정하고, 규칙을 baseline 과 함께 커밋한다.
- **스키마는 배포보다 먼저 merge 될 수 있다** — live response 와 schema version 의 배포 순서를 기록하지 않으면 "아직 배포되지 않은 계약" 을 회귀로 오판한다. lineage 에 배포 시점을 남긴다.
- **gitignore 는 과거 유출을 제거하지 않는다** — 이미 커밋된 비밀은 무시 규칙을 추가해도 히스토리에 남는다. 발견 즉시 rotate/revoke 가 필요하며, 마스킹 규칙 추가만으로 해결됐다고 보고하지 마라.
- **feature branch baseline 을 main truth 로 승격하면 안 된다** — 아직 지원되지 않는 계약이 accepted 로 오인되어, 실제 배포된 API 와 어긋난 기준이 게이트를 통과시킨다.
