#!/usr/bin/env python3
"""인사이트 처리 배정표를 검사한다.

    python3 scripts/check-insights-tracking.py [--final] .claude/kaizen-input/insights-report.md

기본: frontmatter 의 generated·report_file, 필수 열, 모든 행의 배정 값.
--final: 배정이 `Phase N` 인 행마다 대상 계약 칸(계약 슬러그)과 QA 칸(APPROVE·REJECT)까지 본다.
         슬러그 안의 Phase 번호(`-p06-` · `phase12`)가 배정의 N 과 같아야 하고, 번호를 못 읽는 슬러그도 통과시키지 않는다.

exit 0 통과 · 1 위반 · 2 파일이나 표를 못 읽음.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_COLUMNS = ("항목", "배정", "대상 계약", "QA")
DISPOSITION = re.compile(r"이번 스프린트|Phase\s*\d+|기각|해당 없음")
PHASE = re.compile(r"Phase\s*(\d+)")
SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")
SLUG_PHASE = re.compile(r"(?:^|-)p(?:hase)?0*(\d+)[a-z]?(?=-|$)")
VERDICTS = ("APPROVE", "REJECT")
SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body)]


def read_frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"^---\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and key and not key[0].isspace():
            fields[key.strip()] = value.strip()
    return fields


def table_blocks(lines: list[str]) -> list[list[tuple[int, str]]]:
    blocks, current, in_fence = [], [], False
    for no, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_fence = not in_fence
        if not in_fence and line.startswith("|"):
            current.append((no, line))
            continue
        if current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def main() -> int:
    ap = argparse.ArgumentParser(description="인사이트 처리 배정표 검사")
    ap.add_argument("--final", action="store_true",
                    help="Phase 행의 대상 계약·QA 칸까지 채워졌는지 본다 (카이젠 Final)")
    ap.add_argument("path", type=Path)
    args = ap.parse_args()

    try:
        text = args.path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"UNREADABLE 파일을 못 읽음: {args.path}: {exc}")
        return 2
    if not text.strip():
        print(f"UNREADABLE 빈 파일: {args.path}")
        return 2

    problems: list[str] = []
    unreadable: list[str] = []

    fm = read_frontmatter(text)
    if fm is None:
        problems.append("frontmatter 없음")
    else:
        for key in ("generated", "report_file"):
            if not fm.get(key):
                problems.append(f"frontmatter {key} 없음")

    tracked = [b for b in table_blocks(text.splitlines())
               if {"대상 계약", "QA"} <= set(split_row(b[0][1]))]
    if not tracked:
        print("UNREADABLE 머리에 '대상 계약' 과 'QA' 열이 있는 표를 못 찾음")
        return 2

    counts: dict[str, int] = {}
    final_missing = 0
    for block in tracked:
        head_no, head_line = block[0]
        header = split_row(head_line)
        if len(block) < 2 or not SEPARATOR.match(block[1][1]):
            unreadable.append(f"{head_no}행 표: 머리 다음 줄이 구분선이 아니다")
            continue
        rows = block[2:]
        if not rows:
            unreadable.append(f"{head_no}행 표: 데이터 행이 0 개")
            continue
        missing = [c for c in REQUIRED_COLUMNS if c not in header]
        if missing:
            # 배정 열이 빠지면 행 검사를 건너뛰게 되므로 그 사실을 따로 남긴다
            problems.append(f"{head_no}행 표: 필수 열 없음 {', '.join(missing)} — 행 {len(rows)} 개 검사 못 함")
            continue
        col = {name: header.index(name) for name in REQUIRED_COLUMNS}
        for no, line in rows:
            cells = split_row(line)
            if len(cells) != len(header):
                unreadable.append(f"{no}행: 칸 {len(cells)} 개, 머리는 {len(header)} 개")
                continue
            item, disp = cells[col["항목"]], cells[col["배정"]]
            if not item:
                problems.append(f"{no}행: 항목 칸이 비었다")
            if not DISPOSITION.fullmatch(disp):
                problems.append(f"{no}행 {item or '?'}: 배정 '{disp}' 가 이번 스프린트·Phase N·기각·해당 없음 중 하나가 아니다")
                continue
            kind = "Phase" if PHASE.fullmatch(disp) else disp
            counts[kind] = counts.get(kind, 0) + 1
            if args.final and kind == "Phase":
                contract, qa = cells[col["대상 계약"]], cells[col["QA"]]
                bad = []
                slug_phase = SLUG_PHASE.search(contract)
                if not SLUG.fullmatch(contract):
                    bad.append(f"대상 계약 '{contract}'")
                elif not slug_phase:
                    bad.append(f"대상 계약 '{contract}' 에서 Phase 번호를 못 읽음")
                elif int(slug_phase.group(1)) != int(PHASE.fullmatch(disp).group(1)):
                    bad.append(f"대상 계약 '{contract}' 는 Phase {int(slug_phase.group(1))} 슬러그")
                if qa not in VERDICTS:
                    bad.append(f"QA '{qa}'")
                if bad:
                    final_missing += 1
                    problems.append(f"{no}행 {item} ({disp}): {' · '.join(bad)} — 배정과 같은 Phase 번호의 슬러그와 APPROVE·REJECT 가 필요하다")

    for p in problems:
        print(p)
    for u in unreadable:
        print(f"UNREADABLE {u}")
    summary = " · ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    mode = "final" if args.final else "basic"
    print(f"mode={mode} tables={len(tracked)} 배정: {summary or '없음'}"
          + (f" · Phase 행 미완료 {final_missing}" if args.final else ""))
    if unreadable:
        print("TRACKING_TABLE_UNREADABLE")
        return 2
    if problems:
        print("TRACKING_TABLE_FAIL")
        return 1
    print("TRACKING_TABLE_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
