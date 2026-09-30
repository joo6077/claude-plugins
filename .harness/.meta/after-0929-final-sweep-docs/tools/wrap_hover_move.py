"""쪽 `<style>` 의 `:hover` 규칙이 주는 `transform` 값을 `var(--dk-hover-move, 원래 값)` 으로 감싼다.

`python3 wrap_hover_move.py <docs 가 든 폴더> <쪽 목록 파일>` — 움직임 줄이기 설정에서 공통 파일이 `--dk-hover-move` 를
`none` 으로 둔다. 움직임을 허용한 설정에서는 원래 값이 그대로 계산된다. `none` 값과 이미 감싼 값은 건너뛴다.
가만히 있을 때도 transform 이 있는 요소(원래 값에 `translate(-50%` · `rotate` 가 든 값)는 감싸면 제자리를 잃으므로
건너뛰고 이름을 찍는다 — 손으로 고친다.
"""
import re
import sys
from pathlib import Path

RULE = re.compile(r"([^{};]+)\{([^{}]*)\}")
DECL = re.compile(r"(?<![-\w])(transform\s*:\s*)([^;}]+)")


def wrap_rules(css, skipped, page):
    def rule(match):
        selector, body = match.group(1), match.group(2)
        if ":hover" not in selector:
            return match.group(0)

        def decl(d):
            value = d.group(2).strip()
            if value.startswith(("none", "var(--dk-hover-move")):
                return d.group(0)
            if "translate(-50%" in value or "rotate" in value:
                skipped.append(f"{page}: {selector.strip()} {{transform:{value}}}")
                return d.group(0)
            return f"{d.group(1)}var(--dk-hover-move, {value})"
        return selector + "{" + DECL.sub(decl, body) + "}"
    return RULE.sub(rule, css)


def main(root, listing):
    changed, skipped = 0, []
    for rel in Path(listing).read_text(encoding="utf-8").split():
        page = Path(root) / rel
        text = page.read_text(encoding="utf-8")
        new = re.sub(r"(?is)(<style[^>]*>)(.*?)(</style>)",
                     lambda m: m.group(1) + wrap_rules(m.group(2), skipped, rel) + m.group(3), text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            changed += 1
    for line in skipped:
        print("건너뜀", line)
    print(f"고친 쪽 {changed}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
