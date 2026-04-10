# Project Detection Rules

All react-kit skills read this file to determine the current project environment before generating code. Mirrors the `flutter-toolkit/references/project-detection.md` pattern.

## Detection Order

1. **Node version** — read `.nvmrc` first, fallback to `package.json` `engines.node`
2. **pnpm version** — read `packageManager` field in `package.json`
3. **React version** — read `dependencies.react` in `package.json`
4. **Vite install** — check `devDependencies.vite` + `vite.config.ts` exists
5. **Tailwind version** — read `devDependencies.tailwindcss`. v4 vs v3 has different install paths
6. **shadcn initialization** — check `components.json` exists at project root
7. **TanStack Router plugin** — check `devDependencies.@tanstack/router-plugin`
8. **Cargo workspace** — check root `Cargo.toml` with `[workspace]` table
9. **Tauri install** — check `src-tauri/` directory exists and has `tauri.conf.json`
10. **Lingui config** — check `lingui.config.ts` exists
11. **strict TypeScript** — read `tsconfig.json` for `strict: true` and related options

## Detection Outputs

A detection result is a JSON object shaped like:

```json
{
  "node": "22.14.1",
  "pnpm": "9.15.0",
  "react": "19.0.0",
  "vite": "6.0.1",
  "tailwind": "4.0.0",
  "shadcn": true,
  "tanstackRouter": true,
  "cargoWorkspace": true,
  "tauri": true,
  "lingui": true,
  "strictTS": true
}
```

## Skill Behavior Based on Detection

- Tailwind v3 detected → `/react-init` refuses, suggests upgrade. Existing skills use v3 syntax
- shadcn missing → `/react-widget` suggests `pnpm dlx shadcn@latest init --template vite` first
- Cargo workspace missing → `/react-wasm` refuses, suggests `/react-init --with-wasm` first
- Tauri missing → `/react-tauri` refuses, suggests `/react-init --with-tauri` first
- strict TS missing → all generation skills inject the strict compilerOptions

## Caching

Detection result is computed once per skill invocation and cached. Long-running sessions may re-detect on demand.

## Related Documents

- `docs/react/kit-design/g1-scaffolding.md` §1 — `/react-init` scaffolding details
- `docs/react/kit-design/g6-build-audit.md` §1.3 — `/react-run` subcommand enabling based on detection
