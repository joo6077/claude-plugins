#!/usr/bin/env python3
"""두 판 사이에 md 파일의 뜻이 바뀌지 않았는지 잰다.

사용: meaning.py <저장소> <기준 판> <새 판> <파일 목록> [notes 파일]
      meaning.py --selftest

모양 표식(공백 · 빈 줄 · 표 구분 줄 · 코드 블록 언어 · 제목 표식 · 줄 전체 강조 ·
빈 인용 줄 · URL 꺾쇠 · markdownlint 주석)을 떼고 공백을 모두 지운 글자열이 두 판에서 같아야 한다.

출력 줄:
  MISMATCH <경로>           뜻이 바뀐 파일
  FRONTMATTER <경로>        첫 앞머리 블록이 한 글자라도 다르다
  CODEBLOCK <경로>          코드 블록 속 줄이 한 글자라도 다르다 (여는 줄의 언어는 보지 않는다)
  HEADING <경로>:<줄> ...   새 판에서 단계가 바뀌었거나 새로 생긴 제목
  DISABLE <경로>:<줄> ...   새로 넣은 markdownlint 끄기 주석
  BADDISABLE <경로>:<줄> .. 허용하지 않는 꼴의 끄기 주석 (파일 전체 · 규칙 없음 · 짝 없는 disable)
  NOTES_MISSING <경로>:<줄> notes 에 그 자리가 없다 (notes 파일을 줬을 때만)
  CHECKED=<n> MISMATCH=<n> FRONTMATTER=<n> CODEBLOCK=<n> HEADING=<n> DISABLE=<n> BADDISABLE=<n> NOTES_MISSING=<n>
종료 코드: 0 잼 · 2 판이나 파일을 못 읽음
"""
import re
import subprocess
import sys
from collections import Counter

LINT_COMMENT = re.compile(r"^\s*<!--\s*markdownlint-[a-z-]+.*-->\s*$")
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*[\w+#.-]*\s*$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
EMPH_LINE = re.compile(r"^\s*(\*\*|__|\*|_)(.+?)(\*\*|__|\*|_)\s*:?\s*$")
EMPTY_QUOTE = re.compile(r"^\s*(>\s*)+$")
ANGLE_URL = re.compile(r"<((?:https?|ftp)://[^>\s]+)>")
DISABLE = re.compile(r"<!--\s*markdownlint-(disable|enable|disable-next-line|disable-line|disable-file|enable-file|configure-file|capture|restore)\b([^>]*)-->")


def normalize(text):
    out = []
    for line in text.split("\n"):
        if LINT_COMMENT.match(line) or TABLE_SEP.match(line) and "-" in line or EMPTY_QUOTE.match(line):
            continue
        m = FENCE.match(line)
        if m:
            out.append(m.group(2)[0] * 3)
            continue
        m = HEADING.match(line)
        if m:
            line = m.group(2)
        m = EMPH_LINE.match(line)
        if m:
            line = m.group(2)
        line = ANGLE_URL.sub(r"\1", line)
        out.append(line)
    return re.sub(r"\s+", "", "".join(out))


def headings(text):
    res, fence = [], None
    for no, line in enumerate(text.split("\n"), 1):
        m = FENCE.match(line)
        if m:
            ch = m.group(2)[0]
            if fence is None:
                fence = ch
            elif fence == ch:
                fence = None
            continue
        if fence:
            continue
        m = HEADING.match(line)
        if m:
            res.append((no, len(m.group(1)), re.sub(r"\s+", " ", m.group(2))))
    return res


def frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return ""
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[: i + 1])
    return "\n".join(lines)


def code_bodies(text):
    bodies, fence, cur = [], None, []
    for line in text.split("\n"):
        m = FENCE.match(line)
        if m and (fence is None or m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence)):
            if fence is None:
                fence, cur = m.group(2), []
            else:
                bodies.append("\n".join(cur))
                fence = None
            continue
        if fence is not None:
            cur.append(line)
    return bodies


def disables(text):
    return [(no, line.strip()) for no, line in enumerate(text.split("\n"), 1) if DISABLE.search(line)]


def noted(notes, path, no):
    """notes 에 `- <경로>:<줄> … — <이유>` 꼴의 줄이 있는가 (이유는 네 글자 이상)."""
    pat = r"^- " + re.escape(f"{path}:{no}") + r"(?!\d)\s.*—\s*\S.{3,}$"
    return re.search(pat, notes, re.MULTILINE) is not None


def show(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8")


def check_file(path, old, new, notes, out):
    counts = Counter()
    if normalize(old) != normalize(new):
        out.append(f"MISMATCH {path}")
        counts["MISMATCH"] += 1
    if frontmatter(old) != frontmatter(new):
        out.append(f"FRONTMATTER {path}")
        counts["FRONTMATTER"] += 1
    if code_bodies(old) != code_bodies(new):
        out.append(f"CODEBLOCK {path}")
        counts["CODEBLOCK"] += 1
    old_h = Counter((lv, t) for _, lv, t in headings(old))
    old_levels = {}
    for _, lv, t in headings(old):
        old_levels.setdefault(t, lv)
    seen = Counter()
    for no, lv, t in headings(new):
        seen[(lv, t)] += 1
        if seen[(lv, t)] > old_h[(lv, t)]:
            out.append(f"HEADING {path}:{no} {old_levels.get(t, '없음')}->{lv} {t}")
            counts["HEADING"] += 1
            if notes is not None and not noted(notes, path, no):
                out.append(f"NOTES_MISSING {path}:{no}")
                counts["NOTES_MISSING"] += 1
    old_d = Counter(t for _, t in disables(old))
    seen_d = Counter()
    new_d = disables(new)
    for no, t in new_d:
        seen_d[t] += 1
        if seen_d[t] <= old_d[t]:
            continue
        out.append(f"DISABLE {path}:{no} {t}")
        counts["DISABLE"] += 1
        m = DISABLE.search(t)
        kind, rules = m.group(1), m.group(2).strip()
        bad = ""
        if kind not in ("disable-next-line", "disable", "enable"):
            bad = "허용 밖 종류"
        elif not re.match(r"^(MD\d{3}\b[\s,]*)+", rules):
            bad = "규칙 번호 없음"
        elif kind == "disable":
            rs = set(re.findall(r"MD\d{3}", rules))
            later = [x for n2, x in new_d if n2 > no and DISABLE.search(x).group(1) == "enable"]
            if not any(set(re.findall(r"MD\d{3}", x)) == rs for x in later):
                bad = "짝 enable 없음"
        if bad:
            out.append(f"BADDISABLE {path}:{no} {bad}")
            counts["BADDISABLE"] += 1
        if notes is not None and not noted(notes, path, no):
            out.append(f"NOTES_MISSING {path}:{no}")
            counts["NOTES_MISSING"] += 1
    return counts


def summary(checked, counts):
    keys = ["MISMATCH", "FRONTMATTER", "CODEBLOCK", "HEADING", "DISABLE", "BADDISABLE", "NOTES_MISSING"]
    return f"CHECKED={checked} " + " ".join(f"{k}={counts[k]}" for k in keys)


def selftest():
    base = "# 제목\n\n| a | b |\n|---|---|\n| 1 | 2 |\n```\nx=1\n```\n**굵은 줄**\n- 목록\n본문 http://a.b/c 끝\n"
    cases = [
        ("모양만", "# 제목\n\n| a   | b   |\n| --- | --- |\n| 1   | 2   |\n\n```text\nx=1\n```\n\n#### 굵은 줄\n\n- 목록\n\n본문 <http://a.b/c> 끝\n", 0, 1),
        ("낱말 바꿈", base.replace("목록", "명단"), 1, 0),
        ("순서 바꿈", base.replace("| 1 | 2 |", "| 2 | 1 |"), 1, 0),
        ("끄기 주석", "<!-- markdownlint-disable-next-line MD041 -->\n" + base, 0, 0),
    ]
    ok = True
    for name, new, want_mis, want_head in cases:
        out = []
        c = check_file("t.md", base, new, None, out)
        got = (c["MISMATCH"], c["HEADING"])
        flag = "OK" if got == (want_mis, want_head) else "BAD"
        ok &= flag == "OK"
        print(f"{flag} {name} mismatch={got[0]} heading={got[1]} 기대={want_mis},{want_head}")
    fm = "---\nname: x\nlist:\n  - a\n---\n"
    for name, new, key in [("앞머리 들여쓰기", fm.replace("  - a", "    - a") + base, "FRONTMATTER"),
                           ("코드 속 들여쓰기", base.replace("x=1", "  x=1"), "CODEBLOCK")]:
        old = fm + base if key == "FRONTMATTER" else base
        c = check_file("t.md", old, new, None, [])
        flag = "OK" if c[key] == 1 and c["MISMATCH"] == 0 else "BAD"
        ok &= flag == "OK"
        print(f"{flag} {name} {key.lower()}={c[key]} mismatch={c['MISMATCH']} 기대=1,0")
    out = []
    c = check_file("t.md", base, "<!-- markdownlint-disable MD033 -->\n" + base, None, out)
    flag = "OK" if c["BADDISABLE"] == 1 else "BAD"
    ok &= flag == "OK"
    print(f"{flag} 짝 없는 disable baddisable={c['BADDISABLE']} 기대=1")
    out = []
    c = check_file("t.md", base, "<!-- markdownlint-disable-file MD033 -->\n" + base, None, out)
    flag = "OK" if c["BADDISABLE"] == 1 else "BAD"
    ok &= flag == "OK"
    print(f"{flag} 파일 전체 끄기 baddisable={c['BADDISABLE']} 기대=1")
    new = "<!-- markdownlint-disable-next-line MD041 -->\n" + base
    for name, notes, want in [("notes 있음", "- t.md:1 MD041 — 첫 줄 제목을 읽는 스크립트가 있다\n", 0),
                              ("notes 이유 없음", "- t.md:1 MD041\n", 1),
                              ("notes 다른 줄", "- t.md:12 MD041 — 첫 줄 제목을 읽는다\n", 1)]:
        c = check_file("t.md", base, new, notes, [])
        flag = "OK" if c["NOTES_MISSING"] == want else "BAD"
        ok &= flag == "OK"
        print(f"{flag} {name} notes_missing={c['NOTES_MISSING']} 기대={want}")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv):
    if argv[1:2] == ["--selftest"]:
        return selftest()
    if len(argv) < 5:
        print(__doc__)
        return 2
    repo, a, b, lst = argv[1:5]
    notes = None
    if len(argv) > 5:
        with open(argv[5], encoding="utf-8") as f:
            notes = f.read()
    with open(lst, encoding="utf-8") as f:
        paths = [p.strip() for p in f if p.strip()]
    out, counts, checked = [], Counter(), 0
    for p in paths:
        old, new = show(repo, a, p), show(repo, b, p)
        if old is None or new is None:
            print(f"STOP 못 읽음 {a if old is None else b}:{p}")
            return 2
        counts.update(check_file(p, old, new, notes, out))
        checked += 1
    print("\n".join(out)) if out else None
    print(summary(checked, counts))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
