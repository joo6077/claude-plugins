#!/usr/bin/env python3
"""cx3 (1) design-mockup 의 「Step N」 인용이 가리키는 절 제목과 뜻이 맞는지 잰다.

사용법: step-refs.py <판 뿌리 폴더>
두 파일(design-kit/skills/design-mockup/SKILL.md · docs/design-kit/design-mockup.html)에서 절 제목이 아닌
줄의 「Step N」 · 「Step N-x」 인용을 모두 찾는다. 인용이 든 문장에 아래 표의 고정 글자가 있으면 그 인용이
가리키는 절 제목에 짝 낱말이 있어야 한다. 표에 없는 문장의 인용은 unclassified 로 센다.
마지막 줄: "refs=<인용 수> ok=<맞음> bad=<어긋남> unclassified=<표에 없음>"
exit 0 = 셌다, 2 = 파일을 못 읽었거나 절 제목을 못 찾았다.
"""
import html
import re
import sys
from pathlib import Path

RULES = [  # (문장에 든 고정 글자, 가리킨 절 제목에 있어야 할 낱말)
    ("폐기 칸의 경로를 따라", "자동 감지"),
    (".design/approvals/", "승인 기록 생성"),
    ("대상 화면을 정한", "화면 요구사항"),
    ("매트릭스", "개수와 축"),
]
FILES = ["design-kit/skills/design-mockup/SKILL.md", "docs/design-kit/design-mockup.html"]
REF = re.compile(r"Step (\d+(?:-[a-z])?)")


def plain(line: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", line))


def headings(lines: list[str], is_html: bool) -> dict[str, tuple[int, str]]:
    found = {}
    for no, raw in enumerate(lines, 1):
        text = plain(raw) if is_html else raw
        if is_html:
            if not re.search(r'<h[23][^>]*>\s*Step \d', raw):
                continue
        elif not re.match(r"#{2,3} Step \d", raw):
            continue
        m = re.search(r"Step (\d+(?:-[a-z])?)\s*[:·]\s*(.+)", text)
        if m:
            found[m.group(1)] = (no, m.group(2).strip())
    return found


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    refs = ok = bad = unclassified = 0
    for rel in FILES:
        path = root / rel
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            print(f"read failed: {rel}: {exc}", file=sys.stderr)
            return 2
        is_html = rel.endswith(".html")
        heads = headings(lines, is_html)
        if len(heads) < 7:
            print(f"headings not found: {rel} ({len(heads)})", file=sys.stderr)
            return 2
        head_lines = {no for no, _ in heads.values()}
        for no, raw in enumerate(lines, 1):
            if no in head_lines or 'class="section-label"' in raw:
                continue
            text = plain(raw) if is_html else raw
            for m in REF.finditer(text):
                refs += 1
                start = max(text.rfind("다.", 0, m.start()), text.rfind(". ", 0, m.start()), -1) + 1
                ends = [i for i in (text.find("다.", m.end()), text.find(". ", m.end())) if i >= 0]
                sentence = text[start:(min(ends) + 2) if ends else len(text)]
                title = heads.get(m.group(1), (0, "<없는 절>"))[1]
                rule = next((r for r in RULES if r[0] in sentence), None)
                if rule is None:
                    unclassified += 1
                    verdict = "unclassified"
                elif rule[1] in title:
                    ok += 1
                    verdict = "ok"
                else:
                    bad += 1
                    verdict = f"bad(want '{rule[1]}')"
                print(f"{rel}:{no} Step {m.group(1)} -> {title} | {verdict}")
    print(f"refs={refs} ok={ok} bad={bad} unclassified={unclassified}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
