---
feature: "병렬 스프린트 안전성 — 계약 경로 접미형 정식화 + 피드백 귀속 결정론화 + 중간 교정 감사"
created: "2026-07-28 03:40"
complexity: "복잡"
conditions: 25
slug: parallel-sprint-safety
status: active
owner_session: 8a9c2ebc-8d41-48fb-9586-496555a22b30
---

## 배경

harness 는 계약을 단일 고정 경로 `{CONTRACT_ROOT}/.harness/sprint-contract.md` 에, QA 산출물을
`.harness/sprint-feedback.md` 에 쓴다. 같은 프로젝트에서 세션을 병렬로 돌리면 세션 A 의 계약을
세션 B 가 덮어쓰고, A 의 qa-evaluator 가 B 의 계약을 평가한다.

실증: 2026-07-27 카이젠에서 Phase 5~14 를 병렬로 돌릴 때 각 서브에이전트 프롬프트에
"고정 경로 대신 phase 별 경로에 써라" 를 손으로 박아야 했다. 그 원인은
`scripts/spawn-kaizen-phase.sh` 가 고정 경로를 프롬프트에 주입하고 있기 때문이다.

부수 문제 2 종:
- 글로벌 피드백 저장소(`~/.harness/feedback/evaluator/`, 244 건)의 identity 를 LLM 이 생성한다.
  `claude-plugins` 하나에 `project_hash` 43 종, `ea3aeacd` 는 3 개 프로젝트가 공유.
  fallback 이 `pwd` 기반이라 cwd 가 다르면 같은 프로젝트도 다른 해시가 된다.
- 계약이 write-once 라 실행 중 사용자 교정을 담을 자리가 없다. digest 에 usc=true 재위반 12 건,
  그중 계약 본문을 코드에 맞춰 넓혀 위반을 소거한 사례 1 건(`contract-scope-expanded-after-edit`).

## 리서치 소스

- 배포본 실측: fit-pal 3 개 `.harness` 에 접미형 계약 **40 개**, 접미형 피드백 **7 개**.
  최종 수정 2026-07-27. 계약과 피드백이 슬러그로 짝지어져 있다
  (`sprint-contract-emoji-picker.md` ↔ `sprint-feedback-emoji-picker.md`).
- `.harness` 디렉토리 12 개, 그중 4 개가 정상 중첩(`fit-pal/app`, `fit-pal/server`,
  `fit-pal-wt/app`, `fit-pal-wt/server` 이 각자 project.yaml 을 갖고 조상에도 있음).
- 환경변수 `CLAUDE_CODE_SESSION_ID` 가 Bash 에 노출됨을 실측 확인.
- Codex diagnose 3 회 + 설계 패널(3 안 × 9 심사). 초기 접두형 스킴은 배포본 40 개를 고아로
  만든다는 이유로 기각되었고, amendment 를 계약 본문 섹션으로 넣는 안은 schema v4 위반으로 기각.
- 선례: NASA SWE-053(요구사항 변경 통제), ADR supersede 관행, Cucumber living specification.

## GAP 분석

| # | 갭 | 근거 |
|---|---|---|
| G1 | 계약·피드백 경로가 단일 고정이라 병렬 세션이 충돌 | 계약 22 참조 + 피드백 8 참조 |
| G2 | 병렬 스포너가 고정 경로를 프롬프트에 주입 | `scripts/spawn-kaizen-phase.sh` |
| G3 | 피드백 identity 를 LLM 이 생성 + fallback 이 cwd 기반 | `harness/scripts/save-feedback.sh:75-83`, `harness/skills/sprint-contract/SKILL.md:353` |
| G4 | 글로벌 YAML 파일명이 초 단위라 병렬 저장 충돌 | `harness/scripts/save-feedback.sh:72-83` |
| G5 | live reader 가 plain 파일만 읽음 | `harness/skills/sprint/SKILL.md:94`, `scripts/collect-kaizen-data.py:152`, `harness/skills/harness-kaizen/scripts/trigger-check.sh:40-61` |
| G6 | 실행 중 사용자 교정을 담을 구조 없음 | digest usc=true 12 건 |
| G7 | 계약 frontmatter 에 소유권·상태 필드가 없어 ladder 판정 근거가 없음 | `harness/references/contract-schema.md:41` |

## 범위 경계

- 대상: `harness/` (skills·agents·scripts·references), `scripts/` (spawn-kaizen-phase, collect-kaizen-data).
- 비대상: 외부 배포본(fit-pal 등) 파일 수정, 레거시 244 개 피드백 YAML 재작성.
- 브랜치: `kaizen/2026-07-27` 에 이어서 작업.
- **schema drift 인지 사항**: `harness/references/contract-schema.md:44` 는 complexity 를
  `simple|medium|complex` 로 규정하나, 실제 계약 88 개 중 한국어 표기가 80 개다(중간 29 · 복잡 37 ·
  단순 10 등). 본 계약은 다수 관행을 따라 한국어를 쓴다. 어휘 통일은 이번 스프린트 범위 밖이며
  다음 contract-kaizen 이관 사항이다. 이 불일치를 이유로 REJECT 하지 않는다.
- **AP-04 제외 사유**: `.harness/project.yaml:39` 의 AP-04 정규식은 frontmatter 닫는 `---` 에도
  매치되어 대상 98 파일 전부(172 매치)에 히트하는 vacuous 패턴이다. 검사 가치가 없어 제외한다.

## 회귀 게이트

`python3 scripts/validate-plugin.py` 가 11 plugins / 11 OK / Exit 0 이어야 한다.

## Architecture

- [ ] AR-01: 계약 저장 경로가 `{CONTRACT_ROOT}/.harness/sprint-contract-<slug>.md`, QA 산출물이 `{CONTRACT_ROOT}/.harness/sprint-feedback-<slug>.md` 로 규정되고, 슬러그가 없으면 기존 plain 파일명이 계속 유효함이 명시된다. 측정: `harness/references/contract-schema.md` 와 `harness/skills/sprint-contract/SKILL.md` 양쪽에서 `sprint-contract-` 접미형 경로 서술이 각 1 건 이상 grep 되고, plain 유효성 문장이 각 1 건 이상 존재한다. [exact, enumerated]
- [ ] AR-02: 계약 frontmatter 에 `slug`, `status`(active|done), `owner_session` 3 필드가 규정된다. 측정: `harness/references/contract-schema.md` 의 frontmatter 정의 블록에 세 키가 모두 존재한다 (`grep -c` 각 1 이상). [exact, enumerated]
- [ ] AR-03: 중첩 `.harness` 환경에서 CONTRACT_ROOT 가 **가장 가까운 조상**으로 해석된다. 측정: 문서에 기술된 해석 절차를 `~/Hub/10_Dev/fit-pal/app` 에 적용했을 때 결과가 `~/Hub/10_Dev/fit-pal/app` 이어야 하며(`~/Hub/10_Dev/fit-pal` 이 아니다), "후보가 2 개 이상이면 BLOCKED" 류의 규칙이 CONTRACT_ROOT 해석 절에 도입되지 않는다. [exact]
- [ ] AR-04: 계약 본문에 신규 `##` 섹션이 추가되지 않고, amendment 는 사이드카 `{CONTRACT_ROOT}/.harness/sprint-amendments-<slug>.md` 에 기록됨이 규정된다. 측정: `harness/references/contract-schema.md` 의 허용 섹션 목록에 `변경 이력`/`Amendments` 가 **없고**, 사이드카 경로 서술이 1 건 이상 존재한다. [exact]
- [ ] AR-05: `scripts/spawn-kaizen-phase.sh` 소스에 고정 경로 문자열이 남아 있지 않다. 측정(부작용 없음 — 스크립트를 실행하지 않고 소스만 검사): `grep -c '\.harness/sprint-contract\.md' scripts/spawn-kaizen-phase.sh` 가 0. [exact]

## Skill

- [ ] SK-01: `harness/skills/sprint-contract/SKILL.md` 가 (a) 슬러그 도출 규칙 (b) 슬러그 경로 저장 (c) **같은 슬러그를 두 세션이 동시에 생성해도 덮어쓰기가 발생하지 않는 선점 절차** 3 항목을 기술한다. 구현 수단(락 방식)은 지정하지 않는다. 측정: 세 항목에 대응하는 서술이 각 1 건 이상 존재하고, (c) 는 "덮어쓰기 없음" 이라는 결과가 명시된다. [structural, enumerated]
- [ ] SK-02: `harness/agents/qa-evaluator.md` 가 계약 선택 ladder 4 단계를 순서대로 기술한다 — (1) 명시 경로 (2) 현재 세션 소유 active 계약이 유일 (3) active 계약 전체가 유일 (4) 그 외 BLOCKED. 판정 근거는 파일 개수가 아니라 frontmatter `status` 다. 측정: 4 단계가 번호 순서대로 존재하고, `status` 를 읽는다는 서술이 1 건 이상 있으며, 4 단계에 BLOCKED 가 명시된다. [structural, enumerated]
- [ ] SK-03: qa-evaluator 가 선택한 계약을 `경로 + 내용 해시 + status` 로 고정하고 verdict 저장 직전 재확인하여 달라졌으면 BLOCKED 하는 절차를 기술한다. 측정: 세 요소(경로·해시·status)와 "저장 직전 재확인" 이 모두 서술된다. [structural, enumerated]
- [ ] SK-04: qa-evaluator 에 User Correction Audit 단계가 있고 (a) 읽기 전용 (b) 자동 REJECT 를 유발하지 않음 (c) 출력에 `unreflected_corrections` 노출 (d) 로그 부재 시 `correction_log_status: unavailable` 로 degrade 4 항목을 기술한다. 측정: 네 항목 서술이 각 1 건 이상. [structural, enumerated]
- [ ] SK-05: qa-evaluator 의 로그 조회 경로가 **읽기 전용이어서 새 로그 버킷이나 `.project-root` 마커를 생성하지 않는다**. 측정(결과 기준 — 특정 함수명 금지/허용을 문자열로 세지 않는다): 문서에 기술된 조회 절차를 따랐을 때 `~/.claude/logs/` 하위에 디렉토리·파일이 새로 생기지 않음이 절차상 보장되고, 그 취지가 문장으로 명시된다. [structural]
- [ ] SK-06: amendment 규약이 (a) relaxing 또는 unknown 유형은 PASS 근거로 쓸 수 없음 (b) 원 조건 삭제 금지 (c) prompt-log 앵커(timestamp·session·cwd) 필수 3 항목을 명시한다. 측정: 세 항목 서술이 각 1 건 이상. [structural, enumerated]

## Script

- [ ] SC-01: `harness/scripts/save-feedback.sh` 가 `project_name`/`project_hash` 를 스스로 계산해 draft 값을 덮어쓰고, 원본을 `draft_project_name`/`draft_project_hash` 로 보존하며, 값이 달랐으면 stderr 에 경고를 낸다. 결과 기준: 계산 결과가 reflect-kit 의 project-id canonicalization 과 동일해야 하며, 구현이 기존 헬퍼를 재사용하든 자체 구현하든 무관하다. 측정: 임시 draft 에 `project_hash: bogus1` 를 넣고 실행 → 저장된 YAML 의 `project_hash` 가 `bogus1` 이 아니고, `draft_project_hash: bogus1` 가 보존되며, stderr 에 경고 문자열이 1 건 이상 출력된다. [exact]
- [ ] SC-02: 글로벌 피드백 YAML 파일명이 같은 초에 두 번 저장해도 충돌하지 않는다. 측정(정적): 파일명 조립 라인에 세션 식별자·pid·나노초 중 하나 이상이 포함된다. 측정(동적): `HOME` 을 임시 디렉토리로 바꾼 뒤 같은 draft 로 `save-feedback.sh` 를 연속 2 회 실행하면 생성 파일이 2 개다. [exact]
- [ ] SC-03: `scripts/collect-kaizen-data.py` 가 plain `sprint-feedback.md` 와 접미형 `sprint-feedback-*.md` 를 모두 수집하고, 레거시 `project_name` 별칭 병합은 **명시 allowlist 로만** 수행한다(이름 유사도 기반 자동 병합 금지). 측정: 접미형 피드백이 있는 디렉토리를 대상으로 실행했을 때 수집 결과에 접미형 파일이 포함되고, 소스에 유사도·fuzzy 매칭 함수가 도입되지 않았다. [exact]
- [ ] SC-04: `harness/skills/sprint/SKILL.md` 의 QA iteration 카운터가 plain 파일만 세지 않고 **해당 스프린트의 피드백 파일**을 대상으로 한다. 측정: 해당 파일에서 카운터 복원 절차가 슬러그 대응 파일을 가리키고, plain 고정 경로만 세는 서술이 남아 있지 않다. [exact]
- [ ] SC-05: trigger-check 스크립트 중 sprint-feedback 을 실제로 읽는 것만 접미형을 인식하도록 갱신한다. 대상 판정: `harness/skills/harness-kaizen/scripts/trigger-check.sh`(읽음 — 갱신 필요), `harness/skills/contract-kaizen/scripts/trigger-check.sh` · `harness/skills/evaluator-kaizen/scripts/trigger-check.sh` · `flutter-toolkit/skills/flutter-kaizen/scripts/trigger-check.sh`(읽지 않음 — 근거와 함께 N/A 기록). 측정: 4 개 파일 각각에 대해 갱신 또는 N/A 근거가 리포트에 명시된다. [exact, enumerated]

## Error

- [ ] ER-01: 식별 수단·로그가 없는 환경에서 degrade 한다 — (a) `CLAUDE_CODE_SESSION_ID` 부재 시 ladder 2 단계를 건너뛰고 3·4 로 진행하며 부재 자체가 BLOCKED 사유가 아니고, (b) reflect-kit prompt 로그 부재 시 correction audit 이 `unavailable` 로 degrade 하고 기존 QA 를 계속한다. 측정: 두 degrade 경로가 문서에 각 1 건 이상 명시된다. [structural, enumerated]
- [ ] ER-02: 계약 선택이 모호할 때 조용히 하나를 고르지 않는다. 측정: qa-evaluator 문서에 "가장 최근" · "임의 선택" 류의 fallback 이 없고, 모호 시 후보를 나열하고 BLOCKED 한다는 서술이 존재한다. [exact]

## Anti-patterns

- [ ] AP-02: force push 를 사용하지 않는다. 측정: 이 스프린트의 셸 실행 이력과 변경 파일에 `git push --force` / `-f` 가 0 건. [exact]
- [ ] AP-03: bare code fence 0 건. 측정: `python3 scripts/validate-plugin.py` 의 V6 가 전 킷에서 `0 bare` 를 보고한다. [exact]

## Reusability

- [ ] RE-01: 경로 해석·슬러그 도출 규약을 한 곳에 정의하고 나머지는 인용한다. 측정: 규약 정의문이 `harness/references/contract-schema.md` 에만 있고, sprint-contract SKILL·qa-evaluator 는 그 문서를 인용하는 형태다(각자 다른 규약을 재정의하지 않는다). [structural]
- [ ] RE-02: project-id 계산 결과가 reflect-kit 의 canonicalization 과 일치한다. 측정: 같은 디렉토리에 대해 양쪽이 같은 값을 산출한다. 구현이 기존 헬퍼를 재사용하든 동등 로직을 두든 무관하다. [exact]

## Diagnostics

- [ ] DG-01: project.yaml `commands.analyze` 가 통과한다. 측정: `bash -n scripts/release.sh` Exit 0. [exact]
- [ ] DG-02: project.yaml `commands.test` 실행 시 예외·스택트레이스가 없다. 측정: `bash scripts/release.sh 2>&1 || true` 출력에 Traceback·syntax error 가 0 건 (인자 없이 usage 를 출력하고 종료하는 것은 정상 동작이며 FAIL 이 아니다). [exact]
- [ ] DG-03: 이번 스프린트에서 수정한 파일 전부가 문법 검증을 통과하고 회귀가 없다. 대상 결정: `git diff --name-only <스프린트 시작 커밋>..HEAD`. 측정: 그 목록 중 `*.sh` 는 `bash -n` Exit 0, `*.py` 는 `python3 -m py_compile` Exit 0, 그리고 `python3 scripts/validate-plugin.py` 가 11 plugins / 11 OK / Exit 0. [exact]
