// 계약 after-0929-tail Mermaid 대조 측정 — 새 검사와 따로 짠 그리기. 레포 맨 위 폴더에서 부른다.
//   node mmrender.js <mermaid.min.js> <쪽...>
// 예시 = 쪽의 <pre> 가운데 빈 줄 · `%%` 줄을 건넌 첫 줄이 Mermaid 그림 종류 낱말로 시작하는 것.
// 빈 쪽에 mermaid.min.js 를 넣고 예시마다 mermaid.render 를 불러, 그림(svg)이 있고 도형이 1 개 이상이며
// 오류 그림(aria-roledescription="error") · "Syntax error" · "Parse error" 글이 없으면 OK.
// 끝 줄: pages=<예시가 있는 쪽 수> examples=<예시 수> bad=<안 그려진 수>. 종료 코드 0 다 그려짐 · 1 하나라도 안 그려짐 · 2 잴 수 없음.
const path = require('path');
const { chromium } = require(path.join(process.cwd(), 'node_modules', 'playwright'));

const KW = /^(flowchart|graph|sequenceDiagram|classDiagram(-v2)?|stateDiagram(-v2)?|erDiagram|journey|gantt|pie|mindmap|timeline|quadrantChart|gitGraph|C4\w+|requirementDiagram|sankey(-beta)?|xychart(-beta)?|block(-beta)?|architecture(-beta)?|kanban|packet(-beta)?|radar(-beta)?|treemap(-beta)?)\b/;

(async () => {
  const [lib, ...pages] = process.argv.slice(2);
  const b = await chromium.launch();
  const r = await b.newPage();
  await r.setContent('<!doctype html><html><body></body></html>');
  await r.addScriptTag({ path: lib });
  await r.evaluate(() => mermaid.initialize({ startOnLoad: false }));
  let total = 0, bad = 0, withEx = 0;
  for (const f of pages) {
    const p = await b.newPage();
    await p.goto('file://' + path.resolve(f));
    const codes = await p.evaluate((src) => {
      const re = new RegExp(src);
      return [...document.querySelectorAll('pre')].map((e) => e.textContent.replace(/\r/g, '')).filter((t) => {
        const lines = t.split('\n');
        let i = 0;
        while (i < lines.length && (!lines[i].trim() || lines[i].trim().startsWith('%%'))) i++;
        return re.test((lines[i] || '').trim());
      });
    }, KW.source);
    await p.close();
    withEx += codes.length > 0;
    for (let i = 0; i < codes.length; i++) {
      total++;
      const res = await r.evaluate(async ({ code, id }) => {
        try {
          const out = await mermaid.render(id, code);
          const d = new DOMParser().parseFromString(out.svg, 'image/svg+xml');
          return { svg: !!d.querySelector('svg'), shapes: d.querySelectorAll('rect,path,circle,ellipse,polygon,line,text').length,
            err: /Syntax error|Parse error/i.test(out.svg) || !!d.querySelector('[aria-roledescription=error]') };
        } catch (e) {
          return { svg: false, shapes: 0, err: true, msg: String(e.message || e).split('\n')[0].slice(0, 100) };
        }
      }, { code: codes[i], id: 'mm' + total });
      const ok = res.svg && !res.err && res.shapes > 0;
      bad += !ok;
      console.log(`${ok ? 'OK ' : 'BAD'} ${f}#${i + 1} svg=${res.svg ? 1 : 0} shapes=${res.shapes} err=${res.err ? 1 : 0}${res.msg ? ' msg=' + res.msg : ''}`);
    }
  }
  console.log(`pages=${withEx} examples=${total} bad=${bad}`);
  await b.close();
  process.exit(bad ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
