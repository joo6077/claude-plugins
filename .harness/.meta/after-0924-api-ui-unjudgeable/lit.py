"""계약 after-0924-api-ui-unjudgeable 의 글자 검사. 사용: python3 lit.py <U 판 트리 폴더> <v8 파일>
각 줄은 `이름=값` 이다. 절은 제목 줄부터 같은 단계 이하의 다음 제목 전까지로 자른다."""
import re
import sys
from pathlib import Path

LABELS = ['PASS', 'FAIL', '미실행', '판정 불가']
tree, v8 = Path(sys.argv[1]), Path(sys.argv[2])
SK = (tree / 'api-kit/skills/api-ui/SKILL.md').read_text(encoding='utf-8')
VS = (tree / 'api-kit/skills/api-ui/references/viewer-spec.md').read_text(encoding='utf-8')
AL = (tree / 'api-kit/references/api-layout.md').read_text(encoding='utf-8')
AV = (tree / 'api-kit/skills/api-verify/SKILL.md').read_text(encoding='utf-8')
V8 = v8.read_text(encoding='utf-8') if v8.exists() else ''


def section(text, head):
    lines = text.split('\n')
    level = len(head) - len(head.lstrip('#'))
    out, on, fence = [], False, False
    for ln in lines:
        if re.match(r'^\s*(```|~~~)', ln):
            fence = not fence
        m = None if fence else re.match(r'^(#+) ', ln)
        if on and m and len(m.group(1)) <= level:
            break
        if ln.startswith(head):
            on = True
        if on:
            out.append(ln)
    return out


def all4(line):
    return all(L in line for L in LABELS)


def say(k, v):
    print(f'{k}={v}')


s = section(SK, '## Gotchas')
say('sk_gotcha_unj', sum(1 for ln in s if ln.startswith('- **') and '판정 불가' in ln))
s = section(SK, '## 1.')
say('sk_s1_reports_unj', sum(1 for ln in s if ln.startswith('| `reports/`') and '판정 불가' in ln))
s = section(SK, '## 2.')
order = [c for ln in s for c in LABELS if re.match(r'^\|\s*`' + re.escape(c) + r'`\s*\|', ln)]
say('sk_s2_order', '>'.join(order) or '-')
say('sk_s2_phrase', sum(ln.count('한쪽 경로라도 없으면') for ln in s))
say('sk_s2_line', sum(1 for ln in s if '(없음)' in ln and '→ 판정 불가' in ln))
s = section(SK, '## 6.')
say('sk_s6_top', sum(1 for ln in s if ln.startswith('상단바') and all4(ln)))
s = section(SK, '## 7.')
js = re.search(r'```js\n([\s\S]*?)\n```', '\n'.join(s))
say('sk_s7_keys', int(bool(js) and 'chips' in js.group(1) and 'rows' in js.group(1)))
m = next((ln for ln in s if ln.startswith('확정 시안 1280×720 실측')), '')
nums = dict(re.findall(r'\b(ep|shown|targets|under24|under44) (\d+)', m))
say('sk_s7_nums', ' '.join(f'{k}:{nums.get(k, "-")}' for k in ['ep', 'shown', 'targets', 'under24', 'under44']))
row = next((ln for ln in s if ln.startswith('| 누르는 자리 최소 크기')), '')
t = re.search(r'44 미만 (\d+)/(\d+) · 24 미만 (\d+)', row)
say('sk_s7_touch_row', '/'.join(t.groups()) if t else '-')
row = next((ln for ln in s if ln.startswith('| 인라인 항목 수')), '')
t = re.search(r'실측 (\d+) = (\d+)', row)
say('sk_s7_ep_row', '='.join(t.groups()) if t else '-')
s = section(SK, '## 8.')
say('sk_s8_counts', sum(1 for ln in s if ln.startswith('- ') and all4(ln)))
say('sk_v8', SK.count('api-ui-v8.html'))
say('sk_v7', SK.count('api-ui-v7'))

say('vs_v8', VS.count('api-ui-v8.html'))
say('vs_v7', VS.count('api-ui-v7'))
s = section(VS, '### 3.1')
say('vs_31_chips', sum(1 for ln in s if ln.startswith('| 요약 칩') and all4(ln)))
s = section(VS, '### 3.2')
say('vs_32_icons', sum(1 for ln in s if '상태 아이콘' in ln and '판정 불가' in ln))
s = section(VS, '### 3.5')
say('vs_35_unj', sum(ln.count('판정 불가') for ln in s))
say('vs_35_line', sum(1 for ln in s if '(없음)' in ln))
say('vs_35_failtab', sum(1 for ln in s if '실패 원인' in ln and '판정 불가' in ln))
s = section(VS, '## 4.')
st = next((ln for ln in s if re.match(r'^\s*state:', ln) and '//' in ln), '')
say('vs_4_state_values', len(re.findall(r"'[^']+'", st.split('//', 1)[1])) if st else 0)
s = section(VS, '## 6.')
rows6 = [ln for ln in s if ln.startswith('|') and '판정 불가' in ln]
hexes = sorted({h.lower() for ln in rows6 for h in re.findall(r'#[0-9a-fA-F]{6}\b', ln)})
say('vs_6_rows', len(rows6))
say('vs_6_hex', ','.join(hexes) or '-')
say('vs_6_hex_in_v8', f'{sum(1 for h in hexes if h in V8.lower())}/{len(hexes)}')
raw = 0
for h in hexes:
    allc = len(re.findall(re.escape(h), V8, re.I))
    decl = len(re.findall(r'--[\w-]+\s*:\s*' + re.escape(h), V8, re.I))
    raw += allc - decl
say('v8_hex_raw_uses', raw)
s = section(VS, '## 8.')
say('vs_8_text', sum(1 for ln in s if '텍스트 대응물' in ln and all4(ln)))
s = section(VS, '## 1.')
row = next((ln for ln in s if ln.startswith('| 누르는 자리')), '')
t = re.search(r'44 미만 (\d+)/(\d+) · 24 미만 (\d+)', row)
say('vs_1_touch_row', '/'.join(t.groups()) if t else '-')

say('al_reports_unj', sum(1 for ln in AL.split('\n') if ln.startswith('| `reports/` | `/api-verify`') and '판정 불가' in ln))
say('av_phrase', AV.count('한쪽 경로라도 없으면'))
say('av_line', sum(1 for ln in AV.split('\n') if '(없음)' in ln and '→ 판정 불가' in ln))

bad = 0
for p in (tree / 'api-kit').rglob('*'):
    if p.is_file():
        try:
            bad += p.read_text(encoding='utf-8').count('판정불가')
        except UnicodeDecodeError:
            pass
say('bad_spelling', bad + V8.count('판정불가'))
