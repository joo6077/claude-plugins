#!/usr/bin/env bash
# m-a11y.sh <레포> — 접근성 검사의 테마 단추 재기를 네 쪽과 임시 쪽 둘에 돌린다.
# playwright-core 는 레포 node_modules 가 없으면 NODE_PATH 로 준다.
# 줄마다 `<쪽 이름> <OK|FAIL> btn=<값>`, 끝 줄 `rc=<종료 코드>`.
R=${1:?레포 경로}
T=$(mktemp -d "${TMPDIR:-/tmp}/ma11y.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
page() {  # page <파일> <단추 태그>
  cat > "$1" <<H
<!doctype html><html lang="ko" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>t</title>
<style>body{background:#111;color:#eee;font:16px sans-serif;margin:16px}</style></head>
<body><p>본문</p>$2</body></html>
H
}
page "$T/small-toggle.html" '<button class="theme-toggle" id="themeToggle" type="button" style="width:60px;height:30px;background:#222;color:#eee">Dark</button>'
page "$T/big-toggle.html" '<button class="theme-toggle" id="themeToggle" type="button" style="width:60px;height:48px;background:#222;color:#eee">Dark</button>'
cd "$R" || exit 2
out=$(node scripts/check-docs-a11y.js docs/design-kit/color-palette.html docs/design-kit/visual-styles.html \
  docs/tone-kit/korean-technical-writing.html docs/api-kit/research-log.html "$T/small-toggle.html" "$T/big-toggle.html" 2>&1); rc=$?
printf '%s\n' "$out" | sed -n -E 's/^(OK|FAIL) +([^ ]+) .* btn=([^ ]+) .*/\2 \1 btn=\3/p'
echo "rc=$rc"
