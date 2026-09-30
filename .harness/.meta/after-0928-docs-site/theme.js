// 계약 after-0928-docs-site 측정 — 테마 규약(AR-02)과 카드 들뜸(ER-02)을 실제 브라우저로 잰다.
// 사용: node theme.js theme <쪽...> | node theme.js hover
// theme 줄: <쪽> first_light=<light|dark> first_dark=<..> click=<..> stored=<..> reload=<..> bg_differs=<0|1>
const path = require('path');
const { chromium } = require(path.join(process.cwd(), 'node_modules', 'playwright'));

const url = (f) => 'file://' + path.resolve(f);

async function themeLine(browser, f) {
  const first = async (scheme) => {
    const ctx = await browser.newContext({ colorScheme: scheme });
    const p = await ctx.newPage();
    await p.goto(url(f));
    const t = await p.evaluate(() => document.documentElement.getAttribute('data-theme'));
    await ctx.close();
    return t;
  };
  const firstLight = await first('light');
  const firstDark = await first('dark');
  const ctx = await browser.newContext({ colorScheme: 'dark' });
  const p = await ctx.newPage();
  await p.goto(url(f));
  const bg = () => p.evaluate(() => getComputedStyle(document.body).backgroundColor);
  const bgBefore = await bg();
  const btn = await p.$('#theme-btn');
  let click = 'none', stored = 'none', reload = 'none', bgAfter = bgBefore;
  if (btn) {
    await btn.click();
    click = await p.evaluate(() => document.documentElement.getAttribute('data-theme'));
    stored = await p.evaluate(() => localStorage.getItem('dk-theme'));
    bgAfter = await bg();
    await p.reload();
    reload = await p.evaluate(() => document.documentElement.getAttribute('data-theme'));
  }
  await ctx.close();
  return `${f} first_light=${firstLight} first_dark=${firstDark} click=${click} stored=${stored} reload=${reload} bg_differs=${bgBefore !== bgAfter ? 1 : 0}`;
}

async function hoverLine(browser, motion) {
  const f = 'docs/design-kit/design-test.html';
  const ctx = await browser.newContext({ reducedMotion: motion });
  const p = await ctx.newPage();
  await p.goto(url(f));
  const card = await p.$('.feat-card');
  if (!card) { await ctx.close(); return `${motion} cards=0 transform=none`; }
  await card.scrollIntoViewIfNeeded();
  await card.hover();
  await p.waitForTimeout(400);
  const t = await card.evaluate((e) => getComputedStyle(e).transform);
  const n = await p.$$eval('.feat-card', (a) => a.length);
  await ctx.close();
  return `${motion} cards=${n} transform=${t}`;
}

(async () => {
  const [mode, ...files] = process.argv.slice(2);
  const browser = await chromium.launch();
  try {
    if (mode === 'theme') {
      for (const f of files) console.log(await themeLine(browser, f));
    } else if (mode === 'hover') {
      console.log(await hoverLine(browser, 'reduce'));
      console.log(await hoverLine(browser, 'no-preference'));
    } else {
      console.error('사용: node theme.js theme <쪽...> | node theme.js hover');
      process.exitCode = 2;
    }
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(2); });
