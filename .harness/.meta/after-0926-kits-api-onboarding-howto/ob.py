#!/usr/bin/env python3
"""ob.py <evals.json> — onboarding-kit gate_cases 를 읽어 KO-1 · KO-2 조건 값을 한 줄씩 찍는다.

ko1        Step 하나에 출처 줄이 둘이고 출처 없는 Step 은 없는 픽스처를 G1_LEDGER FAIL 로 기대하는 사례 수
g5         기대 출력에 G5_BLOCKING 줄이 정확히 하나인 사례 수 · G5 FAIL 사례의 픽스처가 어떤 결함인지
"""
import json
import os
import sys

HEADER = ["요구", "출처", "막히는 것", "우회"]


def step_counts(text):
    counts, cur = [], None
    for line in text.split("\n"):
        if line.startswith("## "):
            if cur is not None:
                counts.append(cur)
            cur = 0 if line.startswith("## Step ") else None
        elif cur is not None and line.startswith("**출처:**"):
            cur += 1
    if cur is not None:
        counts.append(cur)
    return counts


def blocking_rows(text):
    lines, rows, inside = text.split("\n"), [], False
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else None
        if cells is None:
            inside = False
            continue
        if cells == HEADER:
            inside = True
            continue
        if inside and not all(set(c) <= set("-: ") for c in cells):
            rows.append(cells)
    return rows


def main():
    evals = sys.argv[1]
    base = os.path.dirname(evals)
    cases = json.load(open(evals, encoding="utf-8")).get("gate_cases") or []
    ko1 = []
    g5_one = g5_fail = empty_kind = nourl_kind = 0
    for c in cases:
        text = open(os.path.join(base, c["fixture"]), encoding="utf-8").read()
        sc = step_counts(text)
        g1_fail = any(e.startswith("G1_LEDGER FAIL") for e in c["expect"])
        if sc and max(sc) == 2 and min(sc) >= 1 and g1_fail:
            ko1.append(c["id"])
        g5 = [e for e in c["expect"] if e.startswith("G5_BLOCKING ")]
        if len(g5) == 1:
            g5_one += 1
        if g5 and g5[0].startswith("G5_BLOCKING FAIL"):
            g5_fail += 1
            rows = blocking_rows(text)
            if any(len(r) < 4 or any(x == "" for x in r[1:4]) for r in rows):
                empty_kind += 1
            if any(len(r) >= 2 and "http" not in r[1] for r in rows):
                nourl_kind += 1
    print(f"ko1_cases={len(ko1)} ids={','.join(ko1) or '-'}")
    print(f"cases={len(cases)} g5_one={g5_one} g5_fail_cases={g5_fail} empty_kind={empty_kind} nourl_kind={nourl_kind}")


if __name__ == "__main__":
    main()
