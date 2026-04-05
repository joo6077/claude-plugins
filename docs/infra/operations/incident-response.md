---
title: 인시던트 대응
version: 0.1.0
last_updated: 2026-04-04
---

# 인시던트 대응

Severity 분류, 온콜 체계, 역할 분리, Runbook, Postmortem, RCA, Status Page, 복구 우선순위를 다룬다.

---

## 원칙

### 1. Severity는 사용자/비즈니스 영향 기준으로 분류한다

기술적 원인(서버 다운, DB 락)이 아니라 사용자가 체감하는 영향 범위와 심각도로 분류한다. 기술 원인 기준으로 분류하면 영향이 큰 장애를 과소평가하거나, 영향이 작은 문제에 과잉 대응하게 된다.

> **출처:** [Atlassian — Severity Levels](https://www.atlassian.com/incident-management/kpis/severity-levels)

### 2. 온콜은 primary/secondary 분리하고 handoff 시간을 명시한다

Primary가 응답하지 못할 경우 secondary로 자동 에스컬레이션되어야 한다. handoff 시간(교대 시점)을 명확히 정의하여 "누가 지금 담당인가"에 모호함이 없어야 한다. 온콜 부담은 팀 전체에 공정하게 분배한다.

> **출처:** [Google SRE Book — Being On-Call](https://sre.google/sre-book/being-on-call/)

### 3. 탐지→선언→지휘→커뮤니케이션 역할을 분리한다

Incident Commander(IC)가 의사결정과 조율을 맡고, Communicator가 이해관계자 업데이트를 담당한다. IC가 직접 디버깅에 뛰어들면 전체 조율이 중단된다. 역할이 명확해야 병렬 작업이 가능하다.

> **출처:** [Atlassian — Incident Response Roles and Responsibilities](https://www.atlassian.com/incident-management/incident-response/roles-responsibilities)

### 4. Runbook은 실행 절차다

개념 설명이 아니라 "따라 하면 자동화 가능한 수준"의 단계별 명령 시퀀스여야 한다. 판단이 필요한 지점은 분기 조건을 명시한다. Runbook이 실행 불가능한 산문이면 장애 시 아무도 참조하지 않는다.

> **출처:** [Google SRE Book — Service Best Practices](https://sre.google/sre-book/service-best-practices/)

### 5. Postmortem은 blameless로 수행한다

사람의 실수를 비난하는 대신, 그 실수를 허용한 환경과 안전장치 부재를 고친다. Blame culture가 형성되면 장애를 숨기거나 축소 보고하게 되어 조직 학습이 중단된다.

> **출처:** [Google SRE Book — Service Best Practices](https://sre.google/sre-book/service-best-practices/)

### 6. RCA는 "왜 방어선이 실패했는가"에 집중한다

직접 원인(what)이 아니라 방어선 실패(why)를 추적한다. 5 Whys + timeline 조합으로 인과 관계를 시간순으로 재구성한다. "서버가 죽었다"가 아니라 "왜 자동 복구가 작동하지 않았는가"가 핵심 질문이다.

> **출처:** [Atlassian — 5 Whys Analysis](https://www.atlassian.com/software/confluence/templates/5-whys-analysis/)

### 7. Status page를 단일 진실원천(Single Source of Truth)으로 운영한다

내부 슬랙, 이메일, 전화 등 여러 채널에 장애 상태가 흩어지면 혼란이 가중된다. Status page 하나를 공식 채널로 지정하고, 모든 업데이트를 여기에 먼저 게시한다. 고객, 내부 팀, 경영진 모두 같은 정보를 본다.

> **출처:** [Statuspage — Developer API](https://developer.statuspage.io/)

### 8. 복구 우선순위: data integrity > core availability > noncritical features

데이터 무결성이 최우선이다. 데이터가 손상된 상태로 서비스를 복구하면 피해가 확산된다. 핵심 기능의 가용성이 그다음이고, 부가 기능은 마지막이다. 이 순서를 사전에 합의해두지 않으면 장애 시 우선순위 논쟁으로 시간을 소모한다.

> **출처:** [Google SRE Book — Service Best Practices](https://sre.google/sre-book/service-best-practices/)

---

## 수치/기준값

- **SEV1**: 전면 장애 또는 데이터 손상. 즉시 대응, 전사 에스컬레이션
- **SEV2**: 핵심 기능 중대 저하. 우회 불가 또는 매우 어려움
- **SEV3**: 부분 기능 저하, 우회 가능
- **SEV4**: 경미한 이슈, 사용자 영향 최소
- Statuspage 상태 흐름: investigating → identified → monitoring → resolved
- SEV1: 15분 내 첫 공지, 이후 30분 cadence로 업데이트
- SEV2: 30분 내 첫 공지, 이후 60분 cadence로 업데이트

---

## 안티패턴

- **원인 찾은 뒤에야 공지**: 사용자와 이해관계자는 원인 파악 전에도 "인지하고 있다"는 사실을 알아야 한다. 공지 지연은 신뢰를 훼손한다
- **IC가 직접 디버깅에 몰두**: 조율자가 사라지면 병렬 작업이 중단되고 커뮤니케이션이 끊긴다
- **Postmortem을 개인 실수 보고서로 작성**: Blame 문화를 강화하여 향후 장애 은폐를 유발한다
- **Runbook을 개념 문서로 작성**: 장애 시 읽을 수 없는 문서는 존재하지 않는 것과 같다. 실행 가능한 단계여야 한다
- **Chaos Engineering을 무작위 실험으로 수행**: steady state 가설과 abort condition 없이 장애를 주입하면 그냥 장애다

---

## Gotchas

- SEV 기준을 "내부 긴장도"로 두면 조직마다, 팀마다 다르게 해석한다. 사용자 영향 범위와 비즈니스 지표로 객관화해야 한다
- Status page에 추측성 문구("아마 곧 복구될 것")를 쓰면 복구 지연 시 신뢰가 더 크게 훼손된다. 확인된 사실만 게시한다
- RCA에 timeline이 빠지면 "왜 그 시점에 그 판단을 했는가"를 이해할 수 없어 교훈이 남지 않는다
- Litmus/Gremlin 같은 Chaos Engineering 도구는 도구일 뿐이다. steady state 정의 + abort condition 설계 없이 사용하면 의도치 않은 실제 장애를 유발한다
