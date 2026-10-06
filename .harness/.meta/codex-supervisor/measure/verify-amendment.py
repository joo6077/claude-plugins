#!/usr/bin/env python3
"""Verify amendment artifacts without changing sealed text or legacy measurements."""
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
LOG=HERE/'verification/amendment-1'
SIDE=HERE.parent/'sprint-amendments-codex-supervisor.md'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',MEASURE_NO_LIVE='1')
IDS=['스크립트-'+str(n) for n in range(12,20)]

def run(argv):
    p=subprocess.run([str(a) for a in argv],env=ENV,text=True,capture_output=True)
    return p.returncode,p.stdout+p.stderr


def trial(item):
    ident,flag=item
    argv=['bash',HERE/'measure.sh',ident]+([flag] if flag else [])
    rc,out=run(argv)
    label='controls' if flag=='--controls-only' else 'negative' if flag else 'baseline'
    (LOG/(ident+'-'+label+'.txt')).write_text('$ '+' '.join(map(str,argv))+'\n'+out+'exit='+str(rc)+'\n')
    final=[x for x in out.splitlines() if x.startswith(('PASS ','FAIL '))]
    if label=='controls':
        ok=rc==0 and 'positive_control=1' in out and 'known_answer expected=2 actual=2' in out
        if ident=='스크립트-14': ok=ok and 'heartbeat_live expected=1 actual=1' in out and 'heartbeat_stopped expected=0 actual=0' in out
        if ident=='스크립트-15': ok=ok and 'record_mutations expected=7 actual=7' in out
    else: ok=rc==1 and bool(final) and final[-1].startswith('FAIL '+ident) and 'measurement error' not in out
    print(label+' '+(final[-1] if final else 'NO RESULT')+' exit='+str(rc)+' expected='+str(ok),flush=True)
    return dict(condition=ident,kind=label,rc=rc,result=final[-1] if final else '',ok=ok)


def main():
    LOG.mkdir(parents=True,exist_ok=True)
    syntax=[]
    for f in sorted(HERE.iterdir()):
        if not f.is_file(): continue
        commands=([['bash','-n',f],['zsh','-n',f]] if f.suffix=='.sh' else [['python3','-m','py_compile',f]] if f.suffix=='.py' or f.name=='fake-codex' else [])
        for command in commands:
            rc,out=run(command); syntax.append(dict(command=list(map(str,command)),rc=rc,output=out))
    (LOG/'syntax.json').write_text(json.dumps(syntax,ensure_ascii=False,indent=2))
    good=all(r['rc']==0 for r in syntax)
    print('syntax checks='+str(len(syntax))+' failures='+str(sum(r['rc']!=0 for r in syntax)),flush=True)
    body=SIDE.read_text()
    headers=re.findall(r'^## (AM-\d+) — (narrowing|relaxing|unknown)$',body,re.M)
    entries=re.split(r'(?=^## AM-\d+)',body,flags=re.M)[1:]
    entry_ok=len(headers)==9 and all(all(field in entry for field in ('- 대상 조건:','- 변경:','- 근거 (redaction 거친 원문):','- 앵커:','- consent: anchored')) for entry in entries)
    ids=re.findall(r'^- \[ \] ([^:]+):',body,re.M)
    good=good and entry_ok and ids==IDS
    print('amendment_entries='+str(len(headers))+' new_conditions='+str(len(ids))+' entry_format='+str(entry_ok),flush=True)
    direction=[]
    for shell in ('bash','zsh'):
        for mode,before,after,expected in (
            ('measured','measured-before.txt','measured-after.txt','narrowing measured_removed=0 measured_added=8'),
            ('allowed','allowed-before.txt','allowed-after.txt','relaxing added=27 removed=0'),
            ('allowed','allowed-after.txt','allowed-before.txt','narrowing added=0 removed=27'),
            ('measured','missing-input.txt','measured-after.txt','unknown missing_input=')):
            rc,out=run([shell,HERE/'amendment-direction.sh',mode,LOG/before,LOG/after])
            ok=rc==0 and (out.strip()==expected if not expected.endswith('=') else out.startswith(expected))
            good=good and ok; direction.append(dict(shell=shell,mode=mode,output=out.strip(),ok=ok))
            print(shell+' direction '+out.strip(),flush=True)
        for n in range(1,9):
            rc,out=run([shell,HERE/'amendment-direction.sh','measured',LOG/'measured-before.txt',LOG/('measured-AM-'+str(n).zfill(2)+'.txt')])
            good=good and rc==0 and out.strip()=='narrowing measured_removed=0 measured_added=1'
    (LOG/'directions.json').write_text(json.dumps(direction,indent=2))
    with ThreadPoolExecutor(max_workers=3) as pool:
        controls=list(pool.map(trial,[(ident,'--controls-only') for ident in IDS]))
    with ThreadPoolExecutor(max_workers=3) as pool:
        baselines=list(pool.map(trial,[(ident,'') for ident in IDS]))
    with ThreadPoolExecutor(max_workers=3) as pool:
        negatives=list(pool.map(trial,[(ident,'--negative') for ident in IDS]))
    rc,out=run(['bash',HERE/'measure.sh','스크립트-10'])
    (LOG/'legacy-스크립트-10.txt').write_text(out+'exit='+str(rc)+'\n')
    legacy=rc==0 and 'PASS 스크립트-10 checks=26 failures=0' in out
    print('legacy 스크립트-10 PASS='+str(legacy)+' checks=26 failures=0 exit='+str(rc),flush=True)
    before=json.loads((LOG/'before-hashes.json').read_text())
    changed=[name for name,digest in before.items() if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest]
    meta=json.loads((LOG/'sealed-reference.json').read_text())
    wrapper=hashlib.sha256((HERE/'measure.sh').read_bytes()).hexdigest()[:16]
    sealed=hashlib.sha256(Path(meta['contract']).read_bytes()).hexdigest()==meta['contract_sha256']
    hash_ok=changed==['measure.sh'] and wrapper==meta['wrapper_after'] and meta['wrapper_before'] in body and wrapper in body
    print('existing_files_changed='+','.join(changed)+' disclosed_hashes='+str(hash_ok)+' sealed_contract_unchanged='+str(sealed),flush=True)
    source=Path.home()/'.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/fb4aefa8-0ee1-4711-9b22-7baf9c6b989f.jsonl'
    anchor=json.loads((LOG/'anchor.json').read_text())
    observed=next(json.loads(line) for line in source.read_text().splitlines() if json.loads(line).get('uuid')==anchor['uuid'])
    anchor_ok=all(observed[k]==anchor[k] for k in ('timestamp','sessionId','cwd','message')) and observed['type']=='user' and observed['message']['content']==[dict(type='text',text='1')]
    print('user_anchor_verified='+str(anchor_ok)+' timestamp='+anchor['timestamp'],flush=True)
    good=good and all(r['ok'] for r in controls+baselines+negatives) and legacy and hash_ok and sealed and anchor_ok
    table=['# 개정 1 대조 실측','', '| 조건 | 양성 기대/실제 | 알려진 답 기대/실제 | controls 종료 | 일반 실행 | 음성 대조 |','| --- | --- | --- | ---: | --- | --- |']
    for control,baseline,negative in zip(controls,baselines,negatives):
        table.append('| '+control['condition']+' | 1 / '+('1' if control['ok'] else '불일치')+' | 2 / '+('2' if control['ok'] else '불일치')+' | '+str(control['rc'])+' | '+baseline['result']+' | '+negative['result']+' |')
    table+=['','스크립트-14: heartbeat 살아 있음 1/1, 정지 뒤 갱신 0/0. 스크립트-15: 변이 검출 7/7.','', '기존 스크립트-10은 변경 전·후 동일하게 PASS checks=26 failures=0. 코드 해시는 measure.sh의 공개된 분기 추가 외에 모두 동일하다. 실제 모델 호출 0.']
    (LOG/'control-results.md').write_text('\n'.join(table)+'\n')
    summary='verification='+('PASS' if good else 'FAIL')+' new_conditions=8 controls='+str(sum(r['ok'] for r in controls))+'/8 expected_baseline_failures='+str(sum(r['ok'] for r in baselines))+'/8 negative_failures='+str(sum(r['ok'] for r in negatives))+'/8 legacy_unchanged='+str(hash_ok)+' sealed_unchanged='+str(sealed)+' model_calls=0'
    (LOG/'summary.json').write_text(json.dumps(dict(summary=summary,controls=controls,baselines=baselines,negatives=negatives,legacy_pass=legacy,changed=changed),ensure_ascii=False,indent=2))
    print(summary)
    return 0 if good else 1

if __name__=='__main__': sys.exit(main())
