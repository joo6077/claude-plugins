---
feature: "검사 카테고리 수 표기 V1~V9 동기화"
slug: validate-check-count-sync
created: "2026-09-22 11:30"
complexity: "중간"
conditions: 17
status: active
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:b846c6001c1f0180
locked_at: "2026-09-22 14:46"
---

## 배경

`scripts/validate-plugin.py` 는 검사 9종(V1~V9)을 등록해 실행한다. 기준 문서
`harness/docs/guides/plugin-validation-guide.md` 본문도 이미 9-카테고리로 고쳐졌다.
그런데 그 문서를 카테고리 수의 기준으로 지목하는 살아 있는 지시문 18개 파일 32줄이
아직 `8 카테고리` · `V1~V8` 로 남아 있다. 지시문을 읽고 일하는 다음 세션은 V9
(`arg-substitution` — 스킬 본문의 인자 치환 위험)를 확인하지 않고 "전부 OK" 라고 보고한다.

기준 문서 자체에도 같은 뿌리의 어긋남 3곳이 있다 — V9 를 이미 쓰면서 §7.5 는 "새 카테고리는
V9~ 로 추가" 라 하고, §8 "다음 갱신 예정" 이 이미 쓰인 V9 번호를 다시 쓰며, 변경 이력에 V9
도입 행이 없다. 기준이 어긋난 채로 두면 다음에 같은 일이 또 생긴다.

이번 스프린트는 문구만 고친다. `validate-plugin.py` 의 동작과 검사 내용은 바꾸지 않는다.

## 리서치 소스

- `scripts/validate-plugin.py:765-773` — 실제 등록된 검사 9종과 그 키 이름
- `scripts/validate-plugin.py:512-570` — V6 가 보는 파일 범위 (`skills/*/SKILL.md` ·
  `agents/*.md` · `references/*.md` · 킷 루트 `README.md`. **`docs/` 는 보지 않는다**)
- `harness/docs/guides/plugin-validation-guide.md:64-423` — 카테고리 정의 9종
- 이 레포 관례: 브랜치 `feat/<slug>`, 머지 메시지 `Merge pull request #NN from joo6077/feat/<slug>`

## 범위 경계

**고치는 파일 19개** — 아래 18개 + 기준 문서 1개.

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
harness/skills/contract-kaizen/SKILL.md
harness/skills/create-skill/SKILL.md
harness/skills/evaluator-kaizen/SKILL.md
harness/skills/harness-kaizen/SKILL.md
harness/skills/init/SKILL.md
harness/docs/guides/plugin-validation-guide.md
```

**손대지 않는 파일 292개 (경로 기준)** — 추적 파일 중 `.harness/` 로 시작하는 281개와
`docs/` 로 시작하며 `research-log.md` 로 끝나는 11개. 그때의 사실이라 고치면 기록이 거짓이 된다.

셈법을 섞지 않는다. **경로 기준 292개**가 AR-03 이 재는 집합이다. 그중 옛 표기를 실제로 담은
파일은 **내용 기준 49개**이고 이 값은 참고용이다 — AR-03 의 측정·양성 대조에는 쓰지 않는다.
(교차 진단이 이 혼동을 짚었다: 경로 기준 양성 대조에 내용 기준 값을 적어두면 실행하는 사람이
"패턴이 죽었다" 고 오판한다)

**범위 밖** — `harness`·`flutter-toolkit` 플러그인 버전 올림과 배포. 머지 뒤 main 에서 한다.

### 봉인 전 실측한 기준값

1. 옛 표기 `8 카테고리|8-카테고리|V1~V8|V1-V8` — 대상 19개 파일에서 **32줄**
2. `python3 scripts/validate-plugin.py` 전체 — **14 plugins, 14 OK · Exit: 0**
3. 편집기와 같은 조건의 마크다운 경고 — 대상 19개 파일 합 **337건 · (파일,규칙) 조합 47개**
   (markdownlint-cli2 0.23.2 · `MD013` 끔 — 편집기 확장 `davidanson.vscode-markdownlint-0.62.1`
   이 번들에서 `MD013:!1` 로 끄기 때문)
4. 기준 커밋 — `3498e9edf5301eca527b28266de4d399de6b5e6b`
5. 검사 이름을 8개로 열거한 자리 — **8곳**
6. 기준 문서 V-번호 충돌 — §8 "다음 갱신 예정" 구간으로 좁혀 **1건** (V9).
   문서 전체에 `grep -c 'V9'` 를 걸면 **5건**이라 고친 뒤에도 0 이 될 수 없다 — 구간을 좁혀야 한다
8. 손대지 않을 파일 — 경로 기준 **292개** (`.harness/` 281 + `docs/*/research-log.md` 11)
7. 안티패턴 유효 대상 6개 중 코드 블록이 있는 파일 — `harness/skills/create-skill/SKILL.md`(4) ·
   `harness/skills/init/SKILL.md`(6)

### 측정 환경 주의

이 맥의 `grep` 은 ugrep 7.8.4 이고 `-r` 출력에 `./` 접두를 붙이지 않는다. 경로 패턴에
`^\./` 를 쓰면 매치가 0 이 되어 죽은 측정이 된다. 계약 작성 중 실제로 한 번 겪었다.

### 상한 ref 해석

```bash
sprint_head() {  # sprint_head <slug> — 이 레포 관례(feat/<slug> · PR 머지)
  m=$(git log --merges --format=%H --grep="from joo6077/feat/${1}" -1)
  [ -n "$m" ] && { echo "$m"; return 0; }
  git rev-parse --verify -q "feat/${1}" && return 0
  echo "UNRESOLVED feat/${1}" >&2; return 1
}
```

### 커버리지 해소

커버리지 해소: SK-01 · SK-02 — 산문의 19개 경로를 측정 절이 같은 표기로 열거한다.
커버리지 해소: SC-01 — 산문의 8곳을 측정 절이 파일 경로 8개로 열거한다.
커버리지 해소: AR-03 — 손대지 않을 52개를 경로 패턴 2종(`.harness/` 로 시작 ·
`docs/` 로 시작하며 `research-log.md` 로 끝남)으로 덮는다. 작성 시점에 확장해 52개를 실측했다.
커버리지 해소: AP-03 · AP-04 — 19개 중 검사가 실제로 보는 6개만 대상이다. 나머지 13개는
`.claude/skills/` · 레포 루트 · `docs/` 라서 어떤 자동 검사도 보지 않는다 (V6 범위 참조).

## Skill

- [ ] SK-01: 아래 19개 파일에 옛 표기가 0줄이다 [exact, enumerated]
      (측정: 아래 명령의 `총=` 이 0. `grep -c` 는 매치 없으면 종료 코드 1, 오류면 2 —
      `2>/dev/null` 이나 `|| true` 로 삼키지 않는다. `대상=19` 도 함께 확인한다)

      ```bash
      T=0; C=0
      while IFS= read -r f; do
        C=$((C+1))
        n=$(grep -c '8 카테고리\|8-카테고리\|V1~V8\|V1-V8' "$f"); rc=$?
        [ $rc -ge 2 ] && { echo "ERR $f rc=$rc"; exit 2; }
        [ $rc -eq 1 ] && n=0
        [ "$n" -gt 0 ] && echo "$f:$n"
        T=$((T+n))
      done <<'EOF'
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
      harness/skills/contract-kaizen/SKILL.md
      harness/skills/create-skill/SKILL.md
      harness/skills/evaluator-kaizen/SKILL.md
      harness/skills/harness-kaizen/SKILL.md
      harness/skills/init/SKILL.md
      harness/docs/guides/plugin-validation-guide.md
      EOF
      echo "총=$T 대상=$C"
      ```

      양성 대조: 같은 패턴을 `.harness/history/` 에 걸면 13개 파일에서 매치한다
      (작성 시점 실측). 0 이면 패턴이 죽은 것이다.

- [ ] SK-02: 위 19개 파일 각각에 새 표기(`9 카테고리` · `9-카테고리` · `V1~V9` · `V1-V9`
      중 하나 이상)가 1줄 이상 있다 [structural, enumerated]
      (측정: SK-01 과 같은 루프에서 패턴만
      `9 카테고리\|9-카테고리\|V1~V9\|V1-V9` 로 바꿔 돌려 **19개 전부** 1 이상.
      0 인 파일이 1개라도 있으면 FAIL)

## Script

- [ ] SC-01: 검사 이름을 열거한 8곳 각각에 등록 키 9개가 **전부** 있다 [exact, enumerated]
      (등록 키: `frontmatter` `templates` `refs` `triggers` `placeholders` `code-fence`
      `plugin-json` `hook-exec` `arg-substitution` ·
      대상 8곳: `.claude/skills/bambu-kaizen/SKILL.md` ·
      `.claude/skills/design-kaizen/SKILL.md` · `.claude/skills/infra-kaizen/SKILL.md` ·
      `.claude/skills/onboarding-kaizen/SKILL.md` · `.claude/skills/planning-kaizen/SKILL.md` ·
      `.claude/skills/react-kaizen/SKILL.md`(표 형태) · `.claude/skills/rust-kaizen/SKILL.md` ·
      `.claude/skills/tone-kaizen/SKILL.md` ·
      측정: 아래 블록을 그대로 실행해 `MISSING` 이 0줄.
      이름 하나가 오타면 그 키가 없으므로 이 검사가 잡는다 — 허용 목록 방식이다)

      ```bash
      # 배열을 따옴표로 감싼다. 따옴표 없는 `for k in $KEYS` 는 zsh 에서 단어 분리가
      # 일어나지 않아 루프가 1 회만 돌고 거짓 통과가 난다 (교차 진단에서 실제로 재현됨)
      KEYS=($(grep -oE '"[a-z-]+": check_v[0-9]' scripts/validate-plugin.py \
              | sed -E 's/"([a-z-]+)".*/\1/'))
      echo "키 수=${#KEYS[@]} (9 이어야 한다)"
      FILES=(
        .claude/skills/bambu-kaizen/SKILL.md
        .claude/skills/design-kaizen/SKILL.md
        .claude/skills/infra-kaizen/SKILL.md
        .claude/skills/onboarding-kaizen/SKILL.md
        .claude/skills/planning-kaizen/SKILL.md
        .claude/skills/react-kaizen/SKILL.md
        .claude/skills/rust-kaizen/SKILL.md
        .claude/skills/tone-kaizen/SKILL.md
      )
      echo "파일 수=${#FILES[@]} (8 이어야 한다)"
      for f in "${FILES[@]}"; do
        miss=""
        for k in "${KEYS[@]}"; do
          grep -q -- "$k" "$f" || miss="$miss $k"
        done
        [ -n "$miss" ] && echo "MISSING $f:$miss"
      done
      echo "검사 끝"
      ```

      양성 대조: 고치기 전 이 블록은 8개 파일 전부에서
      `MISSING ... arg-substitution` 을 낸다 (교차 진단 실측). 0 이면 측정이 죽은 것이다.

- [ ] SC-02: `python3 scripts/validate-plugin.py` 전체 실행이 `14 plugins, 14 OK` ·
      `Exit: 0` 이다 [goal]
      (기준값과 같음 — 이 스프린트가 회귀를 만들지 않았음을 뜻한다.
      측정: 그 명령의 마지막 두 줄)

      음성 대조: 대상 파일 중 `harness/skills/init/SKILL.md` 의 여는 fence 에서 언어 힌트를
      지우면 V6 이 FAIL 하고 `14 OK` 가 깨진다. 이 측정은 문서 내용을 직접 읽으므로
      구현을 지워도 통과하는 형태가 아니다.

## Error

- [ ] ER-01: 숫자와 범위가 어긋난 반쪽 치환이 0줄이다 [exact]
      (`9 카테고리 (V1~V8)` 이나 `8 카테고리 (V1~V9)` 처럼 앞 숫자와 V-범위가 다른 형태.
      측정: 위 19개 파일에
      `grep -nE '9[ -]카테고리[^|]{0,12}V1[~-]V8|8[ -]카테고리[^|]{0,12}V1[~-]V9'` 이 0행)

      양성 대조: 작성 시점에 임시 사본에 그 두 형태를 넣어 돌렸더니 2행을 잡았고
      정상 문구 `9 카테고리 (V1~V9)` 는 잡지 않았다. 측정이 살아 있다.

- [ ] ER-02: 기준 문서 안에서 V-번호가 충돌하지 않는다 [exact]
      (§8 "다음 갱신 예정" 이 §3 에 이미 있는 번호를 다시 쓰지 않는다.
      측정: `grep -oE '^### V[0-9]+' <기준문서> | sed 's/### //' | sort -u` 와
      `awk '/다음 갱신 예정/,0' <기준문서> | grep -oE '^- V[0-9]+' | sed 's/^- //' | sort -u`
      를 `comm -12` 로 비교해 교집합 0행)

      양성 대조: 고치기 전 이 측정은 **V9 1건**을 잡는다 (작성 시점 실측).
      0 이면 측정이 죽은 것이다.

## Architecture

- [ ] AR-01: 이 스프린트의 변경 파일이 위 19개 경로와 정확히 일치한다 [exact, enumerated]
      (Given: 이 스프린트의 커밋이 끝난 뒤 ·
      측정: `git diff --name-only 3498e9e..$(sprint_head validate-check-count-sync) --
      . ':(exclude).harness/**'` 의 출력이 19행이고 각 줄이 위 목록에 있다.
      `.harness/` 는 계약·QA 산출물 자리라 제외한다. `UNRESOLVED` 가 나오면 `HEAD` 로
      떨어지지 말고 사용자에게 묻는다)

- [ ] AR-02: 기준 문서 `harness/docs/guides/plugin-validation-guide.md` 의 어긋남 3곳이
      모두 고쳐졌다 [exact, enumerated]
      (측정은 아래 3개를 각각 돌린다. **(b) 는 구간을 좁혀야 한다** — 문서 전체에
      `grep -c 'V9'` 를 걸면 §3 의 정당한 헤더 `### V9 스킬 본문의 인자 치환 위험` 때문에
      고친 뒤에도 5건이 나와 0 이 될 수 없다)

      ```bash
      G=harness/docs/guides/plugin-validation-guide.md

      # (a) §7.5 의 "새 검증 카테고리 도입 시" 줄이 V10 이상을 가리킨다 — 1 이상 기대
      grep -cE '새 검증 카테고리 도입 시.*V1[0-9]' "$G"

      # (b) §8 "다음 갱신 예정" 구간에 §3 이 이미 쓴 번호가 없다 — 0 기대
      awk '/다음 갱신 예정/,0' "$G" | grep -cE '^- V[1-9]:'

      # (b') 같은 구간의 두 항목이 V10 · V11 이다 — 각 1 기대
      awk '/다음 갱신 예정/,0' "$G" | grep -cE '^- V10:'
      awk '/다음 갱신 예정/,0' "$G" | grep -cE '^- V11:'

      # (c) §8 변경 이력 표에 V9 arg-substitution 도입 행이 있다 — 1 이상 기대
      grep -cE '^\| 2026-.*V9 .*arg-substitution' "$G"

      # (c') frontmatter version · last_updated 가 그 행과 맞다 — 눈으로 대조
      sed -n '1,6p' "$G"
      grep -E '^\| 2026-' "$G" | tail -1
      ```

      양성 대조: 고치기 전 (a) 는 0, (b) 는 1(V9), (c) 는 0 이다 (작성 시점 실측).
      고친 뒤 (a) ≥ 1, (b) = 0, (b') 각 1, (c) ≥ 1 이어야 한다.

- [ ] AR-03: 손대지 않기로 한 292개 파일(경로 기준)이 변경되지 않았다 [exact]
      (Given: 이 스프린트의 커밋이 끝난 뒤 ·
      측정: `git diff --name-only 3498e9e..$(sprint_head validate-check-count-sync)` 에서
      (i) `.harness/` 로 시작하는 줄 중 이 스프린트의 산출물 3개
      (`sprint-contract-validate-check-count-sync.md` ·
      `sprint-feedback-validate-check-count-sync.md` ·
      `sprint-amendments-validate-check-count-sync.md`) 를 뺀 나머지가 0행,
      (ii) `docs/` 로 시작하며 `research-log.md` 로 끝나는 줄이 0행.
      `UNRESOLVED` 가 나오면 `HEAD` 로 떨어지지 말고 사용자에게 묻는다)

      양성 대조: **같은 경로 패턴 2종**을 `git ls-files` 전체 목록에 걸면 292행을 잡는다
      (`.harness/` 281 + `docs/*/research-log.md` 11 — 작성 시점 실측).
      0 이면 패턴이 죽은 것이다. 이 값은 경로 기준이다 — 내용 기준 49 와 섞지 마라.

## Anti-patterns

- [ ] AP-03: bare code fence 0건 — 여는 fence 에 언어 힌트가 있다
      (유효 대상은 19개 중 V6 가 보는 6개다 — `flutter-toolkit/skills/flutter-kaizen/SKILL.md`
      와 `harness/skills/{contract-kaizen,create-skill,evaluator-kaizen,harness-kaizen,init}/SKILL.md`.
      `harness/docs/` · `.claude/skills/` · 레포 루트는 V6 범위 밖이다 ·
      측정: `python3 scripts/validate-plugin.py --check=code-fence` 가 전 킷 OK)

      양성 대조: 이 검사는 대상에 코드 블록이 있을 때만 유효하다.
      `harness/skills/create-skill/SKILL.md` 4개 · `harness/skills/init/SKILL.md` 6개를
      작성 시점에 실측했다. 두 파일 중 하나의 여는 fence 에서 힌트를 지우면 FAIL 이 난다.

- [ ] AP-04: SKILL.md frontmatter 의 `name` 필드가 보존됐다 — V1 FAIL 0건
      (유효 대상은 AP-03 과 같은 6개 ·
      측정: `python3 scripts/validate-plugin.py --check=frontmatter` 가 전 킷 OK)

      양성 대조: 6개 대상 중 하나(`harness/skills/init/SKILL.md`)의 frontmatter 에서
      `name:` 을 지우고 같은 명령을 돌리면 `13 OK, 1 ERROR · Exit 2` 가 난다
      (교차 진단이 실제로 돌려 확인했다). 지운 뒤에는 되돌린다.

## Reusability

- [ ] RE-01: N/A (산출물이 문서·지시문 문구뿐이라 재사용 단위 코드가 0개다.
      측정: 변경 19개 파일이 전부 `.md`)
- [ ] RE-02: N/A (같은 사유 — 재사용할 컴포넌트·함수·모듈이 산출물에 없다)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 로 그 한 파일만 잰다 —
      이번 변경 파일과 교집합 0개. 측정: AR-01 의 19행에
      `grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 편집기와 같은 조건으로 잰 마크다운 경고가 기준값을 넘지 않는다
      (기준 337건 · (파일,규칙) 조합 47개 ·
      측정: scratchpad 에 `npm install --no-save markdownlint-cli2@0.23.2` 후 설정
      `{"config":{"MD013":false}}` 를 `--config` 로 넘겨 19개 파일을 돌린다.
      총 건수 ≤ 337 이고, 출력을 `파일 규칙ID` 로 정규화해 `sort | uniq -c` 한 집계에서
      기준보다 건수가 늘어난 조합이 0개. 줄 번호는 밀리므로 집계로 비교한다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 로 그 한 파일만
      돌린다 — 이번 변경 파일과 교집합 0개. 측정: DG-01 과 같음)
- [ ] DG-04: N/A (산출물에 구동할 앱·서버가 없다. 측정: 변경 19개 파일에 실행 진입점 0개 —
      전부 `.md`). 이 자리에 실제로 성립하는 검사는 SC-02 다
