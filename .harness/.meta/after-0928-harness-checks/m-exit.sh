#!/usr/bin/env bash
# m-exit.sh <레포> — 종료 코드 표(harness/evals/gate-exit-codes.md)의 행과 그 표를 인용하는 스크립트를 맞댄다.
# 인용 쪽 = scripts/ · harness/scripts/ · harness/evals/ 아래에서 `gate-exit-codes` 를 적은 파일(표 파일 자신 제외, 추적 + 추적 전 새 파일).
# 출력: `rows=<수> cite=<수> only_rows=[..] only_cite=[..]`
R=${1:?레포}
T=$(mktemp -d "${TMPDIR:-/tmp}/mexit.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
awk '/^\| `[^`]+` \| [0-9]/' "$R/harness/evals/gate-exit-codes.md" | sed -E 's/^\| `([^`]+)`.*/\1/' | LC_ALL=C sort -u > "$T/rows"
(cd "$R" && { git ls-files -- scripts harness/scripts harness/evals; git ls-files --others --exclude-standard -- scripts harness/scripts harness/evals; } \
  | LC_ALL=C sort -u | while IFS= read -r f; do [ -f "$f" ] && grep -qF 'gate-exit-codes' "$f" && printf '%s\n' "$f"; done) \
  | grep -vx 'harness/evals/gate-exit-codes.md' | LC_ALL=C sort -u > "$T/cite"
printf 'rows=%s cite=%s only_rows=[%s] only_cite=[%s]\n' "$(grep -c . "$T/rows")" "$(grep -c . "$T/cite")" \
  "$(comm -23 "$T/rows" "$T/cite" | tr '\n' ',' | sed 's/,$//')" "$(comm -13 "$T/rows" "$T/cite" | tr '\n' ',' | sed 's/,$//')"
