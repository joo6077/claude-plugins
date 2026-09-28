#!/usr/bin/env bash
# m-superseded.sh <레포> — superseded 계약 확인 스크립트를 손으로 답을 아는 세 폴더와 실제 .harness 에 돌린다.
# 줄마다 `<경우> rc=<종료 코드> <요약 줄> states=<상태 낱말 차례로>`.
R=${1:?레포 경로}
C=$R/harness/scripts/check-superseded.sh
T=$(mktemp -d "${TMPDIR:-/tmp}/msup.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
mk() { printf -- '---\n%s\n---\n\n## Skill\n- [ ] SK-01: x\n' "$2" > "$1"; }
# 폴더 A — 넷을 재고 셋이 위반: a→b(active) OK · c 는 가리킴 없음 · d 는 없는 계약 · e→a(superseded) 사슬. f 는 active 라 안 센다
A=$T/a/.harness; mkdir -p "$A"
mk "$A/sprint-contract-a.md" "$(printf 'slug: a\nstatus: superseded   # 새 판 있음\nsuperseded_by: b')"
mk "$A/sprint-contract-b.md" "$(printf 'slug: b\nstatus: active')"
mk "$A/sprint-contract-c.md" "$(printf 'slug: c\nstatus: superseded')"
mk "$A/sprint-contract-d.md" "$(printf 'slug: d\nstatus: superseded\nsuperseded_by: no-such')"
mk "$A/sprint-contract-e.md" "$(printf 'slug: e\nstatus: superseded\nsuperseded_by: a')"
mk "$A/sprint-contract-f.md" "$(printf 'slug: f\nstatus: active')"
# 폴더 B — 하나를 재고 위반 없음
B=$T/b/.harness; mkdir -p "$B"
mk "$B/sprint-contract-x.md" "$(printf 'slug: x\nstatus: superseded\nsuperseded_by: y')"
mk "$B/sprint-contract-y.md" "$(printf 'slug: y\nstatus: done')"
run() {  # run <경우> <폴더>
  out=$(bash "$C" "$2" 2>&1); rc=$?
  printf '%s rc=%s %s states=%s\n' "$1" "$rc" "$(printf '%s\n' "$out" | grep -E '^checked=' | tail -1)" \
    "$(printf '%s\n' "$out" | grep -oE '^(OK|MISSING_BY|MISSING_TARGET|CHAIN) [^ ]*sprint-contract-[a-z]+\.md' | sed -E 's#^([A-Z_]+) .*sprint-contract-([a-z]+)\.md#\2:\1#' | LC_ALL=C sort | tr '\n' ',' | sed 's/,$//')"
}
run A "$A"
run B "$B"
run MISSING "$T/no-such/.harness"
run REPO "$R/.harness"
