#!/usr/bin/env python3
"""AM-01..08 black-box measurements; legacy measurement functions stay unchanged."""
import copy,hashlib,json,os,re,shlex,signal,subprocess,sys,tempfile,time
from pathlib import Path
import measure as old
import prompt_checks
HERE=Path(__file__).resolve().parent
IDS=['스크립트-01','스크립트-02']
NEW=['스크립트-'+str(n) for n in range(12,20)]
check=old.check
eq=old.eq


def rows(path):
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []


def once(ids, trace):
    return sorted(x['id'] for x in trace)==sorted(ids) and len(trace)==len(ids)


def file_under(folder,rel):
    if not isinstance(rel,str) or Path(rel).is_absolute(): raise ValueError('record path must be relative')
    path=(folder/rel).resolve()
    if not path.is_relative_to(folder.resolve()) or not path.is_file(): raise ValueError('missing/outside frozen file')
    return path


def read_bundle(folder,ids):
    """External serialized boundary, independent of production private functions."""
    problems=[]; records=[]; summary=''
    try:
        manifest=json.loads((folder/'MANIFEST.json').read_text())
        pre=manifest['premeasure']
        if not isinstance(pre['records'],list): raise ValueError('records must be paths')
        for rel in pre['records']:
            record=json.loads(file_under(folder,rel).read_text())
            if not isinstance(record,dict): raise ValueError('record must be object')
            if not all(k in record for k in ('id','command','exit_code','output','timed_out')): raise ValueError('required record fields')
            if not isinstance(record['id'],str) or not isinstance(record['command'],str) or not record['command'].strip(): raise ValueError('record identity/command')
            if type(record['exit_code']) is not int or type(record['timed_out']) is not bool or not isinstance(record['output'],str): raise ValueError('record types')
            records.append(record)
        if sorted(x['id'] for x in records)!=sorted(ids): problems.append('record condition set or duplicates')
        summary=file_under(folder,pre['summary']).read_text()
        expected=['condition\texit_code\tlast_line']
        for row in records:
            last=row['output'].splitlines()[-1] if row['output'].splitlines() else ''
            expected.append(row['id']+'\t'+str(row['exit_code'])+'\t'+last.replace('\t',' '))
        if summary!='\n'.join(expected)+'\n': problems.append('summary mismatch')
        for p in folder.rglob('*'):
            if p.is_file() and b'sk-FIXTURE-SECRET' in p.read_bytes(): problems.append('key in frozen input')
    except (KeyError,ValueError,OSError,TypeError): problems.append('missing or invalid frozen premeasurement bundle')
    return records,problems,summary


def setup(label,steps=('approve',),mode='success',setting=True,extra=False):
    c=old.Case('amend-'+label,steps)
    c.env['CODEX_BIN']=str(HERE/'fake_amendment.py')
    c.env['QA_AMEND_TRACE']=str(c.state/'premeasure-trace.jsonl')
    c.env['QA_AMEND_MODE']=mode
    c.env['CODEX_AUDIT_LIMIT']='1'
    command='python3 '+shlex.quote(str(HERE/'amendment_probe.py'))+' {id}'
    if mode=='missing': command='amendment-intentionally-missing-command {id}'
    if setting is True: c.configure('codex_audit:\n  premeasure: '+json.dumps(command)+'\n')
    elif setting=='empty': c.configure('codex_audit:\n  premeasure: ""\n')
    c.amend_command=command
    c.amend_ids=list(IDS)
    if extra:
        c.env['QA_AMEND_EXTRA_ID']='스크립트-03'; c.amend_ids.append('스크립트-03')
        c.sidecar=c.meta/'sprint-amendments-sample.md'
        c.sidecar.write_text('# Test-only sidecar\n## AM-01 — narrowing\n- 대상 조건: 스크립트-03\n- 변경: 손 예제 조건 추가\n- 근거: synthetic fixture\n- 앵커: synthetic fixture; not user consent\n- [ ] 스크립트-03: sample.txt가 존재한다 [exact]\n  측정: test -f sample.txt\n')
    return c


def invoke(c,verdict='APPROVE',calls=1):
    result=c.invoke(limit=30)
    c.outcome(result,0 if verdict=='APPROVE' else 1,verdict,calls)
    observations=rows(c.state/'amend-observations.jsonl')
    folders=sorted((c.meta/'codex-audit').rglob('MANIFEST.json'))
    check(bool(folders),'frozen manifest produced')
    folder=folders[-1].parent if folders else c.meta/'missing-frozen-input'
    return result,observations,folder


def bundle(c,folder):
    records,problems,_=read_bundle(folder,c.amend_ids)
    eq(problems,[],'valid frozen premeasurement records')
    return records


def schedule():
    for name,steps,verdict in (('approve',['approve'],'APPROVE'),('review',['reject','reject'],'REJECT'),
                               ('research-review',['research','research-answer','reject','reject'],'REJECT')):
        c=setup(name,steps)
        _,observed,folder=invoke(c,verdict,len(steps)); bundle(c,folder)
        trace=rows(Path(c.env['QA_AMEND_TRACE']))
        check(once(IDS,trace),'once per condition for whole audit')
        snapshots=[]
        for phase,step in zip(observed,steps):
            if step=='research-answer': continue
            check(once(IDS,phase['trace']),'all premeasurement complete before judgment')
            referenced=[b for b in phase['bundles'] if b['referenced']]
            eq(len(referenced),1,'judge references one frozen manifest')
            if referenced: snapshots.append(referenced[0]['hashes'])
        check(len(snapshots)==(1 if name=='approve' else 2 if name=='review' else 3),'all required judgment stages observed')
        check(bool(snapshots) and all(s==snapshots[0] for s in snapshots),'identical frozen input in judgment rejudgment review')
        final={str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
        if snapshots: eq(final,snapshots[0],'frozen records unchanged after audit')


def configuration():
    for setting in (False,'empty',True):
        c=setup('setting-'+str(setting),setting=setting)
        _,_,folder=invoke(c)
        trace=rows(Path(c.env['QA_AMEND_TRACE']))
        if setting is True:
            check(once(IDS,trace),'configured command substitutes each condition')
            records=bundle(c,folder)
            for r in records: eq(r['command'],c.amend_command.replace('{id}',r['id']),'expanded command recorded')
        else:
            eq(trace,[],'unset or empty premeasure disabled')
            manifest=json.loads((folder/'MANIFEST.json').read_text()) if (folder/'MANIFEST.json').exists() else {}
            check(not manifest.get('premeasure'),'disabled no premeasurement artifacts')


def isolation_timeout():
    c=setup('timeout',mode='timeout'); before=old.bytes_tree(c.repo,('.harness',))
    try:
        _,observed,folder=invoke(c)
        records=bundle(c,folder); trace=rows(Path(c.env['QA_AMEND_TRACE']))
        check(once(IDS,trace),'timeout advances to next condition exactly once')
        for row in trace:
            cwd=Path(row['cwd']).resolve()
            check(cwd!=c.repo.resolve() and cwd.is_relative_to(c.root),'premeasurement writes only temporary clone')
            eq(row['head'],c.head,'premeasurement implementation commit')
            check(row['git_dir']!=str(c.repo/'.git'),'independent clone git metadata')
            check(not row['in_codex'],'command not run by judgment Codex')
        if len(trace)==2:
            check(0<trace[1]['started']-trace[0]['started']<3,'one-second timeout plus under two-second scheduling tolerance')
        eq(old.bytes_tree(c.repo,('.harness',)),before,'original files and git unchanged')
        if observed: check(once(IDS,observed[0]['trace']),'premeasurement occurs before Codex')
        by_id={r['id']:r for r in records}
        check(by_id.get(IDS[0],{}).get('timed_out') is True,'first condition timeout recorded')
        check(by_id.get(IDS[0],{}).get('exit_code') not in (None,0),'timeout nonzero recorded')
        eq(by_id.get(IDS[1],{}).get('exit_code'),0,'next condition still runs')
        beat=c.state/'heartbeat'; check(beat.is_file(),'timeout spawned real child')
        a=beat.read_bytes() if beat.exists() else None
        time.sleep(0.35)
        eq(beat.read_bytes() if beat.exists() else None,a,'child heartbeat stopped after timeout')
    finally:
        pidfile=c.state/'child.pid'
        if pidfile.exists():
            try: os.kill(int(pidfile.read_text()),signal.SIGKILL)
            except ProcessLookupError: pass


def records():
    c=setup('records',mode='secret'); _,_,folder=invoke(c); data=bundle(c,folder)
    check(once(IDS,rows(Path(c.env['QA_AMEND_TRACE']))),'records correspond to executed commands')
    for row in data:
        eq(row['command'],c.amend_command.replace('{id}',row['id']),'exact command stored')
        eq(row['exit_code'],0,'real exit stored')
        check('BEGIN '+row['id'] in row['output'] and 'END '+row['id'] in row['output'] and 'stderr' in row['output'],'stdout and stderr retained')
        check('sk-FIXTURE-SECRET' not in row['output'],'key redacted')
    eq(old.leak_files(c.meta),[],'no key in any audit artifact')


def instruction_issues(text):
    required=('사전 측정','격리 밖','판정 전','증거','격리 안','직접','프로세스','서비스')
    issues=[token for token in required if token not in text]
    if not re.search(r'(못|불가|없는|제한)',text): issues.append('sandbox limitation gate missing')
    stats=prompt_checks.prompt_stats([('judgment',text)])
    if stats['roles'] or stats['bytes']>8192 or stats['examples']>1: issues.append('neutral prompt budget violated')
    return issues


def instructions():
    c=setup('instructions'); _,observed,folder=invoke(c); bundle(c,folder)
    templates=old.SOURCE/'harness/templates/codex-audit'
    prompt_checks.measure_prompt(templates,check,eq)
    calls=c.calls(); check(bool(calls),'judgment prompt observed')
    for row in calls:
        text=prompt_checks.delivered_text(row)
        eq(instruction_issues(text),[],'premeasurement provenance and direct rerun instructions')
        check(str(folder/'MANIFEST.json') in text,'readable frozen manifest referenced')


def command_failure():
    for mode in ('nonzero','missing'):
        for steps,verdict in ((['approve'],'APPROVE'),(['reject','reject'],'REJECT')):
            c=setup(mode+'-'+verdict,steps,mode); _,_,folder=invoke(c,verdict,len(steps)); data=bundle(c,folder)
            for row in data:
                check(row['exit_code']!=0,'failed command recorded')
                if mode=='nonzero': eq(row['exit_code'],7,'known command exit')
                check(bool(row['output'].strip()),'failure output retained')
            check('감독 판정: BLOCKED' not in c.report(),'command failure does not BLOCK judgment')


def document_issues(body,tokens): return [token for token in tokens if token not in body]


def docs():
    import yaml
    config=yaml.safe_load((old.W/'.harness/project.yaml').read_text())
    actual=config.get('codex_audit',{}).get('premeasure')
    eq(actual,'bash .harness/.meta/codex-supervisor/measure/measure.sh {id}','repository opts into its sealed measurements')
    template=(old.SOURCE/'harness/templates/project.yaml').read_text()
    parsed=yaml.safe_load(template)
    check('premeasure' in parsed.get('codex_audit',{}) and parsed['codex_audit']['premeasure'] in ('',None),'template empty premeasure field')
    lines=template.splitlines(); indices=[i for i,line in enumerate(lines) if re.match(r'\s+premeasure:',line)]
    check(any('#' in '\n'.join(lines[max(0,i-3):i+2]) and '{id}' in '\n'.join(lines[max(0,i-3):i+2]) for i in indices),'template documents command placeholder')
    for rel in ('harness/README.md','harness/agents/qa-evaluator.md','harness/skills/sprint-contract/SKILL.md'):
        eq(document_issues((old.SOURCE/rel).read_text(),('premeasure','사전 측정')),[],'documentation '+rel)


def amendments():
    c=setup('sidecar',steps=['reject','reject'],extra=True)
    original=c.sidecar.read_bytes(); _,observed,folder=invoke(c,'REJECT',2); bundle(c,folder)
    copies=[p for p in folder.rglob('*') if p.is_file() and p.read_bytes()==original]
    eq(len(copies),1,'sidecar frozen verbatim exactly once')
    check(once(c.amend_ids,rows(Path(c.env['QA_AMEND_TRACE']))),'new sidecar condition also premeasured')
    for phase in observed:
        check(bool(copies) and (str(copies[0]) in phase['prompt'] or any(b['referenced'] and any(copies[0].name in str(v) for v in b['manifest'].values()) for b in phase['bundles'])),'judge and review directed to frozen amendments')
        check('개정' in phase['prompt'] or 'amendment' in phase['prompt'].lower(),'explicit instruction to read amendments')
    check('스크립트-03' in c.report(),'sidecar condition judged in report')
    eq(c.sidecar.read_bytes(),original,'original sidecar unchanged')
    absent=setup('without-sidecar'); _,_,without=invoke(absent); bundle(absent,without)
    check(not any('amendment' in p.name.lower() for p in without.rglob('*')),'absent sidecar does not invent frozen amendment')

SUITES=dict(zip(NEW,(schedule,configuration,isolation_timeout,records,instructions,command_failure,docs,amendments)))


def known_bundle(folder):
    folder.mkdir(parents=True,exist_ok=True)
    data=[dict(id=i,command='fixture '+i,exit_code=0,output='END '+i+'\n',timed_out=False) for i in IDS]
    names=[]
    for n,row in enumerate(data):
        name='known-'+str(n)+'.json'; names.append(name); (folder/name).write_text(json.dumps(row,ensure_ascii=False))
    (folder/'summary.tsv').write_text('condition\texit_code\tlast_line\n'+''.join(r['id']+'\t0\tEND '+r['id']+'\n' for r in data))
    (folder/'MANIFEST.json').write_text(json.dumps(dict(premeasure=dict(records=names,summary='summary.tsv'))))
    return data


def heartbeat_control():
    folder=old.RUN/'heartbeat-control'; folder.mkdir()
    env=dict(os.environ,QA_AMEND_TRACE=str(folder/'trace.jsonl'),QA_AMEND_MODE='timeout',
             GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1')
    for args in (['init','-q'],['config','user.name','fixture'],['config','user.email','fixture@example.invalid'],['commit','--allow-empty','-qm','fixture']):
        p=old.command(['git',*args],folder,env); eq(p.returncode,0,'heartbeat fixture git')
    with (folder/'stdout.txt').open('w') as out:
        proc=subprocess.Popen(['python3',str(HERE/'amendment_probe.py'),IDS[0]],cwd=folder,env=env,
                              stdout=out,stderr=out,start_new_session=True)
        beat=folder/'heartbeat'
        try:
            deadline=time.monotonic()+3
            while not beat.exists() and time.monotonic()<deadline: time.sleep(0.02)
            first=beat.read_bytes() if beat.exists() else None
            time.sleep(0.2)
            moved=int(beat.exists() and first!=beat.read_bytes())
        finally:
            os.killpg(proc.pid,signal.SIGKILL); proc.wait()
        after=beat.read_bytes() if beat.exists() else None
        time.sleep(0.2)
        still=int(beat.exists() and after!=beat.read_bytes())
    print('heartbeat_live expected=1 actual='+str(moved)); eq(moved,1,'positive live child heartbeat')
    print('heartbeat_stopped expected=0 actual='+str(still)); eq(still,0,'known stopped child heartbeat')


def record_mutations():
    detected=0
    for fault in ('missing','type','duplicate','summary','key','outside','absolute'):
        folder=old.RUN/('record-mutation-'+fault); known_bundle(folder)
        p=folder/'known-1.json'; value=json.loads(p.read_text())
        if fault=='missing': p.unlink()
        if fault=='type': value['exit_code']='0'; p.write_text(json.dumps(value))
        if fault=='duplicate': value['id']=IDS[0]; p.write_text(json.dumps(value))
        if fault=='summary': (folder/'summary.tsv').write_text('wrong')
        if fault=='key': value['output']='sk-FIXTURE-SECRET'; p.write_text(json.dumps(value))
        if fault=='outside':
            manifest=json.loads((folder/'MANIFEST.json').read_text()); outside=old.RUN/'outside-summary.tsv'; outside.write_text((folder/'summary.tsv').read_text()); manifest['premeasure']['summary']='../outside-summary.tsv'
            (folder/'MANIFEST.json').write_text(json.dumps(manifest))
        if fault=='absolute':
            manifest=json.loads((folder/'MANIFEST.json').read_text()); manifest['premeasure']['summary']=str((folder/'summary.tsv').resolve())
            (folder/'MANIFEST.json').write_text(json.dumps(manifest))
        detected+=int(bool(read_bundle(folder,IDS)[1]))
    print('record_mutations expected=7 actual='+str(detected)); eq(detected,7,'seven malformed record inputs rejected')


def controls(condition):
    if condition=='스크립트-14': heartbeat_control()
    if condition=='스크립트-15': record_mutations()
    root=old.RUN/'known'; data=known_bundle(root)
    values,issues,_=read_bundle(root,IDS); eq(issues,[],'known valid frozen record bundle')
    expected=2; actual=len(values)
    if condition in ('스크립트-12','스크립트-13'):
        eq(once(IDS,[dict(id=i) for i in IDS]),True,'known once-per-id trace')
        positive=int(not once(IDS,[dict(id=i) for i in IDS]+[dict(id=IDS[0])]))
    elif condition=='스크립트-14':
        positive=int(not once(IDS,[dict(id=IDS[0])]))
        eq(positive,1,'missing next condition detected')
    elif condition=='스크립트-16':
        good='사전 측정은 감독 스크립트가 판정 전에 격리 밖에서 남긴 기록이다. 격리 안에서 실행할 수 없는 프로세스 관측·겹친 격리·실제 서비스 측정은 이 기록을 증거로 쓸 수 있다. 가능한 측정은 직접 돌린다.'
        eq(instruction_issues(good),[],'known provenance instruction')
        positive=int(bool(instruction_issues(good.replace('격리 밖','다른 곳'))))
    elif condition=='스크립트-18':
        eq(document_issues('premeasure 사전 측정',('premeasure','사전 측정')),[],'known documentation')
        positive=len(document_issues('사전 측정',('premeasure','사전 측정')))
    else:
        (root/'known-1.json').unlink()
        positive=int(bool(read_bundle(root,IDS)[1]))
    print('positive_control='+str(positive)); eq(positive,1,'positive control catches known violation')
    print('known_answer expected='+str(expected)+' actual='+str(actual)); eq(actual,expected,'two hand-counted records')


def main():
    args=sys.argv[1:]
    if not args or args[0] not in SUITES: print('FAIL amendment usage'); return 64
    condition=args[0]
    runs=HERE/'.runs'; runs.mkdir(exist_ok=True)
    old.RUN=Path(tempfile.mkdtemp(prefix=condition+'-amend-',dir=runs))
    print('evidence='+str(old.RUN),flush=True)
    try:
        controls(condition)
        if '--controls-only' not in args:
            old.snapshot()
            if '--negative' in args:
                if condition=='스크립트-18':
                    f=old.SOURCE/'harness/templates/project.yaml'; f.write_text(f.read_text().replace('premeasure','removed-premeasure-field'))
                else: (old.SOURCE/old.SCRIPT).write_text('#!/usr/bin/env bash\nexit 0\n')
            if condition=='스크립트-18' or old.need_script(): SUITES[condition]()
    except Exception as exc:
        check(False,'measurement error',type(exc).__name__+': '+str(exc))
    (old.RUN/'evidence.json').write_text(json.dumps(dict(condition=condition,events=old.EVENTS,failures=old.FAILURES),ensure_ascii=False,indent=2))
    print(('FAIL' if old.FAILURES else 'PASS')+' '+condition+' checks='+str(old.CHECKS)+' failures='+str(len(old.FAILURES)))
    return int(bool(old.FAILURES))

if __name__=='__main__': sys.exit(main())
