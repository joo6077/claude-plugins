"""계약 after-0928-docs-site 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

git 판은 BASE(시작 판 e500a63) 와 작업 폴더의 HEAD 두 가지만 쓴다. 쪽 · 원본 파일은 작업 폴더에서 읽는다.
모든 명령은 끝에 `rc=<종료 코드>` 를 찍지 않는다 — 종료 코드는 셸의 $? 로 본다 (0 = 조건 성립, 1 = 불성립, 2 = 잴 수 없음).
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "e500a63"
SINCE = "6378948"
DRIFT = ["python3", "scripts/detect-docs-drift.py"]
KEEP_FLAG = "--include-format-only"

NEW_PAGES = {
    "bambu-kit/skills/bambu-print-profile/references/comment-analysis.md": "docs/bambu-kit/comment-analysis.html",
    "bambu-kit/skills/bambu-print-profile/references/tolerance.md": "docs/bambu-kit/tolerance.html",
    "bambu-kit/skills/bambu-print-profile/references/user-preferences.md": "docs/bambu-kit/user-preferences.html",
    "flutter-toolkit/references/figma-parity-self-verify.md": "docs/flutter-toolkit/figma-parity-self-verify.html",
    "harness/references/cross-kit-principles.md": "docs/harness/cross-kit-principles.html",
    "react-kit/references/clean-arch-layout.md": "docs/react-kit/clean-arch-layout.html",
    "react-kit/references/common-gotchas.md": "docs/react-kit/common-gotchas.html",
    "react-kit/references/result-patterns.md": "docs/react-kit/result-patterns.html",
    "reflect-kit/skills/reflect-promote/SKILL.md": "docs/reflect-kit/reflect-promote.html",
    "docs/flutter/research-log.md": "docs/flutter-toolkit/research-log.html",
    "docs/planning/research-log.md": "docs/planning-kit/research-log.html",
    "docs/rust/research-log.md": "docs/rust-kit/research-log.html",
    "docs/tone/research-log.md": "docs/tone-kit/research-log.html",
}
PAIRS = {
    "tone-kit/references/core-antipatterns.md": "docs/tone-kit/antipattern-catalog.html",
    "tone-kit/references/core-comment.md": "docs/tone-kit/comment-economy.html",
    "tone-kit/references/core-naming.md": "docs/tone-kit/naming-taxonomy.html",
    "tone-kit/references/core-structure.md": "docs/tone-kit/extraction-thresholds.html",
    "reflect-kit/skills/codex-kaizen/references/search-sources.md": "docs/reflect-kit/codex-kaizen.html",
}
NO_PAGE = ["tone-kit/references/project-detection.md"]
D5_EXTRA = {
    "docs/api/research-log.md": "docs/api-kit/research-log.html",
    "docs/backend/research-log.md": "docs/backend-kit/research-log.html",
    "docs/infra/research-log.md": "docs/infra-kit/research-log.html",
    "docs/react/research-log.md": "docs/react-kit/research-log.html",
    "tone-kit/references/adapter-contract.md": "docs/tone-kit/adapter-contract.html",
    "tone-kit/references/adapter-dart-flutter.md": "docs/tone-kit/adapter-dart-flutter.html",
    "tone-kit/references/locale-korean.md": "docs/tone-kit/locale-korean.html",
    "tone-kit/references/sources.md": "docs/tone-kit/sources.html",
}
A3_PAGES = [
    "docs/design-kit/visual-change-protocol.html",
    "docs/design-kit/design-test.html",
    "docs/flutter-toolkit/visual-evidence-protocol.html",
    "docs/infra-kit/cicd.html",
    "docs/infra-kit/infra-test.html",
    "docs/onboarding-kit/format-checklist.html",
    "docs/react-kit/render-evidence-protocol.html",
]
B16_PAGES = [
    "react-kit/integration", "react-kit/scaffolding", "react-kit/state-data", "react-kit/performance",
    "react-kit/quality", "react-kit/ui-patterns", "react-kit/animation", "react-kit/build-audit",
    "howto-kit/overview", "harness/feedback-system",
]
B16_HEADINGS = {
    "react-kit/integration": ["Bad vs Good — 통합 설계 실수 패턴", "21 스킬 교차 공통 주의사항"],
    "react-kit/scaffolding": ["Bad vs Good — G1 핵심 실수 패턴", "Scaffolding 핵심 Gotchas"],
    "react-kit/performance": ["Bad vs Good — G3 핵심 실수 패턴"],
    "react-kit/ui-patterns": ["Bad vs Good — G5 핵심 실수 패턴", "G5 스킬 공통 주의사항"],
    "react-kit/build-audit": ["감사 실패를 유발하는 패턴 vs 올바른 패턴", "빌드·감사 스킬 공통 주의사항"],
}
B16_OLD = "38cccd1"
B17_PAGES = ["docs/process/kaizen-flow.html", "docs/react-kit/animation.html", "docs/react-kit/build-audit.html"]
CHARREF = re.compile(r"&#(?:x0*2[ed]|0*4[56]);", re.I)
FENCE_LINE = re.compile(r"^\s*(`{3,}|~{3,})\s*\S*\s*$")


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
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    return " ".join(re.findall(r"(?is)<style[^>]*>(.*?)</style>", h))


def site_links(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    return [m for m in re.findall(r"(?is)<link\b[^>]*>", h)
            if re.search(r"""href\s*=\s*["']?[^"'>\s]*assets/site\.css""", m)]


def word_seq(t):
    """모양만 바뀐 것을 가르는 기준 — HTML 주석 · 울타리 줄을 뺀 낱말 순서."""
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    out = []
    for line in t.splitlines():
        if FENCE_LINE.match(line):
            out.append("FENCE")
            continue
        out.extend(re.findall(r"\w+", line))
    return out


def codes(s):
    return {c.strip() for c in re.findall(r"`([^`\n]+)`", s) if c.strip()}


def words(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = "\n".join(l for l in s.splitlines()
                  if not FENCE_LINE.match(l) and not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", l))
    return {w for w in re.findall(r"[0-9A-Za-z가-힣_.-]{2,}", re.sub(r"`[^`]*`", " ", s))
            if re.search(r"[0-9A-Za-z가-힣]", w)}


def drift_lines(*extra):
    r = subprocess.run([*DRIFT, "--since", SINCE, *extra], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if " → " in l]
    return r.returncode, lines, r.stderr


def pairs_of(lines):
    out = []
    for l in lines:
        src, rest = l.split(" → ", 1)
        out.append((src, rest.split()[0], "[NEW" in rest))
    return out


def registry():
    t = read("docs/index.html")
    return re.findall(r"\{\s*id:\s*'([^']+)'[^}]*file:\s*'([^']+)'", t), t


# ── 조건별 측정 ──

def m_sc01():
    rc, lines, _ = drift_lines(KEEP_FLAG)
    got = {s: t for s, t, _ in pairs_of(lines)}
    ok = 0
    for s, page in PAIRS.items():
        hit = got.get(s) == page
        ok += hit
        print(f"{s} → {got.get(s, '-')} {'OK' if hit else 'MISS'}")
    print(f"pairs_ok={ok}/{len(PAIRS)} drift_rc={rc}")
    return 0 if ok == len(PAIRS) and rc == 0 else 1


def m_sc02():
    rc, lines, _ = drift_lines(KEEP_FLAG)
    ps = pairs_of(lines)
    new = sum(1 for *_, n in ps if n)
    nop = sum(1 for s, *_ in ps if s in NO_PAGE)
    print(f"new_marks={new} no_page_lines={nop} lines={len(lines)} drift_rc={rc}")
    return 0 if new == 0 and nop == 0 and rc == 0 and lines else 1


def classify(src):
    a, b = show(SINCE, src), show("HEAD", src)
    if a is None or b is None:
        return "REAL"
    return "SHAPE" if word_seq(a) == word_seq(b) else "REAL"


def m_sc03():
    rc_all, all_lines, _ = drift_lines(KEEP_FLAG)
    rc_def, def_lines, err = drift_lines()
    expect = {l for l in all_lines if classify(l.split(" → ")[0]) == "REAL"}
    got = set(def_lines)
    print(f"all={len(all_lines)} default={len(def_lines)} expect_real={len(expect)} "
          f"only_tool={len(got - expect)} only_ref={len(expect - got)} rc={rc_all},{rc_def}")
    print(f"stderr: {err.strip()}")
    return 0 if got == expect and rc_all == 0 and rc_def == 0 and all_lines else 1


def m_ar04():
    rc, lines, _ = drift_lines()
    bad = 0
    for s, page, _ in pairs_of(lines):
        a, b = show(SINCE, s) or "", show("HEAD", s) or ""
        nc, nw = codes(b) - codes(a), words(b) - words(a)
        if not Path(page).is_file():
            print(f"NOPAGE\t{s}\t{page}")
            bad += 1
            continue
        t = visible(read(page), with_href=True)
        mc = [c for c in nc if re.sub(r"\s+", " ", c) not in t]
        mw = [w for w in nw if w not in t]
        st = "OK" if not mc and not mw else "GAP"
        bad += st != "OK"
        print(f"{st}\t{s}\t{page}\tcode_miss={len(mc)}/{len(nc)}\tword_miss={len(mw)}/{len(nw)}\t{sorted(mc)[:4]}{sorted(mw)[:6]}")
    print(f"pairs={len(lines)} bad={bad} drift_rc={rc}")
    return 0 if bad == 0 and rc == 0 and lines else 1


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


def m_ar01():
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


def m_er01():
    bad = 0
    for p in B17_PAGES:
        h = read(p)
        t = visible(h)
        refs = len(CHARREF.findall(h))
        sm = len(re.findall(r"prefers-reduced-motion", styles(h)))
        lit_css = t.count("site.css")
        lit_rm = t.count("prefers-reduced-motion")
        need = {"docs/process/kaizen-flow.html": ("css", 1), "docs/react-kit/animation.html": ("rm", 4),
                "docs/react-kit/build-audit.html": ("rm", 2)}[p]
        lit = lit_css if need[0] == "css" else lit_rm
        ok = refs == 0 and sm == 0 and len(site_links(h)) == 1 and lit >= need[1]
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {p} charref={refs} style_motion={sm} site_css_links={len(site_links(h))} "
              f"text_site_css={lit_css} text_reduced_motion={lit_rm}")
    return 0 if bad == 0 else 1


def m_er03():
    t = visible(read("docs/onboarding-kit/search-strategy.html"))
    g4, g5 = t.count("G1~G4"), t.count("G1~G5")
    print(f"G1~G4={g4} G1~G5={g5}")
    return 0 if g4 == 0 and g5 >= 1 else 1


def ver_lines(page):
    out = []
    for i, line in enumerate(read(page).splitlines(), 1):
        vis = visible(line)
        if re.search(r"2\.6\.0|02\.06\.00\.51", vis) and not re.search(r"처음|최초|실측", vis):
            out.append(i)
    return out


def m_er04():
    bad = 0
    for p in ["failure-recipes", "materials", "bambu-fields-baseline"]:
        page = f"docs/bambu-kit/{p}.html"
        t = visible(read(page))
        tok = {k: t.count(k) for k in ["실행 때 조회", "Info.plist", "BBL.json", "02.06.00.05", "02.08.00.06", "02.08.02.61"]}
        loose = ver_lines(page) if p != "bambu-fields-baseline" else []
        ok = all(v >= 1 for v in tok.values()) and not loose
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {page} " + " ".join(f"{k}={v}" for k, v in tok.items()) + f" loose_version_lines={loose}")
    return 0 if bad == 0 else 1


def m_er05():
    s = read("onboarding-kit/skills/setup-guide/SKILL.md")
    t = visible(read("docs/onboarding-kit/setup-guide.html"))
    cs = sorted(codes(s))
    miss = [c for c in cs if re.sub(r"\s+", " ", c) not in t]
    rule = all(k in t for k in ["만들 수 없다", "막는 것", "시도한 우회", "통제 불가 사유", "재검증 명령"])
    print(f"code={len(cs) - len(miss)}/{len(cs)} rule_sentence={int(rule)} miss={miss}")
    return 0 if not miss and rule and cs else 1


def m_ka():
    """분류 도우미의 알려진 답 — 표 구분 줄 · HTML 주석만 바뀐 원본은 SHAPE, 낱말 하나(`__`→`_`)가 바뀐 원본은 REAL."""
    a = classify("docs/rust/data/caching.md")
    b = classify("docs/tone/overview.md")
    print(f"caching={a} tone_overview={b}")
    return 0 if (a, b) == ("SHAPE", "REAL") else 1


def m_ar03():
    bad = 0
    for p in B16_PAGES:
        old = show(B16_OLD, f"docs/{p}.html") or ""
        new = read(f"docs/{p}.html")
        pat = r'href="([a-z0-9-]+\.html|\.\./[a-z0-9-]+/[a-z0-9-]+\.html)"'
        lost = sorted(set(re.findall(pat, old)) - set(re.findall(pat, new)))
        parts = re.split(r"(?is)(<h2[^>]*>.*?</h2>)", new)
        body = {visible(parts[i]).strip(): len(visible(parts[i + 1]).strip()) for i in range(1, len(parts), 2)}
        need = B16_HEADINGS.get(p, [])
        miss_h = [x for x in need if body.get(x, 0) < 200]
        ok = not lost and not miss_h
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {p} links_lost={lost} headings_missing_or_short={miss_h}")
    return 0 if bad == 0 else 1


def m_ar05():
    notes = Path(".harness/.meta/after-kaizen-0928/d1-notes.md")
    if not notes.is_file():
        print("notes 없음")
        return 1
    rows = {}
    for line in read(notes).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.startswith("|") or len(cells) < 3:
            continue
        src = re.findall(r"`([^`]+)`", cells[0])
        if len(src) == 1:
            rows.setdefault(src[0], []).append(cells[1])
    _, lines, _ = drift_lines(KEEP_FLAG)
    mapped = {s: t for s, t, _ in pairs_of(lines)}
    reg, _ = registry()
    files = {"docs/" + f for _, f in reg}
    want = {**NEW_PAGES, **PAIRS, **D5_EXTRA, **{s: None for s in NO_PAGE}}
    bad = 0
    for src, page in sorted(want.items()):
        got = rows.get(src, [])
        if len(got) != 1:
            print(f"BAD {src} rows={len(got)}")
            bad += 1
            continue
        d = got[0]
        if page is None:
            ok = d.startswith("페이지 없음") and src not in mapped
        else:
            kind = "짝" if src in PAIRS else "새 페이지"
            ok = d.startswith(kind) and f"`{page}`" in d and page in files and mapped.get(src, page) == page
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {src} | {d}")
    print(f"rows_ok={len(want) - bad}/{len(want)}")
    return 0 if bad == 0 else 1


def m_ext(files=None):
    """바꾼 쪽 · 새 쪽이 레포 밖 자원을 부르지 않는다 — 큰따옴표 · 작은따옴표 · 따옴표 없음 · @import · url() · // 주소.
    파일을 주면 그 파일만 잰다 (양성 대조용)."""
    rc, out = (0, " ".join(files)) if files else git("diff", "--name-only", f"{BASE}..HEAD", "--", "docs")
    pages = [p for p in out.split() if p.endswith(".html") and Path(p).is_file()]
    pat = re.compile(r"""(?is)(?:<(?:script|img|iframe)\b[^>]*\bsrc|<link\b[^>]*\bhref)\s*=\s*["']?\s*(?:https?:)?//|@import\s*(?:url\()?\s*["']?\s*(?:https?:)?//|url\(\s*["']?\s*(?:https?:)?//""")
    bad = 0
    for p in pages:
        n = len(pat.findall(read(p)))
        if n:
            print(f"EXT {p} {n}")
            bad += 1
    print(f"checked={len(pages)} ext_pages={bad} git_rc={rc}")
    return 0 if bad == 0 and rc == 0 and pages else 1


def a11y(pages):
    """검사기는 파일 이름만 찍는다 — 이름이 겹치는 쪽(research-log 등)은 다른 묶음으로 돌려 쪽 경로로 되짚는다."""
    batches = []
    for p in pages:
        for b in batches:
            if all(Path(q).name != Path(p).name for q in b):
                b.append(p)
                break
        else:
            batches.append([p])
    rows, rcs = {}, []
    for b in batches:
        r = subprocess.run(["node", "scripts/check-docs-a11y.js", *b], capture_output=True, text=True)
        rcs.append(r.returncode)
        by_name = {Path(q).name: q for q in b}
        for line in r.stdout.splitlines():
            m = re.match(r"^(OK  |FAIL) (\S+)\s+of=(\S+) err=(\d+) contrastFail=(\d+).*btn=(\S+) theme=(\S+)", line)
            if m and m.group(2) in by_name:
                rows[by_name[m.group(2)]] = m.groups()
    return max(rcs, default=2), rows


def m_ar02():
    pages = A3_PAGES + list(NEW_PAGES.values())
    rc, rows = a11y([p for p in pages if Path(p).is_file()])
    t = subprocess.run(["node", ".harness/.meta/after-0928-docs-site/theme.js", "theme", *[p for p in pages if Path(p).is_file()]],
                       capture_output=True, text=True)
    theme = {l.split()[0]: l for l in t.stdout.splitlines()}
    want = "first_light=light first_dark=dark click=light stored=light reload=light bg_differs=1"
    bad = 0
    for p in pages:
        row = rows.get(p)
        th = theme.get(p, "")
        btn = row[5] if row else "none"
        wh = [int(x) for x in btn.split("x")] if "x" in btn else [0, 0]
        ok = bool(row) and row[0].strip() == "OK" and row[2] == "0/0/0/0" and row[6] == "both" \
            and min(wh) >= 44 and th.endswith(want)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {p} a11y={'/'.join(row[:1] + row[2:]) if row else 'none'} theme=[{th[len(p) + 1:]}]")
    print(f"ok={len(pages) - bad}/{len(pages)} a11y_rc={rc} theme_rc={t.returncode}")
    return 0 if bad == 0 and t.returncode == 0 else 1


def m_pages():
    """BASE 부터 바뀌거나 새로 생긴 docs 쪽 전부 — 넘침 0 · 콘솔 에러 0 · 대비 실패 0."""
    rc, out = git("diff", "--name-only", f"{BASE}..HEAD", "--", "docs")
    pages = [p for p in out.split() if p.endswith(".html") and Path(p).is_file() and p != "docs/index.html"]
    arc, rows = a11y(pages)
    bad = 0
    for p in pages:
        row = rows.get(p)
        ok = bool(row) and row[0].strip() == "OK" and row[2] == "0/0/0/0" and row[3] == "0" and row[4] == "0"
        bad += not ok
        if not ok:
            print(f"BAD {p} {row}")
    print(f"pages={len(pages)} bad={bad} a11y_rc={arc} git_rc={rc}")
    return 0 if bad == 0 and pages and rc == 0 else 1


SIGN = "Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
CONTRACT = ".harness/sprint-contract-after-0928-docs-site.md"


def scope_block():
    t = read(CONTRACT)
    sec = re.search(r"^## 범위 경계.*?(?=^## |\Z)", t, re.M | re.S)
    blk = re.search(r"```text\n# sprint-scope\n(.*?)```", sec.group(0) if sec else "", re.S)
    return [l.strip() for l in (blk.group(1) if blk else "").splitlines() if l.strip()]


def in_scope(path, scope):
    for s in scope:
        if s.endswith("/") and path.startswith(s):
            return True
        if path == s:
            return True
    return path.startswith(".harness/")


def m_commits():
    """BASE..HEAD 커밋마다: 합침 커밋 0 · 맨 위 폴더 하나(docs 는 docs/<킷>/ 하나 + docs/index.html 허용) ·
    .harness/ 와 구현 파일을 한 커밋에 싣지 않음 · 서명 줄 · 바뀐 파일이 범위 목록 안."""
    scope = scope_block()
    rc, revs = git("rev-list", "--reverse", f"{BASE}..HEAD")
    bad = 0
    for c in revs.split():
        _, parents = git("rev-list", "--parents", "-n", "1", c)
        _, files = git("show", "--name-only", "--format=", c)
        _, msg = git("log", "-1", "--format=%B", c)
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
        docs_only = all(t.startswith("docs") for t in tops)
        ok_top = len(tops) == 1 or (docs_only and len(tops) == 1)
        signed = SIGN in [l.strip() for l in msg.splitlines()]
        out = [f for f in fs if not in_scope(f, scope)]
        merge = len(parents.split()) > 2
        ok = ok_top and signed and not out and not merge
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {c[:7]} tops={sorted(tops)} signed={int(signed)} out_of_scope={out[:5]} merge={int(merge)}")
    n = len(revs.split())
    print(f"commits={n} bad={bad} scope_entries={len(scope)} git_rc={rc}")
    return 0 if bad == 0 and n and scope and rc == 0 else 1


CONDS = {
    "SC-01": m_sc01, "SC-02": m_sc02, "SC-03": m_sc03, "AR-04": m_ar04, "AR-01": m_ar01,
    "ER-01": m_er01, "ER-03": m_er03, "ER-04": m_er04, "ER-05": m_er05, "AR-03": m_ar03,
    "AR-05": m_ar05, "EXT": m_ext, "KA": m_ka, "AR-02": m_ar02, "PAGES": m_pages, "COMMITS": m_commits,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CONDS or (len(sys.argv) > 2 and sys.argv[1] != "EXT"):
        print("사용: python3 measure.py <" + "|".join(CONDS) + "> (EXT 만 파일 인자를 받는다)")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]](sys.argv[2:]) if sys.argv[1] == "EXT" else CONDS[sys.argv[1]]())
