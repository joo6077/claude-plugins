#!/usr/bin/env python3
"""check-user-hook-copies.py 가 설치본과 레포 본이 갈린 것을 잡고, 설치본이 없으면 건너뛰는지 보는 시험.

임시 폴더에 도구 사본과 레포 본 자리(harness/evals/hooks/)의 작은 파일 셋을 두고 --installed 를 바꿔 돌린다.
  1. 설치본 폴더가 없음 → 종료 코드 0, 출력이 정확히 「설치본 없음 — 건너뜀」 한 줄
  2. 설치본 폴더는 있으나 세 파일 모두 없음 → 종료 코드 0, 출력이 정확히 「설치본 없음 — 건너뜀」 한 줄
  3. 세 파일이 바이트까지 같음 → 종료 코드 0, 「다름」 줄 없음
  4. 한 파일이 같은 크기로 한 글자 다름 → 종료 코드 1, 「다름: qa-pending-check.sh」 줄 하나
  5. 한 파일만 있고 같음 → 종료 코드 0, 없는 두 파일마다 「설치본 없음 — 건너뜀: <이름>」, 「다름」 줄 없음
  6. 도우미가 마지막 줄바꿈만 다름 → 종료 코드 1, 「다름: _lib-hook-payload.sh」 줄 하나

사용법:
    python3 scripts/test-check-user-hook-copies.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 늘 「설치본 없음 — 건너뜀」 을 찍고 0 으로 끝나는 사본을 주면 경우 4 · 5 · 6 이 실패해야 한다.
종료 코드는 harness/evals/gate-exit-codes.md 의 값을 쓴다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NAMES = ["lint-contract-oracle.sh", "qa-pending-check.sh", "_lib-hook-payload.sh"]
SKIP = "설치본 없음 — 건너뜀"


def repo_text(name: str) -> str:
    return f"#!/usr/bin/env bash\n# {name} 레포 본\necho {name}\n"


def make_tree(root: Path, tool: Path) -> None:
    (root / "scripts").mkdir(parents=True)
    shutil.copy(tool, root / "scripts/check-user-hook-copies.py")
    hooks = root / "harness/evals/hooks"
    hooks.mkdir(parents=True)
    for name in NAMES:
        (hooks / name).write_text(repo_text(name), encoding="utf-8")


def make_installed(installed: Path, shape: str) -> None:
    if shape == "no-folder":
        return
    installed.mkdir()
    if shape == "empty-folder":
        return
    names = ["lint-contract-oracle.sh"] if shape == "one-same" else NAMES
    for name in names:
        text = repo_text(name)
        if shape == "one-byte" and name == "qa-pending-check.sh":
            text = text.replace("레포 본", "레포 판")  # 같은 바이트 수로 한 글자만 다르다
        if shape == "newline" and name == "_lib-hook-payload.sh":
            text = text.rstrip("\n")
        (installed / name).write_text(text, encoding="utf-8")


def run_case(workdir: Path, shape: str, tool: Path) -> tuple[int, list[str]]:
    root = workdir / shape
    make_tree(root, tool)
    installed = workdir / f"{shape}-installed"
    make_installed(installed, shape)
    result = subprocess.run(
        ["python3", "scripts/check-user-hook-copies.py", "--installed", str(installed)],
        cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
    )
    return result.returncode, result.stdout.splitlines()


def differs(lines: list[str]) -> list[str]:
    return [line for line in lines if line.startswith("다름:")]


# (이름표, 모양, 기대 종료 코드, 출력 판정)
CASES = [
    ("1 설치본 폴더가 없으면 건너뛰고 0", "no-folder", 0, lambda lines: lines == [SKIP]),
    ("2 설치본 파일이 하나도 없으면 건너뛰고 0", "empty-folder", 0, lambda lines: lines == [SKIP]),
    ("3 세 파일이 같으면 0", "all-same", 0, lambda lines: not differs(lines)),
    ("4 한 글자 다르면 1", "one-byte", 1,
     lambda lines: [line.split(" ")[1] for line in differs(lines)] == ["qa-pending-check.sh"]),
    ("5 한 파일만 있고 같으면 없는 파일을 적고 0", "one-same", 0,
     lambda lines: not differs(lines) and f"{SKIP}: qa-pending-check.sh" in lines and f"{SKIP}: _lib-hook-payload.sh" in lines),
    ("6 마지막 줄바꿈만 달라도 1", "newline", 1,
     lambda lines: [line.split(" ")[1] for line in differs(lines)] == ["_lib-hook-payload.sh"]),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="check-user-hook-copies.py 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/check-user-hook-copies.py")
    args = parser.parse_args()
    if not args.tool.is_file():
        print(f"ERROR: 도구가 없다 — {args.tool}")
        return 2
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, shape, want_rc, judge in CASES:
            rc, lines = run_case(Path(tmp), shape, args.tool.resolve())
            ok = rc == want_rc and judge(lines)
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} 경우 {label} (rc={rc})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
