// 겹친 코드 블록 자리 검사 — 사용: MDIT_DIR=<node_modules 폴더> node site-check.mjs <sites.tsv>
// sites.tsv 한 줄 = 파일<TAB>처음 줄<TAB>끝 줄<TAB>다음 줄. 세 글은 파일 안에서 한 줄에만 있어야 한다.
// markdown-it 이 그린 코드 블록 가운데 「처음 줄」 을 담은 것이 하나이고, 그 블록이 「끝 줄」 까지 담고,
// 「다음 줄」 이 그 블록이 끝난 뒤 코드 블록 밖에 있으면 OK 다. 바깥 블록이 안쪽 울타리에서 먼저 닫히면 FAIL 이다.
// 출력: 자리마다 `OK|FAIL|BADANCHOR<TAB>파일<TAB>처음 줄 앞 40 자`, 끝에 `SITES<TAB>전체<TAB>OK 수`. 종료 코드: 모두 OK 0 · FAIL 1 · 글을 못 찾음 2.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire(process.env.MDIT_DIR + '/');
const md = require('markdown-it')();
let n = 0, ok = 0, bad = false;
for (const row of readFileSync(process.argv[2], 'utf8').split('\n').filter(Boolean)) {
  const [f, start, end, next] = row.split('\t');
  const src = readFileSync(f, 'utf8'); const L = src.split('\n');
  const where = x => L.map((l, i) => l.includes(x) ? i : -1).filter(i => i >= 0);
  const ws = where(start), we = where(end), wn = where(next);
  n++;
  if (ws.length !== 1 || we.length !== 1 || wn.length !== 1) { bad = true; console.log(['BADANCHOR', f, start.slice(0, 40)].join('\t')); continue; }
  const fences = md.parse(src, {}).filter(t => t.type === 'fence');
  const hits = fences.filter(t => t.content.includes(start));
  const nextInCode = fences.some(t => wn[0] >= t.map[0] && wn[0] < t.map[1]);
  const pass = hits.length === 1 && hits[0].content.includes(end) && wn[0] >= hits[0].map[1] && !nextInCode;
  if (pass) ok++;
  console.log([pass ? 'OK' : 'FAIL', f, start.slice(0, 40)].join('\t'));
}
console.log(['SITES', n, ok].join('\t'));
process.exit(bad ? 2 : ok === n ? 0 : 1);
