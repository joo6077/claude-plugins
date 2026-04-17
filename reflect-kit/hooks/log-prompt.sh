#!/usr/bin/env bash
# UserPromptSubmit hook: 사용자 프롬프트를 프로젝트별 월간 로그에 append
# stdin: {session_id, cwd, prompt, ...}
# 프로젝트 ID는 <basename>-<6자 hash> (git root 기반)

set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib-project-id.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib-redact.sh"

input=$(cat)

cwd=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null)
prompt=$(echo "$input" | jq -r '.prompt // empty' 2>/dev/null)
session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)

[ -z "$cwd" ] && cwd="$PWD"
[ -z "$prompt" ] && exit 0

# 민감 패턴 redaction
prompt=$(redact_sensitive "$prompt")

project_id=$(compute_project_id "$cwd")
log_dir="$HOME/.claude/logs/$project_id"
mkdir -p "$log_dir" 2>/dev/null

log_file="$log_dir/$(date '+%Y-%m').md"
timestamp=$(date '+%Y-%m-%dT%H:%M:%S%z')

{
  echo ""
  echo "## [prompt] $timestamp"
  echo ""
  echo "- session: \`$session_id\`"
  echo "- cwd: \`$cwd\`"
  echo ""
  echo "$prompt"
  echo ""
  echo "---"
} >> "$log_file" 2>/dev/null

exit 0
