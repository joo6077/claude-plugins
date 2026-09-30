#!/bin/bash
# 쉬운 말 목록 파일 하나로 목록 읽개 · 기록 훅 · 상기 훅을 돌린다. 훅은 임시 HOME 에서 돌아 실제 기록 파일을 건드리지 않는다.
# 쓰는 법: bash plain-korean-hooks.sh <목록 파일>
# 출력: `abbr=<허용 약자 수> seven=<SK SC ER AR RE DG AP 가운데 남은 수> pairs=<바꿔 쓸 말 수> words=<허용 낱말 수>`
#       `check_rc=<기록 훅 종료 코드> verdict=<pass|miss> words=<샌 낱말 JSON>`   (보낸 답: 「조건 SK-01 을 확인했다」)
#       `remind_rc=<상기 훅 종료 코드> remind_seven=<상기 문구 약자 줄에 남은 일곱의 수>`
glossary=${1:?목록 파일}; hooks=$HOME/.claude/hooks; parser=$hooks/_plain-korean-glossary.py
python3 - "$parser" "$glossary" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("glossary", sys.argv[1]); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
data = mod.load(sys.argv[2]); abbr = data["allow_abbr"]
print(f"abbr={len(abbr)} seven={sum(x in abbr for x in 'SK SC ER AR RE DG AP'.split())} pairs={len(data['pairs'])} words={len(data['allow_word'])}")
PY
tmp=$(mktemp -d "${TMPDIR:-/tmp}/pkhooks.XXXXXX"); mkdir -p "$tmp/.claude"; trap 'rm -rf "$tmp"' EXIT
jq -nc --arg m "조건 SK-01 을 확인했다" '{last_assistant_message: $m}' \
  | HOME="$tmp" PLAIN_KOREAN_GLOSSARY="$glossary" PLAIN_KOREAN_PARSER="$parser" CLAUDE_HOOK_LIB="$hooks/_lib-hook-payload.sh" bash "$hooks/check-plain-korean.sh"
check_rc=$?
printf 'check_rc=%s verdict=%s words=%s\n' "$check_rc" "$(jq -r .verdict "$tmp/.claude/.plain-korean-last.json" 2>/dev/null)" "$(jq -c .words "$tmp/.claude/.plain-korean-misses.jsonl" 2>/dev/null)"
out=$(printf '{"hook_event_name":"UserPromptSubmit","prompt":"x"}' \
  | HOME="$tmp" PLAIN_KOREAN_GLOSSARY="$glossary" PLAIN_KOREAN_PARSER="$parser" CLAUDE_HOOK_LIB="$hooks/_lib-hook-payload.sh" bash "$hooks/remind-plain-korean.sh")
remind_rc=$?
seven=$(printf '%s\n' "$out" | grep -o '설명 없이 써도 되는 대문자 약자: .*' | tr ' ' '\n' | grep -cxE 'SK|SC|ER|AR|RE|DG|AP')
printf 'remind_rc=%s remind_seven=%s remind_bytes=%s\n' "$remind_rc" "$seven" "$(printf '%s' "$out" | wc -c | tr -d ' ')"
