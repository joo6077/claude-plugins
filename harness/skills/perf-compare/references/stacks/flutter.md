# 스택: Flutter 앱

감지: `pubspec.yaml` 에 `flutter:` 가 있다. 명령 접두는 `.fvmrc` 가 있으면 `fvm flutter`, 없으면 `flutter` 다 — 아래 `{FLUTTER}` 자리에 넣는다.
`{PKG}` 는 Android 패키지 이름, `{BUNDLE}` 은 iOS 번들 ID 다. 한 번 실행이 표본 하나다.

## 환경 다섯 줄 — 측정 전에 응답에 남긴다

```text
빌드 모드: {profile | release | debug}
기기: {실기기 모델명 | 시뮬레이터 · 에뮬레이터 이름}
주사율: {60 | 90 | 120}Hz → 프레임 예산 {16.7 | 11.1 | 8.3}ms
렌더러: {Impeller | Skia}
호스트 상태: {swap 사용량 · memory pressure} (시뮬레이터일 때)
```

모르면 `미확인` 이라 적는다. 디버그 빌드나 시뮬레이터면 잴 수 있는 지표를 서버를 기다리는 구간(랜딩 프리로드)과 전송량으로 좁히고 사용자에게 알린다.

## 함정

- **profile mode · 실기기가 아니면 앱 쪽 수치는 근거가 아니다** — 공식 문서는 성능 측정을 물리 기기 + `--profile` 에서 하라고 하고, profile mode 는 simulator/emulator 에서 꺼져 있다 (<https://docs.flutter.dev/perf/ui-performance>). 프레임 · CPU · 메모리 · 발열 · 배터리는 실기기 profile 빌드에서만 잰다
- **프레임 0 개는 "버벅임 없음" 이 아니라 측정 실패다** — 2026-11-08 viseo365 TC-056 에서 MCP 프레임 지표가 세 번 모두 `No Frame events captured` 를 돌려줬다. 회마다 `frame_count > 0` 을 보고, 0 인 회는 버리고 그 수를 보고에 적는다. 0 이 이어지면 아래 integration_test 경로로 바꾼다
- **프레임 예산은 기기 주사율로 정한다** — `TimelineSummary` 의 `missed_*_budget_count` 는 주사율과 관계없이 16ms 고정값(`kBuildBudget`)으로 센다. 120Hz 기기는 프레임 시간 목록에서 다시 센다
- **시간 마커 임시 코드는 측정 뒤 되돌린다** — 되돌린 뒤 `git diff --stat` 출력을 보고에 남긴다
- **시뮬레이터 · 에뮬레이터의 발열 · 배터리 값은 쓰지 않는다** — 실기기에서 온 값이 아니면 지표에서 빼고 이유를 적는다
- **MCP 서버와 도구 이름은 이 문서에 적지 않는다** — 프레임 · 네트워크 · 성능 지표 도구가 있는지는 프로젝트에 등록된 서버의 도구 목록으로 확인한다

## 어느 경로로 잴까

| 지표 | 실기기 profile | 시뮬레이터 · 디버그 (서버 비교 전용) |
| --- | --- | --- |
| 첫 프레임까지 시간 | `--trace-startup` | 쓰지 않는다 |
| 시작 구간별 시간 | 임시 마커 로그 | 임시 마커 로그 (서버를 기다리는 구간만 의미 있다) |
| 프레임 빌드 · 래스터 시간, 초과 프레임 | integration_test `traceAction` | 쓰지 않는다 |
| 메모리 | Android `dumpsys meminfo` · iOS Instruments | `ps` RSS (같은 빌드끼리만 비교) |
| CPU | Android `top` · iOS Instruments | 쓰지 않는다 |
| 발열 | Android `PowerManager.getCurrentThermalStatus()` 로그 · iOS `thermalState` 로그 | 쓰지 않는다 |
| 배터리 | Android Power Profiler · Macrobenchmark power metric · `batterystats` · iOS Xcode Energy | 쓰지 않는다 |
| 화면당 전송량 | 앱 HTTP 로그 · MCP 네트워크 기록 도구 | 같다 |

## 첫 프레임까지 시간

```bash
{FLUTTER} run --profile --trace-startup -d <기기 ID>
# 첫 프레임 뒤 도구가 start_up_info.json 을 쓴다. 쓰는 폴더는 SDK 판마다 다를 수 있어 찾아서 읽는다
f=$(find build -name start_up_info.json -newer pubspec.yaml | head -1)
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["timeToFirstFrameRasterizedMicros"] / 1000)' "$f"
```

- 키는 `engineEnterTimestampMicros` · `timeToFrameworkInitMicros` · `timeToFirstFrameMicros` · `timeToFirstFrameRasterizedMicros` · `timeAfterFrameworkInitMicros` 다. `timeToFirstFrameMicros` 는 첫 프레임을 **빌드한** 시각이고 옛 벤치마크 호환용이다. 화면에 실제로 그려진 시각은 `timeToFirstFrameRasterizedMicros` 라 이것을 쓴다
- 첫 프레임 이벤트가 타임라인에 없으면 도구가 `Cannot compute startup time.` 오류를 낸다. 그 회는 표본에서 뺀다
- 실행마다 파일이 덮어써지므로 회마다 값을 꺼내 바로 기록한다
- Android 의 TTID(첫 프레임까지 시간)는 `adb shell am start -S -W {PKG}/.MainActivity` 의 `TotalTime` 이나 logcat 의 `Displayed` 줄로 잰다. `-S` 가 시작 전에 앱을 강제 종료한다. 공식 문서도 이 값이 모든 자원이 그려질 때까지를 담지는 않는다고 적는다. Flutter 첫 프레임 값과 섞지 않는다

## 시작 구간별 시간 — 임시 마커

`main()` 첫 줄, `runApp` 직전, 랜딩 프리로드 시작 · 끝처럼 구간 경계에 임시 로그를 넣는다.

```dart
// 측정용 임시 코드 — 측정 뒤 되돌린다
debugPrint('[BOOT] main ${DateTime.now().millisecondsSinceEpoch}');
```

```bash
# iOS 시뮬레이터: 완전히 끄고 다시 켜서 로그에서 마커를 모은다
xcrun simctl terminate booted {BUNDLE}; t0=$(python3 -c 'import time; print(int(time.time()*1000))')
xcrun simctl launch booted {BUNDLE}; sleep 15
xcrun simctl spawn booted log show --last 30s --predicate 'eventMessage CONTAINS "[BOOT]"' --style compact
```

- 실행 시각(`t0`)과 마커 시각의 차가 구간 시간이다. 파싱 명령은 로그 두세 줄로 알려진 답 대조를 먼저 한다
- release 빌드에서는 `debugPrint` 가 남지만 `print` 나 `logger` 설정에 따라 꺼질 수 있다. 첫 회에 마커가 다 찍히는지 본다

## 프레임 — integration_test

```dart
// integration_test/scroll_perf_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('목록 스크롤', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    final list = find.byType(Scrollable).first;
    await binding.traceAction(() async {
      for (var i = 0; i < 10; i++) {
        await tester.fling(list, const Offset(0, -600), 3000);
        await tester.pumpAndSettle();
      }
    }, reportKey: 'scroll');
  });
}
```

```dart
// test_driver/perf_driver.dart
import 'package:flutter_driver/flutter_driver.dart' as driver;
import 'package:integration_test/integration_test_driver.dart';

Future<void> main() {
  return integrationDriver(
    responseDataCallback: (data) async {
      final timeline = driver.Timeline.fromJson(data!['scroll'] as Map<String, dynamic>);
      final summary = driver.TimelineSummary.summarize(timeline);
      await summary.writeTimelineToFile('scroll', pretty: true, includeSummary: true);
    },
  );
}
```

```bash
{FLUTTER} drive --profile -d <기기 ID> \
  --driver=test_driver/perf_driver.dart --target=integration_test/scroll_perf_test.dart
python3 - "$(ls -t build/*.timeline_summary.json | head -1)" <<'EOF'
import json, sys
s = json.load(open(sys.argv[1]))
print(s["frame_count"], s["average_frame_build_time_millis"], s["90th_percentile_frame_build_time_millis"],
      s["missed_frame_build_budget_count"], s["average_frame_rasterizer_time_millis"],
      s["missed_frame_rasterizer_budget_count"])
EOF
```

- `my_app` 은 `pubspec.yaml` 의 `name` 으로 바꾼다. `flutter_driver` · `integration_test` 를 `dev_dependencies` 에 더해야 한다
- 실기기 · 에뮬레이터에서는 `--no-dds` 를 붙여 돌린다 (공식 cookbook 안내)
- 결과는 `build/` 아래 `{이름}.timeline_summary.json` 과 `{이름}.timeline.json` 이다. cookbook 예시도 파일 이름이 `reportKey` 와 다르게 적혀 있어 `ls build/*.timeline_summary.json` 으로 찾아 읽는다
- 초과 프레임 비율 = (`missed_frame_build_budget_count` + `missed_frame_rasterizer_budget_count`) ÷ `frame_count` × 100. 두 수가 같은 프레임을 겹쳐 셀 수 있어 상한 어림값이다 — 보고에 그렇게 적는다
- `missed_*_budget_count` 는 `kBuildBudget` = 16ms 고정값으로 센다. API 문서가 "실제 기기 주사율을 고려하지 않는 고정값" 이라고 적는다. 120Hz 기기는 `frame_build_times` · `frame_rasterizer_times`(마이크로초 목록)에서 8,333 을 넘는 프레임을 다시 세고, 그러지 못하면 보고에 기준이 16ms 라고 적는다
- `frame_count` 가 0 이면 측정 실패다
- MCP 서버에 프레임 지표 도구가 있으면 같은 시나리오에서 함께 돌려 볼 수 있다. 0 프레임이 나오면 그 도구 값은 쓰지 않는다

## 메모리

```bash
# Android: 시나리오 끝에서 TOTAL PSS (KB)
adb shell dumpsys meminfo {PKG} | awk '/TOTAL PSS:/ {print $3; exit} /TOTAL:/ {print $2; exit}'
# iOS 시뮬레이터 · 같은 빌드끼리만: RSS (KB)
ps -o rss= -p "$(pgrep -f '{BUNDLE}' | head -1)"
```

- `TOTAL` 은 그 위 PSS 칸들의 합이고 단위는 KB 다. 공식 문서는 `Pss Total` 과 `Private Dirty` 두 열을 보라고 한다
- `dumpsys meminfo` 출력 형식은 Android 판마다 다르다. 첫 회에 원문을 한 번 보고 파싱 위치를 맞춘다
- iOS 실기기는 Xcode Instruments(Allocations · VM Tracker)로 시나리오 최대값을 읽는다. 자동화가 어려우면 손 측정으로 적고 `source` 에 그렇게 쓴다

## CPU

```bash
# Android: 시나리오 동안 1초마다 앱 CPU % 를 모아 평균
pid=$(adb shell pidof {PKG}); for i in $(seq 1 20); do adb shell top -b -n 1 -p "$pid" | awk -v p="$pid" '$1==p {print $9}'; sleep 1; done
```

- `top` 의 열 순서는 기기마다 다를 수 있다. 머리 줄에서 `%CPU` 위치를 먼저 확인한다
- iOS 실기기는 Instruments Time Profiler 로 시나리오 구간 평균을 읽는다

## 발열

- Android 는 임시 플랫폼 채널로 `PowerManager.getCurrentThermalStatus()`(API 29 이상)를 시나리오 끝에 로그로 찍는다. 값은 0 `NONE` · 1 `LIGHT` · 2 `MODERATE` · 3 `SEVERE` · 4 `CRITICAL` · 5 `EMERGENCY` · 6 `SHUTDOWN` 이다. 공식 문서는 3 `SEVERE` 를 "UX is largely impacted" 로 적는다
- `adb shell dumpsys thermalservice` 도 상태를 보여 주지만 출력 형식이 공식 문서에 없다. 쓰려면 첫 회에 원문을 보고 위 API 값과 같은지 한 번 대조한다
- iOS 는 임시 플랫폼 채널로 `ProcessInfo.processInfo.thermalState` 를 시나리오 끝에 로그로 찍는다. 단계 이름(`nominal` · `fair` · `serious` · `critical`)을 그대로 남기고, 숫자로 바꿀 때는 이 순서로 0~3 을 매긴다고 기록에 적는다 — Apple 문서의 원시값은 이번 대조에서 확인하지 못했다
- 발열은 이전 측정의 열이 남는다. 회 사이에 기기를 식히고(같은 시간 대기) 시작 단계가 0 인지 본다

## 배터리

- Android 는 Android Studio Power Profiler 나 Macrobenchmark power metric 을 먼저 쓴다. Battery Historian 은 공식 문서에서 더 이상 관리되지 않는다고 안내한다
- 명령줄로만 잴 때는 아래 순서다. 통계 지우기는 Battery Historian 설정 문서, 충전 해제 흉내와 되돌리기는 전력 테스트 문서에 있다

```bash
adb shell dumpsys battery unplug          # 충전 해제 상태로 흉내
adb shell dumpsys batterystats --reset    # 통계 지우기
# ... 시나리오 실행 ...
adb shell dumpsys batterystats --charged {PKG} > batterystats.txt   # 앱 UID 별 전력 사용 어림값이 들어 있다
adb shell dumpsys battery reset           # 흉내 되돌리기
```

- 출력에서 앱 UID 의 전력 사용 줄은 판마다 이름이 다르다. 첫 회에 원문을 보고 읽을 줄을 정한다
- 짧은 시나리오는 어림값이 0 에 가깝게 나온다. 시나리오를 5 분 이상 반복하게 묶는다
- iOS 는 Xcode Organizer 의 Energy 보고서나 Instruments Energy Log 로 손 측정한다

## 화면당 전송량

- 앱 HTTP 로그에 응답 bytes 가 찍히면 화면 진입부터 다음 조작 전까지 합산한다
- MCP 서버에 네트워크 기록 도구가 있으면 같은 구간의 응답 크기 합을 쓴다
- 이미지 캐시가 있으면 첫 진입(캐시 비움)과 재진입을 다른 지표로 나눈다
- 전송량은 결정값에 가깝다. 쪽마다 2 회로 같은 값이 나오는지 확인한다

## 출처

- Flutter cookbook — Measure performance with an integration test: <https://docs.flutter.dev/cookbook/testing/integration/profiling>
- `TimelineSummary.summaryJson`: <https://api.flutter.dev/flutter/flutter_driver/TimelineSummary/summaryJson.html> · `kBuildBudget`: <https://api.flutter.dev/flutter/flutter_driver/kBuildBudget-constant.html>
- flutter_tools `tracing.dart` (start_up_info.json 키): <https://flutter.googlesource.com/mirrors/flutter/+/refs/heads/master/packages/flutter_tools/lib/src/tracing.dart>
- Android 앱 시작 시간(TTID · `am start -S -W`): <https://developer.android.com/topic/performance/vitals/launch-time>
- Android 열 완화(상태 0~6): <https://source.android.com/docs/core/power/thermal-mitigation>
- Android `dumpsys` (meminfo · batterystats): <https://developer.android.com/tools/dumpsys>
- Battery Historian 설정(`batterystats --reset`, 관리 중단 안내): <https://developer.android.com/topic/performance/power/setup-battery-historian>
- 전력 테스트(`dumpsys battery unplug` · `reset`): <https://developer.android.com/topic/performance/power/test-power>
