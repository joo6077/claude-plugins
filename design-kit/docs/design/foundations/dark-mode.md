# Dark / Light Mode

design-kit HTML 산출물 템플릿에 적용할 다크/라이트 모드 패턴.

## CSS 변수 기반 테마 전환

`data-theme` 속성 + `prefers-color-scheme` 조합. 우선순위: localStorage → 시스템 설정 → 기본값(라이트).

```css
:root {
  --color-bg: #ffffff;
  --color-surface: #f5f5f5;
  --color-surface-high: #eeeeee;
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #666666;
  --color-border: #e0e0e0;
  --color-shadow: rgba(0, 0, 0, 0.08);
  --color-accent: #1a73e8;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg: #121212;
    --color-surface: #1e1e1e;
    --color-surface-high: #2a2a2a;
    --color-text-primary: #e8e8e8;
    --color-text-secondary: #aaaaaa;
    --color-border: #333333;
    --color-shadow: rgba(0, 0, 0, 0.4);
    --color-accent: #82b4ff;
  }
}

[data-theme="dark"] {
  --color-bg: #121212;
  --color-surface: #1e1e1e;
  --color-surface-high: #2a2a2a;
  --color-text-primary: #e8e8e8;
  --color-text-secondary: #aaaaaa;
  --color-border: #333333;
  --color-shadow: rgba(0, 0, 0, 0.4);
  --color-accent: #82b4ff;
}
```

## 색상 체계

MD3 + Apple HIG 기반. 단순 반전이 아닌 역할별 독립 설계.

| 역할 | 라이트 | 다크 | 비고 |
|------|--------|------|------|
| bg | `#ffffff` | `#121212` | #000 사용 금지 |
| surface | `#f5f5f5` | `#1e1e1e` | 카드/패널 배경 |
| surface-high | `#eeeeee` | `#2a2a2a` | 높은 elevation |
| text-primary | `#1a1a1a` | `#e8e8e8` | #fff 사용 금지 |
| text-secondary | `#666666` | `#aaaaaa` | |
| border | `#e0e0e0` | `#333333` | |
| shadow | `rgba(0,0,0,0.08)` | `rgba(0,0,0,0.4)` | |
| accent | `#1a73e8` | `#82b4ff` | 밝기 올림 |

다크모드에서 elevation은 그림자 대신 tonal overlay(더 밝은 surface)로 표현.

## 토글 구현

최소 JS 패턴 (standalone HTML 권장):

```js
const saved = localStorage.getItem('theme')
  ?? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
document.documentElement.dataset.theme = saved;

function toggleTheme() {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
}
```

## 이미지/미디어 대응

- 일반 이미지: 다크모드에서 `filter: brightness(0.85)`
- SVG inline: `fill: currentColor`로 CSS 변수 자동 전환
- 사진 배경: `opacity: 0.8` 또는 다크 오버레이

## 접근성

- 일반 텍스트: 최소 4.5:1 대비율 (WCAG AA)
- 대형 텍스트 (18px+): 최소 3:1
- 포커스 링: `outline: 2px solid var(--color-accent)` — 배경과 3:1 이상
- 상태 색상: 색상에만 의존 금지, 아이콘/텍스트 병행

## 안티패턴

| 안티패턴 | 문제점 |
|----------|--------|
| `#fff` → `#000` 단순 반전 | 보더/그림자/이미지 깨짐 |
| 순수 검정(`#000`) 배경 | 할레이션(halo) 효과, 눈 피로 |
| 고채도 색상 그대로 사용 | 어두운 배경에서 색 진동 |
| CSS 변수 미사용 | 전환 불가, 유지보수 폭증 |
| 시스템 설정 무시 | 다크모드 OS 사용자 불편 |

## Sources

- Material Design 3 Color Roles
- Apple HIG Dark Mode
- WCAG 2.1 Contrast Requirements
