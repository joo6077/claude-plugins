# 훅 2종 4축 검증 기록 — autofixer-oracle-guards

계약: `.harness/sprint-contract-autofixer-oracle-guards.md` (봉인 `sha256:7703ece3176bcbde`)
사이드카: `.harness/sprint-amendments-autofixer-oracle-guards.md` (AM-01 ~ AM-09)
하네스: `.harness/.meta/verify-autofixer-oracle-guards.sh`
검증일: 2026-08-15

## 산출물

| 파일 | 역할 | git 추적 |
| --- | --- | --- |
| `~/.claude/hooks/block-dirwide-autofixer.sh` | 훅 A · PreToolUse Bash · deny | 아니오 (전역 자산) |
| `~/.claude/hooks/lint-contract-oracle.sh` | 훅 B · PostToolUse Edit\|Write · 경고 | 아니오 (전역 자산) |
| `~/.claude/hooks/_lib-hook-payload.sh` | 공용 페이로드 파싱·JSON 방출 (RE-01 · AM-09) | 아니오 (전역 자산) |
| `~/.claude/settings.json` | 훅 등록 (15 → 17 항목) | 아니오 (전역 자산) |
| `.harness/.meta/verify-autofixer-oracle-guards.sh` | 4축 검증 하네스 | 예 |

훅 출력 스키마는 배포 바이너리 `2.1.232` 에 임베드된 훅 문서에서 확인했다 —
`permissionDecision` / `permissionDecisionReason` 는 **PreToolUse 전용**이고 PostToolUse 는
`hookSpecificOutput.{hookEventName, additionalContext}` 를 쓴다. 훅 B 가 차단하지 않는 것은
설계 선택이자 스키마 제약이다.

## 축 1 — 양성 (차단·검출되어야 하는 입력)

인자 매트릭스: **tool 14 × mode 2 × argshape 3 = 84 케이스**. `cases_total` 은 손으로 적지 않고
세 축 길이의 곱으로 산출한다. 축 값은 하네스에 재타이핑하지 않고 **훅 소스의 `TOOLS_NAME` /
`TOOLS_RO` 배열에서 추출**한다 (두 곳이 어긋날 수 없다).

```text
cases=84 deny=28 pass=56 mismatch=0
deny 셀 = mode(write) × argshape{dir, omitted} × tool 14 = 28
```

훅 B 양성 대조: `.harness/sprint-contract-kaizen-phase6-variant-decision-gates.md` 의 `AR-03`.
측정절이 `표준으로 강제하지 않는다` 라는 **한글 산문 한 구절**을 grep 대상으로 삼아 문서에 그
문장이 있는지만 본다. 비교 연산자(`>= 1`)가 붙어 있어도 재는 것은 문장의 존재뿐이라 oracle 이
아니다 — 검출됨.

## 축 2 — 음성 대조 (구현을 무력화하면 측정이 FAIL 하는가)

서술이 아니라 **변이체(mutant)를 실제로 만들어 실행**했다. 통과하는 변이체는 그 측정이
oracle 이 아니라는 뜻이다.

| # | 무력화 지점 | 기대 | 실측 |
| --- | --- | --- | --- |
| 1 | 훅 A `hook_deny` 분기 제거 | deny 0 | 0 / 4 ✓ |
| 2 | 훅 A mode 축 판정 제거 | check 모드가 deny 로 뒤집힘 | 3 / 3 ✓ |
| 3 | 훅 A `ANCHOR` 제거 | 오탐 입력이 deny 로 잡힘 | 3 / 4 ✓ |
| 4 | 훅 A TTL 비교 제거 | 만료 센티넬이 통과로 뒤집힘 | deny 0 ✓ |
| 5 | 훅 B 산문 판정 분기 제거 | `AR-03` 이 출력에서 사라짐 | 사라짐 ✓ |
| 6 | 훅 A deny 사유의 리터럴 2 종 제거 (AM-06) | ER-01 측정이 FAIL | 잔존 0 / 2 ✓ |
| 7 | settings.json 기존 항목 1 건 삭제 | SC-02 comm 이 1 행 출력 | 1 행 ✓ |

## 축 3 — 오탐 (인접하지만 정당한 입력)

훅 A 는 **명령 위치 앵커**로 판정한다. 포매터 이름이 검색어·문자열·파일명으로 등장하는 경우는
차단하지 않는다.

| 입력 | 결과 |
| --- | --- |
| `git log --grep=prettier` | 통과 ✓ |
| `echo "run black on it"` | 통과 ✓ |
| `cat scripts/fix-markdown-lint.py` | 통과 ✓ |
| `rg "cargo fmt" docs/` | 통과 ✓ |

read-only 모드 28 셀 전부 통과 (`--check` `--dry-run` `--diff` `-l` `--check-only`
`--output=none`). 명시 파일 인자 28 셀 전부 통과.

훅 B 오탐 대조 — 실행·수치 비교로 판정하는 조건은 검출하지 않는다 (AM-03 이 리터럴로 고정):

| 조건 | 성격 | 결과 |
| --- | --- | --- |
| Phase6 `ER-01` | 스니펫 추출 → 실행 → `hamming=0 < 2` + exit 1 | 미검출 ✓ |
| Phase6 `ER-02` | fixture 투입 → 실행 → exit 1 | 미검출 ✓ |
| Phase6 `ER-03` | 없는 경로 → `NO_MANIFEST` + exit 3 | 미검출 ✓ |
| Phase6 `DG-02` | zsh·bash 양쪽 실행 후 `diff` 무출력 | 미검출 ✓ |

**기존 계약 전체 검출률** (§범위 경계 1 에 따라 자기 산출물 제외):

```text
DETECTION_RATE files=21 conditions=447 flagged=32 rate=7.2%
```

이것은 **검출기이지 게이트가 아니다**. contract-schema §측정 커버리지 검출기 가 같은 성격으로
착지했고 (계약 109 개 · enumerated 조건 114 개 → 나이브 76 건 / 좁힌 형태 29 건), 여기서도
`UNCOVERED` 와 마찬가지로 1 건마다 조건 수정 또는 해소 기록을 요구할 뿐 자동 FAIL 시키지 않는다.

설계 과정에서 오탐률을 실제로 좁혔다: 초기 판정은 "백틱 토큰이 비ASCII 면 산문" 이었고 Phase6
한 파일에서만 **10 / 25** 를 잡았다. 표본을 확인하니 `§5.6` · `§5 Variant Contract Matrix`
같은 **절 참조 토큰**이 비ASCII(`§`)라는 이유만으로 잡히고 있었다. 구조용 기호를 먼저 제거하고
**한글이 남는가**로 좁혀 **3 / 25** 가 되었고, 남은 3 건은 전부 진성이다.

## 축 4 — 회귀 (기존 차단이 그대로 동작하는가)

| 대상 | 확인 | 결과 |
| --- | --- | --- |
| `enforce-foreground-research.sh` 등 기존 훅 등록 | 편집 전 command 집합 ⊆ 편집 후 집합 | 소실 0 행 ✓ |
| 등록 항목 수 | 15 → 17 (신규 2 건만 증가) | ✓ |
| 기존 PreToolUse Bash 훅 (`sdk-guard` · `run-guard`) | 플러그인 hooks.json 미변경 | ✓ |
| 유효 JSON | `jq -e` 파싱 | ✓ |

편집 전 baseline (AM-05): sha256 앞 16 자리 `6156d8c323175c4a` · command 항목 **15** 건.

## fail-open (ER-02)

| 케이스 | 훅 A | 훅 B |
| --- | --- | --- |
| `jq` 부재 (shim PATH 격리) | exit 0 · deny 없음 ✓ | exit 0 ✓ |
| 빈 stdin | exit 0 ✓ | exit 0 ✓ |
| 깨진 JSON stdin | exit 0 ✓ | exit 0 ✓ |

두 훅 모두 `set -e` 를 쓰지 않는다. errexit 는 fail-open 을 깨뜨린다 — 훅이 죽어서 정상 작업을
막는 것은 훅이 없는 것보다 나쁘다.

## 진단 (AM-08 이 리터럴로 고정한 대상)

| 항목 | 대상 | 결과 |
| --- | --- | --- |
| DG-01 구문 검사 | 훅 3 종 + 하네스 = 4 파일 × `bash -n` · `zsh -n` | 8 / 8 OK · 워닝 0 |
| DG-02 정적 분석 | `shellcheck 0.11.0` `-S warning` 4 파일 | exit 0 · 출력 0 |
| DG-03 실행 로그 | 하네스 실행 로그 2 종 (bash · zsh) | 에러 패턴 0 건 |
| 셸 이식성 (§범위 경계 4) | 두 셸 출력 `diff` | 무출력 · 양쪽 exit 0 |

## 구현 중 실측으로 잡은 결함 5 건

전부 **실행해서** 드러났다. 서술 검토만 했으면 전부 통과했을 것들이다.

1. **`cargo fmt` 같은 두 단어 도구명** — 첫 단어만 잘라내면 `fmt` 가 파일 인자로 오인되어
   광역 호출이 통과했다. 매치된 실제 텍스트 기준으로 자르도록 수정.
2. **ugrep 의 그룹 내 `$` 오인식** — 이 환경 `grep` 은 ugrep 7.5.0 래퍼다. `--check([ =]|$)` 가
   `parentheses not balanced` 로 죽어 read-only 판정이 통째로 무력화됐다. 끝 경계를 문자열 끝에
   공백을 덧붙이는 방식으로 대체.
3. **구분자 파싱이 정규식을 절단** — `${entry%%|*}` 로 필드를 자르는데 정규식 자체가 `[^;&|]` 로
   `|` 를 포함해 패턴이 대괄호 중간에서 잘렸다. 병렬 배열로 교체.
4. **`grep -c` 의 이중 0** — 매치 0 일 때 `0` 을 출력하고 exit 1 이라 `|| printf '0'` 이 붙으면
   출력이 `0\n0` 이 되어 산술 에러로 루프가 죽었다. 검출률이 조용히 0 으로 보고됐다.
5. **zsh 이식성 2 건** — (a) zsh 배열은 1-based 라 `[0]` 접근이 `parameter not set` 으로 죽었다
   (b) zsh 는 `SH_WORD_SPLIT` 이 기본 off 라 `for m in $MODES` 가 목록 전체를 원소 하나로 넘겨
   **죽지도 않고 조용히** 케이스 수가 84 → 14 로 줄었다. 인덱싱과 단어 분리 의존을 모두 제거.

(4) 와 (5b) 는 **죽지 않고 조용히 틀린 값을 보고**했다. bash 에서만 돌렸으면 (5) 는 못 잡았다.

## DG-04 — 등록 후 라이브 발동 (end-to-end)

하네스 단독 실행이 아니라 **실제 Claude Code 세션의 훅 체인**을 통과한 결과다.

| 축 | 호출 | 결과 |
| --- | --- | --- |
| 실제 Bash 1 건 | `git status --porcelain` (AM-08 고정, read-only) | 정상 실행 · 훅 오류 0 |
| 실제 Edit 1 건 | `sprint-amendments-autofixer-oracle-guards.md` (AM-08 고정) | 정상 저장 · 훅 오류 0 |
| 훅 A 라이브 발동 | `prettier --write nonexistent_dir_xyz/` | **deny** — 사유 전문이 그대로 반환됨 |
| 훅 B 무음 통과 | 같은 Edit (대상 패턴 밖 파일) | 출력 없음 (정상) |

훅 A 의 라이브 deny 는 **설계된 동작이지 훅 오류가 아니다** (AM-08 이 이 구분을 명문화했다).
훅 오류란 훅이 stderr 를 뱉거나 exit 0 이 아닌 경우를 말하며, 그런 사례는 0 건이었다.

## Iteration 2 — QA REJECT(`AP-01`) 대응

iteration 1 판정: **REJECT 20 / 21**. FAIL 은 `AP-01` 1 건이었다.

**결함**: 사이드카 AM-07 이 TTL 규칙을 "TTL 정수는 `${VAR:-N}` 형태의 기본값 표현으로**만**
등장한다" 로 썼는데, 훅 A 의 주석(24 행)과 deny 메시지(170 행)에 설명용 `3600` 이 그 형태 밖에
있었다. 평가자가 엄격 해석을 정확히 적용했다. 평가자는 나아가 "AM-07 이 선례로 인용한
`enforce-foreground-research.sh` 자체가 같은 패턴(4 건 중 3 건이 형태 밖)이라, AM-07 이
해소하려던 자기모순이 재정의 후에도 남아 있다" 고 실측으로 지적했다 — 옳다.

**선택**: 계약을 또 완화(`relaxing`)하는 대신 **구현을 고쳤다.** AP-01 의 범위를 "코드 로직의
변수 대입식" 으로 좁히는 amendment 는 PASS 집합을 넓히므로 또 한 번 사용자 앵커가 필요하고,
무엇보다 그 완화가 **실제 문제를 남긴다** — 사용자가 `DIRWIDE_FORMAT_TTL` 을 조정해도 메시지는
계속 3600 을 안내한다.

**수정 3 곳** (`~/.claude/hooks/block-dirwide-autofixer.sh`):

1. 주석에서 숫자를 제거하고 값의 정의처를 `ttl` 대입식 한 곳으로 가리킨다
2. `ttl="${DIRWIDE_FORMAT_TTL:-3600}"` 대입을 센티넬 존재 검사 **밖으로 hoist** 한다 —
   deny 메시지가 이 값을 인용해야 하고, `set -u` 아래에서 미설정 변수 참조는 스크립트를 죽여
   **fail-open 을 깨뜨린다**
3. deny 메시지의 리터럴을 `${ttl}` 인용으로 교체한다

**결과**: `3600` 이 파일 전체에서 정확히 1 회, `${DIRWIDE_FORMAT_TTL:-3600}` 형태로만 등장한다.

```text
기본값       → "...(TTL 3600 초, DIRWIDE_FORMAT_TTL 로 조정)."
TTL=7200     → "...(TTL 7200 초, DIRWIDE_FORMAT_TTL 로 조정)."
```

메시지가 **실제 유효 TTL 을 반영**하게 되었다 — 규칙 충족과 무관하게 개선이다.

**회귀 (전 축 재실행)**:

| 항목 | 결과 |
| --- | --- |
| 하네스 bash · zsh | 양쪽 exit 0 · 출력 `diff` 무출력 · `cases=84 deny=28 mismatch=0` |
| 검출률 | `files=21 conditions=447 flagged=32 rate=7.2%` (불변) |
| ER-01 리터럴 2 종 | 둘 다 잔존 ✓ |
| ER-02 fail-open | 빈 stdin · 깨진 JSON 모두 exit 0 ✓ |
| DG-01 구문 검사 | 4 파일 × 2 셸 실패 0 |
| DG-02 shellcheck | exit 0 · 출력 0 |
| DG-03 실행 로그 | 에러 패턴 0 건 (두 셸) |

**음성 대조 재실행 + 신규 1 건**:

| # | 무력화 지점 | 결과 |
| --- | --- | --- |
| 4 | TTL 비교 제거 + 만료 센티넬 | deny 0 → 통과로 뒤집힘 ✓ |
| 6 | deny 사유의 리터럴 2 종 제거 | 잔존 0 / 2 ✓ |
| **8 (신규)** | `ttl` 대입의 hoist 를 되돌림 | **exit 1 로 사망** — hoist 가 fail-open 을 지탱하고 있음이 실증됨 ✓ |

**후속 (이번 스프린트 스코프 밖)**: `enforce-foreground-research.sh` 도 같은 TTL 패턴을 갖는다.
Sibling Consistency 관점에서 함께 고칠 값이 있으나, 이번 스프린트 대상은 followup §훅 승격 후보
의 2 건뿐이라 손대지 않았다 (사용자 지시: "후보를 늘리지 마라"). 다음 사이클 후보다.

## APPROVE 후 하드닝 — 계약 조건 아님, 실사용 결함 4 건

iteration 2 는 **APPROVE 21 / 21** 이었고 계약은 `status: done` 으로 전환됐다. 평가자가 FAIL 은
아니지만 Improvement 로 표면화한 항목을 실물로 확인했더니 **계약 문언 밖의 실사용 결함**이
나왔다. 계약이 승인됐다고 배포된 가드에 알려진 결함을 남길 수는 없으므로 고쳤다.

### (1) false negative — 가드의 핵심 실패

`validate-plugin.py` 의 `--check=LIST` 를 read-only 모드로 매핑한 것이 틀렸다. 그것은
**검사 항목 선택**이고 쓰기 여부를 결정하는 것은 `--fix` 다.

```text
수정 전: `validate-plugin.py --check=placeholders --fix` → PASS (실제로는 파일을 고친다)
수정 후: → DENY
```

오탐보다 위험하다 — 가드가 있는데 통과시켰다.

### (2) 오탐 3 건 + 예방적 4 건 — 축약형·대체형 플래그

`TOOLS_RO` 가 각 도구의 긴 형태만 담고 있었다. 평가자가 2 건을 지목했고 전수 확인에서 1 건을
더 찾았다.

| 입력 | 수정 전 | 수정 후 |
| --- | --- | --- |
| `eslint --fix-dry-run src/` (eslint 의 실제 dry-run) | DENY ✗ | PASS ✓ |
| `dart format -o none lib/` (축약형) | DENY ✗ | PASS ✓ |
| `dart format --output none lib/` (공백 구분형) | DENY ✗ | PASS ✓ |
| `prettier -c src/` (`--check` 축약형) | DENY ✗ | PASS ✓ |
| `isort -c .` · `clang-format -n` · `autopep8 -d` | 예방적 추가 | PASS ✓ |

**이 결함 계열은 매트릭스가 구조적으로 못 잡는다.** 84 케이스는 `TOOLS_RO` 에서 파생한 플래그만
쓰므로 **배열 자체가 틀렸다는 사실**을 검증할 수 없다 — 자기지시적 오라클이다. 실제 도구의
플래그를 손으로 적어 투입하는 축을 하네스에 신설했다.

### (3) heredoc 본문이 명령으로 오인됨 — 즉시 재현된 오탐

`grep` 은 줄 단위라 앵커의 `^` 가 **매 줄** 시작에 걸린다. 그 결과 여러 줄 명령 안의 heredoc
본문 — 파일에 **써 넣을 내용** — 이 명령 위치로 판정됐다.

**발견 경위가 그 자체로 증거다**: 위 (1)(2) 테스트 케이스를 이 하네스에 추가하려는 호출이
자기 자신에게 차단됐다. 문서·테스트에 포매터 명령을 적을 때마다 재발하므로 우회를 유발한다.

`strip_heredoc_bodies()` 로 heredoc 본문을 판정 대상에서 제거하되, **heredoc 밖 줄바꿈은 진짜
명령 구분자이므로 그대로 둔다** (false negative 를 새로 만들지 않기 위해):

| 입력 | 기대 | 실측 |
| --- | --- | --- |
| heredoc 본문에 포매터 | PASS (데이터) | PASS ✓ |
| `cd /tmp` 다음 줄에 포매터 | DENY (명령) | DENY ✓ |
| heredoc 종료 후 포매터 | DENY (명령) | DENY ✓ |

### (4) 수정 중 자초한 결함 — 함수 정의가 호출보다 뒤

`strip_heredoc_bodies` 를 파일 중간에 넣어 **호출이 정의보다 앞**에 왔다. `command not found` →
`cmd` 가 빈 문자열 → **가드가 통째로 무발동**했다. fail-open 설계라 조용히 죽었다. 삽입 앵커
문자열이 파일에 2 곳 있어 헬퍼가 **중복 삽입**되기까지 했다. 정의를 호출 앞으로 옮기고 중복을
제거했으며, 그 이유를 소스 주석에 남겼다.

fail-open 은 훅이 정상 작업을 막지 않게 하지만, **가드가 죽은 것도 조용히 숨긴다.** 훅 수정 후에는
반드시 양성 케이스 1 건을 실행해 가드가 살아 있는지 확인해야 한다.

### 하드닝 후 전체 회귀

```text
bash exit=0  zsh exit=0  ·  두 셸 출력 diff 무출력
HARNESS_OK fails=0 cases_total=84
DETECTION_RATE files=21 conditions=447 flagged=32 rate=7.2%
실사용 플래그 변형 13 / 13 ✓   heredoc 3 / 3 ✓
AP-01 (iteration1 FAIL 조건): 3600 형태 밖 0 건 · '/Users/' 리터럴 0 건 (3 파일)
shellcheck -S warning 4 파일 exit=0   계약 SEAL_OK · status done
```

**주의**: 이 하드닝은 APPROVE **이후**의 변경이라, 배포된 훅 A 는 평가자가 판정한 시점의 파일과
다르다. 계약 21 조건은 하네스로 전부 재확인했으나, 엄밀히는 재평가 대상이다.

## Iteration 3 판정 및 정정 — APPROVE 21 / 21

봉인 `sha256:7703ece3176bcbde` 가 iteration 2 와 동일함까지 재확인됐다 (write-once 무결성이
iteration 을 가로질러 유지됨). `status: done` 은 재전환하지 않았다.

평가자가 비차단 Improvement 3 건을 냈고, 그중 2 건은 **내 산출물의 실제 결함**이라 고쳤다.

### (1) 하네스 SK-06 루프가 AM-03 지정 대상을 빠뜨림 — 수정함

AM-03 이 오탐 대조 3 건을 `ER-01` · `ER-02` · `ER-03` 으로 못박았는데, 하네스 루프는
`ER-01 ER-02 DG-02` 를 돌고 있었다. **사이드카가 지정한 대상과 하네스가 실제로 도는 대상이
어긋난 상태**였다. 평가자가 훅 B 를 직접 돌려 `ER-03` 이 실제로 미검출임을 확인했으므로 **동작은
옳았고 커버리지 기록만 틀렸다.** 루프를 `ER-01 ER-02 ER-03 DG-02` 로 고쳤다 (지정 3 건 + 초과 1 건).

문서가 주장하는 커버리지와 실측 커버리지가 갈리는 것은 이 스프린트가 기계화하려는 결함 계열과
같은 뿌리다 — 주장은 검증이 아니다.

### (2) `command` 항목 수의 범위 미기재 — 정정함

"15 → 17" 은 **파일 전체**의 `command` 키를 센 값으로, 훅이 아닌 `statusLine.command` 를 포함한다.
**훅만 세면 14 → 16 이다.** SC-02 의 판정은 영향받지 않는다 — 절대 개수가 아니라 집합 포함관계
(`comm -23` 0 행)로 측정했고, 그 비교가 statusLine 까지 포함해 수행되어 오히려 더 강한 검사였다.
정정 대상은 라벨과 숫자이지 측정 결과가 아니다. 상세는 사이드카 §정정 절 참조.

### (3) SK-03 음성 대조 문구가 4 / 4 를 함의 — 계약 문언 이슈, 수정 불가

계약 SK-03 의 음성 대조 절이 "앵커를 제거하면 이 4 건이 deny 로 잡혀야 한다" 고 읽히는데 실측은
**3 / 4** 다 (4 번째는 무관한 argshape 경로가 따로 막는다). 이 증거 기록은 처음부터 `3 / 4 ✓` 로
정직하게 적었고 하네스 임계도 `>= 3` 이다. **계약 본문은 봉인되어 고칠 수 없으므로** 다음 스프린트가
같은 패턴을 쓸 때의 교훈으로 남긴다: 음성 대조에 **기대 건수를 못박지 말고 "적어도 N 건" 또는
"뒤집히는 케이스가 존재한다" 로 쓰라.** 일부 케이스가 여러 방어층에 걸쳐 보호되는 것은 정상이며,
전건 뒤집힘을 요구하면 정상 구현을 FAIL 시킨다.

### 정정 후 회귀

```text
bash exit=0  zsh exit=0  ·  두 셸 출력 diff 무출력
HARNESS_OK fails=0 cases_total=84
SK-06 오탐 대조: ER-01 · ER-02 · ER-03 · DG-02 (AM-03 지정 3 + 초과 1) 전부 미검출 ✓
```

**평가자 도구 제약 (투명 공개)**: qa-evaluator 서브에이전트의 도구셋에 Task/Agent 가 없어
Step 7 교차 진단을 수행할 수 없었다. 세 iteration 모두 그 사실을 피드백에 명시하고 조용히
건너뛰지 않았다.
