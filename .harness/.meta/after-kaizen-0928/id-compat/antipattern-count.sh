#!/bin/bash
# 레포 .harness/project.yaml 을 임시 프로젝트에 sed 로 바꿔 넣고 harness/scripts/validate.sh 를 돌린다. 레포 뿌리에서 돌린다.
# 쓰는 법: bash vc.sh '<sed -E 식>'   출력: rc=<종료 코드> apwarn=<금지 패턴 수 경고 줄 수> interr=<integer expected 줄 수>
root=$(pwd); t=$(mktemp -d "${TMPDIR:-/tmp}/vc.XXXXXX"); mkdir -p "$t/.harness"
sed -E "$1" "$root/.harness/project.yaml" > "$t/.harness/project.yaml"
out=$(cd "$t" && bash "$root/harness/scripts/validate.sh" 2>&1); rc=$?
printf 'rc=%s apwarn=%s interr=%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c 'anti_patterns .*개 — 최소')" "$(printf '%s\n' "$out" | grep -c 'integer expected')"
rm -rf "$t"
