#!/usr/bin/env python3
"""check-user-hook-overlap.py 가 개인 설정과 harness 플러그인 훅의 겹침을 잡고, 설정이 없으면 건너뛰는지 보는 시험.

임시 폴더에 개인 설정 폴더 모양을 만들고 --settings-dir 를 바꿔 돌린다.
  1. 설정 폴더가 없음 → 종료 코드 0, 출력이 정확히 「개인 설정 없음 — 건너뜀」 한 줄
  2. 설정 폴더는 있으나 settings.json · settings.local.json 이 없음 → 0, 같은 한 줄
  3. settings.json 에 다른 훅만 있음 → 0, 출력이 정확히 「겹침 없음 (설정 파일 1 개)」 한 줄
  4. settings.json 이 두 훅을 Stop · PostToolUse 에 등록 → 1, 「겹침:」 줄의 이벤트가 차례대로 Stop · PostToolUse
  5. settings.local.json 에만 qa-pending-check.sh → 1, 「겹침:」 줄 하나가 settings.local.json 을 가리킨다
  6. settings.json 이 깨진 JSON → 2, `UNREADABLE` 로 시작하는 줄 하나
  7. 두 파일 모두 있고 겹침 없음 → 0, 출력이 정확히 「겹침 없음 (설정 파일 2 개)」 한 줄

사용법:
    python3 scripts/test-check-user-hook-overlap.py [--tool <도구 사본 경로>]

--tool 은 음성 대조용이다 — 늘 「개인 설정 없음 — 건너뜀」 을 찍고 0 으로 끝나는 사본을 주면 경우 3 ~ 7 이 실패해야 한다.
종료 코드는 harness/evals/gate-exit-codes.md 의 값을 쓴다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP = "개인 설정 없음 — 건너뜀"


def hook(event: str, command: str, matcher: str | None = None) -> dict:
    entry = {"hooks": [{"type": "command", "command": command, "timeout": 10}]}
    if matcher:
        entry["matcher"] = matcher
    return {event: [entry]}


OTHER = {"hooks": {**hook("PreToolUse", "bash ~/.claude/hooks/parallel-session-guard.sh", "Bash")}}
BOTH = {"hooks": {**hook("Stop", "bash /Users/x/.claude/hooks/qa-pending-check.sh"),
                  **hook("PostToolUse", "bash ~/.claude/hooks/lint-contract-oracle.sh", "Edit|Write")}}
LOCAL_QA = {"hooks": hook("Stop", "bash ~/.claude/hooks/qa-pending-check.sh")}

# 모양마다 설정 폴더에 둘 파일 — 값이 dict 면 JSON, 글이면 그대로 쓴다. None 이면 폴더도 만들지 않는다
SHAPES = {
    "no-folder": None,
    "empty-folder": {},
    "other-only": {"settings.json": OTHER},
    "both-hooks": {"settings.json": BOTH},
    "local-only": {"settings.json": OTHER, "settings.local.json": LOCAL_QA},
    "broken-json": {"settings.json": "{ not json"},
    "two-clean": {"settings.json": OTHER, "settings.local.json": {"permissions": {}}},
}


def run_case(workdir: Path, shape: str, tool: Path) -> tuple[int, list[str]]:
    settings_dir = workdir / shape
    files = SHAPES[shape]
    if files is not None:
        settings_dir.mkdir()
        for name, body in files.items():
            text = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
            (settings_dir / name).write_text(text, encoding="utf-8")
    result = subprocess.run(
        ["python3", str(tool), "--settings-dir", str(settings_dir)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
    )
    return result.returncode, result.stdout.splitlines()


def overlap_lines(lines: list[str]) -> list[str]:
    return [line for line in lines if line.startswith("겹침:")]


# (이름표, 모양, 기대 종료 코드, 출력 판정)
CASES = [
    ("1 설정 폴더가 없으면 건너뛰고 0", "no-folder", 0, lambda lines: lines == [SKIP]),
    ("2 설정 파일이 없으면 건너뛰고 0", "empty-folder", 0, lambda lines: lines == [SKIP]),
    ("3 다른 훅만 있으면 0", "other-only", 0, lambda lines: lines == ["겹침 없음 (설정 파일 1 개)"]),
    ("4 두 훅이 다 있으면 1", "both-hooks", 1,
     lambda lines: [line.split(" ")[2] for line in overlap_lines(lines)] == ["Stop", "PostToolUse"]),
    ("5 settings.local.json 에만 있어도 1", "local-only", 1,
     lambda lines: len(overlap_lines(lines)) == 1 and "settings.local.json Stop " in overlap_lines(lines)[0]),
    ("6 깨진 JSON 은 2", "broken-json", 2,
     lambda lines: len([line for line in lines if line.startswith("UNREADABLE ")]) == 1),
    ("7 두 파일 다 겹침 없으면 0", "two-clean", 0, lambda lines: lines == ["겹침 없음 (설정 파일 2 개)"]),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="check-user-hook-overlap.py 시험")
    parser.add_argument("--tool", type=Path, default=REPO_ROOT / "scripts/check-user-hook-overlap.py")
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
