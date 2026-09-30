#!/usr/bin/env python3
"""check-install-docs-guidance.py 가 못 읽는 킷 파일을 건너뛰지 않는지 보는 시험.

임시 git 저장소에 킷 하나와 레포 뿌리 docs/ 칸 하나, 도구 사본을 두고 돌린다.
  1. 뿌리 docs/ 를 가리키는 킷 파일을 읽기 권한 없이 두면 → 종료 코드 2, 출력에 그 경로
  2. 같은 파일에 안내 줄이 있고 읽히면 → 종료 코드 0
  3. 추적 중인데 작업 폴더에서 지운 킷 파일은 → 종료 코드 0, 출력에 `SKIP <그 경로>` (커밋 전 삭제는 실패가 아니다)
  4. 추적 중인 바로가기가 가리키는 파일이 없으면 → 종료 코드 2, 출력에 `UNREADABLE <그 경로>` (지운 파일이 아니다)

사용법:
    python3 scripts/test-check-install-docs-guidance.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 읽기 실패를 건너뛰는 옛 사본을 주면 경우 1 이, 바로가기 대상이 없는 것을 지운 파일로 치는
옛 사본을 주면 경우 4 가 실패해야 한다.
root 로 돌면 권한을 빼도 읽혀서 경우 1 을 만들 수 없다 — 그때는 준비 실패 2 로 멈춘다.
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
RAW = "https://raw.githubusercontent.com/joo6077/claude-plugins/main/"
GUIDED = f"참고: docs/foo/x.md\n설치본 플러그인에는 `docs/foo/` 가 없다 — {RAW} 뒤에 붙여 읽는다.\n"


def git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false", *args],
        cwd=root, check=True, capture_output=True,
    )


def make_repo(root: Path, tool: Path, kit_text: str) -> Path:
    (root / "scripts").mkdir(parents=True)
    shutil.copy(tool, root / "scripts/check-install-docs-guidance.py")
    (root / "k/.claude-plugin").mkdir(parents=True)
    (root / "k/.claude-plugin/plugin.json").write_text('{"name":"k"}\n', encoding="utf-8")
    (root / "docs/foo").mkdir(parents=True)
    (root / "docs/foo/x.md").write_text("x\n", encoding="utf-8")
    kit_file = root / "k/a.md"
    kit_file.write_text(kit_text, encoding="utf-8")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    return kit_file


def run_tool(root: Path) -> tuple[int, str]:
    result = subprocess.run(
        ["python3", "scripts/check-install-docs-guidance.py"],
        cwd=root, capture_output=True, text=True, encoding="utf-8",
    )
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    parser = argparse.ArgumentParser(description="check-install-docs-guidance.py 읽기 실패 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/check-install-docs-guidance.py")
    args = parser.parse_args()
    if not args.tool.is_file():
        print(f"ERROR: 도구가 없다 — {args.tool}")
        return 2
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        unreadable_root = Path(tmp) / "unreadable"
        kit_file = make_repo(unreadable_root, args.tool, "참고: docs/foo/x.md\n")
        kit_file.chmod(0)
        try:
            if os.access(kit_file, os.R_OK):
                print("ERROR: 권한을 빼도 파일이 읽힌다 (root 로 도는가) — 경우 1 을 만들 수 없다")
                return 2
            rc, output = run_tool(unreadable_root)
        finally:
            kit_file.chmod(0o644)
        results.append(("1 못 읽는 킷 파일은 종료 코드 2", rc == 2 and "k/a.md" in output, rc))
        make_repo(Path(tmp) / "good", args.tool, GUIDED)
        rc, _ = run_tool(Path(tmp) / "good")
        results.append(("2 읽히고 안내가 붙은 파일은 종료 코드 0", rc == 0, rc))
        deleted_root = Path(tmp) / "deleted"
        make_repo(deleted_root, args.tool, GUIDED)
        # 안내 없는 글이라 읽으면 NEED 로 1 이 된다 — 0 이면 지운 파일을 읽지 않고 넘긴 것이다
        (deleted_root / "k/gone.md").write_text("참고: docs/foo/x.md\n", encoding="utf-8")
        git(deleted_root, "add", "k/gone.md")
        git(deleted_root, "commit", "-qm", "gone")
        (deleted_root / "k/gone.md").unlink()
        rc, output = run_tool(deleted_root)
        results.append(("3 추적 중 지운 파일은 SKIP 하고 종료 코드 0", rc == 0 and "SKIP k/gone.md" in output, rc))
        link_root = Path(tmp) / "broken-link"
        make_repo(link_root, args.tool, GUIDED)
        (link_root / "k/link.md").symlink_to("missing.md")
        git(link_root, "add", "k/link.md")
        git(link_root, "commit", "-qm", "link")
        rc, output = run_tool(link_root)
        results.append(("4 대상 없는 바로가기는 UNREADABLE 하고 종료 코드 2", rc == 2 and "UNREADABLE k/link.md" in output, rc))
    for label, ok, rc in results:
        print(f"{'PASS' if ok else 'FAIL'} 경우 {label} (rc={rc})")
    passed = sum(ok for _, ok, _ in results)
    print(f"경우 {len(results)} 개 중 통과 {passed}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
