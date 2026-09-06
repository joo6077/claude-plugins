---
feature: "harness 귀속 기록 재검증 — 정정된 오라클"
slug: harness-attribution-followup-v2
created: "2026-09-06 14:50"
complexity: "단순"
conditions: 14
status: done
owner_session: 44c7700e-f565-4643-8410-e162aa7d93d5
conditions_digest: sha256:bf6f58b5fcc22715
locked_at: "2026-09-06 14:43"
---

## 배경

선행 계약 `harness-attribution-followup` 은 QA 에서 **REJECT (13/15)** 를 받았다. FAIL 2 건은
구현 결함이 아니라 **조건의 오라클 결함**이다 — 어떤 올바른 구현으로도 만족할 수 없다.

- `AR-01` — `git diff --name-only` 가 (a) 미추적 신규 파일을 원천 제외하고 (b) 동시 편집
  세션의 변경과 이 스프린트 자신의 QA 부산물까지 같은 pathspec 에 담는다. 실측 8 파일(요구 2).
- `DG-04` — 계약 파서용 Step 6.5 게이트를 **사이드카**에도 걸었다. 스키마는
  *"사이드카는 별도 파일이지 계약 섹션이 아니다"* 라고 명시하므로, 이 조건을 만족시키려면
  사이드카를 자기 스키마 위반 상태로 만들어야 한다.

선행 계약은 봉인돼 있어 문구를 고칠 수 없다. 그래서 **그 계약과 REJECT 기록을 그대로 보존**하고,
정정된 오라클로 같은 산출물을 재검증한다. 정정안은 사이드카
`.harness/sprint-amendments-harness-attribution-followup.md` 의 `AR-01'` · `DG-04'` 이며
QA 평가자가 독립적으로 제안한 형태와 동일하다.

**산출물은 새로 만들지 않는다.** 이미 생성된 기록물 2 개를 정정된 기준으로 다시 잴 뿐이다.

## 범위 경계

- 신규 파일은 이 계약 파일 하나뿐이다. 기록물 2 개는 선행 스프린트가 이미 만들었다.
- 봉인된 계약 3 건의 조건 줄은 **어떤 경우에도 수정하지 않는다.**
- 오라클은 pathspec 집계가 아니라 **경로별 존재 확인**을 쓴다 — 동시 작성자가 있어도 안 깨진다.
- 커버리지 해소: SK-01 — 검증 대상 기록물 2 개를 측정 절에 개별 경로로 열거했다.

## Skill

- [ ] SK-01: 기록물 2 개가 baseline 이후 실제로 추가됐다 — `.harness/sprint-amendments-harness-core-defects.md` 와 `.harness/sprint-contract-harness-attribution-followup.md` [exact, enumerated] (측정: 두 경로 각각 `git log --oneline 3cd7dfe..HEAD -- <path> | wc -l` >= 1)
- [ ] SK-02: 사이드카 2 종이 §Amendment 사이드카 엔트리 포맷을 만족한다 — `대상 조건` · `변경` · `근거` · `앵커` 4 항목을 각 파일이 모두 갖는다 [exact, enumerated] (측정: `sprint-amendments-harness-core-defects.md` 와 `sprint-amendments-harness-attribution-followup.md` 각각에서 4 항목 `grep -c` >= 1)
- [ ] SK-03: 사이드카의 `consent` 어휘가 스키마의 2 값 `anchored` · `unanchored` 안에 있고, 그 밖의 값이 0 건이다 [exact, enumerated] (측정: 두 사이드카에서 `consent: applied` 등 비표준 값 `grep -c` == 0)

## Script

- [ ] SC-00: N/A (사유: 기록물만 재검증한다 — 셸 스크립트·실행 코드 변경이 0 건이라 스크립트 카테고리에 잴 대상이 존재하지 않는다)

## Error

- [ ] ER-01: 선행 계약의 REJECT 기록이 보존된다 — `sprint-contract-harness-attribution-followup.md` 의 `status` 가 `active` 이고 그 피드백 리포트가 존재한다 [exact, enumerated] (측정: status 값 확인 + `.harness/sprint-feedback-harness-attribution-followup.md` 존재)

## Architecture

- [ ] AR-01: 계약 파일만 Step 6.5 게이트 대상이다 — 이 계약과 선행 계약이 각각 허용 헤더만 사용하고, 조건 체크박스가 조건 섹션에만 있고, frontmatter `conditions` 값이 실제 조건 수와 일치한다 [exact, enumerated] (측정: 두 계약 파일 각각에 Step 6.5 의 3 개 명령을 실행해 위반 0 건)
- [ ] AR-02: 봉인된 계약 3 건의 `conditions_digest` 가 그대로다 [exact, enumerated] (측정: `sprint-contract-bambu-kit-enum-allowlist-gate.md` · `sprint-contract-harness-core-defects.md` · `sprint-contract-harness-attribution-followup.md` 각각 `verify_seal` == `SEAL_OK`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: N/A (사유: `commands.analyze` 는 `bash -n scripts/release.sh` 인데 셸 스크립트를 변경하지 않는다 — 변경/생성 파일 대상 0 건)
- [ ] DG-02: N/A (사유: IDE diagnostics 미적용 확장자 .md 만 생성한다)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 산출물 종류별로 게이트가 분리 적용된다 — 계약 파일은 Step 6.5 를 위반 0 건으로 통과하고, 사이드카는 §Amendment 사이드카 엔트리 포맷을 만족한다 (사이드카에 Step 6.5 를 적용하지 않는다) [exact, enumerated] (측정: AR-01 과 SK-02 의 측정 결과를 각각 인용)
