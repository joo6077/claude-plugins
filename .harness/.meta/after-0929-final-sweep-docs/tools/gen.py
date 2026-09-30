"""원본 md 한 편을 문서 사이트 쪽 HTML 로 옮긴다. 쪽마다 머리글·요점 카드는 pages.py 가 준다.

`python3 gen.py <레포 폴더> [쪽 경로…]` — 앞 묶음(dr2)이 scratch 에 두었던 변환기를 fs2 가 레포 기록 폴더로 옮겼다.
"""
import html
import re
import sys
from pathlib import Path

E = lambda s: html.escape(s, quote=False)
EA = lambda s: html.escape(s, quote=True)

URL_RE = re.compile(r'https?://[^\s)<>\]"\'`|]+')


INLINE_URL_RE = re.compile(r'https?://[^\s)<>\]"\'`|\x00\x01]+')


def inline(s):
    """인라인 마크다운: 코드 · 링크 · 맨 주소 · 굵게 · 기울임. 코드는 먼저 떼어 두어 굵게가 코드를 건너 묶이게 한다."""
    codes = []

    def hold(m):
        codes.append('<code>' + E(m.group(1)) + '</code>')
        return '\x01%d\x01' % (len(codes) - 1)

    s = re.sub(r'`([^`\n]+)`', hold, s)
    s = inline_text(s)
    return re.sub(r'\x01(\d+)\x01', lambda m: codes[int(m.group(1))], s)


def inline_text(s):
    tokens = []

    def keep(h):
        tokens.append(h)
        return '\x00%d\x00' % (len(tokens) - 1)

    def link(m):
        text, url = m.group(1), m.group(2)
        if url.startswith(('http://', 'https://')):
            return keep('<a class="ext" href="%s" target="_blank" rel="noopener">%s</a>' % (EA(url), inline_text(text)))
        return keep('<span class="xref">%s</span> <span class="xref-path">(%s)</span>' % (inline_text(text), E(url)))

    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, s)

    def bare(m):
        u = m.group(0)
        tail = ''
        while u and u[-1] in '.,;:':
            tail = u[-1] + tail
            u = u[:-1]
        return keep('<a class="ext" href="%s" target="_blank" rel="noopener">%s</a>' % (EA(u), E(u))) + tail

    s = re.sub(r'<(https?://[^>\s]+)>', lambda m: keep('<a class="ext" href="%s" target="_blank" rel="noopener">%s</a>' % (EA(m.group(1)), E(m.group(1)))), s)
    s = INLINE_URL_RE.sub(bare, s)
    s = E(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)([^*\n]+?)\*(?![\w*])', r'<em>\1</em>', s)
    return re.sub(r'\x00(\d+)\x00', lambda m: tokens[int(m.group(1))], s)


def split_row(row):
    row = row.strip()
    if row.startswith('|'):
        row = row[1:]
    if row.endswith('|') and not row.endswith('\\|'):
        row = row[:-1]
    cells, cur, in_code = [], '', False
    i = 0
    while i < len(row):
        c = row[i]
        if c == '`':
            in_code = not in_code
        if c == '\\' and i + 1 < len(row) and row[i + 1] == '|':
            cur += '\\|'
            i += 2
            continue
        if c == '|' and not in_code:
            cells.append(cur.strip())
            cur = ''
        else:
            cur += c
        i += 1
    cells.append(cur.strip())
    return cells


def cell_inline(c):
    """표 칸의 \\| 는 코드 안에서는 원문 그대로 두고(원본이 글자 그대로 논하는 표기), 글에서는 | 로 보인다."""
    parts = re.split(r'(`[^`\n]+`)', c)
    return ''.join(p if p.startswith('`') else p.replace('\\|', '|') for p in parts)


class Doc:
    def __init__(self, md):
        self.lines = md.split('\n')
        self.fm = []
        if self.lines and self.lines[0].strip() == '---':
            end = self.lines.index('---', 1)
            self.fm = self.lines[1:end]
            self.lines = self.lines[end + 1:]
        self.title = None
        self.sections = []   # (level, heading, [html blocks])
        self.urls = []

    def parse(self):
        blocks_intro = []
        cur = None
        L = self.lines
        i = 0
        para = []

        def flush_para(target):
            if para:
                target.append('<p>' + inline(' '.join(x.strip() for x in para)) + '</p>')
                para.clear()

        def target():
            if cur is None:
                return blocks_intro
            return cur[2]

        while i < len(L):
            line = L[i]
            m = re.match(r'^(\s*)(```+|~~~+)(.*)$', line)
            if m:
                flush_para(target())
                fence, lang = m.group(2), m.group(3).strip()
                ind = len(m.group(1))
                body = []
                i += 1
                while i < len(L) and not re.match(r'^\s*' + re.escape(fence[0]) + '{%d,}\\s*$' % len(fence), L[i]):
                    body.append(L[i][ind:] if L[i][:ind].strip() == '' else L[i])
                    i += 1
                i += 1
                label = '<span class="code-lang">%s</span>' % E(lang) if lang else ''
                target().append('<div class="code">%s<pre><code>%s</code></pre></div>' % (label, E('\n'.join(body))))
                continue
            h = re.match(r'^(#{1,4})\s+(.*)$', line)
            if h:
                flush_para(target())
                lvl, text = len(h.group(1)), h.group(2).strip()
                if lvl == 1 and self.title is None:
                    self.title = text
                    i += 1
                    continue
                if lvl <= 2:
                    cur = [2, text, []]
                    self.sections.append(cur)
                else:
                    target().append('<h%d class="sub">%s</h%d>' % (lvl, inline(text), lvl))
                i += 1
                continue
            if line.strip().startswith('|') and i + 1 < len(L) and re.match(r'^\s*\|?\s*:?-+', L[i + 1]):
                flush_para(target())
                head = split_row(line)
                i += 2
                rows = []
                while i < len(L) and L[i].strip().startswith('|'):
                    rows.append(split_row(L[i]))
                    i += 1
                t = ['<div class="table-wrap"><table>', '<thead><tr>']
                t += ['  <th><div class="c">%s</div></th>' % inline(cell_inline(c)) for c in head]
                t.append('</tr></thead><tbody>')
                for r in rows:
                    t.append('<tr>')
                    t += ['  <td><div class="c">%s</div></td>' % inline(cell_inline(c)) for c in r]
                    t.append('</tr>')
                t.append('</tbody></table></div>')
                target().append('\n'.join(t))
                continue
            if line.startswith('>'):
                flush_para(target())
                q = []
                while i < len(L) and L[i].startswith('>'):
                    q.append(L[i][1:].strip())
                    i += 1
                paras, buf = [], []
                for x in q:
                    if x == '':
                        if buf:
                            paras.append(' '.join(buf))
                            buf = []
                    else:
                        buf.append(x)
                if buf:
                    paras.append(' '.join(buf))
                target().append('<blockquote class="quote">%s</blockquote>' % ''.join('<p>%s</p>' % inline(p) for p in paras))
                continue
            lm = re.match(r'^(\s*)([-*]|\d+[.)])\s+(.*)$', line)
            if lm:
                flush_para(target())
                items = []
                while i < len(L):
                    lm = re.match(r'^(\s*)([-*]|\d+[.)])\s+(.*)$', L[i])
                    if lm:
                        items.append([len(lm.group(1)) // 2, lm.group(2), lm.group(3)])
                        i += 1
                        continue
                    if items and L[i].startswith('  ') and L[i].strip() and not re.match(r'^\s*(```|~~~)', L[i]):
                        items[-1][2] += ' ' + L[i].strip()
                        i += 1
                        continue
                    break
                ordered = bool(re.match(r'\d', items[0][1]))
                out = ['<ul class="md-list%s">' % (' ordered' if ordered else '')]
                for lv, mark, text in items:
                    num = '<span class="li-mark">%s</span>' % E(mark) if re.match(r'\d', mark) else '<span class="li-mark dot" aria-hidden="true"></span>'
                    out.append('  <li class="lv%d">%s<div class="li-body">%s</div></li>' % (min(lv, 3), num, inline(text)))
                out.append('</ul>')
                target().append('\n'.join(out))
                continue
            if re.match(r'^\s*(-{3,}|\*{3,})\s*$', line):
                flush_para(target())
                target().append('<hr class="rule">')
                i += 1
                continue
            if line.strip() == '':
                flush_para(target())
                i += 1
                continue
            para.append(line)
            i += 1
        flush_para(target())
        self.intro = blocks_intro
        return self


def fm_table(fm):
    if not fm:
        return ''
    rows = []
    key, val = None, []
    for l in fm:
        m = re.match(r'^([A-Za-z_][\w-]*):\s?(.*)$', l)
        if m:
            if key is not None:
                rows.append((key, '\n'.join(val)))
            key, val = m.group(1), [m.group(2)]
        else:
            val.append(l)
    if key is not None:
        rows.append((key, '\n'.join(val)))
    t = ['<div class="table-wrap"><table class="fm">', '<thead><tr><th>머리 설정 키</th><th>값</th></tr></thead><tbody>']
    for k, v in rows:
        t.append('<tr><td><code>%s</code></td><td class="fm-val">%s</td></tr>' % (E(k), inline(v.strip())))
    t.append('</tbody></table></div>')
    return '\n'.join(t)


def slug(i):
    return 's%d' % i


def render(cfg, src_text, template_css):
    d = Doc(src_text).parse()
    urls = []
    for u in URL_RE.findall(src_text):
        u = u.rstrip('.,;:')
        if u not in urls:
            urls.append(u)
    out = []
    w = out.append
    w('<!DOCTYPE html>')
    w('<html lang="ko" data-theme="dark">')
    w('<head>')
    w('<meta charset="UTF-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w('<title>%s — %s</title>' % (E(cfg['title']), E(cfg['kit'])))
    w('<link rel="stylesheet" href="../assets/site.css">')
    w('<style>')
    css = template_css
    for k, v in cfg['css'].items():
        css = css.replace('{{%s}}' % k, v)
    w(css.rstrip('\n'))
    w('</style>')
    w('</head>')
    w('<body>')
    w('<div class="page">')
    w('')
    w('<div class="topbar">')
    w('  <a href="../index.html" class="nav-back">&#8592; %s</a>' % E(cfg['kit']))
    w('  <button class="theme-toggle" id="theme-btn" type="button" onclick="toggleTheme()" aria-label="테마 전환">Dark</button>')
    w('</div>')
    w('')
    w('<header class="hero">')
    w('  <span class="eyebrow">%s</span>' % E(cfg['eyebrow']))
    w('  <h1>%s</h1>' % E(cfg['title']))
    if d.title and d.title != cfg['title']:
        w('  <p class="orig-title">원본 제목: <strong>%s</strong></p>' % inline(d.title))
    w('  <p class="subtitle">%s</p>' % cfg['subtitle'])
    w('  <div class="meta">')
    for b in cfg['badges']:
        w('    <span class="badge">%s</span>' % b)
    w('  </div>')
    w('</header>')
    w('')
    w('<section class="section" aria-labelledby="glance">')
    w('  <div class="section-label" id="glance">한눈에</div>')
    w('  <div class="glance">')
    for c in cfg['cards']:
        w('    <div class="card glance-card">')
        w('      <h3>%s</h3>' % c[0])
        w('      <p>%s</p>' % c[1])
        w('    </div>')
    w('  </div>')
    w('</section>')
    w('')
    if cfg.get('extra'):
        w(cfg['extra'].strip('\n'))
        w('')
    w('<nav class="toc" aria-label="목차">')
    w('  <div class="section-label">목차</div>')
    w('  <ol class="toc-list">')
    for n, s in enumerate(d.sections, 1):
        w('    <li><a href="#%s"><span class="toc-n">%02d</span>%s</a></li>' % (slug(n), n, inline(s[1])))
    if urls:
        w('    <li><a href="#refs"><span class="toc-n">··</span>출처 주소 모음</a></li>')
    w('  </ol>')
    w('</nav>')
    w('')
    if d.fm or d.intro:
        w('<section class="section lead-block">')
        w('  <div class="section-label">원본 머리말</div>')
        if d.fm:
            w(fm_table(d.fm))
        for b in d.intro:
            w(b)
        w('</section>')
        w('')
    for n, (lvl, head, blocks) in enumerate(d.sections, 1):
        w('<section class="section doc" id="%s">' % slug(n))
        w('  <div class="section-label">§ %02d</div>' % n)
        w('  <h2>%s</h2>' % inline(head))
        w('  <div class="doc-body">')
        for b in blocks:
            w(b)
        w('  </div>')
        w('</section>')
        w('')
    if urls:
        w('<section class="section" id="refs">')
        w('  <div class="section-label">출처 주소 모음</div>')
        w('  <p class="desc">원본에 적힌 주소 %d 개를 나온 순서대로 옮겼다. 본문의 링크와 같은 곳을 가리킨다.</p>' % len(urls))
        w('  <ol class="refs">')
        for u in urls:
            w('    <li><a class="card-source" href="%s" target="_blank" rel="noopener">&#8599; %s</a></li>' % (EA(u), E(u)))
        w('  </ol>')
        w('</section>')
        w('')
    w('<footer class="foot">')
    w('  <p>원본 <code>%s</code> 의 기준 판은 커밋 <code>%s</code> 이다. 원본이 바뀌면 <code>python3 scripts/detect-docs-drift.py</code> 가 이 쪽을 다시 맞출 대상으로 낸다.</p>' % (E(cfg['src']), cfg.get('base', '38cccd1')))
    w('</footer>')
    w('')
    w('</div>')
    w('')
    w('<script>')
    w("function applyTheme(t){")
    w("  document.documentElement.setAttribute('data-theme', t);")
    w("  const btn = document.getElementById('theme-btn');")
    w("  if(btn) btn.textContent = t === 'dark' ? 'Dark' : 'Light';")
    w("}")
    w("function toggleTheme(){")
    w("  const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';")
    w("  try { localStorage.setItem('dk-theme', next); } catch (e) {}")
    w("  applyTheme(next);")
    w("}")
    w("(function initTheme(){")
    w("  let saved = null;")
    w("  try { saved = localStorage.getItem('dk-theme'); } catch (e) {}")
    w("  applyTheme(saved ?? (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'));")
    w("})();")
    w('</script>')
    w('</body>')
    w('</html>')
    # 본문 글의 이름은 원래 글자로 둔다 — 공통 CSS 검사는 <style> 안만 센다(docs-site Gotcha 1)
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    import importlib.util
    here = Path(__file__).parent
    spec = importlib.util.spec_from_file_location('pages', here / 'pages.py')
    pages = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pages)
    repo = Path(sys.argv[1])
    css = (here / 'page.css').read_text(encoding='utf-8')
    only = sys.argv[2:]
    for cfg in pages.PAGES:
        if only and cfg['out'] not in only:
            continue
        src = (repo / cfg['src']).read_text(encoding='utf-8')
        (repo / cfg['out']).parent.mkdir(parents=True, exist_ok=True)
        (repo / cfg['out']).write_text(render(cfg, src, css), encoding='utf-8')
        print('wrote', cfg['out'])
