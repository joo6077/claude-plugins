#!/usr/bin/env bash
# 하네스 저장소 모양(.harness 가 하네스 저장소 폴더로 가는 바로가기)과 프로젝트 안 실제 폴더 모양에서
# 봉인 커밋 · 봉인 대조 · init · 감독 경로 해석이 도는지 임시 저장소로 돌려 본다.
# 사례 이름은 계약 harness-central-store 의 조건이 적은 이름을 따른다.
# 문서 안 코드 블록은 베끼지 않고 파일에서 뽑아 돌린다 — 6.7 은 sprint-contract SKILL.md, 1-e-3 은 qa-evaluator.md.
# 감독 스크립트는 project_root() · layout() · judge_copy() 를 직접 부른다.
# HARNESS_UNDER_TEST 로 잴 harness 폴더를 바꿀 수 있다 — 파일 하나를 옛 판으로 되돌린 사본으로 음성 대조를 돌릴 때 쓴다.

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
under=${HARNESS_UNDER_TEST:-$here/../..}
skill_doc=$under/skills/sprint-contract/SKILL.md
qa_doc=$under/agents/qa-evaluator.md
init_sh=$under/scripts/init.sh
audit_sh=$under/scripts/codex-audit.sh
for f in "$skill_doc" "$qa_doc" "$init_sh" "$audit_sh"; do
  [ -f "$f" ] || { echo "잴 파일이 없다: $f" >&2; exit 2; }
done

unset GIT_INDEX_FILE GIT_DIR GIT_WORK_TREE HARNESS_STORE
# 사용자 전역 설정의 서명 · 훅 경로가 끼면 시험 커밋이 깨진다
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com

# /tmp 는 맥에서 /private/tmp 로 가는 바로가기라 git 이 내는 경로와 글자가 갈린다. 처음부터 실제 경로로 잡는다
work=$(cd "$(mktemp -d)" && pwd -P)
trap 'rm -rf "$work"' EXIT
fails=0

report() {  # report <사례> <0 이면 PASS> [실패 설명]
  if [ "$2" = 0 ]; then echo "PASS $1"; else echo "FAIL $1${3:+ — $3}"; fails=$((fails + 1)); fi
}

# block_after <파일> <제목 앞부분> — 그 제목 아래 첫 ```bash 블록 본문
block_after() {
  awk -v head="$2" '
    index($0, head) == 1 { found = 1; next }
    found && !inside && /^```bash[[:space:]]*$/ { inside = 1; next }
    inside && /^```/ { exit }
    inside { print }
  ' "$1"
}
seal_block=$(block_after "$skill_doc" '### 6.7.')
verify_block=$(block_after "$qa_doc" '#### 1-e-3.')
[ -n "$seal_block" ] || { echo "6.7 블록을 못 뽑았다: $skill_doc" >&2; exit 2; }
[ -n "$verify_block" ] || { echo "1-e-3 블록을 못 뽑았다: $qa_doc" >&2; exit 2; }

new_repo() {  # new_repo <폴더> — 파일 하나짜리 첫 커밋을 가진 main 가지 저장소
  mkdir -p "$1" && git -C "$1" init -q -b main && echo seed >"$1/README" \
    && git -C "$1" add README && git -C "$1" commit -qm init
}

# make_pair <이름> <real|link> — $work/<이름>/proj 와 $work/<이름>/store 를 만들고 계약 경로를 낸다
make_pair() {
  local base=$work/$1
  new_repo "$base/proj" && new_repo "$base/store"
  if [ "$2" = link ]; then
    mkdir -p "$base/store/proj"
    ln -s "$base/store/proj" "$base/proj/.harness"
    echo .harness >"$base/proj/.gitignore"
    git -C "$base/proj" add .gitignore && git -C "$base/proj" commit -qm ignore
  else
    mkdir -p "$base/proj/.harness"
  fi
  printf -- '---\nstatus: active\n---\n\n## 배경\n\n- 본문\n\n## Skill\n\n- [ ] 스킬-01: 조건\n' \
    >"$base/proj/.harness/sprint-contract-t.md"
  echo "$base/proj/.harness/sprint-contract-t.md"
}

run_seal() {  # run_seal <계약> — 프로젝트 최상위에서 6.7 블록을 실제 사용과 같은 입력으로 돌린다
  (cd "$(dirname "$(dirname "$1")")" && CF=$1 SLUG=t N=1 bash -c "$seal_block" 2>&1)
}

run_verify() {  # run_verify <계약>
  (cd "$(dirname "$(dirname "$1")")" && CONTRACT=$1 bash -c "$verify_block" 2>&1)
}

count() { git -C "$1" rev-list --count HEAD; }
branch() { git -C "$1" rev-parse --abbrev-ref HEAD; }

# ── 봉인 커밋 (스킬-01 · 스킬-02 · 오류-02) ──

cf=$(make_pair seal-real real); proj=$(dirname "$(dirname "$cf")")
before=$(count "$proj"); out=$(run_seal "$cf")
names=$(git -C "$proj" show --name-only --format='' HEAD)
[ "$(count "$proj")" = $((before + 1)) ] && [ "$names" = ".harness/sprint-contract-t.md" ] \
  && printf '%s\n' "$out" | grep -qx 'OK seal_commit files=1'
report seal:real $? "$out"
[ "$(branch "$proj")" = feat/t ]
report seal:real-main-branches $? "가지 $(branch "$proj")"

cf=$(make_pair seal-link link); proj=$(dirname "$(dirname "$cf")"); store=$work/seal-link/store
before=$(count "$store"); proj_before=$(count "$proj"); out=$(run_seal "$cf")
names=$(git -C "$store" show --name-only --format='' HEAD)
[ "$(count "$store")" = $((before + 1)) ] && [ "$names" = "proj/sprint-contract-t.md" ] \
  && [ "$(count "$proj")" = "$proj_before" ] && printf '%s\n' "$out" | grep -qx 'OK seal_commit files=1'
report seal:link $? "$out"
[ "$(branch "$store")" = main ] && [ "$(branch "$proj")" = main ]
report seal:link-keeps-branch $? "하네스 저장소 $(branch "$store") · 프로젝트 $(branch "$proj")"

cf=$(make_pair seal-other real); proj=$(dirname "$(dirname "$cf")")
git -C "$proj" checkout -q -b dev
out=$(run_seal "$cf")
[ "$(branch "$proj")" = dev ] && printf '%s\n' "$out" | grep -qx 'OK seal_commit files=1'
report seal:real-other-stays $? "가지 $(branch "$proj") · $out"

# 직전 커밋이 파일 하나짜리라 HEAD 만 세면 거짓 OK 가 나는 상태에서 커밋을 막는다
cf=$(make_pair seal-link-locked link); store=$work/seal-link-locked/store
: >"$store/.git/index.lock"
out=$(run_seal "$cf")
printf '%s\n' "$out" | grep -q '^BLOCKED' && ! printf '%s\n' "$out" | grep -q 'OK seal_commit'
report seal:link-locked $? "$out"

cf=$(make_pair seal-real-locked real); proj=$(dirname "$(dirname "$cf")")
git -C "$proj" checkout -q -b dev   # 가지 옮기기가 락에 먼저 걸려 커밋 단계까지 못 가는 일을 뺀다
: >"$proj/.git/index.lock"
out=$(run_seal "$cf")
printf '%s\n' "$out" | grep -q '^BLOCKED' && ! printf '%s\n' "$out" | grep -q 'OK seal_commit'
report seal:real-locked $? "$out"

# ── 봉인 대조 (스킬-03) ──

for shape in real link; do
  cf=$(make_pair "verify-$shape" "$shape"); run_seal "$cf" >/dev/null
  out=$(run_verify "$cf")
  printf '%s\n' "$out" | grep -qE '^seal_commit=[0-9a-f]+ files=1$' && ! printf '%s\n' "$out" | grep -q SEAL_COMMIT_ABSENT
  report "verify:$shape" $? "$out"
done
cf=$work/verify-link/proj/.harness/sprint-contract-t.md
printf '%s\n' '- 봉인 뒤 더한 산문' >>"$cf"
out=$(run_verify "$cf")
printf '%s\n' "$out" | grep -qxF '+- 봉인 뒤 더한 산문'
report verify:link-prose $? "$out"

# ── init (스킬-04 · 오류-01) ──

run_init() {  # run_init <대상> [HARNESS_STORE 값] — 값을 주지 않으면 변수 자체를 뺀다
  if [ $# -ge 2 ]; then HARNESS_STORE=$2 bash "$init_sh" "$1" generic 2>&1
  else bash "$init_sh" "$1" generic 2>&1; fi
}
linked_to() {  # linked_to <바로가기> <기대 폴더> — 바로가기이고 그 폴더를 가리키는가
  [ -L "$1" ] && [ "$(cd "$1" && pwd -P)" = "$(cd "$2" && pwd -P)" ]
}

new_repo "$work/init-link/proj" && new_repo "$work/init-link/store"
run_init "$work/init-link/proj" "$work/init-link/store" >/dev/null
linked_to "$work/init-link/proj/.harness" "$work/init-link/store/proj" \
  && [ -f "$work/init-link/store/proj/project.yaml" ] \
  && git -C "$work/init-link/proj" check-ignore -q "$work/init-link/proj/.harness"
report init:link $?

new_repo "$work/init-sub/proj" && new_repo "$work/init-sub/store" && mkdir -p "$work/init-sub/proj/app"
run_init "$work/init-sub/proj/app" "$work/init-sub/store" >/dev/null
linked_to "$work/init-sub/proj/app/.harness" "$work/init-sub/store/proj/app" \
  && [ -f "$work/init-sub/store/proj/app/project.yaml" ] \
  && git -C "$work/init-sub/proj" check-ignore -q "$work/init-sub/proj/app/.harness"
report init:link-subdir $?

new_repo "$work/init-plain/proj"
run_init "$work/init-plain/proj" >/dev/null
[ -d "$work/init-plain/proj/.harness" ] && [ ! -L "$work/init-plain/proj/.harness" ] \
  && [ -f "$work/init-plain/proj/.harness/project.yaml" ]
report init:plain $?

new_repo "$work/init-empty/proj"
run_init "$work/init-empty/proj" "" >/dev/null
[ -d "$work/init-empty/proj/.harness" ] && [ ! -L "$work/init-empty/proj/.harness" ]
report init:plain-empty-env $?

new_repo "$work/init-notgit/proj" && mkdir -p "$work/init-notgit/plain"
out=$(run_init "$work/init-notgit/proj" "$work/init-notgit/plain"); code=$?
[ "$code" != 0 ] && [ ! -e "$work/init-notgit/proj/.harness" ] && [ ! -L "$work/init-notgit/proj/.harness" ] \
  && printf '%s\n' "$out" | grep -q 'HARNESS_STORE'
report init:store-not-git $? "종료 $code · $out"

new_repo "$work/init-missing/proj"
out=$(run_init "$work/init-missing/proj" "$work/init-missing/nowhere"); code=$?
[ "$code" != 0 ] && [ ! -e "$work/init-missing/proj/.harness" ] && [ ! -L "$work/init-missing/proj/.harness" ] \
  && printf '%s\n' "$out" | grep -q 'HARNESS_STORE'
report init:store-missing $? "종료 $code · $out"

# ── 감독 경로 해석과 판정 사본 (스크립트-01 · 스크립트-02) ──

# 본문 끝의 main 진입 블록 앞까지만 불러 함수만 쓴다
audit_py=$work/audit.py
awk '/<<.PY.$/ { on = 1; next } /^PY$/ { on = 0 } on' "$audit_sh" \
  | awk '/^try:$/ { stop = NR } { line[NR] = $0 } END { for (i = 1; i < stop; i++) print line[i] }' >"$audit_py"

probe_audit() {  # probe_audit <계약> <판정 사본 폴더 기록 파일> — 해석 결과를 한 줄씩 낸다
  python3 - "$audit_py" "$1" "$2" "$(dirname "$audit_sh")" <<'PROBE'
import sys
source, contract, copy_note, here = sys.argv[1:5]
sys.argv = ['codex-audit', here]
space = {'__name__': 'codex_audit_probe'}
exec(compile(open(source, encoding='utf-8').read(), source, 'exec'), space)
_, meta, _, _ = space['layout'](contract)
root = space['project_root'](meta)
print('meta_name=' + meta.name)
print('root=' + root)
head = space['git'](root, 'rev-parse', 'HEAD').stdout.strip()
copy = space['judge_copy'](root, head, meta)
open(copy_note, 'w').write(str(copy))
PROBE
}

for shape in real link; do
  cf=$(make_pair "audit-$shape" "$shape"); proj=$(cd "$(dirname "$(dirname "$cf")")" && pwd -P)
  mkdir -p "$proj/.harness/.meta/t"
  printf 'echo measure\n' >"$proj/.harness/.meta/t/measure.sh"
  printf 'png' >"$proj/.harness/.meta/t/shot.png"
  # 실제 폴더 모양은 계약 폴더가 커밋돼 있어야 사본에 들어간다
  [ "$shape" = real ] && git -C "$proj" add .harness && git -C "$proj" commit -qm harness
  note=$work/audit-$shape/copy
  out=$(probe_audit "$cf" "$note" 2>&1)
  printf '%s\n' "$out" | grep -qx 'meta_name=.harness' && printf '%s\n' "$out" | grep -qxF "root=$proj"
  report "audit:layout-$shape" $? "$out"
  copy=$(cat "$note" 2>/dev/null)
  if [ "$shape" = link ]; then
    [ -n "$copy" ] && [ -d "$copy/.harness" ] && [ ! -L "$copy/.harness" ] \
      && cmp -s "$copy/.harness/.meta/t/measure.sh" "$proj/.harness/.meta/t/measure.sh" \
      && [ ! -e "$copy/.harness/.meta/t/shot.png" ]
  else
    [ -n "$copy" ] && git -C "$copy" ls-files --error-unmatch .harness/.meta/t/measure.sh >/dev/null 2>&1
  fi
  report "audit:copy-$shape" $? "사본 $copy"
  [ -n "$copy" ] && rm -rf "$copy"
done

echo "실패 $fails 건"
[ "$fails" = 0 ]
