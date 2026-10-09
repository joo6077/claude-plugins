#!/usr/bin/env bash
# spec-neg.sh <레포 폴더> <판> <모양> — 그 판을 임시 폴더에 풀고 시안 틀만 망가뜨린 뒤 visuals.spec.js 의 시험 하나를 돌린다.
# 모양: label — 비교 쪽 왼쪽 이름표를 빈 글자로 채우게 바꾼다 (-g '비교')
#       oldgrid — 틀을 기준 판 cacd9da3 의 것으로 바꾼다 (-g '한 줄')
#       none — 망가뜨리지 않고 둘 다 돌린다 (-g '비교|한 줄')
# 한 줄: mode=<모양> applied=<망가뜨림이 들어갔으면 1> rc=<playwright 종료 코드> passed=<n> failed=<n>
repo=${1:?레포 폴더}; rev=${2:?판}; mode=${3:?모양}
t=$(mktemp -d "${TMPDIR:-/tmp}/spec-neg.XXXXXX") || exit 2
trap 'rm -rf "$t"' EXIT
git -C "$repo" archive "$rev" | tar -x -C "$t" || exit 2
ln -s "$repo/node_modules" "$t/node_modules"
tpl=$t/design-kit/templates/mockup.html
case $mode in
  label) sed -i.orig -e 's/leftLabel\.textContent = T\[currentLang\]\.tab\[leftId\]/leftLabel.textContent = ""/' "$tpl"
         applied=$(grep -c 'leftLabel.textContent = ""' "$tpl"); g='비교' ;;
  oldgrid) git -C "$repo" show cacd9da3:design-kit/templates/mockup.html > "$tpl"
           applied=$(grep -c 'grid-template-columns: repeat(5, 1fr)' "$tpl"); g='한 줄' ;;
  none) applied=0; g='비교|한 줄' ;;
  *) echo "모양을 모른다: $mode" >&2; exit 2 ;;
esac
out=$(cd "$t" && npx playwright test design-kit/evals/visuals.spec.js -g "$g" --reporter=line 2>&1); rc=$?
passed=$(printf '%s\n' "$out" | sed -n -E 's/^.* ([0-9]+) passed.*/\1/p' | tail -1)
failed=$(printf '%s\n' "$out" | sed -n -E 's/^.* ([0-9]+) failed.*/\1/p' | tail -1)
echo "mode=$mode applied=$applied rc=$rc passed=${passed:-0} failed=${failed:-0}"
