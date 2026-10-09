#!/usr/bin/env python3
"""codex-audit-auth-writeback 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

가지 끝 커밋(--base 면 BASE)의 harness/ 를 임시 폴더로 꺼내 가짜 codex 로 감독을 끝까지 돌린다.
자기가 만든 임시 폴더는 끝날 때 지운다 — 앞 스프린트 측정 묶음이 이것을 안 해서 한 폴더에 4.0GB 가 쌓였다.
"""
import datetime
import fcntl
import gzip
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib

HERE = Path(__file__).resolve().parent
W = Path(os.environ.get('MEASURE_W', '/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation'))
BASE, BRANCH = '2f98abee', 'feat/codex-audit-judge-mode'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/README.md']
PREVIOUS = W / '.harness/.meta/codex-audit-subscription/measure/measure.sh'
ALLOWED_NEW = {'codex-audit-usage.jsonl', 'codex-audit-models.json', 'codex-audit-auth.lock'}
FAKE = HERE / 'fake.py'
CHATGPT_AUTH = dict(auth_mode='chatgpt', OPENAI_API_KEY=None, last_refresh='2026-10-08T00:00:00Z',
                    tokens=dict(access_token='original', refresh_token='refresh-fixture', id_token='id-fixture', account_id='acct'))
PRICES = {'gpt-6.1-sol': (2.00, 0.10, 10.00), 'gpt-6-sol': (2.00, 0.20, 10.00), 'gpt-6-luna': (0.10, 0.01, 0.50),
          'gpt-5.6-sol': (4.00, 0.40, 20.00), 'gpt-5.6-terra': (2.00, 0.20, 12.00), 'gpt-5.6-luna': (0.20, 0.02, 1.20)}
MODELS = list(PRICES)
REAL_HOME = Path(pwd.getpwuid(os.getuid()).pw_dir)
REAL_PATH = os.environ['PATH']
USE_BASE = '--base' in sys.argv
POSITIVE = '--positive' in sys.argv
CONTRACT = '''---
feature: "isolation fixture"
created: "2026-10-07 00:00"
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
PREMEASURE = '''import json, os, sys
from pathlib import Path
tmp = Path(os.environ.get("TMPDIR") or "/nonexistent")
record = {key: os.environ.get(key, "") for key in ("TMPDIR", "TMP", "TEMP")}
Path(os.environ["FAKE_STATE"], "prem-" + sys.argv[1] + ".json").write_text(json.dumps(record))
(tmp / "nested" / "deeper").mkdir(parents=True, exist_ok=True)
(tmp / "nested" / "deeper" / "blob.bin").write_bytes(b"0" * 1048576)
Path("left-in-copy.txt").write_text("fixture")
print("fixture measurement", sys.argv[1])
'''
RUN = Path(tempfile.mkdtemp(prefix='cji-measure-'))
LIVE = []


class Fail(Exception):
    pass


def kill_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def check(value, label):
    if not value:
        raise Fail(label)


def git(*args, cwd=W):
    done = subprocess.run(['git', '-C', str(cwd), *map(str, args)], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    check(done.returncode == 0, 'git ' + ' '.join(map(str, args)) + ': ' + done.stderr.strip())
    return done.stdout


def tip():
    found = subprocess.run(['git', '-C', str(W), 'rev-parse', '--verify', '-q', BRANCH], capture_output=True, text=True)
    check(found.returncode == 0 and found.stdout.strip(), 'UNRESOLVED 가지 끝 ' + BRANCH)
    return found.stdout.strip()


def export(ref):
    target = RUN / ('source-' + ref[:12])
    if not target.exists():
        archive = RUN / 'source.tar'
        with archive.open('wb') as sink:
            subprocess.run(['git', '-C', str(W), 'archive', ref, 'harness'], stdout=sink, check=True)
        with tarfile.open(archive) as bundle:
            bundle.extractall(target, filter='data')
        archive.unlink()
    return target


SOURCE_REF = BASE if USE_BASE else None


def source():
    return export(SOURCE_REF or tip())


class Case:
    def __init__(self, name, steps=('approve',), config=None, premeasure=False, model='fixture-supervisor'):
        self.root = RUN / name
        self.root.mkdir()
        self.repo = self.root / 'repo'
        shutil.copytree(source() / 'harness', self.repo / 'harness')
        self.meta = self.repo / '.harness'
        self.meta.mkdir()
        self.contract = self.meta / 'sprint-contract-sample.md'
        self.contract.write_text(CONTRACT)
        self.home = self.root / 'home'
        self.qa = self.home / '.codex-qa'
        self.qa.mkdir(parents=True)
        (self.qa / 'auth.json').write_text(json.dumps(dict(OPENAI_API_KEY='sk-fixture-INVALID-000000000000')))
        (self.qa / 'auth.json').chmod(0o600)
        (self.qa / 'config.toml').write_text('model = "fixture-supervisor"\ncli_auth_credentials_store = "file"\n')
        self.state = self.root / 'state'
        self.state.mkdir()
        (self.state / 'contract.txt').write_text(CONTRACT)
        self.plan(steps)
        self.tmp = self.root / 'tmp'
        self.tmp.mkdir()
        bins = self.root / 'bin'
        bins.mkdir()
        for tool in ('codex', 'npm'):
            shutil.copyfile(FAKE, bins / tool)
            (bins / tool).chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.home), CODEX_BIN=str(bins / 'codex'), FAKE_STATE=str(self.state),
                        PATH=str(bins) + os.pathsep + REAL_PATH, TMPDIR=str(self.tmp) + '/', CODEX_AUDIT_LIMIT='60',
                        CODEX_AUDIT_CHECK_TIMEOUT='2', CODEX_AUDIT_MODELS_URL='http://127.0.0.1:9/v1/models',
                        PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        for key in ('CODEX_HOME', 'CODEX_AUDIT_MODEL', 'CODEX_AUDIT_DRAFT_LIMIT', 'OPENAI_API_KEY', 'HARNESS_CONTRACT'):
            self.env.pop(key, None)
        if config is None:
            config = 'codex_audit:\n  mode: codex\n  codex_home: ' + json.dumps(str(self.qa)) + '\n  model: ' + model + '\n'
        if premeasure:
            (self.repo / 'prem.py').write_text(PREMEASURE)
            config += '  premeasure: "python3 prem.py {id}"\n'
        (self.meta / 'project.yaml').write_text('contract_categories:\n  - id: Script\n    prefix: 스크립트\n' + config)
        (self.repo / 'fixture.txt').write_text('GOOD\n')
        for args in (['init', '-q'], ['config', 'user.name', 'fixture'], ['config', 'user.email', 'f@example.invalid'],
                     ['add', '.'], ['commit', '-qm', 'fixture']):
            done = subprocess.run(['git', *args], cwd=self.repo, env=self.env, capture_output=True)
            check(done.returncode == 0, 'fixture git ' + ' '.join(args))
        self.base = git('rev-parse', 'HEAD', cwd=self.repo).strip()
        self.requirements = self.root / 'requirements.md'
        self.requirements.write_text('fixture requirement')
        self.critique = self.root / 'critique.md'
        self.critique.write_text('fixture critique')

    def plan(self, steps):
        (self.state / 'plan.json').write_text(json.dumps(list(steps)))

    def usage(self, input_tokens, cached, output):
        (self.state / 'usage.json').write_text(json.dumps(dict(input_tokens=input_tokens, cached_input_tokens=cached,
                                                                output_tokens=output)))

    def ledger(self, rows):
        with (self.qa / 'codex-audit-usage.jsonl').open('w') as out:
            for row in rows:
                out.write((row if isinstance(row, str) else json.dumps(row)) + '\n')

    def args(self, verb):
        if verb == 'draft':
            self.contract.write_text('')
            return ['draft', self.requirements, self.contract]
        if verb == 'revise':
            self.contract.write_text(CONTRACT)
            return ['revise', self.contract, self.critique]
        return ['impl', self.contract, self.base]

    def run(self, verb, extra_env=None, timeout=150):
        argv = self.args(verb) if verb in ('draft', 'revise', 'impl') else verb
        done = subprocess.run(['bash', str(self.repo / SCRIPT), *map(str, argv)], cwd=self.repo,
                              env=dict(self.env, **(extra_env or {})), capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=timeout)
        return done.returncode, done.stdout + done.stderr

    def start(self, verb, extra_env=None):
        proc = subprocess.Popen(['bash', str(self.repo / SCRIPT), *map(str, self.args(verb))], cwd=self.repo,
                                env=dict(self.env, **(extra_env or {})), stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
        LIVE.append(proc)
        return proc

    def wait_for(self, name, seconds=60):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if (self.state / name).exists():
                return
            time.sleep(.1)
        check(False, '기다린 표식이 안 생김: ' + name)

    def execs(self):
        path = self.state / 'calls.jsonl'
        rows = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
        return [row for row in rows if row['kind'] == 'exec']

    def folder(self, kind='impl'):
        found = sorted((self.meta / 'codex-audit' / 'sample').glob(kind + '-r*'), key=lambda path: path.stat().st_mtime_ns)
        check(found, '감독 폴더 없음: ' + kind)
        return found[-1]

    def report(self, kind='impl'):
        return (self.folder(kind) / 'report.md').read_text(encoding='utf-8')

    def leftovers(self):
        return sorted(entry.name for entry in self.tmp.iterdir())


def real(path):
    return os.path.realpath(str(path).rstrip('/'))


def section(text, header):
    if header not in text:
        return ''
    return text.split(header, 1)[1].split('\n## ', 1)[0]


def chatgpt(case):
    (case.qa / 'auth.json').write_text(json.dumps(CHATGPT_AUTH))
    (case.qa / 'auth.json').chmod(0o600)
    return case


def config_with(case, extra):
    text = (case.meta / 'project.yaml').read_text()
    (case.meta / 'project.yaml').write_text(text + extra)


def homes(case):
    return {real(call['home']) for call in case.execs()}


def logins(case):
    path = case.state / 'calls.jsonl'
    rows = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    return [row for row in rows if row['kind'] == 'login']



def auth_of(case):
    return json.loads((case.qa / 'auth.json').read_text())


def token_of(case):
    return auth_of(case)['tokens']['access_token']


def in_temp(case, path):
    return real(path).startswith(real(case.tmp) + os.sep)


def held(case, index=0):
    case.wait_for('holding-%d' % index)
    return case.execs()[index]


def release(case, proc, index=0):
    (case.state / ('release-%d' % index)).touch()
    proc.wait(timeout=60)


def script_01():
    for verb, steps, expected in (('impl', ['reject', 'reject'], 1), ('draft', ['draft'], 0), ('revise', ['revise'], 0)):
        case = chatgpt(Case('w01-' + verb, steps))
        code, out = case.run(verb)
        check(code == expected, '%s 종료 %s\n%s' % (verb, code, out))
        used = [call['home'] for call in case.execs()] + [row['home'] for row in logins(case)]
        check(logins(case), verb + ' 로그인 확인 호출이 없다')
        check(all(in_temp(case, home) and real(home) != real(case.qa) for home in used),
              '%s 임시 사본이 아닌 CODEX_HOME: %s' % (verb, [home for home in used if not in_temp(case, home)]))
        last = max(case.execs(), key=lambda call: call['index'])
        check(token_of(case) == last['token'], '%s 갱신이 되돌려지지 않았다: %s (기대 %s)' % (verb, token_of(case), last['token']))
        mode = (case.qa / 'auth.json').stat().st_mode & 0o777
        check(mode == 0o600, '%s auth.json 권한 %o' % (verb, mode))
        check(not case.leftovers(), '%s 남은 임시 항목: %s' % (verb, case.leftovers()))
    case = chatgpt(Case('w01-login', ['approve']))
    (case.state / 'login-refresh').touch()
    (case.state / 'no-refresh').touch()
    code, out = case.run('impl')
    refreshed = [row for row in calls_of(case) if row['kind'] == 'login-refresh']
    check(code == 0 and refreshed, '로그인 확인 갱신 경우: 종료 %s · 갱신 %d' % (code, len(refreshed)))
    check(token_of(case) == refreshed[-1]['token'], '로그인 확인의 갱신이 되돌려지지 않았다: %s' % token_of(case))
    case = chatgpt(Case('w01-timeout', ['timeout']))
    code, out = case.run('impl', {'CODEX_AUDIT_LIMIT': '2'})
    check(case.execs(), '시간 초과 차례가 돌지 않았다')
    check(token_of(case) == case.execs()[0]['token'], '시간 초과 차례의 갱신이 되돌려지지 않았다: %s' % token_of(case))
    check(not case.leftovers(), '시간 초과 뒤 남은 임시 항목: %s' % case.leftovers())


def calls_of(case):
    path = case.state / 'calls.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def entries(folder):
    return {entry.name for entry in folder.iterdir()}


def script_02():
    case = chatgpt(Case('w02', ['reject', 'reject']))
    before, config = entries(case.qa), (case.qa / 'config.toml').read_bytes()
    code, out = case.run('impl')
    check(code == 1, 'impl 종료 %s\n%s' % (code, out))
    for call in case.execs():
        args = call['args']
        check('-p' not in args and '-s' not in args, '%d 차례에 -p 나 -s 가 있다' % call['index'])
        check('default_permissions="codex-audit-judge"' in args, '%d 차례에 권한 프로필이 없다' % call['index'])
        copied = (case.state / ('config-%d.toml' % call['index'])).read_text()
        check(copied.startswith(config.decode()) and copied.count('[permissions.codex-audit-judge]') == 1,
              '%d 차례 사본 config.toml 에 격리 설정이 한 번 붙지 않았다' % call['index'])
    after = entries(case.qa)
    check(not (after - before - ALLOWED_NEW), '감독 폴더에 새로 생긴 항목: %s' % sorted(after - before - ALLOWED_NEW))
    check(not (before - after), '감독 폴더에서 사라진 항목: %s' % sorted(before - after))
    check((case.qa / 'config.toml').read_bytes() == config, 'config.toml 이 바뀌었다')
    check(not list(case.qa.glob('codex-audit-*.config.toml')), '프로필 파일이 감독 폴더에 생겼다')
    case = chatgpt(Case('w02-term', ['hold']))
    before, config = entries(case.qa), (case.qa / 'config.toml').read_bytes()
    proc = case.start('impl')
    try:
        call = held(case)
        os.kill(int((case.folder() / 'pid').read_text()), signal.SIGTERM)
        proc.wait(timeout=60)
    finally:
        if proc.poll() is None:
            kill_group(proc)
    after = entries(case.qa)
    check(not (after - before - ALLOWED_NEW) and not (before - after), 'SIGTERM 뒤 감독 폴더 항목 변화: +%s -%s'
          % (sorted(after - before - ALLOWED_NEW), sorted(before - after)))
    check((case.qa / 'config.toml').read_bytes() == config, 'SIGTERM 뒤 config.toml 이 바뀌었다')
    check(token_of(case) == call['token'], 'SIGTERM 뒤 토큰: %s (기대 %s)' % (token_of(case), call['token']))
    check(not case.leftovers(), 'SIGTERM 뒤 남은 임시 항목: %s' % case.leftovers())


def script_03():
    case = chatgpt(Case('w03-outside', ['hold-late']))
    proc = case.start('impl')
    try:
        held(case)
        outside = json.loads(json.dumps(CHATGPT_AUTH))
        outside['tokens']['access_token'] = 'outside-newer'
        (case.qa / 'auth.json').write_text(json.dumps(outside))
    finally:
        release(case, proc)
    check(proc.returncode == 0, '(a) impl 종료 %s' % proc.returncode)
    check(token_of(case) == 'outside-newer', '(a) 그사이 바뀐 로그인 파일을 덮어썼다: %s' % token_of(case))
    first = chatgpt(Case('w03-a', ['hold-late']))
    second = Case('w03-b', ['hold-late'])
    text = (second.meta / 'project.yaml').read_text().replace(json.dumps(str(second.qa)), json.dumps(str(first.qa)))
    (second.meta / 'project.yaml').write_text(text)
    procs = [first.start('impl'), second.start('impl')]
    try:
        winner = held(first)
        held(second)
        release(first, procs[0])
        check(token_of(first) == winner['token'], '(b) 먼저 끝난 감독의 갱신이 안 들어갔다: %s' % token_of(first))
        release(second, procs[1])
    finally:
        for proc in procs:
            if proc.poll() is None:
                kill_group(proc)
    check(token_of(first) == winner['token'], '(b) 나중 감독이 먼저 감독의 갱신을 덮었다: %s' % token_of(first))
    for label, interrupt in (('c', False), ('d', True)):
        case = chatgpt(Case('w03-' + label, ['hold-late']))
        before = entries(case.qa)
        proc = case.start('impl')
        lock = (case.qa / 'codex-audit-auth.lock').open('a')
        try:
            call = held(case)
            fcntl.flock(lock, fcntl.LOCK_EX)
            (case.state / 'release-0').touch()
            time.sleep(3)
            check(token_of(case) == 'original', '(%s) 잠금을 잡은 동안 로그인 파일이 바뀌었다: %s' % (label, token_of(case)))
            if interrupt:
                os.kill(int((case.folder() / 'pid').read_text()), signal.SIGTERM)
                time.sleep(1)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()
            try:
                proc.wait(timeout=60)
            finally:
                if proc.poll() is None:
                    kill_group(proc)
        check(token_of(case) == call['token'], '(%s) 잠금을 놓은 뒤 토큰: %s (기대 %s)' % (label, token_of(case), call['token']))
        after = entries(case.qa)
        check(not (after - before - ALLOWED_NEW), '(%s) 감독 폴더에 새로 생긴 항목: %s' % (label, sorted(after - before - ALLOWED_NEW)))
        check(not case.leftovers(), '(%s) 남은 임시 항목: %s' % (label, case.leftovers()))


def script_04():
    case = chatgpt(Case('w04-same', ['reject', 'reject']))
    (case.state / 'no-refresh').touch()
    before = (case.qa / 'auth.json').read_bytes(), (case.qa / 'auth.json').stat().st_mtime_ns
    code, out = case.run('impl')
    check(code == 1, '갱신 없는 impl 종료 %s\n%s' % (code, out))
    after = (case.qa / 'auth.json').read_bytes(), (case.qa / 'auth.json').stat().st_mtime_ns
    check(after == before, '안 바뀐 로그인 파일을 다시 썼다')
    case = chatgpt(Case('w04-corrupt', ['corrupt']))
    before = (case.qa / 'auth.json').read_bytes()
    code, out = case.run('impl')
    check(case.execs(), '깨진 파일 차례가 돌지 않았다')
    check((case.qa / 'auth.json').read_bytes() == before, '깨진 사본 로그인 파일을 되돌려 썼다')
    shapes = (('plain', dict(OPENAI_API_KEY='sk-fixture-INVALID-000000000000')),
              ('mode', dict(auth_mode='apikey', OPENAI_API_KEY='sk-fixture-INVALID-000000000000')))
    for label, auth in shapes:
        case = Case('w04-' + label, ['reject', 'reject'])
        (case.qa / 'auth.json').write_text(json.dumps(auth))
        before = (case.qa / 'auth.json').read_bytes()
        code, out = case.run('impl')
        check(code == 1, '%s impl 종료 %s\n%s' % (label, code, out))
        check(all(in_temp(case, call['home']) for call in case.execs()), label + ' 임시 사본이 아닌 CODEX_HOME')
        check(not case.leftovers(), '%s 남은 항목: %s' % (label, case.leftovers()))
        check((case.qa / 'auth.json').read_bytes() == before, label + ' API 키 auth.json 이 바뀌었다')
        check(not (case.qa / 'codex-audit-auth.lock').exists(), label + ' API 키인데 잠금 파일이 생겼다')
        rows = [json.loads(line) for line in (case.qa / 'codex-audit-usage.jsonl').read_text().splitlines()]
        check(rows and all(row.get('plan') == 'apikey' for row in rows), '%s plan: %s' % (label, [row.get('plan') for row in rows]))


def script_05():
    case = chatgpt(Case('w05', ['nothread']))
    code, out = case.run('impl')
    check(case.execs() and case.execs()[0]['step'] == 'nothread', '차례 번호 없는 차례가 돌지 않았다')
    check(code in (0, 1, 2), 'impl 종료 %s\n%s' % (code, out))
    left = sorted(str(path.relative_to(case.qa)) for path in case.qa.rglob('rollout-*.jsonl'))
    check(not left, '감독 폴더에 남은 세션 기록: %s' % left)
    check(not case.leftovers(), '남은 임시 항목: %s' % case.leftovers())


def script_06():
    case = chatgpt(Case('w06', ['hold-reject', 'reject']))
    proc = case.start('impl')
    try:
        held(case)
        (case.qa / 'auth.json').write_text('{')
    finally:
        release(case, proc)
    check(proc.returncode == 1, 'impl 종료 %s' % proc.returncode)
    check(len(case.execs()) == 2, '차례 수 %d (판정 · 재심 기대)' % len(case.execs()))
    rows = [json.loads(line) for line in (case.qa / 'codex-audit-usage.jsonl').read_text().splitlines()]
    check(len(rows) == 2 and all(row.get('plan') == 'chatgpt' for row in rows), '기록 줄 plan: %s' % [row.get('plan') for row in rows])
    lines = [line for line in section(case.report(), '## 비용').splitlines() if line.startswith('- ')]
    check(lines and all('구독 — 청구 없음' in line for line in lines), '비용 줄:\n' + '\n'.join(lines))
    check((case.qa / 'auth.json').read_text() == '{', '그사이 바뀐 로그인 파일을 덮어썼다')


def script_07():
    case = chatgpt(Case('w07', ['hold']))
    proc = case.start('impl')
    done = None
    try:
        call = held(case)
        home, copy, frozen = call['home'], call['cwd'], case.folder() / 'input'
        lines = ['echo w > %s/probe.txt && echo copy-write=ok || echo copy-write=no' % copy,
                 'ls %s >/dev/null 2>&1 && echo input-read=ok || echo input-read=no' % frozen,
                 '(echo x > %s/probe.txt) 2>/dev/null && echo input-write=ok || echo input-write=no' % frozen,
                 'ls %s/.ssh >/dev/null 2>&1 && echo ssh-read=ok || echo ssh-read=no' % REAL_HOME,
                 'cat %s/auth.json >/dev/null 2>&1 && echo auth-read=ok || echo auth-read=no' % case.qa,
                 'cat %s/auth.json >/dev/null 2>&1 && echo copy-auth-read=ok || echo copy-auth-read=no' % home]
        codex = shutil.which('codex', path=REAL_PATH)
        if codex:
            done = subprocess.run([codex, 'sandbox', '-P', 'codex-audit-judge', '-C', str(copy), '--',
                                   '/bin/sh', '-c', '\n'.join(lines)], env=dict(os.environ, CODEX_HOME=home,
                                  TMPDIR=call['env']['TMPDIR'], PATH=call['env']['PATH']),
                                  capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120)
    finally:
        release(case, proc)
    if done is None:
        print('[미검증:ENV] 진짜 codex 를 못 찾음')
        return
    cells = dict(re.findall(r'^([a-z-]+)=(ok|no)$', done.stdout, re.M))
    print('칸: ' + str(cells))
    wanted = [('copy-write', 'ok'), ('input-read', 'ok'), ('input-write', 'no'), ('auth-read', 'no'), ('copy-auth-read', 'no')]
    if (REAL_HOME / '.ssh').is_dir():
        wanted.append(('ssh-read', 'no'))
    else:
        print('[미검증:ENV] ~/.ssh 가 없어 ssh-read 칸을 재지 않는다')
    for name, want in wanted:
        check(cells.get(name) == want, '%s 기대 %s 실제 %s' % (name, want, cells.get(name)))


def script_08():
    for key in ('스크립트-05', '스크립트-06'):
        done = subprocess.run(['bash', str(PREVIOUS), key], capture_output=True,
                              text=True, stdin=subprocess.DEVNULL, timeout=600)
        print(done.stdout.strip().splitlines()[-1] if done.stdout.strip() else key + ' 출력 없음')
        check(done.returncode == 0, '앞 측정 묶음 %s 종료 %s' % (key, done.returncode))
    case = chatgpt(Case('w08-fail', ['approve']))
    (case.state / 'login-fail').touch()
    code, out = case.run('impl')
    check(code == 2 and '로그인-없음' in case.report() and not case.execs(), '로그인 실패: 종료 %s' % code)
    check(not case.leftovers(), '로그인 실패 뒤 남은 임시 항목: %s' % case.leftovers())



def skill_01():
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if '**Codex 감독 설정**' in para), '')
    for word in ('codex-audit-auth.lock', '되돌려 쓴다'):
        check(word in block, 'README 감독 설정 문단에 %s 가 없다' % word)
    for stale in ('감독 폴더를 그대로 쓴다', '복사하지 않고', '`-p` 로 붙', 'codex-audit-<번호>.config.toml'):
        check(stale not in block, 'README 에 옛 문장 「%s」 가 남았다' % stale)


def reuse_01():
    text = at_tip(SCRIPT)
    check(text.count('def judge_profile(') == 1, 'judge_profile 정의 수')
    check(text.count("'[' + table + ']'") == 1, '권한 표 머리 만드는 자리 수')
    check("'-p'" not in text, "'-p' 인자가 남아 있다")
    found = len(re.findall(r'\bsubscription\(', text))
    check(found == 2, 'subscription( 등장 수 %d (정의 1 · 판정 1 기대)' % found)

def at_tip(path):
    return git('show', '%s:%s' % (SOURCE_REF or tip(), path))



def structure_01():
    upper = tip()
    names = [line for line in git('diff', '--name-only', '%s..%s' % (BASE, upper), '--', '.', ':(exclude).harness').splitlines() if line]
    print('바뀐 경로: ' + ' '.join(names))
    check(SCRIPT in names, 'codex-audit.sh 변경이 없다')
    outside = [name for name in names if name not in SCOPE]
    check(not outside, '범위 밖 경로: ' + str(outside))



def mdlint_tool():
    cache = Path.home() / '.cache' / 'claude-plugins-mdlint'
    binary = cache / 'node_modules' / '.bin' / 'markdownlint-cli2'
    if not binary.exists():
        cache.mkdir(parents=True, exist_ok=True)
        subprocess.run(['npm', 'install', '--no-save', '--prefix', str(cache), 'markdownlint-cli2@0.23.2'],
                       capture_output=True, check=True, stdin=subprocess.DEVNULL)
    config = cache / 'config.jsonc'
    config.write_text('{ "config": { "MD013": %s } }\n' % ('true' if POSITIVE else 'false'))
    return binary, config


def diagnostics_02():
    binary, config = mdlint_tool()
    upper = tip()
    files = ['harness/README.md', '.harness/sprint-contract-codex-audit-auth-writeback.md']
    target = RUN / 'mdlint'
    total = 0
    for path in files:
        body = subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (upper, path)], capture_output=True, text=True)
        check(body.returncode == 0 and body.stdout.count('\n') > 0, '가지 끝에서 못 읽은 파일: ' + path)
        copy = target / path
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_text(body.stdout)
        added = set()
        diff = subprocess.run(['git', '-C', str(W), 'diff', '-U0', '%s..%s' % (BASE, upper), '--', path], capture_output=True, text=True).stdout
        for start, length in re.findall(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', diff, re.M):
            added.update(range(int(start), int(start) + int(length or 1)))
        if POSITIVE:
            added = set(range(1, body.stdout.count('\n') + 2))
        done = subprocess.run([str(binary), '--config', str(config), str(copy)], cwd=target, capture_output=True, text=True)
        hits = [int(number) for number in re.findall(re.escape(path) + r':(\d+)', done.stdout + done.stderr)]
        new = [number for number in hits if number in added]
        print('%s 경고 %d · 더한 줄 경고 %d' % (path, len(hits), len(new)))
        total += len(new)
    if POSITIVE:
        check(total >= 1, '양성 대조: 줄 길이 규칙을 켜도 경고 0 — 검사가 죽어 있다')
        return
    check(total == 0, '더한 줄 마크다운 경고 %d' % total)


def ci_commands():
    lines = (W / '.github/workflows/ci.yml').read_text().splitlines()
    return [line.split('run:', 1)[1].strip() for line in lines
            if re.match(r'\s+run: (python3 scripts/|bash harness/|bash flutter-toolkit/)', line)]


def diagnostics_04():
    check(subprocess.run(['bash', '-n', str(source() / SCRIPT)]).returncode == 0, 'bash -n 실패')
    done = subprocess.run(['python3', 'scripts/validate-plugin.py', 'harness'], cwd=W, capture_output=True, text=True)
    check(done.returncode == 0, 'validate-plugin harness:\n' + done.stdout[-2000:])
    others = [key for key in TABLE if key != '진단-04']
    try:
        done = subprocess.run([sys.executable, __file__, 'all', '--skip', '진단-04'], capture_output=True, text=True,
                              env=dict(os.environ, MEASURE_W=str(W)), timeout=900)
    except subprocess.TimeoutExpired:
        check(False, '측정 묶음 전체가 900 초 안에 끝나지 않았다')
    check('Traceback' not in done.stdout + done.stderr, '측정 묶음 출력에 Traceback')
    check(done.returncode == 0, '측정 묶음 %d 개 중 FAIL:\n%s' % (len(others), done.stdout[-3000:]))
    failed = []
    commands = ci_commands()
    check(commands, 'CI 명령을 하나도 못 뽑았다')
    for command in commands:
        run = subprocess.run(['bash', '-c', command], cwd=W, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if run.returncode:
            failed.append(command)
    print('로컬 CI 명령 %d 개 · 실패 %d' % (len(commands), len(failed)))
    check(not failed, '로컬 CI 실패: ' + str(failed))


TABLE = {
    '스크립트-01': script_01, '스크립트-02': script_02, '스크립트-03': script_03, '스크립트-04': script_04,
    '스크립트-05': script_05, '스크립트-06': script_06, '스크립트-07': script_07, '스크립트-08': script_08,
    '스킬-01': skill_01, '구조-01': structure_01,
    '재사용-01': reuse_01, '진단-02': diagnostics_02, '진단-04': diagnostics_04,
}


def run_one(key):
    try:
        TABLE[key]()
        print('PASS ' + key)
        return True
    except Fail as error:
        print('FAIL %s — %s' % (key, error))
    except (subprocess.TimeoutExpired, OSError, ValueError, KeyError, IndexError, json.JSONDecodeError) as error:
        print('FAIL %s — %s: %s' % (key, type(error).__name__, error))
    return False


def main():
    skip = sys.argv[sys.argv.index('--skip') + 1] if '--skip' in sys.argv else ''
    positional = [arg for arg in sys.argv[1:] if not arg.startswith('--') and arg != skip]
    target = positional[0] if positional else None
    if target == 'all':
        results = {key: run_one(key) for key in TABLE if key != skip}
        print('합계 PASS %d · FAIL %d' % (sum(results.values()), len(results) - sum(results.values())))
        return 0 if all(results.values()) else 1
    if target not in TABLE:
        print('쓰는 법: measure.sh <조건 번호|all> [--base] [--positive]')
        return 64
    return 0 if run_one(target) else 1


try:
    status = main()
finally:
    for proc in LIVE:
        if proc.poll() is None:
            kill_group(proc)
    # 가짜 codex 는 감독과 다른 프로세스 묶음이라 위에서 안 죽는다. 기록된 pid 로 끈다.
    for calls in RUN.glob('*/state/calls.jsonl'):
        for line in calls.read_text().splitlines():
            pid = json.loads(line).get('pid')
            if pid:
                try:
                    os.kill(pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
    shutil.rmtree(RUN, ignore_errors=True)
sys.exit(status)
