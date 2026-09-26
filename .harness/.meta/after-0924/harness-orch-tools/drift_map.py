#!/usr/bin/env python3
"""detect-docs-drift 의 매핑을 레포 전체 추적 원본에 돌려 (1) 짝 원본이 없는 등록 페이지(ORPHAN),
(2) 없는 페이지를 가리키는 원본(NEW)을 낸다. 두 번째 인자로 비교 기준 루트를 주면
기준에 없던 ORPHAN · NEW 가 새로 생겼는지(added_*)도 낸다.
사용: drift_map.py <레포 루트> [<기준 루트>]"""
import importlib.util, subprocess, sys
from pathlib import Path
def measure(root: Path):
    spec = importlib.util.spec_from_file_location(f"ddd{abs(hash(str(root)))}", root / "scripts/detect-docs-drift.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    files = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True).stdout.split()
    reg = m.load_registry(); targets, new = {}, set()
    for src in files:
        if src.startswith((".harness/", ".claude/")):
            continue
        c = m.map_source_to_html(src)
        cands = m.SOURCE_OVERRIDES.get(src) or ([c] if c else [])
        for cand in cands:
            t, r, e = m.resolve_target(cand, reg)
            targets.setdefault(t, []).append(src)
            if not e:
                new.add((src, t))
    pages = sorted(p for p in reg if not p.startswith(("docs/process/", "docs/kaizen/")))
    orphan = {p for p in pages if p not in targets}
    return reg, pages, orphan, new
reg, pages, orphan, new = measure(Path(sys.argv[1]))
print(f"registered={len(reg)} kit_pages={len(pages)} orphan_pages={len(orphan)} new_targets={len(new)}")
if len(sys.argv) > 2:
    _, _, o0, n0 = measure(Path(sys.argv[2]))
    ao, an = sorted(orphan - o0), sorted(new - n0)
    for p in ao: print("  added_orphan", p)
    for p in an: print("  added_new", p)
    print(f"added_orphan={len(ao)} added_new={len(an)} removed_orphan={len(o0 - orphan)} removed_new={len(n0 - new)}")
