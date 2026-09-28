#!/usr/bin/env python3
"""
detect-docs-drift.py — docs-site HTML 재생성 필요 manifest 생성

`git diff --since <ref>..HEAD` 기준으로 변경된 `.md` / `.yaml` 소스 파일을 찾아
대응하는 `docs/<plugin>/*.html` 경로를 매핑하여 stdout 에 출력한다.

kaizen-orchestrator Step F2 (docs-site 재생성) 에서 서브에이전트에게
"어느 HTML 을 재생성해야 하는지" 를 정확히 알려주기 위한 manifest 역할이다.

사용법:
    python3 scripts/detect-docs-drift.py [--since <ref>] [--json] [--include-format-only]
    python3 scripts/detect-docs-drift.py --check-table

옵션:
    --since <ref>    기준 git ref (기본: main)
    --json           JSON array 형식으로 출력
    --include-format-only
                     모양만 바뀐 원본의 짝도 낸다. 기본은 뺀 짝 수를 표준 오류에 한 줄로 적고 뺀다.
                     모양만 바뀜 = 두 판에서 HTML 주석을 지우고 코드 울타리 줄을 한 표지로 바꾼 뒤
                     낱말(\\w+)과 기호의 순서가 같다. 기호 가운데 마크다운 꾸밈(줄 앞 제목 · 인용 · 목록 기호,
                     표 구분 줄 · 가로줄, 표 칸 `|`, 강조 `*`, 백틱, `<주소>` 의 꺾쇠, 역슬래시)만 빼고 센다.
                     코드 울타리 안과 인라인 코드 안의 기호는 하나도 빼지 않는다
    --verbose        변경된 소스 전체 목록 포함
    --check-table    이 스크립트의 매핑과 docs-site SKILL.md Step 1 표를 맞댄다.
                     한쪽에만 있는 (원본, 출력 폴더) 짝을 이름으로 대고 exit 1
    --help           사용법 출력
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# 소스 경로 prefix → 출력 HTML 디렉토리 매핑. 사람이 읽는 표는 `.claude/skills/docs-site/SKILL.md` Step 1 에 있다 —
# 한쪽만 고치면 표를 보고 만든 페이지와 이 스크립트가 고르는 재생성 대상이 갈라진다
SOURCE_TO_HTML: list[tuple[str, str]] = [
    ("harness/docs/guides/", "docs/harness/"),
    ("harness/references/", "docs/harness/"),
    ("docs/backend/", "docs/backend-kit/"),
    ("docs/infra/", "docs/infra-kit/"),
    ("docs/rust/", "docs/rust-kit/"),
    ("docs/react/", "docs/react-kit/"),
    ("docs/flutter/", "docs/flutter-toolkit/"),
    ("flutter-toolkit/references/", "docs/flutter-toolkit/"),
    ("design-kit/docs/design/", "docs/design-kit/"),
    # design-kit 의 references/ · skills/ 에는 페이지가 없는 원본이 섞여 있어 짝이 있는 파일만 잇는다
    ("design-kit/references/visual-change-protocol.md", "docs/design-kit/"),
    ("design-kit/skills/design-test/SKILL.md", "docs/design-kit/"),
    ("design-kit/skills/design-mockup/SKILL.md", "docs/design-kit/"),
    ("infra-kit/skills/infra-test/SKILL.md", "docs/infra-kit/"),
    # 아래 3 종은 kaizen-orchestrator SKILL.md 가 매핑 대상으로 명시하는데도 누락되어
    # `.md` 20 개가 조용히 drift 감지 밖에 있었다 (rust-kit 1 · react-kit 7 · docs/planning 12).
    ("rust-kit/references/", "docs/rust-kit/"),
    ("react-kit/references/", "docs/react-kit/"),
    ("docs/planning/", "docs/planning-kit/"),
    ("docs/tone/", "docs/tone-kit/"),
    # 2026-09-13: reflect-kit 이 매핑에 없어 codex-kaizen 문서가 8 일간 조용히 낡았다.
    # 스킬 본문이 곧 문서의 소스인 킷은 skills/ 를 직접 매핑한다.
    ("reflect-kit/skills/", "docs/reflect-kit/"),
    ("reflect-kit/references/", "docs/reflect-kit/"),

    ("tone-kit/references/", "docs/tone-kit/"),

    # 2026-09-14: bambu-kit 이 매핑에 없어 SKILL.md 를 크게 고쳐도 "no docs drift" 가 나왔고,
    # 파생 페이지가 "OrcaSlicer 요청에는 트리거되지 않는다" 를 그대로 단 채 QA 까지 갔다.
    # reflect-kit 과 같은 누락이 같은 이유로 반복된 것이다.
    ("bambu-kit/skills/bambu-print-profile/references/", "docs/bambu-kit/"),

    # 2026-09-25: api-kit · howto-kit · onboarding-kit 원본이 매핑에 없어 고쳐도 "no docs drift" 가 나왔다.
    # 원본 폴더 이름(docs/api · docs/howto)과 페이지 폴더 이름(docs/api-kit · docs/howto-kit)이 다르다.
    ("docs/api/", "docs/api-kit/"),
    ("docs/howto/", "docs/howto-kit/"),
    # onboarding-kit 은 스킬 하나가 킷 전부다. 같은 스킬 폴더의 evals/ 픽스처는 페이지가 아니라서
    # 스킬 폴더 전체가 아니라 본문과 references/ 만 잇는다
    ("onboarding-kit/skills/setup-guide/SKILL.md", "docs/onboarding-kit/"),
    ("onboarding-kit/skills/setup-guide/references/", "docs/onboarding-kit/"),
    # 카이젠 참고 문서 폴더에는 페이지 없는 원본이 섞여 있어 짝이 있는 파일만 잇는다
    (".claude/skills/kaizen-orchestrator/references/phase-research-templates.md", "docs/process/"),
]


# 소스 stem 에서 출력 이름을 유도할 수 없는 매핑 (1:N 허용).
# 규칙으로 추측하면 조용히 틀리므로 여기에 명시한다.
SOURCE_OVERRIDES: dict[str, list[str]] = {
    # 한 소스가 두 페이지로 갈라진다 — stem 규칙으로는 표현 불가
    "design-kit/docs/design/foundations/spacing-layout.md": [
        "docs/design-kit/spacing-system.html",
        "docs/design-kit/grid-alignment.html",
    ],
    # bambu-kit 은 스킬 폴더의 references/ 만 접두 매핑에 있어 본문을 여기 명시한다
    "bambu-kit/skills/bambu-print-profile/SKILL.md": [
        "docs/bambu-kit/bambu-print-profile.html",
    ],
    # 예제 원본은 페이지 이름이 원본 이름과 다르다
    "docs/onboarding-kit/examples/fcm-ios-setup-guide.md": [
        "docs/onboarding-kit/fcm-ios-example.html",
    ],
    "api-kit/skills/api-ui/SKILL.md": ["docs/api-kit/static-evidence-viewer-contract.html"],
    # 원본 이름이 대문자다. 규칙으로 두면 대소문자를 가리지 않는 맥 파일 시스템에서 `DESIGN.html` 이
    # 있는 것으로 나와 등록 안 된 페이지로 잘못 잡힌다
    "reflect-kit/docs/DESIGN.md": ["docs/reflect-kit/design.html"],
    "reflect-kit/docs/SCHEMA.md": ["docs/reflect-kit/schema.html"],
    "reflect-kit/docs/RESEARCH.md": ["docs/reflect-kit/research.html"],
    ".claude/skills/kaizen-orchestrator/SKILL.md": ["docs/process/kaizen-flow.html"],
    # 설계 기록 하나를 출처로 단 페이지가 둘이다 (`grep -l api-kit-design docs/api-kit/*.html`)
    "docs/superpowers/specs/2026-09-02-api-kit-design.md": [
        "docs/api-kit/multi-sample-pagination-variance.html",
        "docs/api-kit/contract-extraction-modes.html",
    ],
    # 원본보다 페이지가 먼저 생겨 이름이 다르다. 새 이름으로 두 번째 페이지를 만들지 않고 기존 페이지와 짝짓는다 (dca DC-9)
    "docs/howto/design-brief.md": ["docs/howto-kit/overview.html"],
    "harness/references/feedback-schema.yaml": ["docs/harness/feedback-system.html"],
    "docs/react/kit-design/final-integration.md": ["docs/react-kit/integration.html"],
    "docs/react/kit-design/g1-scaffolding.md": ["docs/react-kit/scaffolding.html"],
    "docs/react/kit-design/g2-state-data.md": ["docs/react-kit/state-data.html"],
    "docs/react/kit-design/g3-performance.md": ["docs/react-kit/performance.html"],
    "docs/react/kit-design/g4-quality.md": ["docs/react-kit/quality.html"],
    "docs/react/kit-design/g5-ui-patterns.md": ["docs/react-kit/ui-patterns.html"],
    "docs/react/kit-design/g5b-animation.md": ["docs/react-kit/animation.html"],
    "docs/react/kit-design/g6-build-audit.md": ["docs/react-kit/build-audit.html"],
    # tone 코어 규칙은 먼저 생긴 리서치 쪽이 같은 주제를 다룬다. 이름으로 새 쪽을 만들지 않고 그 쪽과 짝짓는다
    "tone-kit/references/core-antipatterns.md": ["docs/tone-kit/antipattern-catalog.html"],
    "tone-kit/references/core-comment.md": ["docs/tone-kit/comment-economy.html"],
    "tone-kit/references/core-naming.md": ["docs/tone-kit/naming-taxonomy.html"],
    "tone-kit/references/core-structure.md": ["docs/tone-kit/extraction-thresholds.html"],
    # 스킬의 부속 목록이라 따로 쪽을 두지 않고 그 스킬 쪽에 묶는다
    "reflect-kit/skills/codex-kaizen/references/search-sources.md": ["docs/reflect-kit/codex-kaizen.html"],
}

DOCS_SITE_SKILL = REPO_ROOT / ".claude/skills/docs-site/SKILL.md"

# 초안 폴더의 SKILL.md 가 스킬 본문 이름 규칙에 걸려 없는 `drafts.html` 을 새 페이지로 냈다.
# tone project-detection 은 킷이 프로젝트 값을 감지하는 절차라 페이지를 만들지 않는 원본이다 (d1 결정표)
SOURCE_EXCLUDES: tuple[str, ...] = ("docs/howto/drafts/", "tone-kit/references/project-detection.md")

# 울타리 뒤에는 언어 표시 한 낱말만 온다. `\S*` 로 두면 `~~~old_value~~~` 같은 본문 줄까지 울타리로 보고 낱말째 지웠다
FENCE_LINE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*[\w.+#-]*\s*$")
TOKEN_RE = re.compile(r"\w+|[^\w\s]")
TABLE_RULE_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
# `___` 는 낱말이라 빼지 않는다 — 낱말만 맞대던 때도 내용으로 셌다
THEMATIC_BREAK_RE = re.compile(r"^\s*([-*=])(\s*\1){2,}\s*$")
# 줄 앞 인용 · 제목 · 목록 기호. 번호 목록의 번호는 낱말이라 남기고 뒤의 `.` · `)` 만 뺀다
LINE_MARK_RE = re.compile(r"^\s*(?:>\s*)*(?:#{1,6}(?=\s|$)|[-*+](?=\s)|(\d+)[.)](?=\s))?")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(.+?)\1(?!`)")
AUTOLINK_RE = re.compile(r"<((?:https?|mailto|ftp):[^>\s]+|[^@\s<>]+@[^@\s<>]+)>")
ESCAPE_RE = re.compile(r"\\([^\w\s])")
DECORATION_RE = re.compile(r"[*|`]")


# docs-site 페이지는 소스 basename 과 1:1 이 아니다.
# 예: harness/docs/guides/plugin-validation-guide.md → docs/harness/plugin-validation.html
# (등록 페이지에는 `-guide` suffix 가 없다). 파일명 규칙을 추측하지 말고
# `docs/index.html` 의 페이지 레지스트리를 SSOT 로 삼아 대조한다.
INDEX_HTML = REPO_ROOT / "docs/index.html"
REGISTRY_FILE_RE = re.compile(r"file:\s*'([^']+\.html)'")

# 후보 target 이 레지스트리에 없을 때 시도할 stem 변형 (앞에서부터 순서대로)
STEM_VARIANTS: list[tuple[str, str]] = [
    ("-guide", ""),   # plugin-validation-guide → plugin-validation
    ("", "-guide"),   # skill-design → skill-design-guide
]


@dataclass
class DriftEntry:
    source: str
    target: str
    registered: bool = False
    exists: bool = False

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "registered": self.registered,
            "exists": self.exists,
        }


def load_registry() -> set[str]:
    """docs/index.html 에 등록된 HTML 경로 집합 (docs/ 기준 상대경로 → repo 상대경로)."""
    if not INDEX_HTML.exists():
        return set()
    text = INDEX_HTML.read_text(encoding="utf-8")
    return {f"docs/{m}" for m in REGISTRY_FILE_RE.findall(text)}


def resolve_target(candidate: str, registry: set[str]) -> tuple[str, bool, bool]:
    """후보 경로를 레지스트리/파일시스템과 대조해 실제 target 을 결정한다.

    Returns (target, registered, exists).
    """
    def probe(path: str) -> tuple[bool, bool]:
        return path in registry, (REPO_ROOT / path).is_file()

    registered, exists = probe(candidate)
    if registered or exists:
        return candidate, registered, exists

    directory, _, filename = candidate.rpartition("/")
    stem = filename[: -len(".html")]
    for old, new in STEM_VARIANTS:
        if old and not stem.endswith(old):
            continue
        variant_stem = (stem[: -len(old)] if old else stem) + new
        if variant_stem == stem:
            continue
        variant = f"{directory}/{variant_stem}.html"
        v_registered, v_exists = probe(variant)
        if v_registered or v_exists:
            return variant, v_registered, v_exists

    # 소스 stem 과 출력 stem 이 다른 경우 (color.md → color-palette.html,
    # typography.md → typography-scale.html). 레지스트리(SSOT)에서 같은 디렉토리의
    # `<stem>-*` 항목을 찾는다. 후보가 정확히 1 개일 때만 채택한다 — 2 개 이상이면
    # 추측이 되므로 신규 생성으로 남겨 사람이 판단하게 한다.
    prefix_matches = sorted(
        p for p in registry
        if p.startswith(f"{directory}/{stem}-") and p.endswith(".html")
    )
    if len(prefix_matches) == 1:
        target = prefix_matches[0]
        return target, True, (REPO_ROOT / target).is_file()

    # 대응 페이지가 아직 없다 — 신규 생성 대상
    return candidate, False, False


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def changed_files(since: str) -> list[str]:
    out = run_git(["diff", "--name-only", f"{since}..HEAD"])
    return [line for line in out.splitlines() if line.strip()]


def show_file(ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout if result.returncode == 0 else None


def content_tokens(text: str) -> list[str]:
    """낱말(`\\w+`)과 기호 한 글자씩의 순서. 마크다운 꾸밈 기호만 빼고 센다.

    낱말만 맞대면 `>= 5` → `<= 5` · `a + 1` → `a - 1` 처럼 기호만 바뀐 내용 수정을 모양만 바뀐 것으로 놓친다.
    코드 울타리 안과 인라인 코드 안은 글자 그대로라 기호를 하나도 빼지 않는다.
    """
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    tokens: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_LINE_RE.match(line):
            tokens.append("FENCE")
            in_fence = not in_fence
            continue
        if in_fence:
            tokens.extend(TOKEN_RE.findall(line))
            continue
        if TABLE_RULE_RE.match(line) or THEMATIC_BREAK_RE.match(line):
            continue
        line = LINE_MARK_RE.sub(lambda match: match.group(1) or "", line)
        for index, part in enumerate(INLINE_CODE_RE.split(line)):
            # split 결과는 코드 밖 · 백틱 묶음 · 코드 안 순서로 돈다
            if index % 3 == 2:
                tokens.extend(TOKEN_RE.findall(part))
            elif index % 3 == 0:
                part = AUTOLINK_RE.sub(r"\1", part)
                part = ESCAPE_RE.sub(r"\1", part)
                tokens.extend(TOKEN_RE.findall(DECORATION_RE.sub(" ", part)))
    return tokens


def is_format_only(source: str, since: str) -> bool:
    """두 판의 낱말 · 기호 순서가 같으면 모양만 바뀐 원본이다. 한쪽 판에 파일이 없으면 내용이 바뀐 것으로 본다."""
    before, after = show_file(since, source), show_file("HEAD", source)
    if before is None or after is None:
        return False
    return content_tokens(before) == content_tokens(after)


def map_source_to_html(source: str) -> str | None:
    """Given a changed source file, return the corresponding HTML target.

    Returns None if the source has no HTML mapping.
    """
    if not (source.endswith(".md") or source.endswith(".yaml") or source.endswith(".yml")):
        return None
    if source.startswith(SOURCE_EXCLUDES):
        return None

    for prefix, html_dir in SOURCE_TO_HTML:
        if source.startswith(prefix):
            # Convert name.md → name.html (strip all extensions).
            # 접두가 파일 경로 전체일 수 있어(onboarding SKILL.md) 이름은 원본 경로에서 뽑는다
            name = re.sub(r"\.(md|yaml|yml)$", "", Path(source).name)
            # 스킬 본문은 파일 이름이 모두 SKILL 이라 `SKILL.html` 로 겹친다 — 스킬 폴더 이름을 페이지 이름으로 쓴다
            if name == "SKILL":
                name = Path(source).parent.name
            # docs-site 출력은 **전부 flat** 이다 — 소스의 subdir 을 보존하면 안 된다.
            # (과거 design-kit 만 subdir 을 보존해 26/26 전부 존재하지 않는 경로를 가리켰고,
            #  그 결과 모든 design-kit 소스 변경이 `[NEW — 신규 생성 필요]` 로 오보되어
            #  재생성 시 기존 HTML 수정이 통째로 날아갔다.)
            return f"{html_dir}{name}.html"
    return None


def detect_drift(since: str, include_format_only: bool = True) -> tuple[list[DriftEntry], int]:
    """(짝 목록, 모양만 바뀌어 뺀 짝 수) 를 돌려준다."""
    sources = changed_files(since)
    registry = load_registry()
    entries: list[DriftEntry] = []
    seen: set[tuple[str, str]] = set()
    skipped = 0
    for src in sources:
        override = SOURCE_OVERRIDES.get(src)
        if override is not None:
            candidates = list(override)
        else:
            candidate = map_source_to_html(src)
            if candidate is None:
                continue
            candidates = [candidate]
        format_only = not include_format_only and is_format_only(src, since)
        for candidate in candidates:
            target, registered, exists = resolve_target(candidate, registry)
            key = (src, target)
            if key in seen:
                continue
            seen.add(key)
            if format_only:
                skipped += 1
                continue
            entries.append(
                DriftEntry(
                    source=src, target=target, registered=registered, exists=exists
                )
            )
    return entries, skipped


def script_pairs() -> set[tuple[str, str]]:
    """이 스크립트가 아는 (원본 경로 또는 접두, 출력 폴더) 짝."""
    pairs = set(SOURCE_TO_HTML)
    for source, pages in SOURCE_OVERRIDES.items():
        pairs.update((source, page.rpartition("/")[0] + "/") for page in pages)
    return pairs


def table_pairs() -> set[tuple[str, str]]:
    """docs-site SKILL.md Step 1 표의 (원본, 출력 폴더) 짝. 백틱으로 적은 칸만 읽는다."""
    text = DOCS_SITE_SKILL.read_text(encoding="utf-8")
    step1 = re.search(r"^## Step 1:.*?(?=^## )", text, re.M | re.S)
    pairs: set[tuple[str, str]] = set()
    for row in (step1.group(0) if step1 else "").splitlines():
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if not row.startswith("|") or len(cells) != 3:
            continue
        outputs = re.findall(r"`([^`]+)`", cells[2])
        pairs.update((source, output) for source in re.findall(r"`([^`]+)`", cells[1]) for output in outputs)
    return pairs


def check_table() -> int:
    """표와 스크립트 매핑이 서로를 덮는지 본다. 폴더 원본(`/` 로 끝남)은 그 아래 파일 원본을 덮는다."""
    def covered(pair: tuple[str, str], others: set[tuple[str, str]]) -> bool:
        source, output = pair
        return any(output == other_output and (source == other or (other.endswith("/") and source.startswith(other)))
                   for other, other_output in others)

    script, table = script_pairs(), table_pairs()
    if not table:
        print(f"ERROR: {DOCS_SITE_SKILL.relative_to(REPO_ROOT)} Step 1 표를 못 읽었다 — 맞댈 것이 없다")
        return 2
    missing = [f"표에 없는 짝 (스크립트에만): {source} → {output}"
               for source, output in sorted(script) if not covered((source, output), table)]
    missing += [f"스크립트에 없는 짝 (표에만): {source} → {output}"
                for source, output in sorted(table) if not covered((source, output), script)]
    for line in missing:
        print(line)
    print(f"매핑 맞대기: 스크립트 {len(script)} 짝 · 표 {len(table)} 짝 · 어긋남 {len(missing)}")
    return 1 if missing else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since",
        default="main",
        help="비교 기준 git ref (기본: main)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON array 형식으로 출력",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose logs"
    )
    parser.add_argument(
        "--check-table", action="store_true", help="매핑과 docs-site SKILL.md Step 1 표를 맞댄다"
    )
    parser.add_argument(
        "--include-format-only", action="store_true", help="모양만 바뀐 원본의 짝도 낸다"
    )
    args = parser.parse_args()
    if args.check_table:
        return check_table()

    entries, skipped = detect_drift(args.since, args.include_format_only)
    if skipped:
        print(f"모양만 바뀐 원본의 짝 {skipped} 개를 뺐다 — 모두 보려면 --include-format-only", file=sys.stderr)

    if args.json:
        print(json.dumps([e.to_dict() for e in entries], ensure_ascii=False, indent=2))
    else:
        if not entries:
            print(f"no docs drift since {args.since}")
        else:
            for e in entries:
                if not e.exists:
                    mark = "  [NEW — 대응 HTML 없음, 신규 생성 + index.html 등록 필요]"
                elif not e.registered:
                    mark = "  [UNREGISTERED — 파일은 있으나 index.html 미등록]"
                else:
                    mark = ""
                print(f"{e.source} → {e.target}{mark}")
            if args.verbose:
                new_count = sum(1 for e in entries if not e.exists)
                print(f"\nTotal: {len(entries)} HTML pages need regeneration"
                      f" ({new_count} new)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
