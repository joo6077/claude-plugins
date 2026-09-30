"""계약 after-0930-end 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

CI 단계 읽기 · 커밋 규칙은 앞 묶음 tail(after-0929-tail) 도우미를 불러 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
임시 폴더는 TMPDIR 아래 만든다. 레포 파일에는 쓰지 않는다.
"""
import html
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "f0fcc534"  # 시작 판 — last · cx 가 합쳐진 chore/after-kaizen-0928 끝
PRE_SKIP = "8dca3e73^"  # 지운 파일도 UNREADABLE 로 치던 install 검사 판 (지운 파일 SKIP 정책 앞)
HERE = ".harness/.meta/after-0930-end"
CONTRACT = ".harness/sprint-contract-after-0930-end.md"
NOTES = ".harness/.meta/after-kaizen-0928/end-notes.md"
TAIL = ".harness/.meta/after-0929-tail/measure.py"
CX_REPRO = ".harness/.meta/after-0929-codex-silent-pass/repro.sh"
INSTALL, INSTALL_TEST = "scripts/check-install-docs-guidance.py", "scripts/test-check-install-docs-guidance.py"
MM_CHECK, MM_TEST = "scripts/check-docs-mermaid.js", "scripts/test-check-docs-mermaid.js"
RUN_EVALS, RUN_TEST = "scripts/run-evals.py", "scripts/test-run-evals.py"
SYNC_EVALS, SYNC_TEST = "scripts/sync-evals.py", "scripts/test-sync-evals.py"
UTILS = "scripts/plugin_utils.py"
RAW = "https://raw.githubusercontent.com/joo6077/claude-plugins/main/"
GUIDED = f"참고: docs/foo/x.md\n설치본 플러그인에는 `docs/foo/` 가 없다 — {RAW} 뒤에 붙여 읽는다.\n"
GOOD_EVALS = ('{"evals":[{"id":1,"skill":"s","prompt":"p","expected_output":"e",'
              '"assertions":[{"text":"a","type":"output"}]}]}\n')
# 머리말 건너뛰기를 되돌린 옛 모양 — firstLine 이 첫 줄만 본다
MM_FRONT_SKIP = ("        const closing = lines[0] === '---' ? lines.indexOf('---', 1) : -1;\n"
                 "        return lines[closing + 1] || '';\n")
MM_OLD = "        return lines[0] || '';\n"
# 머리 읽개 사본 — (이름, 파일, 모양). fm = fm_get <파일> <키>, read_fm = read_fm <키> <파일>, val = awk 함수
FM_COPIES = [
    ("qa-evaluator", "harness/agents/qa-evaluator.md", "fm"),
    ("contract-schema.md", "harness/references/contract-schema.md", "fm"),
    ("contract-schema.html", "docs/harness/contract-schema.html", "fm"),
    ("sprint-contract", "harness/skills/sprint-contract/SKILL.md", "read_fm"),
    ("commit-guard", "harness/scripts/commit-guard.sh", "val"),
]
FM_TEXT = "---\nstatus: active   # 메모\nowner_session: abc\t# 탭 주석\nslug: \"x-y\"  # q\nsuperseded_by: a#b\n---\n"
FM_KEYS = ["status", "owner_session", "slug", "superseded_by"]
FM_WANT = "active|abc|x-y|a#b"
FM_STRIP = "        else if (match(v, /[ \\t]#/)) v = substr(v, 1, RSTART - 1)\n"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tail = load("tail", TAIL)
fs2 = tail.fs2
read, git, run, last, report = fs2.read, fs2.git, tail.run, tail.last, tail.report
GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="t",
               GIT_AUTHOR_EMAIL="t@example.com", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")


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
    d = tmpdir("endperm.")
    p = d / "x"
    p.write_text("x", encoding="utf-8")
    p.chmod(0)
    ok = not os.access(p, os.R_OK)
    p.chmod(0o644)
    shutil.rmtree(d, ignore_errors=True)
    return ok


def fails_of(out):
    return ",".join(sorted(re.findall(r"^FAIL 경우 (\d+)", out, re.M), key=int))


# ---- (1) install 검사: 깨진 바로가기 ----
def install_repo(root, tool, shape):
    """킷 k · 뿌리 docs/foo 칸을 가진 임시 git 저장소에 경우 하나를 만든다."""
    sh = lambda *a: subprocess.run(["git", *a], cwd=root, check=True, capture_output=True, env=GIT_ENV)
    (root / "scripts").mkdir(parents=True)
    shutil.copy(tool, root / "scripts/check-install-docs-guidance.py")
    (root / "k/.claude-plugin").mkdir(parents=True)
    (root / "k/.claude-plugin/plugin.json").write_text('{"name":"k"}\n', encoding="utf-8")
    (root / "docs/foo").mkdir(parents=True)
    (root / "docs/foo/x.md").write_text("x\n", encoding="utf-8")
    (root / "k/a.md").write_text(GUIDED, encoding="utf-8")
    if shape in ("broken-link", "link-deleted"):
        os.symlink("missing.md", root / "k/link.md")
    elif shape == "live-link":
        os.symlink("a.md", root / "k/link.md")
    elif shape == "deleted":
        (root / "k/gone.md").write_text("참고: docs/foo/x.md\n", encoding="utf-8")
    sh("init", "-q")
    sh("add", "-A")
    sh("commit", "-qm", "base")
    if shape == "link-deleted":
        (root / "k/link.md").unlink()
    elif shape == "deleted":
        (root / "k/gone.md").unlink()


# (경우, 기대 종료 코드, 출력에 있어야 할 줄 머리)
INSTALL_CASES = [
    ("broken-link", 2, "UNREADABLE k/link.md"),
    ("deleted", 0, "SKIP k/gone.md"),
    ("link-deleted", 0, "SKIP k/link.md"),
    ("live-link", 0, "TOTAL files=2 ok=2"),
]


def m_install():
    """스크립트-01: 대상 없는 바로가기는 UNREADABLE · 2, 진짜 지운 파일 · 지운 바로가기는 SKIP · 0, 대상 있는 바로가기는 0."""
    if not os.path.lexists(INSTALL):
        return 2
    d = tmpdir("endinst.")
    right = 0
    for shape, want_rc, want in INSTALL_CASES:
        root = d / shape
        install_repo(root, Path(INSTALL).resolve(), shape)
        rc, out = run("python3", "scripts/check-install-docs-guidance.py", cwd=root)
        ok = rc == want_rc and any(l.startswith(want) for l in out.splitlines())
        right += ok
        print(f"{'OK ' if ok else 'BAD'} {shape} rc={rc} want={want_rc} tail=[{last(out)}]")
    shutil.rmtree(d, ignore_errors=True)
    return report({"cases": len(INSTALL_CASES), "right": right, "ok": right == len(INSTALL_CASES)})


def m_install_test():
    """스크립트-02: install 시험 네 경우 · 시작 판 도구는 경우 4 만 실패 · 지운 파일을 UNREADABLE 로 치던 도구는 경우 3 만 실패."""
    rc_t, out_t = run("python3", INSTALL_TEST)
    d = tmpdir("endinstt.")
    base = show(BASE, INSTALL, d / "base.py")
    pre = show(PRE_SKIP, INSTALL, d / "pre.py")
    rc_b, out_b = run("python3", INSTALL_TEST, "--tool", str(base))
    rc_p, out_p = run("python3", INSTALL_TEST, "--tool", str(pre))
    shutil.rmtree(d, ignore_errors=True)
    return report({"test_rc": rc_t, "test_tail": f"[{last(out_t)}]", "test_ok": rc_t == 0 and last(out_t) == "경우 4 개 중 통과 4",
                   "base_rc": rc_b, "base_fails": fails_of(out_b), "base_ok": rc_b == 1 and fails_of(out_b) == "4",
                   "pre_rc": rc_p, "pre_fails": fails_of(out_p), "pre_ok": rc_p == 1 and fails_of(out_p) == "3"})


# ---- (2) Mermaid 시험: 이름표 없는 머리말 예시 ----
def mm_copy(text, d):
    """검사 사본을 d/scripts/ 에 두고 d/node_modules 가 레포 node_modules 를 가리키게 한다 — 사본이 Mermaid 를 찾게."""
    (d / "scripts").mkdir(parents=True)
    os.symlink(Path("node_modules").resolve(), d / "node_modules")
    p = d / "scripts/check-docs-mermaid.js"
    p.write_text(text, encoding="utf-8")
    return p


def m_mm_test():
    """스크립트-03: 시험 아홉 경우 · 머리말 건너뛰기를 되돌린 사본은 경우 9 만 실패 · 늘 0 인 가짜 검사도 잡힘 · 머리 설명 · CI 이름."""
    src = read(MM_CHECK)
    if src.count(MM_FRONT_SKIP) != 1:
        print(f"NOT_APPLIED front-skip hits={src.count(MM_FRONT_SKIP)}")
        return 2
    rc_t, out_t = run("node", MM_TEST)
    d = tmpdir("endmm.")
    old = mm_copy(src.replace(MM_FRONT_SKIP, MM_OLD), d / "old")
    rc_o, out_o = run("node", MM_TEST, "--check", str(old))
    stub = d / "stub-check.js"
    stub.write_text("console.log('쪽 0 · 예시 0 · 안 그려진 예시 0');\nprocess.exit(0);\n", encoding="utf-8")
    rc_s, _ = run("node", MM_TEST, "--check", str(stub))
    shutil.rmtree(d, ignore_errors=True)
    runs = tail.ci_runs().get("playwright", [])
    idx = {r.strip(): i for i, r in enumerate(runs)}
    npm = idx.get("npm ci", -1)
    ci_ok = runs.count(f"node {MM_TEST}") == 1 and idx.get(f"node {MM_TEST}", -1) > npm >= 0 \
        and "아홉 경우" in tail.ci_name(f"node {MM_TEST}")
    m = re.search(r"/\*\*(.*?)\*/", read(MM_TEST), re.S)
    head = m.group(1) if m else ""
    head_ok = "아홉 경우" in head and "  9. " in head
    return report({"test_rc": rc_t, "test_tail": f"[{last(out_t)}]", "test_ok": rc_t == 0 and last(out_t) == "경우 9 개 중 통과 9",
                   "old_rc": rc_o, "old_fails": fails_of(out_o), "old_ok": rc_o == 1 and fails_of(out_o) == "9",
                   "stub_rc": rc_s, "stub_ok": rc_s == 1, "head_ok": head_ok, "ci_ok": ci_ok})


# ---- (3) run-evals · sync-evals ----
def m_named():
    """스크립트-04: 이름으로 준 킷이 없거나(no-such-kit) 평가 파일이 없으면(planning-kit) 2 와 그 이름, 정상 킷 이름(backend-kit)은 0."""
    cases = [("no-such-kit", 2), ("planning-kit", 2), ("backend-kit", 0)]
    right = 0
    for kit, want in cases:
        rc, out = run("python3", RUN_EVALS, kit)
        ok = rc == want and (want == 0 or kit in out)
        right += ok
        print(f"{'OK ' if ok else 'BAD'} {kit} rc={rc} want={want} tail=[{last(out)}]")
    return report({"cases": len(cases), "right": right, "ok": right == len(cases)})


def evals_tree(root, tool_dir):
    (root / "scripts").mkdir(parents=True)
    for name in ("run-evals.py", "sync-evals.py", "plugin_utils.py"):
        shutil.copy(Path(tool_dir) / name, root / "scripts" / name)
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin/marketplace.json").write_text('{"plugins":[{"name":"k","source":"./k"}]}\n', encoding="utf-8")
    (root / "k/skills/s").mkdir(parents=True)
    (root / "k/skills/s/SKILL.md").write_text("---\nname: s\ndescription: d\nuser-invocable: true\n---\n\n본문\n",
                                              encoding="utf-8")
    (root / "k/evals").mkdir()
    p = root / "k/evals/evals.json"
    p.write_text(GOOD_EVALS, encoding="utf-8")
    return p


def m_unreadable():
    """스크립트-05: 못 읽는 evals.json — run-evals · sync-evals --check-only 모두 UNREADABLE 줄(경로 포함)과 2. 읽히면 둘 다 0."""
    if not rootless():
        print("ROOT 권한을 빼도 읽힌다")
        return 2
    d = tmpdir("endeval.")
    root = d / "t"
    p = evals_tree(root, Path("scripts").resolve())
    got = {}
    for name, cmd in (("run", ["python3", "scripts/run-evals.py"]), ("sync", ["python3", "scripts/sync-evals.py", "--check-only"])):
        rc_g, _ = run(*cmd, cwd=root)
        p.chmod(0)
        try:
            rc, out = run(*cmd, cwd=root)
        finally:
            p.chmod(0o644)
        line = any(l.startswith("UNREADABLE") and "k/evals/evals.json" in l for l in out.splitlines())
        got[name] = (rc, line, rc_g)
        print(f"{name} unreadable rc={rc} line={int(line)} good rc={rc_g} tail=[{last(out)}]")
    shutil.rmtree(d, ignore_errors=True)
    return report({"run_ok": got["run"] == (2, True, 0), "sync_ok": got["sync"] == (2, True, 0)})


def m_eval_tests():
    """스크립트-06: run-evals 시험 여섯 경우 · sync-evals 시험 세 경우, 시작 판 도구로는 새 경우만 실패, CI 이름."""
    rc_r, out_r = run("python3", RUN_TEST)
    rc_s, out_s = run("python3", SYNC_TEST)
    d = tmpdir("endevt.")
    for f in (RUN_EVALS, SYNC_EVALS, UTILS):
        show(BASE, f, d / Path(f).name)
    rc_rb, out_rb = run("python3", RUN_TEST, "--tool", str(d / "run-evals.py"))
    rc_sb, out_sb = run("python3", SYNC_TEST, "--tool", str(d / "sync-evals.py"))
    shutil.rmtree(d, ignore_errors=True)
    run_name, sync_name = tail.ci_name(f"python3 {RUN_TEST}"), tail.ci_name(f"python3 {SYNC_TEST}")
    return report({"run_tail": f"[{last(out_r)}]", "run_ok": rc_r == 0 and last(out_r) == "경우 6 개 중 통과 6",
                   "sync_tail": f"[{last(out_s)}]", "sync_ok": rc_s == 0 and last(out_s) == "경우 3 개 중 통과 3",
                   "run_base_fails": fails_of(out_rb), "run_base_ok": rc_rb == 1 and fails_of(out_rb) == "4,5,6",
                   "sync_base_fails": fails_of(out_sb), "sync_base_ok": rc_sb == 1 and fails_of(out_sb) == "3",
                   "ci_ok": "없는 킷" in run_name and "못 읽" in run_name and "못 읽" in sync_name})


def m_usage():
    """구조-02: 도구 설명 글이 새 종료 코드 까닭을 적는다."""
    heads = {INSTALL: tail.doc_head(INSTALL), RUN_EVALS: read(RUN_EVALS).split('"""')[1], SYNC_EVALS: read(SYNC_EVALS).split('"""')[1]}
    need = {INSTALL: ["바로가기"], RUN_EVALS: ["없는 킷", "평가 파일", "못 읽"], SYNC_EVALS: ["못 읽"]}
    miss = [f"{Path(f).name}:{w}" for f, ws in need.items() for w in ws if w not in heads[f]]
    return report({"miss": f"[{','.join(miss)}]", "ok": not miss})


# ---- (4) 머리 읽개 사본 ----
def fm_copy_script(path, shape, text):
    """사본 한 벌을 셸 조각으로 꺼낸다. 돌려주는 조각은 `$F` 파일에서 FM_KEYS 를 읽어 | 로 잇는다."""
    if path.endswith(".html"):
        text = html.unescape(re.sub(r"<[^>]+>", "", text))
    if shape == "val":
        m = re.search(r"^[ \t]*function val\(.*?^[ \t]*\}\n", text, re.S | re.M)
        if not m:
            return None
        prog = m.group(0) + 'BEGIN { SQ = sprintf("%c", 39) }\n$0 ~ "^" k ":" { print val($0); exit }\n'
        body = "\n".join(f"v{i}=$(awk -v k={k} '{prog}' \"$F\")" for i, k in enumerate(FM_KEYS))
        return body + "\nprintf '%s|%s|%s|%s\\n' \"$v0\" \"$v1\" \"$v2\" \"$v3\"\n"
    name = "fm_get" if shape == "fm" else "read_fm"
    m = re.search(rf"^{name}\(\) *\{{.*?^\}}\n", text, re.S | re.M)
    if not m:
        return None
    call = (lambda k: f"fm_get \"$F\" {k}") if shape == "fm" else (lambda k: f"read_fm {k} \"$F\"")
    return m.group(0) + "printf '%s|%s|%s|%s\\n' " + " ".join(f"\"$({call(k)})\"" for k in FM_KEYS) + "\n"


def fm_run(script, f):
    r = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=dict(os.environ, F=str(f)))
    return r.returncode, r.stdout.strip()


def m_fm_copies():
    """오류-01: 머리 읽개 사본 다섯이 줄 끝 주석을 벗긴다. 주석 벗기기 줄을 지운 qa-evaluator 사본은 틀린 값을 낸다."""
    d = tmpdir("endfm.")
    f = d / "fm.md"
    f.write_text(FM_TEXT, encoding="utf-8")
    right = 0
    for name, path, shape in FM_COPIES:
        script = fm_copy_script(path, shape, read(path))
        rc, got = fm_run(script, f) if script else (None, "")
        ok = got == FM_WANT
        right += ok
        print(f"{'OK ' if ok else 'BAD'} {name} rc={rc} got=[{got}]")
    qa = read(FM_COPIES[0][1])
    hits = qa.count(FM_STRIP)
    _, mut = fm_run(fm_copy_script(FM_COPIES[0][1], "fm", qa.replace(FM_STRIP, "")), f) if hits == 1 else (None, "")
    print(f"mutant qa-evaluator strip_hits={hits} got=[{mut}]")
    _, grep_out = git("grep", "-lE", r'index\(\$\(?0\)?, k ":"\) == 1', "--", ".", ":(exclude).harness")
    files = sorted(grep_out.split())
    shutil.rmtree(d, ignore_errors=True)
    want_files = sorted(p for _, p, s in FM_COPIES if s != "val")
    return report({"copies": len(FM_COPIES), "right": right, "ok": right == len(FM_COPIES),
                   "mut_ok": hits == 1 and mut != FM_WANT, "grep_files": len(files), "grep_ok": files == want_files})


# ---- 앞 묶음 측정 · 소비처 ----
CX_KEEP = ["d2 broken-json rc=2 msg=1", "d2 good rc=0", "d4 unreadable rc=2 msg=1", "d4 good rc=0",
           "d6 empty-list rc=2 msg=1", "d6 no-key rc=2 msg=1", "d6 good rc=0"]


def m_cx_keep():
    """오류-02: 앞 묶음 cx 재현의 결함 2 · 4 · 6 줄 일곱이 그대로다."""
    rc, out = run("bash", CX_REPRO, os.getcwd(), str(Path.home() / ".claude/hooks"))
    got = [l.strip() for l in out.splitlines() if re.match(r"^d[246] ", l)]
    for l in got:
        print(l)
    return report({"lines": len(got), "same": got == CX_KEEP})


def m_consumers():
    """오류-03: 킷 이름을 주고 run-evals 를 부르는 소비처 셋(tone-kit · backend-kit · infra-kit)과 인자 없는 CI 실행이 모두 0."""
    right = 0
    for kit in ("tone-kit", "backend-kit", "infra-kit", None):
        rc, out = run("python3", RUN_EVALS, *([kit] if kit else []))
        right += rc == 0
        print(f"{'OK ' if rc == 0 else 'BAD'} {kit or '(인자 없음)'} rc={rc} tail=[{last(out)}]")
    return report({"cases": 4, "right": right, "ok": right == 4})


def m_commits():
    """구조-01: 커밋 규칙 — tail 도우미의 규칙을 이 계약의 시작 판 · 범위 목록으로."""
    tail.BASE, tail.CONTRACT = BASE, CONTRACT
    return tail.m_commits()


def m_notes():
    """구조-03: 기록 파일."""
    t = read(NOTES) if Path(NOTES).is_file() else ""
    keys = ["check-install-docs-guidance", "lexists", "test-check-docs-mermaid", "머리말", "run-evals", "sync-evals",
            "OSError", "fm_get", "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = set(re.findall(r"\b[0-9a-f]{8}\b", t))
    return report({"exists": bool(t), "miss": f"[{','.join(miss)}]", "keys_ok": bool(t) and not miss,
                   "hashes": len(hashes), "hashes_ok": len(hashes) >= 3})


CONDS = {
    "스크립트-01": m_install, "스크립트-02": m_install_test, "스크립트-03": m_mm_test,
    "스크립트-04": m_named, "스크립트-05": m_unreadable, "스크립트-06": m_eval_tests,
    "오류-01": m_fm_copies, "오류-02": m_cx_keep, "오류-03": m_consumers,
    "구조-01": m_commits, "구조-02": m_usage, "구조-03": m_notes,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
