"""밀린 「파일:줄」 참조 찾기 — 사용: python3 ref-shift.py <저장소> [<판>]

<판>(기본 HEAD) 에서 추적되는 .md 가운데 .harness/ 밖 파일의 `경로:줄` 참조를 모은다.
참조가 든 줄을 마지막으로 바꾼 커밋 R 을 git blame -w 로 찾고(공백만 바꾼 커밋은 건너뛴다), 그 때의 대상 파일 줄 N 이
<판> 에서 몇째 줄인지 git diff -U0 -w R <판> 의 조각 머리로 따라간다(표 칸 공백만 바뀐 줄은 같은 줄로 본다). 둘이 다르면 밀린 것이다.
적힌 경로가 저장소 뿌리 · 참조 파일 폴더 기준으로 없으면, 그 경로로 끝나는 추적 파일이 딱 하나일 때 그것으로 본다.
`경로:줄-줄` 범위는 두 끝을 따로 잰다. 같은 수의 줄을 바꾼 조각 안의 줄은 자리대로 옮긴다.
출력: 밀린 참조마다 `SHIFT<TAB>참조 파일:참조 줄<TAB>적힌 경로<TAB>대상:N<TAB>→<TAB>M<TAB>종류` (지워진 줄이면 M 은 GONE).
종류는 SAME(옛 줄과 새 줄이 공백 빼고 같음) · EDIT(자리대로 옮겼지만 글이 바뀜) · GONE.
끝에 `TOTAL<TAB>참조 수<TAB>밀림 수<TAB>못 따라간 수(대상이 R 에 없음)<TAB>경로를 못 찾은 수`.
"""
import re, subprocess, sys, os
repo = sys.argv[1]; rev = sys.argv[2] if len(sys.argv) > 2 else 'HEAD'
def git(*a):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
tracked = set(git('ls-tree', '-r', '--name-only', rev).stdout.split('\n'))
mds = sorted(p for p in tracked if p.endswith('.md') and not p.startswith('.harness/'))
ref = re.compile(r'(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.(?:md|sh|py|json|ya?ml|js|mjs|html|toml|rs|dart|ts|tsx|txt)):(\d+)(?:-(\d+))?(?![\d])')
def resolve(src, t):
    for cand in (t, os.path.normpath(os.path.join(os.path.dirname(src), t))):
        if cand in tracked: return cand
    tail = [x for x in tracked if x.endswith('/' + t)]
    return tail[0] if len(tail) == 1 else None
def mapline(r, t, n):
    d = git('diff', '-U0', '-w', '--no-color', r, rev, '--', t)
    if d.returncode: return None
    off = 0
    for h in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', d.stdout, re.M):
        os_, ns = int(h.group(1)), int(h.group(3))
        oc = int(h.group(2)) if h.group(2) is not None else 1
        nc = int(h.group(4)) if h.group(4) is not None else 1
        start = os_ if oc else os_ + 1
        if n < start: break
        if oc and n < os_ + oc:
            # 같은 수의 줄을 바꾼 조각이면 자리대로 옮긴다(울타리에 언어를 단 줄 등). 아니면 따라갈 수 없다
            return ns + (n - os_) if oc == nc else 'GONE'
        off += nc - oc
    return n + off
refs = shift = lost = unres = 0
for p in mds:
    text = git('show', f'{rev}:{p}').stdout.split('\n')
    hits = [(i + 1, m) for i, l in enumerate(text) for m in ref.finditer(l)]
    if not hits: continue
    blame = {}
    for ln, m in hits:
        t = resolve(p, m.group(1))
        if not t: unres += 1; continue
        refs += 1
        if ln not in blame:
            b = git('blame', '-w', '-l', '-s', '-L', f'{ln},{ln}', rev, '--', p).stdout.split(' ')[0].lstrip('^')
            blame[ln] = b
        r = blame[ln]; n = int(m.group(2))
        if git('cat-file', '-e', f'{r}:{t}').returncode: lost += 1; continue
        ends = [n] + ([int(m.group(3))] if m.group(3) else [])
        for e in ends:
            mm = mapline(r, t, e)
            if mm is None: lost += 1; continue
            if mm != e:
                shift += 1
                kind = 'GONE'
                if mm != 'GONE':
                    a = git('show', f'{r}:{t}').stdout.split('\n')[e - 1]
                    b = git('show', f'{rev}:{t}').stdout.split('\n')[mm - 1]
                    kind = 'SAME' if re.sub(r'\s+', '', a) == re.sub(r'\s+', '', b) else 'EDIT'
                print(f'SHIFT\t{p}:{ln}\t{m.group(1)}\t{t}:{e}\t→\t{mm}\t{kind}')
print(f'TOTAL\t{refs}\t{shift}\t{lost}\t{unres}')
