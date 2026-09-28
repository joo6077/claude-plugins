#!/usr/bin/env python3
"""check-cause-table-copies.py 를 원문만 바꾼 임시 사본 다섯에 돌려 종료 코드와 MISMATCH 수를 맞댄다.

경우는 계약 after-0928-harness-checks 의 SC-04 · ER-03 이다. 사본 둘은 그대로 두고 원문만 바꾼다.
  a 그대로 → 0 · b 마지막 경우 뒤에 줄을 더함 → 1 · c 표지 문단 앞에 문단을 더함 → 1
  d 표지 문단 글만 고침 → 0 · e 표지 문단을 지움 → 2 (CANON_MISSING)
기대값은 손으로 적었다. 바꿈이 원문 사본에 실제로 들어갔는지도 함께 잰다 — 안 들어갔으면 그 경우는 잰 것이 아니다.

사용법:
    python3 scripts/test-check-cause-table-copies.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON = "harness/skills/sprint/SKILL.md"
COPIES = [
    "flutter-toolkit/skills/flutter-preflight/SKILL.md",
    "react-kit/skills/react-preflight/SKILL.md",
]
NOTE = "판정 표와 두 경우는"

# (이름, 원문 바꿈, 바꿈이 들어갔는지 확인할 글, 기대 종료 코드, 기대 MISMATCH 수)
CASES = [
    ("a-그대로", None, NOTE, 0, 0),
    ("b-마지막경우뒤줄", (r"(- \*\*미확정\*\*[^\n]*\n)", r"\1- **새 경우** — 원문에만 더한 줄\n"), "- **새 경우**", 1, 2),
    ("c-표지앞문단", (r"\n(판정 표와 두 경우는)", r"\n**새 문단** — 원문에만 더한 문단\n\n\1"), "**새 문단**", 1, 2),
    ("d-표지글고침", (r"판정 표와 두 경우는", r"판정 표와 두 경우는 (표지 문단 고침)"), "표지 문단 고침", 0, 0),
    ("e-표지지움", (r"\n판정 표와 두 경우는[^\n]*\n", r"\n"), None, 2, 0),
]


def make_copy(dest: Path) -> None:
    shutil.copytree(REPO_ROOT / "scripts", dest / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    for rel in [CANON, *COPIES]:
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / rel, dest / rel)


def run_case(work: Path, name: str, edit, marker: str | None, want_rc: int, want_mismatch: int) -> bool:
    dest = work / name
    make_copy(dest)
    canon = dest / CANON
    text = canon.read_text(encoding="utf-8")
    if edit:
        text = re.sub(edit[0], edit[1], text, count=1)
        canon.write_text(text, encoding="utf-8")
    applied = (marker in text) if marker else (NOTE not in text)
    done = subprocess.run([sys.executable, str(dest / "scripts/check-cause-table-copies.py")],
                          capture_output=True, text=True, check=False)
    mismatch = sum(1 for line in done.stdout.splitlines() if line.startswith("MISMATCH "))
    expected = f"rc={want_rc} mismatch={want_mismatch} applied=True"
    actual = f"rc={done.returncode} mismatch={mismatch} applied={applied}"
    ok = expected == actual
    print(f"{'PASS' if ok else 'FAIL'} {name} 기대 {expected} / 실제 {actual}")
    return ok


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="cause-test.") as tmp:
        results = [run_case(Path(tmp), *case) for case in CASES]
    failed = results.count(False)
    print(f"실패 {failed} 건")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
