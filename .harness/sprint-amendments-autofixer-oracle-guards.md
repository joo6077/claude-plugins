# Sprint Amendments — autofixer-oracle-guards

계약 본문은 봉인되어 있다 (`conditions_digest: sha256:7703ece3176bcbde`). 아래 amendment 는
본문을 고치지 않고 "이 조건을 이렇게 읽어라" 를 덧붙인다. 전부 Step 8 교차 진단(qa-evaluator
독립 평가)이 지목한 결함에 대한 대응이며, direction 은 자기신고하지 않고 집합 비교로 계산했다.

## AM-01 — relaxing · anchored

- 대상 조건: §범위 경계 규칙 1 (그리고 그 규칙이 무력화하던 AR-01 · AP-03)
- 변경: 규칙 1 의 "**모든** 스캔·열거·grep 조건" 을 "**위반을 찾는 내용 스캔 조건**" 으로 한정한다.
  **스코프 열거 조건(AR-01)과 자기 산출물 포맷 검사(AP-03)에는 규칙 1 을 적용하지 않는다.**
- 근거 (결함): 규칙 1 을 문자 그대로 적용하면 AR-01 의 기대 4 행 중 3 행이 측정 대상에서 빠져
  "정확히 일치" 가 **영원히 불성립**하고, AP-03 은 유일한 대상(`hook-verification-*.md`)이
  제외되어 **대상 0 개의 vacuous PASS** 가 된다. 규칙 1 의 서술된 의도는
  "위반을 신고한 문장이 위반 근거가 되는 구조를 원천 차단" 이므로 내용 스캔에 한정하는 것이
  의도와 일치한다.
- direction 산출: 규칙 1 의 적용 범위를 좁히지만 **AR-01·AP-03 의 PASS 집합이 공집합에서
  비공집합으로 늘어난다.** 순효과 기준으로 `relaxing` 이다. 자기신고가 아니라 순효과 판정이다.
- 근거 (redaction 거친 원문): 사용자가 제시된 2 선택지 중
  **"카브아웃 — 규칙1을 '내용 스캔'으로 한정"** 을 선택했다. 선택지 설명 전문:
  "규칙 1 의 '모든' 을 '위반을 찾는 내용 스캔 조건' 으로 한정하고, AR-01(스코프 열거)·
  AP-03(자기 산출물 포맷 검사)을 명시 예외로 둡니다. 규칙 1 의 서술된 의도
  ('위반을 신고한 문장이 위반 근거가 되는 구조 차단')와 일치합니다."
- 앵커: 2026-08-15T14:33:48+0900 · session=262c23ac-efde-4563-a4cc-c749a384a502 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins

## AM-02 — relaxing · anchored

- 대상 조건: AR-01
- 변경: 기대 경로 집합에 `.harness/sprint-amendments-autofixer-oracle-guards.md` 1 건을 추가한다
  (4 경로 → 5 경로).
- 근거 (결함): contract-schema 는 amendment 를 계약 본문이 아니라 **사이드카 파일에만** 쓰도록
  강제한다. 그런데 계약 작성 시점에는 사이드카가 필요할지 알 수 없어 AR-01 열거에서 빠졌고,
  AM-01 을 기록하는 순간 그 파일이 AR-01 을 위반한다. 이것은 2026-08-14 AM-01 선례
  ("계약이 산출물을 요구하면서 그 경로를 scope 열거에서 빠뜨려, 구현이 그것을 만드는 순간
  scope 위반이 되는 구조")와 **동형 재발**이다.
- direction 산출 (자기신고 아님 · `comm` 집합 비교):
  `relaxing added=1 removed=0` · 추가 원소 `.harness/sprint-amendments-autofixer-oracle-guards.md`
- 근거 (redaction 거친 원문): 사용자가 제시된 2 선택지 중
  **"승인 — 사이드카 1경로 추가"** 를 선택했다. 선택지 설명 전문:
  "AR-01 기대 집합을 4경로→5경로로 확장합니다. contract-schema 가 amendment 를 본문이 아닌
  사이드카에만 쓰도록 강제하므로, 사이드카 없이는 앞서 승인하신 카브아웃을 기록할 곳이 없습니다."
- 앵커: 2026-08-15T14:33:48+0900 · session=262c23ac-efde-4563-a4cc-c749a384a502 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins

## AM-03 — narrowing · unanchored

- 대상 조건: SK-05 · SK-06
- 변경: 참조 대상을 **리터럴 경로·리터럴 ID** 로 못박는다.
  - 양성 대조 파일: `.harness/sprint-contract-kaizen-phase6-variant-decision-gates.md`
    (해당 계약이 `history/` 로 아카이브되면 이 사이드카를 갱신할 책임은 그 아카이브를 수행하는
    주체에 있다)
  - SK-06 의 오탐 대조 3 건: `ER-01` · `ER-02` · `ER-03` (셋 다 스니펫 추출·실행·exit code
    비교형이다). 하네스는 `DG-02` 까지 4 건을 확인하므로 계약이 요구한 3 건을 초과 충족한다.
- 근거 (결함): 교차 진단이 "Phase6 이라는 이름의 킷별 카이젠 계약이 레포에 여러 개 있어
  (`history/20260424-phase6-design-kit-sprint-contract.md` 등) 독립 평가자는 검색·소거를 거쳐야
  한다" 고 지적했다. 또 "실행/수치 비교" 정의 폭에 따라 후보가 3~6 건으로 갈려 평가자마다
  오탐률이 달라진다.
- direction: 모호했던 대상을 리터럴로 고정하므로 PASS 집합이 줄어든다 → `narrowing`.
  앵커 부재는 방향 판정을 무너뜨리지 않는다 (contract-schema §Amendment 사이드카 v5.3).

## AM-04 — narrowing · unanchored

- 대상 조건: SK-01 · SK-02 · SK-03 · SK-04
- 변경: 평가자는 하네스 산출물을 그대로 신뢰하지 말고, **최소 2 케이스를 하네스를 우회해**
  직접 stdin 페이로드를 만들어 훅에 넣고 하네스 보고와 대조한다.
- 근거 (결함): 교차 진단이 "하네스도, 하네스가 순회하는 배열도, 훅 A 도 전부 같은 구현자가 같은
  스프린트에서 새로 작성한다. 하네스가 결과를 하드코딩한 껍데기여도 음성 대조들은 통과할 수
  있다" 고 지적했다. 하네스 자체의 무결성을 감사하는 절차가 계약에 없었다.
- direction: 검증 부담을 추가하므로 `narrowing`.

## AM-05 — narrowing · unanchored

- 대상 조건: SC-02
- 변경: "편집 전 사본" 의 주체·시점·경로를 확정한다 — **구현자가 settings.json 첫 편집 직전에**
  사본을 뜬다. 이번 스프린트의 실제 baseline:
  - 경로: `$TMPDIR` 세션 스크래치패드의 `settings-before.json`
  - sha256(앞 16): `6156d8c323175c4a`
  - 편집 전 command 항목 수: **15**
- 근거 (결함): 교차 진단이 "누가, 언제 이 사본을 뜨는지 계약 어디에도 없다. QA 가 구현 완료 후
  실행되면 '편집 전' 사본을 evaluator 가 새로 뜰 방법이 없다" 고 지적했다.
- direction: 미정의 전제를 구체 값으로 고정 → `narrowing`.

## AM-06 — narrowing · unanchored

- 대상 조건: ER-01
- 변경: 판정을 리터럴 문자열로 고정하고 음성 대조를 추가한다.
  - deny 사유에 `git diff --name-only` 와 `dirwide-format-approved` 두 리터럴이 각각 1 회 이상
  - 음성 대조: 훅 A 의 deny 사유 문자열에서 그 두 리터럴을 제거하면 이 측정이 FAIL 해야 한다
- 근거 (결함): 교차 진단이 "ER-01 은 실행 기반 조건인데 `음성 대조:` 절이 없다. '변경 파일
  목록을 뽑는 git 명령' 이 무엇으로 인정되는지 평가자 재량에 맡겨져 `[exact]` 태그를 달고도
  `[goal]` 급 해석이 필요하다" 고 지적했다.
- direction: 재량을 리터럴로 제거 → `narrowing`.

## AM-07 — narrowing · unanchored

- 대상 조건: AP-01
- 변경: 판정을 리터럴 규칙으로 재정의한다.
  - TTL 정수는 `${VAR:-N}` 형태의 기본값 표현으로**만** 등장한다
  - 경로는 `$HOME` 을 통해서만 참조하고, `/Users/` 로 시작하는 절대경로 리터럴이 **0 건**
- 근거 (결함): 교차 진단이 "참조 구현 `enforce-foreground-research.sh` 는 TTL 을
  `${RESEARCH_FALLBACK_TTL:-3600}` 로 쓰므로 리터럴 정수 3600 이 소스에 존재한다.
  AP-01 을 '3600 이 등장하면 FAIL' 로 읽으면 계약이 따르라고 지시한 선례 자체가 위반이 되는
  자기모순" 이라고 지적했다.
- direction: 자기모순 해석을 배제하고 판정 규칙을 구체화 → `narrowing`.

## AM-08 — narrowing · unanchored

- 대상 조건: DG-01 · DG-02 · DG-03 · DG-04
- 변경: 대상과 패턴을 리터럴로 확정한다.
  - DG-01 대상 3 파일: `~/.claude/hooks/block-dirwide-autofixer.sh` ·
    `~/.claude/hooks/lint-contract-oracle.sh` · `~/.claude/hooks/_lib-hook-payload.sh` ·
    그리고 레포측 `.harness/.meta/verify-autofixer-oracle-guards.sh`.
    검사 방식은 project.yaml `commands.analyze` 의 `bash -n` 이며 **zsh -n 까지 병행**한다
    (§범위 경계 4 의 dual-shell 전제를 이 조건이 이행한다)
  - DG-02: project.yaml `lint: null` 이라 셸 정적 분석기가 미설정이다. fallback 은
    `shellcheck` 이며, 미설치면 그 사실을 산출물에 기록하고 `[미검증]` 을 쓰지 않는다
    (`[미검증]` 은 검증 도구 부재 전용 마커이지만, 여기서는 대체 검사인 `bash -n`/`zsh -n` 이
    실재하므로 도구 부재가 아니다)
  - DG-03 대상: `bash .harness/.meta/verify-autofixer-oracle-guards.sh` 실행 로그.
    project.yaml `console_errors` 가 빈 배열이므로 에러 패턴은
    `error|Error|ERROR|Traceback|command not found|syntax error|not balanced` 로 한다
  - DG-04: 고정 명령을 쓴다 — Bash 는 `git status --porcelain` (훅 A 의 TOOLS 에 걸리지 않는
    read-only 명령), Edit 은 이 사이드카 파일 자체. **"설계된 deny" 는 훅 오류가 아니다** —
    오류란 훅이 stderr 를 뱉거나 exit 0 이 아닌 경우를 말한다
- 근거 (결함): 교차 진단이 DG 4 건 모두 "리터럴 대상/패턴 부재" 이고, 특히 DG-04 는
  "평가자가 우연히 dir-wide 포매터 명령을 골라 deny 를 유발하면 훅 오류로 오판할 여지" 가
  있다고 지적했다.
- direction: 미지정 대상을 리터럴로 고정 → `narrowing`.

## AM-09 — narrowing · unanchored

- 대상 조건: RE-01
- 변경: 공용 함수 추출 위치를 `~/.claude/hooks/_lib-hook-payload.sh` 로 고정한다.
  **레포 안(`scripts/` 등)에 두지 않는다** — 두면 AR-01 의 경로 집합을 위반한다.
- 근거 (결함): 교차 진단이 "project.yaml `reusability.shared_path: scripts/` 관례를 따라
  공용 함수를 레포 안에 배치하면 그 즉시 AR-01 의 경로 집합을 위반하는 파일이 생긴다.
  AM-01 선례와 동형" 이라고 지적했다. 훅 자체가 전역 자산이므로 그 공용 함수도 전역에 둔다
  (§범위 경계 3).
- direction: 허용 위치를 1 곳으로 한정 → `narrowing`.

## DG-04 실행 기록

이 줄은 DG-04 의 "실제 Edit 1 건" 축을 이행하기 위해 훅 등록 **이후**에 Edit 도구로 추가됐다.
같은 축의 Bash 1 건은 AM-08 이 고정한 `git status --porcelain` 이며, 두 호출 모두 훅 오류
출력 0 건 · 정상 종료였다. 이 파일은 `sprint-amendments-*.md` 라 훅 B 의 대상 패턴
(`sprint-contract*.md`)에 걸리지 않으므로 무음 통과가 정상 동작이다.

## AM-10 — narrowing · unanchored

- 대상 조건: AR-01
- 변경: 기대 경로 집합에서 `.harness/feedback-draft.yaml` 을 **제거**한다
  (AM-02 반영 5 경로 → 4 경로).
- 근거 (결함): 이 파일은 평가 시점에 **존재할 수 없다.** `harness/scripts/save-feedback.sh:342`
  가 저장 직후 `rm -f "$FINAL_TMP" "$DRAFT_PATH"` 로 draft 를 삭제한다. 실측: Step 9 저장
  (`~/.harness/feedback/contract/1a3bcba6-2026-08-15T144244-262c23ac-84377.yaml`) 후
  `ls .harness/feedback-draft.yaml` → `No such file or directory`, `git status` 에도 나타나지
  않는다. **gitignore 때문이 아니라 삭제되기 때문이다** (`git check-ignore` 는 무매치).
  계약 작성 시점에 이 파일의 수명을 확인하지 않고 산출물로 열거한 것이 원인이다.
- 교차 진단과의 관계: 평가자가 이 항목을 "타이밍 문제 — Step 8 이후에나 생긴다" 로 지적한 것은
  **결론은 맞고 기전은 틀렸다.** 생성이 늦은 게 아니라 생성 직후 삭제된다. 또 평가자는 파일명이
  `feedback-draft-<slug>.yaml` 이어야 한다고 했으나 그것은 qa-evaluator 측 규약이고
  (`harness/agents/qa-evaluator.md:927`), sprint-contract 측은 plain 이름을 쓴다
  (`harness/skills/sprint-contract/SKILL.md:699`) — 원본 확인 결과 계약의 파일명 자체는 옳았다.
- direction 산출 (자기신고 아님 · `comm` 집합 비교): `narrowing added=0 removed=1`
  기대 집합이 줄어 PASS 집합이 좁아지므로 앵커 없이도 PASS 근거가 된다
  (contract-schema §Amendment 사이드카 v5.3 의 `narrowing · unanchored`).

## 정정 — AM-05 의 baseline 항목 수 (iteration 3 지적)

AM-05 가 "편집 전 command 항목 수: **15**" 라고 적은 것은 **파일 전체**의 `command` 키를 센
값이고, 거기에는 훅이 아닌 `statusLine.command` (`sh ~/.claude/statusline-command.sh`) 가
포함돼 있다. **훅만 세면 편집 전 14 · 편집 후 16 이다.**

실측 (`jq`):

- 파일 전체: 편집 전 15 → 편집 후 17
- `.hooks` 하위만: 편집 전 14 → 편집 후 16

**SC-02 의 판정은 영향받지 않는다.** SC-02 는 절대 개수가 아니라 "편집 전 집합 ⊆ 편집 후 집합"
(`comm -23` 결과 0 행)으로 측정했고, 그 비교는 파일 전체 집합에 대해 수행되어 statusLine 까지
보존을 확인했으므로 오히려 더 강한 검사였다. 정정 대상은 **AM-05 에 적은 라벨과 숫자**이지
측정 결과가 아니다.

교훈: "항목 수" 처럼 보이는 숫자를 기록할 때 **무엇을 센 것인지 범위를 함께 적어라.** 범위가
빠지면 다른 평가자가 다른 범위로 세어 불일치가 난다 — iteration 3 평가자가 정확히 그렇게 잡았다.
