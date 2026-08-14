---
slug: kaizen-phase13-failure-modes
created: "2026-08-13 18:40"
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
---

# Phase 13 amendment 사이드카

계약 본문(`.harness/sprint-contract-kaizen-phase13-failure-modes.md`, 봉인
`sha256:27d4a8c7b52f668d`)은 **한 글자도 고치지 않았다.** 아래는 자기 산출물을 사후 허용하기 위한
조건 완화가 아니라, **내가 쓴 측정문 자체의 결함 공개**다. 판정은 평가자에게 남긴다.

## AM-01 — unknown (측정문 결함 공개 · 조건 완화 아님)

- **대상 조건**: AP-03
- **변경**: **없음.** 조건 문구·측정문 모두 원문 그대로 유지한다. 아래는 실행 결과 보고다.
- **결함**: AP-03 의 측정 clause 2
  `git diff -U0 -- bambu-kit | grep -c "^+```$"` → `0` 은 **닫는 fence 까지 센다.**
  마크다운에서 코드블록의 닫는 fence 는 항상 bare ` ``` ` 이므로, 언어 힌트를 제대로 붙인
  코드블록을 **하나라도 추가하면 이 clause 는 구조적으로 0 이 될 수 없다.**
  QA 모호성 태그 분류로는 `측정-방식-불일치` — 조건 프로즈("bare code fence 를 **새로 도입**하지
  않는다")가 지정한 값(= `project.yaml` AP-03 의 `^```\s*$` 를 **여는 fence** 로 해석하는
  validate-plugin V6)과 측정이 재는 값(= 모든 bare 줄)이 다르다.
- **실행 결과 (clause 별 분해 · zsh · bash 동일)**:

  | clause | 명령 | 출력 | 판정 |
  | --- | --- | --- | --- |
  | 1 | `python3 scripts/validate-plugin.py bambu-kit` | `V6 code-fence 0 bare — OK` · `Exit: 0` | 충족 |
  | 2 | `git diff -U0 -- bambu-kit \| grep -c '^+```$'` | `4` (기대 `0`) | **미충족 — 측정문 결함** |
  | 2 보조 | `git diff -U0 -- bambu-kit \| grep -cE '^\+```[a-z]'` | `4` | 여는 fence 4 개 전부 언어 힌트 보유 |
  | 3 | 신규 파일 open/close 짝 | `fr_bare_fence=1` · `fr_open_fence=1` | 충족 |

  추가된 fence 8 줄의 실제 구성 (`git diff -U0 -- bambu-kit | grep -E '^\+```'`):
  ` ```bash ` / ` ``` ` / ` ```text ` / ` ``` ` / ` ```text ` / ` ``` ` / ` ```text ` / ` ``` `
  → **여는 4 : 닫는 4, 여는 쪽은 전부 언어 힌트 보유. bare 여는 fence 신규 도입 0 건.**

- **direction**: `unknown`. 조건을 바꾸지 않았으므로 PASS 집합의 증감 자체가 없다. 만약 clause 2 를
  "여는 fence 만 센다" 로 고친다면 그것은 PASS 집합을 **늘리는** `relaxing` 이므로, 앵커 없이는
  PASS 근거가 될 수 없다 (contract-schema v5.3 §direction × consent). 그래서 **고치지 않았다.**
- **consent**: `unanchored` — 사용자 앵커 없음. 이 세션은 비대화형 카이젠 서브에이전트다.
- **평가자에게**: clause 2 를 문자 그대로 적용하면 AP-03 은 FAIL 이다. 그 판정을 회피하려고
  조건을 고치거나 코드블록을 `~~~` 로 바꾸는(품질을 낮춰 오라클을 통과시키는) 우회를 하지 않았다.
  clause 1·3 과 보조 측정이 조건 **프로즈**의 의도를 충족함을 증거로 남긴다.
- **다음 사이클 처리**: 이 측정문 패턴(`^+```$` 카운트)은 Phase 11 계약에서 그대로 복사됐다.
  Phase 11 은 코드블록을 추가하지 않아 우연히 0 이었을 뿐 같은 결함을 갖는다. contract-design-guide
  의 조건 작성 preflight 예시로 승격할 후보다 — 다만 그것은 Phase 2/4 소관이며 이번 Phase 의
  Scope 밖이다.

## AM-02 — narrowing (조건 수 정정)

- **대상 조건**: 없음 (frontmatter `conditions` 필드)
- **변경**: 초안의 `conditions: 15` 를 **계산값** `16` 으로 정정했다.
  `grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}'` → `16`. 조건 **본문은 추가·삭제·수정하지 않았다**
  (봉인 계산 대상은 조건 체크박스 줄뿐이므로 이 정정은 `SEAL_OK` 를 깨지 않는다).
- **근거**: "열거값은 타이핑하지 말고 계산하라" — 이번 사이클 하드 프레이밍.
- **direction**: `narrowing` — 조건 수를 실제보다 적게 신고하면 평가 커버리지가 줄어든다.
  실제값으로 올리는 것은 평가 대상을 늘리는 방향이다.
- **consent**: `unanchored` — 에이전트 자체 판단. `narrowing` 이므로 PASS 근거로 사용 가능.
- **앵커**: 없음 (비대화형 세션 · 앵커를 지어내지 않는다).
