#!/usr/bin/env python3
"""가짜 codex. 모델을 부르지 않는다. 호출마다 인자 · 환경 · 지시문 · 설정을 FAKE_STATE 에 남긴다."""
import json
import subprocess
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
    login_home = Path(os.environ.get('CODEX_HOME', ''))
    log(dict(kind='login', home=str(login_home)))
    if (STATE / 'login-fail').exists():
        print('Not logged in', file=sys.stderr)
        sys.exit(1)
    try:
        login_auth = json.loads((login_home / 'auth.json').read_text())
    except (OSError, ValueError):
        login_auth = {}
    mode = login_auth.get('auth_mode')
    if mode == 'chatgpt' and (STATE / 'login-refresh').exists():
        login_auth.setdefault('tokens', {})['access_token'] = 'login-refreshed-%d' % os.getpid()
        (login_home / 'auth.json').write_text(json.dumps(login_auth))
        log(dict(kind='login-refresh', token=login_auth['tokens']['access_token']))
    print('Logged in using ChatGPT' if mode == 'chatgpt' else 'Logged in using an API key', file=sys.stderr)
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
profile = option('-p', '--profile')
if profile and (home / (profile + '.config.toml')).is_file():
    (STATE / ('profile-%d.toml' % number)).write_text((home / (profile + '.config.toml')).read_text())
auth_path = home / 'auth.json'
try:
    auth = json.loads(auth_path.read_text())
except (OSError, ValueError):
    auth = {}
token = ''
if auth.get('auth_mode') == 'chatgpt' and not (STATE / 'no-refresh').exists():
    token = 'refreshed-%d-%d' % (number, os.getpid())


def refresh():
    # 진짜 codex 는 아무 때나 갱신한다. hold-late 는 풀린 뒤에 써서 두 감독의 쓰는 순서를 측정이 정한다.
    if step == 'corrupt':
        auth_path.write_text('{')
    elif token:
        auth.setdefault('tokens', {})['access_token'] = token
        auth_path.write_text(json.dumps(auth))


if not step.startswith('hold-late'):
    refresh()
# 진짜 codex 가 자기 폴더에 남기는 부산물 (0.160 실측 이름)
for junk in ('memories_1.sqlite', 'logs_2.sqlite', 'state_5.sqlite', 'thread_history_1.sqlite'):
    (home / junk).write_bytes(b'fixture')
(home / 'shell_snapshots').mkdir(exist_ok=True)
(home / 'shell_snapshots' / ('snap-%d.sh' % number)).write_text('fixture')
log(dict(kind='exec', index=number, step=step, token=token, pid=os.getpid(), model=model, args=ARGS, cwd=option('-C', '--cd') or os.getcwd(), home=str(home),
         env={key: os.environ.get(key, '') for key in ('TMPDIR', 'TMP', 'TEMP', 'PATH')}))

thread = str(uuid.uuid4())
sessions = home / 'sessions' / time.strftime('%Y/%m/%d')
sessions.mkdir(parents=True, exist_ok=True)
(sessions / ('rollout-' + thread + '.jsonl')).write_text(
    json.dumps(dict(type='turn_context', payload=dict(model=model, effort='medium'))) + '\n')
if not step.startswith('nothread'):
    event('thread.started', thread_id=thread)
event('turn.started')
if step == 'timeout':
    while True:
        time.sleep(1)
if step.startswith('hold'):
    (STATE / ('holding-%d' % number)).touch()
    while not (STATE / ('release-%d' % number)).exists():
        time.sleep(.1)
    if step.startswith('hold-late'):
        refresh()
    if step == 'hold-late-orphan':
        # 표준 출력을 쥔 손자를 따로 띄운다 — 감독의 출력 복사 스레드가 끝나지 않은 채 되돌려 쓰기에 들어간다.
        orphan = subprocess.Popen(['sleep', '30'], stdout=sys.stdout, start_new_session=True)
        (STATE / 'orphan.pid').write_text(str(orphan.pid))
if step == 'empty':
    event('turn.completed', usage={})
    sys.exit(0)

rows = [dict(id=item, evidence='fixture', analysis='fixture', verdict='PASS', fix=dict(where='', what='', verify=''))
        for item in IDS]
answer = dict(conditions=rows, verdict='APPROVE', questions=[])
if step in ('reject', 'hold-reject'):
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
