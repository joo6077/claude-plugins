'use strict';
// 상태 폴더를 1초마다 읽어(폴더 감시는 거들기만) 이 창의 작업 폴더에서 도는 Codex 작업을 항목 하나로 짧게 띄운다.
// 세션별 자세한 진행은 그 세션 채팅 창의 작업 카드가 보인다.
const fs = require('fs');
const vscode = require('vscode');
const status = require('./status');

let item = null;
let timer = null;
let watcher = null;

function refresh() {
  const { jobs, usage } = status.readStatus();
  const roots = status.rootsOf((vscode.workspace.workspaceFolders || []).map((folder) => folder.uri.fsPath));
  const summary = status.summarize(status.jobsToItems(jobs, usage, roots, Math.floor(Date.now() / 1000)));
  if (!summary) {
    if (item) item.hide();
    return;
  }
  if (!item) {
    item = vscode.window.createStatusBarItem('joo6077.codex-status', vscode.StatusBarAlignment.Left, 100);
    item.name = 'Codex 진행 상황';
  }
  item.text = summary.text;
  item.tooltip = summary.tooltip;
  item.show();
}

function watch() {
  if (watcher) return;
  try {
    watcher = fs.watch(status.statusDir(), () => refresh());
    watcher.on('error', () => {
      if (watcher) watcher.close();
      watcher = null;
    });
  } catch (error) {
    watcher = null;
  }
}

function activate(context) {
  refresh();
  watch();
  timer = setInterval(() => {
    watch();
    refresh();
  }, 1000);
  context.subscriptions.push({ dispose: deactivate }, vscode.workspace.onDidChangeWorkspaceFolders(refresh));
}

function deactivate() {
  if (timer) clearInterval(timer);
  timer = null;
  if (watcher) watcher.close();
  watcher = null;
  if (item) item.dispose();
  item = null;
}

module.exports = { activate, deactivate };
