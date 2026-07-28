# Sprint Contract 스키마

> sprint-contract 와 qa-evaluator 가 공유하는 계약 포맷 정의.
> contract-kaizen 이 변경 제안 가능, evaluator-kaizen 이 읽어서 평가 루브릭에 반영.
>
> **최근 갱신: 2026-07-28 (Phase 2 kaizen · v5.2)** — 실행 기반 재검증 잔여 결함 봉합. `CONTRACT_ROOT` 탐색 기준을 `.harness/project.yaml` 에서 **`.harness/` 디렉토리 자체**로 바꿔 조용한 오귀속·미초기화 BLOCKED 를 동시에 제거 (`contract_root_unconfigured: true` 경고 + `/harness init` 안내), active 열거 grep 이 `status: "active"` 도 잡도록 수정 (test-fixtures README 와 패턴 일치).
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
- [ ] RE-01: private 일회용 컴포넌트가 없다
- [ ] RE-02: 기존 공용 컴포넌트를 재사용한다
```

### 4. Diagnostics (자동 포함)

```markdown
## Diagnostics
- [ ] DG-01: analyze 경고 0건
- [ ] DG-02: analyze 에러 0건
- [ ] DG-03: 테스트 전체 통과
- [ ] DG-04: 콘솔 에러 0건
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
- 각 amendment 는 **유형**을 반드시 하나 갖는다:

| 유형 | 의미 | QA 에서의 취급 |
| ------ | ------ | ------ |
| `narrowing` | 제약 강화 (범위 축소 · 기준 상향) | PASS 근거로 사용 가능 |
| `relaxing` | 제약 완화 (범위 축소 아님 · 기준 하향 · 조건 면제) | **PASS 근거로 쓸 수 없다.** 사용자 확인 대상으로 표면화 |
| `unknown` | 강화인지 완화인지 판정 불가 | **PASS 근거로 쓸 수 없다.** 사용자 확인 대상으로 표면화 |

- 사용자 발언을 인용할 때는 **reflect-kit prompt 로그 앵커**(timestamp · session · cwd)를 붙인다.
  로그는 redaction 을 거치므로 인용문은 "verbatim" 이 아니라 **"redaction 거친 원문"** 이다 —
  그렇게 표기하라.

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

현재: **v5.2** (2026-07-28)

변경 이력:

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
