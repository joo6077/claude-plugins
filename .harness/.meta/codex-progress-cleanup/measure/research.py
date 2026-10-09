#!/usr/bin/env python3
# 사용: python3 check.py <측정 이름> [--base]
#   가짜 codex(fake/codex)로 리서치 래퍼를 실제로 돌리고, 표준 오류(진행 줄)와 표준 출력(최종 답)을 잰다.
#   --base 는 이번 정리 직전 래퍼 백업(.bak-20261009d)을 잰다 — 옛 판에서 FAIL 이 나와야 측정이 살아 있다.
#   실제 ~/.codex/sessions · ~/.codex-status 는 건드리지 않는다(전부 임시 폴더).
# 측정 이름: activity forms once answer length burst retry flush partial corrupt monitor docs reuse usage nousage nostatus evidence
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser('~')
BASE = '--base' in sys.argv
WRAPPER = os.path.join(HOME, '.claude/bin/codex-research' + ('.bak-20261009d' if BASE else ''))
CLAUDE_MD = os.path.join(HOME, '.claude/CLAUDE.md')
TEMPLATE = os.path.join(HOME, '.claude/codex-prompt-template.md')
DOC_COMMAND = '~/.claude/bin/codex-research <프롬프트파일> <출력파일> 2>&1 >/dev/null'
mode = sys.argv[1] if len(sys.argv) > 1 else ''
failed = 0
STATUS_LEFT = []


def check(name, ok, detail=''):
    global failed
    print(('PASS ' if ok else 'FAIL ') + name + (' — ' + detail if detail else ''))
    if not ok:
        failed += 1


def run(scenario='ok', command=None, progress='2', step='4'):
    """가짜 codex 로 래퍼를 한 번 돌린다. command 를 주면 그 셸 명령을 그대로 돌린다(문서 명령 시험)."""
    tmp = tempfile.mkdtemp(prefix='research-activity-')
    for sub in ('sessions', 'status', 'state', 'home'):
        os.makedirs(os.path.join(tmp, sub))
    prompt = os.path.join(tmp, 'prompt.md')
    open(prompt, 'w', encoding='utf-8').write('MODE=research\nGoal: 가짜 리서치 시험\n')
    out = os.path.join(tmp, 'out', 'answer.md')
    env = dict(os.environ, PATH=os.path.join(HERE, 'fake') + ':' + os.environ['PATH'],
               CODEX_SESS_DIR=os.path.join(tmp, 'sessions'), CODEX_STATUS_DIR=os.path.join(tmp, 'status'),
               FAKE_STATE=os.path.join(tmp, 'state'), FAKE_SCENARIO=scenario, FAKE_STEP=step,
               CODEX_PROGRESS_SECONDS=progress, CODEX_TRIES='2', CODEX_NOTIFY_SINK='/usr/bin/true', HOME=os.path.join(tmp, 'home'))
    if command is None:
        proc = subprocess.run([WRAPPER, prompt, out], env=env, capture_output=True, text=True, timeout=120)
    else:
        command = command.replace('~/.claude/bin/codex-research', WRAPPER).replace('<프롬프트파일>', prompt).replace('<출력파일>', out)
        proc = subprocess.run(['bash', '-c', command], env=env, capture_output=True, text=True, timeout=120)
    answer = open(out, encoding='utf-8').read() if os.path.exists(out) else ''
    global STATUS_LEFT
    status = os.path.join(tmp, 'status')
    STATUS_LEFT = (sorted(os.listdir(status)) if os.path.isdir(status) else []) + \
        ['HOME/' + name for name in sorted(os.listdir(os.path.join(tmp, 'home')))]
    shutil.rmtree(tmp, ignore_errors=True)
    return proc, answer


def line_with(text, prefix, body):
    """prefix 로 시작하고 body 를 담은 줄의 첫 위치(글자 위치). 없으면 -1."""
    pos = 0
    for line in text.splitlines(keepends=True):
        if line.startswith(prefix) and body in line:
            return pos
        pos += len(line)
    return -1


ITEMS = [('  말: ', '공식 문서부터 확인하겠습니다.'), ('  검색: ', 'alpha query one'), ('  검색: ', 'beta query two'),
         ('  검색: ', 'gamma quoted'), ('  열람: ', 'https://example.com/doc'), ('  명령: ', 'gh api repos/x/y/releases')]

if mode in ('activity', 'forms', 'once', 'answer', 'length'):
    proc, answer = run()
    err = proc.stderr
    if mode == 'activity':
        check('종료 코드 0', proc.returncode == 0, str(proc.returncode))
        for prefix, body in ITEMS[:3] + ITEMS[4:]:
            check('「' + prefix.strip() + ' ' + body + '」 줄', line_with(err, prefix, body) >= 0)
        n = sum(1 for line in err.splitlines() if line.startswith('리서치 · 가짜 리서치 시험'))
        check('머리 줄 「리서치 · 가짜 리서치 시험」 2 개 이상', n >= 2, str(n))
        check('활동 6 개 이하 묶음에 「…앞서」 줄 0', '…앞서' not in err, str([l for l in err.splitlines() if '…앞서' in l]))
    elif mode == 'forms':
        check('따옴표 붙은 q 의 검색어 「gamma quoted」 줄', line_with(err, '  검색: ', 'gamma quoted') >= 0)
        check('검색 · 열람이 섞인 호출의 주소 열람 줄', line_with(err, '  열람: ', 'https://example.com/doc') >= 0)
        check('내부 번호 turn0search0 이 표준 오류에 0 번', 'turn0search0' not in err, str(err.count('turn0search0')))
        n = sum(1 for line in err.splitlines() if line.startswith('  명령: '))
        check('「명령:」 줄 정확히 1 개(변수 약식 cmd 는 건너뜀)', n == 1, str(n))
    elif mode == 'once':
        for body in ('공식 문서부터 확인하겠습니다', 'alpha query one', 'beta query two', 'gamma quoted', 'example.com/doc', 'gh api repos/x/y/releases'):
            n = err.count(body)
            check('「' + body + '」 정확히 1 번', n == 1, str(n))
    elif mode == 'answer':
        check('최종 답이 표준 오류에 0 번', 'QQZ' not in err, str(err.count('QQZ')))
        check('최종 답이 표준 출력에 그대로', 'QQZ' in proc.stdout, repr(proc.stdout[-60:]))
        check('출력 파일에 최종 답', 'QQZ' in answer)
        check('완료 줄', '완료 (시도 1/2' in err)
    else:
        progress = [line for line in err.splitlines() if line.startswith('리서치 · ') or line.startswith('  ')]
        long_lines = [len(line) for line in progress if len(line) > 200]
        check('진행 줄(머리 줄 · 두 칸 들여쓴 줄)이 모두 200 자 이하', not long_lines, str(long_lines))
        check('여러 줄 긴 말이 「  말: 긴말」 로 시작해 「…」 로 끝나는 한 줄', any(line.startswith('  말: 긴말') and line.endswith('…') for line in err.splitlines()))
        check('긴 말의 둘째 줄이 따로 나오지 않음', not any(line.startswith('나나나') or line.startswith('가가가') for line in err.splitlines()))
elif mode == 'burst':
    proc, answer = run('burst')
    err = proc.stderr
    lines = err.splitlines()
    run_len, worst = 0, 0
    for line in lines:
        run_len = run_len + 1 if line.startswith('  ') else 0
        worst = max(worst, run_len)
    check('한 번에 내는 들여쓴 줄이 7 줄 이하(앞서 1 + 최신 활동 6)', worst <= 7, str(worst))
    at = lines.index('  …앞서 6개') if '  …앞서 6개' in lines else -1
    check('「  …앞서 6개」 줄이 최신 활동 줄들 바로 앞', at >= 0 and lines[at + 1:at + 7] == ['  검색: burst q%02d' % n for n in range(7, 13)], str(lines[at:at + 7] if at >= 0 else lines))
    check('앞선 검색어 burst q01~q06 은 0 번', not any('burst q0%d' % n in err for n in range(1, 7)))
elif mode == 'retry':
    proc, answer = run('fail-then-ok')
    err = proc.stderr
    check('종료 코드 0', proc.returncode == 0, str(proc.returncode))
    check('시도 1 실패 줄', '시도 1/2 실패' in err)
    for prefix, body in (('  말: ', '첫시도말 확인하겠습니다.'), ('  검색: ', 'first attempt query'), ('  말: ', '둘째시도말 다른 길로 갑니다.'), ('  검색: ', 'second attempt query')):
        check('「' + prefix.strip() + ' ' + body + '」 줄', line_with(err, prefix, body) >= 0)
elif mode == 'flush':
    proc, answer = run(progress='100', step='1')
    err = proc.stderr
    done = err.find('완료 (시도 1/2')
    check('완료 줄', done >= 0)
    for prefix, body in ITEMS[1:] + [('  말: ', '긴말')]:
        at = line_with(err, prefix, body)
        check('주기 전에 끝나도 완료 줄보다 먼저 최신 활동 「' + prefix.strip() + ' ' + body[:20] + '」', 0 <= at < done, '{} / {}'.format(at, done))
    check('한꺼번에 나온 7 개 중 가장 앞선 말은 「  …앞서 1개」 로 묶임', '  …앞서 1개' in err.splitlines() and '공식 문서부터' not in err)
    proc, answer = run('fail-then-ok', progress='100', step='1')
    err = proc.stderr
    fail_at = err.find('시도 1/2 실패')
    at = line_with(err, '  검색: ', 'first attempt query')
    check('실패한 시도의 활동이 실패 줄보다 먼저', 0 <= at < fail_at, '{} / {}'.format(at, fail_at))
elif mode == 'partial':
    proc, answer = run('partial', step='3')
    err = proc.stderr
    check('반쯤 쓰인 줄의 검색어 정확히 1 번', err.count('partial query') == 1, str(err.count('partial query')))
    check('파이썬 오류 흔적 0', 'Traceback' not in err)
elif mode == 'corrupt':
    proc, answer = run('corrupt')
    err = proc.stderr
    check('종료 코드 0', proc.returncode == 0, str(proc.returncode))
    check('깨진 줄 바로 뒤 같은 묶음의 말', line_with(err, '  말: ', '깨진뒤말 이어갑니다.') >= 0)
    check('그다음 묶음의 열람', line_with(err, '  열람: ', 'https://example.com/doc') >= 0)
    check('파이썬 오류 흔적 0', 'Traceback' not in err and 'Error' not in err)
    check('출력 파일에 최종 답', 'QQZ' in answer)
elif mode == 'monitor':
    text = open(CLAUDE_MD, encoding='utf-8').read()
    found = re.findall(r'`(~/\.claude/bin/codex-research <프롬프트파일> <출력파일>[^`]*)`', text)
    found = [cmd for cmd in found if '2>&1' in cmd]
    check('전역 규칙에 「' + DOC_COMMAND + '」 꼴 명령 정확히 1 개', found == [DOC_COMMAND], str(found))
    if found:
        proc, answer = run(command=found[0])
        out = proc.stdout
        check('그 명령의 표준 출력에 진행 줄(검색어)', 'alpha query one' in out, repr(out[:120]))
        check('그 명령의 표준 출력에 최종 답 0 번', 'QQZ' not in out)
        check('그 명령의 표준 출력에 완료 줄', '완료 (시도 1/2' in out)
        check('출력 파일에 최종 답', 'QQZ' in answer)
elif mode == 'docs':
    for path, label in ((CLAUDE_MD, 'CLAUDE.md'), (TEMPLATE, 'codex-prompt-template.md')):
        lines = open(path, encoding='utf-8').read().splitlines()
        hit = [line for line in lines if 'codex-research' in line and ('run_in_background' in line or 'Monitor' in line)]
        check(label + ' 리서치 호출 문장 1 줄', len(hit) == 1, str(len(hit)))
        line = hit[0] if hit else ''
        check(label + ' 그 줄에 Monitor', 'Monitor' in line)
        check(label + ' 그 줄에 명령 「' + DOC_COMMAND + '」', DOC_COMMAND in line)
        check(label + ' 그 줄에 접두 「말:」 「검색:」 「열람:」 「명령:」', all(w in line for w in ('말:', '검색:', '열람:', '명령:')))
        stale = [n for n, l in enumerate(lines, 1) if '작업 카드' in l and 'codex-research' in l]
        check(label + ' 「작업 카드」 와 codex-research 를 함께 담은 줄 0', not stale, str(stale))
elif mode == 'reuse':
    src = open(WRAPPER, encoding='utf-8').read()
    body = re.search(r'^progress_say\(\).*?(?=^\S)', src, re.S | re.M)
    check('진행 줄 함수가 이 차례의 세션 기록(rollout)을 읽음', bool(body) and 'rollout' in body.group(0))
    check('세션 기록을 찾는 find "$SESS_DIR" 는 그대로 2 곳', src.count('find "$SESS_DIR"') == 2, str(src.count('find "$SESS_DIR"')))
    n = sum(1 for line in src.splitlines() if 'progress_every=' in line)
    check('진행 주기 변수 progress_every 를 정하는 줄은 그대로 1 줄', n == 1, str(n))
    before = len(re.findall(r'^[a-z_]+\(\) *\{', open(os.path.join(HOME, '.claude/bin/codex-research.bak-20261009d'), encoding='utf-8').read(), re.M))
    now = len(re.findall(r'^[a-z_]+\(\) *\{', src, re.M))
    check('함수 수 = 정리 직전 판 - 2 (status_write · usage_write 만 빠지고 새 함수 없음)', now == before - 2, '{} → {}'.format(before, now))
elif mode == 'usage':
    proc, answer = run()
    err = proc.stderr
    heads = [line for line in err.splitlines() if line.startswith('리서치 · ')]
    check('머리 줄 하나 이상이 이번 차례 기록의 null 아닌 마지막 사용량 「5시간 14% · 주간 30%」 로 끝남', any(line.endswith('· 5시간 14% · 주간 30%') for line in heads), str(heads))
    check('더 새로운 다른 세션 기록(미끼 77 · 66)의 값 0 번', '77%' not in err and '66%' not in err)
    check('「남은 한도」 를 담은 줄 0', '남은 한도' not in err, str([line for line in err.splitlines() if '남은 한도' in line]))
    check('완료 줄', '완료 (시도 1/2' in err)
elif mode == 'nousage':
    proc, answer = run('fail-then-ok')
    err = proc.stderr
    heads = [line for line in err.splitlines() if line.startswith('리서치 · ')]
    check('사용량 사건이 없는 기록 — 머리 줄에 「%」 0', heads and not any('%' in line for line in heads), str(heads))
    check('파이썬 오류 흔적 0 · 종료 코드 0', 'Traceback' not in err and proc.returncode == 0, str(proc.returncode))
elif mode == 'nostatus':
    proc, answer = run()
    check('종료 코드 0', proc.returncode == 0, str(proc.returncode))
    check('상태 폴더(CODEX_STATUS_DIR)에 남거나 생긴 파일 0', not STATUS_LEFT, str(STATUS_LEFT))
    src = open(WRAPPER, encoding='utf-8').read()
    left = [word for word in ('CODEX_STATUS_DIR', '.codex-status', 'status_write', 'usage_write', 'usage.json', 'STATUS_DIR') if word in src]
    check('래퍼에 상태 폴더 낱말 0', not left, str(left))
elif mode == 'evidence':
    path = os.path.join(HERE, '..', 'evidence', 'real-run.txt')  # 이 묶음의 증거
    lines = open(path, encoding='utf-8').read().splitlines() if os.path.exists(path) else []
    check('증거 파일 있음', bool(lines), path)
    if lines:
        check('첫 줄이 문서 명령 꼴로 실행한 명령', re.match(r'^# 명령: ~/\.claude/bin/codex-research \S+ \S+ 2>&1 >/dev/null$', lines[0]) is not None, lines[0])
        out_line = next((l for l in lines if l.startswith('# 출력: ')), '')
        answer_path = out_line[len('# 출력: '):]
        first = next((l.strip() for l in open(answer_path, encoding='utf-8') if l.strip()), '') if answer_path and os.path.exists(answer_path) else ''
        body = [l for l in lines if not l.startswith('# ')]
        check('출력 파일 첫 줄을 읽음', bool(first), answer_path)
        check('최종 답 첫 줄이 증거(진행 줄)에 0 번', bool(first) and not any(first in l for l in body))
        check('머리 줄 「리서치 · 」 1 개 이상', sum(1 for l in body if l.startswith('리서치 · ')) >= 1)
        check('활동 줄(말 · 검색 · 열람 · 명령) 1 개 이상', sum(1 for l in body if re.match(r'^  (말|검색|열람|명령): ', l)) >= 1)
        check('완료 줄 정확히 1 개', sum(1 for l in body if '완료 (시도' in l) == 1)
        check('Traceback 0', not any('Traceback' in l for l in body))
        check('「남은 한도」 줄 0', not any('남은 한도' in l for l in body))
        roll_line = next((l for l in lines if l.startswith('# 세션기록: ')), '')
        roll = roll_line[len('# 세션기록: '):]
        check('세션 기록 파일이 있고 래퍼 수정 뒤에 쓰임', bool(roll) and os.path.exists(roll) and os.path.getmtime(roll) >= os.path.getmtime(WRAPPER), roll)
        if roll and os.path.exists(roll):
            raw = open(roll, encoding='utf-8', errors='replace').read()
            items = [re.sub(r'^  (검색|열람): ', '', l) for l in body if re.match(r'^  (검색|열람): ', l)]
            check('증거의 검색 · 열람 줄이 그 세션 기록에 모두 있음', items and all(item.rstrip('…')[:60] in raw for item in items), str([i for i in items if i.rstrip('…')[:60] not in raw]))
else:
    check('알 수 없는 측정 이름 [' + mode + ']', False)
sys.exit(1 if failed else 0)
