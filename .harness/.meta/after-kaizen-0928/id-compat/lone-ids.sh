#!/bin/bash
# 규칙 자리에서 영어 자동 번호가 한국어 번호 없이 홀로 남은 줄을 센다.
# 쓰는 법: bash lone-ids.sh <파일> <시작 줄 머리> <끝 줄 머리>   (머리가 빈 값이면 파일 전체)
# 범위: 시작 머리를 담은 줄부터 끝 머리를 담은 줄 앞까지. 시작 머리를 못 찾으면 NO_REGION 으로 exit 2.
# 뺀다: 같은 줄에 「실측」 또는 「출처」 가 있는 줄 (지난 계약 인용).
# 출력: region=<줄 수> lone=<홀로 남은 줄 수> ko=<한국어 자동 번호가 있는 줄 수>
awk -v start="$2" -v stop="$3" '
  BEGIN { on = (start == "") }
  !on && !seen && start != "" && index($0, start) > 0 { on = 1; seen = 1 }
  on && stop != "" && index($0, stop) > 0 && NR > 1 && started { on = 0 }
  on { started = 1; n++
       if ($0 ~ /(RE-0[12]|DG-0[1-4]|AP-00)/ && $0 !~ /(실측|출처)/ && $0 !~ /(재사용-0[12]|진단-0[1-4]|금지-00)/) { lone++; print "LONE " NR ": " substr($0, 1, 100) > "/dev/stderr" }
       if ($0 ~ /(재사용-0[12]|진단-0[1-4]|금지-00)/) ko++ }
  END { if (start != "" && !seen) { print "NO_REGION"; exit 2 }
        printf "region=%d lone=%d ko=%d\n", n, lone + 0, ko + 0 }' "$1"
