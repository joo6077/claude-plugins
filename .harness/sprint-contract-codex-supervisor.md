---
feature: "Codex 계약 작성과 구현 감독"
created: "2026-10-01 17:57"
complexity: "복잡"
conditions: 27
slug: codex-supervisor
owner_session: fb4aefa8-0ee1-4711-9b22-7baf9c6b989f
status: done
conditions_digest: sha256:2467113bd3f57fd7
measurement_digest: sha256:dad78bc3ba520488
locked_at: "2026-10-06 12:57"
---
# Sprint Contract — codex-supervisor

## 배경

요구사항 정본은 W의 `.harness/.meta/codex-supervisor/requirements.md`다. W는 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor`, BASE는 `88b2a84e`, 상한은 `git rev-parse --verify -q feat/codex-supervisor`로 해석한다. 해석 실패는 FAIL이며 HEAD로 대체하지 않는다. 이번 계약은 `draft`가 아직 없어 사람이 Codex를 직접 불러 작성했다. Claude 평가자의 계약 검토와 사용자 승인, 봉인은 아직 하지 않았다. 봉인 필드 세 개는 의도적으로 없다.

복잡도 네 축: 외부 의존(Codex CLI와 세션 기록), 상태(작성·수정·재심·조사·반복), 생산자/소비자(JSON→스크립트→피드백→평가자·대기 훅), 실패 경계(일곱 실패 갈래와 세 운영 갈래)가 모두 있다. 따라서 복잡이며 기능 조건은 19개다. 계약·측정만 작성하고 구현하지 않는다.

설정 리터럴 대조: Skill/스킬, Script/스크립트, Error/오류, Architecture/구조를 그대로 쓴다. `commands.analyze`는 `bash -n scripts/release.sh`, `commands.test`는 `bash scripts/release.sh 2>&1 || true`, `diagnostics.ide_exclude`는 `[]`다. 금지-03·04의 message와 command는 설정 그대로 아래에 옮겼다.

사전 확인: `harness/scripts/qa-pending-check.sh`는 `Verdict:`를 읽고, `harness/scripts/measure-common.sh`는 공통 측정 함수를 제공한다. `harness/skills/sprint-contract/SKILL.md`의 6.2·6.5·6.6·6.7, `harness/agents/qa-evaluator.md`의 Step 5.5·Step 7, `harness/templates/project.yaml`, `harness/README.md`, `scripts/validate-plugin.py`는 실제로 읽었다. 새 구현 경로 두 곳은 요구사항 §4에 있는 `harness/scripts/codex-audit.sh`와 `harness/templates/codex-audit/`뿐이며 현재 없다. 템플릿 아래 개별 파일 이름이나 내부 함수 이름은 지정하지 않는다.

설계 해석을 명시한다. 요구사항의 «계약 폴더»는 contract-schema의 CONTRACT_ROOT를 뜻하도록 통일한다. 계약이 R/.harness 안에 있으면 감독·측정·피드백도 R/.harness 아래다. 파일의 dirname 아래에 .harness를 한 번 더 만들면 기존 대기 훅이 결과를 못 읽기 때문이다. `max_rounds: 2`는 최초 판정 뒤 수정·재감독 두 번을 허용한다(최대 impl 3회, 각 REJECT의 맹검 재심은 별도 차례). 네 번째 impl은 BLOCKED다. 기본 effort는 §4의 medium을 따른다(§2의 low 제안보다 §4 설정을 우선한다).

측정 가능한 외부 응답 경계를 구체화한다. §2의 output-schema 사용과 §4의 명령을 연결하기 위해 Codex의 마지막 JSON 응답은 다음 형식으로 정한다. 이것은 외부 입력/출력 계약이며 구현 내부 자료구조나 템플릿 파일명을 정하지 않는다. 이 구체화에 동의하지 않는 구현자는 봉인 전에 계약 검토에서 변경해야 하며, 측정기를 구현에 맞춰 사후 완화하지 않는다.

- draft·revise: `contract`(계약 본문 문자열), `measurements`(각 원소가 `path` 상대 경로와 `content` 문자열인 배열). 스크립트가 저장 검사를 통과한 뒤 선점된 계약과 `R/.harness/.meta/<slug>/`에 옮긴다. Codex의 작업 경로는 임시 폴더다.
- impl: `conditions` 배열, `verdict`(APPROVE/REJECT/RESEARCH), `questions` 문자열 배열. 조건 원소는 `id`, `evidence`, `analysis`, `verdict`(PASS/FAIL), `fix` 순서이며 fix는 `where`, `what`, `verify` 세 문자열이다. PASS의 fix는 빈 문자열이어도 되지만 FAIL의 세 칸은 공백 제거 후 모두 비어 있지 않아야 한다. evidence·analysis도 비어 있지 않아야 한다. RESEARCH는 중간 응답이고 최종 REJECT가 아니다.
- 조사 차례: `answers` 배열, 각 원소는 `question`, `answer`, `sources`(URL 문자열 배열). 질문과 답을 보존하고 다음 인터넷 허용 판정에 전달한다. 조사 응답에 구현 최종 판정을 맡기지 않는다.
- draft·revise·impl·조사 네 호출의 형식 검사는 strict JSON 스키마와 셸의 의미 검사 둘 다 필요하다. 빈 응답은 응답 메시지와 결과 파일이 모두 없을 때다. 메시지는 있는데 파일만 없거나 종료·사건·내용이 서로 모순되면 형식-깨짐이다.

확인 못 함: 실제 Codex 서버의 현재 응답 모델, 실제 CLI/OS의 원본 쓰기 차단, Claude가 문서대로 행동하는 확률은 이번 초안 검증으로 증명하지 못한다. 모델의 관측 정의는 요구사항 §3대로 해당 thread_id의 turn_context.model이며 서버 측 모델 추정은 하지 않는다. 스크립트-11만 실제 Codex를 호출한다. 구현 전에는 MISSING으로 멈추므로 이번 작성 검증의 실제 모델 호출은 0회다. 로그인 준비 확인은 비용 없는 login status만 호출한다. 문서 조건은 명시된 절차 문장과 훅의 소비 동작을 재며 Claude 실행을 가장하지 않는다.

반복 1회차 지적 반영: 요구사항 §2의 역할 부여 금지·짧은 프롬프트는 구조-02, 운영 전 알려진 답 검증은 스크립트-11에 넣었다. 지시문 상한 8192 UTF-8 바이트는 연구가 증명한 최적값이 아니라 이 계약의 운영 예산이다. draft·revise·impl·조사 네 차례 지시에 각각 2 KiB를 배정한 합계이며, 계약·코드·증거는 파일 참조로 전달하고 출력 JSON 스키마는 제외한다. 핵심 중립 규칙을 담은 측정 표본은 실제 327바이트다. 파일을 쪼개 상한을 우회하지 않도록 템플릿 디렉터리의 지시문을 합산한다. 예시/예제/example 표제로 된 풀이 예시는 합계 1개까지만 허용한다. 엄격·감사관은 지시문에서 금지하며, auditor와 strict/harsh의 역할 부여 꼴도 검출한다. 스키마 속성 strict 자체는 역할 지시가 아니므로 JSON 스키마를 판정에서 제외한다.

반복 2회차 지적 반영: 네 호출의 스키마 전달은 스크립트-10이 모두 재고, 오류-01은 기존 impl 17개 입력에 draft·revise·조사 각 3개 형식 오류를 더해 총 26개 입력을 잰다. 구조-02의 격리 우회 옵션 이름을 명시했다. 당시 조건 수는 전체 26개·기능 18개였다.

2026-10-06 사용자 결정 3·11이 앞선 감독 폴더 직접 사용 방침을 대체한다. 판정 차례도 인터넷을 허용하지만 지시문은 「바깥 사실은 스스로 찾지 말고 질문으로 내라」를 유지한다. 쓰기는 복제 사본·임시 폴더 안으로 제한한다. 조사 차례 분리와 재판정은 그대로다.

사용자 위험 수용: 로그인 원본은 기본 탐색(~/.codex-qa 우선, 없으면 CODEX_HOME 또는 ~/.codex)으로 선택한 설정 폴더의 auth.json에 권한 600으로 저장한다. 사용자는 판정 중 실행되는 구현물·측정 명령이 이 파일을 읽고 인터넷으로 내보낼 수 있는 위험을 알고 받아들였다. 키 사용처 제한·사용 한도가 있는 키 권고는 요구사항에 있으며, 이번 작업에서 계정 설정이나 한도를 변경하지 않는다.

«감독 폴더에 키 글자 없음»의 범위를 구분한다. 로그인 설정 폴더의 원본 auth.json과 실행 중 필요한 권한 600의 임시 인증 사본은 결정 11이 허용한 예외다. 스크립트·실행 출력·세션 기록·감독 산출물 폴더(codex-audit)·보고서·피드백·얼린 입력에는 키 원문이 없어야 하며, 실행 종료 후에는 원본 auth.json 외의 키 사본이 남지 않아야 한다. 구조-04는 정상·형식 실패·시간 초과·SIGINT·SIGTERM 다섯 경로를 잰다. 확인 못 함: SIGKILL·전원 단절처럼 정리 코드를 실행할 수 없는 중단의 즉시 삭제는 이 계약으로 보장하지 못하며 범위 경계에 제외 사유를 기록한다.

스크립트-11의 실제 호출 측정은 auth.json·config.toml을 측정 폴더 아래 쓰기 가능한 권한 700의 임시 폴더로 복사하고, 인증 사본은 생성 시점부터 600으로 만든다. model·effort는 원래 설정을 유지한다. 임시 프로젝트의 codex_audit.codex_home과 CODEX_HOME에 그 사본 경로를 명시하여 ~/.codex-qa 우선 탐색이 읽기 전용 원본으로 되돌아가지 않게 한다. 격리 안·밖에서 같은 방법을 쓰며 원래 폴더에는 쓰지 않는다. 세션 기록은 쓰기 가능한 실행 폴더에 남기고 인증 사본만 finally와 SIGINT/SIGTERM 처리로 삭제한다.

`m 스크립트-11 --prepare-only`는 file 저장 설정·원본 auth.json 권한 600을 검사하고, 원본과 임시 사본에서 각각 codex login status만 실행한다. 둘 다 Logged in·종료 0이고 정리가 끝나야 PREPARED다. 인증 전제 불성립은 PRECONDITION_UNMET·종료 2·implementation_evaluated=false로 구분한다. 2026-10-06 이 격리 환경에서 양쪽 Logged in using an API key·종료 0, 사본 권한 600·삭제 완료·원본 불변·키 누출 0을 확인했다. 실제 모델은 사용자 지시대로 호출하지 않았다.

반복 3회차는 2026-10-06 사용자의 상한 초과 진행 지시로 수행한다. 전체 조건 27개·기능 19개이며 결정 11을 위한 구조-04를 추가한다. 측정 소스의 삭제는 Python unlink/shutil만 사용하고 재귀 강제 삭제 셸 명령은 사용하지 않는다.

## Skill

- [ ] 스킬-01: Given mode가 codex 또는 off인 프로젝트, When `m 스킬-01`, Then `harness/skills/sprint-contract/SKILL.md`가 codex에서는 Claude의 조건 직접·손 편집을 금지하고 요구사항→draft→저장 검사/평가자 지적→revise→Claude 평가자 APPROVE→사용자 승인→6.6 봉인→6.7 커밋 순서 및 max_rounds 초과 시 사용자 판단을 명시하며 off에서는 기존 작성 절차를 유지한다 [structural, enumerated]
  측정: `m 스킬-01`; 원문 대비 변경과 해당 지시의 문장·토큰을 검사한다. 구현 전에도 존재하던 일반 QA 문구만으로는 통과하지 않는다. evidence.json의 document 항목이 전부 OK여야 PASS다.
  음성 대조: `m 스킬-01 --negative`는 사본에서 mode: codex를 제거하므로 FAIL이다. 문서 의미·순서의 최종 확인은 Claude 계약 평가자가 위 조건과 원문을 대조하며, 키워드가 있어도 반대 지시가 남아 있으면 FAIL이다.
- [ ] 스킬-02: Given 구현 감독의 생산물과 두 mode, When `m 스킬-02`, Then `harness/agents/qa-evaluator.md`는 계약 검토에서 조건 번호·문제·고칠 방법과 APPROVE/REJECT를 내고, codex 구현 QA마다 스스로 조건을 판정하지 않고 impl --detach→wait→스크립트의 Verdict: 그대로 보고→APPROVE일 때 Step 5.5의 status done만 수행하며 판정 변경·덧붙임을 금지하고 off는 기존 판정을 유지한다; `harness/scripts/qa-pending-check.sh`는 생성된 APPROVE를 통과시키고 REJECT를 안내한다 [exact, enumerated]
  측정: `m 스킬-02`; 새 문서 지시와 실제 훅 stdin/출력을 함께 잰다. 생산자는 스크립트-03이고 소비자는 이 조건이다. 현재 문서의 충돌 지시가 codex 모드에서도 실행되도록 남으면 FAIL이다.
  양성 대조: 훅에 들어갈 REJECT 피드백은 스크립트가 실제 생성한다. 지금 가능한 계수 대조는 `m 스킬-02 --controls-only`의 알려진 입력이며, 구현 후 훅 출력의 REJECT가 1건 이상이어야 한다.
  음성 대조: `m 스킬-02 --negative`는 mode 지시를 제거하고 감독 명령을 no-op으로 바꾸므로 FAIL이다.

## Script

- [ ] 스크립트-01: Given 선점된 빈 계약, When `m 스크립트-01`이 draft를 호출, Then 유효 본문과 측정 묶음은 지정 경로에 설치되고 종료 0·APPROVE이며 저장 검사 결과가 보고서에 남고, 비어 있지 않음·미선점·허용 밖 헤더·서술 절 조건·조건 수 불일치·미실측 마커 입력은 성공으로 저장되지 않는다 [exact, enumerated]
  측정: `m 스크립트-01`; fixtures.py의 일곱 입력을 각각 실행한다. 비어 있지 않음·미선점은 Codex 호출 0회, 실패 전후 계약 바이트 동일이다. valid는 호출 1회와 본문·measure.sh 설치를 대조한다.
  양성 대조: `m 스크립트-01 --controls-only`의 login 1행+exec 2행 로그를 같은 호출 계수기로 읽어 positive_control=2. 알려진 답: 기대 exec 2, 실제 2, 종료 0.
  음성 대조: `m 스크립트-01 --negative`는 사본의 명령을 exit 0만 남겨 실패 저장 방지·파일 설치 검사가 FAIL이다.
- [ ] 스크립트-02: Given 미봉인 계약과 지적 또는 conditions_digest가 있는 계약, When `m 스크립트-02`가 revise를 호출, Then 미봉인 계약은 지적 반영 본문으로 바뀌고 이전 바이트 전체가 감독 폴더에 보존되며, 봉인 계약은 호출 0회·바이트 불변·종료 2·BLOCKED와 봉인됨 갈래다 [exact, enumerated]
  측정: `m 스크립트-02`; 이전 본문과 동일한 파일을 감독 폴더 전체에서 찾고 봉인 입력을 별도로 실행한다.
  양성 대조: `m 스크립트-02 --controls-only` 호출 계수기 positive_control=2. 알려진 답: login은 제외한 exec 2행을 2로 센다.
  음성 대조: `m 스크립트-02 --negative`에서 no-op 구현은 보존·변경·봉인 거부 검사를 통과할 수 없다.
- [ ] 스크립트-03: Given 두 조건과 기준·구현 커밋, When `m 스크립트-03`의 impl에 유효한 전체 PASS를 반환, Then 종료 0·APPROVE, R/.harness/sprint-feedback-sample.md의 Verdict: APPROVE·Iteration: 1·각 조건 결과, 그리고 얼린 계약·차이·파일 목록이 존재하며 계약 status는 스크립트가 바꾸지 않는다 [exact, enumerated]
  측정: `m 스크립트-03`; sample은 시험용 slug다. 피드백 생산자를 직접 실행하고 파일 바이트·내용을 검사한다. Codex가 피드백을 쓰도록 시뮬레이션하지 않는다.
  양성 대조: `m 스크립트-03 --controls-only` positive_control=2. 알려진 답: 로그인 제외 호출 수 기대 2·실제 2.
  음성 대조: `m 스크립트-03 --negative`의 exit 0만 내는 사본은 출력 파일 검사가 FAIL이다.
- [ ] 스크립트-04: Given 최초 REJECT, When `m 스크립트-04`, Then 최초 분석을 숨긴 별도 작업 사본·새 thread의 재심을 정확히 한 번 받고, 두 번 모두 같은 조건 FAIL이면 종료 1·REJECT와 조건별 어디를·무엇으로·어떻게 확인을 남기며, 재심 PASS 또는 서로 다른 조건 FAIL이면 종료 2·BLOCKED와 재심-엇갈림이다 [exact, enumerated]
  측정: `m 스크립트-04`; 같은 FAIL/재심 PASS/다른 FAIL의 세 입력, resume 부재·서로 다른 cwd·thread_id·첫 분석의 두 번째 프롬프트 부재를 대조한다. 첫 결과 폴더를 두 번째 판정에 읽기 자료로 주지 않아야 한다.
  양성 대조: `m 스크립트-04 --controls-only` positive_control=2. 알려진 답: 호출 두 행을 2로 센다.
  음성 대조: `m 스크립트-04 --negative`의 no-op 명령은 재심 2차례와 출력 검사에서 FAIL이다.
- [ ] 스크립트-05: Given 질문 없는 판정 또는 외부 사실 질문, When `m 스크립트-05`, Then 모든 판정·조사 차례는 인터넷을 허용하되 판정 차례에는 바깥 사실은 직접 찾지 말고 질문으로 내라는 지시를 전달하며, 질문 없이는 판정 1차례만, 질문 있으면 판정→별도 조사→답을 첨부한 재판정 3차례만 실행하고 질문·답을 보고서에 남긴 뒤 최종 APPROVE를 낸다 [exact, enumerated]
  측정: `m 스크립트-05`; fake의 network 관측 배열 [true]와 [true,true,true], 질문 FACT_TOKEN·답 FACT_ANSWER 전달을 대조한다. 판정 지시문·템플릿에서 바깥 사실 직접 조사 금지·질문 제출 문장도 확인한다. 조사 응답의 예시 URL은 손 예제이며 실제 인터넷을 사용하지 않는다.
  양성 대조: `m 스크립트-05 --controls-only` positive_control=2. 알려진 답: 호출 두 행을 2로 센다.
  음성 대조: `m 스크립트-05 --negative`는 실행 차례·질문·답 검사가 FAIL이다.
- [ ] 스크립트-06: Given 최초 REJECT와 기본 max_rounds=2, When `m 스크립트-06`이 고친 뒤 재감독을 반복, Then 최초 및 두 번 재감독까지 판정하고 그 다음은 Codex 추가 호출 없이 종료 2·BLOCKED·반복-상한이며 2회차부터 지난 FAIL 번호별 해결/미해결을 남긴다; max_rounds=1이면 재감독 한 번 뒤 멈춘다 [exact, enumerated]
  측정: `m 스크립트-06`; 계속 REJECT와 REJECT 뒤 APPROVE를 별도 프로젝트에서 실행한다. Iteration은 1·2·3이며 기본 상한까지 재심 포함 exec 6회, max_rounds=1이면 4회다.
  양성 대조: `m 스크립트-06 --controls-only` positive_control=2. 알려진 답: exec 두 행→2이며 나열된 6·4는 각 판정의 2차례를 손으로 합한 기대값이다.
  음성 대조: `m 스크립트-06 --negative`는 반복 차단·지난 지적 결과가 없어 FAIL이다.
- [ ] 스크립트-07: Given 설정 매트릭스, When `m 스크립트-07`, Then mode 기본 codex·off의 draft/revise/impl 종료 3와 호출 0, 명시 codex_home 우선·없을 때 ~/.codex-qa 우선·그것도 없으면 기본 폴더, model 명시값 우선·없으면 선택 폴더 model·둘 다 없으면 설정-오류 BLOCKED, effort_draft/effort_impl 기본 medium·각 override를 따른다 [exact, enumerated]
  측정: `m 스크립트-07`; 실제 모델명을 하드코딩했으면 임의의 fixture-folder-model·fixture-override·other-model·normal-model 전달 검사가 실패한다. mode 잘못된 값도 BLOCKED다. 임시 HOME만 바꾸며 실제 사용자 폴더는 쓰지 않는다.
  양성 대조: `m 스크립트-07 --controls-only` positive_control=2. 알려진 답: exec 2행→2. off 입력의 계약 바이트도 동일해야 한다.
  음성 대조: `m 스크립트-07 --negative`는 SKIPPED와 설정 갈래를 내지 못해 FAIL이다.
- [ ] 스크립트-08: Given 차례별 세션과 더 최신인 무관한 세션, When `m 스크립트-08`, Then 감독 폴더의 report.md 머리에 시작·끝·계정, 각 차례에 해당 thread_id의 모델·생각 강도·격리 종류·기록 경로, 마지막에 감독 판정이 있으며 로그인 출력의 using 부분만 남기고 키 원문은 스크립트·감독 산출물 폴더·보고서·피드백·얼린 입력·임시 잔여물에 0건이고 무관한 세션 값도 0건이다 [exact, enumerated]
  측정: `m 스크립트-08`; fake는 요청 모델과 다른 -observed 값을 turn_context에 쓰고 WRONG-DECOY도 만든다. 감독 산출물 전체에서 sk-FIXTURE-SECRET·WRONG-DECOY 검출이 0이어야 한다.
  양성 대조: `m 스크립트-08 --controls-only`가 임시 report.md에 키 표본을 심고 같은 검출기로 positive_control=1. 알려진 답: 한 오염 파일→1, 종료 0.
  음성 대조: `m 스크립트-08 --negative`는 차례별 출처가 없어 FAIL이다.
- [ ] 스크립트-09: Given draft·revise·impl 및 잘못된 인자, When `m 스크립트-09`, Then --detach는 3초 걸리는 감독을 기다리지 않고 2초 안에 감독 폴더 경로와 종료 0을 내며 wait 0은 RUNNING·75, 완료 뒤 wait는 원래 0/1/2, 명령 없음·모르는 명령·각 필수 인자 누락·잘못된 wait 인자는 64다 [exact, enumerated]
  측정: `m 스크립트-09`; 세 부속 명령의 detach와 APPROVE/REJECT/BLOCKED 완료를 각각 잰다. wait <폴더> [초]의 초는 생략 가능하며 0은 즉시 상태 확인이다.
  양성 대조: `m 스크립트-09 --controls-only` positive_control=2. 알려진 답: 호출 두 행→2. 반환 코드 75는 RUNNING의 명세값이며 호출 수와 혼동하지 않는다.
  음성 대조: `m 스크립트-09 --negative`는 폴더·RUNNING·75를 내지 못해 FAIL이다.
- [ ] 스크립트-10: Given draft·revise·impl·조사 네 종류의 Codex 호출, When `m 스크립트-10`, Then --output-schema로 외부 응답 형식을 전달하고 모든 object의 required가 properties와 일치하며 additionalProperties=false·allOf/if/then 0건이고 impl 조건 키 순서는 evidence→analysis→verdict다 [exact, enumerated]
  측정: `m 스크립트-10`; draft 1회·revise 1회·impl 1회와 질문 impl→조사→재판정 impl 3회의 여섯 실제 fake 호출을 수집한다. 호출마다 --output-schema 파일의 object 전체 필수 칸 일치·additionalProperties=false·금지 결합 부재와 그 차례의 유효 응답 통과를 재며, impl 응답만 evidence→analysis→verdict 순서도 잰다. 네 종류 중 하나라도 호출 또는 틀이 빠지면 FAIL이다. 템플릿 파일 이름은 자유다.
  양성 대조: `m 스크립트-10 --controls-only`에서 두 필드 중 둘째 required만 누락한 스키마를 같은 검사기로 읽어 positive_control=1. 네 차례별 스키마에서도 required 누락을 각각 검출하고 revise·조사의 스키마 미전달은 검출 2/2여야 한다. 알려진 답: 좋은 스키마 required 수 2·실제 2, 네 차례의 유효 스키마 기대 4·실제 4.
  음성 대조: `m 스크립트-10 --negative`는 스키마를 전달하지 않아 FAIL이다.

- [ ] 스크립트-11: Given 기본 감독 설정 폴더의 파일 로그인과 쓰기 가능한 권한 600 인증 사본의 로그인 준비 전제가 성립하고 조건 하나의 좋은 구현·나쁜 구현을 담은 임시 Git 저장소, When `m 스크립트-11`이 실제 Codex로 impl을 각각 실행, Then 좋은 예는 종료 0·APPROVE, 나쁜 예는 맹검 재심 뒤 종료 1·REJECT와 FAIL 조건의 어디를·무엇으로·어떻게 확인 세 칸을 남기고, report.md의 각 차례 모델·생각 강도는 해당 thread_id의 새 실제 세션 turn_context 값과 일치하며, 로그인 전제 불성립은 구현 판정 없이 PRECONDITION_UNMET·종료 2로 구분한다 [exact, enumerated]
  준비 단계: `m 스크립트-11 --prepare-only`가 원본 설정 폴더와 쓰기 가능한 인증 사본의 절대 경로·codex login status의 Logged in 여부·종료 코드, 사본 권한 600·삭제 여부·원본 불변·키 누출 수를 출력한다. 성공은 PREPARED·종료 0, 미로그인은 측정 전제 불성립·종료 2이며 두 경우 모두 모델 호출 0·implementation_evaluated=false다.
  실제 codex 호출 · 비용 발생. 정상 경로는 좋은 예 1차례·나쁜 예 최초 판정과 재심 2차례로 총 3차례이며 측정기가 재실행을 반복하지 않는다. 다른 조건의 가짜 Codex 결과를 재사용하지 않는다.
  측정: `m 스크립트-11`; live_calibration.py가 sample.txt의 정확한 바이트 GOOD+줄바꿈 한 개를 요구하는 계약을 만들고, GOOD+줄바꿈과 BAD+줄바꿈을 서로 다른 저장소에 커밋한다. 기본 감독 설정 폴더의 auth.json·config.toml을 쓰기 가능한 임시 폴더로 복사하고, CODEX_HOME과 임시 프로젝트의 codex_audit.codex_home에 그 경로를 지정한다. 인증 사본은 600이며 정상·실패·시간 초과·SIGINT/SIGTERM 뒤 삭제한다. 원래 HOME과 설정의 model·effort는 유지한다. PATH의 기본 Codex 또는 확인된 @openai/codex 설치의 네이티브 바이너리만 사용한다. 중첩 실행에서 물려받은 CODEX_BIN은 이 기본 설치의 실제 경로와 같을 때만 허용하고 가짜·다른 경로는 거부한다. 실제 네트워크 서비스 사용을 위해 custom provider/endpoint는 거부한다.
  측정: report 차례 수는 좋은 예 1·나쁜 예 2이며 기록 경로는 쓰기 가능한 이번 측정 실행 폴더 안의 sessions 경로에서 이번 호출 시작 이후 생성된 새 파일이어야 한다. 호출 전 기존 파일 목록에도 없고 생성/수정 시각이 시작 시각 이후여야 한다. thread.started와 session_meta.id·파일명 UUID를 대조하고 assistant response_item 및 turn_context를 요구한다. 가짜의 turn_context 한 줄이나 오래된 세션 파일만으로는 PASS할 수 없다. 원본·사본 사전 로그인 미확인은 PRECONDITION_UNMET·종료 2이며 구현 판정은 수행하지 않는다. 전제 성립 후 실행 실패·네트워크 문제·기록 부재·무효 판정은 FAIL이다. 구현이 없으면 바이너리 탐색·API 호출 전에 MISSING으로 FAIL한다.
  양성 대조: `m 스크립트-11 --controls-only`에서 가짜 실행 파일이 네이티브 Codex 검사를 통과하지 못해 positive_control=1이며 생각 강도를 바꾼 세션 표본도 불일치로 잡는다. 실제 모델 호출 없이 준비하는 대조다. 알려진 답: 임시 Git의 GOOD 측정 종료 0, BAD 측정 종료 기대 1·실제 1; 같은 모델·생각 표본 일치 기대 1·실제 1.
  음성 대조: `m 스크립트-11 --negative`는 가짜 CODEX_BIN을 주입하고 LIVE_FAKE_OVERRIDE_REJECTED와 FAIL·종료 1을 요구한다. 이 대조는 비용이 없다. 실제 좋은/나쁜 판정의 PASS 증거는 일반 실행만 만들 수 있다.

## Error

- [ ] 오류-01: Given impl의 기존 17개 오류 입력과 draft·revise·조사마다 결과 파일 없음·깨진 JSON·필수 칸 빠짐을 넣은 9개 입력, When `m 오류-01`, Then nonzero 종료·turn.completed 없음·turn.failed·error·깨진 JSON·결과 파일 없음·추가 키·잘못된 타입·조건 누락·중복·없는 번호·전체/개별 판정 모순 두 방향·FAIL 수정 세 칸 각각 공백·증거 공백 및 다른 세 호출의 형식 오류를 각각 종료 2·BLOCKED·형식-깨짐으로 처리하고 유효 APPROVE/REJECT로 저장하거나 재시도하지 않는다 [exact, enumerated]
  측정: `m 오류-01`; 기존 impl 17개에서 missing-id 등은 두 번째 조건만 변조한다. 추가 9개는 draft의 contract, revise의 measurements, 조사의 answers 필수 칸을 각각 삭제하거나 그 응답의 결과 파일을 없애거나 JSON을 깨뜨린다. impl·draft·revise 입력별 exec 1회, 조사 입력별 질문 impl 1회+깨진 조사 1회로 exec 2회이며 이후 재판정/재시도는 없어야 한다. draft·revise의 실패 전후 계약 바이트도 동일해야 한다. 읽지 못함을 누락 입력으로 시험하며 여러 조건 중 하나만 남겨도 실패다.
  양성 대조: `m 오류-01 --controls-only`의 호출 계수기 positive_control=2. 추가로 실제 fake-codex에 draft·revise·조사 응답별 세 오류를 주입하여 결과 파일 없음·JSON 파싱 실패·스키마 필수 칸 누락을 아홉 번 생성·검출한다. 알려진 답: 로그인 1행+exec 2행→2, 추가 형식 오류 기대 9·실제 9. 기존 17개는 invalid 목록, 추가 9개는 fixtures.py의 nonimpl_faults 매트릭스와 일대일이다.
  음성 대조: `m 오류-01 --negative`는 잘못된 응답을 막지 않는 exit 0 사본이라 FAIL이다.
- [ ] 오류-02: Given Codex 없음·로그인 없음·시간 초과·빈 응답·한도/결제·설정 오류, When `m 오류-02`, Then 일곱 실패 갈래 중 형식-깨짐은 오류-01대로, 나머지 여섯은 정확한 갈래와 종료 2·BLOCKED이고 시간 초과·빈 응답만 새 세션 1회 재시도하며 한도/결제·설정 오류는 재시도하지 않고 시간 초과의 자식 프로세스까지 종료한다 [exact, enumerated]
  측정: `m 오류-02`; CODEX_AUDIT_LIMIT=2, 연속 실패와 한 번 실패 뒤 회복을 모두 실행한다. 명령 없음·로그인 없음은 exec 0, 한도/설정은 1, 연속 시간 초과/빈 응답은 2. 기본 600초는 구조-03의 배포 안내 및 CLI 기본 설정과 대조한다.
  양성 대조: `m 오류-02 --controls-only` positive_control=2. 알려진 답: 같은 호출 계수기에서 exec 두 행→2. 프로세스 번호는 실행 시 기록하고 ps 결과를 남긴다.
  음성 대조: `m 오류-02 --negative`는 BLOCKED·재시도·종료 증거가 없어 FAIL이다.

## Architecture

- [ ] 구조-01: Given 이 스프린트의 커밋이 끝난 뒤, When `U=$(git rev-parse --verify -q feat/codex-supervisor) || exit 2; git diff --no-renames --name-only 88b2a84e.."$U" -- . ':(exclude).harness'` 및 `m 구조-01`, Then 변경 경로는 범위 목록 블록의 허용 집합에 포함되고 구현 스크립트가 포함된 비어 있지 않은 차이이며 플러그인·marketplace 버전 파일 변경은 0이다 [exact, enumerated]
  측정: `m 구조-01`; 범위 목록을 직접 읽는다. pathspec은 전체 `.`이고 생성·기록물 `.harness`는 제외한다. 기대 집합은 정확히 일치가 아닌 포함이다. 해석 실패는 멈춘다.
  양성 대조: `m 구조-01 --controls-only`의 허용 스크립트와 outside.txt 두 경로→범위 밖 1. 알려진 답: a,b,c 중 a만 허용→범위 밖 기대 2·실제 2.
- [ ] 구조-02: Given 구현 커밋과 원래 작업 폴더, When `m 구조-02`, Then 임시 Git 사본의 커밋은 구현 커밋과 같고 .git은 원본과 다르며 사본 쓰기는 성공·원본 파일 및 .git 변화 0, 판정 CLI는 쓰기를 복제 사본·임시 폴더 안으로 제한하는 workspace-write·인터넷 허용·닫힌 stdin이고 ephemeral·ignore-user-config·격리 우회 옵션(--dangerously-bypass-approvals-and-sandbox) 없이 증거 규칙과 입력은 데이터라는 지시를 전달하며, JSON 스키마를 제외한 codex-audit 템플릿 지시문 합계와 손 예제 impl에 실제 전달한 지시문 각각에서 엄격·감사관·auditor 및 strict/harsh 역할 부여 꼴이 0건이고 크기는 8192 UTF-8 바이트 이하·풀이 예시 표제는 1개 이하다 [exact, enumerated]
  측정: `m 구조-02`; fake가 cwd에 probe.txt를 쓰고 전후 원본 해시를 비교한다. 부모 입력 파이프를 열어 둔 채 실행하므로 stdin을 닫지 않으면 시험 상한으로 FAIL이다. draft/revise도 임시 폴더 cwd·원본 바이트 보호를 스크립트-01·02와 같이 재야 한다.
  측정 보강: prompt_checks.py가 harness/templates/codex-audit/의 파일을 읽어 object/properties 형태의 JSON 스키마만 제외하고 지시문 바이트·역할 부여 정규식·예시 표제를 합산한다. strict reviewer, harsh judge, be strict, act as an auditor와 한국어 표본을 검출한다. 계약·코드·증거 데이터는 템플릿 크기 예산에 넣지 않는다. 손 예제 impl 호출의 실제 위치 인자와 stdin 지시문도 별도로 같은 기준으로 검사하여 호출 시 역할을 덧붙이는 경우를 잡는다. CLI 옵션의 스키마/출력 경로·모델·설정값은 지시문으로 세지 않는다.
  양성 대조: `m 구조-02 --controls-only`는 원래 트리 변경 대조 positive_control=1에 더해 역할 부여 다섯 표본을 같은 지시문 검사로 각각 검출하여 prompt_role_positive=5, 8193바이트와 예시 표제 두 개를 위반으로 검출한다. 알려진 답: 한 파일 변경→1, 문자열 가나다·줄바꿈·AB의 UTF-8 길이 기대 12·실제 12, 8192바이트 경계 통과, 예시 두 표제 기대 2·실제 2. JSON 스키마의 strict 속성은 제외되어 지시문 표본 1개만 센다.
  음성 대조: `m 구조-02 --negative`는 임시 템플릿 사본에 역할 부여 문장, 8193바이트, 예시 두 개를 각각 넣어 같은 검사에서 세 FAIL을 낸다. 구현 전에는 중립 손 예제 템플릿 사본에 주입한다. no-op 명령이나 MISSING 때문인 실패로 이 검사를 대신하지 않는다. 이 조건은 OS 격리의 실효성을 실제 Codex로 증명했다는 뜻은 아니다.
- [ ] 구조-03: Given 배포 파일, When `m 구조-03`, Then `harness/templates/project.yaml`에 codex_audit의 mode·codex_home·model·effort_draft·effort_impl·max_rounds 여섯 칸, `harness/templates/codex-audit/`에 지시문/스키마 산출물, `harness/README.md`의 스크립트 표에 codex-audit.sh 행과 CODEX_BIN·CODEX_AUDIT_LIMIT 기본 600 안내가 있다 [structural, enumerated]
  측정: `m 구조-03`; 새 프로젝트 설정 생산자를 검사한다. 설정 소비자는 스크립트-07이다. 경로·칸·표 행 누락은 FAIL이다.

- [ ] 구조-04: Given 권한 600의 파일 auth.json으로 로그인하는 감독 설정 폴더, When `m 구조-04`가 impl의 정상·형식 실패·시간 초과·SIGINT·SIGTERM 다섯 경로를 실행, Then 판정 차례에서 같은 인증 파일을 읽을 수 있고 인증 사본을 만들면 실행 중 권한 600이며 모든 경로 종료 뒤 사본 파일과 원본 auth.json 밖 키 원문은 0건이고 원본 내용·권한은 불변이다 [exact, enumerated]
  측정: `m 구조-04`; 가짜 CODEX_BIN이 실제 읽은 인증의 일치 여부·권한과 실행 중 키 사본 경로·권한만 기록한다. 키 바이트는 기록하지 않는다. 종료 후 사본 경로 부재와 시험 폴더 전체 키 원문 부재를 검사하며 원본 auth.json 하나만 제외한다. 정상은 종료 0, 형식 실패·시간 초과는 2, 중단은 0과 강제 종료 124 이외이며 인증 소비 프로세스와 자식은 남지 않아야 한다. 축은 종료 원인 5개×파일 로그인 1개로 cases_total=5다.
  양성 대조: `m 구조-04 --controls-only`에서 권한 644의 키 사본·키가 든 출력 두 파일을 검사해 positive_control=2. 알려진 답: 키 잔여 파일 기대 2·실제 2, 측정기 자신이 쓰는 인증 복사 도우미의 정상·실패·시간 초과·SIGINT·SIGTERM 정리 기대 5·실제 5. 실제 키 대신 무효 표본을 쓰며 실제 모델 호출은 0이다.
  음성 대조: `m 구조-04 --negative`의 exit 0 사본은 인증 소비 기록·실패 종료가 없어 FAIL이다. 대조 표본의 잘못된 644 권한과 남은 사본도 같은 검사로 검출한다.

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가 (측정: `python3 scripts/validate-plugin.py --check=code-fence`, `m 금지-03`) [exact]
  측정: W를 읽어 푼 사본에서 설정의 명령을 그대로 실행하여 V6 실행 표식·종료 0을 요구한다.
  양성 대조: `m 금지-03 --controls-only`; 같은 사본의 스킬 끝에 bare fence를 넣고 같은 V6에서 대상 파일 FAIL 1 이상을 확인한다. 알려진 답: 위반 파일 하나 검출 여부 기대 1·실제 1.
  음성 대조: `m 금지-03 --negative`는 같은 위반을 남겨 본 측정이 FAIL이어야 한다.
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL (측정: `python3 scripts/validate-plugin.py --check=frontmatter`, `m 금지-04`) [exact]
  측정: 사본에서 설정의 명령을 그대로 실행하여 V1 실행 표식·종료 0을 요구한다.
  양성 대조: `m 금지-04 --controls-only`; 스킬의 name을 하나 지운 사본에 같은 V1을 돌려 대상 파일 FAIL 1 이상. 알려진 답: 위반 파일 하나 검출 여부 기대 1·실제 1.
  음성 대조: `m 금지-04 --negative`는 필드 삭제를 남겨 본 측정이 FAIL이어야 한다.

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 공개 플러그인 스크립트와 템플릿을 배포하고 두 문서가 같은 codex-audit.sh 명령을 사용한다 (측정: `m 재사용-01`) [structural, enumerated]
  측정: `harness/scripts/codex-audit.sh`, `harness/templates/codex-audit/`, `harness/skills/sprint-contract/SKILL.md`, `harness/agents/qa-evaluator.md`를 각각 확인한다.
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 기존 qa-pending-check.sh가 스크립트의 피드백을 읽고 기존 qa-evaluator.md의 status 전환 절차가 그대로 소비한다 (측정: `m 재사용-02`) [exact, enumerated]
  측정: 스킬-02의 실제 소비 시험을 다시 사용한다. 새 상태 전환/대기 훅을 요구하지 않는다.
  음성 대조: `m 재사용-02 --negative`의 no-op 감독은 실제 피드백을 만들지 않아 FAIL이다.

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze = bash -n scripts/release.sh 는 이번 범위 밖 scripts/release.sh만 검사한다; 측정: `m 진단-01`의 기준~상한 변경 경로와의 교집합 0) [exact]
  양성 대조: `m 진단-01 --controls-only`는 scripts/release.sh 한 경로를 같은 교집합 검사에 넣어 positive_control=1. 알려진 답: 한 경로→1.
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 새 셸 스크립트의 bash·zsh 구문 검사와 shellcheck 진단이 0이며 검사 자체가 성공한다 (측정: `m 진단-02`) [exact]
  측정: 두 셸의 -n과 shellcheck -f gcc를 직접 실행하고 종료 코드·진단 출력을 함께 확인한다. 문서의 구조 진단은 금지-03·04, 설정 칸은 구조-03이 맡는다.
  양성 대조: `m 진단-02 --controls-only`의 if then 셸을 같은 bash -n·zsh -n·shellcheck로 재서 positive_control=3. 알려진 답: 깨진 스크립트에 대한 세 검사 실패→3.
  음성 대조: `m 진단-02 --negative`의 구문 파괴 사본은 FAIL이다.
- [ ] 진단-03: N/A (commands.test = bash scripts/release.sh 2>&1 || true 는 이번 범위 밖 scripts/release.sh만 실행한다; 측정: `m 진단-03`의 기준~상한 변경 경로와의 교집합 0) [exact]
  양성 대조: `m 진단-03 --controls-only`에 대상 한 경로를 넣어 positive_control=1. 알려진 답: 한 경로→1. 대신 실제 새 명령 실행은 Script·Error 조건이 맡는다.
- [ ] 진단-04: 실제 앱/서버 구동 시 에러 0개 — 이번 산출물의 실행 진입점인 codex-audit.sh를 가짜 CODEX_BIN으로 실제 기동하면 유효 전체 PASS에서 정상 종료·피드백을 낸다 (측정: `m 진단-04`) [exact]
  측정: 스크립트-03과 같은 실제 셸 실행을 재사용한다. 실제 Codex 서비스 접속 시험으로 오인하지 않는다.
  양성 대조: `m 진단-04 --controls-only`의 호출 기록 계수 positive_control=2. 알려진 답: exec 두 행→2.
  음성 대조: `m 진단-04 --negative`의 no-op 명령은 파일 생성 검사가 FAIL이다.

## 범위 경계

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/templates/codex-audit/
harness/templates/project.yaml
harness/skills/sprint-contract/SKILL.md
harness/agents/qa-evaluator.md
harness/README.md
```

2026-10-06 쓰기 경계: 원래 감독 설정·인증·세션 폴더는 읽기만 한다. 스크립트-11은 측정 폴더 안에 설정·인증 사본과 새 세션을 만들고 인증 사본은 끝에 삭제한다. 레포 W도 읽기 전용이다. 측정 소스의 셸 삭제 명령 유무를 검사하며 시험 사본 정리에는 Python을 사용한다.

`.harness/` 산출물과 프로젝트 설정은 규칙상 자동 허용한다. 이번 작성자의 쓰기 범위는 이 목록이 아니라 사용자 지정 out 계약·out/measure뿐이다. 이 블록은 다음 구현자의 범위를 정한다.

요구사항 §1 사용자 결정 대응: 1→스크립트-04·06, 2→스킬-02, 3→스크립트-05·구조-02, 4→스크립트-06·스킬-01, 5→스크립트-04, 6→스크립트-04·오류-01, 7→스크립트-08·11, 8→스크립트-07, 9→스킬-01·02, 10→스크립트-07·스킬-01·02, 11→스크립트-08·11·구조-04. 결정 11의 SIGKILL·전원 단절 한계는 아래에 명시하며, 그 밖에 조건으로 덮이지 않은 사용자 결정은 없다.

§4 대응: draft→스크립트-01, revise→02, impl/피드백 생산→03, 재심→04, 조사→05, 회차/지난 지적→06, 설정→07, 보고서→08, detach/wait/종료 코드→09, 네 호출의 틀/응답→10, 네 호출의 형식 오류/나머지 실패 갈래·한도→오류-01·02, 격리/파일 인증 수명/시험 환경변수→구조-02·04·스크립트-08·11·오류-02, 새 프로젝트 틀/README→구조-03, 스킬/평가자/기존 훅 소비→스킬-01·02. 관찰 가능한 동작을 제외하여 조건 수를 줄인 항목은 없다.

§2 추가 대응: 역할 부여 금지·프롬프트 크기·풀이 예시 제한→구조-02, 운영 전 실제 감독관의 좋은/나쁜 예 판정과 세션 모델·생각 강도→스크립트-11. 기능 조건은 19개로 상한 20 이하이며 지적 때문에 제외한 요구사항은 없다.

제외: harness 버전 올리기·배포·push, 레포 밖 codex-research 변경, 기록 수집 훅 변경, Gemini. 금지-01(hardcoded.*version)은 버전 산출물이 없고 구조-01이 버전 파일 불변을 잰다. 금지-02(git push.*--force)는 이번 작업에 push가 없어 선택하지 않았다. 금지-03·04 두 개를 선택했다.

중단 범위 제외: SIGKILL·전원 단절은 프로세스가 정리 코드를 실행할 기회가 없어 즉시 인증 사본 삭제를 실증할 수 없다. 결정 11의 중단 경로는 처리 가능한 SIGINT·SIGTERM으로 계약하며 이 한계는 사용자 판단 대상이다. 그 외 사용자 결정의 미대응 항목은 없다.

커버리지 해소: 스킬-02 — 조건 문장의 `harness/agents/qa-evaluator.md` · `harness/scripts/qa-pending-check.sh` 를 `m 스킬-02` 가 코드로 직접 읽고 훅에 실제 입력을 넣는다(측정 줄에 경로를 다시 적지 않았을 뿐, 2026-10-06 3 회차 계약 검토에서 확인). 구조-03 — `harness/templates/project.yaml` · `harness/templates/codex-audit/` · `harness/README.md` 를 `m 구조-03` 이 각각 읽는다(같은 검토에서 확인). 이 두 줄은 봉인 전 부모(Claude)가 검토 참고를 옮겨 적은 서술이며 조건 줄은 바꾸지 않았다.

남는 측정 한계: fake는 실제 codex binary/바로가기를 건드리지 않으며 CLI 인자와 기록·산출물만 관찰한다. 실제 샌드박스 탈출 저항·원본 쓰기 차단의 OS 실효성은 별도 실측이 필요하다. 실제 모델의 좋은/나쁜 예 판정은 스크립트-11이 운영 전에 실측하도록 요구한다. 작은 두 예제의 성공을 일반적인 판정 정확도로 확대하지 않는다. 문서의 의미와 충돌 여부는 Claude 평가자가 확인한다. 이를 자동 PASS나 실제 실행 증거로 취급하지 않는다.

## 회귀 게이트

`m <번호> [옵션]`은 W 맨 위에서 `bash .harness/.meta/codex-supervisor/measure/measure.sh <번호> [옵션]`이다. out/measure 폴더를 meta/codex-supervisor 아래에 그대로 옮긴다. measure 폴더의 내용만 meta 폴더에 놓는 배치도 가능하고 그때 명령에서 measure/만 뺀다. 초안 위치에서는 `bash ./out/measure/measure.sh <번호>`로 같다. cwd가 W가 아니면 환경변수 MEASURE_W 또는 이 문서의 W를 읽는다. 모든 판정은 해석한 가지 상한의 커밋 파일을 대상으로 하며 미커밋 구현은 평가하지 않는다.

준비물은 Python 3.11 이상과 기존 검증기가 요구하는 PyYAML, git, tar, bash, zsh, shellcheck와 레포의 기존 검증기다. pip/npm 설치는 하지 않으며 스크립트-11의 일반 실행만 실제 Codex 서비스에 접속한다. 도구 없음은 FAIL이다. 스크립트와 fake는 해석기가 고정되어 있고 셸 진입점은 bash·zsh 모두 같은 인자 집합을 Python에 넘긴다. out/measure/.runs/<조건>-<임의값>/에는 복사본·임시 git·fake 호출 로그·stdout/stderr·evidence.json을 남긴다. 결과 파일은 재실행할 때 덮지 않는다. 일반 측정은 최종 줄 PASS/FAIL <번호>와 checks/failures, 종료 0/1로 판정한다. 실제 호출의 사전 로그인 전제 불성립은 별도 PRECONDITION_UNMET·종료 2이며 구현 판정 결과에 섞지 않는다. --prepare-only의 PASS는 준비 성공이지 구현 PASS가 아니다. 잘못된 조건 번호는 FAIL usage와 64다. controls-only의 PASS는 구현 PASS가 아니라 대조 준비 성공이다.

음성 대조는 소스 사본만 무력화하며 W는 쓰지 않는다. 셸 스크립트의 본체를 exit 0만 남기는 대조는 기능이 없는 명령이 테스트를 통과하지 못함을 확인한다. 문서·V1·V6·구문 진단은 각각 실제로 검사하는 입력을 삭제/파괴한다. 실제 구현이 없을 때 음성 대조가 성공 구현에서 변이를 잡았다고 주장하지 않는다.

봉인 전 baseline: 상한 88b2a84ee6baed14fd67841af17242e5c09f58ba, BASE 대비 `.harness` 밖 diff는 빈 출력·종료 0. W에는 계약/요구사항 meta의 미추적 파일만 있고 구현 스크립트가 없다. 구현을 요구하는 조건은 MISSING 또는 문서/설정 누락으로 FAIL이어야 한다. 범위 검사는 공허한 포함 통과를 막으려고 비어 있지 않은 구현 차이도 요구한다. 진단-01·03의 N/A, 기존 V1·V6 회귀 검사는 구현 전에도 PASS일 수 있다.
