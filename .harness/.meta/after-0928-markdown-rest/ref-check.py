"""밀린 줄 참조 바로잡기 확인 — 사용: python3 ref-check.py <저장소> <ref-expect.tsv> <기준 판> <끝 판>

ref-expect.tsv 한 줄 = 파일<TAB>적힌 경로<TAB>대상 파일<TAB>옛 줄<TAB>기준 판에서 맞는 줄.
「기준 판에서 맞는 줄」 은 ref-shift.py 가 기준 판에서 git 줄 대응으로 구한 값이다. 끝 판까지 대상 파일이 또 바뀌었을
수 있으므로 git diff -U0 -w <기준 판> <끝 판> 으로 한 번 더 따라가 기대 줄 N 을 정한다(따라가지 못하면 FAIL).
같은 (파일, 적힌 경로, 옛 줄) 이 k 줄이면, 끝 판 파일에서 `적힌 경로:옛 줄` 은 기준 판보다 k 개 적고
`적힌 경로:N` 은 k 개 많아야 OK 다. 앞 글자가 경로 글자가 아니고 뒤가 숫자가 아닌 자리만 센다.
출력: 묶음마다 `OK|FAIL<TAB>파일<TAB>적힌 경로:옛 줄→N<TAB>끝 판 옛 수/기대<TAB>끝 판 새 수/기대`, 끝에 `REFS<TAB>묶음 수<TAB>OK 수`.
종료 코드: 모두 OK 0 · 하나라도 FAIL 1 · 판이나 파일을 못 읽음 2.
"""
import re, sys, subprocess, collections
repo, tsv, base, tip = sys.argv[1:5]
def git(*a):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
def show(rev, p):
    r = git('show', f'{rev}:{p}')
    if r.returncode: print('UNREADABLE', rev, p); sys.exit(2)
    return r.stdout
def mapline(t, n):
    d = git('diff', '-U0', '-w', '--no-color', base, tip, '--', t)
    if d.returncode: print('UNREADABLE diff', t); sys.exit(2)
    off = 0
    for h in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', d.stdout, re.M):
        os_, ns = int(h.group(1)), int(h.group(3))
        oc = int(h.group(2)) if h.group(2) is not None else 1
        nc = int(h.group(4)) if h.group(4) is not None else 1
        start = os_ if oc else os_ + 1
        if n < start: break
        if oc and n < os_ + oc: return ns + (n - os_) if oc == nc else None
        off += nc - oc
    return n + off
def count(text, w, num):
    return len(re.findall(r'(?<![\w/.-])' + re.escape(w) + ':' + str(num) + r'(?![\d])', text))
rows = [l.split('\t') for l in open(tsv, encoding='utf-8').read().split('\n') if l.strip()]
groups = collections.Counter((f, w, t, o, nb) for f, w, t, o, nb in rows)
ok = 0
for (f, w, t, o, nb), k in groups.items():
    n = mapline(t, int(nb))
    b, e = show(base, f), show(tip, f)
    if n is None:
        print(f'FAIL\t{f}\t{w}:{o}→GONE\t-\t-'); continue
    co, cn, bo, bn = count(e, w, o), count(e, w, n), count(b, w, o), count(b, w, n)
    good = co == bo - k and cn == bn + k
    ok += good
    print(f"{'OK' if good else 'FAIL'}\t{f}\t{w}:{o}→{n}\t{co}/{bo - k}\t{cn}/{bn + k}")
print(f'REFS\t{len(groups)}\t{ok}')
sys.exit(0 if ok == len(groups) else 1)
