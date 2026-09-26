// /api-ui 로 만든 예시 ui.html 이 네 상태(PASS · FAIL · 미실행 · 판정 불가)를 칸마다 맞게 보이는지 본다.
// 기대값은 evals.json 의 expect 에서, 칩 숫자 · 트리 줄 수를 세는 식은 SKILL.md §7 에서 그대로 읽는다 — 식의 사본을 두지 않는다.
const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const SKILL_PATH = path.resolve(__dirname, '../skills/api-ui/SKILL.md');
const EVALS = JSON.parse(fs.readFileSync(path.join(__dirname, 'evals.json'), 'utf8'));
const LABELS = ['PASS', 'FAIL', '미실행', '판정 불가'];
const UNJUDGED = '판정 불가';
const UNJUDGED_LINE = /\(없음\).*→ 판정 불가/;
const COMBOS = [
  { width: 1280, height: 720, colorScheme: 'light' },
  { width: 1280, height: 720, colorScheme: 'dark' },
  { width: 375, height: 812, colorScheme: 'light' },
  { width: 375, height: 812, colorScheme: 'dark' },
];

function sectionSevenExpr() {
  const text = fs.readFileSync(SKILL_PATH, 'utf8');
  const block = text.slice(text.indexOf('\n## 7.')).match(/```js\n([\s\S]*?)\n```/);
  if (!block) throw new Error('SKILL.md ## 7. 절에 js 코드 블록이 없다');
  return block[1];
}

function watchErrors(page) {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error' && !/favicon\.ico/.test(msg.text())) errors.push(msg.text()); });
  page.on('pageerror', err => errors.push(err.message));
  return errors;
}

for (const evalCase of EVALS.cases.filter(item => item.skill === 'api-ui')) {
  const url = 'file://' + path.join(__dirname, evalCase.example);

  for (const combo of COMBOS) {
    test.describe(`${evalCase.id} ${combo.width}-${combo.colorScheme}`, () => {
      test.use({ viewport: { width: combo.width, height: combo.height }, colorScheme: combo.colorScheme });

      test('칩 숫자와 트리 줄 수가 상태마다 expect 와 같다', async ({ page }) => {
        const errors = watchErrors(page);
        await page.goto(url);
        await expect(page.locator('html')).toHaveAttribute('data-theme', combo.colorScheme);
        const measured = await page.evaluate(sectionSevenExpr());
        for (const label of LABELS) {
          expect(measured.chips[label], `칩 ${label}`).toBe(evalCase.expect[label]);
          expect(measured.rows[label], `트리 ${label}`).toBe(evalCase.expect[label]);
          const chip = page.locator('header').getByRole('button', { name: label });
          await expect(chip).toHaveCount(1);
          await expect(chip).toBeVisible();
        }
        if (combo.width === 1280) {
          expect(measured.shown).toBe(measured.ep);
          expect(measured.under24).toBe(0);
        }
        expect(errors).toEqual([]);
      });

      if (combo.width !== 1280) return;

      test('판정 불가 칩을 누르면 판정 불가 줄만 남고 다시 누르면 돌아온다', async ({ page }) => {
        await page.goto(url);
        const chip = page.locator('header').getByRole('button', { name: UNJUDGED });
        const shownRows = page.locator('[data-ep]:visible');
        const total = await shownRows.count();
        await chip.click();
        await expect(chip).toHaveAttribute('aria-pressed', 'true');
        await expect(shownRows).toHaveCount(evalCase.expect[UNJUDGED]);
        for (const row of await shownRows.all()) await expect(row).toContainText(UNJUDGED);
        await chip.click();
        await expect(shownRows).toHaveCount(total);
      });

      test('판정 불가 줄은 맨 앞 탭에 글자 그대로 있고, 그 줄을 가진 FAIL 수가 expect 와 같다', async ({ page }) => {
        await page.goto(url);
        const failTab = page.getByRole('tab', { name: '실패 원인' });
        const unjudgedLine = page.getByText(UNJUDGED_LINE);
        for (const row of await page.locator('[data-ep]', { hasText: UNJUDGED }).all()) {
          await row.click();
          await expect(failTab).toHaveCount(0);
          await expect(unjudgedLine.first()).toBeVisible();
        }
        let failWithUnjudged = 0;
        for (const row of await page.locator('[data-ep]', { hasText: 'FAIL' }).all()) {
          await row.click();
          await expect(failTab).toHaveAttribute('aria-selected', 'true');
          if (await unjudgedLine.first().isVisible()) failWithUnjudged += 1;
        }
        expect(failWithUnjudged).toBe(evalCase.expect.fail_with_unjudged);
      });
    });
  }
}
