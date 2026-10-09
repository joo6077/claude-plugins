// 문서 쪽 재기. 쓰임: node page-check.js <레포 뿌리> <html 경로>...
// 폭 320 · 375 · 1280 마다 가로 넘침(scrollWidth - clientWidth)과 페이지 오류(pageerror) 수를 찍는다.
// 쪽마다 <link rel="stylesheet"> 수와 공통 CSS(../assets/site.css) 링크 여부도 찍는다.
// 마지막 줄: PAGES checked=<폭 x 쪽> over=<넘친 수> errors=<오류 수> css_bad=<공통 CSS 링크가 정확히 하나가 아닌 쪽 수>
// 종료 코드: 0 전부 0 · 1 하나라도 있음 · 2 브라우저를 못 띄움
// playwright 는 NODE_MODS(기본: 본 체크아웃 node_modules)에서 읽는다.
const path = require('path');
const fs = require('fs');
const root = process.argv[2];
const mods = process.env.NODE_MODS || '/Users/jackson/Hub/10_Dev/claude-plugins/node_modules';
const { chromium } = require(path.join(mods, 'playwright'));
(async () => {
  let browser;
  try { browser = await chromium.launch({ channel: 'chromium' }); } catch (e) {
    try { browser = await chromium.launch(); } catch (e2) { console.log('STOP 브라우저 실행 실패 ' + e2.message); process.exit(2); }
  }
  let over = 0, errs = 0, n = 0, cssBad = 0;
  for (const rel of process.argv.slice(3)) {
    const html = fs.readFileSync(path.resolve(root, rel), 'utf8');
    const links = (html.match(/<link[^>]+rel=["']stylesheet["'][^>]*>/g) || []);
    const site = links.filter(l => /\.\.\/assets\/site\.css/.test(l)).length;
    if (site !== 1) cssBad += 1;
    console.log(`${rel} stylesheet_links=${links.length} site_css=${site}`);
    for (const width of [320, 375, 1280]) {
      const page = await browser.newPage({ viewport: { width, height: 800 } });
      const pe = [];
      page.on('pageerror', e => pe.push(e.message));
      await page.goto('file://' + path.resolve(root, rel));
      await page.waitForLoadState('load');
      const o = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      n += 1; if (o > 0) over += 1; errs += pe.length;
      console.log(`${rel} ${width} over=${o} pageerror=${pe.length}`);
      await page.close();
    }
  }
  await browser.close();
  console.log(`PAGES checked=${n} over=${over} errors=${errs} css_bad=${cssBad}`);
  process.exit(over || errs || cssBad ? 1 : 0);
})();
