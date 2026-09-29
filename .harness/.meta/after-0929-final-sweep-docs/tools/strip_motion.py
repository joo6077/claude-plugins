"""쪽 `<style>` 에 다시 적은 움직임 줄이기 블록을 지운다 — 공통 파일 `docs/assets/site.css` 가 맡는다.

`python3 strip_motion.py <docs 가 든 폴더> <쪽 목록 파일> [--show]`
- `@media (prefers-reduced-motion: reduce){…}` 블록은 통째로 지운다.
- `@media (prefers-reduced-motion: no-preference){…}` 블록은 껍데기만 벗겨 안의 규칙을 그대로 둔다
  (움직임을 허용한 설정의 들뜸을 지키고, 줄이기 설정에서는 공통 파일이 멈춘다).
- `--show` 는 고치지 않고 지울 블록의 모양만 센다.
"""
import collections
import re
import sys
from pathlib import Path

HEAD = re.compile(r"@media\s*\(\s*prefers-reduced-motion\s*:\s*(reduce|no-preference)\s*\)\s*\{")


def block_end(css, start):
    """`{` 다음 자리부터 짝이 맞는 `}` 바로 뒤 자리를 돌려준다."""
    depth = 1
    i = start
    while depth:
        c = css[i]
        depth += c == "{"
        depth -= c == "}"
        i += 1
    return i


def strip(css, shapes):
    out, pos = [], 0
    for m in HEAD.finditer(css):
        if m.start() < pos:
            continue
        end = block_end(css, m.end())
        inner = css[m.end():end - 1]
        shapes[(m.group(1), re.sub(r"\s+", "", inner))] += 1
        before = css[pos:m.start()]
        # 블록만 있던 줄은 빈 줄로 남기지 않는다
        if m.group(1) == "reduce":
            before = re.sub(r"[ \t]*$", "", before)
            tail = re.match(r"[ \t]*\n?", css[end:])
            end += tail.end() if before.endswith("\n") else 0
            out.append(before)
        else:
            out.append(before + inner.strip("\n"))
        pos = end
    out.append(css[pos:])
    return "".join(out)


def main(root, listing, show=False):
    shapes = collections.Counter()
    changed = 0
    for rel in Path(listing).read_text(encoding="utf-8").split():
        page = Path(root) / rel
        h = page.read_text(encoding="utf-8")
        new = re.sub(r"(?is)(<style[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + strip(m.group(2), shapes) + m.group(3), h)
        if new != h:
            changed += 1
            if not show:
                page.write_text(new, encoding="utf-8")
    if show:
        for (kind, body), n in shapes.most_common():
            print(f"{n:3d} {kind} {body[:160]}")
    print(f"고친 쪽 {changed}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--show" in sys.argv)
