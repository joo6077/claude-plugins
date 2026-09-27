#!/bin/bash
# 사용자 프롬프트에서 세션 마감 신호를 감지하고 handoff 블록 생성 리마인더를 출력
INPUT=$(cat)
# 작업 알림은 사용자 글이 아닌데 prompt 칸으로 들어온다. 알림에 든 명령 설명의 「다음 세션」 에 반응하지 않게 그 구간을 뺀다.
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty | gsub("<task-notification>[\\s\\S]*?</task-notification>"; "")' 2>/dev/null)

if echo "$PROMPT" | grep -qE '다음 세션|이어서 하자|오늘 여기까지|세션 마무리|내일 이어가자|다음에 하자|다음에 이어'; then
  cat <<'HANDOFF'
{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "[세션 마감 감지] 다음 세션 복붙 블록을 생성하라. 포맷:\n```\n[이전 세션 이어서 진행]\n브랜치: <branch> @ <commit-sha>\n오늘까지 완료: <한 줄>\n다음 작업: <한 줄>\n폐기한 결정: <항목> — 원문 자리 <그 기능 PRD 비범위 표 경로, 없으면 작업 계약 범위 경계 절, 둘 다 없으면 승인 기록 경로> (결정을 옮겨 적지 않는다. 항목이 없으면 없음)\n참고 문서:\n- <경로>\n재개 지시:\n<구체 다음 스텝>\n```\n실제 git log/파일 경로 확인 후 사실 기반으로 채울 것. 추측 금지."}}
HANDOFF
fi
