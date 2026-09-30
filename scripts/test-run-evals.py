#!/usr/bin/env python3
"""run-evals.py 가 eval 항목 0 개인 evals.json 을 통과시키지 않는지 보는 시험.

임시 폴더에 킷 하나짜리 마켓 목록과 도구 사본을 두고 돌린다.
  1. {"evals": []} → 종료 코드 2, 출력에 그 경로
  2. 목록 열쇠가 없는 {} → 종료 코드 2, 출력에 그 경로
  3. 항목 하나가 맞는 evals.json → 종료 코드 0

사용법:
    python3 scripts/test-run-evals.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 빈 목록을 경고만 하고 넘기는 옛 사본을 주면 경우 1 · 2 가 실패해야 한다.
도구 옆의 plugin_utils.py 를 같이 복사한다.
종료 코드는 harness/evals/gate-exit-codes.md 의 값을 쓴다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
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
    shutil.copy(tool, root / "scripts/run-evals.py")
    shutil.copy(tool.parent / "plugin_utils.py", root / "scripts/plugin_utils.py")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin/marketplace.json").write_text('{"plugins":[{"name":"k","source":"./k"}]}\n', encoding="utf-8")
    (root / "k/skills/s").mkdir(parents=True)
    (root / "k/skills/s/SKILL.md").write_text("---\nname: s\ndescription: d\nuser-invocable: true\n---\n\n본문\n", encoding="utf-8")
    (root / "k/evals").mkdir()
    (root / "k/evals/evals.json").write_text(evals_text + "\n", encoding="utf-8")


def run_case(workdir: Path, name: str, tool: Path, evals_text: str) -> tuple[int, str]:
    root = workdir / name
    make_tree(root, tool, evals_text)
    result = subprocess.run(
        ["python3", "scripts/run-evals.py"],
        cwd=root, capture_output=True, text=True, encoding="utf-8",
    )
    return result.returncode, result.stdout + result.stderr


CASES = [
    ('1 {"evals": []} 는 종료 코드 2', "empty-list", '{"evals":[]}', 2, "k/evals/evals.json"),
    ("2 목록 열쇠 없는 {} 는 종료 코드 2", "no-key", "{}", 2, "k/evals/evals.json"),
    ("3 항목 하나가 맞으면 종료 코드 0", "good", GOOD_EVALS, 0, ""),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="run-evals.py 빈 목록 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/run-evals.py")
    args = parser.parse_args()
    if not args.tool.is_file() or not (args.tool.parent / "plugin_utils.py").is_file():
        print(f"ERROR: 도구나 옆의 plugin_utils.py 가 없다 — {args.tool}")
        return 2
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, name, evals_text, want_rc, want_text in CASES:
            rc, output = run_case(Path(tmp), name, args.tool, evals_text)
            ok = rc == want_rc and want_text in output
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} 경우 {label} (rc={rc})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
