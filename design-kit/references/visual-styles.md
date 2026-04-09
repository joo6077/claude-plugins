# Visual Styles Reference

35종 비주얼 스타일 구조화 데이터. design-concept, design-mockup 스킬이 스타일 요청 시 참조.
속성이 레이어로 분리되어 있어 조합 가능 (예: "Swiss 구조 + Cyberpunk 컬러").

## 속성 레이어 설명

- **structure**: border-radius, 레이아웃 특성
- **texture**: 그림자, 배경 패턴, blur, 애니메이션
- **color**: 배경, 텍스트, 악센트 색상
- **typography**: 폰트, 굵기, 변형
- **tags**: 검색/분류용 키워드
- **combines-well-with**: 조합 시 잘 어울리는 스타일

---

## Skeuomorphism
- ko: 스큐어모피즘
- structure: { radius: 12px, layout: button-centric }
- texture: { shadow: multi-layer-inset, bg-pattern: multi-stop-gradient }
- color: { bg: "linear-gradient(145deg,#c8c8d0,#a0a0a8)", text: "#3a3a44" }
- typography: { font: system, weight: 700 }
- tags: [tactile, realistic, vintage, 3d-simulation]
- combines-well-with: [Neumorphism, Frutiger-Aero]

## Flat Design
- ko: 플랫 디자인
- structure: { radius: 0, layout: geometric-shapes }
- texture: { shadow: none, bg-pattern: solid-color }
- color: { bg: "#2196F3", text: "#fff", accent: "#FF5722 / #4CAF50 / #FFC107" }
- typography: { font: system, weight: normal }
- tags: [clean, bold-color, no-shadow, geometric]
- combines-well-with: [Material-Design, Corporate-Memphis]

## Flat 2.0
- ko: 플랫 2.0
- structure: { radius: 8px, layout: card-with-icon }
- texture: { shadow: "8px 8px 0 rgba(66,133,244,0.15)", bg-pattern: subtle-gradient }
- color: { bg: "#f0f4f8", accent: "linear-gradient(135deg,#667eea,#764ba2)" }
- typography: { font: system, weight: 600 }
- tags: [semi-flat, long-shadow, subtle-depth]
- combines-well-with: [Flat-Design, Minimalism]

## Material Design
- ko: 머티리얼 디자인
- structure: { radius: 8px, layout: card-elevation }
- texture: { shadow: "0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)", bg-pattern: solid }
- color: { bg: "#FAFAFA", accent: "#6200EE / #03DAC6" }
- typography: { font: system, weight: 600, text-transform: uppercase-labels }
- tags: [elevation, physical-metaphor, google, systematic]
- combines-well-with: [Flat-Design, Dark-Mode]

## Neumorphism
- ko: 뉴모피즘
- structure: { radius: 20px, layout: soft-rounded }
- texture: { shadow: "dual-direction (8px 8px 16px #b8bcc2, -8px -8px 16px #ffffff)", bg-pattern: none }
- color: { bg: "#e0e5ec", text: "#6c7a89", accent: "#6c7a89" }
- typography: { font: system, weight: 500 }
- tags: [soft, tactile, monochromatic, skeuomorphic-revival]
- combines-well-with: [Minimalism, Artificial-Morphism]

## Glassmorphism
- ko: 글래스모피즘
- structure: { radius: 16px, layout: frosted-card }
- texture: { shadow: none, blur: "backdrop-filter:blur(12px)", bg-pattern: translucent-overlay }
- color: { bg: "linear-gradient(135deg,#667eea,#764ba2)", card-bg: "rgba(255,255,255,0.15)", border: "rgba(255,255,255,0.25)" }
- typography: { font: system, weight: 700 }
- tags: [frosted-glass, translucent, blur, layered]
- combines-well-with: [Mesh-Gradient, Aurora-UI, Liquid-Glass]

## Claymorphism
- ko: 클레이모피즘
- structure: { radius: 28px, layout: puffy-card }
- texture: { shadow: "outer + dual-inset (highlight + shadow)", bg-pattern: pastel-gradient }
- color: { bg: "#f8f0ff", card-bg: "linear-gradient(145deg,#e8d5f5,#f3e8ff)", accent: "#d8b4fe" }
- typography: { font: system, weight: 700 }
- tags: [puffy, 3d-plastic, pastel, playful]
- combines-well-with: [Neumorphism, Biomorphism]

## Liquid Glass
- ko: 리퀴드 글래스
- structure: { radius: 20px, layout: dark-frosted-card }
- texture: { shadow: subtle-glow, blur: "backdrop-filter:blur(8px)", animation: shine-sweep }
- color: { bg: "linear-gradient(135deg,#1a1a2e,#16213e,#0f3460)", card-bg: "rgba(255,255,255,0.08)" }
- typography: { font: system, weight: 700 }
- tags: [dark, animated-shine, deep-glass, premium]
- combines-well-with: [Glassmorphism, Spatial-Design, Aurora-UI]

## Artificial Morphism
- ko: 아티피셜 모피즘
- structure: { radius: 16px, layout: hybrid-card }
- texture: { shadow: "dual-direction + border-top highlight", bg-pattern: grid-overlay }
- color: { bg: "#e0e0e8", text: "#555" }
- typography: { font: system, weight: 700 }
- tags: [neumorphic-variant, grid-texture, hybrid, subtle]
- combines-well-with: [Neumorphism, Minimalism]

## Brutalism
- ko: 브루탈리즘
- structure: { radius: 0, layout: raw-block }
- texture: { shadow: none, bg-pattern: solid-background }
- color: { bg: "#ff6b35", text: "#000", accent: "#000 / #ff0" }
- typography: { font: "Courier New, monospace / Georgia, serif", weight: 900, text-transform: uppercase }
- tags: [raw, anti-design, monospace, confrontational]
- combines-well-with: [Neubrutalism, Memphis]

## Neubrutalism
- ko: 뉴브루탈리즘
- structure: { radius: 12px, layout: hard-shadow-card }
- texture: { shadow: "6px 6px 0 #000 (hard offset, no blur)", bg-pattern: solid-pastel }
- color: { bg: "#ffe4e1", card-bg: "#a7f3d0", text: "#000", accent: "#fbbf24" }
- typography: { font: system, weight: 800 }
- tags: [bold-border, hard-shadow, playful, accessible]
- combines-well-with: [Brutalism, Memphis, Bento-Grid]

## Swiss/International
- ko: 스위스/인터내셔널
- structure: { radius: 0, layout: strict-grid }
- texture: { shadow: none, bg-pattern: repeating-grid-lines }
- color: { bg: "#fff", text: "#000", accent: "#FF0000" }
- typography: { font: "Helvetica Neue, Helvetica, Arial", weight: 900, letter-spacing: "-0.04em" }
- tags: [typographic, grid-system, red-accent, structured]
- combines-well-with: [Minimalism, Flat-Design]

## Bento Grid
- ko: 벤토 그리드
- structure: { radius: 12px, layout: multi-span-grid }
- texture: { shadow: none, bg-pattern: gradient-cells }
- color: { bg: "#0d0d14", cells: "#6366f1 / #10b981 / #f59e0b / #ec4899" }
- typography: { font: system, weight: 700 }
- tags: [modular, dashboard, asymmetric-grid, colorful]
- combines-well-with: [Dark-Mode, Material-Design]

## Maximalism
- ko: 맥시멀리즘
- structure: { radius: 20px, layout: overlapping-elements }
- texture: { shadow: none, bg-pattern: animated-multi-gradient, animation: bg-position-infinite }
- color: { bg: "multi-color gradient (#ff006e,#fb5607,#ffbe0b,#06d6a0,#118ab2)", text: "#fff" }
- typography: { font: "Impact / Georgia", weight: 900, style: italic-mix }
- tags: [loud, animated, multi-color, maximalist]
- combines-well-with: [Memphis, Vaporwave]

## Minimalism
- ko: 미니멀리즘
- structure: { radius: 2px, layout: centered-sparse }
- texture: { shadow: none, bg-pattern: hairline-border-only }
- color: { bg: "#fafafa", text: "#222", label: "#999" }
- typography: { font: "Helvetica Neue", weight: 200-300, letter-spacing: "0.1em" }
- tags: [whitespace, hairline, light-weight, zen]
- combines-well-with: [Swiss, Flat-2, Dark-Mode]

## Frutiger Aero
- ko: 프루티거 에어로
- structure: { radius: 20px, layout: nature-lens }
- texture: { shadow: "outer + inset specular", bg-pattern: bokeh-blobs }
- color: { bg: "gradient(#a8d8ea,#68b684,#2e7d32)", text: "#2e5a2e" }
- typography: { font: system, weight: 700 }
- tags: [nature, 2000s-Windows, glossy, organic]
- combines-well-with: [Y2K-Futurism, Biomorphism]

## Y2K Futurism
- ko: Y2K 퓨처리즘
- structure: { radius: "blob (60% 40% 50% 50%)", layout: blob-centric }
- texture: { shadow: inset-specular, bg-pattern: chrome-gradient }
- color: { bg: "gradient(#c0c0c0,#e8e8e8,#a0a0a0)", text: "#555" }
- typography: { font: system, weight: 800 }
- tags: [chrome, blob-shape, iridescent, late-90s]
- combines-well-with: [Frutiger-Aero, Holographic]

## Retro Futurism
- ko: 레트로 퓨처리즘
- structure: { radius: 2px, layout: perspective-grid }
- texture: { shadow: neon-glow, bg-pattern: perspective-grid-sunset }
- color: { bg: "gradient(#0a0014,#1a0033,#ff006e,#ff8c00)", accent: "#00f0ff / #ff2d95" }
- typography: { font: "Courier New, monospace", weight: 700, text-shadow: glow }
- tags: [synthwave, retrowave, perspective-grid, sunset]
- combines-well-with: [Vaporwave, Cyberpunk, Neon-Glow]

## Vaporwave
- ko: 베이퍼웨이브
- structure: { radius: 0, layout: centered-text }
- texture: { shadow: text-shadow-multi-color, bg-pattern: scan-line-overlay }
- color: { bg: "gradient(#ff71ce,#01cdfe,#b967ff,#fffb96)", text: "#fff" }
- typography: { font: "Times New Roman, serif", weight: 900, style: italic, letter-spacing: "0.3em" }
- tags: [pastel-neon, retro-aesthetic, serif, scan-lines]
- combines-well-with: [Retro-Futurism, Holographic]

## Cyberpunk
- ko: 사이버펑크
- structure: { radius: 2px, layout: box-with-border }
- texture: { shadow: neon-glow-cyan, bg-pattern: none, glitch: clip-path-animation }
- color: { bg: "#0a0a0f", text: "#0ff", accent: "#f0f", border: "#0ff" }
- typography: { font: "Courier New, monospace", weight: 900, text-shadow: cyan-glow }
- tags: [neon-cyan, magenta, monospace, glitch, dark]
- combines-well-with: [Neon-Glow, Retro-Futurism, Dark-Mode]

## Memphis Design
- ko: 멤피스 디자인
- structure: { radius: "0 or 50px (mixed)", layout: geometric-collage }
- texture: { shadow: none, bg-pattern: dot-pattern-geometric-shapes }
- color: { bg: "#ffeaa7", accent: "#e17055 / #6c5ce7 / #00cec9" }
- typography: { font: system, weight: 900 }
- tags: [80s, geometric, bold-pattern, playful, eclectic]
- combines-well-with: [Corporate-Memphis, Maximalism, Brutalism]

## Corporate Memphis
- ko: 코퍼레이트 멤피스
- structure: { radius: 16-20px, layout: illustration-centric }
- texture: { shadow: none, bg-pattern: flat-illustration-figures }
- color: { bg: "#f0f4ff", accent: "#6366f1 / #ec4899 / #3b82f6" }
- typography: { font: system, weight: normal }
- tags: [SaaS-illustration, friendly, rounded, tech-startup]
- combines-well-with: [Flat-Design, Bento-Grid]

## Aurora UI
- ko: 오로라 UI
- structure: { radius: 12-16px, layout: dark-blur-card }
- texture: { shadow: none, bg-pattern: animated-blur-blobs, animation: float-translate-scale }
- color: { bg: "#0a0a1a", blobs: "#22c55e / #3b82f6 / #a855f7", text: "#fff" }
- typography: { font: system, weight: 600 }
- tags: [dark, animated-blobs, colorful-glow, dreamy]
- combines-well-with: [Glassmorphism, Mesh-Gradient, Liquid-Glass]

## Mesh Gradient
- ko: 메시 그래디언트
- structure: { radius: 12-16px, layout: color-field }
- texture: { shadow: none, blur: "backdrop-filter:blur(8px)", bg-pattern: overlapping-radial-gradients }
- color: { bg: "#1e1b4b + multi-radial", accents: "#f472b6 / #60a5fa / #34d399 / #fbbf24 / #a78bfa" }
- typography: { font: system, weight: normal }
- tags: [colorful, abstract, modern, gradient-mesh]
- combines-well-with: [Aurora-UI, Glassmorphism]

## Grain/Noise
- ko: 그레인/노이즈
- structure: { radius: 10-12px, layout: textured-card }
- texture: { shadow: none, bg-pattern: "SVG feTurbulence fractalNoise overlay" }
- color: { bg: "gradient(#667eea,#764ba2)", modal-bg: "gradient(#92704a,#6b5b44)", accent: "#c4956a" }
- typography: { font: system, weight: 700 }
- tags: [organic, film-grain, textured, analog]
- combines-well-with: [Minimalism, Duotone]

## Duotone
- ko: 듀오톤
- structure: { radius: 4-8px, layout: color-filter-blocks }
- texture: { shadow: none, bg-pattern: mix-blend-mode-multiply }
- color: { bg: "#1a1a2e", duo: "#e63946 + #457b9d", accent: "#ff6b6b" }
- typography: { font: system, weight: 700 }
- tags: [two-color, photo-filter, editorial, bold]
- combines-well-with: [Grain-Noise, Metallic-Chrome]

## Holographic/Iridescent
- ko: 홀로그래픽/이리데슨트
- structure: { radius: 16px, layout: animated-card }
- texture: { shadow: none, bg-pattern: animated-rainbow-gradient, animation: "holo-shift 3s infinite" }
- color: { bg: "#111", card-bg: "gradient(#ff0080,#ff8c00,#40e0d0,#8a2be2)", text: "#fff" }
- typography: { font: system, weight: 800 }
- tags: [rainbow, animated, iridescent, premium]
- combines-well-with: [Y2K-Futurism, Metallic-Chrome, Vaporwave]

## Metallic/Chrome
- ko: 메탈릭/크롬
- structure: { radius: 8px, layout: bar-plate }
- texture: { shadow: "0 4px 20px rgba(0,0,0,0.4)", bg-pattern: multi-stop-specular-gradient }
- color: { bg: "#2a2a2a", surface: "gradient(#4a4a4a → #e0e0e0 → #888)", text: gradient-white-gray }
- typography: { font: system, weight: 900 }
- tags: [chrome, specular, metallic, industrial]
- combines-well-with: [Holographic, Y2K-Futurism, Cyberpunk]

## Neon Glow
- ko: 네온 글로우
- structure: { radius: 12px, layout: border-glow-box }
- texture: { shadow: "multi-layer glow (5px/15px/30px)", bg-pattern: none, animation: "neon-pulse 2s alternate" }
- color: { bg: "#0a0a0f", border: "#ff00ff", text: "#fff", text-shadow: cyan-glow }
- typography: { font: "Courier New, monospace", weight: 800, text-transform: uppercase }
- tags: [glow, dark, monospace, electric, animated]
- combines-well-with: [Cyberpunk, Retro-Futurism, Dark-Mode]

## Dark Mode
- ko: 다크 모드
- structure: { radius: 12px, layout: card-standard }
- texture: { shadow: "0 2px 8px rgba(0,0,0,0.4)", bg-pattern: none }
- color: { bg: "#121212", card-bg: "#1e1e1e", text: "#e0e0e0", accent: "#bb86fc / #03DAC6" }
- typography: { font: system, weight: 600 }
- tags: [dark-theme, OLED-friendly, accessible, modern]
- combines-well-with: [Material-Design, Glassmorphism, Cyberpunk]

## Kinetic Typography
- ko: 키네틱 타이포그래피
- structure: { radius: 8-12px, layout: text-animation-stage }
- texture: { shadow: none, animation: "wave translateY per-letter stagger" }
- color: { bg: "#111", text: "#fff", accents: "#f472b6 / #60a5fa / #34d399" }
- typography: { font: system, weight: 900, animation: wave-per-letter }
- tags: [animated-text, expressive, per-letter, motion]
- combines-well-with: [Dark-Mode, Maximalism]

## Parallax
- ko: 패럴랙스
- structure: { radius: 12px, layout: perspective-layers }
- texture: { shadow: deep-elevation, blur: "backdrop-filter:blur(4px)", bg-pattern: perspective-translateZ }
- color: { bg: "gradient(#1a1a3e,#2d1b69)", layers: "rgba varied opacity" }
- typography: { font: system, weight: 700 }
- tags: [3d-depth, layered, spatial, perspective]
- combines-well-with: [Spatial-Design, Glassmorphism]

## Spatial Design
- ko: 스페이셜 디자인
- structure: { radius: 20px, layout: 3d-tilted-card }
- texture: { shadow: deep-elevation-60px, blur: "backdrop-filter:blur(20px)" }
- color: { bg: "gradient(#0f0f1a,#1a1a2e)", card-bg: "rgba(255,255,255,0.06)", border: "rgba(255,255,255,0.1)" }
- typography: { font: system, weight: 700 }
- tags: [visionOS, depth, 3d-transform, translucent]
- combines-well-with: [Glassmorphism, Liquid-Glass, Parallax]

## Acrylic (Fluent)
- ko: 아크릴 (플루언트)
- structure: { radius: 8px, layout: windows-card }
- texture: { shadow: none, blur: "backdrop-filter:blur(20px)", bg-pattern: "SVG noise exclusion" }
- color: { bg: "gradient(#2563eb,#7c3aed)", card-bg: "rgba(255,255,255,0.12)", accent: "#60a5fa" }
- typography: { font: "Segoe UI, system-ui", weight: 700 }
- tags: [Windows-11, Fluent, acrylic, noise-texture, blur]
- combines-well-with: [Glassmorphism, Dark-Mode, Spatial-Design]

## Biomorphism
- ko: 바이오모피즘
- structure: { radius: "24px card / animated blob radius", layout: organic-blob }
- texture: { shadow: none, blur: "backdrop-filter:blur(8px)", animation: "bio-morph 8s infinite border-radius" }
- color: { bg: "#f0fdf4", blobs: "gradient(#86efac,#34d399)", card-bg: "rgba(255,255,255,0.7)", accent: "#34d399" }
- typography: { font: system, weight: 700 }
- tags: [organic, nature, morphing, green, animated-shape]
- combines-well-with: [Claymorphism, Frutiger-Aero, Minimalism]

---

## 조합 가이드

스타일 조합 시 레이어별로 선택한다:

1. **구조 선택** — 레이아웃과 radius를 결정하는 스타일
2. **질감 선택** — 그림자, blur, 텍스처를 결정하는 스타일
3. **컬러 선택** — 색상 팔레트를 결정하는 스타일
4. **타이포 선택** — 폰트와 굵기를 결정하는 스타일

예시 조합:
- "Swiss 구조 + Glassmorphism 질감 + Cyberpunk 컬러" → 그리드 레이아웃 + blur 카드 + 네온 색상
- "Minimalism 구조 + Grain/Noise 질감 + Duotone 컬러" → 미니멀 레이아웃 + 필름 그레인 + 2톤 색상
- "Bento Grid 구조 + Neumorphism 질감 + Pastel 컬러" → 벤토 그리드 + 소프트 그림자 + 파스텔
