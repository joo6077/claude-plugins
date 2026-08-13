---
title: 이벤트 기반 아키텍처
version: 0.2.0
last_updated: 2026-08-13
---

# 이벤트 기반 아키텍처

메시지 큐 vs 이벤트 스트리밍, outbox 패턴, saga, 전달 보장(exactly-once/at-least-once), DLQ, idempotency, CQRS, 이벤트 소싱, 스키마 진화를 다룬다.

---

## 원칙

### 1. 큐와 스트리밍은 용도가 다르다

**메시지 큐(RabbitMQ, SQS)**는 작업 분배(work distribution)에 적합하다. 메시지가 한 consumer에게 전달되면 큐에서 제거된다. **이벤트 스트리밍(Kafka)**은 이벤트 로그(event log)다. 메시지가 retention 기간 동안 보존되며 여러 consumer group이 독립적으로 읽는다. 단일 consumer 작업 분배에는 큐, 다중 consumer 이벤트 브로드캐스트에는 스트리밍을 선택한다.

> **출처:** [Apache Kafka Documentation](https://kafka.apache.org/documentation/), [RabbitMQ Tutorials](https://www.rabbitmq.com/docs/tutorials)

### 2. Outbox 패턴으로 이중쓰기를 방지한다

DB 저장과 메시지 발행을 별도로 수행하면 하나만 성공하는 이중쓰기(dual write) 문제가 발생한다. Outbox 패턴은 비즈니스 데이터와 이벤트를 같은 DB 트랜잭션으로 outbox 테이블에 저장하고, 별도 프로세스(Debezium CDC 또는 폴링)가 outbox를 읽어 메시지 브로커에 발행한다. 원자성이 보장된다.

> **출처:** [Microservices.io — Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html)

### 3. Saga로 분산 트랜잭션을 관리한다

마이크로서비스 간 ACID 트랜잭션은 불가능하다. Saga는 로컬 트랜잭션의 연쇄로 분산 트랜잭션을 구현한다. **Choreography**: 각 서비스가 이벤트를 발행하고 다음 서비스가 반응한다. 단순한 흐름(2~3단계)에 적합. **Orchestration**: 중앙 조정자(orchestrator)가 각 서비스에 명령을 보낸다. 복잡한 흐름(4단계 이상)에 적합. 실패 시 보상 트랜잭션(compensating transaction)으로 롤백한다.

> **출처:** [Microservices.io — Saga Pattern](https://microservices.io/patterns/data/saga.html)

### 4. Exactly-once는 대부분 환상이다

네트워크 분할, 프로세스 크래시가 발생하면 메시지가 중복 전달되거나 유실될 수 있다. 실용적인 접근은 **at-least-once 전달 + consumer 측 idempotency**다. Kafka는 idempotent producer + transactional consumer로 "effectively exactly-once"를 제공하지만, 이는 Kafka 내부에서만 보장되며 외부 시스템(DB, API 호출)까지 포함하면 idempotency가 별도로 필요하다.

> **출처:** [Apache Kafka — Message Delivery Semantics](https://kafka.apache.org/documentation/#semantics)

### 5. DLQ로 실패 메시지를 격리한다

처리 실패한 메시지를 무한 재시도하면 consumer가 차단된다. Dead Letter Queue(DLQ)에 실패 메시지를 격리하고, 정상 메시지 처리를 계속한다. DLQ의 메시지는 수동 검토 후 원인을 수정하고 재처리한다. `maxReceiveCount`(SQS 기준 보통 3~5회)를 설정하여 재시도 횟수를 제한한다.

> **출처:** [AWS — SQS Dead-Letter Queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)

### 6. Idempotency key로 중복 처리를 방지한다

at-least-once 환경에서 같은 메시지가 2번 이상 도착할 수 있다. 각 메시지에 고유한 idempotency key를 부여하고, 처리 전 이미 처리된 key인지 확인한다. **키만으로는 부족하다** — 같은 키에 다른 페이로드가 온 경우를 구분해야 하므로 payload fingerprint 를 함께 저장한다. Stripe API가 대표적 구현 — 클라이언트가 `Idempotency-Key` 헤더를 전송하면 서버가 결과를 저장했다가 재요청 시 재생하고, **요청 페이로드를 비교**하며, 키 레코드는 24시간 후 정리(pruning)된다. 즉 24시간은 "응답 보장 기간" 이 아니라 **키 보관 기간**이며, 만료 후 같은 키가 오면 새 요청으로 처리된다. [정정 2026-08-13] 이전 서술은 payload 비교와 만료 시맨틱을 빠뜨린 채 24시간을 "응답 보장 기간" 처럼 읽히게 해 오해를 유발했다.

> **출처:** [Stripe — Idempotent requests](https://docs.stripe.com/api/idempotent_requests)

### 7. CQRS로 읽기/쓰기 모델을 분리한다

Command Query Responsibility Segregation은 쓰기 모델(command)과 읽기 모델(query)을 분리한다. 쓰기는 정규화된 도메인 모델, 읽기는 비정규화된 뷰 모델을 사용한다. 이벤트 소싱(Event Sourcing)과 자주 결합되지만 독립 적용도 가능하다. 읽기/쓰기 비율이 극단적으로 다른 시스템(예: 읽기 90% 이상)에서 효과적이다. 단순한 CRUD에는 과도한 복잡성이다.

> **출처:** [Microsoft — CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| Kafka 기본 retention | 7일 (168시간) | `log.retention.hours`로 설정 |
| Kafka consumer group rebalance timeout | 300초 (5분) | `max.poll.interval.ms` 기본값 |
| SQS 메시지 보존 | 기본 4일, 최대 14일 | `MessageRetentionPeriod` |
| SQS DLQ maxReceiveCount | 3~5회 | 초과 시 DLQ로 이동 |
| Idempotency key 보존 기간 | 24~48시간 | Stripe는 24시간 |
| Kafka 파티션당 권장 consumer | 1개 | consumer > partition이면 유휴 consumer 발생 |
| Outbox 폴링 간격 | 100ms~1초 | CDC(Debezium) 사용 시 실시간에 가까움 |

---

## 안티패턴

### 동기 호출을 이벤트로 과도하게 변환

단순 요청-응답이 적합한 동기 호출까지 이벤트로 바꾸면 디버깅이 어려워지고 지연이 증가한다. 이벤트는 느슨한 결합이 필요한 곳에만 사용한다.

### Idempotency 없는 at-least-once

중복 메시지를 처리하지 않으면 결제 2회 실행, 이메일 중복 발송 등의 문제가 발생한다. 모든 consumer는 idempotency key 검증을 구현한다.

### Outbox 없는 이중쓰기

DB 저장 후 메시지 발행이 실패하면 데이터 불일치가 발생한다. 반대로 메시지 발행 후 DB 저장이 실패해도 불일치다. outbox 패턴이나 CDC로 원자성을 보장한다.

### 모든 것에 CQRS

단순 CRUD 시스템에 CQRS를 적용하면 코드량이 2배 이상 증가하고 eventual consistency 관리 부담이 생긴다. 읽기/쓰기 요구사항이 명확히 다를 때만 도입한다.

---

## Gotchas

- **Kafka consumer offset 관리 실수로 메시지 유실/중복** — `enable.auto.commit=true`(기본값)에서 처리 전 commit되면 유실, 처리 후 commit 전 크래시하면 중복. 수동 commit(`enable.auto.commit=false`)으로 전환하고 처리 완료 후 명시적으로 commit한다
- **Saga 보상 트랜잭션 실패 시 수동 개입 필요** — 보상 트랜잭션도 실패할 수 있다(외부 API 장애 등). 보상 실패를 감지하는 모니터링과 수동 개입 프로세스를 반드시 준비한다
- **이벤트 스키마 변경은 모든 consumer에 영향** — 필드 추가는 하위 호환되지만, 필드 제거나 타입 변경은 기존 consumer를 깨뜨린다. Avro + Schema Registry로 스키마 진화를 관리하고, backward/forward compatibility를 검증한다
