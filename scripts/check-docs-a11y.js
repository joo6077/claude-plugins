#!/usr/bin/env node
/**
 * check-docs-a11y.js — docs/ HTML 페이지의 접근성을 실제 브라우저로 측정한다.
 *
 * 재는 것: 가로 오버플로(320/375/768/1280px) · 콘솔 에러 · WCAG AA 대비 · 터치 타깃 44x44.
 *
 * 왜 이게 필요한가 (실측 2026-09-05): `design-kit/evals/visuals.spec.js` 는 페이지의
 * **텍스트 대비를 재지 않는다** — color-palette.html 의 대비 체커 위젯이 렌더되는지만 본다.
 * 그래서 CI 가 계속 green 인 채로 172 페이지 중 150 개가 AA 미달이었다. 실패 1088 건 중
 * 836 건(77%)이 `--text3:#7A6F64` 한 토큰이었다.
 *
 * 측정 범위에 대한 주의 세 가지. 전부 실제로 잘못 재서 배운 것이다.
 *
 *  1. 선택자 몇 개만 재면 통과가 나온다. `.desc`/`.card-source`/`.section-label` 3 종만 재던
 *     판에서는 minContrast 4.64 로 PASS 였지만 `.caption` 이 3.95 였다. 그래서 여기서는
 *     **직접 자식 텍스트를 가진 모든 요소**를 훑고 유효 배경을 조상으로 거슬러 올라가 계산한다.
 *  2. 다크 전용 페이지에 data-theme="light" 를 걸면 그냥 다크가 렌더된다. 그걸 라이트로 세면
 *     같은 실패를 두 번 센다 (172 중 146 이 다크 전용이었다). 라이트로 칠한 모양이 다를 때만 잰다.
 *  3. 테마 토글이 없는 페이지를 0x0 으로 재고 44px 미만이라 실패시키면 고칠 수도 없는 조건으로
 *     전 페이지가 FAIL 이 된다. 존재할 때만 잰다.
 *
 * 디자인 스타일 표본(뉴모피즘·글래스모피즘 등)은 저대비가 그 스타일의 정의다. AA 로 끌어올리면
 * 표본이 아니게 되므로 `data-contrast-exempt="specimen"` 으로 **명시 면제**하고 `specimen=N`
 * 으로 따로 센다. 조용히 넘기지 않는 것이 요점이다.
 *
 * Usage:
 *   node scripts/check-docs-a11y.js docs/api-kit/*.html
 *   node scripts/check-docs-a11y.js            # docs 전체
 *   VERBOSE=1 node scripts/check-docs-a11y.js <files>   # 면제 항목까지 출력
 *
 * exit 0 = 전부 통과, 1 = 하나라도 실패. 종료 코드 의미: harness/evals/gate-exit-codes.md
 */
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

// 인자가 없으면 docs/ 전체를 대상으로 한다 (CI 기본 동작).
// 한 단계만 훑으면 docs/design-kit/examples/ 같은 하위 디렉토리를 통째로 놓친다 —
// `docs/*/*.html` 글롭으로 세던 초기 집계가 실제로 1 페이지를 빠뜨렸다.
function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(d => {
    const full = path.join(dir, d.name);
    if (d.isDirectory()) return walk(full);
    return d.name.endsWith('.html') ? [full] : [];
  });
}
const files = process.argv.slice(2).length ? process.argv.slice(2) : walk('docs').sort();
const VERBOSE = process.env.VERBOSE === '1';

(async () => {
  const b = await chromium.launch();
  let fails = 0;
  for (const f of files) {
    const ctx = await b.newContext({ viewport: { width: 375, height: 812 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('console', m => m.type() === 'error' && errs.push(m.text()));
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + path.resolve(f));

    const of = {};
    for (const w of [320, 375, 768, 1280]) {
      await p.setViewportSize({ width: w, height: 900 });
      of[w] = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    }

    const sweep = async (theme) => {
      await p.evaluate(t => { document.documentElement.dataset.theme = t; }, theme);
      // body 배경에 0.25s transition 이 걸려 있다. 기다리지 않으면 보간 중인 색을 읽어
      // 다크 테마인데 라이트 배경 대비가 나온다 (실측: 2.51 vs 실제 7.08).
      await p.waitForTimeout(500);
      // 0.5s 넘는 전환도 있다 — 테마를 바꾼 뒤 도는 전환이 끝날 때까지 기다린다 (무한 반복 애니메이션은 뺀다)
      await p.evaluate(() => Promise.all(document.getAnimations()
        .filter(a => a.effect && a.effect.getComputedTiming().iterations !== Infinity)
        .map(a => a.finished.catch(() => null))));
      return await p.evaluate(() => {
        // color-mix() 결과는 color(srgb 0~1 …) 로 나온다 — 0~255 로 읽으면 밝은 색이 검정이 된다
        const parse = c => { const m = (c || '').match(/[\d.]+/g); if (!m) return null;
          const v = m.map(Number); return /^color\(srgb /.test(c) ? [v[0] * 255, v[1] * 255, v[2] * 255, ...v.slice(3)] : v; };
        const lum = rgb => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
          return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2]); };
        const ratio = (a, c) => { const [x, y] = [lum(a), lum(c)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); };
        // 유효 배경 — 투명하면 조상으로 올라간다
        const bgOf = el => {
          for (let n = el; n; n = n.parentElement) {
            const c = parse(getComputedStyle(n).backgroundColor);
            if (c && (c.length < 4 || c[3] > 0.5)) return c;
          }
          return parse(getComputedStyle(document.body).backgroundColor) || [255, 255, 255];
        };
        const out = [];
        for (const el of document.querySelectorAll('body *')) {
          // 직접 자식 텍스트가 있는 요소만 (컨테이너 중복 제외)
          const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).length;
          if (!own) continue;
          const r = el.getBoundingClientRect();
          if (r.width < 2 || r.height < 2) continue;
          const st = getComputedStyle(el);
          if (st.visibility === 'hidden' || st.display === 'none' || +st.opacity === 0) continue;
          // gradient 로 칠한 텍스트(-webkit-text-fill-color:transparent)는 색 판정 대상이 아니다
          if (st.webkitTextFillColor === 'rgba(0, 0, 0, 0)') continue;
          const fg = parse(st.color);
          if (!fg || (fg.length > 3 && fg[3] < 0.5)) continue;
          const size = parseFloat(st.fontSize);
          const weight = parseInt(st.fontWeight, 10) || 400;
          // WCAG AA: 큰 텍스트(24px 이상, 또는 18.66px 이상 bold)는 3:1
          const large = size >= 24 || (size >= 18.66 && weight >= 700);
          const need = large ? 3 : 4.5;
          const got = ratio(fg, bgOf(el));
          if (got + 0.005 < need) {
            // 디자인 스타일 표본(뉴모피즘·글래스모피즘 등)은 저대비가 그 스타일의 정의다.
            // AA 로 끌어올리면 표본이 아니게 된다. 다만 조용히 넘기지 않고 따로 센다 —
            // 면제하려면 HTML 에 data-contrast-exempt="specimen" 을 명시해야 한다.
            const exempt = el.closest('[data-contrast-exempt]');
            const rec = { sel: el.className || el.tagName.toLowerCase(), color: st.color,
                          size: Math.round(size), got: +got.toFixed(2), need };
            if (exempt) { rec.exempt = exempt.getAttribute('data-contrast-exempt') || 'yes'; }
            out.push(rec);
          }
        }
        // 같은 클래스는 1 건만
        const seen = new Set();
        return out.filter(o => { const k = o.sel + o.color; if (seen.has(k)) return false; seen.add(k); return true; });
      });
    };

    // 라이트 테마 규칙이 없는 페이지에 data-theme="light" 를 걸면 그냥 다크가 그대로 렌더된다.
    // 그걸 라이트로 세면 같은 실패를 두 번 세게 된다 (실측: 172 페이지 중 146 개가 다크 전용).
    // 규칙 목록으로 찾지 않는다 — file:// 로 연 쪽은 링크한 공통 파일(docs/assets/site.css)의 cssRules 를
    // 읽을 수 없어(SecurityError) 공통 파일이 주는 밝은 테마를 못 본다. 두 테마로 칠한 모양을 맞대 본다.
    const look = () => p.evaluate(() => [document.documentElement, document.body]
      .map(el => getComputedStyle(el).backgroundColor + getComputedStyle(el).color).join('|'));
    const dark = await sweep('dark');
    const darkLook = await look();
    const lightRun = await sweep('light');
    const hasLight = (await look()) !== darkLook;
    const light = hasLight ? lightRun : [];
    // 테마 토글이 없는 페이지가 172 중 147 이다. 없는 요소를 0x0 으로 재고 44px 미만이라
    // 실패시키면, 고치지도 못할 조건으로 전 페이지가 FAIL 이 된다 (실측: text3 를 고쳤는데도
    // 22/172 그대로였고 원인이 이것이었다). 존재할 때만 잰다.
    // 단추 id 는 쪽마다 둘이다 — themeToggle 쪽을 안 보면 44 미만 단추가 btn=none 으로 통과한다 (2026-09-28 실측 63x33)
    const btn = await p.evaluate(() => { const e = document.getElementById('theme-btn') || document.getElementById('themeToggle');
      if (!e) return null;
      const r = e.getBoundingClientRect();
      return { w: Math.round(r.width), h: Math.round(r.height) }; });

    const all = [...dark, ...light];
    const bad = all.filter(o => !o.exempt).length;
    const exempt = all.length - bad;
    const btnOk = !btn || (btn.h >= 44 && btn.w >= 44);
    const ok = of[320] <= 2 && of[375] <= 2 && of[768] <= 2 && of[1280] <= 2 && errs.length === 0 && bad === 0 && btnOk;
    if (!ok) fails++;
    console.log(`${ok ? 'OK  ' : 'FAIL'} ${path.basename(f).padEnd(42)} of=${of[320]}/${of[375]}/${of[768]}/${of[1280]} err=${errs.length} contrastFail=${bad}${exempt ? ' specimen=' + exempt : ''} btn=${btn ? btn.w + 'x' + btn.h : 'none'} theme=${hasLight ? 'both' : 'dark-only'}`);
    errs.slice(0, 3).forEach(e => console.log('        err: ' + e.slice(0, 160)));
    if (bad || VERBOSE) {
      dark.filter(o => VERBOSE || !o.exempt).forEach(o => console.log(`        dark  ${o.got} < ${o.need}  ${o.color} ${o.size}px  .${o.sel}${o.exempt ? '  [면제:' + o.exempt + ']' : ''}`));
      light.filter(o => VERBOSE || !o.exempt).forEach(o => console.log(`        light ${o.got} < ${o.need}  ${o.color} ${o.size}px  .${o.sel}${o.exempt ? '  [면제:' + o.exempt + ']' : ''}`));
    }
    await ctx.close();
  }
  await b.close();
  console.log(`\n${files.length - fails}/${files.length} PASS`);
  process.exit(fails ? 1 : 0);
})();
