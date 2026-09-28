#!/usr/bin/env python3
"""evals.json gate_cases 에 G5 표 모양 일곱 가지가 FAIL 기대로 등록됐는지 센다 (B6).

쓰임: python3 b6-registered.py <setup-guide evals 폴더>
모양마다 「그 모양을 담은 픽스처 + expect 에 G5_BLOCKING FAIL 줄」 인 사례 수를 찍는다.
끝 줄: SHAPES covered=<n>/7 crlf_cases=<CRLF 픽스처를 쓰는 새 모양 사례 수> cases=<전체 사례 수>
종료 코드: 0 일곱 모양 모두 1 건 이상 · 1 빠진 모양 있음 · 2 읽기 실패
"""
import json, os, re, sys

d = sys.argv[1]
try:
    cases = json.load(open(os.path.join(d, "evals.json"), encoding="utf-8"))["gate_cases"]
except Exception as e:
    print(f"STOP evals.json 읽기 실패 {e}")
    sys.exit(2)
WORDS = ("요구", "출처", "막히는 것", "우회")


def header_like(line):
    return all(w in line for w in WORDS) and "|" in line


SHAPES = {
    "lead-space": lambda ls: any(re.match(r"^ {1,3}\|", l) and header_like(l) for l in ls),
    "nbsp-head": lambda ls: any(header_like(l) and " " in l for l in ls),
    "ideo-head": lambda ls: any(header_like(l) and "　" in l for l in ls),
    "nbsp-cell": lambda ls: any(re.search(r"\| +\|?\s*$", l) or "| |" in l for l in ls),
    "bold-head": lambda ls: any(header_like(l) and "**요구**" in l for l in ls),
    "quote": lambda ls: any(re.match(r"^\s*>\s*\|", l) and header_like(l) for l in ls),
    "unrecognized": lambda ls: any(header_like(l) and re.sub(r"^[\s>]*", "", l).strip().strip("|").count("|") >= 4 for l in ls),
}
count = {k: 0 for k in SHAPES}
crlf = 0
for c in cases:
    if not any(x.startswith("G5_BLOCKING FAIL") for x in c.get("expect", [])):
        continue
    raw = open(os.path.join(d, c["fixture"]), "rb").read()
    text = raw.decode("utf-8")
    ls = [l.rstrip("\r") for l in text.split("\n")]
    hit = [k for k, f in SHAPES.items() if f(ls)]
    for k in hit:
        count[k] += 1
    if hit and b"\r\n" in raw:
        crlf += 1
    if hit:
        print(f"CASE {c['id']} {c['fixture']} shapes={','.join(hit)}{' crlf' if b'\r\n' in raw else ''}")
for k, v in count.items():
    print(f"SHAPE {k} {v}")
cov = sum(1 for v in count.values() if v)
print(f"SHAPES covered={cov}/7 crlf_cases={crlf} cases={len(cases)}")
sys.exit(0 if cov == 7 else 1)
