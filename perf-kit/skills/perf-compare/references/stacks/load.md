# 스택: 서버 부하 시험

감지: 사용자가 처리량 · 동시 접속 · p95 · p99 · 부하를 말하거나, 비교할 변경이 커넥션 풀 · 캐시 · 스레드 수처럼 부하에서만 드러난다. 요청 하나의 응답 시간은 `server.md` 로 충분하다.

## 함정

- **부하 시험 한 번은 표본 하나다** — 한 회 안의 요청 수천 개를 표본으로 쓰지 않는다. 그 요청들은 서로 독립이 아니다. 회마다 p95 · 처리량 하나씩을 표본으로 두고 쪽마다 5 회 이상 돌린다
- **닫힌 모델은 느려진 서버를 덜 느리게 보인다** — 앞 반복이 끝나야 다음 반복이 시작되는 닫힌 모델에서는 서버 응답 시간이 시험 처리량에 영향을 준다. k6 문서는 이 문제를 coordinated omission 이라 부른다. 지연을 비교할 때는 응답 시간이 부하에 영향을 주지 않는 열린 모델(도착률 고정)로 잰다
- **부하 발생기가 먼저 포화되면 서버가 아니라 발생기를 잰 것이다** — 회마다 발생기 쪽 CPU 를 함께 보고 거의 다 쓰고 있으면 그 회를 버린다
- **A · B 를 같은 데이터 상태에서 잰다** — 쓰기 요청이 섞이면 회마다 DB 가 커진다. 회 사이에 데이터를 되돌리거나 읽기 요청만으로 잰다

## 지표별 경로

| 지표 | 경로 | 표본 |
| --- | --- | --- |
| 고정 도착률에서 p95 · p99 지연 | k6 `constant-arrival-rate` | 회마다 요약의 `http_req_duration` p(95) · p(99) |
| 실패율 | k6 | 회마다 `http_req_failed` 비율 |
| 최대 처리량 | wrk | 회마다 `Requests/sec` |

## k6 — 고정 도착률

```javascript
// load.js — 초당 200 요청을 1 분 동안 고정으로 보낸다
import http from 'k6/http';

export const options = {
  scenarios: {
    steady: {
      executor: 'constant-arrival-rate',
      rate: 200,
      timeUnit: '1s',
      duration: '1m',
      preAllocatedVUs: 100,
      maxVUs: 400,
    },
  },
  summaryTrendStats: ['avg', 'med', 'p(95)', 'p(99)', 'max'],
};

export default function () {
  http.get(`${__ENV.BASE}/api/meet-list?page=1&pageSize=50`, { headers: { 'user-api-key': __ENV.TOKEN } });
}

export function handleSummary(data) {
  return { [`${__ENV.OUT}`]: JSON.stringify(data) };
}
```

```bash
BASE=http://localhost:8081 TOKEN="$TOKEN" OUT=run-03-a.json k6 run --quiet load.js
python3 - run-03-a.json <<'EOF'
import json, sys
m = json.load(open(sys.argv[1]))["metrics"]
d = m["http_req_duration"]["values"]
print(d["p(95)"], d["p(99)"], m["http_req_failed"]["values"]["rate"])
EOF
```

- 요약 값의 키는 `summaryTrendStats` 에 따라 정해진다. 그래서 위처럼 `p(95)` · `p(99)` 를 직접 적어 둔다
- k6 v1.5.0 이 새 요약 형식(`--new-machine-readable-summary`)을 들였고 v2 에서 기본이 된다. 판이 바뀌면 JSON 모양이 달라질 수 있어 첫 회에 파일을 열어 키를 확인한다
- 가상 사용자가 모자라면 정한 도착률을 다 내지 못한다. 실행 출력의 경고를 보고, 그런 회는 `maxVUs` 를 늘려 다시 잰다

## wrk — 최대 처리량

```bash
wrk -t4 -c64 -d30s --latency "http://localhost:8081/api/health" | awk '/Requests\/sec/ {print $2}'
```

- wrk 는 연결을 열어 둔 채 응답을 받으면 다음 요청을 보내는 닫힌 모델이라, 지연 비교에는 쓰지 않고 최대 처리량 비교에만 쓴다

## 출처

- k6 열린 · 닫힌 모델(coordinated omission): <https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/>
- k6 `constant-arrival-rate`: <https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-arrival-rate/>
- k6 `handleSummary` · `summaryTrendStats`: <https://grafana.com/docs/k6/latest/results-output/end-of-test/custom-summary/>
- wrk README(`-t` · `-c` · `-d` · `--latency` · `Requests/sec`): <https://github.com/wg/wrk>
