---
title: 백업 & 재해 복구
version: 0.1.0
last_updated: 2026-04-04
---

# 백업 & 재해 복구

RTO/RPO, 3-2-1 규칙, DB 백업(논리/물리), PITR, DR 테스트, 멀티리전, 장애 복구 runbook, chaos engineering을 다룬다.

---

## 원칙

### 1. RTO/RPO를 먼저 정하고, 그에 맞는 백업·복제·자동화 수준을 선택한다

Recovery Time Objective(RTO)는 서비스 복구까지 허용 가능한 최대 시간, Recovery Point Objective(RPO)는 허용 가능한 최대 데이터 손실 시간이다. 이 두 지표가 백업 빈도, 복제 방식, 자동화 수준, 비용을 결정한다. RTO/RPO 없이 백업 전략을 세우면 과잉 투자이거나 과소 보호다.

> **출처:** [AWS Prescriptive Guidance — Backup and Recovery for RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)

### 2. 논리 백업과 물리 백업/PITR은 대체재가 아닌 보완재다

논리 백업(pg_dump, mysqldump)은 사람이 읽을 수 있고 특정 테이블만 복원 가능하지만 느리다. 물리 백업(스냅샷, WAL 아카이브)은 빠른 전체 복원과 PITR을 지원하지만 세밀한 선택적 복원이 어렵다. 두 방식을 병행하여 각각의 약점을 보완한다.

> **출처:** [AWS — Getting Started with Backup and Restore](https://docs.aws.amazon.com/AmazonRDS/latest/gettingstartedguide/managing-backup-restore.html)

### 3. DB 핵심 시스템은 PITR을 기본 옵션으로 활성화한다

Point-in-Time Recovery(PITR)는 특정 시점으로 데이터베이스를 복원한다. 사람의 실수(잘못된 DELETE/UPDATE)에 대응할 수 있는 유일한 자동화 수단이다. RDS는 자동 백업 활성화 시 PITR을 제공하며, retention window 내 임의 시점(초 단위)으로 복원 가능하다.

> **출처:** [AWS RDS — Point-in-Time Recovery](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html)

### 4. 멀티리전 DR은 복제만이 아니라 실제 복구 runbook과 의존성 재구성을 포함한다

데이터 복제가 끝이 아니다. DNS 전환, 로드 밸런서 재설정, 시크릿 동기화, 캐시 워밍, 외부 서비스 엔드포인트 변경 등 전체 의존성 체인을 재구성하는 runbook이 있어야 한다. 복제본이 있어도 runbook이 없으면 실제 장애에서 RTO를 지키지 못한다.

> **출처:** [AWS RDS — Automated Backups and PITR](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/AutomatedBackups.PiTR.html)

### 5. DR은 문서가 아니라 정기 테스트로 검증한다

DR 계획은 테스트하지 않으면 신뢰할 수 없다. 분기별 또는 반기별로 실제 복구 절차를 실행하고, RTO/RPO 달성 여부를 측정한다. Chaos engineering(예: AWS FIS, Gremlin)으로 장애를 주입하여 시스템과 팀의 대응 능력을 검증한다.

> **출처:** [AWS Prescriptive Guidance — Backup and Recovery for RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)

---

## 수치/기준값

- RDS 자동 백업 보존 기간: 최소 0일(비활성) ~ 최대 **35일**
- RDS 트랜잭션 로그: **5분마다** S3에 업로드 (RPO 최소 약 5분)
- PITR 복원 가능 범위: retention window 내 임의 시점, **초 단위** 정밀도
- RDS 스냅샷: 수동 스냅샷은 보존 기간 무제한, 자동 스냅샷은 retention 기간 이후 삭제
- 3-2-1 규칙: 데이터 **3**개 복사본, **2**가지 다른 미디어, **1**개는 오프사이트(다른 리전/계정)
- Aurora Global Database 복제 지연: 일반적으로 **1초 미만**

---

## 안티패턴

- **스냅샷만 믿고 PITR 부재**: 스냅샷 사이 시간의 데이터 변경은 복구 불가. PITR로 초 단위 복원 경로 확보 필수
- **백업 성공 알림만 보고 restore 테스트 미실시**: 백업이 존재해도 복원이 실패할 수 있다. 정기적으로 실제 복원을 실행하고 데이터 정합성을 확인한다
- **복구 순서 미문서화**: DB만 복원해도 앱 서버, 캐시, 외부 연동이 정상이지 않으면 서비스가 작동하지 않는다. 전체 의존성 복구 순서를 runbook에 명시
- **멀티리전 복제를 DR 완료로 간주**: 복제는 DR의 한 요소일 뿐이다. DNS, 시크릿, 네트워크, 모니터링 등 전체 스택 전환 절차가 없으면 실제 장애에서 무력

---

## Gotchas

- PITR 복구는 원본 인스턴스를 덮어쓰지 않고 **새 인스턴스를 생성**한다. 기존 인스턴스에서 새 인스턴스로 트래픽을 전환하는 cutover 절차가 별도로 필요하다
- 복구된 인스턴스는 **기본 parameter group**으로 붙을 수 있다. 커스텀 parameter group, option group을 원본과 동일하게 재적용해야 한다
- 복구 후 태그, Security Group, 서브넷 그룹, 연결 문자열(endpoint) 업데이트가 누락되는 사례가 빈번하다. runbook에 체크리스트로 포함한다
- RDS 자동 백업 보존을 0으로 설정하면 PITR이 비활성화된다. 기본값(7일)을 반드시 확인한다
- Cross-region 스냅샷 복사는 수동 또는 자동화(Lambda/EventBridge)로 구성해야 한다. 자동 백업은 동일 리전에만 저장된다
