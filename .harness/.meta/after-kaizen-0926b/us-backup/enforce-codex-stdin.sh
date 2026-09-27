#!/usr/bin/env bash
# stdin 을 닫지 않은 `codex exec` 호출을 차단한다.
#
# 근거 — memory feedback_codex_stdin_must_be_closed (2026-09-12 실측):
#   stdin 이 열린 채로 부르면 codex 가 `Reading additional input from stdin...` 에서
#   무한 대기한다. 세션 id 는 찍히지만 rollout 파일을 만들지 않아 «멈춘 것» 으로 오진된다.
#   같은 프롬프트가 3 회 연속 실패했고 `</dev/null` 하나로 115 초에 완료됐다.
#
# 규칙 문서와 래퍼만으로는 막히지 않는다 — 규칙은 세션 시작 때만 읽히고, 래퍼는 쓰지 않으면
# 그만이며, 손으로 친 명령은 어느 파일도 읽지 않는다. 그래서 호출 지점에서 막는다.
#
# 통과시키는 것 (오탐 방지):
#   - `</dev/null` · `< /dev/null` 이 있는 호출
#   - `~/.claude/bin/codex-research` 래퍼 (안에서 이미 닫는다)
#   - 파이프 입력을 «의도한» 호출 — `cat x | codex exec -` 처럼 `-` 를 명시한 경우
#   - heredoc 본문·주석에 적힌 예시 문자열 (문서를 쓰다 자기 차단되지 않게)
#
# fail-open: jq 부재·빈 stdin·깨진 JSON 어느 경우에도 exit 0. errexit 를 쓰지 않는다.
set -uo pipefail

LIB="${CLAUDE_HOOK_LIB:-$HOME/.claude/hooks/_lib-hook-payload.sh}"
# shellcheck source=/dev/null
. "$LIB" 2>/dev/null || exit 0

payload="$(cat 2>/dev/null || true)"
[ -n "$payload" ] || exit 0

tool="$(hook_field "$payload" '.tool_name')"
[ "$tool" = "Bash" ] || exit 0

raw="$(hook_field "$payload" '.tool_input.command')"
[ -n "$raw" ] || exit 0

# heredoc 본문을 데이터로 보고 판정에서 제거한다. 문서·테스트에 codex 명령을 적을 때마다
# 자기 차단되면 우회를 유발한다 — block-dirwide-autofixer.sh 가 같은 이유로 같은 처리를 한다.
cmd="$(printf '%s\n' "$raw" | awk '
  !inhd {
    if (match($0, /<<-?[[:space:]]*["'"'"']?[A-Za-z_][A-Za-z0-9_]*["'"'"']?/)) {
      m = substr($0, RSTART, RLENGTH)
      sub(/^<<-?[[:space:]]*/, "", m)
      gsub(/["'"'"']/, "", m)
      marker = m; inhd = 1; print; next
    }
    print; next
  }
  inhd {
    line = $0
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
    if (line == marker) { inhd = 0 }
    next
  }
')"

# 주석 줄은 명령이 아니다.
cmd="$(printf '%s\n' "$cmd" | sed 's/^[[:space:]]*#.*$//')"

# `codex exec` 호출이 실제로 있는가. 명령 위치(줄 시작 · 파이프 · && · ; · $( 뒤)만 본다.
#
# 실행 래퍼 뒤도 명령 위치다. `perl -e 'alarm shift; exec @ARGV' <초> codex exec …` 는
# 템플릿이 상한 방법으로 «권장하는» 형태인데, 래퍼를 안 보면 그 권장 형태가 이 방어를
# 그대로 지나간다 — 실측에서 perl · env · nohup 셋 다 통과했고 실제 stdin 대기에 걸렸다.
#
# 래퍼를 이름으로 열거하는 것은 금지 목록이라 여기 없는 래퍼는 여전히 새어 나간다.
# 그래도 목록을 쓰는 이유는 오탐이 0 이어야 하기 때문이다 — 위치 제한을 풀면 문자열 인자로
# `codex exec` 를 넘기는 명령(이 훅을 시험하는 명령 자신이 그렇다)까지 막혀 훅을 꺼버리게 된다.
# 목록 밖 래퍼와 스크립트 파일 경유는 못 막는다. 그 한계는 템플릿 「멈추면」 절에 적혀 있다.
launchers='perl|env|nohup|xargs|stdbuf|timeout|gtimeout|nice|setsid|caffeinate|command|sudo|time'
cmd_pos='(^|[|;&]|\$\()[[:space:]]*'
codex_call='(/[^[:space:]]*/)?codex[[:space:]]+(exec|e)([[:space:]]|$)'

printf '%s\n' "$cmd" | grep -qE "${cmd_pos}${codex_call}" \
  || printf '%s\n' "$cmd" | grep -qE "${cmd_pos}(${launchers})([[:space:]]|$).*${codex_call}" \
  || exit 0

# 래퍼를 통한 호출은 통과 — 래퍼가 stdin 을 닫는다.
printf '%s\n' "$cmd" | grep -q 'codex-research' && exit 0

# stdin 을 이미 닫았으면 통과.
printf '%s\n' "$cmd" | grep -qE '<[[:space:]]*/dev/null' && exit 0

# 파이프 입력을 의도한 호출은 통과 — `-` 로 stdin 을 프롬프트로 쓴다고 명시한 경우.
# 두 갈래를 따로 본다. 하나로 합치면 `exec` 뒤 공백이 `[[:space:]]+` 에 먹혀
# `codex exec -` 처럼 `-` 가 «바로» 오는 형태를 놓친다 (실측 오탐).
printf '%s\n' "$cmd" | grep -qE 'codex[[:space:]]+(exec|e)[[:space:]]+-([[:space:]]|$)' && exit 0
printf '%s\n' "$cmd" | grep -qE 'codex[[:space:]]+(exec|e)[[:space:]].*[[:space:]]-([[:space:]]|$)' && exit 0

hook_deny "stdin 을 닫지 않은 \`codex exec\` 는 무한 대기한다 — \`</dev/null\` 을 붙여라. codex 는 stdin 이 열려 있으면 \`Reading additional input from stdin...\` 에서 멈추고, 세션 id 만 찍은 뒤 rollout 파일조차 만들지 않아 «응답 없음» 으로 보인다 (2026-09-12 실측: 같은 프롬프트가 3 회 연속 실패 → \`</dev/null\` 하나로 115 초 완료). 파이프(\`| tail\`)나 배경 실행 안에서 특히 잘 걸린다. 고치는 법: 프롬프트 인자 «뒤», 파이프 «앞» 에 \`</dev/null\` 을 넣어라 — \`codex exec --model gpt-5.6-sol -s read-only -o <파일> \"\$(cat <프롬프트>)\" </dev/null 2>&1 | tail -40\`. 리서치라면 \`~/.claude/bin/codex-research <프롬프트파일> <출력파일>\` 을 쓰는 게 낫다 — stdin 차단·상한·조기 감지·재시도가 들어 있어 멈춘 실행을 25 초에 판정한다. stdin 을 «프롬프트로» 넘기려는 의도였다면 \`codex exec -\` 처럼 \`-\` 를 명시하라 — 그건 통과한다."
