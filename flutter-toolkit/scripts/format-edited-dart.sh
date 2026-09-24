#!/usr/bin/env bash
# PostToolUse(Edit|Write|MultiEdit) 훅 — 방금 고친 .dart 파일 하나만 dart format 한다.
# 끄기: FLUTTER_TOOLKIT_FORMAT_ON_EDIT=off
#
# 어떤 경우에도 exit 0 · stdout 빈 값 — 포맷 실패가 편집 흐름에 끼어들면 안 된다.
# set -e 금지 — 중간 실패가 0 아닌 종료로 새면 훅 오류로 뜬다.

[ "${FLUTTER_TOOLKIT_FORMAT_ON_EDIT:-on}" = "off" ] && exit 0
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
[ -n "$input" ] || exit 0
file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
[ -n "$file" ] || exit 0

case "$file" in
  *.dart) ;;
  *) exit 0 ;;
esac
# 생성물은 코드 생성기가 다시 쓴다. 포맷하면 산출물 변경이 수기 변경 목록에 섞인다
[[ "$file" =~ \.(g|freezed|gr|mocks|config|gen)\.dart$ ]] && exit 0

case "$file" in
  /*) ;;
  *)
    cwd=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)
    file="${cwd:-$PWD}/$file"
    ;;
esac
[ -f "$file" ] || exit 0

dir=${file%/*}
while [ ! -f "$dir/pubspec.yaml" ]; do
  up=${dir%/*}
  # 슬래시 없는 경로(윈도 역슬래시)는 값이 안 줄어 같은 자리를 계속 돈다
  if [ -z "$up" ] || [ "$up" = "$dir" ]; then exit 0; fi
  dir=$up
done

# fvm 은 현재 폴더의 .fvmrc 로 버전을 고르므로 프로젝트 폴더에서 부른다.
# stdin 을 닫는다 — 무언가 물으면 답을 기다리다 시간 제한까지 멈춘다
if [ -f "$dir/.fvmrc" ] || [ -d "$dir/.fvm" ]; then
  command -v fvm >/dev/null 2>&1 || exit 0
  (cd "$dir" && fvm dart format -- "$file") </dev/null >/dev/null 2>&1
else
  command -v dart >/dev/null 2>&1 || exit 0
  (cd "$dir" && dart format -- "$file") </dev/null >/dev/null 2>&1
fi
exit 0
