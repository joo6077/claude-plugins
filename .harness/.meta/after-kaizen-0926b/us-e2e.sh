#!/bin/bash
# 설치된 훅을 실제 claude -p 세션으로 돌리고 세션 기록의 훅 첨부를 센다.
# 사용법: us-e2e.sh <라벨> <모드: notify|quoted>
#   notify — 백그라운드 명령의 작업 알림에 「다음 세션」 이 실린다. 사용자 프롬프트에는 그 낱말이 붙어 있지 않다
#   quoted — 워크트리 2 개 · 공용 인덱스에 shared.txt 가 올라간 저장소에서 따옴표 안에 「git commit」 이 든 명령을 돌린다
L=${1:?라벨}; MODE=${2:?모드}
SP=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad
F=$SP/us-e2e-$L
rm -rf "$F"; mkdir -p "$F"
U=$(uuidgen | tr '[:upper:]' '[:lower:]')
if [ "$MODE" = notify ]; then
  cd "$F" || exit 1
  claude -p "Bash 도구를 run_in_background: true 로 한 번 불러 'sleep 5; echo 끝' 을 실행하라. description 은 '다음' 과 '세션 시험 대기' 를 빈칸 하나로 이은 글로 정확히 적어라. 그 뒤 작업 알림이 올 때까지 기다렸다가, 알림을 받으면 '받음' 이라고만 답해." \
    --session-id "$U" --model sonnet --allowedTools Bash --disallowedTools Agent Edit Write >/dev/null 2>&1 </dev/null
else
  R=$F/repo
  git init -q -b main "$R"
  ( cd "$R" && git config user.email t@t && git config user.name t && echo a > a.txt && git add . && git commit -qm init \
    && git worktree add -q "$F/wt2" -b wt2 && echo s > shared.txt && git add shared.txt )
  cd "$R" || exit 1
  claude -p "Bash 도구로 다음 명령 하나만 그대로 실행하고, 끝나면 끝이라고만 답해: printf '%s\n' 'a; git commit -m e2e'" \
    --session-id "$U" --model sonnet --allowedTools Bash --disallowedTools Agent Edit Write >/dev/null 2>&1 </dev/null
fi
T=$(find ~/.claude/projects -maxdepth 2 -name "$U.jsonl" | head -1)
echo "label=$L mode=$MODE session=$U transcript=$T"
[ -f "$T" ] || exit 1
ctx_count() {  # ctx_count <이벤트> <낱말> — 그 이벤트 훅 안내 첨부 중 낱말이 든 것의 수
  jq -c --arg e "$1" 'select(.type=="attachment") | select(.attachment.type=="hook_additional_context") | select((.attachment.hookEvent//"")==$e) | (.attachment.content|tostring)' "$T" \
    | grep -cF -- "$2"
}
if [ "$MODE" = notify ]; then
  # 알림은 기록에 사용자 줄로도, 대기 첨부로도 남는다(실측 두 모양) — 큐에 넣은 원문으로 센다
  printf 'prompt_kw=%s noti_kw=%s handoff_ctx=%s\n' \
    "$(jq -r 'select(.type=="user") | .message.content | strings' "$T" | head -1 | grep -c '다음 세션')" \
    "$(jq -c 'select(.type=="queue-operation" and .operation=="enqueue") | .content | strings | select(startswith("<task-notification>"))' "$T" | grep -c '다음 세션')" \
    "$(ctx_count UserPromptSubmit '세션 마감 감지')"
else
  printf 'pre_ctx=%s post_ctx=%s head_subject=%s\n' \
    "$(ctx_count PreToolUse '인덱스에 올라온 것')" \
    "$(ctx_count PostToolUse '방금 커밋에 실제로 들어간 것')" \
    "$(git -C "$R" log -1 --format=%s)"
fi
printf 'hook_errors=%s\n' "$(jq -c 'select(.type=="attachment") | select(.attachment.type=="hook_non_blocking_error" or .attachment.type=="hook_cancelled" or .attachment.type=="hook_blocking_error") | select(((.attachment.command//"")|test("parallel-session-guard|next-session-handoff|enforce-codex-stdin|_lib-hook-payload")))' "$T" | grep -c .)"
