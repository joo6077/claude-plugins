#!/usr/bin/env bash
# project-detect.sh — react-kit project environment detection
# Reads the current working directory and prints a JSON detection result.
# Used by skills that need quick bash-callable detection (outside of Claude).

set -euo pipefail

# ── Helpers ─────────────────────────────────────────────
read_json_field() {
  # Usage: read_json_field <file> <field-path>
  local file="$1"
  local path="$2"
  if [ ! -f "$file" ]; then
    echo "null"
    return
  fi
  if command -v jq >/dev/null 2>&1; then
    jq -r "$path // \"null\"" "$file" 2>/dev/null || echo "null"
  else
    python3 -c "
import json, sys
try:
    with open('$file') as f:
        data = json.load(f)
    path = '$path'.lstrip('.').split('.')
    for p in path:
        if p.startswith('\"') and p.endswith('\"'):
            p = p[1:-1]
        data = data.get(p) if isinstance(data, dict) else None
    print(data if data else 'null')
except Exception:
    print('null')
"
  fi
}

# ── Detection ───────────────────────────────────────────
NODE_VERSION="null"
if [ -f ".nvmrc" ]; then
  NODE_VERSION=$(tr -d '\n' < .nvmrc)
fi

PNPM_VERSION=$(read_json_field "package.json" ".packageManager")
REACT_VERSION=$(read_json_field "package.json" ".dependencies.react")
VITE_VERSION=$(read_json_field "package.json" ".devDependencies.vite")
TAILWIND_VERSION=$(read_json_field "package.json" ".devDependencies.tailwindcss")

SHADCN=false
[ -f "components.json" ] && SHADCN=true

TANSTACK_ROUTER=false
[ -n "$(read_json_field 'package.json' '.devDependencies.\"@tanstack/router-plugin\"')" ] && TANSTACK_ROUTER=true

CARGO_WORKSPACE=false
if [ -f "Cargo.toml" ] && grep -q '\[workspace\]' Cargo.toml 2>/dev/null; then
  CARGO_WORKSPACE=true
fi

TAURI=false
[ -d "src-tauri" ] && [ -f "src-tauri/tauri.conf.json" ] && TAURI=true

LINGUI=false
[ -f "lingui.config.ts" ] && LINGUI=true

STRICT_TS=false
if [ -f "tsconfig.json" ] && grep -q '"strict"[[:space:]]*:[[:space:]]*true' tsconfig.json 2>/dev/null; then
  STRICT_TS=true
fi

# ── Output JSON ─────────────────────────────────────────
cat <<EOF
{
  "node": "$NODE_VERSION",
  "pnpm": "$PNPM_VERSION",
  "react": "$REACT_VERSION",
  "vite": "$VITE_VERSION",
  "tailwind": "$TAILWIND_VERSION",
  "shadcn": $SHADCN,
  "tanstackRouter": $TANSTACK_ROUTER,
  "cargoWorkspace": $CARGO_WORKSPACE,
  "tauri": $TAURI,
  "lingui": $LINGUI,
  "strictTS": $STRICT_TS
}
EOF
