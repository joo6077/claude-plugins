---
feature: "계약 지침의 검증 가능성 구멍 6건 메우기"
slug: contract-verifiability-gaps
created: "2026-09-23 09:10"
complexity: "복잡"
conditions: 18
status: active
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:4d9e2acca41395be
locked_at: "2026-09-23 09:44"
---

## 배경

앞 두 스프린트를 돌리는 동안 계약 지침 자체의 구멍 6건이 실측으로 드러났다. 전부 **"적힌 근거를
기계로 확인할 수 있는가"** 라는 한 뿌리에서 나왔다. 발견자는 봉인 전 교차 진단과 QA 이며, 각각
근거를 대고 지적했다.

1. **동의 근거의 출처가 하나뿐이다.** 개정의 `consent: anchored` 를 인정하는 조건이
   "reflect-kit prompt 로그 앵커" 로만 적혀 있다. 그런데 선택지로 받은 동의는 그 기록에
   **구조적으로 남지 않는다** — 그 기록은 `UserPromptSubmit` 훅이 쓰고, 선택지 답은 도구 결과라
   훅에 들어오지 않는다. 한 달치 33 건을 전수 확인했더니 전부 다른 프롬프트에 붙여넣은 덩어리 속
   줄이고 실제 입력은 0 건이었다. 결과적으로 선택지 동의는 지침대로는 영원히 `anchored` 가 될 수
   없다.
2. **"고친 근거를 어디서 확인해야 하는가" 가 없다.** 앞 스프린트에서 REJECT 를 받고 개정 문서를
   고쳐 APPROVE 로 뒤집었다. 그것이 정당했던 이유는 뒤집는 근거가 개정 문서의 서술이 아니라
   **구현자가 손댈 수 없는 세션 기록**이었고 교차 진단이 독립으로 같은 값을 뽑았기 때문이다.
   그런데 이 구별선이 어느 문서에도 없다. 없으면 다음번에는 개정 서술만 다듬어 통과하는 길이 열린다.
3. **봉인 뒤 계약 산문 편집을 남기는 규칙이 없다.** 봉인은 조건 줄만 덮으므로 산문은 자유롭게
   고칠 수 있다. 그런데 조건 줄이 "위 N 개 경로" 처럼 산문을 가리키면 산문은 사실상 조건의
   일부다. 앞 스프린트에서 실제로 산문 라벨을 고쳤고 개정 파일에 기록이 없었다.
4. **0 기대 조건이 대상을 개수로만 적는다.** `DG-02` 가 대상을 "`.md` 5개" 로 적고 열거하지
   않아서, 나중에 범위에 더한 파일 1 개가 검사에서 빠졌다. 다음 평가자가 같은 집합을 만들 방법이
   없다.
5. **취지를 글자 하나로 재는 조건이 통과한다.** `ER-01` 의 취지는 "평가자가 교차 진단을 직접
   한다는 서술이 0 건" 인데 재는 것은 `general-purpose` 라는 글자다. 그 글자 없이 같은 지시를
   쓰면 0 이 나온다. 이번에는 우연히 통과했다.
6. **여러 스프린트를 한 브랜치에 쌓으면 앞 계약의 상태 전환이 뒤 스프린트에 걸린다.** 앞
   스프린트가 APPROVE 되면 평가자가 그 계약의 `status` 를 `done` 으로 바꾼다. 그 한 줄이 뒤
   스프린트의 `.harness/` 범위 조건에 들어와 개정과 사용자 승인을 강제했다. 실제로 이번에
   그 때문에 REJECT 가 한 번 났다.

## 리서치 소스

- `harness/references/contract-schema.md:930` · `harness/docs/guides/qa-evaluation-guide.md:426`
  — 동의 근거 2 축 표 (같은 표가 두 곳에 복제돼 있다)
- `harness/references/contract-schema.md:256` · `:994` ·
  `harness/skills/sprint-contract/SKILL.md:702` — 봉인이 덮는 범위 서술 3 곳
- `harness/docs/guides/contract-design-guide.md:749-755` — 0 기대 조건 절
- 이 세션의 실측 — 개정 3건(A-01 정정 · A-02 · A-03), QA 2 회차,
  교차 진단 1 회 (`.harness/sprint-feedback-cross-diagnosis-to-parent.md`)
- 선행 스프린트 계약 2건 — `validate-check-count-sync` · `cross-diagnosis-to-parent`

## 범위 경계

### 설계 결정

**동의 근거의 출처를 늘리되 요구 값은 그대로 둔다.** 지금 표가 요구하는 세 값(시각 · 세션 ·
작업폴더)은 세션 기록의 `AskUserQuestion` 쌍에 전부 들어 있다. 그래서 요구 값을 바꾸지 않고
**출처 목록에 한 줄을 더한다.** 요구 값을 늘리면 기존 개정이 소급으로 무효가 된다.

**같은 표가 두 파일에 복제돼 있으므로 양쪽을 함께 고친다.** 한쪽만 고치면 두 문서가 갈린다 —
평가자는 `qa-evaluation-guide` 를, 계약 작성자는 `contract-schema` 를 본다.

**구멍 6 은 지침 쪽에서 막는다.** 계약마다 산출물 슬러그를 열거하는 대신, `.harness/` 범위
조건의 권장 형태를 "이 구간에서 **조건 줄이 바뀐** 계약 파일 0 개" 로 바꾼다. 상태 전환과 조건
변조를 구별하는 것이 원래 의도였고 봉인 검사(`verify_seal`)가 이미 그것을 한다.

**고치는 파일 4개**

```text
harness/references/contract-schema.md
harness/docs/guides/qa-evaluation-guide.md
harness/docs/guides/contract-design-guide.md
harness/skills/sprint-contract/SKILL.md
```

**범위 밖** — `harness/agents/qa-evaluator.md`. 동의 근거 표의 사본이 그 파일에도 있는지
확인했으나 638 줄 언급은 `qa-evaluation-guide` 를 가리키는 참조이고 표 본문은 없다. 옛 기록
(`.harness/` · `docs/kaizen/` · `harness/evals/`)도 범위 밖이다. 플러그인 버전 올림과 배포는
머지 뒤 main 에서 한다.

### 봉인 전 실측한 기준값

여섯 낱말·구절 전부 **현재 0 건**이다 (양성 대조가 성립한다 — 고친 뒤 1 이상이어야 한다).

| 재는 것 | 파일 | 지금 |
| --- | --- | --- |
| `AskUserQuestion` | `contract-schema.md` | 0 |
| `AskUserQuestion` | `qa-evaluation-guide.md` | 0 |
| `구현자가 쓰지 않은` | `contract-schema.md` | 0 |
| `산문을 고치면` 또는 `산문 편집` | `contract-schema.md` | 0 |
| `대상 파일을 열거` | `contract-design-guide.md` | 0 |
| `status 전환` | `contract-schema.md` | 0 |

- `python3 scripts/validate-plugin.py` — **14 plugins, 14 OK · Exit: 0**
- 편집기와 같은 조건의 마크다운 경고 — 대상 4개 합 **41건 · (파일,규칙) 조합 11개**
  (markdownlint-cli2 0.23.2 · `MD013` 끔)
- 기준 커밋 — `a9c9a0a`

### 측정 환경 주의

이 맥의 `grep` 은 ugrep 7.8.4 로 `-r` 출력에 `./` 접두를 붙이지 않는다. `for f in $VAR` 처럼
따옴표 없이 펼치면 zsh 가 쪼개지 않아 파일을 못 찾고, `2>/dev/null` 이 그 오류를 삼켜 조용히
0 이 된다. 이 세션에서 세 번 겪었다. 여러 파일을 돌릴 때는 목록을 파일에 담아 `while read` 로
돌린다.

### 상한 ref 해석

이번 스프린트는 앞 두 스프린트와 **같은 브랜치**(`feat/validate-check-count-sync`)에 쌓는다.
하한은 `a9c9a0a` 다.

```bash
sprint_head() {  # 이 레포 관례(feat/<slug> · PR 머지)
  m=$(git log --merges --format=%H --grep="from joo6077/feat/${1}" -1)
  [ -n "$m" ] && { echo "$m"; return 0; }
  git rev-parse --verify -q "feat/${1}" && return 0
  echo "UNRESOLVED feat/${1}" >&2; return 1
}
SH=$(sprint_head validate-check-count-sync) || exit 1
[ "$SH" = "$(git rev-parse a9c9a0a)" ] && { echo "STALE_HEAD"; exit 1; }
```

### 커버리지 해소

커버리지 해소: AR-01 — 산문의 4개 경로를 측정 절이 같은 표기로 열거한다.
커버리지 해소: SK-01 · SK-02 — 같은 표가 있는 두 파일을 측정 절이 각각 이름으로 든다.
커버리지 해소: AR-03 — 손대지 않을 것을 경로 패턴 3종으로 덮는다.

## Skill

- [ ] SK-01: 동의 근거 출처 목록에 세션 기록의 `AskUserQuestion` 쌍이 **두 파일 모두**
      추가됐다 [exact, enumerated]
      (대상 2곳: `harness/references/contract-schema.md` ·
      `harness/docs/guides/qa-evaluation-guide.md` ·
      측정: 두 파일 각각에 `grep -c 'AskUserQuestion'` 이 1 이상)

      양성 대조: 고치기 전 두 파일 모두 **0 건**이다 (작성 시점 실측). 0 이면 측정이 죽은 것이다.

- [ ] SK-02: 그 추가가 요구 값 세 개(시각 · 세션 · 작업폴더)를 **늘리지 않았다** [exact, enumerated]
      (요구 값을 늘리면 기존 개정이 소급 무효가 된다. `anchored` 는 두 파일에 7·6 줄씩 나오므로
      "그 행" 을 낱말로 고를 수 없다 — 지금 행의 **원문 전체를 리터럴로 보존 검사**한다
      (교차 진단 지적) ·
      측정: 두 파일 각각에
      `grep -Fc '사용자 발언 인용 + **reflect-kit prompt 로그 앵커**(timestamp · session · cwd)'`
      가 **1**. 그 줄이 그대로 남아 있으면 요구 값이 안 늘어난 것이다. 새 출처는 그 줄을 고치는
      대신 **별도 행 또는 문단으로** 더한다)

      양성 대조: 지금 그 리터럴은 두 파일에서 각 1 건이다 (작성 시점 실측 —
      `contract-schema.md:930` · `qa-evaluation-guide.md:426`). 0 이 되면 원문을 고친 것이다.

- [ ] SK-03: 봉인이 덮는 범위를 서술한 2 파일에 아래 **정확한 문장**이 들어갔다
      [exact, enumerated]

      넣을 문장 (이 리터럴 그대로):
      `조건 줄이 가리키는 산문을 고치면 개정 파일에 남긴다`

      (대상 2 파일: `harness/references/contract-schema.md` ·
      `harness/skills/sprint-contract/SKILL.md` ·
      측정: 두 파일 각각에
      `grep -Fc '조건 줄이 가리키는 산문을 고치면 개정 파일에 남긴다'` 가 1 이상)

      양성 대조: 고치기 전 두 파일 모두 **0 건**이다 (작성 시점 실측).

      **`산문` 이라는 낱말 하나로 재지 않는 이유** — 그 낱말은 이미 `contract-schema.md` 에 6 건,
      `sprint-contract/SKILL.md` 에 2 건 있다 (커버리지 논의의 "산문 측 대상" 등 다른 문맥).
      낱말로 재면 아무것도 안 고쳐도 통과한다 — 교차 진단이 이 오염을 짚었다. 이 계약이 고치려는
      구멍 5(취지를 글자 하나로 재는 조건)와 같은 형태라 특히 조심한다.

## Script

- [ ] SC-01: `contract-schema.md` 에 "고친 근거는 구현자가 쓰지 않은 기록에서 확인돼야 한다"는
      요건이 들어갔다 [exact]
      (측정: `grep -c '구현자가 쓰지 않은' harness/references/contract-schema.md` 이 1 이상)

      양성 대조: 고치기 전 **0 건**이다 (작성 시점 실측).

- [ ] SC-02: `python3 scripts/validate-plugin.py` 전체가 `14 plugins, 14 OK` · `Exit: 0` 이다
      [goal]
      (측정: 그 명령의 마지막 두 줄. 기준값과 같아야 한다)

      음성 대조: 대상 파일 중 `harness/skills/sprint-contract/SKILL.md` 의 여는 fence 에서
      언어 힌트를 지우면 V6 이 FAIL 하고 `14 OK` 가 깨진다. 이 측정은 파일 내용을 직접 읽으므로
      구현을 지워도 통과하는 형태가 아니다.

## Error

- [ ] ER-01: `contract-design-guide.md` 의 0 기대 조건 절에 **대상 파일을 열거하라**는 요구가
      들어갔다 [exact]
      (측정: `grep -c '대상 파일을 열거' harness/docs/guides/contract-design-guide.md` 이
      1 이상이고, 그 자리가 §0 이 기대값인 조건 절 안이다 —
      `awk '/^### 0 이 기대값인 조건/,/^### /'` 로 범위를 잘라 확인)

      양성 대조: 고치기 전 **0 건**이다 (작성 시점 실측).

- [ ] ER-02: 같은 가이드에 아래 **정확한 문장**이 들어갔다 [exact]

      넣을 문장 (이 리터럴 그대로):
      `취지가 서술 부재라면 낱말 하나로 재지 마라`

      (측정: `grep -Fc '취지가 서술 부재라면 낱말 하나로 재지 마라'
      harness/docs/guides/contract-design-guide.md` 가 1 이상 ·
      의역 확인("그 문맥이 …를 말한다")을 빼고 리터럴로 바꿨다 — 평가자마다 다르게 읽을 수 있다는
      교차 진단 지적을 반영. 대상이 한 파일이라 `enumerated` 태그도 뺐다)

      양성 대조: 고치기 전 **0 건**이다 (작성 시점 실측).

## Architecture

- [ ] AR-01: 이 스프린트의 변경 파일이 위 4개 경로와 정확히 일치한다 [exact, enumerated]
      (Given: 이 스프린트의 커밋이 끝난 뒤 · **`STALE_HEAD` 확인을 먼저 통과** ·
      측정: `git diff --name-only a9c9a0a..$(sprint_head validate-check-count-sync) --
      . ':(exclude).harness/**'` 의 출력이 4행이고 각 줄이 위 목록에 있다.
      `UNRESOLVED` 나 `STALE_HEAD` 면 `HEAD` 로 떨어지지 말고 사용자에게 묻는다)

- [ ] AR-02: `.harness/` 범위 조건의 권장 형태가 아래 **정확한 문장**으로 지침에 들어갔다
      [exact]

      넣을 문장 (이 리터럴 그대로):
      `sprint-contract*.md 에 verify_seal 을 돌려 SEAL_BROKEN 이 0 개`

      (앞 스프린트에서 실제로 REJECT 를 낸 함정을 지침 쪽에서 막는 조건이다. 판정 기준을
      `SEAL_OK` 가 아니라 **`SEAL_BROKEN` 0 개**로 쓴 이유는 봉인 없는 레거시 계약 11 개가
      실재하고 스키마가 그것을 "경고이지 실패가 아니다"(`contract-schema.md:287`)로 규정하기
      때문이다 — 교차 진단이 짚었다. 대상 패턴도 `sprint-contract*.md` 로 못박는다.
      `.harness/` 에는 피드백·개정·`project.yaml`·`handoff/` 처럼 계약이 아닌 파일이 섞여 있다 ·
      측정: `grep -Fc 'sprint-contract*.md 에 verify_seal 을 돌려 SEAL_BROKEN 이 0 개'
      harness/references/contract-schema.md` 가 1 이상, 그리고 같은 파일에
      `grep -c 'status 전환'` 이 1 이상)

      양성 대조: 두 문자열 모두 고치기 전 **0 건**이다 (작성 시점 실측).

- [ ] AR-03: 손대지 않기로 한 것이 변경되지 않았다 [exact]
      (Given: 이 스프린트의 커밋이 끝난 뒤 · **`STALE_HEAD` 확인을 먼저 통과** ·
      측정: `git diff --name-only a9c9a0a..$(sprint_head validate-check-count-sync)` 에서
      (i) `harness/evals/` 0행 (ii) `docs/kaizen/` 0행 (iii) `harness/agents/` 0행
      (iv) `.harness/sprint-contract*.md` 에 `verify_seal` 을 돌려 **`SEAL_BROKEN` 이 0 개**.
      `SEAL_OK` 와 `SEAL_ABSENT` 는 **둘 다 통과**다 — 봉인 없는 레거시 계약 11 개가 실재하고
      스키마가 그것을 실패로 보지 않는다(`contract-schema.md:287`). 상태 전환(`status:`)과
      새 산출물 추가도 위반이 아니다. 대상 패턴을 `sprint-contract*.md` 로 좁히는 것은
      `.harness/` 에 계약이 아닌 파일이 섞여 있기 때문이다 — 셋 다 교차 진단 지적이다)

      양성 대조: 경로 패턴 3종을 `git ls-files` 에 걸면 1 이상이 나온다 (추적 파일이 실재한다).
      (iv) 의 봉인 검사는 작성 시점에 67 개 계약에 돌려 **OK 56 · ABSENT 11 · BROKEN 0** 을
      얻었다 — 살아 있는 측정이고 지금 기준으로 통과 상태다. 개수는 산출물 추가로 시점마다
      달라지므로 총수를 고정하지 않는다 (앞 스프린트 A-01 의 교훈).

## Anti-patterns

- [ ] AP-03: bare code fence 0건 — 여는 fence 에 언어 힌트가 있다
      (유효 대상은 4개 중 V6 이 보는 2개다 — `harness/skills/sprint-contract/SKILL.md` 와
      `harness/references/contract-schema.md`. `harness/docs/` 2개는 V6 범위 밖이다
      (`scripts/validate-plugin.py:516-519`) ·
      측정: `python3 scripts/validate-plugin.py --check=code-fence` 가 전 킷 OK)

      양성 대조: 두 파일의 `^```” 개수를 봉인 전에 실측해 1 이상임을 확인한다.

- [ ] AP-04: 대상 파일의 frontmatter 가 보존됐다 — V1 FAIL 0건
      (유효 대상은 4개 중 V1 이 보는 **1개**다 — `harness/skills/sprint-contract/SKILL.md`.
      V1 은 `skills/*/SKILL.md` 와 `agents/*.md` 만 보므로 `harness/references/` 와
      `harness/docs/` 3개는 범위 밖이다. AP-03 과 형식을 맞춰 범위를 적었다 — 교차 진단 제안 ·
      측정: `python3 scripts/validate-plugin.py --check=frontmatter` 가 전 킷 OK)

      양성 대조: `harness/skills/sprint-contract/SKILL.md` 의 `name:` 을 지우고 같은 명령을
      돌리면 `13 OK, 1 ERROR · Exit 2` 가 난다 (앞 스프린트에서 실측된 방식). 지운 뒤 되돌린다.

## Reusability

- [ ] RE-01: N/A (산출물이 지침 문서 문구뿐이라 재사용 단위 코드가 0개다.
      측정: 변경 4개 파일이 전부 `.md` 이고 실행 코드 0개)
- [ ] RE-02: N/A (같은 사유 — 재사용할 컴포넌트·함수·모듈이 산출물에 없다)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 로 그 한 파일만 잰다 —
      이번 변경 파일과 교집합 0개. 측정: AR-01 의 4행에
      `grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 편집기와 같은 조건으로 잰 마크다운 경고가 기준값을 넘지 않는다
      (기준 41건 · (파일,규칙) 조합 11개 · **대상은 아래 4개 파일 전부**를 열거한다 —
      `harness/references/contract-schema.md` ·
      `harness/docs/guides/qa-evaluation-guide.md` ·
      `harness/docs/guides/contract-design-guide.md` ·
      `harness/skills/sprint-contract/SKILL.md` ·
      측정: scratchpad 에 `npm install --no-save markdownlint-cli2@0.23.2` 후 설정
      `{"config":{"MD013":false}}` 를 `--config` 로 넘겨 4개를 돌린다. 총 건수 ≤ 41 이고,
      출력을 `파일 규칙ID` 로 정규화해 `sort | uniq -c` 한 집계에서 기준보다 건수가 늘어난
      조합이 0개. 줄 번호는 밀리므로 집계로 비교한다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 로 그 한 파일만
      돌린다 — 이번 변경 파일과 교집합 0개. 측정: DG-01 과 같음)
- [ ] DG-04: N/A (산출물에 구동할 앱·서버가 없다. 측정: 변경 4개 파일에 실행 진입점 0개 —
      전부 `.md`). 이 자리에 실제로 성립하는 검사는 SC-02 다
