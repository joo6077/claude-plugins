#!/usr/bin/env python3
"""Read the branch snapshot; execute only disposable copies. Exit 0=PASS, 1=FAIL."""
import hashlib
import http.server
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time

HERE = Path(__file__).resolve().parent
W = Path(os.environ.get('MEASURE_W', '/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-audit-progress'))
BASE, BRANCH = 'c78b4f09', 'feat/codex-audit-progress'
SCRIPT = 'harness/scripts/codex-audit.sh'
DOCS = ['harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md']
KEY = 'sk-progress-fixture-INVALID-0123456789'
IDS = ['스킬-01', '스킬-02'] + ['스크립트-%02d' % i for i in range(1, 10)] + ['오류-01', '오류-02', '구조-01', '구조-02', '구조-03', '금지-03', '금지-04', '재사용-01', '재사용-02'] + ['진단-%02d' % i for i in range(1, 5)]
CONTRACT = '''---
feature: "progress fixture"
created: "2026-10-06 00:00"
complexity: simple
conditions: 2
slug: sample
status: active
---
# fixture
## Script
- [ ] 스크립트-01: GOOD [exact]
  측정: printf GOOD
- [ ] 스크립트-02: GOOD [exact]
  측정: printf GOOD
'''
CHECKS, PROCESSES, CASES = [], [], []
NEGATIVE = '--negative' in sys.argv
MUTATION = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--mutation=')), '')
RUN = Path(tempfile.mkdtemp(prefix='audit-progress-measure-', dir=os.environ.get('MEASURE_TMP') or None))
SOURCE = RUN / 'source'

def check(value, label):
    CHECKS.append(dict(ok=bool(value), label=label))
    if not value: raise AssertionError(label)

def command(args, cwd=None, env=None, timeout=30):
    return subprocess.run(list(map(str, args)), cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)

def git(*args):
    p = command(['git', '-C', W, *args])
    check(p.returncode == 0, 'git ' + ' '.join(args) + ': ' + p.stderr.strip())
    return p.stdout.strip()

def snapshot():
    upper = git('rev-parse', '--verify', '-q', BRANCH)
    check(bool(upper), 'branch exists; no HEAD fallback')
    SOURCE.mkdir()
    archive = RUN / 'source.tar'
    with archive.open('wb') as f:
        p = subprocess.run(['git', '-C', str(W), 'archive', upper], stdout=f, stderr=subprocess.PIPE)
    check(p.returncode == 0, 'git archive')
    with tarfile.open(archive) as tf: tf.extractall(SOURCE, filter='data')
    (RUN / 'ref.txt').write_text(upper + '\n')
    if MUTATION or (NEGATIVE and sys.argv[1] in ('오류-02', '스크립트-02')):
        mutation = MUTATION or ('models-exception' if sys.argv[1] == '오류-02' else 'verbose-commands')
        check(mutation in ('models-exception', 'ignore-timeout', 'verbose-commands'), 'known mutation')
        script = SOURCE / SCRIPT
        script.rename(script.with_name('codex-audit-original.sh'))
        prefix = {
            'models-exception': 'if [ "$1" = models ] && [ -f "$PROGRESS_STATE/failure-active" ]; then printf "Traceback: unhandled fixture exception\\n" >&2; exit 1; fi\n',
            'ignore-timeout': 'if [ -f "$PROGRESS_STATE/failure-timeout" ]; then export CODEX_AUDIT_CHECK_TIMEOUT=30; fi\n',
            'verbose-commands': 'if [ "$1" = follow ]; then for i in $(seq 1 40); do printf "[00:00:00] 명령 시작 fixture-%s\\n" "$i"; done; fi\n',
        }[mutation]
        script.write_text('#!/usr/bin/env bash\n' + prefix + 'exec bash "$(dirname -- "$0")/codex-audit-original.sh" "$@"\n')
    elif NEGATIVE:
        if sys.argv[1] == '진단-02':
            (SOURCE / SCRIPT).write_text('#!/usr/bin/env bash\nif then\n')
        elif sys.argv[1] in ('스킬-01','재사용-01'):
            for file in DOCS:
                p=SOURCE/file; p.write_text(p.read_text().replace('follow','REMOVED'))
        elif sys.argv[1] == '구조-03':
            p=SOURCE/'.harness/project.yaml'; p.write_text(p.read_text().replace('premeasure:','removed:'))
        elif sys.argv[1] not in ('스킬-02','구조-02','금지-03','금지-04','진단-01','진단-03'):
            (SOURCE / SCRIPT).write_text('#!/usr/bin/env bash\nexit 0\n')

def lines(text):
    return [re.sub(r'^\[\d{2}:\d{2}:\d{2}\]\s*', '', s) for s in text.splitlines() if s.strip()]

def has(text, pattern):
    check(re.search(pattern, text, re.M) is not None, 'output matches ' + pattern)

class Process:
    def __init__(self, case, args):
        self.case, self.rows = case, []
        self.started = time.monotonic()
        self.args = list(map(str, args))
        self.proc = subprocess.Popen(['bash', str(case.repo / SCRIPT), *self.args], cwd=case.repo,
            env=case.env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, start_new_session=True)
        PROCESSES.append(self)
        def read():
            for row in self.proc.stdout:
                self.rows.append((time.monotonic() - self.started, row.rstrip('\n')))
        self.reader = threading.Thread(target=read, daemon=True)
        self.reader.start()
    def text(self): return '\n'.join(row for _, row in self.rows)
    def until(self, predicate, seconds=5):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if predicate(): return
            if self.proc.poll() is not None:
                self.reader.join(1)
                if predicate(): return
                break
            time.sleep(.05)
        check(False, 'live deadline: ' + ' '.join(self.args) + '\n' + self.text())
    def finish(self, rc, timeout=20):
        try: actual = self.proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired: raise AssertionError('command did not terminate: ' + ' '.join(self.args))
        self.reader.join(2)
        check(actual == rc, 'exit expected=%s actual=%s: %s' % (rc, actual, self.text()))
        return self.text()

class Case:
    def __init__(self, name, steps=('approve',), premeasure=False):
        self.root = RUN / name
        self.root.mkdir()
        self.repo = self.root / 'repo with spaces'
        self.repo.mkdir()
        shutil.copytree(SOURCE / 'harness', self.repo / 'harness')
        self.meta = self.repo / '.harness'
        self.meta.mkdir()
        self.contract = self.meta / 'sprint-contract-sample.md'
        self.contract.write_text(CONTRACT)
        self.home = self.root / 'home'
        self.qa = self.home / '.codex-qa'
        self.qa.mkdir(parents=True)
        (self.qa / 'auth.json').write_text(json.dumps(dict(OPENAI_API_KEY=KEY)))
        (self.qa / 'auth.json').chmod(0o600)
        (self.qa / 'config.toml').write_text('model = "fixture-supervisor"\ncli_auth_credentials_store = "file"\n')
        (self.home / '.claude').mkdir()
        (self.home / '.claude/settings.json').write_text('{"fixture":"unchanged"}\n')
        self.state = self.root / 'state'
        self.state.mkdir()
        (self.state / 'contract.txt').write_text(CONTRACT)
        self.plan(steps)
        self.discovery()
        bins = self.root / 'bin'
        bins.mkdir()
        for name in ('codex', 'npm', 'osascript', 'terminal-notifier', 'notify-send', 'afplay'):
            shutil.copyfile(HERE / 'fake.py', bins / name)
            (bins / name).chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.qa), CODEX_BIN=str(bins / 'codex'),
            PATH=str(bins) + os.pathsep + os.environ['PATH'], PROGRESS_STATE=str(self.state),
            TMPDIR=str(self.root), PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_NOSYSTEM='1',
            GIT_CONFIG_GLOBAL=os.devnull, CODEX_AUDIT_LIMIT='180', CODEX_AUDIT_CHECK_TIMEOUT='2',
            CODEX_AUDIT_MODELS_URL='http://127.0.0.1:9/v1/models')
        for key in ('GIT_DIR', 'GIT_WORK_TREE', 'HARNESS_CONTRACT', 'CLAUDE_CODE_SESSION_ID', 'OPENAI_API_KEY'):
            self.env.pop(key, None)
        self.config = 'contract_categories:\n  - id: Script\n    prefix: 스크립트\ncodex_audit:\n  mode: codex\n  codex_home: ' + json.dumps(str(self.qa)) + '\n  max_rounds: 20\n'
        if premeasure:
            (self.repo / 'prem.py').write_text('import sys,time,os\nfrom pathlib import Path\ns=Path(os.environ["PROGRESS_STATE"])\n(s/("prem-start-"+sys.argv[1][-2:])).touch()\nwhile not (s/("prem-go-"+sys.argv[1][-2:])).exists(): time.sleep(.05)\ntime.sleep(1)\nprint("fixture measurement",sys.argv[1])\n(s/("prem-done-"+sys.argv[1][-2:])).touch()\nsys.exit(0 if sys.argv[1].endswith("01") else 7)\n')
            self.config += '  premeasure: "python3 prem.py {id}"\n'
        (self.meta / 'project.yaml').write_text(self.config)
        (self.repo / 'fixture.txt').write_text('GOOD\n')
        for args in (['init', '-q'], ['config', 'user.name', 'fixture'], ['config', 'user.email', 'fixture@example.invalid'], ['add', '.'], ['commit', '-qm', 'fixture']):
            p = command(['git', *args], self.repo, self.env)
            check(p.returncode == 0, 'fixture git ' + str(args))
        self.base = command(['git', 'rev-parse', 'HEAD'], self.repo, self.env).stdout.strip()
        self.requirements = self.root / 'requirements.md'; self.requirements.write_text('fixture requirement')
        self.critique = self.root / 'critique.md'; self.critique.write_text('fixture critique')
        CASES.append(self)
    def discovery(self, models=None, version='1.2.3', **kwargs):
        (self.state / 'discovery.json').write_text(json.dumps(dict(models=models or ['gpt-fixture-old'], version=version, **kwargs)))
    def plan(self, steps): (self.state / 'plan.json').write_text(json.dumps(list(steps)))
    def release(self, count=10, phases=True):
        for i in range(count): (self.state / ('go-' + str(i))).touch()
        if phases:
            for name in ('command-go','answer-go'): (self.state/name).touch()
    def calls(self):
        p = self.state / 'calls.jsonl'
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
    def execs(self): return [x for x in self.calls() if x['kind'] == 'exec']
    def audit(self, verb='impl', detach=False):
        if verb == 'draft': self.contract.write_text('')
        args = {'impl': [self.contract, self.base], 'draft': [self.requirements, self.contract], 'revise': [self.contract, self.critique]}[verb]
        return Process(self, [verb, *args, *(['--detach'] if detach else [])])
    def folder(self):
        candidates = list((self.meta / 'codex-audit/sample').glob('*-r*'))
        check(bool(candidates), 'audit folder allocated')
        return max(candidates, key=lambda p: p.stat().st_mtime_ns)
    def follow(self, target=None, *options):
        return Process(self, ['follow', target or self.folder(), *options])

def final(p, verdict='APPROVE', rc=0):
    text = p.finish(rc)
    nonempty = text.splitlines()
    check(bool(nonempty), 'follow emits lines')
    check(all(re.match(r'^\[\d{2}:\d{2}:\d{2}\] ', x) for x in nonempty), 'every follow line has timestamp')
    check(lines(text)[-1].startswith('감독 판정: ' + verdict), 'last line verdict')
    has(nonempty[-1], r'총\s*\d+.*초')
    return text

def live():
    cases = list(itertools.product(('draft', 'revise', 'impl'), ('folder', 'contract')))
    print('cases_total=' + str(len(cases)))
    for verb, target in cases:
        c = Case(verb + '-' + target, [verb if verb != 'impl' else 'approve'], premeasure=verb == 'impl')
        if target == 'contract': f = c.follow(c.contract, '--wait-seconds', '10', '--summary-seconds', '2')
        a = c.audit(verb)
        a.until(lambda: bool(list((c.meta/'codex-audit/sample').glob('*-r*'))))
        if target == 'folder': f = c.follow(None, '--summary-seconds', '2')
        f.until(lambda: '감독 시작' in f.text())
        if verb=='impl':
            a.until(lambda: (c.state/'prem-start-01').exists())
            (c.state/'prem-go-01').touch()
            a.until(lambda: (c.state/'prem-done-01').exists())
            f.until(lambda: re.search(r'사전 측정\s*1/2.*스크립트-01',f.text()) is not None)
            check(not c.execs(),'first measurement progress visible before Codex starts')
            (c.state/'prem-go-02').touch()
        a.until(lambda: bool(c.execs()))
        f.until(lambda: '감독 시작' in f.text() and re.search(r'(?:차례|판정|작성|draft|revise).*시작.*fixture-supervisor', f.text()))
        check(a.proc.poll() is None, 'visible before supervisor completion')
        has(f.text(), verb)
        has(f.text(), r'(?:draft|impl|revise)-r\d+')
        has(f.text(), r'조건\s*(?:2|미정|확인 중|알 수 없음)')
        has(f.text(), r'fixture-supervisor.*medium')
        if verb == 'impl':
            has(f.text(), r'사전 측정\s*1/2.*스크립트-01.*종료\s*0.*\d+.*초')
            has(f.text(), r'사전 측정\s*2/2.*스크립트-02.*종료\s*7.*\d+.*초')
            has(f.text(), r'사전 측정.*끝.*\d+.*초')
        c.release(); a.finish(0); text = final(f)
        has(text, r'(?:차례|판정|작성|draft|revise).*끝.*APPROVE')
        if verb == 'impl': has(text, r'PASS\s*2.*FAIL\s*0')

# Shared public line classes; UI review uses the same relay boundary.
MAJOR = r'감독 시작|사전 측정.*끝|(?:차례|판정|작성|draft|revise).*?(?:시작|끝)|다시 시도|조사|재심|감독 판정:'
WARNING = r'오류|모델 확인 못 함:|Codex 조용함|생각 중.*기록은 자람'
SUMMARY = r'활동 요약.*명령\s*(\d+)개.*지금\s*(자료 읽기|측정 시험|파일 쓰기|생각 중|답 작성)'

def relay_line(row):
    return bool(re.search(MAJOR, row) or re.search(WARNING, row)) and not re.search(SUMMARY, row)

def summary_budget(f, interval):
    rows = [(t, x) for t, x in f.rows if x.strip()]
    summaries = [(t, x) for t, x in rows if re.search(SUMMARY, x)]
    major = [(t, x) for t, x in rows if re.search(MAJOR, x) and not re.search(SUMMARY, x)]
    warnings = [(t, x) for t, x in rows if re.search(WARNING, x) and not re.search(SUMMARY, x)]
    check(len(major) <= 5, 'one start/round start/round end/final, optional premeasure end')
    check(len(rows) == len(summaries) + len(major) + len(warnings), 'no per-command or unclassified activity lines')
    check(all(b[0] - a[0] >= interval - .25 for a, b in zip(summaries, summaries[1:])), 'at most one summary per interval')
    check(len(summaries) <= int(rows[-1][0] / interval), 'summary count bounded by elapsed complete intervals')
    check(len(rows) <= len(major) + int(rows[-1][0] / interval) + len(warnings), 'total output bounded by phases + elapsed intervals + warnings')
    check('private reasoning' not in f.text() and 'Traceback' not in f.text(), 'private reasoning and parsing errors not exposed')
    return summaries

def events():
    c = Case('events', ['summary']); c.env['CODEX_AUDIT_LIMIT'] = '240'
    f = c.follow(c.contract, '--summary-seconds', '2', '--idle-seconds', '30')
    a = c.audit(); a.until(lambda: bool(c.execs()))
    c.release(phases=False)
    expected = [('read', '자료 읽기', 40), ('test', '측정 시험', 40), ('write', '파일 쓰기', 40), ('reason', '생각 중', 0), ('answer', '답 작성', 0)]
    for stage, activity, count in expected:
        a.until(lambda: (c.state / ('stage-' + stage)).exists())
        f.until(lambda: any(re.search(SUMMARY, x) and activity in x for _, x in f.rows), 5)
        check(a.proc.poll() is None, 'activity summary flushed before completion: ' + stage)
        (c.state / ('next-' + stage)).touch()
    a.finish(0); final(f)
    summaries = summary_budget(f, 2)
    for stage, activity, count in expected:
        matches = [re.search(SUMMARY, x) for _, x in summaries if activity in x]
        check(sum(int(m.group(1)) for m in matches) == count, 'unique commands since preceding summary: ' + stage)
    errors = [(t, x) for t, x in f.rows if '오류' in x and '7' in x]
    check(len(errors) == 1, 'one immediate command error, no duplicate update error')
    emitted = float((c.state / 'error-at').read_text())
    check(0 <= f.started + errors[0][0] - emitted <= 5, 'error flushed within 5 seconds')
    # The shortened option must not accidentally change the public default.
    c = Case('summary-default', ['summary-default']); c.env['CODEX_AUDIT_LIMIT'] = '120'
    f = c.follow(c.contract)
    a = c.audit(); a.until(lambda: bool(c.execs())); c.release(phases=False)
    a.until(lambda: (c.state / 'stage-default').exists())
    f.until(lambda: any('오류' in x and '7' in x for _, x in f.rows), 5)
    errors = [(t, x) for t, x in f.rows if '오류' in x and '7' in x]
    check(len(errors) == 1 and 0 <= f.started + errors[0][0] - float((c.state / 'error-at').read_text()) <= 5, 'default error is immediate, not deferred to minute summary')
    while time.monotonic() - f.started < 58:
        check(not any(re.search(SUMMARY, x) for _, x in f.rows), 'default has no early activity summary')
        check(not any('명령 시작' in x or '명령 끝' in x for _, x in f.rows), 'command burst does not emit individual lines')
        time.sleep(.2)
    f.until(lambda: any(re.search(SUMMARY, x) for _, x in f.rows), 7)
    (c.state / 'next-default').touch(); a.finish(0); final(f)
    summaries = summary_budget(f, 60)
    check(len(summaries) == 1 and int(re.search(SUMMARY, summaries[0][1]).group(1)) == 40, 'default minute summarizes forty commands exactly once')


def quiet():
    for mode in ('still', 'grow', 'decoy-grow'):
        c = Case('quiet-' + mode); a = c.audit(); a.until(lambda: bool(c.execs()))
        if mode != 'still': (c.state / mode).touch()
        f = c.follow(None, '--idle-seconds', '2'); f.until(lambda: '감독 시작' in f.text())
        f.until(lambda: len([x for x in lines(f.text()) if ('조용함' in x or '기록은 자람' in x)]) >= 2, 8)
        if mode == 'grow':
            has(f.text(), r'생각 중.*기록은 자람')
            check('멈춤 의심' not in f.text(), 'growing matching session is distinguished')
        else: has(f.text(), r'Codex 조용함\s*\d+초.*생각 중이거나 멈춤 의심')
        timed = [(t,x) for t,x in f.rows if '조용함' in x or '기록은 자람' in x]
        check(all(b[0]-a0[0] >= 1.5 for a0,b in zip(timed,timed[1:])), 'idle notification rate bounded')
        check(a.proc.poll() is None, 'silence alone is not a terminal failure')
        c.release(); a.finish(0); final(f)
    c = Case('quiet-default'); a = c.audit(); a.until(lambda: bool(c.execs()))
    f = c.follow(); f.until(lambda: '감독 시작' in f.text())
    start = float((c.state/'last-event-at').read_text())
    while time.monotonic() - start < 58:
        check(not any('조용함' in x or '기록은 자람' in x for _,x in f.rows), 'default does not warn before 60 seconds (2s polling tolerance)')
        time.sleep(.5)
    f.until(lambda: '조용함' in f.text(), 7)
    c.release(); a.finish(0); final(f)

def replay():
    for step, verdict, rc in [('approve','APPROVE',0), ('reject','REJECT',1), ('quota','BLOCKED',2)]:
        c = Case('replay-' + step, [step,step]); c.release(); a = c.audit(); a.finish(rc)
        folder = c.folder(); before = digest_tree(folder)
        one = final(c.follow(folder), verdict, rc); two = final(c.follow(folder), verdict, rc)
        check(lines(one) == lines(two), 'replay is deterministic except timestamps')
        has(one, '감독 시작')
        if step != 'quota': has(one, r'(?:차례|판정).*시작')
        check(before == digest_tree(folder), 'follower does not mutate audit artifacts')
    c = Case('skip-archive'); folder = c.meta / 'codex-audit/sample/impl-r1'; folder.mkdir(parents=True)
    (folder / 'report.md').write_text('시작: 2026-10-06 00:00:00\n끝: 2026-10-06 00:00:01\n단계: impl\n\n감독 판정: SKIPPED\n')
    final(c.follow(folder), 'SKIPPED', 3)

def selection():
    c = Case('selection'); c.release(); c.audit().finish(0)
    old = c.folder()
    f = c.follow(c.contract, '--wait-seconds', '10')
    time.sleep(.7); check(f.proc.poll() is None, 'completed-only contract waits for a new audit')
    for p in c.state.glob('go-*'): p.unlink()
    a = c.audit(); a.until(lambda: len(c.execs()) >= 2)
    new = c.folder(); check(new != old, 'new audit allocated')
    f.until(lambda: new.name in f.text())
    g = c.follow(c.contract, '--wait-seconds', '10'); g.until(lambda: new.name in g.text())
    other = c.meta / 'codex-audit/other/impl-r99'; other.mkdir(parents=True)
    (other / 'report.md').write_text('감독 판정: REJECT\n')
    c.release(); a.finish(0); final(f); final(g)
    for stream in (f,g): check('impl-r99' not in stream.text(), 'contract isolation')
    empty = Case('empty-wait'); t = time.monotonic()
    q = empty.follow(empty.contract, '--wait-seconds', '2'); q.finish(2, 6)
    check(1.5 <= time.monotonic()-t <= 6, 'bounded wait when no audit exists')
    has(q.text(), r'(?:기다|대기|감독).*'); has(q.text(), 'BLOCKED')

def branches():
    for name, steps, rc, verdict, words in [
        ('empty',['empty','approve'],0,'APPROVE',['다시 시도','빈']),
        ('timeout',['timeout','approve'],0,'APPROVE',['다시 시도','시간']),
        ('research',['research','research-answer','approve'],0,'APPROVE',['조사','RESEARCH']),
        ('review',['reject','reject'],1,'REJECT',['재심','REJECT'])]:
        c = Case(name, steps)
        for i in range(len(steps)-1): (c.state/('go-'+str(i))).touch()
        if name == 'timeout': c.env['CODEX_AUDIT_LIMIT'] = '8'
        f=c.follow(c.contract,'--wait-seconds','10')
        a = c.audit(); a.until(lambda: len(c.execs())==len(steps),15)
        f.until(lambda: all(word in f.text() for word in words))
        check(a.proc.poll() is None,'retry/research/review visible while audit runs')
        c.release(); a.finish(rc,25); text=final(f,verdict,rc)
        check(len(c.execs()) == len(steps), 'expected phase/retry count')
        for word in words: has(text, word)

class Discovery:
    def __init__(self, case):
        self.requests = []
        outer = self
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_GET(self):
                spec = json.loads((case.state / 'discovery.json').read_text())
                outer.requests.append(dict(path=self.path, authorized=self.headers.get('Authorization') == 'Bearer ' + KEY))
                if spec.get('http_delay'): time.sleep(spec['http_delay'])
                self.send_response(spec.get('status',200)); self.end_headers()
                body = '{broken' if spec.get('malformed') else json.dumps(dict(data=[dict(id=i, object='model') for i in spec['models']]))
                try: self.wfile.write(body.encode())
                except (BrokenPipeError, ConnectionResetError): pass
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1',0), Handler)
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        case.env['CODEX_AUDIT_MODELS_URL'] = 'http://127.0.0.1:%d/v1/models' % self.server.server_port
    def close(self): self.server.shutdown(); self.server.server_close()

def models():
    c = Case('models'); server = Discovery(c)
    try:
        first = Process(c,['models']); first.finish(0)
        check('새 모델:' not in first.text() and '새 Codex 판:' not in first.text(), 'first observation is silent baseline')
        for word in ('fixture-supervisor','1.2.3','설치','최신'): has(first.text(), word)
        c.discovery(['gpt-fixture-old','gpt-fixture-new','embedding-fixture'], '1.3.0')
        second = Process(c,['models']); second.finish(0)
        has(second.text(), r'새 모델:.*gpt-fixture-new.*지금 감독 모델.*fixture-supervisor')
        has(second.text(), r'새 Codex 판:.*1.3.0.*설치.*1.2.3')
        check('새 모델: embedding-fixture' not in second.text(), 'non GPT model not announced as GPT')
        c.discovery(['embedding-fixture','gpt-fixture-new','gpt-fixture-old'], '1.3.0')
        third = Process(c,['models']); third.finish(0)
        check('새 모델:' not in third.text() and '새 Codex 판:' not in third.text(), 'persistent set comparison, no repeat or reorder notification')
        c.discovery(['gpt-fixture-new'], '1.1.0')
        fourth = Process(c,['models']); fourth.finish(0)
        check('새 모델:' not in fourth.text() and '새 Codex 판:' not in fourth.text(), 'removal and older version are not new releases')
        check(not c.execs() and not (c.meta/'codex-audit').exists(), 'models does not start a supervisor')
        check(server.requests and all(x['authorized'] for x in server.requests), 'uses supervisor account authentication')
        check(all(x['path']=='/v1/models' for x in server.requests),'uses supplied models URL')
        check((c.qa/'config.toml').read_text().startswith('model = "fixture-supervisor"'), 'discovery does not change configured model')
        check(any(p.is_file() and p.name not in ('auth.json','config.toml') for p in c.qa.rglob('*')), 'memory resides in supervisor home')
        check(all(x['args']==['view','@openai/codex','version'] for x in c.calls() if x['kind']=='npm'),'correct registry package and field')
        no_leak(c)
    finally: server.close()

def automatic():
    for verb in ('draft','revise','impl'):
        c = Case('automatic-' + verb, [verb if verb != 'impl' else 'approve']); server = Discovery(c)
        try:
            Process(c,['models']).finish(0)
            c.discovery(['gpt-fixture-old','gpt-fixture-new'], '1.3.0')
            old_config = (c.qa/'config.toml').read_bytes()
            a = c.audit(verb); a.until(lambda: bool(c.execs()), 10)
            f = c.follow(); f.until(lambda: '새 모델:' in f.text() and '새 Codex 판:' in f.text())
            notices = lines(f.text())
            check('새 모델:' in notices[0] or '새 Codex 판:' in notices[0], 'discovery announcement precedes phase output')
            c.release(); a.finish(0); final(f)
            report = (c.folder()/'report.md').read_text()
            has(report, r'새 모델:.*gpt-fixture-new'); has(report, r'새 Codex 판:.*1.3.0')
            check(all(x['model']=='fixture-supervisor' for x in c.execs()), 'new model never selected automatically')
            check((c.qa/'config.toml').read_bytes()==old_config, 'supervisor config unchanged')
            check(len(server.requests)>=2, 'audit itself checks discovery')
            no_leak(c)
        finally: server.close()

def errors():
    c = Case('errors')
    folder=c.meta/'codex-audit/sample/impl-r1'; folder.mkdir(parents=True)
    (folder/'report.md').write_text('시작: 2026-10-06 00:00:00\n끝: 2026-10-06 00:00:01\n단계: impl\n\n감독 판정: SKIPPED\n')
    final(c.follow(folder),'SKIPPED',3)
    cases = [[], [c.root/'missing'], [c.contract,'--idle-seconds','0'], [c.contract,'--idle-seconds','no'], [c.contract,'--wait-seconds','-1'], [c.contract,'--unknown'], [c.contract,'--summary-seconds','0'], [c.contract,'--summary-seconds','no']]
    print('cases_total=' + str(len(cases)))
    for args in cases:
        p = Process(c,['follow',*args]); p.finish(64,5)
        check(bool(p.text().strip()) and 'Traceback' not in p.text(), 'invalid input explains usage without traceback')

def discovery_failure_output(text):
    notices = [x for x in lines(text) if '모델 확인 못 함:' in x]
    check(len(notices) == 1, 'one discovery failure line')
    has(notices[0], r'모델 확인 못 함:\s*\S+')
    check('Traceback' not in text, 'no unhandled discovery exception')

def standalone_failure(c, name, started):
    p = Process(c, ['models'])
    p.finish(2, 4 if name == 'timeout' else 15)
    discovery_failure_output(p.text())
    check(not c.execs() and not (c.meta/'codex-audit').exists(), 'failed standalone models creates no audit or exec')
    if name == 'timeout': check(time.monotonic()-started < 4, '2s lookup bound: standalone returns before 4s despite 5s server delay')

def discovery_failures():
    specs = [('unauthorized',dict(status=401)), ('malformed',dict(malformed=True)), ('timeout',dict(http_delay=5)), ('registry',dict(npm_fail=True)), ('missing-npm',{}), ('missing-auth',{})]
    cases = list(itertools.product(specs, ('models', 'draft', 'revise', 'impl')))
    print('cases_total=' + str(len(cases)))
    for (name, spec), route in cases:
        c = Case('discovery-failure-' + name + '-' + route, [route if route in ('draft','revise') else 'approve'])
        server = Discovery(c)
        try:
            Process(c,['models']).finish(0)
            c.discovery(**spec)
            (c.state/'failure-active').touch()
            if name == 'timeout': (c.state/'failure-timeout').touch()
            original_path = c.env['PATH']
            auth = (c.qa/'auth.json').read_bytes()
            if name == 'missing-auth': (c.qa/'auth.json').unlink()
            if name == 'missing-npm':
                isolated = c.root/'isolated-bin'; isolated.mkdir()
                for tool in ('bash','python3','git','tar','curl','codex','sh','dirname','mkdir','cat','date','sleep','mktemp','chmod','cp','mv','sed','awk','grep','sort','head','tail','wc','tr','uname','cut','readlink','stat','env','tee'):
                    found = shutil.which(tool, path=c.env['PATH'])
                    if found: (isolated/tool).symlink_to(found)
                c.env['PATH'] = str(isolated)
            before = len(server.requests); c.release(); started = time.monotonic()
            if route == 'models':
                standalone_failure(c, name, started)
            else:
                f = c.follow(c.contract)
                a = c.audit(route)
                if name == 'timeout':
                    a.until(lambda: bool(c.execs()), 4)
                    check(time.monotonic()-started < 4, '2s lookup bound: audit reaches exec before 4s despite 5s server delay')
                a.finish(0, 15); text = final(f)
                check(time.monotonic()-started < 15, 'discovery failure does not indefinitely delay audit')
                discovery_failure_output(text)
                discovery_failure_output((c.folder()/'report.md').read_text())
                check(len(c.execs()) == 1, 'failure did not stop or retry audit')
            check(len(server.requests)-before <= 1, 'no discovery retry storm')
            c.env['PATH'] = original_path
            (c.qa/'auth.json').write_bytes(auth); (c.qa/'auth.json').chmod(0o600)
            (c.state/'failure-active').unlink()
            if (c.state/'failure-timeout').exists(): (c.state/'failure-timeout').unlink()
            # Same successful observation must still be remembered after failure.
            c.discovery()
            unchanged = Process(c, ['models']); unchanged.finish(0)
            check('새 모델:' not in unchanged.text() and '새 Codex 판:' not in unchanged.text(), 'failure did not replace success memory with empty values')
            c.discovery(['gpt-fixture-old','gpt-fixture-recovered'],'1.3.0')
            recovered = Process(c,['models']); recovered.finish(0)
            has(recovered.text(),r'새 모델:.*gpt-fixture-recovered')
            has(recovered.text(),r'새 Codex 판:.*1.3.0')
            no_leak(c)
        finally: server.close()


def wait_compat():
    for step,rc,verdict in [('approve',0,'APPROVE'),('reject',1,'REJECT'),('quota',2,'BLOCKED')]:
        c=Case('wait-'+step,[step,step]); c.release()
        a=c.audit(detach=True); text=a.finish(0)
        check(Path(text.strip()).is_dir(), 'detach stdout remains one folder path')
        q=Process(c,['wait',text.strip(),'20']); q.finish(rc,25)
        check(q.text().strip()=='감독 판정: '+verdict, 'legacy wait terminal output unchanged')
    c=Case('wait-running'); a=c.audit(detach=True); folder=a.finish(0).strip()
    q=Process(c,['wait',folder,'0']); q.finish(75); check(q.text()=='RUNNING '+folder,'wait running code and output')
    c.release(); Process(c,['wait',folder,'20']).finish(0,25)
    (c.meta/'project.yaml').write_text(c.config.replace('mode: codex','mode: off'))
    p=c.audit(); p.finish(3); has(p.text(),'SKIPPED')

def digest_tree(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}

def no_leak(c):
    leaks=[str(p.relative_to(c.root)) for p in c.root.rglob('*') if p.is_file() and p!=c.qa/'auth.json' and KEY.encode() in p.read_bytes()]
    check(not leaks,'no fixture key outside source auth: '+str(leaks))
    for p in PROCESSES:
        if p.case==c: check(KEY not in p.text(),'no fixture key in stdout/stderr')

def secrets():
    for step in ('secret','quota'):
        c=Case('secret-'+step,[step]); before=(c.qa/'auth.json').read_bytes(); c.release()
        rc=2 if step=='quota' else 0; a=c.audit(); a.finish(rc)
        final(c.follow(), 'BLOCKED' if rc else 'APPROVE',rc)
        leaks=[str(p.relative_to(c.root)) for p in c.root.rglob('*') if p.is_file() and p!=c.qa/'auth.json' and KEY.encode() in p.read_bytes()]
        check(not leaks,'no secret in output, audit files, cache or temporary copies: '+str(leaks))
        check((c.qa/'auth.json').read_bytes()==before,'original auth unchanged')
        check((c.home/'.claude/settings.json').read_text()=='{"fixture":"unchanged"}\n','user settings unchanged')
        check(not any(x['kind']=='forbidden-notification' for x in c.calls()),'no OS notification command')
        for p in PROCESSES:
            if p.case==c: check(KEY not in p.text(),'no secret on stdout/stderr')

def scope():
    upper=git('rev-parse','--verify','-q',BRANCH)
    for args in [('diff','--name-only'),('diff','--cached','--name-only'),('ls-files','--others','--exclude-standard')]:
        dirty=git(*args).splitlines()
        check(all(p.startswith('.harness/') for p in dirty),'implementation committed before scope measurement')
    paths=git('diff','--no-renames','--name-only',BASE+'..'+upper,'--','.',':(exclude).harness').splitlines()
    if NEGATIVE: paths.append('outside-fixture.txt')
    allowed=[SCRIPT,'harness/scripts/codex-audit/','harness/templates/codex-audit/',*DOCS,'harness/README.md']
    check(SCRIPT in paths,'nonempty implementation change includes public entry point')
    check(all(any(p==a or (a.endswith('/') and p.startswith(a)) for a in allowed) for p in paths),'only permitted implementation paths: '+str(paths))
    for p in ('harness/.claude-plugin/plugin.json','.claude-plugin/marketplace.json'):
        check(git('diff',BASE+'..'+upper,'--',p)=='','version/marketplace unchanged: '+p)
    changed=git('diff','--no-renames','--name-only',BASE+'..'+upper,'--','.harness/project.yaml')
    if changed:
        patch=git('diff','--unified=0',BASE+'..'+upper,'--','.harness/project.yaml')
        edits=[x[1:] for x in patch.splitlines() if x[:1] in ('+','-') and not x.startswith(('+++','---'))]
        check(all(not x.strip() or x.lstrip().startswith(('#','premeasure:')) for x in edits),'project config changes only premeasure/comment lines')

def docs():
    for file in DOCS:
        text=(SOURCE/file).read_text()
        paras=[p for p in text.split('\n\n') if 'follow' in p]
        check(paras,'follow instructions in '+file)
        block='\n'.join(paras)
        for pattern in (r'부모',r'백그라운드|run_in_background',r'항상|요청.*없',r'단계',r'채팅|대화',r'계약',r'시작|동시',r'큰 단계',r'오류',r'조용함',r'최종 판정',r'요약',r'60',r'채팅.*(?:만|제외|옮기지)|(?:만|제외).*채팅'):
            has(block,pattern)
        check(all(x in text for x in ('draft','revise','impl')),'all supervisor verbs documented: '+file)
    table=(SOURCE/'harness/README.md').read_text()
    check(any(x.startswith('|') and 'follow' in x and 'codex-audit' in x for x in table.splitlines()),'README command table includes follow')
    has(table,'models')

def ui_review():
    file=W/'.harness/.meta/codex-audit-progress/evidence/ui-review.json'
    check(file.is_file(),'UI evidence missing; see ui-review.md')
    data=json.loads(file.read_text())
    expected=set(itertools.product(('draft','revise','impl'),('direct','delegated')))
    print('cases_total='+str(len(expected)))
    rows=data['cases']; check(len(rows)==len(expected),'six UI cases')
    if NEGATIVE: rows[-1]['run_in_background']=False
    check({(x['verb'],x['route']) for x in rows}==expected,'UI matrix covers all combinations')
    for row in rows:
        check(row['reviewer'] and row['reviewer']!=row['implementer'],'independent reviewer identified')
        for key in ('transcript','capture','stdout'):
            p=file.parent/row[key]['path']; check(p.is_file() and p.stat().st_size>0,'real UI artifact '+key)
            check(hashlib.sha256(p.read_bytes()).hexdigest()==row[key]['sha256'],'UI artifact hash '+key)
        check(row['follow_actor']==row['parent_session'] and row['run_in_background'] is True,'follow executed by parent in background')
        check(row['user_requested_progress'] is False,'automatic without progress request')
        check(row['follow_started']<=row['first_phase_at']<row['finished_at'],'follower active before first phase')
        check(len(row['phases'])>=2,'at least two observable phase transitions')
        transcript=(file.parent/row['transcript']['path']).read_text().splitlines()
        stdout=(file.parent/row['stdout']['path']).read_text().splitlines()
        required={i+1 for i,s in enumerate(stdout) if relay_line(s)}
        check({x['stdout_location'] for x in row['phases']}==required,'only major phases, errors, quiet warnings and final verdict relayed')
        for phase in row['phases']:
            check(phase['stdout_line'] and phase['chat_line'] and phase['capture_location'] and phase['transcript_location'],'located phase evidence')
            check(stdout[phase['stdout_location']-1]==phase['stdout_line'],'actual stdout line matches evidence')
            check(phase['chat_line'] in transcript[phase['transcript_location']-1],'actual transcript contains relayed chat line')
            check(0<=phase['chat_at']-phase['stdout_at']<=15,'chat relay within 15 seconds')
        check(row['card_visible_during_run'] is True and row['review_verdict']=='PASS','reviewer verified visible refreshing card and each relay')

def configuration():
    text=(SOURCE/'.harness/project.yaml').read_text()
    has(text,r'premeasure:\s*[\"\x27]?bash \.harness/\.meta/codex-audit-progress/measure/measure\.sh \{id\}')
    readme=(SOURCE/'harness/README.md').read_text()
    for token in ('CODEX_AUDIT_MODELS_URL','CODEX_AUDIT_CHECK_TIMEOUT','--idle-seconds','--wait-seconds','--summary-seconds'):
        has(readme,re.escape(token))

def validate(kind):
    if NEGATIVE:
        p=SOURCE/DOCS[0]
        if kind=='code-fence': p.write_text(p.read_text()+'\n```\nbad fence\n```\n')
        else: p.write_text(re.sub(r'^name:.*\n','',p.read_text(),count=1,flags=re.M))
    p=command(['python3','scripts/validate-plugin.py','--check='+kind], SOURCE)
    (RUN/('validate-'+kind+'.txt')).write_text(p.stdout+p.stderr)
    check(p.returncode==0,'configured validator exits zero: '+p.stdout+p.stderr)
    has(p.stdout+p.stderr, 'V6' if kind=='code-fence' else 'V1')

def syntax():
    for shell in ('bash','zsh'):
        p=command([shell,'-n',SOURCE/SCRIPT]); check(p.returncode==0 and not p.stderr,'shell syntax '+shell)
    text=(SOURCE/SCRIPT).read_text()
    if "<<'PY'" in text:
        compile(text.split("<<'PY'",1)[1].split('\n',1)[1].rsplit('\nPY',1)[0],SCRIPT,'exec')
    for p in (SOURCE/'harness/scripts/codex-audit').rglob('*.py') if (SOURCE/'harness/scripts/codex-audit').is_dir() else []:
        compile(p.read_text(),str(p),'exec')

def na():
    upper=git('rev-parse','--verify','-q',BRANCH)
    result=git('diff','--name-only',BASE+'..'+upper,'--','scripts/release.sh')
    if NEGATIVE: result='scripts/release.sh'
    check(not result,'N/A: release command target not changed')

def controls():
    check(len(list(itertools.product(('draft','revise','impl'),('folder','contract'))))==6,'known matrix=6')
    check(lines('[12:00:00] 생각 중\n[12:00:01] 감독 판정: APPROVE · 총 1초')==['생각 중','감독 판정: APPROVE · 총 1초'],'known timestamp stripping=2 lines')
    for bad in ('no timestamp','[1:00:00] invalid'):
        check(re.match(r'^\[\d{2}:\d{2}:\d{2}\] ',bad) is None,'bad timestamp rejected')
    p=RUN/'leak-control'; p.write_text(KEY); check(KEY.encode() in p.read_bytes(),'known secret leak=1'); p.unlink()
    print('CONTROLS_ONLY: implementation not evaluated')

def main():
    if len(sys.argv)<2 or sys.argv[1] not in IDS+['--controls-only']:
        raise AssertionError('unknown condition; supported: '+', '.join(IDS))
    if sys.argv[1]=='--controls-only': controls(); return
    snapshot()
    mapping={'스킬-01':docs,'스킬-02':ui_review,'스크립트-01':live,'스크립트-02':events,'스크립트-03':quiet,'스크립트-04':replay,'스크립트-05':selection,'스크립트-06':branches,'스크립트-07':models,'스크립트-08':automatic,'스크립트-09':wait_compat,'오류-01':errors,'오류-02':discovery_failures,'구조-01':secrets,'구조-02':scope,'구조-03':configuration,'금지-03':lambda:validate('code-fence'),'금지-04':lambda:validate('frontmatter'),'재사용-01':docs,'재사용-02':wait_compat,'진단-01':na,'진단-02':syntax,'진단-03':na,'진단-04':events}
    mapping[sys.argv[1]]()

error=None
try: main()
except Exception as exc:
    error=type(exc).__name__+': '+str(exc)
finally:
    for p in PROCESSES:
        if p.proc.poll() is None:
            try: os.killpg(p.proc.pid,signal.SIGTERM); p.proc.wait(timeout=5)
            except (ProcessLookupError,subprocess.TimeoutExpired):
                try: os.killpg(p.proc.pid,signal.SIGKILL); p.proc.wait(timeout=2)
                except ProcessLookupError: pass
        p.reader.join(1)
    for c in CASES:
        for pidfile in c.meta.glob('codex-audit/*/*/pid'):
            try:
                pid=int(pidfile.read_text()); os.kill(pid,signal.SIGTERM)
            except (ValueError,ProcessLookupError,PermissionError): pass
    evidence=dict(condition=sys.argv[1] if len(sys.argv)>1 else '',source_ref=(RUN/'ref.txt').read_text().strip() if (RUN/'ref.txt').exists() else None,checks=CHECKS,error=error,
        processes=[dict(args=p.args,exit=p.proc.poll(),lines=p.rows) for p in PROCESSES])
    (RUN/'result.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
print(('FAIL' if error else 'PASS')+' '+(sys.argv[1] if len(sys.argv)>1 else 'usage')+' evidence='+str(RUN/'result.json'))
if error: print(error)
sys.exit(1 if error else 0)
