"""계약 after-0930-final 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

평가 실행기 임시 트리 · 킷 칸 나누기는 앞 묶음 ev(after-0930-eval-runners) 도우미를,
CI 단계 읽기 · 커밋 규칙은 그 도우미가 부르는 tail(after-0929-tail) 도우미를 불러 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
임시 폴더는 TMPDIR 아래 만든다. 레포 파일과 ~/.claude/hooks/ 에는 쓰지 않는다.
"""
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = "7fe274fc"  # 시작 판 — chore/ak3-ev 끝 (QA APPROVE, main 에 아직 안 합쳐짐)
BRANCH = "chore/ak3-fin"
CONTRACT = ".harness/sprint-contract-after-0930-final.md"
NOTES = ".harness/.meta/after-kaizen-0928/fin-notes.md"
EV = ".harness/.meta/after-0930-eval-runners/measure.py"
RUN_EVALS, RUN_TEST = "scripts/run-evals.py", "scripts/test-run-evals.py"
SYNC_EVALS, SYNC_TEST = "scripts/sync-evals.py", "scripts/test-sync-evals.py"
CHECKER, CHECKER_TEST = "scripts/check-user-hook-copies.py", "scripts/test-check-user-hook-copies.py"
HOOK_DIR = "harness/evals/hooks"
HOOK_TESTS = [f"{HOOK_DIR}/lint-contract-oracle-test.sh", f"{HOOK_DIR}/qa-pending-check-test.sh"]
HOOK_ENV = {"lint-contract-oracle-test.sh": "LINT_ORACLE_HOOK", "qa-pending-check-test.sh": "QA_PENDING_HOOK"}
# 옮길 파일 셋과 봉인 전(2026-10-01) ~/.claude/hooks/ 설치본 지문 — shasum -a 256 앞 16 자리
COPIED = {"lint-contract-oracle.sh": "182ed51390abd4ae", "qa-pending-check.sh": "07c427c14a16523e",
          "_lib-hook-payload.sh": "dff1e68e020a5028"}
INSTALLED = Path.home() / ".claude/hooks"
SKIP_LINE = "설치본 없음 — 건너뜀"
# 객체가 아닌 내용 다섯 — 세면 안 되는 모양
NON_OBJECT = [("null", "null"), ("number", "5"), ("string", '"x"'), ("array", "[]"), ("boolean", "true")]
GOOD_ENTRY = '{"id":1,"skill":"s","prompt":"p","expected_output":"e","assertions":[{"text":"a","type":"output"}]}'
# 목록 열쇠 셋 — 넘겨야 할 정상 모양
NORMAL = [(key, f'{{"{key}":[{GOOD_ENTRY}]}}') for key in ("evals", "tests", "cases")]
# 어떤 평가 파일 내용이든 null 로 읽는 지나친 판 — 마켓 목록 읽기는 그대로 둔다
NULL_EVALS = ('import json\n_real_loads = json.loads\n'
              'json.loads = lambda s, *a, **k: _real_loads(s, *a, **k) if "\\"plugins\\"" in s else None\n')
# 늘 건너뜀 줄만 찍고 0 으로 끝나는 맞대기 검사 대역
CHECKER_STUB = f'print("{SKIP_LINE}")\n'
HOOK_STUB = "#!/usr/bin/env bash\nexit 0\n"
# 킷 b 의 두 번째 읽기만 못 읽음 표시를 돌려준다 — 두 읽기 사이에 파일이 바뀐 경우
SECOND_READ = '''
import importlib.util, sys
spec = importlib.util.spec_from_file_location("sync_evals", "scripts/sync-evals.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
real_load, calls = mod.load_evals, {}
def second_read_fails(kit):
    calls[kit] = calls.get(kit, 0) + 1
    return mod.UNREADABLE if kit == "b" and calls[kit] == 2 else real_load(kit)
mod.load_evals = second_read_fails
sys.argv = ["sync-evals.py"] + sys.argv[1:]
sys.exit(mod.main())
'''


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ev = load("ev", EV)
tail = ev.tail
read, git, run, last, report = ev.read, ev.git, ev.run, ev.last, ev.report
tmpdir, fails_of, blocks, run_tree = ev.tmpdir, ev.fails_of, ev.blocks, ev.run_tree
TOOLS, KITS = ev.TOOLS, ev.KITS


def sha16(data):
    return hashlib.sha256(data).hexdigest()[:16]


def tool_dir_of(rev):
    """rev 판 도구 셋을 임시 폴더에. rev 가 None 이면 작업 폴더 판."""
    d = tmpdir("finbase.")
    for name in ("run-evals.py", "sync-evals.py", "plugin_utils.py"):
        if rev:
            ev.show(rev, f"scripts/{name}", d / name)
        else:
            shutil.copy(f"scripts/{name}", d / name)
    return d


def mutant_dir():
    d = tool_dir_of(None)
    for name in ("run-evals.py", "sync-evals.py"):
        (d / name).write_text(NULL_EVALS + read(f"scripts/{name}"), encoding="utf-8")
    return d


def content_tree(root, tool_dir, contents, extra):
    """킷 a · b · c 트리. contents[킷] 이 있으면 그 킷 evals.json 을 그 글로, 'unreadable' 이면 권한을 뺀다."""
    shapes = {k: ("unreadable" if v == "unreadable" else "good") for k, v in contents.items()}
    locked = ev.tree(root, tool_dir, shapes, extra)
    for k, v in contents.items():
        if v != "unreadable":
            (root / k / "evals/evals.json").write_text(v + "\n", encoding="utf-8")
    # extra 는 good 칸에만 붙는다 — 내용을 바꾼 칸에서 extra 스킬을 걷어 그 칸이 재지 않은 칸으로 남게 한다
    for k in contents:
        shutil.rmtree(root / k / "skills/extra", ignore_errors=True)
    return locked


def summary_lines(out):
    """마지막 → 줄 뒤의 요약 줄들."""
    lines = out.splitlines()
    heads = [i for i, l in enumerate(lines) if l.startswith("→ ")]
    start = heads[-1] if heads else -1
    return [l.strip() for l in lines[start + 1:] if l.startswith(("못 읽은 킷", "항목 없는 킷"))]


def measured(tool, kit, out):
    return ev.MEASURED[tool].format(kit) in blocks(out).get(kit, "")


# ---- (A) 평가 실행기 ----
def nonobject_matrix(tool_dir):
    right = total = 0
    for label, text in NON_OBJECT:
        for name, cmd in TOOLS:
            d = tmpdir("finobj.")
            content_tree(d / "t", tool_dir, {"b": text}, extra=True)
            rc, out = run_tree(d / "t", cmd, [])
            shutil.rmtree(d, ignore_errors=True)
            line = any("b/evals/evals.json" in l and "객체가 아니다" in l for l in out.splitlines())
            trace = "Traceback" in out
            meas = measured(name, "a", out) and measured(name, "c", out)
            summ = summary_lines(out) == ["못 읽은 킷 1 개: b"]
            ok = rc == 2 and line and not trace and meas and summ
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} b-{label} {name} rc={rc} line={int(line)} trace={int(trace)} measured={int(meas)} summary={int(summ)}")
    return total, right


def m_nonobject():
    """스크립트-01: 가운데 킷 b 의 내용이 객체가 아니면 세 도구 모두 2 · 경로와 까닭 한 줄 · 추적 출력 없음 · a c 는 잼 · 요약 줄."""
    total, right = nonobject_matrix(Path("scripts").resolve())
    return report({"cases": total, "right": right, "ok": right == total})


def normal_cases(tool_dir):
    right = total = 0
    for key, text in NORMAL:
        for name, cmd in TOOLS:
            d = tmpdir("finnorm.")
            content_tree(d / "t", tool_dir, {"b": text}, extra=False)
            rc, out = run_tree(d / "t", cmd, [])
            shutil.rmtree(d, ignore_errors=True)
            ok = rc == 0 and "객체가 아니다" not in out and "UNREADABLE" not in out and "Traceback" not in out
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} b-{key} {name} rc={rc}")
    return total, right


def m_normal():
    """스크립트-02: 목록 열쇠 evals · tests · cases 정상 파일은 세 도구 모두 0. 음성 대조 — NULL_EVALS 변이는 아홉 모두 틀린다."""
    total, right = normal_cases(Path("scripts").resolve())
    mut = mutant_dir()
    _, mut_right = normal_cases(mut)
    shutil.rmtree(mut, ignore_errors=True)
    return report({"cases": total, "right": right, "ok": right == total, "mut_right": mut_right, "mut_ok": mut_right == 0})


EMPTY_SETS = [("b-empty-list", {"b": '{"evals":[]}'}, [], ["b"]),
              ("b-no-key", {"b": "{}"}, [], ["b"]),
              ("ac-empty-list", {"a": '{"evals":[]}', "c": '{"tests":[]}'}, [], ["a", "c"]),
              ("b-unreadable-c-empty", {"b": "unreadable", "c": '{"cases":[]}'}, ["b"], ["c"])]


def m_empty():
    """스크립트-03: run-evals.py 는 항목 0 개 킷에서 멈추지 않고 나머지를 잰 뒤, 끝에 요약 줄을 찍고 2."""
    if not ev.rootless():
        print("ROOT 권한을 빼도 읽힌다")
        return 2
    tool = Path("scripts").resolve()
    right = 0
    for label, contents, unreadable, empty in EMPTY_SETS:
        d = tmpdir("finempty.")
        locked = content_tree(d / "t", tool, contents, extra=True)
        rc, out = run_tree(d / "t", ev.TOOLS[0][1], locked)
        shutil.rmtree(d, ignore_errors=True)
        good = [k for k in KITS if k not in contents]
        want = ([f"못 읽은 킷 {len(unreadable)} 개: {', '.join(unreadable)}"] if unreadable else []) + \
               [f"항목 없는 킷 {len(empty)} 개: {', '.join(empty)}"]
        lines_ok = all(any(f"{k}/evals/evals.json" in l for l in out.splitlines()) for k in empty)
        meas = all(measured("run", k, out) for k in good)
        summ = summary_lines(out) == want
        ok = rc == 2 and lines_ok and meas and summ
        right += ok
        print(f"{'OK ' if ok else 'BAD'} {label} rc={rc} line={int(lines_ok)} measured={int(meas)} summary={summary_lines(out)}")
    return report({"cases": len(EMPTY_SETS), "right": right, "ok": right == len(EMPTY_SETS)})


def m_named():
    """스크립트-04: 이름으로 준 킷 — 대상 없는 바로가기는 못 읽음, 진짜 없는 평가 파일 · 없는 킷은 지금 안내, 정상은 0."""
    tool = Path("scripts").resolve()
    cases = [("b-dangling", {"b": "dangling"}, "b"), ("b-absent", {"b": "absent"}, "b"),
             ("nope", {}, "nope"), ("b-good", {}, "b")]
    right = 0
    for label, shapes, arg in cases:
        d = tmpdir("finnamed.")
        ev.tree(d / "t", tool, shapes, extra=False)
        rc, out = run_tree(d / "t", ["python3", "scripts/run-evals.py", arg], [])
        shutil.rmtree(d, ignore_errors=True)
        lines = out.splitlines()
        if label == "b-dangling":
            ok = rc == 2 and any(l.startswith("UNREADABLE") and "b/evals/evals.json" in l for l in lines) \
                and "evals.json 없음" not in out
        elif label == "b-absent":
            ok = rc == 2 and "ERROR: 이름으로 준 킷 b — evals/evals.json 없음" in lines
        elif label == "nope":
            ok = rc == 2 and "ERROR: 이름으로 준 킷 nope — 킷 폴더 없음" in lines
        else:
            ok = rc == 0 and measured("run", "b", out)
        right += ok
        print(f"{'OK ' if ok else 'BAD'} named {label} rc={rc} tail=[{last(out)}]")
    return report({"cases": len(cases), "right": right, "ok": right == len(cases)})


def m_second_read():
    """스크립트-05: sync-evals.py 가 킷 b 를 다시 읽을 때 못 읽으면 추적 출력 없이 a c 를 재고 요약 줄 · 2."""
    tool = Path("scripts").resolve()
    right = 0
    for name, args in (("sync-check", ["--check-only"]), ("sync-plain", [])):
        d = tmpdir("finsecond.")
        ev.tree(d / "t", tool, {}, extra=True)
        rc, out = run_tree(d / "t", ["python3", "-c", SECOND_READ, *args], [])
        shutil.rmtree(d, ignore_errors=True)
        trace = "Traceback" in out
        meas = measured(name, "a", out) and measured(name, "c", out)
        summ = summary_lines(out) == ["못 읽은 킷 1 개: b"]
        ok = rc == 2 and not trace and meas and summ
        right += ok
        print(f"{'OK ' if ok else 'BAD'} second-read {name} rc={rc} trace={int(trace)} measured={int(meas)} summary={int(summ)}")
    return report({"cases": 2, "right": right, "ok": right == 2})


def m_base():
    """스크립트-01 · 03 · 04 · 05 의 음성 대조 — 시작 판 도구는 걸려야 할 모양에서 모두 틀린다."""
    if not ev.rootless():
        return 2
    d = tool_dir_of(BASE)
    total, right = nonobject_matrix(d)
    shutil.rmtree(d, ignore_errors=True)
    return report({"cases": total, "base_right": right, "base_all_wrong": right == 0})


def m_eval_tests():
    """스크립트-06: 평가 시험 둘 — 끝 줄 · 시작 판 도구로 새 걸릴 경우만 실패 · 지나친 판으로 정상 모양 경우가 실패 · CI 이름."""
    rc_r, out_r = run("python3", RUN_TEST)
    rc_s, out_s = run("python3", SYNC_TEST)
    b = tool_dir_of(BASE)
    rc_rb, out_rb = run("python3", RUN_TEST, "--tool", str(b / "run-evals.py"))
    rc_sb, out_sb = run("python3", SYNC_TEST, "--tool", str(b / "sync-evals.py"))
    m = mutant_dir()
    rc_rm, out_rm = run("python3", RUN_TEST, "--tool", str(m / "run-evals.py"))
    rc_sm, out_sm = run("python3", SYNC_TEST, "--tool", str(m / "sync-evals.py"))
    shutil.rmtree(b, ignore_errors=True)
    shutil.rmtree(m, ignore_errors=True)
    runs = [r.strip() for rs in tail.ci_runs().values() for r in rs]
    run_name, sync_name = tail.ci_name(f"python3 {RUN_TEST}"), tail.ci_name(f"python3 {SYNC_TEST}")
    ci_ok = runs.count(f"python3 {RUN_TEST}") == 1 and runs.count(f"python3 {SYNC_TEST}") == 1 \
        and "스무 경우" in run_name and "열다섯 경우" in sync_name \
        and all(w in run_name for w in ("없는 킷", "못 읽")) and "못 읽" in sync_name
    return report({"run_tail": f"[{last(out_r)}]", "run_ok": rc_r == 0 and last(out_r) == "경우 20 개 중 통과 20",
                   "sync_tail": f"[{last(out_s)}]", "sync_ok": rc_s == 0 and last(out_s) == "경우 15 개 중 통과 15",
                   "run_base_fails": fails_of(out_rb), "run_base_ok": rc_rb == 1 and fails_of(out_rb) == "10,11,12,13,14,17,18,19",
                   "sync_base_fails": fails_of(out_sb), "sync_base_ok": rc_sb == 1 and fails_of(out_sb) == "7,8,9,10,11,14,15",
                   "run_mut_fails": fails_of(out_rm), "run_mut_ok": rc_rm == 1 and fails_of(out_rm) == "3,9,15,16,17,18",
                   "sync_mut_fails": fails_of(out_sm), "sync_mut_ok": rc_sm == 1 and fails_of(out_sm) == "2,6,12,13,14",
                   "ci_ok": ci_ok})


# ---- (B) 훅 둘을 레포로 ----
def missing_files(paths):
    """없는 파일 이름. 하나라도 있으면 그 조건은 불성립(1)으로 끝낸다 — 추적 출력으로 죽지 않게."""
    gone = [p for p in paths if not Path(p).is_file()]
    if gone:
        print(f"MISSING {' '.join(gone)}")
    return gone


def hook_env(home, **extra):
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_HOOK_LIB", "LINT_ORACLE_HOOK", "QA_PENDING_HOOK")}
    env.update(HOME=str(home), **extra)
    return env


def run_env(cmd, env):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    return r.returncode, r.stdout


def m_hook_tests():
    """스크립트-07: 훅 시험 둘이 설치본 없이(빈 HOME) 레포 본으로 두 로캘에서 통과 · 대역 훅 · 도우미 안 넘긴 사본 · 시작 판 시험은 실패."""
    if missing_files([f"{HOOK_DIR}/{f}" for f in COPIED]):
        return report({"ok": False})
    home = tmpdir("finhome.")
    got = {}
    for test in HOOK_TESTS:
        for loc in ("C", "en_US.UTF-8"):
            rc, out = run_env(["bash", test], hook_env(home, LC_ALL=loc))
            got[f"{Path(test).stem}:{loc}"] = rc == 0 and last(out) == "실패 0 건"
            print(f"{Path(test).name} LC_ALL={loc} rc={rc} tail=[{last(out)}]")
    stub = home / "stub-hook.sh"
    stub.write_text(HOOK_STUB, encoding="utf-8")
    stub_rcs, noexport_rcs, base_rcs = [], [], []
    for test in HOOK_TESTS:
        name = Path(test).name
        rc, out = run_env(["bash", test], hook_env(home, **{HOOK_ENV[name]: str(stub)}))
        stub_rcs.append(rc)
        print(f"stub {name} rc={rc} tail=[{last(out)}]")
        # 도우미 경로를 훅에 넘기지 않는 사본 — 훅이 빈 HOME 에서 도우미를 못 찾아 조용히 끝난다
        mut = tmpdir("finnoexp.")
        for f in COPIED:
            shutil.copy(f"{HOOK_DIR}/{f}", mut / f)
        (mut / name).write_text(read(test).replace("export CLAUDE_HOOK_LIB=", "CLAUDE_HOOK_LIB="), encoding="utf-8")
        rc, out = run_env(["bash", str(mut / name)], hook_env(home))
        noexport_rcs.append(rc)
        print(f"noexport {name} rc={rc} tail=[{last(out)}]")
        shutil.rmtree(mut, ignore_errors=True)
        base = tmpdir("finhbase.")
        ev.show(BASE, test, base / name)
        rc, out = run_env(["bash", str(base / name)], hook_env(home))
        base_rcs.append(rc)
        print(f"base {name} rc={rc} tail=[{last(out)}]")
        shutil.rmtree(base, ignore_errors=True)
    shutil.rmtree(home, ignore_errors=True)
    return report({"runs": len(got), "pass": sum(got.values()), "ok": all(got.values()),
                   "stub_rcs": ",".join(map(str, stub_rcs)), "stub_ok": stub_rcs == [1, 1],
                   "noexport_rcs": ",".join(map(str, noexport_rcs)), "noexport_ok": noexport_rcs == [1, 1],
                   "base_rcs": ",".join(map(str, base_rcs)), "base_ok": base_rcs == [2, 2]})


DOCKER_SCRIPT = r'''
set -u
apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq jq zsh python3 >/dev/null 2>&1 || { echo "APT_FAIL"; exit 3; }
echo "awk=$(awk -W version 2>&1 | head -1)"
echo "grep=$(grep -V | head -1)"
cd /w
for t in harness/evals/hooks/lint-contract-oracle-test.sh harness/evals/hooks/qa-pending-check-test.sh; do
  bash "$t" > /tmp/o 2>&1; rc=$?; echo "RESULT $t rc=$rc tail=[$(tail -1 /tmp/o)]"
done
python3 scripts/test-check-user-hook-copies.py > /tmp/o 2>&1; rc=$?
echo "RESULT scripts/test-check-user-hook-copies.py rc=$rc tail=[$(tail -1 /tmp/o)]"
'''


def m_docker():
    """스크립트-08: 리눅스 도커(ubuntu:24.04 · LC_ALL=C.UTF-8 · GNU grep · mawk)에서 훅 시험 둘 · 맞대기 시험이 통과."""
    if shutil.which("docker") is None or subprocess.run(["docker", "info"], capture_output=True).returncode:
        print("DOCKER_UNAVAILABLE")
        return 2
    r = subprocess.run(["docker", "run", "--rm", "-v", f"{os.getcwd()}:/w:ro", "-e", "LC_ALL=C.UTF-8",
                        "ubuntu:24.04", "bash", "-c", DOCKER_SCRIPT], capture_output=True, text=True)
    out = r.stdout + r.stderr
    print("\n".join(l for l in out.splitlines() if l.startswith(("awk=", "grep=", "RESULT", "APT_FAIL"))))
    if "APT_FAIL" in out:
        return 2
    results = re.findall(r"^RESULT (\S+) rc=(\d+) tail=\[(.*)\]$", out, re.M)
    want_tail = {"lint-contract-oracle-test.sh": "실패 0 건", "qa-pending-check-test.sh": "실패 0 건",
                 "test-check-user-hook-copies.py": "경우 6 개 중 통과 6"}
    ok = len(results) == 3 and all(rc == "0" and t == want_tail[Path(p).name] for p, rc, t in results)
    return report({"results": len(results), "mawk": int("mawk" in out), "gnu_grep": int("GNU grep" in out), "ok": ok})


def checker_case(installed):
    rc, out = run("python3", CHECKER, "--installed", str(installed))
    return rc, out.splitlines()


def differ_names(lines):
    return sorted(l.split(" ")[1] for l in lines if l.startswith("다름:"))


def m_checker():
    """스크립트-09: 맞대기 검사 — 설치본 없음은 한 줄 · 0, 같으면 0, 한 글자 다르면 1, 이 맥의 설치본은 따로 맞댄 답과 같다."""
    if missing_files([CHECKER] + [f"{HOOK_DIR}/{f}" for f in COPIED]):
        return report({"ok": False})
    d = tmpdir("finchk.")
    rc_a, la = checker_case(d / "none")
    same = d / "same"
    same.mkdir()
    for f in COPIED:
        shutil.copy(f"{HOOK_DIR}/{f}", same / f)
    rc_b, lb = checker_case(same)
    flip = d / "flip"
    shutil.copytree(same, flip)
    data = bytearray((flip / "qa-pending-check.sh").read_bytes())
    data[-2] = ord("X") if data[-2] != ord("X") else ord("Y")
    (flip / "qa-pending-check.sh").write_bytes(bytes(data))
    rc_c, lc = checker_case(flip)
    shutil.rmtree(d, ignore_errors=True)
    # 이 맥의 설치본 — 이 도우미가 직접 바이트로 맞댄 답(알려진 답)과 검사 출력이 같은가
    present = [f for f in COPIED if (INSTALLED / f).is_file()]
    known = sorted(f for f in present if (INSTALLED / f).read_bytes() != Path(f"{HOOK_DIR}/{f}").read_bytes())
    rc_d, ld = checker_case(INSTALLED)
    want_rc_d = 0 if not present else (1 if known else 0)
    print(f"none rc={rc_a} lines={la}")
    print(f"same rc={rc_b} differ={differ_names(lb)}")
    print(f"flip rc={rc_c} differ={differ_names(lc)}")
    print(f"installed present={len(present)} known={known} rc={rc_d} differ={differ_names(ld)}")
    return report({"none_ok": rc_a == 0 and la == [SKIP_LINE], "same_ok": rc_b == 0 and not differ_names(lb),
                   "flip_ok": rc_c == 1 and differ_names(lc) == ["qa-pending-check.sh"],
                   "installed_ok": rc_d == want_rc_d and differ_names(ld) == known})


def m_checker_test():
    """스크립트-10: 맞대기 시험 — 끝 줄, 늘 건너뜀 대역은 경우 4 · 5 · 6 만 실패."""
    rc, out = run("python3", CHECKER_TEST)
    d = tmpdir("finstub.")
    (d / "stub.py").write_text(CHECKER_STUB, encoding="utf-8")
    rc_s, out_s = run("python3", CHECKER_TEST, "--tool", str(d / "stub.py"))
    shutil.rmtree(d, ignore_errors=True)
    return report({"tail": f"[{last(out)}]", "ok": rc == 0 and last(out) == "경우 6 개 중 통과 6",
                   "stub_fails": fails_of(out_s), "stub_ok": rc_s == 1 and fails_of(out_s) == "4,5,6"})


NEW_RUNS = [f"bash {HOOK_TESTS[0]}", f"bash {HOOK_TESTS[1]}", f"python3 {CHECKER_TEST}", f"python3 {CHECKER}"]


def m_ci():
    """스크립트-11: CI 에 새 단계 넷이 하나씩 있고, 시작 판의 run 단계는 모두 그대로 남는다(줄만 더한다)."""
    import yaml
    runs = [r.strip() for rs in tail.ci_runs().values() for r in rs if r.strip()]
    rc, base_text = git("show", f"{BASE}:.github/workflows/ci.yml")
    if rc:
        return 2
    base_runs = [s.get("run", "").strip() for j in yaml.safe_load(base_text)["jobs"].values()
                 for s in j.get("steps", []) if s.get("run", "").strip()]
    counts = {r: runs.count(r) for r in NEW_RUNS}
    # 개수만 보면 한 줄을 지우고 같은 글자를 딴 자리에 끼워도 통과한다 — 새 넷을 뺀 나머지가 차례까지 시작 판과 같아야 한다
    kept = [r for r in runs if r not in NEW_RUNS] == base_runs
    print(f"new={counts}")
    return report({"base_runs": len(base_runs), "runs": len(runs), "new_once": all(v == 1 for v in counts.values()),
                   "kept": kept, "added_only": len(runs) == len(base_runs) + len(NEW_RUNS)})


# ---- 구조 ----
def m_commits():
    """구조-01: 커밋 규칙 — tail 도우미의 규칙을 이 계약의 시작 판 · 범위 목록으로."""
    tail.BASE, tail.CONTRACT = BASE, CONTRACT
    return tail.m_commits()


def first_block(path):
    """파이썬은 첫 \"\"\" 덩어리, 셸은 첫 빈 줄 앞 주석 덩어리."""
    t = read(path) if Path(path).is_file() else ""
    if path.endswith(".py"):
        parts = t.split('"""')
        return parts[1] if len(parts) > 2 else ""
    return t.split("\n\n", 1)[0]


def m_usage():
    """구조-02: 도구 · 시험 설명 글."""
    need = {RUN_EVALS: ["객체", "항목 없는 킷"], SYNC_EVALS: ["객체"],
            RUN_TEST: ["  17. ", "  18. ", "  19. ", "  20. ", "객체가 아니다"],
            SYNC_TEST: ["  14. ", "  15. ", "객체가 아니다"],
            CHECKER: [SKIP_LINE], CHECKER_TEST: ["  6. "],
            HOOK_TESTS[0]: ["레포 본", "check-user-hook-copies.py"], HOOK_TESTS[1]: ["레포 본", "check-user-hook-copies.py"]}
    miss = [f"{Path(f).name}:{w.strip()}" for f, ws in need.items() for w in ws if w not in first_block(f)]
    stale = [Path(f).name for f in HOOK_TESTS if "CI 에 등록하지 않는다" in read(f)]
    return report({"miss": f"[{','.join(miss)}]", "stale": f"[{','.join(stale)}]", "ok": not miss and not stale})


def m_notes():
    """구조-03: 기록 파일."""
    t = read(NOTES) if Path(NOTES).is_file() else ""
    keys = ["객체가 아니다", "항목 없는 킷", "두 번째 읽기", "lint-contract-oracle.sh", "qa-pending-check.sh",
            "_lib-hook-payload.sh", "check-user-hook-copies", "도커", "판 번호", "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = set(re.findall(r"\b[0-9a-f]{8}\b", t))
    return report({"exists": bool(t), "miss": f"[{','.join(miss)}]", "keys_ok": bool(t) and not miss,
                   "hashes": len(hashes), "hashes_ok": len(hashes) >= 4})


WANT_HARNESS = sorted([f"A\t{HOOK_DIR}/_lib-hook-payload.sh", f"A\t{HOOK_DIR}/lint-contract-oracle.sh",
                       f"M\t{HOOK_TESTS[0]}", f"A\t{HOOK_DIR}/qa-pending-check.sh", f"M\t{HOOK_TESTS[1]}"])


def m_harness_diff():
    """구조-04: harness 아래 바뀐 파일이 정확히 다섯이고 훅 등록 파일에 새 이름이 없다."""
    rc, out = git("diff", "--name-status", f"{BASE}..{BRANCH}", "--", "harness")
    if rc:
        return 2
    got = sorted(l for l in out.splitlines() if l.strip())
    print("\n".join(got))
    hooks_json = read("harness/hooks/hooks.json")
    registered = [f for f in COPIED if f in hooks_json]
    return report({"files": len(got), "same_set": got == WANT_HARNESS, "registered": f"[{','.join(registered)}]",
                   "not_registered": not registered})


def m_copies():
    """구조-05: 세 파일을 처음 담은 커밋의 내용이 봉인 전 설치본 지문과 같고, 끝 판이 다르면 기록에 그 이름과 옮길 줄이 있다."""
    notes = read(NOTES) if Path(NOTES).is_file() else ""
    rows = {}
    for f, want in COPIED.items():
        path = f"{HOOK_DIR}/{f}"
        _, adds = git("log", "--diff-filter=A", "--format=%H", f"{BASE}..{BRANCH}", "--", path)
        adds = [a for a in adds.split() if a]
        first = None
        if len(adds) == 1:
            r = subprocess.run(["git", "show", f"{adds[0]}:{path}"], capture_output=True)
            first = sha16(r.stdout) if r.returncode == 0 else None
        r = subprocess.run(["git", "show", f"{BRANCH}:{path}"], capture_output=True)
        tip = sha16(r.stdout) if r.returncode == 0 else None
        tip_ok = tip == want or (tip is not None and f in notes and "설치본에 옮길 줄" in notes)
        rows[f] = len(adds) == 1 and first == want and tip_ok
        print(f"{f} adds={len(adds)} first={first} tip={tip} want={want}")
    return report({"files": len(rows), "ok": all(rows.values()) and len(rows) == 3})


def m_new_files():
    """재사용-02: scripts · .github 에 새로 생긴 파일은 맞대기 검사와 그 시험 둘뿐."""
    rc, out = git("diff", "--name-status", f"{BASE}..{BRANCH}", "--", "scripts", ".github")
    added = sorted(l.split("\t")[1] for l in out.splitlines() if l.startswith("A\t"))
    print(f"added={added}")
    return report({"added": len(added), "ok": rc == 0 and added == sorted([CHECKER, CHECKER_TEST])})


CONDS = {
    "스크립트-01": m_nonobject, "스크립트-02": m_normal, "스크립트-03": m_empty, "스크립트-04": m_named,
    "스크립트-05": m_second_read, "스크립트-01-base": m_base, "스크립트-06": m_eval_tests,
    "스크립트-07": m_hook_tests, "스크립트-08": m_docker, "스크립트-09": m_checker, "스크립트-10": m_checker_test,
    "스크립트-11": m_ci, "오류-01": ev.m_keep, "오류-02": ev.m_cx_keep,
    "구조-01": m_commits, "구조-02": m_usage, "구조-03": m_notes, "구조-04": m_harness_diff, "구조-05": m_copies,
    "재사용-02": m_new_files,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
