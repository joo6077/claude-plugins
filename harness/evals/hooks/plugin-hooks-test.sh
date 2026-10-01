#!/usr/bin/env bash
# harness 플러그인 훅 lint-contract-oracle.sh · qa-pending-check.sh 가 hooks.json 에 적힌 그대로 도는지 본다.
# hooks.json 의 명령 글자를 꺼내 CLAUDE_PLUGIN_ROOT 만 플러그인 폴더 사본으로 주고 훅 입력 JSON 을 넣어 돌린다.
# 사본 경로에 빈칸을 넣는다 — 명령의 따옴표가 빠지면 셸이 경로를 둘로 쪼개 훅이 안 돈다.
# HOME 을 빈 폴더로, CLAUDE_HOOK_LIB 를 지운 채 돌린다 — ~/.claude/hooks/ 없이 플러그인 안 도우미로 돌아야 한다.
# PLUGIN_HOOKS_ROOT 로 플러그인 폴더(기본: 이 파일 기준 harness/)를 바꿀 수 있다 — 고치기 전 판으로 음성 대조를 돌릴 때 쓴다.
# 종료 코드: 0 통과 · 1 실패 · 2 준비 실패 (플러그인 폴더 · hooks.json · jq 없음)

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
root=${PLUGIN_HOOKS_ROOT:-$here/../..}
[ -f "$root/hooks/hooks.json" ] || { echo "hooks.json 이 없다: $root/hooks/hooks.json" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "jq 가 없다" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/plugin-hooks-test.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
plugin="$work/plugin root"
mkdir -p "$plugin" "$work/home"
cp -R "$root/hooks" "$root/scripts" "$plugin/" || exit 2
fails=0

check() {  # check <이름> <기대> <실제>
  if [ "$2" = "$3" ]; then echo "PASS $1"; else printf 'FAIL %s — 기대 [%s] 실제 [%s]\n' "$1" "$2" "$3"; fails=$((fails + 1)); fi
}

# 훅 파일 이름이 든 등록을 「이벤트 · matcher · timeout · statusMessage」 한 줄로. 여러 개면 여러 줄이다
registration() {  # registration <훅 파일 이름>
  jq -r --arg n "$1" '.hooks | to_entries[] | .key as $e | .value[] | (.matcher // "-") as $m
    | .hooks[] | select(.command | contains($n)) | "\($e) \($m) \(.timeout) \(.statusMessage)"' "$plugin/hooks/hooks.json"
}
command_of() {  # command_of <훅 파일 이름> — hooks.json 의 명령 글자 그대로
  jq -r --arg n "$1" '[.hooks[][].hooks[] | select(.command | contains($n)) | .command][0] // empty' "$plugin/hooks/hooks.json"
}
run_hook() {  # run_hook <훅 파일 이름> <입력 JSON> — 훅이 모델에 넣은 안내문
  printf '%s' "$2" \
    | env -u CLAUDE_HOOK_LIB HOME="$work/home" CLAUDE_PLUGIN_ROOT="$plugin" bash -c "$(command_of "$1")" \
    | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null
}

check "등록-계약오라클" "PostToolUse Edit|Write 10 계약 오라클 린터" "$(registration lint-contract-oracle.sh)"
check "등록-QA대기" "Stop - 10 QA 실행 여부 확인" "$(registration qa-pending-check.sh)"

project=$work/project
mkdir -p "$project/.harness"
contract=$project/.harness/sprint-contract-x.md
printf -- '---\nstatus: active\nowner_session: S1\nlocked_at: "2026-10-01 10:00"\n---\n\n## Skill\n- [ ] 스킬-01: x\n  측정: `grep -cF "표준으로 강제하지 않는다" file.md` >= 1\n' >"$contract"
cp "$contract" "$project/notes.md"

lint_input() { jq -nc --arg f "$1" '{tool_name:"Write",tool_input:{file_path:$f}}'; }
check "계약편집-경고" 1 "$(run_hook lint-contract-oracle.sh "$(lint_input "$contract")" | grep -c '계약 오라클 경고')"
check "계약아닌파일-조용" "" "$(run_hook lint-contract-oracle.sh "$(lint_input "$project/notes.md")")"

stop_input() { jq -nc --arg s "$1" --arg d "$project" --argjson a "$2" '{session_id:$s,cwd:$d,transcript_path:"",stop_hook_active:$a}'; }
check "내계약QA없음-안내" 1 "$(run_hook qa-pending-check.sh "$(stop_input S1 false)" | grep -c 'sprint-contract-x.md')"
check "남의계약-조용" "" "$(run_hook qa-pending-check.sh "$(stop_input S2 false)")"
check "되돌린답-조용" "" "$(run_hook qa-pending-check.sh "$(stop_input S1 true)")"

echo "실패 $fails 건"
[ "$fails" = 0 ]
