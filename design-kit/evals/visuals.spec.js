const { test, expect } = require('@playwright/test');
const path = require('path');

const VISUALS_DIR = path.resolve(__dirname, '../../docs/design/visuals');
const viewports = {
  mobile: { width: 375, height: 812 },
  tablet: { width: 768, height: 1024 },
  desktop: { width: 1440, height: 900 },
};

function fileUrl(filename) {
  // Convert Windows path to file:// URL
  const filePath = path.join(VISUALS_DIR, filename);
  return 'file:///' + filePath.replace(/\\/g, '/');
}

// ============================================================
// color-palette.html
// ============================================================
test.describe('color-palette.html', () => {
  test.describe('Page Load & Structure', () => {
    test('loads without console errors', async ({ page }) => {
      const errors = [];
      page.on('pageerror', (err) => errors.push(err.message));
      await page.goto(fileUrl('color-palette.html'));
      await page.waitForLoadState('domcontentloaded');
      expect(errors).toEqual([]);
    });

    test('all sections render', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      const sections = ['Primary', 'Secondary', 'Surface', 'Semantic'];
      for (const s of sections) {
        await expect(page.locator('.section-title', { hasText: s }).first()).toBeVisible();
      }
      await expect(page.locator('.contrast-section')).toBeVisible();
    });

    test('title and headings are visible', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      await expect(page.locator('h1')).toBeVisible();
      await expect(page.locator('h1')).toHaveText('시맨틱 컬러 팔레트');
    });
  });

  test.describe('Mobile Responsiveness', () => {
    for (const [name, vp] of Object.entries(viewports)) {
      test(`no horizontal overflow at ${name} (${vp.width}px)`, async ({ page }) => {
        await page.setViewportSize(vp);
        await page.goto(fileUrl('color-palette.html'));
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
        expect(overflow).toBe(false);
      });
    }

    test('touch targets >= 44px on mobile', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto(fileUrl('color-palette.html'));
      const toggle = page.locator('.theme-toggle');
      const box = await toggle.boundingBox();
      expect(box.height).toBeGreaterThanOrEqual(44);
    });

    test('content readable at each breakpoint', async ({ page }) => {
      for (const [, vp] of Object.entries(viewports)) {
        await page.setViewportSize(vp);
        await page.goto(fileUrl('color-palette.html'));
        await expect(page.locator('h1')).toBeVisible();
        await expect(page.locator('.color-card').first()).toBeVisible();
      }
    });
  });

  test.describe('Interactive Elements', () => {
    test('light/dark mode toggle switches colors', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      // Default is dark mode - body has no data-theme attribute
      let theme = await page.locator('body').getAttribute('data-theme');
      expect(theme).toBeNull();

      // Click toggle to switch to light
      await page.click('.theme-toggle');
      theme = await page.locator('body').getAttribute('data-theme');
      expect(theme).toBe('light');
      await expect(page.locator('#themeLabel')).toHaveText('라이트 모드');

      // Toggle back to dark
      await page.click('.theme-toggle');
      theme = await page.locator('body').getAttribute('data-theme');
      expect(theme).toBeNull();
      await expect(page.locator('#themeLabel')).toHaveText('다크 모드');
    });

    test('contrast ratio calculator computes correctly (white on black ~ 21:1)', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));

      // Set foreground to white and background to black
      await page.evaluate(() => {
        document.getElementById('fgColor').value = '#ffffff';
        document.getElementById('fgHex').value = '#ffffff';
        document.getElementById('bgColor').value = '#000000';
        document.getElementById('bgHex').value = '#000000';
        updateContrast();
      });

      const ratioText = await page.locator('#ratioValue').textContent();
      // White on black should be 21.0:1
      expect(ratioText).toBe('21.0:1');
    });

    test('contrast badges update based on ratio', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));

      // White on black -- all badges should pass
      await page.evaluate(() => {
        document.getElementById('fgColor').value = '#ffffff';
        document.getElementById('fgHex').value = '#ffffff';
        document.getElementById('bgColor').value = '#000000';
        document.getElementById('bgHex').value = '#000000';
        updateContrast();
      });

      const passBadges = await page.locator('.badge.pass').count();
      expect(passBadges).toBe(4);
    });

    test('contrast checker inputs accept values', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      const fgHex = page.locator('#fgHex');
      await fgHex.fill('#ff0000');
      await fgHex.dispatchEvent('input');
      // The ratio should update (it won't be the default anymore)
      const ratioText = await page.locator('#ratioValue').textContent();
      expect(ratioText).toMatch(/^\d+\.\d+:1$/);
    });

    test('copy to clipboard: toast element exists', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      await expect(page.locator('#copyToast')).toBeAttached();
    });

    test('preview box updates colors based on inputs', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      await page.evaluate(() => {
        document.getElementById('fgColor').value = '#ff0000';
        document.getElementById('fgHex').value = '#ff0000';
        document.getElementById('bgColor').value = '#00ff00';
        document.getElementById('bgHex').value = '#00ff00';
        updateContrast();
      });
      const bgColor = await page.locator('#previewBox').evaluate((el) => el.style.background);
      expect(bgColor).toBe('rgb(0, 255, 0)');
    });
  });

  test.describe('Visual Regression Basics', () => {
    test('dark theme background color applied', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      const bg = await page.locator('body').evaluate((el) => getComputedStyle(el).getPropertyValue('--bg'));
      expect(bg.trim()).toBe('#0d0f14');
    });

    test('light theme CSS variables applied after toggle', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      await page.click('.theme-toggle');
      const bg = await page.locator('body').evaluate((el) => getComputedStyle(el).getPropertyValue('--bg'));
      expect(bg.trim()).toBe('#f0f2f7');
    });

    test('color cards have rounded borders', async ({ page }) => {
      await page.goto(fileUrl('color-palette.html'));
      const radius = await page.locator('.color-card').first().evaluate((el) => getComputedStyle(el).borderRadius);
      expect(radius).toBe('14px');
    });
  });
});

// ============================================================
// typography-scale.html
// ============================================================
test.describe('typography-scale.html', () => {
  test.describe('Page Load & Structure', () => {
    test('loads without console errors', async ({ page }) => {
      const errors = [];
      page.on('pageerror', (err) => errors.push(err.message));
      await page.goto(fileUrl('typography-scale.html'));
      await page.waitForLoadState('domcontentloaded');
      expect(errors).toEqual([]);
    });

    test('all sections render', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      for (const s of ['스케일 설정', 'MD3 타입 스케일', '행간', '반응형 타이포그래피']) {
        await expect(page.locator('.section-title', { hasText: s }).first()).toBeVisible();
      }
    });

    test('title is visible', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      await expect(page.locator('h1')).toHaveText('타이포그래피 스케일');
    });
  });

  test.describe('Mobile Responsiveness', () => {
    for (const [name, vp] of Object.entries(viewports)) {
      test(`no horizontal overflow at ${name} (${vp.width}px)`, async ({ page }) => {
        await page.setViewportSize(vp);
        await page.goto(fileUrl('typography-scale.html'));
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
        expect(overflow).toBe(false);
      });
    }

    test('content readable at each breakpoint', async ({ page }) => {
      for (const [, vp] of Object.entries(viewports)) {
        await page.setViewportSize(vp);
        await page.goto(fileUrl('typography-scale.html'));
        await expect(page.locator('h1')).toBeVisible();
        await expect(page.locator('.scale-row').first()).toBeVisible();
      }
    });
  });

  test.describe('Interactive Elements', () => {
    test('base size slider changes rendered text sizes', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));

      // Get initial display value
      const initialDisplay = await page.locator('#baseDisplay').textContent();
      expect(initialDisplay).toBe('16px');

      // Change slider value
      await page.evaluate(() => {
        const slider = document.getElementById('baseSize');
        slider.value = '20';
        renderScale();
      });
      const updatedDisplay = await page.locator('#baseDisplay').textContent();
      expect(updatedDisplay).toBe('20px');

      // Scale sizes should have changed
      const firstSize = await page.locator('.scale-size').first().textContent();
      // With base=20 and ratio=1.333, Display Large (step=5) = 20 * 1.333^5 ~ 84
      expect(parseInt(firstSize)).toBeGreaterThan(16);
    });

    test('all 15 MD3 type scale levels are displayed', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      const rowCount = await page.locator('.scale-row').count();
      // md3Roles has 15 entries
      expect(rowCount).toBe(15);
    });

    test('scale ratio selector updates ratio badge', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      await page.selectOption('#scaleRatio', '1.618');
      const badgeText = await page.locator('#currentRatio').textContent();
      expect(badgeText).toBe('x1.618');
    });
  });

  test.describe('Line Height Visualization', () => {
    test('line height samples are visible', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      for (const id of ['lhTight', 'lhNormal', 'lhLoose', 'lhExtraLoose']) {
        const el = page.locator(`#${id}`);
        await expect(el).not.toBeEmpty();
      }
    });

    test('line height values match specification', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      const tightLH = await page.locator('#lhTight p').evaluate((el) => getComputedStyle(el).lineHeight);
      // 15px * 1.2 = 18px
      expect(parseFloat(tightLH)).toBeCloseTo(18, 0);
    });
  });

  test.describe('Visual Regression Basics', () => {
    test('dark theme background applied', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      const bg = await page.locator('body').evaluate((el) => getComputedStyle(el).getPropertyValue('--bg'));
      expect(bg.trim()).toBe('#0d0f14');
    });

    test('accent color is correct', async ({ page }) => {
      await page.goto(fileUrl('typography-scale.html'));
      const accent = await page.locator('body').evaluate((el) => getComputedStyle(el).getPropertyValue('--accent'));
      expect(accent.trim()).toBe('#5b8def');
    });
  });
});

// ============================================================
// spacing-system.html
// ============================================================
test.describe('spacing-system.html', () => {
  test.describe('Page Load & Structure', () => {
    test('loads without console errors', async ({ page }) => {
      const errors = [];
      page.on('pageerror', (err) => errors.push(err.message));
      await page.goto(fileUrl('spacing-system.html'));
      await page.waitForLoadState('domcontentloaded');
      expect(errors).toEqual([]);
    });

    test('all sections render', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      for (const s of ['4px 베이스 그리드', '간격 토큰', '간격 스케일 시각화', '터치 타겟 크기 비교', '실전 간격 패턴']) {
        await expect(page.locator('.section-title', { hasText: s }).first()).toBeVisible();
      }
    });

    test('title is visible', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      await expect(page.locator('h1')).toHaveText('간격 시스템');
    });
  });

  test.describe('Mobile Responsiveness', () => {
    for (const [name, vp] of Object.entries(viewports)) {
      test(`no horizontal overflow at ${name} (${vp.width}px)`, async ({ page }) => {
        await page.setViewportSize(vp);
        await page.goto(fileUrl('spacing-system.html'));
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
        expect(overflow).toBe(false);
      });
    }

    test('touch targets >= 44px on mobile', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto(fileUrl('spacing-system.html'));
      // Touch cards should be tappable
      const card = page.locator('.touch-card').first();
      const box = await card.boundingBox();
      expect(box.height).toBeGreaterThanOrEqual(44);
    });
  });

  test.describe('Interactive Elements', () => {
    test('all spacing tokens are displayed (3xs through 4xl)', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      const expectedTokens = ['3xs', '2xs', 'xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl', '4xl'];
      for (const token of expectedTokens) {
        await expect(page.locator('.token-name', { hasText: new RegExp(`^${token.replace('+', '\\+')}$`) }).first()).toBeVisible();
      }
    });

    test('token values match specification', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      const tokenData = await page.evaluate(() => {
        const rows = document.querySelectorAll('.token-row');
        return Array.from(rows).map((row) => ({
          name: row.querySelector('.token-name').textContent.trim(),
          value: row.querySelector('.token-value').textContent.trim(),
        }));
      });

      const expected = {
        '3xs': '2px', '2xs': '4px', 'xs': '8px', 'sm': '12px', 'md': '16px',
        'lg': '24px', 'xl': '32px', '2xl': '48px', '3xl': '64px', '4xl': '96px',
      };

      for (const row of tokenData) {
        if (expected[row.name]) {
          expect(row.value).toBe(expected[row.name]);
        }
      }
    });

    test('touch target comparison elements exist', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      const cardCount = await page.locator('.touch-card').count();
      expect(cardCount).toBe(3);
      // Check the three standards
      await expect(page.locator('.touch-card-title', { hasText: 'Apple iOS' })).toBeVisible();
      await expect(page.locator('.touch-card-title', { hasText: 'Material Design' })).toBeVisible();
      await expect(page.locator('.touch-card-title', { hasText: 'WCAG 2.2' })).toBeVisible();
    });

    test('touch card toggle works', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      const firstCard = page.locator('.touch-card').first();
      await firstCard.click();
      await expect(firstCard).toHaveClass(/active/);

      // Click again to deactivate
      await firstCard.click();
      await expect(firstCard).not.toHaveClass(/active/);
    });
  });

  test.describe('Visual Regression Basics', () => {
    test('dark theme background applied', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      const bg = await page.locator('body').evaluate((el) => getComputedStyle(el).getPropertyValue('--bg'));
      expect(bg.trim()).toBe('#0d0f14');
    });

    test('token bars have gradient background', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      const bg = await page.locator('.token-bar').first().evaluate((el) => getComputedStyle(el).backgroundImage);
      expect(bg).toContain('linear-gradient');
    });

    test('scale visualization blocks exist for all tokens', async ({ page }) => {
      await page.goto(fileUrl('spacing-system.html'));
      const blockCount = await page.locator('.scale-block').count();
      expect(blockCount).toBe(10); // 10 tokens
    });
  });
});

// ============================================================
// ratio-proportion.html
// ============================================================
test.describe('ratio-proportion.html', () => {
  test.describe('Page Load & Structure', () => {
    test('loads without console errors', async ({ page }) => {
      const errors = [];
      page.on('pageerror', (err) => errors.push(err.message));
      await page.goto(fileUrl('ratio-proportion.html'));
      await page.waitForLoadState('domcontentloaded');
      expect(errors).toEqual([]);
    });

    test('all sections render', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      for (const s of ['황금비 그리드', '3분할 법칙', '모듈러 스케일 계산기', '화면 비율 비교']) {
        await expect(page.locator('.section-title', { hasText: s }).first()).toBeVisible();
      }
    });

    test('title is visible', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      await expect(page.locator('h1')).toHaveText('비율과 프로포션');
    });
  });

  test.describe('Mobile Responsiveness', () => {
    for (const [name, vp] of Object.entries(viewports)) {
      test(`no horizontal overflow at ${name} (${vp.width}px)`, async ({ page }) => {
        await page.setViewportSize(vp);
        await page.goto(fileUrl('ratio-proportion.html'));
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
        expect(overflow).toBe(false);
      });
    }

    test('golden ratio buttons are tappable on mobile (>= 44px)', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto(fileUrl('ratio-proportion.html'));
      const btn = page.locator('.golden-controls button').first();
      const box = await btn.boundingBox();
      expect(box.height).toBeGreaterThanOrEqual(44);
    });
  });

  test.describe('Interactive Elements - Golden Ratio', () => {
    test('golden ratio mode buttons switch display', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));

      // Default is spiral -- the first button should be active
      await expect(page.locator('.golden-controls button').first()).toHaveClass(/active/);

      // Click grid button
      const gridBtn = page.locator('.golden-controls button', { hasText: '황금 분할 그리드' });
      await gridBtn.click();
      await expect(gridBtn).toHaveClass(/active/);
      // First button should no longer be active
      await expect(page.locator('.golden-controls button').first()).not.toHaveClass(/active/);

      // Click layout button
      const layoutBtn = page.locator('.golden-controls button', { hasText: '2단 레이아웃' });
      await layoutBtn.click();
      await expect(layoutBtn).toHaveClass(/active/);
    });

    test('golden demo renders SVG for spiral mode', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      const svg = page.locator('#goldenDemo svg');
      await expect(svg).toBeVisible();
    });

    test('golden demo renders layout divs for layout mode', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      await page.locator('.golden-controls button', { hasText: '2단 레이아웃' }).click();
      // Layout mode renders divs with "메인 콘텐츠" and "사이드바"
      await expect(page.locator('#goldenDemo', { hasText: '메인 콘텐츠' })).toBeVisible();
      await expect(page.locator('#goldenDemo', { hasText: '사이드바' })).toBeVisible();
    });
  });

  test.describe('Interactive Elements - Modular Scale Calculator', () => {
    test('changing base updates output', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));

      // Get initial base row value
      const initialBaseValue = await page.locator('.scale-row.base .scale-value').textContent();

      // Change base
      await page.evaluate(() => {
        document.getElementById('calcBase').value = '20';
        calcScale();
      });

      const updatedBaseValue = await page.locator('.scale-row.base .scale-value').textContent();
      expect(updatedBaseValue).toBe('20px');
      expect(updatedBaseValue).not.toBe(initialBaseValue);
    });

    test('changing ratio updates output', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));

      const initialValues = await page.locator('.scale-row .scale-value').allTextContents();

      await page.selectOption('#calcRatio', '1.618');
      await page.evaluate(() => calcScale());

      const updatedValues = await page.locator('.scale-row .scale-value').allTextContents();
      expect(updatedValues).not.toEqual(initialValues);
    });

    test('modular scale outputs correct number of steps', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      // Steps from -3 to +8 = 12 rows
      const rowCount = await page.locator('#scaleOutput .scale-row').count();
      expect(rowCount).toBe(12);
    });

    test('base step is highlighted', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      await expect(page.locator('.scale-row.base')).toBeVisible();
      const baseStep = await page.locator('.scale-row.base .scale-step').textContent();
      expect(baseStep.trim()).toBe('+0');
    });
  });

  test.describe('Interactive Elements - Aspect Ratios', () => {
    test('aspect ratio cards display all variants', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      const expectedRatios = ['16:9', '4:3', '1:1', '3:2', '21:9', '9:16', '2:3', '1.91:1'];
      const allBoxTexts = await page.locator('.ratio-box').allTextContents();
      for (const ratio of expectedRatios) {
        expect(allBoxTexts).toContain(ratio);
      }
    });

    test('all 8 aspect ratio cards are rendered', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      const cardCount = await page.locator('.ratio-card').count();
      expect(cardCount).toBe(8);
    });

    test('ratio detail shows decimal value', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      // 16:9 = 1.778:1
      const detail = await page.locator('.ratio-card').first().locator('.ratio-detail').textContent();
      expect(detail).toMatch(/1\.778\s*:\s*1/);
    });
  });

  test.describe('Visual Regression Basics', () => {
    test('dark theme background applied', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      const bg = await page.locator('body').evaluate((el) => getComputedStyle(el).getPropertyValue('--bg'));
      expect(bg.trim()).toBe('#0d0f14');
    });

    test('golden color variable is set', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      const gold = await page.locator('body').evaluate((el) => getComputedStyle(el).getPropertyValue('--gold'));
      expect(gold.trim()).toBe('#f0c040');
    });

    test('card surfaces have expected background', async ({ page }) => {
      await page.goto(fileUrl('ratio-proportion.html'));
      const surface = await page.locator('.card').first().evaluate((el) => getComputedStyle(el).getPropertyValue('background-color'));
      // --surface: #181b26 = rgb(24, 27, 38)
      expect(surface).toBe('rgb(24, 27, 38)');
    });
  });
});
