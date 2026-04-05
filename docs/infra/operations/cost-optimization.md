---
title: 비용 최적화
version: 0.1.0
last_updated: 2026-04-04
---

# 비용 최적화

비용 가시성, 태그/라벨 전략, Rightsizing, 구매 모델, 스토리지 lifecycle, Idle resource, FinOps 체계, 비프로덕션 중단을 다룬다.

---

## 원칙

### 1. 첫 단계는 절감이 아닌 가시성이다

Cost Explorer, Billing Dashboard 없이는 어디서 비용이 발생하는지 감으로 추측하게 된다. 가시성 확보 전에 절감 시도를 하면 영향이 큰 항목을 놓치고 사소한 곳에 시간을 낭비한다.

> **출처:** [Google Cloud — Optimize Observability Costs](https://docs.cloud.google.com/stackdriver/docs/costs/optimize-costs)

### 2. 태그/라벨 전략이 전제조건이다

env, team, service, cost-center, owner를 표준화하여 모든 리소스에 부착한다. 태그 없이는 비용을 팀/서비스별로 분배할 수 없고, 책임 소재가 불명확해진다. 태그 정책은 IaC + admission webhook으로 강제해야 유지된다.

> **출처:** [AWS — Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)

### 3. Rightsizing은 utilization 기반으로 수행한다

"혹시 모르니 크게"가 아닌 실제 사용량 데이터에 기반하여 인스턴스 크기를 조정한다. GCP는 최근 8일 메트릭으로 머신 타입 추천을 제공한다. 단, CPU만 보면 메모리, 네트워크, cold-start 특성을 놓칠 수 있다.

> **출처:** [GCP — Apply Machine Type Recommendations](https://cloud.google.com/compute/docs/instances/apply-machine-type-recommendations-for-instances)

### 4. 구매 모델은 워크로드 특성에 맞춰 선택한다

안정적인 baseline 워크로드는 Reserved Instances/Savings Plans, 가변적인 batch 워크로드는 Spot/Preemptible, 불확실한 워크로드는 On-Demand를 사용한다. 단일 모델로 모든 워크로드를 커버하려 하면 비용 또는 안정성을 희생한다.

> **출처:** [AWS — Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html)

### 5. 스토리지는 lifecycle 자동 이동이 핵심이다

데이터는 시간이 지남에 따라 접근 빈도가 감소한다. S3 Intelligent-Tiering, GCS Lifecycle Policy 등으로 자동 tier 이동을 설정하면 수동 관리 없이 비용이 최적화된다.

> **출처:** [AWS — S3 Intelligent-Tiering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering-overview.html)

### 6. Idle resource 탐지는 자동 권고/정책화한다

사용하지 않는 EBS 볼륨, 유휴 로드밸런서, 미연결 Elastic IP 등은 자동 탐지하여 권고 또는 정리 정책을 적용한다. 수동 점검에 의존하면 리소스가 계속 누적된다.

> **출처:** [AWS — Export Idle Recommendations](https://docs.aws.amazon.com/compute-optimizer/latest/APIReference/API_ExportIdleRecommendations.html)

### 7. FinOps는 운영 체계다

일회성 절감 프로젝트가 아니라 inform → optimize → operate 반복 루프를 조직에 내재화한다. 가시성(inform)으로 현황을 파악하고, 최적화(optimize)로 조치하고, 운영(operate)으로 지속 관리한다.

> **출처:** [FinOps Foundation — Practice Operations](https://www.finops.org/framework/capabilities/finops-practice-operations/)

### 8. Dev/staging은 업무시간 외 자동 중단이 기본이다

비프로덕션 환경을 24/7 가동하면 불필요한 비용이 지속 발생한다. 업무시간 외 자동 중단(스케줄러, Lambda 등)을 기본값으로 설정하고, 필요 시 수동 시작하는 옵트인 방식으로 운영한다.

> **출처:** [FinOps Foundation — Practice Operations](https://www.finops.org/framework/capabilities/finops-practice-operations/)

---

## 수치/기준값

- GCP label: key/value 각 최대 63자, 표준 라벨 10개 이하 권장
- AWS 비용 할당 태그: 활성화 후 Cost Explorer 반영까지 최대 24시간 대기
- GCP rightsizing 추천: 최근 8일 메트릭 기준
- S3 Intelligent-Tiering: 최소 객체 크기 128KB(미만은 항상 Frequent Access tier)
- 비프로덕션 환경: 업무시간 외 자동 중단 기본
- 월 예산 대비 20% 초과 시 알림 설정 권장

---

## 안티패턴

- **태그 누락 방치 후 분석 시도**: 태그 없는 리소스는 비용 분배가 불가능하다. 분석 전에 태그 정책부터 강제한다
- **Spot을 상태 저장 핵심 서비스에 사용**: Spot은 언제든 회수될 수 있다. stateful 워크로드에 사용하면 데이터 손실 위험
- **Lifecycle 없이 Standard tier에 계속 적재**: 접근하지 않는 데이터가 고비용 tier에 방치된다
- **절감률만 보고 성능 영향 무시**: Rightsizing으로 인스턴스를 줄였는데 latency가 증가하면 사용자 경험이 악화된다
- **Dev/staging 주말 상시 가동**: 누구도 사용하지 않는 시간에 비용이 흘러나간다

---

## Gotchas

- Savings Plans/RI는 면죄부가 아니다. 워크로드가 변화하면 약정 자체가 낭비가 될 수 있으므로 주기적으로 커버리지를 검토한다
- 태그 정책은 문서로만 정의하면 붕괴한다. IaC(Terraform/Pulumi) + admission webhook으로 태그 없는 리소스 생성을 차단해야 유지된다
- Rightsizing에서 CPU 사용률만 보면 메모리 부족, 네트워크 병목, cold-start 지연을 놓친다. 복합 메트릭으로 판단해야 한다
- Anomaly detection(비정상 비용 탐지)은 학습 기간과 seasonality 영향으로 초기에는 알림 품질이 들쑥날쑥하다. 임계값 기반 알림과 병행한다
