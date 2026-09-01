#!/usr/bin/env python3
"""
run-evals.py — evals.json 기반 플러그인 assertion 검증 러너

각 플러그인의 evals.json을 읽어 구조적 assertion을 검증한다:
  - SKILL.md 존재 여부
  - frontmatter 필수 필드 (name, description, user-invocable)
  - assertion 배열 비어있지 않음
  - prompt/expected_output 비어있지 않음
  - placeholder 텍스트 미포함

사용법:
    python3 scripts/run-evals.py [plugin-name] [--verbose]

옵션:
    plugin-name   특정 플러그인만 검증 (생략 시 전체)
    --verbose     상세 출력

Exit codes:
    0 — 전체 PASS
    1 — FAIL 있음
    2 — 구조적 에러
"""

import argparse
import json
import sys
from pathlib import Path

from plugin_utils import REPO_ROOT

ALL_KITS = [
    "harness", "flutter-toolkit", "rust-kit", "react-kit",
    "design-kit", "backend-kit", "infra-kit", "tone-kit",
]

PLACEHOLDER_PATTERNS = [
    "(placeholder)",
    "(TODO:",
    "TBD",
    "FIXME",
]

def load_evals(kit: str) -> dict | None:
    """evals.json 로드. 파일 없으면 None 반환. 파싱 실패 시 즉시 sys.exit(2) 로 종료.

    exit code 구분 (run-evals.py docstring 과 일치):
      - 0: 전체 PASS
      - 1: FAIL 있음 (assertion 불충족)
      - 2: 구조적 에러 (evals.json 파싱 실패 · 파일 손상 등 회복 불가)

    Phase 7 kaizen 에서 backend-kit/infra-kit ER-01 재발 방지를 위해 강화 (2026-04-24).
    """
    path = REPO_ROOT / kit / "evals" / "evals.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        print(f"  ERROR: {path} parse error: {exc}", file=sys.stderr)
        print(f"  FATAL: evals.json structural error — exit 2", file=sys.stderr)
        sys.exit(2)


def get_eval_list(data: dict) -> list[dict]:
    return data.get("evals") or data.get("tests") or []


def _asset_exists(kit: str, skill_name: str) -> bool:
    """스킬 SKILL.md 또는 에이전트 .md 존재 여부."""
    skill_path = REPO_ROOT / kit / "skills" / skill_name / "SKILL.md"
    if skill_path.exists():
        return True
    agent_path = REPO_ROOT / kit / "agents" / f"{skill_name}.md"
    return agent_path.exists()


def has_placeholder(text: str) -> bool:
    lower = text.lower()
    return any(p.lower() in lower for p in PLACEHOLDER_PATTERNS)


def validate_eval_entry(kit: str, entry: dict, verbose: bool) -> list[str]:
    """단일 eval 엔트리 검증. 실패 메시지 리스트 반환."""
    failures = []
    eval_id = entry.get("id", "?")
    skill = entry.get("skill", "") or entry.get("agent", "")
    prompt = entry.get("prompt", "")
    expected = entry.get("expected_output", "")
    assertions = entry.get("assertions", [])

    if not skill:
        failures.append(f"eval #{eval_id}: skill/agent 필드 비어있음")
        return failures

    if not _asset_exists(kit, skill):
        failures.append(f"eval #{eval_id}: '{skill}' — SKILL.md도 agent .md도 없음")

    if not prompt.strip():
        failures.append(f"eval #{eval_id} ({skill}): prompt 비어있음")

    if not expected.strip():
        failures.append(f"eval #{eval_id} ({skill}): expected_output 비어있음")

    if not assertions:
        failures.append(f"eval #{eval_id} ({skill}): assertions 배열 비어있음")

    if has_placeholder(prompt):
        failures.append(f"eval #{eval_id} ({skill}): prompt에 placeholder 텍스트")
    if has_placeholder(expected):
        failures.append(f"eval #{eval_id} ({skill}): expected_output에 placeholder 텍스트")

    for i, a in enumerate(assertions):
        text = a.get("text", "")
        atype = a.get("type", "")
        if not text.strip():
            failures.append(f"eval #{eval_id} ({skill}): assertion[{i}] text 비어있음")
        if atype not in ("behavior", "output"):
            failures.append(f"eval #{eval_id} ({skill}): assertion[{i}] type '{atype}' — 'behavior' 또는 'output'이어야 함")

    if verbose and not failures:
        print(f"    PASS eval #{eval_id} ({skill}): {len(assertions)} assertions")

    return failures


def validate_kit(kit: str, verbose: bool) -> tuple[int, int]:
    """플러그인 검증. (pass_count, fail_count) 반환.

    주의: evals.json 파싱 실패 시 load_evals 내부에서 sys.exit(2) 로 즉시 종료하므로
    본 함수는 파싱 실패 분기를 처리하지 않는다.
    """
    data = load_evals(kit)
    if data is None:
        if verbose:
            print(f"  SKIP (evals.json 없음)")
        return (0, 0)

    entries = get_eval_list(data)
    if not entries:
        print(f"  WARN: evals.json에 eval 엔트리가 없음")
        return (0, 0)

    total_pass = 0
    total_fail = 0

    for entry in entries:
        failures = validate_eval_entry(kit, entry, verbose)
        if failures:
            for msg in failures:
                print(f"    FAIL {msg}")
            total_fail += 1
        else:
            total_pass += 1

    return (total_pass, total_fail)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin", nargs="?", help="특정 플러그인만 검증")
    parser.add_argument("--verbose", "-v", action="store_true", help="상세 출력")
    args = parser.parse_args()

    kits = [args.plugin] if args.plugin else ALL_KITS
    grand_pass = 0
    grand_fail = 0

    for kit in kits:
        kit_path = REPO_ROOT / kit
        if not kit_path.exists():
            print(f"SKIP: {kit} (디렉토리 없음)")
            continue

        print(f"→ {kit}")
        passes, fails = validate_kit(kit, args.verbose)
        grand_pass += passes
        grand_fail += fails
        status = "PASS" if fails == 0 else "FAIL"
        print(f"  {status}: {passes} passed, {fails} failed")

    print()
    print(f"Total: {grand_pass} passed, {grand_fail} failed")

    return 1 if grand_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
