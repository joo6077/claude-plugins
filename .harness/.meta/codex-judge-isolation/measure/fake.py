#!/usr/bin/env python3
"""가짜 codex. 모델을 부르지 않는다. 호출마다 인자 · 환경 · 지시문 · 설정을 FAKE_STATE 에 남긴다."""
import json
import os
from pathlib import Path
import sys
import time
import uuid

STATE = Path(os.environ['FAKE_STATE'])
ARGS = sys.argv[1:]
IDS = ['스크립트-01', '스크립트-02']


def log(record):
    with (STATE / 'calls.jsonl').open('a', encoding='utf-8') as out:
        out.write(json.dumps(record, ensure_ascii=False) + '\n')


def event(kind, **fields):
    print(json.dumps(dict(type=kind, **fields), ensure_ascii=False), flush=True)


def option(*names):
    for index, arg in enumerate(ARGS[:-1]):
        if arg in names:
            return ARGS[index + 1]
    return ''


if Path(sys.argv[0]).name == 'npm':
    sys.exit(1)
if ARGS == ['--version']:
    print('codex-cli 9.9.9')
    sys.exit(0)
if ARGS[:2] == ['login', 'status']:
    print('Logged in using an API key', file=sys.stderr)
    sys.exit(0)
if ARGS[:1] == ['sandbox'] and '--help' in ARGS:
    log(dict(kind='sandbox-help'))
    if not (STATE / 'no-profile').exists():
        print('  -P, --permission-profile <NAME>')
    print('      --log-denials')
    sys.exit(0)
if not ARGS or ARGS[0] != 'exec':
    sys.exit(64)

counter = STATE / 'index'
number = int(counter.read_text()) if counter.exists() else 0
counter.write_text(str(number + 1))
plan = json.loads((STATE / 'plan.json').read_text())
step = plan[min(number, len(plan) - 1)]
home = Path(os.environ['CODEX_HOME'])
config = (home / 'config.toml').read_text() if (home / 'config.toml').is_file() else ''
model = option('-m', '--model')
if not model:
    for line in config.splitlines():
        if line.startswith('model') and '=' in line:
            model = line.split('=', 1)[1].strip().strip('"')
            break
(STATE / ('config-%d.toml' % number)).write_text(config)
log(dict(kind='exec', index=number, step=step, model=model, args=ARGS, cwd=option('-C', '--cd') or os.getcwd(), home=str(home),
         env={key: os.environ.get(key, '') for key in ('TMPDIR', 'TMP', 'TEMP')}))

thread = str(uuid.uuid4())
sessions = home / 'sessions' / time.strftime('%Y/%m/%d')
sessions.mkdir(parents=True, exist_ok=True)
(sessions / ('rollout-' + thread + '.jsonl')).write_text(
    json.dumps(dict(type='turn_context', payload=dict(model=model, effort='medium'))) + '\n')
event('thread.started', thread_id=thread)
event('turn.started')
if step == 'timeout':
    while True:
        time.sleep(1)
if step == 'hold':
    (STATE / ('holding-%d' % number)).touch()
    while not (STATE / ('release-%d' % number)).exists():
        time.sleep(.1)
if step == 'empty':
    event('turn.completed', usage={})
    sys.exit(0)

rows = [dict(id=item, evidence='fixture', analysis='fixture', verdict='PASS', fix=dict(where='', what='', verify=''))
        for item in IDS]
answer = dict(conditions=rows, verdict='APPROVE', questions=[])
if step == 'reject':
    rows[-1].update(verdict='FAIL', fix=dict(where='fixture.txt', what='fixture', verify='fixture'))
    answer['verdict'] = 'REJECT'
if step == 'research':
    answer.update(verdict='RESEARCH', questions=['fixture question?'])
if step == 'research-answer':
    answer = dict(answers=[dict(question='fixture question?', answer='fixture', sources=['https://example.invalid'])])
if step in ('draft', 'revise'):
    answer = dict(contract=(STATE / 'contract.txt').read_text(), measurements=[dict(path='fixture.txt', content='fixture')])
Path(option('-o', '--output-last-message')).write_text(json.dumps(answer, ensure_ascii=False))
event('item.completed', item=dict(id='answer', type='agent_message', text=json.dumps(answer, ensure_ascii=False)))
usage_file = STATE / 'usage.json'
usage = json.loads(usage_file.read_text()) if usage_file.exists() else dict(
    input_tokens=1000, cached_input_tokens=0, output_tokens=100)
event('turn.completed', usage=usage)
