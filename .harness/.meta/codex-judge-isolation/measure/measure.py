#!/usr/bin/env python3
"""codex-judge-isolation 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

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
BASE, BRANCH = 'fc9ab639', 'feat/codex-judge-isolation'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/templates/codex-audit/judge.md',
         'harness/templates/codex-audit/premeasure.md', 'harness/templates/codex-audit/prices.json',
         'harness/templates/project.yaml', 'harness/README.md', 'harness/skills/sprint-contract/SKILL.md',
         'harness/agents/qa-evaluator.md']
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
            shutil.copyfile(HERE / 'fake.py', bins / tool)
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


def judge_args_clean(args):
    return '-s' not in args and not any('sandbox_workspace_write' in arg for arg in args) \
        and sum(1 for arg in args if arg == 'default_permissions="codex-audit-judge"') == 1


def uses_workspace_write(args):
    return any(args[index] == '-s' and args[index + 1] == 'workspace-write' for index in range(len(args) - 1))


def script_01():
    rejected = Case('s01-reject', ['reject', 'reject'])
    code, out = rejected.run('impl')
    check(code == 1, 'impl REJECT 종료 코드 %s\n%s' % (code, out))
    calls = rejected.execs()
    check(len(calls) == 2, 'judge-1 · review-1 두 차례가 아니다: %d' % len(calls))
    for name, call in zip(('judge-1', 'review-1'), calls):
        check(judge_args_clean(call['args']), name + ' 인자: ' + ' '.join(call['args'][:-1]))
    research = Case('s01-research', ['research', 'research-answer', 'approve'])
    code, out = research.run('impl')
    check(code == 0, 'research impl 종료 코드 %s\n%s' % (code, out))
    calls = research.execs()
    check(len(calls) == 3, 'judge-1 · research-1 · judge-2 세 차례가 아니다: %d' % len(calls))
    check(judge_args_clean(calls[0]['args']) and judge_args_clean(calls[2]['args']), '조사 뒤 판정 차례 인자')
    check(uses_workspace_write(calls[1]['args']), 'research-1 에 -s workspace-write 가 없다')
    draft = Case('s01-draft', ['draft'])
    code, out = draft.run('draft')
    check(code == 0, 'draft 종료 코드 %s\n%s' % (code, out))
    check(uses_workspace_write(draft.execs()[0]['args']), 'draft-1 에 -s workspace-write 가 없다')


PROBES = [('copy-write', True), ('input-read', True), ('python', True), ('node', True),
          ('input-write', False), ('ssh-read', False), ('slash-tmp-read', False), ('other-audit-read', False)]


def probe(codex_home, copy, frozen, other_bait, tmp, tool_path):
    tmp_bait = Path('/private/tmp') / ('cji-bait-%d.txt' % os.getpid())
    tmp_bait.write_text('bait')
    check(shutil.which('python3', path=tool_path) and shutil.which('node', path=tool_path), 'python3 · node 를 판정 PATH 에서 못 찾음')
    lines = [
        'echo w > %s/probe-write.txt && echo copy-write=ok || echo copy-write=no' % copy,
        'ls %s >/dev/null 2>&1 && echo input-read=ok || echo input-read=no' % frozen,
        'python3 -c 1 && echo python=ok || echo python=no',
        'node -e 1 && echo node=ok || echo node=no',
        '(echo x > %s/probe-write.txt) 2>/dev/null && echo input-write=ok || echo input-write=no' % frozen,
        'ls %s/.ssh >/dev/null 2>&1 && echo ssh-read=ok || echo ssh-read=no' % REAL_HOME,
        'cat %s >/dev/null 2>&1 && echo slash-tmp-read=ok || echo slash-tmp-read=no' % tmp_bait,
        'cat %s >/dev/null 2>&1 && echo other-audit-read=ok || echo other-audit-read=no' % other_bait,
    ]
    codex = shutil.which('codex', path=REAL_PATH)
    check(codex, '진짜 codex 를 못 찾음')
    try:
        done = subprocess.run([codex, 'sandbox', '-P', 'codex-audit-judge', '-C', str(copy), '--log-denials', '--',
                               '/bin/sh', '-c', '\n'.join(lines)], env=dict(os.environ, CODEX_HOME=str(codex_home), TMPDIR=str(tmp), PATH=tool_path),
                              capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120)
    finally:
        tmp_bait.unlink(missing_ok=True)
    cells = dict(re.findall(r'^([a-z-]+)=(ok|no)$', done.stdout, re.M))
    print('칸: ' + ' '.join('%s=%s' % (name, cells.get(name, '?')) for name, _ in PROBES))
    return cells


def script_02():
    if POSITIVE:
        home = RUN / 'positive-home'
        home.mkdir()
        (home / 'config.toml').write_text('default_permissions = "codex-audit-judge"\n'
                                          '[permissions.codex-audit-judge]\nextends = ":workspace"\n')
        copy, frozen, other = RUN / 'positive-copy', RUN / 'positive-input', RUN / 'positive-other'
        for folder in (copy, frozen, other):
            folder.mkdir()
        (other / 'bait.txt').write_text('bait')
        resolved = os.pathsep.join(os.path.realpath(entry) for entry in REAL_PATH.split(os.pathsep) if entry)
        cells = probe(home, copy, frozen, other / 'bait.txt', RUN, resolved)
        flipped = [name for name in ('ssh-read', 'slash-tmp-read', 'other-audit-read') if cells.get(name) == 'ok']
        check(len(flipped) == 3, '느슨한 프로필에서 3 칸이 됨으로 바뀌지 않았다: ' + str(flipped))
        return
    case = Case('s02', ['hold'])
    other = case.tmp / 'codex-audit-other-bait'
    other.mkdir()
    (other / 'bait.txt').write_text('bait')
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        call = case.execs()[0]
        config = (case.state / 'config-0.toml').read_text()
        frozen = case.folder() / 'input'
        cells = probe(call['home'], call['cwd'], frozen, other / 'bait.txt', call['env']['TMPDIR'], call['env']['PATH'])
    finally:
        (case.state / 'release-0').touch()
        proc.wait(timeout=60)
    for name, allowed in PROBES:
        check(cells.get(name) == ('ok' if allowed else 'no'), '%s 기대 %s 실제 %s' % (name, allowed, cells.get(name)))
    parsed = tomllib.loads(config)
    network = parsed.get('permissions', {}).get('codex-audit-judge', {}).get('network', {})
    check(network.get('enabled') is False, '판정 프로필 인터넷이 꺼져 있지 않다: ' + str(network))


def script_03():
    case = Case('s03', ['reject', 'reject'], premeasure=True)
    code, out = case.run('impl')
    check(code == 1, 'impl 종료 코드 %s\n%s' % (code, out))
    stages = [json.loads((case.state / 'prem-스크립트-01.json').read_text())] + [call['env'] for call in case.execs()]
    check(len(stages) == 3, '사전 측정 · judge-1 · review-1 세 단계가 아니다: %d' % len(stages))
    fixture = real(case.tmp)
    values = []
    for name, env in zip(('사전 측정', 'judge-1', 'review-1'), stages):
        check(env['TMPDIR'] and len({real(env[key]) for key in ('TMPDIR', 'TMP', 'TEMP')}) == 1,
              name + ' 의 TMPDIR · TMP · TEMP 가 같지 않다: ' + str(env))
        value = real(env['TMPDIR'])
        check(value.startswith(fixture + '/') and value != fixture, name + ' 값이 픽스처 TMPDIR 아래가 아니다: ' + value)
        values.append(value)
    check(len(set(values)) == 3, '세 단계 값이 서로 다르지 않다: ' + str(values))


def script_04():
    positive = None
    cases = [('a', ['approve'], 0, {}), ('b', ['reject', 'reject'], 1, {}), ('c', ['timeout'], 2, {'CODEX_AUDIT_LIMIT': '3'})]
    for label, steps, expected, extra in cases:
        case = Case('s04-' + label, steps, premeasure=True)
        code, out = case.run('impl', extra)
        check(code == expected, '(%s) 종료 코드 기대 %s 실제 %s\n%s' % (label, expected, code, out))
        check(not case.leftovers(), '(%s) 남은 항목: %s' % (label, case.leftovers()))
        copies = [call['cwd'] for call in case.execs()]
        check(copies and not any(Path(copy).exists() for copy in copies), '(%s) 판정 사본이 남았다: %s' % (label, copies))
    case = Case('s04-d', ['hold'], premeasure=True)
    proc = case.start('impl')
    try:
        case.wait_for('holding-0')
        positive = len(case.leftovers())
        os.kill(int((case.folder() / 'pid').read_text()), signal.SIGTERM)
        proc.wait(timeout=60)
    finally:
        if proc.poll() is None:
            os.killpg(proc.pid, signal.SIGKILL)
    print('양성 대조: 도는 중 항목 수 %d' % positive)
    check(positive >= 1, '도는 중에도 항목 수가 0 — 세는 대상이 없다')
    check(not case.leftovers(), '(d) 남은 항목: %s' % case.leftovers())
    check(not any(Path(call['cwd']).exists() for call in case.execs()), '(d) 판정 사본이 남았다')


def script_05():
    case = Case('s05', ['approve'], premeasure=True)
    code, out = case.run('impl')
    check(code == 0, 'impl 종료 코드 %s\n%s' % (code, out))
    call = case.execs()[0]
    prompt = call['args'][-1]
    check('스크립트-01' in prompt and '스크립트-02' in prompt, '(1) 사전 측정한 조건 번호가 지시문에 없다')
    check('사전 측정 기록이 있는 조건은 같은 명령을 다시 돌리지 않는다' in prompt, '(2) 재실행 금지 문장이 없다')
    check('격리 안에서 돌릴 수 있는 측정은 직접 돌린다' not in prompt, '(3) 옛 문장이 남아 있다')
    for label, path in (('얼린 입력', case.folder() / 'input'), ('판정 사본', call['cwd']), ('전용 임시 폴더', call['env']['TMPDIR'])):
        check(str(path).rstrip('/') in prompt or real(path) in prompt, '(4) %s 경로가 지시문에 없다: %s' % (label, path))


def cost_case(name, model):
    case = Case(name, ['approve'], model=model)
    case.usage(1000000, 900000, 20000)
    code, out = case.run('impl')
    check(code == 0, name + ' 종료 코드 %s\n%s' % (code, out))
    return case, section(case.report(), '## 비용')


def script_06():
    case, costs = cost_case('s06', 'gpt-6.1-sol')
    check(costs, '## 비용 절이 없다')
    check(any('judge-1' in line and '0.49' in line for line in costs.splitlines()), '차례 줄에 0.49 가 없다:\n' + costs)
    check(any('합계' in line and '0.49' in line for line in costs.splitlines()), '합계 줄에 0.49 가 없다:\n' + costs)
    code, followed = case.run(['follow', case.folder()])
    check(any('judge-1' in line and '0.49' in line for line in followed.splitlines()), 'follow 에 0.49 가 없다:\n' + followed)
    unknown, costs = cost_case('s06-unknown', 'fixture-unknown')
    check('단가 모름' in costs and re.search(r'1,?000,?000', costs), '단가 모름 · 토큰 수가 없다:\n' + costs)


def month_before():
    first = datetime.date.today().replace(day=1)
    return (first - datetime.timedelta(days=1)).isoformat()


def seeded(today_a, today_b):
    today = datetime.date.today().isoformat()
    row = dict(slug='sample', verb='impl', turn='judge-1', model='gpt-6.1-sol', input=0, cached=0, output=0)
    return [dict(row, date=today, repo='/fixture/repo-a', usd=today_a), dict(row, date=today, repo='/fixture/repo-b', usd=today_b),
            dict(row, date=month_before(), repo='/fixture/repo-a', usd=1.00)]


def usage_lines(out):
    return {key: next((line for line in out.splitlines() if key in line), '') for key in ('오늘', '이번 달', 'repo-a', 'repo-b')}


def script_07():
    case = Case('s07', ['approve'], model='gpt-6.1-sol')
    case.ledger(seeded(0.49, 0.25))
    code, out = case.run(['usage'])
    check(code == 0, 'usage 종료 코드 %s\n%s' % (code, out))
    found = usage_lines(out)
    for key, value in (('오늘', '0.74'), ('이번 달', '0.74'), ('repo-a', '0.49'), ('repo-b', '0.25')):
        check(value in found[key], '%s 줄에 %s 가 없다:\n%s' % (key, value, out))
    before = len((case.qa / 'codex-audit-usage.jsonl').read_text().splitlines())
    case.usage(1000000, 900000, 20000)
    code, out = case.run('impl')
    check(code == 0, 'impl 종료 코드 %s\n%s' % (code, out))
    lines = (case.qa / 'codex-audit-usage.jsonl').read_text().splitlines()
    check(len(lines) == before + 1, '기록 줄이 1 줄 늘지 않았다: %d → %d' % (before, len(lines)))
    last = json.loads(lines[-1])
    for key in ('date', 'repo', 'slug', 'verb', 'turn', 'model', 'input', 'cached', 'output', 'usd'):
        check(key in last, '기록 줄에 %s 칸이 없다: %s' % (key, last))
    check(round(float(last['usd']), 2) == 0.49, '기록 줄 달러가 0.49 가 아니다: %s' % last['usd'])


def budget_case(name, limit, today_a, today_b, steps=('approve',)):
    case = Case(name, steps)
    if limit is not None:
        text = (case.meta / 'project.yaml').read_text()
        (case.meta / 'project.yaml').write_text(text + '  daily_budget_usd: %s\n' % limit)
    case.ledger(seeded(today_a, today_b))
    return case


def script_08():
    for verb, steps in (('draft', ['draft']), ('impl', ['approve'])):
        case = budget_case('s08-over-' + verb, '0.50', 0.49, 0.25, steps)
        code, out = case.run(verb)
        check(code == 2, '%s 상한 넘음 종료 코드 %s\n%s' % (verb, code, out))
        check('한도-예산' in case.report(verb), verb + ' 갈래 한도-예산 이 없다')
        check(not case.execs(), verb + ' 가 Codex 를 불렀다: %d 번' % len(case.execs()))
    case = budget_case('s08-under', '0.50', 0.20, 0.10)
    code, out = case.run('impl')
    check(code == 0, '상한 아래 종료 코드 %s\n%s' % (code, out))
    case = budget_case('s08-unset', None, 60.00, 40.00)
    code, out = case.run('impl')
    check(code == 0, '상한 없음 종료 코드 %s\n%s' % (code, out))


def script_09():
    case = Case('s09-draft', ['timeout'])
    code, out = case.run('draft', {'CODEX_AUDIT_DRAFT_LIMIT': '3'})
    check(code == 2 and len(case.execs()) == 1, 'draft 시간 초과: 종료 %s 호출 %d' % (code, len(case.execs())))
    check('시간-초과' in case.report('draft'), 'draft 갈래 시간-초과 가 없다')
    case = Case('s09-impl', ['timeout'])
    code, out = case.run('impl', {'CODEX_AUDIT_LIMIT': '3'})
    check(code == 2 and len(case.execs()) == 1, 'impl 시간 초과: 종료 %s 호출 %d' % (code, len(case.execs())))
    check('시간-초과' in case.report(), 'impl 갈래 시간-초과 가 없다')
    case = Case('s09-empty', ['empty', 'approve'])
    code, out = case.run('impl')
    check(len(case.execs()) == 2, '빈 응답 다시 시도 호출이 2 번이 아니다: %d' % len(case.execs()))
    case = Case('s09-default', ['draft'])
    code, out = case.run('draft')
    check(code == 0, 'draft 종료 코드 %s\n%s' % (code, out))
    check(any('draft-1' in line and '상한 1500초' in line for line in case.report('draft').splitlines()),
          'draft-1 차례 줄에 상한 1500초 가 없다')


def script_10():
    case = Case('s10', ['reject', 'reject'])
    code, out = case.run('impl')
    check(code == 1, 'impl 종료 코드 %s\n%s' % (code, out))
    folder = case.folder()
    plain = [path for path in folder.rglob('*.jsonl') if 'sessions' in path.parts]
    packed = [path for path in folder.rglob('*.jsonl.gz') if 'sessions' in path.parts]
    check(not plain, '압축 안 된 세션 기록: ' + str(plain))
    check(len(packed) >= 2, '압축 세션 기록이 2 개 미만: %d' % len(packed))
    for path in packed:
        with gzip.open(path, 'rt') as stream:
            check('"turn_context"' in stream.readline(), '풀었을 때 첫 줄이 turn_context 가 아니다: ' + str(path))


def script_11():
    case = Case('s11', ['approve'])
    code, out = case.run('impl', {'CODEX_AUDIT_MODEL': 'gpt-6-luna'})
    check(code == 0, 'impl 종료 코드 %s\n%s' % (code, out))
    for call in case.execs():
        args = call['args']
        check('-m' in args and args[args.index('-m') + 1] == 'gpt-6-luna', '-m 값이 gpt-6-luna 가 아니다')
    check(any('차례' in line and 'gpt-6-luna' in line for line in case.report().splitlines()), 'report 차례 줄 모델')
    case = Case('s11-unset', ['approve'])
    code, out = case.run('impl')
    args = case.execs()[0]['args']
    check('-m' in args and args[args.index('-m') + 1] == 'fixture-supervisor', '변수 없을 때 project.yaml model 이 아니다')


def script_12():
    for label, config in (('none', ''), ('nomode', 'codex_audit:\n  max_rounds: 2\n')):
        for verb in ('draft', 'revise', 'impl'):
            case = Case('s12-%s-%s' % (label, verb), [verb if verb != 'impl' else 'approve'], config=config)
            code, out = case.run(verb)
            check(code == 3 and '감독 판정: SKIPPED (codex_audit.mode: off)' in out,
                  '%s/%s: 종료 %s\n%s' % (label, verb, code, out))
            check(not case.execs(), '%s/%s 가 Codex 를 불렀다' % (label, verb))
    case = Case('s12-codex', ['approve'])
    code, out = case.run('impl')
    check(case.execs(), 'mode: codex 인데 Codex 를 안 불렀다')


def error_01():
    case = Case('e01', ['approve'])
    (case.state / 'no-profile').touch()
    code, out = case.run('impl')
    report = case.report()
    check(code == 2 and '설정-오류' in report and '권한 프로필' in report, '종료 %s\n%s' % (code, report))
    check(not case.execs(), '판정 차례가 Codex 를 불렀다: %d 번' % len(case.execs()))


def error_02():
    rows = seeded(0.49, 0.25) + ['{not json', json.dumps(dict(seeded(0, 0)[0], usd='abc'))]
    case = Case('e02', ['approve'])
    case.ledger(rows)
    code, out = case.run(['usage'])
    check(code == 0 and 'Traceback' not in out, 'usage 종료 %s\n%s' % (code, out))
    check('0.74' in usage_lines(out)['오늘'] and '못 읽은 줄 2' in out, 'usage 합계 · 못 읽은 줄:\n' + out)
    case = budget_case('e02-budget', '0.50', 0.49, 0.25)
    case.ledger(rows)
    code, out = case.run('impl')
    report = case.report()
    check('Traceback' not in out and 'Traceback' not in report, 'impl 에 traceback')
    check('못 읽은 줄 2' in out + report, 'impl 출력 · report 에 못 읽은 줄 2 가 없다')


def at_tip(path):
    return git('show', '%s:%s' % (SOURCE_REF or tip(), path))


def skill_01():
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if '**Codex 감독 설정**' in para), '')
    for word in ('codex-audit-judge', 'daily_budget_usd', 'CODEX_AUDIT_DRAFT_LIMIT', 'CODEX_AUDIT_MODEL', 'usage',
                 'codex-audit-usage.jsonl', 'prices.json', '.jsonl.gz'):
        check(word in block, 'README Codex 감독 설정 문단에 %s 가 없다' % word)
    for path in ('harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md'):
        text = at_tip(path)
        check('칸이 없으면(기본값)' not in text, path + ' 에 옛 문장이 남아 있다')
        check(re.search(r'칸이 없으면[^\n]{0,30}(꺼짐|꺼진|off)', text), path + ' 에 칸 없으면 꺼짐 문장이 없다')
        check('daily_budget_usd' in text, path + ' 에 daily_budget_usd 가 없다')
    template = at_tip('harness/templates/project.yaml')
    block = section('\n## ' + template, 'codex_audit:') or template.split('codex_audit:', 1)[-1]
    check(re.search(r'^\s+mode:\s*off\b', block, re.M) and 'daily_budget_usd' in block, 'project.yaml 틀')


def structure_01():
    upper = tip()
    names = [line for line in git('diff', '--name-only', '%s..%s' % (BASE, upper), '--', '.', ':(exclude).harness').splitlines() if line]
    print('바뀐 경로: ' + ' '.join(names))
    check(SCRIPT in names, 'codex-audit.sh 변경이 없다')
    outside = [name for name in names if name not in SCOPE]
    check(not outside, '범위 밖 경로: ' + str(outside))


def structure_02():
    prices = json.loads(at_tip('harness/templates/codex-audit/prices.json'))
    check(prices.get('checked') and prices.get('source'), 'checked · source 칸')
    values = set()
    for model in MODELS:
        entry = prices.get('models', {}).get(model, {})
        for key, expected in zip(('input', 'cached_input', 'output'), PRICES[model]):
            check(isinstance(entry.get(key), (int, float)), '%s 의 %s 단가가 없다' % (model, key))
            check(abs(float(entry[key]) - expected) < 1e-9, '%s 의 %s 단가 %s ≠ 근거 %s' % (model, key, entry[key], expected))
            values.add(float(entry[key]))
    added = [line[1:] for line in git('diff', '-U0', '%s..%s' % (BASE, tip()), '--', SCRIPT).splitlines()
             if line.startswith('+') and not line.startswith('+++')]
    hits = [line.strip() for line in added for number in re.findall(r'(?<![\w.])\d+\.\d+(?![\w.])', line) if float(number) in values]
    check(not hits, '더한 줄에 단가 값 숫자: ' + str(hits[:5]))


def reuse_01():
    text = at_tip(SCRIPT)
    check(text.count('codex-audit-usage.jsonl') == 1, '사용 기록 파일 이름이 한 곳이 아니다: %d' % text.count('codex-audit-usage.jsonl'))
    check(text.count('prices.json') == 1, '단가 표 이름이 한 곳이 아니다: %d' % text.count('prices.json'))


def reuse_02():
    text, before = at_tip(SCRIPT), git('show', '%s:%s' % (BASE, SCRIPT))
    check(text.count('tempfile.mkdtemp') <= before.count('tempfile.mkdtemp'),
          'mkdtemp 자리가 늘었다: %d → %d' % (before.count('tempfile.mkdtemp'), text.count('tempfile.mkdtemp')))
    check(text.count('def cleanup(') == 1 and 'ACTIVE' in text, 'cleanup · ACTIVE 를 그대로 쓰지 않는다')


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
    files = ['harness/README.md', 'harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md',
             '.harness/sprint-contract-codex-judge-isolation.md']
    target = RUN / 'mdlint'
    total = 0
    for path in files:
        body = subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (upper, path)], capture_output=True, text=True)
        if body.returncode:
            continue
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
    for command in commands:
        run = subprocess.run(['bash', '-c', command], cwd=W, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if run.returncode:
            failed.append(command)
    print('로컬 CI 명령 %d 개 · 실패 %d' % (len(commands), len(failed)))
    check(not failed, '로컬 CI 실패: ' + str(failed))


TABLE = {
    '스크립트-01': script_01, '스크립트-02': script_02, '스크립트-03': script_03, '스크립트-04': script_04,
    '스크립트-05': script_05, '스크립트-06': script_06, '스크립트-07': script_07, '스크립트-08': script_08,
    '스크립트-09': script_09, '스크립트-10': script_10, '스크립트-11': script_11, '스크립트-12': script_12,
    '오류-01': error_01, '오류-02': error_02, '스킬-01': skill_01, '구조-01': structure_01, '구조-02': structure_02,
    '재사용-01': reuse_01, '재사용-02': reuse_02, '진단-02': diagnostics_02, '진단-04': diagnostics_04,
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
