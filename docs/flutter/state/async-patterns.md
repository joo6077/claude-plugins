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

## 실전 패턴

### FutureBuilder 올바른 사용

```dart
class MyWidget extends StatefulWidget { ... }
class _MyWidgetState extends State<MyWidget> {
  late final Future<Data> _future;

  @override
  void initState() {
    super.initState();
    _future = fetchData(); // initState에서 한 번만 생성
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Data>(
      future: _future, // build에서 재생성하지 않음
      builder: (context, snapshot) => switch (snapshot) {
        AsyncSnapshot(hasData: true, :final data!) => DataWidget(data),
        AsyncSnapshot(hasError: true, :final error!) => ErrorWidget(error),
        _ => const LoadingWidget(),
      },
    );
  }
}
```

- 출처: https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html

### Isolate 통신 패턴 (Flutter 3.19+)

`Isolate.run`은 단발성 작업에 적합. 지속적 작업은 `Isolate.spawn` + `ReceivePort`/`SendPort`:

```dart
final result = await Isolate.run(() {
  // heavy computation here
  return jsonDecode(hugeJsonString) as Map<String, dynamic>;
});
```

- 출처: https://dart.dev/language/isolates

### 취소 패턴 비교

| 접근법 | 사용 시점 |
|--------|----------|
| `CancelToken` (Dio) | HTTP 요청 취소 — 화면 pop 시 |
| `StreamSubscription.cancel()` | Stream 구독 해제 |
| `ref.onDispose(() => ...)` | Riverpod provider dispose 시 cleanup |
| `useEffect` return | Hook 위젯 unmount 시 자동 cleanup |

### Debounce + Cancel 조합

검색 입력처럼 rapid-fire 요청이 발생하는 경우:
1. Timer로 debounce (300ms)
2. 이전 요청의 CancelToken을 cancel
3. 새 요청 발생

이 패턴은 `useDebounce` 커스텀 훅 + `ref.onDispose`로 구현한다.

## 테스트 전략

- `FutureBuilder` 테스트: `tester.pump()` 1회 → loading 확인, `tester.pumpAndSettle()` → data/error 확인
- Mock을 `Future.delayed(Duration(milliseconds: 100), () => data)`로 만들어 loading 상태 확인 가능
- `compute` 테스트: 실제 isolate spawn이 일어나므로 integration test에서 검증
- 출처: https://docs.flutter.dev/cookbook/testing

## Gotchas

- Flutter **web**은 isolate 제약이 있다 (`dart:isolate`가 사실상 사용 불가). `compute`는 web에서 main isolate에서 동작한다고 가정하고 설계하라.
- 테스트에서 `pumpAndSettle`로 "모든 async를 기다린다"는 멘탈 모델은 끊임없이 흐르는 `Stream`이나 무한 animation과 만나면 timeout을 일으킨다. 해당 화면은 `pump(duration)`으로 명시적 제어해야 한다.
- `async*` generator로 만든 Stream은 listener가 없으면 아예 실행되지 않는다 — 구독 전에 yield가 실행될 거라고 가정하면 안 된다.
- `Future.wait`은 하나라도 실패하면 전체가 실패한다 — 부분 성공이 필요하면 각 Future를 `Result`로 감싸서 `Future.wait`에 넘겨라.
