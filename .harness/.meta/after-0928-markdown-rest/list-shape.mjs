// 그려진 모양 비교 — 사용: MDIT_DIR=<node_modules 폴더> node list-shape.mjs <옛 판 폴더> <새 판 폴더> <파일>...
// markdown-it(html 켬 — 편집기 미리보기처럼 주석은 안 보인다)으로 두 판을 그려 맞댄다.
//   tight : 목록마다 촘촘함(항목 안 문단이 <p> 없이 그려짐) 여부를 차례로 맞대어 다른 목록 수. 한 판에서만 촘촘하면 그 목록 항목이 문단으로 바뀐 것이다
//   count : 목록 · 인용 · 표 · 코드 블록 네 가지 수 가운데 두 판이 다른 것의 수 (목록이 주석 줄에 끊겨 둘로 갈리면 여기 잡힌다)
// 출력: 파일마다 `경로<TAB>tight<TAB>count<TAB>옛 판 목록 수<TAB>새 판 목록 수`, 없는 판은 NA. 끝에 `TOTAL<TAB>tight 합<TAB>count 합<TAB>NA 파일 수`.
import { createRequire } from 'node:module';
import { readFileSync, existsSync } from 'node:fs';
const require = createRequire(process.env.MDIT_DIR + '/');
const md = require('markdown-it')({ html: true });
function shape(path) {
  if (!existsSync(path)) return null;
  const toks = md.parse(readFileSync(path, 'utf8'), {});
  const lists = [], stack = [], n = { bq: 0, table: 0, fence: 0 };
  for (const t of toks) {
    if (/_list_open$/.test(t.type)) { stack.push(lists.length); lists.push(true); }
    else if (/_list_close$/.test(t.type)) stack.pop();
    else if (t.type === 'paragraph_open' && stack.length && !t.hidden) lists[stack[stack.length - 1]] = false;
    else if (t.type === 'blockquote_open') n.bq++;
    else if (t.type === 'table_open') n.table++;
    else if (t.type === 'fence') n.fence++;
  }
  return { lists, n };
}
const [a, b, ...files] = process.argv.slice(2);
let ts = 0, cs = 0, na = 0;
for (const f of files) {
  const x = shape(a + '/' + f), y = shape(b + '/' + f);
  if (!x || !y) { na++; console.log([f, 'NA', 'NA', x ? x.lists.length : 'NA', y ? y.lists.length : 'NA'].join('\t')); continue; }
  let t = 0;
  for (let i = 0; i < Math.min(x.lists.length, y.lists.length); i++) if (x.lists[i] !== y.lists[i]) t++;
  let c = (x.lists.length !== y.lists.length ? 1 : 0) + ['bq', 'table', 'fence'].filter(k => x.n[k] !== y.n[k]).length;
  ts += t; cs += c;
  console.log([f, t, c, x.lists.length, y.lists.length].join('\t'));
}
console.log(['TOTAL', ts, cs, na].join('\t'));
