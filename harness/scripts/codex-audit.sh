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
import gzip
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

HERE = Path(sys.argv[1])
SCRIPT = HERE / 'codex-audit.sh'
TEMPLATES = HERE.parent / 'templates' / 'codex-audit'
REFERENCES = HERE.parent / 'references'
SKILL_DOC = HERE.parent / 'skills' / 'sprint-contract' / 'SKILL.md'
EXIT = dict(APPROVE=0, REJECT=1, BLOCKED=2, SKIPPED=3)
CONDITION = re.compile(r'^- \[[ x]\] ((?:[A-Z]{2,}|[^ -~]+)-[0-9]{2})', re.M)
NARRATIVE = ('배경', '리서치 소스', 'GAP 분석', '범위 경계', '회귀 게이트')
SECRET = re.compile(r'(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{8,}')
KNOWN_KEYS = []
MODELS_URL = 'https://api.openai.com/v1/models'
MODELS_MEMORY = 'codex-audit-models.json'
USAGE_LOG = 'codex-audit-usage.jsonl'
PRICES = TEMPLATES / 'prices.json'
PROFILE = 'codex-audit-judge'
POLL = 0.25
# 키 사본을 지우기 전에 받은 신호로 끝나면 사본이 남는다. 신호를 예외로 바꿔 finally 를 타게 한다.
ACTIVE = []
# 감독 하나가 만드는 임시 폴더를 한 뿌리 아래 모은다. 판정 사본 · 측정이 남긴 파일이 하루 72GB 쌓인 적이 있다.
TEMP_ROOT = []


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
          ' | wait <감독 폴더> [초] | follow <감독 폴더|계약> [--idle-seconds N] [--wait-seconds N]'
          ' [--summary-seconds N] [--relay] | models | usage', file=sys.stderr)
    return 64


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def scrub(text):
    for key in KNOWN_KEYS:
        text = text.replace(key, '[가림]')
    return SECRET.sub('[가림]', text)


def remember_key(home):
    # 모양 규칙은 앞에 글자가 붙은 키를 놓친다(prefixsk-…). 감독 계정의 실제 키는 앞뒤와 상관없이 가린다.
    try:
        key = json.loads((home / 'auth.json').read_text(encoding='utf-8')).get('OPENAI_API_KEY')
    except (OSError, ValueError, AttributeError):
        return
    if isinstance(key, str) and len(key) >= 8 and key not in KNOWN_KEYS:
        KNOWN_KEYS.append(key)


def plain_number(text):
    # str.isdigit 은 ² · ٣ 같은 글자도 참이라 int() 가 터진다. 0~9 만 숫자로 받는다.
    return re.fullmatch(r'[0-9]+', text) is not None


def span(seconds):
    seconds = int(round(seconds))
    return '{}분 {}초'.format(*divmod(seconds, 60)) if seconds >= 60 else '{}초'.format(seconds)


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
             if plain_number(entry.name.rsplit('-r', 1)[1])]
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
        self.costs = []
        self.prices = load_prices()
        self.repo = ''
        self.slug = ''

    def note(self, kind, **fields):
        # follow 가 읽는 진행 기록. 사람이 여는 파일이 아니다.
        fields.update(kind=kind, at=time.time())
        with (self.folder / 'progress.jsonl').open('a', encoding='utf-8') as out:
            out.write(scrub(json.dumps(fields, ensure_ascii=False)) + '\n')

    def section(self, title, lines):
        self.sections.append('## ' + title + '\n' + '\n'.join(lines))

    def finish(self, verdict, category=None, detail=''):
        if self.costs:
            lines = ['- {} · 모델 {} · 입력 {:,} (캐시 {:,}) · 출력 {:,} · {}'.format(name, model, *tokens, money(usd))
                     for name, model, tokens, usd in self.costs]
            known = [usd for *_, usd in self.costs if usd is not None]
            unknown = len(self.costs) - len(known)
            lines.append('- 합계 {}{}'.format(money(sum(known)), ' · 단가 모름 차례 {}개 빠짐'.format(unknown) if unknown else ''))
            self.section('비용', lines)
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
        self.note('final', verdict=verdict)
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


def temp_dir(kind):
    if not TEMP_ROOT:
        root = Path(tempfile.mkdtemp(prefix='codex-audit-'))
        TEMP_ROOT.append(root)
        ACTIVE.append(root)
    return Path(tempfile.mkdtemp(prefix=kind + '-', dir=TEMP_ROOT[0]))


def private_home(source):
    # Codex 는 실행 중 자기 폴더에 써야 하는데 판정 격리 공간은 감독 폴더 쓰기를 막는다. 사본을 만든다.
    home = temp_dir('home')
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
    found = dict(thread='', completed=False, failed=False, message=False, errors=[], usage={})
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
            found['usage'] = event.get('usage') if isinstance(event.get('usage'), dict) else {}
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


def turn_label(name):
    base, again = (name[:-len('-again')], ' · 다시') if name.endswith('-again') else (name, '')
    kind, _, number = base.rpartition('-')
    labels = dict(judge='판정 ' + number + '차', review='재심', research='조사', draft='계약 작성', revise='계약 수정')
    return labels.get(kind, base) + again


def turn_result(result):
    if result['category']:
        return result['category'].replace('-', ' ')
    answer = result['answer']
    if answer.get('verdict') == 'RESEARCH':
        return 'RESEARCH · 질문 {}개'.format(len(answer['questions']))
    if 'conditions' in answer:
        failed = sum(row['verdict'] == 'FAIL' for row in answer['conditions'])
        return '{} · PASS {} · FAIL {}'.format(answer['verdict'], len(answer['conditions']) - failed, failed)
    return '답 받음'


def copy_scrubbed(stream, out):
    for raw in iter(stream.readline, b''):
        out.write(scrub(raw.decode('utf-8', errors='replace')))
        out.flush()


def scrub_file(path):
    if path and path.is_file():
        path.write_text(scrub(path.read_text(encoding='utf-8', errors='replace')), encoding='utf-8')


def read_answer(proc, timed_out, events, stderr, output, record, schema):
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


def judge_profile(frozen, tmp):
    # :root 를 막고 여는 자리만 적는다. python · node 는 설치 폴더와 그 라이브러리를 읽어야 돈다 (2026-10-07 실측).
    reads = {str(frozen)}
    for tool in ('python3', 'node', 'git', 'bash'):
        found = shutil.which(tool)
        if found:
            reads.add(str(Path(os.path.realpath(found)).parents[1]))
    for entry in os.environ.get('PATH', '').split(os.pathsep):
        real = os.path.realpath(entry) if entry else ''
        if real and real not in ('/', str(Path.home())) and Path(real).is_dir():
            reads.add(real)
    reads.update(folder for folder in ('/opt/homebrew', '/usr/local', '/System/Library/OpenSSL',
                                       '/Library/Developer/CommandLineTools') if Path(folder).is_dir())
    table = 'permissions.' + PROFILE
    lines = ['', '[' + table + ']', 'extends = ":workspace"', '', '[' + table + '.filesystem]',
             '":root" = "deny"', '":minimal" = "read"', '":slash_tmp" = "deny"']
    lines += [json.dumps(folder) + ' = "read"' for folder in sorted(reads)]
    lines += [json.dumps(str(tmp)) + ' = "write"', '', '[' + table + '.network]', 'enabled = false']
    return '\n'.join(lines) + '\n'


def load_prices():
    try:
        return json.loads(PRICES.read_text(encoding='utf-8')).get('models', {})
    except (OSError, ValueError, AttributeError):
        return {}


def turn_cost(model, usage, prices):
    rate = prices.get(model)
    tokens = [int(usage.get(key) or 0) for key in ('input_tokens', 'cached_input_tokens', 'output_tokens')]
    if not isinstance(rate, dict):
        return tokens, None
    fresh, cached, output = tokens[0] - tokens[1], tokens[1], tokens[2]
    return tokens, (fresh * rate['input'] + cached * rate['cached_input'] + output * rate['output']) / 1e6


def money(usd):
    return '단가 모름' if usd is None else '{:.2f}달러'.format(usd)


def read_usage(home):
    rows, unreadable = [], 0
    log = home / USAGE_LOG
    for line in log.read_text(encoding='utf-8', errors='replace').splitlines() if log.is_file() else []:
        try:
            row = json.loads(line)
            row['usd'] = None if row.get('usd') is None else float(row['usd'])
            if isinstance(row['usd'], bool) or not isinstance(row.get('date'), str):
                raise TypeError
        except (ValueError, TypeError, AttributeError):
            unreadable += 1
            continue
        rows.append(row)
    return rows, unreadable


def spent(rows, prefix):
    return sum(row['usd'] or 0 for row in rows if row['date'].startswith(prefix))


def record_usage(audit, source, name, model, tokens, usd):
    row = dict(date=datetime.date.today().isoformat(), repo=audit.repo, slug=audit.slug, verb=audit.verb, turn=name,
               model=model, input=tokens[0], cached=tokens[1], output=tokens[2], usd=None if usd is None else round(usd, 6))
    with (source / USAGE_LOG).open('a', encoding='utf-8') as out:
        out.write(json.dumps(row, ensure_ascii=False) + '\n')


def check_budget(conf, source):
    raw = conf.get('daily_budget_usd') or ''
    if not raw:
        return
    try:
        limit = float(raw)
    except ValueError:
        raise Stop('설정-오류', 'codex_audit.daily_budget_usd 가 숫자가 아니다: ' + raw)
    rows, unreadable = read_usage(source)
    today = spent(rows, datetime.date.today().isoformat())
    note = ' · 못 읽은 줄 {}'.format(unreadable) if unreadable else ''
    if today >= limit:
        raise Stop('한도-예산', '오늘 {} ≥ 하루 상한 {} — Codex 를 부르지 않았다 ({}){}'.format(
            money(today), money(limit), source / USAGE_LOG, note))


def pack(record):
    packed = record.with_name(record.name + '.gz')
    with record.open('rb') as raw, gzip.open(packed, 'wb') as out:
        shutil.copyfileobj(raw, out)
    record.unlink()
    return packed


def run_codex(audit, binary, source, name, prompt, schema, cwd, network, effort, judge=False):
    phase_dir = audit.folder / name
    phase_dir.mkdir(exist_ok=True)
    events_file, error_file, output = phase_dir / 'events.jsonl', phase_dir / 'stderr.log', phase_dir / 'answer.json'
    tmp = temp_dir('tmp')
    home = private_home(source)
    ACTIVE.append(home)
    args = [binary, 'exec', '--json', '--skip-git-repo-check', '-C', str(cwd),
            '--output-schema', str(schema), '-o', str(output), '-c', 'model_reasoning_effort="' + effort + '"']
    if judge:
        # -s 나 sandbox_workspace_write 가 하나라도 있으면 권한 프로필 대신 옛 방식이 이긴다 (codex 0.160 문서).
        with (home / 'config.toml').open('a', encoding='utf-8') as config:
            config.write(judge_profile(audit.folder / 'input', tmp))
        args += ['-c', 'default_permissions="' + PROFILE + '"']
    else:
        args[4:4] = ['-s', 'workspace-write']
        if network:
            args += ['-c', 'sandbox_workspace_write.network_access=true']
    model = os.environ.get('CODEX_AUDIT_MODEL') or audit.conf.get('model')
    if model:
        args += ['-m', model]
    args.append(prompt.replace('{{WORKDIR}}', str(cwd)).replace('{{TMPDIR}}', str(tmp)))
    # 계약 작성은 8~16분 걸린다(2026-10-06~07 실측). 판정 상한 600초를 같이 쓰면 다 쓴 일을 버린다.
    limit_key, default = ('CODEX_AUDIT_DRAFT_LIMIT', 1500) if name.startswith(('draft', 'revise')) else ('CODEX_AUDIT_LIMIT', 600)
    limit = int(os.environ.get(limit_key) or default)
    # follow 는 이 임시 폴더의 세션 기록이 자라는지로 생각 중과 멈춤을 가른다.
    audit.note('turn-start', name=name, label=turn_label(name), effort=effort, home=str(home),
               model=model or folder_model(source) or '?')
    began = time.monotonic()
    proc = None
    timed_out = False
    env = dict(os.environ, CODEX_HOME=str(home), TMPDIR=str(tmp), TMP=str(tmp), TEMP=str(tmp))
    try:
        with events_file.open('w', encoding='utf-8') as out, error_file.open('w') as err:
            proc = subprocess.Popen(args, env=env, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.PIPE, stderr=err, start_new_session=True)
            ACTIVE.append(proc)
            # 명령 사건에 키가 실려 와도 파일에는 가린 줄만 남는다. follow 가 이 파일을 실행 중에 읽는다.
            copier = threading.Thread(target=copy_scrubbed, args=(proc.stdout, out), daemon=True)
            copier.start()
            try:
                proc.wait(timeout=limit)
            except subprocess.TimeoutExpired:
                timed_out = True
            kill_group(proc)
            copier.join(5)
    finally:
        if proc is not None and proc in ACTIVE:
            kill_group(proc)
            ACTIVE.remove(proc)
        events = read_events(events_file)
        record = drop_home(home, events['thread'], phase_dir)
        ACTIVE.remove(home)
        shutil.rmtree(tmp, ignore_errors=True)
        scrub_file(record)
        scrub_file(error_file)
    context = {}
    if record:
        for line in record.read_text(encoding='utf-8', errors='replace').splitlines():
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if isinstance(item, dict) and item.get('type') == 'turn_context':
                context = item.get('payload') or {}
        record = pack(record)
    used = context.get('model') or model or folder_model(source) or '?'
    sandbox = (context.get('sandbox_policy') or {}).get('type', PROFILE if judge else '?')
    audit.rows.append('- 차례 {} 모델={} 생각={} 격리={} 상한 {}초 기록={}'.format(
        name, used, context.get('effort', '?'), sandbox, limit, record or '없음'))
    cost = ''
    if events['usage']:
        tokens, usd = turn_cost(used, events['usage'], audit.prices)
        cost = money(usd)
        audit.costs.append((name, used, tokens, usd))
        record_usage(audit, source, name, used, tokens, usd)
    stderr = error_file.read_text(encoding='utf-8', errors='replace')
    result = read_answer(proc, timed_out, events, stderr, output, record, schema)
    audit.note('turn-end', name=name, result=turn_result(result), seconds=time.monotonic() - began, cost=cost)
    return result


def call(audit, binary, source, name, prompt, schema, cwd_factory, network, effort, judge=False):
    # 빈 응답만 새 세션으로 한 번 더 부른다. 시간 초과를 다시 부르면 같은 만큼 또 쓰고 또 끊긴다
    # (2026-10-07 계약 작성 10분 두 번). Codex 가 안에서 이미 4~5 번 다시 시도한다.
    for attempt in (1, 2):
        phase = name if attempt == 1 else name + '-again'
        cwd = cwd_factory()
        try:
            result = run_codex(audit, binary, source, phase, prompt, schema, cwd, network, effort, judge)
        finally:
            shutil.rmtree(cwd, ignore_errors=True)
        if result['category'] != '빈-응답' or attempt == 2:
            return result
        audit.note('retry', name=name, reason=result['category'].replace('-', ' '))


def scratch():
    return temp_dir('work')


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
    audit.note('saved', verb=audit.verb, problems=len(problems), verdict='REJECT' if problems else 'APPROVE')
    if problems:
        audit.section('고칠 것', ['- 전체 어디를: 계약 · 무엇으로: ' + item + ' · 어떻게 확인: 저장 검사 다시 실행'
                                 for item in problems])
        return audit.finish('REJECT')
    contract.write_text(answer['contract'], encoding='utf-8')
    install(meta, slug, answer['measurements'])
    audit.section('설치', ['- 계약: ' + str(contract), '- 측정 묶음: ' + str(meta / '.meta' / slug)])
    return audit.finish('APPROVE')


def prepare(audit, conf):
    if conf.get('mode', 'off') != 'codex':
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
    result = call(audit, binary, source, name, prompt, TEMPLATES / 'impl.schema.json', copy_factory, False, effort,
                  judge=True)
    if result['category']:
        raise Stop(result['category'], result['detail'])
    errors = verdict_errors(result['answer'], ids)
    if errors:
        raise Stop('형식-깨짐', '\n'.join(errors))
    return result['answer']


def premeasure(audit, template, ids, frozen, copy_factory):
    # 판정 격리 안에서는 ps 와 겹친 격리가 막힌다. 그런 측정은 판정 전에 격리 밖에서 한 번 돌려 기록으로 넘긴다.
    limit = int(os.environ.get('CODEX_AUDIT_LIMIT') or 600)
    folder = frozen / 'premeasure'
    folder.mkdir()
    copy = copy_factory()
    tmp = temp_dir('tmp')
    env = dict(os.environ, TMPDIR=str(tmp), TMP=str(tmp), TEMP=str(tmp))
    records, summary = [], ['condition\texit_code\tlast_line']
    began = time.monotonic()
    try:
        for number, item in enumerate(ids, 1):
            started = time.monotonic()
            command = template.replace('{id}', item)
            with tempfile.TemporaryFile() as sink:
                proc = subprocess.Popen(['bash', '-c', command], cwd=copy, env=env, stdin=subprocess.DEVNULL, stdout=sink,
                                        stderr=subprocess.STDOUT, start_new_session=True)
                ACTIVE.append(proc)
                timed_out = False
                try:
                    proc.wait(timeout=limit)
                except subprocess.TimeoutExpired:
                    timed_out = True
                kill_group(proc)
                ACTIVE.remove(proc)
                sink.seek(0)
                output = scrub(sink.read().decode('utf-8', errors='replace'))[-200000:]
            record = dict(id=item, command=command, exit_code=proc.returncode, output=output, timed_out=timed_out)
            name = 'premeasure/{:02d}.json'.format(number)
            (frozen / name).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
            records.append(name)
            last = output.splitlines()[-1] if output.splitlines() else ''
            summary.append('{}\t{}\t{}'.format(item, proc.returncode, last.replace('\t', ' ')))
            audit.note('premeasure', number=number, total=len(ids), id=item, code=proc.returncode,
                       timed_out=timed_out, seconds=time.monotonic() - started)
    finally:
        shutil.rmtree(copy, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)
    audit.note('premeasure-end', total=len(ids), seconds=time.monotonic() - began)
    (folder / 'summary.tsv').write_text('\n'.join(summary) + '\n', encoding='utf-8')
    return dict(records=records, summary='premeasure/summary.tsv')


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
    probe = subprocess.run([binary, 'sandbox', '--help'], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60)
    if '--permission-profile' not in probe.stdout + probe.stderr:
        raise Stop('설정-오류', '설치된 codex 가 권한 프로필(--permission-profile)을 지원하지 않는다 — 판정 격리를 걸 수 없어 '
                   '판정하지 않는다. codex 를 올린 뒤 다시 부른다')
    frozen = audit.folder / 'input'
    frozen.mkdir()
    shutil.copyfile(contract, frozen / 'CONTRACT.md')
    amendments = meta / feedback.name.replace('sprint-feedback', 'sprint-amendments', 1)
    if amendments.is_file():
        shutil.copyfile(amendments, frozen / 'AMENDMENTS.md')
    # 계약 폴더(.harness)의 증거 · 대화 기록이 판정 자료를 수 MB 로 키워 판정 한 번이 120만 토큰을 읽었다.
    # 그 폴더는 바뀐 파일 목록만 싣고, 내용은 판정 사본에서 열게 한다.
    harness_dir = os.path.relpath(meta, repo_root)
    body = git(repo_root, 'diff', base + '..' + head, '--', '.', ':(exclude)' + harness_dir).stdout
    listed = git(repo_root, 'diff', '--stat=200', base + '..' + head, '--', harness_dir).stdout
    if listed.strip():
        body += '\n# ' + harness_dir + '/ 아래 변경은 목록만 싣는다. 내용은 판정 사본의 같은 경로에서 연다.\n' + listed
    (frozen / 'DIFF.patch').write_text(body, encoding='utf-8')
    changed = git(repo_root, 'diff', '--name-only', base + '..' + head).stdout
    (frozen / 'CHANGED.txt').write_text(changed, encoding='utf-8')
    inputs = ['CONTRACT.md'] + (['AMENDMENTS.md'] if amendments.is_file() else []) + ['DIFF.patch', 'CHANGED.txt']
    ids = []
    for name in inputs[:2]:
        if name.endswith('.md'):
            ids += [item for item in CONDITION.findall((frozen / name).read_text(encoding='utf-8')) if item not in ids]
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

    measured = premeasure(audit, conf['premeasure'], ids, frozen, working_copy) if conf.get('premeasure') else None
    (frozen / 'MANIFEST.json').write_text(json.dumps(dict(
        contract=str(contract), base=base, head=head, changed=changed.split(), round=number,
        inputs=inputs, premeasure=measured), ensure_ascii=False, indent=2), encoding='utf-8')
    values = dict(CONTRACT=frozen / 'CONTRACT.md', DIFF=frozen / 'DIFF.patch', MANIFEST=frozen / 'MANIFEST.json',
                  INPUT=frozen, ANSWERS='', AMENDMENTS='', PREMEASURE='')
    if amendments.is_file():
        values['AMENDMENTS'] = '\n- 계약 개정(조건이 더해지거나 읽는 법이 바뀌었다. 계약과 함께 읽는다): ' + str(frozen / 'AMENDMENTS.md')
    if measured:
        values['PREMEASURE'] = fill('premeasure.md', dict(SUMMARY=frozen / measured['summary'], IDS=' · '.join(ids))).strip()
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


class Lookup(Exception):
    pass


def gpt_models(home, url, limit):
    auth = home / 'auth.json'
    if not auth.is_file():
        raise Lookup('감독 계정 인증 파일이 없다 (' + str(auth) + ')')
    try:
        key = json.loads(auth.read_text(encoding='utf-8')).get('OPENAI_API_KEY')
    except ValueError:
        raise Lookup('감독 계정 인증 파일을 읽지 못했다')
    if not key:
        raise Lookup('감독 계정이 OpenAI 키 로그인이 아니다')
    request = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + key})
    try:
        with urllib.request.urlopen(request, timeout=limit) as response:
            body = response.read()
    except urllib.error.HTTPError as error:
        raise Lookup('모델 목록 응답 ' + str(error.code))
    except (urllib.error.URLError, OSError) as error:
        reason = getattr(error, 'reason', error)
        if isinstance(reason, TimeoutError) or 'timed out' in str(reason):
            raise Lookup('모델 목록 조회가 {:g}초 안에 끝나지 않았다'.format(limit))
        raise Lookup('모델 목록에 연결하지 못했다')
    try:
        return [item['id'] for item in json.loads(body)['data']]
    except (ValueError, KeyError, TypeError):
        raise Lookup('모델 목록 응답을 읽지 못했다')


def latest_codex(limit):
    npm = shutil.which('npm')
    if not npm:
        raise Lookup('npm 이 없어 최신 Codex 판을 못 본다')
    try:
        proc = subprocess.run([npm, 'view', '@openai/codex', 'version'], capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=limit)
    except subprocess.TimeoutExpired:
        raise Lookup('npm 조회가 {:g}초 안에 끝나지 않았다'.format(limit))
    found = re.search(r'\d+\.\d+\.\d+', proc.stdout)
    if proc.returncode or not found:
        raise Lookup('npm 최신 판 조회 실패 (종료 ' + str(proc.returncode) + ')')
    return found.group(0)


def installed_codex(limit):
    try:
        proc = subprocess.run([codex_bin(), '--version'], capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, timeout=limit)
    except (Stop, OSError, subprocess.TimeoutExpired):
        return '?'
    found = re.search(r'\d+\.\d+\.\d+', proc.stdout)
    return found.group(0) if found else '?'


def version_key(text):
    return tuple(int(part) for part in text.split('.')) if re.fullmatch(r'\d+\.\d+\.\d+', text or '') else None


def discover(home, model):
    # 새 소식만 알린다. 감독 모델은 바꾸지 않는다 — 바꿀지는 보고를 받은 사람이 정한다.
    limit = float(os.environ.get('CODEX_AUDIT_CHECK_TIMEOUT') or 10)
    url = os.environ.get('CODEX_AUDIT_MODELS_URL') or MODELS_URL
    jobs = dict(models=lambda: gpt_models(home, url, limit), latest=lambda: latest_codex(limit),
                installed=lambda: installed_codex(limit))
    found = {}

    def collect(name):
        try:
            found[name] = jobs[name]()
        except Lookup as error:
            found[name] = Lookup(str(error))
        except Exception as error:
            found[name] = Lookup(type(error).__name__)
    threads = [threading.Thread(target=collect, args=(name,), daemon=True) for name in jobs]
    for thread in threads:
        thread.start()
    deadline = time.monotonic() + limit + 0.5
    for thread in threads:
        thread.join(max(0, deadline - time.monotonic()))
    for name, late in (('models', '모델 목록'), ('latest', 'npm')):
        result = found.get(name, Lookup(late + ' 조회가 {:g}초 안에 끝나지 않았다'.format(limit)))
        if isinstance(result, Lookup):
            return dict(ok=False, news=['모델 확인 못 함: ' + scrub(str(result))], status='')
    installed = found.get('installed', '?')
    gpt = sorted({item for item in found['models'] if item.startswith('gpt-')})
    latest = found['latest']
    memory_file = home / MODELS_MEMORY
    try:
        memory = json.loads(memory_file.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        memory = None
    news = []
    if isinstance(memory, dict):
        added = [item for item in gpt if item not in memory.get('models', [])]
        if added:
            news.append('새 모델: ' + ', '.join(added) + ' (지금 감독 모델 ' + model + ')')
        seen = version_key(memory.get('latest'))
        if version_key(installed) and version_key(latest) > version_key(installed) and (not seen or version_key(latest) > seen):
            news.append('새 Codex 판: ' + latest + ' (설치 ' + installed + ')')
        known = set(memory.get('models', [])) | set(gpt)
        if seen and seen > version_key(latest):
            latest_kept = memory['latest']
        else:
            latest_kept = latest
    else:
        known, latest_kept = set(gpt), latest
    temp = memory_file.with_name(MODELS_MEMORY + '.tmp')
    temp.write_text(json.dumps(dict(models=sorted(known), latest=latest_kept, checked=now()), ensure_ascii=False,
                               indent=2), encoding='utf-8')
    temp.replace(memory_file)
    status = '감독 모델 {} · 설치 Codex {} · 최신 {} · GPT 모델 {}개'.format(model, installed, latest, len(gpt))
    return dict(ok=True, news=news, status=status)


def nearest_meta():
    for folder in (Path.cwd(), *Path.cwd().parents):
        if (folder / '.harness').is_dir():
            return folder / '.harness'
    return None


def models(args):
    if args:
        return usage('models 는 인자를 받지 않는다')
    meta = nearest_meta()
    conf = settings(meta)[0] if meta else {}
    home = supervisor_home(conf)
    found = discover(home, conf.get('model') or folder_model(home) or '?')
    for line in found['news'] + ([found['status']] if found['status'] else []):
        print(line)
    return 0 if found['ok'] else 2


def usage_report(args):
    if args:
        return usage('usage 는 인자를 받지 않는다')
    meta = nearest_meta()
    home = supervisor_home(settings(meta)[0] if meta else {})
    rows, unreadable = read_usage(home)
    today = datetime.date.today()
    month = [row for row in rows if row['date'].startswith(today.strftime('%Y-%m'))]
    print('오늘 ({}) {}'.format(today.isoformat(), money(spent(rows, today.isoformat()))))
    print('이번 달 ({}) {}'.format(today.strftime('%Y-%m'), money(spent(month, ''))))
    for repo in sorted({row.get('repo') or '?' for row in month}):
        print('- {} {}'.format(repo, money(spent([row for row in month if (row.get('repo') or '?') == repo], ''))))
    if unreadable:
        print('못 읽은 줄 {} ({})'.format(unreadable, home / USAGE_LOG))
    return 0


def condition_count(contract, feedback):
    amendments = contract.parent / feedback.name.replace('sprint-feedback', 'sprint-amendments', 1)
    ids = set()
    for path in (contract, amendments):
        if path.is_file():
            ids |= set(CONDITION.findall(path.read_text(encoding='utf-8')))
    return len(ids)


def run(verb, folder, number, args):
    contract, meta, slug, feedback = layout(args[1] if verb == 'draft' else args[0])
    conf, categories = settings(meta)
    home = supervisor_home(conf)
    remember_key(home)
    audit = Audit(folder, verb, conf)
    audit.repo, audit.slug = str(meta.parent), slug
    found = discover(home, conf.get('model') or folder_model(home) or '?')
    for line in found['news']:
        audit.note('notice', text=line)
    audit.section('모델 확인', found['news'] + ([found['status']] if found['status'] else []))
    audit.note('start', verb=verb, folder=folder.name, conditions=condition_count(contract, feedback))
    lines = []
    try:
        check_budget(conf, home)
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
    if len(args) == 2 and not plain_number(args[1]):
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
        if plain_number(pid):
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


class Tail:
    """덧붙여 쓰이는 파일에서 끝난 줄만 꺼낸다. 반쯤 쓰인 줄은 다음 번에 잇는다."""

    def __init__(self, path):
        self.path, self.offset, self.rest = path, 0, b''

    def records(self):
        try:
            with self.path.open('rb') as source:
                source.seek(self.offset)
                data = source.read()
        except OSError:
            return []
        self.offset += len(data)
        *complete, self.rest = (self.rest + data).split(b'\n')
        found = []
        for line in complete:
            try:
                item = json.loads(line.decode('utf-8', errors='replace'))
            except ValueError:
                continue
            if isinstance(item, dict):
                found.append(item)
        return found


def say(text):
    print('[' + datetime.datetime.now().strftime('%H:%M:%S') + '] ' + scrub(text), flush=True)


def command_kind(command):
    text = command if isinstance(command, str) else ' '.join(map(str, command or []))
    text = re.sub(r"^\S*(?:ba|z)?sh\s+-l?c\s+", '', text).strip('\'"')
    # 따옴표 안 글자와 heredoc 본문은 셸이 실행하는 명령이 아니다. 그 안의 > 나 .sh 로 분류가 뒤집혔다.
    bare = re.sub(r"'[^'\n]*'|\"[^\"\n]*\"", "''", text)
    first = bare.split('\n', 1)[0]
    if re.search(r'(?<![0-9&>])>>?\s*(?!/dev/null)[^\s&]|(?:^|[;&|]\s*)(?:tee|cp|mv|rm|mkdir|touch|chmod|apply_patch)\b|\bsed\s+-i', first):
        return '파일 쓰기'
    programs = [segment.split()[0].rsplit('/', 1)[-1] for segment in re.split(r'[;&|\n]+', bare) if segment.split()]
    if any(re.fullmatch(r'python3?|node|bash|sh|zsh|pytest|npm|npx|make|cargo|go|\./\S+', program) for program in programs):
        return '측정 시험'
    return '자료 읽기'


def pid_alive(folder):
    pid = (folder / 'pid').read_text().strip() if (folder / 'pid').is_file() else ''
    if not plain_number(pid):
        return None
    try:
        os.kill(int(pid), 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True


def report_span(report):
    text = report.read_text(encoding='utf-8') if report.is_file() else ''
    stamps = [re.search(r'^' + head + r': (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)', text, re.M) for head in ('시작', '끝')]
    if not all(stamps):
        return '?'
    first, last = (datetime.datetime.strptime(hit.group(1), '%Y-%m-%d %H:%M:%S') for hit in stamps)
    return span((last - first).total_seconds())


class Follower:
    def __init__(self, folder, idle, interval, relay=False):
        self.folder, self.idle, self.interval, self.relay = folder, idle, interval, relay
        self.progress = Tail(folder / 'progress.jsonl')
        self.turn = None
        self.began = None
        self.measured, self.measured_at = [], float('-inf')
        self.summary_at = time.monotonic()
        self.report_seen = None
        self.pending, self.pending_first, self.pending_last = [], 0.0, 0.0

    def emit(self, text):
        # 몇 초 사이에 잇달아 나는 줄은 한 번에 내보낸다. Monitor 는 첫 줄만 바로 알리고 곧이어 온 줄은
        # 다음 출력이 생길 때까지 붙잡아 둔다 — 실사용에서 「차례 시작」 이 감독이 끝날 때까지 56초 늦었다.
        now_mono = time.monotonic()
        if not self.pending:
            self.pending_first = now_mono
        self.pending.append('[' + datetime.datetime.now().strftime('%H:%M:%S') + '] ' + scrub(text))
        self.pending_last = now_mono

    def flush(self, force=False):
        # relay 는 채팅으로 옮길 줄만 낸다. Monitor 가 둘째 알림부터 붙잡아 두므로 한 묶음을 한 줄로 잇는다.
        quiet, longest = (3.0, 4.5) if self.relay else (0.8, 2.5)
        now_mono = time.monotonic()
        if self.pending and (force or now_mono - self.pending_last >= quiet or now_mono - self.pending_first >= longest):
            print((' ‖ ' if self.relay else '\n').join(self.pending), flush=True)
            self.pending = []

    def flush_measured(self):
        if self.measured and self.relay:
            self.measured = []
        if self.measured:
            self.emit('사전 측정 ' + ' | '.join(self.measured))
            self.measured = []
        self.measured_at = time.monotonic()

    def handle(self, record):
        kind, at = record.get('kind'), record.get('at') or time.time()
        if kind == 'notice':
            self.emit(record.get('text', ''))
        elif kind == 'start':
            self.began = at
            count = record.get('conditions')
            self.emit('감독 시작 · {} · {} · {}'.format(record.get('verb'), record.get('folder'),
                                                '조건 {}개'.format(count) if count else '조건 미정'))
        elif kind == 'premeasure':
            self.measured.append('{}/{} · {} · 종료 {}{} · {}'.format(
                record.get('number'), record.get('total'), record.get('id'), record.get('code'),
                ' (시간 초과)' if record.get('timed_out') else '', span(record.get('seconds', 0))))
            if time.monotonic() - self.measured_at >= self.interval:
                self.flush_measured()
        elif kind == 'premeasure-end':
            self.flush_measured()
            self.emit('사전 측정 끝 · {}개 · 총 {}'.format(record.get('total'), span(record.get('seconds', 0))))
        elif kind == 'turn-start':
            self.flush_measured()
            self.turn = dict(name=record.get('name'), home=record.get('home') or '', began=at, thread='',
                             tail=Tail(self.folder / str(record.get('name')) / 'events.jsonl'), seen=set(),
                             failed=set(), window=0, activity='생각 중', size=None, warned=float('-inf'))
            self.emit('차례 {} 시작 · {} · 모델 {} · 생각 {}'.format(record.get('name'), record.get('label'),
                                                       record.get('model'), record.get('effort')))
        elif kind == 'turn-end':
            if self.turn:
                self.take_events()
            self.turn = None
            cost = ' · ' + record['cost'] if record.get('cost') else ''
            self.emit('차례 {} 끝 · {} · {}{}'.format(record.get('name'), record.get('result'), span(record.get('seconds', 0)), cost))
        elif kind == 'retry':
            self.emit('다시 시도 · {} · {}'.format(record.get('name'), record.get('reason')))
        elif kind == 'saved':
            problems = record.get('problems') or 0
            self.emit('{} 계약 저장 끝 · 저장 검사 {} · {}'.format(
                record.get('verb'), '위반 {}건'.format(problems) if problems else '통과', record.get('verdict')))
        elif kind == 'final':
            self.flush_measured()
            if self.turn:
                self.take_events()
            verdict = record.get('verdict')
            self.emit('감독 판정: {} · 총 {}'.format(verdict, span(at - (self.began or at))))
            return EXIT.get(verdict, EXIT['BLOCKED'])
        return None

    def on_event(self, event):
        turn, kind = self.turn, event.get('type')
        item = event.get('item') if isinstance(event.get('item'), dict) else {}
        if kind == 'thread.started':
            turn['thread'] = str(event.get('thread_id') or '')
        elif kind in ('item.started', 'item.updated', 'item.completed'):
            if item.get('type') == 'command_execution':
                key = str(item.get('id') or item.get('command'))
                if key not in turn['seen']:
                    turn['seen'].add(key)
                    turn['window'] += 1
                turn['activity'] = command_kind(item.get('command'))
                code = item.get('exit_code')
                if kind == 'item.completed' and code not in (0, None) and key not in turn['failed']:
                    turn['failed'].add(key)
                    self.emit('오류 · 명령 종료 {} · {}'.format(code, scrub(str(item.get('command') or ''))[:80]))
            elif item.get('type') == 'reasoning' and kind != 'item.completed':
                turn['activity'] = '생각 중'
            elif item.get('type') == 'agent_message' and kind != 'item.completed':
                turn['activity'] = '답 작성'
        elif kind in ('turn.failed', 'error'):
            error = event.get('error')
            message = event.get('message') or (error.get('message') if isinstance(error, dict) else error) or ''
            self.emit('오류 · Codex: ' + scrub(str(message))[:200])

    def take_events(self):
        # 몰려 들어오는 사건 묶음은 끝까지 읽고 나서 요약한다. 반만 읽고 요약하면 명령 수가 다음 일로 넘어간다.
        for _ in range(10):
            events = self.turn['tail'].records()
            if not events:
                return
            self.turn['size'] = None
            for event in events:
                self.on_event(event)
            time.sleep(0.03)

    def rollout_size(self):
        sessions = Path(self.turn['home']) / 'sessions'
        if not self.turn['thread'] or not sessions.is_dir():
            return 0
        return sum(path.stat().st_size for path in sessions.rglob('*' + self.turn['thread'] + '.jsonl'))

    def check_quiet(self):
        turn = self.turn
        events = turn['tail'].path
        last = events.stat().st_mtime if events.is_file() else turn['began']
        if turn['size'] is None:
            turn['size'] = self.rollout_size()
        quiet = time.time() - last
        if quiet < self.idle or time.monotonic() - turn['warned'] < self.idle:
            return
        size = self.rollout_size()
        grew, turn['size'], turn['warned'] = size > turn['size'], size, time.monotonic()
        if grew:
            self.emit('Codex 생각 중(기록은 자람) · 사건 없음 {}초'.format(int(quiet)))
        else:
            self.emit('Codex 조용함 {}초 — 생각 중이거나 멈춤 의심'.format(int(quiet)))

    def stalled(self):
        report = self.folder / 'report.md'
        verdict = last_verdict(report)
        if verdict and not (self.folder / 'progress.jsonl').exists():
            self.emit('감독 판정: {} · 총 {}'.format(verdict, report_span(report)))
            return EXIT.get(verdict, EXIT['BLOCKED'])
        if verdict:
            # 보고서는 진행 기록의 끝 줄보다 먼저 쓰인다. 끝 줄이 끝내 안 오면 보고서를 믿는다.
            self.report_seen = self.report_seen or time.monotonic()
            if time.monotonic() - self.report_seen > 2:
                self.emit('감독 판정: {} · 총 {}'.format(verdict, report_span(report)))
                return EXIT.get(verdict, EXIT['BLOCKED'])
        elif pid_alive(self.folder) is False:
            self.emit('오류 · 감독 프로세스가 판정 없이 끝났다')
            self.emit('감독 판정: BLOCKED · 총 {}'.format(span(time.time() - (self.began or time.time()))))
            return EXIT['BLOCKED']
        return None

    def run(self):
        while True:
            for record in self.progress.records():
                code = self.handle(record)
                if code is not None:
                    self.flush(force=True)
                    return code
            if self.turn:
                self.take_events()
                self.check_quiet()
            if self.measured and time.monotonic() - self.measured_at >= self.interval:
                self.flush_measured()
            if time.monotonic() - self.summary_at >= self.interval:
                if self.turn and not self.relay:
                    self.flush(force=True)
                    say('활동 요약 · 명령 {}개 · 지금 {}'.format(self.turn['window'], self.turn['activity']))
                    self.turn['window'] = 0
                self.summary_at = time.monotonic()
            code = self.stalled()
            if code is not None:
                self.flush(force=True)
                return code
            self.flush()
            time.sleep(POLL)


def audit_folders(root):
    return [entry for entry in root.glob('*-r*') if entry.is_dir() and re.fullmatch(r'(?:draft|impl)-r\d+', entry.name)]


def pick_running(root, wait_seconds):
    known = set(audit_folders(root)) if root.is_dir() else set()
    deadline = time.monotonic() + wait_seconds
    while True:
        running = [entry for entry in (audit_folders(root) if root.is_dir() else [])
                   if last_verdict(entry / 'report.md') is None and pid_alive(entry) is not False
                   and (entry not in known or (entry / 'progress.jsonl').exists())]
        if running:
            return max(running, key=lambda entry: entry.stat().st_mtime)
        if time.monotonic() >= deadline:
            return None
        time.sleep(POLL)


def follow(args):
    options = {'--idle-seconds': 60, '--wait-seconds': 540, '--summary-seconds': 60}
    target, rest, relay = None, list(args), False
    while rest:
        item = rest.pop(0)
        if item == '--relay':
            relay = True
        elif item in options:
            if not rest or not plain_number(rest[0]):
                return usage(item + ' 에는 0 이상의 정수가 필요하다')
            options[item] = int(rest.pop(0))
        elif item.startswith('-'):
            return usage('모르는 옵션: ' + item)
        elif target is None:
            target = item
        else:
            return usage('follow 가 따라갈 대상은 하나다')
    if target is None:
        return usage('follow 에는 감독 폴더나 계약 파일이 필요하다')
    if options['--idle-seconds'] < 1 or options['--summary-seconds'] < 1:
        return usage('--idle-seconds 와 --summary-seconds 는 1 이상이다')
    path = Path(target)
    if path.is_dir():
        folder = path
    elif path.is_file():
        try:
            _, meta, slug, _ = layout(path)
        except ValueError as error:
            return usage(str(error))
        folder = pick_running(meta / 'codex-audit' / slug, options['--wait-seconds'])
        if folder is None:
            say('새 감독이 {}초 안에 시작되지 않아 기다림을 끝낸다 — 계약 {}'.format(options['--wait-seconds'], path.name))
            say('감독 판정: BLOCKED · 총 {}'.format(span(options['--wait-seconds'])))
            return EXIT['BLOCKED']
    else:
        return usage('없는 경로: ' + target)
    return Follower(folder, options['--idle-seconds'], options['--summary-seconds'], relay).run()


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
    if verb == 'follow':
        return follow(args)
    if verb == 'models':
        return models(args)
    if verb == 'usage':
        return usage_report(args)
    if verb not in ('draft', 'revise', 'impl') or len(args) != 2:
        return usage('부속 명령과 인자 둘이 필요하다')
    try:
        contract, meta, slug, _ = layout(args[1] if verb == 'draft' else args[0])
    except ValueError as error:
        return usage(str(error))
    # 칸이 없으면 꺼짐이다. 새 프로젝트가 모르는 사이 감독 키 잔액을 다 쓴 일이 있다 (2026-10-07).
    if settings(meta)[0].get('mode', 'off') == 'off':
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
    (folder / 'pid').write_text(str(os.getpid()))
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
