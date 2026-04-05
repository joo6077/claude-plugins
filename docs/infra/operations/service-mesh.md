---
title: 서비스 메시
version: 0.1.0
last_updated: 2026-04-04
---

# 서비스 메시

Data plane/control plane 분리, sidecar vs ambient, mTLS, 트래픽 관리, 관측성 자동 수집, workload identity 기반 정책, 도입 판단 기준을 다룬다.

---

## 원칙

### 1. 인프라 계층에서 service-to-service 통신 정책을 처리한다

애플리케이션 코드에 retry, timeout, mTLS, 접근 제어를 직접 구현하면 언어/프레임워크마다 중복 구현이 발생하고 일관성이 깨진다. 서비스 메시는 data plane(프록시)과 control plane(설정 관리)을 분리하여 통신 정책을 인프라에 위임한다.

> **출처:** [Istio — Ambient Mesh](https://istio.io/latest/docs/ambient/)

### 2. Sidecar와 ambient 모드의 차이를 이해하고 선택한다

Sidecar 모드는 워크로드(pod)마다 프록시를 배치하여 완전한 L7 제어를 제공한다. Ambient 모드는 노드 단위 ztunnel로 L4 mTLS를 처리하고, L7 정책이 필요한 서비스에만 선택적으로 waypoint 프록시를 배치한다. 리소스 효율성과 기능 요구 수준에 따라 선택한다.

> **출처:** [Istio — Ambient Mesh](https://istio.io/latest/docs/ambient/)

### 3. mTLS는 기본값으로 설정한다

서비스 간 통신을 암호화하고 상호 인증하는 mTLS는 zero-trust 네트워크의 기본 요소다. Linkerd는 automatic mTLS를 제공하고, Istio는 PeerAuthentication으로 mTLS 모드를 제어한다. 메시를 도입하고도 mTLS를 활성화하지 않으면 핵심 가치를 놓치는 것이다.

> **출처:** [Linkerd — Features](https://linkerd.io/2.18/features/) , [Istio — Authorization Policy](https://istio.io/latest/docs/reference/config/security/authorization-policy/)

### 4. 트래픽 관리는 east-west에도 적용한다

canary 배포, retry, timeout, circuit breaking, fault injection은 외부 트래픽(north-south)뿐 아니라 서비스 간 내부 트래픽(east-west)에도 적용해야 한다. 내부 호출의 장애 전파를 차단하지 않으면 cascading failure가 발생한다.

> **출처:** [Istio — Traffic Management](https://istio.io/latest/docs/tasks/traffic-management/)

### 5. 메시의 핵심 가치는 보안+관측성 일관성이다

메트릭(요청 수, 지연, 에러율), 트레이스(분산 추적)를 프록시가 자동 수집하므로 애플리케이션 코드 변경 없이 전체 서비스의 관측성을 확보할 수 있다. 이것이 메시 도입의 ROI를 가장 빠르게 체감할 수 있는 영역이다.

> **출처:** [Istio — Telemetry](https://istio.io/latest/docs/reference/config/telemetry/)

### 6. 정책은 네트워크 ACL보다 workload identity 기반으로 설정한다

IP 주소 기반 ACL은 동적 환경(Kubernetes)에서 불안정하다. AuthorizationPolicy와 RBAC로 서비스 계정(workload identity) 기반 접근 제어를 설정하면 pod가 재스케줄링되어도 정책이 유지된다.

> **출처:** [Istio — Authorization Policy](https://istio.io/latest/docs/reference/config/security/authorization-policy/)

### 7. 도입 판단은 서비스 수, 팀 수, 언어 다양성, zero-trust 필요성, 운영 성숙도를 기준으로 한다

서비스 메시는 운영 복잡성을 추가한다. 서비스가 적거나 단일 팀/단일 언어인 경우 라이브러리 수준 솔루션으로 충분할 수 있다. 도입 전에 현재 pain point가 메시로 해결되는지, 운영할 역량이 있는지 평가한다.

> **출처:** [Istio — Ambient Mesh](https://istio.io/latest/docs/ambient/)

---

## 수치/기준값

- Sidecar 모드: pod당 프록시 1개 (Envoy 컨테이너)
- Ambient 모드: node당 ztunnel 1개 + 필요 시 waypoint 프록시 추가
- 도입 검토 시작점: 독립 서비스 20+, 운영 팀 2+, 언어/프레임워크 혼합, mTLS/RBAC을 앱별로 중복 구현 중인 경우
- p99 latency + CPU 오버헤드: sidecar 도입 전후 벤치마크 필수 (프록시 홉 추가로 수백 마이크로초~밀리초 단위 증가 가능)

---

## 안티패턴

- **서비스 수가 적은데 미리 도입**: 운영 복잡성만 추가되고 ROI가 나지 않는다. 라이브러리 수준 솔루션으로 시작하고, pain point가 명확해지면 도입한다
- **앱 timeout 없이 mesh retry만 의존**: 메시 retry가 앱의 timeout과 조율되지 않으면 사용자가 이미 포기한 요청을 계속 재시도한다
- **mTLS만 켜고 authorization을 비워둠**: 암호화는 되지만 아무 서비스나 다른 서비스를 호출할 수 있다. mTLS + AuthorizationPolicy 조합이 필수
- **모든 서비스에 L7 정책 강제**: L4 mTLS로 충분한 서비스에까지 L7 프록시를 배치하면 리소스 낭비. ambient 모드의 선택적 waypoint가 이 문제를 해결한다
- **관측성 자동 수집만 믿고 SLO 생략**: 메트릭이 수집된다고 해서 SLO가 정의된 것은 아니다. 수집된 데이터로 SLI/SLO를 설정해야 의미가 있다

---

## Gotchas

- Retry는 정상 시에는 복원력을 높이지만 폭주(overload) 시에는 증폭기가 된다. retry budget 또는 circuit breaker와 반드시 조합한다
- Sidecar, ambient 모두 네트워크 경로에 프록시 홉을 추가하므로 디버깅 시 추가 경로를 고려해야 한다. tcpdump, istioctl analyze 등으로 프록시 레벨 문제를 분리한다
- Ambient 모드에서 L7 기능(header 기반 라우팅, fault injection 등)이 필요하면 waypoint 프록시를 별도 설계해야 한다. ztunnel만으로는 L4까지만 처리된다
- Istio는 기능 폭이 넓고 Linkerd는 단순/경량이다. "어느 것이 더 좋은가"보다 조직의 운영 역량과 요구 기능에 맞는 선택이 중요하다
