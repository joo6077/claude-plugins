---
feature: "카이젠 2026-09-24 Phase 4 계약 — 경로 지정 커밋의 삭제 세기 · 피드백 초안 필수 필드 · /sprint 내 경로만 커밋 · 워크트리 · 원인 가르기 · V10 범위 · 수집기 폴더 이름 한 곳 · 범위 선언 자리"
slug: kaizen-0924-p04-harness
created: "2026-09-25 03:20"
complexity: "복잡"
conditions: 28
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:afb7f33963bceeda
locked_at: "2026-09-25 04:17"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase4.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서
`배정` 칸이 `Phase 4` 인 행은 열이다. 러닝북 Phase 4 추가 과제가 셋이고, 앞 Phase 가 넘긴 것(`phase1-notes.md` · `phase2-notes.md` ·
`phase3-notes.md` 의 Phase 4 줄)과 카이젠 스킬 Step 2a 에서 하나를 더 찾았다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `harness:P02` · `F14` | 피드백 저장 첫 검사가 스크립트가 다시 계산할 `project_hash` · `project_name` 을 초안에 요구해 저장이 거부된다 | 반영 — ER-02 |
| `harness:P07` · `F08` | `/sprint` 에 내 경로만 커밋 · 워크트리 권고 · 기준 커밋 비교 | 반영 — SK-01 · SK-02 · SK-03 |
| `user-setup:P2` | `/sprint` 에 워크트리 권고 · 폐기 결정 줄 · 커밋 전 삭제 보고 | 워크트리 · 삭제 보고는 반영(SK-01 · SK-02). 폐기 결정 줄은 미반영 — 기록 자리를 하나로 정하는 일이 `F20`(Phase 11) 몫이다 |
| `F09` | 기준 커밋 가르기 규칙이 harness:P07 · backend-family:P3 · backend-family:P4 세 곳 — 하나로 정한다 | `/sprint` Step 3 에 한 규칙으로 — SK-03. Phase 8 · 9 가 맞출 문장은 notes 로 넘긴다(ER-05) |
| `F28` | 워크트리 준비 · 상태 스크립트 · 커밋 전 검사 | 워크트리 준비는 SK-02, 커밋 전 검사는 ER-01 · AR-03. 상태 스크립트는 미반영 — 근거 파일 §2 F28 이 외부 권고를 찾지 못했다. 시뮬레이터 · 데이터베이스 나누기도 미반영 — 맡은 제안이 없고(처리 배정표 비고) 근거 파일 §2 F28 도 다루지 않는다 |
| `F18` · `other-kits:P10` | 절을 끼워 넣어 표가 갈라짐 · YAML 블록 깨짐 — V10 범위에 `skills/*/references` | V10 범위 반영 — AR-01. YAML 검사는 더하지 않는다(`GAP 분석` 셋째 선택) |
| `insights:scope-commit-block` | 선언 범위 밖 파일 커밋 차단 — 범위 선언을 기계가 읽을 자리부터 | 자리를 정해 킷 문서에 적는다 — AR-03. 쓰는 절차 · 읽는 훅은 다음 사이클(ER-05) |
| 러닝북 과제 (1) | `commit-guard.sh` 가 경로 지정 커밋에서 검사를 통째로 건너뛰어 그 경로 안 대량 삭제가 실린다 | 반영 — ER-01 · AR-04 |
| 러닝북 과제 (2) | 수집기가 facets · session-meta 폴더 이름을 `USAGE_DATA_INPUTS` 와 따로 적어 문서 대조가 어긋남을 못 잡는다 | 반영 — AR-02 |
| Phase 1 넘김 | `/sprint` Step 3 `[미검증]` + 사유 한 줄 · create-agent 「15 종」 「2건 이상 자동 REJECT」 · create-skill 「1500-2000 words」 | 반영 — SK-04 · SK-05 |
| Phase 2 넘김 | `/sprint` 끝 줄 「사용자가 할 일」 · contract-kaizen Step 2 의 true 뜻 섞임 · `feedback-schema.yaml` · sprint-contract Step 9 | 앞 둘은 반영(SK-04 · SK-06). 뒤 둘은 harness-kaizen 이 고치지 못하는 파일이라 다음 사이클로 넘긴다(ER-05) |
| Phase 3 넘김 | `assertions.json 실행기` 를 `scripts/` 에 둘지 | 이번에 만들지 않는다 — 처리 배정표 밖이고 크기에 비해 조건이 는다(ER-05) |
| `reflect-collector:P5` · Phase 1 ~ 3 notes | `harness:P02` 비고가 「같은 파일의 프로젝트 이름 계산을 바꾸므로 함께 시험한다」 고 적었다. `save-feedback.sh` 가 저장본의 `project_name` 을 워크트리 폴더 이름으로 적는다 — Phase 1 · 2 · 3 notes 가 셋 다 `kaizen-0924` 로 적힌 것을 봤다 | 미반영 — 본 레포 이름을 구하는 규칙과 그 출처는 `phase12.md` 에만 있고 이 Phase 근거 파일 `phase4.md` 에는 없다. Phase 12 범위는 `reflect-kit/` 라 이 파일을 고치지 못한다. 다음 사이클 Phase 4 로 넘긴다(ER-05). ER-02 는 필수 필드 목록만 바꾸고 이름 계산 줄은 건드리지 않아 함께 시험할 것이 없다 |

고칠 것은 여덟 갈래다.

1. **경로 지정 커밋 (러닝북 과제 (1) · F08 · F28).** `harness/scripts/commit-guard.sh:166` 이 `-o` · `-- <경로>` 커밋이면 바로
   돌아간다. 경로 커밋은 공용 목록이 아니라 HEAD 위에 그 경로의 작업 폴더 상태를 얹으므로, 그 경로 안에서 작업 폴더에 없는 추적 파일은
   전부 삭제로 실린다. 임시 저장소 실측(git 2.53.0): `git commit -o d1` 이 작업 폴더에서만 지운 60 개를 삭제로 기록했고 훅은 통과시켰다.
   `-i <경로>` 도 목록 삭제 10 개만 세고 같은 경로의 작업 폴더 삭제 45 개를 빼서 55 개가 실렸다.
2. **피드백 초안 필수 필드 (harness:P02 · F14).** `save-feedback.sh:53` · `:75` 가 초안 검사와 최종본 검사에 같은 여덟 필드를 요구한다.
   `project_hash` · `project_name` 은 `:206-209` 에서 다시 계산해 덮어쓰는 값이라 초안에 요구하면 버릴 값 때문에 저장이 거부된다
   (데이터 풀 §0-b `bcf7a121` 2026-09-19: 「missing project_hash/project_name」 으로 여러 번 거부).
3. **`/sprint` 커밋 (harness:P07 · F08 · user-setup:P2).** Step 5 가 「conventional commit → commit」 만 적는다. 공용 작업 폴더에서
   `git add -A` · `git commit -a` 로 남의 변경과 삭제를 싣는 것을 막는 말이 없다 (§0-b `9a0d4163` 3217 개 삭제 · `d93c7e7a` 남의 커밋 두 개 되돌림).
4. **워크트리와 원인 가르기 (F09 · F28).** Step 0 은 겹침을 보고만 하고, Step 3 은 빨간 검사를 누구 탓인지 가르지 않는다
   (§0-b `e863512e`: 다른 세션들이 깬 공용 개발 가지에서 몇 시간 · 사용자가 워크트리를 먼저 제안). 가르는 규칙은 세 곳에 제안이 있어
   `/sprint` Step 3 을 한 규칙으로 두고 Phase 8 · 9 에 맞출 문장을 넘긴다.
5. **V10 범위 (other-kits:P10 · F18).** V10 은 킷 최상위 `references/*.md` 만 보고 스킬 폴더 안 `references/` 문서 41 개를 빼먹는다.
6. **수집기 폴더 이름 (러닝북 과제 (2)).** `scripts/collect-kaizen-data.py:73-76` 의 `USAGE_DATA_INPUTS` 는 문서 대조에만 쓰이고
   실제로 읽는 `:448-449` 는 이름을 따로 적었다. 읽는 자리의 이름을 바꿔도 `validate-doc-contracts.py` 가 통과한다 (봉인 전 실측).
7. **범위 선언 자리 (insights:scope-commit-block).** 커밋 훅이 「이 스프린트가 선언한 경로」 를 읽을 자리가 킷에 없다.
8. **앞 Phase 넘김 (Phase 1 · 2).** `/sprint` Step 3 의 `[미검증]` 표기와 끝 줄, create-agent · create-skill 의 낡은 사실,
   contract-kaizen Step 2 가 옛 문구로 적힌 체크리스트 true 를 반복 실패로 세는 것.

카이젠 스킬 Step 2a 실측(2026-09-25, 글로벌 계약 피드백 최근 10 건 · 파일 이름 시각 순 2026-09-24T135112 ~ 2026-09-25T000307):
임계(10 건 중 3 회)를 넘은 항목은 `nfr_coverage` 6 건 하나뿐인데, 6 건 모두 새 키 `measure_premise_unrun` 이 없는 옛 문구 파일이다. 키가 있는
2 건은 둘 다 false 였다. 설치본 `harness/0.13.0` 의 sprint-contract 도 옛 문구다(`nfr_coverage`: 「반영되었는가?」, 새 키 0 건). 평가 피드백 최근 10 건은
임계를 넘은 항목 0, `repeat_count` 2 이상 0, `regression_link` 0 (APPROVE 9 · REJECT 1). 그래서 8 번을 넣는다.

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase4.md` 에서 가져왔다.

- [git commit](https://git-scm.com/docs/git-commit) — `--only` 는 지정한 경로의 작업 폴더 내용을 커밋하고 다른 경로의 올려 둔 내용은 싣지 않는다 (SK-01 · ER-01)
- [git worktree](https://git-scm.com/docs/git-worktree) — 워크트리마다 `HEAD` 와 목록 같은 파일을 따로 둔다 (SK-02)
- [git merge-base](https://git-scm.com/docs/git-merge-base) — 두 커밋의 공통 조상. 분기점이지 기준 가지의 지금 상태가 아니다 (SK-03)
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) — `isolation: worktree` 는 부모 `HEAD` 가 아니라 기본 가지에서 만든다 (SK-02)
- [Claude Code Skills](https://code.claude.com/docs/en/skills) — `argument-hint` 는 자동 완성 힌트, 스킬 선택은 description 이 맡는다 (SK-05)
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks) — `PreToolUse` 는 exit 2 로 막고 `PostToolUse` 는 되돌리지 못한다 (ER-01 이 pre 에서 막는 근거 — 새로 인용하지는 않는다)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: 피드백 초안과 최종본을 가르는 외부 표준은 없다 — 근거는 스크립트의 생성 순서다(§2 P02).
`-o` 는 소유권을 판정하지 않는다 — 적은 경로 안에 남의 변경이 있으면 같이 실린다(§2 P07). 그래서 SK-01 에 `git diff HEAD -- <내 경로…>` 줄을 둔다.
`merge-base` 하나로 모든 뜻을 대지 않는다 — 분기점과 기준 가지의 지금 상태는 다른 질문이다(§2 P07 · §5). SK-03 은 둘을 따로 돌린다.
YAML 펜스를 일괄 파싱하면 자리표시자 예시 때문에 오탐이 난다(§2 F18) — 이번 실측도 같다(`GAP 분석` 셋째 선택).
범위 선언을 frontmatter 에 둘지 따로 둘지는 열린 선택이다(§5) — `GAP 분석` 넷째 선택이 고른다. 워크트리 상태 스크립트의 외부 권고는 없다(§2 F28).

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b (`9a0d4163` · `e863512e` · `bcf7a121` · `d93c7e7a` · `f5b7f3a5`) · §0.5 [harness] 세 건(변경 범위
조건이 깨진 이유 — 참고만, `미분류` 는 근거로 쓰지 않는다) · §1 · §5. 앞 Phase notes 셋. 글로벌 피드백 최근 10 건씩(위 배경).

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 4 — 커밋 훅 · 피드백 저장 스크립트 · 스킬 문서 다섯 · 검사기 둘(V10 · 수집기) |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 훅이 막는 경우가 는다, 피드백 초안 필수 필드가 준다, 검증 범위가 넓어진다 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 모든 프로젝트의 `git commit` 에 걸리는 훅, 모든 계약 · 평가가 쓰는 피드백 저장, 14 킷 전부의 V10 |

레이어가 넷이고 나머지 세 축이 전부 「예」이며 공개 형태 변경과 소비면이 둘 다 「예」라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다
(ER-01 · ER-02 · AR-01 · AR-04 · SK-04 (c)). 기능 조건은 18 개다 — 복잡 9~20 안이다 (SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 18).

카이젠 스킬 Gotcha 「새로 도입하는 개선 unit 3 개 이하」: 1 · 2 · 3 · 4 · 5 · 6 · 7 은 처리 배정표와 러닝북이 이 Phase 에 준 것이라
(b) 명시 backlog 로 세지 않는다. 8 가운데 create-agent · create-skill · `/sprint` 끝 줄 · `[미검증]` 네 칸은 설계 가이드 · sprint-contract 와 어긋난
사실의 정정이라 (a) 로 세지 않는다. 새로 세는 unit 은 contract-kaizen · harness-kaizen 의 세는 규칙 하나다. 모든 unit 은 조건마다 실행 증거를 남긴다.

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `3a51b73` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `harness/scripts/commit-guard.sh` | `:124-158` (인자 가르기 — 경로 수만 센다) · `:165-166` (경로 커밋이면 바로 돌아감) · `:185-190` (목록 삭제 + `-a`) · `:119` (막는 문구) | 경로 커밋의 삭제를 안 센다 · `-i <경로>` 의 작업 폴더 삭제를 안 센다 | ER-01 · RE-02 |
| `harness/evals/hooks/commit-guard-test.sh` | `:3` (번호 주석) · `:113-119` (⑬ ⑭ — 목록 삭제 60 개 두고 `-o a.txt` 통과) | 경로 안 삭제 · 희소 체크아웃 경우가 없다 | ER-01 |
| `harness/scripts/save-feedback.sh` | `:42-88` (`:53` · `:75` 여덟 필드) · `:90` · `:206-219` (다시 계산) · `:314` | 초안에 다시 계산할 두 필드를 요구 | ER-02 · RE-02 |
| `harness/evals/kaizen/feedback-system/save-test.sh` | `:44-72` (초안) · `:102-121` (음성 시험) | 두 필드 없는 초안 경우가 없다 | ER-02 |
| `harness/skills/sprint/SKILL.md` | `:30-40` (Step 0) · `:73-77` (Step 3 · `:77` 사유 한 줄) · `:86-92` (QA 블록) · `:130-134` (Step 5) · `:136-138` (Step 6) · `:140-149` (References) | 내 경로만 커밋 · 워크트리 · 원인 가르기 · 네 칸 · 끝 줄 없음 | SK-01 ~ SK-04 |
| `harness/skills/create-agent/SKILL.md` | `:25` · `:33` · `:81` · `:106` | 「15 종」 · 「2건 이상 자동 REJECT」 · 앱 이름 | SK-05 |
| `harness/skills/create-skill/SKILL.md` | `:24` · `:29` · `:31` | 「1500-2000 words」 · 「argument-hint 누락은 discovery 실패」 | SK-05 |
| `harness/skills/contract-kaizen/SKILL.md` | `:63-74` (Step 2 · `:68` 임계) | 옛 문구 true 를 가르지 않는다 | SK-06 |
| `harness/skills/harness-kaizen/SKILL.md` | `:120-133` (Step 2a · `:127`) | 같은 세기 | SK-06 |
| `harness/README.md` | `:44-63` (커밋 안전 훅 · `:55` 경로 커밋은 검사하지 않는다) | 바뀐 동작 · 범위 선언 자리 없음 | AR-03 · AR-04 |
| `harness/docs/guides/plugin-validation-guide.md` | `:1-5` · `:431-463` (V10 · 범위 `:445-449`) · `:650-656` (이력) | 스킬 폴더 안 references 가 범위 밖 | AR-01 |
| `scripts/validate-plugin.py` | `:760-782` (V10 설명) · `:783-789` (범위) · `:512-519` (V6 범위 — 바꾸지 않는다) | 같은 범위 밖 | AR-01 |
| `scripts/collect-kaizen-data.py` | `:73-76` · `:117` · `:448-449` | 폴더 이름 두 곳 | AR-02 · RE-01 |
| `scripts/test-collect-kaizen-data.py` | `:184-266` · `:269-289` | 이름 한 곳을 재는 경우가 없다 | AR-02 |

구현 후보가 둘 이상이었던 곳의 선택:

- **경로 커밋의 삭제를 무엇으로 셀지** — HEAD 를 읽은 임시 목록 대 공용 · 개인 목록. **임시 목록을 쓴다.** git 이 경로 커밋을 그렇게 만든다
  (근거 파일 §2 P07 「`git diff --cached` 는 `commit -o` 가 만들 커밋과 같지 않다」). 공용 목록으로 세면 `git rm --cached` 로 목록에서만 뺀 60 개를
  삭제로 잘못 세 막고(git 은 0 개를 싣는다), 빈 개인 목록으로 세면 HEAD 의 60 개 전부를 잘못 센다 — 두 변이가 각각 ⑳ · ㉑ 에서 떨어진다(ER-01 (b)).
  임시 목록에는 희소 체크아웃(`git sparse-checkout`)의 `S`(skip-worktree) 표시가 없어 꺼내지 않은 파일을 전부 삭제로 센다 — 검토가 멀쩡한 커밋
  두 형태(`-- .` · `-- d1 keep`)를 막는 것을 실측했다(git 이 실은 삭제는 0). 그래서 공용 목록의 `S` 줄을 센 이름에서 뺀다(㉕ · 셋째 변이).
  경로 커밋마다 HEAD 전체를 임시 목록으로 읽으므로 추적 파일이 아주 많은 저장소에서는 느려질 수 있다 — 재지 않았다. notes 다음 사이클 메모로 남긴다
- **`--pathspec-from-file`** — 경로 목록 파일을 훅이 읽지 않는다. `git ls-files` 가 그 옵션을 받지 않고(실측 `unknown option`) 드문 형태라
  통과시키고 README 에 적는다 (AR-04). 훅은 판단이 안 서는 입력을 통과시키는 설계다(`commit-guard.sh:6-7`)
- **YAML 블록 검사를 더할지 (F18)** — **더하지 않는다.** 14 킷 마크다운의 `yaml` 펜스 60 개를 파싱하면 3 개가 실패하는데 셋 다 일부러 깨 놓은
  예시거나 자리표시자다(`plugin-validation-guide.md:144` · `skill-design-guide.md:554` · `planning-kit/agents/planning-reviewer.md:66`) — 걸리는 것이 전부
  잘못 잡은 것이다. 실행되는 YAML 은 이미 V2(`templates/`)와 `validate-doc-contracts.py`(`# docs-contract` 블록)가 파싱한다
- **범위 선언 자리** — 계약 `## 범위 경계` 절 안 `# sprint-scope` 블록 · 따로 파일 · frontmatter 배열 셋 가운데 **계약 안 블록**. 봉인 커밋이 계약
  파일 하나만 담으므로(sprint-contract Step 6.7 (c)) 따로 파일은 그 규칙을 바꿔야 하고, frontmatter 는 셸 읽기 함수가 한 줄 값만 읽는다(근거 파일 §5).
  계약 안 블록은 봉인 커밋이 원문을 남기고 `# docs-contract` 블록과 같은 모양이라 읽는 쪽이 짧다(AR-03 의 한 줄 awk). 쓰는 절차(sprint-contract ·
  contract-schema)와 읽는 훅은 다음 사이클 — 훅이 이번 세션의 계약을 찾는 방법(훅 입력 `session_id` 와 계약 `owner_session`)은 그때 실측한다
- **V6 범위** — V10 과 같이 넓히지 않는다. 넓히면 스킬 폴더 안 references 의 언어 힌트 없는 펜스 8 개(카이젠 PR 템플릿 넷 × 2)가 바로 걸린다 — 고치고 넓히는 것은
  다음 사이클(ER-05)
- **원인 가르기 규칙의 자리** — `/sprint` Step 3. 다른 킷은 플러그인이 따로 설치돼 이 파일을 경로로 가리킬 수 없으니 같은 판정 세 줄을 옮겨 적게 한다(ER-05)
- **create-agent · create-skill 의 나머지 낡은 사실 (근거 파일 §3)** — create-agent `:25` · `:80` 의 「`model` 을 생략하면 `inherit`」 와 create-skill `:27` 의
  「공식 필수는 `name` 과 `description`」 · 「다른 플랫폼에서는 무시된다」 는 **고치지 않는다.** 두 스킬이 기준 원본으로 가리키는 `agent-design-guide.md:79` ·
  `skill-design-guide.md` §frontmatter 규칙이 Phase 1 파일이고, Phase 1 은 제 근거 파일에 없어 다음 사이클 메모로 남겼다(`phase1-notes.md` §다음 사이클 메모).
  스킬 쪽만 고치면 스킬과 가이드가 갈린다 — 가이드와 함께 고치도록 넘긴다(ER-05)

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 파일 | 인용 | 이번 처리 |
| --- | --- | --- |
| `harness/hooks/hooks.json:41` · `:53` · `harness/templates/settings-hooks.json:43` · `:55` | 훅 등록 — `commit-guard.sh pre` · `post` | 인자 · 이름이 그대로라 고치지 않는다 |
| `.github/workflows/ci.yml:123` · `:112` · `:68` | 훅 시험 · 피드백 저장 시험 · 수집기 시험을 돌린다 | 새 경우는 기존 시험 파일 안에 넣어 CI 줄을 더하지 않는다 (ER-01 · ER-02 · AR-02) |
| `harness/skills/sprint-contract/SKILL.md` Step 9 · `harness/agents/qa-evaluator.md` | 피드백 초안을 쓴다 | 초안에 두 필드를 적어도 전처럼 저장된다(적은 값은 `draft_*` 로 남는다). Step 9 문구 정리는 다음 사이클 Phase 2 (ER-05) |
| `harness/skills/sprint-contract/SKILL.md` Step 5 · `harness/docs/guides/skill-design-guide.md` §3.7 | `/sprint` 가 맞출 원문 | SK-04 (c) 가 원문이 `$END` 에 그대로인지 잰다 |
| `harness/docs/guides/agent-design-guide.md` · `skill-design-guide.md` | create-agent · create-skill 이 가리키는 표 · 절 | SK-05 가 가리킨 값 · 절이 `$END` 에 있는지 잰다 |
| 14 킷의 `skills/*/references/**/*.md` | V10 새 대상 41 개 | 지금 끊긴 표 0 개 — AR-01 · DG-05 |
| `.claude/skills/kaizen-orchestrator/SKILL.md:222` `# docs-contract` 블록 | 수집기 폴더 이름 선언 | 값이 그대로라 고치지 않는다 — AR-02 (d) · DG-05 |
| `infra-kit` (backend-family:P3) · `rust-kit` (backend-family:P4) · `flutter-preflight` · `react-preflight` | 원인 가르기 규칙 | 다른 Phase 소관 — 맞출 문장을 notes 로 넘긴다 (ER-05) |

### 개선안 초안

정확한 문구는 스크래치 `mock.py`(`회귀 게이트` 절 경로)가 시작 커밋 판 열네 파일에 적용하는 치환 그대로다. BUILD 는 이것을 기준으로 적용한다. 요지:

- `harness/scripts/commit-guard.sh` — 인자를 가를 때 경로 인자를 모으고(`--pathspec-from-file` 은 따로 표시), 경로 커밋이면 HEAD 를 읽은 임시 목록에서
  그 경로 안 `ls-files --deleted` 를 세어 50 개를 넘으면 `확인: git status --short -- <지정한 경로>` 와 함께 막는다. 병합 도중 확인 뒤로 옮긴다.
  희소 체크아웃으로 꺼내지 않은 파일(공용 목록 `ls-files -t` 의 `S`)은 센 이름에서 뺀다. `-i <경로>` 는 목록 삭제에 그 경로의 작업 폴더 삭제를 더한다.
  막는 문구 `git add 나 -a` → `git add · -a · -i`
- `harness/evals/hooks/commit-guard-test.sh` — 번호 주석, ⑰ ~ ㉕ 열 줄(⑰-확인 포함). ㉕ 는 희소 체크아웃이 실제로 걸렸는지부터 보고 안 걸렸으면 FAIL 로 적는다
- `harness/scripts/save-feedback.sh` — 초안 필수 여섯(`schema_version skill timestamp skill_version outcome diagnosis`)과 최종본 여덟(+ `project_hash project_name`)을
  배열 둘로 두고 `validate_yaml <파일> <필드…>` 가 두 백엔드에서 같은 목록을 쓴다
- `harness/evals/kaizen/feedback-system/save-test.sh` — 초안 원본 사본, ⑧ 두 필드 없는 초안 저장 · ⑨ `timestamp` 만 빠진 초안의 누락 보고
- `harness/skills/sprint/SKILL.md` — Step 0 워크트리 문단과 명령 블록, Step 3 네 칸 · 원인 가르기 문단 · 블록 · 표, Step 4 QA 블록 끝 줄, Step 5 내 경로만 싣기 문단 ·
  블록 · 불릿 넷(쓰지 않는 명령에 `git commit -i` 포함 — 근거 파일 §4 둘째 항) · 실측, Step 6 끝맺음, References 네 줄
- `harness/skills/create-agent/SKILL.md` — `15 종` 셋 → `18 종`, Unverifiable 4 항 요약을 agent-design-guide §10 과 같은 말로(앱 이름 빼기), 고치는 줄의 `에 대해` 빼기
- `harness/skills/create-skill/SKILL.md` — 「1500-2000 words」 → 500 줄 권고(skill-design-guide 절 인용), `argument-hint` 설명, 「2000 words」 → 「500 줄 권고」
- `harness/skills/contract-kaizen/SKILL.md` Step 2 · `harness/skills/harness-kaizen/SKILL.md` Step 2a — 옛 문구 12 항목은 `measure_premise_unrun` 키가 있는 파일에서만 센다
- `harness/README.md` 커밋 안전 훅 — 경로 커밋 문단(희소 체크아웃 문장 포함), 검사하지 않는 형태 문장 고침, 범위 선언 자리 문단과 예시 블록
- `harness/docs/guides/plugin-validation-guide.md` — 1.3.1 → 1.4.0, V10 범위 문단, 이력 한 줄
- `scripts/validate-plugin.py` — V10 설명 · 범위 한 줄
- `scripts/collect-kaizen-data.py` — `USAGE_DATA_INPUTS` → 폴더 이름 상수 `USAGE_DATA_DIRS` 하나, 읽는 자리와 `doc_contract()` 가 같이 쓴다
- `scripts/test-collect-kaizen-data.py` — 폴더 이름을 한 곳에서 바꾸면 두 자리가 같이 바뀌는지 보는 경우 하나

## 범위 경계

- 이 Phase 시작 HEAD: `3a51b733ab84a997fe34de042fcc743b45664f46`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p04-harness.md` 의 `end_sha:`
  마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열넷이다 — `harness/scripts/commit-guard.sh` · `harness/evals/hooks/commit-guard-test.sh` · `harness/scripts/save-feedback.sh` ·
  `harness/evals/kaizen/feedback-system/save-test.sh` · `harness/skills/sprint/SKILL.md` · `harness/skills/create-agent/SKILL.md` · `harness/skills/create-skill/SKILL.md` ·
  `harness/skills/contract-kaizen/SKILL.md` · `harness/skills/harness-kaizen/SKILL.md` · `harness/README.md` · `harness/docs/guides/plugin-validation-guide.md` ·
  `scripts/validate-plugin.py` · `scripts/collect-kaizen-data.py` · `scripts/test-collect-kaizen-data.py`. 새 파일은 없다. `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase4-notes.md` · `.harness/.meta/kaizen-0924/phase4-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-05 ③ `verify_seal` 로 잰다
- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p04-harness` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-05 · ER-05 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-05 ① 과 ER-05 넷째 측정은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 **`git add -- <파일> && git commit -o -- <파일…>` 로 열네 파일만** 싣는다(SK-01 이 가르치는 형태). 이 세션의 커밋 훅은 설치본이다 —
  훅 등록(`harness/hooks/hooks.json:41`)이 설치된 플러그인 폴더를 가리키므로 이 가지의 새 판은 BUILD 커밋에 걸리지 않는다. 새 판의 동작은 ER-01 이 시험 저장소에서 잰다
- 측정이 기대는 제목은 이름을 바꾸지 않는다: `### Step 0: Pre-Sprint Sync Check` · `### Step 3: 빌드/분석 검증` · `### Step 4: QA Evaluator` · `### Step 5: Commit` ·
  `### Step 6: Push` (sprint) · `### Step 2: Triage` (contract-kaizen) · `### Step 2a` (harness-kaizen) · `## 커밋 안전 훅` (README) · `### V10 마크다운 표 무결성` ·
  `## 8. 변경 이력` (검증 가이드) · `### SKILL.md 본문 500 라인 미만 권고` (skill-design-guide — 읽기만)
- 공유 파일(`marketplace.json` · `plugin.json` 버전 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 로그 · 실패 횟수 파일 · `docs/kaizen/*.md` ·
  `.github/workflows/ci.yml`)과 다른 Phase 소관 파일(sprint-contract · qa-evaluator · 설계 가이드 넷 · `harness/references/`)은 건드리지 않는다 — ER-05 셋째 · 넷째 측정.
  harness README 의 AUTO 구간은 스킬 frontmatter 를 읽는데 frontmatter 를 바꾸지 않는다. 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- 넘기는 것 — BUILD 가 notes(`.harness/.meta/kaizen-0924/phase4-notes.md`)에 아래 열다섯 문자열을 **각각 한 줄에 한 번 이상** 적는다(ER-05 가 글자 그대로 센다):
  `sprint-contract Step 9` (다음 사이클 Phase 2 — 초안 필수 여섯으로 문구를 맞추고, 고정 이름 `.harness/feedback-draft.yaml` 을 여러 세션이 덮는 문제 · Phase 3 메모) ·
  `feedback-schema.yaml` (다음 사이클 Phase 2 · 3 — true 가 「문제가 있다」 인 뜻과 새 키 둘. harness-kaizen Gotcha 가 이 파일 수정을 막는다) ·
  `# sprint-scope` (쓰는 쪽은 다음 사이클 Phase 2 — contract-schema 절 · sprint-contract Step 6. 읽는 쪽은 다음 사이클 Phase 4 — 커밋 훅이 `owner_session` 으로 이번 세션의 계약을 찾는다) ·
  `assertions.json 실행기` (Phase 3 넘김 — 이번에 만들지 않는다. 처리 배정표 밖) · `agent-design-guide.md:79` (다음 사이클 Phase 1 — model 을 생략했을 때의 동작, 근거 파일 §3) ·
  `sprint-contract Step 6.7 (a)` (다음 사이클 Phase 1 · 2 — 같은 작업 폴더에서 `checkout -b` 하지 않는다는 문장을 skill-design-guide §9 와 함께) ·
  `backend-family:P3` · `backend-family:P4` (Phase 8 · 9 — `/sprint` Step 3 의 판정 세 줄을 옮겨 적는다) · `flutter-preflight` · `react-preflight` (Phase 5 · 10 — 기준 커밋 비교 없음) ·
  `F20` (Phase 11 — 폐기 결정 기록 자리를 하나로 정한 뒤 `/sprint` 재검증 블록에 읽는 줄) · `V6 범위` (다음 사이클 — 언어 힌트 없는 펜스 8 개를 고친 뒤 넓힌다) ·
  `reflect-collector:P5` (다음 사이클 Phase 4 — `save-feedback.sh` 가 `project_name` 을 워크트리 폴더 이름으로 적는다. 규칙의 근거는 이번 사이클 `phase12.md` 에만 있다 — `배경` 표 행) ·
  `create-agent/SKILL.md:25` (다음 사이클 Phase 1 · 4 — `model` 을 생략했을 때의 동작. `agent-design-guide.md:79` 와 함께 고친다) ·
  `create-skill/SKILL.md:27` (다음 사이클 Phase 1 · 4 — 「공식 필수」 · 「다른 플랫폼에서는 무시된다」. skill-design-guide §frontmatter 규칙과 함께 고친다).
  처리 배정표 키 열(`F08` · `F09` · `F14` · `F18` · `F28` · `harness:P02` · `harness:P07` · `user-setup:P2` · `other-kits:P10` · `insights:scope-commit-block`)도 notes 에 적는다.
  러닝북이 적게 한 나머지(바꾼 파일 · changelog 한 단락 · 킷 로그 한 단락 · 다음 사이클 메모)도 notes 에. `.github/workflows/ci.yml` 에 넣을 줄은 없다 — 새 경우는 이미 CI 가 돌리는 시험 파일 안에 있다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다. 설치본 커밋 훅은 이 가지의 새 판이 아니다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase4-review.md`. 검토 VERDICT: 1 회차(2026-09-25 03:37)
  `CHANGES` — 막는 이유 넷(ER-01 · ER-05 · AR-05 · ER-03)과 조건별 고칠 문구 여섯 묶음을 초안이 전부 반영했다. 2 회차(2026-09-25 04:13) `APPROVE` —
  새로 막을 결함 없음, 막지 않는 권고 셋. BUILD 가 봉인 전에 셋을 이렇게 다뤘다 — 첫째(AR-05 ① 이 다른 Phase 서명 커밋도 센다)는 아래 줄로 안내만
  남기고 조건 문구는 그대로 둔다, 둘째(`mut.py` 가 모의본 문구를 글자 그대로 찾는다)는 BUILD 가 `mock.py` 치환을 글자 그대로 적용해 지킨다,
  셋째(서명 줄로 가리는 조건 목록에 DG-03 이 빠졌다)는 위 서명 줄 문단에 DG-03 을 더했다. 3 회차 검토는 없다
- AR-05 ① 이 1 이상이면 그 커밋의 서명 줄부터 본다 — 다른 Phase 서명(`Kaizen-Phase: kaizen-0924-p05-…` 등)이 달린 커밋이면 이 Phase 가 서명을
  빠뜨린 것이 아니다. 판정은 조건 문구 그대로다(2 회차 검토 권고 첫째 — 거짓 통과가 아니라 거짓 실패 쪽이다)
- 오라클 해소: SK-01 ~ SK-06 · AR-01 (d) · AR-03 · AR-04 — 산출물이 스킬 · 문서 문장 자체라 정해진 절 구간에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고
  절을 잘라 재며, 편집 전 파일에서 새 문장 0 · 옛 문장 1 을 봉인 전에 확인했다. 문장 하나만 지운 사본에서 그 값이 0 으로 떨어지는지 돌렸다(`회귀 게이트` 절 표).
  코드 블록을 가르치는 조건(SK-01 (b) · SK-03 (b) · AR-03)은 블록을 떼어 답을 아는 입력에서 실제로 돌린다
- 오라클 해소: ER-01 · ER-02 · AR-01 (a)~(c) · AR-02 — 시험 · 검사를 실제로 돌린 출력이다. 음성 대조(시작 커밋 판 · 변이)와 알려진 답(git 이 실제로 싣는 삭제 수 ·
  `find` 로 따로 센 파일 수 · 3e3ff04 의 지운 줄)이 붙어 있다
- 오라클 해소: ER-03 · ER-04 · AP-01 · AP-03 — 더한 줄을 세는 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-05 · AR-05 · SC-00 · DG-01 — 커밋 기록(`git log`)과 notes 문자열 · 봉인 검증 함수를 실제로 돌린 출력이다
- 오라클 해소: DG-02 · DG-05 · DG-06 — 린터 · 검사 스크립트를 실제로 돌린 출력이다. 뒤따르는 대조는 그 출력의 파일 경로를 이 Phase 파일과 맞출 뿐이다
- 커버리지 해소: SK-01 · SK-03 · SK-04 · SK-05 · SK-06 · ER-01 · ER-02 · AR-01 · AR-02 · AR-03 — 산문의 파일 이름은 측정의 `"$SP"` · `"$RM"` ·
  `"$CA"` · `"$CS"` · `"$T/E/…"` 다. 공통 정의가 그 이름으로 `$END` 판을 꺼낸다. 도우미 이름(`ka-commit.sh` 등)은 측정의 `"$K/…"` 로 부른다
- 커버리지 해소: SK-01 · SK-03 · SK-04 — `/sprint` 는 경로가 아니라 스킬 이름이다. 파일은 `"$SP"`
- 커버리지 해소: SK-05 — `phase1-notes.md` · `create-skill/SKILL.md:29` 는 재는 대상이 아니라 넘김 출처다. URL 은 측정의 `grep -cF` 인자다
- 커버리지 해소: ER-01 — `/bin/bash` 는 해석기다. 측정이 그 해석기로 시험을 돌린다
- 커버리지 해소: ER-05 — notes 경로는 공통 정의의 `$NOTES`, `feedback-schema.yaml` · `create-agent/SKILL.md:25` · `create-skill/SKILL.md:27` 은 측정 `for t in …` 한 줄의 인자다
- 커버리지 해소: AR-01 — 여섯 범위 글롭은 측정 `find` 인자로 하나씩 옮겼다(`-name SKILL.md` · `agents` · `references` · `docs` · `-path "$k/skills/*/references/*"` · `README.md`). `/skills/[^/]+/references/` 는 측정의 `grep -cE` 인자다
- 커버리지 해소: AR-03 — 기대 출력 두 줄은 측정 끝의 한 문자열(공백으로 이은 두 경로)이다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint · shellcheck `SC2016` 둘)는 범위 밖이다 — DG-02 는 더한 줄과 새 경고만 잰다
- 기능 조건 18 · 전체 조건 줄 28

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 블록을 먼저 실행한 **bash** 셸에서 돈다 — 블록과 측정을 한 `bash -c` 안에 넣거나 블록을 파일로 저장해 `. 파일` 뒤에 잇는다.
`END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. 이 절의 도우미 코드 블록 열하나는 각 블록 첫 `#` 주석 줄(셔뱅 다음)에 적힌 이름 그대로 한 폴더에 저장하고, 그 폴더를 공통 정의 블록을 돌리기 전에 `K` 에 넣는다.
`new-warnings.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측: 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` (2026-09-25). 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
준비 단계 실측(2026-09-25): `command -v jq` → `/usr/bin/jq` (jq-1.7.1-apple) · `command -v shellcheck` → `/opt/homebrew/bin/shellcheck` (0.11.0) ·
`command -v yq` → 출력 없음 · 종료 코드 1 (그래서 `parity.sh` 가 가짜 yq 를 만든다) · `/bin/bash --version` 3.2.57 · `zsh --version` 5.9 · `git --version` 2.53.0 ·
`python3 -c 'import yaml'` 6.0.3.

```bash
# 측정 공통 정의 — bash 로 실행한다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다 — C 로케일이면 덜 잡힌다
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924 || exit 2
B=3a51b733ab84a997fe34de042fcc743b45664f46                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p04-harness'
CF=.harness/sprint-contract-kaizen-0924-p04-harness.md
AM=.harness/sprint-amendments-kaizen-0924-p04-harness.md
NOTES=.harness/.meta/kaizen-0924/phase4-notes.md
EVID=.harness/.meta/evidence/phase4.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
FILES=(harness/scripts/commit-guard.sh harness/evals/hooks/commit-guard-test.sh
  harness/scripts/save-feedback.sh harness/evals/kaizen/feedback-system/save-test.sh
  harness/skills/sprint/SKILL.md harness/skills/create-agent/SKILL.md harness/skills/create-skill/SKILL.md
  harness/skills/contract-kaizen/SKILL.md harness/skills/harness-kaizen/SKILL.md harness/README.md
  harness/docs/guides/plugin-validation-guide.md scripts/validate-plugin.py
  scripts/collect-kaizen-data.py scripts/test-collect-kaizen-data.py)
FRE='harness/(scripts/(commit-guard|save-feedback)\.sh|evals/hooks/commit-guard-test\.sh|evals/kaizen/feedback-system/save-test\.sh|skills/(sprint|create-agent|create-skill|contract-kaizen|harness-kaizen)/SKILL\.md|README\.md|docs/guides/plugin-validation-guide\.md)|scripts/(validate-plugin|collect-kaizen-data|test-collect-kaizen-data)\.py'
MDS=(harness/skills/sprint/SKILL.md harness/skills/create-agent/SKILL.md harness/skills/create-skill/SKILL.md
  harness/skills/contract-kaizen/SKILL.md harness/skills/harness-kaizen/SKILL.md harness/README.md
  harness/docs/guides/plugin-validation-guide.md)
SHS=(harness/scripts/commit-guard.sh harness/evals/hooks/commit-guard-test.sh harness/scripts/save-feedback.sh
  harness/evals/kaizen/feedback-system/save-test.sh)
PYS=(scripts/validate-plugin.py scripts/collect-kaizen-data.py scripts/test-collect-kaizen-data.py)
T=$(mktemp -d); H=$(mktemp -d)   # H = 피드백 저장 시험의 HOME — 전역 피드백 폴더(~/.harness/feedback)에 쓰지 않는다
mkdir -p "$T/B" "$T/E"
# 시험은 두 판을 풀어 둔 폴더에서 돈다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B"; git archive "$END" | tar -x -C "$T/E"
SP=$T/E/harness/skills/sprint/SKILL.md; RM=$T/E/harness/README.md
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
toks()  { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
labels() { grep -E '^FAIL ' | awk '{print $2}' | sort | tr '\n' ' '; echo; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

ER-01 (c) 알려진 답 — 경로 지정 커밋 열한 경우에서 훅 판정과 git 이 실제로 싣는 삭제 수를 맞대 본다:

```bash
#!/usr/bin/env bash
# align.sh <훅 경로> — 경로 지정 커밋 열한 경우마다 훅 판정(exit 2 = 막음)과 git 이 실제로 싣는 삭제 수를 맞대 본다.
# 답은 git 이 낸다: 같은 명령을 훅 없이 실제로 커밋해 HEAD 의 삭제 줄을 센다. 막음 ⇔ 삭제 50 개 초과 여야 agree.
hook=${1:?}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
unset HARNESS_COMMIT_GUARD GIT_INDEX_FILE GIT_DIR GIT_WORK_TREE
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
mk() { local r=$1 k; mkdir -p "$r/d1"; git -C "$r" init -q -b main
  for ((k = 1; k <= 60; k++)); do printf 'l%d\n' "$k" >"$r/d1/$(printf 'f%03d' "$k")"; done
  echo a >"$r/a.txt"; git -C "$r" add -A; git -C "$r" commit -qm init; }
rms() { local k; for ((k = 1; k <= $2; k++)); do git -C "$1" rm -q "d1/$(printf 'f%03d' "$k")"; done; }
rmw() { local k; for ((k = ${3:-1}; k <= $2; k++)); do rm -f "$1/d1/$(printf 'f%03d' "$k")"; done; }
case_() {  # case_ <이름> <cwd> <명령>
  local name=$1 cwd=$2 cmd=$3 rc dels before
  jq -nc --arg c "$cmd" --arg d "$cwd" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}' \
    | bash "$hook" pre >/dev/null 2>&1; rc=$?
  before=$(git -C "$cwd" rev-parse HEAD)
  (cd "$cwd" && eval "$cmd") >/dev/null 2>&1
  if [ "$(git -C "$cwd" rev-parse HEAD)" = "$before" ]; then dels=0
  else dels=$(git -C "$cwd" show --diff-filter=D --name-only --format= HEAD | grep -c .); fi
  if { [ "$rc" = 2 ] && [ "$dels" -gt 50 ]; } || { [ "$rc" != 2 ] && [ "$dels" -le 50 ]; }; then a=agree; else a=DISAGREE; fi
  printf '%s hook_rc=%s git_dels=%s %s\n' "$name" "$rc" "$dels" "$a"
}
r=$w/17; mk "$r"; rmw "$r" 60; case_ ⑰ "$r" 'git commit -o d1 -m x'
r=$w/18; mk "$r"; rms "$r" 51; case_ ⑱ "$r" 'git commit -m x -- d1'
r=$w/19; mk "$r"; rmw "$r" 50; case_ ⑲ "$r" 'git commit -o d1 -m x'
r=$w/20; mk "$r"; git -C "$r" rm -q -r --cached d1; case_ ⑳ "$r" 'git commit -o d1 -m x'
r=$w/21; mk "$r"; echo more >>"$r/d1/f001"; case_ ㉑ "$r" "GIT_INDEX_FILE=$w/21-none.idx git commit -o d1 -m x"
r=$w/22; mk "$r"; rms "$r" 10; rmw "$r" 55 11; case_ ㉒ "$r" 'git commit -i d1 -m x'
r=$w/23; mk "$r"; rmw "$r" 59; case_ ㉓ "$r" "git commit -o 'd1/f0*' -m x"
r=$w/24; mk "$r"; rmw "$r" 60; case_ ㉔ "$r/d1" 'git commit -o . -m x'
r=$w/25; mk "$r"; { mkdir -p "$r/keep"; echo k >"$r/keep/b.txt"; git -C "$r" add keep; git -C "$r" commit -qm keep
  git -C "$r" sparse-checkout set --cone keep; echo more >>"$r/keep/b.txt"; } >/dev/null 2>&1; case_ ㉕ "$r" 'git commit -o -m x -- .'
r=$w/13; mk "$r"; rms "$r" 60; echo more >>"$r/a.txt"; case_ ⑬ "$r" 'git commit -o a.txt -m x'
r=$w/14; mk "$r"; rms "$r" 60; echo more >>"$r/a.txt"; case_ ⑭ "$r" 'git commit -m x -- a.txt'
```

SK-01 (b) — `/sprint` Step 5 블록을 떼어 남의 올려 둔 변경이 있는 저장소에서 돌린다:

```bash
#!/usr/bin/env bash
# ka-commit.sh <SKILL.md> — /sprint Step 5 의 내 경로만 싣는 코드 블록을 떼어, 남이 공용 목록에 올려 둔 삭제 · 수정이 있는
# 저장소에서 돌린다. 답: 커밋에 실린 경로 = "A new.txt M mine.txt" · 남의 두 변경(other.txt 삭제 · shared.txt 수정)은 목록에 그대로
skill=${1:?}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
blk=$(awk '/^```bash$/{b=1; buf=""; next} b&&/^```$/{if (buf ~ /git show --name-status --format= HEAD/) {printf "%s", buf; exit} b=0; next} b{buf=buf $0 "\n"}' "$skill")
[ -n "$blk" ] || { echo "NO_BLOCK"; exit 2; }
blk=${blk//<새 파일…>/new.txt}
blk=${blk//<내 경로…>/new.txt mine.txt}
blk=${blk//<메시지>/x}
printf '%s\n' "$blk" > "$w/commit.sh"
r=$w/r; mkdir -p "$r"
{
  git init -q -b main "$r"
  for f in mine other shared; do echo 1 >"$r/$f.txt"; done
  git -C "$r" add -A; git -C "$r" commit -qm init
  git -C "$r" rm -q other.txt; echo 2 >>"$r/shared.txt"; git -C "$r" add shared.txt   # 남이 올려 둔 것
  echo 2 >>"$r/mine.txt"; echo n >"$r/new.txt"                                        # 내 변경
} >/dev/null 2>&1
(cd "$r" && bash "$w/commit.sh") >/dev/null 2>&1
echo "committed=[$(git -C "$r" show --name-status --format= HEAD | tr '\t\n' '  ' | sed 's/ *$//')]"
echo "still_staged=[$(git -C "$r" diff --cached --name-status | tr '\t\n' '  ' | sed 's/ *$//')]"
```

SK-03 (b) — `/sprint` Step 3 블록을 떼어 답을 아는 네 경우에서 돌린다:

```bash
#!/usr/bin/env bash
# ka-split.sh <SKILL.md> — /sprint Step 3 의 원인 가르기 코드 블록을 떼어 네 경우의 답을 아는 저장소에서 돌린다.
# 자리표시자: <기준 가지> → main, <실패한 검사 명령> → grep -q ok status.txt (status.txt 가 ok 면 통과)
# 답: S1 기준에서 이미 실패 = 1 1 1 · S2 이번 커밋 탓 = 1 0 0 · S3 미커밋 탓 = 0 0 0 (공용 폴더만 1) · S4 분기 뒤 기준 가지 = 0 0 1
skill=${1:?}
runner=${RUNNER:-bash}   # RUNNER=zsh 면 떼어 낸 블록을 zsh 로 돌린다
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
blk=$(awk '/^```bash$/{b=1; buf=""; next} b&&/^```$/{if (buf ~ /FORK_BASE=\$\(git merge-base/) {printf "%s", buf; exit} b=0; next} b{buf=buf $0 "\n"}' "$skill")
[ -n "$blk" ] || { echo "NO_BLOCK"; exit 2; }
blk=${blk//<기준 가지>/main}
blk=${blk//<실패한 검사 명령>/grep -q ok status.txt}
printf '%s\n' "$blk" > "$w/split.sh"

mkrepo() {  # mkrepo <이름> <분기점 status> <내 커밋 status> <기준 가지 뒤 status> <미커밋 status>
  local o=$w/$1.git r=$w/$1
  {
  git init -q --bare -b main "$o"
  git clone -q "$o" "$r" 2>/dev/null
  echo "$2" >"$r/status.txt"; git -C "$r" add status.txt; git -C "$r" commit -qm fork; git -C "$r" push -q origin main
  git -C "$r" checkout -q -b feat
  echo "$3" >"$r/status.txt"; echo m >"$r/mine.txt"; git -C "$r" add -A; git -C "$r" commit -qm mine
  if [ -n "$4" ]; then
    local o2=$w/$1-other; git clone -q "$o" "$o2" 2>/dev/null
    echo "$4" >"$o2/status.txt"; git -C "$o2" commit -qam later; git -C "$o2" push -q origin main
    git -C "$r" fetch -q origin
  fi
  [ -n "$5" ] && echo "$5" >"$r/status.txt"
  } >/dev/null 2>&1
  echo "$r"
}
run_case() {  # run_case <이름> <저장소>
  local r=$2 shared out
  (cd "$r" && grep -q ok status.txt); shared=$?
  out=$(cd "$r" && "$runner" "$w/split.sh" 2>&1 | awk '{sub(/^exit=/, "", $NF); printf "%s ", $NF}')
  out=${out% }
  printf '%s shared=%s head/fork/base=%s worktrees=%s\n' "$1" "$shared" "$out" "$(git -C "$r" worktree list | grep -c .)"
}
run_case S1 "$(mkrepo s1 bad bad '' '')"
run_case S2 "$(mkrepo s2 ok bad '' '')"
run_case S3 "$(mkrepo s3 ok ok '' bad)"
run_case S4 "$(mkrepo s4 ok ok bad '')"
```

ER-02 (c) — python · 가짜 yq 두 백엔드의 실패 문구를 맞대 본다:

```bash
#!/usr/bin/env bash
# parity.sh <판 폴더> — 같은 초안을 python 경로와 가짜 yq 경로로 save-feedback.sh 에 넣어 FAIL 줄을 맞대 본다.
# 가짜 yq 는 `yq .<키> <파일>` 만 흉내 낸다 (없는 키 · null 은 진짜 yq 처럼 null). 이 기계에 yq 가 없어 python 경로만 돌기 때문이다
v=${1:?}; t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/bin" "$t/home"
cat >"$t/bin/yq" <<'YQ'
#!/usr/bin/env bash
exec python3 -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[2],encoding="utf-8")) or {}; v=d.get(sys.argv[1].lstrip(".")) if isinstance(d,dict) else None; print("null" if v is None else v)' "$@"
YQ
chmod +x "$t/bin/yq"
full() { printf '%s\n' 'schema_version: 1' 'timestamp: "2026-03-30T10:00:00+09:00"' 'project_hash: "testtest"' 'project_name: "test-project"' \
  'skill: sprint-contract' 'skill_version: "0.3.3"' 'outcome: completed' 'diagnosis:' '  checklist:' '    ambiguous_conditions: false' \
  '  cross_diagnosis_by: qa-evaluator' '  cross_diagnosis_notes: "시험"'; }
for drop in 'timestamp' 'project_hash|project_name|timestamp' 'project_hash|project_name|timestamp|outcome'; do
  for be in python yq; do
    full | grep -vE "^($drop):" >"$t/d.yaml"
    if [ "$be" = yq ]; then HOME=$t/home PATH="$t/bin:$PATH" bash "$v/harness/scripts/save-feedback.sh" contract "$t/d.yaml" >/dev/null 2>"$t/err"
    else HOME=$t/home bash "$v/harness/scripts/save-feedback.sh" contract "$t/d.yaml" >/dev/null 2>"$t/err"; fi
    printf '%s drop=%s rc=%s %s\n' "$be" "$drop" "$?" "$(grep '^FAIL' "$t/err")"
  done
done
echo "saved_under_home=$(find "$t/home" -type f | grep -c .)"
```

ER-02 (d) — 최종본 검사가 두 필드를 요구하는지 본다:

```bash
#!/usr/bin/env bash
# final8.sh <판 폴더> — 다시 계산한 project_name · project_hash 를 덧붙이는 두 줄만 지운 사본에 온전한 초안을 넣는다.
# 최종본 검사가 두 필드를 요구하면 저장이 멈춰야 한다
v=${1:?}; t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/s" "$t/home"; cp "$v"/harness/scripts/*.sh "$t/s/"
python3 - "$t/s/save-feedback.sh" <<'PY'
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
for key, var in (('project_name', 'PROJ_NAME'), ('project_hash', 'PROJ_HASH')):
    line = f"""  printf '{key}: %s\\n' "$(yaml_str "${var}")"\n"""
    print(key, s.count(line)); s = s.replace(line, '')
open(p, 'w', encoding='utf-8').write(s)
PY
printf '%s\n' 'schema_version: 1' 'timestamp: "2026-03-30T10:00:00+09:00"' 'project_hash: "testtest"' 'project_name: "test-project"' \
  'skill: sprint-contract' 'skill_version: "0.3.3"' 'outcome: completed' 'diagnosis:' '  checklist:' '    ambiguous_conditions: false' >"$t/d.yaml"
HOME=$t/home bash "$t/s/save-feedback.sh" contract "$t/d.yaml" >/dev/null 2>"$t/err"
echo "rc=$? $(grep -c 'identity 재작성 후 스키마 검증 실패' "$t/err") $(grep -cF "누락 필드: ['project_hash', 'project_name']" "$t/err") saved_under_home=$(find "$t/home" -type f | grep -c .)"
```

ER-01 (b) — 경로 커밋 삭제를 목록으로 세는 두 변이와 희소 체크아웃 빼기 줄을 지운 변이를 만든다:

```python
# mut.py <훅> <출력 폴더> — 경로 커밋 삭제를 공용 목록 · 개인 목록으로 세는 두 변이(⑳ · ㉑ 이 가르는지)와
# 희소 체크아웃 빼기 줄을 지운 변이(㉕ 가 가르는지)를 만든다
import sys
src = open(sys.argv[1], encoding='utf-8').read(); out = sys.argv[2]
old = '''  names=$(GIT_INDEX_FILE=$t/index git -C "$d" read-tree HEAD 2>/dev/null &&
    GIT_INDEX_FILE=$t/index git -C "$d" -c core.quotePath=false ls-files --full-name --deleted -- "${c_pathv[@]}" 2>/dev/null)'''
sparse = '''  # 희소 체크아웃으로 꺼내지 않은 파일(ls-files -t 의 S)은 작업 폴더에 없어도 git 이 싣지 않는다
  names=$(comm -23 <(printf '%s\\n' "$names" | grep . | sort) \\
    <(g ls-files -t --full-name -- "${c_pathv[@]}" | sed -n 's/^S //p' | sort))
'''
for a in (old, sparse):
    if src.count(a) != 1:
        sys.exit(f'NO_ANCHOR {src.count(a)}')
diff_head = 'git -C "$d" -c core.quotePath=false diff HEAD --name-only --diff-filter=D -- "${c_pathv[@]}"'
open(f'{out}/mut-shared.sh', 'w', encoding='utf-8').write(src.replace(old, f'  names=$({diff_head} 2>/dev/null)'))
priv = src.replace('check_path_commit "$d"', 'check_path_commit "$d" "$idx"').replace(old, f'''  local pi=${{2:-}}
  [ -n "$pi" ] && case $pi in /*) ;; *) pi=$d/$pi ;; esac
  names=$(if [ -n "$pi" ]; then GIT_INDEX_FILE=$pi {diff_head}; else {diff_head}; fi 2>/dev/null)''')
open(f'{out}/mut-private.sh', 'w', encoding='utf-8').write(priv)
open(f'{out}/mut-nosparse.sh', 'w', encoding='utf-8').write(src.replace(sparse, ''))
print('mutants ok')
```

AR-01 (b) 양성 대조 — 스킬 폴더 안 references/ 에 표가 끊긴 문서를 넣은 사본:

```bash
#!/usr/bin/env bash
# v10pos.sh <판 폴더> — 스킬 폴더 안 references/ 에 표가 끊긴 문서 하나를 넣은 사본에서 V10 을 돌린다
v=${1:?}; t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
cp -R "$v/scripts" "$v/.claude-plugin" "$v/api-kit" "$t/"
printf '%s\n' '# 끊긴 표' '' '| 열 | 값 |' '| --- | --- |' '| a | 1 |' '' '## 끼워 넣은 절' '' '| b | 2 |' >"$t/api-kit/skills/api-verify/references/zz-broken-table.md"
(cd "$t" && python3 scripts/validate-plugin.py api-kit --check=table-integrity 2>&1; echo "rc=$?") | grep -E 'V10|FAIL api-kit|^rc='
```

AR-02 (d) — 문서 대조가 폴더 이름 어긋남을 잡는지 본다:

```bash
#!/usr/bin/env bash
# drift.sh <판 폴더> — 문서 대조가 폴더 이름 어긋남을 잡는지 본다. 그대로 한 번, 폴더 이름 상수를 바꾼 사본에서 한 번
v=${1:?}; t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
cp -R "$v" "$t/r" && cd "$t/r" && { git init -q -b main && git add -A && git commit -qm snap; } >/dev/null 2>&1
python3 scripts/validate-doc-contracts.py >/dev/null 2>&1; echo "as_is rc=$?"
python3 - <<'PY'
p = 'scripts/collect-kaizen-data.py'; s = open(p, encoding='utf-8').read()
old = 'USAGE_DATA_DIRS: tuple[str, str] = ("facets", "session-meta")'
print('anchor', s.count(old)); open(p, 'w', encoding='utf-8').write(s.replace(old, old.replace('"facets"', '"facets2"')))
PY
python3 scripts/validate-doc-contracts.py > "$t/out" 2>&1; echo "renamed rc=$? $(grep -c 'usage_data_inputs` 불일치' "$t/out")"
```

AR-04 — README 가 검사하지 않는다고 적은 형태가 실제로 통과하는지 본다:

```bash
#!/usr/bin/env bash
# pfile.sh <훅> — 경로를 파일로 넘긴 커밋(--pathspec-from-file)은 README 대로 검사하지 않고 통과하는지 본다 (작업 폴더 삭제 60)
hook=${1:?}; w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
r=$w/r; mkdir -p "$r/d1"; { git init -q -b main "$r"; for ((k = 1; k <= 60; k++)); do echo "$k" >"$r/d1/f$k"; done
  echo a >"$r/a.txt"; git -C "$r" add -A; git -C "$r" commit -qm init; } >/dev/null 2>&1
rm -f "$r"/d1/f*; echo d1 >"$w/list"
jq -nc --arg c "git commit --pathspec-from-file=$w/list -m x" --arg d "$r" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}' \
  | bash "$hook" pre >/dev/null 2>&1
echo "pfile rc=$?"
```

DG-02 (a) — 더한 줄에 걸린 마크다운 경고만 센다:

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

AP-03 — 언어 힌트 없는 펜스 · 닫히지 않은 펜스를 센다:

```python
# fence.py <파일>… — 여는 펜스에 언어 힌트가 없으면 bare. 4-백틱 바깥 펜스 안의 ``` 는 내용으로 본다
import re, sys
tot_bare = tot_unclosed = 0
for path in sys.argv[1:]:
    open_len = 0; open_ch = ''; bare = []
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line.rstrip('\n'))
        if not m:
            continue
        run, rest = m.group(1), m.group(2).strip()
        if open_len == 0:
            open_len, open_ch = len(run), run[0]
            if not rest:
                bare.append(n)
        elif run[0] == open_ch and len(run) >= open_len and not rest:
            open_len = 0
    tot_bare += len(bare); tot_unclosed += 1 if open_len else 0
    print(f"{path}: bare_open={len(bare)} {bare} unclosed={1 if open_len else 0}")
print(f"bare_open_total={tot_bare} unclosed_total={tot_unclosed}")
```

봉인 전 실측 (2026-09-25 02:3x ~ 03:2x). 「편집 전」 은 시작 커밋 판(`git archive 3a51b73` → 스크래치 `p4d/base`), 「모의본」 은 스크래치
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p4d/mock.py` 를 그 사본에 적용한 판(`p4d/mock`)이다.
도우미는 `p4d/k/` 의 파일과 이 절의 코드 블록이 같다.

측정 묶음은 스크래치 `p4d/meas-pre.sh`(두 판 폴더에 조건 문구 그대로)와 `p4d/meas-full.sh`(공통 정의 그대로, `cd` 만 예행 저장소로)다.

```text
            편집 전 (B · E 둘 다 시작 커밋 판)                          모의본 (B = 시작 커밋 판 · E = 모의본)
[SK-01]     (a) 8 값 전부 0 (b) NO_BLOCK                                (a) 8 값 전부 1 (b) committed=[M mine.txt A new.txt] · still_staged=[D other.txt M shared.txt]
[SK-02]     5 값 전부 0                                                 5 값 전부 1
[SK-03]     (a) 7 값 전부 0 (b) NO_BLOCK · 종료 코드 2                  (a) 7 값 전부 1 (b) bash · zsh 둘 다 네 줄 요구값 · worktrees=1
[SK-04]     (a) 0 0 · 1 (b) 0 · 0 (c) 1 1 · 1                           (a) 1 1 · 0 (b) 1 · 1 (c) 1 1 · 1
[SK-05]     (a) 3 0 1 0 0 0 1 1 · N 15 대 가이드 18 (b) 1 2 0 0 1 · 0 · 1 (a) 0 3 0 1 1 1 0 0 · 18 대 18 (b) 0 0 1 1 0 · 1 · 1
[SK-06]     (a) 0 0 0 (b) 12 · 0 · 12 (c) 0                             (a) 1 1 1 (b) 12 · 12 · 0 (c) 1
[ER-01]     (a) rc=0 · rc=0 · 실패 0 건 둘 · 새 PASS 0                  (a) rc=0 · rc=0 · 실패 0 건 둘 · 새 PASS 10
            (c) agree 6 — ⑰ ⑱ ㉒ ㉓ ㉔ 가 DISAGREE                        (b) ⑰ ⑰-확인 ⑱ ㉒ ㉓ ㉔ · ⑳ · ⑳ ㉑ · ㉕ · 지운 사본 1 · 1
            git_dels 60 51 50 0 0 55 59 60 0 0 0 (두 판 같다 — git 이 낸 답) (c) agree 11
[ER-02]     (a) 1 0 0 · 남은 파일 0 (c) 두 필드 없는 초안에              (a) 1 1 1 · 0 (b) rc=1 · 1 (c) 세 줄 요구값 · saved_under_home=0
            ['timestamp', 'project_hash', 'project_name'] (두 백엔드 같음) (d) project_name 1 project_hash 1 rc=1 1 1 saved_under_home=0
            (d) 모의본과 같은 값 — 최종본 여덟 필드는 전에도 요구했다
[ER-03]     0 (새 (파일, URL) 쌍 0)                                     0 (새 쌍 5 · 양성 대조 1)
[ER-04]     0                                                           0 (첫 모의본 1 — 고치는 줄에 남은 「에 대해」)
[AR-01]     (a) V10 이 OK 인 14 킷 가운데 find 합집합과 다른 킷 10 ·      (a) 다른 킷 0 · references 킷 10 · 252 대 252
            V10 합 211 대 find 합 252 (b) 0 · 0 — `9 md files — OK` · rc=0 (b) 1 · 1 (c) 0 — V6 도 넓힌 변이는 8
            (c) 0 (d) 0 · 2026-09-24 · 0 0 · 0                          (d) 1 · 2026-09-25 · 1 1 · 1
[AR-02]     (a) 2 2 0 (b) 29 통과 · 0 실패 · 0                          (a) 1 1 1 (b) 31 통과 · 0 실패 · 2 (c) 2
            (d) as_is rc=0 · anchor 0 · renamed rc=0 0                  (d) as_is rc=0 · anchor 1 · renamed rc=1 1
[AR-03]     5 값 전부 0 · awk 빈 출력                                   5 값 전부 1 · harness/scripts/commit-guard.sh harness/evals/hooks/
[AR-04]     1 0 0 0 0 · pfile rc=0                                      0 1 1 1 1 · pfile rc=0
[AP-01]     0                                                           0 (양성 대조 1)
[AP-03]     bare 0 · unclosed 0                                         bare 0 · unclosed 0 (양성 대조 bare 1)
[AP-04]     1 1 1 1 1                                                   1 1 1 1 1
[RE-01]     0 0 0                                                       1 0 3
[RE-02]     (없음) · 0 · 1                                              check_path_commit() · 2 · 1
[DG-02]     (a) 일곱 줄 0:0 (b) 0 0 0 0 (c) 0 0 0                       (a) 더한 줄:새 경고 71:0 4:0 3:0 1:0 1:0 11:0 7:0 (b) 0 0 0 0 (c) 0 0 0
            양성 대조 (a) sprint 70:1 (MD031) · README 17:2 (b) 훅 1 (SC2086)
[DG-05]     git 저장소 사본 g-base: validate-plugin · sync-docs ·        g-mock: 같음 · (d) 00 00 00 00
            sync-evals · run-evals · check-stale-values(되살아난 옛 값 없음) · sync-orchestrator · validate-doc-contracts ·
            check-docs-links · check-contrast-claims 전부 종료 코드 0
```

문장 삭제 대조 (러닝북 계약 규칙 — 특정 문장이 있어야 한다는 조건은 그 문장만 지운 사본에서 FAIL 이 나야 한다). 스크래치 `p4d/del.py` 가
모의본에서 조건이 요구하는 문장을 하나씩 지우고 같은 구간에서 다시 센다. 46 문장 전부 1 → 0 이다. 처음 고른 create-agent 토큰
`` `INVALID` 2 건 이상이면 REJECT `` 는 한 줄에 두 번 있어 1 → 1 이 나와 세 토큰으로 쪼갰다:

```text
SK-01 sprint ### Step 5: Commit: 1→0 1→0 1→0 1→0 1→0 1→0 1→0 1→0
SK-02 sprint ### Step 0: Pre-Sprint Sync Check: 1→0 1→0 1→0 1→0 1→0
SK-03 sprint ### Step 3: 빌드/분석 검증: 1→0 1→0 1→0 1→0 1→0 1→0 1→0
SK-04a sprint ### Step 3: 빌드/분석 검증: 1→0 1→0
SK-04b sprint ### Step 4: QA Evaluator: 1→0
SK-04b sprint ### Step 6: Push: 1→0
SK-05a create-agent (파일 전체): 1→0 1→0 1→0
SK-05b create-skill (파일 전체): 1→0 1→0 1→0
SK-06a contract-kaizen ### Step 2: Triage: 1→0 1→0 1→0
SK-06c harness-kaizen ### Step 2a: 1→0
AR-01d plugin-validation-guide.md ### V10 마크다운 표 무결성: 1→0 1→0
AR-01d plugin-validation-guide.md ## 8. 변경 이력: 1→0
AR-03 README.md ## 커밋 안전 훅: 1→0 1→0 1→0 1→0 1→0
AR-04 README.md ## 커밋 안전 훅: 1→0 1→0 1→0 1→0
문장 46 개 · 지운 사본에서 0 이 안 된 것 0
```

그 밖의 대조 (모의본 사본):

- 코드 블록 음성 대조 — SK-01 `-o` 줄을 목록 전체 커밋으로 바꾼 사본 `committed=[M mine.txt A new.txt D other.txt M shared.txt]` · SK-03 `rc=$?` 를
  `echo … exit=$?` 로 합친 사본 네 경우 모두 `0 0 0`. SK-03 블록은 bash 와 zsh 로 실행해도 같다
- 훅 변이 — 경로 커밋 삭제를 공용 목록으로 세는 판은 ⑳ 에서, 개인 목록으로 세는 판은 ⑳ · ㉑ 에서, 희소 체크아웃 빼기 줄을 지운 판은 ㉕ 에서
  떨어진다(셋째는 `align.sh` 에서도 ㉕ 한 줄만 `DISAGREE`). git 실측 근거: `git rm -r --cached d1` 뒤
  `git commit -o d1` 은 「nothing to commit」(삭제 0), 빈 개인 목록 `GIT_INDEX_FILE=<없는 파일> git commit -o a.txt` 는 HEAD 의 나머지 파일을 그대로 둔다(커밋 전후 추적 파일 4 개 → 4 개),
  `git sparse-checkout set --cone keep` 뒤(작업 폴더 `d1` 0 개 · `ls-files -t` 의 `S` 60 개) `git commit -o -m x -- .` 는 삭제 0 개를 싣는다(`align.sh` ㉕)
- ㉕ 전제 대조 — 시험에서 `&& git -C "$r" sparse-checkout set --cone keep` 만 지운 사본은 `FAIL ㉕ 기대 희소 체크아웃 전제 … / 실제 d1/f001 있음 · S 0 개`.
  고친 훅 · 셋째 변이 둘 다 같은 FAIL 이다. 전제 확인 `if` 줄까지 지운 사본에서는 셋째 변이가 `PASS ㉕` — 전제를 안 보면 조용히 통과한다
- ER-03 파일마다 비교 — 다른 파일(`sprint/SKILL.md`)에 이미 있고 근거 파일에는 없는 `https://arxiv.org/abs/2606.27416` 을 create-agent 에 더한 사본에서
  파일마다 비교 1 · 합친 비교 0
- 함수 정의 확인 — 공통 정의 없이 `type my` · `type added` · `type url` · `type unsigned_on` · `type verify_seal` 가드를 붙인 명령은 다섯 모두 종료 코드 2 로 멈춘다.
  가드 없는 `bash -c 'my | grep -c x'` 는 `my: command not found` 뒤 `0` 을 낸다(0 기대 조건이 PASS 로 읽는 값)
- N/A 줄 양성 대조 — SC-00 의 `grep -cE` 에 네 줄 3 · DG-01 의 `grep -c` 에 두 줄 1 · DG-04 의 `grep -cE` 에 세 줄 2
- 백엔드 — 이 기계에 yq 가 없어 가짜 yq 로 셸 쪽 분기를 돌렸다. 모의본 시험 전체를 가짜 yq 로 돌려도 ALL PASSED. CI 는 yq 가 있어 셸 쪽으로 돈다(`harness/scripts/save-feedback.sh:49` 의 2026-08-14 실측 주석)
- 폴더 이름 결함 대조 — 시작 커밋 판의 읽는 자리 `usage_dir / "facets"` 만 `"facets2"` 로 바꾼 사본에서 `validate-doc-contracts.py` 가 종료 코드 0 ·
  `violation 0`. 모의본의 상수를 `"facets2"` 로 바꾼 사본은 종료 코드 1 · `usage_data_inputs` 불일치 1
- YAML 펜스 — 14 킷 마크다운의 `yaml` 펜스 60 개 중 파싱 실패 3 개가 전부 일부러 깨 놓은 예시 · 자리표시자(`GAP 분석` 셋째 선택)
- 커밋 훅 준비 — `git ls-files --pathspec-from-file=list` 는 `error: unknown option` · 종료 코드 129. `GIT_INDEX_FILE=<빈 임시 파일> git read-tree HEAD` 는 종료 코드 0

예행 (2026-09-25 03:5x, 검토 반영 뒤 계약 본문 그대로): 작업 폴더를 스크래치에 복제(`p4d/rehearse.sh` → `p4d/rh`)해 BUILD 를 흉내 냈다 — 이 계약을 봉인해 계약만
커밋(`seal commit files=1`) · 모의본 열네 파일을 `git add -- … && git commit -o -- …` 로 커밋 · 서명 없는 다른 Phase 커밋(`.harness/` 한 파일, 본문에
서명 글자를 인용만) · `end_sha` 커밋 · 스물다섯 문자열 가짜 notes 커밋 · 그 sha 를 적은 `end_sha` 커밋. `p4d/meas-full.sh` 가 28 조건을 돌린 값이 전부
요구값이다 — 위 모의본 열과 같고, git 기록 조건은 `my` 가 열네 파일 · 계약 · 개정 · notes 열일곱 줄(다른 Phase 커밋의 파일은 빠짐), SC-00 0 ·
DG-01 0 · DG-04 0, ER-05 notes 있음 · 25 값 전부 1 · 셋째 0 · 넷째 0, AR-05 ① 0(`harness` · `scripts` 전체) · ② 0 · 14 · ③ `SEAL_ABSENT 10 · SEAL_OK 54` · 이 Phase 몫 0 · 이 계약
`SEAL_OK`, DG-05 전제 0 · (a) 10 · 0 (b) 0 (전체 FAIL 0) (c) `0 0 0 0` · check-stale-values 0 · 0, DG-06 `scope-isolation` PASS (6 commits · 13 kits) ·
`doc-contracts` PASS · `docs-site-regen` FAIL(Final 몫 — 판정에서 뺀 줄) · 합계 `15 checks — 12 PASS / 1 FAIL / 0 ERROR / 2 SKIP`.
음성 대조(`p4d/neg-v2.sh`, 커밋마다 `end_sha` 를 그 뒤로 옮긴다): 예행 사본 `rh2` 에 서명 없이 `harness/hooks/hooks.json` 을 고친 커밋 → AR-05 ① 1 ·
열네 파일만 보던 옛 ① 0 · ② 0. 이어 서명 없이 루트 `README.md` 를 고친 커밋 → ER-05 넷째 1 · 셋째 0. 이어 서명 없이 `harness/README.md` → ① 2 · 옛 ① 1.
따로 `rh4` 에 `Kaizen-Phase: kaizen-0924-p05-flutter` 서명을 단 루트 `README.md` 커밋 → 넷째 0 · ① 0. 가짜 notes 에서 스물다섯 문자열을 하나씩 지운
사본 스물다섯 개는 모두 지운 문자열의 값만 0.

## Skill

- [ ] SK-01: `/sprint` Step 5 가 내 경로만 싣게 가르치고, 그 코드 블록이 남이 공용 목록에 올려 둔 변경을 싣지 않는다 (harness:P07 · user-setup:P2 · F08) — (a) `harness/skills/sprint/SKILL.md` 의 `### Step 5: Commit` 구간에 8 토큰 `**내 경로만 싣는다 (2026-09-25 추가).**` · `git commit -o -m "<메시지>" -- <내 경로…>` · `git show --name-status --format= HEAD` · `` `git add -A` · `git add .` · `git commit -a` · `git commit -i` 를 쓰지 않는다 `` · `확인은 파일 수가 아니라 경로 집합으로 한다` · `git diff HEAD -- <내 경로…>` · `지정한 경로 안의 삭제가 50 개를 넘으면 막는다` · `다른 세션의 커밋 두 개를 되돌렸다` 가 각각 1 건 (b) `회귀 게이트` 절 `ka-commit.sh` 를 `$END` 판 SKILL.md 에 돌린 출력이 두 줄 `committed=[M mine.txt A new.txt]` · `still_staged=[D other.txt M shared.txt]` 다 [exact, enumerated]
      (측정: (a) ``toks "$(sect "$SP" '### Step 5: Commit')" '**내 경로만 싣는다 (2026-09-25 추가).**' 'git commit -o -m "<메시지>" -- <내 경로…>' 'git show --name-status --format= HEAD' '`git add -A` · `git add .` · `git commit -a` · `git commit -i` 를 쓰지 않는다' '확인은 파일 수가 아니라 경로 집합으로 한다' 'git diff HEAD -- <내 경로…>' '지정한 경로 안의 삭제가 50 개를 넘으면 막는다' '다른 세션의 커밋 두 개를 되돌렸다'`` 8 값 전부 1
       (b) `bash "$K/ka-commit.sh" "$SP"` 의 두 줄이 위 값.
       봉인 전 실측: 편집 전 (a) 전부 0 (b) `NO_BLOCK`. 모의본 (a) 전부 1 (b) 요구값. 음성 대조: 블록의 `git commit -o …` 줄을 `git add -- <내 경로…>; git commit -m "<메시지>"` 로 바꾼 사본은 `committed=[M mine.txt A new.txt D other.txt M shared.txt]` · `still_staged=[]`. 문장 삭제 대조: `회귀 게이트` 절 표)
- [ ] SK-02: `/sprint` Step 0 이 병렬 흔적이 있고 커밋이 둘 이상이면 워크트리를 따로 만들게 한다 (F09 · F28 · user-setup:P2) — `### Step 0: Pre-Sprint Sync Check` 구간에 5 토큰 `**병렬 흔적이 있고 커밋이 둘 이상 예상되면 워크트리를 따로 만든다 (2026-09-25 추가).**` · `git worktree add -b <가지> <새 폴더> <검사 통과를 확인한 커밋>` · `로 가지만 바꾸면 남의 미커밋 변경이 새 가지로 따라오고` · `` `isolation: worktree` 는 부모 `` · `sprint-contract Step 6.7 의 가지 만들기는 이 워크트리 안에서 한다` 가 각각 1 건 [exact, enumerated]
      (측정: ``toks "$(sect "$SP" '### Step 0: Pre-Sprint Sync Check')" '**병렬 흔적이 있고 커밋이 둘 이상 예상되면 워크트리를 따로 만든다 (2026-09-25 추가).**' 'git worktree add -b <가지> <새 폴더> <검사 통과를 확인한 커밋>' '로 가지만 바꾸면 남의 미커밋 변경이 새 가지로 따라오고' '`isolation: worktree` 는 부모' 'sprint-contract Step 6.7 의 가지 만들기는 이 워크트리 안에서 한다'`` 5 값 전부 1.
       봉인 전 실측: 편집 전 전부 0, 모의본 전부 1. 문장 삭제 대조: `회귀 게이트` 절 표)
- [ ] SK-03: `/sprint` Step 3 이 빨간 검사의 원인을 셋으로 가르는 규칙 하나를 두고, 그 코드 블록이 답을 아는 네 경우에서 맞는 종료 코드를 낸다 (F09 · harness:P07 기준 커밋 비교 — backend-family:P3 · backend-family:P4 와 하나로 정할 규칙) — (a) `### Step 3: 빌드/분석 검증` 구간에 7 토큰 `**검사가 빨가면 고치기 전에 원인을 셋으로 가른다 (2026-09-25 추가)**` · `FORK_BASE=$(git merge-base HEAD origin/<기준 가지>)` · `| 실패 | 통과 | — | 미커밋 변경 탓` · `| 실패 | 실패 | 실패 | 기준 커밋에서 이미 실패` · `| 실패 | 실패 | 통과 | 이번 커밋 탓일 가능성이 크다 |` · `분기점이지 기준 가지의 지금 상태가 아니다` · `준비 명령을 붙인다` 가 각각 1 건 (b) `ka-split.sh` 를 `$END` 판 SKILL.md 에 떼어 낸 블록을 bash 로 돌린 판과 `RUNNER=zsh` 로 돌린 판의 출력이 둘 다 네 줄 `S1 shared=1 head/fork/base=1 1 1 worktrees=1` · `S2 shared=1 head/fork/base=1 0 0 worktrees=1` · `S3 shared=1 head/fork/base=0 0 0 worktrees=1` · `S4 shared=0 head/fork/base=0 0 1 worktrees=1` 이다 [exact, enumerated]
      (측정: (a) `toks "$(sect "$SP" '### Step 3: 빌드/분석 검증')" '**검사가 빨가면 고치기 전에 원인을 셋으로 가른다 (2026-09-25 추가)**' 'FORK_BASE=$(git merge-base HEAD origin/<기준 가지>)' '| 실패 | 통과 | — | 미커밋 변경 탓' '| 실패 | 실패 | 실패 | 기준 커밋에서 이미 실패' '| 실패 | 실패 | 통과 | 이번 커밋 탓일 가능성이 크다 |' '분기점이지 기준 가지의 지금 상태가 아니다' '준비 명령을 붙인다'` 7 값 전부 1
       (b) `bash "$K/ka-split.sh" "$SP"` 와 `RUNNER=zsh bash "$K/ka-split.sh" "$SP"` 가 둘 다 위 네 줄.
       봉인 전 실측: 편집 전 (a) 전부 0 (b) `NO_BLOCK` · 종료 코드 2. 모의본 (a) 전부 1 (b) 두 판 모두 요구값 · 임시 워크트리가 남지 않는다(`worktrees=1`). 음성 대조: 블록의 `rc=$?` 두 줄을 `echo "$ref $(git rev-parse --short "$ref") exit=$?"` 한 줄로 합친 사본은 네 경우 모두 `head/fork/base=0 0 0` — 종료 코드 대신 `rev-parse` 의 0 을 읽는 결함을 잡는다. 문장 삭제 대조: `회귀 게이트` 절 표)
- [ ] SK-04: `/sprint` 의 검증 불가 표기와 끝 줄이 새 규약과 같은 말을 쓴다 (harness:P09 비고 「sprint/SKILL.md 3 단계 부분은 Phase 4 와 맞춘다」 · harness:P06 의 `/sprint` 쪽 — Phase 2 넘김) — (a) Step 3 구간에 `` `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채운다 `` 1 · `미검증이 2 건 이상이면 완료가 아니라 부분 완료로 보고한다` 1, 파일 전체에 `` `[미검증]` + 사유 한 줄 `` 0 (b) `### Step 4: QA Evaluator` 구간에 `사용자가 할 일: 없음 | <한 줄>` 1 · `### Step 6: Push` 구간에 `` 보고 끝은 `사용자가 할 일: 없음` 또는 `사용자가 할 일: <한 줄>` 로 맺는다 `` 1 (c) 맞춘 원문이 `$END` 판에 그대로 있다 — `harness/skills/sprint-contract/SKILL.md` 에 `` `사용자가 할 일: 없음` `` · `` `사용자가 할 일: <한 줄>` `` 각 1 건 이상, `harness/docs/guides/skill-design-guide.md` 에 `막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령` 1 건 이상 [exact, enumerated]
      (측정: (a) ``toks "$(sect "$SP" '### Step 3: 빌드/분석 검증')" '`[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채운다' '미검증이 2 건 이상이면 완료가 아니라 부분 완료로 보고한다'`` 1 · 1 · ``grep -cF '`[미검증]` + 사유 한 줄' "$SP"`` 0
       (b) `toks "$(sect "$SP" '### Step 4: QA Evaluator')" '사용자가 할 일: 없음 | <한 줄>'` 1 · ``toks "$(sect "$SP" '### Step 6: Push')" '보고 끝은 `사용자가 할 일: 없음` 또는 `사용자가 할 일: <한 줄>` 로 맺는다'`` 1
       (c) ``toks "$(cat "$T/E/harness/skills/sprint-contract/SKILL.md")" '`사용자가 할 일: 없음`' '`사용자가 할 일: <한 줄>`'`` 두 값 1 이상 · `grep -cF '막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령' "$T/E/harness/docs/guides/skill-design-guide.md"` 1 이상.
       봉인 전 실측: 편집 전 (a) 0 · 0 · 1 (b) 0 · 0 (c) 1 · 1 · 1 — 옛 문구가 편집 전 1 이라 측정이 살아 있다. 모의본 (a) 1 · 1 · 0 (b) 1 · 1 (c) 1 · 1 · 1. 문장 삭제 대조: `회귀 게이트` 절 표)
- [ ] SK-05: create-agent · create-skill 의 낡은 사실을 설계 가이드 · 근거 파일에 맞춘다 (Phase 1 넘김 — `phase1-notes.md` §넘기는 것 둘째 · 셋째 줄 · 근거 파일 §3 `create-skill/SKILL.md:29`) — (a) `harness/skills/create-agent/SKILL.md` 에 `15 종` 0 · `18 종` 3 · `2건 이상 자동 REJECT` 0 · `` **`INVALID` 2 건 이상이면 REJECT** 규칙 `` 1 · `` (2) `ENV` 는 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)이 있어야 성립하고 `` 1 · `(3) 조용한 PASS 금지` 1 · `fit-pal` 0 · `agents 에 대해` 0 이고, `공식 subagent frontmatter 는 N 종` 의 N 이 `$END` 판 `agent-design-guide.md` 의 `공식 frontmatter 는 **N 종**` 과 같다 (b) `harness/skills/create-skill/SKILL.md` 에 `1500-2000 words` 0 · `2000 words` 0 · `SKILL.md 본문은 500 줄 미만을 권고한다` 1 · `500 줄 권고를 넘겨` 1 · `argument-hint 누락은 discovery 실패` 0 이고, `` `argument-hint` 는 자동 완성에 뜨는 인자 힌트다 `` 가 든 줄 1 개가 `https://code.claude.com/docs/en/skills` 를 담으며, 인용한 절 `### SKILL.md 본문 500 라인 미만 권고` 가 `$END` 판 `skill-design-guide.md` 에 1 개다 [exact, enumerated]
      (측정: (a) `CA=$T/E/harness/skills/create-agent/SKILL.md` 뒤 ``toks "$(cat "$CA")" '15 종' '18 종' '2건 이상 자동 REJECT' '**`INVALID` 2 건 이상이면 REJECT** 규칙' '(2) `ENV` 는 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)이 있어야 성립하고' '(3) 조용한 PASS 금지' 'fit-pal' 'agents 에 대해'`` 이 `0 3 0 1 1 1 0 0` · `grep -oE '공식 subagent frontmatter 는 [0-9]+ 종' "$CA" | grep -oE '[0-9]+'` 와 `grep -oE '공식 frontmatter 는 \*\*[0-9]+ 종' "$T/E/harness/docs/guides/agent-design-guide.md" | grep -oE '[0-9]+'` 이 같은 한 값
       (b) `CS=$T/E/harness/skills/create-skill/SKILL.md` 뒤 `toks "$(cat "$CS")" '1500-2000 words' '2000 words' 'SKILL.md 본문은 500 줄 미만을 권고한다' '500 줄 권고를 넘겨' 'argument-hint 누락은 discovery 실패'` 이 `0 0 1 1 0` · ``grep -F '`argument-hint` 는 자동 완성에 뜨는 인자 힌트다' "$CS" | grep -cF 'https://code.claude.com/docs/en/skills'`` 1 · `grep -cE '^### SKILL\.md 본문 500 라인 미만 권고' "$T/E/harness/docs/guides/skill-design-guide.md"` 1.
       봉인 전 실측: 편집 전 (a) `3 0 1 0 0 0 1 1` · N 15 대 가이드 18 (b) `1 2 0 0 1` · 0 · 1. 모의본 (a) `0 3 0 1 1 1 0 0` · 18 대 18 (b) `0 0 1 1 0` · 1 · 1. 문장 삭제 대조: `회귀 게이트` 절 표 — 처음 고른 토큰 `` `INVALID` 2 건 이상이면 REJECT `` 는 한 줄에 두 번 있어 한 곳을 지워도 1 이 남았다. 그래서 세 토큰으로 쪼갰다)
- [ ] SK-06: 카이젠 두 스킬이 옛 문구로 적힌 체크리스트 12 항목을 반복 실패로 세지 않는다 (Phase 2 넘김 — `phase2-notes.md` §Phase 4 가 읽을 것 넷째 줄 · 카이젠 Step 2a 실측) — (a) `harness/skills/contract-kaizen/SKILL.md` 의 `### Step 2: Triage` 구간에 `**옛 문구로 적힌 12 항목은 세지 않는다 (2026-09-25 추가).**` 1 · `` `measure_premise_unrun` 이 체크리스트에 있는 파일에서만 `` 1 · `날짜로 가르지 마라` 1 (b) 그 불릿의 항목 이름이 12 개이고, 문구를 바꾼 커밋 `3e3ff04` 에서 sprint-contract 의 지운 체크리스트 줄 이름 집합과 정확히 같다 (c) `harness/skills/harness-kaizen/SKILL.md` 의 `### Step 2a` 구간에 `` contract-kaizen Step 2 의 규칙대로 `measure_premise_unrun` 키가 있는 파일에서만 센다 `` 1 [exact, enumerated]
      (측정: (a) `S2=$(sect "$T/E/harness/skills/contract-kaizen/SKILL.md" '### Step 2: Triage')` 뒤 ``toks "$S2" '**옛 문구로 적힌 12 항목은 세지 않는다 (2026-09-25 추가).**' '`measure_premise_unrun` 이 체크리스트에 있는 파일에서만' '날짜로 가르지 마라'`` 세 값 1
       (b) ``git show 3e3ff04 -- harness/skills/sprint-contract/SKILL.md | grep -E '^-   - `' | sed -E 's/^-   - `([a-z_]+)`.*/\1/' | sort -u > "$T/k12"`` · ``printf '%s\n' "$S2" | grep -F '**옛 문구로 적힌 12 항목은 세지 않는다' | grep -oE '`[a-z_]+`' | tr -d '`' | grep -vx measure_premise_unrun | sort -u > "$T/c12"`` 뒤 `grep -c . "$T/k12"` 12 · `grep -c . "$T/c12"` 12 · `comm -3 "$T/k12" "$T/c12" | grep -c .` 0
       (c) ``toks "$(sect "$T/E/harness/skills/harness-kaizen/SKILL.md" '### Step 2a')" 'contract-kaizen Step 2 의 규칙대로 `measure_premise_unrun` 키가 있는 파일에서만 센다'`` 1.
       봉인 전 실측: 편집 전 (a) 0 · 0 · 0 (b) 12 · 0 · 12 (c) 0. 모의본 (a) 1 · 1 · 1 (b) 12 · 12 · 0 (c) 1. 알려진 답: `3e3ff04` 의 지운 줄은 손으로 센 12 항목(`phase2-notes.md` 넷째 줄 목록)과 같다. 규칙을 최근 계약 피드백 10 건에 적용하면 임계를 넘은 항목이 `nfr_coverage` 6 에서 0 으로 준다 — `배경` 절)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 훅 · 검사 스크립트의 동작은 Error · Architecture 조건이 잰다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `scripts/release.sh` · `.claude-plugin/marketplace.json` · `harness/.claude-plugin/plugin.json` · `harness/README.md` 네 줄을 넣으면 3)

## Error

- [ ] ER-01: 커밋 안전 훅이 경로 지정 커밋(`-o <경로>` · `-- <경로>` · `-i <경로>`)에서 커밋이 실제로 실을 삭제를 세어 50 개를 넘으면 막고, 경로 밖 삭제 · 목록에서만 뺀 파일 · 빈 개인 목록 · 희소 체크아웃에서 꺼내지 않은 파일(skip-worktree)은 세지 않는다 (러닝북 Phase 4 과제 (1) · F08 · F28) — (a) `$END` 판 폴더에서 `harness/evals/hooks/commit-guard-test.sh` 를 bash 와 `/bin/bash`(3.2) 로 각각 돌리면 둘 다 마지막 줄이 `실패 0 건` · 종료 코드 0 이고, `PASS ` 로 시작하는 새 경우 줄이 10 개(⑰ · ⑰-확인 · ⑱ · ⑲ · ⑳ · ㉑ · ㉒ · ㉓ · ㉔ · ㉕)다 (b) 음성 대조 다섯 — 같은 시험을 시작 커밋 판 훅으로 돌리면 FAIL 번호가 정확히 `⑰ ⑰-확인 ⑱ ㉒ ㉓ ㉔` 이고, `mut.py` 가 `$END` 판 훅에서 만든 세 변이(경로 커밋의 삭제를 공용 목록 · 개인 목록으로 세는 판, 희소 체크아웃 빼기 줄을 지운 판)는 각각 `⑳` · `⑳ ㉑` · `㉕` 이며, 시험에서 `sparse-checkout set` 한 곳만 지운 사본은 ㉕ 를 `FAIL` 로 적는다 — 희소 체크아웃이 안 걸리면 훅을 안 고쳐도 통과하는 경우를 시험이 스스로 잡는다 (c) 알려진 답 — `align.sh` 를 `$END` 판 훅에 돌린 열한 줄이 전부 `agree` 이고 `git_dels` 가 차례로 `60 51 50 0 0 55 59 60 0 0 0` 이다 (git 이 같은 명령으로 실제 커밋해 센 삭제 수) [exact, enumerated]
      (측정: (a) `(cd "$T/E" && bash harness/evals/hooks/commit-guard-test.sh > "$T/cg5.txt" 2>&1; echo "rc=$?")` · `(cd "$T/E" && /bin/bash harness/evals/hooks/commit-guard-test.sh > "$T/cg3.txt" 2>&1; echo "rc=$?")` 둘 다 `rc=0` · `tail -1 "$T/cg5.txt"` 와 `tail -1 "$T/cg3.txt"` 둘 다 `실패 0 건` · `grep -cE '^PASS (⑰|⑰-확인|⑱|⑲|⑳|㉑|㉒|㉓|㉔|㉕) ' "$T/cg5.txt"` 10
       (b) `(cd "$T/E" && COMMIT_GUARD_HOOK="$T/B/harness/scripts/commit-guard.sh" bash harness/evals/hooks/commit-guard-test.sh 2>&1 | labels)` 이 `⑰ ⑰-확인 ⑱ ㉒ ㉓ ㉔ ` · `mkdir -p "$T/mut" && python3 "$K/mut.py" "$T/E/harness/scripts/commit-guard.sh" "$T/mut"` 이 `mutants ok` 뒤 `(cd "$T/E" && COMMIT_GUARD_HOOK="$T/mut/mut-shared.sh" bash harness/evals/hooks/commit-guard-test.sh 2>&1 | labels)` 이 `⑳ ` · 같은 명령에 `mut-private.sh` 가 `⑳ ㉑ ` · `mut-nosparse.sh` 가 `㉕ ` ·
       `sed 's/ && git -C "$r" sparse-checkout set --cone keep$//' "$T/E/harness/evals/hooks/commit-guard-test.sh" > "$T/E/harness/evals/hooks/nosp-test.sh"` 뒤 `diff "$T/E/harness/evals/hooks/commit-guard-test.sh" "$T/E/harness/evals/hooks/nosp-test.sh" | grep -c '^<'` 1 · `(cd "$T/E" && bash harness/evals/hooks/nosp-test.sh 2>&1) | grep -c '^FAIL ㉕ '` 1 · 끝나면 `rm -f "$T/E/harness/evals/hooks/nosp-test.sh"`
       (c) `bash "$K/align.sh" "$T/E/harness/scripts/commit-guard.sh" > "$T/align.txt"` 뒤 `grep -c ' agree$' "$T/align.txt"` 11 · `sed -E 's/.*git_dels=([0-9]+).*/\1/' "$T/align.txt" | tr '\n' ' '` 이 `60 51 50 0 0 55 59 60 0 0 0 `.
       봉인 전 실측: 편집 전 판 — 시험 bash · 3.2 둘 다 `실패 0 건`(새 경우 없음), `align.sh` 열한 줄 가운데 ⑰ ⑱ ㉒ ㉓ ㉔ 다섯 줄이 `DISAGREE`(㉕ 는 편집 전 훅이 경로 커밋을 통째로 건너뛰어 agree). 모의본 (a) bash 5.3.9 · 3.2.57 둘 다 `실패 0 건` · 새 PASS 10 (b) `⑰ ⑰-확인 ⑱ ㉒ ㉓ ㉔ ` · `⑳ ` · `⑳ ㉑ ` · `㉕ ` · 지운 사본 차이 1 줄 · `FAIL ㉕ 기대 희소 체크아웃 전제 … / 실제 d1/f001 있음 · S 0 개` 1 줄 (c) 11 · `60 51 50 0 0 55 59 60 0 0 0 `. 셋째 변이를 `align.sh` 에 돌리면 ㉕ 한 줄만 `DISAGREE`. 검토가 찾은 결함 대조: 희소 체크아웃 빼기 줄이 없던 첫 모의본은 `git commit -o -m x -- .` · `-- d1 keep` 을 둘 다 막았고(`hook_rc=2`) git 이 실제로 실은 삭제는 0 이었다 — 셋째 변이가 그 판이다)
- [ ] ER-02: 피드백 저장 스크립트가 초안에 `project_hash` · `project_name` 을 요구하지 않고, 최종본에는 두 필드를 여전히 요구하며, 두 검사 백엔드가 같은 문구로 실패한다 (harness:P02 · F14) — (a) `$END` 판 폴더에서 `HOME` 을 임시 폴더로 바꿔 `harness/evals/kaizen/feedback-system/save-test.sh` 를 돌리면 `=== ALL TESTS PASSED ===` 이고 `PASS: identity 없는 초안 저장` · `PASS: draft missing timestamp only` 가 각각 1 줄, 임시 HOME 에 남은 파일 0 (b) 음성 대조 — 시작 커밋 판 스크립트에 `$END` 판 시험을 돌리면 `FAIL: identity 없는 초안이 거부됐다` 1 줄 · 종료 코드 0 아님 (c) `parity.sh` 를 `$END` 판에 돌린 여섯 줄에서 같은 초안의 python · yq 두 줄이 같은 FAIL 문구를 내고 그 문구가 차례로 `FAIL: 누락 필드: ['timestamp']` · `FAIL: 누락 필드: ['timestamp']` · `FAIL: 누락 필드: ['timestamp', 'outcome']`, 마지막 줄 `saved_under_home=0` (d) 최종본 검사가 두 필드를 요구한다 — `final8.sh` 를 `$END` 판에 돌리면 `project_name 1` · `project_hash 1` 뒤 `rc=1 1 1 saved_under_home=0` [exact, enumerated]
      (측정: (a) `(cd "$T/E" && HOME=$H bash harness/evals/kaizen/feedback-system/save-test.sh > "$T/st.txt" 2>&1)` 뒤 `toks "$(cat "$T/st.txt")" '=== ALL TESTS PASSED ===' 'PASS: identity 없는 초안 저장' 'PASS: draft missing timestamp only'` 이 `1 1 1` · `find "$H" -type f | grep -c .` 0
       (b) `mkdir -p "$T/neg/harness/scripts" "$T/neg/harness/evals/kaizen/feedback-system" && cp "$T/B"/harness/scripts/*.sh "$T/neg/harness/scripts/" && cp "$T/E/harness/evals/kaizen/feedback-system/save-test.sh" "$T/neg/harness/evals/kaizen/feedback-system/"` 뒤 `(cd "$T/neg" && HOME=$H bash harness/evals/kaizen/feedback-system/save-test.sh > "$T/sn.txt" 2>&1; echo "rc=$?")` 이 `rc=1` · `grep -c '^FAIL: identity 없는 초안이 거부됐다' "$T/sn.txt"` 1
       (c) `bash "$K/parity.sh" "$T/E" > "$T/par.txt"` 뒤 `sed -nE 's/^(python|yq) drop=[^ ]+ rc=1 //p' "$T/par.txt" | paste - - | awk -F'\t' '$1==$2{print $1}'` 이 위 세 줄(python · yq 두 줄의 문구가 다르면 그 쌍이 빠져 줄이 모자란다) · `tail -1 "$T/par.txt"` 이 `saved_under_home=0`
       (d) `bash "$K/final8.sh" "$T/E" | tr '\n' ' '` 이 `project_name 1 project_hash 1 rc=1 1 1 saved_under_home=0 `.
       봉인 전 실측: 편집 전 (a) `PASS` 세 줄 뒤 ALL PASSED(새 경우 없음) (c) 두 필드 없는 초안에 `['timestamp', 'project_hash', 'project_name']` — 두 백엔드 모두 (d) 같은 값. 모의본 (a) `1 1 1` · 0 (b) `rc=1` · 1 (c) 요구값 (d) 요구값. 가짜 yq 로 시험 전체를 돌려도 모의본 ALL PASSED)
- [ ] ER-03: 열네 파일에 새로 생긴 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase4.md` 에 있다 — 파일마다 편집 전 판과 비교한다 [exact, enumerated]
      (측정: `type url >/dev/null || exit 2;` 뒤 `for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$T/E/$f"); done | sort -u | comm -23 - <(url < "$EVID") | grep -c .` 0.
       파일마다 비교하는 이유: 열네 파일을 합쳐 비교하면 다른 파일에 이미 있던 URL 을 새로 더한 경우를 못 본다(검토 실측 — 합친 비교는 `create-skill/SKILL.md` 에 새로 생긴 `https://code.claude.com/docs/en/skills` 를 못 봤다).
       봉인 전 실측: 모의본의 새 (파일, URL) 쌍 다섯(`sprint/SKILL.md` 넷 `git-scm.com/docs/git-commit` · `…/git-merge-base` · `…/git-worktree` · `code.claude.com/docs/en/sub-agents`, `create-skill/SKILL.md` 의 `code.claude.com/docs/en/skills`)이 전부 근거 파일에 있어 0. 양성 대조: 모의본 README 끝에 `https://example.invalid/x` 를 더하면 1)
- [ ] ER-04: 열네 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이다 [exact]
      (측정: `type added >/dev/null || exit 2;` 뒤 `added | grep -cE "$K02"` 0. 양성 대조: 고치는 create-agent `:25` 줄의 옛 문구 「V1 이 agents 에 대해」 를 남긴 첫 모의본이 1 — 그래서 그 줄을 고쳤다. 봉인 전 실측 UTF-8 1 → 고친 뒤 0)
- [ ] ER-05: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase4-notes.md` 에 스물다섯 문자열(처리 배정표 키 열 `F08` · `F09` · `F14` · `F18` · `F28` · `harness:P02` · `harness:P07` · `user-setup:P2` · `other-kits:P10` · `insights:scope-commit-block` 과 넘김 열다섯 `sprint-contract Step 9` · `feedback-schema.yaml` · `# sprint-scope` · `assertions.json 실행기` · `agent-design-guide.md:79` · `sprint-contract Step 6.7 (a)` · `backend-family:P3` · `backend-family:P4` · `flutter-preflight` · `react-preflight` · `F20` · `V6 범위` · `reflect-collector:P5` · `create-agent/SKILL.md:25` · `create-skill/SKILL.md:27`)이 각각 1 회 이상 있고, 이 Phase 커밋이 다른 Phase 소관 파일 · 러닝북이 금지한 공유 파일을 하나도 건드리지 않는다. 서명 줄 커밋 목록으로 재고, 서명을 빠뜨린 커밋도 보이게 금지 경로를 건드린 구간 안 커밋을 직접 센다 [exact, enumerated]
      (Given: BUILD 가 notes 를 쓰고 커밋한 뒤 · 측정: `git cat-file -e "$END:$NOTES"` exit 0 ·
       `for t in 'F08' 'F09' 'F14' 'F18' 'F28' 'harness:P02' 'harness:P07' 'user-setup:P2' 'other-kits:P10' 'insights:scope-commit-block' 'sprint-contract Step 9' 'feedback-schema.yaml' '# sprint-scope' 'assertions.json 실행기' 'agent-design-guide.md:79' 'sprint-contract Step 6.7 (a)' 'backend-family:P3' 'backend-family:P4' 'flutter-preflight' 'react-preflight' 'F20' 'V6 범위' 'reflect-collector:P5' 'create-agent/SKILL.md:25' 'create-skill/SKILL.md:27'; do printf '%s ' "$(git show "$END:$NOTES" | grep -cF -- "$t")"; done` 25 값 전부 1 이상 ·
       셋째 — `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(harness/skills/sprint-contract/|harness/agents/qa-evaluator\.md$|harness/docs/guides/(skill|agent|contract)-design-guide\.md$|harness/docs/guides/qa-evaluation-guide\.md$|harness/references/|\.claude-plugin/|[^/]+/\.claude-plugin/plugin\.json$|README\.md$|CLAUDE\.md$|docs/|\.claude/|\.github/|\.harness/\.meta/(orchestrator-audit-log\.md|kaizen-failure-count\.yaml)$)'` 0 ·
       넷째(직접 세기) — `git log --format=%H "$B..$END" -- harness/skills/sprint-contract harness/agents/qa-evaluator.md harness/docs/guides/skill-design-guide.md harness/docs/guides/agent-design-guide.md harness/docs/guides/contract-design-guide.md harness/docs/guides/qa-evaluation-guide.md harness/references .claude-plugin README.md CLAUDE.md .github .claude .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml | while read -r c; do git log -1 --format=%B "$c" | grep -qE '^Kaizen-Phase: kaizen-0924-p(0[1-35-9]|[1-9][0-9])-' || echo "$c"; done | grep -c .` 0.
       다른 Phase 서명 줄이 달린 커밋은 그 Phase 몫이라 뺀다 — 여러 Phase 가 같은 가지에 동시에 커밋한다. `docs/` 와 킷마다의 `plugin.json` 은 다른 Phase 가 제 킷 폴더를 고치며 건드릴 수 있어 넷째에서 빼고 셋째로만 잰다.
       봉인 전 실측: notes 없음 — 구현이 만들 파일이라 면제. 스물다섯 문자열을 한 줄에 하나씩 담은 가짜 notes 로 예행하면 25 값 전부 1, 한 줄씩 지운 사본에서 그 값만 0(`F20` 사본은 `F20` 만 — 다른 키에 `F20` 이 든 글자가 없다). 셋째 측정은 가짜 목록 한 줄씩 `harness/skills/sprint-contract/SKILL.md` · `harness/references/feedback-schema.yaml` · `README.md` · `.github/workflows/ci.yml` · `.harness/.meta/orchestrator-audit-log.md` 각각 1, 이 Phase 파일 열넷 · 계약 · 개정 · notes · 검토 목록은 0. 넷째는 예행 0 · 예행 사본에 서명 없이 루트 `README.md` 를 고친 커밋을 얹으면 1 · 같은 커밋에 다른 Phase 서명 줄(`Kaizen-Phase: kaizen-0924-p05-flutter`)을 달면 0 — 서명 없는 쪽 사본에서 셋째는 0 이라 넷째만 잡는다. 공통 정의 없이 셋째를 돌리면 `type my` 에서 종료 코드 2 로 멈춘다(없으면 `my: command not found` 뒤 조용히 `0`)

## Architecture

- [ ] AR-01: V10 이 스킬 폴더 안 `references/` 문서까지 재고, V6 범위는 그대로이며, 검증 가이드가 그 범위를 적는다 (other-kits:P10 · F18 표 부분) — (a) `$END` 판 폴더에서 `scripts/validate-plugin.py --check=table-integrity` 가 OK 로 보고한 킷마다 V10 파일 수가 `find` 로 따로 센 여섯 범위(`skills/*/SKILL.md` · `agents/*.md` · `references/*.md` · `docs/**/*.md` · `skills/*/references/**/*.md` · `README.md`) 합집합 수와 같고, 스킬 폴더 안 references 문서가 1 개 이상인 킷이 V10 OK 킷 가운데 1 개 이상이다. V10 이 FAIL 인 킷은 FAIL 줄의 파일이 이 Phase 파일이 아니어야 한다(다른 Phase 몫 — 파일 이름을 근거에 적는다) (b) 양성 대조 — `v10pos.sh` 를 `$END` 판에 돌리면 `FAIL api-kit/skills/api-verify/references/zz-broken-table.md:9` 로 시작하는 줄 1 개 · `rc=2` (c) V6 — `$END` 판 폴더에서 `--check=code-fence` 출력에 `/skills/[^/]+/references/` 를 가리키는 `FAIL` 줄 0 (d) `harness/docs/guides/plugin-validation-guide.md` 머리 설정이 `version: 1.4.0` 이고 `last_updated:` 값이 `$END` 까지 이 파일을 마지막으로 고친 커밋의 날짜(`%cs`)와 같으며, `### V10 마크다운 표 무결성` 구간에 `` `skills/*/references/**/*.md` 도 더한다 `` 1 · `V6 는 같은` 1, `## 8. 변경 이력` 구간에 `| 1.4.0 |` 1 [exact, enumerated]
      (측정: (a) `(cd "$T/E" && python3 scripts/validate-plugin.py --check=table-integrity > "$T/v10.txt" 2>&1)` 뒤
       ``awk '/^=== /{k=$2} /^  V10 /{print k, $3, $0 ~ / OK$/ ? "OK" : "FAIL"}' "$T/v10.txt" > "$T/v10k.txt"`` ·
       ``while read -r k n st; do [ "$st" = OK ] || continue; m=$( (cd "$T/E" && { find "$k/skills" -mindepth 2 -maxdepth 2 -name SKILL.md; find "$k/agents" -maxdepth 1 -name '*.md'; find "$k/references" -maxdepth 1 -name '*.md'; find "$k/docs" -name '*.md'; find "$k/skills" -path "$k/skills/*/references/*" -name '*.md'; [ -f "$k/README.md" ] && echo "$k/README.md"; } 2>/dev/null) | sort -u | grep -c .); r=$( (cd "$T/E" && find "$k/skills" -path "$k/skills/*/references/*" -name '*.md' 2>/dev/null) | grep -c .); echo "$k $n $m $r"; done < "$T/v10k.txt" > "$T/v10m.txt"`` 뒤 `awk '$2!=$3' "$T/v10m.txt" | grep -c .` 0 · `awk '$4>0' "$T/v10m.txt" | grep -c .` 1 이상 · `grep -c ' FAIL$' "$T/v10k.txt"` 이 0 이 아니면 `grep -E '^ +FAIL ' "$T/v10.txt" | grep -cE "$FRE"` 0
       (b) `bash "$K/v10pos.sh" "$T/E"` 에서 `grep -c '^ *FAIL api-kit/skills/api-verify/references/zz-broken-table.md:9 '` 1 · `rc=2` 줄 1
       (c) `(cd "$T/E" && python3 scripts/validate-plugin.py --check=code-fence 2>&1) | grep -E '^ +FAIL ' | grep -cE '/skills/[^/]+/references/'` 0
       (d) `head -6 "$T/E/harness/docs/guides/plugin-validation-guide.md" | grep -cx 'version: 1.4.0'` 1 · `sed -n 's/^last_updated: //p' "$T/E/harness/docs/guides/plugin-validation-guide.md" | head -1` 과 `git log -1 --format=%cs "$END" -- harness/docs/guides/plugin-validation-guide.md` 이 같다 · ``toks "$(sect "$T/E/harness/docs/guides/plugin-validation-guide.md" '### V10 마크다운 표 무결성')" '`skills/*/references/**/*.md` 도 더한다' 'V6 는 같은'`` 1 · 1 · `toks "$(sect "$T/E/harness/docs/guides/plugin-validation-guide.md" '## 8. 변경 이력')" '| 1.4.0 |'` 1.
       봉인 전 실측: 편집 전 판 (a) 14 킷 전부 OK 인데 여섯 범위 합집합과 다른 킷이 10 개(스킬 폴더 안 references 가 있는 킷 전부 — V10 수 211 대 합집합 252) (b) `9 md files — OK` · `rc=0` (c) 0. 모의본 (a) 14 킷 OK · 다른 킷 0 · references 있는 킷 10 · V10 수 합 252 (b) 요구값 (c) 0 — V6 를 같이 넓히면 8 줄 (d) `1.4.0` · 모의본 날짜 `2026-09-25` · 1 · 1 · 1)
- [ ] AR-02: 수집기의 facets · session-meta 폴더 이름이 한 곳에 있어 읽는 자리와 문서 대조가 같은 값을 쓴다 (러닝북 Phase 4 과제 (2)) — (a) `$END` 판 `scripts/collect-kaizen-data.py` 에 `"facets"` 1 줄 · `"session-meta"` 1 줄 (두 이름을 적은 곳이 한 줄뿐이다) (b) `$END` 판 폴더에서 `scripts/test-collect-kaizen-data.py` 의 마지막 줄이 `0 실패` 로 끝나고 `PASS 폴더 이름 한 곳` 2 줄 (c) 음성 대조 — 같은 시험을 `--script` 로 시작 커밋 판 수집기에 돌리면 `FAIL 폴더 이름 한 곳` 2 줄 (d) `drift.sh` 를 `$END` 판에 돌리면 세 줄 `as_is rc=0` · `anchor 1` · `renamed rc=1 1` [exact, enumerated]
      (측정: (a) `grep -cF '"facets"' "$T/E/scripts/collect-kaizen-data.py"` 1 · `grep -cF '"session-meta"' "$T/E/scripts/collect-kaizen-data.py"` 1 · 두 매치가 같은 줄 — `grep -F '"facets"' "$T/E/scripts/collect-kaizen-data.py" | grep -cF '"session-meta"'` 1
       (b) `(cd "$T/E" && python3 scripts/test-collect-kaizen-data.py > "$T/ck.txt" 2>&1)` 뒤 `tail -1 "$T/ck.txt" | grep -c ' 0 실패$'` 1 · `grep -c '^PASS 폴더 이름 한 곳' "$T/ck.txt"` 2
       (c) `(cd "$T/E" && python3 scripts/test-collect-kaizen-data.py --script "$T/B/scripts/collect-kaizen-data.py" 2>&1) | grep -c '^FAIL 폴더 이름 한 곳'` 2
       (d) `bash "$K/drift.sh" "$T/E"` 가 위 세 줄.
       봉인 전 실측: 편집 전 (a) `"facets"` 2 줄 · `"session-meta"` 2 줄 (b) 새 경우 없음 · `29 통과 · 0 실패`. 모의본 (a) 1 · 1 · 1 (b) `31 통과 · 0 실패` · 2 (c) 2 (d) 요구값. 결함 대조: 편집 전 판의 읽는 자리 `usage_dir / "facets"` 만 `"facets2"` 로 바꾼 사본에서 `validate-doc-contracts.py` 가 `violation 0` · 종료 코드 0 — 문서 대조가 어긋남을 못 잡는다)
- [ ] AR-03: 선언 범위 밖 커밋 차단의 첫 단계로, 범위 선언을 기계가 읽을 자리를 정해 킷 문서에 적는다 (insights:scope-commit-block · F28 · 러닝북 Phase 4 과제) — `harness/README.md` 의 `## 커밋 안전 훅` 구간에 5 토큰 `**계약이 선언한 범위 밖 경로는 아직 막지 않는다.**` · `` `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 `text` 코드 블록이다 `` · `한 줄에 git pathspec 하나를 레포 루트 기준으로 적는다` · `계약 봉인 커밋(sprint-contract Step 6.7)이 그 원문을 git 에 남기므로` · `계약에 이 블록을 쓰는 절차와 훅이 읽는 절차는 아직 없다` 가 각각 1 건이고, 그 구간에서 첫 줄이 `# sprint-scope` 인 `text` 블록을 읽는 한 줄 awk 가 두 줄 `harness/scripts/commit-guard.sh` · `harness/evals/hooks/` 를 낸다 [exact, enumerated]
      (측정: ``toks "$(sect "$RM" '## 커밋 안전 훅')" '**계약이 선언한 범위 밖 경로는 아직 막지 않는다.**' '`## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 `text` 코드 블록이다' '한 줄에 git pathspec 하나를 레포 루트 기준으로 적는다' '계약 봉인 커밋(sprint-contract Step 6.7)이 그 원문을 git 에 남기므로' '계약에 이 블록을 쓰는 절차와 훅이 읽는 절차는 아직 없다'`` 5 값 전부 1 ·
       ``sect "$RM" '## 커밋 안전 훅' | awk '/^```text$/{b=1;n=0;next} b&&/^```$/{b=0;next} b&&!n{n=1;f=($0=="# sprint-scope");next} b&&f' | tr '\n' ' '`` 이 `harness/scripts/commit-guard.sh harness/evals/hooks/ `.
       봉인 전 실측: 편집 전 5 값 0 · awk 빈 출력. 모의본 5 값 1 · 요구값. 문장 삭제 대조: `회귀 게이트` 절 표)
- [ ] AR-04: README 의 커밋 안전 훅 설명이 바뀐 동작과 같다 (러닝북 Phase 4 과제 (1) 의 반대편) — `## 커밋 안전 훅` 구간에 옛 문장 `` 경로를 지정한 커밋(`-o`, `-- <경로>`)과 병합 · 골라담기 · 되돌리기 도중의 커밋은 검사하지 않는다 `` 0 · 새 토큰 `그 경로 안에서 작업 폴더에 없는 추적 파일만 삭제로 센다` · `` `-i` 는 목록 전체에 그 경로의 작업 폴더 삭제를 더해 센다 `` · `` 경로를 파일로 넘기는 커밋(`--pathspec-from-file`)은 검사하지 않는다 `` · `꺼내지 않은 파일은 작업 폴더에 없어도 git 이 싣지 않으므로 세지 않는다` 각 1 건이고, README 가 검사하지 않는다고 적은 형태가 실제로 통과한다 — `pfile.sh` 를 `$END` 판 훅에 돌리면 `pfile rc=0` [exact, enumerated]
      (측정: ``toks "$(sect "$RM" '## 커밋 안전 훅')" '경로를 지정한 커밋(`-o`, `-- <경로>`)과 병합 · 골라담기 · 되돌리기 도중의 커밋은 검사하지 않는다' '그 경로 안에서 작업 폴더에 없는 추적 파일만 삭제로 센다' '`-i` 는 목록 전체에 그 경로의 작업 폴더 삭제를 더해 센다' '경로를 파일로 넘기는 커밋(`--pathspec-from-file`)은 검사하지 않는다' '꺼내지 않은 파일은 작업 폴더에 없어도 git 이 싣지 않으므로 세지 않는다'`` 이 `0 1 1 1 1` · `bash "$K/pfile.sh" "$T/E/harness/scripts/commit-guard.sh"` 가 `pfile rc=0`. `-i` 문장의 동작은 ER-01 ㉒, 희소 체크아웃 문장의 동작은 ER-01 ㉕ 가 잰다.
       봉인 전 실측: 편집 전 `1 0 0 0 0` — 옛 문장이 편집 전 1 이라 측정이 살아 있다 · `pfile rc=0`. 모의본 `0 1 1 1 1` · `pfile rc=0`. 문장 삭제 대조: `회귀 게이트` 절 표)
- [ ] AR-05: 이 Phase 의 변경이 허용 경로 안에 머물고 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p04-harness` · 측정 셋 —
       ① `type unsigned_on >/dev/null || exit 2;` 뒤 `unsigned_on "$B" "$END" "$SIG" harness scripts | grep -c .` 0 (`harness/` · `scripts/` 를 건드린 구간 안 커밋이 전부 서명했다 — 이 구간에 두 폴더를 고칠 수 있는 Phase 는 4 하나다. 서명을 빠뜨린 이 Phase 커밋이 열네 파일 밖의 `harness/` · `scripts/` 파일을 건드려도 여기서 드러난다)
       ② `.harness/` 밖은 열네 파일뿐이다 — `type my >/dev/null || exit 2;` 뒤 `my | grep -vE "^(\.harness/|($FRE)$)" | grep -c .` 0 · `my | grep -cxE "$FRE"` 14
       ③ `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태 — `type verify_seal >/dev/null || exit 2;` 뒤 `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '{print $1}' | sort | uniq -c` 를 근거로 남기고, 그 가운데 이 Phase 몫인 `SEAL_BROKEN` 이 0 개 — `find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .` 0. 그리고 이 계약 자신이 봉인돼 있다 — `verify_seal "$CF" | cut -d' ' -f1` 이 `SEAL_OK` (`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL).
       봉인 전 실측: `회귀 게이트` 절 `예행` — ① 0 · ② 0 · 14 · ③ 이 Phase 몫 0 · 이 계약 `SEAL_OK`. 음성 대조: 예행 사본에 서명 없이 `harness/hooks/hooks.json` 을 고친 커밋을 얹고 `end_sha` 를 옮기면 ① 1 — 같은 사본에서 열네 파일만 보던 옛 ① 과 서명 줄 목록인 ② 는 둘 다 0 이었다(열네 파일 밖이고 서명이 없다). 서명 없는 커밋이 `harness/README.md` 를 건드려도 ① 1. 봉인 전인 지금 작업 폴더의 이 계약은 `SEAL_ABSENT` — 봉인을 빠뜨리면 ③ 이 떨어진다)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열네 파일에 더한 줄의 버전꼴 문자열(`x.y.z`)이 검증 가이드 자신의 머리 설정 `version` 값(`$END` 판에서 읽은 값) 말고 0 건이다 — 그 값이 이력 줄과 같은지는 AR-01 (d) 가 잰다 [exact]
      (측정: `type added >/dev/null || exit 2;` 뒤 `PGV=$(head -6 "$T/E/harness/docs/guides/plugin-validation-guide.md" | sed -n 's/^version: //p')` 뒤 `added | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | sed 's/^v//' | sort -u | grep -vxF "$PGV" | grep -c .` 0. 봉인 전 실측: 모의본 더한 줄의 버전꼴은 `1.4.0` 두 번뿐이라 0. 양성 대조: 모의본 README 에 `9.9.9` 한 줄을 더하면 1)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 는 검증 가이드를 읽지 않으므로 마크다운 일곱 파일을 같은 판정에 펜스 길이를 더한 검출기로 잰다 [exact]
      (측정: `(cd "$T/E" && python3 "$K/fence.py" "${MDS[@]}") | tail -1` 이 `bare_open_total=0 unclosed_total=0`. V6 쪽은 DG-05. 봉인 전 실측: 모의본 0 · 0. 양성 대조: 모의본 README 끝에 언어 힌트 없는 펜스를 더하면 `bare_open_total=1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 다섯의 첫 frontmatter 블록에 `name: <폴더 이름>` 줄이 1 개씩 그대로다 [exact]
      (측정: `for s in sprint create-agent create-skill contract-kaizen harness-kaizen; do printf '%s ' "$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f' "$T/E/harness/skills/$s/SKILL.md" | grep -cx "name: $s")"; done` 이 `1 1 1 1 1`. V1 쪽은 DG-05. 봉인 전 실측: 편집 전 · 모의본 `1 1 1 1 1`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 수집기의 폴더 이름 상수는 모듈 최상위의 밑줄 없는 이름이라 시험과 `doc_contract()` 가 같은 값을 읽는다 [exact]
      (측정: `grep -cE '^USAGE_DATA_DIRS: ' "$T/E/scripts/collect-kaizen-data.py"` 1 · `grep -c '_USAGE_DATA_DIRS' "$T/E/scripts/collect-kaizen-data.py"` 0 · `grep -c 'module.USAGE_DATA_DIRS' "$T/E/scripts/test-collect-kaizen-data.py"` 1 이상. 봉인 전 실측: 편집 전 0 · 0 · 0, 모의본 1 · 0 · 1)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 훅에 더한 함수는 하나(경로 커밋 세기)뿐이고 기존 도우미 `block` · `top_dirs` 를 불러 막으며, 피드백 저장 스크립트의 검사 함수는 초안 · 최종본이 같이 쓰는 하나다 [exact]
      (측정: ``comm -13 <(grep -oE '^[a-z_]+\(\)' "$T/B/harness/scripts/commit-guard.sh" | sort) <(grep -oE '^[a-z_]+\(\)' "$T/E/harness/scripts/commit-guard.sh" | sort) | tr '\n' ' '`` 이 `check_path_commit() ` · `awk '/^check_path_commit\(\)/{f=1} f; f&&/^}/{exit}' "$T/E/harness/scripts/commit-guard.sh" | grep -cE '^  block |top_dirs '` 2 · `grep -c '^validate_yaml()' "$T/E/harness/scripts/save-feedback.sh"` 1. 봉인 전 실측: 모의본 요구값. 편집 전 `grep -c '^validate_yaml()'` 1)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 양성 대조: 같은 `grep -c` 에 `scripts/release.sh` · `scripts/release.sh.bak` 두 줄을 넣으면 1. 실제 분석은 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: (a) 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 일곱 파일의 **더한 줄**에 걸린 경고가 0 (b) 셸 네 파일의 shellcheck 0.11.0 결과에 편집 전에 없던 경고가 0 (c) 파이썬 세 파일이 `python3 -W error -m py_compile` 로 0. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: (a) `회귀 게이트` 절의 `new-warnings.sh` 를 `for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$T/E/$f" "$T/$k.md"; bash "$K/new-warnings.sh" "$T/$k.0.md" "$T/$k.md"; done` 로 돌려 일곱 줄 모두 `new_warnings=0` 이고 `LINT_NOT_RUN` 줄 0
       (b) `for f in "${SHS[@]}"; do comm -13 <(shellcheck -f gcc "$T/B/$f" | sed -E 's/^[^:]+:[0-9]+:[0-9]+: //' | sort) <(shellcheck -f gcc "$T/E/$f" | sed -E 's/^[^:]+:[0-9]+:[0-9]+: //' | sort) | grep -c .; done | tr '\n' ' '` 이 `0 0 0 0 `
       (c) `for f in "${PYS[@]}"; do python3 -W error -m py_compile "$T/E/$f"; echo $?; done | tr '\n' ' '` 이 `0 0 0 `.
       봉인 전 실측: 모의본 (a) 일곱 줄 `new_warnings=0` (더한 줄 71 · 4 · 3 · 1 · 1 · 11 · 7) (b) `0 0 0 0` — 시험 파일의 편집 전 `SC2016` 둘은 그대로 (c) `0 0 0`. 양성 대조: Step 5 코드 블록 앞 빈 줄을 뺀 sprint 모의본 1 (MD031), 언어 힌트 없는 펜스를 더한 README 모의본 2, 따옴표 없는 `$1` 을 더한 훅 사본 1 (SC2086). 이 양성 대조가 죽은 측정을 찾았다 — 도우미 폴더 옆에 `node_modules` 가 없어 린터가 안 돌았는데 경고 0 이 조용히 나왔다. 그래서 `new-warnings.sh` 는 린터가 돌았다는 줄이 없으면 `LINT_NOT_RUN` 과 종료 코드 2 로 멈춘다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 시험은 ER-01 · ER-02 · AR-02)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 훅 · 스크립트는 ER-01 · ER-02 · AR-02 가 시험 저장소에서 실제로 돌린다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(dart|ts|tsx|js|rs|go)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `a/b.dart` · `c.ts` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사가 이 Phase 파일을 문제로 가리키지 않는다 — (a) `python3 scripts/validate-plugin.py harness` 출력에 `V1` ~ `V10` 열 줄이 있고 하나도 `ERROR` · `FAIL` 이 아니다 (b) 전체 킷 `--check=table-integrity,code-fence` 의 `FAIL` 줄 가운데 이 Phase 파일을 가리키는 줄 0 (c) `sync-docs.py --check-only` · `sync-evals.py --check-only` · `run-evals.py` · `validate-doc-contracts.py` 가 종료 코드 0 이고 `check-stale-values.py` 가 0 또는 1 이며 출력에 이 Phase 파일 0 건 (d) 셸 네 파일이 `bash -n` · `/bin/bash -n` 둘 다 0 [exact]
      (Given: 작업 트리의 열네 파일이 `$END` 와 같다 — `git diff --quiet "$END" -- "${FILES[@]}"` exit 0 · 측정: (a) `python3 scripts/validate-plugin.py harness > "$T/vp.txt" 2>&1` 뒤 `grep -cE '^  V([1-9]|10) ' "$T/vp.txt"` 10 · `grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cE 'ERROR|FAIL'` 0
       (b) `python3 scripts/validate-plugin.py --check=table-integrity,code-fence > "$T/vpa.txt" 2>&1; grep -E '^ +FAIL ' "$T/vpa.txt" | grep -cE "$FRE"` 0. 다른 파일의 FAIL 줄은 다른 Phase 몫으로 근거에 적는다
       (c) `for c in 'sync-docs.py --check-only' 'sync-evals.py --check-only' 'run-evals.py' 'validate-doc-contracts.py'; do python3 scripts/$c >/dev/null 2>&1; printf '%s ' "$?"; done` 이 `0 0 0 0 ` · `python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1; echo $?` 가 0 또는 1 · `grep -cE "$FRE" "$T/sv.txt"` 0
       (d) `for f in "${SHS[@]}"; do bash -n "$T/E/$f"; printf '%s' "$?"; /bin/bash -n "$T/E/$f"; printf '%s ' "$?"; done` 이 `00 00 00 00 `.
       봉인 전 실측: 모의본을 git 저장소로 만든 사본(`p4d/g-mock`)에서 (a) V1 ~ V10 OK (b) FAIL 0 (c) 전부 0 · check-stale-values 0 「되살아난 옛 값 없음」 (d) 전부 0. 편집 전 사본(`p4d/g-base`)도 같다. 양성 대조: V10 은 AR-01 (b), V6 는 AP-03 과 같은 사본)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 3a51b733ab84a997fe34de042fcc743b45664f46` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록에 서명 줄 커밋이 없을 때 이 조건은 PASS 다. `doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄에 나온 경로를 `my` 와 대조해, 겹치는 경로가 0 개면 다른 Phase 몫으로 근거에 적고 이 조건은 PASS 다 [exact]
      (측정: 명령 출력의 두 줄. `doc-contracts` 가 `FAIL` · `ERROR` 일 때만 — `type my >/dev/null || exit 2;` 뒤 `python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u | comm -12 - <(my) | grep -c .` 0.
       `scope-isolation` 이 `FAIL` 일 때만 — `python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1` 뒤
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | grep -c .` 이 1 이상(위반 목록을 실제로 읽었다) ·
       `awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" | while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done | grep -c .` 0.
       첫 값을 함께 거는 이유: 출력 형식이 바뀌어 목록을 하나도 못 읽으면 둘째 값이 조용히 0 이 된다.
       봉인 전 실측: `회귀 게이트` 절 `예행` 의 값)
