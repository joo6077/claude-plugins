#!/usr/bin/env bash
# record: PostToolUse(Edit|Write|MultiEdit) 훅 — 고친 .rs 파일 경로를 세션별 기록에 적기만 한다.
# check : Stop 훅 — 워크스페이스마다 cargo clippy 를 한 번 돌려 기록한 파일의 경고·오류 줄만 골라
#         있으면 종료 코드 2 로 돌려보낸다.
# 끄기: RUST_KIT_LINT_ON_STOP=off
#
# 편집마다 돌리지 않는 이유: 파일 하나 바꾼 뒤 clippy 가 10 초 넘게 걸렸다 (2026-10-10 실측).
# 분석기를 못 돌리면 막지 않고 systemMessage 로 알린다 — 훅이 죽어 모든 세션을 막는 것이 더 나쁘다.
# set -e 금지 — 중간 실패가 0 아닌 종료로 새면 훅 오류로 뜬다.

[ "${RUST_KIT_LINT_ON_STOP:-on}" = "off" ] && exit 0
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
session=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
[ -n "$session" ] || exit 0
state_dir="${CLAUDE_LINT_STATE_DIR:-${TMPDIR:-/tmp}/claude-lint-edited}"
edited_list="$state_dir/rust-$session"

case "${1:-}" in
  record)
    file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    case "$file" in
      *.rs) ;;
      *) exit 0 ;;
    esac
    case "$file" in
      /*) ;;
      *)
        cwd=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)
        file="${cwd:-$PWD}/$file"
        ;;
    esac
    mkdir -p "$state_dir" && printf '%s\n' "$file" >> "$edited_list"
    exit 0
    ;;
  check) ;;
  *) exit 0 ;;
esac

# 이미 한 번 막혀 이어 가는 중이면 통과시킨다. 기록은 남겨 다음 끝내기 때 다시 잰다
[ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false' 2>/dev/null)" = "true" ] && exit 0
[ -s "$edited_list" ] || exit 0

if ! command -v cargo >/dev/null 2>&1; then
  rm -f "$edited_list"
  jq -nc '{systemMessage: "rust-kit: 고친 Rust 파일을 검사 못 함 — cargo 없음"}'
  exit 0
fi

# 파일마다 워크스페이스 폴더를 찾아 "폴더<TAB>워크스페이스 기준 상대 경로" 로 묶는다.
# clippy 는 워크스페이스 기준 상대 경로로 줄을 내므로 같은 꼴로 맞춘다.
# /var 와 /private/var 처럼 같은 폴더가 두 이름을 가지면 접두가 안 맞아 pwd -P 로 실제 경로를 쓴다
pairs=$(sort -u "$edited_list" | while IFS= read -r file; do
  [ -f "$file" ] || continue
  dir=$(cd "${file%/*}" && pwd -P) || continue
  manifest=$(cd "$dir" && cargo locate-project --workspace --message-format plain </dev/null 2>/dev/null) || continue
  workspace=$(cd "${manifest%/*}" && pwd -P)
  printf '%s\t%s\n' "$workspace" "${dir#"$workspace"/}/${file##*/}"
done)

findings=""
unchecked=""
while IFS= read -r workspace; do
  [ -n "$workspace" ] || continue
  output=$(cd "$workspace" && cargo clippy --quiet --message-format=short </dev/null 2>&1)
  status=$?
  # clippy 는 경고만 있으면 0, 컴파일 오류면 101 로 끝난다. 그 밖은 cargo 자체가 실패한 것
  if [ "$status" -ne 0 ] && [ "$status" -ne 101 ]; then
    unchecked="$unchecked $workspace(cargo clippy 종료 코드 $status)"
    continue
  fi
  lines=$(printf '%s\n' "$pairs" | awk -F'\t' -v w="$workspace" '$1 == w { print $2 }' | while IFS= read -r relative; do
    printf '%s\n' "$output" | grep -F "$relative:" | grep -E ':[0-9]+:[0-9]+: (warning|error)'
  done)
  if [ -n "$lines" ]; then
    findings="$findings$lines"$'\n'
  elif [ "$status" -eq 101 ]; then
    # 다른 파일의 컴파일 오류로 기록한 파일까지 검사가 닿지 못했다
    unchecked="$unchecked $workspace(다른 파일 컴파일 오류)"
  fi
done < <(printf '%s\n' "$pairs" | cut -f1 | sort -u)

if [ -n "$findings" ]; then
  {
    echo "고친 Rust 파일에 clippy 경고·오류가 남아 있습니다. 고친 뒤 끝내세요."
    [ -n "$unchecked" ] && echo "검사 못 함:$unchecked"
    printf '%s' "$findings"
  } >&2
  exit 2
fi

rm -f "$edited_list"
if [ -n "$unchecked" ]; then
  jq -nc --arg m "rust-kit: 고친 Rust 파일을 검사 못 함 —$unchecked" '{systemMessage: $m}'
fi
exit 0
