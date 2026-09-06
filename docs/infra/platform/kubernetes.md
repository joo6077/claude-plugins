---
title: 쿠버네티스
version: 0.1.0
last_updated: 2026-04-04
---

# 쿠버네티스

리소스 매니페스트, Helm/Kustomize, RBAC, 네임스페이스, Pod Security Standards, requests/limits, HPA/VPA, 프로브, PDB를 다룬다.

---

## 원칙

### 1. 모든 워크로드에 requests/limits를 명시한다

requests는 스케줄러가 노드를 선택하는 기준이고, limits는 런타임 상한이다. requests가 없으면 스케줄러가 실제 필요량을 모르므로 노드에 과밀 배치되고, limits가 없으면 단일 Pod가 노드 전체를 점유할 수 있다. 두 값을 모두 명시하여 예측 가능한 스케줄링과 격리를 확보한다.

> **출처:** [Kubernetes — Manage Resources Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

### 2. liveness/readiness/startup probe 역할을 분리한다

liveness probe 실패는 컨테이너 재시작, readiness probe 실패는 서비스 엔드포인트 제외, startup probe는 느린 초기화 완료 대기 전용이다. 역할을 혼동하면 초기화 중인 Pod가 재시작 루프에 빠지거나, 장애 Pod가 트래픽을 계속 받는다. 부팅이 느린 앱은 startup probe로 초기화 시간을 확보한 뒤 liveness/readiness가 작동하게 한다.

> **출처:** [Kubernetes — Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)

### 3. 네임스페이스는 팀/정책 경계용이다

네임스페이스는 RBAC, ResourceQuota, NetworkPolicy의 스코핑 단위다. 팀, 환경(dev/staging/prod), 서비스 그룹 단위로 분리한다. 버전 구분(v1/v2)에는 네임스페이스가 아닌 labels와 selectors를 사용한다. `default` 네임스페이스에 워크로드를 배치하지 않는다.

> **출처:** [Kubernetes — Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces)

### 4. RBAC는 namespace-scoped RoleBinding을 우선한다

ClusterRoleBinding은 클러스터 전체에 영향을 주므로 최소한으로 제한한다. 대부분의 워크로드와 운영자 권한은 namespace-scoped RoleBinding으로 충분하다. wildcard(`*`) 리소스/동사, `cluster-admin` 바인딩을 남용하지 않는다. ServiceAccount별로 필요한 최소 권한만 부여한다.

> **출처:** [Kubernetes — RBAC Good Practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)

### 5. Pod Security Standards를 단계적으로 도입한다

restricted 프로파일을 최종 목표로 설정하되, 기존 워크로드에 즉시 enforce하면 대량 실패가 발생한다. warn → audit → enforce 순서로 단계적으로 적용한다. 네임스페이스 레이블로 프로파일을 지정하며, privileged는 시스템 워크로드에만 허용한다.

> **출처:** [Kubernetes — Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

### 6. HPA와 VPA의 역할을 구분한다

HPA(Horizontal Pod Autoscaler)는 부하 증가 시 Pod 수를 늘려 대응한다. VPA(Vertical Pod Autoscaler)는 개별 Pod의 requests/limits를 실 사용량에 맞게 조정(rightsizing)한다. 같은 리소스 메트릭(CPU)에 대해 HPA와 VPA를 동시에 적용하면 서로 충돌하므로, VPA는 메모리 rightsizing 또는 recommendation 모드로만 병행한다.

> **출처:** [Kubernetes — Horizontal Pod Autoscale](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/)

### 7. Helm은 값 구조와 재사용성, Kustomize는 base/overlay 조합이다

Helm은 템플릿 엔진으로 values.yaml을 통해 환경별 설정을 주입한다. 차트의 값 구조를 평탄하고 문서화되게 유지한다. Kustomize는 base 매니페스트 위에 overlay를 패치하는 방식으로 원본을 수정하지 않는다. 프로젝트 특성에 맞게 하나를 선택하거나 Helm으로 생성 후 Kustomize로 환경별 패치하는 조합도 가능하다.

> **출처:** [Helm — Chart Best Practices](https://helm.sh/docs/chart_best_practices/)

### 8. PDB는 자발적 disruption 완화 전용이다

PodDisruptionBudget은 노드 drain, 클러스터 업그레이드 등 자발적(voluntary) disruption 시 최소 가용 Pod 수를 보장한다. 하드웨어 장애, OOM kill 같은 비자발적(involuntary) disruption에는 적용되지 않는다. `minAvailable` 또는 `maxUnavailable`로 설정하며, 모든 다운타임을 방지하는 장치가 아님을 이해한다.

> **출처:** [Kubernetes — Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

---

## 수치/기준값

| 항목 | 값 | 비고 |
|------|-----|------|
| Probe 기본 periodSeconds | 10 | 점검 간격 |
| Probe 기본 timeoutSeconds | 1 | 응답 대기 시간 |
| Probe 기본 failureThreshold | 3 | 연속 실패 횟수 |
| terminationGracePeriodSeconds 기본값 | 30 | SIGTERM 후 SIGKILL까지 |
| Startup probe 예시 | failureThreshold 30 x periodSeconds 10 = 300s | 느린 앱 부팅 허용 |
| HPA sync 주기 | 15s | `--horizontal-pod-autoscaler-sync-period` |
| HPA CPU 초기화 안정 기간 | 5m | `--horizontal-pod-autoscaler-cpu-initialization-period` |
| HPA readiness delay | 30s | `--horizontal-pod-autoscaler-initial-readiness-delay` |
| CPU 최소 단위 | 1m | 1 milliCPU = 0.001 CPU |
| 500m CPU | 0.5 CPU 코어 | 1000m = 1 CPU |

---

## 안티패턴

- **모든 워크로드를 default 네임스페이스에 배치**: RBAC, ResourceQuota, NetworkPolicy 스코핑이 불가능. 팀/환경별 네임스페이스 분리 필수
- **liveness probe로 readiness를 대체**: liveness 실패는 재시작을 일으키므로, 일시적으로 바쁜 Pod가 불필요하게 재시작됨. readiness는 트래픽 제외만 하므로 역할이 다름
- **requests 없이 limits만 설정**: 스케줄러가 적절한 노드를 선택하지 못하고, QoS 클래스가 Burstable로 설정되어 OOM 우선순위가 높아짐
- **ClusterRoleBinding으로 광범위 권한 부여**: 한 서비스의 권한 과잉이 클러스터 전체 보안 위험으로 확대
- **PDB를 롤링 업데이트 보호로 오해**: PDB는 자발적 disruption(drain)용. Deployment의 `maxUnavailable`/`maxSurge`가 롤링 업데이트 전략

---

## Gotchas

- **limits만 설정하면 requests가 limits로 복사될 수 있다.** LimitRange가 설정된 네임스페이스에서 requests를 생략하면 기본값이나 limits 값이 requests로 들어간다. 의도치 않게 높은 requests가 설정되어 스케줄링에 실패할 수 있다.
- **readiness probe 실패는 재시작이 아닌 엔드포인트 제외다.** Service의 Endpoints 목록에서 해당 Pod가 빠져 트래픽을 받지 않을 뿐, 컨테이너는 계속 실행된다. 재시작이 필요하면 liveness probe가 담당한다.
- **PDB는 kubectl delete pod를 막지 못한다.** `kubectl delete pod`는 비자발적 삭제가 아닌 직접 삭제이므로 PDB가 개입하지 않는다. PDB는 Eviction API를 통한 자발적 제거에만 적용된다.
- **VPA는 별도 CRD 설치가 필요하다.** VPA는 Kubernetes 코어에 포함되지 않는다. `autoscaler` 리포지토리에서 VPA 컴포넌트(Recommender, Updater, Admission Controller)를 별도로 설치해야 한다.
