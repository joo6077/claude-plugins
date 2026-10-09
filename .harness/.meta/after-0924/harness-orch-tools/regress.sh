#!/usr/bin/env bash
# 이 스프린트가 건드리는 파일을 재는 기존 검사 여덟과 바뀐 셸 · 파이썬 파일 구문 검사를 돌려 종료 코드를 낸다.
# 사용: regress.sh <워크트리> <base> <upper>   마지막 줄: steps=<N> nonzero=<M>
W=${1:?}; B=${2:?}; U=${3:?}
cd "$W" || exit 2
[ "$(git rev-parse HEAD)" = "$(git rev-parse "$U")" ] || { echo "STOP 작업 폴더 HEAD 가 상한과 다르다"; exit 2; }
pc=$(mktemp -d "${TMPDIR:-/tmp}/regress.XXXXXX"); trap 'rm -rf "$pc"' EXIT
n=0; bad=0
step() { n=$((n + 1)); "$@" >"$pc/log" 2>&1; rc=$?; [ "$rc" = 0 ] || { bad=$((bad + 1)); tail -3 "$pc/log" | sed 's/^/    /'; }; printf 'rc=%s %s\n' "$rc" "$*"; }
step python3 scripts/validate-plugin.py
step python3 scripts/sync-evals.py --check-only
step python3 scripts/sync-docs.py --check-only
step python3 scripts/run-evals.py
step python3 scripts/check-stale-values.py
step python3 scripts/test-collect-kaizen-data.py
step bash harness/evals/hooks/commit-guard-test.sh
step python3 scripts/validate-doc-contracts.py
while IFS= read -r f; do
  [ -f "$f" ] || continue
  case $f in
    *.sh) step bash -n "$f" ;;
    *.py) step env PYTHONPYCACHEPREFIX="$pc/pyc" python3 -m py_compile "$f" ;;
  esac
done < <(git diff --name-only "$B" "$U" -- . ':(exclude).harness')
echo "steps=$n nonzero=$bad"
