# /api-verify 리포트 — dev · 2026-09-02 14:22

## 실행 요약

| 대상 | PASS | FAIL | 보류 | flaky | 판정 불가 | 환경 | 종료 코드 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 3 | 2 | 0 | 0 | 2 | dev | 4 |

PASS · FAIL 은 계약 판정(Hurl)을, 판정 불가는 경로 간 불변식 판정 줄을 센다.
`products.create` 는 케이스와 스냅샷이 없어 대상에서 빠졌다.

## 계약 실패 — 게이트 파괴

| 엔드포인트 | 축 | 내용 |
| --- | --- | --- |
| `products.inventory` | status | `200` 을 기대했는데 `503 Service Unavailable` |
| `products.inventory` | schema | 필수 필드 `$.data.availableQty` 삭제 |
| `users.me` | value | `$.tier` 가 `platinum` — 허용 값 `gold` · `silver` · `bronze` 밖 |

## 경로 간 불변식 판정 줄

- orders.list: $.meta.total=47 · len($.data)=2 → PASS
- products.list: $.meta.total=(없음) · len($.data)=3 → 판정 불가
- products.inventory: $.data.onHand=(없음) · $.data.availableQty=(없음) → 판정 불가

판정 불가 두 줄은 게이트를 깨지 않는다. `products.list` 의 `$.meta.total` 은 계약에서 옵션이라 필드 삭제로도 잡히지 않는다.
