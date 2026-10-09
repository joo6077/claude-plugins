#!/usr/bin/env bash
# 한 리포에 Claude 세션이 둘 이상일 때 «조용히 틀리는» 경로를 잡는다.
#
# 다섯 공유물(인덱스·워킹트리·/tmp 고정 경로·산출물 디렉토리·시뮬레이터) 중
# 인덱스만 소리 없이 터진다 — 남이 스테이징해 둔 파일이 내 커밋에 실려도 커밋은
# 성공하고, QA 가 짚기 전까지 아무도 모른다. 나머지 넷은 «왜 안 되지» 로 바로
# 드러나므로 훅이 없어도 알아챈다. 그래서 여기서는 인덱스만 본다.
#
# 차단하지 않는다. 병합 커밋처럼 경로 한정이 불가능한 정당한 커밋이 있고,
# 오탐으로 정상 작업을 막는 것이 훅이 없는 것보다 나쁘다.
#
# fail-open 이 하드 규칙이다 — jq 부재·빈 stdin·깨진 JSON 어디서도 비정상 종료하지
# 않는다. 그래서 `set -e` 를 쓰지 않는다 (errexit 는 fail-open 을 깨뜨린다).
#
# 사용법: parallel-session-guard.sh <PreToolUse|PostToolUse>

event="${1:-}"
command -v jq >/dev/null 2>&1 || exit 0

LIB="${CLAUDE_HOOK_LIB:-$HOME/.claude/hooks/_lib-hook-payload.sh}"
# shellcheck source=/dev/null
. "$LIB" 2>/dev/null

payload=$(cat 2>/dev/null || true)
[ -n "$payload" ] || exit 0

cmd_raw=$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)
[ -n "$cmd_raw" ] || exit 0
# heredoc 본문(커밋 메시지·문서 내용) 속 "git commit" 글자에 반응하지 않는다.
# 도우미를 못 읽어도 커밋 검사는 돌아야 한다 — 그때는 heredoc 본문 제거만 빠진다
if declare -F strip_heredoc_bodies >/dev/null; then
  cmd=$(printf '%s\n' "$cmd_raw" | strip_heredoc_bodies)
else
  cmd=$cmd_raw
fi

# `git commit` 이 아니면 볼 것이 없다. 커밋 메시지 본문에 들어간 "git commit" 을
# 잡지 않도록 명령 시작 위치에서만 찾는다.
#
# `-C <경로>` 는 값을 하나 먹는 플래그라 «플래그는 값이 없다» 를 가정한 아래 패턴을
# 깨뜨린다 — `git -C /x commit` 이 통째로 안 잡혔다(실측). 매칭 전에 그 짝을 지운다. `-c k=v` 도 같다.
# 명령 앞의 변수 대입(`GIT_INDEX_FILE=… git commit`)과 `env` 도 명령 위치를 가린다 —
# 개인 인덱스로 커밋하는 형태가 통째로 안 잡혔다(실측). 되풀이해 벗긴다.
# `(` · `{` · `then` · `do` · `else` · `time` · `command` 뒤도 명령 위치다. 같은 자리에서 벗긴다.
# 따옴표 안 글자는 인자다 — `printf '%s' 'a; git commit'` 이나 큰따옴표 안 줄바꿈 뒤의 "git commit" 을
# 명령 위치로 읽어 헛경고와 헛알림을 냈다(실측). 판별용 사본에서만 따옴표 안을 `_` 로 덮는다.
# 따옴표 밖 `\'` 와 주석(`# don't`) 속 따옴표는 따옴표가 아니다 — 그걸 시작으로 읽어 뒤의 진짜
# 커밋까지 덮어 경고가 사라졌다(실측). 둘 다 따옴표 판정 전에 먼저 덮는다. 주석은 줄 끝까지다.
# `$'…'` 안에서는 `\'` 가 따옴표를 닫지 않는다 — 큰따옴표처럼 역슬래시 다음 글자를 건너뛴다.
# 치환(`$( … )` · 역따옴표)은 안쪽 따옴표를 새로 센다 — `echo "$(echo "it's")"; git commit` 에서 안쪽 `"` 를
# 바깥 따옴표의 닫힘으로 읽으면 `it's` 의 `'` 가 따옴표를 열어 뒤의 진짜 커밋까지 덮었다(실측).
# 치환 깊이마다 따옴표 상태와 괄호 수를 따로 센다. `$((` 는 산술이라 치환으로 보지 않는다.
# 치환 안과 `bash -c '…'` · `sh -c "…"` 인자도 진짜로 도는 명령이다. 바깥 사본에서는 덮고, 원문을
# 꺼내 같은 규칙으로 따로 한 줄씩 덧붙인다. 닫히지 않은 치환 · 인자 · `(` 는 bash 가 문법 오류로
# 아무것도 안 돌리므로 덧붙이지 않고, 짝 없는 `(` 부터 끝까지는 덮는다.
cmd_unquoted=$(printf '%s' "$cmd" | awk '
function blank(count,   filled) { filled = ""; while (count-- > 0) filled = filled "_"; return filled }
function enqueue(piece) {
  sub(/^[[:space:]]+/, "", piece)
  if (piece != "" && queue_n < 2000) queue[++queue_n] = piece
}
function unescape_dq(body,   pos, ch, plain) {
  plain = ""
  for (pos = 1; pos <= length(body); pos++) {
    ch = substr(body, pos, 1)
    if (ch == "\\" && index("$`\"\\\n", substr(body, pos + 1, 1)) > 0) { pos++; ch = substr(body, pos, 1) }
    plain = plain ch
  }
  return plain
}
function at_command(masked, pos,   back, ch, word_end) {
  back = pos - 1
  while (back >= 1 && substr(masked, back, 1) ~ /[ \t]/) back--
  if (back < 1) return 1
  ch = substr(masked, back, 1)
  if (ch == "\n" || ch ~ /[;&|(]/) return 1
  word_end = back
  while (back >= 1 && substr(masked, back, 1) ~ /[A-Za-z{!]/) back--
  if (substr(masked, back + 1, word_end - back) ~ /^(then|do|else|time|command|[{]|!)$/) return at_command(masked, back + 1)
  return 0
}
function open_subst(kind, body_at) {
  depth++; quote_at[depth] = ""; paren_at[depth] = 0; kind_at[depth] = kind
  if (depth == 1) { subst_from = pos; subst_body = body_at }
}
function close_subst(text) {
  if (depth == 1) { subst_n++; subst_text[subst_n] = substr(text, subst_body, pos - subst_body); subst_at[subst_n] = subst_from }
  depth--
}
function mask(text,   len, ch, quote, out, piece, comment, open_n, cut, found) {
  split("", quote_at); split("", paren_at); split("", kind_at); split("", open_at); subst_n = 0
  len = length(text); depth = 0; quote_at[0] = ""; kind_at[0] = ""; out = ""; piece = ""; comment = 0; open_n = 0
  for (pos = 1; pos <= len; pos++) {
    # 한 글자씩 out 에 이으면 긴 명령에서 매번 전체를 다시 복사한다. 짧은 조각에 모았다가 붙인다
    if (length(piece) > 256) { out = out piece; piece = "" }
    ch = substr(text, pos, 1)
    if (comment) { if (ch == "\n") { comment = 0; piece = piece ch } else piece = piece "_"; continue }
    quote = quote_at[depth]
    if (quote == "") {
      if (ch == "\\" && pos < len) { piece = piece "__"; pos++; continue }
      if (ch == "#" && (pos == 1 || substr(text, pos - 1, 1) ~ /[[:space:];&|(]/)) { comment = 1; piece = piece "_"; continue }
      if (ch == "$" && substr(text, pos + 1, 1) == "(" && substr(text, pos + 2, 1) != "(") { open_subst("(", pos + 2); piece = piece "__"; pos++; continue }
      if (ch == "`") { if (kind_at[depth] == "`") close_subst(text); else open_subst("`", pos + 1); piece = piece "_"; continue }
      if (depth == 0 && ch == "(") open_at[++open_n] = pos
      if (depth == 0 && ch == ")" && open_n > 0) open_n--
      if (kind_at[depth] == "(" && ch == "(") paren_at[depth]++
      if (kind_at[depth] == "(" && ch == ")") { if (paren_at[depth] == 0) { close_subst(text); piece = piece "_"; continue } paren_at[depth]-- }
      if (ch == "\047" || ch == "\"") quote_at[depth] = ch
      if (ch == "\047" && pos > 1 && substr(text, pos - 1, 1) == "$") quote_at[depth] = "$\047"
      piece = piece (depth > 0 ? "_" : ch); continue
    }
    if (quote != "\047" && ch == "\\" && pos < len) { piece = piece "__"; pos++; continue }
    if (ch == quote || (quote == "$\047" && ch == "\047")) { quote_at[depth] = ""; piece = piece (depth > 0 ? "_" : ch); continue }
    if (quote == "\"" && ch == "$" && substr(text, pos + 1, 1) == "(" && substr(text, pos + 2, 1) != "(") { open_subst("(", pos + 2); piece = piece "__"; pos++; continue }
    if (quote == "\"" && ch == "`") { if (kind_at[depth] == "`") close_subst(text); else open_subst("`", pos + 1); piece = piece "_"; continue }
    piece = piece "_"
  }
  out = out piece
  cut = (open_n > 0 ? open_at[1] : len + 1)
  if (cut <= len) out = substr(out, 1, cut - 1) blank(len - cut + 1)
  for (found = 1; found <= subst_n; found++) if (subst_at[found] < cut) enqueue(subst_text[found])
  return out
}
function enqueue_shell_c(text, masked,   offset, word_at, quote_pos, quote, close_len, body) {
  offset = 0
  while (match(substr(masked, offset + 1), /(bash|sh)[ \t]+-[A-Za-z]*c[ \t]+[\047"]/)) {
    word_at = offset + RSTART; quote_pos = offset + RSTART + RLENGTH - 1; offset = quote_pos
    if (word_at > 1 && substr(masked, word_at - 1, 1) ~ /[A-Za-z0-9_.\/-]/) continue
    if (!at_command(masked, word_at)) continue
    quote = substr(masked, quote_pos, 1)
    close_len = index(substr(masked, quote_pos + 1), quote)
    if (close_len == 0) continue
    body = substr(text, quote_pos + 1, close_len - 1)
    enqueue(quote == "\"" ? unescape_dq(body) : body)
  }
}
BEGIN { RS = "\001"; ORS = "" }
{
  queue_n = 0; queue[++queue_n] = $0
  for (done = 1; done <= queue_n; done++) {
    masked = mask(queue[done])
    print (done > 1 ? "\n" : "") masked
    enqueue_shell_c(queue[done], masked)
  }
}')
cmd_probe=$(printf '%s' "$cmd_unquoted" | sed -E \
  -e 's/-C[[:space:]][^[:space:]]*//g' \
  -e ':config' \
  -e 's/(git([[:space:]]+-[^[:space:]]+)*)[[:space:]]+-c[[:space:]]+[^[:space:]]+/\1/' \
  -e 't config' \
  -e ':strip' \
  -e "s/(^|[;&|][[:space:]]*)([(]|(env([[:space:]]+-[^[:space:]]+)*|[A-Za-z_][A-Za-z0-9_]*=(\"[^\"]*\"|'[^']*'|[^[:space:]]*)|then|do|else|time|command|[{])[[:space:]])[[:space:]]*/\1/" \
  -e 't strip')
printf '%s' "$cmd_probe" \
  | grep -qE '(^|[;&|][[:space:]]*)git([[:space:]]+-[^[:space:]]+)*[[:space:]]+commit([[:space:]]|$)' \
  || exit 0

cwd=$(printf '%s' "$payload" | jq -r '.cwd // empty' 2>/dev/null || true)
[ -n "$cwd" ] || cwd="$PWD"

# 명령이 스스로 디렉터리를 옮기면 그쪽이 진짜 대상이다. 페이로드의 cwd 는 세션 것이라
# `cd <다른리포> && git commit` 을 세션 리포의 커밋으로 잘못 읽는다 — 실측으로 다른
# 저장소의 HEAD 를 보여줬다. 잘못된 대상을 짚는 경고는 침묵보다 나쁘다.
# `git -C <경로>` 도 같은 이유로 본다. 마지막에 나온 것이 이긴다. 서브셸 `(cd …` 도 본다.
# 값을 못 풀면(`$` · 역따옴표) 세션 폴더로 떨어지지 않고 지나간다 — `git -C "$W"` 뒤 알림이
# 세션 폴더의 HEAD 를 보였다(실측).
# BSD sed 는 BRE 에서 `\|` 를 안 받는다 (실측: 치환이 통째로 실패해 옛 리포를 계속
# 가리켰다). grep -oE 로 뽑는다.
cd_words=$(printf '%s' "$cmd" | grep -oE '(^|[;&|(][[:space:]]*)cd[[:space:]]+[^;&|[:space:]]+')
dir_flag_words=$(printf '%s' "$cmd" | grep -oE 'git[[:space:]]+-C[[:space:]]+[^;&|[:space:]]+')
case $cd_words$dir_flag_words in *'$'*|*'`'*) exit 0 ;; esac
for part in $(printf '%s' "$cd_words" | grep -oE '/[^;&|[:space:]]+'); do
  [ -d "$part" ] && cwd="$part"
done
for part in $(printf '%s' "$dir_flag_words" | grep -oE '/[^;&|[:space:]]+'); do
  [ -d "$part" ] && cwd="$part"
done

[ -d "$cwd" ] || exit 0

git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1 || exit 0

emit() {  # emit <context>
  jq -nc --arg e "$event" --arg c "$1" \
    '{hookSpecificOutput:{hookEventName:$e,additionalContext:$c}}' 2>/dev/null
  exit 0
}

if [ "$event" = "PostToolUse" ]; then
  # 커밋 뒤에 «무엇이 들어갔는지» 를 눈에 보이게 한다. 메모리
  # feedback_parallel_sessions_share_everything 이 습관으로 굳히라고 한 확인이다.
  landed=$(git -C "$cwd" show --name-only --format='%h %s' HEAD 2>/dev/null | head -40)
  [ -n "$landed" ] || exit 0
  # 옮긴 파일은 R 로 잡혀 여기서 안 센다 — 사라진 파일만 센다
  deleted=$(git -C "$cwd" show --name-status --format= HEAD 2>/dev/null | grep -c '^D')
  deleted_line=""
  [ "${deleted:-0}" -gt 0 ] && deleted_line="

지운 파일 ${deleted} 개 — 이번에 지우려던 파일이 맞는지 본다."
  emit "방금 커밋에 실제로 들어간 것:

$landed${deleted_line}

내가 이번에 건드리지 않은 파일이 섞였으면 다른 세션의 스테이징을 삼킨 것이다. 그 경우
\`git reset --soft HEAD~1\` 로 되돌리고 \`git commit -o <경로>\` 로 다시 커밋하라."
fi

# ---- 아래는 PreToolUse ----

# 워크트리가 하나뿐이면 이 리포에 병렬 세션 흔적이 없다. 조용히 지나간다.
worktrees=$(git -C "$cwd" worktree list 2>/dev/null | wc -l | tr -d ' ')
[ "${worktrees:-1}" -gt 1 ] || exit 0

# 경로를 한정한 커밋(`-o` / `--only`)은 인덱스 전체를 싣지 않으므로 안전하다.
printf '%s' "$cmd" | grep -qE '(^|[[:space:]])(-o|--only)([[:space:]]|=|$)' && exit 0

# 개인 인덱스(`GIT_INDEX_FILE=`)로 커밋하면 공용 인덱스는 상관없다 — 그 파일에 올라온 것을 보여준다.
# 값을 못 풀면(`$` · 역따옴표) 공용 인덱스로 떨어지지 않고 지나간다. 공용 목록을 보여주면 틀린 경고다.
# 명령 앞 대입은 그 명령 하나에만 붙는다. `GIT_INDEX_FILE=x git add … && git commit` 은 공용 인덱스로
# 커밋하는데 개인 인덱스 목록을 보였다(실측). 커밋 명령 앞에 붙은 것, 없으면 앞서 export 한 것만 본다.
index_file=""
index_assign="GIT_INDEX_FILE=(\"[^\"]*\"|'[^']*'|[^[:space:];&|]*)"
index_word=$(printf '%s' "$cmd" | sed -E 's/-C[[:space:]][^[:space:]]*//g' \
  | grep -oE "(^|[;&|])[[:space:]]*((env([[:space:]]+-[^[:space:]]+)*|[A-Za-z_][A-Za-z0-9_]*=(\"[^\"]*\"|'[^']*'|[^[:space:]]*))[[:space:]]+)*git([[:space:]]+-[^[:space:]]+)*[[:space:]]+commit([[:space:]]|$)" \
  | grep -oE "$index_assign" | tail -1)
[ -n "$index_word" ] || index_word=$(printf '%s' "$cmd" \
  | grep -oE "(^|[;&|])[[:space:]]*export[[:space:]]+$index_assign" | grep -oE "$index_assign" | tail -1)
if [ -n "$index_word" ]; then
  index_file=${index_word#GIT_INDEX_FILE=}
  index_file=${index_file#[\"\']}; index_file=${index_file%[\"\']}
  case $index_file in *'$'*|*'`'*|'') exit 0 ;; esac
  case $index_file in /*) ;; *) index_file="$cwd/$index_file" ;; esac
  [ -f "$index_file" ] || exit 0
fi

if [ -n "$index_file" ]; then
  staged=$(GIT_INDEX_FILE="$index_file" git -C "$cwd" diff --cached --name-only 2>/dev/null | head -40)
else
  staged=$(git -C "$cwd" diff --cached --name-only 2>/dev/null | head -40)
fi
[ -n "$staged" ] || exit 0

if [ -n "$index_file" ]; then
  emit "개인 인덱스 \`$index_file\` 로 커밋한다. 이 커밋에 실릴 것:

$staged

이번에 만든 것만 있으면 그대로 진행하라. 커밋 뒤 알림으로 실제로 들어간 것을 다시 본다."
fi

emit "이 리포에 워크트리가 ${worktrees} 개다 — 다른 세션이 같은 인덱스에 스테이징했을 수 있다.
\`git add <경로>\` 는 격리가 아니다. \`add\` 는 지정 경로만 넣지만 \`commit\` 은 인덱스 전체를 싣는다.

지금 인덱스에 올라온 것:

$staged

전부 내가 이번에 만든 것이 맞으면 그대로 진행하라. 아니면 \`git commit -o <경로>\` 로
경로를 한정하라. 병합 커밋처럼 한정이 불가능한 경우는 그대로 두면 된다."
