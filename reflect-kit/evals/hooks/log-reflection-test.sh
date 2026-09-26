#!/usr/bin/env bash
# log-reflection.sh 시험 — 가짜 codex · claude 로 분석기 인자, err= 한 줄, 대체 경로, 코드 블록 정규화, 분석기 표식, 임시 파일 정리를 잰다.
# 가짜 codex 는 codex-cli 0.154.0 처럼 --full-auto 를 unexpected argument · 종료 코드 2 로 거부하고, 성공해도 stderr 에
# 머리글과 받은 프롬프트를 찍는다. 가짜 claude 는 모르는 모델 이름을 종료 코드 1 로 거부한다 (둘 다 2026-09-25 실측 모양).
# 다른 훅 사본으로 돌리기: REFLECT_KIT_HOOKS=<hooks 폴더 사본> bash log-reflection-test.sh
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HOOKS=${REFLECT_KIT_HOOKS:-$(cd "$HERE/../../hooks" && pwd)}
for h in log-reflection.sh log-prompt.sh log-tool-failure.sh; do
  [ -f "$HOOKS/$h" ] || { echo "훅이 없다 — $HOOKS/$h"; exit 2; }
done
command -v jq >/dev/null 2>&1 || { echo "jq 가 없다 — 훅이 입력을 못 읽는다"; exit 2; }

W=$(mktemp -d "${TMPDIR:-/tmp}/lrt.XXXXXX") || exit 2
trap 'rm -rf "$W"' EXIT
mkdir -p "$W/bin" "$W/tmp" "$W/in" "$W/proj" "$W/home"
CALLS=$W/calls.log
MARK=TRANSCRIPT-MARKER-7f3a
# 분석기 호출 기록 — 인자를 [ ] 로 감싸 한 줄에 적고 분석기 표식 값을 붙인다
cat > "$W/bin/codex" <<'EOF'
#!/usr/bin/env bash
{ printf 'codex'; for a in "$@"; do printf ' [%s]' "$a"; done; printf ' analyzer=[%s]\n' "${REFLECT_KIT_ANALYZER:-}"; } >> "$CALLS"
out=""; prev=""
for a in "$@"; do
  if [ "$a" = "--full-auto" ]; then
    printf "error: unexpected argument '--full-auto' found\n\n  tip: to pass '--full-auto' as a value, use '-- --full-auto'\n\nFor more information, try '--help'.\n" >&2
    exit 2
  fi
  [ "$prev" = "--output-last-message" ] && out=$a
  prev=$a
done
printf 'OpenAI Codex v0.154.0\n--------\nsandbox: read-only\n--------\nuser\n%s\n' "$(cat)" >&2
case "${FAKE_CODEX:-ok}" in
  ok) printf '```yaml\nprimary_category: misunderstanding\nmistake_tag: skip-test-tag\nactionability: claude_behavior\n```\n' > "$out"; exit 0 ;;
  limit) printf "ERROR: You've hit your usage limit. Try again at 11:05 PM.\n" >&2; exit 1 ;;
  crash) exit 3 ;;
  empty) exit 0 ;;
  noissues) printf 'no issues\n' > "$out"; exit 0 ;;
  # 형식을 안 따른 출력 — 코드 블록 없음 · 빈 줄로 나뉜 두 블록 · 언어 없는 fence · 환경 블록 · 산문
  nofence1) printf 'primary_category: misunderstanding\nmistake_tag: nofence-one-tag\nactionability: claude_behavior\n' > "$out"; exit 0 ;;
  nofence2) printf 'primary_category: misunderstanding\nmistake_tag: nofence-a-tag\n\nprimary_category: wrong_approach\nmistake_tag: nofence-b-tag\n' > "$out"; exit 0 ;;
  barefence) printf '```\nprimary_category: tool_failure\nmistake_tag: bare-fence-tag\n```\n' > "$out"; exit 0 ;;
  envnofence) printf 'primary_category: tool_failure\nmistake_tag: env-repeat-tag\nactionability: user_environment\n' > "$out"; exit 0 ;;
  prose) printf 'PROSE-LINE 요약 문장만 있다\n' > "$out"; exit 0 ;;
esac
EOF
cat > "$W/bin/claude" <<'EOF'
#!/usr/bin/env bash
model=""; prev=""
for a in "$@"; do [ "$prev" = "--model" ] && model=$a; prev=$a; done
{ printf 'claude'; for a in "$@"; do printf ' [%s]' "$a"; done; printf ' analyzer=[%s]\n' "${REFLECT_KIT_ANALYZER:-}"; } >> "$CALLS"
cat > /dev/null
case "$model" in
  haiku|sonnet|opus|claude-*) ;;
  *) echo "There's an issue with the selected model ($model). It may not exist or you may not have access to it."
     echo "\"$model\" isn't described by this version's model catalog" >&2; exit 1 ;;
esac
case "${FAKE_CLAUDE:-ok}" in
  ok) printf '```yaml\nprimary_category: wrong_approach\nmistake_tag: skip-fallback-tag\nactionability: claude_behavior\n```\n'; exit 0 ;;
  # 키가 185 자 뒤에서 시작한다 — 200 자로 먼저 자르면 키 8 자가 남아 가림 패턴(10 자 이상)에 안 걸린다
  secret) printf 'API Error: 401 %s sk-ant-%s rejected\n' "$(printf 'x%.0s' $(seq 1 169))" "$(printf 'Q7%.0s' $(seq 1 30))" >&2; exit 1 ;;
  stdoutonly) echo "Credit balance is too low"; exit 1 ;;
esac
EOF
chmod 755 "$W/bin/codex" "$W/bin/claude"

T=$W/in/transcript.jsonl
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do printf '{"type":"user","message":{"content":"line %s %s"}}\n' "$i" "$MARK"; done > "$T"
LOGD=$W/home/.claude/logs/proj
ERRS=$LOGD/.errors.log
n=0; bad=0
check() {  # check <이름> <답> <값>
  n=$((n + 1))
  if [ "$2" = "$3" ]; then echo "일치 $1"
  else echo "불일치 $1 — 값 [$3] (답 [$2])"; bad=$((bad + 1)); fi
}
run_bg() {  # run_bg <session> <FAKE_CODEX> <FAKE_CLAUDE> [추가 env...]
  local sid=$1 in=$W/in/$1.json
  shift
  local fc=$1 fl=$2
  shift 2
  jq -cn --arg s "$sid" --arg t "$T" --arg c "$W/proj" '{session_id: $s, transcript_path: $t, cwd: $c}' > "$in"
  : > "$CALLS"
  env HOME="$W/home" TMPDIR="$W/tmp" PATH="$W/bin:$PATH" CALLS="$CALLS" FAKE_CODEX="$fc" FAKE_CLAUDE="$fl" "$@" \
    bash "$HOOKS/log-reflection.sh" --background "$in" > /dev/null 2>&1
}
errs_of() { grep -F " session=$1" "$ERRS" 2>/dev/null | grep -E '\] (fail|fallback|skip):' | sed -E 's/^[^]]*\] //'; }
recorded() { grep -cxF -- "- session: \`$1\`" "$LOGD"/reflections-*.md 2>/dev/null | awk -F: '{s += $NF} END {print s + 0}'; }
fences_of() {  # fences_of <session> — 그 세션 절의 yaml 여는 줄 수 / 맨 fence 줄 수
  awk -v s="- session: \`$1\`" '/^## /{on = 0} $0 == s {on = 1} on && /^```yaml$/ {yaml++} on && /^```$/ {bare++} END {printf "%d/%d", yaml, bare}' "$LOGD"/reflections-*.md 2>/dev/null
}

# 1. codex 성공 — 읽기 전용 인자 · --full-auto 없음 · 분석기 표식 · 대체 경로 안 부름
run_bg S1 ok ok
check "codex 인자 -s read-only" 1 "$(grep -c '^codex .*\[-s\] \[read-only\]' "$CALLS")"
check "codex 인자 --full-auto 없음" 0 "$(grep -c '\[--full-auto\]' "$CALLS")"
check "codex 분석기 표식" 1 "$(grep -c '^codex .* analyzer=\[1\]$' "$CALLS")"
check "codex 성공 시 claude 호출 없음" 0 "$(grep -c '^claude' "$CALLS")"
check "codex 성공 기록" 1 "$(grep -h -c 'skip-test-tag' "$LOGD"/reflections-*.md 2>/dev/null | awk '{s += $1} END {print s + 0}')"
check "codex 성공 실패 줄 없음" "" "$(errs_of S1)"

# 2. codex 한도 초과 → 대체 경로 성공 — err= 는 ERROR 줄 · 대체 경로 인자
run_bg S2 limit ok
check "codex 실패 err= ERROR 줄" "fail:codex-exit-1 session=S2 err=ERROR: You've hit your usage limit. Try again at 11:05 PM.
fallback:claude-used session=S2" "$(errs_of S2)"
check "claude 인자 --model haiku" 1 "$(grep -c '^claude .*\[--model\] \[haiku\]' "$CALLS")"
check "claude 인자 --no-session-persistence" 1 "$(grep -c '^claude .*\[--no-session-persistence\]' "$CALLS")"
check "claude 인자 --safe-mode" 1 "$(grep -c '^claude .*\[--safe-mode\]' "$CALLS")"
check "claude 분석기 표식" 1 "$(grep -c '^claude .* analyzer=\[1\]$' "$CALLS")"
check "대체 경로 기록" 1 "$(recorded S2)"

# 3. codex 가 error 줄 없이 죽음 — err= 는 비어 있지 않은 첫 줄(머리글)이고 프롬프트 전문은 안 남는다
run_bg S3 crash ok
check "codex 실패 err= 첫 줄" "fail:codex-exit-3 session=S3 err=OpenAI Codex v0.154.0
fallback:claude-used session=S3" "$(errs_of S3)"
check "transcript 가 .errors.log 에 없음" 0 "$(grep -c "$MARK" "$ERRS")"

# 4. 대체 경로 실패 — 키가 든 stderr 는 가린 뒤 자른다
run_bg S4 limit secret
check "대체 경로 실패 줄 1" 1 "$(errs_of S4 | grep -c '^fallback:claude-exit-1 session=S4 err=API Error: 401 x')"
check "키 조각 없음" 0 "$(grep -c 'sk-ant-' "$ERRS")"
check "err= 200 자 이하" 1 "$(errs_of S4 | awk -F' err=' '/^fallback:/ {print (length($2) <= 200) ? 1 : 0}')"
check "대체 경로 실패 시 기록 없음" 0 "$(recorded S4)"

# 5. 대체 경로 stderr 가 비면 stdout 에서 고른다
run_bg S5 limit stdoutonly
check "stdout 에서 고른 err=" "fallback:claude-exit-1 session=S5 err=Credit balance is too low" "$(errs_of S5 | grep '^fallback:')"

# 6. codex 빈 응답 — err= 없이 적는다
run_bg S6 empty ok
check "codex 빈 응답 줄" "fail:codex-empty-output session=S6
fallback:claude-used session=S6" "$(errs_of S6)"

# 6-1. 분석 결과 no issues — 기록은 없고 정상 종료 한 줄이 남는다
run_bg S8 noissues ok
check "no issues 정상 종료 줄" 1 "$(grep -c '\] ok:no-issues session=S8$' "$ERRS")"
check "no issues 기록 없음" 0 "$(recorded S8)"

# 6-2. 코드 블록 없는 출력은 yaml 블록으로 감싸 적는다 — 답은 블록 수에서 손으로 정했다
run_bg N1 nofence1 ok
check "코드 블록 없는 한 블록 — 감쌈" "1/1" "$(fences_of N1)"
run_bg N2 nofence2 ok
check "코드 블록 없는 두 블록 — 둘로 감쌈" "2/2" "$(fences_of N2)"
run_bg N3 barefence ok
check "언어 없는 fence — yaml 로" "1/1" "$(fences_of N3)"
run_bg N4 prose ok
check "산문 — 그대로 적고 블록을 안 지어냄" "1 1 0/0" "$(recorded N4) $(grep -c '^PROSE-LINE ' "$LOGD"/reflections-*.md) $(fences_of N4)"
# 코드 블록 없는 환경 블록도 억제 게이트가 본다 — 두 번째 세션은 억제되고 count 는 2
run_bg E1 envnofence ok
run_bg E2 envnofence ok
check "코드 블록 없는 환경 블록 — 두 번째 억제" "1 0 1 2" \
  "$(recorded E1) $(recorded E2) $(grep -c '\] skip:env-dedup-all .* session=E2$' "$ERRS") $(awk -F'\t' '$1 == "env-repeat-tag" {print $4}' "$LOGD/.env-issues.tsv" 2>/dev/null)"

# 7. 분석기 표식이 있으면 세 훅 모두 아무것도 적지 않는다 — 표식 없는 같은 입력은 적는다(양성 대조)
before=$(find "$W/home" -type f | wc -l | tr -d ' ')
run_bg S7 ok ok REFLECT_KIT_ANALYZER=1
check "표식 — Stop 분석 안 함" "0 0 $before" "$(grep -c . "$CALLS") $(recorded S7) $(find "$W/home" -type f | wc -l | tr -d ' ')"
# 훅마다 다른 폴더에서 부른다 — 한 폴더를 같이 쓰면 앞 훅이 쓴 파일이 뒤 훅의 값에 섞인다
for h in log-prompt.sh log-tool-failure.sh; do
  d=$W/p-${h%.sh}; mkdir -p "$d"
  jq -cn --arg c "$d" '{session_id: "P1", cwd: $c, prompt: "hello prompt", tool_name: "Bash", tool_input: {command: "x"}, tool_response: {error: "y"}}' \
    | env HOME="$W/home" TMPDIR="$W/tmp" REFLECT_KIT_ANALYZER=1 bash "$HOOKS/$h" > /dev/null 2>&1
  check "표식 — $h 안 적음" 0 "$(find "$W/home/.claude/logs/p-${h%.sh}" -type f -name '20*.md' 2>/dev/null | wc -l | tr -d ' ')"
done
mkdir -p "$W/p-plain"
jq -cn --arg c "$W/p-plain" '{session_id: "P1", cwd: $c, prompt: "hello prompt"}' \
  | env HOME="$W/home" TMPDIR="$W/tmp" bash "$HOOKS/log-prompt.sh" > /dev/null 2>&1
check "표식 없음 — log-prompt.sh 적음" 1 "$(grep -hc 'hello prompt' "$W/home/.claude/logs/p-plain"/20*.md 2>/dev/null | awk '{s += $1} END {print s + 0}')"

# 8. 임시 파일이 남지 않는다
check "TMPDIR 비었음" 0 "$(find "$W/tmp" -mindepth 1 | wc -l | tr -d ' ')"

echo "결과: $n 경우 중 불일치 $bad"
[ "$bad" = 0 ]
