#!/usr/bin/env python3
"""Offline, host premeasure for AM-01. Never executes evidence or product code."""
import argparse
import ast
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import shlex
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
# Extract only the sealed classifier's definitions; importing measure.py runs tests.
tree = ast.parse((HERE / 'measure.py').read_text())
selected = [n for n in tree.body if
            (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in
             ('MAJOR', 'WARNING', 'SUMMARY') for t in n.targets)) or
            (isinstance(n, ast.FunctionDef) and n.name == 'relay_line')]
ns = {'re': re}
exec(compile(ast.Module(body=selected, type_ignores=[]), '<sealed relay_line>', 'exec'), ns)
relay_line = ns['relay_line']


def records(path):
    return [(i, json.loads(s)) for i, s in enumerate(path.read_text().splitlines(), 1)]


def blocks(d):
    c = d.get('message', {}).get('content', [])
    return c if isinstance(c, list) else []


def chats(d):
    return [b['text'] for b in blocks(d) if b.get('type') == 'text'] if d.get('type') == 'assistant' else []


def epoch(d):
    return datetime.fromisoformat(d['timestamp'].replace('Z', '+00:00')).timestamp()


def detached_return(call, sent, result, verb):
    """Recognize the documented short Bash launch, not a flag in another command."""
    lexer = shlex.shlex(call['input'].get('command', ''), posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    tokens = list(lexer)
    for i, token in enumerate(tokens):
        if Path(token).name != 'codex-audit.sh' or i == 0 or tokens[i - 1] != 'bash':
            continue
        args = []
        for token in tokens[i + 1:]:
            if token in (';', '|', '||', '&&', '&'):
                break
            args.append(token)
        if not args or args[0] != verb or '--detach' not in args:
            continue
        output = result.get('toolUseResult', {})
        stdout = output.get('stdout', '').strip()
        kind = 'impl' if verb == 'impl' else 'draft'
        returned = [b for b in blocks(result) if b.get('tool_use_id') == call['id']]
        return (0 <= epoch(result) - epoch(sent) <= 30
                and not output.get('interrupted') and not output.get('backgroundTaskId')
                and bool(re.fullmatch(r'/[^\n]+/\.harness/codex-audit/[^/\n]+/' + kind + r'-r[1-9]\d*', stdout))
                and any(b.get('is_error') is False and b.get('content', '').strip() == stdout
                        for b in returned))
    return False


def run(root, negative=False):
    failures = []
    def check(ok, message):
        if not ok:
            failures.append(message)
            print('FAIL ' + message)
        return bool(ok)

    files = sorted(p for p in root.rglob('*') if p.is_file() and p.name != 'cli-review.json')
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print('evidence_sha256=' + json.dumps(hashes, sort_keys=True))
    parent = records(root / 'transcript/parent.jsonl')
    session = (root / 'session.txt').read_text().strip()
    driver = ast.parse((root / 'drive-trial.py').read_text())
    messages = next(ast.literal_eval(n.value) for n in driver.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'MESSAGES' for t in n.targets))
    expected = set(itertools.product(('draft', 'revise', 'impl'), ('direct', 'delegated')))
    check(len(messages) == 6 and {(v, r) for v, r, _ in messages} == expected, 'cases_total=6 matrix')
    print('cases_total=' + str(len(expected)) + ' parent_session=' + session)
    # Plain user messages only; task notifications and tool results are not human requests.
    users = [(n, d) for n, d in parent if d.get('type') == 'user'
             and isinstance(d.get('message', {}).get('content'), str)
             and not d['message']['content'].lstrip().startswith('<task-notification>')]
    check([d['message']['content'] for _, d in users] == [m[2] for m in messages],
          'human messages exactly match six driver requests (extra messages fail)')
    for n, d in users:
        check(not re.search(r'진행|follow|백그라운드|progress|background|작업 카드', d['message']['content'], re.I),
              f'parent:{n} progress-request lexical check; intent remains reviewer authority')
    review_path = root / 'cli-review.json'
    review = json.loads(review_path.read_text()) if review_path.exists() else {}
    check(bool(review), 'independent review missing: evidence/cli-review.json')
    if review:
        check(review.get('evidence_sha256') == hashes, 'review hashes cover exact full evidence inventory')
        check(bool(review.get('reviewer')) and bool(review.get('implementer')) and
              review.get('reviewer') != review.get('implementer') and bool(review.get('reviewer_session')) and
              review.get('reviewer_session') != session, 'independent new reviewer identity')
        check(review.get('parent_session') == session, 'review parent session')
        check(len(review.get('cases', [])) == 6 and
              {(c['verb'], c['route']) for c in review.get('cases', [])} == expected, 'review matrix')
    review_cases = {(c['verb'], c['route']): c for c in review.get('cases', [])}
    mutated = False
    for index, (verb, route, prompt) in enumerate(messages, 1):
        label = f'{verb}/{route}'
        try:
            start, user = next((n, d) for n, d in users if d['message']['content'] == prompt)
            end = next((n for n, _ in users if n > start), len(parent) + 1)
            segment = [(n, d) for n, d in parent if start <= n < end]
            check(all(d.get('sessionId') == session and not d.get('isSidechain') for _, d in segment
                      if d.get('type') in ('user', 'assistant')), label + ' same parent session')
            stream_path = f'stream-{index}-{verb}-{route}.jsonl'
            stream = records(root / stream_path)
            check(all(d.get('session_id') == session for _, d in stream if 'session_id' in d), label + ' stream session')
            # Compare parent assistant blocks with the independently exported stream.
            stream_tools = {b['id']: b for _, d in stream if not d.get('parent_tool_use_id')
                            for b in blocks(d) if b.get('type') == 'tool_use'}
            stream_texts = [t for _, d in stream if not d.get('parent_tool_use_id') for t in chats(d)]
            calls = [(n, d, b) for n, d in segment if d.get('type') == 'assistant'
                     for b in blocks(d) if b.get('type') == 'tool_use']
            for n, d, b in calls:
                check(stream_tools.get(b['id']) == b, f'{label} parent:{n} stream tool cross-check')
            check(all(t in stream_texts for _, d in segment for t in chats(d)), label + ' stream chat cross-check')
            follows = [(n, d, b) for n, d, b in calls if b.get('name') == 'Bash' and
                       re.search(r'codex-audit\.sh\s+follow\s', b['input'].get('command', ''))]
            check(len(follows) == 1, label + ' exactly one parent Bash follow')
            fn, fd, fb = follows[0]
            if negative and index == len(messages):
                fb = copy.deepcopy(fb)
                fb['input']['run_in_background'] = False
                mutated = True
                print(f'NEGATIVE mutation {label} parent:{fn} tool={fb["id"]} run_in_background=false (in-memory copy)')
            check(fb['input'].get('run_in_background') is True, f'{label} parent:{fn} follow run_in_background=true')
            result = next(d for _, d in segment if any(b.get('tool_use_id') == fb['id'] for b in blocks(d)))
            task = result['toolUseResult']['backgroundTaskId']
            stdout_path = f'tasks/{task}.output'
            stdout = (root / stdout_path).read_text().splitlines()
            supervisors = [(n, d, b) for n, d, b in calls if
                           (route == 'direct' and b.get('name') == 'Bash' and re.search(
                               r'codex-audit\.sh\s+' + verb + r'\s', b['input'].get('command', ''))) or
                           (route == 'delegated' and b.get('name') == 'Agent' and
                            b['input'].get('subagent_type') == 'harness:qa-evaluator')]
            check(len(supervisors) == 1, label + ' one supervisor launch')
            sn, sd, sb = supervisors[0]
            if route == 'direct':
                sr = next(d for _, d in segment if any(b.get('tool_use_id') == sb['id'] for b in blocks(d)))
                background = (sb['input'].get('run_in_background') is True and
                              bool(sr.get('toolUseResult', {}).get('backgroundTaskId')))
                detached = detached_return(sb, sd, sr, verb)
                check(background or detached, f'{label} parent:{sn} supervisor nonblocking (background or detach return <=30s)')
                if detached:
                    print(f'{label} parent:{sn} detach_return_seconds={epoch(sr) - epoch(sd):.3f}')
            if route == 'delegated':
                check(sb['input'].get('run_in_background') is True, f'{label} parent:{sn} supervisor nonblocking')
                ar = next(d for _, d in segment if any(b.get('tool_use_id') == sb['id'] for b in blocks(d)))
                aid = ar['toolUseResult']['agentId']
                child = records(root / f'transcript/subagents/agent-{aid}.jsonl')
                check(ar['toolUseResult'].get('isAsync') is True, label + ' actual async Agent result')
                check(any(b.get('name') == 'Bash' and re.search(r'codex-audit\.sh\s+' + verb + r'\s',
                          b.get('input', {}).get('command', '')) for _, d in child for b in blocks(d)),
                      label + ' linked child executes requested verb')
            timed = []
            local_day = datetime.fromtimestamp(epoch(fd), ZoneInfo('Asia/Seoul')).date()
            for ln, line in enumerate(stdout, 1):
                m = re.match(r'^\[(\d\d:\d\d:\d\d)\] (.*)', line)
                if not m:
                    check(not relay_line(line), f'{label} {stdout_path}:{ln} relay timestamp required')
                    continue
                t = datetime.fromisoformat(str(local_day) + 'T' + m[1]).replace(tzinfo=ZoneInfo('Asia/Seoul')).timestamp()
                if timed and t < timed[-1][2]:
                    local_day += timedelta(days=1)
                    t += 86400
                timed.append((ln, line, t))
            check(len(timed) >= 2 and timed[0][2] < timed[-1][2], label + ' two distinct timestamped observations')
            observations = [(n, d) for n, d in segment if d.get('type') == 'user' and
                            isinstance(d.get('message', {}).get('content'), str) and
                            '<task-notification>' in d['message']['content'] and
                            timed[0][1] in d['message']['content']]
            check(any(timed[0][2] <= epoch(d) < timed[-1][2] for _, d in observations),
                  label + ' first stdout event observed during supervision; file growth needs reviewer')
            check(epoch(result) < timed[0][2], f'{label} parent:{fn} follow background acknowledged before first phase')
            chat = [(n, d, text) for n, d in segment for text in chats(d)]
            required = [(ln, line, t) for ln, line, t in timed if relay_line(line)]
            print(f'CASE {label} follow=parent:{fn} supervisor=parent:{sn} stdout={stdout_path} relay_lines={len(required)}')
            for ln, line, t in required:
                candidates = [n for n, d, _ in chat if 0 <= epoch(d) - t <= 15]
                check(bool(candidates), f'{label} {stdout_path}:{ln} no parent assistant text within 15s ({line})')
            # Exact summary copies and recognizable partial summaries are mechanically rejected.
            for n, d, text in chat:
                check(not re.search(ns['SUMMARY'], text) and not re.search(r'사전 측정\s*\d+/\d+', text),
                      f'{label} parent:{n} forbidden summary/intermediate chat')
            for ln, line, t in timed:
                if re.search(ns['SUMMARY'], line) or re.search(r'사전 측정\s*\d+/\d+', line):
                    body = re.sub(r'^\[[^]]+\]\s*', '', line)
                    check(not any(body in text for _, _, text in chat), f'{label} {stdout_path}:{ln} summary copied')
            rc = review_cases.get((verb, route))
            if rc:
                check(rc.get('stream') == stream_path and rc.get('stdout') == stdout_path and
                      rc.get('follow_tool_use_id') == fb['id'] and rc.get('supervisor_tool_use_id') == sb['id'],
                      label + ' review source bindings')
                phases = rc.get('phases', [])
                check(len(phases) == len(required) and {p['stdout_location'] for p in phases} ==
                      {ln for ln, _, _ in required}, label + ' exact relay_line coverage, no extras/duplicates')
                for phase in phases:
                    ln, line, t = next(x for x in required if x[0] == phase['stdout_location'])
                    n, d, text = next(x for x in chat if x[0] == phase['transcript_location'] and
                                     phase['chat_line'] and phase['chat_line'] in x[2])
                    check(phase['stdout_line'] == line and phase['stdout_at'] == t and phase['chat_at'] == epoch(d),
                          f'{label} stdout:{ln} timestamps/text derived from source')
                    check(0 <= epoch(d) - t <= 15, f'{label} stdout:{ln} -> parent:{n} relay <=15s')
                    check(phase.get('same_kind_round_conditions_result') is True,
                          f'{label} stdout:{ln} independent semantic verdict')
                for key in ('originals_authentic', 'implementation_revision_verified', 'no_progress_request',
                            'no_summary_relay_or_wakeup', 'follow_output_grew_during_supervision'):
                    check(rc.get(key) is True, label + ' reviewer: ' + key)
                check(bool(rc.get('reason')) and bool(rc.get('growth_locations')) and
                      bool(rc.get('implementation_revision')) and rc.get('review_verdict') == 'PASS',
                      label + ' independent verdict and source reasoning')
        except (KeyError, StopIteration, IndexError, ValueError, OSError, TypeError) as exc:
            check(False, label + ' invalid/missing evidence: ' + repr(exc))
    if negative:
        check(mutated, 'negative mutation reached')
        check(any('follow run_in_background=true' in f for f in failures), 'negative detected by background assertion')
    print(('FAIL' if failures else 'PASS') + f' 스킬-02 failures={len(failures)}')
    return 1 if failures else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('condition', choices=['스킬-02'])
    p.add_argument('--negative', action='store_true')
    args = p.parse_args()
    return run(HERE.parent / 'evidence', args.negative)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, StopIteration, TypeError) as exc:
        print('FAIL 스킬-02 invalid evidence: ' + repr(exc))
        sys.exit(1)
