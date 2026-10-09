"""바뀐 줄 가르기 — 사용: git diff -U0 [...] | python3 line-kinds.py

통합 차이(unified diff, -U0)를 읽어 더한 줄 · 지운 줄을 네 종류로 나눈다.
  fence   : 울타리 줄 (앞 공백 · > 뒤 ``` 또는 ~~~ 셋 이상)
  comment : markdownlint 지시 주석 한 줄 (<!-- markdownlint-... -->)
  blank   : 빈 줄 (공백만 있는 줄 포함)
  other   : 그 밖 — 글이 바뀐 줄
출력: 파일마다 `FILE<TAB>경로<TAB>fence<TAB>comment<TAB>blank<TAB>other`,
other 줄마다 `OTHER<TAB>경로:새 판 줄<TAB>+|-<TAB>앞 60 자`(지운 줄은 옛 판 줄),
block 꼴 지시(disable · enable 뒤 공백 — next-line 이 아닌 것)를 더한 줄마다 `BLOCKDIR<TAB>경로:새 판 줄`,
next-line 지시를 더한 줄마다 `NEXTLINE<TAB>경로:새 판 줄`,
끝에 `TOTAL<TAB>fence<TAB>comment<TAB>blank<TAB>other<TAB>blockdir`.
"""
import re, sys
fence = re.compile(r'^[ \t>]*(`{3,}|~{3,})')
comment = re.compile(r'^\s*<!-- markdownlint-[a-z-]+( MD\d{3})* -->\s*$')
block = re.compile(r'markdownlint-(disable|enable) ')
nextl = re.compile(r'markdownlint-disable-next-line ')
tot = [0, 0, 0, 0, 0]; cur = None; per = {}; order = []
on = nn = 0
for raw in sys.stdin.read().split('\n'):
    if raw.startswith('+++ '):
        p = raw[4:]; cur = p[2:] if p.startswith('b/') else p
        if cur not in per: per[cur] = [0, 0, 0, 0]; order.append(cur)
        continue
    if raw.startswith('--- ') or raw.startswith('diff ') or raw.startswith('index '): continue
    h = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', raw)
    if h: on, nn = int(h.group(1)), int(h.group(2)); continue
    if cur is None or not raw or raw[0] not in '+-': continue
    sign, body = raw[0], raw[1:]
    ln = nn if sign == '+' else on
    if fence.match(body): k = 0
    elif comment.match(body): k = 1
    elif not body.strip(): k = 2
    else: k = 3
    per[cur][k] += 1; tot[k] += 1
    if k == 3: print(f'OTHER\t{cur}:{ln}\t{sign}\t{body[:60]}')
    if sign == '+' and block.search(body): tot[4] += 1; print(f'BLOCKDIR\t{cur}:{ln}')
    if sign == '+' and nextl.search(body): print(f'NEXTLINE\t{cur}:{ln}')
    if sign == '+': nn += 1
    else: on += 1
for p in order: print('FILE\t' + p + '\t' + '\t'.join(map(str, per[p])))
print('TOTAL\t' + '\t'.join(map(str, tot)))
