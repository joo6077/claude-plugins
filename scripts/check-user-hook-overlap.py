#!/usr/bin/env python3
"""개인 설정이 harness 플러그인 훅 둘을 아직 등록해 두 번 도는지 본다.

lint-contract-oracle.sh · qa-pending-check.sh 는 harness 플러그인 훅(harness/hooks/hooks.json)이 됐다.
예전처럼 ~/.claude/settings.json 에도 남아 있으면 같은 안내가 두 번 나온다 — 그 겹침을 이 맥에서 알린다.

사용법:
    python3 scripts/check-user-hook-overlap.py [--settings-dir <개인 설정 폴더>]

settings.json · settings.local.json 이 둘 다 없으면(CI) `개인 설정 없음 — 건너뜀` 한 줄을 찍고 0 으로 끝난다.
있는 파일의 훅 명령 가운데 두 훅 파일 이름이 든 것마다 `겹침: <설정 파일> <이벤트> <명령>` 줄을 찍고 1 로 끝난다.
겹침이 없으면 `겹침 없음 (설정 파일 N 개)` 한 줄과 0. 설정 파일을 못 읽거나 JSON 이 깨졌으면 `UNREADABLE <경로> (<까닭>)` 과 2.
"""

import argparse
import json
import sys
from pathlib import Path

PLUGIN_HOOKS = ["lint-contract-oracle.sh", "qa-pending-check.sh"]
SETTINGS_FILES = ["settings.json", "settings.local.json"]


def overlaps(path: Path, settings: dict) -> list[str]:
    found = []
    hooks = settings.get("hooks") if isinstance(settings, dict) else None
    for event, entries in (hooks or {}).items():
        for entry in entries if isinstance(entries, list) else []:
            for hook in entry.get("hooks", []) if isinstance(entry, dict) else []:
                command = hook.get("command", "") if isinstance(hook, dict) else ""
                if any(name in command for name in PLUGIN_HOOKS):
                    found.append(f"겹침: {path} {event} {command}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="개인 설정과 harness 플러그인 훅의 겹침 검사")
    parser.add_argument("--settings-dir", type=Path, default=Path.home() / ".claude")
    args = parser.parse_args()

    present = [args.settings_dir / name for name in SETTINGS_FILES if (args.settings_dir / name).is_file()]
    if not present:
        print("개인 설정 없음 — 건너뜀")
        return 0
    found, unreadable = [], []
    for path in present:
        try:
            settings = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            unreadable.append(f"UNREADABLE {path} ({type(error).__name__})")
            continue
        found += overlaps(path, settings)
    print("\n".join(found + unreadable) if found or unreadable else f"겹침 없음 (설정 파일 {len(present)} 개)")
    if found:
        print("harness 플러그인이 같은 훅을 이미 돌린다 — 개인 설정의 위 등록을 지워라")
    if unreadable:
        return 2
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
