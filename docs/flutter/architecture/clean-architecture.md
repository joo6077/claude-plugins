---
title: Clean Architecture
version: 0.1.0
last_updated: 2026-04-05
---

# Clean Architecture

Flutter Clean Architecture 레이어 분리, Repository 패턴, UseCase의 적절한 사용, DI 전략, 디렉토리 구조를 다룬다.

---

## 원칙

### 1. 레이어 의존 방향은 Presentation → Domain → Data 단방향

바깥 레이어(UI, Data)가 안쪽 추상화(Domain)에 의존하게 만든다. Flutter 공식 아키텍처 가이드도 UI/Data 분리를 기본으로 두고 Domain layer를 선택적으로 둔다.

> **출처:** [Flutter App Architecture Guide](https://docs.flutter.dev/app-architecture/guide)

### 2. Repository는 앱 데이터의 source of truth

외부 API/DB/plugin 접근은 Service/DataSource로 분리하고, Repository는 여러 DataSource를 조합하여 도메인 모델을 반환한다.

> **출처:** [Flutter App Architecture Guide](https://docs.flutter.dev/app-architecture/guide)

### 3. UseCase는 필수가 아닌 선택

복잡한 비즈니스 규칙이 있을 때 Domain layer에 둔다. 간단한 CRUD 앱에선 과설계. 모든 액션에 UseCase를 강제하면 파일 수만 폭발한다.

> **출처:** [Flutter App Architecture Guide](https://docs.flutter.dev/app-architecture/guide)

### 4. UI는 feature-first, data/domain은 layer-first 혼합

대형 앱에서 가장 실용적인 조합. Flutter 공식 케이스 스터디도 `lib/ui/`, `lib/domain/`, `lib/data/`, `lib/routing/`으로 분리.

> **출처:** [Flutter Architecture Case Study](https://docs.flutter.dev/app-architecture/case-study)

### 5. DI는 get_it 또는 Riverpod 중 하나를 명확히 채택

Widget에서 repository/service를 직접 new하지 않는다. get_it은 service locator, Riverpod은 provider graph 기반.

> **출처:** [get_it on pub.dev](https://pub.dev/packages/get_it)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| get_it 조회 복잡도 | O(1) |
| Flutter 공식 구조 예시 | lib/ui, lib/domain, lib/data, lib/routing, test/, testing/ |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| Repository가 DTO/DioException/JSON Map을 UI로 노출 | transport 세부사항이 UI까지 전파 |
| 모든 액션마다 UseCase 클래스 강제 | 파일 수 폭발, 변경 비용 증가 |
| feature-first와 layer-first 혼합 규칙 없음 | 탐색성 붕괴 |
| Widget 안에서 repository/service 직접 new | 테스트 불가, DI 원칙 위반 |

---

## Gotchas

- **Clean Architecture 과설계 주의** — 작은 앱에 과도한 추상화는 변경 비용을 오히려 증가시킨다.
- **Riverpod ≠ 아키텍처 분리** — 상태관리 도구와 Clean Architecture는 별개다. Riverpod을 써도 Domain/Data 경계는 자동으로 생기지 않는다.
