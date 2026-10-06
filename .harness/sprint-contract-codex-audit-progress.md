---
feature: "Codex 감독 진행 상황 표시와 새 모델·Codex 판 보고"
created: "2026-10-06 15:03"
complexity: complex
conditions: 24
slug: codex-audit-progress
status: active
owner_session: fb4aefa8-0ee1-4711-9b22-7baf9c6b989f
conditions_digest: sha256:74c37f0b7c63a737
measurement_digest: sha256:6778115c6d83ef37
locked_at: "2026-10-06 15:46"
---
# Sprint Contract — codex-audit-progress

## 배경

정본은 W의 `.harness/.meta/codex-audit-progress/requirements.md`이며, 진행 출력·채팅 전달 범위와 조회 실패 측정은 `critique-1.md`의 이번 지적을 우선 적용한다. W는 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-audit-progress`, BASE는 `c78b4f09`, 상한 U는 `git rev-parse --verify -q feat/codex-audit-progress`다. 상한을 못 읽으면 FAIL이며 HEAD로 대체하지 않는다. 측정은 U의 커밋을 임시 폴더에 풀어 실행한다. 원본 저장소와 실제 사용자 설정·인증에는 쓰지 않는다. 사용자 지시대로 계약과 측정만 작성하며 선점·봉인·커밋·구현·실제 감독 재호출은 수행하지 않는다. created 원본은 `2026-10-06T15:03:31+0900`의 date 출력이다.

복잡도 네 축은 CLI·실행 상태·대화 표시의 여러 계층, follow/models 공개 명령 추가, 부모 세션과 평가자의 소비면, wait/재시도/인증/조회 실패의 회귀 위험이다. 기능 조건 16개와 금지 패턴 2개·자동 포함 6개로 총 24개다.

설정 리터럴: 카테고리는 Skill/스킬·Script/스크립트·Error/오류·Architecture/구조다. commands.analyze는 `bash -n scripts/release.sh`, commands.test는 `bash scripts/release.sh 2>&1 || true`, lint/format/codegen은 null, diagnostics.ide_exclude는 []다. 금지-03·04는 아래에 설정 원문을 적용한다.

사전 열람: codex-audit.sh의 main/wait/run_codex/premeasure, sprint-contract의 Codex 작성 모드, qa-evaluator의 Codex 판정 모드, 계약 스키마의 허용 헤더·측정 관례, 이전 codex-supervisor 계약과 측정 예제를 읽었다. 현재 명령은 draft/revise/impl/wait뿐이며 진행 중 세션 기록은 임시 Codex 폴더에 있다. 기존 project.yaml의 premeasure는 이전 codex-supervisor 측정을 가리킨다.

제안 설계를 채택하며 다음 공개 시험 경계를 구체화한다. 내부 진행 기록의 파일명·필드·함수 이름은 정하지 않는다.

- `follow <감독 폴더|계약 파일> [--idle-seconds N] [--wait-seconds N] [--summary-seconds N]`: idle·summary는 양의 정수이며 각각 기본 60초, wait는 음이 아닌 정수이며 기본 540초다. wait는 아직 추적할 새 감독이 없는 경우의 대기 상한이다. 만료는 이유와 BLOCKED·종료 2, 인자 오류는 설명·종료 64다. 실행 중 감독을 이 상한 때문에 종료하지 않는다. 큰 단계(감독 시작·사전 측정 끝·차례 시작·차례 끝·다시 시도·조사·재심·최종 판정)와 오류는 발생 후 5초 안에 stdout에 flush한다. 조용함 경고도 idle 만료 뒤 5초 안에 표시한다. 일반 Codex 활동은 summary 간격이 찰 때 한 줄 `활동 요약 · 명령 N개 · 지금 <자료 읽기|측정 시험|파일 쓰기|생각 중|답 작성>`으로 flush하며, N은 이전 요약 뒤 시작한 고유 명령 수다. 명령 실행 중에는 그 분류와 경과 초를 같은 요약 줄에 더할 수 있다. 명령별 시작·끝, 단순 상태 전환, 답 받음만을 위한 별도 줄은 내지 않는다. 마지막 미완 간격은 차례 끝에 합칠 수 있으며 별도 요약 줄을 추가하지 않는다. 사전 측정 n/m 중간 결과도 같은 간격의 한 줄로 묶되 조건 ID·종료 코드·경과 초를 보존하고 측정 끝에 잔여 결과와 총 시간을 표시한다. 오류·조용함·큰 단계는 요약 시각까지 미루지 않는다. 기본 무출력 경고는 60±2초로 관찰한다. --summary-seconds는 요약 간격의 공개 설정이며 --idle-seconds의 의미는 바꾸지 않는다.
- 채팅 전달은 큰 단계·오류(모델 확인 실패 포함)·조용함 경고·최종 판정에 한정한다. 일반 활동 요약과 사전 측정 n/m 중간 줄은 백그라운드 작업 카드에만 표시하며 줄마다 부모를 깨워 채팅에 옮기지 않는다. 이번 지적의 로그·토큰 절감 요청에 따라 기존 사건별 표시 제안을 이 정책으로 바꾼다.
- `models`는 cwd 프로젝트에 설정된 감독 계정·모델을 사용한다. `CODEX_AUDIT_MODELS_URL`은 모델 목록 HTTP 조회 주소의 시험용 대체값, `CODEX_AUDIT_CHECK_TIMEOUT`은 조회별 상한 초의 시험용 대체값이다. 미지정 때 실제 감독용 모델 목록과 `npm view @openai/codex version`을 조회한다. 테스트는 무효 키·로컬 HTTP 서버·가짜 npm만 사용한다. HTTP 라이브러리는 정하지 않는다. 이 주입점과 시간 옵션은 외부 서비스와 영구 사용자 기억을 오염시키지 않고 공개 명령을 재기 위한 설계 구체화다.
- 신규 알림은 지난 성공 관측 대비 추가된 GPT ID와 설치 판보다 새로우면서 아직 보고하지 않은 Codex 판이다. 순서 변경·삭제·동일 판·낮은 판은 새 소식이 아니다. 첫 성공 관측은 기억만 하고, 실패를 빈 목록의 성공으로 저장하지 않는다. 자동 확인의 새 소식은 follow의 맨 앞 알림 줄과 report.md 양쪽에 나타난다. 두 종류가 있으면 앞의 두 줄을 쓸 수 있다. models 단독 실행은 감독 폴더나 Codex exec를 만들지 않는다. 단독 조회의 성공은 종료 0, 조회 실패는 `모델 확인 못 함: 사유` 한 줄과 종료 2이며 미처리 예외·traceback을 내지 않는다.
- 빈 계약으로 시작하는 draft는 조건 수를 아직 알 수 없으므로 시작 줄에 미정/확인 중/알 수 없음을 쓸 수 있다. revise·impl은 실제 수를 표시한다. revise 회차 폴더가 기존처럼 draft-rN이어도 종류 revise를 구분하면 된다.
- 종료 코드 3 보존을 재기 위해 구형 report.md만 있는 종료 폴더도 읽는다. 공개 손 예제는 `시작: YYYY-MM-DD HH:MM:SS`, `끝: ...`, `단계: impl`, 마지막 `감독 판정: SKIPPED`다. 이런 구형 폴더에는 없는 중간 단계를 만들지 않고 총 시간과 최종 판정만 요구한다. 새 실제 감독에는 중간 단계 재생을 요구한다. mode: off가 새 감독 폴더를 만들어야 한다는 뜻은 아니다.

확인 못 함: 실제 VS Code 확장에서 부모 Bash 작업 카드가 갱신되고 단계가 채팅으로 전달되는 실행 증거는 아직 없다. 스킬-02의 독립 실사용 검토 전에는 문서 검사나 가짜 Codex 성공으로 이를 PASS 처리하지 않는다. 문서 지시의 의미·상충 여부도 평가자가 원문으로 대조한다.

확인 못 함: 실제 감독 계정의 현재 모델 목록·서버 응답·최신 npm 판·실제 Codex의 향후 사건 형식은 조회하지 않았다. gpt-fixture-* 및 1.2.3/1.3.0은 제품 사실이 아닌 손 예제다. 실제 서버 판정 품질은 이번 계약의 대상이 아니다.

확인 못 함: 현재 격리 환경에서는 로컬 HTTP bind를 시도했으나 PermissionError가 났다. 스크립트-07·08·오류-02는 격리 밖 premeasure가 필요하다. 구조-03이 이 묶음을 연결하며 평가자는 실제 사전 측정 출력·종료 코드를 읽는다. 사전 측정이나 UI 증거가 없으면 PASS가 아니다. shellcheck·IDE 서버는 확인하지 않았으므로 진단-02는 명시한 셸/Python 구문 범위만 보장한다.

## Skill

- [ ] 스킬-01: Given Codex 모드의 작성·수정·구현 감독, When 배포 지시를 읽으면, Then sprint-contract와 qa-evaluator 두 문서 모두 직접 호출·평가자 위임에 관계없이 부모 세션이 감독 시작과 함께 항상 `follow <계약 파일>`을 백그라운드로 실행하고 큰 단계·오류·조용함 경고·최종 판정만 채팅에 옮기며 일반 활동은 기본 60초 요약으로 작업 카드에만 표시하도록 명시하며 README 스크립트 표에서 follow와 models 사용법을 찾을 수 있다 [structural]
  측정: `m 스킬-01`; 두 문서의 follow 지시 문단에서 부모·항상·백그라운드·시작·계약·큰 단계·오류·조용함·최종 판정·채팅 범위 제한·60초 요약을 각각 검사하고 README 표 행을 검사한다. 평가자는 두 문서 전체에서 사용자 요청 때만 실행하거나 자식만 실행하거나 일반 활동·중간 측정 줄마다 채팅을 요구하는 상충 지시가 없는지도 확인한다. 문서 존재를 실제 UI 실행으로 인정하지 않는다.
  음성 대조: `m 스킬-01 --negative`는 사본의 두 문서에서 follow 지시를 제거하여 FAIL한다.
- [ ] 스킬-02: Given VS Code 확장의 부모 Claude 세션, When draft·revise·impl을 직접 또는 평가자 경유로 시작하면, Then 진행 표시 요청 없이 부모가 띄운 백그라운드 작업 카드가 감독 중 갱신되고 큰 단계·오류·조용함 경고·최종 판정만 15초 안에 채팅에도 전달되고 일반 활동 요약·사전 측정 중간 줄 때문에 부모가 반복해서 깨어나거나 채팅을 남기지 않는다; 증거는 `.harness/.meta/codex-audit-progress/evidence/ui-review.json`과 그 파일이 해시로 참조하는 원본 대화·follow stdout·화면 캡처다 [goal]
  측정: `m 스킬-02`와 `measure/ui-review.md`의 독립 검토를 모두 통과해야 PASS. 축 verb={draft,revise,impl} × route={direct,delegated}, cases_total은 itertools.product로 산출한다. 각 실행의 stdout의 채팅 전달 대상 줄 집합과 대화 참조 집합이 같고 부모 ID·배경 실행·시각·실제 카드 갱신을 독립 검토자가 확인한다. JSON 자기 진술만으로 PASS하지 않는다.
  음성 대조: 유효한 증거 사본의 마지막 사례에서 run_in_background를 false로 바꾸는 `m 스킬-02 --negative`는 FAIL. 원본 대화에 없는 채팅 줄이나 다른 실행을 가리키는 캡처도 독립 검토 FAIL이다.

## Script

- [ ] 스크립트-01: Given 새 감독과 두 조건(사전 측정 종료 0·7), When 세 종류 감독을 폴더·계약 경로로 따라가면, Then 감독 종료 전에 시각·종류·회차·조건 수·차례 이름·모델·생각 강도가 보이고 impl의 사전 측정 1/2·2/2는 간격 요약으로 묶어도 조건 ID·종료 코드·경과 초를 보존하고 마지막 측정에는 잔여 결과와 총 경과 시간, 차례 끝에는 결과와 impl의 PASS 2·FAIL 0이 보인다 [exact]
  측정: `m 스크립트-01`; verb 3개 × target 2개 전부 실행하며 cases_total을 곱으로 출력한다. --summary-seconds 2로 첫 측정 완료 뒤 둘째 측정을 멈춘 상태에서 1/2 요약이 5초 안에 도착해야 한다. 두 결과가 한 줄에 묶여도 각각 검사한다. Codex 응답도 gate로 멈춰 종료 전 차례 표시를 확인한다. 모든 follow 줄의 시각과 마지막 `감독 판정: APPROVE · 총 ...초`, 종료 0을 검사한다. draft 조건 수 예외는 배경을 따른다.
  음성 대조: `m 스크립트-01 --negative`는 실행 사본을 exit 0으로 바꿔 출력·진행·산출물 누락으로 FAIL한다.
- [ ] 스크립트-02: Given reasoning·command_execution·agent_message 사건, 명령 수십 개·중복 갱신·알 수 없는 사건·깨진 줄·나뉘어 도착한 JSON 줄, When 진행 중 follow를 읽으면, Then 큰 단계·오류는 5초 안에 표시하고 일반 활동은 기본 60초마다 직전 요약 이후의 고유 명령 수와 지금 하는 일(자료 읽기·측정 시험·파일 쓰기·생각 중·답 작성)을 한 줄로 요약하며 명령별 시작·끝이나 단순 상태 전환 줄을 내지 않고 추론 본문·파싱 예외를 노출하지 않는다 [exact]
  측정: `m 스크립트-02`; 실제 CODEX_BIN 사건 스트림에서 자료 읽기(cat)·측정 시험(python3 -m unittest)·파일 쓰기(리다이렉션) 각 40개와 생각 중·답 작성의 다섯 구간을 gate로 유지한다. --summary-seconds 2에서 완료 전에 해당 활동 요약과 고유 명령 수 합계 [40,40,40,0,0]을 검사한다. 중복 완료를 포함한 종료 7 오류는 5초 이내 정확히 한 번 표시한다. 별도 기본값 실행은 첫 명령의 종료 7 오류가 5초 안에 보이는지 확인하고 명령 40개 후 갱신 사건을 계속 보내 침묵 경고 없이 58초 전 요약 없음·65초 안 요약 한 줄을 실시간으로 검사한다. 무사전측정 impl의 큰 단계는 최대 5줄이며 전체 줄 수 ≤ 큰 단계 수 + 완료된 요약 간격 수 + 경고 수, 각 요약 간격·줄 분류도 검사한다. 새 모델 알림이 없는 시험이며 모델 확인 실패는 경고로 센다.
  음성 대조: `m 스크립트-02 --negative`는 follow에 명령 시작 40줄을 더한 사본을 같은 줄 수·분류 검사에서 FAIL시킨다. 요약 누락·중복 갱신을 새 명령으로 세기·오류를 다음 요약까지 보류하는 변이도 해당 내용·수·시각 검사에서 FAIL해야 한다.
- [ ] 스크립트-03: Given 사건이 조용하지만 감독은 실행 중인 차례, When 기본 60초 또는 지정 간격이 지나면, Then 무성장·다른 thread 기록만 성장한 경우 `Codex 조용함 N초 — 생각 중이거나 멈춤 의심`, 해당 thread의 진행 중 임시 기록이 성장한 경우 `생각 중(기록은 자람)`을 구분하고 간격마다 최대 한 번 알리며 침묵만으로 실패 판정을 내리지 않고 다음 사건부터 진행 표시를 계속한다 [exact]
  측정: `m 스크립트-03`; 무성장·해당 기록 성장·decoy 성장 세 경우를 idle 2초로 각각 두 번 관찰한다. 별도 기본값 실행에서 마지막 사건 후 58초 이전 경고 없음·65초 안 경고를 확인한다. 경고 사이 최소 1.5초, 성장 중 멈춤 의심 없음, 재개 뒤 APPROVE·0이 모두 필요하다. 기본값은 실제 시계로 잰다.
  음성 대조: `m 스크립트-03 --negative`는 FAIL. 해당 thread 대신 최신 파일을 고르는 변이는 decoy 사례에서 FAIL해야 한다.
- [ ] 스크립트-04: Given 종료한 실제 APPROVE·REJECT·BLOCKED 감독과 공개 구형 SKIPPED 폴더, When 같은 폴더를 두 번 따라가면, Then 새 감독의 지난 단계가 재생되고 시각을 제외한 결과가 같으며 마지막 감독 판정과 종료 코드가 각각 0·1·2·3이고 총 시간이 보이며 감독 산출물을 변경하지 않는다 [exact]
  측정: `m 스크립트-04`; 앞 세 결과는 실제 감독 실행으로 생성한다. SKIPPED의 공개 형식과 중간 단계 예외는 배경을 따른다. 실제 폴더는 전후 파일 해시도 비교한다.
  음성 대조: `m 스크립트-04 --negative`는 FAIL. 알려진 답: 네 판정의 기대 종료 배열은 [0,1,2,3]이다.
- [ ] 스크립트-05: Given 계약에 실행 중 감독이 있거나 없거나 완료 감독만 있는 상태, When 계약 파일로 follow하면, Then 가장 최근 실행 중 감독을 선택하거나 새 감독을 기다리고 선택 뒤 다른 계약 폴더로 옮겨가지 않으며 새 감독이 없을 때 지정 상한 안에 이유·BLOCKED·종료 2로 끝난다 [exact]
  측정: `m 스크립트-05`; 완료 r1 뒤 대기→새 r2 선택, r2 실행 중 추가 follower 합류, other 계약 r99 간섭 없음, 빈 계약 wait 2초를 실행한다. 종료 시간은 준비 오차 포함 1.5~6초다. 스크립트-01의 계약 선행 실행이 폴더 생성 전 시작도 잰다.
  음성 대조: `m 스크립트-05 --negative`는 FAIL. 완료 폴더를 즉시 재생해 종료하는 변이도 새 r2 선택 전에 FAIL해야 한다.
- [ ] 스크립트-06: Given 빈 응답 뒤 회복·시간 초과 뒤 회복·외부 조사 뒤 재판정·REJECT 뒤 재심, When follow를 함께 실행하면, Then 감독 종료 전에 다시 시도와 원인 또는 조사·재심 단계가 보이고 각 차례 결과와 최종 판정이 실제 호출 순서·횟수와 일치한다 [exact]
  측정: `m 스크립트-06`; 네 시나리오의 exec 기대 수는 2·2·3·2다. 마지막 응답을 막은 상태에서 단계를 확인한다. 회복/조사는 APPROVE·0, 일치하는 두 REJECT는 REJECT·1이다. 시간 초과 사례의 호출 상한은 8초로 두어 정상인 5초 이내 출력 지연을 회복 실패로 오판하지 않는다.
  음성 대조: `m 스크립트-06 --negative`는 FAIL. 기대 호출 수는 fake plan 길이로 계산하며 마지막 결과만 출력하는 사본도 FAIL해야 한다.
- [ ] 스크립트-07: Given 독립 감독 설정 폴더의 성공 조회 기억, When models를 새 프로세스로 연속 호출하면, Then 첫 관측은 알림 없이 기억하고 다음의 새 GPT ID·더 새 Codex 판만 현재 감독 모델·설치 판과 함께 알리며 재조회·순서 변경·삭제·낮은 판에는 새 알림이 없고 현재 모델·설치 판·최신 판을 보여 주며 감독은 시작하지 않는다 [exact]
  측정: `m 스크립트-07`; HTTP에서 감독용 무효 키의 Bearer 사용 여부만 boolean으로 기록한다. 모델 old→old/new/비GPT→재정렬→삭제, 판 1.2.3→1.3.0→동일→1.1.0을 순차 대조한다. npm 인자는 `view @openai/codex version`과 같아야 한다. 기억은 감독 폴더 밖 감독용 Codex 폴더에 존재하고 설정 모델은 유지되어야 한다.
  음성 대조: `m 스크립트-07 --negative`는 출력 누락으로 FAIL. 키 누출은 같은 실행의 전체 시험 폴더·stdout/stderr에서 검사한다. 격리 밖 premeasure 대상이다.
- [ ] 스크립트-08: Given 최초 기억 뒤 새 GPT 모델·Codex 판이 생긴 감독 계정, When draft·revise·impl을 시작하면, Then 별도 models 요청 없이 자동 확인하여 follow의 처음 알림 줄과 해당 report.md에 새 것·현재 감독 모델·설치 판을 보고하고 원래 감독 모델로 계속 실행한다 [exact]
  측정: `m 스크립트-08`; 세 종류를 독립 설정 폴더에서 실행한다. models로 최초 기억을 만든 뒤 조회 값을 바꾸고 Codex 응답 전 알림을 검사한다. 실제 exec 모델·설정 파일 바이트·HTTP 호출 수·보고서 알림·키 누출을 대조한다.
  음성 대조: `m 스크립트-08 --negative`는 FAIL. 신규 모델 선택 변이는 exec 모델/설정 불변 검사에서 FAIL한다. 격리 밖 premeasure 대상이다.
- [ ] 스크립트-09: Given 기존 호출자, When impl --detach·wait·mode off를 사용하면, Then detach는 감독 폴더 한 줄·0, 실행 중 wait 0은 RUNNING 경로·75, 종료 wait는 `감독 판정: APPROVE|REJECT|BLOCKED`와 0|1|2, mode off는 SKIPPED·3을 그대로 반환한다 [exact]
  측정: `m 스크립트-09`; 실제 배경 감독과 fake Codex로 실행한다. 조회나 진행 표시를 기존 wait stdout에 섞으면 FAIL이다.
  음성 대조: `m 스크립트-09 --negative`의 무출력 exit 0은 FAIL. 보존 조건이므로 구현 전에도 PASS할 수 있다.

## Error

- [ ] 오류-01: Given follow의 인자 없음·없는 경로·idle 0·idle 비수치·wait 음수·알 수 없는 옵션·summary 0·summary 비수치, When 각각 호출하면, Then 5초 안에 사용법/이유와 종료 64를 내며 traceback 없이 끝나고 유효한 종료 폴더는 정상적으로 읽는다 [exact]
  측정: `m 오류-01`; 유효 SKIPPED 입력의 3부터 검사하여 모든 입력에 사용법만 내는 미구현이 PASS하지 못하게 한다. 잘못된 입력 수는 배열 길이로 출력한다.
  음성 대조: `m 오류-01 --negative`는 유효/잘못된 입력 종료 코드 대조에서 FAIL한다.
- [ ] 오류-02: Given 모델 조회의 HTTP 401·깨진 JSON·시간 초과·인증 파일 없음 또는 npm 실패·명령 없음, When 감독을 시작하거나 models를 단독으로 부르면, Then 감독은 정상 응답을 받아 APPROVE까지 진행하고 follow와 report.md 각각 `모델 확인 못 함: 사유` 한 줄만 남기며 단독 models는 같은 사유 한 줄과 종료 2로 traceback 없이 끝나고 감독 폴더·Codex exec를 만들지 않으며 두 경로 모두 조회 상한을 지키고 반복 조회로 지연시키거나 성공 기억을 빈 실패 값으로 덮지 않는다 [exact]
  측정: `m 오류-02`; 실패 6종 × 호출 {models,draft,revise,impl}의 독립 조합 수를 곱으로 산출한다. 조회 상한 2초에서 서버를 5초 지연시킨 사례는 단독 models 종료 또는 감독의 첫 exec 시작까지 각각 4초 미만이어야 한다. 전체 감독/follow는 15초 미만, 감독 exec 1회·단독 exec 0회·모델 HTTP 추가 요청 최대 1회를 검사한다. 각 경로의 실패 출력에는 비어 있지 않은 사유가 정확히 한 줄 있어야 하며 traceback은 없어야 한다. 실패 후 같은 성공 값을 재조회해 새 알림이 없고 이어 새 모델/판으로 복구하면 알림을 받는 것과 키 누출 0을 확인한다. 인증 없음은 가짜 Codex 로그인·exec는 가능하되 모델 조회용 auth만 없는 경계 사례다.
  음성 대조: `m 오류-02 --negative`와 `m 오류-02 --mutation=models-exception`은 실패 주입 시 단독 models만 미처리 예외·종료 1로 바꾸며 새 단독 분기에서 FAIL해야 한다. `m 오류-02 --mutation=ignore-timeout`은 실패 주입 시 조회 상한을 30초로 바꿔 5초 지연을 허용하며 4초 경계에서 FAIL해야 한다. 성공 기준 호출은 두 변이 모두 보존한다. report/follow의 원인을 생략하는 사본도 FAIL한다. 격리 밖 premeasure 대상이다.

## Architecture

- [ ] 구조-01: Given 무효 시험 키를 가진 감독 계정, When 키가 들어간 명령 사건의 정상 종료와 오류 종료 및 모델 조회를 실행하면, Then follow·stdout/stderr·감독 기록·보고서·기억·실행 뒤 임시 사본 어디에도 키 원문이 없고 원본 auth와 사용자 settings.json은 불변이며 OS 알림 명령을 실행하지 않는다 [exact]
  측정: `m 구조-01`과 스크립트-07·08·오류-02의 no_leak 검사를 모두 통과해야 PASS. 원본 auth.json 한 파일만 제외한다. osascript/terminal-notifier/notify-send/afplay는 기록 전용 stub으로 받아 호출 0을 확인한다. 평가자는 변경 실행 코드에서 절대 경로·직접 OS API로 알림을 우회하거나 상태줄 기능을 제공하는 코드가 추가되지 않았는지도 대조한다.
  양성 대조: `m --controls-only`는 키가 든 파일 하나를 탐지한다. 알려진 답: 누출 파일 1개→1. 실제 계정 키는 읽지 않는다.
  음성 대조: `m 구조-01 --negative`는 산출물 누락으로 FAIL. 키를 출력하거나 사본에 남기는 변이는 같은 바이트 검사에서 FAIL한다.
- [ ] 구조-02: Given 구현 변경이 커밋된 U, When BASE..U 전체 경로를 생성물 제외 후 비교하면, Then 변경은 범위 목록의 부분집합이고 codex-audit.sh 변경을 포함하며 harness/marketplace 버전 변경·감독 모델 설정 변경·허용 밖 파일 변경은 없다 [exact]
  측정: `m 구조-02`; working/index/untracked의 `.harness/` 밖 미커밋 파일은 FAIL. `git diff --no-renames --name-only c78b4f09.."$U" -- . ':(exclude).harness'`를 사용하며 기대는 동등이 아닌 포함이다. project.yaml 변경은 premeasure·주석·공백 줄만 허용한다. 자동 모델 선택은 스크립트-08의 실제 exec로 별도 검사한다.
  양성 대조: `m 구조-02 --negative`는 변경 집합에 outside-fixture.txt를 추가하여 FAIL한다. 빈 변경 집합도 완료로 인정하지 않는다.
- [ ] 구조-03: Given 판정 격리와 새 측정 묶음, When 구현 감독의 사전 측정을 설정하고 사용법을 읽으면, Then project.yaml의 premeasure가 이 계약의 측정 명령을 조건 ID별로 실행하며 README는 follow의 세 시간 옵션과 모델 조회 주소·상한의 시험용 환경변수를 안내한다 [structural]
  측정: `m 구조-03`; 커밋된 설정에서 `bash .harness/.meta/codex-audit-progress/measure/measure.sh {id}`를 확인한다. README에서 --idle-seconds·--wait-seconds·--summary-seconds·CODEX_AUDIT_MODELS_URL·CODEX_AUDIT_CHECK_TIMEOUT을 읽는다. 설정 소비 동작은 스크립트-01의 사전 측정 실행이 검증한다.
  음성 대조: `m 구조-03 --negative`는 사본에서 premeasure 칸을 제거하여 FAIL한다.

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가 [exact]
  측정: `m 금지-03`; U 사본에서 설정 리터럴 `python3 scripts/validate-plugin.py --check=code-fence`를 실행해 V6 실행 표식과 종료 0을 확인한다. 기준선에서 실제 PASS했다.
  음성 대조: `m 금지-03 --negative`는 사본 스킬에 bare fence 하나를 추가하여 같은 V6가 FAIL해야 한다.
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL [exact]
  측정: `m 금지-04`; U 사본에서 `python3 scripts/validate-plugin.py --check=frontmatter`를 실행해 V1 실행 표식과 종료 0을 확인한다. 기준선에서 실제 PASS했다.
  음성 대조: `m 금지-04 --negative`는 사본 스킬의 name을 지워 같은 V1이 FAIL해야 한다.

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 부모·평가자 문서와 배포 README가 동일한 공개 codex-audit.sh follow 명령을 안내한다 [structural]
  측정: `m 재사용-01`; 스킬-01과 같은 배포 파일을 각각 검사한다. 측정 경로를 플러그인 실행 기능으로 삼으면 FAIL이다.
  음성 대조: `m 재사용-01 --negative`의 follow 지시 삭제는 FAIL한다.
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 기존 detach/wait 소비자는 진행 표시 추가 후에도 같은 공개 출력과 종료 코드로 결과를 받는다 [exact]
  측정: `m 재사용-02`; 스크립트-09의 실제 호출자 회귀를 재사용한다.
  음성 대조: `m 재사용-02 --negative`의 무출력 명령은 FAIL한다.

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze = `bash -n scripts/release.sh`의 대상 scripts/release.sh가 변경 범위에 없다) [exact]
  측정: `m 진단-01`; BASE..U의 scripts/release.sh 변경 목록이 비어 있어야 한다. 오류를 빈 출력으로 삼키지 않는다.
  양성 대조: `m 진단-01 --negative`는 대상 경로 하나를 주입하여 FAIL한다.
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 이번 셸 산출물에 적용하는 실행 가능한 진단 범위는 bash·zsh 구문 오류/경고 0개와 포함된 Python의 컴파일 오류 0개다 [exact]
  측정: `m 진단-02`; 공개 진입점에 bash -n·zsh -n을 실행하고 임베디드 Python 및 새 codex-audit 부속 폴더의 *.py를 compile한다. IDE 서버의 전체 의미 분석이나 shellcheck 실행을 했다는 뜻은 아니다.
  음성 대조: `m 진단-02 --negative`는 사본에 if then 구문 오류를 넣어 실제 파서가 FAIL한다.
- [ ] 진단-03: N/A (commands.test = `bash scripts/release.sh 2>&1 || true`는 변경하지 않는 릴리스 명령이며 이번 작업에서 릴리스를 실행하지 않는다) [exact]
  측정: `m 진단-03`; 진단-01과 같은 변경 교집합 0을 확인한다. 새 기능 실행 검사는 Script·Error 조건이 맡는다.
  양성 대조: `m 진단-03 --negative`의 대상 경로 주입은 FAIL한다.
- [ ] 진단-04: 실제 앱/서버 구동 시 에러 0개 — 이번 실행 진입점과 가짜 Codex 사건 스트림을 함께 기동하면 파싱 traceback 없이 상태 출력과 APPROVE·0을 받는다 [exact]
  측정: `m 진단-04`; 스크립트-02의 실제 프로세스 실행을 사용한다. 실제 모델 서버 호출·VS Code 화면 검증은 대신하지 않는다.
  음성 대조: `m 진단-04 --negative`는 FAIL한다.

## 범위 경계

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/scripts/codex-audit/
harness/templates/codex-audit/
harness/skills/sprint-contract/SKILL.md
harness/agents/qa-evaluator.md
harness/README.md
```

`.harness/`의 계약·측정·검토·진행 증거는 생성물로 제외한다. project.yaml은 이 묶음의 premeasure 연결만 바꾼다. 상태줄, macOS 알림, 사용자 설정 수정, harness 버전 상승, 감독 모델 변경·자동 변경, 릴리스·push는 범위 밖이다. 금지-01/02는 버전 하드코딩이나 force push 기능을 만들지 않으므로 선택하지 않았으며 버전 파일 불변은 구조-02가 잰다.

요구 대응: 자동 부모 진행 창·채팅→스킬-01·02, 단계/시각/측정→스크립트-01, Codex 활동 요약/명령 수/출력량→02, 침묵/임시 세션 성장→03, 종료/재생→04, 계약 선택/대기→05, 재시도/조사/재심→06, 새 모델·판/기억/단독 조회→07·08, 기존 wait→09, 인자 오류→오류-01, 조회 실패 비차단→오류-02, 키/설정/금지 기능→구조-01·02, 격리 밖 실행 연결→구조-03. 문서 생산자와 실제 부모 소비자를 분리해 판정한다.

## 회귀 게이트

`m <ID> [--negative|--mutation=이름]`는 W에서 `bash .harness/.meta/codex-audit-progress/measure/measure.sh <ID> [--negative|--mutation=이름]`다. cwd가 달라도 MEASURE_W 또는 기본 W를 읽는다. 반환 measurements의 상대 경로를 meta/codex-audit-progress 아래에 그대로 배치한다. Python 3.12 이상(현재 확인 3.14.3), git/tar, bash/zsh, 기존 V1/V6 검증기가 필요하다. 추가 패키지 설치는 하지 않는다. 임시 폴더는 TMPDIR 또는 MEASURE_TMP 아래이며 result.json에 U·검사 목록·명령·시각별 출력·종료 코드를 남긴다. evidence 경로를 QA 보고서에 인용한다. 도구 없음·시간 초과·증거 없음·예외는 FAIL·1이며 skip/PASS로 바꾸지 않는다. --controls-only는 오라클 준비 검사일 뿐 구현 PASS가 아니다.

구현 중에는 해당 ID, 커밋 뒤에는 U를 갱신하여 전체 ID, 최종 QA에서는 premeasure와 UI 독립 검토를 대조한다. 측정은 원본에 쓰지 않고 ps·재귀 강제 삭제 셸 명령을 사용하지 않는다. HTTP를 쓰는 세 ID는 premeasure로 격리 밖에서 실행하며 실제 외부 API와 npm에는 연결하지 않는다. UI 검토는 별도 VS Code 세션에서 증거를 수집한다. 새 부속 명령이 없음은 환경 탓으로 면제하지 않는다.

봉인 전 확인: U는 `c78b4f09ae6e3024dd9c2266b28940eb400cf3f7`였다. 조건 수 24·고유 번호 24·허용 헤더·봉인 필드 제외 검사를 통과했다. --controls-only, Python 구문, V6·V1·기존 셸/Python 구문과 기존 wait 회귀는 PASS했다. V1/V6·구문 진단의 결함 주입은 실제 FAIL했다. 새 follow·문서·UI 증거·설정 조건은 미구현/누락으로 FAIL했다. 교차 진단에서 지적한 완료 후 일괄 출력 허용, UI 자기 진술, 조회 경로 키 누출, 시간 측정 기준을 보완했다. 전체 새 동작의 성공·실제 UI·HTTP 분기 성공을 확인했다고 주장하지 않는다. 구현 후에도 양성/음성 사본을 다시 실행한다. 기존 회귀·N/A는 구현 전 PASS일 수 있지만 새 기능을 요구하는 ID는 부족한 명령·지시·증거·설정으로 FAIL해야 한다.

이번 개정의 검증은 이전 봉인 전 확인과 구분한다. 조건 줄 변경은 지적과 연결된 스킬-01·02, 스크립트-01·02, 오류-01·02, 구조-03에 한정하며 나머지 17개 조건 줄은 원문 그대로다. 구조-02의 대조 라벨은 현재 계약에 이미 `양성 대조`이므로 유지한다. 개정 실측: Python 구문·조건 수 24·관련 7개 조건 외 17개 조건 줄 불변 검사를 통과했다. 같은 단독 실패 검사에 넣은 셸 손 예제에서 사유/종료 2와 2초 timeout은 수용하고 미처리 예외/종료 1과 5초 대기는 거부했다. 같은 출력량 검사에서 간격 요약은 수용하고 명령별 40줄·간격 미만 중복 요약은 거부했다. 이는 미구현 기능이나 실제 UI·HTTP 분기의 성공을 뜻하지 않는다. 개정한 전체 측정과 각 결함 주입은 구현 후 U 사본에서 다시 실행해야 한다.
