#!/usr/bin/env python3
"""Reproduce draft QA; writes logs only alongside this file. Never requests model inference; real CLI login status only."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
CONTRACT=HERE.parent/'sprint-contract-codex-supervisor.md'
if not CONTRACT.exists():
    CONTRACT=Path.cwd()/'.harness/sprint-contract-codex-supervisor.md'
LOG=HERE/'verification'
LOG.mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',MEASURE_NO_LIVE='1')

def run(args):
    p=subprocess.run([str(x) for x in args],text=True,capture_output=True,env=ENV)
    return p.returncode,p.stdout+p.stderr

def syntax():
    rows=[]
    # .runs contains intentional syntax failures and copies of the read-only repository.
    # It is fixture DATA, not source of this measurement bundle.
    for f in sorted(HERE.iterdir()):
        if not f.is_file(): continue
        if f.suffix=='.sh':
            for shell in ('bash','zsh'):
                cmd=[shell,'-n',f]; rc,out=run(cmd); rows.append((cmd,rc,out))
        elif f.suffix=='.py' or f.name=='fake-codex':
            cmd=['python3','-m','py_compile',f]; rc,out=run(cmd); rows.append((cmd,rc,out))
    content=''.join('$ '+' '.join(map(str,cmd))+'\n'+out+'exit='+str(rc)+'\n' for cmd,rc,out in rows)
    (LOG/'syntax.txt').write_text(content)
    print('syntax checks='+str(len(rows))+' failures='+str(sum(rc!=0 for _,rc,_ in rows)),flush=True)
    return all(rc==0 for _,rc,_ in rows)

def contract_check():
    rc,out=run(['bash',HERE/'check-contract.sh',CONTRACT]); (LOG/'contract-raw.txt').write_text(out+'exit='+str(rc)+'\n')
    body=CONTRACT.read_text()
    allowed={'Skill','Script','Error','Architecture','Anti-patterns','Reusability','Diagnostics'}
    narrative=('배경','리서치 소스','GAP 분석','범위 경계','회귀 게이트')
    bad_headers=[]; bad_placement=[]; section=''; count=0; tagged=0
    for no,line in enumerate(body.splitlines(),1):
        if line.startswith('## '):
            section=line[3:]
            if section not in allowed and not section.startswith(narrative): bad_headers.append(no)
        if re.match(r'^- \[[ x]\] ',line):
            count+=1
            if section not in allowed: bad_placement.append(no)
            if re.search(r'\[(exact|structural|goal)(, (enumerated|collective))?\]$',line): tagged+=1
    fm=int(re.search(r'^conditions: (\d+)$',body,re.M).group(1))
    front=body.split('---',2)[1]
    correct=('complexity: "복잡"' in front and 'owner_session: fb4aefa8-0ee1-4711-9b22-7baf9c6b989f' in front)
    absent=all(x not in front for x in ('conditions_digest:','measurement_digest:','locked_at:'))
    summary=f'header_violations={len(bad_headers)} placement_violations={len(bad_placement)} conditions={count} frontmatter={fm} tagged={tagged} frontmatter_correction={correct} unsealed={absent}'
    print(summary,flush=True)
    (LOG/'contract-summary.txt').write_text(summary+'\n')
    return rc==0 and not bad_headers and not bad_placement and fm==count==tagged and correct and absent

def cases():
    text=CONTRACT.read_text()
    chunks=re.split(r'(?=^- \[[ x]\] )',text,flags=re.M)[1:]
    result=[]
    for chunk in chunks:
        name=re.match(r'^- \[[ x]\] ([^:]+):',chunk).group(1)
        # End at the next unindented section so prose cannot add an accidental control.
        body=re.split(r'^## ',chunk,flags=re.M)[0]
        if '양성 대조:' in body or '알려진 답:' in body: result.append(name)
    return result

def control(name):
    rc,out=run(['bash',HERE/'measure.sh',name,'--controls-only'])
    (LOG/(name+'-controls.txt')).write_text(out+'exit='+str(rc)+'\n')
    pos=re.search(r'^positive_control=(\d+)$',out,re.M)
    known=re.search(r'^known_answer expected=(\d+) actual=(\d+)$',out,re.M)
    # Independent expected values transcribed from the contract, not the tested function.
    positive={'구조-01':1,'구조-02':1,'스크립트-08':1,'스크립트-10':1,'스크립트-11':1,'진단-01':1,'진단-02':3,'진단-03':1,'금지-03':1,'금지-04':1}.get(name,2)
    answer={'구조-02':1,'스크립트-08':1,'스크립트-11':1,'진단-01':1,'진단-02':3,'진단-03':1,'금지-03':1,'금지-04':1}.get(name,2)
    observed=int(pos.group(1)) if pos else None
    actual=int(known.group(2)) if known else None
    expected_print=int(known.group(1)) if known else None
    ok=rc==0 and observed==positive and actual==answer and expected_print==answer
    if name=='구조-04':
        ok=ok and 'auth_cleanup_paths expected=5 actual=5' in out
    if name=='구조-02':
        ok=ok and 'prompt_role_positive=5' in out and 'prompt_known_bytes expected=12 actual=12' in out
    if name=='스크립트-10':
        ok=ok and 'schema_phases expected=4 actual=4' in out and 'schema_missing_nonimpl_detected=2' in out
    if name=='오류-01':
        ok=ok and 'format_fault_cases expected=9 actual=9' in out
    print(name+' controls '+('PASS' if ok else 'FAIL')+' positive='+str(observed)+' known='+str(actual),flush=True)
    return dict(condition=name,positive_expected=positive,positive_actual=observed,known_expected=answer,known_actual=actual,rc=rc,ok=ok)

def baseline(name):
    rc,out=run(['bash',HERE/'measure.sh',name])
    (LOG/(name+'-baseline.txt')).write_text(out+'exit='+str(rc)+'\n')
    last=[x for x in out.splitlines() if x.startswith(('PASS ','FAIL '))]
    ok=rc==1 and bool(last) and last[-1].startswith('FAIL '+name) and 'measurement error' not in out
    if name=='스크립트-11': ok=ok and 'MISSING harness/scripts/codex-audit.sh' in out
    print('baseline '+(last[-1] if last else 'NO RESULT')+' exit='+str(rc),flush=True)
    return dict(condition=name,rc=rc,result=last[-1] if last else '',expected_failure=ok)

def main():
    good=syntax() and contract_check()
    delete_pattern=re.compile(r'\brm\s+(?:-[A-Za-z]*[fr][A-Za-z]*)(?:\s|$)')
    offenders=[f.name for f in HERE.iterdir() if f.is_file() and (f.suffix in ('.sh','.py') or f.name=='fake-codex') and delete_pattern.search(f.read_text())]
    known='r'+'m -'+'rf fixture'
    scan_ok=not offenders and bool(delete_pattern.search(known))
    print('shell_delete_commands='+str(len(offenders))+' scanner_positive='+str(int(bool(delete_pattern.search(known)))),flush=True)
    (LOG/'deletion-scan.json').write_text(json.dumps(dict(offenders=offenders,positive=1,ok=scan_ok)))
    good=good and scan_ok
    with ThreadPoolExecutor(max_workers=3) as pool:
        controls=list(pool.map(control,cases()))
    with ThreadPoolExecutor(max_workers=3) as pool:
        baselines=list(pool.map(baseline,['스크립트-01','스크립트-02','스크립트-03','스크립트-07','스크립트-10','스크립트-11','오류-01','구조-03','스킬-01','스크립트-05','스크립트-08','구조-04']))
    negatives=[]
    for name in ('구조-02','스크립트-11','구조-04'):
        rc,out=run(['bash',HERE/'measure.sh',name,'--negative'])
        (LOG/(name+'-negative.txt')).write_text(out+'exit='+str(rc)+'\n')
        required=['BAD instruction forbidden role matches','BAD instruction UTF-8 byte limit','BAD instruction worked-example limit'] if name=='구조-02' else ['LIVE_FAKE_OVERRIDE_REJECTED'] if name=='스크립트-11' else ['BAD credentials actually consumed']
        ok=rc==1 and all(token in out for token in required) and 'measurement error' not in out
        negatives.append(dict(condition=name,rc=rc,ok=ok))
        print('negative '+name+' expected_FAIL='+str(ok),flush=True)
    rc,prep_out=run(['bash',HERE/'measure.sh','스크립트-11','--prepare-only'])
    (LOG/'스크립트-11-preparation.txt').write_text(prep_out+'exit='+str(rc)+'\n')
    prep_state='READY' if rc==0 and prep_out.count('login_status=Logged in')==2 and 'auth_copy_removed=true source_unchanged=true secret_leaks=0' in prep_out else 'UNMET' if rc==2 and 'PRECONDITION_UNMET' in prep_out else 'ERROR'
    preparation=dict(state=prep_state,rc=rc,model_calls=0,implementation_evaluated=False)
    print('live_precondition='+prep_state+' exit='+str(rc)+' model_calls=0',flush=True)
    table=['# 계약 대조 실측','',
           '명령: `bash out/measure/measure.sh <조건> --controls-only`. 모든 행의 원문 출력은 verification/<조건>-controls.txt에 있다.',
           '', '| 조건 | 양성 기대 | 양성 실제 | 알려진 답 기대 | 실제 | 종료 | 일치 |',
           '| --- | ---: | ---: | ---: | ---: | ---: | --- |']
    for row in controls:
        table.append('| {condition} | {positive_expected} | {positive_actual} | {known_expected} | {known_actual} | {rc} | '.format(**row)+('PASS' if row['ok'] else 'FAIL')+' |')
    table+=['','양성 대조의 PASS는 구현의 PASS가 아니다. 다음은 옵션 없이 실행한 구현 전 판정이다.','',
            '| 조건 | 현재 결과 | 종료 | 예상한 FAIL인가 |','| --- | --- | ---: | --- |']
    for row in baselines: table.append('| {condition} | {result} | {rc} | '.format(**row)+str(row['expected_failure'])+' |')
    table+=['','구조-02 추가 대조: 역할 부여 다섯 표본 검출 5/5; UTF-8 손 예제 12바이트; 경계 8192 통과·8193 위반; 예시 표제 두 개 검출 2.',
            '스크립트-10 추가 대조: draft·revise·impl·조사 유효 스키마 4/4; revise·조사 스키마 미전달 검출 2/2.',
            '오류-01 추가 대조: draft·revise·조사의 결과 파일 없음·깨진 JSON·필수 칸 빠짐 9/9을 가짜 실행 파일로 실제 생성·검출.',
            '구조-04 추가 대조: 인증 도우미 정상·실패·시간 초과·SIGINT·SIGTERM 정리 기대 5·실제 5.',
            '', '| 음성 대조 | 종료 | 기대 FAIL 확인 |','| --- | ---: | --- |']
    for row in negatives: table.append('| {condition} | {rc} | {ok} |'.format(**row))
    table+=['','실제 감독 폴더 로그인 준비: '+prep_state+' / 종료 '+str(rc)+' / 모델 호출 0 / 구현 판정 안 함. 원문은 verification/스크립트-11-preparation.txt.']
    (HERE/'control-results.md').write_text('\n'.join(table)+'\n')
    good=good and all(x['ok'] for x in controls) and all(x['expected_failure'] for x in baselines) and all(x['ok'] for x in negatives) and prep_state=='READY'
    summary=f'verification={"PASS" if good else "FAIL"} controls={len(controls)} control_mismatches={sum(not x["ok"] for x in controls)} baseline_failures={sum(x["expected_failure"] for x in baselines)}/{len(baselines)} live_precondition={prep_state}'
    (LOG/'summary.json').write_text(json.dumps(dict(summary=summary,controls=controls,baselines=baselines,negatives=negatives,preparation=preparation),ensure_ascii=False,indent=2))
    print(summary)
    return 0 if good else 1

if __name__=='__main__': sys.exit(main())
