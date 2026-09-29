// node overflow.mjs <repo> : 3 pages x 3 widths, prints "page width overflowPx" and total cases
import { chromium } from 'playwright';
const repo = process.argv[2];
const pages = ['docs/harness/contract-schema.html', 'docs/harness/qa-evaluation-guide.html', 'docs/harness/contract-design-guide.html'];
const b = await chromium.launch();
let n = 0, bad = 0;
for (const p of pages) for (const w of [320, 375, 1280]) {
  const pg = await b.newPage({ viewport: { width: w, height: 800 } });
  await pg.goto('file://' + repo + '/' + p);
  const o = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  n++; if (o > 0) bad++; console.log(p, w, o); await pg.close();
}
await b.close(); console.log(`cases=${n} overflow=${bad}`);
