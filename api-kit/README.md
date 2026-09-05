# api-kit

실제 응답을 SSOT로 삼는 블랙박스 API 계약 검증 킷.

## 개요

문서도 소스도 못 믿을 때, **한 번 실제로 때려서 받은 응답을 기준선으로 삼는다.**
OpenAPI 스펙이 없어도, 사람이 쓴 md 와 curl 덤프만 있어도 동작한다.
소스 접근 없이 밖에서 때리므로 다른 팀 API·서드파티 API 에도 쓸 수 있다.

```text
탐색 실행  →  응답 스냅샷 봉인  →  계약(스키마) 추출  →  회귀 실행 시 diff
```

앞의 두 단계가 GUI API 도구를 대체하고, 뒤의 두 단계가 테스트 자동화다.

`/backend-test` 는 **화이트박스**다 — 소스를 읽고 테스트 코드를 만든다.
api-kit 은 **블랙박스**다 — 돌아가는 서버를 밖에서 때려 계약을 뽑는다. 겹치지 않는다.

## 스킬

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `api-contract` | 봉인된 응답 스냅샷에서 계약을 추출한다. 스키마(존재·타입·nullable·enum)와 경로별 assertion 을 뽑아 |
| `api-init` | 블랙박스 API 검증의 기반이 되는 `.api/` 를 초기화한다. OpenAPI 스펙 · 사람이 쓴 md · |
| `api-probe` | 인벤토리의 엔드포인트를 실제로 호출해서 응답을 눈으로 확인하고 스냅샷으로 봉인한다. |
| `api-ui` | `.api/` 산출물 전체를 읽어 의존성 0 단일 파일 계약 뷰어 `.api/ui.html` 을 생성하고 연다. |
| `api-verify` | 계약 전체(또는 필터)를 다시 실행해 baseline 과 대조하고 PASS/FAIL 리포트 + canonical diff 를 낸다. |
<!-- /AUTO:skills -->

## 에이전트

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| `api-reviewer` | 추출된 API 계약이 적절한지 원칙 기준으로 독립 평가한다. |
<!-- /AUTO:agents -->

`api-reviewer` 는 단독 실행하지 않는다 — `/api-contract` 또는 `/api-verify` 를 통해 호출된다.

## 계약 강도 3단계

```text
partial (기본)  존재 · 타입 · enum          — 형태만 본다
pin             위 + 경로별 명시 assertion   — 타입은 멀쩡한데 값만 망가진 회귀를 잡는다
exact           정규화 후 본문 전체 diff
```

**`pin` 은 '값 고정' 이 아니다.** 값 고정(`const`)은 pin 이 표현할 수 있는 assertion 한 종류일 뿐이다.

| 필드 성격 | assertion | 예 |
|---|---|---|
| 안정값 | 값 고정 | `$.token_type = "Bearer"` |
| 열거형 | 집합 소속 | `$.data[].status ∈ active·shipped·cancelled` |
| 변동 수치 | 범위·불변식 | `$.meta.total ≥ len($.data)` |
| 식별자 | 패턴 | `$.orderId ^ord_` |

`total`·`cursor`·`id`·`timestamp` 처럼 매 호출 변하는 필드에 값을 고정하면 매번 실패한다.
**타입 변경은 pin 이 아니라 partial 이 잡는다.**

비교 기준선은 RFC 8785 JCS canonical JSON 이다. 사람이 읽는 화면 표시용 포매팅과 분리한다.

## 안전 가드

- **prod 는 기본 read-only** — GET/HEAD/OPTIONS. 쓰기 메서드는 명시 allowlist 없이는 실행하지 않는다
- **자격증명은 `.gitignore` 등록을 강제** — 등록 확인과 추적 검사를 통과하지 못하면 파일을 만들지 않는다
- **시크릿은 킷 자체 scrubber 를 거친다** — Hurl `--secret` 은 stderr 와 리포트만 가리고 stdout 은 가리지 않는다
- **prod 스냅샷은 커밋하지 않는다** — 스키마만 커밋한다

## 뷰어

`/api-ui` 가 `.api/` 전체를 **의존성 0 단일 HTML** 로 만든다. `file://` 더블클릭으로 열린다.

**브라우저는 요청을 쏘지 않는다.** 폼은 편집 가능하되 `실행` 은 커맨드를 클립보드에 복사한다.
브라우저에서 임의 호스트로 요청을 쏘면 CORS 실패가 기본값이고, 우회하려면 프록시가 필요하며,
토큰을 브라우저에 두게 된다. 요청 실행은 이미 Hurl + CLI 가 맡고 있다.

## 리서치 문서

`docs/api/` 에 12개 원칙 문서가 있으며 모든 스킬이 이를 SSOT 로 참조한다.

### discovery — 입력을 인벤토리로
- **api-inventory-normalization** — operation key 표준화, 소스 신뢰도, 충돌 플래그
- **artifact-interop-import-export** — curl/Talend 임포트 충실도, HAR·JUnit 익스포트, 손실 경고

### execution — 실제로 때리기
- **probe-synthesis-hurl-semantics** — Hurl 옵션 우선순위, capture, entry 격리, exit code
- **environment-safety-gates** — safe method, prod read-only, redirect 가드, rate·timeout 예산
- **auth-secret-lifecycle** — 토큰 발급·TTL 갱신·주입, redaction 경계, 인증 실패 분류

### contract — 계약 만들기
- **snapshot-sealing-canonicalization** — raw evidence 보존, JCS 정규화, I-JSON 게이트, manifest 해시
- **contract-extraction-modes** — partial/pin/exact, required 추론, enum 승격, additionalProperties
- **multi-sample-pagination-variance** — 샘플 예산, 페이지네이션 탐색, 분산 점수, 커서 안전
- **error-status-contracts** — RFC 9457 problem details, 상태 클래스, 4xx pin, 5xx 제외

### verification — 회귀 잡기
- **regression-diff-failure-policy** — drift 분류, exit code 계약, 재시도 확정, CI 산출물
- **static-evidence-viewer-contract** — 런타임 의존성 0, 브라우저 네트워크 0, escape 규칙, 접근성
- **baseline-governance-promotion** — baseline 불변성, 승격 검토, 환경 계보, 만료 경고

리서치 이력과 미검증 항목은 `docs/api/research-log.md` 에 있다.

## 카이젠

- `/api-research` — 외부 1차 출처 폴링으로 `docs/api/` 갱신
- `/api-kaizen` — 리서치 문서 기준으로 스킬 품질 점진 개선

## 사용 예시

```text
/api-init                     스펙·문서·curl 덤프에서 인벤토리 생성
/api-probe orders.list        엔드포인트 하나를 때려 스냅샷 봉인
/api-contract orders.list     스냅샷에서 계약 추출
/api-verify                   전체 회귀 검증
/api-ui                       결과를 단일 HTML 뷰어로 열기
```

## 범위 밖

| 제외 | 이유 |
|---|---|
| gRPC / GraphQL / WebSocket | 계약 모델이 다르다. 필요해지면 별도 어댑터로 |
| 부하·성능 테스트 | k6 영역 |
| consumer-driven contract | Pact 영역. 양쪽 코드를 통제할 때의 문제 정의다 |
| 소스 기반 테스트 생성 | `/backend-test` 영역 (화이트박스) |

## References

<!-- AUTO:references -->
| 파일 | 설명 |
|------|------|
| `api-layout.md` | `.api/` 산출물 레이아웃 |
| `project-detection.md` | API 프로젝트 감지 |
<!-- /AUTO:references -->

## Evals

<!-- AUTO:evals -->
<!-- /AUTO:evals -->
