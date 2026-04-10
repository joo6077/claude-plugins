#!/usr/bin/env bash
# ── Plugin Release Script ──
# Usage: bash scripts/release.sh <plugin-name> <patch|minor|major>
# Example: bash scripts/release.sh harness patch

set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_NAME="${1:-}"
BUMP_TYPE="${2:-}"

# ── 입력 검증 ──
if [ -z "$PLUGIN_NAME" ] || [ -z "$BUMP_TYPE" ]; then
  echo "Usage: bash scripts/release.sh <plugin-name> <patch|minor|major>"
  echo "  Available plugins:"
  for d in "$REPO_ROOT"/*/; do
    [ -f "$d/.claude-plugin/plugin.json" ] && echo "    - $(basename "$d")"
  done
  exit 1
fi

PLUGIN_JSON="$REPO_ROOT/$PLUGIN_NAME/.claude-plugin/plugin.json"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"

if [ ! -f "$PLUGIN_JSON" ]; then
  echo "Error: $PLUGIN_NAME/.claude-plugin/plugin.json not found"
  exit 1
fi

if [[ "$BUMP_TYPE" != "patch" && "$BUMP_TYPE" != "minor" && "$BUMP_TYPE" != "major" ]]; then
  echo "Error: bump type must be patch, minor, or major"
  exit 1
fi

# ── dirty check ──
if ! git -C "$REPO_ROOT" diff --quiet 2>/dev/null || ! git -C "$REPO_ROOT" diff --cached --quiet 2>/dev/null; then
  echo "Warning: working tree has uncommitted changes"
  read -r -p "Continue anyway? [y/N] " confirm
  [ "$confirm" = "y" ] || [ "$confirm" = "Y" ] || exit 1
fi

# ── 현재 버전 읽기 ──
CURRENT_VERSION=$(grep '"version"' "$PLUGIN_JSON" | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

if [ -z "$CURRENT_VERSION" ]; then
  echo "Error: could not parse version from $PLUGIN_JSON"
  exit 1
fi

IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# ── 새 버전 계산 ──
case "$BUMP_TYPE" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
TODAY=$(date +%Y-%m-%d)
TAG="${PLUGIN_NAME}/v${NEW_VERSION}"

echo "=== Release: $PLUGIN_NAME ==="
echo "  $CURRENT_VERSION -> $NEW_VERSION"
echo "  Tag: $TAG"
echo ""

# ── sed -i 크로스플랫폼 (BSD/GNU) ──
if sed --version >/dev/null 2>&1; then
  SED_INPLACE=(sed -i)
else
  SED_INPLACE=(sed -i '')
fi

# ── plugin.json 업데이트 ──
"${SED_INPLACE[@]}" "s/\"version\": \"${CURRENT_VERSION}\"/\"version\": \"${NEW_VERSION}\"/" "$PLUGIN_JSON"
echo "Updated: $PLUGIN_JSON"

# ── marketplace.json 업데이트 ──
# 해당 플러그인 name 블록의 description에서 [vX.Y.Z · YYYY-MM-DD] 패턴 치환
"${SED_INPLACE[@]}" "/$PLUGIN_NAME/,/description/{s/\[v[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]* · [0-9-]*\]/[v${NEW_VERSION} · ${TODAY}]/;}" "$MARKETPLACE_JSON"
echo "Updated: $MARKETPLACE_JSON"

# ── Git commit + tag + push ──
cd "$REPO_ROOT"
git add "$PLUGIN_JSON" "$MARKETPLACE_JSON"
git commit -m "release: ${PLUGIN_NAME} v${NEW_VERSION}"
git tag -a "$TAG" -m "${PLUGIN_NAME} v${NEW_VERSION}"
git push origin HEAD --follow-tags

echo ""
echo "Done! ${PLUGIN_NAME} v${NEW_VERSION} released."
echo "  Tag: $TAG"
