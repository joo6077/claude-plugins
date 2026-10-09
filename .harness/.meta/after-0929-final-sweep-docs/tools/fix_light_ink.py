"""밝은 테마 대비 검사에서 떨어진 글자색을 고친다 — 쪽에 박힌 색 값을 변수로 바꾼다.

`python3 fix_light_ink.py <접근성 검사 출력> <쪽 목록 파일>`
검사 출력의 `light … rgb(r, g, b)` 줄이 가리키는 쪽마다, `<style>` 과 `style=` 속성의 `color:` 값 가운데 그 색과
같은 값을 찾아 바꾼다.
- 쪽 `:root` 에 같은 값을 가진 색 변수가 있고 그 변수를 공통 파일이 밝은 테마에서 어둡게 섞으면 `var(--그 이름)`
- 아니면 `--dk-ink:원래 값;color:var(--dk-ink-out, 원래 값)` — 공통 파일이 밝은 테마에서만 어둡게 섞는다
어두운 테마에서는 둘 다 원래 값으로 계산된다.
"""
import collections
import os
import re
import sys
from pathlib import Path

MIXED = ["accent", "accent2", "success", "error", "warn", "warning", "danger", "info", "green", "red", "yellow",
         "orange", "pink", "cyan", "blue", "purple", "teal", "gold", "lime"]
LITERAL = r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)"


def rgb_of(value):
    value = value.strip().lower()
    if value.startswith("#"):
        digits = value[1:]
        if len(digits) in (3, 4):
            digits = "".join(c * 2 for c in digits)
        return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))
    nums = re.findall(r"[\d.]+", value)
    return tuple(round(float(n)) for n in nums[:3])


def root_vars(css):
    found = {}
    for block in re.findall(r":root\s*\{([^}]*)\}", css):
        for name, value in re.findall(r"--([\w-]+)\s*:\s*([^;]+)", block):
            found[name] = value.strip()
    return found


def failing_colors(report, pages):
    by_name = collections.defaultdict(list)
    for rel in pages:
        by_name[os.path.basename(rel)].append(rel)
    colors, current = collections.defaultdict(set), None
    for line in Path(report).read_text(encoding="utf-8").splitlines():
        head = re.match(r"^(OK  |FAIL) (\S+)", line)
        if head:
            current = by_name.get(head.group(2)) if head.group(1) == "FAIL" else None
            continue
        row = re.match(r"^\s+light\s+\S+ < \S+\s+rgba?\(([^)]*)\)", line)
        if row and current:
            for rel in current:
                colors[rel].add(tuple(round(float(n)) for n in row.group(1).split(",")[:3]))
    return colors


def fix_page(rel, targets):
    text = Path(rel).read_text(encoding="utf-8")
    css = " ".join(re.findall(r"(?is)<style[^>]*>(.*?)</style>", text))
    names = {rgb_of(v): n for n, v in root_vars(css).items() if n in MIXED and re.fullmatch(LITERAL, v)}
    count = 0

    def recolor(match):
        nonlocal count
        value = match.group(2)
        if rgb_of(value) not in targets:
            return match.group(0)
        count += 1
        name = names.get(rgb_of(value))
        if name:
            return f"{match.group(1)}var(--{name})"
        return f"--dk-ink:{value};{match.group(1)}var(--dk-ink-out, {value})"

    decl = re.compile(r"(?<![-\w])(color\s*:\s*)(" + LITERAL + r")")
    text = re.sub(r"(?is)(<style[^>]*>)(.*?)(</style>)",
                  lambda m: m.group(1) + decl.sub(recolor, m.group(2)) + m.group(3), text)
    text = re.sub(r'(\sstyle=")([^"]*)(")', lambda m: m.group(1) + decl.sub(recolor, m.group(2)) + m.group(3), text)
    Path(rel).write_text(text, encoding="utf-8")
    return count


def main(report, listing):
    pages = Path(listing).read_text(encoding="utf-8").split()
    for rel, targets in sorted(failing_colors(report, pages).items()):
        print(f"{fix_page(rel, targets):3d} {rel}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
