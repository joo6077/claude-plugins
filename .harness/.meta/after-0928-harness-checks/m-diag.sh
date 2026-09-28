#!/usr/bin/env bash
# m-diag.sh <레포> <기준 판> <markdownlint-cli2 폴더> — 이번 변경 파일의 편집기 경고를 명령줄로 잰다.
# 변경 파일 = `git diff --name-only <기준 판>` + 추적 전 새 파일, `.harness/` 는 뺀다.
# .md  : markdownlint-cli2 0.23.2 · MD013 끔(편집기 확장과 같음) — 기준 판 뒤에 더한 줄에 걸린 경고만 센다
# .sh  : shellcheck — 새 파일은 전부, 고친 파일은 더한 줄에 걸린 것만
# .py  : python3 -m py_compile 실패 수 · .js : node --check 실패 수
# 출력: 파일마다 `<종류> <경로> new=<수>`, 끝 줄 `md_new=<수> sh_new=<수> py_bad=<수> js_bad=<수> files=<수>`
R=${1:?레포}; BASE=${2:?기준 판}; MDL=${3:?markdownlint-cli2 폴더}
T=$(mktemp -d "${TMPDIR:-/tmp}/mdiag.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
cd "$R" || exit 2
{ git diff --name-only "$BASE"; git ls-files --others --exclude-standard; } | grep -v '^\.harness/' | LC_ALL=C sort -u > "$T/files"
printf '{ "config": { "MD013": false } }\n' > "$T/.markdownlint-cli2.jsonc"
added() {  # added <파일> — 기준 판 뒤에 더한 줄 번호. 새 파일이면 ALL
  if git cat-file -e "$BASE:$1" 2>/dev/null; then
    git diff -U0 "$BASE" -- "$1" | sed -n -E 's/^@@ -[0-9,]+ \+([0-9]+)(,([0-9]+))? @@.*/\1 \3/p' \
      | awk '{ n = ($2 == "") ? 1 : $2; for (i = 0; i < n; i++) print $1 + i }'
  else echo ALL; fi
}
md=0; sh=0; py=0; js=0; nf=0
while IFS= read -r f; do
  [ -f "$f" ] || continue
  nf=$((nf + 1)); added "$f" > "$T/add"
  case "$f" in
    *.md)
      "$MDL/node_modules/.bin/markdownlint-cli2" --config "$T/.markdownlint-cli2.jsonc" "$f" > "$T/out" 2>&1
      sed -n -E 's#^[^:]*:([0-9]+)[: ].*#\1#p' "$T/out" > "$T/lines"
      if grep -qx ALL "$T/add"; then n=$(grep -c . "$T/lines"); else n=$(grep -cxFf "$T/add" "$T/lines"); fi
      md=$((md + n)); echo "md $f new=$n" ;;
    *.sh)
      shellcheck -f gcc "$f" > "$T/out" 2>&1
      sed -n -E 's#^[^:]*:([0-9]+):.*#\1#p' "$T/out" > "$T/lines"
      if grep -qx ALL "$T/add"; then n=$(grep -c . "$T/lines"); else n=$(grep -cxFf "$T/add" "$T/lines"); fi
      sh=$((sh + n)); echo "sh $f new=$n" ;;
    *.py) python3 -m py_compile "$f" 2>/dev/null || { py=$((py + 1)); echo "py $f bad"; } ;;
    *.js) node --check "$f" 2>/dev/null || { js=$((js + 1)); echo "js $f bad"; } ;;
  esac
done < "$T/files"
echo "md_new=$md sh_new=$sh py_bad=$py js_bad=$js files=$nf"
