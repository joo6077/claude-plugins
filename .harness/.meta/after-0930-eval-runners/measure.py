"""계약 after-0930-eval-runners 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

CI 단계 읽기 · 커밋 규칙은 앞 묶음 tail(after-0929-tail) 도우미를 불러 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
임시 폴더는 TMPDIR 아래 만든다. 레포 파일에는 쓰지 않는다.
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "fe6704d8"  # 시작 판 — origin/main (PR #126 합침)
HERE = ".harness/.meta/after-0930-eval-runners"
CONTRACT = ".harness/sprint-contract-after-0930-eval-runners.md"
NOTES = ".harness/.meta/after-kaizen-0928/ev-notes.md"
TAIL = ".harness/.meta/after-0929-tail/measure.py"
CX_REPRO = ".harness/.meta/after-0929-codex-silent-pass/repro.sh"
ABSENT = ".harness/.meta/after-0928-harness-checks-r2/m-evals-absent.sh"
RUN_EVALS, RUN_TEST = "scripts/run-evals.py", "scripts/test-run-evals.py"
SYNC_EVALS, SYNC_TEST = "scripts/sync-evals.py", "scripts/test-sync-evals.py"
UTILS = "scripts/plugin_utils.py"
KAIZEN = ".claude/skills/backend-kaizen/SKILL.md"
KAIZEN_OLD = "`sys.exit(2)` 로 즉시 종료하는 구조 유지"
KITS = ["a", "b", "c"]
# 바로가기 판정을 늘 참으로 바꾸는 변이 — 진짜 없는 평가 파일도 못 읽음으로 치는 지나친 판
LEXISTS_TRUE = "import os\nos.path.lexists = lambda _p: True\n"
SKILL_MD = "---\nname: {0}\ndescription: d\nuser-invocable: true\n---\n\n본문\n"
GOOD_EVALS = ('{"evals":[{"id":1,"skill":"s","prompt":"p","expected_output":"e",'
              '"assertions":[{"text":"a","type":"output"}]}]}\n')
# 도구 셋 — (이름, 명령). sync-plain 은 옵션 없이 돈다(뼈대 항목을 쓴다 — 임시 트리 안에서만)
TOOLS = [("run", ["python3", "scripts/run-evals.py"]),
         ("sync-check", ["python3", "scripts/sync-evals.py", "--check-only"]),
         ("sync-plain", ["python3", "scripts/sync-evals.py"])]
# 킷별로 「쟀다」 는 증거 — 도구마다 그 킷 칸(→ <킷> 줄부터 다음 → 줄 앞까지)에 있어야 할 글
MEASURED = {"run": "PASS: 1 passed, 0 failed", "sync-check": "[{0}] MISSING: extra", "sync-plain": "[{0}] added 1 skeleton entries"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tail = load("tail", TAIL)
fs2 = tail.fs2
read, git, run, last, report = fs2.read, fs2.git, tail.run, tail.last, tail.report


def tmpdir(prefix):
    return Path(tempfile.mkdtemp(prefix=prefix, dir=os.environ.get("TMPDIR") or None))


def show(rev, path, out):
    """rev 판의 path 를 out 에 꺼낸다. 못 꺼내면 잴 수 없음(2)으로 멈춘다."""
    rc, text = git("show", f"{rev}:{path}")
    if rc:
        print(f"NO_REV {rev}:{path}")
        raise SystemExit(2)
    Path(out).write_text(text, encoding="utf-8")
    return Path(out)


def rootless():
    """권한을 빼면 못 읽는지 — root 로 돌면 못 읽는 경우를 만들 수 없다."""
    d = tmpdir("evperm.")
    p = d / "x"
    p.write_text("x", encoding="utf-8")
    p.chmod(0)
    ok = not os.access(p, os.R_OK)
    p.chmod(0o644)
    shutil.rmtree(d, ignore_errors=True)
    return ok


def fails_of(out):
    return ",".join(sorted(re.findall(r"^FAIL 경우 (\d+)", out, re.M), key=int))


# ---- 킷 셋 임시 트리 ----
def tree(root, tool_dir, shapes, extra):
    """킷 a · b · c 를 가진 임시 트리. shapes[킷] 은 good · absent · dangling · unreadable · broken.
    extra 가 참이면 읽히는 킷마다 평가에 없는 스킬 `extra` 를 더 둔다 — sync 가 그 킷을 쟀다는 증거 줄을 내게."""
    (root / "scripts").mkdir(parents=True)
    for name in ("run-evals.py", "sync-evals.py", "plugin_utils.py"):
        shutil.copy(Path(tool_dir) / name, root / "scripts" / name)
    (root / ".claude-plugin").mkdir()
    plugins = ",".join(f'{{"name":"{k}","source":"./{k}"}}' for k in KITS)
    (root / ".claude-plugin/marketplace.json").write_text(f'{{"plugins":[{plugins}]}}\n', encoding="utf-8")
    locked = []
    for k in KITS:
        shape = shapes.get(k, "good")
        skills = ["s", "extra"] if extra and shape == "good" else ["s"]
        for s in skills:
            (root / k / "skills" / s).mkdir(parents=True)
            (root / k / "skills" / s / "SKILL.md").write_text(SKILL_MD.format(s), encoding="utf-8")
        if shape == "absent":
            continue
        (root / k / "evals").mkdir()
        p = root / k / "evals/evals.json"
        if shape == "dangling":
            os.symlink("missing.json", p)
        elif shape == "broken":
            p.write_text("{ broken\n", encoding="utf-8")
        else:
            p.write_text(GOOD_EVALS, encoding="utf-8")
            if shape == "unreadable":
                locked.append(p)
    return locked


def run_tree(root, cmd, locked):
    for p in locked:
        p.chmod(0)
    try:
        r = subprocess.run(cmd, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                           env=dict(os.environ, PYTHONUNBUFFERED="1"))
    finally:
        for p in locked:
            p.chmod(0o644)
    return r.returncode, r.stdout


def blocks(out):
    """→ <킷> 줄부터 다음 → 줄 앞까지를 킷별로 묶는다. 마지막 칸은 끝까지."""
    got, cur = {}, None
    for line in out.splitlines():
        m = re.match(r"^→ (\S+)$", line)
        if m:
            cur = m.group(1)
            got[cur] = []
        elif cur:
            got[cur].append(line)
    return {k: "\n".join(v) for k, v in got.items()}


def measured(tool, kit, out):
    return MEASURED[tool].format(kit) in blocks(out).get(kit, "")


def summary_after(out, bad):
    """끝 줄 모양 `못 읽은 킷 N 개: <이름, …>` 이 마지막 → 줄보다 뒤에 정확히 한 번 있는가."""
    want = f"못 읽은 킷 {len(bad)} 개: {', '.join(bad)}"
    lines = out.splitlines()
    heads = [i for i, l in enumerate(lines) if l.startswith("→ ")]
    hits = [i for i, l in enumerate(lines) if l.strip() == want]
    return len(hits) == 1 and (not heads or hits[0] > heads[-1])


def bad_line(out, kit, shape):
    path = f"{kit}/evals/evals.json"
    lines = [l for l in out.splitlines() if path in l]
    if shape in ("dangling", "unreadable"):
        return any(l.startswith("UNREADABLE") for l in lines)
    return bool(lines)


def case_bad(tool_dir, name, cmd, shapes):
    """못 읽는 칸이 있는 경우 — 종료 코드 2, 못 읽은 킷마다 줄, 읽히는 킷은 쟀다는 증거, 끝에 요약 줄."""
    d = tmpdir("evbad.")
    locked = tree(d / "t", tool_dir, shapes, extra=True)
    rc, out = run_tree(d / "t", cmd, locked)
    shutil.rmtree(d, ignore_errors=True)
    bad = [k for k in KITS if shapes.get(k, "good") != "good"]
    good = [k for k in KITS if k not in bad]
    lines_ok = all(bad_line(out, k, shapes[k]) for k in bad)
    meas_ok = all(measured(name, k, out) for k in good)
    summ = summary_after(out, bad)
    ok = rc == 2 and lines_ok and meas_ok and summ
    return ok, f"rc={rc} line={int(lines_ok)} measured={int(meas_ok)} summary={int(summ)}"


def matrix(tool_dir, shape_sets):
    right = total = 0
    for label, shapes in shape_sets:
        for name, cmd in TOOLS:
            ok, info = case_bad(tool_dir, name, cmd, shapes)
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} {label} {name} {info}")
    return total, right


def m_dangling():
    """스크립트-01: 가운데 킷 b 의 평가 파일이 대상 없는 바로가기면 세 도구 모두 2 · UNREADABLE 줄 · a c 는 잼 · 요약 줄."""
    total, right = matrix(Path("scripts").resolve(), [("b-dangling", {"b": "dangling"})])
    return report({"cases": total, "right": right, "ok": right == total})


def absent_cases(tool_dir):
    """진짜 없는 평가 파일 · 모두 정상 — 세 도구 모두 0, 없는 킷은 「대상 아님」 줄에, UNREADABLE 줄 없음."""
    right = total = 0
    for label, shapes in (("b-absent", {"b": "absent"}), ("all-good", {})):
        for name, cmd in TOOLS:
            d = tmpdir("evabs.")
            tree(d / "t", tool_dir, shapes, extra=False)
            rc, out = run_tree(d / "t", cmd, [])
            shutil.rmtree(d, ignore_errors=True)
            listed = any(l.startswith("평가 파일(evals/evals.json) 없는 킷 1 개 — 대상 아님: b") for l in out.splitlines())
            ok = rc == 0 and "UNREADABLE" not in out and (listed if shapes else "대상 아님" not in out)
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} {label} {name} rc={rc} listed={int(listed)}")
    return total, right


def mutant_dir(tag):
    """W 도구 셋 사본에 바로가기 판정을 늘 참으로 바꾸는 줄을 앞에 붙인다."""
    d = tmpdir(f"evmut{tag}.")
    for name in ("run-evals.py", "sync-evals.py"):
        (d / name).write_text(LEXISTS_TRUE + read(f"scripts/{name}"), encoding="utf-8")
    shutil.copy(UTILS, d / "plugin_utils.py")
    return d


def m_absent():
    """스크립트-02: 진짜 없는 평가 파일은 지금처럼 대상 아님 · 0. 음성 대조 — 바로가기 판정을 늘 참으로 바꾼 변이는 b-absent 에서 셋 다 틀린다."""
    total, right = absent_cases(Path("scripts").resolve())
    lex = sum(read(f).count("os.path.lexists") for f in (RUN_EVALS, SYNC_EVALS))
    mut = mutant_dir("abs")
    rights = 0
    for name, cmd in TOOLS:
        d = tmpdir("evabsm.")
        tree(d / "t", mut, {"b": "absent"}, extra=False)
        rc, _ = run_tree(d / "t", cmd, [])
        shutil.rmtree(d, ignore_errors=True)
        rights += rc == 0
        print(f"mutant b-absent {name} rc={rc}")
    shutil.rmtree(mut, ignore_errors=True)
    return report({"cases": total, "right": right, "ok": right == total, "lexists_uses": lex,
                   "mut_right": rights, "mut_ok": rights == 0})


BAD_SETS = [("b-unreadable", {"b": "unreadable"}), ("b-broken", {"b": "broken"}),
            ("ac-unreadable", {"a": "unreadable", "c": "unreadable"})]


def m_middle():
    """스크립트-03: 못 읽는 칸이 있어도 나머지 킷을 재고, 못 읽은 킷 이름을 모두 적은 뒤 2."""
    if not rootless():
        print("ROOT 권한을 빼도 읽힌다")
        return 2
    total, right = matrix(Path("scripts").resolve(), BAD_SETS)
    return report({"cases": total, "right": right, "ok": right == total})


def base_dir():
    d = tmpdir("evbase.")
    for f in (RUN_EVALS, SYNC_EVALS, UTILS):
        show(BASE, f, d / Path(f).name)
    return d


def m_base():
    """스크립트-01 · 03 의 음성 대조 — 시작 판 도구는 못 읽는 칸 네 모양 모두에서 틀린다."""
    if not rootless():
        return 2
    d = base_dir()
    total, right = matrix(d, [("b-dangling", {"b": "dangling"})] + BAD_SETS)
    shutil.rmtree(d, ignore_errors=True)
    return report({"cases": total, "base_right": right, "base_all_wrong": right == 0})


def m_tests():
    """스크립트-04: 시험 두 파일 — 끝 줄 · 시작 판 도구로 새 걸릴 경우만 실패 · 변이로 넘길 경우만 실패 · CI 이름."""
    rc_r, out_r = run("python3", RUN_TEST)
    rc_s, out_s = run("python3", SYNC_TEST)
    b = base_dir()
    rc_rb, out_rb = run("python3", RUN_TEST, "--tool", str(b / "run-evals.py"))
    rc_sb, out_sb = run("python3", SYNC_TEST, "--tool", str(b / "sync-evals.py"))
    m = mutant_dir("t")
    rc_rm, out_rm = run("python3", RUN_TEST, "--tool", str(m / "run-evals.py"))
    rc_sm, out_sm = run("python3", SYNC_TEST, "--tool", str(m / "sync-evals.py"))
    shutil.rmtree(b, ignore_errors=True)
    shutil.rmtree(m, ignore_errors=True)
    runs = [r.strip() for rs in tail.ci_runs().values() for r in rs]
    run_name, sync_name = tail.ci_name(f"python3 {RUN_TEST}"), tail.ci_name(f"python3 {SYNC_TEST}")
    ci_ok = runs.count(f"python3 {RUN_TEST}") == 1 and runs.count(f"python3 {SYNC_TEST}") == 1 \
        and "아홉 경우" in run_name and "여섯 경우" in sync_name
    return report({"run_tail": f"[{last(out_r)}]", "run_ok": rc_r == 0 and last(out_r) == "경우 9 개 중 통과 9",
                   "sync_tail": f"[{last(out_s)}]", "sync_ok": rc_s == 0 and last(out_s) == "경우 6 개 중 통과 6",
                   "run_base_fails": fails_of(out_rb), "run_base_ok": rc_rb == 1 and fails_of(out_rb) == "7,9",
                   "sync_base_fails": fails_of(out_sb), "sync_base_ok": rc_sb == 1 and fails_of(out_sb) == "4,6",
                   "run_mut_fails": fails_of(out_rm), "run_mut_ok": rc_rm == 1 and fails_of(out_rm) == "8",
                   "sync_mut_fails": fails_of(out_sm), "sync_mut_ok": rc_sm == 1 and fails_of(out_sm) == "5",
                   "ci_ok": ci_ok})


# ---- 그대로 지킬 동작 ----
def m_keep():
    """오류-01: 레포에서 인자 없는 두 실행기 · 킷 이름 소비처 셋이 0, 이름으로 준 대상 없는 바로가기 킷은 2."""
    right = 0
    cmds = [["python3", RUN_EVALS, "--verbose"], ["python3", SYNC_EVALS, "--check-only"],
            ["python3", RUN_EVALS, "tone-kit", "--verbose"], ["python3", RUN_EVALS, "backend-kit"],
            ["python3", RUN_EVALS, "infra-kit"]]
    for cmd in cmds:
        rc, out = run(*cmd)
        right += rc == 0
        print(f"{'OK ' if rc == 0 else 'BAD'} {' '.join(cmd[1:])} rc={rc} tail=[{last(out)}]")
    d = tmpdir("evnamed.")
    tree(d / "t", Path("scripts").resolve(), {"b": "dangling"}, extra=False)
    rc_n, out_n = run_tree(d / "t", ["python3", "scripts/run-evals.py", "b"], [])
    shutil.rmtree(d, ignore_errors=True)
    named_ok = rc_n == 2 and "b" in out_n
    print(f"{'OK ' if named_ok else 'BAD'} named b-dangling rc={rc_n} tail=[{last(out_n)}]")
    # 앞 묶음 측정 m-evals-absent.sh — 레포의 「대상 아님」 목록 · 종료 코드가 시작 판과 HEAD 에서 같은가
    _, ab = run("bash", ABSENT, os.getcwd(), BASE)
    _, ah = run("bash", ABSENT, os.getcwd(), "HEAD")
    strip = lambda o: [re.sub(r"^(\S+) \S+ ", r"\1 ", l) for l in o.splitlines() if l.strip()]
    absent_same = len(strip(ab)) == 2 and strip(ab) == strip(ah)
    print(f"absent base={strip(ab)} head={strip(ah)}")
    return report({"cases": len(cmds) + 1, "right": right + named_ok, "ok": right == len(cmds) and named_ok,
                   "absent_same": absent_same})


CX_KEEP = ["d2 broken-json rc=2 msg=1", "d2 good rc=0", "d4 unreadable rc=2 msg=1", "d4 good rc=0",
           "d6 empty-list rc=2 msg=1", "d6 no-key rc=2 msg=1", "d6 good rc=0"]


def m_cx_keep():
    """오류-02: 앞 묶음 cx 재현의 결함 2 · 4 · 6 줄 일곱이 그대로다."""
    rc, out = run("bash", CX_REPRO, os.getcwd(), str(Path.home() / ".claude/hooks"))
    got = [l.strip() for l in out.splitlines() if re.match(r"^d[246] ", l)]
    for l in got:
        print(l)
    return report({"lines": len(got), "same": got == CX_KEEP})


# ---- 구조 ----
def m_commits():
    """구조-01: 커밋 규칙 — tail 도우미의 규칙을 이 계약의 시작 판 · 범위 목록으로."""
    tail.BASE, tail.CONTRACT = BASE, CONTRACT
    return tail.m_commits()


def head(path):
    t = read(path)
    parts = t.split('"""')
    return parts[1] if len(parts) > 2 else ""


def m_usage():
    """구조-02: 도구 · 시험 설명 글."""
    need = {RUN_EVALS: ["바로가기", "나머지"], SYNC_EVALS: ["바로가기", "나머지"],
            RUN_TEST: ["  7. ", "  8. ", "  9. ", "바로가기"], SYNC_TEST: ["  4. ", "  5. ", "  6. ", "바로가기"]}
    miss = [f"{Path(f).name}:{w.strip()}" for f, ws in need.items() for w in ws if w not in head(f)]
    return report({"miss": f"[{','.join(miss)}]", "ok": not miss})


def m_kaizen():
    """스킬-01: backend-kaizen 10 번 항목이 「즉시 종료」 대신 「나머지를 재고 끝에 2」 를 적는다."""
    t = read(KAIZEN)
    line = next((l for l in t.splitlines() if l.startswith("10. **run-evals.py")), "")
    old = KAIZEN_OLD in t
    ok = bool(line) and not old and "나머지" in line and "2" in line and "sync-evals.py" in line
    return report({"line": int(bool(line)), "old": int(old), "ok": ok})


def m_notes():
    """구조-03: 기록 파일."""
    t = read(NOTES) if Path(NOTES).is_file() else ""
    keys = ["lexists", "run-evals", "sync-evals", "바로가기", "못 읽은 킷", "backend-kaizen", "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = set(re.findall(r"\b[0-9a-f]{8}\b", t))
    return report({"exists": bool(t), "miss": f"[{','.join(miss)}]", "keys_ok": bool(t) and not miss,
                   "hashes": len(hashes), "hashes_ok": len(hashes) >= 3})


def m_frontmatter():
    """금지-04: backend-kaizen 머리말(첫 --- 부터 다음 --- 까지)이 시작 판과 같다."""
    def fm(text):
        m = re.match(r"---\n.*?\n---\n", text, re.S)
        return m.group(0) if m else None
    rc, base = git("show", f"{BASE}:{KAIZEN}")
    now, was = fm(read(KAIZEN)), fm(base) if rc == 0 else None
    return report({"found": now is not None and was is not None, "same": now is not None and now == was})


CONDS = {
    "스크립트-01": m_dangling, "스크립트-02": m_absent, "스크립트-03": m_middle, "스크립트-03-base": m_base,
    "스크립트-04": m_tests, "오류-01": m_keep, "오류-02": m_cx_keep,
    "구조-01": m_commits, "구조-02": m_usage, "구조-03": m_notes, "스킬-01": m_kaizen, "금지-04": m_frontmatter,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
