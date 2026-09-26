#!/usr/bin/env python3
"""Phase 5~17 킷마다 디스크에 있는 폴더(references/ · skills/*/references/ · agents/ · hooks/ · docs/)가
AUTO 범위 줄에 있는지, 범위 줄의 경로가 디스크에 있는지 잰다. 사용: scope_folders.py <레포 루트>"""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
skill = (root / ".claude/skills/kaizen-orchestrator/SKILL.md").read_text(encoding="utf-8")
auto = skill.split("<!-- AUTO:plugin_phases:begin -->", 1)[1].split("<!-- AUTO:plugin_phases:end -->", 1)[0]
have = {}
for sec in re.split(r"(?m)^### Step \d+: ", auto)[1:]:
    m = re.match(r"Phase (\d+) — (\S+) 카이젠", sec)
    rng = sec.split("**범위:**", 1)[1].split("\n\n", 1)[0]
    have[m.group(2)] = re.findall(r"`([^`]+)`", rng)
miss_total = ghost_total = 0
for kit, items in have.items():
    k = root / kit
    folders = []
    for rel in ("references/", "agents/", "hooks/", "docs/"):
        if (k / rel).is_dir():
            folders.append(f"{kit}/{rel}")
    skill_refs = sorted(f"{kit}/{p.relative_to(k)}/" for p in k.glob("skills/*/references") if p.is_dir())
    if skill_refs:
        folders.append(f"{kit}/skills/*/references/")
    hit = lambda d: any(a == d or a.startswith(d) for a in items)
    # 스킬 references 는 별표를 그대로 둔 `<킷>/skills/*/references/` 한 줄로 적거나,
    # 그 킷의 스킬 references 폴더를 하나도 빼지 않고 구체 경로로 적으면 덮인 것으로 본다
    miss = [d for d in folders if not hit(d) and not (d.endswith("/skills/*/references/") and all(hit(s) for s in skill_refs))]
    ghost = [a for a in items if not list(root.glob(a.rstrip("/")))]
    miss_total += len(miss); ghost_total += len(ghost)
    print(f"{kit}: miss={miss} ghost={ghost}")
print(f"folder_miss={miss_total} ghost={ghost_total} kits={len(have)}")
