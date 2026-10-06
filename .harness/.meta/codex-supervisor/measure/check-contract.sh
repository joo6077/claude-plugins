#!/usr/bin/env bash
# These commands mirror contract-schema headers and sprint-contract Step 6.2.
set -eu
CF=${1:?contract path required}
CONTRACT=$CF
grep -n '^## ' "$CONTRACT"
awk '/^## /{s=$(0)} /^- \[ \]/{print FILENAME":"FNR": "s" -> "$(0)}' "$CONTRACT"
grep -cE '^- \[[ x]\] ([A-Z]{2,}|[^ -~]+)-[0-9]{2}' "$CF"
awk '/^## /{s=$(0)} /^- \[[ x]\] ([A-Z]{2,}|[^ -~]+)-[0-9]{2}/{ if (s=="## Anti-patterns") next; if ($(0) ~ /^- \[[ x]\] (RE-0[12]|DG-0[1-4]|재사용-0[12]|진단-0[1-4]):/) next; if ($(0) ~ /: N\/A \(/) next; n++ } END{print n+0}' "$CF"
FM=$(awk -F'[: ]+' '/^conditions:/{print $(2); exit}' "$CF")
N=$(grep -cE '^- \[[ x]\] ([A-Z]{2,}|[^ -~]+)-[0-9]{2}' "$CF")
[ "$FM" = "$N" ] && echo "OK conditions=$N" || { echo "MISMATCH frontmatter=$FM actual=$N"; exit 1; }
