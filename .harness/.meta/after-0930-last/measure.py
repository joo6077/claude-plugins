"""계약 after-0930-last 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

쪽 글 읽기 · 넘침 · 밖 자원 · 커밋 규칙은 앞 묶음 tail(after-0929-tail) 도우미와 그것이 부르는 rest · fs2 도우미를 불러 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "0928bf65"  # 시작 판 — tail 이 합쳐진 chore/after-kaizen-0928 끝
CX = "chore/ak3-cx"  # check-superseded.sh 새 출력 모양을 가진 가지 (아직 통합 가지에 안 합쳐졌다)
HERE = ".harness/.meta/after-0930-last"
CONTRACT = ".harness/sprint-contract-after-0930-last.md"
NOTES = ".harness/.meta/after-kaizen-0928/last-notes.md"
TAIL = ".harness/.meta/after-0929-tail/measure.py"
SKILL = "harness/skills/sprint-contract/SKILL.md"
SCHEMA_MD, SCHEMA_PAGE = "harness/references/contract-schema.md", "docs/harness/contract-schema.html"
MM_CHECK, MM_TEST = "scripts/check-docs-mermaid.js", "scripts/test-check-docs-mermaid.js"
FLOWS, REF = "docs/planning-kit/flows.html", "docs/planning-kit/reference.html"
FRONT = "---\ntitle: 흐름 예시\n---\n"
# 사본 모양 — (이름, 쪽, 찾을 정규식, 바꿀 글(\1 = 앞 태그), 기대 종료 코드, 기대 끝 줄 또는 None)
# 앞 태그는 `<pre …>` 부터 그림 종류 이름 바로 앞까지다. 구현이 `<pre>` 에 이름표를 붙여도 그대로 맞는다
FLOW_HEAD = r'(<pre[^>]*><code><span class="kw">)flowchart LR'
REF_XY = r"(<pre[^>]*>)xychart-beta"
REF_MIND = r"(<pre[^>]*>)mindmap"
MUTATIONS = {
    "flows-typo": (FLOWS, FLOW_HEAD, r"\1flowchat LR", 1, None),
    "ref-typo": (REF, REF_XY, r"\1xychat-beta", 1, None),
    "flows-front-typo": (FLOWS, FLOW_HEAD, r"\1" + FRONT + "flowchat LR", 1, None),
    "flows-front": (FLOWS, FLOW_HEAD, r"\1" + FRONT + "flowchart LR", 0, "쪽 1 · 예시 4 · 안 그려진 예시 0"),
    "ref-front": (REF, REF_MIND, r"\1" + FRONT + "mindmap", 0, "쪽 1 · 예시 3 · 안 그려진 예시 0"),
}
GOOD = '<pre>flowchart LR\n  A[&quot;시작&quot;] --&gt; B[&quot;끝&quot;]</pre>'
SIGN_RE = re.compile(r"^Claude .+ <noreply@anthropic\.com>$")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tail = load("tail", TAIL)
rest, fs2 = tail.rest, tail.fs2
read, git, run, last, report = fs2.read, fs2.git, tail.run, tail.last, tail.report


def tmpdir(prefix):
    return tempfile.mkdtemp(prefix=prefix, dir=os.environ.get("TMPDIR") or None)


def base_check():
    """시작 판 Mermaid 검사를 레포 scripts/ 옆 임시 이름으로 꺼낸다 — node_modules 를 레포에서 찾게."""
    rc, out = git("show", f"{BASE}:{MM_CHECK}")
    if rc:
        raise SystemExit(2)
    p = Path("scripts") / f".base-check-docs-mermaid-{os.getpid()}.js"
    p.write_text(out, encoding="utf-8")
    return p


def mutated(name, root):
    """사본 쪽 하나를 root/docs/planning-kit/<name>.html 로 만든다. 찾을 글이 정확히 한 곳이 아니면 None."""
    page, pat, repl, _, _ = MUTATIONS[name]
    h = read(page)
    hits = len(re.findall(pat, h))
    if hits != 1:
        print(f"NOT_APPLIED {name} hits={hits}")
        return None
    out = Path(root) / "docs/planning-kit" / f"{name}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(re.sub(pat, repl, h, count=1), encoding="utf-8")
    return out


def run_mutations(names, check=MM_CHECK):
    """사본마다 검사를 돌려 (종료 코드 · 끝 줄 · 쪽 이름이 출력에 있는가) 를 찍고 기대와 맞는지 센다."""
    d = tmpdir("lastmm.")
    right = 0
    for n in names:
        p = mutated(n, d)
        if p is None:
            return None
        want_rc, want_tail = MUTATIONS[n][3], MUTATIONS[n][4]
        rc, out = run("node", str(Path(check).resolve()), str(p))
        ok = rc == want_rc and (want_tail is None or last(out) == want_tail) and (rc != 1 or f"{n}.html" in out)
        right += ok
        print(f"{'OK ' if ok else 'BAD'} {n} rc={rc} want={want_rc} tail=[{last(out)}]")
    shutil.rmtree(d, ignore_errors=True)
    return right


def m_typo():
    """스크립트-01: 그림 종류 이름이 틀린 예시(머리말 유무 둘 다)를 안 그려짐으로 잡는다 — flows · reference 사본 셋."""
    names = ["flows-typo", "ref-typo", "flows-front-typo"]
    right = run_mutations(names)
    if right is None:
        return 2
    return report({"cases": len(names), "right": right, "ok": right == len(names)})


def m_front():
    """스크립트-02: 머리말 붙은 정상 예시를 그려짐으로 센다 — flows · reference 사본 둘에서 쪽 예시 수가 원래대로다."""
    names = ["flows-front", "ref-front"]
    right = run_mutations(names)
    if right is None:
        return 2
    return report({"cases": len(names), "right": right, "ok": right == len(names)})


def m_repo():
    """스크립트-03: 레포 전체는 그대로 쪽 3 · 예시 9 · 0, Mermaid 가 아닌 이름표 붙은 `<pre>` 만 있는 쪽은 예시 0 (종료 코드 3)."""
    rc, out = run("node", MM_CHECK)
    d = Path(tmpdir("lastshell."))
    page = d / "shell.html"
    page.write_text('<!DOCTYPE html><html><body><pre aria-label="셸 명령 예시">ls -la</pre>'
                    '<pre aria-label="Reflection YAML 스키마">key: value</pre></body></html>\n', encoding="utf-8")
    rc_s, out_s = run("node", MM_CHECK, str(page))
    return report({"rc": rc, "tail": f"[{last(out)}]", "repo_ok": rc == 0 and last(out) == "쪽 3 · 예시 9 · 안 그려진 예시 0",
                   "shell_rc": rc_s, "shell_ok": rc_s == 3})


def js_head(path):
    t = read(path) if Path(path).is_file() else ""
    m = re.search(r"/\*\*(.*?)\*/", t, re.S)
    return m.group(1) if m else ""


def m_test():
    """스크립트-04: 시험 여덟 경우 · 시작 판 검사 사본은 경우 5 · 6 · 7 만 실패 · 늘 0 인 가짜 검사도 잡힘 · CI 이름."""
    rc_t, out_t = run("node", MM_TEST)
    base = base_check()
    try:
        rc_b, out_b = run("node", MM_TEST, "--check", str(base))
    finally:
        base.unlink()
    fails = sorted(re.findall(r"^FAIL 경우 (\d+)", out_b, re.M))
    d = Path(tmpdir("laststub."))
    stub = d / "stub-check.js"
    stub.write_text("console.log('쪽 0 · 예시 0 · 안 그려진 예시 0');\nprocess.exit(0);\n", encoding="utf-8")
    rc_s, _ = run("node", MM_TEST, "--check", str(stub))
    runs = tail.ci_runs().get("playwright", [])
    idx = {r.strip(): i for i, r in enumerate(runs)}
    npm = idx.get("npm ci", -1)
    ci_ok = runs.count(f"node {MM_TEST}") == 1 and idx.get(f"node {MM_TEST}", -1) > npm >= 0 \
        and "여덟 경우" in tail.ci_name(f"node {MM_TEST}")
    head_ok = "여덟 경우" in js_head(MM_TEST) or all(f"  {i}. " in js_head(MM_TEST) for i in range(5, 9))
    return report({"test_rc": rc_t, "test_tail": f"[{last(out_t)}]", "test_ok": rc_t == 0 and last(out_t) == "경우 8 개 중 통과 8",
                   "base_rc": rc_b, "base_fails": ",".join(fails), "base_ok": rc_b == 1 and fails == ["5", "6", "7"],
                   "stub_rc": rc_s, "stub_ok": rc_s == 1, "head_ok": head_ok, "ci_ok": ci_ok})


def m_empty():
    """오류-01: 이름표 붙은 빈 예시는 건너뛰지 않고 안 그려진 예시로 센다 — 좋은 예시 하나와 함께 둔 쪽이 종료 코드 1."""
    d = Path(tmpdir("lastempty."))
    page = d / "empty.html"
    page.write_text(f'<!DOCTYPE html><html><body>{GOOD}<pre aria-label="Mermaid flowchart 예시"></pre></body></html>\n',
                    encoding="utf-8")
    rc, out = run("node", MM_CHECK, str(page))
    return report({"rc": rc, "tail": f"[{last(out)}]", "ok": rc == 1 and last(out) == "쪽 1 · 예시 2 · 안 그려진 예시 1"})


def m_tail_keep():
    """오류-02: 앞 묶음 tail 측정 스크립트-04(레포 쪽 9 예시 · 괄호 깨진 사본 잡기)가 이 판에서도 통과한다."""
    rc, out = run(sys.executable, TAIL, "스크립트-04")
    print(last(out))
    return report({"tail_rc": rc, "ok": rc == 0})


def skill_block(text):
    """SKILL.md 의 check-superseded 안내 — 「적은 뒤 `check-superseded.sh`」 줄부터 다음 「**결과:」 줄 바로 앞 글 줄까지."""
    lines = text.splitlines()
    s = next((i for i, l in enumerate(lines) if "적은 뒤 `check-superseded.sh`" in l), None)
    r = next((i for i, l in enumerate(lines) if s is not None and i > s and l.startswith("**결과:")), None)
    if s is None or r is None:
        return None, None, ""
    e = max(i for i in range(s, r) if lines[i].strip())
    return s, e, "\n".join(lines[s:e + 1])


def cx_runs():
    """가지 CX 의 check-superseded.sh 를 임시 폴더에 풀어 픽스처 둘(못 읽는 계약 · 새 판 / 모두 읽힘)에 돌린다."""
    d = Path(tmpdir("lastcx."))
    tar = subprocess.run(["git", "archive", CX, "harness"], capture_output=True)
    if tar.returncode:
        return None
    subprocess.run(["tar", "-x", "-C", str(d)], input=tar.stdout, check=True)
    fx = d / "fx"
    fx.mkdir()
    (fx / "sprint-contract-old.md").write_text("---\nstatus: superseded\nsuperseded_by: new\n---\n", encoding="utf-8")
    (fx / "sprint-contract-new.md").write_text("---\nstatus: active\n---\n", encoding="utf-8")
    (fx / "sprint-contract-other.md").write_text("---\nstatus: active\n---\n", encoding="utf-8")
    script = str(d / "harness/scripts/check-superseded.sh")
    os.chmod(fx / "sprint-contract-new.md", 0)
    os.chmod(fx / "sprint-contract-other.md", 0)
    r1 = subprocess.run(["bash", script, str(fx)], capture_output=True, text=True)
    os.chmod(fx / "sprint-contract-new.md", 0o644)
    os.chmod(fx / "sprint-contract-other.md", 0o644)
    r2 = subprocess.run(["bash", script, str(fx)], capture_output=True, text=True)
    return (r1.returncode, r1.stdout), (r2.returncode, r2.stdout)


def m_skill():
    """스킬-01: SKILL.md 안내가 가지 CX 의 새 출력 모양 — UNREADABLE 두 줄 모양 · unreadable= · 종료 코드 2 — 을 적는다.
    알려진 답: CX 스크립트를 픽스처에 돌린 출력의 줄 머리 낱말과 끝 줄 키가 모두 안내에 있다."""
    s, e, blk = skill_block(read(SKILL))
    runs = cx_runs()
    if runs is None or s is None:
        print(f"block={s},{e} cx={'none' if runs is None else 'ok'}")
        return 2
    (rc1, out1), (rc2, out2) = runs
    heads = {l.split()[0] for l in (out1 + out2).splitlines() if l.strip() and not l.startswith("checked=")}
    keys = set(re.findall(r"(\w+)=", last(out1)))
    lits = ["UNREADABLE <계약>", "UNREADABLE <계약> -> <새 판>", "unreadable=", "종료 코드 2", "못 읽",
            "MISSING_BY", "MISSING_TARGET", "CHAIN", "종료 코드 0"]
    miss = [x for x in lits if x not in blk] + [h for h in sorted(heads - {"OK"}) if h not in blk] \
        + [k + "=" for k in sorted(keys) if k + "=" not in blk]
    return report({"block": f"{s + 1}-{e + 1}", "cx_rc": f"{rc1},{rc2}", "cx_heads": ",".join(sorted(heads)),
                   "cx_keys": ",".join(sorted(keys)), "known_ok": rc1 == 2 and rc2 == 0 and heads == {"OK", "UNREADABLE"},
                   "miss": f"[{','.join(miss)}]", "ok": not miss})


def m_skill_scope():
    """스킬-02: SKILL.md 의 바뀐 줄이 모두 check-superseded 안내 안이다 (시작 판 · 새 판 양쪽 줄 번호로)."""
    rc, diff = git("diff", "-U0", f"{BASE}..HEAD", "--", SKILL)
    bs, be, _ = skill_block(fs2.show(BASE, SKILL) or "")
    ns, ne, _ = skill_block(read(SKILL))
    if None in (bs, be, ns, ne) or rc:
        return 2
    hunks, out = 0, 0
    for a, b, c, d in re.findall(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", diff, re.M):
        hunks += 1
        a, b, c, d = int(a), int(b or 1), int(c), int(d or 1)
        old_in = b == 0 or (bs + 1 <= a and a + b - 1 <= be + 1)
        new_in = d == 0 or (ns + 1 <= c and c + d - 1 <= ne + 1)
        if not (old_in and new_in):
            out += 1
            print(f"OUT -{a},{b} +{c},{d} block_old={bs + 1}-{be + 1} block_new={ns + 1}-{ne + 1}")
    return report({"hunks": hunks, "outside": out, "ok": hunks >= 1 and out == 0})


def schema_rows():
    md = next((l for l in read(SCHEMA_MD).splitlines() if l.startswith("| `superseded_by` |")), "")
    page = next((l for l in read(SCHEMA_PAGE).splitlines() if "<tr><td><code>superseded_by</code></td>" in l), "")
    return md, page


def m_schema():
    """구조-01: 규약 문서 superseded_by 행과 쪽의 같은 행이 UNREADABLE · 종료 코드 2 를 적고, 두 행의 인라인 코드가 같다."""
    md, page = schema_rows()
    page_codes = {re.sub(r"\s+", " ", fs2.visible(c)).strip() for c in re.findall(r"<code>(.*?)</code>", page)}
    md_codes = fs2.codes(md)
    page_text = fs2.visible(page)
    need = ["UNREADABLE", "종료 코드 2"]
    return report({"md_row": bool(md), "page_row": bool(page),
                   "md_need_ok": all(x in md for x in need), "page_need_ok": all(x in page_text for x in need),
                   "codes_only_md": f"[{','.join(sorted(md_codes - page_codes))}]",
                   "codes_only_page": f"[{','.join(sorted(page_codes - md_codes))}]",
                   "codes_same": md_codes == page_codes})


def m_overflow():
    """구조-02: 바뀐 docs 쪽 — 두 테마 · 320 · 375 · 1280 넘침 0."""
    rest.BASE = BASE
    return rest.m_overflow()


def m_ext():
    """구조-03: 바뀐 docs 파일이 레포 밖 자원을 부르지 않는다."""
    fs2.BASE = BASE
    return fs2.m_ext()


def m_commits():
    """구조-04: 커밋 규칙 — tail 도우미의 규칙을 이 계약의 시작 판 · 범위 목록으로."""
    tail.BASE, tail.CONTRACT = BASE, CONTRACT
    return tail.m_commits()


def m_notes():
    """구조-05: 기록 파일."""
    t = read(NOTES) if Path(NOTES).is_file() else ""
    keys = ["check-docs-mermaid", "aria-label", "flowchat", "머리말", "UNREADABLE", "check-superseded",
            "contract-schema", "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = set(re.findall(r"\b[0-9a-f]{8}\b", t))
    return report({"exists": bool(t), "miss": f"[{','.join(miss)}]", "keys_ok": bool(t) and not miss,
                   "hashes": len(hashes), "hashes_ok": len(hashes) >= 3})


CONDS = {
    "스킬-01": m_skill, "스킬-02": m_skill_scope,
    "스크립트-01": m_typo, "스크립트-02": m_front, "스크립트-03": m_repo, "스크립트-04": m_test,
    "오류-01": m_empty, "오류-02": m_tail_keep,
    "구조-01": m_schema, "구조-02": m_overflow, "구조-03": m_ext, "구조-04": m_commits, "구조-05": m_notes,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
