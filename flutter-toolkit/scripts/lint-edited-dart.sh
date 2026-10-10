#!/usr/bin/env bash
# record: PostToolUse(Edit|Write|MultiEdit) 훅 — 고친 .dart 파일 경로를 세션별 기록에 적기만 한다.
# check : Stop 훅 — 그 기록의 파일만 dart analyze 해서 오류·경고가 있으면 종료 코드 2 로 돌려보낸다.
# 끄기: FLUTTER_TOOLKIT_LINT_ON_STOP=off
#
# 편집마다 분석하지 않는 이유: 큰 프로젝트는 파일 하나 분석에 40 초 넘게 걸렸다 (2026-10-10 실측).
# 분석기를 못 돌리면 막지 않고 systemMessage 로 알린다 — 훅이 죽어 모든 세션을 막는 것이 더 나쁘다.
# set -e 금지 — 중간 실패가 0 아닌 종료로 새면 훅 오류로 뜬다.

[ "${FLUTTER_TOOLKIT_LINT_ON_STOP:-on}" = "off" ] && exit 0
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
session=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
[ -n "$session" ] || exit 0
state_dir="${CLAUDE_LINT_STATE_DIR:-${TMPDIR:-/tmp}/claude-lint-edited}"
edited_list="$state_dir/dart-$session"

case "${1:-}" in
  record)
    file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    case "$file" in
      *.dart) ;;
      *) exit 0 ;;
    esac
    # 생성물은 코드 생성기가 다시 쓴다
    [[ "$file" =~ \.(g|freezed|gr|mocks|config|gen)\.dart$ ]] && exit 0
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

# 파일마다 pubspec.yaml 이 있는 프로젝트 폴더를 찾아 "폴더<TAB>파일" 로 묶는다
pairs=$(sort -u "$edited_list" | while IFS= read -r file; do
  [ -f "$file" ] || continue
  dir=${file%/*}
  while [ ! -f "$dir/pubspec.yaml" ]; do
    up=${dir%/*}
    if [ -z "$up" ] || [ "$up" = "$dir" ]; then dir=""; break; fi
    dir=$up
  done
  [ -n "$dir" ] && printf '%s\t%s\n' "$dir" "$file"
done)

findings=""
unchecked=""
while IFS= read -r project; do
  [ -n "$project" ] || continue
  files=()
  while IFS= read -r file; do files+=("$file"); done < <(printf '%s\n' "$pairs" | awk -F'\t' -v p="$project" '$1 == p { print $2 }')

  # fvm 은 현재 폴더의 .fvmrc 로 버전을 고르므로 프로젝트 폴더에서 부른다
  if [ -f "$project/.fvmrc" ] || [ -d "$project/.fvm" ]; then
    analyzer=(fvm dart analyze)
  else
    analyzer=(dart analyze)
  fi
  if ! command -v "${analyzer[0]}" >/dev/null 2>&1; then
    unchecked="$unchecked $project(${analyzer[0]} 없음)"
    continue
  fi
  output=$(cd "$project" && "${analyzer[@]}" "${files[@]}" </dev/null 2>&1)
  status=$?
  # dart analyze 는 0~3 으로 끝난다 (3 오류 · 2 경고 · 1 정보). 그 밖은 분석기 자체가 실패한 것
  if [ "$status" -gt 3 ]; then
    unchecked="$unchecked $project(dart analyze 종료 코드 $status)"
    continue
  fi
  lines=$(printf '%s\n' "$output" | grep -E '^[[:space:]]*(error|warning) - ' | sed -E 's/^[[:space:]]+//')
  [ -n "$lines" ] && findings="$findings$lines"$'\n'
done < <(printf '%s\n' "$pairs" | cut -f1 | sort -u)

if [ -n "$findings" ]; then
  {
    echo "고친 Dart 파일에 분석 오류·경고가 남아 있습니다. 고친 뒤 끝내세요."
    [ -n "$unchecked" ] && echo "검사 못 함:$unchecked"
    printf '%s' "$findings"
  } >&2
  exit 2
fi

rm -f "$edited_list"
if [ -n "$unchecked" ]; then
  jq -nc --arg m "flutter-toolkit: 고친 Dart 파일을 검사 못 함 —$unchecked" '{systemMessage: $m}'
fi
exit 0
