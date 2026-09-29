"""계약 after-0929-leftovers 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

쪽 글 · 원본 · 목차를 읽는 함수와 브라우저 측정 br.js 는 앞 묶음 fs2 의 도우미를 그대로 불러 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

BASE = "ab637374"  # 시작 판 — fs1 · fs2 · nr 이 합쳐진 chore/after-kaizen-0928 끝
DRIFT_SINCE = "cacd9da3"  # fs2 가 쪽을 맞춘 기준 판. 그 뒤 fs1 · nr 이 바꾼 원본을 다시 본다
FIRST = "ca2181b2"  # 레포 첫 커밋 — 쪽 없는 원본을 모두 찾는다
FS2 = ".harness/.meta/after-0929-final-sweep-docs/measure.py"
NR = ".harness/.meta/after-0929-four-new-rules/measure.py"
JSM = ".harness/.meta/after-0929-leftovers/jsmotion.js"
CONTRACT = ".harness/sprint-contract-after-0929-leftovers.md"
NOTES = ".harness/.meta/after-kaizen-0928/rest-notes.md"
SKILL = "onboarding-kit/skills/setup-guide/SKILL.md"
SETUP_PAGE = "docs/onboarding-kit/setup-guide.html"
SC_SKILL = "harness/skills/sprint-contract/SKILL.md"
BTN_PAGES = [f"docs/howto-kit/{n}.html" for n in
             ("branch-catalog", "changelog-feeds", "deep-links", "deprecation-policy", "procedure-standards", "ui-anchoring")]
NEW_PAGES = {
    "reflect-kit/references/memory-grounding.md": "docs/reflect-kit/memory-grounding.html",
    "reflect-kit/skills/reflect-kaizen/SKILL.md": "docs/reflect-kit/reflect-kaizen.html",
}
DRIFT_PAIRS = [
    "bambu-kit/skills/bambu-print-profile/SKILL.md", "design-kit/skills/design-mockup/SKILL.md",
    "docs/backend/fundamentals/database.md", "docs/planning/flows.md", "docs/planning/prd-patterns.md",
    "harness/docs/guides/skill-design-guide.md", "harness/references/contract-schema.md",
    "onboarding-kit/skills/setup-guide/SKILL.md",
    "onboarding-kit/skills/setup-guide/references/format-checklist.md",
    "onboarding-kit/skills/setup-guide/references/search-strategy.md",
    "harness/docs/guides/contract-design-guide.md",
]
GUIDE = "harness/docs/guides/contract-design-guide.md"
GUIDE_PAGE = "docs/harness/contract-design-guide.html"
CI_SCOPE_HEAD = "범위 목록과 CI 전용 단계 맞대기"
CI_SCOPE_KEYS = ["# sprint-scope", ".github/workflows/ci.yml", "run:", "check-api-kit-docs.py",
                 "contract_ambiguity_notes", "봉인 전"]

spec = importlib.util.spec_from_file_location("fs2", FS2)
fs2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fs2)
read, git, visible, codes, words = fs2.read, fs2.git, fs2.visible, fs2.codes, fs2.words


def section(text, start, stop=r"^## |^### "):
    """start 줄부터 다음 stop 줄 앞까지. start 줄은 포함한다."""
    lines, out, on = text.splitlines(), [], False
    for line in lines:
        if on and re.match(stop, line):
            break
        if re.match(start, line):
            on = True
        if on:
            out.append(line)
    return "\n".join(out)


def report(checks):
    print(" ".join(f"{k}={int(v) if isinstance(v, bool) else v}" for k, v in checks.items()))
    return 0 if all(v is True for v in checks.values() if isinstance(v, bool)) else 1


def m_sc_gotcha():
    """스킬-01: sprint-contract Gotchas 에 봉인 전 기존 검사 대조 한 줄."""
    g = section(read(SC_SKILL), r"^## Gotchas", r"^## ")
    keys = ["봉인 전", "grep", "사본", "「더하라」", "「그대로」", "겹침"]
    hits = [l for l in g.splitlines() if l.startswith("- ") and all(k in l for k in keys)]
    return report({"line_hits": len(hits) == 1, "hit_count": len(hits), "keys": f"{len(keys)}"})


def m_g10():
    """스킬-02: Gotcha 10 목록에 번호와 ①~⑤ 가 겹치지 않는다."""
    g = section(read(SKILL), r"^### Gotcha 10:", r"^##? ")
    doubled = [l for l in g.splitlines() if re.match(r"^\s*\d+\.\s*[①②③④⑤]", l)]
    marks = [l.strip()[2] for l in g.splitlines() if re.match(r"^- [①②③④⑤]", l.strip())]
    return report({"doubled_zero": not doubled, "doubled": len(doubled),
                   "bullet_marks_in_order": marks == list("①②③④⑤"), "marks": "".join(marks)})


def phase4_steps(text):
    p4 = section(text, r"^### Phase 4:", r"^##? ")
    return [l for l in p4.splitlines() if re.match(r"^\d+\.\s", l)]


def page_phase4_items(h):
    m = re.search(r'(?s)<div class="step-where">Phase 4</div>.*?<ol>(.*?)</ol>', h)
    return [fs2.visible(li) for li in re.findall(r"(?s)<li>(.*?)</li>", m.group(1))] if m else []


def m_phase4():
    """스킬-03: setup-guide Phase 4 에 두 확인 단계 — 원본과 쪽 Phase 4 목록이 같은 수 · 같은 확인을 싣는다."""
    steps = phase4_steps(read(SKILL))
    items = page_phase4_items(read(SETUP_PAGE))
    date = lambda s: "조회일" in s and "Last updated" in s
    sa = lambda s: "서비스 계정 키" in s and "대안" in s and "Gotcha 10" in s
    return report({"skill_steps": len(steps), "page_steps": len(items), "same_count": len(steps) == len(items) > 0,
                   "skill_date": sum(map(date, steps)) == 1, "skill_sa": sum(map(sa, steps)) == 1,
                   "page_date": sum(map(date, items)) == 1, "page_sa": sum(map(sa, items)) == 1})


def last_date(path):
    _, out = git("log", "-1", "--format=%ad", "--date=short", "--", path)
    return out.strip()


def meta_dates(md, page):
    fm = re.search(r"^last_updated:\s*(\S+)", read(md), re.M)
    h = read(page)
    return (fm.group(1) if fm else None, re.findall(r"last_updated (\d{4}-\d{2}-\d{2})", h),
            re.findall(r"last updated (\d{4}-\d{2}-\d{2})", h))


def m_prd():
    """구조-01: prd-patterns 원본 머리 날짜와 쪽 두 자리 날짜가 nr 이 내용을 바꾼 날 2026-09-29 다."""
    fm, meta, foot = meta_dates("docs/planning/prd-patterns.md", "docs/planning-kit/prd-patterns.html")
    want = "2026-09-29"
    return report({"md": fm, "page_meta": ",".join(meta), "page_foot": ",".join(foot),
                   "ok": fm == want and meta == [want] and foot == [want]})


FLOW_KEYS = ["12.0.0", "2026-09-10", "비시험판", "2026-09-28", "registry.npmjs.org/mermaid/latest",
             "releases/tag/mermaid%4012.0.0", "렌더해 확인하지 않았다"]


def m_flows():
    """구조-02: flows 원본 61 줄 문장을 A10 교체안대로 — 원본 · 쪽 모두."""
    md = read("docs/planning/flows.md")
    lines = [l for l in md.splitlines() if l.startswith("아래 예시는 Mermaid 공식 flowchart 문법을 따른다")]
    line = lines[0] if len(lines) == 1 else ""
    h = read("docs/planning-kit/flows.html")
    shown = visible(h, with_href=True)
    miss_md = [k for k in FLOW_KEYS if k not in line]
    miss_page = [k for k in FLOW_KEYS if k not in shown]
    fm, meta, foot = meta_dates("docs/planning/flows.md", "docs/planning-kit/flows.html")
    want = last_date("docs/planning/flows.md")
    return report({"md_lines": len(lines), "md_keys_ok": len(lines) == 1 and not miss_md, "md_miss": miss_md,
                   "page_keys_ok": not miss_page, "page_miss": miss_page,
                   "stale_md": md.count("최신 안정판"), "stale_page": h.count("최신 안정판"),
                   "no_stale": md.count("최신 안정판") == 0 and h.count("최신 안정판") == 0,
                   "dates": f"{fm}/{','.join(meta)}/{','.join(foot)}/{want}",
                   "dates_ok": fm == want and meta == [want] and foot == [want]})


def m_theme6():
    """구조-03: 두 테마인데 단추 없던 howto-kit 여섯 쪽 — 단추 · 저장 · 다시 열기 (fs2 br.js theme)."""
    rc, lines, err = fs2.node("theme", *BTN_PAGES)
    got = fs2.by_page(lines)
    bad = 0
    for p in BTN_PAGES:
        r = got.get(p)
        wh = [int(x) for x in r["btn"].split("x")] if r and "x" in r["btn"] else [0, 0]
        ok = bool(r) and r["first_light"] == "light" and r["first_dark"] == "dark" and r["click"] == "light" \
            and r["stored"] == "light" and r["reload"] == "light" and r["bg_differs"] == "1" and min(wh) >= 44
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {p} {r}")
    print(f"theme_ok={len(BTN_PAGES) - bad}/{len(BTN_PAGES)} br_rc={rc}")
    return 0 if bad == 0 and rc == 0 else 1


def m_a11y():
    """구조-04: 접근성 검사기 docs 전체 — 모든 줄 OK · theme=both · btn=none 0 줄."""
    r = subprocess.run(["node", "scripts/check-docs-a11y.js"], capture_output=True, text=True)
    rows = [l for l in r.stdout.splitlines() if l.startswith(("OK", "FAIL"))]
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    fail = sum(1 for l in rows if l.startswith("FAIL"))
    both = sum(1 for l in rows if l.endswith("theme=both"))
    nobtn = [l.split()[1] for l in rows if " btn=none " in l]
    _, out = git("ls-files", "docs/*.html")
    n = len(out.split())
    print(f"rows={len(rows)} fail={fail} theme_both={both} btn_none={len(nobtn)} tracked={n} tail=[{tail}] rc={r.returncode}")
    for p in nobtn:
        print(f"NOBTN {p}")
    return 0 if r.returncode == 0 and fail == 0 and both == len(rows) == n and not nobtn and tail == f"{n}/{n} PASS" else 1


def m_new_pages():
    """구조-05: reflect-kit 새 쪽 둘 — 400 줄 · 목차 · 아이콘 · 공통 CSS 하나 · 원본 담김, 쪽 없는 원본 0."""
    reg, index = fs2.registry()
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
        wr, cin, cn, fin, fn = fs2.cov(src, page)
        links = len(fs2.site_links(h))
        ok = n >= 400 and uniq and icon and links == 1 and wr >= 0.95 and cin == cn and fin == fn
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {page} lines={n} reg={len(reg_ids)} id_unique={int(uniq)} icon={int(icon)} "
              f"site_css={links} wr={wr:.2f} code={cin}/{cn} fence={fin}/{fn}")
    r = subprocess.run(["python3", "scripts/detect-docs-drift.py", "--since", FIRST, "--include-format-only"],
                       capture_output=True, text=True)
    new = [l for l in r.stdout.splitlines() if "[NEW" in l]
    for l in new:
        print(f"NOPAGE {l.split(' → ')[0]}")
    print(f"new_pages_ok={len(NEW_PAGES) - bad}/{len(NEW_PAGES)} nopage={len(new)} drift_rc={r.returncode}")
    return 0 if bad == 0 and not new and r.returncode == 0 else 1


def m_drift():
    """구조-06: DRIFT_SINCE 뒤 원본 내용이 바뀐 짝 — 짝 목록이 DRIFT_PAIRS 와 같고, 원본이 새로 얻은
    인라인 코드 · 낱말을 쪽이 모두 싣는다."""
    r = subprocess.run(["python3", "scripts/detect-docs-drift.py", "--since", DRIFT_SINCE], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if " → " in l]
    srcs = sorted(l.split(" → ", 1)[0] for l in lines)
    bad = 0
    for l in lines:
        s, rest = l.split(" → ", 1)
        page = rest.split()[0]
        a = fs2.show(DRIFT_SINCE, s) or ""
        b = read(s) if Path(s).is_file() else ""
        nc, nw = codes(b) - codes(a), words(b) - words(a)
        if not Path(page).is_file() or "[NEW" in rest:
            print(f"NOPAGE\t{s}\t{page}")
            bad += 1
            continue
        t = visible(read(page), with_href=True)
        mc = [c for c in nc if re.sub(r"\s+", " ", c) not in t]
        mw = [w for w in nw if w not in t]
        st = "OK" if not mc and not mw else "GAP"
        bad += st != "OK"
        print(f"{st}\t{s}\t{page}\tcode_miss={len(mc)}/{len(nc)}\tword_miss={len(mw)}/{len(nw)}\t{sorted(mc)[:4]}{sorted(mw)[:6]}")
    same = srcs == sorted(DRIFT_PAIRS)
    extra = sorted(set(srcs) - set(DRIFT_PAIRS))
    lack = sorted(set(DRIFT_PAIRS) - set(srcs))
    print(f"pairs={len(lines)} bad={bad} same_set={int(same)} extra={extra} lack={lack} drift_rc={r.returncode}")
    return 0 if bad == 0 and same and r.returncode == 0 else 1


def changed_html():
    rc, out = git("diff", "--name-only", f"{BASE}..HEAD", "--", "docs")
    return [p for p in out.split() if p.endswith(".html") and Path(p).is_file()]


def m_overflow():
    """구조-07: 이번에 바뀌거나 새로 생긴 docs 쪽 — 두 테마 · 320 · 375 · 1280 가로 넘침 0."""
    pages = changed_html()
    bad, rcs = 0, []
    for theme in ("dark", "light"):
        rc, got = fs2.paint(theme, pages)
        rcs.append(rc)
        for p in pages:
            of = got.get(p, {}).get("of")
            if of != "0/0/0":
                bad += 1
                print(f"BAD {theme} {p} of={of}")
    print(f"pages={len(pages)} themes=2 bad={bad} br_rc={','.join(map(str, rcs))}")
    return 0 if bad == 0 and not any(rcs) and pages else 1


def jsm(motion):
    r = subprocess.run(["node", JSM, motion], capture_output=True, text=True)
    got = {}
    for l in r.stdout.splitlines():
        f = l.split("\t")
        got[f[0]] = int(f[-1].split("=")[1])
        print(l)
    return r.returncode, got


def m_js_reduce():
    """오류-01: 움직임 줄이기 설정에서 스크립트 움직임 셋이 누른 뒤 값을 바꾸지 않는다."""
    rc, got = jsm("reduce")
    ok = rc == 0 and len(got) == 3 and all(v == 0 for v in got.values())
    print(f"targets={len(got)} moving={sum(1 for v in got.values() if v)} jsm_rc={rc}")
    return 0 if ok else 1


def m_js_allow():
    """오류-02: 움직임 허용 설정에서는 셋 모두 그대로 움직인다."""
    rc, got = jsm("no-preference")
    ok = rc == 0 and len(got) == 3 and all(v >= 1 for v in got.values())
    print(f"targets={len(got)} moving={sum(1 for v in got.values() if v)} jsm_rc={rc}")
    return 0 if ok else 1


def m_prior():
    """오류-03: 앞 묶음 측정이 이 판에서도 그대로 통과한다 — nr 열 개, fs2 의 움직임 줄이기 · 쪽 안 움직임 규칙."""
    runs = [(NR, c) for c in ("스킬-01", "스킬-02", "스킬-03", "스킬-04", "구조-01", "구조-02", "구조-03", "구조-04",
                              "오류-01", "오류-02")] + [(FS2, "오류-01")]
    bad = 0
    for path, c in runs:
        r = subprocess.run(["python3", path, c], capture_output=True, text=True)
        tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        bad += r.returncode != 0
        print(f"{'OK ' if r.returncode == 0 else 'BAD'} {Path(path).parent.name} {c} rc={r.returncode} [{tail[:120]}]")
    print(f"runs={len(runs)} bad={bad}")
    return 0 if bad == 0 else 1


def m_ci_scope():
    """구조-11: 계약 설계 가이드에 범위 목록 × CI 전용 단계 점검 절 — 원본 · 쪽 모두."""
    md = read(GUIDE)
    heads = [l for l in md.splitlines() if l.startswith(f"### {CI_SCOPE_HEAD}")]
    sec = section(md, rf"^### {CI_SCOPE_HEAD}") if len(heads) == 1 else ""
    steps = [l for l in sec.splitlines() if re.match(r"^\d+\.\s", l)]
    md_miss = [k for k in CI_SCOPE_KEYS if k not in sec]
    shown = visible(read(GUIDE_PAGE), with_href=True)
    page_miss = [k for k in [CI_SCOPE_HEAD] + CI_SCOPE_KEYS if k not in shown]
    return report({"md_heads": len(heads), "md_head_ok": len(heads) == 1, "md_miss": md_miss,
                   "md_keys_ok": bool(sec) and not md_miss, "md_steps": len(steps), "md_steps_ok": len(steps) >= 3,
                   "page_miss": page_miss, "page_keys_ok": not page_miss})


def m_notes():
    """구조-08: 기록 파일."""
    if not Path(NOTES).is_file():
        print(f"{NOTES} 없음")
        return 1
    t = read(NOTES)
    keys = ["prd-patterns", "Gotcha 10", "Phase 4", "flows.md", "check-docs-common-css", "check-api-kit-docs",
            "테마 단추", "matchMedia", "memory-grounding", "reflect-kaizen", "드리프트", "sprint-contract",
            "tone-guide", "남긴 것"]
    miss = [k for k in keys if k not in t]
    hashes = len(set(re.findall(r"\b[0-9a-f]{8}\b", t)))
    return report({"keys_ok": not miss, "miss": miss, "hashes": hashes, "hashes_ok": hashes >= 6})


def m_ext():
    """구조-09: 바뀌거나 새로 생긴 docs 파일이 레포 밖 자원을 부르지 않는다 (fs2 와 같은 식)."""
    fs2.BASE = BASE
    return fs2.m_ext()


def m_commits():
    """구조-10: 커밋 규칙 (fs2 와 같은 식, 기준 판 · 계약만 이 묶음 것)."""
    fs2.BASE, fs2.CONTRACT = BASE, CONTRACT
    return fs2.m_commits()


CONDS = {
    "스킬-01": m_sc_gotcha, "스킬-02": m_g10, "스킬-03": m_phase4, "구조-01": m_prd, "구조-02": m_flows,
    "구조-03": m_theme6, "구조-04": m_a11y, "구조-05": m_new_pages, "구조-06": m_drift, "구조-07": m_overflow,
    "구조-08": m_notes, "구조-11": m_ci_scope, "구조-09": m_ext, "구조-10": m_commits, "오류-01": m_js_reduce, "오류-02": m_js_allow,
    "오류-03": m_prior,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
