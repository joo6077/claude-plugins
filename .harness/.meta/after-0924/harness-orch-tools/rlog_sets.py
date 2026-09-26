#!/usr/bin/env python3
"""킷별 리서치 기록 파일 목록을 네 자리에서 뽑아 맞댄다.
(a) 오케스트레이터 Gotcha 「per-kit research-log 는 파일이 없어도」 줄의 {…} 목록
(b) Step F4 3 번(research-log 업데이트) 목록의 docs/<x>/research-log.md (docs/kaizen 제외)
(c) Post-Kaizen Checklist 의 「per-kit research-log N개 파일 (…)」 괄호 목록과 N
(d) scripts/validate-post-kaizen.py 의 per_kit_paths
사용: rlog_sets.py <레포 루트>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
s = (root / ".claude/skills/kaizen-orchestrator/SKILL.md").read_text(encoding="utf-8")
g = [l for l in s.splitlines() if "per-kit research-log 는 파일이 없어도" in l]
a = set(re.findall(r"docs/\{([^}]+)\}/research-log\.md", g[0])[0].split(",")) if g else set()
f4 = s.split("3. **research-log 업데이트", 1)[1].split("4. **evals 갱신", 1)[0]
b = {x for x in re.findall(r"`docs/([a-z-]+)/research-log\.md`", f4) if x != "kaizen"}
cl = [l for l in s.splitlines() if "per-kit research-log" in l and "- [ ]" in l]
cm = re.search(r"per-kit research-log (?:(\d+)\s*개\s*)?파일\s*\(([^)]+)\)", cl[0]) if cl else None
c = set(x.strip() for x in cm.group(2).split("/")) if cm else set(); cn = int(cm.group(1)) if cm and cm.group(1) else -1
v = (root / "scripts/validate-post-kaizen.py").read_text(encoding="utf-8")
body = v.split("def check_per_kit_research_logs", 1)[1].split("missing =", 1)[0]
d = set(re.findall(r'"docs/([a-z-]+)/research-log\.md"', body))
want = {"backend", "infra", "rust", "react", "flutter", "planning", "design", "tone", "api"}
exist = {x for x in want if (root / f"docs/{x}/research-log.md").is_file()}
for k, val in (("gotcha", a), ("f4", b), ("checklist", c), ("validator", d)):
    print(f"{k}={sorted(val)} n={len(val)} missing_vs_want={sorted(want - val)} extra={sorted(val - want)}")
print(f"checklist_number={cn} want_files_exist={len(exist)}/{len(want)} all_equal={int(a == b == c == d == want)}")
