# CSS Token System — Claude Plugins Documentation

## 공통 기본 토큰 (모든 페이지)

```css
:root {
  /* Background */
  --bg:#0d0d14;--bg2:#12121c;
  /* Surface */
  --surface:#181825;--surface2:#1e1e30;
  /* Border */
  --border:#2a2a40;
  /* Text (warm tint) */
  --text:#F5F0E8;--text2:#A89A8F;--text3:#7A6F64;
  /* Semantic */
  --green:#4ade80;--red:#f87171;--yellow:#fbbf24;
  /* System */
  --radius:14px;--transition:0.25s cubic-bezier(.4,0,.2,1);
  --mono:'SF Mono','Cascadia Code','Consolas',monospace;
}
```

## 플러그인별 Accent 매핑

| 플러그인 | `--accent` | `--accent2` | `--accent-dim` | 배경 gradient rgba |
|----------|-----------|-------------|----------------|---------------------|
| **Harness** | `#D97757` | `#E8A583` | `rgba(217,119,87,0.12)` | `rgba(217,119,87,0.06)` |
| **Flutter Toolkit** | `#22D3EE` | `#67E8F9` | `rgba(34,211,238,0.12)` | `rgba(34,211,238,0.06)` |
| **Design Kit** | `#E8965A` | `#F0B088` | `rgba(232,150,90,0.12)` | `rgba(232,150,90,0.06)` |
| **Backend Kit** | `#A78BFA` | `#C4B5FD` | `rgba(167,139,250,0.12)` | `rgba(167,139,250,0.06)` |
| **Infra Kit** | `#34D399` | `#6EE7B7` | `rgba(52,211,153,0.12)` | `rgba(52,211,153,0.06)` |
| **Rust Kit** | `#E85D4A` | `#F08575` | `rgba(232,93,74,0.12)` | `rgba(232,93,74,0.06)` |
| **React Kit** | `#38BDF8` | `#7DD3FC` | `rgba(56,189,248,0.12)` | `rgba(56,189,248,0.06)` |
| **Planning Kit** | `#EC4899` | `#F9A8D4` | `rgba(236,72,153,0.12)` | `rgba(236,72,153,0.06)` |
| **Process** | `#4ADE80` | `#86EFAC` | `rgba(74,222,128,0.12)` | `rgba(74,222,128,0.06)` |
| **Index (허브)** | `#D97757` | `#E8A583` | `rgba(217,119,87,0.12)` | — |

## 사용 규칙

1. 기본 토큰(bg, surface, border, text, radius)은 **모든 페이지에서 동일**
2. accent 계열만 플러그인별로 변경
3. `body` 배경 gradient에 해당 플러그인의 rgba 값 사용:
   ```css
   body {
     background-image:
       radial-gradient(ellipse at 20% 0%, {accent-gradient-rgba} 0%, transparent 50%),
       radial-gradient(ellipse at 80% 100%, {accent-gradient-rgba-dimmer} 0%, transparent 50%);
   }
   ```
4. `h1` gradient: `linear-gradient(135deg, var(--text), var(--accent))`
5. `.section-label` 색상: `var(--accent)`
6. `.card:hover` 보더: `rgba({accent-r},{accent-g},{accent-b},0.25)`
