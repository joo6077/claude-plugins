#!/bin/bash
# cx3 (4) 계약 고르기가 superseded 계약을 어떻게 다루는지 잰다.
# 사용법: ladder-cases.sh <판 뿌리 폴더>   (예: 작업 폴더, 또는 git worktree 로 풀어 둔 고치기 전 판)
# 두 구현을 같은 입력에 돌린다 — qa-evaluator.md Step 1-b · 1-c 블록(QA) 과 contract-schema.md 의 fm_get ·
# list_contracts · ladder 블록(SCHEMA). 줄마다 "<구현> <경우> <고른 단계> <고른 파일 이름>" 을 찍는다.
V=${1:?판 뿌리 폴더}
QA=$V/harness/agents/qa-evaluator.md
SC=$V/harness/references/contract-schema.md
[ -f "$QA" ] && [ -f "$SC" ] || { echo "missing source" >&2; exit 2; }
F=${CX3_FX:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/cx3-ladder}
rm -rf "$F"; mkdir -p "$F"

block() {  # block <파일> <블록 안에 든 고정 글자> — 그 글자가 든 첫 bash 블록 본문
  awk -v key="$2" '
    /^```bash$/ { inb=1; buf=""; next }
    inb && /^```$/ { if (index(buf, key)) { printf "%s", buf; exit } inb=0; next }
    inb { buf = buf $0 "\n" }' "$1"
}
block "$QA" 'fm_get() {' > "$F/qa-1b.sh"
block "$QA" 'LADDER="3 유일 active"' > "$F/qa-1c.sh"
block "$SC" 'fm_get() { # fm_get <file> <key>' > "$F/sc-fm.sh"
block "$SC" 'list_contracts() { # list_contracts' > "$F/sc-list.sh"
block "$SC" 'echo "ladder3 $pick_act"' > "$F/sc-ladder.sh"
for p in qa-1b qa-1c sc-fm sc-list sc-ladder; do
  [ -s "$F/$p.sh" ] || { echo "block not found: $p" >&2; exit 2; }
done

mk() {  # mk <경우 폴더> <파일 이름> <status 값 또는 -> — status 가 - 면 status 줄 없음(레거시)
  mkdir -p "$1/.harness"
  { echo '---'; echo 'feature: "x"'; [ "$3" = - ] || echo "status: $3"; echo '---'; echo '## Skill'; } > "$1/.harness/$2"
}
# 경우 넷 — superseded 가 레거시로 세이면 결과가 달라지는 모양만 골랐다
C1=$F/c1; mk "$C1" sprint-contract-old.md superseded
C2=$F/c2; mk "$C2" sprint-contract-old.md superseded; mk "$C2" sprint-contract-leg.md -
C3=$F/c3; mk "$C3" sprint-contract-old.md superseded; mk "$C3" sprint-contract-new.md active
C4=$F/c4; mk "$C4" sprint-contract-old.md done;       mk "$C4" sprint-contract-leg.md -

for c in c1 c2 c3 c4; do
  out=$(cd "$F/$c" && CONTRACT_ROOT="$F/$c" HARNESS_CONTRACT= CLAUDE_CODE_SESSION_ID= \
    bash -c ". '$F/qa-1b.sh' >/dev/null; . '$F/qa-1c.sh'" 2>&1)
  lad=$(printf '%s\n' "$out" | sed -n 's/.*| ladder=\(.*\) legacy_contract_used=.*/\1/p' | awk '{print $1}')
  pick=$(printf '%s\n' "$out" | sed -n 's/^CONTRACT=//p'); pick=${pick##*/}
  printf 'QA %s %s %s\n' "$c" "${lad:-?}" "${pick:-?}"
  out=$(CONTRACT_ROOT="$F/$c" CLAUDE_CODE_SESSION_ID= \
    bash -c ". '$F/sc-fm.sh'; . '$F/sc-list.sh'; . '$F/sc-ladder.sh'" 2>&1)
  lad=$(printf '%s\n' "$out" | awk '{print $1}'); pick=$(printf '%s\n' "$out" | awk '{print $2}'); pick=${pick##*/}
  printf 'SCHEMA %s %s %s\n' "$c" "${lad:-?}" "${pick:-?}"
done
