#!/usr/bin/env python3
"""시험 폴더에서 새 부모 세션 하나로 감독 6건을 차례로 요청한다. 진행 표시는 요청하지 않는다."""
import json, subprocess, sys, threading, time
from pathlib import Path
T = '/Users/jackson/Hub/10_Dev/codex-audit-ui-trial'
E = Path(sys.argv[1])
MESSAGES = [
    ('draft', 'direct', 'trial-a 계약을 Codex 로 써 줘. 요구사항은 .harness/.meta/trial-a/requirements.md'),
    ('revise', 'direct', 'trial-a 계약을 .harness/.meta/trial-a/critique.md 지적대로 Codex 에게 고치게 해 줘'),
    ('impl', 'direct', 'trial-a 구현을 Codex 로 판정해 줘. 기준 커밋은 9e400e3'),
    ('draft', 'delegated', 'trial-b 계약을 평가자(harness:qa-evaluator)에게 맡겨서 Codex 로 쓰게 해 줘. 요구사항은 .harness/.meta/trial-b/requirements.md'),
    ('revise', 'delegated', 'trial-b 계약을 평가자에게 맡겨서 .harness/.meta/trial-b/critique.md 지적대로 Codex 가 고치게 해 줘'),
    ('impl', 'delegated', 'trial-b 구현을 평가자에게 맡겨서 Codex 로 판정받아 줘. 기준 커밋은 9e400e3'),
]
TASKS = Path('/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-codex-audit-ui-trial')
STOP = threading.Event()


def watch_growth():
    # 부모가 띄운 백그라운드 작업 출력 파일의 크기를 2초마다 적는다. 카드가 감독 중에 자랐다는 관측 기록이다.
    sizes = {}
    with (E / 'growth.jsonl').open('a') as log:
        while not STOP.is_set():
            for path in TASKS.glob('*/tasks/*.output'):
                if path.is_symlink():
                    continue
                size = path.stat().st_size
                if sizes.get(path) != size:
                    sizes[path] = size
                    log.write(json.dumps(dict(at=time.time(), session=path.parent.parent.name, file=path.name, size=size)) + '\n')
                    log.flush()
            time.sleep(2)


threading.Thread(target=watch_growth, daemon=True).start()
session = None
for number, (verb, route, text) in enumerate(MESSAGES, 1):
    args = ['claude', '-p', text, '--output-format', 'stream-json', '--verbose', '--permission-mode', 'bypassPermissions']
    if session:
        args += ['--resume', session]
    out = E / 'stream-{}-{}-{}.jsonl'.format(number, verb, route)
    began = time.time()
    print('[{}] {} {}/{} 시작'.format(time.strftime('%H:%M:%S'), number, verb, route), flush=True)
    with out.open('w') as sink:
        proc = subprocess.run(args, cwd=T, stdin=subprocess.DEVNULL, stdout=sink, stderr=subprocess.STDOUT, timeout=1800)
    for line in out.read_text().splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        session = record.get('session_id') or session
    print('[{}] {} {}/{} 끝 · 종료 {} · {}초 · 세션 {}'.format(time.strftime('%H:%M:%S'), number, verb, route,
          proc.returncode, int(time.time() - began), session), flush=True)
STOP.set()
(E / 'session.txt').write_text(session + '\n')
