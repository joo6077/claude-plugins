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
  6. ~/.claude/projects/*/memory/*.md 의 `metadata.type: feedback` 엔트리
     (전 프로젝트 교차 · 관련성·중요도 2 축 선별 → 데이터 풀 §0.5. 읽기 전용)

출력:
  .harness/.meta/kaizen-data-pool.md (기본)
  또는 --output <path> 로 다른 경로 지정

Usage:
  python3 scripts/collect-kaizen-data.py
  python3 scripts/collect-kaizen-data.py --output /tmp/kaizen-data.md
  python3 scripts/collect-kaizen-data.py --hub-dir ~/Hub/10_Dev
  python3 scripts/collect-kaizen-data.py --insights .claude/kaizen-input/insights-report.md

문서-스크립트 계약:
  이 스크립트의 인터페이스(옵션 집합 · /insights 입력 후보 · 종료 코드)는
  .claude/skills/kaizen-orchestrator/SKILL.md 의 `docs-contract` 블록에 선언돼 있고
  scripts/validate-doc-contracts.py 가 argparse 실체와 대조한다.
  선언과 실체 중 **실체가 SSOT** 다 — 옵션을 바꾸면 문서 블록도 같이 고쳐야 검사를 통과한다.
"""
from __future__ import annotations

import argparse
import datetime
import re
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

# `/insights` 산출물 입력 후보 — **우선순위 순서**다.
#
# 1) 레포 안의 사람이 정리한 델타 분석본 (`.claude/kaizen-input/insights-report.md`)
# 2) 홈의 같은 이름 (여러 레포가 공유할 때)
# 3) `/insights` 원본 산출물 (`~/.claude/usage-data/report.html`)
#
# 2026-08-13 이전에는 3) 하나만 봤다. 그런데 오케스트레이터 SKILL.md Step 0 은 1)·2) 자동
# 탐색과 `--insights=PATH` 를 이미 주장하고 있었다 — 문서가 없는 인터페이스를 약속한 상태였고,
# 그 결과 **사람이 정리한 §0 델타 분석본이 데이터 풀에 들어가지 못했다.**
# 하위호환: 1)·2) 가 없으면 종전대로 3) 을 쓰고, 셋 다 없으면 §0 에 "(없음)" 을 쓰고 진행한다.
INSIGHTS_CANDIDATES: tuple[Path, ...] = (
    REPO_ROOT / ".claude" / "kaizen-input" / "insights-report.md",
    Path.home() / ".claude" / "kaizen-input" / "insights-report.md",
    Path.home() / ".claude" / "usage-data" / "report.html",
)
# 하위호환 별칭 — 기존 코드/문서가 참조하던 이름. 후보 3 번과 같은 값이다.
INSIGHTS_PATH = INSIGHTS_CANDIDATES[-1]
INSIGHTS_FRESH_DAYS = 60  # 60일 초과 시 stale 경고
INSIGHTS_VERY_FRESH_HOURS = 24  # 24시간 이내 = "방금 실행됨" 표시

# 종료 코드 — harness/evals/gate-exit-codes.md 가 SSOT 다 (여기서 의미를 재정의하지 않는다).
DOC_CONTRACT_EXIT_CODES: tuple[int, ...] = (0, 2)


def display_path(path: Path) -> str:
    """머신 독립적인 표기로 접는다 — 레포 상대경로 우선, 그다음 `~` 상대경로.

    레포를 어디에 클론했든 같은 문자열이 나와야 `docs-contract` 선언과 대조할 수 있다.
    """
    resolved = Path(path)
    for base, prefix in ((REPO_ROOT.resolve(), ""), (Path.home(), "~/")):
        try:
            return prefix + str(resolved.resolve().relative_to(base))
        except ValueError:
            continue
    return str(resolved)


def doc_contract() -> dict:
    """문서가 선언한 인터페이스와 대조할 **실체** 를 돌려준다.

    scripts/validate-doc-contracts.py 가 이 함수를 호출한다. 값은 전부 살아 있는 객체에서
    유도한다 — 여기에 리터럴을 손으로 적으면 drift 검사가 자기 자신을 속이게 된다.
    """
    parser = build_arg_parser()
    options: list[str] = []
    for action in parser._actions:  # noqa: SLF001 — argparse 의 공식 introspection 경로다
        for opt in action.option_strings:
            if opt in ("-h", "--help"):
                continue
            options.append(opt)
    return {
        "script": display_path(Path(__file__)),
        "options": sorted(options),
        "input_candidates": [display_path(p) for p in INSIGHTS_CANDIDATES],
        "exit_codes": sorted(DOC_CONTRACT_EXIT_CODES),
    }

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


def resolve_insights_path(explicit: Path | None = None) -> tuple[Path | None, list[str]]:
    """`/insights` 입력 파일을 우선순위대로 고른다.

    반환: (선택된 경로 또는 None, 후보별 상태 문자열 목록).
    상태 문자열은 stderr 에 그대로 찍어 "무엇을 봤고 무엇을 골랐는지" 를 남긴다 —
    조용히 고르면 이번 D1 같은 drift 를 다시 발견하지 못한다.
    """
    trace: list[str] = []
    chosen: Path | None = None

    if explicit is not None:
        exists = explicit.is_file()
        trace.append(f"{'✓ 선택' if exists else '✗ 없음'}  --insights  {explicit}")
        if not exists:
            trace.append("  ⚠ --insights 로 지정한 경로가 없다 — 자동 탐색으로 넘어가지 않는다")
            return None, trace
        return explicit, trace

    for cand in INSIGHTS_CANDIDATES:
        if chosen is None and cand.is_file():
            chosen = cand
            trace.append(f"✓ 선택  {display_path(cand)}")
        elif cand.is_file():
            trace.append(f"· 후순위 {display_path(cand)} (존재하지만 우선순위 낮음)")
        else:
            trace.append(f"✗ 없음  {display_path(cand)}")
    return chosen, trace


def collect_insights_report(path: Path | None) -> dict | None:
    """`/insights` 산출물을 로드한다.

    경로가 None 이거나 읽을 수 없으면 None 반환. 있으면 경로/mtime/content 를 dict 로 반환한다.
    카이젠 오케스트레이터 Step 0 에서 데이터 풀에 §0 (최상위) 으로 삽입된다.
    `.md` 는 그대로, `.html` 은 태그를 벗겨서 싣는다.
    """
    if path is None or not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"WARNING: /insights 후보를 읽지 못했다 — {path}: {exc}", file=sys.stderr)
        return None
    is_html = path.suffix.lower() in (".html", ".htm")
    content = _extract_html_text(raw) if is_html else raw
    fmt = "html-extracted" if is_html else "markdown"
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
        "format": fmt,
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


# ---------------------------------------------------------------------------
# §0.5 프로젝트 메모리 (`feedback` 타입) — 전 프로젝트 교차 수집
# ---------------------------------------------------------------------------
#
# 소스: `~/.claude/projects/<encoded>/memory/*.md` (`MEMORY.md` 는 색인이라 제외)
# 대상: `metadata.type == feedback` 만. 다른 타입(`project_*` 등)은 세션 진행 상태 메모라
#       카이젠 Phase 가 규칙 근거로 삼을 대상이 아니다.
#
# **선별 축은 관련성 · 중요도 2 축이다. 시간 축(recency)은 쓰지 않는다.**
# 프론트매터의 갱신 시각 필드가 실측 104 건 중 44 건에만 있어(2026-08-14) 나머지 60 건이
# 임의 판정된다. 파일시스템 타임스탬프를 대용으로 쓰는 것도 금지다 — grounding 소급 태깅처럼
# 전건을 한 번에 건드리는 작업이 있으면 모든 파일이 같은 값이 되어 축이 통째로 무의미해진다.
# §1·§2 가 쓰는 시간 정렬 코드를 이 블록으로 가져오지 마라.
MEMORY_ROOT = Path.home() / ".claude" / "projects"
MEMORY_INDEX_FILENAME = "MEMORY.md"

# reflect-kit 승격 ledger 위치. **읽기 전용이다** — 카이젠은 여기에 쓰지 않는다.
# 병렬 쓰기 경로가 생기면 ledger 가 두 갈래로 갈라져 rollback 이 깨진다
# (reflect-promote 가 rule_id · status 전환의 단독 소유자다).
# 없을 수 있다 — 없으면 재발 가중치 0 으로 진행하고 죽지 않는다.
REFLECT_LOGS_ROOT = Path.home() / ".claude" / "logs"
PROMOTION_LEDGER_FILENAME = "promotions-ledger.md"

# grounding 4 값. **의미 정의의 SSOT 는 reflect-kit/references/memory-grounding.md 다** —
# 여기서 각 값이 무엇을 뜻하는지 서술하지 않는다. 이 목록은 ER-02(4 값 밖 제외)를 검증하기
# 위해 값 자체만 소비하는 인용이다. 의미가 궁금하면 SSOT 를 읽어라.
GROUNDING_VALUES: tuple[str, ...] = (
    "user_correction",
    "execution_evidence",
    "mixed",
    "self_inference",
)
GROUNDING_UNTAGGED = "미분류"  # 필드 자체가 아직 없는 파일 (소급 태깅 진행 중이라 정상)

# 외부 검증이 없는 등급 — 주입은 하되 **계약 조건의 PASS 근거로 쓰지 못한다**.
GROUNDING_UNVERIFIED: tuple[str, ...] = ("self_inference", GROUNDING_UNTAGGED)

# 중요도 가중 (hypothesis — 학습된 값이 아니다. Generative Agents 도 수기 튜닝이었다).
GROUNDING_WEIGHT: dict[str, int] = {
    "user_correction": 3,
    "execution_evidence": 3,
    "mixed": 3,
    "self_inference": 0,
    GROUNDING_UNTAGGED: 1,
}

# 관련성 축 — 데이터 풀은 Phase 별로 쪼개지지 않으므로 §0.5 안에서 도메인 그룹으로 나눠
# 각 Phase 가 자기 것을 찾게 한다. 키워드가 ASCII 토큰이면 단어 경계로, 한글이면
# 부분 문자열로 맞춘다 ("ui" 가 "guide" 에 걸리는 식의 오탐 방지).
MEMORY_DOMAIN_GROUPS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("harness", "harness · 계약 · QA (Phase 2·3·4)", (
        "계약", "contract", "sprint", "스프린트", "qa", "evaluator", "평가", "판정",
        "approve", "reject", "oracle", "조건", "amendment", "측정", "harness", "검증",
    )),
    ("flutter", "flutter-toolkit (Phase 5)", (
        "flutter", "dart", "widget", "위젯", "riverpod", "hookwidget", "usestate",
        "usememoized", "useeffect", "freezed", "build_runner", "fvm", "melos",
        "listview", "safearea", "bottomsheet", "custompaint", "shrinkwrap",
        "pubspec", "sliver", "provider",
    )),
    ("design", "design-kit (Phase 6)", (
        "디자인", "design", "시안", "레이아웃", "layout", "아이콘", "icon", "패딩",
        "padding", "radius", "테마", "theme", "컬러", "color", "무드", "타이포",
        "ui", "ux", "토큰", "token", "시각",
    )),
    ("backend", "backend-kit (Phase 7)", (
        "백엔드", "backend", "서버", "server", "api", "엔드포인트", "endpoint",
        "serde", "worker", "트랜잭션", "n+1", "db", "sql", "쿼리", "마이그레이션",
    )),
    ("infra", "infra-kit · 훅 (Phase 8)", (
        "인프라", "infra", "ci", "docker", "배포", "deploy", "fastlane", "훅", "hook",
        "pretooluse", "posttooluse", "sessionstart", "시크릿", "secret", "env",
        "파이프라인", "actions",
    )),
    ("rust", "rust-kit (Phase 9)", (
        "rust", "cargo", "clippy", "axum", "sqlx", "tonic",
    )),
    ("react", "react-kit (Phase 10)", (
        "react", "tauri", "wasm", "vite", "typescript", "tsx", "zustand", "tanstack",
    )),
    ("planning", "planning-kit (Phase 11)", (
        "기획", "planning", "prd", "브레인스토밍", "brainstorm", "우선순위", "요구사항",
    )),
    ("reflect", "reflect-kit · 메모리 (Phase 12)", (
        "메모리", "memory", "reflect", "승격", "promotion", "digest", "ledger",
        "grounding", "학습",
    )),
    ("research", "리서치 위임 · codex", (
        "codex", "리서치", "research", "websearch", "webfetch", "context7", "위임",
    )),
    ("bambu", "bambu-kit · 3D 프린트", (
        "bambu", "3d", "프린트", "seam", "filament", "ironing", "makerworld",
        "slicer", "cad", "노즐",
    )),
    ("onboarding", "onboarding-kit · 셋업 가이드", (
        "셋업", "setup", "온보딩", "onboarding", "콘솔", "console", "firebase",
        "gcp", "aws", "oauth", "app store connect", "용어",
    )),
    ("tooling", "구동 검증 · MCP 도구", (
        "mcp", "playwright", "screenshot", "hot reload", "hot restart", "시뮬레이터",
        "e2e", "실기",
    )),
)
MEMORY_FALLBACK_GROUP = ("general", "공통 · 작업 절차 (도메인 키워드 미검출)")

# 주입량 (hypothesis). 그룹별 상위 N 을 본문까지 싣고, 나머지는 제목만 남긴다 —
# 전량 주입은 엔트리가 늘수록 신호를 희석하고, 전량 배제는 결정적 항목을 놓친다.
MEMORY_INJECT_PER_GROUP = 3
MEMORY_INJECT_CAP = 40
MEMORY_BODY_LINES = 18
MEMORY_DESC_CHARS = 160

_MEMORY_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---[ \t]*\n?", re.S)
# SC-01 의 독립 계산 oracle(`grep -q '^  type: feedback'`)과 **같은 판정**을 쓴다.
# 프론트매터 YAML 파싱이 깨져도 집계 모수가 흔들리지 않아야 N + M 산술이 성립한다.
_MEMORY_FEEDBACK_RE = re.compile(r"^  type: feedback", re.M)
_MEMORY_ATX_RE = re.compile(r"^(#{1,6})[ \t]+(.*)$")
_MEMORY_SCALAR_RE = re.compile(r"^[ \t]*([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*?)[ \t]*$")
# 재발 신호 — 본문이 스스로 "몇 번 반복됐는지" 를 말하는 경우가 많다 (ledger 가 없어도 잡힌다).
_MEMORY_REPEAT_COUNT_RE = re.compile(r"(\d+)\s*(?:회|연속|번째)")
MEMORY_REPEAT_MARKERS: tuple[str, ...] = (
    "재발", "반복", "매번", "연속", "또 ", "다시 ", "again", "repeated", "recurring",
)


def _memory_keyword_matcher(keyword: str):
    """키워드 1 개에 대한 매칭 함수를 만든다 (ASCII 는 단어 경계, 그 외는 부분 문자열)."""
    if re.fullmatch(r"[a-z0-9_+. ]+", keyword):
        pattern = re.compile(r"(?<![a-z0-9_])" + re.escape(keyword) + r"(?![a-z0-9_])")
        return pattern.search
    return lambda haystack, kw=keyword: kw in haystack


_MEMORY_GROUP_MATCHERS = tuple(
    (gid, label, tuple(_memory_keyword_matcher(k) for k in kws))
    for gid, label, kws in MEMORY_DOMAIN_GROUPS
)
MEMORY_GROUP_LABELS: dict[str, str] = {
    gid: label for gid, label, _ in MEMORY_DOMAIN_GROUPS
}
MEMORY_GROUP_LABELS[MEMORY_FALLBACK_GROUP[0]] = MEMORY_FALLBACK_GROUP[1]


def _memory_flat_fields(front: object) -> dict:
    """프론트매터를 평평한 lookup 으로 접는다 (`metadata:` 중첩을 최상위로 올린다).

    최상위 스칼라가 우선이고, 중첩 값은 비어 있는 키만 채운다.
    """
    flat: dict[str, object] = {}
    if not isinstance(front, dict):
        return flat
    for k, v in front.items():
        if not isinstance(v, (dict, list)):
            flat[str(k)] = v
    for v in front.values():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                flat.setdefault(str(k2), v2)
    return flat


def _memory_split_frontmatter(text: str) -> tuple[dict, str]:
    """(평평한 프론트매터 dict, 본문) 을 돌려준다. 파싱 실패해도 예외를 던지지 않는다."""
    m = _MEMORY_FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw_front, body = m.group(1), text[m.end():]
    parsed: object = None
    try:
        parsed = yaml.safe_load(raw_front)
    except Exception:
        parsed = None
    flat = _memory_flat_fields(parsed)
    if flat:
        return flat, body
    # YAML 이 깨졌으면 줄 단위 fallback — 값 하나 때문에 엔트리를 통째로 잃지 않는다.
    fallback: dict[str, object] = {}
    for line in raw_front.splitlines():
        sm = _MEMORY_SCALAR_RE.match(line)
        if sm:
            fallback.setdefault(sm.group(1), sm.group(2).strip().strip("\"'"))
    return fallback, body


def _memory_body_excerpt(body: str, limit: int = MEMORY_BODY_LINES) -> str:
    """본문 발췌를 데이터 풀에 안전하게 실을 형태로 정규화한다.

    - ATX 헤딩은 h5 이하로 강등한다. 원문에 `## 1. ...` 이 있으면 데이터 풀의 섹션 번호
      순서(§0 → §0.5 → §1 …)를 재는 검사가 오탐한다 — 실측 104 건 중 78 건이 헤딩 보유다.
    - 언어 힌트 없는 여는 fence 는 ```text 로 채운다.
    - 잘린 자리가 fence 안이면 닫아 준다.
    """
    out: list[str] = []
    in_fence = False
    truncated = False
    for raw in body.lstrip("\n").splitlines():
        if len(out) >= limit:
            truncated = True
            break
        stripped = raw.strip()
        if stripped.startswith("```"):
            if not in_fence:
                indent = raw[: len(raw) - len(raw.lstrip())]
                hint = stripped[3:].strip()
                out.append(f"{indent}```{hint or 'text'}")
                in_fence = True
            else:
                out.append(raw)
                in_fence = False
            continue
        if not in_fence:
            hm = _MEMORY_ATX_RE.match(raw)
            if hm:
                raw = "#" * min(6, len(hm.group(1)) + 4) + " " + hm.group(2)
        out.append(raw)
    if in_fence:
        out.append("```")
    while out and not out[-1].strip():
        out.pop()
    if truncated:
        out += ["", f"… (본문 {limit} 줄까지만 — 전문은 위 경로를 직접 읽어라)"]
    return "\n".join(out).strip()


def _strip_id_hash_suffix(name: str) -> str:
    """reflect-kit hybrid project_id 의 `-<hash6>` 접미를 벗긴다."""
    if re.fullmatch(r".+-[0-9a-f]{6}", name):
        return name[:-7]
    return name


def collect_promotion_ledger_freq(logs_root: Path) -> tuple[dict[str, int], list[str]]:
    """reflect-promote 의 승격 ledger 에서 재발 빈도만 **읽어** 온다.

    반환: (tag → freq, 읽은 ledger 파일 표시경로 목록).
    `post_freq` 가 숫자면 그 값을, 아니면 `initial_freq` 를 쓴다. ledger 는 없을 수 있고
    (실측 2026-08-14 기준 0 개) 그때는 빈 dict 로 조용히 진행한다 — 중요도 축이 하나
    빠질 뿐 수집이 죽어서는 안 된다.

    **쓰기 금지.** 승격 판정 · rule_id 발급 · status 전환은 전부 reflect-promote 소관이다.
    """
    freq: dict[str, int] = {}
    files: list[str] = []
    if not logs_root.is_dir():
        return freq, files
    try:
        candidates = sorted(logs_root.glob("*/" + PROMOTION_LEDGER_FILENAME))
    except OSError:
        return freq, files
    for ledger in candidates:
        try:
            text = ledger.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        files.append(display_path(ledger))
        tags: list[str] = []
        initial: int | None = None
        post: int | None = None

        def _flush() -> None:
            value = post if post is not None else initial
            if value is None:
                return
            for t in tags:
                if value > freq.get(t, 0):
                    freq[t] = value

        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("- rule_id:"):
                _flush()
                tags, initial, post = [], None, None
                continue
            key, _, value = stripped.partition(":")
            key = key.lstrip("- ").strip()
            value = value.strip()
            if key in ("mistake_tag", "lemma_key") and value:
                tags.append(value.strip("\"'"))
            elif key == "aliases" and value:
                for alias in value.strip("[]").split(","):
                    alias = alias.strip().strip("\"'")
                    if alias:
                        tags.append(alias)
            elif key == "initial_freq" and value.isdigit():
                initial = int(value)
            elif key == "post_freq" and value.isdigit():
                post = int(value)
        _flush()
    return freq, files


def _memory_ledger_freq(
    ledger_freq: dict[str, int], filename: str, name: str
) -> int:
    """메모리 파일 하나에 대응하는 ledger 재발 빈도를 찾는다 (정확 일치만)."""
    if not ledger_freq:
        return 0
    stem = filename[:-3] if filename.endswith(".md") else filename
    if stem.startswith("feedback_"):
        stem = stem[len("feedback_"):]
    keys = {
        stem.replace("_", "-"),
        stem,
        str(name or "").strip(),
        str(name or "").strip().replace("feedback-", "", 1),
    }
    best = 0
    for k in keys:
        if k and k in ledger_freq:
            best = max(best, ledger_freq[k])
    return best


def _memory_domains(name: str, description: str, body: str) -> tuple[str, list[str]]:
    """관련성 축 — (primary group, secondary groups)."""
    head = f"{name}\n{description}".lower()
    tail = body.lower()
    scored: list[tuple[int, int, str]] = []
    for idx, (gid, _label, matchers) in enumerate(_MEMORY_GROUP_MATCHERS):
        score = 0
        for match in matchers:
            if match(head):
                score += 2
            elif match(tail):
                score += 1
        if score:
            scored.append((-score, idx, gid))
    if not scored:
        return MEMORY_FALLBACK_GROUP[0], []
    scored.sort()
    return scored[0][2], [gid for _s, _i, gid in scored[1:]]


def _memory_importance(grounding: str, body: str, ledger_hits: int) -> tuple[int, dict]:
    """중요도 축 — grounding 등급 + 재발 신호. **시간 축은 들어가지 않는다.**"""
    base = GROUNDING_WEIGHT.get(grounding, 0)
    lowered = body.lower()
    markers = sum(1 for m in MEMORY_REPEAT_MARKERS if m in lowered)
    counts = [int(n) for n in _MEMORY_REPEAT_COUNT_RE.findall(body)]
    counted = max(counts) if counts else 0
    parts = {
        "grounding": base,
        "repeat_markers": min(markers, 4),
        "repeat_count": min(counted, 5),
        "ledger": min(ledger_hits, 5),
    }
    return sum(parts.values()), parts


def collect_memory_feedback(
    memory_root: Path | None = None, logs_root: Path | None = None
) -> dict:
    """`~/.claude/projects/*/memory/*.md` 를 전 프로젝트 순회해 feedback 타입만 모은다."""
    root = MEMORY_ROOT if memory_root is None else memory_root
    logs = REFLECT_LOGS_ROOT if logs_root is None else logs_root
    result: dict = {
        "root": root,
        "root_exists": root.is_dir(),
        "scanned": 0,
        "entries": [],
        "projects": [],
        "by_grounding": Counter(),
        "invalid_grounding": Counter(),
        "invalid_count": 0,
        "ledger_files": [],
        "ledger_tags": 0,
    }
    if not root.is_dir():
        return result

    ledger_freq, ledger_files = collect_promotion_ledger_freq(logs)
    result["ledger_files"] = ledger_files
    result["ledger_tags"] = len(ledger_freq)

    projects: set[str] = set()
    for md in sorted(root.glob("*/memory/*.md")):
        if md.name == MEMORY_INDEX_FILENAME or not md.is_file():
            continue
        result["scanned"] += 1
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not _MEMORY_FEEDBACK_RE.search(text):
            continue

        front, body = _memory_split_frontmatter(text)
        name = str(front.get("name") or md.stem)
        description = " ".join(str(front.get("description") or "").split())
        raw_grounding = front.get("grounding")
        if raw_grounding is None:
            grounding, invalid = GROUNDING_UNTAGGED, False
        else:
            token = str(raw_grounding).strip().strip("\"'")
            if token in GROUNDING_VALUES:
                grounding, invalid = token, False
            else:
                grounding, invalid = token or "(빈 값)", True

        project = md.parent.parent.name
        projects.add(project)
        primary, secondary = _memory_domains(name, description, body)
        ledger_hits = _memory_ledger_freq(ledger_freq, md.name, name)
        importance, parts = _memory_importance(
            GROUNDING_UNTAGGED if invalid else grounding, body, ledger_hits
        )

        if invalid:
            result["invalid_grounding"][grounding] += 1
            result["invalid_count"] += 1
        else:
            result["by_grounding"][grounding] += 1

        result["entries"].append(
            {
                "project": project,
                "file": md.name,
                "path": display_path(md),
                "name": name,
                "description": description,
                "grounding": grounding,
                "grounding_invalid": invalid,
                "verified": (not invalid) and grounding not in GROUNDING_UNVERIFIED,
                "primary": primary,
                "secondary": secondary,
                "importance": importance,
                "importance_parts": parts,
                "body": body,
            }
        )

    result["projects"] = sorted(projects)
    return result


def select_memory_entries(entries: list[dict]) -> tuple[list[dict], list[dict]]:
    """관련성(도메인 그룹) · 중요도 2 축 선별. **시간 축을 쓰지 않는다.**

    반환: (주입 대상, 탈락 대상). 두 리스트의 합은 항상 입력 전체와 같다 —
    탈락분은 제목 목록으로 §0.5 말미에 남으므로 어느 엔트리도 조용히 사라지지 않는다.
    grounding 이 허용 4 값 밖인 엔트리는 집계·주입에서 제외되고 탈락 쪽으로 간다.
    """
    eligible = [e for e in entries if not e["grounding_invalid"]]
    excluded = [e for e in entries if e["grounding_invalid"]]

    grouped: dict[str, list[dict]] = defaultdict(list)
    for e in eligible:
        grouped[e["primary"]].append(e)

    def rank(entry: dict) -> tuple:
        # 결정론적 정렬. 동점은 프로젝트·파일명 사전순으로만 가른다.
        return (-entry["importance"], entry["project"], entry["file"])

    picked: list[dict] = []
    for gid, members in grouped.items():
        members.sort(key=rank)
        picked.extend(members[:MEMORY_INJECT_PER_GROUP])

    picked.sort(key=rank)
    if len(picked) > MEMORY_INJECT_CAP:
        picked = picked[:MEMORY_INJECT_CAP]

    chosen_ids = {(e["project"], e["file"]) for e in picked}
    dropped = [
        e for e in eligible if (e["project"], e["file"]) not in chosen_ids
    ] + excluded
    dropped.sort(key=lambda e: (e["primary"], -e["importance"], e["project"], e["file"]))
    return picked, dropped


def render_memory_section(memory: dict | None) -> list[str]:
    """데이터 풀 §0.5 렌더. §0 과 §1 **사이**에 들어간다."""
    lines = [
        "## 0.5. 프로젝트 메모리 (`feedback` 타입 · 전 프로젝트 교차)",
        "",
    ]
    if memory is None or not memory.get("root_exists") or not memory.get("entries"):
        root = memory.get("root") if memory else MEMORY_ROOT
        lines += [
            f"- (없음) `{display_path(Path(root))}` 아래에 `metadata.type: feedback` "
            "메모리가 없다.",
            "- 메모리는 `/reflect-promote` 가 `project_memory` surface 로 승격할 때 생성된다.",
            "",
        ]
        return lines

    entries = memory["entries"]
    picked, dropped = select_memory_entries(entries)
    total = len(entries)
    by_g = memory["by_grounding"]
    dist = " · ".join(
        f"`{g}` {by_g.get(g, 0)}" for g in GROUNDING_VALUES
    ) + f" · `{GROUNDING_UNTAGGED}` {by_g.get(GROUNDING_UNTAGGED, 0)}"

    lines += [
        f"- 소스: `{display_path(Path(memory['root']))}/*/memory/*.md` "
        f"(`{MEMORY_INDEX_FILENAME}` 은 색인이라 제외)",
        f"- 집계: 프로젝트 **{len(memory['projects'])}** · `feedback` 엔트리 **{total}** "
        f"(스캔한 메모리 파일 {memory['scanned']})",
        f"- 주입 **{len(picked)}** · 탈락 **{len(dropped)}** "
        f"(= {len(picked)} + {len(dropped)} = **{total}**)",
        f"- grounding 분포: {dist}",
    ]

    invalid = memory.get("invalid_grounding", Counter())
    if memory.get("invalid_count"):
        detail = ", ".join(f"`{v}` {c}" for v, c in sorted(invalid.items()))
        lines.append(
            f"- ⚠ grounding 값이 허용 4 값 밖 → **집계 제외 {memory['invalid_count']} 건** "
            f"({detail}). 아래 탈락 목록에 `[제외]` 로 표기했다."
        )
    else:
        lines.append("- grounding 값이 허용 4 값 밖 → 집계 제외 **0** 건")

    if memory.get("ledger_files"):
        lines.append(
            f"- 재발 신호 참조 ledger(읽기 전용): {len(memory['ledger_files'])} 개 · "
            f"태그 {memory['ledger_tags']} 종 — "
            + ", ".join(f"`{p}`" for p in memory["ledger_files"][:5])
        )
    else:
        lines.append(
            f"- 재발 신호 참조 ledger: 없음 (`{display_path(REFLECT_LOGS_ROOT)}/*/"
            f"{PROMOTION_LEDGER_FILENAME}` 미존재 — 재발 가중치 0 으로 진행)"
        )

    lines += [
        "",
        "### 선별 축 · 읽는 법",
        "",
        "- 선별은 **관련성 · 중요도 2 축**이다. **시간(recency) 축은 쓰지 않는다** — "
        "갱신 시각 필드의 보유율이 낮아(실측 104 중 44) 나머지가 임의 판정되기 때문이다.",
        "- **관련성**: 메모리 `description`·`name`(가중 2) 과 본문(가중 1) 의 도메인 키워드 "
        "일치. 데이터 풀은 Phase 별로 나뉘지 않으므로 아래 그룹 제목에서 자기 도메인을 찾아라.",
        f"- **중요도**: `grounding` 등급 + 재발 신호(본문의 반복 언급 + ledger `post_freq`/"
        f"`initial_freq`). 그룹별 상위 {MEMORY_INJECT_PER_GROUP} 건까지 본문을 싣고 "
        f"(전체 상한 {MEMORY_INJECT_CAP}), 나머지는 말미에 제목만 남긴다.",
        "- ⚠ **`self_inference` 와 `미분류` 는 계약 조건의 PASS 근거로 쓰지 마라.** "
        "외부 검증(사용자 교정 · 실행 증거)이 없는 자기추론이다. 참고 신호로만 읽고, "
        "근거가 필요하면 원 출처를 다시 확인하라.",
        "- 이 절은 **읽기 전용**이다. 카이젠은 메모리 파일도 승격 ledger 도 직접 쓰지 않는다 — "
        "승격은 `/reflect-promote` 소관이다.",
        "",
        "### 주입 — 도메인 그룹별",
        "",
    ]

    picked_by_group: dict[str, list[dict]] = defaultdict(list)
    for e in picked:
        picked_by_group[e["primary"]].append(e)
    group_total = Counter(e["primary"] for e in entries)

    order = [gid for gid, _l, _k in MEMORY_DOMAIN_GROUPS] + [MEMORY_FALLBACK_GROUP[0]]
    for gid in order:
        members = picked_by_group.get(gid)
        if not members:
            continue
        label = MEMORY_GROUP_LABELS.get(gid, gid)
        lines += [
            f"#### [{gid}] {label} — 전체 {group_total[gid]} 건 중 {len(members)} 건 주입",
            "",
        ]
        for e in members:
            tags = [f"grounding `{e['grounding']}`", f"중요도 {e['importance']}"]
            if e["secondary"]:
                tags.append("연관 " + "·".join(f"`{s}`" for s in e["secondary"]))
            if not e["verified"]:
                tags.append("⚠ **PASS 근거 사용 금지**")
            desc = e["description"][:MEMORY_DESC_CHARS] or "(설명 없음)"
            lines += [
                f"- **{e['name']}** — {desc}",
                f"  - `{e['path']}` · " + " · ".join(tags),
                "",
                f"<details><summary>{e['file']} 본문 발췌</summary>",
                "",
                _memory_body_excerpt(e["body"]),
                "",
                "</details>",
                "",
            ]

    lines += [
        f"### 탈락 — 제목만 ({len(dropped)} 건)",
        "",
        "선별에서 밀렸을 뿐 틀린 신호가 아니다. 자기 도메인 항목이 보이면 경로를 직접 읽어라.",
        "",
    ]
    if not dropped:
        lines.append("- (없음 — 전건 주입됨)")
    for e in dropped:
        mark = "[제외] " if e["grounding_invalid"] else ""
        reason = (
            f"grounding `{e['grounding']}` 가 허용 4 값 밖 — 집계 제외"
            if e["grounding_invalid"]
            else f"grounding `{e['grounding']}` · 중요도 {e['importance']}"
        )
        desc = e["description"][:MEMORY_DESC_CHARS] or "(설명 없음)"
        # 연관 그룹까지 적는다 — primary 만 적으면 rust/react 처럼 primary 보유 엔트리가
        # 0 인 Phase 가 자기 신호를 아예 못 찾는다.
        groups = "".join(f"[{g}]" for g in [e["primary"], *e["secondary"]])
        lines.append(
            f"- {mark}**{e['name']}** {groups} — {desc}  "
            f"(`{e['path']}` · {reason})"
        )
    lines.append("")
    return lines

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
    memory: dict | None = None,
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

    # §0.5: 프로젝트 메모리 (feedback 타입) — **§0 과 §1 사이**에 온다.
    # Phase 서브에이전트가 §0 다음으로 읽는 자리다.
    lines += render_memory_section(memory)

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
        "**모든 Phase 는 §0.5 (프로젝트 메모리) 에서 자기 도메인 그룹을 함께 읽는다.** "
        "그룹 제목의 `[gid]` 가 Phase 대상 킷에 대응한다. 단 `self_inference`·`미분류` "
        "라벨이 붙은 항목은 계약 조건의 PASS 근거로 쓸 수 없다.",
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
    parser.add_argument(
        "--insights",
        type=Path,
        default=None,
        metavar="PATH",
        help=(
            "/insights 산출물 경로를 명시 지정 (자동 탐색보다 우선). "
            "생략하면 후보를 우선순위대로 탐색: "
            + " → ".join(display_path(p) for p in INSIGHTS_CANDIDATES)
        ),
    )
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()

    print("[1/7] /insights 리포트 탐색 중...", file=sys.stderr)
    insights_path, insights_trace = resolve_insights_path(args.insights)
    for line in insights_trace:
        print(f"       {line}", file=sys.stderr)
    if args.insights is not None and insights_path is None:
        # 사용자가 명시한 경로가 없으면 조용히 다른 후보로 대체하지 않는다 —
        # "지정한 리포트로 돌렸다" 는 착각이 그대로 데이터 풀에 남기 때문이다.
        print(
            f"ERROR: --insights 로 지정한 파일이 없다: {args.insights}",
            file=sys.stderr,
        )
        return 2
    insights = collect_insights_report(insights_path)

    print("[2/7] 글로벌 feedback 수집 중...", file=sys.stderr)
    global_fb = collect_global_feedback()

    print("[3/7] 프로젝트 메모리(feedback) 수집 중...", file=sys.stderr)
    memory = collect_memory_feedback()

    print("[4/7] Hub 외부 프로젝트 수집 중...", file=sys.stderr)
    hub_projects = collect_hub_projects(args.hub_dir)

    print("[5/7] followup 문서 수집 중...", file=sys.stderr)
    followups = collect_followup_docs()

    print("[6/7] 현재 레포 sprint-contract 이력 수집 중...", file=sys.stderr)
    local_contracts = collect_recent_local_contracts()

    validate_output: str | None = None
    if not args.skip_validate:
        print("[7/7] validate-plugin 스냅샷 실행 중...", file=sys.stderr)
        validate_output = run_validate_plugin()
    else:
        print("[7/7] validate-plugin 스냅샷 건너뜀 (--skip-validate)", file=sys.stderr)

    content = render_data_pool(
        global_fb,
        hub_projects,
        followups,
        local_contracts,
        validate_output,
        insights,
        memory,
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
        cands = " · ".join(display_path(p) for p in INSIGHTS_CANDIDATES)
        print(f"  - /insights 산출물: 없음 (후보 전부 미존재 — {cands})", file=sys.stderr)
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
    if memory.get("root_exists") and memory.get("entries"):
        picked, dropped = select_memory_entries(memory["entries"])
        print(
            f"  - project memory(feedback): {len(memory['entries'])}건"
            f" / 프로젝트 {len(memory['projects'])}개"
            f" · 주입 {len(picked)} · 탈락 {len(dropped)}"
            f" · grounding 4값 밖 제외 {memory['invalid_count']}건",
            file=sys.stderr,
        )
    else:
        print(
            f"  - project memory(feedback): 없음 ({display_path(Path(memory['root']))})",
            file=sys.stderr,
        )
    print(f"  - followups: {len(followups)}개", file=sys.stderr)
    print(f"  - local contracts: {len(local_contracts)}개", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
