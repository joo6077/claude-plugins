---
feature: "계약 스킬 안내 두 가지 — 피드백 저장의 계약 경로 · zsh 함정"
slug: skill-notes-contract-path-zsh
created: "2026-09-26 18:09"
complexity: "단순"
conditions: 17
status: done
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:6ec480a47c7e34c0
measurement_digest: sha256:aa2bad33ad1b4ac1
locked_at: "2026-09-26 18:13"
---

## 배경

- **피드백 저장의 계약 경로**: sprint-contract Step 9 는 `bash harness/scripts/save-feedback.sh contract .harness/feedback-draft.yaml` 만 적고,
  "`sprint_slug` · `contract_path` 는 스크립트가 채운다 — 초안에 손으로 적지 마라" 고 한다. 그런데 스크립트는 `HARNESS_CONTRACT` 가 없고 초안에도
  경로가 없으면 경로를 **추측하거나 필드를 뺀다** (`harness/scripts/save-feedback.sh:246-270`). 실측(2026-09-26, 임시 HOME):
  Step 9 명령 그대로 → `contract_path` 필드 없음 + 경고 1 줄. `HARNESS_CONTRACT="$CF"` 를 붙이면 → 정확한 경로 + `contract_path_inferred: false`.
  이 세션에서 슬러그 계약 두 개의 피드백이 이 때문에 경로 없이 저장될 뻔했다.
- **zsh 함정 두 가지**: 스키마 §셸 이식성 규약에는 글로브 · 단어 쪼개기 · 배열 첨자 세 가지만 있다. 2026-09-24 에 실제로 걸린 두 함정이 없다 —
  `$n[^0-9]` 처럼 변수 바로 뒤 `[` 를 zsh 가 첨자로 읽어 명령이 죽는 것, `path` 라는 변수가 명령 검색 경로(`PATH`)를 덮는 것.
- **diff 차이 줄 세기**: `diff a b | wc -l` 은 `1c1` · `---` 머리 줄까지 센다. 바뀐 줄만 세려면 `grep -cE '^[<>]'` 다. 2026-09-26 계약 교차 진단이 짚었다.
- 첫째 항목은 다른 세션(`bda55d45…`)의 넘김 목록 `c2-carryover.md` F1H-39 의 "Step 9 문구" 와 같다. 같은 행의 "`.harness/feedback-draft.yaml` 고정 이름"
  은 평가자 쪽도 함께 바꿔야 하는 일이라 이번에 하지 않는다.

## GAP 분석 (구현 전 점검 · 복잡도)

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 스킬 문서 · 스키마 문서 · 문서 페이지 | 아니오 (문서 한 층) |
| 공개 API·계약 변경 | 스크립트 · 필드 · 함수는 그대로. 안내 문구와 명령 한 줄 | 아니오 |
| 소비면 존재 | 스킬을 따라 쓰는 작성자 | 예 |
| 회귀 위험 | Step 9 명령이 바뀐다 — 잘못 쓰면 피드백 저장이 깨진다 | 예 |

2 축 예 → 규칙상 최소 중간이지만, 바꾸는 것이 명령 한 줄과 안내 문장 넷이고 코드 · 스크립트는 그대로라 조건 수는 단순 규모로 둔다.
회귀 위험은 SK-01 이 Step 9 명령을 원문 그대로 실행해 막는다.

**편집 전 점검 (Step 1.4)**

| 대상 파일 | 읽은 자리 | 지금 상태 | 조건화 |
| --- | --- | --- | --- |
| `harness/skills/sprint-contract/SKILL.md` | `:48` 경계값 측정 Gotcha · `:64` 글로빙 Gotcha · Step 9 (`### 9. 피드백 저장`) | `HARNESS_CONTRACT` 0 건 · diff 줄 세기 0 건 | SK-01 ~ SK-03 |
| `harness/scripts/save-feedback.sh` | `:11-22` 머리 설명 · `:234-270` 경로 결정 | `HARNESS_CONTRACT` → 초안 → 슬러그 → 추측 순. 이번에 안 고친다 | 배경 |
| `harness/references/contract-schema.md` | `:78-106` §셸 이식성 규약 (글머리 5 개) | `${n}` 0 건 · `PATH` 0 건 | AR-01 |
| `docs/harness/contract-schema.html` | `id="shell"` 절 (`<li>` 4 개) | `${n}` 0 건 | AR-02 |

## 범위 경계

- **하지 않는 것**: `save-feedback.sh` 동작은 바꾸지 않는다. 초안 고정 이름(`.harness/feedback-draft.yaml`)은 그대로 둔다 (위 배경).
  평가자(`qa-evaluator.md`)의 피드백 저장 절은 이번 범위 밖이다.
- 다른 세션 가지 `chore/after-kaizen-0926`(합치기 전)은 `SKILL.md` 6 단계 근처에 한 줄을 더했다. 이번 변경은 Gotchas 두 줄과 Step 9 라 겹치지 않는다.

### 봉인 전 실측값 (2026-09-26 18:3x, 기준 커밋 6ad3cbc)

- `bash $M/step9_probe.sh harness/skills/sprint-contract/SKILL.md` → `saved=yes` · `contract_path 없음` · `warnings=1`
- 같은 도구에 Step 9 명령 앞에 `HARNESS_CONTRACT="$CF"` 를 붙인 사본(`$M/skill_hc.md`)을 주면 → `contract_path: '…/sprint-contract-measurement-digest-seal.md'` · `contract_path_inferred: false` · `warnings=0`.
  명령을 bash 코드 블록으로 옮긴 사본(`$M/skill_block.md`)도 같은 결과
- 알려진 답: `zsh -c 'n=3; echo "x $n[^0-9]"'` → `bad math expression` · `zsh -c 'n=3; echo "x ${n}[^0-9]"'` → `x 3[^0-9]` ·
  `zsh -c 'path=/tmp; tail -n1 /etc/hosts'` → `command not found: tail` (bash 는 정상) · `diff <(printf 'a\nb\n') <(printf 'a\nc\n')` 를 `wc -l` 로 세면 4, `grep -cE '^[<>]'` 로 세면 2
- 절 자르기 기준값: 스키마 §셸 이식성 글머리(`^- `) 5 · `${n}` 0 · `PATH` 0, HTML `id="shell"` 절 `<li>` 4 · `${n}` 0, SKILL Gotchas 의 `grep -cE '^[<>]'` 0
- 마크다운 경고(markdownlint-cli2 0.23.2, MD013 끔): `SKILL.md` 9 · `contract-schema.md` 8. `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` → `1/1 PASS`

### 공통 정의

- `$M` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0/scratchpad/mds`
- **Step 9 실행**: `bash $M/step9_probe.sh <SKILL.md>` — Step 9 절에서 `save-feedback.sh contract` 가 든 첫 줄을 원문 그대로 뽑아(인라인 백틱이면 그 안,
  코드 블록 줄이면 앞 공백만 벗김), 초안 경로만 임시 파일로 바꾸고 `CF` 를 슬러그 계약으로, `HOME` 을 임시 폴더로 두고 실행한다.
  저장 여부 · `contract_path` 줄 · 경로 경고 수를 낸다. 이 세션 임시 폴더가 사라져도 재현할 수 있게 원문을 아래에 싣는다 (`draft_fixture.yaml` 포함)

  ```bash
  # 사용: bash step9_probe.sh <SKILL.md> — Step 9 의 save-feedback.sh 명령을 원문 그대로(초안 경로만 임시로), 임시 HOME 에서 슬러그 계약으로 실행
  SK=$(cd "$(dirname "${1}")" && pwd)/$(basename "${1}"); M=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0/scratchpad/mds
  cd /Users/jackson/Hub/10_Dev/claude-plugins
  CF=$PWD/.harness/sprint-contract-measurement-digest-seal.md
  RAW=$(awk '/^### 9\. 피드백 저장/{s=1} s&&/^### 10\./{exit} s' "$SK" | grep -m1 'save-feedback\.sh contract')
  case "$RAW" in
    *'`'*) LINE=$(printf '%s' "$RAW" | sed -E 's/^[^`]*`([^`]*save-feedback\.sh contract[^`]*)`.*$/\1/') ;;
    *)     LINE=$(printf '%s' "$RAW" | sed -E 's/^[[:space:]]+//') ;;
  esac
  [ -n "$LINE" ] || { echo "STOP Step 9 저장 명령 없음"; exit 2; }
  echo "LINE: $LINE"
  T=$(mktemp -d); mkdir -p "$T/home"; cp "$M/draft_fixture.yaml" "$T/draft.yaml"
  RUN=$(printf '%s' "$LINE" | sed "s#\.harness/feedback-draft\.yaml#$T/draft.yaml#")
  OUT=$(CF="$CF" HOME="$T/home" bash -c "$RUN" 2>"$T/err" | tail -1)
  if [ -f "$OUT" ]; then echo "saved=yes"; grep -E '^contract_path(_inferred)?:' "$OUT" || echo "contract_path 없음"; else echo "saved=no $(tail -1 "$T/err")"; fi
  echo "warnings=$(grep -c 'WARNING: contract_path' "$T/err")"; rm -rf "$T"
  ```

  ```yaml
  schema_version: 1
  timestamp: "2026-09-26T18:30:00+09:00"
  project_hash: "1a3bcba6"
  project_name: "claude-plugins"
  skill: sprint-contract
  skill_version: "0.15.0"
  outcome: completed
  contract:
    condition_count: 1
    category_count: 1
    category_coverage: 1.0
    anti_pattern_count: 0
    complexity: simple
  diagnosis:
    checklist:
      ambiguous_conditions: false
    cross_diagnosis_by: qa-evaluator
    cross_diagnosis_notes: "시험용"
    improvement_suggestions: []
  regression_link: null
  user_rating: null
  user_comment: null
  ```

- **마크다운 경고 도구**: `$M/../mdlint` 가 없으면 `npx -y markdownlint-cli2@0.23.2` 에 `{"config":{"MD013":false}}` 설정 파일을 준다
- **절 자르기**: 스키마 §셸 이식성 = `awk '/^### 셸 이식성 규약/{p=1;next} p&&/^### /{exit} p'`, HTML = `awk '/id="shell"/{p=1} p&&/<h3 class="sub"/&&!/id="shell"/{exit} p'`,
  SKILL Gotchas = `awk '/^## Gotchas/{p=1;next} p&&/^## /{exit} p'`
- **변경 파일 구간**: 기준 `6ad3cbc`, 상한 `B=$(git rev-parse --verify -q origin/feat/skill-notes-contract-path-zsh || git rev-parse feat/skill-notes-contract-path-zsh)`.
  합친 뒤 가지가 지워졌으면 병합 커밋의 둘째 부모 (`git log --merges --format=%P -1 --grep=skill-notes-contract-path-zsh main | cut -d' ' -f2`)

## Skill
- [ ] SK-01: Given Step 9 의 저장 명령 · When 슬러그 계약 경로를 `CF` 에 두고 원문 그대로 실행하면 · Then 저장된 피드백에 그 계약의 `contract_path` 가 들어가고 `contract_path_inferred: false` 이며 경로 경고가 0 줄이다 [exact]
      (측정: `bash $M/step9_probe.sh harness/skills/sprint-contract/SKILL.md` 출력이 `saved=yes` · `contract_path: '/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-measurement-digest-seal.md'` ·
       `contract_path_inferred: false` · `warnings=0`.
       음성 대조: 기준 판(6ad3cbc) 스킬로 돌리면 `contract_path 없음` · `warnings=1` — 봉인 전 실측)
- [ ] SK-02: Given Step 9 절 · Then 계약 경로를 `HARNESS_CONTRACT` 로 넘겨야 채워지고, 빼면 스크립트가 경로를 추측하거나 필드를 뺀다는 이유가 한 문장 이상 적혀 있다 [exact]
      (측정: `awk '/^### 9\. 피드백 저장/{p=1} p&&/^### 10\./{exit} p' harness/skills/sprint-contract/SKILL.md` 에서 `HARNESS_CONTRACT` ≥ 2 줄(명령 줄 + 설명 줄) ·
       `추측` 또는 `뺀다` ≥ 1)
- [ ] SK-03: Given SKILL Gotchas · Then 경계값 측정 Gotcha 에 두 파일의 차이 줄 수는 `grep -cE '^[<>]'` 로 센다는 문장이 있고, 글로빙 Gotcha 가 나머지 zsh 함정을 스키마 §셸 이식성 규약으로 가리킨다 [exact]
      (측정: Gotchas 절 자르기에서 `경계값 조건` 이 든 항목 줄(기준 1 줄)에 `grep -cF "grep -cE '^[<>]'"` = 1 ·
       `파일을 글로빙으로 열거하지 마라` 가 든 항목 줄(기준 1 줄)에 `grep -c '셸 이식성 규약'` = 1. 기준 판은 둘 다 0)
- [ ] SK-04: Given 바뀐 스킬 본문 · Then 인자 치환 검사(V9)가 통과한다 [exact]
      (측정: `python3 scripts/validate-plugin.py harness` 의 `V9 arg-substitution` 줄이 `OK`)

## Script
- [ ] SC-00: N/A (스크립트를 바꾸지 않는다 — `save-feedback.sh` 는 그대로다. 측정: 변경 파일 구간에 `harness/scripts/` 0 줄)

## Error
- [ ] ER-01: Given 문서에 새로 적은 세 함정 · When 문서에 적힌 예를 그대로 돌리면 · Then 문서가 말한 결과가 나온다 — `$n[` 는 zsh 에서 실패, `${n}[` 는 성공, `path` 변수 뒤 `tail` 이 zsh 에서 실패, 차이 줄 세기는 2 와 4 [exact]
      (측정: 봉인 전 실측값 절의 알려진 답 네 명령을 zsh · bash 로 다시 돌려 같은 결과. 스키마 · SKILL 에 적은 예가 이 네 명령과 같은 모양인지 눈으로 대조)

## Architecture
- [ ] AR-01: Given 스키마 §셸 이식성 규약 · Then 글머리가 둘 늘어 `$변수` 바로 뒤 `[` 는 `${n}` 처럼 감싸라는 규칙과 `path` 라는 변수 이름을 쓰지 말라는 규칙이 있고, 각각 실측 날짜가 붙어 있다 [exact, enumerated]
      (측정: 절 자르기에서 `grep -c '^- '` = 7 (기준 5) · `${n}` 이 든 글머리와 `PATH` 가 든 글머리가 서로 다른 줄로 시작한다 ·
       `grep -c '2026-09-24'` ≥ 3 (기존 배열 첨자 1 + 새 글머리 2). 기준 판 `${n}` 0 · `PATH` 0 · 날짜 1)
- [ ] AR-02: Given `docs/harness/contract-schema.html` 의 `id="shell"` 절 · Then 같은 두 규칙이 `<li>` 둘로 더해져 6 개다 [exact]
      (측정: HTML 절 자르기에서 `grep -c '<li>'` = 6 · `grep -cF '${n}'` ≥ 1 · `grep -c 'PATH'` ≥ 1. 기준 판 `<li>` 4)
- [ ] AR-03: Given 이 스프린트의 커밋이 끝난 뒤 · When `git diff --name-only 6ad3cbc "$B" -- . ':(exclude).harness'` 를 정렬하면 · Then 정확히 3 경로다 [exact, enumerated]
      (`docs/harness/contract-schema.html` · `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md`)

## Anti-patterns
- [ ] AP-03: 새 코드 블록을 넣으면 여는 줄에 언어 표시가 있다 — 판정은 V6 [exact]
      (측정: `python3 scripts/validate-plugin.py harness` 의 `V6 code-fence` 줄이 `0 bare — OK`)
- [ ] AP-04: 스킬 frontmatter `name` 이 그대로다 — 판정은 V1 [exact]
      (측정: 같은 명령의 `V1 frontmatter` 줄이 `9 skills + 1 agent — OK`)

## Reusability
- [ ] RE-01: N/A (재사용 단위 코드를 만들지 않는다 — 바뀌는 것은 문서 세 개. 측정: AR-03 의 3 경로가 전부 `.md` · `.html`)
- [ ] RE-02: zsh 함정 규칙은 스키마 §셸 이식성 한 곳에만 적고 SKILL 은 그 절을 가리킨다 [exact]
      (측정: `grep -cF '${n}' harness/skills/sprint-contract/SKILL.md` 가 기준 판과 같다 — 기준 판 값은 봉인 전에 잰 0)

## Diagnostics
- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 scripts/release.sh 만 잰다 — 변경 3 경로와 교집합 0 개. 측정: AR-03 목록에 `scripts/release.sh` 0 줄)
- [ ] DG-02: 바꾼 마크다운 2 개의 경고 수가 기준값보다 늘지 않는다 [exact, enumerated]
      (측정: `$M/../mdlint/node_modules/.bin/markdownlint-cli2 --config $M/../mdlint-config.jsonc <파일>` 출력에서 `MD[0-9]` 가 있는 줄 수. 기준값 `SKILL.md` 9 · `contract-schema.md` 8)
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` 로 릴리스 스크립트만 돈다 — 변경 3 경로와 교집합 0 개. 측정: DG-01 과 같음)
- [ ] DG-04: 바꾼 HTML 페이지가 접근성 검사를 통과하고 플러그인 검사가 통과한다 [exact]
      (측정: `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` → `1/1 PASS` · `python3 scripts/validate-plugin.py harness` → Exit 0)
