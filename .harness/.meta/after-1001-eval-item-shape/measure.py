"""계약 after-1001-eval-item-shape 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

킷 셋 임시 트리 · 킷 칸 나누기는 앞 묶음 fin(after-0930-final) · ev(after-0930-eval-runners) 도우미를,
CI 단계 읽기 · 커밋 규칙은 그 도우미들이 부르는 tail(after-0929-tail) 도우미를 불러 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
임시 폴더는 TMPDIR 아래 만든다. 레포 파일에는 쓰지 않는다.
"""
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

BASE = "b33ed94a"  # 시작 판 — origin/main (PR #128 합침)
BRANCH = "chore/ak3-ev2"
CONTRACT = ".harness/sprint-contract-after-1001-eval-item-shape.md"
NOTES = ".harness/.meta/after-kaizen-0928/ev2-notes.md"
FIN = ".harness/.meta/after-0930-final/measure.py"
RUN_EVALS, RUN_TEST = "scripts/run-evals.py", "scripts/test-run-evals.py"
SYNC_EVALS, SYNC_TEST = "scripts/sync-evals.py", "scripts/test-sync-evals.py"

GOOD_ITEM = '{"id":1,"skill":"s","prompt":"p","expected_output":"e","assertions":[{"text":"a","type":"output"}]}'
AGENT_ITEM = '{"id":2,"agent":"s","prompt":"p","expected_output":"e","assertions":["a"]}'
API_ITEM = ('{"id":1,"skill":"s","prompt":"p","expect":{"n":1},"assertions":[{"text":"a","type":"output"}],'
            '"example":"x","fixture":"f"}')


def wrap(item, key="evals"):
    return f'{{"{key}":[{item}]}}'


def swap(item, old, new):
    assert old in item, old
    return item.replace(old, new, 1)


# 깨진 모양 아홉 — (이름표, evals.json 내용, 그 줄에 함께 있어야 할 낱말)
BROKEN = [
    ("item-number", '{"evals":[1]}', ["1 번째 항목", "객체가 아니다"]),
    ("list-object", '{"evals":{"x":1}}', ["evals", "목록이 아니다"]),
    ("list-string", '{"evals":"abc"}', ["evals", "목록이 아니다"]),
    ("list-null", '{"evals":null}', ["evals", "목록이 아니다"]),
    ("no-prompt", wrap(swap(GOOD_ITEM, '"prompt":"p",', "")), ["1 번째 항목", "prompt"]),
    ("skill-number", wrap(swap(GOOD_ITEM, '"skill":"s"', '"skill":5')), ["1 번째 항목", "skill"]),
    ("assertion-number", wrap(swap(GOOD_ITEM, '[{"text":"a","type":"output"}]', "[5]")), ["1 번째 항목", "assertions"]),
    ("unknown-key", wrap(swap(GOOD_ITEM, '"prompt":"p"', '"prompt":"p","promt":"p"')), ["1 번째 항목", "promt"]),
    ("second-item", f'{{"evals":[{GOOD_ITEM},1]}}', ["2 번째 항목", "객체가 아니다"]),
]
# 레포 평가 파일이 실제로 쓰는 모양 셋 — 넘겨야 한다
GOOD = [
    ("react-shape", '{"tests":[{"id":"r1","skill":"s","prompt":"p","expected_output":"e","assertions":["a"]}]}'),
    ("api-shape", wrap(API_ITEM, "cases")),
    ("agent-item", f'{{"evals":[{GOOD_ITEM},{AGENT_ITEM}]}}'),
]
# 허용 목록 경계 — 아는 열쇠마다 다른 값 모양, 꼭 있어야 할 열쇠 빠짐, 둘 중 하나 규칙 어김
PROBES = [
    ("id-bool", wrap(swap(GOOD_ITEM, '"id":1', '"id":true')), ["1 번째 항목", "id"]),
    ("skill-number", wrap(swap(GOOD_ITEM, '"skill":"s"', '"skill":5')), ["1 번째 항목", "skill"]),
    ("agent-number", wrap(swap(AGENT_ITEM, '"agent":"s"', '"agent":5')), ["1 번째 항목", "agent"]),
    ("prompt-number", wrap(swap(GOOD_ITEM, '"prompt":"p"', '"prompt":5')), ["1 번째 항목", "prompt"]),
    ("expected-number", wrap(swap(GOOD_ITEM, '"expected_output":"e"', '"expected_output":5')),
     ["1 번째 항목", "expected_output"]),
    ("expect-string", wrap(swap(API_ITEM, '"expect":{"n":1}', '"expect":"x"')), ["1 번째 항목", "expect"]),
    ("assertions-string", wrap(swap(GOOD_ITEM, '[{"text":"a","type":"output"}]', '"a"')), ["1 번째 항목", "assertions"]),
    ("example-number", wrap(swap(API_ITEM, '"example":"x"', '"example":5')), ["1 번째 항목", "example"]),
    ("fixture-number", wrap(swap(API_ITEM, '"fixture":"f"', '"fixture":5')), ["1 번째 항목", "fixture"]),
    ("assertion-extra-key", wrap(swap(GOOD_ITEM, '"type":"output"}', '"type":"output","x":1}')),
     ["1 번째 항목", "assertions"]),
    ("assertion-text-number", wrap(swap(GOOD_ITEM, '"text":"a"', '"text":5')), ["1 번째 항목", "assertions"]),
    ("no-id", wrap(swap(GOOD_ITEM, '"id":1,', "")), ["1 번째 항목", "id"]),
    ("no-assertions", wrap(swap(GOOD_ITEM, ',"assertions":[{"text":"a","type":"output"}]', "")),
     ["1 번째 항목", "assertions"]),
    ("no-skill-agent", wrap(swap(GOOD_ITEM, '"skill":"s",', "")), ["1 번째 항목", "skill"]),
    ("skill-and-agent", wrap(swap(GOOD_ITEM, '"skill":"s"', '"skill":"s","agent":"s"')), ["1 번째 항목", "agent"]),
    ("no-expected-expect", wrap(swap(GOOD_ITEM, '"expected_output":"e",', "")), ["1 번째 항목", "expected_output"]),
    ("expected-and-expect", wrap(swap(GOOD_ITEM, '"expected_output":"e"', '"expected_output":"e","expect":{"n":1}')),
     ["1 번째 항목", "expect"]),
]
# 봉인 전(2026-10-01) 레포 평가 파일을 센 모양 — run-evals.py 가 읽는 9 킷(howto-kit 은 SKIP) 122 항목
KNOWN_FIELDS = {"agent": ["str"], "assertions": ["list"], "example": ["str"], "expect": ["dict"],
                "expected_output": ["str"], "fixture": ["str"], "id": ["int", "str"], "prompt": ["str"],
                "skill": ["str"]}
KNOWN_ASSERTIONS = ["dict:text,type", "str"]
KNOWN_KITS = {"harness": 7, "flutter-toolkit": 24, "design-kit": 30, "backend-kit": 8, "infra-kit": 6,
              "rust-kit": 17, "react-kit": 21, "tone-kit": 4, "api-kit": 5}
# 아는 모양도 모두 깨진 것으로 치는 지나친 판 — 평가 파일 항목마다 모르는 열쇠 하나를 끼워 읽는다
STRICT = '''import json
_real_loads = json.loads
def _strict_loads(s, *a, **k):
    data = _real_loads(s, *a, **k)
    if isinstance(data, dict) and "plugins" not in data:
        for key in ("evals", "tests", "cases"):
            if isinstance(data.get(key), list):
                for item in data[key]:
                    if isinstance(item, dict):
                        item["__x"] = 1
    return data
json.loads = _strict_loads
'''


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fin = load("fin", FIN)
ev, tail = fin.ev, fin.tail
read, git, run, last, report = ev.read, ev.git, ev.run, ev.last, ev.report
tmpdir, fails_of, run_tree, TOOLS, KITS = ev.tmpdir, ev.fails_of, ev.run_tree, ev.TOOLS, ev.KITS
content_tree, summary_lines, measured = fin.content_tree, fin.summary_lines, fin.measured


def tool_dir(rev=None, prefix=""):
    """rev 판 도구 셋(run-evals · sync-evals · plugin_utils)을 임시 폴더에. rev 가 None 이면 작업 폴더 판.
    prefix 를 주면 두 실행기 맨 앞에 붙인다."""
    d = tmpdir("ev2tool.")
    for name in ("run-evals.py", "sync-evals.py", "plugin_utils.py"):
        if rev:
            ev.show(rev, f"scripts/{name}", d / name)
        else:
            shutil.copy(f"scripts/{name}", d / name)
        if prefix and name != "plugin_utils.py":
            (d / name).write_text(prefix + (d / name).read_text(encoding="utf-8"), encoding="utf-8")
    return d


def line_ok(out, kit, words):
    return any(f"{kit}/evals/evals.json" in l and all(w in l for w in words) for l in out.splitlines())


def bad_matrix(tools, shapes):
    """가운데 킷 b 만 깨진 모양 — 세 도구 모두 2 · 그 줄 · 추적 출력 없음 · a c 는 잼 · 요약 줄 · sync-plain 은 b 그대로."""
    right = total = 0
    for label, text, words in shapes:
        for name, cmd in TOOLS:
            d = tmpdir("ev2bad.")
            content_tree(d / "t", tools, {"b": text}, extra=True)
            before = (d / "t/b/evals/evals.json").read_bytes()
            rc, out = run_tree(d / "t", cmd, [])
            kept = (d / "t/b/evals/evals.json").read_bytes() == before
            shutil.rmtree(d, ignore_errors=True)
            line = line_ok(out, "b", words)
            trace = "Traceback" in out
            meas = measured(name, "a", out) and measured(name, "c", out)
            summ = summary_lines(out) == ["못 읽은 킷 1 개: b"]
            ok = rc == 2 and line and not trace and meas and summ and kept
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} b-{label} {name} rc={rc} line={int(line)} trace={int(trace)} "
                  f"measured={int(meas)} summary={int(summ)} kept={int(kept)}")
    return total, right


def m_broken():
    """스크립트-01: 깨진 모양 아홉 × 세 도구."""
    total, right = bad_matrix(Path("scripts").resolve(), BROKEN)
    return report({"cases": total, "right": right, "ok": right == total})


def m_broken_base():
    """스크립트-01 · 03 · 05 의 음성 대조 — 시작 판 도구는 깨진 모양 · 경계 모양에서 하나도 맞히지 못한다."""
    d = tool_dir(BASE)
    total, right = bad_matrix(d, BROKEN + PROBES)
    n_total, n_right = named_matrix(d)
    shutil.rmtree(d, ignore_errors=True)
    return report({"cases": total + n_total, "base_right": right + n_right, "base_all_wrong": right + n_right == 0})


def good_cases(tools):
    right = total = 0
    for label, text in GOOD:
        for name, cmd in TOOLS:
            d = tmpdir("ev2good.")
            content_tree(d / "t", tools, {"b": text}, extra=False)
            rc, out = run_tree(d / "t", cmd, [])
            shutil.rmtree(d, ignore_errors=True)
            clean = not any(w in out for w in ("ERROR", "UNREADABLE", "Traceback", "못 읽은 킷"))
            ok = rc == 0 and clean
            total += 1
            right += ok
            print(f"{'OK ' if ok else 'BAD'} b-{label} {name} rc={rc} clean={int(clean)}")
    return total, right


def m_good():
    """스크립트-02: 레포가 쓰는 정상 모양 셋 × 세 도구는 0. 음성 대조 — 지나친 판은 아홉 모두 틀린다."""
    total, right = good_cases(Path("scripts").resolve())
    mut = tool_dir(prefix=STRICT)
    _, mut_right = good_cases(mut)
    shutil.rmtree(mut, ignore_errors=True)
    return report({"cases": total, "right": right, "ok": right == total, "mut_right": mut_right, "mut_ok": mut_right == 0})


def named_matrix(tools):
    right = 0
    for label, text, words in BROKEN:
        d = tmpdir("ev2named.")
        content_tree(d / "t", tools, {"b": text}, extra=False)
        rc, out = run_tree(d / "t", ["python3", "scripts/run-evals.py", "b"], [])
        shutil.rmtree(d, ignore_errors=True)
        ok = rc == 2 and line_ok(out, "b", words) and "Traceback" not in out and "못 읽은 킷 1 개: b" in out
        right += ok
        print(f"{'OK ' if ok else 'BAD'} named b-{label} rc={rc} tail=[{last(out)}]")
    return len(BROKEN), right


def m_named():
    """스크립트-03: 이름으로 준 킷 b 가 깨진 모양이면 2 · 그 줄 · 추적 출력 없음 · 요약 줄."""
    total, right = named_matrix(Path("scripts").resolve())
    return report({"cases": total, "right": right, "ok": right == total})


def m_tests():
    """스크립트-04: 평가 시험 둘 — 끝 줄 · 시작 판 도구로 새 깨진 모양 경우만 실패 · 지나친 판으로 정상 모양 경우가 모두 실패 · CI 이름."""
    rc_r, out_r = run("python3", RUN_TEST)
    rc_s, out_s = run("python3", SYNC_TEST)
    b = tool_dir(BASE)
    rc_rb, out_rb = run("python3", RUN_TEST, "--tool", str(b / "run-evals.py"))
    rc_sb, out_sb = run("python3", SYNC_TEST, "--tool", str(b / "sync-evals.py"))
    m = tool_dir(prefix=STRICT)
    rc_rm, out_rm = run("python3", RUN_TEST, "--tool", str(m / "run-evals.py"))
    rc_sm, out_sm = run("python3", SYNC_TEST, "--tool", str(m / "sync-evals.py"))
    shutil.rmtree(b, ignore_errors=True)
    shutil.rmtree(m, ignore_errors=True)
    run_mut = set(fails_of(out_rm).split(","))
    sync_mut = set(fails_of(out_sm).split(","))
    runs = [r.strip() for rs in tail.ci_runs().values() for r in rs]
    run_name, sync_name = tail.ci_name(f"python3 {RUN_TEST}"), tail.ci_name(f"python3 {SYNC_TEST}")
    ci_ok = runs.count(f"python3 {RUN_TEST}") == 1 and runs.count(f"python3 {SYNC_TEST}") == 1 \
        and "서른세 경우" in run_name and "스물여덟 경우" in sync_name \
        and "항목 모양" in run_name and "항목 모양" in sync_name
    return report({"run_tail": f"[{last(out_r)}]", "run_ok": rc_r == 0 and last(out_r) == "경우 33 개 중 통과 33",
                   "sync_tail": f"[{last(out_s)}]", "sync_ok": rc_s == 0 and last(out_s) == "경우 28 개 중 통과 28",
                   "run_base_fails": fails_of(out_rb),
                   "run_base_ok": rc_rb == 1 and fails_of(out_rb) == "21,22,23,24,25,26,27,28,29,30",
                   "sync_base_fails": fails_of(out_sb),
                   "sync_base_ok": rc_sb == 1 and fails_of(out_sb) == "16,17,18,19,20,21,22,23,24,25",
                   "run_mut_fails": fails_of(out_rm),
                   "run_mut_ok": rc_rm == 1 and {"3", "15", "16", "31", "32", "33"} <= run_mut,
                   "sync_mut_fails": fails_of(out_sm),
                   "sync_mut_ok": rc_sm == 1 and {"2", "12", "13", "26", "27", "28"} <= sync_mut,
                   "ci_ok": ci_ok})


def census():
    """run-evals.py 가 읽는 킷의 평가 파일 항목 모양을 센다."""
    names = [p["name"] for p in json.loads(read(".claude-plugin/marketplace.json"))["plugins"]]
    fields, forms, kits = {}, set(), {}
    for kit in names:
        p = Path(kit) / "evals/evals.json"
        if kit == "howto-kit" or not p.is_file():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        items = [e for key in ("evals", "tests", "cases") if isinstance(data.get(key), list) for e in data[key]]
        kits[kit] = len(items)
        for e in items:
            for k, v in (e.items() if isinstance(e, dict) else [("<항목>", e)]):
                fields.setdefault(k, set()).add(type(v).__name__)
            for a in (e.get("assertions") if isinstance(e, dict) and isinstance(e.get("assertions"), list) else []):
                forms.add("dict:" + ",".join(sorted(a)) if isinstance(a, dict) else type(a).__name__)
    return {k: sorted(v) for k, v in sorted(fields.items())}, sorted(forms), kits


def m_allowlist():
    """스크립트-05: 허용 목록이 레포가 쓰는 모양과 같다 — 센 모양이 봉인 값과 같고, 경계 모양 열일곱 × 세 도구는 2."""
    fields, forms, kits = census()
    print(f"census fields={fields}")
    print(f"census assertions={forms} kits={kits}")
    total, right = bad_matrix(Path("scripts").resolve(), PROBES)
    return report({"census_ok": fields == KNOWN_FIELDS and forms == KNOWN_ASSERTIONS and kits == KNOWN_KITS,
                   "cases": total, "right": right, "ok": right == total})


def mirror(root, tools):
    """레포 평가에 쓰이는 파일만 옮긴 임시 트리 — 마켓 목록 · 킷마다 평가 파일 · SKILL.md · 에이전트 글 · 도구 셋."""
    (root / "scripts").mkdir(parents=True)
    for name in ("run-evals.py", "sync-evals.py", "plugin_utils.py"):
        shutil.copy(Path(tools) / name, root / "scripts" / name)
    (root / ".claude-plugin").mkdir()
    shutil.copy(".claude-plugin/marketplace.json", root / ".claude-plugin/marketplace.json")
    for p in json.loads(read(".claude-plugin/marketplace.json"))["plugins"]:
        kit = Path(p["name"])
        files = [kit / "evals/evals.json"] if (kit / "evals/evals.json").is_file() else []
        files += sorted(kit.glob("skills/*/SKILL.md")) + sorted(kit.glob("agents/*.md"))
        for f in files:
            (root / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, root / f)


KEEP_CMDS = [["--verbose"], None] + [[k, "--verbose"] for k in KNOWN_KITS]


def keep_run(tools, tag):
    d = tmpdir(f"ev2keep{tag}.")
    mirror(d / "t", tools)
    outs = []
    for args in KEEP_CMDS:
        cmd = ["python3", "scripts/sync-evals.py", "--check-only"] if args is None \
            else ["python3", "scripts/run-evals.py", *args]
        outs.append(run_tree(d / "t", cmd, []))
    evals = sorted((d / "t").glob("*/evals/evals.json"))
    before = [p.read_bytes() for p in evals]
    plain = run_tree(d / "t", ["python3", "scripts/sync-evals.py"], [])
    unchanged = [p.read_bytes() for p in evals] == before
    shutil.rmtree(d, ignore_errors=True)
    return outs, plain, unchanged


def m_keep():
    """오류-01: 정상 입력 전체 대조 — 레포 평가 파일 전부로 돌린 열한 명령의 종료 코드 · 출력이 시작 판과 글자까지 같다."""
    new_outs, plain, unchanged = keep_run(Path("scripts").resolve(), "n")
    b = tool_dir(BASE)
    base_outs, _, _ = keep_run(b, "b")
    shutil.rmtree(b, ignore_errors=True)
    m = tool_dir(prefix=STRICT)
    mut_outs, _, _ = keep_run(m, "m")
    shutil.rmtree(m, ignore_errors=True)
    same = 0
    for args, (rc, out), base in zip(KEEP_CMDS, new_outs, base_outs):
        ok = (rc, out) == base and rc == 0
        same += ok
        print(f"{'OK ' if ok else 'BAD'} {'sync --check-only' if args is None else 'run ' + ' '.join(args)} "
              f"rc={rc} base_rc={base[0]} tail=[{last(out)}]")
    totals = [last(new_outs[0][1]), last(new_outs[1][1])]
    print(f"totals={totals} sync_plain rc={plain[0]} unchanged={int(unchanged)}")
    mut_differs = sum((rc, out) != base for (rc, out), base in zip(mut_outs, base_outs))
    return report({"cmds": len(KEEP_CMDS), "same": same, "ok": same == len(KEEP_CMDS),
                   "totals_ok": totals == ["Total: 122 passed, 0 failed", "Total: 0 added, 0 orphans, 0 missing (preview)"],
                   "plain_ok": plain[0] == 0 and unchanged,
                   "mut_differs": mut_differs, "mut_ok": mut_differs == len(KEEP_CMDS)})


# 앞 묶음 측정 가운데 이번 변경 뒤에도 그대로 0 이어야 하는 것
PRIOR = [(".harness/.meta/after-0930-final/measure.py", c) for c in
         ("스크립트-01", "스크립트-02", "스크립트-03", "스크립트-04", "스크립트-05")] + \
        [(".harness/.meta/after-0930-eval-runners/measure.py", c) for c in
         ("스크립트-01", "스크립트-02", "스크립트-03", "오류-01", "오류-02")]


def m_prior():
    """오류-02: 앞 묶음 평가 실행기 측정 열 개가 그대로 종료 코드 0."""
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
    need = {RUN_EVALS: ["항목 모양", "허용 목록"], SYNC_EVALS: ["항목 모양", "허용 목록"],
            RUN_TEST: ["  21 ~ 29. ", "  30. ", "  31 ~ 33. ", "항목 모양"],
            SYNC_TEST: ["  16 ~ 24. ", "  25. ", "  26 ~ 28. ", "항목 모양"]}
    miss = [f"{Path(f).name}:{w.strip()}" for f, ws in need.items() for w in ws if w not in fin.first_block(f)]
    return report({"miss": f"[{','.join(miss)}]", "ok": not miss})


def m_notes():
    """구조-03: 기록 파일."""
    t = read(NOTES) if Path(NOTES).is_file() else ""
    keys = ["항목 모양", "허용 목록", "run-evals", "sync-evals", "못 읽은 킷", "122", "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = set(re.findall(r"\b[0-9a-f]{8}\b", t))
    return report({"exists": bool(t), "miss": f"[{','.join(miss)}]", "keys_ok": bool(t) and not miss,
                   "hashes": len(hashes), "hashes_ok": len(hashes) >= 3})


CONDS = {
    "스크립트-01": m_broken, "스크립트-01-base": m_broken_base, "스크립트-02": m_good, "스크립트-03": m_named,
    "스크립트-04": m_tests, "스크립트-05": m_allowlist, "오류-01": m_keep, "오류-02": m_prior,
    "구조-01": m_commits, "구조-02": m_usage, "구조-03": m_notes,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
