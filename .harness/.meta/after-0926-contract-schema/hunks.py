"""계약 after-0926-contract-schema 측정 도우미 — 두 판 사이에 더하고 지운 줄을 제목별로 가른다.

사용:
  python3 hunks.py added   <저장소> <기준> <상한> <경로> [제목 줄 ...]   더한 줄. 제목을 주면 그 제목 몫의 줄만
  python3 hunks.py removed <저장소> <기준> <상한> <경로>                지운 줄
  python3 hunks.py outside <저장소> <기준> <상한> <경로> <제목 줄> ...  더한 줄 가운데 주어진 제목 몫이 아닌 줄
  python3 hunks.py owners  <파일>                                       줄마다 몫 제목 (알려진 답 확인용)

줄의 「몫 제목」 은 그 줄 앞에서 가장 가까운 마크다운 제목 줄이다. 코드 울타리(``` · ~~~) 안의 `#` 줄은
제목으로 보지 않는다. 제목 줄 자신의 몫은 자기 자신이다. 첫 제목 전 줄의 몫은 `(없음)` 이다.
출력 줄 모양: `<새 판 줄 번호>\t<줄 내용>` (removed 는 옛 판 줄 번호). 종료 코드: 0 정상, 2 입력 오류.
"""
import re
import subprocess
import sys

HEAD_RE = re.compile(r'^#{1,6} ')
FENCE_RE = re.compile(r'^\s*(`{3,}|~{3,})(.*)$')


def closes(m, fence):
    # 닫는 울타리: 여는 것과 같은 글자 · 같거나 더 긴 길이 · 뒤에 글 없음 (CommonMark)
    return bool(m) and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip()


def owners(lines):
    out, cur, fence = [], '(없음)', None
    for ln in lines:
        m = FENCE_RE.match(ln)
        if fence is None and m:
            fence = m.group(1)
            out.append(cur)
            continue
        if fence is not None:
            if closes(m, fence):
                fence = None
            out.append(cur)
            continue
        if HEAD_RE.match(ln):
            cur = ln.rstrip('\n')
        out.append(cur)
    return out


def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(2)
    return r.stdout


def diff_lines(repo, base, upper, path):
    d = git(repo, 'diff', '-U0', '--no-color', base, upper, '--', path)
    added, removed, o, n, hunk = [], [], 0, 0, False
    for ln in d.splitlines():
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', ln)
        if m:
            o, n, hunk = int(m.group(1)), int(m.group(3)), True
            continue
        if ln.startswith('diff --git'):
            hunk = False
        if not hunk:
            continue
        if ln.startswith('+'):
            added.append((n, ln[1:]))
            n += 1
        elif ln.startswith('-'):
            removed.append((o, ln[1:]))
            o += 1
    return added, removed


def main():
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == 'block':
        # block <파일> <제목 줄> <함수 이름> — 그 제목 몫의 코드 울타리 가운데 함수 정의가 든 것의 본문
        lines = open(sys.argv[2], encoding='utf-8').read().split('\n')
        head, name = sys.argv[3], sys.argv[4]
        own = owners(lines)
        blocks, cur, fence = [], None, None
        for ln, o in zip(lines, own):
            m = FENCE_RE.match(ln)
            if fence is None and m:
                fence = m.group(1)
                cur = [] if o == head else None
                continue
            if fence is not None and closes(m, fence):
                fence = None
                if cur is not None:
                    blocks.append(cur)
                cur = None
                continue
            if cur is not None:
                cur.append(ln)
        hit = [b for b in blocks if any(re.match(r'^\s*' + re.escape(name) + r'\(\)\s*\{', x) for x in b)]
        if len(hit) != 1:
            sys.stderr.write(f'함수 {name} 정의가 든 블록 {len(hit)} 개 (1 개여야 한다)\n')
            sys.exit(2)
        print('\n'.join(hit[0]))
        return
    if cmd == 'owners':
        lines = open(sys.argv[2], encoding='utf-8').read().split('\n')
        for i, o in enumerate(owners(lines), 1):
            print(f'{i}\t{o}')
        return
    if len(sys.argv) < 6:
        sys.stderr.write(__doc__)
        sys.exit(2)
    repo, base, upper, path = sys.argv[2:6]
    heads = sys.argv[6:]
    added, removed = diff_lines(repo, base, upper, path)
    if cmd == 'removed':
        for no, t in removed:
            print(f'{no}\t{t}')
        return
    text = git(repo, 'show', f'{upper}:{path}').split('\n')
    own = owners(text)
    for no, t in added:
        o = own[no - 1]
        if cmd == 'added' and (not heads or o in heads):
            print(f'{no}\t{t}')
        elif cmd == 'outside' and o not in heads:
            print(f'{no}\t{o}\t{t}')
    if cmd not in ('added', 'outside'):
        sys.stderr.write(f'알 수 없는 명령: {cmd}\n')
        sys.exit(2)


main()
