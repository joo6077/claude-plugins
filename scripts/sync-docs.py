#!/usr/bin/env python3
"""README 자동 동기화 스크립트.

SKILL.md / agent .md frontmatter, hooks.json, scripts/*.sh, evals/, references/,
plugin.json, marketplace.json에서 데이터를 읽어 README의
<!-- AUTO:xxx --> 마커 사이를 갱신한다.

Usage:
    python scripts/sync-docs.py              # 전체 동기화
    python scripts/sync-docs.py harness      # 특정 플러그인만
    python scripts/sync-docs.py --check-only # 변경 필요 여부만 확인
    python scripts/sync-docs.py --dry-run    # 변경 예정 내용 출력, 파일 미수정
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

import plugin_utils
from plugin_utils import read_text, load_marketplace, list_kits, parse_frontmatter_raw, REPO_ROOT

# Windows cp949 stdout 대응
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True,
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True,
    )

ROOT = REPO_ROOT

MARKER_RE = re.compile(
    r"(<!-- AUTO:(\w+) -->)\n(.*?)(<!-- /AUTO:\2 -->)",
    re.DOTALL,
)


# ── Task 1: 핵심 유틸리티 함수 ───────────────────────────────────────

def _parse_frontmatter_file(path: Path) -> dict | None:
    """파일을 읽고 plugin_utils.parse_frontmatter_raw 로 frontmatter 를 파싱한다.

    description block scalar(`>`) 는 첫 indent 줄만 추출된다 — README 테이블
    한 줄 요약에 맞춘 동작. 경고 출력은 이 wrapper 가 담당한다.
    """
    text = read_text(path)
    if not text:
        print(f"  [경고] 파일 읽기 실패: {path}", file=sys.stderr)
        return None
    data = parse_frontmatter_raw(text)
    if data is None:
        print(f"  [경고] 프론트매터 없음, 스킵: {path}", file=sys.stderr)
    return data


def first_line(text: str | None) -> str:
    """멀티라인 설명에서 첫 줄을 추출한다."""
    if not text:
        return ""
    return text.split("\n")[0].strip()


def replace_markers(text: str, replacements: dict[str, str]) -> str:
    """<!-- AUTO:key --> ... <!-- /AUTO:key --> 사이를 교체한다."""
    def _sub(m: re.Match) -> str:
        open_tag = m.group(1)
        key = m.group(2)
        close_tag = m.group(4)
        if key in replacements:
            return f"{open_tag}\n{replacements[key]}{close_tag}"
        return m.group(0)
    return MARKER_RE.sub(_sub, text)


def has_marker(text: str, key: str) -> bool:
    """마커 쌍이 존재하는지 확인한다."""
    return f"<!-- AUTO:{key} -->" in text and f"<!-- /AUTO:{key} -->" in text


# ── Task 2: 데이터 수집 함수 ─────────────────────────────────────────

def collect_skills(plugin_dir: Path) -> list[dict]:
    """skills/*/SKILL.md에서 name, description을 수집한다."""
    results = []
    for skill_md in plugin_utils.iter_skills(plugin_dir):
        data = _parse_frontmatter_file(skill_md)
        if data:
            results.append({
                "name": data.get("name", ""),
                "description": first_line(data.get("description", "")),
            })
    return results


def collect_agents(plugin_dir: Path) -> list[dict]:
    """agents/*.md에서 name, description, model, tools를 수집한다."""
    results = []
    for agent_md in plugin_utils.iter_agents(plugin_dir):
        data = _parse_frontmatter_file(agent_md)
        if data:
            results.append({
                "name": data.get("name", ""),
                "description": first_line(data.get("description", "")),
                "model": data.get("model", ""),
                "tools": data.get("tools", ""),
            })
    return results


def collect_hooks(plugin_dir: Path) -> list[dict]:
    """hooks/hooks.json에서 event, command, matcher를 수집한다."""
    hooks_file = plugin_dir / "hooks" / "hooks.json"
    if not hooks_file.is_file():
        return []
    try:
        raw = json.loads(hooks_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [경고] hooks.json 파싱 실패: {hooks_file} ({e})", file=sys.stderr)
        return []

    results = []
    hooks_map = raw.get("hooks", {})
    for event, entries in hooks_map.items():
        for entry in entries:
            matcher = entry.get("matcher", "")
            for hook in entry.get("hooks", []):
                cmd = hook.get("command", "")
                # 스크립트 이름만 추출
                cmd_name = cmd.split("/")[-1] if "/" in cmd else cmd
                results.append({
                    "event": event,
                    "command": cmd_name,
                    "matcher": matcher,
                })
    return results


def collect_scripts(plugin_dir: Path) -> list[dict]:
    """scripts/*.sh에서 name, description(2번째 줄 주석)을 수집한다."""
    scripts_dir = plugin_dir / "scripts"
    if not scripts_dir.is_dir():
        return []
    results = []
    for script_file in sorted(scripts_dir.glob("*.sh")):
        desc = ""
        try:
            lines = script_file.read_text(encoding="utf-8").split("\n")
            if len(lines) > 1:
                # # ── Description ── 패턴
                dm = re.match(r"^#\s*──\s*(.+?)\s*──\s*$", lines[1])
                if dm:
                    desc = dm.group(1)
                elif lines[1].startswith("#"):
                    desc = lines[1].lstrip("# ").strip()
        except Exception:
            pass
        results.append({
            "name": script_file.name,
            "description": desc,
        })
    return results


def collect_evals(plugin_dir: Path) -> list[dict]:
    """evals/ 디렉토리의 파일/하위 디렉토리를 수집한다."""
    evals_dir = plugin_dir / "evals"
    if not evals_dir.is_dir():
        return []
    results = []
    for item in sorted(evals_dir.iterdir()):
        if item.name.startswith("."):
            continue
        results.append({
            "name": item.name,
            "is_dir": item.is_dir(),
        })
    return results


def collect_references(plugin_dir: Path) -> list[dict]:
    """references/ 디렉토리의 파일을 수집한다."""
    refs_dir = plugin_dir / "references"
    if not refs_dir.is_dir():
        return []
    results = []
    for ref_file in sorted(refs_dir.iterdir()):
        if not ref_file.is_file():
            continue
        desc = ""
        try:
            text = ref_file.read_text(encoding="utf-8")
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith("# "):
                    desc = line[2:].strip()
                    break
        except Exception:
            pass
        results.append({
            "name": ref_file.name,
            "description": desc,
        })
    return results


def load_plugin_json(plugin_dir: Path) -> dict | None:
    """plugin.json을 로드한다."""
    pj = plugin_dir / ".claude-plugin" / "plugin.json"
    if not pj.exists():
        return None
    return json.loads(pj.read_text(encoding="utf-8"))


# ── Task 3: 테이블 렌더러 ───────────────────────────────────────────

def render_skills_table(skills: list[dict]) -> str:
    lines = ["| 스킬 | 설명 |", "|------|------|"]
    for s in skills:
        lines.append(f"| `{s['name']}` | {s['description']} |")
    return "\n".join(lines) + "\n"


def render_agents_table(agents: list[dict]) -> str:
    lines = ["| 에이전트 | 설명 |", "|----------|------|"]
    for a in agents:
        lines.append(f"| `{a['name']}` | {a['description']} |")
    return "\n".join(lines) + "\n"


def render_hooks_table(hooks: list[dict]) -> str:
    lines = ["| 이벤트 | 실행 | 설명 |", "|--------|------|------|"]
    for h in hooks:
        matcher_info = f" (matcher: {h['matcher']})" if h["matcher"] else ""
        desc = f"{h['event']}{matcher_info}"
        lines.append(f"| `{h['event']}` | `{h['command']}` | {desc} |")
    return "\n".join(lines) + "\n"


def render_scripts_table(scripts: list[dict]) -> str:
    lines = ["| 스크립트 | 설명 |", "|----------|------|"]
    for s in scripts:
        lines.append(f"| `{s['name']}` | {s['description']} |")
    return "\n".join(lines) + "\n"


def render_evals_table(evals: list[dict]) -> str:
    lines = ["| 파일 | 설명 |", "|------|------|"]
    for e in evals:
        kind = "디렉토리" if e["is_dir"] else "파일"
        lines.append(f"| `{e['name']}` | {kind} |")
    return "\n".join(lines) + "\n"


def render_references_table(refs: list[dict]) -> str:
    lines = ["| 파일 | 설명 |", "|------|------|"]
    for r in refs:
        lines.append(f"| `{r['name']}` | {r['description']} |")
    return "\n".join(lines) + "\n"


def render_plugins_table() -> str:
    """루트 README용 플러그인 테이블."""
    mp = load_marketplace()
    mp_descs: dict[str, str] = {}
    for p in mp.get("plugins", []):
        mp_descs[p["name"]] = p.get("description", "")

    stacks = {"harness": "범용", "flutter-toolkit": "Flutter", "design-kit": "범용"}
    lines = ["| 플러그인 | 버전 | 스택 | 설명 |", "|----------|------|------|------|"]
    for kit_path in list_kits(mp):
        name = kit_path.name
        pj = load_plugin_json(kit_path)
        version = pj["version"] if pj else "?"
        desc = mp_descs.get(name, "") or (pj["description"] if pj else "")
        stack = stacks.get(name, "범용")
        lines.append(
            f"| [`{name}`](./{name}/) | v{version} | {stack} | {desc} |"
        )
    return "\n".join(lines) + "\n"


def render_update_commands() -> str:
    """루트 README용 plugin update 명령 (marketplace.json 순서)."""
    mp = load_marketplace()
    lines = ["```bash"]
    for p in mp.get("plugins", []):
        lines.append(f"claude plugin update {p['name']}@joo6077-plugins")
    lines.append("```")
    return "\n".join(lines) + "\n"


def render_uninstall_commands() -> str:
    """루트 README용 plugin uninstall 명령."""
    mp = load_marketplace()
    lines = ["```bash"]
    for p in mp.get("plugins", []):
        lines.append(f"claude plugin uninstall {p['name']}@joo6077-plugins")
    lines.append("```")
    return "\n".join(lines) + "\n"


def render_release_commands() -> str:
    """루트 README용 release.sh 명령."""
    mp = load_marketplace()
    lines = ["```bash", "# 플러그인별 버전 bump + git tag + push"]
    for p in mp.get("plugins", []):
        lines.append(f"bash scripts/release.sh {p['name']} patch")
    lines.append("```")
    return "\n".join(lines) + "\n"


def render_summary_list() -> str:
    """CLAUDE.md용 플러그인 요약 리스트."""
    desc_map = {
        "harness": "스택 무관 범용 QA 프레임워크 (Sprint Contract + QA Evaluator)",
        "flutter-toolkit": "Flutter 전용 개발 워크플로우 스킬",
        "design-kit": "스택 무관 UI/UX 디자인 플러그인 (디자인 시스템 세팅 + 실시간 가이드 + 감사)",
    }
    lines = []
    for kit_path in list_kits():
        name = kit_path.name
        pj = load_plugin_json(kit_path)
        skill_count = len(collect_skills(kit_path))
        base = desc_map.get(name, pj["description"] if pj else "")
        if name == "flutter-toolkit" and skill_count > 0:
            desc = f"{base} {skill_count}종"
        else:
            desc = base
        lines.append(f"- **{name}** — {desc}")
    return "\n".join(lines) + "\n"


# ── Task 3 (계속): README 동기화 ─────────────────────────────────────

def process_readme(
    readme_path: Path,
    replacements: dict[str, str],
    *,
    dry_run: bool = False,
    check_only: bool = False,
) -> bool:
    """README를 읽고 마커를 교체한다. 변경 있으면 True 반환."""
    if not readme_path.exists():
        print(f"  [경고] README 없음: {readme_path}", file=sys.stderr)
        return False

    original = readme_path.read_text(encoding="utf-8")

    # 마커 존재 확인 — 없는 마커는 경고만 하고 스킵
    for key in replacements:
        if not has_marker(original, key):
            print(f"  [경고] 마커 <!-- AUTO:{key} --> 없음, 스킵: {readme_path.name}", file=sys.stderr)

    updated = replace_markers(original, replacements)
    changed = updated != original

    if check_only:
        status = "변경 필요" if changed else "동기화됨"
        print(f"  {readme_path.relative_to(ROOT)}: {status}")
        return changed

    if dry_run:
        if changed:
            print(f"\n--- {readme_path.relative_to(ROOT)} ---")
            for key, content in replacements.items():
                if has_marker(original, key):
                    print(f"  [AUTO:{key}]")
                    for line in content.strip().split("\n"):
                        print(f"    {line}")
        else:
            print(f"  {readme_path.relative_to(ROOT)}: 변경 없음")
        return changed

    if changed:
        readme_path.write_text(updated, encoding="utf-8")
        print(f"  갱신: {readme_path.relative_to(ROOT)}")
    else:
        print(f"  변경 없음: {readme_path.relative_to(ROOT)}")

    return changed


def sync_plugin(plugin_name: str, *, dry_run: bool, check_only: bool) -> bool:
    """플러그인 README 동기화."""
    plugin_dir = ROOT / plugin_name
    readme = plugin_dir / "README.md"

    print(f"\n[{plugin_name}]")

    replacements: dict[str, str] = {}

    # 스킬 테이블
    skills = collect_skills(plugin_dir)
    if skills:
        replacements["skills"] = render_skills_table(skills)

    # 에이전트 테이블
    agents = collect_agents(plugin_dir)
    if agents:
        replacements["agents"] = render_agents_table(agents)

    # 훅 테이블
    hooks = collect_hooks(plugin_dir)
    if hooks:
        replacements["hooks"] = render_hooks_table(hooks)

    # 스크립트 테이블
    scripts = collect_scripts(plugin_dir)
    if scripts:
        replacements["scripts"] = render_scripts_table(scripts)

    # Evals 테이블
    evals = collect_evals(plugin_dir)
    if evals:
        replacements["evals"] = render_evals_table(evals)

    # 레퍼런스 테이블
    refs = collect_references(plugin_dir)
    if refs:
        replacements["references"] = render_references_table(refs)

    if not replacements:
        print("  데이터 없음")
        return False

    return process_readme(readme, replacements, dry_run=dry_run, check_only=check_only)


# ── Task 4: 루트 README + CLAUDE.md ─────────────────────────────────

def sync_root(*, dry_run: bool, check_only: bool) -> bool:
    """루트 README.md의 AUTO 마커들을 갱신한다 (plugins / update-cmd / uninstall-cmd / release-cmd)."""
    print("\n[root README]")
    replacements = {
        "plugins": render_plugins_table(),
        "update-cmd": render_update_commands(),
        "uninstall-cmd": render_uninstall_commands(),
        "release-cmd": render_release_commands(),
    }
    return process_readme(
        ROOT / "README.md", replacements, dry_run=dry_run, check_only=check_only
    )


def sync_claude_md(*, dry_run: bool, check_only: bool) -> bool:
    """CLAUDE.md의 AUTO:summary 마커를 갱신한다."""
    print("\n[CLAUDE.md]")
    replacements = {"summary": render_summary_list()}
    return process_readme(
        ROOT / "CLAUDE.md", replacements, dry_run=dry_run, check_only=check_only
    )


# ── Task 5: CLI ──────────────────────────────────────────────────────

def main() -> None:
    kit_paths = list_kits()
    kit_names = [k.name for k in kit_paths]

    parser = argparse.ArgumentParser(description="README 자동 동기화")
    parser.add_argument("plugin", nargs="?", help="특정 플러그인만 동기화")
    parser.add_argument("--check-only", action="store_true", help="변경 필요 여부만 확인")
    parser.add_argument("--dry-run", action="store_true", help="변경 예정 내용 출력, 파일 미수정")
    args = parser.parse_args()

    any_changed = False

    if args.plugin:
        if args.plugin not in kit_names:
            print(f"알 수 없는 플러그인: {args.plugin}", file=sys.stderr)
            print(f"사용 가능: {', '.join(kit_names)}", file=sys.stderr)
            sys.exit(1)
        changed = sync_plugin(
            args.plugin, dry_run=args.dry_run, check_only=args.check_only
        )
        any_changed = any_changed or changed
    else:
        for name in kit_names:
            changed = sync_plugin(name, dry_run=args.dry_run, check_only=args.check_only)
            any_changed = any_changed or changed

    # 루트 README + CLAUDE.md는 항상 동기화
    changed = sync_root(dry_run=args.dry_run, check_only=args.check_only)
    any_changed = any_changed or changed

    changed = sync_claude_md(dry_run=args.dry_run, check_only=args.check_only)
    any_changed = any_changed or changed

    if args.check_only:
        if any_changed:
            print("\n동기화가 필요합니다. `python scripts/sync-docs.py`를 실행하세요.")
            sys.exit(1)
        else:
            print("\n모든 README가 동기화 상태입니다.")


if __name__ == "__main__":
    main()
