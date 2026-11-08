# perf-kit 리서치 출처

아래는 2026-11-08 첫 대조 때 원문을 확인한 출처다. 새 출처를 찾기 전에 이 출처가 지금도 같은 말을 하는지 먼저 본다.

## 방법론

| 출처 | 조회 이유 |
| --- | --- |
| [Abedi · Brecht, ICPE 2017](https://research.spec.org/icpe_proceedings/2017/proceedings/p287.pdf) | RMIT — 라운드마다 순서 섞기. PDF 텍스트가 압축돼 있어 WebFetch 가 못 읽으면 내려받은 사본의 스트림을 풀어 읽는다 |
| [Duet Benchmarking (arXiv 2001.05811)](https://arxiv.org/abs/2001.05811) | 동시 실행 비교와 정확도 배수 |
| [Barrett et al., Virtual Machine Warmup Blows Hot and Cold](https://arxiv.org/abs/1602.00602) | 정상 상태 미도달 비율 |
| [SciPy `mannwhitneyu`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html) | exact · 동순위 · 순열 검정 권고, 알려진 답 예제 |

## 스택 문서 (`stacks/*.md` 출처 절과 같다)

| 문서 | 출처 |
| --- | --- |
| `flutter.md` | [Flutter cookbook 성능 측정](https://docs.flutter.dev/cookbook/testing/integration/profiling) · [`TimelineSummary.summaryJson`](https://api.flutter.dev/flutter/flutter_driver/TimelineSummary/summaryJson.html) · [`tracing.dart`](https://flutter.googlesource.com/mirrors/flutter/+/refs/heads/master/packages/flutter_tools/lib/src/tracing.dart) · [Android 시작 시간](https://developer.android.com/topic/performance/vitals/launch-time) · [열 완화](https://source.android.com/docs/core/power/thermal-mitigation) · [dumpsys](https://developer.android.com/tools/dumpsys) |
| `rust.md` | [criterion CSV 출력](https://bheisler.github.io/criterion.rs/book/user_guide/csv_output.html) · [hyperfine](https://github.com/sharkdp/hyperfine) |
| `web.md` | [Lighthouse 변동성](https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md) · [INP](https://web.dev/articles/inp) · [TBT](https://web.dev/articles/tbt) · [Vite CLI](https://vite.dev/guide/cli) |
| `load.md` | [k6 열린 · 닫힌 모델](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/) · [constant-arrival-rate](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-arrival-rate/) · [handleSummary](https://grafana.com/docs/k6/latest/results-output/end-of-test/custom-summary/) · [wrk](https://github.com/wg/wrk) |

## 확인하지 못한 것

- Apple `ProcessInfo.ThermalState` 원시값 — 문서 본문이 스크립트로 그려져 WebFetch 가 제목만 받는다
- k6 `dropped_iterations` 지표 — executor 문서에 없다
- `adb shell dumpsys thermalservice` 출력 형식 — 공식 문서에 없다
