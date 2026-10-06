# 개정 1 독립 검토 절차와 결과 형식

판정 권위는 구현자와 다른 새 평가자에게 있다. 이 문서나 측정 작성자가 검토 결과를 대신 만들지 않는다. 결과 경로는 `.harness/.meta/codex-audit-progress/evidence/cli-review.json`이다. 아래는 형식 설명이며 실제 결과 파일이 아니다. 모든 경로는 evidence 상대 경로, 줄 번호는 1부터 시작한다.

검토자는 stream 6개, session.txt, drive-trial.py, 부모 기록 전체, 연결된 자식 기록, Bash follow 작업 출력과 Monitor 알림을 직접 읽는다. 작업 호출의 tool_use_id → tool_result.backgroundTaskId → tasks/<id>.output을 따라간다. Monitor의 필터 출력은 Bash follow 전체 출력의 대체물이 아니다. 실행기가 적은 요청과 실제 사람이 보낸 메시지 전체를 대조하고, 알림을 사람의 요청으로 세지 않는다. 구현 커밋과 실제 사용 스크립트가 이 가지의 구현인지 확인하며, 원본 진위·검토자 독립성·새 평가자 여부는 식별 문자열만으로 증명되지 않는다.

부모 assistant의 text 블록만 채팅이다. 도구 입력·출력·thinking·사용자 알림·자식 답변은 채팅이 아니다. 각 relay_line 대상에 같은 종류·회차·조건·결과가 전달되어야 한다. 한 채팅이 여러 사건을 명확히 담으면 여러 매핑에서 참조할 수 있다. 단순 “진행 중”은 불충분하다. 의미 동등성과 일반 요약을 바꿔 말한 전달·불필요한 깨움은 전체 문맥으로 검토한다. 기계 측정의 15초 내 텍스트 후보는 필요조건일 뿐 의미 전달의 PASS가 아니다.

시각: 부모 JSONL의 UTC timestamp와 follow의 [HH:MM:SS]를 사용한다. 이 수집의 로컬 시간은 Asia/Seoul이며, 부모 시작일의 KST 날짜를 붙이고 자정을 넘으면 날짜를 올린다. 검토자는 Monitor 알림에 든 동일 사건의 시각과 UTC 수신 시각으로 이 오프셋·날짜를 확인한다. 예: parent:71의 UTC `2026-10-06T08:43:43.301Z` 알림은 `[17:43:37]` 사건을 담는다. stdout_at은 이 규칙으로 계산한 epoch, chat_at은 부모 레코드 timestamp의 epoch이며 자기 신고 시각으로 덮어쓰지 않는다. 초 단위 출력의 경계 오차는 임의로 15초 기준을 늘려 해결하지 않는다.

작업 출력이 감독 중 자랐는지는 시작/종료 사이 서로 다른 시각의 출력과 당시 알림·중간 읽기를 대조한다. 마지막에 모은 파일 하나만으로 실제 쓰기 시각을 확정하지 않는다. `growth_locations`에 출력 줄 범위와 원본 관측 위치·시각을 적고 근거 부족이면 FAIL한다. Monitor가 별도 follow를 실행했다면 그것만으로 Bash 작업 파일 성장까지 확증하지 않는다.

```json
{
  "reviewer": "실제 독립 검토자 ID",
  "reviewer_session": "구현자와 다른 새 검토 세션 ID",
  "implementer": "실제 구현자 ID",
  "parent_session": "session.txt의 ID",
  "evidence_sha256": {"evidence 상대 경로 각각": "파일 전체 sha256 64자리"},
  "cases": [{
    "verb": "draft 또는 revise 또는 impl",
    "route": "direct 또는 delegated",
    "stream": "해당 stream 파일명",
    "stdout": "tasks/부모-Bash-follow-ID.output",
    "follow_tool_use_id": "부모 follow 호출 ID",
    "supervisor_tool_use_id": "부모 Bash 또는 Agent 호출 ID",
    "implementation_revision": "직접 확인한 실행 구현 커밋",
    "implementation_revision_verified": true,
    "originals_authentic": true,
    "no_progress_request": true,
    "no_summary_relay_or_wakeup": true,
    "follow_output_grew_during_supervision": true,
    "growth_locations": ["출력 줄 및 당시 관측의 파일:줄·시각·대조 근거"],
    "phases": [{
      "stdout_location": 1,
      "stdout_line": "시간 접두부를 포함한 실제 출력 한 줄",
      "stdout_at": 0,
      "transcript_location": 1,
      "chat_line": "부모 assistant text에 실제 있는 비어 있지 않은 문자열",
      "chat_at": 0,
      "same_kind_round_conditions_result": true
    }],
    "review_verdict": "PASS 또는 FAIL",
    "reason": "직접 대조한 위치와 의미·시각·성장·실행 커밋·독립성의 근거 또는 실패 이유"
  }]
}
```

cases는 6개를 정확히 채운다. phases는 기존 measure.py의 relay_line이 참인 Bash follow 출력의 모든 줄을 중복 없이 한 번씩 포함한다. 활동 요약·사전 측정 중간 줄을 포함하지 않는다. evidence_sha256은 결과 자신을 제외한 evidence의 모든 파일(자식 meta·Monitor 출력 포함)을 열거한다. 측정 stdout의 해시 목록을 참고하되 검토자가 원본 바이트를 직접 검증한다. true는 실제 확인한 경우만 쓰며 확인 못 한 항목은 false와 이유를 쓴다. 독립 검토 FAIL 또는 누락, 기계 검사 FAIL 중 하나라도 있으면 전체 FAIL이다.

사전 측정 명령은 `bash .harness/.meta/codex-audit-progress/measure/measure.sh 스킬-02`, 음성 대조는 끝에 `--negative`를 붙인다. 감독의 판정 격리 밖에서 원본 증거를 읽는 호스트 사전 측정으로 실행하고 출력·종료 코드를 동결해 판정자에게 준다. 이 측정은 구현을 실행하지 않고 기존 measure.py의 snapshot/격리를 호출하지 않는다. 현재 실행 호스트의 OS sandbox를 스스로 해제하는 기능은 없다. 기존 project.yaml이나 구현은 이 개정에서 수정하지 않는다.
