---
title: 회귀 diff 실패 분류 정책
version: 0.1.0
last_updated: 2026-09-04
---

# 회귀 diff 실패 분류 정책

baseline 과 실제 응답의 차이를 어떤 실패로 부를지 결정하는 판단 규칙. 상태·스키마·값 drift 분류, 계약 실패와 환경 실패의 분리, exit code 계약, CI artifact 매핑을 다룬다.

---

## 원칙

### 1. Status Drift Classification

HTTP 상태 변화는 문자열 diff 가 아니라 상태 클래스 단위로 분류한다. `2xx/3xx/4xx/5xx` 는 의미가 다르므로 `200 -> 500` 과 `200 -> 404` 를 같은 심각도로 묶지 않는다. `200 -> 404` 는 데이터 부재일 수도, 권한 은닉일 수도 있으므로 단정하지 말고 후보 원인을 함께 기록한다.

> **출처:** [RFC 9110 Status Codes](https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes)

### 2. Schema Drift Classification

응답 본문의 구조 변화는 API 표면 변화로 본다. OpenAPI Description 은 API surface 와 semantics 를 기술하는 계약 문서이므로, 필드 추가·삭제·타입 변경 같은 schema mismatch 는 value diff 와 별도 카테고리의 계약 실패다.

> **출처:** [OpenAPI Specification v3](https://swagger.io/specification/v3/)

### 3. Value Drift Classification

상태와 스키마가 같아도 값은 달라질 수 있다. timestamp, id, 정렬 순서 같은 값 drift 는 normalize 를 먼저 적용하고, normalize 이후에도 남는 차이만 assertion failure 로 판정한다. normalize 규칙 자체가 diff 결과의 일부이므로 리포트에 함께 남긴다.

> **출처:** [Hurl Asserting Response](https://hurl.dev/docs/asserting-response.html)

### 4. Network/Auth/Data Split

연결 실패, 인증 실패, 데이터 부재를 하나의 regression 으로 묶지 않는다. Hurl 도 runtime error 와 assert error 를 별도 exit code 로 나눈다. OAuth Bearer 규격은 `invalid_token = 401`, `insufficient_scope = 403` 으로 구분하므로 인증 실패도 한 덩어리로 처리하지 않는다.

> **출처:** [Hurl Exit Codes](https://hurl.dev/docs/manual.html#exit-codes), [RFC 6750 §3.1](https://www.rfc-editor.org/rfc/rfc6750.html#section-3.1)

### 5. Exit Code Contract

CLI 종료 코드는 문서화된 계약이다. `4`(assert 실패)와 `3`(런타임 실패)이 구분되어야 CI 가 "계약이 깨졌다" 와 "서버가 죽었다" 를 다르게 다룰 수 있다. `/api-verify` 는 Hurl 의 코드 체계를 그대로 승계하고 임의로 재매핑하지 않는다.

> **출처:** [Hurl Exit Codes](https://hurl.dev/docs/manual.html#exit-codes)

### 6. Mode-aware Severity

같은 실패라도 모드에 따라 게이트 파괴 여부가 다르다. 새로 만든 계약이나 관찰(observe) 모드는 실패를 기록하되 게이트를 깨지 않고, accepted baseline 이 존재하는 계약의 실패는 회귀로 게이트를 깬다. Pact pending pacts 의 "첫 성공 전은 pending, 성공 후 실패는 breaking" 모델을 따른다.

> **출처:** [Pact Pending Pacts](https://docs.pact.io/pact_broker/advanced_topics/pending_pacts)

### 7. Retry Confirmation

retry 로 성공한 실패를 green 으로 숨기지 않는다. 동일 커밋·동일 입력에서 pass/fail 이 뒤집히는 테스트는 flaky 이며, retry 성공은 "안정"이 아니라 "불안정 신호"로 분류해 별도 카운터에 남긴다.

> **출처:** [Google Testing Blog — Where Do Our Flaky Tests Come From?](https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html)

### 8. CI Artifact Shape

JUnit XML 로 내보낼 때 계약 assertion mismatch 는 `failure`, 실행 불능·환경 오류는 `error`, quarantine 또는 의도된 미실행은 `skipped` 로 기록한다. CI 대시보드는 이 구조로 실패 원인을 집계하므로 전부 `failure` 로 밀어 넣으면 집계가 무의미해진다.

> **출처:** [JUnit XML 포맷 레퍼런스](https://github.com/testmoapp/junitxml), [Ant JUnit XMLConstants](https://svn.apache.org/repos/asf/ant/site/ant/production/manual-1.9.x/api/org/apache/tools/ant/taskdefs/optional/junit/XMLConstants.html)

### 9. Baseline Promotion Gate

diff 가 실패한 순간 baseline 을 자동 갱신하지 않는다. Jest snapshot 관례처럼 baseline 은 코드와 함께 리뷰되며, CI 는 암묵적으로 새 스냅샷을 쓰지 않는 것이 기본값이다. 갱신은 별도 promote 명령의 책임이다.

> **출처:** [Jest Snapshot Testing](https://github.com/jestjs/jest/blob/main/docs/SnapshotTesting.md)

---

## 수치 기준

### Hurl exit code 규약 (`/api-verify` 계약)

| Exit code | 의미 | 분류 | CI 처리 |
|-----------|------|------|---------|
| `0` | 성공 | — | pass |
| `1` | CLI 옵션 파싱 오류 | 도구 사용 오류 | 실행 중단, 재시도 금지 |
| `2` | 입력(.hurl) 파싱 오류 | 계약 파일 오류 | 실행 중단, 계약 파일 수정 |
| `3` | 런타임 오류 (DNS/TLS/connect/timeout) | 환경 실패 | 계약 판정 보류, `error` 로 기록 |
| `4` | assert 실패 | 계약 실패 | 게이트 파괴, `failure` 로 기록 |

> **근거:** [Hurl Exit Codes](https://hurl.dev/docs/manual.html#exit-codes)

### 기타 임계값

| 항목 | 값 | 근거 |
|------|-----|------|
| HTTP 상태 코드 유효 범위 | `100..599`, 클래스는 첫 자리로 결정 | [RFC 9110 Status Codes](https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes) |
| Bearer auth 분류 | malformed `400` / invalid·expired token `401` / insufficient scope `403` | [RFC 6750 §3.1](https://www.rfc-editor.org/rfc/rfc6750.html#section-3.1) |
| JUnit XML 결과 매핑 | 통과는 result child 없음, 실패는 `failure` / `error` / `skipped` 중 하나 | [JUnit XML 레퍼런스](https://github.com/testmoapp/junitxml) |
| retry 확인 횟수 | `initial + 1 replay` (동일 커밋·동일 입력) | 추론 |
| flaky 판정 | 재실행에서 결과가 뒤집히면 `flaky-confirmed`, 계속 실패면 원 분류 유지 | 추론 |
| CI 에서 baseline 자동 write 허용 횟수 | `0` — 명시적 promote 명령 + 리뷰 메타데이터가 있을 때만 | 추론 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 모든 차이를 `diff failed` 한 줄로 출력 | 상태·스키마·값 중 무엇이 깨졌는지 알 수 없어 대응 우선순위를 못 정한다 |
| `401/403/404` 를 무조건 API regression 으로 처리 | 만료된 토큰이나 정상적인 데이터 부재가 계약 위반으로 둔갑해 게이트가 노이즈로 채워진다 |
| retry 성공 시 실패 기록 삭제 | flaky 신호가 사라져 같은 불안정이 무한 반복된다 |
| CI 실패 시 baseline 자동 갱신 | 회귀가 새 truth 로 승격되어 다음 실행부터 green 이 된다 |
| JUnit XML 에서 런타임·인프라 오류를 `failure` 로 기록 | 서버 다운과 계약 파손이 같은 통계로 합쳐져 원인 분석이 불가능해진다 |

---

## Gotchas

- **Hurl `3`(runtime error)은 DNS/TLS/timeout/connect 를 모두 포함한다** — exit code 만으로는 "네트워크가 끊겼다" 이상을 알 수 없으므로, 리포트에 내부 subreason 을 별도 필드로 남긴다. 그렇지 않으면 일시적 타임아웃과 인증서 만료가 구분되지 않는다.
- **additive field 는 모드에 따라 판정이 뒤집힌다** — tolerant 모드에서는 호환이지만 exact·golden 모드에서는 실패다. diff 결과를 읽을 때 반드시 어떤 모드로 실행했는지 함께 봐야 한다.
- **`404` 는 원인이 둘이다** — 진짜 데이터 부재일 수도, 존재를 감추는 `403` 대체 정책일 수도 있다. 자동으로 한쪽으로 단정하지 말고 두 후보를 모두 리포트에 남긴다.
- **실패 artifact 에는 stdout 과 raw body 가 들어간다** — 리포트를 생성하기 전에 redaction 을 먼저 수행한다. 리포트 생성 후 마스킹하면 이미 파일·CI 로그에 비밀이 남는다.
