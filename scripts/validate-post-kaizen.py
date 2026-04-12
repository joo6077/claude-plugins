#!/usr/bin/env python3
"""
validate-post-kaizen.py — Post-Kaizen Checklist 자동 검증 스크립트

카이젠 사이클 완료 후 PR 생성 전에 반드시 실행하여 12 개 항목을 검증한다.
하나라도 FAIL 이면 exit 1 을 반환하여 PR 생성 스크립트가 차단되도록 한다.

사용법:
    python3 scripts/validate-post-kaizen.py [--since <ref>]

옵션:
    --since <ref>  이 git ref 이후 변경된 파일 기준으로 검증 (기본: main)
    --verbose      각 체크의 상세 로그 출력
    --help         사용법 출력
"""

import argparse
import datetime
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class CheckResult:
    name: str
    status: str  # "PASS" | "FAIL" | "SKIP"
    summary: str
    evidence: list[str] = field(default_factory=list)
    hint: str = ""  # 수정 방법 안내 (FAIL 시 출력)


# FAIL 수정 힌트 매핑
FAIL_HINTS: dict[str, str] = {
    "validate-plugin": "python3 scripts/validate-plugin.py --fix 실행 후 재확인",
    "sync-docs": "python3 scripts/sync-docs.py 실행하여 README 동기화",
    "sync-orchestrator": "python3 scripts/sync-orchestrator.py 실행하여 SKILL.md 동기화",
    "plugin-json-bumps": "변경된 플러그인의 plugin.json version을 bump (bash scripts/release.sh <plugin> patch)",
    "marketplace-sync": "bash scripts/release.sh <plugin> patch 로 marketplace.json 갱신",
    "changelog-entry": "docs/kaizen/changelog.md에 오늘 날짜 섹션 추가 (## YYYY-MM-DD 형식)",
    "research-log": "docs/kaizen/research-log.md에 오늘 날짜 리서치 엔트리 추가",
    "per-kit-research-logs": "누락된 docs/<kit>/research-log.md 파일 생성 (리서치 스킬 실행)",
    "docs-site-regen": "/docs-site 스킬 실행하여 HTML 재생성",
    "cleanup-log": ".harness/.meta/cleanup-log.yaml에 오늘 날짜 엔트리 추가 (0 액션이어도 기록)",
    "failure-count": "bash scripts/finalize-phase.sh <phase> <pass|fail> 실행하여 last_updated 갱신",
    "evals-audit": "evals-audit-YYYY-MM-DD.md 파일 생성 (per-kit evals.json vs skills/ 대조)",
    "scope-isolation": "cross-phase 커밋을 분리하거나 revert 후 올바른 Phase 범위로 재커밋",
    "bare-fence": "python3 scripts/validate-plugin.py --fix --check=code-fence 실행",
}


def run(cmd: list[str], cwd: Path = REPO_ROOT) -> tuple[int, str, str]:
    """Run a command and return (code, stdout, stderr)."""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8"
    )
    return result.returncode, result.stdout, result.stderr


def git_diff_names(since: str) -> list[str]:
    """Return list of files changed since the given ref."""
    code, out, _ = run(["git", "diff", "--name-only", f"{since}..HEAD"])
    if code != 0:
        return []
    return [line for line in out.splitlines() if line.strip()]


def today() -> str:
    return datetime.date.today().isoformat()


# --- Checks ---------------------------------------------------------------


def check_validate_plugin() -> CheckResult:
    code, out, err = run(["python3", "scripts/validate-plugin.py"])
    if code == 0 and "7 OK" in out:
        return CheckResult(
            "validate-plugin",
            "PASS",
            "7 plugins, 7 OK",
            ["Total: 7 plugins, 7 OK"],
        )
    return CheckResult(
        "validate-plugin",
        "FAIL",
        f"exit {code}",
        [out.strip().splitlines()[-5:] if out else err[-200:]],
    )


def check_sync_docs() -> CheckResult:
    code, out, _ = run(["python3", "scripts/sync-docs.py", "--check-only"])
    if code == 0 and "동기화 상태" in out:
        return CheckResult("sync-docs", "PASS", "READMEs synced")
    return CheckResult("sync-docs", "FAIL", f"exit {code}", [out[-200:]])


def check_sync_orchestrator() -> CheckResult:
    code, out, err = run(
        ["python3", "scripts/sync-orchestrator.py", "--check-only"]
    )
    if code == 0:
        return CheckResult("sync-orchestrator", "PASS", "no drift")
    return CheckResult(
        "sync-orchestrator",
        "FAIL",
        f"drift detected (exit {code})",
        [err.strip() or out.strip()],
    )


def check_plugin_json_bumps(since: str) -> CheckResult:
    changed = git_diff_names(since)
    bumps = [
        f
        for f in changed
        if f.endswith("/.claude-plugin/plugin.json")
    ]
    if not bumps:
        return CheckResult(
            "plugin-json-bumps",
            "SKIP",
            "no plugin.json in diff (아무 플러그인도 바뀌지 않은 사이클)",
        )
    return CheckResult(
        "plugin-json-bumps",
        "PASS",
        f"{len(bumps)} plugin.json bumped",
        bumps,
    )


def check_marketplace_sync(since: str) -> CheckResult:
    changed = git_diff_names(since)
    plugin_bumps = [f for f in changed if f.endswith("/.claude-plugin/plugin.json")]
    market = ".claude-plugin/marketplace.json"
    if plugin_bumps and market not in changed:
        return CheckResult(
            "marketplace-sync",
            "FAIL",
            "plugin.json bumped but marketplace.json not updated",
            plugin_bumps,
        )
    if market in changed:
        return CheckResult(
            "marketplace-sync",
            "PASS",
            "marketplace.json updated",
        )
    return CheckResult(
        "marketplace-sync",
        "SKIP",
        "no plugin bumps this cycle",
    )


def check_changelog_entry(since: str) -> CheckResult:
    changelog = REPO_ROOT / "docs/kaizen/changelog.md"
    if not changelog.exists():
        return CheckResult("changelog-entry", "FAIL", "docs/kaizen/changelog.md missing")
    text = changelog.read_text(encoding="utf-8")
    t = today()
    # Check either today's date or within last 7 days
    if t in text:
        return CheckResult(
            "changelog-entry", "PASS", f"entry for {t} present"
        )
    return CheckResult(
        "changelog-entry",
        "FAIL",
        f"no entry for {t} in docs/kaizen/changelog.md",
    )


def check_research_log() -> CheckResult:
    rl = REPO_ROOT / "docs/kaizen/research-log.md"
    if not rl.exists():
        return CheckResult("research-log", "FAIL", "docs/kaizen/research-log.md missing")
    if today() in rl.read_text(encoding="utf-8"):
        return CheckResult("research-log", "PASS", f"entry for {today()}")
    return CheckResult(
        "research-log",
        "FAIL",
        f"no entry for {today()} in docs/kaizen/research-log.md",
    )


def check_per_kit_research_logs() -> CheckResult:
    per_kit_paths = [
        REPO_ROOT / "docs/backend/research-log.md",
        REPO_ROOT / "docs/infra/research-log.md",
        REPO_ROOT / "docs/rust/research-log.md",
        REPO_ROOT / "docs/react/research-log.md",
        REPO_ROOT / "docs/flutter/research-log.md",
    ]
    missing = [str(p.relative_to(REPO_ROOT)) for p in per_kit_paths if not p.exists()]
    if missing:
        return CheckResult(
            "per-kit-research-logs",
            "FAIL",
            f"{len(missing)} per-kit research-logs missing",
            missing,
        )
    return CheckResult(
        "per-kit-research-logs",
        "PASS",
        f"all 5 per-kit research-logs exist",
    )


def check_docs_site_regen(since: str) -> CheckResult:
    """Check if docs/harness/*.html was regenerated when source guides changed."""
    changed = git_diff_names(since)
    source_changed = [
        f
        for f in changed
        if f.startswith("harness/docs/guides/")
        or f.startswith("harness/references/")
    ]
    if not source_changed:
        return CheckResult(
            "docs-site-regen",
            "SKIP",
            "no harness source changes",
        )
    html_changed = [
        f for f in changed if f.startswith("docs/harness/") and f.endswith(".html")
    ]
    if not html_changed:
        return CheckResult(
            "docs-site-regen",
            "FAIL",
            "source guides changed but docs/harness/*.html not regenerated",
            source_changed,
        )
    return CheckResult(
        "docs-site-regen",
        "PASS",
        f"{len(html_changed)} HTML files regenerated",
    )


def check_cleanup_log() -> CheckResult:
    path = REPO_ROOT / ".harness/.meta/cleanup-log.yaml"
    if not path.exists():
        return CheckResult("cleanup-log", "FAIL", "cleanup-log.yaml missing")
    if today() in path.read_text(encoding="utf-8"):
        return CheckResult("cleanup-log", "PASS", f"entry for {today()}")
    return CheckResult(
        "cleanup-log",
        "FAIL",
        f"no entry for {today()} in cleanup-log.yaml",
    )


def check_failure_count() -> CheckResult:
    path = REPO_ROOT / ".harness/.meta/kaizen-failure-count.yaml"
    if not path.exists():
        return CheckResult("failure-count", "FAIL", "kaizen-failure-count.yaml missing")
    text = path.read_text(encoding="utf-8")
    if today() in text:
        return CheckResult("failure-count", "PASS", f"last_updated includes {today()}")
    return CheckResult(
        "failure-count",
        "FAIL",
        f"last_updated not {today()}",
    )


def check_evals_audit() -> CheckResult:
    path = REPO_ROOT / f".harness/.meta/evals-audit-{today()}.md"
    if path.exists():
        return CheckResult("evals-audit", "PASS", f"file for {today()} exists")
    # Accept any evals-audit-*.md from this week as fallback
    meta_dir = REPO_ROOT / ".harness/.meta"
    if meta_dir.exists():
        found = list(meta_dir.glob(f"evals-audit-{today()[:7]}*.md"))
        if found:
            return CheckResult(
                "evals-audit",
                "PASS",
                f"recent audit file: {found[-1].name}",
            )
    return CheckResult(
        "evals-audit",
        "FAIL",
        f"no evals-audit-{today()}.md or this-month file",
    )


def check_scope_isolation(since: str) -> CheckResult:
    """Check that Phase 1~10 source files do not overlap across phases.

    This is a light-weight check: ensures no single commit touches both
    harness/skills/ and react-kit/skills/ (cross-phase boundary violation).
    """
    code, out, _ = run(["git", "log", f"{since}..HEAD", "--format=%H"])
    if code != 0:
        return CheckResult("scope-isolation", "SKIP", "git log failed")
    commits = [c for c in out.splitlines() if c.strip()]
    violations = []
    for commit in commits:
        _, files, _ = run(
            ["git", "show", "--name-only", "--format=", commit]
        )
        paths = [p for p in files.splitlines() if p.strip()]
        has_harness_skill = any(p.startswith("harness/skills/") for p in paths)
        has_plugin_skill = any(
            p.startswith(prefix)
            for prefix in [
                "flutter-toolkit/skills/",
                "design-kit/skills/",
                "backend-kit/skills/",
                "infra-kit/skills/",
                "rust-kit/skills/",
                "react-kit/skills/",
            ]
            for p in paths
        )
        if has_harness_skill and has_plugin_skill:
            violations.append(commit[:8])
    if violations:
        return CheckResult(
            "scope-isolation",
            "FAIL",
            f"{len(violations)} cross-phase commits",
            violations,
        )
    return CheckResult(
        "scope-isolation",
        "PASS",
        "no cross-phase commits",
    )


def check_bare_fence() -> CheckResult:
    # Delegate to validate-plugin V6 check output
    code, out, _ = run(["python3", "scripts/validate-plugin.py"])
    if "0 bare" in out:
        return CheckResult("bare-fence", "PASS", "V6 reports 0 bare fences")
    return CheckResult("bare-fence", "FAIL", "V6 detected bare fences")


# --- Runner --------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since",
        default="main",
        help="Validate based on changes since this git ref (default: main)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    args = parser.parse_args()

    since = args.since

    checks: list[Callable[[], CheckResult]] = [
        check_validate_plugin,
        check_sync_docs,
        check_sync_orchestrator,
        lambda: check_plugin_json_bumps(since),
        lambda: check_marketplace_sync(since),
        lambda: check_changelog_entry(since),
        check_research_log,
        check_per_kit_research_logs,
        lambda: check_docs_site_regen(since),
        check_cleanup_log,
        check_failure_count,
        check_evals_audit,
        lambda: check_scope_isolation(since),
        check_bare_fence,
    ]

    results = []
    for check in checks:
        try:
            r = check()
        except Exception as exc:
            r = CheckResult(
                getattr(check, "__name__", "unknown"),
                "FAIL",
                f"exception: {exc}",
            )
        results.append(r)
        status_emoji = {"PASS": "✓", "FAIL": "✗", "SKIP": "·"}[r.status]
        print(f"[ {r.status:4s} ] {status_emoji} {r.name}: {r.summary}")
        if r.status == "FAIL":
            hint = r.hint or FAIL_HINTS.get(r.name, "")
            if hint:
                print(f"           수정: {hint}")
        if args.verbose and r.evidence:
            for ev in r.evidence:
                print(f"           {ev}")

    n_pass = sum(1 for r in results if r.status == "PASS")
    n_fail = sum(1 for r in results if r.status == "FAIL")
    n_skip = sum(1 for r in results if r.status == "SKIP")
    print()
    print(f"Total: {n_pass} PASS / {n_fail} FAIL / {n_skip} SKIP")

    return 1 if n_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
