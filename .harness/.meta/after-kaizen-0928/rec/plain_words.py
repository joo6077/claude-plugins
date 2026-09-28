"""main 커밋 메시지 가운데 쉬운 말 목록(~/.claude/rules/plain-korean.md) 낱말이 든 것을 찾는다.

    python3 plain_words.py scan  [--tip 판]  → 커밋 해시 · 걸린 낱말 · 바꿔 쓸 말(TSV)
    python3 plain_words.py note  <해시>      → 그 커밋에 달 메모 본문
    python3 plain_words.py check [--tip 판]  → 걸린 커밋마다 메모가 있고 바꿔 쓸 말을 다 담았는지. 어긋난 줄 + 요약

가리기와 낱말 판정은 ~/.claude/hooks/check-plain-korean.sh 의 1) 단계와 같은 식이다.
그 훅은 답변 글을 읽으므로 여기서는 같은 식을 커밋 메시지에 적용한다. 대문자 약자 검사(2) 단계)는 뺀다.
"""
import argparse
import importlib.util
import os
import re
import subprocess
import sys

GLOSSARY = os.path.expanduser("~/.claude/rules/plain-korean.md")
LOADER = os.path.expanduser("~/.claude/hooks/_plain-korean-glossary.py")
DEFAULT_TIP = "01b1cac"
HANGUL = r"가-힣"
NOTE_HEAD = "쉬운 말 정정(2026-09-28) — 목록의 뜻으로 쓴 자리에만 해당한다. 출력물 표면처럼 일상 뜻으로 쓴 자리는 그대로 둔다:"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def load_pairs():
    spec = importlib.util.spec_from_file_location("glossary", LOADER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load(GLOSSARY)["pairs"]


def blank(match):
    return " " * len(match.group(0))


def mask(text):
    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", blank, text, flags=re.S)
    text = re.sub(r"`([^`\n]*)`", lambda code: code.group(0) if re.search("[" + HANGUL + "]", code.group(1)) else blank(code), text)
    text = re.sub(r"https?://\S+", blank, text)
    text = re.sub(r"\]\([^)\s]+\)", blank, text)
    text = re.sub(r"[~./]?[\w.-]*/[\w./-]+", blank, text)
    return re.sub(r"\b[A-Za-z_][\w-]*\.[A-Za-z][\w]{0,4}\b", blank, text)


def hits(text, pairs):
    masked, found, seen = mask(text), [], set()
    for key, repl in pairs:
        if key in seen:
            continue
        if re.fullmatch(r"[\x00-\x7f]+", key):
            hit = re.search(r"(?<![\w-])" + re.escape(key) + r"(?![\w-])", masked, re.I)
            # 로마자 낱말은 괄호로 한국어 뜻을 붙였으면 넘어간다
            if hit and re.search(re.escape(key) + r"\s*[（(][^)）]*[" + HANGUL + r"][^)）]*[）)]", masked, re.I):
                seen.add(key)
                continue
        else:
            hit = re.search(r"(?<![" + HANGUL + r"])" + re.escape(key), masked)
        if hit:
            seen.add(key)
            found.append((key, repl))
    return found


def scan(tip, pairs):
    for sha in git("rev-list", tip).split():
        found = hits(git("log", "-1", "--format=%B", sha), pairs)
        if found:
            yield sha, found


def note_body(found):
    return "\n".join([NOTE_HEAD] + [f"- 「{key}」 → {repl}" for key, repl in found])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["scan", "note", "check"])
    parser.add_argument("sha", nargs="?")
    parser.add_argument("--tip", default=DEFAULT_TIP)
    args = parser.parse_args()
    pairs = load_pairs()
    if args.mode == "note":
        print(note_body(hits(git("log", "-1", "--format=%B", args.sha), pairs)))
        return 0
    rows = list(scan(args.tip, pairs))
    if args.mode == "scan":
        for sha, found in rows:
            print("\t".join([sha, ",".join(k for k, _ in found), " | ".join(r for _, r in found)]))
        return 0
    bad = 0
    for sha, found in rows:
        shown = subprocess.run(["git", "notes", "show", sha], capture_output=True, text=True)
        missing = [key for key, repl in found if f"「{key}」 → {repl}" not in shown.stdout]
        if shown.returncode != 0 or missing:
            bad += 1
            print("\t".join([sha, "no-note" if shown.returncode else "missing:" + ",".join(missing)]))
    print(f"SUMMARY commits={len(rows)} bad={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
