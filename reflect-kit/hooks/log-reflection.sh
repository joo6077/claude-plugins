#!/usr/bin/env bash
# Stop hook: 세션 transcript를 codex exec로 분석 → 구조화 YAML 블록으로 기록
# reflect-kit 파이프라인의 분석 수집 레이어. codex CLI 기존 인증 사용.
#
# 동작:
#   (fast path) stdin을 tmp 파일로 저장 → nohup 백그라운드로 자기 자신 재호출 → 즉시 exit 0.
#               Stop 훅 체감 지연 0. plugin spec의 async 필드에 의존하지 않는다.
#   (bg path)   tmp 파일에서 stdin 복원 → codex 분석 실행 → reflections-YYYY-MM.md 에 append.
#               실패 시 .errors.log 에 사유 기록 후 조용히 종료.

set +e

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib-project-id.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib-redact.sh"

HOOK_NAME="log-reflection"

# ── 백그라운드 진입점 ─────────────────────────────────────────────────
if [ "$1" = "--background" ] && [ -n "$2" ]; then
  bg_input_file="$2"
  input=$(cat "$bg_input_file" 2>/dev/null)
  rm -f "$bg_input_file" 2>/dev/null

  if [ -z "$input" ]; then
    exit 0
  fi
  # 실제 작업은 아래 공통 블록으로 이어짐
else
  # ── fast path: stdin을 tmp 파일에 저장하고 백그라운드 재호출 ───────
  bg_input_file=$(mktemp "${TMPDIR:-/tmp}/reflect-hook-XXXXXX")
  cat > "$bg_input_file"

  # stdin이 비어 있으면 백그라운드 호출 자체를 생략
  if [ ! -s "$bg_input_file" ]; then
    rm -f "$bg_input_file" 2>/dev/null
    exit 0
  fi

  nohup bash "$SCRIPT_PATH" --background "$bg_input_file" >/dev/null 2>&1 &
  disown 2>/dev/null
  exit 0
fi

# ── 이하 백그라운드 전용 블록 ─────────────────────────────────────────

cwd=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null)
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null)
session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)

[ -z "$cwd" ] && cwd="$PWD"

project_id=$(compute_project_id "$cwd")
log_dir="$HOME/.claude/logs/$project_id"
mkdir -p "$log_dir" 2>/dev/null

# ── 조용한 스킵 경로 (사유는 .errors.log에 기록) ──────────────────────────
if ! command -v codex >/dev/null 2>&1; then
  log_hook_error "$log_dir" "$HOOK_NAME" "skip:cli-missing session=$session_id"
  exit 0
fi
if [ -z "$transcript_path" ]; then
  log_hook_error "$log_dir" "$HOOK_NAME" "skip:transcript-path-empty session=$session_id"
  exit 0
fi
if [ ! -f "$transcript_path" ]; then
  log_hook_error "$log_dir" "$HOOK_NAME" "skip:transcript-file-missing path=$transcript_path"
  exit 0
fi

line_count=$(wc -l < "$transcript_path" 2>/dev/null | tr -d ' ')
if [ -z "$line_count" ] || [ "$line_count" -lt 10 ]; then
  log_hook_error "$log_dir" "$HOOK_NAME" "skip:transcript-too-short lines=${line_count:-0}"
  exit 0
fi

transcript_content=$(tail -n 150 "$transcript_path" 2>/dev/null | head -c 80000)
if [ -z "$transcript_content" ]; then
  log_hook_error "$log_dir" "$HOOK_NAME" "skip:transcript-empty-after-tail"
  exit 0
fi

# 민감 패턴 redaction (transcript에 포함될 수 있는 API 키/토큰/JWT 등)
transcript_content=$(redact_sensitive "$transcript_content")

out_file="$log_dir/reflections-$(date '+%Y-%m').md"

# ── 프롬프트 구성 (Haiku/GPT-5급 모두 해석 가능한 구조화 스키마) ──────────
prompt=$(cat <<PROMPT_EOF
당신은 개발자-Claude Code 대화 transcript를 분석하는 평가자다. 아래 <transcript>는 Claude Code 세션의 jsonl 원본(각 줄이 role/content 오브젝트)이다.

다음 네 종류의 사건 중 **실제 증거가 명확한 지점만** 추출하라:
- misunderstanding: 사용자 의도를 잘못 해석 (엉뚱한 파일 수정, 범위 오해, 잘못된 가정)
- repeated_error: 같은 세션 내 또는 사용자 교정 뒤에도 반복된 같은 실수
- wrong_approach: 더 적절한 스킬/에이전트/MCP가 있었는데 비효율적이거나 엉뚱한 방법으로 시도
- tool_failure: 도구 호출 실패 중 맥락이 의미있는 것 (단순 exit code-only는 제외)

각 지점마다 아래 YAML 블록을 출력하라. 여러 개면 YAML 블록 사이에 빈 줄만. 문제 없으면 정확히 'no issues' 한 줄만.

\`\`\`yaml
primary_category: misunderstanding | repeated_error | wrong_approach | tool_failure
also_applies: [<추가 해당 카테고리들, 없으면 빈 배열>]
mistake_tag: <kebab-case 영문 태그, 같은 패턴이면 같은 태그>
trigger: <사용자 프롬프트/상황 스니펫 1줄>
undesired_behavior: <Claude가 한 잘못 1줄>
desired_behavior: <사용자가 원한 것 1줄>
severity: low | medium | high
# Surface 결정을 위한 4축 (승격기가 precedence table로 최종 surface 계산)
scope: session | project | global      # 이 규칙이 어느 범위에 적용되어야 하는가
risk_class: low | medium | high        # 위반 시 피해 정도
procedurality: single_rule | multi_step_procedure  # 단일 규칙 vs 절차/체크리스트
enforcement_need: soft_reminder | hard_gate        # 안내로 충분 vs 차단 필요
user_stated_constraint: true | false   # 사용자가 이전에 명시적으로 금지/지시한 제약을 Claude가 다시 위반했는가 (예: "ValueNotifier 쓰지 마", "이 파일 건드리지 마"). true면 omission-constraint-decay 신호 — 승격기가 fast-track 처리
evidence_turns: <교정이 드러난 턴 수, 정수>
tools_used:
  skills: [<invoke된 slash command 이름들, 없으면 빈 배열>]
  agents: [<spawn된 subagent type들>]
  mcp_servers: [<사용한 MCP 서버 prefix>]
approach_note: <시도한 접근법 1줄 — 나중에 "이상한가" 판정 소재>
\`\`\`

규칙:
- 추측성 항목 배제. 근거가 transcript에 명확히 있는 것만.
- 최대 5개 지점.
- tools_used는 transcript의 tool 호출 기록에서 추출. 없으면 빈 배열.
- \`surface_candidate\` 같은 단일 필드는 쓰지 마라 — 위 4축으로만 표현한다.
- \`user_stated_constraint\`: 사용자가 **이전 턴/세션에서 명시적으로 금지하거나 지시한 제약**을 Claude가 다시 어긴 정황이 transcript에 있으면 true. 단순 실수(처음 한 것)는 false. 이 신호가 true면 omission-constraint-decay 사례로, 빈도가 낮아도 durable rule 승격 후보가 된다.
- 마크다운 외 설명/사과/주석 출력 금지. YAML 블록 또는 'no issues'만.

<transcript>
$transcript_content
</transcript>
PROMPT_EOF
)

# ── Claude CLI fallback 함수 ────────────────────────────────────────────
# codex exec 실패(exit != 0 또는 empty output) 시 `claude -p --model haiku-4.5`로 재시도.
# 성공 시 전역 변수 `summary`에 결과를 세팅하고 return 0. 실패 시 사유 태그 기록 후 return 1.
try_claude_fallback() {
  local codex_reason="$1"   # "codex-exit-N" 또는 "codex-empty-output"
  log_hook_error "$log_dir" "$HOOK_NAME" "fail:$codex_reason session=$session_id"

  if ! command -v claude >/dev/null 2>&1; then
    log_hook_error "$log_dir" "$HOOK_NAME" "skip:fallback-unavailable session=$session_id"
    return 1
  fi

  local fb_tmp fb_exit=0 fb_summary
  fb_tmp=$(mktemp)
  echo "$prompt" | claude -p --model haiku-4.5 > "$fb_tmp" 2>/dev/null
  fb_exit=$?
  fb_summary=$(cat "$fb_tmp" 2>/dev/null)
  rm -f "$fb_tmp"

  if [ "$fb_exit" -ne 0 ]; then
    log_hook_error "$log_dir" "$HOOK_NAME" "fallback:claude-exit-$fb_exit session=$session_id"
    return 1
  fi
  if [ -z "$fb_summary" ]; then
    log_hook_error "$log_dir" "$HOOK_NAME" "fallback:claude-empty-output session=$session_id"
    return 1
  fi

  log_hook_error "$log_dir" "$HOOK_NAME" "fallback:claude-used session=$session_id"
  summary="$fb_summary"
  return 0
}

# ── codex exec 호출 ─────────────────────────────────────────────────────
out_tmp=$(mktemp)
codex_exit=0
echo "$prompt" | codex exec \
  --ephemeral \
  --skip-git-repo-check \
  --full-auto \
  --color never \
  --cd "$HOME" \
  --output-last-message "$out_tmp" \
  - >/dev/null 2>&1
codex_exit=$?

summary=$(cat "$out_tmp" 2>/dev/null)
rm -f "$out_tmp"

# ── codex 실패 시 Claude fallback 시도 ──────────────────────────────────
if [ "$codex_exit" -ne 0 ]; then
  try_claude_fallback "codex-exit-$codex_exit" || exit 0
elif [ -z "$summary" ]; then
  try_claude_fallback "codex-empty-output" || exit 0
fi

trimmed=$(echo "$summary" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
[ "$trimmed" = "noissues" ] && exit 0

timestamp=$(date '+%Y-%m-%dT%H:%M:%S%z')
{
  echo ""
  echo "## $timestamp"
  echo ""
  echo "- session: \`$session_id\`"
  echo "- cwd: \`$cwd\`"
  echo ""
  echo "$summary"
  echo ""
  echo "---"
} >> "$out_file" 2>/dev/null

exit 0
