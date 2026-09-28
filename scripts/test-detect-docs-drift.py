#!/usr/bin/env python3
"""detect-docs-drift.py 의 모양/내용 가름 시험.

임시 git 저장소에 도구 사본을 넣고 세 경우를 돌린다.
  1. 표 구분 줄 · 빈 줄 · 울타리 언어 표시 · HTML 주석 · 목록 기호만 바꾼 커밋 → 기본 출력 없음, --include-format-only 1 줄
  2. 낱말 하나를 바꾼 커밋 → 기본 출력 1 줄
  3. 기준 판에 없던 매핑된 원본을 더한 커밋 → 기본 출력 1 줄

사용법:
    python3 scripts/test-detect-docs-drift.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 가름을 망가뜨린 사본을 주면 경우 1 이 실패해야 한다.
종료 코드는 harness/evals/gate-exit-codes.md 의 값을 쓴다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

BASE_SOURCE = """# 개요

<!-- 원본 설명 주석 -->

| 항목 | 값 |
|---|---|
| 규칙 | 하나 |

- 첫째 항목
- 둘째 항목

```
print("hello")
```
"""

FORMAT_ONLY_SOURCE = """# 개요

<!-- 주석 글을 바꿨다 -->


| 항목 | 값 |
| --- | --- |
| 규칙 | 하나 |

* 첫째 항목
* 둘째 항목

```python
print("hello")
```
"""

INDEX_HTML = """<script>
const pages = [
  { id: 'tone-overview', file: 'tone-kit/overview.html' },
];
</script>
"""


class Repo:
    def __init__(self, root: Path, tool: Path):
        self.root = root
        (root / "scripts").mkdir(parents=True)
        shutil.copy(tool, root / "scripts/detect-docs-drift.py")
        self.git("init", "-q")

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-c", "user.name=test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false", *args],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
        )
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} 실패: {result.stderr.strip()}")
        return result.stdout.strip()

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def drift(self, since: str, *extra: str) -> tuple[list[str], str]:
        result = subprocess.run(
            ["python3", "scripts/detect-docs-drift.py", "--since", since, *extra],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
        )
        if result.returncode != 0:
            raise RuntimeError(f"도구 종료 코드 {result.returncode}: {result.stderr.strip()}")
        return [line for line in result.stdout.splitlines() if " → " in line], result.stdout


def fresh_repo(workdir: Path, name: str, tool: Path) -> tuple[Repo, str]:
    repo = Repo(workdir / name, tool)
    repo.write("docs/index.html", INDEX_HTML)
    repo.write("docs/tone-kit/overview.html", "<p>page</p>\n")
    repo.write("docs/tone/overview.md", BASE_SOURCE)
    return repo, repo.commit("base")


def case_format_only(workdir: Path, tool: Path) -> tuple[bool, str]:
    repo, base = fresh_repo(workdir, "format-only", tool)
    repo.write("docs/tone/overview.md", FORMAT_ONLY_SOURCE)
    repo.commit("format only")
    (default, stdout), (full, _) = repo.drift(base), repo.drift(base, "--include-format-only")
    ok = default == [] and "no docs drift" in stdout and len(full) == 1
    return ok, f"default={len(default)} include_format_only={len(full)}"


def case_word_change(workdir: Path, tool: Path) -> tuple[bool, str]:
    repo, base = fresh_repo(workdir, "word-change", tool)
    repo.write("docs/tone/overview.md", BASE_SOURCE.replace("첫째 항목", "첫번째 항목"))
    repo.commit("word change")
    default, _ = repo.drift(base)
    return len(default) == 1, f"default={len(default)}"


def case_new_source(workdir: Path, tool: Path) -> tuple[bool, str]:
    repo, base = fresh_repo(workdir, "new-source", tool)
    repo.write("docs/tone/extra.md", BASE_SOURCE)
    repo.commit("new source")
    default, _ = repo.drift(base)
    return len(default) == 1 and "docs/tone/extra.md" in default[0], f"default={len(default)}"


CASES = [
    ("1 모양만 바뀐 원본은 기본에서 빠진다", case_format_only),
    ("2 낱말이 바뀐 원본은 기본에 남는다", case_word_change),
    ("3 새로 더한 원본은 기본에 남는다", case_new_source),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="detect-docs-drift.py 모양/내용 가름 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/detect-docs-drift.py")
    args = parser.parse_args()
    if not args.tool.is_file():
        print(f"ERROR: 도구가 없다 — {args.tool}")
        return 2
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, case in CASES:
            try:
                ok, detail = case(Path(tmp), args.tool)
            except RuntimeError as error:
                print(f"ERROR 경우 {label}: {error}")
                return 2
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} 경우 {label} ({detail})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
