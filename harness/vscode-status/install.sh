#!/usr/bin/env bash
# Codex 진행 상황 확장을 VSIX 로 묶어 VS Code 에 설치한다. 폴더 복사 설치는 공식 근거가 없다.
set -euo pipefail
here=$(cd "$(dirname "${0}")" && pwd)
code_cli=${CODE_CLI:-$(command -v code || echo '/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code')}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
(cd "$here" && npx --yes @vscode/vsce@4.0.0 package --no-dependencies --allow-missing-repository --skip-license -o "$work/codex-status.vsix")
"$code_cli" --install-extension "$work/codex-status.vsix" --force
echo '설치했다 — VS Code 에서 「Developer: Reload Window」 로 창을 다시 불러오면 Codex 작업이 도는 동안 하단에 뜬다'
