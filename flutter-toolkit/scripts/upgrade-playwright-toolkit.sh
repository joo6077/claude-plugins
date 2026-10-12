#!/usr/bin/env bash
# SessionStart 훅 — 세션 폴더의 flutter_playwright_toolkit 이 최신 toolkit-v* 태그보다 낡았으면 뒤에서 pub upgrade 를 돌린다.
# 끄기: FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE=off · 확인 주기(초): FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_TTL (기본 3600)
# 상태 폴더: FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_STATE
#
# pub upgrade 는 실측 98 초가 걸려 세션 시작에서 기다릴 수 없다. 지금 세션에는 시작 한 줄만,
# 결과는 다음 세션 시작 때 한 줄로 낸다. 커밋은 하지 않는다.
# 어떤 경우에도 exit 0 — 세션 시작을 막으면 안 된다. set -e 금지.

PACKAGE=flutter_playwright_toolkit
STATE=${FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_STATE:-${XDG_STATE_HOME:-$HOME/.local/state}/flutter-toolkit/playwright-upgrade}
TTL=${FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE_TTL:-3600}
GIT_LIMIT=10

# pubspec.yaml 의 의존 블록에서 "git tag_pattern ref url 범위" 를 탭으로 잇는다
read_dependency() {
  awk -v pkg="$PACKAGE" '
    function indent(s) { match(s, /^ */); return RLENGTH }
    /^[^ #]/ { section = $1 }
    !inblock && $0 ~ "^ +" pkg ":[[:space:]]*$" {
      if (section == "dependency_overrides:") { override = 1; next }
      inblock = 1; base = indent($0); next
    }
    inblock {
      if ($0 ~ /^[[:space:]]*$/) next
      if (indent($0) <= base) { inblock = 0; next }
      line = $0; sub(/^ +/, "", line)
      if (line ~ /^git:/) git = 1
      if (line ~ /^tag_pattern:/) tag = 1
      if (line ~ /^ref:/) ref = 1
      if (line ~ /^url:/) { url = line; sub(/^url:[[:space:]]*/, "", url) }
      if (line ~ /^version:/ && indent($0) == base + 2) { range = line; sub(/^version:[[:space:]]*/, "", range); gsub(/["\047]/, "", range) }
    }
    END { if (!override) printf "%d\t%d\t%d\t%s\t%s\n", git, tag, ref, url, range }
  ' "$1"
}

locked_version() {
  awk -v pkg="$PACKAGE" '
    $0 == "  " pkg ":" { inblock = 1; next }
    inblock && /^  [^ ]/ { exit }
    inblock && /^    version:/ { v = $2; gsub(/"/, "", v); print v; exit }
  ' "$1"
}

version_key() {
  local IFS=.
  # shellcheck disable=SC2086
  set -- $1
  printf '%05d%05d%05d' "$1" "$2" "$3"
}

# 범위 위끝(제외). ^A 는 pub 규칙대로 첫 0 아닌 자리를 올린다
range_upper() {
  local range=$1 major minor patch
  case "$range" in
    *'<'*) range=${range##*<}; printf '%s' "${range%% *}" ;;
    '^'*)
      IFS=. read -r major minor patch <<<"${range#^}"
      if [ "$major" -gt 0 ]; then printf '%s' "$((major + 1)).0.0"
      elif [ "$minor" -gt 0 ]; then printf '%s' "0.$((minor + 1)).0"
      else printf '%s' "0.0.$((patch + 1))"
      fi ;;
  esac
}

newest_tag() { # newest_tag <ls-remote 출력 파일> <범위>
  local upper best="" best_key="" tag key
  upper=$(range_upper "$2")
  while IFS= read -r tag; do
    [[ "$tag" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || continue
    key=$(version_key "$tag")
    if [ -n "$upper" ] && [[ ! "$key" < "$(version_key "$upper")" ]]; then continue; fi
    if [ -z "$best_key" ] || [[ "$key" > "$best_key" ]]; then best=$tag; best_key=$key; fi
  done < <(sed -n 's#.*refs/tags/toolkit-v##p' "$1")
  printf '%s' "$best"
}

modified_at() { stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null; }

hash_path() {
  if command -v shasum >/dev/null 2>&1; then printf '%s' "$1" | shasum -a 256 | cut -c1-16
  else printf '%s' "$1" | sha256sum | cut -c1-16
  fi
}

upgrade_command() {
  if [ -f "$1/.fvmrc" ] || [ -d "$1/.fvm" ]; then echo "fvm flutter pub upgrade $PACKAGE"
  else echo "flutter pub upgrade $PACKAGE"
  fi
}

# 뒤쪽 일꾼 — 훅이 끝나도 살아남도록 새 세션에서 돈다
run_worker() {
  local dir=$1 prefix=$2 from=$3 to=$4 cmd rc now
  cmd=$(upgrade_command "$dir")
  (cd "$dir" && $cmd) </dev/null >"$prefix.log" 2>&1
  rc=$?
  now=$(locked_version "$dir/pubspec.lock")
  if [ "$rc" -eq 0 ] && [ "$now" = "$to" ]; then
    echo "$PACKAGE 을 $from → $to 로 올렸다 ($dir). pubspec.lock 이 바뀌었고 커밋은 하지 않았다." > "$prefix.result"
  else
    echo "$PACKAGE 올리기 실패 ($dir, $from → $to, 종료 코드 $rc). 손으로 돌릴 명령: cd '$dir' && $cmd — 기록 $prefix.log" > "$prefix.result"
  fi
  rm -f "$prefix.running"
  : > "$prefix.done"
}

detach() {
  if command -v setsid >/dev/null 2>&1; then setsid "$@"
  elif command -v perl >/dev/null 2>&1; then perl -MPOSIX -e 'POSIX::setsid(); exec @ARGV' "$@"
  else "$@"
  fi
}

check_project() {
  local dir=$1 fields git tag ref url range from prefix pid tags to
  fields=$(read_dependency "$dir/pubspec.yaml")
  IFS=$'\t' read -r git tag ref url range <<<"$fields"
  [ "$git" = 1 ] && [ "$tag" = 1 ] && [ "$ref" != 1 ] && [ -n "$url" ] || return 0
  [ -f "$dir/pubspec.lock" ] || return 0
  from=$(locked_version "$dir/pubspec.lock")
  [ -n "$from" ] || return 0

  prefix=$STATE/$(hash_path "$dir")
  if [ -f "$prefix.result" ]; then
    cat "$prefix.result"
    rm -f "$prefix.result"
  fi
  if [ -f "$prefix.running" ]; then
    pid=$(cat "$prefix.running" 2>/dev/null)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then return 0; fi
    rm -f "$prefix.running"
  fi
  if [ -f "$prefix.checked" ] && [ $(( $(date +%s) - $(modified_at "$prefix.checked") )) -lt "$TTL" ]; then
    return 0
  fi
  : > "$prefix.checked"

  # 표준 출력을 파이프가 아니라 파일로 받는다 — 끊긴 git 의 자식이 파이프를 물면 훅이 같이 멈춘다
  tags=$prefix.tags
  GIT_TERMINAL_PROMPT=0 git ls-remote --tags --refs "$url" 'toolkit-v*' </dev/null >"$tags" 2>/dev/null &
  local git_pid=$!
  ( sleep "$GIT_LIMIT"; kill "$git_pid" 2>/dev/null ) </dev/null >/dev/null 2>&1 &
  local guard=$!
  wait "$git_pid" || { kill "$guard" 2>/dev/null; return 0; }
  kill "$guard" 2>/dev/null

  to=$(newest_tag "$tags" "$range")
  [ -n "$to" ] || return 0
  [[ "$(version_key "$to")" > "$(version_key "$from")" ]] || return 0

  rm -f "$prefix.done"
  ( detach bash "$0" --worker "$dir" "$prefix" "$from" "$to" ) </dev/null >/dev/null 2>&1 &
  echo $! > "$prefix.running"
  echo "$PACKAGE $from → $to 올리는 중 ($dir) — 뒤에서 $(upgrade_command "$dir") 를 돌린다. 결과는 다음 세션 시작 때 알린다."
}

if [ "${1:-}" = "--worker" ]; then
  shift
  run_worker "$@"
  exit 0
fi

[ "${FLUTTER_TOOLKIT_PLAYWRIGHT_UPGRADE:-on}" = "off" ] && exit 0
command -v git >/dev/null 2>&1 || exit 0

input=""
[ -t 0 ] || input=$(cat 2>/dev/null)
root=""
if [ -n "$input" ] && command -v jq >/dev/null 2>&1; then
  root=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)
fi
root=${root:-${CLAUDE_PROJECT_DIR:-$PWD}}
[ -d "$root" ] || exit 0
mkdir -p "$STATE" 2>/dev/null || exit 0

while IFS= read -r pubspec; do
  check_project "${pubspec%/pubspec.yaml}"
done < <(find "$root" -maxdepth 3 \
  \( -name build -o -name .dart_tool -o -name .fvm -o -name node_modules -o -name .git \
     -o -name ios -o -name android -o -name macos -o -name linux -o -name windows -o -name web \) -prune \
  -o -type f -name pubspec.yaml -print 2>/dev/null)
exit 0
