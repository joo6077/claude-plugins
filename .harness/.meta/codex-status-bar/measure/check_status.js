// status.js 의 순수 함수에 고정 입력을 넣고 결과를 JSON 으로 낸다. 판정은 measure.py 가 한다.
const path = require('path');
const status = require(path.join(process.argv[2], 'status.js'));
const now = 1800000000;
const usage = { limits: { '5시간': { used: 12, resets_at: now + 3600 }, '주간': { used: 3, resets_at: now + 86400 } } };
const job = (extra) => Object.assign({ kind: '감독', session: 'a1b2c3d4-0000', folder: '/w/repo/sub', step: 'judge-1',
  started: now - 240, updated: now - 5, pid: 111 }, extra);
const alive = (pid) => pid !== 999;
const run = (jobs, use) => status.jobsToItems(jobs, use, ['/w/repo'], now, alive);
console.log(JSON.stringify({
  a: run([job()], usage),
  b: run([job({ folder: '/elsewhere' })], usage),
  c: run([job({ pid: 999 })], usage),
  d: run([], usage),
  e: run([job(), job({ kind: '리서치', session: 'e5f6a7b8-0000', step: '시도 1/3', pid: 112, started: now - 30 })], usage),
  f: run([job()], null),
  g: run([job({ folder: '/w/repo-other' })], usage),
  h: run([job({ session: '' })], usage),
  i: run([job({ updated: now - 600 })], usage),
  j: run([job()], { limits: { '5시간': { used: 12, resets_at: now - 10 }, '주간': { used: 3, resets_at: now + 86400 } } }),
  k: status.jobsToItems([job({ pid: process.pid, folder: '/w/repo' })], usage, ['/w/repo'], now),
}));
