---
title: 비동기 패턴
version: 0.1.0
last_updated: 2026-04-05
---

# 비동기 패턴

## 요약

`Future` vs `Stream` 선택 기준, `FutureBuilder`/`StreamBuilder` vs `AsyncValue`, Isolate/`compute`, 취소 패턴.

## 원칙

1. **단발성 결과는 `Future`, 지속적 이벤트 스트림은 `Stream`을 쓴다.** 한 번만 받아올 데이터를 Stream으로 감싸지 않는다.
   - 출처: https://dart.dev/language/concurrency

2. **단순 async 렌더링은 `FutureBuilder` / `StreamBuilder`, 앱 상태와 결합되는 경우에는 `AsyncValue` 같은 상위 abstraction을 쓴다.** 화면 상태가 provider와 섞이는 순간 Builder류는 한계가 온다.
   - 출처: https://pub.dev/packages/flutter_riverpod

3. **async 오류는 `try`/`catch`로 처리하고, sync/async 오류를 동일하게 다루려면 `Future.sync`로 감싼다.**
   - 출처: https://dart.dev/libraries/async/futures-error-handling

4. **한 프레임(~16ms)을 넘길 계산은 isolate로 옮긴다.** JSON 대량 파싱은 `compute`가 기본.
   - 출처: https://docs.flutter.dev/cookbook/networking/background-parsing

5. **취소는 `Future` 자체가 아니라 Dio의 `CancelToken`, Stream subscription cancel, provider dispose로 구현한다.** Dart `Future`는 표준 cancel API가 없다.
   - 출처: https://pub.dev/documentation/dio/latest/dio/CancelToken-class.html

## 수치 기준

- Flutter UI 프레임 예산은 약 16ms — 이 시간을 넘기는 동기 계산은 jank를 유발한다.
- `compute`에 넘기는 메시지는 primitive/단순 객체여야 한다. `Future`, `http.Response`, closure 등은 전달 불가.

## 안티패턴

- `FutureBuilder(future: apiCall())`처럼 `build`마다 새 Future를 생성 — 매 rebuild마다 API 재호출.
- 1회성 조회인데 `Stream.fromFuture`로 감싸 `StreamBuilder`에 물리는 구조.
- 작은 JSON 한 건도 `compute`로 보내 isolate spawn 비용이 이득을 넘김.
- 화면 pop/dispose 시 in-flight 요청을 취소하지 않고 결과가 돌아오면 state를 그대로 반영.

## Gotchas

- Flutter **web**은 isolate 제약이 있다 (`dart:isolate`가 사실상 사용 불가). `compute`는 web에서 main isolate에서 동작한다고 가정하고 설계하라.
- 테스트에서 `pumpAndSettle`로 "모든 async를 기다린다"는 멘탈 모델은 끊임없이 흐르는 `Stream`이나 무한 animation과 만나면 timeout을 일으킨다. 해당 화면은 `pump(duration)`으로 명시적 제어해야 한다.
