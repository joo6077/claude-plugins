#!/usr/bin/env python3
"""setup-guide.html 에 옮긴 guide_gate 함수가 SKILL.md 원본과 글자까지 같은지 본다 (B6 페이지 맞추기).

쓰임: python3 b6-page-copy.py <레포 뿌리>
SKILL.md 에서 `guide_gate() {` 부터 첫 `}` 줄까지, 페이지에서 같은 구간을 HTML 태그를 벗기고
엔티티를 풀어 뽑아 빈 줄을 뺀 줄 단위로 맞댄다. 출력: COPY lines=<원본 줄 수> diff=<다른 줄 수>
종료 코드: 0 같음 · 1 다름 · 2 구간을 못 찾음
"""
import html, re, sys, os

root = sys.argv[1]
src = open(os.path.join(root, "onboarding-kit/skills/setup-guide/SKILL.md"), encoding="utf-8").read().split("\n")
page = open(os.path.join(root, "docs/onboarding-kit/setup-guide.html"), encoding="utf-8").read()
text = html.unescape(re.sub(r"<[^>]+>", "", page)).split("\n")


def cut(lines):
    try:
        a = next(i for i, l in enumerate(lines) if l.strip() == "guide_gate() {")
        b = next(i for i in range(a, len(lines)) if lines[i].rstrip() == "}")
    except StopIteration:
        return None
    return [l.rstrip() for l in lines[a:b + 1] if l.strip()]   # 빈 줄은 맞대지 않는다


s, p = cut(src), cut(text)
if s is None or p is None:
    print(f"STOP 구간 없음 skill={s is not None} page={p is not None}")
    sys.exit(2)
# 페이지의 코드 블록은 들여쓰기가 다를 수 있어 앞 공백 폭 차이만 맞춘다
ind = len(p[0]) - len(p[0].lstrip())
p = [l[ind:] if l[:ind].strip() == "" else l for l in p]
diff = sum(1 for a, b in zip(s, p) if a != b) + abs(len(s) - len(p))
print(f"COPY lines={len(s)} page_lines={len(p)} diff={diff}")
sys.exit(0 if diff == 0 else 1)
