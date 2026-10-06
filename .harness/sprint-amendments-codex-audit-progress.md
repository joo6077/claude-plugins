# Sprint Amendments — codex-audit-progress / 개정 1

봉인 기준은 원 계약 `.harness/sprint-contract-codex-audit-progress.md`의 `conditions_digest: sha256:74c37f0b7c63a737`, `measurement_digest: sha256:6778115c6d83ef37`, `locked_at: "2026-10-06 15:46"`이다. 본문·24개 조건·봉인 필드는 수정하지 않는다. 아래는 스킬-02 하나를 읽는 방법과 측정만 바꾸며 구현하지 않는다.

## AM-01 — relaxing

- 대상 조건: 스킬-02의 실행 장소·증거 형태 및 그 측정. 다른 조건에는 적용하지 않는다.
- 변경: VS Code 확장과 작업 카드 화면 캡처 요구를 새 명령줄 부모 Claude 세션의 stream·부모/자식 대화 기록·부모 Bash follow 작업 출력 및 당시 관측으로 대체한다. 카드 갱신은 부모의 follow 백그라운드 출력이 감독 중 자란 것으로 읽는다. 6사례·자동 시작·부모 주체·비차단 감독·15초 전달·요약 비전달·독립 검토는 유지한다.
- 근거 (redaction 거친 원문): 사용자가 고른 답 「제가 명령줄로 돌리기 (추천)」. 질문은 「스킬-02 실사용 확인을 어떻게 끝낼까요?」. 선택지 설명 원문은 「제가 새 Claude 대화를 명령줄로 띄워 6건을 전부 돌리고 증거까지 모읍니다. 사용자는 아무것도 안 하셔도 됩니다. 단 계약의 「VS Code 카드 화면 캡처」 요구를 「대화 기록의 도구 호출·시각 증거」로 바꾸는 개정이 필요하고, 이건 조건을 느슨하게 하는 개정이라 여기서 동의를 받습니다.」이다. 요구사항 `amendment-1-requirements.md` §1~5를 구체화한다. 요구사항에 기록된 1차 실사용 실패는 이번 증거의 자동 PASS 사유가 아니다.
- 앵커: `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/fb4aefa8-0ee1-4711-9b22-7baf9c6b989f.jsonl`의 3199행 AskUserQuestion과 3200행 응답을 직접 JSON 파싱하여 `toolu_01MkhpwQUHdEWDRkPg1so2Du`로 짝지었다. 호출 시각 `2026-10-06T08:41:12.991Z`, 호출 UUID `c0256429-5d5e-4d93-bbcd-353df4a3defd`; **동의 시각** `2026-10-06T08:41:34.255Z`, 응답 UUID `c7d2591f-afdb-4a7a-8a73-17bd1abab2f6`; session=`fb4aefa8-0ee1-4711-9b22-7baf9c6b989f`, cwd=`/Users/jackson/Hub/10_Dev/claude-plugins`. cwd는 실제 응답 레코드 값이며 작업트리 경로로 바꾸지 않는다.
- consent: anchored — 스키마가 허용하는 세션 기록의 AskUserQuestion 호출·선택 응답 쌍이다. 구현 검토자의 판정과 사용자 동의는 별개다. 이번 작업은 커밋하지 않으므로 개정 커밋과 동의의 선후 대조는 그 커밋을 만들 때 확인한다.
- direction 계산: 측정 요구 원자 집합을 사용한 `amend_direction_oracle` 규칙이다. 공통 집합 C={six_cases,same_parent,automatic_parent_follow,follow_before_phase,nonblocking_supervisor,relay_15s,no_summary_relay,independent_review,evidence_hashes}. 원 측정 집합 C∪{vscode_extension,visible_card_capture}, 개정 측정 집합 C∪{cli_session_records,background_output_growth}. 차집합은 removed={vscode_extension,visible_card_capture}, added={cli_session_records,background_output_growth}; 따라서 `relaxing measured_removed=2 measured_added=2`. 허용 집합 헬퍼에 측정 집합을 넣어 극성을 뒤집지 않는다. 실행 환경·화면을 입증하지 못해 원 조건에서 FAIL이던 구현도 명령줄 증거로 PASS할 수 있으므로, 새 증거 검사가 자세해졌더라도 완화다.

문서 정합성 갱신: `git log c78b4f09..HEAD -- harness/`와 `f5162bcf`까지의 sprint-contract·qa-evaluator 문서를 대조했다. 직접 감독의 짧은 `--detach` 호출과 Monitor의 `follow <계약> --relay` 묶음 전달을 반영한다. 종전 개정의 직접 Bash `run_in_background:true`만 허용하던 문구보다 인정 형태는 늘지만, 감독 완료까지 부모를 붙잡지 않는다는 공통 원자 `nonblocking_supervisor`의 같은 의미를 구현한 절차만 인정한다. `--detach` 없는 앞에서 기다리는 호출은 짧아도 FAIL이며, `--detach`가 있어도 30초 초과·오류·중단·감독 경로 미반환은 FAIL이다. 위 방향 계산의 원자 차집합과 `relaxing measured_removed=2 measured_added=2`, 동의 앵커는 그대로다. ` ‖ `로 묶인 Monitor 알림이나 하나의 채팅 text에 여러 사건이 있어도 각 원본 출력 줄을 따로 매핑하고 각 사건의 출력 시각부터 15초를 센다.

- [ ] 스킬-02: Given 진행 표시를 요청하지 않은 새 명령줄 부모 Claude 세션, When draft·revise·impl × direct·delegated의 여섯 감독 사례를 같은 부모 세션에서 수행하면, Then (1) 여섯 조합이 모두 같은 부모 세션에 있고, (2) 각 사례에서 부모가 첫 단계 전에 Bash run_in_background:true로 codex-audit.sh follow를 시작하며 자식 실행으로 대체하지 않고, (3) 직접 감독은 부모 Bash run_in_background:true와 실제 backgroundTaskId 반환, 또는 감독 호출 자체의 --detach 인자와 30초 이내 오류·중단 없는 감독 폴더 경로 반환으로 부모를 막지 않으며, 평가자 경유 감독은 부모 Agent run_in_background:true와 실제 isAsync:true로 시작하며, (4) 감독 중 부모 follow 출력이 자라고 기존 relay_line 분류의 큰 단계·오류·조용함 경고·최종 판정 각 줄의 같은 종류·회차·조건·결과가 부모 assistant 채팅에 15초 안에 전달되며 활동 요약·사전 측정 중간 줄을 전달하거나 그 때문에 반복해서 깨우지 않고, (5) 구현자와 다른 새 독립 평가자가 원본을 직접 대조한 사례별 결과와 증거 전체 해시가 `.harness/.meta/codex-audit-progress/evidence/cli-review.json`에 있고 그 해시가 실제 파일과 일치한다 [goal]
  측정: `bash .harness/.meta/codex-audit-progress/measure/measure.sh 스킬-02`와 `measure/cli-review-amendment1.md`의 독립 검토를 모두 통과해야 PASS다. `amendment1.py`가 evidence를 직접 읽고 itertools.product로 cases_total=6을 산출한다. measure.sh는 이 조건만 새 측정으로 보내며 다른 인자는 기존 measure.py로 보낸다. 기존 measure.py·fake.py·ui-review.md는 불변이다. 새 측정은 판정 격리 밖 사전 측정으로 실행하여 stdout과 종료 코드를 판정 증거로 보존한다.
  음성 대조: 같은 명령 끝에 `--negative`; 마지막 사례 부모 follow 도구 호출을 깊은 복사한 뒤 run_in_background를 false로 바꿔 같은 검사에 넣는다. 원본은 불변이며 검토 파일 누락과 별개로 배경 실행 검사에서 FAIL해야 한다. 음성 대조의 정상 검출도 종료 1이다.

## 증거와 판정 경계

현재 6차 실사용 evidence/session.txt에서 직접 읽은 부모 ID는 `9f134ec7-d4b6-428e-bd04-9c78d30e8299`이다. 부모의 실제 첫 요청은 parent.jsonl:8, `2026-10-06T09:40:25.640Z`; 마지막 요청은 :399, `2026-10-06T09:46:27.220Z`다. 직접 감독 호출/반환은 :59/:60 (`09:40:40.739Z` → `09:40:41.011Z`, 0.272초), :126/:127 (`09:41:52.919Z` → `09:41:53.313Z`, 0.394초), :217/:218 (`09:43:07.720Z` → `09:43:07.964Z`, 0.244초)이며 모두 같은 UTC 날짜에 `--detach`로 감독 폴더 경로를 반환했다. 실행기 사본은 읽기만 하고 실행하지 않는다. 새 측정이 해시를 산출하는 것만으로 원본 진위나 실행 커밋을 확증하지 않는다.

자동 검사는 실제 요청 목록·진행 요청 어휘, 부모 세션·sidechain, stream과 부모 호출/채팅 일치, 호출과 backgroundTaskId 연결 또는 직접 감독의 --detach·30초 이내 감독 경로 반환, 비차단 인자, 위임 결과와 자식의 실제 감독 종류, 첫 단계 전 follow 확인, stdout 줄 분류, 15초 이내 부모 텍스트 존재, 요약 원문·패턴 비전달, 검토 매핑의 원본 위치·텍스트·시각·해시를 검사한다. 검토 파일이 없어도 이 검사를 끝까지 실행해 결함을 보고한다. 의미가 같은 한국어 바꿔쓰기·회차/결과 전달·요약을 바꿔 말한 전달·반복 깨움·실제 작업 출력 성장(`growth.jsonl`의 부모 세션·작업 파일별 크기 관측 포함)·실행 커밋·증거 진위·검토 독립성은 독립 검토자가 원문을 대조할 판정 영역이다. 임의 텍스트 후보만으로 이 영역을 PASS하지 않는다.

검토 결과 파일의 필수 필드와 매핑 형식은 새 `measure/cli-review-amendment1.md`에 정한다. 검토자는 여섯 사례별 verdict와 근거를 작성한다. 이 개정 작성자는 결과 파일 자체를 만들지 않는다. 기존 ui-review.json 또는 화면 검토 절차를 새 결과로 자동 변환하지 않는다.
