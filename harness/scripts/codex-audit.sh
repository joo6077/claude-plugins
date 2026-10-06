#!/usr/bin/env bash
# Codex 가 계약을 쓰고(draft · revise) 구현을 판정한다(impl). 쓰는 법은 harness/README.md 의 스크립트 표.
#
# Codex 호출과 결과 파일 쓰기를 이 스크립트가 맡는다. 서브에이전트에게 감독을 직접 띄우게 했더니
# 띄우지 않고 띄웠다고 적은 일이 두 번 있었다 (qa-evaluator.md Step 7). 에이전트는 결과를 읽기만 한다.
#
# 종료 코드: 0 APPROVE · 1 REJECT · 2 BLOCKED · 3 SKIPPED(설정이 꺼짐) · 64 쓰는 법이 틀림 · 75 아직 도는 중(wait)
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
command -v python3 >/dev/null 2>&1 || { echo "codex-audit: python3 가 필요하다" >&2; exit 64; }
exec python3 - "$here" "$@" <<'PY'
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = Path(sys.argv[1])
SCRIPT = HERE / 'codex-audit.sh'
TEMPLATES = HERE.parent / 'templates' / 'codex-audit'
REFERENCES = HERE.parent / 'references'
SKILL_DOC = HERE.parent / 'skills' / 'sprint-contract' / 'SKILL.md'
EXIT = dict(APPROVE=0, REJECT=1, BLOCKED=2, SKIPPED=3)
CONDITION = re.compile(r'^- \[[ x]\] ((?:[A-Z]{2,}|[^ -~]+)-[0-9]{2})', re.M)
NARRATIVE = ('배경', '리서치 소스', 'GAP 분석', '범위 경계', '회귀 게이트')
SECRET = re.compile(r'sk-[A-Za-z0-9_-]{8,}')
# 키 사본을 지우기 전에 받은 신호로 끝나면 사본이 남는다. 신호를 예외로 바꿔 finally 를 타게 한다.
ACTIVE = []


class Stop(Exception):
    def __init__(self, category, detail=''):
        super().__init__(category)
        self.category = category
        self.detail = detail


class Interrupted(Exception):
    pass


def on_signal(signum, frame):
    raise Interrupted(signum)


def usage(message=''):
    if message:
        print('codex-audit: ' + message, file=sys.stderr)
    print('쓰는 법: codex-audit.sh draft <요구사항> <계약> | revise <계약> <지적> | impl <계약> <기준 커밋> [--detach]'
          ' | wait <감독 폴더> [초]', file=sys.stderr)
    return 64


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def scrub(text):
    return SECRET.sub('[가림]', text)


def git(repo, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True,
                          stdin=subprocess.DEVNULL, env=env)


def layout(contract):
    contract = Path(contract).resolve()
    meta = contract.parent
    if meta.name != '.harness':
        raise ValueError('계약이 .harness 폴더 안에 있지 않다: ' + str(contract))
    match = re.fullmatch(r'sprint-contract(?:-(.+))?\.md', contract.name)
    if not match:
        raise ValueError('계약 파일 이름이 sprint-contract*.md 가 아니다: ' + contract.name)
    slug = match.group(1) or 'plain'
    feedback = meta / ('sprint-feedback' + ('-' + match.group(1) if match.group(1) else '') + '.md')
    return contract, meta, slug, feedback


def settings(meta):
    path = meta / 'project.yaml'
    text = path.read_text(encoding='utf-8') if path.is_file() else ''
    found, inside = {}, False
    for line in text.splitlines():
        if re.match(r'^codex_audit:\s*(#.*)?$', line):
            inside = True
            continue
        if inside:
            if line and not line[0].isspace():
                break
            hit = re.match(r'^\s+([a-z_]+):\s*(.*?)\s*(?:#.*)?$', line)
            if hit:
                value = hit.group(2)
                if len(value) >= 2 and value[0] == value[-1] == '"':
                    # YAML 큰따옴표 안의 \uXXXX 는 글자로 푼다. 다른 도구가 경로를 json.dumps 로 적어 넣는다.
                    try:
                        value = json.loads(value)
                    except ValueError:
                        value = value[1:-1]
                elif len(value) >= 2 and value[0] == value[-1] == "'":
                    value = value[1:-1]
                found[hit.group(1)] = value
    categories = re.findall(r'^\s*-\s*id:\s*["\']?([^"\'\s#]+)', text, re.M)
    return found, categories


def supervisor_home(conf):
    if conf.get('codex_home'):
        return Path(conf['codex_home']).expanduser()
    qa = Path.home() / '.codex-qa'
    if qa.is_dir():
        return qa
    return Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex').expanduser()


def folder_model(home):
    config = home / 'config.toml'
    text = config.read_text(encoding='utf-8') if config.is_file() else ''
    hit = re.search(r'^model\s*=\s*["\']([^"\']+)', text, re.M)
    return hit.group(1) if hit else ''


def allocate(meta, slug, kind):
    root = meta / 'codex-audit' / slug
    root.mkdir(parents=True, exist_ok=True)
    taken = [int(entry.name.rsplit('-r', 1)[1]) for entry in root.glob(kind + '-r*')
             if entry.name.rsplit('-r', 1)[1].isdigit()]
    while True:
        number = max(taken, default=0) + 1
        folder = root / (kind + '-r' + str(number))
        try:
            folder.mkdir()
            return folder, number
        except FileExistsError:
            taken.append(number)


def last_verdict(report):
    lines = report.read_text(encoding='utf-8').strip().splitlines() if report.is_file() else []
    hit = re.match(r'^감독 판정: (\S+)', lines[-1]) if lines else None
    return hit.group(1) if hit else None


class Audit:
    def __init__(self, folder, verb, conf):
        self.folder = folder
        self.verb = verb
        self.conf = conf
        self.started = now()
        self.account = '확인 전'
        self.rows = []
        self.sections = []
        self.copies = []

    def section(self, title, lines):
        self.sections.append('## ' + title + '\n' + '\n'.join(lines))

    def finish(self, verdict, category=None, detail=''):
        if self.copies:
            self.section('판정 사본', self.copies)
        if category:
            cause = ['갈래: ' + category]
            if detail:
                cause.append(scrub(detail).strip()[-1500:])
            self.section('실패 원인', cause)
        head = ['시작: ' + self.started, '끝: ' + now(), '계정: ' + self.account, '단계: ' + self.verb]
        body = '\n'.join(head + self.rows) + '\n\n' + '\n\n'.join(self.sections)
        text = scrub(body).rstrip() + '\n\n감독 판정: ' + verdict + '\n'
        temp = self.folder / 'report.md.tmp'
        temp.write_text(text, encoding='utf-8')
        temp.replace(self.folder / 'report.md')
        return EXIT[verdict]


def kill_group(proc):
    for sig, grace in ((signal.SIGTERM, 2), (signal.SIGKILL, 5)):
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            return
        try:
            proc.wait(timeout=grace)
            return
        except subprocess.TimeoutExpired:
            continue


def private_home(source):
    # Codex 는 실행 중 자기 폴더에 써야 하는데 판정 격리 공간은 감독 폴더 쓰기를 막는다. 사본을 만든다.
    home = Path(tempfile.mkdtemp(prefix='codex-audit-home-'))
    home.chmod(0o700)
    auth = home / 'auth.json'
    if (source / 'auth.json').is_file():
        descriptor = os.open(auth, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, 'wb') as target:
            target.write((source / 'auth.json').read_bytes())
    if (source / 'config.toml').is_file():
        (home / 'config.toml').write_bytes((source / 'config.toml').read_bytes())
    return home


def drop_home(home, keep_thread=None, phase_dir=None):
    (home / 'auth.json').unlink(missing_ok=True)
    kept = None
    if keep_thread and phase_dir is not None:
        for rollout in sorted((home / 'sessions').rglob('*' + keep_thread + '.jsonl')):
            target = phase_dir / 'sessions' / rollout.relative_to(home / 'sessions')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(rollout), str(target))
            kept = target
    shutil.rmtree(home, ignore_errors=True)
    return kept


def codex_bin():
    chosen = os.environ.get('CODEX_BIN') or shutil.which('codex') or ''
    path = Path(chosen) if chosen else None
    if not path or not path.is_file() or not os.access(path, os.X_OK):
        raise Stop('codex-없음', 'codex 실행 파일을 찾지 못했다: ' + (chosen or 'PATH'))
    return str(path)


def login(audit, binary, source):
    home = private_home(source)
    ACTIVE.append(home)
    try:
        proc = subprocess.run([binary, 'login', 'status'], env=dict(os.environ, CODEX_HOME=str(home)),
                              stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60)
    finally:
        drop_home(home)
        ACTIVE.remove(home)
    output = proc.stdout + '\n' + proc.stderr
    hit = re.search(r'Logged in using [A-Za-z ]+?(?=\s+-|\s*$)', output, re.M)
    if proc.returncode != 0 or not hit:
        raise Stop('로그인-없음', 'codex login status 종료 코드 ' + str(proc.returncode) + ' · 폴더 ' + str(source))
    audit.account = hit.group(0).strip()


def check_shape(value, schema):
    kind = schema.get('type')
    if 'enum' in schema and value not in schema['enum']:
        return False
    if kind == 'object':
        props = schema.get('properties', {})
        return (isinstance(value, dict) and set(value) == set(props)
                and all(check_shape(value[key], props[key]) for key in props))
    if kind == 'array':
        return isinstance(value, list) and all(check_shape(item, schema['items']) for item in value)
    if kind == 'string':
        return isinstance(value, str)
    return True


def read_events(path):
    found = dict(thread='', completed=False, failed=False, message=False, errors=[])
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines() if path.is_file() else []:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        kind = event.get('type')
        if kind == 'thread.started':
            found['thread'] = event.get('thread_id', '')
        elif kind == 'turn.completed':
            found['completed'] = True
        elif kind in ('turn.failed', 'error'):
            found['failed'] = True
            error = event.get('error')
            nested = error.get('message') if isinstance(error, dict) else error
            found['errors'].append(str(event.get('message') or nested or ''))
        elif kind == 'item.completed' and (event.get('item') or {}).get('type') == 'agent_message':
            found['message'] = True
    return found


def classify(rc, events, stderr, output):
    said = ' '.join(events['errors']) + ' ' + stderr
    if rc != 0:
        if re.search(r'insufficient_quota|usage limit|quota|billing|credit', said, re.I):
            return '한도-결제'
        if re.search(r'config|unknown (field|option|argument)|unexpected argument|trusted directory|invalid schema', said, re.I):
            return '설정-오류'
        return '형식-깨짐'
    if events['failed'] or not events['completed']:
        return '형식-깨짐'
    if not output.is_file() or not output.read_text(encoding='utf-8', errors='replace').strip():
        return '형식-깨짐' if events['message'] else '빈-응답'
    return None


def run_codex(audit, binary, source, name, prompt, schema, cwd, network, effort):
    phase_dir = audit.folder / name
    phase_dir.mkdir(exist_ok=True)
    events_file, error_file, output = phase_dir / 'events.jsonl', phase_dir / 'stderr.log', phase_dir / 'answer.json'
    args = [binary, 'exec', '--json', '--skip-git-repo-check', '-s', 'workspace-write', '-C', str(cwd),
            '--output-schema', str(schema), '-o', str(output), '-c', 'model_reasoning_effort="' + effort + '"']
    if network:
        args += ['-c', 'sandbox_workspace_write.network_access=true']
    if audit.conf.get('model'):
        args += ['-m', audit.conf['model']]
    args.append(prompt)
    limit = int(os.environ.get('CODEX_AUDIT_LIMIT') or 600)
    home = private_home(source)
    ACTIVE.append(home)
    proc = None
    timed_out = False
    try:
        with events_file.open('w') as out, error_file.open('w') as err:
            proc = subprocess.Popen(args, env=dict(os.environ, CODEX_HOME=str(home)), stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err, start_new_session=True)
            ACTIVE.append(proc)
            try:
                proc.wait(timeout=limit)
            except subprocess.TimeoutExpired:
                timed_out = True
            kill_group(proc)
    finally:
        if proc is not None and proc in ACTIVE:
            kill_group(proc)
            ACTIVE.remove(proc)
        events = read_events(events_file)
        record = drop_home(home, events['thread'], phase_dir)
        ACTIVE.remove(home)
    context = {}
    if record:
        for line in record.read_text(encoding='utf-8', errors='replace').splitlines():
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if isinstance(item, dict) and item.get('type') == 'turn_context':
                context = item.get('payload') or {}
    sandbox = (context.get('sandbox_policy') or {}).get('type', '?')
    audit.rows.append('- 차례 {} 모델={} 생각={} 격리={} 기록={}'.format(
        name, context.get('model', '?'), context.get('effort', '?'), sandbox, record or '없음'))
    stderr = error_file.read_text(encoding='utf-8', errors='replace')
    category = '시간-초과' if timed_out else classify(proc.returncode, events, stderr, output)
    if not category and not record:
        category = '형식-깨짐'
    if category:
        return dict(category=category, detail=stderr[-1500:] + '\n' + ' '.join(events['errors']))
    try:
        answer = json.loads(output.read_text(encoding='utf-8'))
    except ValueError:
        return dict(category='형식-깨짐', detail='답이 JSON 으로 읽히지 않는다')
    if not check_shape(answer, json.loads(schema.read_text(encoding='utf-8'))):
        return dict(category='형식-깨짐', detail='답이 정해진 모양과 다르다')
    return dict(category=None, answer=answer)


def call(audit, binary, source, name, prompt, schema, cwd_factory, network, effort, keep=False):
    # 멈춤과 빈 응답만 새 세션으로 한 번 더 부른다. Codex 가 안에서 이미 4~5 번 다시 시도한다.
    for attempt in (1, 2):
        phase = name if attempt == 1 else name + '-again'
        cwd = cwd_factory()
        try:
            result = run_codex(audit, binary, source, phase, prompt, schema, cwd, network, effort)
        finally:
            # 판정 사본은 판정 근거라 남긴다. 시스템 임시 폴더라 운영체제가 치운다.
            if keep:
                audit.copies.append('- {}: {}'.format(phase, cwd))
            else:
                shutil.rmtree(cwd, ignore_errors=True)
        if result['category'] not in ('시간-초과', '빈-응답') or attempt == 2:
            return result


def scratch():
    return Path(tempfile.mkdtemp(prefix='codex-audit-work-'))


def fill(template, values):
    text = (TEMPLATES / template).read_text(encoding='utf-8')
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', str(value))
    return text


def save_check(text, categories):
    found = []
    allowed = set(categories) | {'Anti-patterns', 'Reusability', 'Diagnostics'}
    section = ''
    for line in text.splitlines():
        if line.startswith('## '):
            section = line[3:].strip()
            if section not in allowed and not section.startswith(NARRATIVE):
                found.append('허용 밖 헤더: ' + line)
        elif CONDITION.match(line) and (section not in allowed):
            found.append('서술 절의 조건 줄: ' + line[:80])
    declared = re.search(r'^conditions:\s*(\d+)', text, re.M)
    count = len(CONDITION.findall(text))
    if not declared or int(declared.group(1)) != count:
        found.append('조건 수 불일치: frontmatter ' + (declared.group(1) if declared else '없음') + ' · 실제 ' + str(count))
    if '[미실측]' in text:
        found.append('[미실측] 표시가 남아 있다')
    evidence = ['헤더 허용 목록 · 조건 줄 위치 · 조건 수 · 미실측 표시 검사: 위반 ' + str(len(found)) + '건']
    return found, evidence + ['- ' + item for item in found]


def install(meta, slug, measurements):
    target = meta / '.meta' / slug
    for item in measurements:
        rel = Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise Stop('형식-깨짐', '측정 묶음 경로가 묶음 폴더 밖을 가리킨다: ' + item['path'])
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(item['content'], encoding='utf-8')
        if item['content'].startswith('#!'):
            dest.chmod(0o755)


def write_contract(audit, meta, slug, contract, categories, answer):
    problems, evidence = save_check(answer['contract'], categories)
    audit.section('저장 검사', evidence)
    if problems:
        audit.section('고칠 것', ['- 전체 어디를: 계약 · 무엇으로: ' + item + ' · 어떻게 확인: 저장 검사 다시 실행'
                                 for item in problems])
        return audit.finish('REJECT')
    contract.write_text(answer['contract'], encoding='utf-8')
    install(meta, slug, answer['measurements'])
    audit.section('설치', ['- 계약: ' + str(contract), '- 측정 묶음: ' + str(meta / '.meta' / slug)])
    return audit.finish('APPROVE')


def prepare(audit, conf):
    if conf.get('mode', 'codex') != 'codex':
        raise Stop('설정-오류', 'codex_audit.mode 가 codex · off 가 아니다: ' + conf.get('mode', ''))
    binary = codex_bin()
    source = supervisor_home(conf)
    if not conf.get('model') and not folder_model(source):
        raise Stop('설정-오류', '모델 지정이 없다 — project.yaml codex_audit.model 도, ' + str(source / 'config.toml') + ' 의 model 도 없다')
    login(audit, binary, source)
    return binary, source


def draft(audit, conf, categories, contract, meta, slug, requirements):
    if not contract.is_file() or contract.stat().st_size:
        raise Stop('설정-오류', '계약 자리는 미리 선점한 빈 파일이어야 한다: ' + str(contract))
    binary, source = prepare(audit, conf)
    prompt = fill('draft.md', dict(REQUIREMENTS=requirements, SCHEMA_DOC=REFERENCES / 'contract-schema.md',
                                   SKILL_DOC=SKILL_DOC, PROJECT=meta / 'project.yaml', REPO=meta.parent,
                                   SLUG=slug, META=meta / '.meta' / slug))
    result = call(audit, binary, source, 'draft-1', prompt, TEMPLATES / 'contract.schema.json', scratch, False,
                  conf.get('effort_draft') or 'medium')
    if result['category']:
        raise Stop(result['category'], result['detail'])
    return write_contract(audit, meta, slug, contract, categories, result['answer'])


def revise(audit, conf, categories, contract, meta, slug, critique):
    if not contract.is_file():
        raise Stop('설정-오류', '계약이 없다: ' + str(contract))
    head = contract.read_text(encoding='utf-8').split('\n---', 1)[0]
    if re.search(r'^conditions_digest:', head, re.M):
        raise Stop('봉인됨', '봉인된 계약은 고치지 않는다. 바꿀 것은 sprint-amendments 파일에 쓴다')
    binary, source = prepare(audit, conf)
    shutil.copyfile(contract, audit.folder / 'previous-contract.md')
    prompt = fill('revise.md', dict(CONTRACT=contract, CRITIQUE=critique, META=meta / '.meta' / slug,
                                    SCHEMA_DOC=REFERENCES / 'contract-schema.md', PROJECT=meta / 'project.yaml'))
    result = call(audit, binary, source, 'revise-1', prompt, TEMPLATES / 'contract.schema.json', scratch, False,
                  conf.get('effort_draft') or 'medium')
    if result['category']:
        raise Stop(result['category'], result['detail'])
    return write_contract(audit, meta, slug, contract, categories, result['answer'])


def verdict_errors(answer, ids):
    rows = answer['conditions']
    got = [row['id'] for row in rows]
    if answer['verdict'] == 'RESEARCH':
        return [] if answer['questions'] else ['RESEARCH 인데 질문이 없다']
    found = []
    if sorted(got) != sorted(ids) or len(set(got)) != len(got):
        found.append('조건 번호가 계약과 다르다: 빠짐 ' + str(sorted(set(ids) - set(got))) + ' · 없는 번호 '
                     + str(sorted(set(got) - set(ids))) + ' · 겹침 ' + str(len(got) - len(set(got))))
    failed = [row for row in rows if row['verdict'] == 'FAIL']
    if (answer['verdict'] == 'APPROVE') != (not failed):
        found.append('전체 판정 ' + answer['verdict'] + ' 이 조건 판정과 맞지 않는다')
    for row in rows:
        if not row['evidence'].strip() or not row['analysis'].strip():
            found.append(row['id'] + ' 증거나 분석이 비었다')
        if row['verdict'] == 'FAIL' and not all(row['fix'][key].strip() for key in ('where', 'what', 'verify')):
            found.append(row['id'] + ' 고칠 방법 세 칸 중 빈 칸이 있다')
    return found


def judged(audit, binary, source, name, prompt, copy_factory, effort, ids):
    result = call(audit, binary, source, name, prompt, TEMPLATES / 'impl.schema.json', copy_factory, True, effort,
                  keep=True)
    if result['category']:
        raise Stop(result['category'], result['detail'])
    errors = verdict_errors(result['answer'], ids)
    if errors:
        raise Stop('형식-깨짐', '\n'.join(errors))
    return result['answer']


def previous_fixes(meta, slug, folder):
    reports = sorted((meta / 'codex-audit' / slug).glob('impl-r*/report.md'),
                     key=lambda report: int(report.parent.name.rsplit('-r', 1)[1]))
    for report in reversed([report for report in reports if report.parent != folder]):
        text = report.read_text(encoding='utf-8')
        if '## 고칠 것' in text:
            return re.findall(r'^- (\S+) 어디를:', text.split('## 고칠 것', 1)[1].split('\n## ', 1)[0], re.M)
    return []


def impl(audit, conf, contract, meta, slug, feedback, base, number):
    repo_root = git(meta.parent, 'rev-parse', '--show-toplevel').stdout.strip()
    if not repo_root:
        raise Stop('설정-오류', '계약 폴더가 git 저장소 안에 있지 않다')
    head = git(repo_root, 'rev-parse', 'HEAD').stdout.strip()
    if git(repo_root, 'rev-parse', '--verify', '-q', base + '^{commit}').returncode:
        raise Stop('설정-오류', '기준 커밋을 찾지 못했다: ' + base)
    rounds = int(conf.get('max_rounds') or 2)
    done = [entry for entry in (meta / 'codex-audit' / slug).glob('impl-r*') if entry != audit.folder
            and last_verdict(entry / 'report.md') in ('APPROVE', 'REJECT')]
    if len(done) > rounds:
        raise Stop('반복-상한', '판정 ' + str(len(done)) + '회 — 첫 판정 뒤 고쳐서 다시 받는 반복 ' + str(rounds)
                   + '회를 넘었다. 사용자 판단이 필요하다')
    binary, source = prepare(audit, conf)
    frozen = audit.folder / 'input'
    frozen.mkdir()
    shutil.copyfile(contract, frozen / 'CONTRACT.md')
    (frozen / 'DIFF.patch').write_text(git(repo_root, 'diff', base + '..' + head).stdout, encoding='utf-8')
    changed = git(repo_root, 'diff', '--name-only', base + '..' + head).stdout
    (frozen / 'CHANGED.txt').write_text(changed, encoding='utf-8')
    (frozen / 'MANIFEST.json').write_text(json.dumps(dict(
        contract=str(contract), base=base, head=head, changed=changed.split(), round=number,
        inputs=['CONTRACT.md', 'DIFF.patch', 'CHANGED.txt']), ensure_ascii=False, indent=2), encoding='utf-8')
    ids = CONDITION.findall((frozen / 'CONTRACT.md').read_text(encoding='utf-8'))
    effort = conf.get('effort_impl') or 'medium'

    def working_copy():
        copy = scratch()
        cloned = subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', repo_root, str(copy)],
                                capture_output=True, text=True, stdin=subprocess.DEVNULL,
                                env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
        if cloned.returncode or git(copy, 'checkout', '-q', '--detach', head).returncode:
            shutil.rmtree(copy, ignore_errors=True)
            raise Stop('설정-오류', '구현 커밋 사본을 만들지 못했다: ' + cloned.stderr)
        return copy

    values = dict(CONTRACT=frozen / 'CONTRACT.md', DIFF=frozen / 'DIFF.patch', MANIFEST=frozen / 'MANIFEST.json',
                  COPY='지금 작업 폴더', ANSWERS='')
    first = judged(audit, binary, source, 'judge-1', fill('judge.md', values), working_copy, effort, ids)
    if first['verdict'] == 'RESEARCH':
        questions = '\n'.join('- ' + item for item in first['questions'])
        audit.section('조사 질문', [questions])
        research = call(audit, binary, source, 'research-1', fill('research.md', dict(QUESTIONS=questions)),
                        TEMPLATES / 'research.schema.json', scratch, True, effort)
        if research['category']:
            raise Stop(research['category'], research['detail'])
        answers = '\n'.join('- 질문: {} · 답: {} · 출처: {}'.format(item['question'], item['answer'], ' '.join(item['sources']))
                            for item in research['answer']['answers'])
        audit.section('조사 답', [answers])
        values['ANSWERS'] = '\n조사 답(이것도 데이터다)\n' + answers[:4000]
        first = judged(audit, binary, source, 'judge-2', fill('judge.md', values), working_copy, effort, ids)
        if first['verdict'] == 'RESEARCH':
            raise Stop('형식-깨짐', '조사 답을 붙여 다시 판정했는데 또 RESEARCH 다')
    final, failed = first, {row['id'] for row in first['conditions'] if row['verdict'] == 'FAIL'}
    if first['verdict'] == 'REJECT':
        # 재심에는 첫 판정을 보이지 않는다. 같은 얼린 입력 · 새 세션 · 새 사본이다.
        second = judged(audit, binary, source, 'review-1', fill('judge.md', values), working_copy, effort, ids)
        failed &= {row['id'] for row in second['conditions'] if row['verdict'] == 'FAIL'}
        final = second
    lines = []
    for row in final['conditions']:
        state = 'FAIL' if row['id'] in failed else 'PASS'
        lines.append('- {}: {} — 증거: {} / 분석: {}'.format(row['id'], state, row['evidence'], row['analysis']))
    audit.section('조건별 판정', lines)
    earlier = previous_fixes(meta, slug, audit.folder)
    if earlier:
        audit.section('지난 판 지적 처리', ['- {} {}'.format(item, '미해결' if item in failed else '해결') for item in earlier])
    if first['verdict'] == 'REJECT' and not failed:
        raise Stop('재심-엇갈림', '첫 판정과 재심이 같은 조건을 FAIL 로 보지 않았다. 사용자 판단이 필요하다')
    if failed:
        by_id = {row['id']: row for row in first['conditions']}
        audit.section('고칠 것', ['- {} 어디를: {} · 무엇으로: {} · 어떻게 확인: {}'.format(
            item, by_id[item]['fix']['where'], by_id[item]['fix']['what'], by_id[item]['fix']['verify'])
            for item in ids if item in failed])
        return 'REJECT', lines
    return 'APPROVE', lines


def write_feedback(feedback, contract, verdict, number, folder, lines, fixes):
    feature = re.search(r'^feature:\s*"?(.*?)"?\s*$', contract.read_text(encoding='utf-8'), re.M)
    text = ['# Sprint Feedback', 'Feature: ' + (feature.group(1) if feature else contract.stem),
            'Evaluated: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'Verdict: ' + verdict,
            'Iteration: ' + str(number), 'Evaluator: codex-audit.sh', '', '## Codex Audit',
            '- 감독 폴더: ' + str(folder), '- 감독 판정: ' + verdict, '', '## Results', *lines]
    if fixes:
        text += ['', '## 고칠 것', *fixes]
    feedback.write_text(scrub('\n'.join(text)) + '\n', encoding='utf-8')


def run(verb, folder, number, args):
    contract, meta, slug, feedback = layout(args[1] if verb == 'draft' else args[0])
    conf, categories = settings(meta)
    audit = Audit(folder, verb, conf)
    lines = []
    try:
        if verb == 'draft':
            return draft(audit, conf, categories, contract, meta, slug, Path(args[0]).resolve())
        if verb == 'revise':
            return revise(audit, conf, categories, contract, meta, slug, Path(args[1]).resolve())
        verdict, lines = impl(audit, conf, contract, meta, slug, feedback, args[1], number)
        code = audit.finish(verdict)
    except Stop as stop:
        code = audit.finish('BLOCKED', stop.category, stop.detail)
        verdict = 'BLOCKED'
    except Interrupted:
        audit.finish('BLOCKED', '중단됨', '신호를 받아 멈췄다')
        raise
    if verb == 'impl':
        report = (folder / 'report.md').read_text(encoding='utf-8')
        fixes = re.findall(r'^- \S+ 어디를: .*$', report.split('## 고칠 것', 1)[1], re.M) if '## 고칠 것' in report else []
        write_feedback(feedback, contract, verdict, number, folder, lines, fixes)
    return code


def wait(args):
    if not args or len(args) > 2:
        return usage('wait 에는 감독 폴더가 필요하다')
    folder = Path(args[0])
    if len(args) == 2 and not args[1].isdigit():
        return usage('기다릴 초는 0 이상의 정수다')
    if not folder.is_dir():
        return usage('감독 폴더가 없다: ' + str(folder))
    deadline = time.monotonic() + int(args[1] if len(args) == 2 else 540)
    while True:
        verdict = last_verdict(folder / 'report.md')
        if verdict in EXIT:
            print('감독 판정: ' + verdict)
            return EXIT[verdict]
        pid = (folder / 'pid').read_text().strip() if (folder / 'pid').is_file() else ''
        alive = False
        if pid.isdigit():
            try:
                os.kill(int(pid), 0)
                alive = True
            except (ProcessLookupError, PermissionError):
                alive = False
        if not alive and not (folder / 'report.md').exists():
            print('감독 판정: BLOCKED')
            return EXIT['BLOCKED']
        if time.monotonic() >= deadline:
            print('RUNNING ' + str(folder))
            return 75
        time.sleep(0.5)


def main(argv):
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, on_signal)
    if argv and argv[0] == '__run':
        folder = Path(argv[1])
        (folder / 'pid').write_text(str(os.getpid()))
        return run(argv[2], folder, int(argv[3]), argv[4:])
    detach = '--detach' in argv
    argv = [item for item in argv if item != '--detach']
    if not argv:
        return usage()
    verb, args = argv[0], argv[1:]
    if verb == 'wait':
        return wait(args)
    if verb not in ('draft', 'revise', 'impl') or len(args) != 2:
        return usage('부속 명령과 인자 둘이 필요하다')
    try:
        contract, meta, slug, _ = layout(args[1] if verb == 'draft' else args[0])
    except ValueError as error:
        return usage(str(error))
    if settings(meta)[0].get('mode') == 'off':
        print('감독 판정: SKIPPED (codex_audit.mode: off)')
        return EXIT['SKIPPED']
    folder, number = allocate(meta, slug, 'impl' if verb == 'impl' else 'draft')
    if detach:
        log = (folder / 'run.log').open('w')
        child = subprocess.Popen(['bash', str(SCRIPT), '__run', str(folder), verb, str(number), *args],
                                 stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
        (folder / 'pid').write_text(str(child.pid))
        print(folder)
        return 0
    code = run(verb, folder, number, args)
    print((folder / 'report.md').read_text(encoding='utf-8').strip().splitlines()[-1])
    print(folder)
    return code


def cleanup():
    for item in reversed(ACTIVE):
        if isinstance(item, subprocess.Popen):
            kill_group(item)
        else:
            (item / 'auth.json').unlink(missing_ok=True)
            shutil.rmtree(item, ignore_errors=True)


status = EXIT['BLOCKED']
try:
    status = main(sys.argv[2:])
except Interrupted as stopped:
    cleanup()
    status = 128 + stopped.args[0]
finally:
    cleanup()
sys.exit(status)
PY
