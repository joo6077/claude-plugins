#!/usr/bin/env node
/**
 * check-docs-mermaid.js — 문서 쪽에 실린 Mermaid 예시가 실제로 그림이 되는지 잰다.
 *
 * 쪽의 예시는 글로만 실려 있어, 문법이 깨져도 아무 검사가 잡지 못했다(2026-09-29). 브라우저 빈 쪽에
 * 레포가 package.json 에 못박은 Mermaid(node_modules)를 넣고 예시마다 mermaid.render 를 부른다.
 *
 * 예시 = 쪽의 <pre> 가운데 빈 줄 · `%%` 줄을 건넌 첫 줄이 Mermaid 그림 종류 낱말로 시작하는 것.
 * 그려짐 = render 가 예외 없이 돌려준 그림에 svg 와 도형이 1 개 이상 있고, 오류 그림
 * (aria-roledescription="error") · "Syntax error" · "Parse error" 글이 없는 것.
 *
 * Usage:
 *   node scripts/check-docs-mermaid.js            # git 이 추적하는 docs/*.html 전부
 *   node scripts/check-docs-mermaid.js <쪽...>    # 준 쪽만
 *
 * 종료 코드는 harness/evals/gate-exit-codes.md — 0 통과 · 1 안 그려진 예시 · 2 못 돌림 · 3 예시 0 개.
 */
const path = require('path');
const { execFileSync } = require('child_process');

const REPO = path.resolve(__dirname, '..');
const DIAGRAM_KEYWORD = /^(flowchart|graph|sequenceDiagram|classDiagram(-v2)?|stateDiagram(-v2)?|erDiagram|journey|gantt|pie|mindmap|timeline|quadrantChart|gitGraph|C4\w+|requirementDiagram|sankey(-beta)?|xychart(-beta)?|block(-beta)?|architecture(-beta)?|kanban|packet(-beta)?|radar(-beta)?|treemap(-beta)?)\b/;

function targetPages() {
  const given = process.argv.slice(2);
  if (given.length) return given.map((page) => path.resolve(page));
  return execFileSync('git', ['-C', REPO, 'ls-files', 'docs/*.html'], { encoding: 'utf8' })
    .split('\n').filter(Boolean).map((file) => path.join(REPO, file));
}

async function examplesOf(browser, page) {
  const tab = await browser.newPage();
  try {
    await tab.goto('file://' + page);
    return await tab.evaluate((keyword) => {
      const pattern = new RegExp(keyword);
      return [...document.querySelectorAll('pre')].map((pre) => pre.textContent.replace(/\r/g, '')).filter((text) => {
        const first = text.split('\n').map((line) => line.trim()).find((line) => line && !line.startsWith('%%'));
        return pattern.test(first || '');
      });
    }, DIAGRAM_KEYWORD.source);
  } finally {
    await tab.close();
  }
}

// 돌려주는 값이 빈 글이면 그려짐, 아니면 안 그려진 까닭 한 줄
function renderProblem(canvas, code, id) {
  return canvas.evaluate(async ({ code, id }) => {
    try {
      const { svg } = await mermaid.render(id, code);
      const drawn = new DOMParser().parseFromString(svg, 'image/svg+xml');
      if (drawn.querySelector('[aria-roledescription=error]') || /Syntax error|Parse error/i.test(svg)) return '오류 그림';
      if (!drawn.querySelector('svg')) return 'svg 없음';
      if (!drawn.querySelectorAll('rect,path,circle,ellipse,polygon,line,text').length) return '도형 없음';
      return '';
    } catch (error) {
      return String(error.message || error).split('\n')[0];
    }
  }, { code, id });
}

async function main() {
  let chromium;
  let mermaidLib;
  try {
    ({ chromium } = require(require.resolve('playwright', { paths: [REPO] })));
    mermaidLib = require.resolve('mermaid/dist/mermaid.min.js', { paths: [REPO] });
  } catch (error) {
    console.log(`ERROR 준비 실패 — npm ci 를 먼저 돌린다 (${error.message.split('\n')[0]})`);
    return 2;
  }
  const browser = await chromium.launch();
  try {
    const canvas = await browser.newPage();
    await canvas.setContent('<!doctype html><html><body></body></html>');
    await canvas.addScriptTag({ path: mermaidLib });
    await canvas.evaluate(() => mermaid.initialize({ startOnLoad: false }));
    let pagesWithExamples = 0;
    let examples = 0;
    let broken = 0;
    for (const page of targetPages()) {
      const codes = await examplesOf(browser, page);
      if (!codes.length) continue;
      pagesWithExamples++;
      const shown = path.relative(REPO, page);
      for (const code of codes) {
        examples++;
        const problem = await renderProblem(canvas, code, `example${examples}`);
        if (problem) broken++;
        console.log(problem ? `BAD ${shown} 예시 ${examples}: ${problem}` : `OK  ${shown} 예시 ${examples}`);
      }
    }
    console.log(`쪽 ${pagesWithExamples} · 예시 ${examples} · 안 그려진 예시 ${broken}`);
    if (!examples) return 3;
    return broken ? 1 : 0;
  } finally {
    await browser.close();
  }
}

main().then((code) => process.exit(code), (error) => {
  console.log(`ERROR ${String(error.message || error).split('\n')[0]}`);
  process.exit(2);
});
