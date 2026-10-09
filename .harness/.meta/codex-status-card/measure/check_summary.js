// status.js 의 작업별 줄(jobsToItems)과 창 하나짜리 요약(summarize)에 고정 입력을 넣고 결과를 JSON 으로 낸다.
const path = require('path');
const status = require(path.join(process.argv[2], 'status.js'));
const now = 1800000000;
const usage = { limits: { '5시간': { used: 12, resets_at: now + 3600 }, '주간': { used: 3, resets_at: now + 86400 } } };
const job = (extra) => Object.assign({ kind: '감독', session: 'a1b2c3d4-0000', folder: '/w/repo', step: 'judge-1',
  started: now - 240, updated: now - 5, pid: 111 }, extra);
const research = job({ kind: '리서치', session: 'e5f6a7b8-0000', step: '시도 1/3', topic: 'VS Code 상태 표시줄 API 조사', started: now - 30, pid: 112 });
const alive = () => true;
const items = (jobs) => status.jobsToItems(jobs, usage, ['/w/repo'], now, alive);
console.log(JSON.stringify({
  one: items([research]),
  both: items([job(), research]),
  summary_both: status.summarize(items([job(), research])),
  summary_one: status.summarize(items([research])),
  summary_none: status.summarize(items([])),
  no_topic: items([job()]),
  summary_many: status.summarize(items([job(), job({ pid: 113, session: 'c0c0c0c0' }), research])),
}));
