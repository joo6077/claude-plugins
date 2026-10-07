#!/usr/bin/env python3
"""codex-audit-judge-mode 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

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
BASE, BRANCH = '889b2a23', 'feat/codex-audit-judge-mode'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/templates/project.yaml', 'harness/README.md',
         'harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md']
FAKE = HERE.parent.parent / 'codex-judge-isolation' / 'measure' / 'fake.py'
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


def judge_config(case, mode_line):
    return 'codex_audit:\n' + mode_line + '  codex_home: ' + json.dumps(str(case.qa)) + '\n  model: fixture-supervisor\n'


def mode_case(name, steps, mode_line):
    case = Case(name, steps)
    (case.meta / 'project.yaml').write_text('contract_categories:\n  - id: Script\n    prefix: 스크립트\n' + judge_config(case, mode_line))
    return case


SKIP_JUDGE = '감독 판정: SKIPPED (codex_audit.mode: judge — 계약은 Claude 가 쓴다)'


def script_01():
    for verb in ('draft', 'revise'):
        case = mode_case('j01-' + verb, [verb], '  mode: judge\n')
        code, out = case.run(verb)
        check(code == 3 and SKIP_JUDGE in out, '%s: 종료 %s\n%s' % (verb, code, out))
        check(not case.execs(), verb + ' 가 Codex 를 불렀다')


def script_02():
    case = mode_case('j02', ['approve'], '  mode: judge\n')
    code, out = case.run('impl')
    check(code == 0, 'impl 종료 %s\n%s' % (code, out))
    check(case.report().strip().splitlines()[-1] == '감독 판정: APPROVE', 'report 끝 줄이 APPROVE 가 아니다')
    calls = case.execs()
    check(calls and 'default_permissions="codex-audit-judge"' in calls[0]['args'], 'judge-1 에 권한 프로필이 없다')


def script_03():
    case = mode_case('j03-codex', ['draft'], '  mode: codex\n')
    code, out = case.run('draft')
    check(code == 0 and len(case.execs()) == 1, '(a) codex draft: 종료 %s 호출 %d' % (code, len(case.execs())))
    for label, mode_line in (('b', '  mode: off\n'), ('c', '')):
        case = mode_case('j03-' + label, ['approve'], mode_line)
        code, out = case.run('impl')
        check(code == 3 and '감독 판정: SKIPPED (codex_audit.mode: off)' in out and not case.execs(),
              '(%s) 종료 %s 호출 %d\n%s' % (label, code, len(case.execs()), out))
    case = mode_case('j03-d', ['approve'], '  mode: banana\n')
    code, out = case.run('impl')
    report = case.report()
    check(code == 2 and '설정-오류' in report and 'codex · judge · off' in report, '(d) 종료 %s\n%s' % (code, report))


def at_tip(path):
    return git('show', '%s:%s' % (SOURCE_REF or tip(), path))


def skill_01():
    skill = at_tip('harness/skills/sprint-contract/SKILL.md')
    check('`mode: judge`' in skill, 'SKILL.md 에 mode: judge 줄이 없다')
    line = next((row for row in skill.splitlines() if '`mode: judge`' in row), '')
    check('mode: off' in line and 'Claude' in line, 'SKILL.md judge 줄에 off 절차 · Claude 가 쓴다는 말이 없다: ' + line)
    agent = at_tip('harness/agents/qa-evaluator.md')
    line = next((row for row in agent.splitlines() if '`mode: judge`' in row), '')
    check(line and 'impl --detach' in line and '계약 검토' in line, 'qa-evaluator judge 줄: ' + line)
    check('codex | judge | off' in at_tip('harness/templates/project.yaml'), 'project.yaml 틀에 codex | judge | off 가 없다')
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if '**Codex 감독 설정**' in para), '')
    check('`judge`' in block or 'mode: judge' in block, 'README Codex 감독 설정 문단에 judge 가 없다')


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
    files = ['harness/README.md', 'harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md',
             '.harness/sprint-contract-codex-audit-judge-mode.md']
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
    '스크립트-01': script_01, '스크립트-02': script_02, '스크립트-03': script_03, '스킬-01': skill_01,
    '구조-01': structure_01, '진단-02': diagnostics_02, '진단-04': diagnostics_04,
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
