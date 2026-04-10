import type { Config } from 'tailwindcss'

// Tailwind v4 uses CSS-first config via @theme in globals.css.
// This file is mainly for tool compatibility; theme extensions live in globals.css.
const config: Config = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
}

export default config
