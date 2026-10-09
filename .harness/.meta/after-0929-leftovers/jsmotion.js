// 계약 after-0929-leftovers 스크립트 움직임 측정. 레포 맨 위 폴더에서 부른다.
//   node jsmotion.js <reduce|no-preference>
// 표본마다 한 줄: 누른 뒤 60 · 150 · 300 · 450 · 600 · 800 · 1000 · 1200ms 에 잰 값과, 첫 값 뒤에 값이 바뀐 횟수(changes).
// 환경 변수 JSM_ROOT 를 주면 쪽을 그 폴더 아래에서 연다 (대조용 사본).
// 종료 코드: 0 다 잼 · 2 잴 수 없음(브라우저 오류 · 요소 없음). 판정은 measure.py 가 한다.
const path = require('path');
const { chromium } = require(path.join(process.cwd(), 'node_modules', 'playwright'));

const TARGETS = [
  { name: 'spring', page: 'docs/design-kit/animation.html', watch: '#springBall', prop: 'left',
    act: (p) => p.click('button[onclick="playSpring()"]') },
  { name: 'flash', page: 'docs/design-kit/animation.html', watch: '#flashBox', prop: 'opacity',
    act: (p) => p.evaluate(() => {
      const s = document.getElementById('flashSlider');
      s.value = '2';
      s.dispatchEvent(new Event('input', { bubbles: true }));
    }) },
  { name: 'progress', page: 'docs/design-kit/data-display.html', watch: '#progressBar', prop: 'width',
    act: (p) => p.click(`button[onclick="switchLoadingState('progress',this)"]`) },
];
const AT = [60, 150, 300, 450, 600, 800, 1000, 1200];

(async () => {
  const motion = process.argv[2];
  if (motion !== 'reduce' && motion !== 'no-preference') {
    console.error('사용: node jsmotion.js <reduce|no-preference>');
    process.exit(2);
  }
  const browser = await chromium.launch();
  try {
    for (const t of TARGETS) {
      const ctx = await browser.newContext({ reducedMotion: motion, viewport: { width: 1280, height: 900 } });
      const p = await ctx.newPage();
      await p.goto('file://' + path.resolve(process.env.JSM_ROOT || '.', t.page));
      await p.waitForTimeout(300);
      if (!(await p.$(t.watch))) throw new Error(`${t.page} 에 ${t.watch} 없음`);
      await t.act(p);
      const start = Date.now();
      const values = [];
      for (const ms of AT) {
        const wait = ms - (Date.now() - start);
        if (wait > 0) await p.waitForTimeout(wait);
        values.push(await p.$eval(t.watch, (el, prop) => el.style[prop], t.prop));
      }
      const changes = values.slice(1).filter((v, i) => v !== values[i]).length;
      console.log(`${t.name}\t${t.page}\tmotion=${motion}\tvalues=${JSON.stringify(values)}\tchanges=${changes}`);
      await ctx.close();
    }
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(2); });
