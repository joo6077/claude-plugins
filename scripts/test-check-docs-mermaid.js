#!/usr/bin/env node
/**
 * check-docs-mermaid.js 시험 — 임시 폴더의 쪽으로 네 경우를 돌린다. 레포 파일은 건드리지 않는다.
 *
 *   1. 그려지는 예시 하나 쪽 → 종료 코드 0
 *   2. 괄호를 닫지 않은 예시 쪽 → 종료 코드 1, 그 쪽 이름이 적힘
 *   3. 예시 없는 쪽 → 종료 코드 3
 *   4. node_modules 를 찾을 수 없는 임시 폴더로 옮긴 검사 사본 → 종료 코드 2
 *
 * Usage:
 *   node scripts/test-check-docs-mermaid.js [--check <검사 사본 경로>]
 *
 * --check 는 음성 대조용이다 — 늘 0 을 내는 사본은 경우 2 · 3 · 4 가 실패해야 한다.
 * 종료 코드는 harness/evals/gate-exit-codes.md 를 따른다 (0 통과 · 1 실패 · 2 준비 실패).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const checkFlag = process.argv.indexOf('--check');
const check = path.resolve(checkFlag > 0 ? process.argv[checkFlag + 1] : path.join(__dirname, 'check-docs-mermaid.js'));
const GOOD = '<pre>flowchart LR\n  A[&quot;시작&quot;] --&gt; B[&quot;끝&quot;]</pre>';

function writePage(dir, name, pre) {
  const file = path.join(dir, name);
  fs.writeFileSync(file, `<!DOCTYPE html><html><body>${pre}</body></html>\n`);
  return file;
}

function runCheck(checkPath, page, cwd) {
  const result = spawnSync('node', [checkPath, page], { cwd, encoding: 'utf8' });
  return { code: result.status, output: result.stdout + result.stderr };
}

const CASES = [
  ['1 그려지는 예시는 통과', (tmp) => runCheck(check, writePage(tmp, 'good.html', GOOD)).code === 0],
  ['2 깨진 예시는 1 과 쪽 이름', (tmp) => {
    const { code, output } = runCheck(check, writePage(tmp, 'broken.html', '<pre>flowchart LR\n  A[&quot;시작 --&gt; B</pre>'));
    return code === 1 && output.includes('broken.html');
  }],
  ['3 예시 없는 쪽은 3', (tmp) => runCheck(check, writePage(tmp, 'none.html', '<pre>ls -la</pre>')).code === 3],
  ['4 node_modules 없는 폴더의 사본은 2', (tmp) => {
    const bare = fs.mkdtempSync(path.join(tmp, 'bare-'));
    fs.mkdirSync(path.join(bare, 'scripts'));
    const copied = path.join(bare, 'scripts', 'check-docs-mermaid.js');
    fs.copyFileSync(check, copied);
    return runCheck(copied, writePage(tmp, 'good-bare.html', GOOD), bare).code === 2;
  }],
];

if (!fs.existsSync(check)) {
  console.log(`ERROR: 검사가 없다 — ${check}`);
  process.exit(2);
}
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'mermaid-test-'));
let passed = 0;
try {
  for (const [label, run] of CASES) {
    const ok = run(tmp);
    passed += ok;
    console.log(`${ok ? 'PASS' : 'FAIL'} 경우 ${label}`);
  }
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
console.log(`경우 ${CASES.length} 개 중 통과 ${passed}`);
process.exit(passed === CASES.length ? 0 : 1);
