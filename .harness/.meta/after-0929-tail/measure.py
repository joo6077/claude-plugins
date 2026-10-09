"""계약 after-0929-tail 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

쪽 글을 읽는 함수 · 넘침 · 밖 자원 측정은 앞 묶음 rest(after-0929-leftovers) · fs2(after-0929-final-sweep-docs) 도우미를 불러 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "c6cfcd09"  # 시작 판 — rest 가 합쳐진 chore/after-kaizen-0928 끝
HERE = ".harness/.meta/after-0929-tail"
CONTRACT = ".harness/sprint-contract-after-0929-tail.md"
NOTES = ".harness/.meta/after-kaizen-0928/tail-notes.md"
REST = ".harness/.meta/after-0929-leftovers/measure.py"
FS2 = ".harness/.meta/after-0929-final-sweep-docs/measure.py"
API_CHECK, API_TEST = "scripts/check-api-kit-docs.py", "scripts/test-check-api-kit-docs.py"
CSS_CHECK, CSS_TEST = "scripts/check-docs-common-css.py", "scripts/test-check-docs-common-css.py"
SHARED = "scripts/plugin_utils.py"
MM_CHECK, MM_TEST = "scripts/check-docs-mermaid.js", "scripts/test-check-docs-mermaid.js"
MM_LIB = os.environ.get("MM_LIB", "node_modules/mermaid/dist/mermaid.min.js")
MM_PAGES = ["docs/planning-kit/data-modeling.html", "docs/planning-kit/flows.html", "docs/planning-kit/reference.html"]
FLOWS_MD, FLOWS_PAGE = "docs/planning/flows.md", "docs/planning-kit/flows.html"
FLOW_KEEP = ["12.0.0", "2026-09-10", "비시험판", "2026-09-28", "registry.npmjs.org/mermaid/latest",
             "releases/tag/mermaid%4012.0.0"]
EXIT_TABLE = "harness/evals/gate-exit-codes.md"
# 시작 판에서 움직임 허용 설정일 때 본문 배경에 0 초 넘는 전환이 걸린 쪽 (body.js list 로 잰 47 쪽)
BODY_PAGES = [f"docs/{p}.html" for p in (
    "api-kit/api-inventory-normalization", "api-kit/artifact-interop-import-export", "api-kit/auth-secret-lifecycle",
    "api-kit/baseline-governance-promotion", "api-kit/contract-extraction-modes", "api-kit/environment-safety-gates",
    "api-kit/error-status-contracts", "api-kit/multi-sample-pagination-variance", "api-kit/probe-synthesis-hurl-semantics",
    "api-kit/regression-diff-failure-policy", "api-kit/research-log", "api-kit/snapshot-sealing-canonicalization",
    "api-kit/static-evidence-viewer-contract", "backend-kit/research-log", "design-kit/color-palette",
    "design-kit/design-template", "design-kit/visual-styles", "harness/feedback-system", "howto-kit/overview",
    "infra-kit/research-log", "process/phase-research-templates", "react-kit/animation", "react-kit/build-audit",
    "react-kit/integration", "react-kit/performance", "react-kit/project-detection", "react-kit/quality",
    "react-kit/research-log", "react-kit/scaffolding", "react-kit/state-data", "react-kit/ui-patterns",
    "reflect-kit/reflect-digest", "rust-kit/project-detection", "tone-kit/adapter-contract",
    "tone-kit/adapter-dart-flutter", "tone-kit/ai-code-stylometry", "tone-kit/antipattern-catalog",
    "tone-kit/campaign-methodology", "tone-kit/comment-economy", "tone-kit/dart-flutter-idioms",
    "tone-kit/extraction-thresholds", "tone-kit/korean-technical-writing", "tone-kit/locale-korean",
    "tone-kit/naming-taxonomy", "tone-kit/overview", "tone-kit/sources", "tone-kit/templates")]
# 연결 판정 열두 경우 — (이름, <head> 안 글, 공통 CSS 연결로 쳐야 하는가)
LINK_CASES = [
    ("stylesheet", '<link rel="stylesheet" href="../assets/site.css">', 1),
    ("quote-mix", "<link href='../assets/site.css' rel=stylesheet>", 1),
    ("preload", '<link rel="preload" as="style" href="../assets/site.css">', 0),
    ("bak", '<link rel="stylesheet" href="../assets/site.css.bak">', 0),
    ("comment", '<!-- <link rel="stylesheet" href="../assets/site.css"> -->', 0),
    ("data-rel", '<link data-rel="stylesheet" rel="preload" href="../assets/site.css">', 0),
    ("data-href", '<link rel="stylesheet" data-href="../assets/site.css" href="x.css">', 0),
    ("alternate", '<link rel="alternate stylesheet" href="../assets/site.css">', 0),
    ("print", '<link rel="stylesheet" media="print" href="../assets/site.css">', 0),
    ("query", '<link rel="stylesheet" href="../assets/site.css?v=2">', 1),
    ("media-all", '<link rel="stylesheet" media="all" href="../assets/site.css">', 1),
    ("media-screen", '<link rel="stylesheet" media="screen" href="../assets/site.css">', 1),
]
SIGN_RE = re.compile(r"^Claude .+ <noreply@anthropic\.com>$")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rest = load("rest", REST)
fs2 = rest.fs2
read, git, visible, words, codes = fs2.read, fs2.git, fs2.visible, fs2.words, fs2.codes


def report(checks):
    print(" ".join(f"{k}={int(v) if isinstance(v, bool) else v}" for k, v in checks.items()))
    return 0 if all(v is True for v in checks.values() if isinstance(v, bool)) else 1


def run(*cmd, cwd=None):
    r = subprocess.run(list(cmd), capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr


def last(out):
    lines = [l for l in out.splitlines() if l.strip()]
    return lines[-1].strip() if lines else ""


def tmpdir(prefix):
    return tempfile.mkdtemp(prefix=prefix, dir=os.environ.get("TMPDIR") or None)


def base_copy(path):
    """시작 판 파일을 임시 폴더에 꺼낸다."""
    d = tmpdir("tailbase.")
    rc, out = git("show", f"{BASE}:{path}")
    if rc:
        raise SystemExit(2)
    p = Path(d) / Path(path).name
    p.write_text(out, encoding="utf-8")
    return p


def ci_runs():
    import yaml
    jobs = yaml.safe_load(read(".github/workflows/ci.yml"))["jobs"]
    return {name: [s.get("run", "") for s in job.get("steps", [])] for name, job in jobs.items()}


def ci_name(run_line):
    """그 run 줄을 가진 CI 단계의 이름. 없으면 빈 글."""
    import yaml
    for job in yaml.safe_load(read(".github/workflows/ci.yml"))["jobs"].values():
        for s in job.get("steps", []):
            if s.get("run", "").strip() == run_line:
                return s.get("name", "")
    return ""


def doc_head(path):
    """시험 파일 맨 앞 설명(첫 docstring 또는 첫 주석 덩어리)."""
    t = read(path) if Path(path).is_file() else ""
    m = re.match(r'#![^\n]*\n"""(.*?)"""', t, re.S)
    return m.group(1) if m else ""


# ── 연결 판정 열두 경우를 한 폴더(레포 또는 사본)의 두 검사에 댄다 ──

MATRIX_CHILD = r'''
import importlib.util, json, subprocess, sys, tempfile
from pathlib import Path
root, cases = Path(sys.argv[1]), json.loads(sys.argv[2])
sys.path.insert(0, str(root / "scripts"))
spec = importlib.util.spec_from_file_location("api", root / "scripts/check-api-kit-docs.py")
api = importlib.util.module_from_spec(spec); spec.loader.exec_module(api)
out = []
with tempfile.TemporaryDirectory() as t:
    t = Path(t); api.REPO = t
    for i, (name, head, want) in enumerate(cases):
        md, html = t / f"docs/api/c{i}.md", t / f"docs/api-kit/c{i}.html"
        md.parent.mkdir(parents=True, exist_ok=True); html.parent.mkdir(parents=True, exist_ok=True)
        md.write_text("# 제목\n\n본문\n", encoding="utf-8")
        filler = "\n".join("<p>본문</p>" for _ in range(460))
        html.write_text(f"<!DOCTYPE html>\n<html><head>{head}<style>:root{{--accent:{api.ACCENT}}}</style></head>\n<body>\n{filler}\n<script>localStorage.getItem('dk-theme')</script></body></html>\n", encoding="utf-8")
        a = int(not any("공통 CSS" in f for f in api.check(md, html)["fail"]))
        page = t / f"common/c{i}.html"; page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(f"<!DOCTYPE html>\n<html><head>{head}</head><body><p>본문</p></body></html>\n", encoding="utf-8")
        r = subprocess.run([sys.executable, str(root / "scripts/check-docs-common-css.py"), str(page)], capture_output=True, text=True)
        if r.returncode == 0:
            c = 1
        elif r.returncode == 1 and "site_css_links=0" in r.stdout:
            c = 0
        else:
            c = "err"
        out.append([name, want, a, c])
print(json.dumps(out))
'''


def matrix(root):
    r = subprocess.run([sys.executable, "-c", MATRIX_CHILD, str(root), json.dumps(LINK_CASES)], capture_output=True, text=True)
    if r.returncode:
        print(r.stderr.strip()[-400:])
        return None
    return json.loads(r.stdout)


# ── 조건별 측정 ──

def m_api_test():
    """스크립트-01: api-kit 문서 검사 시험 열 경우 · 검사 통과 · CI 등록 · 시작 판 사본은 다섯 경우 실패."""
    rc_t, out_t = run("python3", API_TEST)
    rc_c, out_c = run("python3", API_CHECK)
    src = read(API_TEST) if Path(API_TEST).is_file() else ""
    tags = ['data-rel="stylesheet"', 'data-href="../assets/site.css"', 'rel="alternate stylesheet"',
            'media="print"', "site.css?v=2"]
    miss = [t for t in tags if t not in src]
    rc_o, out_o = run("python3", API_TEST, "--check", str(base_copy(API_CHECK)))
    fails = sum(1 for l in out_o.splitlines() if l.startswith("FAIL"))
    ci = sum(1 for r in ci_runs().get("validate", []) if r.strip() == f"python3 {API_TEST}")
    words_ok = "열 경우" in ci_name(f"python3 {API_TEST}") and "열 경우" in doc_head(API_TEST)
    return report({"count_words_ok": words_ok, "test_rc": rc_t, "test_tail": f"[{last(out_t)}]", "test_ok": rc_t == 0 and last(out_t) == "경우 10 개 중 통과 10",
                   "check_ok": rc_c == 0 and last(out_c) == "12/12 PASS", "tag_miss": miss, "tags_ok": not miss,
                   "base_rc": rc_o, "base_fails": fails, "base_ok": rc_o == 1 and fails == 5, "ci": ci, "ci_ok": ci == 1})


def m_css_test():
    """스크립트-02: 공통 CSS 검사 시험 여덟 경우 · 추적 쪽 전부 통과 · 시작 판 사본은 경우 8 실패."""
    rc_t, out_t = run("python3", CSS_TEST)
    rc_c, out_c = run("python3", CSS_CHECK)
    rc_o, out_o = run("python3", CSS_TEST, "--check", str(base_copy(CSS_CHECK)))
    fail8 = [l for l in out_o.splitlines() if l.startswith("FAIL 경우 8")]
    others = [l for l in out_o.splitlines() if l.startswith("FAIL") and not l.startswith("FAIL 경우 8")]
    src = read(CSS_TEST)
    tags = ['data-rel="stylesheet"', 'data-href="../assets/site.css"', 'rel="alternate stylesheet"',
            "site.css?v=2"]
    miss = [t for t in tags if t not in src]
    ci = sum(1 for r in ci_runs().get("validate", []) if r.strip() == f"python3 {CSS_TEST}")
    words_ok = "여덟 경우" in ci_name(f"python3 {CSS_TEST}") and "여덟 경우" in doc_head(CSS_TEST)
    return report({"count_words_ok": words_ok, "test_rc": rc_t, "test_tail": f"[{last(out_t)}]", "test_ok": rc_t == 0 and last(out_t) == "경우 8 개 중 통과 8",
                   "check_tail": f"[{last(out_c)}]", "check_ok": rc_c == 0 and last(out_c) == "검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0",
                   "tag_miss": miss, "tags_ok": not miss,
                   "base_rc": rc_o, "base_ok": rc_o == 1 and len(fail8) == 1 and not others, "ci_ok": ci == 1})


def m_matrix():
    """스크립트-03: 연결 판정 열두 경우에서 두 검사의 판정이 기대와 같고 서로 같다."""
    got = matrix(Path.cwd())
    if got is None:
        return 2
    right = agree = 0
    for name, want, a, c in got:
        right += a == want and c == want
        agree += a == c
        if not (a == want and c == want):
            print(f"BAD {name} want={want} api={a} common={c}")
    return report({"cases": len(got), "right": right, "agree": agree, "all_ok": right == agree == len(LINK_CASES)})


def m_mm_check():
    """스크립트-04: Mermaid 검사가 레포 쪽 예시를 모두 그리고, 깨진 사본은 잡는다. 따로 짠 그리기와 수가 같다."""
    rc, out = run("node", MM_CHECK)
    named = [p for p in MM_PAGES if p not in out]
    rc_r, out_r = run("node", f"{HERE}/mmrender.js", MM_LIB, *fs2.head_pages())
    d = Path(tmpdir("tailmm."))
    broken = d / "docs/planning-kit/flows-broken.html"
    broken.parent.mkdir(parents=True)
    (d / "docs/assets").mkdir(parents=True)
    shutil.copy("docs/assets/site.css", d / "docs/assets/site.css")
    old = '  A["Visitor lands on pricing"] <span class="rel">--&gt;</span> B{"Starts trial?"}'
    h = read(FLOWS_PAGE)
    applied = h.count(old) == 1
    broken.write_text(h.replace(old, '  A["Visitor lands on pricing" <span class="rel">--&gt;</span> B{"Starts trial?"', 1), encoding="utf-8")
    rc_b, out_b = run("node", str(Path(MM_CHECK).resolve()), str(broken))
    return report({"rc": rc, "tail": f"[{last(out)}]", "ok": rc == 0 and last(out) == "쪽 3 · 예시 9 · 안 그려진 예시 0",
                   "pages_named_ok": not named, "ref": f"[{last(out_r)}]", "ref_ok": rc_r == 0 and last(out_r) == "pages=3 examples=9 bad=0",
                   "broken_applied": applied, "broken_rc": rc_b, "broken_ok": applied and rc_b == 1 and "flows-broken.html" in out_b})


def m_mm_test():
    """스크립트-05: Mermaid 검사 시험 네 경우 · CI 등록 · 늘 0 을 내는 가짜 검사는 시험이 잡는다."""
    rc_t, out_t = run("node", MM_TEST)
    d = Path(tmpdir("tailstub."))
    stub = d / "stub-check.js"
    stub.write_text("console.log('쪽 0 · 예시 0 · 안 그려진 예시 0');\nprocess.exit(0);\n", encoding="utf-8")
    rc_s, out_s = run("node", MM_TEST, "--check", str(stub))
    runs = ci_runs().get("playwright", [])
    idx = {r.strip(): i for i, r in enumerate(runs)}
    npm = idx.get("npm ci", -1)
    ci_ok = runs.count(f"node {MM_CHECK}") == 1 and runs.count(f"node {MM_TEST}") == 1 \
        and idx.get(f"node {MM_CHECK}", -1) > npm >= 0 and idx.get(f"node {MM_TEST}", -1) > npm
    ci_ok = ci_ok and "네 경우" in ci_name(f"node {MM_TEST}")
    return report({"test_rc": rc_t, "test_tail": f"[{last(out_t)}]", "test_ok": rc_t == 0 and last(out_t) == "경우 4 개 중 통과 4",
                   "stub_rc": rc_s, "stub_ok": rc_s == 1, "ci_ok": ci_ok})


def m_reduce():
    """오류-01: 움직임 줄이기 설정에서 47 쪽 모두 누른 직후 본문 배경이 끝 값 — 세 번 잰다. 대상 집합도 그대로다."""
    rc_l, out_l = run("node", f"{HERE}/body.js", "list", *fs2.head_pages())
    listed = sorted(l.split()[0] for l in out_l.splitlines() if "body_transition=" in l)
    same = listed == sorted(BODY_PAGES)
    bad, rcs = set(), []
    for _ in range(3):
        rc, out = run("node", f"{HERE}/body.js", "click", "reduce", *BODY_PAGES)
        rcs.append(rc)
        got = {l.split()[0]: l for l in out.splitlines() if l.startswith("docs/")}
        for p in BODY_PAGES:
            l = got.get(p, "")
            if not ("changed=1" in l and "settled=1" in l):
                bad.add(p)
    for p in sorted(bad):
        print(f"BAD {p}")
    return report({"listed": len(listed), "same_set": same, "pages": len(BODY_PAGES), "bad": len(bad),
                   "rcs": ",".join(map(str, rcs)), "ok": same and not bad and not any(rcs) and rc_l == 0})


def m_allow():
    """오류-02: 움직임 허용 설정에서 47 쪽은 그대로 전환한다 — 누른 뒤 본문 배경 값이 셋 이상 거친다."""
    rc, out = run("node", f"{HERE}/body.js", "click", "no-preference", *BODY_PAGES)
    got = {l.split()[0]: l for l in out.splitlines() if l.startswith("docs/")}
    bad = 0
    for p in BODY_PAGES:
        m = re.search(r"changed=1 settled=\d distinct=(\d+)", got.get(p, ""))
        if not (m and int(m.group(1)) >= 3):
            bad += 1
            print(f"BAD {p} {got.get(p)}")
    return report({"pages": len(BODY_PAGES), "moving": len(BODY_PAGES) - bad, "rc": rc, "ok": bad == 0 and rc == 0})


def m_prior():
    """오류-03: 앞 묶음 측정 다섯 — fs2 오류-01 · 오류-02 · 구조-06, rest 오류-01 · 오류-02."""
    runs = [(FS2, "오류-01"), (FS2, "오류-02"), (FS2, "구조-06"), (REST, "오류-01"), (REST, "오류-02")]
    bad = 0
    for path, cond in runs:
        rc, out = run("python3", path, cond)
        bad += rc != 0
        print(f"{'OK ' if rc == 0 else 'BAD'} {path} {cond} rc={rc} [{last(out)}]")
    return report({"runs": len(runs), "bad": bad, "ok": bad == 0})


def string_mutate(src):
    """글자 값(문자열 토큰) 안의 `stylesheet` 만 `nostylesheetx` 로 바꾼다 — 함수 이름 같은 식별자는 두고 판정 값만 망가뜨린다."""
    import io
    import tokenize
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    lines = src.splitlines(keepends=True)
    n = 0
    for tok in reversed(toks):
        if tok.type == tokenize.STRING and "stylesheet" in tok.string:
            (sr, sc), (er, ec) = tok.start, tok.end
            if sr != er:
                continue
            line = lines[sr - 1]
            lines[sr - 1] = line[:sc] + tok.string.replace("stylesheet", "nostylesheetx") + line[ec:]
            n += 1
    return n, "".join(lines)


def m_shared():
    """구조-01: 연결 판정이 공용 모듈 한 곳에 있다 — 두 검사가 그 모듈을 불러오고,
    사본에서 공용 모듈의 `stylesheet` 낱말만 바꾸면 두 검사 모두 연결로 치는 경우가 0 이 된다."""
    imports = {p: bool(re.search(r"^\s*(from plugin_utils import|import plugin_utils)", read(p), re.M)) for p in (API_CHECK, CSS_CHECK)}
    d = Path(tmpdir("tailclone."))
    rc, _ = run("git", "clone", "-q", "--shared", ".", str(d / "r"))
    if rc:
        return 2
    root = d / "r"
    for p in (API_CHECK, CSS_CHECK, SHARED):  # 커밋 전 판도 잴 수 있게 작업 폴더 파일을 얹는다
        shutil.copy(p, root / p)
    n, mutated = string_mutate((root / SHARED).read_text(encoding="utf-8"))
    (root / SHARED).write_text(mutated, encoding="utf-8")
    got = matrix(root)
    if got is None:
        return 2
    pos = [g for g in got if g[1] == 1]
    api_pos = sum(1 for g in pos if g[2] == 1)
    css_pos = sum(1 for g in pos if g[3] == 1)
    return report({"imports": ",".join(f"{Path(k).name}:{int(v)}" for k, v in imports.items()), "imports_ok": all(imports.values()),
                   "replaced": n, "api_pos_after": api_pos, "common_pos_after": css_pos,
                   "ok": n >= 1 and api_pos == 0 and css_pos == 0})


def m_pin():
    """구조-02: Mermaid 를 12.0.0 으로 못박았다 — package.json · package-lock.json · 설치본."""
    pkg = json.loads(read("package.json"))
    lock = json.loads(read("package-lock.json"))
    dev = pkg.get("devDependencies", {})
    lk = lock.get("packages", {})
    inst = Path("node_modules/mermaid/package.json")
    iv = json.loads(inst.read_text())["version"] if inst.is_file() else None
    return report({"pkg": dev.get("mermaid"), "pw": dev.get("@playwright/test"), "lock": lk.get("node_modules/mermaid", {}).get("version"),
                   "lock_root": lk.get("", {}).get("devDependencies", {}).get("mermaid"), "installed": iv,
                   "ok": dev.get("mermaid") == "12.0.0" and dev.get("@playwright/test") == "^1.58.2"
                   and lk.get("node_modules/mermaid", {}).get("version") == "12.0.0"
                   and lk.get("", {}).get("devDependencies", {}).get("mermaid") == "12.0.0" and iv == "12.0.0"})


def m_exit_table():
    """구조-03: 종료 코드 표 소비처에 Mermaid 검사 줄이 하나, 쓰는 값 0 · 1 · 2 · 3."""
    rows = [l for l in read(EXIT_TABLE).splitlines() if l.startswith(f"| `{MM_CHECK}` |")]
    ok = len(rows) == 1 and rows[0].replace(" ", "") == f"|`{MM_CHECK}`|0·1·2·3|"
    return report({"rows": len(rows), "row": f"[{rows[0] if rows else ''}]", "ok": ok})


def m_flows():
    """구조-04: flows 원본 · 쪽이 「렌더해 확인하지 않았다」 를 버리고 검사 이름을 적는다. 나머지 여섯 낱말 · 날짜는 그대로다."""
    md = read(FLOWS_MD)
    lines = [l for l in md.splitlines() if l.startswith("아래 예시는 Mermaid 공식 flowchart 문법을 따른다")]
    line = lines[0] if len(lines) == 1 else ""
    h = read(FLOWS_PAGE)
    shown = visible(h, with_href=True)
    keep_md = [k for k in FLOW_KEEP if k not in line]
    keep_page = [k for k in FLOW_KEEP if k not in shown]
    olds = ["렌더해 확인하지 않았다", "렌더해 봤나", "해 보지 않았다"]
    old_md = sum(md.count(o) for o in olds)
    old_page = sum(shown.count(o) for o in olds)
    new_words = [w for w in words(line) if w not in shown]
    new_codes = [c for c in codes(line) if c not in shown]
    fm, meta, foot = rest.meta_dates(FLOWS_MD, FLOWS_PAGE)
    want = rest.last_date(FLOWS_MD)
    return report({"md_lines": len(lines), "keep_md": keep_md, "keep_page": keep_page,
                   "keep_ok": len(lines) == 1 and not keep_md and not keep_page,
                   "old_md": old_md, "old_page": old_page, "old_ok": old_md == 0 and old_page == 0,
                   "name_ok": "check-docs-mermaid.js" in line and "check-docs-mermaid.js" in shown,
                   "line_in_page_ok": not new_words and not new_codes, "miss": (new_words + new_codes)[:6],
                   "dates": f"{fm}/{','.join(meta)}/{','.join(foot)}/{want}",
                   "dates_ok": fm == want and meta == [want] and foot == [want]})


def m_notes():
    """구조-05: 기록 파일."""
    if not Path(NOTES).is_file():
        print(f"{NOTES} 없음")
        return 1
    t = read(NOTES)
    keys = ["check-api-kit-docs", "check-docs-common-css", "plugin_utils", "data-rel", "site.css?v=2", "prefers-reduced-motion",
            "check-docs-mermaid", "12.0.0", "flows.md", "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = len(set(re.findall(r"\b[0-9a-f]{8}\b", t)))
    return report({"keys_ok": not miss, "miss": miss, "hashes": hashes, "hashes_ok": hashes >= 5})


def m_overflow():
    """구조-06: 바뀐 docs 쪽 — 두 테마 · 320 · 375 · 1280 넘침 0."""
    rest.BASE = BASE
    return rest.m_overflow()


def m_ext():
    """구조-07: 바뀐 docs 파일이 레포 밖 자원을 부르지 않는다."""
    fs2.BASE = BASE
    return fs2.m_ext()


def m_commits():
    """구조-08: 커밋 규칙. 레포 맨 위 폴더 바로 아래 파일(package.json · package-lock.json)은 한 묶음 「(root)」 로 센다."""
    fs2.CONTRACT = CONTRACT
    scope = fs2.scope_block()
    rc, revs = git("rev-list", "--reverse", f"{BASE}..HEAD")
    bad = 0
    for c in revs.split():
        _, parents = git("rev-list", "--parents", "-n", "1", c)
        _, files = git("show", "--name-only", "--format=", c)
        _, trailers = git("log", "-1", "--format=%(trailers:key=Co-Authored-By,valueonly)", c)
        fs = [f for f in files.split("\n") if f]
        tops = set()
        for f in fs:
            parts = f.split("/")
            if len(parts) == 1:
                tops.add("(root)")
            elif parts[0] == "docs" and f != "docs/index.html" and len(parts) > 2:
                tops.add("docs/" + parts[1])
            elif f != "docs/index.html":
                tops.add(parts[0])
        signed = any(SIGN_RE.match(t.strip()) for t in trailers.splitlines())
        out = [f for f in fs if not fs2.in_scope(f, scope)]
        merge = len(parents.split()) > 2
        ok = len(tops) == 1 and signed and not out and not merge
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {c[:8]} tops={sorted(tops)} signed={int(signed)} out_of_scope={out[:5]} merge={int(merge)}")
    n = len(revs.split())
    print(f"commits={n} bad={bad} scope_entries={len(scope)} git_rc={rc}")
    return 0 if bad == 0 and n and scope and rc == 0 else 1


CONDS = {
    "스크립트-01": m_api_test, "스크립트-02": m_css_test, "스크립트-03": m_matrix, "스크립트-04": m_mm_check,
    "스크립트-05": m_mm_test, "오류-01": m_reduce, "오류-02": m_allow, "오류-03": m_prior,
    "구조-01": m_shared, "구조-02": m_pin, "구조-03": m_exit_table, "구조-04": m_flows, "구조-05": m_notes,
    "구조-06": m_overflow, "구조-07": m_ext, "구조-08": m_commits,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
