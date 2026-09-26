#!/usr/bin/env python3
"""phase-research-templates.md 의 Phase 17 절을 잰다 — 제목 수, 표의 출처 행 수, 절 안 URL 가운데
howto 근거(docs/howto/*.md · howto-kit/references/*.md)에 글자 그대로 없는 것, 절 안 역따옴표 경로 가운데 디스크에 없는 것.
사용: phase17.py <레포 루트>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
t = (root / ".claude/skills/kaizen-orchestrator/references/phase-research-templates.md").read_text(encoding="utf-8")
# 제목 뒤 괄호 부연은 허용한다 — Phase 1~12 제목이 `## Phase 2 — Contract (…)` 꼴이다
heads = re.findall(r"(?m)^## Phase 17 — howto-kit(?:\s+\([^\n]*\))?\s*$", t)
sec = ""
if heads:
    sec = t.split(heads[0], 1)[1]
    sec = re.split(r"(?m)^## ", sec, maxsplit=1)[0]
rows = [l for l in sec.splitlines() if re.match(r"^\|\s*\d+\s*\|", l)]
evidence = "".join(p.read_text(encoding="utf-8") for p in sorted(root.glob("docs/howto/*.md")) + sorted(root.glob("howto-kit/references/*.md")))
urls = sorted(set(re.findall(r"https?://[^\s)>\]`|]+", sec)))
invented = [u for u in urls if u not in evidence]
paths = sorted(set(p for p in re.findall(r"`([^`\s]+)`", sec) if "/" in p and not p.startswith("http")))
missing = [p for p in paths if not list(root.glob(p.rstrip("/")))]
print(f"heading={len(heads)} rows={len(rows)} urls={len(urls)} invented={len(invented)} paths={len(paths)} missing_paths={len(missing)}")
for u in invented: print("  invented", u)
for p in missing: print("  missing", p)
