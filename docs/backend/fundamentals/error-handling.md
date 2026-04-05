---
title: 에러 처리
version: 0.1.0
last_updated: 2026-04-04
---

# 에러 처리

Result/Either 패턴, 글로벌 에러 핸들러, 에러 분류 체계, retry 전략, circuit breaker, graceful degradation, 구조화 로깅을 다룬다.

---

## 원칙

### 1. 복구 가능 에러와 불가능 에러를 구분하고 다르게 처리한다

- **복구 가능(recoverable)**: 네트워크 타임아웃, 일시적 DB 장애, 잘못된 사용자 입력. 재시도하거나 사용자에게 안내한다.
- **복구 불가능(unrecoverable)**: 메모리 부족, 설정 파일 누락, 스키마 불일치. 프로세스를 종료하고 운영팀에 알린다.

복구 가능 에러에 `panic`/`process.exit`을 쓰면 서비스 가용성이 떨어지고, 복구 불가능 에러를 삼키면(catch-all 무시) 데이터 손상으로 이어진다.

> **출처:** [The Rust Programming Language — Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

### 2. Result/Either 타입으로 에러를 값으로 다룬다

예외(exception)는 제어 흐름을 비선형으로 만들고, 어떤 함수가 어떤 예외를 던지는지 시그니처에서 알 수 없다(Java checked exception 제외). Result/Either 패턴은 성공과 실패를 하나의 타입으로 표현하여 컴파일러가 에러 처리를 강제한다.

```
Result<User, DbError>   -- Rust
Either<Failure, User>    -- Dart/fp
Result<User, AppError>   -- Kotlin
```

핵심 규칙:
- 함수 경계에서 에러를 변환한다. 인프라 에러(SqlException)를 도메인 에러(UserNotFound)로.
- `unwrap()`/`get()`은 테스트 코드에서만 사용한다. 프로덕션에서는 항상 분기 처리한다.
- 예외는 진짜 예외적인 상황(프로그래머 실수, 불변 조건 위반)에만 사용한다.

> **출처:** [Rust std::result](https://doc.rust-lang.org/std/result/)

### 3. 글로벌 에러 핸들러로 일관된 에러 응답을 보장한다

개별 엔드포인트에서 에러 포맷을 만들지 않는다. 프레임워크의 에러 핸들러 미들웨어에서 모든 에러를 RFC 9457 `application/problem+json`으로 변환한다.

```
[Controller] --throws DomainError--> [Global Error Handler] --returns--> problem+json
```

글로벌 핸들러의 책임:
- 도메인 에러 → 적절한 HTTP 상태 코드 매핑
- 예상치 못한 에러 → 500 + 내부 상세는 로그에만 기록 (클라이언트에 스택트레이스 노출 금지)
- 상관 ID(correlation ID)를 응답과 로그에 포함

> **출처:** [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)

### 4. Retry는 exponential backoff + jitter를 적용한다

일시적 장애(네트워크 불안정, 429 Too Many Requests)에 대해 재시도한다. 고정 간격 재시도는 장애 서버에 동시 요청 폭주(thundering herd)를 유발한다.

```
sleep = min(base * 2^attempt + random_jitter, max_interval)
```

| 파라미터 | 권장값 |
|---------|--------|
| base interval | 1초 |
| max attempts | 5회 |
| max interval | 32초 |
| jitter | `[0, base * 2^attempt)` 범위의 균등 분포 |

재시도 대상: 5xx, 429, 네트워크 에러, DNS 실패. 재시도 금지: 4xx(400, 401, 403, 404 — 재시도해도 결과 동일), 비멱등 요청(POST)은 멱등 키(idempotency key) 없이 재시도 금지.

> **출처:** [AWS Architecture Blog — Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)

### 5. Circuit breaker로 cascading failure를 방지한다

외부 서비스 호출 실패가 반복되면 요청을 차단하여 자기 서비스와 의존 서비스를 보호한다.

```
[Closed] --failure rate >= threshold--> [Open] --timeout--> [Half-Open]
   ^                                                             |
   |______________ success count >= threshold __________________|
```

| 상태 | 동작 |
|------|------|
| **Closed** | 정상. 모든 요청을 통과시키고 실패율을 모니터링. |
| **Open** | 차단. 즉시 fallback 반환. 설정된 timeout 후 Half-Open 전환. |
| **Half-Open** | 제한된 요청(3~5개)만 통과. 성공하면 Closed, 실패하면 다시 Open. |

권장 설정: failure rate threshold 50%, sliding window 10초, Half-Open 시도 횟수 3~5회.

> **출처:** [Microsoft — Circuit Breaker Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

### 6. Graceful degradation: 핵심 기능은 유지, 부가 기능은 fallback한다

추천 서비스가 죽어도 상품 목록은 보여야 한다. 알림 서비스가 느려도 주문은 완료되어야 한다. Bulkhead 패턴으로 서비스 간 장애를 격리한다.

구현 방법:
- **Bulkhead**: 서비스별 스레드 풀/커넥션 풀 분리. 하나가 고갈되어도 다른 서비스에 영향 없음.
- **Timeout**: 모든 외부 호출에 timeout 설정. 무한 대기는 리소스 고갈의 시작.
- **Fallback**: 캐시된 결과 반환, 기본값 사용, 기능 비활성화 + 사용자 안내.

> **출처:** [Microsoft — Bulkhead Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead)

### 7. 에러 로그는 구조화(JSON) + 상관 ID를 포함한다

텍스트 로그(`ERROR: something went wrong`)는 grep으로 분석이 어렵다. 구조화 로그(JSON)로 작성하고, 모든 요청에 상관 ID를 부여하여 분산 시스템에서 요청 흐름을 추적한다.

```json
{
  "timestamp": "2026-04-04T10:30:00Z",
  "level": "ERROR",
  "correlation_id": "req-abc-123",
  "service": "order-service",
  "error_type": "PaymentGatewayTimeout",
  "message": "Payment gateway responded in 5200ms (timeout: 5000ms)",
  "attempt": 3,
  "user_id": "usr-456"
}
```

로그에 포함하면 안 되는 것: 비밀번호, 카드 번호, 주민번호 등 PII. 마스킹(`****`)하거나 로그 레벨로 분리한다.

> **출처:** [Elastic Common Schema](https://www.elastic.co/guide/en/ecs/current/)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| Retry base interval | 1초 |
| Retry max attempts | 5회 |
| Retry max interval | 32초 |
| Circuit breaker failure rate threshold | 50% |
| Circuit breaker sliding window | 10초 |
| Half-Open 시도 횟수 | 3~5회 |
| 외부 호출 timeout 기본값 | 5초 (서비스 특성에 따라 조정) |
| Bulkhead 스레드 풀 크기 | 서비스별 10~20 (부하 테스트로 조정) |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 모든 에러 500 반환 | 클라이언트가 복구 가능 에러와 서버 에러를 구분할 수 없다. |
| catch-all 무시 (`catch(e) {}`) | 에러가 사라져서 디버깅 불가. 데이터 불일치 원인이 된다. |
| Retry 무한 루프 | max attempts 없이 재시도하면 장애 서비스에 부하를 가중시킨다. |
| Circuit breaker 없는 외부 호출 | 외부 서비스 장애가 자기 서비스로 전파된다 (cascading failure). |

---

## Gotchas

- **Jitter 없는 backoff는 thundering herd를 유발한다.** 100개 클라이언트가 동시에 실패하면, exponential backoff만으로는 모두 같은 시간에 재시도한다(1s, 2s, 4s, 8s...). jitter를 추가해야 재시도 시점이 분산된다.
- **Circuit breaker 상태를 인스턴스별로 관리하면 불일치가 발생한다.** 인스턴스 A는 Open인데 인스턴스 B는 Closed일 수 있다. 이것이 문제인지 기능인지는 아키텍처에 따라 다르다. 엄격한 일관성이 필요하면 중앙 저장소(Redis)에 상태를 공유한다.
- **에러 로그에 PII를 포함하면 규정 위반이 된다.** GDPR, 개인정보보호법에 의해 로그에 개인 식별 정보가 포함되면 로그 보존 정책, 접근 통제, 삭제 요청 처리 의무가 발생한다. 로그에는 사용자 ID(내부 식별자)만 포함하고, 이름/이메일/전화번호는 마스킹하거나 제외한다.
