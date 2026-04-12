---
name: design-test
description: >
  UI 코드와 디자인 토큰을 분석하여 디자인 품질 테스트를 자동 생성한다.
  디자인 토큰 일관성 검증, 접근성 테스트(WCAG 2.2 AA),
  시각 회귀 테스트(Playwright/Storybook), 반응형 레이아웃 검증을 생성한다.
  "디자인 테스트", "접근성 테스트", "시각 회귀 테스트", "토큰 검증",
  "design test", "a11y test", "visual regression" 같은 요청 시 트리거.
  디자인 원칙 가이드는 design-guide, 전수 감사는 design-audit를 사용한다.
argument-hint: "<file-or-directory> [token|a11y|visual|responsive]"
user-invocable: true
---

## Gotchas

1. **스택 감지 없이 테스트 생성 금지** — React/Vue/Svelte/Flutter/HTML 등 프로젝트 프레임워크를 먼저 감지하라. Playwright 테스트를 Flutter 프로젝트에 생성하면 안 된다
2. **WCAG 2.2 AA 기준 미적용 금지** — 접근성 테스트는 반드시 WCAG 2.2 AA를 기준으로 한다. 대비 비율 4.5:1 (본문), 3:1 (큰 텍스트/비텍스트 UI), 터치 타겟 24×24px(AA) / 44×44px(AAA). 출처: design-kit design-audit Gotcha #3
3. **axe-core 룰셋 버전 확인** — `@axe-core/playwright` 또는 `axe-core` 사용 시 프로젝트에 설치된 버전의 룰셋을 확인하라. 메이저 버전 간 룰 차이가 있다
4. **시각 회귀 테스트의 threshold 미설정 금지** — 픽셀 단위 비교는 anti-aliasing, 폰트 렌더링 차이로 false positive가 빈번하다. `maxDiffPixelRatio: 0.01` 같은 threshold 필수
5. **토큰 검증에서 하드코딩 탐지 범위 명확히** — CSS에서 `#ff0000`, `16px`, `400` 같은 raw value가 있다고 무조건 FAIL이 아니다. reset/normalize CSS, 외부 라이브러리 코드는 제외하라
6. **반응형 테스트에서 breakpoint 출처 확인** — 프로젝트의 디자인 시스템에 정의된 breakpoint를 사용하라. 임의로 320/768/1024를 넣지 마라
7. **다크 모드 테스트 누락 금지** — 디자인 토큰에 다크 모드 매핑이 있으면 반드시 양쪽 모드에서 테스트한다. `prefers-color-scheme: dark` 미디어 쿼리 또는 토큰 클래스 전환
8. **Storybook 의존 여부 확인** — 시각 회귀 테스트에 Storybook을 전제하지 마라. Storybook이 없으면 Playwright의 페이지 스크린샷으로 대체한다
9. **APCA 대비 알고리즘은 informational** — WCAG 2.2 AA(4.5:1 WCAG2 공식)가 법적 기준. APCA Lc는 추가 정보 제공용으로만 포함하고 PASS/FAIL 판정 기준으로 쓰지 마라. 출처: design-guide Gotcha #10

## Process

### Step 0: 프로젝트 감지

프로젝트 루트에서 UI 스택과 디자인 시스템을 감지한다:

| 감지 대상 | 스택 | 테스트 도구 |
|-----------|------|-----------|
| `package.json` + React | React | Playwright + axe-core + Storybook (선택) |
| `package.json` + Vue | Vue | Playwright + axe-core |
| `package.json` + Svelte | Svelte | Playwright + axe-core |
| `package.json` + Angular | Angular | Playwright + axe-core |
| `pubspec.yaml` + Flutter | Flutter | → flutter-test 스킬로 리다이렉트 |
| `*.html` (정적 사이트) | HTML/CSS | Playwright + axe-core + pa11y |

추가 감지:
- 디자인 토큰: `**/tokens/**`, `**/theme/**`, `**/design-system/**`, CSS custom properties (`--`)
- Storybook: `.storybook/`, `*.stories.*`
- Tailwind: `tailwind.config.*`
- CSS-in-JS: styled-components, emotion, vanilla-extract

### Step 1: 대상 분석

`$ARGUMENTS`에서 대상과 테스트 유형을 파싱한다.

**유형 미지정 시 자동 추론:**

| 대상 특성 | 테스트 유형 |
|-----------|-----------|
| 토큰 파일, 테마 설정 | token (일관성 검증) |
| 컴포넌트, 페이지 | a11y (접근성) + visual (시각 회귀) |
| 레이아웃, 그리드 | responsive (반응형) |
| 전체 프로젝트 | 모든 유형 |

### Step 2: 기존 패턴 탐색

- 기존 접근성 테스트: `*.a11y.test.*`, axe-core import
- 기존 시각 테스트: `*.visual.test.*`, `__snapshots__/`, `.loki/`
- Playwright 설정: `playwright.config.*`
- Storybook 테스트: `*.stories.*` 존재 여부
- 디자인 토큰 검증: 기존 lint 규칙, stylelint 설정

### Step 3: 토큰 일관성 테스트 생성

디자인 토큰 파일을 분석하여 일관성을 검증하는 테스트를 생성한다.

```typescript
// tests/design/tokens.test.ts
import { describe, it, expect } from 'vitest'
import fs from 'fs'

describe('Design Token Consistency', () => {
  // CSS custom properties 파싱
  const cssContent = fs.readFileSync('src/styles/tokens.css', 'utf-8')
  const tokens = [...cssContent.matchAll(/--([^:]+):\s*([^;]+)/g)]

  it('all color tokens use consistent format (hex/oklch/hsl)', () => {
    const colorTokens = tokens.filter(([, name]) => name.includes('color'))
    const formats = new Set(
      colorTokens.map(([, , value]) => {
        if (value.trim().startsWith('#')) return 'hex'
        if (value.trim().startsWith('oklch')) return 'oklch'
        if (value.trim().startsWith('hsl')) return 'hsl'
        return 'other'
      })
    )
    expect(formats.size).toBeLessThanOrEqual(1)
  })

  it('spacing tokens follow scale (base * multiplier)', () => {
    const spacingTokens = tokens
      .filter(([, name]) => name.includes('spacing'))
      .map(([, , value]) => parseFloat(value))
      .sort((a, b) => a - b)

    for (let i = 1; i < spacingTokens.length; i++) {
      const ratio = spacingTokens[i] / spacingTokens[i - 1]
      expect(ratio).toBeGreaterThan(1)
    }
  })

  it('no hardcoded values in component files', () => {
    const componentCss = fs.readFileSync('src/components/Button.css', 'utf-8')
    const rawColors = [...componentCss.matchAll(/#[0-9a-fA-F]{3,8}/g)]
    const rawPx = [...componentCss.matchAll(/:\s*\d+px/g)]
    // reset, normalize, 외부 라이브러리 파일은 검사 대상에서 제외
    expect(rawColors).toEqual([])
    expect(rawPx).toEqual([])
  })

  it('dark mode tokens cover all light mode tokens', () => {
    const lightNames = tokens
      .filter(([, name]) => !name.includes('dark'))
      .map(([, name]) => name.replace('light-', ''))
    const darkNames = tokens
      .filter(([, name]) => name.includes('dark'))
      .map(([, name]) => name.replace('dark-', ''))
    const missing = lightNames.filter(n => !darkNames.includes(n))
    expect(missing).toEqual([])
  })
})
```

### Step 4: 접근성 테스트 생성

```typescript
// tests/design/a11y.test.ts
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

const pages = [
  { name: 'Home', path: '/' },
  { name: 'Settings', path: '/settings' },
  // Step 1에서 감지된 라우트 목록
]

for (const page of pages) {
  test.describe(`${page.name} Accessibility`, () => {
    test('should pass axe-core WCAG 2.2 AA', async ({ page: p }) => {
      await p.goto(page.path)
      const results = await new AxeBuilder({ page: p })
        .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
        .analyze()
      expect(results.violations).toEqual([])
    })

    test('all interactive elements have accessible names', async ({ page: p }) => {
      await p.goto(page.path)
      const buttons = await p.locator('button, [role="button"]').all()
      for (const btn of buttons) {
        const name = await btn.getAttribute('aria-label')
          ?? await btn.textContent()
        expect(name?.trim()).toBeTruthy()
      }
    })

    test('color contrast meets 4.5:1 ratio', async ({ page: p }) => {
      await p.goto(page.path)
      const results = await new AxeBuilder({ page: p })
        .withRules(['color-contrast'])
        .analyze()
      expect(results.violations).toEqual([])
    })

    test('touch targets are at least 24x24px', async ({ page: p }) => {
      await p.setViewportSize({ width: 375, height: 812 })
      await p.goto(page.path)
      const targets = await p.locator(
        'button, a, input, select, [role="button"], [role="link"]'
      ).all()
      for (const target of targets) {
        const box = await target.boundingBox()
        if (box) {
          expect(box.width).toBeGreaterThanOrEqual(24)
          expect(box.height).toBeGreaterThanOrEqual(24)
        }
      }
    })
  })
}

// 다크 모드 접근성 (토큰에 다크 모드가 있을 때)
test('dark mode passes color contrast', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' })
  await page.goto('/')
  const results = await new AxeBuilder({ page })
    .withRules(['color-contrast'])
    .analyze()
  expect(results.violations).toEqual([])
})
```

### Step 5: 시각 회귀 테스트 생성

```typescript
// tests/design/visual-regression.test.ts
import { test, expect } from '@playwright/test'

const viewports = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
]

const pages = [
  { name: 'Home', path: '/' },
  // Step 1에서 감지된 주요 페이지
]

for (const vp of viewports) {
  for (const pg of pages) {
    test(`${pg.name} - ${vp.name} visual snapshot`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height })
      await page.goto(pg.path)
      await page.waitForLoadState('networkidle')
      await expect(page).toHaveScreenshot(
        `${pg.name}-${vp.name}.png`,
        { maxDiffPixelRatio: 0.01 }
      )
    })
  }
}

// Storybook이 있을 때 — 컴포넌트별 시각 테스트
// Storybook 감지 시에만 이 섹션 생성
```

### Step 6: 반응형 레이아웃 테스트 생성

```typescript
// tests/design/responsive.test.ts
import { test, expect } from '@playwright/test'

// 프로젝트 디자인 시스템의 breakpoint 사용
const breakpoints = [
  { name: 'sm', width: 640 },
  { name: 'md', width: 768 },
  { name: 'lg', width: 1024 },
  { name: 'xl', width: 1280 },
]

test.describe('Responsive Layout', () => {
  for (const bp of breakpoints) {
    test(`no horizontal overflow at ${bp.name} (${bp.width}px)`, async ({ page }) => {
      await page.setViewportSize({ width: bp.width, height: 900 })
      await page.goto('/')
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth)
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth)
      expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2) // 2px tolerance
    })
  }

  test('text remains readable on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await page.goto('/')
    const bodyFontSize = await page.evaluate(() => {
      const body = document.querySelector('body')
      return parseFloat(getComputedStyle(body!).fontSize)
    })
    expect(bodyFontSize).toBeGreaterThanOrEqual(14) // 최소 14px
  })

  test('images are responsive (no fixed width overflow)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await page.goto('/')
    const images = await page.locator('img').all()
    for (const img of images) {
      const box = await img.boundingBox()
      if (box) {
        expect(box.width).toBeLessThanOrEqual(375)
      }
    }
  })
})
```

### Step 7: 실행 검증

생성된 테스트를 실행한다:

| 테스트 유형 | 실행 명령 |
|-----------|----------|
| 토큰 검증 | `npx vitest run tests/design/tokens.test.ts` |
| 접근성 | `npx playwright test tests/design/a11y.test.ts` |
| 시각 회귀 | `npx playwright test tests/design/visual-regression.test.ts --update-snapshots` (첫 실행) |
| 반응형 | `npx playwright test tests/design/responsive.test.ts` |

첫 실행 시 시각 회귀 테스트는 `--update-snapshots`로 기준 스냅샷을 생성한다.
도구 미설치 시 설치 안내를 제시한다:

```bash
npm install -D @playwright/test @axe-core/playwright
npx playwright install chromium
```

### Step 8: 결과 보고

생성된 파일 목록, 테스트 케이스 수, 실행 결과를 사용자에게 제시한다.
CI 파이프라인에 통합하는 방법을 안내한다 (접근성 게이트, 시각 회귀 PR 리뷰 등).

## References

- `../design-guide/references/principle-index.md` — 디자인 원칙 인덱스 (접근성 카테고리 포함)
- `../design-system/references/token-principles.md` — 토큰 설계 원칙
