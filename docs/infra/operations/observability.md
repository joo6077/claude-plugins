---
title: 관측성
version: 0.2.0
last_updated: 2026-08-13
---

# 관측성

메트릭·로그·트레이스 상호연결, Prometheus 타입 선택, 대시보드 설계, 구조화 로깅, SLI/SLO, 알림 전략, 카디널리티 관리, 성능 조사 시 환경 요인 선배제(USE × RED)를 다룬다.

---

## 원칙

### 1. 메트릭·로그·트레이스를 공통 컨텍스트로 상호연결한다

세 신호를 독립적으로 수집하면 장애 시 연결 고리가 없어 진단이 지연된다. OpenTelemetry는 signals, context propagation, OTLP, semantic conventions를 표준화하여 trace_id 하나로 메트릭 → 트레이스 → 로그를 탐색할 수 있게 한다. 수집 파이프라인을 통합하는 것이 아니라 컨텍스트를 공유하는 것이 핵심이다.

> **출처:** [OpenTelemetry — Signals](https://opentelemetry.io/docs/concepts/signals/)

### 2. Prometheus 메트릭 타입을 엄격히 선택한다

counter는 누적 증가값(요청 수, 에러 수), gauge는 증감하는 현재값(큐 길이, 온도), histogram은 분포와 SLO 계산(지연 시간 버킷), summary는 클라이언트 측 quantile이다. 타입을 잘못 선택하면 집계 결과가 의미 없어지거나, 멀티 인스턴스 환경에서 합산이 불가능해진다.

> **출처:** [Prometheus — Metric Types](https://prometheus.io/docs/concepts/metric_types/)

### 3. 대시보드는 운영 의사결정 도구로 설계한다

상단에 사용자 영향 지표(에러율, 지연 시간, 가용성)를 배치하고, 하단에 원인 후보(CPU, 메모리, 큐 깊이)를 배치한다. 각 패널은 drill-down이 가능해야 하며, 패널 수집장이 아닌 "무엇이 잘못되었고 어디를 파야 하는가"에 답하는 구조여야 한다.

> **출처:** [Grafana — Alerting Best Practices](https://grafana.com/docs/grafana/latest/alerting/guides/best-practices/)

### 4. 로그는 구조화(JSON/ECS) 우선으로 출력한다

비구조화 텍스트 로그는 파싱 비용이 높고 필드 기반 검색이 어렵다. JSON 또는 ECS(Elastic Common Schema) 형식으로 출력하되, trace_id, service.name, env 필드를 반드시 포함한다. 이 필드들이 메트릭·트레이스와의 연결 고리가 된다.

> **출처:** [Elastic — ECS Application Logs](https://www.elastic.co/guide/en/serverless/current/observability-ecs-application-logs.html)

### 5. SLI/SLO는 제품 우선순위 결정 장치다

SLI(Service Level Indicator)는 측정 가능한 사용자 경험 지표이고, SLO(Service Level Objective)는 그 목표 수준이다. error budget(1 - SLO)을 릴리스 속도와 연결하면 "안정성에 투자할 때"와 "기능에 투자할 때"를 정량적으로 판단할 수 있다. SLO 없이 모니터링만 하면 경보 피로만 쌓인다.

> **출처:** [Google SRE Workbook — Implementing SLOs](https://sre.google/workbook/implementing-slos/)

### 6. 알림은 사용자 증상 중심으로 설정한다

latency, error rate, availability SLI 기반 경보만 페이징(즉시 대응)으로 설정한다. CPU 사용률, 디스크 여유 같은 인프라 경보는 티켓 또는 업무시간 알림으로 분류한다. 모든 경보를 페이징으로 설정하면 경보 피로로 인해 실제 장애를 놓치게 된다.

> **출처:** [Google SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

### 7. 카디널리티를 적극적으로 관리한다

pod_name, user_id, request_id 같은 고유값을 메트릭 라벨에 넣으면 시계열 수가 폭증하여 저장 비용과 쿼리 지연이 급증한다. 이런 값은 로그나 structured metadata로 전달하고, 메트릭 라벨은 유한한 집합(status_code, method, endpoint 등)으로 제한한다.

> **출처:** [Grafana Loki — Modify Default Labels](https://grafana.com/docs/loki/latest/get-started/labels/modify-default-labels/)

### 8. 성능 조사는 환경 요인을 먼저 배제한다 (USE × RED)

느리다는 신고를 받았을 때 앱 코드부터 뜯으면, 원인이 호스트/런타임 포화였을 때 시간을 통째로 버린다. 두 절차를 **동시에** 돌리되 역할을 나눈다.

- **RED — 사용자 영향 확인.** 서비스 단위로 request **R**ate, **E**rror rate, **D**uration 을 본다. "무엇이 얼마나 나빠졌는가" 를 확정하는 층이다.
- **USE — 환경 병목 배제.** 모든 리소스에 대해 **U**tilization, **S**aturation, **E**rrors 를 확인한다. saturation·error 는 utilization 이 낮아 보여도 병목을 드러내므로 특히 중요하다.

USE 로 확인할 최소 지표:

| 리소스 | saturation / error 지표 |
| ------ | ------ |
| CPU | run queue 길이, steal time |
| 메모리 | paging/swap 활동, OOM kill 횟수 |
| 디스크 | I/O queue 깊이, I/O error |
| 네트워크 | drop, retransmit, 인터페이스 error |
| 런타임/프로세스 | GC pause, thread pool 포화, event-loop lag |

**호스트 또는 런타임에 saturation 증거가 있으면 앱 코드를 원인으로 단정하지 마라.** 그 증거를 먼저 해소하거나 격리한 뒤 다시 측정한다. 반대로 USE 가 전부 깨끗한데 RED 만 나쁘면 그때 앱·쿼리·의존 서비스로 좁힌다.

> **출처:** [USE Method — Brendan Gregg](https://www.brendangregg.com/usemethod.html)
>
> RED Method 는 서비스 단위 rate/error/duration 을 보는 대응 절차로 함께 쓰지만, **1차 출처를 이번 갱신 범위에서 확인하지 못했다** — 인용이 필요하면 출처를 먼저 확정하라.

---

## 수치/기준값

- GCP `_Default` 로그 버킷: 기본 보존 30일, `_Required` 버킷: 400일
- CloudWatch Logs: 기본 보존 무기한(반드시 보존 정책을 명시적으로 설정해야 비용 제어 가능)
- Fast burn-rate 알림 창: 5~15분, slow burn-rate 알림 창: 1~6시간 — 이중 창 조합으로 오탐 감소
- Prometheus summary는 샤드(인스턴스) 간 quantile 집계가 수학적으로 불가능

---

## 안티패턴

- **모든 라벨에 high-cardinality 값 사용**: pod_name, user_id를 메트릭 라벨로 넣어 시계열 폭증. 로그/trace로 전달해야 한다
- **로그에 trace_id 누락**: 트레이스에서 로그로 drill-down이 불가능해져 관측성 3대 신호의 연결이 끊긴다
- **대시보드를 패널 수집장으로 운영**: 목적 없는 패널이 수십 개 나열되면 장애 시 어디를 봐야 할지 모른다
- **summary를 전역 p95에 사용**: 멀티 인스턴스 환경에서 summary quantile은 합산 불가. histogram을 사용해야 한다
- **모든 경보를 paging으로 설정**: 경보 피로로 실제 장애 알림을 무시하게 된다. 증상 기반만 페이징

---

## Gotchas

- **OpenTelemetry 를 "3 신호 모두 stable" 한 덩어리로 취급하지 마라.** OTel 은 signal 별로 개발되며 성숙도가 다르다 — tracing(traces) 은 stable, metrics 는 API/protocol 이 stable 이나 SDK 는 언어별로 혼재(mixed), logging(logs) 은 stable, profiles 는 protocol 이 development 단계다. 도입 판단과 감사 기준은 **signal/component 단위**로 세우고, 성숙도가 낮은 signal 은 필수가 아니라 선택으로 둔다. 반대로 낡은 문서의 "아직 experimental" 서술도 그대로 믿지 말고 매번 spec status 를 확인하라 (출처: [OpenTelemetry spec status](https://opentelemetry.io/docs/specs/status/))
- OTel SDK를 도입하는 것만으로 표준화가 되지 않는다. semantic conventions를 팀 규칙으로 정의하고 리뷰해야 일관성이 유지된다
- summary는 멀티 인스턴스 SLO 계산에 부적합하다 — histogram으로 서버 측에서 집계해야 정확한 전역 percentile을 얻는다
- 로그 샘플링은 비용 절감에 효과적이지만 보안 로그, 감사(audit) 로그에는 적용 금지 — 규정 준수 위반 위험
- tracing span naming 품질이 낮으면(예: 모든 span이 "HTTP request") 트레이스 검색과 분석의 실효성이 급격히 떨어진다
