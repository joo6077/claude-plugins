"""계약 after-0926-contract-schema 측정 도우미 — 쉬운 말 목록에서 검사가 켜진 낱말이 글에 몇 번 나오는지 센다.

사용: python3 plain.py <목록 파일> < 입력
입력은 줄마다 글 한 줄이다. 백틱으로 감싼 부분(코드 · 경로 · 이름)은 지우고 잰다.
목록 파일은 `~/.claude/rules/plain-korean.md` 형식 — `## 바꿔 쓸 말` 아래 표의 1 열(` / ` 로 나눔)이
낱말이고 3 열이 `on` 인 줄만 쓴다. 영문 낱말은 대소문자 무시 · 낱말 경계로, 한글 낱말은 글자 그대로 찾는다.
출력: 걸린 줄마다 `HIT <낱말>\t<줄>`, 마지막 줄 `hits=<수> words=<검사한 낱말 수>`. 종료 코드: 0 정상, 2 목록 읽기 실패.
"""
import re
import sys

try:
    src = open(sys.argv[1], encoding='utf-8').read().split('\n')
except (IndexError, OSError) as e:
    sys.stderr.write(f'목록을 못 읽었다: {e}\n')
    sys.exit(2)

words, on_table = [], False
for ln in src:
    if ln.startswith('## '):
        on_table = ln.strip() == '## 바꿔 쓸 말'
        continue
    if not on_table or not ln.startswith('|'):
        continue
    cells = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(cells) < 3 or cells[2] != 'on':
        continue
    for w in cells[0].split(' / '):
        w = w.strip()
        if w:
            words.append(w)

if not words:
    sys.stderr.write('검사할 낱말이 0 개다 — 목록 형식이 바뀌었는지 본다\n')
    sys.exit(2)

pats = []
for w in words:
    if re.fullmatch(r'[A-Za-z0-9+ _-]+', w):
        pats.append((w, re.compile(r'(?<![A-Za-z0-9])' + re.escape(w) + r'(?![A-Za-z0-9])', re.I)))
    else:
        pats.append((w, re.compile(re.escape(w))))

hits = 0
for line in sys.stdin:
    t = re.sub(r'`[^`]*`', ' ', line.rstrip('\n'))
    for w, p in pats:
        if p.search(t):
            hits += 1
            print(f'HIT {w}\t{line.rstrip()}')
print(f'hits={hits} words={len(words)}')
