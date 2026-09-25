#!/usr/bin/env bash
# commit-guard.sh 를 임시 저장소에서 사고 형태와 정상 형태로 돌려 exit 코드와 출력을 대조한다.
# 번호는 계약 조건 SC-01 ①~⑤ · SC-02 ⑥~⑭ · SC-03 ⑮⑯ · ER-01 · ER-02 (insights-0924-hooks-skill-collector) 와
# ⑰~㉕ (kaizen-0924-p04-harness 경로 지정 커밋) · ㉖~㉚ (kaizen-0924-f1-harness-followups 이름 바꾸기) 를 따른다.
# COMMIT_GUARD_HOOK 으로 훅 경로를 바꿀 수 있다 — 판정 줄을 지운 사본으로 음성 대조를 돌릴 때 쓴다.

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
hook=${COMMIT_GUARD_HOOK:-$here/../../scripts/commit-guard.sh}
command -v jq >/dev/null 2>&1 || { echo "jq 가 없어 시험 입력을 만들 수 없다" >&2; exit 1; }
[ -f "$hook" ] || { echo "훅이 없다: $hook" >&2; exit 1; }
bash_bin=$(command -v bash)

unset HARNESS_COMMIT_GUARD GIT_INDEX_FILE GIT_DIR GIT_WORK_TREE
# 사용자 전역 설정의 서명 · 훅 경로가 끼면 시험 커밋이 깨진다
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
fails=0

mk_repo() {  # d1/ 아래 파일 60 개와 a.txt 를 한 커밋으로 만든다
  local r=$1 k
  mkdir -p "$r/d1"
  git -C "$r" init -q -b main
  for ((k = 1; k <= 60; k++)); do printf 'line %d\n' "$k" >"$r/d1/$(printf 'f%03d' "$k")"; done
  echo a >"$r/a.txt"
  git -C "$r" add -A && git -C "$r" commit -qm init
}

rm_staged() {  # d1 의 앞쪽 파일 N 개를 git rm 으로 목록에서 지운다
  local r=$1 k
  local -a names=()
  for ((k = 1; k <= $2; k++)); do names+=("d1/$(printf 'f%03d' "$k")"); done
  git -C "$r" rm -q -- "${names[@]}"
}

rm_worktree() {  # 작업 폴더에서만 지운다
  local r=$1 k
  for ((k = 1; k <= $2; k++)); do rm -f "$r/d1/$(printf 'f%03d' "$k")"; done
}

payload() {  # payload <pre|post> <명령> <cwd>
  jq -nc --arg e "$1" --arg c "$2" --arg d "$3" \
    '{hook_event_name: (if $e == "pre" then "PreToolUse" else "PostToolUse" end), tool_name: "Bash", tool_input: {command: $c}, cwd: $d}'
}

run() {  # run <pre|post> <명령> <cwd>
  payload "$1" "$2" "$3" | "$bash_bin" "$hook" "$1" >"$work/out" 2>"$work/err"
  rc=$?
}

report() {  # report <번호> <맞음 1/0> <기대> <실제>
  local verdict=PASS
  [ "$2" = 1 ] || { verdict=FAIL; fails=$((fails + 1)); }
  printf '%s %s 기대 %s / 실제 %s\n' "$verdict" "$1" "$3" "$4"
}

expect() {  # expect <번호> <기대 exit> [empty] [stderr 에 있어야 할 글자]
  local ok=1 got="exit $rc"
  [ "$rc" = "$2" ] || ok=0
  if [ "${3:-}" = empty ] && [ -s "$work/out" ]; then ok=0; got="$got · stdout 있음"; fi
  if [ "$2" = 2 ] && [ ! -s "$work/err" ]; then ok=0; got="$got · stderr 비어 있음"; fi
  if [ -n "${4:-}" ] && ! grep -qF -- "$4" "$work/err"; then ok=0; got="$got · stderr 에 '$4' 없음"; fi
  report "$1" "$ok" "exit $2${3:+ · stdout 빈 값}${4:+ · stderr 에 '$4'}" "$got"
}

# ── SC-01 사고 형태: exit 2 ──
r=$work/c1; mk_repo "$r"; rm_staged "$r" 51
run pre 'git commit -m x' "$r"; expect ① 2 '' '삭제 51 개'
cp "$work/err" "$work/err1"

r=$work/c2; mk_repo "$r"; rm_worktree "$r" 60
run pre 'git add -A && git commit -m x' "$r"; expect ② 2 '' '삭제 60 개'

r=$work/c3; mk_repo "$r"
echo v1 >"$r/f2"; git -C "$r" add f2; git -C "$r" commit -qm f2-v1
echo v2 >"$r/f2"; git -C "$r" commit -qam f2-v2
old=$(git -C "$r" rev-parse HEAD~1:f2)
git -C "$r" update-index --cacheinfo "100644,$old,f2"
run pre 'git commit -m x' "$r"; expect ③ 2 '' 'f2'

r=$work/c4; mk_repo "$r"; echo b >>"$r/a.txt"
idx=$work/no-such.idx
run pre "GIT_INDEX_FILE=$idx git add a.txt && GIT_INDEX_FILE=$idx git commit -m x" "$r"; expect ④ 2 '' 'read-tree'
run pre "GIT_INDEX_FILE=$idx git read-tree HEAD && GIT_INDEX_FILE=$idx git add a.txt && GIT_INDEX_FILE=$idx git commit -m x" "$r"
expect ④-read-tree 0 empty

r="$work/with space/repo"; mk_repo "$r"; rm_staged "$r" 51
run pre 'git commit -m x' "$r"; expect ⑤ 2 '' '삭제 51 개'
run pre "cd \"$r\" && git commit -m x" "$work"; expect ⑤-cd 2 '' '삭제 51 개'
run pre "git -C \"$r\" commit -m x" "$work"; expect ⑤-C 2 '' '삭제 51 개'
# 풀 수 없는 이동은 대상을 모르므로 조용히 통과한다
run pre 'cd "$SOMEWHERE" && git commit -m x' "$r"; expect ⑤-cd변수 0 empty

# ── ER-02 막을 때 판단 재료와 우회법 ──
lines=$(grep -c '' "$work/err1")
ok=1
for want in 51 d1/ HARNESS_COMMIT_GUARD=off 승인; do grep -qF -- "$want" "$work/err1" || ok=0; done
[ "$lines" -le 15 ] || ok=0
grep -q 'd1/f0' "$work/err1" && ok=0
report ER-02 "$ok" "51 · d1/ · HARNESS_COMMIT_GUARD=off · 승인 · 15 줄 이하 · 파일 이름 없음" "$lines 줄$(grep -q 'd1/f0' "$work/err1" && echo ' · 파일 이름 있음')"

# ── SC-02 정상 형태: exit 0 · stdout 빈 값 ──
r=$work/c6; mk_repo "$r"; echo more >>"$r/a.txt"; git -C "$r" add a.txt
run pre 'git commit -m x' "$r"; expect ⑥ 0 empty

r=$work/c7; mk_repo "$r"; rm_staged "$r" 50
run pre 'git commit -m x' "$r"; expect ⑦ 0 empty

r=$work/c8; mk_repo "$r"; git -C "$r" mv d1 d2
run pre 'git commit -m x' "$r"; expect ⑧ 0 empty

r=$work/c9; mk_repo "$r"; rm_staged "$r" 60; echo more >>"$r/a.txt"
run pre 'HARNESS_COMMIT_GUARD=off git commit -m x' "$r"; expect ⑨ 0 empty
run pre 'env HARNESS_COMMIT_GUARD=off git commit -m x' "$r"; expect ⑩ 0 empty
run pre 'git status' "$r"; expect ⑪ 0 empty
run pre $'cat <<EOF\ngit commit -m x\nEOF' "$r"; expect ⑫ 0 empty
run pre 'git commit -o a.txt -m x' "$r"; expect ⑬ 0 empty
run pre 'git commit -m x -- a.txt' "$r"; expect ⑭ 0 empty

# ── 경로 지정 커밋: 지정한 경로 안에서 커밋이 실을 삭제만 센다 ──
r=$work/c17; mk_repo "$r"; rm_worktree "$r" 60
run pre 'git commit -o d1 -m x' "$r"; expect ⑰ 2 '' '삭제 60 개'
ok=1; grep -qF 'git status --short --' "$work/err" || ok=0
report ⑰-확인 "$ok" "stderr 에 git status --short --" "$(grep -cF 'git status --short --' "$work/err") 줄"

r=$work/c18; mk_repo "$r"; rm_staged "$r" 51
run pre 'git commit -m x -- d1' "$r"; expect ⑱ 2 '' '삭제 51 개'

r=$work/c19; mk_repo "$r"; rm_worktree "$r" 50
run pre 'git commit -o d1 -m x' "$r"; expect ⑲ 0 empty

# 목록에서만 뺀 파일은 작업 폴더에 남아 있어 경로 커밋이 다시 싣는다 — 삭제 0
r=$work/c20; mk_repo "$r"; git -C "$r" rm -q -r --cached d1
run pre 'git commit -o d1 -m x' "$r"; expect ⑳ 0 empty

# 빈 개인 목록이어도 경로 커밋은 HEAD 위에 얹으므로 지우지 않는다
r=$work/c21; mk_repo "$r"; echo more >>"$r/d1/f001"
run pre "GIT_INDEX_FILE=$work/c21-none.idx git commit -o d1 -m x" "$r"; expect ㉑ 0 empty

# -i 는 목록 전체 삭제에 그 경로의 작업 폴더 삭제를 더한다 (목록 10 + 작업 폴더 45)
r=$work/c22; mk_repo "$r"; rm_staged "$r" 10
for ((k = 11; k <= 55; k++)); do rm -f "$r/d1/$(printf 'f%03d' "$k")"; done
run pre 'git commit -i d1 -m x' "$r"; expect ㉒ 2 '' '삭제 55 개'

r=$work/c23; mk_repo "$r"; rm_worktree "$r" 59
run pre "git commit -o 'd1/f0*' -m x" "$r"; expect ㉓ 2 '' '삭제 59 개'

r=$work/c24; mk_repo "$r"; rm_worktree "$r" 60
run pre 'git commit -o . -m x' "$r/d1"; expect ㉔ 2 '' '삭제 60 개'

# 희소 체크아웃으로 꺼내지 않은 d1 60 개는 작업 폴더에 없어도 git 이 싣지 않는다 — 삭제 0.
# 희소 체크아웃이 안 걸리면 d1 이 작업 폴더에 남아 훅을 고치지 않아도 통과하므로 전제부터 본다
r=$work/c25; mk_repo "$r"; mkdir -p "$r/keep"; echo k >"$r/keep/b.txt"
git -C "$r" add keep && git -C "$r" commit -qm keep && git -C "$r" sparse-checkout set --cone keep
echo more >>"$r/keep/b.txt"
sparse_n=$(git -C "$r" ls-files -t | grep -c '^S ')
if [ -e "$r/d1/f001" ] || [ "$sparse_n" != 60 ]; then
  report ㉕ 0 "희소 체크아웃 전제 — 작업 폴더에 d1 없음 · S 60 개" "d1/f001 $([ -e "$r/d1/f001" ] && echo 있음 || echo 없음) · S $sparse_n 개"
else
  run pre 'git commit -o -m x -- .' "$r"; expect ㉕ 0 empty
fi

# ── 이름 바꾸기: 경로 지정 · -i 커밋도 git 이 이름 바꾸기로 잇는 옛 경로는 삭제로 세지 않는다 ──
r=$work/c26; mk_repo "$r"; git -C "$r" mv d1 d2
run pre 'git commit -o -m x -- d1 d2' "$r"; expect ㉖ 0 empty

r=$work/c27; mk_repo "$r"; mv "$r/d1" "$r/d2"; git -C "$r" add d2
run pre 'git commit -o -m x -- d1 d2' "$r"; expect ㉗ 0 empty

r=$work/c28; mk_repo "$r"; mv "$r/d1" "$r/d2"; git -C "$r" add d2
run pre 'git commit -i -m x -- d1' "$r"; expect ㉘ 0 empty

# 이름 바꾸기 60 개에 진짜 삭제 60 개가 섞이면 막는다
r=$work/c29; mk_repo "$r"; mkdir -p "$r/d3"
for ((k = 1; k <= 60; k++)); do printf 'other %d\n' "$k" >"$r/d3/$(printf 'g%03d' "$k")"; done
git -C "$r" add d3 && git -C "$r" commit -qm d3
git -C "$r" mv d1 d2 && git -C "$r" rm -rq d3
run pre 'git commit -o -m x -- d1 d2 d3' "$r"; expect ㉙ 2 '' '개가 실린 커밋을 막았다'

# 옮긴 새 경로가 지정 경로 밖이면 옛 경로 60 개가 삭제로 실린다
r=$work/c30; mk_repo "$r"; git -C "$r" mv d1 d2
run pre 'git commit -o -m x -- d1' "$r"; expect ㉚ 2 '' '삭제 60 개'

# ── SC-03 커밋 직후 알림 ──
r=$work/c15; mk_repo "$r"; rm_staged "$r" 60; git -C "$r" commit -qm del
run post 'git commit -m x' "$r"
ok=1
[ "$rc" = 0 ] || ok=0
jq -e '.hookSpecificOutput.additionalContext | test("60")' "$work/out" >/dev/null 2>&1 || ok=0
jq -e '.hookSpecificOutput.additionalContext | contains("git reset --soft HEAD~1")' "$work/out" >/dev/null 2>&1 || ok=0
report ⑮ "$ok" "exit 0 · additionalContext 에 60 과 git reset --soft HEAD~1" "exit $rc · $(jq -r '.hookSpecificOutput.additionalContext // "없음"' "$work/out" 2>/dev/null || echo 'JSON 아님')"

r=$work/c16; mk_repo "$r"; rm_staged "$r" 1; git -C "$r" commit -qm del1
run post 'git commit -m x' "$r"; expect ⑯ 0 empty

# ── ER-01 깨진 입력 · jq 없음 ──
nojq=$work/nojq-bin
mkdir -p "$nojq"
for t in bash cat grep sed awk git sort comm head uniq paste date tr; do
  p=$(command -v "$t") && ln -s "$p" "$nojq/$t"
done
# bash 3.2 는 앞서 찾은 jq 경로를 기억하므로 새 프로세스로 확인한다
if PATH=$nojq "$bash_bin" -c 'command -v jq' >/dev/null 2>&1; then
  report "ER-01 준비" 0 "링크 폴더 PATH 에서 jq 없음" "jq 가 보임"
else
  report "ER-01 준비" 1 "링크 폴더 PATH 에서 jq 없음" "jq 없음"
fi
commit_in=$(payload pre 'git commit -m x' "$work")
status_in=$(payload pre 'git status' "$work")

for m in pre post; do
  "$bash_bin" "$hook" "$m" </dev/null >"$work/out" 2>"$work/err"; rc=$?
  expect "ER-01 $m (a) 빈 stdin" 0 empty
  printf '{깨진' | "$bash_bin" "$hook" "$m" >"$work/out" 2>"$work/err"; rc=$?
  expect "ER-01 $m (b) 깨진 JSON" 0 empty
done

printf '%s' "$commit_in" | PATH=$nojq "$bash_bin" "$hook" pre >"$work/out" 2>"$work/err"; rc=$?
ok=1
[ "$rc" = 0 ] || ok=0
jq -e '.hookSpecificOutput.additionalContext | test("jq") and test("검사")' "$work/out" >/dev/null 2>&1 || ok=0
report "ER-01 pre (c) jq 없음 · git commit" "$ok" "exit 0 · additionalContext 에 jq 와 검사" "exit $rc · $(jq -r '.hookSpecificOutput.additionalContext // "없음"' "$work/out" 2>/dev/null || echo 'JSON 아님')"

printf '%s' "$status_in" | PATH=$nojq "$bash_bin" "$hook" pre >"$work/out" 2>"$work/err"; rc=$?
expect "ER-01 pre (d) jq 없음 · git status" 0 empty

printf '%s' "$commit_in" | PATH=$nojq "$bash_bin" "$hook" post >"$work/out" 2>"$work/err"; rc=$?
expect "ER-01 post (c) jq 없음 · git commit" 0 empty

echo "실패 $fails 건"
[ "$fails" = 0 ]
