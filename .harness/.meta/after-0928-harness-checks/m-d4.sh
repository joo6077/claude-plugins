#!/usr/bin/env bash
# m-d4.sh <레포> <판> <변환 스크립트 폴더>... — 세션 임시 폴더의 변환 스크립트(gen.py · pages.py · page.css)가
# 그 판의 원본으로 커밋된 쪽을 글자까지 다시 만드는지 잰다. 줄마다 `<SAME|DIFF> <쪽> [차이 줄 수]`, 끝 줄 `same=<수> total=<수>`.
# 판을 git archive 로 푼 사본에 쓰므로 레포는 건드리지 않는다.
R=${1:?레포}; REV=${2:?판}; shift 2
T=$(mktemp -d "${TMPDIR:-/tmp}/md4.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
same=0; total=0; i=0
for G in "$@"; do
  i=$((i + 1)); d=$T/c$i; mkdir -p "$d"
  git -C "$R" archive "$REV" | tar -x -C "$d" || exit 2
  (cd "$G" && PYTHONDONTWRITEBYTECODE=1 python3 gen.py "$d") > "$T/log$i" 2>&1 || { echo "STOP $G 실행 실패"; cat "$T/log$i"; exit 2; }
  for o in $(sed -n 's/^wrote //p' "$T/log$i"); do
    total=$((total + 1))
    git -C "$R" show "$REV:$o" > "$T/orig" 2>/dev/null || { echo "MISSING $o"; continue; }
    if cmp -s "$T/orig" "$d/$o"; then same=$((same + 1)); echo "SAME $o"; else echo "DIFF $o $(diff "$T/orig" "$d/$o" | grep -cE '^[<>]')"; fi
  done
done
echo "same=$same total=$total"
