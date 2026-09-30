#!/usr/bin/env node
/**
 * check-docs-mermaid.js 시험 — 임시 폴더의 쪽으로 아홉 경우를 돌린다. 레포 파일은 건드리지 않는다.
 *
 *   1. 그려지는 예시 하나 쪽 → 종료 코드 0
 *   2. 괄호를 닫지 않은 예시 쪽 → 종료 코드 1, 그 쪽 이름이 적힘
 *   3. 예시 없는 쪽 → 종료 코드 3
 *   4. node_modules 를 찾을 수 없는 임시 폴더로 옮긴 검사 사본 → 종료 코드 2
 *   5. 이름표 「Mermaid flowchart 예시」 에 종류 이름이 틀린 flowchat 예시 쪽 → 종료 코드 1
 *   6. 같은 이름표에 `---` 머리말 + flowchat 예시 쪽 → 종료 코드 1
 *   7. 같은 이름표에 머리말 + 정상 flowchart 예시만 있는 쪽 → 종료 코드 0, 예시 1 개로 셈
 *   8. 이름표 「셸 명령 예시」 인 <pre> 는 예시로 세지 않음 → 종료 코드 0, 예시 1 개로 셈
 *   9. 이름표 없이 머리말 + 정상 flowchart 예시만 있는 쪽 → 종료 코드 0, 예시 1 개로 셈 (머리말 건너뛰기 길)
 *
 * Usage:
 *   node scripts/test-check-docs-mermaid.js [--check <검사 사본 경로>]
 *
 * --check 는 음성 대조용이다 — 늘 0 을 내는 사본은 경우 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 가 실패해야 한다(7 · 8 · 9 는 끝 줄의 예시 수로).
 * 머리말을 건너지 않고 첫 줄만 보는 사본은 경우 9 만 실패한다 — 경우 6 · 7 은 이름표 길로 세어져 그 코드를 지나지 않는다.
 * 종료 코드는 harness/evals/gate-exit-codes.md 를 따른다 (0 통과 · 1 실패 · 2 준비 실패).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const checkFlag = process.argv.indexOf('--check');
const check = path.resolve(checkFlag > 0 ? process.argv[checkFlag + 1] : path.join(__dirname, 'check-docs-mermaid.js'));
const GOOD = '<pre>flowchart LR\n  A[&quot;시작&quot;] --&gt; B[&quot;끝&quot;]</pre>';
const LABEL = 'aria-label="Mermaid flowchart 예시"';
const FRONT = '---\ntitle: 흐름 예시\n---\n';
const EDGE = '\n  A[&quot;시작&quot;] --&gt; B[&quot;끝&quot;]';

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
  ['5 이름표 붙은 종류 이름 오타는 1 과 쪽 이름', (tmp) => {
    const { code, output } = runCheck(check, writePage(tmp, 'typo.html', `${GOOD}<pre ${LABEL}>flowchat LR${EDGE}</pre>`));
    return code === 1 && output.includes('typo.html');
  }],
  ['6 머리말 뒤 종류 이름 오타는 1 과 쪽 이름', (tmp) => {
    const { code, output } = runCheck(check, writePage(tmp, 'front-typo.html', `${GOOD}<pre ${LABEL}>${FRONT}flowchat LR${EDGE}</pre>`));
    return code === 1 && output.includes('front-typo.html');
  }],
  ['7 머리말 붙은 정상 예시는 세고 통과', (tmp) => {
    const { code, output } = runCheck(check, writePage(tmp, 'front.html', `<pre ${LABEL}>${FRONT}flowchart LR${EDGE}</pre>`));
    return code === 0 && output.includes('예시 1 · 안 그려진 예시 0');
  }],
  ['8 Mermaid 아닌 이름표는 안 셈', (tmp) => {
    const { code, output } = runCheck(check, writePage(tmp, 'shell.html', `${GOOD}<pre aria-label="셸 명령 예시">ls -la</pre>`));
    return code === 0 && output.includes('예시 1 · 안 그려진 예시 0');
  }],
  ['9 이름표 없는 머리말 정상 예시는 세고 통과', (tmp) => {
    const { code, output } = runCheck(check, writePage(tmp, 'front-bare.html', `<pre>${FRONT}flowchart LR${EDGE}</pre>`));
    return code === 0 && output.includes('예시 1 · 안 그려진 예시 0');
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
