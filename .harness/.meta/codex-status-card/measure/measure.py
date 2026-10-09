#!/usr/bin/env python3
"""codex-status-card 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

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
W = Path(os.environ.get('MEASURE_W', '/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-status-card'))
BASE, BRANCH = 'afbb36f2', 'feat/codex-status-card'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/README.md', 'harness/vscode-status/extension.js',
         'harness/vscode-status/status.js', 'harness/vscode-status/README.md', 'harness/vscode-status/package.json']
PREVIOUS = [(W / '.harness/.meta/codex-audit-usage-cap/measure/measure.sh', 'feat/codex-audit-usage-cap',
             ['스크립트-01', '스크립트-02', '스크립트-03', '스크립트-04']),
            (W / '.harness/.meta/codex-status-bar/measure/measure.sh', 'feat/codex-status-bar', ['스크립트-01', '스크립트-02', '스크립트-05'])]
HOME_DIR = Path(pwd.getpwuid(os.getuid()).pw_dir)
RULES = [(HOME_DIR / '.claude/CLAUDE.md', '**호출 방식:**'), (HOME_DIR / '.claude/codex-prompt-template.md', '리서치는 래퍼를 쓴다')]
RESEARCH = Path(os.environ.get('MEASURE_RESEARCH') or Path(pwd.getpwuid(os.getuid()).pw_dir) / '.claude/bin/codex-research')
RESEARCH_BASE = RESEARCH.with_name('codex-research.bak-20261009b')
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


def research_run(label, script, prompt='Role: 조사자. Read-only.\n\nGoal: VS Code 상태 표시줄 API 조사\n\n자세한 지시', link=False, extra=None):
    root = RUN / label
    state, sessions, status, real_work, bins = (root / name for name in ('state', 'sessions', 'status', 'work', 'bin'))
    for folder in (state, sessions, status, real_work, bins):
        folder.mkdir(parents=True)
    work = real_work
    if link:
        work = root / 'link'
        work.symlink_to(real_work)
    shutil.copyfile(HERE / 'fake_research.py', bins / 'codex')
    (bins / 'codex').chmod(0o755)
    (real_work / 'prompt.md').write_text(prompt)
    (status / 'usage.json').write_text(json.dumps(dict(limits={'5시간': dict(used=12, resets_at=int(time.time()) + 3600),
                                                                '주간': dict(used=3, resets_at=int(time.time()) - 60)})))
    env = dict(os.environ, PATH=str(bins) + os.pathsep + REAL_PATH, FAKE_STATE=str(state), CODEX_SESS_DIR=str(sessions),
               CODEX_STATUS_DIR=str(status), CLAUDE_CODE_SESSION_ID=SESSION, CODEX_TRIES='1', START_GRACE='30',
               STALL_GRACE='60', PWD=str(work), **(extra or {}))
    out, err = (root / 'stdout.txt').open('w'), (root / 'stderr.txt').open('w')
    proc = subprocess.Popen(['bash', '-c', 'cd "$0" && exec bash "$1" prompt.md out.md gpt-5.6-sol', str(work), str(script)],
                            env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err, start_new_session=True)
    proc.root = root
    LIVE.append(proc)
    return proc, state, status, real_work


PROGRESS = re.compile(r'^리서치 · VS Code 상태 표시줄 API 조사 · 시도 1/1 · \d+(초|분) · 5시간 12%$')


def progress_lines(proc, stream):
    return [line for line in (proc.root / stream).read_text().splitlines() if PROGRESS.match(line)]


def held_research(state):
    deadline = time.monotonic() + 30
    while not (state / 'holding').exists() and time.monotonic() < deadline:
        time.sleep(.1)
    check((state / 'holding').exists(), '가짜 codex 가 차례를 열지 않았다')


def finish_research(proc, state):
    (state / 'release').touch()
    try:
        proc.wait(timeout=90)
    finally:
        if proc.poll() is None:
            kill_group(proc)
    return (proc.root / 'stdout.txt').read_text() + (proc.root / 'stderr.txt').read_text()


def script_01():
    script = RESEARCH_BASE if USE_BASE else RESEARCH
    proc, state, status, work = research_run('c01', script, extra={'CODEX_PROGRESS_SECONDS': '1'})
    try:
        held_research(state)
        time.sleep(7)
        jobs = jobs_in(status)
        check(len(jobs) == 1 and jobs[0].get('topic') == 'VS Code 상태 표시줄 API 조사', '(a) Goal 이 셋째 줄 → topic: %s' % [j.get('topic') for j in jobs])
        before = progress_lines(proc, 'stderr.txt')
        check(len(before) >= 2, '(b1) 놓아주기 전 진행 줄(stderr) %d 개 (2 이상 기대)' % len(before))
    finally:
        finish_research(proc, state)
    check(proc.returncode == 0, '(b) 실행기 종료 %s' % proc.returncode)
    check(not progress_lines(proc, 'stdout.txt'), '(b3) 진행 줄이 stdout(답 통로)에 섞였다')
    proc, state, status, work = research_run('c01-slow', script, extra={'CODEX_PROGRESS_SECONDS': '20'})
    try:
        held_research(state)
        time.sleep(5)
        early = progress_lines(proc, 'stderr.txt')
        check(len(early) <= 1, '(b2) 간격 20 초인데 5 초 안에 진행 줄 %d 개 (시작 줄 1 개까지)' % len(early))
    finally:
        finish_research(proc, state)
    for label, extra in (('c01-long', None), ('c01-long-c', {'LC_ALL': 'C', 'LANG': 'C'})):
        proc, state, status, work = research_run(label, script, prompt='Goal: ' + '가' * 60 + '\n', extra=extra)
        try:
            held_research(state)
            time.sleep(1)
            jobs = jobs_in(status)
            check(len(jobs) == 1 and jobs[0].get('topic') == '가' * 40 + '…', '(c) 긴 주제 자르기(%s): %s' % (label, [j.get('topic') for j in jobs]))
        finally:
            finish_research(proc, state)
    proc, state, status, work = research_run('c01-nogoal', script, prompt='\n\n  첫 줄 주제\n둘째 줄')
    try:
        held_research(state)
        time.sleep(1)
        jobs = jobs_in(status)
        check(len(jobs) == 1 and jobs[0].get('topic') == '첫 줄 주제', '(d) Goal 없을 때 첫 줄: %s' % [j.get('topic') for j in jobs])
    finally:
        finish_research(proc, state)


def script_02():
    proc, state, status, work = research_run('c02', RESEARCH_BASE if USE_BASE else RESEARCH, link=True)
    try:
        held_research(state)
        time.sleep(1)
        jobs = jobs_in(status)
        check(len(jobs) == 1 and jobs[0].get('folder') == os.path.realpath(work), '바로가기 폴더 → 실제 경로: %s (기대 %s)'
              % ([j.get('folder') for j in jobs], os.path.realpath(work)))
    finally:
        finish_research(proc, state)


def script_03():
    cases = node_json('check_summary.js', source() / 'harness/vscode-status')
    one = cases['one']
    check(len(one) == 1 and one[0]['text'] == 'e5f6 리서치 · VS Code 상태 표시줄 API 조사 · 시도 1/3 · 30초 · 5시간 12% · 주간 3%', '(a) %s' % one)
    check(cases['no_topic'][0]['text'] == 'a1b2 감독 · judge-1 · 4분 · 5시간 12% · 주간 3%', '(b) %s' % cases['no_topic'])
    both = cases['summary_both']
    check(both and both['text'] == '$(sync~spin) 감독 1 · 리서치 1', '(c) 요약 글자: %s' % both)
    check(both and all(item['text'] in both['tooltip'] for item in cases['both']), '(c) 풀이에 작업별 줄: %s' % both)
    check(cases['summary_one'] and cases['summary_one']['text'] == '$(sync~spin) 리서치 1', '(d) %s' % cases['summary_one'])
    check(cases['summary_none'] is None, '(e) 작업 없으면 null: %s' % cases['summary_none'])
    check(cases['summary_many'] and cases['summary_many']['text'] == '$(sync~spin) 감독 2 · 리서치 1', '(f) %s' % cases['summary_many'])
    check(isinstance(both['tooltip'], str) and both['tooltip'].count('\n') == 1, '(g) 풀이는 일반 글자 · 작업마다 한 줄: %r' % both['tooltip'])


def script_04():
    began = time.monotonic()
    report = node_json('check_extension.js', source() / 'harness/vscode-status', timeout=30)
    check(time.monotonic() - began < 25, '끈 뒤 스스로 멈추지 않았다')
    two = report['two']
    check(len(two) == 1 and two[0]['text'] == '$(sync~spin) 감독 1 · 리서치 1', '(a) 두 작업 → 항목 1 개: %s' % two)
    check(len(two) == 1 and 'a1b2 감독' in two[0]['tooltip'] and 'e5f6 리서치 · 상태 표시줄 조사' in two[0]['tooltip'], '(a) 풀이: %s' % two)
    check(report['one'] == ['$(sync~spin) 감독 1'], '(b) 하나 지운 뒤: %s' % report['one'])
    check(report['all_disposed'] and report['created_after_off'] == 0, '(c) 살아 있는 채 끄기: 정리 %s · 끈 뒤 새 항목 %s'
          % (report['all_disposed'], report['created_after_off']))
    check(report['ids'] == ['joo6077.codex-status'], '(d) 항목 ID 는 하나로 고정: %s' % report['ids'])


def script_05():
    case = Case('c05', ['hold'])
    bad = case.root / 'not-a-dir'
    bad.write_text('파일이라 폴더를 못 만든다')
    proc = case.start('impl', {'CODEX_STATUS_DIR': str(bad / 'status'), 'CODEX_STATUS_BEAT': '1'})
    try:
        case.wait_for('holding-0')
        time.sleep(3)
    finally:
        release(case, proc)
    out = proc.stdout.read() if proc.stdout else ''
    check(proc.returncode == 0 and last_line(case) == '감독 판정: APPROVE', '(a) 상태 폴더를 못 써도 감독은 끝까지: 종료 %s\n%s' % (proc.returncode, out[-600:]))
    check('Traceback' not in out and 'Exception in thread' not in out, '(a) 오류 출력:\n' + out[-600:])
    rows = [line for line in (case.qa / 'codex-audit-usage.jsonl').read_text().splitlines()] if (case.qa / 'codex-audit-usage.jsonl').exists() else []
    check(len(rows) == 1, '(a) 사용 기록 줄 %d 개 (1 기대 — 상태 폴더 실패가 사용 기록을 막으면 안 된다)' % len(rows))
    case = Case('c05-beat', ['hold'])
    proc = case.start('impl', {'CODEX_STATUS_BEAT': '1'})
    try:
        case.wait_for('holding-0')
        time.sleep(.5)
        first = jobs_in(case.status)[0]['updated']
        time.sleep(3)
        second = jobs_in(case.status)[0]['updated']
        check(second > first, '(b) 감독 updated 가 갱신되지 않는다: %s → %s' % (first, second))
    finally:
        release(case, proc)


def last_line(case):
    return case.report().strip().splitlines()[-1]


def script_06():
    proc, state, status, work = research_run('c06', RESEARCH_BASE if USE_BASE else RESEARCH)
    try:
        held_research(state)
        time.sleep(1)
        first = jobs_in(status)[0]['updated']
        time.sleep(5)
        second = jobs_in(status)[0]['updated']
        check(second > first, '리서치 updated 가 반복 주기마다 갱신되지 않는다: %s → %s' % (first, second))
    finally:
        finish_research(proc, state)


RULE_SENTENCE = '래퍼는 Bash `run_in_background: true` 로 돌려 그 세션 채팅 창의 작업 카드로 진행을 보고, 끝 알림이 오면 출력 파일을 읽는다'


def script_07():
    for path, anchor in RULES:
        text = path.read_text(encoding='utf-8')
        start = text.find(anchor)
        check(start >= 0, '%s 에 「%s」 자리가 없다' % (path, anchor))
        end = text.find('\n\n', start)
        block = text[start:end if end > 0 else len(text)]
        check(RULE_SENTENCE in block, '%s 의 「%s」 문단에 정한 문장이 없다' % (path.name, anchor))
    claude = RULES[0][0].read_text(encoding='utf-8')
    start = claude.find(RULES[0][1])
    block = claude[start:claude.find('\n\n', start)]
    check('직접 부를 때는' in block and '앞에서 기다리며' in block.split('직접 부를 때는', 1)[1],
          'CLAUDE.md: 「앞에서 기다리며」 는 직접 codex exec 부를 때만으로 남아야 한다')


def script_08():
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


def node_json(script, *args, timeout=30):
    done = subprocess.run(['node', str(HERE / script), *map(str, args)], capture_output=True, text=True, timeout=timeout,
                          stdin=subprocess.DEVNULL)
    check(done.returncode == 0, '%s 종료 %s\n%s' % (script, done.returncode, done.stderr[-800:]))
    return json.loads(done.stdout.strip().splitlines()[-1])


def skill_01():
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if '**Codex 진행 상황 표시줄**' in para), '')
    for word in ('작업 카드', '감독 1 · 리서치 1', 'Goal:'):
        check(word in block, 'README 상태 표시줄 문단에 %s 가 없다' % word)


def reuse_01():
    text = at_tip('harness/vscode-status/extension.js')
    check(text.count("require('./status')") == 1, "extension.js 가 require('./status') 를 한 번 쓰지 않는다")
    for stale in ('process.kill', 'relative(', 'resets_at', "'감독'", "'리서치'"):
        check(stale not in text, 'extension.js 에 「%s」 — 판단 · 셈은 status.js 에만 둔다' % stale)


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
    files = ['harness/README.md', 'harness/vscode-status/README.md', '.harness/sprint-contract-codex-status-card.md']
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
    '스크립트-05': script_05, '스크립트-06': script_06, '스크립트-07': script_07, '스크립트-08': script_08,
    '스킬-01': skill_01, '구조-01': structure_01, '재사용-01': reuse_01, '진단-02': diagnostics_02, '진단-04': diagnostics_04,
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
