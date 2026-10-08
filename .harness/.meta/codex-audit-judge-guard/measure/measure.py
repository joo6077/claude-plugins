#!/usr/bin/env python3
"""codex-audit-judge-guard 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

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
BASE, BRANCH = '452ca7b8', 'feat/codex-audit-judge-mode'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/README.md']
PREVIOUS = [(W / '.harness/.meta/codex-audit-auth-writeback/measure/measure.sh', ['all', '--skip', '진단-04']),
            (W / '.harness/.meta/codex-audit-subscription/measure/measure.sh', ['스크립트-05']),
            (W / '.harness/.meta/codex-audit-subscription/measure/measure.sh', ['스크립트-06'])]
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
# /tmp 아래 저장소를 흉내 낼 뿌리. 끝나면 지운다.
SLASH_TMP = []
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
    def __init__(self, name, steps=('approve',), config=None, premeasure=False, model='fixture-supervisor', base=None, tmpdir=None):
        self.root = (base or RUN) / name
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
        self.tmp = tmpdir or self.root / 'tmp'
        self.tmp.mkdir(exist_ok=True)
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




def slash_tmp(prefix):
    folder = Path(tempfile.mkdtemp(prefix='cag-', dir=prefix))
    SLASH_TMP.append(folder)
    return folder


def script_01():
    for prefix in ('/tmp', '/private/tmp'):
        # TMPDIR 은 /tmp 밖에 둔다 — TMPDIR 이나 현재 폴더로 판정하는 구현을 가려낸다.
        case = chatgpt(Case('g01-impl', ['approve'], base=slash_tmp(prefix), tmpdir=Path(tempfile.mkdtemp(dir=RUN))))
        code, out = case.run('impl')
        report = case.report()
        check(code == 2, '%s 아래 impl 종료 %s\n%s' % (prefix, code, out))
        check('갈래: 설정-오류' in report and '/tmp' in section(report, '## 실패 원인'), '%s 실패 원인:\n%s' % (prefix, report[-800:]))
        check(not case.execs() and not logins(case), '%s 아래인데 exec %d 번 · 로그인 확인 %d 번' % (prefix, len(case.execs()), len(logins(case))))
        check(not case.leftovers(), '%s 남은 임시 항목: %s' % (prefix, case.leftovers()))
        case = chatgpt(Case('g01-draft', ['draft'], base=slash_tmp(prefix), tmpdir=Path(tempfile.mkdtemp(dir=RUN))))
        code, out = case.run('draft')
        check(len(case.execs()) == 1 and '설정-오류' not in out, '%s 아래 draft 가 막혔다: 종료 %s\n%s' % (prefix, code, out))
    case = chatgpt(Case('g01-outside', ['approve']))
    code, out = case.run('impl')
    check(code == 0 and len(case.execs()) == 1, '/tmp 밖 impl: 종료 %s · exec %d' % (code, len(case.execs())))
    case = chatgpt(Case('g01-tmpdir', ['approve'], tmpdir=slash_tmp('/tmp')))
    code, out = case.run('impl')
    check(code == 0 and len(case.execs()) == 1, '저장소는 밖 · TMPDIR 만 /tmp 인 impl: 종료 %s · exec %d\n%s' % (code, len(case.execs()), out[-600:]))


def calls_of(case):
    path = case.state / 'calls.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def entries(folder):
    return {entry.name for entry in folder.iterdir()}




def lock_opened(case, seconds=40):
    pid = (case.folder() / 'pid').read_text().strip()
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        listed = subprocess.run(['lsof', '-p', pid, '-Fn'], capture_output=True, text=True).stdout
        if 'codex-audit-auth.lock' in listed:
            return int(pid)
        time.sleep(.2)
    check(False, '감독이 잠금 파일을 열지 않았다')


def script_02():
    # (a) 쓰는 도중 SIGTERM → 쓰기를 마친 뒤 멈춘다 (b) 잠금을 10 초 넘게 못 잡는 동안 SIGINT → 쓰지 않고 멈춘다
    for label, sig, hold, expect in (('a', signal.SIGTERM, 1, 'turn'), ('b', signal.SIGINT, 13, 'original')):
        case = chatgpt(Case('g02-' + label, ['hold-late-orphan']))
        before = entries(case.qa)
        proc = case.start('impl')
        lock = (case.qa / 'codex-audit-auth.lock').open('a')
        try:
            call = held(case)
            fcntl.flock(lock, fcntl.LOCK_EX)
            (case.state / 'release-0').touch()
            pid = lock_opened(case)
            time.sleep(.5)
            check(token_of(case) == 'original', '(%s) 잠금을 잡은 동안 로그인 파일이 바뀌었다: %s' % (label, token_of(case)))
            os.kill(pid, sig)
            time.sleep(hold)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
            lock.close()
            try:
                out = proc.communicate(timeout=60)[0]
            finally:
                if proc.poll() is None:
                    kill_group(proc)
                orphan = case.state / 'orphan.pid'
                if orphan.exists():
                    try:
                        os.kill(int(orphan.read_text()), signal.SIGKILL)
                    except ProcessLookupError:
                        pass
        want = call['token'] if expect == 'turn' else 'original'
        check(token_of(case) == want, '(%s) 토큰 %s (기대 %s)' % (label, token_of(case), want))
        check(proc.returncode == 128 + sig, '(%s) 종료 %s (기대 %d — 신호가 사라졌다)' % (label, proc.returncode, 128 + sig))
        check('갈래: 중단됨' in case.report() and 'Traceback' not in out, '(%s) 갈래 또는 Traceback:\n%s' % (label, out[-600:]))
        after = entries(case.qa)
        check(not (after - before - ALLOWED_NEW), '(%s) 감독 폴더에 새로 생긴 항목: %s' % (label, sorted(after - before - ALLOWED_NEW)))
        check(not case.leftovers(), '(%s) 남은 임시 항목: %s' % (label, case.leftovers()))


def script_03():
    case = chatgpt(Case('g03', ['approve']))
    (case.qa / 'auth.json').chmod(0o644)
    code, out = case.run('impl')
    check(code == 0, 'impl 종료 %s\n%s' % (code, out))
    check(token_of(case) == case.execs()[0]['token'], '되돌려 쓰지 않았다: %s' % token_of(case))
    for name in ('auth.json', 'codex-audit-auth.lock'):
        mode = (case.qa / name).stat().st_mode & 0o777
        check(mode == 0o600, '%s 권한 %o (기대 600)' % (name, mode))
    left = sorted(entry.name for entry in case.qa.iterdir() if entry.name.startswith('.codex-audit-auth-'))
    check(not left, '쓰다 만 임시 파일: %s' % left)


def script_04():
    for path, args in PREVIOUS:
        done = subprocess.run(['bash', str(path), *args], capture_output=True, text=True, stdin=subprocess.DEVNULL,
                              timeout=900, env=dict(os.environ, MEASURE_W=str(W)))
        tail = done.stdout.strip().splitlines()[-1] if done.stdout.strip() else '출력 없음'
        print('%s %s → %s' % (path.parent.parent.name, ' '.join(args), tail))
        check(done.returncode == 0 and 'Traceback' not in done.stdout + done.stderr, '앞 측정 묶음 %s %s 종료 %s' % (path.parent.parent.name, ' '.join(args), done.returncode))


def skill_01():
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if '**Codex 감독 설정**' in para), '')
    check('`/tmp` 아래' in block, 'README 감독 설정 문단에 `/tmp` 아래 안내가 없다')


def reuse_01():
    text = at_tip(SCRIPT)
    check('pthread_sigmask' not in text, 'pthread_sigmask 가 남아 있다')
    check(text.count('def write_back(') == 1, 'write_back 정의 수 %d' % text.count('def write_back('))

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
    files = ['harness/README.md', '.harness/sprint-contract-codex-audit-judge-guard.md']
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
    for folder in [RUN] + SLASH_TMP:
        shutil.rmtree(folder, ignore_errors=True)
sys.exit(status)
