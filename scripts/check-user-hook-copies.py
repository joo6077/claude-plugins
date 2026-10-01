#!/usr/bin/env python3
"""~/.claude/hooks/ 설치본이 레포 본(harness/evals/hooks/)과 갈렸는지 본다.

레포 본은 시험이 CI 에서 돌도록 설치본을 옮겨 둔 것이다. 한쪽만 고치면 시험은 통과하는데
실제로 도는 훅은 다른 판이 된다 — 그 어긋남을 이 맥에서 알린다.

사용법:
    python3 scripts/check-user-hook-copies.py [--installed <설치본 폴더>]

설치본이 하나도 없으면(CI) `설치본 없음 — 건너뜀` 한 줄을 찍고 0 으로 끝난다.
설치본이 있는 파일만 바이트로 맞대고, 없는 파일은 `설치본 없음 — 건너뜀: <이름>` 으로 적는다.
다른 파일마다 `다름: <이름> (…)` 줄과 차이 몇 줄을 찍고 1 로 끝난다. 모두 같으면 0.
"""

import argparse
import difflib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_HOOKS = REPO_ROOT / "harness/evals/hooks"
# 레포 본으로 옮긴 파일 — 시험이 읽는 훅 둘과 그 둘이 부르는 도우미
COPIED = ["lint-contract-oracle.sh", "qa-pending-check.sh", "_lib-hook-payload.sh"]
SHOWN_DIFF_LINES = 6


def diff_summary(installed: Path, repo: Path) -> list[str]:
    old = installed.read_text(encoding="utf-8", errors="replace").splitlines()
    new = repo.read_text(encoding="utf-8", errors="replace").splitlines()
    changed = [line for line in difflib.unified_diff(old, new, "설치본", "레포 본", lineterm="", n=0)
               if line[:1] in "+-" and not line.startswith(("+++", "---"))]
    head = f"다름: {repo.name} (설치본 {len(old)} 줄 · 레포 본 {len(new)} 줄, 다른 줄 {len(changed)} 개)"
    if not changed:
        head += " — 줄 끝 · 마지막 줄바꿈만 다르다"
    return [head] + [f"  {line}" for line in changed[:SHOWN_DIFF_LINES]]


def main() -> int:
    parser = argparse.ArgumentParser(description="설치본 훅과 레포 본 맞대기")
    parser.add_argument("--installed", type=Path, default=Path.home() / ".claude/hooks")
    args = parser.parse_args()

    present = [name for name in COPIED if (args.installed / name).is_file()]
    if not present:
        print("설치본 없음 — 건너뜀")
        return 0
    differs = 0
    for name in COPIED:
        if name not in present:
            print(f"설치본 없음 — 건너뜀: {name}")
            continue
        installed, repo = args.installed / name, REPO_HOOKS / name
        if installed.read_bytes() != repo.read_bytes():
            differs += 1
            print("\n".join(diff_summary(installed, repo)))
    if differs:
        print(f"설치본과 다른 레포 본 {differs} 개 — 맞춘 쪽을 다른 쪽에 옮겨라")
        return 1
    print(f"설치본 {len(present)} 개가 레포 본과 같다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
