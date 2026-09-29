#!/bin/bash
# 한국어 번호 시험 계약을 봉인하고, 조건 문구 · 측정 줄을 하나씩 바꿔 봉인 판정이 깨지는지 본다. 레포 뿌리에서 돌린다.
# 쓰는 법: bash seal-korean.sh [규약 문서]   셸 둘(bash · zsh)에서 같은 절차를 돈다.
# 출력: 셸마다 `<셸> sealed=<판정 둘> cond_changed=<판정 둘> measure_changed=<판정 둘>`
here=$(cd "$(dirname "$0")" && pwd); root=$(pwd)
schema=${1:-harness/references/contract-schema.md}
tmp=$(mktemp -d "${TMPDIR:-/tmp}/sealko.XXXXXX"); trap 'rm -rf "$tmp"' EXIT
for sh in bash zsh; do
  MEASURE_SCHEMA="$schema" "$sh" -c '
    . "$1/harness/scripts/measure-common.sh" || exit 2
    body=$(sed "1,/^---\$/{/^---\$/!d;}" "$2" | sed "1d")
    seal() { printf -- "---\nstatus: active\nconditions_digest: sha256:%s\nmeasurement_digest: sha256:%s\n---\n%s\n" "$(contract_digest "$1")" "$(measurement_digest "$1")" "$body"; }
    seal "$2" > "$3/c.md"
    verdict() { printf "%s,%s" "$(verify_seal "$1" | cut -d" " -f1)" "$(verify_measurement "$1" | cut -d" " -f1)"; }
    sed "s/^- \[ \] 스킬-01: a\$/- [ ] 스킬-01: b/" "$3/c.md" > "$3/cond.md"
    sed "s/^  측정: x\$/  측정: y/" "$3/c.md" > "$3/meas.md"
    printf "%s sealed=%s cond_changed=%s measure_changed=%s\n" "$0" "$(verdict "$3/c.md")" "$(verdict "$3/cond.md")" "$(verdict "$3/meas.md")"
  ' "$sh" "$root" "$here/fixture-korean.md" "$tmp"
done
