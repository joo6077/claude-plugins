#!/usr/bin/env python3
"""codex-audit-subscription 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

가지 끝 커밋(--base 면 BASE)의 harness/ 를 임시 폴더로 꺼내 가짜 codex 로 감독을 끝까지 돌린다.
자기가 만든 임시 폴더는 끝날 때 지운다 — 앞 스프린트 측정 묶음이 이것을 안 해서 한 폴더에 4.0GB 가 쌓였다.
"""
import datetime
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
BASE, BRANCH = 'da5cf49a', 'feat/codex-audit-judge-mode'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/templates/project.yaml', 'harness/README.md',
         'harness/skills/sprint-contract/SKILL.md']
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


def script_01():
    for verb, steps, expected in (('impl', ['reject', 'reject'], 1), ('draft', ['draft'], 0), ('revise', ['revise'], 0)):
        case = chatgpt(Case('u01-' + verb, steps))
        code, out = case.run(verb)
        check(code == expected, '%s 종료 %s\n%s' % (verb, code, out))
        check(homes(case) == {real(case.qa)}, '%s CODEX_HOME 이 감독 폴더가 아니다: %s' % (verb, homes(case)))
        check(logins(case) and {real(row['home']) for row in logins(case)} == {real(case.qa)}, verb + ' 로그인 확인의 CODEX_HOME')
        token = json.loads((case.qa / 'auth.json').read_text())['tokens']['access_token']
        last = max(call['index'] for call in case.execs())
        check(token == 'refreshed-%d' % last, '%s 갱신이 버려졌다: %s (기대 refreshed-%d)' % (verb, token, last))


def profile_files(case):
    return sorted(path.name for path in case.qa.glob('codex-audit-*.config.toml'))


def script_02():
    case = chatgpt(Case('u02', ['reject', 'reject']))
    before = (case.qa / 'config.toml').read_bytes()
    code, out = case.run('impl')
    check(code == 1, 'impl 종료 %s\n%s' % (code, out))
    for call in case.execs():
        args = call['args']
        name = args[args.index('-p') + 1] if '-p' in args else ''
        check(name.startswith('codex-audit-'), '%d 차례에 -p codex-audit-* 가 없다' % call['index'])
        check('default_permissions="codex-audit-judge"' in args and '-s' not in args, '%d 차례 인자' % call['index'])
        profile = case.state / ('profile-%d.toml' % call['index'])
        check(profile.exists(), '%d 차례 중에 프로필 파일이 없었다' % call['index'])
        network = tomllib.loads(profile.read_text()).get('permissions', {}).get('codex-audit-judge', {}).get('network', {})
        check(network.get('enabled') is False, '인터넷이 꺼져 있지 않다: %s' % network)
    check(not profile_files(case), '프로필 파일이 남았다: %s' % profile_files(case))
    check((case.qa / 'config.toml').read_bytes() == before, '감독 폴더 config.toml 이 바뀌었다')
    case = chatgpt(Case('u02-term', ['hold']))
    term_before = (case.qa / 'config.toml').read_bytes()
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        check(profile_files(case), '양성 대조: 도는 중에 프로필 파일이 안 보인다')
        os.kill(int((case.folder() / 'pid').read_text()), signal.SIGTERM)
        proc.wait(timeout=60)
    finally:
        if proc.poll() is None:
            os.killpg(proc.pid, signal.SIGKILL)
    check(not profile_files(case), 'SIGTERM 뒤 프로필 파일이 남았다: %s' % profile_files(case))
    check((case.qa / 'config.toml').read_bytes() == term_before, 'SIGTERM 뒤 config.toml 이 바뀌었다')


def script_03():
    case = chatgpt(Case('u03', ['hold']))
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        call = case.execs()[0]
        args = call['args']
        check('-p' in args, '-p 가 없다')
        name, copy, frozen = args[args.index('-p') + 1], call['cwd'], case.folder() / 'input'
        lines = ['echo w > %s/probe.txt && echo copy-write=ok || echo copy-write=no' % copy,
                 'ls %s >/dev/null 2>&1 && echo input-read=ok || echo input-read=no' % frozen,
                 '(echo x > %s/probe.txt) 2>/dev/null && echo input-write=ok || echo input-write=no' % frozen,
                 'ls %s/.ssh >/dev/null 2>&1 && echo ssh-read=ok || echo ssh-read=no' % REAL_HOME,
                 'cat %s/auth.json >/dev/null 2>&1 && echo auth-read=ok || echo auth-read=no' % case.qa]
        codex = shutil.which('codex', path=REAL_PATH)
        if not codex:
            print('[미검증:ENV] 진짜 codex 를 못 찾음')
            return
        done = subprocess.run([codex, 'sandbox', '-p', name, '-P', 'codex-audit-judge', '-C', str(copy), '--',
                               '/bin/sh', '-c', '\n'.join(lines)], env=dict(os.environ, CODEX_HOME=str(case.qa),
                              TMPDIR=call['env']['TMPDIR'], PATH=call['env']['PATH']),
                              capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120)
    finally:
        (case.state / 'release-0').touch()
        proc.wait(timeout=60)
    cells = dict(re.findall(r'^([a-z-]+)=(ok|no)$', done.stdout, re.M))
    print('칸: ' + str(cells))
    wanted = [('copy-write', 'ok'), ('input-read', 'ok'), ('input-write', 'no'), ('auth-read', 'no')]
    if (REAL_HOME / '.ssh').is_dir():
        wanted.append(('ssh-read', 'no'))
    else:
        print('[미검증:ENV] ~/.ssh 가 없어 ssh-read 칸을 재지 않는다')
    for name, want in wanted:
        check(cells.get(name) == want, '%s 기대 %s 실제 %s' % (name, want, cells.get(name)))


def script_04():
    shapes = (('plain', dict(OPENAI_API_KEY='sk-fixture-INVALID-000000000000')),
              ('mode', dict(auth_mode='apikey', OPENAI_API_KEY='sk-fixture-INVALID-000000000000')))
    for label, auth in shapes:
        case = Case('u04-' + label, ['reject', 'reject'])
        (case.qa / 'auth.json').write_text(json.dumps(auth))
        before = (case.qa / 'auth.json').read_bytes()
        code, out = case.run('impl')
        check(code == 1, '%s impl 종료 %s\n%s' % (label, code, out))
        check(real(case.qa) not in homes(case), label + ' API 키인데 감독 폴더를 그대로 썼다')
        check(not case.leftovers(), '%s 남은 항목: %s' % (label, case.leftovers()))
        check((case.qa / 'auth.json').read_bytes() == before, label + ' API 키 auth.json 이 바뀌었다')
        rows = [json.loads(line) for line in (case.qa / 'codex-audit-usage.jsonl').read_text().splitlines()]
        check(rows and all(row.get('plan') == 'apikey' for row in rows), '%s plan: %s' % (label, [row.get('plan') for row in rows]))


def model_of(call):
    args = call['args']
    return args[args.index('-m') + 1] if '-m' in args else ''


ROLES = {'both': '  model_draft: m-draft\n  model_impl: m-impl\n', 'impl-only': '  model_impl: m-impl\n',
         'draft-only': '  model_draft: m-draft\n', 'none': ''}


def model_case(name, steps, roles, extra_env=None, verb='impl'):
    case = Case(name, steps, model='m-base')
    config_with(case, ROLES[roles] + '  effort_impl: max\n')
    code, out = case.run(verb, extra_env)
    check(code in (0, 1), '%s 종료 %s\n%s' % (name, code, out))
    return case.execs()


def script_05():
    for verb in ('draft', 'revise'):
        check([model_of(c) for c in model_case('u05-' + verb, [verb], 'both', verb=verb)] == ['m-draft'], verb + ' 모델')
    calls = model_case('u05-impl', ['research', 'research-answer', 'reject', 'reject'], 'both')
    check([model_of(c) for c in calls] == ['m-impl'] * 4, 'judge · research · judge · review 모델: %s' % [model_of(c) for c in calls])
    check('model_reasoning_effort="max"' in calls[0]['args'], 'judge 차례에 effort_impl max 가 실리지 않았다')
    for roles, draft_model, judge_model in (('impl-only', 'm-base', 'm-impl'), ('draft-only', 'm-draft', 'm-base'), ('none', 'm-base', 'm-base')):
        check([model_of(c) for c in model_case('u05-d-' + roles, ['draft'], roles, verb='draft')] == [draft_model], roles + ' draft')
        check({model_of(c) for c in model_case('u05-j-' + roles, ['approve'], roles)} == {judge_model}, roles + ' judge')
    check({model_of(c) for c in model_case('u05-env', ['approve'], 'both', {'CODEX_AUDIT_MODEL': 'm-env'})} == {'m-env'}, '환경 변수')
    check([model_of(c) for c in model_case('u05-env-draft', ['draft'], 'both', {'CODEX_AUDIT_MODEL': 'm-env'}, 'draft')] == ['m-env'], '환경 변수 draft')


def seeded(today_a, today_b):
    today = datetime.date.today().isoformat()
    row = dict(slug='sample', verb='impl', turn='judge-1', model='gpt-6.1-sol', input=0, cached=0, output=0)
    return [dict(row, date=today, repo='/fixture/repo-a', usd=today_a), dict(row, date=today, repo='/fixture/repo-b', usd=today_b)]


def script_06():
    case = chatgpt(Case('u06', ['approve'], model='gpt-6.1-sol'))
    case.usage(1000000, 900000, 20000)
    code, out = case.run('impl')
    check(code == 0, 'impl 종료 %s\n%s' % (code, out))
    costs = section(case.report(), '## 비용')
    check(any('judge-1' in line and '구독 — 청구 없음' in line and '1,000,000' in line for line in costs.splitlines()), '차례 줄:\n' + costs)
    check(any('합계' in line and '구독 — 청구 없음' in line for line in costs.splitlines()), '합계 줄:\n' + costs)
    last = json.loads((case.qa / 'codex-audit-usage.jsonl').read_text().splitlines()[-1])
    check(last.get('usd') is None and last.get('plan') == 'chatgpt', '기록 줄: %s' % last)
    case = chatgpt(Case('u06-budget', ['approve'], model='gpt-6.1-sol'))
    config_with(case, '  daily_budget_usd: 0.50\n')
    case.ledger(seeded(0.49, 0.25))
    code, out = case.run('impl')
    check(code == 0 and '구독이라 하루 상한을 건너뛴다' in case.report(), '상한 건너뜀: 종료 %s' % code)
    mixed = seeded(0.49, 0.25) + [dict(seeded(0, 0)[0], usd=None, plan='chatgpt')]
    case = Case('u06-apikey-budget', ['approve'], model='gpt-6.1-sol')
    config_with(case, '  daily_budget_usd: 0.50\n')
    case.ledger(mixed)
    code, out = case.run('impl')
    check(code == 2 and '한도-예산' in case.report() and not case.execs(), 'API 키 상한: 종료 %s' % code)
    case = Case('u06-apikey-cost', ['approve'], model='gpt-6.1-sol')
    case.usage(1000000, 900000, 20000)
    code, out = case.run('impl')
    costs = section(case.report(), '## 비용')
    check(code == 0 and any('judge-1' in line and '0.49달러' in line for line in costs.splitlines()), 'API 키 금액:\n' + costs)


def script_07():
    first = chatgpt(Case('u07-a', ['hold']))
    second = Case('u07-b', ['hold'])
    text = (second.meta / 'project.yaml').read_text().replace(json.dumps(str(second.qa)), json.dumps(str(first.qa)))
    (second.meta / 'project.yaml').write_text(text)
    before = {entry.name for entry in first.qa.iterdir()}
    procs = [first.start('impl'), second.start('impl')]
    try:
        first.wait_for('holding-0')
        second.wait_for('holding-0')
        names = []
        for case in (first, second):
            args = case.execs()[0]['args']
            names.append(args[args.index('-p') + 1] if '-p' in args else '')
        check(all(names) and names[0] != names[1], '두 차례 -p 이름: %s' % names)
        (first.state / 'release-0').touch()
        procs[0].wait(timeout=60)
        check((first.qa / (names[1] + '.config.toml')).exists(), '한쪽이 끝나며 다른 쪽 프로필 파일을 지웠다')
        (second.state / 'release-0').touch()
        procs[1].wait(timeout=60)
    finally:
        for proc in procs:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
    after = {entry.name for entry in first.qa.iterdir()}
    extra = after - before - {'sessions', 'codex-audit-usage.jsonl', 'codex-audit-models.json'}
    check(not extra, '감독 폴더에 남은 새 항목: %s' % sorted(extra))
    check(not (before - after), '감독 폴더에서 사라진 항목: %s' % sorted(before - after))


def script_08():
    case = chatgpt(Case('u08', ['approve']))
    code, out = case.run('impl')
    check(code == 0 and logins(case) and {real(row['home']) for row in logins(case)} == {real(case.qa)}, '로그인 확인의 CODEX_HOME')
    case = chatgpt(Case('u08-fail', ['approve']))
    (case.state / 'login-fail').touch()
    code, out = case.run('impl')
    check(code == 2 and '로그인-없음' in case.report() and not case.execs(), '로그인 실패: 종료 %s' % code)


def at_tip(path):
    return git('show', '%s:%s' % (SOURCE_REF or tip(), path))


def skill_01():
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if '**Codex 감독 설정**' in para), '')
    for word in ('model_draft', 'model_impl', '구독'):
        check(word in block, 'README 감독 설정 문단에 %s 가 없다' % word)
    template = at_tip('harness/templates/project.yaml').split('codex_audit:', 1)[-1]
    check(re.search(r'^\s+model_draft:', template, re.M) and re.search(r'^\s+model_impl:', template, re.M), 'project.yaml 틀')
    check('model_draft' in at_tip('harness/skills/sprint-contract/SKILL.md'), 'SKILL.md')


def structure_01():
    upper = tip()
    names = [line for line in git('diff', '--name-only', '%s..%s' % (BASE, upper), '--', '.', ':(exclude).harness').splitlines() if line]
    print('바뀐 경로: ' + ' '.join(names))
    check(SCRIPT in names, 'codex-audit.sh 변경이 없다')
    outside = [name for name in names if name not in SCOPE]
    check(not outside, '범위 밖 경로: ' + str(outside))


def reuse_01():
    text = at_tip(SCRIPT)
    check(text.count('def judge_profile(') == 1, 'judge_profile 정의 수')
    check(text.count("'[' + table + ']'") == 1, '권한 표 머리 만드는 자리 수: %d' % text.count("'[' + table + ']'"))
    check(text.count('[permissions.') == 0, '권한 표를 손으로 쓴 자리가 있다')


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
    files = ['harness/README.md', 'harness/skills/sprint-contract/SKILL.md',
             '.harness/sprint-contract-codex-audit-subscription.md']
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
            os.killpg(proc.pid, signal.SIGKILL)
    shutil.rmtree(RUN, ignore_errors=True)
sys.exit(status)
