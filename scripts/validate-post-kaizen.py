#!/usr/bin/env python3
"""
validate-post-kaizen.py — Post-Kaizen Checklist 자동 검증 스크립트

카이젠 사이클 완료 후 PR 생성 전에 반드시 실행한다. 검사 항목 수는 요약 줄에 출력된다
(여기에 숫자를 박아두면 항목이 늘 때 조용히 틀린다 — 실측: 문서는 12 인데 실제는 14 였다).

## 상태와 종료 코드

`harness/evals/gate-exit-codes.md` 가 SSOT 다 (여기서 의미를 재정의하지 않는다).

- `PASS`  — 검사를 수행했고 위반 없음
- `FAIL`  — 검사를 수행했고 위반 발견 → exit 1
- `ERROR` — **검사를 수행하지 못했다** (git 실패 · 도구 부재 · 파싱 실패) → exit 2
- `SKIP`  — 해당 사항 없음 (이번 사이클에 플러그인 bump 가 없는 등). 종료 코드에 영향 없음

`ERROR` 는 2026-08-13 에 신설했다. 그전에는 `git_diff_names()` 가 실패 시 빈 목록을 돌려주어
diff 기반 검사 전부가 "변경 없음 → 위반 없음" 으로 **조용히 통과**했고, `check_scope_isolation`
은 `git log` 실패를 `SKIP` 으로 처리했는데 `SKIP` 은 종료 코드를 바꾸지 않았다.

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


class GateInfraError(RuntimeError):
    """검사를 **수행하지 못했다**. 위반 0 건과 구분해야 하는 상황 전용."""


@dataclass
class CheckResult:
    name: str
    status: str  # "PASS" | "FAIL" | "ERROR" | "SKIP"
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
    "doc-contracts": (
        "문서의 docs-contract 선언과 스크립트 실체를 맞춰라 "
        "(python3 scripts/validate-doc-contracts.py -v 로 불일치 확인 · 실체가 SSOT)"
    ),
}


def run(cmd: list[str], cwd: Path = REPO_ROOT) -> tuple[int, str, str]:
    """Run a command and return (code, stdout, stderr)."""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8"
    )
    return result.returncode, result.stdout, result.stderr


def git_diff_names(since: str) -> list[str]:
    """Return list of files changed since the given ref.

    ⚠ 실패 시 빈 목록을 돌려주지 않는다. 그렇게 하면 "diff 를 못 읽었다" 가 "변경이 없다" 로
    둔갑해 diff 기반 검사 전부가 조용히 통과한다 (2026-08-13 실측 결함).
    """
    code, out, err = run(["git", "diff", "--name-only", f"{since}..HEAD"])
    if code != 0:
        raise GateInfraError(f"git diff 실패 (rc={code}) — since={since}: {err.strip()}")
    return [line for line in out.splitlines() if line.strip()]


def plugin_skill_prefixes() -> list[str]:
    """marketplace.json 에서 harness 제외 킷의 `skills/` prefix 를 유도한다.

    하드코드하면 킷이 늘 때 조용히 커버리지가 빠진다 — 실측 2026-08-13: prefix 6 종만 박혀 있어
    planning-kit · reflect-kit · bambu-kit · onboarding-kit 4 종이 scope 격리 검사 밖에 있었다.
    """
    path = REPO_ROOT / ".claude-plugin/marketplace.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GateInfraError(f"marketplace.json 을 읽지 못했다: {exc}") from exc
    names = [
        p.get("name")
        for p in data.get("plugins", [])
        if p.get("name") and p.get("name") != "harness"
    ]
    if not names:
        raise GateInfraError("marketplace.json 에서 harness 제외 킷을 하나도 찾지 못했다")
    return [f"{n}/skills/" for n in names]


def today() -> str:
    return datetime.date.today().isoformat()


# --- Checks ---------------------------------------------------------------


def check_validate_plugin() -> CheckResult:
    code, out, err = run(["python3", "scripts/validate-plugin.py"])
    # plugin count is dynamic — match "Total: N plugins, N OK" pattern with N >= 7
    import re
    m = re.search(r"Total:\s+(\d+)\s+plugins,\s+(\d+)\s+OK", out)
    if code == 0 and m and m.group(1) == m.group(2) and int(m.group(1)) >= 7:
        n = m.group(1)
        return CheckResult(
            "validate-plugin",
            "PASS",
            f"{n} plugins, {n} OK",
            [f"Total: {n} plugins, {n} OK"],
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
    """Phase 간 소스 파일이 한 커밋에 섞이지 않았는지 본다.

    가벼운 검사다: 하나의 커밋이 `harness/skills/` 와 어떤 킷의 `skills/` 를 동시에 건드리면
    cross-phase 경계 위반으로 본다. 킷 목록은 marketplace.json 에서 유도한다 (하드코드 금지).
    """
    code, out, err = run(["git", "log", f"{since}..HEAD", "--format=%H"])
    if code != 0:
        raise GateInfraError(f"git log 실패 (rc={code}) — since={since}: {err.strip()}")
    prefixes = plugin_skill_prefixes()
    commits = [c for c in out.splitlines() if c.strip()]
    violations = []
    for commit in commits:
        rc, files, ferr = run(["git", "show", "--name-only", "--format=", commit])
        if rc != 0:
            raise GateInfraError(f"git show 실패 (rc={rc}) — {commit[:8]}: {ferr.strip()}")
        paths = [p for p in files.splitlines() if p.strip()]
        has_harness_skill = any(p.startswith("harness/skills/") for p in paths)
        has_plugin_skill = any(
            p.startswith(prefix) for prefix in prefixes for p in paths
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
        f"no cross-phase commits ({len(commits)} commits · {len(prefixes)} kits)",
    )


def check_bare_fence() -> CheckResult:
    # Delegate to validate-plugin V6 check output
    code, out, err = run(["python3", "scripts/validate-plugin.py"])
    if not out.strip():
        # 출력이 없으면 검사가 돌지 않은 것이다 — "bare fence 0 건" 이 아니다
        raise GateInfraError(
            f"validate-plugin.py 가 출력 없이 종료 (rc={code}): {err.strip()[:200]}"
        )
    if "0 bare" in out:
        return CheckResult("bare-fence", "PASS", "V6 reports 0 bare fences")
    return CheckResult("bare-fence", "FAIL", "V6 detected bare fences")


def check_doc_contracts() -> CheckResult:
    """문서의 docs-contract 선언과 스크립트 실체가 일치하는지 본다.

    exit 규약은 scripts/validate-doc-contracts.py 와 harness/evals/gate-exit-codes.md 를 따른다.
    """
    code, out, err = run(["python3", "scripts/validate-doc-contracts.py"])
    summary = (out.strip().splitlines() or ["(출력 없음)"])[-1]
    if code == 0:
        return CheckResult("doc-contracts", "PASS", summary)
    if code == 1:
        return CheckResult(
            "doc-contracts", "FAIL", summary, [ln for ln in out.splitlines() if ln.strip()]
        )
    if code == 3:
        return CheckResult("doc-contracts", "SKIP", "docs-contract 선언 블록 없음")
    raise GateInfraError(
        f"validate-doc-contracts.py 를 수행하지 못했다 (rc={code}): {err.strip()[:300]}"
    )


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

    # (표시 이름, 호출) 쌍으로 둔다 — lambda 를 그대로 넣으면 예외 시 이름이 `<lambda>` 로 찍혀
    # 어느 검사가 죽었는지 알 수 없다 (실측 2026-08-13).
    checks: list[tuple[str, Callable[[], CheckResult]]] = [
        ("validate-plugin", check_validate_plugin),
        ("sync-docs", check_sync_docs),
        ("sync-orchestrator", check_sync_orchestrator),
        ("plugin-json-bumps", lambda: check_plugin_json_bumps(since)),
        ("marketplace-sync", lambda: check_marketplace_sync(since)),
        ("changelog-entry", lambda: check_changelog_entry(since)),
        ("research-log", check_research_log),
        ("per-kit-research-logs", check_per_kit_research_logs),
        ("docs-site-regen", lambda: check_docs_site_regen(since)),
        ("cleanup-log", check_cleanup_log),
        ("failure-count", check_failure_count),
        ("evals-audit", check_evals_audit),
        ("scope-isolation", lambda: check_scope_isolation(since)),
        ("bare-fence", check_bare_fence),
        ("doc-contracts", check_doc_contracts),
    ]

    results = []
    for name, check in checks:
        try:
            r = check()
        except GateInfraError as exc:
            # 검사를 수행하지 못했다 — 위반 0 건이 아니다
            r = CheckResult(name, "ERROR", f"검사 수행 불가: {exc}")
        except Exception as exc:
            r = CheckResult(name, "FAIL", f"exception: {exc}")
        results.append(r)
        status_emoji = {"PASS": "✓", "FAIL": "✗", "ERROR": "!", "SKIP": "·"}[r.status]
        print(f"[ {r.status:5s} ] {status_emoji} {r.name}: {r.summary}")
        if r.status == "FAIL":
            hint = r.hint or FAIL_HINTS.get(r.name, "")
            if hint:
                print(f"            수정: {hint}")
        if args.verbose and r.evidence:
            for ev in r.evidence:
                print(f"            {ev}")

    n_pass = sum(1 for r in results if r.status == "PASS")
    n_fail = sum(1 for r in results if r.status == "FAIL")
    n_error = sum(1 for r in results if r.status == "ERROR")
    n_skip = sum(1 for r in results if r.status == "SKIP")
    print()
    print(
        f"Total: {len(results)} checks — "
        f"{n_pass} PASS / {n_fail} FAIL / {n_error} ERROR / {n_skip} SKIP"
    )

    # 종료 코드 의미는 harness/evals/gate-exit-codes.md 가 SSOT.
    # 불완전한 실행(ERROR)이 있으면 결과 집합을 완전한 분석으로 보고하지 않는다 → 2 가 우선.
    if n_error:
        print(
            "→ exit 2 (usage_or_infra_error): 일부 검사를 수행하지 못했다. "
            "FAIL 카운트를 완전한 결과로 읽지 마라.",
            file=sys.stderr,
        )
        return 2
    return 1 if n_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
