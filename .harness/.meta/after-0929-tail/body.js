// 계약 after-0929-tail 본문 배경 전환 측정. 레포 맨 위 폴더에서 부른다.
//   node body.js list <쪽...>                        움직임 허용 설정에서 본문(body) 배경에 0 초 넘는 전환이 걸린 쪽만 한 줄씩
//   node body.js click <reduce|no-preference> <쪽...>  어두운 설정으로 열어 테마 단추를 누르고 본문 배경을 잰다 — 쪽마다 한 줄
// click 줄: changed(누르기 전과 800ms 뒤가 다름) · settled(누른 직후 같은 작업 안에서 읽은 값이 800ms 뒤 값과 같음) ·
//           distinct(누른 직후 · 16 · 50 · 100 · 200 · 400 · 800ms 에 읽은 값의 서로 다른 수)
// 종료 코드: 0 다 잼 · 2 잴 수 없음(브라우저 오류). 판정은 measure.py 가 한다.
const path = require('path');
const { chromium } = require(path.join(process.cwd(), 'node_modules', 'playwright'));

const url = (f) => 'file://' + path.resolve(f);
const BTN = '#theme-btn, #themeToggle, .dk-theme-btn';
const TIMES = [16, 50, 100, 200, 400, 800];

async function list(browser, pages) {
  const ctx = await browser.newContext({ reducedMotion: 'no-preference', colorScheme: 'dark' });
  for (const f of pages) {
    const p = await ctx.newPage();
    await p.goto(url(f));
    const t = await p.evaluate(() => {
      const cs = getComputedStyle(document.body);
      const props = cs.transitionProperty.split(',').map((s) => s.trim());
      const durs = cs.transitionDuration.split(',').map((s) => parseFloat(s));
      return props.some((prop, i) => /^(all|background|background-color)$/.test(prop) && (durs[i % durs.length] || 0) > 0)
        ? `${cs.transitionProperty}|${cs.transitionDuration}` : '';
    });
    if (t) console.log(`${f} body_transition=${t.replace(/ /g, '')}`);
    await p.close();
  }
  await ctx.close();
}

async function click(browser, motion, pages) {
  for (const f of pages) {
    const ctx = await browser.newContext({ reducedMotion: motion, colorScheme: 'dark' });
    const p = await ctx.newPage();
    await p.goto(url(f));
    const before = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
    const found = await p.$(BTN);
    if (!found) {
      console.log(`${f} btn=none`);
      await ctx.close();
      continue;
    }
    // 누르기와 읽기를 한 작업 안에서 한다 — 사이에 그림이 한 번이라도 그려지면 0.01ms 전환은 이미 끝나 있다
    const now = await p.evaluate((sel) => {
      document.querySelector(sel).click();
      return getComputedStyle(document.body).backgroundColor;
    }, BTN);
    const seen = [now];
    let waited = 0;
    for (const t of TIMES) {
      await p.waitForTimeout(t - waited);
      waited = t;
      seen.push(await p.evaluate(() => getComputedStyle(document.body).backgroundColor));
    }
    const last = seen[seen.length - 1];
    console.log(`${f} btn=1 changed=${before !== last ? 1 : 0} settled=${now === last ? 1 : 0} distinct=${new Set(seen).size}`);
    await ctx.close();
  }
}

(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch();
  try {
    if (mode === 'list') await list(browser, rest);
    else if (mode === 'click' && ['reduce', 'no-preference'].includes(rest[0])) await click(browser, rest[0], rest.slice(1));
    else { console.error('사용: node body.js list <쪽...> | click <reduce|no-preference> <쪽...>'); process.exitCode = 2; }
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(2); });
