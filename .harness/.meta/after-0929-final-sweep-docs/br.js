// 계약 after-0929-final-sweep-docs 브라우저 측정. 레포 맨 위 폴더에서 부른다.
//   node br.js theme <쪽...>                  테마 단추 규약 — 쪽마다 한 줄
//   node br.js paint <dark|light> <쪽...>     그 테마로 고정해 색 지문 · 넘침(320/375/1280) — 쪽마다 한 줄
//   node br.js motion <reduce|no-preference> <쪽...>   움직임 — 쪽마다 한 줄
// 쪽 경로는 그대로 file:// 로 연다 (시작 판을 풀어 둔 폴더의 쪽도 줄 수 있다).
// 종료 코드: 0 다 잼 · 2 잴 수 없음(브라우저 오류). 판정은 measure.py 가 한다.
const path = require('path');
const crypto = require('crypto');
const { chromium } = require(path.join(process.cwd(), 'node_modules', 'playwright'));

const url = (f) => 'file://' + path.resolve(f);
const BTN = '#theme-btn, #themeToggle';

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
  const ctx = await browser.newContext({ colorScheme: 'dark', viewport: { width: 375, height: 812 } });
  const p = await ctx.newPage();
  await p.goto(url(f));
  const bg = () => p.evaluate(() => getComputedStyle(document.body).backgroundColor);
  const bgBefore = await bg();
  const btn = await p.$(BTN);
  let click = 'none', stored = 'none', reload = 'none', bgAfter = bgBefore, size = 'none';
  if (btn) {
    const r = await btn.boundingBox();
    size = r ? `${Math.round(r.width)}x${Math.round(r.height)}` : 'hidden';
    await btn.click();
    click = await p.evaluate(() => document.documentElement.getAttribute('data-theme'));
    stored = await p.evaluate(() => localStorage.getItem('dk-theme'));
    bgAfter = await bg();
    await p.reload();
    reload = await p.evaluate(() => document.documentElement.getAttribute('data-theme'));
  }
  await ctx.close();
  return `${f} first_light=${firstLight} first_dark=${firstDark} click=${click} stored=${stored} reload=${reload} bg_differs=${bgBefore !== bgAfter ? 1 : 0} btn=${size}`;
}

// 테마를 고정한다: 브라우저 색 설정 · 저장값 · data-theme 셋 다 같은 값으로 둔다 (시작 판 · 새 판 같은 절차)
async function paintLine(browser, theme, f) {
  // 테마를 바꾸면 색 전환 · 애니메이션이 도는 중에 잴 수 있다 — 움직임 줄이기 설정으로 열어 재는 때마다 같은 값을 얻는다
  const ctx = await browser.newContext({ colorScheme: theme, reducedMotion: 'reduce', viewport: { width: 1280, height: 900 } });
  await ctx.addInitScript((t) => { try { localStorage.setItem('dk-theme', t); } catch (e) { /* 저장 막힘 */ } }, theme);
  const p = await ctx.newPage();
  await p.goto(url(f));
  await p.evaluate((t) => { document.documentElement.dataset.theme = t; }, theme);
  await p.waitForTimeout(300);
  const of = [];
  for (const w of [320, 375, 1280]) {
    await p.setViewportSize({ width: w, height: 900 });
    await p.waitForTimeout(200); // 폭을 바꾼 바로 뒤에는 쪽 스크립트가 줄을 다시 잡기 전이라 넘침이 잠깐 보인다
    of.push(await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth));
  }
  // 색 지문: 글자를 직접 가진 요소의 글자색 · 배경색 + body 배경. 테마 단추 안은 뺀다 (새로 붙는 요소라서)
  const rows = await p.evaluate((sel) => {
    const out = [getComputedStyle(document.body).backgroundColor, getComputedStyle(document.body).color];
    for (const el of document.body.querySelectorAll('*')) {
      if (el.closest(sel) || el.closest('script,style,noscript,template')) continue;
      const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
      if (!own) continue;
      const cs = getComputedStyle(el);
      out.push(`${el.tagName}|${cs.color}|${cs.backgroundColor}`);
    }
    return out;
  }, BTN);
  const fp = crypto.createHash('sha256').update(rows.join('\n')).digest('hex').slice(0, 16);
  await ctx.close();
  return `${f} theme=${theme} of=${of.join('/')} n=${rows.length} fp=${fp}`;
}

async function motionLine(browser, motion, f) {
  const ctx = await browser.newContext({ reducedMotion: motion, viewport: { width: 1280, height: 900 } });
  const p = await ctx.newPage();
  await p.goto(url(f));
  await p.waitForTimeout(500);
  const stat = await p.evaluate(() => {
    const sec = (v) => Math.max(0, ...v.split(',').map((s) => parseFloat(s) * (s.trim().endsWith('ms') ? 0.001 : 1)));
    let tmax = 0, amax = 0;
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      tmax = Math.max(tmax, sec(cs.transitionDuration));
      if (cs.animationName !== 'none') amax = Math.max(amax, sec(cs.animationDuration));
    }
    // 재는 때에 따라 갈리지 않게 상태(playState) 대신 길이로 센다 — 지연 중인 0.01ms 애니메이션은 움직이지 않는다
    const anims = document.getAnimations();
    const moving = anims.filter((a) => a.effect && a.effect.getComputedTiming().activeDuration > 0.02).length;
    const endless = anims.filter((a) => a.effect && a.effect.getComputedTiming().iterations === Infinity).length;
    // 지금 적용되는 규칙 가운데 :hover 에서 transform 류를 주는 것 — 선택자에서 :hover 를 뺀 대상 첫 요소
    const sels = [];
    const walk = (rules) => {
      for (const r of rules) {
        if (r.media && r.cssRules) { if (matchMedia(r.media.mediaText).matches) walk(r.cssRules); continue; }
        if (r.cssRules && !r.selectorText) { walk(r.cssRules); continue; }
        if (!r.selectorText || !r.style) continue;
        const moves = ['transform', 'translate', 'scale', 'rotate'].some((k) => r.style.getPropertyValue(k));
        if (!moves) continue;
        for (const part of r.selectorText.split(',')) {
          if (!part.includes(':hover')) continue;
          const pm = part.match(/::?(before|after)\s*$/);
          const base = part.replace(/::?(before|after)\s*$/, '').replace(/:hover/g, '').trim();
          if (base) sels.push([base, pm ? '::' + pm[1] : null]);
        }
      }
    };
    for (const ss of document.styleSheets) { try { walk(ss.cssRules); } catch (e) { /* 읽기 막힘 */ } }
    return { tmax, amax, moving, endless, sels, sb: getComputedStyle(document.documentElement).scrollBehavior };
  });
  let lifts = 0, tried = 0;
  const seen = new Set();
  for (const [base, pseudo] of stat.sels) {
    const key = base + (pseudo || '');
    if (seen.has(key)) continue;
    seen.add(key);
    let el;
    try { el = await p.$(base); } catch (e) { continue; }
    if (!el || !(await el.isVisible())) continue;
    const tf = () => el.evaluate((e, ps) => getComputedStyle(e, ps).transform + '|' + getComputedStyle(e, ps).translate + '|' + getComputedStyle(e, ps).scale + '|' + getComputedStyle(e, ps).rotate, pseudo);
    try {
      await p.mouse.move(0, 0);
      await el.scrollIntoViewIfNeeded();
      const before = await tf();
      await el.hover({ timeout: 2000 });
      await p.waitForTimeout(120);
      const after = await tf();
      tried++;
      if (before !== after) lifts++;
    } catch (e) { /* 가려진 요소 — 세지 않음 */ }
  }
  await ctx.close();
  const ms = (s) => Math.round(s * 1e6) / 1e3;
  return `${f} motion=${motion} moving=${stat.moving} endless=${stat.endless} transition_ms=${ms(stat.tmax)} animation_ms=${ms(stat.amax)} scroll=${stat.sb} hover_tried=${tried} hover_lifts=${lifts}`;
}

(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch();
  try {
    if (mode === 'theme') {
      for (const f of rest) console.log(await themeLine(browser, f));
    } else if (mode === 'paint') {
      const [theme, ...files] = rest;
      for (const f of files) console.log(await paintLine(browser, theme, f));
    } else if (mode === 'motion') {
      const [motion, ...files] = rest;
      for (const f of files) console.log(await motionLine(browser, motion, f));
    } else {
      console.error('사용: node br.js theme <쪽...> | paint <dark|light> <쪽...> | motion <reduce|no-preference> <쪽...>');
      process.exitCode = 2;
    }
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(2); });
