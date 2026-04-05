---
title: GraphQL
version: 0.1.0
last_updated: 2026-04-04
---

# GraphQL

Versionless evolution, nullability, 페이지네이션, N+1 해결, demand control, federation, subscription, 에러 처리를 다룬다.

---

## 원칙

### 1. Versionless evolution이 기본이다

스키마에 버전 번호를 붙이지 않는다. field/type 추가와 `@deprecated(reason:)` 디렉티브로 진화한다. 삭제는 실제 사용량이 0에 수렴한 후에만 수행한다. REST와 달리 클라이언트가 필요한 필드만 요청하므로 추가는 breaking change가 아니다.

> **출처:** [GraphQL — Schema Design Best Practices](https://graphql.org/learn/schema-design/)

### 2. Nullability는 보수적으로 설정한다

non-null(`!`)로 선언한 필드가 런타임에 null을 반환하면 해당 필드뿐 아니라 상위 nullable 부모까지 null-bubble이 전파된다. "이 필드는 절대 null이 아니다"는 강한 보장이므로, 확신이 없으면 nullable로 두고 클라이언트가 처리하게 한다.

> **출처:** [GraphQL — Schema Design Best Practices](https://graphql.org/learn/schema-design/), [GraphQL Spec — October 2021](https://spec.graphql.org/October2021/)

### 3. 대량 리스트는 cursor-based connection을 사용한다

Relay 스타일 connection(`edges`, `node`, `cursor`, `pageInfo`)을 표준으로 채택한다. offset pagination은 공개 스키마 표준으로 적합하지 않다. connection은 양방향 탐색, 총 개수 힌트, 커서 기반 안정적 순회를 제공한다.

> **출처:** [GraphQL — Pagination](https://graphql.org/learn/pagination/)

### 4. N+1 문제는 DataLoader로 해결한다

DataLoader는 요청(request) 범위에서 동일 리소스에 대한 개별 fetch를 배치(batch)로 묶고, 같은 키를 캐싱하여 중복 조회를 제거한다. resolver마다 개별 DB 쿼리를 실행하면 필드 수에 비례하여 쿼리가 폭증한다.

> **출처:** [graphql/dataloader](https://github.com/graphql/dataloader)

### 5. Demand control은 여러 기법을 조합한다

depth limiting, breadth/alias limiting, batch query limiting, complexity analysis를 함께 적용한다. 단일 기법만으로는 우회가 가능하다. complexity budget은 필드별 가중치를 부여하여 쿼리 비용을 사전에 계산한다.

> **출처:** [GraphQL — Security](https://graphql.org/learn/security/)

### 6. Persisted query/trusted documents로 성능과 보안을 확보한다

클라이언트가 전체 쿼리 문자열 대신 해시(APQ ID)를 전송하여 네트워크 비용을 줄이고, 서버는 allowlist에 등록된 쿼리만 실행한다. first-party 앱은 빌드 시 쿼리를 추출하여 allowlist를 생성한다.

> **출처:** [GraphQL — Security](https://graphql.org/learn/security/)

### 7. Federation은 단일 supergraph 계약, 다수 subgraph로 운영한다

각 팀이 독립적으로 subgraph를 개발·배포하되, composition(스키마 병합)의 안정성을 최우선으로 관리한다. entity ownership을 명확히 하고, `@key` 디렉티브로 subgraph 간 참조를 정의한다.

> **출처:** [Apollo Federation](https://www.apollographql.com/docs/federation/)

### 8. Subscription은 신중하게 사용한다

subscription root field는 정확히 1개만 허용한다. stateful transport(WebSocket)와 pub/sub 인프라가 필요하므로 query/mutation보다 운영 비용이 높다. 폴링으로 충분한 경우 subscription을 쓰지 않는다.

> **출처:** [GraphQL Spec — October 2021](https://spec.graphql.org/October2021/)

### 9. 에러는 errors[] + partial data로 전달한다

GraphQL 응답은 `data`와 `errors`를 동시에 포함할 수 있다. request error(파싱/검증 실패)는 `data`가 없고, execution error(일부 resolver 실패)는 `data`에 부분 결과와 함께 `errors`가 온다. 에러를 200 + 불투명 메시지로만 반환하면 클라이언트가 부분 렌더링을 할 수 없다.

> **출처:** [GraphQL Spec — October 2021](https://spec.graphql.org/October2021/)

### 10. Breaking change는 schema diff + 실제 operation usage로 감지한다

스키마 diff만으로는 사용되지 않는 필드 삭제를 불필요하게 차단하고, usage만으로는 새로 추가된 클라이언트를 놓칠 수 있다. CI에서 schema check를 실행하여 실제 트래픽 기반으로 안전성을 판단한다.

> **출처:** [Apollo GraphOS — Schema Checks Reference](https://www.apollographql.com/docs/graphos/platform/schema-management/checks/reference)

---

## 수치 기준

| 항목 | 값 |
|------|-----|
| Subscription root field 수 | 정확히 1개 |
| APQ ID 형식 | SHA-256 hash |
| Depth limit 운영 시작점 | 8~12 |
| Batch query limit 운영 시작점 | 5~20 |
| Complexity budget 운영 시작점 | 100~1000 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| Offset pagination을 공개 스키마 표준으로 | 데이터 변경 시 row 누락·중복, 대규모 offset 성능 저하. |
| DataLoader를 전역 singleton으로 | cross-request 캐시 오염, 메모리 누수, 인증 경계 무시. |
| Public API에 introspection/batch/alias/depth 모두 개방 | DoS 공격 표면 최대화. 하나만 제한해도 우회 가능. |
| Federation entity ownership 불명확 | subgraph 간 충돌, composition 실패, 책임 소재 불분명. |
| 에러를 200 + opaque message만으로 반환 | 부분 렌더링 불가, 에러 분류·모니터링 불가. |

---

## Gotchas

- **Introspection 비활성화는 보안 보조일 뿐 allowlist를 대체하지 못한다.** introspection을 끄더라도 공격자가 필드명을 추측하거나 유출된 스키마로 악의적 쿼리를 보낼 수 있다. trusted documents/persisted query가 근본 대책이다.
- **errors가 있어도 data가 함께 올 수 있다.** execution error는 실패한 필드만 null로 만들고 나머지는 정상 반환한다. 클라이언트는 errors 존재 여부만으로 전체 실패를 판단하면 안 된다.
- **DataLoader는 요청 범위 캐시이다.** 한 HTTP 요청 내에서만 배치와 캐싱이 동작한다. cross-request 캐싱이 필요하면 별도 캐시 레이어(Redis 등)를 사용해야 한다.
