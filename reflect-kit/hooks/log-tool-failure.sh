#!/usr/bin/env bash
# PostToolUseFailure hook: 도구 실패를 프로젝트별 월간 로그에 append
# stdin: {session_id, cwd, tool_name, tool_input, tool_response, ...}

set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib-project-id.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib-redact.sh"

input=$(cat)

cwd=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null)
tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null)
session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)
tool_input=$(echo "$input" | jq -c '.tool_input // {}' 2>/dev/null)
tool_response=$(echo "$input" | jq -c '.tool_response // {}' 2>/dev/null)

[ -z "$cwd" ] && cwd="$PWD"

# 민감 패턴 redaction (JSON 문자열 내 시크릿도 잡힘)
tool_input=$(redact_sensitive "$tool_input")
tool_response=$(redact_sensitive "$tool_response")

project_id=$(compute_project_id "$cwd")
log_dir="$HOME/.claude/logs/$project_id"
mkdir -p "$log_dir" 2>/dev/null

log_file="$log_dir/$(date '+%Y-%m').md"
timestamp=$(date '+%Y-%m-%dT%H:%M:%S%z')

{
  echo ""
  echo "## [tool-failure] $timestamp — $tool_name"
  echo ""
  echo "- session: \`$session_id\`"
  echo "- cwd: \`$cwd\`"
  echo ""
  echo "### Input"
  echo '```json'
  echo "$tool_input" | jq . 2>/dev/null || echo "$tool_input"
  echo '```'
  echo ""
  echo "### Response"
  echo '```json'
  echo "$tool_response" | jq . 2>/dev/null || echo "$tool_response"
  echo '```'
  echo ""
  echo "---"
} >> "$log_file" 2>/dev/null

exit 0
