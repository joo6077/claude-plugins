---
feature: "harness 스크립트 · 시험 · 커밋 안전 훅 남은 일 (HS-1~6 · CS-12)"
slug: after-0926-harness-scripts
created: "2026-09-26 19:59"
complexity: "복잡"
conditions: 29
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:46d0b11f882527e0
measurement_digest: sha256:457007c4f27ccb5e
locked_at: "2026-09-26 20:10"
---

## 배경

- 출처: 남은 일 목록 `.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md` 의 「## hs」 절 HS-1 ~ HS-6 과 「## cs」 절 CS-12.
  기준 판은 origin/main `6378948`. 작업 가지 `chore/ak2-hs` (워크트리 `.claude/worktrees/ak2-hs`).
- 합의: 사용자 위임 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 · 결정 답 2026-09-26T10:30:16.222Z
  (세션 `bda55d45-296c-491f-89ba-b52042d58e72`, 결정 파일 `.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`).
  이 계약의 합의는 그 위임으로 받았다. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다 — 개정 파일에 동의 칸을 비워 두고 부모가 사용자에게 묻는다.
- 여섯 항목과 CS-12 는 모두 기준 판에서 아직 열려 있다(아래 편집 전 감사의 줄 근거 · 회귀 게이트의 봉인 전 실측).
  - HS-1 피드백 저장: `HARNESS_CONTRACT` 를 줘도 계약 폴더를 셸 위치로 잡는다(실측 `contract_root=<T>/elsewhere`). 초안에 든 `sprint_slug` · `contract_path` · `session_id` · `contract_root` · `contract_path_inferred` 를 그대로 두고 같은 칸을 또 붙여 한 파일에 두 번 든다(실측 다섯 칸 중복). qa-evaluator 는 초안에 이 칸을 쓰라고 한다(`harness/agents/qa-evaluator.md:1105-1107`). sprint-contract Step 9 의 초안 이름은 고정 `.harness/feedback-draft.yaml` 이라 세션끼리 덮는다 — qa-evaluator 는 이미 `feedback-draft-<slug>.yaml` 이다(`:1089`).
  - HS-2 피드백 저장 시험이 고정 `/tmp/test-*.yaml` 아홉 자리를 써서 동시에 돌면 서로 지운다(실측 4 개 동시 3 회 = 12 회 중 12 회 실패). 사용자 HOME 에도 폴더 셋을 남긴다.
  - HS-3 커밋 안전 훅이 `git add <경로> && git commit`(그 경로의 삭제 60 개)과 하위 폴더에서의 `commit -a` · `git add -A && git commit`(폴더 밖 삭제 60 개)을 통과시킨다(실측 넷 다 exit 0).
  - HS-4 평가자 카이젠 회귀 패턴 `silent-check` 셋 중 #2 · #3 이 제목 글자만 봐서 본문을 비운 사본에서도 통과한다(실측).
  - HS-5 종료 코드 정의 파일의 「소비처」 표가 그 파일을 인용하는 스크립트 아홉 중 넷만 적는다 — 목록이 짚은 `check-reviewer-protocol-copies.py` 를 포함해 다섯이 빠졌다(실측).
  - HS-6 봉인 판 계약에서 측정 도우미 코드 블록을 떼는 일과 계약마다 되풀이되는 공통 정의를 Phase 3 · 4 · 7 · f1 이 저마다 스크래치 스크립트로 했다(`.harness/.meta/kaizen-0924/phase4-notes.md:139` · `phase7-notes.md:119` · `f1-harness-followups-notes.md:145`).
  - CS-12 계약의 `# sprint-scope` 블록은 자리만 정하고 쓰는 절차와 훅이 읽는 절차가 없다(`harness/README.md:67`). 이미 계약 열다섯이 그 블록을 쓰고 있다(모두 `status: done`).
- 사용자가 할 일: 없음

## GAP 분석

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하는가 | 예 — 셸 스크립트 · 훅 · 시험 · 계약 규약 문서 · CI 다섯 |
| 공개 API·계약 변경 | 바깥에 드러난 모양이 바뀌는가 | 예 — 저장된 피드백 YAML 의 칸 모양(`draft_*` 칸 추가, 중복 제거) · 커밋 훅이 막는 조건 · 계약 규약에 새 블록 절 · 새 공용 파일 둘 |
| 소비면 존재 | 반대편이 있는가 | 예 — qa-evaluator 초안 · `scripts/collect-kaizen-data.py` 가 피드백을 읽음 · 계약 작성자(sprint-contract) · 설치된 훅 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 훅이 정상 커밋을 막을 수 있고, 피드백 칸 우선순위가 바뀔 수 있다 |

네 축 모두 예 → **복잡**. 기능 조건은 Step 6.2 둘째 명령으로 센다(9~20 안).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유에 그대로) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 같은 값 (DG-03 N/A 사유에 그대로) |
| `diagnostics.ide_exclude` | `[]` | `[]` — 제외 없음 |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 네 절 모두 씀 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence(`command`) · AP-04 frontmatter name 누락 | AP-02 · AP-03 · AP-04 선별 (AP-01 은 버전을 다루는 파일이 없어 뺌) |

### 1.4 편집 전 감사 (기준 판 `6378948` 을 실제로 읽은 줄)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `harness/scripts/save-feedback.sh` | `:112-135` `resolve_contract_root` · `:233-244` 슬러그·계약 경로 · `:296-298` sed 가 project 두 칸만 이름 바꿈 · `:305-322` 다섯 칸을 뒤에 붙임 | 계약 경로를 줘도 계약 폴더를 셸 위치로 잡음 · 초안 칸 중복 | SC-01 · SC-02 |
| `harness/skills/sprint-contract/SKILL.md` | `:565` Step 6 · `:831` 초안 경로 · `:856` 저장 명령 | 고정 초안 이름 · 범위 블록 쓰는 절차 없음 | SK-01 · SK-02 |
| `harness/skills/init/SKILL.md` | `:61` `.harness/feedback-draft.yaml`만 개별 무시 | 슬러그 초안 이름을 못 덮음 | SK-01 |
| `harness/agents/qa-evaluator.md` | `:1089` `feedback-draft-<slug>.yaml` · `:1093-1095` 초안에 slug · 계약 경로 · 세션 칸 · `:679` 「50 개를 넘는 삭제만 막으므로」 · `:917-923` Check Artifacts 절 | 초안에 식별 칸을 쓰게 해 중복의 한쪽 원인 · 훅 설명이 범위 검사를 모름 | SK-04 (679 한 줄) · SC-08 (917 절은 읽기만) |
| `harness/evals/kaizen/feedback-system/save-test.sh` | `:45` `:74` `:106` `:113` `:123` `:127-128` `:164` `:182` 고정 `/tmp/` · `:150` 만 mktemp | 동시 실행 충돌 · HOME 에 폴더 남김 · HS-1 경우 없음 | SC-03 · SC-04 |
| `harness/scripts/commit-guard.sh` | `:234-245` 작업 폴더 삭제 얹기 · `:235` `ls-files --deleted` 가 셸 위치 아래만 셈 · `:303-336` `git add` 는 `.` · `:/` · `-A` · `-u` 만 올림 표시 · `:256` 되돌림 검사는 `add_all` 이면 꺼짐 | HS-3 두 모양 · 범위 블록을 읽지 않음 | SC-05 · SC-06 · ER-02 |
| `harness/evals/hooks/commit-guard-test.sh` | `:1-8` 번호 규칙 · `:9` `COMMIT_GUARD_HOOK` 로 훅 바꾸기 · `:302` 끝 판정 | HS-3 · 범위 경우 없음 | SC-07 |
| `harness/evals/kaizen/evaluator-kaizen/assertions.json` | `:15-19` `silent-check` 셋 | #2 `## Check Artifacts` · #3 `### 산출물이 검사일 때` 가 제목 글자만 봄 | SC-08 |
| `scripts/run-kaizen-assertions.py` | `:26` `KNOWN_TYPES = ("file_contains",)` · `:81` `re.findall(pattern, text)` 플래그 없음 | 여러 줄을 보려면 패턴에 `\n` 을 써야 한다 — 러너는 바꾸지 않는다(vs 묶음) | SC-08 측정 전제 |
| `harness/evals/gate-exit-codes.md` | `:61-68` 「## 소비처」 표 넷 | 인용하는 스크립트 다섯이 표에 없음 | SC-09 |
| `harness/references/contract-schema.md` | `:234-249` `fm_get` · `:310-348` 봉인 함수 다섯 · `:693-701` `sprint_head` · `:732-743` `mine` · `unsigned_on` · `:551-576` §검증 수단 인라인 명시 | 공용 측정 파일 안내 없음 · 범위 블록 절 없음 | SK-02 · SK-03 · SC-11 |
| `harness/README.md` | `:44-74` 「## 커밋 안전 훅」 · `:67` 「아직 막지 않는다」 · 「아직 없다」 | 구현 뒤 사실과 어긋남 | SK-04 |
| `harness/docs/guides/skill-design-guide.md` | `:284` Scope-Bound Edits 행 | 현재 등급 칸이 범위 검사를 모름 | SK-04 |
| `harness/docs/guides/qa-evaluation-guide.md` | `:700-703` 배경 인용 「50 개를 넘는 삭제만 막는다」 | 같음 | SK-04 |
| `.github/workflows/ci.yml` | `:152-171` harness 작업(피드백 저장 시험 · 훅 시험) · `:83` 다른 작업의 zsh 설치 줄 | 새 시험을 돌리는 단계 없음 | SC-12 |
| `scripts/collect-kaizen-data.py` | `:169-175` `sprint_slug` · `contract_path` 가 있으면 신형 세대 · `:615` `yaml.safe_load` | 칸이 한 번씩만 들어도 같은 값을 읽음 | AR-02 |

구현 방향 결정(선택지 하나씩만 남김 — 부모 위임으로 확정):

- HS-1 계약 폴더: `HARNESS_CONTRACT_ROOT` > `HARNESS_CONTRACT` 가 가리키는 파일의 `.harness/` 위 폴더 > 기존 조상 탐색. 초안의 다섯 칸은 `project_*` 처럼 `draft_<칸>` 으로 이름을 바꿔 보존하고 최종 칸은 한 번만 쓴다. 값 우선순위는 지금과 같다(`sprint_slug` 환경 > 초안 > 계약 파일 이름 · `contract_path` 환경 > 초안 · `session_id` 환경 > 초안).
- HS-1 초안 이름: sprint-contract Step 9 도 qa-evaluator 와 같은 `.harness/feedback-draft-<slug>.yaml`(plain 모드만 `feedback-draft.yaml`). init 은 `.harness/feedback-draft*.yaml` 를 무시하라고 적는다.
- HS-3 (a): 같은 명령의 `git add <경로>` 는 그 경로의 작업 폴더 상태(삭제 포함)를 목록 사본에 얹어 센다. `add_all` 은 켜지 않는다 — 되돌림 검사가 꺼지지 않게. (b): `commit -a` · `add -A` · `add -u` 는 저장소 전체 삭제를 센다. 하위 폴더의 `git add .` 는 그 폴더만 센다(지금 동작 유지).
- CS-12: 커밋 직전 훅이 커밋 폴더에서 위로 처음 만나는 `.harness/` 의 계약 가운데 `status: active` 이고 `owner_session` 이 훅 입력의 `session_id`(없으면 `CLAUDE_CODE_SESSION_ID`)와 같은 것의 `## 범위 경계` 안 블록을 모아(여럿이면 합집합) 커밋이 싣는 경로를 대조한다. `.harness/` 아래는 늘 허용. 판단이 안 서면(세션 없음 · 해당 계약 없음 · 블록 없음 · 못 읽음) 조용히 통과.
- HS-6: 새 파일 셋 — `harness/scripts/extract-helpers.py`(떼기) · `harness/scripts/measure-common.sh`(공통 정의, 스키마 블록을 읽어 쓰고 사본을 두지 않음) · `harness/evals/measure/measure-helpers-test.sh`(시험, CI 에서 돎).

### Counterpart — 바뀌는 모양을 받아 쓰는 반대편

| 바뀌는 것 | 반대편 | 조건 |
| --------- | ------ | ---- |
| 저장 피드백 칸 모양 | `scripts/collect-kaizen-data.py` · `scripts/test-collect-kaizen-data.py` | AR-02 (기존 시험 통과 · 값 불변은 SC-02) |
| 초안 이름 | `harness/agents/qa-evaluator.md:1101` (이미 슬러그 이름 — 바꾸지 않음) · `harness/skills/init/SKILL.md:61` | SK-01 |
| 훅이 막는 조건 | `harness/README.md` · `skill-design-guide.md:288` · `qa-evaluation-guide.md:707` · `qa-evaluator.md:689` | SK-04 |
| 계약 규약 새 블록 | 계약 작성자 `harness/skills/sprint-contract/SKILL.md` Step 6 | SK-02 |
| 새 공용 파일 | 계약 규약 §검증 수단 인라인 명시 한 줄 · 종료 코드 소비처 표 | SK-03 · SC-09 |

### 조건 작성 자문 (contract-schema §조건 작성 preflight)

- 측정-수단-부재 · 측정-방식-불일치 — 모든 기능 조건에 도우미 명령과 기대 출력을 들여 적었다. 기준 판 값은 회귀 게이트 절의 봉인 전 실측이다
- 측정-산출물-부재 — 도우미는 이 계약의 코드 블록, 두 판은 공통 정의가 푼다
- 음성 대조 — 시험 통과로 판정하는 조건(SC-03 · SC-07 · SC-12)에 기준 판 스크립트를 끼운 실행을 적었다
- 양성 대조 — 0 이 기대값인 측정(중복 칸 · 범위 밖 경로 · 고정 경로 · 경고 증가)은 기준 판에서 0 이 아닌 값을 실측해 적었다

## 범위 경계

- 이 스프린트가 고치는 경로는 아래 블록이 전부다. `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 셋이다(AR-01 이 따로 잰다)

```text
# sprint-scope
harness/scripts/save-feedback.sh
harness/scripts/commit-guard.sh
harness/scripts/extract-helpers.py
harness/scripts/measure-common.sh
harness/evals/kaizen/feedback-system/save-test.sh
harness/evals/hooks/commit-guard-test.sh
harness/evals/measure/measure-helpers-test.sh
harness/evals/kaizen/evaluator-kaizen/assertions.json
harness/evals/gate-exit-codes.md
harness/references/contract-schema.md
harness/skills/sprint-contract/SKILL.md
harness/skills/init/SKILL.md
harness/README.md
harness/agents/qa-evaluator.md
harness/docs/guides/qa-evaluation-guide.md
harness/docs/guides/skill-design-guide.md
.github/workflows/ci.yml
```

- 커밋 나누기: `.github/workflows/ci.yml` 은 `harness/` 변경과 따로 커밋한다 — AR-01 (c) 가 커밋마다 최상위 폴더 하나만 허용한다. `.harness/` 쪽 계약 · 개정 · 피드백도 따로 커밋한다
- `harness/scripts/measure-common.sh` · `harness/evals/measure/measure-helpers-test.sh` 는 `gate-exit-codes.md` 를 인용하지 않는다. 인용하게 되면 SC-09 의 `missing=0 extra=0` 이 그 행까지 요구하므로 표에 행을 더한다
- `harness/scripts/feedback-path.sh` 는 전역 저장 폴더만 계산하고 계약 폴더를 다루지 않는다(기준 판 전문 31 줄을 읽음) — HS-1 과 겹치는 계산이 없어 범위에 넣지 않는다
- 교차 진단(qa-evaluator, 봉인 전) 반영: SK-03 한 줄 문구 · SK-04 (c)(d) 문구 · SC-07 경우 수 · SC-12 환경 변수 · ER-02 빈 블록 · 주인 칸 없는 계약 두 경우 · AR-01 열일곱의 뜻 · SC-02 반대편 줄 · 위 커밋 나누기 · SC-09 인용 규칙. 모두 조건을 좁히는 쪽이다
- 하지 않는 것: `scripts/run-kaizen-assertions.py` 에 새 패턴 종류를 더하지 않는다(vs 묶음 · VS-1). HS-4 는 패턴 글자만 고친다
- 하지 않는 것: markdownlint 기존 경고를 이 계약에서 고치지 않는다 — DG-02 는 「늘리지 않는다」 만 잰다. 사용자 결정 UD-7(범위 밖 경고 전부 고침)은 부모가 따로 맡긴다
- 하지 않는 것: `reflect-kit/skills/reflect-digest/SKILL.md:28` 의 `.harness/feedback-draft.yaml` 언급은 「초안은 digest 입력이 아니다」 라는 뜻이라 이름이 바뀌어도 틀리지 않는다. 다른 킷이라 이 묶음에서 건드리지 않는다
- 하지 않는 것: `harness/references/feedback-schema.yaml` 에 `draft_*` 칸을 적지 않는다 — 그 파일은 `draft_project_*` 도 적지 않고 있고, cs 묶음(CS-1)이 고치는 파일이다
- 하지 않는 것: `harness/skills/sprint/SKILL.md:201` 「지정한 경로 안의 삭제가 50 개를 넘으면 막는다」 는 구현 뒤에도 참이라 둔다
- 하지 않는 것: 계약 스키마 버전 표를 올리지 않는다 — cs 묶음이 같은 파일 측정 절을 고친다. 새 절에 날짜만 붙인다
- 다른 묶음과 같은 파일: `harness/skills/sprint-contract/SKILL.md`(Step 6 · Step 9 두 자리만) · `harness/references/contract-schema.md`(새 절 하나 · §검증 수단 인라인 명시 한 줄만)
- 처리 표

| ID | 처리 | 근거 |
| -- | ---- | ---- |
| HS-1 | 계약에 넣음 | SC-01 · SC-02 · SC-03 · SK-01 |
| HS-2 | 계약에 넣음 | SC-04 |
| HS-3 | 계약에 넣음 | SC-05 · SC-07 |
| HS-4 | 계약에 넣음 | SC-08 |
| HS-5 | 계약에 넣음 | SC-09 (목록이 짚은 한 행에 더해, 같은 결함인 빠진 행 넷과 새 스크립트 행까지) |
| HS-6 | 계약에 넣음 | SC-10 · SC-11 · SC-12 · SK-03 · ER-01 |
| CS-12 | 계약에 넣음 | SK-02 · SK-04 · SC-06 · SC-07 · ER-02 |

- 커버리지 해소: SK-01 — 산문의 세 이름은 측정의 `grep` 패턴(`feedback-draft-<slug>\.yaml` · `feedback-draft\.yaml` · `.harness/feedback-draft*.yaml`)이다. 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다
- 커버리지 해소: SK-02 — 아홉 글자(`.harness/` · `harness/scripts/commit-guard.sh` 포함)는 측정의 「글자마다 … (아홉 번)」 반복이 하나씩 잰다
- 커버리지 해소: SK-04 — 네 파일은 측정의 `"$T/E/harness/README.md"` · `"$T/E/harness/docs/guides/skill-design-guide.md"` · `<파일>` 두 경로(`$T/E/harness/docs/guides/qa-evaluation-guide.md` · `$T/E/harness/agents/qa-evaluator.md`)다
- 커버리지 해소: SC-01 · SC-06 — 산문의 경로(`<proj>/.harness/sprint-contract-demo.md` · `docs/*.md` · `sub/` · `.harness/`)는 도우미 `hs1.sh` · `scope.sh` 가 만드는 시험 저장소 안 경로다
- 커버리지 해소: SC-09 — 인용 스크립트 집합(`scripts/` · `harness/scripts/` · `harness/evals/` 아래 `.py` · `.sh` · `.js`)은 도우미 `hs5.sh` 의 `grep -rl` 이 모으고, 여섯 행은 측정의 `grep -cF` 를 행마다 한 번 돈다
- 커버리지 해소: AR-01 — `.harness/` 세 파일은 도우미 `scopediff.sh` 의 허용 정규식이, `chore/ak2-hs` 는 공통 정의의 `BR` 이, `B..END` 는 공통 정의의 두 값이 잰다

## 회귀 게이트 — 측정 공통 정의 · 도우미 · 봉인 전 실측

모든 측정은 공통 정의(`common.sh`)를 먼저 읽은 **bash** 에서 돈다: `K=<도우미 폴더> bash -c '. "$K/common.sh"; <측정>'`.
`END_UNRESOLVED` 가 찍히면 종료 코드 2 로 끝난다. `HEAD` 로 바꿔 재지 않는다. 상한은 가지 `refs/heads/chore/ak2-hs` 끝이다.

도우미 준비 — 이 절의 bash 코드 블록 가운데 첫 `#` 주석 줄(셔뱅 다음)이 `# <이름>.sh ` 로 시작하는 것을 그 이름으로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. 떼는 명령:

```bash
# 이 계약에서 도우미 블록을 떼어 $K 에 저장한다 (구현 전에도 쓰는 방법 — 구현 뒤에는 SC-10 이 같은 결과를 새 스크립트로 확인한다)
K=${K:?도우미 폴더}; mkdir -p "$K"
python3 - /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-hs/.harness/sprint-contract-after-0926-harness-scripts.md "$K" <<'PY'
import re, sys, pathlib
src = open(sys.argv[1], encoding="utf-8").read(); K = pathlib.Path(sys.argv[2])
for body in re.findall(r"^```(?:bash|python)\n(.*?)^```$", src, re.S | re.M):
    lines = body.splitlines(); i = 1 if lines and lines[0].startswith("#!") else 0
    m = re.match(r"# ([\w.-]+\.(?:sh|py)) ", lines[i]) if len(lines) > i else None
    if m:
        (K / m.group(1)).write_text(body, encoding="utf-8")
PY
```

준비 단계 실측(2026-09-26): `command -v shellcheck` → `/opt/homebrew/bin/shellcheck` (0.11.0) · `command -v actionlint` → `/opt/homebrew/bin/actionlint` · `command -v jq` → `/usr/bin/jq` ·
`command -v zsh` → `/bin/zsh` · `command -v yq` → 없음(피드백 시험은 python 경로) · `python3 -c 'import yaml'` 성공(6.0.3) ·
markdownlint 는 스크래치에 `npm install --no-save markdownlint-cli2@0.23.2` 로 깔고 `--version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`, 설정은 `{ "config": { "MD013": false } }` 한 줄 파일(편집기 확장과 같은 조건). 경로를 `ML` · `MLCFG` 에 넣는다.
도우미는 모두 `mktemp -d "${TMPDIR:-/tmp}/…"` 임시 폴더와 `GIT_CONFIG_GLOBAL=/dev/null` 임시 저장소만 쓰고 끝나면 지운다. 작업 폴더는 건드리지 않는다.

측정 공통 정의 — 두 판을 풀고 절 자르기 함수를 둔다:

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다: K=<도우미 폴더> bash -c '. "$K/common.sh"; <측정>'
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-hs
B=63789486b72b8998be924fd54d56ae7465e76b21        # origin/main — 이 가지를 만든 판
BR=refs/heads/chore/ak2-hs
CF=.harness/sprint-contract-after-0926-harness-scripts.md
: "${K:?도우미 폴더를 K 에 넣는다}"
END=$(git -C "$W" rev-parse --verify -q "$BR^{commit}") || { echo "END_UNRESOLVED $BR — HEAD 로 바꿔 재지 않는다"; exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/hs.XXXXXX") || exit 2
T=$(cd "$T" && pwd -P) || exit 2
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 두고 거기서 잰다 — 작업 폴더의 미커밋 변경이 끼지 않는다
git -C "$W" archive "$B" | tar -x -C "$T/B" || exit 2
git -C "$W" archive "$END" | tar -x -C "$T/E" || exit 2
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하 다음 제목 전까지. 코드 펜스 안 # 줄은 제목이 아니다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
export T K W B END CF
```

SC-01 · SC-02 — 피드백 저장:

```bash
#!/usr/bin/env bash
# hs1.sh <save-feedback.sh> — 피드백 저장의 계약 폴더 · 식별 칸 중복을 세 경우(A 환경 세션 · B 초안 세션만 · C 없는 계약 경로)로 잰다
S=${1:?save-feedback.sh}
X=$(mktemp -d "${TMPDIR:-/tmp}/hs1.XXXXXX") || exit 2; X=$(cd "$X" && pwd -P); trap 'rm -rf "$X"' EXIT
mkdir -p "$X/home" "$X/proj/.harness" "$X/elsewhere"; : >"$X/proj/.harness/sprint-contract-demo.md"
mkdraft() { cat >"$1" <<'YAML'
schema_version: 1
timestamp: "2026-03-30T10:00:00+09:00"
skill: qa-evaluator
skill_version: "0.3.3"
outcome: completed
sprint_slug: draftslug
contract_path: /somewhere/.harness/sprint-contract-demo.md
session_id: sess-draft
contract_root: /somewhere
contract_path_inferred: false
diagnosis:
  checklist:
    ambiguous_conditions: false
YAML
}
report() {  # report <라벨> <rc> <저장본>
  python3 - "$1" "$2" "$3" "$X" <<'PY'
import sys, yaml, hashlib
lab, rc, path, X = sys.argv[1:5]
seen = []
class L(yaml.SafeLoader): pass
def cm(loader, node, deep=False):
    keys = [loader.construct_object(k) for k, _ in node.value]
    if not seen: seen.append(keys)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)
L.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, cm)
try:
    d = yaml.load(open(path, encoding="utf-8"), Loader=L)
except Exception as e:
    print(f"{lab} rc={rc} unreadable={e.__class__.__name__}"); sys.exit(0)
top = seen[-1] if seen else []
# 맨 위 매핑은 마지막에 끝나므로 construct 순서상 마지막 기록이 아니라 가장 긴 키 목록이 맨 위다
top = max(seen, key=len) if seen else []
dup = sorted({k for k in top if top.count(k) > 1})
root = str(d.get("contract_root", "")).replace(X + "/", "")
ren = sum(1 for k in ("sprint_slug","contract_path","session_id","contract_root","contract_path_inferred") if f"draft_{k}" in d)
want = hashlib.sha256((X + "/proj").encode()).hexdigest()[:8]
cp = str(d.get("contract_path", "")).replace(X + "/", "")
print(f"{lab} rc={rc} root={root} hash={'ok' if d.get('project_hash') == want else 'other'} dup={','.join(dup) or 'none'} "
      f"sprint_slug={d.get('sprint_slug')} contract_path={cp} session_id={d.get('session_id')} renamed={ren}")
PY
}
mkdraft "$X/a.yaml"
A=$(cd "$X/elsewhere" && HOME="$X/home" CLAUDE_CODE_SESSION_ID=sess-env HARNESS_CONTRACT="$X/proj/.harness/sprint-contract-demo.md" bash "$S" evaluator "$X/a.yaml" 2>"$X/a.err"); rc=$?
report A "$rc" "$A"
mkdraft "$X/b.yaml"
Bp=$(cd "$X/elsewhere" && HOME="$X/home" env -u CLAUDE_CODE_SESSION_ID HARNESS_CONTRACT="$X/proj/.harness/sprint-contract-demo.md" bash "$S" evaluator "$X/b.yaml" 2>"$X/b.err"); rc=$?
report B "$rc" "$Bp"
mkdraft "$X/c.yaml"
C=$(cd "$X/elsewhere" && HOME="$X/home" CLAUDE_CODE_SESSION_ID=sess-env HARNESS_CONTRACT="$X/proj/.harness/sprint-contract-gone.md" bash "$S" evaluator "$X/c.yaml" 2>"$X/c.err"); rc=$?
echo "C rc=$rc root=$(sed -n "s/^contract_root:[[:space:]]*//p" "$C" 2>/dev/null | tail -1 | tr -d "'" | sed "s#$X/##") warn=$(grep -c 'HARNESS_CONTRACT' "$X/c.err")"
mkdraft "$X/d.yaml"; mkdir -p "$X/root2/.harness"
D=$(cd "$X/elsewhere" && HOME="$X/home" CLAUDE_CODE_SESSION_ID=sess-env HARNESS_CONTRACT_ROOT="$X/root2" HARNESS_CONTRACT="$X/proj/.harness/sprint-contract-demo.md" bash "$S" evaluator "$X/d.yaml" 2>/dev/null); rc=$?
echo "D rc=$rc root=$(sed -n "s/^contract_root:[[:space:]]*//p" "$D" 2>/dev/null | tail -1 | tr -d "'" | sed "s#$X/##")"
# 반대편 — 모은 저장본 넷을 수집기가 읽는가 (draft_* 칸이 섞인 채로)
CK=$(cd "$(dirname "$S")/../.." && pwd -P)/scripts/collect-kaizen-data.py
E=$(HOME="$X/home" python3 - "$CK" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ck", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.collect_global_feedback()
print(f"total={r['total']} parse_failed={r['parse_failed']} deterministic={sum(v for k, v in r['by_generation'].items() if 'deterministic' in k)}")
PY
)
echo "E collect $E"
```

SC-05 — 커밋 안전 훅 삭제 모양:

```bash
#!/usr/bin/env bash
# hs3.sh <commit-guard.sh> — 커밋 안전 훅이 놓치던 두 모양과 지켜야 할 모양을 임시 저장소에서 돌려 모양마다 종료 코드를 낸다
hook=${1:?hook}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
unset HARNESS_COMMIT_GUARD GIT_INDEX_FILE CLAUDE_CODE_SESSION_ID
work=$(mktemp -d "${TMPDIR:-/tmp}/hs3.XXXXXX") || exit 2; trap 'rm -rf "$work"' EXIT
mk() { local r=$1 k; mkdir -p "$r/d1" "$r/sub"; git -C "$r" init -q -b main
  for ((k=1;k<=60;k++)); do printf 'l%d\n' $k >"$r/d1/$(printf 'f%03d' $k)"; done
  echo s >"$r/sub/s.txt"; echo a >"$r/a.txt"; git -C "$r" add -A; git -C "$r" commit -qm init; }
rmw() { local k; for ((k=1;k<=60;k++)); do rm -f "$1/d1/$(printf 'f%03d' $k)"; done; }
run() { jq -nc --arg c "$2" --arg d "$3" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}' | bash "$hook" pre >/dev/null 2>"$work/err"; echo "$1 exit=$? $(head -1 "$work/err" | grep -oE '삭제 [0-9]+ 개|되돌리는 파일 [0-9]+ 개')"; }
r=$work/a1; mk $r; rmw $r; run a1 'git add d1 && git commit -m x' "$r"
r=$work/a2; mk $r; rmw $r; run a2 'git add d1/ && git commit -m x' "$r"
r=$work/b1; mk $r; rmw $r; run b1 'git commit -am x' "$r/sub"
r=$work/b2; mk $r; rmw $r; run b2 'git add -A && git commit -m x' "$r/sub"
r=$work/k0; mk $r; rmw $r; run k0 'git commit -am x' "$r"
r=$work/k1; mk $r; rmw $r; run k1 'git add . && git commit -m x' "$r/sub"
r=$work/k2; mk $r; echo v1 >"$r/f2"; git -C "$r" add f2; git -C "$r" commit -qm v1; echo v2 >"$r/f2"; git -C "$r" commit -qam v2
old=$(git -C "$r" rev-parse HEAD~1:f2); git -C "$r" update-index --cacheinfo "100644,$old,f2"; echo z >>"$r/a.txt"
run k2 'git add a.txt && git commit -m x' "$r"
r=$work/k3; mk $r; rmw $r; echo z >>"$r/a.txt"; run k3 'git add a.txt && git commit -m x' "$r"
```

SC-06 · ER-02 — 범위 목록 검사:

```bash
#!/usr/bin/env bash
# scope.sh <commit-guard.sh> — 계약 # sprint-scope 블록을 읽는 커밋 검사를 경우마다 임시 저장소에서 돌려 종료 코드를 낸다
hook=${1:?hook}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
unset HARNESS_COMMIT_GUARD GIT_INDEX_FILE CLAUDE_CODE_SESSION_ID
work=$(mktemp -d "${TMPDIR:-/tmp}/scope.XXXXXX") || exit 2; trap 'rm -rf "$work"' EXIT
contract() {  # contract <파일> <status> <owner> [블록 줄…] — 블록 줄이 없으면 블록 없는 계약
  local f=$1 st=$2 ow=$3; shift 3
  { printf -- '---\nfeature: "x"\nstatus: %s\nowner_session: %s\n---\n\n## 범위 경계\n\n- 설명\n' "$st" "$ow"
    if [ $# -gt 0 ]; then printf '\n```text\n# sprint-scope\n'; printf '%s\n' "$@"; printf '```\n'; fi
    printf '\n## Script\n\n- [ ] SC-01: x\n'; } >"$f"; }
mk() { local r=$1; mkdir -p "$r/d1" "$r/docs" "$r/sub" "$r/.harness"; git -C "$r" init -q -b main
  echo 1 >"$r/d1/f001"; echo 2 >"$r/d1/f002"; echo a >"$r/a.txt"; echo x >"$r/docs/x.md"; echo s >"$r/sub/s.txt"
  contract "$r/.harness/sprint-contract-s.md" active S d1/f001 'docs/*.md' sub/
  contract "$r/.harness/sprint-contract-t.md" done S a.txt
  contract "$r/.harness/sprint-contract-u.md" active OTHER a.txt
  git -C "$r" add -A; git -C "$r" commit -qm init; }
run() {  # run <이름> <명령> <폴더> <세션|-> — 세션 - 이면 입력에 session_id 를 넣지 않는다
  local p
  if [ "$4" = - ]; then p=$(jq -nc --arg c "$2" --arg d "$3" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}')
  else p=$(jq -nc --arg c "$2" --arg d "$3" --arg s "$4" '{session_id:$s,hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}'); fi
  printf '%s' "$p" | bash "$hook" pre >/dev/null 2>"$work/err"; rc=$?
  echo "$1 exit=$rc names=[$(grep -oE '(a\.txt|moved\.txt|d1/f001|docs/[a-z]+\.md|sub/s\.txt|\.harness/[a-z.-]+)' "$work/err" | sort -u | tr '\n' ' ' | sed 's/ $//')]"; }
n=0; nr() { n=$((n+1)); r=$work/r$n; mk "$r"; }
nr; echo z >>"$r/a.txt"; git -C "$r" add a.txt;            run s01-out 'git commit -m x' "$r" S
nr; echo z >>"$r/d1/f001"; git -C "$r" add d1/f001;        run s02-in 'git commit -m x' "$r" S
nr; echo n >"$r/.harness/notes.md"; git -C "$r" add .harness; run s03-harness 'git commit -m x' "$r" S
nr; echo y >"$r/docs/y.md"; git -C "$r" add docs;          run s04-glob 'git commit -m x' "$r" S
nr; echo z >>"$r/sub/s.txt"; git -C "$r" add sub;          run s05-dir 'git commit -m x' "$r" S
nr; echo z >>"$r/a.txt"; git -C "$r" add a.txt;            run s06-other-session 'git commit -m x' "$r" Z
nr; echo z >>"$r/a.txt"; git -C "$r" add a.txt
p=$(jq -nc --arg c 'git commit -m x' --arg d "$r" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}')
printf '%s' "$p" | CLAUDE_CODE_SESSION_ID=S bash "$hook" pre >/dev/null 2>"$work/err"; echo "s07-env-session exit=$?"
nr; echo z >>"$r/a.txt";                                     run s08-path-commit 'git commit -o a.txt -m x' "$r" S
nr; echo z >>"$r/a.txt";                                     run s09-add-commit 'git add a.txt && git commit -m x' "$r" S
nr; echo z >>"$r/a.txt";                                     run s10-commit-a 'git commit -am x' "$r" S
nr; echo z >>"$r/a.txt"; git -C "$r" add a.txt;            run s11-off 'HARNESS_COMMIT_GUARD=off git commit -m x' "$r" S
nr; contract "$r/.harness/sprint-contract-v.md" active S a.txt; git -C "$r" add .harness; git -C "$r" commit -qm v
echo z >>"$r/a.txt"; git -C "$r" add a.txt;                  run s12-union 'git commit -m x' "$r" S
nr; git -C "$r" mv d1/f001 moved.txt;                        run s13-rename-out 'git commit -m x' "$r" S
nr; contract "$r/.harness/sprint-contract-s.md" active S; git -C "$r" add .harness; git -C "$r" commit -qm noblock
echo z >>"$r/a.txt"; git -C "$r" add a.txt;                  run s14-no-block 'git commit -m x' "$r" S
nr; git -C "$r" rm -q d1/f001;                               run s15-delete-in 'git commit -m x' "$r" S
nr; echo z >>"$r/a.txt"; echo z >>"$r/d1/f001"; git -C "$r" add a.txt d1/f001; run s16-mixed 'git commit -m x' "$r" S
nr; echo z >>"$r/sub/s.txt";                                 run s17-subdir-a 'git commit -am x' "$r/sub" S
nr; echo z >>"$r/a.txt"; git -C "$r" add a.txt;            run s18-no-session 'git commit -m x' "$r" -
nr; echo z >>"$r/a.txt";                                     run s19-subdir-a-out 'git commit -am x' "$r/sub" S
nr; chmod 000 "$r/.harness/sprint-contract-s.md"; echo z >>"$r/a.txt"; git -C "$r" add a.txt; run s20-unreadable 'git commit -m x' "$r" S; chmod 644 "$r/.harness/sprint-contract-s.md"
nr; printf -- '---\nstatus: active\nowner_session: S\n---\n\n## 배경\n\n```text\n# sprint-scope\nd1/f001\n```\n\n## 범위 경계\n\n- 없음\n' >"$r/.harness/sprint-contract-s.md"
git -C "$r" add .harness; git -C "$r" commit -qm moved; echo z >>"$r/a.txt"; git -C "$r" add a.txt; run s21-block-outside 'git commit -m x' "$r" S
nr; printf -- '---\nstatus: active\nowner_session: S\n---\n\n## 범위 경계\n\n```text\n# sprint-scope\n```\n' >"$r/.harness/sprint-contract-s.md"
git -C "$r" add .harness; git -C "$r" commit -qm empty; echo z >>"$r/a.txt"; git -C "$r" add a.txt; run s22-empty-block 'git commit -m x' "$r" S
nr; printf -- '---\nstatus: active\n---\n\n## 범위 경계\n\n```text\n# sprint-scope\nd1/f001\n```\n' >"$r/.harness/sprint-contract-s.md"
git -C "$r" add .harness; git -C "$r" commit -qm noowner; echo z >>"$r/a.txt"; git -C "$r" add a.txt; run s23-no-owner 'git commit -m x' "$r" S
```

SC-08 — silent-check 본문 민감도:

```bash
#!/usr/bin/env bash
# hs4.sh <풀어 둔 판> — 평가자 카이젠 silent-check 세 패턴을 원본 사본과 「제목만 남기고 본문을 비운」 사본에서 돌린다
R=${1:?root}
X=$(mktemp -d "${TMPDIR:-/tmp}/hs4.XXXXXX") || exit 2; trap 'rm -rf "$X"' EXIT
for v in orig empty; do mkdir -p "$X/$v"; (cd "$R" && tar -cf - scripts harness .claude-plugin) | tar -xf - -C "$X/$v" || exit 2; done
cut_body() { awk -v h="$2" '
  f && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) f = 0 }
  !f && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  !f' "$1" >"$1.new" && mv "$1.new" "$1"; }
body_n() { awk -v h="$2" 'f && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit } f && NF { n++ } !f && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1 } END { print n+0 }' "$1"; }
cut_body "$X/empty/harness/agents/qa-evaluator.md" "## Check Artifacts"
cut_body "$X/empty/harness/docs/guides/qa-evaluation-guide.md" "### 산출물이 검사일 때"
for v in orig empty; do echo "$v body qa=$(body_n "$X/$v/harness/agents/qa-evaluator.md" "## Check Artifacts") guide=$(body_n "$X/$v/harness/docs/guides/qa-evaluation-guide.md" "### 산출물이 검사일 때")"; done
for v in orig empty; do
  out=$(cd "$X/$v" && python3 scripts/run-kaizen-assertions.py); rc=$?
  echo "$v rc=$rc $(printf '%s\n' "$out" | grep 'silent-check' | awk '{print $1 ":" $2}' | sed 's#evaluator-kaizen/##' | tr '\n' ' ')"
done
```

SC-09 — 종료 코드 소비처 표:

```bash
#!/usr/bin/env bash
# hs5.sh <풀어 둔 판> — 종료 코드 정의 파일을 인용하는 스크립트 집합과 「소비처」 표 행 집합을 맞댄다
R=${1:?}; cd "$R" || exit 2
G=harness/evals/gate-exit-codes.md
[ -f "$G" ] || exit 2
cite=$(grep -rl --include='*.py' --include='*.sh' --include='*.js' 'gate-exit-codes' scripts harness/scripts harness/evals | grep -vxF "$G" | LC_ALL=C sort -u)
rows=$(awk '/^## 소비처/{f=1;next} f&&/^## /{exit} f&&/^\| `/{s=$0; sub(/^\| `/,"",s); sub(/`.*/,"",s); print s}' "$G" | LC_ALL=C sort -u)
miss=$(LC_ALL=C comm -23 <(printf '%s\n' "$cite") <(printf '%s\n' "$rows") | grep -c .)
extra=$(LC_ALL=C comm -13 <(printf '%s\n' "$cite") <(printf '%s\n' "$rows") | grep -c .)
echo "cite=$(printf '%s\n' "$cite" | grep -c .) rows=$(printf '%s\n' "$rows" | grep -c .) missing=$miss extra=$extra"
LC_ALL=C comm -23 <(printf '%s\n' "$cite") <(printf '%s\n' "$rows") | sed 's/^/  missing /'
awk '/^## 소비처/{f=1;next} f&&/^## /{exit} f&&/^\| `/' "$G"
```

SC-04 — 피드백 저장 시험 동시 실행:

```bash
#!/usr/bin/env bash
# race.sh <풀어 둔 판> [동시 수] [회차] — 같은 피드백 저장 시험을 동시에 돌려 실패 수를 세고, 한 번 돌린 뒤 HOME 에 남은 것을 센다
R=${1:?root}; N=${2:-4}; RR=${3:-3}
O=$(mktemp -d "${TMPDIR:-/tmp}/race.XXXXXX") || exit 2; trap 'rm -rf "$O"' EXIT
fails=0; total=0
for r in $(seq 1 "$RR"); do
  for i in $(seq 1 "$N"); do { ( cd "$R" && HOME="$O/h$r-$i" bash harness/evals/kaizen/feedback-system/save-test.sh >"$O/$r-$i.log" 2>&1 ); echo $? >"$O/$r-$i.rc"; } & done
  wait
  for i in $(seq 1 "$N"); do total=$((total+1)); [ "$(cat "$O/$r-$i.rc")" = 0 ] || fails=$((fails+1)); done
done
mkdir -p "$O/home1"; ( cd "$R" && HOME="$O/home1" bash harness/evals/kaizen/feedback-system/save-test.sh >"$O/one.log" 2>&1 ); one=$?
echo "race runs=$total fails=$fails single_rc=$one home_left=$(find "$O/home1" -mindepth 1 | grep -c .) fixed_tmp=$(grep -cE '"/tmp/' "$R/harness/evals/kaizen/feedback-system/save-test.sh")"
```

SC-10 · SC-11 · ER-01 — 새 두 파일 알려진 답:

```bash
#!/usr/bin/env bash
# hs6.sh <풀어 둔 판> — 도우미 떼는 스크립트와 공용 측정 파일을 손으로 답을 아는 입력에 돌린다
R=${1:?root}
EX=${MEASURE_EXTRACT:-$R/harness/scripts/extract-helpers.py}
MC=${MEASURE_COMMON:-$R/harness/scripts/measure-common.sh}
SCH=$R/harness/references/contract-schema.md
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
X=$(mktemp -d "${TMPDIR:-/tmp}/hs6.XXXXXX") || exit 2; X=$(cd "$X" && pwd -P); trap 'rm -rf "$X"' EXIT
F=$X/repo; mkdir -p "$F/.harness"; git -C "$F" init -q -b main || exit 2
fence() { printf '```%s\n' "$1"; }
# 봉인 판: 이름 붙은 bash · python 블록 둘, 이름 없는 bash 블록 하나, text 블록 안의 이름 하나(떼지 않는다)
{ printf -- '---\nstatus: active\n---\n\n## Script\n\n- [ ] SC-01: x\n\n'
  fence bash; printf '#!/usr/bin/env bash\n# a.sh <x> — 첫째\necho a\n'; fence ''
  fence python; printf '# b.py — 둘째\nprint("b")\n'; fence ''
  fence bash; printf '# 이름 없는 설명 블록\necho none\n'; fence ''
  fence text; printf '# z.sh — text 블록은 떼지 않는다\n'; fence ''
} >"$F/.harness/c.md"
# 봉인 값은 스키마 블록을 따로 떼어 계산한다 — 봉인 판은 SEAL_OK, 뒤에 조건을 더한 작업 폴더 판은 SEAL_BROKEN 이 답이다
schema_blk() { awk '/^```bash$/{f=1; buf=""; next} f && /^```$/{ if (buf ~ /(fm_get|sha256_16|sprint_head|mine)\(\) \{/) printf "%s", buf; f=0; next} f { buf = buf $0 "\n" }' "$1"; }
schema_blk "$SCH" >"$X/schema.sh"
D=$(bash -c '. "$1"; contract_digest "$2"' _ "$X/schema.sh" "$F/.harness/c.md") || exit 2
sed -i.bak "s/^status: active$/status: active\nconditions_digest: sha256:$D/" "$F/.harness/c.md" && rm -f "$F/.harness/c.md.bak"
git -C "$F" add -A && git -C "$F" commit -qm seal || exit 2
{ printf '\n'; fence bash; printf '# c.sh — 봉인 뒤에 붙은 블록\necho c\n'; fence ''; } >>"$F/.harness/c.md"
git -C "$F" commit -qam later || exit 2
printf '%s\n' "- [ ] SC-02: y" >>"$F/.harness/c.md"   # 작업 폴더에만 있는 변경 — --sealed 는 보지 않는다
{ fence bash; printf '# d.sh — 하나\n'; fence ''; fence bash; printf '# d.sh — 같은 이름\n'; fence ''; } >"$X/dup.md"
printf '# 도우미 없음\n\n```text\nx\n```\n' >"$X/none.md"; echo untracked >"$F/.harness/new.md"
echo "fixture ok blocks=$(grep -cE '^```(bash|python)$' "$F/.harness/c.md")"
[ -f "$EX" ] || { echo "ABSENT $EX"; }
[ -f "$MC" ] || { echo "ABSENT $MC"; }
[ -f "$EX" ] && [ -f "$MC" ] || exit 2
names() { find "$1" -type f | sed 's#.*/##' | LC_ALL=C sort | tr '\n' ',' | sed 's/,$//'; }
python3 "$EX" --sealed "$F/.harness/c.md" "$X/o1" >"$X/o1.log" 2>&1; echo "E1 sealed rc=$? names=$(names "$X/o1")"
python3 "$EX" "$F/.harness/c.md" "$X/o2" >"$X/o2.log" 2>&1; echo "E2 current rc=$? names=$(names "$X/o2")"
awk '/^```bash$/{f=1;b="";next} f&&/^```$/{ if (b ~ /\n# a\.sh /) { printf "%s", b; exit } f=0; next } f{b=b $0 "\n"}' "$F/.harness/c.md" >"$X/a.want"
cmp -s "$X/a.want" "$X/o1/a.sh"; echo "E3 same_bytes=$([ $? = 0 ] && echo 1 || echo 0)"
python3 "$EX" "$X/dup.md" "$X/o4" >"$X/o4.log" 2>&1; echo "E4 dup rc=$? files=$(find "$X/o4" -type f 2>/dev/null | grep -c .) named=$(grep -c 'd.sh' "$X/o4.log")"
python3 "$EX" "$X/none.md" "$X/o5" >/dev/null 2>&1; echo "E5 none rc=$?"
python3 "$EX" "$X/missing.md" "$X/o6" >/dev/null 2>&1; echo "E6 missing rc=$?"
python3 "$EX" --sealed "$F/.harness/new.md" "$X/o7" >/dev/null 2>&1; echo "E7 untracked-sealed rc=$?"
FNS="fm_get sha256_16 contract_digest verify_seal measurement_digest verify_measurement sprint_head mine unsigned_on unpack_rev scratch_dir sect need_fn"
for sh in bash zsh; do
  out=$(cd "$F" && MC="$MC" X="$X" FNS="$FNS" $sh -c '
    . "$MC" || { echo "source_rc=$?"; exit 0; }
    miss=""; for f in $(printf "%s " "$FNS"); do type "$f" >/dev/null 2>&1 || miss="$miss$f,"; done
    echo "source_rc=0 missing=[${miss%,}] seal_now=$(verify_seal .harness/c.md | cut -d" " -f1)"
    d=$(scratch_dir hs6x) && [ -d "$d" ] && case $d in "${TMPDIR:-/tmp}"/hs6x.*) echo scratch=ok ;; *) echo scratch=bad ;; esac; rm -rf "$d"
    unpack_rev HEAD~1 "$X/u-'$sh'" && [ -f "$X/u-'$sh'/.harness/c.md" ] && echo "unpack=ok seal_sealed=$(verify_seal "$X/u-'$sh'/.harness/c.md" | cut -d" " -f1)"
    unpack_rev no-such-rev "$X/v-'$sh'" 2>/dev/null; echo unpack_bad_rc=$?
    need_fn verify_seal; echo need_ok_rc=$?; need_fn no_such_fn 2>/dev/null; echo need_bad_rc=$?
    printf "# t\n\n## A\na\n\n## B\nb1\n\n\`\`\`bash\n## 펜스 안\n\`\`\`\nb2\n\n### B1\nb3\n\n## C\nc\n" >"$X/s-'$sh'.md"
    echo sect_lines=$(sect "$X/s-'$sh'.md" "## B" | grep -c .)
  ' 2>&1 | tr '\n' ' ')
  echo "M-$sh $out"
done
# bash 에서 정의가 스키마 블록과 글자까지 같은가 (사본이 아니라 스키마에서 읽는다)
same=$(bash -c '. "$1" >/dev/null 2>&1 || exit 2; for f in fm_get sha256_16 contract_digest verify_seal measurement_digest verify_measurement sprint_head mine unsigned_on; do declare -f "$f"; done' _ "$MC" | shasum | cut -c1-12)
want=$(bash -c '. "$1"; for f in fm_get sha256_16 contract_digest verify_seal measurement_digest verify_measurement sprint_head mine unsigned_on; do declare -f "$f"; done' _ "$X/schema.sh" | shasum | cut -c1-12)
echo "M3 same_as_schema=$([ "$same" = "$want" ] && echo 1 || echo 0) copies=$(grep -cE '^[[:space:]]*(fm_get|sha256_16|contract_digest|verify_seal|measurement_digest|verify_measurement|sprint_head|mine|unsigned_on)\(\)' "$MC")"
sed 's/^verify_seal() {/verify_sealx() {/' "$SCH" >"$X/broken-schema.md"
MEASURE_SCHEMA="$X/broken-schema.md" bash -c '. "$1"' _ "$MC" >"$X/m4.out" 2>&1; echo "M4 broken_schema rc=$? names_fn=$(grep -c 'verify_seal' "$X/m4.out")"
MEASURE_SCHEMA="$X/no-such-schema.md" bash -c '. "$1"' _ "$MC" >"$X/m5.out" 2>&1; echo "M5 no_schema rc=$?"
```

DG-02 — 경고 수:

```bash
#!/usr/bin/env bash
# lint.sh <기준 판> <끝 판> <markdownlint-cli2 경로> <설정 파일> — 바꾸거나 새로 만든 파일의 경고 수를 두 판에서 센다. 한 줄에 파일 하나: <도구> <파일> base=<n> end=<n>
RB=${1:?}; RE=${2:?}; ML=${3:?}; CFG=${4:?}
cnt_sh() { [ -f "$1" ] || { echo 0; return; }; shellcheck -s bash -f gcc "$1" | grep -c .; }
cnt_md() { [ -f "$1" ] || { echo 0; return; }; "$ML" --config "$CFG" "$1" 2>&1 | grep -cE '^[^ ]+:[0-9]+(:[0-9]+)? (error|warning) MD[0-9]+'; }
for f in harness/scripts/save-feedback.sh harness/scripts/commit-guard.sh harness/scripts/measure-common.sh \
  harness/evals/kaizen/feedback-system/save-test.sh harness/evals/hooks/commit-guard-test.sh harness/evals/measure/measure-helpers-test.sh; do
  echo "shellcheck $f base=$(cnt_sh "$RB/$f") end=$(cnt_sh "$RE/$f") exists=$([ -f "$RE/$f" ] && echo 1 || echo 0)"
done
for f in harness/skills/sprint-contract/SKILL.md harness/skills/init/SKILL.md harness/evals/gate-exit-codes.md harness/references/contract-schema.md \
  harness/README.md harness/docs/guides/skill-design-guide.md harness/docs/guides/qa-evaluation-guide.md harness/agents/qa-evaluator.md; do
  echo "markdownlint $f base=$(cnt_md "$RB/$f") end=$(cnt_md "$RE/$f")"
done
f=harness/scripts/extract-helpers.py
if [ -f "$RE/$f" ]; then python3 -m py_compile "$RE/$f" 2>/dev/null; echo "py_compile $f rc=$?"; else echo "py_compile $f rc=absent"; fi
python3 -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8"))' "$RE/harness/evals/kaizen/evaluator-kaizen/assertions.json"; echo "json assertions rc=$?"
actionlint "$RE/.github/workflows/ci.yml" >/dev/null 2>&1; echo "actionlint ci.yml rc=$?"
```

AR-01 — 바뀐 경로 범위:

```bash
#!/usr/bin/env bash
# scopediff.sh — 이 가지 커밋 구간(B..END)의 바뀐 경로를 계약의 # sprint-scope 블록과 맞댄다. common.sh 를 읽은 셸에서 부른다
: "${W:?}" "${B:?}" "${END:?}" "${CF:?}" "${T:?}"
blk=$(awk '/^```text$/{f=1; n=0; next} f && /^```$/{f=0; next} f { n++; if (n == 1) { g = ($0 == "# sprint-scope"); next } if (g) print }' "$T/E/$CF")
impl=$(git -C "$W" diff --no-renames --name-only "$B..$END" -- . ':(exclude).harness')
out=$(printf '%s\n' "$impl" | grep . | while IFS= read -r p; do printf '%s\n' "$blk" | grep -qxF -- "$p" || echo "$p"; done)
hr=$(git -C "$W" diff --no-renames --name-only "$B..$END" -- .harness | grep -vxE '\.harness/sprint-(contract|amendments|feedback)-after-0926-harness-scripts\.md')
mixed=0; for c in $(git -C "$W" rev-list "$B..$END"); do
  k=$(git -C "$W" show --no-renames --name-only --format= "$c" | grep . | awk -F/ '{print $1}' | LC_ALL=C sort -u | grep -c .); [ "$k" -le 1 ] || mixed=$((mixed+1)); done
echo "block=$(printf '%s\n' "$blk" | grep -c .) changed=$(printf '%s\n' "$impl" | grep -c .) out_of_block=$(printf '%s\n' "$out" | grep -c .) harness_other=$(printf '%s\n' "$hr" | grep -c .) commits=$(git -C "$W" rev-list --count "$B..$END") mixed_commits=$mixed"
printf '%s\n' "$out" | grep . | sed 's/^/  out /'; printf '%s\n' "$hr" | grep . | sed 's/^/  harness_other /'
```

AR-02 — 기존 검사 열둘:

```bash
#!/usr/bin/env bash
# regress.sh <풀어 둔 판> — 기존 검사 열둘을 그 판에서 돌려 검사마다 종료 코드를 낸다
R=${1:?root}; cd "$R" || exit 2
while IFS='|' read -r name cmd; do
  bash -c "$cmd" >/dev/null 2>&1; echo "$name rc=$?"
done <<'L'
validate-plugin|python3 scripts/validate-plugin.py
sync-docs|python3 scripts/sync-docs.py --check-only
sync-evals|python3 scripts/sync-evals.py --check-only
sync-orchestrator|python3 scripts/sync-orchestrator.py --check-only
run-evals|python3 scripts/run-evals.py --verbose
kaizen-assertions|python3 scripts/run-kaizen-assertions.py
contrast-claims|python3 scripts/check-contrast-claims.py
docs-links|python3 scripts/check-docs-links.py
stale-values|python3 scripts/check-stale-values.py
reviewer-copies|python3 scripts/check-reviewer-protocol-copies.py
collector-test|python3 scripts/test-collect-kaizen-data.py
commit-guard-test|bash harness/evals/hooks/commit-guard-test.sh
L
```

### 봉인 전 실측 (2026-09-26, 가지에 커밋이 없어 `END` = `B` = `6378948`)

기준 판 값은 조건이 떨어져야 할 값이다(음성 · 양성 대조). 「모의본」 은 도우미가 옳고 그름을 가려내는지 보려고 스크래치에 만든 흉내 파일이며 구현이 아니다.

| 측정 | 기준 판 출력 (그대로 옮김) | 조건 |
| ---- | ------------------------- | ---- |
| `hs1.sh "$T/B/…/save-feedback.sh"` | `A rc=0 root=elsewhere hash=other dup=contract_path,contract_path_inferred,contract_root,session_id,sprint_slug sprint_slug=draftslug contract_path=proj/.harness/sprint-contract-demo.md session_id=sess-env renamed=0` | SC-01 · SC-02 |
| 〃 | `B rc=0 root=elsewhere hash=other dup=contract_path,contract_path_inferred,contract_root,sprint_slug sprint_slug=draftslug contract_path=proj/.harness/sprint-contract-demo.md session_id=sess-draft renamed=0` | SC-02 |
| 〃 | `C rc=0 root=elsewhere warn=0` · `D rc=0 root=root2` | SC-01 |
| 〃 | `E collect total=4 parse_failed=0 deterministic=4` (기준 판도 같다 — 반대편이 지금 읽는 모양을 끝 판에서도 읽는지 보는 줄) | SC-02 |
| `save-test.sh` (작업 폴더, 단독) | 종료 코드 0 · `=== ALL TESTS PASSED ===` | SC-03 |
| `race.sh "$T/B" 4 3` | `race runs=12 fails=12 single_rc=0 home_left=3 fixed_tmp=9` (실패 줄: `grep: /tmp/test-feedback-draft-src.yaml: No such file or directory` 등) | SC-04 |
| `hs3.sh "$T/B/…/commit-guard.sh"` | `a1 exit=0` · `a2 exit=0` · `b1 exit=0` · `b2 exit=0` · `k0 exit=2 삭제 60 개` · `k1 exit=0` · `k2 exit=2 되돌리는 파일 1 개` · `k3 exit=0` | SC-05 |
| `scope.sh "$T/B/…/commit-guard.sh"` | 스물세 줄 모두 `exit=0 names=[]` (`s07-env-session exit=0`) | SC-06 · ER-02 |
| `commit-guard-test.sh` (작업 폴더) | 종료 코드 0 · `PASS` 65 줄 · `FAIL` 0 줄 · `실패 0 건` | SC-07 |
| `hs4.sh "$T/B"` | `orig body qa=6 guide=38` · `empty body qa=0 guide=0` · `orig rc=0 PASS:silent-check#1 PASS:silent-check#2 PASS:silent-check#3` · `empty rc=0 PASS:silent-check#1 PASS:silent-check#2 PASS:silent-check#3` | SC-08 |
| `hs5.sh "$T/B"` | `cite=9 rows=4 missing=5 extra=0` — 빠진 다섯 `scripts/check-docs-a11y.js` · `scripts/check-reviewer-protocol-copies.py` · `scripts/collect-kaizen-data.py` · `scripts/finalize-phase.sh` · `scripts/sync-orchestrator.py` | SC-09 |
| 새 행 값의 근거 | `check-docs-a11y.js:154` `process.exit(fails ? 1 : 0)` · `check-reviewer-protocol-copies.py:22-23` 0 · 1 · 2 · `collect-kaizen-data.py:82` `DOC_CONTRACT_EXIT_CODES = (0, 2)` · `finalize-phase.sh:43` `:75` `:96` exit 0 · 1 · 2 · `sync-orchestrator.py:204-243` return 0 · 1 · 2 | SC-09 |
| `hs6.sh "$T/B"` | `fixture ok blocks=4` · `ABSENT …/extract-helpers.py` · `ABSENT …/measure-common.sh` · 종료 코드 2 (새 파일이라 값은 구현 뒤에 잰다 — 준비 단계 · 시험 저장소 만들기는 여기서 돌았다) | SC-10 · SC-11 · ER-01 |
| `hs6.sh` 모의본(스크래치 흉내 두 파일을 `$T/B/harness/scripts/` 에 넣음) | `E1 sealed rc=0 names=a.sh,b.py` · `E2 current rc=0 names=a.sh,b.py,c.sh` · `E3 same_bytes=1` · `E4 dup rc=1 files=0 named=1` · `E5 none rc=3` · `E6 missing rc=2` · `E7 untracked-sealed rc=2` · `M-bash`/`M-zsh … seal_now=SEAL_BROKEN … seal_sealed=SEAL_OK unpack_bad_rc=0 … sect_lines=8` · `M3 same_as_schema=1 copies=0` · `M4 broken_schema rc=2 names_fn=1` · `M5 no_schema rc=2` — 흉내의 `unpack_rev` 결함을 `unpack_bad_rc=0` 으로 잡았다 | SC-10 · SC-11 · ER-01 (도우미가 살아 있다는 확인) |
| `hs6.sh` 음성 모의본 | 아무것도 안 쓰는 떼기 흉내: `E1 sealed rc=0 names=` · `E3 same_bytes=0` / `need_fn` 을 뺀 공용 흉내: `missing=[need_fn]` | SC-10 · SC-11 |
| 이 계약의 떼는 명령 | 도우미 열하나(`common.sh` · `hs1.sh` · `hs3.sh` · `scope.sh` · `hs4.sh` · `hs5.sh` · `race.sh` · `hs6.sh` · `lint.sh` · `scopediff.sh` · `regress.sh`) — 저장 뒤 Step 6.5 전에 떼어 세었다 | SC-10 |
| `lint.sh "$T/B" "$T/E"` | shellcheck `save-feedback.sh` 0 · `commit-guard.sh` 0 · `save-test.sh` 0 · `commit-guard-test.sh` 2 (SC2016 두 줄) / markdownlint sprint-contract `SKILL.md` 9 · init 0 · `gate-exit-codes.md` 0 · `contract-schema.md` 8 · `README.md` 56 · `skill-design-guide.md` 2 · `qa-evaluation-guide.md` 9 · `qa-evaluator.md` 23 · `json assertions rc=0` · `actionlint ci.yml rc=0` | DG-02 |
| `regress.sh "$T/B"` | 열두 줄 모두 `rc=0` | AR-02 |
| `scopediff.sh` (지금 `END` = `B`) | `changed=0 … commits=0 mixed_commits=0` / 모의 실행(무관 계약 · `HEAD~4..HEAD`) `block=15 changed=312 out_of_block=298 harness_other=82 commits=175 mixed_commits=17` | AR-01 |
| SK 조건 글자 수 (`$T/B`) | SK-01 `a=0 b=2 c=0 d=0 · 1` · SK-02 제목 0 · Step 6 `# sprint-scope` 0 · `범위 목록 블록` 0 · SK-03 절 18 줄 · SK-04 `(a) 1 · 0 (b) 0 (c) 1 · 0 (d) 1 · 0` · SC-12 harness 작업 시험 줄 0 · zsh 줄 0 (같은 자르기로 훅 시험 줄 1) · RE-02 떼는 스크립트 0 | SK · SC-12 · RE-02 |
| `validate-plugin.py harness` | `V1 frontmatter       9 skills + 1 agent — OK` · `V6 code-fence        0 bare — OK` · 종료 코드 0 | AP-03 · AP-04 |
| `git push.*--force` 파일 전체 | `harness/docs/guides/skill-design-guide.md:810` 1 줄 (그래서 AP-02 는 더한 줄만 잰다) | AP-02 |

## Skill

- [ ] SK-01: 계약 작성 절차와 초기화 안내가 피드백 초안을 슬러그 이름으로 쓴다 — sprint-contract Step 9 의 초안 경로와 저장 명령이 qa-evaluator 와 같은 `.harness/feedback-draft-<slug>.yaml` 을 쓰고, 고정 이름 `feedback-draft.yaml` 은 plain 모드를 말하는 줄에만 남는다. init 은 `.harness/feedback-draft*.yaml` 를 무시하라고 적는다 [exact, enumerated]
      측정: `S9=$(sect "$T/E/harness/skills/sprint-contract/SKILL.md" "### 9. 피드백 저장")` 뒤 (a) `printf '%s\n' "$S9" | grep -c 'feedback-draft-<slug>\.yaml'` ≥ 2 (b) `printf '%s\n' "$S9" | grep 'feedback-draft\.yaml' | grep -vc 'plain'` = 0
      (c) `printf '%s\n' "$S9" | grep 'save-feedback.sh contract' | grep -c 'feedback-draft-<slug>\.yaml'` ≥ 1 (d) `grep -cF '.harness/feedback-draft*.yaml' "$T/E/harness/skills/init/SKILL.md"` = 1 이고 ``grep -cF '`.harness/feedback-draft.yaml`만' "$T/E/harness/skills/init/SKILL.md"`` = 0
      양성 대조: 기준 판 `$T/B` 는 (a) 0 (b) 2 (c) 0 (d) 0 · 1
- [ ] SK-02: 계약에 범위 목록 블록을 쓰는 절차가 생긴다 — 계약 규약에 제목이 `#### 범위 목록 블록` 으로 시작하는 절이 정확히 하나 생기고 그 절에 아래 아홉 글자가 각각 든다: `## 범위 경계` · `text` · `# sprint-scope` · `owner_session` · `session_id` · `status: active` · `.harness/` · `harness/scripts/commit-guard.sh` · `HARNESS_COMMIT_GUARD=off`. sprint-contract Step 6 절은 `# sprint-scope` 와 `범위 목록 블록` 두 글자를 담아 그 절을 가리킨다 [exact, enumerated]
      측정: `grep -c '^#### 범위 목록 블록' "$T/E/harness/references/contract-schema.md"` = 1 · `SS=$(sect "$T/E/harness/references/contract-schema.md" "#### 범위 목록 블록")` 뒤 글자마다 `printf '%s\n' "$SS" | grep -cF -- '<글자>'` ≥ 1 (아홉 번)
      `S6=$(sect "$T/E/harness/skills/sprint-contract/SKILL.md" "### 6. 계약 저장")` 뒤 `printf '%s\n' "$S6" | grep -cF -- '# sprint-scope'` ≥ 1 · `printf '%s\n' "$S6" | grep -cF '범위 목록 블록'` ≥ 1
      양성 대조: 기준 판은 제목 0 · Step 6 두 글자 0 · 0
- [ ] SK-03: 계약 규약 §검증 수단 인라인 명시에 공용 측정 파일 안내가 줄바꿈 없이 정확히 한 줄 더해지고, 그 줄이 `harness/scripts/extract-helpers.py` 와 `harness/scripts/measure-common.sh` 를 둘 다 적는다. 그 절의 다른 줄은 바뀌지 않는다 [exact]
      측정: `diff <(sect "$T/B/harness/references/contract-schema.md" "#### 검증 수단 인라인 명시") <(sect "$T/E/harness/references/contract-schema.md" "#### 검증 수단 인라인 명시")` 의 `^>` 줄 1 · `^<` 줄 0,
      그 `^>` 줄에 `harness/scripts/extract-helpers.py` 1 · `harness/scripts/measure-common.sh` 1 (`grep -cF`)
      양성 대조: 기준 판끼리 대면 `^>` 0 · `^<` 0 (절 18 줄)
- [ ] SK-04: 훅 설명 네 자리가 범위 검사를 반영한다 — (a) `harness/README.md` 「## 커밋 안전 훅」 절에서 「아직 막지 않는다」 · 「아직 없다」 가 든 줄 0 · `owner_session` 1 이상 (b) `harness/docs/guides/skill-design-guide.md` 의 `| Scope-Bound Edits |` 행에 `sprint-scope` (c)(d) 두 파일 `harness/docs/guides/qa-evaluation-guide.md` · `harness/agents/qa-evaluator.md` 각각에서 「50 개를 넘는 삭제만 막」 0 줄 · `sprint-scope` 1 줄 이상 [exact, enumerated]
      측정: (a) `sect "$T/E/harness/README.md" "## 커밋 안전 훅" | grep -cE '아직 막지 않는다|아직 없다'` = 0 · `… | grep -c owner_session` ≥ 1 (b) `grep -F '| Scope-Bound Edits |' "$T/E/harness/docs/guides/skill-design-guide.md" | grep -c sprint-scope` = 1
      (c)(d) 파일마다 `grep -c '50 개를 넘는 삭제만 막' <파일>` = 0 · `grep -c 'sprint-scope' <파일>` ≥ 1 (`<파일>` 은 `$T/E/` 아래 두 경로)
      양성 대조: 기준 판 (a) 1 · 0 (b) 0 (c) 1 · 0 (d) 1 · 0

## Script

- [ ] SC-01: 피드백 저장이 계약 폴더를 계약 경로에서 잡는다 — Given 셸 위치가 `.harness/` 없는 다른 폴더이고 `HARNESS_CONTRACT` 가 `<proj>/.harness/sprint-contract-demo.md` 일 때, When 저장하면, Then `contract_root` 가 `<proj>` 이고 `project_hash` 가 `<proj>` 경로로 계산된 값이다. `HARNESS_CONTRACT` 가 없는 파일이면 기존 조상 탐색으로 잡고 stderr 에 `HARNESS_CONTRACT` 를 적은 경고를 내며 종료 코드 0, `HARNESS_CONTRACT_ROOT` 를 함께 주면 그것이 이긴다 [exact, enumerated]
      측정: `bash "$K/hs1.sh" "$T/E/harness/scripts/save-feedback.sh"` 출력의 `A` 줄이 `A rc=0 root=proj hash=ok` 로 시작, `C` 줄이 `C rc=0 root=elsewhere warn=1`, `D` 줄이 `D rc=0 root=root2`
      양성 대조: 기준 판 `A rc=0 root=elsewhere hash=other …` · `C rc=0 root=elsewhere warn=0` · `D rc=0 root=root2` (D 는 지켜야 할 동작)
- [ ] SC-02: 초안에 식별 칸 다섯(`sprint_slug` · `contract_path` · `session_id` · `contract_root` · `contract_path_inferred`)이 있어도 저장본 맨 위에 칸마다 한 번만 들고, 초안 값은 `draft_<칸>` 다섯으로 남는다. 최종 값의 우선순위는 지금과 같다 — `sprint_slug` 는 초안 값, `contract_path` 는 `HARNESS_CONTRACT`, `session_id` 는 환경 값이 있으면 그것 없으면 초안 값 [exact, enumerated]
      측정: 같은 `hs1.sh` 출력에서 `A` 줄이 `dup=none sprint_slug=draftslug contract_path=proj/.harness/sprint-contract-demo.md session_id=sess-env renamed=5` 를,
      `B` 줄이 `dup=none sprint_slug=draftslug contract_path=proj/.harness/sprint-contract-demo.md session_id=sess-draft renamed=5` 를 담는다 (`dup` 은 YAML 을 읽으며 맨 위 매핑에서 겹친 키)
      반대편: 같은 출력의 `E` 줄이 `E collect total=4 parse_failed=0 deterministic=4` — `scripts/collect-kaizen-data.py` 가 `draft_*` 칸이 든 저장본 넷을 읽는다
      양성 대조: 기준 판 `A … dup=contract_path,contract_path_inferred,contract_root,session_id,sprint_slug … renamed=0` · `B … dup=contract_path,contract_path_inferred,contract_root,sprint_slug … session_id=sess-draft renamed=0`
- [ ] SC-03: 피드백 저장 시험이 SC-01 · SC-02 모양을 직접 돌려 확인하고 끝 판에서 통과한다 [goal]
      측정: `cd "$T/E" && bash harness/evals/kaizen/feedback-system/save-test.sh` 종료 코드 0 · 마지막 줄 `=== ALL TESTS PASSED ===` ·
      `PASS:` 로 시작하는 줄 가운데 `contract_root` 가 든 줄 ≥ 1 · `draft_` 가 든 줄 ≥ 1 · `HARNESS_CONTRACT` 가 든 줄 ≥ 1
      음성 대조: `cp -R "$T/E" "$T/E2"` 뒤 `cp "$T/B/harness/scripts/save-feedback.sh" "$T/E2/harness/scripts/save-feedback.sh"` 로 저장 스크립트만 기준 판으로 되돌리고 같은 시험을 돌리면 종료 코드 ≠ 0 · `FAIL:` 줄 ≥ 1
- [ ] SC-04: 피드백 저장 시험을 동시에 돌려도 서로 지우지 않는다 — 고정 `/tmp/` 경로가 없고, 한 임시 폴더 아래에서만 쓰고, 부른 사람의 HOME 에 아무것도 남기지 않는다 [exact]
      측정: `bash "$K/race.sh" "$T/E" 4 3` 출력이 `race runs=12 fails=0 single_rc=0 home_left=0 fixed_tmp=0`
      양성 대조: 기준 판 `race runs=12 fails=12 single_rc=0 home_left=3 fixed_tmp=9`
- [ ] SC-05: 커밋 안전 훅이 놓치던 두 모양을 막고 지켜야 할 모양은 그대로 둔다 — 막음(exit 2, 막힘 설명에 `삭제 60 개`): `a1` `git add d1 && git commit` · `a2` `git add d1/ && git commit` · `b1` 하위 폴더에서 `git commit -am` · `b2` 하위 폴더에서 `git add -A && git commit`. 그대로: `k0` 최상위 `git commit -am` exit 2 · `k1` 하위 폴더 `git add . && git commit` exit 0 · `k2` 되돌림이 남은 목록 + `git add a.txt && git commit` exit 2(`되돌리는 파일 1 개`) · `k3` 삭제가 실리지 않는 `git add a.txt && git commit` exit 0 [exact, enumerated]
      측정: `bash "$K/hs3.sh" "$T/E/harness/scripts/commit-guard.sh"` 여덟 줄이 차례로 `a1 exit=2 삭제 60 개` · `a2 exit=2 삭제 60 개` · `b1 exit=2 삭제 60 개` · `b2 exit=2 삭제 60 개` ·
      `k0 exit=2 삭제 60 개` · `k1 exit=0` · `k2 exit=2 되돌리는 파일 1 개` · `k3 exit=0` (줄 끝 공백 무시)
      양성 대조: 기준 판은 `a1` · `a2` · `b1` · `b2` 가 `exit=0` 이고 나머지 넷은 위와 같다
- [ ] SC-06: 커밋 안전 훅이 계약의 범위 목록 밖 경로를 막는다 — Given 커밋 폴더 위 첫 `.harness/` 에 `status: active` · `owner_session: S` 계약이 있고 그 「## 범위 경계」 안 `# sprint-scope` 블록이 `d1/f001` · `docs/*.md` · `sub/` 일 때, When 세션 S 가 커밋하면, Then 블록과 `.harness/` 밖 경로를 싣는 커밋은 exit 2 로 막히고 막힘 설명에 그 경로가 나오며 블록 안 경로는 나오지 않는다. 블록 안 · `.harness/` · 끄기 · 합집합은 exit 0 [exact, enumerated]
      측정: `bash "$K/scope.sh" "$T/E/harness/scripts/commit-guard.sh"` 에서 막음 여덟이 `exit=2`: `s01-out`(`names=[a.txt]`) · `s07-env-session` · `s08-path-commit` · `s09-add-commit` · `s10-commit-a` ·
      `s13-rename-out`(`names` 에 `moved.txt` 있고 `d1/f001` 없음) · `s16-mixed`(`names=[a.txt]`) · `s19-subdir-a-out`.
      통과 여덟이 `exit=0`: `s02-in` · `s03-harness` · `s04-glob` · `s05-dir` · `s11-off` · `s12-union` · `s15-delete-in` · `s17-subdir-a`
      양성 대조: 기준 판 훅은 스물한 경우 모두 `exit=0` — 막음 여덟이 떨어진다
- [ ] SC-07: 훅 시험이 SC-05 여덟 경우와 SC-06 · ER-02 스물세 경우를 담고 끝 판에서 통과한다 [goal]
      측정: `cd "$T/E" && bash harness/evals/hooks/commit-guard-test.sh` 종료 코드 0 · `^PASS ` 줄 ≥ 95 (기준 65 + 새 경우 서른하나 중 기존 ② 와 같은 `k0` 를 뺀 30) · `^FAIL ` 줄 0
      음성 대조: `COMMIT_GUARD_HOOK="$T/B/harness/scripts/commit-guard.sh" bash "$T/E/harness/evals/hooks/commit-guard-test.sh"` 가 종료 코드 ≠ 0 · `^FAIL ` 줄 ≥ 12 (기준 판 훅이 떨어뜨리는 SC-05 넷 + SC-06 막음 여덟)
- [ ] SC-08: 평가자 카이젠 `silent-check` #2 · #3 이 절 본문을 본다 — 제목만 남기고 본문을 비운 사본에서 둘 다 FAIL 하고 러너 종료 코드가 1, 원본에서는 셋 다 PASS 하고 종료 코드 0. #1 과 다른 네 키의 값은 바뀌지 않는다 [exact, enumerated]
      측정: `bash "$K/hs4.sh" "$T/E"` 넷째 줄 `orig rc=0 PASS:silent-check#1 PASS:silent-check#2 PASS:silent-check#3` · 다섯째 줄 `empty rc=1 PASS:silent-check#1 FAIL:silent-check#2 FAIL:silent-check#3`
      (첫 두 줄 `orig body qa=6 guide=38` · `empty body qa=0 guide=0` 이 변이가 들어갔다는 확인). `python3 -c 'import json,sys; a,b=(json.load(open(p,encoding="utf-8")) for p in sys.argv[1:]); print(len(b["silent-check"]), a["silent-check"][0]==b["silent-check"][0], all(a[k]==b[k] for k in a if k!="silent-check"))' "$T/B/harness/evals/kaizen/evaluator-kaizen/assertions.json" "$T/E/harness/evals/kaizen/evaluator-kaizen/assertions.json"` 가 `3 True True`
      양성 대조: 기준 판 다섯째 줄 `empty rc=0 PASS:silent-check#1 PASS:silent-check#2 PASS:silent-check#3`
- [ ] SC-09: 종료 코드 정의 파일의 「## 소비처」 표가 그 파일을 인용하는 스크립트(`scripts/` · `harness/scripts/` · `harness/evals/` 아래 `.py` · `.sh` · `.js`) 전부를 한 행씩 담고, 새 행 여섯의 값이 실제 종료 코드와 같다 — `scripts/check-reviewer-protocol-copies.py` `0 · 1 · 2` · `scripts/check-docs-a11y.js` `0 · 1` · `scripts/collect-kaizen-data.py` `0 · 2` · `scripts/finalize-phase.sh` `0 · 1 · 2` · `scripts/sync-orchestrator.py` `0 · 1 · 2` · `harness/scripts/extract-helpers.py` `0 · 1 · 2 · 3` [exact, enumerated]
      측정: `bash "$K/hs5.sh" "$T/E"` 첫 줄이 `missing=0 extra=0` 을 담는다. 여섯 행마다 ``grep -cF '| `<경로>` | <값> |' "$T/E/harness/evals/gate-exit-codes.md"`` = 1
      (예: ``grep -cF '| `scripts/check-reviewer-protocol-copies.py` | 0 · 1 · 2 |'``)
      양성 대조: 기준 판 `cite=9 rows=4 missing=5 extra=0`
- [ ] SC-10: 도우미 떼는 스크립트 `harness/scripts/extract-helpers.py` 가 이름 붙은 bash · python 블록만 떼고, `--sealed` 면 그 계약을 처음 담은 커밋의 판을 읽는다. 떼어 낸 파일은 블록 본문과 바이트까지 같다 [exact, enumerated]
      측정: `bash "$K/hs6.sh" "$T/E"` 의 `E1 sealed rc=0 names=a.sh,b.py` · `E2 current rc=0 names=a.sh,b.py,c.sh` · `E3 same_bytes=1`.
      이 계약 자체: `SEALC=$(git -C "$W" log --diff-filter=A --format=%H -- "$CF" | tail -1)` · `git -C "$W" show "$SEALC:$CF" >"$T/sealed.md"` 에 위 「떼는 명령」 을 돌린 폴더(`$T/k1`)와
      `python3 "$T/E/harness/scripts/extract-helpers.py" --sealed "$W/$CF" "$T/k2"`(종료 코드 0)의 파일 이름 집합이 같고(도우미 열하나 `common.sh` · `hs1.sh` · `hs3.sh` · `scope.sh` · `hs4.sh` · `hs5.sh` · `race.sh` · `hs6.sh` · `lint.sh` · `scopediff.sh` · `regress.sh`) 파일마다 `cmp` 가 같다
      알려진 답: 손으로 만든 시험 계약 — 봉인 판에 이름 붙은 블록 둘(`a.sh` 셔뱅 뒤 · `b.py`), 이름 없는 bash 블록 하나, `text` 블록 안 이름 하나, 봉인 뒤 커밋에 `c.sh`. 기대 E1 둘 · E2 셋. 봉인 전 모의본에서 기대대로 나왔고, 아무것도 쓰지 않는 모의본에서는 `names=` 빈 값 · `same_bytes=0` 이 나왔다
- [ ] SC-11: 공용 측정 파일 `harness/scripts/measure-common.sh` 를 bash · zsh 에서 `.` 로 읽으면 계약 규약의 함수 아홉(`fm_get` · `sha256_16` · `contract_digest` · `verify_seal` · `measurement_digest` · `verify_measurement` · `sprint_head` · `mine` · `unsigned_on`)과 자체 도우미 넷(`unpack_rev` · `scratch_dir` · `sect` · `need_fn`)이 정의되고, 규약 함수는 사본이 아니라 규약 블록에서 읽어 정의가 글자까지 같다 [exact, enumerated]
      측정: `bash "$K/hs6.sh" "$T/E"` 의 `M-bash` · `M-zsh` 줄이 각각 `source_rc=0 missing=[] seal_now=SEAL_BROKEN scratch=ok unpack=ok seal_sealed=SEAL_OK unpack_bad_rc=2 need_ok_rc=0 need_bad_rc=2 sect_lines=8` 이고 `M3 same_as_schema=1 copies=0`
      알려진 답: 시험 저장소의 봉인 판 계약은 `SEAL_OK`, 봉인 뒤 조건 한 줄을 더한 작업 폴더 판은 `SEAL_BROKEN`. `sect` 는 손으로 센 여덟 줄(펜스 안 `## 펜스 안` 에서 멈추지 않음).
      봉인 전 모의본에서 없는 판을 푼 `unpack_rev` 가 0 을 내자 도우미가 `unpack_bad_rc=0` 으로 드러냈고, `need_fn` 을 뺀 모의본에서 `missing=[need_fn]` 이 나왔다
- [ ] SC-12: 새 시험 `harness/evals/measure/measure-helpers-test.sh` 가 SC-10 · SC-11 · ER-01 모양을 돌려 끝 판에서 통과하고, 대상 두 파일을 환경 변수 `MEASURE_EXTRACT` · `MEASURE_COMMON` 으로 바꿀 수 있으며, CI harness 작업이 zsh 를 갖춘 뒤 그 시험을 부른다 [goal]
      측정: (a) `cd "$T/E" && bash harness/evals/measure/measure-helpers-test.sh` 종료 코드 0 (b) `awk '/^  harness:/{f=1;next} f&&/^  [a-z-]+:$/{f=0} f' "$T/E/.github/workflows/ci.yml"` 출력에 `run: bash harness/evals/measure/measure-helpers-test.sh` 1 줄 · `command -v zsh` 1 줄 이상, 그리고 zsh 줄이 시험 줄보다 앞
      (c) `actionlint "$T/E/.github/workflows/ci.yml"` 종료 코드 0
      음성 대조: 시험은 `MEASURE_EXTRACT` · `MEASURE_COMMON` 으로 대상 파일을 바꿀 수 있다. 아무것도 안 쓰는 흉내 스크립트(`import sys; sys.exit(0)`)를 `MEASURE_EXTRACT` 에, `need_fn` 정의를 지운 사본을 `MEASURE_COMMON` 에 따로 넣고 돌리면 각각 종료 코드 ≠ 0
      양성 대조: 기준 판 harness 작업은 시험 줄 0 · zsh 줄 0 (같은 awk 로 훅 시험 줄은 1 이 나와 자르기가 산다)

## Error

- [ ] ER-01: 새 두 파일이 실패를 삼키지 않는다 — 떼는 스크립트는 같은 이름 블록이 둘이면 종료 코드 1 · 파일 0 개 · 출력에 그 이름, 뗄 블록이 없으면 3, 파일이 없거나 `--sealed` 인데 git 이 추적하지 않는 파일이면 2 (값 뜻은 `harness/evals/gate-exit-codes.md`). 공용 측정 파일은 규약에서 함수 하나를 못 찾거나 규약 파일이 없으면 `.` 가 2 를 돌려주고 stderr 에 그 이름을 적는다 [exact, enumerated]
      측정: `bash "$K/hs6.sh" "$T/E"` 의 `E4 dup rc=1 files=0 named=1` · `E5 none rc=3` · `E6 missing rc=2` · `E7 untracked-sealed rc=2` · `M4 broken_schema rc=2 names_fn=1` · `M5 no_schema rc=2`
      알려진 답: 봉인 전 모의본에서 여섯 줄이 모두 이 값으로 나왔다
- [ ] ER-02: 범위 검사는 판단이 안 서면 조용히 통과한다 — `s06-other-session`(다른 세션) · `s14-no-block`(블록 없는 계약) · `s18-no-session`(입력에도 환경에도 세션 없음) · `s20-unreadable`(계약을 못 읽음) · `s21-block-outside`(블록이 「범위 경계」 밖) · `s22-empty-block`(블록 펜스는 있고 경로 0 줄 — 블록 없음과 같이 본다) · `s23-no-owner`(`owner_session` 칸이 없는 계약) 일곱이 exit 0 [exact, enumerated]
      측정: `bash "$K/scope.sh" "$T/E/harness/scripts/commit-guard.sh"` 의 일곱 줄이 `exit=0`. stdout 이 비었는지는 SC-07 의 시험이 `expect … 0 empty` 로 잰다

## Architecture

- [ ] AR-01: Given 이 스프린트 커밋이 끝난 뒤 가지 `chore/ak2-hs` 끝(`END`)까지, 구간 `B..END` 의 바뀐 경로가 (a) `.harness/` 밖은 전부 이 계약 `# sprint-scope` 블록 열일곱 줄 안(포함 · 열일곱은 끝 판 계약에서 다시 센 값이며, 블록을 바꾸는 개정은 허용 파일을 바꾸는 일이라 위임으로 동의 처리하지 않는다) (b) `.harness/` 안은 이 계약 · `.harness/sprint-amendments-after-0926-harness-scripts.md` · `.harness/sprint-feedback-after-0926-harness-scripts.md` 셋 안 (c) 커밋마다 최상위 폴더 하나만 건드린다 (d) 끝 판 계약이 봉인 두 줄 모두 OK [exact, enumerated]
      측정: `bash "$K/scopediff.sh"` 가 `block=17 … out_of_block=0 harness_other=0 … mixed_commits=0` (상한은 `refs/heads/chore/ak2-hs` 해석값, `HEAD` 금지 · `--no-renames` · 이 레포에 생성물 없음)
      (d) `. "$T/E/harness/scripts/measure-common.sh"` 뒤 `verify_seal "$T/E/$CF"` 가 `SEAL_OK` · `verify_measurement "$T/E/$CF"` 가 `MEASURE_OK`
      양성 대조: 무관한 계약(`sprint-contract-after-0924-rust-app-name.md`)과 구간(`HEAD~4..HEAD`)을 넣은 모의 실행이 `out_of_block=298 harness_other=82 mixed_commits=17` 을 냈다
- [ ] AR-02: 기존 검사 열둘이 끝 판에서 모두 종료 코드 0 이다 — `validate-plugin` · `sync-docs` · `sync-evals` · `sync-orchestrator` · `run-evals` · `kaizen-assertions` · `contrast-claims` · `docs-links` · `stale-values` · `reviewer-copies` · `collector-test`(피드백 칸을 읽는 반대편) · `commit-guard-test` [exact, enumerated]
      측정: `bash "$K/regress.sh" "$T/E"` 열두 줄 모두 `rc=0`
      기준: 기준 판도 열둘 모두 `rc=0` (봉인 전 실측)

## Anti-patterns

- [ ] AP-02: force push 금지 — 구간 `B..END` 에서 더한 줄에 `git push.*--force` 가 없다
      측정: `git -C "$W" diff -U0 "$B..$END" | grep '^+' | grep -v '^+++' | grep -cE 'git push.*--force'` = 0
      양성 대조: 기준 판 `harness/docs/guides/skill-design-guide.md:802` 에 이미 한 줄이 있어 파일 전체로 재면 1 — 그래서 더한 줄만 잰다
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
      측정: `cd "$T/E" && python3 scripts/validate-plugin.py harness --check=code-fence` 종료 코드 0 · `V6 code-fence        0 bare — OK` 줄
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
      측정: `cd "$T/E" && python3 scripts/validate-plugin.py harness` 의 `V1 frontmatter` 줄이 `— OK` 로 끝난다 (기준 판 `V1 frontmatter       9 skills + 1 agent — OK`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
      측정: 공용 측정 파일의 자체 도우미 넷이 `.` 로 읽은 셸에서 바로 불린다(SC-11 `missing=[]`) · 떼는 스크립트가 경로 인자만으로 돈다(SC-10 이 계약 자체에 돌린 결과)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
      측정: 규약 함수 아홉은 새로 쓰지 않고 규약 블록을 읽는다(SC-11 `M3 same_as_schema=1 copies=0`). 기준 판 `scripts/` · `harness/scripts/` 에 도우미 블록을 떼는 스크립트 0 개(`grep -rlE '도우미 블록|helper block' "$T/B/scripts" "$T/B/harness/scripts" | grep -c .` = 0)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git -C "$W" diff --name-only "$B..$END" | grep -c '^scripts/release.sh$'` 이 0. 대신 셸 문법은 DG-02 의 shellcheck 가 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude `[]` — 제외 없음. 새 파일은 0 개, 바꾼 기존 파일은 이번 변경이 더한 경고 0 개 = 파일마다 끝 판 ≤ 기준 판)
      측정: `bash "$K/lint.sh" "$T/B" "$T/E" "$ML" "$MLCFG"` 의 `shellcheck` · `markdownlint` 줄마다 `end` ≤ `base` 이고 새 파일(`measure-common.sh` · `measure-helpers-test.sh`) `end=0`,
      `py_compile harness/scripts/extract-helpers.py rc=0` · `json assertions rc=0` · `actionlint ci.yml rc=0`
      기준(봉인 전 실측): shellcheck `save-feedback.sh` 0 · `commit-guard.sh` 0 · `save-test.sh` 0 · `commit-guard-test.sh` 2 / markdownlint sprint-contract `SKILL.md` 9 · init `SKILL.md` 0 · `gate-exit-codes.md` 0 · `contract-schema.md` 8 · `README.md` 56 · `skill-design-guide.md` 2 · `qa-evaluation-guide.md` 9 · `qa-evaluator.md` 23
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 도 scripts/release.sh 만 잰다 — 교집합 0 개, DG-01 과 같은 측정. 시험 셋은 SC-03 · SC-07 · SC-12 가 음성 대조와 함께 잰다)
- [ ] DG-04: N/A (산출물에 구동할 앱 · 서버가 없다 — 바꾼 파일은 셸 · 파이썬 스크립트 · 문서 · CI 설정이다. 훅은 SC-05 · SC-06 이 실제 훅 입력으로 돌린다. 측정: `git -C "$W" diff --name-only "$B..$END" | grep -cE '(^|/)(main\.(dart|ts|js|py)|server\.[a-z]+)$'` 이 0)
