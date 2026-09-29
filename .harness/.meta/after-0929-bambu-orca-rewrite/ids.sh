#!/usr/bin/env bash
# 한국어 조건 번호(스킬 · 스크립트 · 오류 · 구조 · 재사용 · 진단 · 금지)도 읽는 조건 세기 · 봉인 값 계산.
# 레포 도구(계약 형식 문서의 contract_digest · measurement_digest, sprint-contract 6.2 · 6.5)는 영어 약자 번호만 읽는다.
# 그 도구를 고치는 일은 다른 묶음 몫이라, 이 계약은 이 사본으로 센다. 영어 번호는 레포 도구와 같은 값을 낸다.
# 사용: bash ids.sh count|func|digest|mdigest <계약 파일>
set -u
ID='([A-Z]{2,}|스킬|스크립트|오류|구조|재사용|진단|금지)-[0-9]{2}'
h16() { shasum -a 256 | cut -c1-16; }
case "${1}" in
  count)  grep -cE "^- \[[ x]\] $ID" "${2}" ;;
  func)   awk -v id="^- \\\\[[ x]\\\\] $ID" '/^## /{s=$(0)} $(0) ~ id { if (s=="## Anti-patterns") next; if ($(0) ~ /^- \[[ x]\] (RE-0[12]|DG-0[1-4]|재사용-0[12]|진단-0[1-4]):/) next; if ($(0) ~ /: N\/A \(/) next; n++ } END{print n+0}' "${2}" ;;
  digest) grep -E "^- \[[ x]\] $ID" "${2}" | sed -E 's/^- \[[ x]\]/- [ ]/' | h16 ;;
  mdigest)
    awk -v id="^- \\\\[[ x]\\\\] $ID" -v tok="$ID" '
      $(0) ~ id { inb=1; match($(0), tok); print substr($(0), RSTART, RLENGTH); next }
      inb && /^[ \t]+[^ \t]/ { line=$(0); sub(/[ \t]+$/, "", line); print line; next }
      inb && /^[ \t]*$/      { next }
      { inb=0 }
    ' "${2}" | h16 ;;
  *) echo "사용: bash ids.sh count|func|digest|mdigest <계약 파일>" >&2; exit 2 ;;
esac
