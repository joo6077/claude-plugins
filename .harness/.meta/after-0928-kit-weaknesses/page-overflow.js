// 문서 쪽 가로 넘침 재기. 쓰임: node page-overflow.js <레포 뿌리> <html 경로>...
// 폭 320 · 375 · 1280 마다 문서 전체 scrollWidth - clientWidth 를 찍는다. 0 이 아니면 넘침이다.
// 종료 코드: 0 넘침 0 · 1 넘침 있음 · 2 브라우저를 못 띄움
const path = require('path');
const root = process.argv[2];
const { chromium } = require(path.join(root, 'node_modules', 'playwright'));
(async () => {
  let browser;
  try { browser = await chromium.launch({ channel: 'chromium' }); } catch (e) {
    try { browser = await chromium.launch(); } catch (e2) { console.log('STOP 브라우저 실행 실패 ' + e2.message); process.exit(2); }
  }
  let bad = 0, n = 0;
  for (const rel of process.argv.slice(3)) {
    for (const width of [320, 375, 1280]) {
      const page = await browser.newPage({ viewport: { width, height: 800 } });
      await page.goto('file://' + path.resolve(root, rel));
      const over = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      n += 1; if (over > 0) bad += 1;
      console.log(`${rel} ${width} over=${over}`);
      await page.close();
    }
  }
  await browser.close();
  console.log(`OVERFLOW checked=${n} bad=${bad}`);
  process.exit(bad ? 1 : 0);
})();
