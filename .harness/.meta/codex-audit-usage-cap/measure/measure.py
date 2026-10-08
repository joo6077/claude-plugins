#!/usr/bin/env python3
"""codex-audit-usage-cap 측정 묶음. 종료 코드 0 = PASS, 1 = FAIL.

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
W = Path(os.environ.get('MEASURE_W', '/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-usage-cap'))
BASE, BRANCH = 'b699b17e', 'feat/codex-audit-usage-cap'
SCRIPT = 'harness/scripts/codex-audit.sh'
SCOPE = ['harness/scripts/codex-audit.sh', 'harness/templates/project.yaml', 'harness/templates/codex-audit/prices.json',
         'harness/README.md', 'harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md']
PREVIOUS = [(W / '.harness/.meta/codex-audit-judge-guard/measure/measure.sh', ['스크립트-01', '스크립트-02', '스크립트-03']),
            (W / '.harness/.meta/codex-audit-auth-writeback/measure/measure.sh',
             ['스크립트-01', '스크립트-02', '스크립트-03', '스크립트-05', '스크립트-07'])]
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




def calls_of(case):
    path = case.state / 'calls.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def usage_rows(case):
    path = case.qa / 'codex-audit-usage.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def seeded_row(five, week, resets_in=3600, week_resets_in=None, date=None):
    now = int(time.time())
    week_resets = now + (resets_in if week_resets_in is None else week_resets_in)
    return dict(date=date or datetime.date.today().isoformat(), repo='/fixture/other', slug='other', verb='impl', turn='judge-1',
                model='gpt-6.1-sol', input=0, cached=0, output=0,
                limits={'5시간': dict(used=five, resets_at=now + resets_in), '주간': dict(used=week, resets_at=week_resets)})


def plain_row():
    return dict(date=datetime.date.today().isoformat(), repo='/fixture/other', slug='other', verb='impl', turn='judge-1',
                model='gpt-6.1-sol', input=0, cached=0, output=0)


def blocked(case, label, window, used, limit):
    code, out = case.run('impl')
    report = case.report()
    cause = section(report, '## 실패 원인')
    check(code == 2 and '갈래: 한도-사용량' in report and 'Traceback' not in out, '%s: 종료 %s\n%s' % (label, code, report[-600:]))
    pattern = r'%s\D*%s\s*%%' % (window, used)
    check(re.search(pattern, cause) and re.search(r'%s\s*%%' % limit, cause) and re.search(r'\d{1,2}:\d{2}', cause),
          '%s: 실패 원인에 「%s %s%%」 · 상한 %s%% · 풀리는 시각이 없다\n%s' % (label, window, used, limit, cause))
    check(not case.execs() and not logins(case), '%s: exec %d · 로그인 확인 %d' % (label, len(case.execs()), len(logins(case))))


def ran(case, label):
    code, out = case.run('impl')
    check(code == 0 and len(case.execs()) == 1, '%s: 종료 %s · exec %d\n%s' % (label, code, len(case.execs()), out[-600:]))


def script_01():
    case = Case('u01-five'); case.ledger([seeded_row(75, 10)]); blocked(case, '(a) 5시간 75%', '5시간', 75, 70)
    case = Case('u01-week'); case.ledger([seeded_row(10, 75)]); blocked(case, '(b) 주간 75%', '주간', 75, 70)
    case = Case('u01-past'); case.ledger([seeded_row(95, 95, resets_in=-60)]); ran(case, '(c) 창이 이미 풀림')
    case = Case('u01-latest'); case.ledger([seeded_row(95, 95), seeded_row(10, 10)]); ran(case, '(d) 최근 줄은 10%')
    case = Case('u01-empty'); ran(case, '(e) 기록 없음')
    case = Case('u01-custom'); case.ledger([seeded_row(75, 10)]); config_with(case, '  usage_limit_percent: 80\n'); ran(case, '(f) 상한 80')
    case = Case('u01-custom-hit'); case.ledger([seeded_row(85, 10)]); config_with(case, '  usage_limit_percent: 80\n')
    blocked(case, '(g) 상한 80 · 85%', '5시간', 85, 80)
    for label, value in (('h-abc', 'abc'), ('h-zero', '0'), ('h-over', '150'), ('h-percent', '"70%"')):
        case = Case('u01-' + label); config_with(case, '  usage_limit_percent: %s\n' % value)
        code, out = case.run('impl')
        check(code == 2 and '갈래: 설정-오류' in case.report() and not case.execs(), '(h) 상한 %s: 종료 %s' % (value, code))
    case = Case('u01-plain-after'); case.ledger([seeded_row(75, 10), plain_row()]); blocked(case, '(i) 뒤에 limits 없는 줄', '5시간', 75, 70)
    case = Case('u01-exact'); case.ledger([seeded_row(70, 10)]); blocked(case, '(j) 정확히 70%', '5시간', 70, 70)
    case = Case('u01-mixed'); case.ledger([seeded_row(95, 75, resets_in=-60, week_resets_in=86400)])
    blocked(case, '(k) 5시간은 풀리고 주간 75%', '주간', 75, 70)
    bad = seeded_row(10, 10); bad['limits']['5시간']['used'] = 'abc'
    case = Case('u01-bad-row'); case.ledger([seeded_row(75, 10), bad]); blocked(case, '(l) 최근 줄 used 가 글자', '5시간', 75, 70)


def script_02():
    case = Case('u02')
    code, out = case.run('impl')
    check(code == 0, 'impl 종료 %s\n%s' % (code, out))
    rows = usage_rows(case)
    check(len(rows) == 1, '기록 줄 %d' % len(rows))
    limits = rows[0].get('limits') or {}
    check(limits.get('5시간', {}).get('used') == 12 and limits.get('주간', {}).get('used') == 3, '기록 limits: %s' % limits)
    check(all(isinstance(limits[key].get('resets_at'), int) for key in ('5시간', '주간')), 'resets_at: %s' % limits)
    check('usd' not in rows[0] and 'plan' not in rows[0], '기록 줄에 usd · plan 이 남았다: %s' % sorted(rows[0]))
    usage = section(case.report(), '## 사용량')
    check(any('judge-1' in line and '5시간 12%' in line and '주간 3%' in line for line in usage.splitlines()), '## 사용량:\n' + usage)
    check('달러' not in case.report() and '청구' not in case.report(), 'report.md 에 금액 문구가 남았다')
    code, out = case.run([ 'follow', case.folder(), '--wait-seconds', '1'])
    ends = [line for line in out.splitlines() if '차례 judge-1 끝' in line]
    check(ends and '5시간 12%' in ends[-1] and '청구' not in out, 'follow 차례 끝 줄:\n' + '\n'.join(ends or [out[-400:]]))
    case = Case('u02-timeout', ['timeout'])
    code, out = case.run('impl', {'CODEX_AUDIT_LIMIT': '2'})
    rows = usage_rows(case)
    check(rows and (rows[-1].get('limits') or {}).get('5시간', {}).get('used') == 12, '(시간 초과) 기록 줄: %s' % rows)


def script_03():
    shapes = (('plain', dict(OPENAI_API_KEY='sk-fixture-INVALID-000000000000')),
              ('mode', dict(auth_mode='apikey', OPENAI_API_KEY='sk-fixture-INVALID-000000000000')))
    for label, auth in shapes:
        for verb, steps in (('impl', ['approve']), ('draft', ['draft']), ('revise', ['revise'])):
            case = Case('u03-%s-%s' % (label, verb), steps)
            config_with(case, '')
            (case.qa / 'auth.json').write_text(json.dumps(auth))
            code, out = case.run(verb)
            report = case.report(verb)
            check(code == 2 and '갈래: 로그인-없음' in report and '구독' in section(report, '## 실패 원인'),
                  '%s %s: 종료 %s\n%s' % (label, verb, code, report[-600:]))
            check(not case.execs() and not logins(case), '%s %s: exec %d · 로그인 확인 %d' % (label, verb, len(case.execs()), len(logins(case))))
            check(not case.leftovers(), '%s %s 남은 임시 항목: %s' % (label, verb, case.leftovers()))
            check('## 모델 확인' not in report, '%s %s: 구독 확인보다 모델 확인이 먼저 돌았다' % (label, verb))
    case = Case('u03-missing'); (case.qa / 'auth.json').unlink()
    code, out = case.run('impl')
    check(code == 2 and '갈래: 로그인-없음' in case.report() and not case.execs(), 'auth.json 없음: 종료 %s' % code)


def script_04():
    case = Case('u04')
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    case.ledger([seeded_row(1, 1, resets_in=-60, date=yesterday)])
    code, out = case.run('impl')
    check(code == 0, 'impl 종료 %s' % code)
    code, out = case.run(['usage'])
    print(out.strip())
    check(code == 0 and '5시간 12%' in out and '주간 3%' in out and re.search(r'차례 1\b', out) and re.search(r'\d{1,2}:\d{2}', out),
          'usage 출력:\n' + out)
    check('달러' not in out, 'usage 에 금액이 남았다')


def script_05():
    # 앞 묶음은 지운 가지 feat/codex-audit-judge-mode 끝을 잰다. 사본을 떠서 재는 가지만 이번 가지로 바꾼다.
    for path, ids in PREVIOUS:
        copy = RUN / ('prev-' + path.parent.parent.name)
        if not copy.exists():
            shutil.copytree(path.parent, copy)
            script = copy / 'measure.py'
            text = script.read_text()
            check(text.count("'feat/codex-audit-judge-mode'") == 1, path.parent.parent.name + ' 가지 이름 자리를 못 찾음')
            script.write_text(text.replace("'feat/codex-audit-judge-mode'", repr(BRANCH)))
        for key in ids:
            done = subprocess.run(['bash', str(copy / 'measure.sh'), key], capture_output=True, text=True, stdin=subprocess.DEVNULL,
                                  timeout=600, env=dict(os.environ, MEASURE_W=str(W)))
            tail = done.stdout.strip().splitlines()[-1] if done.stdout.strip() else '출력 없음'
            print('%s %s → %s' % (path.parent.parent.name, key, tail))
            check(done.returncode == 0 and 'Traceback' not in done.stdout + done.stderr, '앞 측정 %s %s 종료 %s' % (path.parent.parent.name, key, done.returncode))


def model_of(call):
    args = call['args']
    return args[args.index('-m') + 1] if '-m' in args else ''


def script_06():
    for verb, steps, expected in (('draft', ['draft'], 'm-draft'), ('impl', ['approve'], 'm-impl')):
        case = Case('u06-' + verb, steps, model='m-base')
        config_with(case, '  model_draft: m-draft\n  model_impl: m-impl\n')
        code, out = case.run(verb)
        check(code == 0 and [model_of(c) for c in case.execs()] == [expected], '%s 모델: %s' % (verb, [model_of(c) for c in case.execs()]))


def skill_01():
    readme = at_tip('harness/README.md')
    block = next((para for para in readme.split('\n\n') if '**Codex 감독 설정**' in para), '')
    for word in ('usage_limit_percent', '70', '## 사용량', '한도-사용량', '로그인-없음'):
        check(word in block, 'README 감독 설정 문단에 %s 가 없다' % word)
    template = at_tip('harness/templates/project.yaml').split('codex_audit:', 1)[-1]
    check(re.search(r'^\s+usage_limit_percent:', template, re.M), 'project.yaml 틀에 usage_limit_percent 줄이 없다')
    for path in ('harness/README.md', 'harness/templates/project.yaml', 'harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md'):
        text = at_tip(path)
        for stale in ('daily_budget_usd', '한도-예산', 'API 키로 쓴 만큼', '## 비용', '청구 없음', 'prices.json', 'CODEX_AUDIT_MODELS_URL'):
            check(stale not in text, '%s 에 옛 문구 「%s」 가 남았다' % (path, stale))


def reuse_01():
    text = at_tip(SCRIPT)
    for stale in ('daily_budget', 'load_prices', 'turn_cost', 'money(', 'spent(', 'check_budget', 'SUBSCRIBED', 'subscribed',
                  "'usd'", 'usd=', '달러', 'prices.json', 'gpt_models', 'MODELS_URL'):
        check(stale not in text, 'codex-audit.sh 에 「%s」 가 남았다' % stale)
    found = len(re.findall(r'\bsubscription\(', text))
    check(found == 2, 'subscription( 등장 수 %d (정의 1 · 판정 1 기대)' % found)
    listed = subprocess.run(['git', '-C', str(W), 'cat-file', '-e', '%s:harness/templates/codex-audit/prices.json' % (SOURCE_REF or tip())])
    check(listed.returncode != 0, 'prices.json 이 가지 끝에 남아 있다')


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
    files = ['harness/README.md', 'harness/skills/sprint-contract/SKILL.md', 'harness/agents/qa-evaluator.md',
             '.harness/sprint-contract-codex-audit-usage-cap.md']
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
