#!/usr/bin/env bash
# m-qapending-run.sh <훅 파일> — 레포 밖 qa-pending-check.sh 를 통째로 돌려, 머리 값 뒤에 줄 끝 주석이 붙은
# 이 세션 소유 진행 중 계약(QA 결과 파일 없음)을 붙잡는지 본다. 임시 프로젝트는 끝나면 지운다.
# 경우 둘: plain(`status: active`) · cmt(`status: active   # 진행 중` 과 `owner_session: S1  # 이 세션`).
# 출력: 경우마다 `<이름> rc=<종료 코드> caught=<출력에 계약 파일 이름이 있으면 1>`.
H=${1:?훅 파일}
T=$(mktemp -d "${TMPDIR:-/tmp}/mqapr.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
one() {  # one <이름> <status 줄> <owner 줄>
  p="$T/$1"; mkdir -p "$p/.harness"
  printf -- '---\nslug: x\n%s\n%s\nlocked_at: "2026-09-28 10:00"\n---\n\n## Script\n\n- [ ] SC-01: x\n' "$2" "$3" > "$p/.harness/sprint-contract-x.md"
  out=$(printf '{"session_id":"S1","cwd":"%s","transcript_path":"","stop_hook_active":false}' "$p" | bash "$H" 2>&1)
  rc=$?
  c=0; printf '%s' "$out" | grep -q 'sprint-contract-x.md' && c=1
  echo "$1 rc=$rc caught=$c"
}
one plain 'status: active' 'owner_session: S1'
one cmt 'status: active   # 진행 중' 'owner_session: S1  # 이 세션'
