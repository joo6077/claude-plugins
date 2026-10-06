#!/usr/bin/env python3
"""Harmless premeasurement command: canary output, clone observation, heartbeat."""
import json,os,subprocess,sys,time
from pathlib import Path
ident=sys.argv[1]
trace=Path(os.environ['QA_AMEND_TRACE'])
mode=os.environ.get('QA_AMEND_MODE','success')
def git(*args):
    return subprocess.check_output(['git',*args],text=True).strip()
row=dict(id=ident,started=time.monotonic(),cwd=str(Path.cwd()),head=git('rev-parse','HEAD'),git_dir=git('rev-parse','--absolute-git-dir'),in_codex=os.environ.get('QA_AMEND_IN_CODEX')=='1')
with trace.open('a') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
Path('premeasure-probe.txt').write_text('copy write')
print('BEGIN '+ident,flush=True)
if mode=='secret':
    print('sk-FIXTURE-SECRET',flush=True)
    print('stderr sk-FIXTURE-SECRET',file=sys.stderr,flush=True)
if mode=='timeout' and ident=='스크립트-01':
    beat=trace.parent/'heartbeat'
    child=subprocess.Popen([sys.executable,'-c','import sys,time; from pathlib import Path; p=Path(sys.argv[1]);\nwhile True: p.write_text(str(time.time_ns())); time.sleep(0.05)',str(beat)])
    (trace.parent/'child.pid').write_text(str(child.pid))
    time.sleep(30)
print('END '+ident,flush=True)
if mode=='nonzero': sys.exit(7)
