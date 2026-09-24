---
feature: "검사 개수를 지시문에서 떼어내고 표 무결성 검사를 추가"
slug: check-count-decouple-and-table-gate
created: "2026-09-24 11:20"
complexity: "복잡"
conditions: 19
status: done
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:a20475c34c7fb7a2
locked_at: "2026-09-24 11:10"
---

## 배경

앞 스프린트가 남긴 거리 중 둘을 고친다. 하나는 순서상 다른 하나의 선행 작업이다.

**거리 1 — 마크다운 경고 수가 문서 구조 붕괴에 둔감하다.** 앞 스프린트에서 문서에 절을 끼워
넣어 표를 끊었는데 경고 수가 그것을 잡지 못했다. 실측: 같은 파일을 세 커밋에서 재니 **세 번 다
14 건**이었다 — 167 줄을 넣고 표를 깨고 다시 고치는 동안 숫자가 1 도 안 움직였다. 헤더 없는
고립 표 행은 표로 인식되지 않아 규칙이 적용되지 않는다. 그래서 고립 표 행을 직접 세는 검사가
필요하다.

**거리 2 (선행) — 지시문이 검사 개수를 하드코딩한다.** 그 검사를 `validate-plugin.py` 에 V10 으로
넣으면 **검사 개수가 박힌 19 개 파일이 또 어긋난다.** 이 세션의 첫 스프린트가 바로 그 표기를
`8 카테고리 · V1~V8` 에서 `9 카테고리 · V1~V9` 로 고친 작업이었다. V10 을 넣으면 같은 일을 또
해야 한다. 근본 원인은 지시문이 개수를 적는다는 것이고, 첫 스프린트가 얻은 교훈
("개수를 조건 줄에 박지 마라 · 열거한 목록을 세어 얻게 한다")이 지시문에는 적용되지 않았다.

그래서 **개수 표기를 먼저 없앤 뒤 V10 을 넣는다.** 그러면 V11 이 와도 지시문을 안 고친다.

**거리 3 (곁가지) — 문서가 `--merge` 만 쓰라고 해서 필요 이상으로 좁다.** 교차 진단이 임시
복제본에서 세 병합을 실제로 해보니 재배치도 봉인 커밋의 파일 1 개를 지킨다. 재배치의 위험은
다른 데 있다 — `main` 이 앞서 있으면 커밋 해시가 바뀌어 리포트에 인용한 해시가 `main` 의
조상이 아니게 된다 (기능은 살고 인용만 죽는다). 이 구별을 적는다.

**참고**: 스쿼시 병합은 이번 세션에 레포 설정으로 껐다 (`allow_squash_merge=false`, 사용자 승인).
그래서 문서 경고에만 의존하지 않는다.

## 리서치 소스

- `.harness/sprint-amendments-seal-commit-and-evidence-boundary.md` — 남은 거리 4 건의 근거
- `scripts/validate-plugin.py:512-570` — V6 의 파일 범위 (V10 의 참고 형태)
- `scripts/validate-plugin.py:765-773` — 등록 키 표
- `harness/docs/guides/plugin-validation-guide.md` §7.5 — "새 카테고리는 V10~ 로 추가" (첫
  스프린트가 고쳐 둔 것)
- 앞 스프린트 AR-03 의 고립 표 행 검사 스크립트 (양성 대조까지 확인된 상태)

## 범위 경계

### 설계 결정

**지시문에서 개수와 범위를 빼고 "등록된 검사 전부" 로 바꾼다.** 구체적 형태:

| 지금 | 바꾼 뒤 |
| --- | --- |
| `9 카테고리(V1~V9) 상태를 확인하라` | `등록된 검사 전부의 상태를 확인하라` |
| `9 카테고리 (V1~V9: frontmatter / templates / …)` | `등록된 검사 전부 (목록은 아래 명령으로 얻는다)` |
| `V1~V9 전부 OK 여야 한다` | `등록된 검사 전부 OK 여야 한다` |

검사 이름을 열거한 자리는 **열거를 지우고 명령으로 얻게** 한다.

```bash
grep -oE '"[a-z-]+": check_v[0-9]+' scripts/validate-plugin.py | sed -E 's/"([a-z-]+)".*/\1/'
```

**개수를 아예 안 적는 것이 목표다.** "9 개" 를 "10 개" 로 바꾸는 것이 아니다 — 그러면 V11 에서
같은 일이 또 생긴다. 기준 문서(`plugin-validation-guide.md`)만 예외다. 그 문서는 각 검사를
정의하는 자리라 번호가 본문이다 — 거기서는 개수를 적되 **한 곳에만** 두고 나머지는 그 문서를
가리킨다.

**V10 의 대상 범위는 V6 보다 넓다.** V6 은 `skills/*/SKILL.md` · `agents/*.md` ·
`references/*.md` · 킷 루트 `README.md` 를 본다. 표가 끊긴 자리는 `harness/docs/guides/` 였고
그건 V6 범위 밖이다. V10 은 거기에 킷 안의 `docs/**/*.md` 를 더한다 — 실측 210 파일.

**오탐 0 을 확인한 뒤에 넣는다.** 앞 스프린트 AR-03 의 스크립트를 210 파일 전부에 돌려 고립
0 을 확인했다 (작성 시점 실측). 오탐이 나면 검사가 정상 작업을 막고, 우회된 검사는 없는 것보다
나쁘다.

**고치는 파일 21 개** — 개수 표기 19 개 + `validate-plugin.py` + `sprint-contract/SKILL.md`.

```text
.claude/skills/backend-kaizen/SKILL.md
.claude/skills/bambu-kaizen/SKILL.md
.claude/skills/design-kaizen/SKILL.md
.claude/skills/infra-kaizen/SKILL.md
.claude/skills/onboarding-kaizen/SKILL.md
.claude/skills/planning-kaizen/SKILL.md
.claude/skills/react-kaizen/SKILL.md
.claude/skills/rust-kaizen/SKILL.md
.claude/skills/tone-kaizen/SKILL.md
.claude/skills/tone-research/SKILL.md
CLAUDE.md
README.md
flutter-toolkit/skills/flutter-kaizen/SKILL.md
harness/docs/guides/plugin-validation-guide.md
harness/skills/contract-kaizen/SKILL.md
harness/skills/create-skill/SKILL.md
harness/skills/evaluator-kaizen/SKILL.md
harness/skills/harness-kaizen/SKILL.md
harness/skills/init/SKILL.md
harness/skills/sprint-contract/SKILL.md
scripts/validate-plugin.py
```

**범위 밖** — 남은 거리 하나(측정 명령이 조건 둘째 줄부터라 봉인에 안 덮인다)는 하위 호환
문제가 있어 별 스프린트로 남긴다. `conditions_digest` 의 해싱 범위를 넓히면 기존 계약 62 개가
전부 `SEAL_BROKEN` 이 된다. 새 필드를 두는 설계가 필요하다. 옛 기록(`.harness/` ·
`docs/kaizen/` · `harness/evals/`)과 플러그인 배포도 범위 밖이다.

### 봉인 전 실측한 기준값

- 개수 표기가 있는 파일 **19 개**, 그 안의 줄 **35 줄** (`9 카테고리|9-카테고리|V1~V9|V1-V9`)
- `validate-plugin.py` 의 등록 검사 **9 개** (`frontmatter` `templates` `refs` `triggers`
  `placeholders` `code-fence` `plugin-json` `hook-exec` `arg-substitution`)
- `check_v10` · `table-integrity` 등장 — **0 건**
- `gh pr merge --merge` 만 적힌 자리 — `sprint-contract/SKILL.md` **1 곳**
- `python3 scripts/validate-plugin.py` — **14 plugins, 14 OK · Exit: 0**
- V10 후보 대상 **210 파일**, 고립 표 행 **0** (오탐 0 — 작성 시점 전수 실측)
- 편집기와 같은 조건의 마크다운 경고 — 대상 `.md` 20 개 합 **347 건 · (파일,규칙) 조합 49 개**
- 기준 커밋 — `c0e12a8`

### 측정 환경 주의

이 맥의 `grep` 은 ugrep 7.8.4 로 `-r` 출력에 `./` 접두를 붙이지 않는다. 셸 변수를 따옴표 없이
펼치면 zsh 가 쪼개지 않아 파일을 못 찾고 `2>/dev/null` 이 그 오류를 삼켜 조용히 0 이 된다.
여러 파일은 목록을 파일에 담아 `while read` 로 돌린다.

문서에 절을 끼워 넣을 때는 표·목록 중간에 들어가지 않는지 삽입 전후로 뼈대를 찍어 비교한다.
이번에 추가하는 V10 이 바로 그 검사다 — **자기 자신에게 먼저 돌린다.**

### 상한 ref 해석

```bash
sprint_head() {
  m=$(git log --merges --format=%H --grep="from joo6077/feat/${1}" -1)
  [ -n "$m" ] && { echo "$m"; return 0; }
  git rev-parse --verify -q "feat/${1}" && return 0
  echo "UNRESOLVED feat/${1}" >&2; return 1
}
SH=$(sprint_head check-count-decouple-and-table-gate) || exit 1
[ "$SH" = "$(git rev-parse c0e12a8)" ] && { echo "STALE_HEAD"; exit 1; }
```

### 커버리지 해소

커버리지 해소: SK-01 · AR-01 — 산문의 21 개 경로를 측정 절이 같은 표기로 열거한다.
커버리지 해소: SC-01 — 등록 키 9 개를 명령으로 얻어 대조하므로 열거하지 않는다 (의도된 형태).
커버리지 해소: AR-03 — 손대지 않을 것을 경로 패턴 3 종으로 덮는다.

## Skill

- [ ] SK-01: 위 21 개 파일 중 **기준 문서를 뺀 20 개**에 개수·범위 표기가 0 줄이다
      [exact, enumerated]
      (기준 문서 `harness/docs/guides/plugin-validation-guide.md` 는 각 검사를 정의하는
      자리라 번호가 본문이므로 예외다 ·
      측정: 아래 명령의 `총=` 이 0. `grep -c` 는 매치 없으면 종료 코드 1, 오류면 2 —
      삼키지 않는다)

      ```bash
      T=0; C=0
      while IFS= read -r f; do
        [ "$f" = "harness/docs/guides/plugin-validation-guide.md" ] && continue
        [ "${f##*.}" = "py" ] && continue
        C=$((C+1))
        n=$(grep -c '9 카테고리\|9-카테고리\|V1~V9\|V1-V9' "$f"); rc=$?
        [ $rc -ge 2 ] && { echo "ERR $f rc=$rc"; exit 2; }
        [ $rc -eq 1 ] && n=0
        [ "$n" -gt 0 ] && echo "$f:$n"
        T=$((T+n))
      done <<'EOF'
      (위 범위 경계의 21 개 경로)
      EOF
      echo "총=$T 대상=$C"
      ```

      양성 대조: 고치기 전 같은 명령은 **19 개 파일에서 35 줄**을 잡는다 (작성 시점 실측.
      기준 문서를 빼면 그보다 적다 — 고친 뒤 0 이면 된다). 0 이면 측정이 죽은 것이다.

- [ ] SK-02: 검사 목록을 얻는 **명령**이 지시문에 실려 있다 [structural, enumerated]
      (개수를 적는 대신 명령으로 얻게 하는 것이 이번 변경의 요지다 ·
      측정: 개수 표기를 지운 파일 중 검사 이름을 열거했던 곳에
      `grep -Fc 'check_v[0-9]'` 또는 `grep -Fc 'validate-plugin.py 가 등록한'` 이 1 이상.
      **최소 3 개 파일**에 들어가야 한다 — 전부에 명령을 싣는 것은 중복이므로 요구하지 않는다)

- [ ] SK-03: `sprint-contract/SKILL.md` 의 병합 방식 서술이 재배치도 인정하고 그 위험을
      구별한다 [exact]
      (측정: 그 파일에 `grep -Fc '재배치'` 가 1 이상이고, 같은 문맥에 `main 이 앞서` 또는
      `해시가 바뀌` 가 있다 — 재배치는 파일 1 개를 지키지만 인용한 해시가 죽는다)

      양성 대조: 고치기 전 `재배치` 는 그 파일에 **0 건**이다 (작성 시점 실측).

## Script

- [ ] SC-01: `scripts/validate-plugin.py` 에 표 무결성 검사가 **V10 으로** 등록됐고 돌아간다
      [exact]
      (측정: (a) `grep -c 'def check_v10' scripts/validate-plugin.py` 가 1
      (b) 등록 표에 그 키가 있다 — `grep -oE '"[a-z-]+": check_v10'` 가 1 건
      (c) `python3 scripts/validate-plugin.py --check=<그 키>` 가 전 킷 OK)

      양성 대조: 고치기 전 `check_v10` 은 **0 건**이다. 그리고 그 검사가 살아 있는지는
      앞 스프린트가 확인한 방식으로 본다 — `git show ac77cdc:harness/references/contract-schema.md`
      를 임시 파일로 떠서 같은 판정을 걸면 고립 **1 개**(1036 줄)가 나온다.

- [ ] SC-02: `python3 scripts/validate-plugin.py` 전체가 **14 plugins, 14 OK · Exit: 0** 이다
      [goal]
      (V10 이 늘어도 전 킷이 통과해야 한다. 오탐이 나면 검사가 정상 작업을 막는다 ·
      측정: 그 명령의 마지막 두 줄)

      음성 대조: `git show ac77cdc:harness/references/contract-schema.md` 를 킷 안 경로에
      임시로 놓고 돌리면 V10 이 FAIL 하고 `14 OK` 가 깨진다. 확인 뒤 지운다.

## Error

- [ ] ER-01: V10 의 대상 범위가 **V6 보다 넓고** 그 이유가 적혀 있다 [exact]
      (표가 끊긴 자리는 `harness/docs/guides/` 였고 V6 범위 밖이다 ·
      측정: `def check_v10` 절에 `docs` 를 포함하는 파일 수집이 있고
      (`grep -c "docs" ` 가 1 이상), 기준 문서의 V10 절에 그 이유가 적혀 있다)

- [ ] ER-02: 개수 표기를 지운 자리가 **"등록된 검사 전부"** 같은 개수 없는 표현으로 바뀌었다
      [exact]
      (개수를 9 에서 10 으로 바꾸는 것이 아니다 — 그러면 V11 에서 같은 일이 또 생긴다 ·
      측정: 대상 20 개 파일에 `grep -c '10 카테고리\|V1~V10\|V1-V10'` 이 **0**.
      개수를 새로 박지 않았는지 보는 조건이다)

      양성 대조: 이 측정은 "새 개수를 박았는가" 를 잡는다. 일부러 한 파일에
      `10 카테고리 (V1~V10)` 을 임시로 넣으면 1 이 나온다 — 봉인 전에 임시 사본으로 확인한다.

## Architecture

- [ ] AR-01: 이 스프린트의 변경 파일이 위 21 개 경로와 정확히 일치한다 [exact, enumerated]
      (Given: 이 스프린트의 커밋이 끝난 뒤 · **`STALE_HEAD` 확인을 먼저 통과** ·
      측정: `git diff --name-only c0e12a8..$(sprint_head check-count-decouple-and-table-gate) --
      . ':(exclude).harness/**'` 의 출력이 21 행이고 각 줄이 위 목록에 있다)

- [ ] AR-02: 기준 문서가 **개수를 적는 유일한 자리**가 됐다 [exact]
      (다른 파일은 그 문서를 가리킨다 ·
      측정: `harness/docs/guides/plugin-validation-guide.md` 에 `10 카테고리` 또는
      `V1~V10` 이 1 이상이고, 그 문서 밖 20 개 파일에는 0 이다 (ER-02 와 같은 측정))

- [ ] AR-03: 손대지 않기로 한 것이 변경되지 않았다 [exact]
      (Given: 위와 같음 ·
      측정: 같은 구간에서 (i) `harness/evals/` 0 행 (ii) `docs/kaizen/` 0 행
      (iii) `.harness/sprint-contract*.md` 에 `verify_seal` 을 돌려 `SEAL_BROKEN` 0 개
      (`SEAL_OK` 와 `SEAL_ABSENT` 는 둘 다 통과 · `-maxdepth` 를 걸지 않는다))

      양성 대조: (iii) 은 작성 시점에 전체에 돌려 `SEAL_BROKEN` 0 을 확인한다. 경로 패턴
      2 종은 `git ls-files` 에 걸면 1 이상이 나온다. 총수는 산출물 추가로 달라지므로 고정하지 않는다.

- [ ] AR-04: **이 계약 자신이 봉인 커밋 절차를 따랐다** [exact]
      (앞 스프린트가 만든 Step 6.7 이다 ·
      측정: `git log --diff-filter=A --format='%h' --
      .harness/sprint-contract-check-count-decouple-and-table-gate.md` 로 첫 커밋을 찾고,
      `git show --name-only --format='' <해시>` 의 파일 수가 **1** 이다.
      병합은 `--merge` 또는 `--rebase` 로 한다 — 스쿼시는 레포 설정으로 껐다)

      양성 대조: 앞 스프린트 계약 3 건에 같은 측정을 걸면 파일 수가 20 · 10 · 5 다.
      1 이 아니면 절차를 안 따른 것이므로 구별력이 있다.

## Anti-patterns

- [ ] AP-03: bare code fence 0 건 — 여는 fence 에 언어 힌트가 있다
      (유효 대상은 21 개 중 V6 이 보는 것들이다 — `harness/skills/*/SKILL.md` 6 개 와
      `flutter-toolkit/skills/flutter-kaizen/SKILL.md`. `.claude/skills/` · 레포 루트 ·
      `harness/docs/` · `scripts/` 는 V6 범위 밖이다 ·
      측정: `python3 scripts/validate-plugin.py --check=code-fence` 가 전 킷 OK)

      양성 대조: 그 7 개 중 코드 블록이 있는 파일이 1 개 이상임을 봉인 전에 실측한다.

- [ ] AP-04: frontmatter 가 보존됐다 — V1 FAIL 0 건
      (유효 대상은 V1 이 보는 `skills/*/SKILL.md` 7 개 ·
      측정: `python3 scripts/validate-plugin.py --check=frontmatter` 가 전 킷 OK)

## Reusability

- [ ] RE-01: `validate-plugin.py` 의 V10 이 기존 검사와 같은 형태를 따른다 (새 틀을 만들지
      않았다) [structural]
      (측정: `def check_v10(ctx: CheckContext) -> CheckResult:` 시그니처가 V6 · V9 와 같고,
      `CheckResult` 를 돌려주며 `ctx.read` 를 쓴다 — `grep -c 'ctx.read\|CheckResult'` 가
      그 함수 안에서 1 이상)
- [ ] RE-02: 표 무결성 판정 코드를 계약·문서에 복제하지 않고 `validate-plugin.py` 한 곳에 뒀다
      [structural]
      (앞 스프린트는 그 스크립트를 계약 본문에만 뒀다. 이번에 코드로 옮기는 것이 요지다 ·
      측정: 그 판정 논리가 `scripts/validate-plugin.py` 에 있고, 기준 문서는 그것을 **가리키기만**
      한다 — 기준 문서에 `def ` 로 시작하는 파이썬 함수 정의가 0 개)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 로 그 한 파일만 잰다 —
      이번 변경 파일과 교집합 0 개. 측정: AR-01 의 21 행에
      `grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 편집기와 같은 조건으로 잰 마크다운 경고가 기준값을 넘지 않는다
      (기준 347 건 · (파일,규칙) 조합 49 개 · 대상은 21 개 중 `.md` **20 개** —
      `scripts/validate-plugin.py` 는 마크다운이 아니라 제외 ·
      측정: scratchpad 에 `npm install --no-save markdownlint-cli2@0.23.2` 후 설정
      `{"config":{"MD013":false}}` 로 20 개를 돌린다. 총 건수 ≤ 347 이고, 출력을
      `파일 규칙ID` 로 정규화해 `sort | uniq -c` 한 집계에서 기준보다 건수가 늘어난 조합이 0 개.
      **이 조건은 SC-01 을 대신하지 못한다** — 앞 스프린트에서 표가 끊긴 동안 이 수치는 세 커밋
      내리 같았다. 그것이 V10 을 만드는 이유다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 로 그 한 파일만
      돌린다 — 이번 변경 파일과 교집합 0 개. 측정: DG-01 과 같음)
- [ ] DG-04: N/A (산출물에 구동할 앱·서버가 없다. 측정: 변경 파일에 실행 진입점 0 개 —
      `validate-plugin.py` 는 기존 스크립트의 수정이고 새 진입점이 아니다).
      이 자리에 실제로 성립하는 검사는 SC-02 다
