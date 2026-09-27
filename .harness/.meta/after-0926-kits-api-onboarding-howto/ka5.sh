#!/bin/bash
# ka5.sh <worktree> — /api-contract §9 hurl 예시를 뽑아 항목 0·1·2 개 응답에 돌린다
W="${1:?worktree}"; T=$(mktemp -d); HERE=$(cd "$(dirname "${0}")" && pwd)
awk '/^## 9\./{p=1} p&&/^```hurl/{f=1;next} f&&/^```/{exit} f' "$W/api-kit/skills/api-contract/SKILL.md" > "$T/ex.hurl"
echo "index_asserts=$(grep -cE 'jsonpath "[^"]*\[[0-9]+\]' "$T/ex.hurl")"
echo "collection_line=$(grep -cF 'jsonpath "$.data" isCollection' "$T/ex.hurl")"
for n in 0 1 2; do
  port=$((8800+n)); python3 "$HERE/stub.py" $port $n & sp=$!; sleep 1
  hurl --test --variable baseUrl=http://127.0.0.1:$port --variable access_token=x "$T/ex.hurl" >/dev/null 2>&1; echo "n=$n rc=$?"
  kill $sp; wait $sp 2>/dev/null
done
rm -rf "$T"
