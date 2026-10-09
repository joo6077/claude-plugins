# /api-verify 리포트 — dev · 2026-09-02 14:22

## 실행 요약

| 대상 | PASS | FAIL | 보류 | flaky | 판정 불가 | 환경 | 종료 코드 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 3 | 2 | 1 | 1 | 2 | dev | 4 |

PASS · FAIL 은 계약 판정(Hurl)을, 판정 불가는 경로 간 불변식 판정 줄을 센다. 보류와 flaky 는 FAIL 2 건 안에 든 실패를 따로 한 번 더 센 것이다.
`products.create` 는 케이스와 스냅샷이 없어 대상에서 빠졌다.

## 계약 실패 — 게이트 파괴

| 엔드포인트 | 축 | 내용 |
| --- | --- | --- |
| `products.inventory` | status | `200` 을 기대했는데 `503 Service Unavailable` |
| `products.inventory` | schema | 필수 필드 `$.data.availableQty` 삭제 |

`products.inventory` 는 확인 재실행 한 번에서 통과해 flaky(`flaky-confirmed`)로도 센다. 처음 실패 기록은 지우지 않는다.

## 계약 실패 — 보류 (게이트를 깨지 않음)

| 엔드포인트 | 축 | 내용 |
| --- | --- | --- |
| `users.me` | value | `$.tier` 가 `platinum` — 허용 값 `gold` · `silver` · `bronze` 밖 |

`users.me` 계약은 baseline 이 아직 `pending` 이라 실패를 적되 게이트를 깨지 않는다.

## 경로 간 불변식 판정 줄

- orders.list: $.meta.total=47 · len($.data)=2 → PASS
- products.list: $.meta.total=(없음) · len($.data)=3 → 판정 불가
- products.inventory: $.data.onHand=(없음) · $.data.availableQty=(없음) → 판정 불가

판정 불가 두 줄은 게이트를 깨지 않는다. `products.list` 의 `$.meta.total` 은 계약에서 옵션이라 필드 삭제로도 잡히지 않는다.
