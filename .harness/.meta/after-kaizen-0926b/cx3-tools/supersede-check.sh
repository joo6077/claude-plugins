#!/bin/bash
# cx3 (4) status: superseded 계약이 새 판을 가리키는지 잰다. 사용법: supersede-check.sh <계약 뿌리 폴더>
# 줄마다 "<파일> by=<superseded_by> target=<있음 1/0> target_status=<값> target_slug_ok=<1/0> seal=<OK/BROKEN/ABSENT>"
# 마지막 줄: "superseded=<수> valid=<앞 넷이 모두 맞는 수>"
R=${1:?계약 뿌리 폴더}
fm_get() {  # fm_get <file> <key> — 첫 앞머리 블록만, 따옴표를 벗긴다
  awk -v k="$2" '
    NR==1 && /^---[[:space:]]*$/ { fm=1; next }
    fm && /^---[[:space:]]*$/    { exit }
    fm && index($0, k ":") == 1  { v = substr($0, length(k) + 2); sub(/^[[:space:]]+/, "", v); sub(/[[:space:]]+$/, "", v); print v; exit }
  ' "$1" | sed -e "s/^['\"]//" -e "s/['\"]\$//"
}
digest() {  # 조건 체크박스 줄 지문 — contract-schema §계약 봉인 과 같은 식
  grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | shasum -a 256 | cut -c1-16
}
n=0; ok=0
while IFS= read -r f; do
  [ "$(fm_get "$f" status)" = superseded ] || continue
  n=$((n + 1))
  by=$(fm_get "$f" superseded_by)
  t="$R/.harness/sprint-contract-$by.md"
  has=0; ts=-; slug_ok=0
  if [ -n "$by" ] && [ -f "$t" ]; then
    has=1; ts=$(fm_get "$t" status)
    [ "$(fm_get "$t" slug)" = "$by" ] && slug_ok=1
  fi
  rec=$(fm_get "$f" conditions_digest); rec=${rec#sha256:}
  if [ -z "$rec" ]; then seal=ABSENT; elif [ "$rec" = "$(digest "$f")" ]; then seal=OK; else seal=BROKEN; fi
  printf '%s by=%s target=%s target_status=%s target_slug_ok=%s seal=%s\n' "${f##*/}" "${by:-<none>}" "$has" "$ts" "$slug_ok" "$seal"
  [ "$has" = 1 ] && [ "$ts" != superseded ] && [ "$slug_ok" = 1 ] && [ "$seal" = OK ] && ok=$((ok + 1))
done <<EOF
$(find "$R/.harness" -maxdepth 1 -type f -name 'sprint-contract-*.md' | LC_ALL=C sort)
EOF
printf 'superseded=%s valid=%s\n' "$n" "$ok"
