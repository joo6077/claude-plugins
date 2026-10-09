#!/usr/bin/env python3
"""bambu 음성 대조 표의 기대 칸이 SKILL.md 와 문서 쪽에서 같은지 본다 (B5 · D7 페이지 맞추기).

쓰임: python3 b5-page-table.py <레포 뿌리>
시험 파일 이름마다 기대 칸(셋째 칸)을 마크다운 · HTML 꾸밈을 벗겨 맞댄다.
출력: TABLE skill_rows=<n> page_rows=<n> diff=<기대 칸이 다른 이름 수> only_one_side=<한쪽에만 있는 이름 수>
종료 코드: 0 같음 · 1 다름 · 2 표를 못 찾음
"""
import html, os, re, sys

root = sys.argv[1]
skill = open(os.path.join(root, "bambu-kit/skills/bambu-print-profile/SKILL.md"), encoding="utf-8").read()
page = open(os.path.join(root, "docs/bambu-kit/bambu-print-profile.html"), encoding="utf-8").read()


def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


rows_s = {}
for line in skill.split("\n"):
    m = re.match(r"^\| `evals/gate-fixtures/([^`]+\.json)` \|([^|]*)\|([^|]*)\|", line)
    if m:
        rows_s[m.group(1)] = norm(m.group(3))
rows_p = {}
for m in re.finditer(r"<tr><td><code>([a-z0-9-]+\.json)</code></td><td>[^<]*</td><td>(.*?)</td>", page):
    rows_p[m.group(1)] = norm(m.group(2))
if not rows_s or not rows_p:
    print(f"STOP 표 없음 skill={len(rows_s)} page={len(rows_p)}")
    sys.exit(2)
both = set(rows_s) & set(rows_p)
diff = [k for k in sorted(both) if rows_s[k] != rows_p[k]]
only = sorted(set(rows_s) ^ set(rows_p))
for k in diff:
    print(f"DIFF {k}\n  skill: {rows_s[k]}\n  page:  {rows_p[k]}")
for k in only:
    print(f"ONLY {k}")
print(f"TABLE skill_rows={len(rows_s)} page_rows={len(rows_p)} diff={len(diff)} only_one_side={len(only)}")
sys.exit(0 if not diff and not only else 1)
