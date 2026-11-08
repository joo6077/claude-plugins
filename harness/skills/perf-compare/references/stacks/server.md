# 스택: 서버 · HTTP · 외부 API

감지: 비교 대상이 HTTP 로 부르는 서버거나, 앱이 기다리는 API 구간이다. 다른 스택 문서와 함께 읽을 수 있다 — 앱만 바꿨어도 대조 지표는 이 문서에서 고른다.
새로 짠 명령은 본 측정 전에 알려진 답 대조를 거친다 (SKILL.md 2).

## HTTP 응답 시간과 전송량

```bash
# 한 번: 전체 시간(초) · 첫 바이트까지(초) · 받은 bytes · 상태
curl -s -o /dev/null -w '%{time_total} %{time_starttransfer} %{size_download} %{http_code}\n' \
  -H "user-api-key: $TOKEN" "$BASE/api/meet-list?page=1&pageSize=50"
```

- `size_download` 는 압축이 풀리기 전 bytes 다. 압축 전송량을 보려면 `--compressed` 없이 `Accept-Encoding: gzip` 헤더를 붙인다. 비용은 실제로 선을 탄 bytes 로 계산하므로 운영과 같은 압축 설정으로 잰다
- 상태가 200 이 아닌 표본은 버린다. 버린 수를 보고에 적는다

## 동시 호출 (화면 하나가 부르는 API 묶음)

```bash
# urls.txt 의 주소를 한꺼번에 부르고, 마지막 응답까지 걸린 ms 를 찍는다
start=$(python3 -c 'import time; print(int(time.time()*1000))')
xargs -P 16 -I{} curl -s -o /dev/null -w '%{size_download}\n' -H "user-api-key: $TOKEN" "{}" < urls.txt > sizes.txt
end=$(python3 -c 'import time; print(int(time.time()*1000))')
echo "burst_ms=$((end - start)) bytes=$(paste -sd+ sizes.txt | bc)"
```

- 주소 목록은 앱 로그에서 그 화면의 실제 요청을 옮겨 만든다. 손으로 고르면 빠진 요청이 생긴다
- `-P` 는 앱이 실제로 동시에 보내는 수와 맞춘다

## 서버 CPU 시간 (요청당)

```bash
# 측정 전후 프로세스 누적 CPU 시간(초)의 차 ÷ 요청 수
# ps 의 cputime 은 운영체제마다 [[DD-]HH:]MM:SS[.ss] 중 한 형식이라 뒤에서부터 자리를 읽는다
cpu() {
  ps -o cputime= -p "$1" | python3 -c '
import sys
t = sys.stdin.read().strip()
days, _, t = t.rpartition("-")
sec = 0.0
for part in t.split(":"):
    sec = sec * 60 + float(part)
print(sec + int(days or 0) * 86400)'
}
before=$(cpu "$PID"); ./burst.sh 100; after=$(cpu "$PID")
python3 -c "print(($after - $before) / 100)"
```

- 알려진 답 대조: `0:00.12` → 0.12, `1:02:03` → 3723, `1-00:00:01` → 86401 이 나와야 한다. 셋 중 하나라도 다르면 본 측정에 쓰지 않는다
- 같은 서버에서 다른 요청이 섞이면 안 된다. 로컬 서버나 트래픽 없는 스테이징에서 잰다

## DB 쿼리 수 · 시간

| DB | 방법 |
| --- | --- |
| PostgreSQL | `pg_stat_statements_reset()` → 측정 → `SELECT calls, total_exec_time, query FROM pg_stat_statements ORDER BY total_exec_time DESC` |
| MySQL · MariaDB | `performance_schema.events_statements_summary_by_digest` 를 `TRUNCATE` → 측정 → 같은 표 조회 |
| 앱 쪽 로그 | MyBatis · Hibernate SQL 로그를 켜고 요청 하나에 찍힌 줄 수를 센다 |

쿼리 수는 결정값 지표다. 쪽마다 2 회면 된다.

## 외부 API (LLM · STT · 지도)

- 호출 수는 서버 로그나 앱 로그에서 센다
- LLM 토큰은 응답 본문의 사용량 필드(`usage.input_tokens` · `usage.output_tokens` 처럼 공급자가 돌려주는 값)를 합산한다. 글자 수로 토큰을 어림하지 않는다
- STT 는 과금 단위(초 · 분 · 15 초 단위 올림)를 요금표에서 확인하고 그 단위로 센다
- 캐시 · 재시도가 있으면 실제로 나간 호출만 센다

## 운영 응답과의 동일성

```bash
# 키를 정렬해 비교. 의도해서 뺀 필드는 del 로 지운 뒤 비교한다
diff <(jq -S . old.json) <(jq -S . new.json) && echo same
diff <(jq -S 'del(.data[].contents)' old.json) <(jq -S 'del(.data[].contents)' new.json) && echo same-except-contents
```
