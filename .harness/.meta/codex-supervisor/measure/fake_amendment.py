#!/usr/bin/env python3
"""Observe frozen inputs before delegating to the unchanged fake Codex."""
import hashlib,json,os,runpy,sys
from pathlib import Path
import fixtures
args=sys.argv[1:]
if args and args[0]=='exec':
    root=Path(os.environ['MEASURE_CASE_ROOT'])
    state=Path(os.environ['MEASURE_STATE'])
    prompt='\n'.join(args)
    bundles=[]
    for f in (root/'repo with space/.harness/codex-audit').rglob('MANIFEST.json'):
        files={str(p.relative_to(f.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in f.parent.rglob('*') if p.is_file()}
        bundles.append(dict(path=str(f),referenced=str(f) in prompt,manifest=json.loads(f.read_text()),hashes=files))
    trace=Path(os.environ['QA_AMEND_TRACE'])
    observed=dict(prompt=prompt,bundles=bundles,trace=[json.loads(x) for x in trace.read_text().splitlines()] if trace.exists() else [])
    with (state/'amend-observations.jsonl').open('a') as f: f.write(json.dumps(observed,ensure_ascii=False)+'\n')
    os.environ['QA_AMEND_IN_CODEX']='1'
extra=os.environ.get('QA_AMEND_EXTRA_ID')
original=fixtures.payload
if extra:
    def payload(kind):
        value=original(kind)
        if 'conditions' in value:
            value['conditions'].append(dict(id=extra,evidence='amendment fixture',analysis='new condition read',verdict='PASS',fix=dict(where='',what='',verify='')))
        return value
    fixtures.payload=payload
runpy.run_path(str(Path(__file__).with_name('fake_codex.py')),run_name='__main__')
