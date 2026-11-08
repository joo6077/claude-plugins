# 기록 형식 — perf.json

비교 하나에 `perf.json` 하나를 둔다. `scripts/perf_compare.py check` 가 검사하고 `report` 가 같은 폴더에 `perf-report.html` 을 쓴다.
스크립트는 아래 표에 없는 키를 오타로 보고 막는다. 표에 키를 더하려면 스크립트의 `*_FIELDS` 도 같이 고친다.
예시는 `perf-kit/evals/perf-compare/example/perf.json` 이다.

## 케이스

| 키 | 필수 | 형식 | 뜻 |
| --- | --- | --- | --- |
| `id` | 예 | 문자열 | `PERF-001`. 시나리오 보고서와 같은 폴더에 두면 그 케이스 번호를 쓴다 |
| `title` | 예 | 문자열 | 기대 결과 한 문장 |
| `question` | 예 | 문자열 | 이 비교가 답하려는 질문 |
| `meta` | 예 | 객체 | `date` · `device` · `a` · `b`. `a` · `b` 는 `label`(보고서에 쓰는 이름) · `ref`(커밋 · 빌드) |
| `fixed` | 예 | 문자열 목록 | 고정한 조건. 하나 이상 |
| `order` | 예 | `randomized` · `duet` · `interleaved` · `blocked` | 측정 순서 — `experiment-design.md` §순서 |
| `alpha` | 아니오 | 숫자 | 유의수준. 기본 0.05 |
| `metrics` | 예 | 객체 목록 | 아래 표 |
| `equivalence` | 아니오 | 객체 목록 | `name` · `same`(true · false) · `seen` |
| `budgets` | 아니오 | 객체 목록 | `metric` · `max` 나 `min` 중 하나 · `why` |
| `cost` | 아니오 | 객체 | `currency` · `items` |

## 지표

| 키 | 필수 | 형식 | 뜻 |
| --- | --- | --- | --- |
| `key` | 예 | 문자열 | 겹치지 않는 영문 이름. `budgets` · `cost` 가 이 이름으로 가리킨다 |
| `name` | 예 | 문자열 | 보고서에 쓰는 이름 |
| `unit` | 예 | 문자열 | `ms` · `bytes` · `%` · `MB` · `단계` |
| `better` | 예 | `lower` · `higher` | 어느 쪽이 좋은가 |
| `role` | 예 | `target` · `control` | 목표 지표 · 대조 지표 |
| `warmup` | 아니오 | 0 이상 정수 | `a` · `b` 앞에서 뺄 예열 표본 수. 기본 0 |
| `min_effect_pct` | 아니오 | 0 이상 숫자 | 이보다 작은 변화는 `차이 미미`. 기본 5 |
| `source` | 예 | 문자열 | 측정 방법 한 줄 |
| `a` · `b` | 예 | 숫자 목록 | 원시 표본. 예열을 뺀 뒤 2 개 이상 |

## 비용 항목

| 키 | 필수 | 뜻 |
| --- | --- | --- |
| `category` | 예 | `network` · `server` · `external_api` · `device` |
| `name` | 예 | 보고서에 쓰는 이름 |
| `metric` | 예 | 지표 `key` |
| `scale` · `volume` · `price` | 예 | 0 이상 숫자 — `cost-model.md` 의 식 |
| `volume_source` · `price_source` | 예 | 양 · 단가 출처. 가정은 `(가정)`, 예시 단가는 `(예시 단가)` |

## 판정 계산

판정은 적지 않는다. 스크립트가 예열을 뺀 표본으로 계산한다.

1. 양쪽 표본이 모두 한 값이면 결정값이다. 두 값이 다르면 p = 0, 같으면 p = 1
2. 아니면 양측 Mann-Whitney U. 쪽마다 합이 20 이하면 중간 순위로 순열을 전부 세고(동순위가 있어도 정확하다), 넘으면 동순위 보정 정규 근사
3. 이 표본 수로 낼 수 있는 가장 작은 p 가 `alpha` 이상이면 `표본 부족`
4. p ≥ `alpha` 면 `차이 없음`
5. |변화율| < `min_effect_pct` 면 `차이 미미`
6. 나머지는 `better` 방향에 따라 `개선` · `악화`

비교 전체:

- 대조 지표가 `개선` · `악화` 거나 `equivalence` 에 `same: false` 가 있으면 **무효**
- 대조 지표가 없거나 `표본 부족`, `order` 가 `interleaved` · `blocked`, 예열을 뺀 표본이 4 개 이상인데 모두 같은 방향으로 바뀌면 `주의:` 줄

## 스크립트가 막는 것

아래는 종료 코드 1 로 멈추고 보고서를 쓰지 않는다.

- JSON 문법 오류 · 표에 없는 키 · 필수 키 누락 · 빈 문자열 · 형식이 틀린 값
- 빈 `fixed` · 빈 `metrics` · 겹치는 `key` · 예열을 뺀 표본이 2 개 미만 · 중앙값이 0 인 `a`(변화율을 낼 수 없다)
- `metrics` 에 없는 `key` 를 가리키는 예산 · 비용 항목, `max` · `min` 을 둘 다 쓰거나 안 쓴 예산
- 단가 · 양 출처가 빠진 비용 항목
