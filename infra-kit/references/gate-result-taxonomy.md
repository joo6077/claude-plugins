# 인프라 게이트 결과 상태 taxonomy

> **infra-kit 안에서 이 파일이 상태어 SSOT 다.** `infra-test` 가 생성하는 검증 스크립트,
> `infra-audit` 의 rule 판정, `infra-reviewer` 의 근거 열은 아래 5 상태만 쓰고 자기 문서에서
> 상태를 다시 정의하지 않는다. 인용만 한다.
>
> **여기서 정의하지 않는 것 (상위 SSOT 를 인용만 한다):**
>
> - **exit 숫자의 의미** → `harness/evals/gate-exit-codes.md`
> - **`[미검증]` 마커 의미 · 임계값 · 카운터 분리** →
>   `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol
>
> 신설: 2026-08-13 (Phase 8 kaizen)

## 왜 필요한가 — 실측

2026-07-27 Phase 8 은 `infra-test` 가 생성해주는 CI 검증 스크립트에서 버그 3 건을 고쳤다:
grep 앵커 누락(미핀닝 3 건 중 1 건만 검출) · 결함을 `echo WARN` 하고 exit 0(게이트 무력화) ·
매칭 없는 glob 이 리터럴 패턴으로 남아 "YAML syntax error" 오보.

셋의 공통 뿌리는 **결과에 "검사를 수행하지 못했다" 라는 상태가 없다**는 것이다. 상태가 없으면
도구 부재도, 대상 부재도, 실행 실패도 전부 **"위반 0"** 으로 접힌다. 인프라 감사는 `hadolint` ·
`actionlint` · `kubeconform` · `conftest` · `cosign` · `trivy` 가 없는 환경, kubectl·레지스트리
접근이 막힌 환경이 흔하므로 이 접힘이 특히 자주 일어난다.

**도구 부재를 통과로 집계하는 게이트는 없는 것보다 나쁘다** — 통과 기록이 남기 때문이다.

## 5 상태

| 상태 | 의미 | exit (`harness/evals/gate-exit-codes.md`) | 평가자 분류 (`qa-evaluation-guide.md`) |
| ------ | ------ | ------ | ------ |
| `PASS` | 검사를 **실제로 수행**했고 위반이 없다 | `0` `pass` | PASS |
| `VIOLATION` | 검사를 수행했고 **위반을 찾았다** | `1` `policy_violation` | FAIL |
| `SKIP_NO_TARGET` | 검사 **대상이 하나도 없었다** (해당 카테고리 미사용) | `3` `no_data_not_run` | N/A (카테고리 미해당 · 사유 필수) |
| `TOOL_OR_ENV_MISSING` | 대상은 있는데 **도구·런타임·접근권이 없어** 수행하지 못했다. 리포트에는 `[미검증] TOOL_OR_ENV_MISSING` 으로 적는다 | `2` `usage_or_infra_error` | `[미검증:ENV]` = `UNVERIFIED_ENV` — 단 **남용 방지 4 요건 충족 시에만**. 미충족이면 `[미검증:INVALID]` |
| `EXECUTION_ERROR` | 도구는 있으나 **실행·파싱·권한에서 실패**했다 | `2` `usage_or_infra_error` | 도구 출력은 남았으나 결과가 공허하면 `[미검증:INVALID]` (증거 무효 분기) |

**`SKIP_NO_TARGET` 과 `TOOL_OR_ENV_MISSING` 을 섞지 마라.** 전자는 볼 것이 없는 것이고 후자는
볼 수 없는 것이다. 전자는 정상 종결이지만 후자는 커버리지 손실이다.

**`TOOL_OR_ENV_MISSING` 과 `VIOLATION` 도 섞지 마라.** 도구가 없어 돌리지 못한 rule 은 PASS 도
N/A 도 아니고 `[미검증]` 이다. 같은 원칙이 **규칙 소스**에도 적용된다 — `audit-criteria.md` 를
읽지 못했다면 그 카테고리는 검사하지 않은 것이므로 위반 0 으로 보고하지 마라.

## 우선순위 — 실행 불완전이 정책 위반을 이긴다

한 run 에서 `VIOLATION` 과 `TOOL_OR_ENV_MISSING`/`EXECUTION_ERROR` 가 동시에 나오면 종료 코드는
`2` 다. 실행이 불완전한 run 의 결과 집합을 완전한 분석 결과로 보고해서는 안 되기 때문이다
(근거·규칙 원문: `harness/evals/gate-exit-codes.md` §규칙).

**종료 코드가 하나라고 해서 다른 카운트를 감추지 마라.** 요약 줄에 세 카운트를 모두 출력한다:

```text
VIOLATION=<n>  [미검증]=<n>  EXECUTION_ERROR=<n>
```

## 머리말 4 카운터 (검사 시작 전 출력 · 필수)

게이트 스크립트와 감사 리포트는 **결과보다 먼저** 아래 4 줄을 출력한다. 이 머리말이 없으면
"위반 0" 은 해석 불가다 — 분모를 모르기 때문이다.

```text
대상 <단위> 수     : <n>   (<탐색 경로>)
규칙 소스 수       : <n>   (<규칙 이름 나열 또는 읽은 파일 경로>)
사용 가능 도구 수  : <n>   [<command -v 로 확인된 도구>]
미설치 도구 수     : <n>   [<확인 실패한 도구 — 해당 rule 은 전부 [미검증]>]
```

- 도구 유무는 **추측하지 말고** `command -v <tool>` 결과만 적는다.
- 대상 수가 0 이면 그 자리에서 `SKIP_NO_TARGET` 으로 종결한다 (exit 3). PASS 로 넘기지 마라.
- 규칙 소스를 읽지 못했으면 그 소스 이름을 `[미검증]` 목록에 넣는다.

## 핵심 도구 / 선택 도구 분리

미설치를 전부 하드 실패로 막으면 CI 재현성은 좋아지지만 기여자 진입 장벽이 오른다
(트레이드오프). 그래서 두 층으로 나눈다.

| 층 | 없을 때 | 이유 |
| ------ | ------ | ------ |
| **핵심 도구** (`grep` · `python3` 같이 게이트 자체가 의존) | 즉시 `EXECUTION_ERROR` + exit 2. 검사를 **시작하지 않는다** | 없으면 모든 rule 결과가 오보다. 실측 회귀: `grep` 이 없으면 `grep -q` 가 비영 종료해 "checkout 스텝 없음" **VIOLATION 을 오보**했다 |
| **선택 도구** (`hadolint` · `actionlint` · `kubeconform` · `conftest` · `cosign` · `trivy`) | 해당 rule 만 `TOOL_OR_ENV_MISSING`, 나머지는 계속 검사 | 부분 커버리지가 0 커버리지보다 낫다 |

핵심 도구 검사는 **머리말 출력 직후, 첫 rule 실행 전**에 둔다. 그래야 사용자가 "무엇이 없어서
아무것도 못 했는지" 를 본다.

## 재검증 명령 의무

`TOOL_OR_ENV_MISSING` 을 출력할 때는 **환경이 갖춰졌을 때 이 rule 을 통과시킬 실행 가능한 명령**을
같은 줄에 적는다. 이것은 상위 SSOT 의 남용 방지 4 요건 4 항이 요구하는 것이며, 없으면 그 항목은
`UNVERIFIED_ENV` 가 아니라 `UNVERIFIED_INVALID_EVIDENCE` 로 강등된다.

```text
[미검증] TOOL_OR_ENV_MISSING: kubeconform 미설치 — 재검증: brew install kubeconform && bash tests/k8s-validation.sh
```

## 소비처

| 파일 | 소비 방식 |
| ------ | ------ |
| `infra-kit/skills/infra-test/SKILL.md` | 생성 스크립트의 상태어 · 머리말 · exit 매핑 |
| `infra-kit/skills/infra-audit/SKILL.md` | Step 3a 머리말 · rule 판정어 |
| `infra-kit/agents/infra-reviewer.md` | 근거 열의 분기 매핑 |
