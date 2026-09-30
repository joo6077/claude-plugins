// 울타리 짝 검사 — 사용: MDIT_DIR=<node_modules 폴더> node fence-check.mjs <파일>...
// markdown-it(CommonMark) 가 그린 코드 블록을 보고 짝이 깨진 흔적 여섯 가지를 센다.
//   swallowed: 블록 안에 바깥 울타리와 같은 글자 · 같은 길이 이상의 여는 울타리(뒤에 언어)가 든 줄 — 안쪽 블록이 바깥을 먼저 닫았다
//   unclosed : 닫는 울타리 없이 파일 끝까지 간 블록 (닫는 줄은 목록 · 인용 안도 보도록 앞 공백과 > 를 따지지 않는다)
//   leak     : 계획 문서의 뼈대 줄(`- [ ] **Step N` · `### Task N` · `**Files:**`)이 코드 블록 안에 든 수
//   texthead : 언어가 text 인 블록의 첫 글 줄이 제목(`#`) · 할 일 칸(`- [ ]`) 인 수 — 본문이 코드로 빨려 든 표시
//   mdcolon  : 언어가 markdown · md 인 블록의 마지막 글 줄이 `:` 로 끝나는 수 — 안쪽 여는 울타리에서 닫힌 표시
//   empty    : 내용이 빈 블록 수
// 출력: 파일마다 `경로<TAB>swallowed<TAB>unclosed<TAB>leak<TAB>texthead<TAB>mdcolon<TAB>empty<TAB>blocks`, 끝에 `TOTAL<TAB>…`.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire(process.env.MDIT_DIR + '/');
const md = require('markdown-it')();
const plan = /^(- \[[ x]\] \*\*Step \d|#{2,4} Task \d|\*\*Files:\*\*)/;
const total = [0, 0, 0, 0, 0, 0, 0];
for (const p of process.argv.slice(2)) {
  const src = readFileSync(p, 'utf8');
  const lines = src.split('\n');
  const c = [0, 0, 0, 0, 0, 0, 0];
  for (const t of md.parse(src, {})) {
    if (t.type !== 'fence') continue;
    c[6]++;
    const ch = t.markup[0], L = t.markup.length;
    const inner = new RegExp('^ {0,3}\\' + ch + '{' + L + ',}[^\\s' + ch + ']');
    const body = t.content.split('\n');
    const text = body.filter(x => x.trim());
    for (const ln of body) { if (inner.test(ln)) c[0]++; if (plan.test(ln)) c[2]++; }
    const last = lines[t.map[1] - 1] ?? '';
    const close = new RegExp('^[\\s>]*\\' + ch + '{' + L + ',}\\s*$');
    if (!(t.map[1] - t.map[0] >= 2 && close.test(last))) c[1]++;
    const info = t.info.trim().split(/\s+/)[0];
    if (info === 'text' && text.length && /^(#{1,6} |- \[[ x]\] )/.test(text[0])) c[3]++;
    if ((info === 'markdown' || info === 'md') && text.length && /:\s*$/.test(text[text.length - 1])) c[4]++;
    if (!text.length) c[5]++;
  }
  console.log([p, ...c].join('\t'));
  c.forEach((v, i) => { total[i] += v; });
}
console.log(['TOTAL', ...total].join('\t'));
