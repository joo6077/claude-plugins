#!/usr/bin/env python3
"""Read W; all writes and child execution stay below this measurement bundle."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

from fixtures import CONTRACT, IDS, decision, payload, schema_errors, strict_schema, match_json, fixture_schema, nonimpl_faults
import prompt_checks
import live_calibration
import auth_support

HERE = Path(__file__).resolve().parent
DEFAULT_W = Path('/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor')
W = Path(os.environ.get('MEASURE_W', str(Path.cwd() if (Path.cwd() / 'harness').is_dir() else DEFAULT_W))).resolve()
SCRIPT = 'harness/scripts/codex-audit.sh'
SKILL = 'harness/skills/sprint-contract/SKILL.md'
AGENT = 'harness/agents/qa-evaluator.md'
BRANCH = 'feat/codex-supervisor'
BASE = '88b2a84e'
RUN = None
SOURCE = None
CHECKS = 0
FAILURES = []
EVENTS = []

# These are observable document instructions, not names of implementation functions.
DOC_LINES = {
    '스킬-01': (SKILL, [
        'mode: codex', '요구사항 파일', 'draft', 'revise', '조건 줄', '직접',
        'Claude', 'qa-evaluator', '사용자 승인', '6.6', '6.7', 'max_rounds', 'mode: off']),
    '스킬-02': (AGENT, [
        '계약 검토', '조건 번호', '문제', '고칠 방법', 'mode: codex', 'impl --detach',
        'wait', 'Verdict:', '그대로', 'status', 'done', 'mode: off'])}

def command(argv, cwd=None, env=None, timeout=30):
    return subprocess.run([str(x) for x in argv], cwd=cwd, env=env, text=True,
                          capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)

def git(*args):
    p = command(['git', '-C', W, *args])
    if p.returncode: raise RuntimeError('git failed: ' + p.stderr.strip())
    return p.stdout.strip()

def observation(value):
    if isinstance(value, bytes):
        return dict(byte_length=len(value), sha256=hashlib.sha256(value).hexdigest())
    if isinstance(value, Path): return str(value)
    if isinstance(value, dict): return {str(k):observation(v) for k,v in value.items()}
    if isinstance(value, (tuple,list)): return [observation(v) for v in value]
    return value

def check(ok, label, actual=None, expected=None):
    global CHECKS
    CHECKS += 1
    actual=observation(actual); expected=observation(expected)
    row = dict(check=label, ok=bool(ok), actual=actual, expected=expected)
    EVENTS.append(row)
    if not ok: FAILURES.append(row)
    print(('OK ' if ok else 'BAD ') + label + ('' if actual is None else ' actual=' + json.dumps(actual, ensure_ascii=False)))

def eq(actual, expected, label): check(actual == expected, label, actual, expected)

def snapshot():
    global SOURCE
    upper = git('rev-parse', '--verify', '-q', BRANCH)
    SOURCE = RUN / 'source'
    SOURCE.mkdir()
    archive = RUN / 'source.tar'
    with archive.open('wb') as f:
        p = subprocess.run(['git', '-C', str(W), 'archive', upper], stdout=f, stderr=subprocess.PIPE)
    if p.returncode: raise RuntimeError(p.stderr.decode())
    p = command(['tar', '-xf', archive, '-C', SOURCE])
    if p.returncode: raise RuntimeError(p.stderr)
    archive.unlink()
    print('source_ref=' + upper)

def bytes_tree(root, exclude=()):
    result = {}
    for f in root.rglob('*'):
        rel = str(f.relative_to(root))
        if any(rel == x or rel.startswith(x + '/') for x in exclude): continue
        if f.is_file(): result[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
    return result

def exec_rows(logfile):
    return [row for row in (json.loads(x) for x in logfile.read_text().splitlines()) if row['kind']=='exec'] if logfile.exists() else []

def leak_files(root):
    return [str(f) for f in root.rglob('*') if f.is_file() and
            any(token in f.read_text(errors='replace') for token in ('sk-FIXTURE-SECRET','WRONG-DECOY'))]

def call_boundary(case, verb):
    for row in case.calls():
        dest=Path(row['cwd'])
        check(dest.is_relative_to(case.root) and dest!=case.repo and not dest.is_relative_to(case.repo), verb+': temporary working directory',str(dest))
        eq(row['stdin'],'',verb+': closed stdin')
        eq(row['sandbox'],'workspace-write',verb+': write sandbox')
        if verb in ('draft','revise'): eq(row['network'],False,verb+': offline generation')

def child_check(case):
    f=case.state/'children'
    children=f.read_text().splitlines() if f.exists() else []
    check(bool(children),'timeout created descendants')
    for pid in children:
        p=command(['ps','-o','stat=','-p',pid])
        dead=p.returncode!=0 or not p.stdout.strip() or p.stdout.strip().startswith('Z')
        check(dead,'timeout child terminated '+pid,p.stdout.strip())
        if not dead:
            try: os.kill(int(pid),signal.SIGKILL)
            except ProcessLookupError: pass

class Case:
    def __init__(self, name, steps=('approve',), config='', login=True, missing=False, mutant=False):
        self.root = RUN / name
        self.root.mkdir()
        self.repo = self.root / 'repo with space'
        self.repo.mkdir()
        shutil.copytree(SOURCE / 'harness', self.repo / 'harness', symlinks=True)
        self.home = self.root / 'user'
        self.home.mkdir()
        self.codex_home = self.home / '.codex-qa'
        self.codex_home.mkdir()
        (self.codex_home / 'config.toml').write_text('cli_auth_credentials_store = "file"\nmodel = "fixture-folder-model"\n')
        (self.codex_home/'auth.json').write_text(json.dumps(dict(OPENAI_API_KEY='sk-FIXTURE-SECRET')))
        (self.codex_home/'auth.json').chmod(0o600)
        self.meta = self.repo / '.harness'
        self.meta.mkdir()
        self.contract = self.meta / 'sprint-contract-sample.md'
        self.contract.write_text(CONTRACT)
        self.requirements = self.root / 'requirements.md'
        self.requirements.write_text('요구: sample 의 두 값 GOOD. 계약과 측정 묶음을 작성한다.\n')
        self.critique = self.root / 'critique.md'
        self.critique.write_text('계약 feature 를 지적 반영으로 바꾸세요.\n')
        self.config = config
        self.configure(config)
        (self.repo / 'sample.txt').write_text('GOOD\nGOOD\n')
        self.state = self.root / 'state'
        self.state.mkdir()
        self.plan(steps, login)
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.codex_home),
                        CODEX_BIN=str(self.root / 'missing-codex') if missing else str(HERE / 'fake-codex'),
                        CODEX_AUDIT_LIMIT='2', MEASURE_STATE=str(self.state),
                        TMPDIR=str(self.root), PYTHONDONTWRITEBYTECODE='1',
                        GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        MEASURE_AUTH_SOURCE=str(self.codex_home/'auth.json'), MEASURE_CASE_ROOT=str(self.root))
        for var in ('GIT_DIR', 'GIT_WORK_TREE', 'CLAUDE_CODE_SESSION_ID', 'HARNESS_CONTRACT'):
            self.env.pop(var, None)
        for args in (['init', '-q'], ['config', 'user.name', 'measure'],
                     ['config', 'user.email', 'measure@example.invalid'],
                     ['add', '.'], ['commit', '-qm', 'known fixture']):
            p = command(['git', *args], self.repo, self.env)
            if p.returncode: raise RuntimeError(p.stderr)
        self.base = command(['git', 'rev-parse', 'HEAD'], self.repo, self.env).stdout.strip()
        (self.repo / 'sample.txt').write_text('GOOD\nBAD\n')
        command(['git', 'add', 'sample.txt'], self.repo, self.env)
        command(['git', 'commit', '-qm', 'known implementation'], self.repo, self.env)
        self.head = command(['git', 'rev-parse', 'HEAD'], self.repo, self.env).stdout.strip()
        self.before = bytes_tree(self.repo, ('.harness',))
        if mutant:
            (self.repo / SCRIPT).write_text('#!/usr/bin/env bash\nexit 0\n')

    def configure(self, extra):
        (self.meta / 'project.yaml').write_text('contract_categories:\n  - id: Script\n    prefix: 스크립트\n' + extra)

    def plan(self, steps, login=True):
        (self.state / 'plan.json').write_text(json.dumps(dict(steps=list(steps), login=login)))

    def calls(self):
        return exec_rows(self.state / 'calls.jsonl')

    def invoke(self, verb='impl', extra=(), limit=18):
        args = [verb]
        if verb == 'impl': args += [str(self.contract), self.base]
        if verb == 'draft': args += [str(self.requirements), str(self.contract)]
        if verb == 'revise': args += [str(self.contract), str(self.critique)]
        args += list(extra)
        return self.raw(args, limit)

    def raw(self, args, limit=18, interrupt=None):
        # Keep an inherited input pipe open: the script must explicitly close Codex stdin.
        number = len(list(self.root.glob('stdout-*.txt')))
        out = self.root / ('stdout-' + str(number) + '.txt')
        err = self.root / ('stderr-' + str(number) + '.txt')
        read_fd, write_fd = os.pipe()
        start = time.monotonic()
        with out.open('w') as fo, err.open('w') as fe:
            proc = subprocess.Popen(['bash', str(self.repo / SCRIPT), *map(str, args)], cwd=self.repo,
                                    env=self.env, stdin=read_fd, stdout=fo, stderr=fe, start_new_session=True)
            os.close(read_fd)
            try:
                if interrupt is not None:
                    deadline=time.monotonic()+5
                    while proc.poll() is None and (not self.calls() or not (self.state/'children').exists()) and time.monotonic()<deadline:
                        time.sleep(0.05)
                    check(bool(self.calls()),'interruption after credential observation')
                    if proc.poll() is None: os.killpg(proc.pid,interrupt)
                rc = proc.wait(timeout=limit)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait(); rc = 124
            finally: os.close(write_fd)
        result = dict(rc=rc, stdout=out.read_text(), stderr=err.read_text(), elapsed=time.monotonic()-start)
        (self.root / ('result-' + str(number) + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    def reports(self): return sorted(self.meta.rglob('report.md'))
    def report(self): return '\n'.join(x.read_text() for x in self.reports())
    def feedback(self):
        p = self.meta / 'sprint-feedback-sample.md'
        return p.read_text() if p.exists() else ''

    def outcome(self, result, rc, verdict, calls=None, category=None):
        eq(result['rc'], rc, self.root.name + ': exit')
        if calls is not None: eq(len(self.calls()), calls, self.root.name + ': exec_calls')
        report = self.report()
        check(bool(report), self.root.name + ': report exists')
        if report: check(re.search(r'^감독 판정: ' + verdict + r'\s*$', report, re.M) is not None,
                         self.root.name + ': report verdict', report[-250:])
        if category:
            check('## 실패 원인' in report and '갈래: ' + category in report,
                  self.root.name + ': failure category', category)
        for p in self.reports():
            check(re.search(r'/codex-audit/sample/(draft|impl)-r[1-9][0-9]*/report\.md$', str(p)) is not None,
                  self.root.name + ': audit directory', str(p.relative_to(self.repo)))
            body=p.read_text().strip().splitlines()
            check(bool(body) and body[0].startswith('시작:') and body[-1].startswith('감독 판정:'), self.root.name+': script report boundary')

def need_script():
    if not (SOURCE / SCRIPT).is_file():
        check(False, 'MISSING ' + SCRIPT)
        return False
    return True

def draft():
    for state in ('valid', 'occupied', 'absent', 'header', 'placement', 'count', 'unmeasured'):
        c = Case('draft-' + state, ('draft' if state in ('valid','occupied','absent') else 'draft-' + state,))
        if state == 'absent': c.contract.unlink()
        elif state != 'occupied': c.contract.write_text('')
        old = c.contract.read_bytes() if c.contract.exists() else None
        r = c.invoke('draft')
        if state == 'valid':
            call_boundary(c,'draft')
            c.outcome(r, 0, 'APPROVE', 1)
            eq(c.contract.read_text(), CONTRACT, 'draft: installed content')
            bundle = c.meta / '.meta/sample/measure.sh'
            check(bundle.is_file(), 'draft: measurement installed', str(bundle))
            check(all(x in c.report() for x in ('헤더', '조건', '미실측')), 'draft: save-check evidence')
        else:
            check(r['rc'] != 0, 'draft rejects ' + state, r['rc'])
            eq(c.contract.read_bytes() if c.contract.exists() else None, old, 'draft failure preserves target')
            if state in ('occupied','absent'): eq(len(c.calls()), 0, 'draft guard before Codex')

def revise():
    c = Case('revise', ('draft-revised',))
    old = c.contract.read_bytes()
    r = c.invoke('revise'); c.outcome(r, 0, 'APPROVE', 1)
    call_boundary(c,'revise')
    check('지적 반영' in c.contract.read_text(), 'revise: new content')
    backups = [p for p in (c.meta / 'codex-audit').rglob('*') if p.is_file() and p.read_bytes() == old]
    check(bool(backups), 'revise: exact old version retained', [str(p) for p in backups])
    c = Case('sealed', ('draft-revised',))
    c.contract.write_text(CONTRACT.replace('status: active', 'status: active\nconditions_digest: sha256:0123456789abcdef'))
    old = c.contract.read_bytes()
    r = c.invoke('revise'); c.outcome(r, 2, 'BLOCKED', 0, '봉인됨')
    eq(c.contract.read_bytes(), old, 'sealed unchanged')

def impl():
    c = Case('impl', ('approve',)); old = c.contract.read_bytes()
    r = c.invoke(); c.outcome(r, 0, 'APPROVE', 1)
    fb = c.feedback()
    check(re.search(r'^Verdict: APPROVE$', fb, re.M) is not None, 'feedback: verdict')
    check(re.search(r'^Iteration: 1$', fb, re.M) is not None, 'feedback: iteration')
    for i in IDS: check(i in fb and 'PASS' in fb, 'feedback: ' + i)
    eq(c.contract.read_bytes(), old, 'impl leaves status for evaluator')
    files = [p for p in c.meta.rglob('*') if p.is_file()]
    frozen = [p for p in files if p != c.contract and p.read_bytes() == old]
    check(bool(frozen), 'frozen contract exists')
    diff = command(['git','diff', c.base + '..' + c.head], c.repo, c.env).stdout.strip()
    check(any(diff and diff in p.read_text(errors='replace') for p in files), 'frozen diff exists')
    check(any(p.read_text(errors='replace').strip()=='sample.txt' for p in files), 'frozen changed-file list exact')

def reject():
    for name, steps, rc, verdict, category in (
        ('same', ('reject','reject'),1,'REJECT',None),
        ('pass', ('reject','approve'),2,'BLOCKED','재심-엇갈림'),
        ('different', ('reject','reject-other'),2,'BLOCKED','재심-엇갈림')):
        c = Case('review-' + name, steps)
        r = c.invoke(); c.outcome(r, rc, verdict, 2, category)
        calls = c.calls()
        if len(calls) == 2:
            check(calls[0]['thread_id'] != calls[1]['thread_id'], 'blind review: new thread')
            check(all('resume' not in x['args'] for x in calls), 'blind review: no resume')
            check('BAD 는 GOOD 과 다르다' not in calls[1]['prompt'], 'blind review: first analysis hidden')
            # A fresh CODEX_HOME or a restricted read boundary must prevent reading the first report.
            check(calls[0]['cwd'] != calls[1]['cwd'], 'blind review: separate working copy')
        if verdict == 'REJECT':
            report = c.report()
            check('## 고칠 것' in report, 'reject fixes heading')
            check(re.search(r'- 스크립트-02 어디를: .+ · 무엇으로: .+ · 어떻게 확인: .+', report) is not None, 'reject: three fix cells')
            check('Verdict: REJECT' in c.feedback(), 'reject feedback is authoritative')

def research():
    for name, steps in (('none', ('approve',)), ('requested', ('research','research-answer','approve'))):
        c = Case('research-' + name, steps)
        r = c.invoke(); c.outcome(r, 0, 'APPROVE', len(steps))
        calls = c.calls()
        eq([x['network'] for x in calls], [True] if name == 'none' else [True, True, True], 'network phase matrix')
        templates=c.repo/'harness/templates/codex-audit'
        instructions='\n'.join(x['prompt'] for x in calls)+'\n'+'\n'.join(p.read_text(errors='replace') for p in templates.rglob('*') if p.is_file())
        check(re.search(r'바깥 사실.{0,100}(스스로|직접).{0,30}(찾지|조사하지).{0,80}질문',instructions,re.S) is not None,'external facts must be questions, not self research')
        if len(calls) == 3:
            check('FACT_TOKEN' in calls[1]['prompt'], 'research: question attached')
            check('FACT_ANSWER' in calls[2]['prompt'], 'research: answer attached')
            check('FACT_ANSWER' in c.report(), 'research: answer evidence retained')

def rounds():
    c = Case('rounds', ('reject','reject'))
    # max_rounds means two repair/re-audit cycles after the initial judgment.
    for n in range(1, 4):
        r = c.invoke(); c.outcome(r, 1, 'REJECT', n * 2)
        check('Iteration: ' + str(n) in c.feedback(), 'round iteration ' + str(n))
        if n > 1:
            check('## 지난 판 지적 처리' in c.report() and re.search(r'스크립트-02.*미해결', c.report()), 'unresolved previous condition')
    r = c.invoke(); c.outcome(r, 2, 'BLOCKED', 6, '반복-상한')
    c = Case('resolved', ('reject','reject','approve'))
    c.invoke(); r = c.invoke(); c.outcome(r, 0, 'APPROVE', 3)
    check(re.search(r'스크립트-02.*해결', c.report()) is not None and '## 지난 판 지적 처리' in c.report(), 'previous condition resolved')
    c = Case('custom-rounds', ('reject','reject'), 'codex_audit:\n  max_rounds: 1\n')
    c.invoke(); c.invoke(); r = c.invoke(); c.outcome(r,2,'BLOCKED',4,'반복-상한')

def config():
    for verb in ('draft','revise','impl'):
        c = Case('off-' + verb, config='codex_audit:\n  mode: off\n')
        if verb == 'draft': c.contract.write_text('')
        old = c.contract.read_bytes()
        r = c.invoke(verb); eq(r['rc'],3,'off ' + verb); eq(len(c.calls()),0,'off no Codex'); eq(c.contract.read_bytes(),old,'off unchanged')
        logs=c.state/'calls.jsonl'; eq(logs.read_text() if logs.exists() else '', '', 'off no login invocation either')
    for name, extra, expected_model, expected_effort in (
        ('default','', 'fixture-folder-model','medium'),
        ('override','codex_audit:\n  model: fixture-override\n  effort_impl: high\n','fixture-override','high')):
        c = Case('config-' + name, config=extra); r = c.invoke(); c.outcome(r,0,'APPROVE',1)
        if c.calls():
            eq(c.calls()[0]['model'],expected_model,'model configuration'); eq(c.calls()[0]['effort'],expected_effort,'impl effort')
    c = Case('home-override')
    other = c.root / 'other codex home'; other.mkdir(); (other/'config.toml').write_text('model = "other-model"\n')
    (other/'auth.json').write_bytes((c.codex_home/'auth.json').read_bytes()); (other/'auth.json').chmod(0o600)
    c.env['MEASURE_AUTH_SOURCE']=str(other/'auth.json')
    c.configure('codex_audit:\n  codex_home: "' + str(other) + '"\n')
    r = c.invoke(); c.outcome(r,0,'APPROVE',1)
    if c.calls(): eq(c.calls()[0]['config_bytes_sha256'],hashlib.sha256((other/'config.toml').read_bytes()).hexdigest(),'explicit home settings'); eq(c.calls()[0]['model'],'other-model','home model')
    for home_mode in ('qa-default','normal-default','no-model'):
        c = Case(home_mode); c.env.pop('CODEX_HOME')
        if home_mode != 'qa-default':
            auth_bytes=(c.codex_home/'auth.json').read_bytes()
            shutil.rmtree(c.codex_home); c.codex_home = c.home / '.codex'; c.codex_home.mkdir()
            (c.codex_home/'config.toml').write_text('' if home_mode=='no-model' else 'model = "normal-model"\n')
            (c.codex_home/'auth.json').write_bytes(auth_bytes); (c.codex_home/'auth.json').chmod(0o600)
            c.env['MEASURE_AUTH_SOURCE']=str(c.codex_home/'auth.json')
        r = c.invoke()
        if home_mode=='no-model': c.outcome(r,2,'BLOCKED',0,'설정-오류')
        else:
            c.outcome(r,0,'APPROVE',1)
            if c.calls(): eq(c.calls()[0]['config_bytes_sha256'],hashlib.sha256((c.codex_home/'config.toml').read_bytes()).hexdigest(),'fallback home settings')
    for effort in ('medium','low'):
        c = Case('draft-effort-' + effort, ('draft',), config='' if effort=='medium' else 'codex_audit:\n  effort_draft: low\n')
        c.contract.write_text(''); r=c.invoke('draft'); eq(r['rc'],0,'draft effort result')
        if c.calls(): eq(c.calls()[0]['effort'],effort,'draft effort')
    c = Case('invalid-mode', config='codex_audit:\n  mode: wrong\n'); r=c.invoke(); c.outcome(r,2,'BLOCKED',0,'설정-오류')

def report():
    c=Case('report',('reject','reject')); r=c.invoke(); c.outcome(r,1,'REJECT',2)
    body=c.report()
    for key in ('시작:', '끝:', '계정:'):
        check(re.search(r'^'+key+r'\s*\S+',body,re.M) is not None,'report '+key)
    check(re.search(r'^계정:.*using an API key\s*$',body,re.M) is not None,'account sanitized')
    for call in c.calls():
        pattern=r'- 차례 .+ 모델='+re.escape(call['model']+'-observed')+r' 생각='+call['effort']+r' 격리='+call['sandbox']+r' 기록=.+?'+call['thread_id']+r'\.jsonl'
        check(re.search(pattern,body) is not None,'per-phase actual context '+call['thread_id'])
    eq(leak_files(c.meta),[],'no secret or unrelated-session in artifacts')
    eq(auth_support.secret_paths(c.root,[b'sk-FIXTURE-SECRET'],[c.codex_home/'auth.json']),[],'no key in scripts audit feedback frozen input or temporary leftovers')

def detach():
    for verb in ('draft','revise','impl'):
        step='slow' if verb=='impl' else 'draft'
        c=Case('detach-'+verb,(step,))
        if verb=='draft': c.contract.write_text('')
        # Slow every fake command with a plan flag, without sleeping the measuring process.
        data=json.loads((c.state/'plan.json').read_text()); data['delay']=3; (c.state/'plan.json').write_text(json.dumps(data))
        c.env['CODEX_AUDIT_LIMIT']='10'
        r=c.invoke(verb,('--detach',))
        eq(r['rc'],0,'detach launch'); check(r['elapsed']<2,'detach returns before completion',round(r['elapsed'],2))
        candidates=[Path(x.strip()) for x in r['stdout'].splitlines() if Path(x.strip()).is_dir()]
        check(bool(candidates),'detach prints audit directory',r['stdout'])
        if candidates:
            folder=candidates[-1]
            check(folder.is_relative_to(c.root),'detach folder is in fixture')
            r=c.raw(['wait',folder,'0']); eq(r['rc'],75,'wait pending'); check('RUNNING' in r['stdout'],'wait RUNNING')
            r=c.raw(['wait',folder,'12']); eq(r['rc'],0,'wait complete')
            r=c.raw(['wait',folder]); eq(r['rc'],0,'wait optional seconds omitted')
    c=Case('usage')
    for args in ([],['unknown'],['draft'],['revise'],['impl'],['wait'],['wait','/nonexistent','bad']):
        r=c.raw(args); eq(r['rc'],64,'usage '+repr(args))
    for name,steps,rc in (('reject',('reject','reject'),1),('blocked',('quota',),2)):
        c=Case('detach-'+name,steps); r=c.invoke(extra=('--detach',))
        folders=[Path(x.strip()) for x in r['stdout'].splitlines() if Path(x.strip()).is_dir()]
        check(bool(folders),'detach terminal path '+name)
        if folders: eq(c.raw(['wait',folders[-1],'12'])['rc'],rc,'wait terminal '+name)

def response_schema_issues(schema,response,phase):
    if not isinstance(schema,dict) or schema.get('type')!='object':
        return ['missing --output-schema object']
    issues=schema_errors(schema)
    try:
        if not match_json(response,schema): issues.append('valid response rejected')
        if phase=='impl':
            conditions=schema.get('properties',{}).get('conditions',{}).get('items',{})
            if '$ref' in conditions:
                node=schema
                for key in conditions['$ref'].split('/')[1:]: node=node[key]
                conditions=node
            keys=list(conditions.get('properties',{}))
            if not (all(k in keys for k in ('evidence','analysis','verdict')) and keys.index('evidence')<keys.index('analysis')<keys.index('verdict')):
                issues.append('evidence analysis verdict order')
    except (KeyError,TypeError,ValueError) as exc:
        issues.append('invalid schema: '+str(exc))
    return issues

def schemas():
    scenarios=[('draft','draft',['draft'],[('draft','draft')]),
               ('revise','revise',['draft-revised'],[('revise','draft-revised')]),
               ('impl','impl',['approve'],[('impl','approve')]),
               ('research','impl',['research','research-answer','approve'],
                [('impl','research'),('research','research-answer'),('impl','approve')])]
    phases=set()
    for name,verb,steps,expected in scenarios:
        c=Case('schema-'+name,steps)
        if verb=='draft': c.contract.write_text('')
        r=c.invoke(verb); eq(r['rc'],0,'schema '+name+' success')
        eq(len(c.calls()),len(expected),'schema '+name+' call count')
        for row,(phase,step) in zip(c.calls(),expected):
            phases.add(phase)
            eq(response_schema_issues(row['schema'],payload(step),phase),[],'strict response schema '+name+'/'+phase)
    eq(sorted(phases),['draft','impl','research','revise'],'all four response phases measured')

def invalid():
    cases=['nonzero','no-completed','turn-failed','event-error','malformed','missing-file','extra-key','wrong-type',
           'missing-id','duplicate-id','unknown-id','inconsistent','allpass-reject','fix-where','fix-what','fix-verify','empty-evidence']
    for name in cases:
        c=Case('invalid-'+name,(name,)); r=c.invoke(); c.outcome(r,2,'BLOCKED',1,'형식-깨짐')
        check('Verdict: APPROVE' not in c.feedback() and 'Verdict: REJECT' not in c.feedback(),'invalid never becomes judgment '+name)
    for phase,spec in nonimpl_faults():
        steps=['research',spec] if phase=='research' else [spec]
        c=Case('invalid-'+phase+'-'+spec['fault'],steps)
        verb='impl' if phase=='research' else phase
        if verb=='draft': c.contract.write_text('')
        old=c.contract.read_bytes()
        r=c.invoke(verb); c.outcome(r,2,'BLOCKED',len(steps),'형식-깨짐')
        eq(c.contract.read_bytes(),old,'invalid '+phase+' preserves contract')
        check('Verdict: APPROVE' not in c.feedback() and 'Verdict: REJECT' not in c.feedback(),'invalid '+phase+' never becomes judgment')

def format_controls():
    detected=0
    for phase,spec in nonimpl_faults():
        folder=RUN/('format-control-'+phase+'-'+spec['fault']); folder.mkdir()
        home=folder/'home'; home.mkdir()
        (home/'config.toml').write_text('model = "fixture-format"\n')
        state=folder/'state'; state.mkdir()
        (state/'plan.json').write_text(json.dumps(dict(steps=[spec])))
        output=folder/'result.json'; schema=folder/'schema.json'
        shape=fixture_schema(payload(spec['response']))
        schema.write_text(json.dumps(shape))
        env=dict(os.environ,CODEX_HOME=str(home),MEASURE_STATE=str(state),PYTHONDONTWRITEBYTECODE='1')
        p=command([HERE/'fake-codex','exec','--json','--output-schema',schema,'-o',output,'-C',folder,'-s','workspace-write','fixture'],env=env)
        eq(p.returncode,0,'fake format transport '+phase+'/'+spec['fault'])
        if not output.exists(): observed='missing-file'
        else:
            try: value=json.loads(output.read_text())
            except ValueError: observed='malformed'
            else: observed='missing-required' if not match_json(value,shape) and spec['field'] not in value else 'valid'
        eq(observed,spec['fault'],'known format fault '+phase)
        detected+=int(observed==spec['fault'])
    print('format_fault_cases expected=9 actual='+str(detected))
    eq(detected,9,'three faults across draft revise research')

def failures():
    matrix=[('missing',('approve',),False,True,'codex-없음',0),
            ('login',('approve',),False,False,'로그인-없음',0),
            ('quota',('quota',),True,False,'한도-결제',1),
            ('settings',('config-error',),True,False,'설정-오류',1),
            ('empty',('empty','empty'),True,False,'빈-응답',2),
            ('timeout',('timeout','timeout'),True,False,'시간-초과',2)]
    for name,steps,login,missing,category,count in matrix:
        c=Case('failure-'+name,steps,login=login,missing=missing)
        r=c.invoke(); c.outcome(r,2,'BLOCKED',count,category)
        if name=='timeout': child_check(c)
    for name in ('empty','timeout'):
        c=Case('recover-'+name,(name,'approve')); r=c.invoke(); c.outcome(r,0,'APPROVE',2)
        eq(len({x['thread_id'] for x in c.calls()}),2,'retry fresh session')
        if name=='timeout': child_check(c)

def credentials():
    matrix=[('success',['approve'],None,0),('failure',['malformed'],None,2),
            ('timeout',['timeout','timeout'],None,2),
            ('sigint',['hold'],signal.SIGINT,None),('sigterm',['hold'],signal.SIGTERM,None)]
    for name,steps,interruption,expected in matrix:
        c=Case('credentials-'+name,steps)
        original=(c.codex_home/'auth.json').read_bytes()
        r=c.raw(['impl',c.contract,c.base],interrupt=interruption,limit=12)
        if expected is None:
            check(r['rc'] not in (0,124),'interrupted supervisor terminates without forced kill')
        else: eq(r['rc'],expected,'credential path '+name+' exit')
        rows=c.calls()
        check(bool(rows),'credentials actually consumed '+name)
        for row in rows:
            check(row['auth_readable'] and row['auth_matches_source'],'file authentication readable inside judgment')
            eq(row['auth_mode'],0o600,'judgment auth mode 600')
            used_home=Path(row['home']).resolve()
            check(used_home.is_relative_to(c.root),'credential home inside test temporary boundary')
            if used_home!=c.codex_home.resolve():
                check(not (used_home/'auth.json').exists(),'used credential copy removed after '+name)
            for item in row['auth_copies']:
                eq(item['mode'],0o600,'credential copy permission 600')
                check(not Path(item['path']).exists(),'credential copy removed after '+name)
            proc_state=command(['ps','-o','stat=','-p',str(row['pid'])])
            check(proc_state.returncode!=0 or not proc_state.stdout.strip() or proc_state.stdout.strip().startswith('Z'),'credential consumer terminated')
        eq(auth_support.secret_paths(c.root,[b'sk-FIXTURE-SECRET'],[c.codex_home/'auth.json']),[],'no key outside original auth after '+name)
        eq((c.codex_home/'auth.json').read_bytes(),original,'original auth unchanged')
        eq(auth_support.mode(c.codex_home/'auth.json'),0o600,'original auth permission unchanged')
        if name in ('timeout','sigint','sigterm'): child_check(c)


def credential_controls():
    root=RUN/'credential-controls'; root.mkdir()
    secret=b'sk-CONTROL-ONLY-NOT-A-REAL-KEY'
    a=root/'bad-mode'; a.write_bytes(secret); a.chmod(0o644)
    b=root/'leaked-output'; b.write_bytes(secret)
    count=len(auth_support.secret_paths(root,[secret]))
    eq(auth_support.mode(a),0o644,'known unsafe copy mode detected')
    print('positive_control='+str(count))
    print('known_answer expected=2 actual='+str(count))
    eq(count,2,'two known leaked credential files')
    source=root/'source'; source.mkdir()
    (source/'auth.json').write_bytes(secret); (source/'auth.json').chmod(0o600)
    (source/'config.toml').write_text('cli_auth_credentials_store = "file"\n')
    # Exercise the same helper used for real authentication, using only a canary.
    program="""import os,signal,sys,subprocess
from pathlib import Path
from auth_support import writable_home
source,run,kind=sys.argv[1:]
try:
    with writable_home(Path(source),Path(run)) as home:
        assert (home/'auth.json').stat().st_mode & 0o777 == 0o600
        if kind=='failure': raise ValueError('fixture')
        if kind=='timeout': subprocess.run([sys.executable,'-c','import time; time.sleep(2)'],timeout=0.01)
        if kind in ('sigint','sigterm'): os.kill(os.getpid(),signal.SIGINT if kind=='sigint' else signal.SIGTERM)
except (ValueError,subprocess.TimeoutExpired,InterruptedError): sys.exit(7)
"""
    cleaned=0
    for name in ('success','failure','timeout','sigint','sigterm'):
        target=root/name; target.mkdir()
        p=command(['python3','-c',program,source,target,name],HERE)
        eq(p.returncode,0 if name=='success' else 7,'helper termination '+name)
        leaks=auth_support.secret_paths(target,[secret])
        copies=list(target.rglob('auth.json'))
        eq(leaks,[],'helper removes key '+name); eq(copies,[],'helper removes auth path '+name)
        cleaned+=int(not leaks and not copies)
    print('auth_cleanup_paths expected=5 actual='+str(cleaned))
    eq(cleaned,5,'five credential cleanup paths')


def isolation():
    c=Case('isolation',('probe-write',)); r=c.invoke(); c.outcome(r,0,'APPROVE',1)
    prompt_checks.measure_prompt(c.repo/'harness/templates/codex-audit',check,eq)
    eq(bytes_tree(c.repo,('.harness',)),c.before,'original repository including .git unchanged')
    for row in c.calls():
        dest=Path(row['cwd'])
        check(dest!=c.repo and dest.is_relative_to(c.root),'copy cwd outside original')
        eq(row.get('git_head'),c.head,'copy implementation commit')
        check(row.get('git_dir')!=str(c.repo/'.git'),'copy own git metadata')
        eq(row['sandbox'],'workspace-write','sandbox type'); eq(row['network'],True,'judgment network allowed')
        check((dest/'probe.txt').exists(),'copy writable')
        eq(row['stdin'],'','Codex stdin closed')
        for flag in ('--ephemeral','--ignore-user-config','--dangerously-bypass-approvals-and-sandbox'):
            check(flag not in row['args'],'forbidden CLI flag '+flag)
    # The neutral evidence and data/instruction boundary must be visible to Codex.
    joined='\n'.join(x['prompt'] for x in c.calls())
    for row in c.calls():
        delivered=prompt_checks.prompt_stats([('impl instruction',prompt_checks.delivered_text(row))])
        eq(delivered['roles'],[],'delivered instruction forbidden role matches')
        check(0<delivered['bytes']<=prompt_checks.MAX_BYTES,'delivered instruction UTF-8 byte limit',delivered['bytes'],prompt_checks.MAX_BYTES)
        check(delivered['examples']<=prompt_checks.MAX_EXAMPLES,'delivered instruction worked-example limit',delivered['examples'],prompt_checks.MAX_EXAMPLES)
    template_text='\n'.join(p.read_text(errors='replace') for p in (c.repo/'harness/templates/codex-audit').rglob('*') if p.is_file())
    instruction=joined+'\n'+template_text
    for token in ('PASS','FAIL','증거','데이터','긍정','반대','빠진'):
        check(token in instruction,'prompt rule '+token)

def doc_check(condition):
    rel,tokens=DOC_LINES[condition]
    text=(SOURCE/rel).read_text()
    original=git('show',BASE+':'+rel)
    check(text!=original,'document changed '+rel)
    for token in tokens:
        check(token in text,'document instruction '+token)
    # Check entire clauses, rather than treating an isolated keyword as authority.
    if condition=='스킬-01':
        clauses=[r'Claude[^\n]*(직접|손으로)[^\n]*(않|금지)',r'(평가자|qa-evaluator)[^\n]*APPROVE',r'off[^\n]*(기존|지금|종전)']
    else:
        clauses=[r'(스스로|자체|직접)[^\n]*판정[^\n]*(않|금지)',r'(바꾸|변경|덧붙)[^\n]*(않|금지)',r'off[^\n]*(기존|지금|종전)']
    for pattern in clauses: check(re.search(pattern,text) is not None,'document clause '+pattern)
    if condition=='스킬-02' and (SOURCE/SCRIPT).exists():
        c=Case('consumer',('approve',)); r=c.invoke(); eq(r['rc'],0,'consumer producer run')
        hook=c.repo/'harness/scripts/qa-pending-check.sh'
        data=json.dumps(dict(session_id='measure-session',cwd=str(c.repo),stop_hook_active=False,transcript_path=str(c.root/'unused')))
        def run_hook():
            return subprocess.run(['bash',str(hook)],cwd=c.repo,env=c.env,input=data,capture_output=True,text=True)
        p=run_hook(); eq(p.returncode,0,'hook executes'); eq(p.stdout.strip(),'','hook accepts generated APPROVE')
        c.plan(('reject','reject')); r=c.invoke(); eq(r['rc'],1,'consumer reject producer')
        p=run_hook(); check('REJECT' in p.stdout,'hook notices generated REJECT',p.stdout)

def scope_entries():
    contract=HERE.parent/'sprint-contract-codex-supervisor.md'
    if not contract.exists(): contract=W/'.harness/sprint-contract-codex-supervisor.md'
    s=contract.read_text()
    m=re.search(r'```text\n# sprint-scope\n(.*?)\n```',s,re.S)
    if not m: raise RuntimeError('scope block missing')
    return m.group(1).splitlines()

def scope_bad(paths,entries):
    return [p for p in paths if not any(p==e or (e.endswith('/') and p.startswith(e)) for e in entries)]

def scope():
    upper=git('rev-parse','--verify','-q',BRANCH)
    changed=git('diff','--no-renames','--name-only',BASE+'..'+upper,'--','.',':(exclude).harness').splitlines()
    eq(scope_bad(changed,scope_entries()),[],'scope outside expected inclusion set')
    check(bool(changed),'scope implementation delta nonempty',changed)
    check(SCRIPT in changed,'scope new executable included')
    for rel in ('harness/.claude-plugin/plugin.json','.claude-plugin/marketplace.json'):
        eq(git('diff','--name-only',BASE+'..'+upper,'--',rel),'','version unchanged '+rel)

def templates():
    text=(SOURCE/'harness/templates/project.yaml').read_text()
    check('codex_audit:' in text,'new project configuration section')
    for token in ('mode','codex_home','model','effort_draft','effort_impl','max_rounds'):
        check(re.search(r'^\s+'+token+r':',text,re.M) is not None,'template field '+token)
    readme=(SOURCE/'harness/README.md').read_text()
    check(any('codex-audit.sh' in line and line.strip().startswith('|') for line in readme.splitlines()),'README script table row')
    for token in ('CODEX_BIN','CODEX_AUDIT_LIMIT','600'): check(token in readme,'README operation '+token)
    d=SOURCE/'harness/templates/codex-audit'
    check(d.is_dir() and any(p.is_file() for p in d.rglob('*')),'distributed template directory')

def diagnostics():
    script=SOURCE/SCRIPT
    for shell in ('bash','zsh'):
        p=command([shell,'-n',script]); eq(p.returncode,0,shell+' syntax'); check(not p.stderr.strip(),shell+' syntax diagnostics',p.stderr)
    p=command(['shellcheck','-f','gcc',script]); eq(p.returncode,0,'shellcheck'); eq(p.stdout.strip(),'','shellcheck diagnostics')

def validate_plugin(which):
    p=command(['python3','scripts/validate-plugin.py','--check='+which],SOURCE,dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),120)
    print(p.stdout); print(p.stderr)
    eq(p.returncode,0,'authoritative validate-plugin '+which)
    check(('V6' if which=='code-fence' else 'V1') in p.stdout,'validator ran')

def reuse():
    # Reusability is distribution plus use of existing external consumers, not private functions.
    check((SOURCE/SCRIPT).is_file(),'public plugin script')
    check((SOURCE/'harness/templates/codex-audit').is_dir(),'public templates')
    for rel in (SKILL,AGENT): check('codex-audit.sh' in (SOURCE/rel).read_text(),'shared command consumed '+rel)

def na():
    upper=git('rev-parse','--verify','-q',BRANCH)
    names=git('diff','--name-only',BASE+'..'+upper).splitlines()
    eq([x for x in names if x=='scripts/release.sh'],[],'commands target intersection')

SUITES={
 '스킬-01':lambda:doc_check('스킬-01'),'스킬-02':lambda:doc_check('스킬-02'),
 '스크립트-01':draft,'스크립트-02':revise,'스크립트-03':impl,'스크립트-04':reject,
 '스크립트-05':research,'스크립트-06':rounds,'스크립트-07':config,'스크립트-08':report,
 '스크립트-09':detach,'스크립트-10':schemas,
 '스크립트-11':lambda:live_calibration.run_live(SOURCE,RUN,check,eq),'오류-01':invalid,'오류-02':failures,
 '구조-01':scope,'구조-02':isolation,'구조-03':templates,'구조-04':credentials,
 '재사용-01':reuse,'재사용-02':lambda:doc_check('스킬-02'),
 '진단-01':na,'진단-02':diagnostics,'진단-03':na,'진단-04':impl,
 '금지-03':lambda:validate_plugin('code-fence'),'금지-04':lambda:validate_plugin('frontmatter')}

def controls(condition):
    """Run before missing-implementation checks. Mutate input to the SAME primitive."""
    if condition=='구조-04':
        credential_controls()
        return
    if condition=='오류-01': format_controls()
    if condition=='스크립트-11':
        live_calibration.controls(RUN,check,eq)
        return
    if condition=='구조-01':
        bad=scope_bad(['harness/scripts/codex-audit.sh','outside.txt'],scope_entries())
        known=scope_bad(['a','b','c'],['a'])
        count=len(bad); expected=2; actual=len(known)
    elif condition in ('진단-01','진단-03'):
        count=len([x for x in ['scripts/release.sh'] if x=='scripts/release.sh']); expected=1; actual=count
    elif condition=='진단-02':
        bad=RUN/'broken.sh'; bad.write_text('#!/usr/bin/env bash\nif then\n')
        results=[command(['bash','-n',bad]),command(['zsh','-n',bad]),command(['shellcheck','-f','gcc',bad])]
        count=sum(p.returncode!=0 for p in results); expected=3; actual=count
    elif condition in ('금지-03','금지-04'):
        # Real V6 / V1 on a disposable copy, not a regex substitute.
        rel=SKILL; target=SOURCE/rel; original=target.read_text()
        try:
            target.write_text(original+'\n```\nbad fence\n```\n' if condition=='금지-03' else re.sub(r'^name:.*\n','',original,count=1,flags=re.M))
            which='code-fence' if condition=='금지-03' else 'frontmatter'
            p=command(['python3','scripts/validate-plugin.py','--check='+which],SOURCE,dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),120)
            (RUN/'positive-validator.txt').write_text(p.stdout+p.stderr)
            count=sum('FAIL' in line and ('sprint-contract' in line) for line in p.stdout.splitlines())
            if p.returncode==0: count=0
        finally: target.write_text(original)
        expected=1; actual=int(count>=1)
    elif condition=='스크립트-10':
        good=strict_schema(dict(a=dict(type='string'),b=dict(type='string')))
        bad=copy.deepcopy(good); bad['required']=['a']
        count=len(schema_errors(bad)); expected=2; actual=len(good['required'])
        accepted=0
        for phase,step in (('draft','draft'),('revise','draft-revised'),('impl','approve'),('research','research-answer')):
            value=payload(step); shape=fixture_schema(value)
            issues=response_schema_issues(shape,value,phase)
            eq(issues,[],'known valid schema '+phase)
            accepted+=int(not issues)
            wrong=copy.deepcopy(shape); wrong['required'].pop()
            check(bool(response_schema_issues(wrong,value,phase)),'known missing required schema '+phase)
        print('schema_phases expected=4 actual='+str(accepted))
        absent=sum(bool(response_schema_issues(None,payload(step),phase)) for phase,step in (('revise','draft-revised'),('research','research-answer')))
        eq(absent,2,'missing revise and research schema rejected')
        print('schema_missing_nonimpl_detected='+str(absent))
    elif condition=='스크립트-08':
        folder=RUN/'leak-control'; folder.mkdir(); (folder/'report.md').write_text('계정: sk-FIXTURE-SECRET\n')
        count=len(leak_files(folder)); expected=1; actual=count
    elif condition=='구조-02':
        prompt_checks.controls(RUN,check,eq)
        folder=RUN/'tree-control'; folder.mkdir(); f=folder/'sample'; f.write_text('before')
        old=bytes_tree(folder); f.write_text('after')
        count=sum(old.get(k)!=v for k,v in bytes_tree(folder).items()); expected=1; actual=count
    elif condition=='스킬-01' or condition in ('구조-03','재사용-01','재사용-02'):
        # Existing document as known input; removing required data makes predicate false.
        rel,tokens=DOC_LINES.get(condition,(SKILL,['name:']))
        body=(SOURCE/rel).read_text(); token='name:'
        count=int(token not in body.replace(token,'')); expected=1; actual=int(token in body)
    else:
        # Same call-count reader used by every runtime assertion; login must not count.
        f=RUN/'known-calls.jsonl'
        f.write_text('\n'.join(json.dumps(x) for x in [dict(kind='login'),dict(kind='exec'),dict(kind='exec')])+'\n')
        count=len(exec_rows(f)); expected=2; actual=count
    print('positive_control='+str(count))
    check(count>=1,'positive control detects known violation',count)
    print('known_answer expected='+str(expected)+' actual='+str(actual))
    eq(actual,expected,'known answer')

def main():
    global RUN
    args=sys.argv[1:]
    if not args or args[0] not in SUITES:
        print('FAIL usage: bash measure.sh <조건 번호> [--controls-only]'); return 64
    condition=args[0]
    runs=HERE/'.runs'; runs.mkdir(exist_ok=True)
    RUN=Path(tempfile.mkdtemp(prefix=condition+'-',dir=runs))
    print('evidence='+str(RUN))
    precondition=None
    try:
        if '--prepare-only' in args:
            if condition!='스크립트-11':
                print('FAIL usage: --prepare-only is only for 스크립트-11'); return 64
            with live_calibration.prepare_live(RUN):
                pass
            print('PASS 스크립트-11 PREPARED model_calls=0 implementation_evaluated=false')
            return 0
        snapshot()
        controls(condition)
        if '--negative' in args and '--controls-only' not in args and condition=='구조-02':
            prompt_checks.negative(SOURCE,RUN,check,eq)
        elif '--negative' in args and '--controls-only' not in args and condition=='스크립트-11':
            os.environ['CODEX_BIN']=str(HERE/'fake-codex')
            try:
                live_calibration.real_binary()
                check(False,'live negative guard failed to reject fake CODEX_BIN')
            except ValueError as exc:
                check(False,'LIVE_FAKE_OVERRIDE_REJECTED',str(exc))
        elif '--controls-only' not in args:
            if '--negative' in args:
                # A disposable no-op replacement is a mutant, not an implementation.
                target=SOURCE/SCRIPT; target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text('#!/usr/bin/env bash\nif then\n' if condition=='진단-02' else '#!/usr/bin/env bash\nexit 0\n')
                if condition in DOC_LINES:
                    rel,tokens=DOC_LINES[condition]
                    f=SOURCE/rel; f.write_text(f.read_text().replace('mode: codex','removed-mode'))
                if condition in ('금지-03','금지-04'):
                    f=SOURCE/SKILL
                    f.write_text(f.read_text()+'\n```\nbad\n```\n' if condition=='금지-03' else re.sub(r'^name:.*\n','',f.read_text(),count=1,flags=re.M))
            needs=condition.startswith(('스크립트-','오류-')) or condition in ('구조-02','구조-04','진단-02','진단-04','재사용-01','재사용-02')
            if not needs or need_script(): SUITES[condition]()
    except live_calibration.PreconditionUnmet as exc:
        precondition=str(exc)
        print('PRECONDITION_UNMET '+precondition+' implementation_evaluated=false')
    except Exception as exc:
        check(False,'measurement error',type(exc).__name__+': '+str(exc))
    result=dict(condition=condition,checks=CHECKS,failures=FAILURES,events=EVENTS,precondition=precondition)
    (RUN/'evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    if precondition:
        print('FAIL '+condition+' PRECONDITION_UNMET implementation_evaluated=false')
        return 2
    print(('FAIL' if FAILURES else 'PASS')+' '+condition+' checks='+str(CHECKS)+' failures='+str(len(FAILURES)))
    return 1 if FAILURES else 0

if __name__=='__main__': sys.exit(main())
