#!/usr/bin/env bash
# m-fm.sh <레포> — 계약 머리 읽개 셋(qa-evaluator fm_get · 계약 형식 문서 fm_get · sprint-contract read_fm)을
# 손으로 답을 아는 일곱 입력에 bash · zsh 로 돌린다. 줄마다 `<읽개> <셸> <경우> got=[..] want=[..] OK|NG`, 끝 줄 `ng=<수> total=<수>`.
# 종료 코드: 0 = NG 0, 1 = NG 있음, 2 = 읽개를 떼지 못함
R=${1:?레포 경로}
T=$(mktemp -d "${TMPDIR:-/tmp}/mfm.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
awk '/^fm_get\(\) \{/{f=1} f{print} f && /^}/{exit}' "$R/harness/agents/qa-evaluator.md" > "$T/qa.sh"
awk '/^fm_get\(\) \{ # fm_get/{f=1} f{print} f && /^}/{exit}' "$R/harness/references/contract-schema.md" > "$T/schema.sh"
awk '/^read_fm\(\) \{/{f=1} f{print} f && /^}/{exit}' "$R/harness/skills/sprint-contract/SKILL.md" > "$T/skill.sh"
for i in qa schema skill; do [ -s "$T/$i.sh" ] || { echo "STOP $i 읽개를 떼지 못함"; exit 2; }; done
mk() { printf -- '---\n%s\n---\n\n본문\n' "$2" > "$T/c$1.md"; }
mk 1 'status: superseded   # 새 판 있음'
mk 2 'status: "active" # 주석'
mk 3 'status: active'
mk 4 'owner_session: abc#def'
mk 5 'feature: "a # b"'
mk 6 "$(printf "status: 'done'\t# 탭 앞 주석")"
mk 7 'status: active #'
printf '1 status superseded\n2 status active\n3 status active\n4 owner_session abc#def\n5 feature a # b\n6 status done\n7 status active\n' > "$T/want.txt"
ng=0; total=0
for sh in bash zsh; do
  for impl in qa schema skill; do
    while read -r n key want; do
      if [ "$impl" = skill ]; then
        got=$($sh -c '. "$1"; read_fm "$2" "$3"' _ "$T/$impl.sh" "$key" "$T/c$n.md" 2>&1)
      else
        got=$($sh -c '. "$1"; fm_get "$3" "$2"' _ "$T/$impl.sh" "$key" "$T/c$n.md" 2>&1)
      fi
      total=$((total + 1))
      if [ "$got" = "$want" ]; then v=OK; else v=NG; ng=$((ng + 1)); fi
      printf '%s %s %s got=[%s] want=[%s] %s\n' "$impl" "$sh" "$n" "$got" "$want" "$v"
    done < "$T/want.txt"
  done
done
echo "ng=$ng total=$total"
[ "$ng" = 0 ]
