"""check-api-kit-docs.py 의 외부 리소스 판정식에 사례를 넣어 틀린 사례를 센다.
사용: python3 ext_cases.py <check-api-kit-docs.py 경로>
      python3 ext_cases.py --compare <기준 판 스크립트> <새 판 스크립트>
출력 한 줄: cases=<수> wrong=<수> <틀린 사례 이름 쉼표 나열>. 종료 코드: 틀린 것 0 이면 0, 있으면 1, 판정식을 못 읽으면 2.
--compare 는 시드 20260927 로 만든 입력 200 개를 두 판정식에 넣어 판정이 다른 입력 수를 센다 — 출력 `compare n=200 diff=<수> seed=20260927`.
만드는 입력은 이번에 뜻을 바꾸는 모양(url(// · <img src> · 빈칸 없는 @import)을 뺀 모양뿐이라 두 판이 같아야 한다.
사례 1 = 외부로 잡아야 함, 0 = 잡으면 안 됨. P · N · U 열여덟은 앞 계약(after-0926-codex-and-leftover-fixes SC-01)의 사례를 그대로 옮겼고,
Q · R 은 이번 계약이 더한다 — url(//…) · <img src> · 빈칸 없는 @import.
"""
import runpy
import sys

import random


def load(path):
    try:
        return runpy.run_path(path)['EXTERNAL']
    except Exception as e:  # 판정식을 못 읽으면 판정 불가
        print(f'READ_FAIL {path} {e}')
        sys.exit(2)


if sys.argv[1] == '--compare':
    old, new = load(sys.argv[2]), load(sys.argv[3])
    rng = random.Random(20260927)
    urls = ['https://x.test/a.css', 'HTTPS://x.test/a.css', 'http://x.test/a', '//x.test/a.css', '../assets/site.css',
            'assets/site.css', '/assets/site.css', '\\\\x.test/a.css', 'data:text/css,a']
    quotes, spaces = ['"', "'", ''], ['', ' ', '\t', '\n ']
    shapes = ['<link rel="stylesheet" href={q}{w}{u}{q}>', '<LINK HREF={q}{w}{u}{q} REL=stylesheet>', '<script src={q}{u}{q}></script>',
              '<SCRIPT SRC={q}{u}{q}></SCRIPT>', '<a href={q}{u}{q}>x</a>', '<p>{u}</p>', '@import {q}{u}{q};', '.a{{background:url({w}{q}{u}{q})}}']
    n = diff = 0
    while n < 200:
        shape, u = rng.choice(shapes), rng.choice(urls)
        if 'url(' in shape and u.startswith('//'):
            continue  # 뜻을 바꾸는 모양이라 뺀다
        text = shape.format(q=rng.choice(quotes), w=rng.choice(spaces), u=u)
        n += 1
        diff += bool(old.search(text)) != bool(new.search(text))
    print(f'compare n={n} diff={diff} seed=20260927')
    sys.exit(1 if diff else 0)

ext = load(sys.argv[1])

CASES = [
    ('P1', 1, '<link rel="stylesheet" href="https://x.test/a.css">'),
    ('P2', 1, '<link rel="stylesheet" href="HTTPS://x.test/a.css">'),
    ('P3', 1, '<link rel="stylesheet" href=" https://x.test/a.css">'),
    ('P4', 1, '<LINK REL="stylesheet" HREF="https://x.test/a.css">'),
    ('P5', 1, '<link rel="stylesheet" href="//x.test/a.css">'),
    ('P6', 1, '<link rel=stylesheet href=https://x.test/a.css>'),
    ('P7', 1, '<link rel="stylesheet" href="\thttps://x.test/a.css">'),
    ('P8', 1, "<link rel='stylesheet' href='\n https://x.test/a.css'>"),
    ('P9', 1, '<SCRIPT SRC="https://x.test/a.js"></SCRIPT>'),
    ('P10', 1, '<link rel="stylesheet" href="\\\\x.test/a.css">'),
    ('N1', 0, '<link rel="stylesheet" href="../assets/site.css">'),
    ('N2', 0, '<link rel="stylesheet" href=" ../assets/site.css">'),
    ('N3', 0, '<link rel="stylesheet" href="assets/site.css">'),
    ('N4', 0, '<link rel="stylesheet" href="/assets/site.css">'),
    ('N5', 0, '<a href="https://x.test/doc">문서</a>'),
    ('N6', 0, '<script>const u = "https://x.test/a.js";</script>'),
    ('U1', 1, '.a{background:url(HTTPS://x.test/a.png)}'),
    ('U2', 0, '.a{background:url(../assets/a.png)}'),
    ('Q1', 1, '.a{background:url(//cdn.x.test/a.png)}'),
    ('Q2', 1, ".a{background:url( '//cdn.x.test/a.png')}"),
    ('Q3', 1, '<img src="https://x.test/a.png" alt="">'),
    ('Q4', 1, "<IMG ALT='' SRC='//x.test/a.png'>"),
    ('Q5', 1, '@import"https://x.test/a.css";'),
    ('Q6', 1, "@import'//x.test/a.css';"),
    ('Q7', 1, '@import url(https://x.test/a.css);'),
    ('R1', 0, '<img src="../assets/a.png" alt="">'),
    ('R2', 0, '<img src="data:image/png;base64,AAAA" alt="">'),
    ('R3', 0, '.a{background:url(data:image/png;base64,AAAA)}'),
    ('R4', 0, '<img alt="https://x.test/a.png" src="a.png">'),
    ('R5', 0, '<rect fill="url(#grad)"/>'),
]
wrong = [name for name, want, s in CASES if bool(ext.search(s)) != bool(want)]
print(f'cases={len(CASES)} wrong={len(wrong)} {",".join(wrong)}')
sys.exit(1 if wrong else 0)
