"""Small public-boundary fixtures. No production decision algorithm lives here."""
import copy
import json

IDS = ['스크립트-01', '스크립트-02']
CONTRACT = '''---
feature: "손 예제"
created: "2026-10-01 00:00"
complexity: simple
conditions: 2
slug: sample
status: active
owner_session: measure-session
---
# 손 예제
## Script
- [ ] 스크립트-01: 첫 값이 GOOD 이다 (측정: python3 -c 'print("GOOD")') [exact]
- [ ] 스크립트-02: 둘째 값이 GOOD 이다 (측정: python3 -c 'print("GOOD")') [exact]
## 범위 경계
```text
# sprint-scope
sample.txt
```
'''

def decision(kind='approve'):
    rows = [dict(id=i, evidence='sample.txt: GOOD', analysis='조건과 값 대조',
                 verdict='PASS', fix=dict(where='', what='', verify='')) for i in IDS]
    result = dict(conditions=rows, verdict='APPROVE', questions=[])
    if kind in ('reject', 'reject-other'):
        row = rows[1 if kind == 'reject' else 0]
        row.update(evidence='sample.txt: BAD', analysis='BAD 는 GOOD 과 다르다', verdict='FAIL',
                   fix=dict(where='sample.txt', what='BAD 를 GOOD 으로', verify='같은 조건 재측정'))
        result['verdict'] = 'REJECT'
    elif kind == 'research':
        result.update(verdict='RESEARCH', questions=['외부 규격의 현재 값을 확인해 주세요: FACT_TOKEN'])
    return result

def payload(kind):
    if kind.startswith('draft'):
        body = CONTRACT
        if kind == 'draft-header': body += '\n## Forbidden\n'
        if kind == 'draft-placement': body += '\n## 배경\n- [ ] 스크립트-03: 잘못 놓임 [exact]\n'
        if kind == 'draft-count': body = body.replace('conditions: 2', 'conditions: 9')
        if kind == 'draft-unmeasured': body = body.replace('[exact]', '[exact] [미실측]', 1)
        if kind == 'draft-revised': body = body.replace('손 예제', '지적 반영', 1)
        return dict(contract=body, measurements=[dict(path='measure.sh', content='#!/usr/bin/env bash\nprintf \'PASS sample\\n\'\n')])
    if kind == 'research-answer':
        return dict(answers=[dict(question='외부 규격의 현재 값을 확인해 주세요: FACT_TOKEN',
                                 answer='FACT_ANSWER', sources=['https://example.invalid/fixture'])])
    result = decision(kind)
    if kind == 'missing-id': result['conditions'].pop()
    if kind == 'duplicate-id': result['conditions'][1]['id'] = IDS[0]
    if kind == 'unknown-id': result['conditions'][1]['id'] = '스크립트-99'
    if kind == 'inconsistent': result = decision('reject'); result['verdict'] = 'APPROVE'
    if kind == 'allpass-reject': result['verdict'] = 'REJECT'
    if kind in ('fix-where', 'fix-what', 'fix-verify'):
        result = decision('reject'); result['conditions'][1]['fix'][kind[4:]] = '   '
    if kind == 'extra-key': result['unexpected'] = True
    if kind == 'wrong-type': result['conditions'] = 'not an array'
    if kind == 'empty-evidence': result['conditions'][1]['evidence'] = ''
    return result

def schema_errors(schema):
    """Strict output-schema structure, not an implementation validator replica."""
    errors = []
    def walk(node, at):
        if isinstance(node, dict):
            if 'allOf' in node or 'if' in node or 'then' in node:
                errors.append(at + ': unsupported composition')
            if node.get('type') == 'object' or 'properties' in node:
                if node.get('additionalProperties') is not False:
                    errors.append(at + ': additionalProperties')
                if set(node.get('required', [])) != set(node.get('properties', {})):
                    errors.append(at + ': required')
            for key, value in node.items(): walk(value, at + '/' + key)
        elif isinstance(node, list):
            for n, value in enumerate(node): walk(value, at + '/' + str(n))
    walk(schema, '$')
    return errors

def strict_schema(properties):
    return dict(type='object', properties=properties, required=list(properties), additionalProperties=False)

def fixture_schema(value):
    """Schema for known responses only; not a production schema generator."""
    if isinstance(value,dict): return strict_schema({k:fixture_schema(v) for k,v in value.items()})
    if isinstance(value,list): return dict(type='array',items=fixture_schema(value[0]) if value else dict(type='string'))
    if isinstance(value,str): return dict(type='string')
    raise ValueError('unsupported fixture value')

def nonimpl_faults():
    """Three transport/schema faults in each previously uncovered response phase."""
    for phase,response,field in (('draft','draft','contract'),('revise','draft-revised','measurements'),
                                 ('research','research-answer','answers')):
        for fault in ('missing-file','malformed','missing-required'):
            yield phase,dict(response=response,fault=fault,field=field)

def match_json(value, schema, root=None):
    """Small schema reader for controls; supports the fixture's strict schema subset."""
    root = schema if root is None else root
    if '$ref' in schema:
        node = root
        for key in schema['$ref'].split('/')[1:]: node = node[key]
        return match_json(value, node, root)
    if 'anyOf' in schema: return any(match_json(value, x, root) for x in schema['anyOf'])
    if 'enum' in schema and value not in schema['enum']: return False
    typ = schema.get('type')
    if isinstance(typ, list): return any(match_json(value, dict(schema, type=t), root) for t in typ)
    if typ == 'object':
        if not isinstance(value, dict): return False
        props = schema.get('properties', {})
        if not set(schema.get('required', [])).issubset(value): return False
        if schema.get('additionalProperties') is False and not set(value).issubset(props): return False
        return all(match_json(v, props[k], root) for k, v in value.items() if k in props)
    if typ == 'array': return isinstance(value, list) and all(match_json(v, schema['items'], root) for v in value)
    if typ == 'string': return isinstance(value, str)
    if typ == 'integer': return isinstance(value, int) and not isinstance(value, bool)
    if typ == 'number': return isinstance(value, (int, float)) and not isinstance(value, bool)
    if typ == 'boolean': return isinstance(value, bool)
    if typ == 'null': return value is None
    return True
