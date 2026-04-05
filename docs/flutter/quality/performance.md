---
title: 성능
version: 0.1.0
last_updated: 2026-04-05
---

# 성능

## 요약

Flutter 성능 최적화는 rebuild 최소화, `const` 적극 사용, `RepaintBoundary`로 repaint hotspot 격리, `AutomaticKeepAlive`로 스크롤 캐시 관리, `ListView.builder`로 lazy 렌더, 이미지 캐시 관리, DevTools Performance view로 병목 측정, 무거운 CPU 작업은 isolate로 분리하는 원칙으로 요약된다. 모든 최적화는 frame budget 안에서 build + render를 끝내는 것을 목표로 한다.

## 원칙

### 1. Profiler-first — 측정 후 최적화

DevTools Performance view와 "Track widget rebuilds", "Highlight repaints" 옵션으로 실제 병목을 먼저 식별한다. 직감에 기반한 최적화는 대체로 무효하거나 역효과를 낸다.

출처: https://docs.flutter.dev/perf/best-practices

### 2. Build 비용을 작게 유지

`build` 메서드는 자주 호출된다. 비싼 계산, 객체 생성, 리스트 필터링을 `build` 안에 두지 말고 `initState` / Notifier / memoization으로 밖으로 빼라. 변하지 않는 서브트리는 `const`로 만들어 재사용되도록 한다.

출처: https://docs.flutter.dev/perf/best-practices

### 3. 긴 리스트는 `ListView.builder`

아이템 수가 많거나 길이가 불확정인 리스트는 반드시 `ListView.builder` (또는 `.separated` / `.custom`)로 lazy 빌드한다. `ListView(children: [...])`는 모든 아이템을 미리 빌드하므로 메모리와 프레임을 동시에 낭비한다.

출처: https://api.flutter.dev/flutter/widgets/ListView/ListView.builder.html

### 4. Repaint 격리와 keep-alive는 선별 적용

잦은 repaint가 일어나는 서브트리는 `RepaintBoundary`로 감싸 주변 트리의 재페인트를 막는다. 스크롤 아이템 상태를 유지해야 할 때만 `AutomaticKeepAliveClientMixin`을 적용한다. 둘 다 비용이 있으므로 무조건 씌우면 오히려 메모리와 layer 비용이 증가한다.

출처: https://api.flutter.dev/flutter/widgets/RepaintBoundary-class.html , https://api.flutter.dev/flutter/widgets/AutomaticKeepAliveClientMixin-mixin.html

### 5. 무거운 CPU 작업은 isolate로

대용량 JSON 파싱, 이미지 디코딩, 암호 연산 같은 CPU bound 작업은 메인 isolate(UI thread)를 막는다. `compute()` 또는 `Isolate.run`으로 별도 isolate에 넘겨 UI 프레임을 보호한다.

출처: https://docs.flutter.dev/perf/isolates

## 수치

| 항목 | 값 |
|------|-----|
| 60Hz frame budget | 16ms (build ~8ms + render ~8ms 목표) |
| 120Hz frame budget | 8ms 이하 (고주사율 디바이스) |
| 기본 `ImageCache` 최대 엔트리 | 1000장 |
| 기본 `ImageCache` 최대 바이트 | 약 100MB (LRU) |

## 안티패턴

- 크고 정적인 리스트를 `ListView(children: [...])`로 한 번에 전개한다. 스크롤 바깥의 아이템까지 모두 빌드되어 초기 프레임이 무거워진다.
- 애니메이션 진행 중 `Opacity`, `ClipRect`, `ShaderMask`, `saveLayer`를 남용한다. offscreen composite 비용이 frame budget을 쉽게 초과한다.
- 모든 탭·모든 리스트 아이템에 `AutomaticKeepAlive`를 적용한다. 메모리가 선형으로 늘어나고, 대부분의 아이템은 유지할 필요가 없다.
- Profiler로 jank 원인을 확인하지 않은 채 `RepaintBoundary`와 isolate를 뿌린다. 대부분 효과가 없거나 오히려 느려진다.
- 큰 이미지를 원본 해상도 그대로 `Image.network`로 띄운다. `cacheWidth` / `cacheHeight`를 지정해 디코딩 비용을 줄여야 한다.

## Gotchas

- **Isolate의 spawn/message 비용**: `compute`는 인자와 결과를 복사(직렬화)한다. 작은 작업에 isolate를 쓰면 오히려 더 느리다. 실제로 수십 ms 이상 걸리는 CPU bound 작업에만 사용한다.
- **`RepaintBoundary`는 만능이 아니다**: 서브트리가 실제로 자주 repaint되고, 부모는 그렇지 않을 때만 이득이 있다. 그렇지 않으면 layer 생성/합성 비용만 추가된다. DevTools의 "Highlight repaints"로 효과를 확인한 뒤 적용한다.
- **`const` 생성자 연쇄**: 부모에 `const`를 붙이려면 모든 파라미터가 `const`여야 한다. 한 곳에서 `const`가 깨지면 상위까지 전부 재빌드되므로, 디자인 시스템 레벨 위젯부터 `const` 가능성을 설계에 포함한다.
- **`ImageCache` 재설정**: 이미지가 많은 앱에서는 `PaintingBinding.instance.imageCache`의 `maximumSize` / `maximumSizeBytes`를 조정해야 한다. 기본값은 모든 앱에 최적은 아니다.
- **`setState` 범위**: 큰 위젯 전체의 `setState` 대신 상태가 바뀌는 작은 서브트리로 분리(또는 `ValueListenableBuilder` / Riverpod `select`)하여 rebuild 범위를 좁힌다.
