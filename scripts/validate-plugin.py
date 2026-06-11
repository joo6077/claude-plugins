#!/usr/bin/env python3
"""플러그인 검증 스크립트.

.claude-plugin/marketplace.json 에 등록된 모든 킷을 7가지 카테고리로 검증한다.
가이드: harness/docs/guides/plugin-validation-guide.md

Usage:
    python3 scripts/validate-plugin.py                          # 전체 킷
    python3 scripts/validate-plugin.py react-kit                # 특정 킷
    python3 scripts/validate-plugin.py --check=refs,placeholders # 특정 체크
    python3 scripts/validate-plugin.py --json                   # JSON 출력
    python3 scripts/validate-plugin.py --fix                    # 자동 수정 (V5 + V6)
    python3 scripts/validate-plugin.py --help                   # 사용법
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 이 설치되지 않았습니다. pip install pyyaml 로 설치하세요.", file=sys.stderr)
    sys.exit(2)

from plugin_utils import load_marketplace, list_kits, read_text, parse_frontmatter, REPO_ROOT

# ---------------------------------------------------------------------------
# 상수
# ---------------------------------------------------------------------------

# V5 --fix 치환 매핑: (패턴, 대체문자열)
FIX_PLACEHOLDER_RULES = [
    (re.compile(r'\bTODO\b\s*:?', re.IGNORECASE), "<설명 필요>"),
    (re.compile(r'\bFIXME\b\s*:?', re.IGNORECASE), "<수정 필요>"),
    (re.compile(r'\bTBD\b', re.IGNORECASE), "<내용 추가>"),
]

# V5 검사 대상 파일 glob 패턴
PLACEHOLDER_GLOBS = ["skills/*/SKILL.md", "agents/*.md", "README.md", "references/*.md"]

# V5 단어 경계 패턴
PLACEHOLDER_PATTERN = re.compile(r'\b(TODO|TBD|FIXME)\b', re.IGNORECASE)

# V4 키워드 추출 패턴 (3자 이상)
KEYWORD_PATTERN = re.compile(r'["\']([^"\']{3,})["\']')

# V3 마크다운 링크 추출 패턴 (앵커 제외)
LINK_PATTERN = re.compile(r'\[(?:[^\]]*)\]\(([^)#][^)]*)\)')

# V7 마켓플레이스 버전 태그 패턴
MARKETPLACE_VERSION_PATTERN = re.compile(r'\[v(\d+\.\d+\.\d+)\s*[·•]\s*\d{4}-\d{2}-\d{2}\]')

# V4 kit-specific context tokens — description 에 해당 kit 의 고유 단어가 포함되면
# exact-match cross-kit 중복은 disambiguation 성공으로 간주하여 WARN 제거.
# 이는 "같은 개념 다른 프레임워크" 케이스 (예: React `테스트 만들어줘` vs Flutter `테스트 만들어줘`)
# 를 false positive 로 처리하지 않기 위함.
KIT_CONTEXT_TOKENS: dict[str, set[str]] = {
    "harness": {"harness", "sprint-contract", "qa-evaluator", "계약"},
    "flutter-toolkit": {
        "flutter", "dart", "widget", "hookwidget", "hookconsumerwidget",
        "riverpod", "gorouter", "auto_route", "freezed", "slang", "arb",
    },
    "design-kit": {"design-kit", "디자인", "figma", "mockup", "디자인 토큰", "moodboard"},
    "backend-kit": {"백엔드", "backend-kit", "hexagonal", "api 설계"},
    "infra-kit": {"infra-kit", "devops", "kubernetes", "terraform", "인프라"},
    "rust-kit": {"rust", "cargo", "axum", "sqlx", "tonic", "clippy", "rustc"},
    "react-kit": {
        "react", "vite", "tauri", "shadcn", "zustand", "tanstack",
        "wasm", "wasm-pack", "tailwind v4", "react hook form",
    },
}

# ---------------------------------------------------------------------------
# 결과 구조체
# ---------------------------------------------------------------------------

class CheckResult:
    """단일 체크 결과."""

    def __init__(self, check_id: str, label: str):
        self.check_id = check_id          # V1~V8
        self.label = label                 # 사람이 읽을 이름
        self.status = "OK"                 # OK | WARN | FAIL | SKIP
        self.summary = ""                  # 요약 (예: "7 skills + 1 agent — OK")
        self.details: list[str] = []       # 파일:라인 수준 상세

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "label": self.label,
            "status": self.status,
            "summary": self.summary,
            "details": self.details,
        }


class PluginResult:
    """단일 킷의 전체 검증 결과."""

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.checks: list[CheckResult] = []

    @property
    def overall_status(self) -> str:
        statuses = {c.status for c in self.checks}
        if "FAIL" in statuses:
            return "ERROR"
        if "WARN" in statuses:
            return "WARNING"
        return "OK"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "path": str(self.path.relative_to(REPO_ROOT)),
            "overall": self.overall_status,
            "checks": [c.to_dict() for c in self.checks],
        }


# ---------------------------------------------------------------------------
# CheckContext
# ---------------------------------------------------------------------------

@dataclass
class CheckContext:
    """단일 킷 검증에 필요한 모든 컨텍스트."""

    kit_path: Path
    marketplace_data: dict
    fix: bool = False
    all_keywords: dict[str, set[str]] = field(default_factory=dict)
    all_context_hits: dict[str, bool] = field(default_factory=dict)
    _file_cache: dict[Path, str] = field(default_factory=dict)

    def read(self, path: Path) -> str:
        """파일 내용을 캐시하여 반환한다."""
        if path not in self._file_cache:
            self._file_cache[path] = read_text(path)
        return self._file_cache[path]

    def invalidate(self, path: Path) -> None:
        """fix 후 캐시를 무효화한다."""
        self._file_cache.pop(path, None)


# ---------------------------------------------------------------------------
# V1 Frontmatter 무결성
# V1 — see harness/docs/guides/plugin-validation-guide.md §3.1
# ---------------------------------------------------------------------------

def check_v1_frontmatter(ctx: CheckContext) -> CheckResult:
    """SKILL.md 와 agents/*.md 의 YAML frontmatter 필수 필드를 검증한다."""
    result = CheckResult("V1", "frontmatter")
    required_skill = {"name", "description", "user-invocable"}
    required_agent = {"name", "description", "tools", "model"}

    skill_files = sorted(ctx.kit_path.glob("skills/*/SKILL.md"))
    agent_files = sorted(ctx.kit_path.glob("agents/*.md"))
    failures: list[str] = []

    for path in skill_files:
        text = ctx.read(path)
        fm, _ = parse_frontmatter(text)
        rel = path.relative_to(REPO_ROOT)
        if fm is None:
            failures.append(f"FAIL {rel}: frontmatter 파싱 실패")
            continue
        missing = required_skill - set(fm.keys())
        if missing:
            failures.append(f"FAIL {rel}: 누락 필드 {sorted(missing)}")
        else:
            empty = [f for f in required_skill if fm.get(f) is None or fm.get(f) == ""]
            if empty:
                failures.append(f"FAIL {rel}: 빈 필드 {sorted(empty)}")

    for path in agent_files:
        text = ctx.read(path)
        fm, _ = parse_frontmatter(text)
        rel = path.relative_to(REPO_ROOT)
        if fm is None:
            failures.append(f"FAIL {rel}: frontmatter 파싱 실패")
            continue
        missing = required_agent - set(fm.keys())
        if missing:
            failures.append(f"FAIL {rel}: 누락 필드 {sorted(missing)}")

    ns = len(skill_files)
    na = len(agent_files)
    label_parts = []
    if ns:
        label_parts.append(f"{ns} skill{'s' if ns != 1 else ''}")
    if na:
        label_parts.append(f"{na} agent{'s' if na != 1 else ''}")
    counts = " + ".join(label_parts) if label_parts else "0 files"

    if failures:
        result.status = "FAIL"
        result.summary = f"{counts} — {len(failures)} FAIL"
        result.details = failures
    else:
        result.status = "OK"
        result.summary = f"{counts} — OK"
    return result


# ---------------------------------------------------------------------------
# V2 Templates 구문
# V2 — see harness/docs/guides/plugin-validation-guide.md §3.2
# ---------------------------------------------------------------------------

def check_v2_templates(ctx: CheckContext) -> CheckResult:
    """templates/ 내 JSON/YAML/TOML 파일을 표준 파서로 파싱 검증한다."""
    result = CheckResult("V2", "templates")
    tmpl_dir = ctx.kit_path / "templates"

    if not tmpl_dir.exists():
        result.status = "OK"
        result.summary = "0 files — SKIP (no templates/)"
        return result

    all_files = sorted(tmpl_dir.iterdir())
    parsed = 0
    skipped = 0
    failures: list[str] = []

    for path in all_files:
        if not path.is_file():
            continue
        name_lower = path.name.lower()

        # 확장자 결정: .json.template → .json
        stem = name_lower
        for ext in [".template"]:
            if stem.endswith(ext):
                stem = stem[: -len(ext)]

        if stem.endswith((".ts", ".js", ".tsx", ".jsx")):
            skipped += 1
            continue

        text = ctx.read(path)
        rel = path.relative_to(REPO_ROOT)

        # Placeholder 치환: {{...}} → 빈 문자열 (템플릿 파일은 순수 파싱 불가)
        import re as _re
        text_clean = _re.sub(r"\{\{[^}]*\}\}", "", text)

        if stem.endswith(".json"):
            try:
                json.loads(text_clean)
                parsed += 1
            except json.JSONDecodeError as exc:
                failures.append(f"FAIL {rel}: JSON parse error — {exc}")
        elif stem.endswith((".yaml", ".yml")):
            try:
                yaml.safe_load(text_clean)
                parsed += 1
            except yaml.YAMLError as exc:
                failures.append(f"FAIL {rel}: YAML parse error — {exc}")
        elif stem.endswith(".toml"):
            try:
                tomllib.loads(text_clean)
                parsed += 1
            except tomllib.TOMLDecodeError as exc:
                failures.append(f"FAIL {rel}: TOML parse error — {exc}")
        else:
            skipped += 1

    parts = []
    if parsed:
        parts.append(f"{parsed} parsed")
    if skipped:
        parts.append(f"{skipped} skipped (ts/js)")
    summary_base = ", ".join(parts) if parts else "0 files"

    if failures:
        result.status = "FAIL"
        result.summary = f"{summary_base} — {len(failures)} FAIL"
        result.details = failures
    else:
        result.status = "OK"
        result.summary = f"{summary_base} — OK"
    return result


# ---------------------------------------------------------------------------
# V3 Cross-reference 링크
# V3 — see harness/docs/guides/plugin-validation-guide.md §3.3
# ---------------------------------------------------------------------------

def _body_without_code_blocks(body: str) -> str:
    """마크다운 본문에서 코드 블록(``` ... ```) 내용을 공백으로 제거한다.
    코드 블록 안의 grep 패턴 등이 링크로 오인되는 false-positive를 방지한다.
    """
    lines = body.splitlines(keepends=True)
    result_lines: list[str] = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_block = not in_block
            result_lines.append("\n")  # fence 줄 자체도 제거
        elif in_block:
            result_lines.append("\n")  # 블록 내용 공백으로 대체
        else:
            result_lines.append(line)
    return "".join(result_lines)


def check_v3_refs(ctx: CheckContext) -> CheckResult:
    """SKILL.md 본문의 상대 경로 링크가 실제로 존재하는지 검증한다."""
    result = CheckResult("V3", "refs")
    skill_files = sorted(ctx.kit_path.glob("skills/*/SKILL.md"))
    total_links = 0
    failures: list[str] = []

    for skill_path in skill_files:
        text = ctx.read(skill_path)
        _, body = parse_frontmatter(text)
        # 코드 블록 내부는 링크 검사 제외 (정규식 패턴 등 false-positive 방지)
        search_body = _body_without_code_blocks(body)
        for match in LINK_PATTERN.finditer(search_body):
            raw_path = match.group(1).strip()
            # 절대 URL 제외
            if raw_path.startswith(("http://", "https://", "/")):
                continue
            # 순수 앵커 제외
            if raw_path.startswith("#"):
                continue
            # 정규식 OR 패턴 제외 (파이프 포함 경로는 실제 파일 경로가 아님)
            if "|" in raw_path:
                continue
            # 파일 확장자 없고 공백/특수문자 포함시 텍스트로 간주
            if " " in raw_path or "\n" in raw_path:
                continue
            # 대문자 플레이스홀더 제외 (예: [출처명](URL), [링크](PATH))
            # 확장자 없는 순수 대문자 단어는 템플릿 예시 텍스트로 간주
            if re.match(r'^[A-Z_]+$', raw_path):
                continue
            total_links += 1
            resolved = (skill_path.parent / raw_path).resolve()
            if not resolved.exists():
                line_no = search_body[: match.start()].count("\n") + 1
                rel = skill_path.relative_to(REPO_ROOT)
                failures.append(f"FAIL {rel}:{line_no} → {raw_path} (not found)")

    if failures:
        result.status = "FAIL"
        result.summary = f"{total_links} links, {len(failures)} BROKEN"
        result.details = failures
    else:
        result.status = "OK"
        result.summary = f"{total_links} links — OK"
    return result


# ---------------------------------------------------------------------------
# V4 Trigger 키워드
# V4 — see harness/docs/guides/plugin-validation-guide.md §3.4
# ---------------------------------------------------------------------------

def check_v4_triggers(ctx: CheckContext) -> CheckResult:
    """description 에서 따옴표 키워드를 추출하여 킷 내부 중복을 검출한다."""
    result = CheckResult("V4", "triggers")
    skill_files = sorted(ctx.kit_path.glob("skills/*/SKILL.md"))
    keyword_map: dict[str, list[str]] = {}

    for skill_path in skill_files:
        text = ctx.read(skill_path)
        fm, _ = parse_frontmatter(text)
        if not fm:
            continue
        desc = str(fm.get("description", ""))
        skill_name = skill_path.parent.name
        for m in KEYWORD_PATTERN.finditer(desc):
            kw = m.group(1).lower().strip()
            if len(kw) < 3:
                continue
            keyword_map.setdefault(kw, []).append(skill_name)

    total = sum(len(v) for v in keyword_map.values())
    duplicates: list[str] = []
    for kw, skills in keyword_map.items():
        if len(skills) > 1:
            duplicates.append(f"WARN \"{kw}\" — {', '.join(skills)}")

    # 외부 킷 교차 중복 체크 (all_keywords 제공 시)
    # Context disambiguation: 두 kit 모두 description 에 kit-specific
    # 고유 단어(KIT_CONTEXT_TOKENS)를 포함하면 exact-match cross-kit 겹침은
    # 의도된 "같은 개념 다른 프레임워크" 패턴으로 간주하여 WARN 에서 제외.
    if ctx.all_keywords:
        self_context_hit = ctx.all_context_hits.get(ctx.kit_path.name, False)
        for kw, skills in keyword_map.items():
            for other_kit, other_kws in ctx.all_keywords.items():
                if other_kit == ctx.kit_path.name:
                    continue
                if kw in other_kws:
                    other_context_hit = ctx.all_context_hits.get(other_kit, False)
                    if self_context_hit and other_context_hit:
                        # 양쪽 모두 kit-specific context 보유 → disambiguation 성공
                        continue
                    duplicates.append(
                        f"WARN \"{kw}\" — {ctx.kit_path.name} / {other_kit} (cross-kit)"
                    )

    unique_kws = len(keyword_map)
    if duplicates:
        result.status = "WARN"
        result.summary = f"{unique_kws} keywords, {len(duplicates)} duplicate"
        result.details = duplicates
    else:
        result.status = "OK"
        result.summary = f"{unique_kws} keywords — OK"
    return result


# ---------------------------------------------------------------------------
# V5 Placeholders
# V5 — see harness/docs/guides/plugin-validation-guide.md §3.5
# ---------------------------------------------------------------------------

def check_v5_placeholders(ctx: CheckContext) -> CheckResult:
    """SKILL.md, agents, README, references 에 TODO/TBD/FIXME 가 없는지 검증한다."""
    result = CheckResult("V5", "placeholders")
    failures: list[str] = []
    checked_files: list[Path] = []

    for glob_pat in PLACEHOLDER_GLOBS:
        checked_files.extend(sorted(ctx.kit_path.glob(glob_pat)))

    for path in checked_files:
        text = ctx.read(path)
        lines = text.splitlines()
        file_hits: list[tuple[int, str]] = []
        for lineno, line in enumerate(lines, start=1):
            if PLACEHOLDER_PATTERN.search(line):
                file_hits.append((lineno, line.strip()))

        if file_hits:
            rel = path.relative_to(REPO_ROOT)
            if ctx.fix:
                new_lines = []
                for line in lines:
                    new_line = line
                    for pat, replacement in FIX_PLACEHOLDER_RULES:
                        new_line = pat.sub(replacement, new_line)
                    new_lines.append(new_line)
                path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                ctx.invalidate(path)
                failures.append(f"FIXED {rel}: {len(file_hits)} placeholder(s) replaced")
            else:
                for lineno, snippet in file_hits:
                    failures.append(f"FAIL {rel}:{lineno} — {snippet[:80]}")

    if failures:
        result.status = "WARN" if ctx.fix else "FAIL"
        result.summary = f"{len(failures)} found{' (fixed)' if ctx.fix else ''}"
        result.details = failures
    else:
        result.status = "OK"
        result.summary = "0 found — OK"
    return result


# ---------------------------------------------------------------------------
# V6 Code fence 언어 힌트
# V6 — see harness/docs/guides/plugin-validation-guide.md §3.6
# ---------------------------------------------------------------------------

def check_v6_code_fence(ctx: CheckContext) -> CheckResult:
    """마크다운 코드 블록 여는 fence 에 언어 힌트가 있는지 검증한다."""
    result = CheckResult("V6", "code-fence")
    md_files: list[Path] = []
    md_files.extend(ctx.kit_path.glob("skills/*/SKILL.md"))
    md_files.extend(ctx.kit_path.glob("agents/*.md"))
    md_files.extend(ctx.kit_path.glob("references/*.md"))
    if (ctx.kit_path / "README.md").exists():
        md_files.append(ctx.kit_path / "README.md")

    failures: list[str] = []

    for path in sorted(set(md_files)):
        text = ctx.read(path)
        lines = text.splitlines()
        in_block = False
        file_hits: list[int] = []

        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                if not in_block:
                    hint = stripped[3:].strip()
                    if not hint:
                        file_hits.append(lineno)
                    in_block = True
                else:
                    in_block = False

        if file_hits:
            rel = path.relative_to(REPO_ROOT)
            if ctx.fix:
                new_lines = list(lines)
                for lineno in file_hits:
                    idx = lineno - 1
                    indent = len(new_lines[idx]) - len(new_lines[idx].lstrip())
                    new_lines[idx] = " " * indent + "```text"
                path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                ctx.invalidate(path)
                failures.append(f"FIXED {rel}: {len(file_hits)} bare fence(s) → ```text")
            else:
                for lineno in file_hits:
                    failures.append(f"FAIL {rel}:{lineno} — bare ``` (no language hint)")

    if failures:
        result.status = "WARN" if ctx.fix else "FAIL"
        result.summary = f"{len(failures)} bare{' (fixed)' if ctx.fix else ''}"
        result.details = failures
    else:
        result.status = "OK"
        result.summary = "0 bare — OK"
    return result


# ---------------------------------------------------------------------------
# V7 plugin.json ↔ marketplace.json 정합성
# V7 — see harness/docs/guides/plugin-validation-guide.md §3.7
# ---------------------------------------------------------------------------

def check_v7_plugin_json(ctx: CheckContext) -> CheckResult:
    """plugin.json 버전과 marketplace.json 버전 태그를 비교한다."""
    result = CheckResult("V7", "plugin-json")
    plugin_json_path = ctx.kit_path / ".claude-plugin" / "plugin.json"

    if not plugin_json_path.exists():
        result.status = "FAIL"
        result.summary = ".claude-plugin/plugin.json 없음"
        return result

    try:
        plugin_data = json.loads(ctx.read(plugin_json_path))
    except json.JSONDecodeError as exc:
        result.status = "FAIL"
        result.summary = f"plugin.json parse error — {exc}"
        return result

    plugin_version = plugin_data.get("version", "")

    # marketplace 에서 이 킷 찾기
    kit_name = ctx.kit_path.name
    market_entry = next(
        (p for p in ctx.marketplace_data.get("plugins", []) if p.get("name") == kit_name),
        None,
    )

    if market_entry is None:
        result.status = "WARN"
        result.summary = f"marketplace.json 에 '{kit_name}' 없음"
        return result

    market_desc = market_entry.get("description", "")
    m = MARKETPLACE_VERSION_PATTERN.search(market_desc)

    if not m:
        result.status = "FAIL"
        result.summary = "marketplace description 에 [vX.Y.Z · YYYY-MM-DD] 태그 없음"
        return result

    market_version = m.group(1)
    if plugin_version != market_version:
        result.status = "FAIL"
        result.summary = (
            f"버전 불일치 — plugin.json: v{plugin_version}, marketplace: v{market_version}"
        )
        result.details = [
            f"FAIL {plugin_json_path.relative_to(REPO_ROOT)}: {plugin_version} ≠ {market_version}"
        ]
        return result

    result.status = "OK"
    result.summary = f"v{plugin_version} matches marketplace — OK"
    return result


# ---------------------------------------------------------------------------
# V8 Hook 스크립트 실행 비트 — hooks.json 이 직접 실행하는 .sh 는 mode 0755 여야 한다
# V8 — see harness/docs/guides/plugin-validation-guide.md §3.8
# ---------------------------------------------------------------------------

# ${CLAUDE_PLUGIN_ROOT}/<relative>.sh 추출용. 인터프리터(bash/sh/source) 접두 여부도 함께 판정.
HOOK_SCRIPT_PATTERN = re.compile(r'\$\{CLAUDE_PLUGIN_ROOT\}/(\S+?\.sh)')


def _is_direct_exec(command: str, script_ref: str) -> bool:
    """command 가 스크립트를 인터프리터 없이 직접 실행하는지 판정.

    `${CLAUDE_PLUGIN_ROOT}/x.sh` 가 명령의 첫 토큰(또는 ;/&&/| 직후 첫 토큰)이면
    직접 실행 → exec 비트 필수. `bash ${...}/x.sh` 처럼 인터프리터가 앞서면 불필요.
    """
    marker = "${CLAUDE_PLUGIN_ROOT}/" + script_ref
    idx = command.find(marker)
    if idx < 0:
        return False
    prefix = command[:idx]
    # 직전 토큰 경계 추출 (마지막 셸 구분자 이후)
    for sep in (";", "&&", "||", "|", "\n"):
        prefix = prefix.rsplit(sep, 1)[-1]
    return prefix.strip() == ""


def check_v8_hook_exec(ctx: CheckContext) -> CheckResult:
    """hooks.json 이 직접 실행하는 .sh 스크립트의 실행 비트(0755)를 검증한다.

    근거: hooks.json 의 `${CLAUDE_PLUGIN_ROOT}/scripts/x.sh` 직접 실행 명령은
    스크립트가 git mode 100644(비실행)로 커밋되면 모든 설치본에서 SessionStart·
    PreToolUse hook 이 'Permission denied' 로 실패한다. 2026-06 reflect 집계상
    24개 프로젝트 957건(전체 friction 38%)의 단일 근본원인이었다.
    """
    result = CheckResult("V8", "hook-exec")
    hooks_json = ctx.kit_path / "hooks" / "hooks.json"

    if not hooks_json.exists():
        result.status = "OK"
        result.summary = "no hooks.json — OK"
        return result

    try:
        hooks_data = json.loads(ctx.read(hooks_json))
    except json.JSONDecodeError as exc:
        result.status = "FAIL"
        result.summary = f"hooks.json parse error — {exc}"
        return result

    # 모든 event → matcher → hooks → command 순회하여 command 문자열 수집
    commands: list[str] = []
    for event_entries in hooks_data.get("hooks", {}).values():
        if not isinstance(event_entries, list):
            continue
        for entry in event_entries:
            for hook in entry.get("hooks", []):
                cmd = hook.get("command", "")
                if cmd:
                    commands.append(cmd)

    checked = 0
    failures: list[str] = []
    for cmd in commands:
        for script_ref in HOOK_SCRIPT_PATTERN.findall(cmd):
            if not _is_direct_exec(cmd, script_ref):
                continue  # 인터프리터 경유 — exec 비트 불필요
            checked += 1
            script_path = ctx.kit_path / script_ref
            rel = script_path.relative_to(REPO_ROOT)
            if not script_path.exists():
                failures.append(f"FAIL {rel}: hooks.json 참조 스크립트 없음")
                continue
            mode = script_path.stat().st_mode
            if not (mode & 0o111):
                failures.append(
                    f"FAIL {rel}: 직접 실행 hook 스크립트가 비실행 (mode {oct(mode & 0o777)} — chmod +x 필요)"
                )

    if failures:
        result.status = "FAIL"
        result.summary = f"{len(failures)}개 hook 스크립트 실행 비트 누락"
        result.details = failures
        return result

    result.status = "OK"
    result.summary = (
        f"{checked} hook 스크립트 실행 가능 — OK" if checked else "직접 실행 hook 스크립트 없음 — OK"
    )
    return result


# ---------------------------------------------------------------------------
# CHECK_REGISTRY + validate_kit
# ---------------------------------------------------------------------------

CHECK_REGISTRY: dict[str, Callable[[CheckContext], CheckResult]] = {
    "frontmatter": check_v1_frontmatter,
    "templates": check_v2_templates,
    "refs": check_v3_refs,
    "triggers": check_v4_triggers,
    "placeholders": check_v5_placeholders,
    "code-fence": check_v6_code_fence,
    "plugin-json": check_v7_plugin_json,
    "hook-exec": check_v8_hook_exec,
}


def validate_kit(ctx: CheckContext, enabled_checks: set[str]) -> PluginResult:
    """단일 킷에 대해 활성화된 체크를 모두 실행한다."""
    result = PluginResult(ctx.kit_path.name, ctx.kit_path)
    for name, fn in CHECK_REGISTRY.items():
        if name in enabled_checks:
            result.checks.append(fn(ctx))
    return result


# ---------------------------------------------------------------------------
# 출력
# ---------------------------------------------------------------------------

def print_human(results: list[PluginResult]) -> None:
    """사람이 읽기 좋은 형식으로 출력한다."""
    for pr in results:
        print(f"\n=== {pr.name} ===")
        for cr in pr.checks:
            label = f"  {cr.check_id} {cr.label:<16}"
            print(f"{label}{cr.summary}")
            for detail in cr.details:
                print(f"    {detail}")

    total = len(results)
    n_ok = sum(1 for r in results if r.overall_status == "OK")
    n_warn = sum(1 for r in results if r.overall_status == "WARNING")
    n_error = sum(1 for r in results if r.overall_status == "ERROR")

    parts = [f"{total} plugins"]
    if n_ok:
        parts.append(f"{n_ok} OK")
    if n_warn:
        parts.append(f"{n_warn} WARNING")
    if n_error:
        parts.append(f"{n_error} ERROR")
    print(f"\nTotal: {', '.join(parts)}")
    print(f"Exit: {resolve_exit_code(results)}")


def print_json_output(results: list[PluginResult]) -> None:
    """CI 용 JSON 출력."""
    output = {
        "plugins": [r.to_dict() for r in results],
        "summary": {
            "total": len(results),
            "ok": sum(1 for r in results if r.overall_status == "OK"),
            "warning": sum(1 for r in results if r.overall_status == "WARNING"),
            "error": sum(1 for r in results if r.overall_status == "ERROR"),
        },
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Claude Code 플러그인 8-카테고리 검증 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "체크 이름: frontmatter, templates, refs, triggers, "
            "placeholders, code-fence, plugin-json, hook-exec\n"
            "가이드: harness/docs/guides/plugin-validation-guide.md"
        ),
    )
    parser.add_argument(
        "plugin",
        nargs="?",
        help="특정 킷 이름 (생략 시 전체 킷)",
    )
    parser.add_argument(
        "--check",
        metavar="LIST",
        help="실행할 체크 목록 (쉼표 구분, 예: frontmatter,refs)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 출력 (CI 용)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="자동 수정 모드 — V5 placeholders 와 V6 bare fence 만 수정",
    )
    return parser


def resolve_exit_code(results: list[PluginResult]) -> int:
    statuses = {r.overall_status for r in results}
    if "ERROR" in statuses:
        return 2
    if "WARNING" in statuses:
        return 1
    return 0


def _collect_cross_kit_keywords(
    marketplace_data: dict,
) -> tuple[dict[str, set[str]], dict[str, bool]]:
    """V4 cross-kit 중복 검출용 전체 킷 키워드 사전 수집.

    Returns:
        (all_kit_keywords, all_context_hits)
        - all_kit_keywords: kit 이름 → 해당 kit 의 description 에서 추출한 trigger 키워드 집합
        - all_context_hits: kit 이름 → kit-specific context token 포함 여부 (bool)
          (KIT_CONTEXT_TOKENS 에 정의된 고유 단어를 description 전체에서 발견하면 True)
    """
    all_kit_keywords: dict[str, set[str]] = {}
    all_context_hits: dict[str, bool] = {}
    for kit_path in list_kits(marketplace_data):
        kws: set[str] = set()
        full_desc = ""
        for sf in kit_path.glob("skills/*/SKILL.md"):
            text = read_text(sf)
            fm, _ = parse_frontmatter(text)
            if fm:
                desc = str(fm.get("description", ""))
                full_desc += " " + desc.lower()
                for m in KEYWORD_PATTERN.finditer(desc):
                    kw = m.group(1).lower().strip()
                    if len(kw) >= 3:
                        kws.add(kw)
        all_kit_keywords[kit_path.name] = kws
        context_tokens = KIT_CONTEXT_TOKENS.get(kit_path.name, set())
        all_context_hits[kit_path.name] = any(
            tok.lower() in full_desc for tok in context_tokens
        )
    return all_kit_keywords, all_context_hits


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        marketplace_data = load_marketplace()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: marketplace.json 로드 실패 — {exc}", file=sys.stderr)
        sys.exit(2)

    # 검증 대상 킷 목록 결정
    all_kits = list_kits(marketplace_data)

    if args.plugin:
        target_kits = [k for k in all_kits if k.name == args.plugin]
        if not target_kits:
            available = ", ".join(k.name for k in all_kits)
            print(f"ERROR: '{args.plugin}' 킷을 찾을 수 없습니다. 사용 가능: {available}", file=sys.stderr)
            sys.exit(2)
    else:
        target_kits = all_kits

    # 활성 체크 결정
    all_check_names = set(CHECK_REGISTRY.keys())
    if args.check:
        requested = {c.strip() for c in args.check.split(",")}
        unknown = requested - all_check_names
        if unknown:
            print(f"ERROR: 알 수 없는 체크 이름 {sorted(unknown)}", file=sys.stderr)
            sys.exit(2)
        enabled_checks = requested
    else:
        enabled_checks = all_check_names

    # V4 cross-kit 검증용 전체 킷 키워드 + context hit 사전 수집
    all_kit_keywords: dict[str, set[str]] = {}
    all_context_hits: dict[str, bool] = {}
    if "triggers" in enabled_checks and len(target_kits) > 1:
        all_kit_keywords, all_context_hits = _collect_cross_kit_keywords(marketplace_data)

    # 킷별 검증 실행
    results: list[PluginResult] = []
    for kit_path in target_kits:
        ctx = CheckContext(
            kit_path=kit_path,
            marketplace_data=marketplace_data,
            fix=args.fix,
            all_keywords=all_kit_keywords,
            all_context_hits=all_context_hits,
        )
        results.append(validate_kit(ctx, enabled_checks))

    # 출력
    if args.json:
        print_json_output(results)
    else:
        print_human(results)

    sys.exit(resolve_exit_code(results))


if __name__ == "__main__":
    main()
