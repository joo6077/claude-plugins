#!/usr/bin/env python3
"""
append-audit-log.py — orchestrator-audit-log.md 자동 append

카이젠 사이클 완료 시 Step 11 Final 에서 실행된다. 이번 사이클의 meta-issue
(수동 개입, Post-Kaizen Checklist 실패 항목, orchestrator SKILL.md 수동 edit) 를
`.harness/.meta/orchestrator-audit-log.md` 에 append-only 로 기록한다.

다음 사이클 Step 0.5 Orchestrator Self-Audit 이 이 파일을 읽어 재발 감시한다.

두 가지 모드가 있다:

- **cycle 모드 (기본)** — 사이클 종료 시 전체 엔트리(헤딩 + 3 개 하위 섹션) 를 append.
- **phase 모드 (`--phase`)** — Phase 종료 시 `scripts/finalize-phase.sh` 가 호출한다.
  한 줄짜리 phase 결과 레코드만 append 하므로 사이클당 14 개 헤딩이 쌓이지 않는다.

사용법:
    python3 scripts/append-audit-log.py --cycle-id <id> [옵션]
    python3 scripts/append-audit-log.py --phase <N> --result <pass|fail> [--date YYYY-MM-DD]

옵션:
    --cycle-id <id>          사이클 식별자 (예: kaizen/2026-04-11-research).
                             생략 시 .harness/.meta/kaizen-state.yaml 의 cycle_id →
                             git 브랜치명 → "unknown-cycle" 순으로 해석한다
    --phase <N>              phase 모드. Phase 번호 (1 이상 정수)
    --result <pass|fail>     phase 모드 필수. Regression 결과
    --date <YYYY-MM-DD>      phase 모드 기록 날짜 (기본: 오늘)
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
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG = REPO_ROOT / ".harness/.meta/orchestrator-audit-log.md"
STATE_FILE = REPO_ROOT / ".harness/.meta/kaizen-state.yaml"


def resolve_cycle_id(explicit: str | None) -> str:
    """cycle-id 해석 ladder: 명시값 → kaizen-state.yaml → git 브랜치 → unknown-cycle."""
    if explicit:
        return explicit
    if STATE_FILE.exists():
        m = re.search(
            r'(?m)^cycle_id:\s*"?([^"\n]+)"?\s*$',
            STATE_FILE.read_text(encoding="utf-8"),
        )
        if m and m.group(1).strip():
            return m.group(1).strip()
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except OSError:
        pass
    return "unknown-cycle"


def render_phase_record(cycle_id: str, phase: int, result: str, date: str) -> str:
    """Phase 종료 1 줄 레코드. 라인 자체가 cycle_id 를 담아 self-describing 하다."""
    return f"- Phase {phase} — {result} · {cycle_id} · {date}\n"


def append_phase_record(
    cycle_id: str, phase: int, result: str, date: str, dry_run: bool
) -> int:
    header = f"### Phase log — {cycle_id}"
    record = render_phase_record(cycle_id, phase, result, date)
    current = AUDIT_LOG.read_text(encoding="utf-8")
    block = "" if header in current else f"\n{header}\n\n"

    if dry_run:
        print("=== DRY RUN (append 안 됨) ===")
        print(f"{block}{record}", end="")
        return 0

    if not current.endswith("\n"):
        current += "\n"
    AUDIT_LOG.write_text(current + block + record, encoding="utf-8")
    print(
        f"append-audit-log: {AUDIT_LOG.relative_to(REPO_ROOT)} 에 Phase {phase} "
        f"{result} 레코드 append (cycle={cycle_id})"
    )
    return 0


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
    parser.add_argument("--cycle-id", required=False, default=None)
    parser.add_argument(
        "--phase",
        type=int,
        default=None,
        help="phase 모드 — Phase 번호 (1 이상)",
    )
    parser.add_argument(
        "--result",
        choices=("pass", "fail"),
        default=None,
        help="phase 모드 필수 — Regression 결과",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="phase 모드 기록 날짜 (기본: 오늘)",
    )
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

    cycle_id = resolve_cycle_id(args.cycle_id)

    # phase 모드 — finalize-phase.sh 가 Phase 종료마다 호출한다
    if args.phase is not None or args.result is not None:
        if args.phase is None or args.result is None:
            print(
                "ERROR: phase 모드는 --phase 와 --result 를 함께 요구한다 "
                "(예: --phase 4 --result pass)",
                file=sys.stderr,
            )
            return 2
        if args.phase < 1:
            print(
                f"ERROR: --phase 는 1 이상의 정수 (받은 값: {args.phase})",
                file=sys.stderr,
            )
            return 2
        date = args.date or datetime.date.today().isoformat()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            print(
                f"ERROR: --date 는 YYYY-MM-DD 형식 (받은 값: {date})",
                file=sys.stderr,
            )
            return 2
        return append_phase_record(
            cycle_id, args.phase, args.result, date, args.dry_run
        )

    failures = load_json(args.failures)
    manual_edits = load_json(args.manual_edits)

    entry = render_entry(cycle_id, failures, manual_edits, args.notes)

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
