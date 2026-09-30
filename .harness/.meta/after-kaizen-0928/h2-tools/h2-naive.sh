#!/bin/bash
# h2 양성 대조용 — 고치기 전 백업 훅에서 따옴표 덮기를 끄고 「git … commit 이 아무 데나 있으면 커밋」 으로 넓힌 사본을 만든다.
# 사용법: h2-naive.sh <만들 폴더>. 글자일 뿐인 경우(N 줄)를 재는 측정이 이런 넓힌 판을 잡는지 확인하는 데 쓴다.
HERE=$(cd "$(dirname "${0}")" && pwd)
O=${1:?만들 폴더}
mkdir -p "$O"
sed -e "s/^cmd_unquoted=\$(printf '%s' \"\$cmd\" | awk/cmd_unquoted=\$cmd; : \$(printf '%s' \"\$cmd\" | awk/" \
    -e "s/grep -qE '(^|\[;&|\]\[\[:space:\]\]\*)git(/grep -qE '(^|[^[:alnum:]])git(/" \
    "$HERE/../h2-backup/parallel-session-guard.sh" > "$O/parallel-session-guard.sh"
cp "$HERE/../h2-backup/_lib-hook-payload.sh" "$O/_lib-hook-payload.sh"
diff "$HERE/../h2-backup/parallel-session-guard.sh" "$O/parallel-session-guard.sh" | grep -cE '^[<>]'
