#!/usr/bin/env python3
"""카이젠 회귀 패턴(assertions.json)을 실제로 돌린다.

    python3 scripts/run-kaizen-assertions.py

harness/evals/kaizen/<카이젠>/assertions.json 을 모두 찾아 패턴마다 대상 파일을 읽고 한 줄씩 찍는다.
형식은 {픽스처 이름: [{"type": "file_contains", "file": <레포 기준 경로>, "pattern": <정규식>}]} 이고,
키는 같은 폴더 fixture-feedback-data/<키>.yaml 과 하나씩 짝을 이뤄야 한다.

    PASS <카이젠>/<키>#<n> <대상 파일> (<맞은 수>건)
    FAIL <카이젠>/<키>#<n> <대상 파일> (0건)          패턴이 사라졌다
    FAIL <카이젠>/<키>: <짝 어긋남>                    픽스처와 키 한쪽만 있다
    UNREADABLE <무엇>: <원인>                         JSON · type · 대상 파일 · 정규식을 못 읽음

exit 0 전부 통과 · 1 FAIL 있음 · 2 못 읽은 입력 있음 (나머지는 끝까지 재고 알린다).
"""
from __future__ import annotations

import json
import re
import sys

from plugin_utils import REPO_ROOT

KAIZEN_EVALS = REPO_ROOT / "harness" / "evals" / "kaizen"
KNOWN_TYPES = ("file_contains",)


def main() -> int:
    assertion_files = sorted(KAIZEN_EVALS.glob("*/assertions.json"))
    if not assertion_files:
        print(f"UNREADABLE {KAIZEN_EVALS.relative_to(REPO_ROOT)}: 아래에 assertions.json 이 0 개")
        return 2

    lines: list[str] = []
    passed = failed = unreadable = 0
    for assertion_file in assertion_files:
        kaizen = assertion_file.parent.name
        try:
            patterns_by_key = json.loads(assertion_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            lines.append(f"UNREADABLE {assertion_file.relative_to(REPO_ROOT)}: JSON 을 못 읽음 — {exc}")
            unreadable += 1
            continue
        if not isinstance(patterns_by_key, dict):
            lines.append(f"UNREADABLE {assertion_file.relative_to(REPO_ROOT)}: 맨 위가 {{키: 목록}} 꼴이 아니다")
            unreadable += 1
            continue

        fixtures = {path.stem for path in (assertion_file.parent / "fixture-feedback-data").glob("*.yaml")}
        for key in sorted(fixtures - patterns_by_key.keys()):
            lines.append(f"FAIL {kaizen}/{key}: 픽스처는 있는데 회귀 패턴이 없다")
            failed += 1
        for key in sorted(patterns_by_key.keys() - fixtures):
            lines.append(f"FAIL {kaizen}/{key}: 회귀 패턴은 있는데 픽스처가 없다")
            failed += 1

        for key, assertions in patterns_by_key.items():
            if not isinstance(assertions, list):
                lines.append(f"UNREADABLE {kaizen}/{key}: 값이 목록이 아니다")
                unreadable += 1
                continue
            for index, assertion in enumerate(assertions, 1):
                label = f"{kaizen}/{key}#{index}"
                if not isinstance(assertion, dict) or not {"type", "file", "pattern"} <= assertion.keys():
                    lines.append(f"UNREADABLE {label}: type · file · pattern 세 칸이 다 있어야 한다")
                    unreadable += 1
                    continue
                if assertion["type"] not in KNOWN_TYPES:
                    lines.append(f"UNREADABLE {label}: 모르는 type '{assertion['type']}' — 아는 것 {', '.join(KNOWN_TYPES)}")
                    unreadable += 1
                    continue
                target = REPO_ROOT / assertion["file"]
                try:
                    text = target.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError) as exc:
                    lines.append(f"UNREADABLE {label}: 대상 파일을 못 읽음 {assertion['file']} — {exc.__class__.__name__}")
                    unreadable += 1
                    continue
                try:
                    hits = len(re.findall(assertion["pattern"], text))
                except re.error as exc:
                    lines.append(f"UNREADABLE {label}: 정규식을 못 읽음 — {exc}")
                    unreadable += 1
                    continue
                if hits:
                    lines.append(f"PASS {label} {assertion['file']} ({hits}건)")
                    passed += 1
                else:
                    lines.append(f"FAIL {label} {assertion['file']} (0건)")
                    failed += 1

    print("\n".join(lines))
    print(f"Total: {passed} passed, {failed} failed" + (f", {unreadable} unreadable" if unreadable else ""))
    if unreadable:
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
