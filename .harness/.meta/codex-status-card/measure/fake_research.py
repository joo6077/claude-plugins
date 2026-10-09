#!/usr/bin/env python3
"""리서치 실행기용 가짜 codex. 실제 codex 처럼 빈칸 없는 JSON 한 줄씩 낸다. 차례를 열고 세션 기록에 사용량을 남긴 뒤 release 표식을 기다려 답을 쓴다."""
import json
from functools import partial
import os
from pathlib import Path
import sys
import time
import uuid

STATE = Path(os.environ['FAKE_STATE'])
ARGS = sys.argv[1:]
dumps = partial(json.dumps, separators=(',', ':'), ensure_ascii=False)
if not ARGS or ARGS[0] != 'exec':
    sys.exit(64)
out = Path(ARGS[ARGS.index('-o') + 1])
thread = str(uuid.uuid4())
sessions = Path(os.environ['CODEX_SESS_DIR']) / time.strftime('%Y/%m/%d')
sessions.mkdir(parents=True, exist_ok=True)
limits = dict(primary=dict(used_percent=12.0, window_minutes=300, resets_at=int(time.time()) + 3600),
              secondary=dict(used_percent=3.0, window_minutes=10080, resets_at=int(time.time()) + 86400))
rollout = sessions / ('rollout-fixture-' + thread + '.jsonl')
rollout.write_text(dumps(dict(type='session_meta', payload=dict(id=thread))) + '\n')
(STATE / 'research-pid').write_text(str(os.getpid()))
print(dumps(dict(type='thread.started', thread_id=thread)), flush=True)
print(dumps(dict(type='turn.started')), flush=True)
# 미끼: 이 차례와 상관없는 더 새 세션 기록. 「가장 최근 파일」 로 짐작하는 구현을 가려낸다.
decoy = sessions / 'rollout-decoy-other-thread.jsonl'
decoy.write_text(dumps(dict(type='event_msg', payload=dict(type='token_count', info=None, rate_limits=dict(
    primary=dict(used_percent=50.0, window_minutes=300, resets_at=int(time.time()) + 3600),
    secondary=dict(used_percent=40.0, window_minutes=10080, resets_at=int(time.time()) + 86400))))) + '\n')
os.utime(decoy, (time.time() + 60, time.time() + 60))
(STATE / 'holding').touch()
while not (STATE / 'release').exists():
    time.sleep(.2)
    with rollout.open('a') as grow:
        grow.write(dumps(dict(type='event_msg', payload=dict(type='token_count', info=None, rate_limits=limits))) + '\n')
out.write_text('조사 결과: fixture 근거 https://example.invalid 를 확인했다.\n')
print(dumps(dict(type='turn.completed', usage=dict(input_tokens=10, cached_input_tokens=0, output_tokens=5))), flush=True)
