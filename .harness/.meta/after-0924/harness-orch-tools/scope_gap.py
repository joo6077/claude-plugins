#!/usr/bin/env python3
"""phase-dependencies.md 의 Phase 5~17 목록 경로가 오케스트레이터 AUTO 범위 줄에 덮이는지 잰다.
사용: scope_gap.py <레포 루트>  — 출력: Phase 별 덮이지 않은 경로, 마지막 줄 uncovered=N phases=M"""
import fnmatch, re, sys
from pathlib import Path
root = Path(sys.argv[1])
deps = (root / ".claude/skills/kaizen-orchestrator/references/phase-dependencies.md").read_text(encoding="utf-8")
block = deps.split("```text", 1)[1].split("```", 1)[0]
want: dict[int, list[str]] = {}
cur = None
for line in block.splitlines():
    m = re.match(r"^Phase (\d+):", line)
    if m:
        cur = int(m.group(1)); want[cur] = []; continue
    s = line.strip()
    if cur is None or not s or s.startswith("↓"):
        continue
    want[cur].append(s.split(" ", 1)[0])
skill = (root / ".claude/skills/kaizen-orchestrator/SKILL.md").read_text(encoding="utf-8")
auto = skill.split("<!-- AUTO:plugin_phases:begin -->", 1)[1].split("<!-- AUTO:plugin_phases:end -->", 1)[0]
have: dict[int, list[str]] = {}
for sec in re.split(r"(?m)^### Step \d+: ", auto)[1:]:
    m = re.match(r"Phase (\d+)", sec)
    n = int(m.group(1))
    rng = sec.split("**범위:**", 1)[1].split("\n\n", 1)[0] if "**범위:**" in sec else ""
    have[n] = re.findall(r"`([^`]+)`", rng)
def covered(p: str, items: list[str]) -> bool:
    for a in items:
        if a == p or (a.endswith("/") and p.startswith(a)) or fnmatch.fnmatchcase(p, a):
            return True
        if a.endswith("/") and fnmatch.fnmatchcase(p, a + "*"):
            return True
    return False
total = 0
for n in sorted(k for k in want if k >= 5):
    miss = [p for p in want[n] if not covered(p, have.get(n, []))]
    total += len(miss)
    print(f"P{n} have={have.get(n)} miss={miss}")
print(f"uncovered={total} phases={len([k for k in want if k >= 5])}")
