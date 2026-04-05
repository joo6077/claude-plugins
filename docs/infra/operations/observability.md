---
title: 관측성
version: 0.1.0
last_updated: 2026-04-04
---

# 관측성

메트릭·로그·트레이스 상호연결, Prometheus 타입 선택, 대시보드 설계, 구조화 로깅, SLI/SLO, 알림 전략, 카디널리티 관리를 다룬다.

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

- OTel SDK를 도입하는 것만으로 표준화가 되지 않는다. semantic conventions를 팀 규칙으로 정의하고 리뷰해야 일관성이 유지된다
- summary는 멀티 인스턴스 SLO 계산에 부적합하다 — histogram으로 서버 측에서 집계해야 정확한 전역 percentile을 얻는다
- 로그 샘플링은 비용 절감에 효과적이지만 보안 로그, 감사(audit) 로그에는 적용 금지 — 규정 준수 위반 위험
- tracing span naming 품질이 낮으면(예: 모든 span이 "HTTP request") 트레이스 검색과 분석의 실효성이 급격히 떨어진다
