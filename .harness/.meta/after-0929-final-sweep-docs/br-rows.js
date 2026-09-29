// 개정 AM-01 (구조-03 두 쪽) 브라우저 측정. 레포 맨 위 폴더에서 부른다.
//   node br-rows.js <dark|light> <쪽...>   쪽마다 JSON 한 줄 — body 색 둘과 글자를 직접 가진 요소마다 [태그, 글자색, 배경색, 글자]
// 테마 고정 · 기다림 · 요소 고르기는 br.js paint 와 같다. 글자를 더 실어 새로 더한 요소를 가려낸다.
// 종료 코드: 0 다 잼 · 2 잴 수 없음(브라우저 오류). 판정은 keep-colors-narrow.py 가 한다.
const path = require('path');
const { chromium } = require(path.join(process.cwd(), 'node_modules', 'playwright'));

const url = (file) => 'file://' + path.resolve(file);
const BTN = '#theme-btn, #themeToggle';

async function rowsLine(browser, theme, file) {
  const ctx = await browser.newContext({ colorScheme: theme, reducedMotion: 'reduce', viewport: { width: 1280, height: 900 } });
  await ctx.addInitScript((value) => { try { localStorage.setItem('dk-theme', value); } catch (err) { /* 저장 막힘 */ } }, theme);
  const page = await ctx.newPage();
  await page.goto(url(file));
  await page.evaluate((value) => { document.documentElement.dataset.theme = value; }, theme);
  await page.waitForTimeout(300);
  // br.js 는 넘침을 재느라 폭을 320 · 375 · 1280 으로 돌린 뒤 색을 읽는다 — 같은 상태에서 읽으려고 똑같이 돌린다
  for (const width of [320, 375, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    await page.waitForTimeout(200);
  }
  const result = await page.evaluate((sel) => {
    const body = [getComputedStyle(document.body).backgroundColor, getComputedStyle(document.body).color];
    const rows = [];
    for (const el of document.body.querySelectorAll('*')) {
      if (el.closest(sel) || el.closest('script,style,noscript,template')) continue;
      const own = [...el.childNodes].filter((node) => node.nodeType === 3 && node.textContent.trim());
      if (!own.length) continue;
      const cs = getComputedStyle(el);
      const words = own.map((node) => node.textContent).join(' ').replace(/\s+/g, ' ').trim().slice(0, 160);
      rows.push([el.tagName, cs.color, cs.backgroundColor, words]);
    }
    return { body, rows };
  }, BTN);
  await ctx.close();
  return JSON.stringify({ file, theme, ...result });
}

(async () => {
  const [theme, ...files] = process.argv.slice(2);
  if (!['dark', 'light'].includes(theme)) {
    console.error('사용: node br-rows.js <dark|light> <쪽...>');
    process.exit(2);
  }
  const browser = await chromium.launch();
  try {
    for (const file of files) console.log(await rowsLine(browser, theme, file));
  } finally {
    await browser.close();
  }
})().catch((err) => { console.error(err); process.exit(2); });
