#!/usr/bin/env python3
"""G5 표 모양 변형 입력 만들기 (B6).

쓰임: python3 b6-variants.py <setup-guide evals/fixtures 폴더> <출력 폴더>
원본 두 개(빈 칸이 있는 gate-fail-blocking-empty.md · 다 찬 gate-blocking-ok.md)와
표와 무관한 gate-ok-flutter.md 에서 모양만 바꾼 사본을 LF · CRLF 두 벌씩 쓴다.
  empty-<모양>[-crlf].md  — 빈 칸이 남아 있다 → G5 FAIL 이어야 한다
  ok-<모양>[-crlf].md     — 네 칸이 다 찼다 → G5 PASS rows=2 여야 한다
  plain-unrelated[-crlf].md — 막는 요구 표가 아닌 표 → G5 PASS rows=0 이어야 한다
"""
import os, sys

src_dir, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
H = "| 요구 | 출처 | 막히는 것 | 우회 |"


def read(name):
    with open(os.path.join(src_dir, name), encoding="utf-8") as f:
        return f.read()


def shapes(src, with_empty_only):
    lines = src.split("\n")

    def tbl(fn):
        return "\n".join(fn(l) if l.startswith("|") else l for l in lines)

    v = {
        "lead1": tbl(lambda l: " " + l),
        "lead3": tbl(lambda l: "   " + l),
        "nbsp-head": src.replace(H, "| 요구 | 출처 | 막히는 것 | 우회 |"),
        "ideo-head": src.replace(H, "|　요구　|　출처　|　막히는 것　|　우회　|"),
        "bold-head": src.replace(H, "| **요구** | **출처** | **막히는 것** | **우회** |"),
        "quote": tbl(lambda l: "> " + l),
    }
    if with_empty_only:
        v["nbsp-cell"] = src.replace("| APNs 키 구성 | |", "| APNs 키 구성 | |")
        v["five-col"] = src.replace(H, "| 요구 | 출처 | 막히는 것 | 우회 | 비고 |")
    return v


def write(name, text):
    with open(os.path.join(out, name + ".md"), "w", encoding="utf-8") as f:
        f.write(text)
    with open(os.path.join(out, name + "-crlf.md"), "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\n", "\r\n"))


n = 0
for prefix, name, empty in (("empty", "gate-fail-blocking-empty.md", True), ("ok", "gate-blocking-ok.md", False)):
    src = read(name)
    for k, text in shapes(src, empty).items():
        if text == src:
            sys.exit(f"STOP 변형이 안 먹었다: {prefix}-{k}")
        write(f"{prefix}-{k}", text)
        n += 2
plain = read("gate-ok-flutter.md") + "\n| 요구 사항 | 설명 |\n| --- | --- |\n| 로그인 | 계정이 있어야 한다 |\n"
write("plain-unrelated", plain)
n += 2
print(f"WROTE {n}")
