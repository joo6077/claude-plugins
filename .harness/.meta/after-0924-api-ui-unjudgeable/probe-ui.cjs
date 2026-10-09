// 계약 after-0924-api-ui-unjudgeable 의 바깥 측정기. 구현이 만든 검사와 따로 돈다.
// 사용: node probe-ui.cjs <ui.html> <캡처 폴더> <이름> [§7 식을 뽑을 SKILL.md]
// 종료 코드: 0 = 판정 줄 전부 OK, 1 = NG 가 하나 이상, 2 = 측정 자체가 실패
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const LABELS = ['PASS', 'FAIL', '미실행', '판정 불가'];
const UNJ = '판정 불가';
const COMBOS = [[1280, 720, 'light'], [1280, 720, 'dark'], [375, 812, 'light'], [375, 812, 'dark']];

function section7Expr(skillPath) {
  const text = fs.readFileSync(skillPath, 'utf8');
  const at = text.indexOf('\n## 7.');
  if (at < 0) throw new Error('SKILL.md 에 ## 7. 절이 없다');
  const m = text.slice(at).match(/```js\n([\s\S]*?)\n```/);
  if (!m) throw new Error('## 7. 절에 js 코드 블록이 없다');
  return m[1];
}

// 페이지 안에서 도는 공용 함수 — 대비 식은 scripts/check-docs-a11y.js:74-76 과 같은 WCAG 상대 휘도 식이다
const HELPERS = `
  window.__p = {
    LABELS: ${JSON.stringify(LABELS)},
    shown(el) { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; },
    parse(c) { const m = (c || '').match(/[\\d.]+/g); return m ? m.map(Number) : null; },
    lum(rgb) { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2]); },
    ratio(a, b) { const [x, y] = [this.lum(a), this.lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); },
    bgOf(el) { for (let n = el; n; n = n.parentElement) { const c = this.parse(getComputedStyle(n).backgroundColor);
        if (c && (c.length < 4 || c[3] > 0.5)) return c; }
      return this.parse(getComputedStyle(document.body).backgroundColor) || [255, 255, 255]; },
    rowLabel(row) { const hit = this.LABELS.filter(L => row.textContent.includes(L));
      return hit.length === 1 ? hit[0] : 'AMBIGUOUS:' + hit.join('|'); },
    glyph(el) { const svgs = el.querySelectorAll('svg'); return svgs.length ? svgs[svgs.length - 1] : null; },
    glyphInfo(el) { const g = this.glyph(el); if (!g) return null;
      const color = this.parse(getComputedStyle(g).color);
      return { color: getComputedStyle(g).color, shape: g.innerHTML.replace(/\\s+/g, ' ').trim(),
               ratio: color ? +this.ratio(color, this.bgOf(g.parentElement)).toFixed(2) : null }; },
    textContrast(needle) { const out = [];
      for (const el of document.querySelectorAll('body *')) {
        const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.includes(needle)).length;
        if (!own || !this.shown(el)) continue;
        const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
        const st = getComputedStyle(el); if (+st.opacity === 0) continue;
        const fg = this.parse(st.color); if (!fg) continue;
        const size = parseFloat(st.fontSize), weight = parseInt(st.fontWeight, 10) || 400;
        const need = (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3 : 4.5;
        out.push({ tag: el.tagName.toLowerCase(), cls: String(el.className || ''), got: +this.ratio(fg, this.bgOf(el)).toFixed(2), need });
      }
      return out; }
  };`;

async function chips(page) {
  const loc = page.locator('header button[aria-pressed]');
  const n = await loc.count();
  const out = [];
  for (let i = 0; i < n; i++) {
    const b = loc.nth(i);
    const snap = await b.ariaSnapshot();
    const name = (snap.match(/button "([^"]*)"/) || [, ''])[1];
    const text = await b.innerText();
    const box = await b.boundingBox();
    out.push({ i, name, num: (text.match(/\d+/) || [null])[0], visible: !!box && box.width > 0 && box.height > 0,
               pressed: await b.getAttribute('aria-pressed') });
  }
  return out;
}

async function run() {
  const [file, outdir, label, skill] = process.argv.slice(2);
  if (!file || !outdir || !label) { console.error('사용: node probe-ui.cjs <ui.html> <캡처 폴더> <이름> [SKILL.md]'); process.exit(2); }
  const abs = path.resolve(file);
  fs.mkdirSync(outdir, { recursive: true });
  const expr = skill ? section7Expr(skill) : null;
  const browser = await chromium.launch({ channel: 'chromium' });
  const verdicts = [];
  const ok = (key, pass, detail) => verdicts.push({ key, pass, detail });
  const glyphs = {};

  for (const [w, h, theme] of COMBOS) {
    const tag = `${w}-${theme}`;
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: theme });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error' && !/favicon\.ico/.test(m.text())) errors.push(m.text()); });
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    await page.goto('file://' + abs);
    await page.waitForTimeout(300);
    await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
    await page.waitForTimeout(600);
    await page.addScriptTag({ content: HELPERS });

    const base = await page.evaluate(() => {
      const P = window.__p;
      const rows = [...document.querySelectorAll('[data-ep]')];
      const byLabel = {}; P.LABELS.forEach(L => { byLabel[L] = 0; });
      const ambiguous = [];
      rows.forEach(r => { const L = P.rowLabel(r); if (L in byLabel) byLabel[L]++; else ambiguous.push(r.dataset.ep + '=' + L); });
      const glyphs = {};
      P.LABELS.forEach(L => { const r = rows.find(x => P.rowLabel(x) === L); glyphs[L] = r ? P.glyphInfo(r) : null; });
      return { ep: typeof EP === 'object' ? Object.keys(EP).length : -1, rows: rows.length, byLabel, ambiguous, glyphs };
    });
    const cs = await chips(page);
    const chipOf = {};
    for (const L of LABELS) chipOf[L] = cs.filter(c => c.name.includes(L));
    const chipGlyph = {};
    for (const L of LABELS) {
      if (chipOf[L].length !== 1) continue;
      chipGlyph[L] = await page.locator('header button[aria-pressed]').nth(chipOf[L][0].i).evaluate(b => window.__p.glyphInfo(b));
    }
    glyphs[tag] = { row: base.glyphs, chip: chipGlyph };

    ok(`${tag} rows-one-label`, base.ambiguous.length === 0 && base.rows === base.ep, `ep=${base.ep} rows=${base.rows} ambiguous=${base.ambiguous.join(',') || 0}`);
    for (const L of LABELS) {
      const c = chipOf[L];
      const one = c.length === 1 && c[0].visible;
      ok(`${tag} chip[${L}]`, one && Number(c[0].num) === base.byLabel[L],
         `chips=${c.length} visible=${one} num=${one ? c[0].num : '-'} rows=${base.byLabel[L]}`);
    }
    const sum = LABELS.reduce((a, L) => a + base.byLabel[L], 0);
    ok(`${tag} sum`, sum === base.ep && base.byLabel[UNJ] >= 1, `sum=${sum} ep=${base.ep} ${UNJ}=${base.byLabel[UNJ]}`);
    for (const L of LABELS) {
      const g = base.glyphs[L];
      if (L === UNJ) ok(`${tag} row-glyph-contrast[${L}]`, !!g && g.ratio >= 3, `ratio=${g ? g.ratio : '-'}`);
      const cg = chipGlyph[L];
      if (L === UNJ) ok(`${tag} chip-glyph-contrast[${L}]`, !!cg && cg.ratio >= 3, `ratio=${cg ? cg.ratio : '-'}`);
    }
    const others = LABELS.filter(L => L !== UNJ && base.glyphs[L]);
    const ug = base.glyphs[UNJ];
    ok(`${tag} row-glyph-distinct`, !!ug && others.every(L => base.glyphs[L].shape !== ug.shape && base.glyphs[L].color !== ug.color),
       `unj=${ug ? ug.color : '-'} vs ${others.map(L => L + ':' + base.glyphs[L].color).join(' ')}`);
    const cu = chipGlyph[UNJ];
    ok(`${tag} chip-glyph-distinct`, !!cu && LABELS.filter(L => L !== UNJ && chipGlyph[L]).every(L => chipGlyph[L].shape !== cu.shape),
       `chip shapes compared=${LABELS.filter(L => L !== UNJ && chipGlyph[L]).length}`);

    if (w === 375) {
      const toggle = page.locator('header button[aria-controls][aria-expanded]').first();
      if (await toggle.count()) { await toggle.click(); await page.waitForTimeout(500); }
      const vis = await page.evaluate(() => [...document.querySelectorAll('[data-ep]')].filter(e => window.__p.shown(e)).length);
      ok(`${tag} drawer-rows-visible`, vis === base.ep, `visible=${vis} ep=${base.ep}`);
      const tc = await page.evaluate(n => window.__p.textContrast(n), UNJ);
      ok(`${tag} text-contrast`, tc.every(x => x.got + 0.005 >= x.need), JSON.stringify(tc));
      await page.screenshot({ path: path.join(outdir, `${label}-${tag}.png`) });
    } else {
      if (expr) {
        const r = await page.evaluate(expr);
        const good = r && r.chips && r.rows && LABELS.every(L => r.chips[L] === base.byLabel[L] && r.rows[L] === base.byLabel[L]);
        ok(`${tag} sec7-expr`, !!good && r.ep === r.shown && r.under24 === 0, JSON.stringify(r));
      }
      await page.screenshot({ path: path.join(outdir, `${label}-${tag}.png`) });
      const chipU = chipOf[UNJ];
      if (chipU.length === 1) {
        const btn = page.locator('header button[aria-pressed]').nth(chipU[0].i);
        await btn.click(); await page.waitForTimeout(300);
        const f = await page.evaluate(() => { const P = window.__p;
          const vis = [...document.querySelectorAll('[data-ep]')].filter(e => P.shown(e));
          return { n: vis.length, allUnj: vis.every(e => P.rowLabel(e) === '판정 불가') }; });
        const pressed = await btn.getAttribute('aria-pressed');
        await btn.click(); await page.waitForTimeout(300);
        const back = await page.evaluate(() => [...document.querySelectorAll('[data-ep]')].filter(e => window.__p.shown(e)).length);
        ok(`${tag} filter`, f.n === base.byLabel[UNJ] && f.allUnj && pressed === 'true' && back === base.ep,
           `filtered=${f.n} allUnj=${f.allUnj} pressed=${pressed} back=${back}`);
      } else ok(`${tag} filter`, false, 'chip 없음');

      const unjIds = await page.evaluate(() => [...document.querySelectorAll('[data-ep]')].filter(e => window.__p.rowLabel(e) === '판정 불가').map(e => e.dataset.ep));
      let reasonOk = unjIds.length > 0, noFailTab = true;
      for (const id of unjIds) {
        await page.locator(`[data-ep="${id}"]`).first().click(); await page.waitForTimeout(300);
        const t = await page.evaluate(() => document.body.innerText);
        const line = t.split('\n').some(s => s.includes('(없음)') && s.includes('→ 판정 불가') && s.includes(' · '));
        const failTab = await page.getByRole('tab', { name: '실패 원인' }).count();
        reasonOk = reasonOk && line; noFailTab = noFailTab && failTab === 0;
      }
      ok(`${tag} unjudged-reason`, reasonOk && noFailTab, `endpoints=${unjIds.length} line=${reasonOk} failTab0=${noFailTab}`);
      if (unjIds.length) {
        await page.locator(`[data-ep="${unjIds[0]}"]`).first().click(); await page.waitForTimeout(300);
        const tc = await page.evaluate(n => window.__p.textContrast(n), UNJ);
        ok(`${tag} text-contrast`, tc.length > 0 && tc.every(x => x.got + 0.005 >= x.need), JSON.stringify(tc));
        await page.screenshot({ path: path.join(outdir, `${label}-${tag}-unjudged.png`) });
      }
      const failIds = await page.evaluate(() => [...document.querySelectorAll('[data-ep]')].filter(e => window.__p.rowLabel(e) === 'FAIL').map(e => e.dataset.ep));
      let failWithUnj = 0;
      for (const id of failIds) {
        await page.locator(`[data-ep="${id}"]`).first().click(); await page.waitForTimeout(300);
        const t = await page.evaluate(() => document.body.innerText);
        const failTab = await page.getByRole('tab', { name: '실패 원인' }).count();
        if (failTab > 0 && t.split('\n').some(s => s.includes('(없음)') && s.includes('→ 판정 불가'))) failWithUnj++;
      }
      console.log(`INFO ${label} ${tag} fail-with-unjudged=${failWithUnj} fail-rows=${failIds.length}`);
    }
    ok(`${tag} console-errors`, errors.length === 0, `errors=${errors.length} ${errors.slice(0, 3).join(' | ')}`);
    await ctx.close();
  }
  await browser.close();

  const themeDiff = LABELS.filter(L => glyphs['1280-light'].row[L] && glyphs['1280-dark'].row[L]);
  console.log(`INFO ${label} glyph-colors ` + themeDiff.map(L => `${L}:${glyphs['1280-light'].row[L].color}/${glyphs['1280-dark'].row[L].color}`).join(' '));
  let bad = 0;
  for (const v of verdicts) { if (!v.pass) bad++; console.log(`${v.pass ? 'OK' : 'NG'} ${label} ${v.key} — ${v.detail}`); }
  console.log(`VERDICT ${label} ${bad === 0 ? 'PASS' : 'FAIL'} ng=${bad} checks=${verdicts.length}`);
  process.exit(bad === 0 ? 0 : 1);
}

run().catch(e => { console.error('PROBE_ERROR ' + e.message); process.exit(2); });
