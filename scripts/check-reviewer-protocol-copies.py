#!/usr/bin/env python3
"""check-reviewer-protocol-copies.py — 킷 reviewer 일곱이 든 미검증 규칙 사본이 원문과 글자까지 같은지 잰다.

원문은 `harness/docs/guides/qa-evaluation-guide.md` 의 두 덩어리다.

  조항    §Canonical Unverified-Evidence Protocol 의 번호 목록 (「마커는」 조항부터 절 끝 인용문 앞까지)
  4 요건  §증거 분류 triage 의 `UNVERIFIED_ENV` 남용 방지 4 요건

킷은 따로 설치되어 원문을 읽지 못하므로 reviewer 가 사본을 든다. 원문이 바뀌었는데 사본이
따라가지 않은 일이 세 번 있었다 — 원문 머리말의 「현재 drift (2026-07-27 실측)」,
backend-reviewer 의 2026-08-13 재동기화, 2026-09-24 Phase 8 기록. 사람 다짐으로는 막히지 않아 CI 에 둔다.

같다고 보는 기준: 줄 앞 공백과 인용 표식 `>` 를 떼고 끝 공백을 떼고 빈 줄을 버린 뒤, 원문 덩어리가
사본 파일 안에 끊김 없이 나오면 같다. 들여쓰기 · 인용 표식 · 빈 줄 배치는 킷마다 달라도 된다.

출력은 파일마다 `<상태> <경로>` 한 줄과 끝의 요약 한 줄이다.
  OK · MISMATCH(뒤에 빠진 덩어리) · MISSING · UNREADABLE · UNLISTED · EXCLUDED(뒤에 이유)

Usage:
    python3 scripts/check-reviewer-protocol-copies.py

exit 0 = 일곱 모두 같다, 1 = 다른 사본이나 목록 밖 reviewer 가 있다,
2 = 원문이나 사본을 읽지 못했다 (1 과 함께 나면 2). 값의 정의는 `harness/evals/gate-exit-codes.md`.
"""
import re
import sys

from plugin_utils import REPO_ROOT

GUIDE = "harness/docs/guides/qa-evaluation-guide.md"
CLAUSE_SECTION = "## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)"
CLAUSE_START = re.compile(r"^1\. \*\*마커는")
REQUIREMENTS_HEADING = "#### `UNVERIFIED_ENV` 남용 방지 4 요건"

REVIEWERS = [
    "api-kit/agents/api-reviewer.md",
    "backend-kit/agents/backend-reviewer.md",
    "design-kit/agents/design-reviewer.md",
    "infra-kit/agents/infra-reviewer.md",
    "planning-kit/agents/planning-reviewer.md",
    "react-kit/agents/react-reviewer.md",
    "rust-kit/agents/rust-reviewer.md",
]

# 원문은 모든 `*-kit/agents/*-reviewer.md` 에 사본을 요구하지만 아직 들지 않은 파일. 이유는 출력에 그대로 나간다
EXCLUDED = {
    "howto-kit/agents/howto-reviewer.md":
        "사본을 아직 들지 않는다 — 2026-09-26 사용자 결정이 reviewer 일곱이었다. 다음 사이클 Phase 17 에서 넣는다",
}


def normalized(lines: list[str]) -> list[str]:
    stripped = (re.sub(r"^[\s>]*", "", line).rstrip() for line in lines)
    return [line for line in stripped if line]


def canonical_blocks(guide_lines: list[str]) -> tuple[list[str], list[str]]:
    """원문의 조항 덩어리와 4 요건 덩어리를 날것 그대로 돌려준다. 못 찾은 덩어리는 빈 목록이다."""
    clauses: list[str] = []
    if CLAUSE_SECTION in guide_lines:
        inside = False
        for line in guide_lines[guide_lines.index(CLAUSE_SECTION) + 1:]:
            if line.startswith("## "):
                break
            if not inside and CLAUSE_START.match(line):
                inside = True
            if inside:
                if line.startswith("> "):
                    break
                clauses.append(line)
    requirements: list[str] = []
    inside = False
    for line in guide_lines:
        if line.startswith(REQUIREMENTS_HEADING):
            inside = True
            continue
        if inside:
            if line.startswith(("> ", "#")):
                break
            requirements.append(line)
    return clauses, requirements


def contains_block(lines: list[str], block: list[str]) -> bool:
    width = len(block)
    return any(lines[start:start + width] == block for start in range(len(lines) - width + 1))


def main() -> int:
    repo = REPO_ROOT.resolve()
    try:
        guide_lines = (repo / GUIDE).read_text(encoding="utf-8").split("\n")
    except (OSError, UnicodeDecodeError) as error:
        print(f"UNREADABLE {GUIDE} {error}")
        return 2
    raw_clauses, raw_requirements = canonical_blocks(guide_lines)
    blocks = {"조항": normalized(raw_clauses), "4 요건": normalized(raw_requirements)}
    lost = [name for name, block in blocks.items() if not block]
    if lost:
        print(f"CANON_MISSING {GUIDE} 원문에서 못 찾은 덩어리: {' · '.join(lost)}")
        return 2

    violations = infra_errors = 0
    found = sorted(path.relative_to(repo).as_posix() for path in repo.glob("*-kit/agents/*-reviewer.md"))
    for rel in found:
        if rel in EXCLUDED:
            print(f"EXCLUDED {rel} {EXCLUDED[rel]}")
        elif rel not in REVIEWERS:
            print(f"UNLISTED {rel} 사본을 들어야 하는지 정해 REVIEWERS 나 EXCLUDED 에 넣는다")
            violations += 1

    for rel in REVIEWERS:
        path = repo / rel
        if not path.is_file():
            print(f"MISSING {rel}")
            infra_errors += 1
            continue
        try:
            copy_lines = normalized(path.read_text(encoding="utf-8").split("\n"))
        except (OSError, UnicodeDecodeError) as error:
            print(f"UNREADABLE {rel} {error}")
            infra_errors += 1
            continue
        absent = [name for name, block in blocks.items() if not contains_block(copy_lines, block)]
        if absent:
            print(f"MISMATCH {rel} 원문과 다른 덩어리: {' · '.join(absent)}")
            violations += 1
        else:
            print(f"OK {rel}")

    print(f"checked={len(REVIEWERS)} violations={violations} infra_errors={infra_errors} excluded={len(EXCLUDED)}")
    if infra_errors:
        return 2
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
