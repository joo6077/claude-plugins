---
feature: "훅 2종 — dir-wide autofixer 차단 + 계약 오라클 린터"
slug: autofixer-oracle-guards
created: "2026-08-15 11:30"
complexity: "중간"
conditions: 21
status: done
owner_session: 262c23ac-efde-4563-a4cc-c749a384a502
conditions_digest: sha256:7703ece3176bcbde
locked_at: "2026-08-15 13:43"
---

## 배경

메모리 `feedback_no_dirwide_autofixer` (110 개 중 102 개 무관 파일 오염) 와
`feedback_oracle_must_execute_not_grep` (25 조건 전부 PASS 인데 기능 파손) 을 기계화한다.
근거 문서는 `docs/superpowers/followup-kaizen-memory-integration.md` §훅 승격 후보 이며,
그 표가 지목한 2 건만 대상이다. `feedback_codex_orthodox_hook_not_empire` 가 "자동화는 훅이,
의식은 규칙 슬림화로. 카이젠 제국 금지" 라고 못박고 있으므로 후보를 늘리지 않는다.

배치는 사용자 결정으로 `~/.claude/hooks/` 전역이다. 플러그인 캐시가 레포의 복사본이라
(inode 71950291 vs 2227295) `harness/hooks/` 편집은 release + 재설치 전까지 발효되지 않는 반면,
전역 훅은 즉시 발효하고 `.harness/` 계약을 가진 13 개 프로젝트 전부를 덮는다.

훅 출력 스키마는 배포 바이너리 v2.1.232 에 임베드된 문서에서 확인했다 —
`permissionDecision` / `permissionDecisionReason` 은 PreToolUse 전용이고,
PostToolUse 는 `hookSpecificOutput.{hookEventName, additionalContext}` 를 쓴다.

## 범위 경계

공통 전제는 조건마다 반복하지 않고 여기서 1 회 선언한다. 조건 단위로 관리하면 반드시 하나를
빠뜨린다 (Final v2 가 ER-02 · DG-02 에만 카브아웃을 넣고 ER-01 에 빠뜨린 실측 사례).

1. **자기 산출물 제외** — 이 스프린트의 산출물 5 종은 **모든** 스캔 · 열거 · grep 조건의 대상에서
   제외한다: 이 계약 파일, `sprint-feedback-autofixer-oracle-guards.md`,
   `sprint-amendments-autofixer-oracle-guards.md`,
   `.harness/.meta/hook-verification-autofixer-oracle-guards.md`, `.harness/feedback-draft.yaml`.
   위반을 신고한 문장이 위반 근거가 되는 구조를 원천 차단한다.
2. **상태 전제** — 모든 git 기반 측정의 Given 은 "커밋 직전 working tree" 다 (HEAD 대비,
   untracked 포함). 작성 시점 baseline: `git diff --name-only HEAD` 빈 출력,
   untracked 는 이 계약 파일 1 건.
3. **전역 자산은 git 밖** — 훅 2 종과 전역 settings 는 이 레포가 추적하지 않는다. diff 가 아니라
   파일시스템 검사로 측정한다. AR-01 의 경로 집합에 이들이 없는 것은 누락이 아니다.
4. **셸 이식성** — 모든 측정 명령은 zsh 와 bash 양쪽에서 실행하고 두 출력이 일치해야 한다.
   파일 열거는 글로빙 대신 find 를 쓴다.
5. **`commands.test` 대체** — project.yaml 의 `commands.test` 는 release 스크립트라 tag/push
   부작용이 있다. contract-schema §측정 명령 타당성 이 부작용 명령을 측정에 쓰지 말라고 규정하므로
   DG-03 은 검증 하네스 실행으로 대체한다.
6. **인자 생략 차단의 의도적 과포함** — 사용자 결정으로 훅 A 는 디렉토리 인자와 인자 생략을 모두
   막는다. 일부 도구는 인자 생략이 무해하지만 (stdin 모드 등) 판정을 도구별로 분기하지 않는다.
   `cargo fmt` 무인자가 워크스페이스 전체를 포맷하는 것이 차단 근거이며, 일괄 처리는
   센티넬 승인으로 우회 가능하다.

## Skill

- [ ] SK-01: 훅 A 가 write-mode 포매터와 광역 인자의 곱 중 해당 셀만 deny 한다 [exact, enumerated]
      (축: mode 2 값 · argshape 3 값 · tool 14 값, 값의 출처는 검증 하네스의 `MODES` ·
       `ARGSHAPES` · `TOOLS` 배열이고 하네스가 그 배열을 순회해 케이스를 생성한다 ·
       cases_total: 세 배열 길이의 곱을 명령으로 산출한 값 ·
       측정: 하네스가 tool 14 종 `fix-markdown-lint.py` `validate-plugin.py` `prettier` `black`
       `ruff` `eslint` `dart` `cargo` `gofmt` `shfmt` `isort` `clang-format` `stylua` `autopep8` 를
       mode `write` `check` 와 argshape `dir` `omitted` `file` 에 곱해 각 케이스를 stdin 페이로드로
       훅에 넣고 permissionDecision 을 수집, `mode=write` 이면서 argshape 가 `dir` 또는 `omitted`
       인 셀만 deny 이고 나머지 전 셀이 무출력임을 확인 ·
       음성 대조: 훅의 deny 분기를 제거하면 deny 수가 0 이 되어 이 측정이 FAIL 해야 한다)
- [ ] SK-02: 훅 A 가 read-only 모드를 한 건도 deny 하지 않는다 [exact, enumerated]
      (측정: SK-01 하네스의 mode 축이 `check` 인 전 셀이 무출력. check 모드 플래그는
       `--check` `--dry-run` `--diff` `-l` `--check-only` `--output=none` 6 종을 도구별로 매핑 ·
       음성 대조: mode 축 판정을 제거하면 이 셀들이 deny 로 뒤집혀 FAIL 해야 한다)
- [ ] SK-03: 훅 A 가 포매터 이름을 명령 위치에서만 인식한다 [exact, enumerated]
      (오탐 대조 입력 4 건: git log 의 grep 인자로 포매터명이 등장하는 명령 · echo 문자열 안에
       포매터명이 등장하는 명령 · 포매터 스크립트를 cat 하는 명령 · rg 검색어로 포매터명이
       등장하는 명령 ·
       측정: 4 건 전부 무출력. 판정 앵커는 줄 시작 또는 셸 구분자 직후로 한정한다 ·
       음성 대조: 앵커를 제거하면 이 4 건이 deny 로 잡혀 FAIL 해야 한다)
- [ ] SK-04: 훅 A 센티넬 게이트가 4 축을 만족한다 [exact, enumerated]
      (센티넬 파일은 홈 아래 dirwide-format 승인 파일이고 TTL 기본 3600 초, 환경변수로 조정 ·
       측정: 4 축을 순서대로 실행 — 센티넬 없음이면 deny · epoch 에서 7200 초 뺀 값을 기록한
       만료 상태면 deny · 현재 epoch 을 기록한 유효 상태면 무출력 · 유효 상태에서도 SK-03 의
       오탐 4 건이 여전히 무출력 ·
       음성 대조: TTL 비교를 제거하면 만료 축이 통과로 뒤집혀 FAIL 해야 한다)
- [ ] SK-05: 훅 B 가 산문 존재 grep 오라클을 검출한다 [exact]
      (양성 대조는 Phase6 계약의 AR-03 이다 — 측정절이 한글 산문 한 구절을 grep 대상으로 삼아
       문서에 그 문장이 있는지만 본다 ·
       측정: 그 계약 파일을 file_path 로 하는 PostToolUse 페이로드를 훅에 넣고 출력
       additionalContext 에 조건 ID `AR-03` 이 포함됨을 확인 ·
       음성 대조: 산문 판정 분기를 제거하면 `AR-03` 이 출력에서 사라져 FAIL 해야 한다)
- [ ] SK-06: 훅 B 가 실행형 측정 조건을 검출하지 않고 기존 계약 전체 검출률을 산출물에 기록한다 [exact]
      (오탐 대조: 같은 Phase6 계약에서 명령 실행과 수치 비교로 판정하는 조건 3 건을 지목해
       미검출 확인 ·
       측정: 자기 산출물을 제외한 기존 계약 전부를 훅에 순회 입력해 검출 조건 수와 전체 조건 수를
       `.harness/.meta/hook-verification-autofixer-oracle-guards.md` 에 기록. 검출률 임계를 FAIL
       기준으로 삼지 않는다 — contract-schema §측정 커버리지 검출기 와 동일하게 검출기이지
       게이트가 아니다 ·
       음성 대조: 실행 신호 판정을 제거하면 오탐 대조 3 건이 검출되어 FAIL 해야 한다)
- [ ] SK-07: 훅 B 는 어떤 입력에도 차단 신호를 내지 않는다 [exact]
      (측정: SK-05 와 SK-06 의 전 케이스 출력에서 permissionDecision 키 · block 결정 ·
       continue false 가 각각 0 건이고 모든 케이스가 exit 0 ·
       근거: PostToolUse 는 permissionDecision 을 지원하지 않는다 — 배포 바이너리 v2.1.232 의
       임베디드 훅 문서가 그 필드를 PreToolUse 전용으로 명시한다)

## Script

- [ ] SC-01: 전역 settings 에 훅 A 가 PreToolUse 의 Bash matcher 로, 훅 B 가 PostToolUse 의
      Edit 또는 Write matcher 로 등록되고 파일이 유효 JSON 이다 [exact, enumerated]
      (측정: jq 로 파싱이 성공하고, 두 훅 스크립트의 경로 문자열이 각각 해당 이벤트 배열 안의
       command 값에 존재)
- [ ] SC-02: 기존 훅 등록이 한 건도 소실되지 않는다 [exact, enumerated]
      (Given: 편집 전 전역 settings 사본을 레포 밖 임시 경로에 확보한 상태 ·
       측정: 편집 전후 파일에서 command 값 전체를 jq 로 추출해 정렬한 뒤, 편집 전 집합이 편집 후
       집합의 부분집합임을 comm 으로 확인해 편집 전에만 있는 행이 0 건 ·
       음성 대조: 기존 항목 하나를 지우면 comm 결과가 1 행이 되어 FAIL 해야 한다)

## Error

- [ ] ER-01: 훅 A 의 deny 사유에 대체 경로가 포함된다 [exact]
      (측정: deny 출력의 permissionDecisionReason 에 변경 파일 목록을 뽑는 git 명령과 센티넬
       승인 절차가 각각 1 회 이상 등장 ·
       근거: memory feedback_no_dirwide_autofixer 의 How to apply 가 지정한 대체 경로가
       변경 파일만 개별 인자로 넘기는 것이다)
- [ ] ER-02: 두 훅 모두 fail-open 이다 [exact, enumerated]
      (측정: 3 케이스를 각 훅에 실행 — jq 를 찾을 수 없는 PATH 상태 · 빈 stdin · 깨진 JSON stdin.
       6 회 실행 전부 exit 0 이고 deny 를 내지 않음 ·
       음성 대조: 스크립트에 errexit 를 넣으면 빈 stdin 과 깨진 JSON 축이 비정상 종료해
       FAIL 해야 한다)

## Architecture

- [ ] AR-01: 이 레포의 변경이 정확히 4 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: git status 포슬린 출력을 레포 루트로 한정하고 QA 산출물 경로를 제외한 결과의 경로
       집합이 `.harness/sprint-contract-autofixer-oracle-guards.md` ·
       `.harness/.meta/hook-verification-autofixer-oracle-guards.md` ·
       `.harness/.meta/verify-autofixer-oracle-guards.sh` · `.harness/feedback-draft.yaml`
       4 행과 정확히 일치)
- [ ] AR-02: 훅 2 종이 홈 훅 디렉토리에 실행 권한과 함께 존재한다 [exact, enumerated]
      (측정: `block-dirwide-autofixer.sh` 와 `lint-contract-oracle.sh` 2 파일이 실행 가능 검사를
       통과. 네이밍은 기존 `enforce-foreground-research.sh` 의 동사-목적어 형태를 따른다)

## Anti-patterns

- [ ] AP-01: 훅이 TTL 과 경로를 하드코딩하지 않는다 — 센티넬 TTL 은 환경변수 오버라이드를 제공한다
      (기존 리서치 훅의 TTL 오버라이드 선례를 따른다)
- [ ] AP-03: 신규 마크다운 산출물에 bare code fence 0 건 — 모든 fence 에 언어 힌트를 붙인다

## Reusability

- [ ] RE-01: 두 훅이 공통으로 쓰는 페이로드 파싱과 JSON 방출을 각자 재구현하지 않는다.
      중복이 생기면 공용 함수로 추출한다
- [ ] RE-02: 기존 리서치 훅에 이미 있는 센티넬 TTL 로직을 새로 발명하지 않고 동일 형태를 따른다

## Diagnostics

- [ ] DG-01: 신규 셸 파일 전체에 구문 검사 워닝 0 건 (project.yaml commands.analyze 의 검사 방식을
      이번 변경 파일에 적용)
- [ ] DG-02: IDE diagnostics 워닝 및 인포 0 건 (project.yaml ide_exclude 가 빈 목록이므로 제외 없음,
      스펠체크만 제외)
- [ ] DG-03: 검증 하네스 실행 콘솔 로그에 에러와 예외 0 건 (§범위 경계 5 에 따른 commands.test 대체)
- [ ] DG-04: 훅 등록 후 실제 Bash 호출 1 건과 실제 Edit 1 건을 수행해 훅 오류 출력 0 건
