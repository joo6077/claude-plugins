#!/usr/bin/env bash
# 구간 <base>..<upper> 에서 바뀐 .sh · .md · .py 파일(.harness 밖)의 더한 줄에 걸린 경고만 센다.
# 사용: lint_new.sh <레포> <base> <upper> <markdownlint-cli2 경로> <pyflakes 파이썬 경로>
repo=${1:?}; base=${2:?}; up=${3:?}; mdl=${4:?}; pyf=${5:?}
command -v shellcheck >/dev/null || { echo "STOP shellcheck 없음"; exit 2; }
[ -x "$mdl" ] || { echo "STOP markdownlint-cli2 없음 $mdl"; exit 2; }
"$pyf" -m pyflakes --version >/dev/null 2>&1 || { echo "STOP pyflakes 없음"; exit 2; }
t=$(mktemp -d "${TMPDIR:-/tmp}/lint-new.XXXXXX"); trap 'rm -rf "$t"' EXIT
printf '{ "config": { "MD013": false } }\n' >"$t/.markdownlint-cli2.jsonc"
total=0; files=0
while IFS= read -r f; do
  case $f in *.sh|*.md|*.py) ;; *) continue ;; esac
  git -C "$repo" cat-file -e "$up:$f" 2>/dev/null || continue
  files=$((files + 1))
  mkdir -p "$t/w/$(dirname "$f")"; git -C "$repo" show "$up:$f" >"$t/w/$f"
  git -C "$repo" diff -U0 "$base" "$up" -- "$f" | awk '/^@@/{ split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i }' | sort -n >"$t/added"
  case $f in
    *.sh) (cd "$t/w" && shellcheck -f gcc "$f") | sed -nE 's#^[^:]+:([0-9]+):.*#\1#p' ;;
    *.md) (cd "$t/w" && "$mdl" --config "$t/.markdownlint-cli2.jsonc" "$f" 2>&1) | sed -nE 's#^[^ :]+\.md:([0-9]+)(:[0-9]+)? .*#\1#p' ;;
    *.py) (cd "$t/w" && "$pyf" -m pyflakes "$f") | sed -nE 's#^[^:]+:([0-9]+):.*#\1#p' ;;
  esac | sort -n >"$t/warn"
  n=$(comm -12 <(sort -u "$t/added") <(sort -u "$t/warn") | grep -c .)
  printf '%s new=%s\n' "$f" "$n"; total=$((total + n))
done < <(git -C "$repo" diff --name-only "$base" "$up" -- . ':(exclude).harness')
echo "files=$files new_warnings=$total"
