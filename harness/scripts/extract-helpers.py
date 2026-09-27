#!/usr/bin/env python3
"""계약 안 측정 도우미 코드 블록을 떼어 파일로 저장한다.

도우미 블록은 bash · python 코드 블록 가운데 첫 주석 줄(셔뱅 다음)이 `# <이름>.sh` · `# <이름>.py` 로
시작하는 것이다. 떼어 낸 파일은 블록 본문과 바이트까지 같다.

Usage:
    python3 harness/scripts/extract-helpers.py [--sealed] <계약 파일> <출력 폴더>

--sealed 를 주면 작업 폴더 판이 아니라 그 계약을 처음 담은 커밋의 판을 읽는다 — 봉인 뒤에 계약을
고쳐도 봉인 때 도우미로 잰다.

exit 0 = 떼어 저장했다, 1 = 같은 이름 블록이 둘 이상이라 아무것도 쓰지 않았다,
2 = 계약을 읽지 못했다(파일 없음 · --sealed 인데 git 이 추적하지 않음),
3 = 뗄 블록이 없다. 값의 정의는 `harness/evals/gate-exit-codes.md`.
"""
import argparse
import pathlib
import re
import subprocess
import sys

BLOCK = re.compile(r"^```(?:bash|python)\n(.*?)^```$", re.S | re.M)
NAME = re.compile(r"# ([\w.-]+\.(?:sh|py))(?: |$)")


def sealed_text(path: pathlib.Path) -> str:
    """계약을 처음 담은 커밋의 판을 돌려준다. 추적하지 않는 파일이면 LookupError."""
    top = subprocess.run(["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    rel = path.resolve().relative_to(pathlib.Path(top).resolve()).as_posix()
    added = subprocess.run(["git", "-C", top, "log", "--diff-filter=A", "--format=%H", "--", rel],
                           capture_output=True, text=True, check=True).stdout.split()
    if not added:
        raise LookupError(f"git 이 추적하지 않는 계약이다: {rel}")
    return subprocess.run(["git", "-C", top, "show", f"{added[-1]}:{rel}"],
                          capture_output=True, text=True, check=True).stdout


def helper_blocks(text: str) -> list[tuple[str, str]]:
    found = []
    for body in BLOCK.findall(text):
        lines = body.splitlines()
        first = 1 if lines and lines[0].startswith("#!") else 0
        m = NAME.match(lines[first]) if len(lines) > first else None
        if m:
            found.append((m.group(1), body))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="계약 안 측정 도우미 블록을 떼어 저장한다")
    parser.add_argument("--sealed", action="store_true", help="계약을 처음 담은 커밋의 판을 읽는다")
    parser.add_argument("contract")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    path = pathlib.Path(args.contract)
    try:
        text = sealed_text(path) if args.sealed else path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, subprocess.CalledProcessError, LookupError, ValueError) as exc:
        print(f"계약을 읽지 못했다: {args.contract} — {exc}", file=sys.stderr)
        return 2

    blocks = helper_blocks(text)
    if not blocks:
        print(f"뗄 도우미 블록이 없다: {args.contract}", file=sys.stderr)
        return 3
    names = [name for name, _ in blocks]
    duplicated = sorted({name for name in names if names.count(name) > 1})
    if duplicated:
        # 하나만 골라 쓰면 어느 판으로 쟀는지 알 수 없다 — 아무것도 쓰지 않는다
        print(f"같은 이름 블록이 둘 이상이다: {' '.join(duplicated)}", file=sys.stderr)
        return 1

    out = pathlib.Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, body in blocks:
        (out / name).write_text(body, encoding="utf-8")
    print(f"{len(blocks)} 개 저장: {' '.join(names)} → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
