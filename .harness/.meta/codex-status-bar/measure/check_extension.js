// 가짜 vscode 모듈로 extension.js 를 띄워, 상태 파일에 따라 항목이 작업마다 하나씩 보였다 사라지고 끌 때 정리되는지 잰다.
const Module = require('module');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { spawnSync } = require('child_process');
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cs-ext-'));
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
const now = () => Math.floor(Date.now() / 1000);
const job = (name, extra) => fs.writeFileSync(path.join(status, name), JSON.stringify(Object.assign({ kind: '감독',
  session: 'a1b2c3d4', folder: path.join(dir, 'repo'), step: 'judge-1', started: now() - 60, updated: now(), pid: process.pid }, extra)));
async function until(test) {
  const began = Date.now();
  for (let i = 0; i < 50 && !test(); i += 1) await wait(100);
  return Date.now() - began;
}
(async () => {
  const report = {};
  try { extension.activate(context); report.activate_error = null; } catch (error) { report.activate_error = String(error); }
  report.before = visible().length;                       // 상태 폴더가 아직 없다
  fs.mkdirSync(status);
  fs.writeFileSync(path.join(status, 'usage.json'), JSON.stringify({ limits: { '5시간': { used: 12, resets_at: now() + 3600 } } }));
  fs.writeFileSync(path.join(status, '감독-9.json'), '{"kind": "감');  // 반쯤 쓴 파일
  job('감독-1.json');
  report.shown_ms = await until(() => visible().length >= 1);
  report.shown = visible().map((item) => item.text);
  job('리서치-2.json', { kind: '리서치', session: 'e5f6a7b8', step: '시도 1/3' });
  report.two_ms = await until(() => visible().length >= 2);
  report.two = visible().map((item) => item.id);
  const dead = spawnSync(process.execPath, ['-e', '']).pid;
  job('감독-3.json', { pid: dead, session: 'deaddead' });
  job('감독-4.json', { folder: path.join(dir, 'elsewhere'), session: 'out0out0' });
  await wait(2500);
  report.with_noise = visible().map((item) => item.text);
  fs.unlinkSync(path.join(status, '리서치-2.json'));
  report.one_ms = await until(() => visible().length <= 1);
  report.one = visible().length;
  fs.unlinkSync(path.join(status, '감독-1.json'));
  report.gone_ms = await until(() => visible().length === 0);
  report.after = visible().length;
  report.created_before_off = created.length;
  for (const item of context.subscriptions) if (item && item.dispose) item.dispose();
  if (extension.deactivate) extension.deactivate();
  report.all_disposed = created.every((item) => item.disposed);
  job('감독-5.json');
  await wait(2500);
  report.created_after_off = created.length;
  console.log(JSON.stringify(report));
  fs.rmSync(dir, { recursive: true, force: true });
})();
