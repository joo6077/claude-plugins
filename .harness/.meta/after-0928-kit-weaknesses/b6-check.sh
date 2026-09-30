#!/bin/sh
# G5 표 모양 변형 판정 (B6). 쓰임: sh b6-check.sh <레포 뿌리> <변형 폴더> <셸>
# <셸> 은 zsh 또는 bash. 변형마다 「<파일 이름> <G5 줄>」 을 찍고, 끝에 기대와 다른 수를 센다.
#   empty-*        → 「G5_BLOCKING FAIL」 로 시작해야 한다 (five-col 밖은 정확히 「G5_BLOCKING FAIL rows=2 empty=1 nourl=0」)
#   ok-*           → 정확히 「G5_BLOCKING PASS rows=2」
#   plain-unrelated → 정확히 「G5_BLOCKING PASS rows=0」
# 종료 코드: 0 전부 기대대로 · 1 하나 이상 다름 · 2 준비 실패
R=${1}; V=${2}; SHELL_NAME=${3}
G=$(mktemp "${TMPDIR:-/tmp}/b6gate.XXXXXX") || exit 2
awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' "$R/onboarding-kit/skills/setup-guide/SKILL.md" > "$G"
head -1 "$G" | grep -qx 'guide_gate() {' || { echo "STOP 함수 추출 실패"; rm -f "$G"; exit 2; }
total=0; bad=0
for f in $(find "$V" -maxdepth 1 -type f -name '*.md' | sort); do
  b=$(basename "$f")
  line=$($SHELL_NAME -c ". '$G'; guide_gate '$f' flutter" 2>&1 | grep '^G5_')
  case $b in
    empty-five-col*) want_prefix="G5_BLOCKING FAIL"; want="" ;;
    empty-*) want_prefix=""; want="G5_BLOCKING FAIL rows=2 empty=1 nourl=0" ;;
    ok-*) want_prefix=""; want="G5_BLOCKING PASS rows=2" ;;
    plain-unrelated*) want_prefix=""; want="G5_BLOCKING PASS rows=0" ;;
    *) want_prefix=""; want="?" ;;
  esac
  total=$((total + 1))
  if [ -n "$want" ]; then [ "$line" = "$want" ] && r=OK || r=DIFF
  else case $line in "$want_prefix"*) r=OK ;; *) r=DIFF ;; esac
  fi
  [ "$r" = DIFF ] && bad=$((bad + 1))
  echo "$r $b $line"
done
rm -f "$G"
echo "B6 shell=$SHELL_NAME total=$total diff=$bad"
[ "$total" -gt 0 ] && [ "$bad" = 0 ]
