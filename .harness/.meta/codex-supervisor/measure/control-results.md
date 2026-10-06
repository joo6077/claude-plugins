# 계약 대조 실측

명령: `bash out/measure/measure.sh <조건> --controls-only`. 모든 행의 원문 출력은 verification/<조건>-controls.txt에 있다.

| 조건 | 양성 기대 | 양성 실제 | 알려진 답 기대 | 실제 | 종료 | 일치 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 스킬-02 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-01 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-02 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-03 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-04 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-05 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-06 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-07 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-08 | 1 | 1 | 1 | 1 | 0 | PASS |
| 스크립트-09 | 2 | 2 | 2 | 2 | 0 | PASS |
| 스크립트-10 | 1 | 1 | 2 | 2 | 0 | PASS |
| 스크립트-11 | 1 | 1 | 1 | 1 | 0 | PASS |
| 오류-01 | 2 | 2 | 2 | 2 | 0 | PASS |
| 오류-02 | 2 | 2 | 2 | 2 | 0 | PASS |
| 구조-01 | 1 | 1 | 2 | 2 | 0 | PASS |
| 구조-02 | 1 | 1 | 1 | 1 | 0 | PASS |
| 구조-04 | 2 | 2 | 2 | 2 | 0 | PASS |
| 금지-03 | 1 | 1 | 1 | 1 | 0 | PASS |
| 금지-04 | 1 | 1 | 1 | 1 | 0 | PASS |
| 진단-01 | 1 | 1 | 1 | 1 | 0 | PASS |
| 진단-02 | 3 | 3 | 3 | 3 | 0 | PASS |
| 진단-03 | 1 | 1 | 1 | 1 | 0 | PASS |
| 진단-04 | 2 | 2 | 2 | 2 | 0 | PASS |

양성 대조의 PASS는 구현의 PASS가 아니다. 다음은 옵션 없이 실행한 구현 전 판정이다.

| 조건 | 현재 결과 | 종료 | 예상한 FAIL인가 |
| --- | --- | ---: | --- |
| 스크립트-01 | FAIL 스크립트-01 checks=3 failures=1 | 1 | True |
| 스크립트-02 | FAIL 스크립트-02 checks=3 failures=1 | 1 | True |
| 스크립트-03 | FAIL 스크립트-03 checks=3 failures=1 | 1 | True |
| 스크립트-07 | FAIL 스크립트-07 checks=3 failures=1 | 1 | True |
| 스크립트-10 | FAIL 스크립트-10 checks=12 failures=1 | 1 | True |
| 스크립트-11 | FAIL 스크립트-11 checks=13 failures=1 | 1 | True |
| 오류-01 | FAIL 오류-01 checks=22 failures=1 | 1 | True |
| 구조-03 | FAIL 구조-03 checks=14 failures=12 | 1 | True |
| 스킬-01 | FAIL 스킬-01 checks=19 failures=8 | 1 | True |
| 스크립트-05 | FAIL 스크립트-05 checks=3 failures=1 | 1 | True |
| 스크립트-08 | FAIL 스크립트-08 checks=3 failures=1 | 1 | True |
| 구조-04 | FAIL 구조-04 checks=19 failures=1 | 1 | True |

구조-02 추가 대조: 역할 부여 다섯 표본 검출 5/5; UTF-8 손 예제 12바이트; 경계 8192 통과·8193 위반; 예시 표제 두 개 검출 2.
스크립트-10 추가 대조: draft·revise·impl·조사 유효 스키마 4/4; revise·조사 스키마 미전달 검출 2/2.
오류-01 추가 대조: draft·revise·조사의 결과 파일 없음·깨진 JSON·필수 칸 빠짐 9/9을 가짜 실행 파일로 실제 생성·검출.
구조-04 추가 대조: 인증 도우미 정상·실패·시간 초과·SIGINT·SIGTERM 정리 기대 5·실제 5.

| 음성 대조 | 종료 | 기대 FAIL 확인 |
| --- | ---: | --- |
| 구조-02 | 1 | True |
| 스크립트-11 | 1 | True |
| 구조-04 | 1 | True |

실제 감독 폴더 로그인 준비: READY / 종료 0 / 모델 호출 0 / 구현 판정 안 함. 원문은 verification/스크립트-11-preparation.txt.
