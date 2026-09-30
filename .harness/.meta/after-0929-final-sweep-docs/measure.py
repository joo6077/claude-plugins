"""계약 after-0929-final-sweep-docs 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

판은 BASE(시작 판 cacd9da3, 이 가지를 만든 `chore/after-kaizen-0928` 끝)와 작업 폴더 두 가지만 쓴다.
쪽 · 원본 파일은 작업 폴더에서 읽고, 시작 판 쪽은 `git archive` 로 임시 폴더에 풀어 브라우저로 연다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
"""
import fnmatch
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "cacd9da3"
DRIFT_SINCE = "e500a63"  # d1 이 쪽을 맞춘 기준 판 — 그 뒤에 다른 묶음이 바꾼 원본을 다시 본다
DRIFT = ["python3", "scripts/detect-docs-drift.py"]
BR = [".harness/.meta/after-0929-final-sweep-docs/br.js"]
NEW_PAGES = {
    "docs/design/research-log.md": "docs/design-kit/research-log.html",
    "react-kit/references/style-guide.md": "docs/react-kit/style-guide.html",
}
FENCE_LINE = re.compile(r"^\s*(`{3,}|~{3,})\s*\S*\s*$")
SIGN_RE = re.compile(r"^Claude .+ <noreply@anthropic\.com>$")


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def show(ref, path):
    rc, out = git("show", f"{ref}:{path}")
    return out if rc == 0 else None


def read(path):
    return Path(path).read_text(encoding="utf-8")


def visible(h, with_href=False):
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    extra = ""
    if with_href:
        extra = " " + " ".join(re.findall(r"""(?i)href\s*=\s*["']([^"']+)""", body))
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)) + extra)


def styles(h):
    """쪽 안 `<style>` 글 — HTML 주석과 CSS 주석을 뺀다. `prefers&#45;reduced-motion` 처럼 글자 참조로 적어
    글자 찾기를 비켜 가지 못하게 글자 참조를 풀어서 돌려준다 (시작 판 · 새 판 같은 처리라 선택자 비교에 영향 없음)."""
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    css = " ".join(re.findall(r"(?is)<style[^>]*>(.*?)</style>", h))
    return html.unescape(re.sub(r"/\*.*?\*/", "", css, flags=re.S))


def selectors(css):
    """`{` 앞의 선택자 · 규칙 머리를 빈칸 정리해 모은다."""
    return {re.sub(r"\s+", " ", s).strip() for s in re.findall(r"([^{};]+)\{", css) if s.strip()}


def site_links(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    return [m for m in re.findall(r"(?is)<link\b[^>]*>", h)
            if re.search(r"""href\s*=\s*["']?[^"'>\s]*assets/site\.css""", m)]


def codes(s):
    return {c.strip() for c in re.findall(r"`([^`\n]+)`", s) if c.strip()}


def words(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = "\n".join(l for l in s.splitlines()
                  if not FENCE_LINE.match(l) and not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", l))
    # 문장 끝 마침표 · 줄표는 낱말이 아니다 — 「없음.」 을 쪽이 「없음」 으로 실어도 같은 낱말로 본다
    found = (w.strip(".-") for w in re.findall(r"[0-9A-Za-z가-힣_.-]{2,}", re.sub(r"`[^`]*`", " ", s)))
    return {w for w in found if len(w) >= 2 and re.search(r"[0-9A-Za-z가-힣]", w)}


def base_pages():
    _, out = git("ls-tree", "-r", "--name-only", BASE, "--", "docs")
    return [p for p in out.split("\n") if p.endswith(".html")]


def head_pages():
    _, out = git("ls-files", "docs/*.html")
    return [p for p in out.split("\n") if p]


def dark_only():
    """시작 판에서 쪽 `<style>` 에 밝은 테마 규칙이 없던 쪽."""
    return [p for p in base_pages() if '[data-theme="light"]' not in styles(show(BASE, p) or "")]


def motion_pages():
    """시작 판에서 쪽 `<style>` 에 움직임 줄이기 규칙을 다시 적은 쪽."""
    return [p for p in base_pages() if "prefers-reduced-motion" in styles(show(BASE, p) or "")]


def registry():
    t = read("docs/index.html")
    return re.findall(r"\{\s*id:\s*'([^']+)'[^}]*file:\s*'([^']+)'", t), t


def node(*args):
    r = subprocess.run(["node", *BR, *args], capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines(), r.stderr


def base_tree():
    """시작 판 docs/ 를 임시 폴더에 푼다. 호출한 쪽이 지운다."""
    d = tempfile.mkdtemp(prefix="fs2base.", dir=os.environ.get("TMPDIR") or None)
    a = subprocess.Popen(["git", "archive", BASE, "docs"], stdout=subprocess.PIPE)
    t = subprocess.run(["tar", "-x", "-C", d], stdin=a.stdout)
    a.wait()
    if a.returncode or t.returncode:
        raise SystemExit(2)
    return d


def by_page(lines, prefix=""):
    out = {}
    for l in lines:
        f, rest = l.split(" ", 1)
        out[f[len(prefix):] if prefix and f.startswith(prefix) else f] = dict(kv.split("=", 1) for kv in rest.split())
    return out


# ── 조건별 측정 ──

def m_lists():
    d, m = dark_only(), motion_pages()
    print(f"base={BASE} pages={len(base_pages())} dark_only={len(d)} motion_in_style={len(m)}")
    return 0


def m_theme():
    """구조-01: 어두운 테마만 있던 쪽 + 새 쪽 — 브라우저 색 설정 따르기 · 단추 · 저장 · 다시 열기."""
    pages = dark_only() + list(NEW_PAGES.values())
    have = [p for p in pages if Path(p).is_file()]
    rc, lines, err = node("theme", *have)
    got = by_page(lines)
    bad = 0
    for p in pages:
        r = got.get(p)
        wh = [int(x) for x in r["btn"].split("x")] if r and "x" in r["btn"] else [0, 0]
        ok = bool(r) and r["first_light"] == "light" and r["first_dark"] == "dark" and r["click"] == "light" \
            and r["stored"] == "light" and r["reload"] == "light" and r["bg_differs"] == "1" and min(wh) >= 44
        bad += not ok
        if not ok:
            print(f"BAD {p} {r}")
    print(f"theme_ok={len(pages) - bad}/{len(pages)} br_rc={rc}")
    return 0 if bad == 0 and rc == 0 else 1


def m_page_css():
    """구조-02: 어두운 테마만 있던 쪽의 `<style>` 에 새 선택자 0 · 테마 · 색 설정 규칙 0 · style 속성 늘지 않음,
    밝은 테마 규칙은 공통 파일에 있다."""
    bad = 0
    pages = dark_only()
    for p in pages:
        b, h = show(BASE, p) or "", read(p) if Path(p).is_file() else ""
        new_sel = selectors(styles(h)) - selectors(styles(b))
        banned = [k for k in ("data-theme", "prefers-color-scheme", "theme-btn", "themeToggle") if k in styles(h)]
        attrs = (len(re.findall(r"\sstyle\s*=", h)), len(re.findall(r"\sstyle\s*=", b)))
        ok = bool(h) and not new_sel and not banned and attrs[0] <= attrs[1]
        bad += not ok
        if not ok:
            print(f"BAD {p} new_selectors={sorted(new_sel)[:4]} banned={banned} style_attrs={attrs[1]}->{attrs[0]}")
    site = re.sub(r"/\*.*?\*/", "", read("docs/assets/site.css"), flags=re.S)
    light = site.count('[data-theme="light"]')
    print(f"pages={len(pages)} bad={bad} site_css_light_rules={light}")
    return 0 if bad == 0 and light >= 1 else 1


def paint(theme, pages, root=""):
    rc, lines, err = node("paint", theme, *[os.path.join(root, p) if root else p for p in pages])
    return rc, by_page(lines, prefix=os.path.join(root, "") if root else "")


def m_keep_colors():
    """구조-03: 시작 판 202 쪽의 어두운 테마 색 지문, 밝은 테마가 있던 84 쪽의 밝은 테마 색 지문이 그대로다."""
    pages = base_pages()
    light_pages = [p for p in pages if p not in set(dark_only())]
    d = base_tree()
    try:
        rc1, b_dark = paint("dark", pages, d)
        rc2, b_light = paint("light", light_pages, d)
    finally:
        subprocess.run(["rm", "-rf", d])
    rc3, h_dark = paint("dark", pages)
    rc4, h_light = paint("light", light_pages)
    bad = 0
    for p in pages:
        if b_dark.get(p, {}).get("fp") != h_dark.get(p, {}).get("fp"):
            bad += 1
            print(f"BAD dark {p} {b_dark.get(p, {}).get('fp')} -> {h_dark.get(p, {}).get('fp')}")
    for p in light_pages:
        if b_light.get(p, {}).get("fp") != h_light.get(p, {}).get("fp"):
            bad += 1
            print(f"BAD light {p} {b_light.get(p, {}).get('fp')} -> {h_light.get(p, {}).get('fp')}")
    print(f"dark_pages={len(pages)} light_pages={len(light_pages)} changed={bad} br_rc={rc1},{rc2},{rc3},{rc4}")
    return 0 if bad == 0 and rc1 == rc2 == rc3 == rc4 == 0 else 1


def m_overflow():
    """구조-04: 추적 쪽 전부를 두 테마 · 320 · 375 · 1280 에서 — 가로 넘침 0."""
    pages = head_pages()
    bad = 0
    rcs = []
    for theme in ("dark", "light"):
        rc, got = paint(theme, pages)
        rcs.append(rc)
        for p in pages:
            of = got.get(p, {}).get("of")
            if of != "0/0/0":
                bad += 1
                print(f"BAD {theme} {p} of={of}")
    print(f"pages={len(pages)} themes=2 bad={bad} br_rc={','.join(map(str, rcs))}")
    return 0 if bad == 0 and not any(rcs) and pages else 1


def m_a11y():
    """구조-05: 접근성 검사기를 docs 전체에 — 모든 줄 OK · theme=both · 끝 줄 N/N PASS."""
    r = subprocess.run(["node", "scripts/check-docs-a11y.js"], capture_output=True, text=True)
    rows = [l for l in r.stdout.splitlines() if re.match(r"^(OK  |FAIL) ", l)]
    fail = sum(1 for l in rows if l.startswith("FAIL"))
    both = sum(1 for l in rows if l.endswith("theme=both"))
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    n = len(head_pages())
    print(f"rows={len(rows)} fail={fail} theme_both={both} tracked={n} tail=[{tail}] rc={r.returncode}")
    for l in rows:
        if l.startswith("FAIL") or not l.endswith("theme=both"):
            print("  " + l)
    return 0 if r.returncode == 0 and fail == 0 and both == len(rows) == n and tail == f"{n}/{n} PASS" else 1


def m_motion_css():
    """구조-06: 추적 쪽 `<style>` 에 움직임 줄이기 규칙 0 쪽, 공통 파일에는 줄이기 규칙이 있다."""
    pages = head_pages()
    left = [p for p in pages if "prefers-reduced-motion" in styles(read(p))]
    site = re.sub(r"/\*.*?\*/", "", read("docs/assets/site.css"), flags=re.S)
    has = len(re.findall(r"@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)", site))
    for p in left:
        print(f"LEFT {p}")
    print(f"pages={len(pages)} style_motion_pages={len(left)} base_motion_pages={len(motion_pages())} site_reduce_blocks={has}")
    return 0 if not left and has >= 1 and pages else 1


def motion(mode, pages, root=""):
    rc, lines, err = node("motion", mode, *[os.path.join(root, p) if root else p for p in pages])
    return rc, by_page(lines, prefix=os.path.join(root, "") if root else "")


def m_reduce():
    """오류-01: 움직임 줄이기 설정에서 추적 쪽 전부 — 0.02ms 넘게 움직이는 애니메이션 0 · 전환 0.01ms 이하 · 애니메이션 0.01ms 이하 ·
    scroll-behavior auto · 가리킬 때 들뜨는 요소 0."""
    pages = head_pages()
    rc, got = motion("reduce", pages)
    bad = 0
    for p in pages:
        r = got.get(p)
        ok = bool(r) and r["moving"] == "0" and float(r["transition_ms"]) <= 0.01 \
            and float(r["animation_ms"]) <= 0.01 and r["scroll"] == "auto" and r["hover_lifts"] == "0"
        bad += not ok
        if not ok:
            print(f"BAD {p} {r}")
    print(f"pages={len(pages)} bad={bad} br_rc={rc}")
    return 0 if bad == 0 and rc == 0 and pages else 1


def m_allow():
    """오류-02: 움직임을 허용한 설정에서 시작 판 202 쪽의 가리킬 때 들뜨는 요소 수 · 끝없이 도는 애니메이션 수 · 가장 긴 전환이 그대로다."""
    pages = base_pages()
    d = base_tree()
    try:
        rc1, b = motion("no-preference", pages, d)
    finally:
        subprocess.run(["rm", "-rf", d])
    rc2, h = motion("no-preference", pages)
    bad = 0
    lifts = 0
    for p in pages:
        keys = ("hover_lifts", "endless", "transition_ms")
        bv, hv = [b.get(p, {}).get(k) for k in keys], [h.get(p, {}).get(k) for k in keys]
        lifts += int(bv[0] or 0)
        if bv != hv or None in bv:
            bad += 1
            print(f"BAD {p} base={bv} head={hv}")
    print(f"pages={len(pages)} changed={bad} base_hover_lifts={lifts} br_rc={rc1},{rc2}")
    return 0 if bad == 0 and rc1 == rc2 == 0 else 1


def m_drift_map():
    """스크립트-02: 디자인 연구 기록이 드리프트 연결표에 있다."""
    want = "docs/design/research-log.md → docs/design-kit/research-log.html"
    r = subprocess.run([*DRIFT, "--since", "6378948", "--include-format-only"], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.startswith("docs/design/")]
    t = subprocess.run([*DRIFT, "--check-table"], capture_output=True, text=True)
    last = t.stdout.strip().splitlines()[-1] if t.stdout.strip() else ""
    print(f"lines={lines} drift_rc={r.returncode} check_table_rc={t.returncode} check_table_tail=[{last}]")
    return 0 if lines == [want] and r.returncode == 0 and t.returncode == 0 and "어긋남 0" in last else 1


def cov(src, page):
    s = read(src)
    t = visible(read(page))
    cs = sorted(codes(s))
    cin = sum(1 for c in cs if re.sub(r"\s+", " ", c) in t)
    ws = {w for w in re.findall(r"[0-9A-Za-z가-힣_.-]{2,}", re.sub(r"`[^`]*`", " ", s))}
    wr = sum(1 for w in ws if w in t) / max(1, len(ws))
    squash = re.sub(r"\s+", "", t)
    fl, fence = set(), False
    for line in s.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
            continue
        if fence:
            q = re.sub(r"\s+", "", line)
            if len(q) >= 8:
                fl.add(q)
    fin = sum(1 for q in fl if q in squash)
    return wr, cin, len(cs), fin, len(fl)


def m_new_pages():
    """구조-07: 새 쪽 둘 — 400 줄 이상 · 목차 항목 하나 · id 하나뿐 · 아이콘 · 공통 CSS 링크 하나 · 원본 담김."""
    reg, index = registry()
    ids = [i for i, _ in reg]
    bad = 0
    for src, page in NEW_PAGES.items():
        if not Path(page).is_file():
            print(f"{page} MISSING")
            bad += 1
            continue
        h = read(page)
        n = h.count("\n")
        rel = page[len("docs/"):]
        reg_ids = [i for i, f in reg if f == rel]
        icon = bool(reg_ids) and f"'{reg_ids[0]}':" in index.split("function getIcon", 1)[-1]
        uniq = len(reg_ids) == 1 and ids.count(reg_ids[0]) == 1
        wr, cin, cn, fin, fn = cov(src, page)
        ok = (n >= 400 and uniq and icon and len(site_links(h)) == 1 and wr >= 0.95
              and cin == cn and fin == fn)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {page} lines={n} reg={len(reg_ids)} id_unique={int(uniq)} icon={int(icon)} "
              f"site_css={len(site_links(h))} wr={wr:.2f} code={cin}/{cn} fence={fin}/{fn}")
    print(f"new_pages_ok={len(NEW_PAGES) - bad}/{len(NEW_PAGES)}")
    return 0 if bad == 0 else 1


def m_drift_follow():
    """구조-08: DRIFT_SINCE 뒤 원본 내용이 바뀐 짝(모양만 바뀐 원본은 도구가 뺀다)의 쪽이 원본이 새로 얻은
    인라인 코드 · 낱말을 모두 싣는다."""
    r = subprocess.run([*DRIFT, "--since", DRIFT_SINCE], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if " → " in l]
    bad = 0
    for l in lines:
        s, rest = l.split(" → ", 1)
        page = rest.split()[0]
        a, b = show(DRIFT_SINCE, s) or "", read(s) if Path(s).is_file() else ""
        nc, nw = codes(b) - codes(a), words(b) - words(a)
        if not Path(page).is_file():
            print(f"NOPAGE\t{s}\t{page}")
            bad += 1
            continue
        t = visible(read(page), with_href=True)
        mc = [c for c in nc if re.sub(r"\s+", " ", c) not in t]
        mw = [w for w in nw if w not in t]
        st = "OK" if not mc and not mw and "[NEW" not in rest else "GAP"
        bad += st != "OK"
        print(f"{st}\t{s}\t{page}\tcode_miss={len(mc)}/{len(nc)}\tword_miss={len(mw)}/{len(nw)}\t{sorted(mc)[:4]}{sorted(mw)[:6]}")
    print(f"pairs={len(lines)} bad={bad} drift_rc={r.returncode}")
    return 0 if bad == 0 and r.returncode == 0 and lines else 1


def m_ext():
    """구조-10: 바뀌거나 새로 생긴 docs 파일이 레포 밖 자원을 부르지 않는다."""
    rc, out = git("diff", "--name-only", f"{BASE}..HEAD", "--", "docs")
    files = [p for p in out.split() if p.endswith((".html", ".css", ".js")) and Path(p).is_file()]
    pat = re.compile(r"""(?is)(?:<(?:script|img|iframe)\b[^>]*\bsrc|<link\b[^>]*\bhref)\s*=\s*["']?\s*(?:https?:)?//|@import\s*(?:url\()?\s*["']?\s*(?:https?:)?//|url\(\s*["']?\s*(?:https?:)?//""")
    bad = 0
    for p in files:
        n = len(pat.findall(read(p)))
        if n:
            print(f"EXT {p} {n}")
            bad += 1
    print(f"checked={len(files)} ext_files={bad} git_rc={rc}")
    return 0 if bad == 0 and rc == 0 and files else 1


CONTRACT = ".harness/sprint-contract-after-0929-final-sweep-docs.md"


def scope_block():
    t = read(CONTRACT)
    sec = re.search(r"^## 범위 경계.*?(?=^## |\Z)", t, re.M | re.S)
    blk = re.search(r"```text\n# sprint-scope\n(.*?)```", sec.group(0) if sec else "", re.S)
    return [l.strip() for l in (blk.group(1) if blk else "").splitlines() if l.strip()]


def in_scope(path, scope):
    for s in scope:
        if s.endswith("/") and path.startswith(s):
            return True
        if path == s or (("*" in s or "?" in s) and fnmatch.fnmatchcase(path, s)):
            return True
    return path.startswith(".harness/")


def m_commits():
    """구조-11: BASE..HEAD 커밋마다 합침 커밋 아님 · 맨 위 폴더 하나(docs 는 docs/<폴더> 하나, docs/index.html 은 곁들여도 됨) ·
    .harness/ 와 구현 파일을 한 커밋에 싣지 않음 · 서명 줄 · 바뀐 파일이 범위 목록 안."""
    scope = scope_block()
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
            if parts[0] == "docs" and f != "docs/index.html" and len(parts) > 2:
                tops.add("docs/" + parts[1])
            elif f != "docs/index.html":
                tops.add(parts[0])
        if not tops and fs:
            tops.add("docs")
        signed = any(SIGN_RE.match(t.strip()) for t in trailers.splitlines())
        out = [f for f in fs if not in_scope(f, scope)]
        merge = len(parents.split()) > 2
        ok = len(tops) == 1 and signed and not out and not merge
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {c[:8]} tops={sorted(tops)} signed={int(signed)} out_of_scope={out[:5]} merge={int(merge)}")
    n = len(revs.split())
    print(f"commits={n} bad={bad} scope_entries={len(scope)} git_rc={rc}")
    return 0 if bad == 0 and n and scope and rc == 0 else 1


def m_skill():
    """스킬-01: docs-site 스킬 글이 이번 규칙을 적는다 — 줄 머리로 찾은 네 줄을 잰다."""
    lines = read(".claude/skills/docs-site/SKILL.md").splitlines()
    pick = lambda head: next((l for l in lines if l.startswith(head)), "")
    g1, g13 = pick("1. **외부 리소스 금지**"), pick("13. **테마 토글을 넣으면 영속화까지**")
    motion, row = pick("- **Motion**:"), pick("| design-kit |")
    checks = {
        "g1_checker": "check-docs-common-css.py" in g1 and "prefers-reduced-motion" in g1,
        # 없어야 할 낱말은 글자 참조(`no&#45;preference`)로 적어도 잡는다
        "g1_no_preference_gone": bool(g1) and "no-preference" not in html.unescape(g1),
        "g13_site_css": "docs/assets/site.css" in g13,
        "motion_transform": "transform" in motion and "docs/assets/site.css" in motion,
        "table_design_log": "`docs/design/`" in row,
    }
    print(" ".join(f"{k}={int(v)}" for k, v in checks.items()))
    return 0 if all(checks.values()) else 1


CONDS = {
    "LISTS": m_lists, "구조-01": m_theme, "구조-02": m_page_css, "구조-03": m_keep_colors, "구조-04": m_overflow,
    "구조-05": m_a11y, "구조-06": m_motion_css, "오류-01": m_reduce, "오류-02": m_allow, "스크립트-02": m_drift_map,
    "구조-07": m_new_pages, "스킬-01": m_skill, "구조-08": m_drift_follow, "구조-10": m_ext, "구조-11": m_commits,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
