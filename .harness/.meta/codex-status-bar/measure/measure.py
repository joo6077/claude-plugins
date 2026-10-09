#!/usr/bin/env python3
"""codex-status-bar 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

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
W = Path(os.environ.get('MEASURE_W', '/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-status-bar'))
BASE, BRANCH = 'd72bd22c', 'feat/codex-status-bar'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/README.md', 'harness/vscode-status/package.json',
         'harness/vscode-status/extension.js', 'harness/vscode-status/status.js', 'harness/vscode-status/install.sh',
         'harness/vscode-status/.vscodeignore', 'harness/vscode-status/README.md']
PREVIOUS = [(W / '.harness/.meta/codex-audit-usage-cap/measure/measure.sh', 'feat/codex-audit-usage-cap',
             ['스크립트-01', '스크립트-02', '스크립트-03', '스크립트-04'])]
RESEARCH = Path(os.environ.get('MEASURE_RESEARCH') or Path(pwd.getpwuid(os.getuid()).pw_dir) / '.claude/bin/codex-research')
RESEARCH_BASE = RESEARCH.with_name('codex-research.bak-20261009')
SESSION = 'a1b2c3d4-sess-test'
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




def calls_of(case):
    path = case.state / 'calls.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def jobs_in(folder):
    found = []
    for path in sorted(folder.glob('*.json')) if folder.is_dir() else []:
        if path.name != 'usage.json':
            found.append(json.loads(path.read_text()))
    return found


def usage_in(folder):
    path = folder / 'usage.json'
    return json.loads(path.read_text()) if path.exists() else {}


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def check_job(jobs, kind, folder, step_word, label):
    check(len(jobs) == 1, '%s: 상태 파일 %d 개 (1 기대): %s' % (label, len(jobs), jobs))
    job = jobs[0]
    check(job.get('kind') == kind and job.get('session') == SESSION, '%s: kind · session: %s' % (label, job))
    check(real(job.get('folder', '')) == real(folder), '%s: folder %s (기대 %s)' % (label, job.get('folder'), folder))
    check(step_word in str(job.get('step')), '%s: step %r 에 %r 가 없다' % (label, job.get('step'), step_word))
    check(all(isinstance(job.get(key), int) for key in ('started', 'updated', 'pid')) and alive(job['pid']), '%s: 시각 · pid: %s' % (label, job))


def script_01():
    case = Case('s01', ['hold'])
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        time.sleep(.5)
        check_job(jobs_in(case.status), '감독', case.repo, 'judge-1', '(a) 판정 차례 중')
    finally:
        (case.state / 'release-0').touch()
        proc.wait(timeout=60)
    check(proc.returncode == 0, '(b) impl 종료 %s' % proc.returncode)
    check(not jobs_in(case.status), '(b) 끝난 뒤 남은 상태 파일: %s' % jobs_in(case.status))
    limits = usage_in(case.status).get('limits') or {}
    check(limits.get('5시간', {}).get('used') == 12 and limits.get('주간', {}).get('used') == 3, '(b) usage.json: %s' % limits)
    case = Case('s01-term', ['hold'])
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        time.sleep(.5)
        check(jobs_in(case.status), '(c) 차례 중 상태 파일이 없다')
        os.kill(int((case.folder() / 'pid').read_text()), signal.SIGTERM)
        proc.wait(timeout=60)
    finally:
        if proc.poll() is None:
            kill_group(proc)
    check(not jobs_in(case.status), '(c) SIGTERM 뒤 남은 상태 파일: %s' % jobs_in(case.status))
    case = Case('s01-blocked')
    (case.qa / 'auth.json').write_text(json.dumps(dict(OPENAI_API_KEY='sk-fixture-INVALID-000000000000')))
    code, out = case.run('impl')
    check(code == 2 and not jobs_in(case.status), '(d) 막힌 감독 종료 %s · 남은 상태 파일 %s' % (code, jobs_in(case.status)))
    case = Case('s01-detach', ['hold'])
    code, out = case.run(case.args('impl') + ['--detach'])
    check(code == 0, '(e) --detach 종료 %s\n%s' % (code, out))
    case.wait_for('holding-0')
    time.sleep(.5)
    jobs = jobs_in(case.status)
    check_job(jobs, '감독', case.repo, 'judge-1', '(e) --detach 판정 차례 중')
    check(jobs[0]['pid'] == int((case.folder() / 'pid').read_text()), '(e) pid %s ≠ 감독 pid 파일' % jobs[0]['pid'])
    (case.state / 'release-0').touch()
    deadline = time.monotonic() + 60
    while jobs_in(case.status) and time.monotonic() < deadline:
        time.sleep(.2)
    check(not jobs_in(case.status), '(e) --detach 끝난 뒤 남은 상태 파일: %s' % jobs_in(case.status))


def research_run(label, script):
    root = RUN / label
    state, sessions, status, work, bins = (root / name for name in ('state', 'sessions', 'status', 'work', 'bin'))
    for folder in (state, sessions, status, work, bins):
        folder.mkdir(parents=True)
    shutil.copyfile(HERE / 'fake_research.py', bins / 'codex')
    (bins / 'codex').chmod(0o755)
    (work / 'prompt.md').write_text('fixture 조사')
    env = dict(os.environ, PATH=str(bins) + os.pathsep + REAL_PATH, FAKE_STATE=str(state), CODEX_SESS_DIR=str(sessions),
               CODEX_STATUS_DIR=str(status), CLAUDE_CODE_SESSION_ID=SESSION, CODEX_TRIES='1', START_GRACE='30', STALL_GRACE='60')
    proc = subprocess.Popen(['bash', str(script), 'prompt.md', 'out.md', 'gpt-5.6-sol'], cwd=work, env=env,
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            start_new_session=True)
    LIVE.append(proc)
    return proc, state, status, work


def script_02():
    proc, state, status, work = research_run('s02', RESEARCH_BASE if USE_BASE else RESEARCH)
    try:
        deadline = time.monotonic() + 30
        while not (state / 'holding').exists() and time.monotonic() < deadline:
            time.sleep(.1)
        check((state / 'holding').exists(), '가짜 codex 가 차례를 열지 않았다')
        time.sleep(4)   # 실행기 반복 주기(3 초)보다 길게
        check_job(jobs_in(status), '리서치', work, '시도 1/1', '(a) 리서치 도는 중')
    finally:
        (state / 'release').touch()
        try:
            out = proc.communicate(timeout=90)[0]
        finally:
            if proc.poll() is None:
                kill_group(proc)
    check(proc.returncode == 0, '(b) 리서치 종료 %s\n%s' % (proc.returncode, out[-800:]))
    check(not jobs_in(status), '(b) 끝난 뒤 남은 상태 파일: %s' % jobs_in(status))
    limits = usage_in(status).get('limits') or {}
    check(limits.get('5시간', {}).get('used') == 12 and limits.get('주간', {}).get('used') == 3,
          '(b) usage.json: %s (미끼 기록 50/40 을 읽었으면 짐작한 것)' % limits)
    if USE_BASE:
        return
    proc, state, status, work = research_run('s02-term', RESEARCH)
    try:
        deadline = time.monotonic() + 30
        while not (state / 'holding').exists() and time.monotonic() < deadline:
            time.sleep(.1)
        time.sleep(4)
        check(jobs_in(status), '(c) 도는 중 상태 파일이 없다')
        proc.send_signal(signal.SIGTERM)
        proc.communicate(timeout=60)
    finally:
        if proc.poll() is None:
            kill_group(proc)
    fake = int((state / 'research-pid').read_text())
    time.sleep(1)
    check(not jobs_in(status), '(c) 끝내라는 신호 뒤 남은 상태 파일: %s' % jobs_in(status))
    check(not alive(fake), '(c) 끝내라는 신호 뒤 가짜 codex(pid %d)가 살아 있다' % fake)


def node_json(script, *args, timeout=30):
    done = subprocess.run(['node', str(HERE / script), *map(str, args)], capture_output=True, text=True, timeout=timeout,
                          stdin=subprocess.DEVNULL)
    check(done.returncode == 0, '%s 종료 %s\n%s' % (script, done.returncode, done.stderr[-800:]))
    return json.loads(done.stdout.strip().splitlines()[-1])


def script_03():
    cases = node_json('check_status.js', source() / 'harness/vscode-status')
    a = cases['a']
    check(len(a) == 1 and re.fullmatch(r'\$\(sync~spin\) a1b2 감독 judge-1 · 4분 · 5시간 12% · 주간 3%', a[0]['text']), '(a) %s' % a)
    check('a1b2c3d4-0000' in a[0]['tooltip'] and '/w/repo/sub' in a[0]['tooltip'], '(a) 풀이: %s' % a[0]['tooltip'])
    for key in ('b', 'c', 'd', 'g'):
        check(cases[key] == [], '(%s) 항목이 없어야 한다: %s' % (key, cases[key]))
    e = cases['e']
    check(len(e) == 2 and len({item['key'] for item in e}) == 2, '(e) 두 세션이 따로 나와야 한다: %s' % e)
    check(any(re.fullmatch(r'\$\(sync~spin\) e5f6 리서치 시도 1/3 · 30초 · 5시간 12% · 주간 3%', item['text']) for item in e), '(e) %s' % e)
    f = cases['f']
    check(len(f) == 1 and '%' not in f[0]['text'], '(f) 사용량 없으면 % 없이: %s' % f)
    h = cases['h']
    check(len(h) == 1 and h[0]['text'].startswith('$(sync~spin) ---- 감독'), '(h) 세션 없음 표시: %s' % h)
    check(cases['i'] == [], '(i) updated 가 10 분 전이면 항목이 없어야 한다: %s' % cases['i'])
    j = cases['j']
    check(len(j) == 1 and '5시간' not in j[0]['text'] and '주간 3%' in j[0]['text'], '(j) 풀린 창은 % 를 빼야 한다: %s' % j)
    check(len(cases['k']) == 1, '(k) 살아 있음 판단을 안 넘기면 기본 판단(살아 있는 pid)으로 1 개: %s' % cases['k'])


def script_04():
    began = time.monotonic()
    report = node_json('check_extension.js', source() / 'harness/vscode-status', timeout=40)
    check(time.monotonic() - began < 35, '확장이 끈 뒤 스스로 멈추지 않았다(타이머 · 감시자 남음)')
    check(report['activate_error'] is None and report['before'] == 0, '(a) 상태 폴더 없이 시작: 오류 %s · 항목 %s' % (report['activate_error'], report['before']))
    check(len(report['shown']) == 1 and '감독 judge-1' in report['shown'][0] and '5시간 12%' in report['shown'][0]
          and report['shown_ms'] <= 4000, '(b) 반쯤 쓴 파일이 섞여도 작업 1 개: %s (%sms)' % (report['shown'], report['shown_ms']))
    check(len(report['two']) == 2 and len(set(report['two'])) == 2 and report['two_ms'] <= 4000, '(c) 두 작업 → 항목 2 개 · id 다름: %s' % report['two'])
    check(len(report['with_noise']) == 2, '(d) 죽은 pid · 폴더 밖 작업이 보였다: %s' % report['with_noise'])
    check(report['one'] == 1 and report['one_ms'] <= 4000, '(e) 하나 지운 뒤 항목 %s (%sms)' % (report['one'], report['one_ms']))
    check(report['after'] == 0 and report['gone_ms'] <= 4000, '(f) 다 지운 뒤 항목 %s (%sms)' % (report['after'], report['gone_ms']))
    check(report['created_before_off'] <= 4, '(g) 만든 항목이 본 작업 수보다 많다(쌓임): %s' % report['created_before_off'])
    check(report['all_disposed'] and report['created_after_off'] == report['created_before_off'],
          '(h) 끈 뒤 정리: 전부 dispose %s · 끈 뒤 새로 만든 항목 %s' % (report['all_disposed'], report['created_after_off'] - report['created_before_off']))


def script_05():
    folder = source() / 'harness/vscode-status'
    manifest = json.loads((folder / 'package.json').read_text())
    check(manifest.get('main') == './extension.js' and manifest.get('activationEvents') == ['onStartupFinished'], 'main · activationEvents: %s' % manifest)
    check(all(manifest.get(key) for key in ('name', 'publisher', 'version')) and (manifest.get('engines') or {}).get('vscode'), '필수 칸: %s' % manifest)
    check(not manifest.get('dependencies'), '의존성이 있다: %s' % manifest.get('dependencies'))
    out = RUN / 'pack.vsix'
    done = subprocess.run(['npx', '--yes', '@vscode/vsce@4.0.0', 'package', '--no-dependencies', '--allow-missing-repository',
                           '--skip-license', '-o', str(out)], cwd=folder, capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    check(done.returncode == 0 and out.exists(), 'vsce package 종료 %s\n%s' % (done.returncode, (done.stdout + done.stderr)[-800:]))
    import zipfile
    names = set(zipfile.ZipFile(out).namelist())
    for name in ('extension/package.json', 'extension/extension.js', 'extension/status.js'):
        check(name in names, '묶음에 %s 가 없다: %s' % (name, sorted(names)))
    check(not any(name.startswith('extension/install') for name in names), '설치 스크립트가 묶음에 들어갔다')


def script_06():
    for path, branch, ids in PREVIOUS:
        copy = RUN / ('prev-' + path.parent.parent.name)
        if not copy.exists():
            shutil.copytree(path.parent, copy)
            script = copy / 'measure.py'
            text = script.read_text()
            check(text.count(repr(branch)) == 1, path.parent.parent.name + ' 가지 이름 자리를 못 찾음')
            script.write_text(text.replace(repr(branch), repr(BRANCH)))
        for key in ids:
            done = subprocess.run(['bash', str(copy / 'measure.sh'), key], capture_output=True, text=True, stdin=subprocess.DEVNULL,
                                  timeout=600, env=dict(os.environ, MEASURE_W=str(W)))
            tail = done.stdout.strip().splitlines()[-1] if done.stdout.strip() else '출력 없음'
            print('%s %s → %s' % (path.parent.parent.name, key, tail))
            check(done.returncode == 0 and 'Traceback' not in done.stdout + done.stderr, '앞 측정 %s %s 종료 %s' % (path.parent.parent.name, key, done.returncode))


def skill_01():
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if 'vscode-status' in para), '')
    for word in ('~/.codex-status', 'CLAUDE_CODE_SESSION_ID', 'install.sh', '감독', '리서치'):
        check(word in block, 'README 상태 표시줄 문단에 %s 가 없다' % word)


def reuse_01():
    text = at_tip('harness/vscode-status/extension.js')
    check(text.count("require('./status')") == 1, "extension.js 가 require('./status') 를 한 번 쓰지 않는다")
    for stale in ('process.kill', 'relative(', 'resets_at'):
        check(stale not in text, 'extension.js 에 「%s」 — 판단은 status.js 에만 둔다' % stale)


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
    files = ['harness/README.md', '.harness/sprint-contract-codex-status-bar.md']
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
    check(subprocess.run(['bash', '-n', str(RESEARCH)]).returncode == 0, 'codex-research bash -n 실패')
    for name in ('extension.js', 'status.js'):
        check(subprocess.run(['node', '--check', str(source() / 'harness/vscode-status' / name)]).returncode == 0, 'node --check ' + name)
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
    '스크립트-05': script_05, '스크립트-06': script_06, '스킬-01': skill_01, '구조-01': structure_01,
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
