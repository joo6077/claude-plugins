#!/usr/bin/env bash
# MakerWorld 받는 법 블록 시험 — SKILL.md 「### JSON 주소」 절의 bash 블록을 뽑아 가짜 curl 로 돌린다.
# 블록을 베끼지 않고 매번 SKILL.md 에서 뽑는다. 다른 사본을 잴 때: BAMBU_FETCH_SKILL=<SKILL.md 사본> bash makerworld-fetch-test.sh
# 가짜 curl 의 응답 모양은 2026-09-24 · 09-27 관측을 따른다 — 답글 배열 comment.commentReply · 답글 수 comment.replyCount,
# 모델 주소가 막히면 403 과 「Just a moment...」 HTML.
# 알려진 답: 댓글 둘(replyCount 2 · 배열 2 개, replyCount 1 · 배열 0 개) → replyCount 3 · 받은 commentReply 2.
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SKILL=${BAMBU_FETCH_SKILL:-$HERE/../skills/bambu-print-profile/SKILL.md}
command -v python3 >/dev/null 2>&1 || { echo "python3 이 없다 — 블록이 응답을 못 센다"; exit 2; }

W=$(mktemp -d "${TMPDIR:-/tmp}/mwf.XXXXXX") || exit 2
trap 'rm -rf "$W"' EXIT
mkdir -p "$W/bin"
awk 'index($0,"### JSON 주소")==1 {h=1} h && /^```bash$/ {b=1; next} b && /^```$/ {exit} b' "$SKILL" > "$W/block.sh"
grep -q 'curl' "$W/block.sh" || { echo "STOP 받는 법 블록을 못 뽑았다 — $SKILL"; exit 2; }

# -o · -w 만 흉내 낸다. 주소마다 준비한 본문과 상태 코드를 돌려준다
cat > "$W/bin/curl" <<'EOF'
#!/usr/bin/env bash
o=""; w=""; u=""
while [ $# -gt 0 ]; do case "$1" in -o) o=$2; shift 2 ;; -w) w=$2; shift 2 ;; -*) shift ;; *) u=$1; shift ;; esac; done
code=200; body=""
case "$u" in
  *makerworld.com/api/v1/design-service/design/*) code=$MW_CODE
    if [ "$code" = 200 ]; then body='{"title":"T","commentCount":2,"instances":[]}'; else body='<!DOCTYPE html><title>Just a moment...</title>'; fi ;;
  */instances) body='{"hits":[],"total":0}' ;;
  *commentandrating*offset=0*) body='{"total":2,"hits":[{"type":1,"comment":{"id":1,"replyCount":2,"commentReply":[{"id":11},{"id":12}]}},{"type":1,"comment":{"id":2,"replyCount":1,"commentReply":[]}}]}' ;;
  *commentandrating*) body='{"total":2,"hits":[]}' ;;
esac
[ -n "$o" ] && printf '%s' "$body" > "$o"
printf '%s' "${w//%\{http_code\}/$code}"
EOF
chmod 755 "$W/bin/curl"

run_block() {  # run_block <모델 주소 상태 코드> — 블록 출력 뒤에 exit=N
  local d=$W/run-$1
  mkdir -p "$d/out"
  sed -e "s#<모델 번호>#1186414#" -e "s#<output_dir>#$d/out#" "$W/block.sh" > "$d/block.sh"
  ( cd "$d" && PATH="$W/bin:$PATH" MW_CODE="$1" bash "$d/block.sh" 2>&1; echo "exit=$?" )
}

n=0; bad=0
check() {  # check <이름> <답> <값>
  n=$((n + 1))
  if [ "$2" = "$3" ]; then echo "일치 $1"
  else echo "불일치 $1 — 값 [$3] (답 [$2])"; bad=$((bad + 1)); fi
}

ok=$(run_block 200)
check "200 — 종료 코드 0" "exit=0" "$(printf '%s\n' "$ok" | tail -1)"
check "댓글 수 — total 2 · 받은 hits 2" 1 "$(printf '%s\n' "$ok" | grep -c '^comments total 2 · 받은 hits 2 ')"
check "답글 수 — replyCount 3 · commentReply 2" 1 "$(printf '%s\n' "$ok" | grep '답글' | grep 'replyCount 3' | grep -c 'commentReply 2')"

blocked=$(run_block 403)
check "403 모델 주소 — FAIL design.json 한 줄" 1 "$(printf '%s\n' "$blocked" | grep -c '^FAIL design.json')"
check "403 모델 주소 — 종료 코드 1" "exit=1" "$(printf '%s\n' "$blocked" | tail -1)"

echo "결과: $n 경우 중 불일치 $bad"
[ "$bad" = 0 ]
