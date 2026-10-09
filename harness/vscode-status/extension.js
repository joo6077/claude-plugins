'use strict';
// 상태 폴더를 1초마다 읽어(폴더 감시는 거들기만) 이 창의 작업 폴더에서 도는 Codex 작업을 작업마다 하나씩 띄운다.
const fs = require('fs');
const vscode = require('vscode');
const status = require('./status');

const items = new Map();
let timer = null;
let watcher = null;

function refresh() {
  const { jobs, usage } = status.readStatus();
  const roots = status.rootsOf((vscode.workspace.workspaceFolders || []).map((folder) => folder.uri.fsPath));
  const wanted = status.jobsToItems(jobs, usage, roots, Math.floor(Date.now() / 1000));
  const keep = new Set(wanted.map((want) => want.key));
  for (const [key, item] of items) {
    if (!keep.has(key)) {
      item.dispose();
      items.delete(key);
    }
  }
  wanted.forEach((want, order) => {
    let item = items.get(want.key);
    if (!item) {
      item = vscode.window.createStatusBarItem(`joo6077.codex-status.${want.key}`, vscode.StatusBarAlignment.Left, 100 - order);
      item.name = 'Codex 진행 상황';
      items.set(want.key, item);
    }
    item.text = want.text;
    item.tooltip = want.tooltip;
    item.show();
  });
}

function watch() {
  if (watcher) return;
  try {
    watcher = fs.watch(status.statusDir(), () => refresh());
    watcher.on('error', () => {
      watcher.close();
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
  for (const item of items.values()) item.dispose();
  items.clear();
}

module.exports = { activate, deactivate };
