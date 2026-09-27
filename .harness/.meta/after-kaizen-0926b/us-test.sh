#!/bin/bash
# us 묶음(US-1 ~ US-5) 시험. 사용법: us-test.sh <훅 폴더> <handoff SKILL.md>
# 줄마다 "<경우> <잰 값>" 을 찍는다. 판정은 계약이 한다.
# 고치기 전: us-test.sh <이 폴더>/us-backup <이 폴더>/us-backup/handoff-SKILL.md
# 고친 뒤:   us-test.sh ~/.claude/hooks ~/.claude/skills/handoff/SKILL.md
H=${1:?훅 폴더}
SKILL=${2:?SKILL.md}
HERE=$(cd "$(dirname "${0}")" && pwd)
# 훅이 읽는 공용 도우미도 시험 대상 폴더의 것으로 — 안 그러면 설치본 도우미를 읽는다
export CLAUDE_HOOK_LIB="$H/_lib-hook-payload.sh"
F=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/us-fx
rm -rf "$F"; mkdir -p "$F"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
unset GIT_INDEX_FILE

has() { grep -qF -- "$1" <<<"$2" && echo 1 || echo 0; }
isempty() { [ -z "$1" ] && echo 1 || echo 0; }

# ---- 병렬 세션 훅 (US-2) ----
# 저장소 R: 워크트리 2 개, 공용 인덱스에 shared.txt, 개인 인덱스에 mine.txt
R=$F/repo
git init -q -b main "$R"
( cd "$R" && echo a > a.txt && echo d1 > d1.txt && echo d2 > d2.txt && git add . && git commit -qm init \
  && git worktree add -q "$F/wt2" -b wt2 && echo s > shared.txt && git add shared.txt )
IDX=$F/private.idx
( cd "$R" && GIT_INDEX_FILE=$IDX git read-tree HEAD && echo m > mine.txt && GIT_INDEX_FILE=$IDX git add mine.txt )
R1=$F/solo
git init -q -b main "$R1"
( cd "$R1" && echo a > a.txt && git add . && git commit -qm init && echo s > s.txt && git add s.txt )

pg() {  # pg <이벤트> <명령> [cwd] — 병렬 세션 훅 안내문
  jq -nc --arg c "$2" --arg d "${3:-$R}" --arg e "$1" \
    '{tool_name:"Bash",tool_input:{command:$c},cwd:$d,hook_event_name:$e}' \
    | bash "$H/parallel-session-guard.sh" "$1" \
    | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null
}
show() {  # show <경우> <안내문>
  printf '%s empty=%s shared=%s mine=%s private=%s\n' "$1" "$(isempty "$2")" \
    "$(has shared.txt "$2")" "$(has mine.txt "$2")" "$(has '개인 인덱스' "$2")"
}

# 기존 동작 (앞 계약 user-setup-p6-p10 의 경우 이름 그대로)
show SC02a "$(pg PreToolUse 'git commit -m x')"
show SC02b "$(pg PreToolUse "GIT_INDEX_FILE=$IDX git commit -m x")"
show SC02c "$(pg PreToolUse "env GIT_INDEX_FILE=$IDX git commit -m x")"
show SC02d "$(pg PreToolUse "cat > $F/n.md <<'EOF'
git commit -m y
EOF")"
show SC03a "$(pg PreToolUse "git -C $R commit -m x" "$F")"
show SC03b "$(pg PreToolUse "cd $R && git commit -m x" "$F")"
show SC03c "$(pg PreToolUse 'git commit -o a.txt -m x')"
show SC03d "$(pg PreToolUse 'git commit -m x' "$R1")"
show SC03e "$(pg PreToolUse 'git status')"
show SC03f "$(pg PreToolUse "git commit -F - <<'EOF'
msg
EOF")"
show SC05a "$(pg PreToolUse 'GIT_INDEX_FILE="$T" git commit -m x')"
show SC05b "$(pg PreToolUse "GIT_INDEX_FILE=$F/nope.idx git commit -m x")"
show SC05c "$(pg PreToolUse "export GIT_INDEX_FILE=$IDX; git commit -m x")"
show SC05d "$(pg PreToolUse 'GIT_INDEX_FILE=../private.idx git commit -m x')"
show ER02 "$(CLAUDE_HOOK_LIB=$F/none.sh pg PreToolUse 'git commit -m x')"

# US-2 (가) 따옴표 안 글자는 명령 위치가 아니다
show Q1-pre "$(pg PreToolUse "printf '%s\n' 'a; git commit -m x'")"
show Q2-pre "$(pg PreToolUse 'echo "첫 줄
git commit -m y"')"
show Q3-pre "$(pg PreToolUse 'printf "%s" "a && git commit -m z"')"
show Q4-pre "$(pg PreToolUse 'git commit -m "a; git commit"')"
show Q5-pre "$(pg PreToolUse "echo 'x' && git commit -m y")"
# US-2 (나) GIT_INDEX_FILE 이 git add 에만 붙은 꼴
show I1-pre "$(pg PreToolUse "GIT_INDEX_FILE=$IDX git add mine.txt && git commit -m x")"
show I2-pre "$(pg PreToolUse "GIT_INDEX_FILE=$IDX git add mine.txt && GIT_INDEX_FILE=$IDX git commit -m x")"
show I3-pre "$(pg PreToolUse "export GIT_INDEX_FILE=$IDX; git add mine.txt; git commit -m x")"

# 커밋 뒤 알림
( cd "$R" && git reset -q && git rm -q d1.txt d2.txt && git commit -qm del )
c=$(pg PostToolUse 'git commit -m del')
printf 'SC04a landed=%s del2=%s\n' "$(has '방금 커밋에 실제로 들어간 것' "$c")" "$(has '지운 파일 2 개' "$c")"
( cd "$R" && echo n > n.txt && git add n.txt && git commit -qm add )
c=$(pg PostToolUse 'git commit -m add')
printf 'SC04b landed=%s delword=%s\n' "$(has '방금 커밋에 실제로 들어간 것' "$c")" "$(has '지운 파일' "$c")"
c=$(pg PostToolUse "GIT_INDEX_FILE=$IDX git commit -m add")
printf 'SC04c landed=%s\n' "$(has '방금 커밋에 실제로 들어간 것' "$c")"
c=$(pg PostToolUse "printf '%s\n' 'a; git commit -m x'")
printf 'Q1-post landed=%s\n' "$(has '방금 커밋에 실제로 들어간 것' "$c")"
c=$(pg PostToolUse 'echo "첫 줄
git commit -m y"')
printf 'Q2-post landed=%s\n' "$(has '방금 커밋에 실제로 들어간 것' "$c")"
c=$(pg PostToolUse 'git commit -m "a; git commit"')
printf 'Q4-post landed=%s\n' "$(has '방금 커밋에 실제로 들어간 것' "$c")"

# 조용히 지나가야 하는 입력 (종료 코드 · 출력)
er() {  # er <경우> <훅 파일> <이벤트 인자> <입력> [env 앞말]
  local out rc
  out=$(printf '%s' "$4" | ${5:+env $5} bash "$H/$2" ${3:+"$3"}); rc=$?
  printf '%s rc=%s empty=%s\n' "$1" "$rc" "$(isempty "$out")"
}
PL=$(jq -nc --arg d "$R" '{tool_name:"Bash",tool_input:{command:"git commit -m x"},cwd:$d}')
er ER01-pre-empty parallel-session-guard.sh PreToolUse ''
er ER01-pre-broken parallel-session-guard.sh PreToolUse '{'
er ER01-pre-nojq parallel-session-guard.sh PreToolUse "$PL" PATH=/bin
er ER01-post-empty parallel-session-guard.sh PostToolUse ''
er ER01-post-broken parallel-session-guard.sh PostToolUse '{'
er ER01-post-nojq parallel-session-guard.sh PostToolUse "$PL" PATH=/bin

# ---- 세션 마감 훅 (US-1 · US-5) ----
NOTI=$(jq -r .prompt "$HERE/us-fixtures/task-notification.json")
ho() {  # ho <프롬프트> — 세션 마감 훅 출력 원문
  jq -nc --arg p "$1" '{hook_event_name:"UserPromptSubmit",prompt:$p}' | bash "$H/next-session-handoff.sh"
}
ctx() { printf '%s' "$1" | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null; }
o=$(ho "$NOTI")
printf 'N1 noti_has_kw=%s empty=%s\n' "$(has '다음 세션' "$NOTI")" "$(isempty "$o")"
o=$(ho "$NOTI

다음 세션에 이어가자")
printf 'N2 detect=%s\n' "$(has '세션 마감 감지' "$(ctx "$o")")"
o=$(ho "$NOTI

안녕")
printf 'N3 empty=%s\n' "$(isempty "$o")"
o=$(ho '오늘 여기까지')
c=$(ctx "$o")
pline=$(printf '%s\n' "$c" | grep '^폐기한 결정:')
printf 'H1 json=%s detect=%s pline_count=%s pline_prd=%s pline_scope=%s pline_approval=%s pline_order=%s pline_none=%s pline_reason=%s\n' \
  "$(printf '%s' "$o" | jq -e . >/dev/null 2>&1 && echo 1 || echo 0)" \
  "$(has '세션 마감 감지' "$c")" \
  "$(printf '%s\n' "$c" | grep -c '^폐기한 결정:')" \
  "$(has 'PRD 비범위 표' "$pline")" "$(has '범위 경계' "$pline")" "$(has '승인 기록' "$pline")" \
  "$(printf '%s' "$pline" | grep -c 'PRD 비범위 표.*범위 경계.*승인 기록')" \
  "$(has '없으면 없음' "$pline")" "$(has '이유' "$pline")"
o=$(ho '안녕')
printf 'H2 empty=%s\n' "$(isempty "$o")"
for k in empty broken nojq; do
  case $k in empty) in=''; e='';; broken) in='{'; e='';; nojq) in='{"prompt":"오늘 여기까지"}'; e=PATH=/bin;; esac
  er "ER01-handoff-$k" next-session-handoff.sh '' "$in" $e
done

# ---- codex stdin 훅 (US-3) ----
cx() {  # cx <경우> <명령> [도구 이름]
  local d
  d=$(jq -nc --arg c "$2" --arg t "${3:-Bash}" '{tool_name:$t,tool_input:{command:$c}}' \
    | bash "$H/enforce-codex-stdin.sh" \
    | jq -r '.hookSpecificOutput.permissionDecision // empty' 2>/dev/null)
  printf '%s %s\n' "$1" "${d:-none}"
}
cx C01 'codex exec "hi"'
cx C02 'codex exec "hi" </dev/null'
cx C03 "cat > f.md <<'EOF'
codex exec \"x\"
EOF"
cx C04 'cat <<EOF > g.md
codex exec x
EOF
codex exec y'
cx C05 "cat <<-EOF > h.md
	codex exec x
	EOF"
cx C06 '~/.claude/bin/codex-research p.md o.md'
cx C07 "perl -e 'alarm shift; exec @ARGV' 60 codex exec x"
cx C08 'cat p.md | codex exec -'
cx C09 '# codex exec x'
cx C10 'codex exec x' Write
cx C11 'cat > a.md <<"EOF"
codex exec z
EOF'
cx C12 'cat <<EOF
codex exec x'
CPL='{"tool_name":"Bash","tool_input":{"command":"codex exec x"}}'
er CX-empty enforce-codex-stdin.sh '' ''
er CX-broken enforce-codex-stdin.sh '' '{'
er CX-nojq enforce-codex-stdin.sh '' "$CPL" PATH=/bin
er CX-nolib enforce-codex-stdin.sh '' "$CPL" CLAUDE_HOOK_LIB=$F/none.sh

# ---- 핸드오프 5 단계 커밋 (US-4) ----
S=$F/skill5
git init -q -b main "$S"
( cd "$S" && echo a > a.txt && git add . && git commit -qm init && echo o > other.txt && git add other.txt \
  && mkdir -p .harness/handoff && echo h > .harness/handoff/t.md )
awk '/^### 5\. /{s=1; next} s && /^```bash/{b=1; next} b && /^```/{exit} b{print}' "$SKILL" \
  | sed -e 's/<file>/t/g' -e 's/<세션 요약 한 줄>/시험/g' > "$F/step5.sh"
n0=$(git -C "$S" rev-list --count HEAD)
( cd "$S" && bash "$F/step5.sh" >/dev/null 2>&1 )
printf 'SK5 new_commits=%s subject=%s files=%s other_in_commit=%s other_still_staged=%s coauthor_now=%s coauthor_old=%s\n' \
  "$(( $(git -C "$S" rev-list --count HEAD) - n0 ))" \
  "$(git -C "$S" log -1 --format=%s | grep -c '시험')" \
  "$(git -C "$S" show --name-only --format= HEAD | grep -c .)" \
  "$(git -C "$S" show --name-only --format= HEAD | grep -cx other.txt)" \
  "$(git -C "$S" diff --cached --name-only | grep -cx other.txt)" \
  "$(git -C "$S" log -1 --format=%B | grep -cxF 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>')" \
  "$(git -C "$S" log -1 --format=%B | grep -c 'Opus 4')"
