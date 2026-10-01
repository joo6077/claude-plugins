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
    2 — 구조적 에러 (evals.json 파싱 실패 · 못 읽음(대상 없는 바로가기 포함) · 내용이 객체가 아님(null · 숫자 · 글 · 목록) ·
        목록 열쇠의 값이 목록이 아니거나 항목 모양이 허용 목록 밖 ·
        eval 항목 0 개, 이름으로 준 킷이 없는 킷이거나 평가 파일이 없음)
        못 읽은 킷 · 항목 없는 킷이 있어도 나머지 킷은 끝까지 재고, 그 킷 이름을 모두 적은 뒤 2 로 끝난다
"""

import argparse
import json
import os
import sys
from pathlib import Path

from plugin_utils import REPO_ROOT, load_marketplace

# 평가 대상은 마켓 목록의 킷 가운데 evals/evals.json 이 있는 것이다. 손 목록은 새 킷을 조용히 빠뜨린다.
# 형식이 달라 이 러너로 못 도는 킷만 이유와 함께 뺀다 — 빼는 줄은 `SKIP <킷> (<사유>)` 로 찍는다
SKIP_KITS = {
    "howto-kit": "게이트 픽스처 형식 — CI 가 sh howto-kit/evals/run-evals.sh 로 따로 돈다",
}


def eval_kits() -> list[str]:
    names = [plugin["name"] for plugin in load_marketplace().get("plugins", [])]
    # 대상 없는 바로가기는 파일 자리가 있으니 대상이다 — 못 읽음으로 잰다
    have = [name for name in names if os.path.lexists(REPO_ROOT / name / "evals" / "evals.json")]
    # 평가 파일이 없는 킷도 이름을 찍는다 — 다른 이름으로 둔 킷이 소리 없이 빠지지 않게
    absent = [name for name in names if name not in have]
    if absent:
        print(f"평가 파일(evals/evals.json) 없는 킷 {len(absent)} 개 — 대상 아님: {', '.join(absent)}")
    return have

# 못 읽거나 깨진 평가 파일 — 없는 파일(None)과 갈라 그 킷 이름을 모은다
UNREADABLE = object()
# eval 항목이 0 개인 평가 파일 — 못 읽음과 따로 모아 끝에 적는다
EMPTY = object()
JSON_KINDS = {type(None): "null", bool: "참거짓", int: "숫자", float: "숫자", str: "글", list: "목록"}

# 평가 항목이 쓸 수 있는 열쇠와 값 모양 — 2026-10-01 레포 평가 파일을 세어 정한 허용 목록이다.
# 여기 없는 열쇠 · 모양은 구조 오류다. 오타 난 열쇠도 그래서 걸린다
ITEM_FIELDS = {"id": (int, str), "skill": (str,), "agent": (str,), "prompt": (str,), "expected_output": (str,),
               "expect": (dict,), "assertions": (list,), "example": (str,), "fixture": (str,)}
ITEM_REQUIRED = ("id", "prompt", "assertions")
ITEM_ONE_OF = (("skill", "agent"), ("expected_output", "expect"))


def kind_of(value) -> str:
    return "객체" if isinstance(value, dict) else JSON_KINDS.get(type(value), type(value).__name__)


def item_problem(entry) -> str | None:
    if not isinstance(entry, dict):
        return f"객체가 아니다 ({kind_of(entry)})"
    unknown = sorted(set(entry) - set(ITEM_FIELDS))
    if unknown:
        return f"모르는 열쇠 {', '.join(unknown)}"
    for name, types in ITEM_FIELDS.items():
        # bool 은 int 의 하위 형이라 따로 막는다
        if name in entry and (isinstance(entry[name], bool) or not isinstance(entry[name], types)):
            return f"{name} 값이 {kind_of(entry[name])}"
    missing = [name for name in ITEM_REQUIRED if name not in entry]
    if missing:
        return f"{', '.join(missing)} 없음"
    for pair in ITEM_ONE_OF:
        if sum(name in entry for name in pair) != 1:
            return f"{' · '.join(pair)} 가운데 하나만 있어야 한다"
    for n, assertion in enumerate(entry["assertions"], 1):
        if isinstance(assertion, str):
            continue
        if isinstance(assertion, dict) and sorted(assertion) == ["text", "type"] \
                and all(isinstance(value, str) for value in assertion.values()):
            continue
        return f"assertions 의 {n} 번째가 글도 text · type 객체도 아니다 ({kind_of(assertion)})"
    return None


def shape_problem(data: dict) -> str | None:
    """목록 열쇠의 값과 그 항목이 허용 목록 모양인지 본다. 어긋난 첫 자리의 까닭 한 줄, 맞으면 None."""
    for key in ("evals", "tests", "cases"):
        if key not in data:
            continue
        if not isinstance(data[key], list):
            return f"{key} 가 목록이 아니다 ({kind_of(data[key])})"
        for n, entry in enumerate(data[key], 1):
            problem = item_problem(entry)
            if problem:
                return f"{key} 의 {n} 번째 항목 — {problem}"
    return None


PLACEHOLDER_PATTERNS = [
    "(placeholder)",
    "(TODO:",
    "TBD",
    "FIXME",
]

def load_evals(kit: str) -> dict | object | None:
    """evals.json 로드. 파일 없으면 None, 못 읽거나 파싱 실패면 UNREADABLE 을 돌려준다.

    여기서 끝내지 않는 것은 한 킷 때문에 뒤 킷을 못 재는 일을 막으려는 것이다 — 종료 코드 2 는 main 이 낸다.

    exit code 구분 (run-evals.py docstring 과 일치):
      - 0: 전체 PASS
      - 1: FAIL 있음 (assertion 불충족)
      - 2: 구조적 에러 (evals.json 파싱 실패 · 파일 손상 등 회복 불가)

    Phase 7 kaizen 에서 backend-kit/infra-kit ER-01 재발 방지를 위해 강화 (2026-04-24).
    """
    path = REPO_ROOT / kit / "evals" / "evals.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if os.path.lexists(path):
            print(f"UNREADABLE {path} (바로가기 대상 없음)", file=sys.stderr)
            return UNREADABLE
        return None
    except OSError as exc:
        # 권한 등으로 못 읽은 파일을 통과로 치지 않는다 — 파싱 실패와 같은 구조 오류다
        print(f"UNREADABLE {path} ({exc.strerror})", file=sys.stderr)
        return UNREADABLE
    except json.JSONDecodeError as exc:
        print(f"  ERROR: {path} parse error: {exc}", file=sys.stderr)
        return UNREADABLE
    if not isinstance(data, dict):
        # null 을 그대로 넘기면 「파일 없음」 None 과 섞여 통과하고, 숫자 · 글은 아래에서 추적 출력으로 죽는다
        print(f"  ERROR: {path} 내용이 객체가 아니다 ({JSON_KINDS.get(type(data), type(data).__name__)})", file=sys.stderr)
        return UNREADABLE
    problem = shape_problem(data)
    if problem:
        print(f"  ERROR: {path} {problem}", file=sys.stderr)
        return UNREADABLE
    return data


def get_eval_list(data: dict) -> list[dict]:
    # api-kit 은 사례를 `cases` 에 둔다 — 이 열쇠를 안 읽으면 킷을 목록에 넣어도 0 건으로 통과한다
    return data.get("evals") or data.get("tests") or data.get("cases") or []


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

    # api-kit 뷰어 사례는 기대 결과를 글이 아니라 `expect` 수치로 적는다
    if not expected.strip() and not entry.get("expect"):
        failures.append(f"eval #{eval_id} ({skill}): expected_output 비어있음")

    if not assertions:
        failures.append(f"eval #{eval_id} ({skill}): assertions 배열 비어있음")

    if has_placeholder(prompt):
        failures.append(f"eval #{eval_id} ({skill}): prompt에 placeholder 텍스트")
    if has_placeholder(expected):
        failures.append(f"eval #{eval_id} ({skill}): expected_output에 placeholder 텍스트")

    for i, a in enumerate(assertions):
        # 글자 한 줄짜리 assertion 은 출력 판정으로 본다
        text, atype = (a, "output") if isinstance(a, str) else (a.get("text", ""), a.get("type", ""))
        if not text.strip():
            failures.append(f"eval #{eval_id} ({skill}): assertion[{i}] text 비어있음")
        if atype not in ("behavior", "output"):
            failures.append(f"eval #{eval_id} ({skill}): assertion[{i}] type '{atype}' — 'behavior' 또는 'output'이어야 함")

    if verbose and not failures:
        print(f"    PASS eval #{eval_id} ({skill}): {len(assertions)} assertions")

    return failures


def validate_kit(kit: str, verbose: bool) -> tuple[int, int] | object | None:
    """플러그인 검증. (pass_count, fail_count) 반환. 평가 파일을 못 읽었으면 None, 항목이 0 개면 EMPTY."""
    data = load_evals(kit)
    if data is UNREADABLE:
        return None
    if data is None:
        if verbose:
            print(f"  SKIP (evals.json 없음)")
        return (0, 0)

    entries = get_eval_list(data)
    if not entries:
        # 검사한 항목이 0 개면 통과가 아니다 — {"evals": []} 나 목록 열쇠 없는 {} 가 여기로 온다
        path = REPO_ROOT / kit / "evals" / "evals.json"
        print(f"  ERROR: {path} 에 eval 항목이 없다 (evals · tests · cases 모두 비었거나 없음) — exit 2", file=sys.stderr)
        return EMPTY

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

    # 대상 없는 바로가기는 파일 자리가 있으니 넘겨서 못 읽음으로 잰다 — 「없음」 안내와 가른다
    if args.plugin and args.plugin not in SKIP_KITS \
            and not os.path.lexists(REPO_ROOT / args.plugin / "evals" / "evals.json"):
        # 이름으로 준 킷은 꼭 재라는 뜻이다. 없는 킷 · 평가 파일 없는 킷을 SKIP 하고 0 을 내면 오타가 통과한다
        reason = "킷 폴더 없음" if not (REPO_ROOT / args.plugin).is_dir() else "evals/evals.json 없음"
        print(f"ERROR: 이름으로 준 킷 {args.plugin} — {reason}", file=sys.stderr)
        return 2
    kits = [args.plugin] if args.plugin else eval_kits()
    grand_pass = 0
    grand_fail = 0
    unreadable = []
    empty = []

    for kit in kits:
        if kit in SKIP_KITS:
            print(f"SKIP {kit} ({SKIP_KITS[kit]})")
            continue

        print(f"→ {kit}")
        result = validate_kit(kit, args.verbose)
        if result is None:
            unreadable.append(kit)
            continue
        if result is EMPTY:
            empty.append(kit)
            continue
        passes, fails = result
        grand_pass += passes
        grand_fail += fails
        status = "PASS" if fails == 0 else "FAIL"
        print(f"  {status}: {passes} passed, {fails} failed")

    print()
    print(f"Total: {grand_pass} passed, {grand_fail} failed")
    if unreadable:
        print(f"못 읽은 킷 {len(unreadable)} 개: {', '.join(unreadable)}")
    if empty:
        print(f"항목 없는 킷 {len(empty)} 개: {', '.join(empty)}")
    if unreadable or empty:
        return 2

    return 1 if grand_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
