'use strict';
// 상태 폴더를 읽고 무엇을 띄울지 정한다. 판단은 모두 여기 있고 extension.js 는 그리기만 한다.
const fs = require('fs');
const os = require('os');
const path = require('path');

// 쓰는 쪽은 30초마다 updated 를 고친다. 2분 넘게 멈췄으면 강제 종료로 남은 파일이거나 pid 가 재사용된 것이다.
const STALE_SECONDS = 120;

function statusDir() {
  return process.env.CODEX_STATUS_DIR || path.join(os.homedir(), '.codex-status');
}

function pidAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error.code === 'EPERM';
  }
}

function rootsOf(folders) {
  return folders.map((folder) => {
    try {
      return fs.realpathSync(folder);
    } catch (error) {
      return folder;
    }
  });
}

function inside(folder, roots) {
  return roots.some((root) => {
    const rest = path.relative(root, folder);
    return rest === '' || (!rest.startsWith('..') && !path.isAbsolute(rest));
  });
}

function elapsed(seconds) {
  return seconds < 60 ? `${Math.max(0, seconds)}초` : `${Math.floor(seconds / 60)}분`;
}

function usageText(usage, now) {
  const limits = (usage && usage.limits) || {};
  return Object.entries(limits)
    .filter(([, window]) => window && typeof window.used === 'number' && typeof window.resets_at === 'number' && window.resets_at > now)
    .map(([label, window]) => ` · ${label} ${+window.used.toFixed(1)}%`)
    .join('');
}

function jobsToItems(jobs, usage, folders, now, alive = pidAlive) {
  const shown = usageText(usage, now);
  return jobs
    .filter((job) => job && Number.isInteger(job.pid) && typeof job.folder === 'string' && inside(job.folder, folders)
      && alive(job.pid) && now - (job.updated || 0) <= STALE_SECONDS)
    .map((job) => {
      const short = (job.session || '').slice(0, 4) || '----';
      const topic = job.topic ? `${job.topic} · ` : '';
      return {
        key: `${job.session || ''}|${job.kind}|${job.pid}`,
        kind: job.kind,
        text: `${short} ${job.kind} · ${topic}${job.step} · ${elapsed(now - (job.started || now))}${shown}`,
      };
    });
}

// 창마다 항목 하나 — 종류별 개수만 짧게 보이고, 작업별 줄은 풀이에 한 줄씩.
const KINDS = ['감독', '리서치'];

function summarize(items) {
  if (!items.length) return null;
  const counts = KINDS.map((kind) => [kind, items.filter((item) => item.kind === kind).length]).filter(([, count]) => count);
  return {
    text: `$(sync~spin) ${counts.map(([kind, count]) => `${kind} ${count}`).join(' · ')}`,
    tooltip: items.map((item) => item.text).join('\n'),
  };
}

function readStatus(dir = statusDir()) {
  let names = [];
  try {
    names = fs.readdirSync(dir);
  } catch (error) {
    return { jobs: [], usage: null };
  }
  const jobs = [];
  let usage = null;
  for (const name of names) {
    if (!name.endsWith('.json') || name.startsWith('.')) continue;
    let data;
    try {
      data = JSON.parse(fs.readFileSync(path.join(dir, name), 'utf8'));
    } catch (error) {
      continue;
    }
    if (name === 'usage.json') usage = data;
    else jobs.push(data);
  }
  return { jobs, usage };
}

module.exports = { statusDir, pidAlive, rootsOf, jobsToItems, summarize, readStatus };
