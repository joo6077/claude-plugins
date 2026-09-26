#!/usr/bin/env bash
# 복제본에서 원본 여덟(짝 여섯 · 초안 · 대조용 howto 리서치 문서)에 한 줄씩 더해 커밋하고
# detect-docs-drift --since HEAD~1 --json 을 돌려 원본 → 페이지 줄을 낸다.
# 사용: drift_e2e.sh <워크트리 또는 레포 경로> [스크립트 경로(생략 시 복제본의 것)]
src=${1:?}; alt=${2:-}
t=$(mktemp -d "${TMPDIR:-/tmp}/drift-e2e.XXXXXX"); trap 'rm -rf "$t"' EXIT
git clone -q "$src" "$t/r" || { echo "clone 실패"; exit 3; }
[ -n "$alt" ] && cp "$alt" "$t/r/scripts/detect-docs-drift.py"
cd "$t/r" || exit 3
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
files=(design-kit/references/visual-change-protocol.md design-kit/skills/design-test/SKILL.md
  reflect-kit/docs/DESIGN.md reflect-kit/docs/SCHEMA.md reflect-kit/docs/RESEARCH.md
  api-kit/skills/api-ui/SKILL.md docs/howto/drafts/SKILL.md docs/howto/deep-links.md)
for f in "${files[@]}"; do [ -f "$f" ] || { echo "원본 없음 $f"; exit 3; }; printf '\n<!-- e2e -->\n' >>"$f"; done
git add -- "${files[@]}" && git commit -qm e2e || exit 3
python3 scripts/detect-docs-drift.py --since HEAD~1 --json >"$t/out.json"; rc=$?
python3 - "$t/out.json" "$rc" <<'PY'
import json, sys
rows = json.load(open(sys.argv[1]))
want = {
    ("design-kit/references/visual-change-protocol.md", "docs/design-kit/visual-change-protocol.html"),
    ("design-kit/skills/design-test/SKILL.md", "docs/design-kit/design-test.html"),
    ("reflect-kit/docs/DESIGN.md", "docs/reflect-kit/design.html"),
    ("reflect-kit/docs/SCHEMA.md", "docs/reflect-kit/schema.html"),
    ("reflect-kit/docs/RESEARCH.md", "docs/reflect-kit/research.html"),
    ("api-kit/skills/api-ui/SKILL.md", "docs/api-kit/static-evidence-viewer-contract.html"),
    ("docs/howto/deep-links.md", "docs/howto-kit/deep-links.html"),
}
got = {(r["source"], r["target"]) for r in rows if r["registered"] and r["exists"]}
for r in rows:
    print(f"{r['source']} -> {r['target']} registered={r['registered']} exists={r['exists']}")
hit = len(want & got); extra = sorted({(r["source"], r["target"]) for r in rows} - want)
for e in extra: print("  unexpected", e)
print(f"expected_hit={hit}/{len(want)} unexpected={len(extra)} entries={len(rows)} rc={sys.argv[2]}")
PY
