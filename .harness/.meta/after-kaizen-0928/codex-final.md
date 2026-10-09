현재 판에서 false-pass 결함 10개를 찾았습니다. 이 중 실제 검사 게이트에 영향을 주는 8개는 합치기 전에 고치는 편이 안전합니다. 저장소 파일은 변경하지 않았습니다.

## 1. 결함 목록

1. **막음 · 확증(실행)** — 잘못된 git 기준판을 “drift 없음”으로 통과

   - 위치: [scripts/detect-docs-drift.py:238](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/detect-docs-drift.py:238), [scripts/detect-docs-drift.py:251](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/detect-docs-drift.py:251), [scripts/detect-docs-drift.py:442](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/detect-docs-drift.py:442)
   - 원인: `git diff` 실패를 `""`로 바꿔 변경 파일 0개로 해석합니다.
   - 가장 작은 입력: `--since refs/heads/definitely-not-there`
   - 관찰 결과:

     ```text
     no docs drift since refs/heads/definitely-not-there
     rc=0
     ```

   - 가장 작은 고침: `run_git()`에서 비정상 종료를 예외/구조 오류로 올리고 `main()`이 2를 반환하게 합니다.

2. **막음 · 확증(코드 경로 모의 실행)** — 깨진 `evals.json`을 없는 파일처럼 건너뛰고 0 반환

   - 위치: [scripts/sync-evals.py:50](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/sync-evals.py:50), [scripts/sync-evals.py:184](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/sync-evals.py:184), [scripts/sync-evals.py:204](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/sync-evals.py:204)
   - 원인: 파일 없음과 JSON 파싱 실패가 모두 `None`이고, 호출부는 둘 다 `SKIP` 처리합니다.
   - 가장 작은 입력: 마켓에 등록된 킷의 `evals/evals.json` 내용이 `{ broken`.
   - 같은 반환 경로를 모의 실행한 결과:

     ```text
     → api-kit
       SKIP (no evals.json)
     Total: 0 added, 0 orphans, 0 missing (preview)
     simulated_bad_json_rc=0
     ```

   - 가장 작은 고침: 파일 없음만 `None`; 파싱·읽기 실패는 즉시 `return 2` 또는 예외로 구분합니다.

3. **막음 · 확증(정적)** — 실행할 `run` 단계가 0개여도 로컬 CI 성공

   - 위치: [scripts/ci-local.sh:45](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/ci-local.sh:45), [scripts/ci-local.sh:72](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/ci-local.sh:72), [scripts/ci-local.sh:96](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/ci-local.sh:96)
   - 가장 작은 입력:

     ```yaml
     jobs:
       a:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
     ```

   - `uses` 단계는 48–49행에서 버려지고, 마지막 판정은 `failed=0 && unsupported=0`뿐이라 `steps=0 run=0 rc=0`입니다.
   - 현재 테스트는 `uses`와 `run`이 함께 있는 경우만 다뤄 이 경우를 놓칩니다.
   - 가장 작은 고침: 파싱 뒤 `steps == 0` 또는 `ran == 0`이면 준비 실패 2로 끝냅니다. 모든 `run`이 SKIP인 경우도 정책을 명시하는 편이 좋습니다.

4. **막음 · 확증(정적)** — 추적 파일 읽기 실패를 조용히 버림

   - 위치: [scripts/check-install-docs-guidance.py:84](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/check-install-docs-guidance.py:84), [scripts/check-install-docs-guidance.py:111](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/check-install-docs-guidance.py:111)
   - 가장 작은 입력: 킷의 추적된 Markdown 한 파일에 `docs/foo/` 참조가 있고 안내는 없으며, 그 파일을 읽을 수 없게 `chmod 000`으로 둔 저장소.
   - 86–89행에서 `OSError`를 `continue`하고 `need`가 늘지 않아 0으로 끝납니다.
   - 가장 작은 고침: `unreadable` 수와 경로를 기록하고 하나라도 있으면 종료 코드 2를 반환합니다. 검사할 텍스트 확장자를 먼저 제한하면 바이너리와도 구분할 수 있습니다.

5. **막음 · 확증(정적)** — `superseded_by` 대상이 읽히지 않아도 `OK`

   - 위치: [harness/scripts/check-superseded.sh:24](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/harness/scripts/check-superseded.sh:24), [harness/scripts/check-superseded.sh:26](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/harness/scripts/check-superseded.sh:26), [harness/scripts/check-superseded.sh:29](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/harness/scripts/check-superseded.sh:29)
   - 가장 작은 입력:
     - `a`: `status: superseded`, `superseded_by: b`
     - `b`: 파일은 존재하지만 읽을 수 없음
   - `-f b`는 참이고 `fm_get b status`는 실패/빈 값이므로 `superseded`가 아니라고 보아 31행의 `OK`로 갑니다. 원본 계약 자체를 못 읽으면 24행에서 검사 대상에서도 빠집니다.
   - 가장 작은 고침: 모든 `fm_get` 호출의 종료 코드를 먼저 확인하고 실패하면 `UNREADABLE`과 종료 코드 2를 냅니다.

6. **막음 · 확증(모의 실행)** — 비어 있는 eval 목록을 경고만 하고 PASS

   - 위치: [scripts/run-evals.py:140](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/run-evals.py:140), [scripts/run-evals.py:152](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/run-evals.py:152)
   - 가장 작은 입력: `{"evals":[]}` 또는 알려진 목록 키가 전혀 없는 `{}`.
   - 관찰 결과:

     ```text
     WARN: evals.json에 eval 엔트리가 없음
     empty_evals_result=(0, 0)
     ```

   - `main()`은 실패 수 0으로 종료 코드 0을 냅니다.
   - 가장 작은 고침: 엔트리 0개를 구조 오류 2 또는 적어도 실패 1건으로 셉니다.

7. **막음 · 확증(정적)** — 접근성 검사 대상 HTML이 0개여도 `0/0 PASS`

   - 위치: [scripts/check-docs-a11y.js:40](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/check-docs-a11y.js:40), [scripts/check-docs-a11y.js:47](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/check-docs-a11y.js:47), [scripts/check-docs-a11y.js:162](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/scripts/check-docs-a11y.js:162)
   - 가장 작은 입력: 존재하지만 HTML 파일이 하나도 없는 `docs/`.
   - `files=[]`, 반복 0회, `fails=0`이 되어 `0/0 PASS`와 종료 코드 0입니다.
   - 가장 작은 고침: 브라우저를 띄우기 전에 `files.length === 0`이면 오류를 내고 2로 끝냅니다.

8. **막음 · 확증(정적)** — 같은 Bambu 픽스처의 두 번째 표 행을 무시

   - 위치: [bambu-kit/evals/run-gate-fixtures.sh:52](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/bambu-kit/evals/run-gate-fixtures.sh:52), [bambu-kit/evals/run-gate-fixtures.sh:60](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/bambu-kit/evals/run-gate-fixtures.sh:60)
   - 가장 작은 입력: 같은 `x.json`을 표에 두 번 적되 첫 행은 실제 결과와 맞고 둘째 행은 반대 기대값, 실행 줄은 한 번.
   - 집합 대조는 `sort -u`로 중복을 없애고, 실제 기대값은 `head -1`만 사용합니다. 따라서 잘못된 둘째 행이 있어도 첫 행만 맞으면 통과합니다.
   - 가장 작은 고침: 표와 실행 목록 각각에서 `sort | uniq -d`가 한 줄이라도 나오면 불일치로 끝내고 `head -1`에 의존하지 않습니다.

9. **막지 않음 · 확증(최소 AWK 입력 실행)** — 산문을 찾는 grep 명령 전체가 한 백틱 안에 있으면 오라클 경고 누락

   - 위치: [lint-contract-oracle.sh:72](/Users/jackson/.claude/hooks/lint-contract-oracle.sh:72), [lint-contract-oracle.sh:81](/Users/jackson/.claude/hooks/lint-contract-oracle.sh:81)
   - 가장 작은 입력:

     ```markdown
     - [ ] SK-01: x
       측정: `grep -cF "표준으로 강제하지 않는다" file.md` >= 1
     ```

   - `is_command(t)`가 참이면 84행에서 명령 덩어리 전체를 건너뜁니다. `grep -c`와 `>=` 때문에 실행 신호는 있다고 보므로 태그가 비어 버립니다.
   - 동일 판정식 실행 결과: `lint_tag=[] prose=0 exec_sig=1`.
   - 가장 작은 고침: 명령 백틱을 통째로 제외하지 말고, grep/rg의 검색 패턴 인수를 떼어 `is_prose()`에 넣습니다.
   - 이 훅은 설계상 경고만 내므로 “막지 않음”으로 분류했습니다.

10. **막지 않음 · 확증(정적)** — 빈 QA 결과 파일을 완료된 QA로 인정

   - 위치: [qa-pending-check.sh:76](/Users/jackson/.claude/hooks/qa-pending-check.sh:76), [qa-pending-check.sh:82](/Users/jackson/.claude/hooks/qa-pending-check.sh:82), [qa-pending-check.sh:87](/Users/jackson/.claude/hooks/qa-pending-check.sh:87), [qa-pending-check.sh:95](/Users/jackson/.claude/hooks/qa-pending-check.sh:95)
   - 가장 작은 입력: 이 세션 소유의 active 계약과, 이름만 맞는 0바이트 `sprint-feedback-….md`.
   - 파일 존재 검사는 통과하고 `verdict=""`, `evaluated=""`가 됩니다. 빈 verdict는 `REJECT|BLOCKED`가 아니며 날짜 검사도 생략되어 `pending`에 아무것도 추가되지 않습니다.
   - 가장 작은 고침: 허용 판정을 명시적으로 열거합니다. 예를 들어 `APPROVE`만 완료로 보고, verdict 또는 유효한 `Evaluated` 시각이 없으면 pending으로 셉니다.
   - 이 훅도 `additionalContext`만 내는 안내 장치라 “막지 않음”입니다.

## 2. 본 파일과 관점

지정된 저장소 파일 21개와 외부 훅 2개를 모두 한 번 이상 읽었습니다.

- JS/브라우저: `api-ui.spec.js`, `visuals.spec.js`, `check-docs-a11y.js`
  - 0개 테스트·0개 HTML, 첫 locator만 보는지, 생성한 mockup의 복제 범위, 브라우저 오류 전파를 확인했습니다.
- 셸 검사와 시험: Bambu fixture runner, commit-guard 본체/시험, measure 시험, superseded 본체/시험, validate, trigger-check, ci-local과 시험, spawn-kaizen-phase
  - 빈 입력, 중복 행, `head -1`, 읽기 실패, 파이프라인 종료 코드, glob 0개, bash/zsh 문법과 배열 사용을 봤습니다.
- Python 검사와 시험: cause-table 검사/시험, 설치 안내 검사, docs drift/시험, run-evals, sync-evals
  - JSON·git·파일 읽기 실패, 빈 대상, 동적 대상 발견, 첫 일치/중복, 오류 코드 2 보존을 봤습니다.
- 외부 훅: `lint-contract-oracle.sh`, `qa-pending-check.sh`
  - 한글 판정의 로캘 의존성, command-span 누락, 빈·깨진 QA 결과, 첫 머리말/첫 verdict 처리를 봤습니다.

추가 확인 결과:

- 대상 셸 파일은 `bash -n`과 `zsh -n`을 모두 통과했습니다.
- Python AST와 JS `node --check`도 통과했습니다.
- `[ -~]` 범위식은 이 Mac의 `C`, `C.UTF-8`, `en_US.UTF-8`, `ko_KR.UTF-8`에서 한글을 지우지 않았습니다.
- 현재 실제 저장소에서는 sync `rc=0`, 설치 안내 검사 `94 files / need=0`, cause-table 검사 `rc=0`, superseded 검사 `6건 / violations=0`이었습니다.
- `git diff --check origin/main...HEAD`는 깨끗했습니다.
- 확인 뒤 `git status --short` 출력도 비어 있었습니다.

이번 범위에서는 **이 Mac에서만 우연히 도는 것으로 확증된 결함은 없었습니다**. 특히 지적된 zsh glob과 한글 로캘 범위는 별도로 확인했지만 새 실패를 재현하지 못했습니다.

## 3. 보지 못한 것과 까닭

- 읽기 전용 샌드박스가 `/tmp`의 `mktemp`와 출력 리다이렉션까지 `Operation not permitted`로 막았습니다. 따라서 권한 없는 파일, 빈 `docs/`, 중복 Bambu 표, uses-only CI를 실제 임시 저장소로 만드는 종단 실행은 못 했습니다. 해당 항목은 줄별 제어 흐름과 쓰기 없는 모의 실행으로 확증했습니다.
- 같은 이유로 새 Playwright 출력 폴더와 브라우저 프로필이 필요한 시각 시험은 다시 돌리지 못했습니다.
- Bambu Studio/OrcaSlicer 설치본 유무에 따른 실제 슬라이서 판정은 실행하지 못했습니다. 설치본이 없는 환경의 `건너뜀` 정책 자체는 이번 결함 목록에 포함하지 않았습니다.