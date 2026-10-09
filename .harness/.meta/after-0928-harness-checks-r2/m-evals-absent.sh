#!/usr/bin/env bash
# m-evals-absent.sh <레포> <판> — <판> 의 run-evals.py · sync-evals.py 가 평가 파일(evals/evals.json) 없는 킷을 이름으로 알리는지 잰다.
# 임시 사본에 마켓 목록 · 킷 폴더 · scripts 를 뜨고, 두 스크립트만 `git show <판>:…` 로 바꿔 돌린다.
# 출력: 스크립트마다 `<run|sync> <판> rc=<종료 코드> absent=[<「없는 킷 N 개 — 대상 아님:」 뒤 이름들, 없으면 빈 값>]`.
R=${1:?레포}; REV=${2:?판}
T=$(mktemp -d "${TMPDIR:-/tmp}/mevab.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
cd "$R" || exit 2
kits=$(python3 -c 'import json; [print(p["name"]) for p in json.load(open(".claude-plugin/marketplace.json",encoding="utf-8"))["plugins"]]')
# shellcheck disable=SC2086
tar -cf - .claude-plugin scripts $kits | tar -xf - -C "$T" || exit 2
for s in run sync; do
  git show "$REV:scripts/$s-evals.py" > "$T/scripts/$s-evals.py" || exit 2
done
out=$(cd "$T" && python3 scripts/run-evals.py 2>&1); rc=$?
echo "run $REV rc=$rc absent=[$(printf '%s\n' "$out" | sed -n -E 's/^.*없는 킷 [0-9]+ 개 — 대상 아님: (.*)$/\1/p' | head -1)]"
out=$(cd "$T" && python3 scripts/sync-evals.py --check-only 2>&1); rc=$?
echo "sync $REV rc=$rc absent=[$(printf '%s\n' "$out" | sed -n -E 's/^.*없는 킷 [0-9]+ 개 — 대상 아님: (.*)$/\1/p' | head -1)]"
