---
title: 테스팅
version: 0.2.0
last_updated: 2026-08-13
---

# 테스팅

테스트 피라미드, 테스트 유형별 비율과 전략, contract testing, 테스트 더블, DB 테스트, 통합 테스트의 타깃 증명, 부하 테스트, 커버리지 기준을 다룬다.

---

## 원칙

### 1. 테스트 피라미드를 따른다

단위 테스트를 가장 많이, 통합 테스트를 중간, E2E 테스트를 최소로 유지한다. 이 비율이 뒤집힌 "아이스크림 콘"은 느리고 깨지기 쉬운 테스트 스위트를 만든다. Google 엔지니어링 팀 기준 권장 비율은 **단위 70% / 통합 20% / E2E 10%**이다. 피라미드 상단으로 갈수록 실행 시간, 유지 비용, 비결정성(flakiness)이 기하급수적으로 증가한다.

> **출처:** [Martin Fowler — The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

### 2. 각 테스트 유형의 역할을 구분한다

단위 테스트는 밀리초 단위로 빠르고 외부 의존성 없이 격리 실행한다. 통합 테스트는 실제 DB, 메시지 큐 등 실제 의존성과의 상호작용을 검증한다. E2E 테스트는 사용자 시나리오 전체를 브라우저/API 레벨에서 검증하며, 핵심 플로우(happy path)에 집중한다.

> **출처:** [Martin Fowler — The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

### 3. Contract testing으로 서비스 간 계약을 검증한다

마이크로서비스 환경에서 consumer-driven contract testing은 서비스 간 API 계약이 깨지지 않음을 보장한다. Consumer가 기대하는 요청/응답 형태를 Pact 파일로 정의하고, Provider가 이를 검증한다. 통합 테스트 환경 없이도 서비스 간 호환성을 확인할 수 있다.

> **출처:** [Pact Documentation](https://docs.pact.io/)

### 4. 테스트 더블을 목적에 맞게 선택한다

**Mock**은 행위를 검증한다(호출 여부, 호출 횟수, 인자). **Stub**은 미리 정해진 응답을 반환한다. **Fake**는 경량 구현체다(인메모리 DB 등). **Spy**는 실제 객체를 감싸서 호출을 기록한다. Mock 과다 사용은 구현에 결합된 깨지기 쉬운 테스트를 만든다 — 가능하면 상태 기반 검증(stub/fake)을 우선한다.

> **출처:** [Martin Fowler — TestDouble](https://martinfowler.com/bliki/TestDouble.html)

### 5. DB 테스트는 실제 데이터베이스로 실행한다

인메모리 DB(H2 등)는 실제 DB와 동작이 다르다. Testcontainers는 Docker로 실제 DB(PostgreSQL, MySQL, MongoDB 등)를 테스트 시 자동 생성/폐기한다. 테스트 간 격리는 트랜잭션 롤백 또는 테스트별 스키마 생성으로 보장한다.

> **출처:** [Testcontainers](https://testcontainers.com/)

### 6. 부하 테스트로 성능 기준선을 설정한다

k6는 JavaScript로 시나리오를 작성하고 CLI에서 실행하는 부하 테스트 도구다. 기본 설정: VU(virtual user) 10~50명, duration 30초~5분으로 시작하여 점진적으로 늘린다. Artillery도 YAML 기반으로 유사한 기능을 제공한다. 성능 기준선(p95 응답 시간, 에러율)을 CI에 통합하면 성능 회귀를 조기에 탐지한다.

> **출처:** [Grafana k6 Documentation](https://grafana.com/docs/k6/latest/)

### 7. 커버리지는 지표이지 목표가 아니다

커버리지 80%를 넘으면 수확체감이 발생한다. 100% 커버리지가 버그 없음을 보장하지 않는다 — 코드 경로를 실행한 것이지 결과의 정확성을 검증한 것이 아니다. 커버리지보다 **mutation testing**(돌연변이 테스트)이 테스트 품질을 더 정확히 측정한다. 커버리지를 KPI로 설정하면 의미 없는 assertion 없는 테스트가 양산된다.

> **출처:** [Martin Fowler — TestCoverage](https://martinfowler.com/bliki/TestCoverage.html)

### 8. 통합 테스트는 "실 의존성" 과 "실 대상" 을 모두 만족해야 한다

두 조건은 **다른 축**이다. 실제 DB/브로커를 띄웠더라도 테스트가 검증 대상 로직(SQL 술어 · 가드
분기 · 핸들러 파이프라인)을 **독립적으로 재작성**했다면 구현과의 결합이 0 이라, 구현에서 그 로직을
삭제해도 테스트는 통과한다. 통합 테스트로 계상하려면 production 심볼(함수 · 리포지토리 · 핸들러)
또는 실제 실행 바이너리/로컬 기동 provider 를 호출해야 한다.

- provider 검증 방식(요청을 로컬 기동 provider 에 재생하고 실제 응답을 비교)도 유효한 타깃
  증명이다. 다만 요청 본문을 추출·검증하기 **전 레이어를 stub 하면 어떤 garbage body 도 통과**
  하므로 stub 위치를 함께 확인한다.
- 동시성 가드 · 인증/인가 guard · 멱등 arbiter 같은 핵심 guard 는 그 지점을 무력화했을 때
  테스트가 **FAIL 해야** 의미가 있다. 결함을 주입했는데 통과하면 그 테스트는 결함을 잡지 못한다.
- 다만 mutation/negative control 을 전 코드베이스에 적용하지 마라 — 비용이 크다. 위 핵심 guard 로
  범위를 한정한다.

> **출처:** [Pact — Provider verification](https://docs.pact.io/provider), [PIT — Mutation testing](https://pitest.org/), [Testcontainers — Getting started](https://testcontainers.com/getting-started/)

---

## 수치 기준

| 항목 | 기준값 | 비고 |
|------|--------|------|
| 테스트 비율 (Google 기준) | 단위 70% / 통합 20% / E2E 10% | 아이스크림 콘 방지 |
| 커버리지 실용 상한 | 80% | 초과 시 수확체감 |
| 단위 테스트 실행 시간 | 개별 < 10ms, 전체 < 1분 | 느리면 개발 피드백 루프 저하 |
| k6 기본 VU | 10~50 VU, 30초~5분 | 점진적으로 증가시킴 |
| Pact contract 파일 | consumer당 1개 | provider 측에서 검증 |
| Testcontainers 기동 시간 | PostgreSQL ~3초, MySQL ~5초 | CI 환경에 따라 편차 |

---

## 안티패턴

### 아이스크림 콘 (E2E 과다)

E2E 비율이 단위 테스트보다 높으면 테스트 스위트가 느리고, 비결정적이며, 유지 비용이 높다. E2E는 핵심 플로우에만 한정하고 나머지는 하위 레벨에서 검증한다.

### Mock 과다 (가짜 그린)

모든 의존성을 mock하면 테스트가 항상 통과하지만 실제 통합 문제를 잡지 못한다. Mock은 외부 서비스 경계에만 사용하고, 내부 모듈 간에는 실제 구현을 사용한다.

### 로직을 재작성한 "통합" 테스트

실 DB 를 띄워놓고 테스트가 SQL 을 직접 다시 작성해 "일반적인 동작" 만 확인하면, 구현의 가드를 지워도 통과한다. 의존성은 진짜인데 대상이 가짜인 경우다. 테스트는 구현 심볼을 호출해야 한다.

### 테스트 간 상태 공유

테스트가 공유 DB 레코드나 전역 변수에 의존하면 실행 순서에 따라 결과가 달라진다. 각 테스트는 독립적으로 setup/teardown해야 한다.

### 커버리지 강박

커버리지 수치 자체를 목표로 삼으면 getter/setter 테스트, assertion 없는 테스트 등 의미 없는 코드가 양산된다. 비즈니스 로직과 엣지 케이스에 집중한다.

---

## Gotchas

- **Testcontainers는 CI에서 Docker 필요** — GitHub Actions는 기본 지원하지만, 일부 CI 환경(CircleCI machine executor 아닌 경우 등)에서는 Docker-in-Docker 설정이 필요하다
- **Mock이 실제 API와 drift** — Mock을 수동 관리하면 실제 API가 변경되어도 테스트가 통과한다. Contract testing이나 자동 생성 mock(OpenAPI spec 기반)으로 방지
- **Flaky test는 즉시 수정 또는 격리** — 비결정적 테스트를 방치하면 팀이 테스트 실패를 무시하는 습관이 생긴다. 재현 불가능하면 quarantine 처리 후 별도 추적
