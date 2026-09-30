#!/usr/bin/env python3
"""
sync-evals.py — 각 플러그인 evals/evals.json 과 skills/ 디렉토리 동기화

각 플러그인의 `skills/` 디렉토리에 존재하는 스킬 목록과 `evals/evals.json` 의
`skill` 필드를 대조하여:
  - **missing**: 디스크에는 있는데 evals 에 없는 스킬 (스켈레톤 엔트리 자동 추가)
  - **orphan**: evals 에 있는데 디스크에 없는 스킬 (보고만, 수동 확인 필요)

사용법:
    python3 scripts/sync-evals.py [--check-only] [--dry-run]

옵션:
    --check-only  drift 만 감지하고 종료 (exit 1 if drift)
    --dry-run     변경 내용만 출력하고 파일 수정 안 함
    --help        사용법 출력

Exit codes:
    0 — no drift (check-only) 또는 동기화 완료
    1 — drift detected (check-only 모드만)
    2 — 구조적 에러 (evals.json 파싱 실패 · 못 읽음 포함)
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 대상은 마켓 목록의 킷 가운데 evals/evals.json 이 있는 것이다. 손 목록은 새 킷을 조용히 빠뜨린다.
# 스킬마다 사례를 두는 규칙이 맞지 않는 킷만 이유와 함께 뺀다 — 빼는 줄은 `SKIP <킷> (<사유>)` 로 찍는다
SKIP_KITS = {
    "harness": "evals.json 이 스킬 사례 목록이 아니다 — sprint · refactor-checklist 가 사례 없음으로 나온다",
    "howto-kit": "게이트 픽스처 형식 — CI 가 sh howto-kit/evals/run-evals.sh 로 따로 돈다",
}


def target_kits() -> list[str]:
    marketplace = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    names = [plugin["name"] for plugin in json.loads(marketplace.read_text(encoding="utf-8")).get("plugins", [])]
    have = [name for name in names if (REPO_ROOT / name / "evals" / "evals.json").is_file()]
    # 평가 파일이 없는 킷도 이름을 찍는다 — 다른 이름으로 둔 킷이 소리 없이 빠지지 않게
    absent = [name for name in names if name not in have]
    if absent:
        print(f"평가 파일(evals/evals.json) 없는 킷 {len(absent)} 개 — 대상 아님: {', '.join(absent)}")
    return have


def load_evals(kit: str) -> dict | None:
    path = REPO_ROOT / kit / "evals" / "evals.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        # 권한 등으로 못 읽은 파일을 없는 파일처럼 넘기면 --check-only 가 통과한다
        print(f"UNREADABLE {path} ({exc.strerror})", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        # 없는 파일처럼 SKIP 하면 깨진 평가 파일이 --check-only 를 통과한다
        print(f"ERROR: {path} parse error: {exc}", file=sys.stderr)
        sys.exit(2)


def save_evals(kit: str, data: dict) -> None:
    path = REPO_ROOT / kit / "evals" / "evals.json"
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def discover_skills(kit: str) -> set[str]:
    skills_dir = REPO_ROOT / kit / "skills"
    if not skills_dir.exists():
        return set()
    return {
        p.name
        for p in skills_dir.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    }


def get_eval_list(data: dict) -> list[dict]:
    """Return the list of eval entries from {evals: []}, {tests: []} or {cases: []} (api-kit)."""
    for key in ("evals", "tests", "cases"):
        if key in data:
            return data[key]
    return []


def set_eval_list(data: dict, entries: list[dict]) -> None:
    for key in ("evals", "tests", "cases"):
        if key in data:
            data[key] = entries
            return
    data["tests"] = entries


def get_skill_field(entry: dict) -> str:
    return entry.get("skill") or entry.get("target_skill") or ""


def next_id(entries: list[dict]) -> int:
    max_id = 0
    for e in entries:
        try:
            max_id = max(max_id, int(e.get("id", 0)))
        except (ValueError, TypeError):
            pass
    return max_id + 1


def make_skeleton_entry(skill_name: str, eval_id: int) -> dict:
    return {
        "id": eval_id,
        "skill": skill_name,
        "prompt": f"(placeholder) {skill_name} 스킬 동작 검증",
        "expected_output": "(TODO: add expected output)",
        "assertions": [
            {
                "text": f"({skill_name}) 스킬이 올바르게 실행된다",
                "type": "behavior",
            }
        ],
    }


def process_kit(kit: str, check_only: bool, dry_run: bool) -> tuple[int, int, int]:
    """Return (added, orphans, errors)."""
    data = load_evals(kit)
    if data is None:
        # No evals.json — SKIP
        return (0, 0, 0)

    entries = get_eval_list(data)
    disk_skills = discover_skills(kit)
    eval_skills = {get_skill_field(e) for e in entries if get_skill_field(e)}

    missing = sorted(disk_skills - eval_skills)
    orphans = sorted(eval_skills - disk_skills)

    added = 0
    if missing:
        if check_only or dry_run:
            for s in missing:
                print(f"  [{kit}] MISSING: {s} (would add skeleton entry)")
        else:
            eid = next_id(entries)
            for s in missing:
                entries.append(make_skeleton_entry(s, eid))
                eid += 1
                added += 1
            set_eval_list(data, entries)
            save_evals(kit, data)
            print(f"  [{kit}] added {added} skeleton entries")

    if orphans:
        for o in orphans:
            print(f"  [{kit}] ORPHAN: {o} (eval references non-existent skill)")

    return (added, len(orphans), 0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="drift 만 감지 (exit 1 if drift)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="변경 내용만 출력",
    )
    args = parser.parse_args()

    total_added = 0
    total_orphans = 0
    total_missing_preview = 0

    for kit in target_kits():
        if kit in SKIP_KITS:
            print(f"SKIP {kit} ({SKIP_KITS[kit]})")
            continue
        print(f"→ {kit}")
        data = load_evals(kit)
        if data is None:
            print(f"  SKIP (no evals.json)")
            continue
        entries = get_eval_list(data)
        disk_skills = discover_skills(kit)
        eval_skills = {get_skill_field(e) for e in entries if get_skill_field(e)}
        missing = sorted(disk_skills - eval_skills)
        total_missing_preview += len(missing)

        added, orphans, _ = process_kit(kit, args.check_only, args.dry_run)
        total_added += added
        total_orphans += orphans

    print()
    print(
        f"Total: {total_added} added, {total_orphans} orphans, "
        f"{total_missing_preview} missing (preview)"
    )

    if args.check_only:
        drift = total_missing_preview > 0 or total_orphans > 0
        return 1 if drift else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
