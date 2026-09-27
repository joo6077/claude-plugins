#!/usr/bin/env python3
"""lint.sh 경고 줄을 AUTO 블록 안 · 밖으로 나눠 센다.

사용: auto.py <저장소> <lint.sh 출력 파일>
AUTO 블록 = 코드 블록 밖에서 줄 첫머리가 `<!-- AUTO:<이름>` 인 줄부터 `<!-- /AUTO:<이름>` 줄까지(두 표식 줄 포함).
코드 블록 속이나 줄 중간의 표식(설계 문서의 예시)은 블록으로 보지 않는다.
끝 줄: in_auto=<n> out_auto=<n>
"""
import os, re, sys
repo, lint = sys.argv[1:3]
spans = {}
def auto_lines(path):
    if path not in spans:
        s, inside, fence = set(), None, None
        with open(os.path.join(repo, path), encoding='utf-8') as f:
            for no, line in enumerate(f, 1):
                fm = re.match(r'^\s*(`{3,}|~{3,})', line)
                if fm:
                    ch = fm.group(1)[0]
                    fence = ch if fence is None else (None if fence == ch else fence)
                m = None if fence or fm else re.match(r'^<!--\s*(/?)AUTO:([\w-]+)', line)
                if m and not m.group(1):
                    inside = m.group(2)
                if inside:
                    s.add(no)
                if m and m.group(1):
                    inside = None
        spans[path] = s
    return spans[path]
i = o = 0
for line in open(lint, encoding='utf-8'):
    m = re.match(r'^([^ ]+?):(\d+)', line)
    if not m:
        continue
    if int(m.group(2)) in auto_lines(m.group(1)):
        i += 1; print('IN ' + line.rstrip())
    else:
        o += 1
print(f'in_auto={i} out_auto={o}')
