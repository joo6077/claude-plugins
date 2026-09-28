"""lineref.py find 목록을 줄 내용으로 따로 확인한다. 줄 번호 계산 코드를 쓰지 않는다.

    python3 lineref.py find | python3 content_check.py [--base 판]

moved 인 줄: 옛 판의 옛 줄과 기준 판의 새 줄이 글자까지 같아야 한다.
changed 인 줄: 둘이 달라야 한다 (같으면 moved 로 적었어야 한다).
어긋난 줄을 출력하고 끝에 요약 한 줄. 어긋남이 있으면 종료 코드 1.
"""
import argparse
import re
import subprocess
import sys

cache = {}


def lines_of(rev, path):
    if (rev, path) not in cache:
        cache[(rev, path)] = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout.split("\n")
    return cache[(rev, path)]


def first_line(ref):
    return int(re.split(r"[-–~]", ref.rsplit(":", 1)[1])[0])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="e500a63")
    args = parser.parse_args()
    counts, bad = {"moved": 0, "changed": 0}, 0
    for row in sys.stdin:
        record, no, old_ref, new_ref, target, kind, zone, view = row.rstrip("\n").split("\t")
        same = lines_of(view, target)[first_line(old_ref) - 1] == lines_of(args.base, target)[first_line(new_ref) - 1]
        counts[kind] = counts.get(kind, 0) + 1
        if same != (kind == "moved"):
            bad += 1
            print("\t".join(["mismatch", record, no, old_ref, new_ref, kind]))
    print(f"SUMMARY moved={counts['moved']} changed={counts['changed']} bad={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
