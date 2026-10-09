#!/usr/bin/env bash
# 오르카 경로 하나의 기준 내용을 표준 출력으로 낸다.
# 통합 가지가 공통 기준 뒤에 그 경로를 안 바꿨으면 앞 회차 가지 끝 판을, 바꿨으면 세 판 합치기(충돌 자리는 앞 회차 쪽)를 낸다.
# 사용: bash ref3.sh <레포> <레포 안 경로>
# 종료 코드: 0 정상 · 2 판을 못 읽음
set -u
REPO=${1}; P=${2}
BASE=c25d16ec9bc55e7ef4b2021975c8c40da08d2af7   # chore/ak3-orca 시작점
INTEG=bfdfd5a39800d837ed5b4b529cd44061ec9da275  # chore/after-kaizen-0928 (이 가지 시작점)
PREV=a2e762c220bb1c5bdacf8f5cae463cc6c37047ec   # chore/ak3-orca 끝
T=$(mktemp -d "${TMPDIR:-/tmp}/ref3.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
git -C "$REPO" show "$PREV:$P" > "$T/prev" 2>/dev/null || { echo "STOP 앞 회차 판에 없음 $P" >&2; exit 2; }
if git -C "$REPO" diff --quiet "$BASE" "$INTEG" -- "$P"; then cat "$T/prev"; exit 0; fi
git -C "$REPO" show "$BASE:$P" > "$T/base" 2>/dev/null || : > "$T/base"
git -C "$REPO" show "$INTEG:$P" > "$T/integ" || exit 2
git merge-file -p --theirs "$T/integ" "$T/base" "$T/prev"
exit 0
