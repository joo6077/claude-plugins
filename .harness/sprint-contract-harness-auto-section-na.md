---
feature: "harness 자동 포함 조건 N/A 허용 — 코드가 아닌 산출물"
slug: harness-auto-section-na
created: "2026-09-19 14:05"
complexity: "복잡"
conditions: 20
status: done
owner_session: be3037df-1ee8-45db-aa79-f54d3cadb2fc
conditions_digest: sha256:60d5bc4f0b98511c
locked_at: "2026-09-19 13:58"
---

## 배경

- 2026-09-19 설정 파일 · 문서 산출물 스프린트 2 건(H2 AMS Flipper v2, bambu-kit 출력 교훈)에서 교차 진단이 같은 결함을 두 번 짚었다:
  자동 포함 `DG-01` · `DG-03` 은 이 레포 `commands` 가 `scripts/release.sh` 만 재서 그 파일을 안 건드린 스프린트에 판별력이 0 이고,
  `DG-04` 는 구동할 앱이 없고, `RE-01` · `RE-02` 는 산출물에 컴포넌트가 없어 FAIL 상태를 한 문장으로 쓸 수 없다.
- **쓰는 쪽과 읽는 쪽이 어긋나 있다.** 읽는 쪽 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol
  2 항은 이미 "공허한 0 을 PASS 로 적지 말고 `N/A (사유)`" 를 요구하는데, 쓰는 쪽 `harness/skills/sprint-contract/SKILL.md` Step 4 ·
  `harness/references/contract-schema.md` §3 · §4 · `harness/skills/sprint-contract/references/red-flags.md` 는 "사용자 수정 불가" 라
  적혀 있어 계약 작성자가 공허한 조건을 그대로 넣게 된다. 사용자가 이 반영을 선택했다 (2026-09-19 "harness: 설정·문서 산출물 예외").
- **공통 전제 (모든 조건에 적용):** `H` = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/harness-auto-section-na`
  (브랜치 `feat/harness-auto-section-na`) · 저장소 스크립트는 `$H/scripts/` 를 `$H` 에서 실행한다 ·
  "범위" 는 각 조건 측정 절의 awk 식으로 자른 구간이다.
- 복잡도 4 축: 레이어 = 작성 스킬 · 스키마 · 평가자 · 평가 가이드 (예) / 공개 계약 = 계약 포맷의 허용 문구가 바뀐다 (예) /
  소비면 = qa-evaluator 가 계약을 읽는다, 모든 킷 계약 (예) / 회귀 = 평가자가 N/A 를 PASS 로 흘리거나 남용을 못 잡을 수 있다 (예)
  → **복잡**. 생산 쪽(SK-01 · SK-02 · SK-03)과 소비 쪽(SK-04 · SK-05)을 나눈다.
- 설정 리터럴 대조: `commands.analyze` = `bash -n scripts/release.sh` · `commands.test` = `bash scripts/release.sh 2>&1 || true` ·
  `diagnostics.ide_exclude` = `[]` · 카테고리 = `Skill/SK` · `Script/SC` · `Error/ER` · `Architecture/AR` · 안티패턴 선별 `AP-01` · `AP-03`.

## GAP 분석

- Pre-Edit Audit (실제 Read 증거, 기준 `origin/main` baa1a38):
  - `harness/skills/sprint-contract/SKILL.md:504-518` Step 4 "모든 계약에 자동 포함되며 사용자 수정 불가" → SK-01
  - `harness/references/contract-schema.md:790-806` §3 · §4 자동 포함 블록, N/A 언급 0 → SK-03
  - `harness/skills/sprint-contract/references/red-flags.md:20` "Diagnostics 조건 빼줘 … 수정 불가" → SK-02
  - `harness/agents/qa-evaluator.md:582-597` Reusability · Diagnostics 검증 — 조건 본문이 N/A 일 때 처리 규칙 0 → SK-04
  - `harness/docs/guides/qa-evaluation-guide.md:1029-1039` 2 항 — `commands` 가 null 인 경우만 다룬다. 명령이 있어도 이번 변경
    파일을 재지 않는 경우 · 앱 없음 · 컴포넌트 없음은 없다 → SK-05
  - `harness/evals/skill-behavior.md:28` "analyze/test 명령 미설정 표시" 사례 1 개 — 설정 · 문서 산출물 사례 없음 → SK-06
- 같은 문구를 복제한 곳: `commands.analyze 미설정` 문구는 `qa-evaluation-guide.md` 에만 있다(전수 grep). 킷 reviewer 6 종은 §Canonical
  을 이름으로만 참조하므로 2 항 개정이 복제본 불일치를 만들지 않는다.

## 범위 경계

- 조건 ID(`RE-01` ~ `DG-04`)와 자동 포함 자체는 유지한다. 바뀌는 것은 "적용 대상이 없을 때 `N/A (사유)` 로 쓸 수 있다" 뿐이다.
- 이 계약 자신의 Diagnostics 는 개정 전 규칙(설치본)으로 쓴다 — 개정이 아직 배포되지 않았다.
- 평가자가 실제로 N/A 를 어떻게 판정하는지 LLM 을 돌려 재는 것은 범위 밖이다. 문서 규칙과 파서 게이트 통과까지만 잰다.
- 오라클 해소: SK-01 — 산출물이 에이전트가 읽는 규칙 문서라 문서 안 규칙 문장이 곧 산출물이다. 파서 통과는 ER-01 · ER-02 가 실행으로 잰다.
- 오라클 해소: SK-04 — 같은 사유. 평가자가 규칙대로 판정하는지 LLM 으로 재는 것은 범위 밖(위).
- 오라클 해소: SK-06 — 같은 사유. 평가 사례 문서 자체가 산출물이다.
- 커버리지 해소: AR-01 — 경로 9 개는 기대 집합이고, 측정 명령 하나(`git diff --name-only`)가 바뀐 파일 전부를 한 번에 낸다.

## 회귀 게이트

- 봉인 전 실측: `$H` 에서 `grep -c '사용자 수정 불가' harness/skills/sprint-contract/SKILL.md` = 1 ·
  `grep -c 'N/A' harness/references/contract-schema.md` = 0 · `harness/evals/skill-behavior.md` 의 사례 수(`^- \*\*` 또는 `^###` 로 시작하는 줄) 기록.
- CI 검사 10 개는 개정 전 `$H` 에서 전부 exit 0 이었다 (bambu-kit 스프린트 워크트리에서 같은 main 기준 실측).

## Skill

- [ ] SK-01: `harness/skills/sprint-contract/SKILL.md` Step 4 (범위: `awk '/^### 4\. 자동 포함 섹션/{s=1;next} /^### 5\./{s=0} s'`)에서 `사용자 수정 불가` 가 0 회이고, 조건을 **지우거나 ID 를 바꾸지 않는다**는 문장과 `N/A (사유)` 규칙이 있으며, N/A 가 허용되는 경우로 `DG-01` · `DG-02` · `DG-03` · `DG-04` · `RE-01` · `RE-02` 가 각각 1 회 이상 나온다 [structural, enumerated] (측정: 범위에 `grep -c` — `사용자 수정 불가` 0, `N/A (` 1 이상, 여섯 ID 각각 1 이상)
- [ ] SK-02: `harness/skills/sprint-contract/references/red-flags.md` 의 `"Diagnostics 조건 빼줘"` 행이 "지우는 것은 불가" 와 "`N/A (사유)`" 를 함께 말하고 `수정 불가` 로 끝나지 않는다 [structural] (측정: 그 행 1 줄에 `grep -c 'N/A'` 1, `grep -c '수정 불가 |$'` 0)
- [ ] SK-03: `harness/references/contract-schema.md` §3 · §4 (범위: `awk '/^### 3\. Reusability/{s=1;next} /^## Amendment 사이드카/{s=0} s'`)에 N/A 형식 예시 줄(`- [ ] DG-0` 로 시작하고 `N/A (` 가 든 줄)이 1 개 이상 있고, 판정 의미의 정본으로 `qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 을 가리킨다 [structural] (측정: 범위에 `grep -cE '^- \[ \] DG-0[1-4]: N/A \('` 1 이상 + `grep -c 'Canonical Unverified-Evidence Protocol'` 1 이상)
- [ ] SK-04: `harness/agents/qa-evaluator.md` Reusability · Diagnostics 검증 절 (범위: `awk '/^\*\*Reusability 검증:\*\*/{s=1} /^### Step 3:/{s=0} s'`)에 조건 본문이 `N/A (사유)` 일 때의 처리가 있다 — (a) 명령을 돌리지 않고 사유를 잰다, (b) 사유가 사실이면 PASS · FAIL · `[미검증]` 어디에도 넣지 않고 N/A 로 따로 센다, (c) 사유가 거짓이거나 사유가 없으면 FAIL [structural, enumerated] (측정: 범위에 `grep -c 'N/A'` 3 이상 + `사유가 거짓` 1 이상 + `FAIL` 1 이상 + `따로 센다` 또는 `따로 집계` 1 이상)
- [ ] SK-05: `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 2 항 (범위: `awk '/가 성립하지 않는 프로젝트의/{s=1} /^3\. \*\*.\[미검증\]. 은 검증 도구/{s=0} s'`)이 N/A 경우를 넷으로 넓힌다 — 명령 미설정(기존), 명령이 이번 변경 파일을 재지 않음, 구동할 앱 · 서버 없음(`DG-04`), 재사용 단위 코드 없음(`RE-01` · `RE-02`). 각 경우에 사유를 **측정하는 방법**이 한 줄 붙는다 [structural, enumerated] (측정: 범위에 `변경 파일` · `DG-04` · `RE-01` 각각 1 이상 + `측정` 3 이상)
- [ ] SK-06: `harness/evals/skill-behavior.md` 에 설정 · 문서 산출물 스프린트 사례가 1 개 추가되고, 기대 행동으로 "자동 포함 조건을 지우지 않고 `N/A (사유)` 로 쓴다" 와 "사유에 측정 방법을 적는다" 가 있다 [structural] (측정: `grep -c 'N/A (사유)' harness/evals/skill-behavior.md` 1 이상 + 그 사례 블록에 `측정` 1 이상)

## Script

- [ ] SC-00: N/A (이 스프린트는 `scripts/release.sh` · 버전 bump · marketplace.json 을 건드리지 않는다)

## Error

- [ ] ER-01: `harness/skills/sprint-contract/SKILL.md` 의 Step 6.2 조건 수 명령과 Step 6.5 (1)(2)(3) 명령을 원문 그대로 추출해, 자동 포함 6 개 중 4 개를 `N/A (사유)` 로 쓴 예시 계약(`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/be3037df-1ee8-45db-aa79-f54d3cadb2fc/scratchpad/harness/example-na-contract.md`)에 돌리면 조건 수가 N/A 줄까지 포함해 세어지고(예시 계약의 체크박스 줄 수와 같다) 서술 섹션에 체크박스 0 · `MISMATCH` 0 이다 [exact] (측정: 추출 명령 실행 출력. 음성 대조: 예시 계약의 frontmatter `conditions` 를 1 줄이면 `MISMATCH` 가 나와야 한다)
- [ ] ER-02: 같은 예시 계약에 `harness/references/contract-schema.md` §계약 봉인의 `contract_digest` 를 두 번 돌려 같은 값이고, N/A 줄 하나의 사유 문구를 바꾸면 값이 달라진다 — N/A 문구도 봉인 대상이다 [exact] (측정: 두 실행 비교 + 변형 사본 비교)

## Architecture

- [ ] AR-01: Given 이 스프린트 커밋 완료, `git -C $H diff --name-only origin/main...feat/harness-auto-section-na` 결과가 다음 집합에 포함된다 — `harness/skills/sprint-contract/SKILL.md` · `harness/skills/sprint-contract/references/red-flags.md` · `harness/references/contract-schema.md` · `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md` · `harness/evals/skill-behavior.md` · `.harness/sprint-contract-harness-auto-section-na.md` · `.harness/sprint-feedback-harness-auto-section-na.md` · `.harness/sprint-amendments-harness-auto-section-na.md` [exact, enumerated] (측정: 위 명령, 상한 ref 는 브랜치 이름)
- [ ] AR-02: `$H` 에서 CI 검사 10 개가 전부 exit 0 이다 — `python3 scripts/validate-plugin.py` · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/sync-docs.py --check-only` · `python3 scripts/sync-orchestrator.py --check-only` · `python3 scripts/run-evals.py --verbose` · `python3 scripts/check-contrast-claims.py` · `python3 scripts/check-docs-links.py` · `python3 scripts/check-stale-values.py` · `bash harness/evals/kaizen/feedback-system/save-test.sh` · `node scripts/check-docs-a11y.js` [exact, enumerated] (측정: bash 스크립트 파일로 순서대로 실행)
- [ ] AR-03: 다른 브랜치와 병합 충돌이 없다 — `git -C $H merge-tree --write-tree feat/bambu-kit-print-lessons feat/harness-auto-section-na` 와 `git -C $H merge-tree --write-tree feat/bambu-kit-orca-h2s-feedback feat/harness-auto-section-na` 가 둘 다 exit 0 [exact, enumerated] (측정: 두 명령 exit)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다 (이 스프린트는 `harness/.claude-plugin/plugin.json` 을 바꾸지 않는다. 측정: AR-01 목록에 그 파일 없음)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `$H` 에서 `python3 scripts/validate-plugin.py harness --check=code-fence` exit 0)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: bash -n scripts/release.sh 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외)
- [ ] DG-03: bash scripts/release.sh 2>&1 || true 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
