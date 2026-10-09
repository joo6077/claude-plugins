#!/bin/bash
# h2-cases.sh 의 K · N 명령을 진짜 bash 로 돌려, git commit 이 실제로 불리는지 센다 (시험 입력의 정답 확인).
# 가짜 git 은 scratch 의 새 일반 파일이다. 진짜 git 을 가리키는 바로가기를 만들지 않는다.
# 출력: "<경우> ran=<가짜 git 이 commit 으로 불린 횟수>"
HERE=$(cd "$(dirname "${0}")" && pwd)
F=${H2_TRUTH:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/h2-truth}
rm -rf "$F"; mkdir -p "$F/bin" "$F/run"
printf '#!/bin/sh\nfor a in "$@"; do [ "$a" = commit ] && echo ran >> %s/log && exit 0; done\nexit 0\n' "$F" > "$F/bin/git"
chmod +x "$F/bin/git"
echo a > "$F/run/a.txt"
grep -E "^case_line [KN][0-9]+ " "$HERE/h2-cases.sh" > "$F/lines"
while IFS= read -r line; do
  id=$(printf '%s' "$line" | awk '{print $2}')
  cmd=$(eval "set -- ${line#case_line }; printf '%s' \"\$2\"")
  rm -f "$F/log"
  ( cd "$F/run" && PATH="$F/bin:$PATH" bash -c "$cmd" >/dev/null 2>&1 )
  printf '%s ran=%s\n' "$id" "$( [ -f "$F/log" ] && grep -c . "$F/log" || echo 0)"
done < "$F/lines"
