#!/usr/bin/env python3
"""detect-docs-drift 의 매핑(접두 · 개별 지정)과 두 스킬 파일의 매핑 표를 (원본, 출력 폴더) 쌍 집합으로 맞대 잰다.
한쪽 쌍의 원본이 다른 쪽의 같은 출력 폴더 접두(끝이 /) 안에 들면 덮인 것으로 본다.
사용: map_tables.py <레포 루트>
출력: 파일마다 표 행 수 · 쌍 수 · 스크립트에만 있는 쌍 · 표에만 있는 쌍, 디스크에 없는 원본, 마지막 줄 요약"""
import importlib.util, re, sys
from pathlib import Path
root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ddd", root / "scripts/detect-docs-drift.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
script = {(p, d) for p, d in m.SOURCE_TO_HTML}
for src, outs in m.SOURCE_OVERRIDES.items():
    for o in outs:
        script.add((src, o.rsplit("/", 1)[0] + "/"))
def covered(pair, pool):
    s, d = pair
    return pair in pool or any(pd == d and ps.endswith("/") and s.startswith(ps) for ps, pd in pool)
def table_pairs(path: Path, section: str | None):
    rows, pairs = 0, set()
    text = path.read_text(encoding="utf-8")
    if section:
        # 그 절만 — 다음 `## ` 제목 앞까지
        text = text.split(section, 1)[1].split("\n## ", 1)[0] if section in text else ""
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            continue
        outs = re.findall(r"`([^`]+)`", cells[2])
        if not outs or not outs[0].startswith("docs/"):
            continue
        rows += 1
        for s in re.findall(r"`([^`]+)`", cells[1]):
            pairs.add((s, outs[0]))
    return rows, pairs
ghost_script = sorted(s for s, _ in script if not (root / s).exists())
summary = [f"script_pairs={len(script)} script_ghost={len(ghost_script)}"]
for g in ghost_script: print("script_ghost", g)
# 오케스트레이터는 파일 전체(표가 어디에도 없어야 한다), docs-site 는 Step 1 절만 본다
for rel, section in ((".claude/skills/kaizen-orchestrator/SKILL.md", None), (".claude/skills/docs-site/SKILL.md", "\n## Step 1:")):
    rows, pairs = table_pairs(root / rel, section)
    only_s = sorted(p for p in script if not covered(p, pairs)) if rows else []
    only_t = sorted(p for p in pairs if not covered(p, script))
    ghost = sorted(s for s, _ in pairs if not (root / s).exists())
    print(f"{rel}: rows={rows} pairs={len(pairs)} script_only={len(only_s)} table_only={len(only_t)} ghost={len(ghost)}")
    for p in only_s: print("   script_only", p)
    for p in only_t: print("   table_only", p)
    for g in ghost: print("   ghost", g)
    summary.append(f"{Path(rel).parent.name}:rows={rows},script_only={len(only_s)},table_only={len(only_t)},ghost={len(ghost)}")
print(" ".join(summary))
