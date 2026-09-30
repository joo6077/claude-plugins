#!/bin/bash
# 두 판의 그려진 모양 비교 — 사용: MDIT_DIR=<node_modules 폴더> bash shape-run.sh <저장소> <옛 판> <새 판> <파일 목록 파일>
# 두 판을 git archive 로 임시 폴더에 풀어 list-shape.mjs 에 넘기고 그 종료 코드와 출력을 그대로 돌려준다.
# 판을 못 찾거나 풀기에 실패하면 list-shape.mjs 를 부르지 않고 종료 코드 2 로 멈춘다.
R=${1:?저장소}; A=${2:?옛 판}; B=${3:?새 판}; L=${4:?파일 목록}
HERE=$(cd "$(dirname "${0}")" && pwd)
git -C "$R" rev-parse --verify -q "${A}^{commit}" >/dev/null && git -C "$R" rev-parse --verify -q "${B}^{commit}" >/dev/null \
  || { echo "STOP 판 없음: $A · $B" >&2; exit 2; }
[ -s "$L" ] || { echo "STOP 파일 목록 없음: $L" >&2; exit 2; }
D=$(mktemp -d "${TMPDIR:-/tmp}/two.XXXXXX") || exit 2
trap 'rm -rf "$D"' EXIT
mkdir "$D/a" "$D/b"
git -C "$R" archive "$A" | tar -x -C "$D/a" && git -C "$R" archive "$B" | tar -x -C "$D/b" \
  || { echo "STOP 풀기 실패: $A · $B" >&2; exit 2; }
node "$HERE/list-shape.mjs" "$D/a" "$D/b" $(cat "$L")
