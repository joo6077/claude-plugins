#!/bin/bash
# 사용: bash m.sh <ID>   (ID: SC-01 SC-02 SC-03 SC-04 SC-05 AR-01 AR-02 AR-03 AP-03 AP-04)
# 환경: R=작업 폴더(기본 ak2-l1) · HREF=재는 판(기본 가지 chore/ak2-l1 끝). 시작 판을 잴 때만 HREF 에 시작 커밋을 준다.
R=${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l1}
S=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint
HERE=$(cd "$(dirname "${0}")" && pwd)
B=90d07163b675cd4222b41c11d3a58b28c968976a
H=$(git -C "$R" rev-parse --verify -q "${HREF:-refs/heads/chore/ak2-l1}^{commit}") || { echo UNRESOLVED; exit 2; }
git -C "$R" rev-parse --verify -q "${B}^{commit}" >/dev/null || { echo UNRESOLVED; exit 2; }
L=.harness/.meta/after-kaizen-0926b/l1-files.txt
NOTES=.harness/.meta/after-kaizen-0926b/l1-notes.md
SLUG=after-0926-mdlint-l1

unpack() {  # unpack <판> <폴더>
  mkdir -p "${2}" && git -C "$R" archive "${1}" | tar -x -C "${2}" || { echo "STOP 풀기 실패 ${1}"; exit 2; }
}
headings() {  # headings <파일> — 코드 블록 밖 제목 줄만
  awk '/^[[:space:]]*(```|~~~)/{f=!f; next} !f && /^#{1,6}[[:space:]]/' "${1}" 2>/dev/null
}

T=$(mktemp -d "${TMPDIR:-/tmp}/l1m.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT

case "${1}" in
SC-01)
  unpack "$H" "$T/h"
  n_list=$(grep -c . "$T/h/$L")
  list_diff=$(git -C "$R" diff --name-only "$B" "$H" -- "$L" | grep -c .)
  warn=$(bash "$S/run.sh" "$T/h" "$T/h/$L" | grep -c .)
  linted=$(cd "$T/h" && "$S/node_modules/.bin/markdownlint-cli2" --config "$S/cfg.jsonc" $(cat "$L") 2>&1 | sed -nE 's/^Linting: ([0-9]+) file.*/\1/p')
  echo "list=$n_list list_diff=$list_diff linted=$linted warn=$warn"
  ;;
SC-02)
  git -C "$R" ls-tree -r --name-only "$H" -- design-kit | grep '\.md$' | sort > "$T/all"
  git -C "$R" show "$H:$L" | sort > "$T/list"
  comm -23 "$T/all" "$T/list" > "$T/excl"
  ex=$(grep -c . "$T/excl")
  touched=0
  while IFS= read -r p; do
    [ -n "$(git -C "$R" diff --name-only "$B" "$H" -- "$p")" ] && touched=$((touched+1))
  done < "$T/excl"
  hmod=$(git -C "$R" diff --name-status "$B" "$H" -- .harness | awk '$(1)!="A"' | grep -c .)
  echo "excluded=$ex excluded_touched=$touched harness_modified=$hmod"
  ;;
SC-03)
  unpack "$B" "$T/b"; unpack "$H" "$T/h"
  python3 "$HERE/norm.py" "$T/b" "$T/h" "$T/h/$L"
  echo "rc=$?"
  added=$(git -C "$R" diff -U0 "$B" "$H" -- $(git -C "$R" show "$H:$L") | grep -E '^\+[^+]' | grep -cE 'markdownlint-(disable|enable|configure-file|capture|restore)' )
  narrow=$(git -C "$R" diff -U0 "$B" "$H" -- $(git -C "$R" show "$H:$L") | grep -E '^\+[^+]' | grep -cE '^\+[[:space:]]*<!-- markdownlint-disable-next-line( MD[0-9]{3})+ -->[[:space:]]*$')
  echo "lint_comments_added=$added narrow_added=$narrow wide_added=$((added-narrow))"
  ;;
SC-04)
  unpack "$H" "$T/h"
  : > "$T/loc"
  while IFS= read -r p; do
    grep -nE '^[[:space:]]*<!-- markdownlint-disable-next-line( MD[0-9]{3})+ -->[[:space:]]*$' "$T/h/$p" | cut -d: -f1 | sed "s#^#$p:#" >> "$T/loc"
  done < "$T/h/$L"
  n=$(grep -c . "$T/loc")
  if [ -f "$T/h/$NOTES" ]; then
    stated=$(sed -nE 's/^좁힌 끄기 주석: ([0-9]+)[[:space:]]*$/\1/p' "$T/h/$NOTES" | head -1)
    listed=0
    while IFS= read -r loc; do
      grep -E "(^|[^0-9A-Za-z_./-])${loc}([^0-9]|$)" "$T/h/$NOTES" | grep -qE 'MD[0-9]{3}.*[^[:space:]]{2,}' && listed=$((listed+1))
    done < "$T/loc"
  else
    stated=NONE; listed=0
  fi
  echo "disables=$n stated=${stated:-NONE} listed=$listed"
  ;;
SC-05)
  cd "$R" || exit 2
  [ "$(git rev-parse HEAD)" = "$H" ] || { echo "STOP HEAD 가 가지 끝이 아님"; exit 2; }
  [ -z "$(git status --porcelain -- . ':(exclude).harness')" ] || { echo "STOP 작업 폴더가 깨끗하지 않음"; exit 2; }
  out=""
  for c in "scripts/validate-plugin.py" "scripts/sync-docs.py --check-only" "scripts/sync-orchestrator.py --check-only" \
           "scripts/sync-evals.py --check-only" "scripts/run-evals.py" "scripts/run-kaizen-assertions.py" \
           "scripts/check-reviewer-protocol-copies.py" "scripts/check-cause-table-copies.py"; do
    python3 $c > /dev/null 2>&1; out="$out $(basename ${c%% *} .py)=$?"
  done
  mkdir -p "$T/ci"
  TMPDIR="$T/ci" bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh "$R" > "$T/ci.out" 2>&1
  circ=$?
  steps=$(grep -c 'rc=' "$T/ci/ci-local/summary.txt")
  bad=$(grep -v 'rc=0' "$T/ci/ci-local/summary.txt" | grep -vc 'feedback-agg-test SKIP (yq 없음)')
  echo "$out | ci_rc=$circ ci_steps=$steps ci_bad=$bad"
  ;;
AR-01)
  git -C "$R" show "$H:$L" | sort > "$T/list"
  git -C "$R" diff --name-only "$B" "$H" -- . ':(exclude).harness' | sort > "$T/chg"
  outside=$(comm -23 "$T/chg" "$T/list" | grep -c .)
  hx=$(git -C "$R" diff --name-only "$B" "$H" -- .harness | grep -vxE "\.harness/sprint-(contract|feedback|amendments)-$SLUG\.md|\.harness/\.meta/$SLUG/.+|\.harness/\.meta/after-kaizen-0926b/l1-notes\.md" | grep -c .)
  echo "changed=$(grep -c . "$T/chg") outside=$outside harness_outside=$hx"
  ;;
AR-02)
  multi=0; n=0
  for c in $(git -C "$R" rev-list --no-merges "$B..$H"); do
    n=$((n+1))
    k=$(git -C "$R" show --name-only --format='' "$c" | grep . | awk -F/ '{print (NF>1)?$(1):"(root)"}' | sort -u | grep -c .)
    [ "$k" -gt 1 ] && multi=$((multi+1))
  done
  merges=$(git -C "$R" rev-list --merges "$B..$H" | grep -c .)
  echo "commits=$n multi_top=$multi merges=$merges"
  ;;
AR-03)
  unpack "$B" "$T/b"; unpack "$H" "$T/h"
  hc=0; noted=0
  while IFS= read -r p; do
    if [ "$(headings "$T/b/$p")" != "$(headings "$T/h/$p")" ]; then
      hc=$((hc+1))
      [ -f "$T/h/$NOTES" ] && grep -F "$p" "$T/h/$NOTES" | grep -q 'grep' && noted=$((noted+1))
    fi
  done < "$T/h/$L"
  echo "heading_changed_files=$hc noted_with_grep=$noted"
  ;;
AP-03)
  unpack "$H" "$T/h"; (cd "$T/h" && python3 scripts/validate-plugin.py design-kit --check=code-fence > "$T/o" 2>&1); echo "rc=$? $(sed -nE 's/.*V6 code-fence +([0-9]+) bare.*/bare=\1/p' "$T/o")"
  ;;
AP-04)
  unpack "$H" "$T/h"; (cd "$T/h" && python3 scripts/validate-plugin.py design-kit --check=frontmatter > /dev/null 2>&1); echo "rc=$?"
  ;;
*) echo "모르는 ID ${1}"; exit 2 ;;
esac
