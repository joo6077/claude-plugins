#!/usr/bin/env python3
"""check-contrast-claims.py — 문서에 적힌 대비비 주장을 실제 값과 대조한다.

`#757575 on #FFFFFF` + `3.5:1 FAIL` 처럼 색 쌍과 수치가 같이 적힌 곳을 찾아
WCAG 상대휘도로 실제 비율을 계산하고 어긋나면 실패한다. 이건 눈으로 볼 일이 아니라 산수다.

`scripts/check-docs-a11y.js` 와 재는 것이 다르다 — 저쪽은 **렌더된 픽셀의 실제 대비**를,
이쪽은 **문서가 사실이라고 적어 놓은 수치**를 본다. 페이지가 실제로는 접근성을 지키면서도
"3.5:1 FAIL" 같은 틀린 설명을 달고 있을 수 있고, 그건 저쪽 게이트가 잡지 못한다.

실측 2026-09-05: `docs/design-kit/typography-scale.html` 이 `#757575 on #FFFFFF` 를
"3.5:1 FAIL" 로 적었는데 실제는 **4.61:1 (AA 통과)** 였고, 같은 표의 `#A0A0B8 on #1A1A2E`
는 "5.2:1" 인데 실제 **6.67** 이었다. 디자인 가이드가 대비 기준을 틀리게 가르치고 있었다.

한계: `A on B` 형태로 색 쌍이 명시된 자리만 본다. 표나 산문에 흩어진 주장은 못 잡는다.
그쪽은 사람이나 에이전트가 훑어야 한다.

Usage:
    python3 scripts/check-contrast-claims.py           # docs 전체
    python3 scripts/check-contrast-claims.py --json    # 기계 판독용

exit 0 = 어긋난 주장 없음, 1 = 있음.
"""
import re, pathlib, json, sys

def lum(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    f = lambda v: v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la+0.05)/(lb+0.05)

HEX = r'#[0-9a-fA-F]{3,8}'
# "A on B" / "A / B" / "A vs B" 형태로 색 쌍이 적힌 자리
PAIR = re.compile(rf'({HEX})\s*(?:on|/|vs\.?|위에?)\s*({HEX})', re.I)
RATIO = re.compile(r'([0-9]+(?:\.[0-9]+)?)\s*:\s*1')
VERDICT = re.compile(r'\b(AAA|AA|PASS|FAIL|통과|미달|실패)\b', re.I)

rows = []
for f in sorted(pathlib.Path('docs').rglob('*.html')):
    text = f.read_text(encoding='utf-8')
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for m in PAIR.finditer(line):
            fg, bg = m.group(1), m.group(2)
            # 색 쌍 뒤부터 3 줄 안에서 수치·판정을 찾는다 (배지가 다음 줄에 오는 마크업이 흔하다).
            # 쌍 앞은 보지 않는다 — 같은 문단에 있는 무관한 판정어를 이 쌍의 것으로 오인한다.
            window = '\n'.join([line[m.end():]] + lines[i+1:i+4])
            rm = RATIO.search(window)
            vm = VERDICT.search(window)
            if not rm and not vm:
                continue
            actual = ratio(fg, bg)
            stated = float(rm.group(1)) if rm else None
            rows.append({
                'file': str(f), 'line': i+1, 'fg': fg, 'bg': bg,
                'stated': stated, 'actual': round(actual, 2),
                'verdict': vm.group(1) if vm else None,
                'delta': None if stated is None else round(abs(stated-actual), 2),
            })

bad = []
for r in rows:
    problems = []
    if r['stated'] is not None and r['delta'] > 0.15:
        problems.append(f"수치 {r['stated']} vs 실제 {r['actual']}")
    v = (r['verdict'] or '').upper()
    a = r['actual']
    true_v = 'AAA' if a >= 7 else ('AA' if a >= 4.5 else 'FAIL')
    if v in ('FAIL', '미달', '실패') and a >= 4.5:
        problems.append(f"FAIL 로 표기했으나 실제 {a} → {true_v}")
    if v in ('AAA',) and a < 7:
        problems.append(f"AAA 로 표기했으나 실제 {a}")
    if v in ('AA', 'PASS', '통과') and a < 4.5:
        problems.append(f"{v} 로 표기했으나 실제 {a}")
    if problems:
        r['problems'] = problems
        bad.append(r)

if '--json' in sys.argv:
    print(json.dumps({'total': len(rows), 'bad': bad}, ensure_ascii=False, indent=1))
else:
    print(f"색 쌍 + 수치/판정이 함께 적힌 자리: {len(rows)}")
    print(f"어긋난 것: {len(bad)}\n")
    for r in bad:
        print(f"  {r['file']}:{r['line']}  {r['fg']} on {r['bg']}")
        for p in r['problems']:
            print(f"     └ {p}")
sys.exit(1 if bad else 0)
