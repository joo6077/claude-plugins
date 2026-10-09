# Sprint Amendments — codex-supervisor / 개정 1

봉인 기준: 커밋 `850cf4c9`, 본문 `conditions_digest: sha256:2467113bd3f57fd7`. 원본 조건 27개와 그 본문·봉인 필드는 수정하지 않는다. 이 파일은 `.harness/sprint-amendments-codex-supervisor.md`로 옮길 사이드카다. 작성자는 계약과 측정만 작성하며 구현하지 않는다.

## 배경과 근거

요구사항 §6의 8개 요구를 AM-01~08의 스크립트-12~19로 덮는다. 첫 감독 보고서 impl-r1/report.md의 REJECT 이유는 스크립트-11의 중첩 격리 시작 실패, 오류-02·구조-04의 ps 관측 불가다. 이것을 기존 구현의 자동 PASS 근거로 쓰지 않는다. 확인 못 함: 요구사항에 적힌 세 조건의 격리 밖 PASS는 이번 작업에서 실제 서비스 호출로 재측정하지 않았다. 새 조건 시험은 전부 무효 키 표본과 가짜 CODEX_BIN을 사용한다.

이번 개정은 단순한 조건 추가만이 아니다. AM-09는 기존 조건을 만족했다고 인정할 증거 출처를 넓히므로 별도의 relaxing 항목이다. 새 제약 강화와 상계해서 전체가 narrowing이라고 부르지 않는다. 원래 기능 기대값·종료 코드·측정 함수는 유지하며, 사전 기록만 있다고 자동 PASS하지 않는다.

사용자 동의 원문은 「1」이다. 세션 JSONL을 직접 파싱하여 user 레코드 UUID `5bbabb26-1974-49aa-9626-c556240db6a8`, 1405행, 답변 시각 `2026-10-06T04:23:30.477Z`를 확인했다. 앞 assistant의 선택지 1은 「격리 밖 사전 측정 기능을 추가하고 다시 감독받기」다(2026-10-06T04:22:31.668Z, UUID eb132726-c2f7-43ea-8138-6e0f28d29bd8). 구조적 동의 레코드가 기준이며 설명문만으로 동의를 추정하지 않았다.

세션 출처: `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/fb4aefa8-0ee1-4711-9b22-7baf9c6b989f.jsonl`. 규약이 타이핑 동의에 요구하는 reflect-kit prompt 로그도 `/Users/jackson/.claude/logs/claude-plugins/2026-10.md:1182`에서 직접 확인했다: `2026-10-06T13:23:30+0900`, 같은 session·cwd, 본문 「1」(1187행). 두 시각은 UTC/KST 변환 시 같은 초다. 따라서 모든 항목의 consent는 anchored다. 아직 개정 커밋을 만들지 않았으므로 개정 커밋보다 동의가 앞서는지의 최종 대조는 커밋 후 필요하다. 기존 봉인 승인 「ㄱㄱ」를 이번 개정 동의로 대신하지 않는다.

## 관측 경계와 실행

`m <조건> [옵션]`은 W에서 `bash .harness/.meta/codex-supervisor/measure/measure.sh <조건> [옵션]`이다. 현재는 `bash out/measure/measure.sh <조건> [옵션]`로 실행한다. 기존 조건은 기존 measure.py로 그대로 보낸다. 새 조건만 amendment.py로 보낸다. 커밋 상한은 기존처럼 `git rev-parse --verify -q feat/codex-supervisor`, 기준은 `88b2a84e`이며 HEAD 대체는 없다.

요구사항이 기록 직렬화 형식을 정하지 않아 독립적으로 재기 위한 공개 파일 경계를 다음처럼 정한다. 기존에 존재하는 얼린 입력 MANIFEST.json에 premeasure 객체를 추가한다. records는 조건별 JSON 파일의 상대 경로 배열, summary는 요약 TSV 파일의 상대 경로다. 두 종류의 실제 파일 이름은 구현자가 고른다. 경로는 얼린 입력 폴더 안의 실재 파일이어야 한다. 조건별 기록은 id·command·exit_code·output·timed_out 필드를 갖는다. 조건 번호는 중복·누락이 없고 명령은 치환 완료 문자열, 종료 코드는 정수, 출력은 키를 가린 stdout·stderr, timed_out은 불리언이다. 요약 헤더는 `condition\texit_code\tlast_line`이며 각 기록 순서대로 조건·종료 코드·출력의 마지막 줄을 탭으로 나눈다. 마지막 줄의 탭은 공백으로 바꾸고 각 행은 줄바꿈으로 끝난다. 새 구현 파일명이나 내부 함수명은 정하지 않는다.

사전 측정 스크립트가 판정 Codex보다 먼저 실행되어 기록을 만드는지, 모든 판정 차례에서 읽는 바이트가 동일한지, 구현 커밋이 같은지는 가짜 Codex 앞의 관측 도우미가 확인한다. 허용된 쓰기는 out의 이 개정 파일과 out/measure 안뿐이다. W는 읽기만 한다. 이번 시험에서는 실제 Codex를 호출하지 않는다. 운영에서 이 계약의 모든 조건을 사전 측정하면 기존 스크립트-11의 실제 호출 3회 비용이 추가될 수 있으며, 사용자가 선택한 안의 비용이다.

## AM-01 — narrowing
- 대상 조건: 스크립트-12 (신규)
- 변경: §6 요구 1를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 1를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-12: Given 두 조건과 premeasure 명령 틀, When `m 스크립트-12`가 APPROVE·맹검 재심·조사 뒤 재판정과 재심을 각각 실행, Then 조건마다 사전 측정을 정확히 한 번 완료한 뒤 첫 판정 Codex를 부르고 모든 판정·재판정·재심은 같은 얼린 기록 바이트를 읽으며 감독 중 사전 측정을 다시 하지 않는다 [exact, enumerated]
  측정: `m 스크립트-12`; APPROVE 1차례, REJECT→REJECT 2차례, RESEARCH→조사 응답→REJECT→REJECT 4차례의 세 손 예제를 쓴다. 각 예제 조건은 2개라 사전 측정 호출 기대 2회다. fake가 각 판정 직전에 관측한 호출 목록과 MANIFEST가 가리키는 얼린 파일 해시를 비교한다. 조사 자체에는 구현 최종 판정을 맡기지 않는다.
  양성 대조: `m 스크립트-12 --controls-only`; 조건 둘의 호출 로그에 첫 번호를 한 번 더 넣으면 once 검사 위반 1. 알려진 답은 서로 다른 조건 기록 2개→2. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-12 --negative`; 격리된 구현 사본만 무력화한다. 실행 명령을 exit 0으로 바꿔 필수 실행·기록이 없으면 FAIL임을 확인한다.

기존 파일 변경 고지: `out/measure/measure.sh`만 새 조건 번호 분기를 위해 바꾼다. 전 SHA256 앞 16자리 `f93d4ca766677c04`, 후 `4a004a4122d20303`. 기존 번호의 `exec python3 "$measure_dir/measure.py" "$@"`와 기존 측정 함수·픽스처는 바꾸지 않았다. 나머지는 신규 amendment.py·amendment_probe.py·fake_amendment.py와 방향·검증 도구의 추가다. 전체 기존 파일 해시 비교는 verification/amendment-1/before-hashes.json과 최종 검증에 남긴다.

## AM-02 — narrowing
- 대상 조건: 스크립트-13 (신규)
- 변경: §6 요구 2를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 2를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-13: Given premeasure 미설정·빈 문자열·{id}를 포함한 명령 틀 세 설정, When `m 스크립트-13`, Then 앞 두 설정은 사전 측정 호출·산출물 0건으로 기존 판정을 유지하고 명령 틀 설정은 각 조건 번호를 치환한 명령을 실행하여 그 명령 문자열과 기록을 남긴다 [exact, enumerated]
  측정: `m 스크립트-13`; 설정 세 값×손 예제 조건 2개를 사용한다. 미설정·빈 문자열은 fake Codex APPROVE 1회와 사전 호출 0회, 설정됨은 조건별 호출 2회와 기록 command의 {id} 치환 결과를 확인한다. 이 스프린트에서는 빈 문자열도 끔으로 해석한다.
  양성 대조: `m 스크립트-13 --controls-only`; 같은 조건 번호를 중복 실행한 호출 목록을 같은 once 검사에 넣어 위반 1. 알려진 답은 두 조건 기록→2. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-13 --negative`; 격리된 구현 사본만 무력화한다. 실행 명령을 exit 0으로 바꿔 필수 실행·기록이 없으면 FAIL임을 확인한다.

## AM-03 — narrowing
- 대상 조건: 스크립트-14 (신규)
- 변경: §6 요구 3를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 3를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-14: Given 첫 조건은 자식 프로세스를 띄우고 멈추며 둘째 조건은 정상 종료하는 명령과 CODEX_AUDIT_LIMIT=1, When `m 스크립트-14`, Then 판정 Codex 호출 전 구현 커밋 사본에서 사전 측정하고 사본의 .git은 원본과 다르며 원본 파일·.git 변화 0, 첫 조건의 시간 초과·비정상 종료를 기록하고 자식의 주기적 파일 쓰기가 멎은 뒤 둘째 조건도 한 번 실행한다 [exact, enumerated]
  측정: `m 스크립트-14`; probe가 cwd·커밋·.git 경로·판정 프로세스 내부 여부를 기록하고 사본 파일에 쓴다. 첫 probe의 자식은 0.05초마다 heartbeat 파일을 갱신한다. 첫·둘째 probe 시작 간격은 1초 상한+스케줄링 허용 오차 2초 미만이어야 한다. 사전 측정 종료 뒤 0.35초 동안 갱신이 없어야 하며, 둘째 조건 종료는 0이어야 한다. 측정은 마지막에 자신이 만든 자식 PID만 정리한다. 이 대조는 판정 Codex 밖이라는 실행 순서·프로세스 경계를 재며 macOS 격리의 실효성을 별도 실증한다고 주장하지 않는다.
  양성 대조: `m 스크립트-14 --controls-only`; 둘째 조건이 빠진 trace를 같은 once 검사에 넣어 위반 1. 알려진 답은 두 조건 기록→2. 같은 --controls-only에서 heartbeat 대조로 살아 있는 자식의 갱신 검출 기대 1·실제 1, 종료 뒤 갱신 기대 0·실제 0도 확인한다. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-14 --negative`; 격리된 구현 사본만 무력화한다. 실행 명령을 exit 0으로 바꿔 필수 실행·기록이 없으면 FAIL임을 확인한다.

## AM-04 — narrowing
- 대상 조건: 스크립트-15 (신규)
- 변경: §6 요구 4를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 4를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-15: Given stdout·stderr에 알려진 키 표본과 조건별 시작·끝 줄을 출력하는 사전 명령, When `m 스크립트-15`, Then 감독 스크립트가 조건별 명령·실제 종료 코드·키를 가린 출력을 얼린 입력에 남기고 조건·종료 코드·마지막 줄 요약 한 장과 모든 기록 위치를 MANIFEST.json에 넣으며 감독 산출물의 키 원문은 0건이다 [exact, enumerated]
  측정: `m 스크립트-15`; fake Codex는 기록을 만들지 않는다. probe 실행 로그와 생산된 JSON 기록·TSV 요약을 대조한다. command는 치환된 실제 명령, exit_code는 정수, output은 stdout·stderr를 포함한 문자열, timed_out은 불리언이다. 출력의 비밀 아닌 BEGIN·END·stderr 표식은 유지되어야 한다. 아래 직렬화 경계가 검사 형식이다.
  양성 대조: `m 스크립트-15 --controls-only`; 정상 손 예제 기록 파일 하나를 지워 같은 read_bundle 검사에서 위반 1. 알려진 답은 정상 기록 2개→2. 같은 --controls-only에서 파일 누락·종료 타입·중복 번호·요약 불일치·키 원문·폴더 밖 경로·절대 경로 일곱 변이도 검사하여 검출 기대 7·실제 7이어야 한다. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-15 --negative`; 격리된 구현 사본만 무력화한다. 실행 명령을 exit 0으로 바꿔 필수 실행·기록이 없으면 FAIL임을 확인한다.

## AM-05 — narrowing
- 대상 조건: 스크립트-16 (신규)
- 변경: §6 요구 5를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 5를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-16: Given 유효한 사전 측정 기록, When `m 스크립트-16`, Then 실제 판정 지시문은 감독 스크립트가 판정 전에 격리 밖에서 작성한 기록임을 밝히고 격리 안에서 실행할 수 없는 프로세스 관측·겹친 격리·실제 서비스 측정에 한해 증거로 쓸 수 있다고 안내하며 가능한 측정은 직접 실행하도록 지시하고 기존 역할 말·8192바이트·예시 수 제한을 지킨다 [exact, enumerated]
  측정: `m 스크립트-16`; 전달된 실제 지시문과 MANIFEST 경로를 검사하고, 기존 prompt_checks를 그대로 재사용하여 지시문 템플릿 합계와 전달문을 확인한다. 출처 문장의 사전 측정·격리 밖·판정 전·증거·격리 안·직접·프로세스·서비스와 실행 불가 제한 표현을 확인한다. 키워드만 있고 반대 지시가 남는지는 평가자가 원문으로 대조하며 반대 지시가 있으면 FAIL이다.
  양성 대조: `m 스크립트-16 --controls-only`; 짧고 중립적인 손 예제 지시문의 격리 밖 출처를 제거해 위반 1. 알려진 답은 읽힌 기록 2개→2. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-16 --negative`; 격리된 구현 사본만 무력화한다. 실행 명령을 exit 0으로 바꿔 필수 실행·기록이 없으면 FAIL임을 확인한다.

## AM-06 — narrowing
- 대상 조건: 스크립트-17 (신규)
- 변경: §6 요구 6를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 6를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-17: Given 사전 명령이 종료 7 또는 없는 명령으로 실패하고 판정 Codex는 유효 APPROVE 또는 같은 조건의 두 REJECT를 내는 경우, When `m 스크립트-17`, Then 사전 명령의 비정상 종료·오류 출력은 기록하되 그 실패만으로 BLOCKED하지 않고 Codex 판정에 따라 각각 종료 0·APPROVE 또는 종료 1·REJECT를 낸다 [exact, enumerated]
  측정: `m 스크립트-17`; 사전 명령 실패 2종×판정 2종의 cases_total=4. 각 손 예제의 조건은 2개다. 기록의 비정상 종료와 비어 있지 않은 오류 출력, fake Codex 호출 1회 또는 2회, 최종 보고서와 종료 코드를 재며 숫자 7을 실제 probe의 종료와 맞댄다. 시간 초과 후 진행·최종 APPROVE는 스크립트-14가 별도로 잰다.
  양성 대조: `m 스크립트-17 --controls-only`; 실패 기록 파일 누락을 같은 read_bundle 검사로 검출하여 위반 1. 알려진 답은 기록 2개→2. 사전 측정의 실패를 판정 실패와 혼동하는 no-op 사본은 음성 대조에서 FAIL이다. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-17 --negative`; 격리된 구현 사본만 무력화한다. 실행 명령을 exit 0으로 바꿔 필수 실행·기록이 없으면 FAIL임을 확인한다.

## AM-07 — narrowing
- 대상 조건: 스크립트-18 (신규)
- 변경: §6 요구 7를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 7를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-18: Given 저장소 설정·새 프로젝트 틀·배포 문서, When `m 스크립트-18`, Then .harness/project.yaml의 codex_audit.premeasure는 이 계약의 measure.sh {id} 명령이고 harness/templates/project.yaml에는 설명 주석과 빈 premeasure가 있으며 README·qa-evaluator·sprint-contract 문서 각각에 premeasure와 사전 측정 설명이 있다 [exact, enumerated]
  측정: `m 스크립트-18`; 저장소 설정은 W의 현재 .harness/project.yaml에서 읽고 나머지는 feat/codex-supervisor 커밋에서 읽는다. 정확한 활성 명령은 bash .harness/.meta/codex-supervisor/measure/measure.sh {id}다. 틀의 주석은 {id} 치환 설명을 포함한다. 문서는 실제 존재하는 harness/README.md, harness/agents/qa-evaluator.md, harness/skills/sprint-contract/SKILL.md다.
  양성 대조: `m 스크립트-18 --controls-only`; 문서 표본에서 premeasure를 제거하여 같은 문서 검사기로 누락 1을 검출한다. 알려진 답은 손 예제 기록 2개→2. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-18 --negative`; 격리된 구현 사본만 무력화한다. 새 프로젝트 틀의 premeasure 칸을 제거하여 FAIL이다.

## AM-08 — narrowing
- 대상 조건: 스크립트-19 (신규)
- 변경: §6 요구 8를 아래 독립 조건으로 추가한다.
- 근거 (redaction 거친 원문): "1" — 사전 측정 기능 추가 후 다시 감독 선택. 요구사항 §6 요구 8를 구체화했다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 위 세션 user 레코드와 prompt 로그에서 직접 확인.
- direction 계산: amend_direction_oracle에 기존 27개 측정 집합과 거기에 이 조건 한 개를 추가한 28개 집합을 넣으면 `narrowing measured_removed=0 measured_added=1`. 입력은 허용 집합이 아닌 추가되는 측정 집합이다.

- [ ] 스크립트-19: Given 조건 하나를 추가한 sprint-amendments-sample.md가 있는 계약과 없는 계약, When `m 스크립트-19`, Then 존재하는 개정 파일은 원문 바이트 그대로 얼린 입력에 한 번 포함되고 판정·재심이 그 파일을 읽도록 지시받으며 추가 조건도 사전 측정·조건별 판정에 포함되고 원본 개정 파일은 불변이며 파일이 없으면 기존 계약만으로 진행한다 [exact, enumerated]
  측정: `m 스크립트-19`; 원 계약 조건 2개+개정 조건 스크립트-03 하나인 손 예제다. fake Codex가 세 조건의 답을 내므로 기존 두 번호만 허용하는 구현은 통과하지 못한다. 파일명은 원본 규약명만 고정하며 얼린 사본 이름은 자유다. 실제 전달문에 사본 경로나 사본을 열거하는 MANIFEST 경로와 개정을 읽으라는 지시가 있어야 한다. sidecar 없는 손 예제도 같은 기록 검사를 통과해야 한다.
  양성 대조: `m 스크립트-19 --controls-only`; 얼린 기록 파일 누락을 같은 read_bundle로 검출하여 위반 1. 알려진 답은 기본 손 예제 기록 2개→2. 개정 손 예제의 유효 번호 집합은 3개이며 일반 실행에서 각각 한 번인지 확인한다. 모든 대조의 positive_control 기대 1·known_answer 기대 2이며 실제 모델 호출 0이다.
  음성 대조: `m 스크립트-19 --negative`; 격리된 구현 사본만 무력화한다. 실행 명령을 exit 0으로 바꿔 필수 실행·기록이 없으면 FAIL임을 확인한다.

## AM-09 — relaxing
- 대상 조건: 봉인 본문의 기존 27개 조건 전체에 대한 증거 출처 규칙. 현재 격리 제약이 확인된 대상은 스크립트-11·오류-02·구조-04이며, 다른 조건도 해당 제약을 증명한 경우에만 아래 예외가 적용된다.
- 변경: 격리 안 직접 실행 증거를 계속 허용하면서, 격리 안에서 실행할 수 없는 측정은 감독 스크립트가 같은 구현 커밋을 대상으로 판정 전에 격리 밖에서 생성·동결한 사전 측정 기록도 증거로 허용한다. 가능한 측정은 직접 실행한다. 실패·시간 초과·누락 기록을 PASS로 바꾸지 않으며, 기존 조건의 기대 동작·종료 코드·실제 서비스 검증 요구·측정 코드는 완화하지 않는다. 특히 스크립트-11은 실제 Codex 실행 결과가 있어야 하고 가짜·준비 단계 PASS만으로는 성립하지 않는다. 출처·조건 번호·실행 명령·기준 커밋·산출물 연결을 확인할 수 없으면 이 예외의 PASS 근거가 아니다.
- 근거 (redaction 거친 원문): "1" — 사용자가 이번만 판단 통과나 격리 확대 대신 사전 측정 기능 추가를 선택했다. 요구사항 §6 요구 5와 첫 감독의 증거 부족을 해결하기 위해 증거 출처 자체를 넓힌다.
- 앵커: 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor
- consent: anchored — 세션 user 레코드와 reflect-kit prompt 로그의 같은 응답. reviewer 승인을 사용자 동의의 추가 요건으로 만들지 않는다.
- direction 계산: 허용 출처의 원자 집합을 조건 번호×증거 출처로 정의한다. 원 집합은 기존 27개 번호 각각의 direct 27개, 개정 집합은 여기에 각 번호의 premeasure_if_sandbox_unavailable 27개를 더한 54개다. `amend_direction allowed-before.txt allowed-after.txt` 결과는 `relaxing added=27 removed=0`. 실제 실행 가능 여부의 제약은 토큰 이름에 포함된 필요조건이며 무조건적인 사전 기록 대체를 허용하는 집합이 아니다. 격리 안에서 증거 부족으로 FAIL이던 같은 구현이 유효 사전 기록으로 PASS할 수 있으므로 완화가 맞다.

검증: `bash out/measure/amendment-direction.sh allowed out/measure/verification/amendment-1/allowed-before.txt out/measure/verification/amendment-1/allowed-after.txt`. 양성 대조는 원·개정 허용 집합의 방향을 뒤집어 narrowing이 되는지와 파일 결측이 unknown인지 확인한다. AM-01~08의 기존 27개→개정 적용 35개 측정 집합의 비교는 별도로 `narrowing measured_removed=0 measured_added=8`이다. 이 결과를 AM-09와 합쳐 narrowing이라고 보고하지 않는다.

## 범위 경계와 남는 확인

§6 대응: 요구 1→스크립트-12, 2→13, 3→14, 4→15, 5→16·AM-09, 6→17, 7→18, 8→19. 요구 8개 중 제외한 것은 없다. 조건 번호는 본문의 스크립트-11 다음 12~19이며 중복이 없다. 봉인 본문 conditions=27은 유지하고 개정 적용 시 전체 35개·기능 27개다. 기능 상한 20을 넘는 이유는 기존 기능 19개를 봉인 그대로 유지하면서 새 요구 8개를 각각 독립 판정하기 위해서다. 개수를 맞추려고 기존 조건이나 새 요구를 제외하지 않았다.

기존 구현 범위 블록은 그대로다. 추가 설정 경로 .harness/project.yaml과 사이드카는 규약의 .harness 자동 허용 범위다. 새 기능의 구현 변경은 요구사항에 이미 있는 codex-audit.sh·codex-audit 템플릿과 기존 문서에 한한다. 새 측정 코드는 out/measure에만 추가한다. 봉인 계약 본문과 out의 이전 계약 초안은 수정하지 않는다.

확인 못 함: 실제 모델이 새 출처 지시를 따르는지와 OS 격리의 실효성은 가짜 시험만으로 증명하지 못한다. 실제 모델 호출 0회, 로그·키는 무효 표본이다. 기존 계약의 SIGKILL·전원 단절 한계도 그대로다. 첫 보고서의 기존 FAIL을 이 사이드카 작성만으로 APPROVE로 뒤집지 않는다. 구현자가 기능을 구현한 뒤 원래 감독 절차로 다시 판정해야 한다.
