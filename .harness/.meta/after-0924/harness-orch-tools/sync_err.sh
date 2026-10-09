#!/usr/bin/env bash
# 복제본에서 sync-orchestrator.py 의 종료 코드 세 가지를 잰다 — 그대로(0) · AUTO 시작 표지 한 줄 삭제(2) · marketplace.json 치움(2)
# 사용: sync_err.sh <레포 또는 워크트리> <ref>
src=${1:?}; ref=${2:?}
t=$(mktemp -d "${TMPDIR:-/tmp}/sync-err.XXXXXX"); trap 'rm -rf "$t"' EXIT
git clone -q "$src" "$t/r" && git -C "$t/r" checkout -q "$ref" || { echo "STOP 복제 실패"; exit 2; }
cd "$t/r" || exit 2
python3 scripts/sync-orchestrator.py --check-only >/dev/null 2>&1; a=$?
F=.claude/skills/kaizen-orchestrator/SKILL.md
grep -v '^<!-- AUTO:plugin_phases:begin -->$' "$F" >"$t/s" && cp "$t/s" "$F"
python3 scripts/sync-orchestrator.py --check-only >/dev/null 2>&1; b=$?
git checkout -q -- "$F"; mv .claude-plugin/marketplace.json "$t/m"
python3 scripts/sync-orchestrator.py --check-only >/dev/null 2>&1; c=$?
echo "intact=$a no_begin_marker=$b no_marketplace=$c"
