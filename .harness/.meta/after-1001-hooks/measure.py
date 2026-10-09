#!/usr/bin/env python3
"""계약 after-1001-hooks-into-harness 의 측정 도우미.

사용법: 레포 맨 위 폴더에서 `python3 .harness/.meta/after-1001-hooks/measure.py <조건 번호>`.
종료 코드: 0 성립 · 1 불성립 · 2 잴 수 없음 (도커 · claude · markdownlint 를 못 씀).
TMPDIR 은 절대 경로로 준다. ~/.claude 아래는 읽기만 한다.
"""

import difflib
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid
from pathlib import Path

BASE = "b33ed94a"  # 시작 판 — origin/main (#128 합침)
BRANCH = "chore/ak3-hk"
CONTRACT = ".harness/sprint-contract-after-1001-hooks-into-harness.md"
NOTES = ".harness/.meta/after-kaizen-0928/hk-notes.md"
SCRATCH = "/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad"
MDL = f"{SCRATCH}/fin/mdl/node_modules/.bin/markdownlint-cli2"
MDL_CONFIG = f"{SCRATCH}/fin/mdl/mdl.jsonc"
SIGN_RE = re.compile(r"^Claude .+ <noreply@anthropic\.com>$")

HOOKS = ["lint-contract-oracle.sh", "qa-pending-check.sh"]
MOVED = HOOKS + ["_lib-hook-payload.sh"]
OLD_DIR, NEW_DIR = "harness/evals/hooks", "harness/scripts"
HOOK_TESTS = [f"{OLD_DIR}/lint-contract-oracle-test.sh", f"{OLD_DIR}/qa-pending-check-test.sh"]
HOOK_ENV = {"lint-contract-oracle-test.sh": "LINT_ORACLE_HOOK", "qa-pending-check-test.sh": "QA_PENDING_HOOK"}
PLUGIN_TEST = f"{OLD_DIR}/plugin-hooks-test.sh"
CHECKER, CHECKER_TEST = "scripts/check-user-hook-overlap.py", "scripts/test-check-user-hook-overlap.py"
OLD_CHECKER, OLD_CHECKER_TEST = "scripts/check-user-hook-copies.py", "scripts/test-check-user-hook-copies.py"
SKIP = "개인 설정 없음 — 건너뜀"
LOCALES = ["C", "en_US.UTF-8"]
LIB_DEFAULT_NEW = 'LIB="${CLAUDE_HOOK_LIB:-$(dirname "${BASH_SOURCE[0]}")/_lib-hook-payload.sh}"'
LIB_DEFAULT_OLD = 'LIB="${CLAUDE_HOOK_LIB:-$HOME/.claude/hooks/_lib-hook-payload.sh}"'

# 플러그인 hooks.json 에 새로 들어갈 두 등록 — 2026-10-01 ~/.claude/settings.json 의 값 그대로
NEW_REGS = [
    ("PostToolUse", "Edit|Write", 10, "계약 오라클 린터", '"${CLAUDE_PLUGIN_ROOT}/scripts/lint-contract-oracle.sh"'),
    ("Stop", None, 10, "QA 실행 여부 확인", '"${CLAUDE_PLUGIN_ROOT}/scripts/qa-pending-check.sh"'),
]
NEW_RUNS = ["bash harness/evals/hooks/plugin-hooks-test.sh", "python3 scripts/test-check-user-hook-overlap.py",
            "python3 scripts/check-user-hook-overlap.py"]
OLD_RUNS = ["python3 scripts/test-check-user-hook-copies.py", "python3 scripts/check-user-hook-copies.py"]
WANT_CHANGED = sorted([
    f"{OLD_DIR}/_lib-hook-payload.sh", f"{OLD_DIR}/lint-contract-oracle.sh", f"{OLD_DIR}/qa-pending-check.sh",
    f"{NEW_DIR}/_lib-hook-payload.sh", f"{NEW_DIR}/lint-contract-oracle.sh", f"{NEW_DIR}/qa-pending-check.sh",
    HOOK_TESTS[0], HOOK_TESTS[1], PLUGIN_TEST, "harness/hooks/hooks.json", "harness/README.md",
    OLD_CHECKER, OLD_CHECKER_TEST, CHECKER, CHECKER_TEST, "scripts/sync-docs.py", ".github/workflows/ci.yml",
])
# 옮긴 세 파일의 시작 판 대비 (지운 줄, 더한 줄) — 도우미 찾는 줄과 그 설명만 바뀐다
# 지울 수 있는 줄 — 시작 판 옛 자리의 글자 그대로. 이 밖의 줄을 지우면 BAD
WANT_REMOVED = {
    "lint-contract-oracle.sh": [LIB_DEFAULT_OLD,
                                "#   - docs/superpowers/followup-kaizen-memory-integration.md §훅 승격 후보 —",
                                "#     이 항목은 «훅이 아니라 계약 린터» 로 분류되어 있다. 그래서 차단하지 않는다."],
    "qa-pending-check.sh": [LIB_DEFAULT_OLD],
    "_lib-hook-payload.sh": ["# block-dirwide-autofixer.sh (PreToolUse) 와 lint-contract-oracle.sh (PostToolUse) 가 공유한다.",
                             "# parallel-session-guard.sh 는 strip_heredoc_bodies 만 쓴다."],
}
WANT_MOVE_DIFF = {"lint-contract-oracle.sh": (3, 4), "qa-pending-check.sh": (1, 2), "_lib-hook-payload.sh": (2, 2)}
WANT_HOOK_ROWS = [
    "| `SessionStart` | `env-check.sh` | SessionStart |",
    "| `PreToolUse` | `sdk-guard.sh` | PreToolUse (matcher: Bash) |",
    "| `PreToolUse` | `run-guard.sh` | PreToolUse (matcher: Bash) |",
    "| `PreToolUse` | `commit-guard.sh pre` | PreToolUse (matcher: Bash) |",
    "| `PostToolUse` | `commit-guard.sh post` | PostToolUse (matcher: Bash) |",
    "| `PostToolUse` | `lint-contract-oracle.sh` | PostToolUse (matcher: Edit\\|Write) |",
    "| `Stop` | `qa-pending-check.sh` | Stop |",
]
KEEP_SCRIPTS = ["env-check.sh", "sdk-guard.sh", "run-guard.sh", "commit-guard.sh"]
NOTE_KEYS = ["minor", "0.18.0", "settings.json", "_lib-hook-payload.sh", "block-dirwide-autofixer.sh",
             "CLAUDE.md", "check-user-hook-overlap", "--plugin-dir", "도커", "tone-guide", "남긴 것"]
E2E_PROMPT = ("Use the Write tool exactly once to create the file {path} whose content is these three lines: "
              "'## Skill' then '- [ ] 스킬-01: y' then '  측정: `grep -cF \"표준으로 강제하지 않는다\" f.md` >= 1'. "
              "Then reply with the word done.")
DOCKER_SCRIPT = r'''
apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq jq zsh python3 >/dev/null 2>&1 || exit 2
useradd -m u; cd /repo
for t in harness/evals/hooks/lint-contract-oracle-test.sh harness/evals/hooks/qa-pending-check-test.sh harness/evals/hooks/plugin-hooks-test.sh; do
  su u -c "LC_ALL=C.UTF-8 TMPDIR=/tmp bash $t" >/tmp/o 2>&1; echo "RESULT $t rc=$? tail=[$(tail -1 /tmp/o)]"
done
su u -c "python3 scripts/test-check-user-hook-overlap.py" >/tmp/o 2>&1; echo "RESULT overlap-test rc=$? tail=[$(tail -1 /tmp/o)]"
su u -c "python3 scripts/check-user-hook-overlap.py" >/tmp/o 2>&1; echo "RESULT overlap-check rc=$? tail=[$(tail -1 /tmp/o)]"
echo "AWK $(awk -W version 2>&1 | head -1)"; echo "GREP $(grep --version | head -1)"
'''


def run(*cmd, cwd=None, env=None, stdin=None):
    r = subprocess.run(list(cmd), cwd=cwd, env=env, input=stdin, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def git(*args):
    rc, out = run("git", *args)
    return rc, out.rstrip("\n")


def last(out):
    lines = [x for x in out.splitlines() if x.strip()]
    return lines[-1] if lines else ""


def tmpdir(prefix):
    return Path(tempfile.mkdtemp(prefix=prefix, dir=os.environ.get("TMPDIR")))


def clean_env(**extra):
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_HOOK_LIB", "LINT_ORACLE_HOOK", "QA_PENDING_HOOK", "PLUGIN_HOOKS_ROOT")}
    env.update(extra)
    return env


def base_tree(path, dest):
    """시작 판의 <path> 폴더를 dest 아래에 풀어 그 폴더 경로를 돌려준다."""
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / "base.tar"
    run("git", "archive", "-o", str(archive), BASE, path)
    with tarfile.open(archive) as tar:
        tar.extractall(dest, filter="data")
    return dest / path


def missing(paths):
    gone = [p for p in paths if not Path(p).is_file()]
    if gone:
        print("MISSING " + " ".join(gone))
    return gone


def registrations(data):
    regs = []
    for event, entries in data.get("hooks", {}).items():
        for entry in entries:
            for hook in entry.get("hooks", []):
                regs.append((event, entry.get("matcher"), hook.get("timeout"), hook.get("statusMessage"), hook.get("command")))
    return regs


def m_registration():
    """스크립트-01: hooks.json 에 두 등록이 개인 설정과 같은 값으로 한 번씩 들고, 기존 등록은 차례까지 그대로다."""
    current = registrations(json.loads(Path("harness/hooks/hooks.json").read_text(encoding="utf-8")))
    _, base_text = git("show", f"{BASE}:harness/hooks/hooks.json")
    base = registrations(json.loads(base_text))
    found = sum(current.count(reg) == 1 for reg in NEW_REGS)
    kept = [reg for reg in current if reg not in NEW_REGS] == base
    personal = "absent"
    settings = Path.home() / ".claude/settings.json"
    if settings.is_file():
        mine = [(e, m, t, s) for e, m, t, s, c in registrations(json.loads(settings.read_text(encoding="utf-8")))
                if any(name in (c or "") for name in HOOKS)]
        if mine:  # 부모가 개인 등록을 지운 뒤에는 비교할 값이 없다 — 그때는 absent
            personal = "same" if sorted(mine, key=str) == sorted([r[:4] for r in NEW_REGS], key=str) else f"differ={mine}"
    ok = found == 2 and kept and personal in ("same", "absent")
    print(f"new_found={found} base_kept={int(kept)} base_regs={len(base)} regs={len(current)} personal={personal} ok={int(ok)}")
    return 0 if ok else 1


def harness_copy(dest, mutate):
    root = dest / "harness"
    shutil.copytree("harness/hooks", root / "hooks")
    shutil.copytree("harness/scripts", root / "scripts")
    mutate(root)
    return root


def strip_quotes(root):
    p = root / "hooks/hooks.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    for entries in data["hooks"].values():
        for entry in entries:
            for hook in entry["hooks"]:
                if any(name in hook["command"] for name in HOOKS):
                    hook["command"] = hook["command"].replace('"', "")
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def home_lib(root):
    for name in HOOKS:
        p = root / "scripts" / name
        p.write_text(p.read_text(encoding="utf-8").replace(LIB_DEFAULT_NEW, LIB_DEFAULT_OLD), encoding="utf-8")


def m_plugin_test():
    """스크립트-02: 플러그인 훅 시험이 두 로캘에서 통과하고, 시작 판 · 따옴표 뺀 판 · 홈 도우미 판에서 실패한다."""
    if missing([PLUGIN_TEST]):
        print("ok=0")
        return 1
    work = tmpdir("hk-plugin-")
    home = work / "home"
    home.mkdir()
    passes = 0
    for loc in LOCALES:
        rc, out = run("bash", PLUGIN_TEST, env=clean_env(HOME=str(home), LC_ALL=loc))
        passes += rc == 0 and last(out) == "실패 0 건"
        print(f"RUN LC_ALL={loc} rc={rc} tail=[{last(out)}]")
    variants = {"base": base_tree("harness", work / "b"),
                "noquote": harness_copy(work / "q", strip_quotes),
                "homelib": harness_copy(work / "h", home_lib)}
    rcs = {}
    for name, root in variants.items():
        rcs[name], out = run("bash", PLUGIN_TEST, env=clean_env(HOME=str(home), PLUGIN_HOOKS_ROOT=str(root)))
        print(f"NEG {name} rc={rcs[name]} tail=[{last(out)}]")
    ok = passes == 2 and all(rc == 1 for rc in rcs.values())
    print(f"runs=2 pass={passes} base_rc={rcs['base']} noquote_rc={rcs['noquote']} homelib_rc={rcs['homelib']} ok={int(ok)}")
    return 0 if ok else 1


def m_hook_tests():
    """스크립트-03: 훅 시험 둘이 빈 HOME · 두 로캘에서 플러그인 자리 훅으로 통과하고, 대역 훅이면 실패한다."""
    if missing([f"{NEW_DIR}/{n}" for n in MOVED] + HOOK_TESTS):
        print("ok=0")
        return 1
    work = tmpdir("hk-hooktests-")
    home = work / "home"
    home.mkdir()
    stub = work / "stub.sh"
    stub.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    passes, stub_rcs = 0, []
    for test in HOOK_TESTS:
        for loc in LOCALES:
            rc, out = run("bash", test, env=clean_env(HOME=str(home), LC_ALL=loc))
            passes += rc == 0 and last(out) == "실패 0 건"
            print(f"RUN {test} LC_ALL={loc} rc={rc} tail=[{last(out)}]")
        rc, _ = run("bash", test, env=clean_env(HOME=str(home), **{HOOK_ENV[Path(test).name]: str(stub)}))
        stub_rcs.append(rc)
    exports = sum(line.strip().startswith("export CLAUDE_HOOK_LIB")
                  for test in HOOK_TESTS for line in Path(test).read_text(encoding="utf-8").splitlines())
    ok = passes == 4 and stub_rcs == [1, 1] and exports == 0
    print(f"runs=4 pass={passes} stub_rcs={','.join(map(str, stub_rcs))} lib_exports={exports} ok={int(ok)}")
    return 0 if ok else 1


def e2e_run(plugin_root, work, tag):
    project = work / f"proj-{tag}"
    (project / ".harness").mkdir(parents=True)
    session = str(uuid.uuid4())
    (project / ".harness/sprint-contract-x.md").write_text(
        f'---\nstatus: active\nowner_session: {session}\nlocked_at: "2026-10-01 10:00"\n---\n\n## Skill\n- [ ] 스킬-01: x\n',
        encoding="utf-8")
    prompt = E2E_PROMPT.format(path=project / ".harness/sprint-contract-y.md")
    rc, out = run("claude", "-p", "--setting-sources", "project", "--plugin-dir", str(plugin_root),
                  "--session-id", session, "--no-session-persistence", "--model", "haiku",
                  "--permission-mode", "acceptEdits", "--output-format", "stream-json", "--verbose",
                  "--include-hook-events", prompt, cwd=project, stdin="")
    events = []
    for line in out.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    init = next((e for e in events if e.get("subtype") == "init"), {})
    plugins = [p.get("path") for p in init.get("plugins", []) if p.get("path") != "builtin"]
    responses = [e for e in events if e.get("subtype") == "hook_response"]
    wrote = any(c.get("type") == "tool_use" and c.get("name") == "Write"
                for e in events if e.get("type") == "assistant"
                for c in (e.get("message", {}).get("content") or []) if isinstance(c, dict))
    text = lambda e: str(e.get("output") or e.get("stdout") or "")  # noqa: E731
    lint = sum(e.get("hook_event") == "PostToolUse" and "계약 오라클 경고" in text(e) for e in responses)
    stop = sum(e.get("hook_event") == "Stop" and "QA 가 끝나지 않았습니다" in text(e) and "sprint-contract-x.md" in text(e)
               for e in responses)
    errors = sum(e.get("exit_code") != 0 or e.get("outcome") != "success" for e in responses)
    result = next((e for e in events if e.get("type") == "result"), {})
    usable = rc == 0 and result.get("subtype") == "success" and wrote
    print(f"E2E {tag} rc={rc} result={result.get('subtype')} wrote={int(wrote)} plugins={plugins} "
          f"hooks={len(responses)} lint={lint} stop={stop} errors={errors}")
    return usable, plugins, lint, stop, errors


def m_e2e():
    """스크립트-04 · 진단-04: 실제 claude 를 이 플러그인 폴더 하나만 얹어 비대화로 돌려 두 훅이 돌고, 시작 판 폴더로는 안 돈다."""
    if shutil.which("claude") is None:
        print("claude 없음 — 잴 수 없음")
        return 2
    if missing([f"{NEW_DIR}/{n}" for n in HOOKS]):
        print("ok=0")
        return 1
    work = tmpdir("hk-e2e-")
    root = Path("harness").resolve()
    usable, plugins, lint, stop, errors = e2e_run(root, work, "branch")
    b_usable, _, b_lint, b_stop, _ = e2e_run(base_tree("harness", work / "b").resolve(), work, "base")
    if not (usable and b_usable):
        print("claude 실행이 끝나지 않았거나 Write 를 안 불렀다 — 잴 수 없음")
        return 2
    plugin_ok = plugins == [str(root)]
    ok = plugin_ok and lint >= 1 and stop >= 1 and errors == 0 and b_lint == 0 and b_stop == 0
    print(f"plugin_ok={int(plugin_ok)} lint={int(lint >= 1)} stop={int(stop >= 1)} errors={errors} "
          f"base_lint={b_lint} base_stop={b_stop} ok={int(ok)}")
    return 0 if ok else 1


def known_overlaps(settings_dir):
    """검사와 따로 개인 설정을 읽어 낸 알려진 답 — (파일 이름, 이벤트, 훅 이름) 목록."""
    found = []
    for name in ("settings.json", "settings.local.json"):
        p = settings_dir / name
        if not p.is_file():
            continue
        for event, _, _, _, command in registrations(json.loads(p.read_text(encoding="utf-8"))):
            for hook in HOOKS:
                if hook in (command or ""):
                    found.append(f"{name}:{event}:{hook}")
    return found


def got_overlaps(out):
    found = []
    for line in out.splitlines():
        if line.startswith("겹침: "):
            path, event, command = line[4:].split(" ", 2)
            found += [f"{Path(path).name}:{event}:{h}" for h in HOOKS if h in command]
    return found


def m_overlap():
    """스크립트-05: 겹침 검사가 설정 없음 · 이 맥 설정 · 두 등록을 지운 이 맥 설정 · 깨진 JSON 을 바르게 알린다."""
    if missing([CHECKER]):
        print("ok=0")
        return 1
    work = tmpdir("hk-overlap-")
    rc, out = run("python3", CHECKER, "--settings-dir", str(work / "none"))
    none_ok = rc == 0 and out.splitlines() == [SKIP]
    home = Path.home() / ".claude"
    try:
        known = known_overlaps(home)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"개인 설정을 못 읽음 ({type(error).__name__}) — 잴 수 없음")
        return 2
    present = [n for n in ("settings.json", "settings.local.json") if (home / n).is_file()]
    rc, out = run("python3", CHECKER)
    got = got_overlaps(out)
    if not present:
        home_ok = rc == 0 and out.splitlines() == [SKIP]
    else:
        home_ok = got == known and rc == (1 if known else 0)
    cleaned = work / "cleaned"
    cleaned.mkdir()
    for name in present:
        data = json.loads((home / name).read_text(encoding="utf-8"))
        for event, entries in list(data.get("hooks", {}).items()):
            for entry in entries:
                entry["hooks"] = [h for h in entry.get("hooks", []) if not any(n in h.get("command", "") for n in HOOKS)]
            data["hooks"][event] = [e for e in entries if e["hooks"]]
        (cleaned / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    rc_c, out_c = run("python3", CHECKER, "--settings-dir", str(cleaned))
    cleaned_ok = (rc_c == 0 and out_c.splitlines() == [f"겹침 없음 (설정 파일 {len(present)} 개)"]) if present \
        else (rc_c == 0 and out_c.splitlines() == [SKIP])
    broken = work / "broken"
    broken.mkdir()
    (broken / "settings.json").write_text("{ not json", encoding="utf-8")
    rc_b, out_b = run("python3", CHECKER, "--settings-dir", str(broken))
    broken_ok = rc_b == 2 and sum(x.startswith("UNREADABLE ") for x in out_b.splitlines()) == 1
    ok = none_ok and home_ok and cleaned_ok and broken_ok
    print(f"none_ok={int(none_ok)} known={known} got={got} home_rc={rc} home_ok={int(home_ok)} "
          f"cleaned_ok={int(cleaned_ok)} broken_ok={int(broken_ok)} ok={int(ok)}")
    return 0 if ok else 1


def m_overlap_test():
    """스크립트-06: 겹침 시험이 일곱 경우를 통과하고, 늘 건너뛰는 대역 검사에서 경우 3 ~ 7 만 실패한다."""
    if missing([CHECKER_TEST]):
        print("ok=0")
        return 1
    rc, out = run("python3", CHECKER_TEST)
    tail_ok = rc == 0 and last(out) == "경우 7 개 중 통과 7"
    work = tmpdir("hk-overlap-test-")
    stub = work / "stub.py"
    stub.write_text(f'print("{SKIP}")\n', encoding="utf-8")
    rc_s, out_s = run("python3", CHECKER_TEST, "--tool", str(stub))
    fails = [m.group(1) for m in re.finditer(r"^FAIL 경우 (\d+) ", out_s, re.M)]
    stub_ok = rc_s == 1 and fails == ["3", "4", "5", "6", "7"]
    ok = tail_ok and stub_ok
    print(f"tail=[{last(out)}] ok_tail={int(tail_ok)} stub_fails={','.join(fails)} stub_rc={rc_s} ok={int(ok)}")
    return 0 if ok else 1


def ci_runs(text):
    import yaml  # noqa: PLC0415 — 로컬 CI 와 같은 읽기
    doc = yaml.safe_load(text)
    return [step["run"].strip() for job in doc["jobs"].values() for step in job.get("steps", []) if "run" in step]


def m_ci():
    """스크립트-07: CI run 줄에서 옛 둘을 빼고 새 셋을 한 번씩 더했을 뿐 나머지는 차례까지 그대로다."""
    runs = ci_runs(Path(".github/workflows/ci.yml").read_text(encoding="utf-8"))
    _, base_text = git("show", f"{BASE}:.github/workflows/ci.yml")
    base = ci_runs(base_text)
    new_once = all(runs.count(r) == 1 for r in NEW_RUNS)
    old_gone = all(runs.count(r) == 0 for r in OLD_RUNS) and all(base.count(r) == 1 for r in OLD_RUNS)
    kept = [r for r in runs if r not in NEW_RUNS] == [r for r in base if r not in OLD_RUNS]
    ok = new_once and old_gone and kept and len(runs) == len(base) + 1
    print(f"base_runs={len(base)} runs={len(runs)} new_once={int(new_once)} old_gone={int(old_gone)} kept={int(kept)} ok={int(ok)}")
    return 0 if ok else 1


def m_docker():
    """스크립트-08: 리눅스(ubuntu:24.04 · C.UTF-8 · mawk · GNU grep)에서 훅 시험 셋 · 겹침 시험 · 겹침 검사가 돈다."""
    if shutil.which("docker") is None or run("docker", "info")[0] != 0:
        print("도커 없음 — 잴 수 없음")
        return 2
    rc, out = run("docker", "run", "--rm", "-v", f"{Path.cwd()}:/repo:ro", "-e", "LC_ALL=C.UTF-8",
                  "ubuntu:24.04", "bash", "-c", DOCKER_SCRIPT)
    if rc == 2:
        print("apt 실패 — 잴 수 없음")
        return 2
    results = re.findall(r"^RESULT (\S+) rc=(\d+) tail=\[(.*)\]$", out, re.M)
    want = {"harness/evals/hooks/lint-contract-oracle-test.sh": "실패 0 건",
            "harness/evals/hooks/qa-pending-check-test.sh": "실패 0 건",
            "harness/evals/hooks/plugin-hooks-test.sh": "실패 0 건",
            "overlap-test": "경우 7 개 중 통과 7", "overlap-check": SKIP}
    good = sum(rc_ == "0" and want.get(name) == tail for name, rc_, tail in results)
    mawk = int(bool(re.search(r"^AWK mawk", out, re.M)))
    gnu = int(bool(re.search(r"^GREP grep \(GNU grep\)", out, re.M)))
    for name, rc_, tail in results:
        print(f"RESULT {name} rc={rc_} tail=[{tail}]")
    ok = good == 5 and len(results) == 5 and mawk and gnu
    print(f"results={len(results)} good={good} mawk={mawk} gnu_grep={gnu} ok={int(ok)}")
    return 0 if ok else 1


def auto_rows(text):
    m = re.search(r"<!-- AUTO:hooks -->\n(.*?)<!-- /AUTO:hooks -->", text, re.S)
    return [x for x in m.group(1).splitlines() if x.startswith("| `")] if m else None


def mdl_issues(path):
    if not Path(MDL).is_file():
        return None, ""
    rc, out = run(MDL, "--config", MDL_CONFIG, str(path))
    return len(re.findall(r" MD[0-9]{3}", out)), out


def m_docs():
    """스크립트-09: README 훅 표가 sync-docs 로 일곱 줄이 되고, 설명이 두 훅과 겹침 검사를 적고, 표가 안 갈린다."""
    rc, out = run("python3", "scripts/sync-docs.py", "--check-only")
    synced = rc == 0 and "모든 README가 동기화 상태입니다." in out
    text = Path("harness/README.md").read_text(encoding="utf-8")
    rows = auto_rows(text)
    rows_ok = rows == WANT_HOOK_ROWS
    outside = re.sub(r"<!-- AUTO:hooks -->.*?<!-- /AUTO:hooks -->", "", text, flags=re.S)
    prose = [w for w in ("scripts/qa-pending-check.sh", "scripts/lint-contract-oracle.sh",
                         "scripts/check-user-hook-overlap.py", "CLAUDE_HOOK_LIB", "plugin-hooks-test.sh") if w not in outside]
    issues, mdl_out = mdl_issues("harness/README.md")
    if issues is None:
        print("markdownlint 없음 — 잴 수 없음")
        return 2
    work = tmpdir("hk-docs-")
    bad = work / "README.md"
    bad.write_text(text.replace("Edit\\|Write", "Edit|Write"), encoding="utf-8")
    bad_issues, bad_out = mdl_issues(bad)
    md056 = len(re.findall(r" MD056", bad_out))
    ok = synced and rows_ok and not prose and issues == 0 and "Linting: 1 file" in mdl_out and md056 >= 1
    print(f"synced={int(synced)} rows={len(rows or [])} rows_ok={int(rows_ok)} prose_miss={prose} "
          f"mdl={issues} pos_md056={md056} ok={int(ok)}")
    return 0 if ok else 1


def m_failopen():
    """오류-01: 두 훅이 도우미를 못 찾거나 · 빈 입력 · 깨진 JSON 이면 출력 없이 0 이다."""
    if missing([f"{NEW_DIR}/{n}" for n in HOOKS]):
        print("ok=0")
        return 1
    work = tmpdir("hk-failopen-")
    (work / ".harness").mkdir()
    contract = work / ".harness/sprint-contract-x.md"
    contract.write_text('---\nstatus: active\nowner_session: S1\n---\n\n## Skill\n- [ ] 스킬-01: x\n'
                        '  측정: `grep -cF "표준으로 강제하지 않는다" f.md` >= 1\n', encoding="utf-8")
    good = {"lint-contract-oracle.sh": json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(contract)}}),
            "qa-pending-check.sh": json.dumps({"session_id": "S1", "cwd": str(work), "transcript_path": ""})}
    right = 0
    for name in HOOKS:
        hook = f"{NEW_DIR}/{name}"
        cases = [("nolib", good[name], {"CLAUDE_HOOK_LIB": str(work / "none.sh")}), ("empty", "", {}), ("broken", "{", {})]
        for label, stdin, extra in cases:
            rc, out = run("bash", hook, env=clean_env(**extra), stdin=stdin)
            ok = rc == 0 and out == ""
            right += ok
            print(f"{'OK ' if ok else 'BAD'} {name} {label} rc={rc} out={len(out)}")
        rc, out = run("bash", hook, env=clean_env(), stdin=good[name])
        live = rc == 0 and "additionalContext" in out
        right += live
        print(f"{'OK ' if live else 'BAD'} {name} live rc={rc} context={int('additionalContext' in out)}")
    print(f"cases=8 right={right} ok={int(right == 8)}")
    return 0 if right == 8 else 1


def m_keep():
    """오류-02: 기존 훅 스크립트 넷은 바이트 그대로이고 커밋 훅 시험이 통과한다."""
    rc, out = git("diff", "--name-only", f"{BASE}..{BRANCH}", "--", *[f"{NEW_DIR}/{n}" for n in KEEP_SCRIPTS])
    same = rc == 0 and out == ""
    rc_t, out_t = run("bash", f"{OLD_DIR}/commit-guard-test.sh")
    ok = same and rc_t == 0
    print(f"same={int(same)} commit_guard_rc={rc_t} tail=[{last(out_t)}] ok={int(ok)}")
    return 0 if ok else 1


def scope_block():
    text = Path(CONTRACT).read_text(encoding="utf-8")
    sec = re.search(r"^## 범위 경계\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    entries = []
    for block in re.findall(r"```text\n(.*?)```", sec.group(1) if sec else "", re.S):
        lines = block.splitlines()
        if lines and lines[0].strip() == "# sprint-scope":
            entries += [x.strip() for x in lines[1:] if x.strip() and not x.startswith("#")]
    return entries


def in_scope(path, scope):
    if path.startswith(".harness/"):
        return True
    return any(path == s or (s.endswith("/") and path.startswith(s)) or ("*" in s and fnmatch.fnmatch(path, s))
               for s in scope)


def m_commits():
    """구조-01: 시작 판 뒤 커밋마다 합침 아님 · 맨 위 폴더 하나 · 서명 줄 · 범위 안."""
    scope = scope_block()
    rc, revs = git("rev-list", "--reverse", f"{BASE}..{BRANCH}")
    bad = 0
    for c in revs.split():
        _, parents = git("rev-list", "--parents", "-n", "1", c)
        _, files = git("show", "--name-only", "--format=", c)
        _, trailers = git("log", "-1", "--format=%(trailers:key=Co-Authored-By,valueonly)", c)
        fs = [f for f in files.split("\n") if f]
        tops = {f.split("/")[0] if "/" in f else "(root)" for f in fs}
        signed = any(SIGN_RE.match(t.strip()) for t in trailers.splitlines())
        out = [f for f in fs if not in_scope(f, scope)]
        merge = len(parents.split()) > 2
        ok = len(tops) == 1 and signed and not out and not merge
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {c[:8]} tops={sorted(tops)} signed={int(signed)} out_of_scope={out[:5]} merge={int(merge)}")
    n = len(revs.split())
    print(f"commits={n} bad={bad} scope_entries={len(scope)} git_rc={rc}")
    return 0 if bad == 0 and n and len(scope) == len(WANT_CHANGED) and rc == 0 else 1


def m_layout():
    """구조-02: 바뀐 파일이 정확히 열일곱이고, 훅 파일 셋은 레포에 한 벌씩 harness/scripts/ 에만 있다."""
    _, out = git("diff", "--no-renames", "--name-only", f"{BASE}..{BRANCH}", "--", ".", ":(exclude).harness")
    changed = sorted(x for x in out.splitlines() if x)
    _, tracked = git("ls-tree", "-r", "--name-only", BRANCH)
    copies = sorted(x for x in tracked.splitlines() if Path(x).name in MOVED and not x.startswith(".harness/"))
    want_copies = sorted(f"{NEW_DIR}/{n}" for n in MOVED)
    extra = sorted(set(changed) - set(WANT_CHANGED))
    lack = sorted(set(WANT_CHANGED) - set(changed))
    ok = changed == WANT_CHANGED and copies == want_copies
    print(f"files={len(changed)} extra={extra} lack={lack} copies={copies} ok={int(ok)}")
    return 0 if ok else 1


def m_moved():
    """구조-03: 옮긴 세 파일은 도우미 찾는 줄과 그 설명만 바뀌고, 코드 줄이 ~/.claude/hooks 를 안 보고, 실행 비트가 있다."""
    if missing([f"{NEW_DIR}/{n}" for n in MOVED]):
        print("ok=0")
        return 1
    right = 0
    for name in MOVED:
        _, old = git("show", f"{BASE}:{OLD_DIR}/{name}")
        new = Path(f"{NEW_DIR}/{name}").read_text(encoding="utf-8")
        diff = [x for x in difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0)
                if x[:1] in "+-" and not x.startswith(("+++", "---"))]
        counts = (sum(x.startswith("-") for x in diff), sum(x.startswith("+") for x in diff))
        removed_ok = sorted(x[1:] for x in diff if x.startswith("-")) == sorted(WANT_REMOVED[name])
        code_home = sum(".claude/hooks" in x for x in new.splitlines() if not x.lstrip().startswith("#"))
        _, mode = git("ls-tree", BRANCH, f"{NEW_DIR}/{name}")
        exec_ok = mode.startswith("100755")
        ok = counts == WANT_MOVE_DIFF[name] and removed_ok and code_home == 0 and exec_ok
        right += ok
        print(f"{'OK ' if ok else 'BAD'} {name} diff={counts} want={WANT_MOVE_DIFF[name]} removed_ok={int(removed_ok)} code_home={code_home} exec={int(exec_ok)}")
    rc_v, out_v = run("python3", "scripts/validate-plugin.py", "harness", "--check=hook-exec")
    v8 = rc_v == 0
    print(f"files=3 right={right} v8_rc={rc_v} ok={int(right == 3 and v8)}")
    return 0 if right == 3 and v8 else 1


def m_notes():
    """구조-04: 기록에 판 올림 판단 · 사용자 쪽 정리 할 일 · 확인 방법 · 커밋 해시가 있다."""
    p = Path(NOTES)
    if not p.is_file():
        print(f"MISSING {NOTES} keys_ok=0")
        return 1
    text = p.read_text(encoding="utf-8")
    miss = [k for k in NOTE_KEYS if k not in text]
    _, revs = git("rev-list", f"{BASE}..{BRANCH}")
    mine = {r[:8] for r in revs.split()}
    hashes = set(re.findall(r"\b[0-9a-f]{8}\b", text)) & mine
    ok = not miss and len(hashes) >= 3
    print(f"keys_ok={int(not miss)} miss={miss} branch_hashes={len(hashes)} ok={int(ok)}")
    return 0 if ok else 1


def m_version():
    """구조-05: 이 묶음은 판 번호 · 마켓 목록을 안 바꾼다 (릴리스는 부모)."""
    rc, out = git("diff", "--name-only", f"{BASE}..{BRANCH}", "--", "harness/.claude-plugin", ".claude-plugin")
    ok = rc == 0 and out == ""
    print(f"version_files_changed=[{out}] ok={int(ok)}")
    return 0 if ok else 1


def m_reuse():
    """재사용-02: 도우미는 레포에 하나뿐이고 두 훅이 그것을 부르며, 새 폴더가 없다."""
    _, tracked = git("ls-tree", "-r", "--name-only", BRANCH)
    libs = [x for x in tracked.splitlines() if Path(x).name == "_lib-hook-payload.sh" and not x.startswith(".harness/")]
    users = sum(any(line.strip() == LIB_DEFAULT_NEW for line in Path(f"{NEW_DIR}/{n}").read_text(encoding="utf-8").splitlines())
                for n in HOOKS if Path(f"{NEW_DIR}/{n}").is_file())
    _, out = git("diff", "--no-renames", "--name-only", "--diff-filter=A", f"{BASE}..{BRANCH}", "--", ".", ":(exclude).harness")
    _, base_tree_list = git("ls-tree", "-r", "--name-only", BASE)
    base_dirs = {str(Path(x).parent) for x in base_tree_list.splitlines()}
    new_dirs = sorted({str(Path(x).parent) for x in out.splitlines() if x} - base_dirs)
    ok = len(libs) == 1 and users == 2 and not new_dirs
    print(f"libs={libs} lib_users={users} new_dirs={new_dirs} ok={int(ok)}")
    return 0 if ok else 1


def m_diag04():
    """진단-04: 이 플러그인 폴더로 돌린 실제 claude 실행에서 모든 훅 응답이 종료 코드 0 · success 다."""
    if shutil.which("claude") is None:
        print("claude 없음 — 잴 수 없음")
        return 2
    usable, _, _, _, errors = e2e_run(Path("harness").resolve(), tmpdir("hk-diag04-"), "branch")
    if not usable:
        print("claude 실행이 끝나지 않았거나 Write 를 안 불렀다 — 잴 수 없음")
        return 2
    print(f"errors={errors} ok={int(errors == 0)}")
    return 0 if errors == 0 else 1


CONDS = {
    "스크립트-01": m_registration, "스크립트-02": m_plugin_test, "스크립트-03": m_hook_tests, "스크립트-04": m_e2e,
    "스크립트-05": m_overlap, "스크립트-06": m_overlap_test, "스크립트-07": m_ci, "스크립트-08": m_docker,
    "스크립트-09": m_docs, "오류-01": m_failopen, "오류-02": m_keep, "구조-01": m_commits, "구조-02": m_layout,
    "구조-03": m_moved, "구조-04": m_notes, "구조-05": m_version, "재사용-02": m_reuse, "진단-04": m_diag04,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
