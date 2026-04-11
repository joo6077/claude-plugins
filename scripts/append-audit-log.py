#!/usr/bin/env python3
"""
append-audit-log.py — orchestrator-audit-log.md 자동 append

카이젠 사이클 완료 시 Step 11 Final 에서 실행된다. 이번 사이클의 meta-issue
(수동 개입, Post-Kaizen Checklist 실패 항목, orchestrator SKILL.md 수동 edit) 를
`.harness/.meta/orchestrator-audit-log.md` 에 append-only 로 기록한다.

다음 사이클 Step 0.5 Orchestrator Self-Audit 이 이 파일을 읽어 재발 감시한다.

사용법:
    python3 scripts/append-audit-log.py --cycle-id <id> [옵션]

옵션:
    --cycle-id <id>          사이클 식별자 (예: kaizen/2026-04-11-research)
    --failures <file>        Post-Kaizen Checklist 실패 항목 JSON 파일 경로
    --manual-edits <file>    수동으로 edit 된 orchestrator SKILL.md 라인 정보 JSON
    --notes <text>           자유 기술 (1 줄)
    --dry-run                append 하지 않고 stdout 에 미리보기만
    --help                   사용법 출력

입력 JSON 형식:
    failures.json:
        [
            {"check": "docs-site-regen", "reason": "docs/harness/*.html not regenerated"},
            ...
        ]
    manual-edits.json:
        [
            {"file": ".claude/skills/kaizen-orchestrator/SKILL.md", "line_count": 12, "reason": "Step 11.5 added"},
            ...
        ]
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG = REPO_ROOT / ".harness/.meta/orchestrator-audit-log.md"


def load_json(path: Path | None) -> list[dict]:
    if path is None:
        return []
    if not path.exists():
        print(f"WARN: {path} 없음 — 빈 목록으로 처리", file=sys.stderr)
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError as exc:
        print(f"ERROR: {path} JSON 파싱 실패: {exc}", file=sys.stderr)
        sys.exit(2)


def render_entry(
    cycle_id: str,
    failures: list[dict],
    manual_edits: list[dict],
    notes: str,
) -> str:
    today = datetime.date.today().isoformat()
    lines: list[str] = []
    lines.append(f"## {today} — {cycle_id}")
    lines.append("")
    lines.append(
        f"**Cycle:** {cycle_id}  "
    )
    lines.append(
        f"**Generated:** `scripts/append-audit-log.py` (auto-append)  "
    )
    if notes:
        lines.append(f"**Notes:** {notes}  ")
    lines.append("")

    lines.append("### Post-Kaizen Checklist failures")
    lines.append("")
    if failures:
        for f in failures:
            check = f.get("check", "unknown")
            reason = f.get("reason", "")
            lines.append(f"- **{check}**: {reason}")
    else:
        lines.append("- 없음 (모든 체크 PASS)")
    lines.append("")

    lines.append("### Orchestrator SKILL.md manual edits")
    lines.append("")
    if manual_edits:
        for m in manual_edits:
            file = m.get("file", "unknown")
            line_count = m.get("line_count", 0)
            reason = m.get("reason", "")
            lines.append(f"- `{file}` (+/- {line_count} lines): {reason}")
    else:
        lines.append("- 없음 (수동 개입 없이 완료)")
    lines.append("")

    lines.append("### Next-cycle watchlist")
    lines.append("")
    if failures:
        for f in failures:
            check = f.get("check", "unknown")
            lines.append(f"- [ ] `{check}` 재발 방지 — Step 0.5 에서 확인")
    else:
        lines.append("- 특별 감시 대상 없음")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--cycle-id", required=False, default="unknown-cycle")
    parser.add_argument(
        "--failures", type=Path, default=None, help="Post-Kaizen 실패 JSON 파일"
    )
    parser.add_argument(
        "--manual-edits",
        type=Path,
        default=None,
        help="수동 edit 목록 JSON 파일",
    )
    parser.add_argument("--notes", default="", help="자유 기술 (1 줄)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="append 하지 않고 stdout 미리보기",
    )
    args = parser.parse_args()

    if not AUDIT_LOG.exists():
        print(f"ERROR: {AUDIT_LOG} 없음. 먼저 파일을 생성하세요.", file=sys.stderr)
        return 2

    failures = load_json(args.failures)
    manual_edits = load_json(args.manual_edits)

    entry = render_entry(args.cycle_id, failures, manual_edits, args.notes)

    if args.dry_run:
        print("=== DRY RUN (append 안 됨) ===")
        print(entry)
        return 0

    # Append-only
    current = AUDIT_LOG.read_text(encoding="utf-8")
    if not current.endswith("\n"):
        current += "\n"
    AUDIT_LOG.write_text(current + entry, encoding="utf-8")
    print(
        f"append-audit-log: {AUDIT_LOG.relative_to(REPO_ROOT)} 에 1 개 엔트리 append "
        f"(failures={len(failures)}, manual_edits={len(manual_edits)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
