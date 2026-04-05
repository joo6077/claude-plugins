---
title: 실시간 통신
version: 0.1.0
last_updated: 2026-04-04
---

# 실시간 통신

WebSocket, SSE, long polling 선택 기준, 연결 수명 관리, 인증/인가, 수평 확장, 메시지 순서, 백프레셔를 다룬다.

---

## 원칙

### 1. 프로토콜은 상호작용 패턴에 맞게 선택한다

- **WebSocket**: full-duplex 양방향. 채팅, 게임, 협업 편집처럼 클라이언트-서버 양쪽이 자유롭게 메시지를 보내는 경우.
- **SSE(Server-Sent Events)**: 서버→클라이언트 단방향. 알림, 피드, 로그 스트리밍처럼 서버가 일방적으로 push하는 경우.
- **Long polling**: 최후 fallback. WebSocket/SSE를 지원하지 않는 환경에서만.

상호작용이 필요하면 WebSocket, 단순 피드면 SSE를 선택한다.

> **출처:** [RFC 6455 — The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455), [HTML Living Standard — Server-Sent Events](https://html.spec.whatwg.org/dev/server-sent-events.html)

### 2. WebSocket 수명 관리를 설계한다

HTTP Upgrade 핸드셰이크 이후 TCP 연결이 장시간 유지된다. heartbeat(ping/pong)로 연결 생존을 확인하고, clean close(1000 Normal Closure)로 정상 종료를 보장한다. 핸드셰이크만 하고 수명 관리를 생략하면 zombie connection이 쌓인다.

> **출처:** [RFC 6455 — The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)

### 3. SSE는 브라우저 자동 재연결 + Last-Event-ID가 장점이다

EventSource API는 연결이 끊기면 자동으로 재연결하고, `Last-Event-ID` 헤더로 마지막 수신 이벤트를 서버에 전달한다. 서버가 event ID 전략을 올바르게 구현하면 유실 없는 재개가 가능하다.

> **출처:** [HTML Living Standard — Server-Sent Events](https://html.spec.whatwg.org/dev/server-sent-events.html)

### 4. 인증은 connection 시점, 인가는 message 시점에도 계속 검증한다

연결 수립 시 토큰/쿠키로 1차 인증한다. 이후 권한 변경(역할 변경, 차단 등)이 발생할 수 있으므로, 민감한 메시지나 채널 구독 시 message-level authorization을 추가로 검증한다.

> **출처:** [ASP.NET Core SignalR — Authentication and Authorization](https://learn.microsoft.com/en-us/aspnet/core/signalr/authn-and-authz)

### 5. 연결 관리는 ping/pong + heartbeat timeout + exponential backoff + resubscribe 세트로

ping/pong으로 연결 생존 확인, heartbeat timeout 초과 시 연결 종료 판단, 재연결 시 exponential backoff로 서버 부하 방지, 재연결 후 이전 구독을 자동 복원한다. 이 중 하나라도 빠지면 불완전한 연결 관리가 된다.

> **출처:** [RFC 6455 — The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)

### 6. 수평 확장 시 프로토콜별 특성을 고려한다

Long polling은 매 요청이 다른 서버에 갈 수 있어 sticky session이 필요하다. WebSocket은 단일 TCP 연결이라 sticky에 덜 민감하지만, 다수 서버 간 메시지 전달을 위해 Redis Pub/Sub 등 브로커로 fan-out한다.

> **출처:** [Socket.IO — Using Multiple Nodes](https://socket.io/docs/v4/using-multiple-nodes/)

### 7. 메시지 순서는 연결/스트림 단위일 뿐 전체 시스템 순서가 아니다

단일 WebSocket/SSE 연결 내에서는 순서가 보장된다. 그러나 재연결, 멀티노드 fan-out, 네트워크 분할 상황에서는 전체 순서가 보장되지 않는다. 전역 순서가 필요하면 시퀀스 번호나 벡터 클럭 등 별도 메커니즘을 도입한다.

> **출처:** [RFC 6455 — The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455), [Redis — Pub/Sub](https://redis.io/docs/latest/develop/pubsub/)

### 8. 백프레셔를 명시적으로 설계한다

서버가 클라이언트보다 빠르게 메시지를 생산하면 outbound buffer가 무한 증가한다. 브라우저 WebSocket API는 백프레셔 메커니즘을 제공하지 않으므로, 서버에서 queue length 상한과 drop/throttle 정책을 구현해야 한다.

> **출처:** [MDN — WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| WS control opcode | Close 0x8, Ping 0x9, Pong 0xA |
| Control frame payload 상한 | 125 bytes |
| SSE readyState | 0=CONNECTING, 1=OPEN, 2=CLOSED |
| Socket.IO pingInterval / pingTimeout | 25s / 20s |
| Redis Pub/Sub 전달 보장 | at-most-once |
| Reconnect backoff | 시작 0.5s → max 30s |
| Heartbeat 간격 권장 | 15~30s |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 모든 실시간을 무조건 WebSocket | SSE로 충분한 단방향 피드에 불필요한 복잡도 추가. |
| Connection 인증만 하고 message authz 생략 | 권한 변경 후에도 민감 데이터를 계속 수신. |
| Long polling + 멀티노드에 sticky 없음 | 매 요청마다 세션 상태를 찾지 못해 연결 실패. |
| Redis Pub/Sub를 durable queue로 사용 | at-most-once이므로 구독자 부재 시 메시지 유실. |
| Outbound buffer 상한 없이 push | 느린 클라이언트에게 메모리가 무한 증가, OOM 발생. |

---

## Gotchas

- **SSE 자동 재연결이지만 서버 event ID 전략 없으면 복구 품질이 낮다.** 브라우저가 재연결해도 서버가 Last-Event-ID를 처리하지 않으면 유실된 이벤트를 복구할 수 없다. ID 없이 보낸 이벤트는 재개 불가.
- **WebSocket API는 백프레셔가 약하다.** `bufferedAmount` 속성으로 미전송 데이터 크기를 확인할 수 있지만 흐름 제어 메커니즘은 아니다. 서버에서 queue length 모니터링 + drop 정책을 구현해야 한다.
- **Redis Pub/Sub는 메시지 유실을 허용한다.** 구독자가 없거나 연결이 끊긴 동안의 메시지는 사라진다. 재전송이 필요한 시나리오에서는 Redis Streams나 별도 메시지 브로커(Kafka 등)를 사용해야 한다.
