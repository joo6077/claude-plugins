#!/usr/bin/env python3
"""시안 개수 규칙 자리 검사 — sites.py <레포 뿌리>

자리마다 구간을 잘라 태그 · ** · 백틱을 걷어 낸 뒤
  need  : 반드시 들어 있어야 할 글자
  old   : 옛 규칙 글자 (0 번이어야 한다)
를 센다. 줄 모양: SITE <ID> <파일> need_miss=<빠진 글자|-> old=<수> ok=<0|1>
마지막 줄: SITES total=<n> ok=<k> bad=<m> — bad=0 이면 종료 코드 0, 아니면 1, 파일 · 구간을 못 찾으면 2.
"""
import json, re, sys, os

OLD = (r"미지정[^0-9\n]{0,6}3|최대 ?5|상한 ?5|배치를 나(눠|누어)|그 이상 늘리지 않|늘리지 않음"
       r"|§5\.6 ?의 ?(기본값)? ?\(?3|시안 ?3 ?개|정확히 3 ?개|다섯 개(를)? 전부")
OLD_DK = OLD + r"|개수 상한|정본 규칙\(상한"
RULE = ["최소 5", "위 제한 없"]

# (ID, 파일, 시작 정규식, 끝 정규식(None=시작 줄 하나), need, old)
SITES = [
 ("S01", "design-kit/skills/design-mockup/SKILL.md", r"^description:", r"^argument-hint:", RULE, OLD_DK),
 ("S02", "design-kit/skills/design-mockup/SKILL.md", r"^16\. ", None, RULE, OLD_DK),
 ("S03", "design-kit/skills/design-mockup/SKILL.md", r"^### Step 2-a", r"^### Step 2-b", RULE + ["정확히 그 수"], OLD_DK),
 ("S04", "design-kit/skills/design-mockup/SKILL.md", r"^### Step 2-b", r"^## Step 3", ["풀 밖", "칸 묶음"], OLD_DK),
 ("S05", "design-kit/references/visual-change-protocol.md", r"^## 5\. Variant Contract Matrix", r"^### variant 필수", RULE + ["정확히 그 수"], OLD_DK),
 ("S06", "design-kit/skills/design-concept/SKILL.md", r"^6\. ", None, ["§5.6"], OLD_DK),
 ("S07", "design-kit/evals/evals.json", "json-id:19", None, ["최소 5"], OLD),
 ("S08", "design-kit/README.md", r"^\| `design-mockup` \|", None, RULE, OLD_DK),
 ("S10", "harness/docs/guides/skill-design-guide.md", r"^## 5\.6\. ", r"^## 6\. ", RULE + ["상한 3"], OLD),
 ("S11", "harness/docs/guides/skill-design-guide.md", r"^\| \*\*Variant Budget\*\* \|", None, RULE, OLD),
 ("S12", "docs/design-kit/design-mockup.html", r'class="hero-meta"', r"</div>", RULE, OLD_DK),
 ("S13", "docs/design-kit/design-mockup.html", r"<td>사용자 지정 시안</td>", r"구별성: 지정 축 3개 이상", RULE, OLD_DK),
 ("S14", "docs/design-kit/design-mockup.html", r"Step 2-a ·", r"Step 2-b ·", RULE + ["정확히 그 수"], OLD_DK),
 ("S15", "docs/design-kit/design-mockup.html", r"Step 2-b ·", r'id="step3-title"', ["풀 밖", "칸 묶음"], OLD_DK),
 ("S16", "docs/design-kit/design-mockup.html", r'<span class="check">16</span>', None, RULE, OLD_DK),
 ("S17", "docs/design-kit/design-reference.html", r'class="next-desc">[^<]*하이파이 HTML 시안 생성', None, RULE, OLD_DK),
 ("S18", "docs/design-kit/visual-change-protocol.html", r"<!-- 5\. VARIANT CONTRACT MATRIX -->", r"variant 필수 4 필드", RULE + ["정확히 그 수"], OLD_DK),
 ("S19", "docs/design-kit/design-template.html", r'<div class="tmpl-filename">mockup\.html</div>', r'class="tmpl-desc"', ["최소 5"], OLD_DK),
 ("S20", "docs/harness/skill-design-guide.html", r"<!-- ═══ 5\.6 Variant Budget", r"<!-- ═══ 6\. ", RULE + ["상한 3"], OLD),
 ("S21", "docs/harness/skill-design-guide.html", r"<td><strong>Variant Budget</strong></td>", None, RULE, OLD),
]

def norm(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("**", "").replace("`", "").replace("&nbsp;", " ")
    return s

def region(path, start, end):
    if start.startswith("json-id:"):
        want = int(start.split(":")[1])
        d = json.load(open(path, encoding="utf-8"))
        ev = d["evals"] if isinstance(d, dict) else d
        hit = [e for e in ev if e.get("id") == want]
        return json.dumps(hit[0], ensure_ascii=False) if hit else None
    lines = open(path, encoding="utf-8").read().split("\n")
    for i, l in enumerate(lines):
        if re.search(start, l):
            if end is None:
                return l
            out = [l]
            for m in lines[i + 1:]:
                out.append(m)
                if re.search(end, m):
                    return "\n".join(out)
            return None
    return None

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    ok = bad = 0
    err = False
    for sid, rel, start, end, need, old in SITES:
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            print(f"SITE {sid} {rel} MISSING_FILE"); err = True; continue
        r = region(p, start, end)
        if r is None:
            print(f"SITE {sid} {rel} MISSING_REGION"); err = True; continue
        t = norm(r)
        miss = [n for n in need if n not in t]
        o = len(re.findall(old, t))
        good = int(not miss and o == 0)
        ok += good; bad += 1 - good
        print(f"SITE {sid} {rel} need_miss={'|'.join(miss) if miss else '-'} old={o} ok={good}")
    print(f"SITES total={len(SITES)} ok={ok} bad={bad}")
    sys.exit(2 if err else (0 if bad == 0 else 1))

main()
