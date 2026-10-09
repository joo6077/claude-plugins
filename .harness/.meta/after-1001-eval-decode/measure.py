"""계약 after-1001-eval-decode 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

킷 셋 임시 트리 · 킷 칸 나누기 · 요약 줄은 앞 묶음 ev2(after-1001-eval-item-shape) 도우미와 그 도우미가 부르는
fin · ev · tail 도우미를 불러 쓴다. 종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
임시 폴더는 TMPDIR 아래 만든다. 레포 파일에는 쓰지 않는다.
"""
import importlib.util
import re
import shutil
import sys
from pathlib import Path

BASE = "9390bf96"  # 시작 판 — chore/ak3-ev2 끝 (ev2 QA 승인 뒤 기록 커밋)
CONTRACT = ".harness/sprint-contract-after-1001-eval-decode.md"
NOTES = ".harness/.meta/after-kaizen-0928/ev3-notes.md"
EV2 = ".harness/.meta/after-1001-eval-item-shape/measure.py"
RUN_EVALS, RUN_TEST = "scripts/run-evals.py", "scripts/test-run-evals.py"
SYNC_EVALS, SYNC_TEST = "scripts/sync-evals.py", "scripts/test-sync-evals.py"
MARKET = ".claude-plugin/marketplace.json"

GOOD_ITEM = '{"id":1,"skill":"s","prompt":"p","expected_output":"e","assertions":[{"text":"a","type":"output"}]}'
# 평가 파일 읽기 오류 셋 — (이름표, b/evals/evals.json 바이트, 그 줄에 함께 있어야 할 낱말(대소문자 무시))
READ_ERRORS = [
    ("bad-utf8", ('{"evals":[' + GOOD_ITEM.replace('"prompt":"p"', '"prompt":"p\udcff"') + ']}')
     .encode("utf-8", "surrogateescape"), ["utf-8"]),
    ("big-number", ('{"evals":[' + GOOD_ITEM.replace('"id":1', '"id":' + "1" * 5000) + ']}').encode(), []),
    ("deep-nest", ('{"evals":[' + GOOD_ITEM + '],"x":' + "[" * 200000 + "]" * 200000 + "}").encode(), []),
]
# 마켓 목록 읽기 오류 셋 — None 은 파일을 지운다
MARKET_ERRORS = [
    ("market-utf8", b'{"plugins":[{"name":"a","source":"./a\xff"}]}\n'),
    ("market-broken", b"{ broken\n"),
    ("market-missing", None),
]
# 어떤 평가 파일이든 잘못된 UTF-8 로 치는 지나친 판 — 정상 킷도 못 읽은 킷으로 센다
OVERSTRICT = '''import pathlib
_real_read_text = pathlib.Path.read_text
def _strict_read_text(self, *a, **k):
    if self.name == "evals.json":
        raise UnicodeDecodeError("utf-8", b"\\xff", 0, 1, "invalid start byte")
    return _real_read_text(self, *a, **k)
pathlib.Path.read_text = _strict_read_text
'''


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ev2 = load("ev2", EV2)
fin, ev, tail = ev2.fin, ev2.ev, ev2.tail
read, git, run, last, report = ev.read, ev.git, ev.run, ev.last, ev.report
tmpdir, fails_of, run_tree, TOOLS = ev.tmpdir, ev.fails_of, ev.run_tree, ev.TOOLS
content_tree, summary_lines, measured, blocks = fin.content_tree, fin.summary_lines, fin.measured, ev.blocks


def tool_dir(rev=None, prefix=""):
    """rev 판 도구 셋을 임시 폴더에. rev 가 None 이면 작업 폴더 판. prefix 는 두 실행기 맨 앞에 붙인다."""
    d = tmpdir("ev3tool.")
    for name in ("run-evals.py", "sync-evals.py", "plugin_utils.py"):
        if rev:
            ev.show(rev, f"scripts/{name}", d / name)
        else:
            shutil.copy(f"scripts/{name}", d / name)
        if prefix and name != "plugin_utils.py":
            (d / name).write_text(prefix + (d / name).read_text(encoding="utf-8"), encoding="utf-8")
    return d


def kit_tree(root, tools, data, extra):
    """킷 셋 트리를 만들고 가운데 킷 b 의 평가 파일을 바이트 그대로 바꾼다."""
    content_tree(root, tools, {"b": GOOD_ITEM}, extra=extra)
    (root / "b/evals/evals.json").write_bytes(data)


def line_ok(out, where, words):
    return any(where in l and all(w in l.lower() for w in words) for l in out.splitlines())


def read_matrix(tools, shapes=READ_ERRORS):
    """가운데 킷 b 만 읽기 오류 — 세 도구 모두 2 · 그 줄 · 추적 출력 없음 · a c 는 잼 · 요약 줄 · b 바이트 그대로."""
    right = total = 0
    for label, data, words in shapes:
        for name, cmd in TOOLS:
            d = tmpdir("ev3read.")
            kit_tree(d / "t", tools, data, extra=True)
            rc, out = run_tree(d / "t", cmd, [])
            kept = (d / "t/b/evals/evals.json").read_bytes() == data
            shutil.rmtree(d, ignore_errors=True)
            line = line_ok(out, "b/evals/evals.json", words)
            trace = "Traceback" in out
            meas = measured(name, "a", out) and measured(name, "c", out)
            summ = summary_lines(out) == ["못 읽은 킷 1 개: b"]
            ok = rc == 2 and line and not trace and meas and summ and kept
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} b-{label} {name} rc={rc} line={int(line)} trace={int(trace)} "
                  f"measured={int(meas)} summary={int(summ)} kept={int(kept)}")
    return total, right


def named_matrix(tools):
    right = 0
    for label, data, words in READ_ERRORS:
        d = tmpdir("ev3named.")
        kit_tree(d / "t", tools, data, extra=False)
        rc, out = run_tree(d / "t", ["python3", "scripts/run-evals.py", "b"], [])
        shutil.rmtree(d, ignore_errors=True)
        ok = rc == 2 and line_ok(out, "b/evals/evals.json", words) and "Traceback" not in out \
            and "못 읽은 킷 1 개: b" in out
        right += ok
        print(f"{'OK ' if ok else 'BAD'} named b-{label} rc={rc} tail=[{last(out)}]")
    return len(READ_ERRORS), right


def market_matrix(tools):
    """마켓 목록 읽기 오류 — 세 도구 모두 2 · 마켓 목록 경로가 든 줄 · 추적 출력 없음 · 킷 칸 없음."""
    right = total = 0
    for label, data in MARKET_ERRORS:
        for name, cmd in TOOLS:
            d = tmpdir("ev3market.")
            content_tree(d / "t", tools, {}, extra=True)
            market = d / "t" / MARKET
            if data is None:
                market.unlink()
            else:
                market.write_bytes(data)
            rc, out = run_tree(d / "t", cmd, [])
            shutil.rmtree(d, ignore_errors=True)
            line = line_ok(out, MARKET, [])
            trace = "Traceback" in out
            heads = sum(l.startswith("→ ") for l in out.splitlines())
            ok = rc == 2 and line and not trace and heads == 0
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} {label} {name} rc={rc} line={int(line)} trace={int(trace)} heads={heads}")
    return total, right


def skills_dir_matrix(tools):
    """가운데 킷 b 의 skills 폴더를 못 읽음 — sync 두 도구 모두 2 · 그 폴더 경로가 든 줄 · 추적 출력 없음 · a c 는 잼 · 요약 줄."""
    right = total = 0
    for name, cmd in TOOLS:
        if not name.startswith("sync"):
            continue
        d = tmpdir("ev3dir.")
        content_tree(d / "t", tools, {}, extra=True)
        locked = d / "t/b/skills"
        locked.chmod(0)
        try:
            rc, out = run_tree(d / "t", cmd, [])
        finally:
            locked.chmod(0o755)
        shutil.rmtree(d, ignore_errors=True)
        line = line_ok(out, "b/skills", [])
        trace = "Traceback" in out
        meas = measured(name, "a", out) and measured(name, "c", out)
        summ = summary_lines(out) == ["못 읽은 킷 1 개: b"]
        ok = rc == 2 and line and not trace and meas and summ
        total += 1
        right += ok
        print(f"{'OK ' if ok else 'BAD'} b-skills-dir {name} rc={rc} line={int(line)} trace={int(trace)} "
              f"measured={int(meas)} summary={int(summ)}")
    return total, right


def m_skills_dir():
    """스크립트-07: sync 가 읽는 skills 폴더를 못 읽는 킷."""
    if not ev.rootless():
        print("ROOT 권한을 빼도 읽힌다 — 잴 수 없음")
        return 2
    total, right = skills_dir_matrix(Path("scripts").resolve())
    return report({"cases": total, "right": right, "ok": right == total})


def m_read():
    """스크립트-01: 평가 파일 읽기 오류 셋 × 세 도구."""
    total, right = read_matrix(Path("scripts").resolve())
    return report({"cases": total, "right": right, "ok": right == total})


def m_named():
    """스크립트-02: 이름으로 준 킷 b 가 읽기 오류면 2 · 그 줄 · 추적 출력 없음 · 요약 줄."""
    total, right = named_matrix(Path("scripts").resolve())
    return report({"cases": total, "right": right, "ok": right == total})


def m_market():
    """스크립트-03: 마켓 목록 읽기 오류 셋 × 세 도구."""
    total, right = market_matrix(Path("scripts").resolve())
    return report({"cases": total, "right": right, "ok": right == total})


def m_base():
    """스크립트-01 ~ 03 · 07 의 음성 대조 — 시작 판 도구는 스물세 경우를 하나도 맞히지 못한다."""
    d = tool_dir(BASE)
    t1, r1 = read_matrix(d)
    t2, r2 = named_matrix(d)
    t3, r3 = market_matrix(d)
    t4, r4 = skills_dir_matrix(d)
    shutil.rmtree(d, ignore_errors=True)
    return report({"cases": t1 + t2 + t3 + t4, "base_right": r1 + r2 + r3 + r4,
                   "base_all_wrong": r1 + r2 + r3 + r4 == 0})


def good_cases(tools):
    """킷 셋 모두 정상(extra 없음) — 세 도구 0 · 세 칸 · 오류 글자 없음 · run 은 칸마다 PASS 줄."""
    right = 0
    for name, cmd in TOOLS:
        d = tmpdir("ev3good.")
        content_tree(d / "t", tools, {}, extra=False)
        rc, out = run_tree(d / "t", cmd, [])
        shutil.rmtree(d, ignore_errors=True)
        got = blocks(out)
        three = sorted(got) == ["a", "b", "c"]
        clean = not any(w in out for w in ("ERROR", "UNREADABLE", "Traceback", "못 읽은 킷"))
        passed = name != "run" or all("PASS: 1 passed, 0 failed" in got.get(k, "") for k in "abc")
        ok = rc == 0 and three and clean and passed
        right += ok
        print(f"{'OK ' if ok else 'BAD'} all-good {name} rc={rc} three={int(three)} clean={int(clean)} passed={int(passed)}")
    return len(TOOLS), right


def m_good():
    """스크립트-04: 정상 킷 셋은 그대로 넘긴다. 음성 대조 — 지나친 판은 셋 모두 틀린다."""
    total, right = good_cases(Path("scripts").resolve())
    mut = tool_dir(prefix=OVERSTRICT)
    _, mut_right = good_cases(mut)
    shutil.rmtree(mut, ignore_errors=True)
    return report({"cases": total, "right": right, "ok": right == total, "mut_right": mut_right, "mut_ok": mut_right == 0})


def m_tests():
    """스크립트-05: 평가 시험 둘 — 끝 줄 · 시작 판은 새 읽기 오류 경우만 실패 · 지나친 판은 정상 킷 셋 경우 실패 · CI 이름."""
    rc_r, out_r = run("python3", RUN_TEST)
    rc_s, out_s = run("python3", SYNC_TEST)
    b = tool_dir(BASE)
    rc_rb, out_rb = run("python3", RUN_TEST, "--tool", str(b / "run-evals.py"))
    rc_sb, out_sb = run("python3", SYNC_TEST, "--tool", str(b / "sync-evals.py"))
    m = tool_dir(prefix=OVERSTRICT)
    rc_rm, out_rm = run("python3", RUN_TEST, "--tool", str(m / "run-evals.py"))
    rc_sm, out_sm = run("python3", SYNC_TEST, "--tool", str(m / "sync-evals.py"))
    shutil.rmtree(b, ignore_errors=True)
    shutil.rmtree(m, ignore_errors=True)
    run_mut = set(fails_of(out_rm).split(","))
    sync_mut = set(fails_of(out_sm).split(","))
    runs = [r.strip() for rs in tail.ci_runs().values() for r in rs]
    run_name, sync_name = tail.ci_name(f"python3 {RUN_TEST}"), tail.ci_name(f"python3 {SYNC_TEST}")
    ci_ok = runs.count(f"python3 {RUN_TEST}") == 1 and runs.count(f"python3 {SYNC_TEST}") == 1 \
        and "서른여덟 경우" in run_name and "서른네 경우" in sync_name \
        and "잘못된 UTF-8" in run_name and "잘못된 UTF-8" in sync_name
    return report({"run_tail": f"[{last(out_r)}]", "run_ok": rc_r == 0 and last(out_r) == "경우 38 개 중 통과 38",
                   "sync_tail": f"[{last(out_s)}]", "sync_ok": rc_s == 0 and last(out_s) == "경우 34 개 중 통과 34",
                   "run_base_fails": fails_of(out_rb), "run_base_ok": rc_rb == 1 and fails_of(out_rb) == "34,35,36,37",
                   "sync_base_fails": fails_of(out_sb), "sync_base_ok": rc_sb == 1 and fails_of(out_sb) == "29,30,31,32,33",
                   "run_mut_fails": fails_of(out_rm), "run_mut_ok": rc_rm == 1 and "38" in run_mut,
                   "sync_mut_fails": fails_of(out_sm), "sync_mut_ok": rc_sm == 1 and "34" in sync_mut,
                   "ci_ok": ci_ok})


def m_target():
    """스크립트-06: target_skill 읽는 줄이 없고, 그 열쇠를 가진 항목은 그대로 모르는 열쇠 구조 오류다."""
    _, hits = git("grep", "-n", "target_skill", "--", "scripts", ".github")
    hits = [h for h in hits.splitlines() if h.strip()]
    for h in hits:
        print(f"HIT {h}")
    shape = [("target-skill", '{"evals":[' + GOOD_ITEM.replace('"skill":"s"', '"skill":"s","target_skill":"s"') + ']}',
              ["1 번째 항목", "target_skill"])]
    total, right = ev2.bad_matrix(Path("scripts").resolve(), shape)
    return report({"hits": len(hits), "hits_ok": not hits, "cases": total, "right": right, "ok": right == total})


def keep_run(tools, tag):
    return ev2.keep_run(tools, tag)


def m_keep():
    """오류-01: 레포 평가 파일 전부로 돌린 열한 명령의 종료 코드 · 출력이 시작 판과 글자까지 같다."""
    new_outs, plain, unchanged = keep_run(Path("scripts").resolve(), "n")
    b = tool_dir(BASE)
    base_outs, _, _ = keep_run(b, "b")
    shutil.rmtree(b, ignore_errors=True)
    m = tool_dir(prefix=OVERSTRICT)
    mut_outs, _, _ = keep_run(m, "m")
    shutil.rmtree(m, ignore_errors=True)
    same = 0
    for args, (rc, out), base in zip(ev2.KEEP_CMDS, new_outs, base_outs):
        ok = (rc, out) == base and rc == 0
        same += ok
        print(f"{'OK ' if ok else 'BAD'} {'sync --check-only' if args is None else 'run ' + ' '.join(args)} "
              f"rc={rc} base_rc={base[0]} tail=[{last(out)}]")
    totals = [last(new_outs[0][1]), last(new_outs[1][1])]
    print(f"totals={totals} sync_plain rc={plain[0]} unchanged={int(unchanged)}")
    mut_differs = sum((rc, out) != base for (rc, out), base in zip(mut_outs, base_outs))
    n = len(ev2.KEEP_CMDS)
    return report({"cmds": n, "same": same, "ok": same == n,
                   "totals_ok": totals == ["Total: 122 passed, 0 failed", "Total: 0 added, 0 orphans, 0 missing (preview)"],
                   "plain_ok": plain[0] == 0 and unchanged, "mut_differs": mut_differs, "mut_ok": mut_differs == n})


# 앞 묶음 ev2 측정 가운데 이번 변경 뒤에도 그대로 0 이어야 하는 것
PRIOR = [(EV2, c) for c in ("스크립트-01", "스크립트-01-base", "스크립트-02", "스크립트-03", "스크립트-05",
                            "오류-01", "오류-02", "구조-02")]


def m_prior():
    """오류-02: 앞 묶음 ev2 측정 여덟 개가 그대로 종료 코드 0."""
    rcs = []
    for helper, cond in PRIOR:
        rc, out = run("python3", helper, cond)
        rcs.append(rc)
        print(f"{'OK ' if rc == 0 else 'BAD'} {Path(helper).parent.name} {cond} rc={rc} tail=[{last(out)}]")
    return report({"cases": len(PRIOR), "zero": rcs.count(0), "ok": rcs.count(0) == len(PRIOR)})


def m_commits():
    """구조-01: 커밋 규칙 — tail 도우미의 규칙을 이 계약의 시작 판 · 범위 목록으로."""
    tail.BASE, tail.CONTRACT = BASE, CONTRACT
    return tail.m_commits()


def m_usage():
    """구조-02: 도구 · 시험 설명 글(첫 \"\"\" 덩어리)."""
    need = {RUN_EVALS: ["잘못된 UTF-8", "마켓 목록"], SYNC_EVALS: ["잘못된 UTF-8", "마켓 목록"],
            RUN_TEST: ["  34 ~ 36. ", "  37. ", "  38. ", "잘못된 UTF-8"],
            SYNC_TEST: ["  29 ~ 31. ", "  32. ", "  33. ", "  34. ", "잘못된 UTF-8"]}
    miss = [f"{Path(f).name}:{w.strip()}" for f, ws in need.items() for w in ws if w not in fin.first_block(f)]
    return report({"miss": f"[{','.join(miss)}]", "ok": not miss})


def m_notes():
    """구조-03: 기록 파일."""
    t = read(NOTES) if Path(NOTES).is_file() else ""
    keys = ["잘못된 UTF-8", "target_skill", "마켓 목록", "skills 폴더", "run-evals", "sync-evals", "못 읽은 킷", "122",
            "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = set(re.findall(r"\b[0-9a-f]{8}\b", t))
    return report({"exists": bool(t), "miss": f"[{','.join(miss)}]", "keys_ok": bool(t) and not miss,
                   "hashes": len(hashes), "hashes_ok": len(hashes) >= 3})


CONDS = {
    "스크립트-01": m_read, "스크립트-02": m_named, "스크립트-03": m_market, "스크립트-01-base": m_base,
    "스크립트-04": m_good, "스크립트-05": m_tests, "스크립트-06": m_target, "스크립트-07": m_skills_dir, "오류-01": m_keep, "오류-02": m_prior,
    "구조-01": m_commits, "구조-02": m_usage, "구조-03": m_notes,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
