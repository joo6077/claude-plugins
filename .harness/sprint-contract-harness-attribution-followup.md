---
feature: "harness 스프린트 귀속 기록 + 계약 결함 사이드카"
slug: harness-attribution-followup
created: "2026-09-06 12:30"
complexity: "중간"
conditions: 15
status: active
owner_session: 44c7700e-f565-4643-8410-e162aa7d93d5
conditions_digest: sha256:1ae9a29f5adabadf
locked_at: "2026-09-06 12:41"
---

## 배경

동시 편집 세션이 이 세션의 스프린트 산출물을 자기 커밋에 함께 쓸어담았다. 실측 3 회:
`e73429f`("죽은 외부 링크 40건 교정") 에 구현 14 파일, `3cd7dfe`("QA REJECT 2건 수정") 에
QA 산출물 3 개. 사용자 결정은 **이력을 그대로 두고 후속 커밋으로 정리**(옵션 a)다.

따라서 남는 일은 두 가지다. (1) 어느 커밋의 어느 파일이 어느 스프린트 것인지 **귀속을 기록물로
남긴다** — 커밋 메시지가 내용과 어긋나 있어 기록이 없으면 나중에 추적 불가능하다.
(2) `harness-core-defects` 계약이 REJECT 되면서 평가자가 남긴 **계약 결함 3 건을 사이드카에
기록한다** — 계약은 봉인돼 있어 본문 수정이 금지된다.

이 계약 자체가 `harness-core-defects` 의 `DG-04` 산출물이기도 하다. 그 조건은 "변경한 문서
규약대로 계약을 1 건 작성해 Step 6.5 게이트가 위반 0 건으로 통과한다" 를 요구한다. 그래서 이
계약은 이번 스프린트가 신설한 규약 3 종을 **실제로 행사**한다: 빈 카테고리의 `N/A (사유)` 표기 ·
통합 결함 태그 preflight · 리터럴 환경값 대신 baseline 커밋 해시 고정.

## 범위 경계

- 산출물은 기록물 2 개뿐이다. **코드·스킬·가이드 본문을 고치지 않는다.**
- 봉인된 계약 2 건의 조건 줄은 **어떤 경우에도 수정하지 않는다.**
- baseline 은 리터럴 상태 서술이 아니라 커밋 해시 `3cd7dfe` 로 고정한다 (평가자 권고
  `[AR-03] 측정-상태-모호`). 동시 세션이 추가 커밋을 해도 이 baseline 은 흔들리지 않는다.
- 커버리지 해소: AR-01 — 귀속 대상 커밋 2 개를 측정 절에 개별 해시로 열거했다.

## Skill

- [ ] SK-01: 귀속 기록물이 `.harness/sprint-amendments-harness-core-defects.md` 에 존재하고, 평가자가 남긴 계약 결함 3 종 `측정-상태-모호` · `측정-산출물-부재` · `범위-미명시` 를 각각 조건 ID 와 함께 기록한다 [exact, enumerated] (측정: 파일 존재 + 3 종 각각 `grep -c` >= 1)
- [ ] SK-02: 사이드카가 amendment 의 `direction` 을 자기신고하지 않고 **집합 비교로 산출**한 근거를 함께 적는다 [structural] (측정: `direction` 필드와 그 산출 근거 문장이 각각 1 건 이상)
- [ ] SK-03: 귀속 기록이 커밋 해시별로 **어느 파일이 어느 스프린트 소속인지** 표로 남는다 [structural] (측정: 커밋 해시 2 종과 스프린트 슬러그 2 종이 같은 표 안에 등장)

## Script

- [ ] SC-00: N/A (사유: 이번 스프린트는 기록물 2 개만 생성한다 — 셸 스크립트·실행 코드 변경이 0 건이라 스크립트 카테고리에 잴 대상이 존재하지 않는다)

## Error

- [ ] ER-01: 사이드카가 봉인된 계약 본문을 대체하지 않고 **보완**임을 명시하며, 원 조건 문구를 인용할 때 수정본이 아니라 원문임을 밝힌다 [structural] (측정: 본문 수정 금지를 명시한 문장 1 건 이상)

## Architecture

- [ ] AR-01: 변경 범위가 기록물 2 개로 한정된다. Given: baseline 커밋 `3cd7dfe`. `git diff --name-only 3cd7dfe -- .harness/` 결과가 이 계약 파일과 사이드카 파일 2 개뿐이고, `harness/` · `bambu-kit/` · `docs/` 경로 0 건이다 [exact, enumerated] (측정: `git diff --name-only 3cd7dfe -- .harness/ harness/ bambu-kit/ docs/` 출력 전체를 인용)
- [ ] AR-02: 봉인된 계약 2 건의 `conditions_digest` 가 baseline 시점과 동일하다 [exact, enumerated] (측정: `sprint-contract-bambu-kit-enum-allowlist-gate.md` 와 `sprint-contract-harness-core-defects.md` 각각 `verify_seal` 이 `SEAL_OK`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-03: bare code fence 금지 — validate-plugin V6 FAIL (언어 힌트 필수: ```text, ```bash, ```yaml 등)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: N/A (사유: `commands.analyze` 는 `bash -n scripts/release.sh` 인데 이번 스프린트는 셸 스크립트를 변경하지 않는다 — 변경/생성 파일 대상이 0 건이라 잴 것이 없다)
- [ ] DG-02: N/A (사유: IDE diagnostics 미적용 확장자 .md 만 생성한다)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 생성한 기록물 2 개가 Step 6.5 게이트 기준(허용 헤더만 사용 · 조건 체크박스가 조건 섹션에만 존재 · frontmatter conditions 값 일치)을 위반 0 건으로 통과한다
