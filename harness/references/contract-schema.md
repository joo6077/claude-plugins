# Sprint Contract 스키마

> sprint-contract 와 qa-evaluator 가 공유하는 계약 포맷 정의.
> contract-kaizen 이 변경 제안 가능, evaluator-kaizen 이 읽어서 평가 루브릭에 반영.
>
> **최근 갱신: 2026-08-13 (Phase 2 kaizen · v5.3)** — write-once 를 서술에서 **결정론적 봉인**으로 승급. frontmatter `conditions_digest` / `locked_at` 신설 (조건 체크박스 줄만 정규화 해시 — 체크박스 토글·서술 편집은 통과, 조건 문구 변조·조건 추가는 즉시 `SEAL_BROKEN`), amendment 를 **direction × consent 2 축**으로 분리 (앵커 부재가 방향 판정을 `unknown` 으로 붕괴시키던 구조 제거 · 경로 집합 amendment 의 direction 은 집합 비교로 **계산**), 조건 패턴 3 종 추가 (측정 커버리지 표기 · 인자 매트릭스 · 음성 대조).
>
> 이전: 2026-07-28 (v5.2) — 실행 기반 재검증 잔여 결함 봉합. `CONTRACT_ROOT` 탐색 기준을 `.harness/project.yaml` 에서 **`.harness/` 디렉토리 자체**로 바꿔 조용한 오귀속·미초기화 BLOCKED 를 동시에 제거 (`contract_root_unconfigured: true` 경고 + `/harness init` 안내), active 열거 grep 이 `status: "active"` 도 잡도록 수정 (test-fixtures README 와 패턴 일치).
>
> 이전: 2026-07-28 (v5.1) — v5 회귀 봉합. ladder 3.5 레거시 브릿지 (active 0 개일 때 레거시 plain 우선 → 없으면 레거시 유일 → 채택 + `legacy_contract_used` 경고), `status: done` 전환 주체 명시 (qa-evaluator, APPROVE 직후, `status: active` 명시분만), frontmatter 값 따옴표 규약 (writer 무따옴표 · reader 벗겨서 비교), 셸 이식성 규약 (zsh `nomatch` 때문에 글로빙 대신 `find`), 슬러그 재사용 우선 규칙.
>
> 이전: 2026-07-28 (v5) — 병렬 스프린트 안전성. 접미형 산출물 경로 (`-<slug>`) 정식화, 슬러그 규칙, frontmatter `slug` / `status` / `owner_session` 3 필드, status 해석 규칙 (필드 없으면 레거시 → active 제외), amendment 사이드카 규약, `CONTRACT_ROOT` 단일 해석 규칙 명문화.
>
> 이전: 2026-07-27 (v4) — 허용 섹션 헤더 2 계층 분류 (조건 섹션 / 서술 섹션), Counterpart 조건 패턴 (producer/consumer 분리 필수), Diff-Scope Oracle 표준형 4 요소, 증거 아티팩트 경로 명시 의무 추가. 상세 작성법은 `harness/docs/guides/contract-design-guide.md` 참조.
>
> 이전: 2026-04-24 (v3) — 검증 수단 명시 의무, 스코프 범위 인라인 명시, sibling consistency enumerated 필수, `[미검증]` 마커 표기 규칙 추가.
>
> 이전: 2026-04-11 (v2) — 조건 태그 (Specificity Tag) 서브섹션 신설, aggregation mode 개념 추가.

## 계약 파일 — 산출물 경로 (v5 개정)

> **이 섹션이 경로·슬러그 규약의 SSOT 다.** sprint-contract 스킬, qa-evaluator 에이전트,
> `harness/scripts/*.sh`, 각종 가이드 문서는 여기를 **인용만** 하고 자체 규칙을 재정의하지 않는다.

### CONTRACT_ROOT 해석 — 먼저 만나는 `.harness/` 에서 멈춘다 (v5.2 개정)

`CONTRACT_ROOT` 는 현재 디렉토리부터 위로 올라가며 **처음 만나는 `.harness/` 디렉토리를 가진
조상의 절대경로**다. 판정 기준은 `.harness/project.yaml` 이 아니라 **`.harness/` 디렉토리 자체**다.
세션 도중 cwd 가 바뀌어도 이 값을 기준으로 경로를 해석한다 (v4 추가 — `cwd-contract-path-drift`
재발 방지).

**v5.1 까지는 `project.yaml` 을 기준으로 삼았고, 그것이 조용한 오귀속을 만들었다.** `project.yaml`
이 없는 `.harness/` 는 그냥 지나쳐 상위로 올라갔기 때문에, **자기 계약을 가진 디렉토리를 건너뛰고
남의 계약을 채점**했다. 실측 (2026-07-28): `apps/app_kiosk` 는 자체 `.harness/sprint-contract.md`
(sha256 `e1a45c8bb5744b66…` · "adm_statistic_screen 리팩토링") 를 갖고 있으나 `project.yaml` 이
없어, 조상 `apps/` 의 다른 계약 (`ac9cd299b0cc9711…` · "preset skin 화면 스펙 통합") 이 **경고
없이** 선택됐다. BLOCKED 보다 나쁘다 — 사용자는 남의 계약으로 받은 verdict 를 자기 판정으로 읽는다.

- **`.harness/` 를 가진 디렉토리를 건너뛰고 상위 계약을 채점하지 마라.** 탐색은 첫 `.harness/`
  에서 무조건 멈춘다.
- 멈춘 디렉토리에 `project.yaml` 이 **없으면** 그 디렉토리를 그대로 `CONTRACT_ROOT` 로 쓰되,
  산출물에 **`contract_root_unconfigured: true`** 를 남기고 `/harness init` 실행을 안내한다.
- **`project.yaml` 부재만으로 BLOCKED 하지 마라.** 계약 파일이 실재하면 정상 평가한다 —
  `contract_root_unconfigured` 는 경고이지 실패가 아니며 ladder 판정을 바꾸지 않는다.
  `project.yaml` 에서만 오는 값 (`contract_categories` · `commands` · `anti_patterns`) 을 읽을 수
  없다는 사실을 경고에 함께 적고, 그 값에 의존하는 진단은 실행 불가로 기록한다.
- **복구 안내 문구를 원인에 맞춰라.** 계약 파일이 실재하는데 "Sprint Contract 가 존재하지
  않습니다" 라고 말하지 마라 — 실제 원인은 `/harness init` 미실행 (= `project.yaml` 부재) 이다.
  실측 3 곳 (`flutter_playwright` · `purchase-bot` · `_sandbox/flutter_colorpicker`) 이 계약을
  가진 채 이 오안내로 BLOCKED 됐다.
- 조상 체인에 `.harness/` 가 여러 개 있어도 **가장 깊은 것 하나를 채택하고 그대로 진행한다.**
  **"후보가 2 개 이상이면 BLOCKED" 같은 규칙을 도입하지 마라** — 실측상 정상 중첩 배포본이
  존재한다 (`fit-pal/app`, `fit-pal/server`, `fit-pal-wt/app`, `fit-pal-wt/server` 4 개가 각자
  `.harness/` 를 가지면서 조상에도 있다). 중첩을 에러로 처리하면 이 배포본들이 전부 깨진다.

```bash
# CONTRACT_ROOT 탐색 — 첫 `.harness/` 에서 멈춘다 (zsh · bash 동일)
resolve_contract_root() { # [시작디렉토리] → "<절대경로> configured|unconfigured", 없으면 exit 1
  d=${1:-$PWD}
  while [ -n "$d" ] && [ "$d" != "/" ]; do
    if [ -d "$d/.harness" ]; then
      if [ -f "$d/.harness/project.yaml" ]; then echo "$d configured"
      else echo "$d unconfigured"; fi
      return 0
    fi
    d=$(dirname "$d")
  done
  return 1   # 조상 체인에 .harness/ 가 없다 — 이때만 "harness 미초기화" 다
}
```

### 셸 이식성 규약 — 글로빙 대신 `find` (v5.1)

**이 스키마를 구현하는 문서·스크립트의 셸 스니펫은 zsh 에서도 그대로 돌아야 한다.** 사용자 기본
셸이 zsh 이고, zsh 는 `nomatch` 가 기본이라 **매치가 0 인 글로브는 명령을 실행조차 하지 않고 죽인다.**
bash 는 패턴 문자열을 그대로 넘기므로 같은 코드가 bash 에서만 동작한다.

- 계약·피드백·amendment 파일을 열거할 때 `sprint-contract-*.md` 같은 **글로브를 쓰지 마라.**
  `find <dir> -maxdepth 1 -type f \( -name ... -o -name ... \)` 로 열거한다.
- `for f in a.md b-*.md; do [ -f "$f" ] || continue; ...; done` 형태는 **가드가 무력하다.**
  zsh 는 `b-*.md` 가 없으면 루프 본문에 진입하지 않고 스크립트를 중단한다 — `a.md` 까지 통째로
  누락된다.
- **파일 목록을 문자열에 모아 unquoted 로 넘기지 마라 (v5.2).** zsh 는 `SH_WORD_SPLIT` 이 기본
  off 라 `grep ... $files` 가 목록 전체를 **파일명 하나**로 넘긴다. bash 에서만 동작하고 zsh 에서는
  매치 0 으로 **조용히 미발동**한다 — 죽지도 않으니 발견이 더 늦다. 배열로 모아
  (`arr+=("$f")` → `"${arr[@]}"`) 넘긴다. 공백 포함 파일명도 이때만 안전하다.
- 선례: `harness/skills/harness-kaizen/scripts/trigger-check.sh` 의 `current_feedback_files()` /
  `history_feedback_files()` 가 `find` 형태이고, `check_repeated_antipatterns()` 가 배열 형태다.
  새 구현은 그 형태를 따른다.

```bash
# 계약 후보 열거 (plain + 접미형) — 매치 0 이어도 두 셸에서 동일하게 빈 출력 + exit 0
list_contracts() { # list_contracts <CONTRACT_ROOT>
  find "$1/.harness" -maxdepth 1 -type f \
    \( -name 'sprint-contract.md' -o -name 'sprint-contract-*.md' \) 2>/dev/null | LC_ALL=C sort
}
```

### 산출물 3 종

| 산출물 | 경로 | 생성 주체 |
| ------ | ------ | ------ |
| 계약 | `{CONTRACT_ROOT}/.harness/sprint-contract-<slug>.md` | sprint-contract |
| QA 산출물 | `{CONTRACT_ROOT}/.harness/sprint-feedback-<slug>.md` | qa-evaluator |
| amendment 사이드카 | `{CONTRACT_ROOT}/.harness/sprint-amendments-<slug>.md` | sprint-contract / qa-evaluator |

3 종은 **같은 슬러그**로 짝지어진다. `sprint-contract-emoji-picker.md` ↔
`sprint-feedback-emoji-picker.md` ↔ `sprint-amendments-emoji-picker.md`.

### plain 모드는 계속 유효하다

슬러그가 없으면 접미 없는 파일명이 **그대로 유효**하다:

```text
{CONTRACT_ROOT}/.harness/sprint-contract.md
{CONTRACT_ROOT}/.harness/sprint-feedback.md
{CONTRACT_ROOT}/.harness/sprint-amendments.md
```

plain 모드를 폐기하거나 마이그레이션을 강제하지 마라. 병렬 세션을 돌리지 않는 프로젝트에서는
plain 이 정상 경로다. 접두형(`<slug>-sprint-contract.md`)은 **쓰지 않는다** — 실측 배포본의
접미형 계약 40 개 · 접미형 피드백 7 개가 고아가 된다.

### 슬러그 규칙

슬러그는 feature 이름에서 도출한다:

1. 소문자화
2. 공백·특수문자를 `-` 로 치환
3. 연속된 `-` 를 하나로 축약
4. 앞뒤 `-` 제거

최종 형식은 다음 정규식을 만족해야 한다 (총 1~48 자):

```text
^[a-z0-9][a-z0-9-]{0,47}$
```

도출 결과가 이 정규식을 만족하지 않으면 (예: 한국어만으로 된 feature 명이라 전부 치환되어 빈
문자열이 되는 경우) **임의로 지어내지 말고 사용자에게 슬러그를 물어라.**

기존 배포본 슬러그와 호환된다: `emoji-picker`, `ws5-stage2-apply`, `s6`, `az4-current-session`.

#### 슬러그 재사용 우선 (v5.1)

**같은 스프린트를 이어서 작업할 때는 새 슬러그를 도출하지 말고 기존 계약의 슬러그를 재사용한다.**
계약 · 피드백 · amendment 3 종은 같은 슬러그로만 짝지어지므로, 이어작업에서 슬러그를 새로
도출하면 이미 존재하는 피드백·사이드카가 고아가 된다 (실측 배포본에 접미형 짝 40 개가 있다).

- 재사용 판정 순서: 대상 계약 파일의 frontmatter `slug` → 파일명 접미 → (둘 다 없으면) plain 모드.
  **도출 규칙은 신규 스프린트에서만 쓴다.**
- **비ASCII feature 명에서 정보를 잃은 슬러그는 자동 채택하지 마라.** 도출 규칙은 `[^a-z0-9]+` 를
  `-` 로 치환하므로 한국어 부분이 통째로 사라진다 — `"emoji picker 개선"` → `emoji-picker` 는
  정규식은 통과하지만 "개선" 이 소실되어 원 스프린트와 구별되지 않는다. 정규식 통과 여부와 무관하게
  **비ASCII 문자가 제거된 경우 사용자에게 슬러그를 확인받는다.**
- 전부 치환되어 빈 문자열이 되는 경우(`"병렬 스프린트 안전성"`)는 위 §슬러그 규칙대로 즉시 질의한다.

## 허용 섹션 헤더 (v4 추가)

계약 파일의 2 단계(`##`) 헤더는 아래 두 계층 중 하나여야 한다. 밖의 헤더는 금지다.

| 계층 | 허용 헤더 | 헤더 매칭 | 조건 체크박스 |
| ------ | ------ | ------ | ------ |
| **조건 섹션 (parsed)** | `project.yaml.contract_categories` 의 각 `id` + `Anti-patterns` + `Reusability` + `Diagnostics` | 정확히 일치 (괄호 부연 금지) | `- [ ] {PREFIX}-{NN}:` 형태로 **여기에만** 존재 |
| **서술 섹션 (non-parsed)** | `배경` · `리서치 소스` · `GAP 분석` · `범위 경계` · `회귀 게이트` | 접두 일치 (뒤에 부연 허용) | 조건 체크박스 **금지** — 일반 불릿만 |

**결정론적 검사 (E3)** — 계약 저장 직후 실행하고 위반 0 건을 확인한 뒤 다음 단계로 넘어간다
(`$CONTRACT` = 방금 저장한 계약의 절대경로):

```bash
CONTRACT="$CONTRACT_ROOT/.harness/sprint-contract-<slug>.md"   # plain 모드면 접미 없이

# (1) 헤더 목록 — 허용 목록 밖 헤더가 있으면 위반
grep -n '^## ' "$CONTRACT"

# (2) 서술 섹션에 조건 체크박스가 섞였는지 — 조건 섹션 밖의 '- [ ]' 는 위반
awk '/^## /{s=$0} /^- \[ \]/{print FILENAME":"FNR": "s" -> "$0}' "$CONTRACT"
```

**허용 헤더 목록은 v5 에서도 늘어나지 않았다.** 스프린트 도중 합의된 조건 변경(amendment)을
기록하려고 계약 본문에 `## 변경 이력` · `## Amendments` · `## Notes` 같은 섹션을 추가하지 마라 —
허용 목록 위반이며 `parser-incompatible-contract-section` 재발이다. amendment 는 **별도 사이드카
파일**에 쓴다 (§Amendment 사이드카 참조).

## 메타데이터 (YAML frontmatter)

```yaml
feature: "{기능명}"
created: "{YYYY-MM-DD HH:mm}"
complexity: "{simple|medium|complex}"
conditions: {총 조건 수}
slug: {slug}                # v5 — 접미형일 때 필수, plain 모드면 생략. 따옴표 없이
status: active              # v5 — active | done. 따옴표 없이
owner_session: {세션 ID}    # v5 — $CLAUDE_CODE_SESSION_ID. 값이 없으면 필드 자체를 생략. 따옴표 없이
conditions_digest: sha256:{16hex}   # v5.3 — 조건 봉인. 따옴표 없이
locked_at: "{YYYY-MM-DD HH:mm}"     # v5.3 — 봉인 시각
```

### 값 따옴표 규약 (v5.1 — writer / reader 대칭)

`slug` · `status` · `owner_session` 세 필드는 **기계가 문자열 동등 비교**로 소비한다. writer 와
reader 의 따옴표 규약이 어긋나면 비교가 영원히 실패한다 — v5 에서 writer 가 `owner_session: "abc"`
로 쓰는데 reader awk 가 따옴표를 벗기지 않아 `$CLAUDE_CODE_SESSION_ID` 와 **절대 일치하지 않았고**,
ladder 2 단계(세션 소유 계약)가 통째로 죽어 있었다.

- **writer (sprint-contract)**: 세 필드를 **따옴표 없이** 쓴다. `feature` · `created` 같은 자유
  서술 필드는 기존대로 따옴표를 써도 된다 (비교 대상이 아니다).
- **reader (qa-evaluator 등)**: 따옴표가 **있든 없든 벗겨서** 비교한다. 값 앞뒤가 같은 종류의
  따옴표(`"` 또는 `'`)로 감싸인 경우에만 한 쌍을 제거하고, 앞뒤 공백도 제거한다.

```bash
# frontmatter 스칼라 1 개 읽기 — 값의 따옴표를 벗겨서 돌려준다 (zsh · bash 동일)
fm_get() { # fm_get <file> <key>
  awk -v k="$2" -v q="\"'" '
    NR==1 && /^---[[:space:]]*$/ { fm=1; next }
    fm && /^---[[:space:]]*$/    { exit }
    fm && index($0, k ":") == 1 {
      v = substr($0, length(k) + 2)
      sub(/^[[:space:]]+/, "", v); sub(/[[:space:]]+$/, "", v)
      c = substr(v, 1, 1)
      if (length(v) > 1 && index(q, c) > 0 && substr(v, length(v), 1) == c)
        v = substr(v, 2, length(v) - 2)
      print v; exit
    }' "$1"
}
```

### v5 신규 필드

| 필드 | 값 | 규칙 |
| ------ | ------ | ------ |
| `slug` | 슬러그 규칙을 만족하는 문자열 | 파일명 접미와 **동일**해야 한다. plain 모드면 필드 자체를 생략 |
| `status` | `active` \| `done` | 작성 시 `active`. `done` 전환 주체·시점은 §`status: done` 전환 주체 참조 |
| `owner_session` | `$CLAUDE_CODE_SESSION_ID` 값 | 환경변수가 비어 있으면 **필드를 쓰지 마라.** 빈 문자열·`unknown` 같은 placeholder 금지 |

### 계약 봉인 — `conditions_digest` / `locked_at` (v5.3 신규 · E3)

계약은 **write-once** 다. 승인 후에는 조건 문구를 고치지 않는다. v5 는 그 규칙을 amendment
사이드카라는 **대안 경로**로만 표현했고, 위반을 재는 오라클이 없었다. 실측 결과 규칙은 지켜지지
않았다 — 2026-08-11 REJECT: *"계약 write-once 위반 — 생성자가 자신이 만든 산출물을 사후에
허용하려 계약 AR-04 조건 문구를 직접 편집(5→7 경로, 사이드카/사용자 승인 앵커 없음)"*.

**근본원인 3 가지** (셋을 다 막아야 재발이 끊긴다):

| # | 근본원인 | 대응 |
| ------ | ------ | ------ |
| RC1 | write-once 규칙이 **읽기 측 문서에만** 있었다 (qa-evaluator / qa-evaluation-guide). 본문을 편집하는 주체는 **생성자**인데 생성자 문서(SKILL.md · contract-design-guide)에는 0 건이었다 | 쓰기 측 3 표면에 동일 규약 착지 |
| RC2 | 준수 경로(사이드카)의 기대 보상이 위반 경로보다 낮았다 — 앵커가 없다는 이유로 `unknown` 이 되어 아무 효력이 없었다 | §Amendment 사이드카 의 **direction × consent 2 축** 분리 |
| RC3 | 위반을 **탐지할 수 없었다** — 저장 검사 게이트는 헤더와 조건 **개수**만 본다. 문구가 바뀌어도 개수가 같으면 통과한다 | 본 절의 봉인 (E3) |

**정의** — `conditions_digest` 는 계약의 **조건 체크박스 줄만** 파일 순서대로 뽑아 체크 상태를
`- [ ]` 로 정규화한 뒤 sha256 을 취한 값의 앞 16 자리다. 접두 `sha256:` 을 붙여 쓴다.

- **정규화 대상이 조건 줄뿐인 이유**: 평가 진행에 따른 체크박스 토글(`- [ ]` → `- [x]`)과 서술
  섹션 보강은 계약 변조가 아니다. 이 둘로 봉인이 깨지면 게이트가 정상 작업을 막고, **우회된
  게이트는 없는 게이트보다 나쁘다.**
- 조건 **문구 변조**와 **조건 추가·삭제**는 반드시 깨진다. 이것이 봉인의 유일한 목적이다.
- 조건 열거 정규식은 §조건 수 계산과 **같은 것**을 쓴다 (`[A-Z]{2,}-[0-9]{2}`). 새 패턴을
  발명하면 두 게이트가 서로 다른 집합을 세게 된다.

```bash
# 봉인 계산·검증 — zsh · bash 동일. 해시 백엔드 4 종은 같은 값을 낸다
sha256_16() {  # stdin → sha256 앞 16 자리
  if   command -v sha256sum >/dev/null 2>&1; then sha256sum
  elif command -v shasum    >/dev/null 2>&1; then shasum -a 256
  elif command -v python3   >/dev/null 2>&1; then python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'
  else openssl dgst -sha256 | sed 's/.*= //'
  fi | cut -c1-16
}

contract_digest() {  # contract_digest <계약파일>
  grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16
}

verify_seal() {  # verify_seal <계약파일> → SEAL_OK | SEAL_BROKEN | SEAL_ABSENT
  rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}
  if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1")
  if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"
  else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi
}
```

**하위호환 — 부재는 실패가 아니다.** 두 필드는 **선택 필드**다. `conditions_digest` 가 없으면
`SEAL_ABSENT` 이며 이것은 경고이지 실패가 아니다. ladder 판정·`status` 해석·`conditions` 검사에
전혀 영향을 주지 않는다. 실측 (2026-08-13): 이 레포와 `history/` 의 기존 계약 **109 개 전부**가
`SEAL_ABSENT` 이고 `SEAL_BROKEN` 은 0 건이다 (zsh·bash 동일). **레거시 계약에 봉인을 소급해서
써 넣지 마라** — 그 순간 그 계약의 원문이 무엇이었는지 증명할 수 없는 봉인이 된다.

**`SEAL_BROKEN` 을 만났을 때** — 조용히 다시 봉인하지 마라. 그것은 위반을 지우는 행위다.
사용자에게 `recorded` / `actual` 두 값과 함께 보고하고, 변경 의도가 정당하면 **사이드카
amendment** 로 기록한다 (§Amendment 사이드카).

### status 해석 규칙 (backward-compat 의 핵심)

계약을 "active 인가" 로 세는 모든 로직 — 특히 qa-evaluator 의 계약 선택 — 은 아래를 그대로 따른다:

- **`status: active` 가 명시된 계약만 active 로 센다.**
- `status:` 필드가 **없으면 레거시**로 간주하고 **active 후보에서 제외**한다.
- **frontmatter 자체가 없어도 동일하게 제외**한다. 파싱 실패로 중단하지 마라.
- `status: done` 은 당연히 제외한다.

**근거 (실측, 2026-07-27 기준)**: 배포본 fit-pal 계열 `.harness` 에 이미 존재하는 접미형 계약
40 개 중 `status:` 필드를 가진 것은 **0 개**다. 이들을 active 로 세면 후보가 수십 개가 되어 그
프로젝트의 QA 가 영구 BLOCKED 된다. **파일 개수를 세지 말고 `status` 를 읽어라.**

```bash
# active 계약 열거 — frontmatter 없는 레거시는 자연히 빠진다.
# 글로빙 금지 (§셸 이식성 규약): 매치 0 이면 zsh 가 명령을 죽인다.
# 따옴표 유무를 모두 잡는다 (§값 따옴표 규약): writer 는 무따옴표로 쓰지만 손으로 적은
# `status: "active"` 가 실재하며, 그걸 놓치면 active 를 0 개로 세어 없던 BLOCKED 를 만든다.
find "$CONTRACT_ROOT/.harness" -maxdepth 1 -type f \
  \( -name 'sprint-contract.md' -o -name 'sprint-contract-*.md' \) \
  -exec grep -lE "^status:[[:space:]]*[\"']?active" {} + 2>/dev/null
# grep 은 매치 0 이면 exit 1 이다 — `set -e` 아래에서 쓸 때는 `|| true` 를 붙여라
# 이 열거는 빠른 스크리닝이다. 값 동등 비교가 필요하면 §값 따옴표 규약의 `fm_get` 을 써라.
# 같은 패턴을 `harness/evals/test-fixtures/README.md` 의 사전 점검이 쓴다 — 두 곳이 어긋나면 안 된다.
```

`status` 를 나중에 `done` 으로 바꾸는 것은 frontmatter 값 수정이므로 허용 섹션 헤더 규칙과 무관하다
(본문에 새 `##` 를 만드는 것이 아니다).

### ladder 3.5 — 레거시 브릿지 (v5.1 · 회귀 봉합)

레거시를 active 후보에서 제외하는 규칙만으로는 **기존 프로젝트 전체가 0-active BLOCKED** 가 된다.
v5 이전에는 평가자가 plain 계약을 조건 없이 읽었으므로 이것은 명백한 회귀다. 따라서 ladder 3 과 4
사이에 브릿지 한 단계를 둔다. **active 후보가 0 개일 때만** 보며, 하위 규칙은 2 개다:

| 하위 규칙 | 조건 | 선택 |
| ------ | ------ | ------ |
| **3.5-a plain 우선** | 레거시 중 plain `sprint-contract.md` 가 **있다** | 그것을 쓴다 (= v5 이전 동작 그대로) |
| **3.5-b 유일 접미형** | plain 이 없고 레거시가 **정확히 1 개** | 그것을 쓴다 |
| 그 외 | plain 없고 레거시 2 개 이상 | 발동하지 않는다 → ladder 4 BLOCKED |

- 어느 하위 규칙으로 선택했든 산출물에 **`legacy_contract_used: true` 경고**를 남긴다.
- active 가 1 개 이상이면 이 단계를 보지 않는다 — ladder 3 이 확정했거나 (2 개 이상이면) ladder 4
  BLOCKED 다. **레거시와 active 를 섞어 판단하지 않는다.**
- **`legacy_contract_used: true` 는 경고이지 실패가 아니다.** verdict 는 정상 산출한다. 다만 그
  계약은 소유 세션을 알 수 없으므로, 병렬 세션 환경이라면 사용자에게 계약 확정
  (`status: active` 부여 또는 `HARNESS_CONTRACT` 고정)을 권고한다.

**왜 plain 을 우선하는가 (실측, 2026-07-28 · `~/Hub/10_Dev` 하위 `.harness` 13 개)**: active 가
1 개인 곳은 이 레포뿐이고 나머지 12 개는 전부 `status` 미보유 레거시다. 그 12 개는 **전부 plain
`sprint-contract.md` 를 갖고 있다.** 반면 접미형 레거시는 `fit-pal/app` 27 개 · `fit-pal/server`
12 개처럼 과거 스프린트가 쌓여 있어, "레거시가 정확히 1 개일 때만" 이라는 규칙만 두면 이 3 개
배포본이 BLOCKED 로 남아 회귀가 남는다. plain 우선은 v5 이전 동작과 정확히 같으므로 회귀가 0 이다
(실측 결과: 13 개 중 1 개 ladder 3 · 12 개 ladder 3.5-a · BLOCKED 0).

```bash
# ladder 2 / 3 / 3.5 / 4 판정 — fm_get · list_contracts 는 위 정의를 쓴다 (zsh · bash 동일)
n_act=0; n_own=0; n_leg=0; pick_act=""; pick_own=""; pick_leg=""; pick_plain=""
while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$(fm_get "$f" status)" in
    active)
      n_act=$((n_act + 1)); pick_act="$f"
      if [ -n "$CLAUDE_CODE_SESSION_ID" ] &&
         [ "$(fm_get "$f" owner_session)" = "$CLAUDE_CODE_SESSION_ID" ]; then
        n_own=$((n_own + 1)); pick_own="$f"
      fi ;;
    "done") ;;
    *)
      n_leg=$((n_leg + 1)); pick_leg="$f"
      [ "$(basename "$f")" = "sprint-contract.md" ] && pick_plain="$f" ;;
  esac
done <<EOF
$(list_contracts "$CONTRACT_ROOT")
EOF

if [ -n "$CLAUDE_CODE_SESSION_ID" ] && [ "$n_own" -eq 1 ]; then
  echo "ladder2 $pick_own"
elif [ "$n_act" -eq 1 ]; then
  echo "ladder3 $pick_act"
elif [ "$n_act" -eq 0 ] && [ -n "$pick_plain" ]; then
  echo "ladder3.5a $pick_plain legacy_contract_used=true"
elif [ "$n_act" -eq 0 ] && [ "$n_leg" -eq 1 ]; then
  echo "ladder3.5b $pick_leg legacy_contract_used=true"
else
  echo "BLOCKED active=$n_act legacy=$n_leg"
fi
```

### `status: done` 전환 주체 (v5.1)

v5 는 "스프린트가 끝나면 `done` 으로 바꾼다" 고만 적어 **주체가 없었다.** 주체를 고정한다:

**전환하지 않으면 active 계약이 단조 증가한다** — 두 번째 스프린트부터 active 가 2 개가 되어
ladder 3(유일 active)이 무너지고 곧바로 BLOCKED 로 떨어진다. 종료 시점을 아는 주체는 판정을 낸
평가자이므로 평가자가 전환한다.

| 시점 | 주체 | 동작 |
| ------ | ------ | ------ |
| verdict = **APPROVE** 직후 | **qa-evaluator** | 평가한 계약의 frontmatter `status` 를 `done` 으로 전환 |
| verdict = **REJECT** | **qa-evaluator** | 전환하지 않는다 — `active` 를 유지한다 (재작업 대상) |
| verdict = **BLOCKED** | 아무도 | 전환하지 않는다 — 애초에 verdict 가 아니다 |
| 같은 슬러그 재작성 시 아카이브 | sprint-contract | `history/` 로 옮긴 **사본**의 `status` 를 `done` 으로 (§sprint-contract Step 6 아카이브) |

- **`status: active` 가 명시된 계약만 전환한다.** ladder 3.5 로 채택한 레거시 계약(= `status`
  필드 없음)에는 **`status` 를 새로 써 넣지 마라.** 레거시는 애초에 active 후보가 아니라 단조 증가를
  일으키지 않으며, `status: done` 을 박으면 다음 호출에서 브릿지 후보가 사라져 **없던 BLOCKED 를
  새로 만든다.**
- **전환은 verdict 산출 이후의 후처리다. 전환 실패는 verdict 를 무효화하지 않는다.** 파일이 읽기
  전용이거나 다른 세션이 이미 바꿨더라도 판정은 그대로 유효하며, 전환 결과
  (`active -> done` / `skipped` / `failed`)만 산출물에 기록한다.
- frontmatter 안의 `status:` 만 바꾼다. 본문에 우연히 등장하는 `status:` 줄은 건드리지 않는다.
- 전환은 frontmatter 값 수정이므로 §허용 섹션 헤더 규칙과 무관하다.

## 필수 섹션

### 1. 카테고리별 조건

```markdown
## {CategoryID}
- [ ] {PREFIX}-{NN}: {PASS/FAIL 이진 판정 가능한 조건문} [specificity-tag]
```

- `CategoryID` 와 `PREFIX` 는 `project.yaml.contract_categories` 에서 가져온다
- 조건문은 능동태, 단일 조건, 측정 가능해야 한다
- "잘 동작한다", "적절히 처리한다" 같은 모호 표현 금지
- 조건 끝에 **구체성 태그** 를 붙여라 — 상세는 아래 §조건 태그 섹션 참조

#### 조건 태그 (Specificity Tag)

모든 계약 조건은 끝에 구체성 태그를 붙여야 한다. 미명시 시 `[structural]` 로 간주.

| 태그 | 의미 |
|------|------|
| `[exact]` | 이름/값/구조 문자 그대로 매칭 |
| `[structural]` | 섹션/필드/파일 존재 확인 (기본값) |
| `[goal]` | 목표 달성 여부만 판정, 수단 무관 |

**예시:**

```markdown
- [ ] UI-01: 라우터에 /settings 경로가 등록된다 [exact]
- [ ] UI-02: 설정 화면에 접근성 라벨이 모든 버튼에 존재한다 [structural]
- [ ] LO-01: 로그인 실패 시 사용자에게 실패 원인이 전달된다 [goal]
```

**Aggregation Mode** — 다수 대상 (파일/모듈/키워드) 조건은 태그에 모드를 함께 명시한다:

| 모드 | 의미 |
|------|------|
| `enumerated` | 각 대상을 개별 이름으로 명시해야 PASS |
| `collective` | 포괄 경로/패턴 하나로도 PASS (기본값) |

**예시:**

```markdown
- [ ] RE-01: References 에 g1, g2, g3, g4, g5, g5b, g6 7 개 파일이 각각 파일명으로 명시된다 [exact, enumerated]
- [ ] RE-02: References 에 docs/react/kit-design/ 경로가 명시된다 [structural, collective]
```

**규칙:**

- 숫자 레벨 태그 (L-one/L-two/L-three) 는 **QA 평가 깊이 전용** — 계약 태그로 재사용 금지
- 상세한 작성법은 `harness/docs/guides/contract-design-guide.md` §조건 구체성 태그 참조

#### 검증 수단 인라인 명시 (v3 추가)

모든 조건은 "어떤 도구 · 명령 · 관찰로 판정할지" 를 인라인 기술한다.

**형식:**

```markdown
- [ ] {PREFIX}-{NN}: {조건} (측정: {명령/도구/관찰}) [specificity-tag]
```

**예시:**

```markdown
- [ ] AR-03: docs/flutter/ 총 줄 수 >= 1500 (측정: `wc -l docs/flutter/*.md | tail -1`) [exact]
- [ ] UI-05: 모달 overlay 가 표시된다 (측정: MCP Figma read-back 또는 Playwright snapshot) [goal]
```

**MCP / 외부 도구 fallback 3 단계 (v3 추가):**

외부 도구 의존 조건은 다음 3 단계를 인라인 기술한다:

```markdown
- [ ] LG-02: 모달 close 버튼 클릭 시 overlay 가 dismiss 된다
      (측정: 1차 MCP Figma read-back · 2차 fallback: MutationObserver 로 CSS display
      상태 확인 스크린샷 · 3차 불가능 시 `[미검증]` 마커 허용) [goal]
```

#### `[미검증]` 마커 (v3 추가)

평가 시점에 검증 도구가 모두 불가능하면 평가자는 해당 조건에 `[미검증]` 마커를
붙이고 근거 블록에 사유를 기록한다.

**수용 임계:**

- 계약 전체에서 `[미검증]` 마커 **1 건까지만** PASS 처리 가능
- **2 건 이상 누적 시 자동 REJECT** (qa-evaluation-guide 의 동일 정책과 맞물림)
- 계약 작성 단계에서 `[미검증]` 허용 건수 예상치가 2 건 이상이면 조건 재설계

#### Sibling Consistency enumerated (v3 추가)

플러그인 내 여러 스킬에 공통 원칙을 요구하는 조건은 반드시 `[exact, enumerated]`
또는 `[structural, enumerated]` 를 사용한다. 대상 스킬 개수를 숫자로 명시하고
이름 전부 열거.

```markdown
- [ ] SK-03: domain event + outbox 원칙이 rust-init, rust-feature, rust-service,
      rust-api 4 개 스킬 Gotchas 에 모두 존재한다 [exact, enumerated]
```

#### Counterpart 조건 (v4 추가)

계약 · 직렬화 포맷 · 공유 모델 · 공개 시그니처 · DB 스키마를 변경하는 스프린트는
**producer 면과 consumer 면을 각각 별도 조건**으로 담아야 한다. 한 조건에 양면을 묶는 것은
복합 조건이므로 금지다. 각 조건은 해당 면의 파일 경로를 `[exact, enumerated]` 로 열거한다
(`collective` 금지). consumer 가 없으면 "소비자 없음" 을 근거와 함께 조건에 명시한다.

```markdown
- [ ] AR-04: 응답 필드 rename 이 producer 면 파일 `server/src/handler/schedule.rs` 에
      반영된다 [exact, enumerated] (측정: 신규 필드명 존재 · 구 필드명 0 건)
- [ ] AR-05: 같은 rename 이 consumer 면 파일 `app/lib/data/model/schedule_model.dart`,
      `app/lib/data/model/schedule_model.g.dart` 2 개에 반영된다 [exact, enumerated]
      (측정: 신규 필드명 존재 · 구 필드명 0 건)
```

소비면의 **내부 구현**은 조건화하지 않는다 (과잉 계약). 한 스프린트에서 양면을 다 못 바꾸면
남는 쪽은 `[미검증]` 이 아니라 **명시적 미완 조건**으로 남긴다 — `[미검증]` 은 검증 도구 부재
전용 마커다.

#### Diff-Scope Oracle 표준형 (v4 추가)

"변경 범위" 를 조건으로 쓸 때 `git diff` 자유 서술을 금지한다. 아래 4 요소를 모두 채운다:
**(1) 상태 전제** (`Given: 커밋 직전 working tree` 또는 `Given: 스테이징 완료 후`) ·
**(2) 경로 한정 pathspec** · **(3) 생성물 제외 pathspec** · **(4) 기대 집합**("정확히 일치" 인지
"포함" 인지).

```markdown
- [ ] AR-01: 변경이 변환 헬퍼 2 개 파일로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git diff --name-only HEAD -- app/lib ':(exclude)*.g.dart'` 결과가
       `app/lib/data/mapper/schedule_mapper.dart`,
       `app/lib/data/mapper/group_mapper.dart` 2 행과 정확히 일치)
```

계약 작성 시점에 그 명령을 1 회 실행하고 현재 출력(baseline)을 서술 섹션에 남긴다.

#### 증거 아티팩트 경로 (v4 추가)

조건이 참조하는 증거가 코드 · 파일 · 명령 출력이 아니라 **기록물**(승인 로그, 합의 기록, 실측
수치)이면, 그 기록물이 평가 시점에 존재할 **경로**를 조건에 적는다. 경로를 적을 수 없으면 그
조건을 만들지 않는다.

```markdown
- [ ] UI-06: 채택 시안 ID 와 승인 일시가 `.harness/design-approval.md` 에 기록되어 있다
      [structural] (측정: 파일 존재 + 시안 ID 1 건 이상)
```

#### 측정 커버리지 표기 (v5.3 추가 · E2 검출기)

`enumerated` 조건은 **산문이 요구한 대상 집합**과 **측정이 실제로 훑는 대상 집합**이 같아야 한다.
실측 improvement: *"[AR-04] 계약-측정-불일치 — 조건 프로즈(화이트리스트 12항목)와 측정 필드(5개
무관 디렉토리 grep)의 커버리지 갭"*.

**표기 규약** — 두 집합을 **같은 표기**로 적어 기계가 대조할 수 있게 한다:

- 대상은 **백틱으로 감싼 공백 없는 토큰**으로 적는다 (`app/lib/foo.dart`, `RE-01`, `--cached`).
  백틱 안에 공백이 있으면 명령으로 간주해 대상 집합에서 제외한다 — `` `wc -l` `` 은 대상이 아니다.
- 산문 측 = 조건에서 `측정` 이라는 낱말이 처음 나오기 **전**의 토큰. 측정 측 = 그 **뒤**의 토큰.
- 상위 패턴 하나로 여러 대상을 덮을 때는 **작성 시점에 그 명령을 1 회 실행해 확장 결과를 측정 절에
  백틱으로 열거**한다 (Diff-Scope 표준형의 baseline 규칙과 같은 방식). 실행하지 않은 커버리지
  주장은 추측이다.
- **경로 화이트리스트는 예외 — 목록을 두 번 적지 마라.** 같은 경로 집합을 산문과 측정 명령
  양쪽에서 관리하면 한쪽만 고쳐지는 순간 계약이 자기모순에 빠진다 (실측 AR-04 의 배경 구조).
  화이트리스트형 조건은 **산문에 개수만** 적고(`정확히 N 경로로 한정된다`) **열거는 §Diff-Scope
  Oracle 표준형의 "기대 집합" 한 곳에서만** 한다. 이렇게 쓰면 산문 측 대상 토큰이 0 개라 위
  검출기도 자연히 통과한다.

```bash
# 커버리지 검출기 — zsh · bash 동일. 경로형 토큰이 2 개 이상인 enumerated 조건만 본다
awk -v MODE=path -v MIN=2 '
function collect(s, arr,   n, i, parts, t, c) {
  c = 0; n = split(s, parts, "`")
  for (i = 2; i <= n; i += 2) {
    t = parts[i]
    if (t == "" || t ~ /[ \t]/) continue
    if (MODE == "path" && t !~ /\// && t !~ /\.[A-Za-z0-9]+$/) continue
    arr[t] = 1; c++
  }
  return c
}
function flush(   i, p, m, pos, miss, np) {
  if (id == "") return
  if (buf ~ /enumerated/) {
    delete P; delete M
    pos = index(buf, "측정")
    if (pos > 0) { p = substr(buf, 1, pos - 1); m = substr(buf, pos) } else { p = buf; m = "" }
    np = collect(p, P); collect(m, M)
    if (np >= MIN) {
      miss = ""
      for (i in P) if (!(i in M)) miss = miss " " i
      if (miss != "") printf "UNCOVERED %s %s:%s\n", FILENAME, id, miss
    }
  }
  id = ""; buf = ""
}
match($0, /^- \[[ x]\] [A-Z]{2,}-[0-9]{2}/) {
  flush(); id = substr($0, RSTART + 6, RLENGTH - 6); sub(/^[^A-Z]*/, "", id); buf = $0; next
}
/^## /  { flush(); next }
/^- \[/ { flush(); next }
{ if (id != "") buf = buf " " $0 }
END { flush() }
' "$CF"
```

**이것은 blocking 게이트가 아니라 검출기다.** 실측 오탐률 때문이다 (2026-08-13 · 계약 109 개 ·
`enumerated` 조건 114 개): 백틱 토큰 전부를 대상으로 보는 나이브 형태는 **76 건**을 잡아 사실상
전건 경보였고, 경로형 토큰 2 개 이상으로 좁혀도 **29 건**이 남았다. 표본을 확인하면 상당수가
"상위 명령이 실제로 덮는" 정당 케이스다. 따라서 `UNCOVERED` 1 건마다 **(a) 조건을 고치거나
(b) 서술 절에 해소 기록 한 줄을 남긴다.** 자동으로 FAIL 시키지 않는다.

#### 인자 매트릭스 (Factor Matrix · v5.3 추가)

축이 **2 개 이상**이고 그 곱이 조건의 의미를 결정할 때만 쓴다. 축 하나짜리 조건에 강요하면
과잉 절차다.

실측 REJECT 두 건이 같은 뿌리다 — *"3 visibility x 6 relation = 18 케이스 중 15케이스(5 relation)만
재현. GroupMemberAndFollower 관계가 전체 누락"* · *"16종 매핑 단위 테스트 커버리지 부족 (2종만 검증)"*.

**규약:**

- 축과 축 값을 조건에 **열거**하고, 값의 출처를 코드의 **공유 상수/enum** 으로 지정한다.
  개별 테스트가 값을 재입력하면 다시 어긋난다 (improvement: *"audience_matrix.rs 의 6 relation 을
  feed_integration.rs 가 상수/enum 으로 재사용해 … 기계적으로 순회"*).
- **`cases_total` 을 손으로 적지 마라.** 축 값 개수의 곱을 산출하는 명령을 조건에 적고 그 출력을 쓴다.
- 기본은 **full Cartesian** 이다. pairwise 로 낮추려면 곱셈 결과와 사유를 서술 절에 적고 사용자
  승인을 받는다. 임계 숫자를 지어내지 않는다.

```markdown
- [ ] LG-01: visibility 3 값 × relation 6 값 전 조합이 테스트로 재현된다 [exact, enumerated]
      (축: visibility = `Public`,`Followers`,`Private` (출처 `audience.rs`) ·
       relation = `Self`,`Follower`,`GroupMember`,`GroupMemberAndFollower`,`Stranger`,`Blocked`
       (출처 `audience_matrix.rs`) ·
       cases_total: 축 값 개수의 곱을 명령으로 산출한 값 ·
       측정: 테스트가 두 상수를 import 해 순회하고 케이스 수가 cases_total 과 일치)
```

**두 번째 용법 — variant 구별성.** 탐색형 스프린트(시안·목업·변주)는 같은 매트릭스를 **variant
쪽에** 쓴다. variant 마다 축 값 조합을 `[exact, enumerated]` 로 열거하고, **동일 조합이 2 개 이상이면
FAIL** 이다. 실측 REJECT `UI-04`: *"B3(단일 컬럼)과 B6(조밀 로그)이 계약 지정 4축 전부에서
동일값 — 구조 구별 요구 위반"*. 스킬 측 짝은 `skill-design-guide.md` §5.6 Variant Budget 의
Variant Matrix 다 — 계약은 그 매트릭스를 **조건으로** 받는다.

```bash
# variant 축 조합 중복 검출 — 1 열 variant ID, 2 열부터 축 값 (탭 구분). zsh · bash 동일
TAB=$(printf '\t')
cut -f2- "$VARIANTS" | LC_ALL=C sort | uniq -d > "$DUPS"
n=$(grep -c . "$DUPS" || true)
while IFS= read -r dup; do
  [ -n "$dup" ] || continue
  printf 'DUP_AXIS [%s] <- variants: %s\n' "$dup" "$(grep -F "$TAB$dup" "$VARIANTS" | cut -f1 | tr '\n' ' ')"
done < "$DUPS"
[ "$n" -eq 0 ] && echo "VARIANT_DISTINCT_OK" || echo "VARIANT_DISTINCT_FAIL n=$n"
```

#### 음성 대조 (Negative Control · v5.3 추가)

조건이 **테스트 통과**를 요구하면, 그 테스트가 실제로 구현을 훑는지까지 조건에 담는다.
구현을 제거해도 통과하는 측정문은 오라클이 아니다.

실측 REJECT `ER-02` (2026-08-12): *"신규 통합 테스트가 실제 바이너리를 호출하지 않고 독립적으로
재작성한 SQL로 … **mutation test로 확정 — 실제 코드에서 동시성 가드(WHERE exercises = $3::jsonb)를
완전히 삭제해도 이 테스트는 여전히 통과한다**"*. 같은 날 `LG-01` · `LG-03` 도 "측정문은 통과하는데
구현과 결합되지 않은" 동형이다.

**적용 범위 (한정)** — 조건이 **테스트·실행 산출물로 판정**될 때만 필수다. 파일·섹션 존재를 보는
`[structural]` 조건에는 적용하지 않는다 (대상을 지우면 자명하게 실패하므로 무의미하다).

**규약:**

- 조건에 `음성 대조:` 절을 넣고 **어느 구현 지점을 무력화하면 그 측정이 FAIL 하는지**를 적는다.
- 측정이 구현을 **직접** 호출하는지 확인한다. 테스트가 로직을 재작성해 검증하면 결합이 없다 —
  바이너리·함수·쿼리를 그대로 호출하는 경로로 바꾼다.
- 계약 작성 시점에 음성 대조를 실제로 돌릴 수 없으면 그 사실을 조건에 적는다. **"돌렸다" 고
  적지 마라.**

```markdown
- [ ] ER-02: 낙관적 동시성 가드가 conflict 경로를 실제로 막는다 [goal]
      (측정: 백필 대상 행을 사전 변형한 뒤 실제 바이너리를 호출해 skipped 카운터 증가 관찰 ·
       음성 대조: 가드 술어를 제거하면 이 측정이 FAIL 해야 한다)
```

#### 조건 작성 preflight — QA 모호성 태그의 되먹임 (v5.3 추가)

평가자가 improvement 에 반복해서 붙이는 태그는 **계약 작성 단계에서 미리 잡을 수 있는 결함**의
목록이다. DRAFT 를 제시하기 전에 조건마다 6 항을 확인한다.

**이 표가 결함 태그 어휘의 SSOT 다.** 평가자(`harness/agents/qa-evaluator.md`)와 계약 작성
(`harness/skills/sprint-contract/SKILL.md`)이 **같은 어휘를 쓴다.** 다른 파일은 이 표를 복제하지
말고 경로로 참조하라.

> **왜 통합했나 (v5.4).** 이전 판은 평가자 집합 5 종과 작성 집합 6 종이 **교집합 `측정-중복`
> 하나뿐인 별개 어휘**였다. 그래서 평가자가 3 회 반복해 붙인 `측정-상태-모호` 가 작성 단계로
> 되먹여질 자리가 아예 없었고, 같은 결함이 계약마다 재생산됐다. 되먹임 루프의 단절이 원인이므로
> 규칙 문장을 더 쓰는 것으로는 안 걸린다 — **어휘를 하나로 만드는 것**이 수정이다.

| 태그 | 평가자 측 — 언제 붙이는가 | 작성자 측 — DRAFT 전 무엇을 자문하는가 |
| ---- | ------------------------- | -------------------------------------- |
| `측정-수단-부재` | 조건에 판정 명령·도구·관찰이 아예 없다 | 이 조건을 어떤 명령·도구·관찰로 판정하는지 인라인에 적었는가 |
| `측정-방식-불일치` | 측정이 조건 산문과 다른 값(뷰포트·경로·상태)을 쓴다 | 측정이 조건이 지정한 **값**과 같은 값을 쓰는가 |
| `측정-환경-오염` | 병렬 세션·잔여 산출물·설치본 차이가 결과를 흔들었다 | 환경 의존이 있는가 → `Given:` 에 환경 전제를 박았는가. **리터럴 환경값을 조건에 박지 않았는가** |
| `측정-산출물-부재` | 측정이 읽을 대상이 평가 시점에 없다 | 측정이 읽을 대상(테스트·기록물·출력)이 평가 시점에 실재하는가 |
| `검증경로-미기재` | 1 차 도구 부재 시 무엇을 할지가 없다 | 1 차 도구가 없을 때의 fallback 을 적었는가 |
| `측정-중복` | 같은 것을 두 조건이 재고 있다 | 같은 것을 두 조건이 재고 있지 않은가 (SSOT 위반) |
| `측정-상태-모호` | 측정 명령이 어떤 상태 전제에서 실행되는지 불명확해 판정이 갈린다 | 명령이 상태 의존적인가 → `Given:` 으로 전제(커밋 완료·빌드 산출·기동 여부)를 박았는가 |
| `태그-산출물-불일치` | `[exact]` 인데 산출물 이름이 다르거나, 태그가 요구하는 산출물이 제출되지 않았다 | 태그 강도가 실제 제출물과 맞는가. 낼 생각 없는 부산출물을 `[exact]` 로 적지 않았는가 |
| `범위-미명시` | "주요·모든·핵심" 같은 범위어가 열거 없이 쓰여 대상 집합이 갈린다 | 범위어를 인라인 enumerate 했는가. 예외를 조건 내부에 적었는가 |
| `증거-경로-부재` | `[goal]` 조건이 참조하는 기록물의 경로가 없어 읽을 대상이 없다 | 승인 기록·합의 로그에 의존한다면 그 기록물의 **경로**를 조건에 적었는가 |

이 표는 **검출용 자문 목록**이지 자동 판정기가 아니다. LLM 에게 "이 조건 모호한가?" 만 묻는
게이트를 만들지 마라 — 판정 근거가 남지 않는다.

### 2. Anti-patterns

```markdown
## Anti-patterns
- [ ] {id}: {message}
```

- `project.yaml.anti_patterns`에서 최소 2개 선별
- 해당 구현에서 발생 가능성이 높은 것을 우선 선택

### 3. Reusability (자동 포함)

```markdown
## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
```

### 4. Diagnostics (자동 포함)

```markdown
## Diagnostics
- [ ] DG-01: {commands.analyze} 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ({diagnostics.ide_exclude} 제외)
- [ ] DG-03: {commands.test} 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
```

## Amendment 사이드카 (v5 추가)

스프린트 도중 사용자와 합의해 조건을 바꿨다면 **계약 본문을 건드리지 말고** 사이드카 파일에 쓴다.

**경로**: `{CONTRACT_ROOT}/.harness/sprint-amendments-<slug>.md` (plain 모드면 `sprint-amendments.md`)

### 규약

- **계약 본문에 새 `##` 섹션을 추가하지 마라.** 허용 섹션 헤더 목록(§허용 섹션 헤더)은 고정이며,
  `## 변경 이력` / `## Amendments` 를 그 목록에 넣지 않는다. 사이드카는 **별도 파일**이지 계약
  섹션이 아니다.
- **원 조건을 삭제·수정하지 마라. 추가만 한다.** 계약 본문의 `- [ ]` 조건은 그대로 둔다. 사이드카는
  "이 조건을 이렇게 읽어라" 를 덧붙일 뿐이다.
- 각 amendment 는 **direction** 과 **consent** 두 축을 각각 갖는다 (v5.3 — 이전에는 한 축이었다):

축 1 · **direction** — PASS 집합이 어느 쪽으로 움직이는지를 본다.

판정 기준은 단 하나다: **이 amendment 를 적용하면 PASS 하는 구현의 집합이 줄어드는가, 늘어나는가.**
"범위 축소" 라는 말로 판정하지 마라 — 무엇의 범위인지에 따라 정반대가 된다.

| direction | 의미 | QA 에서의 취급 |
| ------ | ------ | ------ |
| `narrowing` | PASS 집합이 **줄어든다** (제약 강화 · 기준 상향 · 허용 범위 축소) | PASS 근거로 사용 가능 — 완화가 불가능하므로 consent 축과 무관 |
| `relaxing` | PASS 집합이 **늘어난다** (기준 하향 · 조건 면제 · 허용 범위 확대) | consent 가 `anchored` 일 때만 PASS 근거. `unanchored` 면 **불가** |
| `unknown` | PASS 집합의 증감을 판정할 수 없다 | **PASS 근거로 쓸 수 없다.** 사용자 확인 대상으로 표면화 |

**집합형 조건의 direction 은 자기신고하지 말고 계산한다.** 경로 화이트리스트·파일 열거·대상
목록처럼 조건이 집합을 담고 있으면 원 집합과 개정 집합을 비교해 direction 을 **계산**한다.
실측 위반(3 경로 → 5 경로)은 이 계산에서 `relaxing added=2 removed=0` 이 나온다 — 서술로
"범위 조정" 이라 부를 여지가 사라진다.

```bash
# 집합형 amendment 의 direction 계산 — zsh · bash 동일
amend_direction() {  # amend_direction <원집합파일> <개정집합파일> (각 줄 1 원소)
  added=$(comm -13 <(LC_ALL=C sort -u "$1") <(LC_ALL=C sort -u "$2") | grep -c . || true)
  removed=$(comm -23 <(LC_ALL=C sort -u "$1") <(LC_ALL=C sort -u "$2") | grep -c . || true)
  if   [ "$added" -eq 0 ] && [ "$removed" -gt 0 ]; then echo "narrowing added=$added removed=$removed"
  elif [ "$added" -gt 0 ]; then echo "relaxing added=$added removed=$removed"
  else echo "unknown added=$added removed=$removed"; fi
}
```

축 2 · **consent** — 사용자 동의 근거가 있는지를 본다.

| consent | 조건 |
| ------ | ------ |
| `anchored` | 사용자 발언 인용 + **reflect-kit prompt 로그 앵커**(timestamp · session · cwd) |
| `unanchored` | 앵커를 붙일 수 없다 (로그 미설치 · 구두 합의 · 에이전트 자체 판단) |

**앵커 부재가 direction 판정을 무너뜨리지 않는다 (v5.3 의 핵심 교정).** v5 는 두 축이 한
필드에 뭉쳐 있어서, 앵커가 없다는 이유만으로 방향까지 `unknown` 이 되었다 — 실측:
*"amendment A-01은 prompt-log 앵커 부재로 unknown 분류, PASS 근거 불가"*. 그 결과 준수 경로가
아무 효력이 없어졌고, 다음 시도에서 **계약 본문 직접 편집**으로 우회가 일어났다. 두 축을 분리하면
`narrowing · unanchored` 는 정상적으로 PASS 근거가 된다 (제약을 강화하는 방향이라 남용 불가).

| direction \ consent | `anchored` | `unanchored` |
| ------ | ------ | ------ |
| `narrowing` | PASS 근거 가능 | **PASS 근거 가능** |
| `relaxing` | PASS 근거 가능 (사용자 재승인 성립) | PASS 근거 **불가** — 표면화 |
| `unknown` | PASS 근거 불가 — 표면화 | PASS 근거 불가 — 표면화 |

- **`relaxing` 의 승인 주체는 사용자뿐이다.** reviewer 확인을 추가 요건으로 두지 않는다 —
  평가자는 계약에 없는 요구를 만들지 않는 것이 원칙이다 (contract-design-guide §Cross-Surface
  Parity item 12 착지 구조).
- 사용자 발언을 인용할 때 로그는 redaction 을 거치므로 인용문은 "verbatim" 이 아니라
  **"redaction 거친 원문"** 이다 — 그렇게 표기하라.
- **`unanchored` 를 감추려고 앵커를 지어내지 마라.** 없으면 `unanchored` 라고 쓰는 것이
  `narrowing` 을 살리는 유일한 길이다.

### 엔트리 포맷

```markdown
## AM-01 — narrowing
- 대상 조건: AR-02
- 변경: 대상 파일을 `harness/scripts/save-feedback.sh` 1 개로 한정 (원 조건은 `harness/scripts/` 전체)
- 근거 (redaction 거친 원문): "피드백 스크립트만 손대고 나머지는 다른 에이전트가 한다"
- 앵커: 2026-07-28T10:14:02+09:00 · session=8a9c2ebc · cwd=/Users/jackson/Hub/10_Dev/claude-plugins
```

사이드카 파일은 계약 파서 대상이 아니므로 `##` 헤더 이름에 제약이 없다. 다만 위 5 개 항목
(대상 조건 · 변경 · 근거 · 앵커 · 헤더의 유형)은 전부 채운다. 앵커를 붙일 수 없는 구두 합의는
amendment 로 인정하지 않는다 — 계약 조건과 동일하게, 평가 시점에 읽을 대상이 없으면 판정 불가다.

## 복잡도별 조건 수 가이드

| 복잡도 | 파일 영향 | 조건 수 |
|--------|----------|--------|
| 단순 | 1-3 | 4-6 |
| 중간 | 4-8 | 8-12 |
| 복잡 | 9+ | 12-20 |

## 스키마 버전

현재: **v5.3** (2026-08-13)

변경 이력:

- **v5.3 (2026-08-13)** — write-once 를 서술에서 **결정론적 봉인(E3)** 으로 승급 + 조건 패턴 3 종 추가.
  **계약 봉인** (`conditions_digest` · `locked_at` 선택 필드 · 조건 체크박스 줄만 정규화 해시 ·
  체크박스 토글과 서술 편집은 `SEAL_OK` · 조건 문구 변조와 조건 추가·삭제는 `SEAL_BROKEN` ·
  부재는 `SEAL_ABSENT` 경고이지 실패 아님) — 직전 사이클이 도입한 amendment 사이드카만으로는
  2026-08-11 REJECT (*"계약 write-once 위반 — 생성자가 자신이 만든 산출물을 사후에 허용하려 계약
  AR-04 조건 문구를 직접 편집(5→7 경로)"*) 를 막지 못했다. 근본원인은 3 개였다 — 규칙이 **읽기 측
  문서에만** 존재 (쓰기 측 grep 0 건) · 준수 경로의 기대 보상이 위반 경로보다 낮음 · **위반을 재는
  오라클 부재**. 실측 하위호환: 기존 계약 109 개 전부 `SEAL_ABSENT` · `SEAL_BROKEN` 0 (zsh·bash 동일).
  **amendment direction × consent 2 축 분리** — v5 는 두 축이 한 필드에 뭉쳐 있어 앵커 부재만으로
  방향 판정까지 `unknown` 으로 붕괴했고 (실측: *"amendment A-01은 prompt-log 앵커 부재로 unknown
  분류, PASS 근거 불가"*) 그 결과 준수 경로가 무력화됐다. 이제 `narrowing · unanchored` 는 PASS
  근거가 되고, 집합형 조건의 direction 은 `comm` 집합 비교로 **계산**한다 (3→5 경로 = `relaxing`).
  **측정 커버리지 표기 + 검출기(E2)** — improvement *"[AR-04] 계약-측정-불일치"* 대응. blocking
  게이트가 아니다: 실측 오탐률(계약 109 개 · enumerated 조건 114 개 · 나이브 76 건 / 좁힌 형태
  29 건) 때문에 "검출기 + 해소 기록" 으로 착지했다. **인자 매트릭스** — 조합 케이스 수 수기 오류
  (`3 x 6 = 18 중 15 만 재현` · `16 종 중 2 종만 검증`) 와 variant 축 값 중복 (`UI-04`) 을 같은
  패턴으로 처리. **음성 대조** — `ER-02` 의 mutation test 확정 결함(가드를 삭제해도 테스트 통과)
  대응. 테스트 통과를 요구하는 조건에만 적용. **조건 작성 preflight** — QA 모호성 태그 6 종을
  작성 단계 자문 목록으로 되먹임.
- **v5.2 (2026-07-28)** — v5.1 을 실행 기반으로 재검증해 남은 결함 봉합.
  **`CONTRACT_ROOT` 탐색 기준 개정** (조상 체인에서 **먼저 만나는 `.harness/` 에서 멈춘다** ·
  기준이 `project.yaml` 이 아니라 디렉토리 자체 · `project.yaml` 이 없으면 그 디렉토리를 쓰되
  `contract_root_unconfigured: true` 경고 + `/harness init` 안내 · 부재만으로 BLOCKED 금지) —
  v5.1 기준으로는 `project.yaml` 없는 `.harness/` 를 건너뛰어 **자기 계약을 가진 `apps/app_kiosk`
  대신 조상 `apps/` 의 다른 계약을 경고 없이 채점**했고 (실측 sha256 `e1a45c8b…` vs
  `ac9cd299…`), 반대로 계약이 실재하는 배포본 3 곳 (`flutter_playwright` · `purchase-bot` ·
  `_sandbox/flutter_colorpicker`) 은 `CONTRACT_ROOT` 가 빈 문자열이 되어 "계약이 존재하지
  않습니다" 라는 **틀린 사유로 BLOCKED** 됐다. **active 열거 grep 의 따옴표 대응**
  (`grep -lE "^status:[[:space:]]*[\"']?active"`) — v5.1 패턴은 `status: "active"` 를 놓쳐
  active 를 0 개로 세었고, `harness/evals/test-fixtures/README.md` 의 사전 점검 패턴과도
  어긋나 있었다. 두 곳의 패턴을 동일하게 맞춘다.
- **v5.1 (2026-07-28)** — v5 회귀 봉합 (적대적 검증 blocking 5 · major 6 대응).
  **ladder 3.5 레거시 브릿지** (active 0 개일 때만 · 3.5-a 레거시 plain `sprint-contract.md` 우선 ·
  3.5-b plain 이 없고 레거시가 정확히 1 개면 그것 · 둘 다 아니면 BLOCKED · 선택 시
  `legacy_contract_used: true` 경고) — v5 의 레거시 제외 규칙만 적용하면 실측 CONTRACT_ROOT 13 개 중
  12 개가 0-active BLOCKED 가 되어, plain 계약을 조건 없이 읽던 v5 이전 대비 명백한 회귀였다
  (브릿지 적용 후 실측: ladder 3 1 개 · 3.5-a 12 개 · BLOCKED 0). **`status: done` 전환 주체 명시**
  (qa-evaluator 가 APPROVE 직후 전환 · REJECT/BLOCKED 면 `active` 유지 · `status: active` 명시분만
  전환하고 레거시에는 필드를 새로 쓰지 않음 · 전환 실패는 verdict 를 무효화하지 않음 · 아카이브
  사본은 sprint-contract 담당). **frontmatter 값 따옴표 규약** (`slug`/`status`/`owner_session` 은
  writer 가 따옴표 없이 쓰고 reader 는 있든 없든 벗겨서 비교 — v5 에서 writer 가 `"..."` 로 쓰고
  reader awk 가 벗기지 않아 ladder 2 단계가 상시 불성립이었다). **셸 이식성 규약** (사용자 기본 셸
  zsh 의 `nomatch` 로 매치 0 인 글로브가 명령을 죽이므로 파일 열거는 글로빙 대신 `find` —
  `harness/skills/harness-kaizen/scripts/trigger-check.sh` 선례). **슬러그 재사용 우선** (이어작업은
  기존 `slug`/파일명 접미를 재사용 · 비ASCII 문자가 제거되어 정보를 잃은 슬러그는 자동 채택 금지).
- **v5 (2026-07-28)** — 병렬 스프린트 안전성. 계약/피드백/amendment 3 종의 **접미형 경로**
  (`sprint-{contract,feedback,amendments}-<slug>.md`) 정식화 + plain 모드 병존 유지, 슬러그 규칙
  (`^[a-z0-9][a-z0-9-]{0,47}$`), frontmatter `slug` / `status` / `owner_session` 3 필드 추가,
  **status 해석 규칙** (`status: active` 명시분만 active · 필드 없거나 frontmatter 자체가 없으면
  레거시로 active 제외 — 배포본 접미형 계약 40 개 전부 `status` 미보유라 이 규칙이 없으면 영구
  BLOCKED), amendment 사이드카 규약 (유형 narrowing/relaxing/unknown · relaxing·unknown 은 PASS
  근거 불가 · 계약 본문 `##` 섹션 추가 금지 · prompt-log 앵커 필수), `CONTRACT_ROOT` 는 "가장 가까운
  조상" 단일 규칙임을 명문화 (중첩 배포본 4 개 보호 — 다중 후보를 BLOCKED 로 처리하지 않는다).
- **v4 (2026-07-27)** — 허용 섹션 헤더 2 계층 분류 (조건 섹션 parsed / 서술 섹션 non-parsed) 와 저장 직후 결정론적 검사, `CONTRACT_ROOT` 기준 경로 해석, Counterpart 조건 (producer/consumer 분리 · `[exact, enumerated]` 필수), Diff-Scope Oracle 표준형 4 요소, 증거 아티팩트 경로 명시 의무. Phase 1 §3.7 enforcement 등급 사다리를 계약 레이어에 적용하여 재발 규칙 4 건을 승급.
- **v3 (2026-04-24)** — 검증 수단 인라인 명시 필수, MCP/외부 도구 의존 조건의 3 단계 fallback 규칙, `[미검증]` 마커 및 수용 임계 (1 건 허용 / 2 건 이상 REJECT) 명문화, Sibling Consistency 조건 enumerated 필수. Phase 1 (skill/agent-design-guide) Cross-Surface Parity 원칙을 계약 레이어에 전수.
- **v2 (2026-04-11)** — 조건 구체성 태그 (`[exact]` / `[structural]` / `[goal]`) 와 aggregation mode (`enumerated` / `collective`) 필수화. 숫자 레벨 태그 금지 명시.
- **v1** — 초기 스키마.
