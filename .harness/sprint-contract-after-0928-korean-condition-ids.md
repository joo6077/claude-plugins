---
feature: "계약 조건 번호를 한국어 이름으로 (묶음 id — SK · SC · ER · AR · RE · DG · AP → 스킬 · 스크립트 · 오류 · 구조 · 재사용 · 진단 · 금지)"
slug: after-0928-korean-condition-ids
created: "2026-09-29 09:21"
complexity: "복잡"
conditions: 29
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:2dfbe5bc0290bd96
measurement_digest: sha256:d63c0cc68f812773
locked_at: "2026-09-29 09:38"
---

## 배경

- 사용자 결정(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md` 19~21 줄, 원문 「계약서 작성할 때 뭔가 줄임말 안썼으면 하는데 er 머 이런거」): 새 계약의 조건 번호 앞자리를 한국어로 쓴다 — `SK`→`스킬` · `SC`→`스크립트` · `ER`→`오류` · `AR`→`구조` · `RE`→`재사용` · `DG`→`진단` · `AP`→`금지`. 봉인된 옛 계약(영어 번호)은 한 글자도 고치지 않고 그대로 읽혀야 한다. 쉬운 말 목록(`~/.claude/rules/plain-korean.md`)의 허용 약자 둘째 줄에서 일곱을 뺀다.
- 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).
- **이 계약부터 한국어 번호를 쓴다.** 그래서 조건 섹션 이름은 지금 `project.yaml` 카테고리 id(`Skill` · `Script` · `Error` · `Architecture`)를 그대로 쓰고, 번호 앞자리만 이 묶음이 바꿀 값(`스킬` · `스크립트` · `오류` · `구조` · `재사용` · `진단` · `금지`)을 미리 쓴다. 금지 패턴 번호 `금지-03` · `금지-04` 는 지금 `project.yaml` 의 `AP-03` · `AP-04` 와 같은 패턴이다(문구 · 명령 그대로).
- **지금 도구는 한국어 번호를 못 읽는다 (봉인 전 실측, W 끝 `98ac739f`).** 조건 세기 · 봉인 계산 · 측정 줄 봉인이 모두 `[A-Z]{2,}-[0-9]{2}` 모양만 본다.
  - 시험 계약 `.harness/.meta/after-kaizen-0928/id-compat/fixture-korean.md`(한국어 번호 7 줄)에서 지금 정규식 `grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}'` 은 0, 한국어를 더한 정규식은 7.
  - 지금 규약 문서의 `contract_digest` · `measurement_digest` 는 둘 다 `e3b0c44298fc1c14` (빈 입력의 지문)를 낸다 — bash · zsh 같다.
  - `seal-korean.sh` 실측: 지금 도구로 봉인한 한국어 계약은 조건 문구를 바꿔도 · 측정 줄을 바꿔도 `SEAL_OK,MEASURE_OK` 다 — 변조를 못 잡는다.
  - 그래서 **이 계약은 도구를 고친 뒤 봉인한다** (Step 6.6 은 스킬-01 · 스크립트-02 가 통과한 판에서 돈다). 이 판의 `conditions:` 는 아래 6.2 절 명령(한국어를 더한 정규식)으로 채우고, 지금 도구의 6.5 (3) 은 `MISMATCH` 가 나는 것이 정상이다 — 이 사실을 6.5 요약에 적는다.
  - 봉인 순서 (교차 진단 뒤 확정): 네 문서 · 쪽 둘의 정규식만 작업 폴더에서 먼저 고치고(커밋 안 함), 그 상태에서 스킬-01 · 스크립트-02 · 오류-01 · 스크립트-01 을 재 통과를 확인한 뒤 6.5 · 6.6 을 돈다. 6.7 봉인 커밋에는 계약 파일 하나만 담고, 정규식 수정은 그 뒤 harness · docs 커밋으로 들어간다 — git 기록에서 봉인 커밋이 구현 커밋보다 앞선다.
- 새 정규식 한 모양 (규약 문서가 정한다, 모든 읽는 곳이 같은 글자를 쓴다):
  - 확장 정규식: `([A-Z]{2,}|[가-힣]+)-[0-9]{2}`
  - awk 모양: `([A-Z][A-Z]+|[가-힣]+)-[0-9][0-9]`
  - 봉인 전 실측: 옛 계약 240 개(`.harness/` · `.harness/history/`, 이 계약 제외)에서 조건 수 · `contract_digest` · `measurement_digest` · `verify_seal` · `verify_measurement` 가 지금 정규식과 새 정규식에서 한 줄도 다르지 않다 (bash · zsh 호출 모두). 조건 수 합 4930, `SEAL_OK` 127 · `SEAL_ABSENT` 113 · `MEASURE_OK` 38 · `MEASURE_ABSENT` 202. `LC_ALL=C` · `en_US.UTF-8` · `ko_KR.UTF-8` 에서 한국어 시험 계약의 두 지문이 같다(`8b52386c713a6054` · `c51d48673b5caeee`). 두 값은 파이썬으로 따로 계산한 값과 같다.
- 측정 묶음 (W 에 커밋됨, 폴더 `.harness/.meta/after-kaizen-0928/id-compat/` — 아래 `C` 로 줄여 쓴다. 파일 지문은 sha256 앞 16 자리):
  - 커밋 `2ceb3101`: `old-contracts.txt b9208ab84925e2d9` · `base-old.txt cec1a2c5f20d762c` · `fixture-korean.md f4655b51780eddb3` · `fixture-mixed.md 5a2e12929a17b0af` · `fcount.sh 2f22118047df25ad` · `lone-ids.sh 586b4ae81326dd00` · `regions.txt 39df44b3c2c66619` · `overflow.mjs 086621caa310a5eb`
  - 커밋 `ab1666f0`: `fixture-coverage.md 5b2ae472f57e6986`
  - 커밋 `98ac739f` (마지막 판): `compat.sh 95306a9be78b6195` · `lone-ids-all.sh e0cd7a4cf2daeef3` · `antipattern-count.sh 4693fd62ff0bfe23` · `antipattern-repeat.sh a3a74a6cdc19b61d` · `seal-korean.sh ed3e53f2a52192ac` · `plain-korean-hooks.sh dcdc6f7503587ea4`
  - 이 묶음 파일은 구현 중에 고치지 않는다. 모든 측정은 레포 뿌리(W)에서 돈다.
- 앞선 측정 묶음 재사용: `M` = `.harness/.meta/after-0928-harness-checks/` 의 `m-scope.sh a5b343e119307246` · `m-diag.sh 08291bb42d36311f`. markdownlint 는 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl` 의 markdownlint-cli2 0.23.2, shellcheck 0.11.0 (`/opt/homebrew/bin/shellcheck`).

## 리서치 소스

- `harness/references/contract-schema.md` §계약 봉인 · §측정 줄 봉인 · §4. Diagnostics · §해당 없음 마커 · §복잡도별 조건 수 가이드 · §측정 관례.
- `harness/skills/sprint-contract/SKILL.md` Step 0.5 · 2 · 3 · 4 · 6.2 · 6.5 · 6.6.
- `harness/agents/qa-evaluator.md` 1-b 조건 수 대조 · 1-e-3 봉인 커밋 대조.
- `~/.claude/hooks/_plain-korean-glossary.py` `load()` — 둘째 `text` 울타리를 허용 약자로 읽는다(`fences[1].split()`).

## GAP 분석

번호를 쓰거나 읽는 곳을 레포 전체(`.harness/` 봉인 파일 제외, 추적 파일 967 개)에서 찾은 결과다. 찾은 명령: 조건 정규식 모양 `git ls-files | xargs grep -nE 'A-Z\][^ ]{0,6}-(\[0-9\]|\\d)'` · 번호 글자 `git grep -nE '(RE-0[12]|DG-0[1-4]|AP-00|XX-00|\{PREFIX\}|prefix: ")'` · 코드 파일 `git ls-files '*.sh' '*.py' '*.js' '*.mjs' | xargs grep -nE '(AP|RE|DG|SK|SC|ER|AR)-(\[|[0-9]|\\d)'`.

- 읽는 곳 (정규식) — 계약 형식 문서 `contract-schema.md` 에 확장 정규식 4 (300 · 333 · 907 · 1493 줄) · awk 모양 2 (346 줄), sprint-contract `SKILL.md` 6 (312 · 699 · 709 · 726 · 764 · 773), `qa-evaluator.md` 2 (517 · 592), `qa-evaluation-guide.md` 1 (766). 쪽 `docs/harness/contract-schema.html` 확장 5 · awk 2, `docs/harness/qa-evaluation-guide.html` 1. 커버리지 검출기(계약 형식 문서 907 · 908 줄)는 정규식에 더해 번호 칸을 떼는 `sub(/^[^A-Z]*/, "", id)` 가 한국어 번호를 지운다. `harness/scripts/measure-common.sh` 는 규약 문서의 함수를 그대로 읽으므로 규약만 고치면 따라온다.
- 읽는 곳 (금지 패턴 번호) — `harness/scripts/validate.sh:72` `grep -c "id: AP-"`. 한국어 번호면 0 건이 되고, 0 건일 때 `grep -c` 의 `0` 과 `|| echo "0"` 이 겹쳐 `[: 0\n0: integer expected` 로 경고가 조용히 빠진다 (실측 `antipattern-count.sh`: 금지 4 개 · 0 개 모두 `interr=1 apwarn=0`). `harness/skills/harness-kaizen/scripts/trigger-check.sh:79-80` `AP-[0-9]` — 한국어 번호 피드백 셋이 반복돼도 알리지 않는다 (실측 `antipattern-repeat.sh 금지-01 금지-01 금지-01` → `rc=1 out=[]`).
- 쓰는 곳 (틀 · 규칙) — `.harness/project.yaml` 의 prefix 넷 · 금지 패턴 id 넷, `harness/templates/project.yaml` 의 금지 패턴 주석 id 둘, `SKILL.md` Step 2 · 3 · 4 (자동 포함 여섯 줄 · `AP-00` · N/A 표), 계약 형식 문서 §해당 없음 마커 · §2~4 · §복잡도별 조건 수 · 예시 두 줄(555 · 556), `red-flags.md:7`, `contract-design-guide.md:1131`, `qa-evaluation-guide.md` 미검증 규칙 덩어리(1289~1303, 킷 reviewer 여덟 · `flutter-audit` 에 글자 그대로 사본), `harness/README.md:120 · 121 · 129`, `harness/skills/init/SKILL.md:55`, `harness/evals/skill-behavior.md:57 · 58`, 평가 사례 `harness/evals/kaizen/contract-kaizen/assertions.json:13` (`"AP-00: N/A"` 를 찾는다) · `expected-improvements.md:29`.
- 규칙 자리 17 곳의 지금 값 (`bash C/lone-ids-all.sh`): 17 곳 모두 한국어 번호 0 줄, 16 곳에 영어 번호만 있는 줄이 있다 — `regions=17 not_clean=17`. 틀 줄 `- [ ] (RE-0[12]|DG-0[1-4]|AP-00):` 는 `SKILL.md` 7 · `contract-schema.md` 12 · `contract-schema.html` 12. `AP-00` 글자는 `SKILL.md` 2 · `contract-schema.md` 2 · `red-flags.md` 1 · `contract-design-guide.md` 1 · `contract-schema.html` 2 · `contract-design-guide.html` 3 (그중 279 · 280 은 바뀐 내역 인용).
- 기능 조건 세기 (`fcount.sh`, 시험 계약 `fixture-mixed.md` — 한국어 · 영어 섞인 8 줄, 손으로 센 기능 조건 2): 지금 `SKILL.md` · 규약 문서 둘 다 1.
- 이미 됨 / 해당 없음 — `scripts/*.py`(validate-plugin · collect-kaizen-data · run-evals · sync-evals · spawn-kaizen-phase 등)는 조건 번호 모양을 읽지 않는다(위 코드 파일 검색에서 주석 · 시험 이름표만 나온다). `harness/scripts/check-superseded.sh` · `commit-guard.sh` · `save-feedback.sh` 도 번호를 읽지 않는다. `harness/scripts/validate.sh:79` prefix 중복 검사 · `:89` 카테고리 id 읽기는 글자 종류와 무관하다.
- 못 함 (이유) — `harness/templates/project.yaml` · `react-kit/templates/harness-project.yaml.template` 의 **카테고리** prefix(`UI` · `LG` · `ER` · `AR` / `AR` · `ST` · `PF` · `A11Y` · `LP` · `TS`)는 결정 목록 밖 약자와 한 틀에 섞여 있어, 일곱만 바꾸면 한 계약에 두 방식이 섞인다. 사용자 결정이 일곱으로 한정했으므로 이번에는 그대로 두고 남은 일로 적는다. 지난 계약 인용(「RE-02 재발 방지」 · 「실측 `ER-02`」 같은 글, 시험 파일 이름표 · 주석)은 옛 계약의 조건 이름이라 그대로 둔다.

## 범위 경계

- 이 계약이 고치는 것: 위 GAP 의 읽는 곳 · 쓰는 곳 · 쪽 셋 · 레포 밖 목록 한 파일. 카테고리 id(`## Skill` 같은 섹션 이름)와 `Anti-patterns` · `Reusability` · `Diagnostics` 섹션 이름은 그대로다.
- 봉인된 계약 · QA 리포트 · 개정 파일(`66e6c74b` 에 이미 있는 `.harness/sprint-contract-*.md` · `sprint-feedback-*.md` · `sprint-amendments-*.md` · `.harness/history/*`)은 고치지 않는다. 시험 픽스처 `harness/evals/test-fixtures/*/contract.md` 도 옛 모양 그대로 둔다 — 옛 번호가 읽히는지 보는 자리다.
- 규칙 자리 17 곳의 머리 글자(`C/regions.txt` 의 둘째 · 셋째 칸)는 바꾸지 않는다. 바꾸면 `NO_REGION` 으로 스킬-05 · 구조-01 이 FAIL 한다.
- 옛 번호를 가리켜야 하는 규칙 문장에서는 한국어 번호 옆에 옛 번호를 괄호로 붙인다 (예: `진단-01`(옛 계약은 `DG-01`)). 영어 번호만 남은 줄은 규칙 자리에서 0 이다.
- 레포 밖 예외: `~/.claude/rules/plain-korean.md` 한 파일, 허용 약자 울타리의 둘째 줄 `SK SC ER AR RE DG AP` 과 그 설명 줄 `둘째 줄은 계약 조건 번호의 앞자리다 (스킬 · 스크립트 · 에러 · 구조 · 재사용 · 진단 · 안티패턴).` 두 줄만 지운다. 고치기 전에 원본을 `.harness/.meta/after-kaizen-0928/id-backup/plain-korean.md` 로 복사해 커밋한다. `~/.claude/hooks/` 는 고치지 않는다.
- `.harness/` 안에서 더하는 것: 이 계약 · 측정 묶음 `C` · 백업 폴더 · notes `.harness/.meta/after-kaizen-0928/id-notes.md` · QA 산출물 · 피드백 초안.
- 대응 쪽: `contract-schema.md` → `docs/harness/contract-schema.html`, `qa-evaluation-guide.md` → `docs/harness/qa-evaluation-guide.html`, `contract-design-guide.md` → `docs/harness/contract-design-guide.html`. `SKILL.md` · `qa-evaluator.md` · 킷 에이전트 · `README.md` 는 짝 쪽이 없다 (`scripts/detect-docs-drift.py` 짝 표 기준).
- 커밋: 맨 위 폴더 하나씩 (harness · docs · 킷 여덟 · flutter-toolkit · .harness). 메시지는 한국어, 끝에 서명 줄. 구현 전에 `tone-kit:tone-guide` 1 단계, 완료 전에 5 단계를 돈다.
- 오라클 해소: 스킬-05 · 구조-01 — `lone-ids.sh` 는 「실측」·「출처」 가 든 줄을 지난 계약 인용으로 보고 뺀다. 그런 줄만 있는 범위가 통과하지 않도록 범위마다 한국어 번호 1 줄 이상을 함께 요구한다.
- 커버리지 해소: 스킬-06 — 킷 reviewer 여덟 · `flutter-audit` 아홉 사본은 `scripts/check-reviewer-protocol-copies.py` 가 원문 덩어리와 글자로 맞대고, 원문 덩어리는 스킬-05 의 범위 6 번이 잰다.
- 커버리지 해소: 구조-02 — `m-scope.sh` 의 `changed=` 줄이 28 경로 전체를 한 번에 맞댄다(`.harness` 는 제외 경로 표기).
- 조건 수: 기능 조건 21 개로 복잡 가이드 상한 20 을 하나 넘는다. 읽는 곳과 쓰는 곳을 나누면 그 사이 판에서 새 계약이 봉인되지 않거나 옛 계약 판정이 갈리므로 한 묶음으로 둔다 (사용자 위임 범위 안의 판단).
- 범위 목록 (커밋 직전 훅이 읽는다, 구조-02 의 28 경로와 같다):

```text
# sprint-scope
api-kit/agents/api-reviewer.md
backend-kit/agents/backend-reviewer.md
design-kit/agents/design-reviewer.md
docs/harness/contract-design-guide.html
docs/harness/contract-schema.html
docs/harness/qa-evaluation-guide.html
flutter-toolkit/skills/flutter-audit/SKILL.md
harness/README.md
harness/agents/qa-evaluator.md
harness/docs/guides/contract-design-guide.md
harness/docs/guides/qa-evaluation-guide.md
harness/evals/kaizen/contract-kaizen/assertions.json
harness/evals/kaizen/contract-kaizen/expected-improvements.md
harness/evals/measure/measure-helpers-test.sh
harness/evals/skill-behavior.md
harness/references/contract-schema.md
harness/scripts/validate.sh
harness/skills/harness-kaizen/scripts/trigger-check.sh
harness/skills/init/SKILL.md
harness/skills/sprint-contract/SKILL.md
harness/skills/sprint-contract/references/red-flags.md
harness/templates/project.yaml
howto-kit/agents/howto-reviewer.md
infra-kit/agents/infra-reviewer.md
planning-kit/agents/planning-reviewer.md
react-kit/agents/react-reviewer.md
rust-kit/agents/rust-reviewer.md
.harness/project.yaml
```

## 회귀 게이트

- 로컬 CI 전체와 CI 파일에만 있는 단계 열여섯(구조-05) — 봉인 전 모두 통과 (`measure-helpers-test.sh` 는 `PASS` 19 줄 · `실패 0 건`).
- 옛 계약 240 개 판정 불변 (스크립트-01).

## Skill

- [ ] 스킬-01: 조건 줄을 읽는 네 문서의 정규식이 모두 두 형식을 읽는 한 모양으로 바뀐다 [exact, enumerated]
  측정: 파일마다 `grep -oF '[A-Z]{2,}-[0-9]{2}' <파일> | wc -l` 과 `grep -oF '[A-Z][A-Z]+-[0-9][0-9]' <파일> | wc -l` 이 0, `grep -oF '([A-Z]{2,}|[가-힣]+)-[0-9]{2}' <파일> | wc -l` 이 아래 값 이상, `grep -oF '([A-Z][A-Z]+|[가-힣]+)-[0-9][0-9]' <파일> | wc -l` 이 아래 값 이상
  대상과 최소값(확장 · awk): `harness/references/contract-schema.md` 4 · 2, `harness/skills/sprint-contract/SKILL.md` 6 · 0, `harness/agents/qa-evaluator.md` 2 · 0, `harness/docs/guides/qa-evaluation-guide.md` 1 · 0
  기준(봉인 전): 옛 모양이 4 · 2, 6, 2, 1 이고 새 모양은 모두 0
  음성 대조: 옛 모양이 한 곳이라도 남으면 그 파일의 옛 모양 수가 1 이상이라 FAIL
  측정 (검출기): 규약 문서 §측정 커버리지 표기 의 bash 블록(첫 줄 `# 커버리지 검출기`)을 떼어 `CF=C/fixture-coverage.md` 로 돌리면 `UNCOVERED` 줄이 정확히 둘이고 번호 칸이 `스킬-99:` · `SK-98:` 이다 (봉인 전 실측: 지금 검출기는 `SK-98:` 한 줄만 낸다. 번호 칸을 떼는 `sub(/^[^A-Z]*/, "", id)` 도 한국어 번호를 지운다)
- [ ] 스킬-02: 기능 조건 세기 awk 가 한국어 자동 번호도 뺀다 — 섞인 시험 계약에서 두 문서 모두 2 를 낸다 [exact, enumerated]
  측정: `bash C/fcount.sh harness/skills/sprint-contract/SKILL.md C/fixture-mixed.md` 와 `bash C/fcount.sh harness/references/contract-schema.md C/fixture-mixed.md` 가 각각 `2`
  알려진 답: `fixture-mixed.md` 는 `## Skill` 에 `스킬-01` · `SK-03` · `오류-02: N/A (x)`, `## Anti-patterns` 에 `금지-01`, `## Reusability` 에 `재사용-01` · `RE-02`, `## Diagnostics` 에 `진단-04` · `DG-01` — 기능 조건은 `스킬-01` · `SK-03` 둘. 봉인 전 실제값 두 문서 모두 1 (종료 코드 0)
  음성 대조: awk 제외 목록에서 `재사용-0[12]|진단-0[1-4]` 를 빼면 4, 한국어 정규식을 빼면 1 이 나와 FAIL
- [ ] 스킬-03: 새 계약의 틀이 한국어 자동 번호만 쓴다 — 자동 포함 여섯 줄과 금지 패턴 해당 없음 줄 [exact, enumerated]
  측정 (1): `grep -cE -- '- \[ \] (RE-0[12]|DG-0[1-4]|AP-00):' <파일>` 이 `harness/skills/sprint-contract/SKILL.md` · `harness/references/contract-schema.md` 에서 각각 0 (기준 7 · 12)
  측정 (2): 두 파일 각각에서 아래 여섯 글자의 `grep -cF` 가 1 이상 — `- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다` · `- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다` · `- [ ] 진단-01: {commands.analyze} 워닝 0개 (변경/생성 파일 대상)` · `- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ({diagnostics.ide_exclude} 제외)` · `- [ ] 진단-03: {commands.test} 콘솔 로그에 에러/예외 0개` · `- [ ] 진단-04: 실제 앱/서버 구동 시 에러 0개`
  측정 (3): `grep -c 'AP-00: N/A' <파일>` 이 `harness/skills/sprint-contract/SKILL.md` · `harness/references/contract-schema.md` · `harness/skills/sprint-contract/references/red-flags.md` · `harness/docs/guides/contract-design-guide.md` 에서 각각 0 이고 `grep -c '금지-00: N/A' <파일>` 이 각각 1 이상 (기준 `AP-00: N/A` 2 · 2 · 1 · 1, `금지-00` 0)
- [ ] 스킬-04: 계약 형식 문서에 옛 번호와 새 번호의 짝 일곱이 한 표로 있고, 옛 번호 계약도 같은 뜻으로 읽힌다는 문장이 있다 [exact, enumerated]
  측정: `harness/references/contract-schema.md` 에서 일곱 짝 각각 `grep -cE` 가 1 이상 — ``'`SK`.*`스킬`'`` · ``'`SC`.*`스크립트`'`` · ``'`ER`.*`오류`'`` · ``'`AR`.*`구조`'`` · ``'`RE`.*`재사용`'`` · ``'`DG`.*`진단`'`` · ``'`AP`.*`금지`'`` (기준 일곱 모두 0)
  측정: 같은 파일에서 `grep -cE '옛 계약.*(영어|SK|DG).*(그대로|같은 뜻)|(그대로|같은 뜻).*옛 계약'` 이 1 이상 (기준 0 — 봉인 전 실측)
- [ ] 스킬-05: 규칙 자리 17 곳에 영어 자동 번호만 남은 줄이 없고, 17 곳 모두 한국어 자동 번호가 한 줄 이상 있다 [exact, enumerated]
  측정: `bash C/lone-ids-all.sh` 끝 줄이 `regions=17 not_clean=0` (기준 `regions=17 not_clean=17`)
  17 곳 (`C/regions.txt`): `SKILL.md` Step 2 · Step 3~4, `contract-schema.md` §해당 없음 마커 · §2 Anti-patterns~§Amendment 앞 · §복잡도별 조건 수, `qa-evaluation-guide.md` 미검증 규칙 2 항, `contract-design-guide.md` 과소 안티패턴 행, `harness/README.md` · `harness/skills/init/SKILL.md` · `harness/evals/skill-behavior.md` · `harness/skills/sprint-contract/references/red-flags.md` 파일 전체, `docs/harness/contract-schema.html` 네 곳 · `docs/harness/qa-evaluation-guide.html` 한 곳 · `docs/harness/contract-design-guide.html` 한 곳
  알려진 답: 손 입력 `머리 / DG-01 a / 진단-01 (옛 DG-01) / 실측 DG-02 / 끝` 에서 `lone-ids.sh` 가 `region=4 lone=1 ko=1`, 없는 머리에서 `NO_REGION` 종료 코드 2 (봉인 전 실측)
- [ ] 스킬-06: 킷 reviewer 여덟과 `flutter-audit` 의 미검증 규칙 사본이 바뀐 원문과 글자까지 같다 [exact, enumerated]
  측정: `python3 scripts/check-reviewer-protocol-copies.py` 종료 코드 0, 끝 줄 `checked=9 violations=0 infra_errors=0 excluded=0`
  대상 아홉: `api-kit/agents/api-reviewer.md` · `backend-kit/agents/backend-reviewer.md` · `design-kit/agents/design-reviewer.md` · `howto-kit/agents/howto-reviewer.md` · `infra-kit/agents/infra-reviewer.md` · `planning-kit/agents/planning-reviewer.md` · `react-kit/agents/react-reviewer.md` · `rust-kit/agents/rust-reviewer.md` · `flutter-toolkit/skills/flutter-audit/SKILL.md`
  양성 대조: 임시 폴더에 `scripts/check-reviewer-protocol-copies.py` · `scripts/plugin_utils.py` 와 원문 · 사본 열 파일을 복사해 돌리면 `checked=9 violations=0`, 그 사본 `rust-kit/agents/rust-reviewer.md` 의 한 글자(`산출물에` → `산출물이`)를 바꾸면 `violations=1` · 종료 코드 1 (봉인 전 실측)
- [ ] 스킬-07: 평가 사례가 새 해당 없음 줄을 찾는다 [exact, enumerated]
  측정: `harness/evals/kaizen/contract-kaizen/assertions.json` 에서 `grep -c '"금지-00: N/A"'` 가 1 · `grep -c 'AP-00'` 이 0, `harness/evals/kaizen/contract-kaizen/expected-improvements.md` 에서 `grep -c 'AP-00'` 이 0 · `grep -c '금지-00'` 이 1 이상, `python3 scripts/run-kaizen-assertions.py` 끝 줄 `Total: 14 passed, 0 failed` 이고 `PASS contract-kaizen/vacuous-boilerplate#1` 줄이 있다
  음성 대조: `git show 66e6c74b:harness/skills/sprint-contract/SKILL.md | grep -c '금지-00: N/A'` 가 0 — 옛 스킬 본문이면 이 사례가 FAIL 한다

## Script

- [ ] 스크립트-01: 옛 계약 240 개의 조건 수 · 두 지문 · 봉인 판정 두 가지가 고친 뒤에도 한 줄도 바뀌지 않는다 [exact, enumerated]
  측정: `bash C/compat.sh | diff - C/base-old.txt | grep -cE '^[<>]'` 이 0 이고 `compat.sh` 종료 코드 0, `zsh -c 'bash C/compat.sh' | diff - C/base-old.txt | grep -cE '^[<>]'` 도 0
  대상: `C/old-contracts.txt` 의 240 경로 (봉인 전 `.harness/` 아래 `*sprint-contract*.md` 전부에서 이 계약만 뺀 것). 기준 조건 수 합 4930 · `SEAL_OK` 127 · `SEAL_ABSENT` 113 · `MEASURE_OK` 38 · `MEASURE_ABSENT` 202
  음성 대조: 규약 정규식에서 영어 쪽을 뺀 사본(`([가-힣]+)-[0-9]{2}` · awk 모양도 같이)을 `bash C/compat.sh <사본>` 으로 돌리면 `diff <출력> C/base-old.txt | grep -c '^<'` 이 217 (`grep -cE '^[<>]'` 로 세면 양쪽을 다 세어 434) — 봉인 전 실측, 두 값 모두 0 이 아니라 FAIL
- [ ] 스크립트-02: 고친 규약의 함수가 한국어 번호 시험 계약을 읽는다 — 조건 7 · 두 지문이 알려진 답과 같다, bash · zsh · 세 로캘 모두 [exact, enumerated]
  측정: `for sh in bash zsh; do for loc in C en_US.UTF-8 ko_KR.UTF-8; do LC_ALL=$loc $sh -c '. harness/scripts/measure-common.sh; contract_digest C/fixture-korean.md; measurement_digest C/fixture-korean.md'; done; done` 여섯 번 모두 `8b52386c713a6054` 와 `c51d48673b5caeee` (C 는 묶음 폴더 경로로 바꿔 넣는다), `grep -cE "$(awk '/^contract_digest\(\)/{getline; print; exit}' harness/references/contract-schema.md | sed -E "s/.*grep -E '([^']*)'.*/\1/")" C/fixture-korean.md` 이 7
  알려진 답: 두 지문은 파이썬 `hashlib` 로 조건 줄 7 줄 · 번호와 들여쓴 줄 8 줄을 따로 해시한 값이다. 봉인 전 실제값은 두 함수 모두 `e3b0c44298fc1c14`, 규약 정규식 조건 수 0
- [ ] 스크립트-03: 공용 측정 시험에 한국어 번호 확인이 둘 이상 들어가고 CI 가 이미 돌리는 그 시험이 통과한다 [exact, enumerated]
  측정: `bash harness/evals/measure/measure-helpers-test.sh` 종료 코드 0, 끝 줄 `실패 0 건`, `^PASS K` 로 시작하는 줄 2 이상, `^PASS` 줄 21 이상 (기준 19 · K 0), 시험 파일에서 `grep -c 8b52386c713a6054` 와 `grep -c c51d48673b5caeee` 가 각각 1 이상
  음성 대조: 임시 폴더에 `harness/evals/measure/` · `harness/scripts/` 를 복사하고 `harness/references/contract-schema.md` 자리에 `git show 66e6c74b:harness/references/contract-schema.md` 를 두고 그 사본의 시험을 돌리면 `^FAIL K` 줄이 1 이상 · 종료 코드가 0 이 아니다
- [ ] 스크립트-04: 금지 패턴 반복 알림이 한국어 번호를 읽고 옛 번호도 그대로 읽는다 [exact, enumerated]
  측정: `bash C/antipattern-repeat.sh 금지-01 금지-01 금지-01` → `rc=0 out=[TRIGGER: Anti-pattern 반복: 금지-01 (3회)]`, `bash C/antipattern-repeat.sh AP-01 AP-01 AP-01` → `rc=0 out=[TRIGGER: Anti-pattern 반복: AP-01 (3회)]`, `bash C/antipattern-repeat.sh 금지-01 금지-01 AP-01` → `rc=1 out=[]` (다른 번호는 합치지 않는다)
  기준(봉인 전): 첫째 `rc=1 out=[]` · 둘째 지금과 같음 · 셋째 `rc=1 out=[]`
- [ ] 스크립트-05: 설정 검사가 금지 패턴을 두 형식으로 세고 0 건에서도 경고를 낸다 [exact, enumerated]
  Given: `.harness/project.yaml` 의 금지 패턴 id 가 `금지-01`~`금지-04` 로 바뀐 뒤
  측정: `bash C/antipattern-count.sh '<식>'` 다섯 번 — `s/x/x/` → `rc=0 apwarn=0 interr=0`, `s/id: 금지-/id: AP-/` → `rc=0 apwarn=0 interr=0`, `s/id: 금지-0([34])/id: AP-0\1/` → `rc=0 apwarn=0 interr=0`, `s/id: 금지-0([234])/id: ZZ-0\1/` → `rc=0 apwarn=1 interr=0`, `s/id: 금지-0/id: ZZ-0/` → `rc=0 apwarn=1 interr=0`
  기준(봉인 전, 지금 파일은 AP): 한국어 4 개 `apwarn=0 interr=1`, 0 개 `apwarn=0 interr=1`, 1 개 `apwarn=1 interr=0`
  판별력: 다섯 식 가운데 둘째 · 셋째(옛 번호만 · 섞임)는 안 고친 `validate.sh` 로도 같은 값이 나오는 옛 번호 유지 확인이다. 고친 것과 안 고친 것을 가르는 식은 첫째 · 넷째 · 다섯째다 (교차 진단 실측)
- [ ] 스크립트-06: 이 레포 설정과 설정 틀이 한국어 앞자리 · 한국어 금지 패턴 번호를 쓴다 [exact, enumerated]
  측정: `sed -n '/^contract_categories:/,/^# ──/p' .harness/project.yaml | grep -E 'id:|prefix:' | tr -d ' '` 출력이 `-id:Skill` · `prefix:"스킬"` · `-id:Script` · `prefix:"스크립트"` · `-id:Error` · `prefix:"오류"` · `-id:Architecture` · `prefix:"구조"` 여덟 줄 그대로, `grep -cE '^  - id: 금지-0[1-4]$' .harness/project.yaml` 이 4 · `grep -c 'AP-' .harness/project.yaml` 이 0, `harness/templates/project.yaml` 에서 `grep -cE '^  # - id: 금지-0[12]$'` 이 2 · `grep -c 'AP-'` 이 0
  기준(봉인 전): prefix `SK` · `SC` · `ER` · `AR`, 금지 패턴 id `AP-01`~`AP-04`, 틀 주석 `AP-01` · `AP-02`

## Error

- [ ] 오류-01: 한국어 번호 계약도 봉인이 변조를 잡는다 — 조건 문구를 바꾸면 조건 봉인이, 측정 줄을 바꾸면 측정 봉인이 깨진다 [exact, enumerated]
  측정: `bash C/seal-korean.sh` 출력 두 줄이 `bash sealed=SEAL_OK,MEASURE_OK cond_changed=SEAL_BROKEN,MEASURE_OK measure_changed=SEAL_OK,MEASURE_BROKEN` · `zsh sealed=SEAL_OK,MEASURE_OK cond_changed=SEAL_BROKEN,MEASURE_OK measure_changed=SEAL_OK,MEASURE_BROKEN`
  기준(봉인 전): 두 셸 모두 세 칸이 `SEAL_OK,MEASURE_OK` — 지금 도구는 변조를 못 잡는다
- [ ] 오류-02: 봉인된 옛 계약 · QA 리포트 · 개정 파일이 한 글자도 바뀌지 않는다 [exact, enumerated]
  Given: 이 스프린트 커밋이 끝난 뒤, 상한은 가지 `chore/ak3-id` 끝 (`git rev-parse --verify -q refs/heads/chore/ak3-id` 가 안 풀리면 종료 코드 2 로 멈춘다)
  측정: `git diff --name-only 66e6c74b chore/ak3-id -- .harness | grep -vcE '^\.harness/(project\.yaml|sprint-(contract|feedback|amendments)-after-0928-korean-condition-ids\.md|\.meta/after-kaizen-0928/(id-compat|id-backup)/.+|\.meta/after-kaizen-0928/id-notes\.md)$'` 이 0
  양성 대조: 봉인 전 `git diff --name-only 66e6c74b fc3fab3e -- .harness` 에 이 식을 걸면 0 (측정 묶음만), 임시 목록에 `.harness/sprint-contract-after-0928-harness-checks-r2.md` 한 줄을 더하면 1
- [ ] 오류-03: 쉬운 말 목록에서 두 줄만 빠지고, 목록을 읽는 두 훅이 그 뒤에도 정상으로 돈다 [exact, enumerated]
  측정 (1) 백업: `git ls-files --error-unmatch .harness/.meta/after-kaizen-0928/id-backup/plain-korean.md` 종료 코드 0, 그 파일 `shasum -a 256 | cut -c1-16` 이 `694f07858cf9016c` (고치기 전 원본의 봉인 전 실측값)
  측정 (2) 차이: `diff .harness/.meta/after-kaizen-0928/id-backup/plain-korean.md ~/.claude/rules/plain-korean.md | grep -E '^[<>]'` 가 정확히 두 줄 `< 둘째 줄은 계약 조건 번호의 앞자리다 (스킬 · 스크립트 · 에러 · 구조 · 재사용 · 진단 · 안티패턴).` · `< SK SC ER AR RE DG AP`
  측정 (3) 훅: `bash C/plain-korean-hooks.sh ~/.claude/rules/plain-korean.md` 출력이 `abbr=43 seven=0 pairs=69 words=12` · `check_rc=0 verdict=miss words=["SK"]` · `remind_rc=0 remind_seven=0` 로 시작하는 세 줄
  기준(봉인 전, 원본 사본): `abbr=50 seven=7 pairs=69 words=12` · `check_rc=0 verdict=pass words=` · `remind_rc=0 remind_seven=7`

## Architecture

- [ ] 구조-01: 문서 사이트 쪽 셋이 원문과 같은 정규식 · 해당 없음 줄 · 짝 표를 싣고, 공통 스타일 링크 하나 · 세 폭 넘침 0 을 지킨다 [exact, enumerated]
  측정 (1): `docs/harness/contract-schema.html` 에서 옛 확장 · awk 모양 `grep -oF` 수 0 · 새 확장 5 이상 · 새 awk 2 이상, `docs/harness/qa-evaluation-guide.html` 에서 옛 확장 0 · 새 확장 1 이상 (기준 옛 5 · 2 · 1)
  측정 (2): `grep -c 'AP-00: N/A' docs/harness/contract-schema.html` 이 0 (기준 2), 일곱 짝 ``'`SK`.*`스킬`'`` 모양 대신 쪽에서는 ``'<code>SK</code>.*<code>스킬</code>'`` 모양 일곱이 `docs/harness/contract-schema.html` 에서 각각 1 이상 (기준 0), 규칙 자리 여섯 곳은 스킬-05 가 잰다
  측정 (3): 세 쪽 각각 `grep -c '<link rel="stylesheet" href="../assets/site.css">'` 가 1, `python3 scripts/check-docs-common-css.py` 종료 코드 0, `node C/overflow.mjs <W 절대 경로>` 끝 줄 `cases=9 overflow=0` (세 쪽 × 320 · 375 · 1280)
  양성 대조: 봉인 전 세 쪽 사본 중 `contract-schema.html` 에 폭 2000px 블록을 넣은 임시 폴더에서 `overflow.mjs` 가 `cases=9 overflow=3`
- [ ] 구조-02: 바뀐 경로(.harness 밖)가 범위 목록 28 경로 안에 있고, 커밋마다 맨 위 폴더 하나 · 서명 줄 하나다 [exact, enumerated]
  Given: 이 스프린트 커밋이 끝난 뒤
  측정: `bash M/m-scope.sh <W> 66e6c74b chore/ak3-id` 의 `changed=` 경로 각각이 `## 범위 경계` 의 `# sprint-scope` 블록 27 경로(`.harness/project.yaml` 은 `.harness` 제외라 안 나온다) 중 하나이고, 끝 줄이 `commits=<n> bad=0 dirty=0` (n ≥ 1)
  기준(봉인 전, 끝 `98ac739f`): `changed=` 빈 값 · `commits=5 bad=0 dirty=0`
- [ ] 구조-03: 커밋 메시지 제목이 모두 한국어를 담는다 [exact, enumerated]
  Given: 이 스프린트 커밋이 끝난 뒤
  측정: `git log --no-merges --format=%s 66e6c74b..chore/ak3-id | grep -vc '[가-힣]'` 이 0 이고 `git log --no-merges --format=%s 66e6c74b..chore/ak3-id | grep -c .` 이 1 이상
- [ ] 구조-04: 원본을 바꾼 문서의 짝 쪽이 모두 같이 바뀌었다 [exact, enumerated]
  Given: 이 스프린트 커밋이 끝난 뒤, 작업 폴더가 가지 `chore/ak3-id` 끝에 있을 때
  측정: `python3 scripts/detect-docs-drift.py --since 66e6c74b --json` 이 낸 쪽 경로 각각이 `bash M/m-scope.sh <W> 66e6c74b chore/ak3-id` 의 `changed=` 안에 있다 (쪽이 0 개면 통과가 아니라 FAIL — 원본 셋을 바꾸므로 쪽 셋 `docs/harness/contract-schema.html` · `docs/harness/qa-evaluation-guide.html` · `docs/harness/contract-design-guide.html` 이 나와야 한다. 모양만 바뀐 짝으로 빠지면 `--include-format-only` 로 다시 잰다)
- [ ] 구조-05: 로컬 CI 전체와 CI 파일에만 있는 단계가 모두 통과한다 [exact, enumerated]
  측정 (1): `TMPDIR=<scratch 아래 새 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` 의 단계 줄이 모두 `rc=0` 또는 `SKIP (yq 없음)`(feedback-agg-test 하나) 이고 끝 줄 `rc=0`
  측정 (2): 로컬 CI 도구 밖 단계 열여섯이 각각 종료 코드 0 — `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-check-docs-common-css.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/check-install-docs-guidance.py` · `python3 scripts/test-check-cause-table-copies.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test design-kit/evals/visuals.spec.js` · `npx playwright test api-kit/evals/`
  기준(봉인 전, 끝 `fc3fab3e` — 그 뒤 커밋은 `.harness/.meta` 만 바꿨다): (1) 단계 25 줄 모두 `rc=0`, `feedback-agg-test SKIP (yq 없음)`, 끝 줄 `rc=0` · (2) 열여섯 모두 종료 코드 0

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (설정의 `AP-03` 과 같은 패턴). 측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 (고치는 `SKILL.md` · 계약 형식 문서 · 에이전트에 코드 블록이 있다)
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지 (설정의 `AP-04` 와 같은 패턴). 측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0 (`SKILL.md` 둘 · 에이전트 아홉을 고친다)

## Reusability

- [ ] 재사용-01: N/A (새로 만드는 공용 코드 단위가 없다 — 고치는 코드는 기존 스크립트 둘 `validate.sh` · `trigger-check.sh` 의 번호 읽는 줄과 규약 문서의 정규식이다. 측정: 구조-02 `changed=` 에 새 파일 0 개 — `git diff --diff-filter=A --name-only 66e6c74b chore/ak3-id -- . ':(exclude).harness' | grep -c .` 이 0)
- [ ] 재사용-02: 정규식은 규약 문서 한 곳에 두고 공용 측정 파일은 사본 없이 그것을 읽는다. 측정: `bash harness/evals/measure/measure-helpers-test.sh` 에 `PASS M3-규약과같음 same_as_schema=1 copies=0` 줄이 있다

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: (커밋 뒤) `git diff --name-only 66e6c74b chore/ak3-id | grep -c '^scripts/release.sh$'` 이 0. 실제 오라클은 진단-02 · 구조-05)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude 는 빈 목록) — 바꾼 `.md` 의 더한 줄에 markdownlint 경고 0 · 고친 `.sh` 의 더한 줄에 shellcheck 경고 0, 그리고 레포 밖 목록 파일의 경고 수가 백업과 같다
  측정: `bash M/m-diag.sh <W> 66e6c74b /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl` 끝 줄 `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=<n>`, 목록 파일은 `MD013` 을 끈 같은 markdownlint-cli2 로 백업과 실제 파일을 각각 돌려 `grep -cE '^[^ ]+:[0-9]+'` 수가 같다 (봉인 전 원본 40 · 두 줄 뺀 사본 40)
- [ ] 진단-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` 로 릴리스 스크립트만 돈다 — 이번 변경 파일과 교집합 0 개. 실제 오라클은 구조-05 의 로컬 CI 전체)
- [ ] 진단-04: N/A (산출물에 구동할 앱 · 서버가 없다 — 변경은 문서 · 검사 스크립트 · 설정 · 문서 쪽 · 레포 밖 목록 파일. 실제 오라클은 구조-01 의 브라우저 측정 · 오류-03 의 훅 통째 실행)

사용자가 할 일: 없음
