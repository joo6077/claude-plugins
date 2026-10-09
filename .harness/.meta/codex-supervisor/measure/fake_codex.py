import datetime
import hashlib
import stat
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

from fixtures import payload

args = sys.argv[1:]
state = Path(os.environ['MEASURE_STATE'])
state.mkdir(parents=True, exist_ok=True)
plan = json.loads((state / 'plan.json').read_text())
logfile = state / 'calls.jsonl'

def log(row):
    with logfile.open('a') as f: f.write(json.dumps(row, ensure_ascii=False) + '\n')

def option(*names):
    for n, arg in enumerate(args):
        if arg in names and n + 1 < len(args): return args[n + 1]
        for name in names:
            if arg.startswith(name + '='): return arg.split('=', 1)[1]
    return None

if args == ['--version']:
    print('codex-cli 0.157.1 (fixture)'); sys.exit(0)
if args[:2] == ['login', 'status']:
    log(dict(kind='login', args=args))
    if plan.get('login') is False:
        print('Not logged in', file=sys.stderr); sys.exit(1)
    print('Logged in using an API key - sk-FIXTURE-SECRET', file=sys.stderr)
    sys.exit(0)
if not args or args[0] != 'exec':
    print('unsupported fake invocation', args, file=sys.stderr); sys.exit(64)

index_file = state / 'index'
index = int(index_file.read_text()) if index_file.exists() else 0
index_file.write_text(str(index + 1))
steps = plan['steps']
spec = steps[min(index, len(steps) - 1)]
step = spec['fault'] if isinstance(spec,dict) else spec
home = Path(os.environ['CODEX_HOME'])
home.mkdir(parents=True, exist_ok=True)
configs = '\n'.join(args[n + 1] for n, a in enumerate(args[:-1]) if a in ('-c', '--config'))
folder_config = (home / 'config.toml').read_text() if (home / 'config.toml').exists() else ''
model = option('-m', '--model')
if not model:
    found = re.findall(r'(?:^|\n)model\s*=\s*[\"\']([^\"\']+)', configs + '\n' + folder_config)
    model = found[0] if found else 'fixture-unconfigured'
effort = re.findall(r'model_reasoning_effort\s*=\s*[\"\']?([a-z]+)', configs)
effort = effort[0] if effort else 'medium'
directory = Path(option('-C', '--cd') or os.getcwd()).resolve()
schema_file = option('--output-schema')
output_file = option('-o', '--output-last-message')
stdin = sys.stdin.read()
prompt = '\n'.join(args) + '\n' + stdin
thread = str(uuid.uuid4())
network = bool(re.search(r'sandbox_workspace_write.network_access\s*=\s*true', configs))
sandbox = option('-s', '--sandbox') or 'unspecified'
schema = json.loads(Path(schema_file).read_text()) if schema_file else None
row = dict(kind='exec', index=index, step=step, response=spec.get('response') if isinstance(spec,dict) else None, args=args, stdin=stdin, prompt=prompt,
           home=str(home), cwd=str(directory), model=model, effort=effort, network=network,
           sandbox=sandbox, schema=schema, output=output_file, thread_id=thread, pid=os.getpid())
if directory.exists():
    p = subprocess.run(['git', '-C', str(directory), 'rev-parse', '--show-toplevel'],
                       capture_output=True, text=True)
    row['git_root'] = p.stdout.strip() if p.returncode == 0 else None
    if p.returncode == 0:
        row['git_head'] = subprocess.check_output(['git', '-C', str(directory), 'rev-parse', 'HEAD'], text=True).strip()
        row['git_dir'] = subprocess.check_output(['git', '-C', str(directory), 'rev-parse', '--absolute-git-dir'], text=True).strip()
# Observe credentials without recording even the fixture key bytes.
auth=home/'auth.json'
origin=Path(os.environ.get('MEASURE_AUTH_SOURCE',str(auth)))
row['auth_readable']=auth.is_file()
row['auth_mode']=stat.S_IMODE(auth.stat().st_mode) if auth.is_file() else None
row['auth_matches_source']=auth.is_file() and origin.is_file() and auth.read_bytes()==origin.read_bytes()
row['config_bytes_sha256']=hashlib.sha256(folder_config.encode()).hexdigest()
row['auth_copies']=[]
case_root=os.environ.get('MEASURE_CASE_ROOT')
if case_root and origin.is_file():
    key=json.loads(origin.read_text()).get('OPENAI_API_KEY','').encode()
    for candidate in Path(case_root).rglob('*'):
        if candidate.is_file() and candidate!=origin and key and key in candidate.read_bytes():
            row['auth_copies'].append(dict(path=str(candidate),mode=stat.S_IMODE(candidate.stat().st_mode)))
log(row)
session_dir = home / 'sessions' / datetime.datetime.now().strftime('%Y/%m/%d')
session_dir.mkdir(parents=True, exist_ok=True)
session = session_dir / ('rollout-' + thread + '.jsonl')
session.write_text(json.dumps(dict(type='turn_context', payload=dict(model=model + '-observed',
                   effort=effort, sandbox_policy=dict(type=sandbox, network_access=network)))) + '\n')
# A newer unrelated session detects "latest file" instead of thread_id matching.
(session_dir / ('rollout-decoy-' + str(uuid.uuid4()) + '.jsonl')).write_text(
    json.dumps(dict(type='turn_context', payload=dict(model='WRONG-DECOY', effort='high', sandbox_policy=dict(type='danger-full-access')))) + '\n')
print(json.dumps(dict(type='thread.started', thread_id=thread)), flush=True)

if step in ('timeout','hold'):
    child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])
    with (state / 'children').open('a') as f: f.write(str(child.pid) + '\n')
    time.sleep(120)
if step == 'slow': time.sleep(3)
elif plan.get('delay'): time.sleep(plan['delay'])
if step in ('quota', 'config-error'):
    print(json.dumps(dict(type='error', message='insufficient_quota usage limit' if step == 'quota' else 'invalid configuration')), flush=True)
    sys.exit(1)
if step == 'empty':
    print(json.dumps(dict(type='turn.completed')), flush=True); sys.exit(0)
if step == 'probe-write':
    (directory / 'probe.txt').write_text('copy only')
kind = 'approve' if step in ('slow', 'probe-write', 'nonzero', 'no-completed', 'turn-failed', 'event-error', 'malformed', 'missing-file') else step
if isinstance(spec,dict): kind=spec['response']
result = payload(kind)
if step=='missing-required': result.pop(spec['field'])
if output_file and step != 'missing-file':
    dest = Path(output_file)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text('{bad json' if step == 'malformed' else json.dumps(result, ensure_ascii=False))
print(json.dumps(dict(type='item.completed', item=dict(type='agent_message', text=json.dumps(result, ensure_ascii=False)))), flush=True)
if step in ('turn-failed', 'event-error'):
    print(json.dumps(dict(type='turn.failed' if step == 'turn-failed' else 'error', message='fixture protocol failure')), flush=True)
if step != 'no-completed': print(json.dumps(dict(type='turn.completed', usage={})), flush=True)
sys.exit(9 if step == 'nonzero' else 0)
