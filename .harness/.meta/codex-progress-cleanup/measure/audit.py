#!/usr/bin/env python3
"""codex-progress-cleanup 감독 쪽 측정 묶음 (codex-status-bar 측정 묶음에서 가져와 검사 함수만 바꿨다). 종료 코드 0 = PASS, 1 = FAIL.

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
W = Path(os.environ.get('MEASURE_W', '/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-research-activity'))
BASE, BRANCH = 'ae918dab', 'feat/codex-research-activity'
SCRIPT = 'harness/scripts/codex-audit.sh'
SESSION = 'a1b2c3d4-sess-test'
ALLOWED_NEW = {'codex-audit-usage.jsonl', 'codex-audit-models.json', 'codex-audit-auth.lock'}
FAKE = HERE / "fake_audit.py"
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
        (self.qa / 'auth.json').write_text(json.dumps(CHATGPT_AUTH))
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
        self.status = self.root / 'status'
        self.env = dict(os.environ, HOME=str(self.home), CODEX_BIN=str(bins / 'codex'), FAKE_STATE=str(self.state),
                        CODEX_STATUS_DIR=str(self.status), CLAUDE_CODE_SESSION_ID=SESSION,
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


def status_files(case):
    # 상태 폴더 변수를 무시하고 홈 아래(.codex-status 등)나 임시 폴더에 써도 잡는다. 감독 폴더 .codex-qa 는 원래 쓰는 곳이다
    found = sorted('status/' + path.name for path in case.status.rglob('*')) if case.status.exists() else []
    found += sorted('HOME/' + path.name for path in case.home.iterdir() if path.name != '.codex-qa')
    found += sorted('TMP/' + path.name for path in case.tmp.rglob('감독-*.json'))
    return found


def committed():
    # 가지 끝 커밋을 꺼내 재므로, 커밋 안 된 변경이 있으면 낡은 판을 잰 통과가 된다
    if USE_BASE:
        return
    dirty = git('status', '--porcelain', '--', 'harness/scripts', 'harness/README.md', 'harness/vscode-status').strip()
    check(not dirty, '커밋 안 된 변경이 있다 — 구현 커밋 뒤 재라: ' + dirty.replace(chr(10), ' | '))


def ledger_limits(case):
    path = case.qa / 'codex-audit-usage.jsonl'
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    return next((row['limits'] for row in reversed(rows) if row.get('limits')), {})


def supervisor_01():
    committed()
    case = Case('a01', ['hold'])
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        time.sleep(.5)
        check(not status_files(case), '(a) 판정 차례 중 상태 폴더 파일: %s' % status_files(case))
    finally:
        (case.state / 'release-0').touch()
        proc.wait(timeout=60)
    check(proc.returncode == 0, '(b) impl 종료 %s' % proc.returncode)
    check(not status_files(case), '(b) 끝난 뒤 상태 폴더 파일: %s' % status_files(case))
    limits = ledger_limits(case)
    check(limits.get('5시간', {}).get('used') == 12 and limits.get('주간', {}).get('used') == 3, '(b) 사용 기록 limits: %s' % limits)
    case = Case('a01-term', ['hold'])
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        time.sleep(.5)
        os.kill(int((case.folder() / 'pid').read_text()), signal.SIGTERM)
        proc.wait(timeout=60)
    finally:
        if proc.poll() is None:
            kill_group(proc)
    check(not status_files(case), '(c) SIGTERM 뒤 상태 폴더 파일: %s' % status_files(case))
    case = Case('a01-detach', ['hold'])
    code, out = case.run(case.args('impl') + ['--detach'])
    check(code == 0, '(d) --detach 종료 %s\n%s' % (code, out))
    case.wait_for('holding-0')
    time.sleep(.5)
    check(not status_files(case), '(d) --detach 판정 차례 중 상태 폴더 파일: %s' % status_files(case))
    (case.state / 'release-0').touch()
    deadline = time.monotonic() + 60
    while not (case.folder() / 'report.md').exists() and time.monotonic() < deadline:
        time.sleep(.2)
    time.sleep(1)
    check(not status_files(case), '(d) --detach 끝난 뒤 상태 폴더 파일: %s' % status_files(case))


def seeded_row(five, week, resets_in=3600):
    now = int(time.time())
    return dict(date=datetime.date.today().isoformat(), repo='/fixture/other', slug='other', verb='impl', turn='judge-1',
                model='gpt-6.1-sol', input=0, cached=0, output=0,
                limits={'5시간': dict(used=five, resets_at=now + resets_in), '주간': dict(used=week, resets_at=now + resets_in)})


def supervisor_02():
    committed()
    case = Case('a02')
    case.ledger([seeded_row(80, 10)])
    code, out = case.run('impl')
    report = case.report()
    check(code == 2 and '갈래: 한도-사용량' in report and 'Traceback' not in out, '상한 막힘: 종료 %s\n%s' % (code, report[-400:]))
    check(not case.execs(), '막혔는데 Codex 를 불렀다: exec %d' % len(case.execs()))
    check(not status_files(case), '막힌 뒤 상태 폴더 파일: %s' % status_files(case))


def at_ref(path):
    ref = BASE if USE_BASE else tip()
    done = subprocess.run(['git', '-C', str(W), 'show', ref + ':' + path], capture_output=True, text=True)
    return done.stdout if done.returncode == 0 else None


def structure_01():
    committed()
    ref = BASE if USE_BASE else tip()
    tracked = git('ls-tree', '-r', '--name-only', ref, '--', 'harness/vscode-status').split()
    check(not tracked, '확장 폴더 파일이 남았다: %s' % tracked)
    readme = at_ref('harness/README.md') or ''
    stale = [line[:60] for line in readme.splitlines() if re.search(r'vscode-status|진행 상황 표시줄|CODEX_STATUS|\.codex-status', line)]
    check(not stale, 'harness/README.md 에 남은 줄: %s' % stale)
    script = at_ref(SCRIPT) or ''
    left = [word for word in ('status_dir', 'write_json', 'class Board', 'CODEX_STATUS', '.codex-status', 'board') if word in script]
    check(script and not left, '%s 에 남은 낱말: %s' % (SCRIPT, left))


TABLE = {'감독-01': supervisor_01, '감독-02': supervisor_02, '구조-01': structure_01}


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
