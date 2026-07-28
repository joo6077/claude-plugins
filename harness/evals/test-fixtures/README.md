# QA Accuracy Test Fixtures

qa-accuracy.md eval에서 사용하는 테스트 픽스처.
각 Fixture는 sprint-contract + 코드 조합으로 구성된다.

## 디렉토리 구조

```text
test-fixtures/
├── fixture-a/          # 완벽한 구현 → Expected: APPROVE
│   ├── contract.md
│   └── code/
├── fixture-b/          # 1개 FAIL → Expected: REJECT
│   ├── contract.md
│   └── code/
├── fixture-c/          # Anti-pattern 위반 → Expected: REJECT
│   ├── contract.md
│   └── code/
├── fixture-d/          # 관대함 함정 (동의어) → Expected: REJECT
│   ├── contract.md
│   └── code/
└── fixture-e/          # 주석 함정 → Expected: REJECT
    ├── contract.md
    └── code/
```

## 픽스처 frontmatter 규약 (contract-schema v5 대응)

| Fixture | `slug` | `status` | 기대 판정 |
| ------ | ------ | ------ | ------ |
| fixture-a | `qaa-a` | 없음 (레거시) | APPROVE |
| fixture-b | `qaa-b` | 없음 (레거시) | REJECT |
| fixture-c | `qaa-c` | 없음 (레거시) | REJECT |
| fixture-d | `qaa-d` | 없음 (레거시) | REJECT |
| fixture-e | `qaa-e` | 없음 (레거시) | REJECT |

- `slug` 는 산출물 경로를 결정론적으로 만든다. 픽스처마다 값이 달라 5 종을 병렬로 돌려도
  피드백 파일이 서로 덮어쓰지 않는다.
- **`status` 는 일부러 없다.** `status` 없는 계약은 레거시이며 qa-evaluator ladder 의
  active 후보가 아니다 (`harness/references/contract-schema.md` §status 해석 규칙).
  따라서 픽스처는 **ladder 1 단계(명시 경로)** 로만 평가되며, 이 조합 자체가
  **레거시 계약 브릿지 회귀 테스트**다.
- **픽스처에 `status: active` 를 추가하지 마라.** 추가하는 순간 레거시 경로 검증이 사라지고,
  5 종을 동시에 두면 active 후보 5 개가 되어 ladder 가 BLOCKED 로 떨어진다.

## 실행 절차

`cp fixture-x/contract.md .harness/sprint-contract.md` 방식은 **더 이상 쓰지 않는다.**
레거시(=status 없음) 계약은 active 후보가 아니라 ladder 2·3 단계에서 해소되지 않고
BLOCKED 로 끝나며, 레포의 `.harness/` 를 오염시켜 병렬 스프린트의 계약과 충돌한다.

대신 **격리 CONTRACT_ROOT + `HARNESS_CONTRACT` 명시 경로**로 돌린다.

> 셸 스니펫은 zsh · bash 양쪽에서 동작해야 한다. **글로빙 대신 `find` 를 쓴다** —
> zsh 는 기본 `nomatch` 라 매치 없는 글로브가 명령 자체를 죽인다
> (`for f in sprint-contract-*.md` → `zsh: no matches found`, 루프 진입 실패).

```bash
FIX=<레포>/harness/evals/test-fixtures   # 절대경로
F=a                                       # a|b|c|d|e

# 1) 격리 CONTRACT_ROOT 생성 — 레포 .harness 를 건드리지 않는다
EVAL_ROOT=$(mktemp -d)
mkdir -p "$EVAL_ROOT/.harness"
cat > "$EVAL_ROOT/.harness/project.yaml" <<'YAML'
stack: "flutter"
commands:
  analyze: null
  test: null
contract_categories:
  - id: UI
    prefix: "UI"
  - id: Logic
    prefix: "LG"
  - id: Error
    prefix: "ER"
  - id: Architecture
    prefix: "AR"
anti_patterns:
  - id: AP-01
    pattern: "(Consumer)?StatefulWidget"
    message: "StatefulWidget / ConsumerStatefulWidget 사용하지 않는다"
YAML

# 2) 계약을 슬러그 접미 이름으로 복사 (frontmatter slug 와 파일명 접미가 일치해야 한다)
CONTRACT="$EVAL_ROOT/.harness/sprint-contract-qaa-$F.md"
cp "$FIX/fixture-$F/contract.md" "$CONTRACT"

# 3) 사전 점검 — active 후보 0 개인데도 명시 경로로 1 개가 확정되는지 (BLOCKED 회귀 가드)
n_active=$(find "$EVAL_ROOT/.harness" -maxdepth 1 -type f \
  \( -name 'sprint-contract.md' -o -name 'sprint-contract-*.md' \) \
  -exec grep -lE "^status:[[:space:]]*[\"']?active" {} + 2>/dev/null | wc -l | tr -d ' ')
echo "ladder=1(explicit)  contract=$CONTRACT  active_candidates=$n_active"
```

기대 출력은 `active_candidates=0` 이다. 0 인데도 평가가 진행되어야 정상 —
그것이 ladder 1 단계(명시 경로)가 레거시 계약을 구제한다는 증거다.

### qa-evaluator spawn

서브에이전트 프롬프트에 아래 3 개를 **절대경로 그대로** 박는다. 평가자가 cwd 기준으로
CONTRACT_ROOT 를 다시 탐색하지 않도록 명시한다.

```text
HARNESS_CONTRACT=$EVAL_ROOT/.harness/sprint-contract-qaa-<F>.md
CONTRACT_ROOT=$EVAL_ROOT          # cwd 기준 재탐색 금지
검증 대상 코드=$FIX/fixture-<F>/code/
```

### 기대 산출물

계약이 접미형이므로 QA 산출물도 **같은 슬러그**로 떨어진다
(`harness/references/contract-schema.md` §산출물 3 종):

```text
$EVAL_ROOT/.harness/sprint-feedback-qaa-<F>.md
```

```bash
# 판정 수집 — 슬러그 대응 경로. 평가자가 CONTRACT_ROOT 를 cwd 로 재탐색했다면
# 레포 .harness/ 쪽에 떨어지므로 두 곳을 함께 확인하고, 레포 쪽에 생겼으면 지운다.
find "$EVAL_ROOT/.harness" "<레포>/.harness" -maxdepth 1 -type f \
  -name "sprint-feedback-qaa-$F.md" 2>/dev/null
```

측정 후 `rm -rf "$EVAL_ROOT"` 로 정리한다.

### DG-01 취급

픽스처 환경에는 Flutter 프로젝트가 없어 `analyze` 명령이 `null` 이다. DG-01 은
`[미검증]` 1 건으로 처리되며 수용 임계(1 건) 이내라 APPROVE/REJECT 판정에 영향을 주지 않는다.
`[미검증]` 이 2 건 이상이면 그 자체가 결함이므로 셋업을 다시 확인하라.
