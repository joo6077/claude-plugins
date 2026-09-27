#!/usr/bin/env python3
"""check-cause-table-copies.py — preflight 두 스킬이 든 「실패 원인 가르기」 판정 표 사본이 원문과 글자까지 같은지 잰다.

원문은 `harness/skills/sprint/SKILL.md` Step 3 의 `| 공용 작업 폴더 |` 줄부터 `- **미확정**` 줄까지다
(판정 표와 CI 에서만 실패할 때의 두 경우). 킷은 따로 설치되어 원문을 읽지 못하므로 사본을 든다.
원문 첫 줄이 강화되고 두 경우가 더해졌는데 사본 둘이 따라가지 못한 일이 있었다(2026-09-27 Codex 점검).

같다고 보는 기준은 reviewer 사본 검사와 같다 — 줄 앞 공백과 인용 표식 `>` · 끝 공백을 떼고 빈 줄을 버린 뒤,
원문 덩어리가 사본의 `## 실패 원인 가르기` 절 안에 끊김 없이 나오면 같다.

출력은 파일마다 `<상태> <경로>` 한 줄과 끝의 요약 한 줄이다.
  OK · MISMATCH · UNREADABLE(뒤에 이유) · CANON_MISSING(원문 덩어리를 못 찾음)

Usage:
    python3 scripts/check-cause-table-copies.py

exit 0 = 둘 다 같다, 1 = 다른 사본이 있다, 2 = 원문이나 사본을 읽지 못했다 (1 과 함께 나면 2).
값의 정의는 `harness/evals/gate-exit-codes.md`.
"""
import sys

from plugin_utils import REPO_ROOT, contains_block, normalized

CANON = "harness/skills/sprint/SKILL.md"
BLOCK_START = "| 공용 작업 폴더 |"
BLOCK_END = "- **미확정**"
COPY_SECTION = "## 실패 원인 가르기"

COPIES = [
    "flutter-toolkit/skills/flutter-preflight/SKILL.md",
    "react-kit/skills/react-preflight/SKILL.md",
]


def read_lines(rel: str) -> list[str]:
    return (REPO_ROOT / rel).read_text(encoding="utf-8").split("\n")


def canonical_block(lines: list[str]) -> list[str]:
    """시작 줄부터 끝 줄까지. 둘 중 하나라도 못 찾으면 빈 목록이다."""
    block: list[str] = []
    for line in lines:
        if not block and not line.startswith(BLOCK_START):
            continue
        block.append(line)
        if line.startswith(BLOCK_END):
            return block
    return []


def copy_section(lines: list[str]) -> list[str]:
    section: list[str] = []
    inside = False
    for line in lines:
        if line.startswith(COPY_SECTION):
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            section.append(line)
    return section


def main() -> int:
    try:
        block = normalized(canonical_block(read_lines(CANON)))
    except (OSError, UnicodeDecodeError) as error:
        print(f"UNREADABLE {CANON} {error}")
        return 2
    if not block:
        print(f"CANON_MISSING {CANON} `{BLOCK_START}` 줄부터 `{BLOCK_END}` 줄까지의 덩어리가 없다")
        return 2

    violations = infra_errors = 0
    for rel in COPIES:
        try:
            section = normalized(copy_section(read_lines(rel)))
        except (OSError, UnicodeDecodeError) as error:
            print(f"UNREADABLE {rel} {error}")
            infra_errors += 1
            continue
        if contains_block(section, block):
            print(f"OK {rel}")
        else:
            print(f"MISMATCH {rel}")
            violations += 1

    print(f"checked={len(COPIES)} violations={violations} infra_errors={infra_errors}")
    if infra_errors:
        return 2
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
