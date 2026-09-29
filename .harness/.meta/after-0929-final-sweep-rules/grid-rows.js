// grid-rows.js <틀 파일> — 시안 5 · 6 · 8 개 틀을 만들어 투표 카드 · 메모 칸이 몇 줄로 놓이는지 잰다.
// 여섯째부터는 e 칸 묶음을 f, g, h 로 복제한다 (design-kit/evals/visuals.spec.js 의 여섯 시안 만들기와 같은 방식).
// 줄마다: n=<시안 수> w=<폭> vote_rows=<줄 수> vote_cols=<첫 줄 칸 수> note_rows=… note_cols=… overflow=<가로 넘침 px>
// 종료 코드: 0 잼 · 2 틀을 못 읽거나 칸 묶음을 못 찾음
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('@playwright/test');

const template = process.argv[2];
if (!template || !fs.existsSync(template)) { console.error(`틀이 없다: ${template}`); process.exit(2); }

function replaceOnce(html, pattern, build) {
  const match = html.match(pattern);
  if (!match) { console.error(`칸 묶음을 못 찾음: ${pattern}`); process.exit(2); }
  return html.replace(match[0], build(match[0]));
}

function toVariant(block, low) {
  const up = low.toUpperCase();
  return block
    .replace(/^(\s*)e: \{/m, `$1${low}: {`)
    .replace(/'e'/g, `'${low}'`)
    .replace(/-e\b/g, `-${low}`)
    .replace(/"e"/g, `"${low}"`)
    .replace(/tab\.e/g, `tab.${low}`)
    .replace(/_E\b/g, `_${up}`)
    .replace(/시안 E/g, `시안 ${up}`)
    .replace(/>E</g, `>${up}<`);
}

function build(n) {
  let html = fs.readFileSync(template, 'utf8');
  const extra = 'fghijk'.slice(0, n - 5).split('');
  const blocks = [
    /<button class="mockup-tab"[^>]*\n\s*data-tab="e"[\s\S]*?<\/button>/,
    /<div class="mockup-panel" id="panel-e">[\s\S]*?<\/div>\n\s*<\/div>/,
    /<div class="mockup-vote-card" onclick="castVote\('e'\)"[\s\S]*?<\/div>\n\s*<\/div>/,
    /<div class="mockup-note-field">\s*<label class="mockup-note-label" for="note-e">[\s\S]*?<\/div>/,
    /\n(\s*)e: \{\n[\s\S]*?\n\s*\},/,
  ];
  if (extra.length) {
    for (const pattern of blocks) {
      html = replaceOnce(html, pattern, (b) => b + extra.map((l) => '\n' + toVariant(b, l).replace(/^\n/, '')).join(''));
    }
    for (const side of ['compare-left', 'compare-right']) {
      html = replaceOnce(html, new RegExp(`id="${side}"[\\s\\S]*?<option value="e"[^\\n]*`),
        (b) => b + extra.map((l) => `\n<option value="${l}" data-i18n="tab.${l}">시안 ${l.toUpperCase()}</option>`).join(''));
    }
    html = replaceOnce(html, /e: '시안 E' \}/, () => "e: '시안 E', " + extra.map((l) => `${l}: '시안 ${l.toUpperCase()}'`).join(', ') + ' }');
    html = replaceOnce(html, /e: 'Variant E' \}/, () => "e: 'Variant E', " + extra.map((l) => `${l}: 'Variant ${l.toUpperCase()}'`).join(', ') + ' }');
  }
  return html.replace(/\{\{TAGS_[A-Z]\}\}/g, '[]');
}

function rows(boxes) {
  const tops = [...new Set(boxes.map((b) => Math.round(b.y)))].sort((a, b) => a - b);
  const first = boxes.filter((b) => Math.round(b.y) === tops[0]).length;
  return { rows: tops.length, cols: first };
}

(async () => {
  const dir = fs.mkdtempSync(path.join(process.env.TMPDIR || os.tmpdir(), 'grid-rows.'));
  const browser = await chromium.launch();
  try {
    for (const n of [5, 6, 8]) {
      const file = path.join(dir, `mockup-${n}.html`);
      fs.writeFileSync(file, build(n));
      for (const w of [1280, 375]) {
        const page = await browser.newPage({ viewport: { width: w, height: 900 } });
        await page.route(/^https?:/, (r) => r.abort());
        await page.goto('file://' + file);
        const vote = await page.$$eval('.mockup-vote-card', (els) => els.map((e) => e.getBoundingClientRect().toJSON()));
        const note = await page.$$eval('.mockup-note-field', (els) => els.map((e) => e.getBoundingClientRect().toJSON()));
        const of = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        const v = rows(vote); const t = rows(note);
        console.log(`n=${n} w=${w} vote=${vote.length} vote_rows=${v.rows} vote_cols=${v.cols} note=${note.length} note_rows=${t.rows} note_cols=${t.cols} overflow=${of}`);
        await page.close();
      }
    }
  } finally {
    await browser.close();
    fs.rmSync(dir, { recursive: true, force: true });
  }
})().catch((e) => { console.error(e); process.exit(2); });
