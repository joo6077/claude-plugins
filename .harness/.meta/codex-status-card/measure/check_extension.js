// 가짜 vscode 모듈로 extension.js 를 띄워 창마다 항목이 하나뿐이고, 작업 수에 따라 글자가 바뀌며, 작업이 살아 있는 채로 꺼도 정리되는지 잰다.
const Module = require('module');
const path = require('path');
const fs = require('fs');
const os = require('os');
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cs-card-'));
const status = path.join(dir, 'status');
process.env.CODEX_STATUS_DIR = status;
const created = [];
const vscode = {
  StatusBarAlignment: { Left: 1, Right: 2 },
  MarkdownString: class { constructor(value) { this.value = value; } },
  window: {
    createStatusBarItem(id, alignment, priority) {
      const item = { id, alignment, priority, text: '', tooltip: '', visible: false, disposed: false,
        show() { this.visible = true; }, hide() { this.visible = false; }, dispose() { this.disposed = true; this.visible = false; } };
      created.push(item);
      return item;
    },
  },
  workspace: { workspaceFolders: [{ uri: { fsPath: path.join(dir, 'repo') } }], onDidChangeWorkspaceFolders: () => ({ dispose() {} }) },
};
const load = Module._load;
Module._load = function (request, ...rest) { return request === 'vscode' ? vscode : load.call(this, request, ...rest); };
const extension = require(path.join(process.argv[2], 'extension.js'));
const context = { subscriptions: [] };
const wait = (ms) => new Promise((done) => setTimeout(done, ms));
const visible = () => created.filter((item) => item.visible && !item.disposed);
const tooltip = (item) => (item.tooltip && item.tooltip.value !== undefined ? item.tooltip.value : String(item.tooltip));
const now = () => Math.floor(Date.now() / 1000);
const job = (name, extra) => fs.writeFileSync(path.join(status, name), JSON.stringify(Object.assign({ kind: '감독',
  session: 'a1b2c3d4', folder: path.join(dir, 'repo'), step: 'judge-1', started: now() - 60, updated: now(), pid: process.pid }, extra)));
async function until(test) {
  for (let i = 0; i < 50 && !test(); i += 1) await wait(100);
}
(async () => {
  const report = {};
  extension.activate(context);
  fs.mkdirSync(status);
  fs.writeFileSync(path.join(status, 'usage.json'), JSON.stringify({ limits: { '5시간': { used: 12, resets_at: now() + 3600 } } }));
  job('감독-1.json');
  job('리서치-2.json', { kind: '리서치', session: 'e5f6a7b8', step: '시도 1/3', topic: '상태 표시줄 조사' });
  await until(() => visible().length && visible()[0].text.includes('리서치'));
  report.two = visible().map((item) => ({ text: item.text, tooltip: tooltip(item) }));
  fs.unlinkSync(path.join(status, '리서치-2.json'));
  await until(() => visible().length && !visible()[0].text.includes('리서치'));
  report.one = visible().map((item) => item.text);
  report.created_so_far = created.length;
  // 작업이 살아 있는 채로 끈다 — 끄는 쪽이 직접 정리해야 한다.
  // 구독 목록은 하나도 부르지 않고 deactivate 만 부른다.
  report.ids = [...new Set(created.map((item) => item.id))];
  if (extension.deactivate) extension.deactivate();
  report.all_disposed = created.every((item) => item.disposed);
  job('리서치-3.json', { kind: '리서치', session: 'f0f0f0f0' });
  await wait(2500);
  report.created_after_off = created.length - report.created_so_far;
  console.log(JSON.stringify(report));
  fs.rmSync(dir, { recursive: true, force: true });
})();
