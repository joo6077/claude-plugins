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
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib-tag-canon.sh"

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

# ── 기존 태그 어휘 수집 (canonicalization 용 episodic memory) ──────────────
# 분석기는 세션마다 stateless 라 과거에 쓴 mistake_tag 를 모른다. 그래서 같은
# 근본원인이 매번 다른 태그로 쪼개진다. ledger 의 post_freq 가 태그를 키로 재발을
# 세므로 이 파편화는 리포팅 문제가 아니라 **측정 버그**다.
# Reflexion (arXiv 2303.11366) 의 episodic memory buffer 를 그대로 적용 — 이미 쓴
# 어휘를 프롬프트로 되돌려 주어 "발명" 대신 "재사용" 을 유도한다.
#
# 단 raw 목록을 그대로 되돌려주면 LLM 이 어느 표기를 골라야 하는지 알 수 없다.
# **결정론적 정규화 pass 를 LLM 앞에 두고** (형태소 → 동의어 → 명시 alias),
# `canonical_tag → aliases(freq)` 형태로 접어서 주입한다.
# 규약·근거: ../references/tag-canonicalization.md · 데이터: ../references/tag-lemma-map.tsv
# 2026-08-13 실측: 이 pass 로 skipped-required-api-doc-check 클러스터가 71 → 110 건이 됐다
# (원시 태그 단독 집계는 39 건, 즉 55% 를 과소집계하고 있었다).
#
# cluster_freq >= 2 상위 40 클러스터만 주입해 프롬프트 크기를 제한한다.
canon_tsv=$(mktemp)
refl_files=$(find "$log_dir" -maxdepth 1 -type f -name 'reflections-*.md' 2>/dev/null | sort)
if [ -n "$refl_files" ]; then
  # zsh 의 nomatch 로 글로빙이 명령을 통째로 죽인 전례가 있어 find 로 열거한다.
  # 배열 분해(셸별 word-splitting 차이)를 피하려고 원시 태그를 먼저 뽑아 stdin 으로 넘긴다.
  # 추출 규칙(grep 패턴 + sed 정리)은 라이브러리의 tag_canon_extract 가 정본이다 —
  # 여기에 같은 패턴을 다시 쓰면 수집면과 집계면이 조용히 갈라진다 (한쪽만 고쳐지는 순간
  # 훅이 주입하는 어휘와 digest 가 세는 어휘가 달라져 K3 과소집계가 그대로 돌아온다).
  raw_tags=$(printf '%s\n' "$refl_files" | while IFS= read -r f; do
    [ -n "$f" ] && tag_canon_extract "$f"
  done)
  printf '%s\n' "$raw_tags" | tag_canon_groups > "$canon_tsv" 2>/dev/null
  canon_rc=$?
  frag_line=$(printf '%s\n' "$raw_tags" | tag_canon_fragmentation 2>/dev/null)
else
  canon_rc=1
  frag_line=""
fi

[ "$canon_rc" = "3" ] && log_hook_error "$log_dir" "$HOOK_NAME" \
  "warn:lemma-map-unreadable path=$(tag_canon_map_path) session=$session_id"
[ -n "$frag_line" ] && log_hook_error "$log_dir" "$HOOK_NAME" \
  "vocab:raw_distinct/clusters/entries/singletons/fold/singleton_share/epc=$(printf '%s' "$frag_line" | tr '\t' '/') session=$session_id"

known_tags_block=$(awk -F'\t' '$1 >= 2 {
  n++
  if (n > 40) exit
  if ($3 == "") printf "- %s  (freq %d)\n", $2, $1
  else printf "- %s  (freq %d)  ← 같은 뜻으로 쓰인 다른 표기: %s\n", $2, $1, $3
}' "$canon_tsv" 2>/dev/null)
rm -f "$canon_tsv" 2>/dev/null

if [ -n "$known_tags_block" ]; then
  known_tags_block="## 이 프로젝트의 canonical mistake_tag 어휘 (canonical → 과거 표기들)
의미가 같은 사건이면 **canonical 철자를 글자 그대로** 재사용하라. \`←\` 뒤 표기들은 같은
근본원인의 과거 변형이므로 **다시 쓰지 마라** — canonical 쪽으로 쓴다.
$known_tags_block"
else
  known_tags_block="## 이 프로젝트의 canonical mistake_tag 어휘 (canonical → 과거 표기들)
(없음 — 첫 수집)"
fi

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
mistake_tag: <kebab-case 영문 태그. 아래 "mistake_tag 작성 규칙" 을 반드시 따른다>
new_tag_reason: <아래 canonical 어휘에 **없는** 새 태그를 만들었을 때만 이 줄을 넣는다. 기존 canonical 중 어느 것과도 근본원인이 다른 이유 1줄. canonical 을 재사용했으면 이 줄 자체를 생략한다>
trigger: <사용자 프롬프트/상황 스니펫 1줄>
undesired_behavior: <Claude가 한 잘못 1줄>
desired_behavior: <사용자가 원한 것 1줄>
severity: low | medium | high
actionability: claude_behavior | user_environment   # 이 사건을 Claude 행동으로 막을 수 있었는가. 아래 "actionability 판정" 참조
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
- \`new_tag_reason\` 은 **새 태그를 만든 블록에만** 넣는다. canonical 을 재사용한 블록에는 넣지 마라.
- \`user_stated_constraint\`: 사용자가 **이전 턴/세션에서 명시적으로 금지하거나 지시한 제약**을 Claude가 다시 어긴 정황이 transcript에 있으면 true. 단순 실수(처음 한 것)는 false. 이 신호가 true면 omission-constraint-decay 사례로, 빈도가 낮아도 durable rule 승격 후보가 된다.
- 마크다운 외 설명/사과/주석 출력 금지. YAML 블록 또는 'no issues'만.

## mistake_tag 작성 규칙 (집계 키다 — 파편화되면 승격이 불가능해진다)

1. **근본원인 1개 = 태그 1개.** 증상·파일명·도구명·발생 횟수를 태그에 넣지 마라. 같은 원인이 5개 파일/5번 툴콜에서 터졌으면 태그는 1개다.
2. **같은 근본원인은 이 세션에서 블록 1개로만 보고하라.** 반복 횟수는 \`evidence_turns\` 에 넣는다. 같은 원인을 여러 블록으로 쪼개지 마라.
3. **형태는 \`<동사원형>-<대상>\` kebab-case** (예: \`edit-before-read\`, \`skip-api-doc-lookup\`). **과거형·진행형을 쓰지 마라** — \`edited-\`/\`skipped-\`/\`used-\` 같은 활용형은 같은 원인을 다른 태그로 쪼갠다. 상태 서술형(\`missing-*-script\`)도 대상을 매번 다르게 쓰게 되므로 피한다.
4. **아래 canonical 어휘에 의미가 같은 항목이 있으면 철자 그대로 재사용하라.** 단수/복수(\`script\`/\`scripts\`), 어순, 동의어(\`pretool\`/\`pretooluse\`)를 바꿔 새 태그를 만들지 마라. 각 줄의 \`←\` 뒤에 붙은 표기는 **이미 canonical 로 접힌 과거 변형**이므로 다시 쓰지 마라.
5. **단, 어휘에 없는 새로운 종류의 사건이면 새 태그를 만들어라.** 드문 신호를 억지로 기존 태그에 끼워넣지 마라 — catch-all 로 흡수되면 집계 자체가 무의미해진다. 재사용은 "의미가 같을 때만" 이다. **새 태그를 만들었으면 \`new_tag_reason\` 줄을 반드시 붙여라** (어느 canonical 과도 근본원인이 다른 이유 1줄).
6. **표기가 닮았다고 억지로 합치지도 마라.** 특히 \`stale ...\` 계열은 대상마다 필요한 조치(위젯 재조회 / MCP 재연결 / VM 재부착)가 달라 서로 다른 원인이다. \`undesired_behavior\` 와 \`desired_behavior\` 가 **둘 다 같을 때만** 같은 태그를 쓴다.

$known_tags_block

## actionability 판정

- \`claude_behavior\` (기본값) — Claude가 다르게 행동했다면 피할 수 있었던 사건.
- \`user_environment\` — **사용자 환경/설정만 고치면 해소되고 Claude 행동으로는 막을 수 없는** 사건. 예: \`.claude/settings.json\` 이 존재하지 않는 스크립트를 참조, 훅 스크립트 실행 권한 없음, CLI 미설치, 포트 점유, 상대경로 훅이 서브디렉토리 cwd 에서 해석 실패.
- \`user_environment\` 인 경우 \`desired_behavior\` 에 **환경 수정 지시를 쓰지 마라.** "훅 스크립트를 만들어야 했다", "설정에서 훅을 제거해야 했다" 같은 문장은 Claude의 행동 개선이 아니라 사용자 작업이다. 대신 **Claude가 그 상황에서 무엇을 보고/판단했어야 하는가**를 써라 (예: "반복 실패를 무시하지 말고 환경 오설정으로 1회 보고했어야 한다").
- 판정이 애매하면 \`claude_behavior\` 를 써라. 이 필드는 반복 로깅 억제에 쓰이므로 과잉 \`user_environment\` 는 진짜 행동 신호를 삼킨다.

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

# ── 환경 오설정 반복 로깅 억제 (결정론적 dedup 게이트) ─────────────────────
# actionability: user_environment 블록은 같은 mistake_tag 가 억제 창(기본 7일) 안에
# 이미 기록돼 있으면 append 하지 않고 상태 파일의 count 만 올린다. Alertmanager 의
# group_by + repeat_interval(기본 4h) 과 같은 구조 — 같은 성격의 사건을 한 그룹으로
# 묶고 재알림 간격 안에서는 다시 알리지 않는다.
# 창 7일은 hypothesis 다: /reflect-digest 기본 period 가 7d 이므로 digest 사이클마다
# 최대 1회 재노출된다. 근거: https://prometheus.io/docs/alerting/latest/configuration/
#
# 이 게이트는 LLM 을 호출하지 않는 순수 판정이다. actionability 누락·파싱 실패·awk
# 비정상 종료 시에는 원본을 그대로 기록한다 (fail-open — 행동 신호는 절대 잃지 않는다).
# 억제해도 사건은 유실되지 않는다: .env-issues.tsv 가 first_seen/last_seen/count 를
# 보존하고 /reflect-digest 가 이를 "환경 액션 아이템" 으로 보고한다.
#
# 알려진 한계 (2026-08-13 재검증에서 확인 · 미해결) — 이 게이트의 그룹 키는 **원시 태그**다.
# 아래 awk 는 블록 안에서 mistake_tag 와 actionability 를 짝지어 읽어야 해서 라이브러리의
# tag_canon_extract(플랫 목록)를 그대로 쓸 수 없고, lemma 정규화를 여기서 다시 구현하면
# references/tag-canonicalization.md §1 의 SSOT 가 깨진다. 그 결과 같은 환경 문제가 다른
# 표기로 오면 **다른 그룹으로 보여 억제되지 않는다** — post_freq 과소집계(§0)와 같은
# 파편화가 이 경로에는 아직 남아 있다. 해소는 정규화 pass 를 스트림 필터로 노출하는
# 별도 스프린트 대상이다. **여기에 norm() 을 복제해 임시로 막지 마라.**
env_state="$log_dir/.env-issues.tsv"
env_state_tmp=$(mktemp)
env_report_tmp=$(mktemp)

filtered=$(printf '%s\n' "$summary" | awk \
  -v state="$env_state" \
  -v state_out="$env_state_tmp" \
  -v report="$env_report_tmp" \
  -v now="$(date '+%s')" \
  -v days="${REFLECT_ENV_REPEAT_DAYS:-7}" '
BEGIN {
  win = days * 86400
  sq = sprintf("%c", 39)
  while ((getline line < state) > 0) {
    n = split(line, f, "\t")
    if (n >= 4) { first[f[1]] = f[2]; last[f[1]] = f[3]; cnt[f[1]] = f[4] }
  }
  close(state)
  inblock = 0; nb = 0; kept = 0; dropped = 0; droplist = ""
}
inblock == 0 && $0 ~ /^[ \t]*```yaml[ \t]*$/ {
  inblock = 1; nb = 1; buf[1] = $0; tag = ""; act = ""
  next
}
inblock == 1 {
  nb++; buf[nb] = $0
  if ($0 ~ /^[ \t]*mistake_tag:/) {
    tag = $0
    sub(/^[ \t]*mistake_tag:[ \t]*/, "", tag)
    sub(/[ \t]*#.*$/, "", tag)
    gsub(/"/, "", tag); gsub(sq, "", tag); gsub(/[ \t]+$/, "", tag)
  }
  if ($0 ~ /^[ \t]*actionability:/) {
    act = $0
    sub(/^[ \t]*actionability:[ \t]*/, "", act)
    sub(/[ \t]*#.*$/, "", act)
    gsub(/"/, "", act); gsub(sq, "", act); gsub(/[ \t]+$/, "", act)
  }
  if ($0 ~ /^[ \t]*```[ \t]*$/) {
    inblock = 0
    drop = 0
    if (act == "user_environment" && tag != "") {
      if ((tag in last) && (now - last[tag]) < win) drop = 1
      if (!(tag in first)) first[tag] = now
      last[tag] = now
      cnt[tag] = (tag in cnt) ? cnt[tag] + 1 : 1
    }
    if (drop) { dropped++; droplist = droplist " drop=" tag }
    else { kept++; for (i = 1; i <= nb; i++) print buf[i]; print "" }
  }
  next
}
{ if ($0 !~ /^[ \t]*$/) print }
END {
  if (inblock == 1) { for (i = 1; i <= nb; i++) print buf[i]; kept++ }
  for (t in last) printf "%s\t%s\t%s\t%s\n", t, first[t], last[t], cnt[t] > state_out
  printf "kept=%d dropped=%d%s\n", kept, dropped, droplist > report
}
')
dedup_exit=$?
env_dedup_summary=$(cat "$env_report_tmp" 2>/dev/null)

if [ "$dedup_exit" -ne 0 ]; then
  log_hook_error "$log_dir" "$HOOK_NAME" "warn:env-dedup-failed exit=$dedup_exit session=$session_id"
  rm -f "$env_state_tmp" "$env_report_tmp" 2>/dev/null
else
  [ -s "$env_state_tmp" ] && mv -f "$env_state_tmp" "$env_state" 2>/dev/null
  rm -f "$env_state_tmp" "$env_report_tmp" 2>/dev/null

  env_dropped=$(printf '%s' "$env_dedup_summary" | sed -n 's/.*dropped=\([0-9]*\).*/\1/p')
  if [ -n "$env_dropped" ] && [ "$env_dropped" -gt 0 ] 2>/dev/null; then
    log_hook_error "$log_dir" "$HOOK_NAME" "env-dedup:$env_dedup_summary session=$session_id"
  fi

  if [ -z "$(printf '%s' "$filtered" | tr -d '[:space:]')" ]; then
    log_hook_error "$log_dir" "$HOOK_NAME" "skip:env-dedup-all $env_dedup_summary session=$session_id"
    exit 0
  fi
  summary="$filtered"
fi

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
