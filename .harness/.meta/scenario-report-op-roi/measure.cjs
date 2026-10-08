// 구조-02 · 구조-03 브라우저 측정. 사용: node measure.cjs <조건 번호> <작업 폴더> <playwright 모듈 경로>
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

const state = (page) => page.evaluate(async () => {
  const viewer = document.querySelector("dialog.viewer"), big = viewer.querySelector(".stage img"), dot = viewer.querySelector(".stage .tap");
  if (!big.complete) await new Promise((done) => { big.onload = done; });
  await new Promise((done) => requestAnimationFrame(done));
  return { open: viewer.open, info: viewer.querySelector(".info").textContent, prevHidden: viewer.querySelector(".prev").hidden,
           nextHidden: viewer.querySelector(".next").hidden, dotHidden: dot.hidden,
           big: (({ left, top, width, height }) => ({ left, top, width, height }))(big.getBoundingClientRect()),
           dot: (({ left, top, width, height }) => ({ x: left + width / 2, y: top + height / 2 }))(dot.getBoundingClientRect()) };
});

function offset(read, x, y, width, height) {
  return { dx: read.dot.x - (read.big.left + x / width * read.big.width), dy: read.dot.y - (read.big.top + y / height * read.big.height) };
}

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
  const close = () => page.evaluate(() => document.querySelector("dialog.viewer").close());
  try {
    await waitUp(page, `${example.base}/TC-003-shot-strip/index.html`);
    if (condition === "구조-02") {
      const first = page.locator(".op-thumb").first();
      await first.click();
      let read = await state(page);
      expect("열림", read.open, true);
      expect("표시 1/3", read.info, "조작 1/3 · ⋯ 버튼 탭");
      expect("이전 숨김", read.prevHidden, true);
      expect("다음 보임", read.nextHidden, false);
      expect("동그라미 보임", read.dotHidden, false);
      expect("첫 클릭 위치 2px 안", offset(read, 362, 81, 402, 874), (gap) => Math.abs(gap.dx) <= 2 && Math.abs(gap.dy) <= 2);
      await page.screenshot({ path: path.join(work, "viewer.png") });
      await page.keyboard.press("ArrowRight");
      await page.keyboard.press("ArrowRight");
      read = await state(page);
      expect("→ 두 번 3/3", read.info, "조작 3/3 · \"PGA 브라보\" 탭");
      expect("끝에서 다음 숨김", read.nextHidden, true);
      await page.keyboard.press("ArrowLeft");
      read = await state(page);
      expect("← 한 번 2/3", read.info, "조작 2/3 · \"방장 넘기기\" 탭");
      await page.keyboard.press("Escape");
      expect("Esc 닫힘 · 초점 복귀", await page.evaluate(() => ({ open: document.querySelector("dialog.viewer").open,
        focus: document.activeElement === document.querySelectorAll(".op-thumb")[0] })), { open: false, focus: true });
      await first.click();
      read = await state(page);
      expect("두 번째 클릭 위치 2px 안", offset(read, 362, 81, 402, 874), (gap) => Math.abs(gap.dx) <= 2 && Math.abs(gap.dy) <= 2);
      await close();
    } else {
      await page.locator(".shots img").nth(1).click();
      let read = await state(page);
      expect("사진 2/5", read.info, "사진 2/5 · 그룹 고르는 창");
      expect("사진 동그라미 숨김", read.dotHidden, true);
      await close();
      for (const key of ["Enter", "Space"]) {
        await page.locator(".op-thumb").first().focus();
        await page.keyboard.press(key);
        expect(`${key} 로 열림`, await page.evaluate(() => document.querySelector("dialog.viewer").open), true);
        await close();
      }
      await page.goto(`${example.base}/TC-002-appoint-vice-leader/index.html`);
      await page.locator(".op-thumb").first().click();
      read = await state(page);
      expect("한 장 묶음 1/1", read.info, "조작 1/1 · ⋯ 버튼 탭");
      expect("한 장 묶음 버튼 둘 다 숨김", [read.prevHidden, read.nextHidden], [true, true]);
      await close();
      await page.locator(".zoom img").click();
      read = await state(page);
      expect("확대 사진 표시", read.info, "확대 · 잘린 제목");
      expect("확대 사진 버튼 · 동그라미 숨김", [read.prevHidden, read.nextHidden, read.dotHidden], [true, true, true]);
      await close();
      await page.goto(`${fold.base}/TC-003-fold/index.html`);
      await page.locator(".op-thumb").first().click();
      for (let step = 0; step < 3; step++) await page.keyboard.press("ArrowRight");
      read = await state(page);
      expect("접힌 조작 4/4", read.info, "조작 4/4 · 네 번째 조작");
      expect("좌표 없는 조작 동그라미 숨김", read.dotHidden, true);
      await close();
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(`${example.base}/TC-003-shot-strip/index.html`);
      expect("390 폭 칸 72×72 · 가로 넘침 없음", await page.evaluate(() => {
        const box = document.querySelector(".op-thumb").getBoundingClientRect();
        return { width: box.width, height: box.height, fits: document.documentElement.scrollWidth <= innerWidth };
      }), { width: 72, height: 72, fits: true });
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
