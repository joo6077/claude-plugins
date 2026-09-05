---
title: 다중 샘플과 페이지네이션 변동성
version: 0.1.0
last_updated: 2026-09-04
---

# 다중 샘플과 페이지네이션 변동성

계약을 승격하기 전에 샘플을 몇 개, 어디까지 모아야 하는지에 대한 규칙.
컬렉션 응답은 한 페이지만 보면 계약이 아니라 우연을 봉인하게 된다.

---

## 원칙

### 1. 단일 응답은 계약이 아니라 후보다

quicktype, GenSON, json-schema-inferrer 는 모두 여러 샘플을 합쳐 required, nullable, union, 공통 필드를 판단한다.
변동이 있는 API 는 반복 호출과 페이지 샘플을 먼저 모은 뒤에 추출한다.
샘플 예산을 정하지 않으면 첫 응답의 우연한 형태가 그대로 baseline 이 된다.

> **출처:** [quicktype](https://quicktype.io/), [GenSON](https://github.com/wolverdude/GenSON), [json-schema-inferrer](https://github.com/saasquatch/json-schema-inferrer)

### 2. prod 샘플링은 safe method 로 제한한다

prod 에서 반복 샘플링할 때는 서버 상태를 바꾸지 않는 method 만 쓴다.
HTTP 는 GET·HEAD·OPTIONS·TRACE 를 safe method 로 정의한다.
이 킷의 prod read-only 범위는 **아직 미확정이며 기본값은 GET/HEAD/OPTIONS** 다(2026-09-04 결정) — 확장은 사용자 명시 승인이 있을 때만.

> **출처:** [RFC 9110 §9.2.1 Safe Methods](https://datatracker.ietf.org/doc/html/rfc9110)

### 3. 페이지네이션 프로토콜을 먼저 식별한다

`nextLink`, `@odata.nextLink`, GraphQL `edges`/`pageInfo`, Stripe `data`/`has_more` 같은 envelope 를 먼저 찾는다.
컬렉션의 계약은 페이지 본문이 아니라 **페이지네이션 프로토콜** 이다.
프로토콜을 모른 채 본문만 봉인하면 종료 조건 변경 같은 실제 회귀를 놓친다.

> **출처:** [Microsoft Graph paging](https://learn.microsoft.com/en-us/graph/paging), [Relay Connections](https://relay.dev/graphql/connections.htm), [Stripe pagination](https://docs.stripe.com/api/pagination)

### 4. cursor 는 opaque 다

cursor, `$skiptoken`, `nextLink` 는 불투명 값으로 취급한다.
반환된 전체 URL 또는 cursor 를 그대로 다음 요청에 쓰고, 파싱·수정·합성하지 않는다.
토큰 내부 구조는 계약이 아니며 사전 공지 없이 바뀐다.

> **출처:** [Microsoft Graph paging](https://learn.microsoft.com/en-us/graph/paging), [Data API builder `$after`](https://learn.microsoft.com/en-us/azure/data-api-builder/keywords/after-rest), [Relay Connections](https://relay.dev/graphql/connections.htm)

### 5. 안정 정렬이 있어야 순서 계약을 건다

배열 index assertion 과 컬렉션 exact diff 는 안정 정렬이 보장될 때만 허용한다.
GraphQL connection 은 페이지 간 edge 순서 일관성을 요구하고, Microsoft 가이드라인도 모든 페이지에 동일한 filter/sort 를 쓰라고 규정한다.
정렬 보장이 없으면 순서는 pin 대상이 아니라 variance 신호다.

> **출처:** [Relay Connections](https://relay.dev/graphql/connections.htm), [Microsoft Azure API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md)

### 6. 승격 전에 변동성을 점수화한다

path 별로 presence, type set, scalar 값 churn, 배열 길이, 순서 churn 을 점수화한 뒤 계약 강도를 정한다.
snapshot 도구들의 scrubber/redaction 관례가 같은 순서 — 비결정 출력을 먼저 안정화하고 그다음 비교 — 를 따른다.
점수 없이 승격하면 partial 로 충분한 필드에 pin 이 붙어 오탐이 쌓인다.

> **출처:** [Jest Snapshot Testing](https://jestjs.io/docs/snapshot-testing), [insta redactions](https://insta.rs/docs/redactions/), [ApprovalTests Scrubbers](https://approvaltestscpp.readthedocs.io/en/latest/generated_docs/explanations/Scrubbers.html)

### 7. optionality 는 전 페이지 item 집합에서 계산한다

item 필드의 required/optional 은 첫 페이지가 아니라 수집한 모든 페이지의 item 집합으로 판정한다.
Microsoft 는 snapshot 보장이 없는 paginated collection 에서 skip/duplicate 가 발생할 수 있다고 경고한다 — 즉 페이지마다 관측 모집단이 다르다.

> **출처:** [Microsoft Azure API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md), [GenSON](https://github.com/wolverdude/GenSON)

### 8. 대표 페이지를 나눠서 남긴다

첫 페이지만 보면 종료 envelope 차이(`nextLink` 부재, `has_more=false`)를 놓친다.
가능한 경우 first, next 중 최소 하나, terminal 세 종류를 구분해 증거로 남긴다.

> **출처:** [Microsoft Graph paging](https://learn.microsoft.com/en-us/graph/paging), [Stripe pagination](https://docs.stripe.com/api/pagination)

### 9. 컬렉션 계약은 세 조각으로 분리한다

envelope schema, item schema, pagination marker semantics 를 각각 따로 계약한다.
페이지 길이나 전체 item 순서는 API 가 snapshot 또는 안정 정렬을 보장할 때만 exact assertion 으로 승격한다.

> **출처:** [Stripe pagination](https://docs.stripe.com/api/pagination), [Relay Connections](https://relay.dev/graphql/connections.htm), [Azure Service Design Considerations](https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md)

---

## 수치 기준

| 항목 | 값 | 근거 |
|------|-----|------|
| Stripe list `limit` | default `10`, 허용 `1..100` | [Stripe pagination](https://docs.stripe.com/api/pagination) |
| Microsoft Graph `/users` 서버 기본 page size | `100` | [Microsoft Graph paging](https://learn.microsoft.com/en-us/graph/paging) |
| Azure REST `nextLink` 등장 시점 | 결과가 클 때 반환, 문서상 보통 `>1000` items | [Azure REST API](https://learn.microsoft.com/en-us/rest/api/azure/) |
| 페이지네이션 종료 신호 | `nextLink`/`@odata.nextLink` 부재 · Stripe `has_more=false` · GraphQL `hasNextPage=false` | [Graph](https://learn.microsoft.com/en-us/graph/paging), [Stripe](https://docs.stripe.com/api/pagination), [Relay](https://relay.dev/graphql/connections.htm) |
| 일반 샘플 예산 | 최소 `3` captures, 최대 `5` pages 또는 `500` items | 추론 — 다중 샘플 추론 도구들의 교집합 판정에 필요한 하한 |
| 수집 중지 후보 | 연속 `2` 페이지에서 신규 path/type 없음 | 추론 — 변동성 수렴 신호 |
| 컬렉션 exact 자격 | 안정 정렬/cursor 존재, duplicate stable id `0`, ordering variance `0`, normalized item schema variance `0` | 추론 — 네 조건 중 하나만 깨져도 매 실행 실패 |
| prod 샘플링 기본 method | `GET` · `HEAD` · `OPTIONS` | 2026-09-04 결정 (범위 미확정) — RFC 9110 safe methods 부분집합 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 첫 페이지의 item 개수를 전체 컬렉션 길이로 봉인 | 서버 page size 를 컬렉션 크기로 착각한다. 데이터가 늘어도 줄어도 감지 못한다 |
| offset/skip 기반 페이지를 live-changing 컬렉션의 exact diff 기준으로 사용 | 항목이 삽입/삭제되면 페이지 경계가 밀려 매번 diff 가 난다 |
| `nextLink` 에서 token 만 뜯어 다른 query 에 붙임 | cursor 는 opaque 다. 내부 구조가 바뀌면 조용히 잘못된 페이지를 읽는다 |
| 정렬 보장 없는 컬렉션에 index 기반 pin 사용 | `$.data[0].id` 같은 assertion 이 정상 동작에도 실패한다 |
| auto-pagination helper 결과만 저장하고 페이지별 raw evidence 를 버림 | envelope 와 종료 marker 증거가 사라져 페이지네이션 회귀를 진단할 수 없다 |

---

## Gotchas

- **`nextLink: null` 을 표준 종료 marker 로 일반화하지 않는다** — Microsoft Azure 가이드라인은 마지막 페이지에서 `nextLink` 를 아예 생략하라고 한다. 부재와 null 은 다른 신호다.
- **GraphQL backward pagination 에서 순서를 뒤집지 않는다** — `last`/`before` 도 forward 와 같은 logical order 를 유지해야 한다. 역순으로 저장하면 페이지 간 비교가 깨진다.
- **skip/duplicate 는 item schema 위반이 아니다** — snapshot 보장이 없는 live collection 에서는 정상 현상이며, 컬렉션 variance 신호로 분류해야 한다. schema 실패로 올리면 오탐이다.
- **`nextLink` 의 absolute/relative 정책은 provider 마다 다르다** — 증거에는 원문을 그대로 남기고, 계약에는 provider 별 canonical 규칙을 따로 기록한다.
