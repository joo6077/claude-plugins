"""lineref.py find 목록을 줄 내용으로 따로 확인한다 (2 회차). 줄 번호 계산 코드를 쓰지 않는다.

    python3 lineref.py find | python3 content_check.py [--base 판]

범위 참조는 첫 줄부터 끝 줄까지 덩어리로 맞댄다. 새 범위의 앞뒤가 뒤집히면 틀림이다.
moved: 빈 줄 · markdownlint 주석 줄을 뺀 옛 덩어리와 새 덩어리가 글자까지 같아야 한다(경고 정리가 범위 안에 넣은 줄이다). changed · quoted: 달라야 한다.
기록 줄의 인용문이 옛 덩어리에 있었으면 새 덩어리에도 있어야 한다 (unresolved 는 사람 확인 목록 몫이라 빼고 센다).
옛 덩어리가 빈 줄 · `>` 만 있는 줄뿐이면 무엇과도 같아 보이므로 「판정 못 함」 으로 따로 센다.
"""
import argparse
import re
import subprocess
import sys

QUOTE_RE = re.compile(r"`([^`]+)`|「([^」]+)」")
BLANKISH_RE = re.compile(r"^[ \t>]*$")
# 경고 정리가 범위 안에 넣은 줄: 빈 줄과 markdownlint 끄고 켜는 주석
LINT_INSERT_RE = re.compile(r"^[ \t>]*$|^[ \t]*<!-- markdownlint-[a-z-]+( [A-Za-z0-9 ,-]+)? -->[ \t]*$")

cache = {}


def lines_of(rev, path):
    if (rev, path) not in cache:
        cache[(rev, path)] = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout.split("\n")
    return cache[(rev, path)]


def numbers(ref):
    return [int(value) for value in re.findall(r"\d+", ref[ref.index(":"):])]


def quotes_in(line):
    found = []
    for match in QUOTE_RE.finditer(line):
        text = (match.group(1) or match.group(2)).strip()
        if len(text) >= 4 and ".md:" not in text and not re.fullmatch(r":[0-9`~–-]+", text):
            found.append(text)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="e500a63")
    args = parser.parse_args()
    counts, bad = {}, 0
    for row in sys.stdin:
        record, no, _, old_ref, new_ref, target, kind, zone, view = row.rstrip("\n").split("\t")
        counts[kind] = counts.get(kind, 0) + 1
        olds, news = numbers(old_ref), numbers(new_ref)
        problem = None
        if news != sorted(news):
            problem = "reversed-range"
        elif kind != "unresolved":
            old_block = lines_of(view, target)[olds[0] - 1:olds[-1]]
            new_block = lines_of(args.base, target)[news[0] - 1:news[-1]]
            if all(BLANKISH_RE.match(text) for text in old_block):
                counts["undecidable"] = counts.get("undecidable", 0) + 1
                continue
            record_line = lines_of(args.base, record)[int(no) - 1]
            held = [quote for quote in quotes_in(record_line) if any(quote in text for text in old_block)]
            same = [text for text in old_block if not LINT_INSERT_RE.match(text)] == [text for text in new_block if not LINT_INSERT_RE.match(text)]
            if same != (kind == "moved"):
                problem = "content-" + kind
            elif any(not any(quote in text for text in new_block) for quote in held):
                problem = "quote-lost"
        if problem:
            bad += 1
            print("\t".join([problem, record, no, old_ref, new_ref, kind]))
    print("SUMMARY " + " ".join(f"{key}={counts.get(key, 0)}" for key in ("moved", "changed", "quoted", "unresolved", "undecidable")) + f" bad={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
