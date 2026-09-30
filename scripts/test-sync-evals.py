#!/usr/bin/env python3
"""sync-evals.py 가 깨지거나 못 읽는 evals.json 을 없는 파일처럼 넘기지 않는지 보는 시험.

임시 폴더에 킷 하나짜리 마켓 목록과 도구 사본을 두고 --check-only 로 돌린다.
  1. 깨진 evals.json → 종료 코드 2, 출력에 그 경로
  2. 스킬과 맞는 정상 evals.json → 종료 코드 0
  3. 읽기 권한 없는 evals.json → 종료 코드 2, 출력에 UNREADABLE 과 그 경로

사용법:
    python3 scripts/test-sync-evals.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 파싱 실패를 SKIP 으로 넘기는 옛 사본을 주면 경우 1 이, 못 읽는 파일에서 멈추는
(추적 출력 · 종료 코드 1) 옛 사본을 주면 경우 3 이 실패해야 한다.
root 로 돌면 권한을 빼도 읽혀서 경우 3 을 만들 수 없다 — 그때는 준비 실패 2 로 멈춘다.
종료 코드는 harness/evals/gate-exit-codes.md 의 값을 쓴다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

GOOD_EVALS = (
    '{"evals":[{"id":1,"skill":"s","prompt":"p","expected_output":"e",'
    '"assertions":[{"text":"a","type":"output"}]}]}'
)


def make_tree(root: Path, tool: Path, evals_text: str) -> None:
    (root / "scripts").mkdir(parents=True)
    shutil.copy(tool, root / "scripts/sync-evals.py")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin/marketplace.json").write_text('{"plugins":[{"name":"k","source":"./k"}]}\n', encoding="utf-8")
    (root / "k/skills/s").mkdir(parents=True)
    (root / "k/skills/s/SKILL.md").write_text("---\nname: s\ndescription: d\nuser-invocable: true\n---\n\n본문\n", encoding="utf-8")
    (root / "k/evals").mkdir()
    (root / "k/evals/evals.json").write_text(evals_text + "\n", encoding="utf-8")


def run_case(workdir: Path, name: str, tool: Path, evals_text: str, unreadable: bool) -> tuple[int, str]:
    root = workdir / name
    make_tree(root, tool, evals_text)
    evals = root / "k/evals/evals.json"
    if unreadable:
        evals.chmod(0)
    try:
        result = subprocess.run(
            ["python3", "scripts/sync-evals.py", "--check-only"],
            cwd=root, capture_output=True, text=True, encoding="utf-8",
        )
    finally:
        evals.chmod(0o644)
    return result.returncode, result.stdout + result.stderr


# (이름표, 폴더, evals.json 내용, 권한 빼기, 기대 종료 코드, 출력에 있어야 할 글)
CASES = [
    ("1 깨진 evals.json 은 종료 코드 2", "broken", "{ broken", False, 2, "k/evals/evals.json"),
    ("2 정상 evals.json 은 종료 코드 0", "good", GOOD_EVALS, False, 0, ""),
    ("3 못 읽는 evals.json 은 종료 코드 2", "unreadable", GOOD_EVALS, True, 2, "UNREADABLE"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="sync-evals.py 깨진 파일 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/sync-evals.py")
    args = parser.parse_args()
    if not args.tool.is_file():
        print(f"ERROR: 도구가 없다 — {args.tool}")
        return 2
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "probe"
        probe.write_text("x", encoding="utf-8")
        probe.chmod(0)
        if os.access(probe, os.R_OK):
            print("ERROR: 권한을 빼도 파일이 읽힌다 (root 로 도는가) — 경우 3 을 만들 수 없다")
            return 2
        for label, name, evals_text, unreadable, want_rc, want_text in CASES:
            rc, output = run_case(Path(tmp), name, args.tool, evals_text, unreadable)
            ok = rc == want_rc and want_text in output and (not unreadable or "k/evals/evals.json" in output)
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} 경우 {label} (rc={rc})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
