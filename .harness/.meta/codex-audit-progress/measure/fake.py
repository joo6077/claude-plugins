#!/usr/bin/env python3
"""Protocol fixtures only. Never calls a model or a package registry."""
import datetime
import json
import os
from pathlib import Path
import sys
import time
import uuid

S = Path(os.environ['PROGRESS_STATE'])
A = sys.argv[1:]
def log(obj):
    with (S / 'calls.jsonl').open('a') as f:
        f.write(json.dumps(obj) + '\n')
def event(kind, **kw):
    print(json.dumps(dict(type=kind, **kw)), flush=True)
def option(*names):
    for i, arg in enumerate(A[:-1]):
        if arg in names:
            return A[i + 1]
    return ''
if Path(sys.argv[0]).name in ('osascript','terminal-notifier','notify-send','afplay'):
    log(dict(kind='forbidden-notification', args=A))
    sys.exit(0)
if Path(sys.argv[0]).name == 'npm':
    log(dict(kind='npm', args=A))
    if A != ['view', '@openai/codex', 'version']:
        print('wrong npm registry query', file=sys.stderr)
        sys.exit(64)
    spec = json.loads((S / 'discovery.json').read_text())
    if spec.get('npm_fail'):
        print('fixture registry unavailable', file=sys.stderr)
        sys.exit(1)
    print(spec['version'])
    sys.exit(0)
if A == ['--version']:
    print('codex-cli 1.2.3')
    sys.exit(0)
if A[:2] == ['login', 'status']:
    print('Logged in using an API key', file=sys.stderr)
    sys.exit(0)
if not A or A[0] != 'exec':
    sys.exit(64)
index = S / 'index'
n = int(index.read_text()) if index.exists() else 0
index.write_text(str(n + 1))
plan = json.loads((S / 'plan.json').read_text())
step = plan[min(n, len(plan) - 1)]
home = Path(os.environ['CODEX_HOME'])
model = option('-m', '--model') or 'fixture-supervisor'
thread = str(uuid.uuid4())
sessions = home / 'sessions' / datetime.datetime.now().strftime('%Y/%m/%d')
sessions.mkdir(parents=True, exist_ok=True)
rollout = sessions / ('rollout-' + thread + '.jsonl')
rollout.write_text(json.dumps(dict(type='turn_context', payload=dict(model=model, effort='medium', sandbox_policy=dict(type='workspace-write')))) + '\n')
decoy = sessions / ('rollout-' + str(uuid.uuid4()) + '.jsonl')
decoy.write_text('{}\n')
log(dict(kind='exec', index=n, step=step, model=model, args=A, thread=thread))
event('thread.started', thread_id=thread)
event('turn.started')
if step == 'timeout':
    time.sleep(180)
if step == 'quota':
    event('error', message='insufficient_quota fixture')
    sys.exit(1)
if step == 'empty':
    event('turn.completed')
    sys.exit(0)
event('item.started', item=dict(id='r', type='reasoning', text='private reasoning must not be printed'))
event('item.updated', item=dict(id='r', type='reasoning', text='private reasoning must not be printed'))
event('item.updated', item=dict(id='r', type='reasoning', text='private reasoning must not be printed'))
(S/'last-event-at').write_text(str(time.monotonic()))
gate = S / ('go-' + str(n))
while not gate.exists():
    if (S / 'grow').exists():
        with rollout.open('a') as f: f.write('{}\n')
    if (S / 'decoy-grow').exists():
        with decoy.open('a') as f: f.write('{}\n')
    time.sleep(.2)
if step in ('summary', 'summary-default'):
    stages = [('default', 'cat fixture.txt')] if step == 'summary-default' else [
        ('read', 'cat fixture.txt'), ('test', 'python3 -m unittest'),
        ('write', 'printf fixture > fixture.txt'), ('reason', None), ('answer', None)]
    for stage, cmd in stages:
        current = dict(id=stage, type='reasoning' if stage == 'reason' else 'agent_message', text='')
        if cmd:
            for i in range(40):
                current = dict(id=stage + '-' + str(i), type='command_execution', command=cmd, status='in_progress')
                event('item.started', item=current)
                event('item.updated', item=current)
                event('item.updated', item=current)
                if i < 39:
                    code = 7 if stage == 'default' and i == 0 else 0
                    if code: (S / 'error-at').write_text(str(time.monotonic()))
                    event('item.completed', item=dict(current, status='completed', exit_code=code))
        else:
            event('item.started', item=current)
        print('{broken fixture line', flush=True)
        event('fixture.unknown', harmless=True)
        (S / ('stage-' + stage)).touch()
        while not (S / ('next-' + stage)).exists():
            event('item.updated', item=current)
            time.sleep(.1)
        if cmd:
            code = 7 if stage == 'test' else 0
            if code: (S / 'error-at').write_text(str(time.monotonic()))
            completed = dict(type='item.completed', item=dict(current, status='completed', exit_code=code))
            raw = json.dumps(completed)
            sys.stdout.write(raw[:len(raw)//2]); sys.stdout.flush()
            time.sleep(.1)
            sys.stdout.write(raw[len(raw)//2:] + '\n'); sys.stdout.flush()
            event('item.completed', item=completed['item'])

if step in ('events', 'secret'):
    cmd = 'printf PROGRESS_COMMAND_SENTINEL'
    if step == 'secret':
        cmd += ' ' + json.loads((home / 'auth.json').read_text())['OPENAI_API_KEY']
    item = dict(id='cmd', type='command_execution', command=cmd, status='in_progress')
    event('item.started', item=item)
    event('item.updated', item=item)
    event('item.updated', item=item)
    print('{broken fixture line', flush=True)
    event('fixture.unknown', harmless=True)
    time.sleep(2.2)
    while not (S/'command-go').exists(): time.sleep(.05)
    item.update(status='completed', exit_code=7)
    raw = json.dumps(dict(type='item.completed', item=item))
    sys.stdout.write(raw[:len(raw)//2]); sys.stdout.flush()
    time.sleep(.2)
    sys.stdout.write(raw[len(raw)//2:] + '\n'); sys.stdout.flush()
ids = ['스크립트-01', '스크립트-02']
rows = [dict(id=i, evidence='fixture.txt: GOOD', analysis='fixture comparison', verdict='PASS', fix=dict(where='', what='', verify='')) for i in ids]
answer = dict(conditions=rows, verdict='APPROVE', questions=[])
if step == 'reject':
    rows[-1].update(verdict='FAIL', fix=dict(where='fixture.txt', what='use GOOD', verify='read fixture.txt'))
    answer['verdict'] = 'REJECT'
if step == 'research':
    answer.update(verdict='RESEARCH', questions=['fixture external fact?'])
if step == 'research-answer':
    answer = dict(answers=[dict(question='fixture external fact?', answer='fixture answer', sources=['https://example.invalid/fixture'])])
if step in ('draft', 'revise'):
    answer = dict(contract=(S / 'contract.txt').read_text(), measurements=[dict(path='fixture.txt', content='fixture')])
event('item.started', item=dict(id='answer', type='agent_message', text=''))
time.sleep(.4)
if step in ('events','secret'):
    while not (S/'answer-go').exists(): time.sleep(.05)
Path(option('-o', '--output-last-message')).write_text(json.dumps(answer, ensure_ascii=False))
event('item.completed', item=dict(id='answer', type='agent_message', text=json.dumps(answer)))
event('turn.completed', usage={})
