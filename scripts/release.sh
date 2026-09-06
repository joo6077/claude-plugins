#!/usr/bin/env bash
# ── Plugin Release Script ──
# Usage: bash scripts/release.sh <plugin-name> <patch|minor|major>
# Example: bash scripts/release.sh harness patch

set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# ── --help 지원 ──
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Plugin Release Script"
  echo ""
  echo "Usage: bash scripts/release.sh <plugin-name> <patch|minor|major>"
  echo ""
  echo "Bumps the plugin version in plugin.json and marketplace.json, then creates"
  echo "a release branch + commit + tag, pushes it, and opens a PR against main."
  echo ""
  echo "main 에 직접 push 하지 않습니다 — main 은 branch protection(enforce_admins=true)"
  echo "으로 보호되며 릴리스도 CI 3 체크를 통과해야 머지됩니다. 태그는 보호 대상이"
  echo "아니므로 즉시 push 됩니다."
  echo ""
  echo "Arguments:"
  echo "  plugin-name   Name of the plugin directory (e.g. harness, flutter-toolkit)"
  echo "  bump-type     Version bump type: patch, minor, or major"
  echo ""
  echo "Options:"
  echo "  --dry-run     버전은 계산·수정하되 branch/commit/tag/push/PR 은 하지 않음"
  echo ""
  echo "Available plugins:"
  for d in "$REPO_ROOT"/*/; do
    [ -f "$d/.claude-plugin/plugin.json" ] && echo "  - $(basename "$d")"
  done
  exit 0
fi

# ── --dry-run (어느 위치에 와도 인식) ──
DRY_RUN=0
ARGS=()
for a in "$@"; do
  if [ "$a" = "--dry-run" ]; then DRY_RUN=1; else ARGS+=("$a"); fi
done
set -- "${ARGS[@]+"${ARGS[@]}"}"

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

# ── marketplace.json 에서 파생되는 문서 재생성 ──
# marketplace.json 의 description 은 두 곳으로 흘러간다:
#   README.md 플러그인 표          (sync-docs.py)
#   kaizen-orchestrator AUTO 블록  (sync-orchestrator.py)
# 이걸 안 돌리면 릴리스마다 drift 가 쌓인다 — 실측 2026-09-06: bambu-kit v0.7.0 릴리스 후
# orchestrator 가 v0.6.0 설명을 들고 있어 --check-only 가 exit 1 이었다.
python3 "$REPO_ROOT/scripts/sync-docs.py" >/dev/null
python3 "$REPO_ROOT/scripts/sync-orchestrator.py" >/dev/null
echo "Synced: README.md · kaizen-orchestrator"

# ── Git commit + tag + PR ──
#
# main 에 직접 push 하지 않는다. main 은 branch protection 으로 보호되며
# enforce_admins=true 이므로 소유자의 직접 push 도 거부된다 (그것이 의도다 —
# 이 레포는 Playwright 잡이 32 회 연속 red 인 채로 릴리스가 계속 나간 이력이 있다).
# 릴리스도 CI 3 체크를 통과해야 main 에 들어간다.
#
# 태그는 branch protection 대상이 아니므로(태그 보호 규칙 없음) 그대로 push 한다.
cd "$REPO_ROOT"

RELEASE_BRANCH="release/${PLUGIN_NAME}-v${NEW_VERSION}"

# ── 사전 가드 ──
# 이 검사들이 없으면 `git tag -a` 가 fatal 로 죽고 set -e 가 스크립트를 중단시켜
# 브랜치 push 와 PR 생성이 조용히 건너뛰어진다 (버전 파일만 수정된 채로 남는다).
GUARD_FAIL=0

if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
  echo "Error: 태그 $TAG 가 이미 로컬에 있습니다." >&2
  echo "  이전 릴리스 시도가 남긴 것이라면: git tag -d $TAG" >&2
  GUARD_FAIL=1
fi

if [ -n "$(git ls-remote --tags origin "refs/tags/$TAG" 2>/dev/null)" ]; then
  echo "Error: 태그 $TAG 가 이미 origin 에 있습니다 — 이 버전은 이미 릴리스되었습니다." >&2
  echo "  되돌리려면: git push origin :refs/tags/$TAG" >&2
  GUARD_FAIL=1
fi

if git rev-parse -q --verify "refs/heads/$RELEASE_BRANCH" >/dev/null; then
  echo "Error: 브랜치 $RELEASE_BRANCH 가 이미 있습니다." >&2
  echo "  이전 시도가 남긴 것이라면: git branch -D $RELEASE_BRANCH" >&2
  GUARD_FAIL=1
fi

if [ "$GUARD_FAIL" = "1" ]; then
  echo "" >&2
  echo "버전 파일은 이미 수정되었습니다. 되돌리려면:" >&2
  echo "  git checkout -- \"$PLUGIN_JSON\" \"$MARKETPLACE_JSON\"" >&2
  exit 1
fi

if [ "$DRY_RUN" = "1" ]; then
  echo ""
  echo "[dry-run] 아래 동작을 수행하지 않고 종료합니다:"
  echo "  git checkout -b $RELEASE_BRANCH"
  echo "  git add $PLUGIN_JSON $MARKETPLACE_JSON README.md .claude/skills/kaizen-orchestrator/SKILL.md"
  echo "  git commit -m 'release: ${PLUGIN_NAME} v${NEW_VERSION}'"
  echo "  git tag -a $TAG -m '${PLUGIN_NAME} v${NEW_VERSION}'"
  echo "  git push -u origin $RELEASE_BRANCH --follow-tags"
  echo "  gh pr create --base main --head $RELEASE_BRANCH"
  echo ""
  echo "[dry-run] plugin.json / marketplace.json 은 이미 수정되었습니다. 되돌리려면:"
  echo "  git checkout -- $PLUGIN_JSON $MARKETPLACE_JSON"
  exit 0
fi

git checkout -b "$RELEASE_BRANCH"
git add "$PLUGIN_JSON" "$MARKETPLACE_JSON" \
  "$REPO_ROOT/README.md" "$REPO_ROOT/.claude/skills/kaizen-orchestrator/SKILL.md"
git commit -m "release: ${PLUGIN_NAME} v${NEW_VERSION}"
git tag -a "$TAG" -m "${PLUGIN_NAME} v${NEW_VERSION}"
git push -u origin "$RELEASE_BRANCH" --follow-tags

PR_URL="$(gh pr create --base main --head "$RELEASE_BRANCH" \
  --title "release: ${PLUGIN_NAME} v${NEW_VERSION}" \
  --body "\`${PLUGIN_NAME}\` ${CURRENT_VERSION} → **${NEW_VERSION}** (${BUMP_TYPE})

- \`${PLUGIN_NAME}/.claude-plugin/plugin.json\`
- \`.claude-plugin/marketplace.json\` (description 날짜 ${TODAY})

태그 \`${TAG}\` 는 이미 push 되었습니다. CI 3 체크 통과 후 머지하세요.

이 PR 은 \`scripts/release.sh\` 가 생성했습니다 — main 은 protection 으로
직접 push 가 차단되어 있어 릴리스도 CI 를 통과해야 합니다.")"

echo ""
echo "Done! ${PLUGIN_NAME} v${NEW_VERSION} — PR 생성 완료."
echo "  Tag:    $TAG (push 완료)"
echo "  Branch: $RELEASE_BRANCH"
echo "  PR:     $PR_URL"
echo ""
echo "CI 3 체크 통과 후 머지하세요:"
echo "  gh pr checks $PR_URL"
echo "  gh pr merge $PR_URL --merge --delete-branch"
echo ""
echo "⚠ 태그 $TAG 는 머지 전에 push 되었습니다. PR 을 머지하지 않고 버리면"
echo "  태그가 main 에서 도달 불가능해집니다. 그 경우 태그도 지우세요:"
echo "    git push origin :refs/tags/$TAG && git tag -d $TAG"
