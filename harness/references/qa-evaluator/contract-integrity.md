<!-- 옮김: L479-L583 -->

# QA Evaluator — 계약 봉인 확인

## Step 1-e 다음

### 봉인 확인 두 단계

#### 1-e-2. 계약 봉인 검증 — `verify_seal` (E3 · contract-schema v5.3)

지문(1-e)은 **평가 도중**의 변경을 잡는다. 봉인은 **평가 이전**의 변경 — 승인 후 조건 문구가
변조됐는지 — 를 잡는다. 실측 위반: `AR-04: 계약 write-once 위반 — 생성자가 자신이 만든 산출물을
사후에 허용하려 계약 조건 문구를 직접 편집(5→7 경로, 사이드카/사용자 승인 앵커 없음)`.

**함수 정의는 여기서 재정의하지 않는다.** `sha256_16` · `contract_digest` · `verify_seal` ·
`measurement_digest` · `verify_measurement` 다섯 함수의 SSOT 는 `harness/references/contract-schema.md` §계약 봉인 이다. 그 절의 코드 블록을
**그대로 붙여넣어** 정의하고 호출만 한다 — 다른 구현을 적으면 작성 측 게이트와 평가 측 게이트가
서로 다른 집합을 해싱하게 된다. 스키마 파일은 Step 8 과 **같은 순서의 경로 해석 ladder** 로 찾는다:

```bash
# (1) 설치된 플러그인 → (2) harness 레포 자체 → (3) 마켓플레이스 탐색
SCHEMA="${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md"
[ -f "$SCHEMA" ] || SCHEMA="$CONTRACT_ROOT/harness/references/contract-schema.md"
[ -f "$SCHEMA" ] || SCHEMA=$(find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f \
  -path '*/harness/references/contract-schema.md' 2>/dev/null | head -1)
[ -n "$SCHEMA" ] && [ -f "$SCHEMA" ] && echo "SCHEMA: $SCHEMA" || echo "SCHEMA MISSING"
# 이후: 위 파일 §계약 봉인 의 코드 블록을 그대로 정의하고 `verify_seal "$CONTRACT"` 와
#       `verify_measurement "$CONTRACT"` 를 실행한다 (fm_get 은 §값 따옴표 규약 블록).
# 스키마를 못 찾으면 seal_status: unavailable 로 기록하고 평가를 계속한다 (BLOCKED 아님).
```

**붙여넣기 전에 먼저 불러오기를 쓴다.** 코드 블록을 `sed` · `awk` 로 잘라 붙이거나 긴 따옴표로 조립하다 깨진 명령이 수 시간씩 멈춘 일이 있다 (최근 30일 4 건 · 합계 약 32 시간). `harness/scripts/measure-common.sh` 는 위 스키마 파일의 같은 코드 블록을 읽어 다섯 함수를 정의하고, 하나라도 못 찾으면 2 를 돌려준다 — 정의가 SSOT 와 같으니 재정의가 아니다:

```bash
MEASURE_SCHEMA="$SCHEMA" . "${CLAUDE_PLUGIN_ROOT}/scripts/measure-common.sh" \
  && { verify_seal "$CONTRACT"; verify_measurement "$CONTRACT"; } \
  || echo "measure-common 못 읽음 — 위 코드 블록을 그대로 붙여넣는다"
```

**결과별 취급:**

| 결과 | verdict 영향 | 기록 |
| ------ | ------ | ------ |
| `SEAL_OK` | 없음 | `seal_status: SEAL_OK` |
| `SEAL_ABSENT` | **없음 — 경고이지 실패가 아니다** | `seal_status: SEAL_ABSENT` (레거시 계약. 실측 109 개 전부가 이 상태이므로 BLOCKED 로 만들면 전 배포본이 죽는다) |
| `SEAL_BROKEN` + 사이드카에 `consent: anchored` 로 그 변경을 기술한 amendment 가 있음 | 없음 — 경고 + 사용자 확인 목록 | `contract_seal_broken: reconciled` |
| `SEAL_BROKEN` + 그 외 | **verdict = REJECT** | `contract_seal_broken: unreconciled` + `recorded` / `actual` 두 값 인용 |
| `MEASURE_OK` | 없음 | `measure_status: MEASURE_OK` |
| `MEASURE_ABSENT` | **없음 — 경고이지 실패가 아니다** | `measure_status: MEASURE_ABSENT` (v5.6 전 계약은 전부 이 상태다. 실측 104 개) |
| `MEASURE_BROKEN` + 사이드카에 `consent: anchored` 로 그 측정 변경을 기술한 amendment 가 있음 | 없음 — 경고 + 사용자 확인 목록 | `measure_status: MEASURE_BROKEN(reconciled)` |
| `MEASURE_BROKEN` + 그 외 | **verdict = REJECT** | `measure_status: MEASURE_BROKEN(unreconciled)` + `recorded` / `actual` 두 값 인용 |

`MEASURE_BROKEN` 은 조건 문구는 그대로인데 그 아래 들여쓴 측정 · 음성 대조 · 픽스처 줄이 봉인 뒤에 바뀌었다는
뜻이다. 통과 기준을 바꾼 것이라 `SEAL_BROKEN` 과 같은 급으로 다룬다. 실측(2026-09-26): 봉인 커밋이 있는 계약
74 개 중 4 개가 이렇게 바뀌었고 넷 다 `SEAL_OK` 였다 — 그중 하나는 범위를 3 경로에서 5 경로로 넓혔다.

- **조용히 다시 봉인하지 마라.** 그것은 위반을 지우는 행위다. 평가자는 계약 본문을 수정하지 않는다
  (Step 5.5 의 frontmatter `status` 전환만 예외이며, 봉인은 조건 줄만 해싱하므로 깨지지 않는다)
- **레거시 계약에 봉인을 소급해서 써 넣지 마라** — 원문이 무엇이었는지 증명할 수 없는 봉인이 된다
- `SEAL_BROKEN` 을 BLOCKED 로 만들지 않는 이유: BLOCKED 는 verdict 부재라 글로벌 피드백 코퍼스에
  위반이 남지 않는다. 그러면 다음 카이젠이 이 결함을 볼 수 없다

#### 1-e-3. 봉인 커밋 대조 — 산문 변조와 조용한 재봉인을 잡는다 (2026-09-24 추가)

`verify_seal` 은 **조건 줄만** 본다. 그래서 두 가지를 놓친다 — (a) 조건이 가리키는 **산문**을
고쳐 통과 집합을 바꾼 것 (b) 조건을 고친 뒤 **새 값으로 다시 봉인**해 `SEAL_BROKEN` 을 없앤 것.
둘 다 **봉인 시점 원문과 대조해야** 잡힌다.

계약 작성 측이 봉인 직후 계약 파일만 단독 커밋한다 (`sprint-contract` Step 6.7). 그 커밋을 찾아
지금 판과 비교한다.

```bash
# 깃은 계약 폴더로 들어가 파일 이름으로 부른다. .harness 가 하네스 저장소로 가는 바로가기면 봉인 커밋은
# 그 저장소에 있고, 프로젝트에서 절대경로로 부르면 "outside repository" 로 못 찾는다 (실측 2026-10-09)
SEAL_DIR=$(dirname "$CONTRACT"); SEAL_NAME=$(basename "$CONTRACT")
# 봉인 커밋(계약이 git 에 처음 들어온 커밋)을 찾는다
SEAL_COMMIT=$(git -C "$SEAL_DIR" log --diff-filter=A --format='%h' -- "$SEAL_NAME" 2>/dev/null | tail -1)
if [ -z "$SEAL_COMMIT" ]; then
  echo "SEAL_COMMIT_ABSENT $CONTRACT"      # 추적 안 된 계약 — 경고이지 실패가 아니다
else
  # 그 커밋에 계약 하나만 담겼는지 (섞였으면 '봉인 시점 원문' 성질이 없다)
  N=$(git -C "$SEAL_DIR" show --name-only --format='' "$SEAL_COMMIT" | grep -c .)
  echo "seal_commit=$SEAL_COMMIT files=$N"
  # 조건 줄 밖(산문)에 무엇이 바뀌었는지 본다.
  # frontmatter 의 status 전환은 빼야 한다 — 평가자 자신이 Step 5.5 에서 하는 일이다.
  # 차이 머리 줄은 '--- ' · '+++ ' 로만 뺀다 — 둘째 글자로 거르면 더한 목록 줄(+- …)까지 사라진다
  git -C "$SEAL_DIR" diff "$SEAL_COMMIT" -- "$SEAL_NAME" | grep -E '^[+-]' \
    | grep -vE '^(\+\+\+|---) ' | grep -vE '^[+-]- \[[ x]\] ([A-Z]{2,}|[^ -~]+)-[0-9]{2}' \
    | grep -vE '^[+-]status: (active|done)$'
  # 두 지문 가운데 하나라도 바뀌었으면 재봉인이다 (measurement_digest 는 v5.6)
  git -C "$SEAL_DIR" diff "$SEAL_COMMIT" -- "$SEAL_NAME" | grep -E '^[+-](conditions|measurement)_digest:'
  # 그 교체가 계약에 기록돼 있는가 (1-e-2 의 화해 경로와 같은 급)
  grep -cE '^supersedes_digest:|^supersedes_commit:' "$CONTRACT"
fi
```

**결과별 취급:**

| 관측 | verdict 영향 | 기록 |
| ------ | ------ | ------ |
| 봉인 커밋 없음 (`SEAL_COMMIT_ABSENT`) | **없음 — 경고이지 실패가 아니다** | `seal_commit: absent`. 절차 도입 전 계약이 다수다 (실측: 68 여 개 중 12 개는 추적조차 안 됨). 소급으로 만들지 마라 |
| 봉인 커밋에 파일이 2 개 이상 | 없음 — 경고 | `seal_commit: mixed(N files)`. 구현 파일이 섞여 대조 기준이 약하다 |
| 차이가 frontmatter `status` 전환뿐 | **없음 — 경고도 아니다** | 평가자 자신이 Step 5.5 에서 하는 일이다. 걸러내기에서 빼므로 아예 안 나온다. 1-e-2 에 적힌 것과 **같은 예외**다 |
| 산문 차이 있음 + 개정 파일에 그 기록 있음 | 없음 | `prose_edit: recorded` |
| 산문 차이 있음 + 개정 기록 없음 | 없음 — 경고 + 사용자 확인 목록 | `prose_edit: unrecorded` + 바뀐 줄 인용. 조건이 그 산문을 가리키면 통과 집합이 달라졌는지 **직접** 확인한다 |
| `conditions_digest` 또는 `measurement_digest` 가 바뀜 + 계약에 `supersedes_digest` · `supersedes_commit` 로 그 교체가 기록돼 있음 | 없음 — 경고 | `reseal: reconciled` + 두 값 인용. **1-e-2 의 `SEAL_BROKEN` 화해 경로와 같은 급이다** |
| `conditions_digest` 또는 `measurement_digest` 가 바뀜 + 그 외 | **verdict = REJECT** | `reseal_detected: true` + 두 값 인용. 조용한 재봉인은 위반을 지우는 행위다 |

- **산문 차이를 자동으로 REJECT 로 만들지 마라.** 서술 섹션 보강은 의도된 설계다. 조건이 그
  산문을 **가리킬 때만** 통과 집합이 달라진다
- 이 대조는 `git` 이 없거나 계약이 추적되지 않으면 못 한다. 그 경우 `seal_commit: absent` 로
  적고 평가를 계속한다 — BLOCKED 가 아니다
- **1-e-2 에 있는 예외와 화해 경로를 그대로 가져와야 한다.** 이 절을 처음 만들 때 둘을 빠뜨려
  실측 두 건이 곧바로 걸렸다 (2026-09-24, 교차 진단이 찾음): (a) 이 절을 도입한 계약 자신이
  두 번째 평가부터 `status: active → done` 을 "기록 없는 산문 변조" 로 잡았다 (b)
  `sprint-contract-kaizen-final-2026-08-13.md` 는 `supersedes_digest` · `supersedes_commit` 로
  교체를 기록해 뒀는데도 화해 경로가 없어 REJECT 대상이 됐다
- **봉인 커밋을 아직 원격에 밀어 올리지 않았으면** 그 해시는 이 기계에만 있고 `commit --amend`
  나 재배치로 갈아도 드러나지 않는다. 그 상태의 해시를 근거로 인용할 때는 "밀어 올리기 전" 임을
  함께 적는다 (§근거 경계 — 고칠 수 있는가 그리고 고친 것이 드러나는가)
