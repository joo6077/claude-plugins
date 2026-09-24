# 카이젠 2026-09-24 Phase 4 (harness) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p04-harness.md` (조건 28 · 기능 조건 18, 봉인 `sha256:afb7f33963bceeda` · `locked_at` 2026-09-25 04:17)
- 개정: `.harness/sprint-amendments-kaizen-0924-p04-harness.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase4-review.md` (1 회차 CHANGES 막는 이유 넷은 초안이 반영, 2 회차 APPROVE 권고 셋은 BUILD 가 봉인 전에 반영)
- 시작 커밋 `3a51b733ab84a997fe34de042fcc743b45664f46`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T042346-de8c7935-31191.yaml` (`verify-feedback.sh` PASS). 레포 판
  `save-feedback.sh` 로 저장했다 — 초안에 `project_hash` · `project_name` 을 일부러 적지 않았는데 저장됐다(ER-02 를 실제 초안으로 한 번 더 돌린 셈)

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `4a888e1` | 봉인 커밋 | 계약 1 개 |
| `4d2c985` | 커밋 안전 훅 — 경로 지정 커밋의 삭제 세기 | `harness/scripts/commit-guard.sh` · `harness/evals/hooks/commit-guard-test.sh` · `harness/README.md` |
| `42f300b` | 피드백 초안 필수 필드 | `harness/scripts/save-feedback.sh` · `harness/evals/kaizen/feedback-system/save-test.sh` |
| `bcaa878` | 스킬 다섯 | `harness/skills/{sprint,create-agent,create-skill,contract-kaizen,harness-kaizen}/SKILL.md` |
| `0da6157` | V10 범위 · 검증 가이드 1.4.0 | `scripts/validate-plugin.py` · `harness/docs/guides/plugin-validation-guide.md` |
| `c9477a4` | 수집기 폴더 이름 한 곳 | `scripts/collect-kaizen-data.py` · `scripts/test-collect-kaizen-data.py` |
| `f6cc80c` | 개정 파일에 `end_sha` (`c9477a4`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p04-harness` 줄이 있다. 구현 커밋은 수정 단위마다
`git add -- <파일> && git commit -o -- <파일…>` 로 내 경로만 실었다. 이 세션의 커밋 훅은 설치본(0.13.0)이라 새 판이 걸리지 않았다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

28 조건 측정은 봉인 판 계약에서 기계로 뗀 묶음으로 돌렸다 — 스크래치 `p4build/extract.py`(계약 `회귀 게이트` 절 코드 블록을 첫 주석 줄의
이름으로 저장 — `common.sh` 와 도우미 열하나, 초안의 `p4d/k/` 와 `cmp` 로 같다) · `p4build/run.sh`(공통 정의를 `.` 로 읽은 뒤 조건 문구 그대로의 측정).
ER-05 를 뺀 27 조건이 notes 전에 전부 요구값이었다(`p4build/run1.txt`). QA 가 같은 묶음을 다시 돌릴 수 있다.

## 바꾼 파일

- `harness/scripts/commit-guard.sh` — 인자를 가를 때 경로 인자를 모으고(`--pathspec-from-file` 은 따로 표시), 경로 지정 커밋이면
  새 함수 `check_path_commit` 이 HEAD 를 읽은 임시 목록에서 그 경로 안 `ls-files --deleted` 를 센다. 희소 체크아웃으로 꺼내지 않은 파일(`S`)은 뺀다.
  50 개를 넘으면 `확인: git status --short -- <지정한 경로>` 와 함께 막는다. `-i <경로>` 는 목록 삭제에 그 경로의 작업 폴더 삭제를 더한다.
  병합 도중 확인을 경로 커밋 판정 앞으로 옮겼다
- `harness/evals/hooks/commit-guard-test.sh` — 경우 ⑰ ~ ㉕ 열 줄(⑰-확인 포함). ㉕ 는 희소 체크아웃 전제부터 확인한다
- `harness/scripts/save-feedback.sh` — 초안 필수 여섯 · 최종본 필수 여덟을 배열 둘로, `validate_yaml <파일> <필드…>` 가 두 백엔드에서 같은 목록
- `harness/evals/kaizen/feedback-system/save-test.sh` — ⑧ 두 필드 없는 초안 저장 · ⑨ `timestamp` 만 빠진 초안의 누락 보고
- `harness/skills/sprint/SKILL.md` — Step 0 워크트리, Step 3 `[미검증]` 네 칸 · 원인 셋 가르기(코드 블록 · 판정 표), Step 4 QA 블록 끝 줄,
  Step 5 내 경로만 싣기, Step 6 끝맺음, References 네 줄
- `harness/skills/create-agent/SKILL.md` — `15 종` → `18 종` 세 곳, Unverifiable 4 항을 agent-design-guide §10 과 같은 말로(특정 앱 이름 삭제)
- `harness/skills/create-skill/SKILL.md` — 「1500-2000 words」 → 500 줄 권고, `argument-hint` 는 자동 완성 힌트
- `harness/skills/contract-kaizen/SKILL.md` Step 2 · `harness/skills/harness-kaizen/SKILL.md` Step 2a — 옛 문구 12 항목은
  `measure_premise_unrun` 키가 있는 파일에서만 센다
- `harness/README.md` 커밋 안전 훅 절 — 바뀐 동작, 검사하지 않는 형태, 범위 선언을 읽을 자리(`# sprint-scope` 블록)
- `harness/docs/guides/plugin-validation-guide.md` 1.3.1 → 1.4.0 — V10 범위 문단 · 이력 한 줄
- `scripts/validate-plugin.py` — V10 범위에 `skills/*/references/**/*.md`
- `scripts/collect-kaizen-data.py` — `USAGE_DATA_INPUTS` → 폴더 이름 상수 `USAGE_DATA_DIRS` 하나를 읽는 자리와 `doc_contract()` 가 같이 쓴다
- `scripts/test-collect-kaizen-data.py` — 폴더 이름을 한 곳에서 바꾸는 경우 하나(검사 둘)

스킬 frontmatter 는 그대로다 — harness README AUTO 구간 변화 없음(`sync-docs.py --check-only` 0).

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `harness:P02` · `F14` | 피드백 저장 첫 검사가 초안에 `project_hash` · `project_name` 을 요구하지 않는다. 최종본 검사는 여전히 요구한다 (ER-02) |
| `harness:P07` · `F08` | `/sprint` Step 5 내 경로만 싣기 · Step 0 워크트리 · Step 3 기준 커밋 비교 (SK-01 · SK-02 · SK-03) |
| `user-setup:P2` | 워크트리 권고 · 커밋 전 삭제 보고(Step 5 `git status --short -- <내 경로…>` 줄)는 반영. 폐기 결정 줄은 미반영(아래) |
| `F09` | 원인 가르기 규칙을 `/sprint` Step 3 하나로 정했다 (SK-03). 다른 킷이 맞출 판정 세 줄은 아래 넘김 표 |
| `F28` | 워크트리 준비는 `/sprint` Step 0, 커밋 전 검사는 커밋 안전 훅의 경로 지정 커밋 (ER-01 · AR-04) |
| `F18` · `other-kits:P10` | V10 범위에 스킬 폴더 안 references (AR-01). 14 킷 41 개가 검사 밖이었고 끊긴 표는 0 개 |
| `insights:scope-commit-block` | 범위 선언을 기계가 읽을 자리를 정했다 — 계약 `## 범위 경계` 절 안 첫 줄이 `# sprint-scope` 인 `text` 블록 (AR-03). 쓰는 절차 · 읽는 훅은 넘김 |

러닝북 Phase 4 추가 과제 셋도 반영했다 — (1) 경로 지정 커밋 삭제(ER-01 · AR-04) (2) 수집기 폴더 이름(AR-02) (3) 범위 선언 자리(AR-03).
앞 Phase 넘김은 Phase 1 의 `/sprint` `[미검증]` · create-agent · create-skill(SK-04 · SK-05), Phase 2 의 `/sprint` 끝 줄 · contract-kaizen 세기(SK-04 · SK-06).

## 미반영 키와 사유

- `user-setup:P2` 의 폐기 결정 줄 — 기록 자리를 하나로 정하는 일이 `F20`(Phase 11) 몫이다
- `F28` 의 워크트리 상태 스크립트 — 근거 파일 §2 F28 이 외부 권고를 찾지 못했다. 시뮬레이터 · 데이터베이스 나누기도 맡은 제안이 없다
- `F18` 의 YAML 블록 검사 — 14 킷 `yaml` 펜스 60 개 중 파싱 실패 3 개가 전부 일부러 깨 놓은 예시 · 자리표시자라 걸리는 것이 전부 잘못 잡은 것이다.
  실행되는 YAML 은 V2 와 `validate-doc-contracts.py` 가 이미 파싱한다
- Phase 3 이 넘긴 `assertions.json 실행기` — 처리 배정표 밖이고 크기에 비해 조건이 는다. 아래 넘김 표

## 넘기는 것 (명시적 미완)

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `sprint-contract Step 9` | 다음 사이클 Phase 2 | 초안 필수 여섯(`schema_version skill timestamp skill_version outcome diagnosis`)으로 문구를 맞춘다. 고정 이름 `.harness/feedback-draft.yaml` 을 여러 세션이 덮는 문제(Phase 3 메모) — 이번에도 `.harness/feedback-draft-p04.yaml` 로 갈라 썼다 |
| `feedback-schema.yaml` | 다음 사이클 Phase 2 · 3 | true 가 「문제가 있다」 인 뜻과 새 키 둘(`measure_premise_unrun` · `known_answer_missing`). harness-kaizen Gotcha 가 이 파일 수정을 막는다 |
| `# sprint-scope` | 쓰는 쪽 다음 사이클 Phase 2 · 읽는 쪽 다음 사이클 Phase 4 | 쓰는 쪽은 contract-schema 절 · sprint-contract Step 6. 읽는 쪽은 커밋 훅이 훅 입력 `session_id` 와 계약 `owner_session` 으로 이번 세션의 계약을 찾는다 — 그때 실측한다 |
| `assertions.json 실행기` | 다음 사이클 (Phase 3 넘김) | 이번에 만들지 않았다. 처리 배정표 밖이다. contract-kaizen · evaluator-kaizen 두 벌을 도는 실행기 |
| `agent-design-guide.md:79` | 다음 사이클 Phase 1 | `model` 을 생략했을 때의 동작 — 근거 파일 §3 |
| `create-agent/SKILL.md:25` | 다음 사이클 Phase 1 · 4 | 「`model` 을 생략하면 `inherit`」 (`:80` 도 같다). `agent-design-guide.md:79` 와 함께 고친다 — 스킬만 고치면 가이드와 갈린다 |
| `create-skill/SKILL.md:27` | 다음 사이클 Phase 1 · 4 | 「공식 필수는 `name` 과 `description`」 · 「다른 플랫폼에서는 무시된다」. skill-design-guide §frontmatter 규칙과 함께 고친다 |
| `sprint-contract Step 6.7 (a)` | 다음 사이클 Phase 1 · 2 | 같은 작업 폴더에서 `checkout -b` 하지 않는다는 문장을 skill-design-guide §9 와 함께 넣는다 — `/sprint` Step 0 워크트리 문단과 맞춘다 |
| `backend-family:P3` · `backend-family:P4` | Phase 8 · 9 | `/sprint` Step 3 의 판정 세 줄을 옮겨 적는다 (아래 블록). 플러그인이 따로 설치돼 경로로 가리킬 수 없다 |
| `flutter-preflight` · `react-preflight` | Phase 5 · 10 | 기준 커밋 비교가 없다 — 필요하면 같은 판정 세 줄을 쓴다 |
| `F20` | Phase 11 | 폐기 결정 기록 자리를 하나로 정한 뒤 `/sprint` 재검증 블록에 그 자리를 읽는 줄을 둔다 |
| `V6 범위` | 다음 사이클 Phase 4 | 스킬 폴더 안 references 의 언어 힌트 없는 펜스 8 개(카이젠 PR 템플릿 넷 × 2)를 고친 뒤 V10 과 같은 범위로 넓힌다 |
| `reflect-collector:P5` | 다음 사이클 Phase 4 | `save-feedback.sh` 가 저장본 `project_name` 을 워크트리 폴더 이름으로 적는다 — 이번 저장본도 `kaizen-0924`. 본 레포 이름을 구하는 규칙의 근거는 이번 사이클 `phase12.md` 에만 있고 Phase 12 범위는 `reflect-kit/` 라 이 파일을 못 고친다 |
| `.github/workflows/ci.yml` | 없음 | 넣을 줄이 없다 — 새 경우는 CI 가 이미 돌리는 시험 파일(`commit-guard-test.sh` · `save-test.sh` · `test-collect-kaizen-data.py`) 안에 있다 |
| `docs/harness/*.html` | Final F2 | 검증 가이드 1.4.0 페이지를 다시 만든다. `validate-post-kaizen.py --since 3a51b73` 의 `docs-site-regen` 이 이 때문에 FAIL 이다 |

Phase 8 · 9 가 옮겨 적을 판정 세 줄(`harness/skills/sprint/SKILL.md` Step 3, 원문 그대로):

```text
| 실패 | 통과 | — | 미커밋 변경 탓 — `git status --short` 의 파일이 내가 쓴 목록 밖이면 남의 미커밋이다 |
| 실패 | 실패 | 실패 | 기준 커밋에서 이미 실패 — 내 변경 전부터다 |
| 실패 | 실패 | 통과 | 이번 커밋 탓일 가능성이 크다 |
```

열은 차례로 공용 작업 폴더 · `HEAD` 임시 워크트리 · `FORK_BASE`(`git merge-base HEAD origin/<기준 가지>`) 임시 워크트리 · 판정이다.

Final 이 더 할 것: `harness` plugin.json 버전 — harness-kaizen 버전 판단표로는 스킬 절차 추가(`/sprint`)와 훅 동작 변경이라 minor 다.
이 Phase 는 공유 파일(marketplace · plugin.json · 루트 README · 루트 CLAUDE.md · `docs/` · 감사 로그 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml`)을 건드리지 않았다.

## changelog 한 단락

커밋 안전 훅이 경로를 지정한 커밋(`git commit -o <경로>` · `-- <경로>`)도 검사한다. 그전에는 이 형태를 통째로 건너뛰어 그 경로 안의
대량 삭제가 그대로 실렸다. 경로 지정 커밋은 공용 목록이 아니라 HEAD 위에 그 경로의 작업 폴더 상태를 얹으므로, 훅도 그 경로 안에서
작업 폴더에 없는 추적 파일만 세어 50 개를 넘으면 막는다. 목록에서만 뺀 파일 · 빈 개인 목록 · 희소 체크아웃으로 꺼내지 않은 파일은 git 이
싣지 않으므로 세지 않는다. 피드백 저장 스크립트는 초안에 `project_hash` · `project_name` 을 요구하지 않는다 — 스크립트가 다시 계산해
덮어쓰는 값이라 초안에 요구하면 버릴 값 때문에 저장이 거부됐다. `/sprint` 는 내 경로만 싣는 커밋 절차, 병렬 작업일 때 워크트리, 빨간 검사의
원인을 이번 변경 · 남의 미커밋 · 기준 커밋 셋으로 가르는 코드 블록을 얻었다. V10 표 검사가 스킬 폴더 안 references 문서까지 본다.
카이젠 수집기의 facets · session-meta 폴더 이름은 한 곳에만 적는다. 범위 밖 커밋을 막을 때 훅이 읽을 자리(계약의 `# sprint-scope` 블록)를 정했다.

## 킷 로그 한 단락 (harness)

2026-09-24 Phase 4 — harness-kaizen. 트리거 orchestrator-phase-4. 피드백: 글로벌 계약 피드백 최근 10 건(임계를 넘은 항목은 옛 문구로 적힌
`nfr_coverage` 6 건뿐 — 새 세기 규칙으로 0) · 평가 피드백 최근 10 건(임계 넘은 항목 0). 근거:
[git commit](https://git-scm.com/docs/git-commit) (`--only` 는 지정한 경로의 작업 폴더 내용을 싣는다 — 훅 · `/sprint` Step 5),
[git worktree](https://git-scm.com/docs/git-worktree) (워크트리마다 `HEAD` 와 목록을 따로 둔다 — Step 0),
[git merge-base](https://git-scm.com/docs/git-merge-base) (분기점이지 기준 가지의 지금 상태가 아니다 — Step 3),
[Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) (`isolation: worktree` 는 기본 가지에서 만든다 — Step 0),
[Claude Code Skills](https://code.claude.com/docs/en/skills) (`argument-hint` 는 자동 완성 힌트 — create-skill),
[Claude Code Hooks](https://code.claude.com/docs/en/hooks) (`PreToolUse` 는 exit 2 로 막는다 — 훅이 커밋 전에 막는 근거).
근거 파일이 밝힌 한계 — 피드백 초안과 최종본을 가르는 외부 표준은 없다(근거는 스크립트의 생성 순서), `-o` 는 누가 고쳤는지 판정하지 않는다
(그래서 Step 5 에 `git diff HEAD -- <내 경로…>` 줄), 범위 선언을 frontmatter 에 둘지 따로 둘지는 열린 선택이었다(계약 안 블록을 골랐다).

## 다음 사이클 메모

- 경로 지정 커밋마다 HEAD 전체를 임시 목록으로 읽는다 — 추적 파일이 아주 많은 저장소에서 속도를 재지 않았다. 자기진단 `nfr_coverage` 를 true 로 적었다
- 계약 피드백 자기진단 `implementation_leakage` 도 true — RE-01 · RE-02 가 함수 · 상수 이름을 조건에 적었다. 산출물이 스크립트라 재사용을 재는 자리가 그 이름뿐이었다
- 봉인 판 계약에서 도우미 코드 블록을 떼는 일을 이번에도 스크래치 스크립트(`p4build/extract.py`)로 했다. Phase 3 도 같은 일을 했다 — harness scripts 에 둘 만하다
- harness-kaizen `추적 규칙` 표는 커밋 머리를 `kaizen:` 으로 적으라는데 이번 사이클 Phase 1 ~ 4 는 모두 `docs(harness):` · `fix(...)` 형태로 적었다. 표를 고칠지 따를지 다음 사이클이 정한다
- 2 회차 검토 권고 첫째 — AR-05 ① 은 다른 Phase 서명이 달린 커밋도 서명 없는 커밋으로 센다. ER-05 넷째는 그 경우를 뺀다. 두 측정의 태도를 맞추는 형태를 contract-schema 에 올릴 만하다
