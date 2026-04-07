---
title: 실시간 통신 원칙
version: 0.1.0
last_updated: 2026-04-07
---

# 실시간 통신 원칙

axum 0.8.x 내장 WebSocket(`ws::WebSocketUpgrade`)과 SSE(`Sse`)로 실시간 통신을 구현한다. 별도 외부 크레이트 없이 axum이 두 방식을 모두 제공한다.

---

## 원칙

### 1. WebSocket 핸들러는 `WebSocketUpgrade`로 업그레이드하고 `on_upgrade`로 처리한다

```rust
use axum::{
    extract::{ws::{WebSocket, WebSocketUpgrade, Message}, State},
    response::IntoResponse,
    routing::any,
    Router,
};

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/ws", any(ws_handler))  // WebSocket은 any() 권장
}

async fn ws_handler(
    ws: WebSocketUpgrade,
    State(state): State<AppState>,
) -> impl IntoResponse {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(mut socket: WebSocket, state: AppState) {
    // 송수신 분리 (split)
    let (mut sender, mut receiver) = socket.split();

    // 수신 루프
    while let Some(msg) = receiver.next().await {
        match msg {
            Ok(Message::Text(text)) => {
                // 에코
                if sender.send(Message::Text(text)).await.is_err() {
                    break;
                }
            }
            Ok(Message::Close(_)) | Err(_) => break,
            _ => {}
        }
    }
}
```

### 2. 다중 클라이언트 브로드캐스트는 `tokio::sync::broadcast`로 구현한다

```rust
use tokio::sync::broadcast;

#[derive(Clone)]
pub struct AppState {
    pub tx: broadcast::Sender<String>,
}

async fn handle_socket(mut socket: WebSocket, state: AppState) {
    let mut rx = state.tx.subscribe();
    let (mut sender, mut receiver) = socket.split();

    // 브로드캐스트 수신 → WebSocket 전송
    let mut send_task = tokio::spawn(async move {
        while let Ok(msg) = rx.recv().await {
            if sender.send(Message::Text(msg.into())).await.is_err() {
                break;
            }
        }
    });

    // WebSocket 수신 → 브로드캐스트
    let tx = state.tx.clone();
    let mut recv_task = tokio::spawn(async move {
        while let Some(Ok(Message::Text(text))) = receiver.next().await {
            let _ = tx.send(text.to_string());
        }
    });

    // 어느 쪽이 먼저 끝나도 나머지를 중단
    tokio::select! {
        _ = &mut send_task => recv_task.abort(),
        _ = &mut recv_task => send_task.abort(),
    }
}
```

### 3. SSE는 `Sse<S>`와 `Event`로 단방향 스트림을 서빙한다

```rust
use axum::response::sse::{Event, KeepAlive, Sse};
use tokio_stream::{wrappers::BroadcastStream, StreamExt};
use std::convert::Infallible;

async fn sse_handler(
    State(state): State<AppState>,
) -> Sse<impl futures::Stream<Item = Result<Event, Infallible>>> {
    let rx = state.tx.subscribe();
    let stream = BroadcastStream::new(rx)
        .filter_map(|result| result.ok())
        .map(|msg| Ok(Event::default().data(msg)));

    Sse::new(stream)
        .keep_alive(
            KeepAlive::new()
                .interval(Duration::from_secs(15))
                .text("ping"),
        )
}
```

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| WebSocket 라우트 메서드 | `any()` | GET 업그레이드 핸드셰이크 처리 |
| SSE keepalive 간격 | 15~30초 | 프록시 타임아웃 방지 |
| broadcast 채널 용량 | 100~1000 | 느린 구독자 버퍼 크기 |
| WebSocket 메시지 크기 제한 | 설정 필요 | `.max_message_size(16 * 1024)` |

---

## 안티패턴

### WebSocket 라우트에 `get()` 사용

WebSocket 업그레이드는 HTTP GET으로 시작하지만 `Router::get()`이 아닌 `Router::any()`를 사용해야 한다. `get()`은 업그레이드 응답을 올바르게 처리하지 못할 수 있다.

### SSE 스트림에 keepalive 미설정

nginx/ALB 같은 프록시는 60초 이상 응답이 없으면 연결을 끊는다. `KeepAlive`를 설정해 주기적으로 빈 이벤트를 전송한다.

### 단일 `Mutex<Vec<Sender>>`로 브로드캐스트 구현

구독자가 많을 때 Mutex 경합이 심해진다. `tokio::sync::broadcast` 채널이 내부적으로 더 효율적이다.

---

## Gotchas

### `WebSocket::split()`은 `sender`와 `receiver`를 독립적으로 움직인다

`split()` 후 sender와 receiver를 각각 별도 `tokio::spawn` 태스크로 분리하면 독립적으로 동작한다. 한쪽이 끊기면 `tokio::select!`로 다른 쪽도 중단한다.

### `broadcast::Receiver`는 느린 구독자의 메시지를 유실할 수 있다

채널이 가득 차면 오래된 메시지가 삭제된다(`RecvError::Lagged`). 수신 루프에서 `Lagged` 에러를 처리하고 클라이언트에 재연결을 안내한다.

### SSE `Event::id()`를 설정하면 클라이언트가 재연결 시 `Last-Event-ID`를 전송한다

이벤트 ID를 설정하면 브라우저가 연결 끊김 후 재연결 시 마지막 수신 ID를 헤더로 전달한다. 이를 활용해 누락된 이벤트를 재전송할 수 있다.

### `tokio-stream`의 `BroadcastStream`은 별도 의존성이다

```toml
tokio-stream = { version = "0.1", features = ["sync"] }
```
`BroadcastStream`을 사용하려면 `sync` feature를 활성화해야 한다.
