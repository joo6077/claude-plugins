#!/usr/bin/env python3
"""카이젠 오케스트레이션용 데이터 풀 수집 스크립트.

수집 소스:
  1. 글로벌 feedback: ~/.harness/feedback/evaluator/*.yaml
  2. Hub/10_Dev 내 .harness 디렉토리 보유 프로젝트들의 sprint-feedback + history
  3. docs/superpowers/followup-*.md 최근 파일
  4. 레포 자체의 .harness/history 최근 sprint-contract
  5. scripts/validate-plugin.py 최근 실행 결과 (옵션)

출력:
  .harness/.meta/kaizen-data-pool.md (기본)
  또는 --output <path> 로 다른 경로 지정

Usage:
  python3 scripts/collect-kaizen-data.py
  python3 scripts/collect-kaizen-data.py --output /tmp/kaizen-data.md
  python3 scripts/collect-kaizen-data.py --hub-dir ~/Hub/10_Dev
"""
from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 이 설치되지 않았습니다. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_OUTPUT = REPO_ROOT / ".harness" / ".meta" / "kaizen-data-pool.md"
DEFAULT_HUB = Path.home() / "Hub" / "10_Dev"
GLOBAL_FEEDBACK_DIR = Path.home() / ".harness" / "feedback" / "evaluator"

# `/insights` 외부 도구 산출물 자동 탐색 경로 (우선순위 순)
INSIGHTS_CANDIDATES = [
    REPO_ROOT / ".claude" / "kaizen-input" / "insights-report.md",
    Path.home() / ".claude" / "kaizen-input" / "insights-report.md",
]
INSIGHTS_FRESH_DAYS = 60  # 60일 초과 시 stale 경고


def collect_insights_report() -> dict | None:
    """`/insights` 외부 도구 산출물(insights-report.md)을 자동 탐색·로드한다.

    파일이 없으면 None 반환. 있으면 경로/mtime/content 를 dict 로 반환한다.
    카이젠 오케스트레이터 Step 0 에서 데이터 풀에 §0 (최상위) 으로 삽입된다.
    """
    for path in INSIGHTS_CANDIDATES:
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue
        mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        age_days = (datetime.datetime.now() - mtime).days
        return {
            "path": path,
            "mtime": mtime.isoformat(timespec="seconds"),
            "age_days": age_days,
            "stale": age_days > INSIGHTS_FRESH_DAYS,
            "content": content,
        }
    return None


def collect_global_feedback() -> dict:
    """글로벌 evaluator 피드백 통계와 샘플을 수집한다."""
    result = {
        "total": 0,
        "by_verdict": Counter(),
        "by_skill": Counter(),
        "by_project": Counter(),
        "reject_samples": [],
        "improvement_samples": [],
    }
    if not GLOBAL_FEEDBACK_DIR.exists():
        return result

    files = sorted(GLOBAL_FEEDBACK_DIR.glob("*.yaml"))
    result["total"] = len(files)

    for f in files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue

        ev = data.get("evaluation", {}) or {}
        verdict = ev.get("verdict", "UNKNOWN")
        result["by_verdict"][verdict] += 1
        result["by_skill"][data.get("skill", "unknown")] += 1
        result["by_project"][data.get("project_name", "unknown")] += 1

        ts = str(data.get("timestamp", ""))[:10]
        project = data.get("project_name", "?")

        if verdict == "REJECT":
            for r in (ev.get("reject_reasons") or [])[:2]:
                result["reject_samples"].append((ts, project, str(r)[:200]))

        diag = data.get("diagnosis", {}) or {}
        for s in (diag.get("improvement_suggestions") or [])[:2]:
            result["improvement_samples"].append((ts, project, str(s)[:200]))

    # 최근순 정렬 후 상위 n 유지
    result["reject_samples"] = sorted(result["reject_samples"], reverse=True)[:20]
    result["improvement_samples"] = sorted(result["improvement_samples"], reverse=True)[:15]
    return result


def collect_hub_projects(hub_dir: Path) -> list[dict]:
    """Hub/10_Dev 내 .harness 디렉토리 보유 프로젝트 정보를 수집한다."""
    projects: list[dict] = []
    if not hub_dir.exists():
        return projects

    for harness_dir in sorted(hub_dir.glob("*/.harness")):
        project_path = harness_dir.parent
        name = project_path.name
        if name == REPO_ROOT.name:
            continue  # 현재 레포 자신은 별도 처리

        entry = {"name": name, "path": str(project_path)}

        sf = harness_dir / "sprint-feedback.md"
        if sf.exists():
            text = sf.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
            entry["sprint_feedback_lines"] = len(lines)
            entry["sprint_feedback_head"] = "\n".join(lines[:20])

        history = harness_dir / "history"
        if history.exists():
            contracts = sorted(history.glob("*-sprint-contract.md"))
            entry["history_count"] = len(contracts)
            entry["recent_contracts"] = [c.name for c in contracts[-5:]]
        else:
            entry["history_count"] = 0

        projects.append(entry)
    return projects


def collect_followup_docs() -> list[Path]:
    """docs/superpowers/followup-*.md 최근 파일을 수집한다."""
    followup_dir = REPO_ROOT / "docs" / "superpowers"
    if not followup_dir.exists():
        return []
    return sorted(followup_dir.glob("followup-*.md"))[-5:]


def collect_recent_local_contracts() -> list[str]:
    """현재 레포의 최근 sprint-contract archive 이름들."""
    history = REPO_ROOT / ".harness" / "history"
    if not history.exists():
        return []
    contracts = sorted(history.glob("*-sprint-contract.md"))
    return [c.name for c in contracts[-10:]]


def run_validate_plugin() -> str | None:
    """validate-plugin.py 를 실행하여 현재 상태 스냅샷을 얻는다 (옵션)."""
    script = REPO_ROOT / "scripts" / "validate-plugin.py"
    if not script.exists():
        return None
    try:
        out = subprocess.check_output(
            ["python3", str(script)],
            cwd=str(REPO_ROOT),
            stderr=subprocess.STDOUT,
            timeout=60,
            text=True,
        )
        return out
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return getattr(e, "output", "") or str(e)


def render_data_pool(
    global_fb: dict,
    hub_projects: list[dict],
    followups: list[Path],
    local_contracts: list[str],
    validate_output: str | None,
    insights: dict | None = None,
) -> str:
    """수집한 데이터를 마크다운 data pool 로 렌더링한다."""
    now = datetime.datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Kaizen Data Pool",
        "",
        f"Generated: {now}",
        "Generator: `scripts/collect-kaizen-data.py`",
        "",
        "카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. "
        "이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.",
        "",
    ]

    # §0: /insights 리포트 (있을 때만, 모든 Phase 가 최우선 참조)
    if insights is not None:
        rel = insights["path"]
        try:
            rel = insights["path"].relative_to(REPO_ROOT)
        except ValueError:
            rel = insights["path"]
        stale_warn = " ⚠ STALE" if insights["stale"] else ""
        lines += [
            "## 0. `/insights` Report (외부 도구 산출물)",
            "",
            f"- 경로: `{rel}`",
            f"- 최근 갱신: {insights['mtime']} ({insights['age_days']}일 전){stale_warn}",
            "- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions)",
            "",
            "<details><summary>insights-report.md 본문</summary>",
            "",
            insights["content"].rstrip(),
            "",
            "</details>",
            "",
        ]
    else:
        lines += [
            "## 0. `/insights` Report",
            "",
            "- (없음) `~/.claude/kaizen-input/insights-report.md` 또는 `<repo>/.claude/kaizen-input/insights-report.md` 미존재",
            "- `/insights` 외부 도구 실행 후 산출물을 위 경로에 배치하면 다음 사이클부터 자동 통합된다.",
            "",
        ]

    lines += [
        "## 1. 글로벌 Evaluator Feedback",
        "",
        f"- 경로: `{GLOBAL_FEEDBACK_DIR}`",
        f"- 총 파일: **{global_fb['total']}**",
        "",
        "### Verdict 분포",
        "",
    ]
    for v, c in global_fb["by_verdict"].most_common():
        lines.append(f"- **{v}**: {c}")
    lines += [
        "",
        "### Skill 분포",
        "",
    ]
    for s, c in global_fb["by_skill"].most_common():
        lines.append(f"- `{s}`: {c}")
    lines += [
        "",
        "### Project 분포",
        "",
    ]
    for p, c in global_fb["by_project"].most_common():
        lines.append(f"- `{p}`: {c}")

    lines += ["", "### 최근 REJECT 사유 (Top 20)", ""]
    for ts, proj, reason in global_fb["reject_samples"]:
        lines.append(f"- [{ts}] **{proj}**: {reason}")

    lines += ["", "### 최근 Improvement Suggestions (Top 15)", ""]
    for ts, proj, sug in global_fb["improvement_samples"]:
        lines.append(f"- [{ts}] **{proj}**: {sug}")

    lines += [
        "",
        "## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백",
        "",
        f"- Hub 루트: `{DEFAULT_HUB}`",
        f"- 발견된 프로젝트: **{len(hub_projects)}**",
        "",
    ]
    for proj in hub_projects:
        lines += [
            f"### `{proj['name']}`",
            "",
            f"- 경로: `{proj['path']}`",
            f"- sprint-feedback.md: {proj.get('sprint_feedback_lines', 0)} lines",
            f"- history sprint-contracts: {proj.get('history_count', 0)}",
        ]
        if proj.get("recent_contracts"):
            lines.append("- 최근 contracts:")
            for c in proj["recent_contracts"]:
                lines.append(f"  - {c}")
        if proj.get("sprint_feedback_head"):
            lines += ["", "<details><summary>sprint-feedback.md 앞부분</summary>", "", "```markdown"]
            lines.append(proj["sprint_feedback_head"])
            lines += ["```", "", "</details>", ""]

    lines += [
        "",
        "## 3. Followup 문서",
        "",
    ]
    if followups:
        for p in followups:
            rel = p.relative_to(REPO_ROOT)
            lines.append(f"- `{rel}`")
    else:
        lines.append("- (없음)")

    lines += [
        "",
        "## 4. 현재 레포 최근 Sprint Contracts",
        "",
    ]
    if local_contracts:
        for c in local_contracts:
            lines.append(f"- `.harness/history/{c}`")
    else:
        lines.append("- (없음)")

    if validate_output is not None:
        lines += [
            "",
            "## 5. Validate-Plugin 최근 실행 스냅샷",
            "",
            "```text",
        ]
        # 너무 길면 뒤쪽만 tail
        snap = validate_output.strip().splitlines()
        if len(snap) > 80:
            lines.append("... (이전 출력 생략)")
            snap = snap[-80:]
        lines.extend(snap)
        lines += ["```", ""]

    lines += [
        "",
        "## 6. Phase 별 참조 가이드",
        "",
        "각 Phase subagent 는 아래 매핑을 참고하여 자신의 범위에 맞는 섹션을 우선 읽는다. "
        "§0 (/insights) 가 존재할 때는 **모든 Phase** 가 §0 을 최우선 참조한다.",
        "",
        "| Phase | 스킬 | 주요 참조 섹션 |",
        "|-------|------|---------------|",
        "| 1 설계 가이드 | skill-design-guide, agent-design-guide | §0 + §1 Improvement Suggestions |",
        "| 2 Contract | contract-design-guide + sprint-contract | §0 + §1 Reject 사유 (계약 모호성) |",
        "| 3 Evaluator | qa-evaluation-guide + qa-evaluator | §0 + §1 Improvement (L3, set intersection) |",
        "| 4 Harness | harness/skills/* (sprint-contract, qa-evaluator 제외) | §0 + §5 validate-plugin 현재 상태 |",
        "| 5 Flutter | flutter-toolkit/skills/* | §0 + §2 Hub 외부 프로젝트 (fit-pal, apps) |",
        "| 6 Design | design-kit/skills/* | §0 + §5 validate-plugin 현재 상태 |",
        "| 7 Backend | backend-kit/skills/* | §0 + §1 Backend 관련 feedback (있다면) |",
        "| 8 Infra | infra-kit/skills/* | §0 + §5 validate-plugin 현재 상태 |",
        "| 9 Rust | rust-kit/skills/* | §0 + §2 Hub 외부 프로젝트 (fit-pal server) |",
        "| 10 React | react-kit/skills/* | §0 + §3 followup-2026-04-11, §5 |",
        "| 11 Planning | planning-kit/skills/* | §0 + §1 planning 관련 feedback |",
        "| 12 Reflect | reflect-kit/skills/* | §0 + §1 Reflexion 패턴 피드백 |",
        "",
    ]

    return "\n".join(lines) + "\n"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="카이젠 오케스트레이션용 데이터 풀 수집",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"출력 경로 (default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--hub-dir",
        type=Path,
        default=DEFAULT_HUB,
        help=f"Hub 루트 (default: {DEFAULT_HUB})",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="validate-plugin.py 실행을 생략",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()

    print("[1/6] /insights 리포트 자동 탐색 중...", file=sys.stderr)
    insights = collect_insights_report()

    print("[2/6] 글로벌 feedback 수집 중...", file=sys.stderr)
    global_fb = collect_global_feedback()

    print("[3/6] Hub 외부 프로젝트 수집 중...", file=sys.stderr)
    hub_projects = collect_hub_projects(args.hub_dir)

    print("[4/6] followup 문서 수집 중...", file=sys.stderr)
    followups = collect_followup_docs()

    print("[5/6] 현재 레포 sprint-contract 이력 수집 중...", file=sys.stderr)
    local_contracts = collect_recent_local_contracts()

    validate_output: str | None = None
    if not args.skip_validate:
        print("[6/6] validate-plugin 스냅샷 실행 중...", file=sys.stderr)
        validate_output = run_validate_plugin()
    else:
        print("[6/6] validate-plugin 스냅샷 건너뜀 (--skip-validate)", file=sys.stderr)

    content = render_data_pool(
        global_fb, hub_projects, followups, local_contracts, validate_output, insights
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")

    print(f"\nData pool 생성: {args.output}", file=sys.stderr)
    if insights is not None:
        stale_marker = " ⚠ STALE" if insights["stale"] else ""
        print(
            f"  - /insights 리포트: {insights['path']} ({insights['age_days']}일 전){stale_marker}",
            file=sys.stderr,
        )
    else:
        print("  - /insights 리포트: 없음 (자동 탐색 경로 미존재)", file=sys.stderr)
    print(
        f"  - global feedback: {global_fb['total']}개",
        f"(REJECT {global_fb['by_verdict'].get('REJECT', 0)}, "
        f"APPROVE {global_fb['by_verdict'].get('APPROVE', 0)})",
        file=sys.stderr,
    )
    print(f"  - hub projects: {len(hub_projects)}개", file=sys.stderr)
    print(f"  - followups: {len(followups)}개", file=sys.stderr)
    print(f"  - local contracts: {len(local_contracts)}개", file=sys.stderr)


if __name__ == "__main__":
    main()
