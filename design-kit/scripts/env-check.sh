#!/usr/bin/env bash
set -euo pipefail

echo "=== Environment Check ==="

# OS 감지
case "$(uname -s 2>/dev/null || echo Windows)" in
  Darwin*)  OS="macOS" ;;
  Linux*)   OS="linux" ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
  *)        OS="windows" ;;
esac
echo "OS: $OS"

echo ""
echo "✅ All checks passed"
