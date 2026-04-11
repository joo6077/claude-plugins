#!/usr/bin/env python3
"""
sync-orchestrator.py — marketplace.json 을 기반으로 kaizen-orchestrator SKILL.md 의
Phase 5~N 섹션을 자동 생성한다.

kit 을 추가/수정/삭제하면 이 스크립트를 실행하여 오케스트레이터가 자동으로 반영되도록 한다.
`--check-only` 모드는 drift 만 감지한다 (CI / hook 용).

Phase 1~4 는 harness 플러그인 전용 메타 Phase 이므로 이 스크립트의 관심 범위 밖이다.
이 스크립트는 `<!-- AUTO:plugin_phases:begin -->` ~ `<!-- AUTO:plugin_phases:end -->` 마커
사이 영역만 교체한다.

Usage:
    python3 scripts/sync-orchestrator.py              # 전체 동기화
    python3 scripts/sync-orchestrator.py --check-only # drift 감지만
    python3 scripts/sync-orchestrator.py --dry-run    # diff 미리보기
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
ORCHESTRATOR_SKILL = REPO_ROOT / ".claude" / "skills" / "kaizen-orchestrator" / "SKILL.md"

BEGIN_MARKER = "<!-- AUTO:plugin_phases:begin -->"
END_MARKER = "<!-- AUTO:plugin_phases:end -->"

# harness 는 Phase 1~4 전용 (meta Phase) 이므로 자동 생성 대상에서 제외
EXCLUDED_PLUGINS = {"harness"}

# Phase 5 부터 시작
FIRST_PLUGIN_PHASE = 5


def load_marketplace() -> list[dict]:
    data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    return data.get("plugins", [])


def filter_plugin_list(plugins: list[dict]) -> list[dict]:
    return [p for p in plugins if p.get("name") not in EXCLUDED_PLUGINS]


def generate_phase_sections(plugins: list[dict]) -> str:
    """Phase 5~N 섹션 Markdown 생성."""
    lines: list[str] = []
    lines.append(
        "<!-- 이 섹션은 scripts/sync-orchestrator.py 에 의해 자동 생성됩니다."
    )
    lines.append(
        "     marketplace.json 을 변경한 뒤 스크립트를 재실행하면 동기화됩니다."
    )
    lines.append("     직접 편집하지 마세요. -->")
    lines.append("")

    for idx, plugin in enumerate(plugins):
        phase_num = FIRST_PLUGIN_PHASE + idx
        step_num = phase_num  # Step 번호 = Phase 번호
        name = plugin.get("name", "unknown")
        description = plugin.get("description", "")

        # kaizen 스킬 이름은 관례상 `<kit>-kaizen` (flutter-toolkit 은 `flutter-kaizen` 예외)
        # marketplace 에 정의된 별도 필드가 없으면 간단한 매핑 룰 적용
        kaizen_skill_name = plugin.get("kaizen_skill") or infer_kaizen_skill(name)

        # 리서치 문서 소스 경로 기본값 추정
        research_docs_dir = plugin.get("research_docs_dir") or infer_research_docs_dir(name)

        lines.append(f"### Step {step_num}: Phase {phase_num} — {name} 카이젠")
        lines.append("")
        lines.append(f"**범위:** `{name}/skills/*/SKILL.md`, `{name}/references/`")
        if research_docs_dir:
            lines.append(f", `{research_docs_dir}` 리서치 문서")
        lines.append("")
        lines.append(
            f"공통 실행 패턴에 따라 `/{kaizen_skill_name}` 서브에이전트로 실행. "
            f"Phase 1 에서 설계 가이드가 변경되었으면 {name} 전 스킬을 전수 감사한다. "
            f"{name} 플러그인 전용 리서치는 해당 카이젠 스킬이 수행한다."
        )
        lines.append("")
        lines.append(f"> 플러그인 설명: {description}")
        lines.append("")

    lines.append(
        "<!-- /sync-orchestrator.py 자동 생성 끝. 다음 사이클 전에 marketplace.json 을 수정했으면 다시 실행하세요. -->"
    )

    return "\n".join(lines)


def infer_kaizen_skill(plugin_name: str) -> str:
    """플러그인 이름 → kaizen 스킬 이름.

    `flutter-toolkit` → `flutter-kaizen`
    `design-kit` → `design-kaizen`
    `rust-kit` → `rust-kaizen`
    `backend-kit` → `backend-kaizen`
    """
    base = plugin_name.replace("-toolkit", "").replace("-kit", "")
    return f"{base}-kaizen"


def infer_research_docs_dir(plugin_name: str) -> str | None:
    """플러그인 이름 → 리서치 문서 디렉토리 경로.

    `backend-kit` → `docs/backend/`
    `infra-kit` → `docs/infra/`
    `rust-kit` → `docs/rust/`
    `react-kit` → `docs/react/`
    `flutter-toolkit` → `docs/flutter/`
    `design-kit` → `design-kit/docs/design/`
    """
    mapping = {
        "backend-kit": "docs/backend/",
        "infra-kit": "docs/infra/",
        "rust-kit": "docs/rust/",
        "react-kit": "docs/react/",
        "flutter-toolkit": "docs/flutter/",
        "design-kit": "design-kit/docs/design/",
    }
    return mapping.get(plugin_name)


def replace_auto_section(content: str, new_section: str) -> str:
    begin_idx = content.find(BEGIN_MARKER)
    end_idx = content.find(END_MARKER)
    if begin_idx == -1 or end_idx == -1:
        raise RuntimeError(
            f"AUTO markers not found in {ORCHESTRATOR_SKILL}. "
            "Add `{BEGIN_MARKER}` and `{END_MARKER}` first."
        )
    before = content[: begin_idx + len(BEGIN_MARKER)]
    after = content[end_idx:]
    return before + "\n" + new_section + "\n" + after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="drift 만 감지. 변경 시 exit 1",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="변경 내용 미리보기 (파일 수정 안 함)",
    )
    args = parser.parse_args()

    if not MARKETPLACE_JSON.exists():
        print(f"ERROR: {MARKETPLACE_JSON} 가 없습니다.", file=sys.stderr)
        return 2
    if not ORCHESTRATOR_SKILL.exists():
        print(f"ERROR: {ORCHESTRATOR_SKILL} 가 없습니다.", file=sys.stderr)
        return 2

    plugins = load_marketplace()
    plugins = filter_plugin_list(plugins)

    new_section = generate_phase_sections(plugins)

    current = ORCHESTRATOR_SKILL.read_text(encoding="utf-8")

    try:
        updated = replace_auto_section(current, new_section)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if current == updated:
        print(f"sync-orchestrator: 이미 동기화됨 ({len(plugins)} plugins)")
        return 0

    if args.check_only:
        print(
            f"sync-orchestrator: DRIFT 감지 — `python3 scripts/sync-orchestrator.py` 실행 필요",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print("=== DRY RUN — 변경 예정 내용 ===")
        print(new_section)
        print("=== (파일 수정 없음) ===")
        return 0

    ORCHESTRATOR_SKILL.write_text(updated, encoding="utf-8")
    print(
        f"sync-orchestrator: {ORCHESTRATOR_SKILL} 동기화 완료 ({len(plugins)} plugins)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
