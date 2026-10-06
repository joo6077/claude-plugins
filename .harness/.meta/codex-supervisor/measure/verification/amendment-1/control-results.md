# 개정 1 대조 실측

| 조건 | 양성 기대/실제 | 알려진 답 기대/실제 | controls 종료 | 일반 실행 | 음성 대조 |
| --- | --- | --- | ---: | --- | --- |
| 스크립트-12 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-12 checks=52 failures=12 | FAIL 스크립트-12 checks=28 failures=23 |
| 스크립트-13 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-13 checks=31 failures=2 | FAIL 스크립트-13 checks=22 failures=11 |
| 스크립트-14 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-14 checks=26 failures=7 | FAIL 스크립트-14 checks=22 failures=9 |
| 스크립트-15 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-15 checks=14 failures=2 | FAIL 스크립트-15 checks=11 failures=5 |
| 스크립트-16 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-16 checks=19 failures=2 | FAIL 스크립트-16 checks=14 failures=5 |
| 스크립트-17 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-17 checks=39 failures=4 | FAIL 스크립트-17 checks=27 failures=18 |
| 스크립트-18 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-18 checks=10 failures=6 | FAIL 스크립트-18 checks=10 failures=6 |
| 스크립트-19 | 1 / 1 | 2 / 2 | 0 | FAIL 스크립트-19 checks=26 failures=9 | FAIL 스크립트-19 checks=18 failures=12 |

스크립트-14: heartbeat 살아 있음 1/1, 정지 뒤 갱신 0/0. 스크립트-15: 변이 검출 7/7.

기존 스크립트-10은 변경 전·후 동일하게 PASS checks=26 failures=0. 코드 해시는 measure.sh의 공개된 분기 추가 외에 모두 동일하다. 실제 모델 호출 0.
