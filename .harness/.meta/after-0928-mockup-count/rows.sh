#!/bin/sh
# §5.6 Variant Matrix 예시 행 수 · Good 줄 · 예시 이름표 — rows.sh <레포 뿌리>
# 출력: MATRIX md_rows=<n> md_good5=<0|1> md_label=<0|1> html_rows=<n> html_good5=<0|1> html_label=<0|1>
# good5  = §5.6 안 Good 줄에 「시안」 · 「5 행」 · 「5 파일」 이 모두 있다.
# label  = Variant Matrix 제목과 표 머리 사이에 「시안」 · 「최소 5」 · 「상한 3」 이 모두 든 줄이 있다
#          (예시가 시안 규칙을 보여 주고, 시안이 아닌 탐색형 산출물은 여전히 상한 3 이라고 밝힌다).
# 파일이 없으면 종료 코드 2.
R=${1:-.}
MD="$R/harness/docs/guides/skill-design-guide.md"; HT="$R/docs/harness/skill-design-guide.html"
[ -f "$MD" ] && [ -f "$HT" ] || { echo "MISSING_FILE"; exit 2; }
md=$(awk '/^## 5\.6\. /{p=1} /^## 6\. /{p=0} p' "$MD")
ht=$(awk '/<!-- ═══ 5\.6 Variant Budget/{p=1} /<!-- ═══ 6\. /{p=0} p' "$HT")
mr=$(printf '%s\n' "$md" | grep -cE '^\| A[0-9]+ \|')
hr=$(printf '%s\n' "$ht" | grep -cE '<tr><td>A[0-9]+</td>')
mg=$(printf '%s\n' "$md" | grep -E '^Good:' | grep '시안' | grep '5 행' | grep -c '5 파일')
hg=$(printf '%s\n' "$ht" | grep -E '^Good:' | grep '시안' | grep '5 행' | grep -c '5 파일')
ml=$(printf '%s\n' "$md" | awk '/^### Variant Matrix/{p=1; next} /^\| id \|/{p=0} p' \
  | sed -e 's/\*\*//g' -e 's/`//g' | grep '시안' | grep '최소 5' | grep -c '상한 3')
hl=$(printf '%s\n' "$ht" | awk '/<h3 class="sub">Variant Matrix/{p=1; next} /<thead>/{p=0} p' \
  | sed -e 's/<[^>]*>//g' | grep '시안' | grep '최소 5' | grep -c '상한 3')
[ "$ml" -gt 0 ] && ml=1; [ "$hl" -gt 0 ] && hl=1
echo "MATRIX md_rows=$mr md_good5=$mg md_label=$ml html_rows=$hr html_good5=$hg html_label=$hl"
