"""원본에서 페이지가 마지막으로 고쳐진 뒤 새로 생긴 코드 표시(백틱 글)가 페이지에 들었는지 잰다.
사용: python3 drift.py <레포> <pairs.txt> <기준 판>
기준 판은 봉인 때 잰 페이지 마지막 커밋을 고정하려고 받는다 — 이 판에서 페이지를 마지막으로 고친 커밋을 찾는다.
출력: 짝마다 한 줄 `added=<새 코드 수> in_page=<페이지에 든 수> missing=<빠진 수> [빠진 것 앞 5 개]`, 끝 줄 `pairs=<짝 수> total_missing=<합>`.
종료 코드: 빠진 것이 0 이면 0, 있으면 1, 읽기 실패 2.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

repo, pairs_file, pin = sys.argv[1], sys.argv[2], sys.argv[3]


def git(*args):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True)
    if r.returncode:
        print(f'READ_FAIL git {" ".join(args)}: {r.stderr.strip()}')
        sys.exit(2)
    return r.stdout


def page_text(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h)))


def codes(s):
    return {re.sub(r'\s+', ' ', c.strip()) for c in re.findall(r'`([^`\n]+)`', s) if c.strip()}


total = 0
pairs = [ln.split() for ln in Path(pairs_file).read_text(encoding='utf-8').splitlines() if ln.strip()]
for src, page in pairs:
    last = git('log', '-1', '--format=%H', pin, '--', page).strip()
    if not last:
        print(f'READ_FAIL 페이지 커밋 없음 {page}')
        sys.exit(2)
    before = codes(git('show', f'{last}:{src}'))
    now = codes(Path(repo, src).read_text(encoding='utf-8'))
    added = sorted(now - before)
    text = page_text(Path(repo, page).read_text(encoding='utf-8'))
    miss = [c for c in added if c not in text]
    total += len(miss)
    print(f'{page}\t{src}\tsince={last[:7]}\tadded={len(added)}\tin_page={len(added) - len(miss)}\tmissing={len(miss)}\t{miss[:5]}')
print(f'pairs={len(pairs)}\ttotal_missing={total}')
sys.exit(1 if total else 0)
