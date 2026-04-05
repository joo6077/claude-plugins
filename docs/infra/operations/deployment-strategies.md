---
title: 배포 전략
version: 0.1.0
last_updated: 2026-04-04
---

# 배포 전략

Rolling, Blue-Green, Canary, A/B, feature flag, GitOps(ArgoCD/Flux), 롤백, SLI/SLO 기반 자동 롤백을 다룬다.

---

## 원칙

### 1. 기본 롤링 업데이트는 단순하지만 실패 감지와 자동 되돌림은 별도 장치가 필요하다

Kubernetes 기본 롤링 업데이트는 새 Pod를 점진적으로 띄우고 이전 Pod를 제거한다. 그러나 새 버전이 메트릭 수준에서 악화되는지 자동 감지하지 않으며, readiness probe 실패 외에는 자동 롤백 메커니즘이 없다. Argo Rollouts 같은 도구로 분석 기반 승격/중단을 추가해야 한다.

> **출처:** [Argo Rollouts — Progressive Delivery](https://argoproj.github.io/rollouts/)

### 2. Blue-Green은 빠른 전환과 즉시 rollback을 제공하지만 이중 자원 비용을 감수한다

Blue(현재)와 Green(신규) 두 환경을 동시에 유지하고, 검증 완료 후 트래픽을 한 번에 전환한다. 문제가 발생하면 이전 환경으로 즉시 되돌린다. 리소스 사용량이 2배이므로 비용 효율을 따져야 하며, preview 서비스로 사전 검증한 뒤 전환하는 것이 기본 패턴이다.

> **출처:** [Argo Rollouts — Blue-Green Strategy](https://argoproj.github.io/argo-rollouts/features/bluegreen/)

### 3. Canary는 트래픽 점진 상승과 KPI 기반 승격/중단을 결합한다

소수의 사용자(또는 트래픽 비율)에게 먼저 새 버전을 노출하고, 에러율·지연·성공률 등 KPI를 분석하여 승격 또는 중단을 결정한다. Argo Rollouts는 step 기반으로 트래픽 비율(setWeight)과 분석(analysis) 단계를 정의할 수 있다. Istio, Nginx, ALB 등 트래픽 라우터와 연동하여 실제 트래픽 비율을 제어한다.

> **출처:** [Argo Rollouts — Canary Strategy](https://argoproj.github.io/argo-rollouts/features/canary/)

### 4. 자동 rollback은 배포 이벤트가 아닌 SLI/SLO 위반 기반이어야 한다

"에러 로그가 없으면 승격"이 아니라, Prometheus/Datadog 등에서 수집한 SLI(에러율, p99 지연, 성공률)가 SLO 임계치를 위반하면 자동으로 abort한다. Argo Rollouts의 AnalysisTemplate이 이 패턴을 지원하며, 메트릭 쿼리 결과에 따라 승격/중단/재시도를 결정한다.

> **출처:** [Argo Rollouts — Analysis and Progressive Delivery](https://argoproj.github.io/argo-rollouts/features/analysis/)

### 5. GitOps에서 rollback의 source of truth가 Git인지 cluster stable revision인지 구분한다

Argo Rollouts의 rollback은 클러스터 내 이전 안정 revision으로 되돌리는 것이며, Git 리포지토리를 자동 수정하지 않는다. 따라서 rollback 후 Git 상태와 클러스터 상태가 일시적으로 불일치한다. 운영팀은 rollback 발생 시 Git을 수동으로 동기화하거나, 자동화 파이프라인으로 Git revert를 트리거해야 한다.

> **출처:** [Argo Rollouts — FAQ](https://argoproj.github.io/argo-rollouts/FAQ/)

### 6. Feature flag는 배포와 릴리스를 분리하는 도구이며, 영구 플래그 누적을 방지한다

Feature flag를 사용하면 코드를 배포하되 기능은 비활성 상태로 유지할 수 있다. 이를 통해 배포 리스크를 줄이고, 특정 사용자 그룹에게만 기능을 노출하는 점진적 롤아웃이 가능하다. 그러나 만료 정책 없이 플래그를 누적하면 코드 분기가 복잡해지고 테스트 조합이 폭발한다. 플래그에 만료일을 설정하고, 완전 롤아웃 후 플래그를 제거하는 프로세스를 운영한다.

---

## 수치/기준값

- Canary 기본 maxSurge: **25%**, maxUnavailable: **25%** (Kubernetes Deployment 기본값)
- Blue-Green maxUnavailable 기본값: **0** (기존 환경을 유지한 채 전환)
- Post-promotion 분석 후 old ReplicaSet scale-down 대기: 최소 **30초** (scaleDownDelaySeconds)
- Rollback window revisionHistoryLimit: **3**이면 최근 3개 revision 내에서 fast-track rollback 가능
- Argo Rollouts AnalysisRun 기본 타임아웃: analysisTemplate에서 지정, 미지정 시 무기한 대기
- Canary step 간 pause 없이 승격하면 분석 구간이 확보되지 않음. 최소 **60초** pause 권장

---

## 안티패턴

- **모든 서비스에 동일 배포 전략 강제**: 서비스 특성(stateless/stateful, 트래픽 규모, 장애 영향도)에 따라 전략이 달라야 한다. 소규모 내부 서비스에 canary + analysis는 과잉
- **Canary를 replica 비율만으로 판단하고 트래픽 라우팅 무시**: Pod 수 비율과 실제 트래픽 비율은 다르다. Service mesh나 Ingress 레벨에서 트래픽 가중치를 제어해야 정확한 canary
- **메트릭 없이 "에러 없으면 승격"**: 에러 로그 부재가 정상을 의미하지 않는다. 지연 증가, 성공률 하락, 리소스 사용량 급증 등을 SLI로 측정하고 임계치 기반으로 판단
- **GitOps rollback 후 Git 상태 방치**: 클러스터는 이전 버전으로 돌아갔지만 Git에는 문제 버전이 HEAD로 남아 있으면, 다음 sync에서 문제 버전이 재배포된다

---

## Gotchas

- Argo Rollouts rollback은 Git을 자동 수정하지 않는다. 클러스터와 Git이 일시적으로 불일치하며, ArgoCD auto-sync가 켜져 있으면 문제 버전이 재배포될 수 있다. rollback 시 auto-sync 일시 중단 또는 Git revert 자동화가 필요하다
- HPA(Horizontal Pod Autoscaler)와 canary를 동시에 사용하면 pod 집합의 평균 메트릭 해석이 꼬인다. canary pod의 메트릭이 stable pod에 희석되어 문제를 감지하지 못할 수 있다. canary와 stable을 별도 HPA로 분리하거나, AnalysisTemplate에서 canary pod만 필터링하는 쿼리를 사용한다
- Blue-Green에서 preview 환경 검증 없이 바로 전환하면 비용만 2배인 롤링 업데이트에 불과하다. preview 서비스로 smoke test, integration test를 실행한 뒤 promote한다
- Feature flag는 만료 정책 없이 누적되면 설정 지옥이 된다. 코드에 if/else 분기가 쌓이고, 플래그 조합 테스트가 불가능해진다. 플래그 도입 시 만료일과 제거 담당자를 함께 기록한다
- Argo Rollouts의 AnalysisRun이 Inconclusive를 반환하면 기본 동작은 pause다. abort로 처리할지 계속 진행할지 명시적으로 설정해야 한다
