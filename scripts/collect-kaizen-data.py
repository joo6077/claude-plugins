#!/usr/bin/env python3
"""카이젠 오케스트레이션용 데이터 풀 수집 스크립트.

수집 소스:
  1. 글로벌 feedback: ~/.harness/feedback/evaluator/*.yaml
     (레거시 project_name 은 명시 allowlist 로만 canonical 병합 — raw 분포도 함께 출력)
  2. Hub/10_Dev 내 .harness 보유 프로젝트(2단계 깊이)의 sprint-feedback + history
     plain `sprint-feedback.md` 와 접미형 `sprint-feedback-<slug>.md` 를 모두 수집
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

# `/insights` Claude Code CLI 슬래시 커맨드의 산출물 경로.
# 사용자가 `/insights` 를 실행하면 `~/.claude/usage-data/report.html` 가 생성된다.
INSIGHTS_PATH = Path.home() / ".claude" / "usage-data" / "report.html"
INSIGHTS_FRESH_DAYS = 60  # 60일 초과 시 stale 경고
INSIGHTS_VERY_FRESH_HOURS = 24  # 24시간 이내 = "방금 실행됨" 표시

# canonical 기준 = **writer 쪽 identity**.
#
# `harness/scripts/save-feedback.sh` 가 앞으로 쓰는 project_name 은 CONTRACT_ROOT 의
# **git root basename** 이다 (reflect-kit project-id 와 동일 규약). 집계 쪽이 이와 다른
# 방향으로 정규화하면 같은 프로젝트가 "앞으로 쌓이는 버킷" 과 "이미 쌓인 버킷" 으로 영구
# 분열한다. 그래서 이 allowlist 는 writer 가 산출할 이름으로 수렴시킨다.
#
# **명시 allowlist 전용이다. 이름 유사도/fuzzy 매칭을 도입하지 마라** —
# 다른 프로젝트를 잘못 합칠 위험이 있다. 새 항목을 추가할 때는 아래 세 근거 중
# 하나를 실측으로 확인하고 주석에 남긴다:
#   (a) 동일 project_hash 를 canonical 이름과 공유한다
#   (b) raw 이름이 canonical 이름을 리터럴 경로 성분으로 포함한다
#   (c) raw 이름의 project_hash 가 sha256(실재 경로)[:8] 로 역산되고, 그 경로의
#       git root basename 이 canonical 이름과 같다 (= writer 가 산출할 이름)
#
# 실측(2026-07-27, 글로벌 피드백 244건): project_hash 는 그 자체로 identity 가 아니다.
#   - ea3aeacd 하나가 fit-pal / fit-pal-app / fit-pal-server 3개 이름에 걸침
#   - claude-plugins 이름 하나에 해시 43종
# 따라서 병합은 "해시가 같으니 같은 프로젝트" 가 아니라 (c) 처럼 **해시를 실재 경로로
# 역산해 git root 를 확인**하거나 (a)/(b) 리터럴 근거가 있을 때만 한다.
PROJECT_NAME_ALIASES: dict[str, str] = {
    # (c) 실측 2026-07-28 — 세 이름의 해시가 전부 실재 경로로 역산되고, 그 경로들의
    #     git root 가 모두 `/Users/jackson/Hub/10_Dev/fit-pal` 하나다
    #     (app/ server/ 에 .git 없음 → `git rev-parse --show-toplevel` 이 fit-pal 반환):
    #       sha256("…/fit-pal")[:8]        = ea3aeacd  → raw "fit-pal"
    #       sha256("…/fit-pal/app")[:8]    = 19f8fc56  → raw "fit-pal-app", "fit-pal/app"
    #       sha256("…/fit-pal/server")[:8] = 9d23407f  → raw "fit-pal-server",
    #                                                     "fit-pal/server", "fitpal-server"
    #     즉 save-feedback.sh 는 이 셋 모두에 대해 "fit-pal" 을 쓴다. 여기서도 fit-pal 로
    #     모아야 신·구 데이터가 한 버킷에 남는다. 서브프로젝트 구분은 아래 canonical
    #     그룹 멤버 내역 + raw 분포로 그대로 보존된다 (병합이 원본을 감추지 않는다).
    "fit-pal/app": "fit-pal",
    "fit-pal-app": "fit-pal",
    "fit-pal/server": "fit-pal",
    "fit-pal-server": "fit-pal",
    "fitpal-server": "fit-pal",
    # (b) 자유 서술형 project_name 이나 "claude-plugins" 를 리터럴 접두로 포함
    "claude-plugins / react-kit phase10-research kaizen": "claude-plugins",
    # (b) bambu-kit 은 claude-plugins 레포 내부 플러그인이다 (별도 레포 없음 — 실측).
    "bambu-kit/bambu-print-profile": "claude-plugins",
    "bambu-kit/bambu-print-profile v0.4.1": "claude-plugins",
    "bambu-kit-v0.4.0-9mm-craft-knife": "claude-plugins",
    # 의도적 미포함: "fit-pal-flutter" — 해시(13d29f62)가 실재 경로로 역산되지 않고
    #   (`~/Hub/10_Dev/fit-pal-flutter` 부재 — 실측 2026-07-28), fit-pal 과 해시 공유도
    #   경로 성분 관계도 없다. 이름만 비슷해서 합치는 것은 금지된 fuzzy 매칭이다.
    #   raw 분포에 독립 그룹으로 그대로 남긴다.
}

# 결정론적 identity(save-feedback.sh 가 CONTRACT_ROOT 기준으로 계산) 도입 이후에만
# 존재하는 필드들. 하나라도 있으면 신형 세대로 분류한다.
DETERMINISTIC_IDENTITY_FIELDS = (
    "draft_project_name",
    "draft_project_hash",
    "sprint_slug",
    "contract_path",
)


def normalize_schema_version(raw: object) -> str:
    """schema_version 을 비교 가능한 문자열로 정규화한다.

    실측상 `1`(int) · `"1"` · `"1.0"` 세 표기가 섞여 있다. 셋 다 "1" 로 모은다.
    """
    if raw is None:
        return "(없음)"
    s = str(raw).strip()
    if not s:
        return "(없음)"
    # "1.0" → "1" (trailing zero-only 소수부 제거)
    if "." in s:
        head, _, tail = s.partition(".")
        if head.isdigit() and tail.strip("0") == "":
            return head
    return s


def canonical_project_name(raw: str) -> tuple[str, bool]:
    """raw project_name 을 canonical 이름으로 매핑한다.

    Returns: (canonical, alias 적용 여부). allowlist 에 없으면 raw 를 그대로 돌려준다.
    """
    canon = PROJECT_NAME_ALIASES.get(raw)
    if canon is None:
        return raw, False
    return canon, True


def feedback_generation(data: dict) -> str:
    """schema_version + 결정론적 identity 필드 유무로 피드백 세대를 구분한다."""
    sv = normalize_schema_version(data.get("schema_version"))
    if any(k in data for k in DETERMINISTIC_IDENTITY_FIELDS):
        return f"v{sv} · deterministic-identity"
    return f"v{sv} · legacy-identity"


def _extract_html_text(html: str) -> str:
    """HTML 에서 가독 텍스트만 추출. 표준 라이브러리만 사용 (BeautifulSoup 의존성 회피)."""
    import re as _re
    import html as _html
    txt = _re.sub(r"<script.*?</script>", "", html, flags=_re.S | _re.I)
    txt = _re.sub(r"<style.*?</style>", "", txt, flags=_re.S | _re.I)
    txt = _re.sub(r"<(br|/?p|/?div|/?li|/?h[1-6]|/?tr)[^>]*>", "\n", txt, flags=_re.I)
    txt = _re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(txt)
    txt = _re.sub(r"[ \t]+", " ", txt)
    txt = _re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


def collect_insights_report() -> dict | None:
    """`/insights` 산출물(report.html)을 로드한다.

    파일이 없으면 None 반환. 있으면 경로/mtime/content 를 dict 로 반환한다.
    카이젠 오케스트레이터 Step 0 에서 데이터 풀에 §0 (최상위) 으로 삽입된다.
    """
    path = INSIGHTS_PATH
    if not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return None
    content = _extract_html_text(raw)
    mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
    age_seconds = (datetime.datetime.now() - mtime).total_seconds()
    age_days = age_seconds / 86400
    very_fresh = age_seconds < INSIGHTS_VERY_FRESH_HOURS * 3600
    return {
        "path": path,
        "mtime": mtime.isoformat(timespec="seconds"),
        "age_days": int(age_days),
        "age_hours": round(age_seconds / 3600, 1),
        "very_fresh": very_fresh,
        "stale": age_days > INSIGHTS_FRESH_DAYS,
        "content": content,
        "format": "html-extracted",
    }


def collect_global_feedback() -> dict:
    """글로벌 evaluator 피드백 통계와 샘플을 수집한다."""
    result = {
        "total": 0,
        "parse_failed": 0,
        "by_verdict": Counter(),
        "by_skill": Counter(),
        "by_project": Counter(),  # canonical (allowlist 병합 후)
        "by_project_raw": Counter(),  # 원본 project_name (병합 전)
        "canonical_members": defaultdict(Counter),  # canonical -> raw -> count
        "by_schema_version": Counter(),  # 정규화된 schema_version
        "by_schema_version_raw": Counter(),  # 원본 표기
        "by_generation": Counter(),
        "alias_hits": Counter(),  # 실제로 적용된 allowlist 항목
        # save-feedback.sh 가 contract_path 를 추측한 건수 (true/false/미보유).
        # 추론 귀속이 조용히 누적되면 피드백이 stale 계약에 붙는다 — 표면화한다.
        "contract_path_inferred": Counter(),
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
            result["parse_failed"] += 1
            continue
        if not isinstance(data, dict):
            result["parse_failed"] += 1
            continue

        ev = data.get("evaluation", {}) or {}
        verdict = ev.get("verdict", "UNKNOWN")
        result["by_verdict"][verdict] += 1
        result["by_skill"][data.get("skill", "unknown")] += 1

        raw_name = str(data.get("project_name", "unknown"))
        canon_name, aliased = canonical_project_name(raw_name)
        result["by_project"][canon_name] += 1
        result["by_project_raw"][raw_name] += 1
        result["canonical_members"][canon_name][raw_name] += 1
        if aliased:
            result["alias_hits"][raw_name] += 1

        if "contract_path" in data:
            inferred = data.get("contract_path_inferred")
            result["contract_path_inferred"][
                "inferred(추측)" if inferred is True
                else "explicit(명시)" if inferred is False
                else "unknown(필드 없음 — 구버전)"
            ] += 1

        result["by_schema_version"][normalize_schema_version(data.get("schema_version"))] += 1
        result["by_schema_version_raw"][repr(data.get("schema_version"))] += 1
        result["by_generation"][feedback_generation(data)] += 1

        ts = str(data.get("timestamp", ""))[:10]
        # 샘플은 원본 이름을 그대로 보존한다 (병합으로 출처를 감추지 않는다).
        project = raw_name

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


FEEDBACK_DETAIL_LIMIT = 5  # details 블록으로 본문을 실어줄 최대 파일 수 (mtime 최신순)


def collect_sprint_feedback(harness_dir: Path) -> list[dict]:
    """`.harness` 안의 sprint-feedback 파일들을 수집한다.

    병렬 스프린트 규약(SSOT §1)상 계약/피드백은 접미형이다:
      - plain  : sprint-feedback.md          (슬러그 없는 스프린트 — 계속 유효)
      - 접미형 : sprint-feedback-<slug>.md   (슬러그별 병렬 스프린트)
    둘 다 수집한다. plain 을 먼저, 접미형은 mtime 최신순으로 이어붙인다.
    """
    found: list[dict] = []
    if not harness_dir.is_dir():
        return found

    plain = harness_dir / "sprint-feedback.md"
    suffixed = sorted(
        (p for p in harness_dir.glob("sprint-feedback-*.md") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    ordered = ([plain] if plain.is_file() else []) + suffixed

    for path in ordered:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        slug = path.stem[len("sprint-feedback-"):] if path.name != "sprint-feedback.md" else None
        found.append(
            {
                "file": path.name,
                "slug": slug,
                "lines": len(lines),
                "head": "\n".join(lines[:20]),
                "mtime": datetime.datetime.fromtimestamp(path.stat().st_mtime).isoformat(
                    timespec="seconds"
                ),
            }
        )
    return found


def collect_hub_projects(hub_dir: Path) -> list[dict]:
    """Hub/10_Dev 내 .harness 디렉토리 보유 프로젝트 정보를 수집한다.

    중첩 배포본(`fit-pal/app`, `fit-pal/server` 등)도 독립 CONTRACT_ROOT 이므로
    2단계 깊이까지 스캔한다 (SSOT §CONTRACT_ROOT 해석 v5.2).

    판정 기준은 `.harness/` 디렉토리 존재 자체다 — `project.yaml` 유무가 아니다.
    `project.yaml` 이 없는 배포본(실측: purchase-bot · flutter_playwright ·
    apps/apps/app_kiosk)도 계약·피드백을 갖고 있으므로 제외하면 집계에서 통째로 누락된다.
    """
    projects: list[dict] = []
    if not hub_dir.exists():
        return projects

    seen: set[Path] = set()
    candidates = sorted(set(hub_dir.glob("*/.harness")) | set(hub_dir.glob("*/*/.harness")))
    for harness_dir in candidates:
        if not harness_dir.is_dir():
            continue
        project_path = harness_dir.parent
        resolved = project_path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved == REPO_ROOT.resolve() or project_path.name == REPO_ROOT.name:
            continue  # 현재 레포 자신은 별도 처리

        try:
            name = str(project_path.relative_to(hub_dir))
        except ValueError:
            name = project_path.name

        entry = {"name": name, "path": str(project_path)}

        feedbacks = collect_sprint_feedback(harness_dir)
        entry["feedback_files"] = feedbacks
        entry["feedback_count"] = len(feedbacks)
        entry["feedback_slugs"] = [f["slug"] for f in feedbacks if f["slug"]]
        entry["sprint_feedback_lines"] = sum(f["lines"] for f in feedbacks)

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
        try:
            rel = insights["path"].relative_to(REPO_ROOT)
        except ValueError:
            rel = insights["path"]
        if insights["stale"]:
            fresh_marker = " ⚠ STALE (60일 초과)"
        elif insights["very_fresh"]:
            fresh_marker = f" ✓ VERY FRESH ({insights['age_hours']}시간 전)"
        else:
            fresh_marker = f" ({insights['age_days']}일 전)"
        fmt_note = " · HTML 추출 텍스트" if insights["format"] == "html-extracted" else " · Markdown 추출본"
        lines += [
            "## 0. `/insights` Report (외부 도구 산출물)",
            "",
            f"- 경로: `{rel}`{fmt_note}",
            f"- 최근 갱신: {insights['mtime']}{fresh_marker}",
            "- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)",
            "",
            "<details><summary>insights report 본문 (auto-extracted)</summary>",
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
            f"- (없음) `{INSIGHTS_PATH}` 미존재",
            "- 사용자가 Claude Code CLI 에서 `/insights` 를 실행하면 자동 생성된다.",
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
        "### Project 분포 (canonical — allowlist 병합 후)",
        "",
        "canonical 기준은 **writer 쪽 identity** 다 — `harness/scripts/save-feedback.sh` 가 "
        "CONTRACT_ROOT 의 git root basename 으로 계산하는 이름. 집계가 다른 방향으로 정규화하면 "
        "같은 프로젝트가 신·구 버킷으로 영구 분열하므로 writer 에 맞춘다 "
        "(예: `fit-pal/app`·`fit-pal/server` 는 .git 이 없어 git root 가 `fit-pal` 하나다).",
        "",
        "병합은 `PROJECT_NAME_ALIASES` **명시 allowlist** 로만 한다. 이름 유사도/fuzzy 매칭은 "
        "쓰지 않는다. 병합된 그룹은 서브프로젝트 구분이 사라지지 않도록 원본 이름 내역을 "
        "`←` 뒤에 함께 보여준다.",
        "",
    ]
    members_map = global_fb.get("canonical_members", {})
    for p, c in global_fb["by_project"].most_common():
        members = members_map.get(p, Counter())
        if len(members) > 1:
            detail = ", ".join(f"`{m}` {n}" for m, n in members.most_common())
            lines.append(f"- `{p}`: {c}  ← {detail}")
        else:
            lines.append(f"- `{p}`: {c}")

    lines += [
        "",
        "### Project 분포 (raw `project_name` — 병합 전 원본)",
        "",
        "병합이 원본을 감추지 않도록 그대로 남긴다. "
        "canonical 과 raw 개수가 다르면 그 차이가 곧 레거시 표기 흔들림의 규모다.",
        "",
    ]
    for p, c in global_fb["by_project_raw"].most_common():
        alias_of, aliased = canonical_project_name(p)
        suffix = f"  → merged into `{alias_of}`" if aliased else ""
        lines.append(f"- `{p}`: {c}{suffix}")

    raw_names = len(global_fb["by_project_raw"])
    canon_names = len(global_fb["by_project"])
    lines += [
        "",
        f"- raw 이름 종류: **{raw_names}** → canonical 그룹: **{canon_names}** "
        f"(allowlist 적용 파일 {sum(global_fb['alias_hits'].values())}건)",
    ]
    unused_aliases = [k for k in PROJECT_NAME_ALIASES if k not in global_fb["by_project_raw"]]
    if unused_aliases:
        lines.append(
            "- ⚠ 미적중 allowlist 항목 (데이터에 없음 — 정리 후보): "
            + ", ".join(f"`{k}`" for k in unused_aliases)
        )

    lines += [
        "",
        "### schema_version / 세대 분포",
        "",
        "`schema_version` 과 결정론적 identity 필드"
        f"({', '.join('`' + f + '`' for f in DETERMINISTIC_IDENTITY_FIELDS)}) 유무로 신·구 피드백을 구분한다. "
        "`legacy-identity` 는 `project_name`/`project_hash` 가 cwd 기준으로 계산되던 시기의 기록이라 "
        "위 raw 분포의 표기 흔들림 원인이 된다.",
        "",
    ]
    for sv, c in global_fb["by_schema_version"].most_common():
        lines.append(f"- schema_version `{sv}`: {c}")
    raw_sv = global_fb.get("by_schema_version_raw", Counter())
    if len(raw_sv) > 1:
        lines.append(
            "  - 정규화 전 원본 표기: "
            + ", ".join(f"`{sv}` {c}" for sv, c in raw_sv.most_common())
        )
    lines.append("")
    for gen, c in global_fb["by_generation"].most_common():
        lines.append(f"- {gen}: {c}")

    cpi = global_fb.get("contract_path_inferred", Counter())
    if cpi:
        lines += [
            "",
            "#### `contract_path` 귀속 근거",
            "",
            "`save-feedback.sh` 는 `HARNESS_CONTRACT` / draft 값이 없으면 계약 경로를 **추측**하고 "
            "`contract_path_inferred: true` 를 남긴다. `inferred` 비율이 높으면 피드백이 stale 한 "
            "plain 계약에 오귀속되고 있을 수 있다.",
            "",
        ]
        for kind, c in cpi.most_common():
            lines.append(f"- {kind}: {c}")

    if global_fb.get("parse_failed"):
        lines.append(f"- ⚠ 파싱 실패(집계 제외): {global_fb['parse_failed']}")

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
    total_feedback_files = sum(p.get("feedback_count", 0) for p in hub_projects)
    total_slugged = sum(len(p.get("feedback_slugs", [])) for p in hub_projects)
    lines += [
        f"- 수집된 sprint-feedback 파일: **{total_feedback_files}** "
        f"(그중 접미형 `sprint-feedback-<slug>.md`: **{total_slugged}**)",
        "",
    ]
    for proj in hub_projects:
        feedbacks = proj.get("feedback_files", [])
        lines += [
            f"### `{proj['name']}`",
            "",
            f"- 경로: `{proj['path']}`",
            f"- sprint-feedback 파일: {len(feedbacks)}개 "
            f"(총 {proj.get('sprint_feedback_lines', 0)} lines)",
            f"- history sprint-contracts: {proj.get('history_count', 0)}",
        ]
        if proj.get("feedback_slugs"):
            lines.append("- 접미형 슬러그: " + ", ".join(f"`{s}`" for s in proj["feedback_slugs"]))
        if proj.get("recent_contracts"):
            lines.append("- 최근 contracts:")
            for c in proj["recent_contracts"]:
                lines.append(f"  - {c}")
        if feedbacks:
            lines.append("- 파일별 내역:")
            for fb in feedbacks:
                tag = f"slug=`{fb['slug']}`" if fb["slug"] else "plain (슬러그 없음)"
                lines.append(f"  - `{fb['file']}` — {tag}, {fb['lines']} lines, mtime {fb['mtime']}")
        for fb in feedbacks[:FEEDBACK_DETAIL_LIMIT]:
            if not fb["head"].strip():
                continue
            lines += [
                "",
                f"<details><summary>{fb['file']} 앞부분</summary>",
                "",
                "```markdown",
                fb["head"],
                "```",
                "",
                "</details>",
            ]
        if len(feedbacks) > FEEDBACK_DETAIL_LIMIT:
            lines.append(
                f"- (본문 미리보기는 최신 {FEEDBACK_DETAIL_LIMIT}개만 표시 — "
                f"나머지 {len(feedbacks) - FEEDBACK_DETAIL_LIMIT}개는 위 파일별 내역 참조)"
            )
        lines.append("")

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
        if insights["stale"]:
            marker = " ⚠ STALE"
        elif insights["very_fresh"]:
            marker = f" ✓ VERY FRESH ({insights['age_hours']}h ago)"
        else:
            marker = f" ({insights['age_days']}d ago)"
        print(
            f"  - /insights 산출물: {insights['path']}{marker} · format={insights['format']}",
            file=sys.stderr,
        )
    else:
        print(f"  - /insights 산출물: 없음 ({INSIGHTS_PATH} 미존재)", file=sys.stderr)
    print(
        f"  - global feedback: {global_fb['total']}개",
        f"(REJECT {global_fb['by_verdict'].get('REJECT', 0)}, "
        f"APPROVE {global_fb['by_verdict'].get('APPROVE', 0)})",
        file=sys.stderr,
    )
    print(
        f"  - project_name: raw {len(global_fb['by_project_raw'])}종"
        f" → canonical {len(global_fb['by_project'])}종"
        f" (allowlist 적용 {sum(global_fb['alias_hits'].values())}건)",
        file=sys.stderr,
    )
    fb_total = sum(p.get("feedback_count", 0) for p in hub_projects)
    fb_slugged = sum(len(p.get("feedback_slugs", [])) for p in hub_projects)
    print(
        f"  - hub projects: {len(hub_projects)}개"
        f" · sprint-feedback {fb_total}개 (접미형 {fb_slugged}개)",
        file=sys.stderr,
    )
    print(f"  - followups: {len(followups)}개", file=sys.stderr)
    print(f"  - local contracts: {len(local_contracts)}개", file=sys.stderr)


if __name__ == "__main__":
    main()
