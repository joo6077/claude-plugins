"""Paid integration measurement. Only the normal 스크립트-11 dispatch calls run_live.

File authentication and unchanged settings are copied to a private writable home.
Only the credential copy is removed on completion, error or catchable signal.
"""
from contextlib import contextmanager
import auth_support
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import time
import tomllib

SCRIPT='harness/scripts/codex-audit.sh'
REPORT_ROW=re.compile(r'^- 차례 (?P<phase>.+?) 모델=(?P<model>\S+) 생각=(?P<effort>\S+) 격리=(?P<sandbox>\S+) 기록=(?P<record>.+?)\s*$',re.M)
LIVE_CONTRACT='''---
feature: "감독관 알려진 답"
created: "2026-10-01 00:00"
complexity: "단순"
conditions: 1
slug: sample
status: active
---
# 감독관 알려진 답
## Script
- [ ] 스크립트-01: sample.txt의 바이트가 GOOD과 줄바꿈 하나이다 (측정: python3 -c 'from pathlib import Path; import sys; sys.exit(0 if Path("sample.txt").read_bytes()==b"GOOD\\n" else 1)') [exact]
'''

def native_binary(candidate):
    f=Path(candidate).resolve()
    if not f.is_file(): return False
    with f.open('rb') as stream: magic=stream.read(4)
    return magic in (b'\x7fELF',b'\xcf\xfa\xed\xfe',b'\xce\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xca\xfe\xba\xbe') and os.access(f,os.X_OK)

def real_binary():
    # Nested supervisors may export the installed default binary. Reject every
    # different override; a renamed fake cannot satisfy the resolved-path check.
    found=shutil.which('codex')
    if not found: raise ValueError('LIVE_MISSING_CODEX')
    executable=Path(found).resolve()
    def verified(native):
        override=os.environ.get('CODEX_BIN')
        if override:
            candidate=Path(shutil.which(override) or override).resolve()
            if candidate not in (executable,native.resolve()):
                raise ValueError('LIVE_REJECTS_CODEX_BIN_OVERRIDE')
        return native
    if native_binary(executable): return verified(executable)
    # The locally inspected official npm launcher resolves one platform-native file.
    package=executable.parent.parent
    manifest=package/'package.json'
    if not manifest.is_file() or json.loads(manifest.read_text()).get('name')!='@openai/codex':
        raise ValueError('LIVE_REJECTS_NON_NATIVE_OR_UNRECOGNIZED_LAUNCHER')
    machine=platform.machine().lower()
    arch='arm64' if machine in ('arm64','aarch64') else 'x64'
    osname='darwin' if platform.system()=='Darwin' else 'linux'
    triple=('aarch64' if arch=='arm64' else 'x86_64')+('-apple-darwin' if osname=='darwin' else '-unknown-linux-musl')
    pkg='codex-'+osname+'-'+arch
    candidates=[package/'node_modules/@openai'/pkg/'vendor'/triple/'bin/codex',
                package.parent/pkg/'vendor'/triple/'bin/codex',package/'vendor'/triple/'bin/codex']
    for f in candidates:
        if native_binary(f): return verified(f.resolve())
    raise ValueError('LIVE_MISSING_NATIVE_CODEX: '+str(package))

def matches_context(row,record):
    return record.get('type')=='turn_context' and record.get('payload',{}).get('model')==row['model'] and record['payload'].get('effort')==row['effort']

def known_exit(content): return 0 if content==b'GOOD\n' else 1

def controls(run,check,eq):
    fixture=run/'live-known'; fixture.mkdir()
    env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
    for args in (['init','-q'],['config','user.name','measure'],['config','user.email','measure@example.invalid']):
        p=subprocess.run(['git',*args],cwd=fixture,env=env,capture_output=True,text=True)
        eq(p.returncode,0,'live known git preparation')
    bad_rc=None
    for content,expected in ((b'GOOD\n',0),(b'BAD\n',1)):
        (fixture/'sample.txt').write_bytes(content)
        for args in (['add','sample.txt'],['commit','-qm','known fixture']):
            p=subprocess.run(['git',*args],cwd=fixture,env=env,capture_output=True,text=True)
            eq(p.returncode,0,'live known git commit')
        p=subprocess.run(['python3','-c','from pathlib import Path; import sys; sys.exit(0 if Path("sample.txt").read_bytes()==b"GOOD\\n" else 1)'],cwd=fixture,env=env)
        eq(p.returncode,expected,'known implementation measurement exit')
        bad_rc=p.returncode
    fake=run/'fake-native'; fake.write_text('#!/usr/bin/env python3\nprint("APPROVE")\n'); fake.chmod(0o700)
    rejected=int(not native_binary(fake))
    print('live_fake_rejected='+str(rejected)); eq(rejected,1,'fake executable cannot be native Codex')
    row=dict(model='known-model',effort='medium')
    record=dict(type='turn_context',payload=dict(model='known-model',effort='medium'))
    eq(int(matches_context(row,record)),1,'known matching session context')
    record['payload']['effort']='low'
    eq(int(matches_context(row,record)),0,'mismatching session effort rejected')
    print('positive_control='+str(rejected))
    print('known_answer expected=1 actual='+str(bad_rc))

class PreconditionUnmet(RuntimeError):
    """The environment cannot be measured; this is not an implementation defect."""


def default_supervisor_home():
    qa=Path.home()/'.codex-qa'
    return (qa if qa.is_dir() else Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex'))).expanduser()).resolve()


@contextmanager
def prepare_live(run):
    """File login in source and writable copy; no model request."""
    did_yield=False
    try:
        executable=real_binary()
        audit_home=default_supervisor_home()
        config=audit_home/'config.toml'
        if not config.is_file(): raise ValueError('LIVE_DEFAULT_CONFIG_MISSING: '+str(config))
        parsed=tomllib.loads(config.read_text())
        if not parsed.get('model'): raise ValueError('LIVE_DEFAULT_MODEL_MISSING')
        if parsed.get('model_provider','openai')!='openai' or parsed.get('model_providers'):
            raise ValueError('LIVE_CUSTOM_PROVIDER_NOT_ALLOWED')
        if any(os.environ.get(k) for k in ('OPENAI_BASE_URL','OPENAI_API_BASE','CODEX_API_BASE_URL','CODEX_OSS_BASE_URL')):
            raise ValueError('LIVE_CUSTOM_API_ENDPOINT_NOT_ALLOWED')
        auth=audit_home/'auth.json'
        if parsed.get('cli_auth_credentials_store')!='file':
            raise ValueError('LIVE_REQUIRES_FILE_AUTH_STORE')
        if not auth.is_file() or auth_support.mode(auth)!=0o600:
            raise ValueError('LIVE_REQUIRES_AUTH_FILE_MODE_600')
        # Parse without logging values. A real API-key login must be present.
        credentials=json.loads(auth.read_text())
        if not credentials.get('OPENAI_API_KEY'):
            raise ValueError('LIVE_REQUIRES_FILE_API_KEY')
        secret=credentials['OPENAI_API_KEY'].encode()
        original_auth=auth.read_bytes()
        original_config=config.read_bytes()
        env=dict(os.environ,CODEX_HOME=str(audit_home),CODEX_BIN=str(executable),TMPDIR=str(run),
                 PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
        for name in ('MEASURE_STATE','CODEX_AUDIT_LIMIT','GIT_DIR','GIT_WORK_TREE','HARNESS_CONTRACT','CLAUDE_CODE_SESSION_ID','OPENAI_API_KEY','CODEX_API_KEY'):
            env.pop(name,None)
        cmd=[str(executable),'login','status']
        observations=[]
        def login(home,label):
            selected=dict(env,CODEX_HOME=str(home))
            p=subprocess.run(cmd,env=selected,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=30)
            lines=(p.stdout+'\n'+p.stderr).splitlines()
            logged=p.returncode==0 and any(line.startswith('Logged in') for line in lines)
            status='Logged in' if logged else 'Not logged in'
            if logged and any(line.startswith('Logged in using an API key') for line in lines):
                status='Logged in using an API key'
            observations.append(dict(stage=label,codex_home=str(home),login_status=status,login_exit=p.returncode))
            print('stage='+label+' CODEX_HOME='+str(home))
            print('login_status='+status+' login_exit='+str(p.returncode)+' model_calls=0')
            if not logged: raise PreconditionUnmet('측정 전제 불성립: '+label+' 파일 로그인 확인 불가')
        copied=None
        try:
            login(audit_home,'source')
            with auth_support.writable_home(audit_home,run) as copied:
                login(copied,'writable-copy')
                print('auth_copy_mode=600')
                did_yield=True
                yield dict(executable=executable,audit_home=copied,source_home=audit_home,
                           config=copied/'config.toml',secret=secret,env=dict(env,CODEX_HOME=str(copied)))
        finally:
            removed=copied is None or not (copied/'auth.json').exists()
            unchanged=auth.read_bytes()==original_auth and config.read_bytes()==original_config
            leaks=auth_support.secret_paths(run,[secret])
            evidence=dict(command=cmd,observations=observations,auth_copy_removed=removed,
                          source_unchanged=unchanged,leak_count=len(leaks),model_calls_during_preparation=0)
            (run/'live-preparation.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
            print('auth_copy_removed='+str(removed).lower()+' source_unchanged='+str(unchanged).lower()+' secret_leaks='+str(len(leaks)))
            if not removed or not unchanged or leaks:
                raise RuntimeError('live authentication cleanup or secret containment failed')

    except (ValueError,OSError,subprocess.TimeoutExpired) as exc:
        if did_yield: raise
        raise PreconditionUnmet('측정 전제 불성립: '+str(exc)) from exc


def run_live(source,run,check,eq):
    if os.environ.get('MEASURE_NO_LIVE')=='1': raise PreconditionUnmet('LIVE_DISABLED_IN_DRAFT_VERIFY')
    with prepare_live(run) as prepared:
        measure_live(source,run,check,eq,prepared)


def measure_live(source,run,check,eq,prepared):
    executable=prepared['executable']; audit_home=prepared['audit_home']; config=prepared['config']; env=prepared['env']
    config_digest=hashlib.sha256(config.read_bytes()).hexdigest()
    manifest=dict(binary=str(executable),binary_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(),
                  settings_source=str(config),settings_sha256=config_digest,codex_home=str(audit_home))
    (run/'live-provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

    def git(repo,*args):
        p=subprocess.run(['git',*args],cwd=repo,env=env,text=True,capture_output=True)
        if p.returncode: raise RuntimeError('live fixture git: '+p.stderr)
        return p.stdout.strip()

    for label,content,expected_rc,verdict,phase_count in (
        ('good',b'GOOD\n',0,'APPROVE',1),('bad',b'BAD\n',1,'REJECT',2)):
        repo=run/('live-'+label); repo.mkdir()
        shutil.copytree(source/'harness',repo/'harness')
        meta=repo/'.harness'; meta.mkdir()
        (meta/'project.yaml').write_text('contract_categories:\n  - id: Script\n    prefix: 스크립트\ncodex_audit:\n  codex_home: '+json.dumps(str(audit_home))+'\n')
        contract=meta/'sprint-contract-sample.md'; contract.write_text(LIVE_CONTRACT)
        git(repo,'init','-q'); git(repo,'config','user.name','measure'); git(repo,'config','user.email','measure@example.invalid')
        git(repo,'add','.'); git(repo,'commit','-qm','known baseline')
        base=git(repo,'rev-parse','HEAD')
        (repo/'sample.txt').write_bytes(content)
        git(repo,'add','sample.txt'); git(repo,'commit','-qm','calibration input')
        # No answer/verdict is passed to the supervisor beyond the one-condition contract.
        command=['bash',str(repo/SCRIPT),'impl',str(contract),base]
        existing_sessions={f.resolve() for f in run.rglob('*.jsonl')}
        started=time.time_ns()
        print('LIVE_CODEX cost phase='+label,flush=True)
        with (run/(label+'-stdout.txt')).open('w') as out,(run/(label+'-stderr.txt')).open('w') as err:
            proc=subprocess.Popen(command,cwd=repo,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
            try: rc=proc.wait(timeout=1900)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGTERM)
                try: proc.wait(timeout=5)
                except subprocess.TimeoutExpired: os.killpg(proc.pid,signal.SIGKILL); proc.wait()
                rc=124
            finally:
                if proc.poll() is None:
                    os.killpg(proc.pid,signal.SIGTERM)
                    try: proc.wait(timeout=5)
                    except subprocess.TimeoutExpired: os.killpg(proc.pid,signal.SIGKILL); proc.wait()
        eq(rc,expected_rc,'live '+label+' impl exit')
        reports=list((meta/'codex-audit/sample').rglob('report.md'))
        eq(len(reports),1,'live '+label+' report count')
        if len(reports)!=1: continue
        report=reports[0].read_text()
        check(report.rstrip().endswith('감독 판정: '+verdict),'live '+label+' verdict',report[-100:])
        feedback=meta/'sprint-feedback-sample.md'
        check(feedback.is_file() and re.search(r'^Verdict: '+verdict+r'\s*$',feedback.read_text(),re.M) is not None,'live feedback agrees')
        rows=[m.groupdict() for m in REPORT_ROW.finditer(report)]
        eq(len(rows),phase_count,'live '+label+' phase count')
        # Find thread.started in the actual supervisor's saved --json stream, not in a mock log.
        thread_ids=set()
        for f in (meta/'codex-audit').rglob('*'):
            if not f.is_file() or f.stat().st_size>20_000_000: continue
            for line in f.read_text(errors='replace').splitlines():
                try: event=json.loads(line)
                except ValueError: continue
                if isinstance(event,dict) and event.get('type')=='thread.started': thread_ids.add(event.get('thread_id'))
        seen=set()
        for row in rows:
            record_path=Path(row['record']).expanduser().resolve()
            inside=record_path.is_relative_to(run) and 'sessions' in record_path.parts
            check(inside and record_path.is_file(),'live original session exists under writable run',str(record_path))
            if not inside or not record_path.is_file(): continue
            stats=record_path.stat()
            born=getattr(stats,'st_birthtime_ns',int(getattr(stats,'st_birthtime',stats.st_mtime)*1_000_000_000))
            check(record_path not in existing_sessions and born>=started and stats.st_mtime_ns>=started,'live session created after invocation')
            records=[json.loads(x) for x in record_path.read_text().splitlines() if x.strip()]
            sessions=[r['payload'].get('id') for r in records if r.get('type')=='session_meta']
            check(len(sessions)==1 and sessions[0] in thread_ids and record_path.stem.endswith(sessions[0]),'live thread/event/session linkage',sessions)
            seen.update(sessions)
            contexts=[r for r in records if r.get('type')=='turn_context']
            check(bool(contexts) and all(matches_context(row,r) for r in contexts),'live report equals turn_context model/effort',dict(model=row['model'],effort=row['effort']))
            check(any(r.get('type')=='response_item' and r.get('payload',{}).get('role')=='assistant' for r in records),'live session contains actual assistant response')
        eq(len(seen),phase_count,'live distinct fresh sessions')
        if label=='bad':
            fix=re.search(r'^- 스크립트-01 어디를: (.+?) · 무엇으로: (.+?) · 어떻게 확인: (.+?)\s*$',report,re.M)
            check('## 고칠 것' in report and fix is not None and all(x.strip() for x in fix.groups()),'live bad fix has three nonempty cells')
    eq(hashlib.sha256(config.read_bytes()).hexdigest(),config_digest,'default settings unchanged')
