---
title: gRPC
version: 0.1.0
last_updated: 2026-04-04
---

# gRPC

Proto 계약, RPC 타입 선택, deadline 전파, metadata, 구조화 에러, 헬스체크, 로드밸런싱, TLS, 호환성 규칙을 다룬다.

---

## 원칙

### 1. .proto는 네트워크 계약이다

.proto 파일은 서비스 간 통신 계약이지 저장 스키마가 아니다. DB 테이블 구조와 1:1로 매핑하지 않는다. field number는 wire format의 영구 식별자이므로 한번 할당하면 절대 변경하거나 재사용하지 않는다.

> **출처:** [Protocol Buffers — Dos and Don'ts](https://protobuf.dev/best-practices/dos-donts/)

### 2. Unary RPC를 기본으로 하고 streaming은 진짜 필요할 때만

4가지 RPC 타입(unary, server streaming, client streaming, bidirectional) 중 unary가 가장 단순하고 디버깅이 쉽다. 데이터가 incremental하게 생성되거나 interactive 응답이 필요할 때만 streaming을 선택한다. streaming은 연결 관리, 에러 처리, 로드밸런싱 모두 복잡해진다.

> **출처:** [gRPC — Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)

### 3. Deadline은 클라이언트가 명시하고 서버가 전파한다

클라이언트가 RPC마다 deadline을 설정하고, 서버는 남은 시간을 조회하여 하위 RPC에 전파한다. deadline 없는 RPC는 서버 리소스를 무한히 점유할 수 있다. 전체 call chain에서 deadline이 줄어드는 방향으로만 흘러야 한다.

> **출처:** [gRPC — Deadlines](https://grpc.io/docs/guides/deadlines/)

### 4. Metadata는 사이드채널 용도로만 사용한다

인증 토큰, 트레이싱 ID, 정책 힌트 등 횡단 관심사를 metadata에 담는다. 비즈니스 payload를 metadata에 넣으면 크기 제한에 걸리고, 타입 안전성이 없으며, 디버깅이 어렵다.

> **출처:** [gRPC — Metadata](https://grpc.io/docs/guides/metadata/)

### 5. 에러는 google.rpc.Status + details로 구조화한다

status code만으로 부족한 정보를 `google.rpc.Status`의 details 필드에 담는다. 재시도 가능성(`RetryInfo`), 지역화된 메시지(`LocalizedMessage`), 필드별 위반(`BadRequest.FieldViolation`)을 구조화하여 클라이언트가 프로그래밍적으로 에러를 처리할 수 있게 한다.

> **출처:** [Google Cloud API Design — Errors](https://cloud.google.com/apis/design/errors)

### 6. grpc.health.v1 헬스체크를 구현한다

표준 Health 서비스를 구현하여 로드밸런서와 오케스트레이터가 서비스 상태를 확인할 수 있게 한다. `Watch` RPC를 지원하면 상태 변화를 스트리밍으로 감지할 수 있다.

> **출처:** [gRPC — Health Checking](https://grpc.io/docs/guides/health-checking/)

### 7. 로드밸런싱 전략은 환경에 맞게 선택한다

신뢰할 수 있는 내부 네트워크에서는 client-side LB(pick_first, round_robin, xDS)가 효율적이다. internet-facing 서비스에서는 proxy/L7 LB(Envoy, nginx 등)를 사용한다. HTTP/2의 단일 TCP 연결 특성상 L4 LB만으로는 요청이 균등 분배되지 않는다.

> **출처:** [gRPC — Load Balancing](https://grpc.io/blog/grpc-load-balancing/)

### 8. TLS를 기본으로 하고 zero-trust에서는 mTLS를 우선한다

gRPC 채널은 기본적으로 TLS로 암호화한다. 서비스 메시 환경이나 zero-trust 아키텍처에서는 양방향 인증(mTLS)으로 클라이언트 신원까지 검증한다.

> **출처:** [gRPC — Authentication](https://grpc.io/docs/guides/auth/)

### 9. 하위 호환성: 번호 재사용 금지, 삭제 필드 reserve, wire 의미 유지

field number를 삭제 후 재사용하면 이전 클라이언트가 다른 타입의 데이터를 파싱하여 silent corruption이 발생한다. 삭제하는 필드는 `reserved`로 선언하여 미래 재사용을 방지한다. 필드의 wire 의미(타입, 시맨틱)를 변경하지 않는다.

> **출처:** [Protocol Buffers — Dos and Don'ts](https://protobuf.dev/best-practices/dos-donts/)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| Field number 범위 | 1~536,870,911 (19000~19999 예약) |
| RPC 타입 | 4가지 (unary, server streaming, client streaming, bidirectional) |
| Metadata 권고 크기 | 기본 8 KiB |
| Retry maxAttempts 상한 | 5 (초과 시 5로 제한) |
| Retry throttling 예시 | maxTokens: 10, tokenRatio: 0.1 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 삭제한 field의 같은 tag number 재사용 | 이전 클라이언트가 다른 타입으로 파싱, silent data corruption. |
| Unary로 충분한 걸 streaming으로 구현 | 연결 관리, 에러 처리, LB 복잡도가 불필요하게 증가. |
| Deadline 없는 내부 fan-out | 하위 서비스 장애 시 상위 서비스 리소스 누수, cascading failure. |
| Metadata에 대용량 데이터 | 크기 제한 초과, 타입 안전성 없음, 프록시에서 잘릴 수 있음. |
| UNKNOWN/INTERNAL만 남발 | 클라이언트가 에러 원인을 알 수 없어 복구 로직 구현 불가. |

---

## Gotchas

- **DEADLINE_EXCEEDED는 서버 작업 완료 여부와 무관하다.** 서버가 이미 작업을 완료했어도 응답이 deadline 안에 도착하지 않으면 클라이언트는 실패로 본다. 부수 효과가 있는 RPC는 멱등성 설계가 필수이다.
- **Transparent retry로 앱이 명시하지 않은 재시도가 발생할 수 있다.** gRPC 런타임이 특정 조건(stream not yet written, GOAWAY 등)에서 자동 재시도한다. 비멱등 RPC에서 예상치 못한 중복 실행을 유발할 수 있다.
- **pick_first는 사실상 로드밸런싱이 아니다.** 이름 그대로 첫 번째 주소에만 연결한다. 여러 서버 인스턴스가 있어도 하나에만 트래픽이 몰린다. 명시적으로 round_robin 이상의 정책을 설정해야 한다.
