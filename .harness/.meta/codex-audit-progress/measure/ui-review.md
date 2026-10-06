# 부모 대화 화면 실사용 측정

이 절차는 스킬-02 측정의 일부다. measure.py의 PASS만으로 화면 동작을 인정하지 않는다. 구현자와 다른 검토자가 원본 대화와 캡처를 직접 열고 아래 항목을 확인한 뒤 ui-review.json을 작성한다. 없는 실행을 손 예제로 채우거나 가짜 Codex CLI 성공을 화면 증거로 옮기지 않는다.

1. 구현 커밋 U의 플러그인을 사용하는 VS Code Claude Code 확장에서 새 부모 세션을 연다. 진행 창을 요청하지 않고 draft, revise, impl을 각각 실행한다. 각 종류를 부모 직접 호출과 평가자 위임 경로로 반복한다. 총 사례 수는 Python `len(list(itertools.product(('draft','revise','impl'),('direct','delegated'))))`로 구한다. 감독은 최소 두 단계가 보이게 실행한다.
2. 원본 대화 내보내기(도구 호출과 부모/자식 세션 식별 포함), 실제 follow stdout, 작업 카드가 서로 다른 단계로 갱신되는 화면 캡처를 보존한다. 캡처는 한 파일에 두 시점 이상을 담은 이미지/PDF여도 된다. 진행 표시 요청이 없었는지 전체 대화를 확인한다.
3. 부모가 follow를 run_in_background로 시작했는지 확인한다. 자식 내부 Bash 출력은 부모 카드의 대체 증거가 아니다. 첫 단계 전에 follower가 살아 있고, 감독 중 카드가 실제 갱신되며, 큰 단계·오류·조용함 경고·최종 판정 줄만 15초 내 부모 채팅에 옮겨졌는지 직접 대조한다. 상태줄·OS 알림·사용자가 파일을 여는 동작은 대체 수단이 아니다.
4. 큰 단계(감독 시작·사전 측정 끝·차례 시작·차례 끝·다시 시도·조사·재심), 오류(모델 확인 실패 포함), 조용함 경고, 최종 판정 줄만 stdout의 1부터 시작하는 줄 번호로 매핑한다. 일반 활동 요약과 사전 측정 n/m 중간 줄은 매핑하거나 채팅에 옮기지 않는다. 원본 대화 전체에서 이런 중간 줄 때문에 부모가 반복해서 깨어나거나 채팅을 남기지 않았는지도 직접 확인한다. 활동 요약은 기본 60초마다 명령 수와 지금 하는 일을 보여 주며 명령별 시작·끝 줄이 없어야 한다. 채팅 요약은 같은 종류·회차·조건·결과를 전달해야 하며 단순 “진행 중”은 인정하지 않는다. 출력과 채팅 시각은 같은 기준의 epoch 초로 기록한다.
5. 증거 파일은 `.harness/.meta/codex-audit-progress/evidence/`에 두고 아래 모양의 ui-review.json을 쓴다. 실제 값만 기록한다. 이 문서에는 PASS 증거 파일을 제공하지 않는다. 경로는 evidence 폴더 상대 경로이며 sha256은 해당 파일의 실제 전체 해시다. reviewer는 독립 검토자, implementer는 구현자 식별자다.

```json
{
  "cases": [
    {
      "verb": "draft|revise|impl",
      "route": "direct|delegated",
      "reviewer": "실제 검토자",
      "implementer": "실제 구현자",
      "parent_session": "실제 부모 ID",
      "follow_actor": "실제 도구 호출 주체 ID",
      "run_in_background": true,
      "user_requested_progress": false,
      "follow_started": 0,
      "first_phase_at": 0,
      "finished_at": 0,
      "transcript": {"path": "실제 대화 경로", "sha256": "실제 해시"},
      "stdout": {"path": "실제 stdout 경로", "sha256": "실제 해시"},
      "capture": {"path": "실제 화면 기록 경로", "sha256": "실제 해시"},
      "phases": [
        {
          "stdout_location": 1,
          "stdout_line": "실제 단계 출력 한 줄",
          "stdout_at": 0,
          "chat_line": "실제 부모 채팅 한 줄",
          "chat_at": 0,
          "transcript_location": 1,
          "capture_location": "해당 화면/프레임/영역 위치"
        }
      ],
      "card_visible_during_run": true,
      "review_verdict": "PASS|FAIL"
    }
  ]
}
```

위 JSON은 필드 설명이며 증거가 아니다. 전체 여섯 사례의 실제 값을 채운 뒤 `m 스킬-02`를 실행한다. 자동 검사는 해시·실제 텍스트 줄·사례 집합·전달 대상 누락·불필요한 전달 참조·시간·부모 ID를 검사한다. 화면 내용, 원본 대화의 진위, 증거의 실행 커밋, 요약의 의미는 독립 검토자의 직접 대조가 판정 권위다. 검토가 없거나 하나라도 실패하면 스킬-02는 FAIL이다. 음성 대조는 `m 스킬-02 --negative`로 마지막 사례의 배경 실행을 무력화하며 원본 증거는 고치지 않는다.
