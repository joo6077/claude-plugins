#!/usr/bin/env python3
"""css-tokens.md 의 Howto Kit 행 값과 docs/howto-kit/*.html 첫 :root 블록 값을 맞댄다.
사용: accent.py <레포 루트>  출력: rows=<Howto Kit 행 수> pages=<쪽 수> page_variants=<서로 다른 값 조합 수> match=<0|1>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
tok = (root / ".claude/skills/docs-site/references/css-tokens.md").read_text(encoding="utf-8")
rows = [l for l in tok.splitlines() if re.match(r"^\|\s*\*\*Howto Kit\*\*\s*\|", l)]
combos = set()
pages = sorted(root.glob("docs/howto-kit/*.html"))
for p in pages:
    h = p.read_text(encoding="utf-8")
    blk = re.search(r":root\s*\{([^}]*)\}", h).group(1)
    grad = re.search(r"radial-gradient\(ellipse at 20% 0%,\s*(rgba\([^)]*\))", h)
    vals = tuple(re.search(rf"--{k}:\s*([^;]+);", blk).group(1).strip() for k in ("accent", "accent2", "accent-dim"))
    combos.add(vals + ((grad.group(1).replace(" ", "") if grad else "-"),))
match = 0
if len(rows) == 1 and len(combos) == 1:
    cells = [re.sub(r"[`\s]", "", c) for c in rows[0].strip().strip("|").split("|")][1:5]
    match = int(tuple(cells) == next(iter(combos)))
print(f"rows={len(rows)} pages={len(pages)} page_variants={len(combos)} page_values={sorted(combos)} match={match}")
