// 구조-02 · 구조-03 브라우저 측정 (Chromium). 사용: node measure.cjs <조건 번호> <작업 폴더> <playwright 모듈 경로>
const { spawn } = require("child_process");
const path = require("path");
const [condition, work, playwrightPath] = process.argv.slice(2);
const { chromium } = require(playwrightPath);

function serve(folder) {
  const port = 20000 + Math.floor(Math.random() * 20000);
  const server = spawn("python3", ["-m", "http.server", String(port), "--bind", "127.0.0.1"], { cwd: folder, stdio: "ignore" });
  return { server, base: `http://127.0.0.1:${port}` };
}

async function waitUp(page, url) {
  for (let attempt = 0; attempt < 50; attempt++) {
    try { await page.goto(url); return; } catch { await new Promise((done) => setTimeout(done, 100)); }
  }
  throw new Error(`서버가 뜨지 않았다: ${url}`);
}

const box = (rect) => ({ left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom, width: rect.width, height: rect.height });
const panels = (page) => page.evaluate(() => [...document.querySelectorAll(".scn")].map((card) => {
  const panel = card.querySelector(".follow");
  if (!panel) return null;
  const big = panel.querySelector(".stage img"), dot = panel.querySelector(".tap"), rect = (node) => node.getBoundingClientRect();
  return { display: getComputedStyle(panel).display, label: panel.querySelector(".label").textContent, dotHidden: dot.hidden,
           big: (({ left, top, width, height }) => ({ left, top, width, height }))(rect(big)),
           dot: (({ left, top, width, height }) => ({ x: left + width / 2, y: top + height / 2 }))(rect(dot)),
           panel: (({ left, top }) => ({ left, top }))(rect(panel)),
           steps: (({ top, right, bottom }) => ({ top, right, bottom }))(rect(card.querySelector(".stepl"))) };
}));
const thumbSize = (page) => page.evaluate(() => {
  const thumb = document.querySelector(".op-thumb").getBoundingClientRect(), image = document.querySelector(".op-thumb img").getBoundingClientRect();
  return { width: thumb.width, height: thumb.height, image: image.width };
});

const checks = [];
function expect(name, actual, wanted) {
  const ok = typeof wanted === "function" ? wanted(actual) : JSON.stringify(actual) === JSON.stringify(wanted);
  checks.push({ name, ok, actual });
}

(async () => {
  const example = serve(path.join(work, "example")), fold = serve(path.join(work, "fold"));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); });
  page.on("pageerror", (problem) => errors.push(String(problem)));
  try {
    if (condition === "구조-02") {
      await waitUp(page, `${example.base}/TC-003-shot-strip/index.html`);
      expect("칸 108×108 · 그림 폭 108", await thumbSize(page), { width: 108, height: 108, image: 108 });
      let [first] = await panels(page);
      expect("큰 화면 보임", first && first.display, "block");
      expect("처음 글줄", first.label, "PGA 브라보를 골라 확인 창을 연다 — 조작 1/3 · ⋯ 버튼 탭");
      expect("단계 목록 오른쪽에 놓임", first, (read) => read.panel.left >= read.steps.right && read.panel.top >= read.steps.top && read.panel.top <= read.steps.bottom);
      await page.locator(".op-thumb").nth(2).hover();
      [first] = await panels(page);
      expect("세 번째에 마우스 → 3/3", first.label, "PGA 브라보를 골라 확인 창을 연다 — 조작 3/3 · \"PGA 브라보\" 탭");
      expect("동그라미 위치 2px 안", { dx: first.dot.x - (first.big.left + 137 / 402 * first.big.width), dy: first.dot.y - (first.big.top + 684 / 874 * first.big.height) },
             (gap) => Math.abs(gap.dx) <= 2 && Math.abs(gap.dy) <= 2);
      await page.mouse.move(5, 5);
      await page.mouse.wheel(0, 300);
      await page.waitForTimeout(300);
      [first] = await panels(page);
      expect("빈 곳 · 스크롤 300 뒤 그대로 3/3", first.label.endsWith("조작 3/3 · \"PGA 브라보\" 탭"), true);
      await page.locator(".op-thumb").first().focus();
      [first] = await panels(page);
      expect("키보드 초점 → 1/3", first.label.endsWith("조작 1/3 · ⋯ 버튼 탭"), true);
      await page.locator(".op-thumb").first().click();
      expect("누르면 확대 창 1/3", await page.evaluate(() => ({ open: document.querySelector("dialog.viewer").open, info: document.querySelector("dialog.viewer .info").textContent })),
             { open: true, info: "조작 1/3 · ⋯ 버튼 탭" });
      await page.screenshot({ path: path.join(work, "follow.png") });
    } else {
      await waitUp(page, `${example.base}/TC-002-appoint-vice-leader/index.html`);
      let read = await panels(page);
      expect("큰 화면 2 개 · 시나리오 3 은 없음", read.map((item) => item !== null), [true, true, false]);
      await page.locator(".scn").nth(1).locator(".op-thumb").hover();
      read = await panels(page);
      expect("시나리오 2 글줄 바뀜", read[1].label, "부방장 임명을 누른다 — 조작 1/1 · \"부방장 임명\" 탭");
      expect("시나리오 1 글줄 그대로", read[0].label, "⋯ 버튼을 누른다 — 조작 1/1 · ⋯ 버튼 탭");
      await page.setViewportSize({ width: 1000, height: 900 });
      read = await panels(page);
      expect("폭 1000 칸 108 · 큰 화면 안 보임", { thumb: await thumbSize(page), display: read[0].display }, { thumb: { width: 108, height: 108, image: 108 }, display: "none" });
      await page.setViewportSize({ width: 390, height: 844 });
      read = await panels(page);
      expect("폭 390 칸 72 · 큰 화면 안 보임 · 넘침 없음", { thumb: await thumbSize(page), display: read[0].display,
             fits: await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth) },
             { thumb: { width: 72, height: 72, image: 72 }, display: "none", fits: true });
      await page.setViewportSize({ width: 1280, height: 900 });
      await page.goto(`${fold.base}/TC-003-fold/index.html`);
      await page.locator("details.more summary").first().click();
      await page.locator("details.more .do li img").first().hover();
      [read] = await panels(page);
      expect("펼친 네 번째 → 4/4 · 동그라미 숨김", { label: read.label.split(" — ")[1], dot: read.dotHidden }, { label: "조작 4/4 · 네 번째 조작", dot: true });
    }
    expect("콘솔 오류 0", errors, []);
  } finally {
    await browser.close();
    example.server.kill();
    fold.server.kill();
  }
  for (const check of checks) console.log(`${check.ok ? "ok  " : "FAIL"} ${check.name} — ${JSON.stringify(check.actual)}`);
  const failed = checks.filter((check) => !check.ok).length;
  console.log(`${failed ? "FAIL" : "PASS"} ${condition} 검사 ${checks.length}개 · 실패 ${failed}개 · 작업 폴더 ${work}`);
  process.exit(failed ? 1 : 0);
})().catch((problem) => { console.log(`FAIL ${condition} 측정 중 오류 — ${problem.message}`); process.exit(2); });
