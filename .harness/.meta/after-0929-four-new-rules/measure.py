"""계약 after-0929-four-new-rules 측정 도우미. 레포 맨 위 폴더에서 `python3 <이 파일> <조건>` 으로 부른다.

판은 BASE(시작 판 279085a3, 가지 chore/ak3-fs2 끝)와 작업 폴더 두 가지만 쓴다.
종료 코드는 셸의 $? 로 본다 — 0 조건 성립 · 1 불성립 · 2 잴 수 없음.
환경 변수 NR_ROOT 를 주면 그 폴더를 레포로 보고 잰다 (양성 · 음성 대조용 사본).
"""
import fnmatch
import html
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = "279085a3"
ROOT = os.environ.get("NR_ROOT") or os.getcwd()
CONTRACT = ".harness/sprint-contract-after-0929-four-new-rules.md"
NOTES = ".harness/.meta/after-kaizen-0928/nr-notes.md"
EX = [".harness/.meta/after-kaizen-0928/ex/A8.md", ".harness/.meta/after-kaizen-0928/ex/A10.md",
      ".harness/.meta/after-kaizen-0928/ex/A12.md"]
BR = ".harness/.meta/after-0929-final-sweep-docs/br.js"
SIGN_RE = re.compile(r"^Claude .+ <noreply@anthropic\.com>$")

SHAPE = "YYYY-MM-DDTHH:mm:ss[.fraction]"
KIT_SHAPE = "이 킷이 고른 형식"
Q_RFC = "All times expressed have a stated relationship (offset) to Coordinated Universal Time (UTC)."
Q_ISO = "September 27, 2022 at 6 p.m. is represented as 2022-09-27 18:00:00.000."
Q_ATL = ("A product requirements document (PRD) defines the purpose, features, and behavior of a product, "
         "aligning stakeholders and guiding development.")
Q_ADR = "An Architectural Decision Record (ADR) captures a single AD and its rationale."
Q_NYG = "Each record describes a set of forces and a single decision in response to those forces."
INFER = "원문에 직접 근거가 없는 추론"
KEEP_DATE = "조회일을 바꾸지 않는다"
KIT_RULE = "이 킷의 규칙"
Q_SA1 = "We recommend that you avoid using service account keys whenever possible."
Q_SA2 = ("Use Workload Identity Federation whenever an application needs to access Google Cloud "
         "and has access to ambient credentials.")
Q_SA3 = "this way of initializing the SDK is strongly recommended for applications running in Google environments"
Q_SA4 = "For client-side applications such as tools, desktop programs, or mobile apps, don't use service accounts."
ORDER = [("①", ["ADC"]), ("②", ["Workload Identity Federation for GKE"]), ("③", ["서비스 계정 가장"]),
         ("④", ["Workload Identity Federation", "외부"]), ("⑤", ["서비스 계정 키"])]

PAGES = {
    "backend": ("docs/backend/fundamentals/database.md", "docs/backend-kit/database.html"),
    "planning": ("docs/planning/prd-patterns.md", "docs/planning-kit/prd-patterns.html"),
    "onboarding": ("onboarding-kit/skills/setup-guide/SKILL.md", "docs/onboarding-kit/setup-guide.html"),
    "checklist": ("onboarding-kit/skills/setup-guide/references/format-checklist.md",
                  "docs/onboarding-kit/format-checklist.html"),
}
CHANGED_MD = [
    "backend-kit/skills/backend-system/SKILL.md", "backend-kit/skills/backend-audit/references/audit-criteria.md",
    "docs/backend/fundamentals/database.md", "planning-kit/skills/plan-prd/SKILL.md", "docs/planning/prd-patterns.md",
    "onboarding-kit/skills/setup-guide/SKILL.md", "onboarding-kit/skills/setup-guide/references/format-checklist.md",
]


def git(*args):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def show(ref, path):
    rc, out = git("show", f"{ref}:{path}")
    return out if rc == 0 else None


def read(path):
    p = Path(ROOT) / path
    return p.read_text(encoding="utf-8") if p.exists() else ""


def visible(h):
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))


def flat(s):
    return re.sub(r"\s+", " ", s)


def line_with(text, head):
    return next((l for l in text.splitlines() if l.startswith(head)), "")


def section(text, start_re, end_re):
    m = re.search(start_re, text, re.M)
    if not m:
        return ""
    rest = text[m.start():]
    nl = rest.find("\n") + 1 or len(rest)
    e = re.search(end_re, rest[nl:], re.M)
    return rest if not e else rest[: nl + e.start()]


def has(text, needles):
    return {n: (n in flat(text)) for n in needles}


def report(checks):
    miss = [k for k, v in checks.items() if not v]
    print(f"checks={len(checks)} missing={len(miss)}")
    for k in miss:
        print(f"  MISSING {k}")
    return 0 if not miss else 1


def ordered(text):
    """①~⑤ 가 차례대로 나오고, 각 표지부터 다음 표지 앞까지 그 자리의 낱말이 있는가."""
    pos, start = [], 0
    for mark, _ in ORDER:
        i = text.find(mark, start)
        if i < 0:
            return False, f"no {mark}"
        pos.append(i)
        start = i + 1
    for k, (mark, words) in enumerate(ORDER):
        seg = text[pos[k]: pos[k + 1] if k + 1 < len(pos) else len(text)]
        for w in words:
            if w not in seg:
                return False, f"{mark} lacks {w}"
    return True, "ok"


# ── 조건별 측정 ──

def m_skill1():
    """스킬-01: backend-kit 원본 둘이 벽시계 문자열 모양을 적는다."""
    g15 = line_with(read("backend-kit/skills/backend-system/SKILL.md"), "15. **timestamp")
    row = line_with(read("backend-kit/skills/backend-audit/references/audit-criteria.md"), "| Timestamp 직렬화 규칙 |")
    checks = {f"gotcha15:{k}": v for k, v in has(g15, [SHAPE, "type: string", "pattern", "example", KIT_SHAPE]).items()}
    checks.update({f"audit_row:{k}": v for k, v in has(row, [SHAPE, "type: string", "pattern", KIT_SHAPE]).items()})
    return report(checks)


def m_skill2():
    """스킬-02: plan-prd Gotcha 15 가 PRD · ADR 경계를 추론으로 표시해 적는다."""
    g15 = line_with(read("planning-kit/skills/plan-prd/SKILL.md"), "15. **")
    return report({f"gotcha15:{k}": v for k, v in has(g15, ["ADR", "비범위", INFER, "docs/planning/prd-patterns.md"]).items()})


def m_skill3():
    """스킬-03: 출처 원장 절 · 출처 줄 틀이 조회일과 원문 갱신일을 따로 적는다."""
    led = section(read(PAGES["onboarding"][0]), r"^### 출처 원장", r"^### ")
    tmpl = [l for l in read(PAGES["checklist"][0]).splitlines() if l.startswith("**출처:** <")]
    checks = {f"ledger:{k}": v for k, v in has(led, ["조회일", "Last updated", KEEP_DATE, KIT_RULE]).items()}
    checks["template_one_line"] = len(tmpl) == 1
    checks.update({f"template:{k}": v for k, v in has(tmpl[0] if tmpl else "", ["조회 YYYY-MM-DD", "Last updated"]).items()})
    return report(checks)


def m_skill4():
    """스킬-04: setup-guide Gotcha 10 이 서비스 계정 선택 순서를 적는다."""
    t = read(PAGES["onboarding"][0])
    g10 = section(t, r"^### Gotcha 10:", r"^##? ")
    heads = [l for l in t.splitlines() if re.match(r"^(### Gotcha \d+:|## Process)", l)]
    ok, why = ordered(g10)
    checks = {f"g10:{k}": v for k, v in has(g10, [Q_SA1, Q_SA2, Q_SA3, Q_SA4, "조회 2026-09-28",
                                                   "Last updated 2026-09-24 UTC"]).items()}
    checks[f"order({why})"] = ok
    checks["heads_tail=[Gotcha 9, Gotcha 10, Process]"] = [h.split(":")[0] for h in heads[-3:]] == [
        "### Gotcha 9", "### Gotcha 10", "## Process"]
    return report(checks)


def m_arch1():
    """구조-01: 데이터베이스 원칙 10 과 그 쪽이 벽시계 문자열 모양과 원문 인용 둘을 싣는다."""
    md, page = PAGES["backend"]
    p10 = section(read(md), r"^### 10\.", r"^(### |---)")
    need = [SHAPE, "type: string", "pattern", "example", Q_RFC, Q_ISO, KIT_SHAPE]
    checks = {f"md:{k}": v for k, v in has(p10, need).items()}
    checks.update({f"html:{k}": v for k, v in has(visible(read(page)), need).items()})
    return report(checks)


def m_arch2():
    """구조-02: PRD 원칙 문서와 그 쪽이 원문 인용 셋과 추론 표시를 싣는다."""
    md, page = PAGES["planning"]
    t = read(md)
    need = [Q_ATL, Q_ADR, Q_NYG, INFER]
    checks = {f"md:{k}": v for k, v in has(t, need).items()}
    checks["md:adr_heading"] = any(l.startswith("### ") and "ADR" in l for l in t.splitlines())
    checks.update({f"html:{k}": v for k, v in has(visible(read(page)), need).items()})
    return report(checks)


def m_arch3():
    """구조-03: 셋업 가이드 쪽 · 형식 목록 쪽이 두 날짜 규칙을 싣는다."""
    v1 = visible(read(PAGES["onboarding"][1]))
    v2 = visible(read(PAGES["checklist"][1]))
    checks = {f"setup_html:{k}": v for k, v in has(v1, ["Last updated", KEEP_DATE, KIT_RULE]).items()}
    checks["checklist_html:template"] = bool(re.search(r"\*\*출처:\*\* <[^>]*조회 YYYY-MM-DD[^>]*Last updated[^>]*>", v2))
    return report(checks)


def m_arch4():
    """구조-04: 셋업 가이드 쪽 Gotchas 목록이 10 항목이고 10 번이 선택 순서를 싣는다."""
    h = read(PAGES["onboarding"][1])
    sec = section(h, r'aria-labelledby="gotchas-title"', r"</section>")
    items = re.findall(r'<li><span class="check">(\d+)</span>(.*?)</li>', sec, re.S)
    nums = [n for n, _ in items]
    ten = visible(dict(items).get("10", ""))
    ok, why = ordered(ten)
    final = section(h, r'aria-labelledby="final-title"', r"</section>")
    checks = {
        "gotcha_items=1..10": nums == [str(i) for i in range(1, 11)],
        f"item10_order({why})": ok,
        "item10:Q_SA1": Q_SA1 in flat(ten),
        "desc:10개 체크": "10개 체크" in visible(sec),
        "desc:9개 체크 없음": "9개 체크" not in visible(sec),
        "final:서비스 계정 키": "서비스 계정 키" in visible(final),
        "final:Last updated": "Last updated" in visible(final),
    }
    print(f"gotcha_items={','.join(nums)}")
    return report(checks)


def m_drift():
    """구조-05: 드리프트 도구가 원본 · 쪽 넷을 짝짓고, 짝의 쪽이 모두 같은 구간에서 바뀌었고, 다른 쪽은 안 바뀌었다."""
    r = subprocess.run(["python3", "scripts/detect-docs-drift.py", "--since", BASE], cwd=ROOT,
                       capture_output=True, text=True)
    pairs = sorted(l.strip() for l in r.stdout.splitlines() if " → " in l)
    want = sorted(f"{s} → {h}" for s, h in PAGES.values())
    _, names = git("diff", "--name-only", f"{BASE}..HEAD")
    changed = set(names.split())
    pages_changed = sorted(f for f in changed if f.startswith("docs/") and f.endswith(".html"))
    new_mark = sum("[NEW" in l for l in r.stdout.splitlines())
    print(f"pairs={len(pairs)} drift_rc={r.returncode} new_marks={new_mark}")
    for p in pairs:
        print(f"  {p}")
    print(f"pages_changed={pages_changed}")
    ok = (pairs == want and r.returncode == 0 and new_mark == 0
          and pages_changed == sorted(h for _, h in PAGES.values()))
    return 0 if ok else 1


def m_overflow():
    """구조-06: 바뀐 쪽 넷이 두 테마 · 320 · 375 · 1280 에서 가로 넘침 0, 접근성 검사기 OK."""
    pages = sorted(h for _, h in PAGES.values())
    bad, rcs = 0, []
    for theme in ("dark", "light"):
        r = subprocess.run(["node", BR, "paint", theme, *pages], cwd=ROOT, capture_output=True, text=True)
        rcs.append(r.returncode)
        got = {l.split(" ", 1)[0]: l for l in r.stdout.splitlines()}
        for p in pages:
            m = re.search(r"of=(\S+)", got.get(p, ""))
            if not m or m.group(1) != "0/0/0":
                bad += 1
                print(f"BAD {theme} {p} of={m.group(1) if m else None}")
    a = subprocess.run(["node", "scripts/check-docs-a11y.js", *pages], cwd=ROOT, capture_output=True, text=True)
    rows = [l for l in a.stdout.splitlines() if re.match(r"^(OK  |FAIL) ", l)]
    ok_rows = sum(l.startswith("OK") for l in rows)
    print(f"pages={len(pages)} bad={bad} br_rc={','.join(map(str, rcs))} a11y_ok={ok_rows}/{len(rows)} a11y_rc={a.returncode}")
    return 0 if bad == 0 and not any(rcs) and ok_rows == len(rows) == len(pages) and a.returncode == 0 else 1


QUOTE_RE = re.compile(r"「([^」]+)」|“([^”]+)”|\"([^\"]+)\"")


def added_text(path):
    _, d = git("diff", "-U0", f"{BASE}..HEAD", "--", path)
    lines = [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
    t = "\n".join(lines)
    return visible(t) if path.endswith(".html") else t


def m_quotes():
    """오류-01: 새로 더한 글의 영어 원문 인용이 모두 대조 파일 글자 그대로다."""
    src = flat(" ".join(read(p) for p in EX).replace("`", ""))
    files = ["backend-kit/skills/backend-system/SKILL.md", "backend-kit/skills/backend-audit/references/audit-criteria.md",
             "planning-kit/skills/plan-prd/SKILL.md"] + [p for pair in PAGES.values() for p in pair]
    found, bad = set(), 0
    for f in files:
        for m in QUOTE_RE.finditer(added_text(f)):
            q = flat(next(g for g in m.groups() if g)).strip()
            if len(re.findall(r"[A-Za-z]+", q)) < 4 or re.search(r"[가-힣]", q):
                continue
            found.add(q)
            if q.replace("`", "") not in src:
                bad += 1
                print(f"BAD {f}: {q}")
    need = [Q_RFC, Q_ISO, Q_ATL, Q_ADR, Q_NYG, Q_SA1, Q_SA2, Q_SA3, Q_SA4]
    missing = [q for q in need if not any(q.rstrip(".") in f for f in found)]
    print(f"quotes={len(found)} bad={bad} need_missing={len(missing)} ex_len={len(src)}")
    for q in missing:
        print(f"  MISSING {q}")
    return 0 if bad == 0 and not missing and len(src) > 1000 else 1


def gate_block(text):
    m = re.search(r"^```bash\n(# Guide Conformance Gate.*?)^```$", text or "", re.M | re.S)
    return m.group(1) if m else None


def run_gate(block):
    r = subprocess.run(["bash", "-c", block + "\nguide_gate docs/onboarding-kit/examples/fcm-ios-setup-guide.md flutter"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout


def m_keep():
    """오류-02: 기존 동작 유지 — 가이드 게이트 코드 · 그 출력, 이웃 규칙 줄이 시작 판과 같다."""
    path = PAGES["onboarding"][0]
    b, h = gate_block(show(BASE, path)), gate_block(read(path))
    same_block = b is not None and b == h
    brc, bout = run_gate(b or "")
    hrc, hout = run_gate(h or "")
    keep = {
        "plan-prd gotcha14": ("planning-kit/skills/plan-prd/SKILL.md", "14. **"),
        "backend-system gotcha18": ("backend-kit/skills/backend-system/SKILL.md", "18. **"),
        "audit 시각 종류별 저장": ("backend-kit/skills/backend-audit/references/audit-criteria.md", "| 시각 종류별 저장 |"),
        "setup-guide gotcha9 head": (path, "### Gotcha 9:"),
    }
    checks = {"gate_block_same": same_block, "gate_out_same": bout == hout and brc == hrc == 0 and "GATE_PASS" in hout}
    for k, (f, head) in keep.items():
        bl, hl = line_with(show(BASE, f) or "", head), line_with(read(f), head)
        checks[k] = bool(bl) and bl == hl
    print(f"gate_rc={brc},{hrc} gate_tail=[{hout.strip().splitlines()[-1] if hout.strip() else ''}]")
    return report(checks)


def m_notes():
    """구조-07: 기록 파일에 규칙 넷의 커밋 · tone-guide · 남긴 것."""
    t = read(NOTES)
    keys = ["시각 문자열", "ADR", "조회일", "서비스 계정", "tone-guide", "남긴 것"]
    for k in keys:
        print(f"{k}={t.count(k)}")
    hashes = len(set(re.findall(r"\b[0-9a-f]{8}\b", t)))
    print(f"hashes={hashes}")
    return 0 if t and all(t.count(k) >= 1 for k in keys) and hashes >= 4 else 1


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
    """구조-08: BASE..HEAD 커밋마다 합침 아님 · 맨 위 폴더 하나(docs 는 docs/<폴더>) · .harness 는 따로 · 서명 줄 · 범위 안."""
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
            tops.add("docs/" + parts[1] if parts[0] == "docs" and len(parts) > 2 else parts[0])
        signed = any(SIGN_RE.match(t.strip()) for t in trailers.splitlines())
        out = [f for f in fs if not in_scope(f, scope)]
        merge = len(parents.split()) > 2
        ok = len(tops) == 1 and signed and not out and not merge
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {c[:8]} tops={sorted(tops)} signed={int(signed)} out_of_scope={out[:5]} merge={int(merge)}")
    n = len(revs.split())
    print(f"commits={n} bad={bad} scope_entries={len(scope)} git_rc={rc}")
    return 0 if bad == 0 and n and scope and rc == 0 else 1


CONDS = {
    "스킬-01": m_skill1, "스킬-02": m_skill2, "스킬-03": m_skill3, "스킬-04": m_skill4,
    "구조-01": m_arch1, "구조-02": m_arch2, "구조-03": m_arch3, "구조-04": m_arch4, "구조-05": m_drift,
    "구조-06": m_overflow, "구조-07": m_notes, "구조-08": m_commits, "오류-01": m_quotes, "오류-02": m_keep,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CONDS:
        print("사용: python3 measure.py <" + " | ".join(CONDS) + ">")
        sys.exit(2)
    sys.exit(CONDS[sys.argv[1]]())
