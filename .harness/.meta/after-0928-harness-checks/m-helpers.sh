#!/usr/bin/env bash
# m-helpers.sh <레포> <옛 판> — 공용 측정 시험을 두 번 돌린다: 작업 폴더 그대로, 그리고 계약 형식 문서의 fm_get 만 옛 판 것으로 되돌린 사본.
# 줄마다 `<경우> rc=<종료 코드> pass_F=<^PASS F[1-7]- 줄 수> fail_F=<^FAIL F 줄 수> swapped=<옛 fm_get 이 들어갔는지 1|0>`
R=${1:?레포}; OLD=${2:?옛 판}
T=$(mktemp -d "${TMPDIR:-/tmp}/mhelp.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
run() {  # run <경우> <레포 사본>
  out=$(TMPDIR=$T bash "$2/harness/evals/measure/measure-helpers-test.sh" 2>&1); rc=$?
  printf '%s rc=%s pass_F=%s fail_F=%s swapped=%s\n' "$1" "$rc" "$(printf '%s\n' "$out" | grep -cE '^PASS F[1-7]-')" \
    "$(printf '%s\n' "$out" | grep -cE '^FAIL F')" "$3"
}
run current "$R" 0
mkdir -p "$T/old"
(cd "$R" && tar -cf - harness) | tar -xf - -C "$T/old"
git -C "$R" show "$OLD:harness/references/contract-schema.md" > "$T/old-schema.md" || exit 2
python3 - "$T/old/harness/references/contract-schema.md" "$T/old-schema.md" <<'PY'
import sys
def block(t):
    lines = t.split("\n"); s = next(i for i, l in enumerate(lines) if l.startswith("fm_get() { # fm_get"))
    e = next(i for i in range(s, len(lines)) if lines[i] == "}")
    return lines, s, e
new = open(sys.argv[1], encoding="utf-8").read(); old = open(sys.argv[2], encoding="utf-8").read()
nl, ns, ne = block(new); ol, os_, oe = block(old)
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(nl[:ns] + ol[os_:oe + 1] + nl[ne + 1:]))
PY
if awk '/^fm_get\(\) \{ # fm_get/{f=1} f{print} f && /^}/{exit}' "$T/old/harness/references/contract-schema.md" \
   | cmp -s - <(awk '/^fm_get\(\) \{ # fm_get/{f=1} f{print} f && /^}/{exit}' "$T/old-schema.md"); then sw=1; else sw=0; fi
run old-fm_get "$T/old" "$sw"
