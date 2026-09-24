#!/usr/bin/env python3
"""collect-kaizen-data.py 의 /insights 입력 선택과 facets 집계를 임시 폴더에서 재현한다.

경우마다 `기대 / 실제` 한 줄을 찍고, 전부 맞으면 exit 0 · 하나라도 틀리면 exit 1.
기대값은 손으로 적었다 — 구현이 낸 값을 기대값으로 쓰면 틀린 구현도 통과한다.

사용법:
    python3 scripts/test-collect-kaizen-data.py
    python3 scripts/test-collect-kaizen-data.py --script <수집기 사본>   # 음성 대조
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NEWEST = "report-2026-09-24-095238.html"
OLDER = "report-2026-08-13-083357.html"
REPORT_HTML = "<html><body><p>Observed 2026-09-14 to 2026-09-23</p></body></html>"
TEMP_LABEL = "(임시 폴더 — 시험 세션)"


class Tally:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def check(self, case: str, expected: object, actual: object) -> None:
        ok = expected == actual
        if ok:
            self.passed += 1
        else:
            self.failed += 1
        print(f"{'PASS' if ok else 'FAIL'} {case} — 기대 {expected!r} / 실제 {actual!r}")


def load_collector(path: Path):
    spec = importlib.util.spec_from_file_location("collect_kaizen_data_under_test", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"수집기를 불러오지 못했다: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_usage_dir(path: Path) -> Path:
    path.mkdir(parents=True)
    for name in (OLDER, NEWEST, "report.html"):
        (path / name).write_text(REPORT_HTML, encoding="utf-8")
    return path


def write_summary(path: Path, frontmatter: str | None) -> Path:
    head = f"---\n{frontmatter}\n---\n\n" if frontmatter is not None else ""
    path.write_text(head + "# 요약\n\n## 마찰\n\n- 본문에는 관측 기간을 적지 않았다\n", encoding="utf-8")
    return path


def run_main_in_process(module, argv: list[str]) -> tuple[int, str]:
    """stderr 를 붙잡으려고 같은 프로세스에서 main 을 돈다. 후보 목록을 바꿔 끼울 수 있는 길이 이것뿐이다."""
    buffer = io.StringIO()
    saved = sys.argv
    sys.argv = ["collect-kaizen-data.py", *argv]
    try:
        with contextlib.redirect_stderr(buffer):
            code = module.main()
    finally:
        sys.argv = saved
    return code, buffer.getvalue()


def section_0b(pool: str) -> str:
    lines = pool.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("### 0-b")), None)
    end = next((i for i, line in enumerate(lines) if line.startswith("## 0.5")), len(lines))
    return "\n".join(lines[start:end]) if start is not None else ""


def selection_cases(module, root: Path, tally: Tally) -> None:
    usage = make_usage_dir(root / "usage-select")
    original = usage / "report.html"
    cases = [
        ("① report_file 이 가장 새 보고서", f"report_file: ~/.claude/usage-data/{NEWEST}", "요약본"),
        ("② report_file 이 옛 보고서 (generated 는 새 날짜)", f"generated: 2026-09-24\nreport_file: {OLDER}", "원본"),
        ("③ report_file 없음 · generated 가 보고서 날짜와 같다", "generated: 2026-09-24", "요약본"),
        ("③ report_file 없음 · generated 가 보고서 날짜보다 늦다", "generated: 2026-09-25", "요약본"),
        ("④ report_file 없음 · generated 가 더 이르다", "generated: 2026-09-01", "원본"),
        ("⑤ frontmatter 없음", None, "원본"),
    ]
    for index, (label, frontmatter, expected) in enumerate(cases):
        summary = write_summary(root / f"summary-{index}.md", frontmatter)
        chosen, _ = module.resolve_insights_path(None, [summary, original], usage)
        actual = "요약본" if chosen == summary else "원본" if chosen == original else str(chosen)
        tally.check(label, expected, actual)


def stderr_case(module, root: Path, tally: Tally) -> None:
    usage = make_usage_dir(root / "usage-stderr")
    summary = write_summary(root / "summary-stderr.md", f"generated: 2026-09-24\nreport_file: {OLDER}")
    saved = module.INSIGHTS_CANDIDATES
    module.INSIGHTS_CANDIDATES = (summary, usage / "report.html")
    try:
        code, err = run_main_in_process(
            module,
            ["--usage-data", str(usage), "--output", str(root / "pool-stderr.md"),
             "--skip-validate", "--hub-dir", str(root / "no-hub")],
        )
    finally:
        module.INSIGHTS_CANDIDATES = saved
    chosen = [line for line in err.splitlines() if "✓ 선택" in line]
    excluded = [line for line in err.splitlines() if "summary-stderr.md" in line and "✓ 선택" not in line]
    tally.check("② stderr ✓ 선택 줄이 원본 report.html", True,
                len(chosen) == 1 and chosen[0].rstrip().endswith("usage-stderr/report.html"))
    tally.check("② stderr 에 진 요약본 줄이 하나, 옛 보고서 이름을 이유로 든다", (1, True),
                (len(excluded), bool(excluded) and OLDER in excluded[0]))
    tally.check("② main exit", 0, code)


def missing_insights_case(script: Path, root: Path, tally: Tally) -> None:
    proc = subprocess.run(
        [sys.executable, str(script), "--insights", str(root / "없는-요약본.md"),
         "--output", str(root / "pool-missing.md"), "--skip-validate",
         "--hub-dir", str(root / "no-hub"), "--usage-data", str(root / "no-usage")],
        capture_output=True, text=True,
    )
    tally.check("⑥ --insights <없는 경로> exit", 2, proc.returncode)


def age_cases(module, root: Path, tally: Tally) -> None:
    usage = make_usage_dir(root / "usage-age")
    generated = datetime.date.today() - datetime.timedelta(days=42)
    summary = write_summary(root / "summary-age.md", f"generated: {generated.isoformat()}\nreport_file: {NEWEST}")
    now = time.time()
    os.utime(summary, (now, now))
    info = module.collect_insights_report(summary, usage)
    tally.check("⑦ 요약본 나이 — 수정 시각을 지금으로 바꿔도 generated 기준 (나이, VERY FRESH)",
                (42, False), (info["age_days"], info["very_fresh"]))
    tally.check("⑦ 요약본 본문에 없는 관측 기간은 report_file 원본에서 읽는다",
                ("2026-09-14", "2026-09-23"), info["period"])

    three_days_ago = now - 3 * 86400 - 60
    os.utime(usage / "report.html", (three_days_ago, three_days_ago))
    info = module.collect_insights_report(usage / "report.html", usage)
    tally.check("⑦ 원본 html 나이는 수정 시각 기준", 3, info["age_days"])


def git(cwd: Path, *args: str) -> None:
    # 사용자 전역 훅·서명 설정이 시험 커밋을 막지 않게 끈다.
    subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
         "-c", "user.name=test", "-c", "user.email=test@example.com", *args],
        cwd=cwd, check=True, capture_output=True, text=True,
    )


def write_session(usage: Path, session_id: str, project_path: str, facet: dict | None) -> None:
    meta = {"session_id": session_id, "project_path": project_path, "start_time": "2026-09-20T01:00:00Z"}
    (usage / "session-meta" / f"{session_id}.json").write_text(json.dumps(meta), encoding="utf-8")
    if facet is not None:
        payload = {**facet, "session_id": session_id}
        (usage / "facets" / f"{session_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )


def default_prefix_cases(module, tally: Tally) -> None:
    for path in ("/private/tmp/claude-1/scratchpad", "/tmp/x", "/var/folders/ab/T/x"):
        tally.check(f"기본 임시 폴더 판정 {path}", TEMP_LABEL, module.project_group(path))
    tally.check("git 이 못 여는 지운 워크트리는 레포 폴더 이름으로",
                "sample-app", module.project_group("/nonexistent-ckd/Hub/sample-app/.claude/worktrees/feature"))


def facets_cases(module, script: Path, root: Path, tally: Tally) -> None:
    repo = root / "sample-repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "commit", "-q", "--allow-empty", "-m", "init")
    worktree = root / "sample-worktree"
    git(repo, "worktree", "add", "-q", "-b", "wt", str(worktree))

    usage = root / "usage-facets"
    (usage / "facets").mkdir(parents=True)
    (usage / "session-meta").mkdir()
    fake_tmp = f"/private/tmp/ckd-fake-{uuid.uuid4().hex[:8]}"
    write_session(usage, "aaaaaaaa-0001", str(repo), {
        "underlying_goal": "harness 계약 조건 정리",
        "outcome": "mostly_achieved",
        "friction_counts": {"buggy_code": 2, "wrong_approach": 1},
        "friction_detail": "측정 명령을 두 번 고쳤다",
        "brief_summary": "본 레포 세션",
    })
    write_session(usage, "bbbbbbbb-0002", str(worktree), {
        "underlying_goal": "화면 간격 손질",
        "outcome": "partially_achieved",
        "friction_counts": {"buggy_code": 1, "misunderstood_request": 3},
        "friction_detail": "요청을 잘못 읽었다",
        "brief_summary": "워크트리 세션",
    })
    write_session(usage, "cccccccc-0003", f"{fake_tmp}/scratchpad/probe", {
        "underlying_goal": "평가 흉내",
        "outcome": "fully_achieved",
        "friction_counts": {"environment_issue": 1},
        "friction_detail": "도구가 없었다",
        "brief_summary": "임시 폴더 세션",
    })
    write_session(usage, "dddddddd-eval", str(repo), None)
    (usage / "facets" / "broken.json").write_text("{깨진", encoding="utf-8")
    summary = write_summary(root / "summary-facets.md", f"report_file: {NEWEST}")

    # 시험 저장소가 시스템 임시 폴더 안에 있어 기본 판정이면 전부 임시로 묶인다. 가짜 임시 경로만 임시로 본다.
    saved = module.TEMP_PATH_PREFIXES
    module.TEMP_PATH_PREFIXES = (fake_tmp,)
    pool_path = root / "pool-facets.md"
    try:
        code, err = run_main_in_process(
            module,
            ["--usage-data", str(usage), "--insights", str(summary), "--output", str(pool_path),
             "--skip-validate", "--hub-dir", str(root / "no-hub")],
        )
    finally:
        module.TEMP_PATH_PREFIXES = saved
    pool = pool_path.read_text(encoding="utf-8") if pool_path.is_file() else ""
    part = section_0b(pool)
    counts = "세션 3 · 프로젝트 묶음 1 · 임시 폴더 1 · 못 읽은 파일 1"
    lines = pool.splitlines()
    heads = [
        next((i for i, line in enumerate(lines) if line.startswith(prefix)), -1)
        for prefix in ("## 0. ", "### 0-b", "## 0.5")
    ]

    tally.check("ER-03 main exit", 0, code)
    tally.check("ER-03 stderr 집계 줄", True, counts in err)
    tally.check("ER-03 §0-b 집계 줄", True, counts in part)
    tally.check("ER-03 못 읽은 파일 이름이 stderr 와 §0-b 양쪽에", (True, True),
                ("broken.json" in err, "broken.json" in part))
    tally.check("ER-03 제목 순서 ## 0. < ### 0-b < ## 0.5", True, 0 <= heads[0] < heads[1] < heads[2])
    tally.check("ER-03 본 레포 + 워크트리 = 한 묶음 2 세션", True, "| sample-repo | 2 |" in part)
    tally.check("ER-03 임시 폴더 1 세션", True, f"| {TEMP_LABEL} | 1 |" in part)
    tally.check("ER-03 마찰 합계 — 종류별로 더한다", (True, True, True),
                ("buggy_code 3" in part, "misunderstood_request 3" in part, "environment_issue 1" in part))
    row_a = next((line for line in part.splitlines() if "`aaaaaaaa`" in line), "")
    row_b = next((line for line in part.splitlines() if "`bbbbbbbb`" in line), "")
    tally.check("ER-03 킷 이름이 목표에 글자 그대로 있으면 언급된 킷", True, "언급된 킷: harness" in row_a)
    tally.check("ER-03 킷 이름이 없으면 전 Phase 공통", True, "킷 언급 없음" in row_b)
    tally.check("ER-03 facets 없는 평가 세션은 세지 않는다", False, "dddddddd" in part)

    proc = subprocess.run(
        [sys.executable, str(script), "--usage-data", str(root / "usage-empty"),
         "--insights", str(summary), "--output", str(root / "pool-empty.md"),
         "--skip-validate", "--hub-dir", str(root / "no-hub")],
        capture_output=True, text=True,
    )
    empty_pool = (root / "pool-empty.md").read_text(encoding="utf-8") if (root / "pool-empty.md").is_file() else ""
    tally.check("ER-03 facets 폴더 없음 → exit 0 과 §0-b 의 (없음)", (0, True),
                (proc.returncode, "(없음)" in section_0b(empty_pool)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--script", type=Path, default=REPO_ROOT / "scripts" / "collect-kaizen-data.py",
                        help="시험할 수집기 경로 (음성 대조 때 사본을 준다)")
    args = parser.parse_args()
    script = args.script.resolve()
    module = load_collector(script)
    tally = Tally()
    with tempfile.TemporaryDirectory(prefix="ckd-test-") as tmp:
        root = Path(tmp)
        selection_cases(module, root, tally)
        stderr_case(module, root, tally)
        missing_insights_case(script, root, tally)
        age_cases(module, root, tally)
        default_prefix_cases(module, tally)
        facets_cases(module, script, root, tally)
    print(f"결과: {tally.passed} 통과 · {tally.failed} 실패")
    return 0 if tally.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
