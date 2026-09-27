// 페이지마다 세 폭(320 · 375 · 1280) × 두 테마(light · dark)로 열어 가로 넘침 · 글 잘림 · 콘솔 오류를 센다.
// 사용: node layout.js <레포> <페이지>... (레포의 node_modules/playwright-core 를 쓴다)
// 출력: 칸마다 `<페이지> w=<폭> theme=<테마> overflow=<px> clipped=<수> errors=<수>` 한 줄, 끝 줄 `cells=<칸 수> bad=<나쁜 칸 수>`.
// 테마는 prefers-color-scheme 흉내 · localStorage dk-theme · html[data-theme] 셋을 모두 맞춘다 — 페이지마다 테마를 읽는 자리가 다르다.
// 글 잘림: 자기 글을 가진 요소 가운데 overflow 가 hidden · clip 이거나 text-overflow 가 ellipsis 인데 내용 폭이 상자 폭보다 1px 넘게 큰 것.
// 종료 코드: 나쁜 칸 0 이면 0, 있으면 1, 페이지를 못 열면 2.
const path = require('path');
const repo = process.argv[2];
const { chromium } = require(path.join(repo, 'node_modules', 'playwright-core'));
const pages = process.argv.slice(3);
(async () => {
  const browser = await chromium.launch();
  let cells = 0, bad = 0;
  for (const rel of pages) {
    for (const theme of ['light', 'dark']) {
      const ctx = await browser.newContext({ colorScheme: theme, viewport: { width: 1280, height: 900 } });
      await ctx.addInitScript(t => { try { localStorage.setItem('dk-theme', t); } catch (e) {} }, theme);
      const page = await ctx.newPage();
      const errors = [];
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      page.on('pageerror', e => errors.push(String(e)));
      try {
        await page.goto('file://' + path.resolve(repo, rel), { waitUntil: 'load' });
      } catch (e) {
        console.log(`OPEN_FAIL ${rel} ${e}`); process.exitCode = 2; await ctx.close(); continue;
      }
      await page.evaluate(t => { document.documentElement.dataset.theme = t; }, theme);
      for (const w of [320, 375, 1280]) {
        await page.setViewportSize({ width: w, height: 900 });
        await page.waitForTimeout(300);
        const r = await page.evaluate(() => {
          const d = document.documentElement;
          const overflow = Math.max(d.scrollWidth, document.body.scrollWidth) - d.clientWidth;
          let clipped = 0;
          for (const el of document.body.querySelectorAll('*')) {
            const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
            if (!own) continue;
            const s = getComputedStyle(el);
            if (s.display === 'none' || s.visibility === 'hidden') continue;
            const cut = ['hidden', 'clip'].includes(s.overflowX) || s.textOverflow === 'ellipsis';
            if (cut && el.scrollWidth - el.clientWidth > 1) clipped++;
          }
          return { overflow, clipped };
        });
        cells++;
        const isBad = r.overflow > 0 || r.clipped > 0 || errors.length > 0;
        if (isBad) bad++;
        console.log(`${rel} w=${w} theme=${theme} overflow=${r.overflow} clipped=${r.clipped} errors=${errors.length}${isBad ? ' BAD' : ''}`);
      }
      await ctx.close();
    }
  }
  await browser.close();
  console.log(`cells=${cells} bad=${bad}`);
  if (!process.exitCode) process.exitCode = bad ? 1 : 0;
})();
