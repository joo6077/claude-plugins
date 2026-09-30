#!/usr/bin/env bash
# 커밋 안전 훅. Claude Code 의 Bash PreToolUse · PostToolUse 에서 부른다.
#   commit-guard.sh pre   커밋 직전. 삭제 50 개 초과 · 남의 커밋 되돌림 · 빈 개인 목록 · 계약 범위 목록 밖 경로면 exit 2
#   commit-guard.sh post  커밋 직후. 방금 커밋의 삭제가 50 개를 넘으면 알리기만 한다
#
# 훅이 죽어서 정상 커밋을 막는 것이 훅이 없는 것보다 나쁘다. 그래서 set -e 를 쓰지 않고,
# 판단이 안 서는 입력(빈 stdin · 깨진 JSON · 풀 수 없는 cd)은 조용히 통과시킨다.
# macOS 기본 /bin/bash 3.2 에서도 돌아야 한다 — 연관 배열 · mapfile 금지.

mode=${1:-pre}
limit=50

[ "${HARNESS_COMMIT_GUARD:-}" = off ] && exit 0
payload=$(cat 2>/dev/null)
[ -n "$payload" ] || exit 0

if ! command -v jq >/dev/null 2>&1; then
  # 조용히 넘기면 검사가 돈 줄 알고 커밋한다
  if [ "$mode" = pre ] && printf '%s' "$payload" | grep -qE 'git[^"]*[[:space:]]commit'; then
    printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"커밋 안전 훅이 jq 가 없어 검사를 못 했다. 커밋 전에 git diff --cached --stat 으로 삭제 수를 직접 확인한다."}}'
  fi
  exit 0
fi

cmd=$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null)
case $cmd in *commit*) ;; *) exit 0 ;; esac
cwd=$(printf '%s' "$payload" | jq -r '.cwd // empty' 2>/dev/null)
[ -n "$cwd" ] || cwd=$PWD

# 명령을 단순 명령 하나당 한 줄로, 낱말은 \037 로 이어 낸다. heredoc 본문은 버린다 —
# 커밋 메시지 본문에 든 "git commit" 글자를 커밋으로 읽으면 안 된다.
split_commands() {
  awk '
  function word_end() { if (inword) { seg = seg (nw ? US : "") word; nw++; word = ""; inword = 0 } }
  function seg_end() { word_end(); if (nw) print seg; seg = ""; nw = 0 }
  BEGIN { US = sprintf("%c", 31); SQ = sprintf("%c", 39) }
  hcur < hcnt {
    t = $0
    if (hdash[hcur]) sub(/^\t+/, "", t)
    if (t == hdelim[hcur]) hcur++
    next
  }
  {
    line = $0; n = length(line); cont = 0
    for (i = 1; i <= n; i++) {
      c = substr(line, i, 1)
      if (sq) { if (c == SQ) sq = 0; else word = word c; continue }
      # 큰따옴표 안의 << 는 "$(cat <<EOF" 꼴일 때만 heredoc 이다
      if (c == "<" && substr(line, i + 1, 1) == "<" && substr(line, i + 2, 1) != "<" && (!dq || index(word, "$("))) {
        j = i + 2; dash = 0
        if (substr(line, j, 1) == "-") { dash = 1; j++ }
        while (substr(line, j, 1) ~ /[ \t]/) j++
        d = ""
        for (; j <= n; j++) {
          cc = substr(line, j, 1)
          if (cc ~ /[ \t;&|()<>]/) break
          if (cc != SQ && cc != "\"" && cc != "\\") d = d cc
        }
        if (d != "") { hdelim[hpend] = d; hdash[hpend] = dash; hpend++ }
        i = j - 1
        continue
      }
      if (dq) {
        if (c == "\\" && i < n) { i++; word = word substr(line, i, 1); continue }
        if (c == "\"") dq = 0; else word = word c
        continue
      }
      if (c == "\\") { if (i == n) { cont = 1; break } i++; word = word substr(line, i, 1); inword = 1; continue }
      if (c == SQ) { sq = 1; inword = 1; continue }
      if (c == "\"") { dq = 1; inword = 1; continue }
      if (c == " " || c == "\t") { word_end(); continue }
      if (c ~ /[;&|()]/) { seg_end(); continue }
      if (c == "#" && !inword) break
      word = word c; inword = 1
    }
    if (sq || dq) word = word " "
    else if (!cont) seg_end()
    if (hpend) { hcnt = hpend; hcur = 0; hpend = 0 }
  }
  END { seg_end() }'
}

resolve_dir() {  # resolve_dir <기준 폴더> <경로>
  local p=$2
  case $p in
    *'$'* | *'`'* | *'*'* | *'?'* | *'['*) return 1 ;;
    \~) p=$HOME ;;
    \~/*) p=$HOME/${p#\~/} ;;
    \~*) return 1 ;;
  esac
  case $p in /*) ;; *) p=$1/$p ;; esac
  printf '%s\n' "$p"
}

# core.quotePath=false — 한글 이름이 "\355..." 꼴로 감싸지면 상위 폴더 집계가 깨진다
g() {
  if [ -n "$g_index" ]; then
    GIT_INDEX_FILE=$g_index git -C "$g_dir" -c core.quotePath=false "$@" 2>/dev/null
  else
    git -C "$g_dir" -c core.quotePath=false "$@" 2>/dev/null
  fi
}

top_dirs() {  # 삭제 이름 목록에서 상위 폴더 최대 5 개와 개수
  printf '%s\n' "$1" | awk -F/ 'NF { print (NF > 1 ? $1 "/" : "(최상위)") }' \
    | sort | uniq -c | sort -rn | head -5 | sed -E 's/^ *([0-9]+) (.*)$/  \2 \1 개/'
}

block() {  # block <이유 한 줄> [본문]
  {
    printf '커밋 안전 훅: %s\n' "$1"
    [ -n "${2:-}" ] && printf '%s\n' "$2"
    printf '의도한 것이면 HARNESS_COMMIT_GUARD=off 를 git commit 명령 앞에 붙인다 — 개수와 폴더를 사용자에게 보여 주고 승인을 받은 뒤에만.\n'
  } >&2
  exit 2
}

block_deleted() {  # block_deleted <개수> <이름 목록> <작업 폴더 삭제 목록>
  block "삭제 $1 개가 실린 커밋을 막았다 (기준 $limit 개 초과${3:+ · 같은 명령의 git add · -a · -i 가 올릴 작업 폴더 삭제 포함})." "상위 폴더:
$(top_dirs "$2")
확인: git diff --cached --stat --diff-filter=D"
}

parse_commit_args() {
  c_all=0 c_incl=0 c_paths=0 c_dry=0 c_pfile=0
  c_pathv=()
  local a take=0 after_dd=0 k ch
  for a in "$@"; do
    if [ "$take" = 1 ]; then take=0; continue; fi
    if [ "$after_dd" = 1 ]; then c_paths=$((c_paths + 1)); c_pathv+=("$a"); continue; fi
    case $a in
      --) after_dd=1 ;;
      --all) c_all=1 ;;
      --include) c_incl=1 ;;
      --dry-run) c_dry=1 ;;
      --pathspec-from-file=*) c_paths=$((c_paths + 1)); c_pfile=1 ;;
      --pathspec-from-file) c_paths=$((c_paths + 1)); c_pfile=1; take=1 ;;
      --message | --file | --author | --date | --reuse-message | --reedit-message | --fixup | --squash | --template | --cleanup | --trailer) take=1 ;;
      --*) ;;
      -*)
        k=1
        while [ "$k" -lt "${#a}" ]; do
          ch=${a:k:1}
          case $ch in
            a) c_all=1 ;;
            i) c_incl=1 ;;
            m | F | C | c | t) [ $((k + 1)) -lt "${#a}" ] || take=1; break ;;
            u | S) break ;;
          esac
          k=$((k + 1))
        done
        ;;
      [0-9]*'>'* | [0-9]*'<'* | '>'* | '<'*)
        case $a in *[!0-9\<\>]*) ;; *) take=1 ;; esac
        ;;
      *) c_paths=$((c_paths + 1)); c_pathv+=("$a") ;;
    esac
  done
}

# overlay_deletes <목록 파일> <이름 목록> — 목록 파일에 그 이름들의 작업 폴더 상태를 얹고, git 처럼 이름 바꾸기(-M)를
# 가려 남는 삭제 이름을 낸다. 파일 수로 세면 git mv 로 옮긴 폴더가 통째로 삭제로 보인다.
# 희소 체크아웃으로 꺼내지 않은 파일(ls-files -t 의 S)은 작업 폴더에 없어도 git 이 싣지 않으므로 얹지 않는다
overlay_deletes() {
  local idx=$1 top names name
  top=$(g rev-parse --show-toplevel) || return 0
  names=$(comm -23 <(printf '%s\n' "$2" | grep . | sort -u) \
    <(g ls-files -t --full-name -- "${c_pathv[@]}" | sed -n 's/^S //p' | sort))
  # 파일 자리가 폴더로(또는 그 반대로) 바뀐 이름은 --replace 가 없으면 update-index 가 통째로 실패한다 — git add 처럼 바꿔 넣는다
  if printf '%s\n' "$names" | grep . | GIT_INDEX_FILE=$idx git -C "$top" update-index --add --remove --replace --stdin 2>/dev/null; then
    GIT_INDEX_FILE=$idx git -C "$top" -c core.quotePath=false diff --cached -M --diff-filter=D --name-only HEAD 2>/dev/null
    return 0
  fi
  # 그래도 못 얹으면(읽을 수 없는 새 파일 등) 이름 바꾸기를 가리지 않고 작업 폴더에 없는 이름을 삭제로 더한다 — 빈 값을 내면 목록의 삭제까지 빠진다
  {
    GIT_INDEX_FILE=$idx git -C "$top" -c core.quotePath=false diff --cached -M --diff-filter=D --name-only HEAD 2>/dev/null
    printf '%s\n' "$names" | while IFS= read -r name; do
      [ -z "$name" ] || [ -e "$top/$name" ] || [ -L "$top/$name" ] || printf '%s\n' "$name"
    done
  } | sort -u
}

# 경로 지정 커밋은 공용 목록이 아니라 HEAD 위에 그 경로의 작업 폴더 상태를 얹는다. 목록으로 세면
# 목록에서만 뺀 파일(rm --cached)이나 빈 개인 목록을 삭제로 잘못 세고, 목록에 없는 작업 폴더 삭제는 놓친다.
# git 이 얹는 파일은 HEAD 와 실제 목록의 합이다 — 새 경로만 목록에 있는 이동(git mv)도 그래서 이름 바꾸기로 잡힌다
check_path_commit() {  # check_path_commit <저장소 폴더>
  local d=$1 t names n
  [ "$c_pfile" = 1 ] && return 0   # 경로를 파일로 넘기면 대상을 모른다
  g rev-parse -q --verify HEAD >/dev/null || return 0
  t=$(mktemp -d "${TMPDIR:-/tmp}/commit-guard.XXXXXX") || return 0
  names=$(GIT_INDEX_FILE=$t/index git -C "$d" read-tree HEAD 2>/dev/null &&
    overlay_deletes "$t/index" "$(GIT_INDEX_FILE=$t/index git -C "$d" -c core.quotePath=false ls-files --full-name -- "${c_pathv[@]}" 2>/dev/null
      g ls-files --full-name -- "${c_pathv[@]}")")
  rm -rf "$t"
  n=$(printf '%s\n' "$names" | grep -c .)
  [ "$n" -gt "$limit" ] && block "삭제 $n 개가 실린 커밋을 막았다 (기준 $limit 개 초과 · 지정한 경로 안에서 작업 폴더에 없는 추적 파일)." "상위 폴더:
$(top_dirs "$names")
확인: git status --short -- <지정한 경로>"
  check_scope "$d" "$(carried_paths "" "$(g ls-tree -r --full-name --name-only HEAD -- "${c_pathv[@]}"
    g ls-files --full-name -- "${c_pathv[@]}")")"
}

# carried_paths <목록 파일 | 빈 값> <얹을 이름 목록> — 이 커밋이 싣는 경로를 이름 바꾸기 없이 낸다.
# 목록 파일이 빈 값이면 HEAD 에서 시작한다(경로 지정 커밋). 이름 바꾸기로 묶으면 범위 밖으로 옮긴 새 경로가 옛 경로 뒤에 숨는다
carried_paths() {
  local top t
  g rev-parse -q --verify HEAD >/dev/null || return 0
  top=$(g rev-parse --show-toplevel) || return 0
  t=$(mktemp -d "${TMPDIR:-/tmp}/commit-guard.XXXXXX") || return 0
  if [ -n "$1" ]; then
    cp "$1" "$t/index" 2>/dev/null || { rm -rf "$t"; return 0; }
  else
    GIT_INDEX_FILE=$t/index git -C "$top" read-tree HEAD 2>/dev/null || { rm -rf "$t"; return 0; }
  fi
  printf '%s\n' "$2" | grep . | sort -u | GIT_INDEX_FILE=$t/index git -C "$top" update-index --add --remove --replace --stdin 2>/dev/null
  GIT_INDEX_FILE=$t/index git -C "$top" -c core.quotePath=false diff --cached --no-renames --name-only HEAD 2>/dev/null
  rm -rf "$t"
}

# scope_blocks <계약 폴더> <세션> — 그 폴더 .harness/ 의 계약 가운데 status: active 이고 owner_session 이 세션과 같은 것의
# 「## 범위 경계」 절 안 # sprint-scope 블록 줄을 낸다. 규약: harness/references/contract-schema.md §범위 목록 블록
scope_blocks() {
  local f
  find "$1/.harness" -maxdepth 1 -type f -name 'sprint-contract*.md' 2>/dev/null | while IFS= read -r f; do
    [ -r "$f" ] || continue
    awk -v s="$2" '
      # 계약 형식 문서 §값 따옴표 규약의 fm_get 과 같게 읽는다 — 따옴표 벗기기 · 빈칸이나 탭 뒤 # 부터는 주석
      function val(l,  c, e) {
        sub(/^[^:]*:[[:space:]]*/, "", l); c = substr(l, 1, 1); e = index(substr(l, 2), c)
        if ((c == "\"" || c == SQ) && e > 0) return substr(l, 2, e - 1)
        if (c == "#") return ""
        if (match(l, /[ \t]#/)) l = substr(l, 1, RSTART - 1)
        sub(/[[:space:]]+$/, "", l); return l
      }
      BEGIN { SQ = sprintf("%c", 39) }
      NR == 1 { if ($0 ~ /^---[[:space:]]*$/) { fm = 1; next } exit }
      fm && /^---[[:space:]]*$/ { fm = 0; if (st != "active" || ow != s) exit; next }
      fm && /^status:/ { st = val($0); next }
      fm && /^owner_session:/ { ow = val($0); next }
      fm { next }
      /^[[:space:]]*(```|~~~)/ { if (fence) { fence = 0; blk = 0 } else { fence = 1; first = 1; blk = (sect && $0 ~ /^```text[[:space:]]*$/) } next }
      fence && first { first = 0; if ($0 != "# sprint-scope") blk = 0; next }
      fence && blk && NF && $0 !~ /^#/ { sub(/[[:space:]]+$/, ""); print; next }
      fence { next }
      /^## / { sect = (index($0, "## 범위 경계") == 1) }
    ' "$f" 2>/dev/null
  done
}

# check_scope <저장소 폴더> <실린 경로 목록> — 이 세션의 활성 계약이 범위 목록을 적었으면 그 밖 경로를 싣는 커밋을 막는다.
# 판단이 안 서면(세션 없음 · 해당 계약 없음 · 블록 없음 · 못 읽음) 통과시킨다
check_scope() {
  local d=$1 sess root top rel pats out p pat hit
  sess=$(printf '%s' "$payload" | jq -r '.session_id // empty' 2>/dev/null)
  [ -n "$sess" ] || sess=${CLAUDE_CODE_SESSION_ID:-}
  [ -n "$sess" ] || return 0
  root=$d
  while [ ! -d "$root/.harness" ]; do
    [ "$root" = / ] && return 0
    root=$(dirname "$root")
  done
  root=$(cd "$root" 2>/dev/null && pwd -P) || return 0
  pats=$(scope_blocks "$root" "$sess" | sort -u)
  [ -n "$pats" ] || return 0
  top=$(g rev-parse --show-toplevel) || return 0
  case $root in "$top") rel="" ;; "$top"/*) rel=${root#"$top"/}/ ;; *) return 0 ;; esac
  out=$(printf '%s\n' "$2" | grep . | while IFS= read -r p; do
    case $p in "${rel}.harness/"*) continue ;; esac
    hit=0
    while IFS= read -r pat; do
      # shellcheck disable=SC2254  # 범위 목록 줄은 글롭 패턴이라 따옴표 없이 맞춘다
      case $pat in
        */) case $p in "$pat"*) hit=1 ;; esac ;;
        *) case $p in $pat | "$pat"/*) hit=1 ;; esac ;;
      esac
      [ "$hit" = 1 ] && break
    done <<<"$pats"
    [ "$hit" = 1 ] || printf '%s\n' "$p"
  done)
  [ -n "$out" ] || return 0
  block "계약 범위 목록 밖 경로 $(printf '%s\n' "$out" | grep -c .) 개를 싣는 커밋을 막았다 (이 세션의 활성 계약 # sprint-scope 블록 기준)." "$(printf '%s\n' "$out" | head -20 | sed 's/^/  /')
범위를 넓혀야 하면 계약 본문이 아니라 개정 파일에 적고 사용자 동의를 받는다."
}

check_commit_pre() {  # check_commit_pre <저장소 폴더> <GIT_INDEX_FILE 값> <commit 인자…>
  local d=$1 idx=$2 gd f staged extra worktree_deleted names del_count reverted shown more t src incl modified
  shift 2
  parse_commit_args "$@"
  [ "$c_dry" = 1 ] && return 0
  g_dir=$d g_index=""
  gd=$(g rev-parse --absolute-git-dir) || return 0
  [ -n "$gd" ] || return 0
  for f in MERGE_HEAD CHERRY_PICK_HEAD REVERT_HEAD; do
    [ -e "$gd/$f" ] && return 0
  done
  # 경로 지정 커밋은 공용 목록 전체를 싣지 않는다 (-i 는 목록 전체 + 경로)
  if [ "$c_paths" -gt 0 ] && [ "$c_incl" = 0 ]; then
    check_path_commit "$d"
    return 0
  fi

  if [ -n "$idx" ]; then
    case $idx in /*) ;; *) idx=$d/$idx ;; esac
    case $read_trees in *"|$idx|"*) return 0 ;; esac
    if [ ! -s "$idx" ]; then
      block "GIT_INDEX_FILE 로 지정한 개인 목록이 없거나 비어 있다: $idx" \
"이대로 커밋하면 HEAD 의 추적 파일 $(g ls-tree -r --name-only HEAD | grep -c .) 개 중 새로 올린 것 말고는 전부 삭제로 기록된다.
같은 명령 안에서 먼저 GIT_INDEX_FILE=$idx git read-tree HEAD 로 채운다."
    fi
    g_index=$idx
  fi

  staged=$(g diff --cached -M --diff-filter=D --name-only)
  extra=""
  src=${g_index:-$(g rev-parse --git-path index)}
  case $src in /*) ;; *) src=$d/$src ;; esac
  incl=""
  if [ "$c_incl" = 1 ] && [ "${#c_pathv[@]}" -gt 0 ]; then incl=$(g ls-files --full-name -- "${c_pathv[@]}"); fi
  # -a 와 같은 명령의 git add 는 작업 폴더 상태를, -i 는 지정한 경로의 작업 폴더 상태를 목록에 더해 싣는다.
  # 목록 사본에 얹어 세야 옮긴 폴더의 옛 경로가 삭제가 아니라 이름 바꾸기로 잡힌다
  if [ "$c_all" = 1 ] || [ "$add_all" = 1 ] || [ -n "$add_deleted" ] || [ -n "$incl" ]; then
    # -a 는 하위 폴더에서 불러도 저장소 전체 삭제를 싣는다 — 셸 위치 아래만 세면 폴더 밖 삭제를 놓친다
    worktree_deleted=$add_deleted
    [ "$c_all" = 1 ] && worktree_deleted="$worktree_deleted
$(g ls-files --full-name --deleted -- :/)"
    [ -n "$incl" ] && worktree_deleted="$worktree_deleted
$(g ls-files --full-name --deleted -- "${c_pathv[@]}")"
    t=$(mktemp -d "${TMPDIR:-/tmp}/commit-guard.XXXXXX") || return 0
    if cp "$src" "$t/index" 2>/dev/null; then
      # add -A · add . 는 새 파일도 올린다 — 새 경로가 사본에 없으면 이름 바꾸기로 잡히지 않는다
      staged=$(overlay_deletes "$t/index" "$(printf '%s\n%s\n%s\n' "$worktree_deleted" "$add_untracked" "$incl")")
    fi
    rm -rf "$t"
    # 목록에서 이미 지운 삭제만으로 막을 때는 막힘 설명에 작업 폴더 삭제를 적지 않는다
    extra=$(comm -12 <(printf '%s\n' "$staged" | sort) <(printf '%s\n' "$worktree_deleted" | sort) | grep .)
  fi
  names=$(printf '%s\n' "$staged" | grep -v '^$' | sort -u)
  del_count=$(printf '%s\n' "$names" | grep -c .)
  [ "$del_count" -gt "$limit" ] && block_deleted "$del_count" "$names" "$extra"
  modified=""
  [ "$c_all" = 1 ] && modified=$(g ls-files --full-name -m -d -- :/)
  check_scope "$d" "$(carried_paths "$src" "$(printf '%s\n%s\n%s\n%s\n' "$modified" "$add_changed" "$add_untracked" "$incl")")"

  # 다른 세션이 HEAD 를 옮긴 뒤 공용 목록에 남은 옛 내용 — 목록 ≠ HEAD, 목록 ≠ 작업 폴더, 작업 폴더 = HEAD
  [ "$c_all" = 1 ] || [ "$add_all" = 1 ] && return 0
  g rev-parse -q --verify HEAD >/dev/null || return 0
  reverted=$(comm -12 <(g diff --cached --name-only | sort) <(g diff --name-only | sort) \
    | comm -23 - <(g diff HEAD --name-only | sort))
  [ -n "$reverted" ] || return 0
  shown=$(printf '%s\n' "$reverted" | head -10 | sed 's/^/  /')
  more=$(($(printf '%s\n' "$reverted" | grep -c .) - 10))
  [ "$more" -gt 0 ] && shown="$shown
  외 $more 개"
  block "공용 목록의 옛 내용이 최근 커밋을 되돌리는 파일 $(printf '%s\n' "$reverted" | grep -c .) 개가 있어 막았다." "$shown
작업 폴더는 이미 HEAD 와 같다. git restore --staged <파일> 로 목록을 HEAD 에 맞춘 뒤 다시 커밋한다."
}

check_commit_post() {  # check_commit_post <저장소 폴더>
  local d=$1 ct names n dirs msg
  g_dir=$d g_index=""
  ct=$(g log -1 --format=%ct HEAD)
  [ -n "$ct" ] || return 0
  [ $(($(date +%s) - ct)) -le 60 ] || return 0
  names=$(g show -M --diff-filter=D --name-only --format= HEAD | grep -v '^$')
  n=$(printf '%s\n' "$names" | grep -c .)
  [ "$n" -gt "$limit" ] || return 0
  dirs=$(top_dirs "$names" | sed 's/^  //' | paste -sd ',' - | sed 's/,/, /g')
  msg="커밋 안전 훅: 방금 커밋 $(g rev-parse --short HEAD) 이 파일 $n 개를 삭제로 기록했다 (기준 $limit 개 초과, 상위 폴더: $dirs). 의도하지 않은 삭제면 사용자에게 알리고 git reset --soft HEAD~1 로 커밋만 되돌린다 — 변경은 공용 목록에 그대로 남는다."
  jq -nc --arg c "$msg" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $c}}'
  exit 0
}

handle_git() {  # handle_git <off> <GIT_INDEX_FILE 값> <git 인자…>
  local off=$1 idx=$2 gdir=$dir glost=$lost sub a take=0 after_dd=0 flag_all=0 flag_update=0 no_new=0 no_rm=0 spec_file=0
  local -a specs=()
  shift 2
  while [ $# -gt 0 ]; do
    case $1 in
      -C) gdir=$(resolve_dir "$gdir" "${2:-}") || glost=1; shift ;;
      -c | --namespace | --config-env | --super-prefix) shift ;;
      --git-dir | --work-tree) glost=1; shift ;;
      --git-dir=* | --work-tree=*) glost=1 ;;
      -*) ;;
      *) break ;;
    esac
    shift
  done
  sub=${1:-}
  [ $# -gt 0 ] && shift
  if [ -n "$idx" ]; then case $idx in /*) ;; *) idx=$gdir/$idx ;; esac; fi
  case $sub in
    add)
      for a in "$@"; do
        if [ "$take" = 1 ]; then take=0; continue; fi
        if [ "$after_dd" = 1 ]; then specs+=("$a"); continue; fi
        case $a in
          --) after_dd=1 ;;
          --update) flag_update=1 ;;
          --all | --no-ignore-removal) flag_all=1 ;;
          --dry-run | --interactive | --patch | --edit | --intent-to-add) no_new=1 ;;
          --ignore-removal | --no-all) no_rm=1 ;;
          --pathspec-from-file) spec_file=1; take=1 ;;
          --pathspec-from-file=*) spec_file=1 ;;
          --*) ;;
          -*)
            case $a in *A*) flag_all=1 ;; *u*) flag_update=1 ;; esac
            case $a in *[nipeN]*) no_new=1 ;; esac
            ;;
          [0-9]*'>'* | [0-9]*'<'* | '>'* | '<'*)
            case $a in *[!0-9\<\>]*) ;; *) take=1 ;; esac
            ;;
          *) specs+=("$a") ;;
        esac
      done
      { [ "$flag_all" = 1 ] || [ "$flag_update" = 1 ]; } && add_all=1
      for a in "${specs[@]}"; do case $a in . | :/) add_all=1 ;; esac; done
      # 같은 명령의 커밋이 실을 작업 폴더 상태. 경로를 준 add 는 그 경로 안만, -A · -u 만 주면 저장소 전체다.
      # 경로를 준 add 는 add_all 을 켜지 않는다 — 켜면 공용 목록 되돌림 검사가 꺼진다
      # -n · -p 같은 add 는 목록을 바꾸지 않고, --ignore-removal 은 삭제를 싣지 않는다
      if [ "$no_new" = 0 ] && [ "$spec_file" = 0 ] && [ "$glost" = 0 ]; then
        g_dir=$gdir g_index=$idx
        if [ "$no_rm" = 1 ] && [ "$flag_update" = 0 ]; then
          set -- "${specs[@]}"
          [ $# -gt 0 ] || [ "$flag_all" = 0 ] || set -- :/
          [ $# -gt 0 ] && add_changed="$add_changed
$(comm -23 <(g ls-files --full-name -m -- "$@" | sort) <(g ls-files --full-name --deleted -- "$@" | sort))"
        elif [ "${#specs[@]}" -gt 0 ]; then
          add_deleted="$add_deleted
$(g ls-files --full-name --deleted -- "${specs[@]}")"
          add_changed="$add_changed
$(g ls-files --full-name -m -d -- "${specs[@]}")"
        elif [ "$flag_all" = 1 ] || [ "$flag_update" = 1 ]; then
          add_deleted="$add_deleted
$(g ls-files --full-name --deleted -- :/)"
          add_changed="$add_changed
$(g ls-files --full-name -m -d -- :/)"
        fi
      fi
      # 새 파일은 -A, 또는 -u 없이 경로를 준 add 만 올리고 그 경로 안의 것뿐이다. 경로 밖 추적 안 된 사본까지 얹으면
      # git 이 싣지 않는 새 파일이 진짜 삭제와 이름 바꾸기로 짝지어져 삭제가 빠진다
      if [ "$no_new" = 0 ] && [ "$spec_file" = 0 ] && [ "$glost" = 0 ] &&
        { [ "$flag_all" = 1 ] || { [ "$flag_update" = 0 ] && [ "${#specs[@]}" -gt 0 ]; }; }; then
        [ "${#specs[@]}" -gt 0 ] || specs=(:/)
        g_dir=$gdir g_index=$idx
        add_untracked="$add_untracked
$(g ls-files --full-name --others --exclude-standard -- "${specs[@]}")"
      fi
      ;;
    read-tree) read_trees="$read_trees$idx|" ;;
    commit)
      [ "$off" = 1 ] || [ "$glost" = 1 ] && return 0
      if [ "$mode" = post ]; then
        parse_commit_args "$@"
        [ "$c_dry" = 1 ] || check_commit_post "$gdir"
      else
        check_commit_pre "$gdir" "$idx" "$@"
      fi
      ;;
  esac
}

handle_segment() {
  local -a w=("$@")
  local i=0 n=$# off=$x_off idx=$x_index in_env=0 a
  while [ "$i" -lt "$n" ]; do
    a=${w[i]}
    if [[ $a =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
      case ${a%%=*} in
        HARNESS_COMMIT_GUARD) [ "${a#*=}" = off ] && off=1 ;;
        GIT_INDEX_FILE) idx=${a#*=} ;;
      esac
    elif [ "$a" = env ] && [ "$in_env" = 0 ]; then
      in_env=1
    elif [ "$in_env" = 1 ] && [[ $a == -* ]]; then
      case $a in -u | -C | -S) i=$((i + 1)) ;; esac
    else
      case $a in
        if | then | else | elif | do | while | until | '!' | '{' | command) ;;
        *) break ;;
      esac
    fi
    i=$((i + 1))
  done
  [ "$i" -lt "$n" ] || return 0
  a=${w[i]}
  i=$((i + 1))
  case $a in
    cd | pushd)
      local p=""
      for a in "${w[@]:i}"; do
        case $a in
          -) lost=1; return 0 ;;
          -*) ;;
          *) p=$a; break ;;
        esac
      done
      [ -n "$p" ] || p=$HOME
      p=$(resolve_dir "$dir" "$p") || { lost=1; return 0; }
      dir=$p
      ;;
    popd) lost=1 ;;
    export)
      for a in "${w[@]:i}"; do
        case $a in
          HARNESS_COMMIT_GUARD=off) x_off=1 ;;
          GIT_INDEX_FILE=*) x_index=${a#*=} ;;
        esac
      done
      ;;
    git) handle_git "$off" "$idx" "${w[@]:i}" ;;
  esac
}

dir=$cwd lost=0 add_all=0 add_untracked="" add_deleted="" add_changed="" x_off=0 x_index="" read_trees="|"
while IFS= read -r seg; do
  IFS=$'\037' read -r -a words <<<"$seg"
  handle_segment "${words[@]}"
done < <(printf '%s\n' "$cmd" | split_commands)
exit 0
